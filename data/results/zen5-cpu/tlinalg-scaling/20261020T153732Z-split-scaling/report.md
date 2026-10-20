# `tlinalg-scaling` on `zen5-cpu`

- tlinalg-rs commit: `4dcd35f080a6b4fd6b1423871af66a33fd398482`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `f7f0996f8e64e5d57d85266f4a9e989e6a7ed3bc`
- toolkit commit: `d4385102914b6db32c0a0a25a2362c83ad2e7f45`
- measured binary SHA-256: `dce21ac38e7150502f3291d58bb393080b1e1f363df08a2caf08052ff5e09987`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T16:08:05.977065Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-scaling --aa 4 --reps 5 --prime-ms 250 --label split-scaling`
- raw data: `data/results/zen5-cpu/tlinalg-scaling/20261020T153732Z-split-scaling/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: The scaling table declares 8T only. The pool has nothing to parallelise at 1T (it is one lane with extra machinery), and a 1T verify pass is the slowest single thing this host runs: measured 2026-10-20, one 1T population took over twenty minutes. The baseline the table needs is the one lane *on the same budget*.
  Known blind spot: The batched regime stops at n=32: at batch 1024 the harness's verify recomputes every case with its residual checks, and n=64 pushed one verify pass past 45 minutes on this host (measured 2026-10-20). n=64 returns when verify can run on a declared grid of its own (campaign-toolkit#28), not as part of the timing run.
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
    As measured: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.73%, worst 100.78% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 63 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.48%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
`🔵 tlinalg X faster than <row>` / `🔴 tlinalg X slower than <row>` (the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

## batch-small, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.834399 ± 0.0206276 (W 0.00239448) | 0.115771 ± 0.00246288 (W 0.0013635) | 🔴 tlinalg 7.21× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 3.21097 ± 0.157693 (W 0.00756325) | 0.467643 ± 0.192095 (W 0.0047896) | 🔴 tlinalg 6.87× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `cholesky/n4/b1024` | 0.177357 ± 0.00106666 (W 0.0012365) | 0.0295955 ± 0.000282162 (W 0.000563608) | 🔴 tlinalg 5.99× slower than `tlinalg-pool` |  |
| `cholesky/n8/b1024` | 0.357468 ± 0.00528306 (W 0.00219791) | 0.0528385 ± 0.00103164 (W 0.000623721) | 🔴 tlinalg 6.77× slower than `tlinalg-pool` |  |
| `eig/n16/b1024` | 93.9476 ± 0.238012 (W 0.270431) | 11.8539 ± 3.0782 (W 0.0431706) | 🔴 tlinalg 7.93× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `eig/n32/b1024` | 424.115 ± 0.661304 (W 1.98888) | 53.3789 ± 0.120471 (W 0.227706) | 🔴 tlinalg 7.95× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 6.12948 ± 0.0842218 (W 0.0142641) | 0.796852 ± 0.0189745 (W 0.00416865) | 🔴 tlinalg 7.69× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eig/n8/b1024` | 23.3767 ± 0.0427431 (W 0.034631) | 2.94881 ± 0.315436 (W 0.00804174) | 🔴 tlinalg 7.93× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigh/n16/b1024` | 29.5235 ± 0.0394945 (W 0.0275793) | 3.75896 ± 0.0137049 (W 0.00542855) | 🔴 tlinalg 7.85× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 113.357 ± 0.114953 (W 0.364745) | 14.3745 ± 0.0342731 (W 0.0365927) | 🔴 tlinalg 7.89× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.4001 ± 0.00210961 (W 0.00413868) | 0.313305 ± 0.00647067 (W 0.00214082) | 🔴 tlinalg 7.66× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 8.40233 ± 0.0189289 (W 0.0154245) | 1.07493 ± 0.00729081 (W 0.00677081) | 🔴 tlinalg 7.82× slower than `tlinalg-pool` |  |
| `eigvals/n16/b1024` | 64.7077 ± 0.109307 (W 0.0574165) | 8.17543 ± 0.0404928 (W 0.0287873) | 🔴 tlinalg 7.91× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 288.371 ± 0.447041 (W 0.36753) | 36.2799 ± 0.0524805 (W 0.034587) | 🔴 tlinalg 7.95× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 3.16781 ± 0.0699432 (W 0.00860649) | 0.418798 ± 0.00804434 (W 0.00261942) | 🔴 tlinalg 7.56× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 15.2972 ± 0.0560441 (W 0.0309524) | 1.9516 ± 0.0252354 (W 0.00850397) | 🔴 tlinalg 7.84× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 22.2014 ± 0.0820586 (W 0.0245674) | 2.81305 ± 0.0318384 (W 0.00513313) | 🔴 tlinalg 7.89× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 86.2184 ± 0.121087 (W 0.0754981) | 10.9233 ± 0.0224365 (W 0.0352113) | 🔴 tlinalg 7.89× slower than `tlinalg-pool` |  |
| `eigvalsh/n4/b1024` | 1.95037 ± 0.00407865 (W 0.00466356) | 0.253108 ± 0.0013214 (W 0.00172667) | 🔴 tlinalg 7.71× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 6.7735 ± 0.0196157 (W 0.00829981) | 0.857917 ± 0.00217809 (W 0.00214969) | 🔴 tlinalg 7.90× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 3.28478 ± 0.109861 (W 0.0140587) | 0.456893 ± 0.00626719 (W 0.00468287) | 🔴 tlinalg 7.19× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu/n32/b1024` | 13.7145 ± 0.164918 (W 0.0481204) | 1.98462 ± 0.00412115 (W 0.0263595) | 🔴 tlinalg 6.91× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.387458 ± 0.00713331 (W 0.00224716) | 0.0843025 ± 0.00141432 (W 0.00192801) | 🔴 tlinalg 4.60× slower than `tlinalg-pool` |  |
| `full_piv_lu/n8/b1024` | 1.05337 ± 0.0102775 (W 0.00611232) | 0.170915 ± 0.0412707 (W 0.00432597) | 🔴 tlinalg 6.16× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `full_piv_lu_solve/n16/b1024` | 3.32685 ± 0.0195554 (W 0.0124934) | 0.444275 ± 0.00380066 (W 0.00295527) | 🔴 tlinalg 7.49× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 11.2798 ± 0.186261 (W 0.0329916) | 1.50572 ± 0.0113488 (W 0.0522892) | 🔴 tlinalg 7.49× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.511926 ± 0.00483762 (W 0.00304537) | 0.079584 ± 0.0058467 (W 0.00376524) | 🔴 tlinalg 6.43× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `full_piv_lu_solve/n8/b1024` | 1.25398 ± 0.0478148 (W 0.00654107) | 0.169186 ± 0.00284299 (W 0.00240285) | 🔴 tlinalg 7.41× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n16/b1024` | 4.49038 ± 0.0561077 (W 0.00658266) | 0.603082 ± 0.00780087 (W 0.00361894) | 🔴 tlinalg 7.45× slower than `tlinalg-pool` |  |
| `householder_apply/n32/b1024` | 18.689 ± 0.448389 (W 0.0419427) | 2.44935 ± 0.0388346 (W 0.0220328) | 🔴 tlinalg 7.63× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.356131 ± 0.00675635 (W 0.00167046) | 0.0521475 ± 0.000767082 (W 0.000703345) | 🔴 tlinalg 6.83× slower than `tlinalg-pool` |  |
| `householder_apply/n8/b1024` | 1.16693 ± 0.0220384 (W 0.00319348) | 0.171145 ± 0.0688338 (W 0.00253606) | 🔴 tlinalg 6.82× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `householder_factor/n16/b1024` | 3.639 ± 0.0415637 (W 0.0103227) | 0.476099 ± 0.00349353 (W 0.00147625) | 🔴 tlinalg 7.64× slower than `tlinalg-pool` |  |
| `householder_factor/n32/b1024` | 12.3586 ± 0.106073 (W 0.0413696) | 1.64145 ± 0.00988733 (W 0.0140674) | 🔴 tlinalg 7.53× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.445382 ± 0.00170931 (W 0.00245356) | 0.063889 ± 0.000410601 (W 0.00140901) | 🔴 tlinalg 6.97× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.18917 ± 0.00642114 (W 0.00324353) | 0.164668 ± 0.00416425 (W 0.00125089) | 🔴 tlinalg 7.22× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n16/b1024` | 2.63655 ± 0.0290818 (W 0.037127) | 0.368228 ± 0.00147518 (W 0.00516434) | 🔴 tlinalg 7.16× slower than `tlinalg-pool` |  |
| `lu/n32/b1024` | 8.95705 ± 0.159267 (W 0.0396835) | 1.32875 ± 0.0477899 (W 0.0245319) | 🔴 tlinalg 6.74× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n4/b1024` | 0.291304 ± 0.00437891 (W 0.0021509) | 0.072801 ± 0.000324772 (W 0.00253334) | 🔴 tlinalg 4.00× slower than `tlinalg-pool` |  |
| `lu/n8/b1024` | 0.833122 ± 0.0129713 (W 0.00276032) | 0.143102 ± 0.00129722 (W 0.00243022) | 🔴 tlinalg 5.82× slower than `tlinalg-pool` |  |
| `lu_factor/n16/b1024` | 1.89662 ± 0.0239902 (W 0.0108108) | 0.269359 ± 0.00162886 (W 0.00244377) | 🔴 tlinalg 7.04× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 5.57359 ± 0.097882 (W 0.0326071) | 0.756428 ± 0.0145667 (W 0.00383209) | 🔴 tlinalg 7.37× slower than `tlinalg-pool` |  |
| `lu_factor/n4/b1024` | 0.220061 ± 0.0033877 (W 0.00225496) | 0.0634435 ± 0.00135016 (W 0.00178608) | 🔴 tlinalg 3.47× slower than `tlinalg-pool` |  |
| `lu_factor/n8/b1024` | 0.594921 ± 0.0113457 (W 0.00595661) | 0.112274 ± 0.0006012 (W 0.00109201) | 🔴 tlinalg 5.30× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 2.40016 ± 0.0321269 (W 0.00615788) | 0.343894 ± 0.0091874 (W 0.00445236) | 🔴 tlinalg 6.98× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n32/b1024` | 6.86429 ± 0.106518 (W 0.0174578) | 0.925926 ± 0.00858069 (W 0.00537205) | 🔴 tlinalg 7.41× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n4/b1024` | 0.279236 ± 0.0078079 (W 0.00239888) | 0.0648115 ± 0.00171323 (W 0.00141361) | 🔴 tlinalg 4.31× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.796309 ± 0.00875365 (W 0.00572425) | 0.129983 ± 0.00136872 (W 0.00159299) | 🔴 tlinalg 6.13× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 0.599741 ± 0.00254194 (W 0.00264169) | 0.10712 ± 0.000861744 (W 0.00085255) | 🔴 tlinalg 5.60× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 2.37374 ± 0.149465 (W 0.032115) | 0.303423 ± 0.00599687 (W 0.00969537) | 🔴 tlinalg 7.82× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.067606 ± 0.000190395 (W 0.000208408) | 0.0337385 ± 0.00231428 (W 0.000674291) | 🔴 tlinalg 2.00× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.228878 ± 0.00122296 (W 0.00172599) | 0.056526 ± 0.00968915 (W 0.00144878) | 🔴 tlinalg 4.05× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `qr/n16/b1024` | 8.61569 ± 0.0818835 (W 0.0182122) | 1.12554 ± 0.00668549 (W 0.00268624) | 🔴 tlinalg 7.65× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 35.5413 ± 0.142246 (W 0.0860075) | 4.521 ± 0.0304367 (W 0.0125401) | 🔴 tlinalg 7.86× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.734899 ± 0.00963569 (W 0.00277969) | 0.100132 ± 0.00144782 (W 0.000919938) | 🔴 tlinalg 7.34× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.33649 ± 0.0348709 (W 0.00476189) | 0.308181 ± 0.00391725 (W 0.00226383) | 🔴 tlinalg 7.58× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 9.80854 ± 0.054607 (W 0.0162024) | 1.28292 ± 0.014335 (W 0.00235089) | 🔴 tlinalg 7.65× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 35.4578 ± 0.245637 (W 0.0407095) | 4.58129 ± 0.0527989 (W 0.0242283) | 🔴 tlinalg 7.74× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.15066 ± 0.0166106 (W 0.00352394) | 0.15289 ± 0.0013069 (W 0.00182799) | 🔴 tlinalg 7.53× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n8/b1024` | 3.15465 ± 0.0750939 (W 0.00623395) | 0.415512 ± 0.00640017 (W 0.00571855) | 🔴 tlinalg 7.59× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n16/b1024` | 2.61447 ± 0.0345647 (W 0.0107793) | 0.351897 ± 0.00245635 (W 0.00180867) | 🔴 tlinalg 7.43× slower than `tlinalg-pool` |  |
| `solve/n32/b1024` | 7.11509 ± 0.0873153 (W 0.015678) | 0.942006 ± 0.00979646 (W 0.0053982) | 🔴 tlinalg 7.55× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.369551 ± 0.00568729 (W 0.00250256) | 0.0541805 ± 0.00124961 (W 0.00124077) | 🔴 tlinalg 6.82× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n8/b1024` | 0.917075 ± 0.02627 (W 0.00574888) | 0.129086 ± 0.00218602 (W 0.00234587) | 🔴 tlinalg 7.10× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 55.4367 ± 2.04464 (W 0.0516291) | 7.25063 ± 0.13639 (W 0.0401261) | 🔴 tlinalg 7.65× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 201.797 ± 0.693149 (W 0.241536) | 26.395 ± 0.483229 (W 0.0364091) | 🔴 tlinalg 7.65× slower than `tlinalg-pool` |  |
| `svd_full/n4/b1024` | 4.28514 ± 0.0817761 (W 0.00623124) | 0.544426 ± 0.00542063 (W 0.0045284) | 🔴 tlinalg 7.87× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 15.1361 ± 0.433623 (W 0.030563) | 1.93609 ± 0.968552 (W 0.00777939) | 🔴 tlinalg 7.82× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_thin/n16/b1024` | 55.3556 ± 2.1201 (W 0.224881) | 7.25518 ± 0.178416 (W 0.00943953) | 🔴 tlinalg 7.63× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 201.786 ± 0.444401 (W 0.419156) | 26.0191 ± 1.51526 (W 0.195472) | 🔴 tlinalg 7.76× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 4.21921 ± 0.0635364 (W 0.00759478) | 0.545919 ± 0.0329216 (W 0.00320802) | 🔴 tlinalg 7.73× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 15.0707 ± 0.123277 (W 0.0199625) | 1.92375 ± 0.0164883 (W 0.00568739) | 🔴 tlinalg 7.83× slower than `tlinalg-pool` |  |
| `svd_values/n16/b1024` | 40.6847 ± 0.159167 (W 0.0495048) | 5.17543 ± 0.0308109 (W 0.0145134) | 🔴 tlinalg 7.86× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 158.74 ± 0.281849 (W 0.259766) | 20.1183 ± 0.0657362 (W 0.0530075) | 🔴 tlinalg 7.89× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 3.16747 ± 0.0359421 (W 0.0059954) | 0.413297 ± 0.00253927 (W 0.00416976) | 🔴 tlinalg 7.66× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 11.2685 ± 0.0592124 (W 0.0141284) | 1.43721 ± 0.123369 (W 0.0080135) | 🔴 tlinalg 7.84× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n16/b1024` | 0.502001 ± 0.00286163 (W 0.00267199) | 0.084918 ± 0.00014994 (W 0.00395106) | 🔴 tlinalg 5.91× slower than `tlinalg-pool` |  |
| `triangular_solve/n32/b1024` | 1.92455 ± 0.0308573 (W 0.0283942) | 0.219544 ± 0.0108595 (W 0.00670248) | 🔴 tlinalg 8.77× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.0917515 ± 0.00036472 (W 0.00161546) | 0.01885 ± 0.000359222 (W 0.00104772) | 🔴 tlinalg 4.87× slower than `tlinalg-pool` |  |
| `triangular_solve/n8/b1024` | 0.219996 ± 0.000644384 (W 0.00209219) | 0.0355515 ± 0.000573768 (W 0.0014282) | 🔴 tlinalg 6.19× slower than `tlinalg-pool` |  |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 1.29089 ± 0.0292833 (W 0.00584749) | 0.170764 ± 0.00111154 (W 0.00204047) | 🔴 tlinalg 7.56× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 5.8643 ± 0.0396675 (W 0.020017) | 0.823733 ± 0.0100844 (W 0.00641613) | 🔴 tlinalg 7.12× slower than `tlinalg-pool` |  |
| `cholesky/n4/b1024` | 0.1981 ± 0.00228771 (W 0.00198212) | 0.032376 ± 0.000399967 (W 0.000591589) | 🔴 tlinalg 6.12× slower than `tlinalg-pool` |  |
| `cholesky/n8/b1024` | 0.414495 ± 0.00521187 (W 0.00297911) | 0.060127 ± 0.000741689 (W 0.00086012) | 🔴 tlinalg 6.89× slower than `tlinalg-pool` |  |
| `eig/n16/b1024` | 128.62 ± 0.459392 (W 0.0779803) | 16.4089 ± 0.0332443 (W 0.0545899) | 🔴 tlinalg 7.84× slower than `tlinalg-pool` |  |
| `eig/n32/b1024` | 533.694 ± 0.317173 (W 0.423589) | 67.3061 ± 0.181442 (W 0.31173) | 🔴 tlinalg 7.93× slower than `tlinalg-pool` |  |
| `eig/n4/b1024` | 10.0099 ± 0.174728 (W 0.0194573) | 1.29905 ± 0.142458 (W 0.00237675) | 🔴 tlinalg 7.71× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `eig/n8/b1024` | 34.7028 ± 0.0897963 (W 0.0292359) | 4.46275 ± 0.0377621 (W 0.0127829) | 🔴 tlinalg 7.78× slower than `tlinalg-pool` |  |
| `eigh/n16/b1024` | 32.1301 ± 0.103847 (W 0.0530713) | 4.02897 ± 0.00906638 (W 0.00630733) | 🔴 tlinalg 7.97× slower than `tlinalg-pool` |  |
| `eigh/n32/b1024` | 141.12 ± 0.240074 (W 0.0868826) | 17.9171 ± 0.0511318 (W 0.0514333) | 🔴 tlinalg 7.88× slower than `tlinalg-pool` |  |
| `eigh/n4/b1024` | 2.8891 ± 0.00429134 (W 0.00419958) | 0.377159 ± 0.00588162 (W 0.00181297) | 🔴 tlinalg 7.66× slower than `tlinalg-pool` |  |
| `eigh/n8/b1024` | 9.0421 ± 0.0160409 (W 0.0157834) | 1.15374 ± 0.13678 (W 0.00965546) | 🔴 tlinalg 7.84× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigvals/n16/b1024` | 76.9161 ± 0.223411 (W 0.220926) | 9.70342 ± 0.024091 (W 0.029657) | 🔴 tlinalg 7.93× slower than `tlinalg-pool` |  |
| `eigvals/n32/b1024` | 336.891 ± 0.572277 (W 0.379533) | 42.6038 ± 0.478852 (W 0.204945) | 🔴 tlinalg 7.91× slower than `tlinalg-pool` |  |
| `eigvals/n4/b1024` | 4.7415 ± 0.0308841 (W 0.00544709) | 0.62039 ± 0.00726649 (W 0.00425855) | 🔴 tlinalg 7.64× slower than `tlinalg-pool` |  |
| `eigvals/n8/b1024` | 19.7907 ± 0.0653643 (W 0.0291295) | 2.52065 ± 0.014498 (W 0.00427324) | 🔴 tlinalg 7.85× slower than `tlinalg-pool` |  |
| `eigvalsh/n16/b1024` | 23.7489 ± 0.0734883 (W 0.0253913) | 3.00297 ± 0.0690593 (W 0.00726628) | 🔴 tlinalg 7.91× slower than `tlinalg-pool` |  |
| `eigvalsh/n32/b1024` | 92.8581 ± 0.158457 (W 0.217074) | 11.8588 ± 1.23219 (W 0.4042) | 🔴 tlinalg 7.83× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `eigvalsh/n4/b1024` | 2.35952 ± 0.0116838 (W 0.0043312) | 0.311115 ± 0.00431104 (W 0.00235929) | 🔴 tlinalg 7.58× slower than `tlinalg-pool` |  |
| `eigvalsh/n8/b1024` | 7.24368 ± 0.0205867 (W 0.00478789) | 0.922759 ± 0.00144237 (W 0.00171494) | 🔴 tlinalg 7.85× slower than `tlinalg-pool` |  |
| `full_piv_lu/n16/b1024` | 4.39254 ± 0.0782984 (W 0.0345178) | 0.622588 ± 0.011492 (W 0.00965129) | 🔴 tlinalg 7.06× slower than `tlinalg-pool` |  |
| `full_piv_lu/n32/b1024` | 20.4103 ± 0.162414 (W 0.0362312) | 3.05816 ± 0.0112877 (W 0.019514) | 🔴 tlinalg 6.67× slower than `tlinalg-pool` |  |
| `full_piv_lu/n4/b1024` | 0.469697 ± 0.00583046 (W 0.00429222) | 0.0889365 ± 0.00160098 (W 0.00290287) | 🔴 tlinalg 5.28× slower than `tlinalg-pool` |  |
| `full_piv_lu/n8/b1024` | 1.24613 ± 0.0452725 (W 0.00940874) | 0.191723 ± 0.0128259 (W 0.00643463) | 🔴 tlinalg 6.50× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 5.32553 ± 0.0394773 (W 0.00927916) | 0.704331 ± 0.0105989 (W 0.00971249) | 🔴 tlinalg 7.56× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n32/b1024` | 20.1865 ± 0.223599 (W 0.033387) | 2.70862 ± 0.0279589 (W 0.0227774) | 🔴 tlinalg 7.45× slower than `tlinalg-pool` |  |
| `full_piv_lu_solve/n4/b1024` | 0.78776 ± 0.0216153 (W 0.00335938) | 0.114399 ± 0.00196835 (W 0.00282482) | 🔴 tlinalg 6.89× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 1.95992 ± 0.0294079 (W 0.0167601) | 0.275239 ± 0.03172 (W 0.00288284) | 🔴 tlinalg 7.12× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_apply/n16/b1024` | 4.98444 ± 0.0748139 (W 0.0200608) | 0.620148 ± 0.00749082 (W 0.00833137) | 🔴 tlinalg 8.04× slower than `tlinalg-pool` |  |
| `householder_apply/n32/b1024` | 27.3657 ± 0.145508 (W 0.0574776) | 3.62186 ± 0.0225619 (W 0.0297231) | 🔴 tlinalg 7.56× slower than `tlinalg-pool` |  |
| `householder_apply/n4/b1024` | 0.33243 ± 0.00223053 (W 0.00228009) | 0.050054 ± 0.000708582 (W 0.000650125) | 🔴 tlinalg 6.64× slower than `tlinalg-pool` |  |
| `householder_apply/n8/b1024` | 1.09434 ± 0.0111613 (W 0.00156231) | 0.153321 ± 0.00387495 (W 0.0042594) | 🔴 tlinalg 7.14× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 4.36538 ± 0.0132611 (W 0.00744167) | 0.577554 ± 0.0126671 (W 0.00464947) | 🔴 tlinalg 7.56× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `householder_factor/n32/b1024` | 19.5437 ± 0.106974 (W 0.0684872) | 2.55242 ± 0.0239093 (W 0.0132171) | 🔴 tlinalg 7.66× slower than `tlinalg-pool` |  |
| `householder_factor/n4/b1024` | 0.542698 ± 0.00253824 (W 0.00247521) | 0.0753305 ± 0.000600523 (W 0.00140336) | 🔴 tlinalg 7.20× slower than `tlinalg-pool` |  |
| `householder_factor/n8/b1024` | 1.41353 ± 0.00671123 (W 0.00273299) | 0.192524 ± 0.0011744 (W 0.00170825) | 🔴 tlinalg 7.34× slower than `tlinalg-pool` |  |
| `lu/n16/b1024` | 3.09149 ± 0.0606623 (W 0.0228134) | 0.436515 ± 0.00129586 (W 0.00815539) | 🔴 tlinalg 7.08× slower than `tlinalg-pool` |  |
| `lu/n32/b1024` | 14.004 ± 0.0549401 (W 0.062481) | 2.1652 ± 0.0594702 (W 0.0408669) | 🔴 tlinalg 6.47× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n4/b1024` | 0.354928 ± 0.0123485 (W 0.00264999) | 0.06989 ± 0.00298375 (W 0.00153453) | 🔴 tlinalg 5.08× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.909796 ± 0.0163234 (W 0.00431696) | 0.148703 ± 0.00181309 (W 0.00335074) | 🔴 tlinalg 6.12× slower than `tlinalg-pool` |  |
| `lu_factor/n16/b1024` | 2.09488 ± 0.0263678 (W 0.00773045) | 0.297245 ± 0.00570844 (W 0.0078676) | 🔴 tlinalg 7.05× slower than `tlinalg-pool` |  |
| `lu_factor/n32/b1024` | 9.51059 ± 0.0692684 (W 0.0275002) | 1.26604 ± 0.0300437 (W 0.0251104) | 🔴 tlinalg 7.51× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor/n4/b1024` | 0.269168 ± 0.00206155 (W 0.00211717) | 0.067266 ± 0.00140698 (W 0.00158377) | 🔴 tlinalg 4.00× slower than `tlinalg-pool` |  |
| `lu_factor/n8/b1024` | 0.657122 ± 0.00616196 (W 0.00452371) | 0.107495 ± 0.000633432 (W 0.00219589) | 🔴 tlinalg 6.11× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n16/b1024` | 3.37182 ± 0.0249524 (W 0.0115361) | 0.459719 ± 0.00462535 (W 0.00946879) | 🔴 tlinalg 7.33× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n32/b1024` | 13.1243 ± 0.0528436 (W 0.0287968) | 1.77386 ± 0.021371 (W 0.0223844) | 🔴 tlinalg 7.40× slower than `tlinalg-pool` |  |
| `lu_factor_solve/n4/b1024` | 0.418436 ± 0.00360268 (W 0.0031386) | 0.0818625 ± 0.00221843 (W 0.000985741) | 🔴 tlinalg 5.11× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 1.12725 ± 0.00464687 (W 0.00298537) | 0.164803 ± 0.0019219 (W 0.00132962) | 🔴 tlinalg 6.84× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n16/b1024` | 1.31333 ± 0.0097711 (W 0.00465165) | 0.194729 ± 0.000362327 (W 0.00175146) | 🔴 tlinalg 6.74× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n32/b1024` | 6.45575 ± 0.0611621 (W 0.0330752) | 0.909053 ± 0.00599632 (W 0.00710957) | 🔴 tlinalg 7.10× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n4/b1024` | 0.163445 ± 0.000391712 (W 0.00147681) | 0.0445885 ± 0.000528931 (W 0.000763211) | 🔴 tlinalg 3.67× slower than `tlinalg-pool` |  |
| `lu_solve_prepared/n8/b1024` | 0.487606 ± 0.00163513 (W 0.00331468) | 0.089001 ± 0.0342733 (W 0.00179646) | 🔴 tlinalg 5.48× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `qr/n16/b1024` | 10.9593 ± 0.0152814 (W 0.0305566) | 1.40153 ± 0.0075397 (W 0.0044703) | 🔴 tlinalg 7.82× slower than `tlinalg-pool` |  |
| `qr/n32/b1024` | 72.9681 ± 0.120176 (W 0.0587479) | 9.39674 ± 0.0452361 (W 0.0247122) | 🔴 tlinalg 7.77× slower than `tlinalg-pool` |  |
| `qr/n4/b1024` | 0.84884 ± 0.00166085 (W 0.00246801) | 0.114529 ± 0.000354863 (W 0.001756) | 🔴 tlinalg 7.41× slower than `tlinalg-pool` |  |
| `qr/n8/b1024` | 2.61658 ± 0.00969994 (W 0.0034936) | 0.339119 ± 0.00400074 (W 0.00475111) | 🔴 tlinalg 7.72× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n16/b1024` | 12.1268 ± 0.0228711 (W 0.0189687) | 1.561 ± 0.00755883 (W 0.00426544) | 🔴 tlinalg 7.77× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n32/b1024` | 67.0336 ± 0.368743 (W 0.155769) | 8.66209 ± 0.0438209 (W 0.0431922) | 🔴 tlinalg 7.74× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n4/b1024` | 1.39302 ± 0.0353814 (W 0.00341211) | 0.19019 ± 0.00704751 (W 0.00170917) | 🔴 tlinalg 7.32× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `rank_revealing_qr/n8/b1024` | 3.67347 ± 0.0386079 (W 0.0111088) | 0.47843 ± 0.00584371 (W 0.00268088) | 🔴 tlinalg 7.68× slower than `tlinalg-pool` |  |
| `solve/n16/b1024` | 3.70485 ± 0.0195049 (W 0.00763197) | 0.510955 ± 0.232701 (W 0.0105426) | 🔴 tlinalg 7.25× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `solve/n32/b1024` | 13.8948 ± 0.0501268 (W 0.0678021) | 1.86019 ± 0.018942 (W 0.00649097) | 🔴 tlinalg 7.47× slower than `tlinalg-pool` |  |
| `solve/n4/b1024` | 0.537199 ± 0.00275587 (W 0.00303401) | 0.0773395 ± 0.00415786 (W 0.00235482) | 🔴 tlinalg 6.95× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `solve/n8/b1024` | 1.33495 ± 0.0104209 (W 0.00493268) | 0.186293 ± 0.0098964 (W 0.00163968) | 🔴 tlinalg 7.17× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 60.5826 ± 0.390988 (W 0.0905396) | 7.75051 ± 0.0641313 (W 0.0687276) | 🔴 tlinalg 7.82× slower than `tlinalg-pool` |  |
| `svd_full/n32/b1024` | 261.591 ± 0.638245 (W 0.295944) | 33.6322 ± 0.400727 (W 0.0371528) | 🔴 tlinalg 7.78× slower than `tlinalg-pool` |  |
| `svd_full/n4/b1024` | 4.97454 ± 0.0107289 (W 0.00603418) | 0.63778 ± 0.00149241 (W 0.00242842) | 🔴 tlinalg 7.80× slower than `tlinalg-pool` |  |
| `svd_full/n8/b1024` | 16.7836 ± 0.0329613 (W 0.0133097) | 2.18316 ± 0.0393245 (W 0.0396273) | 🔴 tlinalg 7.69× slower than `tlinalg-pool` |  |
| `svd_thin/n16/b1024` | 60.7146 ± 0.41946 (W 0.105939) | 7.82398 ± 0.364042 (W 0.0458621) | 🔴 tlinalg 7.76× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n32/b1024` | 261.325 ± 1.30399 (W 0.35055) | 33.3724 ± 0.545291 (W 0.288611) | 🔴 tlinalg 7.83× slower than `tlinalg-pool` |  |
| `svd_thin/n4/b1024` | 4.98534 ± 0.014731 (W 0.00960835) | 0.637411 ± 0.017197 (W 0.0026679) | 🔴 tlinalg 7.82× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `svd_thin/n8/b1024` | 16.7124 ± 0.0614473 (W 0.0275694) | 2.16692 ± 1.05995 (W 0.00786446) | 🔴 tlinalg 7.71× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `svd_values/n16/b1024` | 45.5894 ± 0.200832 (W 0.058768) | 5.91161 ± 0.0253257 (W 0.0217128) | 🔴 tlinalg 7.71× slower than `tlinalg-pool` |  |
| `svd_values/n32/b1024` | 176.411 ± 0.210176 (W 0.370027) | 22.3513 ± 0.0591122 (W 0.0222966) | 🔴 tlinalg 7.89× slower than `tlinalg-pool` |  |
| `svd_values/n4/b1024` | 3.86602 ± 0.0122535 (W 0.00596474) | 0.494804 ± 0.00300886 (W 0.00187308) | 🔴 tlinalg 7.81× slower than `tlinalg-pool` |  |
| `svd_values/n8/b1024` | 12.97 ± 0.0348047 (W 0.0182855) | 1.64656 ± 0.00605769 (W 0.0033127) | 🔴 tlinalg 7.88× slower than `tlinalg-pool` |  |
| `triangular_solve/n16/b1024` | 0.992805 ± 0.0165924 (W 0.00627475) | 0.140067 ± 0.000808515 (W 0.00374919) | 🔴 tlinalg 7.09× slower than `tlinalg-pool` |  |
| `triangular_solve/n32/b1024` | 4.62924 ± 0.13654 (W 0.0590471) | 0.619881 ± 0.00664511 (W 0.00946411) | 🔴 tlinalg 7.47× slower than `tlinalg-pool` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.162914 ± 0.0004903 (W 0.00140045) | 0.028238 ± 0.00985332 (W 0.000851335) | 🔴 tlinalg 5.77× slower than `tlinalg-pool` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n8/b1024` | 0.399066 ± 0.00394278 (W 0.00274092) | 0.065683 ± 0.000544354 (W 0.00110158) | 🔴 tlinalg 6.08× slower than `tlinalg-pool` |  |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.063383 ± 0.00194998 (W 0.000133898) | 0.0634735 ± 0.00233641 (W 0.00103447) | · | `!` between-start range over 5% |
| `lu/n128/b1` | 0.147976 ± 0.00103348 (W 0.00167001) | 0.186148 ± 0.00293128 (W 0.00509859) | 🔵 tlinalg 1.26× faster than `tlinalg-pool` |  |
| `lu_factor/n128/b1` | 0.094857 ± 0.000461585 (W 0.00145738) | 0.129447 ± 0.0017298 (W 0.00361482) | 🔵 tlinalg 1.36× faster than `tlinalg-pool` |  |
| `lu_factor_solve/n128/b1` | 0.107972 ± 0.000575959 (W 0.00129392) | 0.141705 ± 0.00313231 (W 0.00471401) | 🔵 tlinalg 1.31× faster than `tlinalg-pool` | `!` between-start range over 5% |
| `lu_solve_prepared/n128/b1` | 0.010019 ± 0.000732958 (W 7.42474e-05) | 0.010074 ± 6.85584e-05 (W 0.000110411) | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.11276 ± 0.000260124 (W 0.00200495) | 0.150114 ± 0.00334452 (W 0.0036688) | 🔵 tlinalg 1.33× faster than `tlinalg-pool` |  |
| `svd_values/n128/b1` | 2.35198 ± 0.00639605 (W 0.00449141) | 2.38239 ± 0.00141108 (W 0.00275772) | · |  |
| `triangular_solve/n128/b1` | 0.006813 ± 0.000255522 (W 7.38819e-05) | 0.006863 ± 3.17844e-05 (W 6.4512e-05) | · | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.181534 ± 0.000665268 (W 0.00147161) | 0.187545 ± 0.000594098 (W 0.00238517) | · |  |
| `lu/n128/b1` | 0.337085 ± 0.000661718 (W 0.00292696) | 0.349498 ± 0.00646593 (W 0.00453939) | · |  |
| `lu_factor/n128/b1` | 0.267319 ± 0.000347305 (W 0.00164797) | 0.265446 ± 0.00243161 (W 0.00323515) | · |  |
| `lu_factor_solve/n128/b1` | 0.297982 ± 0.000583382 (W 0.00171045) | 0.295267 ± 0.00114145 (W 0.00184174) | · |  |
| `lu_solve_prepared/n128/b1` | 0.0313785 ± 0.000111447 (W 9.03075e-05) | 0.0312735 ± 6.31955e-05 (W 0.000130946) | · |  |
| `solve/n128/b1` | 0.312854 ± 0.00109669 (W 0.00230748) | 0.325874 ± 0.00395815 (W 0.00543174) | · |  |
| `svd_values/n128/b1` | 3.12306 ± 0.0110849 (W 0.0040142) | 3.15707 ± 0.00476407 (W 0.00828921) | · |  |
| `triangular_solve/n128/b1` | 0.0187095 ± 0.000114587 (W 0.00166838) | 0.01871 ± 2.62996e-05 (W 8.2566e-05) | · | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 47.571 ± 0.330591 (W 0.0661172) | 23.5164 ± 0.0549676 (W 0.160418) | 🔴 tlinalg 2.02× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 23.4152 ± 0.0950916 (W 0.0224686) | 18.6965 ± 0.0166135 (W 0.0308378) | 🔴 tlinalg 1.25× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 10.364 ± 0.0938748 (W 0.0259497) | 2.87847 ± 0.0230137 (W 0.0580087) | 🔴 tlinalg 3.60× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 7.27317 ± 0.0340094 (W 0.00870022) | 2.7284 ± 0.00779464 (W 0.028431) | 🔴 tlinalg 2.67× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 19.3234 ± 0.0322573 (W 0.0286019) | 7.84775 ± 0.0724515 (W 0.103909) | 🔴 tlinalg 2.46× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 24.9783 ± 0.131827 (W 0.029959) | 9.58758 ± 0.064784 (W 0.0973609) | 🔴 tlinalg 2.61× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 117.524 ± 0.526833 (W 0.265504) | 60.9109 ± 0.338062 (W 0.163603) | 🔴 tlinalg 1.93× slower than `tlinalg-pool` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 104.684 ± 0.132948 (W 0.0511411) | 38.4885 ± 0.325629 (W 0.434787) | 🔴 tlinalg 2.72× slower than `tlinalg-pool` |  |
| `eigvalsh/n512/b1` | 49.0995 ± 0.195234 (W 0.0402031) | 28.9936 ± 0.0380791 (W 0.0547546) | 🔴 tlinalg 1.69× slower than `tlinalg-pool` |  |
| `householder_apply/n512/b1` | 40.2451 ± 0.705133 (W 0.0722686) | 6.93318 ± 0.0668894 (W 0.0845323) | 🔴 tlinalg 5.80× slower than `tlinalg-pool` |  |
| `householder_factor/n512/b1` | 27.8182 ± 0.101566 (W 0.0333276) | 6.9167 ± 0.0536598 (W 0.0751004) | 🔴 tlinalg 4.02× slower than `tlinalg-pool` |  |
| `qr/n512/b1` | 70.5827 ± 0.0822653 (W 0.0522573) | 16.9952 ± 0.103489 (W 0.13301) | 🔴 tlinalg 4.15× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/n512/b1` | 82.9728 ± 0.199108 (W 0.110781) | 19.658 ± 0.0367719 (W 0.0904744) | 🔴 tlinalg 4.22× slower than `tlinalg-pool` |  |
| `svd_thin/n512/b1` | 262.011 ± 0.468779 (W 0.596847) | 99.8145 ± 0.417873 (W 0.722856) | 🔴 tlinalg 2.62× slower than `tlinalg-pool` |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 22.9403 ± 0.0987247 (W 0.0271115) | 7.87972 ± 0.0376324 (W 0.0617386) | 🔴 tlinalg 2.91× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 66.5681 ± 0.137537 (W 0.0883552) | 22.4082 ± 0.239769 (W 0.424604) | 🔴 tlinalg 2.97× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 102.115 ± 0.417069 (W 0.328844) | 24.7742 ± 0.303392 (W 0.601281) | 🔴 tlinalg 4.12× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 102.954 ± 0.0774752 (W 0.229709) | 39.9307 ± 0.197276 (W 0.414677) | 🔴 tlinalg 2.58× slower than `tlinalg-pool` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-1lane (ms) | tlinalg-pool (ms) | vs `tlinalg-pool` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 85.4246 ± 0.424524 (W 0.283538) | 19.9318 ± 0.0333668 (W 0.0266502) | 🔴 tlinalg 4.29× slower than `tlinalg-pool` |  |
| `qr/4096x256/b1` | 236.201 ± 0.115147 (W 0.276553) | 53.2205 ± 0.141664 (W 0.139337) | 🔴 tlinalg 4.44× slower than `tlinalg-pool` |  |
| `rank_revealing_qr/4096x256/b1` | 342.994 ± 2.47961 (W 0.805488) | 60.8009 ± 0.0347327 (W 0.202562) | 🔴 tlinalg 5.64× slower than `tlinalg-pool` |  |
| `svd_thin/4096x256/b1` | 366.344 ± 0.660298 (W 0.6172) | 112.011 ± 0.486142 (W 0.395234) | 🔴 tlinalg 3.27× slower than `tlinalg-pool` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
