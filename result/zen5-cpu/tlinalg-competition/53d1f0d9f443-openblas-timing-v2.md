<!-- generated from data/results/zen5-cpu/tlinalg-competition/20261031T125207Z-pub-53d1f0d9-20261031-competition-openblas/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `f00d46158eeb5cacf198bceba6197d5eb2043afc`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `028b45886580e5353ddee46798f3d2cd7cf52f7521251264812b3a908590da86`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-31T13:12:47.858146Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 1 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor openblas --aa 4 --reps 5 --prime-ms 250 --label pub-53d1f0d9-20261031-competition-openblas`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261031T125207Z-pub-53d1f0d9-20261031-competition-openblas/`

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
- CPU sets: 8T -> `4-11`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 4 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.42%, worst 44.91% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 31 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.30%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.113637 ± 0.000702971 (W 0.00146877) | 1.0144 ± 0.00941944 (W 0.00295457) | 🔵 tlinalg-pool 8.93× faster than `lapack-openblas` |  |
| `cholesky/n32/b1024` | 0.473548 ± 0.0204748 (W 0.00380976) | 3.6075 ± 0.0349977 (W 0.0103144) | 🔵 tlinalg-pool 7.62× faster than `lapack-openblas` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.178849 ± 0.00113335 (W 0.00170774) | 0.19552 ± 0.00122606 (W 0.00166425) | 🔵 tlinalg-pool 1.09× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.0473985 ± 0.000402236 (W 5.98449e-05) | 0.399275 ± 0.0164214 (W 0.00296936) | 🔵 tlinalg-pool 8.42× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eig/n16/b1024` | 12.1179 ± 0.060568 (W 0.0106715) | 68.6138 ± 0.440776 (W 0.232486) | 🔵 tlinalg-pool 5.66× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 54.1907 ± 0.21907 (W 0.230475) | 323.455 ± 1.9205 (W 0.460581) | 🔵 tlinalg-pool 5.97× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 0.81181 ± 0.00258999 (W 0.0024569) | 5.32108 ± 0.0269894 (W 0.00854824) | 🔵 tlinalg-pool 6.55× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 3.03126 ± 0.0159111 (W 0.00647191) | 17.4806 ± 0.101067 (W 0.0213814) | 🔵 tlinalg-pool 5.77× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 3.78046 ± 0.0180345 (W 0.00511951) | 40.2435 ± 0.240105 (W 0.0747414) | 🔵 tlinalg-pool 10.65× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 13.9953 ± 0.0140153 (W 0.0109558) | 117.371 ± 1.14203 (W 0.128688) | 🔵 tlinalg-pool 8.39× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 0.322522 ± 0.00264501 (W 0.00262968) | 3.02853 ± 0.047657 (W 0.005041) | 🔵 tlinalg-pool 9.39× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.09772 ± 0.00696365 (W 0.00287568) | 10.8607 ± 0.103804 (W 0.0167573) | 🔵 tlinalg-pool 9.89× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 8.37632 ± 0.0309983 (W 0.00801003) | 49.6668 ± 0.34083 (W 0.0455797) | 🔵 tlinalg-pool 5.93× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 36.7128 ± 0.0834891 (W 0.0502087) | 218.867 ± 0.529766 (W 0.461716) | 🔵 tlinalg-pool 5.96× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.439795 ± 0.00327809 (W 0.00224756) | 3.42441 ± 0.0212902 (W 0.00535561) | 🔵 tlinalg-pool 7.79× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 2.0019 ± 0.00612204 (W 0.00517038) | 13.23 ± 0.020519 (W 0.0126543) | 🔵 tlinalg-pool 6.61× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 2.85802 ± 0.0177015 (W 0.00493553) | 14.566 ± 0.0691657 (W 0.0109715) | 🔵 tlinalg-pool 5.10× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 10.6853 ± 0.0401972 (W 0.00772998) | 49.975 ± 0.146727 (W 0.0378518) | 🔵 tlinalg-pool 4.68× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.264394 ± 0.00479905 (W 0.0017066) | 1.39248 ± 0.00893127 (W 0.00509385) | 🔵 tlinalg-pool 5.27× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.882705 ± 0.00762956 (W 0.00289559) | 4.54011 ± 0.0375614 (W 0.00620435) | 🔵 tlinalg-pool 5.14× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.511039 ± 0.00555535 (W 0.00438864) | 4.74741 ± 0.131469 (W 0.0189384) | 🔵 tlinalg-pool 9.29× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 2.01948 ± 0.0294496 (W 0.00633381) | 28.4704 ± 0.444058 (W 0.122104) | 🔵 tlinalg-pool 14.10× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1024` | 0.493667 ± 0.00360875 (W 0.00379742) | 0.37206 ± 0.00432701 (W 0.00220794) | 🔴 tlinalg-pool 1.33× slower than `lapack-openblas` |  |
| `full_piv_lu/n8/b1024` | 0.181084 ± 0.00161244 (W 0.00213312) | 1.03839 ± 0.0108366 (W 0.00366431) | 🔵 tlinalg-pool 5.73× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n16/b1024` | 0.517367 ± 0.00424877 (W 0.00302689) | 6.39387 ± 0.166147 (W 0.0326794) | 🔵 tlinalg-pool 12.36× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n32/b1024` | 1.67728 ± 0.0264198 (W 0.0172894) | 30.7264 ± 1.02755 (W 0.130431) | 🔵 tlinalg-pool 18.32× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n4/b1024` | 0.084643 ± 0.000454001 (W 0.000333903) | 0.950705 ± 0.00543087 (W 0.00198699) | 🔵 tlinalg-pool 11.23× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n8/b1024` | 0.205689 ± 0.000799246 (W 0.00231976) | 1.98263 ± 0.0193922 (W 0.00593324) | 🔵 tlinalg-pool 9.64× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.62197 ± 0.0267052 (W 0.00191618) | 4.4854 ± 0.0275885 (W 0.00823738) | 🔵 tlinalg-pool 7.21× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 2.44853 ± 0.0664279 (W 0.00906694) | 19.3162 ± 0.280287 (W 0.0624283) | 🔵 tlinalg-pool 7.89× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.0543915 ± 0.00182311 (W 0.000904463) | 0.414374 ± 0.00191379 (W 0.00253759) | 🔵 tlinalg-pool 7.62× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.171665 ± 0.00735371 (W 0.00167355) | 1.20516 ± 0.00941745 (W 0.00349716) | 🔵 tlinalg-pool 7.02× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.509896 ± 0.00393539 (W 0.00199243) | 4.3828 ± 0.016638 (W 0.00734207) | 🔵 tlinalg-pool 8.60× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 1.68705 ± 0.0256475 (W 0.00521465) | 14.7129 ± 0.0439735 (W 0.020967) | 🔵 tlinalg-pool 8.72× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.063884 ± 0.00018518 (W 0.00137804) | 0.542114 ± 0.00155842 (W 0.00266131) | 🔵 tlinalg-pool 8.49× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.168395 ± 0.00228822 (W 0.00113771) | 1.5137 ± 0.010886 (W 0.00236105) | 🔵 tlinalg-pool 8.99× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.378718 ± 0.00556474 (W 0.00298386) | 2.3824 ± 0.0269309 (W 0.0156598) | 🔵 tlinalg-pool 6.29× faster than `lapack-openblas` |  |
| `lu/n32/b1024` | 1.34402 ± 0.00911716 (W 0.007284) | 9.54719 ± 0.0877557 (W 0.0178615) | 🔵 tlinalg-pool 7.10× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.30596 ± 0.0150693 (W 0.00323127) | 0.323244 ± 0.0024349 (W 0.00227444) | 🔵 tlinalg-pool 1.06× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.134802 ± 0.000832268 (W 0.00157552) | 0.805808 ± 0.0123864 (W 0.00332517) | 🔵 tlinalg-pool 5.98× faster than `lapack-openblas` |  |
| `lu_factor/n16/b1024` | 0.253138 ± 0.00271177 (W 0.00230391) | 1.81208 ± 0.0196057 (W 0.00375656) | 🔵 tlinalg-pool 7.16× faster than `lapack-openblas` |  |
| `lu_factor/n32/b1024` | 0.728163 ± 0.00548621 (W 0.0038916) | 6.68616 ± 0.0622966 (W 0.0122029) | 🔵 tlinalg-pool 9.18× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.235906 ± 0.00343856 (W 0.00237391) | 0.218282 ± 0.00039731 (W 0.0017539) | 🔴 tlinalg-pool 1.08× slower than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.095724 ± 0.000790473 (W 0.00146437) | 0.568021 ± 0.00171527 (W 0.00340386) | 🔵 tlinalg-pool 5.93× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.322182 ± 0.0035143 (W 0.00226528) | 3.44301 ± 0.0155718 (W 0.0143953) | 🔵 tlinalg-pool 10.69× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 0.883377 ± 0.00402351 (W 0.00313532) | 9.70563 ± 0.0528652 (W 0.0141085) | 🔵 tlinalg-pool 10.99× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.056932 ± 0.000312234 (W 0.000889787) | 1.14556 ± 0.0273782 (W 0.00644519) | 🔵 tlinalg-pool 20.12× faster than `lapack-openblas` |  |
| `lu_factor_solve/n8/b1024` | 0.119087 ± 0.00147217 (W 0.0011653) | 1.51461 ± 0.0191967 (W 0.0243727) | 🔵 tlinalg-pool 12.72× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1024` | 0.0967655 ± 0.000634893 (W 0.00119696) | 1.16731 ± 0.0232353 (W 0.0213954) | 🔵 tlinalg-pool 12.06× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n32/b1024` | 0.231257 ± 0.00185917 (W 0.0025262) | 2.13969 ± 0.0111898 (W 0.00864756) | 🔵 tlinalg-pool 9.25× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n4/b1024` | 0.020799 ± 0.000412679 (W 0.000120644) | 0.863685 ± 0.0104609 (W 0.00766977) | 🔵 tlinalg-pool 41.53× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n8/b1024` | 0.0436565 ± 0.00037422 (W 0.000212915) | 0.791886 ± 0.0338814 (W 0.0266088) | 🔵 tlinalg-pool 18.14× faster than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n16/b1024` | 1.1455 ± 0.0120778 (W 0.00346222) | 7.88776 ± 0.0457973 (W 0.0183901) | 🔵 tlinalg-pool 6.89× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 4.24405 ± 0.0312234 (W 0.00720853) | 27.6089 ± 0.149946 (W 0.0310253) | 🔵 tlinalg-pool 6.51× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.10169 ± 0.0034508 (W 0.000463141) | 0.966481 ± 0.0110653 (W 0.00363798) | 🔵 tlinalg-pool 9.50× faster than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n8/b1024` | 0.31596 ± 0.0014777 (W 0.00186408) | 2.64362 ± 0.0098279 (W 0.00571947) | 🔵 tlinalg-pool 8.37× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.37069 ± 0.0269469 (W 0.00406587) | 9.46642 ± 0.0545899 (W 0.0397452) | 🔵 tlinalg-pool 6.91× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 4.37808 ± 0.0214128 (W 0.0205493) | 34.1061 ± 0.179205 (W 0.0680055) | 🔵 tlinalg-pool 7.79× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 0.176029 ± 0.00126602 (W 0.00171284) | 1.17645 ± 0.00723306 (W 0.00303146) | 🔵 tlinalg-pool 6.68× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.443988 ± 0.00908807 (W 0.00245319) | 3.04034 ± 0.0125155 (W 0.00929313) | 🔵 tlinalg-pool 6.85× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.36112 ± 0.00397385 (W 0.00275424) | 3.84673 ± 0.0633988 (W 0.0106512) | 🔵 tlinalg-pool 10.65× faster than `lapack-openblas` |  |
| `solve/n32/b1024` | 0.956388 ± 0.0158358 (W 0.00474281) | 9.86737 ± 0.0458723 (W 0.0136092) | 🔵 tlinalg-pool 10.32× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.053495 ± 0.00095947 (W 0.000381996) | 1.34446 ± 0.042994 (W 0.00527474) | 🔵 tlinalg-pool 25.13× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.126951 ± 0.00111959 (W 0.00121283) | 1.97649 ± 0.0240962 (W 0.00430178) | 🔵 tlinalg-pool 15.57× faster than `lapack-openblas` |  |
| `svd_full/n16/b1024` | 6.86574 ± 0.203534 (W 0.00577274) | 81.2154 ± 0.740273 (W 0.081829) | 🔵 tlinalg-pool 11.83× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 23.6293 ± 0.185813 (W 0.0206994) | 239.513 ± 1.19443 (W 0.42837) | 🔵 tlinalg-pool 10.14× faster than `lapack-openblas` |  |
| `svd_full/n4/b1024` | 0.574718 ± 0.032691 (W 0.00226631) | 6.39579 ± 0.100113 (W 0.012799) | 🔵 tlinalg-pool 11.13× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 1.91186 ± 0.0405172 (W 0.00165365) | 21.3165 ± 0.21028 (W 0.026294) | 🔵 tlinalg-pool 11.15× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 6.87327 ± 0.213082 (W 0.00587681) | 80.8895 ± 0.74564 (W 0.0860693) | 🔵 tlinalg-pool 11.77× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 23.6614 ± 0.136814 (W 0.0278183) | 239.349 ± 0.636488 (W 0.207811) | 🔵 tlinalg-pool 10.12× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1024` | 0.575444 ± 0.0196686 (W 0.00221472) | 6.43313 ± 0.0737174 (W 0.00906488) | 🔵 tlinalg-pool 11.18× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 1.87604 ± 0.0433958 (W 0.00299454) | 21.3416 ± 0.177102 (W 0.0228253) | 🔵 tlinalg-pool 11.38× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 2.81168 ± 0.0309683 (W 0.00438005) | 25.0764 ± 0.104787 (W 0.022889) | 🔵 tlinalg-pool 8.92× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 9.42195 ± 0.0232528 (W 0.0058235) | 79.7255 ± 0.415219 (W 0.259808) | 🔵 tlinalg-pool 8.46× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.365042 ± 0.000838665 (W 0.00225174) | 3.47329 ± 0.0133249 (W 0.0050386) | 🔵 tlinalg-pool 9.51× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.00597 ± 0.00299834 (W 0.0020489) | 8.94876 ± 0.0370544 (W 0.0131582) | 🔵 tlinalg-pool 8.90× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.067717 ± 0.000161824 (W 0.000231471) | 0.897073 ± 0.0143926 (W 0.00289873) | 🔵 tlinalg-pool 13.25× faster than `lapack-openblas` |  |
| `triangular_solve/n32/b1024` | 0.156678 ± 0.00095801 (W 0.00232962) | 1.47367 ± 0.0141495 (W 0.00530808) | 🔵 tlinalg-pool 9.41× faster than `lapack-openblas` |  |
| `triangular_solve/n4/b1024` | 0.0143115 ± 9.32041e-05 (W 0.0002423) | 0.716373 ± 0.0332544 (W 0.00687479) | 🔵 tlinalg-pool 50.06× faster than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.0306775 ± 0.000426646 (W 0.000113389) | 0.75159 ± 0.0040158 (W 0.00425316) | 🔵 tlinalg-pool 24.50× faster than `lapack-openblas` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.159257 ± 0.00103866 (W 0.00145458) | 1.544 ± 0.00549866 (W 0.0100414) | 🔵 tlinalg-pool 9.70× faster than `lapack-openblas` |  |
| `cholesky/n32/b1024` | 0.788136 ± 0.00355739 (W 0.00802258) | 6.31548 ± 0.110247 (W 0.0103851) | 🔵 tlinalg-pool 8.01× faster than `lapack-openblas` |  |
| `cholesky/n4/b1024` | 0.0275915 ± 0.000276575 (W 9.05184e-05) | 0.231838 ± 0.00176635 (W 0.00175238) | 🔵 tlinalg-pool 8.40× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.054752 ± 0.000614653 (W 0.000386386) | 0.486092 ± 0.00168639 (W 0.00253009) | 🔵 tlinalg-pool 8.88× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 16.4531 ± 0.0238473 (W 0.0139802) | 199.277 ± 0.413577 (W 0.326167) | 🔵 tlinalg-pool 12.11× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 67.8968 ± 0.266678 (W 0.0442335) | 887.128 ± 2.66053 (W 0.744715) | 🔵 tlinalg-pool 13.07× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 1.37833 ± 0.00625651 (W 0.00309467) | 13.254 ± 0.0560174 (W 0.0270338) | 🔵 tlinalg-pool 9.62× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 4.55381 ± 0.0210702 (W 0.0045855) | 46.7242 ± 0.513448 (W 0.042586) | 🔵 tlinalg-pool 10.26× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 4.02836 ± 0.0178157 (W 0.00924572) | 45.3489 ± 0.123892 (W 0.069982) | 🔵 tlinalg-pool 11.26× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 17.4876 ± 0.0460321 (W 0.0194357) | 188.369 ± 0.625392 (W 0.189625) | 🔵 tlinalg-pool 10.77× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 0.385589 ± 0.00189634 (W 0.0016078) | 3.60396 ± 0.0067923 (W 0.00612087) | 🔵 tlinalg-pool 9.35× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.17973 ± 0.00667414 (W 0.00229871) | 12.4114 ± 0.0463819 (W 0.0122804) | 🔵 tlinalg-pool 10.52× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 9.92603 ± 0.0591576 (W 0.00795602) | 149.391 ± 0.391381 (W 0.241759) | 🔵 tlinalg-pool 15.05× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 43.029 ± 0.184073 (W 0.0166894) | 601.064 ± 1.83733 (W 0.667594) | 🔵 tlinalg-pool 13.97× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.696284 ± 0.013261 (W 0.00324871) | 10.0491 ± 0.0311495 (W 0.012939) | 🔵 tlinalg-pool 14.43× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 2.61834 ± 0.010365 (W 0.00151636) | 37.0604 ± 0.151491 (W 0.047249) | 🔵 tlinalg-pool 14.15× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 3.04073 ± 0.0150375 (W 0.00329569) | 19.4154 ± 0.0330966 (W 0.0348549) | 🔵 tlinalg-pool 6.39× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 11.5661 ± 0.038041 (W 0.00742776) | 73.2501 ± 0.140848 (W 0.18621) | 🔵 tlinalg-pool 6.33× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.314271 ± 0.00389868 (W 0.00196613) | 2.12523 ± 0.0139032 (W 0.00506523) | 🔵 tlinalg-pool 6.76× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.949742 ± 0.00468983 (W 0.00193887) | 6.17475 ± 0.0229133 (W 0.0170308) | 🔵 tlinalg-pool 6.50× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.700959 ± 0.0114697 (W 0.00693635) | 33.3627 ± 0.253327 (W 0.0571457) | 🔵 tlinalg-pool 47.60× faster than `lapack-openblas` |  |
| `full_piv_lu/n32/b1024` | 3.04988 ± 0.00601346 (W 0.0153116) | 199.8 ± 0.932354 (W 0.506835) | 🔵 tlinalg-pool 65.51× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1024` | 0.089202 ± 0.0195535 (W 0.00223192) | 0.910949 ± 0.00738149 (W 0.00227128) | 🔵 tlinalg-pool 10.21× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `full_piv_lu/n8/b1024` | 0.216544 ± 0.00166869 (W 0.00280027) | 3.89587 ± 0.0247942 (W 0.00739432) | 🔵 tlinalg-pool 17.99× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n16/b1024` | 0.813813 ± 0.0065582 (W 0.00296521) | 37.8926 ± 0.123346 (W 0.0667898) | 🔵 tlinalg-pool 46.56× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 2.76164 ± 0.0177748 (W 0.0141706) | 211.169 ± 0.601992 (W 0.349811) | 🔵 tlinalg-pool 76.47× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.121357 ± 0.00209886 (W 0.00251767) | 2.18829 ± 0.0135075 (W 0.00406473) | 🔵 tlinalg-pool 18.03× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n8/b1024` | 0.289766 ± 0.00251552 (W 0.0025748) | 6.20082 ± 0.0618638 (W 0.011878) | 🔵 tlinalg-pool 21.40× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.625387 ± 0.0119581 (W 0.00444785) | 7.22676 ± 0.156721 (W 0.0178936) | 🔵 tlinalg-pool 11.56× faster than `lapack-openblas` |  |
| `householder_apply/n32/b1024` | 3.57525 ± 0.0156446 (W 0.0130742) | 35.9034 ± 0.295803 (W 0.0375794) | 🔵 tlinalg-pool 10.04× faster than `lapack-openblas` |  |
| `householder_apply/n4/b1024` | 0.0526185 ± 0.00215527 (W 0.000123449) | 0.429612 ± 0.00164544 (W 0.00260464) | 🔵 tlinalg-pool 8.16× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.154348 ± 0.00456334 (W 0.00129419) | 1.48348 ± 0.0071478 (W 0.00471445) | 🔵 tlinalg-pool 9.61× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.610665 ± 0.00810943 (W 0.00375274) | 7.35798 ± 0.0387324 (W 0.02374) | 🔵 tlinalg-pool 12.05× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 2.60039 ± 0.03213 (W 0.00891376) | 27.3285 ± 0.0814685 (W 0.0337291) | 🔵 tlinalg-pool 10.51× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.0787575 ± 0.000444746 (W 0.00174085) | 0.92657 ± 0.00270134 (W 0.00221623) | 🔵 tlinalg-pool 11.76× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.20084 ± 0.00161951 (W 0.00177071) | 2.36745 ± 0.0113182 (W 0.00426332) | 🔵 tlinalg-pool 11.79× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.451849 ± 0.00545225 (W 0.0067817) | 3.9615 ± 0.13928 (W 0.0128001) | 🔵 tlinalg-pool 8.77× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n32/b1024` | 2.18331 ± 0.012896 (W 0.0115653) | 15.4739 ± 0.10468 (W 0.0206575) | 🔵 tlinalg-pool 7.09× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.0634035 ± 0.00110509 (W 0.000958212) | 0.379243 ± 0.0047094 (W 0.00285604) | 🔵 tlinalg-pool 5.98× faster than `lapack-openblas` |  |
| `lu/n8/b1024` | 0.136054 ± 0.00171974 (W 0.0020534) | 1.03326 ± 0.0274728 (W 0.00244628) | 🔵 tlinalg-pool 7.59× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.286153 ± 0.00428108 (W 0.00148544) | 2.67642 ± 0.00781021 (W 0.00442222) | 🔵 tlinalg-pool 9.35× faster than `lapack-openblas` |  |
| `lu_factor/n32/b1024` | 1.24855 ± 0.00921724 (W 0.00691534) | 11.1836 ± 0.0506941 (W 0.0451721) | 🔵 tlinalg-pool 8.96× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.0608435 ± 0.000330306 (W 0.000571555) | 0.271467 ± 0.0021826 (W 0.00174316) | 🔵 tlinalg-pool 4.46× faster than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.104851 ± 0.00109129 (W 0.00175533) | 0.75632 ± 0.00144255 (W 0.002189) | 🔵 tlinalg-pool 7.21× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.455175 ± 0.000648186 (W 0.00337846) | 5.02967 ± 0.0587444 (W 0.00832606) | 🔵 tlinalg-pool 11.05× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 1.70367 ± 0.0118262 (W 0.00524951) | 15.3664 ± 0.062087 (W 0.0177884) | 🔵 tlinalg-pool 9.02× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.071248 ± 0.00079098 (W 0.00100132) | 1.11088 ± 0.009298 (W 0.00364057) | 🔵 tlinalg-pool 15.59× faster than `lapack-openblas` |  |
| `lu_factor_solve/n8/b1024` | 0.160705 ± 0.00287389 (W 0.00132202) | 2.29475 ± 0.0295728 (W 0.00616518) | 🔵 tlinalg-pool 14.28× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1024` | 0.184329 ± 0.00173415 (W 0.00186127) | 1.93875 ± 0.00841969 (W 0.00534189) | 🔵 tlinalg-pool 10.52× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n32/b1024` | 0.873241 ± 0.00549215 (W 0.00440819) | 4.02883 ± 0.020794 (W 0.0142927) | 🔵 tlinalg-pool 4.61× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n4/b1024` | 0.0337535 ± 0.000487231 (W 0.000434394) | 0.736144 ± 0.0257148 (W 0.00687378) | 🔵 tlinalg-pool 21.81× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.076092 ± 0.000454849 (W 0.000329986) | 1.33527 ± 0.0234547 (W 0.00522284) | 🔵 tlinalg-pool 17.55× faster than `lapack-openblas` |  |
| `qr/n16/b1024` | 1.39993 ± 0.0116288 (W 0.00456594) | 12.6687 ± 0.0559292 (W 0.0100561) | 🔵 tlinalg-pool 9.05× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 9.00105 ± 0.0460372 (W 0.0187552) | 49.6932 ± 0.311267 (W 0.0395781) | 🔵 tlinalg-pool 5.52× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.120816 ± 0.000822733 (W 0.000981448) | 1.41452 ± 0.00583912 (W 0.00630851) | 🔵 tlinalg-pool 11.71× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 0.343129 ± 0.00227337 (W 0.00213184) | 3.82147 ± 0.0181062 (W 0.00704435) | 🔵 tlinalg-pool 11.14× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.58682 ± 0.00824498 (W 0.00322515) | 16.8038 ± 0.0718976 (W 0.0340178) | 🔵 tlinalg-pool 10.59× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 8.48042 ± 0.0357949 (W 0.0145924) | 65.9249 ± 0.366738 (W 0.128677) | 🔵 tlinalg-pool 7.77× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 0.195781 ± 0.00133197 (W 0.00148975) | 1.83216 ± 0.0109604 (W 0.00528043) | 🔵 tlinalg-pool 9.36× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.493375 ± 0.00311423 (W 0.0027148) | 5.0154 ± 0.0240928 (W 0.00892492) | 🔵 tlinalg-pool 10.17× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.502684 ± 0.0106806 (W 0.00370911) | 5.23085 ± 0.0494202 (W 0.0148813) | 🔵 tlinalg-pool 10.41× faster than `lapack-openblas` |  |
| `solve/n32/b1024` | 1.857 ± 0.0148855 (W 0.00383936) | 16.2361 ± 0.0679426 (W 0.0261413) | 🔵 tlinalg-pool 8.74× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.0836465 ± 0.00106773 (W 0.00103217) | 1.46229 ± 0.0166907 (W 0.0076383) | 🔵 tlinalg-pool 17.48× faster than `lapack-openblas` |  |
| `solve/n8/b1024` | 0.188136 ± 0.0060726 (W 0.00186065) | 2.31756 ± 0.0154626 (W 0.0213636) | 🔵 tlinalg-pool 12.32× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 7.45161 ± 0.163487 (W 0.0104577) | 93.4606 ± 0.124076 (W 0.275314) | 🔵 tlinalg-pool 12.54× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 31.0982 ± 0.120904 (W 0.0385905) | 297.442 ± 0.602756 (W 0.445782) | 🔵 tlinalg-pool 9.56× faster than `lapack-openblas` |  |
| `svd_full/n4/b1024` | 0.674449 ± 0.0222475 (W 0.00242499) | 7.86595 ± 0.0409101 (W 0.0158447) | 🔵 tlinalg-pool 11.66× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n8/b1024` | 2.10848 ± 0.0710424 (W 0.00174323) | 24.8597 ± 0.0544166 (W 0.026577) | 🔵 tlinalg-pool 11.79× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.43395 ± 0.131604 (W 0.0138429) | 93.7738 ± 0.277578 (W 0.187002) | 🔵 tlinalg-pool 12.61× faster than `lapack-openblas` |  |
| `svd_thin/n32/b1024` | 31.0929 ± 0.130428 (W 0.0436691) | 296.409 ± 1.19662 (W 0.367159) | 🔵 tlinalg-pool 9.53× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1024` | 0.667902 ± 0.0282992 (W 0.00422807) | 7.91632 ± 0.048634 (W 0.0121122) | 🔵 tlinalg-pool 11.85× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 2.17544 ± 0.0678544 (W 0.00379189) | 24.9239 ± 0.036912 (W 0.0208885) | 🔵 tlinalg-pool 11.46× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 3.18532 ± 0.0136457 (W 0.00208356) | 33.4652 ± 0.0882183 (W 0.0277493) | 🔵 tlinalg-pool 10.51× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 11.3738 ± 0.0480991 (W 0.0084497) | 110.254 ± 0.646616 (W 0.2538) | 🔵 tlinalg-pool 9.69× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.444388 ± 0.00328041 (W 0.00211202) | 4.65059 ± 0.0296487 (W 0.0061206) | 🔵 tlinalg-pool 10.47× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.15058 ± 0.00658974 (W 0.00184838) | 11.2713 ± 0.0717445 (W 0.00983786) | 🔵 tlinalg-pool 9.80× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.12829 ± 0.00145889 (W 0.00147589) | 1.35913 ± 0.0191829 (W 0.00562788) | 🔵 tlinalg-pool 10.59× faster than `lapack-openblas` |  |
| `triangular_solve/n32/b1024` | 0.546847 ± 0.00572213 (W 0.00595351) | 3.03749 ± 0.0129041 (W 0.00485001) | 🔵 tlinalg-pool 5.55× faster than `lapack-openblas` |  |
| `triangular_solve/n4/b1024` | 0.0240245 ± 0.000309937 (W 0.000137831) | 0.790566 ± 0.0140814 (W 0.00239568) | 🔵 tlinalg-pool 32.91× faster than `lapack-openblas` |  |
| `triangular_solve/n8/b1024` | 0.0546765 ± 0.000359348 (W 0.000370225) | 0.908322 ± 0.0153052 (W 0.00641218) | 🔵 tlinalg-pool 16.61× faster than `lapack-openblas` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0705165 ± 0.000828188 (W 0.00180657) | 0.077074 ± 0.00108625 (W 0.00087669) | 🔵 tlinalg-pool 1.09× faster than `lapack-openblas` |  |
| `lu/n128/b1` | 0.173969 ± 0.00253684 (W 0.00172381) | 0.14509 ± 0.00143983 (W 0.00195492) | 🔴 tlinalg-pool 1.20× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.093354 ± 0.00100087 (W 0.000211139) | 0.130783 ± 0.000820345 (W 0.00185299) | 🔵 tlinalg-pool 1.40× faster than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.104976 ± 0.000849844 (W 0.000491159) | 0.147435 ± 0.000689228 (W 0.00170845) | 🔵 tlinalg-pool 1.40× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.011271 ± 9.25509e-05 (W 4.10396e-05) | 0.012338 ± 0.000132288 (W 0.000115601) | 🔵 tlinalg-pool 1.09× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.119714 ± 0.000754551 (W 0.00173954) | 0.153907 ± 0.000438551 (W 0.00219973) | 🔵 tlinalg-pool 1.29× faster than `lapack-openblas` |  |
| `svd_values/n128/b1` | 1.14043 ± 0.00341274 (W 0.00511815) | 1.38743 ± 0.00429392 (W 0.00280299) | 🔵 tlinalg-pool 1.22× faster than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.00795 ± 1.70783e-05 (W 5.12379e-05) | 0.006888 ± 0.000154381 (W 0.000107213) | 🔴 tlinalg-pool 1.15× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.157778 ± 0.00117117 (W 0.00124498) | 0.157559 ± 0.00120141 (W 0.00196674) | · |  |
| `lu/n128/b1` | 0.319571 ± 0.00241293 (W 0.00279699) | 0.234071 ± 0.00264405 (W 0.00208313) | 🔴 tlinalg-pool 1.37× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.225035 ± 0.000959822 (W 0.00174813) | 0.1898 ± 0.00217693 (W 0.00188755) | 🔴 tlinalg-pool 1.19× slower than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.25971 ± 0.00116272 (W 0.0018995) | 0.222325 ± 0.00197714 (W 0.00216142) | 🔴 tlinalg-pool 1.17× slower than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.0336775 ± 0.000110877 (W 0.000168908) | 0.0296805 ± 5.55158e-05 (W 0.000192801) | 🔴 tlinalg-pool 1.13× slower than `lapack-openblas` |  |
| `solve/n128/b1` | 0.283965 ± 0.00203427 (W 0.00151882) | 0.237223 ± 0.000527402 (W 0.00349621) | 🔴 tlinalg-pool 1.20× slower than `lapack-openblas` |  |
| `svd_values/n128/b1` | 1.43802 ± 0.00518201 (W 0.00321026) | 2.58498 ± 0.0105203 (W 0.00425194) | 🔵 tlinalg-pool 1.80× faster than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.020117 ± 6.62338e-05 (W 0.000168854) | 0.013505 ± 0.000135277 (W 0.000132378) | 🔴 tlinalg-pool 1.49× slower than `lapack-openblas` |  |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 27.3505 ± 0.0578615 (W 0.0230387) | 23.4501 ± 0.0644224 (W 0.0242599) | 🔴 tlinalg-pool 1.17× slower than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 16.214 ± 0.0334409 (W 0.0146255) | 11.2364 ± 0.0463387 (W 0.0178833) | 🔴 tlinalg-pool 1.44× slower than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 1.55536 ± 0.00381001 (W 0.00347993) | 9.81095 ± 0.0915604 (W 0.0213836) | 🔵 tlinalg-pool 6.31× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 1.84506 ± 0.00718713 (W 0.00492137) | 6.65989 ± 0.0366841 (W 0.0176109) | 🔵 tlinalg-pool 3.61× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 5.47599 ± 0.0131954 (W 0.0109176) | 13.4853 ± 0.0715864 (W 0.0185606) | 🔵 tlinalg-pool 2.46× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 7.25994 ± 0.0136999 (W 0.00994734) | 22.8718 ± 0.0101188 (W 0.0942788) | 🔵 tlinalg-pool 3.15× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 38.5701 ± 0.132366 (W 0.0307242) | 84.9901 ± 0.248708 (W 0.104427) | 🔵 tlinalg-pool 2.20× faster than `lapack-openblas` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 37.0138 ± 0.0767851 (W 0.0254273) | 203.375 ± 0.575511 (W 0.349192) | 🔵 tlinalg-pool 5.49× faster than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 20.4466 ± 0.0699934 (W 0.0195009) | 29.7391 ± 0.0927531 (W 0.0309846) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 5.67833 ± 0.00893137 (W 0.010198) | 14.6198 ± 0.277443 (W 0.0282451) | 🔵 tlinalg-pool 2.57× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 5.26653 ± 0.0232988 (W 0.00863078) | 10.7222 ± 0.024677 (W 0.0194345) | 🔵 tlinalg-pool 2.04× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 13.3313 ± 0.0558323 (W 0.0246606) | 21.7257 ± 0.0818613 (W 0.0292186) | 🔵 tlinalg-pool 1.63× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 14.3005 ± 0.0307523 (W 0.0290572) | 24.3503 ± 0.0630077 (W 0.0417404) | 🔵 tlinalg-pool 1.70× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 74.9962 ± 0.197543 (W 0.116033) | 97.8644 ± 0.970394 (W 0.295174) | 🔵 tlinalg-pool 1.30× faster than `lapack-openblas` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 6.02684 ± 0.0345719 (W 0.0244677) | 17.9783 ± 0.115682 (W 0.0430487) | 🔵 tlinalg-pool 2.98× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 21.8066 ± 0.022948 (W 0.0470504) | 35.8284 ± 0.197215 (W 0.0415782) | 🔵 tlinalg-pool 1.64× faster than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 21.4119 ± 0.0468023 (W 0.0632051) | 39.0542 ± 0.184177 (W 0.0347143) | 🔵 tlinalg-pool 1.82× faster than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 35.2304 ± 0.0406626 (W 0.0619395) | 60.8544 ± 0.29715 (W 0.0903935) | 🔵 tlinalg-pool 1.73× faster than `lapack-openblas` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 17.653 ± 0.0490225 (W 0.0514272) | 20.12 ± 0.0928749 (W 0.0274036) | 🔵 tlinalg-pool 1.14× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 58.4649 ± 0.151674 (W 0.0781798) | 40.1287 ± 0.111999 (W 0.0526735) | 🔴 tlinalg-pool 1.46× slower than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 59.6647 ± 0.21807 (W 0.182363) | 51.4944 ± 0.277735 (W 0.121319) | 🔴 tlinalg-pool 1.16× slower than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 108.818 ± 0.224917 (W 0.276155) | 85.2422 ± 0.472405 (W 0.0977869) | 🔴 tlinalg-pool 1.28× slower than `lapack-openblas` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
