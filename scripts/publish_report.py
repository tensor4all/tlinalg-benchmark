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
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def page_path(manifest):
    """One page per measured (suite, profile, commit, version).

    The page is named after the revision rather than the cell so that measuring
    a new commit adds a page instead of replacing the previous one: the tree
    keeps the history the index links to, and a reader can always see what a
    number was measured at. A dirty checkout gets its own suffix, because its
    numbers are not comparable with a clean build of the same commit.
    """
    library = manifest["library"]
    suffix = "-dirty" if library["dirty"] else ""
    version = f"-{library['version']}" if library.get("version") else ""
    return (ROOT / "result" / manifest["target_profile"] / manifest["suite_id"]
            / f"{library['commit'][:12]}{version}{suffix}.md")


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
    else:
        print(f"kept the existing {report.relative_to(ROOT)}: this run is partial and a "
              f"full-coverage page for the same revision already exists")
    subprocess.run([sys.executable, str(ROOT / "scripts/gen_index.py"), "--write"], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    args = ap.parse_args()
    publish(pathlib.Path(args.run_dir).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
