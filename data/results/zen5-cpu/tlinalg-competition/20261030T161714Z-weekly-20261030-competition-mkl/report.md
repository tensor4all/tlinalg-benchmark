# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `3957b5af620eff5da5d1435afd97a4a8619ba473`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `f9de3c2ea11208f98dfddae328c2a2b5c15bdc311582ad4269a4c6dda4ca4673`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-30T16:37:24.149649Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor mkl --aa 4 --reps 5 --prime-ms 250 --label weekly-20261030-competition-mkl --no-publish`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261030T161714Z-weekly-20261030-competition-mkl/`

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
  - `lapack-mkl` — The same provider against Intel oneAPI MKL, linked from the installation `MKLROOT` names. One binary links one vendor library, so this row is measured by its own build of the harness and recorded as its own run; no page carries two vendor arms. The interface and threading layers are pinned by the harness before the first MKL call, because MKL otherwise lets the environment choose them and the interface layer is an ABI.
    Identity: the MKL build recorded in this run's manifest (`providers[mkl]`)
    Caveat: MKL reports no dispatched-kernel name and no processor count, so its manifest records neither rather than inferring them. Its threading is vendor-owned, as for OpenBLAS.
    As measured: linked shared; mkl 2026.2; kernel not reported by the vendor; openmp threading; config `Intel(R) oneAPI Math Kernel Library Version 2026.2-Product Build 20260915 for Intel(R) 64 architecture applications`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.34%, worst 26.27% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 27 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.34%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.121199 ± 0.00174899 (W 0.00154561) | 1.06421 ± 0.00719719 (W 0.00237799) | 🔵 tlinalg-pool 8.78× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.482897 ± 0.00431932 (W 0.00490516) | 3.79101 ± 0.0186931 (W 0.0150452) | 🔵 tlinalg-pool 7.85× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.182358 ± 0.000684605 (W 0.00134254) | 0.12674 ± 0.00125766 (W 0.00166521) | 🔴 tlinalg-pool 1.44× slower than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.0481345 ± 0.000755823 (W 0.000523779) | 0.325976 ± 0.00231066 (W 0.00198633) | 🔵 tlinalg-pool 6.77× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 12.075 ± 0.0433901 (W 0.0172831) | 53.002 ± 0.254248 (W 0.067077) | 🔵 tlinalg-pool 4.39× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 54.1109 ± 0.173709 (W 0.0523347) | 285.69 ± 0.985659 (W 0.403854) | 🔵 tlinalg-pool 5.28× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 0.828404 ± 0.00301859 (W 0.00193265) | 2.86063 ± 0.0165935 (W 0.00835143) | 🔵 tlinalg-pool 3.45× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 3.03778 ± 0.0210118 (W 0.00785056) | 11.8083 ± 0.0447059 (W 0.0102441) | 🔵 tlinalg-pool 3.89× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 3.75939 ± 0.0239316 (W 0.00596881) | 23.8827 ± 0.0765257 (W 0.0277546) | 🔵 tlinalg-pool 6.35× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 13.9982 ± 0.0703265 (W 0.0231773) | 98.0588 ± 0.332748 (W 0.33707) | 🔵 tlinalg-pool 7.01× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.327715 ± 0.00146646 (W 0.00232564) | 2.98028 ± 0.00514927 (W 0.00417698) | 🔵 tlinalg-pool 9.09× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.09616 ± 0.00219056 (W 0.00139975) | 7.91865 ± 0.0153485 (W 0.0124259) | 🔵 tlinalg-pool 7.22× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 8.36686 ± 0.0313009 (W 0.00888022) | 36.7827 ± 0.159144 (W 0.070631) | 🔵 tlinalg-pool 4.40× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 36.7305 ± 0.716805 (W 0.0705033) | 172.527 ± 0.612264 (W 0.354662) | 🔵 tlinalg-pool 4.70× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.446827 ± 0.00666266 (W 0.00442137) | 2.10971 ± 0.00982219 (W 0.00261757) | 🔵 tlinalg-pool 4.72× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 2.01829 ± 0.006753 (W 0.00323126) | 9.06316 ± 0.0523604 (W 0.00884667) | 🔵 tlinalg-pool 4.49× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 2.8292 ± 0.00899483 (W 0.00751677) | 12.7837 ± 0.0525697 (W 0.0393526) | 🔵 tlinalg-pool 4.52× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 10.692 ± 0.0371518 (W 0.00921582) | 41.5784 ± 0.16806 (W 0.030301) | 🔵 tlinalg-pool 3.89× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.257923 ± 0.000793922 (W 0.00197125) | 1.55883 ± 0.00829841 (W 0.00360704) | 🔵 tlinalg-pool 6.04× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.866815 ± 0.00215625 (W 0.00201384) | 4.48599 ± 0.0232504 (W 0.00548403) | 🔵 tlinalg-pool 5.18× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.511154 ± 0.00279754 (W 0.00334896) | 3.91015 ± 0.0270434 (W 0.0109809) | 🔵 tlinalg-pool 7.65× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 2.03745 ± 0.0144398 (W 0.0149277) | 26.2642 ± 0.0386183 (W 0.0260434) | 🔵 tlinalg-pool 12.89× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.50553 ± 0.0300754 (W 0.00326259) | 0.40706 ± 0.00603935 (W 0.00241637) | 🔴 tlinalg-pool 1.24× slower than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.175546 ± 0.00404613 (W 0.00261952) | 1.00573 ± 0.00633445 (W 0.00308498) | 🔵 tlinalg-pool 5.73× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.498707 ± 0.0229275 (W 0.00402033) | 5.70341 ± 0.0298583 (W 0.014738) | 🔵 tlinalg-pool 11.44× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n32/b1024` | 1.59456 ± 0.0124146 (W 0.0110538) | 29.4156 ± 0.0652813 (W 0.0410565) | 🔵 tlinalg-pool 18.45× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.0822425 ± 0.00109889 (W 0.00326789) | 1.00225 ± 0.0059902 (W 0.00319604) | 🔵 tlinalg-pool 12.19× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.197472 ± 0.00153478 (W 0.0027961) | 1.87455 ± 0.0175999 (W 0.00673983) | 🔵 tlinalg-pool 9.49× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.599957 ± 0.0106579 (W 0.0028195) | 2.68325 ± 0.0181666 (W 0.0187209) | 🔵 tlinalg-pool 4.47× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 2.42283 ± 0.0572444 (W 0.00780444) | 13.394 ± 0.0948655 (W 0.0566337) | 🔵 tlinalg-pool 5.53× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.052548 ± 0.0014756 (W 0.00116168) | 0.319627 ± 0.000804957 (W 0.00173367) | 🔵 tlinalg-pool 6.08× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.160873 ± 0.00183452 (W 0.00185599) | 0.783983 ± 0.00960682 (W 0.00700915) | 🔵 tlinalg-pool 4.87× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1024` | 0.500277 ± 0.0118081 (W 0.00243743) | 2.96792 ± 0.0152107 (W 0.00471189) | 🔵 tlinalg-pool 5.93× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 1.67181 ± 0.0263829 (W 0.00645296) | 12.0716 ± 0.0576824 (W 0.0223334) | 🔵 tlinalg-pool 7.22× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.0642745 ± 0.00019312 (W 0.000864487) | 0.337808 ± 0.00142686 (W 0.00296748) | 🔵 tlinalg-pool 5.26× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.168002 ± 0.00250428 (W 0.00186648) | 0.867275 ± 0.00142352 (W 0.00205837) | 🔵 tlinalg-pool 5.16× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.377 ± 0.0128391 (W 0.00333141) | 1.78437 ± 0.0267136 (W 0.00800466) | 🔵 tlinalg-pool 4.73× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 1.3205 ± 0.0287457 (W 0.0111142) | 12.906 ± 0.0617901 (W 0.0315016) | 🔵 tlinalg-pool 9.77× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.322363 ± 0.00562723 (W 0.00331693) | 0.249474 ± 0.0311467 (W 0.00256848) | 🔴 tlinalg-pool 1.29× slower than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu/n8/b1024` | 0.135067 ± 0.00149958 (W 0.00107769) | 0.565713 ± 0.0212774 (W 0.00345766) | 🔵 tlinalg-pool 4.19× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.251829 ± 0.00611359 (W 0.0020721) | 1.29931 ± 0.0266939 (W 0.00374237) | 🔵 tlinalg-pool 5.16× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 0.721236 ± 0.009479 (W 0.00417094) | 10.2627 ± 0.0632575 (W 0.0139677) | 🔵 tlinalg-pool 14.23× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.241427 ± 0.00243857 (W 0.00298946) | 0.178366 ± 0.00397832 (W 0.00168469) | 🔴 tlinalg-pool 1.35× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.097306 ± 0.000859439 (W 0.00122195) | 0.362687 ± 0.0071759 (W 0.00344364) | 🔵 tlinalg-pool 3.73× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.328309 ± 0.00476502 (W 0.00207885) | 2.37091 ± 0.0383987 (W 0.00768744) | 🔵 tlinalg-pool 7.22× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 0.894926 ± 0.00982182 (W 0.00266236) | 14.7791 ± 0.0737823 (W 0.0290543) | 🔵 tlinalg-pool 16.51× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.056079 ± 0.000801017 (W 0.00127442) | 0.272628 ± 0.00103274 (W 0.00215239) | 🔵 tlinalg-pool 4.86× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.119543 ± 0.00236902 (W 0.00178781) | 0.910415 ± 0.00524883 (W 0.00283158) | 🔵 tlinalg-pool 7.62× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.098097 ± 0.000247353 (W 0.000306639) | 1.06832 ± 0.00714306 (W 0.00437925) | 🔵 tlinalg-pool 10.89× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.233935 ± 0.00669743 (W 0.00245249) | 4.46264 ± 0.0232006 (W 0.0125164) | 🔵 tlinalg-pool 19.08× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.020723 ± 0.000297524 (W 9.93846e-05) | 0.132872 ± 0.000442527 (W 0.00184871) | 🔵 tlinalg-pool 6.41× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.044432 ± 0.00554328 (W 0.000193366) | 0.608207 ± 0.000980853 (W 0.00276601) | 🔵 tlinalg-pool 13.69× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `qr/n16/b1024` | 1.13776 ± 0.0121331 (W 0.00222156) | 5.32091 ± 0.0413722 (W 0.00806294) | 🔵 tlinalg-pool 4.68× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 4.28249 ± 0.0213524 (W 0.0107574) | 20.7385 ± 0.105273 (W 0.0372446) | 🔵 tlinalg-pool 4.84× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.098858 ± 0.00122339 (W 0.00293508) | 0.707658 ± 0.0058743 (W 0.00263861) | 🔵 tlinalg-pool 7.16× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.311001 ± 0.00612385 (W 0.00200314) | 1.68081 ± 0.0107347 (W 0.00579897) | 🔵 tlinalg-pool 5.40× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.36227 ± 0.0321419 (W 0.00682232) | 8.9264 ± 0.0322519 (W 0.0169452) | 🔵 tlinalg-pool 6.55× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 4.50742 ± 0.0525726 (W 0.00451191) | 30.8862 ± 0.0808485 (W 0.0366868) | 🔵 tlinalg-pool 6.85× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.169299 ± 0.00185499 (W 0.00170789) | 1.43968 ± 0.00756674 (W 0.00572903) | 🔵 tlinalg-pool 8.50× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.439602 ± 0.00731057 (W 0.00235585) | 3.35797 ± 0.00917131 (W 0.00563325) | 🔵 tlinalg-pool 7.64× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.351893 ± 0.00312669 (W 0.00270827) | 2.52686 ± 0.0594469 (W 0.00544553) | 🔵 tlinalg-pool 7.18× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 0.962539 ± 0.0131463 (W 0.00208046) | 15.2166 ± 0.0532548 (W 0.0214065) | 🔵 tlinalg-pool 15.81× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.053299 ± 0.0011949 (W 0.000368938) | 0.340798 ± 0.00946086 (W 0.0022219) | 🔵 tlinalg-pool 6.39× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.125858 ± 0.00221906 (W 0.00190811) | 1.01844 ± 0.00951501 (W 0.00340734) | 🔵 tlinalg-pool 8.09× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 6.74186 ± 0.091463 (W 0.010153) | 52.5088 ± 0.186723 (W 0.247874) | 🔵 tlinalg-pool 7.79× faster than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 23.9761 ± 0.596212 (W 0.0211118) | 193.423 ± 0.360632 (W 0.236036) | 🔵 tlinalg-pool 8.07× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.556953 ± 0.00697126 (W 0.00256032) | 6.34707 ± 0.0173612 (W 0.0113737) | 🔵 tlinalg-pool 11.40× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 1.91235 ± 0.0440774 (W 0.00416738) | 19.1226 ± 0.0386133 (W 0.0605964) | 🔵 tlinalg-pool 10.00× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 6.77622 ± 0.0906072 (W 0.00961786) | 52.5393 ± 0.202199 (W 0.0542378) | 🔵 tlinalg-pool 7.75× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 23.8137 ± 0.220598 (W 0.0245028) | 193.344 ± 0.778889 (W 0.318432) | 🔵 tlinalg-pool 8.12× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1024` | 0.555249 ± 0.00629857 (W 0.00292264) | 6.35267 ± 0.01828 (W 0.00810754) | 🔵 tlinalg-pool 11.44× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 1.91297 ± 0.0471792 (W 0.00278575) | 19.1358 ± 0.045092 (W 0.0111889) | 🔵 tlinalg-pool 10.00× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 2.81807 ± 0.0215181 (W 0.00521461) | 19.6045 ± 0.136353 (W 0.0170945) | 🔵 tlinalg-pool 6.96× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 9.3532 ± 0.034545 (W 0.00408417) | 63.5737 ± 0.63914 (W 0.214695) | 🔵 tlinalg-pool 6.80× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.368457 ± 0.00161974 (W 0.00269443) | 2.90212 ± 0.014952 (W 0.00268659) | 🔵 tlinalg-pool 7.88× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.00913 ± 0.00953101 (W 0.00123919) | 7.09042 ± 0.0323757 (W 0.00823667) | 🔵 tlinalg-pool 7.03× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.069639 ± 0.000643876 (W 0.00174234) | 0.55286 ± 0.00595939 (W 0.00474189) | 🔵 tlinalg-pool 7.94× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.160072 ± 0.0016112 (W 0.00300063) | 2.65469 ± 0.0278079 (W 0.0131182) | 🔵 tlinalg-pool 16.58× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.0141365 ± 0.000188548 (W 0.000116528) | 0.276207 ± 0.00517578 (W 0.00190649) | 🔵 tlinalg-pool 19.54× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.030978 ± 0.000154785 (W 0.000110327) | 0.358474 ± 0.00576627 (W 0.00256412) | 🔵 tlinalg-pool 11.57× faster than `lapack-mkl` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.168072 ± 0.00307736 (W 0.00210004) | 1.81951 ± 0.0173023 (W 0.00981248) | 🔵 tlinalg-pool 10.83× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.803828 ± 0.00256712 (W 0.00633914) | 8.71845 ± 0.0354562 (W 0.0176081) | 🔵 tlinalg-pool 10.85× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.027957 ± 0.000364829 (W 9.66157e-05) | 0.176181 ± 0.000417742 (W 0.00168264) | 🔵 tlinalg-pool 6.30× faster than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.05653 ± 0.000453592 (W 0.000197249) | 0.48299 ± 0.00269806 (W 0.0031571) | 🔵 tlinalg-pool 8.54× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 16.4586 ± 0.157143 (W 0.0246657) | 179.812 ± 0.915532 (W 0.22958) | 🔵 tlinalg-pool 10.93× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 67.7468 ± 0.120991 (W 0.0487793) | 827.717 ± 2.85104 (W 1.91276) | 🔵 tlinalg-pool 12.22× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 1.37288 ± 0.0150643 (W 0.00310586) | 12.2024 ± 0.0528894 (W 0.0272835) | 🔵 tlinalg-pool 8.89× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 4.57049 ± 0.0341472 (W 0.00709128) | 42.7618 ± 0.0335575 (W 0.0493354) | 🔵 tlinalg-pool 9.36× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 4.0114 ± 0.0223418 (W 0.00739126) | 32.1615 ± 0.472551 (W 0.0322107) | 🔵 tlinalg-pool 8.02× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 17.5105 ± 0.0635406 (W 0.0145479) | 148.468 ± 0.628996 (W 0.247033) | 🔵 tlinalg-pool 8.48× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.384552 ± 0.00264371 (W 0.00226158) | 2.89803 ± 0.00115619 (W 0.00444573) | 🔵 tlinalg-pool 7.54× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.17576 ± 0.00423196 (W 0.00412715) | 8.98725 ± 0.0251836 (W 0.00999427) | 🔵 tlinalg-pool 7.64× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 9.87672 ± 0.111849 (W 0.0143581) | 125.772 ± 0.649519 (W 0.252028) | 🔵 tlinalg-pool 12.73× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 43.0681 ± 0.0823054 (W 0.0412647) | 545.736 ± 1.21088 (W 0.668392) | 🔵 tlinalg-pool 12.67× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.678109 ± 0.0231797 (W 0.00269513) | 9.5021 ± 0.00647275 (W 0.00795084) | 🔵 tlinalg-pool 14.01× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigvals/n8/b1024` | 2.55416 ± 0.00693223 (W 0.00346631) | 33.827 ± 0.0301825 (W 0.0404943) | 🔵 tlinalg-pool 13.24× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 3.02571 ± 0.00523278 (W 0.00181545) | 17.4357 ± 0.121854 (W 0.0222633) | 🔵 tlinalg-pool 5.76× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 11.5943 ± 0.0351058 (W 0.00990615) | 72.3468 ± 0.235888 (W 0.0927071) | 🔵 tlinalg-pool 6.24× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.311917 ± 0.000877621 (W 0.00239666) | 1.75042 ± 0.0205298 (W 0.00414003) | 🔵 tlinalg-pool 5.61× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.952436 ± 0.00135264 (W 0.00161404) | 5.30136 ± 0.0081407 (W 0.0108871) | 🔵 tlinalg-pool 5.57× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.656875 ± 0.00473465 (W 0.00783917) | 5.61105 ± 0.0950689 (W 0.0195874) | 🔵 tlinalg-pool 8.54× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 3.06542 ± 0.0265569 (W 0.0164387) | 27.4995 ± 0.107082 (W 0.0840903) | 🔵 tlinalg-pool 8.97× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.090087 ± 0.00248468 (W 0.00118299) | 0.53161 ± 0.00465003 (W 0.00417098) | 🔵 tlinalg-pool 5.90× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.213616 ± 0.00275534 (W 0.00281072) | 1.28301 ± 0.00205254 (W 0.00259499) | 🔵 tlinalg-pool 6.01× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.771006 ± 0.00461588 (W 0.00481021) | 8.72444 ± 0.0507893 (W 0.0247966) | 🔵 tlinalg-pool 11.32× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 2.74359 ± 0.00487174 (W 0.00743158) | 35.8014 ± 0.0487238 (W 0.0525975) | 🔵 tlinalg-pool 13.05× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.125317 ± 0.00186718 (W 0.00201117) | 1.47988 ± 0.01055 (W 0.00794115) | 🔵 tlinalg-pool 11.81× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.291424 ± 0.00321963 (W 0.0025827) | 3.10607 ± 0.0234098 (W 0.00659764) | 🔵 tlinalg-pool 10.66× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.632293 ± 0.0107842 (W 0.00315279) | 6.50928 ± 0.0911363 (W 0.0196247) | 🔵 tlinalg-pool 10.29× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 3.54306 ± 0.024075 (W 0.0161316) | 38.6259 ± 0.410278 (W 0.0921644) | 🔵 tlinalg-pool 10.90× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.0526475 ± 0.000773052 (W 0.000226078) | 0.474247 ± 0.0059821 (W 0.00293306) | 🔵 tlinalg-pool 9.01× faster than `lapack-mkl` |  |
| `householder_apply/n8/b1024` | 0.151286 ± 0.0027634 (W 0.00141428) | 1.47022 ± 0.026691 (W 0.0258253) | 🔵 tlinalg-pool 9.72× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1024` | 0.603731 ± 0.00779544 (W 0.00314361) | 6.32147 ± 0.0179708 (W 0.00687049) | 🔵 tlinalg-pool 10.47× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 2.55543 ± 0.0152888 (W 0.0124124) | 26.8458 ± 0.103959 (W 0.043479) | 🔵 tlinalg-pool 10.51× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.079738 ± 0.000139715 (W 0.000319553) | 0.529976 ± 0.00304466 (W 0.00224526) | 🔵 tlinalg-pool 6.65× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.20199 ± 0.000815044 (W 0.00102427) | 1.49758 ± 0.00228477 (W 0.00358391) | 🔵 tlinalg-pool 7.41× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.449709 ± 0.00388312 (W 0.0057502) | 3.51188 ± 0.0337595 (W 0.014124) | 🔵 tlinalg-pool 7.81× faster than `lapack-mkl` |  |
| `lu/n32/b1024` | 2.14351 ± 0.0129535 (W 0.022395) | 19.4613 ± 0.0536929 (W 0.0349515) | 🔵 tlinalg-pool 9.08× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.0639835 ± 0.000589623 (W 0.000855304) | 0.295419 ± 0.00345729 (W 0.00247444) | 🔵 tlinalg-pool 4.62× faster than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.142539 ± 0.0023128 (W 0.00194497) | 0.896582 ± 0.00992044 (W 0.00241482) | 🔵 tlinalg-pool 6.29× faster than `lapack-mkl` |  |
| `lu_factor/n16/b1024` | 0.29081 ± 0.00691461 (W 0.00183285) | 2.40649 ± 0.0208428 (W 0.00324357) | 🔵 tlinalg-pool 8.28× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 1.22348 ± 0.0109727 (W 0.0105845) | 15.243 ± 0.0945036 (W 0.0268464) | 🔵 tlinalg-pool 12.46× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.0612485 ± 0.000776015 (W 0.000456291) | 0.202114 ± 0.0037433 (W 0.0020577) | 🔵 tlinalg-pool 3.30× faster than `lapack-mkl` |  |
| `lu_factor/n8/b1024` | 0.104179 ± 0.00151307 (W 0.000932118) | 0.593386 ± 0.00578968 (W 0.00241757) | 🔵 tlinalg-pool 5.70× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.459064 ± 0.00695758 (W 0.00346991) | 5.08189 ± 0.0466755 (W 0.0108716) | 🔵 tlinalg-pool 11.07× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 1.68662 ± 0.00953544 (W 0.015142) | 20.846 ± 0.100162 (W 0.028922) | 🔵 tlinalg-pool 12.36× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.0732755 ± 0.000493509 (W 0.0017748) | 0.517922 ± 0.0035886 (W 0.00281364) | 🔵 tlinalg-pool 7.07× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.159436 ± 0.000607858 (W 0.00158391) | 1.53153 ± 0.00518339 (W 0.00322809) | 🔵 tlinalg-pool 9.61× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.183225 ± 0.00112089 (W 0.00265847) | 2.56488 ± 0.0166152 (W 0.0114906) | 🔵 tlinalg-pool 14.00× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.877413 ± 0.00494761 (W 0.00409584) | 5.55043 ± 0.0429793 (W 0.0809122) | 🔵 tlinalg-pool 6.33× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.033367 ± 0.000309758 (W 0.000108979) | 0.324677 ± 0.000542133 (W 0.00222209) | 🔵 tlinalg-pool 9.73× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.076366 ± 0.000520746 (W 0.00165452) | 0.946924 ± 0.00209167 (W 0.00191769) | 🔵 tlinalg-pool 12.40× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.38701 ± 0.00877518 (W 0.00307354) | 10.8544 ± 0.043754 (W 0.018407) | 🔵 tlinalg-pool 7.83× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 8.98839 ± 0.0448082 (W 0.00651894) | 49.6889 ± 0.504283 (W 0.228556) | 🔵 tlinalg-pool 5.53× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.117608 ± 0.00138397 (W 0.000124169) | 0.986792 ± 0.00202122 (W 0.00322659) | 🔵 tlinalg-pool 8.39× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.340296 ± 0.00286426 (W 0.00204157) | 2.80615 ± 0.00962335 (W 0.0107786) | 🔵 tlinalg-pool 8.25× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.60532 ± 0.00684892 (W 0.00286738) | 15.956 ± 0.13123 (W 0.0273073) | 🔵 tlinalg-pool 9.94× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 8.45854 ± 0.231909 (W 0.0116423) | 68.2073 ± 0.132805 (W 0.239737) | 🔵 tlinalg-pool 8.06× faster than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/n4/b1024` | 0.198127 ± 0.00132108 (W 0.00172033) | 1.90431 ± 0.00607923 (W 0.0073686) | 🔵 tlinalg-pool 9.61× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.498447 ± 0.0108235 (W 0.00242756) | 4.98869 ± 0.0141769 (W 0.019604) | 🔵 tlinalg-pool 10.01× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.498354 ± 0.00313098 (W 0.00308156) | 5.37223 ± 0.0554122 (W 0.00947903) | 🔵 tlinalg-pool 10.78× faster than `lapack-mkl` |  |
| `solve/n32/b1024` | 1.81833 ± 0.0123993 (W 0.0108258) | 21.5574 ± 0.0923358 (W 0.0369326) | 🔵 tlinalg-pool 11.86× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.07572 ± 0.0009044 (W 0.00174499) | 0.596392 ± 0.00241734 (W 0.00233986) | 🔵 tlinalg-pool 7.88× faster than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.18908 ± 0.00325128 (W 0.00235223) | 1.63975 ± 0.00546265 (W 0.00522339) | 🔵 tlinalg-pool 8.67× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 7.86181 ± 0.347071 (W 0.0094517) | 68.2464 ± 0.199665 (W 0.0804793) | 🔵 tlinalg-pool 8.68× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 31.2186 ± 1.65083 (W 0.0172545) | 280.04 ± 1.22753 (W 0.279838) | 🔵 tlinalg-pool 8.97× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.661254 ± 0.0217622 (W 0.00382683) | 7.57044 ± 0.0517047 (W 0.00722867) | 🔵 tlinalg-pool 11.45× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 2.10736 ± 0.066061 (W 0.00361065) | 22.4349 ± 0.0404075 (W 0.0204935) | 🔵 tlinalg-pool 10.65× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.22451 ± 0.249685 (W 0.010743) | 67.8225 ± 0.177449 (W 0.0557969) | 🔵 tlinalg-pool 9.39× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 31.1842 ± 0.244367 (W 0.0356848) | 280.264 ± 1.61881 (W 0.315261) | 🔵 tlinalg-pool 8.99× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1024` | 0.66219 ± 0.00422659 (W 0.00313096) | 7.5561 ± 0.0110482 (W 0.00800379) | 🔵 tlinalg-pool 11.41× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 2.09386 ± 0.053127 (W 0.00295892) | 22.3582 ± 0.0474729 (W 0.0284308) | 🔵 tlinalg-pool 10.68× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 3.22178 ± 0.00756771 (W 0.00434064) | 27.3709 ± 0.0337536 (W 0.0401963) | 🔵 tlinalg-pool 8.50× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 11.5781 ± 0.0319895 (W 0.0112934) | 102.488 ± 0.237744 (W 0.225481) | 🔵 tlinalg-pool 8.85× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.440753 ± 0.00214424 (W 0.00279044) | 3.54142 ± 0.0100598 (W 0.00432233) | 🔵 tlinalg-pool 8.03× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.14722 ± 0.0021215 (W 0.00148718) | 8.9614 ± 0.0056612 (W 0.0113134) | 🔵 tlinalg-pool 7.81× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.127947 ± 0.00043622 (W 0.000967175) | 1.40302 ± 0.0168649 (W 0.00540113) | 🔵 tlinalg-pool 10.97× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.533324 ± 0.00268205 (W 0.00441721) | 3.37836 ± 0.0259776 (W 0.00957824) | 🔵 tlinalg-pool 6.33× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.0238745 ± 0.000197957 (W 0.000114972) | 0.308897 ± 0.000482727 (W 0.00223912) | 🔵 tlinalg-pool 12.94× faster than `lapack-mkl` |  |
| `triangular_solve/n8/b1024` | 0.054326 ± 0.000594249 (W 0.000331676) | 0.62743 ± 0.00474391 (W 0.0034634) | 🔵 tlinalg-pool 11.55× faster than `lapack-mkl` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0732105 ± 0.000382637 (W 0.000342491) | 0.094054 ± 0.000615937 (W 0.00172985) | 🔵 tlinalg-pool 1.28× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.167039 ± 0.0065179 (W 0.00139079) | 0.15053 ± 0.000412133 (W 0.00167748) | 🔴 tlinalg-pool 1.11× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n128/b1` | 0.093037 ± 0.000536441 (W 0.000429277) | 0.136123 ± 0.000566175 (W 0.0020299) | 🔵 tlinalg-pool 1.46× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.102981 ± 0.00106849 (W 0.000256279) | 0.157632 ± 0.0016081 (W 0.00164336) | 🔵 tlinalg-pool 1.53× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.011411 ± 5.44082e-05 (W 6.88772e-05) | 0.016566 ± 0.000132004 (W 0.00026286) | 🔵 tlinalg-pool 1.45× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.121986 ± 0.00156521 (W 0.00157579) | 0.16467 ± 0.000673742 (W 0.00189562) | 🔵 tlinalg-pool 1.35× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 1.14763 ± 0.00571192 (W 0.00309001) | 1.10581 ± 0.00481226 (W 0.00354172) | · |  |
| `triangular_solve/n128/b1` | 0.008025 ± 8.28654e-05 (W 7.66742e-05) | 0.009723 ± 4.19325e-05 (W 0.000124765) | 🔵 tlinalg-pool 1.21× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.160262 ± 0.000854105 (W 0.00158148) | 0.40773 ± 0.0016293 (W 0.00326609) | 🔵 tlinalg-pool 2.54× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.308447 ± 0.00726281 (W 0.00252018) | 0.438388 ± 0.000750531 (W 0.00321795) | 🔵 tlinalg-pool 1.42× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n128/b1` | 0.218646 ± 0.00128911 (W 0.00208342) | 0.404907 ± 0.000500278 (W 0.00324328) | 🔵 tlinalg-pool 1.85× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.254121 ± 0.00153741 (W 0.00231209) | 0.434729 ± 0.00364553 (W 0.00378965) | 🔵 tlinalg-pool 1.71× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.0338125 ± 0.00031896 (W 0.000229) | 0.0252165 ± 0.000159805 (W 0.000199008) | 🔴 tlinalg-pool 1.34× slower than `lapack-mkl` |  |
| `solve/n128/b1` | 0.275983 ± 0.00268188 (W 0.00227436) | 0.450677 ± 0.00193427 (W 0.00351022) | 🔵 tlinalg-pool 1.63× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 1.4726 ± 0.00264667 (W 0.00354359) | 1.88312 ± 0.0101584 (W 0.00826285) | 🔵 tlinalg-pool 1.28× faster than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.020192 ± 7.97303e-05 (W 0.000112639) | 0.0128985 ± 0.000125648 (W 9.60282e-05) | 🔴 tlinalg-pool 1.57× slower than `lapack-mkl` |  |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 27.3598 ± 0.0330059 (W 0.0255529) | 14.7891 ± 0.0247149 (W 0.0464995) | 🔴 tlinalg-pool 1.85× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 16.2725 ± 0.0386002 (W 0.0176252) | 12.1608 ± 0.0317305 (W 0.0140098) | 🔴 tlinalg-pool 1.34× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 1.59458 ± 0.00513828 (W 0.00461657) | 3.16436 ± 0.0132614 (W 0.0177073) | 🔵 tlinalg-pool 1.98× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 1.86033 ± 0.00346049 (W 0.00334443) | 2.11787 ± 0.00609167 (W 0.00684423) | 🔵 tlinalg-pool 1.14× faster than `lapack-mkl` |  |
| `qr/n512/b1` | 5.50551 ± 0.00576664 (W 0.00993477) | 8.78766 ± 0.135201 (W 0.0244337) | 🔵 tlinalg-pool 1.60× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 6.77342 ± 0.0317609 (W 0.0136618) | 24.2454 ± 0.138872 (W 0.0332673) | 🔵 tlinalg-pool 3.58× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 38.4593 ± 0.0769637 (W 0.0341857) | 48.3988 ± 0.456289 (W 0.0514647) | 🔵 tlinalg-pool 1.26× faster than `lapack-mkl` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 37.2267 ± 0.0496431 (W 0.0296649) | 65.6863 ± 0.10046 (W 0.0615122) | 🔵 tlinalg-pool 1.76× faster than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 20.4707 ± 0.0347978 (W 0.0172241) | 28.0443 ± 0.0776923 (W 0.0207545) | 🔵 tlinalg-pool 1.37× faster than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 5.64729 ± 0.0182877 (W 0.0154696) | 8.20373 ± 0.0399672 (W 0.0185401) | 🔵 tlinalg-pool 1.45× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 5.27452 ± 0.0107088 (W 0.00694209) | 5.49193 ± 0.0159285 (W 0.0154176) | · |  |
| `qr/n512/b1` | 13.2881 ± 0.0349621 (W 0.0170699) | 15.4303 ± 0.0546435 (W 0.014044) | 🔵 tlinalg-pool 1.16× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 14.2853 ± 0.0435151 (W 0.0229631) | 59.4349 ± 0.254761 (W 0.19834) | 🔵 tlinalg-pool 4.16× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 76.0317 ± 0.103616 (W 0.176804) | 86.3513 ± 0.689787 (W 0.0793162) | 🔵 tlinalg-pool 1.14× faster than `lapack-mkl` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 6.05697 ± 0.0360906 (W 0.0411713) | 6.18077 ± 0.0548791 (W 0.0417963) | · |  |
| `qr/4096x256/b1` | 22.4279 ± 0.0141609 (W 0.0686291) | 18.1289 ± 0.0331261 (W 0.0682853) | 🔴 tlinalg-pool 1.24× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 21.5908 ± 0.0635125 (W 0.0587891) | 56.135 ± 0.813445 (W 0.599057) | 🔵 tlinalg-pool 2.60× faster than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 35.1421 ± 0.0438973 (W 0.0527785) | 33.9409 ± 0.130396 (W 0.113435) | · |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 17.7624 ± 0.0842676 (W 0.0332064) | 16.8791 ± 0.074119 (W 0.120088) | 🔴 tlinalg-pool 1.05× slower than `lapack-mkl` |  |
| `qr/4096x256/b1` | 58.8952 ± 0.155558 (W 0.0492143) | 40.4763 ± 0.301507 (W 0.232569) | 🔴 tlinalg-pool 1.46× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 58.8993 ± 0.347689 (W 0.185089) | 154.845 ± 0.502868 (W 0.354191) | 🔵 tlinalg-pool 2.63× faster than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 108.792 ± 0.220599 (W 0.213285) | 75.4221 ± 0.485468 (W 0.525231) | 🔴 tlinalg-pool 1.44× slower than `lapack-mkl` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
