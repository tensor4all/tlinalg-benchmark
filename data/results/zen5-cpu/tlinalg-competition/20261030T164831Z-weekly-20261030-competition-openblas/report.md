# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `53d1f0d9f44378596c4f2bce932e45cc961b0d78`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.27.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.2 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `3957b5af620eff5da5d1435afd97a4a8619ba473`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `028b45886580e5353ddee46798f3d2cd7cf52f7521251264812b3a908590da86`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-30T17:09:11.542440Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor openblas --aa 4 --reps 5 --prime-ms 250 --label weekly-20261030-competition-openblas --no-publish`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261030T164831Z-weekly-20261030-competition-openblas/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.27%, worst 29.22% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 34 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.33%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `cholesky/n16/b1024` | 0.114614 ± 0.00295082 (W 0.00203929) | 1.01023 ± 0.00822897 (W 0.00174222) | 🔵 tlinalg-pool 8.81× faster than `lapack-openblas` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 0.461771 ± 0.0112516 (W 0.00618914) | 3.59798 ± 0.0174252 (W 0.00603374) | 🔵 tlinalg-pool 7.79× faster than `lapack-openblas` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.180502 ± 0.00788506 (W 0.00157186) | 0.197279 ± 0.000608097 (W 0.00186754) | 🔵 tlinalg-pool 1.09× faster than `lapack-openblas` | `!` between-start range over 5% |
| `cholesky/n8/b1024` | 0.0470375 ± 0.000415121 (W 0.00013997) | 0.391191 ± 0.00590274 (W 0.00262434) | 🔵 tlinalg-pool 8.32× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 12.0407 ± 0.0461067 (W 0.0158875) | 68.6886 ± 0.0788656 (W 0.0909276) | 🔵 tlinalg-pool 5.70× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 53.9233 ± 0.0599799 (W 0.0749021) | 326.327 ± 0.795657 (W 0.867166) | 🔵 tlinalg-pool 6.05× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 0.81106 ± 0.00432819 (W 0.00180829) | 5.36828 ± 0.0322918 (W 0.00949481) | 🔵 tlinalg-pool 6.62× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 3.01918 ± 0.0072788 (W 0.00586247) | 17.5389 ± 0.0776142 (W 0.0304679) | 🔵 tlinalg-pool 5.81× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 3.77505 ± 0.0124465 (W 0.00585604) | 40.3455 ± 0.0988162 (W 0.127351) | 🔵 tlinalg-pool 10.69× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 13.9691 ± 0.0535294 (W 0.0420764) | 117.488 ± 0.520536 (W 0.331929) | 🔵 tlinalg-pool 8.41× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 0.321511 ± 0.00246462 (W 0.00262133) | 3.02505 ± 0.0120781 (W 0.00419912) | 🔵 tlinalg-pool 9.41× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.10115 ± 0.00713245 (W 0.00273028) | 10.8378 ± 0.0157782 (W 0.0121365) | 🔵 tlinalg-pool 9.84× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 8.38789 ± 0.0180417 (W 0.00377799) | 49.9183 ± 0.313165 (W 0.0469576) | 🔵 tlinalg-pool 5.95× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 36.7194 ± 0.0614782 (W 0.0761877) | 219.346 ± 1.60026 (W 1.06678) | 🔵 tlinalg-pool 5.97× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.43663 ± 0.000732288 (W 0.00288683) | 3.43392 ± 0.0145786 (W 0.00484506) | 🔵 tlinalg-pool 7.86× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 2.00053 ± 0.00461102 (W 0.00262895) | 13.5036 ± 0.0678977 (W 0.0734332) | 🔵 tlinalg-pool 6.75× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 2.86663 ± 0.0111178 (W 0.00385221) | 14.601 ± 0.00910976 (W 0.0140232) | 🔵 tlinalg-pool 5.09× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 10.708 ± 0.0148336 (W 0.00347518) | 50.392 ± 0.356908 (W 0.0387898) | 🔵 tlinalg-pool 4.71× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.265486 ± 0.00207964 (W 0.00591292) | 1.40055 ± 0.00486274 (W 0.006644) | 🔵 tlinalg-pool 5.28× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.88508 ± 0.000584717 (W 0.00139699) | 4.56507 ± 0.013053 (W 0.00695658) | 🔵 tlinalg-pool 5.16× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.512971 ± 0.00326394 (W 0.00349741) | 4.66482 ± 0.103743 (W 0.0308222) | 🔵 tlinalg-pool 9.09× faster than `lapack-openblas` |  |
| `full_piv_lu/n32/b1024` | 2.01785 ± 0.0102242 (W 0.00851108) | 28.2191 ± 1.02316 (W 0.205601) | 🔵 tlinalg-pool 13.98× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n4/b1024` | 0.490727 ± 0.00984739 (W 0.00252139) | 0.380607 ± 0.0269988 (W 0.0028506) | 🔴 tlinalg-pool 1.29× slower than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.181745 ± 0.00249448 (W 0.00227611) | 1.0397 ± 0.0456861 (W 0.00392022) | 🔵 tlinalg-pool 5.72× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 0.513976 ± 0.00852249 (W 0.00336563) | 6.42041 ± 0.104652 (W 0.0288279) | 🔵 tlinalg-pool 12.49× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 1.62409 ± 0.0267441 (W 0.0122199) | 30.7959 ± 0.901368 (W 0.201217) | 🔵 tlinalg-pool 18.96× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n4/b1024` | 0.084623 ± 0.00204834 (W 0.00160192) | 0.943367 ± 0.023635 (W 0.00396869) | 🔵 tlinalg-pool 11.15× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.207043 ± 0.00187028 (W 0.00171974) | 1.9747 ± 0.0152787 (W 0.00496096) | 🔵 tlinalg-pool 9.54× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.600686 ± 0.00480275 (W 0.00327086) | 4.55354 ± 0.0651638 (W 0.0182135) | 🔵 tlinalg-pool 7.58× faster than `lapack-openblas` |  |
| `householder_apply/n32/b1024` | 2.4037 ± 0.047641 (W 0.0178887) | 19.0144 ± 0.304069 (W 0.0466222) | 🔵 tlinalg-pool 7.91× faster than `lapack-openblas` |  |
| `householder_apply/n4/b1024` | 0.0524885 ± 0.00104844 (W 0.000114757) | 0.416257 ± 0.00115757 (W 0.00277941) | 🔵 tlinalg-pool 7.93× faster than `lapack-openblas` |  |
| `householder_apply/n8/b1024` | 0.165059 ± 0.00544131 (W 0.00173327) | 1.22884 ± 0.014596 (W 0.00412832) | 🔵 tlinalg-pool 7.44× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.502355 ± 0.00446427 (W 0.00233333) | 4.36329 ± 0.00817646 (W 0.00680507) | 🔵 tlinalg-pool 8.69× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 1.67822 ± 0.00423057 (W 0.00509472) | 14.7753 ± 0.149364 (W 0.0172179) | 🔵 tlinalg-pool 8.80× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.064095 ± 0.000643758 (W 0.000785612) | 0.541187 ± 0.00232275 (W 0.00253676) | 🔵 tlinalg-pool 8.44× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.167663 ± 0.00343593 (W 0.00143299) | 1.51376 ± 0.00937809 (W 0.00506478) | 🔵 tlinalg-pool 9.03× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.377577 ± 0.00545341 (W 0.00347081) | 2.375 ± 0.0318655 (W 0.00810697) | 🔵 tlinalg-pool 6.29× faster than `lapack-openblas` |  |
| `lu/n32/b1024` | 1.35905 ± 0.00374585 (W 0.00814181) | 9.6392 ± 0.038277 (W 0.0271821) | 🔵 tlinalg-pool 7.09× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.308931 ± 0.00576927 (W 0.00407679) | 0.325143 ± 0.00490675 (W 0.002501) | 🔵 tlinalg-pool 1.05× faster than `lapack-openblas` |  |
| `lu/n8/b1024` | 0.133078 ± 0.00105501 (W 0.00280484) | 0.799091 ± 0.0041858 (W 0.0033029) | 🔵 tlinalg-pool 6.00× faster than `lapack-openblas` |  |
| `lu_factor/n16/b1024` | 0.253319 ± 0.00204211 (W 0.0012282) | 1.80803 ± 0.00593634 (W 0.00536359) | 🔵 tlinalg-pool 7.14× faster than `lapack-openblas` |  |
| `lu_factor/n32/b1024` | 0.724751 ± 0.00671793 (W 0.00335858) | 6.65292 ± 0.0241728 (W 0.0215568) | 🔵 tlinalg-pool 9.18× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.235681 ± 0.00263642 (W 0.00256672) | 0.218068 ± 0.00116717 (W 0.00192315) | 🔴 tlinalg-pool 1.08× slower than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.0963055 ± 0.000145076 (W 0.00111564) | 0.570809 ± 0.000857801 (W 0.00322589) | 🔵 tlinalg-pool 5.93× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.321701 ± 0.00194277 (W 0.00228988) | 3.4217 ± 0.0271501 (W 0.0137039) | 🔵 tlinalg-pool 10.64× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 0.890742 ± 0.00690096 (W 0.00267541) | 9.63415 ± 0.0752984 (W 0.0101755) | 🔵 tlinalg-pool 10.82× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.0580585 ± 0.000458985 (W 0.000669707) | 1.12989 ± 0.0308293 (W 0.00599019) | 🔵 tlinalg-pool 19.46× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.118136 ± 0.000803677 (W 0.00132661) | 1.48359 ± 0.0242045 (W 0.0183882) | 🔵 tlinalg-pool 12.56× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1024` | 0.0965355 ± 0.000248798 (W 0.00183763) | 1.14316 ± 0.0156915 (W 0.022709) | 🔵 tlinalg-pool 11.84× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n32/b1024` | 0.230579 ± 0.00141326 (W 0.00180504) | 2.12589 ± 0.0302216 (W 0.00845506) | 🔵 tlinalg-pool 9.22× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n4/b1024` | 0.020879 ± 0.000216649 (W 0.000117072) | 0.872656 ± 0.0289822 (W 0.0103304) | 🔵 tlinalg-pool 41.80× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.043757 ± 0.000129228 (W 0.000139445) | 0.773616 ± 0.027719 (W 0.0220679) | 🔵 tlinalg-pool 17.68× faster than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n16/b1024` | 1.13163 ± 0.0163349 (W 0.002791) | 7.9157 ± 0.0238857 (W 0.0128074) | 🔵 tlinalg-pool 6.99× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 4.24864 ± 0.0474352 (W 0.00683629) | 27.7203 ± 0.0617792 (W 0.0432045) | 🔵 tlinalg-pool 6.52× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.0998415 ± 0.00306338 (W 0.00155206) | 0.970349 ± 0.0177737 (W 0.00157336) | 🔵 tlinalg-pool 9.72× faster than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n8/b1024` | 0.311968 ± 0.0039193 (W 0.002794) | 2.64346 ± 0.0461978 (W 0.00316457) | 🔵 tlinalg-pool 8.47× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.33954 ± 0.0247196 (W 0.00383042) | 9.41807 ± 0.0307431 (W 0.0273012) | 🔵 tlinalg-pool 7.03× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 4.36241 ± 0.0362267 (W 0.00959195) | 33.9429 ± 0.0996615 (W 0.0389118) | 🔵 tlinalg-pool 7.78× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 0.173013 ± 0.000761634 (W 0.00177659) | 1.16975 ± 0.00620135 (W 0.00743195) | 🔵 tlinalg-pool 6.76× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.438108 ± 0.00657106 (W 0.00218663) | 3.06 ± 0.016017 (W 0.00948586) | 🔵 tlinalg-pool 6.98× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.361347 ± 0.00616314 (W 0.00360833) | 3.79678 ± 0.0472506 (W 0.0100512) | 🔵 tlinalg-pool 10.51× faster than `lapack-openblas` |  |
| `solve/n32/b1024` | 0.954101 ± 0.0125771 (W 0.00603535) | 9.88607 ± 0.0623269 (W 0.011833) | 🔵 tlinalg-pool 10.36× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.0541305 ± 0.00240076 (W 0.00131569) | 1.35389 ± 0.0483745 (W 0.005386) | 🔵 tlinalg-pool 25.01× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.124863 ± 0.000574878 (W 0.00114404) | 1.99801 ± 0.0625326 (W 0.00603902) | 🔵 tlinalg-pool 16.00× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 6.71263 ± 0.0788534 (W 0.0103539) | 81.7391 ± 0.374895 (W 0.209709) | 🔵 tlinalg-pool 12.18× faster than `lapack-openblas` |  |
| `svd_full/n32/b1024` | 24.394 ± 1.19983 (W 0.0279926) | 239.801 ± 0.695131 (W 0.308791) | 🔵 tlinalg-pool 9.83× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.554038 ± 0.00431818 (W 0.00186198) | 6.38559 ± 0.0502878 (W 0.00790524) | 🔵 tlinalg-pool 11.53× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 1.92656 ± 0.0407327 (W 0.00493481) | 21.2796 ± 0.0724926 (W 0.0270118) | 🔵 tlinalg-pool 11.05× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 6.69968 ± 0.0860949 (W 0.0107965) | 81.2312 ± 0.362708 (W 0.387487) | 🔵 tlinalg-pool 12.12× faster than `lapack-openblas` |  |
| `svd_thin/n32/b1024` | 24.3833 ± 1.27509 (W 0.0207969) | 239.833 ± 0.686085 (W 0.247616) | 🔵 tlinalg-pool 9.84× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.550959 ± 0.00166872 (W 0.0014633) | 6.3831 ± 0.00828739 (W 0.0104023) | 🔵 tlinalg-pool 11.59× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1024` | 1.91573 ± 0.0403912 (W 0.00495045) | 21.2977 ± 0.0677835 (W 0.0252778) | 🔵 tlinalg-pool 11.12× faster than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 2.80121 ± 0.00674508 (W 0.00303462) | 25.1694 ± 0.143784 (W 0.021472) | 🔵 tlinalg-pool 8.99× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 9.40885 ± 0.0111256 (W 0.00363963) | 80.3219 ± 0.412277 (W 0.0572072) | 🔵 tlinalg-pool 8.54× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.364607 ± 0.00115105 (W 0.00246096) | 3.47854 ± 0.0186119 (W 0.00438474) | 🔵 tlinalg-pool 9.54× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.00089 ± 0.0040894 (W 0.00109646) | 8.97877 ± 0.0320078 (W 0.0152339) | 🔵 tlinalg-pool 8.97× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.067567 ± 0.000130622 (W 0.000267798) | 0.892791 ± 0.0237526 (W 0.00429517) | 🔵 tlinalg-pool 13.21× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n32/b1024` | 0.15548 ± 0.000393245 (W 0.00252432) | 1.45457 ± 0.019336 (W 0.00812141) | 🔵 tlinalg-pool 9.36× faster than `lapack-openblas` |  |
| `triangular_solve/n4/b1024` | 0.014232 ± 0.000110575 (W 0.000132151) | 0.728797 ± 0.00496041 (W 0.00572223) | 🔵 tlinalg-pool 51.21× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `triangular_solve/n8/b1024` | 0.030662 ± 4.60462e-05 (W 0.000197025) | 0.75081 ± 0.016843 (W 0.00288527) | 🔵 tlinalg-pool 24.49× faster than `lapack-openblas` | `!` between-start range over 5% |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.159062 ± 0.00130739 (W 0.00274728) | 1.62674 ± 0.0104738 (W 0.00408663) | 🔵 tlinalg-pool 10.23× faster than `lapack-openblas` |  |
| `cholesky/n32/b1024` | 0.789562 ± 0.00260151 (W 0.00713372) | 6.25099 ± 0.0501785 (W 0.0151327) | 🔵 tlinalg-pool 7.92× faster than `lapack-openblas` |  |
| `cholesky/n4/b1024` | 0.0272655 ± 0.000191386 (W 0.000103597) | 0.23294 ± 0.00142157 (W 0.00184261) | 🔵 tlinalg-pool 8.54× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.0541565 ± 0.000776093 (W 0.000330167) | 0.486499 ± 0.0027517 (W 0.003087) | 🔵 tlinalg-pool 8.98× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 16.4743 ± 0.0470622 (W 0.0291885) | 199.558 ± 0.316575 (W 0.416798) | 🔵 tlinalg-pool 12.11× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 67.6885 ± 0.168118 (W 0.0695433) | 887.365 ± 0.969612 (W 0.604017) | 🔵 tlinalg-pool 13.11× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 1.39333 ± 0.005445 (W 0.00220189) | 13.2164 ± 0.0278565 (W 0.0168063) | 🔵 tlinalg-pool 9.49× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 4.58276 ± 0.0253773 (W 0.0061749) | 46.6916 ± 0.0296345 (W 0.0692426) | 🔵 tlinalg-pool 10.19× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 3.99912 ± 0.0090377 (W 0.00789061) | 45.2721 ± 0.116678 (W 0.0687271) | 🔵 tlinalg-pool 11.32× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 17.3535 ± 0.0435644 (W 0.00631603) | 188.773 ± 0.548558 (W 0.448474) | 🔵 tlinalg-pool 10.88× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 0.382165 ± 0.00132588 (W 0.00251673) | 3.60295 ± 0.0227283 (W 0.0104473) | 🔵 tlinalg-pool 9.43× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.17084 ± 0.00174627 (W 0.00494757) | 12.409 ± 0.0397098 (W 0.0221547) | 🔵 tlinalg-pool 10.60× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 9.93755 ± 0.0216039 (W 0.0066637) | 149.5 ± 0.165276 (W 0.238409) | 🔵 tlinalg-pool 15.04× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 43.0953 ± 0.0442385 (W 0.0422816) | 600.637 ± 0.415447 (W 0.860142) | 🔵 tlinalg-pool 13.94× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.712661 ± 0.0180842 (W 0.00222014) | 10.0478 ± 0.0232584 (W 0.0105317) | 🔵 tlinalg-pool 14.10× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigvals/n8/b1024` | 2.59928 ± 0.0170121 (W 0.00307979) | 37.0356 ± 0.102969 (W 0.0652585) | 🔵 tlinalg-pool 14.25× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 3.04725 ± 0.00513236 (W 0.00163792) | 19.3535 ± 0.0711981 (W 0.0550344) | 🔵 tlinalg-pool 6.35× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 11.568 ± 0.0309871 (W 0.0179527) | 73.5348 ± 0.36779 (W 0.158557) | 🔵 tlinalg-pool 6.36× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.315645 ± 0.00143106 (W 0.00152111) | 2.11463 ± 0.00861618 (W 0.00705965) | 🔵 tlinalg-pool 6.70× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.955715 ± 0.00282143 (W 0.000642207) | 6.18328 ± 0.00768135 (W 0.0120181) | 🔵 tlinalg-pool 6.47× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.693561 ± 0.00557338 (W 0.00833725) | 33.5116 ± 0.32423 (W 0.052879) | 🔵 tlinalg-pool 48.32× faster than `lapack-openblas` |  |
| `full_piv_lu/n32/b1024` | 3.07365 ± 0.00763754 (W 0.0153201) | 200.19 ± 2.23928 (W 0.262725) | 🔵 tlinalg-pool 65.13× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1024` | 0.0868575 ± 0.000450967 (W 0.000553485) | 0.904978 ± 0.00594379 (W 0.00231421) | 🔵 tlinalg-pool 10.42× faster than `lapack-openblas` |  |
| `full_piv_lu/n8/b1024` | 0.20897 ± 0.00130761 (W 0.00291477) | 3.8548 ± 0.0357048 (W 0.00431812) | 🔵 tlinalg-pool 18.45× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n16/b1024` | 0.810904 ± 0.00504016 (W 0.00327673) | 37.9288 ± 0.277931 (W 0.10979) | 🔵 tlinalg-pool 46.77× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 2.77669 ± 0.0123224 (W 0.00750864) | 211.551 ± 0.339389 (W 0.448052) | 🔵 tlinalg-pool 76.19× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.120119 ± 0.00274961 (W 0.00203604) | 2.19535 ± 0.0131106 (W 0.00409847) | 🔵 tlinalg-pool 18.28× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.28927 ± 0.000984667 (W 0.00233225) | 6.18135 ± 0.0321025 (W 0.00820311) | 🔵 tlinalg-pool 21.37× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.629953 ± 0.00691944 (W 0.00339999) | 7.25902 ± 0.070995 (W 0.0142655) | 🔵 tlinalg-pool 11.52× faster than `lapack-openblas` |  |
| `householder_apply/n32/b1024` | 3.58153 ± 0.0182098 (W 0.00927157) | 35.6612 ± 0.592633 (W 0.0514225) | 🔵 tlinalg-pool 9.96× faster than `lapack-openblas` |  |
| `householder_apply/n4/b1024` | 0.0511405 ± 0.000823768 (W 0.000101746) | 0.431618 ± 0.00490503 (W 0.00281295) | 🔵 tlinalg-pool 8.44× faster than `lapack-openblas` |  |
| `householder_apply/n8/b1024` | 0.152185 ± 0.00170256 (W 0.00142511) | 1.4846 ± 0.0110004 (W 0.00363466) | 🔵 tlinalg-pool 9.76× faster than `lapack-openblas` |  |
| `householder_factor/n16/b1024` | 0.606314 ± 0.00460054 (W 0.00316954) | 7.37307 ± 0.0218048 (W 0.020809) | 🔵 tlinalg-pool 12.16× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 2.58324 ± 0.0259079 (W 0.00788932) | 27.2083 ± 0.224213 (W 0.0250668) | 🔵 tlinalg-pool 10.53× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.078933 ± 0.000271478 (W 0.000717818) | 0.92866 ± 0.0053982 (W 0.00136333) | 🔵 tlinalg-pool 11.77× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.20289 ± 0.000885718 (W 0.00219293) | 2.37673 ± 0.011196 (W 0.00354731) | 🔵 tlinalg-pool 11.71× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.452064 ± 0.00595858 (W 0.0051685) | 3.80046 ± 0.0706235 (W 0.0172451) | 🔵 tlinalg-pool 8.41× faster than `lapack-openblas` |  |
| `lu/n32/b1024` | 2.20489 ± 0.297474 (W 0.0098058) | 15.4834 ± 0.118325 (W 0.0268939) | 🔵 tlinalg-pool 7.02× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu/n4/b1024` | 0.062962 ± 0.00194607 (W 0.00093286) | 0.380345 ± 0.00055842 (W 0.00253832) | 🔵 tlinalg-pool 6.04× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.135823 ± 0.00187257 (W 0.00180607) | 1.07179 ± 0.0259904 (W 0.00369569) | 🔵 tlinalg-pool 7.89× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n16/b1024` | 0.285784 ± 0.00195427 (W 0.00154421) | 2.67201 ± 0.0108861 (W 0.00492857) | 🔵 tlinalg-pool 9.35× faster than `lapack-openblas` |  |
| `lu_factor/n32/b1024` | 1.24379 ± 0.00485323 (W 0.00454305) | 11.2197 ± 0.0582627 (W 0.0140782) | 🔵 tlinalg-pool 9.02× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.0618 ± 0.000828021 (W 0.000736869) | 0.272273 ± 0.00183013 (W 0.00270513) | 🔵 tlinalg-pool 4.41× faster than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.102837 ± 0.000800759 (W 0.000756855) | 0.75845 ± 0.00591768 (W 0.00314286) | 🔵 tlinalg-pool 7.38× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.456341 ± 0.00228248 (W 0.00382225) | 5.0152 ± 0.0354361 (W 0.0168429) | 🔵 tlinalg-pool 10.99× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 1.69976 ± 0.00832749 (W 0.00876265) | 15.3915 ± 0.0959248 (W 0.0173434) | 🔵 tlinalg-pool 9.06× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.0716235 ± 0.000251994 (W 0.000749867) | 1.08461 ± 0.0246809 (W 0.00331866) | 🔵 tlinalg-pool 15.14× faster than `lapack-openblas` |  |
| `lu_factor_solve/n8/b1024` | 0.158265 ± 0.00101926 (W 0.00171245) | 2.28488 ± 0.0186497 (W 0.00395624) | 🔵 tlinalg-pool 14.44× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n16/b1024` | 0.183593 ± 0.000693648 (W 0.00209728) | 1.94071 ± 0.0188675 (W 0.00582349) | 🔵 tlinalg-pool 10.57× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n32/b1024` | 0.883543 ± 0.00411936 (W 0.00492554) | 3.97498 ± 0.0145955 (W 0.0114871) | 🔵 tlinalg-pool 4.50× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n4/b1024` | 0.0338985 ± 0.000287485 (W 0.000978675) | 0.738332 ± 0.0230728 (W 0.00812342) | 🔵 tlinalg-pool 21.78× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.075947 ± 0.00133085 (W 0.0023283) | 1.33113 ± 0.0178594 (W 0.005578) | 🔵 tlinalg-pool 17.53× faster than `lapack-openblas` |  |
| `qr/n16/b1024` | 1.38979 ± 0.0131635 (W 0.00267334) | 12.6535 ± 0.0333635 (W 0.0197933) | 🔵 tlinalg-pool 9.10× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 8.98437 ± 0.0156825 (W 0.0122393) | 49.716 ± 0.151979 (W 0.0297603) | 🔵 tlinalg-pool 5.53× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.120069 ± 0.000307938 (W 0.00173867) | 1.41444 ± 0.00313905 (W 0.00462517) | 🔵 tlinalg-pool 11.78× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 0.344443 ± 0.004983 (W 0.00218782) | 3.81496 ± 0.0107827 (W 0.00738757) | 🔵 tlinalg-pool 11.08× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.57611 ± 0.0108635 (W 0.00338987) | 16.7461 ± 0.13679 (W 0.0484499) | 🔵 tlinalg-pool 10.62× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 8.45979 ± 0.0519795 (W 0.0053784) | 65.9682 ± 0.709937 (W 0.232265) | 🔵 tlinalg-pool 7.80× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 0.192419 ± 0.00118363 (W 0.00245747) | 1.8322 ± 0.0109445 (W 0.00504253) | 🔵 tlinalg-pool 9.52× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.490491 ± 0.00476331 (W 0.00239938) | 5.03178 ± 0.0391005 (W 0.0106656) | 🔵 tlinalg-pool 10.26× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.500169 ± 0.00507737 (W 0.00349656) | 5.22424 ± 0.107667 (W 0.0192598) | 🔵 tlinalg-pool 10.44× faster than `lapack-openblas` |  |
| `solve/n32/b1024` | 1.84476 ± 0.00554016 (W 0.00388755) | 16.2077 ± 0.0889315 (W 0.0414741) | 🔵 tlinalg-pool 8.79× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.082625 ± 0.00052642 (W 0.00118009) | 1.47177 ± 0.0403435 (W 0.00674015) | 🔵 tlinalg-pool 17.81× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.184169 ± 0.00330337 (W 0.00236671) | 2.34442 ± 0.0343942 (W 0.00965731) | 🔵 tlinalg-pool 12.73× faster than `lapack-openblas` |  |
| `svd_full/n16/b1024` | 7.42704 ± 0.0520266 (W 0.014295) | 93.6215 ± 0.648417 (W 0.134413) | 🔵 tlinalg-pool 12.61× faster than `lapack-openblas` |  |
| `svd_full/n32/b1024` | 31.2703 ± 0.41645 (W 0.0580309) | 297.963 ± 1.04896 (W 0.307396) | 🔵 tlinalg-pool 9.53× faster than `lapack-openblas` |  |
| `svd_full/n4/b1024` | 0.6598 ± 0.00476044 (W 0.00339917) | 7.85723 ± 0.0488398 (W 0.0176997) | 🔵 tlinalg-pool 11.91× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 2.09747 ± 0.0366902 (W 0.00381899) | 24.9989 ± 0.0508982 (W 0.0242033) | 🔵 tlinalg-pool 11.92× faster than `lapack-openblas` |  |
| `svd_thin/n16/b1024` | 7.52638 ± 0.571516 (W 0.0157546) | 93.4948 ± 0.661405 (W 0.164877) | 🔵 tlinalg-pool 12.42× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 31.2768 ± 0.426149 (W 0.0367198) | 296.806 ± 0.73244 (W 0.432496) | 🔵 tlinalg-pool 9.49× faster than `lapack-openblas` |  |
| `svd_thin/n4/b1024` | 0.665102 ± 0.0954963 (W 0.00320745) | 7.88211 ± 0.0484093 (W 0.0183797) | 🔵 tlinalg-pool 11.85× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_thin/n8/b1024` | 2.09426 ± 0.0175989 (W 0.00463288) | 24.9176 ± 0.0792485 (W 0.0214294) | 🔵 tlinalg-pool 11.90× faster than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 3.21636 ± 0.00562081 (W 0.00533522) | 33.356 ± 0.0478038 (W 0.0390065) | 🔵 tlinalg-pool 10.37× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 11.3452 ± 0.0383792 (W 0.017261) | 110.288 ± 0.170946 (W 0.241987) | 🔵 tlinalg-pool 9.72× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.444585 ± 0.00263405 (W 0.0019707) | 4.63661 ± 0.00897783 (W 0.0118308) | 🔵 tlinalg-pool 10.43× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.15105 ± 0.00305015 (W 0.00343574) | 11.2318 ± 0.0304283 (W 0.0114169) | 🔵 tlinalg-pool 9.76× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.128159 ± 0.000590696 (W 0.00145575) | 1.35403 ± 0.022805 (W 0.00537598) | 🔵 tlinalg-pool 10.57× faster than `lapack-openblas` |  |
| `triangular_solve/n32/b1024` | 0.54113 ± 0.00168554 (W 0.00404225) | 2.95808 ± 0.0122955 (W 0.00865424) | 🔵 tlinalg-pool 5.47× faster than `lapack-openblas` |  |
| `triangular_solve/n4/b1024` | 0.0238695 ± 9.34715e-05 (W 0.000163881) | 0.836184 ± 0.0381106 (W 0.00421606) | 🔵 tlinalg-pool 35.03× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.054261 ± 0.000146425 (W 0.000265915) | 0.921692 ± 0.0295967 (W 0.00510691) | 🔵 tlinalg-pool 16.99× faster than `lapack-openblas` | `!` between-start range over 5% |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.067015 ± 0.00249008 (W 0.00167634) | 0.073498 ± 0.000412084 (W 0.000496183) | 🔵 tlinalg-pool 1.10× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n128/b1` | 0.171885 ± 0.00204343 (W 0.00216169) | 0.144766 ± 0.000583045 (W 0.0023018) | 🔴 tlinalg-pool 1.19× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.0906945 ± 0.000806638 (W 0.000406995) | 0.130094 ± 0.000442732 (W 0.00180469) | 🔵 tlinalg-pool 1.43× faster than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.100693 ± 0.000534277 (W 0.000362762) | 0.146338 ± 0.000974655 (W 0.00180644) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.011326 ± 2.5e-05 (W 5.33972e-05) | 0.011812 ± 0.000126326 (W 8.49487e-05) | · | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.116378 ± 0.000521941 (W 0.00166413) | 0.152555 ± 0.000781043 (W 0.00193451) | 🔵 tlinalg-pool 1.31× faster than `lapack-openblas` |  |
| `svd_values/n128/b1` | 1.13736 ± 0.00420041 (W 0.00316293) | 1.38809 ± 0.00538877 (W 0.0019315) | 🔵 tlinalg-pool 1.22× faster than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.008035 ± 4.57347e-05 (W 6.46677e-05) | 0.006823 ± 4.64579e-05 (W 0.000155387) | 🔴 tlinalg-pool 1.18× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.154378 ± 0.00121399 (W 0.00136119) | 0.148663 ± 0.00135442 (W 0.00241366) | · |  |
| `lu/n128/b1` | 0.312814 ± 0.0111414 (W 0.00289301) | 0.235109 ± 0.00148617 (W 0.00267579) | 🔴 tlinalg-pool 1.33× slower than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n128/b1` | 0.223542 ± 0.000722141 (W 0.00185223) | 0.191172 ± 0.00110751 (W 0.00154912) | 🔴 tlinalg-pool 1.17× slower than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.257216 ± 0.00064738 (W 0.0021169) | 0.22495 ± 0.0012805 (W 0.00299671) | 🔴 tlinalg-pool 1.14× slower than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.033573 ± 0.000327221 (W 0.000131025) | 0.030216 ± 8.61215e-05 (W 0.00157309) | 🔴 tlinalg-pool 1.11× slower than `lapack-openblas` |  |
| `solve/n128/b1` | 0.277759 ± 0.000583421 (W 0.00172991) | 0.233746 ± 0.00197049 (W 0.00295684) | 🔴 tlinalg-pool 1.19× slower than `lapack-openblas` |  |
| `svd_values/n128/b1` | 1.43699 ± 0.00301638 (W 0.00308737) | 2.55921 ± 0.0113406 (W 0.00590997) | 🔵 tlinalg-pool 1.78× faster than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.0201375 ± 0.000187124 (W 0.000157184) | 0.0152435 ± 3.51224e-05 (W 0.00020538) | 🔴 tlinalg-pool 1.32× slower than `lapack-openblas` |  |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 27.3322 ± 0.0453084 (W 0.0372253) | 23.4621 ± 0.122878 (W 0.0248631) | 🔴 tlinalg-pool 1.16× slower than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 16.1879 ± 0.0274754 (W 0.0120038) | 11.3218 ± 0.00427005 (W 0.018307) | 🔴 tlinalg-pool 1.43× slower than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 1.55527 ± 0.00135776 (W 0.0034611) | 9.84521 ± 0.0344166 (W 0.0246924) | 🔵 tlinalg-pool 6.33× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 1.85676 ± 0.00752146 (W 0.0033791) | 6.64584 ± 0.0398609 (W 0.0158889) | 🔵 tlinalg-pool 3.58× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 5.45005 ± 0.00920668 (W 0.0107996) | 13.4226 ± 0.00876876 (W 0.0199025) | 🔵 tlinalg-pool 2.46× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 7.25268 ± 0.0232592 (W 0.0085771) | 22.963 ± 0.125908 (W 0.0542942) | 🔵 tlinalg-pool 3.17× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 38.603 ± 0.0801829 (W 0.040944) | 84.6993 ± 0.349874 (W 0.0402217) | 🔵 tlinalg-pool 2.19× faster than `lapack-openblas` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 37.0477 ± 0.025449 (W 0.0263328) | 203.961 ± 0.699555 (W 0.279478) | 🔵 tlinalg-pool 5.51× faster than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 20.4339 ± 0.0483683 (W 0.0465698) | 29.7177 ± 0.111502 (W 0.0296681) | 🔵 tlinalg-pool 1.45× faster than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 5.62784 ± 0.0189037 (W 0.0101283) | 14.248 ± 0.0949878 (W 0.132669) | 🔵 tlinalg-pool 2.53× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 5.1964 ± 0.0205898 (W 0.0101952) | 10.7878 ± 0.0262881 (W 0.0148401) | 🔵 tlinalg-pool 2.08× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 13.3783 ± 0.0235216 (W 0.0065343) | 21.7966 ± 0.0219168 (W 0.0324987) | 🔵 tlinalg-pool 1.63× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 14.3052 ± 0.0242476 (W 0.0220496) | 24.3731 ± 0.0682761 (W 0.0425252) | 🔵 tlinalg-pool 1.70× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 75.0588 ± 0.326549 (W 0.17168) | 100.288 ± 0.668576 (W 0.320477) | 🔵 tlinalg-pool 1.34× faster than `lapack-openblas` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 5.99124 ± 0.0503155 (W 0.0193784) | 18.0866 ± 0.243043 (W 0.027806) | 🔵 tlinalg-pool 3.02× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 22.2207 ± 0.0362647 (W 0.0365374) | 35.5599 ± 0.211378 (W 0.051498) | 🔵 tlinalg-pool 1.60× faster than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 21.6245 ± 0.0774289 (W 0.0537143) | 39.123 ± 0.320441 (W 0.073196) | 🔵 tlinalg-pool 1.81× faster than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 35.0475 ± 0.0717761 (W 0.0615287) | 60.5929 ± 0.349302 (W 0.0630142) | 🔵 tlinalg-pool 1.73× faster than `lapack-openblas` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 17.5265 ± 0.038593 (W 0.0366431) | 20.1071 ± 0.110743 (W 0.0421198) | 🔵 tlinalg-pool 1.15× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 58.8895 ± 0.21906 (W 0.0979234) | 40.4636 ± 0.0185661 (W 0.0572157) | 🔴 tlinalg-pool 1.46× slower than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 59.2562 ± 0.0590416 (W 0.113332) | 51.524 ± 0.197626 (W 0.0957277) | 🔴 tlinalg-pool 1.15× slower than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 107.863 ± 0.388861 (W 0.339214) | 85.6765 ± 0.429923 (W 0.0545142) | 🔴 tlinalg-pool 1.26× slower than `lapack-openblas` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
