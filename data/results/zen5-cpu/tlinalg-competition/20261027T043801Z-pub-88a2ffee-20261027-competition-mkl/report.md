# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `88a2ffeea4c5ef514dac91b2ea65d43c52b121e9`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.25.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `6c795e30d74f6a15af990fb38902ac28af9b3299`
- toolkit commit: `467573e6e3e405b8ec30b3b61d096c1d0c9893c3`
- measured binary SHA-256: `82fd37de55cf67cd1efd4b78f359c66d2a60481f45bfbad82896c2f37492a202`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-27T04:58:21.288235Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor mkl --aa 4 --reps 5 --prime-ms 250 --label pub-88a2ffee-20261027-competition-mkl`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261027T043801Z-pub-88a2ffee-20261027-competition-mkl/`

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
    As measured: `t4a-faer` 0.25.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.13%, worst 97.44% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 30 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.34%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.11816 ± 0.00144156 (W 0.00195627) | 1.05378 ± 0.0047196 (W 0.00189261) | 🔵 tlinalg-pool 8.92× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.47261 ± 0.00202699 (W 0.0044669) | 3.72177 ± 0.0276019 (W 0.014555) | 🔵 tlinalg-pool 7.87× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.180246 ± 0.000474068 (W 0.00124504) | 0.120043 ± 0.00270533 (W 0.000985078) | 🔴 tlinalg-pool 1.50× slower than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.359496 ± 0.00249846 (W 0.00145839) | 0.323663 ± 0.00203801 (W 0.0017502) | 🔴 tlinalg-pool 1.11× slower than `lapack-mkl` |  |
| `eig/n16/b1024` | 11.8592 ± 0.0248078 (W 0.024848) | 52.7487 ± 0.225565 (W 0.0587057) | 🔵 tlinalg-pool 4.45× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 53.2362 ± 0.0640746 (W 0.0834665) | 283.232 ± 0.368463 (W 0.317788) | 🔵 tlinalg-pool 5.32× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 6.19311 ± 0.00872016 (W 0.00736154) | 2.83519 ± 0.0100826 (W 0.0030865) | 🔴 tlinalg-pool 2.18× slower than `lapack-mkl` |  |
| `eig/n8/b1024` | 2.95749 ± 0.0094049 (W 0.00520947) | 11.659 ± 0.0389843 (W 0.0243671) | 🔵 tlinalg-pool 3.94× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 3.80283 ± 0.261475 (W 0.010128) | 23.4481 ± 0.0791156 (W 0.0228858) | 🔵 tlinalg-pool 6.17× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigh/n32/b1024` | 13.8743 ± 0.223488 (W 0.0197439) | 100.538 ± 0.420364 (W 0.23531) | 🔵 tlinalg-pool 7.25× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 2.54698 ± 0.0071688 (W 0.00807891) | 2.86083 ± 0.0215404 (W 0.00391321) | 🔵 tlinalg-pool 1.12× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.11581 ± 0.0594232 (W 0.00400823) | 7.76804 ± 0.0291926 (W 0.00826225) | 🔵 tlinalg-pool 6.96× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigvals/n16/b1024` | 8.16628 ± 0.0546839 (W 0.0188581) | 36.4317 ± 0.0641599 (W 0.0198027) | 🔵 tlinalg-pool 4.46× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 36.3319 ± 0.0631985 (W 0.0883505) | 169.038 ± 0.523315 (W 0.270615) | 🔵 tlinalg-pool 4.65× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 3.17788 ± 0.00890266 (W 0.00389388) | 2.10349 ± 0.00433425 (W 0.00173553) | 🔴 tlinalg-pool 1.51× slower than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 1.93278 ± 0.00821512 (W 0.00533842) | 8.91508 ± 0.00535516 (W 0.0153767) | 🔵 tlinalg-pool 4.61× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 2.80348 ± 0.00312577 (W 0.00635393) | 12.9887 ± 0.0110118 (W 0.0130209) | 🔵 tlinalg-pool 4.63× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 10.9147 ± 0.0307473 (W 0.0312863) | 42.9908 ± 0.0844967 (W 0.0293525) | 🔵 tlinalg-pool 3.94× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 2.03018 ± 0.00429639 (W 0.00385414) | 1.50636 ± 0.0114289 (W 0.0072123) | 🔴 tlinalg-pool 1.35× slower than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.878141 ± 0.00275443 (W 0.00188356) | 4.43659 ± 0.0190481 (W 0.0046929) | 🔵 tlinalg-pool 5.05× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.4598 ± 0.00576516 (W 0.00595304) | 3.97896 ± 0.0416646 (W 0.0132564) | 🔵 tlinalg-pool 8.65× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 1.92922 ± 0.0487688 (W 0.0154352) | 26.1093 ± 0.0676489 (W 0.0194422) | 🔵 tlinalg-pool 13.53× faster than `lapack-mkl` | `!` between-start range over 5% |
| `full_piv_lu/n4/b1024` | 0.404844 ± 0.00616303 (W 0.00306533) | 0.427105 ± 0.0101113 (W 0.00187067) | 🔵 tlinalg-pool 1.05× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 1.06747 ± 0.00584804 (W 0.00140735) | 0.988058 ± 0.0197048 (W 0.00291438) | 🔴 tlinalg-pool 1.08× slower than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.467441 ± 0.00635259 (W 0.00571056) | 5.80022 ± 0.0177901 (W 0.023089) | 🔵 tlinalg-pool 12.41× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 1.58272 ± 0.0154707 (W 0.0269313) | 29.5597 ± 0.0217285 (W 0.0362495) | 🔵 tlinalg-pool 18.68× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.516157 ± 0.00918342 (W 0.00369929) | 1.13677 ± 0.00693131 (W 0.00747968) | 🔵 tlinalg-pool 2.20× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.16953 ± 0.00124213 (W 0.00144469) | 1.97278 ± 0.0199891 (W 0.00592752) | 🔵 tlinalg-pool 11.64× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.638849 ± 0.00474801 (W 0.00539493) | 2.69055 ± 0.0341321 (W 0.0205845) | 🔵 tlinalg-pool 4.21× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 2.5237 ± 0.0329392 (W 0.0241492) | 13.2509 ± 0.172242 (W 0.0580387) | 🔵 tlinalg-pool 5.25× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.387874 ± 0.0145873 (W 0.00176908) | 0.324398 ± 0.00212146 (W 0.00188943) | 🔴 tlinalg-pool 1.20× slower than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.179378 ± 0.0032174 (W 0.00127903) | 0.796562 ± 0.0102122 (W 0.00489705) | 🔵 tlinalg-pool 4.44× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1024` | 0.49791 ± 0.00696704 (W 0.00238599) | 2.94034 ± 0.00781064 (W 0.00342453) | 🔵 tlinalg-pool 5.91× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 1.699 ± 0.0193508 (W 0.0109188) | 12.2133 ± 0.0244821 (W 0.0180051) | 🔵 tlinalg-pool 7.19× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.472704 ± 0.0121099 (W 0.00196333) | 0.305203 ± 0.000654684 (W 0.00150186) | 🔴 tlinalg-pool 1.55× slower than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n8/b1024` | 0.180314 ± 0.0030229 (W 0.000989288) | 0.837235 ± 0.000257387 (W 0.00186398) | 🔵 tlinalg-pool 4.64× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.381081 ± 0.00546883 (W 0.00507207) | 1.6597 ± 0.0709782 (W 0.00328129) | 🔵 tlinalg-pool 4.36× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 1.32936 ± 0.00971138 (W 0.0111012) | 11.8367 ± 0.0715406 (W 0.0273531) | 🔵 tlinalg-pool 8.90× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.309763 ± 0.00235548 (W 0.00208239) | 0.168041 ± 0.000514188 (W 0.00120425) | 🔴 tlinalg-pool 1.84× slower than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.865545 ± 0.00975462 (W 0.00841614) | 0.51714 ± 0.00930959 (W 0.00162204) | 🔴 tlinalg-pool 1.67× slower than `lapack-mkl` |  |
| `lu_factor/n16/b1024` | 0.269961 ± 0.0031475 (W 0.00933431) | 1.19543 ± 0.0219353 (W 0.00277083) | 🔵 tlinalg-pool 4.43× faster than `lapack-mkl` |  |
| `lu_factor/n32/b1024` | 0.746059 ± 0.00441663 (W 0.0103484) | 8.91864 ± 0.0428401 (W 0.00970524) | 🔵 tlinalg-pool 11.95× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.235572 ± 0.00100239 (W 0.00124075) | 0.065116 ± 0.00163536 (W 0.000233289) | 🔴 tlinalg-pool 3.62× slower than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.625053 ± 0.00764757 (W 0.0043897) | 0.258957 ± 0.00260471 (W 0.00196132) | 🔴 tlinalg-pool 2.41× slower than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.339516 ± 0.00306921 (W 0.00383229) | 2.39592 ± 0.0328189 (W 0.00663494) | 🔵 tlinalg-pool 7.06× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 0.899804 ± 0.0120415 (W 0.00897025) | 13.058 ± 0.0666914 (W 0.0089373) | 🔵 tlinalg-pool 14.51× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.299334 ± 0.00485133 (W 0.0016378) | 0.179723 ± 0.00173571 (W 0.00135435) | 🔴 tlinalg-pool 1.67× slower than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.129802 ± 0.000811224 (W 0.00173819) | 0.821025 ± 0.00195482 (W 0.00246347) | 🔵 tlinalg-pool 6.33× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.106978 ± 0.000927392 (W 0.00131231) | 1.0448 ± 0.0113723 (W 0.00278094) | 🔵 tlinalg-pool 9.77× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.298284 ± 0.0125048 (W 0.00825076) | 4.01292 ± 0.0333861 (W 0.0122729) | 🔵 tlinalg-pool 13.45× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.070716 ± 0.000201561 (W 0.000140473) | 0.130617 ± 0.00109725 (W 0.00139523) | 🔵 tlinalg-pool 1.85× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.230517 ± 0.00120624 (W 0.00169671) | 0.584804 ± 0.00185926 (W 0.00236185) | 🔵 tlinalg-pool 2.54× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.15447 ± 0.0184059 (W 0.00725262) | 5.27501 ± 0.0444724 (W 0.00778422) | 🔵 tlinalg-pool 4.57× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 4.58438 ± 0.0133174 (W 0.0222059) | 21.1541 ± 0.0707778 (W 0.0366872) | 🔵 tlinalg-pool 4.61× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.767939 ± 0.0085408 (W 0.0021626) | 0.721904 ± 0.00407835 (W 0.00166761) | 🔴 tlinalg-pool 1.06× slower than `lapack-mkl` |  |
| `qr/n8/b1024` | 2.43052 ± 0.0479365 (W 0.00266579) | 1.68659 ± 0.0230013 (W 0.00330049) | 🔴 tlinalg-pool 1.44× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.35195 ± 0.0235322 (W 0.0110695) | 8.3491 ± 0.0413144 (W 0.0328257) | 🔵 tlinalg-pool 6.18× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 4.5939 ± 0.0533953 (W 0.0733823) | 31.1327 ± 0.0507464 (W 0.0587301) | 🔵 tlinalg-pool 6.78× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 1.2732 ± 0.0276169 (W 0.00222673) | 1.21547 ± 0.0184932 (W 0.00288108) | · |  |
| `rank_revealing_qr/n8/b1024` | 3.39964 ± 0.0617467 (W 0.00537711) | 2.94237 ± 0.0167314 (W 0.00519293) | 🔴 tlinalg-pool 1.16× slower than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.367439 ± 0.0234606 (W 0.00264413) | 2.49184 ± 0.0643437 (W 0.00325987) | 🔵 tlinalg-pool 6.78× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 0.957036 ± 0.0103328 (W 0.0172835) | 13.6251 ± 0.0732898 (W 0.0212336) | 🔵 tlinalg-pool 14.24× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.372424 ± 0.00451688 (W 0.00304182) | 0.235736 ± 0.00132863 (W 0.00167166) | 🔴 tlinalg-pool 1.58× slower than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.134049 ± 0.0650218 (W 0.00298282) | 0.896969 ± 0.00988452 (W 0.00289819) | 🔵 tlinalg-pool 6.69× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_full/n16/b1024` | 7.13045 ± 0.0461361 (W 0.0722109) | 51.5142 ± 0.0381934 (W 0.070309) | 🔵 tlinalg-pool 7.22× faster than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 25.8327 ± 0.305905 (W 0.243245) | 195.083 ± 0.516915 (W 0.148465) | 🔵 tlinalg-pool 7.55× faster than `lapack-mkl` |  |
| `svd_full/n4/b1024` | 4.41298 ± 0.0533854 (W 0.0110598) | 6.19924 ± 0.00413809 (W 0.0111332) | 🔵 tlinalg-pool 1.40× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 2.08238 ± 0.144288 (W 0.0244668) | 18.9269 ± 0.0191579 (W 0.0113063) | 🔵 tlinalg-pool 9.09× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.13321 ± 0.0568622 (W 0.0404927) | 51.4693 ± 0.0425392 (W 0.0566181) | 🔵 tlinalg-pool 7.22× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 25.8222 ± 1.51538 (W 0.949076) | 194.823 ± 0.813349 (W 0.13055) | 🔵 tlinalg-pool 7.54× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 4.36568 ± 0.0547672 (W 0.00571141) | 6.24945 ± 0.0215901 (W 0.00856845) | 🔵 tlinalg-pool 1.43× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 2.1003 ± 0.0798912 (W 0.0204702) | 18.9087 ± 0.0257276 (W 0.0152622) | 🔵 tlinalg-pool 9.00× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 5.13785 ± 0.0102969 (W 0.006938) | 19.2346 ± 0.0618029 (W 0.00862122) | 🔵 tlinalg-pool 3.74× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 19.9715 ± 0.0331836 (W 0.0291881) | 64.6301 ± 0.239906 (W 0.0669885) | 🔵 tlinalg-pool 3.24× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 3.17163 ± 0.0160105 (W 0.00618161) | 2.67119 ± 0.00256029 (W 0.00554454) | 🔴 tlinalg-pool 1.19× slower than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.43233 ± 0.00498556 (W 0.0039559) | 6.72611 ± 0.0257945 (W 0.00735482) | 🔵 tlinalg-pool 4.70× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.079583 ± 0.00251456 (W 0.000324752) | 0.602336 ± 0.0039071 (W 0.00424021) | 🔵 tlinalg-pool 7.57× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 0.211118 ± 0.00230304 (W 0.00493161) | 2.65688 ± 0.0266847 (W 0.00486194) | 🔵 tlinalg-pool 12.58× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.093213 ± 0.000185221 (W 0.000694343) | 0.312501 ± 0.0131218 (W 0.00337833) | 🔵 tlinalg-pool 3.35× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.219507 ± 0.000418277 (W 0.00164106) | 0.410702 ± 0.00208294 (W 0.00294179) | 🔵 tlinalg-pool 1.87× faster than `lapack-mkl` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.165167 ± 0.00285707 (W 0.00257786) | 1.79895 ± 0.00564825 (W 0.00795481) | 🔵 tlinalg-pool 10.89× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.792058 ± 0.00559249 (W 0.00831354) | 8.82948 ± 0.0747306 (W 0.0192738) | 🔵 tlinalg-pool 11.15× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.201809 ± 0.000722179 (W 0.00142189) | 0.177214 ± 0.000544343 (W 0.00109625) | 🔴 tlinalg-pool 1.14× slower than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.416632 ± 0.0030258 (W 0.00261668) | 0.472433 ± 0.00227097 (W 0.00179459) | 🔵 tlinalg-pool 1.13× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 16.3237 ± 0.0406195 (W 0.0341502) | 174.913 ± 0.345452 (W 0.22987) | 🔵 tlinalg-pool 10.72× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 67.1865 ± 0.0218717 (W 0.185408) | 790.948 ± 1.26925 (W 2.09175) | 🔵 tlinalg-pool 11.77× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 10.3213 ± 0.0545377 (W 0.00973861) | 12.424 ± 0.0121179 (W 0.00518603) | 🔵 tlinalg-pool 1.20× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 4.41723 ± 0.0307641 (W 0.00730629) | 43.1874 ± 0.0757051 (W 0.0397118) | 🔵 tlinalg-pool 9.78× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 4.13608 ± 0.175486 (W 0.0657377) | 32.0976 ± 0.0715638 (W 0.016766) | 🔵 tlinalg-pool 7.76× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigh/n32/b1024` | 17.4418 ± 0.288005 (W 0.064869) | 151.171 ± 0.307535 (W 0.0721474) | 🔵 tlinalg-pool 8.67× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 2.89691 ± 0.0120012 (W 0.00600325) | 2.84663 ± 0.00842104 (W 0.00349538) | · |  |
| `eigh/n8/b1024` | 1.17594 ± 0.0225432 (W 0.0175849) | 8.94099 ± 0.037576 (W 0.00627186) | 🔵 tlinalg-pool 7.60× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 9.73352 ± 0.0148217 (W 0.00706188) | 124.671 ± 0.202277 (W 0.0924196) | 🔵 tlinalg-pool 12.81× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 42.5667 ± 0.0209696 (W 0.0249829) | 521.974 ± 0.841399 (W 0.580095) | 🔵 tlinalg-pool 12.26× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 4.99917 ± 0.0563388 (W 0.00781479) | 9.54806 ± 0.00644153 (W 0.00605725) | 🔵 tlinalg-pool 1.91× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 2.51759 ± 0.00813904 (W 0.00699654) | 34.2088 ± 0.0279121 (W 0.0233198) | 🔵 tlinalg-pool 13.59× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 3.01117 ± 0.0128937 (W 0.0115094) | 18.299 ± 0.016168 (W 0.0194512) | 🔵 tlinalg-pool 6.08× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 11.7829 ± 0.0235692 (W 0.0231587) | 77.0694 ± 0.0434207 (W 0.0371674) | 🔵 tlinalg-pool 6.54× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 2.36142 ± 0.0200882 (W 0.00767829) | 1.79692 ± 0.0152792 (W 0.00159269) | 🔴 tlinalg-pool 1.31× slower than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.931736 ± 0.00136474 (W 0.00303744) | 5.53719 ± 0.00987975 (W 0.00642559) | 🔵 tlinalg-pool 5.94× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.612035 ± 0.00216031 (W 0.0152629) | 5.41381 ± 0.047409 (W 0.0176671) | 🔵 tlinalg-pool 8.85× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 2.97553 ± 0.0224426 (W 0.0214036) | 27.0369 ± 0.0307568 (W 0.0345904) | 🔵 tlinalg-pool 9.09× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.462672 ± 0.00499384 (W 0.00298534) | 0.527087 ± 0.00753213 (W 0.00276861) | 🔵 tlinalg-pool 1.14× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 0.189966 ± 0.00371953 (W 0.00514785) | 1.29344 ± 0.0104595 (W 0.00271855) | 🔵 tlinalg-pool 6.81× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.707432 ± 0.0110544 (W 0.0113343) | 8.44327 ± 0.00757532 (W 0.0145129) | 🔵 tlinalg-pool 11.94× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 2.63965 ± 0.0172518 (W 0.0249751) | 34.4224 ± 0.0733062 (W 0.0462211) | 🔵 tlinalg-pool 13.04× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.77799 ± 0.00371637 (W 0.0047459) | 1.60625 ± 0.00644341 (W 0.00653963) | 🔵 tlinalg-pool 2.06× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.267145 ± 0.00187 (W 0.00307652) | 3.20344 ± 0.0125906 (W 0.00382873) | 🔵 tlinalg-pool 11.99× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.635574 ± 0.00595288 (W 0.00577262) | 6.13049 ± 0.066583 (W 0.0184729) | 🔵 tlinalg-pool 9.65× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 3.57131 ± 0.0442559 (W 0.034025) | 37.7888 ± 0.277852 (W 0.0435326) | 🔵 tlinalg-pool 10.58× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.357461 ± 0.00630281 (W 0.00237194) | 0.41537 ± 0.00422641 (W 0.00284802) | 🔵 tlinalg-pool 1.16× faster than `lapack-mkl` |  |
| `householder_apply/n8/b1024` | 0.154496 ± 0.00207461 (W 0.00195847) | 1.24156 ± 0.0521208 (W 0.00571554) | 🔵 tlinalg-pool 8.04× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.624251 ± 0.0146723 (W 0.0111572) | 6.30446 ± 0.0156077 (W 0.00668291) | 🔵 tlinalg-pool 10.10× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n32/b1024` | 2.62336 ± 0.0444875 (W 0.0338397) | 27.6297 ± 0.0376572 (W 0.0193492) | 🔵 tlinalg-pool 10.53× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.567893 ± 0.00329165 (W 0.00202445) | 0.513624 ± 0.000882723 (W 0.00176218) | 🔴 tlinalg-pool 1.11× slower than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.203637 ± 0.00113619 (W 0.00177262) | 1.47712 ± 0.000858516 (W 0.00183881) | 🔵 tlinalg-pool 7.25× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.45428 ± 0.00503117 (W 0.00881368) | 3.57882 ± 0.0232788 (W 0.010662) | 🔵 tlinalg-pool 7.88× faster than `lapack-mkl` |  |
| `lu/n32/b1024` | 2.12015 ± 0.0201004 (W 0.0104729) | 19.654 ± 0.0639959 (W 0.0302205) | 🔵 tlinalg-pool 9.27× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.39222 ± 0.00551881 (W 0.00277203) | 0.281026 ± 0.00195863 (W 0.00215989) | 🔴 tlinalg-pool 1.40× slower than `lapack-mkl` |  |
| `lu/n8/b1024` | 0.152397 ± 0.00152253 (W 0.00307445) | 0.89525 ± 0.0192834 (W 0.00204753) | 🔵 tlinalg-pool 5.87× faster than `lapack-mkl` |  |
| `lu_factor/n16/b1024` | 0.310295 ± 0.0035677 (W 0.0120439) | 2.64562 ± 0.0190857 (W 0.00434134) | 🔵 tlinalg-pool 8.53× faster than `lapack-mkl` |  |
| `lu_factor/n32/b1024` | 1.3051 ± 0.0200737 (W 0.0127557) | 15.4033 ± 0.0790734 (W 0.0177741) | 🔵 tlinalg-pool 11.80× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.300873 ± 0.00270131 (W 0.00235366) | 0.182868 ± 0.00038405 (W 0.00121939) | 🔴 tlinalg-pool 1.65× slower than `lapack-mkl` |  |
| `lu_factor/n8/b1024` | 0.114873 ± 0.000564835 (W 0.00153982) | 0.619419 ± 0.00216494 (W 0.00221938) | 🔵 tlinalg-pool 5.39× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.476079 ± 0.00382671 (W 0.00251843) | 5.28099 ± 0.0182198 (W 0.00355848) | 🔵 tlinalg-pool 11.09× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 1.80251 ± 0.0182351 (W 0.0187586) | 20.667 ± 0.0222673 (W 0.0203899) | 🔵 tlinalg-pool 11.47× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.456411 ± 0.00179545 (W 0.00210495) | 0.415648 ± 0.000620113 (W 0.00180195) | 🔴 tlinalg-pool 1.10× slower than `lapack-mkl` |  |
| `lu_factor_solve/n8/b1024` | 0.172934 ± 0.0015887 (W 0.00208106) | 1.66176 ± 0.00418885 (W 0.00141049) | 🔵 tlinalg-pool 9.61× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.198777 ± 0.00356605 (W 0.00365503) | 2.59259 ± 0.0160642 (W 0.00540144) | 🔵 tlinalg-pool 13.04× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.922353 ± 0.0117793 (W 0.0133873) | 4.99463 ± 0.0370721 (W 0.0132105) | 🔵 tlinalg-pool 5.42× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.166223 ± 0.00176096 (W 0.00164584) | 0.240449 ± 0.000495363 (W 0.00153186) | 🔵 tlinalg-pool 1.45× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.087873 ± 0.000620549 (W 0.000766418) | 1.06903 ± 0.00322176 (W 0.00286678) | 🔵 tlinalg-pool 12.17× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.40608 ± 0.00130453 (W 0.00633763) | 10.511 ± 0.0420574 (W 0.0142856) | 🔵 tlinalg-pool 7.48× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 9.40335 ± 0.0604833 (W 0.0380481) | 49.4689 ± 0.18023 (W 0.019917) | 🔵 tlinalg-pool 5.26× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.871581 ± 0.00519215 (W 0.00234312) | 0.932743 ± 0.0156053 (W 0.00248417) | 🔵 tlinalg-pool 1.07× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.342309 ± 0.00394485 (W 0.00200921) | 2.65537 ± 0.00393418 (W 0.00751371) | 🔵 tlinalg-pool 7.76× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.59635 ± 0.0733241 (W 0.0114495) | 15.8155 ± 0.0430919 (W 0.0160928) | 🔵 tlinalg-pool 9.91× faster than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/n32/b1024` | 8.62972 ± 0.045571 (W 0.0325646) | 69.1725 ± 0.292239 (W 0.0593122) | 🔵 tlinalg-pool 8.02× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 1.48392 ± 0.030017 (W 0.00226129) | 1.78756 ± 0.0060614 (W 0.00475047) | 🔵 tlinalg-pool 1.20× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.49468 ± 0.00856051 (W 0.00368858) | 4.79864 ± 0.0119172 (W 0.00706367) | 🔵 tlinalg-pool 9.70× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.529887 ± 0.0151663 (W 0.0115682) | 5.54956 ± 0.0107933 (W 0.00570418) | 🔵 tlinalg-pool 10.47× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n32/b1024` | 1.88574 ± 0.0140666 (W 0.00952354) | 21.7089 ± 0.0713661 (W 0.0331966) | 🔵 tlinalg-pool 11.51× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.570728 ± 0.00671252 (W 0.00265192) | 0.475144 ± 0.00190779 (W 0.00237915) | 🔴 tlinalg-pool 1.20× slower than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.194761 ± 0.00655113 (W 0.00269998) | 1.74153 ± 0.00899743 (W 0.00177228) | 🔵 tlinalg-pool 8.94× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 7.71446 ± 0.0646465 (W 0.025055) | 67.3185 ± 0.0908306 (W 0.217786) | 🔵 tlinalg-pool 8.73× faster than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 34.6566 ± 0.806786 (W 0.170511) | 285.181 ± 0.622173 (W 0.295084) | 🔵 tlinalg-pool 8.23× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 5.25212 ± 0.0284442 (W 0.00326105) | 7.57654 ± 0.0207038 (W 0.00973944) | 🔵 tlinalg-pool 1.44× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 2.31814 ± 0.0875153 (W 0.0352854) | 22.5428 ± 0.0371875 (W 0.010712) | 🔵 tlinalg-pool 9.72× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.80754 ± 0.0856146 (W 0.0236423) | 67.2165 ± 0.141455 (W 0.033909) | 🔵 tlinalg-pool 8.61× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 33.3068 ± 0.414238 (W 0.113304) | 285.872 ± 0.787426 (W 0.233632) | 🔵 tlinalg-pool 8.58× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1024` | 5.2533 ± 0.0124963 (W 0.00446239) | 7.55285 ± 0.00891062 (W 0.00868025) | 🔵 tlinalg-pool 1.44× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 2.18021 ± 0.0819182 (W 0.0238073) | 22.5419 ± 0.0794562 (W 0.0146204) | 🔵 tlinalg-pool 10.34× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 5.80273 ± 0.0739596 (W 0.0082379) | 28.1506 ± 0.0398454 (W 0.0234935) | 🔵 tlinalg-pool 4.85× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 22.4645 ± 0.0531168 (W 0.0320753) | 105.38 ± 0.0694728 (W 0.0543694) | 🔵 tlinalg-pool 4.69× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 4.05353 ± 0.00793004 (W 0.00341962) | 3.54829 ± 0.0102753 (W 0.00464115) | 🔴 tlinalg-pool 1.14× slower than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.67877 ± 0.00930833 (W 0.00215997) | 9.08353 ± 0.0122686 (W 0.0101364) | 🔵 tlinalg-pool 5.41× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.138837 ± 0.00110373 (W 0.00134077) | 1.39141 ± 0.0174466 (W 0.00498318) | 🔵 tlinalg-pool 10.02× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.615366 ± 0.00212721 (W 0.0159747) | 3.55413 ± 0.00715131 (W 0.0168041) | 🔵 tlinalg-pool 5.78× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.165195 ± 0.000878523 (W 0.00131313) | 0.302554 ± 0.00159831 (W 0.00170742) | 🔵 tlinalg-pool 1.83× faster than `lapack-mkl` |  |
| `triangular_solve/n8/b1024` | 0.065862 ± 0.000385386 (W 0.000682452) | 0.608469 ± 0.00254983 (W 0.00356578) | 🔵 tlinalg-pool 9.24× faster than `lapack-mkl` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.065301 ± 0.00188863 (W 0.000150734) | 0.092186 ± 0.000448718 (W 0.000141155) | 🔵 tlinalg-pool 1.41× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n128/b1` | 0.195353 ± 0.00159333 (W 0.00406133) | 0.135059 ± 0.000443082 (W 0.00179415) | 🔴 tlinalg-pool 1.45× slower than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.118199 ± 0.00310637 (W 0.00438064) | 0.120438 ± 0.000439928 (W 0.00146366) | · | `!` between-start range over 5% |
| `lu_factor_solve/n128/b1` | 0.12412 ± 0.00201912 (W 0.00226076) | 0.143707 ± 0.00044106 (W 0.000999988) | 🔵 tlinalg-pool 1.16× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.010289 ± 3.41565e-05 (W 8.55951e-05) | 0.015764 ± 0.000130449 (W 0.000157886) | 🔵 tlinalg-pool 1.53× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.138081 ± 0.00102486 (W 0.00307723) | 0.149757 ± 0.000615386 (W 0.00191584) | 🔵 tlinalg-pool 1.08× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 2.37647 ± 0.00188902 (W 0.00261572) | 1.14152 ± 0.00169936 (W 0.00256725) | 🔴 tlinalg-pool 2.08× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.007138 ± 9.10586e-05 (W 9.86153e-05) | 0.010119 ± 0.000365594 (W 0.000216709) | 🔵 tlinalg-pool 1.42× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.187959 ± 0.00152285 (W 0.00280749) | 0.409348 ± 0.00199171 (W 0.00307837) | 🔵 tlinalg-pool 2.18× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.350141 ± 0.00335503 (W 0.00444658) | 0.450431 ± 0.0018315 (W 0.00264609) | 🔵 tlinalg-pool 1.29× faster than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.271012 ± 0.00312387 (W 0.00249348) | 0.417436 ± 0.00120914 (W 0.00278952) | 🔵 tlinalg-pool 1.54× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.305878 ± 0.00243842 (W 0.00515817) | 0.448104 ± 0.000684027 (W 0.00214974) | 🔵 tlinalg-pool 1.46× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.031754 ± 0.000109479 (W 0.000110076) | 0.0252815 ± 6.70342e-05 (W 0.000140717) | 🔴 tlinalg-pool 1.26× slower than `lapack-mkl` |  |
| `solve/n128/b1` | 0.327182 ± 0.00116895 (W 0.00451576) | 0.463969 ± 0.00164177 (W 0.00195804) | 🔵 tlinalg-pool 1.42× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 3.26103 ± 0.00638476 (W 0.0127987) | 1.92164 ± 0.00986727 (W 0.00543672) | 🔴 tlinalg-pool 1.70× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.0187645 ± 8.97144e-05 (W 0.000104229) | 0.012954 ± 5.19615e-05 (W 9.07845e-05) | 🔴 tlinalg-pool 1.45× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 29.1749 ± 0.072167 (W 0.0794185) | 14.9922 ± 0.0328072 (W 0.0422729) | 🔴 tlinalg-pool 1.95× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 17.6522 ± 0.0473387 (W 0.0258605) | 12.6446 ± 0.0229647 (W 0.0116131) | 🔴 tlinalg-pool 1.40× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 1.76002 ± 0.00316849 (W 0.00497625) | 3.14314 ± 0.0472926 (W 0.0198665) | 🔵 tlinalg-pool 1.79× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 2.08716 ± 0.13318 (W 0.0181278) | 2.17973 ± 0.00396754 (W 0.00507886) | · | `!` between-start range over 5% |
| `qr/n512/b1` | 6.06002 ± 0.00523791 (W 0.009003) | 8.55763 ± 0.0276456 (W 0.0167526) | 🔵 tlinalg-pool 1.41× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 9.02999 ± 0.0274011 (W 0.0255858) | 24.7301 ± 0.108759 (W 0.0946693) | 🔵 tlinalg-pool 2.74× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 59.7688 ± 0.244838 (W 0.0572341) | 48.9218 ± 0.0930879 (W 0.064136) | 🔴 tlinalg-pool 1.22× slower than `lapack-mkl` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 40.4349 ± 0.43125 (W 0.365728) | 65.5663 ± 0.169379 (W 0.0720538) | 🔵 tlinalg-pool 1.62× faster than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 23.8219 ± 0.065593 (W 0.0549455) | 28.8931 ± 0.0583789 (W 0.0224125) | 🔵 tlinalg-pool 1.21× faster than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 5.6775 ± 0.0160003 (W 0.00859838) | 8.4166 ± 0.137729 (W 0.0111147) | 🔵 tlinalg-pool 1.48× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 5.63332 ± 0.00650171 (W 0.00728457) | 5.63259 ± 0.00342713 (W 0.00580989) | · |  |
| `qr/n512/b1` | 14.8809 ± 0.0075053 (W 0.0262273) | 15.3025 ± 0.0174279 (W 0.0263164) | · |  |
| `rank_revealing_qr/n512/b1` | 16.8189 ± 0.0545835 (W 0.0258467) | 60.5837 ± 0.0918355 (W 0.154234) | 🔵 tlinalg-pool 3.60× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 95.3558 ± 0.102113 (W 0.287231) | 85.3061 ± 0.760821 (W 0.0874368) | 🔴 tlinalg-pool 1.12× slower than `lapack-mkl` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 6.97688 ± 0.0143854 (W 0.0257235) | 6.18701 ± 0.0197274 (W 0.035676) | 🔴 tlinalg-pool 1.13× slower than `lapack-mkl` |  |
| `qr/4096x256/b1` | 23.4463 ± 0.0654522 (W 0.0534801) | 18.2969 ± 0.0507366 (W 0.0441115) | 🔴 tlinalg-pool 1.28× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 24.5803 ± 0.0972784 (W 0.0829737) | 61.0475 ± 2.0044 (W 0.944583) | 🔵 tlinalg-pool 2.48× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/4096x256/b1` | 40.7083 ± 0.16389 (W 0.0682436) | 34.287 ± 0.239118 (W 0.0739752) | 🔴 tlinalg-pool 1.19× slower than `lapack-mkl` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 18.7655 ± 0.037154 (W 0.0373203) | 17.0212 ± 0.141927 (W 0.159903) | 🔴 tlinalg-pool 1.10× slower than `lapack-mkl` |  |
| `qr/4096x256/b1` | 55.4432 ± 0.181878 (W 0.903627) | 40.1698 ± 0.173905 (W 0.177043) | 🔴 tlinalg-pool 1.38× slower than `lapack-mkl` |  |
| `rank_revealing_qr/4096x256/b1` | 61.5753 ± 0.700023 (W 0.876444) | 161.578 ± 1.06051 (W 0.520752) | 🔵 tlinalg-pool 2.62× faster than `lapack-mkl` |  |
| `svd_thin/4096x256/b1` | 110.764 ± 0.498402 (W 0.981802) | 73.6806 ± 0.415224 (W 0.309084) | 🔴 tlinalg-pool 1.50× slower than `lapack-mkl` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
