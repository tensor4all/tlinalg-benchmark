<!-- generated from data/results/zen5-cpu/tlinalg-competition/20261020T175935Z-pub-mkl-corefixed/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `4dcd35f080a6b4fd6b1423871af66a33fd398482`
- features: `tlinalg-bench/link-mkl`
- faer provider: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `2f14740fac770401de0fc4c087051ccdbaacb651`
- toolkit commit: `b30708eaa5b5f288c9d4ec8ff9c0bda2389125d3`
- measured binary SHA-256: `1cc3ca9b16c76de0b3c25d4c027be838f28ec38f401c14c3a62df4b7006e20ec`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T18:30:29.448736Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor mkl --aa 4 --reps 5 --prime-ms 250 --label pub-mkl-corefixed`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261020T175935Z-pub-mkl-corefixed/`

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
- CPU sets: 8T -> `4-11`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 4 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.55%, worst 104.89% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 70 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.48%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

## batch-small, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.12276 ± 0.038072 (W 0.00162189) | 1.06652 ± 0.00912005 (W 0.00239685) | 🔵 tlinalg 8.69× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `cholesky/n32/b1024` | 0.470547 ± 0.0140421 (W 0.00725289) | 3.69057 ± 0.0500625 (W 0.026662) | 🔵 tlinalg 7.84× faster than `lapack-mkl` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.030046 ± 0.000444955 (W 0.000606569) | 0.122115 ± 0.00164579 (W 0.00122663) | 🔵 tlinalg 4.06× faster than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.0531695 ± 0.000445763 (W 0.000508365) | 0.322819 ± 0.00824485 (W 0.00241682) | 🔵 tlinalg 6.07× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eig/n16/b1024` | 11.927 ± 0.0403538 (W 0.0465504) | 52.9043 ± 0.0650311 (W 0.0464826) | 🔵 tlinalg 4.44× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 54.1599 ± 13.1113 (W 0.5141) | 284.271 ± 0.629282 (W 0.413017) | 🔵 tlinalg 5.25× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `eig/n4/b1024` | 0.784099 ± 0.00507472 (W 0.00330654) | 2.83596 ± 0.00652393 (W 0.00496057) | 🔵 tlinalg 3.62× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 2.95128 ± 0.00746645 (W 0.00472654) | 11.7127 ± 0.0513809 (W 0.0202346) | 🔵 tlinalg 3.97× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 3.74117 ± 0.0236769 (W 0.00626081) | 23.45 ± 0.029123 (W 0.023591) | 🔵 tlinalg 6.27× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 14.3456 ± 0.0180845 (W 0.0362957) | 100.491 ± 0.383975 (W 0.046744) | 🔵 tlinalg 7.00× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.31942 ± 0.00292232 (W 0.00191156) | 2.79224 ± 0.0303417 (W 0.00682503) | 🔵 tlinalg 8.74× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.0725 ± 0.00793258 (W 0.00241542) | 7.72627 ± 0.0138862 (W 0.0132638) | 🔵 tlinalg 7.20× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 8.174 ± 0.05106 (W 0.0157612) | 36.4501 ± 0.0678256 (W 0.222931) | 🔵 tlinalg 4.46× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 36.2856 ± 0.0444592 (W 0.0602832) | 169.447 ± 0.170364 (W 0.244445) | 🔵 tlinalg 4.67× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.410172 ± 0.00841306 (W 0.00304164) | 2.10636 ± 0.00164287 (W 0.00256714) | 🔵 tlinalg 5.14× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 1.93071 ± 0.00294126 (W 0.0020621) | 8.97997 ± 0.0303228 (W 0.0289784) | 🔵 tlinalg 4.65× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 2.79215 ± 0.0359172 (W 0.00461599) | 12.9534 ± 0.0234297 (W 0.0270214) | 🔵 tlinalg 4.64× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 10.9249 ± 0.0168719 (W 0.0386942) | 43.0858 ± 0.0645802 (W 0.0520674) | 🔵 tlinalg 3.94× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.25397 ± 0.00106625 (W 0.00284596) | 1.44779 ± 0.00294292 (W 0.00227395) | 🔵 tlinalg 5.70× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.858805 ± 0.00349265 (W 0.00384307) | 4.40172 ± 0.00823763 (W 0.00687978) | 🔵 tlinalg 5.13× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.47607 ± 0.00333019 (W 0.00591496) | 3.86814 ± 0.0265456 (W 0.00786037) | 🔵 tlinalg 8.13× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 1.99493 ± 0.0232258 (W 0.0318182) | 26.2636 ± 0.0727789 (W 0.138736) | 🔵 tlinalg 13.17× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.082185 ± 0.00108636 (W 0.00249055) | 0.402778 ± 0.0037201 (W 0.00192127) | 🔵 tlinalg 4.90× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 0.164994 ± 0.0026383 (W 0.00303356) | 0.972226 ± 0.0143659 (W 0.00214171) | 🔵 tlinalg 5.89× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.459816 ± 0.00785186 (W 0.00316492) | 5.81096 ± 0.0409797 (W 0.0142124) | 🔵 tlinalg 12.64× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 1.50617 ± 0.0290535 (W 0.00771586) | 29.7131 ± 0.130293 (W 0.0321304) | 🔵 tlinalg 19.73× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.0746 ± 0.00209381 (W 0.00076866) | 1.11515 ± 0.00882419 (W 0.00362106) | 🔵 tlinalg 14.95× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.17635 ± 0.0018782 (W 0.00242167) | 1.96185 ± 0.0252513 (W 0.00684394) | 🔵 tlinalg 11.12× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.608844 ± 0.0244564 (W 0.00281046) | 2.71009 ± 0.0456661 (W 0.0220863) | 🔵 tlinalg 4.45× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 2.48673 ± 0.0683522 (W 0.0168131) | 13.209 ± 0.341262 (W 0.0679007) | 🔵 tlinalg 5.31× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.0527995 ± 0.00142094 (W 0.000506823) | 0.323726 ± 0.0021642 (W 0.0026494) | 🔵 tlinalg 6.13× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.171376 ± 0.00974799 (W 0.00157056) | 0.796727 ± 0.00831383 (W 0.0111358) | 🔵 tlinalg 4.65× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.490409 ± 0.0151369 (W 0.0035615) | 2.96303 ± 0.0141281 (W 0.00542626) | 🔵 tlinalg 6.04× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n32/b1024` | 1.67126 ± 0.022802 (W 0.00908655) | 12.3354 ± 0.0918934 (W 0.0290936) | 🔵 tlinalg 7.38× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.063755 ± 0.00109281 (W 0.00147602) | 0.30652 ± 0.00105262 (W 0.00133245) | 🔵 tlinalg 4.81× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.16783 ± 0.00354927 (W 0.00114997) | 0.845263 ± 0.00382859 (W 0.00264689) | 🔵 tlinalg 5.04× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.36793 ± 0.00452255 (W 0.00503507) | 1.76424 ± 0.0501802 (W 0.00857052) | 🔵 tlinalg 4.80× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 1.32623 ± 0.0526449 (W 0.0190267) | 11.9124 ± 0.116667 (W 0.0325315) | 🔵 tlinalg 8.98× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n4/b1024` | 0.076218 ± 0.00105608 (W 0.00341667) | 0.167033 ± 0.00102226 (W 0.0018079) | 🔵 tlinalg 2.19× faster than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.14935 ± 0.00528518 (W 0.00378102) | 0.51046 ± 0.0187172 (W 0.00309239) | 🔵 tlinalg 3.42× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.265439 ± 0.000931109 (W 0.00378268) | 1.15492 ± 0.0428383 (W 0.00234865) | 🔵 tlinalg 4.35× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 0.753126 ± 0.0047915 (W 0.0052194) | 8.97607 ± 0.0415868 (W 0.0299781) | 🔵 tlinalg 11.92× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.0621265 ± 0.000898938 (W 0.00130227) | 0.0657085 ± 0.00071793 (W 0.00214573) | 🔵 tlinalg 1.06× faster than `lapack-mkl` |  |
| `lu_factor/n8/b1024` | 0.111119 ± 0.00213004 (W 0.00177144) | 0.262333 ± 0.0006303 (W 0.00205867) | 🔵 tlinalg 2.36× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.335338 ± 0.00489649 (W 0.00191024) | 2.32495 ± 0.00475253 (W 0.00524251) | 🔵 tlinalg 6.93× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 0.892638 ± 0.00630802 (W 0.00371891) | 13.7828 ± 0.1565 (W 0.0113793) | 🔵 tlinalg 15.44× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.064577 ± 0.00135247 (W 0.0019585) | 0.181061 ± 0.00141806 (W 0.00205604) | 🔵 tlinalg 2.80× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.130169 ± 0.00362869 (W 0.00480269) | 0.826369 ± 0.00375561 (W 0.00224291) | 🔵 tlinalg 6.35× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1024` | 0.130785 ± 0.000974345 (W 0.00144641) | 1.06872 ± 0.00615697 (W 0.00518017) | 🔵 tlinalg 8.17× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.313843 ± 0.0122362 (W 0.0132955) | 4.51435 ± 0.105988 (W 0.0103864) | 🔵 tlinalg 14.38× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.0330265 ± 0.00104736 (W 0.000836053) | 0.133356 ± 0.00141391 (W 0.00112711) | 🔵 tlinalg 4.04× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.0553335 ± 0.000607214 (W 0.000619482) | 0.587515 ± 0.00115457 (W 0.00231495) | 🔵 tlinalg 10.62× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.13941 ± 0.0192032 (W 0.00308949) | 5.26943 ± 0.0736761 (W 0.0151336) | 🔵 tlinalg 4.62× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 4.50263 ± 0.0167041 (W 0.011701) | 21.2 ± 0.0927276 (W 0.0827579) | 🔵 tlinalg 4.71× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.105708 ± 0.00112229 (W 0.00087872) | 0.723452 ± 0.0446376 (W 0.00277295) | 🔵 tlinalg 6.84× faster than `lapack-mkl` | `!` between-start range over 5% |
| `qr/n8/b1024` | 0.319414 ± 0.00501954 (W 0.00249357) | 1.70532 ± 0.0342946 (W 0.00451374) | 🔵 tlinalg 5.34× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.31468 ± 0.0808588 (W 0.00675199) | 8.36527 ± 0.0612889 (W 0.0534111) | 🔵 tlinalg 6.36× faster than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/n32/b1024` | 4.59964 ± 0.0273336 (W 0.012053) | 31.2784 ± 0.114079 (W 0.0673225) | 🔵 tlinalg 6.80× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.15831 ± 0.00018362 (W 0.00159683) | 1.22586 ± 0.0387475 (W 0.00376725) | 🔵 tlinalg 7.74× faster than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/n8/b1024` | 0.418285 ± 0.00680902 (W 0.00207268) | 2.93498 ± 0.0301822 (W 0.00577135) | 🔵 tlinalg 7.02× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.35216 ± 0.00530586 (W 0.00495616) | 2.44867 ± 0.0544339 (W 0.0052741) | 🔵 tlinalg 6.95× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 0.942222 ± 0.0160339 (W 0.00391288) | 13.6841 ± 0.279476 (W 0.0200333) | 🔵 tlinalg 14.52× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.055008 ± 0.0285815 (W 0.000582692) | 0.229638 ± 0.00212644 (W 0.0021756) | 🔵 tlinalg 4.17× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `solve/n8/b1024` | 0.131578 ± 0.00345137 (W 0.00243084) | 0.888525 ± 0.0123193 (W 0.00175641) | 🔵 tlinalg 6.75× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 7.12465 ± 0.100236 (W 0.0159416) | 51.5408 ± 0.158107 (W 0.0404379) | 🔵 tlinalg 7.23× faster than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 25.68 ± 1.2532 (W 0.31697) | 195.408 ± 0.784409 (W 0.298293) | 🔵 tlinalg 7.61× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.559603 ± 0.0234668 (W 0.00287938) | 6.11763 ± 0.0335963 (W 0.0389055) | 🔵 tlinalg 10.93× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 1.94047 ± 0.0251406 (W 0.010574) | 18.576 ± 0.0514726 (W 0.0214354) | 🔵 tlinalg 9.57× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 7.2453 ± 0.19651 (W 0.0728173) | 51.4432 ± 0.152097 (W 0.0660463) | 🔵 tlinalg 7.10× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 27.5104 ± 1.69299 (W 0.0372225) | 195.312 ± 0.946067 (W 0.166638) | 🔵 tlinalg 7.10× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.55727 ± 0.00685259 (W 0.00232723) | 6.10455 ± 0.048546 (W 0.00911423) | 🔵 tlinalg 10.95× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 1.97185 ± 0.0163361 (W 0.0223358) | 18.5895 ± 0.0273376 (W 0.0496887) | 🔵 tlinalg 9.43× faster than `lapack-mkl` |  |
| `svd_values/n16/b1024` | 5.2428 ± 0.104837 (W 0.019588) | 19.2897 ± 0.0390806 (W 0.031287) | 🔵 tlinalg 3.68× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 20.0506 ± 0.0338124 (W 0.046468) | 64.6236 ± 0.126986 (W 0.0357893) | 🔵 tlinalg 3.22× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.418254 ± 0.0118027 (W 0.00536) | 2.67359 ± 0.0490119 (W 0.0054135) | 🔵 tlinalg 6.39× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n8/b1024` | 1.45114 ± 0.0204991 (W 0.00983844) | 6.6852 ± 0.0582931 (W 0.00952085) | 🔵 tlinalg 4.61× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.085911 ± 0.000562596 (W 0.00292045) | 0.585171 ± 0.0015084 (W 0.00504206) | 🔵 tlinalg 6.81× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.199089 ± 0.013611 (W 0.00653743) | 2.52341 ± 0.1206 (W 0.00739785) | 🔵 tlinalg 12.67× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.018965 ± 0.00025652 (W 0.000489368) | 0.294289 ± 0.0131102 (W 0.00204269) | 🔵 tlinalg 15.52× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.035361 ± 0.00029726 (W 0.00113018) | 0.394197 ± 0.00493122 (W 0.00361856) | 🔵 tlinalg 11.15× faster than `lapack-mkl` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.174202 ± 0.00164984 (W 0.00237378) | 1.82676 ± 0.00924939 (W 0.00844036) | 🔵 tlinalg 10.49× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.814971 ± 0.00102433 (W 0.0105677) | 8.85274 ± 0.086585 (W 0.0309765) | 🔵 tlinalg 10.86× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.032656 ± 0.000340869 (W 0.000420276) | 0.177021 ± 0.000181992 (W 0.00156802) | 🔵 tlinalg 5.42× faster than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.0605335 ± 0.00107836 (W 0.000618184) | 0.471269 ± 0.0124106 (W 0.00302621) | 🔵 tlinalg 7.79× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eig/n16/b1024` | 16.5046 ± 0.144671 (W 0.085372) | 175.242 ± 0.218263 (W 0.0948532) | 🔵 tlinalg 10.62× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 67.3092 ± 0.104663 (W 0.0682735) | 791.567 ± 2.68529 (W 2.3457) | 🔵 tlinalg 11.76× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 1.32108 ± 0.0269827 (W 0.00905802) | 12.4359 ± 0.0275516 (W 0.0239668) | 🔵 tlinalg 9.41× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 4.46289 ± 0.0332416 (W 0.0186923) | 43.3132 ± 0.0968693 (W 0.050637) | 🔵 tlinalg 9.71× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 4.06712 ± 0.0371524 (W 0.0178531) | 32.2539 ± 0.119767 (W 0.0460727) | 🔵 tlinalg 7.93× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 17.959 ± 0.0545537 (W 0.0377201) | 151.992 ± 0.235019 (W 0.232285) | 🔵 tlinalg 8.46× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.378375 ± 0.00100055 (W 0.00234623) | 2.81605 ± 0.00276294 (W 0.00238315) | 🔵 tlinalg 7.44× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.15469 ± 0.00963141 (W 0.00570283) | 8.90632 ± 0.0123291 (W 0.0208292) | 🔵 tlinalg 7.71× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 9.68124 ± 1.15095 (W 0.0283146) | 124.796 ± 0.0771748 (W 0.255371) | 🔵 tlinalg 12.89× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigvals/n32/b1024` | 42.7161 ± 0.548281 (W 0.184322) | 522.534 ± 0.445274 (W 0.37991) | 🔵 tlinalg 12.23× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.615769 ± 0.00809607 (W 0.00897475) | 9.54884 ± 0.0167252 (W 0.0168789) | 🔵 tlinalg 15.51× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 2.49934 ± 0.00252289 (W 0.0722688) | 34.331 ± 0.034112 (W 0.0460916) | 🔵 tlinalg 13.74× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 3.01575 ± 0.00836091 (W 0.0101348) | 18.3656 ± 0.0510458 (W 0.0211311) | 🔵 tlinalg 6.09× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 11.9619 ± 0.0492143 (W 0.0465142) | 77.2988 ± 0.110441 (W 0.217681) | 🔵 tlinalg 6.46× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.310411 ± 0.000970936 (W 0.00272973) | 1.79366 ± 0.0169092 (W 0.00250881) | 🔵 tlinalg 5.78× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.928155 ± 0.0012975 (W 0.00288029) | 5.54375 ± 0.00208933 (W 0.00502783) | 🔵 tlinalg 5.97× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.626299 ± 0.00211748 (W 0.0116043) | 5.52569 ± 0.117801 (W 0.0158046) | 🔵 tlinalg 8.82× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 3.02888 ± 0.0164596 (W 0.0281782) | 27.044 ± 0.176619 (W 0.0453273) | 🔵 tlinalg 8.93× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.08792 ± 0.00303092 (W 0.00161632) | 0.526079 ± 0.00844896 (W 0.00301314) | 🔵 tlinalg 5.98× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.190046 ± 0.00392488 (W 0.003996) | 1.29855 ± 0.0140796 (W 0.00396396) | 🔵 tlinalg 6.83× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.69575 ± 0.00155285 (W 0.00717871) | 8.4601 ± 0.0300722 (W 0.0172349) | 🔵 tlinalg 12.16× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 2.68445 ± 0.0155922 (W 0.0129069) | 34.5265 ± 0.0332116 (W 0.0548382) | 🔵 tlinalg 12.86× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.107587 ± 0.00419942 (W 0.00203256) | 1.5916 ± 0.00417433 (W 0.00535655) | 🔵 tlinalg 14.79× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.260954 ± 0.00120787 (W 0.00198655) | 3.1428 ± 0.0127677 (W 0.00595994) | 🔵 tlinalg 12.04× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.636219 ± 0.0187762 (W 0.0100889) | 6.26488 ± 0.0563461 (W 0.0302138) | 🔵 tlinalg 9.85× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 3.61805 ± 0.0834117 (W 0.0163708) | 38.2981 ± 0.454986 (W 0.0607453) | 🔵 tlinalg 10.59× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.050515 ± 0.00396938 (W 0.000729713) | 0.426877 ± 0.012251 (W 0.00242629) | 🔵 tlinalg 8.45× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `householder_apply/n8/b1024` | 0.15461 ± 0.00485033 (W 0.00199165) | 1.26918 ± 0.0299225 (W 0.00374129) | 🔵 tlinalg 8.21× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.602761 ± 0.0222793 (W 0.0117983) | 6.29721 ± 0.0153825 (W 0.011668) | 🔵 tlinalg 10.45× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n32/b1024` | 2.65463 ± 0.0588728 (W 0.0217303) | 27.4353 ± 0.0705817 (W 0.0506714) | 🔵 tlinalg 10.33× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.0758175 ± 0.000557755 (W 0.000822267) | 0.515738 ± 0.00318087 (W 0.00326444) | 🔵 tlinalg 6.80× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.197213 ± 0.0330459 (W 0.00586135) | 1.48186 ± 0.00377617 (W 0.00250016) | 🔵 tlinalg 7.51× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu/n16/b1024` | 0.440518 ± 0.0206881 (W 0.00952734) | 3.58903 ± 0.0656098 (W 0.0158435) | 🔵 tlinalg 8.15× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 2.20695 ± 0.815619 (W 0.0188356) | 19.5292 ± 0.0406915 (W 0.0464827) | 🔵 tlinalg 8.85× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu/n4/b1024` | 0.0705425 ± 0.00110184 (W 0.00136127) | 0.283382 ± 0.00104334 (W 0.00245351) | 🔵 tlinalg 4.02× faster than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.155456 ± 0.0135477 (W 0.00367465) | 0.882927 ± 0.00680675 (W 0.00294924) | 🔵 tlinalg 5.68× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor/n16/b1024` | 0.292565 ± 0.0286391 (W 0.00302085) | 2.63366 ± 0.00866427 (W 0.00676497) | 🔵 tlinalg 9.00× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 1.26761 ± 0.0214309 (W 0.015748) | 15.4335 ± 0.0469116 (W 0.0256861) | 🔵 tlinalg 12.18× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.067803 ± 0.00204463 (W 0.00221913) | 0.183084 ± 0.000451232 (W 0.00153341) | 🔵 tlinalg 2.70× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.112675 ± 0.00219808 (W 0.00492463) | 0.621142 ± 0.00354873 (W 0.00240554) | 🔵 tlinalg 5.51× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.50737 ± 0.0567163 (W 0.00500003) | 5.29157 ± 0.0267222 (W 0.0169236) | 🔵 tlinalg 10.43× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor_solve/n32/b1024` | 1.77574 ± 0.00392616 (W 0.0226239) | 20.9463 ± 0.217565 (W 0.0462709) | 🔵 tlinalg 11.80× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.081483 ± 0.000576142 (W 0.00198849) | 0.416593 ± 0.00152176 (W 0.00263276) | 🔵 tlinalg 5.11× faster than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.170353 ± 0.0131723 (W 0.00225578) | 1.66805 ± 0.0101348 (W 0.00268443) | 🔵 tlinalg 9.79× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1024` | 0.19451 ± 0.00320324 (W 0.00163129) | 2.62297 ± 0.0140519 (W 0.00842217) | 🔵 tlinalg 13.49× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.875331 ± 0.0340872 (W 0.0193248) | 5.66136 ± 0.124322 (W 0.0653185) | 🔵 tlinalg 6.47× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.0455055 ± 0.000638487 (W 0.000694609) | 0.242665 ± 0.00118296 (W 0.0014087) | 🔵 tlinalg 5.33× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.0874645 ± 0.00120784 (W 0.000778548) | 1.072 ± 0.00269872 (W 0.000849653) | 🔵 tlinalg 12.26× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.39962 ± 0.00829831 (W 0.00741024) | 10.5526 ± 0.0212086 (W 0.0182856) | 🔵 tlinalg 7.54× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 9.32213 ± 0.0319635 (W 0.0395684) | 49.3847 ± 0.133958 (W 0.0354345) | 🔵 tlinalg 5.30× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.117655 ± 0.000810541 (W 0.00267834) | 0.926465 ± 0.00290115 (W 0.00288917) | 🔵 tlinalg 7.87× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.344117 ± 0.00396023 (W 0.00354361) | 2.63474 ± 0.00680363 (W 0.00543303) | 🔵 tlinalg 7.66× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.5677 ± 0.0031106 (W 0.00412455) | 15.7948 ± 0.0508535 (W 0.0366451) | 🔵 tlinalg 10.08× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 8.64768 ± 0.0833925 (W 0.0408756) | 69.4229 ± 0.0836977 (W 0.0243181) | 🔵 tlinalg 8.03× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.186881 ± 0.00188853 (W 0.000690299) | 1.75345 ± 0.00769268 (W 0.00673606) | 🔵 tlinalg 9.38× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.483581 ± 0.00309787 (W 0.0048684) | 4.74255 ± 0.00353651 (W 0.01208) | 🔵 tlinalg 9.81× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.523739 ± 0.0157628 (W 0.00522227) | 5.55159 ± 0.00678659 (W 0.00990703) | 🔵 tlinalg 10.60× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 1.82911 ± 0.00775964 (W 0.00808283) | 21.5439 ± 0.187972 (W 0.0342291) | 🔵 tlinalg 11.78× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.076202 ± 0.000994484 (W 0.00316539) | 0.479227 ± 0.00275998 (W 0.00235691) | 🔵 tlinalg 6.29× faster than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.200024 ± 0.0829449 (W 0.00282758) | 1.75052 ± 0.0107112 (W 0.00329612) | 🔵 tlinalg 8.75× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_full/n16/b1024` | 7.78184 ± 0.55475 (W 0.0441712) | 67.537 ± 0.109172 (W 0.057594) | 🔵 tlinalg 8.68× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 33.5593 ± 1.50185 (W 0.160811) | 285.699 ± 0.272201 (W 0.428934) | 🔵 tlinalg 8.51× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.643854 ± 0.0113495 (W 0.00406886) | 7.39802 ± 0.020326 (W 0.0548511) | 🔵 tlinalg 11.49× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 2.14014 ± 0.0323489 (W 0.0170106) | 22.1825 ± 0.0599964 (W 0.0289401) | 🔵 tlinalg 10.36× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 7.78071 ± 0.0427699 (W 0.0454594) | 67.288 ± 0.116441 (W 0.0536766) | 🔵 tlinalg 8.65× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 33.4523 ± 0.786409 (W 0.117447) | 285.171 ± 0.264888 (W 0.531407) | 🔵 tlinalg 8.52× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.645985 ± 0.0147216 (W 0.0109046) | 7.39576 ± 0.0268522 (W 0.0162034) | 🔵 tlinalg 11.45× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 2.15511 ± 0.0919479 (W 0.0393001) | 22.1929 ± 0.0560997 (W 0.0291011) | 🔵 tlinalg 10.30× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 5.73688 ± 0.115069 (W 0.0180708) | 28.1256 ± 0.0734747 (W 0.0231249) | 🔵 tlinalg 4.90× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 22.4576 ± 0.0925623 (W 0.0398708) | 105.893 ± 0.105035 (W 0.193673) | 🔵 tlinalg 4.72× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.491084 ± 0.000850279 (W 0.00174623) | 3.50855 ± 0.00530734 (W 0.00827875) | 🔵 tlinalg 7.14× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.65244 ± 0.00318777 (W 0.00935285) | 9.11677 ± 0.0208259 (W 0.0107838) | 🔵 tlinalg 5.52× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.139081 ± 0.00603995 (W 0.0049335) | 1.3415 ± 0.0203422 (W 0.00372393) | 🔵 tlinalg 9.65× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 0.56926 ± 0.0368866 (W 0.0076637) | 3.44807 ± 0.15306 (W 0.0101506) | 🔵 tlinalg 6.06× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.0282235 ± 0.000279968 (W 0.000471824) | 0.301376 ± 0.000289027 (W 0.00237529) | 🔵 tlinalg 10.68× faster than `lapack-mkl` |  |
| `triangular_solve/n8/b1024` | 0.067186 ± 0.00244603 (W 0.00178709) | 0.580185 ± 0.00324697 (W 0.00298612) | 🔵 tlinalg 8.64× faster than `lapack-mkl` | `!` between-start range over 5% |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0663495 ± 0.000135924 (W 0.000159693) | 0.0942715 ± 0.000688672 (W 0.000950236) | 🔵 tlinalg 1.42× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.185593 ± 0.00342469 (W 0.0037275) | 0.135713 ± 0.000664529 (W 0.00188522) | 🔴 tlinalg 1.37× slower than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.125741 ± 0.00127619 (W 0.00529209) | 0.120887 ± 0.000234598 (W 0.00122752) | · |  |
| `lu_factor_solve/n128/b1` | 0.135609 ± 0.00188152 (W 0.00415897) | 0.143488 ± 0.000243154 (W 0.00143961) | 🔵 tlinalg 1.06× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.0099085 ± 0.000479568 (W 7.7852e-05) | 0.0165815 ± 0.000136052 (W 0.000265316) | 🔵 tlinalg 1.67× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.146269 ± 0.00126918 (W 0.00402788) | 0.150131 ± 0.000512986 (W 0.0015629) | · |  |
| `svd_values/n128/b1` | 2.38788 ± 0.00237538 (W 0.00425833) | 1.13146 ± 0.00253791 (W 0.00218134) | 🔴 tlinalg 2.11× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.0068425 ± 6.72824e-05 (W 6.20949e-05) | 0.009958 ± 0.000276507 (W 0.000165556) | 🔵 tlinalg 1.46× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.186549 ± 9.19601e-05 (W 0.00224601) | 0.407656 ± 0.015792 (W 0.00377794) | 🔵 tlinalg 2.19× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n128/b1` | 0.342833 ± 0.00286199 (W 0.00639094) | 0.454094 ± 0.00131364 (W 0.00290096) | 🔵 tlinalg 1.32× faster than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.260937 ± 0.0012001 (W 0.0042623) | 0.416297 ± 0.00218452 (W 0.00268092) | 🔵 tlinalg 1.60× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.292233 ± 0.00273264 (W 0.00393066) | 0.445875 ± 0.00423011 (W 0.00177571) | 🔵 tlinalg 1.53× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.0314185 ± 0.000146402 (W 0.000122738) | 0.0251825 ± 6.072e-05 (W 0.000175494) | 🔴 tlinalg 1.25× slower than `lapack-mkl` |  |
| `solve/n128/b1` | 0.317769 ± 0.00229734 (W 0.00385444) | 0.463577 ± 0.000900065 (W 0.00202758) | 🔵 tlinalg 1.46× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 3.15531 ± 0.0101037 (W 0.00541577) | 1.9236 ± 0.0122541 (W 0.00381005) | 🔴 tlinalg 1.64× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.0186345 ± 6.95e-05 (W 9.71765e-05) | 0.01309 ± 3.5805e-05 (W 7.77472e-05) | 🔴 tlinalg 1.42× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 23.6104 ± 0.0416166 (W 0.104426) | 14.9753 ± 0.0633745 (W 0.0765529) | 🔴 tlinalg 1.58× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 18.5608 ± 0.0388776 (W 0.0274262) | 12.7365 ± 0.0189465 (W 0.030795) | 🔴 tlinalg 1.46× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 2.76048 ± 0.0396463 (W 0.0705592) | 3.15194 ± 0.0133426 (W 0.0141868) | 🔵 tlinalg 1.14× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 2.68198 ± 0.166805 (W 0.0480482) | 2.13774 ± 0.00370018 (W 0.00389845) | 🔴 tlinalg 1.25× slower than `lapack-mkl` | `!` between-start range over 5% |
| `qr/n512/b1` | 7.79468 ± 0.0524703 (W 0.108022) | 8.74482 ± 0.02037 (W 0.0139792) | 🔵 tlinalg 1.12× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 9.63445 ± 0.0598353 (W 0.0953914) | 24.5995 ± 0.264089 (W 0.0284812) | 🔵 tlinalg 2.55× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 60.7754 ± 0.0944252 (W 0.294316) | 49.3125 ± 0.0812221 (W 0.0705549) | 🔴 tlinalg 1.23× slower than `lapack-mkl` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 38.6224 ± 0.491602 (W 0.529941) | 65.8509 ± 0.0897618 (W 0.145206) | 🔵 tlinalg 1.70× faster than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 28.843 ± 0.061146 (W 0.0687579) | 28.9146 ± 0.302296 (W 0.0289377) | · |  |
| `householder_apply/n512/b1` | 7.01812 ± 0.00880437 (W 0.072888) | 8.11008 ± 0.0183848 (W 0.0170916) | 🔵 tlinalg 1.16× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 6.94187 ± 0.0542775 (W 0.109774) | 5.43366 ± 0.0159201 (W 0.00420319) | 🔴 tlinalg 1.28× slower than `lapack-mkl` |  |
| `qr/n512/b1` | 16.681 ± 0.138353 (W 0.265948) | 15.2492 ± 0.0397784 (W 0.0189847) | 🔴 tlinalg 1.09× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 18.7744 ± 0.0502486 (W 0.0965308) | 59.6268 ± 0.12872 (W 0.223446) | 🔵 tlinalg 3.18× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 99.408 ± 0.317422 (W 0.617953) | 87.0164 ± 1.08536 (W 0.0953476) | 🔴 tlinalg 1.14× slower than `lapack-mkl` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 7.81069 ± 0.012311 (W 0.0284708) | 6.16374 ± 0.0240462 (W 0.0436942) | 🔴 tlinalg 1.27× slower than `lapack-mkl` |  |
| `qr/4096x256/b1` | 22.3651 ± 0.405485 (W 0.479765) | 18.0558 ± 0.101029 (W 0.0450266) | 🔴 tlinalg 1.24× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 23.7242 ± 0.402032 (W 0.306258) | 59.9477 ± 2.70573 (W 0.724423) | 🔵 tlinalg 2.53× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/4096x256/b1` | 39.3039 ± 0.0564223 (W 0.335985) | 34.6609 ± 0.423364 (W 0.0815068) | 🔴 tlinalg 1.13× slower than `lapack-mkl` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 19.9645 ± 0.218413 (W 0.0472) | 16.9134 ± 0.0549062 (W 0.0786859) | 🔴 tlinalg 1.18× slower than `lapack-mkl` |  |
| `qr/4096x256/b1` | 53.698 ± 0.0737052 (W 0.0957099) | 40.7248 ± 0.269237 (W 0.262735) | 🔴 tlinalg 1.32× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 60.6148 ± 0.156586 (W 0.358105) | 161.895 ± 1.1027 (W 0.380694) | 🔵 tlinalg 2.67× faster than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 111.258 ± 0.240914 (W 0.253296) | 75.8289 ± 0.367724 (W 0.365188) | 🔴 tlinalg 1.47× slower than `lapack-mkl` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
