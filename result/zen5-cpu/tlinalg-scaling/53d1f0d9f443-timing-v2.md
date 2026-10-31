<!-- generated from data/results/zen5-cpu/tlinalg-scaling/20261031T131253Z-pub-53d1f0d9-20261031-scaling/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-scaling` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `f00d46158eeb5cacf198bceba6197d5eb2043afc`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `028b45886580e5353ddee46798f3d2cd7cf52f7521251264812b3a908590da86`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-31T13:33:34.104119Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 1 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-scaling --aa 4 --reps 5 --prime-ms 250 --label pub-53d1f0d9-20261031-scaling`
- raw data: `data/results/zen5-cpu/tlinalg-scaling/20261031T131253Z-pub-53d1f0d9-20261031-scaling/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.57%, worst 12.05% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 27 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.32%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.855849 ± 0.0291032 (W 0.00195178) | 0.115596 ± 0.00297433 (W 0.00131191) | 🔴 tlinalg-1lane 7.40× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 3.20277 ± 0.0344566 (W 0.0222837) | 0.477874 ± 0.0236719 (W 0.0055627) | 🔴 tlinalg-1lane 6.70× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.17919 ± 0.000665212 (W 0.00162742) | 0.179998 ± 0.000707896 (W 0.00154636) | · |  |
| `cholesky/n8/b1024` | 0.359067 ± 0.00779763 (W 0.00249448) | 0.046963 ± 0.00113275 (W 0.000118693) | 🔴 tlinalg-1lane 7.65× slower than `tlinalg-pool` |  |
| `eig/n16/b1024` | 96.3224 ± 0.232625 (W 0.148996) | 12.0664 ± 0.0226326 (W 0.0155419) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 431.294 ± 1.31978 (W 2.26262) | 54.1353 ± 0.161072 (W 0.0599572) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 6.40936 ± 0.0384349 (W 0.0144335) | 0.814918 ± 0.00734586 (W 0.0039772) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `eig/n8/b1024` | 24.1055 ± 0.0553928 (W 0.0354991) | 3.02484 ± 0.0150027 (W 0.00528488) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `eigh/n16/b1024` | 30.0237 ± 0.142752 (W 0.0199264) | 3.78373 ± 0.0102178 (W 0.00674009) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 111.788 ± 0.262223 (W 0.244854) | 13.9812 ± 0.0605025 (W 0.0152887) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.53722 ± 0.0185145 (W 0.00557133) | 0.322693 ± 0.00247533 (W 0.00180856) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 8.69073 ± 0.084301 (W 0.0150905) | 1.0969 ± 0.0086676 (W 0.00140577) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigvals/n16/b1024` | 66.6984 ± 0.184383 (W 0.0455893) | 8.40082 ± 0.0140545 (W 0.00504718) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 292.463 ± 0.431381 (W 0.576801) | 36.7273 ± 0.105627 (W 0.191188) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 3.42968 ± 0.0369116 (W 0.00700129) | 0.440434 ± 0.00255486 (W 0.00317691) | 🔴 tlinalg-1lane 7.79× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 15.7784 ± 0.0619819 (W 0.0294281) | 1.99883 ± 0.00683196 (W 0.0042415) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 22.7451 ± 0.153439 (W 0.0198078) | 2.85937 ± 0.0131626 (W 0.00274532) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 85.1785 ± 0.241138 (W 0.0809479) | 10.6777 ± 0.0541594 (W 0.00634604) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.08059 ± 0.00260483 (W 0.00224398) | 0.263557 ± 0.000780352 (W 0.00321034) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 6.9658 ± 0.0236987 (W 0.00678945) | 0.883954 ± 0.00519868 (W 0.00158982) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 3.89463 ± 0.0309431 (W 0.0158966) | 0.512506 ± 0.0053001 (W 0.0046377) | 🔴 tlinalg-1lane 7.60× slower than `tlinalg-pool` |  |
| `full_piv_lu/n32/b1024` | 14.9886 ± 0.151486 (W 0.0253562) | 2.0321 ± 0.0125992 (W 0.0168606) | 🔴 tlinalg-1lane 7.38× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.492873 ± 0.00424397 (W 0.00365398) | 0.493069 ± 0.00219258 (W 0.00347171) | · |  |
| `full_piv_lu/n8/b1024` | 1.29494 ± 0.0127305 (W 0.0103216) | 0.181891 ± 0.00180557 (W 0.00207077) | 🔴 tlinalg-1lane 7.12× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n16/b1024` | 3.97782 ± 0.0419627 (W 0.0106712) | 0.518838 ± 0.0104859 (W 0.00271659) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 12.7556 ± 0.22577 (W 0.071261) | 1.63829 ± 0.0144249 (W 0.0170708) | 🔴 tlinalg-1lane 7.79× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.643456 ± 0.00153958 (W 0.00375278) | 0.085125 ± 0.00068985 (W 0.00205518) | 🔴 tlinalg-1lane 7.56× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n8/b1024` | 1.58164 ± 0.0186299 (W 0.0103959) | 0.205722 ± 0.00048924 (W 0.00152377) | 🔴 tlinalg-1lane 7.69× slower than `tlinalg-pool` |  |
| `householder_apply/n16/b1024` | 4.90249 ± 0.146096 (W 0.00771353) | 0.610801 ± 0.0190718 (W 0.00305887) | 🔴 tlinalg-1lane 8.03× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 20.3604 ± 0.786062 (W 0.04494) | 2.46243 ± 0.0650348 (W 0.0103442) | 🔴 tlinalg-1lane 8.27× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.402465 ± 0.00935227 (W 0.00233096) | 0.0512605 ± 0.00121339 (W 0.000251588) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.3187 ± 0.0650999 (W 0.00368994) | 0.166221 ± 0.00555407 (W 0.0015534) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 4.02627 ± 0.061204 (W 0.00458937) | 0.511219 ± 0.00918973 (W 0.00217504) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `householder_factor/n32/b1024` | 13.4184 ± 0.308597 (W 0.0424563) | 1.67912 ± 0.0257903 (W 0.00485654) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n4/b1024` | 0.489 ± 0.00325598 (W 0.00205088) | 0.0639655 ± 0.000667716 (W 0.000332418) | 🔴 tlinalg-1lane 7.64× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.30977 ± 0.0226862 (W 0.00249652) | 0.168345 ± 0.00267909 (W 0.000867601) | 🔴 tlinalg-1lane 7.78× slower than `tlinalg-pool` |  |
| `lu/n16/b1024` | 2.91453 ± 0.0350465 (W 0.0142099) | 0.382903 ± 0.00483953 (W 0.00258095) | 🔴 tlinalg-1lane 7.61× slower than `tlinalg-pool` |  |
| `lu/n32/b1024` | 10.3944 ± 0.1278 (W 0.0373975) | 1.35435 ± 0.00344806 (W 0.00811035) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.305559 ± 0.0035299 (W 0.00294347) | 0.304856 ± 0.00308516 (W 0.0033308) | · |  |
| `lu/n8/b1024` | 0.878233 ± 0.0130956 (W 0.00322447) | 0.135704 ± 0.00140518 (W 0.0014278) | 🔴 tlinalg-1lane 6.47× slower than `tlinalg-pool` |  |
| `lu_factor/n16/b1024` | 1.91506 ± 0.0249218 (W 0.013055) | 0.252263 ± 0.00212198 (W 0.00150737) | 🔴 tlinalg-1lane 7.59× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 5.66441 ± 0.0239483 (W 0.0145566) | 0.723919 ± 0.00431761 (W 0.00184592) | 🔴 tlinalg-1lane 7.82× slower than `tlinalg-pool` |  |
| `lu_factor/n4/b1024` | 0.236664 ± 0.000912643 (W 0.0026237) | 0.236148 ± 0.00167616 (W 0.00155674) | · |  |
| `lu_factor/n8/b1024` | 0.609159 ± 0.00623041 (W 0.00475437) | 0.0967765 ± 0.000975413 (W 0.00147184) | 🔴 tlinalg-1lane 6.29× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 2.4989 ± 0.0264915 (W 0.00846591) | 0.322345 ± 0.00508703 (W 0.00216781) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 7.01706 ± 0.0244384 (W 0.011271) | 0.887383 ± 0.00628826 (W 0.00462447) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n4/b1024` | 0.298426 ± 0.00287018 (W 0.0024136) | 0.057302 ± 0.00179883 (W 0.000687229) | 🔴 tlinalg-1lane 5.21× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.837041 ± 0.00774732 (W 0.00861025) | 0.119423 ± 0.00152607 (W 0.00149415) | 🔴 tlinalg-1lane 7.01× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 0.620486 ± 0.00330643 (W 0.00357745) | 0.097026 ± 0.000704381 (W 0.00172004) | 🔴 tlinalg-1lane 6.40× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 2.36994 ± 0.0245499 (W 0.0204599) | 0.230733 ± 0.00244539 (W 0.00195802) | 🔴 tlinalg-1lane 10.27× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n4/b1024` | 0.0732025 ± 0.00016526 (W 0.00100761) | 0.020814 ± 0.000122848 (W 0.000135739) | 🔴 tlinalg-1lane 3.52× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n8/b1024` | 0.237337 ± 0.00111239 (W 0.00259421) | 0.0436525 ± 0.000365632 (W 0.00049437) | 🔴 tlinalg-1lane 5.44× slower than `tlinalg-pool` |  |
| `qr/n16/b1024` | 9.03765 ± 0.159149 (W 0.0154025) | 1.13528 ± 0.0190053 (W 0.00244876) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 33.5354 ± 0.106137 (W 0.0291889) | 4.23196 ± 0.00843614 (W 0.00830256) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.770061 ± 0.00521924 (W 0.00410492) | 0.101009 ± 0.00186983 (W 0.00066209) | 🔴 tlinalg-1lane 7.62× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.41926 ± 0.0386027 (W 0.006063) | 0.309712 ± 0.00426611 (W 0.00199856) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 10.8266 ± 0.0966263 (W 0.0192324) | 1.35361 ± 0.0140052 (W 0.00250411) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 34.4205 ± 0.50422 (W 0.0415197) | 4.37063 ± 0.0250375 (W 0.0105433) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.34628 ± 0.0234005 (W 0.00392067) | 0.174407 ± 0.003185 (W 0.00204238) | 🔴 tlinalg-1lane 7.72× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n8/b1024` | 3.45962 ± 0.0299402 (W 0.00500486) | 0.444638 ± 0.0196609 (W 0.00270843) | 🔴 tlinalg-1lane 7.78× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n16/b1024` | 2.79951 ± 0.00902763 (W 0.015382) | 0.358156 ± 0.00489281 (W 0.00324112) | 🔴 tlinalg-1lane 7.82× slower than `tlinalg-pool` |  |
| `solve/n32/b1024` | 7.63433 ± 0.0424703 (W 0.0249661) | 0.961314 ± 0.0102158 (W 0.00518737) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.398651 ± 0.00610768 (W 0.00378354) | 0.0530095 ± 0.00107019 (W 0.00044153) | 🔴 tlinalg-1lane 7.52× slower than `tlinalg-pool` |  |
| `solve/n8/b1024` | 0.9533 ± 0.00926522 (W 0.00415344) | 0.125198 ± 0.00167272 (W 0.00146855) | 🔴 tlinalg-1lane 7.61× slower than `tlinalg-pool` |  |
| `svd_full/n16/b1024` | 53.3921 ± 0.176067 (W 0.0375215) | 6.68884 ± 0.0377078 (W 0.0105584) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 187.035 ± 4.09193 (W 0.437846) | 25.4885 ± 0.72332 (W 0.0210242) | 🔴 tlinalg-1lane 7.34× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 4.38734 ± 0.0253421 (W 0.00708009) | 0.553285 ± 0.00594591 (W 0.0033564) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 14.9096 ± 0.369134 (W 0.0241369) | 1.88544 ± 0.0481036 (W 0.00230222) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 53.4391 ± 0.25332 (W 0.0457313) | 6.69341 ± 0.0260079 (W 0.00778176) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `svd_thin/n32/b1024` | 187.212 ± 4.17959 (W 0.324838) | 25.5112 ± 0.667937 (W 0.0188084) | 🔴 tlinalg-1lane 7.34× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 4.36506 ± 0.0295653 (W 0.00495021) | 0.552784 ± 0.00278392 (W 0.00285223) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `svd_thin/n8/b1024` | 14.8115 ± 0.420935 (W 0.0266155) | 1.89821 ± 0.0480317 (W 0.00566023) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 22.1934 ± 0.0847129 (W 0.0371547) | 2.80804 ± 0.0156281 (W 0.00184502) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 74.5443 ± 0.252253 (W 0.108117) | 9.45575 ± 0.0565566 (W 0.00645828) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 2.88112 ± 0.0246642 (W 0.00557846) | 0.365038 ± 0.00378279 (W 0.00181227) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 7.90004 ± 0.0446828 (W 0.00773972) | 1.00182 ± 0.00664936 (W 0.00130818) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 0.523161 ± 0.00252261 (W 0.00318308) | 0.067923 ± 0.000406449 (W 0.000355283) | 🔴 tlinalg-1lane 7.70× slower than `tlinalg-pool` |  |
| `triangular_solve/n32/b1024` | 1.34304 ± 0.0104851 (W 0.0201505) | 0.15789 ± 0.00137315 (W 0.00235982) | 🔴 tlinalg-1lane 8.51× slower than `tlinalg-pool` |  |
| `triangular_solve/n4/b1024` | 0.093564 ± 0.000990301 (W 0.00174753) | 0.014277 ± 0.000508211 (W 0.000129012) | 🔴 tlinalg-1lane 6.55× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.226043 ± 0.000346012 (W 0.00201615) | 0.030708 ± 7.56351e-05 (W 0.000139216) | 🔴 tlinalg-1lane 7.36× slower than `tlinalg-pool` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 1.28538 ± 0.0239876 (W 0.00824835) | 0.15977 ± 0.00112832 (W 0.00166947) | 🔴 tlinalg-1lane 8.05× slower than `tlinalg-pool` |  |
| `cholesky/n32/b1024` | 5.65626 ± 0.0507389 (W 0.0160628) | 0.793188 ± 0.00520949 (W 0.00607663) | 🔴 tlinalg-1lane 7.13× slower than `tlinalg-pool` |  |
| `cholesky/n4/b1024` | 0.19737 ± 6.93319e-05 (W 0.00218379) | 0.027612 ± 0.000214399 (W 0.000133912) | 🔴 tlinalg-1lane 7.15× slower than `tlinalg-pool` |  |
| `cholesky/n8/b1024` | 0.419466 ± 0.0141926 (W 0.0030408) | 0.0555145 ± 0.00132994 (W 0.000799489) | 🔴 tlinalg-1lane 7.56× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eig/n16/b1024` | 130.849 ± 0.424093 (W 0.20312) | 16.491 ± 0.0393093 (W 0.0193509) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 540.891 ± 0.521459 (W 0.560875) | 67.8147 ± 0.0988268 (W 0.168301) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 10.8051 ± 0.0261343 (W 0.020983) | 1.38413 ± 0.00557563 (W 0.00280759) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `eig/n8/b1024` | 35.7582 ± 0.142647 (W 0.0371665) | 4.57954 ± 0.00716057 (W 0.00606449) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `eigh/n16/b1024` | 32.2372 ± 0.0338834 (W 0.0970892) | 4.01829 ± 0.00822771 (W 0.00606951) | 🔴 tlinalg-1lane 8.02× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 139.376 ± 0.229955 (W 0.0567097) | 17.4101 ± 0.105418 (W 0.016723) | 🔴 tlinalg-1lane 8.01× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.98734 ± 0.0267806 (W 0.003892) | 0.385568 ± 0.000198534 (W 0.00198619) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 9.32093 ± 0.0344586 (W 0.01151) | 1.1855 ± 0.0136439 (W 0.00258504) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `eigvals/n16/b1024` | 78.494 ± 0.214892 (W 0.0389553) | 9.90462 ± 0.0157364 (W 0.0057164) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 341.618 ± 0.76001 (W 0.512053) | 43.3047 ± 0.256161 (W 0.0176132) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 5.50508 ± 0.0220492 (W 0.00929968) | 0.702493 ± 0.0125656 (W 0.00136886) | 🔴 tlinalg-1lane 7.84× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 20.5258 ± 0.132634 (W 0.0152265) | 2.60502 ± 0.0165216 (W 0.00346474) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 24.1794 ± 0.0725263 (W 0.0128363) | 3.04515 ± 0.00269629 (W 0.0025504) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 92.1772 ± 0.101092 (W 0.225622) | 11.5653 ± 0.0297567 (W 0.00837582) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.49101 ± 0.016896 (W 0.00495819) | 0.317123 ± 0.00260755 (W 0.0027383) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 7.54171 ± 0.0326531 (W 0.00874277) | 0.956037 ± 0.00216682 (W 0.00191545) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 5.21645 ± 0.193348 (W 0.0210197) | 0.69198 ± 0.0120868 (W 0.00705793) | 🔴 tlinalg-1lane 7.54× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 21.4471 ± 0.26812 (W 0.0241189) | 3.03571 ± 0.00758872 (W 0.0149521) | 🔴 tlinalg-1lane 7.06× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.590545 ± 0.00927172 (W 0.00389761) | 0.0880455 ± 0.000572177 (W 0.000605743) | 🔴 tlinalg-1lane 6.71× slower than `tlinalg-pool` |  |
| `full_piv_lu/n8/b1024` | 1.52066 ± 0.0185886 (W 0.00774503) | 0.211531 ± 0.0053198 (W 0.00272508) | 🔴 tlinalg-1lane 7.19× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 6.26332 ± 0.0700505 (W 0.083906) | 0.80608 ± 0.00675734 (W 0.00332452) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 21.5046 ± 0.302278 (W 0.0158413) | 2.75114 ± 0.0254169 (W 0.00697919) | 🔴 tlinalg-1lane 7.82× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.903879 ± 0.00800231 (W 0.00410868) | 0.118688 ± 0.00262013 (W 0.00269116) | 🔴 tlinalg-1lane 7.62× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n8/b1024` | 2.262 ± 0.00992288 (W 0.0114047) | 0.28849 ± 0.00377799 (W 0.00227125) | 🔴 tlinalg-1lane 7.84× slower than `tlinalg-pool` |  |
| `householder_apply/n16/b1024` | 5.55637 ± 0.103586 (W 0.0150257) | 0.628277 ± 0.00755659 (W 0.00358075) | 🔴 tlinalg-1lane 8.84× slower than `tlinalg-pool` |  |
| `householder_apply/n32/b1024` | 27.6293 ± 0.252139 (W 0.0460723) | 3.50438 ± 0.0138348 (W 0.0135921) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `householder_apply/n4/b1024` | 0.392699 ± 0.00893044 (W 0.00270337) | 0.0517825 ± 0.00125398 (W 0.000178476) | 🔴 tlinalg-1lane 7.58× slower than `tlinalg-pool` |  |
| `householder_apply/n8/b1024` | 1.21038 ± 0.0180582 (W 0.00365588) | 0.152191 ± 0.00173001 (W 0.00200301) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `householder_factor/n16/b1024` | 4.81899 ± 0.0277782 (W 0.0165255) | 0.607811 ± 0.0086288 (W 0.00296049) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `householder_factor/n32/b1024` | 20.3651 ± 0.231054 (W 0.0165742) | 2.58815 ± 0.00630614 (W 0.00793076) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.598907 ± 0.00572545 (W 0.00328803) | 0.0789025 ± 0.000233924 (W 0.000264616) | 🔴 tlinalg-1lane 7.59× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.58249 ± 0.00112833 (W 0.00199674) | 0.203464 ± 0.00138985 (W 0.00160078) | 🔴 tlinalg-1lane 7.78× slower than `tlinalg-pool` |  |
| `lu/n16/b1024` | 3.32176 ± 0.041246 (W 0.0272603) | 0.442744 ± 0.00321664 (W 0.00749766) | 🔴 tlinalg-1lane 7.50× slower than `tlinalg-pool` |  |
| `lu/n32/b1024` | 14.9569 ± 0.0427859 (W 0.0414373) | 2.16555 ± 0.00775342 (W 0.0115644) | 🔴 tlinalg-1lane 6.91× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.365368 ± 0.00272097 (W 0.00300299) | 0.0633085 ± 0.000539309 (W 0.000682587) | 🔴 tlinalg-1lane 5.77× slower than `tlinalg-pool` |  |
| `lu/n8/b1024` | 0.950569 ± 0.00583529 (W 0.00847487) | 0.135986 ± 0.00106466 (W 0.00251411) | 🔴 tlinalg-1lane 6.99× slower than `tlinalg-pool` |  |
| `lu_factor/n16/b1024` | 2.15059 ± 0.0385855 (W 0.00591663) | 0.283028 ± 0.00420529 (W 0.00148772) | 🔴 tlinalg-1lane 7.60× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 9.82913 ± 0.0298877 (W 0.0197885) | 1.24296 ± 0.0139209 (W 0.00367804) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `lu_factor/n4/b1024` | 0.289491 ± 0.00194583 (W 0.00236056) | 0.0620865 ± 0.00117632 (W 0.0008339) | 🔴 tlinalg-1lane 4.66× slower than `tlinalg-pool` |  |
| `lu_factor/n8/b1024` | 0.708804 ± 0.0110046 (W 0.00366876) | 0.102968 ± 0.0023637 (W 0.00156562) | 🔴 tlinalg-1lane 6.88× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 3.51095 ± 0.0490205 (W 0.0090668) | 0.453072 ± 0.0048761 (W 0.00334839) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 13.517 ± 0.07813 (W 0.0126448) | 1.71451 ± 0.00919679 (W 0.00602896) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n4/b1024` | 0.456199 ± 0.00332448 (W 0.00331504) | 0.0727255 ± 0.00135844 (W 0.000676138) | 🔴 tlinalg-1lane 6.27× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n8/b1024` | 1.19613 ± 0.0137258 (W 0.00273542) | 0.15773 ± 0.00117848 (W 0.00191939) | 🔴 tlinalg-1lane 7.58× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 1.35571 ± 0.0106795 (W 0.00490564) | 0.184124 ± 0.00218684 (W 0.00134483) | 🔴 tlinalg-1lane 7.36× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 6.86552 ± 0.0714994 (W 0.0301493) | 0.939333 ± 0.00963784 (W 0.0124752) | 🔴 tlinalg-1lane 7.31× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n4/b1024` | 0.176455 ± 0.000765631 (W 0.00199462) | 0.033978 ± 0.000302326 (W 0.000405034) | 🔴 tlinalg-1lane 5.19× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n8/b1024` | 0.500232 ± 0.00710698 (W 0.0031523) | 0.0760175 ± 0.000182671 (W 0.00169845) | 🔴 tlinalg-1lane 6.58× slower than `tlinalg-pool` |  |
| `qr/n16/b1024` | 11.1791 ± 0.0670875 (W 0.012904) | 1.40611 ± 0.00523828 (W 0.00481913) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 71.7039 ± 0.421098 (W 0.059286) | 8.93241 ± 0.0662829 (W 0.0108604) | 🔴 tlinalg-1lane 8.03× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.933366 ± 0.00695303 (W 0.00163928) | 0.120058 ± 0.00111786 (W 0.000669157) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.72505 ± 0.0258193 (W 0.00530172) | 0.342433 ± 0.00199048 (W 0.00251128) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 12.596 ± 0.0700264 (W 0.0197643) | 1.58619 ± 0.0113445 (W 0.00336078) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 67.0404 ± 0.288876 (W 0.0455975) | 8.43201 ± 0.0325196 (W 0.0142625) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.51263 ± 0.0206142 (W 0.00255275) | 0.194875 ± 0.00292921 (W 0.00164045) | 🔴 tlinalg-1lane 7.76× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n8/b1024` | 3.88745 ± 0.0123452 (W 0.00521444) | 0.492556 ± 0.00410607 (W 0.00245592) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `solve/n16/b1024` | 3.92546 ± 0.0395587 (W 0.00714371) | 0.502991 ± 0.0049424 (W 0.00230284) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` |  |
| `solve/n32/b1024` | 14.4318 ± 0.0583992 (W 0.0158539) | 1.84476 ± 0.0139515 (W 0.0034312) | 🔴 tlinalg-1lane 7.82× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.629698 ± 0.0103083 (W 0.00337184) | 0.082674 ± 0.000958606 (W 0.000886017) | 🔴 tlinalg-1lane 7.62× slower than `tlinalg-pool` |  |
| `solve/n8/b1024` | 1.43473 ± 0.00711314 (W 0.00915072) | 0.18492 ± 0.000607923 (W 0.00149538) | 🔴 tlinalg-1lane 7.76× slower than `tlinalg-pool` |  |
| `svd_full/n16/b1024` | 57.7402 ± 0.467004 (W 0.0388564) | 7.22931 ± 0.15502 (W 0.0099396) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 246.361 ± 1.06191 (W 0.385223) | 31.0429 ± 0.284233 (W 0.0435566) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `svd_full/n4/b1024` | 5.2355 ± 0.0160379 (W 0.00811481) | 0.661181 ± 0.00504798 (W 0.00200157) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 16.5342 ± 0.0242796 (W 0.0134403) | 2.10683 ± 0.0249002 (W 0.00427323) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `svd_thin/n16/b1024` | 57.7949 ± 0.178256 (W 0.330102) | 7.25694 ± 0.102446 (W 0.0074772) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `svd_thin/n32/b1024` | 245.974 ± 0.713985 (W 0.444368) | 31.0439 ± 0.338167 (W 0.0243581) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `svd_thin/n4/b1024` | 5.23331 ± 0.00779485 (W 0.00519314) | 0.677936 ± 0.0350737 (W 0.0017882) | 🔴 tlinalg-1lane 7.72× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 16.5213 ± 0.0415848 (W 0.0785085) | 2.13234 ± 0.0534661 (W 0.00464835) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `svd_values/n16/b1024` | 25.622 ± 0.0526437 (W 0.0158991) | 3.2085 ± 0.0234414 (W 0.00277774) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 90.6482 ± 0.419792 (W 0.0833006) | 11.4469 ± 0.057231 (W 0.0177248) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 3.53501 ± 0.0206521 (W 0.00623745) | 0.448059 ± 0.00293904 (W 0.00213503) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 9.15925 ± 0.0293712 (W 0.0105678) | 1.1539 ± 0.0058777 (W 0.00166669) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 1.02693 ± 0.0152713 (W 0.00528121) | 0.129217 ± 0.00163603 (W 0.00172495) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `triangular_solve/n32/b1024` | 4.27327 ± 0.0420663 (W 0.0147631) | 0.539872 ± 0.00224006 (W 0.00442122) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `triangular_solve/n4/b1024` | 0.172242 ± 0.00105772 (W 0.00128183) | 0.0239945 ± 0.000162656 (W 0.00101274) | 🔴 tlinalg-1lane 7.18× slower than `tlinalg-pool` |  |
| `triangular_solve/n8/b1024` | 0.414199 ± 0.0078952 (W 0.00355543) | 0.054852 ± 0.00106515 (W 0.000402374) | 🔴 tlinalg-1lane 7.55× slower than `tlinalg-pool` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0669 ± 0.00212853 (W 9.57283e-05) | 0.0690595 ± 0.00196527 (W 0.00161333) | · | `!` between-start range over 5% |
| `lu/n128/b1` | 0.168801 ± 0.00110254 (W 0.0016513) | 0.173409 ± 0.00165156 (W 0.00166176) | · |  |
| `lu_factor/n128/b1` | 0.0955385 ± 0.000667572 (W 0.00203813) | 0.093059 ± 0.00116777 (W 0.00030513) | · |  |
| `lu_factor_solve/n128/b1` | 0.104777 ± 0.000945151 (W 0.00178702) | 0.103918 ± 0.000677575 (W 0.000433825) | · |  |
| `lu_solve_prepared/n128/b1` | 0.009964 ± 7.14143e-05 (W 5.69318e-05) | 0.011351 ± 6.20134e-05 (W 3.03041e-05) | 🔵 tlinalg-1lane 1.14× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.112991 ± 0.000793057 (W 0.000115658) | 0.118311 ± 0.000839641 (W 0.00132211) | · |  |
| `svd_values/n128/b1` | 1.05009 ± 0.00180357 (W 0.00322754) | 1.14114 ± 0.00505631 (W 0.00243071) | 🔵 tlinalg-1lane 1.09× faster than `tlinalg-pool` |  |
| `triangular_solve/n128/b1` | 0.006918 ± 6.0208e-05 (W 4.47201e-05) | 0.00801 ± 8.05828e-05 (W 5.02259e-05) | 🔵 tlinalg-1lane 1.16× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.177813 ± 0.000227549 (W 0.00202236) | 0.156769 ± 0.00229206 (W 0.00151937) | 🔴 tlinalg-1lane 1.13× slower than `tlinalg-pool` |  |
| `lu/n128/b1` | 0.358216 ± 0.00334689 (W 0.00334171) | 0.314957 ± 0.00196992 (W 0.00385947) | 🔴 tlinalg-1lane 1.14× slower than `tlinalg-pool` |  |
| `lu_factor/n128/b1` | 0.273166 ± 0.00287235 (W 0.00254956) | 0.2254 ± 0.00111694 (W 0.00173016) | 🔴 tlinalg-1lane 1.21× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n128/b1` | 0.304059 ± 0.00127159 (W 0.00224354) | 0.258043 ± 0.0021565 (W 0.0019576) | 🔴 tlinalg-1lane 1.18× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n128/b1` | 0.0317295 ± 0.000113946 (W 0.000106186) | 0.033873 ± 0.000224512 (W 0.000816128) | 🔵 tlinalg-1lane 1.07× faster than `tlinalg-pool` |  |
| `solve/n128/b1` | 0.314994 ± 0.00120712 (W 0.00282996) | 0.282965 ± 0.00211172 (W 0.00220004) | 🔴 tlinalg-1lane 1.11× slower than `tlinalg-pool` |  |
| `svd_values/n128/b1` | 1.7639 ± 0.00335475 (W 0.00795172) | 1.43433 ± 0.00532239 (W 0.00249503) | 🔴 tlinalg-1lane 1.23× slower than `tlinalg-pool` |  |
| `triangular_solve/n128/b1` | 0.0189055 ± 0.000105894 (W 0.000104426) | 0.0201325 ± 0.000212715 (W 0.000137296) | 🔵 tlinalg-1lane 1.06× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 56.8057 ± 0.286211 (W 0.247835) | 27.3049 ± 0.0240236 (W 0.0169525) | 🔴 tlinalg-1lane 2.08× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 23.4726 ± 0.267259 (W 0.0276072) | 16.2183 ± 0.0475803 (W 0.0159732) | 🔴 tlinalg-1lane 1.45× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 10.2447 ± 0.0567724 (W 0.0103856) | 1.59405 ± 0.0026899 (W 0.00323868) | 🔴 tlinalg-1lane 6.43× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 7.10544 ± 0.0306333 (W 0.0105699) | 1.84575 ± 0.00981167 (W 0.00475265) | 🔴 tlinalg-1lane 3.85× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 19.1257 ± 0.135494 (W 0.0196129) | 5.49195 ± 0.0122292 (W 0.0103794) | 🔴 tlinalg-1lane 3.48× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 29.6834 ± 0.128296 (W 0.0304971) | 7.28305 ± 0.0143347 (W 0.0174838) | 🔴 tlinalg-1lane 4.08× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 107.282 ± 0.840718 (W 0.284136) | 38.5445 ± 0.10678 (W 0.0209864) | 🔴 tlinalg-1lane 2.78× slower than `tlinalg-pool` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 113.9 ± 0.0547224 (W 0.0797068) | 37.0025 ± 0.0375861 (W 0.20581) | 🔴 tlinalg-1lane 3.08× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 49.4074 ± 0.19457 (W 0.0335589) | 20.4494 ± 0.00997976 (W 0.028072) | 🔴 tlinalg-1lane 2.42× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 41.0623 ± 0.0492058 (W 0.0267711) | 5.63233 ± 0.0102797 (W 0.0106328) | 🔴 tlinalg-1lane 7.29× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 27.2316 ± 0.0475866 (W 0.0246958) | 5.17474 ± 0.0169352 (W 0.00942564) | 🔴 tlinalg-1lane 5.26× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 70.0125 ± 0.19024 (W 0.0407955) | 13.3358 ± 0.0380976 (W 0.0166864) | 🔴 tlinalg-1lane 5.25× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 79.3833 ± 0.212833 (W 0.0476459) | 14.2642 ± 0.0349989 (W 0.0122797) | 🔴 tlinalg-1lane 5.57× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 255.569 ± 0.495028 (W 0.964147) | 75.0869 ± 0.050694 (W 0.0986574) | 🔴 tlinalg-1lane 3.40× slower than `tlinalg-pool` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 23.1538 ± 0.352265 (W 0.0351949) | 5.92498 ± 0.0144641 (W 0.0270192) | 🔴 tlinalg-1lane 3.91× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 65.0536 ± 0.0326541 (W 0.0780722) | 22.1582 ± 0.0876764 (W 0.0477128) | 🔴 tlinalg-1lane 2.94× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 101.263 ± 0.727538 (W 0.356657) | 21.4538 ± 0.140407 (W 0.0578058) | 🔴 tlinalg-1lane 4.72× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 99.7401 ± 0.364976 (W 0.257105) | 35.0016 ± 0.0365897 (W 0.0532894) | 🔴 tlinalg-1lane 2.85× slower than `tlinalg-pool` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 85.6167 ± 0.0622036 (W 0.171229) | 17.444 ± 0.0747473 (W 0.0344407) | 🔴 tlinalg-1lane 4.91× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 234.404 ± 0.292511 (W 0.443775) | 58.543 ± 0.0484898 (W 0.0761094) | 🔴 tlinalg-1lane 4.00× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 348.83 ± 2.57016 (W 0.75279) | 59.746 ± 0.187146 (W 0.141795) | 🔴 tlinalg-1lane 5.84× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 363.38 ± 0.258475 (W 0.333036) | 108.807 ± 0.0741426 (W 0.256627) | 🔴 tlinalg-1lane 3.34× slower than `tlinalg-pool` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
