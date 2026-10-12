<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261012T131758Z/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `6a873e6168e5738c0b023f0a0862f5965880cda0`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
- harness commit: `8c55247e04967493cc7b584648ebb91151c68ef8`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-12T14:15:33.197220Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261012T131758Z/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: Only the kernel entry points are measured. Tensor construction, dtype dispatch, session entry and pool checkout are tenferro's and are out of scope.
  Known blind spot: Batch extents are declared per regime, so a cost proportional to batch elements is visible only where the regime says so.
  Known blind spot: The providers are compared at the thread budgets declared here; a budget the vendor threads itself by, outside that set, is not covered.
  Known blind spot: A vendor arm records the vendor library, but only OpenBLAS reports the kernel its runtime dispatched to. MKL's manifest records its own version and the threading layer the harness pins; it names no kernel, because MKL exposes none to name.
  Known blind spot: The small and medium regimes give up the middle of their batch axis (small: batch 64 of 1, 64, 1024; medium: batch 16 of 1, 16, 128) and the medium regime also gives up n=64 of 32, 64, 128. A cost that is only visible in the middle of one of those ranges is not covered here. Large and tall declare every shape they measure.
- **Rows** — one row per engine in every table below:
  - `faer-1lane` — The faer-backed provider on one sequential lane: the per-item cost plus the batch loop, with no threading at all. The overhead baseline.
    Identity: tlinalg-rs (this repository's pinned revision)
    As measured: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
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
- CPU sets: 1T -> `4`, 4T -> `4-7`, 8T -> `4-11`

Every row below passed `tlbench verify` on the same grid before timing: the two
providers' factorizations are checked against each provider's documented convention
(reconstruction, orthonormality, residuals), not against each other's floating-point
output. Times are milliseconds, the best wall time per case and engine row; with more
than one complete set repeat the table shows the best repeat, and the A/A spread is
reported at its foot.

## small, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | - | 0.0007 |
| `cholesky/n16/b1024` | 0.5358 | - | 0.6195 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1077 | - | 0.1147 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2153 | - | 0.2280 |
| `eig/n16/b1` | 0.0535 | - | 0.0406 |
| `eig/n16/b1024` | 56.1489 | - | 41.5900 |
| `eig/n4/b1` | 0.0041 | - | 0.0037 |
| `eig/n4/b1024` | 3.5934 | - | 3.3120 |
| `eig/n8/b1` | 0.0143 | - | 0.0112 |
| `eig/n8/b1024` | 13.8649 | - | 10.6084 |
| `eigh/n16/b1` | 0.0178 | - | 0.0230 |
| `eigh/n16/b1024` | 17.9483 | - | 24.1536 |
| `eigh/n4/b1` | 0.0016 | - | 0.0019 |
| `eigh/n4/b1024` | 1.4806 | - | 1.7900 |
| `eigh/n8/b1` | 0.0051 | - | 0.0064 |
| `eigh/n8/b1024` | 5.0930 | - | 6.4904 |
| `eigvals/n16/b1` | 0.0371 | - | 0.0292 |
| `eigvals/n16/b1024` | 39.1101 | - | 29.8537 |
| `eigvals/n4/b1` | 0.0024 | - | 0.0026 |
| `eigvals/n4/b1024` | 1.9874 | - | 2.0740 |
| `eigvals/n8/b1` | 0.0098 | - | 0.0087 |
| `eigvals/n8/b1024` | 9.2269 | - | 8.0309 |
| `eigvalsh/n16/b1` | 0.0132 | - | 0.0084 |
| `eigvalsh/n16/b1024` | 13.2562 | - | 8.6762 |
| `eigvalsh/n4/b1` | 0.0013 | - | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1792 | - | 0.8339 |
| `eigvalsh/n8/b1` | 0.0044 | - | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0362 | - | 2.7096 |
| `full_piv_lu/n16/b1` | 0.0026 | - | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.1072 | - | 2.7106 |
| `full_piv_lu/n4/b1` | 0.0007 | - | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2332 | - | 0.2201 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6651 | - | 0.5994 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | - | 0.0038 |
| `full_piv_lu_solve/n16/b1024` | 2.1067 | - | 3.7155 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0006 |
| `full_piv_lu_solve/n4/b1024` | 0.3194 | - | 0.4348 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0012 |
| `full_piv_lu_solve/n8/b1024` | 0.7778 | - | 0.9936 |
| `householder_apply/n16/b1` | 0.0030 | - | 0.0030 |
| `householder_apply/n16/b1024` | 2.9458 | - | 2.6380 |
| `householder_apply/n4/b1` | 0.0004 | - | 0.0006 |
| `householder_apply/n4/b1024` | 0.2249 | - | 0.2471 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0011 |
| `householder_apply/n8/b1024` | 0.7541 | - | 0.7245 |
| `householder_factor/n16/b1` | 0.0023 | - | 0.0027 |
| `householder_factor/n16/b1024` | 2.2512 | - | 2.6052 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.2584 | - | 0.3200 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.7240 | - | 0.9012 |
| `lu/n16/b1` | 0.0019 | - | 0.0016 |
| `lu/n16/b1024` | 1.6158 | - | 1.3985 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.1807 | - | 0.1928 |
| `lu/n8/b1` | 0.0007 | - | 0.0007 |
| `lu/n8/b1024` | 0.4821 | - | 0.4789 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0011 |
| `lu_factor/n16/b1024` | 1.1386 | - | 1.1109 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1350 | - | 0.1298 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3473 | - | 0.3395 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0019 |
| `lu_factor_solve/n16/b1024` | 1.4482 | - | 1.8447 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.1648 | - | 0.3153 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0007 |
| `lu_factor_solve/n8/b1024` | 0.4751 | - | 0.6441 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0012 |
| `lu_solve_prepared/n16/b1024` | 0.3599 | - | 0.7095 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | - | 0.1882 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1380 | - | 0.3135 |
| `qr/n16/b1` | 0.0057 | - | 0.0048 |
| `qr/n16/b1024` | 5.4744 | - | 4.7115 |
| `qr/n4/b1` | 0.0008 | - | 0.0008 |
| `qr/n4/b1024` | 0.4450 | - | 0.5792 |
| `qr/n8/b1` | 0.0016 | - | 0.0018 |
| `qr/n8/b1024` | 1.4555 | - | 1.5958 |
| `rank_revealing_qr/n16/b1` | 0.0068 | - | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.2260 | - | 5.6397 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6913 | - | 0.6895 |
| `rank_revealing_qr/n8/b1` | 0.0023 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8771 | - | 1.8327 |
| `solve/n16/b1` | 0.0022 | - | 0.0023 |
| `solve/n16/b1024` | 1.6088 | - | 1.8793 |
| `solve/n4/b1` | 0.0006 | - | 0.0006 |
| `solve/n4/b1024` | 0.2193 | - | 0.3391 |
| `solve/n8/b1` | 0.0009 | - | 0.0009 |
| `solve/n8/b1024` | 0.5810 | - | 0.6713 |
| `svd_full/n16/b1` | 0.0327 | - | 0.0496 |
| `svd_full/n16/b1024` | 33.6713 | - | 49.6421 |
| `svd_full/n4/b1` | 0.0027 | - | 0.0044 |
| `svd_full/n4/b1024` | 2.5618 | - | 3.8780 |
| `svd_full/n8/b1` | 0.0091 | - | 0.0127 |
| `svd_full/n8/b1024` | 9.1534 | - | 12.9700 |
| `svd_thin/n16/b1` | 0.0328 | - | 0.0495 |
| `svd_thin/n16/b1024` | 33.9380 | - | 49.5252 |
| `svd_thin/n4/b1` | 0.0029 | - | 0.0043 |
| `svd_thin/n4/b1024` | 2.5325 | - | 3.8485 |
| `svd_thin/n8/b1` | 0.0093 | - | 0.0127 |
| `svd_thin/n8/b1024` | 9.4798 | - | 12.9740 |
| `svd_values/n16/b1` | 0.0240 | - | 0.0151 |
| `svd_values/n16/b1024` | 24.7132 | - | 15.1992 |
| `svd_values/n4/b1` | 0.0023 | - | 0.0026 |
| `svd_values/n4/b1024` | 1.9043 | - | 2.0907 |
| `svd_values/n8/b1` | 0.0069 | - | 0.0056 |
| `svd_values/n8/b1024` | 6.8038 | - | 5.3727 |
| `triangular_solve/n16/b1` | 0.0005 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3020 | - | 0.3991 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0512 | - | 0.1184 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n8/b1024` | 0.1310 | - | 0.1800 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0030 | 0.0007 |
| `cholesky/n16/b1024` | 0.4978 | 0.2531 | 0.6034 |
| `cholesky/n4/b1` | 0.0002 | 0.0026 | 0.0002 |
| `cholesky/n4/b1024` | 0.1079 | 0.0345 | 0.1168 |
| `cholesky/n8/b1` | 0.0003 | 0.0020 | 0.0003 |
| `cholesky/n8/b1024` | 0.2161 | 0.0594 | 0.2450 |
| `eig/n16/b1` | 0.0533 | 0.0569 | 0.0404 |
| `eig/n16/b1024` | 55.9573 | 16.9215 | 41.6254 |
| `eig/n4/b1` | 0.0040 | 0.0067 | 0.0037 |
| `eig/n4/b1024` | 3.5817 | 1.8265 | 3.2932 |
| `eig/n8/b1` | 0.0142 | 0.0169 | 0.0111 |
| `eig/n8/b1024` | 13.7529 | 6.4891 | 10.6597 |
| `eigh/n16/b1` | 0.0176 | 0.0204 | 0.0228 |
| `eigh/n16/b1024` | 17.6534 | 4.5060 | 23.9581 |
| `eigh/n4/b1` | 0.0016 | 0.0037 | 0.0019 |
| `eigh/n4/b1024` | 1.4714 | 0.3766 | 1.7830 |
| `eigh/n8/b1` | 0.0051 | 0.0068 | 0.0064 |
| `eigh/n8/b1024` | 5.0235 | 2.5317 | 6.5035 |
| `eigvals/n16/b1` | 0.0372 | 0.0399 | 0.0292 |
| `eigvals/n16/b1024` | 38.9825 | 15.9980 | 29.6879 |
| `eigvals/n4/b1` | 0.0023 | 0.0051 | 0.0026 |
| `eigvals/n4/b1024` | 1.9713 | 0.9770 | 2.0794 |
| `eigvals/n8/b1` | 0.0096 | 0.0121 | 0.0086 |
| `eigvals/n8/b1024` | 9.1765 | 3.1692 | 8.0062 |
| `eigvalsh/n16/b1` | 0.0132 | 0.0161 | 0.0084 |
| `eigvalsh/n16/b1024` | 13.2036 | 3.6679 | 8.6951 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0035 | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1727 | 0.5913 | 0.8265 |
| `eigvalsh/n8/b1` | 0.0044 | 0.0070 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0662 | 2.0382 | 2.7213 |
| `full_piv_lu/n16/b1` | 0.0027 | 0.0049 | 0.0027 |
| `full_piv_lu/n16/b1024` | 2.0905 | 1.0352 | 2.8535 |
| `full_piv_lu/n4/b1` | 0.0008 | 0.0024 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2334 | 0.1234 | 0.2262 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0036 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.7044 | 0.1966 | 0.5891 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0049 | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0955 | 1.0632 | 3.8439 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0025 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3218 | 0.1657 | 0.5462 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0039 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7858 | 0.3978 | 1.1725 |
| `householder_apply/n16/b1` | 0.0028 | 0.0048 | 0.0030 |
| `householder_apply/n16/b1024` | 2.7523 | 0.6876 | 2.7141 |
| `householder_apply/n4/b1` | 0.0004 | 0.0026 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2063 | 0.0603 | 0.2475 |
| `householder_apply/n8/b1` | 0.0008 | 0.0038 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6904 | 0.1798 | 0.7213 |
| `householder_factor/n16/b1` | 0.0022 | 0.0046 | 0.0027 |
| `householder_factor/n16/b1024` | 2.2005 | 0.5540 | 2.6279 |
| `householder_factor/n4/b1` | 0.0003 | 0.0026 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2658 | 0.0710 | 0.3221 |
| `householder_factor/n8/b1` | 0.0008 | 0.0033 | 0.0010 |
| `householder_factor/n8/b1024` | 0.7149 | 0.3668 | 0.9083 |
| `lu/n16/b1` | 0.0020 | 0.0044 | 0.0016 |
| `lu/n16/b1024` | 1.5350 | 0.7874 | 1.4668 |
| `lu/n4/b1` | 0.0004 | 0.0022 | 0.0004 |
| `lu/n4/b1024` | 0.1669 | 0.0483 | 0.1931 |
| `lu/n8/b1` | 0.0007 | 0.0024 | 0.0007 |
| `lu/n8/b1024` | 0.4830 | 0.1283 | 0.4794 |
| `lu_factor/n16/b1` | 0.0013 | 0.0037 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1490 | 0.5736 | 1.0718 |
| `lu_factor/n4/b1` | 0.0003 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1334 | 0.0419 | 0.1282 |
| `lu_factor/n8/b1` | 0.0006 | 0.0022 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3568 | 0.0926 | 0.3399 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0042 | 0.0021 |
| `lu_factor_solve/n16/b1024` | 1.4851 | 0.3793 | 2.0282 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0025 | 0.0006 |
| `lu_factor_solve/n4/b1024` | 0.1656 | 0.0510 | 0.6535 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0025 | 0.0011 |
| `lu_factor_solve/n8/b1024` | 0.4879 | 0.2459 | 0.8915 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0028 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3608 | 0.1906 | 0.6660 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0402 | 0.0190 | 0.5057 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0028 | 0.0009 |
| `lu_solve_prepared/n8/b1024` | 0.1369 | 0.0460 | 0.4783 |
| `qr/n16/b1` | 0.0055 | 0.0089 | 0.0049 |
| `qr/n16/b1024` | 5.2711 | 2.0604 | 4.7178 |
| `qr/n4/b1` | 0.0008 | 0.0024 | 0.0008 |
| `qr/n4/b1024` | 0.4319 | 0.1124 | 0.5764 |
| `qr/n8/b1` | 0.0016 | 0.0038 | 0.0018 |
| `qr/n8/b1024` | 1.4263 | 0.7058 | 1.5757 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0100 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 5.9833 | 1.5430 | 5.6128 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0033 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6821 | 0.1780 | 0.6890 |
| `rank_revealing_qr/n8/b1` | 0.0023 | 0.0046 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8397 | 0.9413 | 1.8026 |
| `solve/n16/b1` | 0.0021 | 0.0045 | 0.0023 |
| `solve/n16/b1024` | 1.5510 | 0.4059 | 2.2060 |
| `solve/n4/b1` | 0.0006 | 0.0027 | 0.0009 |
| `solve/n4/b1024` | 0.2188 | 0.0605 | 0.7924 |
| `solve/n8/b1` | 0.0010 | 0.0034 | 0.0011 |
| `solve/n8/b1024` | 0.5706 | 0.2776 | 1.1391 |
| `svd_full/n16/b1` | 0.0329 | 0.0366 | 0.0489 |
| `svd_full/n16/b1024` | 33.4103 | 8.9121 | 48.5384 |
| `svd_full/n4/b1` | 0.0029 | 0.0050 | 0.0043 |
| `svd_full/n4/b1024` | 2.5174 | 1.2905 | 3.8221 |
| `svd_full/n8/b1` | 0.0090 | 0.0116 | 0.0125 |
| `svd_full/n8/b1024` | 9.2173 | 2.2807 | 12.7993 |
| `svd_thin/n16/b1` | 0.0327 | 0.0368 | 0.0491 |
| `svd_thin/n16/b1024` | 33.3469 | 12.0220 | 48.7816 |
| `svd_thin/n4/b1` | 0.0029 | 0.0049 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5286 | 1.2894 | 3.8158 |
| `svd_thin/n8/b1` | 0.0091 | 0.0119 | 0.0124 |
| `svd_thin/n8/b1024` | 9.0570 | 2.8442 | 12.8194 |
| `svd_values/n16/b1` | 0.0239 | 0.0267 | 0.0149 |
| `svd_values/n16/b1024` | 24.7869 | 6.7895 | 14.9282 |
| `svd_values/n4/b1` | 0.0021 | 0.0044 | 0.0026 |
| `svd_values/n4/b1024` | 1.9038 | 0.9532 | 2.0965 |
| `svd_values/n8/b1` | 0.0068 | 0.0094 | 0.0056 |
| `svd_values/n8/b1024` | 6.7540 | 3.3725 | 5.3553 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0027 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3059 | 0.0837 | 0.6895 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0516 | 0.0212 | 0.4574 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0027 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1296 | 0.0419 | 0.4181 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0034 | 0.0007 |
| `cholesky/n16/b1024` | 0.5461 | 0.0779 | 0.6161 |
| `cholesky/n4/b1` | 0.0002 | 0.0023 | 0.0002 |
| `cholesky/n4/b1024` | 0.1074 | 0.0215 | 0.1200 |
| `cholesky/n8/b1` | 0.0003 | 0.0031 | 0.0003 |
| `cholesky/n8/b1024` | 0.2125 | 0.0608 | 0.2346 |
| `eig/n16/b1` | 0.0537 | 0.0577 | 0.0403 |
| `eig/n16/b1024` | 55.9837 | 9.0915 | 41.6650 |
| `eig/n4/b1` | 0.0040 | 0.0068 | 0.0037 |
| `eig/n4/b1024` | 3.6222 | 0.9122 | 3.2934 |
| `eig/n8/b1` | 0.0143 | 0.0171 | 0.0112 |
| `eig/n8/b1024` | 13.8220 | 2.3725 | 10.6735 |
| `eigh/n16/b1` | 0.0177 | 0.0206 | 0.0230 |
| `eigh/n16/b1024` | 17.7993 | 2.2859 | 24.0036 |
| `eigh/n4/b1` | 0.0017 | 0.0041 | 0.0019 |
| `eigh/n4/b1024` | 1.4675 | 0.3748 | 1.7929 |
| `eigh/n8/b1` | 0.0051 | 0.0081 | 0.0064 |
| `eigh/n8/b1024` | 5.0676 | 1.0301 | 6.5334 |
| `eigvals/n16/b1` | 0.0372 | 0.0404 | 0.0292 |
| `eigvals/n16/b1024` | 38.9587 | 6.3734 | 29.7949 |
| `eigvals/n4/b1` | 0.0023 | 0.0054 | 0.0026 |
| `eigvals/n4/b1024` | 1.9142 | 0.2886 | 2.0755 |
| `eigvals/n8/b1` | 0.0098 | 0.0233 | 0.0086 |
| `eigvals/n8/b1024` | 9.1604 | 1.1982 | 7.9724 |
| `eigvalsh/n16/b1` | 0.0162 | 0.0162 | 0.0085 |
| `eigvalsh/n16/b1024` | 13.2171 | 1.7126 | 8.7349 |
| `eigvalsh/n4/b1` | 0.0014 | 0.0043 | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1703 | 0.3009 | 0.8404 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0073 | 0.0030 |
| `eigvalsh/n8/b1024` | 4.0136 | 0.5239 | 2.7916 |
| `full_piv_lu/n16/b1` | 0.0027 | 0.0051 | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.1135 | 0.5332 | 2.8661 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0029 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2334 | 0.0647 | 0.2252 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0036 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6632 | 0.1731 | 0.6039 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0057 | 0.0039 |
| `full_piv_lu_solve/n16/b1024` | 2.0884 | 0.5225 | 3.8054 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0028 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3195 | 0.0858 | 0.5696 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0046 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7844 | 0.2041 | 1.1898 |
| `householder_apply/n16/b1` | 0.0029 | 0.0058 | 0.0030 |
| `householder_apply/n16/b1024` | 2.8283 | 0.3624 | 2.6433 |
| `householder_apply/n4/b1` | 0.0004 | 0.0020 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2161 | 0.0561 | 0.2473 |
| `householder_apply/n8/b1` | 0.0008 | 0.0025 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6894 | 0.1830 | 0.7198 |
| `householder_factor/n16/b1` | 0.0022 | 0.0052 | 0.0027 |
| `householder_factor/n16/b1024` | 2.2023 | 0.5571 | 2.6023 |
| `householder_factor/n4/b1` | 0.0004 | 0.0023 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2600 | 0.0704 | 0.3195 |
| `householder_factor/n8/b1` | 0.0008 | 0.0025 | 0.0011 |
| `householder_factor/n8/b1024` | 0.7225 | 0.1894 | 0.8986 |
| `lu/n16/b1` | 0.0019 | 0.0044 | 0.0016 |
| `lu/n16/b1024` | 1.5157 | 0.3867 | 1.3975 |
| `lu/n4/b1` | 0.0004 | 0.0036 | 0.0004 |
| `lu/n4/b1024` | 0.1779 | 0.0474 | 0.1948 |
| `lu/n8/b1` | 0.0007 | 0.0043 | 0.0007 |
| `lu/n8/b1024` | 0.4562 | 0.1260 | 0.4800 |
| `lu_factor/n16/b1` | 0.0013 | 0.0040 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1474 | 0.2891 | 1.0921 |
| `lu_factor/n4/b1` | 0.0003 | 0.0025 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1326 | 0.0393 | 0.1323 |
| `lu_factor/n8/b1` | 0.0005 | 0.0025 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3446 | 0.0937 | 0.3407 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0048 | 0.0022 |
| `lu_factor_solve/n16/b1024` | 1.4433 | 0.3696 | 2.2801 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0029 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.1658 | 0.0297 | 0.7743 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0038 | 0.0009 |
| `lu_factor_solve/n8/b1024` | 0.4836 | 0.1249 | 1.2391 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0023 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3740 | 0.1064 | 0.9194 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0023 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0400 | 0.0182 | 0.6189 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0027 | 0.0008 |
| `lu_solve_prepared/n8/b1024` | 0.1368 | 0.0334 | 0.7611 |
| `qr/n16/b1` | 0.0054 | 0.0084 | 0.0048 |
| `qr/n16/b1024` | 5.3259 | 0.6916 | 4.7083 |
| `qr/n4/b1` | 0.0008 | 0.0025 | 0.0008 |
| `qr/n4/b1024` | 0.4362 | 0.0665 | 0.5748 |
| `qr/n8/b1` | 0.0016 | 0.0046 | 0.0018 |
| `qr/n8/b1024` | 1.3941 | 0.3590 | 1.5803 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0098 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.0993 | 1.0887 | 5.5899 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0043 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7179 | 0.1796 | 0.7053 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0055 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8725 | 0.4752 | 1.8123 |
| `solve/n16/b1` | 0.0020 | 0.0052 | 0.0023 |
| `solve/n16/b1024` | 1.5416 | 0.2101 | 1.9779 |
| `solve/n4/b1` | 0.0006 | 0.0026 | 0.0009 |
| `solve/n4/b1024` | 0.2198 | 0.0599 | 0.7251 |
| `solve/n8/b1` | 0.0010 | 0.0043 | 0.0011 |
| `solve/n8/b1024` | 0.5558 | 0.0920 | 0.8990 |
| `svd_full/n16/b1` | 0.0325 | 0.0357 | 0.0490 |
| `svd_full/n16/b1024` | 33.4250 | 7.9832 | 48.9276 |
| `svd_full/n4/b1` | 0.0029 | 0.0060 | 0.0043 |
| `svd_full/n4/b1024` | 2.5212 | 0.6426 | 3.8470 |
| `svd_full/n8/b1` | 0.0089 | 0.0112 | 0.0125 |
| `svd_full/n8/b1024` | 9.0027 | 1.9247 | 12.9748 |
| `svd_thin/n16/b1` | 0.0328 | 0.0358 | 0.0486 |
| `svd_thin/n16/b1024` | 33.5144 | 7.5291 | 48.7670 |
| `svd_thin/n4/b1` | 0.0029 | 0.0057 | 0.0044 |
| `svd_thin/n4/b1024` | 2.5335 | 0.6423 | 3.8626 |
| `svd_thin/n8/b1` | 0.0090 | 0.0217 | 0.0124 |
| `svd_thin/n8/b1024` | 9.0731 | 1.7088 | 12.7890 |
| `svd_values/n16/b1` | 0.0238 | 0.0267 | 0.0150 |
| `svd_values/n16/b1024` | 24.3497 | 3.5482 | 14.9853 |
| `svd_values/n4/b1` | 0.0021 | 0.0053 | 0.0026 |
| `svd_values/n4/b1024` | 1.8789 | 0.4782 | 2.1054 |
| `svd_values/n8/b1` | 0.0069 | 0.0100 | 0.0056 |
| `svd_values/n8/b1024` | 6.7795 | 0.8893 | 5.3448 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0038 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3038 | 0.0822 | 0.6920 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0033 | 0.0005 |
| `triangular_solve/n4/b1024` | 0.0519 | 0.0173 | 0.3965 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0022 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1293 | 0.0368 | 0.5051 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0010 |
| `cholesky/n16/b1024` | 0.7863 | - | 0.9173 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1266 | - | 0.1361 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2684 | - | 0.2861 |
| `eig/n16/b1` | 0.0721 | - | 0.1001 |
| `eig/n16/b1024` | 76.4095 | - | 119.6233 |
| `eig/n4/b1` | 0.0060 | - | 0.0081 |
| `eig/n4/b1024` | 5.8633 | - | 7.9131 |
| `eig/n8/b1` | 0.0201 | - | 0.0262 |
| `eig/n8/b1024` | 20.6012 | - | 27.9801 |
| `eigh/n16/b1` | 0.0179 | - | 0.0261 |
| `eigh/n16/b1024` | 19.5226 | - | 26.9691 |
| `eigh/n4/b1` | 0.0019 | - | 0.0022 |
| `eigh/n4/b1024` | 1.7226 | - | 2.1442 |
| `eigh/n8/b1` | 0.0057 | - | 0.0072 |
| `eigh/n8/b1024` | 5.4603 | - | 7.4192 |
| `eigvals/n16/b1` | 0.0437 | - | 0.0749 |
| `eigvals/n16/b1024` | 46.4863 | - | 89.9505 |
| `eigvals/n4/b1` | 0.0030 | - | 0.0063 |
| `eigvals/n4/b1024` | 2.8644 | - | 6.0370 |
| `eigvals/n8/b1` | 0.0119 | - | 0.0211 |
| `eigvals/n8/b1024` | 11.9935 | - | 22.1947 |
| `eigvalsh/n16/b1` | 0.0136 | - | 0.0116 |
| `eigvalsh/n16/b1024` | 14.4247 | - | 11.5483 |
| `eigvalsh/n4/b1` | 0.0016 | - | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4375 | - | 1.2529 |
| `eigvalsh/n8/b1` | 0.0046 | - | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3551 | - | 3.6632 |
| `full_piv_lu/n16/b1` | 0.0031 | - | 0.0125 |
| `full_piv_lu/n16/b1024` | 2.8809 | - | 20.4761 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2784 | - | 0.5397 |
| `full_piv_lu/n8/b1` | 0.0012 | - | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.7899 | - | 2.3046 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | - | 0.0152 |
| `full_piv_lu_solve/n16/b1024` | 3.0737 | - | 22.4831 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4494 | - | 1.1576 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0036 |
| `full_piv_lu_solve/n8/b1024` | 1.1021 | - | 3.5766 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0046 |
| `householder_apply/n16/b1024` | 3.0797 | - | 4.4488 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0008 |
| `householder_apply/n4/b1024` | 0.1994 | - | 0.2709 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0016 |
| `householder_apply/n8/b1024` | 0.6535 | - | 0.8909 |
| `householder_factor/n16/b1` | 0.0027 | - | 0.0046 |
| `householder_factor/n16/b1024` | 2.6503 | - | 4.4443 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0007 |
| `householder_factor/n4/b1024` | 0.3239 | - | 0.5552 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0016 |
| `householder_factor/n8/b1024` | 0.8504 | - | 1.4254 |
| `lu/n16/b1` | 0.0022 | - | 0.0023 |
| `lu/n16/b1024` | 1.8260 | - | 2.4392 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.2142 | - | 0.2211 |
| `lu/n8/b1` | 0.0008 | - | 0.0008 |
| `lu/n8/b1024` | 0.5643 | - | 0.6073 |
| `lu_factor/n16/b1` | 0.0015 | - | 0.0017 |
| `lu_factor/n16/b1024` | 1.3103 | - | 1.6745 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1623 | - | 0.1619 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0005 |
| `lu_factor/n8/b1024` | 0.4258 | - | 0.4521 |
| `lu_factor_solve/n16/b1` | 0.0024 | - | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0734 | - | 2.6386 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0005 |
| `lu_factor_solve/n4/b1024` | 0.2602 | - | 0.4157 |
| `lu_factor_solve/n8/b1` | 0.0010 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.7020 | - | 0.9247 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7906 | - | 1.0095 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0982 | - | 0.2497 |
| `lu_solve_prepared/n8/b1` | 0.0005 | - | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.2884 | - | 0.4553 |
| `qr/n16/b1` | 0.0067 | - | 0.0077 |
| `qr/n16/b1024` | 6.4634 | - | 7.6501 |
| `qr/n4/b1` | 0.0007 | - | 0.0012 |
| `qr/n4/b1024` | 0.5163 | - | 0.8376 |
| `qr/n8/b1` | 0.0018 | - | 0.0026 |
| `qr/n8/b1024` | 1.6058 | - | 2.2522 |
| `rank_revealing_qr/n16/b1` | 0.0075 | - | 0.0098 |
| `rank_revealing_qr/n16/b1024` | 7.2631 | - | 10.0644 |
| `rank_revealing_qr/n4/b1` | 0.0012 | - | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8198 | - | 1.0818 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1834 | - | 2.9522 |
| `solve/n16/b1` | 0.0028 | - | 0.0030 |
| `solve/n16/b1024` | 2.2585 | - | 2.8108 |
| `solve/n4/b1` | 0.0007 | - | 0.0007 |
| `solve/n4/b1024` | 0.3099 | - | 0.4400 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.8000 | - | 0.9611 |
| `svd_full/n16/b1` | 0.0347 | - | 0.0551 |
| `svd_full/n16/b1024` | 36.7789 | - | 56.5507 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_full/n4/b1024` | 3.0010 | - | 4.7213 |
| `svd_full/n8/b1` | 0.0097 | - | 0.0146 |
| `svd_full/n8/b1024` | 10.1053 | - | 15.0017 |
| `svd_thin/n16/b1` | 0.0348 | - | 0.0554 |
| `svd_thin/n16/b1024` | 41.6408 | - | 56.7465 |
| `svd_thin/n4/b1` | 0.0030 | - | 0.0053 |
| `svd_thin/n4/b1024` | 3.0023 | - | 4.7720 |
| `svd_thin/n8/b1` | 0.0097 | - | 0.0147 |
| `svd_thin/n8/b1024` | 10.1412 | - | 15.0021 |
| `svd_values/n16/b1` | 0.0261 | - | 0.0198 |
| `svd_values/n16/b1024` | 27.3077 | - | 20.3004 |
| `svd_values/n4/b1` | 0.0026 | - | 0.0033 |
| `svd_values/n4/b1024` | 2.3041 | - | 2.7905 |
| `svd_values/n8/b1` | 0.0076 | - | 0.0072 |
| `svd_values/n8/b1024` | 7.7945 | - | 6.7188 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0007 |
| `triangular_solve/n16/b1024` | 0.6076 | - | 0.5665 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0955 | - | 0.1525 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.2420 | - | 0.2625 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0032 | 0.0010 |
| `cholesky/n16/b1024` | 0.7957 | 0.3944 | 0.9347 |
| `cholesky/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1175 | 0.0372 | 0.1368 |
| `cholesky/n8/b1` | 0.0004 | 0.0022 | 0.0004 |
| `cholesky/n8/b1024` | 0.2492 | 0.0696 | 0.2918 |
| `eig/n16/b1` | 0.0714 | 0.0759 | 0.0999 |
| `eig/n16/b1024` | 75.6445 | 20.9328 | 119.8084 |
| `eig/n4/b1` | 0.0061 | 0.0081 | 0.0082 |
| `eig/n4/b1024` | 5.8317 | 2.9671 | 7.9270 |
| `eig/n8/b1` | 0.0198 | 0.0231 | 0.0260 |
| `eig/n8/b1024` | 20.4406 | 10.3851 | 27.8848 |
| `eigh/n16/b1` | 0.0180 | 0.0211 | 0.0262 |
| `eigh/n16/b1024` | 19.4012 | 8.0192 | 26.9800 |
| `eigh/n4/b1` | 0.0019 | 0.0046 | 0.0022 |
| `eigh/n4/b1024` | 1.7275 | 0.4364 | 2.1425 |
| `eigh/n8/b1` | 0.0056 | 0.0093 | 0.0072 |
| `eigh/n8/b1024` | 5.4486 | 2.7443 | 7.5101 |
| `eigvals/n16/b1` | 0.0438 | 0.0468 | 0.0750 |
| `eigvals/n16/b1024` | 46.9295 | 17.9859 | 89.5482 |
| `eigvals/n4/b1` | 0.0030 | 0.0055 | 0.0063 |
| `eigvals/n4/b1024` | 2.8461 | 1.0490 | 6.0430 |
| `eigvals/n8/b1` | 0.0118 | 0.0147 | 0.0210 |
| `eigvals/n8/b1024` | 11.8819 | 2.9859 | 22.2271 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0168 | 0.0115 |
| `eigvalsh/n16/b1024` | 14.3338 | 6.3356 | 11.5929 |
| `eigvalsh/n4/b1` | 0.0017 | 0.0037 | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4208 | 0.7145 | 1.2492 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0066 | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3929 | 1.1046 | 3.6609 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0057 | 0.0118 |
| `full_piv_lu/n16/b1024` | 2.7484 | 1.3824 | 20.1724 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0025 | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2713 | 0.0723 | 0.5322 |
| `full_piv_lu/n8/b1` | 0.0012 | 0.0037 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7696 | 0.3947 | 2.3055 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0059 | 0.0161 |
| `full_piv_lu_solve/n16/b1024` | 3.0957 | 0.8014 | 22.6263 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0036 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4482 | 0.2293 | 1.2773 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0038 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1477 | 0.3115 | 3.6490 |
| `householder_apply/n16/b1` | 0.0027 | 0.0050 | 0.0046 |
| `householder_apply/n16/b1024` | 3.3972 | 1.1515 | 4.4150 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0009 |
| `householder_apply/n4/b1024` | 0.1957 | 0.0580 | 0.2703 |
| `householder_apply/n8/b1` | 0.0007 | 0.0036 | 0.0015 |
| `householder_apply/n8/b1024` | 0.6550 | 0.3215 | 0.8865 |
| `householder_factor/n16/b1` | 0.0027 | 0.0047 | 0.0045 |
| `householder_factor/n16/b1024` | 2.7293 | 0.7023 | 4.4138 |
| `householder_factor/n4/b1` | 0.0004 | 0.0027 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3225 | 0.0862 | 0.5506 |
| `householder_factor/n8/b1` | 0.0010 | 0.0032 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8597 | 0.2190 | 1.4198 |
| `lu/n16/b1` | 0.0021 | 0.0049 | 0.0023 |
| `lu/n16/b1024` | 1.8091 | 0.9129 | 2.5214 |
| `lu/n4/b1` | 0.0005 | 0.0026 | 0.0004 |
| `lu/n4/b1024` | 0.2077 | 0.0588 | 0.2319 |
| `lu/n8/b1` | 0.0008 | 0.0033 | 0.0008 |
| `lu/n8/b1024` | 0.5618 | 0.2841 | 0.6406 |
| `lu_factor/n16/b1` | 0.0015 | 0.0031 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2898 | 0.6473 | 1.6369 |
| `lu_factor/n4/b1` | 0.0004 | 0.0021 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1606 | 0.0458 | 0.1616 |
| `lu_factor/n8/b1` | 0.0006 | 0.0033 | 0.0005 |
| `lu_factor/n8/b1024` | 0.4122 | 0.1095 | 0.4505 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0040 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0717 | 1.0387 | 3.0102 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0026 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2535 | 0.1328 | 0.8351 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0032 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.7081 | 0.1787 | 1.4038 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0035 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7768 | 0.3993 | 1.1688 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0023 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0980 | 0.0346 | 0.6009 |
| `lu_solve_prepared/n8/b1` | 0.0005 | 0.0027 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2885 | 0.0838 | 0.8397 |
| `qr/n16/b1` | 0.0068 | 0.0096 | 0.0076 |
| `qr/n16/b1024` | 6.5602 | 3.2692 | 7.5901 |
| `qr/n4/b1` | 0.0007 | 0.0024 | 0.0011 |
| `qr/n4/b1024` | 0.5074 | 0.2573 | 0.8375 |
| `qr/n8/b1` | 0.0018 | 0.0041 | 0.0026 |
| `qr/n8/b1024` | 1.5638 | 0.7833 | 2.2456 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0098 | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.2450 | 2.2996 | 10.0417 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0034 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8140 | 0.4131 | 1.0777 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0047 | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.1874 | 1.1146 | 2.9531 |
| `solve/n16/b1` | 0.0028 | 0.0057 | 0.0031 |
| `solve/n16/b1024` | 2.3120 | 0.5766 | 2.9855 |
| `solve/n4/b1` | 0.0007 | 0.0024 | 0.0009 |
| `solve/n4/b1024` | 0.3124 | 0.0842 | 0.7094 |
| `solve/n8/b1` | 0.0012 | 0.0038 | 0.0014 |
| `solve/n8/b1024` | 0.8156 | 0.2103 | 1.2611 |
| `svd_full/n16/b1` | 0.0358 | 0.0375 | 0.0551 |
| `svd_full/n16/b1024` | 36.5371 | 14.8572 | 56.4815 |
| `svd_full/n4/b1` | 0.0031 | 0.0056 | 0.0052 |
| `svd_full/n4/b1024` | 2.9933 | 1.5057 | 4.7147 |
| `svd_full/n8/b1` | 0.0097 | 0.0126 | 0.0146 |
| `svd_full/n8/b1024` | 10.0970 | 5.0915 | 14.9385 |
| `svd_thin/n16/b1` | 0.0346 | 0.0378 | 0.0551 |
| `svd_thin/n16/b1024` | 36.4438 | 10.2300 | 56.5419 |
| `svd_thin/n4/b1` | 0.0030 | 0.0060 | 0.0053 |
| `svd_thin/n4/b1024` | 3.0145 | 1.5087 | 4.7117 |
| `svd_thin/n8/b1` | 0.0097 | 0.0128 | 0.0147 |
| `svd_thin/n8/b1024` | 10.0799 | 2.6569 | 14.9827 |
| `svd_values/n16/b1` | 0.0260 | 0.0292 | 0.0198 |
| `svd_values/n16/b1024` | 27.1978 | 10.0383 | 20.1006 |
| `svd_values/n4/b1` | 0.0026 | 0.0049 | 0.0033 |
| `svd_values/n4/b1024` | 2.3056 | 1.1529 | 2.7649 |
| `svd_values/n8/b1` | 0.0076 | 0.0104 | 0.0071 |
| `svd_values/n8/b1024` | 7.8181 | 2.3846 | 6.7280 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0024 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6153 | 0.1542 | 0.8030 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0007 |
| `triangular_solve/n4/b1024` | 0.0959 | 0.0511 | 0.3904 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0028 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2377 | 0.0685 | 0.6158 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0035 | 0.0010 |
| `cholesky/n16/b1024` | 0.7924 | 0.1950 | 0.9925 |
| `cholesky/n4/b1` | 0.0003 | 0.0028 | 0.0002 |
| `cholesky/n4/b1024` | 0.1195 | 0.0340 | 0.1388 |
| `cholesky/n8/b1` | 0.0004 | 0.0039 | 0.0004 |
| `cholesky/n8/b1024` | 0.2464 | 0.0668 | 0.2899 |
| `eig/n16/b1` | 0.0719 | 0.0769 | 0.1001 |
| `eig/n16/b1024` | 75.8801 | 10.1410 | 119.7234 |
| `eig/n4/b1` | 0.0061 | 0.0092 | 0.0081 |
| `eig/n4/b1024` | 5.7837 | 0.7554 | 7.9273 |
| `eig/n8/b1` | 0.0196 | 0.0228 | 0.0262 |
| `eig/n8/b1024` | 20.3956 | 3.0102 | 27.9760 |
| `eigh/n16/b1` | 0.0180 | 0.0211 | 0.0260 |
| `eigh/n16/b1024` | 19.4094 | 2.9094 | 27.1910 |
| `eigh/n4/b1` | 0.0019 | 0.0045 | 0.0023 |
| `eigh/n4/b1024` | 1.7183 | 0.2290 | 2.1612 |
| `eigh/n8/b1` | 0.0056 | 0.0084 | 0.0072 |
| `eigh/n8/b1024` | 5.4567 | 1.3392 | 7.4197 |
| `eigvals/n16/b1` | 0.0436 | 0.0465 | 0.0750 |
| `eigvals/n16/b1024` | 46.1998 | 8.2388 | 89.7149 |
| `eigvals/n4/b1` | 0.0031 | 0.0062 | 0.0063 |
| `eigvals/n4/b1024` | 2.8187 | 0.7139 | 6.0462 |
| `eigvals/n8/b1` | 0.0119 | 0.0142 | 0.0211 |
| `eigvals/n8/b1024` | 11.8800 | 1.5213 | 22.2400 |
| `eigvalsh/n16/b1` | 0.0137 | 0.0165 | 0.0117 |
| `eigvalsh/n16/b1024` | 14.2787 | 2.1966 | 11.5905 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0055 | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4216 | 0.3648 | 1.2833 |
| `eigvalsh/n8/b1` | 0.0046 | 0.0072 | 0.0040 |
| `eigvalsh/n8/b1024` | 4.3571 | 1.0929 | 3.6995 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0060 | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.8453 | 0.4502 | 20.1152 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0039 | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2724 | 0.0737 | 0.5409 |
| `full_piv_lu/n8/b1` | 0.0012 | 0.0050 | 0.0021 |
| `full_piv_lu/n8/b1024` | 0.7816 | 0.2036 | 2.3094 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0066 | 0.0155 |
| `full_piv_lu_solve/n16/b1024` | 3.1142 | 0.7739 | 22.8620 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0039 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4444 | 0.0620 | 1.2823 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0048 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1203 | 0.2807 | 3.6942 |
| `householder_apply/n16/b1` | 0.0027 | 0.0059 | 0.0046 |
| `householder_apply/n16/b1024` | 3.3721 | 0.7064 | 4.4670 |
| `householder_apply/n4/b1` | 0.0003 | 0.0038 | 0.0009 |
| `householder_apply/n4/b1024` | 0.1978 | 0.0550 | 0.2731 |
| `householder_apply/n8/b1` | 0.0007 | 0.0036 | 0.0015 |
| `householder_apply/n8/b1024` | 0.6723 | 0.1701 | 0.8927 |
| `householder_factor/n16/b1` | 0.0027 | 0.0057 | 0.0045 |
| `householder_factor/n16/b1024` | 2.6639 | 0.6760 | 4.4181 |
| `householder_factor/n4/b1` | 0.0004 | 0.0020 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3248 | 0.0533 | 0.5542 |
| `householder_factor/n8/b1` | 0.0009 | 0.0041 | 0.0017 |
| `householder_factor/n8/b1024` | 0.8561 | 0.2216 | 1.4232 |
| `lu/n16/b1` | 0.0022 | 0.0054 | 0.0023 |
| `lu/n16/b1024` | 1.9482 | 0.2766 | 2.4593 |
| `lu/n4/b1` | 0.0005 | 0.0025 | 0.0004 |
| `lu/n4/b1024` | 0.2146 | 0.0580 | 0.2288 |
| `lu/n8/b1` | 0.0008 | 0.0038 | 0.0009 |
| `lu/n8/b1024` | 0.5624 | 0.1510 | 0.6117 |
| `lu_factor/n16/b1` | 0.0015 | 0.0044 | 0.0016 |
| `lu_factor/n16/b1024` | 1.3333 | 0.3396 | 1.6509 |
| `lu_factor/n4/b1` | 0.0004 | 0.0032 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1628 | 0.0291 | 0.1630 |
| `lu_factor/n8/b1` | 0.0006 | 0.0031 | 0.0005 |
| `lu_factor/n8/b1024` | 0.4259 | 0.0661 | 0.4557 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0049 | 0.0028 |
| `lu_factor_solve/n16/b1024` | 2.1032 | 0.5372 | 3.0328 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0021 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2516 | 0.0702 | 0.8201 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0038 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.7063 | 0.1881 | 1.4268 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0039 | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7757 | 0.2118 | 1.1848 |
| `lu_solve_prepared/n4/b1` | 0.0003 | 0.0037 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0984 | 0.0346 | 0.6008 |
| `lu_solve_prepared/n8/b1` | 0.0005 | 0.0035 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2879 | 0.0862 | 0.8250 |
| `qr/n16/b1` | 0.0066 | 0.0099 | 0.0076 |
| `qr/n16/b1024` | 6.6238 | 0.8495 | 7.5957 |
| `qr/n4/b1` | 0.0007 | 0.0033 | 0.0012 |
| `qr/n4/b1024` | 0.5111 | 0.0693 | 0.8357 |
| `qr/n8/b1` | 0.0018 | 0.0052 | 0.0026 |
| `qr/n8/b1024` | 1.5482 | 0.2011 | 2.2434 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0105 | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.3079 | 1.8573 | 9.9729 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0036 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8267 | 0.2128 | 1.0773 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0055 | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1664 | 0.2786 | 2.9466 |
| `solve/n16/b1` | 0.0028 | 0.0058 | 0.0031 |
| `solve/n16/b1024` | 2.2709 | 0.5754 | 3.1533 |
| `solve/n4/b1` | 0.0007 | 0.0041 | 0.0009 |
| `solve/n4/b1024` | 0.3157 | 0.0824 | 0.7027 |
| `solve/n8/b1` | 0.0012 | 0.0048 | 0.0014 |
| `solve/n8/b1024` | 0.8038 | 0.2131 | 1.4216 |
| `svd_full/n16/b1` | 0.0352 | 0.0376 | 0.0547 |
| `svd_full/n16/b1024` | 36.6969 | 5.5683 | 56.5492 |
| `svd_full/n4/b1` | 0.0030 | 0.0061 | 0.0053 |
| `svd_full/n4/b1024` | 3.0013 | 0.7575 | 4.7001 |
| `svd_full/n8/b1` | 0.0097 | 0.0122 | 0.0147 |
| `svd_full/n8/b1024` | 10.1741 | 1.3190 | 15.1933 |
| `svd_thin/n16/b1` | 0.0355 | 0.0379 | 0.0551 |
| `svd_thin/n16/b1024` | 36.5877 | 7.9970 | 56.5334 |
| `svd_thin/n4/b1` | 0.0031 | 0.0059 | 0.0054 |
| `svd_thin/n4/b1024` | 2.9901 | 0.7611 | 4.7772 |
| `svd_thin/n8/b1` | 0.0097 | 0.0231 | 0.0146 |
| `svd_thin/n8/b1024` | 10.1112 | 2.5570 | 14.9804 |
| `svd_values/n16/b1` | 0.0261 | 0.0293 | 0.0197 |
| `svd_values/n16/b1024` | 27.3701 | 6.3799 | 20.1956 |
| `svd_values/n4/b1` | 0.0024 | 0.0054 | 0.0033 |
| `svd_values/n4/b1024` | 2.2926 | 0.5803 | 2.7834 |
| `svd_values/n8/b1` | 0.0076 | 0.0106 | 0.0071 |
| `svd_values/n8/b1024` | 7.7876 | 1.0133 | 6.7035 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0032 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6043 | 0.0861 | 0.8177 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0026 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0966 | 0.0280 | 0.4605 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0029 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2383 | 0.0429 | 0.5229 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0372 | - | 0.0400 |
| `cholesky/n128/b128` | 5.7386 | - | 6.3425 |
| `cholesky/n32/b1` | 0.0019 | - | 0.0020 |
| `cholesky/n32/b128` | 0.2444 | - | 0.2592 |
| `eigh/n128/b1` | 1.2694 | - | 1.1261 |
| `eigh/n128/b128` | 162.6567 | - | 147.7126 |
| `eigh/n32/b1` | 0.0643 | - | 0.0785 |
| `eigh/n32/b128` | 8.4498 | - | 10.0059 |
| `eigvalsh/n128/b1` | 0.6973 | - | 0.4966 |
| `eigvalsh/n128/b128` | 91.0806 | - | 64.6414 |
| `eigvalsh/n32/b1` | 0.0486 | - | 0.0291 |
| `eigvalsh/n32/b128` | 6.4064 | - | 3.7350 |
| `householder_apply/n128/b1` | 0.1261 | - | 0.2564 |
| `householder_apply/n128/b128` | 17.4711 | - | 33.9179 |
| `householder_apply/n32/b1` | 0.0108 | - | 0.0114 |
| `householder_apply/n32/b128` | 1.3669 | - | 1.3543 |
| `householder_factor/n128/b1` | 0.1033 | - | 0.2171 |
| `householder_factor/n128/b128` | 13.5991 | - | 28.3533 |
| `householder_factor/n32/b1` | 0.0073 | - | 0.0085 |
| `householder_factor/n32/b128` | 0.9263 | - | 1.0767 |
| `lu/n128/b1` | 0.0896 | - | 0.0870 |
| `lu/n128/b128` | 12.1731 | - | 13.5624 |
| `lu/n32/b1` | 0.0053 | - | 0.0050 |
| `lu/n32/b128` | 0.6100 | - | 0.5994 |
| `lu_factor/n128/b1` | 0.0578 | - | 0.0782 |
| `lu_factor/n128/b128` | 8.2990 | - | 11.1735 |
| `lu_factor/n32/b1` | 0.0033 | - | 0.0039 |
| `lu_factor/n32/b128` | 0.3938 | - | 0.4970 |
| `lu_factor_solve/n128/b1` | 0.0630 | - | 0.0903 |
| `lu_factor_solve/n128/b128` | 8.8914 | - | 12.4071 |
| `lu_factor_solve/n32/b1` | 0.0042 | - | 0.0057 |
| `lu_factor_solve/n32/b128` | 0.5048 | - | 0.7170 |
| `lu_solve_prepared/n128/b1` | 0.0059 | - | 0.0121 |
| `lu_solve_prepared/n128/b128` | 1.7486 | - | 2.5096 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0017 |
| `lu_solve_prepared/n32/b128` | 0.1129 | - | 0.2045 |
| `qr/n128/b1` | 0.3391 | - | 0.4291 |
| `qr/n128/b128` | 44.0081 | - | 57.1737 |
| `qr/n32/b1` | 0.0205 | - | 0.0160 |
| `qr/n32/b128` | 2.5766 | - | 2.0113 |
| `rank_revealing_qr/n128/b1` | 0.3458 | - | 0.4936 |
| `rank_revealing_qr/n128/b128` | 45.4046 | - | 65.2871 |
| `rank_revealing_qr/n32/b1` | 0.0205 | - | 0.0197 |
| `rank_revealing_qr/n32/b128` | 2.5772 | - | 2.4829 |
| `solve/n128/b1` | 0.0664 | - | 0.0924 |
| `solve/n128/b128` | 8.7798 | - | 12.6040 |
| `solve/n32/b1` | 0.0048 | - | 0.0063 |
| `solve/n32/b128` | 0.5356 | - | 0.7373 |
| `svd_thin/n128/b1` | 2.4074 | - | 1.9986 |
| `svd_thin/n128/b128` | 306.8680 | - | 259.9750 |
| `svd_thin/n32/b1` | 0.1188 | - | 0.1390 |
| `svd_thin/n32/b128` | 15.5565 | - | 17.8024 |
| `svd_values/n128/b1` | 1.4155 | - | 0.8129 |
| `svd_values/n128/b128` | 181.0207 | - | 106.0524 |
| `svd_values/n32/b1` | 0.0930 | - | 0.0461 |
| `svd_values/n32/b128` | 11.9965 | - | 5.9911 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0061 |
| `triangular_solve/n128/b128` | 0.8287 | - | 1.3290 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0010 |
| `triangular_solve/n32/b128` | 0.0886 | - | 0.1076 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0362 | 0.0467 | 0.0456 |
| `cholesky/n128/b128` | 5.7657 | 6.7883 | 6.9146 |
| `cholesky/n32/b1` | 0.0019 | 0.0037 | 0.0021 |
| `cholesky/n32/b128` | 0.2392 | 0.1258 | 0.2566 |
| `eigh/n128/b1` | 1.2563 | 1.2852 | 0.9069 |
| `eigh/n128/b128` | 162.4922 | 163.8514 | 117.2682 |
| `eigh/n32/b1` | 0.0644 | 0.0678 | 0.0705 |
| `eigh/n32/b128` | 8.4462 | 2.1173 | 9.1153 |
| `eigvalsh/n128/b1` | 0.6981 | 0.7014 | 0.4732 |
| `eigvalsh/n128/b128` | 90.6980 | 90.5981 | 62.2865 |
| `eigvalsh/n32/b1` | 0.0485 | 0.0516 | 0.0290 |
| `eigvalsh/n32/b128` | 6.4012 | 3.2538 | 3.7785 |
| `householder_apply/n128/b1` | 0.1354 | 0.1320 | 0.2296 |
| `householder_apply/n128/b128` | 18.2527 | 17.8850 | 31.5112 |
| `householder_apply/n32/b1` | 0.0105 | 0.0131 | 0.0107 |
| `householder_apply/n32/b128` | 1.3771 | 0.3465 | 1.3316 |
| `householder_factor/n128/b1` | 0.1047 | 0.1236 | 0.2308 |
| `householder_factor/n128/b128` | 13.5453 | 16.4968 | 29.5488 |
| `householder_factor/n32/b1` | 0.0071 | 0.0101 | 0.0086 |
| `householder_factor/n32/b128` | 0.9258 | 0.2412 | 1.0896 |
| `lu/n128/b1` | 0.0900 | 0.1022 | 0.0866 |
| `lu/n128/b128` | 12.6886 | 13.8094 | 13.6160 |
| `lu/n32/b1` | 0.0052 | 0.0084 | 0.0049 |
| `lu/n32/b128` | 0.6045 | 0.3073 | 0.6107 |
| `lu_factor/n128/b1` | 0.0573 | 0.0710 | 0.0792 |
| `lu_factor/n128/b128` | 8.3327 | 2.5343 | 11.1808 |
| `lu_factor/n32/b1` | 0.0033 | 0.0060 | 0.0039 |
| `lu_factor/n32/b128` | 0.3940 | 0.2086 | 0.4954 |
| `lu_factor_solve/n128/b1` | 0.0626 | 0.0755 | 0.0881 |
| `lu_factor_solve/n128/b128` | 8.9848 | 2.7155 | 12.1383 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0070 | 0.0053 |
| `lu_factor_solve/n32/b128` | 0.5060 | 0.2609 | 0.7307 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0091 | 0.0072 |
| `lu_solve_prepared/n128/b128` | 2.0598 | 1.0368 | 2.0313 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0034 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1139 | 0.0351 | 0.1593 |
| `qr/n128/b1` | 0.3434 | 0.6377 | 0.4531 |
| `qr/n128/b128` | 44.3099 | 81.4604 | 60.1798 |
| `qr/n32/b1` | 0.0206 | 0.0469 | 0.0161 |
| `qr/n32/b128` | 2.5587 | 0.6475 | 1.9902 |
| `rank_revealing_qr/n128/b1` | 0.3448 | 0.3675 | 0.5121 |
| `rank_revealing_qr/n128/b128` | 44.9037 | 47.5979 | 67.1147 |
| `rank_revealing_qr/n32/b1` | 0.0205 | 0.0464 | 0.0197 |
| `rank_revealing_qr/n32/b128` | 2.5695 | 0.6650 | 2.4816 |
| `solve/n128/b1` | 0.0660 | 0.0811 | 0.0913 |
| `solve/n128/b128` | 8.7132 | 10.5292 | 12.3761 |
| `solve/n32/b1` | 0.0047 | 0.0084 | 0.0058 |
| `solve/n32/b128` | 0.5371 | 0.2748 | 0.7223 |
| `svd_thin/n128/b1` | 2.4110 | 1.8182 | 1.9895 |
| `svd_thin/n128/b128` | 306.8514 | 230.9819 | 261.2819 |
| `svd_thin/n32/b1` | 0.1171 | 0.1217 | 0.1381 |
| `svd_thin/n32/b128` | 15.1357 | 4.2181 | 17.8944 |
| `svd_values/n128/b1` | 1.4099 | 1.4412 | 0.8145 |
| `svd_values/n128/b128` | 182.1294 | 181.0526 | 110.8811 |
| `svd_values/n32/b1` | 0.0924 | 0.0966 | 0.0462 |
| `svd_values/n32/b128` | 11.9218 | 4.0165 | 6.0204 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0059 | 0.0040 |
| `triangular_solve/n128/b128` | 1.0751 | 1.1214 | 1.2833 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0024 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0891 | 0.0279 | 0.1026 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0376 | 0.0533 | 0.0449 |
| `cholesky/n128/b128` | 5.7296 | 7.0385 | 6.8418 |
| `cholesky/n32/b1` | 0.0019 | 0.0051 | 0.0020 |
| `cholesky/n32/b128` | 0.2403 | 0.0363 | 0.2619 |
| `eigh/n128/b1` | 1.2674 | 1.2440 | 0.8696 |
| `eigh/n128/b128` | 162.4379 | 160.0795 | 113.0275 |
| `eigh/n32/b1` | 0.0645 | 0.0676 | 0.0697 |
| `eigh/n32/b128` | 8.4662 | 2.1483 | 8.9808 |
| `eigvalsh/n128/b1` | 0.6944 | 0.6972 | 0.4771 |
| `eigvalsh/n128/b128` | 90.0468 | 89.9214 | 61.2242 |
| `eigvalsh/n32/b1` | 0.0488 | 0.0518 | 0.0290 |
| `eigvalsh/n32/b128` | 6.3771 | 1.6350 | 3.7934 |
| `householder_apply/n128/b1` | 0.1287 | 0.1888 | 0.2372 |
| `householder_apply/n128/b128` | 17.5290 | 24.2657 | 31.3635 |
| `householder_apply/n32/b1` | 0.0106 | 0.0138 | 0.0107 |
| `householder_apply/n32/b128` | 1.3585 | 0.3409 | 1.3285 |
| `householder_factor/n128/b1` | 0.1050 | 0.1731 | 0.2312 |
| `householder_factor/n128/b128` | 13.6997 | 22.6373 | 29.9138 |
| `householder_factor/n32/b1` | 0.0073 | 0.0100 | 0.0085 |
| `householder_factor/n32/b128` | 0.9163 | 0.2401 | 1.0732 |
| `lu/n128/b1` | 0.0862 | 0.1160 | 0.0867 |
| `lu/n128/b128` | 12.6543 | 15.5134 | 13.6272 |
| `lu/n32/b1` | 0.0052 | 0.0139 | 0.0049 |
| `lu/n32/b128` | 0.5776 | 0.0815 | 0.6086 |
| `lu_factor/n128/b1` | 0.0564 | 0.0833 | 0.0777 |
| `lu_factor/n128/b128` | 8.3714 | 2.2177 | 11.1297 |
| `lu_factor/n32/b1` | 0.0033 | 0.0058 | 0.0040 |
| `lu_factor/n32/b128` | 0.3951 | 0.1084 | 0.4984 |
| `lu_factor_solve/n128/b1` | 0.0620 | 0.0868 | 0.0870 |
| `lu_factor_solve/n128/b128` | 9.0378 | 1.6412 | 12.3087 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0072 | 0.0054 |
| `lu_factor_solve/n32/b128` | 0.4958 | 0.1332 | 0.7463 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0088 | 0.0073 |
| `lu_solve_prepared/n128/b128` | 1.8767 | 0.2985 | 2.2334 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0041 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1150 | 0.0340 | 0.1597 |
| `qr/n128/b1` | 0.3420 | 0.9428 | 0.4571 |
| `qr/n128/b128` | 44.1004 | 120.1588 | 59.9399 |
| `qr/n32/b1` | 0.0207 | 0.0615 | 0.0163 |
| `qr/n32/b128` | 2.5746 | 0.3339 | 2.0258 |
| `rank_revealing_qr/n128/b1` | 0.3487 | 0.4207 | 0.5123 |
| `rank_revealing_qr/n128/b128` | 45.3567 | 56.2837 | 66.7197 |
| `rank_revealing_qr/n32/b1` | 0.0206 | 0.0674 | 0.0196 |
| `rank_revealing_qr/n32/b128` | 2.5520 | 0.3399 | 2.4705 |
| `solve/n128/b1` | 0.0666 | 0.0922 | 0.0919 |
| `solve/n128/b128` | 8.8063 | 12.0702 | 12.3678 |
| `solve/n32/b1` | 0.0048 | 0.0071 | 0.0059 |
| `solve/n32/b128` | 0.5416 | 0.1406 | 0.7236 |
| `svd_thin/n128/b1` | 2.4109 | 1.8597 | 1.9996 |
| `svd_thin/n128/b128` | 307.7219 | 238.9991 | 260.4217 |
| `svd_thin/n32/b1` | 0.1170 | 0.1218 | 0.1384 |
| `svd_thin/n32/b128` | 15.1626 | 1.9242 | 17.8678 |
| `svd_values/n128/b1` | 1.4095 | 1.4367 | 0.8232 |
| `svd_values/n128/b128` | 180.8806 | 180.3248 | 105.6621 |
| `svd_values/n32/b1` | 0.0930 | 0.0966 | 0.0453 |
| `svd_values/n32/b128` | 12.0114 | 2.1354 | 5.9660 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0064 | 0.0040 |
| `triangular_solve/n128/b128` | 1.0769 | 1.1457 | 1.2416 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0032 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0902 | 0.0256 | 0.1054 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1087 | - | 0.1084 |
| `cholesky/n128/b128` | 15.9636 | - | 15.4932 |
| `cholesky/n32/b1` | 0.0033 | - | 0.0034 |
| `cholesky/n32/b128` | 0.4240 | - | 0.4335 |
| `eigh/n128/b1` | 1.8424 | - | 3.2633 |
| `eigh/n128/b128` | 241.1736 | - | 422.4383 |
| `eigh/n32/b1` | 0.0806 | - | 0.1084 |
| `eigh/n32/b128` | 10.5385 | - | 14.0684 |
| `eigvalsh/n128/b1` | 0.9291 | - | 0.9477 |
| `eigvalsh/n128/b128` | 122.0228 | - | 123.6025 |
| `eigvalsh/n32/b1` | 0.0526 | - | 0.0419 |
| `eigvalsh/n32/b128` | 6.9065 | - | 5.4201 |
| `householder_apply/n128/b1` | 0.4852 | - | 0.6923 |
| `householder_apply/n128/b128` | 64.4034 | - | 91.7605 |
| `householder_apply/n32/b1` | 0.0143 | - | 0.0199 |
| `householder_apply/n32/b128` | 1.8539 | - | 2.5051 |
| `householder_factor/n128/b1` | 0.3505 | - | 0.4357 |
| `householder_factor/n128/b128` | 45.3587 | - | 57.0742 |
| `householder_factor/n32/b1` | 0.0113 | - | 0.0157 |
| `householder_factor/n32/b128` | 1.4470 | - | 1.9999 |
| `lu/n128/b1` | 0.2018 | - | 0.2137 |
| `lu/n128/b128` | 28.2565 | - | 31.2355 |
| `lu/n32/b1` | 0.0080 | - | 0.0080 |
| `lu/n32/b128` | 1.0771 | - | 1.1085 |
| `lu_factor/n128/b1` | 0.1622 | - | 0.1936 |
| `lu_factor/n128/b128` | 22.5328 | - | 25.6134 |
| `lu_factor/n32/b1` | 0.0056 | - | 0.0064 |
| `lu_factor/n32/b128` | 0.6835 | - | 0.8219 |
| `lu_factor_solve/n128/b1` | 0.1806 | - | 0.2208 |
| `lu_factor_solve/n128/b128` | 25.0369 | - | 29.3032 |
| `lu_factor_solve/n32/b1` | 0.0078 | - | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9587 | - | 1.1294 |
| `lu_solve_prepared/n128/b1` | 0.0188 | - | 0.0286 |
| `lu_solve_prepared/n128/b128` | 4.0615 | - | 5.1525 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.2871 | - | 0.3127 |
| `qr/n128/b1` | 0.9675 | - | 0.8712 |
| `qr/n128/b128` | 124.8416 | - | 113.8734 |
| `qr/n32/b1` | 0.0422 | - | 0.0291 |
| `qr/n32/b128` | 5.4527 | - | 3.6568 |
| `rank_revealing_qr/n128/b1` | 1.0125 | - | 0.9906 |
| `rank_revealing_qr/n128/b128` | 129.9390 | - | 132.0438 |
| `rank_revealing_qr/n32/b1` | 0.0386 | - | 0.0366 |
| `rank_revealing_qr/n32/b128` | 4.9548 | - | 4.8896 |
| `solve/n128/b1` | 0.1865 | - | 0.2282 |
| `solve/n128/b128` | 24.5658 | - | 29.3581 |
| `solve/n32/b1` | 0.0085 | - | 0.0093 |
| `solve/n32/b128` | 1.0123 | - | 1.1757 |
| `svd_thin/n128/b1` | 3.9156 | - | 3.4969 |
| `svd_thin/n128/b128` | 505.4976 | - | 456.0185 |
| `svd_thin/n32/b1` | 0.1505 | - | 0.1675 |
| `svd_thin/n32/b128` | 19.6746 | - | 22.0986 |
| `svd_values/n128/b1` | 1.8812 | - | 1.3893 |
| `svd_values/n128/b128` | 244.9872 | - | 178.4588 |
| `svd_values/n32/b1` | 0.1009 | - | 0.0635 |
| `svd_values/n32/b128` | 13.3089 | - | 8.3320 |
| `triangular_solve/n128/b1` | 0.0109 | - | 0.0147 |
| `triangular_solve/n128/b128` | 2.2679 | - | 2.9546 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0013 |
| `triangular_solve/n32/b128` | 0.1913 | - | 0.1554 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1094 | 0.1104 | 0.0787 |
| `cholesky/n128/b128` | 16.0058 | 15.7227 | 11.2875 |
| `cholesky/n32/b1` | 0.0033 | 0.0059 | 0.0035 |
| `cholesky/n32/b128` | 0.4186 | 0.2119 | 0.4437 |
| `eigh/n128/b1` | 1.8616 | 1.7570 | 3.1923 |
| `eigh/n128/b128` | 241.4949 | 227.1765 | 408.2695 |
| `eigh/n32/b1` | 0.0803 | 0.0845 | 0.1089 |
| `eigh/n32/b128` | 10.5387 | 2.6603 | 14.1564 |
| `eigvalsh/n128/b1` | 0.9358 | 0.9338 | 0.8897 |
| `eigvalsh/n128/b128` | 122.0234 | 121.5243 | 115.5557 |
| `eigvalsh/n32/b1` | 0.0526 | 0.0559 | 0.0420 |
| `eigvalsh/n32/b128` | 6.9249 | 3.4943 | 5.4365 |
| `householder_apply/n128/b1` | 0.4748 | 0.2574 | 0.3696 |
| `householder_apply/n128/b128` | 65.8058 | 35.3921 | 50.2694 |
| `householder_apply/n32/b1` | 0.0145 | 0.0176 | 0.0195 |
| `householder_apply/n32/b128` | 1.8447 | 0.9371 | 2.4880 |
| `householder_factor/n128/b1` | 0.3433 | 0.2227 | 0.3843 |
| `householder_factor/n128/b128` | 45.4462 | 29.1321 | 50.7082 |
| `householder_factor/n32/b1` | 0.0113 | 0.0144 | 0.0158 |
| `householder_factor/n32/b128` | 1.4508 | 0.3708 | 1.9747 |
| `lu/n128/b1` | 0.2072 | 0.1902 | 0.1441 |
| `lu/n128/b128` | 28.3476 | 26.0507 | 21.9065 |
| `lu/n32/b1` | 0.0078 | 0.0107 | 0.0080 |
| `lu/n32/b128` | 1.0070 | 0.5005 | 1.1164 |
| `lu_factor/n128/b1` | 0.1625 | 0.1517 | 0.1202 |
| `lu_factor/n128/b128` | 22.6025 | 6.2952 | 15.5768 |
| `lu_factor/n32/b1` | 0.0056 | 0.0082 | 0.0065 |
| `lu_factor/n32/b128` | 0.6789 | 0.3520 | 0.8256 |
| `lu_factor_solve/n128/b1` | 0.1815 | 0.1711 | 0.1407 |
| `lu_factor_solve/n128/b128` | 24.9817 | 6.6810 | 18.1144 |
| `lu_factor_solve/n32/b1` | 0.0079 | 0.0110 | 0.0086 |
| `lu_factor_solve/n32/b128` | 0.9612 | 0.2527 | 1.1562 |
| `lu_solve_prepared/n128/b1` | 0.0187 | 0.0221 | 0.0179 |
| `lu_solve_prepared/n128/b128` | 4.1448 | 1.5329 | 4.0657 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0048 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2851 | 0.1474 | 0.2601 |
| `qr/n128/b1` | 0.9700 | 0.8472 | 0.7722 |
| `qr/n128/b128` | 124.9152 | 111.1147 | 101.2206 |
| `qr/n32/b1` | 0.0418 | 0.0654 | 0.0286 |
| `qr/n32/b128` | 5.3859 | 1.3762 | 3.6608 |
| `rank_revealing_qr/n128/b1` | 1.0158 | 0.7999 | 0.9083 |
| `rank_revealing_qr/n128/b128` | 130.6624 | 104.0943 | 120.5260 |
| `rank_revealing_qr/n32/b1` | 0.0388 | 0.0629 | 0.0364 |
| `rank_revealing_qr/n32/b128` | 4.9625 | 2.4895 | 4.8219 |
| `solve/n128/b1` | 0.1862 | 0.1728 | 0.1485 |
| `solve/n128/b128` | 24.4902 | 22.7955 | 19.2340 |
| `solve/n32/b1` | 0.0085 | 0.0115 | 0.0093 |
| `solve/n32/b128` | 1.0045 | 0.2672 | 1.1766 |
| `svd_thin/n128/b1` | 3.9219 | 2.7165 | 3.0274 |
| `svd_thin/n128/b128` | 506.2389 | 350.6490 | 390.2659 |
| `svd_thin/n32/b1` | 0.1499 | 0.1541 | 0.1712 |
| `svd_thin/n32/b128` | 19.5793 | 7.1085 | 22.5320 |
| `svd_values/n128/b1` | 1.8880 | 1.9107 | 1.5379 |
| `svd_values/n128/b128` | 244.0409 | 243.4273 | 195.2678 |
| `svd_values/n32/b1` | 0.1007 | 0.1051 | 0.0638 |
| `svd_values/n32/b128` | 13.2791 | 6.2761 | 8.3005 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0133 | 0.0093 |
| `triangular_solve/n128/b128` | 2.3330 | 2.2754 | 2.5257 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0033 | 0.0013 |
| `triangular_solve/n32/b128` | 0.1937 | 0.0979 | 0.1559 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1059 | 0.1133 | 0.0899 |
| `cholesky/n128/b128` | 16.0358 | 16.4194 | 13.7754 |
| `cholesky/n32/b1` | 0.0033 | 0.0063 | 0.0034 |
| `cholesky/n32/b128` | 0.4143 | 0.0562 | 0.4329 |
| `eigh/n128/b1` | 1.8484 | 1.6229 | 3.1654 |
| `eigh/n128/b128` | 240.9614 | 211.9578 | 408.6857 |
| `eigh/n32/b1` | 0.0808 | 0.0850 | 0.1089 |
| `eigh/n32/b128` | 10.4982 | 1.3615 | 14.0066 |
| `eigvalsh/n128/b1` | 0.9267 | 0.9293 | 0.8856 |
| `eigvalsh/n128/b128` | 121.9071 | 121.6712 | 114.9871 |
| `eigvalsh/n32/b1` | 0.0528 | 0.0557 | 0.0421 |
| `eigvalsh/n32/b128` | 6.9369 | 1.7543 | 5.4708 |
| `householder_apply/n128/b1` | 0.4733 | 0.3306 | 0.3212 |
| `householder_apply/n128/b128` | 64.5310 | 44.5924 | 44.8524 |
| `householder_apply/n32/b1` | 0.0143 | 0.0174 | 0.0199 |
| `householder_apply/n32/b128` | 1.8954 | 0.4705 | 2.5052 |
| `householder_factor/n128/b1` | 0.3437 | 0.2773 | 0.3802 |
| `householder_factor/n128/b128` | 45.4938 | 36.6744 | 50.1020 |
| `householder_factor/n32/b1` | 0.0113 | 0.0142 | 0.0159 |
| `householder_factor/n32/b128` | 1.4372 | 0.3672 | 1.9904 |
| `lu/n128/b1` | 0.2067 | 0.2021 | 0.1384 |
| `lu/n128/b128` | 28.7610 | 28.1748 | 21.0215 |
| `lu/n32/b1` | 0.0078 | 0.0106 | 0.0080 |
| `lu/n32/b128` | 1.0096 | 0.1262 | 1.1179 |
| `lu_factor/n128/b1` | 0.1626 | 0.1616 | 0.1130 |
| `lu_factor/n128/b128` | 22.5349 | 6.1716 | 14.6909 |
| `lu_factor/n32/b1` | 0.0056 | 0.0082 | 0.0064 |
| `lu_factor/n32/b128` | 0.6757 | 0.1784 | 0.8196 |
| `lu_factor_solve/n128/b1` | 0.1812 | 0.1817 | 0.1346 |
| `lu_factor_solve/n128/b128` | 24.9910 | 3.6849 | 17.3526 |
| `lu_factor_solve/n32/b1` | 0.0078 | 0.0112 | 0.0087 |
| `lu_factor_solve/n32/b128` | 0.9534 | 0.1343 | 1.1551 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0220 | 0.0184 |
| `lu_solve_prepared/n128/b128` | 4.0833 | 0.7655 | 4.1297 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0053 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2851 | 0.0772 | 0.2574 |
| `qr/n128/b1` | 0.9697 | 1.1839 | 0.7667 |
| `qr/n128/b128` | 125.0619 | 154.4545 | 100.3256 |
| `qr/n32/b1` | 0.0424 | 0.0866 | 0.0288 |
| `qr/n32/b128` | 5.3949 | 0.7126 | 3.6470 |
| `rank_revealing_qr/n128/b1` | 1.0101 | 0.8683 | 0.8964 |
| `rank_revealing_qr/n128/b128` | 130.2039 | 114.4308 | 119.5139 |
| `rank_revealing_qr/n32/b1` | 0.0386 | 0.0853 | 0.0365 |
| `rank_revealing_qr/n32/b128` | 4.9211 | 0.9722 | 4.8390 |
| `solve/n128/b1` | 0.1849 | 0.1861 | 0.1504 |
| `solve/n128/b128` | 24.5665 | 24.3756 | 19.3117 |
| `solve/n32/b1` | 0.0085 | 0.0112 | 0.0095 |
| `solve/n32/b128` | 1.0083 | 0.2578 | 1.2059 |
| `svd_thin/n128/b1` | 3.9169 | 2.7622 | 2.9870 |
| `svd_thin/n128/b128` | 505.9690 | 359.9821 | 387.8083 |
| `svd_thin/n32/b1` | 0.1507 | 0.1542 | 0.1672 |
| `svd_thin/n32/b128` | 21.0506 | 2.7604 | 22.0456 |
| `svd_values/n128/b1` | 1.8770 | 1.9154 | 1.5752 |
| `svd_values/n128/b128` | 244.0126 | 243.0883 | 202.1945 |
| `svd_values/n32/b1` | 0.1003 | 0.1054 | 0.0636 |
| `svd_values/n32/b128` | 13.3325 | 1.7404 | 8.2923 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0135 | 0.0092 |
| `triangular_solve/n128/b128` | 2.1848 | 2.2627 | 2.4929 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0047 | 0.0012 |
| `triangular_solve/n32/b128` | 0.1945 | 0.0503 | 0.1700 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1927 | - | 0.2322 |
| `cholesky/n256/b4` | 0.7811 | - | 0.9329 |
| `cholesky/n512/b1` | 1.2482 | - | 1.5821 |
| `cholesky/n512/b4` | 5.7434 | - | 6.6283 |
| `eigh/n256/b1` | 5.5647 | - | 5.4024 |
| `eigh/n256/b4` | 22.3427 | - | 21.5956 |
| `eigh/n512/b1` | 28.7351 | - | 30.2944 |
| `eigh/n512/b4` | 115.4480 | - | 121.4590 |
| `eigvalsh/n256/b1` | 2.9269 | - | 2.4761 |
| `eigvalsh/n256/b4` | 11.9439 | - | 9.8422 |
| `eigvalsh/n512/b1` | 14.1633 | - | 14.1036 |
| `eigvalsh/n512/b4` | 57.1244 | - | 57.0221 |
| `householder_apply/n256/b1` | 0.8252 | - | 1.6344 |
| `householder_apply/n256/b4` | 3.3257 | - | 6.6089 |
| `householder_apply/n512/b1` | 6.2023 | - | 11.8851 |
| `householder_apply/n512/b4` | 25.0344 | - | 47.5748 |
| `householder_factor/n256/b1` | 0.6248 | - | 1.0962 |
| `householder_factor/n256/b4` | 2.4994 | - | 4.3854 |
| `householder_factor/n512/b1` | 4.3641 | - | 7.4218 |
| `householder_factor/n512/b4` | 17.5177 | - | 29.7925 |
| `lu/n256/b1` | 0.4638 | - | 0.4854 |
| `lu/n256/b4` | 1.9435 | - | 2.0646 |
| `lu/n512/b1` | 3.1789 | - | 3.2022 |
| `lu/n512/b4` | 12.7637 | - | 13.1402 |
| `lu_factor/n256/b1` | 0.3537 | - | 0.4449 |
| `lu_factor/n256/b4` | 1.5283 | - | 1.7882 |
| `lu_factor/n512/b1` | 2.8208 | - | 2.8903 |
| `lu_factor/n512/b4` | 11.7227 | - | 11.8346 |
| `lu_factor_solve/n256/b1` | 0.3709 | - | 0.4882 |
| `lu_factor_solve/n256/b4` | 1.4972 | - | 1.9556 |
| `lu_factor_solve/n512/b1` | 2.8861 | - | 3.0477 |
| `lu_factor_solve/n512/b4` | 12.0628 | - | 12.4407 |
| `lu_solve_prepared/n256/b1` | 0.0171 | - | 0.0423 |
| `lu_solve_prepared/n256/b4` | 0.0800 | - | 0.1935 |
| `lu_solve_prepared/n512/b1` | 0.0624 | - | 0.1440 |
| `lu_solve_prepared/n512/b4` | 0.4312 | - | 1.0187 |
| `qr/n256/b1` | 1.8528 | - | 2.1771 |
| `qr/n256/b4` | 7.3877 | - | 8.7410 |
| `qr/n512/b1` | 11.4752 | - | 14.7794 |
| `qr/n512/b4` | 46.0389 | - | 60.1057 |
| `rank_revealing_qr/n256/b1` | 2.1080 | - | 2.6194 |
| `rank_revealing_qr/n256/b4` | 8.4674 | - | 10.5786 |
| `rank_revealing_qr/n512/b1` | 14.7430 | - | 18.7752 |
| `rank_revealing_qr/n512/b4` | 59.1761 | - | 75.9053 |
| `solve/n256/b1` | 0.3865 | - | 0.4944 |
| `solve/n256/b4` | 1.5509 | - | 1.9996 |
| `solve/n512/b1` | 2.8383 | - | 3.0716 |
| `solve/n512/b4` | 11.3370 | - | 12.3972 |
| `svd_thin/n256/b1` | 12.1985 | - | 11.0020 |
| `svd_thin/n256/b4` | 48.7467 | - | 44.1328 |
| `svd_thin/n512/b1` | 70.7314 | - | 71.3951 |
| `svd_thin/n512/b4` | 283.5374 | - | 291.1290 |
| `svd_values/n256/b1` | 6.9975 | - | 4.5789 |
| `svd_values/n256/b4` | 27.7297 | - | 18.6102 |
| `svd_values/n512/b1` | 38.8044 | - | 31.2008 |
| `svd_values/n512/b4` | 154.4810 | - | 127.4149 |
| `triangular_solve/n256/b1` | 0.0106 | - | 0.0203 |
| `triangular_solve/n256/b4` | 0.0437 | - | 0.0840 |
| `triangular_solve/n512/b1` | 0.0344 | - | 0.0752 |
| `triangular_solve/n512/b4` | 0.1615 | - | 0.3653 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1923 | 0.1798 | 0.1548 |
| `cholesky/n256/b4` | 0.7825 | 0.7322 | 0.6385 |
| `cholesky/n512/b1` | 1.2711 | 0.7824 | 0.7635 |
| `cholesky/n512/b4` | 5.5948 | 3.6253 | 3.4382 |
| `eigh/n256/b1` | 5.5947 | 4.2389 | 3.6045 |
| `eigh/n256/b4` | 22.5386 | 17.3761 | 14.3812 |
| `eigh/n512/b1` | 28.6245 | 15.9791 | 16.3759 |
| `eigh/n512/b4` | 115.1424 | 64.9473 | 65.4873 |
| `eigvalsh/n256/b1` | 2.9435 | 2.9647 | 1.9131 |
| `eigvalsh/n256/b4` | 11.9809 | 11.9200 | 7.6912 |
| `eigvalsh/n512/b1` | 14.0829 | 11.9851 | 7.5226 |
| `eigvalsh/n512/b4` | 56.7018 | 47.9018 | 30.3641 |
| `householder_apply/n256/b1` | 0.8219 | 0.3242 | 1.0966 |
| `householder_apply/n256/b4` | 3.3198 | 1.3380 | 4.5020 |
| `householder_apply/n512/b1` | 6.1582 | 1.8184 | 6.8354 |
| `householder_apply/n512/b4` | 25.0866 | 7.5693 | 27.9767 |
| `householder_factor/n256/b1` | 0.6194 | 0.3444 | 0.8451 |
| `householder_factor/n256/b4` | 2.4908 | 1.3821 | 3.4409 |
| `householder_factor/n512/b1` | 4.3505 | 1.6412 | 4.5171 |
| `householder_factor/n512/b4` | 17.5926 | 6.7160 | 18.3699 |
| `lu/n256/b1` | 0.4769 | 0.4377 | 0.2850 |
| `lu/n256/b4` | 1.9498 | 1.7756 | 1.2515 |
| `lu/n512/b1` | 3.1721 | 1.9211 | 1.6800 |
| `lu/n512/b4` | 12.9244 | 7.6160 | 6.9978 |
| `lu_factor/n256/b1` | 0.3530 | 0.3133 | 0.2399 |
| `lu_factor/n256/b4` | 1.5233 | 0.7782 | 0.9662 |
| `lu_factor/n512/b1` | 2.8160 | 1.4755 | 1.3600 |
| `lu_factor/n512/b4` | 11.7566 | 5.2720 | 5.5585 |
| `lu_factor_solve/n256/b1` | 0.3704 | 0.3364 | 0.2701 |
| `lu_factor_solve/n256/b4` | 1.4924 | 0.3873 | 1.0936 |
| `lu_factor_solve/n512/b1` | 2.8780 | 1.5424 | 1.4718 |
| `lu_factor_solve/n512/b4` | 12.1033 | 4.6736 | 6.1225 |
| `lu_solve_prepared/n256/b1` | 0.0172 | 0.0228 | 0.0277 |
| `lu_solve_prepared/n256/b4` | 0.0799 | 0.0227 | 0.1301 |
| `lu_solve_prepared/n512/b1` | 0.0742 | 0.0697 | 0.1006 |
| `lu_solve_prepared/n512/b4` | 0.4366 | 0.1969 | 0.8471 |
| `qr/n256/b1` | 1.8471 | 1.7451 | 1.6812 |
| `qr/n256/b4` | 7.3948 | 7.1327 | 6.7901 |
| `qr/n512/b1` | 11.6236 | 6.1214 | 9.1280 |
| `qr/n512/b4` | 46.0307 | 24.3095 | 36.7773 |
| `rank_revealing_qr/n256/b1` | 2.1188 | 1.4987 | 2.3079 |
| `rank_revealing_qr/n256/b4` | 8.4574 | 5.9412 | 9.3211 |
| `rank_revealing_qr/n512/b1` | 14.6906 | 6.2546 | 14.7470 |
| `rank_revealing_qr/n512/b4` | 59.1867 | 24.9959 | 58.8822 |
| `solve/n256/b1` | 0.3867 | 0.3478 | 0.2844 |
| `solve/n256/b4` | 1.5299 | 1.4739 | 1.1532 |
| `solve/n512/b1` | 2.8397 | 1.5856 | 1.5395 |
| `solve/n512/b4` | 11.3271 | 6.2505 | 6.1661 |
| `svd_thin/n256/b1` | 12.2304 | 8.7641 | 9.3462 |
| `svd_thin/n256/b4` | 48.8753 | 35.8379 | 37.4427 |
| `svd_thin/n512/b1` | 71.7944 | 40.0686 | 55.8302 |
| `svd_thin/n512/b4` | 283.8018 | 161.6335 | 223.3163 |
| `svd_values/n256/b1` | 6.9412 | 7.0992 | 4.4246 |
| `svd_values/n256/b4` | 27.6811 | 28.1417 | 17.9813 |
| `svd_values/n512/b1` | 38.9828 | 31.7564 | 28.8075 |
| `svd_values/n512/b4` | 155.2595 | 126.5355 | 117.7951 |
| `triangular_solve/n256/b1` | 0.0105 | 0.0153 | 0.0127 |
| `triangular_solve/n256/b4` | 0.0462 | 0.0593 | 0.0606 |
| `triangular_solve/n512/b1` | 0.0343 | 0.0359 | 0.0507 |
| `triangular_solve/n512/b4` | 0.1545 | 0.1408 | 0.2572 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1953 | 0.1914 | 0.1600 |
| `cholesky/n256/b4` | 0.8089 | 0.8703 | 0.6520 |
| `cholesky/n512/b1` | 1.3092 | 0.7259 | 0.6934 |
| `cholesky/n512/b4` | 5.5903 | 3.2277 | 3.0692 |
| `eigh/n256/b1` | 5.8419 | 4.1420 | 3.3281 |
| `eigh/n256/b4` | 22.5853 | 16.8239 | 13.4993 |
| `eigh/n512/b1` | 28.5884 | 14.9574 | 14.1123 |
| `eigh/n512/b4` | 114.8195 | 59.6517 | 55.8973 |
| `eigvalsh/n256/b1` | 2.9626 | 2.9851 | 1.9013 |
| `eigvalsh/n256/b4` | 11.7651 | 12.0138 | 7.5209 |
| `eigvalsh/n512/b1` | 14.0117 | 11.5942 | 6.8396 |
| `eigvalsh/n512/b4` | 56.8964 | 47.2284 | 27.1452 |
| `householder_apply/n256/b1` | 0.8258 | 0.4046 | 1.0500 |
| `householder_apply/n256/b4` | 3.3163 | 1.6754 | 4.1873 |
| `householder_apply/n512/b1` | 6.1042 | 1.8227 | 5.8881 |
| `householder_apply/n512/b4` | 25.2161 | 7.8603 | 24.4242 |
| `householder_factor/n256/b1` | 0.6204 | 0.4293 | 0.8378 |
| `householder_factor/n256/b4` | 2.4642 | 1.6821 | 3.2922 |
| `householder_factor/n512/b1` | 4.3434 | 1.7489 | 4.0650 |
| `householder_factor/n512/b4` | 17.4707 | 7.1631 | 16.2724 |
| `lu/n256/b1` | 0.4629 | 0.4827 | 0.2488 |
| `lu/n256/b4` | 1.9121 | 1.9274 | 1.1087 |
| `lu/n512/b1` | 3.1926 | 1.9847 | 1.1612 |
| `lu/n512/b4` | 12.7570 | 7.8932 | 4.8794 |
| `lu_factor/n256/b1` | 0.3811 | 0.3824 | 0.2025 |
| `lu_factor/n256/b4` | 1.5309 | 1.4559 | 0.8169 |
| `lu_factor/n512/b1` | 2.8417 | 1.4821 | 0.8435 |
| `lu_factor/n512/b4` | 11.7661 | 6.3484 | 3.4470 |
| `lu_factor_solve/n256/b1` | 0.3978 | 0.3991 | 0.2387 |
| `lu_factor_solve/n256/b4` | 1.4893 | 1.4436 | 0.9467 |
| `lu_factor_solve/n512/b1` | 2.8984 | 1.5906 | 0.9781 |
| `lu_factor_solve/n512/b4` | 12.0351 | 6.4758 | 3.9552 |
| `lu_solve_prepared/n256/b1` | 0.0174 | 0.0294 | 0.0266 |
| `lu_solve_prepared/n256/b4` | 0.0748 | 0.1087 | 0.1215 |
| `lu_solve_prepared/n512/b1` | 0.0731 | 0.0763 | 0.1097 |
| `lu_solve_prepared/n512/b4` | 0.3721 | 0.3835 | 0.7803 |
| `qr/n256/b1` | 1.8565 | 2.4500 | 1.6623 |
| `qr/n256/b4` | 7.4118 | 9.8639 | 6.6788 |
| `qr/n512/b1` | 11.5284 | 6.8595 | 8.2347 |
| `qr/n512/b4` | 46.0189 | 28.1661 | 32.8771 |
| `rank_revealing_qr/n256/b1` | 2.1276 | 1.5676 | 2.3063 |
| `rank_revealing_qr/n256/b4` | 8.3703 | 6.2250 | 9.1751 |
| `rank_revealing_qr/n512/b1` | 14.7156 | 5.7588 | 13.8521 |
| `rank_revealing_qr/n512/b4` | 58.9179 | 23.5689 | 56.7221 |
| `solve/n256/b1` | 0.3869 | 0.4191 | 0.2545 |
| `solve/n256/b4` | 1.5360 | 1.6552 | 1.0130 |
| `solve/n512/b1` | 2.8465 | 1.6522 | 1.0352 |
| `solve/n512/b4` | 11.3688 | 6.6200 | 4.1819 |
| `svd_thin/n256/b1` | 12.2223 | 8.9576 | 9.2132 |
| `svd_thin/n256/b4` | 48.8418 | 35.9076 | 36.8433 |
| `svd_thin/n512/b1` | 70.8311 | 38.0982 | 52.5075 |
| `svd_thin/n512/b4` | 283.2472 | 154.0104 | 212.5840 |
| `svd_values/n256/b1` | 6.9391 | 7.1768 | 4.4534 |
| `svd_values/n256/b4` | 27.6271 | 28.6947 | 18.0247 |
| `svd_values/n512/b1` | 38.6913 | 32.2283 | 28.3981 |
| `svd_values/n512/b4` | 154.3214 | 128.2536 | 116.0523 |
| `triangular_solve/n256/b1` | 0.0106 | 0.0191 | 0.0127 |
| `triangular_solve/n256/b4` | 0.0460 | 0.0641 | 0.0621 |
| `triangular_solve/n512/b1` | 0.0362 | 0.0441 | 0.0553 |
| `triangular_solve/n512/b4` | 0.1718 | 0.1847 | 0.3037 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7045 | - | 0.7653 |
| `cholesky/n256/b4` | 2.7784 | - | 3.0700 |
| `cholesky/n512/b1` | 4.7163 | - | 5.4190 |
| `cholesky/n512/b4` | 19.7301 | - | 22.6289 |
| `eigh/n256/b1` | 10.2537 | - | 21.4963 |
| `eigh/n256/b4` | 41.3101 | - | 86.0813 |
| `eigh/n512/b1` | 63.0322 | - | 156.7710 |
| `eigh/n512/b4` | 253.1947 | - | 630.6183 |
| `eigvalsh/n256/b1` | 4.9702 | - | 5.6440 |
| `eigvalsh/n256/b4` | 19.8646 | - | 22.6506 |
| `eigvalsh/n512/b1` | 29.5346 | - | 37.4802 |
| `eigvalsh/n512/b4` | 118.5590 | - | 149.7384 |
| `householder_apply/n256/b1` | 3.3694 | - | 4.7166 |
| `householder_apply/n256/b4` | 13.6453 | - | 19.0701 |
| `householder_apply/n512/b1` | 24.7725 | - | 32.1087 |
| `householder_apply/n512/b4` | 97.1557 | - | 128.8832 |
| `householder_factor/n256/b1` | 2.3344 | - | 3.0038 |
| `householder_factor/n256/b4` | 9.3306 | - | 12.0177 |
| `householder_factor/n512/b1` | 16.7322 | - | 20.8135 |
| `householder_factor/n512/b4` | 67.2961 | - | 83.6046 |
| `lu/n256/b1` | 1.2684 | - | 1.4306 |
| `lu/n256/b4` | 5.1944 | - | 5.9574 |
| `lu/n512/b1` | 8.7072 | - | 10.2525 |
| `lu/n512/b4` | 34.9430 | - | 41.1811 |
| `lu_factor/n256/b1` | 1.1381 | - | 1.3326 |
| `lu_factor/n256/b4` | 4.5996 | - | 5.3437 |
| `lu_factor/n512/b1` | 8.1099 | - | 9.5361 |
| `lu_factor/n512/b4` | 33.0180 | - | 38.2135 |
| `lu_factor_solve/n256/b1` | 1.2008 | - | 1.4575 |
| `lu_factor_solve/n256/b4` | 4.8578 | - | 5.7872 |
| `lu_factor_solve/n512/b1` | 8.2926 | - | 9.9763 |
| `lu_factor_solve/n512/b4` | 33.9665 | - | 39.9947 |
| `lu_solve_prepared/n256/b1` | 0.0627 | - | 0.1216 |
| `lu_solve_prepared/n256/b4` | 0.2506 | - | 0.4458 |
| `lu_solve_prepared/n512/b1` | 0.2086 | - | 0.4997 |
| `lu_solve_prepared/n512/b4` | 1.3074 | - | 2.1259 |
| `qr/n256/b1` | 6.2453 | - | 6.0105 |
| `qr/n256/b4` | 24.8269 | - | 24.1594 |
| `qr/n512/b1` | 42.2543 | - | 41.7061 |
| `qr/n512/b4` | 169.5653 | - | 168.0337 |
| `rank_revealing_qr/n256/b1` | 6.7520 | - | 6.4418 |
| `rank_revealing_qr/n256/b4` | 26.9424 | - | 26.0815 |
| `rank_revealing_qr/n512/b1` | 47.4796 | - | 44.9416 |
| `rank_revealing_qr/n512/b4` | 192.2346 | - | 180.3003 |
| `solve/n256/b1` | 1.1985 | - | 1.4819 |
| `solve/n256/b4` | 4.7924 | - | 5.9430 |
| `solve/n512/b1` | 8.2743 | - | 9.9773 |
| `solve/n512/b4` | 33.0447 | - | 40.4406 |
| `svd_thin/n256/b1` | 23.9824 | - | 22.4569 |
| `svd_thin/n256/b4` | 97.2193 | - | 89.5352 |
| `svd_thin/n512/b1` | 152.4603 | - | 143.7229 |
| `svd_thin/n512/b4` | 608.3683 | - | 574.9358 |
| `svd_values/n256/b1` | 11.0136 | - | 9.6954 |
| `svd_values/n256/b4` | 44.0530 | - | 38.6693 |
| `svd_values/n512/b1` | 66.5748 | - | 59.1325 |
| `svd_values/n512/b4` | 264.0723 | - | 236.4395 |
| `triangular_solve/n256/b1` | 0.0339 | - | 0.0628 |
| `triangular_solve/n256/b4` | 0.1374 | - | 0.2596 |
| `triangular_solve/n512/b1` | 0.1137 | - | 0.2212 |
| `triangular_solve/n512/b4` | 0.5132 | - | 0.8757 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7044 | 0.4953 | 0.3692 |
| `cholesky/n256/b4` | 2.8368 | 1.9816 | 1.3833 |
| `cholesky/n512/b1` | 4.7488 | 2.4519 | 2.0857 |
| `cholesky/n512/b4` | 19.6896 | 10.3938 | 9.2702 |
| `eigh/n256/b1` | 10.2318 | 7.1855 | 19.4372 |
| `eigh/n256/b4` | 41.2954 | 31.9564 | 78.3135 |
| `eigh/n512/b1` | 63.0154 | 28.6650 | 127.6652 |
| `eigh/n512/b4` | 251.8279 | 115.7781 | 511.5508 |
| `eigvalsh/n256/b1` | 4.9650 | 5.0291 | 4.9402 |
| `eigvalsh/n256/b4` | 19.8855 | 19.9671 | 19.6981 |
| `eigvalsh/n512/b1` | 29.4604 | 19.9911 | 20.5180 |
| `eigvalsh/n512/b4` | 118.1361 | 79.7700 | 82.0318 |
| `householder_apply/n256/b1` | 3.3760 | 1.0522 | 2.2406 |
| `householder_apply/n256/b4` | 13.6706 | 4.3058 | 9.2037 |
| `householder_apply/n512/b1` | 24.6213 | 6.7555 | 12.3327 |
| `householder_apply/n512/b4` | 97.1089 | 26.9107 | 49.2841 |
| `householder_factor/n256/b1` | 2.3252 | 0.9487 | 1.7081 |
| `householder_factor/n256/b4` | 9.3508 | 3.8361 | 6.8768 |
| `householder_factor/n512/b1` | 16.6561 | 5.3223 | 8.4810 |
| `householder_factor/n512/b4` | 66.8688 | 21.3631 | 34.6538 |
| `lu/n256/b1` | 1.2683 | 0.8391 | 0.7778 |
| `lu/n256/b4` | 5.2919 | 3.4864 | 3.3010 |
| `lu/n512/b1` | 8.7767 | 3.9343 | 3.7231 |
| `lu/n512/b4` | 34.9523 | 15.5658 | 14.9594 |
| `lu_factor/n256/b1` | 1.1372 | 0.6969 | 0.6651 |
| `lu_factor/n256/b4` | 4.5882 | 1.1912 | 2.6743 |
| `lu_factor/n512/b1` | 8.0671 | 3.1520 | 2.9925 |
| `lu_factor/n512/b4` | 32.9806 | 9.1235 | 11.9771 |
| `lu_factor_solve/n256/b1` | 1.2052 | 0.7630 | 0.7486 |
| `lu_factor_solve/n256/b4` | 4.9060 | 1.2561 | 2.9977 |
| `lu_factor_solve/n512/b1` | 8.2939 | 3.3121 | 3.3489 |
| `lu_factor_solve/n512/b4` | 33.9585 | 9.7063 | 13.5202 |
| `lu_solve_prepared/n256/b1` | 0.0628 | 0.0600 | 0.0935 |
| `lu_solve_prepared/n256/b4` | 0.2487 | 0.1348 | 0.2993 |
| `lu_solve_prepared/n512/b1` | 0.2091 | 0.1616 | 0.3586 |
| `lu_solve_prepared/n512/b4` | 1.3032 | 0.3774 | 1.8197 |
| `qr/n256/b1` | 6.2493 | 3.0949 | 3.4303 |
| `qr/n256/b4` | 24.9169 | 12.3212 | 13.9167 |
| `qr/n512/b1` | 42.3965 | 14.5539 | 17.3838 |
| `qr/n512/b4` | 169.6406 | 58.3210 | 69.7387 |
| `rank_revealing_qr/n256/b1` | 6.7638 | 3.7798 | 3.8628 |
| `rank_revealing_qr/n256/b4` | 26.9602 | 15.9512 | 15.8422 |
| `rank_revealing_qr/n512/b1` | 47.7976 | 16.4251 | 19.1168 |
| `rank_revealing_qr/n512/b4` | 191.5139 | 67.7563 | 76.4909 |
| `solve/n256/b1` | 1.2021 | 0.7696 | 0.8137 |
| `solve/n256/b4` | 4.7957 | 3.0887 | 3.1880 |
| `solve/n512/b1` | 8.3118 | 3.4515 | 3.4236 |
| `solve/n512/b4` | 33.1747 | 13.6489 | 14.1183 |
| `svd_thin/n256/b1` | 24.1331 | 14.8767 | 14.3371 |
| `svd_thin/n256/b4` | 96.0781 | 61.1450 | 57.7100 |
| `svd_thin/n512/b1` | 151.8216 | 66.9905 | 70.9210 |
| `svd_thin/n512/b4` | 607.3406 | 270.2114 | 287.7296 |
| `svd_values/n256/b1` | 11.0364 | 10.7593 | 7.2161 |
| `svd_values/n256/b4` | 44.0872 | 43.3674 | 28.9958 |
| `svd_values/n512/b1` | 65.8789 | 41.8493 | 32.1564 |
| `svd_values/n512/b4` | 262.9867 | 167.8555 | 128.6996 |
| `triangular_solve/n256/b1` | 0.0340 | 0.0417 | 0.0459 |
| `triangular_solve/n256/b4` | 0.1484 | 0.1334 | 0.2133 |
| `triangular_solve/n512/b1` | 0.1118 | 0.0841 | 0.1476 |
| `triangular_solve/n512/b4` | 0.5047 | 0.3736 | 0.8002 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7034 | 0.4866 | 0.3397 |
| `cholesky/n256/b4` | 2.8253 | 1.9814 | 1.3288 |
| `cholesky/n512/b1` | 4.7822 | 1.8954 | 1.4506 |
| `cholesky/n512/b4` | 19.7512 | 7.9435 | 6.5132 |
| `eigh/n256/b1` | 10.2605 | 7.0488 | 19.2619 |
| `eigh/n256/b4` | 41.2777 | 27.9828 | 77.1480 |
| `eigh/n512/b1` | 63.0062 | 23.9107 | 123.8231 |
| `eigh/n512/b4` | 251.8088 | 98.2106 | 492.0041 |
| `eigvalsh/n256/b1` | 4.9828 | 5.0048 | 4.8281 |
| `eigvalsh/n256/b4` | 19.8848 | 19.8376 | 19.3684 |
| `eigvalsh/n512/b1` | 29.4776 | 17.9077 | 17.9132 |
| `eigvalsh/n512/b4` | 118.4293 | 71.9014 | 71.7062 |
| `householder_apply/n256/b1` | 3.3079 | 0.9224 | 1.7808 |
| `householder_apply/n256/b4` | 13.5649 | 3.7618 | 7.2527 |
| `householder_apply/n512/b1` | 24.6598 | 4.5532 | 8.5566 |
| `householder_apply/n512/b4` | 99.0559 | 18.4180 | 35.4887 |
| `householder_factor/n256/b1` | 2.3304 | 0.9815 | 1.5251 |
| `householder_factor/n256/b4` | 9.1570 | 3.8266 | 6.1114 |
| `householder_factor/n512/b1` | 16.5633 | 4.3569 | 6.4914 |
| `householder_factor/n512/b4` | 66.7855 | 17.7950 | 26.1572 |
| `lu/n256/b1` | 1.2656 | 0.8361 | 0.5533 |
| `lu/n256/b4` | 5.1990 | 3.4406 | 2.4597 |
| `lu/n512/b1` | 8.6939 | 3.4429 | 2.2901 |
| `lu/n512/b4` | 34.7936 | 13.3677 | 9.2566 |
| `lu_factor/n256/b1` | 1.1314 | 0.6811 | 0.4538 |
| `lu_factor/n256/b4` | 4.4243 | 2.6444 | 1.7725 |
| `lu_factor/n512/b1` | 8.0821 | 2.6267 | 1.6383 |
| `lu_factor/n512/b4` | 32.9233 | 10.6133 | 6.6626 |
| `lu_factor_solve/n256/b1` | 1.1983 | 0.7466 | 0.5451 |
| `lu_factor_solve/n256/b4` | 4.6706 | 2.9227 | 2.0883 |
| `lu_factor_solve/n512/b1` | 8.2880 | 2.7875 | 1.9844 |
| `lu_factor_solve/n512/b4` | 33.9764 | 11.3120 | 8.0098 |
| `lu_solve_prepared/n256/b1` | 0.0633 | 0.0669 | 0.1012 |
| `lu_solve_prepared/n256/b4` | 0.2610 | 0.2677 | 0.3102 |
| `lu_solve_prepared/n512/b1` | 0.2230 | 0.1697 | 0.3398 |
| `lu_solve_prepared/n512/b4` | 1.1083 | 0.8594 | 1.5016 |
| `qr/n256/b1` | 6.2134 | 3.5130 | 3.0649 |
| `qr/n256/b4` | 24.9266 | 14.0429 | 12.3750 |
| `qr/n512/b1` | 42.3597 | 12.5025 | 13.1657 |
| `qr/n512/b4` | 169.5070 | 50.0066 | 53.3940 |
| `rank_revealing_qr/n256/b1` | 6.7345 | 3.5655 | 3.5127 |
| `rank_revealing_qr/n256/b4` | 27.0202 | 15.0018 | 14.3710 |
| `rank_revealing_qr/n512/b1` | 47.6849 | 12.2835 | 14.8396 |
| `rank_revealing_qr/n512/b4` | 190.6424 | 49.0789 | 60.7305 |
| `solve/n256/b1` | 1.1978 | 0.7941 | 0.5846 |
| `solve/n256/b4` | 4.7737 | 3.0931 | 2.4179 |
| `solve/n512/b1` | 8.2834 | 2.9494 | 2.1140 |
| `solve/n512/b4` | 33.0954 | 11.6961 | 8.6953 |
| `svd_thin/n256/b1` | 23.9326 | 14.8923 | 13.3092 |
| `svd_thin/n256/b4` | 96.7717 | 59.6785 | 53.4669 |
| `svd_thin/n512/b1` | 151.7130 | 55.2407 | 59.6109 |
| `svd_thin/n512/b4` | 607.1076 | 223.6316 | 243.0830 |
| `svd_values/n256/b1` | 11.0446 | 10.8031 | 7.1705 |
| `svd_values/n256/b4` | 44.0609 | 43.2589 | 28.6206 |
| `svd_values/n512/b1` | 65.8395 | 39.7603 | 28.6059 |
| `svd_values/n512/b4` | 263.6263 | 159.8474 | 115.2044 |
| `triangular_solve/n256/b1` | 0.0338 | 0.0378 | 0.0425 |
| `triangular_solve/n256/b4` | 0.1440 | 0.1469 | 0.1984 |
| `triangular_solve/n512/b1` | 0.1140 | 0.0895 | 0.1527 |
| `triangular_solve/n512/b4` | 0.5240 | 0.4062 | 0.8074 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3240 | - | 0.5518 |
| `householder_factor/4096x256/b1` | 14.1400 | - | 23.2735 |
| `qr/1024x64/b1` | 0.9792 | - | 1.0748 |
| `qr/4096x256/b1` | 41.1271 | - | 47.3285 |
| `rank_revealing_qr/1024x64/b1` | 0.9691 | - | 1.1675 |
| `rank_revealing_qr/4096x256/b1` | 63.8931 | - | 58.2466 |
| `svd_thin/1024x64/b1` | 1.4603 | - | 1.9784 |
| `svd_thin/4096x256/b1` | 72.5500 | - | 74.4370 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3294 | 0.2681 | 0.5896 |
| `householder_factor/4096x256/b1` | 14.1292 | 6.7549 | 12.3925 |
| `qr/1024x64/b1` | 0.9833 | 0.9094 | 1.1449 |
| `qr/4096x256/b1` | 41.2658 | 20.0219 | 24.5443 |
| `rank_revealing_qr/1024x64/b1` | 0.9678 | 0.7355 | 1.2289 |
| `rank_revealing_qr/4096x256/b1` | 65.1931 | 23.7656 | 28.3765 |
| `svd_thin/1024x64/b1` | 1.4518 | 1.3917 | 1.8834 |
| `svd_thin/4096x256/b1` | 72.6106 | 40.5879 | 41.8031 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3284 | 0.2953 | 0.5933 |
| `householder_factor/4096x256/b1` | 14.1983 | 6.7274 | 10.8693 |
| `qr/1024x64/b1` | 0.9835 | 1.1421 | 1.1467 |
| `qr/4096x256/b1` | 41.1739 | 19.9044 | 22.0571 |
| `rank_revealing_qr/1024x64/b1` | 0.9656 | 0.7495 | 1.2367 |
| `rank_revealing_qr/4096x256/b1` | 65.2640 | 18.9514 | 24.4062 |
| `svd_thin/1024x64/b1` | 1.4548 | 1.6327 | 1.8705 |
| `svd_thin/4096x256/b1` | 72.3343 | 32.5489 | 37.5469 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.9854 | - | 1.0626 |
| `householder_factor/4096x256/b1` | 53.9075 | - | 69.1596 |
| `qr/1024x64/b1` | 2.8537 | - | 2.0581 |
| `qr/4096x256/b1` | 147.7680 | - | 139.2701 |
| `rank_revealing_qr/1024x64/b1` | 2.8657 | - | 2.2510 |
| `rank_revealing_qr/4096x256/b1` | 244.1628 | - | 171.8528 |
| `svd_thin/1024x64/b1` | 3.5673 | - | 3.9428 |
| `svd_thin/4096x256/b1` | 232.0080 | - | 218.4938 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0032 | 0.6573 | 0.4332 |
| `householder_factor/4096x256/b1` | 54.1647 | 21.3483 | 19.9977 |
| `qr/1024x64/b1` | 2.8499 | 1.6267 | 0.8066 |
| `qr/4096x256/b1` | 147.7095 | 57.4611 | 40.3004 |
| `rank_revealing_qr/1024x64/b1` | 2.8697 | 1.7649 | 1.0356 |
| `rank_revealing_qr/4096x256/b1` | 246.7868 | 82.0569 | 55.0831 |
| `svd_thin/1024x64/b1` | 3.5472 | 2.2666 | 2.0907 |
| `svd_thin/4096x256/b1` | 232.8151 | 103.6111 | 75.2748 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.9919 | 0.6670 | 0.3451 |
| `householder_factor/4096x256/b1` | 54.0694 | 19.3140 | 12.4666 |
| `qr/1024x64/b1` | 2.8776 | 1.7293 | 0.6243 |
| `qr/4096x256/b1` | 147.4476 | 46.3750 | 25.6903 |
| `rank_revealing_qr/1024x64/b1` | 2.8723 | 1.7123 | 0.8588 |
| `rank_revealing_qr/4096x256/b1` | 245.3667 | 52.9331 | 34.1337 |
| `svd_thin/1024x64/b1` | 3.5495 | 2.4249 | 1.8245 |
| `svd_thin/4096x256/b1` | 232.2703 | 85.0178 | 53.7931 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
