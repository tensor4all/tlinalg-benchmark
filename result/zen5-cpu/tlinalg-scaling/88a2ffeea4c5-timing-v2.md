<!-- generated from data/results/zen5-cpu/tlinalg-scaling/20261027T051928Z-pub-88a2ffee-20261027-scaling/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-scaling` on `zen5-cpu`

- tlinalg-rs commit: `88a2ffeea4c5ef514dac91b2ea65d43c52b121e9`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.25.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `6c795e30d74f6a15af990fb38902ac28af9b3299`
- toolkit commit: `467573e6e3e405b8ec30b3b61d096c1d0c9893c3`
- measured binary SHA-256: `64481af2f151a58e4c90c1572083238ad05b2faa0e627db883da7f71a93af272`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-27T05:40:26.333781Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-scaling --aa 4 --reps 5 --prime-ms 250 --label pub-88a2ffee-20261027-scaling`
- raw data: `data/results/zen5-cpu/tlinalg-scaling/20261027T051928Z-pub-88a2ffee-20261027-scaling/`

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
    As measured: `t4a-faer` 0.25.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.25.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.80%, worst 69.29% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 50 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.36%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.865833 ± 0.0159561 (W 0.00465482) | 0.116287 ± 0.000631196 (W 0.00216823) | 🔴 tlinalg-1lane 7.45× slower than `tlinalg-pool` |  |
| `cholesky/n32/b1024` | 3.30211 ± 0.257664 (W 0.0252545) | 0.442482 ± 0.0266201 (W 0.00995187) | 🔴 tlinalg-1lane 7.46× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.182943 ± 0.00163138 (W 0.00134924) | 0.184956 ± 0.000915602 (W 0.0012586) | · |  |
| `cholesky/n8/b1024` | 0.365854 ± 0.00393082 (W 0.00181039) | 0.365969 ± 0.00223287 (W 0.00225028) | · |  |
| `eig/n16/b1024` | 94.1097 ± 0.0704232 (W 0.0945552) | 11.9074 ± 0.047779 (W 0.0442691) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 424.548 ± 0.464354 (W 2.02134) | 53.4368 ± 0.0905323 (W 0.0996651) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 6.18299 ± 0.0554701 (W 0.013016) | 6.18791 ± 0.0434959 (W 0.00660746) | · |  |
| `eig/n8/b1024` | 23.6217 ± 0.0426773 (W 0.0222125) | 2.98901 ± 0.388894 (W 0.0086608) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigh/n16/b1024` | 29.4615 ± 0.163285 (W 0.0141107) | 3.76398 ± 0.048968 (W 0.0327927) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 110.605 ± 1.31825 (W 0.0600448) | 13.9694 ± 0.147897 (W 0.022509) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.54116 ± 0.00761152 (W 0.00317408) | 2.54083 ± 0.0124089 (W 0.00452461) | · |  |
| `eigh/n8/b1024` | 8.51413 ± 0.0234077 (W 0.00749832) | 1.11056 ± 0.0868121 (W 0.00547696) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigvals/n16/b1024` | 65.0397 ± 0.155772 (W 0.0664192) | 8.1712 ± 0.0208182 (W 0.0129003) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 288.623 ± 0.386197 (W 0.357364) | 36.3538 ± 0.108244 (W 0.113083) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 3.19245 ± 0.00531782 (W 0.00342278) | 3.18884 ± 0.0155562 (W 0.00541158) | · |  |
| `eigvals/n8/b1024` | 15.2595 ± 0.237414 (W 0.011569) | 1.94147 ± 0.0109444 (W 0.0109976) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 22.2201 ± 0.0658585 (W 0.0109967) | 2.8139 ± 0.00981458 (W 0.00486879) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 86.335 ± 0.321709 (W 0.0649063) | 10.8968 ± 0.0370895 (W 0.0156402) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.05307 ± 0.00777575 (W 0.00303855) | 2.06032 ± 0.00924392 (W 0.00335389) | · |  |
| `eigvalsh/n8/b1024` | 6.87306 ± 0.0187208 (W 0.00826292) | 0.870003 ± 0.00210782 (W 0.00243779) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 3.83482 ± 0.0406951 (W 0.0175363) | 0.517587 ± 0.0102656 (W 0.00846384) | 🔴 tlinalg-1lane 7.41× slower than `tlinalg-pool` |  |
| `full_piv_lu/n32/b1024` | 16.0857 ± 0.161977 (W 0.0284541) | 2.18591 ± 0.0416383 (W 0.00955165) | 🔴 tlinalg-1lane 7.36× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.406029 ± 0.00751024 (W 0.00222731) | 0.404051 ± 0.00670401 (W 0.00156097) | · |  |
| `full_piv_lu/n8/b1024` | 1.1426 ± 0.0132091 (W 0.00468584) | 1.15412 ± 0.0187947 (W 0.00465195) | · |  |
| `full_piv_lu_solve/n16/b1024` | 3.52976 ± 0.00812468 (W 0.011976) | 0.470058 ± 0.00824731 (W 0.00325734) | 🔴 tlinalg-1lane 7.51× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 11.6528 ± 0.0866347 (W 0.0540378) | 1.57456 ± 0.028375 (W 0.0208977) | 🔴 tlinalg-1lane 7.40× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.539875 ± 0.010125 (W 0.00443694) | 0.535475 ± 0.00520477 (W 0.00394934) | · |  |
| `full_piv_lu_solve/n8/b1024` | 1.27496 ± 0.00738943 (W 0.00673362) | 0.172232 ± 0.000857942 (W 0.00276655) | 🔴 tlinalg-1lane 7.40× slower than `tlinalg-pool` |  |
| `householder_apply/n16/b1024` | 4.69808 ± 0.146372 (W 0.00468026) | 0.624421 ± 0.00848041 (W 0.00180619) | 🔴 tlinalg-1lane 7.52× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 19.3074 ± 0.606821 (W 0.0342146) | 2.48604 ± 0.0502181 (W 0.0152317) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.386799 ± 0.0130785 (W 0.00172686) | 0.389639 ± 0.0139743 (W 0.00214253) | · | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.25868 ± 0.0185828 (W 0.00239019) | 0.178774 ± 0.00656772 (W 0.00125468) | 🔴 tlinalg-1lane 7.04× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 3.78443 ± 0.0360593 (W 0.00680875) | 0.501331 ± 0.00521675 (W 0.00241122) | 🔴 tlinalg-1lane 7.55× slower than `tlinalg-pool` |  |
| `householder_factor/n32/b1024` | 12.8716 ± 0.211739 (W 0.030082) | 1.68233 ± 0.0177644 (W 0.0107589) | 🔴 tlinalg-1lane 7.65× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.461642 ± 0.00283596 (W 0.00215883) | 0.464799 ± 0.00563055 (W 0.00209709) | · |  |
| `householder_factor/n8/b1024` | 1.26428 ± 0.0200176 (W 0.00195856) | 0.174532 ± 0.0042827 (W 0.000983577) | 🔴 tlinalg-1lane 7.24× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n16/b1024` | 2.62312 ± 0.0433326 (W 0.00843651) | 0.3673 ± 0.00807293 (W 0.00383322) | 🔴 tlinalg-1lane 7.14× slower than `tlinalg-pool` |  |
| `lu/n32/b1024` | 9.17168 ± 0.055868 (W 0.0206442) | 1.2963 ± 0.0148041 (W 0.0125033) | 🔴 tlinalg-1lane 7.08× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.319407 ± 0.015475 (W 0.00184825) | 0.315094 ± 0.0168486 (W 0.00271375) | · | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.859892 ± 0.0161639 (W 0.00369051) | 0.865109 ± 0.0350917 (W 0.00700321) | · | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 1.85393 ± 0.0349208 (W 0.00507189) | 0.265772 ± 0.00432235 (W 0.00256272) | 🔴 tlinalg-1lane 6.98× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 5.50613 ± 0.0925646 (W 0.0128474) | 0.735554 ± 0.0224294 (W 0.01306) | 🔴 tlinalg-1lane 7.49× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n4/b1024` | 0.244082 ± 0.00214336 (W 0.00194392) | 0.242959 ± 0.00170233 (W 0.00190805) | · |  |
| `lu_factor/n8/b1024` | 0.611244 ± 0.00669179 (W 0.00310577) | 0.615312 ± 0.00853508 (W 0.00489045) | · |  |
| `lu_factor_solve/n16/b1024` | 2.50055 ± 0.0249631 (W 0.0059558) | 0.340286 ± 0.00560016 (W 0.00276933) | 🔴 tlinalg-1lane 7.35× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 6.85988 ± 0.0518154 (W 0.00795337) | 0.905338 ± 0.0183844 (W 0.0110191) | 🔴 tlinalg-1lane 7.58× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n4/b1024` | 0.301874 ± 0.00611893 (W 0.00204196) | 0.304064 ± 0.00605016 (W 0.00227786) | · |  |
| `lu_factor_solve/n8/b1024` | 0.83973 ± 0.0212923 (W 0.00494197) | 0.131226 ± 0.00210441 (W 0.00161214) | 🔴 tlinalg-1lane 6.40× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1024` | 0.603789 ± 0.00820206 (W 0.00229768) | 0.107711 ± 0.000683346 (W 0.00142269) | 🔴 tlinalg-1lane 5.61× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 2.44873 ± 0.0611439 (W 0.024597) | 0.324847 ± 0.0178546 (W 0.0141582) | 🔴 tlinalg-1lane 7.54× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.070923 ± 9.22691e-05 (W 0.00152274) | 0.070878 ± 0.000630149 (W 0.000185887) | · |  |
| `lu_solve_prepared/n8/b1024` | 0.23293 ± 0.000530776 (W 0.00168948) | 0.232681 ± 0.00441266 (W 0.00202449) | · |  |
| `qr/n16/b1024` | 8.8158 ± 0.0979287 (W 0.00827271) | 1.12899 ± 0.0206905 (W 0.00720969) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 36.0334 ± 0.168145 (W 0.0399701) | 4.61126 ± 0.0377618 (W 0.0140948) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.771232 ± 0.0126719 (W 0.0022063) | 0.767616 ± 0.00959647 (W 0.00304201) | · |  |
| `qr/n8/b1024` | 2.36768 ± 0.0319147 (W 0.00220762) | 2.37552 ± 0.0355434 (W 0.00308046) | · |  |
| `rank_revealing_qr/n16/b1024` | 10.4467 ± 0.230588 (W 0.0190002) | 1.35136 ± 0.0313291 (W 0.0462827) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `rank_revealing_qr/n32/b1024` | 36.1199 ± 0.286299 (W 0.0357759) | 4.63999 ± 0.0492296 (W 0.022016) | 🔴 tlinalg-1lane 7.78× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.25283 ± 0.0226422 (W 0.00454112) | 1.25389 ± 0.0404667 (W 0.00631177) | · | `!` between-start range over 5% |
| `rank_revealing_qr/n8/b1024` | 3.37441 ± 0.0255359 (W 0.00812593) | 3.43512 ± 0.0674479 (W 0.0068472) | · |  |
| `solve/n16/b1024` | 2.70534 ± 0.0550594 (W 0.0183117) | 0.361501 ± 0.00115828 (W 0.00233033) | 🔴 tlinalg-1lane 7.48× slower than `tlinalg-pool` |  |
| `solve/n32/b1024` | 7.24391 ± 0.0992962 (W 0.0447685) | 0.963348 ± 0.00617059 (W 0.00710255) | 🔴 tlinalg-1lane 7.52× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.388772 ± 0.00258933 (W 0.00385048) | 0.384133 ± 0.00247795 (W 0.00345268) | · |  |
| `solve/n8/b1024` | 0.943127 ± 0.00767837 (W 0.00440359) | 0.13161 ± 0.00529993 (W 0.00276061) | 🔴 tlinalg-1lane 7.17× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 55.9192 ± 0.250794 (W 0.0537085) | 7.09854 ± 0.0401452 (W 0.0805798) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 202.288 ± 0.471164 (W 0.286976) | 26.0288 ± 0.83135 (W 0.0212901) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 4.35434 ± 0.00690074 (W 0.00714162) | 4.36112 ± 0.0447724 (W 0.00512268) | · |  |
| `svd_full/n8/b1024` | 15.1856 ± 0.0413402 (W 0.00872934) | 1.97761 ± 0.0217866 (W 0.02458) | 🔴 tlinalg-1lane 7.68× slower than `tlinalg-pool` |  |
| `svd_thin/n16/b1024` | 55.7981 ± 0.104037 (W 0.0295791) | 7.12988 ± 0.0383943 (W 0.146299) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` |  |
| `svd_thin/n32/b1024` | 202.505 ± 0.591613 (W 0.362021) | 25.8685 ± 0.22288 (W 1.17001) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` |  |
| `svd_thin/n4/b1024` | 4.32781 ± 0.0126593 (W 0.00763768) | 4.3665 ± 0.0373489 (W 0.00867942) | · |  |
| `svd_thin/n8/b1024` | 15.3054 ± 0.165217 (W 0.0125415) | 1.97419 ± 0.123395 (W 0.0225529) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 40.5299 ± 0.100119 (W 0.0398403) | 5.12033 ± 0.0165424 (W 0.00585817) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 158.704 ± 0.444082 (W 0.0833878) | 20.0636 ± 0.0667661 (W 0.0424265) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 3.20849 ± 0.0224355 (W 0.0046282) | 3.22105 ± 0.0466421 (W 0.00470389) | · |  |
| `svd_values/n8/b1024` | 11.3854 ± 0.0673259 (W 0.00798326) | 1.44006 ± 0.00495357 (W 0.00366366) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 0.507726 ± 0.0134789 (W 0.0022538) | 0.0786775 ± 0.00127025 (W 0.001278) | 🔴 tlinalg-1lane 6.45× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 1.7957 ± 0.184417 (W 0.015583) | 0.206902 ± 0.0137838 (W 0.00619258) | 🔴 tlinalg-1lane 8.68× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.0908545 ± 0.000338704 (W 0.000169404) | 0.09104 ± 0.000351521 (W 0.00134793) | · |  |
| `triangular_solve/n8/b1024` | 0.21955 ± 0.000838974 (W 0.00164914) | 0.219895 ± 0.000709488 (W 0.00178135) | · |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 1.2981 ± 0.0170158 (W 0.00308845) | 0.173394 ± 0.0584157 (W 0.00201991) | 🔴 tlinalg-1lane 7.49× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `cholesky/n32/b1024` | 5.81369 ± 0.031945 (W 0.0159763) | 0.813589 ± 0.00440961 (W 0.00533695) | 🔴 tlinalg-1lane 7.15× slower than `tlinalg-pool` |  |
| `cholesky/n4/b1024` | 0.202479 ± 0.00336674 (W 0.00187507) | 0.202223 ± 0.00282242 (W 0.00138066) | · |  |
| `cholesky/n8/b1024` | 0.414094 ± 0.00600687 (W 0.00220204) | 0.415426 ± 0.00738018 (W 0.00186484) | · |  |
| `eig/n16/b1024` | 128.473 ± 0.251113 (W 0.0473078) | 16.3426 ± 0.164586 (W 0.174168) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 533.755 ± 0.454245 (W 0.392465) | 67.1784 ± 0.239136 (W 0.0592417) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 10.2058 ± 0.045504 (W 0.0171375) | 10.1685 ± 0.117467 (W 0.0176935) | · |  |
| `eig/n8/b1024` | 34.8371 ± 0.0896442 (W 0.0709297) | 4.42221 ± 0.0109969 (W 0.00681193) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `eigh/n16/b1024` | 31.6052 ± 0.102069 (W 0.0135427) | 4.00303 ± 0.0421677 (W 0.108593) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 136.997 ± 0.0722067 (W 0.126338) | 17.442 ± 0.130285 (W 0.0939303) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.92418 ± 0.0105785 (W 0.006643) | 2.92658 ± 0.00790585 (W 0.00750616) | · |  |
| `eigh/n8/b1024` | 9.12543 ± 0.0119976 (W 0.00666283) | 1.18612 ± 0.0458043 (W 0.00334228) | 🔴 tlinalg-1lane 7.69× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigvals/n16/b1024` | 76.8888 ± 0.139811 (W 0.0483698) | 9.71536 ± 0.00995767 (W 0.0166524) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 336.323 ± 0.652483 (W 0.121515) | 42.4896 ± 0.048364 (W 0.104763) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 5.01706 ± 0.0183359 (W 0.00768667) | 5.01596 ± 0.0429651 (W 0.00558303) | · |  |
| `eigvals/n8/b1024` | 19.9763 ± 0.0517384 (W 0.0162822) | 2.534 ± 0.00435184 (W 0.00840972) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 23.906 ± 0.0688777 (W 0.0116229) | 3.01866 ± 0.299397 (W 0.00704893) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigvalsh/n32/b1024` | 93.1158 ± 0.378293 (W 0.252375) | 11.7295 ± 0.0271042 (W 0.014817) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.42614 ± 0.00760625 (W 0.00593868) | 2.44417 ± 0.0120169 (W 0.00673407) | · |  |
| `eigvalsh/n8/b1024` | 7.341 ± 0.0191678 (W 0.00650553) | 0.940648 ± 0.00843263 (W 0.00313589) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 4.60886 ± 0.056554 (W 0.0294592) | 0.654424 ± 0.0108044 (W 0.00808134) | 🔴 tlinalg-1lane 7.04× slower than `tlinalg-pool` |  |
| `full_piv_lu/n32/b1024` | 21.3356 ± 0.263561 (W 0.0320832) | 3.10022 ± 0.0262479 (W 0.0201977) | 🔴 tlinalg-1lane 6.88× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.458535 ± 0.00412015 (W 0.00457206) | 0.459819 ± 0.00744596 (W 0.00438019) | · |  |
| `full_piv_lu/n8/b1024` | 1.25836 ± 0.0077291 (W 0.00943207) | 0.197945 ± 0.00661225 (W 0.00301586) | 🔴 tlinalg-1lane 6.36× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 5.32045 ± 0.0363721 (W 0.0133382) | 0.705974 ± 0.00806162 (W 0.0168874) | 🔴 tlinalg-1lane 7.54× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 20.0236 ± 0.14283 (W 0.0187464) | 2.66787 ± 0.011693 (W 0.0131403) | 🔴 tlinalg-1lane 7.51× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.768521 ± 0.0196347 (W 0.00423571) | 0.773621 ± 0.0105189 (W 0.00429294) | · | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 2.01364 ± 0.0596247 (W 0.0127022) | 0.278535 ± 0.00558342 (W 0.00181881) | 🔴 tlinalg-1lane 7.23× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n16/b1024` | 5.12153 ± 0.172184 (W 0.0168018) | 0.651385 ± 0.0206197 (W 0.0126275) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 27.3589 ± 0.3385 (W 0.0400126) | 3.60227 ± 0.0413003 (W 0.0230752) | 🔴 tlinalg-1lane 7.59× slower than `tlinalg-pool` |  |
| `householder_apply/n4/b1024` | 0.357098 ± 0.0180321 (W 0.00283178) | 0.362187 ± 0.0155335 (W 0.00226254) | · | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.1399 ± 0.0275455 (W 0.00172327) | 0.156788 ± 0.00260859 (W 0.00215149) | 🔴 tlinalg-1lane 7.27× slower than `tlinalg-pool` |  |
| `householder_factor/n16/b1024` | 4.53163 ± 0.0362263 (W 0.0129798) | 0.601598 ± 0.0154623 (W 0.00599893) | 🔴 tlinalg-1lane 7.53× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n32/b1024` | 19.7656 ± 0.149817 (W 0.0312759) | 2.60157 ± 0.024567 (W 0.0172731) | 🔴 tlinalg-1lane 7.60× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.570777 ± 0.00476096 (W 0.00177903) | 0.570701 ± 0.00434016 (W 0.00166594) | · |  |
| `householder_factor/n8/b1024` | 1.47738 ± 0.00414939 (W 0.00210932) | 0.202338 ± 0.0022377 (W 0.00177881) | 🔴 tlinalg-1lane 7.30× slower than `tlinalg-pool` |  |
| `lu/n16/b1024` | 3.17931 ± 0.0780061 (W 0.0155074) | 0.450713 ± 0.00787496 (W 0.00708161) | 🔴 tlinalg-1lane 7.05× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n32/b1024` | 14.2407 ± 0.141286 (W 0.0221006) | 2.12058 ± 0.0160096 (W 0.0141126) | 🔴 tlinalg-1lane 6.72× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.394363 ± 0.00535517 (W 0.00259647) | 0.382499 ± 0.00851761 (W 0.00254443) | · |  |
| `lu/n8/b1024` | 0.9539 ± 0.0118962 (W 0.00463296) | 0.154308 ± 0.00150245 (W 0.00253774) | 🔴 tlinalg-1lane 6.18× slower than `tlinalg-pool` |  |
| `lu_factor/n16/b1024` | 2.1935 ± 0.0290349 (W 0.00615819) | 0.308352 ± 0.00759491 (W 0.00306905) | 🔴 tlinalg-1lane 7.11× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 9.52427 ± 0.187431 (W 0.0255534) | 1.28059 ± 0.0238099 (W 0.0115715) | 🔴 tlinalg-1lane 7.44× slower than `tlinalg-pool` |  |
| `lu_factor/n4/b1024` | 0.300265 ± 0.00305522 (W 0.00219334) | 0.300315 ± 0.00230507 (W 0.00206035) | · |  |
| `lu_factor/n8/b1024` | 0.726231 ± 0.00603307 (W 0.00467553) | 0.114564 ± 0.00161452 (W 0.00138078) | 🔴 tlinalg-1lane 6.34× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 3.48012 ± 0.0379602 (W 0.00905716) | 0.466978 ± 0.00309523 (W 0.00687195) | 🔴 tlinalg-1lane 7.45× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 13.2124 ± 0.122627 (W 0.0337285) | 1.79017 ± 0.0530121 (W 0.0215282) | 🔴 tlinalg-1lane 7.38× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n4/b1024` | 0.456617 ± 0.00326283 (W 0.00288015) | 0.455968 ± 0.00337066 (W 0.00310695) | · |  |
| `lu_factor_solve/n8/b1024` | 1.20298 ± 0.0171824 (W 0.00442315) | 0.174571 ± 0.00220119 (W 0.002457) | 🔴 tlinalg-1lane 6.89× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 1.32028 ± 0.0124527 (W 0.00631598) | 0.197114 ± 0.000801128 (W 0.00129709) | 🔴 tlinalg-1lane 6.70× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 6.36194 ± 0.276502 (W 0.0180862) | 0.898393 ± 0.00945169 (W 0.0157612) | 🔴 tlinalg-1lane 7.08× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.166156 ± 0.000399225 (W 0.00156922) | 0.165269 ± 0.000711378 (W 0.001715) | · |  |
| `lu_solve_prepared/n8/b1024` | 0.4867 ± 0.00220224 (W 0.00311252) | 0.0882295 ± 0.000374371 (W 0.00130785) | 🔴 tlinalg-1lane 5.52× slower than `tlinalg-pool` |  |
| `qr/n16/b1024` | 11.159 ± 0.0742642 (W 0.0159786) | 1.44089 ± 0.0136802 (W 0.0156592) | 🔴 tlinalg-1lane 7.74× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 73.0476 ± 0.492377 (W 0.0530919) | 9.36951 ± 0.0467353 (W 0.0436091) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.923571 ± 0.0102342 (W 0.00250674) | 0.921332 ± 0.0125615 (W 0.00144846) | · |  |
| `qr/n8/b1024` | 2.69394 ± 0.0195136 (W 0.00269898) | 0.352094 ± 0.00499052 (W 0.00230859) | 🔴 tlinalg-1lane 7.65× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 12.3767 ± 0.113852 (W 0.0189281) | 1.58246 ± 0.00739187 (W 0.0142929) | 🔴 tlinalg-1lane 7.82× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 67.2395 ± 0.278295 (W 0.0298652) | 8.70533 ± 0.0909631 (W 0.0468757) | 🔴 tlinalg-1lane 7.72× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.55697 ± 0.0200709 (W 0.00333318) | 1.55651 ± 0.0193918 (W 0.00304045) | · |  |
| `rank_revealing_qr/n8/b1024` | 3.80893 ± 0.0259823 (W 0.00413005) | 0.490312 ± 0.00385086 (W 0.00312452) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` |  |
| `solve/n16/b1024` | 3.83303 ± 0.0630791 (W 0.0126306) | 0.517904 ± 0.0117919 (W 0.0150804) | 🔴 tlinalg-1lane 7.40× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n32/b1024` | 14.0316 ± 0.0432309 (W 0.0411989) | 1.86986 ± 0.0149513 (W 0.00933086) | 🔴 tlinalg-1lane 7.50× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.574538 ± 0.00466811 (W 0.00333073) | 0.572494 ± 0.00329563 (W 0.00348243) | · |  |
| `solve/n8/b1024` | 1.39125 ± 0.0188467 (W 0.00410879) | 0.192289 ± 0.000230599 (W 0.00174322) | 🔴 tlinalg-1lane 7.24× slower than `tlinalg-pool` |  |
| `svd_full/n16/b1024` | 61.0747 ± 0.302829 (W 0.0289124) | 7.74028 ± 0.111332 (W 0.037991) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 261.558 ± 0.269573 (W 0.173469) | 33.9397 ± 1.25834 (W 1.23357) | 🔴 tlinalg-1lane 7.71× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 5.24319 ± 0.020611 (W 0.00522649) | 5.24903 ± 0.020614 (W 0.00333025) | · |  |
| `svd_full/n8/b1024` | 17.1134 ± 0.0343908 (W 0.0074651) | 2.20565 ± 0.0495134 (W 0.0174233) | 🔴 tlinalg-1lane 7.76× slower than `tlinalg-pool` |  |
| `svd_thin/n16/b1024` | 60.9384 ± 0.157404 (W 0.0509913) | 7.74237 ± 0.101158 (W 0.0372981) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `svd_thin/n32/b1024` | 261.512 ± 0.303238 (W 0.423722) | 33.3996 ± 2.66933 (W 0.25813) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 5.26107 ± 0.0504836 (W 0.00457062) | 5.26091 ± 0.167024 (W 0.0082572) | · | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 17.1233 ± 0.336091 (W 0.0144916) | 2.17416 ± 0.0663422 (W 0.0277973) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 45.8312 ± 0.130283 (W 0.0294981) | 5.86788 ± 0.0963949 (W 0.0438417) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 177.564 ± 0.128996 (W 0.407811) | 22.5687 ± 0.234702 (W 0.064589) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 4.02458 ± 0.020003 (W 0.00320011) | 4.03972 ± 0.0235233 (W 0.00291332) | · |  |
| `svd_values/n8/b1024` | 13.3219 ± 0.0573229 (W 0.0119322) | 1.68141 ± 0.00873096 (W 0.00252017) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 0.989802 ± 0.00379273 (W 0.00130189) | 0.137802 ± 0.00397597 (W 0.0027597) | 🔴 tlinalg-1lane 7.18× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 4.19654 ± 0.626999 (W 0.0586239) | 0.5951 ± 0.0610104 (W 0.0160335) | 🔴 tlinalg-1lane 7.05× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.16386 ± 0.000705953 (W 0.0015289) | 0.164652 ± 0.000937656 (W 0.00160929) | · |  |
| `triangular_solve/n8/b1024` | 0.405262 ± 0.0043537 (W 0.0029277) | 0.0662335 ± 0.000618719 (W 0.000764516) | 🔴 tlinalg-1lane 6.12× slower than `tlinalg-pool` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0637895 ± 0.000238485 (W 0.00163926) | 0.0642 ± 0.000165 (W 0.000762554) | · |  |
| `lu/n128/b1` | 0.151253 ± 0.000911228 (W 0.00172493) | 0.176905 ± 0.00173966 (W 0.00395196) | 🔵 tlinalg-1lane 1.17× faster than `tlinalg-pool` |  |
| `lu_factor/n128/b1` | 0.0958645 ± 0.000616562 (W 0.000903029) | 0.114474 ± 0.00579144 (W 0.00512682) | 🔵 tlinalg-1lane 1.19× faster than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n128/b1` | 0.106259 ± 0.000656797 (W 0.00132425) | 0.123971 ± 0.000622618 (W 0.00124569) | 🔵 tlinalg-1lane 1.17× faster than `tlinalg-pool` |  |
| `lu_solve_prepared/n128/b1` | 0.010054 ± 5.71548e-05 (W 0.000101678) | 0.0102545 ± 5.33253e-05 (W 6.24641e-05) | · | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.114504 ± 0.00067459 (W 0.00086068) | 0.139866 ± 0.00206507 (W 0.00440483) | 🔵 tlinalg-1lane 1.22× faster than `tlinalg-pool` |  |
| `svd_values/n128/b1` | 2.3426 ± 0.00531691 (W 0.00225969) | 2.38006 ± 0.00625391 (W 0.00294289) | · |  |
| `triangular_solve/n128/b1` | 0.006872 ± 7.85085e-05 (W 2.87643e-05) | 0.007093 ± 9.99346e-05 (W 6.74726e-05) | · | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.176514 ± 0.000290059 (W 0.000403907) | 0.185847 ± 0.000556793 (W 0.00276415) | 🔵 tlinalg-1lane 1.05× faster than `tlinalg-pool` |  |
| `lu/n128/b1` | 0.328569 ± 0.00453098 (W 0.00342719) | 0.344639 ± 0.00508559 (W 0.00534265) | · |  |
| `lu_factor/n128/b1` | 0.266062 ± 0.00120618 (W 0.00293169) | 0.269718 ± 0.00395909 (W 0.00338685) | · |  |
| `lu_factor_solve/n128/b1` | 0.295417 ± 0.00106524 (W 0.00277934) | 0.30014 ± 0.00248675 (W 0.00351507) | · |  |
| `lu_solve_prepared/n128/b1` | 0.031514 ± 7.59386e-05 (W 7.46729e-05) | 0.031679 ± 6.34429e-05 (W 7.03102e-05) | · |  |
| `solve/n128/b1` | 0.303798 ± 0.001006 (W 0.00180225) | 0.319522 ± 0.00339738 (W 0.00470821) | 🔵 tlinalg-1lane 1.05× faster than `tlinalg-pool` |  |
| `svd_values/n128/b1` | 3.13618 ± 0.0178183 (W 0.00507532) | 3.23276 ± 0.0138551 (W 0.00854363) | · |  |
| `triangular_solve/n128/b1` | 0.0185645 ± 4.49481e-05 (W 8.54732e-05) | 0.01878 ± 5.00691e-05 (W 0.000114419) | · | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 57.1687 ± 0.435879 (W 0.0203536) | 29.0907 ± 0.0426128 (W 0.0340605) | 🔴 tlinalg-1lane 1.97× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 23.3981 ± 0.557403 (W 0.204351) | 17.5989 ± 0.0480101 (W 0.020411) | 🔴 tlinalg-1lane 1.33× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n512/b1` | 10.2773 ± 0.0286498 (W 0.00729489) | 1.77665 ± 0.017543 (W 0.00568224) | 🔴 tlinalg-1lane 5.78× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 7.23857 ± 0.00666485 (W 0.00790473) | 2.06452 ± 0.00940168 (W 0.0103806) | 🔴 tlinalg-1lane 3.51× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 19.363 ± 0.0841233 (W 0.0148962) | 6.16167 ± 0.00992824 (W 0.01574) | 🔴 tlinalg-1lane 3.14× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 24.7452 ± 0.1279 (W 0.0257131) | 8.68843 ± 0.0650873 (W 0.0335947) | 🔴 tlinalg-1lane 2.85× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 116.751 ± 0.475156 (W 0.529771) | 60.2043 ± 0.224245 (W 0.0731031) | 🔴 tlinalg-1lane 1.94× slower than `tlinalg-pool` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 114.397 ± 0.0963488 (W 0.106381) | 39.9479 ± 0.347142 (W 0.382336) | 🔴 tlinalg-1lane 2.86× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 49.0616 ± 0.256664 (W 0.366998) | 23.6422 ± 0.123406 (W 0.0694215) | 🔴 tlinalg-1lane 2.08× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 40.8884 ± 0.216108 (W 0.0341234) | 5.82915 ± 0.00572249 (W 0.0152993) | 🔴 tlinalg-1lane 7.01× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 27.6325 ± 0.0511374 (W 0.039765) | 5.55035 ± 0.0166113 (W 0.00820596) | 🔴 tlinalg-1lane 4.98× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 70.4843 ± 0.042125 (W 0.0401819) | 15.0116 ± 0.0236313 (W 0.0172752) | 🔴 tlinalg-1lane 4.70× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 83.1585 ± 0.154783 (W 0.0628839) | 16.9667 ± 0.0265253 (W 0.0253664) | 🔴 tlinalg-1lane 4.90× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 261.424 ± 0.750468 (W 0.712675) | 95.9695 ± 0.314649 (W 0.231861) | 🔴 tlinalg-1lane 2.72× slower than `tlinalg-pool` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 22.9525 ± 0.267711 (W 0.0413737) | 6.97287 ± 0.0199433 (W 0.0190604) | 🔴 tlinalg-1lane 3.29× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 66.8969 ± 0.206555 (W 0.0689655) | 23.4876 ± 0.0527883 (W 0.0445602) | 🔴 tlinalg-1lane 2.85× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 101.45 ± 0.822464 (W 0.284266) | 24.5231 ± 0.0142853 (W 0.0602584) | 🔴 tlinalg-1lane 4.14× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 103.162 ± 0.100717 (W 0.0937782) | 40.905 ± 0.096229 (W 0.132237) | 🔴 tlinalg-1lane 2.52× slower than `tlinalg-pool` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 84.2698 ± 0.0878943 (W 0.085441) | 18.8039 ± 0.0111856 (W 0.0207662) | 🔴 tlinalg-1lane 4.48× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 235.528 ± 0.235981 (W 0.442238) | 55.1274 ± 0.672628 (W 1.20841) | 🔴 tlinalg-1lane 4.27× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 341.805 ± 0.816679 (W 0.608351) | 61.4339 ± 0.596463 (W 0.724725) | 🔴 tlinalg-1lane 5.56× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 365.459 ± 0.0942483 (W 0.671831) | 110.34 ± 0.400263 (W 0.821007) | 🔴 tlinalg-1lane 3.31× slower than `tlinalg-pool` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
