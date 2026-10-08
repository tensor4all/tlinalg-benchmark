# `tlinalg-benchmark`

The benchmark campaign for [tlinalg-rs](https://github.com/tensor4all/tlinalg-rs):
results keyed by **library commit × hardware profile**, with the staleness of
every cell visible rather than implied. It is the same shape as
[tprims-benchmark](https://github.com/tensor4all/tprims-benchmark), which owns the
same job for `tprims-rs`.

| | |
|---|---|
| Latest results | [`result/INDEX.md`](result/INDEX.md) — generated table of contents over the per-revision pages |
| Result layout | [`docs/results.md`](docs/results.md) |
| Timing policy | [`docs/timing-policy.md`](docs/timing-policy.md) |
| Reference revision | [`pins/tlinalg-rs.rev`](pins/tlinalg-rs.rev) — what `status` is measured against |
| Design record | [`docs/worklog.md`](docs/worklog.md) — decisions, fixed failures, open items |

## How it works

The harness lives in tlinalg-rs (`crates/tlinalg-bench`, binary `tlbench`) and is
built **out of the same checkout as the library it measures**, into a target
directory keyed by that commit. A harness built from this repository could
silently measure a different revision of the library than the one it was written
against; building it in place makes the recorded commit describe both.

```bash
./scripts/setup_extern_deps.sh                     # clone tlinalg-rs at pins/tlinalg-rs.rev
./scripts/setup_extern_deps.sh /path/to/checkout   # or symlink a local checkout

# record one cell: build, verify, measure, validate, publish, reindex
python3 scripts/record_run.py zen5-cpu tlinalg-kernels
```

The comparison is between the two providers of the interface — the faer-backed
`tlinalg` and the LAPACK/BLAS-backed `tlinalg-blas` — with the vendor library
named and its own thread budget set and read back, because a row labelled `1T` is
only a single-thread measurement if the vendor library also ran on one thread.
OpenBLAS is the first vendor; BLIS is a later arm and needs its own linkage
decision, since BLIS ships no LAPACK.

## What this repository is not

It is not the library's per-PR suite. tlinalg-rs keeps its own Criterion rows
(`crates/tlinalg-bench/benches/kernels.rs`), its protocol scripts
(`benchmarks/scripts/{pinned.sh,idle_cpus.py}`) and its harness; this repository
owns the campaign: the declarations, the revision pin, the run manifests, the
index and the published reports.
