# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `9e0796cacb99e3374840e06d8ea47279e6ebf838`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
- harness commit: `73b4f7df95227aba5f47dd4af4a7054491d29d92`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-11T11:44:31.038255Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas --checkout /tmp/tl-pin2 --aa 1 --label refix`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261011T105053Z-refix/`

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
| `cholesky/n16/b1024` | 0.5011 | - | 0.6091 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1067 | - | 0.1140 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2139 | - | 0.2314 |
| `eig/n16/b1` | 0.0533 | - | 0.0405 |
| `eig/n16/b1024` | 55.9106 | - | 41.5444 |
| `eig/n4/b1` | 0.0040 | - | 0.0037 |
| `eig/n4/b1024` | 3.5287 | - | 3.2438 |
| `eig/n8/b1` | 0.0143 | - | 0.0112 |
| `eig/n8/b1024` | 13.7094 | - | 10.6127 |
| `eigh/n16/b1` | 0.0182 | - | 0.0233 |
| `eigh/n16/b1024` | 17.7970 | - | 24.1349 |
| `eigh/n4/b1` | 0.0017 | - | 0.0020 |
| `eigh/n4/b1024` | 1.4673 | - | 1.8112 |
| `eigh/n8/b1` | 0.0051 | - | 0.0065 |
| `eigh/n8/b1024` | 5.0132 | - | 6.5094 |
| `eigvals/n16/b1` | 0.0375 | - | 0.0292 |
| `eigvals/n16/b1024` | 39.1253 | - | 30.2037 |
| `eigvals/n4/b1` | 0.0024 | - | 0.0025 |
| `eigvals/n4/b1024` | 1.9043 | - | 2.0751 |
| `eigvals/n8/b1` | 0.0099 | - | 0.0086 |
| `eigvals/n8/b1024` | 9.1650 | - | 7.9676 |
| `eigvalsh/n16/b1` | 0.0133 | - | 0.0086 |
| `eigvalsh/n16/b1024` | 13.3346 | - | 8.7496 |
| `eigvalsh/n4/b1` | 0.0014 | - | 0.0011 |
| `eigvalsh/n4/b1024` | 1.1738 | - | 0.8505 |
| `eigvalsh/n8/b1` | 0.0044 | - | 0.0030 |
| `eigvalsh/n8/b1024` | 4.0191 | - | 2.7480 |
| `full_piv_lu/n16/b1` | 0.0027 | - | 0.0027 |
| `full_piv_lu/n16/b1024` | 2.1470 | - | 2.8928 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2240 | - | 0.2187 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0007 |
| `full_piv_lu/n8/b1024` | 0.6280 | - | 0.5844 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | - | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0262 | - | 3.7936 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | - | 0.0006 |
| `full_piv_lu_solve/n4/b1024` | 0.3083 | - | 0.4171 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0012 |
| `full_piv_lu_solve/n8/b1024` | 0.7363 | - | 0.9859 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0030 |
| `householder_apply/n16/b1024` | 2.6254 | - | 2.7998 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0006 |
| `householder_apply/n4/b1024` | 0.1849 | - | 0.2471 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0011 |
| `householder_apply/n8/b1024` | 0.6320 | - | 0.7205 |
| `householder_factor/n16/b1` | 0.0021 | - | 0.0027 |
| `householder_factor/n16/b1024` | 2.0848 | - | 2.6240 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.2346 | - | 0.3199 |
| `householder_factor/n8/b1` | 0.0007 | - | 0.0011 |
| `householder_factor/n8/b1024` | 0.6440 | - | 0.9007 |
| `lu/n16/b1` | 0.0020 | - | 0.0017 |
| `lu/n16/b1024` | 1.4669 | - | 1.5207 |
| `lu/n4/b1` | 0.0005 | - | 0.0003 |
| `lu/n4/b1024` | 0.1673 | - | 0.1901 |
| `lu/n8/b1` | 0.0008 | - | 0.0006 |
| `lu/n8/b1024` | 0.4625 | - | 0.4797 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0011 |
| `lu_factor/n16/b1024` | 1.0689 | - | 1.0850 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1365 | - | 0.1288 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3389 | - | 0.3399 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0019 |
| `lu_factor_solve/n16/b1024` | 1.3921 | - | 1.8706 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.1663 | - | 0.3145 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0007 |
| `lu_factor_solve/n8/b1024` | 0.4650 | - | 0.6440 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0008 |
| `lu_solve_prepared/n16/b1024` | 0.3589 | - | 0.7106 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0408 | - | 0.1890 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1375 | - | 0.3063 |
| `qr/n16/b1` | 0.0053 | - | 0.0048 |
| `qr/n16/b1024` | 5.1620 | - | 4.7281 |
| `qr/n4/b1` | 0.0007 | - | 0.0008 |
| `qr/n4/b1024` | 0.4480 | - | 0.5705 |
| `qr/n8/b1` | 0.0016 | - | 0.0018 |
| `qr/n8/b1024` | 1.3734 | - | 1.5949 |
| `rank_revealing_qr/n16/b1` | 0.0065 | - | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.1020 | - | 5.5447 |
| `rank_revealing_qr/n4/b1` | 0.0010 | - | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7091 | - | 0.6850 |
| `rank_revealing_qr/n8/b1` | 0.0022 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8506 | - | 1.8072 |
| `solve/n16/b1` | 0.0021 | - | 0.0023 |
| `solve/n16/b1024` | 1.5246 | - | 1.9648 |
| `solve/n4/b1` | 0.0006 | - | 0.0006 |
| `solve/n4/b1024` | 0.2192 | - | 0.3501 |
| `solve/n8/b1` | 0.0009 | - | 0.0009 |
| `solve/n8/b1024` | 0.5405 | - | 0.6817 |
| `svd_full/n16/b1` | 0.0329 | - | 0.0486 |
| `svd_full/n16/b1024` | 33.2973 | - | 48.7509 |
| `svd_full/n4/b1` | 0.0028 | - | 0.0043 |
| `svd_full/n4/b1024` | 2.5634 | - | 3.8302 |
| `svd_full/n8/b1` | 0.0090 | - | 0.0126 |
| `svd_full/n8/b1024` | 9.0269 | - | 12.7816 |
| `svd_thin/n16/b1` | 0.0327 | - | 0.0486 |
| `svd_thin/n16/b1024` | 33.4302 | - | 48.6017 |
| `svd_thin/n4/b1` | 0.0027 | - | 0.0043 |
| `svd_thin/n4/b1024` | 2.5506 | - | 3.8190 |
| `svd_thin/n8/b1` | 0.0091 | - | 0.0125 |
| `svd_thin/n8/b1024` | 9.0399 | - | 12.7671 |
| `svd_values/n16/b1` | 0.0238 | - | 0.0151 |
| `svd_values/n16/b1024` | 24.3875 | - | 15.0411 |
| `svd_values/n4/b1` | 0.0021 | - | 0.0026 |
| `svd_values/n4/b1024` | 1.8842 | - | 2.1059 |
| `svd_values/n8/b1` | 0.0068 | - | 0.0056 |
| `svd_values/n8/b1024` | 6.7737 | - | 5.3991 |
| `triangular_solve/n16/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3029 | - | 0.3906 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0508 | - | 0.1178 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n8/b1024` | 0.1314 | - | 0.1833 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0022 | 0.0007 |
| `cholesky/n16/b1024` | 0.5386 | 0.1385 | 0.6128 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1077 | 0.0340 | 0.1174 |
| `cholesky/n8/b1` | 0.0003 | 0.0022 | 0.0003 |
| `cholesky/n8/b1024` | 0.2158 | 0.1121 | 0.2304 |
| `eig/n16/b1` | 0.0534 | 0.0565 | 0.0408 |
| `eig/n16/b1024` | 55.8284 | 22.4238 | 41.8535 |
| `eig/n4/b1` | 0.0040 | 0.0061 | 0.0037 |
| `eig/n4/b1024` | 3.5513 | 1.8017 | 3.2560 |
| `eig/n8/b1` | 0.0144 | 0.0172 | 0.0112 |
| `eig/n8/b1024` | 13.7811 | 6.5418 | 10.6920 |
| `eigh/n16/b1` | 0.0175 | 0.0206 | 0.0232 |
| `eigh/n16/b1024` | 18.1706 | 7.5455 | 23.8389 |
| `eigh/n4/b1` | 0.0017 | 0.0044 | 0.0020 |
| `eigh/n4/b1024` | 1.4617 | 0.3685 | 1.7988 |
| `eigh/n8/b1` | 0.0051 | 0.0077 | 0.0065 |
| `eigh/n8/b1024` | 4.9978 | 2.5362 | 6.4804 |
| `eigvals/n16/b1` | 0.0370 | 0.0402 | 0.0291 |
| `eigvals/n16/b1024` | 39.1510 | 15.6519 | 29.6978 |
| `eigvals/n4/b1` | 0.0023 | 0.0045 | 0.0025 |
| `eigvals/n4/b1024` | 1.8985 | 0.9514 | 2.0496 |
| `eigvals/n8/b1` | 0.0098 | 0.0129 | 0.0086 |
| `eigvals/n8/b1024` | 9.2076 | 2.3241 | 7.9499 |
| `eigvalsh/n16/b1` | 0.0132 | 0.0161 | 0.0086 |
| `eigvalsh/n16/b1024` | 13.2937 | 4.0970 | 8.7161 |
| `eigvalsh/n4/b1` | 0.0015 | 0.0035 | 0.0011 |
| `eigvalsh/n4/b1024` | 1.1788 | 0.5955 | 0.8498 |
| `eigvalsh/n8/b1` | 0.0044 | 0.0074 | 0.0030 |
| `eigvalsh/n8/b1024` | 4.0255 | 2.0468 | 2.7336 |
| `full_piv_lu/n16/b1` | 0.0027 | 0.0050 | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.1528 | 0.5660 | 2.8619 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2234 | 0.0607 | 0.2313 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0036 | 0.0007 |
| `full_piv_lu/n8/b1024` | 0.6330 | 0.3207 | 0.5986 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0052 | 0.0038 |
| `full_piv_lu_solve/n16/b1024` | 2.0270 | 0.5303 | 3.7727 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0023 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3046 | 0.1576 | 0.5496 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0028 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7410 | 0.1971 | 1.1870 |
| `householder_apply/n16/b1` | 0.0027 | 0.0050 | 0.0030 |
| `householder_apply/n16/b1024` | 2.5992 | 0.6607 | 2.6422 |
| `householder_apply/n4/b1` | 0.0004 | 0.0026 | 0.0006 |
| `householder_apply/n4/b1024` | 0.1786 | 0.0485 | 0.2475 |
| `householder_apply/n8/b1` | 0.0007 | 0.0032 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6366 | 0.1699 | 0.7230 |
| `householder_factor/n16/b1` | 0.0021 | 0.0045 | 0.0027 |
| `householder_factor/n16/b1024` | 2.0650 | 0.5227 | 2.6478 |
| `householder_factor/n4/b1` | 0.0003 | 0.0028 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2331 | 0.0648 | 0.3206 |
| `householder_factor/n8/b1` | 0.0007 | 0.0032 | 0.0011 |
| `householder_factor/n8/b1024` | 0.6512 | 0.1690 | 0.9122 |
| `lu/n16/b1` | 0.0019 | 0.0047 | 0.0017 |
| `lu/n16/b1024` | 1.5303 | 0.7945 | 1.5033 |
| `lu/n4/b1` | 0.0005 | 0.0028 | 0.0003 |
| `lu/n4/b1024` | 0.1714 | 0.0889 | 0.1933 |
| `lu/n8/b1` | 0.0008 | 0.0034 | 0.0006 |
| `lu/n8/b1024` | 0.4691 | 0.2432 | 0.4759 |
| `lu_factor/n16/b1` | 0.0013 | 0.0037 | 0.0011 |
| `lu_factor/n16/b1024` | 1.0792 | 0.5626 | 1.0844 |
| `lu_factor/n4/b1` | 0.0003 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1349 | 0.0383 | 0.1298 |
| `lu_factor/n8/b1` | 0.0006 | 0.0022 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3455 | 0.0927 | 0.3403 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0045 | 0.0019 |
| `lu_factor_solve/n16/b1024` | 1.4330 | 0.7183 | 2.0432 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0026 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.1660 | 0.0478 | 0.7276 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0033 | 0.0011 |
| `lu_factor_solve/n8/b1024` | 0.4776 | 0.1267 | 0.9496 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0022 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3576 | 0.1041 | 0.6986 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0028 | 0.0005 |
| `lu_solve_prepared/n4/b1024` | 0.0405 | 0.0273 | 0.4918 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0027 | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.1366 | 0.0457 | 0.4601 |
| `qr/n16/b1` | 0.0054 | 0.0090 | 0.0048 |
| `qr/n16/b1024` | 5.1846 | 2.3761 | 4.6799 |
| `qr/n4/b1` | 0.0008 | 0.0024 | 0.0008 |
| `qr/n4/b1024` | 0.4288 | 0.2231 | 0.5804 |
| `qr/n8/b1` | 0.0016 | 0.0041 | 0.0018 |
| `qr/n8/b1024` | 1.3490 | 0.3573 | 1.5764 |
| `rank_revealing_qr/n16/b1` | 0.0064 | 0.0095 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.1286 | 1.5414 | 5.6253 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0032 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7035 | 0.1791 | 0.6868 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0050 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8343 | 0.9324 | 1.8155 |
| `solve/n16/b1` | 0.0021 | 0.0044 | 0.0023 |
| `solve/n16/b1024` | 1.5470 | 0.4002 | 1.9754 |
| `solve/n4/b1` | 0.0006 | 0.0022 | 0.0008 |
| `solve/n4/b1024` | 0.2176 | 0.0597 | 0.7906 |
| `solve/n8/b1` | 0.0010 | 0.0025 | 0.0011 |
| `solve/n8/b1024` | 0.5315 | 0.1392 | 1.1596 |
| `svd_full/n16/b1` | 0.0325 | 0.0357 | 0.0497 |
| `svd_full/n16/b1024` | 33.2113 | 15.8479 | 48.8730 |
| `svd_full/n4/b1` | 0.0029 | 0.0050 | 0.0043 |
| `svd_full/n4/b1024` | 2.5408 | 0.6501 | 3.8467 |
| `svd_full/n8/b1` | 0.0089 | 0.0118 | 0.0126 |
| `svd_full/n8/b1024` | 9.0066 | 2.2860 | 12.8179 |
| `svd_thin/n16/b1` | 0.0324 | 0.0355 | 0.0490 |
| `svd_thin/n16/b1024` | 33.3303 | 10.8593 | 48.6402 |
| `svd_thin/n4/b1` | 0.0027 | 0.0049 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5345 | 1.2792 | 3.8047 |
| `svd_thin/n8/b1` | 0.0089 | 0.0120 | 0.0126 |
| `svd_thin/n8/b1024` | 8.9880 | 4.5356 | 12.9923 |
| `svd_values/n16/b1` | 0.0238 | 0.0267 | 0.0150 |
| `svd_values/n16/b1024` | 24.4493 | 6.1829 | 15.3082 |
| `svd_values/n4/b1` | 0.0022 | 0.0037 | 0.0027 |
| `svd_values/n4/b1024` | 1.9020 | 0.9531 | 2.1591 |
| `svd_values/n8/b1` | 0.0068 | 0.0094 | 0.0057 |
| `svd_values/n8/b1024` | 6.7479 | 3.2457 | 5.4109 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0029 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3087 | 0.0800 | 0.6529 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0024 | 0.0005 |
| `triangular_solve/n4/b1024` | 0.0509 | 0.0290 | 0.4396 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0022 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1296 | 0.0411 | 0.5210 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0035 | 0.0007 |
| `cholesky/n16/b1024` | 0.5082 | 0.0699 | 0.6289 |
| `cholesky/n4/b1` | 0.0002 | 0.0023 | 0.0002 |
| `cholesky/n4/b1024` | 0.1056 | 0.0312 | 0.1181 |
| `cholesky/n8/b1` | 0.0003 | 0.0035 | 0.0003 |
| `cholesky/n8/b1024` | 0.2171 | 0.0357 | 0.2326 |
| `eig/n16/b1` | 0.0535 | 0.0565 | 0.0401 |
| `eig/n16/b1024` | 55.9541 | 7.0691 | 41.4450 |
| `eig/n4/b1` | 0.0041 | 0.0070 | 0.0037 |
| `eig/n4/b1024` | 3.5382 | 0.8823 | 3.2684 |
| `eig/n8/b1` | 0.0144 | 0.0171 | 0.0110 |
| `eig/n8/b1024` | 13.7495 | 1.7632 | 10.5498 |
| `eigh/n16/b1` | 0.0175 | 0.0207 | 0.0232 |
| `eigh/n16/b1024` | 18.1093 | 2.3046 | 24.1246 |
| `eigh/n4/b1` | 0.0016 | 0.0047 | 0.0020 |
| `eigh/n4/b1024` | 1.4602 | 0.3707 | 1.8196 |
| `eigh/n8/b1` | 0.0051 | 0.0075 | 0.0065 |
| `eigh/n8/b1024` | 4.9933 | 0.6356 | 6.5153 |
| `eigvals/n16/b1` | 0.0370 | 0.0404 | 0.0293 |
| `eigvals/n16/b1024` | 39.0689 | 8.0547 | 29.9956 |
| `eigvals/n4/b1` | 0.0024 | 0.0055 | 0.0025 |
| `eigvals/n4/b1024` | 1.9430 | 0.4799 | 2.0469 |
| `eigvals/n8/b1` | 0.0099 | 0.0120 | 0.0085 |
| `eigvals/n8/b1024` | 9.1630 | 1.7610 | 7.9579 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0161 | 0.0086 |
| `eigvalsh/n16/b1024` | 13.2595 | 2.3656 | 8.7838 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0042 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1812 | 0.3010 | 0.8560 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0071 | 0.0030 |
| `eigvalsh/n8/b1024` | 4.0059 | 1.0127 | 2.7430 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0057 | 0.0026 |
| `full_piv_lu/n16/b1024` | 2.1207 | 0.5374 | 2.7368 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0023 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2252 | 0.0613 | 0.2170 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0043 | 0.0007 |
| `full_piv_lu/n8/b1024` | 0.6394 | 0.0863 | 0.5888 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0050 | 0.0038 |
| `full_piv_lu_solve/n16/b1024` | 2.0177 | 0.5116 | 3.7408 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0042 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3035 | 0.0823 | 0.5692 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0039 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7314 | 0.1904 | 1.1918 |
| `householder_apply/n16/b1` | 0.0027 | 0.0052 | 0.0030 |
| `householder_apply/n16/b1024` | 2.5906 | 0.6532 | 2.6455 |
| `householder_apply/n4/b1` | 0.0003 | 0.0037 | 0.0006 |
| `householder_apply/n4/b1024` | 0.1803 | 0.0499 | 0.2477 |
| `householder_apply/n8/b1` | 0.0007 | 0.0040 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6410 | 0.1664 | 0.7196 |
| `householder_factor/n16/b1` | 0.0021 | 0.0049 | 0.0027 |
| `householder_factor/n16/b1024` | 2.0755 | 0.2764 | 2.6128 |
| `householder_factor/n4/b1` | 0.0003 | 0.0021 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2375 | 0.0637 | 0.3203 |
| `householder_factor/n8/b1` | 0.0007 | 0.0024 | 0.0010 |
| `householder_factor/n8/b1024` | 0.6564 | 0.1718 | 0.9057 |
| `lu/n16/b1` | 0.0019 | 0.0048 | 0.0017 |
| `lu/n16/b1024` | 1.5896 | 0.3792 | 1.4871 |
| `lu/n4/b1` | 0.0005 | 0.0041 | 0.0004 |
| `lu/n4/b1024` | 0.1679 | 0.0477 | 0.1952 |
| `lu/n8/b1` | 0.0008 | 0.0025 | 0.0006 |
| `lu/n8/b1024` | 0.4710 | 0.0653 | 0.4930 |
| `lu_factor/n16/b1` | 0.0013 | 0.0043 | 0.0011 |
| `lu_factor/n16/b1024` | 1.0825 | 0.2821 | 1.0945 |
| `lu_factor/n4/b1` | 0.0004 | 0.0025 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1329 | 0.0378 | 0.1304 |
| `lu_factor/n8/b1` | 0.0006 | 0.0038 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3436 | 0.0978 | 0.3421 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0047 | 0.0022 |
| `lu_factor_solve/n16/b1024` | 1.3644 | 0.3607 | 2.0339 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0040 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1684 | 0.0470 | 0.6755 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0034 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.4658 | 0.1277 | 0.8901 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0037 | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.3725 | 0.1045 | 0.6585 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0026 | 0.0005 |
| `lu_solve_prepared/n4/b1024` | 0.0405 | 0.0196 | 0.5259 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0026 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.1498 | 0.0452 | 0.4831 |
| `qr/n16/b1` | 0.0056 | 0.0085 | 0.0048 |
| `qr/n16/b1024` | 5.1296 | 1.3204 | 4.6847 |
| `qr/n4/b1` | 0.0006 | 0.0030 | 0.0008 |
| `qr/n4/b1024` | 0.4321 | 0.0626 | 0.5842 |
| `qr/n8/b1` | 0.0015 | 0.0043 | 0.0018 |
| `qr/n8/b1024` | 1.3460 | 0.3421 | 1.5751 |
| `rank_revealing_qr/n16/b1` | 0.0064 | 0.0096 | 0.0060 |
| `rank_revealing_qr/n16/b1024` | 5.9171 | 1.5161 | 5.6110 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0037 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7047 | 0.1829 | 0.6924 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0051 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8338 | 0.2331 | 1.8169 |
| `solve/n16/b1` | 0.0021 | 0.0049 | 0.0023 |
| `solve/n16/b1024` | 1.5172 | 0.3842 | 1.9660 |
| `solve/n4/b1` | 0.0006 | 0.0040 | 0.0008 |
| `solve/n4/b1024` | 0.2170 | 0.0364 | 0.8370 |
| `solve/n8/b1` | 0.0010 | 0.0030 | 0.0011 |
| `solve/n8/b1024` | 0.5388 | 0.1428 | 1.1711 |
| `svd_full/n16/b1` | 0.0334 | 0.0358 | 0.0486 |
| `svd_full/n16/b1024` | 33.4106 | 7.1527 | 48.2366 |
| `svd_full/n4/b1` | 0.0030 | 0.0059 | 0.0043 |
| `svd_full/n4/b1024` | 2.5438 | 0.3440 | 3.7993 |
| `svd_full/n8/b1` | 0.0089 | 0.0121 | 0.0125 |
| `svd_full/n8/b1024` | 9.0877 | 1.1791 | 12.7721 |
| `svd_thin/n16/b1` | 0.0325 | 0.0356 | 0.0493 |
| `svd_thin/n16/b1024` | 33.4528 | 4.2945 | 48.3179 |
| `svd_thin/n4/b1` | 0.0028 | 0.0054 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5486 | 0.3248 | 3.8077 |
| `svd_thin/n8/b1` | 0.0089 | 0.0117 | 0.0125 |
| `svd_thin/n8/b1024` | 9.1612 | 1.1879 | 12.7432 |
| `svd_values/n16/b1` | 0.0238 | 0.0267 | 0.0149 |
| `svd_values/n16/b1024` | 24.3731 | 3.0992 | 14.8946 |
| `svd_values/n4/b1` | 0.0021 | 0.0056 | 0.0026 |
| `svd_values/n4/b1024` | 1.8870 | 0.4838 | 2.0849 |
| `svd_values/n8/b1` | 0.0068 | 0.0099 | 0.0056 |
| `svd_values/n8/b1024` | 6.7785 | 1.3339 | 5.3752 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0028 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.2976 | 0.0811 | 0.6893 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0030 | 0.0005 |
| `triangular_solve/n4/b1024` | 0.0514 | 0.0157 | 0.4556 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0022 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1310 | 0.0277 | 0.5492 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0010 |
| `cholesky/n16/b1024` | 0.7928 | - | 0.9969 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1198 | - | 0.1359 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2480 | - | 0.2888 |
| `eig/n16/b1` | 0.0726 | - | 0.1002 |
| `eig/n16/b1024` | 76.4776 | - | 119.5173 |
| `eig/n4/b1` | 0.0061 | - | 0.0081 |
| `eig/n4/b1024` | 5.8815 | - | 7.9617 |
| `eig/n8/b1` | 0.0199 | - | 0.0262 |
| `eig/n8/b1024` | 20.5870 | - | 27.9621 |
| `eigh/n16/b1` | 0.0181 | - | 0.0261 |
| `eigh/n16/b1024` | 19.5732 | - | 26.9188 |
| `eigh/n4/b1` | 0.0020 | - | 0.0023 |
| `eigh/n4/b1024` | 1.7313 | - | 2.1199 |
| `eigh/n8/b1` | 0.0057 | - | 0.0073 |
| `eigh/n8/b1024` | 5.4541 | - | 7.3992 |
| `eigvals/n16/b1` | 0.0435 | - | 0.0747 |
| `eigvals/n16/b1024` | 46.5224 | - | 89.7452 |
| `eigvals/n4/b1` | 0.0032 | - | 0.0064 |
| `eigvals/n4/b1024` | 2.9853 | - | 6.0471 |
| `eigvals/n8/b1` | 0.0118 | - | 0.0210 |
| `eigvals/n8/b1024` | 12.0575 | - | 22.2519 |
| `eigvalsh/n16/b1` | 0.0136 | - | 0.0116 |
| `eigvalsh/n16/b1024` | 14.3195 | - | 11.5379 |
| `eigvalsh/n4/b1` | 0.0017 | - | 0.0016 |
| `eigvalsh/n4/b1024` | 1.4370 | - | 1.2522 |
| `eigvalsh/n8/b1` | 0.0046 | - | 0.0040 |
| `eigvalsh/n8/b1024` | 4.3917 | - | 3.6759 |
| `full_piv_lu/n16/b1` | 0.0030 | - | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.7560 | - | 20.1897 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2585 | - | 0.5421 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7249 | - | 2.3158 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | - | 0.0152 |
| `full_piv_lu_solve/n16/b1024` | 3.1284 | - | 22.5472 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4392 | - | 1.1495 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0036 |
| `full_piv_lu_solve/n8/b1024` | 1.1121 | - | 3.5780 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0046 |
| `householder_apply/n16/b1024` | 3.3207 | - | 4.4184 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0008 |
| `householder_apply/n4/b1024` | 0.1789 | - | 0.2588 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0014 |
| `householder_apply/n8/b1024` | 0.5999 | - | 0.8963 |
| `householder_factor/n16/b1` | 0.0026 | - | 0.0045 |
| `householder_factor/n16/b1024` | 2.5615 | - | 4.4467 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0007 |
| `householder_factor/n4/b1024` | 0.3041 | - | 0.5543 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0016 |
| `householder_factor/n8/b1024` | 0.8112 | - | 1.4211 |
| `lu/n16/b1` | 0.0023 | - | 0.0023 |
| `lu/n16/b1024` | 1.8287 | - | 2.5096 |
| `lu/n4/b1` | 0.0005 | - | 0.0004 |
| `lu/n4/b1024` | 0.2063 | - | 0.2310 |
| `lu/n8/b1` | 0.0009 | - | 0.0008 |
| `lu/n8/b1024` | 0.5561 | - | 0.6450 |
| `lu_factor/n16/b1` | 0.0015 | - | 0.0017 |
| `lu_factor/n16/b1024` | 1.2849 | - | 1.6266 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1649 | - | 0.1621 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0005 |
| `lu_factor/n8/b1024` | 0.4223 | - | 0.4535 |
| `lu_factor_solve/n16/b1` | 0.0024 | - | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0450 | - | 2.6652 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.2509 | - | 0.4007 |
| `lu_factor_solve/n8/b1` | 0.0010 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6871 | - | 0.9127 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.8158 | - | 1.0320 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0967 | - | 0.2415 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.2882 | - | 0.4505 |
| `qr/n16/b1` | 0.0067 | - | 0.0077 |
| `qr/n16/b1024` | 6.6800 | - | 7.6197 |
| `qr/n4/b1` | 0.0007 | - | 0.0012 |
| `qr/n4/b1024` | 0.5059 | - | 0.8499 |
| `qr/n8/b1` | 0.0019 | - | 0.0025 |
| `qr/n8/b1024` | 1.5882 | - | 2.2617 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.3243 | - | 10.1074 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8287 | - | 1.1381 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.2005 | - | 3.0205 |
| `solve/n16/b1` | 0.0028 | - | 0.0030 |
| `solve/n16/b1024` | 2.2113 | - | 2.7761 |
| `solve/n4/b1` | 0.0007 | - | 0.0007 |
| `solve/n4/b1024` | 0.3218 | - | 0.4371 |
| `solve/n8/b1` | 0.0013 | - | 0.0012 |
| `solve/n8/b1024` | 0.7763 | - | 0.9921 |
| `svd_full/n16/b1` | 0.0351 | - | 0.0550 |
| `svd_full/n16/b1024` | 36.6767 | - | 56.7653 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_full/n4/b1024` | 3.0114 | - | 4.7622 |
| `svd_full/n8/b1` | 0.0097 | - | 0.0146 |
| `svd_full/n8/b1024` | 10.1443 | - | 14.9853 |
| `svd_thin/n16/b1` | 0.0347 | - | 0.0550 |
| `svd_thin/n16/b1024` | 36.6089 | - | 56.6104 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0052 |
| `svd_thin/n4/b1024` | 3.0005 | - | 4.7178 |
| `svd_thin/n8/b1` | 0.0097 | - | 0.0145 |
| `svd_thin/n8/b1024` | 10.1988 | - | 14.9409 |
| `svd_values/n16/b1` | 0.0261 | - | 0.0198 |
| `svd_values/n16/b1024` | 27.3361 | - | 20.0361 |
| `svd_values/n4/b1` | 0.0026 | - | 0.0033 |
| `svd_values/n4/b1024` | 2.3022 | - | 2.8222 |
| `svd_values/n8/b1` | 0.0076 | - | 0.0072 |
| `svd_values/n8/b1024` | 7.7984 | - | 6.7986 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0007 |
| `triangular_solve/n16/b1024` | 0.6032 | - | 0.5857 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0965 | - | 0.1534 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.2383 | - | 0.2652 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0035 | 0.0010 |
| `cholesky/n16/b1024` | 0.7294 | 0.3765 | 0.9271 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1171 | 0.0371 | 0.1364 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2425 | 0.0659 | 0.2899 |
| `eig/n16/b1` | 0.0714 | 0.0764 | 0.1002 |
| `eig/n16/b1024` | 75.8374 | 29.2204 | 119.3245 |
| `eig/n4/b1` | 0.0061 | 0.0098 | 0.0081 |
| `eig/n4/b1024` | 5.8161 | 2.9690 | 7.9256 |
| `eig/n8/b1` | 0.0198 | 0.0230 | 0.0262 |
| `eig/n8/b1024` | 21.0054 | 7.2482 | 28.0512 |
| `eigh/n16/b1` | 0.0181 | 0.0210 | 0.0262 |
| `eigh/n16/b1024` | 19.4809 | 4.9092 | 27.3829 |
| `eigh/n4/b1` | 0.0019 | 0.0047 | 0.0024 |
| `eigh/n4/b1024` | 1.7234 | 0.8732 | 2.1278 |
| `eigh/n8/b1` | 0.0056 | 0.0090 | 0.0074 |
| `eigh/n8/b1024` | 5.4274 | 2.7492 | 7.3783 |
| `eigvals/n16/b1` | 0.0432 | 0.0466 | 0.0748 |
| `eigvals/n16/b1024` | 47.2130 | 17.1375 | 89.6717 |
| `eigvals/n4/b1` | 0.0031 | 0.0063 | 0.0064 |
| `eigvals/n4/b1024` | 2.9616 | 0.7849 | 6.0236 |
| `eigvals/n8/b1` | 0.0117 | 0.0146 | 0.0211 |
| `eigvals/n8/b1024` | 11.8628 | 5.9107 | 22.1946 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0166 | 0.0117 |
| `eigvalsh/n16/b1024` | 14.3655 | 3.6825 | 11.5355 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0040 | 0.0016 |
| `eigvalsh/n4/b1024` | 1.4523 | 0.7256 | 1.2519 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0080 | 0.0040 |
| `eigvalsh/n8/b1024` | 4.4106 | 2.2360 | 3.6819 |
| `full_piv_lu/n16/b1` | 0.0030 | 0.0060 | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.8277 | 1.1842 | 20.1633 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2539 | 0.1329 | 0.5490 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0036 | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.8128 | 0.3553 | 2.3501 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0063 | 0.0158 |
| `full_piv_lu_solve/n16/b1024` | 3.1195 | 1.3258 | 22.6418 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0033 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4449 | 0.2277 | 1.2685 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0039 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1437 | 0.5664 | 3.6941 |
| `householder_apply/n16/b1` | 0.0026 | 0.0052 | 0.0045 |
| `householder_apply/n16/b1024` | 3.1664 | 1.2555 | 4.3249 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0008 |
| `householder_apply/n4/b1024` | 0.1819 | 0.0500 | 0.2571 |
| `householder_apply/n8/b1` | 0.0007 | 0.0032 | 0.0014 |
| `householder_apply/n8/b1024` | 0.6200 | 0.1657 | 0.8900 |
| `householder_factor/n16/b1` | 0.0026 | 0.0048 | 0.0046 |
| `householder_factor/n16/b1024` | 2.5700 | 0.6575 | 4.4662 |
| `householder_factor/n4/b1` | 0.0004 | 0.0025 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3059 | 0.0864 | 0.5507 |
| `householder_factor/n8/b1` | 0.0009 | 0.0032 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8058 | 0.4063 | 1.4329 |
| `lu/n16/b1` | 0.0021 | 0.0048 | 0.0023 |
| `lu/n16/b1024` | 1.8660 | 0.9226 | 2.5458 |
| `lu/n4/b1` | 0.0005 | 0.0027 | 0.0004 |
| `lu/n4/b1024` | 0.2047 | 0.1081 | 0.2287 |
| `lu/n8/b1` | 0.0008 | 0.0037 | 0.0009 |
| `lu/n8/b1024` | 0.5322 | 0.2745 | 0.6237 |
| `lu_factor/n16/b1` | 0.0015 | 0.0039 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2277 | 0.3168 | 1.6264 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1619 | 0.0466 | 0.1619 |
| `lu_factor/n8/b1` | 0.0006 | 0.0024 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3945 | 0.2047 | 0.4574 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0042 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 1.9979 | 1.0050 | 3.0293 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0028 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2491 | 0.0682 | 0.8004 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0040 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6776 | 0.1767 | 1.4633 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0036 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7890 | 0.4000 | 1.2106 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0028 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0971 | 0.0342 | 0.5867 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0028 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2889 | 0.0841 | 0.8383 |
| `qr/n16/b1` | 0.0068 | 0.0095 | 0.0077 |
| `qr/n16/b1024` | 6.5586 | 1.6789 | 7.5987 |
| `qr/n4/b1` | 0.0007 | 0.0024 | 0.0012 |
| `qr/n4/b1024` | 0.5085 | 0.2587 | 0.8489 |
| `qr/n8/b1` | 0.0018 | 0.0042 | 0.0025 |
| `qr/n8/b1024` | 1.5632 | 0.4103 | 2.2743 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0102 | 0.0100 |
| `rank_revealing_qr/n16/b1024` | 7.2916 | 2.2511 | 10.1020 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0033 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8102 | 0.4103 | 1.1247 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0046 | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.1995 | 1.1287 | 3.0133 |
| `solve/n16/b1` | 0.0027 | 0.0059 | 0.0031 |
| `solve/n16/b1024` | 2.1475 | 0.5446 | 3.0023 |
| `solve/n4/b1` | 0.0007 | 0.0024 | 0.0009 |
| `solve/n4/b1024` | 0.3173 | 0.0876 | 0.6663 |
| `solve/n8/b1` | 0.0012 | 0.0036 | 0.0014 |
| `solve/n8/b1024` | 0.7591 | 0.1972 | 1.2125 |
| `svd_full/n16/b1` | 0.0347 | 0.0376 | 0.0552 |
| `svd_full/n16/b1024` | 37.3094 | 15.0977 | 56.5016 |
| `svd_full/n4/b1` | 0.0031 | 0.0052 | 0.0053 |
| `svd_full/n4/b1024` | 2.9980 | 1.5339 | 4.7162 |
| `svd_full/n8/b1` | 0.0097 | 0.0125 | 0.0146 |
| `svd_full/n8/b1024` | 10.1459 | 3.0630 | 14.9643 |
| `svd_thin/n16/b1` | 0.0348 | 0.0378 | 0.0551 |
| `svd_thin/n16/b1024` | 37.2470 | 15.1311 | 56.3552 |
| `svd_thin/n4/b1` | 0.0031 | 0.0055 | 0.0053 |
| `svd_thin/n4/b1024` | 2.9994 | 1.5352 | 4.7260 |
| `svd_thin/n8/b1` | 0.0097 | 0.0122 | 0.0147 |
| `svd_thin/n8/b1024` | 10.1021 | 2.6712 | 14.9754 |
| `svd_values/n16/b1` | 0.0262 | 0.0292 | 0.0197 |
| `svd_values/n16/b1024` | 27.3251 | 9.3209 | 20.0596 |
| `svd_values/n4/b1` | 0.0025 | 0.0048 | 0.0033 |
| `svd_values/n4/b1024` | 2.2980 | 0.7884 | 2.8049 |
| `svd_values/n8/b1` | 0.0076 | 0.0103 | 0.0072 |
| `svd_values/n8/b1024` | 7.7840 | 3.9243 | 6.8357 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0025 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5882 | 0.2998 | 0.8280 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0958 | 0.0292 | 0.5009 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0027 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2387 | 0.0652 | 0.6270 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0034 | 0.0010 |
| `cholesky/n16/b1024` | 0.7395 | 0.1863 | 0.9881 |
| `cholesky/n4/b1` | 0.0003 | 0.0038 | 0.0002 |
| `cholesky/n4/b1024` | 0.1171 | 0.0231 | 0.1407 |
| `cholesky/n8/b1` | 0.0004 | 0.0033 | 0.0004 |
| `cholesky/n8/b1024` | 0.2452 | 0.0431 | 0.2892 |
| `eig/n16/b1` | 0.0717 | 0.0770 | 0.1007 |
| `eig/n16/b1024` | 76.3221 | 15.7489 | 119.7992 |
| `eig/n4/b1` | 0.0060 | 0.0091 | 0.0083 |
| `eig/n4/b1024` | 5.8783 | 0.7756 | 8.0626 |
| `eig/n8/b1` | 0.0199 | 0.0230 | 0.0264 |
| `eig/n8/b1024` | 20.5467 | 2.6242 | 28.0473 |
| `eigh/n16/b1` | 0.0180 | 0.0209 | 0.0264 |
| `eigh/n16/b1024` | 19.5722 | 2.9446 | 27.2970 |
| `eigh/n4/b1` | 0.0020 | 0.0050 | 0.0025 |
| `eigh/n4/b1024` | 1.7308 | 0.4409 | 2.1824 |
| `eigh/n8/b1` | 0.0057 | 0.0091 | 0.0075 |
| `eigh/n8/b1024` | 5.4171 | 1.3867 | 7.5611 |
| `eigvals/n16/b1` | 0.0432 | 0.0467 | 0.0748 |
| `eigvals/n16/b1024` | 46.3404 | 8.8476 | 89.5929 |
| `eigvals/n4/b1` | 0.0031 | 0.0062 | 0.0064 |
| `eigvals/n4/b1024` | 2.9780 | 0.7464 | 6.1014 |
| `eigvals/n8/b1` | 0.0118 | 0.0146 | 0.0211 |
| `eigvals/n8/b1024` | 11.9505 | 1.5448 | 22.2815 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0164 | 0.0118 |
| `eigvalsh/n16/b1024` | 14.4579 | 3.5946 | 11.6049 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0053 | 0.0016 |
| `eigvalsh/n4/b1024` | 1.4456 | 0.3651 | 1.2694 |
| `eigvalsh/n8/b1` | 0.0046 | 0.0072 | 0.0041 |
| `eigvalsh/n8/b1024` | 4.3864 | 0.5550 | 3.7101 |
| `full_piv_lu/n16/b1` | 0.0030 | 0.0062 | 0.0125 |
| `full_piv_lu/n16/b1024` | 2.9016 | 0.4344 | 20.4875 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0033 | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2566 | 0.0438 | 0.5449 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0038 | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.7256 | 0.1878 | 2.2711 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0060 | 0.0154 |
| `full_piv_lu_solve/n16/b1024` | 3.1246 | 0.4107 | 22.9403 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0034 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4428 | 0.0664 | 1.2788 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0047 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1341 | 0.2927 | 3.6833 |
| `householder_apply/n16/b1` | 0.0026 | 0.0057 | 0.0046 |
| `householder_apply/n16/b1024` | 3.2539 | 0.3955 | 4.3833 |
| `householder_apply/n4/b1` | 0.0003 | 0.0025 | 0.0008 |
| `householder_apply/n4/b1024` | 0.1778 | 0.0485 | 0.2583 |
| `householder_apply/n8/b1` | 0.0007 | 0.0047 | 0.0014 |
| `householder_apply/n8/b1024` | 0.6224 | 0.1582 | 0.8930 |
| `householder_factor/n16/b1` | 0.0025 | 0.0054 | 0.0046 |
| `householder_factor/n16/b1024` | 2.6154 | 0.6532 | 4.4322 |
| `householder_factor/n4/b1` | 0.0004 | 0.0025 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3080 | 0.0628 | 0.5486 |
| `householder_factor/n8/b1` | 0.0009 | 0.0035 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8069 | 0.1121 | 1.4454 |
| `lu/n16/b1` | 0.0021 | 0.0055 | 0.0024 |
| `lu/n16/b1024` | 1.8823 | 0.2888 | 2.6345 |
| `lu/n4/b1` | 0.0005 | 0.0023 | 0.0004 |
| `lu/n4/b1024` | 0.2094 | 0.0563 | 0.2346 |
| `lu/n8/b1` | 0.0008 | 0.0041 | 0.0009 |
| `lu/n8/b1024` | 0.5292 | 0.1432 | 0.6323 |
| `lu_factor/n16/b1` | 0.0014 | 0.0049 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2482 | 0.3208 | 1.6335 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1643 | 0.0459 | 0.1652 |
| `lu_factor/n8/b1` | 0.0006 | 0.0042 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3939 | 0.1086 | 0.4553 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0050 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0050 | 0.5091 | 3.0611 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0039 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2508 | 0.0404 | 0.8293 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0042 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6783 | 0.1767 | 1.4308 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0042 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7706 | 0.2060 | 1.1601 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0023 | 0.0005 |
| `lu_solve_prepared/n4/b1024` | 0.0978 | 0.0336 | 0.5973 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0022 | 0.0006 |
| `lu_solve_prepared/n8/b1024` | 0.2904 | 0.0863 | 0.8192 |
| `qr/n16/b1` | 0.0066 | 0.0091 | 0.0079 |
| `qr/n16/b1024` | 6.5847 | 1.6738 | 7.8477 |
| `qr/n4/b1` | 0.0007 | 0.0041 | 0.0012 |
| `qr/n4/b1024` | 0.5026 | 0.0943 | 0.9418 |
| `qr/n8/b1` | 0.0019 | 0.0050 | 0.0028 |
| `qr/n8/b1024` | 1.5453 | 0.2045 | 2.4193 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0184 | 0.0101 |
| `rank_revealing_qr/n16/b1024` | 7.3257 | 1.4318 | 10.2194 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0027 | 0.0017 |
| `rank_revealing_qr/n4/b1024` | 0.8215 | 0.2098 | 1.2330 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0056 | 0.0035 |
| `rank_revealing_qr/n8/b1024` | 2.2018 | 0.3092 | 3.1903 |
| `solve/n16/b1` | 0.0027 | 0.0056 | 0.0031 |
| `solve/n16/b1024` | 2.1102 | 0.5396 | 3.1788 |
| `solve/n4/b1` | 0.0007 | 0.0033 | 0.0009 |
| `solve/n4/b1024` | 0.3467 | 0.0853 | 0.9116 |
| `solve/n8/b1` | 0.0012 | 0.0039 | 0.0014 |
| `solve/n8/b1024` | 0.7532 | 0.1975 | 1.3990 |
| `svd_full/n16/b1` | 0.0348 | 0.0377 | 0.0552 |
| `svd_full/n16/b1024` | 36.6847 | 4.6482 | 56.6076 |
| `svd_full/n4/b1` | 0.0031 | 0.0059 | 0.0054 |
| `svd_full/n4/b1024` | 3.0033 | 0.4089 | 4.7377 |
| `svd_full/n8/b1` | 0.0097 | 0.0123 | 0.0148 |
| `svd_full/n8/b1024` | 10.1030 | 1.2867 | 15.0510 |
| `svd_thin/n16/b1` | 0.0348 | 0.0378 | 0.0550 |
| `svd_thin/n16/b1024` | 36.5250 | 7.9899 | 56.3288 |
| `svd_thin/n4/b1` | 0.0031 | 0.0061 | 0.0054 |
| `svd_thin/n4/b1024` | 3.0186 | 0.3801 | 4.7743 |
| `svd_thin/n8/b1` | 0.0098 | 0.0123 | 0.0147 |
| `svd_thin/n8/b1024` | 10.1260 | 1.3344 | 15.0051 |
| `svd_values/n16/b1` | 0.0260 | 0.0290 | 0.0199 |
| `svd_values/n16/b1024` | 27.3150 | 3.5515 | 20.2404 |
| `svd_values/n4/b1` | 0.0024 | 0.0057 | 0.0034 |
| `svd_values/n4/b1024` | 2.2952 | 0.5812 | 2.8856 |
| `svd_values/n8/b1` | 0.0076 | 0.0107 | 0.0073 |
| `svd_values/n8/b1024` | 7.9154 | 1.2989 | 6.8624 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0026 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5921 | 0.1543 | 0.8281 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0038 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0963 | 0.0282 | 0.4394 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0041 | 0.0008 |
| `triangular_solve/n8/b1024` | 0.2375 | 0.0638 | 0.5353 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0372 | - | 0.0405 |
| `cholesky/n128/b128` | 5.7156 | - | 6.3271 |
| `cholesky/n32/b1` | 0.0021 | - | 0.0020 |
| `cholesky/n32/b128` | 0.2432 | - | 0.2570 |
| `eigh/n128/b1` | 1.2667 | - | 1.1225 |
| `eigh/n128/b128` | 163.2126 | - | 147.7740 |
| `eigh/n32/b1` | 0.0645 | - | 0.0788 |
| `eigh/n32/b128` | 8.6230 | - | 10.0345 |
| `eigvalsh/n128/b1` | 0.6971 | - | 0.4932 |
| `eigvalsh/n128/b128` | 90.8390 | - | 63.9239 |
| `eigvalsh/n32/b1` | 0.0492 | - | 0.0290 |
| `eigvalsh/n32/b128` | 6.4876 | - | 3.7540 |
| `householder_apply/n128/b1` | 0.3010 | - | 0.2551 |
| `householder_apply/n128/b128` | 42.8420 | - | 34.0514 |
| `householder_apply/n32/b1` | 0.0103 | - | 0.0109 |
| `householder_apply/n32/b128` | 1.3112 | - | 1.3703 |
| `householder_factor/n128/b1` | 0.1934 | - | 0.2181 |
| `householder_factor/n128/b128` | 25.3153 | - | 28.5919 |
| `householder_factor/n32/b1` | 0.0071 | - | 0.0085 |
| `householder_factor/n32/b128` | 0.9104 | - | 1.1123 |
| `lu/n128/b1` | 0.0860 | - | 0.0874 |
| `lu/n128/b128` | 11.9102 | - | 13.6316 |
| `lu/n32/b1` | 0.0052 | - | 0.0050 |
| `lu/n32/b128` | 0.5749 | - | 0.6254 |
| `lu_factor/n128/b1` | 0.0568 | - | 0.0784 |
| `lu_factor/n128/b128` | 8.1536 | - | 11.3251 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0040 |
| `lu_factor/n32/b128` | 0.3830 | - | 0.4993 |
| `lu_factor_solve/n128/b1` | 0.0627 | - | 0.0907 |
| `lu_factor_solve/n128/b128` | 8.9421 | - | 12.7094 |
| `lu_factor_solve/n32/b1` | 0.0041 | - | 0.0056 |
| `lu_factor_solve/n32/b128` | 0.4832 | - | 0.7042 |
| `lu_solve_prepared/n128/b1` | 0.0059 | - | 0.0120 |
| `lu_solve_prepared/n128/b128` | 1.7387 | - | 2.7498 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0016 |
| `lu_solve_prepared/n32/b128` | 0.1134 | - | 0.2003 |
| `qr/n128/b1` | 0.3408 | - | 0.4299 |
| `qr/n128/b128` | 44.3450 | - | 57.4153 |
| `qr/n32/b1` | 0.0208 | - | 0.0159 |
| `qr/n32/b128` | 2.6323 | - | 2.0418 |
| `rank_revealing_qr/n128/b1` | 0.3465 | - | 0.4927 |
| `rank_revealing_qr/n128/b128` | 44.9666 | - | 64.7955 |
| `rank_revealing_qr/n32/b1` | 0.0209 | - | 0.0199 |
| `rank_revealing_qr/n32/b128` | 2.6032 | - | 2.5063 |
| `solve/n128/b1` | 0.0665 | - | 0.0913 |
| `solve/n128/b128` | 8.8179 | - | 12.5726 |
| `solve/n32/b1` | 0.0047 | - | 0.0061 |
| `solve/n32/b128` | 0.5189 | - | 0.7297 |
| `svd_thin/n128/b1` | 2.4065 | - | 1.9956 |
| `svd_thin/n128/b128` | 306.8498 | - | 259.5679 |
| `svd_thin/n32/b1` | 0.1177 | - | 0.1389 |
| `svd_thin/n32/b128` | 15.2436 | - | 17.7622 |
| `svd_values/n128/b1` | 1.4124 | - | 0.8094 |
| `svd_values/n128/b128` | 181.4024 | - | 106.2578 |
| `svd_values/n32/b1` | 0.0937 | - | 0.0458 |
| `svd_values/n32/b128` | 11.9549 | - | 5.9802 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0061 |
| `triangular_solve/n128/b128` | 0.8220 | - | 1.3110 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0010 |
| `triangular_solve/n32/b128` | 0.0883 | - | 0.1093 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0370 | 0.0460 | 0.0425 |
| `cholesky/n128/b128` | 5.6535 | 6.8928 | 6.5392 |
| `cholesky/n32/b1` | 0.0018 | 0.0042 | 0.0021 |
| `cholesky/n32/b128` | 0.2367 | 0.1153 | 0.2567 |
| `eigh/n128/b1` | 1.2751 | 1.2702 | 0.9002 |
| `eigh/n128/b128` | 169.3093 | 169.9849 | 117.9655 |
| `eigh/n32/b1` | 0.0663 | 0.0699 | 0.0699 |
| `eigh/n32/b128` | 8.7946 | 2.2559 | 8.9404 |
| `eigvalsh/n128/b1` | 0.7023 | 0.7026 | 0.4818 |
| `eigvalsh/n128/b128` | 91.6359 | 90.6969 | 62.1576 |
| `eigvalsh/n32/b1` | 0.0493 | 0.0525 | 0.0290 |
| `eigvalsh/n32/b128` | 6.5064 | 1.6414 | 3.7629 |
| `householder_apply/n128/b1` | 0.3161 | 0.3248 | 0.2338 |
| `householder_apply/n128/b128` | 43.8455 | 44.3810 | 31.6690 |
| `householder_apply/n32/b1` | 0.0117 | 0.0140 | 0.0107 |
| `householder_apply/n32/b128` | 1.4703 | 0.3766 | 1.3614 |
| `householder_factor/n128/b1` | 0.2001 | 0.2073 | 0.2317 |
| `householder_factor/n128/b128` | 25.4118 | 26.0353 | 29.5868 |
| `householder_factor/n32/b1` | 0.0077 | 0.0101 | 0.0086 |
| `householder_factor/n32/b128` | 0.9859 | 0.2514 | 1.0839 |
| `lu/n128/b1` | 0.0888 | 0.1005 | 0.0876 |
| `lu/n128/b128` | 12.3283 | 13.6165 | 13.6988 |
| `lu/n32/b1` | 0.0052 | 0.0077 | 0.0050 |
| `lu/n32/b128` | 0.6027 | 0.1581 | 0.6249 |
| `lu_factor/n128/b1` | 0.0570 | 0.0710 | 0.0781 |
| `lu_factor/n128/b128` | 8.2460 | 2.4954 | 11.2172 |
| `lu_factor/n32/b1` | 0.0032 | 0.0062 | 0.0039 |
| `lu_factor/n32/b128` | 0.3901 | 0.2026 | 0.5013 |
| `lu_factor_solve/n128/b1` | 0.0624 | 0.0754 | 0.0882 |
| `lu_factor_solve/n128/b128` | 8.8983 | 2.7887 | 12.3996 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0072 | 0.0053 |
| `lu_factor_solve/n32/b128` | 0.4917 | 0.1316 | 0.7384 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0096 | 0.0074 |
| `lu_solve_prepared/n128/b128` | 1.7727 | 0.4964 | 2.0304 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0033 | 0.0011 |
| `lu_solve_prepared/n32/b128` | 0.1135 | 0.0346 | 0.1625 |
| `qr/n128/b1` | 0.3418 | 0.6236 | 0.4459 |
| `qr/n128/b128` | 43.9589 | 81.3942 | 58.9534 |
| `qr/n32/b1` | 0.0216 | 0.0433 | 0.0159 |
| `qr/n32/b128` | 2.6497 | 0.6712 | 2.0040 |
| `rank_revealing_qr/n128/b1` | 0.3448 | 0.3661 | 0.5172 |
| `rank_revealing_qr/n128/b128` | 44.3140 | 47.0819 | 67.3468 |
| `rank_revealing_qr/n32/b1` | 0.0213 | 0.0466 | 0.0197 |
| `rank_revealing_qr/n32/b128` | 2.6071 | 0.6895 | 2.4616 |
| `solve/n128/b1` | 0.0661 | 0.0820 | 0.0919 |
| `solve/n128/b128` | 8.7690 | 10.4423 | 12.3621 |
| `solve/n32/b1` | 0.0047 | 0.0081 | 0.0058 |
| `solve/n32/b128` | 0.5192 | 0.2634 | 0.7245 |
| `svd_thin/n128/b1` | 2.4064 | 1.8105 | 1.9937 |
| `svd_thin/n128/b128` | 306.6869 | 230.8931 | 260.9269 |
| `svd_thin/n32/b1` | 0.1191 | 0.1229 | 0.1385 |
| `svd_thin/n32/b128` | 15.2070 | 4.4143 | 17.6681 |
| `svd_values/n128/b1` | 1.4090 | 1.4356 | 0.8264 |
| `svd_values/n128/b128` | 180.5893 | 180.3873 | 108.4517 |
| `svd_values/n32/b1` | 0.0934 | 0.0968 | 0.0456 |
| `svd_values/n32/b128` | 12.0066 | 5.3853 | 5.9587 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0071 | 0.0039 |
| `triangular_solve/n128/b128` | 0.7680 | 0.7784 | 1.1200 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0024 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0904 | 0.0304 | 0.1058 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0351 | 0.0536 | 0.0431 |
| `cholesky/n128/b128` | 5.9351 | 6.7430 | 6.6009 |
| `cholesky/n32/b1` | 0.0021 | 0.0053 | 0.0020 |
| `cholesky/n32/b128` | 0.2565 | 0.0357 | 0.2538 |
| `eigh/n128/b1` | 1.2607 | 1.2477 | 0.8743 |
| `eigh/n128/b128` | 162.5125 | 159.9802 | 112.9583 |
| `eigh/n32/b1` | 0.0667 | 0.0710 | 0.0695 |
| `eigh/n32/b128` | 8.8335 | 2.2352 | 8.9192 |
| `eigvalsh/n128/b1` | 0.7016 | 0.7030 | 0.4753 |
| `eigvalsh/n128/b128` | 91.0982 | 90.8653 | 61.8426 |
| `eigvalsh/n32/b1` | 0.0492 | 0.0519 | 0.0293 |
| `eigvalsh/n32/b128` | 6.4465 | 1.6487 | 3.7670 |
| `householder_apply/n128/b1` | 0.3161 | 0.3229 | 0.2325 |
| `householder_apply/n128/b128` | 42.0896 | 42.9221 | 31.6898 |
| `householder_apply/n32/b1` | 0.0103 | 0.0139 | 0.0106 |
| `householder_apply/n32/b128` | 1.3581 | 0.3393 | 1.3217 |
| `householder_factor/n128/b1` | 0.1986 | 0.2035 | 0.2313 |
| `householder_factor/n128/b128` | 25.1551 | 25.5966 | 29.7529 |
| `householder_factor/n32/b1` | 0.0071 | 0.0103 | 0.0085 |
| `householder_factor/n32/b128` | 0.9096 | 0.2368 | 1.0846 |
| `lu/n128/b1` | 0.0903 | 0.1149 | 0.0878 |
| `lu/n128/b128` | 12.0108 | 15.2657 | 13.6621 |
| `lu/n32/b1` | 0.0052 | 0.0088 | 0.0051 |
| `lu/n32/b128` | 0.5824 | 0.1558 | 0.6277 |
| `lu_factor/n128/b1` | 0.0570 | 0.0838 | 0.0788 |
| `lu_factor/n128/b128` | 8.3018 | 1.4946 | 11.3343 |
| `lu_factor/n32/b1` | 0.0032 | 0.0066 | 0.0039 |
| `lu_factor/n32/b128` | 0.3866 | 0.1066 | 0.5000 |
| `lu_factor_solve/n128/b1` | 0.0614 | 0.0896 | 0.0882 |
| `lu_factor_solve/n128/b128` | 8.8861 | 1.5571 | 12.4554 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0067 | 0.0054 |
| `lu_factor_solve/n32/b128` | 0.4891 | 0.1312 | 0.7470 |
| `lu_solve_prepared/n128/b1` | 0.0058 | 0.0088 | 0.0075 |
| `lu_solve_prepared/n128/b128` | 1.8663 | 0.4815 | 2.0122 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0036 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1127 | 0.0333 | 0.1643 |
| `qr/n128/b1` | 0.3406 | 0.9459 | 0.4480 |
| `qr/n128/b128` | 43.7577 | 121.0500 | 58.6954 |
| `qr/n32/b1` | 0.0208 | 0.0657 | 0.0159 |
| `qr/n32/b128` | 2.5931 | 0.3347 | 2.0239 |
| `rank_revealing_qr/n128/b1` | 0.3490 | 0.4330 | 0.5179 |
| `rank_revealing_qr/n128/b128` | 44.9437 | 55.5096 | 67.6764 |
| `rank_revealing_qr/n32/b1` | 0.0206 | 0.0638 | 0.0196 |
| `rank_revealing_qr/n32/b128` | 2.5837 | 0.3479 | 2.4680 |
| `solve/n128/b1` | 0.0658 | 0.0918 | 0.0926 |
| `solve/n128/b128` | 8.7365 | 12.0267 | 12.3536 |
| `solve/n32/b1` | 0.0047 | 0.0080 | 0.0059 |
| `solve/n32/b128` | 0.5124 | 0.1364 | 0.7392 |
| `svd_thin/n128/b1` | 2.4155 | 1.8668 | 1.9978 |
| `svd_thin/n128/b128` | 307.2718 | 237.2641 | 261.1582 |
| `svd_thin/n32/b1` | 0.1173 | 0.1218 | 0.1396 |
| `svd_thin/n32/b128` | 15.1297 | 2.0154 | 17.7789 |
| `svd_values/n128/b1` | 1.4082 | 1.4329 | 0.8208 |
| `svd_values/n128/b128` | 180.2747 | 180.1869 | 108.2712 |
| `svd_values/n32/b1` | 0.0922 | 0.0958 | 0.0463 |
| `svd_values/n32/b128` | 11.9372 | 1.5534 | 5.9972 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0069 | 0.0039 |
| `triangular_solve/n128/b128` | 0.8308 | 0.8159 | 1.2048 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0025 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0908 | 0.0256 | 0.1041 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1078 | - | 0.1088 |
| `cholesky/n128/b128` | 15.8593 | - | 15.5014 |
| `cholesky/n32/b1` | 0.0033 | - | 0.0034 |
| `cholesky/n32/b128` | 0.4168 | - | 0.4340 |
| `eigh/n128/b1` | 1.8663 | - | 3.2653 |
| `eigh/n128/b128` | 244.0680 | - | 421.7999 |
| `eigh/n32/b1` | 0.0810 | - | 0.1085 |
| `eigh/n32/b128` | 10.5894 | - | 14.0256 |
| `eigvalsh/n128/b1` | 0.9348 | - | 0.9504 |
| `eigvalsh/n128/b128` | 122.9153 | - | 123.3355 |
| `eigvalsh/n32/b1` | 0.0527 | - | 0.0421 |
| `eigvalsh/n32/b128` | 6.9673 | - | 5.4625 |
| `householder_apply/n128/b1` | 0.6841 | - | 0.6919 |
| `householder_apply/n128/b128` | 93.2001 | - | 92.1047 |
| `householder_apply/n32/b1` | 0.0145 | - | 0.0196 |
| `householder_apply/n32/b128` | 1.8493 | - | 2.4539 |
| `householder_factor/n128/b1` | 0.4587 | - | 0.4399 |
| `householder_factor/n128/b128` | 59.3208 | - | 57.2703 |
| `householder_factor/n32/b1` | 0.0112 | - | 0.0157 |
| `householder_factor/n32/b128` | 1.4114 | - | 1.9973 |
| `lu/n128/b1` | 0.1965 | - | 0.2127 |
| `lu/n128/b128` | 27.7749 | - | 31.4152 |
| `lu/n32/b1` | 0.0078 | - | 0.0080 |
| `lu/n32/b128` | 1.0196 | - | 1.1298 |
| `lu_factor/n128/b1` | 0.1556 | - | 0.1924 |
| `lu_factor/n128/b128` | 22.1111 | - | 25.5217 |
| `lu_factor/n32/b1` | 0.0054 | - | 0.0064 |
| `lu_factor/n32/b128` | 0.6616 | - | 0.8203 |
| `lu_factor_solve/n128/b1` | 0.1743 | - | 0.2184 |
| `lu_factor_solve/n128/b128` | 24.4795 | - | 29.3056 |
| `lu_factor_solve/n32/b1` | 0.0077 | - | 0.0087 |
| `lu_factor_solve/n32/b128` | 0.9489 | - | 1.1310 |
| `lu_solve_prepared/n128/b1` | 0.0187 | - | 0.0262 |
| `lu_solve_prepared/n128/b128` | 4.2391 | - | 5.1508 |
| `lu_solve_prepared/n32/b1` | 0.0022 | - | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.2841 | - | 0.3136 |
| `qr/n128/b1` | 0.9770 | - | 0.8652 |
| `qr/n128/b128` | 126.3953 | - | 114.2135 |
| `qr/n32/b1` | 0.0423 | - | 0.0291 |
| `qr/n32/b128` | 5.3862 | - | 3.6993 |
| `rank_revealing_qr/n128/b1` | 0.9995 | - | 0.9836 |
| `rank_revealing_qr/n128/b128` | 131.7278 | - | 131.3217 |
| `rank_revealing_qr/n32/b1` | 0.0389 | - | 0.0368 |
| `rank_revealing_qr/n32/b128` | 4.9452 | - | 4.8388 |
| `solve/n128/b1` | 0.1815 | - | 0.2289 |
| `solve/n128/b128` | 23.9988 | - | 29.8327 |
| `solve/n32/b1` | 0.0085 | - | 0.0095 |
| `solve/n32/b128` | 0.9895 | - | 1.1824 |
| `svd_thin/n128/b1` | 3.9635 | - | 3.5005 |
| `svd_thin/n128/b128` | 513.0940 | - | 454.2331 |
| `svd_thin/n32/b1` | 0.1497 | - | 0.1664 |
| `svd_thin/n32/b128` | 19.6151 | - | 22.0058 |
| `svd_values/n128/b1` | 1.9410 | - | 1.3872 |
| `svd_values/n128/b128` | 251.5626 | - | 177.9991 |
| `svd_values/n32/b1` | 0.1010 | - | 0.0637 |
| `svd_values/n32/b128` | 13.3137 | - | 8.2341 |
| `triangular_solve/n128/b1` | 0.0110 | - | 0.0143 |
| `triangular_solve/n128/b128` | 2.2443 | - | 2.9624 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0013 |
| `triangular_solve/n32/b128` | 0.1894 | - | 0.1584 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1060 | 0.1058 | 0.0766 |
| `cholesky/n128/b128` | 15.8685 | 15.6544 | 11.3107 |
| `cholesky/n32/b1` | 0.0032 | 0.0048 | 0.0034 |
| `cholesky/n32/b128` | 0.3940 | 0.2041 | 0.4400 |
| `eigh/n128/b1` | 1.8482 | 1.7472 | 3.1605 |
| `eigh/n128/b128` | 242.1623 | 208.9983 | 409.3174 |
| `eigh/n32/b1` | 0.0805 | 0.0850 | 0.1087 |
| `eigh/n32/b128` | 10.5242 | 2.6656 | 14.0149 |
| `eigvalsh/n128/b1` | 0.9279 | 0.9364 | 0.8888 |
| `eigvalsh/n128/b128` | 121.8968 | 122.3744 | 115.8702 |
| `eigvalsh/n32/b1` | 0.0524 | 0.0558 | 0.0419 |
| `eigvalsh/n32/b128` | 6.9079 | 2.3209 | 5.4418 |
| `householder_apply/n128/b1` | 0.6982 | 0.6963 | 0.3682 |
| `householder_apply/n128/b128` | 92.0398 | 93.2293 | 50.8398 |
| `householder_apply/n32/b1` | 0.0144 | 0.0171 | 0.0198 |
| `householder_apply/n32/b128` | 1.8347 | 0.9139 | 2.4902 |
| `householder_factor/n128/b1` | 0.4589 | 0.4611 | 0.3862 |
| `householder_factor/n128/b128` | 59.1960 | 59.5714 | 50.7457 |
| `householder_factor/n32/b1` | 0.0113 | 0.0141 | 0.0158 |
| `householder_factor/n32/b128` | 1.4671 | 0.3646 | 2.0085 |
| `lu/n128/b1` | 0.1959 | 0.1862 | 0.1455 |
| `lu/n128/b128` | 27.7943 | 25.9297 | 22.0283 |
| `lu/n32/b1` | 0.0077 | 0.0107 | 0.0080 |
| `lu/n32/b128` | 1.0127 | 0.5043 | 1.1101 |
| `lu_factor/n128/b1` | 0.1580 | 0.1449 | 0.1185 |
| `lu_factor/n128/b128` | 22.0553 | 6.2835 | 15.5175 |
| `lu_factor/n32/b1` | 0.0056 | 0.0093 | 0.0064 |
| `lu_factor/n32/b128` | 0.6835 | 0.1783 | 0.8278 |
| `lu_factor_solve/n128/b1` | 0.1758 | 0.1642 | 0.1377 |
| `lu_factor_solve/n128/b128` | 24.4630 | 6.5207 | 18.1013 |
| `lu_factor_solve/n32/b1` | 0.0077 | 0.0111 | 0.0086 |
| `lu_factor_solve/n32/b128` | 0.9477 | 0.4875 | 1.1422 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0222 | 0.0181 |
| `lu_solve_prepared/n128/b128` | 4.3164 | 1.5398 | 4.0687 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0039 | 0.0020 |
| `lu_solve_prepared/n32/b128` | 0.2841 | 0.0760 | 0.2571 |
| `qr/n128/b1` | 0.9686 | 0.8524 | 0.7693 |
| `qr/n128/b128` | 124.7811 | 113.1025 | 100.8270 |
| `qr/n32/b1` | 0.0430 | 0.0672 | 0.0288 |
| `qr/n32/b128` | 5.4614 | 1.6627 | 3.6720 |
| `rank_revealing_qr/n128/b1` | 1.0101 | 0.7964 | 0.9024 |
| `rank_revealing_qr/n128/b128` | 130.0847 | 103.5896 | 121.0410 |
| `rank_revealing_qr/n32/b1` | 0.0388 | 0.0668 | 0.0366 |
| `rank_revealing_qr/n32/b128` | 5.0290 | 1.2590 | 4.8458 |
| `solve/n128/b1` | 0.1811 | 0.1705 | 0.1485 |
| `solve/n128/b128` | 23.9735 | 22.0622 | 19.7711 |
| `solve/n32/b1` | 0.0084 | 0.0113 | 0.0094 |
| `solve/n32/b128` | 0.9875 | 0.4981 | 1.2075 |
| `svd_thin/n128/b1` | 3.9778 | 2.7728 | 3.0212 |
| `svd_thin/n128/b128` | 516.0109 | 358.4680 | 391.1972 |
| `svd_thin/n32/b1` | 0.1514 | 0.1552 | 0.1672 |
| `svd_thin/n32/b128` | 19.8271 | 8.0520 | 22.0472 |
| `svd_values/n128/b1` | 1.9352 | 1.9722 | 1.5070 |
| `svd_values/n128/b128` | 251.4815 | 251.4747 | 193.6719 |
| `svd_values/n32/b1` | 0.1016 | 0.1048 | 0.0637 |
| `svd_values/n32/b128` | 13.3844 | 6.3183 | 8.2267 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0138 | 0.0089 |
| `triangular_solve/n128/b128` | 2.3540 | 2.3111 | 2.5487 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0038 | 0.0013 |
| `triangular_solve/n32/b128` | 0.1919 | 0.0970 | 0.1541 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1080 | 0.1169 | 0.0970 |
| `cholesky/n128/b128` | 15.9529 | 16.4721 | 13.7529 |
| `cholesky/n32/b1` | 0.0032 | 0.0064 | 0.0034 |
| `cholesky/n32/b128` | 0.4012 | 0.0556 | 0.4377 |
| `eigh/n128/b1` | 1.8566 | 1.6340 | 3.1606 |
| `eigh/n128/b128` | 241.8642 | 213.1661 | 409.0556 |
| `eigh/n32/b1` | 0.0804 | 0.0857 | 0.1084 |
| `eigh/n32/b128` | 10.5177 | 1.3880 | 13.9871 |
| `eigvalsh/n128/b1` | 0.9295 | 0.9391 | 0.8883 |
| `eigvalsh/n128/b128` | 122.0564 | 122.3564 | 115.2005 |
| `eigvalsh/n32/b1` | 0.0523 | 0.0571 | 0.0422 |
| `eigvalsh/n32/b128` | 6.9003 | 1.7568 | 5.4567 |
| `householder_apply/n128/b1` | 0.6882 | 0.6914 | 0.3233 |
| `householder_apply/n128/b128` | 92.8003 | 93.1496 | 45.0990 |
| `householder_apply/n32/b1` | 0.0143 | 0.0175 | 0.0195 |
| `householder_apply/n32/b128` | 1.8504 | 0.4667 | 2.4372 |
| `householder_factor/n128/b1` | 0.4590 | 0.4616 | 0.3806 |
| `householder_factor/n128/b128` | 59.3450 | 59.6981 | 49.2943 |
| `householder_factor/n32/b1` | 0.0112 | 0.0140 | 0.0159 |
| `householder_factor/n32/b128` | 1.4181 | 0.3584 | 2.0038 |
| `lu/n128/b1` | 0.1968 | 0.1949 | 0.1405 |
| `lu/n128/b128` | 27.8641 | 27.4121 | 21.5570 |
| `lu/n32/b1` | 0.0079 | 0.0107 | 0.0080 |
| `lu/n32/b128` | 1.0363 | 0.2347 | 1.1227 |
| `lu_factor/n128/b1` | 0.1575 | 0.1566 | 0.1153 |
| `lu_factor/n128/b128` | 21.9734 | 3.4073 | 14.7889 |
| `lu_factor/n32/b1` | 0.0055 | 0.0081 | 0.0065 |
| `lu_factor/n32/b128` | 0.6551 | 0.1762 | 0.8207 |
| `lu_factor_solve/n128/b1` | 0.1754 | 0.1766 | 0.1340 |
| `lu_factor_solve/n128/b128` | 24.4188 | 3.6857 | 17.4169 |
| `lu_factor_solve/n32/b1` | 0.0077 | 0.0197 | 0.0085 |
| `lu_factor_solve/n32/b128` | 0.9346 | 0.2457 | 1.1430 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0220 | 0.0180 |
| `lu_solve_prepared/n128/b128` | 4.4064 | 0.7962 | 4.1245 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0059 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2811 | 0.0473 | 0.2579 |
| `qr/n128/b1` | 0.9586 | 1.2036 | 0.7557 |
| `qr/n128/b128` | 124.9191 | 156.2308 | 100.3067 |
| `qr/n32/b1` | 0.0423 | 0.0889 | 0.0287 |
| `qr/n32/b128` | 5.3677 | 0.7254 | 3.6419 |
| `rank_revealing_qr/n128/b1` | 1.0036 | 0.8830 | 0.8935 |
| `rank_revealing_qr/n128/b128` | 130.5799 | 114.1149 | 120.4784 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0885 | 0.0368 |
| `rank_revealing_qr/n32/b128` | 4.9264 | 0.6277 | 4.8652 |
| `solve/n128/b1` | 0.1815 | 0.1811 | 0.1457 |
| `solve/n128/b128` | 24.0270 | 23.6382 | 19.3221 |
| `solve/n32/b1` | 0.0083 | 0.0108 | 0.0096 |
| `solve/n32/b128` | 0.9845 | 0.2510 | 1.1930 |
| `svd_thin/n128/b1` | 3.9655 | 2.8126 | 2.9918 |
| `svd_thin/n128/b128` | 512.6016 | 364.3591 | 386.2955 |
| `svd_thin/n32/b1` | 0.1501 | 0.1556 | 0.1672 |
| `svd_thin/n32/b128` | 19.5620 | 2.5431 | 22.1936 |
| `svd_values/n128/b1` | 1.9376 | 1.9667 | 1.5441 |
| `svd_values/n128/b128` | 250.8745 | 250.4750 | 199.9576 |
| `svd_values/n32/b1` | 0.1008 | 0.1050 | 0.0641 |
| `svd_values/n32/b128` | 13.2590 | 3.3516 | 8.3007 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0136 | 0.0081 |
| `triangular_solve/n128/b128` | 2.2209 | 2.2377 | 2.5470 |
| `triangular_solve/n32/b1` | 0.0015 | 0.0048 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1899 | 0.0343 | 0.1717 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1920 | - | 0.2322 |
| `cholesky/n256/b4` | 0.7837 | - | 0.9327 |
| `cholesky/n512/b1` | 1.2487 | - | 1.5753 |
| `cholesky/n512/b4` | 5.7402 | - | 6.6171 |
| `eigh/n256/b1` | 5.5949 | - | 5.4062 |
| `eigh/n256/b4` | 22.4823 | - | 21.6208 |
| `eigh/n512/b1` | 28.8806 | - | 30.3971 |
| `eigh/n512/b4` | 115.9058 | - | 121.8535 |
| `eigvalsh/n256/b1` | 2.9614 | - | 2.5170 |
| `eigvalsh/n256/b4` | 12.0727 | - | 9.8565 |
| `eigvalsh/n512/b1` | 14.1469 | - | 14.4110 |
| `eigvalsh/n512/b4` | 57.5297 | - | 57.6248 |
| `householder_apply/n256/b1` | 2.2938 | - | 1.6446 |
| `householder_apply/n256/b4` | 9.7712 | - | 6.6920 |
| `householder_apply/n512/b1` | 18.9328 | - | 11.8186 |
| `householder_apply/n512/b4` | 82.7848 | - | 47.7093 |
| `householder_factor/n256/b1` | 1.4740 | - | 1.0955 |
| `householder_factor/n256/b4` | 5.9476 | - | 4.3892 |
| `householder_factor/n512/b1` | 12.0936 | - | 7.4496 |
| `householder_factor/n512/b4` | 49.0594 | - | 29.8304 |
| `lu/n256/b1` | 0.4684 | - | 0.4833 |
| `lu/n256/b4` | 1.9405 | - | 2.0642 |
| `lu/n512/b1` | 3.1964 | - | 3.1860 |
| `lu/n512/b4` | 12.9455 | - | 13.0875 |
| `lu_factor/n256/b1` | 0.3548 | - | 0.4447 |
| `lu_factor/n256/b4` | 1.5241 | - | 1.7844 |
| `lu_factor/n512/b1` | 2.8232 | - | 2.8912 |
| `lu_factor/n512/b4` | 11.7647 | - | 11.8345 |
| `lu_factor_solve/n256/b1` | 0.3694 | - | 0.4866 |
| `lu_factor_solve/n256/b4` | 1.4946 | - | 1.9483 |
| `lu_factor_solve/n512/b1` | 2.8853 | - | 3.0310 |
| `lu_factor_solve/n512/b4` | 12.0080 | - | 12.3823 |
| `lu_solve_prepared/n256/b1` | 0.0173 | - | 0.0407 |
| `lu_solve_prepared/n256/b4` | 0.0777 | - | 0.1916 |
| `lu_solve_prepared/n512/b1` | 0.0623 | - | 0.1443 |
| `lu_solve_prepared/n512/b4` | 0.4384 | - | 0.9966 |
| `qr/n256/b1` | 1.8467 | - | 2.1746 |
| `qr/n256/b4` | 7.3853 | - | 8.7808 |
| `qr/n512/b1` | 11.4990 | - | 14.8158 |
| `qr/n512/b4` | 46.0075 | - | 60.2406 |
| `rank_revealing_qr/n256/b1` | 2.1089 | - | 2.6183 |
| `rank_revealing_qr/n256/b4` | 8.4611 | - | 10.6199 |
| `rank_revealing_qr/n512/b1` | 14.7763 | - | 18.7258 |
| `rank_revealing_qr/n512/b4` | 59.2333 | - | 75.5092 |
| `solve/n256/b1` | 0.3889 | - | 0.4914 |
| `solve/n256/b4` | 1.5574 | - | 1.9875 |
| `solve/n512/b1` | 2.8474 | - | 3.0570 |
| `solve/n512/b4` | 11.3262 | - | 12.3558 |
| `svd_thin/n256/b1` | 12.1963 | - | 10.9388 |
| `svd_thin/n256/b4` | 48.7659 | - | 44.1396 |
| `svd_thin/n512/b1` | 70.6374 | - | 72.3951 |
| `svd_thin/n512/b4` | 282.3507 | - | 291.2563 |
| `svd_values/n256/b1` | 6.9542 | - | 4.5753 |
| `svd_values/n256/b4` | 27.6626 | - | 18.6247 |
| `svd_values/n512/b1` | 38.5565 | - | 31.0300 |
| `svd_values/n512/b4` | 154.0071 | - | 126.8929 |
| `triangular_solve/n256/b1` | 0.0106 | - | 0.0203 |
| `triangular_solve/n256/b4` | 0.0457 | - | 0.0843 |
| `triangular_solve/n512/b1` | 0.0340 | - | 0.0750 |
| `triangular_solve/n512/b4` | 0.1363 | - | 0.3270 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1965 | 0.1831 | 0.1578 |
| `cholesky/n256/b4` | 0.7976 | 0.7686 | 0.6384 |
| `cholesky/n512/b1` | 1.2510 | 0.7938 | 0.7663 |
| `cholesky/n512/b4` | 5.5682 | 3.5992 | 3.4182 |
| `eigh/n256/b1` | 5.6074 | 4.2445 | 3.6086 |
| `eigh/n256/b4` | 22.5296 | 17.0211 | 14.4324 |
| `eigh/n512/b1` | 29.0258 | 16.0080 | 16.3610 |
| `eigh/n512/b4` | 116.5196 | 64.9473 | 65.9593 |
| `eigvalsh/n256/b1` | 2.9555 | 2.9771 | 1.9160 |
| `eigvalsh/n256/b4` | 11.8200 | 11.9663 | 7.7085 |
| `eigvalsh/n512/b1` | 14.5528 | 11.9329 | 7.4965 |
| `eigvalsh/n512/b4` | 57.8253 | 47.8722 | 30.3090 |
| `householder_apply/n256/b1` | 2.3277 | 2.3693 | 1.0962 |
| `householder_apply/n256/b4` | 9.7408 | 9.8173 | 4.5129 |
| `householder_apply/n512/b1` | 18.9475 | 19.0044 | 6.9397 |
| `householder_apply/n512/b4` | 83.2896 | 83.4499 | 27.9545 |
| `householder_factor/n256/b1` | 1.4823 | 1.5136 | 0.8480 |
| `householder_factor/n256/b4` | 5.9653 | 6.0251 | 3.4360 |
| `householder_factor/n512/b1` | 12.0700 | 12.1204 | 4.5056 |
| `householder_factor/n512/b4` | 48.5803 | 48.7369 | 18.3731 |
| `lu/n256/b1` | 0.4782 | 0.4496 | 0.2853 |
| `lu/n256/b4` | 1.9533 | 1.8879 | 1.2488 |
| `lu/n512/b1` | 3.2365 | 1.9861 | 1.6741 |
| `lu/n512/b4` | 12.7195 | 7.9095 | 6.9335 |
| `lu_factor/n256/b1` | 0.3541 | 0.3084 | 0.2399 |
| `lu_factor/n256/b4` | 1.5258 | 0.7757 | 0.9709 |
| `lu_factor/n512/b1` | 2.8292 | 1.4660 | 1.3652 |
| `lu_factor/n512/b4` | 11.7530 | 3.7437 | 5.5595 |
| `lu_factor_solve/n256/b1` | 0.3699 | 0.3336 | 0.2694 |
| `lu_factor_solve/n256/b4` | 1.4864 | 0.7625 | 1.0946 |
| `lu_factor_solve/n512/b1` | 2.8856 | 1.5363 | 1.4743 |
| `lu_factor_solve/n512/b4` | 12.0716 | 5.7538 | 6.1214 |
| `lu_solve_prepared/n256/b1` | 0.0170 | 0.0234 | 0.0281 |
| `lu_solve_prepared/n256/b4` | 0.0792 | 0.0225 | 0.1303 |
| `lu_solve_prepared/n512/b1` | 0.0712 | 0.0690 | 0.0962 |
| `lu_solve_prepared/n512/b4` | 0.4466 | 0.1993 | 0.8606 |
| `qr/n256/b1` | 1.8426 | 1.7018 | 1.6851 |
| `qr/n256/b4` | 7.3725 | 6.7720 | 6.7914 |
| `qr/n512/b1` | 11.4578 | 6.0928 | 9.0240 |
| `qr/n512/b4` | 45.9999 | 24.0465 | 36.8206 |
| `rank_revealing_qr/n256/b1` | 2.0885 | 1.4953 | 2.3159 |
| `rank_revealing_qr/n256/b4` | 8.3651 | 5.9682 | 9.3854 |
| `rank_revealing_qr/n512/b1` | 14.9068 | 6.2848 | 14.7491 |
| `rank_revealing_qr/n512/b4` | 60.2277 | 25.1582 | 58.9802 |
| `solve/n256/b1` | 0.3861 | 0.3559 | 0.2861 |
| `solve/n256/b4` | 1.5414 | 1.4336 | 1.1533 |
| `solve/n512/b1` | 2.8482 | 1.5596 | 1.5389 |
| `solve/n512/b4` | 11.3824 | 6.2705 | 6.2039 |
| `svd_thin/n256/b1` | 12.2530 | 8.7356 | 9.3867 |
| `svd_thin/n256/b4` | 48.9221 | 35.8397 | 37.5238 |
| `svd_thin/n512/b1` | 70.8972 | 40.4867 | 54.3236 |
| `svd_thin/n512/b4` | 282.6523 | 160.4537 | 220.4524 |
| `svd_values/n256/b1` | 6.9385 | 7.0618 | 4.4268 |
| `svd_values/n256/b4` | 27.6035 | 27.9957 | 17.9923 |
| `svd_values/n512/b1` | 38.6377 | 31.8979 | 28.5946 |
| `svd_values/n512/b4` | 154.3161 | 126.8593 | 116.2706 |
| `triangular_solve/n256/b1` | 0.0105 | 0.0157 | 0.0130 |
| `triangular_solve/n256/b4` | 0.0453 | 0.0579 | 0.0613 |
| `triangular_solve/n512/b1` | 0.0337 | 0.0358 | 0.0508 |
| `triangular_solve/n512/b4` | 0.1580 | 0.1492 | 0.2466 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1987 | 0.1983 | 0.1596 |
| `cholesky/n256/b4` | 0.7953 | 0.7973 | 0.6523 |
| `cholesky/n512/b1` | 1.3189 | 0.7304 | 0.6962 |
| `cholesky/n512/b4` | 5.6252 | 3.2604 | 3.0894 |
| `eigh/n256/b1` | 5.7073 | 4.3780 | 3.3125 |
| `eigh/n256/b4` | 22.5785 | 16.8354 | 13.4915 |
| `eigh/n512/b1` | 28.7125 | 14.5683 | 14.1379 |
| `eigh/n512/b4` | 116.1507 | 59.6250 | 56.4540 |
| `eigvalsh/n256/b1` | 2.9199 | 2.9428 | 1.8706 |
| `eigvalsh/n256/b4` | 12.0095 | 11.8489 | 7.4661 |
| `eigvalsh/n512/b1` | 14.0841 | 11.4079 | 6.7663 |
| `eigvalsh/n512/b4` | 56.8207 | 46.2521 | 27.1420 |
| `householder_apply/n256/b1` | 2.3384 | 2.3800 | 1.0572 |
| `householder_apply/n256/b4` | 9.7593 | 9.8117 | 4.1917 |
| `householder_apply/n512/b1` | 18.7836 | 18.8899 | 5.9148 |
| `householder_apply/n512/b4` | 82.7623 | 82.7741 | 24.3540 |
| `householder_factor/n256/b1` | 1.4714 | 1.5139 | 0.8381 |
| `householder_factor/n256/b4` | 5.9192 | 5.9555 | 3.3031 |
| `householder_factor/n512/b1` | 12.1207 | 12.1166 | 4.0756 |
| `householder_factor/n512/b4` | 48.6441 | 48.5613 | 16.3321 |
| `lu/n256/b1` | 0.4787 | 0.4667 | 0.2516 |
| `lu/n256/b4` | 1.9873 | 1.9380 | 1.1069 |
| `lu/n512/b1` | 3.2453 | 1.9664 | 1.1555 |
| `lu/n512/b4` | 12.8106 | 7.8446 | 4.8206 |
| `lu_factor/n256/b1` | 0.3768 | 0.3599 | 0.2046 |
| `lu_factor/n256/b4` | 1.5135 | 1.4750 | 0.8228 |
| `lu_factor/n512/b1` | 2.8460 | 1.5196 | 0.8495 |
| `lu_factor/n512/b4` | 11.7472 | 6.2733 | 3.4448 |
| `lu_factor_solve/n256/b1` | 0.3952 | 0.4032 | 0.2379 |
| `lu_factor_solve/n256/b4` | 1.4826 | 1.4655 | 0.9421 |
| `lu_factor_solve/n512/b1` | 2.9074 | 1.6242 | 0.9833 |
| `lu_factor_solve/n512/b4` | 12.0371 | 6.5843 | 3.9630 |
| `lu_solve_prepared/n256/b1` | 0.0174 | 0.0276 | 0.0283 |
| `lu_solve_prepared/n256/b4` | 0.0742 | 0.1053 | 0.1249 |
| `lu_solve_prepared/n512/b1` | 0.0730 | 0.0778 | 0.1127 |
| `lu_solve_prepared/n512/b4` | 0.3789 | 0.3829 | 0.7724 |
| `qr/n256/b1` | 1.8546 | 2.4311 | 1.6723 |
| `qr/n256/b4` | 7.4222 | 9.8264 | 6.7512 |
| `qr/n512/b1` | 11.5389 | 7.0562 | 8.1049 |
| `qr/n512/b4` | 46.0748 | 27.5989 | 32.7426 |
| `rank_revealing_qr/n256/b1` | 2.0957 | 1.5603 | 2.3078 |
| `rank_revealing_qr/n256/b4` | 8.4641 | 6.2238 | 9.3001 |
| `rank_revealing_qr/n512/b1` | 14.8998 | 5.9552 | 14.0076 |
| `rank_revealing_qr/n512/b4` | 59.7695 | 23.4185 | 56.5404 |
| `solve/n256/b1` | 0.3834 | 0.4215 | 0.2516 |
| `solve/n256/b4` | 1.5439 | 1.6200 | 1.0040 |
| `solve/n512/b1` | 2.8468 | 1.7441 | 1.0316 |
| `solve/n512/b4` | 11.3487 | 6.5765 | 4.2782 |
| `svd_thin/n256/b1` | 12.2624 | 9.1490 | 9.2334 |
| `svd_thin/n256/b4` | 49.0221 | 36.8160 | 37.0625 |
| `svd_thin/n512/b1` | 71.2041 | 38.4089 | 53.0054 |
| `svd_thin/n512/b4` | 284.9110 | 153.6789 | 213.9110 |
| `svd_values/n256/b1` | 6.9510 | 7.1795 | 4.4536 |
| `svd_values/n256/b4` | 27.7046 | 28.5729 | 18.1080 |
| `svd_values/n512/b1` | 38.6271 | 32.3358 | 28.2386 |
| `svd_values/n512/b4` | 153.8247 | 128.8631 | 117.1648 |
| `triangular_solve/n256/b1` | 0.0105 | 0.0189 | 0.0129 |
| `triangular_solve/n256/b4` | 0.0456 | 0.0635 | 0.0629 |
| `triangular_solve/n512/b1` | 0.0357 | 0.0439 | 0.0547 |
| `triangular_solve/n512/b4` | 0.1686 | 0.1828 | 0.3056 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7044 | - | 0.7714 |
| `cholesky/n256/b4` | 2.7874 | - | 3.0702 |
| `cholesky/n512/b1` | 4.7003 | - | 5.4210 |
| `cholesky/n512/b4` | 19.6855 | - | 22.7249 |
| `eigh/n256/b1` | 10.2624 | - | 21.4899 |
| `eigh/n256/b4` | 41.4420 | - | 86.4343 |
| `eigh/n512/b1` | 63.1481 | - | 157.0438 |
| `eigh/n512/b4` | 252.5168 | - | 630.9449 |
| `eigvalsh/n256/b1` | 5.0011 | - | 5.6679 |
| `eigvalsh/n256/b4` | 20.0224 | - | 22.6428 |
| `eigvalsh/n512/b1` | 29.9522 | - | 37.4467 |
| `eigvalsh/n512/b4` | 119.8531 | - | 150.4822 |
| `householder_apply/n256/b1` | 5.2912 | - | 4.7336 |
| `householder_apply/n256/b4` | 21.8547 | - | 19.2060 |
| `householder_apply/n512/b1` | 45.1270 | - | 32.1587 |
| `householder_apply/n512/b4` | 181.4772 | - | 129.1787 |
| `householder_factor/n256/b1` | 3.4768 | - | 3.0066 |
| `householder_factor/n256/b4` | 14.0922 | - | 12.0829 |
| `householder_factor/n512/b1` | 29.3993 | - | 20.8467 |
| `householder_factor/n512/b4` | 119.0001 | - | 83.7632 |
| `lu/n256/b1` | 1.2479 | - | 1.4220 |
| `lu/n256/b4` | 5.1437 | - | 6.0369 |
| `lu/n512/b1` | 8.6880 | - | 10.2534 |
| `lu/n512/b4` | 34.7404 | - | 41.2186 |
| `lu_factor/n256/b1` | 1.1224 | - | 1.3319 |
| `lu_factor/n256/b4` | 4.5260 | - | 5.3426 |
| `lu_factor/n512/b1` | 8.0305 | - | 9.5155 |
| `lu_factor/n512/b4` | 32.7978 | - | 38.2409 |
| `lu_factor_solve/n256/b1` | 1.1796 | - | 1.4588 |
| `lu_factor_solve/n256/b4` | 4.7797 | - | 5.8037 |
| `lu_factor_solve/n512/b1` | 8.2637 | - | 10.0130 |
| `lu_factor_solve/n512/b4` | 33.8399 | - | 40.1448 |
| `lu_solve_prepared/n256/b1` | 0.0635 | - | 0.1218 |
| `lu_solve_prepared/n256/b4` | 0.2628 | - | 0.4483 |
| `lu_solve_prepared/n512/b1` | 0.2094 | - | 0.5110 |
| `lu_solve_prepared/n512/b4` | 1.3257 | - | 1.9512 |
| `qr/n256/b1` | 6.2507 | - | 6.0301 |
| `qr/n256/b4` | 24.9358 | - | 24.1928 |
| `qr/n512/b1` | 42.2953 | - | 41.7773 |
| `qr/n512/b4` | 169.5241 | - | 168.2994 |
| `rank_revealing_qr/n256/b1` | 6.7750 | - | 6.4366 |
| `rank_revealing_qr/n256/b4` | 27.0580 | - | 25.9967 |
| `rank_revealing_qr/n512/b1` | 47.6352 | - | 44.8107 |
| `rank_revealing_qr/n512/b4` | 191.6111 | - | 180.5581 |
| `solve/n256/b1` | 1.1761 | - | 1.4843 |
| `solve/n256/b4` | 4.7349 | - | 5.9443 |
| `solve/n512/b1` | 8.2492 | - | 10.0228 |
| `solve/n512/b4` | 32.9113 | - | 40.5435 |
| `svd_thin/n256/b1` | 24.5404 | - | 22.5166 |
| `svd_thin/n256/b4` | 98.9960 | - | 89.9727 |
| `svd_thin/n512/b1` | 154.8270 | - | 144.5525 |
| `svd_thin/n512/b4` | 619.1495 | - | 576.7220 |
| `svd_values/n256/b1` | 11.4870 | - | 9.6994 |
| `svd_values/n256/b4` | 46.2439 | - | 38.8442 |
| `svd_values/n512/b1` | 68.1561 | - | 59.7048 |
| `svd_values/n512/b4` | 272.8307 | - | 239.4365 |
| `triangular_solve/n256/b1` | 0.0341 | - | 0.0655 |
| `triangular_solve/n256/b4` | 0.1379 | - | 0.2605 |
| `triangular_solve/n512/b1` | 0.1118 | - | 0.2254 |
| `triangular_solve/n512/b4` | 0.5074 | - | 0.8678 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7046 | 0.4992 | 0.3694 |
| `cholesky/n256/b4` | 2.7735 | 1.9952 | 1.4018 |
| `cholesky/n512/b1` | 4.7097 | 2.4680 | 2.0934 |
| `cholesky/n512/b4` | 19.6948 | 10.3905 | 9.3437 |
| `eigh/n256/b1` | 10.2667 | 7.6873 | 19.5404 |
| `eigh/n256/b4` | 41.5112 | 31.9734 | 78.3549 |
| `eigh/n512/b1` | 63.1384 | 28.6517 | 127.5613 |
| `eigh/n512/b4` | 253.3905 | 115.6557 | 515.6149 |
| `eigvalsh/n256/b1` | 5.0098 | 5.0277 | 4.9489 |
| `eigvalsh/n256/b4` | 19.8699 | 19.9416 | 19.7853 |
| `eigvalsh/n512/b1` | 29.8345 | 19.9253 | 20.5555 |
| `eigvalsh/n512/b4` | 119.2758 | 78.9640 | 82.4267 |
| `householder_apply/n256/b1` | 5.2655 | 5.3368 | 2.2749 |
| `householder_apply/n256/b4` | 21.8723 | 21.8267 | 9.0780 |
| `householder_apply/n512/b1` | 45.8254 | 45.9556 | 12.4420 |
| `householder_apply/n512/b4` | 179.9434 | 180.4365 | 49.3830 |
| `householder_factor/n256/b1` | 3.4663 | 3.5682 | 1.7114 |
| `householder_factor/n256/b4` | 13.8807 | 13.9197 | 6.9121 |
| `householder_factor/n512/b1` | 29.3372 | 29.2650 | 8.4993 |
| `householder_factor/n512/b4` | 119.4891 | 119.6432 | 34.6883 |
| `lu/n256/b1` | 1.2390 | 0.8309 | 0.7758 |
| `lu/n256/b4` | 5.1207 | 3.4112 | 3.2964 |
| `lu/n512/b1` | 8.7121 | 3.8965 | 3.7219 |
| `lu/n512/b4` | 34.6379 | 15.4733 | 14.9637 |
| `lu_factor/n256/b1` | 1.1110 | 0.6786 | 0.6647 |
| `lu_factor/n256/b4` | 4.5339 | 1.4219 | 2.6608 |
| `lu_factor/n512/b1` | 8.0631 | 3.1087 | 3.0102 |
| `lu_factor/n512/b4` | 32.8269 | 9.0290 | 12.0421 |
| `lu_factor_solve/n256/b1` | 1.1822 | 0.7422 | 0.7590 |
| `lu_factor_solve/n256/b4` | 4.7880 | 1.2300 | 3.0029 |
| `lu_factor_solve/n512/b1` | 8.2230 | 3.2946 | 3.3499 |
| `lu_factor_solve/n512/b4` | 33.9465 | 9.6210 | 13.5073 |
| `lu_solve_prepared/n256/b1` | 0.0633 | 0.0595 | 0.0939 |
| `lu_solve_prepared/n256/b4` | 0.2504 | 0.1363 | 0.3026 |
| `lu_solve_prepared/n512/b1` | 0.2082 | 0.1606 | 0.3598 |
| `lu_solve_prepared/n512/b4` | 1.3352 | 0.6457 | 1.7269 |
| `qr/n256/b1` | 6.2269 | 3.0905 | 3.4492 |
| `qr/n256/b4` | 24.8004 | 12.4483 | 13.9352 |
| `qr/n512/b1` | 42.3201 | 14.5615 | 17.4758 |
| `qr/n512/b4` | 169.4173 | 58.4802 | 69.8085 |
| `rank_revealing_qr/n256/b1` | 6.7650 | 3.8006 | 3.8782 |
| `rank_revealing_qr/n256/b4` | 26.8936 | 15.9768 | 15.7341 |
| `rank_revealing_qr/n512/b1` | 47.6891 | 17.1565 | 19.1058 |
| `rank_revealing_qr/n512/b4` | 191.5816 | 68.2360 | 76.7018 |
| `solve/n256/b1` | 1.1817 | 0.7624 | 0.8158 |
| `solve/n256/b4` | 4.7141 | 3.0379 | 3.2621 |
| `solve/n512/b1` | 8.3582 | 3.3837 | 3.4407 |
| `solve/n512/b4` | 32.9399 | 13.4635 | 14.1561 |
| `svd_thin/n256/b1` | 24.7468 | 15.3808 | 14.4338 |
| `svd_thin/n256/b4` | 98.3644 | 63.0413 | 57.6053 |
| `svd_thin/n512/b1` | 155.0236 | 67.9527 | 71.1024 |
| `svd_thin/n512/b4` | 618.8017 | 272.5629 | 289.1199 |
| `svd_values/n256/b1` | 11.5019 | 11.1772 | 7.2524 |
| `svd_values/n256/b4` | 46.0226 | 45.0295 | 28.9603 |
| `svd_values/n512/b1` | 68.2233 | 42.4722 | 32.4565 |
| `svd_values/n512/b4` | 273.6005 | 170.2998 | 129.0254 |
| `triangular_solve/n256/b1` | 0.0338 | 0.0343 | 0.0478 |
| `triangular_solve/n256/b4` | 0.1475 | 0.1351 | 0.2172 |
| `triangular_solve/n512/b1` | 0.1125 | 0.0847 | 0.1478 |
| `triangular_solve/n512/b4` | 0.5055 | 0.3692 | 0.8175 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7011 | 0.4853 | 0.3392 |
| `cholesky/n256/b4` | 2.8118 | 1.9966 | 1.3352 |
| `cholesky/n512/b1` | 4.7537 | 1.7938 | 1.4613 |
| `cholesky/n512/b4` | 19.8048 | 7.9624 | 6.5614 |
| `eigh/n256/b1` | 10.3115 | 7.0110 | 19.2373 |
| `eigh/n256/b4` | 41.3637 | 27.8500 | 78.8166 |
| `eigh/n512/b1` | 63.1926 | 24.2711 | 123.4210 |
| `eigh/n512/b4` | 253.5158 | 96.3026 | 493.3233 |
| `eigvalsh/n256/b1` | 5.0056 | 5.0143 | 4.8344 |
| `eigvalsh/n256/b4` | 19.9533 | 19.9117 | 19.4214 |
| `eigvalsh/n512/b1` | 29.4769 | 17.9157 | 17.9859 |
| `eigvalsh/n512/b4` | 118.4455 | 71.8419 | 72.1018 |
| `householder_apply/n256/b1` | 5.2656 | 5.3224 | 1.7637 |
| `householder_apply/n256/b4` | 21.6207 | 21.6592 | 7.2318 |
| `householder_apply/n512/b1` | 44.5973 | 44.6973 | 8.5973 |
| `householder_apply/n512/b4` | 180.7293 | 180.5020 | 35.5940 |
| `householder_factor/n256/b1` | 3.4637 | 3.5388 | 1.5456 |
| `householder_factor/n256/b4` | 13.9170 | 13.9992 | 6.0911 |
| `householder_factor/n512/b1` | 29.7258 | 29.6695 | 6.4783 |
| `householder_factor/n512/b4` | 118.3797 | 118.9356 | 26.1881 |
| `lu/n256/b1` | 1.2372 | 0.8112 | 0.5688 |
| `lu/n256/b4` | 5.1271 | 3.3894 | 2.4320 |
| `lu/n512/b1` | 8.6550 | 3.3158 | 2.3076 |
| `lu/n512/b4` | 34.9443 | 13.1161 | 9.2994 |
| `lu_factor/n256/b1` | 1.1176 | 0.6558 | 0.4546 |
| `lu_factor/n256/b4` | 4.3524 | 2.5557 | 1.7656 |
| `lu_factor/n512/b1` | 8.0362 | 2.5738 | 1.6411 |
| `lu_factor/n512/b4` | 32.7091 | 10.4610 | 6.6097 |
| `lu_factor_solve/n256/b1` | 1.1807 | 0.7240 | 0.5588 |
| `lu_factor_solve/n256/b4` | 4.6067 | 2.8328 | 2.0654 |
| `lu_factor_solve/n512/b1` | 8.2373 | 2.7187 | 1.9904 |
| `lu_factor_solve/n512/b4` | 33.7067 | 11.1124 | 8.0416 |
| `lu_solve_prepared/n256/b1` | 0.0627 | 0.0677 | 0.1031 |
| `lu_solve_prepared/n256/b4` | 0.2458 | 0.2546 | 0.3199 |
| `lu_solve_prepared/n512/b1` | 0.2233 | 0.1680 | 0.3403 |
| `lu_solve_prepared/n512/b4` | 1.0671 | 0.8764 | 1.5763 |
| `qr/n256/b1` | 6.2016 | 3.5122 | 3.0464 |
| `qr/n256/b4` | 24.8836 | 14.0392 | 12.3139 |
| `qr/n512/b1` | 42.3457 | 12.3846 | 13.1371 |
| `qr/n512/b4` | 169.4566 | 50.0746 | 53.4239 |
| `rank_revealing_qr/n256/b1` | 6.7303 | 3.6775 | 3.5196 |
| `rank_revealing_qr/n256/b4` | 27.0397 | 14.7156 | 14.3367 |
| `rank_revealing_qr/n512/b1` | 47.4843 | 12.2193 | 14.8391 |
| `rank_revealing_qr/n512/b4` | 190.7183 | 48.5776 | 59.8668 |
| `solve/n256/b1` | 1.1817 | 0.7538 | 0.5833 |
| `solve/n256/b4` | 4.7292 | 2.9853 | 2.4668 |
| `solve/n512/b1` | 8.2172 | 2.8655 | 2.1348 |
| `solve/n512/b4` | 32.8171 | 11.3471 | 8.7599 |
| `svd_thin/n256/b1` | 24.4829 | 14.9816 | 13.2973 |
| `svd_thin/n256/b4` | 98.0052 | 59.8699 | 54.1038 |
| `svd_thin/n512/b1` | 154.4014 | 55.4425 | 60.8529 |
| `svd_thin/n512/b4` | 617.7661 | 224.7857 | 243.8359 |
| `svd_values/n256/b1` | 11.5534 | 11.1827 | 7.1832 |
| `svd_values/n256/b4` | 46.5852 | 44.8124 | 29.1631 |
| `svd_values/n512/b1` | 68.0757 | 40.0785 | 28.8097 |
| `svd_values/n512/b4` | 271.7025 | 160.3328 | 115.6482 |
| `triangular_solve/n256/b1` | 0.0338 | 0.0380 | 0.0416 |
| `triangular_solve/n256/b4` | 0.1389 | 0.1486 | 0.1713 |
| `triangular_solve/n512/b1` | 0.1148 | 0.0898 | 0.1547 |
| `triangular_solve/n512/b4` | 0.5111 | 0.4108 | 0.8211 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5407 | - | 0.5493 |
| `householder_factor/4096x256/b1` | 42.0389 | - | 23.4146 |
| `qr/1024x64/b1` | 0.9782 | - | 1.0757 |
| `qr/4096x256/b1` | 41.3216 | - | 46.9697 |
| `rank_revealing_qr/1024x64/b1` | 0.9670 | - | 1.1668 |
| `rank_revealing_qr/4096x256/b1` | 64.6682 | - | 57.1649 |
| `svd_thin/1024x64/b1` | 1.4580 | - | 1.9700 |
| `svd_thin/4096x256/b1` | 72.5618 | - | 74.5206 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5378 | 0.5445 | 0.5931 |
| `householder_factor/4096x256/b1` | 41.8156 | 41.7530 | 12.4650 |
| `qr/1024x64/b1` | 0.9836 | 0.9029 | 1.1425 |
| `qr/4096x256/b1` | 41.2606 | 20.2465 | 24.7581 |
| `rank_revealing_qr/1024x64/b1` | 0.9671 | 0.7311 | 1.2341 |
| `rank_revealing_qr/4096x256/b1` | 64.4978 | 23.9182 | 28.4959 |
| `svd_thin/1024x64/b1` | 1.4525 | 1.3736 | 1.8852 |
| `svd_thin/4096x256/b1` | 72.3670 | 40.5568 | 41.5038 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5387 | 0.5443 | 0.5932 |
| `householder_factor/4096x256/b1` | 41.7892 | 42.1124 | 10.7332 |
| `qr/1024x64/b1` | 0.9879 | 1.1131 | 1.1347 |
| `qr/4096x256/b1` | 41.2078 | 19.7271 | 22.1013 |
| `rank_revealing_qr/1024x64/b1` | 0.9678 | 0.7485 | 1.2481 |
| `rank_revealing_qr/4096x256/b1` | 65.2263 | 18.8685 | 23.7452 |
| `svd_thin/1024x64/b1` | 1.4560 | 1.6397 | 1.8861 |
| `svd_thin/4096x256/b1` | 72.3114 | 33.2221 | 37.6372 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.3362 | - | 1.0655 |
| `householder_factor/4096x256/b1` | 128.8446 | - | 68.7092 |
| `qr/1024x64/b1` | 2.8565 | - | 2.0774 |
| `qr/4096x256/b1` | 147.2317 | - | 138.4926 |
| `rank_revealing_qr/1024x64/b1` | 2.8646 | - | 2.2715 |
| `rank_revealing_qr/4096x256/b1` | 244.4609 | - | 172.5886 |
| `svd_thin/1024x64/b1` | 3.5555 | - | 3.9826 |
| `svd_thin/4096x256/b1` | 232.4358 | - | 218.8962 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.3433 | 1.3855 | 0.4344 |
| `householder_factor/4096x256/b1` | 129.6629 | 129.2440 | 19.9524 |
| `qr/1024x64/b1` | 2.8544 | 1.6255 | 0.8114 |
| `qr/4096x256/b1` | 146.5819 | 57.0388 | 40.1055 |
| `rank_revealing_qr/1024x64/b1` | 2.8589 | 1.7676 | 1.0313 |
| `rank_revealing_qr/4096x256/b1` | 245.7045 | 83.4455 | 55.6935 |
| `svd_thin/1024x64/b1` | 3.5544 | 2.3089 | 2.1016 |
| `svd_thin/4096x256/b1` | 232.5270 | 105.3649 | 75.7146 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.3245 | 1.3581 | 0.3458 |
| `householder_factor/4096x256/b1` | 127.6646 | 127.8382 | 12.5042 |
| `qr/1024x64/b1` | 2.8460 | 1.7564 | 0.6218 |
| `qr/4096x256/b1` | 146.9405 | 46.2177 | 25.7286 |
| `rank_revealing_qr/1024x64/b1` | 2.8571 | 1.7289 | 0.8604 |
| `rank_revealing_qr/4096x256/b1` | 244.7805 | 52.4554 | 34.1542 |
| `svd_thin/1024x64/b1` | 3.5432 | 2.4589 | 1.8200 |
| `svd_thin/4096x256/b1` | 231.6037 | 74.3714 | 54.2909 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
