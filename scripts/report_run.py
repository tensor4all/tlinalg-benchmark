#!/usr/bin/env python3
"""Turn one run's tlbench CSVs into the tracked report for a (profile, suite) cell.

Only the numbers that came from a verified run are published: every row here was
gated by `tlbench verify` (reconstruction, orthonormality and residual checks,
family by family) before the timing pass started. The report repeats the run's
provenance in its own header, because a table that is copied into a discussion
without its commit is the thing this repository exists to stop.
"""
import argparse
import csv
import pathlib
import statistics
import sys

from campaign import ROOT, load

COLUMNS = ["regime", "family", "dtype", "m", "n", "batch", "row", "threads",
           "total_ms", "per_item_us", "status", "note"]


def read_rows(csv_paths):
    """Rows from the run CSVs, tagged with the repeat they came from.

    A repeat is one complete pass over the declared populations; the harness
    already reduced `--reps` timed iterations to a best time, so a repeat holds
    one number per (case, engine row).
    """
    rows = []
    for path in csv_paths:
        repeat = pathlib.Path(path).stem.split("-")[0]  # run0-small-8t -> run0
        with open(path) as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                missing = [c for c in COLUMNS if c not in row]
                if missing:
                    raise SystemExit(f"{path}: missing columns {missing}")
                row["repeat"] = repeat
                rows.append(row)
    return rows


def case_name(row):
    shape = f"n{row['n']}" if row["m"] == row["n"] else f"{row['m']}x{row['n']}"
    return f"{row['family']}/{shape}/b{row['batch']}"


def best_per_case(rows):
    """(case, dtype, threads) -> engine row -> (best ms, spread), skipped cases."""
    best, skipped = {}, {}
    for row in rows:
        key = (row["regime"], case_name(row), row["dtype"], int(row["threads"]))
        if row["status"] == "skipped":
            skipped.setdefault((row["regime"], int(row["threads"])), set()).add(
                f"{row['family']}/{row['m']}x{row['n']}")
            continue
        if row["status"] != "ok":
            continue
        times = best.setdefault(key, {}).setdefault(row["row"], [])
        times.append(float(row["total_ms"]))
    return best, skipped


def render(manifest, suite, rows, run_dir):
    vendor = manifest.get("vendor") or {}
    engines = manifest["run_spec"]["engines"]
    row_names = [e for e in ["faer-1lane", "faer-pool", "lapack-openblas"] if e in engines]
    best, skipped = best_per_case(rows)
    out = [
        f"# `{manifest['suite_id']}` on `{manifest['target_profile']}`",
        "",
        f"- tlinalg-rs commit: `{manifest['library']['commit']}`"
        + (" **(dirty)**" if manifest["library"]["dirty"] else ""),
        f"- features: `{', '.join(manifest['library']['features']) or 'default'}`",
        f"- harness commit: `{manifest['harness']['commit']}`",
        f"- hardware profile: `{manifest['target_profile']}`",
        f"- timestamp: `{manifest['timestamp']}`",
        f"- timing policy: v{manifest['timing_policy']['version']}, "
        f"{manifest['timing_policy']['statistic']} of {manifest['timing_policy']['repetitions']} reps, "
        f"priming {manifest['timing_policy']['minimum_untimed_priming_ms']} ms "
        f"(time-based, identical on every row)",
        f"- guards: idle window {manifest['guards']['idle_window_seconds']} s, "
        f"max busy {manifest['guards']['max_busy_percent']}% including SMT siblings, "
        f"{manifest['guards']['attempts']} attempts",
        f"- command: `{manifest['command']}`",
        f"- raw data: `{run_dir.relative_to(ROOT)}/`",
        "",
        "## What was measured",
        "",
        f"- **Workload** — {suite['workloads']['description']}",
        f"  Source: {suite['workloads']['source']}",
    ]
    for spot in suite["workloads"].get("known_blind_spots", []):
        out.append(f"  Known blind spot: {spot}")
    out += ["- **Rows** — one row per engine in every table below:"]
    for engine in row_names:
        doc = suite["engines_doc"].get(engine)
        if doc is None:
            out.append(f"  - `{engine}` — (undocumented in the suite declaration)")
            continue
        out.append(f"  - `{engine}` — {doc['summary']}")
        out.append(f"    Identity: {doc['identity']}")
        if doc.get("caveat"):
            out.append(f"    Caveat: {doc['caveat']}")
    if row_names and "lapack-openblas" in row_names:
        parts = [f"linked {vendor.get('linkage', '?')}"]
        if vendor.get("version"):
            parts.append(f"OpenBLAS {vendor['version']}")
        if vendor.get("corename"):
            parts.append(f"kernel dispatched to `{vendor['corename']}`")
        if vendor.get("parallel"):
            parts.append(f"{vendor['parallel']} threading")
        if vendor.get("config"):
            parts.append(f"config `{vendor['config']}`")
        out.append(f"    As measured: " + "; ".join(parts))
    out += [
        "",
        "## Hardware",
        "",
        f"- CPU: `{manifest['host']['cpu']}`",
        f"- logical CPUs: `{manifest['host']['logical_cpus']}`",
        f"- L3: `{manifest['host']['l3']}`",
        f"- L3 domains: `{manifest['host'].get('l3_domains') or manifest['host']['l3']}`",
        f"- OS / arch: `{manifest['host']['os']}` / `{manifest['host']['arch']}`",
        f"- hostname: `{manifest['host']['hostname']}`",
        "- CPU sets: " + ", ".join(f"{t}T -> `{c}`"
                                   for t, c in sorted(manifest["threads"]["cpu_sets"].items(),
                                                      key=lambda kv: int(kv[0]))),
        "",
        "Every row below passed `tlbench verify` on the same grid before timing: the two",
        "providers' factorizations are checked against each provider's documented convention",
        "(reconstruction, orthonormality, residuals), not against each other's floating-point",
        "output. Times are milliseconds, the best wall time per case and engine row; with more",
        "than one complete set repeat the table shows the best repeat, and the A/A spread is",
        "reported at its foot.",
        "",
    ]
    for population in manifest["run_spec"]["populations"]:
        regime = population["regime"]
        for dtype in manifest["run_spec"]["dtypes"]:
            for threads in manifest["threads"]["counts"]:
                cases = sorted({k[1] for k in best if k[0] == regime and k[2] == dtype
                                and k[3] == threads})
                if not cases:
                    continue
                out.append(f"## {regime}, {dtype}, {threads}T "
                           f"(CPU {manifest['threads']['cpu_sets'].get(str(threads), '?')})")
                out.append("")
                out.append("| case | " + " | ".join(f"{e} (ms)" for e in row_names) + " |")
                out.append("|" + "---|" * (len(row_names) + 1))
                for case in cases:
                    cells = []
                    for engine in row_names:
                        times = best.get((regime, case, dtype, threads), {}).get(engine, [])
                        cells.append(f"{min(times):.4f}" if times else "-")
                    out.append(f"| `{case}` | " + " | ".join(cells) + " |")
                out.append("")
                if threads in [t for (r, t) in skipped if r == regime]:
                    cases_skipped = sorted(skipped[(regime, threads)])
                    out.append(f"Not applicable to these shapes and reported as skipped: "
                               f"{', '.join('`' + c + '`' for c in cases_skipped)}.")
                    out.append("")
    if manifest["run_spec"]["aa"] > 1:
        spreads = []
        for key, per_row in best.items():
            for engine, times in per_row.items():
                if len(times) > 1 and min(times) > 0:
                    spreads.append(max(times) / min(times))
        if spreads:
            out.append(f"A/A across {manifest['run_spec']['aa']} complete set repeats: "
                       f"median max/min {statistics.median(spreads):.3f}, "
                       f"worst {max(spreads):.3f}. A comparison is made from paired repeats, "
                       f"not from one table read twice.")
            out.append("")
    else:
        out.append("This run made a single complete set, so it carries no A/A: it is a scan, "
                   "not a paired comparison.")
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run_dir = pathlib.Path(args.run_dir).resolve()
    manifest = load(run_dir / "run.yaml")
    suite = load(ROOT / "benchmarks/suites" / f"{manifest['suite_id']}.yaml")
    rows = read_rows(sorted(run_dir.glob("*.csv")))
    (run_dir / "report.md").write_text(render(manifest, suite, rows, run_dir))
    print(f"wrote {run_dir}/report.md from {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
