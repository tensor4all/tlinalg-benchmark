#!/usr/bin/env python3
"""Publish one recorded run as the cell's report, then regenerate the index.

This is the only place the publish rule lives, so `record_run.py` and a manual
re-publish after a report-format change cannot disagree:

* a run that did not cover the suite's declared spec never displaces the
  published report;
* the published file is a copy of the run's own report, so the report and the
  raw data it came from cannot drift apart.
"""
import argparse
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def page_source(page):
    """The run directory a page was generated from, read out of the page itself.

    The page's first line names the report it was copied from, so the index can tell which run
    a page actually holds instead of guessing from the newest manifest that would have written
    it. Publishing refuses a partial run over a full-coverage page, so those two are not the same
    question and must not be conflated.
    """
    with open(page) as handle:
        first = handle.readline()
    found = re.match(r"<!-- generated from (\S+)/report\.md by ", first)
    return ROOT / found.group(1) if found else None


def page_path(manifest):
    """One page per measured (suite, profile, commit, version, vendor arm).

    The page is named after the revision rather than the cell so that measuring
    a new commit adds a page instead of replacing the previous one: the tree
    keeps the history the index links to, and a reader can always see what a
    number was measured at. A dirty checkout gets its own suffix, because its
    numbers are not comparable with a clean build of the same commit.

    The vendor is part of the name because it is part of the measurement: one
    binary links one vendor library, so one run carries one arm, and two arms at
    the same revision are two pages that a reader compares side by side.
    """
    library = manifest["library"]
    suffix = "-dirty" if library["dirty"] else ""
    version = f"-{library['version']}" if library.get("version") else ""
    vendor = (manifest.get("vendor") or {}).get("name")
    arm = f"-{vendor}" if vendor else ""
    return (ROOT / "result" / manifest["target_profile"] / manifest["suite_id"]
            / f"{library['commit'][:12]}{version}{arm}{suffix}.md")


def publish(run_dir):
    manifest = yaml.safe_load((run_dir / "run.yaml").read_text())
    report = page_path(manifest)
    report.parent.mkdir(parents=True, exist_ok=True)
    covers = manifest["run_spec"]["covers_declared_suite"]
    header = (f"<!-- generated from {run_dir.relative_to(ROOT)}/report.md "
              f"by scripts/publish_report.py; the report below is the source of truth -->\n\n")
    if covers or not report.exists():
        report.write_text(header + (run_dir / "report.md").read_text())
        print(f"published {report.relative_to(ROOT)} from {run_dir.relative_to(ROOT)} "
              f"(coverage={'full' if covers else 'partial'})")
    elif published_full(report):
        print(f"kept the existing {report.relative_to(ROOT)}: this run is partial and the page "
              f"already there covers the whole declaration")
    else:
        report.write_text(header + (run_dir / "report.md").read_text())
        print(f"replaced the partial {report.relative_to(ROOT)} with this run "
              f"(coverage=partial): the page it held did not cover the whole declaration")
    subprocess.run([sys.executable, str(ROOT / "scripts/gen_index.py"), "--write"], check=True)


def published_full(report):
    """Whether the page already published for this revision covers the whole declaration."""
    source = page_source(report)
    manifest = source / "run.yaml" if source else None
    if manifest is None or not manifest.exists():
        return False
    return bool(yaml.safe_load(manifest.read_text())["run_spec"].get("covers_declared_suite"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    args = ap.parse_args()
    publish(pathlib.Path(args.run_dir).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
