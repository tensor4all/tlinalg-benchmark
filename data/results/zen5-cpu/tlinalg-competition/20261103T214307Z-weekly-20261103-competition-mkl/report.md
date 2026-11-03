# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `3635d96231122648fe3f239027d9f29065331a4c`
- toolkit commit: `74e50e8199cb2c2f07e810744a0943fc3a8c1170`
- measured binary SHA-256: `f9de3c2ea11208f98dfddae328c2a2b5c15bdc311582ad4269a4c6dda4ca4673`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-03T22:03:17.695594Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor mkl --aa 4 --reps 5 --prime-ms 250 --label weekly-20261103-competition-mkl --no-publish`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261103T214307Z-weekly-20261103-competition-mkl/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.32%, worst 38.77% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 31 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.30%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.120955 ± 0.0017151 (W 0.00147127) | 1.07467 ± 0.0155119 (W 0.00572825) | 🔵 tlinalg-pool 8.88× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.483636 ± 0.00494415 (W 0.00415732) | 3.80996 ± 0.0369737 (W 0.0145463) | 🔵 tlinalg-pool 7.88× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.18277 ± 0.000786624 (W 0.00163165) | 0.126004 ± 0.00228673 (W 0.000211605) | 🔴 tlinalg-pool 1.45× slower than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.0488105 ± 0.00141413 (W 0.000110414) | 0.32707 ± 0.00436879 (W 0.00217594) | 🔵 tlinalg-pool 6.70× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eig/n16/b1024` | 12.0336 ± 0.6907 (W 0.0208422) | 52.7657 ± 0.13596 (W 0.0383881) | 🔵 tlinalg-pool 4.38× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eig/n32/b1024` | 54.1643 ± 0.379472 (W 0.0431636) | 284.675 ± 1.10932 (W 0.415777) | 🔵 tlinalg-pool 5.26× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 0.822472 ± 0.0110581 (W 0.00255896) | 2.84303 ± 0.0204768 (W 0.0057808) | 🔵 tlinalg-pool 3.46× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 3.02176 ± 0.0269125 (W 0.00663752) | 11.7478 ± 0.0167044 (W 0.0139348) | 🔵 tlinalg-pool 3.89× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 3.74202 ± 0.012955 (W 0.00690147) | 23.8107 ± 0.0748876 (W 0.0363341) | 🔵 tlinalg-pool 6.36× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 13.9791 ± 0.062226 (W 0.0116081) | 98.26 ± 0.233591 (W 0.216348) | 🔵 tlinalg-pool 7.03× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.324784 ± 0.00187443 (W 0.00221383) | 2.96888 ± 0.00858683 (W 0.00847341) | 🔵 tlinalg-pool 9.14× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.0925 ± 0.00198113 (W 0.00200606) | 7.89638 ± 0.0392312 (W 0.0231772) | 🔵 tlinalg-pool 7.23× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 8.27316 ± 0.0339954 (W 0.0082852) | 36.5615 ± 0.11876 (W 0.0576662) | 🔵 tlinalg-pool 4.42× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 36.4525 ± 0.145607 (W 0.0753322) | 172.422 ± 0.496298 (W 0.179138) | 🔵 tlinalg-pool 4.73× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.442497 ± 0.00259668 (W 0.00274563) | 2.10513 ± 0.00586789 (W 0.00269064) | 🔵 tlinalg-pool 4.76× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 1.97932 ± 0.00616011 (W 0.0052323) | 9.02482 ± 0.0347454 (W 0.00793849) | 🔵 tlinalg-pool 4.56× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 2.81083 ± 0.0139182 (W 0.00194089) | 12.7025 ± 0.0406679 (W 0.0158539) | 🔵 tlinalg-pool 4.52× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 10.5662 ± 0.0438775 (W 0.0104513) | 41.4682 ± 0.150174 (W 0.0352186) | 🔵 tlinalg-pool 3.92× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.256122 ± 0.0021055 (W 0.00183106) | 1.55673 ± 0.011563 (W 0.0039223) | 🔵 tlinalg-pool 6.08× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.861753 ± 0.00658855 (W 0.00178231) | 4.46983 ± 0.0142241 (W 0.0109891) | 🔵 tlinalg-pool 5.19× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.514763 ± 0.0050883 (W 0.00366535) | 3.91154 ± 0.0329198 (W 0.0168781) | 🔵 tlinalg-pool 7.60× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 2.04637 ± 0.0367019 (W 0.0130032) | 26.2101 ± 0.0897802 (W 0.0290886) | 🔵 tlinalg-pool 12.81× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.505686 ± 0.0139888 (W 0.00331995) | 0.409616 ± 0.0102034 (W 0.00337737) | 🔴 tlinalg-pool 1.23× slower than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.177421 ± 0.00151755 (W 0.00194059) | 1.00975 ± 0.00611177 (W 0.00348101) | 🔵 tlinalg-pool 5.69× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.496919 ± 0.0046325 (W 0.00314973) | 5.66029 ± 0.050232 (W 0.0106831) | 🔵 tlinalg-pool 11.39× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 1.60152 ± 0.00655465 (W 0.00740945) | 29.2141 ± 0.0984582 (W 0.0340487) | 🔵 tlinalg-pool 18.24× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.0824635 ± 0.000836095 (W 0.00112566) | 0.998079 ± 0.00255574 (W 0.00165585) | 🔵 tlinalg-pool 12.10× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.194552 ± 0.00227569 (W 0.00168005) | 1.86294 ± 0.0117383 (W 0.00437017) | 🔵 tlinalg-pool 9.58× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.591166 ± 0.024437 (W 0.00150327) | 2.66779 ± 0.0252305 (W 0.0172513) | 🔵 tlinalg-pool 4.51× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 2.39945 ± 0.0674938 (W 0.00394243) | 13.3364 ± 0.0866467 (W 0.038708) | 🔵 tlinalg-pool 5.56× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.050725 ± 0.00303622 (W 0.000120285) | 0.320511 ± 0.0025643 (W 0.0019929) | 🔵 tlinalg-pool 6.32× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.158289 ± 0.00778128 (W 0.000790091) | 0.790756 ± 0.00544473 (W 0.00645698) | 🔵 tlinalg-pool 5.00× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.501684 ± 0.00907142 (W 0.00244252) | 2.95468 ± 0.018414 (W 0.00218066) | 🔵 tlinalg-pool 5.89× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 1.65831 ± 0.0249873 (W 0.00368227) | 12.0538 ± 0.0815975 (W 0.0249257) | 🔵 tlinalg-pool 7.27× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.064375 ± 0.000423722 (W 0.000877472) | 0.336947 ± 0.00190511 (W 0.00224964) | 🔵 tlinalg-pool 5.23× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.164982 ± 0.0048787 (W 0.00164367) | 0.865417 ± 0.00671791 (W 0.00197266) | 🔵 tlinalg-pool 5.25× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n16/b1024` | 0.37883 ± 0.00697285 (W 0.00287344) | 1.77272 ± 0.036273 (W 0.00612991) | 🔵 tlinalg-pool 4.68× faster than `lapack-mkl` |  |
| `lu/n32/b1024` | 1.31432 ± 0.0102145 (W 0.00651458) | 12.8896 ± 0.0580129 (W 0.0241456) | 🔵 tlinalg-pool 9.81× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.317445 ± 0.0084898 (W 0.00317843) | 0.224573 ± 0.0277698 (W 0.00231188) | 🔴 tlinalg-pool 1.41× slower than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu/n8/b1024` | 0.135873 ± 0.00136054 (W 0.00167325) | 0.565298 ± 0.0118494 (W 0.00414698) | 🔵 tlinalg-pool 4.16× faster than `lapack-mkl` |  |
| `lu_factor/n16/b1024` | 0.242617 ± 0.00485831 (W 0.00184703) | 1.28405 ± 0.0350237 (W 0.00299987) | 🔵 tlinalg-pool 5.29× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 0.699021 ± 0.0109865 (W 0.0042332) | 10.1558 ± 0.0327576 (W 0.0180663) | 🔵 tlinalg-pool 14.53× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.240638 ± 0.00302066 (W 0.0023194) | 0.17469 ± 0.00356232 (W 0.0025238) | 🔴 tlinalg-pool 1.38× slower than `lapack-mkl` |  |
| `lu_factor/n8/b1024` | 0.0984635 ± 0.000383563 (W 0.00168125) | 0.362955 ± 0.00596422 (W 0.00265194) | 🔵 tlinalg-pool 3.69× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.327786 ± 0.00696429 (W 0.0032425) | 2.40588 ± 0.0266781 (W 0.0089501) | 🔵 tlinalg-pool 7.34× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n32/b1024` | 0.878133 ± 0.00928217 (W 0.00295778) | 14.8428 ± 0.0791359 (W 0.0168358) | 🔵 tlinalg-pool 16.90× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.0572815 ± 0.000870805 (W 0.00127776) | 0.274361 ± 0.00299578 (W 0.00232228) | 🔵 tlinalg-pool 4.79× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.117689 ± 0.00198635 (W 0.00111552) | 0.921175 ± 0.0162419 (W 0.00268493) | 🔵 tlinalg-pool 7.83× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.0978025 ± 0.00109382 (W 0.000225816) | 1.06821 ± 0.00387297 (W 0.00548844) | 🔵 tlinalg-pool 10.92× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.231486 ± 0.00273316 (W 0.00209683) | 4.44219 ± 0.0391275 (W 0.0115156) | 🔵 tlinalg-pool 19.19× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.020929 ± 7.21359e-05 (W 5.05595e-05) | 0.13401 ± 0.000484598 (W 0.000782474) | 🔵 tlinalg-pool 6.40× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.044152 ± 0.000176878 (W 0.00137179) | 0.610781 ± 0.00202943 (W 0.00308723) | 🔵 tlinalg-pool 13.83× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.12874 ± 0.0282288 (W 0.00169746) | 5.28848 ± 0.0134479 (W 0.0118594) | 🔵 tlinalg-pool 4.69× faster than `lapack-mkl` | `!` between-start range over 5% |
| `qr/n32/b1024` | 4.3178 ± 0.00744641 (W 0.00977805) | 20.9252 ± 0.169574 (W 0.0458362) | 🔵 tlinalg-pool 4.85× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.0980675 ± 0.000872469 (W 0.00128454) | 0.705915 ± 0.00372036 (W 0.00272368) | 🔵 tlinalg-pool 7.20× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.313207 ± 0.00549768 (W 0.00232827) | 1.68934 ± 0.0102206 (W 0.0055298) | 🔵 tlinalg-pool 5.39× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.34493 ± 0.0285619 (W 0.00344303) | 8.89552 ± 0.0107374 (W 0.0164047) | 🔵 tlinalg-pool 6.61× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 4.48354 ± 0.0367018 (W 0.00448865) | 30.9149 ± 0.0707985 (W 0.0402236) | 🔵 tlinalg-pool 6.90× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.169516 ± 0.00179033 (W 0.00130044) | 1.42828 ± 0.00480001 (W 0.00679744) | 🔵 tlinalg-pool 8.43× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.433606 ± 0.00245154 (W 0.00232338) | 3.35501 ± 0.0131301 (W 0.0121671) | 🔵 tlinalg-pool 7.74× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.35256 ± 0.00783463 (W 0.00227266) | 2.54509 ± 0.0591848 (W 0.0077059) | 🔵 tlinalg-pool 7.22× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 0.951337 ± 0.0108968 (W 0.0019478) | 15.1624 ± 0.0307995 (W 0.0303936) | 🔵 tlinalg-pool 15.94× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.053905 ± 0.000416582 (W 0.000288165) | 0.339132 ± 0.00383765 (W 0.00201057) | 🔵 tlinalg-pool 6.29× faster than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.124306 ± 0.00110498 (W 0.00163882) | 1.01741 ± 0.0127756 (W 0.00242952) | 🔵 tlinalg-pool 8.18× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 6.94467 ± 0.156506 (W 0.00852884) | 52.2529 ± 0.148864 (W 0.0990093) | 🔵 tlinalg-pool 7.52× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 24.9479 ± 0.683724 (W 0.0271822) | 194.113 ± 0.27098 (W 0.159072) | 🔵 tlinalg-pool 7.78× faster than `lapack-mkl` |  |
| `svd_full/n4/b1024` | 0.549669 ± 0.0194773 (W 0.00153137) | 6.30482 ± 0.0232476 (W 0.00876423) | 🔵 tlinalg-pool 11.47× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 1.93207 ± 0.154547 (W 0.00456719) | 19.0226 ± 0.0528677 (W 0.0233945) | 🔵 tlinalg-pool 9.85× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 6.81555 ± 0.102815 (W 0.0114371) | 52.4929 ± 0.277001 (W 0.221439) | 🔵 tlinalg-pool 7.70× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 25.0704 ± 1.39973 (W 0.0224073) | 193.458 ± 0.746601 (W 0.247868) | 🔵 tlinalg-pool 7.72× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.546047 ± 0.0176323 (W 0.00172407) | 6.35669 ± 0.0551599 (W 0.0111548) | 🔵 tlinalg-pool 11.64× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 1.87913 ± 0.0129569 (W 0.00298448) | 19.0574 ± 0.214152 (W 0.013221) | 🔵 tlinalg-pool 10.14× faster than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 2.79692 ± 0.0157557 (W 0.00178057) | 19.615 ± 0.204626 (W 0.0154368) | 🔵 tlinalg-pool 7.01× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 9.25199 ± 0.0557279 (W 0.0119197) | 63.4573 ± 0.337744 (W 0.0690892) | 🔵 tlinalg-pool 6.86× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.366638 ± 0.00138706 (W 0.00436847) | 2.90982 ± 0.0145312 (W 0.00559973) | 🔵 tlinalg-pool 7.94× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 0.993362 ± 0.00523067 (W 0.000970798) | 7.08299 ± 0.0411342 (W 0.00717195) | 🔵 tlinalg-pool 7.13× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.069454 ± 0.000459795 (W 0.000534651) | 0.546593 ± 0.00250249 (W 0.00519631) | 🔵 tlinalg-pool 7.87× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.155814 ± 0.00237521 (W 0.00225098) | 2.65733 ± 0.0222255 (W 0.00630679) | 🔵 tlinalg-pool 17.05× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.014251 ± 7.68782e-05 (W 0.000126247) | 0.276049 ± 0.001287 (W 0.00263804) | 🔵 tlinalg-pool 19.37× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.030913 ± 0.000201064 (W 0.000227161) | 0.355417 ± 0.00396463 (W 0.00240632) | 🔵 tlinalg-pool 11.50× faster than `lapack-mkl` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.168509 ± 0.000916397 (W 0.000837865) | 1.78979 ± 0.0083744 (W 0.0165217) | 🔵 tlinalg-pool 10.62× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.805202 ± 0.00289154 (W 0.00617083) | 8.69864 ± 0.0404379 (W 0.0153371) | 🔵 tlinalg-pool 10.80× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.027852 ± 0.000221867 (W 8.31999e-05) | 0.175667 ± 0.000849666 (W 0.00162608) | 🔵 tlinalg-pool 6.31× faster than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.056821 ± 0.000844925 (W 0.000868814) | 0.47961 ± 0.00148163 (W 0.00280835) | 🔵 tlinalg-pool 8.44× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 16.4318 ± 0.104937 (W 0.0162699) | 179.482 ± 0.23212 (W 0.279931) | 🔵 tlinalg-pool 10.92× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 67.7334 ± 0.542347 (W 0.036814) | 826.584 ± 3.53366 (W 1.99919) | 🔵 tlinalg-pool 12.20× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 1.35724 ± 0.00558811 (W 0.00480691) | 12.1373 ± 0.0537977 (W 0.0154153) | 🔵 tlinalg-pool 8.94× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 4.51563 ± 0.0321368 (W 0.0104698) | 42.6236 ± 0.174418 (W 0.0455607) | 🔵 tlinalg-pool 9.44× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 4.0178 ± 0.0130801 (W 0.00501962) | 32.093 ± 0.164759 (W 0.0328765) | 🔵 tlinalg-pool 7.99× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 17.5588 ± 0.0314137 (W 0.194315) | 147.918 ± 0.564755 (W 0.238454) | 🔵 tlinalg-pool 8.42× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.382085 ± 0.00248402 (W 0.00168955) | 2.88735 ± 0.0058819 (W 0.00652656) | 🔵 tlinalg-pool 7.56× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.16947 ± 0.00561591 (W 0.00273345) | 8.93525 ± 0.0207952 (W 0.0121412) | 🔵 tlinalg-pool 7.64× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 9.84564 ± 0.365369 (W 0.017306) | 124.876 ± 0.282793 (W 0.134192) | 🔵 tlinalg-pool 12.68× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigvals/n32/b1024` | 42.8924 ± 0.0870964 (W 0.0392469) | 542.249 ± 0.577041 (W 1.02344) | 🔵 tlinalg-pool 12.64× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.657628 ± 0.0233488 (W 0.00209317) | 9.469 ± 0.0279371 (W 0.017755) | 🔵 tlinalg-pool 14.40× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigvals/n8/b1024` | 2.54357 ± 0.0403798 (W 0.00306941) | 33.6865 ± 0.0597557 (W 0.026058) | 🔵 tlinalg-pool 13.24× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 3.00124 ± 0.00613953 (W 0.00509577) | 17.3968 ± 0.263879 (W 0.0295677) | 🔵 tlinalg-pool 5.80× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 11.4696 ± 0.0465711 (W 0.0137246) | 71.9377 ± 0.36592 (W 0.0784) | 🔵 tlinalg-pool 6.27× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.311495 ± 0.00236407 (W 0.00205787) | 1.73799 ± 0.00399848 (W 0.00244651) | 🔵 tlinalg-pool 5.58× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.942523 ± 0.00442556 (W 0.00169849) | 5.27986 ± 0.0267427 (W 0.00979861) | 🔵 tlinalg-pool 5.60× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.659075 ± 0.00198637 (W 0.00795517) | 5.54386 ± 0.0604438 (W 0.0201119) | 🔵 tlinalg-pool 8.41× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 3.06582 ± 0.00628757 (W 0.015491) | 27.3606 ± 0.152626 (W 0.0268244) | 🔵 tlinalg-pool 8.92× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.0888555 ± 0.00283495 (W 0.0012987) | 0.527106 ± 0.00140848 (W 0.0028283) | 🔵 tlinalg-pool 5.93× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.21249 ± 0.0028682 (W 0.00242933) | 1.29451 ± 0.0187618 (W 0.00318511) | 🔵 tlinalg-pool 6.09× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.771821 ± 0.0040599 (W 0.00446879) | 8.63292 ± 0.0568698 (W 0.0124154) | 🔵 tlinalg-pool 11.19× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 2.77271 ± 0.0264595 (W 0.00946314) | 35.5997 ± 0.0914797 (W 0.0402207) | 🔵 tlinalg-pool 12.84× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.125825 ± 0.000274489 (W 0.00138279) | 1.4826 ± 0.0269188 (W 0.00594127) | 🔵 tlinalg-pool 11.78× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.289518 ± 0.00137577 (W 0.00239776) | 3.08901 ± 0.0383993 (W 0.00649376) | 🔵 tlinalg-pool 10.67× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.634977 ± 0.00856833 (W 0.00539366) | 6.46515 ± 0.0509716 (W 0.0223653) | 🔵 tlinalg-pool 10.18× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 3.5234 ± 0.0221208 (W 0.00760019) | 38.6208 ± 0.324245 (W 0.073361) | 🔵 tlinalg-pool 10.96× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.052121 ± 0.00133015 (W 0.0001039) | 0.471245 ± 0.00234172 (W 0.00352705) | 🔵 tlinalg-pool 9.04× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.15033 ± 0.00174912 (W 0.00230195) | 1.43105 ± 0.0108572 (W 0.0229002) | 🔵 tlinalg-pool 9.52× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1024` | 0.599107 ± 0.00527325 (W 0.00279502) | 6.25392 ± 0.0149829 (W 0.00822167) | 🔵 tlinalg-pool 10.44× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 2.54237 ± 0.00938986 (W 0.00722342) | 26.7563 ± 0.410656 (W 0.0346486) | 🔵 tlinalg-pool 10.52× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.0792275 ± 0.000257993 (W 0.00149307) | 0.527451 ± 0.00196707 (W 0.00322793) | 🔵 tlinalg-pool 6.66× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.200158 ± 0.000700859 (W 0.00180153) | 1.48978 ± 0.00312464 (W 0.00524063) | 🔵 tlinalg-pool 7.44× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.450944 ± 0.00275859 (W 0.00667725) | 3.49264 ± 0.0408083 (W 0.0139416) | 🔵 tlinalg-pool 7.75× faster than `lapack-mkl` |  |
| `lu/n32/b1024` | 2.15831 ± 0.00726478 (W 0.0108028) | 19.3992 ± 0.0455943 (W 0.0273081) | 🔵 tlinalg-pool 8.99× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.066504 ± 0.00104138 (W 0.000792914) | 0.294402 ± 0.00264267 (W 0.00254764) | 🔵 tlinalg-pool 4.43× faster than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.141363 ± 0.0036953 (W 0.00274419) | 0.88366 ± 0.0192376 (W 0.00290049) | 🔵 tlinalg-pool 6.25× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.286894 ± 0.00446445 (W 0.00185312) | 2.42063 ± 0.028336 (W 0.00742432) | 🔵 tlinalg-pool 8.44× faster than `lapack-mkl` |  |
| `lu_factor/n32/b1024` | 1.21052 ± 0.0104086 (W 0.00778339) | 15.2291 ± 0.112563 (W 0.0323207) | 🔵 tlinalg-pool 12.58× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.05892 ± 0.000513518 (W 0.000527769) | 0.199286 ± 0.003253 (W 0.00176458) | 🔵 tlinalg-pool 3.38× faster than `lapack-mkl` |  |
| `lu_factor/n8/b1024` | 0.103948 ± 0.00207055 (W 0.00124459) | 0.598949 ± 0.00420492 (W 0.00305846) | 🔵 tlinalg-pool 5.76× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.453203 ± 0.00517343 (W 0.00316598) | 5.05946 ± 0.0346087 (W 0.00530358) | 🔵 tlinalg-pool 11.16× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 1.68551 ± 0.016367 (W 0.00820385) | 20.8015 ± 0.0939137 (W 0.0137775) | 🔵 tlinalg-pool 12.34× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.072996 ± 0.00096128 (W 0.00119804) | 0.517974 ± 0.0023257 (W 0.00250986) | 🔵 tlinalg-pool 7.10× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.161145 ± 0.0010809 (W 0.00144585) | 1.5291 ± 0.0119191 (W 0.00349381) | 🔵 tlinalg-pool 9.49× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.184879 ± 0.0023192 (W 0.00077608) | 2.5812 ± 0.0235965 (W 0.00833177) | 🔵 tlinalg-pool 13.96× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.885417 ± 0.00722754 (W 0.00584655) | 5.621 ± 0.0360462 (W 0.0290967) | 🔵 tlinalg-pool 6.35× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.0330515 ± 6.99065e-05 (W 0.000211156) | 0.324624 ± 0.0020956 (W 0.00190214) | 🔵 tlinalg-pool 9.82× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.0759765 ± 0.000374585 (W 0.00199612) | 0.943873 ± 0.00406845 (W 0.00219883) | 🔵 tlinalg-pool 12.42× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.40783 ± 0.00796292 (W 0.00271435) | 10.8054 ± 0.0407102 (W 0.0122574) | 🔵 tlinalg-pool 7.68× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 9.14157 ± 0.0304051 (W 0.0158318) | 49.4998 ± 0.317031 (W 0.0539723) | 🔵 tlinalg-pool 5.41× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.117158 ± 0.000719275 (W 0.000179458) | 0.983421 ± 0.00882319 (W 0.00381091) | 🔵 tlinalg-pool 8.39× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.343332 ± 0.00218216 (W 0.00202832) | 2.79404 ± 0.0114146 (W 0.00445782) | 🔵 tlinalg-pool 8.14× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.60779 ± 0.308161 (W 0.003356) | 15.8476 ± 0.0682686 (W 0.0341344) | 🔵 tlinalg-pool 9.86× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `rank_revealing_qr/n32/b1024` | 8.51358 ± 0.021561 (W 0.0185382) | 67.8314 ± 0.526385 (W 0.242872) | 🔵 tlinalg-pool 7.97× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.199335 ± 0.0023435 (W 0.0015792) | 1.90057 ± 0.00914527 (W 0.00552854) | 🔵 tlinalg-pool 9.53× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.498311 ± 0.00198636 (W 0.00211613) | 4.96491 ± 0.0216475 (W 0.0132537) | 🔵 tlinalg-pool 9.96× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.501734 ± 0.00286559 (W 0.00257202) | 5.28924 ± 0.0522604 (W 0.010025) | 🔵 tlinalg-pool 10.54× faster than `lapack-mkl` |  |
| `solve/n32/b1024` | 1.83653 ± 0.0271907 (W 0.0147337) | 21.402 ± 0.0948495 (W 0.0235868) | 🔵 tlinalg-pool 11.65× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.0768785 ± 0.00118216 (W 0.00127903) | 0.591555 ± 0.00273929 (W 0.00299324) | 🔵 tlinalg-pool 7.69× faster than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.189387 ± 0.00199266 (W 0.00210825) | 1.63983 ± 0.0179345 (W 0.00534816) | 🔵 tlinalg-pool 8.66× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 7.30236 ± 0.0902128 (W 0.00873147) | 67.6191 ± 0.173325 (W 0.0852742) | 🔵 tlinalg-pool 9.26× faster than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 31.2825 ± 0.342858 (W 0.0277234) | 280.426 ± 0.540416 (W 0.555727) | 🔵 tlinalg-pool 8.96× faster than `lapack-mkl` |  |
| `svd_full/n4/b1024` | 0.678904 ± 0.0284787 (W 0.00243963) | 7.5335 ± 0.012449 (W 0.016213) | 🔵 tlinalg-pool 11.10× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 2.08725 ± 0.0055352 (W 0.00424964) | 22.2434 ± 0.0195487 (W 0.0384903) | 🔵 tlinalg-pool 10.66× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 7.31479 ± 0.0536453 (W 0.0645619) | 67.5574 ± 0.146075 (W 0.279984) | 🔵 tlinalg-pool 9.24× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 31.3896 ± 0.78963 (W 0.0211836) | 280.347 ± 1.13259 (W 0.402504) | 🔵 tlinalg-pool 8.93× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.65569 ± 0.0128237 (W 0.00201098) | 7.52421 ± 0.0284882 (W 0.00699964) | 🔵 tlinalg-pool 11.48× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 2.10362 ± 0.0507309 (W 0.00448018) | 22.2947 ± 0.0946231 (W 0.0205173) | 🔵 tlinalg-pool 10.60× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 3.19026 ± 0.0141731 (W 0.00525603) | 27.5898 ± 0.214969 (W 0.0505311) | 🔵 tlinalg-pool 8.65× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 11.558 ± 0.0129023 (W 0.0312524) | 102.454 ± 0.40458 (W 0.0519896) | 🔵 tlinalg-pool 8.86× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.4381 ± 0.00264855 (W 0.00253911) | 3.53689 ± 0.0294194 (W 0.00457468) | 🔵 tlinalg-pool 8.07× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.14204 ± 0.0024543 (W 0.00221652) | 8.91092 ± 0.0450367 (W 0.0109584) | 🔵 tlinalg-pool 7.80× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.128008 ± 0.000973701 (W 0.00195672) | 1.42752 ± 0.0102317 (W 0.00435543) | 🔵 tlinalg-pool 11.15× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.538548 ± 0.00221519 (W 0.00437867) | 3.39789 ± 0.0107926 (W 0.0108966) | 🔵 tlinalg-pool 6.31× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.023789 ± 9.33202e-05 (W 0.000146469) | 0.308604 ± 0.00104531 (W 0.00204249) | 🔵 tlinalg-pool 12.97× faster than `lapack-mkl` |  |
| `triangular_solve/n8/b1024` | 0.054136 ± 0.00101487 (W 0.000211691) | 0.643112 ± 0.0040159 (W 0.00357848) | 🔵 tlinalg-pool 11.88× faster than `lapack-mkl` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0734415 ± 0.000114398 (W 0.000397574) | 0.0932435 ± 0.000947767 (W 0.00162842) | 🔵 tlinalg-pool 1.27× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.178368 ± 0.00575743 (W 0.00165226) | 0.149844 ± 0.000501632 (W 0.00196064) | 🔴 tlinalg-pool 1.19× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n128/b1` | 0.093053 ± 0.000510649 (W 0.000414989) | 0.135617 ± 0.00106258 (W 0.00195247) | 🔵 tlinalg-pool 1.46× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.104319 ± 0.000515306 (W 0.000408032) | 0.157418 ± 0.000549105 (W 0.000525362) | 🔵 tlinalg-pool 1.51× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.011511 ± 0.000117062 (W 5.94946e-05) | 0.016371 ± 7.7816e-05 (W 0.000325196) | 🔵 tlinalg-pool 1.42× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.121506 ± 0.00104307 (W 0.000899374) | 0.164521 ± 0.000426007 (W 0.00218584) | 🔵 tlinalg-pool 1.35× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 1.15191 ± 0.00404322 (W 0.0018115) | 1.11061 ± 0.00197052 (W 0.00313167) | · |  |
| `triangular_solve/n128/b1` | 0.008055 ± 9.91211e-05 (W 4.38312e-05) | 0.009668 ± 5.37742e-05 (W 0.000189805) | 🔵 tlinalg-pool 1.20× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.159811 ± 0.000905257 (W 0.00175406) | 0.406571 ± 0.00223866 (W 0.00372907) | 🔵 tlinalg-pool 2.54× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.316188 ± 0.0067927 (W 0.00235695) | 0.436737 ± 0.000830943 (W 0.00279855) | 🔵 tlinalg-pool 1.38× faster than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.219057 ± 0.00139688 (W 0.00167229) | 0.403185 ± 0.00103663 (W 0.00266989) | 🔵 tlinalg-pool 1.84× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.253847 ± 0.00192177 (W 0.00188942) | 0.433036 ± 0.000524288 (W 0.00248969) | 🔵 tlinalg-pool 1.71× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.0335925 ± 0.000187921 (W 0.000162629) | 0.0248815 ± 0.00015236 (W 0.000123687) | 🔴 tlinalg-pool 1.35× slower than `lapack-mkl` |  |
| `solve/n128/b1` | 0.278737 ± 0.00264229 (W 0.00246449) | 0.449207 ± 0.00244018 (W 0.00236184) | 🔵 tlinalg-pool 1.61× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 1.48094 ± 0.00633509 (W 0.00403542) | 1.87943 ± 0.00631535 (W 0.00841599) | 🔵 tlinalg-pool 1.27× faster than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.0201575 ± 0.000213171 (W 0.000159065) | 0.012984 ± 4.19325e-05 (W 0.000107018) | 🔴 tlinalg-pool 1.55× slower than `lapack-mkl` |  |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 27.5328 ± 0.0421374 (W 0.0235954) | 14.6925 ± 0.0662355 (W 0.0394777) | 🔴 tlinalg-pool 1.87× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 16.3442 ± 0.062413 (W 0.214812) | 12.1164 ± 0.0212618 (W 0.0201074) | 🔴 tlinalg-pool 1.35× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 1.58973 ± 0.00608916 (W 0.00257898) | 3.17298 ± 0.0102855 (W 0.0206233) | 🔵 tlinalg-pool 2.00× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 1.8437 ± 0.00484271 (W 0.00595247) | 2.12549 ± 0.00431549 (W 0.00540744) | 🔵 tlinalg-pool 1.15× faster than `lapack-mkl` |  |
| `qr/n512/b1` | 5.5337 ± 0.0191653 (W 0.00926393) | 8.67117 ± 0.0554498 (W 0.017193) | 🔵 tlinalg-pool 1.57× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 6.7373 ± 0.0228987 (W 0.0135082) | 24.376 ± 0.0863528 (W 0.0408677) | 🔵 tlinalg-pool 3.62× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 38.6369 ± 0.0553216 (W 0.042751) | 48.2276 ± 0.301584 (W 0.0656353) | 🔵 tlinalg-pool 1.25× faster than `lapack-mkl` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 37.1823 ± 0.0457946 (W 0.0243504) | 65.1183 ± 0.230796 (W 0.0741523) | 🔵 tlinalg-pool 1.75× faster than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 20.4861 ± 0.0501875 (W 0.0190408) | 27.8126 ± 0.0593969 (W 0.0168956) | 🔵 tlinalg-pool 1.36× faster than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 5.63432 ± 0.0120277 (W 0.0100609) | 8.22881 ± 0.0222215 (W 0.0178493) | 🔵 tlinalg-pool 1.46× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 5.2401 ± 0.00722449 (W 0.00932026) | 5.51804 ± 0.00706765 (W 0.00904349) | 🔵 tlinalg-pool 1.05× faster than `lapack-mkl` |  |
| `qr/n512/b1` | 13.1883 ± 0.0560396 (W 0.0276351) | 15.3808 ± 0.0707622 (W 0.0310935) | 🔵 tlinalg-pool 1.17× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 14.2224 ± 0.0445429 (W 0.0237186) | 59.0037 ± 0.50397 (W 0.195118) | 🔵 tlinalg-pool 4.15× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 76.0492 ± 0.123324 (W 0.362239) | 85.0316 ± 0.843482 (W 0.0786804) | 🔵 tlinalg-pool 1.12× faster than `lapack-mkl` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 6.02102 ± 0.0606368 (W 0.0223276) | 6.217 ± 0.0248048 (W 0.0275257) | · |  |
| `qr/4096x256/b1` | 22.4342 ± 0.0596416 (W 0.0486318) | 18.0197 ± 0.0690144 (W 0.0436828) | 🔴 tlinalg-pool 1.24× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 21.6491 ± 0.082253 (W 0.254747) | 55.8855 ± 0.801846 (W 0.663394) | 🔵 tlinalg-pool 2.58× faster than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 35.2783 ± 0.0359939 (W 0.253108) | 33.8388 ± 0.262422 (W 0.0795435) | · |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 17.6687 ± 0.105691 (W 0.0403548) | 16.9265 ± 0.0249969 (W 0.0675579) | · |  |
| `qr/4096x256/b1` | 58.542 ± 0.0356871 (W 0.0996441) | 40.4829 ± 0.122622 (W 0.216268) | 🔴 tlinalg-pool 1.45× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 58.5495 ± 0.278176 (W 0.136693) | 155.203 ± 1.69604 (W 0.35163) | 🔵 tlinalg-pool 2.65× faster than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 108.831 ± 0.185759 (W 0.207201) | 74.9593 ± 0.111167 (W 0.501479) | 🔴 tlinalg-pool 1.45× slower than `lapack-mkl` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
