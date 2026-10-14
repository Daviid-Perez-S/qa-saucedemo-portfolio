"""Validate one CI suite's existing Surefire, Allure and axe evidence."""

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


COUNTS = {"functional": 15, "accessibility": 6}
STATES = {
    "A11Y-AUTO-001": {"login-initial", "login-invalid-credentials"},
    "A11Y-AUTO-002": {"products-initial", "products-product-added", "products-menu-open"},
    "A11Y-AUTO-003": {"cart-with-product", "cart-empty"},
    "A11Y-AUTO-004": {"checkout-information-initial", "checkout-error-first-name",
                      "checkout-error-last-name", "checkout-error-postal-code"},
    "A11Y-AUTO-005": {"checkout-overview"},
    "A11Y-AUTO-006": {"checkout-complete"},
}
CATEGORIES = ("passes", "violations", "incomplete", "inapplicable")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(values, label):
    require(all(isinstance(value, str) and value for value in values),
            f"Missing or invalid {label}")
    require(len(values) == len(set(values)), f"Duplicate {label}")


def load_json(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"Invalid JSON object: {path}")
    return value


def attachments(node):
    """Include attachments in steps and configuration fixtures, not just roots."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "attachments":
                require(isinstance(value, list), "Invalid Allure attachments list")
                yield from value
            else:
                yield from attachments(value)
    elif isinstance(node, list):
        for value in node:
            yield from attachments(value)


def validate_surefire(target, suite, publication=False):
    files = sorted((target / "surefire-reports").glob("TEST-*.xml"))
    require(files, "No Surefire TEST-*.xml files")
    names = []
    outcomes = {}
    for path in files:
        root = ET.parse(path).getroot()
        require(root.tag == "testsuite", f"Unexpected Surefire XML: {path}")
        cases = root.findall("testcase")
        require(int(root.attrib["tests"]) == len(cases), f"XML count mismatch: {path}")
        for key in ("failures", "errors", "skipped"):
            if publication:
                tag = {"failures": "failure", "errors": "error", "skipped": "skipped"}[key]
                require(int(root.attrib[key]) == sum(case.find(tag) is not None for case in cases),
                        f"XML {key} count mismatch: {path}")
            else:
                require(int(root.attrib[key]) == 0, f"Surefire {key}: {path}")
        for case in cases:
            if publication:
                require(case.find("skipped") is None, "Skipped XML testcase is not publishable")
                require(sum(len(case.findall(tag)) for tag in ("failure", "error")) <= 1,
                        "Conflicting XML testcase outcomes")
            else:
                require(not any(case.find(tag) is not None for tag in
                                ("failure", "error", "skipped")), "Unsuccessful XML testcase")
            classname = case.attrib["classname"]
            if suite == "functional":
                require(classname.rsplit(".", 1)[0] == "com.david.qa.tests",
                        f"Non-functional test: {classname}")
            else:
                require(classname == "com.david.qa.tests.accessibility.AccessibilityTest",
                        f"Non-accessibility test: {classname}")
            name = f"{classname}.{case.attrib['name']}"
            names.append(name)
            outcomes[name] = "unsuccessful" if any(case.find(tag) is not None for tag in
                                                  ("failure", "error")) else "passed"
    unique(names, "Surefire tests")
    require(len(names) == COUNTS[suite], f"Expected {COUNTS[suite]} XML tests; got {len(names)}")
    return outcomes if publication else set(names)


def validate_allure(target, expected, publication=False):
    directory = target / "allure-results"
    results = [load_json(path) for path in sorted(directory.glob("*-result.json"))]
    require(len(results) == len(expected), "Allure result count mismatch")
    unique([r.get("uuid") for r in results], "Allure result UUIDs")
    unique([r.get("fullName") for r in results], "Allure tests")
    require({r["fullName"] for r in results} == set(expected), "Surefire/Allure tests differ")
    if publication:
        for result in results:
            status = result.get("status")
            require(status in ("passed", "failed", "broken"), "Non-final Allure test status")
            # TestNG's Surefire XML uses failure for both assertion and runtime failures.
            require((status == "passed") == (expected[result["fullName"]] == "passed"),
                    f"Surefire/Allure outcomes differ: {result['fullName']}")
            require(result.get("stage") == "finished", "Unfinished Allure test")
            require(all(type(result.get(key)) is int and result[key] >= 0 for key in
                        ("start", "stop")) and result["stop"] >= result["start"],
                    "Invalid Allure test timestamps")
            if status != "passed":
                details = result.get("statusDetails", {})
                require(isinstance(details, dict) and any(
                    isinstance(details.get(key), str) and details[key].strip()
                    for key in ("message", "trace")), "Missing Allure failure details")
    else:
        require(all(r.get("status") == "passed" for r in results), "Non-passed Allure result")
    evidence = []
    sources = []
    # Containers also reference configuration evidence and test result UUIDs.
    container_ids = []
    for path in sorted(directory.glob("*-container.json")):
        container = load_json(path)
        container_ids.append(container.get("uuid"))
        require(set(container.get("children", [])) <= {r["uuid"] for r in results},
                f"Container references missing results: {path}")
    unique(container_ids, "Allure container UUIDs")
    if publication:
        unique([r["uuid"] for r in results] + container_ids, "Allure result/container UUIDs")
    for path in sorted(directory.glob("*.json")):
        document = load_json(path)
        for attachment in attachments(document):
            require(isinstance(attachment, dict), f"Invalid attachment in {path}")
            source = attachment.get("source")
            require(isinstance(source, str) and Path(source).name == source,
                    f"Invalid attachment source: {source}")
            if publication:
                require(source not in ("", ".", "..") and not any(c in source for c in "/\\:"),
                        f"Unsafe attachment source: {source}")
            attached = directory / source
            require(attached.is_file() and attached.stat().st_size > 0,
                    f"Missing or empty attachment: {source}")
            sources.append(source)
            if attachment.get("type") == "application/json" or attached.suffix == ".json":
                item = load_json(attached)
                if "caseId" in item and "fullName" in document:
                    require(item["caseId"] == document.get("name", "").split(":", 1)[0],
                            "Accessibility attachment belongs to a different test")
                evidence.append(item)
    unique(sources, "Allure attachment references")
    if publication:
        for result in results:
            validate_publication_attachments(result, directory)
    return evidence, len(sources)


def validate_publication_files(target):
    """Treat downloaded evidence as data; reject links and nested file paths."""
    require(target.is_dir() and not target.is_symlink() and not target.is_junction(),
            "Invalid evidence directory")
    for name in ("surefire-reports", "allure-results"):
        directory = target / name
        require(directory.is_dir() and not directory.is_symlink() and not directory.is_junction(),
                f"Invalid directory: {name}")
        # Surefire also contains TestNG HTML subdirectories, which we never consume.
        paths = directory.glob("TEST-*.xml") if name == "surefire-reports" else directory.iterdir()
        for path in paths:
            require(path.is_file() and not path.is_symlink() and not path.is_junction(),
                    f"Non-regular evidence file: {path}")
    directory = target / "allure-results"
    for kind in ("result", "container"):
        for path in directory.glob(f"*-{kind}.json"):
            document = load_json(path)
            require(path.name == f"{document.get('uuid')}-{kind}.json",
                    f"Allure UUID/filename mismatch: {path.name}")
            if kind == "container":
                children = document.get("children")
                require(isinstance(children, list), "Invalid Allure container children")
                unique(children, "Allure container child references")


def validate_publication_attachments(result, directory):
    """Bind accessibility evidence to its owning test, including nested attachments."""
    attached = list(attachments(result))
    if result["fullName"].startswith("com.david.qa.tests.accessibility."):
        case_id = result.get("name", "").split(":", 1)[0]
        require(case_id in STATES, "Missing or unexpected accessibility case ID")
        items = [load_json(directory / item["source"]) for item in attached
                 if item.get("type") == "application/json" or item["source"].endswith(".json")]
        require(all(item.get("caseId") == case_id for item in items),
                "Accessibility evidence belongs to a different test")
        scans = [item for item in items if "stateKey" in item]
        manifests = [item for item in items if "requiredScans" in item]
        require(len(manifests) == 1 and len(scans) == len(STATES[case_id]) and
                {scan.get("stateKey") for scan in scans} == STATES[case_id] and
                len(items) == len(scans) + 1, "Missing or unexpected test accessibility attachments")
        require(manifests[0].get("outcome") == "PASS" or result["status"] in ("failed", "broken"),
                "Unsuccessful accessibility manifest in a passed Allure test")
    elif result["status"] == "passed":
        require(not attached, "Unexpected attachments in passed functional tests")
    else:
        require(all(item.get("type") in ("image/png", "text/plain") for item in attached),
                "Unexpected functional failure attachment type")


def validate_publication_scan(scan, axe):
    require(isinstance(scan.get("url"), str) and scan["url"] and
            isinstance(scan.get("environment"), dict) and scan["environment"],
            "Missing accessibility scan metadata")
    times = [datetime.fromisoformat(scan[key]) for key in ("startedAt", "finishedAt")]
    require(all(time.utcoffset() is not None for time in times) and times[1] >= times[0],
            "Invalid accessibility scan timestamps")
    require(not axe.get("errored") and not axe.get("error"), "Errored axe result")
    require(scan.get("incompleteReviewStatus") ==
            ("Pending" if axe["incomplete"] else "Not Required"),
            "Inconsistent incomplete human-review status")


def validate_accessibility(evidence, publication=False):
    scans = [item for item in evidence if "stateKey" in item]
    manifests = [item for item in evidence if "requiredScans" in item]
    require(len(scans) == 13 and len(manifests) == 6, "Expected 13 scans and 6 manifests")
    unique([m.get("caseId") for m in manifests], "manifest case IDs")
    require({m["caseId"] for m in manifests} == set(STATES), "Unexpected manifest cases")
    keys = [(s.get("caseId"), s.get("stateKey")) for s in scans]
    expected = {(case, state) for case, states in STATES.items() for state in states}
    require(len(set(keys)) == 13 and set(keys) == expected, "Missing, duplicate or unexpected scans")
    run_ids = {item.get("runId") for item in scans + manifests}
    require(len(run_ids) == 1 and all(run_ids), "Missing or inconsistent accessibility run IDs")
    if publication:
        require(all(isinstance(run_id, str) and run_id.strip() for run_id in run_ids),
                "Invalid accessibility run ID")
    incomplete = 0
    for scan in scans:
        require(scan.get("executionStatus") == "Completed" and
                scan.get("preparationCompleted") is True and not scan.get("technicalError"),
                f"Incomplete scan: {scan['stateKey']}")
        axe = scan.get("axe", {})
        require(axe.get("testEngine", {}).get("version") == "4.13.0" and
                axe.get("url") == scan.get("url") and axe.get("timestamp"), "Invalid axe envelope")
        for category in CATEGORIES:
            rules = axe.get(category)
            require(isinstance(rules, list), f"Missing axe category: {category}")
            unique([rule.get("id") for rule in rules], f"{category} rule IDs")
            require(all(isinstance(rule.get("nodes"), list) for rule in rules), "Invalid axe nodes")
        if publication:
            validate_publication_scan(scan, axe)
        else:
            require(not axe["violations"], f"Confirmed axe violations: {scan['stateKey']}")
        incomplete += len(axe["incomplete"])
    for manifest in manifests:
        states = manifest.get("states", [])
        unique([state.get("stateKey") for state in states], "manifest states")
        required = STATES[manifest["caseId"]]
        require({state["stateKey"] for state in states} == required and
                manifest.get("requiredScans") == len(required) and
                manifest.get("completedScans") == len(required), "Manifest count/state mismatch")
        complete = all(state.get("executionStatus") == "Completed" and
                       state.get("preparationCompleted") is True and not state.get("technicalError")
                       for state in states)
        if publication:
            require(all(type(manifest.get(key)) is int for key in ("requiredScans", "completedScans")),
                    "Invalid manifest scan counts")
            violations = sum(len(scan["axe"]["violations"]) for scan in scans
                             if scan["caseId"] == manifest["caseId"])
            errors = manifest.get("technicalErrors")
            require(isinstance(errors, list) and all(isinstance(error, dict) and
                    all(isinstance(error.get(key), str) and error[key].strip()
                        for key in ("stage", "exception", "stackTrace")) for error in errors),
                    "Invalid manifest technical errors")
            outcome = "FAIL" if violations else "Technical Error" if errors else "PASS"
            require(complete and type(manifest.get("violationRuleOccurrences")) is int and
                    manifest["violationRuleOccurrences"] == violations and
                    manifest.get("outcome") == outcome, "Inconsistent accessibility manifest outcome")
        else:
            require(manifest.get("outcome") == "PASS" and manifest.get("technicalErrors") == [] and
                    manifest.get("violationRuleOccurrences") == 0 and complete,
                    "Unsuccessful accessibility manifest")
        for state in states:
            scan = next(s for s in scans if s["caseId"] == manifest["caseId"] and
                        s["stateKey"] == state["stateKey"])
            require(all(state.get(key) == scan.get(key) for key in
                        ("url", "startedAt", "finishedAt", "environment", "incompleteReviewStatus")),
                    "Manifest and scan metadata differ")
    print(f"Accessibility evidence: 13 scans, 6 manifests; incomplete rule occurrences: {incomplete}")
    print("Incomplete findings require human review; WCAG conformance is not established.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", choices=COUNTS)
    parser.add_argument("--target", type=Path, default=Path("target"))
    parser.add_argument("--publication", action="store_true",
                        help="Check complete evidence, allowing documented test failures; does not publish")
    args = parser.parse_args()
    try:
        if args.publication:
            validate_publication_files(args.target)
        expected = validate_surefire(args.target, args.suite, args.publication)
        evidence, count = validate_allure(args.target, expected, args.publication)
        if args.suite == "accessibility":
            validate_accessibility(evidence, args.publication)
        elif args.publication:
            require(not evidence, "Unexpected JSON evidence in functional suite")
        else:
            require(not evidence and count == 0, "Unexpected attachments in passed functional tests")
        if args.publication:
            unsuccessful = sum(outcome == "unsuccessful" for outcome in expected.values())
            print(f"Publication evidence PASS: {args.suite}, {len(expected)} executed tests, "
                  f"{unsuccessful} unsuccessful tests, {count} attachments")
            print("Suite evidence is publishable; report generation and deployment are separate checks.")
        else:
            print(f"Evidence integrity PASS: {args.suite}, {len(expected)} passed tests, {count} attachments")
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, ET.ParseError) as error:
        label = "Publication evidence" if args.publication else "Evidence integrity"
        print(f"{label} FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
