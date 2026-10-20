<!-- generated from data/results/zen5-cpu/tlinalg-competition/20261020T215232Z-verify-narrowed/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `4dcd35f080a6b4fd6b1423871af66a33fd398482`
- features: `tlinalg-bench/link-mkl`
- faer provider: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `8c1287010fb00be27de2ff72dfafa0e3a51c7ab4`
- toolkit commit: `e9760430705cfd3024a5da0d37502e80ec428059`
- measured binary SHA-256: `1cc3ca9b16c76de0b3c25d4c027be838f28ec38f401c14c3a62df4b7006e20ec`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T22:17:12.814671Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor mkl --aa 4 --reps 5 --prime-ms 250 --label verify-narrowed`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261020T215232Z-verify-narrowed/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.45%, worst 95.69% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 70 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.47%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.121606 ± 0.00237869 (W 0.00154702) | 1.056 ± 0.00499906 (W 0.00262263) | 🔵 tlinalg-pool 8.68× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.462256 ± 0.213866 (W 0.0122161) | 3.68226 ± 0.017886 (W 0.0182962) | 🔵 tlinalg-pool 7.97× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `cholesky/n4/b1024` | 0.030006 ± 0.000192588 (W 0.000887028) | 0.120394 ± 0.00426816 (W 0.00142392) | 🔵 tlinalg-pool 4.01× faster than `lapack-mkl` | `!` between-start range over 5% |
| `cholesky/n8/b1024` | 0.0536445 ± 0.000393714 (W 0.00103241) | 0.322405 ± 0.00308103 (W 0.00208426) | 🔵 tlinalg-pool 6.01× faster than `lapack-mkl` |  |
| `eig/n16/b1024` | 11.9316 ± 0.0168178 (W 0.0272405) | 52.7762 ± 0.0626004 (W 0.067591) | 🔵 tlinalg-pool 4.42× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 53.2071 ± 0.117634 (W 0.188094) | 283.706 ± 0.949039 (W 0.188217) | 🔵 tlinalg-pool 5.33× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 0.785547 ± 0.0200052 (W 0.00521261) | 2.83342 ± 0.00299599 (W 0.00551067) | 🔵 tlinalg-pool 3.61× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eig/n8/b1024` | 2.94833 ± 0.0362855 (W 0.00737106) | 11.675 ± 0.067638 (W 0.0301321) | 🔵 tlinalg-pool 3.96× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 3.74781 ± 0.0152911 (W 0.00567988) | 23.4827 ± 0.0893444 (W 0.0540381) | 🔵 tlinalg-pool 6.27× faster than `lapack-mkl` |  |
| `eigh/n32/b1024` | 14.3294 ± 0.0779087 (W 0.0212585) | 100.663 ± 0.325364 (W 0.352732) | 🔵 tlinalg-pool 7.02× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.318563 ± 0.0028685 (W 0.0019919) | 2.82322 ± 0.0118562 (W 0.00700393) | 🔵 tlinalg-pool 8.86× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.07701 ± 0.00623048 (W 0.00257358) | 7.73299 ± 0.0295757 (W 0.0157157) | 🔵 tlinalg-pool 7.18× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 8.16946 ± 0.047101 (W 0.0165768) | 36.5073 ± 0.0826389 (W 0.0472979) | 🔵 tlinalg-pool 4.47× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 36.3321 ± 0.0349917 (W 0.099252) | 169.323 ± 0.205683 (W 0.0950808) | 🔵 tlinalg-pool 4.66× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.409017 ± 0.00415587 (W 0.00245429) | 2.10652 ± 0.00777113 (W 0.00432676) | 🔵 tlinalg-pool 5.15× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 1.94011 ± 0.00572955 (W 0.00547737) | 8.92663 ± 0.0588898 (W 0.0172059) | 🔵 tlinalg-pool 4.60× faster than `lapack-mkl` |  |
| `eigvalsh/n16/b1024` | 2.79746 ± 0.00933589 (W 0.00420352) | 12.9566 ± 0.0118618 (W 0.0178961) | 🔵 tlinalg-pool 4.63× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 10.8985 ± 0.0421512 (W 0.0345427) | 43.0437 ± 0.0572277 (W 0.0275762) | 🔵 tlinalg-pool 3.95× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.263185 ± 0.0120034 (W 0.00214293) | 1.45673 ± 0.00545739 (W 0.00458291) | 🔵 tlinalg-pool 5.54× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eigvalsh/n8/b1024` | 0.858198 ± 0.00135313 (W 0.00237775) | 4.39312 ± 0.00777091 (W 0.00964448) | 🔵 tlinalg-pool 5.12× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.483691 ± 0.00730585 (W 0.007675) | 3.91803 ± 0.0507473 (W 0.00812744) | 🔵 tlinalg-pool 8.10× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 2.00754 ± 0.0334886 (W 0.022313) | 26.2629 ± 0.0668475 (W 0.0341475) | 🔵 tlinalg-pool 13.08× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.0831855 ± 0.000814367 (W 0.00241145) | 0.40023 ± 0.0019237 (W 0.0029399) | 🔵 tlinalg-pool 4.81× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 0.162934 ± 0.00161981 (W 0.00352367) | 0.984033 ± 0.00918252 (W 0.00253502) | 🔵 tlinalg-pool 6.04× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.45119 ± 0.00839727 (W 0.00437766) | 5.77847 ± 0.028728 (W 0.0108206) | 🔵 tlinalg-pool 12.81× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n32/b1024` | 1.47911 ± 0.0196214 (W 0.0160905) | 29.6368 ± 0.0897295 (W 0.0630729) | 🔵 tlinalg-pool 20.04× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.0748145 ± 0.00103573 (W 0.00294667) | 1.11298 ± 0.00477068 (W 0.0062395) | 🔵 tlinalg-pool 14.88× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.172626 ± 0.00632894 (W 0.00389568) | 1.93897 ± 0.0107034 (W 0.00453228) | 🔵 tlinalg-pool 11.23× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n16/b1024` | 0.616158 ± 0.00625151 (W 0.00357615) | 2.66743 ± 0.014905 (W 0.0184974) | 🔵 tlinalg-pool 4.33× faster than `lapack-mkl` |  |
| `householder_apply/n32/b1024` | 2.46837 ± 0.0548104 (W 0.00771775) | 13.0572 ± 0.151938 (W 0.0751233) | 🔵 tlinalg-pool 5.29× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.0544015 ± 0.00130761 (W 0.000547492) | 0.323087 ± 0.00211473 (W 0.00268647) | 🔵 tlinalg-pool 5.94× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.167156 ± 0.00166951 (W 0.00169292) | 0.802088 ± 0.00313458 (W 0.00838076) | 🔵 tlinalg-pool 4.80× faster than `lapack-mkl` |  |
| `householder_factor/n16/b1024` | 0.483381 ± 0.00571188 (W 0.00282935) | 2.95332 ± 0.0107464 (W 0.00609265) | 🔵 tlinalg-pool 6.11× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 1.68564 ± 0.0151862 (W 0.010412) | 12.3122 ± 0.0795421 (W 0.0377682) | 🔵 tlinalg-pool 7.30× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.0646655 ± 0.0133385 (W 0.000502017) | 0.306296 ± 0.000843377 (W 0.0019344) | 🔵 tlinalg-pool 4.74× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `householder_factor/n8/b1024` | 0.16671 ± 0.00164425 (W 0.00170395) | 0.844823 ± 0.00193488 (W 0.00165113) | 🔵 tlinalg-pool 5.07× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.360947 ± 0.00620923 (W 0.00791757) | 1.74714 ± 0.054895 (W 0.0095497) | 🔵 tlinalg-pool 4.84× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 1.2934 ± 0.0476024 (W 0.0202452) | 11.7919 ± 0.03303 (W 0.0252065) | 🔵 tlinalg-pool 9.12× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n4/b1024` | 0.072881 ± 0.00237852 (W 0.00279209) | 0.167577 ± 0.000955277 (W 0.000798285) | 🔵 tlinalg-pool 2.30× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.143387 ± 0.00242898 (W 0.00249593) | 0.499109 ± 0.00880948 (W 0.00261349) | 🔵 tlinalg-pool 3.48× faster than `lapack-mkl` |  |
| `lu_factor/n16/b1024` | 0.261622 ± 0.00142314 (W 0.00181453) | 1.19426 ± 0.0321788 (W 0.00235867) | 🔵 tlinalg-pool 4.56× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 0.754455 ± 0.00237821 (W 0.00461927) | 8.97074 ± 0.0369859 (W 0.0243152) | 🔵 tlinalg-pool 11.89× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.0616795 ± 0.00135633 (W 0.00192381) | 0.0665495 ± 0.00332041 (W 0.00142339) | 🔵 tlinalg-pool 1.08× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.108051 ± 0.000605489 (W 0.00147) | 0.26352 ± 0.00205984 (W 0.00216778) | 🔵 tlinalg-pool 2.44× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.335093 ± 0.00297363 (W 0.00233134) | 2.38985 ± 0.0301702 (W 0.0114445) | 🔵 tlinalg-pool 7.13× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 0.913478 ± 0.00754984 (W 0.00402883) | 13.9445 ± 0.0495587 (W 0.0415731) | 🔵 tlinalg-pool 15.27× faster than `lapack-mkl` |  |
| `lu_factor_solve/n4/b1024` | 0.0653015 ± 0.00175172 (W 0.00263859) | 0.182671 ± 0.00175467 (W 0.00148126) | 🔵 tlinalg-pool 2.80× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.130684 ± 0.00482292 (W 0.00142943) | 0.828128 ± 0.00331211 (W 0.00223364) | 🔵 tlinalg-pool 6.34× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1024` | 0.130608 ± 0.000986676 (W 0.000902833) | 1.06414 ± 0.0220334 (W 0.00546557) | 🔵 tlinalg-pool 8.15× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n32/b1024` | 0.314947 ± 0.00505309 (W 0.0102524) | 4.56719 ± 0.0320861 (W 0.0273012) | 🔵 tlinalg-pool 14.50× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n4/b1024` | 0.032581 ± 0.00154034 (W 0.00101987) | 0.133524 ± 0.000917668 (W 0.000760623) | 🔵 tlinalg-pool 4.10× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.055568 ± 0.000468844 (W 0.00136576) | 0.586542 ± 0.00201042 (W 0.0026807) | 🔵 tlinalg-pool 10.56× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.14411 ± 0.0229985 (W 0.0047767) | 5.26367 ± 0.0203896 (W 0.0138891) | 🔵 tlinalg-pool 4.60× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 4.52839 ± 0.0387685 (W 0.0281934) | 21.0132 ± 0.0528052 (W 0.0365718) | 🔵 tlinalg-pool 4.64× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.105401 ± 0.000586171 (W 0.000607712) | 0.724506 ± 0.0303314 (W 0.00325838) | 🔵 tlinalg-pool 6.87× faster than `lapack-mkl` | `!` between-start range over 5% |
| `qr/n8/b1024` | 0.309922 ± 0.016623 (W 0.00184263) | 1.68542 ± 0.0108696 (W 0.0042348) | 🔵 tlinalg-pool 5.44× faster than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/n16/b1024` | 1.30287 ± 0.0216488 (W 0.00418838) | 8.3419 ± 0.0566898 (W 0.0185861) | 🔵 tlinalg-pool 6.40× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n32/b1024` | 4.60245 ± 0.0765412 (W 0.0209092) | 31.0211 ± 0.0431944 (W 0.0591707) | 🔵 tlinalg-pool 6.74× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.160384 ± 0.00231577 (W 0.00177472) | 1.22276 ± 0.0111805 (W 0.00330205) | 🔵 tlinalg-pool 7.62× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.420799 ± 0.00417054 (W 0.00337789) | 2.91399 ± 0.00612433 (W 0.00714062) | 🔵 tlinalg-pool 6.92× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.354386 ± 0.00362849 (W 0.00236981) | 2.42507 ± 0.0211184 (W 0.00504438) | 🔵 tlinalg-pool 6.84× faster than `lapack-mkl` |  |
| `solve/n32/b1024` | 0.944541 ± 0.00723642 (W 0.0148452) | 13.4746 ± 0.0472758 (W 0.0210078) | 🔵 tlinalg-pool 14.27× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.054887 ± 0.000824336 (W 0.0010276) | 0.23129 ± 0.00364693 (W 0.00205204) | 🔵 tlinalg-pool 4.21× faster than `lapack-mkl` |  |
| `solve/n8/b1024` | 0.132221 ± 0.0020718 (W 0.00268931) | 0.89272 ± 0.00278028 (W 0.00248544) | 🔵 tlinalg-pool 6.75× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 7.11742 ± 0.504694 (W 0.112523) | 51.5429 ± 0.100078 (W 0.0559778) | 🔵 tlinalg-pool 7.24× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 26.8402 ± 1.04279 (W 0.329673) | 194.433 ± 0.372513 (W 0.2389) | 🔵 tlinalg-pool 7.24× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.565664 ± 0.0194703 (W 0.0236725) | 6.09128 ± 0.0189407 (W 0.0133952) | 🔵 tlinalg-pool 10.77× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 1.98392 ± 0.181571 (W 0.0126685) | 18.5901 ± 0.0397399 (W 0.0315521) | 🔵 tlinalg-pool 9.37× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.22998 ± 0.130381 (W 0.104104) | 51.3581 ± 0.0924534 (W 0.0548919) | 🔵 tlinalg-pool 7.10× faster than `lapack-mkl` |  |
| `svd_thin/n32/b1024` | 25.8891 ± 0.212137 (W 0.0939896) | 194.618 ± 0.555514 (W 0.202059) | 🔵 tlinalg-pool 7.52× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1024` | 0.583554 ± 0.0427739 (W 0.00269515) | 6.08683 ± 0.00901789 (W 0.00629693) | 🔵 tlinalg-pool 10.43× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 1.9441 ± 0.183939 (W 0.00483177) | 18.5729 ± 0.0566969 (W 0.0323642) | 🔵 tlinalg-pool 9.55× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 5.18946 ± 0.0467734 (W 0.0253505) | 19.2555 ± 0.0360632 (W 0.0245227) | 🔵 tlinalg-pool 3.71× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 20.1271 ± 0.0597423 (W 0.0193201) | 64.7517 ± 0.0929919 (W 0.227805) | 🔵 tlinalg-pool 3.22× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.412333 ± 0.00215029 (W 0.00532137) | 2.67339 ± 0.0108872 (W 0.00613369) | 🔵 tlinalg-pool 6.48× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.45567 ± 0.0159755 (W 0.00597205) | 6.68622 ± 0.0128886 (W 0.012011) | 🔵 tlinalg-pool 4.59× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.0854245 ± 0.00087811 (W 0.00254948) | 0.594836 ± 0.00797623 (W 0.00376138) | 🔵 tlinalg-pool 6.96× faster than `lapack-mkl` |  |
| `triangular_solve/n32/b1024` | 0.189663 ± 0.00263774 (W 0.00563782) | 2.44578 ± 0.0179001 (W 0.0130905) | 🔵 tlinalg-pool 12.90× faster than `lapack-mkl` |  |
| `triangular_solve/n4/b1024` | 0.0189505 ± 0.00709933 (W 0.000805262) | 0.294478 ± 0.00747112 (W 0.00254375) | 🔵 tlinalg-pool 15.54× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.03496 ± 0.000188229 (W 0.000623236) | 0.397275 ± 0.00448465 (W 0.00289698) | 🔵 tlinalg-pool 11.36× faster than `lapack-mkl` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.173364 ± 0.00322754 (W 0.00303411) | 1.79841 ± 0.0172309 (W 0.0143502) | 🔵 tlinalg-pool 10.37× faster than `lapack-mkl` |  |
| `cholesky/n32/b1024` | 0.808486 ± 0.0162844 (W 0.0042831) | 8.8493 ± 0.025694 (W 0.0252183) | 🔵 tlinalg-pool 10.95× faster than `lapack-mkl` |  |
| `cholesky/n4/b1024` | 0.032721 ± 0.000564251 (W 0.000453778) | 0.178227 ± 0.000737568 (W 0.00165621) | 🔵 tlinalg-pool 5.45× faster than `lapack-mkl` |  |
| `cholesky/n8/b1024` | 0.0604275 ± 0.00157147 (W 0.000936475) | 0.470487 ± 0.0119452 (W 0.00302609) | 🔵 tlinalg-pool 7.79× faster than `lapack-mkl` | `!` between-start range over 5% |
| `eig/n16/b1024` | 16.4433 ± 0.0333485 (W 0.0737915) | 175.394 ± 0.193957 (W 0.311316) | 🔵 tlinalg-pool 10.67× faster than `lapack-mkl` |  |
| `eig/n32/b1024` | 67.3984 ± 0.33371 (W 0.181206) | 793.593 ± 1.13117 (W 1.05096) | 🔵 tlinalg-pool 11.77× faster than `lapack-mkl` |  |
| `eig/n4/b1024` | 1.30493 ± 0.0100795 (W 0.0141901) | 12.4539 ± 0.0223056 (W 0.0203771) | 🔵 tlinalg-pool 9.54× faster than `lapack-mkl` |  |
| `eig/n8/b1024` | 4.46184 ± 0.0311922 (W 0.0172622) | 43.2435 ± 0.0674282 (W 0.0401267) | 🔵 tlinalg-pool 9.69× faster than `lapack-mkl` |  |
| `eigh/n16/b1024` | 4.06105 ± 0.477726 (W 0.0313327) | 32.2381 ± 0.184573 (W 0.0279093) | 🔵 tlinalg-pool 7.94× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigh/n32/b1024` | 17.9443 ± 0.0691245 (W 0.0270159) | 152.062 ± 0.405791 (W 0.233277) | 🔵 tlinalg-pool 8.47× faster than `lapack-mkl` |  |
| `eigh/n4/b1024` | 0.378531 ± 0.004092 (W 0.00184677) | 2.82244 ± 0.0347823 (W 0.00542107) | 🔵 tlinalg-pool 7.46× faster than `lapack-mkl` |  |
| `eigh/n8/b1024` | 1.15495 ± 0.00335156 (W 0.00213873) | 8.91985 ± 0.00959031 (W 0.0137286) | 🔵 tlinalg-pool 7.72× faster than `lapack-mkl` |  |
| `eigvals/n16/b1024` | 9.69366 ± 0.0161279 (W 0.0276532) | 124.922 ± 0.0316303 (W 0.0808156) | 🔵 tlinalg-pool 12.89× faster than `lapack-mkl` |  |
| `eigvals/n32/b1024` | 42.4887 ± 0.0728142 (W 0.183488) | 523.51 ± 0.365211 (W 0.538437) | 🔵 tlinalg-pool 12.32× faster than `lapack-mkl` |  |
| `eigvals/n4/b1024` | 0.613599 ± 0.0114077 (W 0.010526) | 9.56403 ± 0.00625228 (W 0.0156493) | 🔵 tlinalg-pool 15.59× faster than `lapack-mkl` |  |
| `eigvals/n8/b1024` | 2.54607 ± 0.237655 (W 0.00853226) | 34.3614 ± 0.0444391 (W 0.0257885) | 🔵 tlinalg-pool 13.50× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigvalsh/n16/b1024` | 3.03481 ± 0.0573121 (W 0.00798423) | 18.3868 ± 0.00784189 (W 0.0193171) | 🔵 tlinalg-pool 6.06× faster than `lapack-mkl` |  |
| `eigvalsh/n32/b1024` | 11.917 ± 0.0806169 (W 0.0555404) | 77.4789 ± 0.0173485 (W 0.0355516) | 🔵 tlinalg-pool 6.50× faster than `lapack-mkl` |  |
| `eigvalsh/n4/b1024` | 0.309251 ± 0.00172078 (W 0.00172928) | 1.78252 ± 0.00409837 (W 0.00334899) | 🔵 tlinalg-pool 5.76× faster than `lapack-mkl` |  |
| `eigvalsh/n8/b1024` | 0.929762 ± 0.00357479 (W 0.00270853) | 5.58392 ± 0.00774665 (W 0.00911304) | 🔵 tlinalg-pool 6.01× faster than `lapack-mkl` |  |
| `full_piv_lu/n16/b1024` | 0.621653 ± 0.00834721 (W 0.00762647) | 5.57642 ± 0.117981 (W 0.0150546) | 🔵 tlinalg-pool 8.97× faster than `lapack-mkl` |  |
| `full_piv_lu/n32/b1024` | 3.04533 ± 0.0328277 (W 0.0378511) | 27.0181 ± 0.140721 (W 0.047077) | 🔵 tlinalg-pool 8.87× faster than `lapack-mkl` |  |
| `full_piv_lu/n4/b1024` | 0.088395 ± 0.000742232 (W 0.00212617) | 0.519534 ± 0.00426149 (W 0.00283793) | 🔵 tlinalg-pool 5.88× faster than `lapack-mkl` |  |
| `full_piv_lu/n8/b1024` | 0.196401 ± 0.002794 (W 0.00379327) | 1.31036 ± 0.0233579 (W 0.00324217) | 🔵 tlinalg-pool 6.67× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n16/b1024` | 0.701342 ± 0.176973 (W 0.00814064) | 8.44998 ± 0.0416518 (W 0.0205723) | 🔵 tlinalg-pool 12.05× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `full_piv_lu_solve/n32/b1024` | 2.65749 ± 0.0112326 (W 0.00627269) | 34.5518 ± 0.0364858 (W 0.0415497) | 🔵 tlinalg-pool 13.00× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n4/b1024` | 0.106182 ± 0.0025064 (W 0.00257367) | 1.59675 ± 0.00427573 (W 0.00519253) | 🔵 tlinalg-pool 15.04× faster than `lapack-mkl` |  |
| `full_piv_lu_solve/n8/b1024` | 0.264273 ± 0.00136225 (W 0.00229533) | 3.15822 ± 0.0202753 (W 0.00481074) | 🔵 tlinalg-pool 11.95× faster than `lapack-mkl` |  |
| `householder_apply/n16/b1024` | 0.636 ± 0.0192611 (W 0.0102557) | 6.19001 ± 0.0893384 (W 0.0229932) | 🔵 tlinalg-pool 9.73× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 3.52716 ± 0.030043 (W 0.0208449) | 37.8521 ± 0.188014 (W 0.0757596) | 🔵 tlinalg-pool 10.73× faster than `lapack-mkl` |  |
| `householder_apply/n4/b1024` | 0.0503635 ± 0.00414148 (W 0.00152745) | 0.416065 ± 0.00209416 (W 0.00543492) | 🔵 tlinalg-pool 8.26× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.156632 ± 0.00337081 (W 0.00370772) | 1.27306 ± 0.0137394 (W 0.00453788) | 🔵 tlinalg-pool 8.13× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.580852 ± 0.00487671 (W 0.00416013) | 6.29767 ± 0.0306936 (W 0.0103353) | 🔵 tlinalg-pool 10.84× faster than `lapack-mkl` |  |
| `householder_factor/n32/b1024` | 2.6052 ± 0.0334947 (W 0.0218756) | 27.4504 ± 0.08103 (W 0.031061) | 🔵 tlinalg-pool 10.54× faster than `lapack-mkl` |  |
| `householder_factor/n4/b1024` | 0.075135 ± 0.000446439 (W 0.000542159) | 0.516177 ± 0.00301964 (W 0.00236094) | 🔵 tlinalg-pool 6.87× faster than `lapack-mkl` |  |
| `householder_factor/n8/b1024` | 0.196511 ± 0.000678453 (W 0.00175495) | 1.4871 ± 0.00611152 (W 0.00344517) | 🔵 tlinalg-pool 7.57× faster than `lapack-mkl` |  |
| `lu/n16/b1024` | 0.44003 ± 0.00484161 (W 0.00809407) | 3.57708 ± 0.211586 (W 0.0175123) | 🔵 tlinalg-pool 8.13× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu/n32/b1024` | 2.15443 ± 0.0445072 (W 0.0183997) | 19.7081 ± 0.125036 (W 0.0438559) | 🔵 tlinalg-pool 9.15× faster than `lapack-mkl` |  |
| `lu/n4/b1024` | 0.070622 ± 0.0010373 (W 0.00144865) | 0.28456 ± 0.0433377 (W 0.00231896) | 🔵 tlinalg-pool 4.03× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu/n8/b1024` | 0.155469 ± 0.000494925 (W 0.00390492) | 0.893088 ± 0.0907577 (W 0.00195389) | 🔵 tlinalg-pool 5.74× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.293417 ± 0.00674373 (W 0.0116637) | 2.65038 ± 0.0092202 (W 0.0049128) | 🔵 tlinalg-pool 9.03× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 1.27303 ± 0.0177549 (W 0.0212376) | 15.5367 ± 0.0449932 (W 0.0310101) | 🔵 tlinalg-pool 12.20× faster than `lapack-mkl` |  |
| `lu_factor/n4/b1024` | 0.069199 ± 0.00233399 (W 0.000857185) | 0.182981 ± 0.00053724 (W 0.00175373) | 🔵 tlinalg-pool 2.64× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.116241 ± 0.00142189 (W 0.00252596) | 0.621463 ± 0.00166102 (W 0.00267804) | 🔵 tlinalg-pool 5.35× faster than `lapack-mkl` |  |
| `lu_factor_solve/n16/b1024` | 0.476187 ± 0.00763988 (W 0.00877875) | 5.2816 ± 0.0125948 (W 0.00806216) | 🔵 tlinalg-pool 11.09× faster than `lapack-mkl` |  |
| `lu_factor_solve/n32/b1024` | 1.84965 ± 0.0445352 (W 0.0265043) | 21.1286 ± 0.0843237 (W 0.0736158) | 🔵 tlinalg-pool 11.42× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n4/b1024` | 0.080315 ± 0.00247729 (W 0.00109621) | 0.415484 ± 0.00354636 (W 0.00256839) | 🔵 tlinalg-pool 5.17× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.172837 ± 0.0018201 (W 0.00143852) | 1.66619 ± 0.00791159 (W 0.00250563) | 🔵 tlinalg-pool 9.64× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n16/b1024` | 0.207797 ± 0.0171933 (W 0.00654444) | 2.6259 ± 0.0135436 (W 0.010536) | 🔵 tlinalg-pool 12.64× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n32/b1024` | 0.867197 ± 0.01092 (W 0.0172731) | 5.66791 ± 0.125035 (W 0.0996096) | 🔵 tlinalg-pool 6.54× faster than `lapack-mkl` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.0455955 ± 0.000540081 (W 0.00161651) | 0.241335 ± 0.00113386 (W 0.00132768) | 🔵 tlinalg-pool 5.29× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n8/b1024` | 0.0876935 ± 0.00148239 (W 0.000997389) | 1.07515 ± 0.00232468 (W 0.00176766) | 🔵 tlinalg-pool 12.26× faster than `lapack-mkl` |  |
| `qr/n16/b1024` | 1.4044 ± 0.0122321 (W 0.00593186) | 10.5538 ± 0.0564987 (W 0.0202349) | 🔵 tlinalg-pool 7.51× faster than `lapack-mkl` |  |
| `qr/n32/b1024` | 9.33379 ± 0.039464 (W 0.0193785) | 49.5435 ± 0.14507 (W 0.0342353) | 🔵 tlinalg-pool 5.31× faster than `lapack-mkl` |  |
| `qr/n4/b1024` | 0.117885 ± 0.000417618 (W 0.0010384) | 0.92321 ± 0.00364486 (W 0.00247312) | 🔵 tlinalg-pool 7.83× faster than `lapack-mkl` |  |
| `qr/n8/b1024` | 0.341927 ± 0.00588858 (W 0.00379584) | 2.66796 ± 0.0514307 (W 0.00640667) | 🔵 tlinalg-pool 7.80× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n16/b1024` | 1.58768 ± 0.0780705 (W 0.0522101) | 15.8708 ± 0.0828307 (W 0.0238319) | 🔵 tlinalg-pool 10.00× faster than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/n32/b1024` | 8.61367 ± 0.0102682 (W 0.0483492) | 69.4617 ± 0.153003 (W 0.0629084) | 🔵 tlinalg-pool 8.06× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n4/b1024` | 0.185044 ± 0.0019961 (W 0.00134591) | 1.7521 ± 0.00401051 (W 0.00707548) | 🔵 tlinalg-pool 9.47× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n8/b1024` | 0.483617 ± 0.00874206 (W 0.00251864) | 4.73709 ± 0.0260353 (W 0.00983401) | 🔵 tlinalg-pool 9.80× faster than `lapack-mkl` |  |
| `solve/n16/b1024` | 0.518392 ± 0.00956028 (W 0.0161653) | 5.58063 ± 0.0289174 (W 0.00865029) | 🔵 tlinalg-pool 10.77× faster than `lapack-mkl` |  |
| `solve/n32/b1024` | 1.81743 ± 0.0097747 (W 0.0101357) | 21.4786 ± 0.025381 (W 0.0252269) | 🔵 tlinalg-pool 11.82× faster than `lapack-mkl` |  |
| `solve/n4/b1024` | 0.077113 ± 0.00272944 (W 0.0021663) | 0.477595 ± 0.00211723 (W 0.00236312) | 🔵 tlinalg-pool 6.19× faster than `lapack-mkl` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.18553 ± 0.00102222 (W 0.00180009) | 1.76741 ± 0.0190619 (W 0.00302924) | 🔵 tlinalg-pool 9.53× faster than `lapack-mkl` |  |
| `svd_full/n16/b1024` | 7.81511 ± 0.0717807 (W 0.0633612) | 67.551 ± 0.0903696 (W 0.060876) | 🔵 tlinalg-pool 8.64× faster than `lapack-mkl` |  |
| `svd_full/n32/b1024` | 33.3445 ± 0.106819 (W 0.0274504) | 285.392 ± 0.975622 (W 0.593116) | 🔵 tlinalg-pool 8.56× faster than `lapack-mkl` |  |
| `svd_full/n4/b1024` | 0.642908 ± 0.00984228 (W 0.00184133) | 7.39152 ± 0.0152648 (W 0.0165202) | 🔵 tlinalg-pool 11.50× faster than `lapack-mkl` |  |
| `svd_full/n8/b1024` | 2.18547 ± 0.0258755 (W 0.0796521) | 22.1487 ± 0.0264823 (W 0.0292237) | 🔵 tlinalg-pool 10.13× faster than `lapack-mkl` |  |
| `svd_thin/n16/b1024` | 8.12453 ± 0.596378 (W 0.113471) | 67.3997 ± 0.100529 (W 0.0890074) | 🔵 tlinalg-pool 8.30× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_thin/n32/b1024` | 33.3332 ± 0.747337 (W 0.044308) | 286.197 ± 1.04957 (W 0.288326) | 🔵 tlinalg-pool 8.59× faster than `lapack-mkl` |  |
| `svd_thin/n4/b1024` | 0.641545 ± 0.0103913 (W 0.00232642) | 7.38461 ± 0.0145112 (W 0.0188571) | 🔵 tlinalg-pool 11.51× faster than `lapack-mkl` |  |
| `svd_thin/n8/b1024` | 2.16662 ± 0.0540666 (W 0.00577077) | 22.1473 ± 0.0353436 (W 0.024648) | 🔵 tlinalg-pool 10.22× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 5.80778 ± 0.10072 (W 0.0172) | 28.2591 ± 0.0803377 (W 0.0466292) | 🔵 tlinalg-pool 4.87× faster than `lapack-mkl` |  |
| `svd_values/n32/b1024` | 22.3648 ± 0.0194513 (W 0.0290461) | 105.96 ± 0.249328 (W 0.0438984) | 🔵 tlinalg-pool 4.74× faster than `lapack-mkl` |  |
| `svd_values/n4/b1024` | 0.492733 ± 0.00233315 (W 0.00233874) | 3.51227 ± 0.00825161 (W 0.00640414) | 🔵 tlinalg-pool 7.13× faster than `lapack-mkl` |  |
| `svd_values/n8/b1024` | 1.65043 ± 0.00453485 (W 0.00628035) | 9.11357 ± 0.0273703 (W 0.0182357) | 🔵 tlinalg-pool 5.52× faster than `lapack-mkl` |  |
| `triangular_solve/n16/b1024` | 0.142841 ± 0.00384874 (W 0.00740819) | 1.33724 ± 0.0384065 (W 0.00366983) | 🔵 tlinalg-pool 9.36× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 0.539736 ± 0.252901 (W 0.0113826) | 3.56187 ± 0.030996 (W 0.0255159) | 🔵 tlinalg-pool 6.60× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n4/b1024` | 0.0280625 ± 0.000659926 (W 0.000936743) | 0.302073 ± 0.000953517 (W 0.00210788) | 🔵 tlinalg-pool 10.76× faster than `lapack-mkl` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.065492 ± 0.00046021 (W 0.00110029) | 0.584052 ± 0.00559501 (W 0.00344394) | 🔵 tlinalg-pool 8.92× faster than `lapack-mkl` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.066459 ± 0.000630893 (W 0.000138984) | 0.0941155 ± 0.000481287 (W 0.0010573) | 🔵 tlinalg-pool 1.42× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.185446 ± 0.00385348 (W 0.0062456) | 0.136149 ± 0.000407392 (W 0.00112943) | 🔴 tlinalg-pool 1.36× slower than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.126771 ± 0.00120733 (W 0.00284903) | 0.12106 ± 0.000175549 (W 0.00095346) | · |  |
| `lu_factor_solve/n128/b1` | 0.134817 ± 0.0011646 (W 0.00429039) | 0.144019 ± 0.000851477 (W 0.00167171) | 🔵 tlinalg-pool 1.07× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.009928 ± 3.90758e-05 (W 0.000120485) | 0.016556 ± 5.25198e-05 (W 0.000297585) | 🔵 tlinalg-pool 1.67× faster than `lapack-mkl` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.149193 ± 0.00187656 (W 0.00452737) | 0.150891 ± 0.000601184 (W 0.00119282) | · |  |
| `svd_values/n128/b1` | 2.38738 ± 0.00651744 (W 0.00262694) | 1.13233 ± 0.00443002 (W 0.00302846) | 🔴 tlinalg-pool 2.11× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.0068575 ± 7.90907e-05 (W 7.45264e-05) | 0.0104045 ± 0.000504383 (W 0.000240707) | 🔵 tlinalg-pool 1.52× faster than `lapack-mkl` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.187138 ± 0.000541455 (W 0.00239505) | 0.409728 ± 0.00170022 (W 0.00333755) | 🔵 tlinalg-pool 2.19× faster than `lapack-mkl` |  |
| `lu/n128/b1` | 0.342293 ± 0.00224635 (W 0.00467664) | 0.451326 ± 0.0014239 (W 0.00285133) | 🔵 tlinalg-pool 1.32× faster than `lapack-mkl` |  |
| `lu_factor/n128/b1` | 0.262019 ± 0.00149553 (W 0.00305705) | 0.415199 ± 0.00127375 (W 0.00298318) | 🔵 tlinalg-pool 1.58× faster than `lapack-mkl` |  |
| `lu_factor_solve/n128/b1` | 0.28965 ± 0.00207095 (W 0.00283012) | 0.446241 ± 0.00193535 (W 0.00205305) | 🔵 tlinalg-pool 1.54× faster than `lapack-mkl` |  |
| `lu_solve_prepared/n128/b1` | 0.0312485 ± 0.000162574 (W 0.00011645) | 0.0251265 ± 0.000131226 (W 9.79448e-05) | 🔴 tlinalg-pool 1.24× slower than `lapack-mkl` |  |
| `solve/n128/b1` | 0.316584 ± 0.00320948 (W 0.00515612) | 0.463139 ± 0.000578367 (W 0.00276384) | 🔵 tlinalg-pool 1.46× faster than `lapack-mkl` |  |
| `svd_values/n128/b1` | 3.15856 ± 0.00961659 (W 0.00540219) | 1.92098 ± 0.00552202 (W 0.00562493) | 🔴 tlinalg-pool 1.64× slower than `lapack-mkl` |  |
| `triangular_solve/n128/b1` | 0.01864 ± 0.000108152 (W 0.000121584) | 0.013009 ± 6.89704e-05 (W 9.18845e-05) | 🔴 tlinalg-pool 1.43× slower than `lapack-mkl` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 23.6612 ± 0.10555 (W 0.110916) | 15.038 ± 0.0728209 (W 0.0355972) | 🔴 tlinalg-pool 1.57× slower than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 18.5617 ± 0.0338739 (W 0.0346088) | 12.6663 ± 0.0200189 (W 0.0127108) | 🔴 tlinalg-pool 1.47× slower than `lapack-mkl` |  |
| `householder_apply/n512/b1` | 2.73573 ± 0.0321844 (W 0.0524102) | 3.1582 ± 0.0766923 (W 0.0272867) | 🔵 tlinalg-pool 1.15× faster than `lapack-mkl` | `!` between-start range over 5% |
| `householder_factor/n512/b1` | 2.66062 ± 0.0242662 (W 0.0329361) | 2.1333 ± 0.00375801 (W 0.00374449) | 🔴 tlinalg-pool 1.25× slower than `lapack-mkl` |  |
| `qr/n512/b1` | 7.84731 ± 0.0534165 (W 0.077981) | 8.74615 ± 0.0145672 (W 0.0249704) | 🔵 tlinalg-pool 1.11× faster than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 9.6927 ± 0.14648 (W 0.144917) | 24.6562 ± 0.211599 (W 0.0746781) | 🔵 tlinalg-pool 2.54× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 60.7376 ± 0.197726 (W 0.135853) | 49.131 ± 0.0549404 (W 0.170158) | 🔴 tlinalg-pool 1.24× slower than `lapack-mkl` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 39.1729 ± 0.531057 (W 0.490657) | 65.8481 ± 0.086262 (W 0.118165) | 🔵 tlinalg-pool 1.68× faster than `lapack-mkl` |  |
| `eigvalsh/n512/b1` | 28.8647 ± 0.0685283 (W 0.0615579) | 28.9568 ± 0.806039 (W 0.109505) | · | `!` between-start range over 5% |
| `householder_apply/n512/b1` | 7.06691 ± 0.033475 (W 0.103459) | 8.12216 ± 0.0128529 (W 0.0148617) | 🔵 tlinalg-pool 1.15× faster than `lapack-mkl` |  |
| `householder_factor/n512/b1` | 6.94726 ± 0.0697756 (W 0.120228) | 5.45011 ± 0.0443646 (W 0.00953294) | 🔴 tlinalg-pool 1.27× slower than `lapack-mkl` |  |
| `qr/n512/b1` | 16.7766 ± 0.0802107 (W 0.168827) | 15.2289 ± 0.0573613 (W 0.0281039) | 🔴 tlinalg-pool 1.10× slower than `lapack-mkl` |  |
| `rank_revealing_qr/n512/b1` | 18.8542 ± 0.120696 (W 0.130801) | 59.6579 ± 0.390596 (W 0.141225) | 🔵 tlinalg-pool 3.16× faster than `lapack-mkl` |  |
| `svd_thin/n512/b1` | 100.861 ± 0.432426 (W 0.600913) | 86.5714 ± 0.1206 (W 0.216242) | 🔴 tlinalg-pool 1.17× slower than `lapack-mkl` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 7.84882 ± 0.982383 (W 0.0352985) | 6.14661 ± 0.28496 (W 0.0351048) | 🔴 tlinalg-pool 1.28× slower than `lapack-mkl` | `!` between-start range over 5% |
| `qr/4096x256/b1` | 22.5045 ± 1.47175 (W 0.565956) | 18.9593 ± 2.43203 (W 0.0872895) | 🔴 tlinalg-pool 1.19× slower than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/4096x256/b1` | 24.3732 ± 3.98711 (W 0.467811) | 63.204 ± 18.767 (W 1.12433) | 🔵 tlinalg-pool 2.59× faster than `lapack-mkl` | `!` between-start range over 5% |
| `svd_thin/4096x256/b1` | 39.6408 ± 1.9777 (W 0.399292) | 34.6223 ± 3.91767 (W 0.153239) | 🔴 tlinalg-pool 1.14× slower than `lapack-mkl` | `!` between-start range over 5% |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-mkl (ms) | vs `lapack-mkl` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 19.9705 ± 1.13992 (W 0.0807203) | 16.889 ± 2.42121 (W 0.0951264) | 🔴 tlinalg-pool 1.18× slower than `lapack-mkl` | `!` between-start range over 5% |
| `qr/4096x256/b1` | 53.5904 ± 1.62775 (W 0.122476) | 40.8881 ± 4.13948 (W 0.120474) | 🔴 tlinalg-pool 1.31× slower than `lapack-mkl` | `!` between-start range over 5% |
| `rank_revealing_qr/4096x256/b1` | 60.7077 ± 14.6941 (W 0.3409) | 162.302 ± 14.7213 (W 0.772922) | 🔵 tlinalg-pool 2.67× faster than `lapack-mkl` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_thin/4096x256/b1` | 115.649 ± 5.50524 (W 0.483385) | 76.0307 ± 4.37265 (W 0.505635) | 🔴 tlinalg-pool 1.52× slower than `lapack-mkl` | `!` between-start range over 5% |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
