# `tlinalg-competition` on `zen5-cpu`

- tlinalg-rs commit: `4dcd35f080a6b4fd6b1423871af66a33fd398482`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `faer` 0.24.4 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.6 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer-traits` 0.24.0 (linked dependency of the measured provider; source registry+https://github.com/rust-lang/crates.io-index)
- harness commit: `817b3e8e11c932bee2c86cd89e0e6130287ee586`
- toolkit commit: `b30708eaa5b5f288c9d4ec8ff9c0bda2389125d3`
- measured binary SHA-256: `dce21ac38e7150502f3291d58bb393080b1e1f363df08a2caf08052ff5e09987`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T19:00:38.050596Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-competition --vendor openblas --aa 4 --reps 5 --prime-ms 250 --label pub-openblas-corefixed`
- raw data: `data/results/zen5-cpu/tlinalg-competition/20261020T183038Z-pub-openblas-corefixed/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.70%, worst 106.67% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 84 of 396 engine cells exceed 5% and carry `!`; median within-process relative SD 0.44%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.114013 ± 0.00137894 (W 0.00180289) | 1.03086 ± 0.396971 (W 0.00210431) | 🔵 tlinalg 9.04× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `cholesky/n32/b1024` | 0.428276 ± 0.00296578 (W 0.00583484) | 3.67068 ± 0.0295992 (W 0.00718008) | 🔵 tlinalg 8.57× faster than `lapack-openblas` |  |
| `cholesky/n4/b1024` | 0.0299815 ± 0.0046906 (W 0.000992047) | 0.197239 ± 0.00128434 (W 0.00151433) | 🔵 tlinalg 6.58× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `cholesky/n8/b1024` | 0.0527985 ± 0.000312541 (W 0.000424114) | 0.390842 ± 0.00629782 (W 0.00239212) | 🔵 tlinalg 7.40× faster than `lapack-openblas` |  |
| `eig/n16/b1024` | 11.8796 ± 0.02929 (W 0.0242826) | 69.0092 ± 0.520932 (W 0.0793014) | 🔵 tlinalg 5.81× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 53.3026 ± 1.97892 (W 0.633898) | 324.264 ± 0.944573 (W 0.526396) | 🔵 tlinalg 6.08× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eig/n4/b1024` | 0.786482 ± 0.00577498 (W 0.00203535) | 5.36275 ± 0.0363158 (W 0.00861698) | 🔵 tlinalg 6.82× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 2.95819 ± 0.00381954 (W 0.00607215) | 17.5112 ± 0.0388151 (W 0.0331013) | 🔵 tlinalg 5.92× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 3.75649 ± 0.00919627 (W 0.00594213) | 40.4155 ± 0.336466 (W 0.0442196) | 🔵 tlinalg 10.76× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 14.4109 ± 0.299952 (W 0.0503679) | 119.088 ± 0.730433 (W 0.297502) | 🔵 tlinalg 8.26× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 0.313926 ± 0.00281245 (W 0.00160513) | 3.02856 ± 0.0166907 (W 0.00629503) | 🔵 tlinalg 9.65× faster than `lapack-openblas` |  |
| `eigh/n8/b1024` | 1.07769 ± 0.00794658 (W 0.00308622) | 10.8526 ± 0.023363 (W 0.0199779) | 🔵 tlinalg 10.07× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 8.21531 ± 0.0341403 (W 0.0320197) | 49.6174 ± 0.220314 (W 0.0470294) | 🔵 tlinalg 6.04× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 36.2867 ± 0.0673943 (W 0.0412926) | 218.246 ± 1.50518 (W 0.664291) | 🔵 tlinalg 6.01× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.414184 ± 0.0101991 (W 0.00285983) | 3.39492 ± 0.00638276 (W 0.0100707) | 🔵 tlinalg 8.20× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eigvals/n8/b1024` | 1.93992 ± 0.0195387 (W 0.0050936) | 13.2285 ± 0.0205827 (W 0.0172476) | 🔵 tlinalg 6.82× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 2.80272 ± 0.0113614 (W 0.00604842) | 14.5783 ± 0.0211683 (W 0.0190993) | 🔵 tlinalg 5.20× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 10.9364 ± 0.0139394 (W 0.0456235) | 50.2066 ± 0.0569314 (W 0.0313319) | 🔵 tlinalg 4.59× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.25408 ± 0.00233577 (W 0.00171765) | 1.40364 ± 0.0100715 (W 0.00547328) | 🔵 tlinalg 5.52× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.859099 ± 0.00438704 (W 0.00206387) | 4.55921 ± 0.0156754 (W 0.0045994) | 🔵 tlinalg 5.31× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.458626 ± 0.00210503 (W 0.00367571) | 4.70267 ± 0.109874 (W 0.0327222) | 🔵 tlinalg 10.25× faster than `lapack-openblas` |  |
| `full_piv_lu/n32/b1024` | 2.02988 ± 0.386092 (W 0.0626466) | 28.7661 ± 0.855986 (W 0.268266) | 🔵 tlinalg 14.17× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `full_piv_lu/n4/b1024` | 0.08562 ± 0.00176917 (W 0.00227666) | 0.362813 ± 0.0209345 (W 0.002003) | 🔵 tlinalg 4.24× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.170755 ± 0.00191589 (W 0.00352671) | 1.03613 ± 0.0288043 (W 0.00396397) | 🔵 tlinalg 6.07× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 0.440162 ± 0.0048931 (W 0.00314707) | 6.54438 ± 0.0766345 (W 0.0225205) | 🔵 tlinalg 14.87× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 1.48402 ± 0.0234438 (W 0.01468) | 31.3623 ± 0.113879 (W 0.217989) | 🔵 tlinalg 21.13× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.0748345 ± 0.00342249 (W 0.00353063) | 0.947234 ± 0.00283657 (W 0.00226179) | 🔵 tlinalg 12.66× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.165053 ± 0.00362107 (W 0.00270673) | 2.00375 ± 0.00431416 (W 0.0043334) | 🔵 tlinalg 12.14× faster than `lapack-openblas` |  |
| `householder_apply/n16/b1024` | 0.603914 ± 0.0145007 (W 0.00206329) | 4.53172 ± 0.0391948 (W 0.0225201) | 🔵 tlinalg 7.50× faster than `lapack-openblas` |  |
| `householder_apply/n32/b1024` | 2.45922 ± 0.0654619 (W 0.00997565) | 19.0205 ± 0.277388 (W 0.0569565) | 🔵 tlinalg 7.73× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n4/b1024` | 0.052809 ± 0.0238579 (W 0.000836941) | 0.41799 ± 0.000968785 (W 0.00210265) | 🔵 tlinalg 7.92× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `householder_apply/n8/b1024` | 0.168339 ± 0.00353626 (W 0.00178244) | 1.21052 ± 0.0037573 (W 0.00274804) | 🔵 tlinalg 7.19× faster than `lapack-openblas` |  |
| `householder_factor/n16/b1024` | 0.492817 ± 0.0749994 (W 0.00451587) | 4.37114 ± 0.0107916 (W 0.00782097) | 🔵 tlinalg 8.87× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `householder_factor/n32/b1024` | 1.6337 ± 0.00896215 (W 0.0111518) | 14.7242 ± 0.402435 (W 0.037056) | 🔵 tlinalg 9.01× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n4/b1024` | 0.063929 ± 0.000441105 (W 0.000648369) | 0.537723 ± 0.00143767 (W 0.00199268) | 🔵 tlinalg 8.41× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.164834 ± 0.0011015 (W 0.00166876) | 1.50687 ± 0.00841654 (W 0.00403588) | 🔵 tlinalg 9.14× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.36612 ± 0.0115324 (W 0.00356228) | 2.36837 ± 0.0494122 (W 0.0104245) | 🔵 tlinalg 6.47× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n32/b1024` | 1.31827 ± 0.02926 (W 0.0275567) | 9.64593 ± 0.034258 (W 0.0632078) | 🔵 tlinalg 7.32× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n4/b1024` | 0.0716485 ± 0.00185446 (W 0.00194333) | 0.329105 ± 0.00259409 (W 0.00192127) | 🔵 tlinalg 4.59× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n8/b1024` | 0.143363 ± 0.00272641 (W 0.00248077) | 0.802662 ± 0.00408225 (W 0.00315308) | 🔵 tlinalg 5.60× faster than `lapack-openblas` |  |
| `lu_factor/n16/b1024` | 0.267977 ± 0.1178 (W 0.00329673) | 1.8119 ± 0.0286584 (W 0.00257533) | 🔵 tlinalg 6.76× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_factor/n32/b1024` | 0.756586 ± 0.00617782 (W 0.00197991) | 6.7539 ± 0.0435793 (W 0.0153262) | 🔵 tlinalg 8.93× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.0638695 ± 0.000699583 (W 0.0019649) | 0.222246 ± 0.0184214 (W 0.00228406) | 🔵 tlinalg 3.48× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n8/b1024` | 0.112947 ± 0.000220322 (W 0.00186791) | 0.569299 ± 0.00102102 (W 0.00302417) | 🔵 tlinalg 5.04× faster than `lapack-openblas` |  |
| `lu_factor_solve/n16/b1024` | 0.343666 ± 0.00990042 (W 0.00477453) | 3.57961 ± 0.206506 (W 0.00865259) | 🔵 tlinalg 10.42× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n32/b1024` | 0.910732 ± 0.0109809 (W 0.00559059) | 9.72477 ± 0.150397 (W 0.0123577) | 🔵 tlinalg 10.68× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.064315 ± 0.00205333 (W 0.00145915) | 1.16699 ± 0.0380646 (W 0.00463665) | 🔵 tlinalg 18.14× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.130799 ± 0.00470993 (W 0.00161361) | 1.74831 ± 0.26849 (W 0.010855) | 🔵 tlinalg 13.37× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n16/b1024` | 0.105933 ± 0.000257152 (W 0.000881017) | 1.36753 ± 0.233537 (W 0.00790662) | 🔵 tlinalg 12.91× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n32/b1024` | 0.311361 ± 0.00860341 (W 0.0177477) | 2.21633 ± 0.0816894 (W 0.00515781) | 🔵 tlinalg 7.12× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.033337 ± 0.000773019 (W 0.000793613) | 0.839396 ± 0.0297006 (W 0.00734296) | 🔵 tlinalg 25.18× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.0556135 ± 0.00155589 (W 0.000881917) | 1.02744 ± 0.273124 (W 0.00925467) | 🔵 tlinalg 18.47× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `qr/n16/b1024` | 1.12821 ± 0.0125196 (W 0.0024335) | 7.86965 ± 0.062679 (W 0.0167366) | 🔵 tlinalg 6.98× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 4.5408 ± 0.00759228 (W 0.0222397) | 27.3997 ± 0.173552 (W 0.0475342) | 🔵 tlinalg 6.03× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.099676 ± 0.00023083 (W 0.000844724) | 0.964805 ± 0.00144089 (W 0.00202545) | 🔵 tlinalg 9.68× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 0.312143 ± 0.163618 (W 0.00270113) | 2.66858 ± 0.0349439 (W 0.00870985) | 🔵 tlinalg 8.55× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `rank_revealing_qr/n16/b1024` | 1.32198 ± 0.0888906 (W 0.0028143) | 9.42815 ± 0.1857 (W 0.0280232) | 🔵 tlinalg 7.13× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `rank_revealing_qr/n32/b1024` | 4.5677 ± 0.0252182 (W 0.0369771) | 33.9171 ± 0.16101 (W 0.0880156) | 🔵 tlinalg 7.43× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n4/b1024` | 0.153932 ± 0.000936744 (W 0.00135299) | 1.16522 ± 0.00285309 (W 0.0033963) | 🔵 tlinalg 7.57× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.4117 ± 0.00753713 (W 0.00207449) | 3.06162 ± 0.0181944 (W 0.00529716) | 🔵 tlinalg 7.44× faster than `lapack-openblas` |  |
| `solve/n16/b1024` | 0.352934 ± 0.00466674 (W 0.00208123) | 3.71063 ± 0.245713 (W 0.0110674) | 🔵 tlinalg 10.51× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n32/b1024` | 0.953971 ± 0.0197124 (W 0.0117132) | 9.85251 ± 0.130554 (W 0.0151855) | 🔵 tlinalg 10.33× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.0542265 ± 0.000753694 (W 0.0010221) | 1.35134 ± 0.0188282 (W 0.00433961) | 🔵 tlinalg 24.92× faster than `lapack-openblas` |  |
| `solve/n8/b1024` | 0.129142 ± 0.000823399 (W 0.0060238) | 2.0483 ± 0.0430417 (W 0.00370634) | 🔵 tlinalg 15.86× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 7.42299 ± 0.407255 (W 0.0152445) | 81.0115 ± 0.189634 (W 0.252922) | 🔵 tlinalg 10.91× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 25.9403 ± 0.407044 (W 0.0630652) | 238.306 ± 1.41992 (W 0.354419) | 🔵 tlinalg 9.19× faster than `lapack-openblas` |  |
| `svd_full/n4/b1024` | 0.544152 ± 0.0026785 (W 0.0044516) | 6.32192 ± 0.0205514 (W 0.0119216) | 🔵 tlinalg 11.62× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 1.93987 ± 0.0862479 (W 0.0340198) | 21.2531 ± 0.0430521 (W 0.0406609) | 🔵 tlinalg 10.96× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.17199 ± 0.106423 (W 0.130466) | 80.7471 ± 0.439779 (W 0.33974) | 🔵 tlinalg 11.26× faster than `lapack-openblas` |  |
| `svd_thin/n32/b1024` | 27.9037 ± 1.20523 (W 0.146132) | 238.811 ± 0.909317 (W 0.9686) | 🔵 tlinalg 8.56× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.546057 ± 0.00179162 (W 0.00701734) | 6.34506 ± 0.0346932 (W 0.0157163) | 🔵 tlinalg 11.62× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1024` | 1.91697 ± 0.0508149 (W 0.0212547) | 21.3123 ± 0.120726 (W 0.0307283) | 🔵 tlinalg 11.12× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_values/n16/b1024` | 5.13764 ± 0.0156723 (W 0.00612517) | 25.1313 ± 0.168746 (W 0.0416756) | 🔵 tlinalg 4.89× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 20.1428 ± 0.0992101 (W 0.0358681) | 79.6873 ± 0.64862 (W 0.0775857) | 🔵 tlinalg 3.96× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.410388 ± 0.00206496 (W 0.00200236) | 3.44662 ± 0.0120687 (W 0.00414201) | 🔵 tlinalg 8.40× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.43741 ± 0.0191923 (W 0.00389797) | 8.93888 ± 0.0279815 (W 0.015362) | 🔵 tlinalg 6.22× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.084317 ± 0.000841055 (W 0.00316438) | 1.08434 ± 0.109825 (W 0.00582423) | 🔵 tlinalg 12.86× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n32/b1024` | 0.205809 ± 0.0169421 (W 0.00653264) | 1.53271 ± 0.0483292 (W 0.00728908) | 🔵 tlinalg 7.45× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n4/b1024` | 0.020784 ± 0.00275148 (W 0.000751476) | 0.749399 ± 0.0626967 (W 0.00384918) | 🔵 tlinalg 36.06× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.0349705 ± 0.000438961 (W 0.000540285) | 0.882232 ± 0.0425801 (W 0.00376005) | 🔵 tlinalg 25.23× faster than `lapack-openblas` | `!` between-start range over 5% |

## batch-small, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n16/b1024` | 0.172613 ± 0.00163386 (W 0.00271808) | 1.61566 ± 0.0437038 (W 0.00678215) | 🔵 tlinalg 9.36× faster than `lapack-openblas` | `!` between-start range over 5% |
| `cholesky/n32/b1024` | 0.822817 ± 0.0388665 (W 0.00801672) | 6.37083 ± 0.00859705 (W 0.0071406) | 🔵 tlinalg 7.74× faster than `lapack-openblas` | `!` between-start range over 5% |
| `cholesky/n4/b1024` | 0.032235 ± 0.000539727 (W 0.000529758) | 0.232459 ± 0.00162113 (W 0.00140669) | 🔵 tlinalg 7.21× faster than `lapack-openblas` |  |
| `cholesky/n8/b1024` | 0.061019 ± 0.00150283 (W 0.000386217) | 0.498322 ± 0.01504 (W 0.00233742) | 🔵 tlinalg 8.17× faster than `lapack-openblas` | `!` between-start range over 5% |
| `eig/n16/b1024` | 16.4234 ± 0.0427607 (W 0.0399982) | 198.988 ± 0.650485 (W 0.364182) | 🔵 tlinalg 12.12× faster than `lapack-openblas` |  |
| `eig/n32/b1024` | 67.2382 ± 0.0687037 (W 0.0303204) | 886.777 ± 1.00318 (W 0.393702) | 🔵 tlinalg 13.19× faster than `lapack-openblas` |  |
| `eig/n4/b1024` | 1.29051 ± 0.0118615 (W 0.0108906) | 13.2532 ± 0.0377922 (W 0.0385004) | 🔵 tlinalg 10.27× faster than `lapack-openblas` |  |
| `eig/n8/b1024` | 4.46854 ± 0.0183192 (W 0.0173177) | 46.6002 ± 0.359382 (W 0.0771498) | 🔵 tlinalg 10.43× faster than `lapack-openblas` |  |
| `eigh/n16/b1024` | 4.01947 ± 0.00858745 (W 0.00495748) | 45.2356 ± 0.163908 (W 0.0926548) | 🔵 tlinalg 11.25× faster than `lapack-openblas` |  |
| `eigh/n32/b1024` | 17.9039 ± 0.031762 (W 0.0274534) | 187.539 ± 0.615919 (W 0.242937) | 🔵 tlinalg 10.47× faster than `lapack-openblas` |  |
| `eigh/n4/b1024` | 0.380301 ± 0.0570137 (W 0.00157046) | 3.58742 ± 0.0106668 (W 0.00434774) | 🔵 tlinalg 9.43× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `eigh/n8/b1024` | 1.15338 ± 0.00375158 (W 0.00197712) | 12.3931 ± 0.105284 (W 0.0165128) | 🔵 tlinalg 10.75× faster than `lapack-openblas` |  |
| `eigvals/n16/b1024` | 9.68117 ± 0.031304 (W 0.0105272) | 149.162 ± 0.620377 (W 0.208299) | 🔵 tlinalg 15.41× faster than `lapack-openblas` |  |
| `eigvals/n32/b1024` | 42.4545 ± 0.164689 (W 0.142495) | 599.572 ± 0.960014 (W 0.682618) | 🔵 tlinalg 14.12× faster than `lapack-openblas` |  |
| `eigvals/n4/b1024` | 0.626835 ± 0.00354899 (W 0.0042935) | 10.0295 ± 0.0188524 (W 0.0208333) | 🔵 tlinalg 16.00× faster than `lapack-openblas` |  |
| `eigvals/n8/b1024` | 2.51063 ± 0.0021953 (W 0.00455518) | 36.9907 ± 0.0244126 (W 0.0558515) | 🔵 tlinalg 14.73× faster than `lapack-openblas` |  |
| `eigvalsh/n16/b1024` | 3.00717 ± 0.00849306 (W 0.0071106) | 19.3107 ± 0.0318797 (W 0.0500713) | 🔵 tlinalg 6.42× faster than `lapack-openblas` |  |
| `eigvalsh/n32/b1024` | 11.8551 ± 0.0129255 (W 0.0459601) | 73.0087 ± 0.167492 (W 0.0936851) | 🔵 tlinalg 6.16× faster than `lapack-openblas` |  |
| `eigvalsh/n4/b1024` | 0.309313 ± 0.000507454 (W 0.00214657) | 2.1057 ± 0.00581206 (W 0.00370838) | 🔵 tlinalg 6.81× faster than `lapack-openblas` |  |
| `eigvalsh/n8/b1024` | 0.925642 ± 0.00460348 (W 0.00227389) | 6.17183 ± 0.0192864 (W 0.0145016) | 🔵 tlinalg 6.67× faster than `lapack-openblas` |  |
| `full_piv_lu/n16/b1024` | 0.628623 ± 0.00774172 (W 0.00825791) | 33.3899 ± 0.0685432 (W 0.0873108) | 🔵 tlinalg 53.12× faster than `lapack-openblas` |  |
| `full_piv_lu/n32/b1024` | 3.0551 ± 0.0312934 (W 0.0235906) | 201.759 ± 1.24603 (W 1.4497) | 🔵 tlinalg 66.04× faster than `lapack-openblas` |  |
| `full_piv_lu/n4/b1024` | 0.08825 ± 0.00264845 (W 0.00184992) | 0.906719 ± 0.0286644 (W 0.00289831) | 🔵 tlinalg 10.27× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu/n8/b1024` | 0.200043 ± 0.00772681 (W 0.00405419) | 3.92352 ± 0.0843634 (W 0.0100794) | 🔵 tlinalg 19.61× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n16/b1024` | 0.706839 ± 0.00449727 (W 0.00563542) | 37.8766 ± 0.167387 (W 0.0420825) | 🔵 tlinalg 53.59× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n32/b1024` | 2.67704 ± 0.0176514 (W 0.012831) | 211.557 ± 1.27952 (W 0.319527) | 🔵 tlinalg 79.03× faster than `lapack-openblas` |  |
| `full_piv_lu_solve/n4/b1024` | 0.116398 ± 0.00528053 (W 0.0021543) | 2.14216 ± 0.0115132 (W 0.00694872) | 🔵 tlinalg 18.40× faster than `lapack-openblas` | `!` between-start range over 5% |
| `full_piv_lu_solve/n8/b1024` | 0.279006 ± 0.0569182 (W 0.00247743) | 6.13752 ± 0.0486728 (W 0.0118665) | 🔵 tlinalg 22.00× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `householder_apply/n16/b1024` | 0.621229 ± 0.0142742 (W 0.00968236) | 7.09994 ± 0.184628 (W 0.0269534) | 🔵 tlinalg 11.43× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n32/b1024` | 3.56848 ± 0.0779788 (W 0.0178369) | 36.0122 ± 0.381408 (W 0.0721041) | 🔵 tlinalg 10.09× faster than `lapack-openblas` |  |
| `householder_apply/n4/b1024` | 0.049653 ± 0.0031643 (W 0.00098818) | 0.441435 ± 0.00116111 (W 0.00280425) | 🔵 tlinalg 8.89× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_apply/n8/b1024` | 0.161061 ± 0.0117862 (W 0.00532574) | 1.49047 ± 0.00730228 (W 0.00336697) | 🔵 tlinalg 9.25× faster than `lapack-openblas` | `!` between-start range over 5% |
| `householder_factor/n16/b1024` | 0.575476 ± 0.00539725 (W 0.00385144) | 7.38155 ± 0.0282787 (W 0.0176688) | 🔵 tlinalg 12.83× faster than `lapack-openblas` |  |
| `householder_factor/n32/b1024` | 2.63168 ± 0.0388916 (W 0.0416234) | 27.1298 ± 0.1888 (W 0.0318975) | 🔵 tlinalg 10.31× faster than `lapack-openblas` |  |
| `householder_factor/n4/b1024` | 0.075456 ± 0.000501121 (W 0.000577728) | 0.924272 ± 0.00593815 (W 0.0016966) | 🔵 tlinalg 12.25× faster than `lapack-openblas` |  |
| `householder_factor/n8/b1024` | 0.192549 ± 0.00143758 (W 0.00181665) | 2.3766 ± 0.0110249 (W 0.00670962) | 🔵 tlinalg 12.34× faster than `lapack-openblas` |  |
| `lu/n16/b1024` | 0.432979 ± 0.00562674 (W 0.00685623) | 3.98662 ± 0.0567853 (W 0.00983231) | 🔵 tlinalg 9.21× faster than `lapack-openblas` |  |
| `lu/n32/b1024` | 2.12432 ± 0.0246833 (W 0.0177218) | 15.4428 ± 0.145575 (W 0.0262942) | 🔵 tlinalg 7.27× faster than `lapack-openblas` |  |
| `lu/n4/b1024` | 0.070557 ± 0.00121861 (W 0.00146337) | 0.382379 ± 0.00260219 (W 0.00258645) | 🔵 tlinalg 5.42× faster than `lapack-openblas` |  |
| `lu/n8/b1024` | 0.149985 ± 0.00154069 (W 0.00342833) | 1.05255 ± 0.0134039 (W 0.00266987) | 🔵 tlinalg 7.02× faster than `lapack-openblas` |  |
| `lu_factor/n16/b1024` | 0.295186 ± 0.0182973 (W 0.00759162) | 2.71974 ± 0.0159372 (W 0.00581023) | 🔵 tlinalg 9.21× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor/n32/b1024` | 1.32229 ± 0.0258548 (W 0.0174975) | 11.3386 ± 0.169502 (W 0.0223366) | 🔵 tlinalg 8.57× faster than `lapack-openblas` |  |
| `lu_factor/n4/b1024` | 0.067411 ± 0.000383415 (W 0.00138786) | 0.271418 ± 0.00181876 (W 0.00185564) | 🔵 tlinalg 4.03× faster than `lapack-openblas` |  |
| `lu_factor/n8/b1024` | 0.117985 ± 0.0138991 (W 0.00161758) | 0.759049 ± 0.00183941 (W 0.00303478) | 🔵 tlinalg 6.43× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n16/b1024` | 0.456869 ± 0.00506595 (W 0.00378305) | 5.11843 ± 0.0586761 (W 0.019864) | 🔵 tlinalg 11.20× faster than `lapack-openblas` |  |
| `lu_factor_solve/n32/b1024` | 1.75546 ± 0.0200154 (W 0.0333742) | 15.5752 ± 0.27609 (W 0.0158843) | 🔵 tlinalg 8.87× faster than `lapack-openblas` |  |
| `lu_factor_solve/n4/b1024` | 0.080911 ± 0.000810398 (W 0.00110093) | 1.40062 ± 0.0395304 (W 0.0049225) | 🔵 tlinalg 17.31× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_factor_solve/n8/b1024` | 0.16555 ± 0.0683428 (W 0.00227442) | 2.20147 ± 0.164157 (W 0.00511664) | 🔵 tlinalg 13.30× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `lu_solve_prepared/n16/b1024` | 0.19572 ± 0.0189682 (W 0.00352107) | 1.97275 ± 0.0165671 (W 0.00849174) | 🔵 tlinalg 10.08× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n32/b1024` | 0.884143 ± 0.0216936 (W 0.00869384) | 3.90134 ± 0.0412984 (W 0.0111773) | 🔵 tlinalg 4.41× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n4/b1024` | 0.0447585 ± 0.000346288 (W 0.00121656) | 1.03755 ± 0.0374376 (W 0.00516968) | 🔵 tlinalg 23.18× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu_solve_prepared/n8/b1024` | 0.087363 ± 0.00106372 (W 0.000902096) | 1.2164 ± 0.152874 (W 0.00248359) | 🔵 tlinalg 13.92× faster than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n16/b1024` | 1.39947 ± 0.0033504 (W 0.00511432) | 12.5603 ± 0.0431006 (W 0.0297604) | 🔵 tlinalg 8.98× faster than `lapack-openblas` |  |
| `qr/n32/b1024` | 9.41301 ± 0.0234656 (W 0.0347283) | 49.5516 ± 0.292016 (W 0.064714) | 🔵 tlinalg 5.26× faster than `lapack-openblas` |  |
| `qr/n4/b1024` | 0.114249 ± 0.00126011 (W 0.00141198) | 1.37963 ± 0.00344576 (W 0.00300589) | 🔵 tlinalg 12.08× faster than `lapack-openblas` |  |
| `qr/n8/b1024` | 0.335957 ± 0.000620989 (W 0.00196992) | 3.74028 ± 0.0112216 (W 0.006076) | 🔵 tlinalg 11.13× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n16/b1024` | 1.56728 ± 0.013733 (W 0.00587322) | 16.6501 ± 0.044163 (W 0.0259538) | 🔵 tlinalg 10.62× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n32/b1024` | 8.72147 ± 1.31232 (W 0.0826752) | 65.6304 ± 0.230549 (W 0.0871364) | 🔵 tlinalg 7.53× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `rank_revealing_qr/n4/b1024` | 0.183537 ± 0.000960837 (W 0.00172398) | 1.77411 ± 0.0130734 (W 0.00438807) | 🔵 tlinalg 9.67× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n8/b1024` | 0.472859 ± 0.016882 (W 0.00208419) | 4.91663 ± 0.0182032 (W 0.0100596) | 🔵 tlinalg 10.40× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n16/b1024` | 0.508539 ± 0.00741731 (W 0.0123776) | 5.15597 ± 0.197197 (W 0.0190523) | 🔵 tlinalg 10.14× faster than `lapack-openblas` | `!` between-start range over 5% |
| `solve/n32/b1024` | 1.84572 ± 0.0203152 (W 0.00847055) | 16.0648 ± 0.210122 (W 0.0144144) | 🔵 tlinalg 8.70× faster than `lapack-openblas` |  |
| `solve/n4/b1024` | 0.0765125 ± 0.00110691 (W 0.00263016) | 1.47565 ± 0.171204 (W 0.00588362) | 🔵 tlinalg 19.29× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `solve/n8/b1024` | 0.186287 ± 0.00370951 (W 0.00165544) | 2.36366 ± 0.157112 (W 0.0032374) | 🔵 tlinalg 12.69× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n16/b1024` | 7.75212 ± 0.275074 (W 0.0844928) | 93.7184 ± 0.139146 (W 0.0647117) | 🔵 tlinalg 12.09× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n32/b1024` | 34.5236 ± 1.5545 (W 0.788951) | 296.788 ± 1.00723 (W 0.507046) | 🔵 tlinalg 8.60× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_full/n4/b1024` | 0.637073 ± 0.00127364 (W 0.00267627) | 7.9199 ± 0.0500496 (W 0.0128364) | 🔵 tlinalg 12.43× faster than `lapack-openblas` |  |
| `svd_full/n8/b1024` | 2.16674 ± 0.0757461 (W 0.0537403) | 25.1488 ± 0.141991 (W 0.0231398) | 🔵 tlinalg 11.61× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n16/b1024` | 7.76759 ± 0.07083 (W 0.0488894) | 93.9546 ± 0.354904 (W 0.296305) | 🔵 tlinalg 12.10× faster than `lapack-openblas` |  |
| `svd_thin/n32/b1024` | 34.6575 ± 1.60891 (W 0.32377) | 296.758 ± 1.55635 (W 0.422526) | 🔵 tlinalg 8.56× faster than `lapack-openblas` | `!` between-start range over 5% |
| `svd_thin/n4/b1024` | 0.645722 ± 0.0104946 (W 0.00255229) | 7.92581 ± 0.0137568 (W 0.0147519) | 🔵 tlinalg 12.27× faster than `lapack-openblas` |  |
| `svd_thin/n8/b1024` | 2.16798 ± 0.0391072 (W 0.0374402) | 24.96 ± 0.178769 (W 0.0294621) | 🔵 tlinalg 11.51× faster than `lapack-openblas` |  |
| `svd_values/n16/b1024` | 5.86249 ± 0.0470878 (W 0.0267828) | 33.4194 ± 0.0681238 (W 0.0414114) | 🔵 tlinalg 5.70× faster than `lapack-openblas` |  |
| `svd_values/n32/b1024` | 22.3545 ± 0.0631473 (W 0.131033) | 110.463 ± 0.195405 (W 0.166232) | 🔵 tlinalg 4.94× faster than `lapack-openblas` |  |
| `svd_values/n4/b1024` | 0.496807 ± 0.00212269 (W 0.00167365) | 4.54826 ± 0.00964077 (W 0.0056216) | 🔵 tlinalg 9.15× faster than `lapack-openblas` |  |
| `svd_values/n8/b1024` | 1.64685 ± 0.0135313 (W 0.00483269) | 11.2404 ± 0.0389778 (W 0.0175071) | 🔵 tlinalg 6.83× faster than `lapack-openblas` |  |
| `triangular_solve/n16/b1024` | 0.144795 ± 0.0614267 (W 0.00410531) | 1.36192 ± 0.0753983 (W 0.00508851) | 🔵 tlinalg 9.41× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n32/b1024` | 0.534079 ± 0.0526721 (W 0.0112238) | 3.09951 ± 0.122402 (W 0.0125576) | 🔵 tlinalg 5.80× faster than `lapack-openblas` | `!` between-start range over 5%; `p` position effect over 5% |
| `triangular_solve/n4/b1024` | 0.028343 ± 0.000481197 (W 0.000853476) | 0.754563 ± 0.0727299 (W 0.00358742) | 🔵 tlinalg 26.62× faster than `lapack-openblas` | `!` between-start range over 5% |
| `triangular_solve/n8/b1024` | 0.065547 ± 0.00041511 (W 0.00109842) | 1.01691 ± 0.0554418 (W 0.00464818) | 🔵 tlinalg 15.51× faster than `lapack-openblas` | `!` between-start range over 5% |

## canary-factor, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.0655025 ± 0.00214799 (W 0.000704945) | 0.0777355 ± 0.00060756 (W 0.00102094) | 🔵 tlinalg 1.19× faster than `lapack-openblas` | `!` between-start range over 5% |
| `lu/n128/b1` | 0.184764 ± 0.0018791 (W 0.00405565) | 0.146139 ± 0.000275259 (W 0.00210002) | 🔴 tlinalg 1.26× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.129663 ± 0.00382243 (W 0.00498146) | 0.130499 ± 0.000365501 (W 0.00145194) | · | `!` between-start range over 5% |
| `lu_factor_solve/n128/b1` | 0.134586 ± 0.0021705 (W 0.00485527) | 0.146118 ± 0.000597041 (W 0.00125043) | 🔵 tlinalg 1.09× faster than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.009903 ± 4.13148e-05 (W 0.000127985) | 0.0121225 ± 0.000116076 (W 0.000125554) | 🔵 tlinalg 1.22× faster than `lapack-openblas` | dispatch-dominated (row under 20 us) |
| `solve/n128/b1` | 0.148147 ± 0.00320999 (W 0.00293233) | 0.154624 ± 0.000575504 (W 0.00109961) | · |  |
| `svd_values/n128/b1` | 2.37897 ± 0.00467959 (W 0.00335758) | 1.37847 ± 0.00437886 (W 0.00275707) | 🔴 tlinalg 1.73× slower than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.0067625 ± 6.69347e-05 (W 5.53367e-05) | 0.0067775 ± 8.67962e-05 (W 0.000186949) | · | dispatch-dominated (row under 20 us) |

## canary-factor, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `cholesky/n128/b1` | 0.187345 ± 0.000973791 (W 0.00208158) | 0.164152 ± 0.00130766 (W 0.00155686) | 🔴 tlinalg 1.14× slower than `lapack-openblas` |  |
| `lu/n128/b1` | 0.356035 ± 0.00337431 (W 0.00384996) | 0.237799 ± 0.00181954 (W 0.0027091) | 🔴 tlinalg 1.50× slower than `lapack-openblas` |  |
| `lu_factor/n128/b1` | 0.271502 ± 0.00181032 (W 0.00310908) | 0.190099 ± 0.00234732 (W 0.00203639) | 🔴 tlinalg 1.43× slower than `lapack-openblas` |  |
| `lu_factor_solve/n128/b1` | 0.299439 ± 0.00176552 (W 0.00260969) | 0.221934 ± 0.000770396 (W 0.00173213) | 🔴 tlinalg 1.35× slower than `lapack-openblas` |  |
| `lu_solve_prepared/n128/b1` | 0.0312935 ± 0.000121848 (W 0.000127835) | 0.0291795 ± 0.000136359 (W 0.00018085) | 🔴 tlinalg 1.07× slower than `lapack-openblas` |  |
| `solve/n128/b1` | 0.328063 ± 0.00426999 (W 0.0047647) | 0.242903 ± 0.000488008 (W 0.00255534) | 🔴 tlinalg 1.35× slower than `lapack-openblas` |  |
| `svd_values/n128/b1` | 3.14675 ± 0.00859905 (W 0.00875446) | 2.60483 ± 0.00324328 (W 0.00439927) | 🔴 tlinalg 1.21× slower than `lapack-openblas` |  |
| `triangular_solve/n128/b1` | 0.018725 ± 6.45497e-05 (W 0.000122175) | 0.0153135 ± 0.000178364 (W 0.00014582) | 🔴 tlinalg 1.22× slower than `lapack-openblas` | dispatch-dominated (row under 20 us) |

## canary-decompose, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 23.5542 ± 0.105105 (W 0.105037) | 23.4583 ± 0.0778266 (W 0.0600774) | · |  |
| `eigvalsh/n512/b1` | 18.7042 ± 0.0575184 (W 0.0211457) | 11.2348 ± 0.00706165 (W 0.00768317) | 🔴 tlinalg 1.66× slower than `lapack-openblas` |  |
| `householder_apply/n512/b1` | 2.86728 ± 0.0458374 (W 0.0577571) | 9.89995 ± 0.104697 (W 0.0236682) | 🔵 tlinalg 3.45× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 2.73316 ± 0.00813568 (W 0.0391458) | 6.78853 ± 0.0215687 (W 0.00965911) | 🔵 tlinalg 2.48× faster than `lapack-openblas` |  |
| `qr/n512/b1` | 7.68994 ± 0.055808 (W 0.108951) | 13.4764 ± 0.127907 (W 0.0139148) | 🔵 tlinalg 1.75× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 9.55947 ± 0.0761818 (W 0.104882) | 23.1913 ± 0.171338 (W 0.0419118) | 🔵 tlinalg 2.43× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 60.8953 ± 0.0528764 (W 0.107577) | 85.1764 ± 0.818956 (W 0.0819677) | 🔵 tlinalg 1.40× faster than `lapack-openblas` |  |

## canary-decompose, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `eigh/n512/b1` | 38.8685 ± 0.171927 (W 0.423891) | 204.264 ± 0.44243 (W 0.346546) | 🔵 tlinalg 5.26× faster than `lapack-openblas` |  |
| `eigvalsh/n512/b1` | 28.9399 ± 0.0372377 (W 0.0558823) | 29.8373 ± 0.0779838 (W 0.0202827) | · |  |
| `householder_apply/n512/b1` | 7.08357 ± 0.0689304 (W 0.0602982) | 14.8265 ± 0.0566596 (W 0.0368967) | 🔵 tlinalg 2.09× faster than `lapack-openblas` |  |
| `householder_factor/n512/b1` | 6.9061 ± 0.0583879 (W 0.126565) | 10.8785 ± 0.651895 (W 0.0142747) | 🔵 tlinalg 1.58× faster than `lapack-openblas` | `!` between-start range over 5% |
| `qr/n512/b1` | 16.9656 ± 0.170664 (W 0.238427) | 21.8073 ± 0.0423767 (W 0.0220397) | 🔵 tlinalg 1.29× faster than `lapack-openblas` |  |
| `rank_revealing_qr/n512/b1` | 19.5559 ± 0.0783467 (W 0.147364) | 24.6119 ± 0.230759 (W 0.0236384) | 🔵 tlinalg 1.26× faster than `lapack-openblas` |  |
| `svd_thin/n512/b1` | 99.8139 ± 0.307806 (W 0.786339) | 98.7976 ± 0.69727 (W 0.0543399) | · |  |

## canary-rectangular, f64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 7.89053 ± 0.0161559 (W 0.0365686) | 17.922 ± 0.0872771 (W 0.0212743) | 🔵 tlinalg 2.27× faster than `lapack-openblas` |  |
| `qr/4096x256/b1` | 22.8411 ± 0.0325104 (W 0.579827) | 35.7013 ± 0.339325 (W 0.0255107) | 🔵 tlinalg 1.56× faster than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 24.5597 ± 0.454449 (W 0.305451) | 38.973 ± 0.410198 (W 0.0313668) | 🔵 tlinalg 1.59× faster than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 39.4189 ± 0.279698 (W 0.259719) | 60.7983 ± 0.018257 (W 0.0707943) | 🔵 tlinalg 1.54× faster than `lapack-openblas` |  |

## canary-rectangular, c64, 8T (CPU 4-11)

| case | tlinalg-pool (ms) | lapack-openblas (ms) | vs `lapack-openblas` | notes |
|---|---|---|---|---|
| `householder_factor/4096x256/b1` | 19.9411 ± 0.0476979 (W 0.0553556) | 20.1088 ± 0.0483605 (W 0.0243042) | · |  |
| `qr/4096x256/b1` | 53.456 ± 0.169055 (W 0.12754) | 40.365 ± 0.13962 (W 0.033922) | 🔴 tlinalg 1.32× slower than `lapack-openblas` |  |
| `rank_revealing_qr/4096x256/b1` | 60.3822 ± 0.177435 (W 0.265862) | 51.4232 ± 0.313834 (W 1.102) | 🔴 tlinalg 1.17× slower than `lapack-openblas` |  |
| `svd_thin/4096x256/b1` | 111.219 ± 0.321955 (W 1.02001) | 86.0045 ± 0.162196 (W 0.35479) | 🔴 tlinalg 1.29× slower than `lapack-openblas` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
