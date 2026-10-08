# Timing policy, version 1

Recorded in every `run.yaml` as `timing_policy`. A run carries the version in
force when it was taken; do not compare ratios across versions, and do not use an
earlier version's numbers to assess a later library revision.

## What is timed

Steady-state kernel execution. Inputs, layouts, output buffers and the recycling
LAPACK workspace are prepared before the clock starts. The clock stops after the
provider call returns, with outputs still alive. Restoring a mutated input
between iterations happens **outside** the clock: this is the boundary the
campaign declares, and it is deliberately not the boundary of the Criterion rows
in `crates/tlinalg-bench/benches/kernels.rs`, which restore inputs inside the timed
closure. Compare across the two only after accounting for that.

Tensor construction, dtype dispatch, session entry and pool checkout are
tenferro's work and are not in any number here.

## Priming

At least 0.5 s of untimed, time-based priming per row, and the same amount of
time on every row. A fixed call count is not equivalent: after an idle gate this
host reads low for the first second or two of sustained work, which is easily
mistaken for a kernel defect. The reference harness in `tprims-rs` records
`minimum_untimed_priming_ms: 500` while its timer performs a single warm-up call
(`benchmarks/benchmarks/tcbench/engines/mod.rs`); `tlbench` measures the priming
time instead, and the recorder records the value it was asked for.

## Thread budget

`--threads N` is required for a campaign row and is enforced at both levels: a
Rayon pool of `N` workers for the faer rows, and the vendor library's own thread
count for the LAPACK row, set with `openblas_set_num_threads` and read back with
`openblas_get_num_threads` before each measurement. A mismatch is an error, not a
warning, because a row labelled `1T` whose vendor library ran on 24 threads is a
lie with a number attached. The ambient `OPENBLAS_NUM_THREADS`, `OMP_NUM_THREADS`
and `RAYON_NUM_THREADS` are removed from the measured process and their absence
is recorded.

## Statistic and repetitions

`best` wall time per engine row and case, over 5 timed repetitions, with the
complete set repeated for A/A when a comparison is being made. The harness
reports the best time per row; the report aggregates repeats and prints the A/A
spread. A single scan flags suspects; only a complete paired run makes a
performance claim.

**Measured noise floor, and what it costs the pooled row.** Two complete sets of
the *same* revision (the small regime, 1T and 8T, 360 cells per row) give the
ratios below, which must be 1.0 if a row reproduces. They do not, for the pooled
rows:

| threads | row | median | p10-p90 | cells off by more than 15% |
|---|---|---|---|---|
| 1T | `faer-1lane` | 1.002 | 0.972-1.029 | 1.1% |
| 1T | `lapack-openblas` | 1.000 | 0.985-1.018 | 0.0% |
| 8T | `faer-1lane` | 1.005 | 0.983-1.038 | 1.1% |
| 8T | `faer-pool` | 1.007 | 0.771-1.463 | **28.9%** |
| 8T | `lapack-openblas` | 0.998 | 0.972-1.030 | 5.3% |

A per-cell claim is therefore made on the **1T rows**, where a complete set
reproduces to about 3%; the pooled rows move by up to 2.5x between complete sets
of identical code, so a pooled number is a distribution rather than a value unless
several complete sets are taken, and the vendor's threaded rows sit in between. A
comparison that reports pooled cells without their spread is reporting machine
state. `scripts/compare_runs.py` prints the per-cell ratios and the A/A spread for
exactly this reason.

## Guarding the host

Every measurement runs through `benchmarks/scripts/pinned.sh` of the measured
checkout: `taskset` to the declared CPU set, a 3-second `/proc/stat` idle window
covering those CPUs **and their SMT siblings**, at most 5% busy before and after,
3 attempts. A spoiled run is discarded, not published. The recorder holds one
campaign-level lock across build, verify and timing, so no second recorder builds
another revision while a measurement runs; unrelated workloads remain an
operator precondition.

## What a report may and may not claim

A report states the revision, the host, the vendor and its kernel, the coverage
and the guards, and it is a claim about *that* cell. It is not evidence about a
population the run did not contain: a grid whose large regime has unit batch
extent says nothing about per-batch-element cost at that size, and the index's
`coverage` column plus `run_spec.populations[].skipped` are the mechanisms that
keep that visible.
