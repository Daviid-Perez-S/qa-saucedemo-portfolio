"""Read-only GitHub provenance checks, publication ordering and safe CI metadata.

No deployments or repository mutations are performed by this script.
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


REPOSITORY = "Daviid-Perez-S/qa-saucedemo-portfolio"
PREFIX = f"/repos/{REPOSITORY}/actions"
CI_PATH = ".github/workflows/ci.yml"
PAGES_PATH = ".github/workflows/pages.yml"
PAGES_NAME = "Allure Pages"
DEPLOY_JOB = "Deploy Allure to GitHub Pages"
DEPLOY_STEP = "Deploy GitHub Pages"
TITLE = re.compile(r"Allure Pages - CI #(\d+) attempt (\d+) source (\d+)\Z")
SUITES = {
    "functional": ("Check Java, Maven and Chrome", "Upload functional evidence"),
    "accessibility": ("Accessibility tests", "Upload accessibility evidence"),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def positive(value):
    require(type(value) is int and value > 0, "Invalid numeric GitHub identity")
    return value


def instant(value):
    parsed = datetime.fromisoformat(value)
    require(parsed.utcoffset() is not None, "Timestamp lacks timezone")
    return parsed.astimezone(timezone.utc)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


class GitHub:
    def __init__(self, token):
        require(token, "Missing GH_TOKEN")
        self.token = token
        self.opener = build_opener(NoRedirect())

    def get(self, path):
        require(path.startswith(PREFIX + "/"), "API request outside authorized repository")
        request = Request("https://api.github.com" + path, headers={
            "Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "saucedemo-allure-pages",
        })
        with self.opener.open(request, timeout=30) as response:
            return json.load(response)

    def items(self, path, key):
        page = 1
        while True:
            separator = "&" if "?" in path else "?"
            response = self.get(f"{path}{separator}per_page=100&page={page}")
            values = response[key]
            require(isinstance(values, list), "Invalid paginated GitHub response")
            yield from values
            if len(values) < 100:
                return
            page += 1


def check_run(run, workflow_id, expected=None):
    require(run.get("repository", {}).get("full_name") == REPOSITORY and
            run.get("head_repository", {}).get("full_name") == REPOSITORY,
            "CI run belongs to an unauthorized repository")
    require(run.get("head_branch") == "master" and run.get("event") in ("push", "workflow_dispatch"),
            "CI run must be push/workflow_dispatch on master")
    require(run.get("name") == "SauceDemo CI" and run.get("workflow_id") == workflow_id and
            run.get("path", "").split("@", 1)[0] == CI_PATH, "Unexpected CI workflow")
    require(run.get("status") == "completed" and run.get("conclusion") in ("success", "failure"),
            "CI attempt is not a completed, non-cancelled execution")
    for key in ("id", "run_number", "run_attempt"):
        positive(run.get(key))
    require(isinstance(run.get("head_sha"), str) and re.fullmatch(r"[0-9a-f]{40}", run["head_sha"]),
            "Invalid original commit SHA")
    require(run.get("html_url") == f"https://github.com/{REPOSITORY}/actions/runs/{run['id']}",
            "Unexpected original run URL")
    instant(run["run_started_at"])
    if expected:
        require(all(run.get(key) == expected.get(key) for key in
                    ("id", "run_number", "run_attempt", "head_sha", "workflow_id")),
                "Original event and CI attempt disagree")


def verified_source(api, event):
    require(event.get("repository", {}).get("full_name") == REPOSITORY,
            "Unauthorized workflow_run event repository")
    original = event["workflow_run"]
    workflow = api.get(f"{PREFIX}/workflows/ci.yml")
    require(workflow.get("name") == "SauceDemo CI" and workflow.get("path") == CI_PATH,
            "Unexpected authorized CI workflow")
    check_run(original, workflow["id"])
    # Read the specific attempt: a later cancelled rerun must not invalidate an older valid attempt.
    run = api.get(f"{PREFIX}/runs/{original['id']}/attempts/{original['run_attempt']}")
    check_run(run, workflow["id"], original)
    repository_id = positive(event["repository"].get("id"))
    require(run["repository"].get("id") == repository_id and
            run["head_repository"].get("id") == repository_id, "Repository IDs differ")
    jobs = list(api.items(f"{PREFIX}/runs/{run['id']}/attempts/{run['run_attempt']}/jobs", "jobs"))
    artifacts = list(api.items(f"{PREFIX}/runs/{run['id']}/artifacts", "artifacts"))
    selected = {}
    for suite, (job_name, upload_name) in SUITES.items():
        matching_jobs = [job for job in jobs if job.get("name") == job_name]
        require(len(matching_jobs) == 1, f"Missing or ambiguous {suite} job for original attempt")
        job = matching_jobs[0]
        require(job.get("run_id") == run["id"] and job.get("head_sha") == run["head_sha"] and
                job.get("status") == "completed", f"Invalid {suite} job provenance")
        uploads = [step for step in job.get("steps", []) if step.get("name") == upload_name]
        require(len(uploads) == 1 and uploads[0].get("conclusion") == "success" and
                uploads[0].get("status") == "completed", f"{suite} artifact upload did not finish")
        start = instant(uploads[0]["started_at"]).replace(microsecond=0)
        finish = instant(uploads[0]["completed_at"])
        require(finish >= start, "Invalid upload step timestamps")
        matches = [item for item in artifacts if item.get("name") == f"{suite}-evidence" and
                   start <= instant(item["created_at"]) <= finish]
        require(len(matches) == 1, f"Missing or ambiguous {suite} artifact for original attempt")
        artifact = matches[0]
        provenance = artifact.get("workflow_run", {})
        require(provenance.get("id") == run["id"] and provenance.get("head_branch") == "master" and
                provenance.get("head_sha") == run["head_sha"] and
                provenance.get("repository_id") == repository_id and
                provenance.get("head_repository_id") == repository_id,
                f"Invalid {suite} artifact provenance")
        require(artifact.get("expired") is False and artifact.get("size_in_bytes", 0) > 0,
                f"{suite} artifact is expired or empty")
        selected[suite] = positive(artifact.get("id"))
    require(len(set(selected.values())) == 2, "Suite artifact IDs collide")
    return run, selected


def can_publish(api, source, current_publisher, publisher_attempt=1):
    """Only confirmed Pages deployments advance the watermark; failed preparations do not."""
    candidate = (source["run_number"], source["run_attempt"])
    workflow = api.get(f"{PREFIX}/workflows/pages.yml")
    require(workflow.get("name") == PAGES_NAME and workflow.get("path") == PAGES_PATH,
            "Unexpected Pages workflow")
    # No search filters: GitHub caps filtered workflow-run searches at 1,000 results.
    for publisher in api.items(f"{PREFIX}/workflows/pages.yml/runs", "workflow_runs"):
        if (publisher.get("workflow_id") != workflow["id"] or publisher.get("head_branch") != "master" or
                publisher.get("event") != "workflow_run" or
                publisher.get("head_repository", {}).get("full_name") != REPOSITORY):
            continue
        title = TITLE.fullmatch(publisher.get("display_title", ""))
        if title and (int(title[1]), int(title[2])) < candidate:
            continue
        # Earlier successful publisher attempts remain relevant even if a later retry failed.
        latest_attempt = positive(publisher.get("run_attempt"))
        if publisher["id"] == current_publisher:
            latest_attempt = publisher_attempt - 1
        for attempt in range(latest_attempt, 0, -1):
            jobs = api.items(f"{PREFIX}/runs/{publisher['id']}/attempts/{attempt}/jobs", "jobs")
            for job in jobs:
                if job.get("name") != DEPLOY_JOB:
                    continue
                require(job.get("run_id") == publisher["id"], "Deployment job belongs to another run")
                deployed = any(step.get("name") == DEPLOY_STEP and step.get("status") == "completed" and
                               step.get("conclusion") == "success"
                               for step in job.get("steps", []))
                if deployed:
                    require(title is not None, "Published origin is unknown; review publication history")
                    published = (int(title[1]), int(title[2]))
                    require(int(title[3]) != source["id"] or int(title[1]) == source["run_number"],
                            "Conflicting published source identity")
                    if published >= candidate:
                        print("Publication omitted: an equal or newer CI attempt is already published")
                        return False
    return True


def public_origin(run):
    return {"repository": REPOSITORY, "run_id": run["id"], "run_number": run["run_number"],
            "run_attempt": run["run_attempt"], "started_at": instant(run["run_started_at"]).isoformat(),
            "commit": run["head_sha"], "branch": "master", "event": run["event"], "run_url": run["html_url"]}


def write_environment(run, results):
    origin = public_origin(run)
    rows = [f"CI.{key}={value}" for key, value in origin.items()]
    rows.append("Accessibility.review=incomplete findings require human review; WCAG conformance is not established")
    with (results / "environment.properties").open("x", encoding="utf-8") as stream:
        stream.write("\n".join(rows) + "\n")


def write_report_origin(run, report):
    require(report.is_dir() and not report.is_symlink() and not report.is_junction(),
            "Invalid public report directory")
    for path in report.rglob("*"):
        require(not path.is_symlink() and not path.is_junction() and
                (path.is_dir() or path.is_file()), "Public report contains a link or non-regular file")
        require(not path.name.startswith("."), "Public report contains hidden files")
    with (report / "ci-origin.json").open("x", encoding="utf-8") as stream:
        json.dump(public_origin(run), stream, indent=2)


def output(values):
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
        for key, value in values.items():
            text = str(value)
            require("\n" not in text and "\r" not in text, "Unsafe workflow output")
            stream.write(f"{key}={text}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "gate", "environment", "report-origin"))
    parser.add_argument("--source", type=Path, default=Path("target/pages-source.json"),
                        help="Trusted local source metadata file (not used by gate)")
    parser.add_argument("--results", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        require(os.environ.get("GITHUB_REPOSITORY") == REPOSITORY and
                os.environ.get("GITHUB_REF") == "refs/heads/master" and
                os.environ.get("GITHUB_EVENT_NAME") == "workflow_run",
                "Publisher must run as workflow_run on authorized master")
        with Path(os.environ["GITHUB_EVENT_PATH"]).open(encoding="utf-8") as stream:
            event = json.load(stream)
        if args.command in ("prepare", "gate"):
            api = GitHub(os.environ.get("GH_TOKEN"))
            run, artifacts = verified_source(api, event)
            publish = can_publish(api, run, positive(int(os.environ["GITHUB_RUN_ID"])),
                                  positive(int(os.environ.get("GITHUB_RUN_ATTEMPT", "1"))))
            if args.command == "prepare":
                args.source.parent.mkdir(parents=True, exist_ok=True)
                with args.source.open("x", encoding="utf-8") as stream:
                    json.dump({"run": run, "artifacts": artifacts}, stream)
                output({"publish": str(publish).lower(), "run_id": run["id"], "run_number": run["run_number"],
                        "run_attempt": run["run_attempt"], "commit": run["head_sha"],
                        **{f"{suite}_artifact": identity for suite, identity in artifacts.items()}})
            else:
                require(str(artifacts["functional"]) == os.environ["CI_FUNCTIONAL_ARTIFACT"] and
                        str(artifacts["accessibility"]) == os.environ["CI_ACCESSIBILITY_ARTIFACT"],
                        "Original artifacts changed after preparation")
                output({"publish": str(publish).lower()})
        else:
            with args.source.open(encoding="utf-8") as stream:
                saved = json.load(stream)
            run = saved["run"]
            check_run(run, event["workflow_run"]["workflow_id"], event["workflow_run"])
            if args.command == "environment":
                require(args.results is not None, "Missing --results")
                write_environment(run, args.results)
            else:
                require(args.report is not None, "Missing --report")
                write_report_origin(run, args.report)
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, URLError) as error:
        # Do not print headers, token values, or error response bodies.
        message = f"GitHub API HTTP {error.code}" if isinstance(error, HTTPError) else str(error)
        print(f"Pages preparation FAIL: {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
