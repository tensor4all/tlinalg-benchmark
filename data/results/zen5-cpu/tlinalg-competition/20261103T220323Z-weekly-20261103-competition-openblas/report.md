# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `3635d96231122648fe3f239027d9f29065331a4c`
- toolkit commit: `74e50e8199cb2c2f07e810744a0943fc3a8c1170`
- measured binary SHA-256: `028b45886580e5353ddee46798f3d2cd7cf52f7521251264812b3a908590da86`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-03T22:24:02.668087Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor openblas --aa 4 --reps 5 --prime-ms 250 --label weekly-20261103-competition-openblas --no-publish`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261103T220323Z-weekly-20261103-competition-openblas/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: The batched regime stops at n=32 by choice: batch 1024 is the regime this campaign is about, and the four shapes up to 32 already separate the rows by four to nine times, so larger matrices would add cells without changing the answer. Above that size faer-benchmark measures the same backends. (Recorded while the grid still held 64: one verify pass at n=64 ran past 45 minutes because the harness recomputes every case, which made the last shape cost far more than it added.)
  Known blind spot: Only the kernel entry points are measured. Tensor construction, dtype dispatch, session entry and pool checkout are tenferro's and are out of scope.
  Known blind spot: The 2026-10-17 trim narrowed the suite to the batched small regime plus three single-shape canaries (factor at 128, decompose at 512, rectangular at 4096x256, each at batch 1). The medium, large and tall grids are no longer measured here: faer-benchmark measures that geometry directly with the same backends these rows wrap, so a cost that appears only at those sizes has to be read from that campaign's page.
  Known blind spot: The small regime declares batch 1 and 1024 and gives up the middle of the axis, so a cost that appears only at an intermediate batch is not covered.
  Known blind spot: The thread axis is 1T and 8T; a budget between them (4T) is not measured, so a scaling curve cannot be read off this page.
  Known blind spot: The providers are compared at the thread budgets declared here; a budget the vendor threads itself by, outside that set, is not covered.
  Known blind spot: A vendor arm records the vendor library, but only OpenBLAS reports the kernel its runtime dispatched to. MKL's manifest records its own version and the threading layer the harness pins; it names no kernel, because MKL exposes none to name.
  Known blind spot: The batched regime measures batch 1024 only: batch 1 has nothing to parallelise, so it measures dispatch rather than the library, and the canaries carry the single-call sizes. An intermediate batch is therefore not covered.
- **Rows** — one row per engine in every table below:
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
  - `lapack-openblas` — The LAPACK/BLAS provider: vendor calls and their marshalling, a serial batch loop, vendor-owned threading. The vendor's own thread budget is set by the harness before the row and read back, and the vendor identity and the kernel its runtime dispatched to are recorded in the manifest.
    Identity: the OpenBLAS build recorded in this run's manifest (`providers[openblas]`)
    Caveat: LAPACK and BLAS own their threading, so this row's thread budget is the vendor's, not the host pool's. Where a family has no LAPACK route the row is absent and the CSV says the case was skipped for it.
    As measured: linked static; openblas 0.3.32; kernel dispatched to `Cooperlake`; pthread threading; config `OpenBLAS 0.3.32 DYNAMIC_ARCH NO_AFFINITY Cooperlake MAX_THREADS=24`

## Hardware

- CPU: `AMD Ryzen AI 9 HX 470`
- logical CPUs: `24`
- L3: `24 MiB (2 instances)`
- L3 domains: `0-3: 16 MiB shared; 4-11: 8 MiB shared`
- OS / arch: `Linux 7.0.0-38-generic` / `x86_64`
- hostname: `shinaoka-EVO-X1Pro`
- CPU sets: 8T -> `4-11`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 4 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.37%, worst 29.63% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 30 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.31%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
The `vs tlinalg-pool` column is the rotation-averaged ratio
exp(mean over starts of log(engine median / tlinalg-pool median)),
with the per-start ratios beside it: `R > 1`
means the engine was slower than that first-declared row in that start. It removes a
row-position
effect only under one position effect shared by the engines and stable across starts,
and only where every declared engine has a measured row (`*` marks a cell where one has
no row, so no ratio there is position-balanced). `!` marks a cell where some engine's own
per-start median range exceeds 5% of its median, and `p` a balanced cell whose estimated
position-effect ratio exceeds 1.05. Flagged cells are retained, not discarded; the
between-start variation can exceed the difference being compared.
The `vs` columns mark only differences larger than the spread this run recorded for those
two rows (combined between-start SD, floored at 5%), always with the measured library as the subject:
`🔵 <row> X faster than <row>` / `🔴 <row> X slower than <row>` (the subject is the first column of the table, the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

## batch-small, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.114999 ± 0.00080726 (W 0.000542542) | 1.01537 ± 0.00850051 (W 0.00341607) | 🔵 tlinalg-pool 8.83× faster than `lapack-openblas` |  |
| `cholesky/n32/b1024` | 0.471587 ± 0.00611432 (W 0.00571276) | 3.62407 ± 0.0272751 (W 0.0116937) | 🔵 tlinalg-pool 7.68× faster than `lapack-openblas` |  |
| `cholesky/n4/b1024` | 0.178818 ± 0.00106701 (W 0.00156467) | 0.210532 ± 0.000421928 (W 0.00175298) | 🔵 tlinalg-pool 1.18× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.047689 ± 0.000472461 (W 0.000204413) | 0.402884 ± 0.00333301 (W 0.00306122) | 🔵 tlinalg-pool 8.45× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 12.0366 ± 0.0689959 (W 0.0271377) | 68.2543 ± 0.342759 (W 0.0506906) | 🔵 tlinalg-pool 5.67× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 53.9761 ± 1.16995 (W 0.0456899) | 324.5 ± 1.35838 (W 0.53453) | 🔵 tlinalg-pool 6.01× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 0.809982 ± 0.00389159 (W 0.00361641) | 5.33347 ± 0.0210274 (W 0.0082835) | 🔵 tlinalg-pool 6.58× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 3.02035 ± 0.0585984 (W 0.00627696) | 17.4804 ± 0.0982968 (W 0.0156108) | 🔵 tlinalg-pool 5.79× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 3.7641 ± 0.0133755 (W 0.00606332) | 40.2601 ± 0.23486 (W 0.118063) | 🔵 tlinalg-pool 10.70× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 13.9609 ± 0.373011 (W 0.0168548) | 117.949 ± 0.566359 (W 0.214513) | 🔵 tlinalg-pool 8.45× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigh/n4/b1024` | 0.31968 ± 0.00497365 (W 0.00186447) | 3.04147 ± 0.00891315 (W 0.00642705) | 🔵 tlinalg-pool 9.51× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.09632 ± 0.00600241 (W 0.0035092) | 10.8369 ± 0.0378043 (W 0.0137091) | 🔵 tlinalg-pool 9.88× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 8.32436 ± 0.0401174 (W 0.0115187) | 49.5337 ± 0.172739 (W 0.0486976) | 🔵 tlinalg-pool 5.95× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 36.5902 ± 0.129896 (W 0.0814629) | 217.173 ± 1.07792 (W 0.621944) | 🔵 tlinalg-pool 5.94× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.435976 ± 0.00238041 (W 0.00181386) | 3.42012 ± 0.00827675 (W 0.00650913) | 🔵 tlinalg-pool 7.84× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 1.98509 ± 0.0127685 (W 0.00481666) | 13.4105 ± 0.0156324 (W 0.0387181) | 🔵 tlinalg-pool 6.76× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 2.84793 ± 0.00953282 (W 0.00461835) | 14.5421 ± 0.0085126 (W 0.0169321) | 🔵 tlinalg-pool 5.11× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 10.5934 ± 0.019739 (W 0.0108732) | 49.9544 ± 0.169663 (W 0.0618225) | 🔵 tlinalg-pool 4.72× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.264136 ± 0.00366913 (W 0.00211811) | 1.38881 ± 0.00304777 (W 0.00441117) | 🔵 tlinalg-pool 5.26× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.878184 ± 0.00757219 (W 0.0018497) | 4.52363 ± 0.0211898 (W 0.0107195) | 🔵 tlinalg-pool 5.15× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.516787 ± 0.0238543 (W 0.00455155) | 4.74863 ± 0.0449822 (W 0.0262291) | 🔵 tlinalg-pool 9.19× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 2.04084 ± 0.0223233 (W 0.0104667) | 28.221 ± 0.450531 (W 0.106716) | 🔵 tlinalg-pool 13.83× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1024` | 0.491585 ± 0.00539306 (W 0.00352094) | 0.366912 ± 0.0199469 (W 0.00258906) | 🔴 tlinalg-pool 1.34× slower than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.18294 ± 0.00275719 (W 0.00146423) | 1.0604 ± 0.0154127 (W 0.00425507) | 🔵 tlinalg-pool 5.80× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n16/b1024` | 0.517678 ± 0.00594376 (W 0.00354292) | 6.47837 ± 0.00867126 (W 0.0279972) | 🔵 tlinalg-pool 12.51× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 1.63467 ± 0.022562 (W 0.0113007) | 30.9503 ± 0.544325 (W 0.18675) | 🔵 tlinalg-pool 18.93× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.0862905 ± 0.000510498 (W 0.000673493) | 1.00728 ± 0.0368781 (W 0.00455083) | 🔵 tlinalg-pool 11.67× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.209054 ± 0.00251196 (W 0.00278404) | 2.03687 ± 0.0883941 (W 0.00403416) | 🔵 tlinalg-pool 9.74× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n16/b1024` | 0.62644 ± 0.00951663 (W 0.00191077) | 4.48717 ± 0.082878 (W 0.0122098) | 🔵 tlinalg-pool 7.16× faster than `lapack-openblas` |  |
| `householder_apply/n32/b1024` | 2.45474 ± 0.0446856 (W 0.00919243) | 18.8909 ± 0.618986 (W 0.054186) | 🔵 tlinalg-pool 7.70× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.053369 ± 0.00204069 (W 0.000177096) | 0.41669 ± 0.00803254 (W 0.00268626) | 🔵 tlinalg-pool 7.81× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.172681 ± 0.00406239 (W 0.000808285) | 1.22858 ± 0.0201265 (W 0.00406801) | 🔵 tlinalg-pool 7.11× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.51107 ± 0.00453809 (W 0.00165074) | 4.34179 ± 0.0251221 (W 0.0108565) | 🔵 tlinalg-pool 8.50× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 1.68157 ± 0.0167134 (W 0.00384278) | 14.6585 ± 0.134846 (W 0.0210465) | 🔵 tlinalg-pool 8.72× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.063438 ± 0.000427583 (W 0.00149533) | 0.536854 ± 0.00203789 (W 0.00275208) | 🔵 tlinalg-pool 8.46× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.169986 ± 0.00413125 (W 0.00155413) | 1.50717 ± 0.0109924 (W 0.00442759) | 🔵 tlinalg-pool 8.87× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n16/b1024` | 0.385898 ± 0.00531645 (W 0.00340734) | 2.44622 ± 0.0607801 (W 0.00532619) | 🔵 tlinalg-pool 6.34× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n32/b1024` | 1.36969 ± 0.0117524 (W 0.0107149) | 9.66062 ± 0.0890998 (W 0.0236128) | 🔵 tlinalg-pool 7.05× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.303675 ± 0.00488443 (W 0.00319706) | 0.345137 ± 0.0176745 (W 0.00280163) | 🔵 tlinalg-pool 1.14× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.133588 ± 0.00202879 (W 0.00137238) | 0.804552 ± 0.0134141 (W 0.00322217) | 🔵 tlinalg-pool 6.02× faster than `lapack-openblas` |  |
| `lu_factor/n16/b1024` | 0.25025 ± 0.00217844 (W 0.00178091) | 1.80425 ± 0.0172547 (W 0.00534155) | 🔵 tlinalg-pool 7.21× faster than `lapack-openblas` |  |
| `lu_factor/n32/b1024` | 0.716563 ± 0.0031882 (W 0.00352195) | 6.67458 ± 0.0373211 (W 0.0102815) | 🔵 tlinalg-pool 9.31× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.235288 ± 0.00129679 (W 0.00176881) | 0.218857 ± 0.00106665 (W 0.00194536) | 🔴 tlinalg-pool 1.08× slower than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.0957225 ± 0.00139435 (W 0.00161913) | 0.565813 ± 0.00282063 (W 0.00280699) | 🔵 tlinalg-pool 5.91× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.32512 ± 0.00279984 (W 0.00227084) | 3.44611 ± 0.0296957 (W 0.014166) | 🔵 tlinalg-pool 10.60× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 0.887246 ± 0.00797427 (W 0.00327136) | 9.52799 ± 0.181177 (W 0.0210378) | 🔵 tlinalg-pool 10.74× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.0577475 ± 0.000709772 (W 0.000953656) | 1.12689 ± 0.0369109 (W 0.00611644) | 🔵 tlinalg-pool 19.51× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.117964 ± 0.000633988 (W 0.001755) | 1.49074 ± 0.018328 (W 0.00813057) | 🔵 tlinalg-pool 12.64× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1024` | 0.096289 ± 0.0044367 (W 0.00170501) | 1.15083 ± 0.0133468 (W 0.0162897) | 🔵 tlinalg-pool 11.95× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n32/b1024` | 0.232844 ± 0.00436775 (W 0.00227694) | 2.12616 ± 0.0173876 (W 0.0126396) | 🔵 tlinalg-pool 9.13× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n4/b1024` | 0.020844 ± 0.000203814 (W 0.000126861) | 0.862054 ± 0.0337381 (W 0.00886446) | 🔵 tlinalg-pool 41.36× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.0436665 ± 0.00427894 (W 0.000359151) | 0.792189 ± 0.0192687 (W 0.017005) | 🔵 tlinalg-pool 18.14× faster than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n16/b1024` | 1.15297 ± 0.00648776 (W 0.00218654) | 7.84502 ± 0.0568411 (W 0.0159644) | 🔵 tlinalg-pool 6.80× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 4.21231 ± 0.0330782 (W 0.00841858) | 27.4918 ± 0.1247 (W 0.0277219) | 🔵 tlinalg-pool 6.53× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.101289 ± 0.00152389 (W 0.000328775) | 0.996188 ± 0.00379875 (W 0.00407204) | 🔵 tlinalg-pool 9.84× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 0.315777 ± 0.00478188 (W 0.00191653) | 2.65552 ± 0.00999246 (W 0.00525551) | 🔵 tlinalg-pool 8.41× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.36388 ± 0.00571348 (W 0.00315268) | 9.35639 ± 0.0720315 (W 0.0264903) | 🔵 tlinalg-pool 6.86× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 4.38408 ± 0.0454185 (W 0.0160198) | 34.0226 ± 0.526538 (W 0.042736) | 🔵 tlinalg-pool 7.76× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 0.173542 ± 0.000909545 (W 0.00166301) | 1.1787 ± 0.00843045 (W 0.00547962) | 🔵 tlinalg-pool 6.79× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.44345 ± 0.00234501 (W 0.00253724) | 3.06318 ± 0.0170522 (W 0.0167788) | 🔵 tlinalg-pool 6.91× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.360636 ± 0.00525993 (W 0.00373311) | 3.80206 ± 0.0739204 (W 0.00975129) | 🔵 tlinalg-pool 10.54× faster than `lapack-openblas` |  |
| `solve/n32/b1024` | 0.962241 ± 0.0196999 (W 0.00470355) | 9.87606 ± 0.109505 (W 0.0174167) | 🔵 tlinalg-pool 10.26× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.053339 ± 0.00290373 (W 0.000291101) | 1.35956 ± 0.0149715 (W 0.00426268) | 🔵 tlinalg-pool 25.49× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.128184 ± 0.014348 (W 0.00194877) | 1.99899 ± 0.0394277 (W 0.00699958) | 🔵 tlinalg-pool 15.59× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 6.8471 ± 0.162001 (W 0.00679189) | 81.5608 ± 0.477976 (W 0.0663585) | 🔵 tlinalg-pool 11.91× faster than `lapack-openblas` |  |
| `svd_full/n32/b1024` | 23.8692 ± 0.188808 (W 0.0246479) | 239.509 ± 0.649752 (W 0.206502) | 🔵 tlinalg-pool 10.03× faster than `lapack-openblas` |  |
| `svd_full/n4/b1024` | 0.557478 ± 0.0063244 (W 0.00178122) | 6.43027 ± 0.0542188 (W 0.00920479) | 🔵 tlinalg-pool 11.53× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 1.89418 ± 0.0258561 (W 0.00485911) | 21.2973 ± 0.125715 (W 0.0176233) | 🔵 tlinalg-pool 11.24× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 6.80114 ± 0.168272 (W 0.00928431) | 80.7007 ± 0.219438 (W 0.103533) | 🔵 tlinalg-pool 11.87× faster than `lapack-openblas` |  |
| `svd_thin/n32/b1024` | 23.8185 ± 0.166115 (W 0.0194316) | 239.886 ± 1.13093 (W 0.356726) | 🔵 tlinalg-pool 10.07× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1024` | 0.554778 ± 0.00331346 (W 0.002011) | 6.45594 ± 0.0178148 (W 0.00986292) | 🔵 tlinalg-pool 11.64× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1024` | 1.88941 ± 0.028127 (W 0.00335335) | 21.2526 ± 0.0617782 (W 0.0114524) | 🔵 tlinalg-pool 11.25× faster than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 2.7694 ± 0.0240677 (W 0.00426261) | 25.1226 ± 0.0882979 (W 0.0314801) | 🔵 tlinalg-pool 9.07× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 9.26355 ± 0.0409915 (W 0.0149484) | 80.0881 ± 0.348574 (W 0.0488261) | 🔵 tlinalg-pool 8.65× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.358938 ± 0.00170721 (W 0.00234747) | 3.4692 ± 0.0222557 (W 0.00930193) | 🔵 tlinalg-pool 9.67× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 0.988304 ± 0.01399 (W 0.00132159) | 9.01371 ± 0.0670896 (W 0.0125999) | 🔵 tlinalg-pool 9.12× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.068082 ± 0.000336695 (W 0.0013882) | 0.906647 ± 0.0160673 (W 0.00688878) | 🔵 tlinalg-pool 13.32× faster than `lapack-openblas` |  |
| `triangular_solve/n32/b1024` | 0.156081 ± 0.00130462 (W 0.0026426) | 1.48533 ± 0.0149578 (W 0.00734032) | 🔵 tlinalg-pool 9.52× faster than `lapack-openblas` |  |
| `triangular_solve/n4/b1024` | 0.014071 ± 0.000190153 (W 0.000121812) | 0.735118 ± 0.0189863 (W 0.00455898) | 🔵 tlinalg-pool 52.24× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.030602 ± 5.31507e-05 (W 8.13151e-05) | 0.772568 ± 0.0164557 (W 0.00420412) | 🔵 tlinalg-pool 25.25× faster than `lapack-openblas` | `!` between-start range over 5% |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.160689 ± 0.00188141 (W 0.00162297) | 1.58823 ± 0.0313438 (W 0.00761919) | 🔵 tlinalg-pool 9.88× faster than `lapack-openblas` |  |
| `cholesky/n32/b1024` | 0.78486 ± 0.00494302 (W 0.00733901) | 6.35871 ± 0.0996449 (W 0.00490917) | 🔵 tlinalg-pool 8.10× faster than `lapack-openblas` |  |
| `cholesky/n4/b1024` | 0.027501 ± 0.000347904 (W 8.9714e-05) | 0.231045 ± 0.00213394 (W 0.00171297) | 🔵 tlinalg-pool 8.40× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.055588 ± 0.00116838 (W 0.000949629) | 0.48619 ± 0.00302037 (W 0.00242742) | 🔵 tlinalg-pool 8.75× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 16.3969 ± 0.349549 (W 0.0171989) | 197.82 ± 0.0769561 (W 0.201359) | 🔵 tlinalg-pool 12.06× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 67.7636 ± 0.147126 (W 0.0388946) | 883.093 ± 1.5351 (W 1.08594) | 🔵 tlinalg-pool 13.03× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 1.38128 ± 0.00423915 (W 0.00309234) | 13.1673 ± 0.0354184 (W 0.0274006) | 🔵 tlinalg-pool 9.53× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 4.54039 ± 0.0135243 (W 0.00558695) | 46.4268 ± 0.0491098 (W 0.0600997) | 🔵 tlinalg-pool 10.23× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 4.02055 ± 0.0114126 (W 0.0040322) | 45.1157 ± 0.454711 (W 0.0540441) | 🔵 tlinalg-pool 11.22× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 17.4792 ± 0.0414343 (W 0.0228631) | 187.358 ± 0.572993 (W 0.284977) | 🔵 tlinalg-pool 10.72× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 0.383474 ± 0.0442822 (W 0.00232865) | 3.58711 ± 0.0324582 (W 0.00849797) | 🔵 tlinalg-pool 9.35× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigh/n8/b1024` | 1.17027 ± 0.0039555 (W 0.00269508) | 12.3393 ± 0.0309796 (W 0.0644629) | 🔵 tlinalg-pool 10.54× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 9.81379 ± 0.017648 (W 0.00953743) | 148.852 ± 0.414717 (W 0.363799) | 🔵 tlinalg-pool 15.17× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 42.8743 ± 0.156964 (W 0.0536737) | 598.573 ± 0.581914 (W 1.07498) | 🔵 tlinalg-pool 13.96× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.699661 ± 0.0105925 (W 0.00195787) | 9.99901 ± 0.0254753 (W 0.0165925) | 🔵 tlinalg-pool 14.29× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 2.57689 ± 0.00520271 (W 0.00576813) | 36.889 ± 0.100778 (W 0.0565401) | 🔵 tlinalg-pool 14.32× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 3.00803 ± 0.0105938 (W 0.00516192) | 19.3136 ± 0.101428 (W 0.0297775) | 🔵 tlinalg-pool 6.42× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 11.4887 ± 0.0271817 (W 0.0119664) | 73.089 ± 0.12493 (W 0.0903968) | 🔵 tlinalg-pool 6.36× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.317235 ± 0.00150103 (W 0.00243104) | 2.12033 ± 0.0122749 (W 0.00464376) | 🔵 tlinalg-pool 6.68× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.943645 ± 0.00386508 (W 0.00183365) | 6.1512 ± 0.0449459 (W 0.0117119) | 🔵 tlinalg-pool 6.52× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.700829 ± 0.00313489 (W 0.00750748) | 33.4326 ± 0.108955 (W 0.0617606) | 🔵 tlinalg-pool 47.70× faster than `lapack-openblas` |  |
| `full_piv_lu/n32/b1024` | 3.07824 ± 0.00410323 (W 0.0169878) | 201.953 ± 1.38674 (W 0.372077) | 🔵 tlinalg-pool 65.61× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1024` | 0.0869215 ± 0.00173636 (W 0.000422591) | 0.90576 ± 0.00796432 (W 0.00450092) | 🔵 tlinalg-pool 10.42× faster than `lapack-openblas` |  |
| `full_piv_lu/n8/b1024` | 0.212269 ± 0.00230633 (W 0.00218652) | 3.8941 ± 0.0396653 (W 0.00713108) | 🔵 tlinalg-pool 18.35× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n16/b1024` | 0.806035 ± 0.00210442 (W 0.00243409) | 37.8139 ± 0.063112 (W 0.0418501) | 🔵 tlinalg-pool 46.91× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 2.76946 ± 0.0259281 (W 0.00464604) | 210.806 ± 1.88194 (W 0.335146) | 🔵 tlinalg-pool 76.12× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.117453 ± 0.00366235 (W 0.00204676) | 2.12387 ± 0.0191178 (W 0.00490324) | 🔵 tlinalg-pool 18.08× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.289569 ± 0.00133924 (W 0.00256564) | 6.13753 ± 0.0653911 (W 0.0145885) | 🔵 tlinalg-pool 21.20× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.63951 ± 0.0111329 (W 0.0026931) | 7.22772 ± 0.11158 (W 0.0218489) | 🔵 tlinalg-pool 11.30× faster than `lapack-openblas` |  |
| `householder_apply/n32/b1024` | 3.60765 ± 0.0318424 (W 0.0127331) | 35.4282 ± 0.465436 (W 0.0338368) | 🔵 tlinalg-pool 9.82× faster than `lapack-openblas` |  |
| `householder_apply/n4/b1024` | 0.053309 ± 0.00132936 (W 0.000114444) | 0.429094 ± 0.00975724 (W 0.00328041) | 🔵 tlinalg-pool 8.05× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.153325 ± 0.00228798 (W 0.00124284) | 1.47648 ± 0.0049226 (W 0.00447764) | 🔵 tlinalg-pool 9.63× faster than `lapack-openblas` |  |
| `householder_factor/n16/b1024` | 0.608993 ± 0.012343 (W 0.00314498) | 7.29599 ± 0.0477499 (W 0.010567) | 🔵 tlinalg-pool 11.98× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 2.56734 ± 0.0309721 (W 0.00755429) | 27.074 ± 0.0653404 (W 0.0236051) | 🔵 tlinalg-pool 10.55× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.078676 ± 0.000490205 (W 0.00020572) | 0.918503 ± 0.00137111 (W 0.00189534) | 🔵 tlinalg-pool 11.67× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.203483 ± 0.000794136 (W 0.000940411) | 2.35351 ± 0.00375026 (W 0.00513506) | 🔵 tlinalg-pool 11.57× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.457035 ± 0.00797147 (W 0.00612218) | 3.92996 ± 0.0671419 (W 0.0207765) | 🔵 tlinalg-pool 8.60× faster than `lapack-openblas` |  |
| `lu/n32/b1024` | 2.19373 ± 0.00452554 (W 0.00817517) | 15.2981 ± 0.103955 (W 0.0258574) | 🔵 tlinalg-pool 6.97× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.0637695 ± 0.00141628 (W 0.000893696) | 0.381315 ± 0.00766383 (W 0.00278733) | 🔵 tlinalg-pool 5.98× faster than `lapack-openblas` |  |
| `lu/n8/b1024` | 0.140917 ± 0.00634853 (W 0.00310214) | 1.03682 ± 0.0192627 (W 0.00283262) | 🔵 tlinalg-pool 7.36× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.289834 ± 0.00465619 (W 0.00204481) | 2.66905 ± 0.0144312 (W 0.00581353) | 🔵 tlinalg-pool 9.21× faster than `lapack-openblas` |  |
| `lu_factor/n32/b1024` | 1.24737 ± 0.00447897 (W 0.00393761) | 11.1986 ± 0.126257 (W 0.0187559) | 🔵 tlinalg-pool 8.98× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.0611535 ± 0.00047747 (W 0.00117576) | 0.271771 ± 0.00192051 (W 0.00211918) | 🔵 tlinalg-pool 4.44× faster than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.104615 ± 0.0152314 (W 0.00130521) | 0.758456 ± 0.0026601 (W 0.00323777) | 🔵 tlinalg-pool 7.25× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor_solve/n16/b1024` | 0.455883 ± 0.00337944 (W 0.00304981) | 5.01738 ± 0.0327721 (W 0.00652142) | 🔵 tlinalg-pool 11.01× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 1.70475 ± 0.0042293 (W 0.0048414) | 15.4011 ± 0.115169 (W 0.028692) | 🔵 tlinalg-pool 9.03× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.073276 ± 0.000574751 (W 0.00131515) | 1.07681 ± 0.00557969 (W 0.00467598) | 🔵 tlinalg-pool 14.70× faster than `lapack-openblas` |  |
| `lu_factor_solve/n8/b1024` | 0.160774 ± 0.00169977 (W 0.00137583) | 2.29292 ± 0.0279084 (W 0.00581529) | 🔵 tlinalg-pool 14.26× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1024` | 0.184012 ± 0.000735794 (W 0.00206026) | 1.93128 ± 0.0236515 (W 0.00471642) | 🔵 tlinalg-pool 10.50× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n32/b1024` | 0.874012 ± 0.00214872 (W 0.00649931) | 4.00515 ± 0.0179189 (W 0.00540692) | 🔵 tlinalg-pool 4.58× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n4/b1024` | 0.033668 ± 0.000225788 (W 0.000301603) | 0.7361 ± 0.0186906 (W 0.00704421) | 🔵 tlinalg-pool 21.86× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n8/b1024` | 0.076217 ± 0.0011313 (W 0.00182815) | 1.32611 ± 0.0168007 (W 0.00330926) | 🔵 tlinalg-pool 17.40× faster than `lapack-openblas` |  |
| `qr/n16/b1024` | 1.40462 ± 0.00556473 (W 0.00368506) | 12.6401 ± 0.0234924 (W 0.0168575) | 🔵 tlinalg-pool 9.00× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 9.05504 ± 0.0365279 (W 0.0185405) | 49.458 ± 0.237282 (W 0.0356266) | 🔵 tlinalg-pool 5.46× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.120378 ± 0.000573238 (W 0.000770952) | 1.40747 ± 0.00885606 (W 0.00524931) | 🔵 tlinalg-pool 11.69× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 0.346975 ± 0.000465563 (W 0.00204637) | 3.79722 ± 0.0105539 (W 0.00435239) | 🔵 tlinalg-pool 10.94× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.59296 ± 0.0142649 (W 0.00231578) | 16.7555 ± 0.0362332 (W 0.0345411) | 🔵 tlinalg-pool 10.52× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 8.52654 ± 0.051139 (W 0.0250528) | 65.8161 ± 0.358947 (W 0.0640541) | 🔵 tlinalg-pool 7.72× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 0.194306 ± 0.00156737 (W 0.00160763) | 1.82556 ± 0.00335972 (W 0.00543934) | 🔵 tlinalg-pool 9.40× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.493423 ± 0.00178504 (W 0.00250762) | 4.98043 ± 0.0198686 (W 0.00478025) | 🔵 tlinalg-pool 10.09× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.492472 ± 0.00228518 (W 0.00230326) | 5.14998 ± 0.0662704 (W 0.0136879) | 🔵 tlinalg-pool 10.46× faster than `lapack-openblas` |  |
| `solve/n32/b1024` | 1.84405 ± 0.00723695 (W 0.00482996) | 16.1543 ± 0.0726243 (W 0.0167441) | 🔵 tlinalg-pool 8.76× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.075446 ± 0.000143371 (W 0.000833452) | 1.47909 ± 0.0274797 (W 0.004279) | 🔵 tlinalg-pool 19.60× faster than `lapack-openblas` |  |
| `solve/n8/b1024` | 0.177129 ± 0.00132627 (W 0.0021959) | 2.35249 ± 0.0127745 (W 0.00789873) | 🔵 tlinalg-pool 13.28× faster than `lapack-openblas` |  |
| `svd_full/n16/b1024` | 7.44952 ± 0.181621 (W 0.0116551) | 93.0026 ± 0.190989 (W 0.0963685) | 🔵 tlinalg-pool 12.48× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 31.2472 ± 0.223751 (W 0.0107614) | 295.389 ± 0.588689 (W 0.441026) | 🔵 tlinalg-pool 9.45× faster than `lapack-openblas` |  |
| `svd_full/n4/b1024` | 0.660789 ± 0.0100079 (W 0.00275058) | 7.87154 ± 0.0426082 (W 0.0161405) | 🔵 tlinalg-pool 11.91× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 2.08724 ± 0.0118329 (W 0.00305408) | 24.7155 ± 0.0470575 (W 0.0285754) | 🔵 tlinalg-pool 11.84× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 7.43756 ± 0.171243 (W 0.00559561) | 93.0926 ± 0.631051 (W 0.0853653) | 🔵 tlinalg-pool 12.52× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 31.3099 ± 0.262756 (W 0.13739) | 295.556 ± 0.844013 (W 0.50005) | 🔵 tlinalg-pool 9.44× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1024` | 0.658065 ± 0.0169751 (W 0.00170138) | 7.86273 ± 0.0189491 (W 0.0170789) | 🔵 tlinalg-pool 11.95× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 2.11665 ± 0.0350956 (W 0.00216397) | 24.7676 ± 0.0720465 (W 0.0266743) | 🔵 tlinalg-pool 11.70× faster than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 3.19388 ± 0.00974972 (W 0.00553711) | 33.1917 ± 0.0713071 (W 0.0684885) | 🔵 tlinalg-pool 10.39× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 11.3575 ± 0.0370766 (W 0.015555) | 109.819 ± 0.534382 (W 0.0623373) | 🔵 tlinalg-pool 9.67× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.435841 ± 0.00344197 (W 0.00245641) | 4.63194 ± 0.0208303 (W 0.00939057) | 🔵 tlinalg-pool 10.63× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.13971 ± 0.00330685 (W 0.00221299) | 11.1942 ± 0.0171339 (W 0.00897477) | 🔵 tlinalg-pool 9.82× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.129196 ± 0.0007989 (W 0.00179128) | 1.37865 ± 0.00838472 (W 0.00659808) | 🔵 tlinalg-pool 10.67× faster than `lapack-openblas` |  |
| `triangular_solve/n32/b1024` | 0.533623 ± 0.00342083 (W 0.00398525) | 3.00396 ± 0.0294461 (W 0.00620543) | 🔵 tlinalg-pool 5.63× faster than `lapack-openblas` |  |
| `triangular_solve/n4/b1024` | 0.025398 ± 7.98138e-05 (W 8.40644e-05) | 0.79263 ± 0.0307544 (W 0.00584708) | 🔵 tlinalg-pool 31.21× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.05654 ± 0.000347036 (W 0.000430326) | 0.90313 ± 0.0112842 (W 0.00573974) | 🔵 tlinalg-pool 15.97× faster than `lapack-openblas` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0664735 ± 0.00211063 (W 0.000639019) | 0.0733565 ± 0.00132397 (W 0.000647384) | 🔵 tlinalg-pool 1.10× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n128/b1` | 0.170738 ± 0.000908846 (W 0.0017531) | 0.144444 ± 0.000550193 (W 0.00187921) | 🔴 tlinalg-pool 1.18× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.091861 ± 0.000422888 (W 0.000326946) | 0.129727 ± 0.000704752 (W 0.00172507) | 🔵 tlinalg-pool 1.41× faster than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.101724 ± 0.000873432 (W 0.000343323) | 0.145146 ± 0.000849314 (W 0.00318935) | 🔵 tlinalg-pool 1.43× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.011221 ± 5.59762e-05 (W 6.60181e-05) | 0.011892 ± 0.00020106 (W 7.75677e-05) | 🔵 tlinalg-pool 1.06× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.116957 ± 0.000510331 (W 0.00156748) | 0.152865 ± 0.000573906 (W 0.00174966) | 🔵 tlinalg-pool 1.31× faster than `lapack-openblas` |  |
| `svd_values/n128/b1` | 1.14037 ± 0.00493375 (W 0.00269769) | 1.37914 ± 0.00483736 (W 0.00253546) | 🔵 tlinalg-pool 1.21× faster than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.0079745 ± 2.65251e-05 (W 5.40854e-05) | 0.006783 ± 6.8313e-05 (W 7.80043e-05) | 🔴 tlinalg-pool 1.18× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.154137 ± 0.00122165 (W 0.00138894) | 0.149443 ± 0.00159496 (W 0.00107747) | · |  |
| `lu/n128/b1` | 0.313439 ± 0.00501625 (W 0.00231231) | 0.235444 ± 0.000872048 (W 0.00315335) | 🔴 tlinalg-pool 1.33× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.224072 ± 0.00124189 (W 0.00214237) | 0.189478 ± 0.000509769 (W 0.00233279) | 🔴 tlinalg-pool 1.18× slower than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.258131 ± 0.000767386 (W 0.00192583) | 0.224473 ± 0.00202315 (W 0.0033855) | 🔴 tlinalg-pool 1.15× slower than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.033076 ± 0.000337092 (W 0.000208141) | 0.030046 ± 0.000136961 (W 0.000207664) | 🔴 tlinalg-pool 1.10× slower than `lapack-openblas` |  |
| `solve/n128/b1` | 0.278794 ± 0.00140371 (W 0.00229064) | 0.233664 ± 0.00128149 (W 0.00235895) | 🔴 tlinalg-pool 1.19× slower than `lapack-openblas` |  |
| `svd_values/n128/b1` | 1.44346 ± 0.00487465 (W 0.00210279) | 2.58141 ± 0.00363571 (W 0.00509749) | 🔵 tlinalg-pool 1.79× faster than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.020133 ± 0.000200469 (W 9.37723e-05) | 0.015203 ± 0.000213839 (W 0.000155613) | 🔴 tlinalg-pool 1.32× slower than `lapack-openblas` |  |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 27.3372 ± 0.0159234 (W 0.0377993) | 23.5485 ± 0.0718655 (W 0.0300803) | 🔴 tlinalg-pool 1.16× slower than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 16.1595 ± 0.0392268 (W 0.0130052) | 11.3856 ± 0.0335097 (W 0.00846395) | 🔴 tlinalg-pool 1.42× slower than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 1.54412 ± 0.00488168 (W 0.00552712) | 9.81124 ± 0.104357 (W 0.0187334) | 🔵 tlinalg-pool 6.35× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 1.84411 ± 0.00210025 (W 0.00487051) | 6.74195 ± 0.0426875 (W 0.0158164) | 🔵 tlinalg-pool 3.66× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 5.4475 ± 0.00607166 (W 0.0142791) | 13.4573 ± 0.0181599 (W 0.0199295) | 🔵 tlinalg-pool 2.47× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 7.21812 ± 0.0326013 (W 0.0173359) | 22.8272 ± 0.188955 (W 0.0726169) | 🔵 tlinalg-pool 3.16× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 38.784 ± 0.0619981 (W 0.0361203) | 85.0589 ± 0.55687 (W 0.320688) | 🔵 tlinalg-pool 2.19× faster than `lapack-openblas` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 37.062 ± 0.0488983 (W 0.0330177) | 203.369 ± 0.760552 (W 0.361449) | 🔵 tlinalg-pool 5.49× faster than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 20.4821 ± 0.0277586 (W 0.0572832) | 29.7354 ± 0.0564355 (W 0.0266557) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 5.60107 ± 0.0196962 (W 0.0178437) | 14.0976 ± 0.0526681 (W 0.0201019) | 🔵 tlinalg-pool 2.52× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 5.14598 ± 0.00667667 (W 0.00706174) | 10.7609 ± 0.0535306 (W 0.0165432) | 🔵 tlinalg-pool 2.09× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 13.2619 ± 0.0383369 (W 0.024294) | 21.7735 ± 0.0502535 (W 0.0373275) | 🔵 tlinalg-pool 1.64× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 14.1728 ± 0.0390977 (W 0.023974) | 24.2835 ± 0.0527343 (W 0.0434069) | 🔵 tlinalg-pool 1.71× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 75.0243 ± 0.145631 (W 0.0704848) | 99.9531 ± 0.382807 (W 0.123141) | 🔵 tlinalg-pool 1.33× faster than `lapack-openblas` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 5.89798 ± 0.0315977 (W 0.0212631) | 18.118 ± 0.190512 (W 0.0232551) | 🔵 tlinalg-pool 3.07× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 22.227 ± 0.0131073 (W 0.049254) | 35.7087 ± 0.240038 (W 0.0514674) | 🔵 tlinalg-pool 1.61× faster than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 21.473 ± 0.0981155 (W 0.0545331) | 39.0642 ± 0.244176 (W 0.0485633) | 🔵 tlinalg-pool 1.82× faster than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 35.204 ± 0.0165581 (W 0.0744875) | 61.0225 ± 0.602411 (W 0.0671557) | 🔵 tlinalg-pool 1.73× faster than `lapack-openblas` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 17.3176 ± 0.0583264 (W 0.0358997) | 20.0668 ± 0.127145 (W 0.0260202) | 🔵 tlinalg-pool 1.16× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 58.5534 ± 0.164275 (W 0.0816382) | 40.1753 ± 0.201298 (W 0.0338573) | 🔴 tlinalg-pool 1.46× slower than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 59.416 ± 0.3573 (W 0.184984) | 51.113 ± 0.117339 (W 0.0970257) | 🔴 tlinalg-pool 1.16× slower than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 109.106 ± 0.255096 (W 0.201968) | 85.6235 ± 0.410867 (W 0.0894872) | 🔴 tlinalg-pool 1.27× slower than `lapack-openblas` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
