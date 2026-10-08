#!/usr/bin/env python3
"""Record one (profile, suite) run: build at a revision, verify, measure, publish.

Order matters and is enforced here:

1. one campaign-level admission lock is taken first and held across build,
   verify and timing. The campaign is one measurement at a time and no build
   while a measurement runs; a lock inside a per-revision target directory
   would let a second recorder build another revision during this one;
2. the harness is built out of the *measured checkout*, into a target directory
   keyed by its revision;
3. `tlbench verify` runs over every population and thread budget before any
   timing, and a mismatch aborts the run (nothing is published from an
   unverified run);
4. each measurement goes through the pinned, idle-checked protocol script that
   belongs to the same revision;
5. the manifest is validated against its schema *before* it is written, and the
   recorded commit must resolve in the checkout it names.
"""
import argparse
import datetime
import fcntl
import hashlib
import os
import pathlib
import platform
import subprocess
import sys

import yaml

from campaign import PROVIDER_OF_ENGINE, ROOT, populations, same_populations, vendors_declared


def sh(cmd, **kw):
    print(f"+ {' '.join(str(c) for c in cmd)}", file=sys.stderr)
    return subprocess.run([str(c) for c in cmd], check=True, text=True,
                          capture_output=True, **kw)


def git(dir_, *args):
    return subprocess.run(["git", "-C", str(dir_), *args], check=True,
                          text=True, capture_output=True).stdout.strip()


def build(checkout):
    env_file = ROOT / "target/pin.env"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    sh([ROOT / "scripts/build_for_tlinalg_rev.sh", checkout, env_file, "tlbench"])
    pin = {}
    for line in env_file.read_text().splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            pin[k] = v.strip().strip("'\"")
    return pin


def host_info(profile_name, profiles):
    profile = next(p for p in profiles if p["name"] == profile_name)
    lscpu = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
    logical = next((int(l.split(":")[1].strip()) for l in lscpu.splitlines()
                    if l.startswith("CPU(s):")), 0)
    l3 = next((l.split(":", 1)[1].strip() for l in lscpu.splitlines()
               if l.startswith("L3 cache:")), None)
    return {
        "hostname": platform.node(),
        "cpu": profile["cpu"],
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "logical_cpus": logical or profile["logical_cpus"],
        "l3": l3 or profile.get("l3"),
        "l3_domains": profile.get("l3"),
        "notes": profile.get("description"),
    }


# What provides each engine name the harness emits lives in campaign.py, shared
# with the validator so the two cannot disagree.


def vendor_identity(binary, env):
    """`tlbench info` -> the vendor's own account of what was linked.

    Read from the binary that will be measured, executed directly the way the
    recorder executes it, so a loader or link problem shows up here rather than
    halfway through a timing pass.
    """
    out = subprocess.run([str(binary), "info"], capture_output=True, text=True, env=env)
    if out.returncode != 0:
        sys.exit(f"ERROR: {binary} info failed: {out.stderr.strip()}")
    fields = {}
    for line in out.stdout.splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            fields[k.strip()] = v.strip()
    return fields


def providers_for(engines, vendor):
    out = []
    names = {PROVIDER_OF_ENGINE.get(e) for e in engines}
    if "tlinalg" in names:
        out.append({"name": "tlinalg", "version": None, "commit": None, "path": None,
                    "note": "the faer-backed provider in the measured revision; see library above"})
    if "openblas" in names:
        config = vendor.get("vendor.config") or ""
        note = f"linked {vendor.get('vendor.linkage', '?')}"
        if vendor.get("vendor.corename"):
            note += f", kernel dispatched to {vendor['vendor.corename']}"
        if config:
            note += f", config {config}"
        out.append({"name": "openblas", "version": vendor.get("vendor.version") or None,
                    "commit": None, "path": None, "note": note})
    return out


def vendor_block(vendor, build_env):
    """The structured vendor identity, or None when no vendor arm was declared."""
    if not vendor.get("vendor.name") or vendor["vendor.name"] == "none":
        return None
    return {
        "name": vendor["vendor.name"],
        "linkage": vendor.get("vendor.linkage") or "none",
        "version": vendor.get("vendor.version") or None,
        "config": vendor.get("vendor.config") or None,
        "corename": vendor.get("vendor.corename") or None,
        "parallel": vendor.get("vendor.parallel") or None,
        "procs": int(vendor["vendor.procs"]) if vendor.get("vendor.procs") else None,
        "build_env": build_env or None,
    }


def skipped_of(csv_paths):
    """`family/MxN` pairs the harness reported as not applicable, per population.

    Recorded rather than inferred: a family the provider rejects is coverage the
    run did not have, and a page that claimed the whole grid would be wrong.
    """
    seen = {}
    for path in csv_paths:
        with open(path) as handle:
            for row in csv.DictReader(handle):
                if row.get("status") != "skipped":
                    continue
                key = row["regime"]
                shape = row["n"] if row["m"] == row["n"] else f"{row['m']}x{row['n']}"
                seen.setdefault(key, set()).add(f"{row['family']}/{shape}")
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profile")
    ap.add_argument("suite_id")
    ap.add_argument("--checkout", default=str(ROOT / "extern/tlinalg-rs"))
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--aa", type=int, default=1, help="number of complete set repeats (>=2 gives A/A)")
    ap.add_argument("--prime-ms", type=int, default=500)
    ap.add_argument("--regimes", default=None, help="override, comma separated")
    ap.add_argument("--families", default=None,
                    help="override: measure only these families (comma separated). The run records the "
                         "subset it covered, so a partial population is visible rather than implied.")
    ap.add_argument("--threads", default=None, help="override, comma separated")
    ap.add_argument("--dtypes", default=None)
    ap.add_argument("--engines", default=None)
    ap.add_argument("--label", default=None, help="suffix for the run directory")
    args = ap.parse_args()

    profiles = yaml.safe_load((ROOT / "benchmarks/profiles.yaml").read_text())["profiles"]
    suite = yaml.safe_load((ROOT / "benchmarks/suites" / f"{args.suite_id}.yaml").read_text())
    spec = suite["runs"][0]
    declared = populations(suite)
    covered = declared
    if args.regimes:
        wanted = set(args.regimes.split(","))
        covered = [p for p in declared if p["regime"] in wanted]
    if args.families:
        wanted = set(args.families.split(","))
        declared_families = {f for p in declared for f in p["families"]}
        unknown = wanted - declared_families
        if unknown:
            sys.exit(f"ERROR: {sorted(unknown)} are not declared by this suite")
        covered = [dict(p, families=[f for f in p["families"] if f in wanted]) for p in covered]
        covered = [p for p in covered if p["families"]]
    threads = [int(t) for t in args.threads.split(",")] if args.threads else spec["threads"]
    dtypes = args.dtypes.split(",") if args.dtypes else spec["dtypes"]
    engines = args.engines.split(",") if args.engines else spec["engines"]
    cpu_sets = {str(t): spec["cpu_sets"][spec["threads"].index(t)] for t in threads}

    # One measurement at a time, and no build while a measurement runs. Taken
    # before the build and held for the whole run.
    lock_path = ROOT / "target/campaign.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock = open(lock_path, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit("ERROR: another campaign run holds target/campaign.lock; "
                 "the campaign is one measurement at a time")

    checkout = pathlib.Path(args.checkout)
    pin = build(checkout)
    rev, dirty = pin["TLINALG_REV"], pin["TLINALG_DIRTY"] == "true"
    if dirty:
        print("WARNING: the measured checkout is dirty; this cell will be marked dirty", file=sys.stderr)

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"{stamp}-{args.label}" if args.label else stamp
    run_dir = ROOT / "data/results" / args.profile / args.suite_id / name
    run_dir.mkdir(parents=True, exist_ok=True)

    bin_dir = pathlib.Path(pin["BIN_DIR"])
    tlbench = bin_dir / "tlbench"
    pinned = checkout / "benchmarks/scripts/pinned.sh"
    idle = checkout / "benchmarks/scripts/idle_cpus.py"
    if not pinned.exists() or not idle.exists():
        sys.exit(f"ERROR: {pinned} or {idle} missing; the protocol scripts belong to the measured revision")

    # The thread budget is the measurement's, not the environment's. The vendor
    # library is set from the row's budget by the harness and read back, so an
    # ambient value must not be inherited as if it were a declaration.
    env = dict(os.environ)
    for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "RAYON_NUM_THREADS"):
        env.pop(variable, None)
    env.setdefault("CARGO_BUILD_JOBS", str(max(1, (os.cpu_count() or 4) // 4)))

    vendor = vendor_identity(tlbench, env)
    if "openblas" in {PROVIDER_OF_ENGINE.get(e) for e in engines} and (
            not vendor.get("vendor.name") or vendor["vendor.name"] == "none"):
        sys.exit("ERROR: the suite declares a vendor arm, but the harness reports no vendor library")

    guards = []
    csvs = []
    skipped = {}

    # 1. correctness first, for the whole covered grid, at every budget.
    for population in covered:
        for t in threads:
            stem = f"verify-{population['regime']}-{t}t"
            out = run_dir / f"{stem}.txt"
            guard = run_dir / f"{stem}.guard"
            r = subprocess.run([str(pinned), cpu_sets[str(t)], "--", str(tlbench), "verify",
                                "--threads", str(t),
                                "--n", ",".join(population["n"]),
                                "--batch", ",".join(str(b) for b in population["batch"]),
                                "--dtype", ",".join(dtypes),
                                "--family", ",".join(population["families"])],
                               env=env, capture_output=True, text=True)
            out.write_text(r.stdout)
            guard.write_text(r.stderr)
            guards.append(guard.name)
            if r.returncode != 0 or "MISMATCH" in r.stdout:
                sys.exit(f"ERROR: verify failed for {population['regime']} {t}T (see {out}); nothing published")
            if "all comparisons within tolerance" not in r.stdout:
                sys.exit(f"ERROR: verify did not report a clean grid for {population['regime']} {t}T")

    # 2. timing, one CSV per (repeat, population, threads).
    for rep in range(args.aa):
        for population in covered:
            for t in threads:
                stem = f"run{rep}-{population['regime']}-{t}t"
                r = subprocess.run([str(pinned), cpu_sets[str(t)], "--", str(tlbench), "run",
                                    "--threads", str(t),
                                    "--n", ",".join(population["n"]),
                                    "--batch", ",".join(str(b) for b in population["batch"]),
                                    "--dtype", ",".join(dtypes),
                                    "--family", ",".join(population["families"]),
                                    "--regime", population["regime"],
                                    "--reps", str(args.reps), "--prime-ms", str(args.prime_ms),
                                    "--csv", str(run_dir / f"{stem}.csv")],
                                   env=env, capture_output=True, text=True)
                (run_dir / f"{stem}.guard").write_text(r.stderr)
                guards.append(f"{stem}.guard")
                if r.returncode != 0:
                    sys.exit(f"ERROR: run failed for {population['regime']} {t}T (repeat {rep}): {r.stderr[-2000:]}")
                if not (run_dir / f"{stem}.csv").exists():
                    sys.exit(f"ERROR: no CSV produced for {population['regime']} {t}T")
                csvs.append(str(run_dir / f"{stem}.csv"))

    skipped = skipped_of(csvs)
    recorded = []
    for population in covered:
        entry = dict(population)
        if skipped.get(population["regime"]):
            entry["skipped"] = sorted(skipped[population["regime"]])
        recorded.append(entry)

    manifest = {
        "schema_version": 1,
        "target_profile": args.profile,
        "suite_id": args.suite_id,
        "suite_file": f"benchmarks/suites/{args.suite_id}.yaml",
        "suite_sha256": hashlib.sha256(
            (ROOT / "benchmarks/suites" / f"{args.suite_id}.yaml").read_bytes()).hexdigest(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": " ".join(sys.argv),
        "library": {
            "url": "https://github.com/tensor4all/tlinalg-rs",
            "commit": rev,
            "dirty": dirty,
            "features": [f for f in pin["BUILD_FEATURES"].split(",") if f],
            "measured_path": pin["TLINALG_DIR"],
            "version": None,
        },
        "vendor": vendor_block(vendor, pin.get("BUILD_ENV")),
        "harness": {
            "commit": git(ROOT, "rev-parse", "HEAD"),
            "dirty": bool(git(ROOT, "status", "--porcelain", "--untracked-files=no")),
        },
        "host": host_info(args.profile, profiles),
        "threads": {
            "counts": threads,
            "cpu_sets": cpu_sets,
            "env": {k: os.environ.get(k) for k in
                    ["OMP_NUM_THREADS", "RAYON_NUM_THREADS", "OPENBLAS_NUM_THREADS"]},
            "note": "the vendor's budget is set by the harness from the row's thread count and "
                    "read back before each measurement; these variables were removed from the "
                    "measured process's environment so it cannot inherit a different one",
        },
        "timing_policy": {
            "version": 1,
            "minimum_untimed_priming_ms": args.prime_ms,
            "statistic": "best",
            "repetitions": args.reps,
            "notes": "priming is time-based, not a call count: after an idle gate this host "
                     "reads low for the first second or two of sustained work",
        },
        "guards": {
            "idle_window_seconds": int(os.environ.get("PINNED_IDLE_SECONDS", 3)),
            "max_busy_percent": round(float(os.environ.get("PINNED_MAX_BUSY", 0.05)) * 100, 3),
            "attempts": int(os.environ.get("PINNED_RETRIES", 3)),
            "sibling_aware": True,
            "logs": sorted(set(guards)),
        },
        "providers": providers_for(engines, vendor),
        "invalidated_by": suite["invalidated_by"],
        "result_files": [pathlib.Path(c).name for c in csvs],
        "run_spec": {
            "populations": recorded,
            "dtypes": dtypes,
            "engines": engines,
            "aa": args.aa,
            "covers_declared_suite": (threads == spec["threads"]
                                      and dtypes == spec["dtypes"]
                                      and engines == spec["engines"]
                                      and same_populations(covered, declared)),
        },
    }

    manifest_path = run_dir / "run.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
    v = subprocess.run([sys.executable, str(ROOT / "scripts/validate_run.py"), str(manifest_path)],
                       capture_output=True, text=True)
    print(v.stdout + v.stderr, file=sys.stderr)
    if v.returncode != 0:
        sys.exit("ERROR: run.yaml does not validate; nothing published")

    subprocess.run([sys.executable, str(ROOT / "scripts/report_run.py"), "--run-dir", str(run_dir)], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/publish_report.py"), str(run_dir)], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
