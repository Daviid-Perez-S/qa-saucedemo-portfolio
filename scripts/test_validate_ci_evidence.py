"""Synthetic publication contracts. No browsers, real results, or third-party libraries.

Run: python -B -m unittest discover -s scripts -p test_validate_ci_evidence.py -v
An optional CI_EVIDENCE_BASELINE script enables exact strict-mode regression checks.
"""

from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).with_name("validate-ci-evidence.py")
SPEC = importlib.util.spec_from_file_location("validator", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


class Fixture:
    """Clearly synthetic identities and URLs, isolated from SauceDemo history."""

    def __init__(self, target, suite):
        self.target, self.suite = target, suite
        self.directory = target / "allure-results"
        self.directory.mkdir(parents=True)
        (target / "surefire-reports" / "junitreports").mkdir(parents=True)
        self.xml = target / "surefire-reports" / "TEST-synthetic.xml"
        self.root = ET.Element("testsuite", tests=str(VALIDATOR.COUNTS[suite]),
                               failures="0", errors="0", skipped="0")
        self.results, self.evidence = [], {}
        classname = ("com.david.qa.tests.SyntheticTest" if suite == "functional" else
                     "com.david.qa.tests.accessibility.AccessibilityTest")
        for index in range(VALIDATOR.COUNTS[suite]):
            method = f"syntheticCase{index}"
            ET.SubElement(self.root, "testcase", classname=classname, name=method)
            result = {"uuid": f"synthetic-test-{index}", "fullName": f"{classname}.{method}",
                      "name": f"SYNTHETIC-{index}", "status": "passed", "stage": "finished",
                      "start": 1000, "stop": 2000, "attachments": []}
            if suite == "accessibility":
                case_id = list(VALIDATOR.STATES)[index]
                result["name"] = f"{case_id}: synthetic contract only"
                states = []
                for state_key in sorted(VALIDATOR.STATES[case_id]):
                    scan = {"caseId": case_id, "runId": "synthetic-run", "stateKey": state_key,
                            "executionStatus": "Completed", "preparationCompleted": True,
                            "url": "https://example.invalid/synthetic-contract",
                            "startedAt": "2026-10-13T10:00:00Z",
                            "finishedAt": "2026-10-13T10:00:01Z",
                            "environment": {"browser": "synthetic"},
                            "incompleteReviewStatus": "Not Required"}
                    states.append(deepcopy(scan))
                    scan["axe"] = {"testEngine": {"version": "4.13.0"}, "url": scan["url"],
                                   "timestamp": scan["startedAt"],
                                   **{category: [] for category in VALIDATOR.CATEGORIES}}
                    self.attach_json(result, f"{case_id}-{state_key}.json", scan)
                manifest = {"caseId": case_id, "runId": "synthetic-run", "states": states,
                            "requiredScans": len(states), "completedScans": len(states),
                            "outcome": "PASS", "technicalErrors": [], "violationRuleOccurrences": 0}
                self.attach_json(result, f"{case_id}-manifest.json", manifest)
            self.results.append(result)
        self.container = {"uuid": "synthetic-container",
                          "children": [result["uuid"] for result in self.results]}

    def attach_json(self, result, source, value):
        result["attachments"].append({"name": "Synthetic evidence", "type": "application/json",
                                      "source": source})
        self.evidence[source] = value

    def fail(self, status="failed", xml_tag="failure"):
        self.root.set("errors" if xml_tag == "error" else "failures", "1")
        ET.SubElement(self.root[0], xml_tag, type="SyntheticFailure").text = "Synthetic failure"
        self.results[0].update(status=status, statusDetails={"message": "Synthetic failure",
                                                           "trace": "SyntheticFailure: contract"})

    def scan(self):
        return next(item for item in self.evidence.values() if "stateKey" in item)

    def manifest(self):
        return self.evidence["A11Y-AUTO-001-manifest.json"]

    def violation(self):
        self.fail()
        self.scan()["axe"]["violations"] = [{"id": "synthetic-rule", "nodes": []}]
        self.manifest().update(outcome="FAIL", violationRuleOccurrences=1)

    def incomplete(self):
        self.scan()["axe"]["incomplete"] = [{"id": "synthetic-review", "nodes": []}]
        self.scan()["incompleteReviewStatus"] = "Pending"
        self.manifest()["states"][0]["incompleteReviewStatus"] = "Pending"

    def save(self):
        ET.ElementTree(self.root).write(self.xml, encoding="utf-8", xml_declaration=True)
        for result in self.results:
            write_json(self.directory / f"{result['uuid']}-result.json", result)
        write_json(self.directory / f"{self.container['uuid']}-container.json", self.container)
        for source, item in self.evidence.items():
            write_json(self.directory / source, item)


class PublicationContracts(unittest.TestCase):
    scenario_count = 0

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="publication-contract-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def check(self, name, suite, mutate=None, after_save=None, publication=1, strict=1):
        fixture = Fixture(self.root / name, suite)
        if mutate:
            mutate(fixture)
        fixture.save()
        if after_save:
            after_save(fixture)
        arguments = [suite, "--target", str(fixture.target)]
        results = {}
        for mode, code in (("publication", publication), ("strict", strict)):
            command = [sys.executable, "-B", str(SCRIPT), *arguments]
            if mode == "publication":
                command.append("--publication")
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, code, f"{name} / {mode}: {result.stderr}")
            self.assertIn(("Publication evidence" if mode == "publication" else "Evidence integrity")
                          + (" PASS:" if code == 0 else " FAIL:"), result.stdout + result.stderr)
            results[mode] = result
        baseline = os.environ.get("CI_EVIDENCE_BASELINE")
        if baseline:
            original = subprocess.run([sys.executable, "-B", baseline, *arguments],
                                      capture_output=True, text=True, check=False)
            current = results["strict"]
            self.assertEqual((current.returncode, current.stdout, current.stderr),
                             (original.returncode, original.stdout, original.stderr), name)
        type(self).scenario_count += 1
        return fixture, results

    def test_successful_suites_and_incomplete_human_review(self):
        for suite in VALIDATOR.COUNTS:
            self.check(f"success-{suite}", suite, publication=0, strict=0)
        _, results = self.check("incomplete-review", "accessibility", lambda f: f.incomplete(),
                                publication=0, strict=0)
        self.assertIn("human review", results["publication"].stdout)
        self.assertIn("WCAG conformance is not established", results["publication"].stdout)

    def test_documented_failures_are_publishable(self):
        for suite in VALIDATOR.COUNTS:
            for status, tag in (("failed", "failure"), ("broken", "failure"), ("broken", "error")):
                self.check(f"{suite}-{status}-{tag}", suite,
                           lambda f, s=status, t=tag: f.fail(s, t), publication=0)
        def screenshot(f):
            f.fail()
            f.results[0]["steps"] = [{"attachments": [
                {"name": "Browser screenshot", "type": "image/png", "source": "synthetic.png"},
                {"name": "Current URL", "type": "text/plain", "source": "synthetic.txt"}]}]
        def files(f):
            (f.directory / "synthetic.png").write_bytes(b"\x89PNG\r\n\x1a\nsynthetic")
            (f.directory / "synthetic.txt").write_text("https://example.invalid", encoding="utf-8")
        self.check("nested-failure-attachments", "functional", screenshot, files, publication=0)
        self.check("axe-violation", "accessibility", lambda f: f.violation(), publication=0)
        def case_error(f):
            f.fail("broken")
            f.manifest().update(outcome="Technical Error", technicalErrors=[
                {"stage": "case", "exception": "SyntheticError", "stackTrace": "Synthetic trace"}])
        self.check("case-error-with-complete-scans", "accessibility", case_error, publication=0)

    def test_outcome_and_execution_integrity(self):
        changes = {
            "surefire-allure-disagree": lambda f: f.results[0].update(status="failed"),
            "unknown-status": lambda f: f.results[0].update(status="unknown"),
            "allure-skipped": lambda f: f.results[0].update(status="skipped"),
            "unfinished": lambda f: f.results[0].update(stage="running"),
            "reversed-time": lambda f: f.results[0].update(stop=999),
            "missing-time": lambda f: f.results[0].pop("start"),
            "missing-result": lambda f: f.results.pop(),
            "different-test": lambda f: f.results[0].update(fullName="other.test"),
            "duplicate-test": lambda f: f.results[1].update(fullName=f.results[0]["fullName"]),
            "duplicate-uuid": lambda f: f.results[1].update(uuid=f.results[0]["uuid"]),
            "dangling-container": lambda f: f.container["children"].append("missing-test"),
            "duplicate-child": lambda f: f.container["children"].append(f.container["children"][0]),
            "conflicting-uuid": lambda f: f.container.update(uuid=f.results[0]["uuid"]),
        }
        stricter_only = {"unfinished", "reversed-time", "missing-time", "duplicate-child", "conflicting-uuid"}
        for name, change in changes.items():
            with self.subTest(name=name):
                self.check(name, "functional", change, strict=0 if name in stricter_only else 1)
        def skipped(f):
            f.root.set("skipped", "1")
            ET.SubElement(f.root[0], "skipped")
            f.results[0]["status"] = "skipped"
        self.check("xml-skipped", "functional", skipped)
        def conflicting(f):
            f.fail()
            ET.SubElement(f.root[0], "error")
            f.root.set("errors", "1")
        self.check("xml-conflicting-outcomes", "functional", conflicting)
        def mismatch(f):
            f.fail()
            f.root.set("failures", "0")
        self.check("xml-counter-mismatch", "functional", mismatch)
        def missing_details(f):
            f.fail()
            f.results[0].pop("statusDetails")
        self.check("missing-failure-details", "functional", missing_details)

    def test_file_and_attachment_integrity(self):
        def failed_attachment(f):
            f.fail()
            f.results[0]["attachments"] = [{"name": "Synthetic", "type": "text/plain",
                                              "source": "missing.txt"}]
        self.check("missing-attachment", "functional", failed_attachment)
        self.check("empty-attachment", "functional", failed_attachment,
                   lambda f: (f.directory / "missing.txt").write_bytes(b""))
        for source in ("../outside.txt", "..\\outside.txt", "file:stream", "", "."):
            def unsafe(f, value=source):
                failed_attachment(f)
                f.results[0]["attachments"][0]["source"] = value
            self.check(f"unsafe-{len(list(self.root.iterdir()))}", "functional", unsafe)
        self.check("invalid-json", "functional", after_save=lambda f:
                   (f.directory / "synthetic-test-0-result.json").write_text("{", encoding="utf-8"))
        self.check("invalid-xml", "functional", after_save=lambda f:
                   f.xml.write_text("<", encoding="utf-8"))
        self.check("filename-mismatch", "functional", after_save=lambda f:
                   (f.directory / "synthetic-test-0-result.json").rename(f.directory / "other-result.json"),
                   strict=0)
        self.check("nested-result-directory", "functional", after_save=lambda f:
                   (f.directory / "unexpected").mkdir(), strict=0)
        self.check("missing-suite-directory", "functional", after_save=lambda f:
                   f.xml.rename(f.xml.with_suffix(".txt")))
        self.check("success-with-attachments", "accessibility", after_save=lambda f:
                   write_json(f.directory / "synthetic-container-container.json", {
                       **f.container, "befores": [{"attachments": [
                           {"type": "text/plain", "source": "missing-fixture.txt"}]}]}))

    def test_accessibility_scan_integrity(self):
        changes = {
            "scan-not-executed": lambda f: f.scan().update(executionStatus="Not Executed"),
            "scan-technical-error": lambda f: f.scan().update(executionStatus="Technical Error"),
            "preparation-incomplete": lambda f: f.scan().update(preparationCompleted=False),
            "wrong-engine": lambda f: f.scan()["axe"]["testEngine"].update(version="wrong"),
            "missing-category": lambda f: f.scan()["axe"].pop("incomplete"),
            "invalid-category": lambda f: f.scan()["axe"].update(passes=None),
            "invalid-nodes": lambda f: f.scan()["axe"].update(passes=[{"id": "rule", "nodes": None}]),
            "duplicate-rules": lambda f: f.scan()["axe"].update(passes=[{"id": "rule", "nodes": []}] * 2),
            "wrong-axe-url": lambda f: f.scan()["axe"].update(url="https://example.invalid/wrong"),
            "mixed-runs": lambda f: f.scan().update(runId="other-run"),
            "duplicate-state": lambda f: f.scan().update(stateKey="login-invalid-credentials"),
            "manifest-scan-disagree": lambda f: f.manifest()["states"][0].update(url="other"),
            "missing-scan-metadata": lambda f: (f.scan().pop("environment"),
                                               f.manifest()["states"][0].pop("environment")),
            "errored-axe": lambda f: f.scan()["axe"].update(errored=True),
            "invalid-scan-time": lambda f: (f.scan().update(finishedAt="invalid"),
                                           f.manifest()["states"][0].update(finishedAt="invalid")),
            "incorrect-review-status": lambda f: (f.incomplete(), f.scan().update(incompleteReviewStatus="Not Required"),
                                                  f.manifest()["states"][0].update(incompleteReviewStatus="Not Required")),
        }
        stricter_only = {"missing-scan-metadata", "errored-axe", "invalid-scan-time", "incorrect-review-status"}
        for name, change in changes.items():
            with self.subTest(name=name):
                self.check(name, "accessibility", change, strict=0 if name in stricter_only else 1)
        self.check("missing-scan-file", "accessibility", after_save=lambda f:
                   (f.directory / f.results[0]["attachments"][0]["source"]).unlink())
        self.check("missing-manifest-file", "accessibility", after_save=lambda f:
                   (f.directory / "A11Y-AUTO-001-manifest.json").unlink())
        def duplicate_attachment(f):
            f.results[0]["steps"] = [{"attachments": [f.results[0]["attachments"][0]]}]
        self.check("duplicate-attachment-reference", "accessibility", duplicate_attachment)
        def numeric_run_id(f):
            for item in f.evidence.values():
                item["runId"] = 1
        self.check("invalid-run-id", "accessibility", numeric_run_id, strict=0)
        def invalid_timestamps(f):
            f.scan()["finishedAt"] = "2026-10-13T09:59:59Z"
            f.manifest()["states"][0]["finishedAt"] = f.scan()["finishedAt"]
        self.check("reversed-scan-time", "accessibility", invalid_timestamps, strict=0)

    def test_accessibility_manifest_and_test_consistency(self):
        changes = {
            "violation-count-mismatch": lambda f: (f.violation(), f.manifest().update(violationRuleOccurrences=0)),
            "violation-hidden-as-pass": lambda f: (f.violation(), f.manifest().update(outcome="PASS")),
            "violation-passed-test": lambda f: (f.violation(), f.results[0].update(status="passed"),
                                               f.root[0].remove(f.root[0].find("failure")), f.root.set("failures", "0")),
            "unexpected-manifest-case": lambda f: f.manifest().update(caseId="other"),
            "missing-manifest-state": lambda f: f.manifest()["states"].pop(),
            "wrong-completed-count": lambda f: f.manifest().update(completedScans=1),
            "wrong-required-count": lambda f: f.manifest().update(requiredScans=1),
            "invalid-technical-errors": lambda f: (f.fail("broken"), f.manifest().update(
                outcome="Technical Error", technicalErrors=[{}])),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                self.check(name, "accessibility", change)
        def wrong_owner(f):
            f.results[0]["steps"] = [{"attachments": [f.results[1]["attachments"].pop(0)]}]
        self.check("nested-evidence-wrong-owner", "accessibility", wrong_owner)
        self.check("unattached-manifest", "accessibility", lambda f: f.results[0]["attachments"].pop())
        def boolean_count(f):
            f.evidence["A11Y-AUTO-005-manifest.json"].update(requiredScans=True, completedScans=True)
        self.check("boolean-scan-count", "accessibility", boolean_count, strict=0)

    def test_links_are_rejected_without_following_them(self):
        fixture = Fixture(self.root / "links", "functional")
        fixture.save()
        targets = (fixture.target, fixture.directory, fixture.xml,
                   fixture.directory / "synthetic-test-0-result.json")
        for method in ("is_symlink", "is_junction"):
            for target in targets:
                with self.subTest(method=method, target=target.name):
                    with patch.object(Path, method, autospec=True, side_effect=lambda p, t=target: p == t):
                        with self.assertRaises(ValueError):
                            VALIDATOR.validate_publication_files(fixture.target)


if __name__ == "__main__":
    unittest.main(verbosity=2)
