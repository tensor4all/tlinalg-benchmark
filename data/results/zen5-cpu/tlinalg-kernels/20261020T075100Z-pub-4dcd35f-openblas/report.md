# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `4dcd35f080a6b4fd6b1423871af66a33fd398482`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `4d13938002ca0480addb58124c4f4dc2ace0e2c7`
- toolkit commit: `90fbeeb3dd2389b8a5d9bc63679f5e2bf3fc1741`
- measured binary SHA-256: `dce21ac38e7150502f3291d58bb393080b1e1f363df08a2caf08052ff5e09987`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T08:22:05.850372Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas --aa 3 --reps 5 --prime-ms 250 --label pub-4dcd35f-openblas`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261020T075100Z-pub-4dcd35f-openblas/`

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
- CPU sets: 1T -> `4`, 8T -> `4-11`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 3 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.47%, worst 109.32% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 181 of 1390 engine cells exceed 5% and carry `!`; median within-process relative SD 0.65%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001162 ± 5.19615e-06 (W 3.75007e-05) | - | 0.001152 ± 2.08167e-05 (W 2.32852e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 0.840182 ± 0.00234434 (W 0.00165062) | - | 1.0036 ± 0.00558496 (W 0.00191956) | - | 🔵 fork 1.19× faster than `lapack-openblas` | `*` one row has no measurement here |
| `cholesky/n4/b1` | 0.000531 ± 5.7735e-06 (W 3.20936e-05) | - | 0.000371 ± 5.7735e-06 (W 1.0015e-05) | - | 🔴 fork 1.43× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.178935 ± 0.00132155 (W 0.00149325) | - | 0.190888 ± 0.000164734 (W 0.00173519) | - | 🔵 fork 1.07× faster than `lapack-openblas` | `*` one row has no measurement here |
| `cholesky/n8/b1` | 0.000691 ± 1.73205e-05 (W 2.72433e-05) | - | 0.000561 ± 1.1547e-05 (W 1.34164e-05) | - | 🔴 fork 1.23× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.356277 ± 0.00152814 (W 0.00264954) | - | 0.380983 ± 0.00686065 (W 0.00245049) | - | 🔵 fork 1.07× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n16/b1` | 0.090179 ± 0.000148987 (W 0.00153362) | - | 0.067767 ± 0.00055805 (W 0.000211131) | - | 🔴 fork 1.33× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n16/b1024` | 93.9241 ± 0.135764 (W 0.0759685) | - | 69.3357 ± 0.425226 (W 0.337308) | - | 🔴 fork 1.35× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n4/b1` | 0.006883 ± 9.50438e-06 (W 8.14248e-05) | - | 0.006201 ± 3.04467e-05 (W 3.94233e-05) | - | 🔴 fork 1.11× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 6.14915 ± 0.00905749 (W 0.0119058) | - | 5.34405 ± 0.0175168 (W 0.00931157) | - | 🔴 fork 1.15× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n8/b1` | 0.024155 ± 4.6188e-05 (W 0.000152376) | - | 0.018425 ± 9.68005e-05 (W 0.000101219) | - | 🔴 fork 1.31× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n8/b1024` | 23.404 ± 0.0298189 (W 0.0332186) | - | 17.4891 ± 0.118476 (W 0.0239609) | - | 🔴 fork 1.34× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n16/b1` | 0.029696 ± 0.00018791 (W 0.000108937) | - | 0.038382 ± 2.64575e-05 (W 7.12039e-05) | - | 🔵 fork 1.29× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n16/b1024` | 29.7473 ± 0.118819 (W 0.0364415) | - | 40.1612 ± 0.197854 (W 0.144574) | - | 🔵 fork 1.35× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n4/b1` | 0.002835 ± 2.5697e-05 (W 4.87052e-05) | - | 0.003206 ± 3.21455e-05 (W 5.70728e-05) | - | 🔵 fork 1.13× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.40945 ± 0.0130577 (W 0.00617571) | - | 3.05127 ± 0.0210985 (W 0.00804279) | - | 🔵 fork 1.27× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n8/b1` | 0.008696 ± 1.52753e-05 (W 2.77489e-05) | - | 0.01064 ± 9.29157e-05 (W 5.16546e-05) | - | 🔵 fork 1.22× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 8.44119 ± 0.0246772 (W 0.0211977) | - | 10.8351 ± 0.00415769 (W 0.0237647) | - | 🔵 fork 1.28× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n16/b1` | 0.061887 ± 0.00013604 (W 0.000168847) | - | 0.048682 ± 0.00014283 (W 0.000234756) | - | 🔴 fork 1.27× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n16/b1024` | 64.8126 ± 0.0836509 (W 0.0938823) | - | 49.7625 ± 0.572531 (W 0.229734) | - | 🔴 fork 1.30× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n4/b1` | 0.003837 ± 4.58258e-05 (W 3.83432e-05) | - | 0.004177 ± 6.68356e-05 (W 2.70185e-05) | - | 🔵 fork 1.09× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 3.15126 ± 0.00671411 (W 0.0049859) | - | 3.39902 ± 0.0136654 (W 0.00308095) | - | 🔵 fork 1.08× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n8/b1` | 0.01625 ± 0.000138818 (W 7.29541e-05) | - | 0.014247 ± 6.4291e-05 (W 5.26336e-05) | - | 🔴 fork 1.14× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 15.2872 ± 0.0254404 (W 0.0234922) | - | 13.2359 ± 0.0310928 (W 0.0237703) | - | 🔴 fork 1.15× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n16/b1` | 0.022371 ± 0.000164612 (W 0.000102713) | - | 0.014007 ± 3.00056e-05 (W 4.85304e-05) | - | 🔴 fork 1.60× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n16/b1024` | 22.1461 ± 0.0429951 (W 0.029959) | - | 14.4113 ± 0.00940475 (W 0.0302824) | - | 🔴 fork 1.54× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n4/b1` | 0.002404 ± 2.66521e-05 (W 9.61161e-05) | - | 0.001723 ± 2.64575e-05 (W 5.6686e-05) | - | 🔴 fork 1.40× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 1.95302 ± 0.0130458 (W 0.00222253) | - | 1.37864 ± 0.00128177 (W 0.00322394) | - | 🔴 fork 1.42× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n8/b1` | 0.007293 ± 7.75263e-05 (W 8.63203e-05) | - | 0.00486 ± 4.41626e-05 (W 3.28055e-05) | - | 🔴 fork 1.50× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 6.74706 ± 0.00387295 (W 0.0148548) | - | 4.49387 ± 0.00758936 (W 0.0124785) | - | 🔴 fork 1.50× slower than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu/n16/b1` | 0.004118 ± 9.50438e-06 (W 4.94803e-05) | - | 0.004569 ± 7.26659e-05 (W 2.70056e-05) | - | 🔵 fork 1.11× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 3.35945 ± 0.0748732 (W 0.0121325) | - | 4.89047 ± 0.0801089 (W 0.0224948) | - | 🔵 fork 1.46× faster than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu/n4/b1` | 0.001042 ± 1.52753e-05 (W 3.36155e-05) | - | 0.000611 ± 1e-05 (W 2.02781e-05) | - | 🔴 fork 1.71× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.384554 ± 0.00349236 (W 0.00203674) | - | 0.361586 ± 0.00225491 (W 0.0024728) | - | 🔴 fork 1.06× slower than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu/n8/b1` | 0.001833 ± 3.52184e-05 (W 4.97524e-05) | - | 0.001302 ± 1.48436e-05 (W 1.83112e-05) | - | 🔴 fork 1.41× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.06167 ± 0.0162342 (W 0.00478967) | - | 1.04447 ± 0.0138605 (W 0.00300625) | - | · | `*` one row has no measurement here |
| `full_piv_lu_solve/n16/b1` | 0.004359 ± 0.000737728 (W 5.8019e-05) | - | 0.006322 ± 3.45977e-05 (W 2.70185e-05) | - | 🔵 fork 1.45× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 3.39071 ± 0.958236 (W 0.0149844) | - | 6.30613 ± 0.0925987 (W 0.0271472) | - | 🔵 fork 1.86× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `full_piv_lu_solve/n4/b1` | 0.001333 ± 3.64737e-05 (W 3.82923e-05) | - | 0.001073 ± 1.70392e-05 (W 5.35462e-05) | - | 🔴 fork 1.24× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.51006 ± 0.0520561 (W 0.00168623) | - | 0.710661 ± 0.0206171 (W 0.00576633) | - | 🔵 fork 1.39× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1` | 0.002204 ± 0.000266158 (W 7.8091e-05) | - | 0.002004 ± 1.53948e-05 (W 1.63187e-05) | - | · | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.25874 ± 0.41434 (W 0.00900995) | - | 1.6577 ± 0.00194279 (W 0.00579708) | - | · | `*` one row has no measurement here; `!` between-start range over 5% |
| `householder_apply/n16/b1` | 0.004759 ± 0.0001367 (W 6.78985e-05) | - | 0.005069 ± 4.04145e-05 (W 5.85081e-05) | - | 🔵 fork 1.07× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 4.48522 ± 0.135639 (W 0.00543552) | - | 4.47645 ± 0.00924122 (W 0.0118992) | - | · | `*` one row has no measurement here; `!` between-start range over 5% |
| `householder_apply/n4/b1` | 0.000662 ± 6.35085e-06 (W 7.11498e-05) | - | 0.001062 ± 2.08167e-05 (W 2.58844e-05) | - | 🔵 fork 1.60× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.346803 ± 0.0073806 (W 0.00186723) | - | 0.416749 ± 0.00179311 (W 0.00256305) | - | 🔵 fork 1.20× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_apply/n8/b1` | 0.001433 ± 5.63057e-05 (W 1.6562e-05) | - | 0.001863 ± 2.47049e-05 (W 3.61843e-05) | - | 🔵 fork 1.30× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.15125 ± 0.0563732 (W 0.00361077) | - | 1.20995 ± 0.00186779 (W 0.00325029) | - | · | `*` one row has no measurement here; `!` between-start range over 5% |
| `householder_factor/n16/b1` | 0.003827 ± 5.1316e-05 (W 4.17289e-05) | - | 0.004559 ± 2.51064e-05 (W 5.76307e-05) | - | 🔵 fork 1.19× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 3.65361 ± 0.0181391 (W 0.00356397) | - | 4.35549 ± 0.00366705 (W 0.00870752) | - | 🔵 fork 1.19× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_factor/n4/b1` | 0.000691 ± 1.73205e-05 (W 2.52844e-05) | - | 0.000802 ± 6.35085e-06 (W 2.52646e-05) | - | 🔵 fork 1.16× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.447442 ± 0.004545 (W 0.00269944) | - | 0.537978 ± 0.00069951 (W 0.00270907) | - | 🔵 fork 1.20× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_factor/n8/b1` | 0.001393 ± 2.02567e-05 (W 1.58209e-05) | - | 0.001783 ± 2e-05 (W 3.39013e-05) | - | 🔵 fork 1.28× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.19584 ± 0.00814396 (W 0.00238404) | - | 1.51411 ± 0.00400322 (W 0.00241891) | - | 🔵 fork 1.27× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu/n16/b1` | 0.003106 ± 5.50757e-06 (W 5.15975e-05) | - | 0.002766 ± 2.09841e-05 (W 6.24364e-05) | - | 🔴 fork 1.12× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 2.53528 ± 0.0192928 (W 0.0106345) | - | 2.4015 ± 0.0736311 (W 0.00708489) | - | 🔴 fork 1.06× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `lu/n4/b1` | 0.000761 ± 1.57162e-05 (W 7.71965e-05) | - | 0.000591 ± 2.08167e-05 (W 1.2661e-05) | - | 🔴 fork 1.29× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.28661 ± 0.000729196 (W 0.0023764) | - | 0.321921 ± 0.00390901 (W 0.00211979) | - | 🔵 fork 1.12× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu/n8/b1` | 0.001303 ± 2.08167e-05 (W 3.34111e-05) | - | 0.001112 ± 3.05505e-05 (W 2.09332e-05) | - | 🔴 fork 1.17× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.809264 ± 0.00565942 (W 0.0031101) | - | 0.811417 ± 0.00176535 (W 0.00627305) | - | · | `*` one row has no measurement here |
| `lu_factor/n16/b1` | 0.002044 ± 4.3589e-05 (W 5.50454e-05) | - | 0.001894 ± 2.60832e-05 (W 3.83836e-05) | - | 🔴 fork 1.08× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 1.85823 ± 0.0321859 (W 0.00307977) | - | 1.79844 ± 0.0141013 (W 0.00837948) | - | · | `*` one row has no measurement here |
| `lu_factor/n4/b1` | 0.000551 ± 4.04145e-05 (W 5.56705e-05) | - | 0.00032 ± 1.70392e-05 (W 3.39013e-05) | - | 🔴 fork 1.72× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.222537 ± 0.00128124 (W 0.00202178) | - | 0.217907 ± 0.000687547 (W 0.00183962) | - | · | `*` one row has no measurement here |
| `lu_factor/n8/b1` | 0.000882 ± 2.91605e-05 (W 2.19089e-05) | - | 0.000641 ± 5.7735e-06 (W 6.08958e-05) | - | 🔴 fork 1.38× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.574246 ± 0.0118584 (W 0.00371602) | - | 0.56809 ± 0.00338564 (W 0.00429336) | - | · | `*` one row has no measurement here |
| `lu_factor_solve/n16/b1` | 0.002745 ± 1e-05 (W 1.54013e-05) | - | 0.003286 ± 3e-05 (W 2.60615e-05) | - | 🔵 fork 1.20× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 2.39488 ± 0.00158189 (W 0.0125763) | - | 3.14022 ± 0.0230562 (W 0.0150401) | - | 🔵 fork 1.31× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor_solve/n4/b1` | 0.000591 ± 0 (W 4.84768e-05) | - | 0.000611 ± 1.73205e-05 (W 2.74809e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.276066 ± 0.00428722 (W 0.00220735) | - | 0.524562 ± 0.00709651 (W 0.0036652) | - | 🔵 fork 1.90× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor_solve/n8/b1` | 0.001212 ± 3.78594e-05 (W 2.16795e-05) | - | 0.001223 ± 5.7735e-07 (W 1.4639e-05) | - | · | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 0.81094 ± 0.00332324 (W 0.00542749) | - | 1.073 ± 0.000573544 (W 0.00283115) | - | 🔵 fork 1.32× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n16/b1` | 0.000862 ± 2.6839e-05 (W 3.26374e-05) | - | 0.001292 ± 1.51767e-05 (W 1.15888e-05) | - | 🔵 fork 1.50× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 0.601944 ± 0.00166309 (W 0.00294223) | - | 1.20142 ± 0.0105163 (W 0.00500307) | - | 🔵 fork 2.00× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n4/b1` | 0.000351 ± 1.1547e-05 (W 2.79696e-05) | - | 0.000411 ± 5.7735e-06 (W 1.05972e-05) | - | 🔵 fork 1.17× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.067436 ± 0.000227952 (W 0.000123379) | - | 0.313397 ± 0.00315242 (W 0.00234639) | - | 🔵 fork 4.65× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n8/b1` | 0.000501 ± 2.08167e-05 (W 2.50998e-05) | - | 0.000592 ± 1.00167e-05 (W 1.3274e-05) | - | 🔵 fork 1.18× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.228518 ± 0.000405414 (W 0.00174486) | - | 0.515744 ± 0.00302175 (W 0.00375815) | - | 🔵 fork 2.26× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n16/b1` | 0.009177 ± 7e-05 (W 9.6479e-05) | - | 0.008135 ± 2.88675e-05 (W 4.63487e-05) | - | 🔴 fork 1.13× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 8.7674 ± 0.030943 (W 0.0247185) | - | 7.90143 ± 0.0335554 (W 0.0136104) | - | 🔴 fork 1.11× slower than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n4/b1` | 0.001242 ± 3.21455e-05 (W 3.63634e-05) | - | 0.001403 ± 1.73205e-05 (W 2.80232e-05) | - | 🔵 fork 1.13× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.74352 ± 0.00500863 (W 0.00213421) | - | 0.973684 ± 0.00234917 (W 0.0049951) | - | 🔵 fork 1.31× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n8/b1` | 0.002865 ± 3.84318e-05 (W 2.37129e-05) | - | 0.003016 ± 1.73205e-05 (W 4.62742e-05) | - | 🔵 fork 1.05× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.30348 ± 0.0029327 (W 0.00273346) | - | 2.66056 ± 0.0254895 (W 0.00412028) | - | 🔵 fork 1.16× faster than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/n16/b1` | 0.01082 ± 0.000144777 (W 5.86455e-05) | - | 0.009929 ± 7.23418e-05 (W 9.07193e-05) | - | 🔴 fork 1.09× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 10.1035 ± 0.140573 (W 0.0306426) | - | 9.41828 ± 0.00916253 (W 0.0247326) | - | 🔴 fork 1.07× slower than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/n4/b1` | 0.001894 ± 1.95021e-05 (W 3.78722e-05) | - | 0.001873 ± 1.78979e-05 (W 4.20036e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.16185 ± 0.00490162 (W 0.00249877) | - | 1.16729 ± 0.00331494 (W 0.0019451) | - | · | `*` one row has no measurement here |
| `rank_revealing_qr/n8/b1` | 0.004017 ± 4.58258e-05 (W 3.73537e-05) | - | 0.003817 ± 5.7735e-06 (W 4.72229e-05) | - | 🔴 fork 1.05× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.08566 ± 0.0384696 (W 0.00418896) | - | 3.05399 ± 0.0156709 (W 0.00930671) | - | · | `*` one row has no measurement here |
| `solve/n16/b1` | 0.003697 ± 3.05505e-05 (W 8.19756e-05) | - | 0.003777 ± 3.21455e-05 (W 6.14003e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 2.61441 ± 0.0266074 (W 0.0105029) | - | 3.31386 ± 0.0246858 (W 0.00549773) | - | 🔵 fork 1.27× faster than `lapack-openblas` | `*` one row has no measurement here |
| `solve/n4/b1` | 0.001192 ± 4.04145e-05 (W 6.64921e-05) | - | 0.000992 ± 3.21455e-05 (W 1.30384e-05) | - | 🔴 fork 1.20× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.364733 ± 0.0034749 (W 0.0025762) | - | 0.594119 ± 0.00813772 (W 0.01014) | - | 🔵 fork 1.63× faster than `lapack-openblas` | `*` one row has no measurement here |
| `solve/n8/b1` | 0.001964 ± 1.0504e-05 (W 3.78854e-05) | - | 0.001633 ± 2.64575e-05 (W 2.32852e-05) | - | 🔴 fork 1.20× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 0.910877 ± 0.0145923 (W 0.00635557) | - | 1.16207 ± 0.00364495 (W 0.00531827) | - | 🔵 fork 1.28× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_full/n16/b1` | 0.054802 ± 0.000138818 (W 0.000125643) | - | 0.081012 ± 0.000369658 (W 9.89859e-05) | - | 🔵 fork 1.48× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_full/n16/b1024` | 55.8231 ± 0.323698 (W 0.0385349) | - | 80.5678 ± 0.248509 (W 0.0712335) | - | 🔵 fork 1.44× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_full/n4/b1` | 0.004809 ± 1e-05 (W 4.3359e-05) | - | 0.007114 ± 4.00042e-05 (W 5.57961e-05) | - | 🔵 fork 1.48× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 4.21235 ± 0.019955 (W 0.00289849) | - | 6.30426 ± 0.0335173 (W 0.00939588) | - | 🔵 fork 1.50× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_full/n8/b1` | 0.015138 ± 4.33628e-05 (W 0.000100947) | - | 0.020769 ± 6.50641e-05 (W 4.49589e-05) | - | 🔵 fork 1.37× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 15.0295 ± 0.118713 (W 0.016234) | - | 21.1891 ± 0.0861436 (W 0.0229647) | - | 🔵 fork 1.41× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n16/b1` | 0.054281 ± 0.00035428 (W 0.000110001) | - | 0.08065 ± 0.000554601 (W 0.000196334) | - | 🔵 fork 1.49× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n16/b1024` | 55.6449 ± 0.431476 (W 0.0445508) | - | 80.5402 ± 0.424857 (W 0.0419226) | - | 🔵 fork 1.45× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n4/b1` | 0.004729 ± 5.7735e-06 (W 7.56968e-05) | - | 0.007144 ± 1.78979e-05 (W 2.58515e-05) | - | 🔵 fork 1.51× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 4.20882 ± 0.0428619 (W 0.0123663) | - | 6.3352 ± 0.0209018 (W 0.00851646) | - | 🔵 fork 1.51× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n8/b1` | 0.015329 ± 0.000250414 (W 0.000103682) | - | 0.020629 ± 0.000118462 (W 4.54973e-05) | - | 🔵 fork 1.35× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 15.0646 ± 0.0499283 (W 0.0291055) | - | 21.2666 ± 0.119539 (W 0.0311352) | - | 🔵 fork 1.41× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n16/b1` | 0.039935 ± 0.000272746 (W 0.0012349) | - | 0.024977 ± 0.000225167 (W 6.67705e-05) | - | 🔴 fork 1.60× slower than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n16/b1024` | 40.7082 ± 0.0755267 (W 0.0406772) | - | 25.0545 ± 0.178309 (W 0.0475853) | - | 🔴 fork 1.62× slower than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n4/b1` | 0.003757 ± 3.09892e-05 (W 8.77337e-05) | - | 0.004218 ± 6.65833e-05 (W 3.07766e-05) | - | 🔵 fork 1.12× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.16649 ± 0.00352448 (W 0.0123644) | - | 3.45134 ± 0.0213649 (W 0.00642337) | - | 🔵 fork 1.09× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n8/b1` | 0.011382 ± 6.55515e-05 (W 3.21605e-05) | - | 0.009277 ± 5.68624e-05 (W 5.93658e-05) | - | 🔴 fork 1.23× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 11.209 ± 0.0403475 (W 0.0164397) | - | 8.92642 ± 0.0519265 (W 0.017553) | - | 🔴 fork 1.26× slower than `lapack-openblas` | `*` one row has no measurement here |
| `triangular_solve/n16/b1` | 0.000982 ± 4.6188e-05 (W 5.59464e-05) | - | 0.000892 ± 9.50438e-06 (W 5.41295e-06) | - | 🔴 fork 1.10× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.504435 ± 0.0100924 (W 0.00249379) | - | 0.658109 ± 0.00279183 (W 0.00392869) | - | 🔵 fork 1.30× faster than `lapack-openblas` | `*` one row has no measurement here |
| `triangular_solve/n4/b1` | 0.000571 ± 5.7735e-06 (W 4.08656e-05) | - | 0.000491 ± 3.21455e-05 (W 1.14018e-05) | - | 🔴 fork 1.16× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.092033 ± 0.000242962 (W 0.000153262) | - | 0.253574 ± 0.0334964 (W 0.0021633) | - | 🔵 fork 2.76× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `triangular_solve/n8/b1` | 0.000701 ± 2.08167e-05 (W 4.91243e-05) | - | 0.000561 ± 5.7735e-06 (W 1.64317e-05) | - | 🔴 fork 1.25× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.219533 ± 0.00140289 (W 0.00208146) | - | 0.302555 ± 0.00123703 (W 0.00224864) | - | 🔵 fork 1.38× faster than `lapack-openblas` | `*` one row has no measurement here |

## batch-small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001202 ± 3.66106e-05 (W 4.65425e-05) | 0.001272 ± 3.80832e-05 (W 5.28517e-05) | 0.001173 ± 2.00083e-05 (W 1.51658e-05) | 🔵 fork 1.06× faster than `faer-pool` | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 0.89871 ± 0.0247246 (W 0.00134114) | 0.12311 ± 0.00482356 (W 0.00147075) | 1.02431 ± 0.00443835 (W 0.0045731) | 🔴 fork 7.30× slower than `faer-pool` | 🔵 fork 1.14× faster than `lapack-openblas` | `!` between-start range over 5% |
| `cholesky/n4/b1` | 0.000541 ± 1.52753e-05 (W 3.36155e-05) | 0.000611 ± 2.51661e-05 (W 5.48379e-05) | 0.000381 ± 1.1547e-05 (W 1.09545e-05) | 🔵 fork 1.13× faster than `faer-pool` | 🔴 fork 1.42× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.178095 ± 0.000249985 (W 0.00143971) | 0.030347 ± 0.000430965 (W 0.00112887) | 0.197611 ± 0.00134449 (W 0.00164086) | 🔴 fork 5.87× slower than `faer-pool` | 🔵 fork 1.11× faster than `lapack-openblas` |  |
| `cholesky/n8/b1` | 0.000742 ± 2.0502e-05 (W 4.58617e-05) | 0.000791 ± 2.95014e-05 (W 2.75372e-05) | 0.000571 ± 0 (W 2.49439e-05) | 🔵 fork 1.07× faster than `faer-pool` | 🔴 fork 1.30× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.359973 ± 0.000667323 (W 0.00194393) | 0.053921 ± 0.00105314 (W 0.00157031) | 0.381727 ± 0.01529 (W 0.00246947) | 🔴 fork 6.68× slower than `faer-pool` | 🔵 fork 1.06× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eig/n16/b1` | 0.090459 ± 0.000415328 (W 0.00156744) | 0.090169 ± 0.000853605 (W 0.000190959) | 0.066996 ± 0.00065793 (W 0.000165143) | · | 🔴 fork 1.35× slower than `lapack-openblas` |  |
| `eig/n16/b1024` | 94.0908 ± 0.0413153 (W 0.0767787) | 11.944 ± 0.0613523 (W 0.0516887) | 68.4354 ± 0.526976 (W 0.0453245) | 🔴 fork 7.88× slower than `faer-pool` | 🔴 fork 1.37× slower than `lapack-openblas` |  |
| `eig/n4/b1` | 0.007004 ± 2.51064e-05 (W 0.00011662) | 0.006983 ± 9.02053e-05 (W 6.09688e-05) | 0.006221 ± 3.49333e-05 (W 4.67568e-05) | · | 🔴 fork 1.13× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 6.21731 ± 0.0179028 (W 0.00780986) | 0.79598 ± 0.00296897 (W 0.00253707) | 5.37465 ± 0.0488923 (W 0.00446436) | 🔴 fork 7.81× slower than `faer-pool` | 🔴 fork 1.16× slower than `lapack-openblas` |  |
| `eig/n8/b1` | 0.024235 ± 0.00010602 (W 0.00016346) | 0.024346 ± 0.000156142 (W 6.66206e-05) | 0.018505 ± 0.00011415 (W 6.01357e-05) | · | 🔴 fork 1.31× slower than `lapack-openblas` |  |
| `eig/n8/b1024` | 23.3619 ± 0.0758831 (W 0.0414653) | 2.96116 ± 0.0128404 (W 0.00501865) | 17.6165 ± 0.15856 (W 0.0240484) | 🔴 fork 7.89× slower than `faer-pool` | 🔴 fork 1.33× slower than `lapack-openblas` |  |
| `eigh/n16/b1` | 0.029465 ± 0.000564731 (W 0.000157042) | 0.029656 ± 0.000303167 (W 9.69603e-05) | 0.038412 ± 0.000321934 (W 9.55107e-05) | · | 🔵 fork 1.30× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 29.7498 ± 0.322712 (W 0.0349085) | 3.76876 ± 0.0238564 (W 0.00538639) | 40.3685 ± 0.373792 (W 0.0776519) | 🔴 fork 7.89× slower than `faer-pool` | 🔵 fork 1.36× faster than `lapack-openblas` |  |
| `eigh/n4/b1` | 0.002816 ± 3.09892e-05 (W 4.36268e-05) | 0.002885 ± 6.16468e-05 (W 5.92723e-05) | 0.003176 ± 3.21455e-05 (W 6.42651e-05) | · | 🔵 fork 1.13× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.417 ± 0.0828378 (W 0.00763063) | 0.314749 ± 0.18357 (W 0.00137456) | 3.04573 ± 0.0193012 (W 0.00744606) | 🔴 fork 7.68× slower than `faer-pool` | 🔵 fork 1.26× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigh/n8/b1` | 0.008796 ± 4.7648e-05 (W 7.41842e-05) | 0.008897 ± 7.22519e-05 (W 5.862e-05) | 0.01068 ± 6.55744e-05 (W 6.40312e-05) | · | 🔵 fork 1.21× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 8.42543 ± 0.0684842 (W 0.0145083) | 1.08262 ± 0.13064 (W 0.00425371) | 10.8784 ± 0.0340376 (W 0.0222498) | 🔴 fork 7.78× slower than `faer-pool` | 🔵 fork 1.29× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigvals/n16/b1` | 0.061976 ± 0.000158547 (W 0.00149593) | 0.062015 ± 0.000150879 (W 0.000128146) | 0.048611 ± 0.0001105 (W 9.27362e-05) | · | 🔴 fork 1.27× slower than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 64.8296 ± 0.136724 (W 0.0611905) | 8.17514 ± 0.04453 (W 0.0261475) | 49.6157 ± 0.0352877 (W 0.0574236) | 🔴 fork 7.93× slower than `faer-pool` | 🔴 fork 1.31× slower than `lapack-openblas` |  |
| `eigvals/n4/b1` | 0.003887 ± 5.7735e-06 (W 5.62512e-05) | 0.003937 ± 7.3328e-05 (W 7.96442e-05) | 0.004178 ± 4.58258e-05 (W 2e-05) | · | 🔵 fork 1.07× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 3.24743 ± 0.0113857 (W 0.00837888) | 0.423912 ± 0.00410963 (W 0.00232181) | 3.39643 ± 0.0166339 (W 0.00426586) | 🔴 fork 7.66× slower than `faer-pool` | · |  |
| `eigvals/n8/b1` | 0.01642 ± 8.00021e-05 (W 9.08697e-05) | 0.01636 ± 0.000157121 (W 0.000117031) | 0.014257 ± 4.6694e-05 (W 5.15102e-05) | · | 🔴 fork 1.15× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 15.3714 ± 0.045608 (W 0.0182697) | 1.95078 ± 0.0320353 (W 0.0135915) | 13.2544 ± 0.0529889 (W 0.018319) | 🔴 fork 7.88× slower than `faer-pool` | 🔴 fork 1.16× slower than `lapack-openblas` |  |
| `eigvalsh/n16/b1` | 0.022322 ± 0.000140631 (W 0.000131785) | 0.022422 ± 7e-05 (W 9.08036e-05) | 0.014166 ± 5.18684e-05 (W 5.41498e-05) | · | 🔴 fork 1.58× slower than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 22.2538 ± 0.0829924 (W 0.0283856) | 2.80182 ± 0.0089998 (W 0.00240201) | 14.5592 ± 0.043461 (W 0.0260634) | 🔴 fork 7.94× slower than `faer-pool` | 🔴 fork 1.53× slower than `lapack-openblas` |  |
| `eigvalsh/n4/b1` | 0.002414 ± 4.17971e-05 (W 5.90017e-05) | 0.002475 ± 3.60555e-05 (W 8.54418e-05) | 0.001723 ± 1e-05 (W 2.64045e-05) | · | 🔴 fork 1.40× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 1.94911 ± 0.0228321 (W 0.00341517) | 0.259145 ± 0.147247 (W 0.00151548) | 1.40078 ± 0.00589297 (W 0.00259417) | 🔴 fork 7.52× slower than `faer-pool` | 🔴 fork 1.39× slower than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigvalsh/n8/b1` | 0.007233 ± 1.0504e-05 (W 6.54087e-05) | 0.007274 ± 3.50761e-05 (W 3.20936e-05) | 0.004839 ± 2.64575e-05 (W 3.71484e-05) | · | 🔴 fork 1.49× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 6.78791 ± 0.0279683 (W 0.0184326) | 0.858024 ± 0.00477221 (W 0.00393853) | 4.55189 ± 0.0255966 (W 0.00768764) | 🔴 fork 7.91× slower than `faer-pool` | 🔴 fork 1.49× slower than `lapack-openblas` |  |
| `full_piv_lu/n16/b1` | 0.004138 ± 8.5049e-05 (W 5.86447e-05) | 0.004228 ± 4.58258e-05 (W 7.31437e-05) | 0.004549 ± 6.15386e-05 (W 1.1149e-05) | · | 🔵 fork 1.10× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 3.38547 ± 0.0469094 (W 0.0140498) | 0.461647 ± 0.00249565 (W 0.00525506) | 4.71238 ± 0.0945117 (W 0.0226507) | 🔴 fork 7.33× slower than `faer-pool` | 🔵 fork 1.39× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1` | 0.001032 ± 1.52753e-05 (W 4.9295e-05) | 0.001102 ± 5.7735e-06 (W 7.71181e-05) | 0.000611 ± 1.1547e-05 (W 2.88097e-05) | 🔵 fork 1.07× faster than `faer-pool` | 🔴 fork 1.69× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.381625 ± 0.00911252 (W 0.00291489) | 0.083616 ± 0.0017765 (W 0.00209223) | 0.371407 ± 0.0158464 (W 0.00212331) | 🔴 fork 4.56× slower than `faer-pool` | · | `!` between-start range over 5% |
| `full_piv_lu/n8/b1` | 0.001794 ± 4.96689e-05 (W 8.80977e-05) | 0.001853 ± 2.51661e-05 (W 5.4289e-05) | 0.001302 ± 1.51767e-05 (W 1.12827e-05) | · | 🔴 fork 1.38× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.04296 ± 0.029268 (W 0.00687817) | 0.168084 ± 0.000283525 (W 0.00283645) | 1.01045 ± 0.0210226 (W 0.00295299) | 🔴 fork 6.20× slower than `faer-pool` | · |  |
| `full_piv_lu_solve/n16/b1` | 0.004468 ± 6.05558e-05 (W 7.31662e-05) | 0.004479 ± 9.33292e-05 (W 7.86022e-05) | 0.006562 ± 2.6839e-05 (W 3.82256e-05) | · | 🔵 fork 1.47× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 3.43495 ± 0.0434566 (W 0.00771851) | 0.451085 ± 0.0108696 (W 0.00506974) | 6.4526 ± 0.111375 (W 0.0230122) | 🔴 fork 7.61× slower than `faer-pool` | 🔵 fork 1.88× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1` | 0.001333 ± 6.4291e-05 (W 7.62974e-05) | 0.001423 ± 1.95021e-05 (W 3.4775e-05) | 0.001323 ± 1.78979e-05 (W 1.96545e-05) | 🔵 fork 1.07× faster than `faer-pool` | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.514361 ± 0.0160796 (W 0.00401251) | 0.074499 ± 0.00467237 (W 0.00198364) | 0.953743 ± 0.00173198 (W 0.0034796) | 🔴 fork 6.90× slower than `faer-pool` | 🔵 fork 1.85× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1` | 0.002204 ± 3.05014e-05 (W 6.22093e-05) | 0.002254 ± 7.78267e-05 (W 0.000117751) | 0.002325 ± 2.0664e-05 (W 2.40832e-05) | · | 🔵 fork 1.05× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.21642 ± 0.00722691 (W 0.005322) | 0.166621 ± 0.000467479 (W 0.00357201) | 1.98752 ± 0.0142054 (W 0.00301801) | 🔴 fork 7.30× slower than `faer-pool` | 🔵 fork 1.63× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1` | 0.004658 ± 0.000144777 (W 6.93347e-05) | 0.004669 ± 0.000121533 (W 3.20936e-05) | 0.005019 ± 5.0797e-05 (W 0.000108854) | · | 🔵 fork 1.08× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 4.62721 ± 0.139659 (W 0.0136954) | 0.58603 ± 0.0200741 (W 0.00338066) | 4.53262 ± 0.0230166 (W 0.0101768) | 🔴 fork 7.90× slower than `faer-pool` | · | `!` between-start range over 5% |
| `householder_apply/n4/b1` | 0.000641 ± 1.58219e-05 (W 5.34434e-05) | 0.000691 ± 1.47309e-05 (W 3.81995e-05) | 0.001042 ± 1.0504e-05 (W 3.53553e-05) | 🔵 fork 1.08× faster than `faer-pool` | 🔵 fork 1.63× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.359463 ± 0.00868793 (W 0.00215036) | 0.052077 ± 0.00203466 (W 0.00187891) | 0.418813 ± 0.000674611 (W 0.00208876) | 🔴 fork 6.90× slower than `faer-pool` | 🔵 fork 1.17× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n8/b1` | 0.001482 ± 4.72582e-05 (W 4.73308e-05) | 0.001503 ± 5.1316e-05 (W 2.5046e-05) | 0.001884 ± 4.58258e-05 (W 3.77001e-05) | · | 🔵 fork 1.27× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.18338 ± 0.021321 (W 0.00356264) | 0.166402 ± 0.00605756 (W 0.00135449) | 1.21095 ± 0.0044206 (W 0.00255784) | 🔴 fork 7.11× slower than `faer-pool` | · | `!` between-start range over 5% |
| `householder_factor/n16/b1` | 0.003877 ± 3.21455e-05 (W 9.43361e-05) | 0.003908 ± 3.06649e-05 (W 6.30262e-05) | 0.004629 ± 2.51661e-05 (W 4.86642e-05) | · | 🔵 fork 1.19× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 3.6353 ± 0.0282314 (W 0.00433382) | 0.474987 ± 0.00429503 (W 0.00152477) | 4.38222 ± 0.0214251 (W 0.0119298) | 🔴 fork 7.65× slower than `faer-pool` | 🔵 fork 1.21× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1` | 0.000691 ± 2.51661e-05 (W 3.15785e-05) | 0.000721 ± 9.50438e-06 (W 4.59162e-05) | 0.000802 ± 5.7735e-06 (W 3.25607e-05) | · | 🔵 fork 1.16× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.4382 ± 0.00431427 (W 0.0018807) | 0.063479 ± 0.00022301 (W 0.000469798) | 0.537835 ± 0.0039068 (W 0.00220369) | 🔴 fork 6.90× slower than `faer-pool` | 🔵 fork 1.23× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1` | 0.001393 ± 2.91605e-05 (W 3.96257e-05) | 0.001422 ± 1.95021e-05 (W 2.08878e-05) | 0.001793 ± 1.0504e-05 (W 5.24147e-05) | · | 🔵 fork 1.29× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.18525 ± 0.0362037 (W 0.00250494) | 0.171601 ± 0.0038111 (W 0.00171454) | 1.51467 ± 0.00721906 (W 0.00389379) | 🔴 fork 6.91× slower than `faer-pool` | 🔵 fork 1.28× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n16/b1` | 0.003176 ± 7.57188e-05 (W 5.58856e-05) | 0.003276 ± 5.1316e-05 (W 0.000134552) | 0.002785 ± 3.78594e-05 (W 4.79583e-05) | · | 🔴 fork 1.14× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 2.59528 ± 0.0710904 (W 0.00886942) | 0.369651 ± 0.0026495 (W 0.00567118) | 2.43045 ± 0.011933 (W 0.00896667) | 🔴 fork 7.02× slower than `faer-pool` | 🔴 fork 1.07× slower than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n4/b1` | 0.000792 ± 2.6839e-05 (W 4.51254e-05) | 0.000852 ± 3.06649e-05 (W 5.09529e-05) | 0.000591 ± 1.52753e-05 (W 3.4641e-05) | 🔵 fork 1.08× faster than `faer-pool` | 🔴 fork 1.34× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.305452 ± 0.00450604 (W 0.00192239) | 0.07433 ± 0.000605908 (W 0.00272265) | 0.32471 ± 0.00406501 (W 0.00323377) | 🔴 fork 4.11× slower than `faer-pool` | 🔵 fork 1.06× faster than `lapack-openblas` |  |
| `lu/n8/b1` | 0.001332 ± 1.70392e-05 (W 5.9618e-05) | 0.001383 ± 2.64575e-05 (W 2.56574e-05) | 0.001092 ± 2e-05 (W 4.49444e-05) | · | 🔴 fork 1.22× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.806977 ± 0.0192879 (W 0.00480938) | 0.144249 ± 0.00285655 (W 0.00307329) | 0.814792 ± 0.0225114 (W 0.00420291) | 🔴 fork 5.59× slower than `faer-pool` | · | `!` between-start range over 5% |
| `lu_factor/n16/b1` | 0.002094 ± 4.58258e-05 (W 5.54076e-05) | 0.002124 ± 3e-05 (W 5.05292e-05) | 0.001893 ± 5.7735e-06 (W 3.04844e-05) | · | 🔴 fork 1.11× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 1.88933 ± 0.017902 (W 0.0045236) | 0.269974 ± 0.00726167 (W 0.0039209) | 1.81483 ± 0.0131529 (W 0.00451135) | 🔴 fork 7.00× slower than `faer-pool` | · | `!` between-start range over 5% |
| `lu_factor/n4/b1` | 0.000531 ± 3.25115e-05 (W 4.79583e-05) | 0.000551 ± 2.08167e-05 (W 6.26099e-05) | 0.000301 ± 1.67432e-05 (W 3.66511e-05) | · | 🔴 fork 1.76× slower than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.219992 ± 0.00246606 (W 0.00162593) | 0.064642 ± 0.00170932 (W 0.00169631) | 0.21914 ± 0.00038368 (W 0.00161525) | 🔴 fork 3.40× slower than `faer-pool` | · |  |
| `lu_factor/n8/b1` | 0.000882 ± 2.51661e-05 (W 5.11889e-05) | 0.000891 ± 4.32474e-05 (W 3.35753e-05) | 0.000651 ± 1.58219e-05 (W 1.84201e-05) | · | 🔴 fork 1.35× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.584374 ± 0.00708597 (W 0.00258368) | 0.11151 ± 0.00214547 (W 0.000995601) | 0.573608 ± 0.00599222 (W 0.00457821) | 🔴 fork 5.24× slower than `faer-pool` | · |  |
| `lu_factor_solve/n16/b1` | 0.002815 ± 5.7735e-06 (W 5.18093e-05) | 0.002835 ± 6.35085e-06 (W 4.32574e-05) | 0.003777 ± 6.65833e-05 (W 9.71082e-05) | · | 🔵 fork 1.34× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 2.41709 ± 0.0172369 (W 0.00625122) | 0.335451 ± 0.00358604 (W 0.00418502) | 3.80576 ± 0.062617 (W 0.00572018) | 🔴 fork 7.21× slower than `faer-pool` | 🔵 fork 1.57× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1` | 0.000591 ± 5.7735e-07 (W 6.36412e-05) | 0.000612 ± 5.50757e-06 (W 4.76151e-05) | 0.001242 ± 6.65833e-05 (W 5.85688e-05) | · | 🔵 fork 2.10× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.277479 ± 0.00270743 (W 0.00251688) | 0.063961 ± 0.000773866 (W 0.00132558) | 1.25837 ± 0.0521809 (W 0.0039269) | 🔴 fork 4.34× slower than `faer-pool` | 🔵 fork 4.54× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1` | 0.001173 ± 3.00056e-05 (W 5.49936e-05) | 0.001212 ± 1.1547e-05 (W 9.18874e-05) | 0.001593 ± 0.000240901 (W 3.78153e-05) | · | 🔵 fork 1.36× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 0.805478 ± 0.0151687 (W 0.0027875) | 0.129983 ± 0.00145763 (W 0.00284614) | 2.02449 ± 0.0070776 (W 0.00332012) | 🔴 fork 6.20× slower than `faer-pool` | 🔵 fork 2.51× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1` | 0.000911 ± 1.53948e-05 (W 5.55986e-05) | 0.000921 ± 2.58908e-05 (W 3.99775e-05) | 0.001693 ± 0.00013 (W 0.000105723) | · | 🔵 fork 1.86× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 0.596836 ± 0.0129207 (W 0.00234026) | 0.106819 ± 0.00201108 (W 0.000784187) | 1.55601 ± 0.0479553 (W 0.00350009) | 🔴 fork 5.59× slower than `faer-pool` | 🔵 fork 2.61× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1` | 0.000361 ± 3.10966e-05 (W 3.80565e-05) | 0.000361 ± 4.3589e-05 (W 5.06952e-05) | 0.001002 ± 0.000165227 (W 6.34823e-05) | · | 🔵 fork 2.78× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.067436 ± 0.000462396 (W 8.37096e-05) | 0.033894 ± 0.000578815 (W 0.000973157) | 0.836666 ± 0.0426462 (W 0.00414112) | 🔴 fork 1.99× slower than `faer-pool` | 🔵 fork 12.41× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1` | 0.000541 ± 4.16333e-05 (W 3.28634e-05) | 0.000531 ± 3.15331e-05 (W 2.54951e-05) | 0.001383 ± 8.00021e-05 (W 7.56987e-05) | · | 🔵 fork 2.56× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.229749 ± 0.000737734 (W 0.00168353) | 0.055434 ± 0.000798092 (W 0.00173552) | 1.23452 ± 0.0141612 (W 0.00485035) | 🔴 fork 4.14× slower than `faer-pool` | 🔵 fork 5.37× faster than `lapack-openblas` |  |
| `qr/n16/b1` | 0.008917 ± 0.000277849 (W 0.000181025) | 0.008986 ± 0.000266736 (W 0.000118322) | 0.008205 ± 6.08276e-06 (W 9.4606e-05) | · | 🔴 fork 1.09× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 8.58527 ± 0.26061 (W 0.019258) | 1.1352 ± 0.0277075 (W 0.00410429) | 7.89397 ± 0.0338494 (W 0.0172446) | 🔴 fork 7.56× slower than `faer-pool` | 🔴 fork 1.09× slower than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n4/b1` | 0.001253 ± 2.12211e-05 (W 3.9119e-05) | 0.001302 ± 5.7735e-07 (W 2.53436e-05) | 0.001423 ± 1.1547e-05 (W 6.44143e-05) | · | 🔵 fork 1.14× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.731718 ± 0.00721158 (W 0.00267037) | 0.099818 ± 0.00122844 (W 0.00151875) | 0.962652 ± 0.00278112 (W 0.00335369) | 🔴 fork 7.33× slower than `faer-pool` | 🔵 fork 1.32× faster than `lapack-openblas` |  |
| `qr/n8/b1` | 0.003036 ± 0.000110151 (W 8.19713e-05) | 0.002976 ± 9.20887e-05 (W 5.68357e-05) | 0.003066 ± 2.08167e-05 (W 4.29802e-05) | · | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.36803 ± 0.0837663 (W 0.00575157) | 0.317904 ± 0.0124823 (W 0.00186502) | 2.6572 ± 0.0154271 (W 0.0216357) | 🔴 fork 7.45× slower than `faer-pool` | 🔵 fork 1.12× faster than `lapack-openblas` | `!` between-start range over 5% |
| `rank_revealing_qr/n16/b1` | 0.01081 ± 0.000235514 (W 8.21724e-05) | 0.010871 ± 0.000215028 (W 6.9414e-05) | 0.009978 ± 8.56174e-05 (W 0.000100349) | · | 🔴 fork 1.08× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 10.1164 ± 0.250991 (W 0.0114617) | 1.29717 ± 0.0306595 (W 0.00410575) | 9.44386 ± 0.0368045 (W 0.0159564) | 🔴 fork 7.80× slower than `faer-pool` | 🔴 fork 1.07× slower than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1` | 0.001864 ± 2.3388e-05 (W 7.56062e-05) | 0.001934 ± 2.51661e-05 (W 9.87279e-05) | 0.001883 ± 7.2111e-05 (W 4.98126e-05) | · | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.16526 ± 0.00821958 (W 0.00408819) | 0.153177 ± 0.000297837 (W 0.00183567) | 1.16825 ± 0.00717846 (W 0.00316325) | 🔴 fork 7.61× slower than `faer-pool` | · |  |
| `rank_revealing_qr/n8/b1` | 0.004008 ± 2.0502e-05 (W 4.08203e-05) | 0.004028 ± 3e-05 (W 1.70382e-05) | 0.003797 ± 2.5697e-05 (W 7.55268e-05) | · | 🔴 fork 1.06× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.11506 ± 0.0367522 (W 0.00454993) | 0.404967 ± 0.0133709 (W 0.00221148) | 3.05218 ± 0.0126777 (W 0.00489739) | 🔴 fork 7.69× slower than `faer-pool` | · | `!` between-start range over 5% |
| `solve/n16/b1` | 0.003737 ± 4.93288e-05 (W 4.84768e-05) | 0.003837 ± 0.000108786 (W 7.45533e-05) | 0.003798 ± 7.55006e-05 (W 3.96232e-05) | · | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 2.6367 ± 0.0340644 (W 0.0107241) | 0.35844 ± 0.00376385 (W 0.00159137) | 3.73611 ± 0.0482962 (W 0.0120218) | 🔴 fork 7.36× slower than `faer-pool` | 🔵 fork 1.42× faster than `lapack-openblas` |  |
| `solve/n4/b1` | 0.001222 ± 4.16333e-05 (W 5.43526e-05) | 0.001253 ± 1.76163e-05 (W 6.56909e-05) | 0.001674 ± 2.28108e-05 (W 6.98584e-05) | · | 🔵 fork 1.37× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.363741 ± 0.00273948 (W 0.00282434) | 0.054081 ± 0.000948458 (W 0.000789226) | 1.38154 ± 0.0519371 (W 0.00581139) | 🔴 fork 6.73× slower than `faer-pool` | 🔵 fork 3.80× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1` | 0.002014 ± 3.60555e-05 (W 7.68518e-05) | 0.001984 ± 7.25282e-05 (W 5.59464e-05) | 0.001943 ± 0.000222913 (W 3.40632e-05) | · | · | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 0.900403 ± 0.0217561 (W 0.00824803) | 0.129343 ± 0.00166891 (W 0.00310186) | 2.01787 ± 0.0324453 (W 0.00271806) | 🔴 fork 6.96× slower than `faer-pool` | 🔵 fork 2.24× faster than `lapack-openblas` |  |
| `svd_full/n16/b1` | 0.054411 ± 0.000354636 (W 0.000318374) | 0.054552 ± 0.000240069 (W 0.00011068) | 0.081413 ± 0.000965869 (W 0.000100764) | · | 🔵 fork 1.50× faster than `lapack-openblas` |  |
| `svd_full/n16/b1024` | 55.6339 ± 0.0969829 (W 0.028718) | 7.21028 ± 0.122967 (W 0.0429669) | 80.804 ± 0.884016 (W 0.110102) | 🔴 fork 7.72× slower than `faer-pool` | 🔵 fork 1.45× faster than `lapack-openblas` |  |
| `svd_full/n4/b1` | 0.004779 ± 5.08626e-05 (W 5.93296e-05) | 0.004849 ± 5.68624e-05 (W 6.0936e-05) | 0.007214 ± 5.53203e-05 (W 4.89724e-05) | · | 🔵 fork 1.51× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 4.22194 ± 0.0373062 (W 0.0110131) | 0.544619 ± 0.00556135 (W 0.00415164) | 6.36658 ± 0.0512315 (W 0.0143694) | 🔴 fork 7.75× slower than `faer-pool` | 🔵 fork 1.51× faster than `lapack-openblas` |  |
| `svd_full/n8/b1` | 0.015149 ± 6.82422e-05 (W 6.73662e-05) | 0.015188 ± 6.9282e-05 (W 5.89008e-05) | 0.020919 ± 0.000184481 (W 5.76481e-05) | · | 🔵 fork 1.38× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 15.0809 ± 0.114179 (W 0.0193632) | 1.95965 ± 0.0216895 (W 0.0190005) | 21.2792 ± 0.182729 (W 0.045557) | 🔴 fork 7.70× slower than `faer-pool` | 🔵 fork 1.41× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1` | 0.054361 ± 0.000239952 (W 0.00139543) | 0.054432 ± 0.000130512 (W 0.000138225) | 0.082044 ± 0.000861039 (W 0.000116289) | · | 🔵 fork 1.51× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 55.6786 ± 0.233763 (W 0.0477276) | 7.13808 ± 0.122275 (W 0.141384) | 80.9163 ± 0.866115 (W 0.395464) | 🔴 fork 7.80× slower than `faer-pool` | 🔵 fork 1.45× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1` | 0.004749 ± 3.78594e-05 (W 6.65582e-05) | 0.004789 ± 5.50757e-05 (W 8.73499e-05) | 0.007224 ± 7.05715e-05 (W 3.70837e-05) | · | 🔵 fork 1.52× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 4.18502 ± 0.0122835 (W 0.00318942) | 0.559601 ± 0.0134385 (W 0.00463354) | 6.33266 ± 0.0207564 (W 0.0168678) | 🔴 fork 7.48× slower than `faer-pool` | 🔵 fork 1.51× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1` | 0.015088 ± 0.000131036 (W 0.000103053) | 0.015169 ± 9.06661e-05 (W 6.7082e-05) | 0.020839 ± 7.63763e-05 (W 5.26308e-05) | · | 🔵 fork 1.38× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 15.0885 ± 0.0432206 (W 0.0300021) | 1.92818 ± 0.00621106 (W 0.00713274) | 21.2923 ± 0.209248 (W 0.0293813) | 🔴 fork 7.83× slower than `faer-pool` | 🔵 fork 1.41× faster than `lapack-openblas` |  |
| `svd_values/n16/b1` | 0.040085 ± 0.000257962 (W 0.000127966) | 0.039924 ± 6.69104e-05 (W 7.82707e-05) | 0.024947 ± 9.11976e-05 (W 9.48536e-05) | · | 🔴 fork 1.61× slower than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 40.6806 ± 0.167278 (W 0.0633632) | 5.1353 ± 0.0263336 (W 0.0178356) | 25.0946 ± 0.171806 (W 0.0362986) | 🔴 fork 7.92× slower than `faer-pool` | 🔴 fork 1.62× slower than `lapack-openblas` |  |
| `svd_values/n4/b1` | 0.003627 ± 4.3589e-05 (W 0.000159043) | 0.003747 ± 2.51661e-05 (W 6.69328e-05) | 0.004268 ± 4.3589e-05 (W 8.46416e-05) | · | 🔵 fork 1.18× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.17181 ± 0.0194765 (W 0.00523361) | 0.410658 ± 0.00183836 (W 0.00268512) | 3.45497 ± 0.00598262 (W 0.00853914) | 🔴 fork 7.72× slower than `faer-pool` | 🔵 fork 1.09× faster than `lapack-openblas` |  |
| `svd_values/n8/b1` | 0.011452 ± 3.76431e-05 (W 4.50577e-05) | 0.011552 ± 3.78594e-05 (W 9.68205e-05) | 0.009297 ± 5.25389e-05 (W 4.21462e-05) | · | 🔴 fork 1.23× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 11.2408 ± 0.0418029 (W 0.0183809) | 1.43426 ± 0.00412318 (W 0.00664167) | 8.94711 ± 0.0245462 (W 0.00984065) | 🔴 fork 7.84× slower than `faer-pool` | 🔴 fork 1.26× slower than `lapack-openblas` |  |
| `triangular_solve/n16/b1` | 0.000992 ± 1.52753e-05 (W 2.88097e-05) | 0.000992 ± 2.08167e-05 (W 2.07364e-05) | 0.001362 ± 7.99396e-05 (W 6.05169e-05) | · | 🔵 fork 1.37× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.513961 ± 0.00746094 (W 0.00284638) | 0.08587 ± 0.00164811 (W 0.00354915) | 1.07002 ± 0.113532 (W 0.00771948) | 🔴 fork 5.99× slower than `faer-pool` | 🔵 fork 2.08× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n4/b1` | 0.000611 ± 4e-05 (W 5.59464e-05) | 0.000591 ± 1.95021e-05 (W 3.57771e-05) | 0.000971 ± 2.66521e-05 (W 3.64692e-05) | · | 🔵 fork 1.59× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.091801 ± 0.000263751 (W 0.000245917) | 0.019046 ± 0.00041625 (W 0.000626786) | 0.777804 ± 0.0327721 (W 0.005704) | 🔴 fork 4.82× slower than `faer-pool` | 🔵 fork 8.47× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n8/b1` | 0.000702 ± 1.52753e-05 (W 2.58128e-05) | 0.000722 ± 4.57202e-05 (W 2.97876e-05) | 0.001132 ± 0.000134946 (W 3.20811e-05) | · | 🔵 fork 1.61× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.220374 ± 0.000963578 (W 0.00243613) | 0.035326 ± 0.0179401 (W 0.00373736) | 0.836594 ± 0.0233286 (W 0.00577323) | 🔴 fork 6.24× slower than `faer-pool` | 🔵 fork 3.80× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |

## batch-small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001603 ± 4.16333e-05 (W 2e-05) | - | 0.001653 ± 1.52753e-05 (W 3.76457e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 1.29278 ± 0.0227275 (W 0.00379635) | - | 1.56365 ± 0.00924742 (W 0.0196381) | - | 🔵 fork 1.21× faster than `lapack-openblas` | `*` one row has no measurement here |
| `cholesky/n4/b1` | 0.000561 ± 1.52753e-05 (W 7.02225e-05) | - | 0.000401 ± 5.7735e-06 (W 1.35757e-05) | - | 🔴 fork 1.40× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.197231 ± 0.00313399 (W 0.00153167) | - | 0.22468 ± 0.00211229 (W 0.00134631) | - | 🔵 fork 1.14× faster than `lapack-openblas` | `*` one row has no measurement here |
| `cholesky/n8/b1` | 0.000791 ± 5.7735e-07 (W 2.97876e-05) | - | 0.000652 ± 1.00167e-05 (W 8.31865e-06) | - | 🔴 fork 1.21× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.429074 ± 0.0198052 (W 0.00264626) | - | 0.490432 ± 0.00941269 (W 0.00229524) | - | 🔵 fork 1.14× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `eig/n16/b1` | 0.121689 ± 0.000512915 (W 0.00146991) | - | 0.166973 ± 0.000398288 (W 0.000986998) | - | 🔵 fork 1.37× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n16/b1024` | 128.41 ± 0.213033 (W 0.0418288) | - | 199.081 ± 0.338717 (W 0.265895) | - | 🔵 fork 1.55× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n4/b1` | 0.01033 ± 0.000118773 (W 0.000197622) | - | 0.013605 ± 3.50761e-05 (W 6.29071e-05) | - | 🔵 fork 1.32× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 10.0201 ± 0.0755085 (W 0.0203267) | - | 13.2196 ± 0.0422447 (W 0.0303736) | - | 🔵 fork 1.32× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n8/b1` | 0.034023 ± 0.000195679 (W 0.000253547) | - | 0.043741 ± 7.06706e-05 (W 0.000103563) | - | 🔵 fork 1.29× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eig/n8/b1024` | 34.8661 ± 0.0148462 (W 0.0435453) | - | 46.6937 ± 0.147634 (W 0.20344) | - | 🔵 fork 1.34× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n16/b1` | 0.030287 ± 0.000115036 (W 0.0010692) | - | 0.043231 ± 0.000473146 (W 5.94138e-05) | - | 🔵 fork 1.43× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n16/b1024` | 32.103 ± 0.0938529 (W 0.0519437) | - | 45.027 ± 0.391493 (W 0.052485) | - | 🔵 fork 1.40× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n4/b1` | 0.003487 ± 6.55006e-05 (W 5.92225e-05) | - | 0.003677 ± 3.09892e-05 (W 1.64317e-05) | - | 🔵 fork 1.05× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.90309 ± 0.00968051 (W 0.0068815) | - | 3.52392 ± 0.0165206 (W 0.00432224) | - | 🔵 fork 1.21× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigh/n8/b1` | 0.009718 ± 5.7735e-06 (W 6.34768e-05) | - | 0.011932 ± 0.000104978 (W 6.65222e-05) | - | 🔵 fork 1.23× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 9.09802 ± 0.0455187 (W 0.013298) | - | 12.3114 ± 0.0345821 (W 0.0364639) | - | 🔵 fork 1.35× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n16/b1` | 0.072676 ± 0.000419405 (W 0.000136382) | - | 0.124823 ± 0.000616909 (W 0.00146025) | - | 🔵 fork 1.72× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n16/b1024` | 77.549 ± 0.118291 (W 0.0893637) | - | 149.377 ± 0.205791 (W 0.250861) | - | 🔵 fork 1.93× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n4/b1` | 0.00529 ± 1.1547e-05 (W 9.50263e-05) | - | 0.0106 ± 4.04145e-05 (W 5.69228e-05) | - | 🔵 fork 2.00× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 4.76547 ± 0.0169723 (W 0.00385005) | - | 10.055 ± 0.029849 (W 0.0250404) | - | 🔵 fork 2.11× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvals/n8/b1` | 0.019717 ± 9.16515e-05 (W 9.19853e-05) | - | 0.035116 ± 5.17397e-05 (W 4.53134e-05) | - | 🔵 fork 1.78× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 19.8354 ± 0.0319272 (W 0.0311168) | - | 37.0291 ± 0.0930561 (W 0.0313832) | - | 🔵 fork 1.87× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n16/b1` | 0.022943 ± 0.000109697 (W 8.77496e-05) | - | 0.019145 ± 2.28108e-05 (W 6.8775e-05) | - | 🔴 fork 1.20× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n16/b1024` | 23.741 ± 0.0302873 (W 0.0312997) | - | 19.1971 ± 0.048258 (W 0.0334381) | - | 🔴 fork 1.24× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n4/b1` | 0.002966 ± 1.73205e-05 (W 0.00014145) | - | 0.002504 ± 5.50757e-06 (W 3.31708e-05) | - | 🔴 fork 1.18× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 2.35773 ± 0.019895 (W 0.00728927) | - | 2.07804 ± 0.00814208 (W 0.00427596) | - | 🔴 fork 1.13× slower than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n8/b1` | 0.007874 ± 2.09841e-05 (W 8.3978e-05) | - | 0.006502 ± 5.7735e-07 (W 5.76212e-05) | - | 🔴 fork 1.21× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 7.28506 ± 0.0331917 (W 0.0166448) | - | 6.06578 ± 0.0248787 (W 0.0138798) | - | 🔴 fork 1.20× slower than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu/n16/b1` | 0.00506 ± 9.34719e-05 (W 5.01727e-05) | - | 0.020328 ± 9.71253e-05 (W 3.84213e-05) | - | 🔵 fork 4.02× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 4.41606 ± 0.0496717 (W 0.0240282) | - | 33.5672 ± 0.210935 (W 0.0554578) | - | 🔵 fork 7.60× faster than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu/n4/b1` | 0.001113 ± 4.0501e-05 (W 3.92454e-05) | - | 0.001062 ± 2e-05 (W 1.48324e-05) | - | · | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.471441 ± 0.0152955 (W 0.00311499) | - | 0.911944 ± 0.00500553 (W 0.00268146) | - | 🔵 fork 1.93× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `full_piv_lu/n8/b1` | 0.002104 ± 1.52753e-05 (W 8.8713e-05) | - | 0.003747 ± 3.4641e-05 (W 2.70185e-05) | - | 🔵 fork 1.78× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.26628 ± 0.01222 (W 0.00533238) | - | 3.87879 ± 0.0344275 (W 0.0151493) | - | 🔵 fork 3.06× faster than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu_solve/n16/b1` | 0.006222 ± 3.82143e-05 (W 5.57153e-05) | - | 0.025868 ± 0.000379519 (W 6.18159e-05) | - | 🔵 fork 4.16× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 5.31339 ± 0.109414 (W 0.0149484) | - | 37.6955 ± 0.0565069 (W 0.14011) | - | 🔵 fork 7.09× faster than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu_solve/n4/b1` | 0.001654 ± 1.53948e-05 (W 6.65597e-05) | - | 0.002154 ± 4.93288e-05 (W 3.54429e-05) | - | 🔵 fork 1.30× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.801571 ± 0.00704294 (W 0.00450607) | - | 1.91668 ± 0.0108743 (W 0.00464794) | - | 🔵 fork 2.39× faster than `lapack-openblas` | `*` one row has no measurement here |
| `full_piv_lu_solve/n8/b1` | 0.002916 ± 4.04145e-05 (W 8.4097e-05) | - | 0.006021 ± 8.75233e-05 (W 3.23914e-05) | - | 🔵 fork 2.06× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.93409 ± 0.0236948 (W 0.0130464) | - | 5.97803 ± 0.0635961 (W 0.0157719) | - | 🔵 fork 3.09× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_apply/n16/b1` | 0.004579 ± 1e-05 (W 2.67451e-05) | - | 0.007644 ± 7.23418e-05 (W 7.97822e-05) | - | 🔵 fork 1.67× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 5.02081 ± 0.0124735 (W 0.0116062) | - | 7.0024 ± 0.145982 (W 0.0177671) | - | 🔵 fork 1.39× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_apply/n4/b1` | 0.000621 ± 2.51661e-05 (W 2.60998e-05) | - | 0.001393 ± 1.52753e-05 (W 2.62907e-05) | - | 🔵 fork 2.24× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.332936 ± 0.00106746 (W 0.00258144) | - | 0.449055 ± 0.00436245 (W 0.00203691) | - | 🔵 fork 1.35× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_apply/n8/b1` | 0.001332 ± 2.28108e-05 (W 1.95525e-05) | - | 0.002414 ± 2.52389e-05 (W 3.24238e-05) | - | 🔵 fork 1.81× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.10791 ± 0.00840926 (W 0.0015976) | - | 1.49974 ± 0.00575422 (W 0.0039632) | - | 🔵 fork 1.35× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_factor/n16/b1` | 0.004558 ± 3.00056e-05 (W 2.78801e-05) | - | 0.007564 ± 3.21455e-05 (W 3.81733e-05) | - | 🔵 fork 1.66× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 4.41985 ± 0.0396981 (W 0.0103151) | - | 7.36219 ± 0.0261891 (W 0.0252921) | - | 🔵 fork 1.67× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_factor/n4/b1` | 0.000792 ± 1.52753e-05 (W 5.88073e-05) | - | 0.001222 ± 2.02567e-05 (W 3.72465e-05) | - | 🔵 fork 1.54× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.552303 ± 0.0136511 (W 0.00204631) | - | 0.923817 ± 0.000580155 (W 0.00477802) | - | 🔵 fork 1.67× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_factor/n8/b1` | 0.001643 ± 0 (W 2.58844e-05) | - | 0.002665 ± 1.52753e-05 (W 1.87083e-05) | - | 🔵 fork 1.62× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.42117 ± 0.0102022 (W 0.00384714) | - | 2.35876 ± 0.00980407 (W 0.00306791) | - | 🔵 fork 1.66× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu/n16/b1` | 0.003597 ± 3.00056e-05 (W 3.20656e-05) | - | 0.003847 ± 5.7735e-07 (W 0.000145758) | - | 🔵 fork 1.07× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 2.99256 ± 0.0561847 (W 0.0102971) | - | 4.00502 ± 0.0131289 (W 0.0214276) | - | 🔵 fork 1.34× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu/n4/b1` | 0.000882 ± 1.1547e-05 (W 4.26063e-05) | - | 0.000662 ± 1.1547e-05 (W 3.03513e-05) | - | 🔴 fork 1.33× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.36162 ± 0.00343495 (W 0.00240053) | - | 0.376238 ± 0.00131227 (W 0.00203406) | - | · | `*` one row has no measurement here |
| `lu/n8/b1` | 0.001583 ± 6.0803e-05 (W 0.000173551) | - | 0.001393 ± 2.51661e-05 (W 4.97825e-05) | - | 🔴 fork 1.14× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.907667 ± 0.0102913 (W 0.0105645) | - | 1.06718 ± 0.0118681 (W 0.00327226) | - | 🔵 fork 1.18× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor/n16/b1` | 0.002324 ± 4.95681e-05 (W 2.34798e-05) | - | 0.002705 ± 1.1547e-05 (W 4.50555e-05) | - | 🔵 fork 1.16× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 2.09911 ± 0.0231512 (W 0.00766964) | - | 2.71087 ± 0.0176616 (W 0.0144212) | - | 🔵 fork 1.29× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor/n4/b1` | 0.000571 ± 1.48436e-05 (W 6.05805e-05) | - | 0.00035 ± 5.19615e-06 (W 2.24767e-05) | - | 🔴 fork 1.63× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.2667 ± 0.00325269 (W 0.00184957) | - | 0.269123 ± 0.000985805 (W 0.00208036) | - | · | `*` one row has no measurement here |
| `lu_factor/n8/b1` | 0.000962 ± 4.50925e-05 (W 2.28035e-05) | - | 0.000821 ± 5.7735e-06 (W 2.47447e-05) | - | 🔴 fork 1.17× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.670071 ± 0.0253838 (W 0.0022606) | - | 0.753822 ± 0.00118541 (W 0.00230045) | - | 🔵 fork 1.12× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `lu_factor_solve/n16/b1` | 0.003777 ± 2.60832e-05 (W 0.000110055) | - | 0.004388 ± 4.45758e-05 (W 5.89915e-05) | - | 🔵 fork 1.16× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 3.35421 ± 0.0594579 (W 0.00920994) | - | 4.39663 ± 0.0242902 (W 0.0104239) | - | 🔵 fork 1.31× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor_solve/n4/b1` | 0.000812 ± 1e-05 (W 4.04623e-05) | - | 0.000772 ± 9.50438e-06 (W 2.07196e-05) | - | 🔴 fork 1.05× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.420626 ± 0.00577985 (W 0.00242767) | - | 0.669082 ± 0.00585941 (W 0.00283454) | - | 🔵 fork 1.59× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor_solve/n8/b1` | 0.001543 ± 5.56776e-05 (W 4.39318e-05) | - | 0.001634 ± 1.51767e-05 (W 2.58844e-05) | - | 🔵 fork 1.06× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 1.13485 ± 0.0205757 (W 0.0045856) | - | 1.51463 ± 0.0119599 (W 0.00237157) | - | 🔵 fork 1.33× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n16/b1` | 0.001533 ± 1.1547e-05 (W 5.44977e-05) | - | 0.001683 ± 5.7735e-06 (W 3.75007e-05) | - | 🔵 fork 1.10× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 1.32184 ± 0.000957749 (W 0.00377351) | - | 1.67786 ± 0.0183521 (W 0.00524606) | - | 🔵 fork 1.27× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n4/b1` | 0.000461 ± 1.0504e-05 (W 5.4037e-05) | - | 0.000491 ± 1e-05 (W 3.49285e-05) | - | 🔵 fork 1.07× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.163676 ± 0.00213705 (W 0.00187767) | - | 0.399818 ± 0.00222907 (W 0.00217419) | - | 🔵 fork 2.44× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n8/b1` | 0.000791 ± 1.51767e-05 (W 2.79875e-05) | - | 0.000832 ± 1.0504e-05 (W 5.41295e-06) | - | 🔵 fork 1.05× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.492286 ± 0.00185588 (W 0.00220804) | - | 0.761593 ± 0.0108973 (W 0.00192212) | - | 🔵 fork 1.55× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n16/b1` | 0.011321 ± 5.50757e-05 (W 8.92709e-05) | - | 0.012824 ± 0.000104484 (W 8.68907e-05) | - | 🔵 fork 1.13× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 11.0085 ± 0.058367 (W 0.0374089) | - | 12.6046 ± 0.0644011 (W 0.0173895) | - | 🔵 fork 1.14× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n4/b1` | 0.001373 ± 9.50438e-06 (W 8.35835e-05) | - | 0.001893 ± 9.50438e-06 (W 4.06485e-05) | - | 🔵 fork 1.38× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.858608 ± 0.00581005 (W 0.00146854) | - | 1.37776 ± 0.00176171 (W 0.00385124) | - | 🔵 fork 1.60× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n8/b1` | 0.003186 ± 1.73205e-05 (W 9.5289e-05) | - | 0.004288 ± 1.1547e-05 (W 2.96648e-05) | - | 🔵 fork 1.35× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.59537 ± 0.00453581 (W 0.00330303) | - | 3.74358 ± 0.0107201 (W 0.00403135) | - | 🔵 fork 1.44× faster than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/n16/b1` | 0.012724 ± 7.81025e-05 (W 8.20366e-05) | - | 0.016541 ± 4.72582e-05 (W 6.97854e-05) | - | 🔵 fork 1.30× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 12.1993 ± 0.0189472 (W 0.0278864) | - | 16.7657 ± 0.0746202 (W 0.113933) | - | 🔵 fork 1.37× faster than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/n4/b1` | 0.002063 ± 4.17971e-05 (W 1.88468e-05) | - | 0.002695 ± 5.91636e-05 (W 7.8091e-05) | - | 🔵 fork 1.31× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.37095 ± 0.00403289 (W 0.00561698) | - | 1.7727 ± 0.0087456 (W 0.00734762) | - | 🔵 fork 1.29× faster than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/n8/b1` | 0.004388 ± 1.52753e-05 (W 8.78635e-05) | - | 0.005621 ± 2.09841e-05 (W 5.99858e-05) | - | 🔵 fork 1.28× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.67907 ± 0.0427269 (W 0.0035666) | - | 4.99468 ± 0.0329831 (W 0.0171689) | - | 🔵 fork 1.36× faster than `lapack-openblas` | `*` one row has no measurement here |
| `solve/n16/b1` | 0.004809 ± 1e-05 (W 9.34639e-05) | - | 0.004949 ± 3.05505e-05 (W 5.634e-05) | - | · | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 3.75654 ± 0.0410948 (W 0.0127) | - | 4.66333 ± 0.0035188 (W 0.00904766) | - | 🔵 fork 1.24× faster than `lapack-openblas` | `*` one row has no measurement here |
| `solve/n4/b1` | 0.001403 ± 4.50925e-05 (W 7.64022e-05) | - | 0.001142 ± 1e-05 (W 0.000105958) | - | 🔴 fork 1.23× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.540226 ± 0.00206461 (W 0.00439594) | - | 0.729644 ± 0.00168103 (W 0.00268963) | - | 🔵 fork 1.35× faster than `lapack-openblas` | `*` one row has no measurement here |
| `solve/n8/b1` | 0.002454 ± 7.64875e-05 (W 7.99894e-05) | - | 0.002043 ± 1.53948e-05 (W 3.7818e-05) | - | 🔴 fork 1.20× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 1.34236 ± 0.02565 (W 0.00484379) | - | 1.5921 ± 0.00396062 (W 0.00429077) | - | 🔵 fork 1.19× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_full/n16/b1` | 0.057468 ± 0.000274651 (W 0.00013058) | - | 0.091402 ± 0.000167144 (W 0.00156521) | - | 🔵 fork 1.59× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_full/n16/b1024` | 60.1757 ± 1.77632 (W 0.0346108) | - | 93.8616 ± 0.294075 (W 0.0554927) | - | 🔵 fork 1.56× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `svd_full/n4/b1` | 0.00534 ± 2.08167e-05 (W 0.000115154) | - | 0.008876 ± 0.000112829 (W 6.42651e-05) | - | 🔵 fork 1.66× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 4.98606 ± 0.0671207 (W 0.00279239) | - | 7.93169 ± 0.0570953 (W 0.0240909) | - | 🔵 fork 1.59× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_full/n8/b1` | 0.016271 ± 5.62168e-05 (W 0.000134411) | - | 0.024255 ± 0.000115902 (W 5.65447e-05) | - | 🔵 fork 1.49× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 16.6793 ± 0.0453875 (W 0.0217488) | - | 25.0011 ± 0.279361 (W 0.0276403) | - | 🔵 fork 1.50× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n16/b1` | 0.057688 ± 0.000211266 (W 0.000153095) | - | 0.091272 ± 0.000195732 (W 0.000207507) | - | 🔵 fork 1.58× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n16/b1024` | 62.5476 ± 1.51496 (W 0.0520303) | - | 93.566 ± 0.120014 (W 0.0823757) | - | 🔵 fork 1.50× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n4/b1` | 0.00531 ± 1.1547e-05 (W 9.28019e-05) | - | 0.008847 ± 1.76163e-05 (W 6.12397e-05) | - | 🔵 fork 1.67× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 4.99297 ± 0.00728594 (W 0.0138797) | - | 7.90299 ± 0.028151 (W 0.0210809) | - | 🔵 fork 1.58× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n8/b1` | 0.016241 ± 4.07063e-05 (W 7.57516e-05) | - | 0.024185 ± 0.000113271 (W 0.000166037) | - | 🔵 fork 1.49× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 16.6911 ± 0.0401503 (W 0.0323062) | - | 24.8389 ± 0.009983 (W 0.0522848) | - | 🔵 fork 1.49× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n16/b1` | 0.043732 ± 8.2282e-05 (W 9.67636e-05) | - | 0.032881 ± 0.000187981 (W 0.000130592) | - | 🔴 fork 1.33× slower than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n16/b1024` | 45.5761 ± 0.132744 (W 0.029807) | - | 33.448 ± 0.0301858 (W 0.059291) | - | 🔴 fork 1.36× slower than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n4/b1` | 0.004228 ± 4.72582e-05 (W 0.000182973) | - | 0.00546 ± 0.000105357 (W 4.70351e-05) | - | 🔵 fork 1.29× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.86712 ± 0.00886953 (W 0.00288201) | - | 4.57199 ± 0.0197434 (W 0.0311222) | - | 🔵 fork 1.18× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n8/b1` | 0.012864 ± 0.000100732 (W 3.11448e-05) | - | 0.011782 ± 8.56174e-05 (W 5.35724e-05) | - | 🔴 fork 1.09× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 12.9466 ± 0.0449743 (W 0.018054) | - | 11.2035 ± 0.0116372 (W 0.0216451) | - | 🔴 fork 1.16× slower than `lapack-openblas` | `*` one row has no measurement here |
| `triangular_solve/n16/b1` | 0.001422 ± 3.04467e-05 (W 7.09246e-05) | - | 0.001132 ± 2.3094e-05 (W 2.88097e-05) | - | 🔴 fork 1.26× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.994068 ± 0.00445552 (W 0.00367059) | - | 0.940638 ± 0.00593192 (W 0.00513485) | - | 🔴 fork 1.06× slower than `lapack-openblas` | `*` one row has no measurement here |
| `triangular_solve/n4/b1` | 0.000631 ± 9.50438e-06 (W 3.10854e-05) | - | 0.000531 ± 5.7735e-06 (W 4.47214e-06) | - | 🔴 fork 1.19× slower than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.162907 ± 0.000430272 (W 0.00159738) | - | 0.260701 ± 0.00352628 (W 0.0020232) | - | 🔵 fork 1.60× faster than `lapack-openblas` | `*` one row has no measurement here |
| `triangular_solve/n8/b1` | 0.000902 ± 4.2194e-05 (W 4.98116e-05) | - | 0.000702 ± 5.7735e-07 (W 1.14586e-05) | - | 🔴 fork 1.28× slower than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.407161 ± 0.00238255 (W 0.00257622) | - | 0.445287 ± 0.00187581 (W 0.00246002) | - | 🔵 fork 1.09× faster than `lapack-openblas` | `*` one row has no measurement here |

## batch-small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n16/b1` | 0.001582 ± 5.53203e-05 (W 2.93292e-05) | 0.001613 ± 4.04145e-05 (W 7.44983e-05) | 0.001663 ± 2e-05 (W 3.04516e-05) | · | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n16/b1024` | 1.28255 ± 0.0212652 (W 0.00592832) | 0.169608 ± 0.00178742 (W 0.00271341) | 1.56498 ± 0.028953 (W 0.00786882) | 🔴 fork 7.56× slower than `faer-pool` | 🔵 fork 1.22× faster than `lapack-openblas` |  |
| `cholesky/n4/b1` | 0.000551 ± 1.52753e-05 (W 6.50385e-05) | 0.000612 ± 3.01164e-05 (W 1.67988e-05) | 0.000421 ± 1.52753e-05 (W 8.3666e-06) | 🔵 fork 1.11× faster than `faer-pool` | 🔴 fork 1.31× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n4/b1024` | 0.195626 ± 0.000789405 (W 0.00112651) | 0.032441 ± 0.000588887 (W 0.000463436) | 0.231815 ± 0.00171194 (W 0.00150629) | 🔴 fork 6.03× slower than `faer-pool` | 🔵 fork 1.18× faster than `lapack-openblas` |  |
| `cholesky/n8/b1` | 0.000762 ± 3.72872e-05 (W 5.39843e-05) | 0.000852 ± 2.88675e-05 (W 3.70581e-05) | 0.000671 ± 1.52753e-05 (W 2.14756e-05) | 🔵 fork 1.12× faster than `faer-pool` | 🔴 fork 1.14× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `cholesky/n8/b1024` | 0.41709 ± 0.011822 (W 0.00191873) | 0.060142 ± 0.000438088 (W 0.0014889) | 0.490829 ± 0.00332931 (W 0.00277151) | 🔴 fork 6.94× slower than `faer-pool` | 🔵 fork 1.18× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eig/n16/b1` | 0.12266 ± 0.000290999 (W 0.00238269) | 0.122068 ± 0.000251064 (W 0.00028434) | 0.166904 ± 0.000746306 (W 0.00137242) | · | 🔵 fork 1.36× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 128.962 ± 0.667913 (W 0.270067) | 16.5279 ± 5.2344 (W 0.393539) | 199.567 ± 0.476232 (W 0.164436) | 🔴 fork 7.80× slower than `faer-pool` | 🔵 fork 1.55× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `eig/n4/b1` | 0.010559 ± 8.05419e-05 (W 0.000256136) | 0.010599 ± 8.69502e-05 (W 0.000137889) | 0.013605 ± 0.000119876 (W 3.68266e-05) | · | 🔵 fork 1.29× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eig/n4/b1024` | 9.95091 ± 0.109699 (W 0.0234115) | 1.29271 ± 0.00711143 (W 0.00619193) | 13.2828 ± 0.0592285 (W 0.0235129) | 🔴 fork 7.70× slower than `faer-pool` | 🔵 fork 1.33× faster than `lapack-openblas` |  |
| `eig/n8/b1` | 0.034064 ± 0.00632497 (W 0.00205668) | 0.034274 ± 0.00050843 (W 0.000164073) | 0.043662 ± 0.000312571 (W 9.2844e-05) | · | 🔵 fork 1.28× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `eig/n8/b1024` | 34.5846 ± 0.378634 (W 0.0381429) | 4.49208 ± 0.0304131 (W 0.0254697) | 46.6686 ± 0.197761 (W 0.0716094) | 🔴 fork 7.70× slower than `faer-pool` | 🔵 fork 1.35× faster than `lapack-openblas` |  |
| `eigh/n16/b1` | 0.030197 ± 9.84886e-05 (W 0.00147854) | 0.030297 ± 0.000320983 (W 0.000185011) | 0.043672 ± 0.000171553 (W 7.82943e-05) | · | 🔵 fork 1.45× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 32.1689 ± 0.0227034 (W 0.0771442) | 4.01928 ± 0.0180613 (W 0.0325505) | 45.2496 ± 0.291099 (W 0.0646415) | 🔴 fork 8.00× slower than `faer-pool` | 🔵 fork 1.41× faster than `lapack-openblas` |  |
| `eigh/n4/b1` | 0.003507 ± 5.45008e-05 (W 9.98364e-05) | 0.003537 ± 1.52753e-05 (W 6.4748e-05) | 0.003737 ± 3.05505e-05 (W 4.85613e-05) | · | 🔵 fork 1.07× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigh/n4/b1024` | 2.92439 ± 0.0188654 (W 0.00596211) | 0.375602 ± 0.0012693 (W 0.00202361) | 3.61304 ± 0.02316 (W 0.00806152) | 🔴 fork 7.79× slower than `faer-pool` | 🔵 fork 1.24× faster than `lapack-openblas` |  |
| `eigh/n8/b1` | 0.009608 ± 6.4291e-05 (W 7.92465e-05) | 0.009729 ± 0.000115544 (W 8.54412e-05) | 0.012023 ± 7.3146e-05 (W 6.28037e-05) | · | 🔵 fork 1.25× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigh/n8/b1024` | 9.09168 ± 0.0592311 (W 0.0146923) | 1.15039 ± 0.0115289 (W 0.00369247) | 12.4326 ± 0.044737 (W 0.0243244) | 🔴 fork 7.90× slower than `faer-pool` | 🔵 fork 1.37× faster than `lapack-openblas` |  |
| `eigvals/n16/b1` | 0.072365 ± 0.000292005 (W 0.00169275) | 0.072456 ± 0.000118027 (W 0.000151953) | 0.124613 ± 0.000207967 (W 0.00151944) | · | 🔵 fork 1.72× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 76.9513 ± 0.0827512 (W 0.0608251) | 9.68103 ± 0.0403026 (W 0.0155286) | 149.138 ± 0.33778 (W 0.38188) | 🔴 fork 7.95× slower than `faer-pool` | 🔵 fork 1.94× faster than `lapack-openblas` |  |
| `eigvals/n4/b1` | 0.00534 ± 2.51661e-05 (W 5.02991e-05) | 0.00534 ± 4.58258e-05 (W 7.42967e-05) | 0.0106 ± 5e-05 (W 5.06952e-05) | · | 🔵 fork 1.99× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvals/n4/b1024` | 4.77095 ± 0.0215128 (W 0.00912806) | 0.626306 ± 0.00851961 (W 0.00520066) | 10.0891 ± 0.0539397 (W 0.0264929) | 🔴 fork 7.62× slower than `faer-pool` | 🔵 fork 2.11× faster than `lapack-openblas` |  |
| `eigvals/n8/b1` | 0.019667 ± 0.000144338 (W 0.000143422) | 0.019747 ± 0.000225019 (W 0.000104203) | 0.035025 ± 0.000264275 (W 8.4618e-05) | · | 🔵 fork 1.78× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvals/n8/b1024` | 19.8606 ± 0.0823601 (W 0.0281044) | 2.52234 ± 0.0120784 (W 0.0108748) | 36.9995 ± 0.0388827 (W 0.033942) | 🔴 fork 7.87× slower than `faer-pool` | 🔵 fork 1.86× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1` | 0.022903 ± 0.000104083 (W 0.000126372) | 0.022973 ± 7.86787e-05 (W 8.76681e-05) | 0.019396 ± 2.51661e-05 (W 7.54135e-05) | · | 🔴 fork 1.18× slower than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 23.8489 ± 0.0439118 (W 0.0382137) | 3.00647 ± 0.00178528 (W 0.00773716) | 19.4229 ± 0.01601 (W 0.0244499) | 🔴 fork 7.93× slower than `faer-pool` | 🔴 fork 1.23× slower than `lapack-openblas` |  |
| `eigvalsh/n4/b1` | 0.002915 ± 1.67432e-05 (W 7.5923e-05) | 0.002956 ± 4.0501e-05 (W 0.00013205) | 0.002574 ± 1.70392e-05 (W 2.07364e-05) | · | 🔴 fork 1.13× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n4/b1024` | 2.35978 ± 0.0050901 (W 0.00175818) | 0.30946 ± 0.0011753 (W 0.00178478) | 2.1237 ± 0.0105271 (W 0.00428601) | 🔴 fork 7.63× slower than `faer-pool` | 🔴 fork 1.11× slower than `lapack-openblas` |  |
| `eigvalsh/n8/b1` | 0.007985 ± 2.64575e-05 (W 8.32466e-05) | 0.008005 ± 3.05014e-05 (W 4.96417e-05) | 0.006563 ± 1.12694e-05 (W 2.93649e-05) | · | 🔴 fork 1.22× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `eigvalsh/n8/b1024` | 7.27882 ± 0.0292922 (W 0.007587) | 0.922114 ± 0.00476374 (W 0.00183865) | 6.16108 ± 0.0142069 (W 0.0142373) | 🔴 fork 7.89× slower than `faer-pool` | 🔴 fork 1.18× slower than `lapack-openblas` |  |
| `full_piv_lu/n16/b1` | 0.005009 ± 2.6839e-05 (W 4.80135e-05) | 0.004999 ± 0.000135769 (W 6.8185e-05) | 0.021039 ± 0.000401867 (W 4.17528e-05) | · | 🔵 fork 4.20× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `full_piv_lu/n16/b1024` | 4.3963 ± 0.0365781 (W 0.0187616) | 0.612485 ± 0.0127652 (W 0.010291) | 33.3289 ± 0.123545 (W 0.0748326) | 🔴 fork 7.18× slower than `faer-pool` | 🔵 fork 7.58× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1` | 0.001102 ± 3.05014e-05 (W 7.64866e-05) | 0.001172 ± 7.63763e-05 (W 9.73874e-05) | 0.001062 ± 1.73205e-05 (W 5.21536e-05) | · | · | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n4/b1024` | 0.476572 ± 0.0111822 (W 0.00498305) | 0.091171 ± 0.00202546 (W 0.00297766) | 0.903715 ± 0.0398101 (W 0.00163057) | 🔴 fork 5.23× slower than `faer-pool` | 🔵 fork 1.90× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1` | 0.002134 ± 5.2915e-05 (W 8.43813e-05) | 0.002205 ± 9.07028e-05 (W 6.22519e-05) | 0.003807 ± 1.73205e-05 (W 3.42053e-05) | · | 🔵 fork 1.78× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `full_piv_lu/n8/b1024` | 1.24552 ± 0.049376 (W 0.00547938) | 0.193804 ± 0.00527541 (W 0.00367701) | 3.93196 ± 0.0356595 (W 0.00168319) | 🔴 fork 6.43× slower than `faer-pool` | 🔵 fork 3.16× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1` | 0.006242 ± 5.85947e-05 (W 9.82354e-05) | 0.006262 ± 8.55395e-05 (W 6.30079e-05) | 0.026078 ± 0.000525511 (W 5.74561e-05) | · | 🔵 fork 4.18× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n16/b1024` | 5.22134 ± 0.040609 (W 0.0106903) | 0.694888 ± 0.00600491 (W 0.00373255) | 37.9743 ± 0.169414 (W 0.0622172) | 🔴 fork 7.51× slower than `faer-pool` | 🔵 fork 7.27× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1` | 0.001693 ± 2.51661e-05 (W 6.4181e-05) | 0.001683 ± 3.05505e-05 (W 4.68743e-05) | 0.002405 ± 2.3388e-05 (W 2.05232e-05) | · | 🔵 fork 1.42× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n4/b1024` | 0.794135 ± 0.00489498 (W 0.00564159) | 0.116288 ± 0.00161526 (W 0.00159829) | 2.13563 ± 0.0414116 (W 0.00489581) | 🔴 fork 6.83× slower than `faer-pool` | 🔵 fork 2.69× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n8/b1` | 0.002915 ± 2.5632e-05 (W 5.70552e-05) | 0.002955 ± 3.4641e-05 (W 4.6522e-05) | 0.006172 ± 3.05505e-05 (W 2.73898e-05) | · | 🔵 fork 2.12× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `full_piv_lu_solve/n8/b1024` | 1.98219 ± 0.0328348 (W 0.0151179) | 0.2719 ± 0.00615335 (W 0.00206314) | 6.20448 ± 0.0328366 (W 0.0165965) | 🔴 fork 7.29× slower than `faer-pool` | 🔵 fork 3.13× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1` | 0.004689 ± 0.000104083 (W 7.1624e-05) | 0.004749 ± 0.000315902 (W 5.09245e-05) | 0.007684 ± 6.61085e-05 (W 5.47193e-05) | · | 🔵 fork 1.64× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n16/b1024` | 5.25564 ± 0.185077 (W 0.0187977) | 0.632306 ± 0.0120475 (W 0.0134292) | 7.0921 ± 0.102668 (W 0.0142543) | 🔴 fork 8.31× slower than `faer-pool` | 🔵 fork 1.35× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n4/b1` | 0.000621 ± 2.51661e-05 (W 4.52769e-05) | 0.000661 ± 9.50438e-06 (W 0.000137004) | 0.001402 ± 2.51064e-05 (W 5.07563e-05) | 🔵 fork 1.06× faster than `faer-pool` | 🔵 fork 2.26× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `householder_apply/n4/b1024` | 0.33736 ± 0.00280629 (W 0.00189678) | 0.050324 ± 0.000780642 (W 0.000772438) | 0.441496 ± 0.00279091 (W 0.00229269) | 🔴 fork 6.70× slower than `faer-pool` | 🔵 fork 1.31× faster than `lapack-openblas` |  |
| `householder_apply/n8/b1` | 0.001313 ± 1.58219e-05 (W 6.4096e-05) | 0.001363 ± 1.76163e-05 (W 3.60597e-05) | 0.002395 ± 0 (W 4.86755e-05) | · | 🔵 fork 1.82× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `householder_apply/n8/b1024` | 1.12408 ± 0.00840543 (W 0.00196875) | 0.157133 ± 0.00122223 (W 0.0131009) | 1.49007 ± 0.0119181 (W 0.00197354) | 🔴 fork 7.15× slower than `faer-pool` | 🔵 fork 1.33× faster than `lapack-openblas` |  |
| `householder_factor/n16/b1` | 0.004589 ± 1.78979e-05 (W 5.4848e-05) | 0.004599 ± 3.51188e-05 (W 9.2358e-05) | 0.007524 ± 4e-05 (W 7.35677e-05) | · | 🔵 fork 1.64× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `householder_factor/n16/b1024` | 4.39817 ± 0.0399946 (W 0.00448269) | 0.574064 ± 0.00554716 (W 0.00248913) | 7.34983 ± 0.0125495 (W 0.0318129) | 🔴 fork 7.66× slower than `faer-pool` | 🔵 fork 1.67× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1` | 0.000792 ± 5.7735e-06 (W 3.50314e-05) | 0.000841 ± 1.52753e-05 (W 7.98768e-05) | 0.001202 ± 6.35085e-06 (W 4.21568e-05) | 🔵 fork 1.06× faster than `faer-pool` | 🔵 fork 1.52× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `householder_factor/n4/b1024` | 0.540394 ± 0.00488939 (W 0.00200553) | 0.077184 ± 0.00287517 (W 0.00166138) | 0.926799 ± 0.00450787 (W 0.00285074) | 🔴 fork 7.00× slower than `faer-pool` | 🔵 fork 1.72× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n8/b1` | 0.001643 ± 1.52753e-05 (W 4.76256e-05) | 0.001674 ± 1.21244e-05 (W 4.49444e-05) | 0.002665 ± 5.7735e-06 (W 3.03315e-05) | · | 🔵 fork 1.62× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `householder_factor/n8/b1024` | 1.40999 ± 0.0103413 (W 0.00242455) | 0.195545 ± 0.00255132 (W 0.00171401) | 2.3808 ± 0.00398382 (W 0.0106206) | 🔴 fork 7.21× slower than `faer-pool` | 🔵 fork 1.69× faster than `lapack-openblas` |  |
| `lu/n16/b1` | 0.003637 ± 6.65833e-05 (W 6.26897e-05) | 0.003666 ± 3.00056e-05 (W 0.000117789) | 0.003797 ± 2.3094e-05 (W 4.60435e-05) | · | · | dispatch-dominated (row under 20 us) |
| `lu/n16/b1024` | 3.01362 ± 0.0320396 (W 0.00805228) | 0.440905 ± 0.00373019 (W 0.0131642) | 3.86673 ± 0.0425556 (W 0.0221837) | 🔴 fork 6.84× slower than `faer-pool` | 🔵 fork 1.28× faster than `lapack-openblas` |  |
| `lu/n4/b1` | 0.000892 ± 2.70247e-05 (W 7.98123e-05) | 0.000982 ± 4.12351e-05 (W 0.000122195) | 0.000651 ± 2.47049e-05 (W 2.21179e-05) | 🔵 fork 1.10× faster than `faer-pool` | 🔴 fork 1.37× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu/n4/b1024` | 0.356637 ± 0.00651985 (W 0.00231847) | 0.06946 ± 0.000732632 (W 0.00112484) | 0.385541 ± 0.00157273 (W 0.00250056) | 🔴 fork 5.13× slower than `faer-pool` | 🔵 fork 1.08× faster than `lapack-openblas` |  |
| `lu/n8/b1` | 0.001582 ± 1.12694e-05 (W 7.63819e-05) | 0.001603 ± 1e-05 (W 7.02225e-05) | 0.001352 ± 3.04467e-05 (W 2.64632e-05) | · | 🔴 fork 1.17× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu/n8/b1024` | 0.90307 ± 0.00881195 (W 0.00451865) | 0.147125 ± 0.00178969 (W 0.00253152) | 1.06116 ± 0.00762373 (W 0.00212729) | 🔴 fork 6.14× slower than `faer-pool` | 🔵 fork 1.18× faster than `lapack-openblas` |  |
| `lu_factor/n16/b1` | 0.002374 ± 3.56417e-05 (W 7.17635e-05) | 0.002424 ± 4.0501e-05 (W 3.96762e-05) | 0.002745 ± 2.08167e-05 (W 3.10677e-05) | · | 🔵 fork 1.16× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu_factor/n16/b1024` | 2.14292 ± 0.0597807 (W 0.00737494) | 0.301544 ± 0.00766827 (W 0.00558485) | 2.72651 ± 0.0319833 (W 0.00888554) | 🔴 fork 7.11× slower than `faer-pool` | 🔵 fork 1.27× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n4/b1` | 0.000591 ± 5.7735e-06 (W 6.63325e-05) | 0.000581 ± 3.56417e-05 (W 7.69415e-05) | 0.00036 ± 1.53948e-05 (W 2.20068e-05) | · | 🔴 fork 1.64× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n4/b1024` | 0.27251 ± 0.00178088 (W 0.00239451) | 0.068839 ± 0.00234045 (W 0.00166578) | 0.270837 ± 0.000368647 (W 0.00216866) | 🔴 fork 3.96× slower than `faer-pool` | · | `!` between-start range over 5% |
| `lu_factor/n8/b1` | 0.000962 ± 5.7735e-06 (W 5.12835e-05) | 0.000982 ± 1e-05 (W 3.42053e-05) | 0.000821 ± 3.06649e-05 (W 2.51257e-05) | · | 🔴 fork 1.17× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor/n8/b1024` | 0.675152 ± 0.0113501 (W 0.00425673) | 0.107151 ± 0.0020852 (W 0.00155275) | 0.756771 ± 0.00213018 (W 0.00246544) | 🔴 fork 6.30× slower than `faer-pool` | 🔵 fork 1.12× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1` | 0.003777 ± 9.29157e-05 (W 7.14157e-05) | 0.003938 ± 6.86319e-05 (W 7.95626e-05) | 0.004879 ± 0.000126623 (W 0.000109349) | · | 🔵 fork 1.29× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n16/b1024` | 3.41955 ± 0.06767 (W 0.00573271) | 0.455532 ± 0.00354216 (W 0.00295899) | 4.99078 ± 0.142566 (W 0.00702607) | 🔴 fork 7.51× slower than `faer-pool` | 🔵 fork 1.46× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n4/b1` | 0.000821 ± 3.09892e-05 (W 4.08693e-05) | 0.000822 ± 2.82902e-05 (W 8.38409e-05) | 0.001573 ± 9.64365e-05 (W 8.08084e-05) | · | 🔵 fork 1.92× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n4/b1024` | 0.418763 ± 0.00387196 (W 0.00143654) | 0.080099 ± 0.00222435 (W 0.00113764) | 1.40209 ± 0.182891 (W 0.00735322) | 🔴 fork 5.23× slower than `faer-pool` | 🔵 fork 3.35× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor_solve/n8/b1` | 0.001593 ± 2.51661e-05 (W 4.18712e-05) | 0.001623 ± 1.52753e-05 (W 2.65763e-05) | 0.002295 ± 5.1449e-05 (W 8.64708e-05) | · | 🔵 fork 1.44× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `lu_factor_solve/n8/b1024` | 1.1382 ± 0.0175274 (W 0.00151388) | 0.164468 ± 0.00214265 (W 0.00118029) | 2.34384 ± 0.156516 (W 0.00375657) | 🔴 fork 6.92× slower than `faer-pool` | 🔵 fork 2.06× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n16/b1` | 0.001573 ± 3.21455e-05 (W 6.46529e-05) | 0.001583 ± 1.52753e-05 (W 4.32435e-05) | 0.001823 ± 0.000161401 (W 4.10634e-05) | · | 🔵 fork 1.16× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n16/b1024` | 1.3077 ± 0.00512029 (W 0.00772134) | 0.196558 ± 0.0178738 (W 0.00209656) | 1.93476 ± 0.185277 (W 0.00711694) | 🔴 fork 6.65× slower than `faer-pool` | 🔵 fork 1.48× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n4/b1` | 0.000441 ± 2.3094e-05 (W 5.77062e-05) | 0.000481 ± 1.73205e-05 (W 8.92087e-05) | 0.001122 ± 0.000217332 (W 5.0836e-05) | 🔵 fork 1.09× faster than `faer-pool` | 🔵 fork 2.54× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n4/b1024` | 0.163437 ± 0.00103388 (W 0.00176117) | 0.044273 ± 0.000867011 (W 0.0006355) | 1.01585 ± 0.187638 (W 0.00618756) | 🔴 fork 3.69× slower than `faer-pool` | 🔵 fork 6.22× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n8/b1` | 0.000761 ± 4.12351e-05 (W 4.35695e-05) | 0.000772 ± 1.1547e-05 (W 4.83249e-05) | 0.001423 ± 2.66521e-05 (W 6.39156e-05) | · | 🔵 fork 1.87× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `lu_solve_prepared/n8/b1024` | 0.492752 ± 0.0102012 (W 0.00417469) | 0.088576 ± 0.020541 (W 0.00165405) | 1.36599 ± 0.170414 (W 0.0037816) | 🔴 fork 5.56× slower than `faer-pool` | 🔵 fork 2.77× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `qr/n16/b1` | 0.011352 ± 4.53909e-05 (W 0.000165137) | 0.011371 ± 3.84318e-05 (W 0.000101633) | 0.012724 ± 2.88675e-05 (W 7.79102e-05) | · | 🔵 fork 1.12× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `qr/n16/b1024` | 11.0654 ± 0.13429 (W 0.028289) | 1.39978 ± 0.0108503 (W 0.016178) | 12.5368 ± 0.0396322 (W 0.0278081) | 🔴 fork 7.91× slower than `faer-pool` | 🔵 fork 1.13× faster than `lapack-openblas` |  |
| `qr/n4/b1` | 0.001403 ± 3.05505e-05 (W 6.20185e-05) | 0.001442 ± 2.28108e-05 (W 0.000162636) | 0.001873 ± 1.0504e-05 (W 3.98773e-05) | · | 🔵 fork 1.33× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `qr/n4/b1024` | 0.853245 ± 0.00314809 (W 0.00133285) | 0.115125 ± 0.00156853 (W 0.00231024) | 1.39094 ± 0.0106307 (W 0.00414772) | 🔴 fork 7.41× slower than `faer-pool` | 🔵 fork 1.63× faster than `lapack-openblas` |  |
| `qr/n8/b1` | 0.003186 ± 1e-05 (W 8.70632e-05) | 0.003256 ± 3.78594e-05 (W 3.56371e-05) | 0.004288 ± 1e-05 (W 2.40832e-05) | · | 🔵 fork 1.35× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `qr/n8/b1024` | 2.60052 ± 0.022023 (W 0.00283992) | 0.338174 ± 0.00226713 (W 0.00196792) | 3.74839 ± 0.0066335 (W 0.00443684) | 🔴 fork 7.69× slower than `faer-pool` | 🔵 fork 1.44× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1` | 0.012704 ± 0.000106491 (W 0.000121772) | 0.012684 ± 0.00012108 (W 6.23402e-05) | 0.016501 ± 0.00015885 (W 7.1624e-05) | · | 🔵 fork 1.30× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n16/b1024` | 12.1884 ± 0.0963952 (W 0.0170754) | 1.56259 ± 0.0199267 (W 0.004365) | 16.7526 ± 0.130208 (W 0.0409152) | 🔴 fork 7.80× slower than `faer-pool` | 🔵 fork 1.37× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1` | 0.002054 ± 3.05505e-05 (W 8e-05) | 0.002124 ± 0.000439819 (W 3.78153e-05) | 0.002695 ± 3.84318e-05 (W 5.73603e-05) | · | 🔵 fork 1.31× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n4/b1024` | 1.36571 ± 0.0114477 (W 0.00345333) | 0.183333 ± 0.00263583 (W 0.00209025) | 1.77806 ± 0.00635818 (W 0.00620243) | 🔴 fork 7.45× slower than `faer-pool` | 🔵 fork 1.30× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1` | 0.004398 ± 5.56776e-05 (W 8.28855e-05) | 0.004389 ± 3.98372e-05 (W 2.86915e-05) | 0.005611 ± 7.13933e-05 (W 6.04343e-05) | · | 🔵 fork 1.28× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `rank_revealing_qr/n8/b1024` | 3.70716 ± 0.0308162 (W 0.00542957) | 0.487692 ± 0.0082664 (W 0.00470019) | 4.93535 ± 0.0138434 (W 0.0056574) | 🔴 fork 7.60× slower than `faer-pool` | 🔵 fork 1.33× faster than `lapack-openblas` |  |
| `solve/n16/b1` | 0.004879 ± 6.61085e-05 (W 5.1672e-05) | 0.004919 ± 4.64794e-05 (W 5.81911e-05) | 0.00543 ± 8.94446e-05 (W 0.000116727) | · | 🔵 fork 1.11× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `solve/n16/b1024` | 3.74557 ± 0.0460753 (W 0.0061815) | 0.514462 ± 0.00836397 (W 0.0139565) | 5.22596 ± 0.12507 (W 0.0183328) | 🔴 fork 7.28× slower than `faer-pool` | 🔵 fork 1.40× faster than `lapack-openblas` |  |
| `solve/n4/b1` | 0.001492 ± 6.35085e-06 (W 6.24516e-05) | 0.001523 ± 6.08276e-05 (W 0.000107471) | 0.001834 ± 3.00056e-05 (W 6.91035e-05) | · | 🔵 fork 1.23× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n4/b1024` | 0.532991 ± 0.00552444 (W 0.00514757) | 0.079048 ± 0.00204939 (W 0.00293632) | 1.51524 ± 0.0412308 (W 0.00623544) | 🔴 fork 6.74× slower than `faer-pool` | 🔵 fork 2.84× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1` | 0.002465 ± 2.58908e-05 (W 7.187e-05) | 0.002575 ± 8.5049e-05 (W 5.1672e-05) | 0.002735 ± 9.76746e-05 (W 0.000101673) | · | 🔵 fork 1.11× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n8/b1024` | 1.34384 ± 0.00439563 (W 0.0104291) | 0.190015 ± 0.00249535 (W 0.00363859) | 2.32777 ± 0.027809 (W 0.00658139) | 🔴 fork 7.07× slower than `faer-pool` | 🔵 fork 1.73× faster than `lapack-openblas` |  |
| `svd_full/n16/b1` | 0.058048 ± 0.000421328 (W 0.000155766) | 0.058309 ± 0.000328649 (W 0.000240772) | 0.091992 ± 0.000320468 (W 0.000148257) | · | 🔵 fork 1.58× faster than `lapack-openblas` |  |
| `svd_full/n16/b1024` | 60.5777 ± 0.387193 (W 0.0472774) | 7.82092 ± 0.0585121 (W 0.0993627) | 93.9377 ± 0.128437 (W 0.222517) | 🔴 fork 7.75× slower than `faer-pool` | 🔵 fork 1.55× faster than `lapack-openblas` |  |
| `svd_full/n4/b1` | 0.00529 ± 2.3388e-05 (W 0.000115888) | 0.00536 ± 1.1547e-05 (W 4.97996e-05) | 0.008837 ± 8.67583e-05 (W 4.80344e-05) | · | 🔵 fork 1.67× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_full/n4/b1024` | 4.99244 ± 0.01827 (W 0.0126275) | 0.643795 ± 0.00438859 (W 0.00745316) | 7.94719 ± 0.0443854 (W 0.012542) | 🔴 fork 7.75× slower than `faer-pool` | 🔵 fork 1.59× faster than `lapack-openblas` |  |
| `svd_full/n8/b1` | 0.01633 ± 9.30609e-05 (W 8.38344e-05) | 0.016271 ± 8.41843e-05 (W 0.00156666) | 0.024416 ± 0.000100664 (W 6.27001e-05) | · | 🔵 fork 1.50× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_full/n8/b1024` | 16.8486 ± 0.277885 (W 0.0249979) | 2.13342 ± 0.0822549 (W 0.00998215) | 24.9495 ± 0.0348087 (W 0.0313985) | 🔴 fork 7.90× slower than `faer-pool` | 🔵 fork 1.48× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n16/b1` | 0.057989 ± 0.000160935 (W 0.000268428) | 0.058048 ± 0.000321352 (W 0.000171214) | 0.091782 ± 0.000405468 (W 0.000212429) | · | 🔵 fork 1.58× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 60.5399 ± 1.25995 (W 0.0467284) | 7.70645 ± 0.0985018 (W 0.0446333) | 93.9383 ± 0.196047 (W 0.261859) | 🔴 fork 7.86× slower than `faer-pool` | 🔵 fork 1.55× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1` | 0.00528 ± 2.64575e-05 (W 6.9282e-05) | 0.00533 ± 2.08167e-05 (W 8.36313e-05) | 0.008896 ± 0.00298572 (W 7.50886e-05) | · | 🔵 fork 1.68× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `svd_thin/n4/b1024` | 5.01404 ± 0.0122789 (W 0.0483258) | 0.642682 ± 0.0103306 (W 0.00299394) | 7.90187 ± 0.119902 (W 0.0120312) | 🔴 fork 7.80× slower than `faer-pool` | 🔵 fork 1.58× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1` | 0.016381 ± 0.000146186 (W 0.000141419) | 0.01643 ± 0.000105532 (W 9.92179e-05) | 0.024235 ± 6.71342e-05 (W 5.56435e-05) | · | 🔵 fork 1.48× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_thin/n8/b1024` | 16.7673 ± 0.0647042 (W 0.025755) | 2.17823 ± 0.0287367 (W 0.0519402) | 24.9238 ± 0.0185997 (W 0.042049) | 🔴 fork 7.70× slower than `faer-pool` | 🔵 fork 1.49× faster than `lapack-openblas` |  |
| `svd_values/n16/b1` | 0.043702 ± 6.86319e-05 (W 0.000159293) | 0.043722 ± 0.000310054 (W 0.000146316) | 0.032861 ± 7.78481e-05 (W 5.43351e-05) | · | 🔴 fork 1.33× slower than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 45.4515 ± 0.128707 (W 0.0584954) | 5.90182 ± 0.00146738 (W 0.0187778) | 33.4382 ± 0.0558274 (W 0.0332196) | 🔴 fork 7.70× slower than `faer-pool` | 🔴 fork 1.36× slower than `lapack-openblas` |  |
| `svd_values/n4/b1` | 0.004268 ± 2.51661e-05 (W 0.000155007) | 0.004298 ± 4e-05 (W 0.000182975) | 0.0055 ± 2.64575e-05 (W 6.10737e-05) | · | 🔵 fork 1.29× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_values/n4/b1024` | 3.86747 ± 0.00990432 (W 0.00531607) | 0.498555 ± 0.314078 (W 0.00301395) | 4.55431 ± 0.0149874 (W 0.00937575) | 🔴 fork 7.76× slower than `faer-pool` | 🔵 fork 1.18× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_values/n8/b1` | 0.012834 ± 9.0185e-05 (W 7.15542e-05) | 0.012864 ± 8e-05 (W 3.93472e-05) | 0.011812 ± 7.62911e-05 (W 7.58169e-05) | · | 🔴 fork 1.09× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `svd_values/n8/b1024` | 13.009 ± 0.0506751 (W 0.0177554) | 1.64549 ± 0.00586632 (W 0.00452653) | 11.2019 ± 0.0217713 (W 0.0193726) | 🔴 fork 7.91× slower than `faer-pool` | 🔴 fork 1.16× slower than `lapack-openblas` |  |
| `triangular_solve/n16/b1` | 0.001443 ± 1.0504e-05 (W 6.1887e-05) | 0.001422 ± 2.36714e-05 (W 2.99383e-05) | 0.001573 ± 6.02771e-05 (W 7.4162e-05) | · | 🔵 fork 1.09× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n16/b1024` | 0.998638 ± 0.0160668 (W 0.0083805) | 0.13899 ± 0.00129938 (W 0.00520092) | 1.35752 ± 0.0193281 (W 0.00630574) | 🔴 fork 7.18× slower than `faer-pool` | 🔵 fork 1.36× faster than `lapack-openblas` |  |
| `triangular_solve/n4/b1` | 0.000651 ± 4e-05 (W 6.0747e-05) | 0.000662 ± 1.53948e-05 (W 9.138e-05) | 0.001062 ± 2.51661e-05 (W 5.33854e-05) | · | 🔵 fork 1.63× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n4/b1024` | 0.163876 ± 0.00126583 (W 0.0017693) | 0.027992 ± 0.000111132 (W 0.000293592) | 0.715759 ± 0.007295 (W 0.00374626) | 🔴 fork 5.85× slower than `faer-pool` | 🔵 fork 4.37× faster than `lapack-openblas` |  |
| `triangular_solve/n8/b1` | 0.000902 ± 2.5697e-05 (W 6.34823e-05) | 0.000882 ± 1e-05 (W 2.82542e-05) | 0.001293 ± 3.19427e-05 (W 6.56909e-05) | · | 🔵 fork 1.43× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.405689 ± 0.00259928 (W 0.00223169) | 0.066565 ± 0.00407204 (W 0.00154551) | 1.03364 ± 0.0715906 (W 0.00306106) | 🔴 fork 6.09× slower than `faer-pool` | 🔵 fork 2.55× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |

Not applicable to this population's shapes and reported as skipped: `cholesky/16`, `cholesky/4`, `cholesky/8`, `eig/16`, `eig/4`, `eig/8`, `eigh/16`, `eigh/4`, `eigh/8`, `eigvals/16`, `eigvals/4`, `eigvals/8`, `eigvalsh/16`, `eigvalsh/4`, `eigvalsh/8`, `full_piv_lu/16`, `full_piv_lu/4`, `full_piv_lu/8`, `full_piv_lu_solve/16`, `full_piv_lu_solve/4`, `full_piv_lu_solve/8`, `householder_apply/16`, `householder_apply/4`, `householder_apply/8`, `householder_factor/16`, `householder_factor/4`, `householder_factor/8`, `lu/16`, `lu/4`, `lu/8`, `lu_factor/16`, `lu_factor/4`, `lu_factor/8`, `lu_factor_solve/16`, `lu_factor_solve/4`, `lu_factor_solve/8`, `lu_solve_prepared/16`, `lu_solve_prepared/4`, `lu_solve_prepared/8`, `qr/16`, `qr/4`, `qr/8`, `rank_revealing_qr/16`, `rank_revealing_qr/4`, `rank_revealing_qr/8`, `solve/16`, `solve/4`, `solve/8`, `svd_full/16`, `svd_full/4`, `svd_full/8`, `svd_thin/16`, `svd_thin/4`, `svd_thin/8`, `svd_values/16`, `svd_values/4`, `svd_values/8`, `triangular_solve/16`, `triangular_solve/4`, `triangular_solve/8`.

## canary-factor, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.063619 ± 0.00256702 (W 0.000150862) | - | 0.070562 ± 0.000497591 (W 0.00016809) | - | 🔵 fork 1.11× faster than `lapack-openblas` | `*` one row has no measurement here; `!` between-start range over 5% |
| `lu/n128/b1` | 0.148478 ± 0.00119845 (W 0.00147126) | - | 0.146896 ± 0.000566146 (W 0.000589569) | - | · | `*` one row has no measurement here |
| `lu_factor/n128/b1` | 0.093155 ± 0.000789121 (W 0.00142421) | - | 0.130064 ± 0.000349896 (W 0.00145347) | - | 🔵 fork 1.40× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor_solve/n128/b1` | 0.103775 ± 0.000130847 (W 0.00137156) | - | 0.150832 ± 0.000507425 (W 0.00134456) | - | 🔵 fork 1.45× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n128/b1` | 0.009939 ± 5.1316e-05 (W 0.000113266) | - | 0.020128 ± 5.32948e-05 (W 8.91415e-05) | - | 🔵 fork 2.03× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.112751 ± 0.00050518 (W 0.0017674) | - | 0.157855 ± 0.00110581 (W 0.000372289) | - | 🔵 fork 1.40× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n128/b1` | 2.3396 ± 0.000594007 (W 0.00289307) | - | 1.34803 ± 0.0050842 (W 0.00280643) | - | 🔴 fork 1.74× slower than `lapack-openblas` | `*` one row has no measurement here |
| `triangular_solve/n128/b1` | 0.006883 ± 0 (W 4.91935e-05) | - | 0.010109 ± 7.76745e-05 (W 2.21856e-05) | - | 🔵 fork 1.47× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |

## canary-factor, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.063058 ± 0.00223989 (W 0.00015687) | 0.062928 ± 0.00231828 (W 0.00149785) | 0.072465 ± 0.000574627 (W 0.00063767) | · | 🔵 fork 1.15× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n128/b1` | 0.147486 ± 0.000828616 (W 0.00182774) | 0.18762 ± 0.00215088 (W 0.00464153) | 0.144631 ± 0.000579271 (W 0.00192995) | 🔵 fork 1.27× faster than `faer-pool` | · |  |
| `lu_factor/n128/b1` | 0.094377 ± 0.000449638 (W 0.00026184) | 0.126757 ± 0.00186004 (W 0.00468903) | 0.129984 ± 0.000130539 (W 0.00160349) | 🔵 fork 1.34× faster than `faer-pool` | 🔵 fork 1.38× faster than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.104415 ± 0.00116006 (W 0.00157834) | 0.137978 ± 0.000513421 (W 0.00562799) | 0.145652 ± 0.000436258 (W 0.00127398) | 🔵 fork 1.32× faster than `faer-pool` | 🔵 fork 1.39× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.009938 ± 5.13842e-05 (W 6.97223e-05) | 0.009918 ± 0.000157513 (W 0.000126215) | 0.012003 ± 0.000102031 (W 8.97118e-05) | · | 🔵 fork 1.21× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.11209 ± 0.000419262 (W 0.0018466) | 0.148709 ± 0.00414313 (W 0.00619707) | 0.152756 ± 0.00080748 (W 0.00197234) | 🔵 fork 1.33× faster than `faer-pool` | 🔵 fork 1.36× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_values/n128/b1` | 2.35541 ± 0.00356422 (W 0.00318993) | 2.38521 ± 0.00565588 (W 0.00232419) | 1.36975 ± 0.00349425 (W 0.00260395) | · | 🔴 fork 1.72× slower than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.006852 ± 2.85832e-05 (W 9.04942e-05) | 0.006772 ± 7.56329e-05 (W 8.67139e-05) | 0.006862 ± 0.00012766 (W 0.000211116) | · | · | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.18139 ± 0.000193521 (W 0.00178687) | - | 0.180368 ± 0.000962887 (W 0.00176546) | - | · | `*` one row has no measurement here |
| `lu/n128/b1` | 0.338864 ± 0.00689216 (W 0.0022277) | - | 0.354171 ± 0.00338163 (W 0.00263307) | - | · | `*` one row has no measurement here |
| `lu_factor/n128/b1` | 0.268163 ± 0.0013105 (W 0.00156873) | - | 0.31989 ± 0.000335756 (W 0.0025724) | - | 🔵 fork 1.19× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_factor_solve/n128/b1` | 0.299371 ± 0.0012004 (W 0.00195464) | - | 0.363782 ± 0.00104225 (W 0.00190901) | - | 🔵 fork 1.22× faster than `lapack-openblas` | `*` one row has no measurement here |
| `lu_solve_prepared/n128/b1` | 0.031349 ± 0.000195021 (W 0.000124001) | - | 0.044553 ± 0.000581619 (W 0.000374397) | - | 🔵 fork 1.42× faster than `lapack-openblas` | `*` one row has no measurement here |
| `solve/n128/b1` | 0.316802 ± 0.00141365 (W 0.0016605) | - | 0.377996 ± 0.000852256 (W 0.00267869) | - | 🔵 fork 1.19× faster than `lapack-openblas` | `*` one row has no measurement here |
| `svd_values/n128/b1` | 3.13281 ± 0.0104917 (W 0.00580049) | - | 2.35112 ± 0.00512426 (W 0.00471353) | - | 🔴 fork 1.33× slower than `lapack-openblas` | `*` one row has no measurement here |
| `triangular_solve/n128/b1` | 0.018735 ± 4.58258e-05 (W 0.000139238) | - | 0.024326 ± 0.000123843 (W 0.000127032) | - | 🔵 fork 1.30× faster than `lapack-openblas` | `*` one row has no measurement here; dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `cholesky/n128/b1` | 0.181369 ± 0.00063753 (W 0.00181966) | 0.187862 ± 0.00110252 (W 0.00186753) | 0.161282 ± 0.00140235 (W 0.00223759) | · | 🔴 fork 1.12× slower than `lapack-openblas` |  |
| `lu/n128/b1` | 0.339605 ± 0.0044195 (W 0.00270381) | 0.351659 ± 0.000721579 (W 0.00402073) | 0.238216 ± 0.00225435 (W 0.00243123) | · | 🔴 fork 1.43× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.269835 ± 0.00111752 (W 0.00162031) | 0.272049 ± 0.00436766 (W 0.00440725) | 0.189364 ± 0.000363842 (W 0.00249409) | · | 🔴 fork 1.42× slower than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.300913 ± 0.000820356 (W 0.00216167) | 0.301636 ± 0.0032915 (W 0.00430679) | 0.221686 ± 0.000726118 (W 0.00278895) | · | 🔴 fork 1.36× slower than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.031309 ± 0.000361594 (W 0.000109404) | 0.031299 ± 0.000195065 (W 0.000129438) | 0.029375 ± 9.16515e-05 (W 0.000337304) | · | 🔴 fork 1.07× slower than `lapack-openblas` |  |
| `solve/n128/b1` | 0.315241 ± 0.000595003 (W 0.00137134) | 0.328795 ± 0.00245577 (W 0.00477459) | 0.245158 ± 0.000894336 (W 0.00230652) | · | 🔴 fork 1.29× slower than `lapack-openblas` |  |
| `svd_values/n128/b1` | 3.12515 ± 0.00808898 (W 0.0057465) | 3.15394 ± 0.00475595 (W 0.00478782) | 2.59531 ± 0.0134334 (W 0.00532928) | · | 🔴 fork 1.20× slower than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.018625 ± 6.65833e-05 (W 0.000108858) | 0.018534 ± 5.27289e-05 (W 0.000136802) | 0.015799 ± 0.000147422 (W 0.000189085) | · | 🔴 fork 1.18× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |

Not applicable to this population's shapes and reported as skipped: `cholesky/128`, `lu/128`, `lu_factor/128`, `lu_factor_solve/128`, `lu_solve_prepared/128`, `solve/128`, `svd_values/128`, `triangular_solve/128`.

## canary-decompose, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 47.828 ± 0.234971 (W 0.0866652) | - | 50.7265 ± 0.491723 (W 0.0832066) | - | 🔵 fork 1.06× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n512/b1` | 23.6756 ± 0.306496 (W 0.0300948) | - | 23.8683 ± 0.249833 (W 0.0290518) | - | · | `*` one row has no measurement here |
| `householder_apply/n512/b1` | 10.0335 ± 0.0877437 (W 0.0223487) | - | 19.5865 ± 0.0187284 (W 0.0295144) | - | 🔵 fork 1.95× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_factor/n512/b1` | 7.0916 ± 0.0158886 (W 0.0213153) | - | 12.2916 ± 0.0206716 (W 0.0327505) | - | 🔵 fork 1.73× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n512/b1` | 19.2821 ± 0.0367799 (W 0.03513) | - | 24.6705 ± 0.153814 (W 0.043073) | - | 🔵 fork 1.28× faster than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/n512/b1` | 29.9284 ± 0.0359692 (W 0.0528652) | - | 31.4379 ± 0.21363 (W 0.107668) | - | · | `*` one row has no measurement here |
| `svd_thin/n512/b1` | 117.916 ± 0.224388 (W 0.398933) | - | 119.976 ± 0.231835 (W 0.176136) | - | · | `*` one row has no measurement here |

## canary-decompose, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 47.6298 ± 0.173981 (W 0.0674456) | 23.5402 ± 0.0339707 (W 0.149626) | 23.3318 ± 0.150669 (W 0.0207807) | 🔴 fork 2.02× slower than `faer-pool` | 🔴 fork 2.04× slower than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 23.7604 ± 0.24356 (W 0.0524791) | 18.6931 ± 0.0278951 (W 0.0428654) | 11.1718 ± 0.0580455 (W 0.00920193) | 🔴 fork 1.27× slower than `faer-pool` | 🔴 fork 2.13× slower than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 10.31 ± 0.0391763 (W 0.0320961) | 2.87019 ± 0.0149369 (W 0.0828321) | 9.86795 ± 0.0419587 (W 0.0144552) | 🔴 fork 3.59× slower than `faer-pool` | · |  |
| `householder_factor/n512/b1` | 7.28652 ± 0.011769 (W 0.00931505) | 2.72367 ± 0.0134948 (W 0.0360611) | 6.72958 ± 0.0348624 (W 0.00714965) | 🔴 fork 2.68× slower than `faer-pool` | 🔴 fork 1.08× slower than `lapack-openblas` |  |
| `qr/n512/b1` | 19.3425 ± 0.123941 (W 0.0340624) | 7.66891 ± 0.0655733 (W 0.128925) | 13.3907 ± 0.0776781 (W 0.0274234) | 🔴 fork 2.52× slower than `faer-pool` | 🔴 fork 1.44× slower than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 25.007 ± 0.0331205 (W 0.0382419) | 9.65873 ± 0.0132122 (W 0.0919515) | 23.124 ± 0.173501 (W 0.0176216) | 🔴 fork 2.59× slower than `faer-pool` | 🔴 fork 1.08× slower than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 118.579 ± 0.522996 (W 0.411863) | 60.7888 ± 0.213729 (W 0.429017) | 85.8803 ± 0.300585 (W 0.0810616) | 🔴 fork 1.95× slower than `faer-pool` | 🔴 fork 1.38× slower than `lapack-openblas` |  |

## canary-decompose, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 104.541 ± 0.0791736 (W 0.0802996) | - | 260.418 ± 0.92907 (W 0.308514) | - | 🔵 fork 2.49× faster than `lapack-openblas` | `*` one row has no measurement here |
| `eigvalsh/n512/b1` | 49.3241 ± 0.13116 (W 0.111839) | - | 62.2933 ± 0.186254 (W 0.0350592) | - | 🔵 fork 1.26× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_apply/n512/b1` | 41.0771 ± 0.166887 (W 0.124156) | - | 53.3701 ± 0.0926324 (W 0.100396) | - | 🔵 fork 1.30× faster than `lapack-openblas` | `*` one row has no measurement here |
| `householder_factor/n512/b1` | 27.7068 ± 0.0271889 (W 0.0375898) | - | 34.6176 ± 0.0366649 (W 0.0538718) | - | 🔵 fork 1.25× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/n512/b1` | 70.1255 ± 0.0437216 (W 0.0727083) | - | 69.3833 ± 0.0832468 (W 0.0708465) | - | · | `*` one row has no measurement here |
| `rank_revealing_qr/n512/b1` | 79.344 ± 0.31668 (W 0.07093) | - | 75.0219 ± 0.676855 (W 0.531316) | - | 🔴 fork 1.06× slower than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/n512/b1` | 261.55 ± 0.618428 (W 0.405327) | - | 239.517 ± 1.33901 (W 0.360089) | - | 🔴 fork 1.09× slower than `lapack-openblas` | `*` one row has no measurement here |

## canary-decompose, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `eigh/n512/b1` | 104.687 ± 0.142411 (W 0.118549) | 38.7609 ± 0.087123 (W 0.501456) | 204.822 ± 0.895348 (W 0.719852) | 🔴 fork 2.70× slower than `faer-pool` | 🔵 fork 1.96× faster than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 49.3068 ± 0.0425787 (W 0.0470223) | 28.92 ± 0.0596398 (W 0.0512633) | 29.821 ± 0.0947103 (W 0.012858) | 🔴 fork 1.70× slower than `faer-pool` | 🔴 fork 1.65× slower than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 41.1234 ± 0.0319493 (W 0.0225346) | 7.19293 ± 0.1006 (W 0.0836741) | 14.7945 ± 0.069656 (W 0.0218778) | 🔴 fork 5.72× slower than `faer-pool` | 🔴 fork 2.78× slower than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 27.772 ± 0.0291465 (W 0.0488266) | 6.88396 ± 0.0251773 (W 0.0680379) | 10.8116 ± 0.108215 (W 0.013708) | 🔴 fork 4.03× slower than `faer-pool` | 🔴 fork 2.57× slower than `lapack-openblas` |  |
| `qr/n512/b1` | 70.2609 ± 0.0607409 (W 0.0706669) | 17.0172 ± 3.67023 (W 0.265633) | 21.7305 ± 0.219409 (W 0.0271645) | 🔴 fork 4.13× slower than `faer-pool` | 🔴 fork 3.23× slower than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `rank_revealing_qr/n512/b1` | 82.5702 ± 0.115366 (W 0.0755381) | 19.636 ± 0.0663674 (W 0.14689) | 24.6155 ± 0.231367 (W 0.0420835) | 🔴 fork 4.21× slower than `faer-pool` | 🔴 fork 3.35× slower than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 262.186 ± 0.356577 (W 0.62309) | 100.269 ± 0.539265 (W 0.535711) | 98.4917 ± 0.0264093 (W 0.0990761) | 🔴 fork 2.61× slower than `faer-pool` | 🔴 fork 2.66× slower than `lapack-openblas` |  |

Not applicable to this population's shapes and reported as skipped: `eigh/512`, `eigvalsh/512`, `householder_apply/512`, `householder_factor/512`, `qr/512`, `rank_revealing_qr/512`, `svd_thin/512`.

## canary-rectangular, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 23.44 ± 0.150902 (W 0.0248062) | - | 38.505 ± 0.0876527 (W 0.0345954) | - | 🔵 fork 1.64× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/4096x256/b1` | 66.4763 ± 0.0910696 (W 0.0904495) | - | 77.1859 ± 0.323456 (W 0.10945) | - | 🔵 fork 1.16× faster than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/4096x256/b1` | 101.103 ± 0.86483 (W 0.455459) | - | 90.8037 ± 1.44787 (W 0.183706) | - | 🔴 fork 1.11× slower than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/4096x256/b1` | 103.35 ± 0.0553559 (W 0.227629) | - | 122.937 ± 0.394509 (W 0.375928) | - | 🔵 fork 1.19× faster than `lapack-openblas` | `*` one row has no measurement here |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 23.3713 ± 0.255658 (W 0.0322858) | 7.9058 ± 0.0314836 (W 0.027516) | 18.0137 ± 0.17325 (W 0.0281808) | 🔴 fork 2.96× slower than `faer-pool` | 🔴 fork 1.30× slower than `lapack-openblas` |  |
| `qr/4096x256/b1` | 67.0024 ± 0.252324 (W 0.0769315) | 22.6622 ± 0.275092 (W 0.501101) | 36.1587 ± 0.161193 (W 0.0302045) | 🔴 fork 2.96× slower than `faer-pool` | 🔴 fork 1.85× slower than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 103.165 ± 0.617619 (W 0.160501) | 24.9349 ± 0.3611 (W 0.546248) | 39.158 ± 0.379282 (W 0.0442804) | 🔴 fork 4.14× slower than `faer-pool` | 🔴 fork 2.63× slower than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 102.811 ± 0.318482 (W 0.100616) | 39.9353 ± 0.103927 (W 0.321271) | 60.9806 ± 0.408847 (W 0.0531556) | 🔴 fork 2.57× slower than `faer-pool` | 🔴 fork 1.69× slower than `lapack-openblas` |  |

## canary-rectangular, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 86.4247 ± 0.0507835 (W 0.0924196) | - | 109.016 ± 0.307489 (W 0.168525) | - | 🔵 fork 1.26× faster than `lapack-openblas` | `*` one row has no measurement here |
| `qr/4096x256/b1` | 237.103 ± 0.196468 (W 0.49293) | - | 218.376 ± 0.904126 (W 0.37253) | - | 🔴 fork 1.09× slower than `lapack-openblas` | `*` one row has no measurement here |
| `rank_revealing_qr/4096x256/b1` | 349.541 ± 0.436689 (W 1.21417) | - | 251.752 ± 0.522706 (W 0.423054) | - | 🔴 fork 1.39× slower than `lapack-openblas` | `*` one row has no measurement here |
| `svd_thin/4096x256/b1` | 366.493 ± 0.364244 (W 0.486262) | - | 350.237 ± 1.41646 (W 0.859719) | - | · | `*` one row has no measurement here |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) | vs `faer-pool` | vs `lapack-openblas` | notes |
|---|---|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 86.1412 ± 0.468087 (W 0.345921) | 19.8929 ± 0.12022 (W 0.0738401) | 20.1863 ± 0.0795977 (W 0.0194658) | 🔴 fork 4.33× slower than `faer-pool` | 🔴 fork 4.27× slower than `lapack-openblas` |  |
| `qr/4096x256/b1` | 237.213 ± 0.25473 (W 0.467648) | 53.6596 ± 0.105565 (W 0.0760328) | 40.4281 ± 0.141025 (W 0.0669049) | 🔴 fork 4.42× slower than `faer-pool` | 🔴 fork 5.87× slower than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 345.498 ± 0.174716 (W 3.01464) | 60.4898 ± 0.219646 (W 0.241163) | 51.3347 ± 0.12247 (W 0.442972) | 🔴 fork 5.71× slower than `faer-pool` | 🔴 fork 6.73× slower than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 366.671 ± 0.152016 (W 0.572064) | 111.479 ± 2.06843 (W 0.240652) | 86.9024 ± 0.461562 (W 0.261611) | 🔴 fork 3.29× slower than `faer-pool` | 🔴 fork 4.22× slower than `lapack-openblas` |  |

Not applicable to this population's shapes and reported as skipped: `householder_factor/4096x256`, `qr/4096x256`, `rank_revealing_qr/4096x256`, `svd_thin/4096x256`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
