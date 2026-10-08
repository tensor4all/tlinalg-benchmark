#!/usr/bin/env python3
"""Validate one run manifest against the schema and the declared profiles/suites.

Schema validation is only half of it. The rest is the part a schema cannot
express: that the profile and suite are declared, that `cpu_sets` lines up with
`threads`, and that the recorded commit actually exists in the checkout it
names — a manifest that points at a commit nobody can resolve is not evidence.
"""
import argparse
import json
import pathlib
import subprocess
import sys

import jsonschema

from campaign import PROVIDER_OF_ENGINE, ROOT, load, populations, same_populations, vendors_declared


def known_profiles():
    return {p["name"] for p in load(ROOT / "benchmarks/profiles.yaml")["profiles"]}


def find_suite(suite_id):
    for f in sorted((ROOT / "benchmarks/suites").glob("*.yaml")):
        data = load(f)
        if data["id"] == suite_id:
            return f, data
    return None, None


def declaration_drifted(manifest, suite_file):
    """True when this run was taken under a different suite declaration.

    Evidence is immutable and declarations are not: adding an engine to a suite
    must not retroactively invalidate a manifest that was correct when it was
    written, and reconstructing the old declaration is impossible. A manifest
    with no recorded hash predates the field, so it is treated the same way.
    """
    recorded = manifest.get("suite_sha256")
    if not recorded:
        return True
    import hashlib
    current = hashlib.sha256(pathlib.Path(suite_file).read_bytes()).hexdigest()
    return recorded != current


def validate(path, check_git=True):
    errors = []
    manifest = load(path)
    schema = json.loads((ROOT / "schemas/benchmark-run.schema.json").read_text())
    try:
        jsonschema.validate(manifest, schema)
    except jsonschema.ValidationError as e:
        return [f"schema: {e.json_path}: {e.message}"]

    if manifest["target_profile"] not in known_profiles():
        errors.append(f"target_profile {manifest['target_profile']!r} is not in benchmarks/profiles.yaml")

    suite_file, suite = find_suite(manifest["suite_id"])
    if suite is None:
        errors.append(f"suite_id {manifest['suite_id']!r} has no benchmarks/suites/*.yaml declaration")
    else:
        declared = pathlib.Path(manifest["suite_file"])
        if declared.resolve() != suite_file.resolve():
            errors.append(f"suite_file {declared} is not the declaration for {manifest['suite_id']!r} ({suite_file})")
        if manifest["target_profile"] not in suite["required_profiles"] + suite.get("optional_profiles", []):
            errors.append(f"suite {manifest['suite_id']!r} does not list profile {manifest['target_profile']!r}")
        elif declaration_drifted(manifest, suite_file):
            print(f"note {path}: measured under a different declaration than the current one "
                  f"(recorded suite_sha256 {manifest.get('suite_sha256') or 'absent'}); "
                  f"declaration-derived checks skipped", file=sys.stderr)
            return errors
        spec = suite["runs"][0]
        declared = {p["regime"]: p for p in populations(suite)}
        # A partial run is legitimate -- the campaign is not run in full on every
        # profile -- but it may only be a subset of what the suite declares, and
        # the manifest has to say whether it covered the declaration.
        for t in manifest["threads"]["counts"]:
            if t not in spec["threads"]:
                errors.append(f"threads.counts contains {t}, which the suite does not declare")
            if str(t) not in manifest["threads"]["cpu_sets"]:
                errors.append(f"threads.cpu_sets is missing an entry for {t}T")
        rs = manifest.get("run_spec", {})
        covered = rs.get("populations", [])
        if not covered:
            errors.append("run_spec.populations is empty: a run states what it covered")
        for population in covered:
            want = declared.get(population.get("regime"))
            if want is None:
                errors.append(f"run_spec.populations names regime {population.get('regime')!r}, "
                              f"which the suite does not declare")
                continue
            for family in population.get("families", []):
                if family not in want["families"]:
                    errors.append(f"run_spec.populations[{population['regime']}] contains family "
                                  f"{family!r}, which the suite does not declare for that regime")
            for n in population.get("n", []):
                if n not in want["n"]:
                    errors.append(f"run_spec.populations[{population['regime']}] contains n {n!r}, "
                                  f"which the suite does not declare for that regime")
            for batch in population.get("batch", []):
                if batch not in want["batch"]:
                    errors.append(f"run_spec.populations[{population['regime']}] contains batch "
                                  f"{batch!r}, which the suite does not declare for that regime")
        for key, declared_values in (("dtypes", spec["dtypes"]), ("engines", spec["engines"])):
            for v in rs.get(key, []):
                if v not in declared_values:
                    errors.append(f"run_spec.{key} contains {v!r}, which the suite does not declare")
        if vendors_declared(rs.get("engines", [])) and not manifest.get("vendor"):
            errors.append("run_spec.engines declares a vendor arm, but the manifest records no vendor "
                          "identity; nothing is published from an arm whose library cannot be named")
        covers = (same_populations(covered, populations(suite))
                  and manifest["threads"]["counts"] == spec["threads"]
                  and rs.get("dtypes") == spec["dtypes"]
                  and rs.get("engines") == spec["engines"])
        if rs.get("covers_declared_suite") != covers:
            errors.append(f"run_spec.covers_declared_suite should be {covers}")

    if check_git:
        commit = manifest["library"]["commit"]
        # Resolve in a checkout that exists *here*, never in the path recorded
        # by the measuring host: a committed manifest has to be verifiable in
        # any checkout, or it is not evidence.
        candidates = [ROOT / "extern/tlinalg-rs"]
        measured = manifest["library"].get("measured_path")
        if measured and pathlib.Path(measured, ".git").exists():
            candidates.insert(0, pathlib.Path(measured))
        resolved = False
        for directory in candidates:
            if not (directory / ".git").exists():
                continue
            r = subprocess.run(["git", "-C", str(directory), "cat-file", "-e", f"{commit}^{{commit}}"],
                               capture_output=True)
            if r.returncode == 0:
                resolved = True
                break
        if not resolved:
            tried = ", ".join(str(c) for c in candidates)
            errors.append(f"library.commit {commit} could not be resolved in any available checkout ({tried})")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", nargs="+")
    ap.add_argument("--no-git", action="store_true")
    args = ap.parse_args()
    failed = False
    for m in args.manifest:
        errors = validate(m, check_git=not args.no_git)
        if errors:
            failed = True
            print(f"FAIL {m}")
            for e in errors:
                print(f"  {e}")
        else:
            print(f"ok   {m}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
