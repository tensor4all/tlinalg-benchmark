# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `4dcd35f080a6b4fd6b1423871af66a33fd398482`
- features: `tlinalg-bench/link-mkl`
- faer provider: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `72c74338818d51cf4a3ba0a1c097c2f4006f28cf`
- toolkit commit: `40e7e11c031788543163d3251b51ee24af72162c`
- measured binary SHA-256: `1cc3ca9b16c76de0b3c25d4c027be838f28ec38f401c14c3a62df4b7006e20ec`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T12:14:38.041719Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor mkl --aa 4 --reps 5 --prime-ms 250 --label split-competition-mkl`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261020T113024Z-split-competition-mkl/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: The batched regime stops at n=32: at batch 1024 the harness's verify recomputes every case with its residual checks, and n=64 pushed one verify pass past 45 minutes on this host (measured 2026-10-20). n=64 returns when verify can run on a declared grid of its own (campaign-toolkit#28), not as part of the timing run.
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
    As measured: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
  - `lapack-mkl` — The same provider against Intel oneAPI MKL, linked from the installation `MKLROOT` names. One binary links one vendor library, so this row is measured by its own build of the harness and recorded as its own run; no page carries two vendor arms. The interface and threading layers are pinned by the harness before the first MKL call, because MKL otherwise lets the environment choose them and the interface layer is an ABI.
    Identity: the MKL build recorded in this run's manifest (`providers[mkl]`)
    Caveat: MKL reports no dispatched-kernel name and no processor count, so its manifest records neither rather than inferring them. Its threading is vendor-owned, as for OpenBLAS.
    As measured: linked shared; mkl 2026.1; kernel not reported by the vendor; openmp threading; config `Intel(R) oneAPI Math Kernel Library Version 2026.1-Product Build 20260612 for Intel(R) 64 architecture applications`

## Hardware

- CPU: `AMD Ryzen AI 9 HX 470`
- logical CPUs: `24`
- L3: `24 MiB (2 instances)`
- L3 domains: `0-3: 16 MiB shared; 4-11: 8 MiB shared`
- OS / arch: `Linux 7.0.0-38-generic` / `x86_64`
- hostname: `shinaoka-EVO-X1Pro`
- CPU sets: 8T -> `4`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 4 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.05%, worst 40.74% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 30 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.32%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
`🔵 tlinalg X faster than <row>` / `🔴 tlinalg X slower than <row>` (the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

## batch-small, f64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.909638 ± 0.0209445 (W 0.00580284) | 1.06446 ± 0.00876258 (W 0.00206916) | 🔵 tlinalg 1.17× faster than `lapack-mkl` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 3.49387 ± 0.135961 (W 0.0124661) | 3.71123 ± 0.0235686 (W 0.0119374) | 🔵 tlinalg 1.06× faster than `lapack-mkl` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.18329 ± 0.00379986 (W 0.0016765) | 0.124183 ± 0.00230292 (W 0.000154144) | 🔴 tlinalg 1.48× slower than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.369647 ± 0.000718771 (W 0.00158981) | 0.326109 ± 0.0045623 (W 0.00255771) | 🔴 tlinalg 1.13× slower than `lapack-mkl` |  |
| `eig/n16/b1024` | 93.6996 ± 0.0458958 (W 0.275384) | 52.8404 ± 0.106721 (W 0.0446985) | 🔴 tlinalg 1.77× slower than `lapack-mkl` |  |
| `eig/n32/b1024` | 423.487 ± 0.346127 (W 0.552541) | 284.623 ± 0.386629 (W 0.333747) | 🔴 tlinalg 1.49× slower than `lapack-mkl` |  |
| `eig/n4/b1024` | 6.19162 ± 0.00787418 (W 0.0162967) | 2.83699 ± 0.012934 (W 0.00363264) | 🔴 tlinalg 2.18× slower than `lapack-mkl` |  |
| `eig/n8/b1024` | 23.3245 ± 0.0284501 (W 0.033688) | 11.6262 ± 0.0327193 (W 0.0291581) | 🔴 tlinalg 2.01× slower than `lapack-mkl` |  |
| `eigh/n16/b1024` | 29.8944 ± 0.131191 (W 0.0364685) | 23.5198 ± 0.0462601 (W 0.033077) | 🔴 tlinalg 1.27× slower than `lapack-mkl` |  |
| `eigh/n32/b1024` | 113.238 ± 0.25975 (W 0.23174) | 227.635 ± 1.57983 (W 0.318688) | 🔵 tlinalg 2.01× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 2.47422 ± 0.00825856 (W 0.00386234) | 2.80456 ± 0.0161471 (W 0.0061817) | 🔵 tlinalg 1.13× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 8.52529 ± 0.0316729 (W 0.0184475) | 7.72598 ± 0.0468063 (W 0.00985288) | 🔴 tlinalg 1.10× slower than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 64.8566 ± 0.0777299 (W 0.0407531) | 36.5463 ± 0.062852 (W 0.227778) | 🔴 tlinalg 1.77× slower than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 287.9 ± 0.205508 (W 0.28213) | 169.307 ± 0.492159 (W 0.238156) | 🔴 tlinalg 1.70× slower than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 3.21705 ± 0.0241768 (W 0.0250633) | 2.11895 ± 0.00975056 (W 0.00228228) | 🔴 tlinalg 1.52× slower than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 15.3358 ± 0.0671017 (W 0.0251619) | 8.95775 ± 0.0257941 (W 0.0299159) | 🔴 tlinalg 1.71× slower than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 22.071 ± 0.0212439 (W 0.027142) | 12.961 ± 0.0335578 (W 0.0163181) | 🔴 tlinalg 1.70× slower than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 85.8215 ± 0.207119 (W 0.0548652) | 43.1811 ± 0.0922835 (W 0.0339321) | 🔴 tlinalg 1.99× slower than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 1.96066 ± 0.00923076 (W 0.00445072) | 1.46175 ± 0.0142695 (W 0.00312733) | 🔴 tlinalg 1.34× slower than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 6.78815 ± 0.00888077 (W 0.0128734) | 4.41516 ± 0.016049 (W 0.0073385) | 🔴 tlinalg 1.54× slower than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 3.51207 ± 0.00753333 (W 0.0128058) | 3.91382 ± 0.0396056 (W 0.0113862) | 🔵 tlinalg 1.11× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 13.9852 ± 0.0504719 (W 0.0387376) | 26.3145 ± 0.0952051 (W 0.0365586) | 🔵 tlinalg 1.88× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.402735 ± 0.00501987 (W 0.00479545) | 0.405683 ± 0.0110902 (W 0.00243023) | · | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 1.06191 ± 0.0113391 (W 0.00660085) | 0.984611 ± 0.0159922 (W 0.00235111) | 🔴 tlinalg 1.08× slower than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 3.43086 ± 0.0249821 (W 0.0095675) | 5.83748 ± 0.0472133 (W 0.0155128) | 🔵 tlinalg 1.70× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 11.3039 ± 0.16019 (W 0.0377673) | 29.6039 ± 0.0698083 (W 0.0429468) | 🔵 tlinalg 2.62× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.524511 ± 0.00534478 (W 0.00380085) | 1.12839 ± 0.00994994 (W 0.00429891) | 🔵 tlinalg 2.15× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 1.30093 ± 0.00604905 (W 0.00836564) | 1.95362 ± 0.0133567 (W 0.00899644) | 🔵 tlinalg 1.50× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 4.75549 ± 0.0670983 (W 0.0163104) | 2.70336 ± 0.0435637 (W 0.0219223) | 🔴 tlinalg 1.76× slower than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 19.1137 ± 0.424789 (W 0.0554318) | 13.1731 ± 0.159186 (W 0.125239) | 🔴 tlinalg 1.45× slower than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.374362 ± 0.00960139 (W 0.00327664) | 0.328217 ± 0.00578415 (W 0.00231007) | 🔴 tlinalg 1.14× slower than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.20585 ± 0.0301472 (W 0.00570964) | 0.803611 ± 0.00301287 (W 0.00672436) | 🔴 tlinalg 1.50× slower than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 3.64924 ± 0.0318073 (W 0.014368) | 2.95992 ± 0.00950511 (W 0.00474043) | 🔴 tlinalg 1.23× slower than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 12.6782 ± 0.091134 (W 0.0316979) | 12.3782 ± 0.0626632 (W 0.0332489) | · |  |
| `householder_factor/n4/b1024` | 0.462035 ± 0.00878415 (W 0.00314554) | 0.306604 ± 0.00162406 (W 0.00174732) | 🔴 tlinalg 1.51× slower than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 1.21044 ± 0.0130501 (W 0.00584188) | 0.846291 ± 0.00308501 (W 0.00190616) | 🔴 tlinalg 1.43× slower than `lapack-mkl` |  |
| `lu/n16/b1024` | 2.65718 ± 0.0424851 (W 0.0120172) | 1.72426 ± 0.0576799 (W 0.00524702) | 🔴 tlinalg 1.54× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 9.00527 ± 0.0505654 (W 0.0538061) | 11.7806 ± 0.069001 (W 0.0435619) | 🔵 tlinalg 1.31× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.302968 ± 0.00536741 (W 0.00338633) | 0.169087 ± 0.000768805 (W 0.00131417) | 🔴 tlinalg 1.79× slower than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.838006 ± 0.0321676 (W 0.00720414) | 0.501453 ± 0.00363623 (W 0.00227054) | 🔴 tlinalg 1.67× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 1.84427 ± 0.0287086 (W 0.00319579) | 1.19878 ± 0.0355062 (W 0.00100395) | 🔴 tlinalg 1.54× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 5.72426 ± 0.0314868 (W 0.0242352) | 9.01442 ± 0.0321508 (W 0.0113978) | 🔵 tlinalg 1.57× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.222081 ± 0.000259295 (W 0.00261906) | 0.0655385 ± 0.00380186 (W 0.000777188) | 🔴 tlinalg 3.39× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.599749 ± 0.0185742 (W 0.00881172) | 0.262691 ± 0.00169164 (W 0.0026692) | 🔴 tlinalg 2.28× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n16/b1024` | 2.46306 ± 0.0204494 (W 0.0151979) | 2.36867 ± 0.040824 (W 0.00508771) | · |  |
| `lu_factor_solve/n32/b1024` | 6.90503 ± 0.0534105 (W 0.0163847) | 28.4521 ± 0.111653 (W 0.0462508) | 🔵 tlinalg 4.12× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.281153 ± 0.00338637 (W 0.00201941) | 0.182166 ± 0.00158406 (W 0.000742482) | 🔴 tlinalg 1.54× slower than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.832499 ± 0.00694535 (W 0.0106369) | 0.827492 ± 0.00311087 (W 0.0027433) | · |  |
| `lu_solve_prepared/n16/b1024` | 0.647177 ± 0.00339582 (W 0.00369811) | 1.06519 ± 0.00388825 (W 0.00411719) | 🔵 tlinalg 1.65× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 2.26167 ± 0.164999 (W 0.0345024) | 19.3512 ± 0.083048 (W 0.0323622) | 🔵 tlinalg 8.56× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.0730885 ± 0.000380143 (W 0.00104361) | 0.133821 ± 0.00138381 (W 0.000870503) | 🔵 tlinalg 1.83× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.235741 ± 0.0043357 (W 0.00145963) | 0.587655 ± 0.00293509 (W 0.00230963) | 🔵 tlinalg 2.49× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 8.88516 ± 0.208438 (W 0.0282346) | 5.27638 ± 0.0175732 (W 0.0170693) | 🔴 tlinalg 1.68× slower than `lapack-mkl` | `!` between-start range over 5% |
| `qr/n32/b1024` | 35.3631 ± 0.051671 (W 0.0374076) | 21.1984 ± 0.115815 (W 0.0503254) | 🔴 tlinalg 1.67× slower than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.791574 ± 0.00246582 (W 0.00411696) | 0.722063 ± 0.00123212 (W 0.00334819) | 🔴 tlinalg 1.10× slower than `lapack-mkl` |  |
| `qr/n8/b1024` | 2.38403 ± 0.00891911 (W 0.00676257) | 1.70522 ± 0.0110173 (W 0.00557414) | 🔴 tlinalg 1.40× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 10.2037 ± 0.141733 (W 0.0330485) | 8.33776 ± 0.0189426 (W 0.0262112) | 🔴 tlinalg 1.22× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 35.7012 ± 0.0761313 (W 0.0880602) | 31.2028 ± 0.0453936 (W 0.0420347) | 🔴 tlinalg 1.14× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 1.20502 ± 0.0054726 (W 0.00553496) | 1.23254 ± 0.00196182 (W 0.00450048) | · |  |
| `rank_revealing_qr/n8/b1024` | 3.20898 ± 0.0657918 (W 0.00792809) | 2.92006 ± 0.016471 (W 0.00655694) | 🔴 tlinalg 1.10× slower than `lapack-mkl` |  |
| `solve/n16/b1024` | 2.68822 ± 0.0398454 (W 0.00842905) | 2.47986 ± 0.0544035 (W 0.00708904) | 🔴 tlinalg 1.08× slower than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 7.21189 ± 0.0683727 (W 0.0257408) | 28.4849 ± 0.140524 (W 0.0335165) | 🔵 tlinalg 3.95× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.373808 ± 0.0042016 (W 0.0036616) | 0.229803 ± 0.00112176 (W 0.00172816) | 🔴 tlinalg 1.63× slower than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.958905 ± 0.00729957 (W 0.0060913) | 0.890948 ± 0.00597015 (W 0.00208387) | 🔴 tlinalg 1.08× slower than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 55.9832 ± 0.0802078 (W 0.23858) | 51.5323 ± 0.087858 (W 0.0567016) | 🔴 tlinalg 1.09× slower than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 202.824 ± 0.759325 (W 0.572304) | 371.43 ± 0.656647 (W 0.294781) | 🔵 tlinalg 1.83× faster than `lapack-mkl` |  |
| `svd_full/n4/b1024` | 4.31945 ± 0.0112493 (W 0.0211173) | 6.10183 ± 0.0226407 (W 0.0110565) | 🔵 tlinalg 1.41× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 15.1978 ± 0.0185444 (W 0.0227538) | 18.608 ± 0.0608666 (W 0.0260337) | 🔵 tlinalg 1.22× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 56.0034 ± 0.40005 (W 0.402464) | 51.6174 ± 0.1024 (W 0.246477) | 🔴 tlinalg 1.08× slower than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 202.962 ± 0.763279 (W 0.706702) | 372.03 ± 1.07282 (W 0.64348) | 🔵 tlinalg 1.83× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1024` | 4.31317 ± 0.0239302 (W 0.014048) | 6.11292 ± 0.0314607 (W 0.0160514) | 🔵 tlinalg 1.42× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 15.1685 ± 0.0286631 (W 0.0349112) | 18.6157 ± 0.0723612 (W 0.0327003) | 🔵 tlinalg 1.23× faster than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 40.9012 ± 0.0354867 (W 0.0359682) | 19.2917 ± 0.0337558 (W 0.0259116) | 🔴 tlinalg 2.12× slower than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 159.157 ± 0.728551 (W 0.235147) | 64.8165 ± 0.312083 (W 0.0445632) | 🔴 tlinalg 2.46× slower than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 3.20996 ± 0.00604987 (W 0.0112593) | 2.6804 ± 0.00841688 (W 0.00288872) | 🔴 tlinalg 1.20× slower than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 11.318 ± 0.0214443 (W 0.0206982) | 6.72926 ± 0.0186323 (W 0.0107272) | 🔴 tlinalg 1.68× slower than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.537302 ± 0.00343971 (W 0.00309445) | 0.594618 ± 0.00356945 (W 0.00344297) | 🔵 tlinalg 1.11× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 1.50265 ± 0.0133978 (W 0.0234386) | 10.0951 ± 0.0117102 (W 0.0225092) | 🔵 tlinalg 6.72× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.097113 ± 0.00387792 (W 0.0015992) | 0.299619 ± 0.00216322 (W 0.00258401) | 🔵 tlinalg 3.09× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.223496 ± 0.00391196 (W 0.00191854) | 0.400278 ± 0.00320793 (W 0.00215393) | 🔵 tlinalg 1.79× faster than `lapack-mkl` |  |

## batch-small, c64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 1.35644 ± 0.0128451 (W 0.0080624) | 1.83319 ± 0.0254096 (W 0.0105165) | 🔵 tlinalg 1.35× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 5.97961 ± 0.0283468 (W 0.0174748) | 8.91064 ± 0.0288241 (W 0.0209607) | 🔵 tlinalg 1.49× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.211588 ± 0.00509378 (W 0.00189018) | 0.176874 ± 0.00072028 (W 0.00152313) | 🔴 tlinalg 1.20× slower than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.46278 ± 0.0215181 (W 0.00339386) | 0.473221 ± 0.00371478 (W 0.00253451) | · | `!` between-start range over 5% |
| `eig/n16/b1024` | 129.618 ± 0.112982 (W 0.285239) | 226.637 ± 0.143104 (W 0.404403) | 🔵 tlinalg 1.75× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 536.65 ± 0.258971 (W 0.529215) | 1003.2 ± 2.16536 (W 1.06315) | 🔵 tlinalg 1.87× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 10.1842 ± 0.0394607 (W 0.0218208) | 12.4643 ± 0.0189364 (W 0.0274579) | 🔵 tlinalg 1.22× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 35.1127 ± 0.0387268 (W 0.0421999) | 43.3335 ± 0.0522785 (W 0.0480806) | 🔵 tlinalg 1.23× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 32.3934 ± 0.03965 (W 0.0523913) | 32.3571 ± 0.0504726 (W 0.0338071) | · |  |
| `eigh/n32/b1024` | 141.404 ± 0.183103 (W 0.242026) | 152.311 ± 0.297349 (W 0.420008) | 🔵 tlinalg 1.08× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 2.9635 ± 0.00193897 (W 0.00260761) | 2.82693 ± 0.0369606 (W 0.00326856) | · |  |
| `eigh/n8/b1024` | 9.14031 ± 0.00419934 (W 0.0174258) | 8.96115 ± 0.0678524 (W 0.0193213) | · |  |
| `eigvals/n16/b1024` | 77.1046 ± 0.0532951 (W 0.259324) | 124.958 ± 0.0849516 (W 0.107964) | 🔵 tlinalg 1.62× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 338.251 ± 0.154771 (W 0.416775) | 523.631 ± 0.408135 (W 0.467433) | 🔵 tlinalg 1.55× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 4.79991 ± 0.0278928 (W 0.00868507) | 9.57232 ± 0.00291642 (W 0.0168261) | 🔵 tlinalg 1.99× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 19.8 ± 0.0247873 (W 0.0292592) | 34.3725 ± 0.0280589 (W 0.0416591) | 🔵 tlinalg 1.74× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 23.907 ± 0.0515533 (W 0.0272979) | 18.3904 ± 0.03406 (W 0.0229587) | 🔴 tlinalg 1.30× slower than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 93.4444 ± 0.206762 (W 0.053675) | 77.4498 ± 0.109084 (W 0.0595211) | 🔴 tlinalg 1.21× slower than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 2.41405 ± 0.0163054 (W 0.00559762) | 1.78451 ± 0.00983491 (W 0.00224636) | 🔴 tlinalg 1.35× slower than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 7.34343 ± 0.0212544 (W 0.0134651) | 5.58029 ± 0.00994051 (W 0.00573579) | 🔴 tlinalg 1.32× slower than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 4.33001 ± 0.0107026 (W 0.0165279) | 5.62458 ± 0.024274 (W 0.0247463) | 🔵 tlinalg 1.30× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 19.9624 ± 0.0164573 (W 0.0437717) | 27.0582 ± 0.058395 (W 0.0414745) | 🔵 tlinalg 1.36× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.459622 ± 0.00533375 (W 0.00388935) | 0.527866 ± 0.0102947 (W 0.00276454) | 🔵 tlinalg 1.15× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 1.25742 ± 0.0104352 (W 0.0157568) | 1.29783 ± 0.0269631 (W 0.00341237) | · |  |
| `full_piv_lu_solve/n16/b1024` | 5.25135 ± 0.0325371 (W 0.0128499) | 8.45596 ± 0.0144662 (W 0.015309) | 🔵 tlinalg 1.61× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 19.7682 ± 0.1071 (W 0.0495667) | 34.5358 ± 0.102349 (W 0.0556834) | 🔵 tlinalg 1.75× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.769737 ± 0.00989286 (W 0.00448359) | 1.59707 ± 0.0147551 (W 0.0049568) | 🔵 tlinalg 2.07× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 1.91758 ± 0.0123229 (W 0.0111961) | 3.19829 ± 0.0195092 (W 0.00552506) | 🔵 tlinalg 1.67× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 5.10723 ± 0.0196796 (W 0.0140853) | 6.24248 ± 0.104662 (W 0.0298361) | 🔵 tlinalg 1.22× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 25.8465 ± 0.0802537 (W 0.0725842) | 38.1898 ± 0.195753 (W 0.0911338) | 🔵 tlinalg 1.48× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.353955 ± 0.000594265 (W 0.00261898) | 0.417015 ± 0.00479999 (W 0.00345584) | 🔵 tlinalg 1.18× faster than `lapack-mkl` |  |
| `householder_apply/n8/b1024` | 1.13433 ± 0.00900475 (W 0.00497828) | 1.27868 ± 0.010682 (W 0.00676995) | 🔵 tlinalg 1.13× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1024` | 4.45548 ± 0.0238866 (W 0.0156352) | 6.31275 ± 0.0164896 (W 0.0195603) | 🔵 tlinalg 1.42× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 19.6229 ± 0.0149724 (W 0.0284644) | 27.472 ± 0.0698874 (W 0.0525027) | 🔵 tlinalg 1.40× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.554577 ± 0.00460554 (W 0.00284662) | 0.515434 ± 0.00261804 (W 0.00199178) | 🔴 tlinalg 1.08× slower than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 1.43854 ± 0.00324494 (W 0.00679341) | 1.48289 ± 0.00187453 (W 0.00254041) | · |  |
| `lu/n16/b1024` | 3.10403 ± 0.0268527 (W 0.0173557) | 3.52643 ± 0.0421457 (W 0.0142155) | 🔵 tlinalg 1.14× faster than `lapack-mkl` |  |
| `lu/n32/b1024` | 14.0719 ± 0.101956 (W 0.0417908) | 19.5668 ± 0.108048 (W 0.0412519) | 🔵 tlinalg 1.39× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.368837 ± 0.00576646 (W 0.00285131) | 0.283053 ± 0.00102394 (W 0.00176458) | 🔴 tlinalg 1.30× slower than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.958595 ± 0.00561106 (W 0.0100854) | 0.893899 ± 0.0118631 (W 0.00359045) | 🔴 tlinalg 1.07× slower than `lapack-mkl` |  |
| `lu_factor/n16/b1024` | 2.06697 ± 0.019495 (W 0.00597496) | 2.63597 ± 0.00387183 (W 0.00387631) | 🔵 tlinalg 1.28× faster than `lapack-mkl` |  |
| `lu_factor/n32/b1024` | 9.51199 ± 0.0845318 (W 0.0293159) | 15.5605 ± 0.0578511 (W 0.0240168) | 🔵 tlinalg 1.64× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.278622 ± 0.00417521 (W 0.00207443) | 0.183241 ± 0.000775126 (W 0.00142011) | 🔴 tlinalg 1.52× slower than `lapack-mkl` |  |
| `lu_factor/n8/b1024` | 0.691704 ± 0.00249743 (W 0.00365029) | 0.621199 ± 0.0058778 (W 0.00244232) | 🔴 tlinalg 1.11× slower than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 3.51434 ± 0.022889 (W 0.00914028) | 5.34061 ± 0.0305763 (W 0.00963258) | 🔵 tlinalg 1.52× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 13.1658 ± 0.0602835 (W 0.0282727) | 36.1924 ± 0.0124524 (W 0.051814) | 🔵 tlinalg 2.75× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.436125 ± 0.00814234 (W 0.00471818) | 0.41717 ± 0.00174454 (W 0.00215975) | · |  |
| `lu_factor_solve/n8/b1024` | 1.18625 ± 0.00887802 (W 0.00689186) | 1.66508 ± 0.00262489 (W 0.00196738) | 🔵 tlinalg 1.40× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 1.31004 ± 0.0133281 (W 0.00559927) | 2.62933 ± 0.0120347 (W 0.00572095) | 🔵 tlinalg 2.01× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 6.14144 ± 0.0236182 (W 0.0476899) | 21.6051 ± 0.0168942 (W 0.0314407) | 🔵 tlinalg 3.52× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.168401 ± 0.00451341 (W 0.0014304) | 0.243086 ± 0.000229169 (W 0.00165402) | 🔵 tlinalg 1.44× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.491534 ± 0.00428776 (W 0.00393543) | 1.07205 ± 0.00238069 (W 0.0019283) | 🔵 tlinalg 2.18× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 10.9135 ± 0.0352446 (W 0.0178502) | 10.5821 ± 0.0588621 (W 0.0315899) | · |  |
| `qr/n32/b1024` | 72.6386 ± 0.0296103 (W 0.0618865) | 49.8614 ± 0.368663 (W 0.227245) | 🔴 tlinalg 1.46× slower than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.885593 ± 0.0113468 (W 0.00517292) | 0.924992 ± 0.00414632 (W 0.00198502) | · |  |
| `qr/n8/b1024` | 2.65886 ± 0.0095982 (W 0.00576675) | 2.66035 ± 0.0159306 (W 0.00845823) | · |  |
| `rank_revealing_qr/n16/b1024` | 12.1962 ± 0.0620786 (W 0.0264429) | 15.8518 ± 0.0647896 (W 0.0426486) | 🔵 tlinalg 1.30× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 66.9114 ± 0.235979 (W 0.0665152) | 69.7439 ± 0.484746 (W 0.0455864) | · |  |
| `rank_revealing_qr/n4/b1024` | 1.43751 ± 0.00429468 (W 0.00761817) | 1.75638 ± 0.0026355 (W 0.00710421) | 🔵 tlinalg 1.22× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 3.73968 ± 0.0178174 (W 0.012974) | 4.75126 ± 0.0108115 (W 0.00806948) | 🔵 tlinalg 1.27× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 3.89381 ± 0.0191891 (W 0.0106662) | 5.598 ± 0.0333461 (W 0.0126832) | 🔵 tlinalg 1.44× faster than `lapack-mkl` |  |
| `solve/n32/b1024` | 13.8014 ± 0.0703053 (W 0.031315) | 37.1897 ± 0.146161 (W 0.0411868) | 🔵 tlinalg 2.69× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.544784 ± 0.00997305 (W 0.00418597) | 0.480116 ± 0.0024389 (W 0.00315929) | 🔴 tlinalg 1.13× slower than `lapack-mkl` |  |
| `solve/n8/b1024` | 1.36191 ± 0.00524065 (W 0.00540034) | 1.75523 ± 0.00679487 (W 0.00211425) | 🔵 tlinalg 1.29× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 60.8691 ± 0.5031 (W 0.181641) | 67.4992 ± 0.127985 (W 0.049157) | 🔵 tlinalg 1.11× faster than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 261.683 ± 0.593035 (W 0.751791) | 462.689 ± 1.11556 (W 0.502949) | 🔵 tlinalg 1.77× faster than `lapack-mkl` |  |
| `svd_full/n4/b1024` | 5.03154 ± 0.0300857 (W 0.00715445) | 7.39175 ± 0.0183325 (W 0.0159004) | 🔵 tlinalg 1.47× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 16.9254 ± 0.0618001 (W 0.0434074) | 22.1735 ± 0.0259556 (W 0.0216889) | 🔵 tlinalg 1.31× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 60.65 ± 0.135511 (W 0.0959745) | 67.4518 ± 0.125518 (W 0.246569) | 🔵 tlinalg 1.11× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 262.099 ± 1.48821 (W 1.58881) | 463.759 ± 2.82792 (W 0.591855) | 🔵 tlinalg 1.77× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1024` | 5.02427 ± 0.0051405 (W 0.00686353) | 7.41036 ± 0.0174018 (W 0.0151308) | 🔵 tlinalg 1.47× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 16.8814 ± 0.0136187 (W 0.0338846) | 22.1994 ± 0.0481277 (W 0.0410258) | 🔵 tlinalg 1.32× faster than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 45.5528 ± 0.0717496 (W 0.0493568) | 28.2399 ± 0.101206 (W 0.0464961) | 🔴 tlinalg 1.61× slower than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 176.881 ± 0.187115 (W 0.366368) | 106.153 ± 0.542927 (W 0.238414) | 🔴 tlinalg 1.67× slower than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 3.86432 ± 0.0128616 (W 0.00355989) | 3.5106 ± 0.0122671 (W 0.0040853) | 🔴 tlinalg 1.10× slower than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 12.9872 ± 0.0179539 (W 0.020277) | 9.13505 ± 0.0162449 (W 0.0213048) | 🔴 tlinalg 1.42× slower than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 1.05054 ± 0.00636172 (W 0.00773847) | 1.33685 ± 0.00715301 (W 0.00423563) | 🔵 tlinalg 1.27× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 3.8606 ± 0.0218707 (W 0.0210054) | 11.4712 ± 0.052509 (W 0.0192753) | 🔵 tlinalg 2.97× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.170676 ± 0.00119566 (W 0.00114973) | 0.303855 ± 0.00149044 (W 0.00177732) | 🔵 tlinalg 1.78× faster than `lapack-mkl` |  |
| `triangular_solve/n8/b1024` | 0.406501 ± 0.00341539 (W 0.00324005) | 0.581292 ± 0.00128885 (W 0.00290415) | 🔵 tlinalg 1.43× faster than `lapack-mkl` |  |

## canary-factor, f64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.066651 ± 0.000280879 (W 0.00112134) | 0.093322 ± 0.000619085 (W 0.000374871) | 🔵 tlinalg 1.40× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.166768 ± 0.0034059 (W 0.00168092) | 0.136419 ± 0.0006675 (W 0.00158204) | 🔴 tlinalg 1.22× slower than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.106528 ± 0.000408511 (W 0.00125036) | 0.121204 ± 0.000284284 (W 0.00101818) | 🔵 tlinalg 1.14× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.119092 ± 0.00358467 (W 0.00143534) | 0.183605 ± 0.000234915 (W 0.00161469) | 🔵 tlinalg 1.54× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n128/b1` | 0.009924 ± 8.88819e-05 (W 5.00821e-05) | 0.0623735 ± 0.000254018 (W 0.000183378) | 🔵 tlinalg 6.29× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.128746 ± 0.00400588 (W 0.0026785) | 0.188572 ± 0.000511896 (W 0.00179492) | 🔵 tlinalg 1.46× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n128/b1` | 2.37884 ± 0.00462728 (W 0.00485724) | 1.54438 ± 0.0106557 (W 0.00373138) | 🔴 tlinalg 1.54× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.006883 ± 4.43471e-05 (W 9.85915e-05) | 0.0372245 ± 0.000172293 (W 0.000148174) | 🔵 tlinalg 5.41× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.21601 ± 0.00392165 (W 0.00148823) | 0.408357 ± 0.00177213 (W 0.00441043) | 🔵 tlinalg 1.89× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.347062 ± 0.00564207 (W 0.00213023) | 0.454178 ± 0.00323922 (W 0.00284074) | 🔵 tlinalg 1.31× faster than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.275307 ± 0.00104117 (W 0.00146738) | 0.415825 ± 0.00260333 (W 0.00252686) | 🔵 tlinalg 1.51× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.306005 ± 0.000919044 (W 0.00215253) | 0.521143 ± 0.00333039 (W 0.00244134) | 🔵 tlinalg 1.70× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.0314845 ± 3.99208e-05 (W 0.000127107) | 0.101537 ± 0.00023565 (W 0.00094922) | 🔵 tlinalg 3.22× faster than `lapack-mkl` |  |
| `solve/n128/b1` | 0.324153 ± 0.00552952 (W 0.00254901) | 0.532115 ± 0.001391 (W 0.00268979) | 🔵 tlinalg 1.64× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 3.14823 ± 0.00713758 (W 0.00489845) | 7.78172 ± 0.0213368 (W 0.014419) | 🔵 tlinalg 2.47× faster than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.018735 ± 8.85264e-05 (W 0.000127336) | 0.0509705 ± 8.24313e-05 (W 0.000614841) | 🔵 tlinalg 2.72× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 72.9288 ± 3.50888 (W 4.4456) | 99.7885 ± 0.860601 (W 0.0988056) | 🔵 tlinalg 1.37× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigvalsh/n512/b1` | 24.6384 ± 0.110851 (W 0.0344298) | 62.398 ± 0.330106 (W 0.0986596) | 🔵 tlinalg 2.53× faster than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 24.3827 ± 0.0322887 (W 4.33023) | 23.3043 ± 0.201382 (W 0.0636839) | · |  |
| `householder_factor/n512/b1` | 16.5918 ± 0.82366 (W 2.87881) | 675.393 ± 13.4738 (W 13.6524) | 🔵 tlinalg 40.71× faster than `lapack-mkl` | `!` between-start range over 5% |
| `qr/n512/b1` | 41.1794 ± 2.46837 (W 6.98271) | 719.377 ± 6.24483 (W 28.0894) | 🔵 tlinalg 17.47× faster than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/n512/b1` | 43.8779 ± 2.14782 (W 4.16094) | 39.0003 ± 0.147972 (W 0.107821) | 🔴 tlinalg 1.13× slower than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n512/b1` | 169.487 ± 2.99136 (W 4.12906) | 157.649 ± 0.623866 (W 0.413845) | 🔴 tlinalg 1.08× slower than `lapack-mkl` |  |

## canary-decompose, c64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 159.663 ± 3.13498 (W 7.40925) | 306.793 ± 0.439393 (W 0.495927) | 🔵 tlinalg 1.92× faster than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 50.2761 ± 0.0357322 (W 0.0429167) | 125.142 ± 0.184927 (W 0.134161) | 🔵 tlinalg 2.49× faster than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 91.2403 ± 1.78617 (W 4.13642) | 62.5375 ± 0.123639 (W 0.117045) | 🔴 tlinalg 1.46× slower than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 58.4825 ± 2.69143 (W 4.97298) | 725.777 ± 1.4758 (W 2.29031) | 🔵 tlinalg 12.41× faster than `lapack-mkl` | `!` between-start range over 5% |
| `qr/n512/b1` | 141.359 ± 2.47864 (W 8.1515) | 769.424 ± 12.5074 (W 11.7597) | 🔵 tlinalg 5.44× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 121.781 ± 4.65756 (W 6.57466) | 127.443 ± 0.675476 (W 0.82661) | · | `!` between-start range over 5% |
| `svd_thin/n512/b1` | 381.537 ± 9.94341 (W 12.1148) | 344.921 ± 0.346856 (W 0.803288) | 🔴 tlinalg 1.11× slower than `lapack-mkl` | `!` between-start range over 5% |

## canary-rectangular, f64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 39.5335 ± 0.471575 (W 6.53776) | 3628.68 ± 3.43689 (W 14.1613) | 🔵 tlinalg 91.79× faster than `lapack-mkl` |  |
| `qr/4096x256/b1` | 161.633 ± 10.6676 (W 49.3342) | 3658.7 ± 9.61908 (W 22.0156) | 🔵 tlinalg 22.64× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `rank_revealing_qr/4096x256/b1` | 129.497 ± 2.31522 (W 3.85472) | 89.6469 ± 2.77883 (W 0.312504) | 🔴 tlinalg 1.44× slower than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/4096x256/b1` | 193.979 ± 37.0922 (W 47.7216) | 3719.81 ± 14.0313 (W 37.4644) | 🔵 tlinalg 19.18× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |

## canary-rectangular, c64, 8T (CPU 4)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 139.369 ± 4.1198 (W 4.29046) | 3706.43 ± 17.5941 (W 24.9997) | 🔵 tlinalg 26.59× faster than `lapack-mkl` | `!` between-start range over 5% |
| `qr/4096x256/b1` | 387.809 ± 7.2987 (W 16.2937) | 3816.96 ± 10.0739 (W 26.7252) | 🔵 tlinalg 9.84× faster than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 448.977 ± 1.75139 (W 3.07288) | 300.113 ± 0.952137 (W 0.628865) | 🔴 tlinalg 1.50× slower than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 599.455 ± 21.6829 (W 48.5039) | 3984.57 ± 11.6187 (W 37.4394) | 🔵 tlinalg 6.65× faster than `lapack-mkl` | `!` between-start range over 5% |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
