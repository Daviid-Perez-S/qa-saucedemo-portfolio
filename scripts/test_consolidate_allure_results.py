"""Isolated synthetic contracts for merging and verifying Allure 3 reports.

Run: python -B -m unittest discover -s scripts -p test_consolidate_allure_results.py -v
No Maven, browsers, or historical evidence are modified by these tests.
"""

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).with_name("consolidate-allure-results.py")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MERGER = load_module("merger", SCRIPT)
FIXTURES = load_module("evidence_fixtures", SCRIPT.with_name("test_validate_ci_evidence.py"))


def fingerprint(directory):
    return {str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in directory.rglob("*") if path.is_file()}


class ConsolidationContracts(unittest.TestCase):
    scenarios = 0

    def setUp(self):
        # Keep temporary data within the already ignored verification area.
        # Some Windows sandboxes cannot use the OS temporary directory.
        area = ROOT / ".accessibility-verification" / "consolidation-contract"
        area.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="synthetic-", dir=area)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def fixtures(self, name, mutate=None):
        functional = FIXTURES.Fixture(self.root / name / "functional", "functional")
        accessibility = FIXTURES.Fixture(self.root / name / "accessibility", "accessibility")
        for result in accessibility.results:
            result["uuid"] = "accessibility-" + result["uuid"]
        accessibility.container.update(uuid="accessibility-container",
                                       children=[item["uuid"] for item in accessibility.results])
        if mutate:
            mutate(functional, accessibility)
        functional.save()
        accessibility.save()
        return functional, accessibility

    def merge(self, name, mutate=None, after=None, code=1, message=None):
        functional, accessibility = self.fixtures(name, mutate)
        output = self.root / name / "combined"
        if after:
            after(functional, accessibility, output)
        before = [fingerprint(item.target) for item in (functional, accessibility)]
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "merge",
                                 "--functional", str(functional.target),
                                 "--accessibility", str(accessibility.target), "--output", str(output)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertEqual(before, [fingerprint(item.target) for item in (functional, accessibility)])
        if message:
            self.assertIn(message, result.stdout + result.stderr)
        if code == 0:
            expected = {path.name: path.read_bytes() for item in (functional, accessibility)
                        for path in item.directory.iterdir() if path.name not in MERGER.REPORT_METADATA}
            self.assertEqual(expected, {path.name: path.read_bytes() for path in output.iterdir()})
        elif not (output / "sentinel.txt").exists():
            self.assertFalse(output.exists(), "Failed preflight created output")
        type(self).scenarios += 1
        return output, functional, accessibility

    def test_success_and_explicit_report_metadata_exclusion(self):
        self.merge("success", code=0, message="21 tests")
        def metadata(f, a, output):
            for item in (f, a):
                FIXTURES.write_json(item.directory / "executor.json", {"name": "Synthetic partial report"})
                (item.directory / "allure.properties").write_text("allure.results.directory=synthetic", encoding="utf-8")
        self.merge("metadata", after=metadata, code=0, message="metadata excluded explicitly")

    def test_failed_and_broken_results_are_preserved(self):
        def failures(f, a):
            f.fail("broken")
            a.violation()
            f.results[0]["attachments"] = [{"name": "Synthetic URL", "type": "text/plain",
                                             "source": "synthetic-url.txt"}]
        def url(f, a, output):
            (f.directory / "synthetic-url.txt").write_text("https://example.invalid", encoding="utf-8")
        output, _, _ = self.merge("failed", failures, url, code=0)
        states = Counter(item["status"] for item in MERGER.inventory(output)["results"])
        self.assertEqual(states, {"passed": 19, "failed": 1, "broken": 1})

    def test_collisions_and_incomplete_evidence_fail_before_copy(self):
        changes = {
            "result-container-uuid": lambda f, a: a.container.update(uuid=f.results[0]["uuid"]),
            "container-uuid": lambda f, a: a.container.update(uuid=f.container["uuid"]),
            "history-id": lambda f, a: (f.results[0].update(historyId="duplicate-history"),
                                       a.results[0].update(historyId="duplicate-history")),
            "test-case-id": lambda f, a: (f.results[0].update(testCaseId="duplicate-case"),
                                         a.results[0].update(testCaseId="duplicate-case")),
            "incomplete-scan": lambda f, a: a.scan().update(executionStatus="Not Executed"),
            "wrong-test-identity": lambda f, a: a.results[0].update(fullName=f.results[0]["fullName"]),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                self.merge(name, change)
        def shared(f, a):
            f.fail()
            a.fail()
            f.results[0]["attachments"] = [{"name": "Synthetic", "type": "text/plain", "source": "shared.txt"}]
            a.results[0]["attachments"].append({"name": "Synthetic", "type": "text/plain", "source": "SHARED.txt"})
        def shared_files(f, a, output):
            (f.directory / "shared.txt").write_text("same bytes", encoding="utf-8")
            (a.directory / "SHARED.txt").write_text("same bytes", encoding="utf-8")
        self.merge("attachment-collision", shared, shared_files, message="attachment references")
        self.merge("missing-json", after=lambda f, a, o:
                   (a.directory / a.results[0]["attachments"][0]["source"]).unlink())
        self.merge("orphan-file", after=lambda f, a, o:
                   (f.directory / "orphan.txt").write_text("synthetic", encoding="utf-8"), message="unsupported")
        self.merge("downloaded-config", after=lambda f, a, o:
                   FIXTURES.write_json(a.directory / "allurerc.json", {}), message="unsupported")

    def test_output_is_never_overwritten_or_placed_in_an_input(self):
        def existing(f, a, output):
            output.mkdir()
            (output / "sentinel.txt").write_text("keep", encoding="utf-8")
        output, _, _ = self.merge("existing", after=existing, message="Output already exists")
        self.assertEqual((output / "sentinel.txt").read_text(), "keep")
        f, a = self.fixtures("inside-input")
        with self.assertRaisesRegex(ValueError, "outside both input"):
            MERGER.consolidate(f.target, a.target, f.target / "new-results")

    def test_global_identity_and_filename_checks(self):
        f, a = self.fixtures("global-checks")
        inputs = [MERGER.inventory(item.directory) for item in (f, a)]
        inputs[1]["results"][0]["fullName"] = inputs[0]["results"][0]["fullName"]
        with self.assertRaisesRegex(ValueError, "test identities"):
            MERGER.check_collisions(inputs)
        inputs = [MERGER.inventory(item.directory) for item in (f, a)]
        inputs[1]["files"].append(inputs[0]["files"][0])
        with self.assertRaisesRegex(ValueError, "filenames"):
            MERGER.check_collisions(inputs)

    def make_report(self, name):
        results, _, _ = self.merge(name, code=0)
        report = self.root / name / "report"
        (report / "data" / "test-results").mkdir(parents=True)
        (report / "data" / "attachments").mkdir()
        (report / "widgets").mkdir()
        (report / "index.html").write_text('<html><script src="app.js"></script></html>', encoding="utf-8")
        (report / "app.js").write_text("/* Synthetic report contract; not a rendered Allure app. */", encoding="utf-8")
        for result in MERGER.inventory(results)["results"]:
            links = []
            for attachment in MERGER.attachments(result):
                content = (results / attachment["source"]).read_bytes()
                identity = hashlib.sha256(content).hexdigest()
                extension = Path(attachment["source"]).suffix
                (report / "data" / "attachments" / (identity + extension)).write_bytes(content)
                links.append({"type": "attachment", "link": {"used": True, "missed": False,
                    "id": identity, "ext": extension, "originalFileName": attachment["source"]}})
            FIXTURES.write_json(report / "data" / "test-results" / (result["uuid"] + ".json"), {
                "name": result["name"], "fullName": result["fullName"], "status": result["status"],
                "isRetry": False, "retries": [], "steps": links, "attachments": links})
        FIXTURES.write_json(report / "widgets" / "statistic.json", {"total": 21, "passed": 21})
        return results, report

    def test_rendered_states_assets_and_attachments_are_verified(self):
        results, report = self.make_report("rendered-success")
        MERGER.verify_report(results, report)
        changes = {
            "missing-entry": lambda p: (p / "index.html").unlink(),
            "missing-app": lambda p: (p / "app.js").unlink(),
            "missing-test": lambda p: next((p / "data" / "test-results").glob("*.json")).unlink(),
            "missing-attachment": lambda p: next((p / "data" / "attachments").iterdir()).unlink(),
            "changed-attachment": lambda p: next((p / "data" / "attachments").iterdir()).write_bytes(b"changed"),
            "wrong-summary": lambda p: FIXTURES.write_json(p / "widgets" / "statistic.json", {"total": 20, "passed": 20}),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                results, report = self.make_report(name)
                change(report)
                with self.assertRaises(ValueError):
                    MERGER.verify_report(results, report)
        for key, value in (("status", "failed"), ("fullName", "other"), ("name", "changed"), ("isRetry", True)):
            with self.subTest(key=key):
                results, report = self.make_report("wrong-" + key)
                path = next((report / "data" / "test-results").glob("*.json"))
                item = MERGER.load_json(path)
                item[key] = value
                FIXTURES.write_json(path, item)
                with self.assertRaises(ValueError):
                    MERGER.verify_report(results, report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
