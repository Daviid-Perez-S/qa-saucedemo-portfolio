"""Validate one CI suite's existing Surefire, Allure and axe evidence."""

import argparse
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


def validate_surefire(target, suite):
    files = sorted((target / "surefire-reports").glob("TEST-*.xml"))
    require(files, "No Surefire TEST-*.xml files")
    names = []
    for path in files:
        root = ET.parse(path).getroot()
        require(root.tag == "testsuite", f"Unexpected Surefire XML: {path}")
        cases = root.findall("testcase")
        require(int(root.attrib["tests"]) == len(cases), f"XML count mismatch: {path}")
        for key in ("failures", "errors", "skipped"):
            require(int(root.attrib[key]) == 0, f"Surefire {key}: {path}")
        for case in cases:
            require(not any(case.find(tag) is not None for tag in
                            ("failure", "error", "skipped")), "Unsuccessful XML testcase")
            classname = case.attrib["classname"]
            if suite == "functional":
                require(classname.rsplit(".", 1)[0] == "com.david.qa.tests",
                        f"Non-functional test: {classname}")
            else:
                require(classname == "com.david.qa.tests.accessibility.AccessibilityTest",
                        f"Non-accessibility test: {classname}")
            names.append(f"{classname}.{case.attrib['name']}")
    unique(names, "Surefire tests")
    require(len(names) == COUNTS[suite], f"Expected {COUNTS[suite]} XML tests; got {len(names)}")
    return set(names)


def validate_allure(target, expected):
    directory = target / "allure-results"
    results = [load_json(path) for path in sorted(directory.glob("*-result.json"))]
    require(len(results) == len(expected), "Allure result count mismatch")
    unique([r.get("uuid") for r in results], "Allure result UUIDs")
    unique([r.get("fullName") for r in results], "Allure tests")
    require({r["fullName"] for r in results} == expected, "Surefire/Allure tests differ")
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
    for path in sorted(directory.glob("*.json")):
        document = load_json(path)
        for attachment in attachments(document):
            require(isinstance(attachment, dict), f"Invalid attachment in {path}")
            source = attachment.get("source")
            require(isinstance(source, str) and Path(source).name == source,
                    f"Invalid attachment source: {source}")
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
    return evidence, len(sources)


def validate_accessibility(evidence):
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
        require(not axe["violations"], f"Confirmed axe violations: {scan['stateKey']}")
        incomplete += len(axe["incomplete"])
    for manifest in manifests:
        states = manifest.get("states", [])
        unique([state.get("stateKey") for state in states], "manifest states")
        required = STATES[manifest["caseId"]]
        require({state["stateKey"] for state in states} == required and
                manifest.get("requiredScans") == len(required) and
                manifest.get("completedScans") == len(required), "Manifest count/state mismatch")
        require(manifest.get("outcome") == "PASS" and manifest.get("technicalErrors") == [] and
                manifest.get("violationRuleOccurrences") == 0 and
                all(state.get("executionStatus") == "Completed" and
                    state.get("preparationCompleted") is True and not state.get("technicalError")
                    for state in states),
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
    args = parser.parse_args()
    try:
        expected = validate_surefire(args.target, args.suite)
        evidence, count = validate_allure(args.target, expected)
        if args.suite == "accessibility":
            validate_accessibility(evidence)
        else:
            require(not evidence and count == 0, "Unexpected attachments in passed functional tests")
        print(f"Evidence integrity PASS: {args.suite}, {len(expected)} passed tests, {count} attachments")
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, ET.ParseError) as error:
        print(f"Evidence integrity FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
