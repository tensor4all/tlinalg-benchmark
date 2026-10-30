# `tlinalg-scaling` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `3957b5af620eff5da5d1435afd97a4a8619ba473`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `028b45886580e5353ddee46798f3d2cd7cf52f7521251264812b3a908590da86`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-30T17:29:57.759463Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-scaling --aa 4 --reps 5 --prime-ms 250 --label weekly-20261030-scaling --no-publish`
- raw data: `data/results/zen5-cpu/tlinalg-scaling/20261030T170916Z-weekly-20261030-scaling/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: The scaling table declares 8T only. The pool has nothing to parallelise at 1T (it is one lane with extra machinery), and a 1T verify pass is the slowest single thing this host runs: measured 2026-10-20, one 1T population took over twenty minutes. The baseline the table needs is the one lane *on the same budget*.
  Known blind spot: The batched regime stops at n=32 by choice: batch 1024 is the regime this campaign is about, and the four shapes up to 32 already separate the rows by four to nine times, so larger matrices would add cells without changing the answer. Above that size faer-benchmark measures the same backends. (Recorded while the grid still held 64: one verify pass at n=64 ran past 45 minutes because the harness recomputes every case, which made the last shape cost far more than it added.)
  Known blind spot: Only the kernel entry points are measured. Tensor construction, dtype dispatch, session entry and pool checkout are tenferro's and are out of scope.
  Known blind spot: The 2026-10-17 trim narrowed the suite to the batched small regime plus three single-shape canaries (factor at 128, decompose at 512, rectangular at 4096x256, each at batch 1). The medium, large and tall grids are no longer measured here: faer-benchmark measures that geometry directly with the same backends these rows wrap, so a cost that appears only at those sizes has to be read from that campaign's page.
  Known blind spot: The small regime declares batch 1 and 1024 and gives up the middle of the axis, so a cost that appears only at an intermediate batch is not covered.
  Known blind spot: The thread axis is 1T and 8T; a budget between them (4T) is not measured, so a scaling curve cannot be read off this page.
  Known blind spot: The providers are compared at the thread budgets declared here; a budget the vendor threads itself by, outside that set, is not covered.
  Known blind spot: A vendor arm records the vendor library, but only OpenBLAS reports the kernel its runtime dispatched to. MKL's manifest records its own version and the threading layer the harness pins; it names no kernel, because MKL exposes none to name.
  Known blind spot: The batched regime measures batch 1024 only: batch 1 has nothing to parallelise, so it measures dispatch rather than the library, and the canaries carry the single-call sizes. An intermediate batch is therefore not covered.
- **Rows** — one row per engine in every table below:
  - `faer-1lane` — The faer-backed provider on one sequential lane: the per-item cost plus the batch loop, with no threading at all. The overhead baseline.
    Identity: tlinalg-rs (this repository's pinned revision)
    As measured: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.47%, worst 12.23% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 33 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.33%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
The `vs tlinalg-1lane` column is the rotation-averaged ratio
exp(mean over starts of log(engine median / tlinalg-1lane median)),
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

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.902384 ± 0.0153265 (W 0.00801155) | 0.113937 ± 0.00250585 (W 0.00152634) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 3.42156 ± 0.211321 (W 0.0361667) | 0.478883 ± 0.00803842 (W 0.0068679) | 🔴 tlinalg-1lane 7.14× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.17945 ± 0.000497645 (W 0.00180704) | 0.180897 ± 0.000851214 (W 0.00220873) | · |  |
| `cholesky/n8/b1024` | 0.359716 ± 0.00598478 (W 0.00258069) | 0.047068 ± 0.000156046 (W 8.52523e-05) | 🔴 tlinalg-1lane 7.64× slower than `tlinalg-pool` |  |
| `eig/n16/b1024` | 96.5376 ± 0.1145 (W 0.248103) | 12.0905 ± 0.168006 (W 0.0227335) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 432.529 ± 0.516554 (W 2.2059) | 54.1571 ± 1.9108 (W 0.0395662) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eig/n4/b1024` | 6.43037 ± 0.00801367 (W 0.0118576) | 0.808403 ± 0.00603379 (W 0.00256229) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `eig/n8/b1024` | 24.1353 ± 0.0763648 (W 0.0232998) | 3.02451 ± 0.00542953 (W 0.00808194) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eigh/n16/b1024` | 29.899 ± 0.111543 (W 0.0206256) | 3.77557 ± 0.0126683 (W 0.0046691) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 111.844 ± 0.378455 (W 0.208133) | 13.972 ± 0.0212311 (W 0.0137524) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.53137 ± 0.0131999 (W 0.00444856) | 0.3218 ± 0.000985132 (W 0.00193635) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 8.65572 ± 0.0610217 (W 0.0107511) | 1.09761 ± 0.00388483 (W 0.00340843) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `eigvals/n16/b1024` | 66.8963 ± 0.13198 (W 0.0628892) | 8.39185 ± 0.023665 (W 0.00425791) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 292.806 ± 0.911845 (W 0.291223) | 36.7517 ± 0.0718811 (W 0.0809812) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 3.42875 ± 0.00399728 (W 0.00885316) | 0.437976 ± 0.00136991 (W 0.00176863) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 15.827 ± 0.027431 (W 0.0336313) | 1.99309 ± 0.00611936 (W 0.00443388) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 22.7412 ± 0.0782363 (W 0.0208655) | 2.86792 ± 0.00650155 (W 0.00420212) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 85.4957 ± 0.162435 (W 0.0728236) | 10.6958 ± 0.0301375 (W 0.0102539) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.08414 ± 0.00110758 (W 0.00291151) | 0.264363 ± 0.00105841 (W 0.00209053) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 6.98449 ± 0.0168948 (W 0.0104972) | 0.885391 ± 0.00281411 (W 0.00243525) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 3.83764 ± 0.0559924 (W 0.0123164) | 0.512486 ± 0.00329471 (W 0.003629) | 🔴 tlinalg-1lane 7.49× slower than `tlinalg-pool` |  |
| `full_piv_lu/n32/b1024` | 14.9486 ± 0.0941562 (W 0.0327998) | 2.03706 ± 0.0166721 (W 0.0108074) | 🔴 tlinalg-1lane 7.34× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.491011 ± 0.00109909 (W 0.00315997) | 0.492113 ± 0.00415648 (W 0.00318335) | · |  |
| `full_piv_lu/n8/b1024` | 1.30942 ± 0.0222844 (W 0.00920528) | 0.180482 ± 0.00244618 (W 0.00204177) | 🔴 tlinalg-1lane 7.26× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n16/b1024` | 3.97993 ± 0.00652858 (W 0.0137238) | 0.513503 ± 0.0099328 (W 0.00317671) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 12.5492 ± 0.211949 (W 0.0533426) | 1.62979 ± 0.0231377 (W 0.0136193) | 🔴 tlinalg-1lane 7.70× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.646315 ± 0.00233317 (W 0.00500643) | 0.084202 ± 0.00066501 (W 0.00141822) | 🔴 tlinalg-1lane 7.68× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n8/b1024` | 1.59435 ± 0.023689 (W 0.0121161) | 0.207522 ± 0.00187355 (W 0.00188141) | 🔴 tlinalg-1lane 7.68× slower than `tlinalg-pool` |  |
| `householder_apply/n16/b1024` | 4.81438 ± 0.104487 (W 0.0109388) | 0.599558 ± 0.0116396 (W 0.00305228) | 🔴 tlinalg-1lane 8.03× slower than `tlinalg-pool` |  |
| `householder_apply/n32/b1024` | 19.5387 ± 0.198695 (W 0.0463418) | 2.42013 ± 0.0266143 (W 0.0103628) | 🔴 tlinalg-1lane 8.07× slower than `tlinalg-pool` |  |
| `householder_apply/n4/b1024` | 0.384547 ± 0.01157 (W 0.00216183) | 0.053565 ± 0.00206446 (W 0.000801433) | 🔴 tlinalg-1lane 7.18× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.25645 ± 0.0391074 (W 0.00301934) | 0.169131 ± 0.00695406 (W 0.00146253) | 🔴 tlinalg-1lane 7.43× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 4.02587 ± 0.131342 (W 0.0043748) | 0.508328 ± 0.00931806 (W 0.00249646) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n32/b1024` | 13.3144 ± 0.251915 (W 0.0437788) | 1.68116 ± 0.0272542 (W 0.00216953) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.492844 ± 0.0111695 (W 0.00214716) | 0.064245 ± 0.000372442 (W 0.000150598) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.32063 ± 0.0691556 (W 0.00217804) | 0.16932 ± 0.00453551 (W 0.0015426) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n16/b1024` | 2.91168 ± 0.0937689 (W 0.0141914) | 0.376872 ± 0.00472214 (W 0.00272079) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n32/b1024` | 10.3999 ± 0.0704322 (W 0.0282471) | 1.35781 ± 0.015295 (W 0.0147531) | 🔴 tlinalg-1lane 7.66× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.306587 ± 0.00350276 (W 0.00245528) | 0.309323 ± 0.00240863 (W 0.00390696) | · |  |
| `lu/n8/b1024` | 0.855355 ± 0.018244 (W 0.00793419) | 0.133388 ± 0.00269624 (W 0.0013657) | 🔴 tlinalg-1lane 6.41× slower than `tlinalg-pool` |  |
| `lu_factor/n16/b1024` | 1.92766 ± 0.0405819 (W 0.00698686) | 0.253001 ± 0.00110572 (W 0.00140937) | 🔴 tlinalg-1lane 7.62× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 5.67943 ± 0.0493686 (W 0.0206309) | 0.721957 ± 0.00907533 (W 0.00404103) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `lu_factor/n4/b1024` | 0.232648 ± 0.00514083 (W 0.00278731) | 0.238029 ± 0.000852298 (W 0.0014586) | · |  |
| `lu_factor/n8/b1024` | 0.619044 ± 0.00564679 (W 0.00954686) | 0.097427 ± 0.0019427 (W 0.00170958) | 🔴 tlinalg-1lane 6.35× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 2.48262 ± 0.0264797 (W 0.01278) | 0.320122 ± 0.00203813 (W 0.00238444) | 🔴 tlinalg-1lane 7.76× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 7.02173 ± 0.0762492 (W 0.019564) | 0.890945 ± 0.0047368 (W 0.00510159) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n4/b1024` | 0.304814 ± 0.00543031 (W 0.00244837) | 0.056776 ± 0.00035311 (W 0.000830305) | 🔴 tlinalg-1lane 5.37× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n8/b1024` | 0.825039 ± 0.00732114 (W 0.00858674) | 0.118681 ± 0.00212447 (W 0.00225909) | 🔴 tlinalg-1lane 6.95× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 0.619801 ± 0.0056053 (W 0.00290463) | 0.096881 ± 0.000214407 (W 0.00159049) | 🔴 tlinalg-1lane 6.40× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 2.33512 ± 0.0243297 (W 0.0138921) | 0.231917 ± 0.00117261 (W 0.00182936) | 🔴 tlinalg-1lane 10.07× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n4/b1024` | 0.0730915 ± 0.000386422 (W 0.000122992) | 0.020869 ± 0.000285214 (W 9.28088e-05) | 🔴 tlinalg-1lane 3.50× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n8/b1024` | 0.237939 ± 0.000574019 (W 0.00242869) | 0.043812 ± 0.000198746 (W 0.000151684) | 🔴 tlinalg-1lane 5.43× slower than `tlinalg-pool` |  |
| `qr/n16/b1024` | 9.19985 ± 0.184536 (W 0.0107575) | 1.13797 ± 0.0244253 (W 0.00118937) | 🔴 tlinalg-1lane 8.08× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `qr/n32/b1024` | 33.4442 ± 0.158976 (W 0.0220607) | 4.221 ± 0.0332666 (W 0.0199697) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.771945 ± 0.0130399 (W 0.00451004) | 0.09915 ± 0.00160756 (W 0.00163745) | 🔴 tlinalg-1lane 7.79× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.45301 ± 0.052866 (W 0.00678721) | 0.308165 ± 0.00519348 (W 0.00160374) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 10.6959 ± 0.188869 (W 0.00536389) | 1.34482 ± 0.0225945 (W 0.00314711) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 34.5151 ± 0.231895 (W 0.0319399) | 4.37317 ± 0.180756 (W 0.0104325) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `rank_revealing_qr/n4/b1024` | 1.33543 ± 0.010546 (W 0.00373108) | 0.172973 ± 0.00187619 (W 0.00150663) | 🔴 tlinalg-1lane 7.72× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n8/b1024` | 3.44679 ± 0.0436223 (W 0.00387334) | 0.437922 ± 0.00602575 (W 0.00204783) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `solve/n16/b1024` | 2.79202 ± 0.0382665 (W 0.0107433) | 0.35958 ± 0.0054799 (W 0.00332571) | 🔴 tlinalg-1lane 7.76× slower than `tlinalg-pool` |  |
| `solve/n32/b1024` | 7.63117 ± 0.0575263 (W 0.022687) | 0.960636 ± 0.00757387 (W 0.00659989) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.389767 ± 0.00639693 (W 0.0030989) | 0.0517265 ± 0.000405876 (W 0.000302094) | 🔴 tlinalg-1lane 7.54× slower than `tlinalg-pool` |  |
| `solve/n8/b1024` | 0.946441 ± 0.0142771 (W 0.0053938) | 0.125995 ± 0.00102576 (W 0.00139764) | 🔴 tlinalg-1lane 7.51× slower than `tlinalg-pool` |  |
| `svd_full/n16/b1024` | 53.3214 ± 0.224491 (W 0.0428908) | 6.70758 ± 0.0305986 (W 0.00602996) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 187.22 ± 0.365617 (W 0.249815) | 23.6582 ± 0.208441 (W 0.0632412) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `svd_full/n4/b1024` | 4.37678 ± 0.0199592 (W 0.00428202) | 0.553817 ± 0.00657548 (W 0.00238686) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 14.814 ± 0.0353123 (W 0.0217299) | 1.88662 ± 0.105597 (W 0.00496218) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 53.2355 ± 0.245711 (W 0.0206958) | 6.71849 ± 0.0244029 (W 0.00973378) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `svd_thin/n32/b1024` | 187.715 ± 0.230956 (W 0.288665) | 23.6543 ± 0.254877 (W 0.0309613) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `svd_thin/n4/b1024` | 4.34786 ± 0.0168333 (W 0.0084567) | 0.551599 ± 0.00312504 (W 0.00245369) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `svd_thin/n8/b1024` | 14.8232 ± 0.0401216 (W 0.0168895) | 1.88513 ± 0.097065 (W 0.0049939) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 22.0708 ± 0.119525 (W 0.0397513) | 2.80084 ± 0.0118814 (W 0.00411187) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 74.5745 ± 0.119 (W 0.0782662) | 9.46111 ± 0.0394444 (W 0.0122162) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 2.88325 ± 0.0164781 (W 0.0057084) | 0.365853 ± 0.00265552 (W 0.00216323) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 7.89079 ± 0.0221014 (W 0.00729769) | 1.00894 ± 0.00400215 (W 0.000900644) | 🔴 tlinalg-1lane 7.82× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 0.522564 ± 0.00360103 (W 0.00310888) | 0.0677015 ± 0.00043889 (W 0.000302616) | 🔴 tlinalg-1lane 7.72× slower than `tlinalg-pool` |  |
| `triangular_solve/n32/b1024` | 1.34229 ± 0.0221715 (W 0.0196212) | 0.157644 ± 0.0006598 (W 0.00228672) | 🔴 tlinalg-1lane 8.51× slower than `tlinalg-pool` |  |
| `triangular_solve/n4/b1024` | 0.094356 ± 0.00012728 (W 0.00185768) | 0.0143165 ± 0.000339642 (W 0.000213667) | 🔴 tlinalg-1lane 6.59× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.225891 ± 0.000677691 (W 0.00206768) | 0.030752 ± 0.000112953 (W 0.000127918) | 🔴 tlinalg-1lane 7.35× slower than `tlinalg-pool` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 1.27764 ± 0.0258774 (W 0.00445863) | 0.159362 ± 0.00281229 (W 0.00252838) | 🔴 tlinalg-1lane 8.02× slower than `tlinalg-pool` |  |
| `cholesky/n32/b1024` | 5.6866 ± 0.0412759 (W 0.0111003) | 0.789473 ± 0.00486072 (W 0.00658201) | 🔴 tlinalg-1lane 7.20× slower than `tlinalg-pool` |  |
| `cholesky/n4/b1024` | 0.198039 ± 0.000841763 (W 0.00141732) | 0.0273565 ± 0.000308433 (W 8.3659e-05) | 🔴 tlinalg-1lane 7.24× slower than `tlinalg-pool` |  |
| `cholesky/n8/b1024` | 0.415731 ± 0.00185587 (W 0.00326136) | 0.0541865 ± 0.00109446 (W 0.000128467) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` |  |
| `eig/n16/b1024` | 130.895 ± 0.199216 (W 0.253512) | 16.7821 ± 0.246141 (W 0.0156467) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 541.815 ± 0.781207 (W 0.608157) | 67.7365 ± 0.140666 (W 0.236494) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 10.8428 ± 0.0958056 (W 0.0128137) | 1.37308 ± 0.0107349 (W 0.00248995) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `eig/n8/b1024` | 35.9997 ± 2.15893 (W 0.0441422) | 4.56296 ± 0.00617789 (W 0.00605661) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigh/n16/b1024` | 32.238 ± 0.130756 (W 0.0940543) | 4.0157 ± 0.00820014 (W 0.00766081) | 🔴 tlinalg-1lane 8.03× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 139.108 ± 0.573879 (W 0.130007) | 17.3974 ± 0.030263 (W 0.0155878) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 3.01361 ± 0.0354816 (W 0.00488215) | 0.384597 ± 0.00384155 (W 0.00179547) | 🔴 tlinalg-1lane 7.84× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 9.30921 ± 0.0843963 (W 0.0132973) | 1.17482 ± 0.00578041 (W 0.00342397) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigvals/n16/b1024` | 78.4608 ± 0.239059 (W 0.0762977) | 9.90826 ± 0.013946 (W 0.0125625) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 341.506 ± 0.393437 (W 0.504441) | 43.1616 ± 0.0707379 (W 0.0276726) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 5.51949 ± 0.0364489 (W 0.00735267) | 0.708892 ± 0.0110968 (W 0.00217626) | 🔴 tlinalg-1lane 7.79× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 20.4907 ± 0.0710106 (W 0.0200301) | 2.61708 ± 0.114576 (W 0.00194407) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigvalsh/n16/b1024` | 24.2597 ± 0.0895255 (W 0.0170393) | 3.04633 ± 0.00458702 (W 0.00303725) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 92.6783 ± 0.501604 (W 0.231884) | 11.579 ± 0.0297502 (W 0.0114328) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.47389 ± 0.0341166 (W 0.00455415) | 0.317111 ± 0.00123076 (W 0.00243017) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 7.53623 ± 0.0479715 (W 0.011259) | 0.955798 ± 0.00283945 (W 0.00130939) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 5.28477 ± 0.13513 (W 0.0294411) | 0.70287 ± 0.0078493 (W 0.00720493) | 🔴 tlinalg-1lane 7.52× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 21.3505 ± 0.296442 (W 0.0324737) | 3.07185 ± 0.0306839 (W 0.0237249) | 🔴 tlinalg-1lane 6.95× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.589715 ± 0.00402185 (W 0.00521555) | 0.090253 ± 0.00387155 (W 0.000434813) | 🔴 tlinalg-1lane 6.53× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 1.52119 ± 0.0538282 (W 0.0109958) | 0.213623 ± 0.0039046 (W 0.00209649) | 🔴 tlinalg-1lane 7.12× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 6.26441 ± 0.0614228 (W 0.0140248) | 0.814133 ± 0.00772437 (W 0.00202211) | 🔴 tlinalg-1lane 7.69× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 21.5301 ± 0.166948 (W 0.0176705) | 2.7707 ± 0.0175036 (W 0.00785694) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.904993 ± 0.00586894 (W 0.00905593) | 0.12027 ± 0.00354555 (W 0.00164682) | 🔴 tlinalg-1lane 7.52× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 2.24595 ± 0.00854274 (W 0.00929615) | 0.28974 ± 0.00243043 (W 0.00208012) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `householder_apply/n16/b1024` | 5.41595 ± 0.136964 (W 0.0140552) | 0.628626 ± 0.00922101 (W 0.00378674) | 🔴 tlinalg-1lane 8.62× slower than `tlinalg-pool` |  |
| `householder_apply/n32/b1024` | 27.9289 ± 0.257602 (W 0.0487612) | 3.52767 ± 0.0412098 (W 0.0125782) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `householder_apply/n4/b1024` | 0.397206 ± 0.0133569 (W 0.00352993) | 0.0517965 ± 0.00212715 (W 0.000241701) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.19537 ± 0.0352772 (W 0.00256751) | 0.150736 ± 0.00450352 (W 0.0019854) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 4.78146 ± 0.035586 (W 0.00985193) | 0.610554 ± 0.00212702 (W 0.00301691) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` |  |
| `householder_factor/n32/b1024` | 20.5199 ± 0.21405 (W 0.0218984) | 2.57972 ± 0.0295108 (W 0.00806146) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.610107 ± 0.0084409 (W 0.00299425) | 0.0791375 ± 0.000317208 (W 0.000834187) | 🔴 tlinalg-1lane 7.71× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.57789 ± 0.0239367 (W 0.00338886) | 0.203981 ± 0.0015032 (W 0.00160081) | 🔴 tlinalg-1lane 7.74× slower than `tlinalg-pool` |  |
| `lu/n16/b1024` | 3.20448 ± 0.0317967 (W 0.0233563) | 0.452243 ± 0.00648791 (W 0.00989352) | 🔴 tlinalg-1lane 7.09× slower than `tlinalg-pool` |  |
| `lu/n32/b1024` | 15.0983 ± 0.152382 (W 0.0436088) | 2.19057 ± 0.0224878 (W 0.00994241) | 🔴 tlinalg-1lane 6.89× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.364024 ± 0.0110996 (W 0.00343431) | 0.0638995 ± 0.000350129 (W 0.000441996) | 🔴 tlinalg-1lane 5.70× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.960797 ± 0.0249779 (W 0.00648943) | 0.137381 ± 0.00126009 (W 0.00319064) | 🔴 tlinalg-1lane 6.99× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 2.18745 ± 0.0362261 (W 0.0108687) | 0.288062 ± 0.00283079 (W 0.00274572) | 🔴 tlinalg-1lane 7.59× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 9.78251 ± 0.0905624 (W 0.0142824) | 1.24358 ± 0.0104313 (W 0.00708761) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `lu_factor/n4/b1024` | 0.290837 ± 0.00148247 (W 0.00230389) | 0.0623915 ± 0.000240129 (W 0.000546949) | 🔴 tlinalg-1lane 4.66× slower than `tlinalg-pool` |  |
| `lu_factor/n8/b1024` | 0.706768 ± 0.00712505 (W 0.00454404) | 0.103569 ± 0.00077882 (W 0.000821461) | 🔴 tlinalg-1lane 6.82× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 3.52648 ± 0.0332277 (W 0.00876164) | 0.454497 ± 0.00365033 (W 0.00325522) | 🔴 tlinalg-1lane 7.76× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 13.4271 ± 0.0567783 (W 0.0156281) | 1.70491 ± 0.00693321 (W 0.00771885) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n4/b1024` | 0.454477 ± 0.00282488 (W 0.00305006) | 0.0735075 ± 0.000593027 (W 0.000787833) | 🔴 tlinalg-1lane 6.18× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n8/b1024` | 1.19824 ± 0.0203108 (W 0.00399419) | 0.157399 ± 0.00231805 (W 0.00175644) | 🔴 tlinalg-1lane 7.61× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 1.36254 ± 0.0149785 (W 0.00444274) | 0.184885 ± 0.00149239 (W 0.00212325) | 🔴 tlinalg-1lane 7.37× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 6.97017 ± 0.155627 (W 0.0363737) | 0.916229 ± 0.00887415 (W 0.00514223) | 🔴 tlinalg-1lane 7.61× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.174786 ± 0.000450545 (W 0.00229396) | 0.033818 ± 0.000345513 (W 0.000676454) | 🔴 tlinalg-1lane 5.17× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n8/b1024` | 0.500433 ± 0.00580298 (W 0.0032946) | 0.076377 ± 0.000304347 (W 0.000928109) | 🔴 tlinalg-1lane 6.55× slower than `tlinalg-pool` |  |
| `qr/n16/b1024` | 11.159 ± 0.0492871 (W 0.0169303) | 1.4045 ± 0.00505033 (W 0.00272224) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 71.7255 ± 0.21346 (W 0.0519075) | 8.96275 ± 0.03781 (W 0.0138842) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.933772 ± 0.00216604 (W 0.00161274) | 0.120034 ± 0.000511853 (W 0.00183926) | 🔴 tlinalg-1lane 7.78× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.73801 ± 0.0297788 (W 0.00363895) | 0.344457 ± 0.00135764 (W 0.00232077) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 12.6319 ± 0.111508 (W 0.0249244) | 1.58438 ± 0.00408934 (W 0.00332734) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 66.9063 ± 0.47107 (W 0.0696894) | 8.43046 ± 0.0396354 (W 0.0105354) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.50856 ± 0.01287 (W 0.00316216) | 0.193746 ± 0.00227229 (W 0.00166183) | 🔴 tlinalg-1lane 7.79× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n8/b1024` | 3.89773 ± 0.0176473 (W 0.00750189) | 0.49349 ± 0.00367465 (W 0.00311804) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `solve/n16/b1024` | 3.93992 ± 0.0297474 (W 0.0073504) | 0.501365 ± 0.00541105 (W 0.00360533) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `solve/n32/b1024` | 14.4775 ± 0.086968 (W 0.0350828) | 1.84574 ± 0.0164694 (W 0.0060458) | 🔴 tlinalg-1lane 7.84× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.626934 ± 0.00349462 (W 0.00359492) | 0.082153 ± 0.000236137 (W 0.000260087) | 🔴 tlinalg-1lane 7.63× slower than `tlinalg-pool` |  |
| `solve/n8/b1024` | 1.43435 ± 0.0226915 (W 0.00702425) | 0.184364 ± 0.00315246 (W 0.0018549) | 🔴 tlinalg-1lane 7.78× slower than `tlinalg-pool` |  |
| `svd_full/n16/b1024` | 57.7864 ± 0.363031 (W 0.0515862) | 7.32564 ± 0.12741 (W 0.00537246) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 246.538 ± 6.73924 (W 0.375072) | 31.0677 ± 0.353164 (W 0.0297484) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 5.25511 ± 0.0299201 (W 0.00563953) | 0.665486 ± 0.00446216 (W 0.00335372) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 16.5881 ± 0.289224 (W 0.0212567) | 2.08867 ± 0.0156492 (W 0.00331114) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `svd_thin/n16/b1024` | 58.0204 ± 0.260069 (W 0.314948) | 7.35801 ± 0.0753289 (W 0.00695633) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `svd_thin/n32/b1024` | 246.329 ± 1.24603 (W 0.327045) | 31.0638 ± 0.352082 (W 0.0441471) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `svd_thin/n4/b1024` | 5.24822 ± 0.00820926 (W 0.00588772) | 0.660347 ± 0.00307117 (W 0.00200847) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `svd_thin/n8/b1024` | 16.5498 ± 0.0467392 (W 0.0997977) | 2.10118 ± 0.0478193 (W 0.00453648) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `svd_values/n16/b1024` | 25.6086 ± 0.213152 (W 0.0352797) | 3.22191 ± 0.00614746 (W 0.0040358) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 90.7734 ± 0.242675 (W 0.0493872) | 11.5087 ± 0.0550926 (W 0.0164725) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 3.53382 ± 0.0123745 (W 0.00469481) | 0.445762 ± 0.00315043 (W 0.00214896) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 9.13794 ± 0.0136464 (W 0.0047206) | 1.15379 ± 0.00471853 (W 0.00475971) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 1.03173 ± 0.0103994 (W 0.00323701) | 0.128845 ± 0.00191612 (W 0.0018549) | 🔴 tlinalg-1lane 8.01× slower than `tlinalg-pool` |  |
| `triangular_solve/n32/b1024` | 4.35423 ± 0.0337789 (W 0.0123945) | 0.54171 ± 0.00590258 (W 0.00387425) | 🔴 tlinalg-1lane 8.04× slower than `tlinalg-pool` |  |
| `triangular_solve/n4/b1024` | 0.172517 ± 8.82435e-05 (W 0.00187256) | 0.02404 ± 0.000107363 (W 0.000173565) | 🔴 tlinalg-1lane 7.18× slower than `tlinalg-pool` |  |
| `triangular_solve/n8/b1024` | 0.414203 ± 0.00162159 (W 0.00339469) | 0.0543715 ± 0.000570308 (W 0.00134084) | 🔴 tlinalg-1lane 7.62× slower than `tlinalg-pool` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.066259 ± 0.0021357 (W 8.31844e-05) | 0.069194 ± 0.0018341 (W 0.000823516) | · | `!` between-start range over 5% |
| `lu/n128/b1` | 0.167979 ± 0.000859174 (W 0.00197504) | 0.170999 ± 0.000826097 (W 0.00177867) | · |  |
| `lu_factor/n128/b1` | 0.0945715 ± 0.00116563 (W 0.00178219) | 0.09133 ± 0.000362734 (W 0.000336529) | · |  |
| `lu_factor_solve/n128/b1` | 0.104545 ± 0.000128863 (W 0.00190268) | 0.102096 ± 0.000548918 (W 0.000415024) | · |  |
| `lu_solve_prepared/n128/b1` | 0.0099635 ± 3.12557e-05 (W 6.42042e-05) | 0.011356 ± 4.34933e-05 (W 5.53515e-05) | 🔵 tlinalg-1lane 1.14× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.111483 ± 0.000891944 (W 0.000285874) | 0.117569 ± 0.000632667 (W 0.00173472) | 🔵 tlinalg-1lane 1.05× faster than `tlinalg-pool` |  |
| `svd_values/n128/b1` | 1.04819 ± 0.00166292 (W 0.001042) | 1.13647 ± 0.00958545 (W 0.00377264) | 🔵 tlinalg-1lane 1.08× faster than `tlinalg-pool` |  |
| `triangular_solve/n128/b1` | 0.006963 ± 3.86221e-05 (W 6.22128e-05) | 0.0080045 ± 6.21041e-05 (W 5.74514e-05) | 🔵 tlinalg-1lane 1.15× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.176053 ± 0.00023432 (W 0.00186193) | 0.154143 ± 0.00101206 (W 0.00178607) | 🔴 tlinalg-1lane 1.14× slower than `tlinalg-pool` |  |
| `lu/n128/b1` | 0.357491 ± 0.00341935 (W 0.00368112) | 0.317883 ± 0.0064995 (W 0.00402544) | 🔴 tlinalg-1lane 1.12× slower than `tlinalg-pool` |  |
| `lu_factor/n128/b1` | 0.272933 ± 0.000569721 (W 0.002172) | 0.223747 ± 0.00126846 (W 0.00145034) | 🔴 tlinalg-1lane 1.22× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n128/b1` | 0.304723 ± 0.000909535 (W 0.00186742) | 0.257315 ± 0.00169227 (W 0.00189154) | 🔴 tlinalg-1lane 1.18× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n128/b1` | 0.0317895 ± 0.000136365 (W 8.1058e-05) | 0.034053 ± 0.000280916 (W 0.000172002) | 🔵 tlinalg-1lane 1.07× faster than `tlinalg-pool` |  |
| `solve/n128/b1` | 0.315308 ± 0.00126885 (W 0.00266206) | 0.279602 ± 0.00318749 (W 0.00183819) | 🔴 tlinalg-1lane 1.13× slower than `tlinalg-pool` |  |
| `svd_values/n128/b1` | 1.77247 ± 0.00619782 (W 0.00420091) | 1.4381 ± 0.00672384 (W 0.00343074) | 🔴 tlinalg-1lane 1.23× slower than `tlinalg-pool` |  |
| `triangular_solve/n128/b1` | 0.0189505 ± 6.06376e-05 (W 7.69039e-05) | 0.0202025 ± 0.00027618 (W 0.000108844) | 🔵 tlinalg-1lane 1.07× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 57.1425 ± 0.403774 (W 0.237783) | 27.2843 ± 0.0555811 (W 0.0204184) | 🔴 tlinalg-1lane 2.09× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 23.6903 ± 0.264609 (W 0.0293533) | 16.2024 ± 0.0451566 (W 0.0198062) | 🔴 tlinalg-1lane 1.46× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 10.306 ± 0.0359727 (W 0.0134275) | 1.59342 ± 0.0010673 (W 0.00647643) | 🔴 tlinalg-1lane 6.47× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 7.13289 ± 0.02659 (W 0.0111141) | 1.85569 ± 0.00379807 (W 0.00393876) | 🔴 tlinalg-1lane 3.84× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 18.9497 ± 0.155067 (W 0.0300574) | 5.43632 ± 0.00571122 (W 0.0132529) | 🔴 tlinalg-1lane 3.49× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 29.8621 ± 0.0622145 (W 0.0505184) | 7.23823 ± 0.0263764 (W 0.00915912) | 🔴 tlinalg-1lane 4.13× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 106.329 ± 0.357984 (W 0.265733) | 38.543 ± 0.0452361 (W 0.0608729) | 🔴 tlinalg-1lane 2.76× slower than `tlinalg-pool` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 114.021 ± 0.0916062 (W 0.0635384) | 37.079 ± 0.055944 (W 0.0451198) | 🔴 tlinalg-1lane 3.08× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 49.3193 ± 0.115585 (W 0.0589166) | 20.448 ± 0.020566 (W 0.024259) | 🔴 tlinalg-1lane 2.41× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 40.7092 ± 0.142369 (W 0.0498471) | 5.61809 ± 0.0112117 (W 0.0105355) | 🔴 tlinalg-1lane 7.25× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 27.2781 ± 0.09777 (W 0.0261826) | 5.19176 ± 0.0115498 (W 0.00507032) | 🔴 tlinalg-1lane 5.25× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 70.0172 ± 0.053385 (W 0.0605909) | 13.372 ± 0.0223992 (W 0.00979614) | 🔴 tlinalg-1lane 5.24× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 79.5998 ± 0.21824 (W 0.0648879) | 14.3165 ± 0.0291774 (W 0.0296426) | 🔴 tlinalg-1lane 5.56× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 256.094 ± 0.765974 (W 0.772005) | 75.0534 ± 0.169277 (W 0.228685) | 🔴 tlinalg-1lane 3.41× slower than `tlinalg-pool` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 22.8612 ± 0.0810014 (W 0.0332064) | 5.94473 ± 0.00532692 (W 0.0201055) | 🔴 tlinalg-1lane 3.85× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 65.3017 ± 0.0318675 (W 0.0714105) | 22.2112 ± 0.0809791 (W 0.0528854) | 🔴 tlinalg-1lane 2.94× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 101.794 ± 0.473443 (W 0.23435) | 21.5507 ± 0.0370335 (W 0.0575128) | 🔴 tlinalg-1lane 4.72× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 99.836 ± 0.202491 (W 0.171741) | 35.0745 ± 0.0996615 (W 0.109753) | 🔴 tlinalg-1lane 2.85× slower than `tlinalg-pool` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 85.5607 ± 0.652664 (W 0.146629) | 17.4599 ± 0.599918 (W 0.0435123) | 🔴 tlinalg-1lane 4.90× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `qr/4096x256/b1` | 234.716 ± 0.257465 (W 0.36461) | 58.5776 ± 0.0362461 (W 0.0879912) | 🔴 tlinalg-1lane 4.01× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 350.108 ± 1.48494 (W 1.52206) | 59.325 ± 0.19465 (W 0.211312) | 🔴 tlinalg-1lane 5.90× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 362.448 ± 0.238736 (W 0.526435) | 107.996 ± 0.142615 (W 0.329848) | 🔴 tlinalg-1lane 3.36× slower than `tlinalg-pool` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
