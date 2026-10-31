<!-- generated from data/results/zen5-cpu/tlinalg-competition/20261031T121942Z-pub-53d1f0d9-20261031-competition-mkl/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `f00d46158eeb5cacf198bceba6197d5eb2043afc`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `f9de3c2ea11208f98dfddae328c2a2b5c15bdc311582ad4269a4c6dda4ca4673`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-31T12:39:53.545790Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 1 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor mkl --aa 4 --reps 5 --prime-ms 250 --label pub-53d1f0d9-20261031-competition-mkl`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261031T121942Z-pub-53d1f0d9-20261031-competition-mkl/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.29%, worst 33.28% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 40 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.33%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.119366 ± 0.000695398 (W 0.00243473) | 1.06652 ± 0.0012858 (W 0.00236541) | 🔵 tlinalg-pool 8.93× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.478287 ± 0.00162469 (W 0.00805826) | 3.80665 ± 0.0286122 (W 0.0272017) | 🔵 tlinalg-pool 7.96× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.180484 ± 0.000492269 (W 0.00118859) | 0.122973 ± 0.00348857 (W 0.000154185) | 🔴 tlinalg-pool 1.47× slower than `lapack-mkl` | `!` between-start range over 5% |
| `cholesky/n8/b1024` | 0.049577 ± 0.000192094 (W 0.00013725) | 0.324446 ± 0.00294615 (W 0.00208806) | 🔵 tlinalg-pool 6.54× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 11.9975 ± 0.0650107 (W 0.0168664) | 52.9614 ± 0.224429 (W 0.0880673) | 🔵 tlinalg-pool 4.41× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 54.104 ± 0.303204 (W 0.053995) | 284.458 ± 0.569281 (W 0.394215) | 🔵 tlinalg-pool 5.26× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 0.809944 ± 0.00616379 (W 0.00230116) | 2.86368 ± 0.00988159 (W 0.00386905) | 🔵 tlinalg-pool 3.54× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 3.01189 ± 0.0171852 (W 0.00313188) | 11.8942 ± 0.0941696 (W 0.0771669) | 🔵 tlinalg-pool 3.95× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 3.76006 ± 0.032309 (W 0.00302925) | 23.7982 ± 0.093972 (W 0.0233712) | 🔵 tlinalg-pool 6.33× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 14.0282 ± 0.379079 (W 0.0152491) | 98.2109 ± 0.30753 (W 0.0830395) | 🔵 tlinalg-pool 7.00× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigh/n4/b1024` | 0.327388 ± 0.00378897 (W 0.00181745) | 2.97912 ± 0.00642394 (W 0.00693686) | 🔵 tlinalg-pool 9.10× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.09479 ± 0.00690597 (W 0.00213734) | 7.90817 ± 0.0439254 (W 0.0251364) | 🔵 tlinalg-pool 7.22× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 8.31216 ± 0.0279002 (W 0.00776498) | 36.6592 ± 0.0651843 (W 0.0579515) | 🔵 tlinalg-pool 4.41× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 36.5899 ± 1.00648 (W 0.14705) | 172.208 ± 0.241021 (W 0.125402) | 🔵 tlinalg-pool 4.71× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigvals/n4/b1024` | 0.435388 ± 0.00193674 (W 0.00371657) | 2.11081 ± 0.00254759 (W 0.00253394) | 🔵 tlinalg-pool 4.85× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 1.98517 ± 0.0229189 (W 0.00450907) | 9.00817 ± 0.0458474 (W 0.0326745) | 🔵 tlinalg-pool 4.54× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 2.83436 ± 0.0160631 (W 0.00378289) | 12.8109 ± 0.0534213 (W 0.0350109) | 🔵 tlinalg-pool 4.52× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 10.6891 ± 0.067658 (W 0.00980008) | 41.7591 ± 0.227219 (W 0.0356976) | 🔵 tlinalg-pool 3.91× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.258344 ± 0.00341627 (W 0.00177503) | 1.56355 ± 0.00466164 (W 0.00398407) | 🔵 tlinalg-pool 6.05× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.867673 ± 0.00232566 (W 0.00165564) | 4.47864 ± 0.0183198 (W 0.00901993) | 🔵 tlinalg-pool 5.16× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.511474 ± 0.00531828 (W 0.00410327) | 3.90206 ± 0.0198445 (W 0.0150677) | 🔵 tlinalg-pool 7.63× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 2.04786 ± 0.0164883 (W 0.0125611) | 26.4313 ± 0.0914399 (W 0.0342001) | 🔵 tlinalg-pool 12.91× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.499476 ± 0.00463083 (W 0.00303123) | 0.410552 ± 0.00221707 (W 0.00366255) | 🔴 tlinalg-pool 1.22× slower than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 0.18033 ± 0.013566 (W 0.00215613) | 0.990912 ± 0.00673613 (W 0.00362077) | 🔵 tlinalg-pool 5.50× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 0.494542 ± 0.00640566 (W 0.00229787) | 5.7094 ± 0.0498696 (W 0.0186833) | 🔵 tlinalg-pool 11.54× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 1.64316 ± 0.0583896 (W 0.011049) | 29.4225 ± 0.0987485 (W 0.0256403) | 🔵 tlinalg-pool 17.91× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n4/b1024` | 0.083129 ± 0.00109193 (W 0.00233362) | 1.00305 ± 0.010374 (W 0.00246386) | 🔵 tlinalg-pool 12.07× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.196053 ± 0.00181085 (W 0.00202102) | 1.84464 ± 0.00846074 (W 0.00556875) | 🔵 tlinalg-pool 9.41× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.593711 ± 0.0276941 (W 0.00316985) | 2.66365 ± 0.0121582 (W 0.0173898) | 🔵 tlinalg-pool 4.49× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 2.38334 ± 0.103052 (W 0.00841008) | 13.1578 ± 0.069558 (W 0.0297086) | 🔵 tlinalg-pool 5.52× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.053154 ± 0.00214224 (W 9.14955e-05) | 0.324001 ± 0.00936724 (W 0.00175717) | 🔵 tlinalg-pool 6.10× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.162937 ± 0.00547241 (W 0.00139798) | 0.790552 ± 0.0236046 (W 0.00727305) | 🔵 tlinalg-pool 4.85× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.509431 ± 0.0100065 (W 0.00160179) | 2.97236 ± 0.0148809 (W 0.00399112) | 🔵 tlinalg-pool 5.83× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 1.6921 ± 0.0399759 (W 0.00448705) | 11.9834 ± 0.0576054 (W 0.0169103) | 🔵 tlinalg-pool 7.08× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.0641495 ± 0.000420595 (W 0.000219177) | 0.338652 ± 0.000353067 (W 0.00226803) | 🔵 tlinalg-pool 5.28× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.168623 ± 0.00276937 (W 0.00184911) | 0.870051 ± 0.00435685 (W 0.00247303) | 🔵 tlinalg-pool 5.16× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.37944 ± 0.00892459 (W 0.00265691) | 1.77274 ± 0.0679692 (W 0.00614462) | 🔵 tlinalg-pool 4.67× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 1.30948 ± 0.0124985 (W 0.0090838) | 12.8866 ± 0.0955553 (W 0.0535561) | 🔵 tlinalg-pool 9.84× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.320168 ± 0.00710418 (W 0.00198132) | 0.225382 ± 0.00133864 (W 0.00299944) | 🔴 tlinalg-pool 1.42× slower than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.135136 ± 0.00337252 (W 0.00164006) | 0.575311 ± 0.0270779 (W 0.00310002) | 🔵 tlinalg-pool 4.26× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.257242 ± 0.00316305 (W 0.00207202) | 1.28429 ± 0.0250401 (W 0.00398581) | 🔵 tlinalg-pool 4.99× faster than `lapack-mkl` |  |
| `lu_factor/n32/b1024` | 0.72575 ± 0.0149605 (W 0.00483698) | 10.1861 ± 0.0506232 (W 0.020593) | 🔵 tlinalg-pool 14.04× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.241818 ± 0.00105785 (W 0.0030186) | 0.177428 ± 0.00477551 (W 0.00251216) | 🔴 tlinalg-pool 1.36× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.097922 ± 0.00251031 (W 0.00152307) | 0.360488 ± 0.0063067 (W 0.00270498) | 🔵 tlinalg-pool 3.68× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n16/b1024` | 0.330608 ± 0.00592306 (W 0.00184971) | 2.34275 ± 0.0272617 (W 0.00825972) | 🔵 tlinalg-pool 7.09× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 0.895887 ± 0.0147266 (W 0.00238273) | 14.9719 ± 0.0330008 (W 0.0269733) | 🔵 tlinalg-pool 16.71× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.058208 ± 0.000583417 (W 0.00078612) | 0.273182 ± 0.00255291 (W 0.00198573) | 🔵 tlinalg-pool 4.69× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.122723 ± 0.0033357 (W 0.00188726) | 0.907332 ± 0.00297284 (W 0.00286306) | 🔵 tlinalg-pool 7.39× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1024` | 0.098523 ± 0.000294766 (W 0.00151826) | 1.06835 ± 0.00260445 (W 0.00337279) | 🔵 tlinalg-pool 10.84× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.230759 ± 0.00309364 (W 0.00263335) | 4.54385 ± 0.0464633 (W 0.0132085) | 🔵 tlinalg-pool 19.69× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.0210085 ± 8.12214e-05 (W 7.75035e-05) | 0.133111 ± 0.00170169 (W 0.000771642) | 🔵 tlinalg-pool 6.34× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.0445475 ± 0.000460545 (W 0.000795233) | 0.604369 ± 0.00179725 (W 0.00278207) | 🔵 tlinalg-pool 13.57× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.14216 ± 0.0219224 (W 0.00267594) | 5.2779 ± 0.0317296 (W 0.0111846) | 🔵 tlinalg-pool 4.62× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 4.32393 ± 0.0289844 (W 0.00824499) | 20.7514 ± 0.248037 (W 0.0530126) | 🔵 tlinalg-pool 4.80× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.100737 ± 0.00181879 (W 0.00191474) | 0.703844 ± 0.00255676 (W 0.0034727) | 🔵 tlinalg-pool 6.99× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.31785 ± 0.00380356 (W 0.00159441) | 1.67646 ± 0.0131834 (W 0.00626323) | 🔵 tlinalg-pool 5.27× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.35124 ± 0.0236431 (W 0.00277756) | 8.91119 ± 0.0216359 (W 0.0197253) | 🔵 tlinalg-pool 6.59× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 4.44424 ± 0.0372938 (W 0.0110531) | 30.7919 ± 0.136283 (W 0.0453715) | 🔵 tlinalg-pool 6.93× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.16989 ± 0.00226019 (W 0.00202227) | 1.4229 ± 0.00989097 (W 0.00907752) | 🔵 tlinalg-pool 8.38× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.434831 ± 0.00572977 (W 0.00233604) | 3.35526 ± 0.0105529 (W 0.0085574) | 🔵 tlinalg-pool 7.72× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.349388 ± 0.0107417 (W 0.00267286) | 2.54989 ± 0.0221538 (W 0.00753675) | 🔵 tlinalg-pool 7.30× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 0.966313 ± 0.0215521 (W 0.00396535) | 14.72 ± 0.057166 (W 0.0343269) | 🔵 tlinalg-pool 15.23× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n4/b1024` | 0.054035 ± 0.00111283 (W 0.000405406) | 0.340878 ± 0.00199523 (W 0.00251761) | 🔵 tlinalg-pool 6.31× faster than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.122893 ± 0.00093204 (W 0.00149233) | 1.01487 ± 0.0162562 (W 0.0052772) | 🔵 tlinalg-pool 8.26× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 6.87036 ± 0.443727 (W 0.00675432) | 52.4679 ± 0.0902141 (W 0.0785504) | 🔵 tlinalg-pool 7.64× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 24.1871 ± 0.967404 (W 0.0183637) | 191.723 ± 1.12906 (W 0.303226) | 🔵 tlinalg-pool 7.93× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.572588 ± 0.0215205 (W 0.00322539) | 6.3225 ± 0.028221 (W 0.0144448) | 🔵 tlinalg-pool 11.04× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 1.88997 ± 0.0566594 (W 0.0022933) | 19.099 ± 0.0623562 (W 0.0204268) | 🔵 tlinalg-pool 10.11× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 6.89804 ± 0.622163 (W 0.00457178) | 52.6191 ± 0.114144 (W 0.0510928) | 🔵 tlinalg-pool 7.63× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 24.2551 ± 0.975725 (W 0.0279806) | 191.814 ± 0.93527 (W 0.227386) | 🔵 tlinalg-pool 7.91× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.571729 ± 0.0222319 (W 0.00214241) | 6.33864 ± 0.0120435 (W 0.0086895) | 🔵 tlinalg-pool 11.09× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 1.88562 ± 0.0137377 (W 0.00266192) | 19.1577 ± 0.0832235 (W 0.0351668) | 🔵 tlinalg-pool 10.16× faster than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 2.81557 ± 0.0121674 (W 0.00403825) | 19.5588 ± 0.0986441 (W 0.0113506) | 🔵 tlinalg-pool 6.95× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 9.31691 ± 0.0452969 (W 0.00866318) | 63.595 ± 0.216324 (W 0.0432841) | 🔵 tlinalg-pool 6.83× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.36844 ± 0.00110696 (W 0.00243827) | 2.90059 ± 0.0112345 (W 0.00432119) | 🔵 tlinalg-pool 7.87× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.00315 ± 0.00488521 (W 0.00178261) | 7.0708 ± 0.0217544 (W 0.00704129) | 🔵 tlinalg-pool 7.05× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.069133 ± 0.0012737 (W 0.00163497) | 0.550728 ± 0.00387386 (W 0.00385602) | 🔵 tlinalg-pool 7.97× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.155453 ± 0.000959696 (W 0.00208212) | 2.4389 ± 0.021163 (W 0.00768739) | 🔵 tlinalg-pool 15.69× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.0142065 ± 0.000211692 (W 9.52228e-05) | 0.273933 ± 0.00152698 (W 0.00208705) | 🔵 tlinalg-pool 19.28× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.030878 ± 0.000124125 (W 8.37215e-05) | 0.353351 ± 0.000878036 (W 0.0031586) | 🔵 tlinalg-pool 11.44× faster than `lapack-mkl` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.167972 ± 0.000867682 (W 0.00171297) | 1.82851 ± 0.0175074 (W 0.0064643) | 🔵 tlinalg-pool 10.89× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.813679 ± 0.0047973 (W 0.0101863) | 8.80461 ± 0.0223368 (W 0.0221494) | 🔵 tlinalg-pool 10.82× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.027947 ± 0.000108128 (W 0.000104704) | 0.176668 ± 0.00104121 (W 0.00122062) | 🔵 tlinalg-pool 6.32× faster than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.056149 ± 0.000176448 (W 0.000166025) | 0.485301 ± 0.00585491 (W 0.00300216) | 🔵 tlinalg-pool 8.64× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 16.4298 ± 0.0668662 (W 0.0202465) | 178.909 ± 0.637622 (W 0.325128) | 🔵 tlinalg-pool 10.89× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 67.8524 ± 0.215202 (W 0.0388257) | 829.526 ± 2.70966 (W 0.706293) | 🔵 tlinalg-pool 12.23× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 1.35031 ± 0.0218482 (W 0.00276297) | 12.2118 ± 0.0202064 (W 0.012747) | 🔵 tlinalg-pool 9.04× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 4.53662 ± 0.268479 (W 0.00795708) | 42.6675 ± 0.0423436 (W 0.0307788) | 🔵 tlinalg-pool 9.41× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigh/n16/b1024` | 4.01873 ± 0.0226977 (W 0.00570928) | 32.4064 ± 0.0725361 (W 0.0375604) | 🔵 tlinalg-pool 8.06× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 17.5467 ± 0.0314309 (W 0.0243668) | 148.67 ± 0.41902 (W 0.114779) | 🔵 tlinalg-pool 8.47× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.386557 ± 0.0036253 (W 0.00220016) | 2.90388 ± 0.00319824 (W 0.00594525) | 🔵 tlinalg-pool 7.51× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.17594 ± 0.0076735 (W 0.00600897) | 8.97761 ± 0.0266706 (W 0.0145838) | 🔵 tlinalg-pool 7.63× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 9.88176 ± 0.0476928 (W 0.00998751) | 125.635 ± 0.715946 (W 0.0859134) | 🔵 tlinalg-pool 12.71× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 43.0824 ± 0.157906 (W 0.203105) | 545.63 ± 1.86374 (W 0.737776) | 🔵 tlinalg-pool 12.66× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.656215 ± 0.00295758 (W 0.00214927) | 9.4867 ± 0.0139339 (W 0.00805664) | 🔵 tlinalg-pool 14.46× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 2.55768 ± 0.0330171 (W 0.00562527) | 33.8712 ± 0.0120229 (W 0.0339689) | 🔵 tlinalg-pool 13.24× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 3.02979 ± 0.0122945 (W 0.00456902) | 17.4238 ± 0.0715822 (W 0.0275924) | 🔵 tlinalg-pool 5.75× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 11.5511 ± 0.0753726 (W 0.00957483) | 72.1641 ± 0.143205 (W 0.0680414) | 🔵 tlinalg-pool 6.25× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.313126 ± 0.000419917 (W 0.00435368) | 1.75258 ± 0.00404464 (W 0.002383) | 🔵 tlinalg-pool 5.60× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.950023 ± 0.00341168 (W 0.001126) | 5.2963 ± 0.0227017 (W 0.00669682) | 🔵 tlinalg-pool 5.57× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.663536 ± 0.00663237 (W 0.00719773) | 5.52821 ± 0.0541605 (W 0.0318754) | 🔵 tlinalg-pool 8.33× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 3.05292 ± 0.0162968 (W 0.0237323) | 27.4138 ± 0.0478198 (W 0.0312138) | 🔵 tlinalg-pool 8.98× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.089807 ± 0.00140417 (W 0.00195054) | 0.524309 ± 0.00251695 (W 0.0026538) | 🔵 tlinalg-pool 5.84× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 0.215661 ± 0.00358962 (W 0.0036334) | 1.2991 ± 0.0173998 (W 0.00431858) | 🔵 tlinalg-pool 6.02× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.772098 ± 0.0760571 (W 0.00592058) | 8.6789 ± 0.057581 (W 0.0147617) | 🔵 tlinalg-pool 11.24× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n32/b1024` | 2.78859 ± 0.162026 (W 0.00810435) | 35.7819 ± 0.127571 (W 0.0277378) | 🔵 tlinalg-pool 12.83× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n4/b1024` | 0.124721 ± 0.00158905 (W 0.000346273) | 1.46958 ± 0.00514433 (W 0.0057464) | 🔵 tlinalg-pool 11.78× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.290895 ± 0.0238717 (W 0.00237389) | 3.08634 ± 0.019169 (W 0.00460287) | 🔵 tlinalg-pool 10.61× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n16/b1024` | 0.628286 ± 0.0104661 (W 0.0037559) | 6.42107 ± 0.0383028 (W 0.0196395) | 🔵 tlinalg-pool 10.22× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 3.41821 ± 0.0256013 (W 0.014677) | 38.2476 ± 0.0993242 (W 0.0717989) | 🔵 tlinalg-pool 11.19× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.053284 ± 0.000899909 (W 0.000173094) | 0.474705 ± 0.00351651 (W 0.00408517) | 🔵 tlinalg-pool 8.91× faster than `lapack-mkl` |  |
| `householder_apply/n8/b1024` | 0.152568 ± 0.00222402 (W 0.00268478) | 1.4457 ± 0.0154141 (W 0.0243934) | 🔵 tlinalg-pool 9.48× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1024` | 0.606064 ± 0.00475241 (W 0.00303154) | 6.3175 ± 0.0307895 (W 0.017034) | 🔵 tlinalg-pool 10.42× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 2.55174 ± 0.0266503 (W 0.00995623) | 26.8795 ± 0.252602 (W 0.0471571) | 🔵 tlinalg-pool 10.53× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.078856 ± 0.00034618 (W 0.000386736) | 0.53092 ± 0.00113349 (W 0.00213582) | 🔵 tlinalg-pool 6.73× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.201734 ± 0.00152752 (W 0.0019306) | 1.498 ± 0.00350066 (W 0.0029168) | 🔵 tlinalg-pool 7.43× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.451277 ± 0.00830773 (W 0.010145) | 3.55922 ± 0.0382891 (W 0.0213834) | 🔵 tlinalg-pool 7.89× faster than `lapack-mkl` |  |
| `lu/n32/b1024` | 2.15567 ± 0.0042777 (W 0.0120985) | 19.4545 ± 0.0975885 (W 0.0304779) | 🔵 tlinalg-pool 9.02× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.065216 ± 0.000203446 (W 0.000447652) | 0.29643 ± 0.00774873 (W 0.00223171) | 🔵 tlinalg-pool 4.55× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.146483 ± 0.00150834 (W 0.00386085) | 0.893957 ± 0.014012 (W 0.00337117) | 🔵 tlinalg-pool 6.10× faster than `lapack-mkl` |  |
| `lu_factor/n16/b1024` | 0.29932 ± 0.0453424 (W 0.00960387) | 2.40883 ± 0.0296736 (W 0.00892815) | 🔵 tlinalg-pool 8.05× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor/n32/b1024` | 1.23868 ± 0.00441619 (W 0.00897191) | 15.8422 ± 0.108862 (W 0.06842) | 🔵 tlinalg-pool 12.79× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.0621 ± 0.00138809 (W 0.00104195) | 0.202215 ± 0.00329816 (W 0.00164566) | 🔵 tlinalg-pool 3.26× faster than `lapack-mkl` |  |
| `lu_factor/n8/b1024` | 0.110675 ± 0.00137764 (W 0.00144311) | 0.598351 ± 0.00684294 (W 0.00284748) | 🔵 tlinalg-pool 5.41× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.457174 ± 0.00712969 (W 0.00320492) | 5.0818 ± 0.0248943 (W 0.00572779) | 🔵 tlinalg-pool 11.12× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 1.71004 ± 0.00855749 (W 0.00773808) | 21.3466 ± 0.0667313 (W 0.0328272) | 🔵 tlinalg-pool 12.48× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.073722 ± 0.000702314 (W 0.000763728) | 0.5202 ± 0.00481519 (W 0.00316847) | 🔵 tlinalg-pool 7.06× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.163483 ± 0.000518144 (W 0.00184367) | 1.53273 ± 0.00815629 (W 0.00278981) | 🔵 tlinalg-pool 9.38× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.185109 ± 0.00573822 (W 0.00292238) | 2.57222 ± 0.00415097 (W 0.00802481) | 🔵 tlinalg-pool 13.90× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n32/b1024` | 0.857903 ± 0.0116911 (W 0.0157464) | 5.80603 ± 0.0737261 (W 0.0213193) | 🔵 tlinalg-pool 6.77× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.0336225 ± 0.000189435 (W 0.000110729) | 0.324848 ± 0.000329841 (W 0.0024088) | 🔵 tlinalg-pool 9.66× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.076452 ± 0.000498405 (W 0.000718886) | 0.948265 ± 0.00578778 (W 0.00101495) | 🔵 tlinalg-pool 12.40× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.39302 ± 0.0131984 (W 0.00383314) | 10.8516 ± 0.0238972 (W 0.0207752) | 🔵 tlinalg-pool 7.79× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 9.05035 ± 0.0621253 (W 0.0533833) | 49.8696 ± 0.339317 (W 0.0481521) | 🔵 tlinalg-pool 5.51× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.116982 ± 0.000568191 (W 0.00068379) | 0.992902 ± 0.01388 (W 0.00281623) | 🔵 tlinalg-pool 8.49× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.343191 ± 0.000496805 (W 0.00223239) | 2.81914 ± 0.00697732 (W 0.00382445) | 🔵 tlinalg-pool 8.21× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.60772 ± 0.0109874 (W 0.00518074) | 15.9342 ± 0.0497725 (W 0.0428035) | 🔵 tlinalg-pool 9.91× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 8.46454 ± 0.0226968 (W 0.0173802) | 68.0391 ± 0.103188 (W 0.0579193) | 🔵 tlinalg-pool 8.04× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.196785 ± 0.00117459 (W 0.00161189) | 1.92676 ± 0.00901126 (W 0.00492602) | 🔵 tlinalg-pool 9.79× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.500244 ± 0.00416756 (W 0.00230648) | 4.98903 ± 0.0125952 (W 0.0158562) | 🔵 tlinalg-pool 9.97× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.504792 ± 0.00500344 (W 0.00328202) | 5.32623 ± 0.0316632 (W 0.00702174) | 🔵 tlinalg-pool 10.55× faster than `lapack-mkl` |  |
| `solve/n32/b1024` | 1.84128 ± 0.00559207 (W 0.0135305) | 21.2901 ± 0.0837487 (W 0.042374) | 🔵 tlinalg-pool 11.56× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.0768775 ± 0.000971446 (W 0.00138394) | 0.596172 ± 0.00161865 (W 0.00253086) | 🔵 tlinalg-pool 7.75× faster than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.192462 ± 0.00167068 (W 0.00186658) | 1.64203 ± 0.0110557 (W 0.00392524) | 🔵 tlinalg-pool 8.53× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 7.23494 ± 0.215149 (W 0.0104705) | 68.1057 ± 0.111342 (W 0.121762) | 🔵 tlinalg-pool 9.41× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 32.2954 ± 1.4704 (W 0.0349428) | 280.013 ± 1.73455 (W 0.403932) | 🔵 tlinalg-pool 8.67× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.656308 ± 0.00199331 (W 0.00287165) | 7.57509 ± 0.0114215 (W 0.0108629) | 🔵 tlinalg-pool 11.54× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 2.09477 ± 0.0075509 (W 0.00234563) | 22.4333 ± 0.0577012 (W 0.018546) | 🔵 tlinalg-pool 10.71× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 7.30161 ± 0.109845 (W 0.0121055) | 68.226 ± 0.211607 (W 0.0480674) | 🔵 tlinalg-pool 9.34× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 31.6144 ± 1.29042 (W 0.0302418) | 280.755 ± 1.5689 (W 0.563023) | 🔵 tlinalg-pool 8.88× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.660842 ± 0.0277084 (W 0.00235839) | 7.56623 ± 0.00689966 (W 0.0105329) | 🔵 tlinalg-pool 11.45× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 2.0973 ± 0.0211672 (W 0.00438508) | 22.4731 ± 0.0759655 (W 0.0210141) | 🔵 tlinalg-pool 10.72× faster than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 3.2133 ± 0.0111974 (W 0.00398733) | 27.4942 ± 0.105445 (W 0.0239469) | 🔵 tlinalg-pool 8.56× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 11.5924 ± 0.0669832 (W 0.00715205) | 102.873 ± 0.085737 (W 0.0410978) | 🔵 tlinalg-pool 8.87× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.43886 ± 0.000991242 (W 0.00225378) | 3.54738 ± 0.00812642 (W 0.00500346) | 🔵 tlinalg-pool 8.08× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.15005 ± 0.0058432 (W 0.00195437) | 8.93908 ± 0.0158868 (W 0.0143353) | 🔵 tlinalg-pool 7.77× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.128112 ± 0.000771222 (W 0.00152988) | 1.4305 ± 0.0376085 (W 0.00238329) | 🔵 tlinalg-pool 11.17× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.44712 ± 0.00819434 (W 0.0089471) | 3.61862 ± 0.00578569 (W 0.00955593) | 🔵 tlinalg-pool 8.09× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.023764 ± 0.000171367 (W 7.94309e-05) | 0.30992 ± 0.000655568 (W 0.00238498) | 🔵 tlinalg-pool 13.04× faster than `lapack-mkl` |  |
| `triangular_solve/n8/b1024` | 0.0542105 ± 0.00116934 (W 0.000185104) | 0.6501 ± 0.00342499 (W 0.00419132) | 🔵 tlinalg-pool 11.99× faster than `lapack-mkl` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0735465 ± 0.000687156 (W 0.000853346) | 0.0933735 ± 0.000476988 (W 0.00126529) | 🔵 tlinalg-pool 1.27× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.167216 ± 0.00106527 (W 0.00165127) | 0.149533 ± 0.000908165 (W 0.00131143) | 🔴 tlinalg-pool 1.12× slower than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.092332 ± 0.000776729 (W 0.000346523) | 0.135632 ± 0.000514717 (W 0.00180098) | 🔵 tlinalg-pool 1.47× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.103141 ± 0.000524736 (W 0.000676954) | 0.158649 ± 0.00101824 (W 0.00198641) | 🔵 tlinalg-pool 1.54× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.011251 ± 0.00018038 (W 3.82569e-05) | 0.016716 ± 6.18466e-05 (W 0.000193425) | 🔵 tlinalg-pool 1.49× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.122693 ± 0.00133637 (W 0.000828576) | 0.165031 ± 0.000725834 (W 0.00177351) | 🔵 tlinalg-pool 1.35× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 1.14748 ± 0.00443571 (W 0.00325793) | 1.11546 ± 0.00569049 (W 0.00357881) | · |  |
| `triangular_solve/n128/b1` | 0.00794 ± 2.94392e-05 (W 4.18594e-05) | 0.009773 ± 0.00020563 (W 0.000198949) | 🔵 tlinalg-pool 1.23× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.160518 ± 0.0011965 (W 0.00182112) | 0.405117 ± 0.00300999 (W 0.00285939) | 🔵 tlinalg-pool 2.52× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.321968 ± 0.00733412 (W 0.00227619) | 0.436812 ± 0.00224565 (W 0.0032091) | 🔵 tlinalg-pool 1.36× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n128/b1` | 0.219212 ± 0.00177031 (W 0.00195326) | 0.405553 ± 0.00236996 (W 0.00340396) | 🔵 tlinalg-pool 1.85× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.253315 ± 0.000942247 (W 0.00208183) | 0.434641 ± 0.00172474 (W 0.00205019) | 🔵 tlinalg-pool 1.72× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.033838 ± 0.000161348 (W 0.000159423) | 0.025257 ± 0.000181292 (W 0.000241655) | 🔴 tlinalg-pool 1.34× slower than `lapack-mkl` |  |
| `solve/n128/b1` | 0.277134 ± 0.00173591 (W 0.00158139) | 0.448612 ± 0.00209856 (W 0.00334157) | 🔵 tlinalg-pool 1.62× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 1.47441 ± 0.00310378 (W 0.00210003) | 1.87705 ± 0.00559179 (W 0.00509176) | 🔵 tlinalg-pool 1.27× faster than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.0202525 ± 0.000170177 (W 0.000135064) | 0.0128685 ± 0.000132414 (W 9.70445e-05) | 🔴 tlinalg-pool 1.57× slower than `lapack-mkl` |  |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 27.4738 ± 0.0563774 (W 0.0339181) | 14.7972 ± 0.0855144 (W 0.0394975) | 🔴 tlinalg-pool 1.86× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 16.4032 ± 0.058584 (W 0.0195112) | 12.1463 ± 0.0371633 (W 0.0164584) | 🔴 tlinalg-pool 1.35× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 1.59774 ± 0.00381379 (W 0.00369377) | 3.15687 ± 0.0173248 (W 0.0113455) | 🔵 tlinalg-pool 1.98× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 1.84929 ± 0.00988124 (W 0.00247655) | 2.12667 ± 0.00747398 (W 0.00489313) | 🔵 tlinalg-pool 1.15× faster than `lapack-mkl` |  |
| `qr/n512/b1` | 5.53346 ± 0.025967 (W 0.00820808) | 8.72886 ± 0.0579293 (W 0.0151971) | 🔵 tlinalg-pool 1.58× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 6.75077 ± 0.0306744 (W 0.0168998) | 24.4183 ± 0.120216 (W 0.0416585) | 🔵 tlinalg-pool 3.62× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 38.5014 ± 0.0894592 (W 0.0483642) | 48.629 ± 0.547267 (W 0.107363) | 🔵 tlinalg-pool 1.26× faster than `lapack-mkl` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 37.239 ± 0.0486318 (W 0.0445833) | 65.6223 ± 0.166345 (W 0.0382979) | 🔵 tlinalg-pool 1.76× faster than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 20.4405 ± 0.0299368 (W 0.0257485) | 28.0051 ± 0.0697041 (W 0.0320551) | 🔵 tlinalg-pool 1.37× faster than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 5.64474 ± 0.0182834 (W 0.0105379) | 8.22309 ± 0.0216757 (W 0.0132105) | 🔵 tlinalg-pool 1.46× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 5.26644 ± 0.0221716 (W 0.0113588) | 5.50302 ± 0.019781 (W 0.00920332) | · |  |
| `qr/n512/b1` | 13.2016 ± 0.0448342 (W 0.0159747) | 15.4331 ± 0.0478059 (W 0.0273575) | 🔵 tlinalg-pool 1.17× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 14.2815 ± 0.0232676 (W 0.0218404) | 59.1693 ± 0.403852 (W 0.139036) | 🔵 tlinalg-pool 4.14× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 75.8311 ± 0.134335 (W 0.122135) | 86.3747 ± 0.848109 (W 0.643391) | 🔵 tlinalg-pool 1.14× faster than `lapack-mkl` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 6.01493 ± 0.0439439 (W 0.0111476) | 6.23455 ± 0.00943519 (W 0.043483) | · |  |
| `qr/4096x256/b1` | 22.4006 ± 0.313193 (W 0.086658) | 18.2284 ± 0.190078 (W 0.0831052) | 🔴 tlinalg-pool 1.23× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 21.7024 ± 0.0399421 (W 0.0529407) | 56.27 ± 1.30057 (W 1.01239) | 🔵 tlinalg-pool 2.59× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/4096x256/b1` | 35.1677 ± 0.0746121 (W 0.0546528) | 34.1378 ± 0.0932472 (W 0.059167) | · |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 17.7569 ± 0.0756208 (W 0.0373886) | 16.8929 ± 0.116388 (W 0.0968582) | · |  |
| `qr/4096x256/b1` | 58.7002 ± 0.16483 (W 0.120004) | 40.6364 ± 0.208148 (W 0.23166) | 🔴 tlinalg-pool 1.44× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 58.6503 ± 0.500407 (W 0.185234) | 155.816 ± 2.07293 (W 0.435231) | 🔵 tlinalg-pool 2.66× faster than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 108.93 ± 0.267681 (W 0.203813) | 75.3067 ± 0.481383 (W 0.535393) | 🔴 tlinalg-pool 1.45× slower than `lapack-mkl` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
