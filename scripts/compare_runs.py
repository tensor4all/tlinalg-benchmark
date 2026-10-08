#!/usr/bin/env python3
"""Compare two recorded runs of the same suite: what changed between two revisions.

    compare_runs.py <before-run-dir> <after-run-dir> [--families a,b] [--threads 1]

Both directories are raw run directories (`data/results/<profile>/<suite>/<timestamp>/`),
and both must have been produced by `tlbench` over overlapping cells. For every
cell the table reports the ratio `after / before` of the best wall time, so a value
below 1 means the change made that cell faster.

What this is and is not:

* it is a **scan** over whatever the two runs covered. A cell that only one run
  contains is reported as such and contributes no ratio, because a difference
  between two different populations is not a comparison;
* a ratio from a single complete set is not a performance claim. The timing policy
  requires complete-set repeats for that, and this prints the A/A spread when the
  runs have them, so a reader can see whether the difference is above the noise;
* it says nothing about a family neither run measured.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import statistics
import sys

COLUMNS = ["regime", "family", "dtype", "m", "n", "batch", "row", "threads",
           "total_ms", "per_item_us", "status", "note"]


def read(run_dir: pathlib.Path):
    """(cell -> [ms per repeat]) plus the repeat count and the manifest."""
    cells: dict[tuple, list[float]] = {}
    repeats = set()
    for path in sorted(run_dir.glob("run*.csv")):
        repeats.add(path.stem.split("-")[0])
        with open(path) as handle:
            for row in csv.DictReader(handle):
                missing = [c for c in COLUMNS if c not in row]
                if missing:
                    sys.exit(f"{path}: missing columns {missing}")
                if row["status"] != "ok":
                    continue
                key = (row["regime"], row["family"], row["dtype"], int(row["m"]),
                       int(row["n"]), int(row["batch"]), row["row"], int(row["threads"]))
                cells.setdefault(key, []).append(float(row["total_ms"]))
    return cells, len(repeats)


def shape(key) -> str:
    _, family, _, m, n, batch, row, threads = key
    dims = f"n{n}" if m == n else f"{m}x{n}"
    return f"`{family}/{dims}/b{batch}` @{threads}T {row}"


def aggregate(pairs):
    """(family, threads, dtype) -> ratios, for the family-level table."""
    groups: dict[tuple, list[float]] = {}
    for key, ratio in pairs:
        _, family, dtype, _, _, _, _, threads = key
        groups.setdefault((family, threads, dtype), []).append(ratio)
    return groups


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--families", default=None, help="only these families (comma separated)")
    ap.add_argument("--threads", default=None, help="only this thread count")
    args = ap.parse_args()

    before_dir, after_dir = pathlib.Path(args.before), pathlib.Path(args.after)
    before, before_repeats = read(before_dir)
    after, after_repeats = read(after_dir)

    wanted = set(args.families.split(",")) if args.families else None
    keys = sorted(set(before) & set(after))
    if wanted:
        keys = [k for k in keys if k[1] in wanted]
    if args.threads:
        keys = [k for k in keys if k[7] == int(args.threads)]

    print(f"# {args.before} -> {args.after}")
    print()
    print(f"- complete-set repeats: before {before_repeats}, after {after_repeats}")
    only_before = len(set(before) - set(after))
    only_after = len(set(after) - set(before))
    print(f"- cells only in one run (no ratio): {only_before} before, {only_after} after")
    if min(before_repeats, after_repeats) < 2:
        print("- this is a **scan**, not a paired comparison: at least one side has a single")
        print("  complete set, so the ratios carry no A/A spread")
    print()

    pairs = []
    print("## Per cell")
    print()
    print("| cell | before (ms) | after (ms) | after/before |")
    print("|---|---|---|---|")
    for key in keys:
        b, a = min(before[key]), min(after[key])
        pairs.append((key, a / b))
        mark = "" if 0.95 <= a / b <= 1.05 else (" **faster**" if a < b else " slower")
        print(f"| {shape(key)} | {b:.6g} | {a:.6g} | {a / b:.3f}{mark} |")

    print()
    print("## Per family")
    print()
    print("| family | threads | dtype | cells | median after/before | min | max |")
    print("|---|---|---|---|---|---|---|")
    for (family, threads, dtype), ratios in sorted(aggregate(pairs).items()):
        print(f"| `{family}` | {threads}T | {dtype} | {len(ratios)} | "
              f"{statistics.median(ratios):.3f} | {min(ratios):.3f} | {max(ratios):.3f} |")

    if min(before_repeats, after_repeats) >= 2:
        print()
        print("## A/A spread within each run")
        print()
        for name, cells in (("before", before), ("after", after)):
            spreads = [max(v) / min(v) for v in cells.values() if len(v) > 1 and min(v) > 0]
            if spreads:
                print(f"- {name}: median max/min {statistics.median(spreads):.3f}, "
                      f"worst {max(spreads):.3f} over {len(spreads)} cells")
    return 0


if __name__ == "__main__":
    sys.exit(main())
