# `tlinalg-scaling` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `3635d96231122648fe3f239027d9f29065331a4c`
- toolkit commit: `74e50e8199cb2c2f07e810744a0943fc3a8c1170`
- measured binary SHA-256: `028b45886580e5353ddee46798f3d2cd7cf52f7521251264812b3a908590da86`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-03T22:44:48.143693Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-scaling --aa 4 --reps 5 --prime-ms 250 --label weekly-20261103-scaling --no-publish`
- raw data: `data/results/zen5-cpu/tlinalg-scaling/20261103T222407Z-weekly-20261103-scaling/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: The scaling table declares 8T only. The pool has nothing to parallelise at 1T (it is one lane with extra machinery), and a 1T verify pass is the slowest single thing this host runs: measured 2026-10-20, one 1T population took over twenty minutes. The baseline the table needs is the one lane *on the same budget*.
  Known blind spot: The batched regime stops at n=32 by choice: batch 1024 is the regime this campaign is about, and the four shapes up to 32 already separate the rows by four to nine times, so larger matrices would add cells without changing the answer. Above that size faer-benchmark measures the same backends. (Recorded while the grid still held 64: one verify pass at n=64 ran past 45 minutes because the harness recomputes every case, which made the last shape cost far more than it added.)
  Known blind spot: Only the kernel entry points are measured. Tensor construction, dtype dispatch, session entry and pool checkout are tenferro's and are out of scope.
  Known blind spot: The 2026-10-17 trim narrowed the suite to the batched small regime plus three single-shape canaries (factor at 128, decompose at 512, rectangular at 4096x256, each at batch 1). The medium, large and tall grids are no longer measured here: faer-benchmark measures that geometry directly with the same backends these rows wrap, so a cost that appears only at those sizes has to be read from that campaign's page.
  Known blind spot: The small regime declares batch 1 and 1024 and gives up the middle of the axis, so a cost that appears only at an intermediate batch is not covered.
  Known blind spot: The thread axis is 1T and 8T; a budget between them (4T) is not measured, so a scaling curve cannot be read off this page.
  Known blind spot: The providers are compared at the thread budgets declared here; a budget the vendor threads itself by, outside that set, is not covered.
  Known blind spot: A vendor arm records the vendor library, but only OpenBLAS reports the kernel its runtime dispatched to. MKL's manifest records its own version and the threading layer the harness pins; it names no kernel, because MKL exposes none to name.
  Known blind spot: The batched regime measures batch 1024 only: batch 1 has nothing to parallelise, so it measures dispatch rather than the library, and the canaries carry the single-call sizes. An intermediate batch is therefore not covered.
- **Rows** — one row per engine in every table below:
  - `faer-1lane` — The faer-backed provider on one sequential lane: the per-item cost plus the batch loop, with no threading at all. The overhead baseline.
    Identity: tlinalg-rs (this repository's pinned revision)
    As measured: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.90%, worst 87.07% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 86 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.33%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
The `vs tlinalg-1lane` column is the rotation-averaged ratio
exp(mean over starts of log(engine median / tlinalg-1lane median)),
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

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.88465 ± 0.0566083 (W 0.00266475) | 0.111468 ± 0.00175384 (W 0.000179645) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 3.49103 ± 0.118078 (W 0.0175363) | 0.483397 ± 0.0508557 (W 0.00540044) | 🔴 tlinalg-1lane 7.22× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.17876 ± 0.000867205 (W 0.00160323) | 0.178463 ± 0.000838007 (W 0.00162723) | · |  |
| `cholesky/n8/b1024` | 0.360985 ± 0.00478429 (W 0.00247936) | 0.0471635 ± 0.000314612 (W 0.000118988) | 🔴 tlinalg-1lane 7.65× slower than `tlinalg-pool` |  |
| `eig/n16/b1024` | 95.717 ± 0.370021 (W 0.149788) | 12.0338 ± 0.0484168 (W 0.0257309) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 430.572 ± 1.67106 (W 2.35002) | 54.1466 ± 1.16714 (W 0.059753) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 6.38775 ± 0.0212214 (W 0.0145639) | 0.80967 ± 0.00205986 (W 0.00249502) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `eig/n8/b1024` | 24.0067 ± 0.143756 (W 0.035305) | 3.01763 ± 0.00854623 (W 0.00422719) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `eigh/n16/b1024` | 29.9697 ± 0.17172 (W 0.0246225) | 3.76099 ± 0.0159562 (W 0.00805063) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 111.625 ± 0.501173 (W 0.129458) | 13.9632 ± 0.0701429 (W 0.0167204) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.51053 ± 0.0217562 (W 0.00248767) | 0.320005 ± 0.000670896 (W 0.00174789) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 8.71742 ± 0.092156 (W 0.0109073) | 1.1106 ± 0.112788 (W 0.0045756) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigvals/n16/b1024` | 66.4219 ± 0.2281 (W 0.205974) | 8.33287 ± 0.0277186 (W 0.00772439) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 291.926 ± 0.724252 (W 0.465056) | 36.4912 ± 0.136309 (W 0.0673956) | 🔴 tlinalg-1lane 8.00× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 3.41371 ± 0.0271644 (W 0.0106454) | 0.436028 ± 0.0012785 (W 0.00262349) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 15.7343 ± 0.0921082 (W 0.0399071) | 1.97685 ± 0.00985118 (W 0.0033051) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 22.6781 ± 0.0479515 (W 0.0235871) | 2.84302 ± 0.0126315 (W 0.00219182) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 85.1209 ± 0.199069 (W 0.0914015) | 10.6254 ± 0.035873 (W 0.00676401) | 🔴 tlinalg-1lane 8.01× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.07825 ± 0.0091086 (W 0.00455253) | 0.262362 ± 0.00100316 (W 0.00206982) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 7.00757 ± 0.0528818 (W 0.00681469) | 0.882878 ± 0.00642031 (W 0.00203716) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 3.83682 ± 0.097951 (W 0.0335657) | 0.519053 ± 0.0148799 (W 0.00506573) | 🔴 tlinalg-1lane 7.39× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 15.1966 ± 0.341452 (W 0.0445548) | 2.02676 ± 0.0377976 (W 0.0138461) | 🔴 tlinalg-1lane 7.50× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.498495 ± 0.0128378 (W 0.00343719) | 0.500725 ± 0.0161564 (W 0.00448959) | · | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 1.29123 ± 0.0374814 (W 0.0160779) | 0.179596 ± 0.00213089 (W 0.0018665) | 🔴 tlinalg-1lane 7.19× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 4.04669 ± 0.0638453 (W 0.0196067) | 0.521821 ± 0.0128814 (W 0.00373354) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n32/b1024` | 12.9245 ± 0.359281 (W 0.0596026) | 1.63827 ± 0.0277013 (W 0.0135814) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n4/b1024` | 0.648245 ± 0.0018064 (W 0.00379572) | 0.0866875 ± 0.00138311 (W 0.000877031) | 🔴 tlinalg-1lane 7.48× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n8/b1024` | 1.57942 ± 0.00836355 (W 0.00944194) | 0.207149 ± 0.00202462 (W 0.00175076) | 🔴 tlinalg-1lane 7.62× slower than `tlinalg-pool` |  |
| `householder_apply/n16/b1024` | 4.78552 ± 0.287148 (W 0.0136028) | 0.605675 ± 0.0200635 (W 0.0052806) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 19.4921 ± 0.216363 (W 0.099947) | 2.39766 ± 0.0945851 (W 0.00465045) | 🔴 tlinalg-1lane 8.13× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.393359 ± 0.016221 (W 0.00183649) | 0.052854 ± 0.00095753 (W 0.000801973) | 🔴 tlinalg-1lane 7.44× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.30167 ± 0.05198 (W 0.00532423) | 0.161949 ± 0.00546829 (W 0.00160418) | 🔴 tlinalg-1lane 8.04× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 3.96952 ± 0.0486985 (W 0.00903327) | 0.509266 ± 0.00896191 (W 0.00221842) | 🔴 tlinalg-1lane 7.79× slower than `tlinalg-pool` |  |
| `householder_factor/n32/b1024` | 13.26 ± 0.165361 (W 0.0271485) | 1.67859 ± 0.0164368 (W 0.00687634) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.489227 ± 0.0106907 (W 0.00290509) | 0.064656 ± 0.00149563 (W 0.00131036) | 🔴 tlinalg-1lane 7.57× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.29398 ± 0.0220232 (W 0.00557163) | 0.168695 ± 0.00452256 (W 0.000602066) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n16/b1024` | 2.95724 ± 0.0477004 (W 0.0104453) | 0.389517 ± 0.00725359 (W 0.00290898) | 🔴 tlinalg-1lane 7.59× slower than `tlinalg-pool` |  |
| `lu/n32/b1024` | 10.3821 ± 0.0788801 (W 0.0380958) | 1.36078 ± 0.0279767 (W 0.00532492) | 🔴 tlinalg-1lane 7.63× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.308955 ± 0.00456038 (W 0.00367531) | 0.309466 ± 0.00698688 (W 0.00172463) | · | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.902377 ± 0.018143 (W 0.0080487) | 0.132963 ± 0.00299075 (W 0.00223702) | 🔴 tlinalg-1lane 6.79× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 1.9197 ± 0.0203214 (W 0.00584798) | 0.25317 ± 0.00357031 (W 0.00148305) | 🔴 tlinalg-1lane 7.58× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 5.69096 ± 0.164791 (W 0.0189524) | 0.721691 ± 0.0122539 (W 0.00309529) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n4/b1024` | 0.236996 ± 0.0014303 (W 0.00215623) | 0.236034 ± 0.00355201 (W 0.00156804) | · |  |
| `lu_factor/n8/b1024` | 0.62069 ± 0.00709843 (W 0.00585577) | 0.0961695 ± 0.00154479 (W 0.00103584) | 🔴 tlinalg-1lane 6.45× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 2.50309 ± 0.0525581 (W 0.00875481) | 0.323642 ± 0.0055852 (W 0.00232602) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 7.11254 ± 0.216831 (W 0.0156467) | 0.901541 ± 0.0210572 (W 0.00294467) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n4/b1024` | 0.299843 ± 0.00252659 (W 0.00354469) | 0.057027 ± 0.0004736 (W 0.00070522) | 🔴 tlinalg-1lane 5.26× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n8/b1024` | 0.834113 ± 0.0112749 (W 0.00440071) | 0.119423 ± 0.00145436 (W 0.00132589) | 🔴 tlinalg-1lane 6.98× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 0.629059 ± 0.119541 (W 0.0021863) | 0.0963255 ± 0.0038984 (W 0.00108666) | 🔴 tlinalg-1lane 6.53× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n32/b1024` | 2.37885 ± 0.314286 (W 0.0252016) | 0.232258 ± 0.0994728 (W 0.00335294) | 🔴 tlinalg-1lane 10.24× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n4/b1024` | 0.0729155 ± 0.000369998 (W 0.000107923) | 0.020824 ± 0.000203695 (W 0.000199051) | 🔴 tlinalg-1lane 3.50× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n8/b1024` | 0.237535 ± 0.0059082 (W 0.00246002) | 0.0435715 ± 0.000125786 (W 0.000116441) | 🔴 tlinalg-1lane 5.45× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `qr/n16/b1024` | 9.07561 ± 0.0346199 (W 0.0164004) | 1.14364 ± 0.00787325 (W 0.00176177) | 🔴 tlinalg-1lane 7.94× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 33.4414 ± 0.0295912 (W 0.113506) | 4.22845 ± 0.0238981 (W 0.00383234) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.768776 ± 0.00648334 (W 0.00662966) | 0.0996665 ± 0.00163946 (W 0.000243814) | 🔴 tlinalg-1lane 7.71× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.4117 ± 0.0558868 (W 0.00682631) | 0.308978 ± 0.00549711 (W 0.00195812) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `rank_revealing_qr/n16/b1024` | 10.7184 ± 0.160635 (W 0.0200181) | 1.34823 ± 0.00852466 (W 0.004043) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 34.5263 ± 0.218954 (W 0.0691855) | 4.39883 ± 0.0417569 (W 0.0216878) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.3318 ± 0.0178039 (W 0.00437184) | 0.173099 ± 0.00359536 (W 0.00138941) | 🔴 tlinalg-1lane 7.69× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n8/b1024` | 3.46468 ± 0.140286 (W 0.00544532) | 0.437857 ± 0.00373914 (W 0.00240692) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n16/b1024` | 2.80363 ± 0.0222207 (W 0.00898362) | 0.36271 ± 0.00632614 (W 0.00428108) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` |  |
| `solve/n32/b1024` | 7.66909 ± 0.108122 (W 0.0230421) | 0.963753 ± 0.0256877 (W 0.00650984) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n4/b1024` | 0.388786 ± 0.00780563 (W 0.00301638) | 0.052278 ± 0.000136717 (W 0.000761344) | 🔴 tlinalg-1lane 7.44× slower than `tlinalg-pool` |  |
| `solve/n8/b1024` | 0.969686 ± 0.0123276 (W 0.00539965) | 0.1252 ± 0.00249125 (W 0.0018633) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `svd_full/n16/b1024` | 52.9977 ± 0.0874822 (W 0.0535345) | 6.64992 ± 0.328441 (W 0.00953351) | 🔴 tlinalg-1lane 7.97× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 186.764 ± 1.82326 (W 0.343625) | 23.6251 ± 0.21953 (W 0.0173739) | 🔴 tlinalg-1lane 7.91× slower than `tlinalg-pool` |  |
| `svd_full/n4/b1024` | 4.38134 ± 0.0262554 (W 0.00838472) | 0.557851 ± 0.00421025 (W 0.00247646) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 14.8047 ± 0.0302343 (W 0.0167414) | 1.88467 ± 0.0390869 (W 0.00299953) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `svd_thin/n16/b1024` | 53.0437 ± 3.20129 (W 0.0531584) | 6.66158 ± 0.299125 (W 0.0121034) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 187.224 ± 1.966 (W 0.253035) | 23.6119 ± 0.147738 (W 0.0205668) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `svd_thin/n4/b1024` | 4.39223 ± 0.0409127 (W 0.00463737) | 0.558145 ± 0.00365868 (W 0.00219311) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `svd_thin/n8/b1024` | 14.7614 ± 0.117353 (W 0.0134151) | 1.90676 ± 0.0401332 (W 0.0042326) | 🔴 tlinalg-1lane 7.74× slower than `tlinalg-pool` |  |
| `svd_values/n16/b1024` | 21.7949 ± 0.10446 (W 0.0274549) | 2.77592 ± 0.00518117 (W 0.00351698) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 74.756 ± 0.467613 (W 0.0777665) | 9.43797 ± 0.0442137 (W 0.014189) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 2.81765 ± 0.0173108 (W 0.0042778) | 0.35867 ± 0.00247858 (W 0.00243805) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 7.81737 ± 0.0317972 (W 0.0121708) | 0.991375 ± 0.003641 (W 0.000906674) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 0.521937 ± 0.0407189 (W 0.00368941) | 0.068387 ± 0.00893183 (W 0.0011878) | 🔴 tlinalg-1lane 7.63× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 1.33255 ± 0.176507 (W 0.0154374) | 0.157448 ± 0.0380655 (W 0.00195534) | 🔴 tlinalg-1lane 8.46× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.091797 ± 0.000592003 (W 0.00112123) | 0.014342 ± 0.00047562 (W 0.000168785) | 🔴 tlinalg-1lane 6.40× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.226018 ± 0.00419089 (W 0.00250961) | 0.0308425 ± 0.000813822 (W 0.000181602) | 🔴 tlinalg-1lane 7.33× slower than `tlinalg-pool` | `!` between-start range over 5% |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 1.26149 ± 0.0708729 (W 0.00912045) | 0.16084 ± 0.0179716 (W 0.0028254) | 🔴 tlinalg-1lane 7.84× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 5.68453 ± 0.26761 (W 0.0115981) | 0.799983 ± 0.0692267 (W 0.0106366) | 🔴 tlinalg-1lane 7.11× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.195931 ± 0.00131128 (W 0.00182536) | 0.027722 ± 0.00267138 (W 0.000579071) | 🔴 tlinalg-1lane 7.07× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n8/b1024` | 0.425716 ± 0.0261078 (W 0.00287344) | 0.0547125 ± 0.001076 (W 0.000778822) | 🔴 tlinalg-1lane 7.78× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eig/n16/b1024` | 129.827 ± 0.267038 (W 0.112888) | 16.4545 ± 0.0506751 (W 0.0168074) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 540.409 ± 1.66587 (W 0.602983) | 67.7237 ± 0.208326 (W 0.0465899) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 10.7759 ± 0.0376388 (W 0.01007) | 1.37284 ± 0.00823252 (W 0.00221685) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `eig/n8/b1024` | 35.6813 ± 0.0207233 (W 0.03229) | 4.5449 ± 0.0142633 (W 0.010006) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` |  |
| `eigh/n16/b1024` | 32.0274 ± 0.138812 (W 0.036354) | 4.02393 ± 0.0290892 (W 0.00795742) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 138.113 ± 0.230759 (W 0.267437) | 17.4766 ± 0.0706572 (W 0.0134514) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.98031 ± 0.0144517 (W 0.00522605) | 0.383407 ± 0.00239925 (W 0.0025736) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 9.25465 ± 0.00789482 (W 0.0134924) | 1.17096 ± 0.00301357 (W 0.0033944) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `eigvals/n16/b1024` | 78.4865 ± 0.376238 (W 0.0412511) | 9.82586 ± 0.0272675 (W 0.0130812) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 341.896 ± 1.18093 (W 0.450497) | 42.9584 ± 0.264027 (W 0.0388192) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 5.50131 ± 0.0173878 (W 0.0119892) | 0.703695 ± 0.00826886 (W 0.00224426) | 🔴 tlinalg-1lane 7.82× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 20.5087 ± 0.126299 (W 0.0507459) | 2.60761 ± 0.0833344 (W 0.00401952) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigvalsh/n16/b1024` | 24.0768 ± 0.129977 (W 0.0176911) | 3.01845 ± 0.0107633 (W 0.00381017) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 91.8462 ± 0.343608 (W 0.0502328) | 11.4947 ± 0.0375589 (W 0.0127129) | 🔴 tlinalg-1lane 7.99× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 2.45753 ± 0.0161049 (W 0.00657595) | 0.317378 ± 0.00176022 (W 0.00164645) | 🔴 tlinalg-1lane 7.74× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 7.4639 ± 0.0475113 (W 0.0125876) | 0.94138 ± 0.00439543 (W 0.00187208) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 5.21554 ± 0.142806 (W 0.0322257) | 0.693784 ± 0.0261542 (W 0.0102604) | 🔴 tlinalg-1lane 7.52× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 21.3483 ± 0.606296 (W 0.0535914) | 3.07951 ± 0.0252856 (W 0.01016) | 🔴 tlinalg-1lane 6.93× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu/n4/b1024` | 0.58858 ± 0.010627 (W 0.00366483) | 0.0883995 ± 0.0011913 (W 0.00197656) | 🔴 tlinalg-1lane 6.66× slower than `tlinalg-pool` |  |
| `full_piv_lu/n8/b1024` | 1.51356 ± 0.0712674 (W 0.013547) | 0.215668 ± 0.00665372 (W 0.00273256) | 🔴 tlinalg-1lane 7.02× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 6.28453 ± 0.0761289 (W 0.016394) | 0.8135 ± 0.00948765 (W 0.00186921) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 21.0542 ± 0.339415 (W 0.0264718) | 2.76748 ± 0.0172334 (W 0.00801769) | 🔴 tlinalg-1lane 7.61× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.900243 ± 0.00610256 (W 0.00252282) | 0.120736 ± 0.00356798 (W 0.00154578) | 🔴 tlinalg-1lane 7.46× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 2.26227 ± 0.0405069 (W 0.0082366) | 0.293334 ± 0.00131271 (W 0.00230519) | 🔴 tlinalg-1lane 7.71× slower than `tlinalg-pool` |  |
| `householder_apply/n16/b1024` | 5.46948 ± 0.273255 (W 0.0193545) | 0.633725 ± 0.0676369 (W 0.00336349) | 🔴 tlinalg-1lane 8.63× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 27.8996 ± 0.79765 (W 0.0393183) | 3.57601 ± 0.0834796 (W 0.0170556) | 🔴 tlinalg-1lane 7.80× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.389895 ± 0.00962465 (W 0.00303979) | 0.051351 ± 0.000632301 (W 0.000179906) | 🔴 tlinalg-1lane 7.59× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 1.21129 ± 0.0986389 (W 0.00223401) | 0.153571 ± 0.00338287 (W 0.00202946) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 4.84642 ± 0.064509 (W 0.00769061) | 0.611142 ± 0.00679808 (W 0.00482791) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `householder_factor/n32/b1024` | 20.5571 ± 0.237293 (W 0.0328201) | 2.57542 ± 0.0126459 (W 0.015659) | 🔴 tlinalg-1lane 7.98× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.606898 ± 0.00617296 (W 0.00359926) | 0.078477 ± 0.000233595 (W 0.00155142) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.58465 ± 0.0210233 (W 0.00309599) | 0.202298 ± 0.00230487 (W 0.00153703) | 🔴 tlinalg-1lane 7.83× slower than `tlinalg-pool` |  |
| `lu/n16/b1024` | 3.26498 ± 0.0837597 (W 0.027781) | 0.454889 ± 0.0302964 (W 0.00827423) | 🔴 tlinalg-1lane 7.18× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n32/b1024` | 15.0776 ± 0.248293 (W 0.0434395) | 2.20025 ± 0.0143817 (W 0.0107147) | 🔴 tlinalg-1lane 6.85× slower than `tlinalg-pool` |  |
| `lu/n4/b1024` | 0.369017 ± 0.00357468 (W 0.0031447) | 0.0641705 ± 0.00102015 (W 0.000650278) | 🔴 tlinalg-1lane 5.75× slower than `tlinalg-pool` |  |
| `lu/n8/b1024` | 0.988083 ± 0.0193999 (W 0.00859125) | 0.140852 ± 0.000552681 (W 0.00319797) | 🔴 tlinalg-1lane 7.02× slower than `tlinalg-pool` |  |
| `lu_factor/n16/b1024` | 2.2056 ± 0.0503852 (W 0.012131) | 0.287671 ± 0.00485844 (W 0.00262534) | 🔴 tlinalg-1lane 7.67× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 9.7569 ± 0.355395 (W 0.032026) | 1.23489 ± 0.0218828 (W 0.0064317) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n4/b1024` | 0.292298 ± 0.0031053 (W 0.00177597) | 0.0607535 ± 0.000302314 (W 0.00109683) | 🔴 tlinalg-1lane 4.81× slower than `tlinalg-pool` |  |
| `lu_factor/n8/b1024` | 0.713118 ± 0.0205921 (W 0.00491334) | 0.105182 ± 0.00104035 (W 0.00161258) | 🔴 tlinalg-1lane 6.78× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n16/b1024` | 3.53182 ± 0.13495 (W 0.0135248) | 0.45429 ± 0.00519129 (W 0.00382665) | 🔴 tlinalg-1lane 7.77× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n32/b1024` | 13.3788 ± 0.602087 (W 0.0203007) | 1.6978 ± 0.0888445 (W 0.0184155) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n4/b1024` | 0.45451 ± 0.00789226 (W 0.00326086) | 0.0726055 ± 0.000896137 (W 0.000983309) | 🔴 tlinalg-1lane 6.26× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n8/b1024` | 1.20048 ± 0.029395 (W 0.00382693) | 0.159494 ± 0.00186448 (W 0.0020683) | 🔴 tlinalg-1lane 7.53× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1024` | 1.34985 ± 0.223388 (W 0.00592039) | 0.185613 ± 0.0196765 (W 0.00844659) | 🔴 tlinalg-1lane 7.27× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n32/b1024` | 6.87778 ± 0.321766 (W 0.021482) | 0.926157 ± 0.0782491 (W 0.00489295) | 🔴 tlinalg-1lane 7.43× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.174867 ± 0.00179342 (W 0.00147191) | 0.033593 ± 0.000143644 (W 0.000424203) | 🔴 tlinalg-1lane 5.21× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n8/b1024` | 0.491286 ± 0.0284195 (W 0.00308213) | 0.0759975 ± 0.00262789 (W 0.00155739) | 🔴 tlinalg-1lane 6.46× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `qr/n16/b1024` | 11.1134 ± 0.0540028 (W 0.0124972) | 1.40214 ± 0.0228753 (W 0.00376704) | 🔴 tlinalg-1lane 7.93× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 71.222 ± 0.290802 (W 0.071388) | 9.02858 ± 0.0966988 (W 0.00613132) | 🔴 tlinalg-1lane 7.89× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.927941 ± 0.00457891 (W 0.00251674) | 0.119994 ± 0.00082726 (W 0.00149598) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.72034 ± 0.0175909 (W 0.00717372) | 0.346092 ± 0.00112849 (W 0.00226224) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 12.4604 ± 0.0832317 (W 0.0115473) | 1.58263 ± 0.0243393 (W 0.00404141) | 🔴 tlinalg-1lane 7.87× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 66.363 ± 0.611438 (W 0.223864) | 8.49721 ± 0.0631448 (W 0.00725801) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.50962 ± 0.0144276 (W 0.00370093) | 0.195515 ± 0.0006412 (W 0.00160866) | 🔴 tlinalg-1lane 7.72× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n8/b1024` | 3.86802 ± 0.0431415 (W 0.00609972) | 0.491081 ± 0.00147058 (W 0.00203907) | 🔴 tlinalg-1lane 7.88× slower than `tlinalg-pool` |  |
| `solve/n16/b1024` | 3.81186 ± 0.0733134 (W 0.00951876) | 0.492178 ± 0.0118893 (W 0.00266016) | 🔴 tlinalg-1lane 7.74× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n32/b1024` | 14.3505 ± 0.137133 (W 0.0290146) | 1.83813 ± 0.0128582 (W 0.00356306) | 🔴 tlinalg-1lane 7.81× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.551365 ± 0.0133086 (W 0.00310604) | 0.0746245 ± 0.000353396 (W 0.000968041) | 🔴 tlinalg-1lane 7.39× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n8/b1024` | 1.37142 ± 0.0126273 (W 0.0051102) | 0.178489 ± 0.00205933 (W 0.00213224) | 🔴 tlinalg-1lane 7.68× slower than `tlinalg-pool` |  |
| `svd_full/n16/b1024` | 57.4098 ± 0.32781 (W 0.0499841) | 7.50212 ± 0.0571157 (W 0.0136086) | 🔴 tlinalg-1lane 7.65× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 244.705 ± 0.880658 (W 0.422756) | 31.6367 ± 0.832115 (W 0.0120298) | 🔴 tlinalg-1lane 7.73× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 5.14032 ± 0.0303224 (W 0.00748419) | 0.663369 ± 0.0121563 (W 0.00252285) | 🔴 tlinalg-1lane 7.75× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 16.4117 ± 0.115725 (W 0.00904638) | 2.08898 ± 0.00812376 (W 0.00198606) | 🔴 tlinalg-1lane 7.86× slower than `tlinalg-pool` |  |
| `svd_thin/n16/b1024` | 57.5202 ± 0.184518 (W 0.0488362) | 7.48311 ± 0.112062 (W 0.0158769) | 🔴 tlinalg-1lane 7.69× slower than `tlinalg-pool` |  |
| `svd_thin/n32/b1024` | 244.152 ± 0.504263 (W 0.339036) | 31.6687 ± 0.873331 (W 0.0157711) | 🔴 tlinalg-1lane 7.71× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 5.15163 ± 0.0163296 (W 0.00353) | 0.665655 ± 0.00891001 (W 0.00175598) | 🔴 tlinalg-1lane 7.74× slower than `tlinalg-pool` |  |
| `svd_thin/n8/b1024` | 16.4234 ± 1.12342 (W 0.0197047) | 2.09105 ± 0.0304762 (W 0.00240122) | 🔴 tlinalg-1lane 7.85× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 25.6172 ± 0.112863 (W 0.0524984) | 3.22332 ± 0.0470729 (W 0.00850747) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 90.1353 ± 0.393066 (W 0.0920233) | 11.4122 ± 0.116687 (W 0.00700461) | 🔴 tlinalg-1lane 7.90× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 3.43915 ± 0.0230263 (W 0.00581096) | 0.43449 ± 0.0030055 (W 0.002678) | 🔴 tlinalg-1lane 7.92× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 9.026 ± 0.0805513 (W 0.00952538) | 1.13561 ± 0.00506355 (W 0.00162926) | 🔴 tlinalg-1lane 7.95× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 1.03078 ± 0.108482 (W 0.00389568) | 0.129507 ± 0.0195467 (W 0.00205548) | 🔴 tlinalg-1lane 7.96× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 4.34394 ± 0.214067 (W 0.0280204) | 0.530479 ± 0.0551895 (W 0.00398471) | 🔴 tlinalg-1lane 8.19× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.185191 ± 0.00395065 (W 0.00210475) | 0.025663 ± 0.000115866 (W 6.40742e-05) | 🔴 tlinalg-1lane 7.22× slower than `tlinalg-pool` |  |
| `triangular_solve/n8/b1024` | 0.44146 ± 0.0212929 (W 0.00399006) | 0.057147 ± 0.00381062 (W 0.000765838) | 🔴 tlinalg-1lane 7.72× slower than `tlinalg-pool` | `!` between-start range over 5% |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.066294 ± 0.000298608 (W 0.000833797) | 0.0672405 ± 0.00229653 (W 0.000342014) | · | `!` between-start range over 5% |
| `lu/n128/b1` | 0.167068 ± 0.000925096 (W 0.00185099) | 0.172442 ± 0.00106996 (W 0.00178494) | · |  |
| `lu_factor/n128/b1` | 0.0946575 ± 0.000850839 (W 0.00189345) | 0.091497 ± 0.000723755 (W 0.00036381) | · |  |
| `lu_factor_solve/n128/b1` | 0.103218 ± 0.00108259 (W 0.00158012) | 0.101745 ± 0.000895387 (W 0.000366514) | · |  |
| `lu_solve_prepared/n128/b1` | 0.010024 ± 8.99537e-05 (W 7.39125e-05) | 0.011191 ± 4.78714e-05 (W 2.98253e-05) | 🔵 tlinalg-1lane 1.12× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.112356 ± 0.000670789 (W 0.000242517) | 0.117425 ± 0.00112628 (W 0.00174238) | · |  |
| `svd_values/n128/b1` | 1.04733 ± 0.00272048 (W 0.00245324) | 1.14339 ± 0.0066074 (W 0.00324891) | 🔵 tlinalg-1lane 1.09× faster than `tlinalg-pool` |  |
| `triangular_solve/n128/b1` | 0.006958 ± 0.000122577 (W 4.97722e-05) | 0.007975 ± 5.88784e-05 (W 6.80969e-05) | 🔵 tlinalg-1lane 1.15× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.175463 ± 0.000478708 (W 0.00166309) | 0.154805 ± 0.00178097 (W 0.00212825) | 🔴 tlinalg-1lane 1.13× slower than `tlinalg-pool` |  |
| `lu/n128/b1` | 0.355105 ± 0.00304279 (W 0.00414829) | 0.318187 ± 0.00860022 (W 0.00316403) | 🔴 tlinalg-1lane 1.12× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n128/b1` | 0.273172 ± 0.00140294 (W 0.00174318) | 0.225298 ± 0.00162506 (W 0.00168849) | 🔴 tlinalg-1lane 1.21× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n128/b1` | 0.304836 ± 0.00147172 (W 0.00237114) | 0.258688 ± 0.00093853 (W 0.00143975) | 🔴 tlinalg-1lane 1.18× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n128/b1` | 0.0317545 ± 0.000153862 (W 8.04272e-05) | 0.0337985 ± 0.000226201 (W 0.000219791) | 🔵 tlinalg-1lane 1.06× faster than `tlinalg-pool` |  |
| `solve/n128/b1` | 0.312897 ± 0.00137584 (W 0.00219996) | 0.280452 ± 0.00126404 (W 0.00181539) | 🔴 tlinalg-1lane 1.12× slower than `tlinalg-pool` |  |
| `svd_values/n128/b1` | 1.76521 ± 0.00371088 (W 0.00408586) | 1.44771 ± 0.00857799 (W 0.00376158) | 🔴 tlinalg-1lane 1.22× slower than `tlinalg-pool` |  |
| `triangular_solve/n128/b1` | 0.0187 ± 6.89807e-05 (W 6.68367e-05) | 0.020243 ± 0.000134505 (W 0.000158019) | 🔵 tlinalg-1lane 1.08× faster than `tlinalg-pool` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 56.924 ± 0.164989 (W 0.0407975) | 27.4295 ± 0.0705211 (W 0.0257385) | 🔴 tlinalg-1lane 2.08× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 23.6158 ± 0.263708 (W 0.0164147) | 16.2269 ± 0.0460912 (W 0.0140955) | 🔴 tlinalg-1lane 1.46× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 10.2841 ± 0.0393371 (W 0.0219348) | 1.57784 ± 0.00814536 (W 0.00698922) | 🔴 tlinalg-1lane 6.52× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 7.11951 ± 0.0245544 (W 0.0095042) | 1.83499 ± 0.0127443 (W 0.00338202) | 🔴 tlinalg-1lane 3.88× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 18.9455 ± 0.0739034 (W 0.03252) | 5.46056 ± 0.0245237 (W 0.0220716) | 🔴 tlinalg-1lane 3.47× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 29.8178 ± 0.121517 (W 0.0315005) | 7.23472 ± 0.0317677 (W 0.0172208) | 🔴 tlinalg-1lane 4.12× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 106.289 ± 0.211555 (W 0.233825) | 38.7508 ± 0.0676348 (W 0.0433025) | 🔴 tlinalg-1lane 2.74× slower than `tlinalg-pool` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 113.697 ± 0.308949 (W 0.137026) | 37.0668 ± 0.0161499 (W 0.0300342) | 🔴 tlinalg-1lane 3.07× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 49.1348 ± 0.217324 (W 0.0806447) | 20.4841 ± 0.0283741 (W 0.0213238) | 🔴 tlinalg-1lane 2.40× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 40.4774 ± 0.0925207 (W 0.0370551) | 5.60316 ± 0.0157798 (W 0.0120699) | 🔴 tlinalg-1lane 7.22× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 27.1448 ± 0.0611739 (W 0.0343386) | 5.14356 ± 0.00847903 (W 0.00898925) | 🔴 tlinalg-1lane 5.28× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 69.9511 ± 0.169813 (W 0.0817765) | 13.2735 ± 0.0519256 (W 0.01836) | 🔴 tlinalg-1lane 5.27× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 79.3535 ± 0.255647 (W 0.0506603) | 14.2164 ± 0.0349143 (W 0.0247661) | 🔴 tlinalg-1lane 5.58× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 256.008 ± 0.559184 (W 0.685299) | 75.2083 ± 0.0635503 (W 0.186939) | 🔴 tlinalg-1lane 3.40× slower than `tlinalg-pool` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 22.9078 ± 0.0605471 (W 0.0460758) | 5.91198 ± 0.0294845 (W 0.0332268) | 🔴 tlinalg-1lane 3.87× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 65.4011 ± 0.0800429 (W 0.0625596) | 22.364 ± 0.056912 (W 0.033467) | 🔴 tlinalg-1lane 2.92× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 101.172 ± 0.680023 (W 0.22236) | 21.569 ± 0.0608053 (W 0.0458209) | 🔴 tlinalg-1lane 4.69× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 100.055 ± 0.101131 (W 0.194463) | 35.2717 ± 0.0980119 (W 0.069851) | 🔴 tlinalg-1lane 2.84× slower than `tlinalg-pool` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 85.5851 ± 0.614687 (W 0.256239) | 17.347 ± 0.00882101 (W 0.0153846) | 🔴 tlinalg-1lane 4.93× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 234.586 ± 0.337839 (W 0.427728) | 58.5703 ± 0.130893 (W 0.0824063) | 🔴 tlinalg-1lane 4.01× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 351.714 ± 3.12301 (W 1.43515) | 59.3438 ± 0.265434 (W 0.182239) | 🔴 tlinalg-1lane 5.93× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 363.557 ± 0.549629 (W 0.559509) | 109.101 ± 0.142107 (W 0.308356) | 🔴 tlinalg-1lane 3.33× slower than `tlinalg-pool` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
