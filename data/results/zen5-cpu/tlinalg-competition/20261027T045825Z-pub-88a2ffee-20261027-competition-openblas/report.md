# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `88a2ffeea4c5ef514dac91b2ea65d43c52b121e9`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.25.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `6c795e30d74f6a15af990fb38902ac28af9b3299`
- toolkit commit: `467573e6e3e405b8ec30b3b61d096c1d0c9893c3`
- measured binary SHA-256: `64481af2f151a58e4c90c1572083238ad05b2faa0e627db883da7f71a93af272`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-27T05:19:24.564062Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor openblas --aa 4 --reps 5 --prime-ms 250 --label pub-88a2ffee-20261027-competition-openblas`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261027T045825Z-pub-88a2ffee-20261027-competition-openblas/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.59%, worst 60.43% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 53 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.34%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.115831 ± 0.000822909 (W 0.00177606) | 1.02348 ± 0.0229 (W 0.00168164) | 🔵 tlinalg-pool 8.84× faster than `lapack-openblas` |  |
| `cholesky/n32/b1024` | 0.436202 ± 0.00688286 (W 0.00660227) | 3.61067 ± 0.0579113 (W 0.00819164) | 🔵 tlinalg-pool 8.28× faster than `lapack-openblas` |  |
| `cholesky/n4/b1024` | 0.182434 ± 0.00103055 (W 0.00131396) | 0.196366 ± 0.000277045 (W 0.00128066) | 🔵 tlinalg-pool 1.08× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.360556 ± 0.00325099 (W 0.00178496) | 0.391438 ± 0.0069268 (W 0.00280302) | 🔵 tlinalg-pool 1.09× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 11.8888 ± 0.0427365 (W 0.0354367) | 68.7331 ± 0.281975 (W 0.0728445) | 🔵 tlinalg-pool 5.78× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 53.4036 ± 0.0844592 (W 0.329476) | 324.78 ± 1.8485 (W 0.679122) | 🔵 tlinalg-pool 6.08× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 6.19849 ± 0.0132486 (W 0.0126934) | 5.32 ± 0.0169792 (W 0.00719111) | 🔴 tlinalg-pool 1.17× slower than `lapack-openblas` |  |
| `eig/n8/b1024` | 2.99139 ± 0.0228095 (W 0.0075552) | 17.5878 ± 0.0260527 (W 0.0181406) | 🔵 tlinalg-pool 5.88× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 3.80156 ± 0.109535 (W 0.0182831) | 40.1353 ± 0.291824 (W 0.0949408) | 🔵 tlinalg-pool 10.56× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigh/n32/b1024` | 13.9991 ± 0.112837 (W 0.111004) | 119.549 ± 0.490114 (W 0.204832) | 🔵 tlinalg-pool 8.54× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 2.5466 ± 0.0123608 (W 0.00288794) | 3.02976 ± 0.00810649 (W 0.0033896) | 🔵 tlinalg-pool 1.19× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.11944 ± 0.0334521 (W 0.0274408) | 10.856 ± 0.0668914 (W 0.0100859) | 🔵 tlinalg-pool 9.70× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigvals/n16/b1024` | 8.20468 ± 0.0498275 (W 0.0283853) | 49.663 ± 0.258883 (W 0.046725) | 🔵 tlinalg-pool 6.05× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 36.4059 ± 0.0672407 (W 0.0880231) | 218.11 ± 1.8602 (W 0.457356) | 🔵 tlinalg-pool 5.99× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 3.19327 ± 0.0163456 (W 0.0126401) | 3.41338 ± 0.00561554 (W 0.00511686) | 🔵 tlinalg-pool 1.07× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 1.95964 ± 0.0559743 (W 0.01734) | 13.2765 ± 0.0542738 (W 0.00917883) | 🔵 tlinalg-pool 6.77× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigvalsh/n16/b1024` | 2.81534 ± 0.0143008 (W 0.00574729) | 14.5344 ± 0.0565757 (W 0.00699669) | 🔵 tlinalg-pool 5.16× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 10.9239 ± 0.0374498 (W 0.026731) | 50.1168 ± 0.332884 (W 0.211124) | 🔵 tlinalg-pool 4.59× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 2.04936 ± 0.00234144 (W 0.00281848) | 1.39635 ± 0.0129779 (W 0.0024437) | 🔴 tlinalg-pool 1.47× slower than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.873355 ± 0.00405706 (W 0.00217548) | 4.55874 ± 0.0119514 (W 0.00324856) | 🔵 tlinalg-pool 5.22× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.513731 ± 0.00459812 (W 0.00711304) | 4.74228 ± 0.118499 (W 0.0227884) | 🔵 tlinalg-pool 9.23× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 2.17045 ± 0.0352224 (W 0.0126136) | 28.9437 ± 1.1893 (W 0.110655) | 🔵 tlinalg-pool 13.34× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n4/b1024` | 0.407417 ± 0.00305197 (W 0.00190131) | 0.367258 ± 0.00156688 (W 0.00194645) | 🔴 tlinalg-pool 1.11× slower than `lapack-openblas` |  |
| `full_piv_lu/n8/b1024` | 1.14999 ± 0.0072062 (W 0.00418327) | 1.04027 ± 0.0125749 (W 0.00260861) | 🔴 tlinalg-pool 1.11× slower than `lapack-openblas` |  |
| `full_piv_lu_solve/n16/b1024` | 0.466818 ± 0.00346781 (W 0.0023712) | 6.49679 ± 0.100431 (W 0.0194758) | 🔵 tlinalg-pool 13.92× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 1.55165 ± 0.0192153 (W 0.0169212) | 31.7534 ± 0.524983 (W 0.267357) | 🔵 tlinalg-pool 20.46× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.531243 ± 0.00271847 (W 0.00341891) | 0.948203 ± 0.00417228 (W 0.00219706) | 🔵 tlinalg-pool 1.78× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n8/b1024` | 0.172431 ± 0.00393633 (W 0.0014649) | 2.01761 ± 0.0138558 (W 0.00737823) | 🔵 tlinalg-pool 11.70× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.633489 ± 0.0108165 (W 0.0116424) | 4.46261 ± 0.0677051 (W 0.0096787) | 🔵 tlinalg-pool 7.04× faster than `lapack-openblas` |  |
| `householder_apply/n32/b1024` | 2.55651 ± 0.0361869 (W 0.030708) | 19.0966 ± 0.375509 (W 0.0500507) | 🔵 tlinalg-pool 7.47× faster than `lapack-openblas` |  |
| `householder_apply/n4/b1024` | 0.385317 ± 0.00541028 (W 0.00163251) | 0.418769 ± 0.00330711 (W 0.00191399) | 🔵 tlinalg-pool 1.09× faster than `lapack-openblas` |  |
| `householder_apply/n8/b1024` | 0.178131 ± 0.00361483 (W 0.00271061) | 1.20379 ± 0.0133207 (W 0.00417576) | 🔵 tlinalg-pool 6.76× faster than `lapack-openblas` |  |
| `householder_factor/n16/b1024` | 0.50562 ± 0.0103861 (W 0.00196655) | 4.32263 ± 0.00667262 (W 0.00688515) | 🔵 tlinalg-pool 8.55× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 1.69067 ± 0.045729 (W 0.013099) | 14.6004 ± 0.0403202 (W 0.0200138) | 🔵 tlinalg-pool 8.64× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n4/b1024` | 0.4676 ± 0.00309011 (W 0.00229123) | 0.535977 ± 0.00294267 (W 0.00231764) | 🔵 tlinalg-pool 1.15× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.174174 ± 0.00271979 (W 0.00154645) | 1.49543 ± 0.00400896 (W 0.00211746) | 🔵 tlinalg-pool 8.59× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.36277 ± 0.00653679 (W 0.00491152) | 2.39565 ± 0.0329747 (W 0.0039499) | 🔵 tlinalg-pool 6.60× faster than `lapack-openblas` |  |
| `lu/n32/b1024` | 1.27034 ± 0.0107635 (W 0.00891927) | 9.73588 ± 0.0568326 (W 0.0246988) | 🔵 tlinalg-pool 7.66× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.308009 ± 0.00658006 (W 0.00247144) | 0.329839 ± 0.00533192 (W 0.00185811) | 🔵 tlinalg-pool 1.07× faster than `lapack-openblas` |  |
| `lu/n8/b1024` | 0.848789 ± 0.0114558 (W 0.00462561) | 0.813463 ± 0.0121557 (W 0.00195453) | · |  |
| `lu_factor/n16/b1024` | 0.267067 ± 0.00261926 (W 0.00246784) | 1.80995 ± 0.0141442 (W 0.00413412) | 🔵 tlinalg-pool 6.78× faster than `lapack-openblas` |  |
| `lu_factor/n32/b1024` | 0.739486 ± 0.0111277 (W 0.00992806) | 6.80178 ± 0.0892271 (W 0.00875737) | 🔵 tlinalg-pool 9.20× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.256257 ± 0.0019459 (W 0.00163778) | 0.218451 ± 0.000824783 (W 0.00101106) | 🔴 tlinalg-pool 1.17× slower than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.624927 ± 0.0141651 (W 0.00475539) | 0.572445 ± 0.00148068 (W 0.00336155) | 🔴 tlinalg-pool 1.09× slower than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.340734 ± 0.0244192 (W 0.00275711) | 3.73993 ± 0.0293265 (W 0.00714342) | 🔵 tlinalg-pool 10.98× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n32/b1024` | 0.898277 ± 0.0109225 (W 0.00539666) | 9.85064 ± 0.0570497 (W 0.0214597) | 🔵 tlinalg-pool 10.97× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.318176 ± 0.00600234 (W 0.00167628) | 1.31778 ± 0.0256123 (W 0.00344876) | 🔵 tlinalg-pool 4.14× faster than `lapack-openblas` |  |
| `lu_factor_solve/n8/b1024` | 0.131269 ± 0.000870778 (W 0.00203876) | 1.95336 ± 0.0198828 (W 0.00353414) | 🔵 tlinalg-pool 14.88× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1024` | 0.108091 ± 0.00130538 (W 0.00305807) | 1.56374 ± 0.0377564 (W 0.00420955) | 🔵 tlinalg-pool 14.47× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n32/b1024` | 0.323277 ± 0.00957474 (W 0.0161677) | 2.31328 ± 0.0101608 (W 0.00656351) | 🔵 tlinalg-pool 7.16× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.0712075 ± 0.000213253 (W 0.000805738) | 0.985288 ± 0.0387587 (W 0.00342259) | 🔵 tlinalg-pool 13.84× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.233329 ± 0.000579608 (W 0.00203614) | 1.25781 ± 0.0216744 (W 0.00590235) | 🔵 tlinalg-pool 5.39× faster than `lapack-openblas` |  |
| `qr/n16/b1024` | 1.1341 ± 0.0111089 (W 0.00585662) | 7.79074 ± 0.0773897 (W 0.0100286) | 🔵 tlinalg-pool 6.87× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 4.57626 ± 0.0209588 (W 0.0151796) | 27.1742 ± 0.237606 (W 0.0355756) | 🔵 tlinalg-pool 5.94× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.764017 ± 0.00703963 (W 0.00136798) | 0.957666 ± 0.00472188 (W 0.00180489) | 🔵 tlinalg-pool 1.25× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 2.36233 ± 0.0350214 (W 0.00291797) | 2.61491 ± 0.00292615 (W 0.00284527) | 🔵 tlinalg-pool 1.11× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.34745 ± 0.0169477 (W 0.00347547) | 9.41738 ± 0.0708146 (W 0.0372737) | 🔵 tlinalg-pool 6.99× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 4.61331 ± 0.0484498 (W 0.0353822) | 33.6207 ± 0.0462524 (W 0.102835) | 🔵 tlinalg-pool 7.29× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 1.2613 ± 0.0247767 (W 0.00620184) | 1.14852 ± 0.00462593 (W 0.00287006) | 🔴 tlinalg-pool 1.10× slower than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 3.40138 ± 0.038629 (W 0.00568472) | 3.02578 ± 0.0222472 (W 0.0089922) | 🔴 tlinalg-pool 1.12× slower than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.359449 ± 0.00547876 (W 0.00227685) | 3.7492 ± 0.0140708 (W 0.00836091) | 🔵 tlinalg-pool 10.43× faster than `lapack-openblas` |  |
| `solve/n32/b1024` | 0.980148 ± 0.0125778 (W 0.0238265) | 9.9059 ± 0.0509006 (W 0.0504676) | 🔵 tlinalg-pool 10.11× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.386254 ± 0.00380939 (W 0.00301288) | 1.26375 ± 0.0607452 (W 0.00940769) | 🔵 tlinalg-pool 3.27× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.135386 ± 0.00260973 (W 0.00256063) | 2.04149 ± 0.0259247 (W 0.00706886) | 🔵 tlinalg-pool 15.08× faster than `lapack-openblas` |  |
| `svd_full/n16/b1024` | 7.23096 ± 0.0697134 (W 0.112671) | 80.4687 ± 0.642304 (W 0.24861) | 🔵 tlinalg-pool 11.13× faster than `lapack-openblas` |  |
| `svd_full/n32/b1024` | 26.237 ± 1.1376 (W 0.205987) | 238.787 ± 0.413731 (W 0.098751) | 🔵 tlinalg-pool 9.10× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 4.34651 ± 0.0260325 (W 0.00830655) | 6.30693 ± 0.0100899 (W 0.00319679) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 1.97388 ± 0.0620062 (W 0.0211791) | 21.2462 ± 0.0169103 (W 0.0158883) | 🔵 tlinalg-pool 10.76× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.42111 ± 0.231423 (W 0.0985893) | 80.9252 ± 0.555225 (W 0.24138) | 🔵 tlinalg-pool 10.90× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 26.0906 ± 0.279536 (W 0.0593399) | 238.864 ± 1.42338 (W 0.393455) | 🔵 tlinalg-pool 9.16× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1024` | 4.36278 ± 0.023722 (W 0.00513781) | 6.31736 ± 0.0272301 (W 0.00741009) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1024` | 1.9534 ± 0.0387594 (W 0.0125211) | 21.2034 ± 0.203035 (W 0.0222155) | 🔵 tlinalg-pool 10.85× faster than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 5.12872 ± 0.0101151 (W 0.0116694) | 25.0499 ± 0.280895 (W 0.0202599) | 🔵 tlinalg-pool 4.88× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 20.0955 ± 0.0430097 (W 0.20246) | 79.4625 ± 0.290644 (W 0.0866422) | 🔵 tlinalg-pool 3.95× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 3.18416 ± 0.0182354 (W 0.00574599) | 3.46262 ± 0.0174327 (W 0.00480187) | 🔵 tlinalg-pool 1.09× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.44403 ± 0.0102175 (W 0.00269347) | 8.92303 ± 0.0313565 (W 0.012487) | 🔵 tlinalg-pool 6.18× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.0785715 ± 0.0040262 (W 0.00193069) | 1.04135 ± 0.108276 (W 0.00867309) | 🔵 tlinalg-pool 13.25× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n32/b1024` | 0.207862 ± 0.015201 (W 0.00753265) | 1.55002 ± 0.0421587 (W 0.0182887) | 🔵 tlinalg-pool 7.46× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.09137 ± 0.000248556 (W 0.000688929) | 0.766261 ± 0.0151998 (W 0.00487141) | 🔵 tlinalg-pool 8.39× faster than `lapack-openblas` |  |
| `triangular_solve/n8/b1024` | 0.220525 ± 0.00148701 (W 0.00163755) | 0.913679 ± 0.0411722 (W 0.00422571) | 🔵 tlinalg-pool 4.14× faster than `lapack-openblas` | `!` between-start range over 5% |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.168247 ± 0.00127109 (W 0.00193349) | 1.5449 ± 0.0261815 (W 0.00827893) | 🔵 tlinalg-pool 9.18× faster than `lapack-openblas` |  |
| `cholesky/n32/b1024` | 0.815357 ± 0.0076747 (W 0.00906212) | 6.28275 ± 0.0288274 (W 0.00921707) | 🔵 tlinalg-pool 7.71× faster than `lapack-openblas` |  |
| `cholesky/n4/b1024` | 0.20155 ± 0.00361586 (W 0.00112187) | 0.229928 ± 0.00201718 (W 0.00139305) | 🔵 tlinalg-pool 1.14× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.420908 ± 0.000463632 (W 0.00274279) | 0.488183 ± 0.00297212 (W 0.00208827) | 🔵 tlinalg-pool 1.16× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 16.353 ± 0.297862 (W 0.0532519) | 198.83 ± 0.279421 (W 0.433126) | 🔵 tlinalg-pool 12.16× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 67.2542 ± 0.0447112 (W 0.0811742) | 885.643 ± 23.407 (W 0.792737) | 🔵 tlinalg-pool 13.17× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eig/n4/b1024` | 10.2527 ± 0.0176541 (W 0.0123505) | 13.4065 ± 0.025134 (W 0.0159456) | 🔵 tlinalg-pool 1.31× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 4.43329 ± 0.0173455 (W 0.00953156) | 46.6787 ± 0.143099 (W 0.223821) | 🔵 tlinalg-pool 10.53× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 4.14293 ± 0.0837391 (W 0.0282233) | 45.1621 ± 0.21983 (W 0.0356135) | 🔵 tlinalg-pool 10.90× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 17.4172 ± 0.603188 (W 0.176511) | 187.987 ± 0.624269 (W 0.118652) | 🔵 tlinalg-pool 10.79× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigh/n4/b1024` | 2.92837 ± 0.00827253 (W 0.00772235) | 3.63664 ± 0.00847265 (W 0.00381445) | 🔵 tlinalg-pool 1.24× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.23775 ± 0.0462286 (W 0.0208823) | 12.4034 ± 0.103411 (W 0.0103568) | 🔵 tlinalg-pool 10.02× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigvals/n16/b1024` | 9.71274 ± 0.0205403 (W 0.0542253) | 148.679 ± 0.216166 (W 0.444748) | 🔵 tlinalg-pool 15.31× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 42.4618 ± 0.0286741 (W 0.0462638) | 597.723 ± 0.493331 (W 0.891888) | 🔵 tlinalg-pool 14.08× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 5.02102 ± 0.0192011 (W 0.0105101) | 10.034 ± 0.0288924 (W 0.00461887) | 🔵 tlinalg-pool 2.00× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 2.53493 ± 0.00206675 (W 0.00871485) | 36.948 ± 0.135348 (W 0.0216792) | 🔵 tlinalg-pool 14.58× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 3.01833 ± 0.00680026 (W 0.00987925) | 19.3767 ± 0.0597495 (W 0.022882) | 🔵 tlinalg-pool 6.42× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 11.7765 ± 0.0225242 (W 0.0252773) | 73.2416 ± 0.306103 (W 0.13452) | 🔵 tlinalg-pool 6.22× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 2.4269 ± 0.0115083 (W 0.00589869) | 2.13264 ± 0.00847243 (W 0.00363091) | 🔴 tlinalg-pool 1.14× slower than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.933999 ± 0.0039741 (W 0.00341139) | 6.16366 ± 0.0311285 (W 0.00581578) | 🔵 tlinalg-pool 6.60× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.654875 ± 0.00537657 (W 0.00962371) | 33.2708 ± 0.14039 (W 0.0534897) | 🔵 tlinalg-pool 50.80× faster than `lapack-openblas` |  |
| `full_piv_lu/n32/b1024` | 3.07942 ± 0.0300656 (W 0.0132808) | 199.78 ± 2.37727 (W 0.353201) | 🔵 tlinalg-pool 64.88× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1024` | 0.462395 ± 0.00615094 (W 0.00454162) | 0.901808 ± 0.00452438 (W 0.00199569) | 🔵 tlinalg-pool 1.95× faster than `lapack-openblas` |  |
| `full_piv_lu/n8/b1024` | 0.195121 ± 0.00354099 (W 0.00331943) | 3.87555 ± 0.0312997 (W 0.00469206) | 🔵 tlinalg-pool 19.86× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n16/b1024` | 0.711339 ± 0.0124379 (W 0.0147774) | 37.7339 ± 0.165327 (W 0.0340171) | 🔵 tlinalg-pool 53.05× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 2.65967 ± 0.0140767 (W 0.00961588) | 211.664 ± 1.6357 (W 0.256585) | 🔵 tlinalg-pool 79.58× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.762271 ± 0.00269772 (W 0.00310748) | 2.12774 ± 0.0190713 (W 0.00353211) | 🔵 tlinalg-pool 2.79× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n8/b1024` | 0.280707 ± 0.00526909 (W 0.00392276) | 6.13932 ± 0.0586772 (W 0.00752616) | 🔵 tlinalg-pool 21.87× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.642292 ± 0.0156504 (W 0.00913629) | 7.19737 ± 0.153977 (W 0.0182638) | 🔵 tlinalg-pool 11.21× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 3.56412 ± 0.078881 (W 0.0332999) | 35.393 ± 0.669378 (W 0.0399594) | 🔵 tlinalg-pool 9.93× faster than `lapack-openblas` |  |
| `householder_apply/n4/b1024` | 0.36286 ± 0.00432104 (W 0.0019142) | 0.438631 ± 0.000450266 (W 0.00193288) | 🔵 tlinalg-pool 1.21× faster than `lapack-openblas` |  |
| `householder_apply/n8/b1024` | 0.156626 ± 0.00401426 (W 0.00146448) | 1.48481 ± 0.0136839 (W 0.00325063) | 🔵 tlinalg-pool 9.48× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.599471 ± 0.0181174 (W 0.00672999) | 7.32993 ± 0.0258324 (W 0.0089297) | 🔵 tlinalg-pool 12.23× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n32/b1024` | 2.59585 ± 0.0204463 (W 0.0175617) | 27.2451 ± 0.128436 (W 0.0197896) | 🔵 tlinalg-pool 10.50× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.573148 ± 0.00363015 (W 0.00233865) | 0.925486 ± 0.00339089 (W 0.00169663) | 🔵 tlinalg-pool 1.61× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.200919 ± 0.000265695 (W 0.00294178) | 2.36849 ± 0.00380375 (W 0.00335941) | 🔵 tlinalg-pool 11.79× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.44584 ± 0.00198473 (W 0.0100505) | 3.82384 ± 0.128884 (W 0.0153596) | 🔵 tlinalg-pool 8.58× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n32/b1024` | 2.09234 ± 0.0125589 (W 0.0119431) | 15.4322 ± 0.20034 (W 0.0189064) | 🔵 tlinalg-pool 7.38× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.378584 ± 0.00882074 (W 0.00249016) | 0.376842 ± 0.0496584 (W 0.00250672) | · | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.154432 ± 0.00221751 (W 0.00396397) | 1.02056 ± 0.0920491 (W 0.00183171) | 🔵 tlinalg-pool 6.61× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.350152 ± 0.094582 (W 0.0204632) | 2.69263 ± 0.00924127 (W 0.00514524) | 🔵 tlinalg-pool 7.69× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor/n32/b1024` | 1.29691 ± 0.038324 (W 0.0443762) | 11.2921 ± 0.134472 (W 0.0157959) | 🔵 tlinalg-pool 8.71× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n4/b1024` | 0.30354 ± 0.00715188 (W 0.00258671) | 0.271375 ± 0.00171203 (W 0.00166938) | 🔴 tlinalg-pool 1.12× slower than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.114237 ± 0.00177571 (W 0.00193684) | 0.754328 ± 0.00851392 (W 0.00282038) | 🔵 tlinalg-pool 6.60× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.464474 ± 0.00543965 (W 0.00424362) | 5.07023 ± 0.108764 (W 0.0101428) | 🔵 tlinalg-pool 10.92× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 1.79378 ± 0.0435937 (W 0.0169653) | 15.4837 ± 0.254168 (W 0.0161713) | 🔵 tlinalg-pool 8.63× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n4/b1024` | 0.457967 ± 0.0100565 (W 0.0029922) | 1.10948 ± 0.163213 (W 0.00229131) | 🔵 tlinalg-pool 2.42× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor_solve/n8/b1024` | 0.174134 ± 0.01387 (W 0.00657279) | 2.38791 ± 0.0304927 (W 0.00418359) | 🔵 tlinalg-pool 13.71× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n16/b1024` | 0.197132 ± 0.0462067 (W 0.00376695) | 1.93 ± 0.157526 (W 0.00585239) | 🔵 tlinalg-pool 9.79× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n32/b1024` | 0.89241 ± 0.033715 (W 0.0135466) | 3.94291 ± 0.163753 (W 0.0126407) | 🔵 tlinalg-pool 4.42× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.165468 ± 0.000333067 (W 0.00169133) | 0.775949 ± 0.14247 (W 0.00940855) | 🔵 tlinalg-pool 4.69× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n8/b1024` | 0.0884495 ± 0.00181075 (W 0.00412834) | 1.39704 ± 0.0239078 (W 0.00450177) | 🔵 tlinalg-pool 15.79× faster than `lapack-openblas` |  |
| `qr/n16/b1024` | 1.43366 ± 0.0130763 (W 0.0102023) | 12.5423 ± 0.0216253 (W 0.0250228) | 🔵 tlinalg-pool 8.75× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 9.37455 ± 0.078953 (W 0.0264915) | 49.5074 ± 0.149891 (W 0.209576) | 🔵 tlinalg-pool 5.28× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.91871 ± 0.00560864 (W 0.00204609) | 1.42946 ± 0.0157339 (W 0.00372875) | 🔵 tlinalg-pool 1.56× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 0.351664 ± 0.00342454 (W 0.00284694) | 3.77246 ± 0.0161733 (W 0.00258636) | 🔵 tlinalg-pool 10.73× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.57377 ± 0.0129001 (W 0.00974695) | 16.7227 ± 0.101798 (W 0.0297145) | 🔵 tlinalg-pool 10.63× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 8.58819 ± 0.060905 (W 0.0349042) | 65.6058 ± 0.347961 (W 0.355948) | 🔵 tlinalg-pool 7.64× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 1.53686 ± 0.01878 (W 0.00321282) | 1.80352 ± 0.012944 (W 0.00599221) | 🔵 tlinalg-pool 1.17× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.496209 ± 0.00777758 (W 0.00638893) | 5.04359 ± 0.0206025 (W 0.00391782) | 🔵 tlinalg-pool 10.16× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.513385 ± 0.0116489 (W 0.00864559) | 5.16157 ± 0.183578 (W 0.0187679) | 🔵 tlinalg-pool 10.05× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n32/b1024` | 1.86693 ± 0.017851 (W 0.0163157) | 16.2394 ± 0.0409975 (W 0.0157513) | 🔵 tlinalg-pool 8.70× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.574003 ± 0.00467282 (W 0.00328337) | 1.51455 ± 0.046113 (W 0.00256951) | 🔵 tlinalg-pool 2.64× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.192383 ± 0.00168387 (W 0.00185518) | 2.20817 ± 0.159966 (W 0.00909961) | 🔵 tlinalg-pool 11.48× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_full/n16/b1024` | 7.77616 ± 0.0771587 (W 0.03979) | 93.4677 ± 0.284051 (W 0.261942) | 🔵 tlinalg-pool 12.02× faster than `lapack-openblas` |  |
| `svd_full/n32/b1024` | 33.721 ± 1.02104 (W 0.0904805) | 294.879 ± 1.03672 (W 0.451659) | 🔵 tlinalg-pool 8.74× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 5.24338 ± 0.0141527 (W 0.00432623) | 7.82344 ± 0.049825 (W 0.0225109) | 🔵 tlinalg-pool 1.49× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 2.20454 ± 0.0358642 (W 0.0594616) | 24.8906 ± 0.0308784 (W 0.0176416) | 🔵 tlinalg-pool 11.29× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 7.78827 ± 0.109083 (W 0.0492392) | 93.5542 ± 0.302686 (W 0.0485448) | 🔵 tlinalg-pool 12.01× faster than `lapack-openblas` |  |
| `svd_thin/n32/b1024` | 33.4038 ± 0.220881 (W 0.0746673) | 295.416 ± 0.603145 (W 0.567471) | 🔵 tlinalg-pool 8.84× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1024` | 5.22826 ± 0.0122426 (W 0.00319908) | 7.82854 ± 0.0414143 (W 0.00776528) | 🔵 tlinalg-pool 1.50× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1024` | 2.18035 ± 0.08133 (W 0.0596297) | 24.8259 ± 0.0480017 (W 0.0190909) | 🔵 tlinalg-pool 11.39× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 5.943 ± 0.102397 (W 0.0234551) | 33.3801 ± 0.104509 (W 0.0138868) | 🔵 tlinalg-pool 5.62× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 22.6985 ± 0.107268 (W 0.0561621) | 109.875 ± 0.388918 (W 0.276549) | 🔵 tlinalg-pool 4.84× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 4.01723 ± 0.0233529 (W 0.00336322) | 4.56732 ± 0.0496255 (W 0.00361919) | 🔵 tlinalg-pool 1.14× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.67349 ± 0.00401093 (W 0.00908118) | 11.1841 ± 0.0334278 (W 0.0155873) | 🔵 tlinalg-pool 6.68× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.137882 ± 0.00259031 (W 0.00213711) | 1.25651 ± 0.0587948 (W 0.00533689) | 🔵 tlinalg-pool 9.11× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 0.636164 ± 0.0202597 (W 0.0110732) | 2.9501 ± 0.0585679 (W 0.0102641) | 🔵 tlinalg-pool 4.64× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.164791 ± 0.0017035 (W 0.00196342) | 0.746134 ± 0.0586288 (W 0.00381375) | 🔵 tlinalg-pool 4.53× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n8/b1024` | 0.0671645 ± 0.00435348 (W 0.000638852) | 1.02235 ± 0.0430839 (W 0.00438948) | 🔵 tlinalg-pool 15.22× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.064355 ± 0.00133556 (W 0.00158861) | 0.078426 ± 0.00133018 (W 0.000764699) | 🔵 tlinalg-pool 1.22× faster than `lapack-openblas` |  |
| `lu/n128/b1` | 0.175997 ± 0.00474629 (W 0.00402909) | 0.145873 ± 0.000607088 (W 0.00160282) | 🔴 tlinalg-pool 1.21× slower than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n128/b1` | 0.118411 ± 0.00372906 (W 0.00525971) | 0.130478 ± 9.71494e-05 (W 0.00107223) | 🔵 tlinalg-pool 1.10× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n128/b1` | 0.124997 ± 0.00160512 (W 0.00294206) | 0.147056 ± 0.000290747 (W 0.000813873) | 🔵 tlinalg-pool 1.18× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.0102895 ± 0.000135377 (W 8.28236e-05) | 0.012278 ± 5.058e-05 (W 0.000116698) | 🔵 tlinalg-pool 1.19× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.138524 ± 0.0015091 (W 0.00196264) | 0.154244 ± 0.000925326 (W 0.00102653) | 🔵 tlinalg-pool 1.11× faster than `lapack-openblas` |  |
| `svd_values/n128/b1` | 2.37734 ± 0.00253974 (W 0.00387491) | 1.37925 ± 0.00208043 (W 0.00260626) | 🔴 tlinalg-pool 1.72× slower than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.0070835 ± 2.97811e-05 (W 4.04742e-05) | 0.006812 ± 8.53913e-05 (W 0.000138746) | · | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.185707 ± 0.00121489 (W 0.0038702) | 0.149728 ± 0.00119777 (W 0.00164674) | 🔴 tlinalg-pool 1.24× slower than `lapack-openblas` |  |
| `lu/n128/b1` | 0.340106 ± 0.000655558 (W 0.00520187) | 0.234576 ± 0.00217091 (W 0.00158875) | 🔴 tlinalg-pool 1.45× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.265015 ± 0.00144075 (W 0.00260541) | 0.191962 ± 0.00107912 (W 0.00196132) | 🔴 tlinalg-pool 1.38× slower than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.300068 ± 0.00322166 (W 0.00415643) | 0.22598 ± 0.000869681 (W 0.00181596) | 🔴 tlinalg-pool 1.33× slower than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.031774 ± 0.000112132 (W 8.05419e-05) | 0.029896 ± 0.000547334 (W 0.000157844) | 🔴 tlinalg-pool 1.06× slower than `lapack-openblas` |  |
| `solve/n128/b1` | 0.318307 ± 0.00122954 (W 0.00348759) | 0.234399 ± 0.00105116 (W 0.00139477) | 🔴 tlinalg-pool 1.36× slower than `lapack-openblas` |  |
| `svd_values/n128/b1` | 3.24942 ± 0.00994004 (W 0.00921002) | 2.57648 ± 0.00754251 (W 0.00352385) | 🔴 tlinalg-pool 1.26× slower than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.0186745 ± 5.58592e-05 (W 7.49325e-05) | 0.013335 ± 0.000418809 (W 7.57525e-05) | 🔴 tlinalg-pool 1.40× slower than `lapack-openblas` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 29.0606 ± 0.0476514 (W 0.0309587) | 23.4437 ± 0.0966878 (W 0.0201093) | 🔴 tlinalg-pool 1.24× slower than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 17.6059 ± 0.0238696 (W 0.030695) | 11.0839 ± 0.036557 (W 0.00404075) | 🔴 tlinalg-pool 1.59× slower than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 1.77507 ± 0.00929193 (W 0.0081583) | 9.85781 ± 0.0591743 (W 0.0133266) | 🔵 tlinalg-pool 5.55× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 2.06826 ± 0.012508 (W 0.0145947) | 6.78018 ± 0.0410363 (W 0.0147275) | 🔵 tlinalg-pool 3.28× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 6.14632 ± 0.026018 (W 0.0114485) | 13.5395 ± 0.0764982 (W 0.0244065) | 🔵 tlinalg-pool 2.20× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 8.60556 ± 0.0557393 (W 0.0390378) | 23.2618 ± 0.0763545 (W 0.0829385) | 🔵 tlinalg-pool 2.70× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 60.069 ± 0.368649 (W 0.0909446) | 84.6495 ± 0.549728 (W 0.123854) | 🔵 tlinalg-pool 1.41× faster than `lapack-openblas` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 39.9188 ± 0.36905 (W 0.363537) | 205.463 ± 1.14552 (W 0.405502) | 🔵 tlinalg-pool 5.15× faster than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 23.6418 ± 0.0569227 (W 0.0479428) | 29.8076 ± 0.0570086 (W 0.0173851) | 🔵 tlinalg-pool 1.26× faster than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 5.84963 ± 0.0221755 (W 0.0164069) | 14.4934 ± 0.173237 (W 0.0181259) | 🔵 tlinalg-pool 2.48× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 5.54873 ± 0.0227664 (W 0.00830392) | 10.7518 ± 0.0219535 (W 0.0140543) | 🔵 tlinalg-pool 1.94× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 14.983 ± 0.0233723 (W 0.0207769) | 21.7938 ± 0.109075 (W 0.0248756) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 16.8923 ± 0.0317839 (W 0.0170109) | 24.4289 ± 0.0977114 (W 0.0479901) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 95.7224 ± 0.430571 (W 0.263016) | 97.7779 ± 0.712128 (W 0.0826973) | · |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 6.93783 ± 0.0214457 (W 0.0158027) | 17.9967 ± 0.104293 (W 0.0232321) | 🔵 tlinalg-pool 2.59× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 23.593 ± 0.0920066 (W 0.0622897) | 35.5275 ± 0.413347 (W 0.03468) | 🔵 tlinalg-pool 1.51× faster than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 24.5624 ± 0.0657247 (W 0.0362153) | 38.8237 ± 0.218431 (W 0.0505704) | 🔵 tlinalg-pool 1.58× faster than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 40.9522 ± 0.134037 (W 0.128143) | 60.6598 ± 0.618124 (W 0.0548918) | 🔵 tlinalg-pool 1.48× faster than `lapack-openblas` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 18.8769 ± 0.0770746 (W 0.0237199) | 20.1445 ± 0.0222079 (W 0.0229127) | 🔵 tlinalg-pool 1.07× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 55.3953 ± 0.741779 (W 0.804664) | 40.1408 ± 0.135086 (W 0.0468689) | 🔴 tlinalg-pool 1.38× slower than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 61.7249 ± 0.708337 (W 0.928784) | 51.3527 ± 0.116022 (W 0.113671) | 🔴 tlinalg-pool 1.20× slower than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 111.587 ± 0.660808 (W 1.17114) | 85.4027 ± 0.201127 (W 0.0476096) | 🔴 tlinalg-pool 1.31× slower than `lapack-openblas` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
