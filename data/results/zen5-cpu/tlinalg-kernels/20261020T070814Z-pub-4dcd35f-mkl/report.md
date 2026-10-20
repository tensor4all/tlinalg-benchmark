# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `4dcd35f080a6b4fd6b1423871af66a33fd398482`
- features: `tlinalg-bench/link-mkl`
- faer provider: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `f233d9d8787bb55df50bf115bbd7f026ddc64f5f`
- toolkit commit: `90fbeeb3dd2389b8a5d9bc63679f5e2bf3fc1741`
- measured binary SHA-256: `1cc3ca9b16c76de0b3c25d4c027be838f28ec38f401c14c3a62df4b7006e20ec`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T07:40:03.699738Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor mkl --aa 3 --reps 5 --prime-ms 250 --label pub-4dcd35f-mkl`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261020T070814Z-pub-4dcd35f-mkl/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: Only the kernel entry points are measured. Tensor construction, dtype dispatch, session entry and pool checkout are tenferro's and are out of scope.
  Known blind spot: The 2026-10-17 trim narrowed the suite to the batched small regime plus three single-shape canaries (factor at 128, decompose at 512, rectangular at 4096x256, each at batch 1). The medium, large and tall grids are no longer measured here: faer-benchmark measures that geometry directly with the same backends these rows wrap, so a cost that appears only at those sizes has to be read from that campaign's page.
  Known blind spot: The small regime declares batch 1 and 1024 and gives up the middle of the axis, so a cost that appears only at an intermediate batch is not covered.
  Known blind spot: The thread axis is 1T and 8T; a budget between them (4T) is not measured, so a scaling curve cannot be read off this page.
  Known blind spot: The providers are compared at the thread budgets declared here; a budget the vendor threads itself by, outside that set, is not covered.
  Known blind spot: A vendor arm records the vendor library, but only OpenBLAS reports the kernel its runtime dispatched to. MKL's manifest records its own version and the threading layer the harness pins; it names no kernel, because MKL exposes none to name.
  Known blind spot: The small and medium regimes give up the middle of their batch axis (small: batch 64 of 1, 64, 1024; medium: batch 16 of 1, 16, 128) and the medium regime also gives up n=64 of 32, 64, 128. A cost that is only visible in the middle of one of those ranges is not covered here. Large and tall declare every shape they measure.
- **Rows** — one row per engine in every table below:
  - `faer-1lane` — The faer-backed provider on one sequential lane: the per-item cost plus the batch loop, with no threading at all. The overhead baseline.
    Identity: tlinalg-rs (this repository's pinned revision)
    As measured: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
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
- CPU sets: 1T -> `4`, 8T -> `4-11`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 3 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.25%, worst 78.79% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 141 of 1390 engine cells exceed 5% and carry `!`; median within-process relative SD 0.65%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
The `vs faer-1lane` column is the rotation-averaged ratio exp(mean over starts of
log(engine median / faer-1lane median)), with the per-start ratios beside it: `R > 1`
means the engine was slower than that first-declared row in that start. It removes a
row-position
effect only under one position effect shared by the engines and stable across starts,
and only where every declared engine has a measured row (`*` marks a cell where one has
no row, so no ratio there is position-balanced). `!` marks a cell where some engine's own
per-start median range exceeds 5% of its median, and `p` a balanced cell whose estimated
position-effect ratio exceeds 1.05. Flagged cells are retained, not discarded; the
between-start variation can exceed the difference being compared.
The `vs` columns mark only differences larger than the spread this run recorded for those
two rows (combined between-start SD, floored at 5%), always with the fork as the subject:
`🔵 fork X faster than <row>` / `🔴 fork X slower than <row>` (the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

## batch-small, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001232 ± 3.4641e-05 (W 3.58092e-05) | - | 0.001212 ± 2.08167e-05 (W 1.1327e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 0.878797 ± 0.0204427 (W 0.002322) | - | 1.05352 ± 0.00998891 (W 0.00195173) | - | 🔵 fork 1.20× faster than `lapack-mkl` | `*` one row has no measurement here |
| `cholesky/n4/b1` | 0.000561 ± 5.7735e-06 (W 3.99149e-05) | - | 0.000311 ± 1.1547e-05 (W 2.57915e-05) | - | 🔴 fork 1.80× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.178402 ± 0.000282236 (W 0.00183352) | - | 0.124663 ± 0.000678535 (W 0.00135624) | - | 🔴 fork 1.43× slower than `lapack-mkl` | `*` one row has no measurement here |
| `cholesky/n8/b1` | 0.000731 ± 3.27159e-05 (W 4.20987e-05) | - | 0.000491 ± 1.1547e-05 (W 1.09545e-05) | - | 🔴 fork 1.49× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.359199 ± 0.00737323 (W 0.00222077) | - | 0.318523 ± 0.00491662 (W 0.00160827) | - | 🔴 fork 1.13× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n16/b1` | 0.089667 ± 9.86425e-05 (W 0.000284079) | - | 0.050584 ± 5.68624e-05 (W 5.57701e-05) | - | 🔴 fork 1.77× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n16/b1024` | 93.642 ± 0.0436079 (W 0.377123) | - | 52.8608 ± 0.0398073 (W 0.0445485) | - | 🔴 fork 1.77× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n4/b1` | 0.006893 ± 0.000115902 (W 0.000136822) | - | 0.003557 ± 2.85832e-05 (W 5.30028e-05) | - | 🔴 fork 1.94× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 6.09713 ± 0.0175253 (W 0.00968556) | - | 2.8371 ± 0.0027791 (W 0.00707989) | - | 🔴 fork 2.15× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n8/b1` | 0.024055 ± 6.55744e-05 (W 0.00014775) | - | 0.012363 ± 1.58219e-05 (W 2.90568e-05) | - | 🔴 fork 1.95× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n8/b1024` | 23.3097 ± 0.0761074 (W 0.0357489) | - | 11.6564 ± 0.02489 (W 0.0267704) | - | 🔴 fork 2.00× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigh/n16/b1` | 0.029455 ± 9.29157e-05 (W 0.000247762) | - | 0.022492 ± 0.000110092 (W 5.80112e-05) | - | 🔴 fork 1.31× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigh/n16/b1024` | 29.6232 ± 0.21603 (W 0.041131) | - | 23.5732 ± 0.0695076 (W 0.0179495) | - | 🔴 fork 1.26× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigh/n4/b1` | 0.002895 ± 1.12694e-05 (W 7.8653e-05) | - | 0.003126 ± 1.73205e-05 (W 2.38747e-05) | - | 🔵 fork 1.08× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.41208 ± 0.0119366 (W 0.00721604) | - | 2.87096 ± 0.0122626 (W 0.00763997) | - | 🔵 fork 1.19× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigh/n8/b1` | 0.008757 ± 6.97878e-05 (W 5.80973e-05) | - | 0.007865 ± 5.22526e-05 (W 4.1833e-05) | - | 🔴 fork 1.11× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 8.42398 ± 0.0170645 (W 0.017347) | - | 7.78828 ± 0.0258748 (W 0.00761363) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvals/n16/b1` | 0.061865 ± 0.000113578 (W 0.000120284) | - | 0.035306 ± 0.000113725 (W 0.000137586) | - | 🔴 fork 1.75× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvals/n16/b1024` | 64.7246 ± 0.142149 (W 0.41251) | - | 36.5404 ± 0.0473407 (W 0.156942) | - | 🔴 fork 1.77× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvals/n4/b1` | 0.003867 ± 4.72582e-05 (W 7.46204e-05) | - | 0.002845 ± 6.08276e-06 (W 1.86091e-05) | - | 🔴 fork 1.36× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 3.14928 ± 0.008921 (W 0.00861471) | - | 2.11418 ± 0.00444911 (W 0.00351158) | - | 🔴 fork 1.49× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvals/n8/b1` | 0.016201 ± 5.27289e-05 (W 5.19153e-05) | - | 0.009839 ± 1.53948e-05 (W 3.72062e-05) | - | 🔴 fork 1.65× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 15.3019 ± 1.68346 (W 0.0143134) | - | 8.92313 ± 0.815686 (W 0.0131563) | - | 🔴 fork 1.71× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `eigvalsh/n16/b1` | 0.022412 ± 2.58908e-05 (W 9.91464e-05) | - | 0.012654 ± 3.21455e-05 (W 1.72134e-05) | - | 🔴 fork 1.77× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n16/b1024` | 22.2837 ± 0.0431669 (W 0.0353322) | - | 12.9968 ± 0.0358656 (W 0.0182279) | - | 🔴 fork 1.71× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n4/b1` | 0.002424 ± 2.6839e-05 (W 7.42516e-05) | - | 0.001903 ± 4.16333e-05 (W 3.82792e-05) | - | 🔴 fork 1.27× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 1.92158 ± 0.0222911 (W 0.00580216) | - | 1.49373 ± 0.018778 (W 0.00288508) | - | 🔴 fork 1.29× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n8/b1` | 0.007263 ± 3.06649e-05 (W 3.18795e-05) | - | 0.004819 ± 9.58662e-05 (W 1.66793e-05) | - | 🔴 fork 1.51× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 6.76455 ± 0.02017 (W 0.0134232) | - | 4.4335 ± 0.0191121 (W 0.00632552) | - | 🔴 fork 1.53× slower than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu/n16/b1` | 0.004238 ± 3.60555e-05 (W 4.61519e-05) | - | 0.004017 ± 3.66106e-05 (W 4.53575e-05) | - | 🔴 fork 1.06× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 3.47991 ± 0.0400652 (W 0.0185411) | - | 3.94257 ± 0.0329758 (W 0.0160016) | - | 🔵 fork 1.13× faster than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu/n4/b1` | 0.001022 ± 3.05505e-05 (W 9.045e-05) | - | 0.000761 ± 1.95021e-05 (W 2.2832e-05) | - | 🔴 fork 1.34× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.405437 ± 0.00555588 (W 0.00680455) | - | 0.404874 ± 0.00181971 (W 0.00240501) | - | · | `*` one row has no measurement here |
| `full_piv_lu/n8/b1` | 0.001723 ± 2.51661e-05 (W 7.95437e-05) | - | 0.001322 ± 1.12694e-05 (W 1.9578e-05) | - | 🔴 fork 1.30× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.05144 ± 0.018427 (W 0.00324625) | - | 0.970481 ± 0.0103855 (W 0.00320079) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu_solve/n16/b1` | 0.004348 ± 2.51661e-05 (W 6.94982e-05) | - | 0.006161 ± 4.0501e-05 (W 1.60406e-05) | - | 🔵 fork 1.42× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 3.45715 ± 0.0317483 (W 0.00910323) | - | 5.81292 ± 0.0236272 (W 0.0169665) | - | 🔵 fork 1.68× faster than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu_solve/n4/b1` | 0.001303 ± 2.04206e-05 (W 4.52471e-05) | - | 0.001583 ± 1.1547e-05 (W 3.89872e-05) | - | 🔵 fork 1.21× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.608155 ± 0.023238 (W 0.00433376) | - | 1.11845 ± 0.0101418 (W 0.00306016) | - | 🔵 fork 1.84× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1` | 0.002194 ± 4.04145e-05 (W 4.86025e-05) | - | 0.002394 ± 1.70392e-05 (W 3.0138e-05) | - | 🔵 fork 1.09× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.28506 ± 0.0224829 (W 0.00383519) | - | 1.96041 ± 0.0137855 (W 0.00797967) | - | 🔵 fork 1.53× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_apply/n16/b1` | 0.004859 ± 7.37111e-05 (W 4.47214e-05) | - | 0.003116 ± 5.1316e-05 (W 5.52268e-05) | - | 🔴 fork 1.56× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 4.62098 ± 0.118915 (W 0.0169208) | - | 2.68274 ± 0.00922569 (W 0.0330187) | - | 🔴 fork 1.72× slower than `lapack-mkl` | `*` one row has no measurement here |
| `householder_apply/n4/b1` | 0.000621 ± 5.50757e-06 (W 5.41322e-05) | - | 0.000782 ± 2.3388e-05 (W 2.38998e-05) | - | 🔵 fork 1.26× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.359962 ± 0.0247075 (W 0.00194505) | - | 0.334434 ± 0.00232346 (W 0.00272569) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `householder_apply/n8/b1` | 0.001413 ± 3.95011e-05 (W 1.54693e-05) | - | 0.001312 ± 3.61985e-05 (W 1.43283e-05) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.17173 ± 0.0262894 (W 0.00297239) | - | 0.805952 ± 0.00297619 (W 0.00517902) | - | 🔴 fork 1.45× slower than `lapack-mkl` | `*` one row has no measurement here |
| `householder_factor/n16/b1` | 0.003817 ± 2.3094e-05 (W 2.71882e-05) | - | 0.002996 ± 1.70392e-05 (W 2.30716e-05) | - | 🔴 fork 1.27× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 3.67568 ± 0.0236878 (W 0.0103431) | - | 2.97224 ± 0.0102884 (W 0.0052016) | - | 🔴 fork 1.24× slower than `lapack-mkl` | `*` one row has no measurement here |
| `householder_factor/n4/b1` | 0.000701 ± 1.73205e-05 (W 2.13588e-05) | - | 0.000571 ± 2.08167e-05 (W 2.19363e-05) | - | 🔴 fork 1.23× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.442405 ± 0.102976 (W 0.00365309) | - | 0.30558 ± 0.0232364 (W 0.00166001) | - | 🔴 fork 1.45× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `householder_factor/n8/b1` | 0.001403 ± 4.04145e-05 (W 8.20366e-06) | - | 0.001072 ± 5.7735e-06 (W 1.78885e-05) | - | 🔴 fork 1.31× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.18878 ± 0.00704493 (W 0.00420652) | - | 0.847471 ± 0.00234615 (W 0.00203824) | - | 🔴 fork 1.40× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu/n16/b1` | 0.003065 ± 2.62742e-05 (W 4.14765e-05) | - | 0.001924 ± 3.10966e-05 (W 3.52605e-05) | - | 🔴 fork 1.59× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 2.55129 ± 0.0364495 (W 0.0164823) | - | 1.7516 ± 0.0927308 (W 0.00811137) | - | 🔴 fork 1.46× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `lu/n4/b1` | 0.000802 ± 6.08276e-06 (W 6.83315e-05) | - | 0.00045 ± 1.12694e-05 (W 1.64317e-05) | - | 🔴 fork 1.78× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.290943 ± 0.00678889 (W 0.00332971) | - | 0.167152 ± 0.000346074 (W 0.00160251) | - | 🔴 fork 1.74× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu/n8/b1` | 0.001363 ± 3.17857e-05 (W 5.18102e-05) | - | 0.000761 ± 1e-05 (W 2.53436e-05) | - | 🔴 fork 1.79× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.829967 ± 0.00769809 (W 0.00621124) | - | 0.50919 ± 0.0145065 (W 0.00244824) | - | 🔴 fork 1.63× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `lu_factor/n16/b1` | 0.002074 ± 5.5109e-05 (W 2.53219e-05) | - | 0.001202 ± 0.00010116 (W 7.0852e-06) | - | 🔴 fork 1.73× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 1.81999 ± 0.0251334 (W 0.0053959) | - | 1.17754 ± 0.0464871 (W 0.00282046) | - | 🔴 fork 1.55× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `lu_factor/n4/b1` | 0.000521 ± 1e-05 (W 4.08656e-05) | - | 0.00016 ± 0 (W 2.35648e-05) | - | 🔴 fork 3.26× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.21967 ± 0.00162143 (W 0.00263476) | - | 0.064851 ± 0.00214061 (W 0.00202781) | - | 🔴 fork 3.39× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `lu_factor/n8/b1` | 0.000902 ± 2.04206e-05 (W 3.62381e-05) | - | 0.000351 ± 1e-05 (W 1.10091e-05) | - | 🔴 fork 2.57× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.589831 ± 0.00838225 (W 0.00505014) | - | 0.263361 ± 0.000341791 (W 0.00164062) | - | 🔴 fork 2.24× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor_solve/n16/b1` | 0.002755 ± 4.58258e-05 (W 2.50998e-05) | - | 0.002445 ± 2e-05 (W 5.50018e-05) | - | 🔴 fork 1.13× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 2.3678 ± 0.0280125 (W 0.00384752) | - | 2.3245 ± 0.0324991 (W 0.00411071) | - | · | `*` one row has no measurement here |
| `lu_factor_solve/n4/b1` | 0.000592 ± 2.09841e-05 (W 3.08221e-05) | - | 0.000301 ± 2.09841e-05 (W 2.47043e-05) | - | 🔴 fork 1.97× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.275765 ± 0.0041476 (W 0.00214757) | - | 0.183813 ± 0.0039696 (W 0.0013945) | - | 🔴 fork 1.50× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor_solve/n8/b1` | 0.001182 ± 5.19615e-06 (W 5.71839e-05) | - | 0.000892 ± 1.57162e-05 (W 7.09225e-06) | - | 🔴 fork 1.33× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 0.799742 ± 0.0108612 (W 0.00325704) | - | 0.824396 ± 0.00252623 (W 0.00187265) | - | · | `*` one row has no measurement here |
| `lu_solve_prepared/n16/b1` | 0.000932 ± 1.73205e-05 (W 2.40832e-05) | - | 0.001183 ± 1.51767e-05 (W 3.24238e-05) | - | 🔵 fork 1.27× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 0.626698 ± 0.00153035 (W 0.00305437) | - | 1.05383 ± 0.0257233 (W 0.00587198) | - | 🔵 fork 1.68× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_solve_prepared/n4/b1` | 0.000351 ± 1.48436e-05 (W 3.15151e-05) | - | 0.00023 ± 9.50438e-06 (W 1.7672e-05) | - | 🔴 fork 1.53× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.067736 ± 0.00016544 (W 0.0015767) | - | 0.133058 ± 7.26659e-05 (W 8.63035e-05) | - | 🔵 fork 1.96× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_solve_prepared/n8/b1` | 0.000521 ± 1.52753e-05 (W 4.44972e-05) | - | 0.000661 ± 5.7735e-07 (W 1.51063e-05) | - | 🔵 fork 1.27× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.230319 ± 0.00143472 (W 0.00134986) | - | 0.588378 ± 0.00113956 (W 0.00210925) | - | 🔵 fork 2.55× faster than `lapack-mkl` | `*` one row has no measurement here |
| `qr/n16/b1` | 0.009328 ± 8.71799e-05 (W 6.24284e-05) | - | 0.005681 ± 3.60555e-05 (W 3.14516e-05) | - | 🔴 fork 1.64× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 8.86531 ± 0.149138 (W 0.0246759) | - | 5.32086 ± 0.0143402 (W 0.00900179) | - | 🔴 fork 1.67× slower than `lapack-mkl` | `*` one row has no measurement here |
| `qr/n4/b1` | 0.001262 ± 5.7735e-06 (W 3.17364e-05) | - | 0.001192 ± 2.64575e-05 (W 3.00865e-05) | - | 🔴 fork 1.06× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.760588 ± 0.013985 (W 0.00382166) | - | 0.722598 ± 0.00967788 (W 0.00286739) | - | 🔴 fork 1.05× slower than `lapack-mkl` | `*` one row has no measurement here |
| `qr/n8/b1` | 0.002956 ± 4.33628e-05 (W 2.5499e-05) | - | 0.002244 ± 1.1547e-05 (W 2.58322e-05) | - | 🔴 fork 1.32× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.36297 ± 0.0458525 (W 0.00372791) | - | 1.71242 ± 0.0174901 (W 0.0056728) | - | 🔴 fork 1.38× slower than `lapack-mkl` | `*` one row has no measurement here |
| `rank_revealing_qr/n16/b1` | 0.01081 ± 8.88819e-05 (W 6.60704e-05) | - | 0.009007 ± 2.64575e-05 (W 5.76194e-05) | - | 🔴 fork 1.20× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 10.2125 ± 0.0759518 (W 0.0257365) | - | 8.36511 ± 0.0105606 (W 0.0114009) | - | 🔴 fork 1.22× slower than `lapack-mkl` | `*` one row has no measurement here |
| `rank_revealing_qr/n4/b1` | 0.001884 ± 1.67432e-05 (W 3.17065e-05) | - | 0.002004 ± 6.35085e-06 (W 5.5857e-05) | - | 🔵 fork 1.06× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.18917 ± 0.0112474 (W 0.00277013) | - | 1.21757 ± 0.00889845 (W 0.00384664) | - | · | `*` one row has no measurement here |
| `rank_revealing_qr/n8/b1` | 0.004078 ± 3.64737e-05 (W 3.04187e-05) | - | 0.003747 ± 4.16333e-05 (W 7.82943e-05) | - | 🔴 fork 1.09× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.14541 ± 0.102976 (W 0.00762473) | - | 2.95908 ± 0.0186605 (W 0.00470619) | - | 🔴 fork 1.06× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `solve/n16/b1` | 0.003686 ± 3.82143e-05 (W 6.45074e-05) | - | 0.002935 ± 1e-05 (W 3.19875e-05) | - | 🔴 fork 1.26× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 2.55945 ± 0.00253754 (W 0.0242605) | - | 2.38117 ± 0.00808782 (W 0.00453993) | - | 🔴 fork 1.07× slower than `lapack-mkl` | `*` one row has no measurement here |
| `solve/n4/b1` | 0.001283 ± 6.60328e-05 (W 8.58679e-05) | - | 0.000571 ± 5.7735e-07 (W 1.9084e-05) | - | 🔴 fork 2.25× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.364189 ± 0.00183529 (W 0.00202945) | - | 0.228817 ± 0.00294731 (W 0.00171287) | - | 🔴 fork 1.59× slower than `lapack-mkl` | `*` one row has no measurement here |
| `solve/n8/b1` | 0.001983 ± 5.19615e-06 (W 5.03716e-05) | - | 0.001222 ± 5.7735e-06 (W 1.47411e-05) | - | 🔴 fork 1.62× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 0.914496 ± 0.0248355 (W 0.0043759) | - | 0.887254 ± 0.00119316 (W 0.00260752) | - | · | `*` one row has no measurement here; `!` between-start range over 5% |
| `svd_full/n16/b1` | 0.054772 ± 0.000584364 (W 0.00117744) | - | 0.051065 ± 0.000231294 (W 8.20366e-05) | - | 🔴 fork 1.07× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_full/n16/b1024` | 55.8274 ± 0.421297 (W 0.0432393) | - | 51.6374 ± 0.063829 (W 0.0879614) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_full/n4/b1` | 0.004899 ± 0.000569158 (W 0.000301856) | - | 0.006552 ± 3.05505e-05 (W 4.14524e-05) | - | 🔵 fork 1.34× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 4.2931 ± 0.0385365 (W 0.00617341) | - | 6.15896 ± 0.0319216 (W 0.00600164) | - | 🔵 fork 1.43× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_full/n8/b1` | 0.015319 ± 9.71253e-05 (W 0.00140095) | - | 0.017854 ± 1.57162e-05 (W 6.32456e-05) | - | 🔵 fork 1.17× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 15.1652 ± 0.0870124 (W 0.0332607) | - | 18.6292 ± 0.0388282 (W 0.0225526) | - | 🔵 fork 1.23× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n16/b1` | 0.054682 ± 0.000167033 (W 0.000169499) | - | 0.050825 ± 0.000157513 (W 0.000107704) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n16/b1024` | 55.559 ± 0.25907 (W 0.0449809) | - | 51.6057 ± 0.0769081 (W 0.383116) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n4/b1` | 0.004879 ± 5.1316e-05 (W 3.96232e-05) | - | 0.006573 ± 3.19427e-05 (W 3.03315e-05) | - | 🔵 fork 1.35× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 4.31527 ± 0.0115829 (W 0.0165584) | - | 6.1663 ± 0.0382762 (W 0.0180882) | - | 🔵 fork 1.43× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n8/b1` | 0.015378 ± 5.80259e-05 (W 7.99137e-05) | - | 0.018034 ± 0.000126808 (W 4.50699e-05) | - | 🔵 fork 1.17× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 15.1398 ± 0.0397065 (W 0.0300094) | - | 18.6972 ± 0.0565151 (W 0.0272061) | - | 🔵 fork 1.23× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n16/b1` | 0.040246 ± 0.000250241 (W 0.00016758) | - | 0.018635 ± 4.09512e-05 (W 5.63028e-05) | - | 🔴 fork 2.16× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n16/b1024` | 40.9843 ± 0.237655 (W 0.0646273) | - | 19.3313 ± 0.0471797 (W 0.0302376) | - | 🔴 fork 2.12× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n4/b1` | 0.003807 ± 1.73205e-05 (W 9.71813e-05) | - | 0.003086 ± 2.64575e-05 (W 5.85662e-05) | - | 🔴 fork 1.23× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.18514 ± 0.0199335 (W 0.00492139) | - | 2.67627 ± 0.00798061 (W 0.00726274) | - | 🔴 fork 1.19× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n8/b1` | 0.011502 ± 8.6122e-05 (W 7.38871e-05) | - | 0.006802 ± 1.0504e-05 (W 3.11817e-05) | - | 🔴 fork 1.69× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 11.2643 ± 0.0297086 (W 0.0229561) | - | 6.70655 ± 0.0262478 (W 0.00604742) | - | 🔴 fork 1.68× slower than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n16/b1` | 0.000982 ± 5.50757e-06 (W 4.29337e-05) | - | 0.000862 ± 1.52753e-05 (W 1.3975e-05) | - | 🔴 fork 1.14× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.502297 ± 0.0011458 (W 0.00258438) | - | 0.574492 ± 0.00476377 (W 0.00289021) | - | 🔵 fork 1.14× faster than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n4/b1` | 0.000581 ± 2.3094e-05 (W 3.20936e-05) | - | 0.000611 ± 1.52753e-05 (W 3.11448e-05) | - | 🔵 fork 1.05× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.087804 ± 0.00026704 (W 0.000375361) | - | 0.291544 ± 0.00164546 (W 0.002129) | - | 🔵 fork 3.32× faster than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n8/b1` | 0.000722 ± 3.21455e-05 (W 4.39124e-05) | - | 0.000672 ± 6.35085e-06 (W 2.1594e-05) | - | 🔴 fork 1.07× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.217435 ± 0.000911583 (W 0.00176647) | - | 0.382092 ± 0.00331747 (W 0.00342256) | - | 🔵 fork 1.76× faster than `lapack-mkl` | `*` one row has no measurement here |

## batch-small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001303 ± 2.04206e-05 (W 4.61443e-05) | 0.001302 ± 2.46374e-05 (W 4.86344e-05) | 0.001212 ± 3.51188e-05 (W 1.49064e-05) | · | 🔴 fork 1.08× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 0.915418 ± 0.02414 (W 0.00737491) | 0.119613 ± 0.00322011 (W 0.00126558) | 1.05513 ± 0.00950433 (W 0.0017308) | 🔴 fork 7.65× slower than `faer-pool` | 🔵 fork 1.15× faster than `lapack-mkl` | `!` between-start range over 5% |
| `cholesky/n4/b1` | 0.000581 ± 5.7735e-06 (W 3.70135e-05) | 0.000601 ± 1.52753e-05 (W 5.93296e-05) | 0.000311 ± 5.7735e-06 (W 8.01249e-06) | · | 🔴 fork 1.87× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.178843 ± 0.000657818 (W 0.00135103) | 0.029365 ± 0.0001861 (W 0.000232229) | 0.119373 ± 0.00440332 (W 0.00121909) | 🔴 fork 6.09× slower than `faer-pool` | 🔴 fork 1.50× slower than `lapack-mkl` | `!` between-start range over 5% |
| `cholesky/n8/b1` | 0.000752 ± 1.57162e-05 (W 2.33731e-05) | 0.000772 ± 5.50757e-06 (W 4.11862e-05) | 0.000501 ± 1.1547e-05 (W 8.94427e-06) | · | 🔴 fork 1.50× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.36994 ± 0.00621606 (W 0.00243245) | 0.05374 ± 0.000531031 (W 0.000579699) | 0.311822 ± 0.0055889 (W 0.00208119) | 🔴 fork 6.88× slower than `faer-pool` | 🔴 fork 1.19× slower than `lapack-mkl` |  |
| `eig/n16/b1` | 0.090208 ± 0.000118462 (W 0.000246883) | 0.090529 ± 0.000436734 (W 0.00151004) | 0.050614 ± 5.80259e-05 (W 8.88099e-05) | · | 🔴 fork 1.78× slower than `lapack-mkl` |  |
| `eig/n16/b1024` | 93.7675 ± 0.19688 (W 0.11819) | 11.893 ± 0.0094117 (W 0.0336152) | 52.9454 ± 0.0518393 (W 0.0779191) | 🔴 fork 7.88× slower than `faer-pool` | 🔴 fork 1.77× slower than `lapack-mkl` |  |
| `eig/n4/b1` | 0.006843 ± 4.16333e-05 (W 8.9975e-05) | 0.006793 ± 7.23418e-05 (W 9.82344e-05) | 0.003557 ± 1e-05 (W 4.99229e-05) | · | 🔴 fork 1.92× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 6.11556 ± 0.013595 (W 0.012245) | 0.79352 ± 0.0156421 (W 0.00407653) | 2.83638 ± 0.00388739 (W 0.0093502) | 🔴 fork 7.71× slower than `faer-pool` | 🔴 fork 2.16× slower than `lapack-mkl` |  |
| `eig/n8/b1` | 0.024055 ± 4.16333e-05 (W 0.00159067) | 0.024085 ± 0.000137078 (W 0.000135703) | 0.012363 ± 5e-05 (W 4.9942e-05) | · | 🔴 fork 1.95× slower than `lapack-mkl` |  |
| `eig/n8/b1024` | 23.2346 ± 0.0576713 (W 0.0303822) | 2.95065 ± 0.00910881 (W 0.00565267) | 11.6391 ± 0.00608836 (W 0.0236551) | 🔴 fork 7.87× slower than `faer-pool` | 🔴 fork 2.00× slower than `lapack-mkl` |  |
| `eigh/n16/b1` | 0.029505 ± 0.000105987 (W 0.000255794) | 0.029706 ± 3.61985e-05 (W 0.000106392) | 0.022492 ± 5.85947e-05 (W 6.10737e-05) | · | 🔴 fork 1.31× slower than `lapack-mkl` |  |
| `eigh/n16/b1024` | 29.5643 ± 0.101276 (W 0.0313562) | 3.76075 ± 0.00495339 (W 0.0110136) | 23.499 ± 0.0495142 (W 0.0394166) | 🔴 fork 7.86× slower than `faer-pool` | 🔴 fork 1.26× slower than `lapack-mkl` |  |
| `eigh/n4/b1` | 0.002926 ± 7.75263e-05 (W 6.66206e-05) | 0.002965 ± 9.50438e-06 (W 8.72422e-05) | 0.003086 ± 4.16333e-05 (W 6.64831e-05) | · | 🔵 fork 1.05× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.41272 ± 0.0343164 (W 0.00613289) | 0.312382 ± 0.00685151 (W 0.0025781) | 2.78465 ± 0.0259486 (W 0.00920873) | 🔴 fork 7.72× slower than `faer-pool` | 🔵 fork 1.15× faster than `lapack-mkl` |  |
| `eigh/n8/b1` | 0.008787 ± 2.47049e-05 (W 0.000100579) | 0.008817 ± 8.41843e-05 (W 9.06162e-05) | 0.007805 ± 3.95011e-05 (W 2.53239e-05) | · | 🔴 fork 1.13× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 8.41675 ± 0.0211706 (W 0.0227502) | 1.07902 ± 0.00226594 (W 0.00492161) | 7.70282 ± 0.0226219 (W 0.0138521) | 🔴 fork 7.80× slower than `faer-pool` | 🔴 fork 1.09× slower than `lapack-mkl` |  |
| `eigvals/n16/b1` | 0.061885 ± 9.02238e-05 (W 0.000116749) | 0.062196 ± 6.35085e-05 (W 0.00146976) | 0.035076 ± 0.000130985 (W 3.36199e-05) | · | 🔴 fork 1.76× slower than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 64.7569 ± 0.0923711 (W 0.0565357) | 8.17574 ± 0.0516588 (W 0.0258492) | 36.584 ± 0.0632633 (W 0.0323888) | 🔴 fork 7.92× slower than `faer-pool` | 🔴 fork 1.77× slower than `lapack-mkl` |  |
| `eigvals/n4/b1` | 0.003858 ± 2.95014e-05 (W 5.53281e-05) | 0.003908 ± 3.21455e-05 (W 7.24997e-05) | 0.002855 ± 2.04206e-05 (W 3.84708e-05) | · | 🔴 fork 1.35× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 3.13264 ± 0.0315574 (W 0.00904732) | 0.4129 ± 0.00198011 (W 0.00299886) | 2.11288 ± 0.0035735 (W 0.00596231) | 🔴 fork 7.59× slower than `faer-pool` | 🔴 fork 1.48× slower than `lapack-mkl` |  |
| `eigvals/n8/b1` | 0.01626 ± 0.000115544 (W 8.70701e-05) | 0.01627 ± 7.63763e-05 (W 5.36777e-05) | 0.009858 ± 4.04145e-05 (W 7.25893e-05) | · | 🔴 fork 1.65× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 15.2854 ± 0.0784277 (W 0.0165127) | 1.92883 ± 0.0133536 (W 0.00375225) | 8.91379 ± 0.0141726 (W 0.0337725) | 🔴 fork 7.92× slower than `faer-pool` | 🔴 fork 1.71× slower than `lapack-mkl` |  |
| `eigvalsh/n16/b1` | 0.022542 ± 0.000124231 (W 0.000106767) | 0.022662 ± 1.73205e-05 (W 0.000111997) | 0.012643 ± 1.18462e-05 (W 4.36612e-05) | · | 🔴 fork 1.78× slower than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 22.3663 ± 0.0726819 (W 0.0238374) | 2.81786 ± 0.00216934 (W 0.00518888) | 13.0276 ± 0.0202436 (W 0.0222068) | 🔴 fork 7.94× slower than `faer-pool` | 🔴 fork 1.72× slower than `lapack-mkl` |  |
| `eigvalsh/n4/b1` | 0.002374 ± 2.13776e-05 (W 0.000122643) | 0.002445 ± 3.60555e-05 (W 9.11987e-05) | 0.001893 ± 2.04206e-05 (W 4.45567e-05) | · | 🔴 fork 1.25× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 1.92468 ± 0.0148344 (W 0.00669211) | 0.253272 ± 0.00227792 (W 0.00200047) | 1.45625 ± 0.0136607 (W 0.00377525) | 🔴 fork 7.60× slower than `faer-pool` | 🔴 fork 1.32× slower than `lapack-mkl` |  |
| `eigvalsh/n8/b1` | 0.007183 ± 2.88675e-05 (W 7.8613e-05) | 0.007254 ± 3.59212e-05 (W 4.52913e-05) | 0.004739 ± 2.95014e-05 (W 2.77489e-05) | · | 🔴 fork 1.52× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 6.79871 ± 0.0226822 (W 0.0173377) | 0.871756 ± 0.00446002 (W 0.010005) | 4.40421 ± 0.00794788 (W 0.0100523) | 🔴 fork 7.80× slower than `faer-pool` | 🔴 fork 1.54× slower than `lapack-mkl` |  |
| `full_piv_lu/n16/b1` | 0.004218 ± 8.32666e-05 (W 9.7766e-05) | 0.004358 ± 7.54983e-05 (W 7.12264e-05) | 0.004028 ± 5.05008e-05 (W 3.12298e-05) | · | · | dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 3.41942 ± 0.0155191 (W 0.0120994) | 0.473162 ± 0.00168467 (W 0.00555675) | 3.89523 ± 0.0707803 (W 0.0114878) | 🔴 fork 7.23× slower than `faer-pool` | 🔵 fork 1.14× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1` | 0.001002 ± 1.67432e-05 (W 6.3539e-05) | 0.001142 ± 3.21455e-05 (W 6.59545e-05) | 0.000761 ± 1.95021e-05 (W 3.32611e-05) | 🔵 fork 1.14× faster than `faer-pool` | 🔴 fork 1.32× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.411938 ± 0.0256894 (W 0.0137266) | 0.084808 ± 0.00059419 (W 0.00326821) | 0.406248 ± 0.00511317 (W 0.00211196) | 🔴 fork 4.86× slower than `faer-pool` | · | `!` between-start range over 5% |
| `full_piv_lu/n8/b1` | 0.001754 ± 4.09512e-05 (W 0.000102505) | 0.001834 ± 2.64575e-05 (W 4.58825e-05) | 0.001303 ± 2.85832e-05 (W 1.48762e-05) | · | 🔴 fork 1.35× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.04193 ± 0.0172354 (W 0.00300248) | 0.167402 ± 0.00144943 (W 0.0030104) | 0.987131 ± 0.014443 (W 0.00313112) | 🔴 fork 6.22× slower than `faer-pool` | 🔴 fork 1.06× slower than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1` | 0.004368 ± 5.50757e-05 (W 7.36206e-05) | 0.004398 ± 8.14269e-05 (W 7.73195e-05) | 0.006182 ± 6.245e-05 (W 6.08621e-05) | · | 🔵 fork 1.42× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 3.38236 ± 0.0250643 (W 0.0125933) | 0.448797 ± 0.0115188 (W 0.00625866) | 5.75359 ± 0.011035 (W 0.00886585) | 🔴 fork 7.54× slower than `faer-pool` | 🔵 fork 1.70× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n4/b1` | 0.001352 ± 5.55908e-05 (W 7.05216e-05) | 0.001342 ± 1.52753e-05 (W 8.13038e-05) | 0.001603 ± 1.58219e-05 (W 8.06114e-05) | · | 🔵 fork 1.19× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.606561 ± 0.0354133 (W 0.00387802) | 0.086361 ± 0.000112694 (W 0.00102051) | 1.10829 ± 0.0182827 (W 0.003519) | 🔴 fork 7.02× slower than `faer-pool` | 🔵 fork 1.83× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1` | 0.002244 ± 5.03322e-05 (W 7.81358e-05) | 0.002264 ± 7.6922e-05 (W 2.16148e-05) | 0.002455 ± 4.17971e-05 (W 4.05006e-05) | · | 🔵 fork 1.09× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.26658 ± 0.00785085 (W 0.00680689) | 0.172662 ± 0.00284322 (W 0.00248731) | 1.93355 ± 0.0268901 (W 0.00405964) | 🔴 fork 7.34× slower than `faer-pool` | 🔵 fork 1.53× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1` | 0.004649 ± 7e-05 (W 7.59757e-05) | 0.004719 ± 4.50925e-05 (W 0.000120291) | 0.003076 ± 4.04145e-05 (W 7.15542e-05) | · | 🔴 fork 1.51× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 4.65805 ± 0.05075 (W 0.0162129) | 0.60607 ± 0.00222136 (W 0.00197016) | 2.68213 ± 0.0153069 (W 0.0287624) | 🔴 fork 7.69× slower than `faer-pool` | 🔴 fork 1.74× slower than `lapack-mkl` |  |
| `householder_apply/n4/b1` | 0.000622 ± 5.7735e-06 (W 3.01861e-05) | 0.000711 ± 0.00014526 (W 3.53553e-05) | 0.000752 ± 5.7735e-07 (W 2.30282e-05) | · | 🔵 fork 1.21× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.352787 ± 0.00143049 (W 0.00203216) | 0.052247 ± 0.000907556 (W 0.000779098) | 0.321891 ± 0.000850161 (W 0.00327264) | 🔴 fork 6.75× slower than `faer-pool` | 🔴 fork 1.10× slower than `lapack-mkl` |  |
| `householder_apply/n8/b1` | 0.001422 ± 3.95011e-05 (W 3.74339e-05) | 0.001433 ± 4.04145e-05 (W 2.28035e-05) | 0.001262 ± 1.00167e-05 (W 2.68365e-05) | · | 🔴 fork 1.13× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.14284 ± 0.0722778 (W 0.00310268) | 0.167813 ± 0.00429228 (W 0.00164433) | 0.795844 ± 0.0129876 (W 0.00422246) | 🔴 fork 6.81× slower than `faer-pool` | 🔴 fork 1.44× slower than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1` | 0.003827 ± 2.64575e-05 (W 7.96568e-05) | 0.003887 ± 2.13776e-05 (W 3.96005e-05) | 0.002996 ± 2.85832e-05 (W 4.62418e-05) | · | 🔴 fork 1.28× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 3.66289 ± 0.0425516 (W 0.0062973) | 0.485796 ± 0.0111039 (W 0.00474427) | 2.95475 ± 0.00869952 (W 0.00488961) | 🔴 fork 7.54× slower than `faer-pool` | 🔴 fork 1.24× slower than `lapack-mkl` |  |
| `householder_factor/n4/b1` | 0.000691 ± 3.00056e-05 (W 3.54161e-05) | 0.000731 ± 1.57162e-05 (W 5.41138e-05) | 0.000561 ± 1.1547e-05 (W 1.67332e-05) | 🔵 fork 1.06× faster than `faer-pool` | 🔴 fork 1.23× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.448547 ± 0.00919679 (W 0.00210736) | 0.063298 ± 0.000322909 (W 0.00119923) | 0.306352 ± 0.00143105 (W 0.00159253) | 🔴 fork 7.09× slower than `faer-pool` | 🔴 fork 1.46× slower than `lapack-mkl` |  |
| `householder_factor/n8/b1` | 0.001413 ± 3.00056e-05 (W 3.09241e-05) | 0.001443 ± 2.51661e-05 (W 3.79645e-05) | 0.001082 ± 1.1547e-05 (W 2.12132e-05) | · | 🔴 fork 1.31× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.18533 ± 0.0127165 (W 0.00657861) | 0.16649 ± 0.00223793 (W 0.00231634) | 0.8471 ± 0.00162497 (W 0.00201444) | 🔴 fork 7.12× slower than `faer-pool` | 🔴 fork 1.40× slower than `lapack-mkl` |  |
| `lu/n16/b1` | 0.003186 ± 2.51661e-05 (W 5.89915e-05) | 0.003226 ± 8.14453e-05 (W 7.36152e-05) | 0.001933 ± 3.04467e-05 (W 3.67328e-05) | · | 🔴 fork 1.65× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 2.60453 ± 0.0135237 (W 0.01502) | 0.364901 ± 0.00252139 (W 0.00547812) | 1.70558 ± 0.0455432 (W 0.00859652) | 🔴 fork 7.14× slower than `faer-pool` | 🔴 fork 1.53× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n4/b1` | 0.000781 ± 3.23574e-05 (W 5.40953e-05) | 0.000832 ± 1.57162e-05 (W 3.46006e-05) | 0.000451 ± 1e-05 (W 3e-05) | 🔵 fork 1.07× faster than `faer-pool` | 🔴 fork 1.73× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.31085 ± 0.0114762 (W 0.00454473) | 0.072906 ± 0.00096532 (W 0.0035148) | 0.167031 ± 0.0004774 (W 0.00144519) | 🔴 fork 4.26× slower than `faer-pool` | 🔴 fork 1.86× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n8/b1` | 0.001263 ± 5.16753e-05 (W 4.41396e-05) | 0.001353 ± 3.72872e-05 (W 7.48078e-05) | 0.000762 ± 1e-05 (W 2.45418e-05) | 🔵 fork 1.07× faster than `faer-pool` | 🔴 fork 1.66× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.830728 ± 0.00641511 (W 0.00660324) | 0.143387 ± 0.00267134 (W 0.00429971) | 0.495094 ± 0.0169981 (W 0.0027367) | 🔴 fork 5.79× slower than `faer-pool` | 🔴 fork 1.68× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n16/b1` | 0.002114 ± 4.56107e-05 (W 6.22896e-05) | 0.002144 ± 1e-05 (W 3.03315e-05) | 0.001232 ± 2.5632e-05 (W 2.72452e-05) | · | 🔴 fork 1.72× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 1.86923 ± 0.00371097 (W 0.00530466) | 0.262991 ± 0.00231072 (W 0.00155127) | 1.18559 ± 0.0309618 (W 0.00292542) | 🔴 fork 7.11× slower than `faer-pool` | 🔴 fork 1.58× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n4/b1` | 0.000531 ± 0 (W 4.12311e-05) | 0.000521 ± 2.3388e-05 (W 6.73662e-05) | 0.00016 ± 0 (W 2.05718e-05) | · | 🔴 fork 3.32× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.221694 ± 0.00363616 (W 0.00201651) | 0.062838 ± 0.000581149 (W 0.00153791) | 0.065321 ± 9.31504e-05 (W 0.000422144) | 🔴 fork 3.53× slower than `faer-pool` | 🔴 fork 3.39× slower than `lapack-mkl` |  |
| `lu_factor/n8/b1` | 0.000862 ± 1.1547e-05 (W 4.12092e-05) | 0.000921 ± 3.40637e-05 (W 6.34846e-05) | 0.000331 ± 5.19615e-06 (W 1.70382e-05) | 🔵 fork 1.07× faster than `faer-pool` | 🔴 fork 2.60× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.59459 ± 0.00857913 (W 0.00550786) | 0.111427 ± 0.00395328 (W 0.0025854) | 0.262018 ± 0.00268192 (W 0.0016682) | 🔴 fork 5.34× slower than `faer-pool` | 🔴 fork 2.27× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n16/b1` | 0.002765 ± 9.50438e-06 (W 4.97212e-05) | 0.002845 ± 3.05505e-05 (W 6.00017e-05) | 0.002505 ± 7.01926e-05 (W 5.87393e-05) | · | 🔴 fork 1.10× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 2.39657 ± 0.0076044 (W 0.00455955) | 0.335365 ± 0.00247921 (W 0.00320785) | 2.38916 ± 0.0405041 (W 0.00499494) | 🔴 fork 7.15× slower than `faer-pool` | · |  |
| `lu_factor_solve/n4/b1` | 0.000591 ± 1.1547e-05 (W 4.08656e-05) | 0.000651 ± 1.18462e-05 (W 4.41588e-05) | 0.000271 ± 1.09697e-05 (W 1.22597e-05) | 🔵 fork 1.10× faster than `faer-pool` | 🔴 fork 2.18× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.276085 ± 0.00258786 (W 0.00187655) | 0.063739 ± 0.00113393 (W 0.000840271) | 0.181789 ± 0.00187155 (W 0.00117782) | 🔴 fork 4.33× slower than `faer-pool` | 🔴 fork 1.52× slower than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1` | 0.001162 ± 2e-05 (W 8.04002e-05) | 0.001222 ± 5.08626e-05 (W 5.8062e-05) | 0.000882 ± 5.7735e-07 (W 1.12827e-05) | 🔵 fork 1.05× faster than `faer-pool` | 🔴 fork 1.32× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 0.819237 ± 0.0557677 (W 0.00625856) | 0.131746 ± 0.00443439 (W 0.00135597) | 0.825579 ± 0.00326728 (W 0.0035208) | 🔴 fork 6.22× slower than `faer-pool` | · | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1` | 0.000941 ± 2.09841e-05 (W 4.06202e-05) | 0.000962 ± 2.60832e-05 (W 3.04959e-05) | 0.001212 ± 1.09697e-05 (W 2.96193e-05) | · | 🔵 fork 1.29× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 0.622982 ± 0.00141877 (W 0.00208196) | 0.129512 ± 0.00059328 (W 0.00146973) | 1.05345 ± 0.0127677 (W 0.00615165) | 🔴 fork 4.81× slower than `faer-pool` | 🔵 fork 1.69× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1` | 0.000361 ± 2.46374e-05 (W 5.16749e-05) | 0.0004 ± 3.09892e-05 (W 4.45567e-05) | 0.000221 ± 1.70392e-05 (W 1.9857e-05) | · | 🔴 fork 1.63× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.067476 ± 0.000105987 (W 6.9857e-05) | 0.033142 ± 0.000407424 (W 0.000441809) | 0.130503 ± 0.000397581 (W 0.00168761) | 🔴 fork 2.04× slower than `faer-pool` | 🔵 fork 1.93× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1` | 0.000521 ± 5.7735e-06 (W 3.42053e-05) | 0.000591 ± 3.60555e-05 (W 4.03733e-05) | 0.000661 ± 1.1547e-05 (W 4.02492e-06) | 🔵 fork 1.13× faster than `faer-pool` | 🔵 fork 1.27× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.228757 ± 0.000876084 (W 0.00217808) | 0.055052 ± 0.000176721 (W 0.000629945) | 0.587285 ± 0.00225313 (W 0.00228782) | 🔴 fork 4.16× slower than `faer-pool` | 🔵 fork 2.57× faster than `lapack-mkl` |  |
| `qr/n16/b1` | 0.009046 ± 0.000145741 (W 0.000211682) | 0.009157 ± 0.000167004 (W 0.000107342) | 0.0056 ± 4.03361e-05 (W 4.86755e-05) | · | 🔴 fork 1.62× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 8.74584 ± 0.108497 (W 0.012925) | 1.13265 ± 0.00526847 (W 0.00414938) | 5.27954 ± 0.00426599 (W 0.0238009) | 🔴 fork 7.72× slower than `faer-pool` | 🔴 fork 1.66× slower than `lapack-mkl` |  |
| `qr/n4/b1` | 0.001243 ± 6.08276e-06 (W 6.54851e-05) | 0.001302 ± 2.3388e-05 (W 6.72332e-05) | 0.001212 ± 2.88675e-05 (W 5.78792e-05) | · | · | dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.756239 ± 0.00817162 (W 0.00283518) | 0.104926 ± 0.000837 (W 0.00148418) | 0.725712 ± 0.0218984 (W 0.00251653) | 🔴 fork 7.21× slower than `faer-pool` | · | `!` between-start range over 5% |
| `qr/n8/b1` | 0.003045 ± 5.50757e-06 (W 4.51697e-05) | 0.003066 ± 5.19615e-05 (W 4.39318e-05) | 0.002204 ± 5.7735e-06 (W 3.08739e-05) | · | 🔴 fork 1.38× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.43064 ± 0.0412167 (W 0.00292892) | 0.319215 ± 0.000813396 (W 0.0055478) | 1.69189 ± 0.00976901 (W 0.00368611) | 🔴 fork 7.61× slower than `faer-pool` | 🔴 fork 1.44× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1` | 0.01069 ± 5.7735e-05 (W 8.90404e-05) | 0.010861 ± 5.31068e-05 (W 4.219e-05) | 0.008996 ± 4.41626e-05 (W 5.67301e-05) | · | 🔴 fork 1.19× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 10.1661 ± 0.0578027 (W 0.0223187) | 1.31321 ± 0.00966057 (W 0.00535512) | 8.36548 ± 0.179252 (W 0.0167493) | 🔴 fork 7.74× slower than `faer-pool` | 🔴 fork 1.22× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1` | 0.001903 ± 3.19427e-05 (W 6.92907e-05) | 0.001924 ± 6.245e-05 (W 0.000100399) | 0.001984 ± 2.25167e-05 (W 5.14218e-05) | · | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.16684 ± 0.0102596 (W 0.00523478) | 0.159938 ± 0.00437655 (W 0.0020207) | 1.2325 ± 0.00800188 (W 0.00248417) | 🔴 fork 7.30× slower than `faer-pool` | 🔵 fork 1.06× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1` | 0.004058 ± 3.5171e-05 (W 3.23929e-05) | 0.004148 ± 1.1547e-05 (W 3.05827e-05) | 0.003747 ± 1.52753e-05 (W 3.50714e-05) | · | 🔴 fork 1.08× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.14084 ± 0.0274026 (W 0.00442413) | 0.424602 ± 0.00482069 (W 0.00339619) | 2.93362 ± 0.0431188 (W 0.00809911) | 🔴 fork 7.40× slower than `faer-pool` | 🔴 fork 1.07× slower than `lapack-mkl` |  |
| `solve/n16/b1` | 0.003727 ± 2.51661e-05 (W 4.9295e-05) | 0.003847 ± 0.000110151 (W 6.89202e-05) | 0.002975 ± 2.08167e-05 (W 5.47923e-05) | · | 🔴 fork 1.25× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 2.62503 ± 0.0405745 (W 0.00909724) | 0.360211 ± 0.0020352 (W 0.00500845) | 2.46057 ± 0.0351358 (W 0.010842) | 🔴 fork 7.29× slower than `faer-pool` | 🔴 fork 1.07× slower than `lapack-mkl` |  |
| `solve/n4/b1` | 0.001232 ± 3.66106e-05 (W 6.5202e-05) | 0.001282 ± 4.08697e-05 (W 6.29706e-05) | 0.000571 ± 1.1547e-05 (W 4.15933e-05) | · | 🔴 fork 2.16× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.371853 ± 0.00141392 (W 0.00237499) | 0.056485 ± 0.00259565 (W 0.000841602) | 0.232955 ± 0.00319637 (W 0.00188335) | 🔴 fork 6.58× slower than `faer-pool` | 🔴 fork 1.60× slower than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n8/b1` | 0.001974 ± 3.06649e-05 (W 5.30971e-05) | 0.002084 ± 5.56776e-05 (W 7.52542e-05) | 0.001213 ± 2.3388e-05 (W 4.25476e-05) | 🔵 fork 1.06× faster than `faer-pool` | 🔴 fork 1.63× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 0.910658 ± 0.00739184 (W 0.0100638) | 0.132046 ± 0.00185781 (W 0.00203557) | 0.900488 ± 0.0100278 (W 0.00154346) | 🔴 fork 6.90× slower than `faer-pool` | · |  |
| `svd_full/n16/b1` | 0.054512 ± 0.000143377 (W 0.000216435) | 0.054873 ± 0.000354798 (W 9.97106e-05) | 0.051065 ± 0.000261024 (W 8.89618e-05) | · | 🔴 fork 1.07× slower than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 55.6871 ± 0.538156 (W 0.0493122) | 7.27429 ± 0.139101 (W 0.0258377) | 51.5858 ± 0.121495 (W 0.113326) | 🔴 fork 7.66× slower than `faer-pool` | 🔴 fork 1.08× slower than `lapack-mkl` |  |
| `svd_full/n4/b1` | 0.004899 ± 3.05505e-05 (W 0.000105972) | 0.004939 ± 2.88675e-05 (W 3.92467e-05) | 0.006522 ± 4e-05 (W 5.79931e-05) | · | 🔵 fork 1.33× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 4.29948 ± 0.0344928 (W 0.0192308) | 0.615127 ± 0.103943 (W 0.00160664) | 6.09393 ± 0.0120763 (W 0.0139853) | 🔴 fork 6.99× slower than `faer-pool` | 🔵 fork 1.42× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_full/n8/b1` | 0.015509 ± 0.000156205 (W 6.14923e-05) | 0.015319 ± 5.11892e-05 (W 5.08262e-05) | 0.017923 ± 4.58258e-05 (W 5.31536e-05) | · | 🔵 fork 1.16× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 15.1712 ± 0.04754 (W 0.0349145) | 1.97994 ± 0.0402158 (W 0.0188834) | 18.5869 ± 0.0276061 (W 0.0289862) | 🔴 fork 7.66× slower than `faer-pool` | 🔵 fork 1.23× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1` | 0.054601 ± 0.000293746 (W 0.000161029) | 0.055032 ± 0.000399151 (W 7.95883e-05) | 0.050995 ± 5.56776e-05 (W 0.00165675) | · | 🔴 fork 1.07× slower than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 55.6504 ± 0.124348 (W 0.0545388) | 7.1158 ± 0.0591437 (W 0.0614177) | 51.523 ± 0.20934 (W 0.169419) | 🔴 fork 7.82× slower than `faer-pool` | 🔴 fork 1.08× slower than `lapack-mkl` |  |
| `svd_thin/n4/b1` | 0.004859 ± 4.72582e-05 (W 6.05805e-05) | 0.004909 ± 6.4291e-05 (W 7.84219e-05) | 0.006543 ± 6.02246e-05 (W 7.71706e-05) | · | 🔵 fork 1.35× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 4.26564 ± 0.0230404 (W 0.011078) | 0.5843 ± 0.0316285 (W 0.00203408) | 6.09894 ± 0.00894518 (W 0.0141044) | 🔴 fork 7.30× slower than `faer-pool` | 🔵 fork 1.43× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n8/b1` | 0.015209 ± 0.000217025 (W 6.89949e-05) | 0.015619 ± 0.000295794 (W 0.000161531) | 0.017844 ± 5.62168e-05 (W 2.89862e-05) | · | 🔵 fork 1.17× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 15.205 ± 0.0217606 (W 0.0249362) | 1.93623 ± 0.131484 (W 0.00361373) | 18.5869 ± 0.0213054 (W 0.0284984) | 🔴 fork 7.85× slower than `faer-pool` | 🔵 fork 1.22× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1` | 0.040335 ± 0.000130512 (W 0.000123289) | 0.040145 ± 0.00013 (W 0.000135353) | 0.018494 ± 5.56507e-05 (W 0.00177329) | · | 🔴 fork 2.18× slower than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 40.8146 ± 0.215562 (W 0.0551798) | 5.16846 ± 0.0139466 (W 0.0177118) | 19.3429 ± 0.0496307 (W 0.0175835) | 🔴 fork 7.90× slower than `faer-pool` | 🔴 fork 2.11× slower than `lapack-mkl` |  |
| `svd_values/n4/b1` | 0.003808 ± 6.16468e-05 (W 0.000149064) | 0.003868 ± 2.5697e-05 (W 0.000184001) | 0.003105 ± 2.0664e-05 (W 4.219e-05) | · | 🔴 fork 1.23× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.18464 ± 0.0115417 (W 0.00306546) | 0.412128 ± 0.00292726 (W 0.00165453) | 2.65601 ± 0.00535896 (W 0.00475875) | 🔴 fork 7.73× slower than `faer-pool` | 🔴 fork 1.20× slower than `lapack-mkl` |  |
| `svd_values/n8/b1` | 0.011602 ± 2.5632e-05 (W 0.000108103) | 0.011612 ± 6.46555e-05 (W 7.71317e-05) | 0.006793 ± 1.00167e-05 (W 4.62093e-05) | · | 🔴 fork 1.71× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 11.2951 ± 0.0250975 (W 0.0185442) | 1.43977 ± 0.00334673 (W 0.00498836) | 6.67845 ± 0.00493908 (W 0.0160584) | 🔴 fork 7.85× slower than `faer-pool` | 🔴 fork 1.69× slower than `lapack-mkl` |  |
| `triangular_solve/n16/b1` | 0.001011 ± 4.17971e-05 (W 5.95819e-05) | 0.000982 ± 2.64575e-05 (W 5.3331e-05) | 0.000892 ± 1.1547e-05 (W 3.44848e-05) | · | 🔴 fork 1.13× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.506414 ± 0.00128018 (W 0.00295687) | 0.085139 ± 0.000838743 (W 0.00269219) | 0.588097 ± 0.00166763 (W 0.00425914) | 🔴 fork 5.95× slower than `faer-pool` | 🔵 fork 1.16× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1` | 0.000612 ± 2.6839e-05 (W 4.98116e-05) | 0.000611 ± 6.20511e-05 (W 5.92638e-05) | 0.000641 ± 1e-05 (W 5.06952e-05) | · | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.087623 ± 0.000181357 (W 0.000215422) | 0.022872 ± 0.00350008 (W 0.00244822) | 0.293277 ± 0.000255147 (W 0.00310747) | 🔴 fork 3.83× slower than `faer-pool` | 🔵 fork 3.35× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n8/b1` | 0.000722 ± 1.53948e-05 (W 4.77493e-05) | 0.000772 ± 6.02771e-05 (W 4.59489e-05) | 0.000701 ± 5.50757e-06 (W 3.19578e-05) | · | · | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.219709 ± 0.000818819 (W 0.00175625) | 0.034895 ± 0.000437769 (W 0.00081149) | 0.390628 ± 0.00164166 (W 0.00260375) | 🔴 fork 6.30× slower than `faer-pool` | 🔵 fork 1.78× faster than `lapack-mkl` |  |

## batch-small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001593 ± 2.08167e-05 (W 1.87083e-05) | - | 0.001924 ± 1.21244e-05 (W 1.66523e-05) | - | 🔵 fork 1.21× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 1.3029 ± 0.00526383 (W 0.00538724) | - | 1.82363 ± 0.0210314 (W 0.00870397) | - | 🔵 fork 1.40× faster than `lapack-mkl` | `*` one row has no measurement here |
| `cholesky/n4/b1` | 0.000581 ± 5.7735e-06 (W 0.000105694) | - | 0.000361 ± 6.08276e-06 (W 2.95008e-05) | - | 🔴 fork 1.61× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.197809 ± 0.000856453 (W 0.00114334) | - | 0.17701 ± 0.000494975 (W 0.00136957) | - | 🔴 fork 1.12× slower than `lapack-mkl` | `*` one row has no measurement here |
| `cholesky/n8/b1` | 0.000832 ± 2.5697e-05 (W 3.06806e-05) | - | 0.000651 ± 1.52753e-05 (W 2.1822e-05) | - | 🔴 fork 1.28× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.425043 ± 0.00628018 (W 0.00273857) | - | 0.477921 ± 0.0133313 (W 0.00258507) | - | 🔵 fork 1.12× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `eig/n16/b1` | 0.122408 ± 0.000278342 (W 0.00167896) | - | 0.165849 ± 0.000303355 (W 0.00119845) | - | 🔵 fork 1.35× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n16/b1024` | 128.98 ± 0.119866 (W 0.0656819) | - | 178.223 ± 0.207899 (W 0.404802) | - | 🔵 fork 1.38× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n4/b1` | 0.01033 ± 0.000125381 (W 0.000179781) | - | 0.012814 ± 1.73205e-05 (W 5.94668e-05) | - | 🔵 fork 1.24× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 9.99751 ± 0.034137 (W 0.0148457) | - | 12.4808 ± 0.0163405 (W 0.0314334) | - | 🔵 fork 1.25× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n8/b1` | 0.034394 ± 0.000285365 (W 0.000242834) | - | 0.041628 ± 0.000133167 (W 8.25245e-05) | - | 🔵 fork 1.21× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eig/n8/b1024` | 34.8256 ± 0.204006 (W 0.0383975) | - | 43.323 ± 0.0124246 (W 0.0392454) | - | 🔵 fork 1.24× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigh/n16/b1` | 0.030416 ± 0.00010591 (W 0.000135541) | - | 0.031008 ± 0.000334207 (W 0.0015758) | - | · | `*` one row has no measurement here |
| `eigh/n16/b1024` | 32.2701 ± 0.0318982 (W 0.0346396) | - | 32.362 ± 0.135472 (W 0.0267135) | - | · | `*` one row has no measurement here |
| `eigh/n4/b1` | 0.003487 ± 5.54106e-05 (W 7.29328e-05) | - | 0.003025 ± 6.35085e-06 (W 6.6025e-05) | - | 🔴 fork 1.15× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.89882 ± 0.00535791 (W 0.00235439) | - | 2.82311 ± 0.00485401 (W 0.00293767) | - | · | `*` one row has no measurement here |
| `eigh/n8/b1` | 0.009658 ± 7e-05 (W 7.29328e-05) | - | 0.008806 ± 3.00056e-05 (W 3.695e-05) | - | 🔴 fork 1.10× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 9.11082 ± 0.053325 (W 0.0130546) | - | 8.92595 ± 0.0232099 (W 0.00994887) | - | · | `*` one row has no measurement here |
| `eigvals/n16/b1` | 0.072525 ± 0.000123452 (W 0.000199593) | - | 0.113692 ± 0.000240069 (W 0.000192635) | - | 🔵 fork 1.57× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigvals/n16/b1024` | 77.3024 ± 0.08113 (W 0.387526) | - | 125.099 ± 0.261772 (W 0.189096) | - | 🔵 fork 1.62× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigvals/n4/b1` | 0.00532 ± 2.5697e-05 (W 6.03755e-05) | - | 0.010098 ± 3.80832e-05 (W 4.30116e-05) | - | 🔵 fork 1.90× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 4.79636 ± 0.0329532 (W 0.0127233) | - | 9.58629 ± 0.0168526 (W 0.0132743) | - | 🔵 fork 2.00× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigvals/n8/b1` | 0.019787 ± 0.000146936 (W 0.000145135) | - | 0.032581 ± 9.0185e-05 (W 1.67332e-05) | - | 🔵 fork 1.65× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 19.8574 ± 0.0986982 (W 0.0146218) | - | 34.4165 ± 0.0586476 (W 0.0438379) | - | 🔵 fork 1.73× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n16/b1` | 0.022943 ± 9.97848e-05 (W 8.50294e-05) | - | 0.017914 ± 7.0946e-05 (W 4.14524e-05) | - | 🔴 fork 1.28× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n16/b1024` | 23.8042 ± 0.0366444 (W 0.0341841) | - | 18.4313 ± 0.0187227 (W 0.0293855) | - | 🔴 fork 1.29× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n4/b1` | 0.002976 ± 2.13776e-05 (W 0.000110839) | - | 0.002214 ± 1e-05 (W 3.76191e-05) | - | 🔴 fork 1.34× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 2.40268 ± 0.00584715 (W 0.00738926) | - | 1.78602 ± 0.00962583 (W 0.000877011) | - | 🔴 fork 1.35× slower than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n8/b1` | 0.007945 ± 3.60555e-05 (W 7.04152e-05) | - | 0.00585 ± 6.72632e-05 (W 2.77705e-05) | - | 🔴 fork 1.36× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 7.28555 ± 0.0327152 (W 0.0131674) | - | 5.59198 ± 0.0161773 (W 0.00906191) | - | 🔴 fork 1.30× slower than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu/n16/b1` | 0.005039 ± 0.000231517 (W 6.92048e-05) | - | 0.004959 ± 2.46374e-05 (W 2.52052e-05) | - | · | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 4.20301 ± 0.0194958 (W 0.0108825) | - | 5.50378 ± 0.0168165 (W 0.0156108) | - | 🔵 fork 1.31× faster than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu/n4/b1` | 0.001172 ± 1.53948e-05 (W 5.49209e-05) | - | 0.000812 ± 6.35085e-06 (W 5.0022e-05) | - | 🔴 fork 1.44× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.451141 ± 0.00823349 (W 0.0036928) | - | 0.524399 ± 0.00135785 (W 0.00286858) | - | 🔵 fork 1.16× faster than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu/n8/b1` | 0.002164 ± 1.73205e-05 (W 0.000171919) | - | 0.001613 ± 5.7735e-06 (W 3.03315e-05) | - | 🔴 fork 1.34× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.24341 ± 0.0541515 (W 0.00874099) | - | 1.2945 ± 0.020014 (W 0.00519993) | - | · | `*` one row has no measurement here; `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1` | 0.006292 ± 5.18684e-05 (W 6.68154e-05) | - | 0.008876 ± 7.59408e-05 (W 4.78048e-05) | - | 🔵 fork 1.41× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 5.26013 ± 0.06853 (W 0.009404) | - | 8.47643 ± 0.0224378 (W 0.0169594) | - | 🔵 fork 1.61× faster than `lapack-mkl` | `*` one row has no measurement here |
| `full_piv_lu_solve/n4/b1` | 0.001643 ± 6.02771e-05 (W 6.74181e-05) | - | 0.002104 ± 1e-05 (W 6.20484e-05) | - | 🔵 fork 1.28× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.756721 ± 0.0301536 (W 0.00351452) | - | 1.5901 ± 0.00646894 (W 0.00485118) | - | 🔵 fork 2.10× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1` | 0.002905 ± 6.08276e-06 (W 7.77515e-05) | - | 0.003717 ± 4.16333e-05 (W 3.89872e-05) | - | 🔵 fork 1.28× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.90803 ± 0.00563856 (W 0.00840173) | - | 3.17594 ± 0.00509917 (W 0.00899093) | - | 🔵 fork 1.66× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_apply/n16/b1` | 0.004779 ± 8.38272e-05 (W 3.52307e-05) | - | 0.005931 ± 5.05008e-05 (W 3.55289e-05) | - | 🔵 fork 1.24× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 5.31216 ± 0.0503453 (W 0.0201094) | - | 6.29918 ± 0.0408951 (W 0.0124486) | - | 🔵 fork 1.19× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_apply/n4/b1` | 0.000601 ± 5.7735e-06 (W 0.000121812) | - | 0.000861 ± 2.0664e-05 (W 1.6947e-05) | - | 🔵 fork 1.43× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.341778 ± 0.00655317 (W 0.00301624) | - | 0.428077 ± 0.00484617 (W 0.00328522) | - | 🔵 fork 1.25× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_apply/n8/b1` | 0.001313 ± 3.55949e-05 (W 6.13531e-05) | - | 0.001653 ± 1.47309e-05 (W 2.68328e-05) | - | 🔵 fork 1.26× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.12284 ± 0.0140338 (W 0.00243576) | - | 1.30643 ± 0.00173183 (W 0.00373285) | - | 🔵 fork 1.16× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_factor/n16/b1` | 0.004609 ± 2.64575e-05 (W 5.14519e-05) | - | 0.006302 ± 2.88675e-05 (W 2.79142e-05) | - | 🔵 fork 1.37× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 4.46302 ± 0.0311175 (W 0.0113642) | - | 6.32365 ± 0.020478 (W 0.0134985) | - | 🔵 fork 1.42× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_factor/n4/b1` | 0.000762 ± 1.73205e-05 (W 2.43783e-05) | - | 0.000761 ± 5.7735e-07 (W 1.75585e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.544014 ± 0.00371861 (W 0.00207517) | - | 0.518596 ± 0.002065 (W 0.00218615) | - | · | `*` one row has no measurement here |
| `householder_factor/n8/b1` | 0.001643 ± 1.73205e-05 (W 1.67332e-05) | - | 0.001734 ± 2.95014e-05 (W 3.06154e-05) | - | 🔵 fork 1.06× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.42735 ± 0.00947123 (W 0.00380721) | - | 1.48852 ± 0.00446353 (W 0.00528837) | - | · | `*` one row has no measurement here |
| `lu/n16/b1` | 0.003717 ± 0.000133167 (W 7.19722e-05) | - | 0.003556 ± 3.10966e-05 (W 3.41511e-05) | - | · | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 3.10156 ± 0.0384754 (W 0.00987945) | - | 3.62794 ± 0.0192268 (W 0.00962996) | - | 🔵 fork 1.17× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu/n4/b1` | 0.000872 ± 2.04206e-05 (W 8.44707e-05) | - | 0.000551 ± 5.7735e-06 (W 3.8784e-05) | - | 🔴 fork 1.58× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.363548 ± 0.00606247 (W 0.00305308) | - | 0.282637 ± 0.000308293 (W 0.00185565) | - | 🔴 fork 1.29× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu/n8/b1` | 0.001603 ± 0.000114282 (W 5.41295e-05) | - | 0.001152 ± 3e-05 (W 2e-05) | - | 🔴 fork 1.39× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.946364 ± 0.0177885 (W 0.00626013) | - | 0.893856 ± 0.00855157 (W 0.00271915) | - | 🔴 fork 1.06× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor/n16/b1` | 0.002315 ± 1.67432e-05 (W 8.04506e-05) | - | 0.002655 ± 1e-05 (W 2.38747e-05) | - | 🔵 fork 1.15× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 2.12019 ± 0.0132201 (W 0.00493641) | - | 2.66403 ± 0.0236275 (W 0.00277222) | - | 🔵 fork 1.26× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor/n4/b1` | 0.000571 ± 1.1547e-05 (W 5.35724e-05) | - | 0.00029 ± 1.18462e-05 (W 2.4682e-05) | - | 🔴 fork 1.97× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.274161 ± 0.00206791 (W 0.00268687) | - | 0.183532 ± 0.000444119 (W 0.00151843) | - | 🔴 fork 1.49× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor/n8/b1` | 0.000982 ± 2.08167e-05 (W 3.11448e-05) | - | 0.000671 ± 5.7735e-06 (W 8.84308e-06) | - | 🔴 fork 1.46× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.695308 ± 0.00974627 (W 0.00397036) | - | 0.61652 ± 0.00474159 (W 0.00198477) | - | 🔴 fork 1.13× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor_solve/n16/b1` | 0.003998 ± 5.80259e-05 (W 2.92113e-05) | - | 0.00527 ± 1.52753e-05 (W 2.58844e-05) | - | 🔵 fork 1.32× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 3.51193 ± 0.0144916 (W 0.0170813) | - | 5.28815 ± 0.028033 (W 0.00501378) | - | 🔵 fork 1.51× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor_solve/n4/b1` | 0.000792 ± 1.52753e-05 (W 2.82188e-05) | - | 0.000541 ± 1.52753e-05 (W 2.09332e-05) | - | 🔴 fork 1.46× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.425293 ± 0.002996 (W 0.00357303) | - | 0.417589 ± 0.00116181 (W 0.00247554) | - | · | `*` one row has no measurement here |
| `lu_factor_solve/n8/b1` | 0.001703 ± 0.000117304 (W 6.41872e-05) | - | 0.001723 ± 5.7735e-06 (W 3.11448e-05) | - | · | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 1.1821 ± 0.0270087 (W 0.00473872) | - | 1.66389 ± 0.00366158 (W 0.00301969) | - | 🔵 fork 1.41× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_solve_prepared/n16/b1` | 0.001553 ± 2.3094e-05 (W 4.35683e-05) | - | 0.002615 ± 2e-05 (W 2.28035e-05) | - | 🔵 fork 1.68× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 1.28855 ± 0.00316049 (W 0.00173221) | - | 2.61569 ± 0.0236408 (W 0.00576233) | - | 🔵 fork 2.03× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_solve_prepared/n4/b1` | 0.000451 ± 2.13776e-05 (W 3.53553e-05) | - | 0.00035 ± 5.50757e-06 (W 2.02534e-05) | - | 🔴 fork 1.29× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.162102 ± 0.000104978 (W 0.00176354) | - | 0.24136 ± 0.000261547 (W 0.00143588) | - | 🔵 fork 1.49× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_solve_prepared/n8/b1` | 0.000782 ± 1.0504e-05 (W 4.84066e-05) | - | 0.001132 ± 0 (W 8.84308e-06) | - | 🔵 fork 1.45× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.475556 ± 0.00205385 (W 0.00300029) | - | 1.06953 ± 0.00292635 (W 0.00177013) | - | 🔵 fork 2.25× faster than `lapack-mkl` | `*` one row has no measurement here |
| `qr/n16/b1` | 0.011321 ± 1.73205e-05 (W 0.000149249) | - | 0.01074 ± 3.05505e-05 (W 4.32435e-05) | - | 🔴 fork 1.05× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 10.9252 ± 0.054794 (W 0.0324448) | - | 10.6794 ± 0.0283313 (W 0.0324507) | - | · | `*` one row has no measurement here |
| `qr/n4/b1` | 0.001432 ± 5.7735e-06 (W 3.34709e-05) | - | 0.001503 ± 1.0504e-05 (W 4.98929e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.872868 ± 0.0072037 (W 0.00182414) | - | 0.926958 ± 0.0187514 (W 0.00200957) | - | 🔵 fork 1.06× faster than `lapack-mkl` | `*` one row has no measurement here |
| `qr/n8/b1` | 0.003256 ± 3.51188e-05 (W 0.000105458) | - | 0.003256 ± 3.4641e-05 (W 4.15933e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.62584 ± 0.0132999 (W 0.00308863) | - | 2.67895 ± 0.00368307 (W 0.00550811) | - | · | `*` one row has no measurement here |
| `rank_revealing_qr/n16/b1` | 0.012764 ± 1e-05 (W 0.000121788) | - | 0.015749 ± 6.08276e-05 (W 4.72261e-05) | - | 🔵 fork 1.23× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 12.3027 ± 0.0578553 (W 0.0186662) | - | 15.9061 ± 0.0169748 (W 0.04363) | - | 🔵 fork 1.29× faster than `lapack-mkl` | `*` one row has no measurement here |
| `rank_revealing_qr/n4/b1` | 0.002154 ± 1.52753e-05 (W 2.72819e-05) | - | 0.002555 ± 2.3094e-05 (W 5.00829e-05) | - | 🔵 fork 1.19× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.43851 ± 0.00339881 (W 0.00625264) | - | 1.75405 ± 0.00505058 (W 0.00548179) | - | 🔵 fork 1.22× faster than `lapack-mkl` | `*` one row has no measurement here |
| `rank_revealing_qr/n8/b1` | 0.004438 ± 2.02567e-05 (W 3.64692e-05) | - | 0.00537 ± 4.04145e-05 (W 5.93296e-05) | - | 🔵 fork 1.21× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.73611 ± 0.0116543 (W 0.00467435) | - | 4.78498 ± 0.0165085 (W 0.00878465) | - | 🔵 fork 1.28× faster than `lapack-mkl` | `*` one row has no measurement here |
| `solve/n16/b1` | 0.00496 ± 7.08543e-05 (W 0.000126417) | - | 0.00582 ± 5.02693e-05 (W 5.27257e-05) | - | 🔵 fork 1.17× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 3.90149 ± 0.0435848 (W 0.0107234) | - | 5.53233 ± 0.0388805 (W 0.00889311) | - | 🔵 fork 1.42× faster than `lapack-mkl` | `*` one row has no measurement here |
| `solve/n4/b1` | 0.001503 ± 4.6188e-05 (W 7.28011e-05) | - | 0.000841 ± 1.67432e-05 (W 1.81191e-05) | - | 🔴 fork 1.79× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.533044 ± 0.00684262 (W 0.00428911) | - | 0.483001 ± 0.0049197 (W 0.00205391) | - | 🔴 fork 1.10× slower than `lapack-mkl` | `*` one row has no measurement here |
| `solve/n8/b1` | 0.002574 ± 5.55908e-05 (W 7.76292e-05) | - | 0.002054 ± 3.60555e-05 (W 1.30384e-05) | - | 🔴 fork 1.25× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 1.33637 ± 0.0108319 (W 0.00466459) | - | 1.75928 ± 0.0270974 (W 0.00475863) | - | 🔵 fork 1.32× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_full/n16/b1` | 0.057998 ± 6.35085e-06 (W 0.000188762) | - | 0.065903 ± 0.000271165 (W 0.000114586) | - | 🔵 fork 1.14× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_full/n16/b1024` | 60.303 ± 5.73759 (W 0.0461502) | - | 67.6922 ± 0.0837402 (W 0.0850974) | - | 🔵 fork 1.12× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5% |
| `svd_full/n4/b1` | 0.00527 ± 2.3094e-05 (W 0.000208171) | - | 0.007875 ± 3.21455e-05 (W 3.64692e-05) | - | 🔵 fork 1.49× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 5.00163 ± 0.00174171 (W 0.00413901) | - | 7.47158 ± 0.0168156 (W 0.0112107) | - | 🔵 fork 1.49× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_full/n8/b1` | 0.01629 ± 5.31068e-05 (W 0.000139597) | - | 0.021069 ± 7.02163e-05 (W 5.59214e-05) | - | 🔵 fork 1.29× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 16.781 ± 0.0632843 (W 0.0302053) | - | 22.2268 ± 0.027241 (W 0.0276562) | - | 🔵 fork 1.32× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n16/b1` | 0.058328 ± 0.00148454 (W 0.00023774) | - | 0.065512 ± 6.80686e-05 (W 9.93136e-05) | - | 🔵 fork 1.12× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n16/b1024` | 60.4129 ± 0.046603 (W 0.0326305) | - | 67.5765 ± 0.0862379 (W 0.395619) | - | 🔵 fork 1.12× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n4/b1` | 0.005259 ± 4.0501e-05 (W 2.08399e-05) | - | 0.007824 ± 1.51767e-05 (W 0.000111518) | - | 🔵 fork 1.49× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 5.00422 ± 0.0395168 (W 0.0108392) | - | 7.45223 ± 0.00429635 (W 0.0156987) | - | 🔵 fork 1.49× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n8/b1` | 0.01629 ± 5.04017e-05 (W 7.09521e-05) | - | 0.02106 ± 3.06649e-05 (W 3.46742e-05) | - | 🔵 fork 1.29× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 16.8078 ± 0.0599054 (W 0.0254125) | - | 22.2318 ± 0.0382311 (W 0.0229318) | - | 🔵 fork 1.32× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n16/b1` | 0.043802 ± 0.000195244 (W 0.000111536) | - | 0.027411 ± 0.000254146 (W 7.61577e-05) | - | 🔴 fork 1.60× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n16/b1024` | 45.5437 ± 0.111283 (W 0.0522451) | - | 28.2173 ± 0.0495092 (W 0.0214639) | - | 🔴 fork 1.61× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n4/b1` | 0.004258 ± 1.1547e-05 (W 9.5289e-05) | - | 0.003857 ± 1.52753e-05 (W 4.75521e-05) | - | 🔴 fork 1.10× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.84753 ± 0.00759773 (W 0.00472706) | - | 3.51192 ± 0.00628368 (W 0.00330437) | - | 🔴 fork 1.10× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n8/b1` | 0.012783 ± 5.53203e-05 (W 3.74059e-05) | - | 0.009016 ± 4.08697e-05 (W 4.46352e-05) | - | 🔴 fork 1.42× slower than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 12.9467 ± 0.0220362 (W 0.0275015) | - | 9.13471 ± 0.0176425 (W 0.0157198) | - | 🔴 fork 1.42× slower than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n16/b1` | 0.001473 ± 6.69104e-05 (W 2.94958e-05) | - | 0.001563 ± 1.52753e-05 (W 2.50998e-05) | - | 🔵 fork 1.06× faster than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.985037 ± 0.00687089 (W 0.00277406) | - | 1.37106 ± 0.025169 (W 0.00745712) | - | 🔵 fork 1.39× faster than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n4/b1` | 0.000732 ± 2.52389e-05 (W 3.72586e-05) | - | 0.000601 ± 1.73205e-05 (W 3.71106e-05) | - | 🔴 fork 1.22× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.162574 ± 0.000391716 (W 0.00233514) | - | 0.297905 ± 0.00176119 (W 0.00229968) | - | 🔵 fork 1.83× faster than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n8/b1` | 0.000971 ± 2.52389e-05 (W 0.000117369) | - | 0.000862 ± 1.12694e-05 (W 1.53069e-05) | - | 🔴 fork 1.13× slower than `lapack-mkl` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.39716 ± 0.000841531 (W 0.00299289) | - | 0.57389 ± 0.00324998 (W 0.0021803) | - | 🔵 fork 1.44× faster than `lapack-mkl` | `*` one row has no measurement here |

## batch-small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001653 ± 9.31504e-05 (W 5.12865e-05) | 0.001633 ± 8.14064e-05 (W 5.43259e-05) | 0.001913 ± 1.47309e-05 (W 1.65318e-05) | · | 🔵 fork 1.16× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 1.29814 ± 0.00881193 (W 0.00696182) | 0.172712 ± 0.00429976 (W 0.00270114) | 1.82413 ± 0.00861307 (W 0.00920606) | 🔴 fork 7.52× slower than `faer-pool` | 🔵 fork 1.41× faster than `lapack-mkl` |  |
| `cholesky/n4/b1` | 0.000621 ± 5.7735e-06 (W 4.32458e-05) | 0.000611 ± 5.7735e-06 (W 2.5044e-05) | 0.000361 ± 5.7735e-06 (W 1.51658e-05) | · | 🔴 fork 1.72× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.19821 ± 0.000698191 (W 0.00153457) | 0.03249 ± 0.000255069 (W 0.000340118) | 0.17706 ± 0.000537799 (W 0.00148332) | 🔴 fork 6.10× slower than `faer-pool` | 🔴 fork 1.12× slower than `lapack-mkl` |  |
| `cholesky/n8/b1` | 0.000861 ± 3.04467e-05 (W 4.41396e-05) | 0.000861 ± 1.12694e-05 (W 2.93292e-05) | 0.000651 ± 5.7735e-06 (W 5.21536e-06) | · | 🔴 fork 1.32× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.419652 ± 0.0103945 (W 0.00227437) | 0.062347 ± 0.00127835 (W 0.0020285) | 0.469786 ± 0.010426 (W 0.00249325) | 🔴 fork 6.73× slower than `faer-pool` | 🔵 fork 1.12× faster than `lapack-mkl` |  |
| `eig/n16/b1` | 0.122469 ± 0.000337147 (W 0.000408379) | 0.122529 ± 0.000321623 (W 0.0012573) | 0.163966 ± 0.000389051 (W 0.00169459) | · | 🔵 fork 1.34× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 128.89 ± 0.35528 (W 0.226118) | 16.4525 ± 0.0308307 (W 0.0341772) | 175.214 ± 0.33905 (W 0.38012) | 🔴 fork 7.83× slower than `faer-pool` | 🔵 fork 1.36× faster than `lapack-mkl` |  |
| `eig/n4/b1` | 0.01037 ± 0.000135094 (W 0.000116787) | 0.0105 ± 0.0001505 (W 0.000158124) | 0.012844 ± 5.74195e-05 (W 7.53737e-05) | · | 🔵 fork 1.24× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 10.0029 ± 0.0338467 (W 0.021735) | 1.33279 ± 0.0154426 (W 0.00509757) | 12.4614 ± 0.0150312 (W 0.0199109) | 🔴 fork 7.51× slower than `faer-pool` | 🔵 fork 1.25× faster than `lapack-mkl` |  |
| `eig/n8/b1` | 0.034334 ± 0.000261 (W 0.000168684) | 0.034234 ± 0.00017091 (W 0.000225693) | 0.041657 ± 8.05005e-05 (W 6.11253e-05) | · | 🔵 fork 1.21× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 35.0945 ± 0.22968 (W 0.214402) | 4.4692 ± 0.0185522 (W 0.0152833) | 43.2834 ± 0.090218 (W 0.034678) | 🔴 fork 7.85× slower than `faer-pool` | 🔵 fork 1.23× faster than `lapack-mkl` |  |
| `eigh/n16/b1` | 0.030577 ± 8.0829e-05 (W 0.000120955) | 0.030507 ± 0.000116477 (W 8.81476e-05) | 0.030988 ± 0.00015201 (W 9.40744e-05) | · | · |  |
| `eigh/n16/b1024` | 32.0685 ± 0.0963081 (W 0.022468) | 4.05587 ± 0.0408398 (W 0.0104098) | 32.2847 ± 0.0682927 (W 0.0797864) | 🔴 fork 7.91× slower than `faer-pool` | · |  |
| `eigh/n4/b1` | 0.003547 ± 7.37111e-05 (W 6.35232e-05) | 0.003566 ± 5.55908e-05 (W 6.39398e-05) | 0.003045 ± 2.58908e-05 (W 4.22398e-05) | · | 🔴 fork 1.16× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.88331 ± 0.0370477 (W 0.00911871) | 0.372906 ± 0.00112649 (W 0.00187918) | 2.81187 ± 0.0115031 (W 0.00311647) | 🔴 fork 7.73× slower than `faer-pool` | · |  |
| `eigh/n8/b1` | 0.009768 ± 7.76745e-05 (W 9.20771e-05) | 0.009799 ± 5.02693e-05 (W 7.76228e-05) | 0.008757 ± 1.70392e-05 (W 2.34158e-05) | · | 🔴 fork 1.12× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 9.13348 ± 0.0644626 (W 0.0108884) | 1.15603 ± 0.00210301 (W 0.00599733) | 8.95303 ± 0.0633447 (W 0.0100408) | 🔴 fork 7.90× slower than `faer-pool` | · |  |
| `eigvals/n16/b1` | 0.072776 ± 0.000167004 (W 0.000174385) | 0.072785 ± 0.000479504 (W 0.00104627) | 0.113913 ± 9.48174e-05 (W 0.00129041) | · | 🔵 fork 1.57× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 77.2591 ± 0.294136 (W 0.0451476) | 9.73945 ± 3.61459 (W 0.00875482) | 124.851 ± 0.302503 (W 0.0698122) | 🔴 fork 7.93× slower than `faer-pool` | 🔵 fork 1.62× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigvals/n4/b1` | 0.0054 ± 0.000115889 (W 0.000120317) | 0.00556 ± 0.000150921 (W 0.000125452) | 0.010099 ± 3.51188e-05 (W 6.76018e-05) | · | 🔵 fork 1.87× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 4.78966 ± 0.0893938 (W 0.0196115) | 0.61609 ± 0.0104012 (W 0.00530601) | 9.56955 ± 0.0109872 (W 0.0101843) | 🔴 fork 7.77× slower than `faer-pool` | 🔵 fork 2.00× faster than `lapack-mkl` |  |
| `eigvals/n8/b1` | 0.019697 ± 3.78594e-05 (W 0.000125499) | 0.019937 ± 0.000110604 (W 0.00141932) | 0.032601 ± 4.16333e-05 (W 6.30079e-05) | · | 🔵 fork 1.66× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 19.7925 ± 0.0414464 (W 0.0173583) | 2.52968 ± 0.0052858 (W 0.00823686) | 34.3928 ± 0.044738 (W 0.0213305) | 🔴 fork 7.82× slower than `faer-pool` | 🔵 fork 1.74× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1` | 0.022852 ± 9.61787e-05 (W 0.00012482) | 0.022943 ± 4.6188e-05 (W 0.000138862) | 0.017924 ± 1.52753e-05 (W 3.03035e-05) | · | 🔴 fork 1.27× slower than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 23.8976 ± 0.108496 (W 0.0150795) | 3.01052 ± 0.00127661 (W 0.00996461) | 18.392 ± 0.013426 (W 0.0203479) | 🔴 fork 7.94× slower than `faer-pool` | 🔴 fork 1.30× slower than `lapack-mkl` |  |
| `eigvalsh/n4/b1` | 0.003036 ± 4.78226e-05 (W 0.000125842) | 0.003005 ± 4.50925e-05 (W 0.000131351) | 0.002214 ± 2.5632e-05 (W 2.87611e-05) | · | 🔴 fork 1.37× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 2.40015 ± 0.00721869 (W 0.00460314) | 0.31099 ± 0.000833796 (W 0.00233319) | 1.784 ± 0.0033805 (W 0.00626368) | 🔴 fork 7.72× slower than `faer-pool` | 🔴 fork 1.35× slower than `lapack-mkl` |  |
| `eigvalsh/n8/b1` | 0.008025 ± 5.1316e-05 (W 0.00138761) | 0.007985 ± 6.50641e-05 (W 4.82203e-05) | 0.005841 ± 1.73205e-05 (W 3.27109e-05) | · | 🔴 fork 1.37× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 7.33294 ± 0.0399626 (W 0.0129864) | 0.928763 ± 0.00211721 (W 0.00344828) | 5.56474 ± 0.0155754 (W 0.00794765) | 🔴 fork 7.90× slower than `faer-pool` | 🔴 fork 1.32× slower than `lapack-mkl` |  |
| `full_piv_lu/n16/b1` | 0.00505 ± 8.87149e-05 (W 7.41768e-05) | 0.00511 ± 8.66622e-05 (W 6.02271e-05) | 0.004919 ± 3.05505e-05 (W 4.20143e-05) | · | · | dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 4.28319 ± 0.0578188 (W 0.0145858) | 0.623665 ± 0.282463 (W 0.00726431) | 5.52087 ± 0.124572 (W 0.017749) | 🔴 fork 6.87× slower than `faer-pool` | 🔵 fork 1.29× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `full_piv_lu/n4/b1` | 0.001182 ± 2.51661e-05 (W 6.80162e-05) | 0.001223 ± 1.12694e-05 (W 5.28044e-05) | 0.000811 ± 1.48436e-05 (W 3.83054e-05) | · | 🔴 fork 1.46× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.456531 ± 0.0048846 (W 0.00441262) | 0.087483 ± 0.00170007 (W 0.00140256) | 0.522295 ± 0.00708554 (W 0.00392117) | 🔴 fork 5.22× slower than `faer-pool` | 🔵 fork 1.14× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1` | 0.002254 ± 9.50438e-05 (W 5.8798e-05) | 0.002294 ± 3.4641e-05 (W 6.50484e-05) | 0.001623 ± 1.78979e-05 (W 4.43847e-05) | · | 🔴 fork 1.39× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.23844 ± 0.00888401 (W 0.00599277) | 0.196456 ± 0.00252262 (W 0.00376163) | 1.27053 ± 0.0104513 (W 0.00450533) | 🔴 fork 6.30× slower than `faer-pool` | · |  |
| `full_piv_lu_solve/n16/b1` | 0.006262 ± 0.000117205 (W 5.04975e-05) | 0.006302 ± 5.55908e-05 (W 0.000109226) | 0.008867 ± 9.16515e-05 (W 6.90456e-05) | · | 🔵 fork 1.42× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 5.12064 ± 0.0406501 (W 0.0275915) | 0.689637 ± 0.00519037 (W 0.0133299) | 8.45243 ± 0.0707066 (W 0.0155311) | 🔴 fork 7.43× slower than `faer-pool` | 🔵 fork 1.65× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1` | 0.001643 ± 2e-05 (W 5.59464e-05) | 0.001693 ± 4.41626e-05 (W 5.81378e-05) | 0.002104 ± 1e-05 (W 5.02215e-05) | · | 🔵 fork 1.28× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.746123 ± 0.00230504 (W 0.00290191) | 0.103162 ± 0.000759369 (W 0.00165525) | 1.58485 ± 0.00619619 (W 0.00358642) | 🔴 fork 7.23× slower than `faer-pool` | 🔵 fork 2.12× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1` | 0.002925 ± 4.07063e-05 (W 7.46324e-05) | 0.002895 ± 1.52753e-05 (W 5.67477e-05) | 0.003707 ± 1.52753e-05 (W 2.73861e-05) | · | 🔵 fork 1.27× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.83304 ± 0.00695765 (W 0.0150521) | 0.258382 ± 0.00258301 (W 0.0015648) | 3.16319 ± 0.0138929 (W 0.00556307) | 🔴 fork 7.09× slower than `faer-pool` | 🔵 fork 1.73× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1` | 0.004709 ± 7.0946e-05 (W 4.77493e-05) | 0.004699 ± 3.98372e-05 (W 4.50355e-05) | 0.005871 ± 0.000104083 (W 3.6417e-05) | · | 🔵 fork 1.25× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 5.11984 ± 0.0381973 (W 0.014325) | 0.627121 ± 0.0179254 (W 0.00659776) | 6.33638 ± 0.365812 (W 0.0403867) | 🔴 fork 8.16× slower than `faer-pool` | 🔵 fork 1.24× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `householder_apply/n4/b1` | 0.000631 ± 1.52753e-05 (W 2.67245e-05) | 0.000661 ± 2.64575e-05 (W 3.47448e-05) | 0.000861 ± 6.35085e-06 (W 5.42245e-05) | · | 🔵 fork 1.36× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.338952 ± 0.00115776 (W 0.00316782) | 0.050635 ± 0.000675862 (W 0.000557704) | 0.422207 ± 0.0118181 (W 0.00416339) | 🔴 fork 6.69× slower than `faer-pool` | 🔵 fork 1.25× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1` | 0.001342 ± 3.55012e-05 (W 3.8887e-05) | 0.001323 ± 3.19427e-05 (W 2.97876e-05) | 0.001663 ± 5.50757e-05 (W 4.72366e-05) | · | 🔵 fork 1.24× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.12689 ± 0.0105059 (W 0.00308338) | 0.15516 ± 0.00284551 (W 0.00511056) | 1.27682 ± 0.0142329 (W 0.00511485) | 🔴 fork 7.26× slower than `faer-pool` | 🔵 fork 1.13× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1` | 0.004648 ± 2.60832e-05 (W 0.000128001) | 0.004659 ± 3.09892e-05 (W 6.26897e-05) | 0.006241 ± 1.95021e-05 (W 2.97708e-05) | · | 🔵 fork 1.34× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 4.45201 ± 0.00567498 (W 0.00911256) | 0.582067 ± 0.0043097 (W 0.00235713) | 6.29458 ± 0.018654 (W 0.0167597) | 🔴 fork 7.65× slower than `faer-pool` | 🔵 fork 1.41× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1` | 0.000781 ± 1.00167e-05 (W 3.98535e-05) | 0.000831 ± 1e-05 (W 3.68822e-05) | 0.000762 ± 5.7735e-07 (W 2.44806e-05) | 🔵 fork 1.06× faster than `faer-pool` | · | dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.549194 ± 0.00675604 (W 0.00200504) | 0.075251 ± 0.000115889 (W 0.000544407) | 0.51459 ± 0.00081798 (W 0.00215763) | 🔴 fork 7.30× slower than `faer-pool` | 🔴 fork 1.07× slower than `lapack-mkl` |  |
| `householder_factor/n8/b1` | 0.001633 ± 1.52753e-05 (W 4.32435e-05) | 0.001663 ± 2e-05 (W 3.39116e-05) | 0.001723 ± 1.51767e-05 (W 1.30077e-05) | · | 🔵 fork 1.06× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.44219 ± 0.0169848 (W 0.00426365) | 0.195585 ± 0.0024347 (W 0.00239556) | 1.48442 ± 0.00327347 (W 0.00304341) | 🔴 fork 7.37× slower than `faer-pool` | · |  |
| `lu/n16/b1` | 0.003747 ± 0.00012897 (W 4.61519e-05) | 0.003767 ± 0.000119304 (W 0.000134239) | 0.003556 ± 9.50438e-06 (W 1.77848e-05) | · | 🔴 fork 1.05× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 2.98715 ± 0.0715129 (W 0.0146058) | 0.442316 ± 0.0395135 (W 0.00649405) | 3.45652 ± 0.0770175 (W 0.00776792) | 🔴 fork 6.75× slower than `faer-pool` | 🔵 fork 1.16× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu/n4/b1` | 0.000822 ± 2.3388e-05 (W 6.30896e-05) | 0.000892 ± 2e-05 (W 8.31523e-05) | 0.000551 ± 1.52753e-05 (W 1.34164e-05) | 🔵 fork 1.09× faster than `faer-pool` | 🔴 fork 1.49× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.356044 ± 0.00341305 (W 0.00329886) | 0.071233 ± 0.00125182 (W 0.00179341) | 0.285622 ± 0.000928035 (W 0.00212558) | 🔴 fork 5.00× slower than `faer-pool` | 🔴 fork 1.25× slower than `lapack-mkl` |  |
| `lu/n8/b1` | 0.001623 ± 3.21455e-05 (W 9.0566e-05) | 0.001603 ± 1.58219e-05 (W 7.53658e-05) | 0.001162 ± 2.3094e-05 (W 2.34521e-05) | · | 🔴 fork 1.40× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.957155 ± 0.0166741 (W 0.00520439) | 0.153968 ± 0.0151504 (W 0.00167572) | 0.890951 ± 0.012858 (W 0.00154995) | 🔴 fork 6.22× slower than `faer-pool` | 🔴 fork 1.07× slower than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor/n16/b1` | 0.002335 ± 4.74377e-05 (W 0.000104016) | 0.002374 ± 0.000140571 (W 0.000111114) | 0.002645 ± 5.7735e-06 (W 2.30217e-05) | · | 🔵 fork 1.13× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 2.0593 ± 0.291419 (W 0.00585256) | 0.29474 ± 0.0372235 (W 0.00265068) | 2.63593 ± 0.0106615 (W 0.0046397) | 🔴 fork 6.99× slower than `faer-pool` | 🔵 fork 1.28× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor/n4/b1` | 0.000561 ± 1.1547e-05 (W 6.6106e-05) | 0.000601 ± 5.7735e-06 (W 7.49346e-05) | 0.00027 ± 5.7735e-06 (W 2.49439e-05) | 🔵 fork 1.07× faster than `faer-pool` | 🔴 fork 2.08× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.275143 ± 0.00315343 (W 0.00178557) | 0.072776 ± 0.00196105 (W 0.00118731) | 0.183102 ± 3.00056e-05 (W 0.0015173) | 🔴 fork 3.78× slower than `faer-pool` | 🔴 fork 1.50× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1` | 0.000972 ± 1e-05 (W 6.78233e-05) | 0.000982 ± 2.88675e-05 (W 0.000106603) | 0.000672 ± 5.50757e-06 (W 6.72309e-06) | · | 🔴 fork 1.45× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.690006 ± 0.0117665 (W 0.00248155) | 0.121646 ± 0.0109025 (W 0.00215664) | 0.618293 ± 0.001823 (W 0.00199238) | 🔴 fork 5.67× slower than `faer-pool` | 🔴 fork 1.12× slower than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor_solve/n16/b1` | 0.003918 ± 5.51392e-05 (W 4.79302e-05) | 0.003988 ± 4.95008e-05 (W 2.91548e-05) | 0.00528 ± 3e-05 (W 2.07364e-05) | · | 🔵 fork 1.35× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 3.46831 ± 0.0344163 (W 0.0105363) | 0.483211 ± 0.0257155 (W 0.0128605) | 5.29329 ± 0.0414645 (W 0.0126167) | 🔴 fork 7.18× slower than `faer-pool` | 🔵 fork 1.53× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n4/b1` | 0.000771 ± 1.48436e-05 (W 6.39633e-05) | 0.000831 ± 1.0504e-05 (W 4.89826e-05) | 0.000541 ± 1e-05 (W 1.78885e-05) | 🔵 fork 1.08× faster than `faer-pool` | 🔴 fork 1.43× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.426696 ± 0.00222991 (W 0.0029541) | 0.080871 ± 0.00189214 (W 0.00126012) | 0.416597 ± 0.00159016 (W 0.00234169) | 🔴 fork 5.28× slower than `faer-pool` | · |  |
| `lu_factor_solve/n8/b1` | 0.001663 ± 2.88675e-05 (W 5.53913e-05) | 0.001673 ± 5.7735e-06 (W 6.52097e-05) | 0.001723 ± 1.73205e-05 (W 2.96648e-05) | · | · | dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 1.17358 ± 0.00890912 (W 0.00358472) | 0.172602 ± 0.00159407 (W 0.00292316) | 1.66684 ± 0.00148522 (W 0.00282868) | 🔴 fork 6.80× slower than `faer-pool` | 🔵 fork 1.42× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1` | 0.001563 ± 2.13776e-05 (W 9.15423e-05) | 0.001583 ± 5.7735e-06 (W 5.54274e-05) | 0.002625 ± 2e-05 (W 3.49285e-05) | · | 🔵 fork 1.68× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 1.29761 ± 0.00783616 (W 0.00363522) | 0.194132 ± 0.0130873 (W 0.00139908) | 2.61545 ± 0.0138656 (W 0.00519927) | 🔴 fork 6.68× slower than `faer-pool` | 🔵 fork 2.02× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1` | 0.00046 ± 1.70392e-05 (W 4.91935e-05) | 0.000471 ± 1.1547e-05 (W 4.3359e-05) | 0.00035 ± 5.50757e-06 (W 3.24238e-05) | · | 🔴 fork 1.31× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.163255 ± 0.000885941 (W 0.00127535) | 0.045315 ± 0.000183567 (W 0.00143703) | 0.2413 ± 0.00145645 (W 0.00179053) | 🔴 fork 3.60× slower than `faer-pool` | 🔵 fork 1.48× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1` | 0.000751 ± 3.21455e-05 (W 7.31457e-05) | 0.000802 ± 1.00167e-05 (W 4.18007e-05) | 0.001142 ± 5.7735e-06 (W 8.94427e-06) | 🔵 fork 1.07× faster than `faer-pool` | 🔵 fork 1.52× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.478121 ± 0.0024801 (W 0.00316326) | 0.087153 ± 0.000526537 (W 0.000505911) | 1.07192 ± 0.000996161 (W 0.00219279) | 🔴 fork 5.49× slower than `faer-pool` | 🔵 fork 2.24× faster than `lapack-mkl` |  |
| `qr/n16/b1` | 0.011341 ± 0.000106775 (W 0.00014622) | 0.011361 ± 0.000101195 (W 6.14003e-05) | 0.010619 ± 7e-05 (W 3.57379e-05) | · | 🔴 fork 1.07× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 10.9051 ± 0.00831315 (W 0.0195763) | 1.40086 ± 0.00554314 (W 0.00768375) | 10.5779 ± 0.0295166 (W 0.0296803) | 🔴 fork 7.78× slower than `faer-pool` | · |  |
| `qr/n4/b1` | 0.001413 ± 3.76431e-05 (W 4.9972e-05) | 0.001463 ± 1.12694e-05 (W 5.08458e-05) | 0.001463 ± 5.19615e-06 (W 6.20484e-05) | · | · | dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.871194 ± 0.00233133 (W 0.00255043) | 0.118732 ± 0.000578545 (W 0.0013553) | 0.926508 ± 0.000962388 (W 0.00180492) | 🔴 fork 7.34× slower than `faer-pool` | 🔵 fork 1.06× faster than `lapack-mkl` |  |
| `qr/n8/b1` | 0.003246 ± 3.51188e-05 (W 4.71169e-05) | 0.003326 ± 3.05505e-05 (W 3.11448e-05) | 0.003155 ± 5.50757e-06 (W 3.16228e-05) | · | · | dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.64064 ± 0.0296205 (W 0.00244614) | 0.344162 ± 0.00513691 (W 0.00216335) | 2.65598 ± 0.0141292 (W 0.00687637) | 🔴 fork 7.67× slower than `faer-pool` | · |  |
| `rank_revealing_qr/n16/b1` | 0.012784 ± 0.000110726 (W 5.41498e-05) | 0.012684 ± 0.000136077 (W 0.000105869) | 0.015609 ± 0.000141539 (W 6.7855e-05) | · | 🔵 fork 1.22× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 12.3408 ± 0.0461742 (W 0.014738) | 1.57349 ± 0.0188072 (W 0.0107732) | 15.8254 ± 0.0510913 (W 0.0112971) | 🔴 fork 7.84× slower than `faer-pool` | 🔵 fork 1.28× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1` | 0.002144 ± 1.1547e-05 (W 6.4608e-05) | 0.002194 ± 4.3589e-05 (W 8.11862e-05) | 0.002534 ± 3.23574e-05 (W 2.96007e-05) | · | 🔵 fork 1.18× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.44308 ± 0.0110517 (W 0.00637248) | 0.190216 ± 0.00198714 (W 0.00174651) | 1.75158 ± 0.00316686 (W 0.00596304) | 🔴 fork 7.59× slower than `faer-pool` | 🔵 fork 1.21× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1` | 0.004388 ± 1.73205e-05 (W 7.06484e-05) | 0.004468 ± 1.57162e-05 (W 4.20868e-05) | 0.00535 ± 4.04145e-05 (W 4.80229e-05) | · | 🔵 fork 1.22× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.72551 ± 0.0153666 (W 0.00686074) | 0.486096 ± 0.108143 (W 0.00305192) | 4.73561 ± 0.00569483 (W 0.0109682) | 🔴 fork 7.66× slower than `faer-pool` | 🔵 fork 1.27× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `solve/n16/b1` | 0.00498 ± 2.08167e-05 (W 9.30446e-05) | 0.005069 ± 7.37111e-05 (W 0.000108781) | 0.005841 ± 2.08167e-05 (W 4.98919e-05) | · | 🔵 fork 1.17× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 3.92428 ± 0.038758 (W 0.010849) | 0.510753 ± 0.0226289 (W 0.00567619) | 5.58123 ± 0.020231 (W 0.0111194) | 🔴 fork 7.68× slower than `faer-pool` | 🔵 fork 1.42× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n4/b1` | 0.001423 ± 1.73205e-05 (W 5.94239e-05) | 0.001503 ± 2.08167e-05 (W 8.3666e-05) | 0.000821 ± 1.58219e-05 (W 2.58128e-05) | 🔵 fork 1.06× faster than `faer-pool` | 🔴 fork 1.73× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.534947 ± 0.0114752 (W 0.00347396) | 0.076613 ± 0.00092362 (W 0.00279297) | 0.479885 ± 0.000778535 (W 0.00245851) | 🔴 fork 6.98× slower than `faer-pool` | 🔴 fork 1.11× slower than `lapack-mkl` |  |
| `solve/n8/b1` | 0.002575 ± 7.63763e-05 (W 0.000126768) | 0.002595 ± 4.50925e-05 (W 7.46994e-05) | 0.002074 ± 1.18462e-05 (W 2.53436e-05) | · | 🔴 fork 1.24× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 1.33892 ± 0.0022284 (W 0.00528963) | 0.18738 ± 0.00253207 (W 0.00189548) | 1.74207 ± 0.0154943 (W 0.00361609) | 🔴 fork 7.15× slower than `faer-pool` | 🔵 fork 1.30× faster than `lapack-mkl` |  |
| `svd_full/n16/b1` | 0.058018 ± 0.000252924 (W 0.000390527) | 0.057848 ± 0.000117205 (W 0.000105755) | 0.065763 ± 0.000138529 (W 0.00138478) | · | 🔵 fork 1.13× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 60.3618 ± 0.0557914 (W 0.0429445) | 7.81975 ± 0.108045 (W 0.110603) | 67.5047 ± 0.120511 (W 0.202651) | 🔴 fork 7.72× slower than `faer-pool` | 🔵 fork 1.12× faster than `lapack-mkl` |  |
| `svd_full/n4/b1` | 0.00525 ± 5.19615e-06 (W 0.000112148) | 0.00529 ± 6.4291e-05 (W 0.000116919) | 0.007765 ± 5.57704e-05 (W 6.25236e-05) | · | 🔵 fork 1.48× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 4.9988 ± 0.00407048 (W 0.00686479) | 0.638271 ± 0.00248621 (W 0.00278552) | 7.41695 ± 0.0165009 (W 0.0100081) | 🔴 fork 7.83× slower than `faer-pool` | 🔵 fork 1.48× faster than `lapack-mkl` |  |
| `svd_full/n8/b1` | 0.016291 ± 9.01499e-05 (W 0.000109659) | 0.01641 ± 7.59627e-05 (W 0.000117453) | 0.020989 ± 0.000164418 (W 7.32953e-05) | · | 🔵 fork 1.29× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 16.7646 ± 0.00997443 (W 0.0198576) | 2.19444 ± 0.04411 (W 0.00440978) | 22.211 ± 0.0182853 (W 0.0355381) | 🔴 fork 7.64× slower than `faer-pool` | 🔵 fork 1.32× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1` | 0.057948 ± 0.000145258 (W 0.000151756) | 0.058148 ± 0.00019975 (W 8.15181e-05) | 0.065382 ± 0.000391 (W 0.00131345) | · | 🔵 fork 1.13× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 60.3821 ± 0.212221 (W 0.0347899) | 7.82429 ± 0.0886823 (W 0.0439031) | 67.3289 ± 0.185855 (W 0.0440178) | 🔴 fork 7.72× slower than `faer-pool` | 🔵 fork 1.12× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1` | 0.00526 ± 5.17397e-05 (W 6.26762e-05) | 0.0053 ± 1e-05 (W 6.2724e-05) | 0.007775 ± 9.50438e-06 (W 4.70128e-05) | · | 🔵 fork 1.48× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 5.03482 ± 0.0171181 (W 0.00755397) | 0.650234 ± 0.0102787 (W 0.0193707) | 7.39477 ± 0.0191906 (W 0.0215559) | 🔴 fork 7.74× slower than `faer-pool` | 🔵 fork 1.47× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1` | 0.016311 ± 8.79223e-05 (W 0.000113271) | 0.01633 ± 2.47049e-05 (W 9.53116e-05) | 0.021019 ± 0.000130128 (W 4.51475e-05) | · | 🔵 fork 1.29× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 16.7721 ± 0.0221164 (W 0.0262777) | 2.13098 ± 0.0536764 (W 0.0154135) | 22.1807 ± 0.0195337 (W 0.0260397) | 🔴 fork 7.87× slower than `faer-pool` | 🔵 fork 1.32× faster than `lapack-mkl` |  |
| `svd_values/n16/b1` | 0.043992 ± 0.000117898 (W 0.000149034) | 0.044152 ± 0.000312714 (W 0.000166626) | 0.02729 ± 2.28108e-05 (W 7.4364e-05) | · | 🔴 fork 1.61× slower than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 45.6515 ± 0.228168 (W 0.0337305) | 5.89814 ± 0.00849424 (W 0.0223075) | 28.1081 ± 0.0170247 (W 0.0299018) | 🔴 fork 7.74× slower than `faer-pool` | 🔴 fork 1.62× slower than `lapack-mkl` |  |
| `svd_values/n4/b1` | 0.004328 ± 4.6188e-05 (W 0.00013476) | 0.004389 ± 7.55667e-05 (W 0.000138008) | 0.003887 ± 2.02567e-05 (W 2.19841e-05) | · | 🔴 fork 1.11× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.84937 ± 0.00772152 (W 0.00640159) | 0.492678 ± 0.00150466 (W 0.00122358) | 3.4985 ± 0.00631474 (W 0.00745277) | 🔴 fork 7.81× slower than `faer-pool` | 🔴 fork 1.10× slower than `lapack-mkl` |  |
| `svd_values/n8/b1` | 0.012794 ± 4.04145e-05 (W 4.21936e-05) | 0.012844 ± 6.48614e-05 (W 5.83095e-05) | 0.008947 ± 3.09892e-05 (W 3.56371e-05) | · | 🔴 fork 1.43× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 12.9517 ± 0.0289417 (W 0.0184246) | 1.64324 ± 0.00747527 (W 0.00460797) | 9.09932 ± 0.0321838 (W 0.022101) | 🔴 fork 7.88× slower than `faer-pool` | 🔴 fork 1.42× slower than `lapack-mkl` |  |
| `triangular_solve/n16/b1` | 0.001523 ± 4.58258e-05 (W 6.09918e-05) | 0.001563 ± 2.88675e-05 (W 4.72229e-05) | 0.001573 ± 2.88675e-05 (W 2.58844e-05) | · | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.988263 ± 0.00775921 (W 0.00314519) | 0.138328 ± 0.00313208 (W 0.00281658) | 1.3368 ± 0.013479 (W 0.00409833) | 🔴 fork 7.14× slower than `faer-pool` | 🔵 fork 1.35× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1` | 0.000692 ± 5.27289e-05 (W 5.61899e-05) | 0.000692 ± 2.28108e-05 (W 5.3808e-05) | 0.000611 ± 1.52753e-05 (W 3.10998e-05) | · | 🔴 fork 1.13× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.162083 ± 0.000501787 (W 0.00193208) | 0.028052 ± 0.000399325 (W 0.000285027) | 0.30072 ± 0.000667876 (W 0.00234412) | 🔴 fork 5.78× slower than `faer-pool` | 🔵 fork 1.86× faster than `lapack-mkl` |  |
| `triangular_solve/n8/b1` | 0.000982 ± 5.1316e-05 (W 3.57771e-05) | 0.001032 ± 4.2194e-05 (W 4.89898e-05) | 0.000881 ± 2.04206e-05 (W 1.91651e-05) | · | 🔴 fork 1.11× slower than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.400656 ± 0.00336053 (W 0.00308923) | 0.065733 ± 0.000769 (W 0.000864686) | 0.580752 ± 0.000957546 (W 0.00294677) | 🔴 fork 6.10× slower than `faer-pool` | 🔵 fork 1.45× faster than `lapack-mkl` |  |

Not applicable to this population's shapes and reported as skipped: `cholesky/16`, `cholesky/4`, `cholesky/8`, `eig/16`, `eig/4`, `eig/8`, `eigh/16`, `eigh/4`, `eigh/8`, `eigvals/16`, `eigvals/4`, `eigvals/8`, `eigvalsh/16`, `eigvalsh/4`, `eigvalsh/8`, `full_piv_lu/16`, `full_piv_lu/4`, `full_piv_lu/8`, `full_piv_lu_solve/16`, `full_piv_lu_solve/4`, `full_piv_lu_solve/8`, `householder_apply/16`, `householder_apply/4`, `householder_apply/8`, `householder_factor/16`, `householder_factor/4`, `householder_factor/8`, `lu/16`, `lu/4`, `lu/8`, `lu_factor/16`, `lu_factor/4`, `lu_factor/8`, `lu_factor_solve/16`, `lu_factor_solve/4`, `lu_factor_solve/8`, `lu_solve_prepared/16`, `lu_solve_prepared/4`, `lu_solve_prepared/8`, `qr/16`, `qr/4`, `qr/8`, `rank_revealing_qr/16`, `rank_revealing_qr/4`, `rank_revealing_qr/8`, `solve/16`, `solve/4`, `solve/8`, `svd_full/16`, `svd_full/4`, `svd_full/8`, `svd_thin/16`, `svd_thin/4`, `svd_thin/8`, `svd_values/16`, `svd_values/4`, `svd_values/8`, `triangular_solve/16`, `triangular_solve/4`, `triangular_solve/8`.

## canary-factor, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.066555 ± 6.12127e-05 (W 0.00113149) | - | 0.093975 ± 0.000879656 (W 0.000266362) | - | 🔵 fork 1.41× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu/n128/b1` | 0.149218 ± 0.000778365 (W 0.00210052) | - | 0.136825 ± 0.000267644 (W 0.00163332) | - | 🔴 fork 1.09× slower than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor/n128/b1` | 0.094677 ± 0.00036093 (W 9.71766e-05) | - | 0.121647 ± 0.000299962 (W 0.00120982) | - | 🔵 fork 1.28× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor_solve/n128/b1` | 0.105787 ± 0.000770312 (W 0.00134816) | - | 0.142235 ± 7.20208e-05 (W 0.00142261) | - | 🔵 fork 1.34× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_solve_prepared/n128/b1` | 0.009888 ± 1.57162e-05 (W 0.000107677) | - | 0.020829 ± 0.000222913 (W 8.40833e-05) | - | 🔵 fork 2.11× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.111218 ± 0.000780498 (W 0.000271027) | - | 0.146283 ± 0.000200083 (W 0.00116161) | - | 🔵 fork 1.32× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n128/b1` | 2.33476 ± 0.00650357 (W 0.00415086) | - | 1.16178 ± 0.00204729 (W 0.00284927) | - | 🔴 fork 2.01× slower than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n128/b1` | 0.006993 ± 3.78594e-05 (W 0.000107453) | - | 0.011702 ± 0.000110092 (W 8.88774e-05) | - | 🔵 fork 1.67× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |

## canary-factor, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.066554 ± 0.000260832 (W 0.0012174) | 0.066594 ± 0.000101046 (W 0.000116882) | 0.093685 ± 0.000307208 (W 0.00205649) | · | 🔵 fork 1.41× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.149088 ± 0.00117384 (W 0.00118911) | 0.186588 ± 0.00440818 (W 0.00708381) | 0.135864 ± 0.000157162 (W 0.0017001) | 🔵 fork 1.25× faster than `faer-pool` | 🔴 fork 1.10× slower than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.093385 ± 0.000346541 (W 0.00190963) | 0.126466 ± 0.00223698 (W 0.00428258) | 0.120915 ± 0.000140607 (W 0.00181319) | 🔵 fork 1.35× faster than `faer-pool` | 🔵 fork 1.29× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.102912 ± 0.000684176 (W 0.00141404) | 0.134501 ± 0.00218855 (W 0.00559347) | 0.143157 ± 0.000501019 (W 0.00176343) | 🔵 fork 1.31× faster than `faer-pool` | 🔵 fork 1.39× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.009838 ± 5.55608e-05 (W 0.000106251) | 0.009979 ± 2.88675e-05 (W 0.00010045) | 0.01648 ± 0.000190815 (W 0.000338021) | · | 🔵 fork 1.68× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.113272 ± 0.00160512 (W 0.001492) | 0.147044 ± 0.00170345 (W 0.00275097) | 0.151162 ± 6.55744e-05 (W 0.00154784) | 🔵 fork 1.30× faster than `faer-pool` | 🔵 fork 1.33× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 2.35431 ± 0.00129945 (W 0.00339503) | 2.38991 ± 0.00680796 (W 0.0032266) | 1.1337 ± 0.00191922 (W 0.00308227) | · | 🔴 fork 2.08× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.006903 ± 5.1316e-05 (W 4.36142e-05) | 0.006942 ± 0.000105406 (W 6.85565e-05) | 0.01084 ± 0.000197536 (W 0.000323401) | · | 🔵 fork 1.57× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.18212 ± 0.000486499 (W 0.00154915) | - | 0.40748 ± 0.00135008 (W 0.00178806) | - | 🔵 fork 2.24× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu/n128/b1` | 0.32704 ± 0.000786716 (W 0.00168462) | - | 0.453426 ± 0.00162002 (W 0.00211274) | - | 🔵 fork 1.39× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor/n128/b1` | 0.261448 ± 0.00166089 (W 0.00186441) | - | 0.415625 ± 0.000894683 (W 0.00244017) | - | 🔵 fork 1.59× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_factor_solve/n128/b1` | 0.292014 ± 0.00131674 (W 0.00179646) | - | 0.468775 ± 0.000666253 (W 0.00185581) | - | 🔵 fork 1.61× faster than `lapack-mkl` | `*` one row has no measurement here |
| `lu_solve_prepared/n128/b1` | 0.031199 ± 0.000146323 (W 0.000159644) | - | 0.051296 ± 0.000130908 (W 0.00025687) | - | 🔵 fork 1.64× faster than `lapack-mkl` | `*` one row has no measurement here |
| `solve/n128/b1` | 0.303877 ± 0.00106134 (W 0.00150546) | - | 0.480406 ± 0.00390578 (W 0.00209736) | - | 🔵 fork 1.58× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_values/n128/b1` | 3.12917 ± 0.00274206 (W 0.0108834) | - | 2.65415 ± 0.00795871 (W 0.00364142) | - | 🔴 fork 1.18× slower than `lapack-mkl` | `*` one row has no measurement here |
| `triangular_solve/n128/b1` | 0.018535 ± 4.50925e-05 (W 0.000107533) | - | 0.025488 ± 9.54481e-05 (W 3.97492e-05) | - | 🔵 fork 1.38× faster than `lapack-mkl` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.180647 ± 0.00120157 (W 0.00174178) | 0.188392 ± 0.00134825 (W 0.00249489) | 0.412049 ± 0.00196921 (W 0.00291384) | · | 🔵 fork 2.28× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.32748 ± 0.00181803 (W 0.00284509) | 0.341597 ± 0.00271973 (W 0.00738186) | 0.451543 ± 0.000307573 (W 0.00330446) | · | 🔵 fork 1.38× faster than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.260475 ± 0.00105293 (W 0.0020202) | 0.26256 ± 0.000905964 (W 0.00390213) | 0.415295 ± 0.000902454 (W 0.00268551) | · | 🔵 fork 1.59× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.290382 ± 0.00143724 (W 0.00211239) | 0.289299 ± 0.00266945 (W 0.00349318) | 0.448146 ± 0.00137329 (W 0.00295737) | · | 🔵 fork 1.54× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.031178 ± 8.55589e-05 (W 0.000176367) | 0.031259 ± 5e-05 (W 7.68069e-05) | 0.025487 ± 0.00015885 (W 0.000187297) | · | 🔴 fork 1.22× slower than `lapack-mkl` |  |
| `solve/n128/b1` | 0.304377 ± 0.000202527 (W 0.00260593) | 0.318914 ± 0.00226108 (W 0.00381087) | 0.464877 ± 0.000552071 (W 0.00237525) | · | 🔵 fork 1.53× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 3.1391 ± 0.0100205 (W 0.016294) | 3.15811 ± 0.00116192 (W 0.00369338) | 1.92117 ± 0.003775 (W 0.00405575) | · | 🔴 fork 1.63× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.018635 ± 0.000100167 (W 9.03394e-05) | 0.018694 ± 0.000195144 (W 0.000213237) | 0.013145 ± 4.55741e-05 (W 0.000103297) | · | 🔴 fork 1.42× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |

Not applicable to this population's shapes and reported as skipped: `cholesky/128`, `lu/128`, `lu_factor/128`, `lu_factor_solve/128`, `lu_solve_prepared/128`, `solve/128`, `svd_values/128`, `triangular_solve/128`.

## canary-decompose, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 47.9239 ± 0.375676 (W 0.0533467) | - | 60.439 ± 0.108734 (W 0.0752627) | - | 🔵 fork 1.26× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n512/b1` | 23.6511 ± 0.236861 (W 0.0195501) | - | 27.5554 ± 0.0731947 (W 0.039775) | - | 🔵 fork 1.17× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_apply/n512/b1` | 10.2483 ± 0.0137471 (W 0.0205249) | - | 21.748 ± 0.0623876 (W 0.0372807) | - | 🔵 fork 2.12× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_factor/n512/b1` | 7.2082 ± 0.0141325 (W 0.0197259) | - | 13.3563 ± 0.00607627 (W 0.0220844) | - | 🔵 fork 1.85× faster than `lapack-mkl` | `*` one row has no measurement here |
| `qr/n512/b1` | 19.4383 ± 0.164076 (W 0.0262012) | - | 28.4329 ± 0.0776175 (W 0.0236893) | - | 🔵 fork 1.46× faster than `lapack-mkl` | `*` one row has no measurement here |
| `rank_revealing_qr/n512/b1` | 29.8423 ± 0.0236611 (W 0.0381202) | - | 35.4134 ± 0.0637 (W 0.0653523) | - | 🔵 fork 1.19× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n512/b1` | 116.618 ± 0.0680278 (W 0.474834) | - | 117.207 ± 0.45714 (W 0.183468) | - | · | `*` one row has no measurement here |

## canary-decompose, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 48.125 ± 0.294018 (W 0.0599392) | 23.8473 ± 0.140741 (W 0.125357) | 14.9293 ± 0.026346 (W 0.0372157) | 🔴 fork 2.02× slower than `faer-pool` | 🔴 fork 3.22× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 23.5576 ± 0.0952194 (W 0.0288647) | 18.6149 ± 0.0199059 (W 0.0400257) | 12.6599 ± 0.0111465 (W 0.0141501) | 🔴 fork 1.27× slower than `faer-pool` | 🔴 fork 1.86× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 10.0766 ± 0.0377707 (W 0.0240642) | 2.77154 ± 0.0191187 (W 0.0684261) | 3.15826 ± 0.0114721 (W 0.0222003) | 🔴 fork 3.64× slower than `faer-pool` | 🔴 fork 3.19× slower than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 7.10103 ± 0.00253973 (W 0.00924589) | 2.6557 ± 0.00807163 (W 0.0268659) | 2.13804 ± 0.00410168 (W 0.00603026) | 🔴 fork 2.67× slower than `faer-pool` | 🔴 fork 3.32× slower than `lapack-mkl` |  |
| `qr/n512/b1` | 19.3576 ± 0.109868 (W 0.0915068) | 7.7667 ± 0.0303644 (W 0.0728464) | 8.73132 ± 0.0265609 (W 0.0165654) | 🔴 fork 2.49× slower than `faer-pool` | 🔴 fork 2.22× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 25.1691 ± 0.138003 (W 0.0283183) | 9.63884 ± 0.0765496 (W 0.100369) | 24.6309 ± 0.264962 (W 0.0476372) | 🔴 fork 2.61× slower than `faer-pool` | · |  |
| `svd_thin/n512/b1` | 117.911 ± 0.0765582 (W 0.087443) | 60.6797 ± 0.0328795 (W 0.126711) | 49.2116 ± 0.335585 (W 0.0614896) | 🔴 fork 1.94× slower than `faer-pool` | 🔴 fork 2.40× slower than `lapack-mkl` |  |

## canary-decompose, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 104.845 ± 0.380745 (W 0.0556507) | - | 252.783 ± 0.0991896 (W 0.464176) | - | 🔵 fork 2.41× faster than `lapack-mkl` | `*` one row has no measurement here |
| `eigvalsh/n512/b1` | 49.2471 ± 0.28447 (W 0.0450957) | - | 96.5676 ± 0.12299 (W 0.0891141) | - | 🔵 fork 1.96× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_apply/n512/b1` | 41.0634 ± 0.0411017 (W 0.037182) | - | 61.276 ± 0.0385096 (W 0.0819328) | - | 🔵 fork 1.49× faster than `lapack-mkl` | `*` one row has no measurement here |
| `householder_factor/n512/b1` | 27.2784 ± 0.12093 (W 0.0814531) | - | 37.634 ± 0.0148533 (W 0.0608176) | - | 🔵 fork 1.38× faster than `lapack-mkl` | `*` one row has no measurement here |
| `qr/n512/b1` | 70.2458 ± 0.108057 (W 0.0570317) | - | 77.7251 ± 0.0798195 (W 0.0613962) | - | 🔵 fork 1.11× faster than `lapack-mkl` | `*` one row has no measurement here |
| `rank_revealing_qr/n512/b1` | 82.1809 ± 0.0976182 (W 0.056097) | - | 105.983 ± 0.393759 (W 0.428521) | - | 🔵 fork 1.29× faster than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/n512/b1` | 261.392 ± 0.645545 (W 0.518177) | - | 312.313 ± 1.13612 (W 0.801381) | - | 🔵 fork 1.19× faster than `lapack-mkl` | `*` one row has no measurement here |

## canary-decompose, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 104.581 ± 0.180733 (W 0.0788673) | 39.4144 ± 0.481517 (W 0.450218) | 65.817 ± 0.0251772 (W 0.430674) | 🔴 fork 2.65× slower than `faer-pool` | 🔴 fork 1.59× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 48.8615 ± 0.0643766 (W 0.0371301) | 28.9244 ± 0.0669134 (W 0.0471103) | 28.8241 ± 0.0390486 (W 0.0129539) | 🔴 fork 1.69× slower than `faer-pool` | 🔴 fork 1.70× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 40.6338 ± 0.0658875 (W 0.0674136) | 7.0341 ± 0.0289007 (W 0.0597503) | 8.10741 ± 0.00668006 (W 0.0132828) | 🔴 fork 5.78× slower than `faer-pool` | 🔴 fork 5.01× slower than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 27.2792 ± 0.030177 (W 0.0269401) | 6.9216 ± 0.0377094 (W 0.0277337) | 5.44692 ± 0.00675708 (W 0.0122665) | 🔴 fork 3.94× slower than `faer-pool` | 🔴 fork 5.01× slower than `lapack-mkl` |  |
| `qr/n512/b1` | 70.0712 ± 0.0754659 (W 0.0255609) | 16.6952 ± 0.113235 (W 0.172271) | 15.4869 ± 0.025348 (W 0.0221335) | 🔴 fork 4.20× slower than `faer-pool` | 🔴 fork 4.52× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 78.8083 ± 0.123469 (W 0.387007) | 18.8379 ± 0.0738089 (W 0.127784) | 60.1712 ± 0.426855 (W 0.0365357) | 🔴 fork 4.18× slower than `faer-pool` | 🔴 fork 1.31× slower than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 260.512 ± 0.136139 (W 0.76286) | 100.362 ± 7.90832 (W 0.414769) | 86.4789 ± 0.118722 (W 0.404403) | 🔴 fork 2.60× slower than `faer-pool` | 🔴 fork 3.01× slower than `lapack-mkl` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `eigh/512`, `eigvalsh/512`, `householder_apply/512`, `householder_factor/512`, `qr/512`, `rank_revealing_qr/512`, `svd_thin/512`.

## canary-rectangular, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 22.9916 ± 0.040503 (W 0.0306998) | - | 28.6562 ± 0.090537 (W 0.0594388) | - | 🔵 fork 1.25× faster than `lapack-mkl` | `*` one row has no measurement here |
| `qr/4096x256/b1` | 66.5161 ± 0.0799142 (W 0.170498) | - | 69.1252 ± 0.21263 (W 0.0666754) | - | · | `*` one row has no measurement here |
| `rank_revealing_qr/4096x256/b1` | 102.03 ± 0.160772 (W 0.293601) | - | 94.7417 ± 1.22637 (W 1.35836) | - | 🔴 fork 1.08× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/4096x256/b1` | 102.964 ± 0.0877937 (W 0.126872) | - | 109.574 ± 0.2515 (W 0.380721) | - | 🔵 fork 1.06× faster than `lapack-mkl` | `*` one row has no measurement here |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 23.0628 ± 0.111852 (W 0.0238326) | 7.8759 ± 0.0201061 (W 0.0242007) | 6.18189 ± 0.0336776 (W 0.03095) | 🔴 fork 2.93× slower than `faer-pool` | 🔴 fork 3.73× slower than `lapack-mkl` |  |
| `qr/4096x256/b1` | 66.8831 ± 0.123272 (W 0.0493279) | 22.3033 ± 0.35334 (W 0.374208) | 18.1151 ± 0.174193 (W 0.0368245) | 🔴 fork 3.00× slower than `faer-pool` | 🔴 fork 3.69× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 102.319 ± 0.313585 (W 0.107952) | 23.8457 ± 0.253588 (W 0.396218) | 63.4402 ± 0.416483 (W 2.23254) | 🔴 fork 4.29× slower than `faer-pool` | 🔴 fork 1.61× slower than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 103.092 ± 0.126371 (W 0.229848) | 39.6073 ± 0.256346 (W 0.37275) | 34.4506 ± 0.131734 (W 0.106388) | 🔴 fork 2.60× slower than `faer-pool` | 🔴 fork 2.99× slower than `lapack-mkl` |  |

## canary-rectangular, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 85.8359 ± 0.0661564 (W 0.323145) | - | 105.078 ± 1.52487 (W 0.337785) | - | 🔵 fork 1.22× faster than `lapack-mkl` | `*` one row has no measurement here |
| `qr/4096x256/b1` | 237.651 ± 0.164781 (W 0.181507) | - | 214.353 ± 0.257341 (W 0.355969) | - | 🔴 fork 1.11× slower than `lapack-mkl` | `*` one row has no measurement here |
| `rank_revealing_qr/4096x256/b1` | 349.542 ± 0.931594 (W 1.0558) | - | 281.031 ± 1.36193 (W 0.490064) | - | 🔴 fork 1.24× slower than `lapack-mkl` | `*` one row has no measurement here |
| `svd_thin/4096x256/b1` | 366.819 ± 0.0753974 (W 0.759286) | - | 349.96 ± 1.04059 (W 1.03328) | - | · | `*` one row has no measurement here |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) | vs `faer-pool` | vs `lapack-mkl` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 85.9865 ± 0.0715927 (W 0.419516) | 19.7746 ± 0.110229 (W 0.0406762) | 16.8601 ± 0.0738913 (W 0.0688868) | 🔴 fork 4.35× slower than `faer-pool` | 🔴 fork 5.10× slower than `lapack-mkl` |  |
| `qr/4096x256/b1` | 237.886 ± 0.27225 (W 0.466193) | 53.2556 ± 0.1764 (W 0.12629) | 40.641 ± 0.119921 (W 0.215494) | 🔴 fork 4.47× slower than `faer-pool` | 🔴 fork 5.85× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 344.12 ± 1.68566 (W 0.936162) | 60.6931 ± 0.306175 (W 0.328058) | 162.003 ± 0.23282 (W 0.536174) | 🔴 fork 5.67× slower than `faer-pool` | 🔴 fork 2.12× slower than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 367.072 ± 0.474356 (W 0.402651) | 112.41 ± 0.52905 (W 0.453273) | 75.8561 ± 0.346574 (W 0.433035) | 🔴 fork 3.27× slower than `faer-pool` | 🔴 fork 4.84× slower than `lapack-mkl` |  |

Not applicable to this population's shapes and reported as skipped: `householder_factor/4096x256`, `qr/4096x256`, `rank_revealing_qr/4096x256`, `svd_thin/4096x256`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
