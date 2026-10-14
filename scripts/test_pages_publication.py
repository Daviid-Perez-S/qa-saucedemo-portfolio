"""Offline provenance and ordering contracts; never call GitHub or deploy Pages."""

from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pages", ROOT / "scripts" / "pages-publication.py")
PAGES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PAGES)


class FakeGitHub:
    def __init__(self):
        self.responses = {}
        self.calls = []

    def get(self, path):
        self.calls.append(path)
        return deepcopy(self.responses[path])

    def items(self, path, key):
        yield from self.get(path)[key]


def fixture():
    api = FakeGitHub()
    repo = {"id": 99, "full_name": PAGES.REPOSITORY}
    run = {"id": 123, "run_number": 42, "run_attempt": 2, "workflow_id": 10,
           "repository": repo, "head_repository": repo, "name": "SauceDemo CI", "path": PAGES.CI_PATH,
           "head_branch": "master", "event": "push", "status": "completed", "conclusion": "failure",
           "head_sha": "a" * 40, "html_url": f"https://github.com/{PAGES.REPOSITORY}/actions/runs/123",
           "run_started_at": "2026-10-13T16:00:00Z"}
    event = {"repository": repo, "workflow_run": deepcopy(run)}
    api.responses[f"{PAGES.PREFIX}/workflows/ci.yml"] = {"id": 10, "name": "SauceDemo CI", "path": PAGES.CI_PATH}
    api.responses[f"{PAGES.PREFIX}/workflows/pages.yml"] = {"id": 20, "name": PAGES.PAGES_NAME, "path": PAGES.PAGES_PATH}
    api.responses[f"{PAGES.PREFIX}/runs/123/attempts/2"] = deepcopy(run)
    jobs, artifacts = [], []
    for index, (suite, (job_name, upload_name)) in enumerate(PAGES.SUITES.items()):
        minute = 5 + index
        jobs.append({"id": 100 + index, "run_id": 123, "head_sha": run["head_sha"], "status": "completed",
                     "conclusion": "failure", "name": job_name, "steps": [{"name": upload_name,
                         "status": "completed", "conclusion": "success",
                         "started_at": f"2026-10-13T16:0{minute}:00Z", "completed_at": f"2026-10-13T16:0{minute}:05Z"}]})
        artifacts.append({"id": 501 + index, "name": f"{suite}-evidence", "expired": False,
                          "size_in_bytes": 1024, "created_at": f"2026-10-13T16:0{minute}:01Z",
                          "workflow_run": {"id": 123, "head_sha": run["head_sha"], "head_branch": "master",
                                           "repository_id": 99, "head_repository_id": 99}})
    api.responses[f"{PAGES.PREFIX}/runs/123/attempts/2/jobs"] = {"jobs": jobs}
    api.responses[f"{PAGES.PREFIX}/runs/123/artifacts"] = {"artifacts": artifacts}
    api.responses[f"{PAGES.PREFIX}/workflows/pages.yml/runs"] = {"workflow_runs": []}
    return api, event, run


def publisher(api, number, source_attempt=1, identity=9001, publisher_attempt=1, deployed=None):
    source_id = 123 if number == 42 else 1000 + number
    record = {"id": identity, "workflow_id": 20, "head_branch": "master", "event": "workflow_run",
              "head_repository": {"full_name": PAGES.REPOSITORY}, "run_attempt": publisher_attempt,
              "display_title": f"Allure Pages - CI #{number} attempt {source_attempt} source {source_id}"}
    api.responses[f"{PAGES.PREFIX}/workflows/pages.yml/runs"]["workflow_runs"].append(record)
    for attempt in range(1, publisher_attempt + 1):
        conclusion = (deployed or {}).get(attempt, "skipped")
        api.responses[f"{PAGES.PREFIX}/runs/{identity}/attempts/{attempt}/jobs"] = {"jobs": [{
            "run_id": identity, "name": PAGES.DEPLOY_JOB, "steps": [{"name": PAGES.DEPLOY_STEP,
            "status": "completed", "conclusion": conclusion}]}]}
    return record


class ProvenanceContracts(unittest.TestCase):
    def test_complete_failed_ci_and_manual_runs_are_allowed(self):
        for event_name in ("push", "workflow_dispatch"):
            for conclusion in ("success", "failure"):
                with self.subTest(event=event_name, conclusion=conclusion):
                    api, event, _ = fixture()
                    event["workflow_run"].update(event=event_name, conclusion=conclusion)
                    api.responses[f"{PAGES.PREFIX}/runs/123/attempts/2"].update(event=event_name, conclusion=conclusion)
                    _, selected = PAGES.verified_source(api, event)
                    self.assertEqual(selected, {"functional": 501, "accessibility": 502})

    def test_untrusted_or_cancelled_originals_are_rejected(self):
        changes = {
            "fork": lambda r: r["head_repository"].update(full_name="other/fork"),
            "repository": lambda r: r["repository"].update(full_name="other/repository"),
            "branch": lambda r: r.update(head_branch="feature/untrusted"),
            "pr": lambda r: r.update(event="pull_request"),
            "cancelled": lambda r: r.update(conclusion="cancelled"),
            "running": lambda r: r.update(status="in_progress"),
            "workflow": lambda r: r.update(workflow_id=11),
            "path": lambda r: r.update(path=".github/workflows/other.yml"),
            "bad-sha": lambda r: r.update(head_sha="invalid"),
            "bad-url": lambda r: r.update(html_url="https://example.invalid"),
            "missing-attempt": lambda r: r.update(run_attempt=None),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                api, event, _ = fixture()
                change(event["workflow_run"])
                with self.assertRaises((ValueError, KeyError, TypeError)):
                    PAGES.verified_source(api, event)

    def test_missing_mixed_expired_and_ambiguous_artifacts_are_rejected(self):
        for field, value in (("id", 999), ("head_sha", "b" * 40), ("repository_id", 100),
                             ("head_repository_id", 100), ("head_branch", "feature/other")):
            with self.subTest(field=field):
                api, event, _ = fixture()
                api.responses[f"{PAGES.PREFIX}/runs/123/artifacts"]["artifacts"][0]["workflow_run"][field] = value
                with self.assertRaises(ValueError):
                    PAGES.verified_source(api, event)
        for field, value in (("expired", True), ("size_in_bytes", 0), ("created_at", "2026-10-13T15:05:01Z"),
                             ("id", False)):
            with self.subTest(field=field):
                api, event, _ = fixture()
                api.responses[f"{PAGES.PREFIX}/runs/123/artifacts"]["artifacts"][0][field] = value
                with self.assertRaises(ValueError):
                    PAGES.verified_source(api, event)
        api, event, _ = fixture()
        data = api.responses[f"{PAGES.PREFIX}/runs/123/artifacts"]["artifacts"]
        data.append(deepcopy(data[0]))
        with self.assertRaises(ValueError):
            PAGES.verified_source(api, event)
        api, event, _ = fixture()
        api.responses[f"{PAGES.PREFIX}/runs/123/attempts/2/jobs"]["jobs"].pop()
        with self.assertRaises(ValueError):
            PAGES.verified_source(api, event)

    def test_attempt_is_pinned_even_if_newer_attempt_is_cancelled(self):
        api, event, run = fixture()
        api.responses[f"{PAGES.PREFIX}/runs/123"] = {**run, "run_attempt": 3, "conclusion": "cancelled"}
        current = deepcopy(api.responses[f"{PAGES.PREFIX}/runs/123/artifacts"]["artifacts"][0])
        current.update(id=503, created_at="2026-10-13T17:00:00Z")
        api.responses[f"{PAGES.PREFIX}/runs/123/artifacts"]["artifacts"].append(current)
        original, selected = PAGES.verified_source(api, event)
        self.assertEqual(original["run_attempt"], 2)
        self.assertEqual(selected["functional"], 501)
        self.assertNotIn(f"{PAGES.PREFIX}/runs/123", api.calls)

    def test_artifact_timestamp_precision_and_event_api_disagreement(self):
        api, event, _ = fixture()
        api.responses[f"{PAGES.PREFIX}/runs/123/attempts/2/jobs"]["jobs"][0]["steps"][0]["started_at"] = "2026-10-13T16:05:00.900Z"
        api.responses[f"{PAGES.PREFIX}/runs/123/artifacts"]["artifacts"][0]["created_at"] = "2026-10-13T16:05:00Z"
        PAGES.verified_source(api, event)
        api.responses[f"{PAGES.PREFIX}/runs/123/attempts/2"]["head_sha"] = "b" * 40
        with self.assertRaises(ValueError):
            PAGES.verified_source(api, event)


class OrderingContracts(unittest.TestCase):
    def test_newer_unpublished_attempts_do_not_block_valid_candidate(self):
        for conclusion in ("skipped", "cancelled", "failure", "timed_out"):
            with self.subTest(conclusion=conclusion):
                api, _, run = fixture()
                publisher(api, 43, deployed={1: conclusion})
                self.assertTrue(PAGES.can_publish(api, run, 9000))
        api, _, run = fixture()
        publisher(api, 43)
        api.responses[f"{PAGES.PREFIX}/runs/9001/attempts/1/jobs"] = {"jobs": [{
            "run_id": 9001, "name": "Prepare validated Allure report", "conclusion": "failure", "steps": []}]}
        self.assertTrue(PAGES.can_publish(api, run, 9000))

    def test_equal_and_newer_published_sources_block_duplicates_and_rollbacks(self):
        for number, attempt, expected in ((41, 99, True), (42, 1, True), (42, 2, False),
                                          (42, 3, False), (43, 1, False)):
            with self.subTest(number=number, attempt=attempt):
                api, _, run = fixture()
                publisher(api, number, attempt, deployed={1: "success"})
                self.assertEqual(PAGES.can_publish(api, run, 9000), expected)

    def test_publication_completion_order_and_older_created_runs_are_considered(self):
        api, _, run = fixture()
        publisher(api, 41, identity=9002, deployed={1: "success"})
        publisher(api, 43, identity=9001, deployed={1: "success"})
        self.assertFalse(PAGES.can_publish(api, run, 9000))

    def test_publisher_reruns_keep_earlier_success_and_skip_own_duplicate(self):
        api, _, run = fixture()
        publisher(api, 43, publisher_attempt=2, deployed={1: "success", 2: "failure"})
        self.assertFalse(PAGES.can_publish(api, run, 9000))
        api, _, run = fixture()
        publisher(api, 42, source_attempt=2, identity=9000, publisher_attempt=2,
                  deployed={1: "success", 2: "skipped"})
        self.assertFalse(PAGES.can_publish(api, run, 9000, publisher_attempt=2))

    def test_api_failures_and_unknown_successful_origin_fail_closed(self):
        api, _, run = fixture()
        record = publisher(api, 43, deployed={1: "success"})
        record["display_title"] = "unrecognized origin"
        with self.assertRaises(ValueError):
            PAGES.can_publish(api, run, 9000)
        api, _, run = fixture()
        with patch.object(api, "items", side_effect=OSError("simulated API outage")):
            with self.assertRaises(OSError):
                PAGES.can_publish(api, run, 9000)

    def test_foreign_publisher_and_pr_records_are_ignored(self):
        for change in ({"head_branch": "feature/other"}, {"event": "pull_request"},
                       {"head_repository": {"full_name": "other/repo"}}):
            api, _, run = fixture()
            publisher(api, 43, deployed={1: "success"}).update(change)
            self.assertTrue(PAGES.can_publish(api, run, 9000))


class TransportContracts(unittest.TestCase):
    def test_pagination_reads_beyond_first_page_without_search_filters(self):
        api = PAGES.GitHub("synthetic-only")
        first = {"workflow_runs": [{"id": index} for index in range(100)]}
        second = {"workflow_runs": [{"id": 100}]}
        with patch.object(api, "get", side_effect=[first, second]) as getter:
            result = list(api.items(f"{PAGES.PREFIX}/workflows/pages.yml/runs", "workflow_runs"))
        self.assertEqual(len(result), 101)
        self.assertEqual(getter.call_count, 2)
        for call in getter.call_args_list:
            self.assertNotIn("branch=", call.args[0])
            self.assertNotIn("status=", call.args[0])

    def test_credentials_are_never_redirected_or_sent_to_another_repository(self):
        api = PAGES.GitHub("synthetic-only")
        with self.assertRaises(ValueError):
            api.get("/repos/other/repository/actions/runs/1")
        self.assertIsNone(PAGES.NoRedirect().redirect_request(None, None, 302, "redirect", {},
                                                             "https://example.invalid"))


class MetadataAndCliContracts(unittest.TestCase):
    def setUp(self):
        area = ROOT / ".accessibility-verification" / "pages-local"
        area.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="contract-", dir=area)
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def test_only_safe_original_metadata_is_written_and_never_overwritten(self):
        _, _, run = fixture()
        run["private_actor_data"] = {"token": "synthetic-secret-must-not-be-published"}
        PAGES.write_environment(run, self.directory)
        PAGES.write_report_origin(run, self.directory)
        public = json.loads((self.directory / "ci-origin.json").read_text(encoding="utf-8"))
        self.assertEqual(public["run_number"], 42)
        self.assertEqual(public["run_attempt"], 2)
        self.assertEqual(public["branch"], "master")
        self.assertNotIn("private_actor_data", public)
        for path in self.directory.iterdir():
            self.assertNotIn("synthetic-secret", path.read_text(encoding="utf-8"))
        with self.assertRaises(FileExistsError):
            PAGES.write_report_origin(run, self.directory)
        self.assertIn("WCAG conformance is not established", (self.directory / "environment.properties").read_text())

    def test_publication_tree_rejects_hidden_files_and_links(self):
        _, _, run = fixture()
        hidden = self.directory / ".private"
        hidden.write_text("synthetic", encoding="utf-8")
        with self.assertRaises(ValueError):
            PAGES.write_report_origin(run, self.directory)
        hidden.unlink()
        ordinary = self.directory / "asset.js"
        ordinary.write_text("/* synthetic */", encoding="utf-8")
        with patch.object(Path, "is_symlink", autospec=True, side_effect=lambda p: p == ordinary):
            with self.assertRaises(ValueError):
                PAGES.write_report_origin(run, self.directory)

    def test_main_prepare_and_gate_using_mock_api_without_network(self):
        api, event, _ = fixture()
        event_path, source_path, output_path = [self.directory / name for name in ("event.json", "source.json", "outputs")]
        event_path.write_text(json.dumps(event), encoding="utf-8")
        env = {"GITHUB_REPOSITORY": PAGES.REPOSITORY, "GITHUB_REF": "refs/heads/master",
               "GITHUB_EVENT_NAME": "workflow_run", "GITHUB_EVENT_PATH": str(event_path),
               "GITHUB_RUN_ID": "9000", "GITHUB_RUN_ATTEMPT": "1", "GITHUB_OUTPUT": str(output_path),
               "GH_TOKEN": "synthetic-only", "CI_FUNCTIONAL_ARTIFACT": "501", "CI_ACCESSIBILITY_ARTIFACT": "502"}
        with patch.dict(os.environ, env), patch.object(PAGES, "GitHub", return_value=api):
            with patch.object(PAGES.sys, "argv", ["pages", "prepare", "--source", str(source_path)]):
                self.assertEqual(PAGES.main(), 0)
            self.assertIn("publish=true", output_path.read_text())
            with patch.object(PAGES.sys, "argv", ["pages", "gate"]):
                self.assertEqual(PAGES.main(), 0)
            with patch.dict(os.environ, {"CI_FUNCTIONAL_ARTIFACT": "999"}):
                with patch.object(PAGES.sys, "argv", ["pages", "gate"]):
                    self.assertEqual(PAGES.main(), 1)
            with patch.dict(os.environ, {"GITHUB_REF": "refs/heads/feature/other"}):
                with patch.object(PAGES.sys, "argv", ["pages", "gate"]):
                    self.assertEqual(PAGES.main(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
