"""Combine validated Allure evidence without rewriting or overwriting its files.

Generation stays a separate `mvn allure:report` step using the existing POM.
"""

import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit


VALIDATOR_PATH = Path(__file__).with_name("validate-ci-evidence.py")
SPEC = importlib.util.spec_from_file_location("ci_evidence", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
require = VALIDATOR.require
unique = VALIDATOR.unique
load_json = VALIDATOR.load_json
attachments = VALIDATOR.attachments
REPORT_METADATA = {"executor.json", "allure.properties"}


def inventory(directory):
    """Only result/container documents and their referenced attachments may be copied."""
    require(directory.is_dir() and not directory.is_symlink() and not directory.is_junction(),
            f"Invalid results directory: {directory}")
    entries = sorted(directory.iterdir())
    require(all(path.is_file() and not path.is_symlink() and not path.is_junction() for path in entries),
            "Results must contain only regular files")
    # Maven writes per-report metadata back into results. It is not suite evidence.
    # Do not choose one job's executor; Maven regenerates it for the consolidated report.
    files = [path for path in entries if path.name not in REPORT_METADATA]
    documents = [(path, load_json(path)) for path in files
                 if path.name.endswith(("-result.json", "-container.json"))]
    results = [document for path, document in documents if path.name.endswith("-result.json")]
    references = [item["source"] for _, document in documents for item in attachments(document)]
    permitted = {path.name for path, _ in documents} | set(references)
    require({path.name for path in files} == permitted,
            "Missing, orphaned or unsupported Allure input files")
    return {"files": files, "documents": documents, "results": results, "references": references}


def check_collisions(inputs):
    documents = [document for item in inputs for _, document in item["documents"]]
    results = [result for item in inputs for result in item["results"]]
    unique([document.get("uuid") for document in documents], "combined result/container UUIDs")
    unique([result.get("fullName") for result in results], "combined test identities")
    # Allure can group different results as retries when these identities collide.
    for key in ("historyId", "testCaseId"):
        unique([result[key] for result in results if key in result], f"combined {key} identities")
    unique([source.casefold() for item in inputs for source in item["references"]],
           "combined attachment references")
    unique([path.name.casefold() for item in inputs for path in item["files"]],
           "combined filenames (case-insensitive)")
    require(len(results) == sum(VALIDATOR.COUNTS.values()), "Expected 21 combined test results")


def consolidate(functional, accessibility, output):
    require(not os.path.lexists(output), "Output already exists; choose a fresh results directory")
    destination = output.absolute()
    require(not any(path.is_symlink() or path.is_junction() for path in destination.parents),
            "Output parent must not contain links")
    for target in (functional, accessibility):
        source = target.resolve()
        require(destination.resolve() != source and source not in destination.resolve().parents,
                "Output must be outside both input artifacts")
    for suite, target in (("functional", functional), ("accessibility", accessibility)):
        result = subprocess.run([sys.executable, "-B", str(VALIDATOR_PATH), suite,
                                 "--publication", "--target", str(target)], check=False)
        require(result.returncode == 0, f"{suite} publication validation failed")
    inputs = [inventory(target / "allure-results") for target in (functional, accessibility)]
    for target in (functional, accessibility):
        metadata = sorted(path.name for path in (target / "allure-results").iterdir()
                          if path.name in REPORT_METADATA)
        if metadata:
            print(f"Per-report metadata excluded explicitly from {target}: {', '.join(metadata)}")
    check_collisions(inputs)
    # Read all bytes before creating output. Preflight failures leave no partial merge.
    content = [(path.name, path.read_bytes()) for item in inputs for path in item["files"]]
    output.mkdir(parents=True, exist_ok=False)
    for name, data in content:
        with (output / name).open("xb") as stream:
            stream.write(data)
    for name, data in content:
        require((output / name).read_bytes() == data, f"Copied bytes differ: {name}")
    merged = inventory(output)
    check_collisions([merged])
    counts = Counter(result["status"] for result in merged["results"])
    print(f"Consolidation PASS: 21 tests, {dict(counts)}, "
          f"{len(merged['references'])} attachments, {len(content)} unchanged files")


class PageAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("src", "href") and value:
                url = urlsplit(value)
                if not url.scheme and not url.netloc and url.path:
                    self.paths.append(unquote(url.path))


def report_file(report, relative):
    path = report / relative
    require(path.resolve().is_relative_to(report.resolve()) and path.is_file() and
            not path.is_symlink() and not path.is_junction() and path.stat().st_size > 0,
            f"Missing or unsafe report file: {relative}")
    require(not any(parent.is_symlink() or parent.is_junction()
                    for parent in path.parents if parent.is_relative_to(report)),
            f"Linked report directory: {relative}")
    return path


def report_links(node):
    """Allure 3 repeats attachment links in its summary and step tree."""
    if isinstance(node, dict):
        if node.get("type") == "attachment":
            require(isinstance(node.get("link"), dict), "Invalid report attachment link")
            yield node["link"]
        else:
            for value in node.values():
                yield from report_links(value)
    elif isinstance(node, list):
        for value in node:
            yield from report_links(value)


def verify_report(results, report):
    """Verify the multi-file output produced by the pinned Allure 3.20.0 report."""
    source = inventory(results)
    check_collisions([source])
    require(report.is_dir() and not report.is_symlink() and not report.is_junction(),
            "Invalid report directory")
    index = report_file(report, "index.html")
    page = PageAssets()
    page.feed(index.read_text(encoding="utf-8"))
    require(page.paths, "Report has no application assets")
    for relative in page.paths:
        report_file(report, relative)
    expected = {result["fullName"]: result for result in source["results"]}
    generated = [load_json(report_file(report, str(path.relative_to(report))))
                 for path in sorted((report / "data" / "test-results").glob("*.json"))]
    require(len(generated) == 21, "Expected 21 rendered test results")
    unique([item.get("fullName") for item in generated], "rendered test identities")
    require({item["fullName"] for item in generated} == set(expected), "Rendered tests differ from inputs")
    rendered_sources = set()
    for item in generated:
        original = expected[item["fullName"]]
        require(item.get("status") == original["status"] and item.get("name") == original.get("name"),
                f"Rendered test name/status differs: {item['fullName']}")
        require(item.get("isRetry") is False and not item.get("retries"),
                "Unexpected report retry grouping")
        owned = {attachment["source"] for attachment in attachments(original)}
        for _, document in source["documents"]:
            if original["uuid"] in document.get("children", []):
                owned.update(attachment["source"] for attachment in attachments(document))
        seen = set()
        for link in report_links(item):
            filename = link.get("originalFileName")
            require(filename in owned and link.get("used") is True and link.get("missed") is False,
                    "Missing or wrongly owned rendered attachment")
            attachment_name = f"{link.get('id', '')}{link.get('ext', '')}"
            require(attachment_name and not any(c in attachment_name for c in "/\\:"),
                    "Unsafe rendered attachment filename")
            attached = report_file(report, f"data/attachments/{attachment_name}")
            require(hashlib.sha256(attached.read_bytes()).digest() ==
                    hashlib.sha256((results / filename).read_bytes()).digest(),
                    f"Rendered attachment bytes differ: {filename}")
            seen.add(filename)
        require(seen == owned, f"Rendered attachments missing: {item['fullName']}")
        rendered_sources.update(seen)
    require(rendered_sources == set(source["references"]), "Not all original attachments are rendered")
    stats = load_json(report_file(report, "widgets/statistic.json"))
    counts = Counter(item["status"] for item in generated)
    require(stats.get("total") == 21 and all(stats.get(status, 0) == counts[status]
            for status in ("passed", "failed", "broken", "skipped", "unknown")),
            "Report summary counts differ from test results")
    print(f"Report verification PASS: 21 tests, {dict(counts)}, "
          f"{len(rendered_sources)} attachments with original bytes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    merge = commands.add_parser("merge", help="Validate both suites and copy to a new results directory")
    merge.add_argument("--functional", type=Path, required=True, help="Functional artifact root")
    merge.add_argument("--accessibility", type=Path, required=True, help="Accessibility artifact root")
    merge.add_argument("--output", type=Path, required=True, help="New allure-results directory")
    verify = commands.add_parser("verify-report", help="Check generated Allure 3 HTML, states and attachment bytes")
    verify.add_argument("--results", type=Path, required=True, help="Consolidated allure-results directory")
    verify.add_argument("--report", type=Path, required=True, help="Generated allure-report directory")
    args = parser.parse_args()
    try:
        if args.command == "merge":
            consolidate(args.functional, args.accessibility, args.output)
        else:
            verify_report(args.results, args.report)
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        label = "Consolidation" if args.command == "merge" else "Report verification"
        print(f"{label} FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
