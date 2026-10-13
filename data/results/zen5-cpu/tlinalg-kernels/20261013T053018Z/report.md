# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `6180fb0da69717891fe09bc67a76c3e7b74fba02`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.24.4 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c); `t4a-faer-traits` 0.24.0 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c)
- harness commit: `27a223546fc69ec3d102ce004d5f4d60e0f69db9`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-13T06:29:46.639357Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor mkl`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261013T053018Z/`

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
    As measured: `t4a-faer` 0.24.4 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c); `t4a-faer-traits` 0.24.0 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.24.4 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c); `t4a-faer-traits` 0.24.0 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c)
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
- CPU sets: 1T -> `4`, 4T -> `4-7`, 8T -> `4-11`

Every row below passed `tlbench verify` on the same grid before timing: the two
providers' factorizations are checked against each provider's documented convention
(reconstruction, orthonormality, residuals), not against each other's floating-point
output. Times are milliseconds, the best wall time per case and engine row; with more
than one complete set repeat the table shows the best repeat, and the A/A spread is
reported at its foot.

## small, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | - | 0.0007 |
| `cholesky/n16/b1024` | 0.5285 | - | 0.6316 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1072 | - | 0.0731 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2143 | - | 0.1919 |
| `eig/n16/b1` | 0.0534 | - | 0.0306 |
| `eig/n16/b1024` | 55.8946 | - | 31.8355 |
| `eig/n4/b1` | 0.0040 | - | 0.0022 |
| `eig/n4/b1024` | 3.5574 | - | 1.7455 |
| `eig/n8/b1` | 0.0141 | - | 0.0074 |
| `eig/n8/b1024` | 13.7062 | - | 7.0106 |
| `eigh/n16/b1` | 0.0177 | - | 0.0135 |
| `eigh/n16/b1024` | 17.8979 | - | 14.1213 |
| `eigh/n4/b1` | 0.0016 | - | 0.0019 |
| `eigh/n4/b1024` | 1.4301 | - | 1.7014 |
| `eigh/n8/b1` | 0.0051 | - | 0.0047 |
| `eigh/n8/b1024` | 5.0343 | - | 4.6512 |
| `eigvals/n16/b1` | 0.0373 | - | 0.0211 |
| `eigvals/n16/b1024` | 39.2779 | - | 21.8707 |
| `eigvals/n4/b1` | 0.0023 | - | 0.0017 |
| `eigvals/n4/b1024` | 1.9313 | - | 1.2718 |
| `eigvals/n8/b1` | 0.0098 | - | 0.0059 |
| `eigvals/n8/b1024` | 9.1378 | - | 5.3633 |
| `eigvalsh/n16/b1` | 0.0133 | - | 0.0076 |
| `eigvalsh/n16/b1024` | 13.1890 | - | 7.7895 |
| `eigvalsh/n4/b1` | 0.0013 | - | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1361 | - | 0.8847 |
| `eigvalsh/n8/b1` | 0.0044 | - | 0.0029 |
| `eigvalsh/n8/b1024` | 3.9966 | - | 2.6583 |
| `full_piv_lu/n16/b1` | 0.0026 | - | 0.0024 |
| `full_piv_lu/n16/b1024` | 1.9840 | - | 2.4376 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2269 | - | 0.2712 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6155 | - | 0.5870 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | - | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0684 | - | 3.5238 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | - | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3344 | - | 0.6709 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7770 | - | 1.1854 |
| `householder_apply/n16/b1` | 0.0028 | - | 0.0018 |
| `householder_apply/n16/b1024` | 2.7662 | - | 1.6053 |
| `householder_apply/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.2204 | - | 0.2014 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0008 |
| `householder_apply/n8/b1024` | 0.7075 | - | 0.4915 |
| `householder_factor/n16/b1` | 0.0022 | - | 0.0018 |
| `householder_factor/n16/b1024` | 2.1769 | - | 1.7702 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0003 |
| `householder_factor/n4/b1024` | 0.2600 | - | 0.1830 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0006 |
| `householder_factor/n8/b1024` | 0.7118 | - | 0.5029 |
| `lu/n16/b1` | 0.0020 | - | 0.0012 |
| `lu/n16/b1024` | 1.6342 | - | 1.1555 |
| `lu/n4/b1` | 0.0004 | - | 0.0003 |
| `lu/n4/b1024` | 0.1705 | - | 0.1045 |
| `lu/n8/b1` | 0.0007 | - | 0.0005 |
| `lu/n8/b1024` | 0.5145 | - | 0.3064 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0008 |
| `lu_factor/n16/b1024` | 1.1054 | - | 0.7026 |
| `lu_factor/n4/b1` | 0.0003 | - | 0.0001 |
| `lu_factor/n4/b1024` | 0.1315 | - | 0.0400 |
| `lu_factor/n8/b1` | 0.0005 | - | 0.0002 |
| `lu_factor/n8/b1024` | 0.3445 | - | 0.1569 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4494 | - | 1.3896 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1640 | - | 0.1086 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4746 | - | 0.4964 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3559 | - | 0.6232 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0405 | - | 0.0790 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1367 | - | 0.3547 |
| `qr/n16/b1` | 0.0054 | - | 0.0033 |
| `qr/n16/b1024` | 5.3042 | - | 3.1961 |
| `qr/n4/b1` | 0.0008 | - | 0.0007 |
| `qr/n4/b1024` | 0.4382 | - | 0.4130 |
| `qr/n8/b1` | 0.0016 | - | 0.0013 |
| `qr/n8/b1024` | 1.3940 | - | 1.0204 |
| `rank_revealing_qr/n16/b1` | 0.0066 | - | 0.0054 |
| `rank_revealing_qr/n16/b1024` | 6.2812 | - | 5.0208 |
| `rank_revealing_qr/n4/b1` | 0.0012 | - | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7049 | - | 0.7690 |
| `rank_revealing_qr/n8/b1` | 0.0023 | - | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.9338 | - | 1.8057 |
| `solve/n16/b1` | 0.0021 | - | 0.0018 |
| `solve/n16/b1024` | 1.5745 | - | 1.4479 |
| `solve/n4/b1` | 0.0006 | - | 0.0003 |
| `solve/n4/b1024` | 0.2153 | - | 0.1421 |
| `solve/n8/b1` | 0.0010 | - | 0.0007 |
| `solve/n8/b1024` | 0.5611 | - | 0.5413 |
| `svd_full/n16/b1` | 0.0325 | - | 0.0308 |
| `svd_full/n16/b1024` | 33.3338 | - | 31.1363 |
| `svd_full/n4/b1` | 0.0028 | - | 0.0039 |
| `svd_full/n4/b1024` | 2.5243 | - | 3.6975 |
| `svd_full/n8/b1` | 0.0089 | - | 0.0107 |
| `svd_full/n8/b1024` | 8.9524 | - | 11.1376 |
| `svd_thin/n16/b1` | 0.0334 | - | 0.0305 |
| `svd_thin/n16/b1024` | 33.6728 | - | 31.2178 |
| `svd_thin/n4/b1` | 0.0029 | - | 0.0039 |
| `svd_thin/n4/b1024` | 2.5068 | - | 3.6790 |
| `svd_thin/n8/b1` | 0.0089 | - | 0.0107 |
| `svd_thin/n8/b1024` | 8.9763 | - | 11.1806 |
| `svd_values/n16/b1` | 0.0239 | - | 0.0112 |
| `svd_values/n16/b1024` | 24.4571 | - | 11.6232 |
| `svd_values/n4/b1` | 0.0021 | - | 0.0018 |
| `svd_values/n4/b1024` | 1.9145 | - | 1.5932 |
| `svd_values/n8/b1` | 0.0069 | - | 0.0041 |
| `svd_values/n8/b1024` | 6.7425 | - | 4.0523 |
| `triangular_solve/n16/b1` | 0.0005 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3040 | - | 0.3395 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0516 | - | 0.1741 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1305 | - | 0.2268 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0024 | 0.0007 |
| `cholesky/n16/b1024` | 0.5227 | 0.2621 | 0.6312 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1059 | 0.0329 | 0.0716 |
| `cholesky/n8/b1` | 0.0003 | 0.0021 | 0.0003 |
| `cholesky/n8/b1024` | 0.2155 | 0.0602 | 0.1940 |
| `eig/n16/b1` | 0.0530 | 0.0568 | 0.0307 |
| `eig/n16/b1024` | 55.8831 | 16.9813 | 32.0542 |
| `eig/n4/b1` | 0.0040 | 0.0061 | 0.0022 |
| `eig/n4/b1024` | 3.5391 | 0.9249 | 1.7494 |
| `eig/n8/b1` | 0.0142 | 0.0170 | 0.0074 |
| `eig/n8/b1024` | 13.5954 | 3.4343 | 7.0415 |
| `eigh/n16/b1` | 0.0176 | 0.0205 | 0.0135 |
| `eigh/n16/b1024` | 17.7169 | 4.8976 | 14.1729 |
| `eigh/n4/b1` | 0.0017 | 0.0040 | 0.0019 |
| `eigh/n4/b1024` | 1.4291 | 0.7191 | 1.6753 |
| `eigh/n8/b1` | 0.0051 | 0.0074 | 0.0047 |
| `eigh/n8/b1024` | 5.0318 | 2.0794 | 4.6282 |
| `eigvals/n16/b1` | 0.0372 | 0.0403 | 0.0210 |
| `eigvals/n16/b1024` | 39.0177 | 10.2763 | 21.9604 |
| `eigvals/n4/b1` | 0.0023 | 0.0045 | 0.0017 |
| `eigvals/n4/b1024` | 1.8984 | 0.9539 | 1.2631 |
| `eigvals/n8/b1` | 0.0098 | 0.0130 | 0.0059 |
| `eigvals/n8/b1024` | 9.1722 | 4.6395 | 5.3727 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0163 | 0.0075 |
| `eigvalsh/n16/b1024` | 13.2217 | 6.2118 | 7.8015 |
| `eigvalsh/n4/b1` | 0.0014 | 0.0036 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1403 | 0.5751 | 0.8888 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0072 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0324 | 1.6609 | 2.6417 |
| `full_piv_lu/n16/b1` | 0.0026 | 0.0043 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.0000 | 0.9814 | 2.3327 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2276 | 0.1212 | 0.2702 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0032 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6242 | 0.1715 | 0.5900 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0048 | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0685 | 0.5329 | 3.4975 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0027 | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3367 | 0.1742 | 0.6608 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0038 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.8242 | 0.3909 | 1.1626 |
| `householder_apply/n16/b1` | 0.0028 | 0.0053 | 0.0018 |
| `householder_apply/n16/b1024` | 2.7465 | 0.6954 | 1.6361 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0004 |
| `householder_apply/n4/b1024` | 0.2094 | 0.0551 | 0.1916 |
| `householder_apply/n8/b1` | 0.0008 | 0.0034 | 0.0007 |
| `householder_apply/n8/b1024` | 0.7070 | 0.1877 | 0.4731 |
| `householder_factor/n16/b1` | 0.0023 | 0.0039 | 0.0018 |
| `householder_factor/n16/b1024` | 2.1549 | 0.5576 | 1.7653 |
| `householder_factor/n4/b1` | 0.0003 | 0.0020 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2605 | 0.1352 | 0.1835 |
| `householder_factor/n8/b1` | 0.0008 | 0.0034 | 0.0007 |
| `householder_factor/n8/b1024` | 0.6977 | 0.1860 | 0.5045 |
| `lu/n16/b1` | 0.0021 | 0.0042 | 0.0012 |
| `lu/n16/b1024` | 1.6606 | 0.8198 | 1.0959 |
| `lu/n4/b1` | 0.0004 | 0.0022 | 0.0003 |
| `lu/n4/b1024` | 0.1715 | 0.0518 | 0.1028 |
| `lu/n8/b1` | 0.0007 | 0.0035 | 0.0005 |
| `lu/n8/b1024` | 0.5097 | 0.2552 | 0.3009 |
| `lu_factor/n16/b1` | 0.0013 | 0.0030 | 0.0007 |
| `lu_factor/n16/b1024` | 1.1279 | 0.2866 | 0.6974 |
| `lu_factor/n4/b1` | 0.0003 | 0.0021 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1309 | 0.0701 | 0.0379 |
| `lu_factor/n8/b1` | 0.0006 | 0.0024 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3389 | 0.0951 | 0.1579 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0045 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4055 | 0.3673 | 1.3731 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1659 | 0.0469 | 0.1094 |
| `lu_factor_solve/n8/b1` | 0.0008 | 0.0039 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4768 | 0.1272 | 0.4936 |
| `lu_solve_prepared/n16/b1` | 0.0006 | 0.0036 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3782 | 0.1915 | 0.6209 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0028 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0406 | 0.0205 | 0.0785 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0028 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1393 | 0.0464 | 0.3505 |
| `qr/n16/b1` | 0.0056 | 0.0086 | 0.0033 |
| `qr/n16/b1024` | 5.1664 | 2.5793 | 3.1634 |
| `qr/n4/b1` | 0.0007 | 0.0023 | 0.0007 |
| `qr/n4/b1024` | 0.4309 | 0.2203 | 0.4121 |
| `qr/n8/b1` | 0.0016 | 0.0039 | 0.0013 |
| `qr/n8/b1024` | 1.3752 | 0.6884 | 0.9916 |
| `rank_revealing_qr/n16/b1` | 0.0067 | 0.0099 | 0.0054 |
| `rank_revealing_qr/n16/b1024` | 6.0207 | 3.0971 | 4.9696 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0034 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7037 | 0.3570 | 0.7634 |
| `rank_revealing_qr/n8/b1` | 0.0023 | 0.0046 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.9055 | 0.9614 | 1.7957 |
| `solve/n16/b1` | 0.0022 | 0.0044 | 0.0019 |
| `solve/n16/b1024` | 1.5568 | 0.4038 | 1.4608 |
| `solve/n4/b1` | 0.0006 | 0.0023 | 0.0003 |
| `solve/n4/b1024` | 0.2165 | 0.0627 | 0.1410 |
| `solve/n8/b1` | 0.0010 | 0.0034 | 0.0007 |
| `solve/n8/b1024` | 0.5458 | 0.2829 | 0.5354 |
| `svd_full/n16/b1` | 0.0325 | 0.0350 | 0.0306 |
| `svd_full/n16/b1024` | 33.2192 | 8.8123 | 30.9724 |
| `svd_full/n4/b1` | 0.0028 | 0.0049 | 0.0039 |
| `svd_full/n4/b1024` | 2.5128 | 1.2980 | 3.6685 |
| `svd_full/n8/b1` | 0.0090 | 0.0116 | 0.0106 |
| `svd_full/n8/b1024` | 8.9221 | 2.2613 | 11.1058 |
| `svd_thin/n16/b1` | 0.0325 | 0.0352 | 0.0305 |
| `svd_thin/n16/b1024` | 33.3472 | 10.8274 | 30.9466 |
| `svd_thin/n4/b1` | 0.0027 | 0.0051 | 0.0039 |
| `svd_thin/n4/b1024` | 2.5195 | 1.2887 | 3.6401 |
| `svd_thin/n8/b1` | 0.0091 | 0.0114 | 0.0106 |
| `svd_thin/n8/b1024` | 8.9211 | 2.8218 | 11.1070 |
| `svd_values/n16/b1` | 0.0238 | 0.0266 | 0.0112 |
| `svd_values/n16/b1024` | 24.3872 | 6.1898 | 11.5878 |
| `svd_values/n4/b1` | 0.0021 | 0.0044 | 0.0018 |
| `svd_values/n4/b1024` | 1.8887 | 0.4835 | 1.5894 |
| `svd_values/n8/b1` | 0.0068 | 0.0092 | 0.0041 |
| `svd_values/n8/b1024` | 6.7535 | 3.4098 | 4.0347 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0022 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3096 | 0.1573 | 0.3519 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0510 | 0.0295 | 0.1845 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0027 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1294 | 0.0379 | 0.2361 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0039 | 0.0007 |
| `cholesky/n16/b1024` | 0.5221 | 0.0725 | 0.6290 |
| `cholesky/n4/b1` | 0.0002 | 0.0038 | 0.0002 |
| `cholesky/n4/b1024` | 0.1070 | 0.0220 | 0.0702 |
| `cholesky/n8/b1` | 0.0003 | 0.0026 | 0.0003 |
| `cholesky/n8/b1024` | 0.2186 | 0.0588 | 0.1880 |
| `eig/n16/b1` | 0.0532 | 0.0570 | 0.0306 |
| `eig/n16/b1024` | 55.6206 | 7.8928 | 31.9856 |
| `eig/n4/b1` | 0.0039 | 0.0066 | 0.0021 |
| `eig/n4/b1024` | 3.5889 | 0.4789 | 1.7401 |
| `eig/n8/b1` | 0.0142 | 0.0172 | 0.0074 |
| `eig/n8/b1024` | 13.6334 | 1.7519 | 7.0313 |
| `eigh/n16/b1` | 0.0176 | 0.0207 | 0.0135 |
| `eigh/n16/b1024` | 17.7508 | 2.2656 | 14.0640 |
| `eigh/n4/b1` | 0.0016 | 0.0052 | 0.0019 |
| `eigh/n4/b1024` | 1.4202 | 0.3651 | 1.6769 |
| `eigh/n8/b1` | 0.0051 | 0.0077 | 0.0047 |
| `eigh/n8/b1024` | 5.0677 | 1.2862 | 4.6208 |
| `eigvals/n16/b1` | 0.0373 | 0.0403 | 0.0212 |
| `eigvals/n16/b1024` | 38.9756 | 4.9161 | 21.9384 |
| `eigvals/n4/b1` | 0.0023 | 0.0054 | 0.0017 |
| `eigvals/n4/b1024` | 1.8952 | 0.4826 | 1.2734 |
| `eigvals/n8/b1` | 0.0098 | 0.0128 | 0.0059 |
| `eigvals/n8/b1024` | 9.1605 | 1.1583 | 5.3762 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0162 | 0.0075 |
| `eigvalsh/n16/b1024` | 13.1842 | 1.6779 | 7.8125 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0047 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1422 | 0.1602 | 0.8973 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0071 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0146 | 0.5158 | 2.6487 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0059 | 0.0023 |
| `full_piv_lu/n16/b1024` | 1.9863 | 0.2725 | 2.4050 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0035 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2415 | 0.0646 | 0.2642 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0044 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6190 | 0.1658 | 0.5823 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0057 | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0547 | 0.3042 | 3.4787 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0032 | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3364 | 0.0896 | 0.6687 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0044 | 0.0015 |
| `full_piv_lu_solve/n8/b1024` | 0.7632 | 0.1984 | 1.1839 |
| `householder_apply/n16/b1` | 0.0028 | 0.0056 | 0.0018 |
| `householder_apply/n16/b1024` | 2.7536 | 0.6861 | 1.5845 |
| `householder_apply/n4/b1` | 0.0003 | 0.0022 | 0.0005 |
| `householder_apply/n4/b1024` | 0.2046 | 0.0554 | 0.1947 |
| `householder_apply/n8/b1` | 0.0008 | 0.0024 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6697 | 0.1790 | 0.4694 |
| `householder_factor/n16/b1` | 0.0022 | 0.0053 | 0.0018 |
| `householder_factor/n16/b1024` | 2.1605 | 0.5484 | 1.7687 |
| `householder_factor/n4/b1` | 0.0004 | 0.0021 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2586 | 0.0701 | 0.1834 |
| `householder_factor/n8/b1` | 0.0008 | 0.0037 | 0.0006 |
| `householder_factor/n8/b1024` | 0.6968 | 0.1844 | 0.5045 |
| `lu/n16/b1` | 0.0020 | 0.0054 | 0.0012 |
| `lu/n16/b1024` | 1.5655 | 0.4069 | 1.0984 |
| `lu/n4/b1` | 0.0004 | 0.0022 | 0.0003 |
| `lu/n4/b1024` | 0.1725 | 0.0491 | 0.1029 |
| `lu/n8/b1` | 0.0007 | 0.0038 | 0.0005 |
| `lu/n8/b1024` | 0.5034 | 0.0691 | 0.3031 |
| `lu_factor/n16/b1` | 0.0014 | 0.0038 | 0.0007 |
| `lu_factor/n16/b1024` | 1.0968 | 0.2872 | 0.7179 |
| `lu_factor/n4/b1` | 0.0003 | 0.0028 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1317 | 0.0379 | 0.0396 |
| `lu_factor/n8/b1` | 0.0006 | 0.0024 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3498 | 0.0929 | 0.1559 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0047 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4227 | 0.3619 | 1.3897 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0028 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1663 | 0.0473 | 0.1094 |
| `lu_factor_solve/n8/b1` | 0.0008 | 0.0039 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4699 | 0.1272 | 0.4924 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0039 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3580 | 0.1051 | 0.6351 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0038 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0405 | 0.0229 | 0.0810 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0021 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1387 | 0.0452 | 0.3505 |
| `qr/n16/b1` | 0.0055 | 0.0148 | 0.0033 |
| `qr/n16/b1024` | 5.2021 | 1.2999 | 3.1692 |
| `qr/n4/b1` | 0.0007 | 0.0037 | 0.0007 |
| `qr/n4/b1024` | 0.4330 | 0.0601 | 0.4060 |
| `qr/n8/b1` | 0.0016 | 0.0049 | 0.0013 |
| `qr/n8/b1024` | 1.3712 | 0.3486 | 0.9994 |
| `rank_revealing_qr/n16/b1` | 0.0066 | 0.0094 | 0.0054 |
| `rank_revealing_qr/n16/b1024` | 6.1164 | 0.7758 | 4.9867 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0035 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7024 | 0.0939 | 0.7648 |
| `rank_revealing_qr/n8/b1` | 0.0023 | 0.0055 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8951 | 0.4838 | 1.7700 |
| `solve/n16/b1` | 0.0022 | 0.0052 | 0.0019 |
| `solve/n16/b1024` | 1.6055 | 0.4031 | 1.5963 |
| `solve/n4/b1` | 0.0006 | 0.0042 | 0.0003 |
| `solve/n4/b1024` | 0.2150 | 0.0594 | 0.1378 |
| `solve/n8/b1` | 0.0010 | 0.0041 | 0.0007 |
| `solve/n8/b1024` | 0.5497 | 0.0746 | 0.5348 |
| `svd_full/n16/b1` | 0.0325 | 0.0353 | 0.0307 |
| `svd_full/n16/b1024` | 33.0930 | 6.9998 | 30.9071 |
| `svd_full/n4/b1` | 0.0027 | 0.0059 | 0.0039 |
| `svd_full/n4/b1024` | 2.5183 | 0.3275 | 3.6589 |
| `svd_full/n8/b1` | 0.0089 | 0.0113 | 0.0106 |
| `svd_full/n8/b1024` | 8.9047 | 1.5202 | 11.1046 |
| `svd_thin/n16/b1` | 0.0324 | 0.0354 | 0.0305 |
| `svd_thin/n16/b1024` | 33.0142 | 5.7951 | 31.0894 |
| `svd_thin/n4/b1` | 0.0028 | 0.0056 | 0.0039 |
| `svd_thin/n4/b1024` | 2.5010 | 0.6402 | 3.6376 |
| `svd_thin/n8/b1` | 0.0089 | 0.0219 | 0.0106 |
| `svd_thin/n8/b1024` | 8.9442 | 1.1425 | 11.1203 |
| `svd_values/n16/b1` | 0.0239 | 0.0268 | 0.0112 |
| `svd_values/n16/b1024` | 24.4730 | 3.1396 | 11.5631 |
| `svd_values/n4/b1` | 0.0021 | 0.0053 | 0.0018 |
| `svd_values/n4/b1024` | 1.8997 | 0.4822 | 1.5808 |
| `svd_values/n8/b1` | 0.0069 | 0.0100 | 0.0041 |
| `svd_values/n8/b1024` | 6.7892 | 0.8604 | 4.0264 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0032 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.2983 | 0.0823 | 0.3608 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0022 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0511 | 0.0127 | 0.1751 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0031 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1295 | 0.0368 | 0.2353 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0012 |
| `cholesky/n16/b1024` | 0.8058 | - | 1.0837 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1200 | - | 0.1073 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2620 | - | 0.2847 |
| `eig/n16/b1` | 0.0724 | - | 0.0991 |
| `eig/n16/b1024` | 76.6252 | - | 107.1108 |
| `eig/n4/b1` | 0.0060 | - | 0.0077 |
| `eig/n4/b1024` | 5.8584 | - | 7.4783 |
| `eig/n8/b1` | 0.0198 | - | 0.0250 |
| `eig/n8/b1024` | 20.4933 | - | 26.0223 |
| `eigh/n16/b1` | 0.0181 | - | 0.0184 |
| `eigh/n16/b1024` | 19.3511 | - | 19.4345 |
| `eigh/n4/b1` | 0.0019 | - | 0.0018 |
| `eigh/n4/b1024` | 1.7262 | - | 1.7105 |
| `eigh/n8/b1` | 0.0057 | - | 0.0053 |
| `eigh/n8/b1024` | 5.4575 | - | 5.4060 |
| `eigvals/n16/b1` | 0.0433 | - | 0.0681 |
| `eigvals/n16/b1024` | 46.2410 | - | 75.1202 |
| `eigvals/n4/b1` | 0.0031 | - | 0.0061 |
| `eigvals/n4/b1024` | 2.9195 | - | 5.7644 |
| `eigvals/n8/b1` | 0.0117 | - | 0.0195 |
| `eigvals/n8/b1024` | 11.7863 | - | 20.6556 |
| `eigvalsh/n16/b1` | 0.0135 | - | 0.0108 |
| `eigvalsh/n16/b1024` | 14.3011 | - | 11.0981 |
| `eigvalsh/n4/b1` | 0.0016 | - | 0.0013 |
| `eigvalsh/n4/b1024` | 1.4303 | - | 1.0658 |
| `eigvalsh/n8/b1` | 0.0047 | - | 0.0035 |
| `eigvalsh/n8/b1024` | 4.3867 | - | 3.3476 |
| `full_piv_lu/n16/b1` | 0.0030 | - | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.6942 | - | 3.5286 |
| `full_piv_lu/n4/b1` | 0.0007 | - | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2693 | - | 0.3474 |
| `full_piv_lu/n8/b1` | 0.0012 | - | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7126 | - | 0.7668 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | - | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.0995 | - | 5.0938 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4518 | - | 0.9970 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1658 | - | 1.9394 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0035 |
| `householder_apply/n16/b1024` | 3.3177 | - | 4.1511 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.1969 | - | 0.2547 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0010 |
| `householder_apply/n8/b1024` | 0.6601 | - | 0.7587 |
| `householder_factor/n16/b1` | 0.0027 | - | 0.0038 |
| `householder_factor/n16/b1024` | 2.6679 | - | 3.8028 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.3207 | - | 0.3075 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.8519 | - | 0.8883 |
| `lu/n16/b1` | 0.0022 | - | 0.0021 |
| `lu/n16/b1024` | 1.8061 | - | 2.3128 |
| `lu/n4/b1` | 0.0005 | - | 0.0003 |
| `lu/n4/b1024` | 0.2118 | - | 0.1716 |
| `lu/n8/b1` | 0.0008 | - | 0.0007 |
| `lu/n8/b1024` | 0.5501 | - | 0.5541 |
| `lu_factor/n16/b1` | 0.0015 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2168 | - | 1.5836 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1605 | - | 0.1100 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3949 | - | 0.3720 |
| `lu_factor_solve/n16/b1` | 0.0023 | - | 0.0032 |
| `lu_factor_solve/n16/b1024` | 1.9590 | - | 3.2092 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2524 | - | 0.2490 |
| `lu_factor_solve/n8/b1` | 0.0009 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6838 | - | 0.9994 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7846 | - | 1.5595 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0987 | - | 0.1448 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2865 | - | 0.6417 |
| `qr/n16/b1` | 0.0067 | - | 0.0064 |
| `qr/n16/b1024` | 6.6550 | - | 6.5065 |
| `qr/n4/b1` | 0.0007 | - | 0.0009 |
| `qr/n4/b1024` | 0.5073 | - | 0.5725 |
| `qr/n8/b1` | 0.0018 | - | 0.0019 |
| `qr/n8/b1024` | 1.5484 | - | 1.5844 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0094 |
| `rank_revealing_qr/n16/b1024` | 7.3904 | - | 9.6226 |
| `rank_revealing_qr/n4/b1` | 0.0012 | - | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8224 | - | 1.0510 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1967 | - | 2.8831 |
| `solve/n16/b1` | 0.0027 | - | 0.0036 |
| `solve/n16/b1024` | 2.1344 | - | 3.3481 |
| `solve/n4/b1` | 0.0007 | - | 0.0005 |
| `solve/n4/b1024` | 0.3128 | - | 0.2867 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7395 | - | 1.0499 |
| `svd_full/n16/b1` | 0.0352 | - | 0.0394 |
| `svd_full/n16/b1024` | 36.5970 | - | 40.7801 |
| `svd_full/n4/b1` | 0.0030 | - | 0.0047 |
| `svd_full/n4/b1024` | 3.0092 | - | 4.4707 |
| `svd_full/n8/b1` | 0.0096 | - | 0.0127 |
| `svd_full/n8/b1024` | 10.1163 | - | 13.3526 |
| `svd_thin/n16/b1` | 0.0347 | - | 0.0395 |
| `svd_thin/n16/b1024` | 36.4993 | - | 40.8833 |
| `svd_thin/n4/b1` | 0.0030 | - | 0.0047 |
| `svd_thin/n4/b1024` | 2.9908 | - | 4.4777 |
| `svd_thin/n8/b1` | 0.0096 | - | 0.0126 |
| `svd_thin/n8/b1024` | 10.0118 | - | 13.3239 |
| `svd_values/n16/b1` | 0.0262 | - | 0.0165 |
| `svd_values/n16/b1024` | 27.2656 | - | 16.9859 |
| `svd_values/n4/b1` | 0.0024 | - | 0.0023 |
| `svd_values/n4/b1024` | 2.3106 | - | 2.1128 |
| `svd_values/n8/b1` | 0.0076 | - | 0.0054 |
| `svd_values/n8/b1024` | 7.7475 | - | 5.4828 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6075 | - | 0.8374 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0962 | - | 0.1782 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2362 | - | 0.3423 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0034 | 0.0011 |
| `cholesky/n16/b1024` | 0.8280 | 0.3995 | 1.1237 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1178 | 0.0366 | 0.1072 |
| `cholesky/n8/b1` | 0.0004 | 0.0023 | 0.0004 |
| `cholesky/n8/b1024` | 0.2541 | 0.0696 | 0.2829 |
| `eig/n16/b1` | 0.0718 | 0.0769 | 0.0951 |
| `eig/n16/b1024` | 75.8979 | 20.4163 | 102.1236 |
| `eig/n4/b1` | 0.0058 | 0.0083 | 0.0077 |
| `eig/n4/b1024` | 5.7777 | 1.4861 | 7.4766 |
| `eig/n8/b1` | 0.0198 | 0.0229 | 0.0250 |
| `eig/n8/b1024` | 20.4138 | 5.1583 | 26.0441 |
| `eigh/n16/b1` | 0.0180 | 0.0211 | 0.0185 |
| `eigh/n16/b1024` | 19.3949 | 8.4503 | 19.3882 |
| `eigh/n4/b1` | 0.0020 | 0.0045 | 0.0018 |
| `eigh/n4/b1024` | 1.7265 | 0.4391 | 1.6984 |
| `eigh/n8/b1` | 0.0057 | 0.0086 | 0.0053 |
| `eigh/n8/b1024` | 5.4327 | 2.7525 | 5.3506 |
| `eigvals/n16/b1` | 0.0434 | 0.0468 | 0.0684 |
| `eigvals/n16/b1024` | 46.1886 | 12.3659 | 75.4231 |
| `eigvals/n4/b1` | 0.0030 | 0.0053 | 0.0060 |
| `eigvals/n4/b1024` | 2.8266 | 1.4392 | 5.7826 |
| `eigvals/n8/b1` | 0.0117 | 0.0143 | 0.0196 |
| `eigvals/n8/b1024` | 11.8231 | 5.0018 | 20.6213 |
| `eigvalsh/n16/b1` | 0.0138 | 0.0166 | 0.0107 |
| `eigvalsh/n16/b1024` | 14.3847 | 6.7689 | 11.0652 |
| `eigvalsh/n4/b1` | 0.0017 | 0.0031 | 0.0013 |
| `eigvalsh/n4/b1024` | 1.4375 | 0.3665 | 1.0630 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0083 | 0.0035 |
| `eigvalsh/n8/b1024` | 4.4219 | 1.1216 | 3.3173 |
| `full_piv_lu/n16/b1` | 0.0030 | 0.0057 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.5965 | 1.3539 | 3.5903 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0034 | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2598 | 0.1345 | 0.3335 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0035 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7375 | 0.3690 | 0.7599 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0060 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1601 | 1.0516 | 5.0804 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0034 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4513 | 0.2348 | 0.9742 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0032 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1876 | 0.3212 | 1.9334 |
| `householder_apply/n16/b1` | 0.0027 | 0.0048 | 0.0035 |
| `householder_apply/n16/b1024` | 3.3345 | 1.5685 | 4.1674 |
| `householder_apply/n4/b1` | 0.0003 | 0.0027 | 0.0005 |
| `householder_apply/n4/b1024` | 0.2016 | 0.0555 | 0.2462 |
| `householder_apply/n8/b1` | 0.0007 | 0.0036 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6605 | 0.1926 | 0.7489 |
| `householder_factor/n16/b1` | 0.0026 | 0.0058 | 0.0038 |
| `householder_factor/n16/b1024` | 2.6528 | 1.0196 | 3.7828 |
| `householder_factor/n4/b1` | 0.0004 | 0.0026 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3200 | 0.0855 | 0.3081 |
| `householder_factor/n8/b1` | 0.0009 | 0.0037 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8463 | 0.2174 | 0.8939 |
| `lu/n16/b1` | 0.0022 | 0.0043 | 0.0022 |
| `lu/n16/b1024` | 1.9542 | 0.9532 | 2.2790 |
| `lu/n4/b1` | 0.0004 | 0.0023 | 0.0004 |
| `lu/n4/b1024` | 0.2135 | 0.0604 | 0.1724 |
| `lu/n8/b1` | 0.0008 | 0.0036 | 0.0007 |
| `lu/n8/b1024` | 0.5538 | 0.2773 | 0.5368 |
| `lu_factor/n16/b1` | 0.0014 | 0.0038 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2390 | 0.6131 | 1.5873 |
| `lu_factor/n4/b1` | 0.0004 | 0.0019 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1663 | 0.0470 | 0.1100 |
| `lu_factor/n8/b1` | 0.0006 | 0.0023 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3934 | 0.1160 | 0.3725 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0053 | 0.0032 |
| `lu_factor_solve/n16/b1024` | 1.9951 | 0.5259 | 3.2006 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0027 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2499 | 0.0710 | 0.2496 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0035 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6585 | 0.3408 | 0.9996 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0037 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7911 | 0.4006 | 1.5574 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0991 | 0.0338 | 0.1458 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0022 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2877 | 0.0842 | 0.6432 |
| `qr/n16/b1` | 0.0067 | 0.0096 | 0.0064 |
| `qr/n16/b1024` | 6.5161 | 3.3103 | 6.4132 |
| `qr/n4/b1` | 0.0007 | 0.0024 | 0.0009 |
| `qr/n4/b1024` | 0.5016 | 0.2592 | 0.5702 |
| `qr/n8/b1` | 0.0018 | 0.0034 | 0.0019 |
| `qr/n8/b1024` | 1.5385 | 0.7752 | 1.5770 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0103 | 0.0093 |
| `rank_revealing_qr/n16/b1024` | 7.2316 | 1.8362 | 9.5305 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0036 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8117 | 0.4128 | 1.0513 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0046 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.2052 | 0.5702 | 2.8352 |
| `solve/n16/b1` | 0.0028 | 0.0051 | 0.0035 |
| `solve/n16/b1024` | 2.0933 | 1.0892 | 3.3470 |
| `solve/n4/b1` | 0.0007 | 0.0030 | 0.0005 |
| `solve/n4/b1024` | 0.3154 | 0.0896 | 0.2864 |
| `solve/n8/b1` | 0.0012 | 0.0029 | 0.0012 |
| `solve/n8/b1024` | 0.7381 | 0.1961 | 1.0458 |
| `svd_full/n16/b1` | 0.0348 | 0.0386 | 0.0394 |
| `svd_full/n16/b1024` | 36.4177 | 10.5722 | 40.8578 |
| `svd_full/n4/b1` | 0.0030 | 0.0057 | 0.0046 |
| `svd_full/n4/b1024` | 2.9976 | 1.5233 | 4.4314 |
| `svd_full/n8/b1` | 0.0097 | 0.0124 | 0.0126 |
| `svd_full/n8/b1024` | 10.0151 | 3.4269 | 13.2817 |
| `svd_thin/n16/b1` | 0.0349 | 0.0385 | 0.0393 |
| `svd_thin/n16/b1024` | 36.4979 | 10.8350 | 40.8567 |
| `svd_thin/n4/b1` | 0.0030 | 0.0052 | 0.0047 |
| `svd_thin/n4/b1024` | 2.9896 | 1.5251 | 4.4441 |
| `svd_thin/n8/b1` | 0.0096 | 0.0126 | 0.0126 |
| `svd_thin/n8/b1024` | 9.9892 | 3.8245 | 13.2930 |
| `svd_values/n16/b1` | 0.0261 | 0.0289 | 0.0164 |
| `svd_values/n16/b1024` | 27.3077 | 6.9420 | 16.9548 |
| `svd_values/n4/b1` | 0.0025 | 0.0048 | 0.0023 |
| `svd_values/n4/b1024` | 2.3176 | 1.1878 | 2.1059 |
| `svd_values/n8/b1` | 0.0076 | 0.0103 | 0.0054 |
| `svd_values/n8/b1024` | 7.7751 | 1.9528 | 5.4628 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0030 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5942 | 0.2994 | 0.8081 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0025 | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0989 | 0.0299 | 0.1822 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0027 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2442 | 0.0684 | 0.3466 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0043 | 0.0011 |
| `cholesky/n16/b1024` | 0.8034 | 0.1982 | 1.0849 |
| `cholesky/n4/b1` | 0.0002 | 0.0038 | 0.0002 |
| `cholesky/n4/b1024` | 0.1176 | 0.0231 | 0.1067 |
| `cholesky/n8/b1` | 0.0004 | 0.0021 | 0.0004 |
| `cholesky/n8/b1024` | 0.2516 | 0.0369 | 0.2816 |
| `eig/n16/b1` | 0.0721 | 0.0751 | 0.0976 |
| `eig/n16/b1024` | 76.0044 | 9.5692 | 104.9762 |
| `eig/n4/b1` | 0.0059 | 0.0091 | 0.0077 |
| `eig/n4/b1024` | 5.7745 | 1.4827 | 7.4821 |
| `eig/n8/b1` | 0.0198 | 0.0228 | 0.0250 |
| `eig/n8/b1024` | 20.2793 | 2.5835 | 25.9593 |
| `eigh/n16/b1` | 0.0179 | 0.0210 | 0.0184 |
| `eigh/n16/b1024` | 19.3456 | 2.4328 | 19.5238 |
| `eigh/n4/b1` | 0.0019 | 0.0049 | 0.0018 |
| `eigh/n4/b1024` | 1.7393 | 0.4407 | 1.7012 |
| `eigh/n8/b1` | 0.0057 | 0.0083 | 0.0053 |
| `eigh/n8/b1024` | 5.4374 | 0.6860 | 5.3421 |
| `eigvals/n16/b1` | 0.0436 | 0.0465 | 0.0681 |
| `eigvals/n16/b1024` | 46.0748 | 6.8843 | 75.1200 |
| `eigvals/n4/b1` | 0.0030 | 0.0063 | 0.0060 |
| `eigvals/n4/b1024` | 2.8222 | 0.3711 | 5.7448 |
| `eigvals/n8/b1` | 0.0118 | 0.0271 | 0.0195 |
| `eigvals/n8/b1024` | 11.7763 | 2.0794 | 20.6161 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0167 | 0.0107 |
| `eigvalsh/n16/b1024` | 14.2999 | 2.3295 | 11.0042 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0048 | 0.0013 |
| `eigvalsh/n4/b1024` | 1.4250 | 0.3667 | 1.0627 |
| `eigvalsh/n8/b1` | 0.0046 | 0.0071 | 0.0035 |
| `eigvalsh/n8/b1024` | 4.3762 | 0.5642 | 3.3375 |
| `full_piv_lu/n16/b1` | 0.0030 | 0.0063 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.8197 | 0.6651 | 3.3904 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0030 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2611 | 0.0460 | 0.3409 |
| `full_piv_lu/n8/b1` | 0.0012 | 0.0029 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7300 | 0.1034 | 0.7710 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0064 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1021 | 0.7806 | 5.0760 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0033 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4608 | 0.1207 | 0.9769 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0047 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1435 | 0.3002 | 1.9170 |
| `householder_apply/n16/b1` | 0.0027 | 0.0058 | 0.0035 |
| `householder_apply/n16/b1024` | 3.4595 | 0.4680 | 4.0480 |
| `householder_apply/n4/b1` | 0.0003 | 0.0028 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1995 | 0.0382 | 0.2467 |
| `householder_apply/n8/b1` | 0.0007 | 0.0041 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6650 | 0.1669 | 0.7719 |
| `householder_factor/n16/b1` | 0.0026 | 0.0055 | 0.0037 |
| `householder_factor/n16/b1024` | 2.6303 | 0.6623 | 3.8074 |
| `householder_factor/n4/b1` | 0.0004 | 0.0033 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3200 | 0.0495 | 0.3083 |
| `householder_factor/n8/b1` | 0.0009 | 0.0039 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8396 | 0.2189 | 0.8854 |
| `lu/n16/b1` | 0.0022 | 0.0056 | 0.0022 |
| `lu/n16/b1024` | 1.9153 | 0.2656 | 2.2604 |
| `lu/n4/b1` | 0.0004 | 0.0031 | 0.0003 |
| `lu/n4/b1024` | 0.2130 | 0.0358 | 0.1712 |
| `lu/n8/b1` | 0.0008 | 0.0040 | 0.0007 |
| `lu/n8/b1024` | 0.5431 | 0.1463 | 0.5423 |
| `lu_factor/n16/b1` | 0.0015 | 0.0042 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2057 | 0.3140 | 1.5959 |
| `lu_factor/n4/b1` | 0.0004 | 0.0025 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1628 | 0.0463 | 0.1100 |
| `lu_factor/n8/b1` | 0.0006 | 0.0022 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3925 | 0.1067 | 0.3727 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0054 | 0.0031 |
| `lu_factor_solve/n16/b1024` | 1.9847 | 0.2941 | 3.1998 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0042 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2522 | 0.0702 | 0.2514 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0027 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6740 | 0.1763 | 0.9972 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0040 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7846 | 0.2092 | 1.5674 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0040 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0979 | 0.0340 | 0.1441 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0037 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2884 | 0.0858 | 0.6401 |
| `qr/n16/b1` | 0.0067 | 0.0091 | 0.0064 |
| `qr/n16/b1024` | 6.4837 | 0.8301 | 6.3195 |
| `qr/n4/b1` | 0.0007 | 0.0041 | 0.0009 |
| `qr/n4/b1024` | 0.5014 | 0.1332 | 0.5723 |
| `qr/n8/b1` | 0.0018 | 0.0050 | 0.0019 |
| `qr/n8/b1024` | 1.5263 | 0.3872 | 1.5736 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0104 | 0.0093 |
| `rank_revealing_qr/n16/b1024` | 7.2342 | 0.9354 | 9.5008 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0040 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8173 | 0.2108 | 1.0452 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0055 | 0.0031 |
| `rank_revealing_qr/n8/b1024` | 2.2250 | 0.5601 | 2.8495 |
| `solve/n16/b1` | 0.0028 | 0.0059 | 0.0036 |
| `solve/n16/b1024` | 2.1299 | 0.5379 | 3.3558 |
| `solve/n4/b1` | 0.0007 | 0.0038 | 0.0005 |
| `solve/n4/b1024` | 0.3104 | 0.0849 | 0.2859 |
| `solve/n8/b1` | 0.0012 | 0.0037 | 0.0012 |
| `solve/n8/b1024` | 0.7451 | 0.1094 | 1.0467 |
| `svd_full/n16/b1` | 0.0346 | 0.0376 | 0.0392 |
| `svd_full/n16/b1024` | 36.3584 | 4.6888 | 40.7930 |
| `svd_full/n4/b1` | 0.0031 | 0.0062 | 0.0047 |
| `svd_full/n4/b1024` | 2.9882 | 0.7515 | 4.4328 |
| `svd_full/n8/b1` | 0.0096 | 0.0126 | 0.0126 |
| `svd_full/n8/b1024` | 10.0457 | 1.3090 | 13.2482 |
| `svd_thin/n16/b1` | 0.0346 | 0.0376 | 0.0393 |
| `svd_thin/n16/b1024` | 36.4020 | 4.6960 | 40.8063 |
| `svd_thin/n4/b1` | 0.0031 | 0.0061 | 0.0046 |
| `svd_thin/n4/b1024` | 3.0208 | 0.4089 | 4.4225 |
| `svd_thin/n8/b1` | 0.0097 | 0.0125 | 0.0126 |
| `svd_thin/n8/b1024` | 10.0860 | 1.2831 | 13.2927 |
| `svd_values/n16/b1` | 0.0263 | 0.0290 | 0.0164 |
| `svd_values/n16/b1024` | 27.1784 | 3.5347 | 16.9553 |
| `svd_values/n4/b1` | 0.0025 | 0.0054 | 0.0023 |
| `svd_values/n4/b1024` | 2.3135 | 0.5854 | 2.1195 |
| `svd_values/n8/b1` | 0.0076 | 0.0106 | 0.0054 |
| `svd_values/n8/b1024` | 7.7649 | 1.8429 | 5.4806 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0038 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5906 | 0.1512 | 0.8689 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0038 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0956 | 0.0282 | 0.1811 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0021 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2396 | 0.0657 | 0.3507 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0394 | - | 0.0560 |
| `cholesky/n128/b128` | 5.9588 | - | 8.2144 |
| `cholesky/n32/b1` | 0.0021 | - | 0.0022 |
| `cholesky/n32/b128` | 0.2583 | - | 0.2689 |
| `eigh/n128/b1` | 1.2631 | - | 1.0815 |
| `eigh/n128/b128` | 162.7239 | - | 145.4728 |
| `eigh/n32/b1` | 0.0638 | - | 0.0554 |
| `eigh/n32/b128` | 8.4275 | - | 7.0616 |
| `eigvalsh/n128/b1` | 0.6987 | - | 0.4668 |
| `eigvalsh/n128/b128` | 90.7259 | - | 60.3855 |
| `eigvalsh/n32/b1` | 0.0487 | - | 0.0246 |
| `eigvalsh/n32/b128` | 6.4207 | - | 3.2153 |
| `householder_apply/n128/b1` | 0.1247 | - | 0.3150 |
| `householder_apply/n128/b128` | 17.7873 | - | 43.0588 |
| `householder_apply/n32/b1` | 0.0110 | - | 0.0077 |
| `householder_apply/n32/b128` | 1.3924 | - | 0.9199 |
| `householder_factor/n128/b1` | 0.1047 | - | 0.1961 |
| `householder_factor/n128/b128` | 13.4953 | - | 25.9308 |
| `householder_factor/n32/b1` | 0.0075 | - | 0.0068 |
| `householder_factor/n32/b128` | 0.9417 | - | 0.8914 |
| `lu/n128/b1` | 0.1058 | - | 0.0824 |
| `lu/n128/b128` | 12.9827 | - | 13.0118 |
| `lu/n32/b1` | 0.0059 | - | 0.0063 |
| `lu/n32/b128` | 0.6651 | - | 0.7780 |
| `lu_factor/n128/b1` | 0.0564 | - | 0.0728 |
| `lu_factor/n128/b128` | 8.1613 | - | 10.0617 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0052 |
| `lu_factor/n32/b128` | 0.4005 | - | 0.6561 |
| `lu_factor_solve/n128/b1` | 0.0623 | - | 0.0848 |
| `lu_factor_solve/n128/b128` | 8.9047 | - | 11.4939 |
| `lu_factor_solve/n32/b1` | 0.0042 | - | 0.0066 |
| `lu_factor_solve/n32/b128` | 0.4892 | - | 0.8482 |
| `lu_solve_prepared/n128/b1` | 0.0058 | - | 0.0121 |
| `lu_solve_prepared/n128/b128` | 1.7026 | - | 2.3952 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0014 |
| `lu_solve_prepared/n32/b128` | 0.1151 | - | 0.1693 |
| `qr/n128/b1` | 0.3399 | - | 0.3917 |
| `qr/n128/b128` | 44.2400 | - | 52.5942 |
| `qr/n32/b1` | 0.0210 | - | 0.0123 |
| `qr/n32/b128` | 2.6427 | - | 1.5854 |
| `rank_revealing_qr/n128/b1` | 0.3429 | - | 0.4805 |
| `rank_revealing_qr/n128/b128` | 45.0025 | - | 63.0801 |
| `rank_revealing_qr/n32/b1` | 0.0210 | - | 0.0181 |
| `rank_revealing_qr/n32/b128` | 2.5711 | - | 2.2845 |
| `solve/n128/b1` | 0.0661 | - | 0.0880 |
| `solve/n128/b128` | 8.7404 | - | 12.0277 |
| `solve/n32/b1` | 0.0048 | - | 0.0070 |
| `solve/n32/b128` | 0.5294 | - | 0.8663 |
| `svd_thin/n128/b1` | 2.4157 | - | 2.0263 |
| `svd_thin/n128/b128` | 307.4143 | - | 264.3067 |
| `svd_thin/n32/b1` | 0.1178 | - | 0.1068 |
| `svd_thin/n32/b128` | 15.2716 | - | 13.7975 |
| `svd_values/n128/b1` | 1.4100 | - | 0.7031 |
| `svd_values/n128/b128` | 180.4605 | - | 92.8653 |
| `svd_values/n32/b1` | 0.0923 | - | 0.0373 |
| `svd_values/n32/b128` | 11.9051 | - | 4.8786 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0071 |
| `triangular_solve/n128/b128` | 1.0159 | - | 1.3584 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0008 |
| `triangular_solve/n32/b128` | 0.0921 | - | 0.0866 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0375 | 0.0497 | 0.0567 |
| `cholesky/n128/b128` | 6.0188 | 6.9581 | 8.2061 |
| `cholesky/n32/b1` | 0.0021 | 0.0038 | 0.0022 |
| `cholesky/n32/b128` | 0.2588 | 0.1352 | 0.2653 |
| `eigh/n128/b1` | 1.2654 | 1.2335 | 0.6248 |
| `eigh/n128/b128` | 163.3031 | 163.9327 | 84.5897 |
| `eigh/n32/b1` | 0.0644 | 0.0685 | 0.0582 |
| `eigh/n32/b128` | 8.4934 | 2.6920 | 7.4362 |
| `eigvalsh/n128/b1` | 0.6956 | 0.7032 | 0.4326 |
| `eigvalsh/n128/b128` | 90.3804 | 90.7695 | 56.6710 |
| `eigvalsh/n32/b1` | 0.0488 | 0.0516 | 0.0248 |
| `eigvalsh/n32/b128` | 6.4024 | 1.6170 | 3.2284 |
| `householder_apply/n128/b1` | 0.1247 | 0.1290 | 0.0863 |
| `householder_apply/n128/b128` | 17.1968 | 17.5581 | 11.5013 |
| `householder_apply/n32/b1` | 0.0108 | 0.0138 | 0.0074 |
| `householder_apply/n32/b128` | 1.3571 | 0.6789 | 0.9145 |
| `householder_factor/n128/b1` | 0.1044 | 0.1307 | 0.1142 |
| `householder_factor/n128/b128` | 13.5413 | 16.7699 | 14.1833 |
| `householder_factor/n32/b1` | 0.0074 | 0.0099 | 0.0068 |
| `householder_factor/n32/b128` | 0.9393 | 0.4708 | 0.8941 |
| `lu/n128/b1` | 0.1012 | 0.1196 | 0.0817 |
| `lu/n128/b128` | 12.9768 | 14.9360 | 12.7435 |
| `lu/n32/b1` | 0.0059 | 0.0091 | 0.0062 |
| `lu/n32/b128` | 0.6689 | 0.3384 | 0.7726 |
| `lu_factor/n128/b1` | 0.0563 | 0.0721 | 0.0728 |
| `lu_factor/n128/b128` | 8.1224 | 3.3038 | 10.0099 |
| `lu_factor/n32/b1` | 0.0033 | 0.0058 | 0.0052 |
| `lu_factor/n32/b128` | 0.3876 | 0.1089 | 0.6536 |
| `lu_factor_solve/n128/b1` | 0.0625 | 0.0776 | 0.0869 |
| `lu_factor_solve/n128/b128` | 8.9566 | 2.6789 | 11.9946 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0079 | 0.0078 |
| `lu_factor_solve/n32/b128` | 0.4966 | 0.1309 | 0.9767 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0084 | 0.0099 |
| `lu_solve_prepared/n128/b128` | 1.9817 | 0.5494 | 2.4054 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0037 | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.1129 | 0.0342 | 0.2984 |
| `qr/n128/b1` | 0.3413 | 0.6193 | 0.3003 |
| `qr/n128/b128` | 44.1610 | 82.7729 | 40.0340 |
| `qr/n32/b1` | 0.0209 | 0.0453 | 0.0120 |
| `qr/n32/b128` | 2.6084 | 0.6562 | 1.5589 |
| `rank_revealing_qr/n128/b1` | 0.3465 | 0.3647 | 0.4273 |
| `rank_revealing_qr/n128/b128` | 43.8896 | 47.2730 | 61.0958 |
| `rank_revealing_qr/n32/b1` | 0.0206 | 0.0468 | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6407 | 1.2985 | 2.2897 |
| `solve/n128/b1` | 0.0674 | 0.0816 | 0.0905 |
| `solve/n128/b128` | 8.8320 | 10.5053 | 12.1014 |
| `solve/n32/b1` | 0.0048 | 0.0069 | 0.0082 |
| `solve/n32/b128` | 0.5302 | 0.2685 | 1.0003 |
| `svd_thin/n128/b1` | 2.4270 | 1.8125 | 1.6046 |
| `svd_thin/n128/b128` | 307.9833 | 230.8849 | 210.0428 |
| `svd_thin/n32/b1` | 0.1170 | 0.1215 | 0.1117 |
| `svd_thin/n32/b128` | 15.1038 | 3.7933 | 14.4778 |
| `svd_values/n128/b1` | 1.4159 | 1.4321 | 0.6853 |
| `svd_values/n128/b128` | 180.9724 | 180.5406 | 89.1559 |
| `svd_values/n32/b1` | 0.0925 | 0.0967 | 0.0372 |
| `svd_values/n32/b128` | 11.9094 | 5.2565 | 4.8614 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0065 | 0.0060 |
| `triangular_solve/n128/b128` | 0.7829 | 0.7634 | 1.3868 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0025 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0876 | 0.0284 | 0.1782 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0391 | 0.0532 | 0.0553 |
| `cholesky/n128/b128` | 6.0046 | 7.3236 | 8.2944 |
| `cholesky/n32/b1` | 0.0021 | 0.0052 | 0.0022 |
| `cholesky/n32/b128` | 0.2569 | 0.0361 | 0.2565 |
| `eigh/n128/b1` | 1.2675 | 1.2497 | 0.5872 |
| `eigh/n128/b128` | 164.7906 | 159.9566 | 79.3621 |
| `eigh/n32/b1` | 0.0643 | 0.0686 | 0.0589 |
| `eigh/n32/b128` | 8.4645 | 1.4954 | 7.5597 |
| `eigvalsh/n128/b1` | 0.6958 | 0.7090 | 0.4484 |
| `eigvalsh/n128/b128` | 91.0327 | 90.2495 | 58.1083 |
| `eigvalsh/n32/b1` | 0.0488 | 0.0516 | 0.0246 |
| `eigvalsh/n32/b128` | 6.4033 | 1.3793 | 3.2324 |
| `householder_apply/n128/b1` | 0.1240 | 0.1740 | 0.0570 |
| `householder_apply/n128/b128` | 17.3946 | 24.6753 | 7.3892 |
| `householder_apply/n32/b1` | 0.0111 | 0.0131 | 0.0073 |
| `householder_apply/n32/b128` | 1.3709 | 0.3466 | 0.9118 |
| `householder_factor/n128/b1` | 0.1042 | 0.1730 | 0.0898 |
| `householder_factor/n128/b128` | 13.6665 | 22.9993 | 11.6623 |
| `householder_factor/n32/b1` | 0.0073 | 0.0180 | 0.0067 |
| `householder_factor/n32/b128` | 0.9317 | 0.2417 | 0.9176 |
| `lu/n128/b1` | 0.0991 | 0.1262 | 0.0821 |
| `lu/n128/b128` | 13.0560 | 16.9194 | 13.0163 |
| `lu/n32/b1` | 0.0059 | 0.0098 | 0.0063 |
| `lu/n32/b128` | 0.6555 | 0.1701 | 0.7729 |
| `lu_factor/n128/b1` | 0.0559 | 0.0818 | 0.0728 |
| `lu_factor/n128/b128` | 8.2502 | 2.4841 | 10.0546 |
| `lu_factor/n32/b1` | 0.0033 | 0.0065 | 0.0053 |
| `lu_factor/n32/b128` | 0.3925 | 0.1088 | 0.6551 |
| `lu_factor_solve/n128/b1` | 0.0628 | 0.0907 | 0.0868 |
| `lu_factor_solve/n128/b128` | 8.8833 | 1.5528 | 11.8376 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0078 | 0.0077 |
| `lu_factor_solve/n32/b128` | 0.4893 | 0.0711 | 1.0128 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0094 | 0.0098 |
| `lu_solve_prepared/n128/b128` | 2.0533 | 0.5144 | 2.2702 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0047 | 0.0025 |
| `lu_solve_prepared/n32/b128` | 0.1134 | 0.0344 | 0.3265 |
| `qr/n128/b1` | 0.3392 | 0.9071 | 0.2777 |
| `qr/n128/b128` | 44.7296 | 121.5122 | 39.3366 |
| `qr/n32/b1` | 0.0208 | 0.0630 | 0.0121 |
| `qr/n32/b128` | 2.6224 | 0.6550 | 1.5434 |
| `rank_revealing_qr/n128/b1` | 0.3421 | 0.4240 | 0.4888 |
| `rank_revealing_qr/n128/b128` | 44.6511 | 55.6605 | 62.6215 |
| `rank_revealing_qr/n32/b1` | 0.0210 | 0.0674 | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.5625 | 0.6465 | 2.3005 |
| `solve/n128/b1` | 0.0675 | 0.0942 | 0.0905 |
| `solve/n128/b128` | 8.8240 | 11.8995 | 12.2110 |
| `solve/n32/b1` | 0.0048 | 0.0078 | 0.0083 |
| `solve/n32/b128` | 0.5312 | 0.1400 | 0.9940 |
| `svd_thin/n128/b1` | 2.4110 | 1.8648 | 1.5417 |
| `svd_thin/n128/b128` | 308.2578 | 238.4537 | 199.9469 |
| `svd_thin/n32/b1` | 0.1174 | 0.1213 | 0.1124 |
| `svd_thin/n32/b128` | 15.2345 | 2.0437 | 14.5538 |
| `svd_values/n128/b1` | 1.4009 | 1.4388 | 0.6741 |
| `svd_values/n128/b128` | 180.0892 | 180.8843 | 89.2269 |
| `svd_values/n32/b1` | 0.0923 | 0.0969 | 0.0372 |
| `svd_values/n32/b128` | 12.0149 | 1.9633 | 4.8408 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0071 | 0.0062 |
| `triangular_solve/n128/b128` | 0.9956 | 1.0393 | 1.3221 |
| `triangular_solve/n32/b1` | 0.0009 | 0.0033 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0971 | 0.0256 | 0.1847 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1088 | - | 0.2444 |
| `cholesky/n128/b128` | 16.0165 | - | 32.9300 |
| `cholesky/n32/b1` | 0.0033 | - | 0.0048 |
| `cholesky/n32/b128` | 0.4314 | - | 0.6309 |
| `eigh/n128/b1` | 1.8416 | - | 2.9709 |
| `eigh/n128/b128` | 241.6675 | - | 384.5171 |
| `eigh/n32/b1` | 0.0808 | - | 0.0867 |
| `eigh/n32/b128` | 10.5396 | - | 11.3429 |
| `eigvalsh/n128/b1` | 0.9287 | - | 1.2661 |
| `eigvalsh/n128/b128` | 121.8667 | - | 163.7471 |
| `eigvalsh/n32/b1` | 0.0527 | - | 0.0441 |
| `eigvalsh/n32/b128` | 6.9747 | - | 5.7583 |
| `householder_apply/n128/b1` | 0.4850 | - | 0.9698 |
| `householder_apply/n128/b128` | 65.7947 | - | 126.3523 |
| `householder_apply/n32/b1` | 0.0142 | - | 0.0197 |
| `householder_apply/n32/b128` | 1.8700 | - | 2.5690 |
| `householder_factor/n128/b1` | 0.3499 | - | 0.5400 |
| `householder_factor/n128/b128` | 45.5209 | - | 70.5140 |
| `householder_factor/n32/b1` | 0.0113 | - | 0.0155 |
| `householder_factor/n32/b128` | 1.4376 | - | 2.0088 |
| `lu/n128/b1` | 0.2001 | - | 0.2702 |
| `lu/n128/b128` | 28.0571 | - | 38.8125 |
| `lu/n32/b1` | 0.0079 | - | 0.0107 |
| `lu/n32/b128` | 1.0159 | - | 1.4455 |
| `lu_factor/n128/b1` | 0.1562 | - | 0.2494 |
| `lu_factor/n128/b128` | 21.8444 | - | 32.6899 |
| `lu_factor/n32/b1` | 0.0054 | - | 0.0089 |
| `lu_factor/n32/b128` | 0.6509 | - | 1.1437 |
| `lu_factor_solve/n128/b1` | 0.1755 | - | 0.2816 |
| `lu_factor_solve/n128/b128` | 24.2191 | - | 36.8364 |
| `lu_factor_solve/n32/b1` | 0.0075 | - | 0.0133 |
| `lu_factor_solve/n32/b128` | 0.9224 | - | 1.7110 |
| `lu_solve_prepared/n128/b1` | 0.0188 | - | 0.0313 |
| `lu_solve_prepared/n128/b128` | 4.2636 | - | 5.7787 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0044 |
| `lu_solve_prepared/n32/b128` | 0.2860 | - | 0.5605 |
| `qr/n128/b1` | 0.9726 | - | 1.1448 |
| `qr/n128/b128` | 125.4499 | - | 148.3617 |
| `qr/n32/b1` | 0.0421 | - | 0.0283 |
| `qr/n32/b128` | 5.4095 | - | 3.6611 |
| `rank_revealing_qr/n128/b1` | 1.0108 | - | 1.5913 |
| `rank_revealing_qr/n128/b128` | 131.4839 | - | 207.4592 |
| `rank_revealing_qr/n32/b1` | 0.0390 | - | 0.0391 |
| `rank_revealing_qr/n32/b128` | 4.9977 | - | 5.1305 |
| `solve/n128/b1` | 0.1800 | - | 0.2862 |
| `solve/n128/b128` | 23.8579 | - | 37.7827 |
| `solve/n32/b1` | 0.0082 | - | 0.0139 |
| `solve/n32/b128` | 0.9601 | - | 1.7590 |
| `svd_thin/n128/b1` | 3.9236 | - | 4.1968 |
| `svd_thin/n128/b128` | 507.1036 | - | 540.7529 |
| `svd_thin/n32/b1` | 0.1505 | - | 0.1536 |
| `svd_thin/n32/b128` | 19.7075 | - | 20.7339 |
| `svd_values/n128/b1` | 1.8859 | - | 1.5963 |
| `svd_values/n128/b128` | 244.7312 | - | 207.1037 |
| `svd_values/n32/b1` | 0.1007 | - | 0.0613 |
| `svd_values/n32/b128` | 13.3446 | - | 8.0137 |
| `triangular_solve/n128/b1` | 0.0109 | - | 0.0153 |
| `triangular_solve/n128/b128` | 2.3086 | - | 2.8332 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0021 |
| `triangular_solve/n32/b128` | 0.1897 | - | 0.2644 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1087 | 0.1094 | 0.2440 |
| `cholesky/n128/b128` | 15.9660 | 15.7452 | 32.8922 |
| `cholesky/n32/b1` | 0.0034 | 0.0068 | 0.0048 |
| `cholesky/n32/b128` | 0.4252 | 0.2157 | 0.6228 |
| `eigh/n128/b1` | 1.8551 | 1.7447 | 1.8024 |
| `eigh/n128/b128` | 241.9459 | 228.7226 | 236.0583 |
| `eigh/n32/b1` | 0.0808 | 0.0857 | 0.0869 |
| `eigh/n32/b128` | 10.5472 | 2.6495 | 11.3411 |
| `eigvalsh/n128/b1` | 0.9313 | 0.9295 | 0.8160 |
| `eigvalsh/n128/b128` | 121.9796 | 121.5035 | 106.7836 |
| `eigvalsh/n32/b1` | 0.0528 | 0.0557 | 0.0440 |
| `eigvalsh/n32/b128` | 6.9880 | 2.2282 | 5.7793 |
| `householder_apply/n128/b1` | 0.4859 | 0.2602 | 0.2755 |
| `householder_apply/n128/b128` | 64.4574 | 35.1487 | 37.7234 |
| `householder_apply/n32/b1` | 0.0145 | 0.0172 | 0.0197 |
| `householder_apply/n32/b128` | 1.8756 | 0.4680 | 2.5761 |
| `householder_factor/n128/b1` | 0.3505 | 0.2267 | 0.2599 |
| `householder_factor/n128/b128` | 45.5537 | 29.9375 | 33.8337 |
| `householder_factor/n32/b1` | 0.0114 | 0.0143 | 0.0156 |
| `householder_factor/n32/b128` | 1.4382 | 0.3703 | 2.0191 |
| `lu/n128/b1` | 0.2013 | 0.1903 | 0.2703 |
| `lu/n128/b128` | 28.3597 | 26.5995 | 38.6928 |
| `lu/n32/b1` | 0.0079 | 0.0108 | 0.0105 |
| `lu/n32/b128` | 1.0793 | 0.5032 | 1.4342 |
| `lu_factor/n128/b1` | 0.1561 | 0.1468 | 0.2493 |
| `lu_factor/n128/b128` | 21.7547 | 6.2603 | 32.7808 |
| `lu_factor/n32/b1` | 0.0053 | 0.0088 | 0.0090 |
| `lu_factor/n32/b128` | 0.6418 | 0.2399 | 1.1447 |
| `lu_factor_solve/n128/b1` | 0.1751 | 0.1651 | 0.2691 |
| `lu_factor_solve/n128/b128` | 24.5565 | 6.5053 | 35.2864 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0106 | 0.0118 |
| `lu_factor_solve/n32/b128` | 0.9224 | 0.2324 | 1.5654 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0220 | 0.0152 |
| `lu_solve_prepared/n128/b128` | 4.0799 | 1.5240 | 3.7731 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0048 | 0.0025 |
| `lu_solve_prepared/n32/b128` | 0.2781 | 0.0750 | 0.3649 |
| `qr/n128/b1` | 0.9585 | 0.8911 | 0.5946 |
| `qr/n128/b128` | 125.1439 | 114.2228 | 77.9781 |
| `qr/n32/b1` | 0.0427 | 0.0697 | 0.0285 |
| `qr/n32/b128` | 5.3917 | 2.7348 | 3.6811 |
| `rank_revealing_qr/n128/b1` | 1.0038 | 0.8148 | 1.3741 |
| `rank_revealing_qr/n128/b128` | 130.5476 | 105.2902 | 178.9015 |
| `rank_revealing_qr/n32/b1` | 0.0392 | 0.0649 | 0.0389 |
| `rank_revealing_qr/n32/b128` | 5.1027 | 2.5140 | 5.1412 |
| `solve/n128/b1` | 0.1797 | 0.1698 | 0.2802 |
| `solve/n128/b128` | 23.8865 | 22.0547 | 36.5653 |
| `solve/n32/b1` | 0.0083 | 0.0107 | 0.0125 |
| `solve/n32/b128` | 0.9724 | 0.2735 | 1.5881 |
| `svd_thin/n128/b1` | 3.9218 | 2.7077 | 2.5166 |
| `svd_thin/n128/b128` | 510.0101 | 350.2013 | 326.2254 |
| `svd_thin/n32/b1` | 0.1503 | 0.1554 | 0.1574 |
| `svd_thin/n32/b128` | 20.3179 | 7.7512 | 21.2227 |
| `svd_values/n128/b1` | 1.8864 | 1.9116 | 1.2180 |
| `svd_values/n128/b128` | 245.2434 | 244.3568 | 157.7511 |
| `svd_values/n32/b1` | 0.1008 | 0.1052 | 0.0607 |
| `svd_values/n32/b128` | 13.2603 | 3.4046 | 7.9586 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0138 | 0.0078 |
| `triangular_solve/n128/b128` | 2.1856 | 2.2670 | 2.3191 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0044 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1919 | 0.0988 | 0.1870 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1080 | 0.1152 | 0.2445 |
| `cholesky/n128/b128` | 16.1720 | 16.7023 | 33.1054 |
| `cholesky/n32/b1` | 0.0034 | 0.0065 | 0.0048 |
| `cholesky/n32/b128` | 0.4266 | 0.0581 | 0.6262 |
| `eigh/n128/b1` | 1.8552 | 1.6256 | 1.6240 |
| `eigh/n128/b128` | 242.0601 | 212.1532 | 211.6477 |
| `eigh/n32/b1` | 0.0808 | 0.0852 | 0.0866 |
| `eigh/n32/b128` | 10.5260 | 2.6804 | 11.2996 |
| `eigvalsh/n128/b1` | 0.9253 | 0.9313 | 0.7364 |
| `eigvalsh/n128/b128` | 122.3706 | 121.3762 | 96.7844 |
| `eigvalsh/n32/b1` | 0.0527 | 0.0567 | 0.0441 |
| `eigvalsh/n32/b128` | 6.9692 | 0.9394 | 5.7637 |
| `householder_apply/n128/b1` | 0.4874 | 0.3504 | 0.1725 |
| `householder_apply/n128/b128` | 64.3413 | 44.7778 | 21.9138 |
| `householder_apply/n32/b1` | 0.0144 | 0.0176 | 0.0196 |
| `householder_apply/n32/b128` | 1.8551 | 0.4672 | 2.6295 |
| `householder_factor/n128/b1` | 0.3447 | 0.2857 | 0.1783 |
| `householder_factor/n128/b128` | 45.6633 | 36.6049 | 23.5180 |
| `householder_factor/n32/b1` | 0.0114 | 0.0139 | 0.0156 |
| `householder_factor/n32/b128` | 1.4513 | 0.3622 | 2.0046 |
| `lu/n128/b1` | 0.2013 | 0.1994 | 0.2710 |
| `lu/n128/b128` | 28.1916 | 28.0761 | 38.7587 |
| `lu/n32/b1` | 0.0079 | 0.0107 | 0.0105 |
| `lu/n32/b128` | 1.0480 | 0.2435 | 1.4289 |
| `lu_factor/n128/b1` | 0.1551 | 0.1518 | 0.2468 |
| `lu_factor/n128/b128` | 21.8308 | 3.2855 | 32.6817 |
| `lu_factor/n32/b1` | 0.0053 | 0.0081 | 0.0090 |
| `lu_factor/n32/b128` | 0.6421 | 0.0897 | 1.1380 |
| `lu_factor_solve/n128/b1` | 0.1743 | 0.1726 | 0.2653 |
| `lu_factor_solve/n128/b128` | 24.2065 | 3.5793 | 35.3367 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0098 | 0.0119 |
| `lu_factor_solve/n32/b128` | 0.9175 | 0.2448 | 1.5431 |
| `lu_solve_prepared/n128/b1` | 0.0187 | 0.0217 | 0.0151 |
| `lu_solve_prepared/n128/b128` | 4.3168 | 1.1579 | 3.6623 |
| `lu_solve_prepared/n32/b1` | 0.0022 | 0.0054 | 0.0026 |
| `lu_solve_prepared/n32/b128` | 0.2837 | 0.0772 | 0.3600 |
| `qr/n128/b1` | 0.9800 | 1.2068 | 0.4327 |
| `qr/n128/b128` | 125.1969 | 153.9733 | 57.5228 |
| `qr/n32/b1` | 0.0426 | 0.0884 | 0.0283 |
| `qr/n32/b128` | 5.4478 | 1.3792 | 3.6617 |
| `rank_revealing_qr/n128/b1` | 1.0174 | 0.8800 | 1.2220 |
| `rank_revealing_qr/n128/b128` | 130.5718 | 115.0892 | 159.5491 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0865 | 0.0389 |
| `rank_revealing_qr/n32/b128` | 4.9844 | 0.6362 | 5.1440 |
| `solve/n128/b1` | 0.1802 | 0.1832 | 0.2796 |
| `solve/n128/b128` | 23.7924 | 23.5869 | 36.4627 |
| `solve/n32/b1` | 0.0082 | 0.0198 | 0.0126 |
| `solve/n32/b128` | 0.9665 | 0.2450 | 1.6073 |
| `svd_thin/n128/b1` | 3.9456 | 2.7785 | 2.2163 |
| `svd_thin/n128/b128` | 508.2649 | 358.4924 | 285.7522 |
| `svd_thin/n32/b1` | 0.1506 | 0.1548 | 0.1593 |
| `svd_thin/n32/b128` | 19.5935 | 2.5290 | 21.4664 |
| `svd_values/n128/b1` | 1.8843 | 1.9137 | 1.1562 |
| `svd_values/n128/b128` | 244.5741 | 243.8191 | 150.7180 |
| `svd_values/n32/b1` | 0.1007 | 0.1051 | 0.0608 |
| `svd_values/n32/b128` | 13.2795 | 1.6979 | 7.9032 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0138 | 0.0078 |
| `triangular_solve/n128/b128` | 2.2806 | 2.2994 | 2.2456 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0055 | 0.0016 |
| `triangular_solve/n32/b128` | 0.1899 | 0.0349 | 0.1814 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2006 | - | 0.2661 |
| `cholesky/n256/b4` | 0.8094 | - | 1.0665 |
| `cholesky/n512/b1` | 1.2925 | - | 1.9957 |
| `cholesky/n512/b4` | 5.5231 | - | 8.4056 |
| `eigh/n256/b1` | 5.6043 | - | 5.9212 |
| `eigh/n256/b4` | 22.5462 | - | 23.8845 |
| `eigh/n512/b1` | 28.8632 | - | 36.7059 |
| `eigh/n512/b4` | 115.9117 | - | 146.3594 |
| `eigvalsh/n256/b1` | 2.9158 | - | 2.5706 |
| `eigvalsh/n256/b4` | 11.9165 | - | 10.3337 |
| `eigvalsh/n512/b1` | 14.3381 | - | 16.6019 |
| `eigvalsh/n512/b4` | 57.7705 | - | 66.2972 |
| `householder_apply/n256/b1` | 0.8201 | - | 1.9400 |
| `householder_apply/n256/b4` | 3.3001 | - | 7.7947 |
| `householder_apply/n512/b1` | 5.9824 | - | 12.8378 |
| `householder_apply/n512/b4` | 25.2541 | - | 52.5053 |
| `householder_factor/n256/b1` | 0.6138 | - | 1.1185 |
| `householder_factor/n256/b4` | 2.4897 | - | 4.5218 |
| `householder_factor/n512/b1` | 4.3509 | - | 8.0787 |
| `householder_factor/n512/b4` | 17.5795 | - | 32.1496 |
| `lu/n256/b1` | 0.5072 | - | 0.4996 |
| `lu/n256/b4` | 2.0471 | - | 2.1499 |
| `lu/n512/b1` | 3.2954 | - | 3.3152 |
| `lu/n512/b4` | 13.3054 | - | 13.5712 |
| `lu_factor/n256/b1` | 0.3528 | - | 0.4569 |
| `lu_factor/n256/b4` | 1.5330 | - | 1.8379 |
| `lu_factor/n512/b1` | 2.7553 | - | 3.0049 |
| `lu_factor/n512/b4` | 11.7425 | - | 12.3672 |
| `lu_factor_solve/n256/b1` | 0.3700 | - | 0.4995 |
| `lu_factor_solve/n256/b4` | 1.5993 | - | 2.0123 |
| `lu_factor_solve/n512/b1` | 2.8177 | - | 3.1867 |
| `lu_factor_solve/n512/b4` | 11.9726 | - | 13.1621 |
| `lu_solve_prepared/n256/b1` | 0.0168 | - | 0.0398 |
| `lu_solve_prepared/n256/b4` | 0.0812 | - | 0.1731 |
| `lu_solve_prepared/n512/b1` | 0.0711 | - | 0.1937 |
| `lu_solve_prepared/n512/b4` | 0.3711 | - | 0.9856 |
| `qr/n256/b1` | 1.8561 | - | 2.3702 |
| `qr/n256/b4` | 7.4010 | - | 9.5648 |
| `qr/n512/b1` | 11.5157 | - | 17.1453 |
| `qr/n512/b4` | 46.0800 | - | 69.4989 |
| `rank_revealing_qr/n256/b1` | 2.0930 | - | 2.9399 |
| `rank_revealing_qr/n256/b4` | 8.4579 | - | 11.8520 |
| `rank_revealing_qr/n512/b1` | 14.9219 | - | 21.2563 |
| `rank_revealing_qr/n512/b4` | 59.7666 | - | 86.2408 |
| `solve/n256/b1` | 0.3865 | - | 0.5104 |
| `solve/n256/b4` | 1.5361 | - | 2.0425 |
| `solve/n512/b1` | 2.8555 | - | 3.2296 |
| `solve/n512/b4` | 11.3878 | - | 13.0015 |
| `svd_thin/n256/b1` | 12.2428 | - | 10.9175 |
| `svd_thin/n256/b4` | 49.2106 | - | 43.7659 |
| `svd_thin/n512/b1` | 70.8796 | - | 71.5032 |
| `svd_thin/n512/b4` | 283.1640 | - | 291.7431 |
| `svd_values/n256/b1` | 6.9683 | - | 4.1109 |
| `svd_values/n256/b4` | 27.7603 | - | 16.5694 |
| `svd_values/n512/b1` | 38.7328 | - | 28.3279 |
| `svd_values/n512/b4` | 154.6043 | - | 114.9374 |
| `triangular_solve/n256/b1` | 0.0104 | - | 0.0235 |
| `triangular_solve/n256/b4` | 0.0428 | - | 0.0975 |
| `triangular_solve/n512/b1` | 0.0346 | - | 0.0937 |
| `triangular_solve/n512/b4` | 0.1461 | - | 0.4020 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2010 | 0.1855 | 0.1638 |
| `cholesky/n256/b4` | 0.8102 | 0.7559 | 0.6847 |
| `cholesky/n512/b1` | 1.2946 | 0.8259 | 0.8925 |
| `cholesky/n512/b4` | 5.6331 | 3.6222 | 4.0294 |
| `eigh/n256/b1` | 5.5848 | 4.6612 | 2.7995 |
| `eigh/n256/b4` | 22.3787 | 17.1143 | 11.3057 |
| `eigh/n512/b1` | 28.6967 | 15.9044 | 13.1665 |
| `eigh/n512/b4` | 115.2253 | 63.9788 | 53.1121 |
| `eigvalsh/n256/b1` | 2.9478 | 2.9537 | 1.8743 |
| `eigvalsh/n256/b4` | 11.9901 | 11.8523 | 7.4964 |
| `eigvalsh/n512/b1` | 14.3595 | 11.9492 | 8.9348 |
| `eigvalsh/n512/b4` | 57.5379 | 47.9513 | 35.9823 |
| `householder_apply/n256/b1` | 0.8263 | 0.3294 | 0.5745 |
| `householder_apply/n256/b4` | 3.3033 | 1.3133 | 2.2971 |
| `householder_apply/n512/b1` | 6.1414 | 1.8006 | 3.5019 |
| `householder_apply/n512/b4` | 25.1228 | 7.5210 | 14.1752 |
| `householder_factor/n256/b1` | 0.6235 | 0.3505 | 0.3676 |
| `householder_factor/n256/b4` | 2.4704 | 1.3869 | 1.4525 |
| `householder_factor/n512/b1` | 4.3417 | 1.6383 | 2.1853 |
| `householder_factor/n512/b4` | 17.4645 | 6.7101 | 8.8437 |
| `lu/n256/b1` | 0.4937 | 0.4618 | 0.2014 |
| `lu/n256/b4` | 2.0581 | 1.9269 | 0.8973 |
| `lu/n512/b1` | 3.2910 | 2.0765 | 1.1383 |
| `lu/n512/b4` | 13.2185 | 8.1358 | 4.8928 |
| `lu_factor/n256/b1` | 0.3831 | 0.3248 | 0.1593 |
| `lu_factor/n256/b4` | 1.5250 | 0.7723 | 0.6502 |
| `lu_factor/n512/b1` | 2.8461 | 1.4661 | 0.8480 |
| `lu_factor/n512/b4` | 11.7579 | 3.5040 | 3.4828 |
| `lu_factor_solve/n256/b1` | 0.3737 | 0.3349 | 0.1931 |
| `lu_factor_solve/n256/b4` | 1.4778 | 0.7802 | 0.7658 |
| `lu_factor_solve/n512/b1` | 2.8952 | 1.5440 | 0.9616 |
| `lu_factor_solve/n512/b4` | 12.0689 | 3.2067 | 3.9232 |
| `lu_solve_prepared/n256/b1` | 0.0170 | 0.0240 | 0.0246 |
| `lu_solve_prepared/n256/b4` | 0.0743 | 0.0389 | 0.1240 |
| `lu_solve_prepared/n512/b1` | 0.0618 | 0.0631 | 0.0970 |
| `lu_solve_prepared/n512/b4` | 0.4424 | 0.1822 | 0.5520 |
| `qr/n256/b1` | 1.8492 | 1.6782 | 1.1414 |
| `qr/n256/b4` | 7.4061 | 7.0720 | 4.6597 |
| `qr/n512/b1` | 11.5270 | 6.0422 | 6.9195 |
| `qr/n512/b4` | 46.0412 | 24.1570 | 28.0170 |
| `rank_revealing_qr/n256/b1` | 2.1195 | 1.4770 | 2.3200 |
| `rank_revealing_qr/n256/b4` | 8.5104 | 5.8925 | 9.2865 |
| `rank_revealing_qr/n512/b1` | 14.8011 | 6.2174 | 15.7190 |
| `rank_revealing_qr/n512/b4` | 59.2440 | 24.7877 | 63.4986 |
| `solve/n256/b1` | 0.3861 | 0.3661 | 0.2091 |
| `solve/n256/b4` | 1.5398 | 1.4195 | 0.8397 |
| `solve/n512/b1` | 2.9020 | 1.5646 | 1.0212 |
| `solve/n512/b4` | 11.4288 | 6.2650 | 4.1428 |
| `svd_thin/n256/b1` | 12.2351 | 8.7966 | 7.6682 |
| `svd_thin/n256/b4` | 49.0179 | 35.7581 | 30.8160 |
| `svd_thin/n512/b1` | 71.0354 | 40.2937 | 37.1937 |
| `svd_thin/n512/b4` | 282.5374 | 160.7355 | 149.4251 |
| `svd_values/n256/b1` | 6.9546 | 7.1593 | 3.6971 |
| `svd_values/n256/b4` | 27.8253 | 28.1539 | 14.9757 |
| `svd_values/n512/b1` | 38.9064 | 31.8572 | 15.6547 |
| `svd_values/n512/b4` | 154.7913 | 126.9749 | 62.6589 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0157 | 0.0151 |
| `triangular_solve/n256/b4` | 0.0461 | 0.0562 | 0.0749 |
| `triangular_solve/n512/b1` | 0.0361 | 0.0358 | 0.0575 |
| `triangular_solve/n512/b4` | 0.1426 | 0.1401 | 0.2521 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1994 | 0.1957 | 0.1599 |
| `cholesky/n256/b4` | 0.7977 | 0.8345 | 0.4767 |
| `cholesky/n512/b1` | 1.2628 | 0.7030 | 0.5511 |
| `cholesky/n512/b4` | 5.5564 | 3.2272 | 2.7253 |
| `eigh/n256/b1` | 5.5947 | 4.1377 | 2.3302 |
| `eigh/n256/b4` | 22.5498 | 16.7849 | 9.3944 |
| `eigh/n512/b1` | 29.1244 | 14.6352 | 9.3264 |
| `eigh/n512/b4` | 116.0454 | 60.0246 | 37.5175 |
| `eigvalsh/n256/b1` | 2.9028 | 2.9591 | 1.7833 |
| `eigvalsh/n256/b4` | 11.8674 | 11.8785 | 7.1628 |
| `eigvalsh/n512/b1` | 14.2620 | 11.5111 | 7.6219 |
| `eigvalsh/n512/b4` | 56.9935 | 46.9464 | 30.6800 |
| `householder_apply/n256/b1` | 0.8250 | 0.3976 | 0.3172 |
| `householder_apply/n256/b4` | 3.3153 | 1.6933 | 1.2416 |
| `householder_apply/n512/b1` | 6.2521 | 1.8273 | 1.9302 |
| `householder_apply/n512/b4` | 25.1775 | 7.6110 | 8.0002 |
| `householder_factor/n256/b1` | 0.6220 | 0.4356 | 0.3197 |
| `householder_factor/n256/b4` | 2.5018 | 1.7140 | 1.2759 |
| `householder_factor/n512/b1` | 4.3563 | 1.7459 | 1.3006 |
| `householder_factor/n512/b4` | 17.7259 | 7.2406 | 5.3877 |
| `lu/n256/b1` | 0.4933 | 0.4817 | 0.1870 |
| `lu/n256/b4` | 2.0632 | 2.0623 | 0.8601 |
| `lu/n512/b1` | 3.2874 | 2.0860 | 0.9090 |
| `lu/n512/b4` | 13.3007 | 8.2844 | 3.8802 |
| `lu_factor/n256/b1` | 0.3779 | 0.3683 | 0.1522 |
| `lu_factor/n256/b4` | 1.5357 | 1.4595 | 0.6138 |
| `lu_factor/n512/b1` | 2.8244 | 1.5102 | 0.6197 |
| `lu_factor/n512/b4` | 11.7792 | 6.1625 | 2.4428 |
| `lu_factor_solve/n256/b1` | 0.3713 | 0.3762 | 0.1912 |
| `lu_factor_solve/n256/b4` | 1.4915 | 1.5114 | 0.7738 |
| `lu_factor_solve/n512/b1` | 2.8889 | 1.5910 | 0.7220 |
| `lu_factor_solve/n512/b4` | 12.0100 | 6.5563 | 2.9992 |
| `lu_solve_prepared/n256/b1` | 0.0171 | 0.0289 | 0.0243 |
| `lu_solve_prepared/n256/b4` | 0.0824 | 0.1110 | 0.1289 |
| `lu_solve_prepared/n512/b1` | 0.0721 | 0.0781 | 0.0981 |
| `lu_solve_prepared/n512/b4` | 0.4402 | 0.3835 | 0.5965 |
| `qr/n256/b1` | 1.8563 | 2.4298 | 1.1122 |
| `qr/n256/b4` | 7.3941 | 9.8372 | 4.4752 |
| `qr/n512/b1` | 11.5112 | 6.8879 | 5.3027 |
| `qr/n512/b4` | 46.2443 | 28.1254 | 21.5147 |
| `rank_revealing_qr/n256/b1` | 2.0963 | 1.5634 | 2.2146 |
| `rank_revealing_qr/n256/b4` | 8.3573 | 6.2529 | 8.8693 |
| `rank_revealing_qr/n512/b1` | 14.9427 | 5.7352 | 14.8602 |
| `rank_revealing_qr/n512/b4` | 59.3169 | 23.0482 | 59.9923 |
| `solve/n256/b1` | 0.3843 | 0.4169 | 0.2105 |
| `solve/n256/b4` | 1.5290 | 1.6020 | 0.8322 |
| `solve/n512/b1` | 2.8571 | 1.6724 | 0.7546 |
| `solve/n512/b4` | 11.3667 | 6.5911 | 3.2264 |
| `svd_thin/n256/b1` | 12.2358 | 8.9474 | 7.1135 |
| `svd_thin/n256/b4` | 48.9039 | 35.8687 | 28.4902 |
| `svd_thin/n512/b1` | 70.6882 | 38.4280 | 30.7350 |
| `svd_thin/n512/b4` | 284.9853 | 154.0407 | 123.7422 |
| `svd_values/n256/b1` | 6.9745 | 7.1535 | 3.6380 |
| `svd_values/n256/b4` | 27.7680 | 28.4858 | 14.6832 |
| `svd_values/n512/b1` | 38.9471 | 32.2141 | 13.4736 |
| `svd_values/n512/b4` | 156.3995 | 128.5026 | 54.3115 |
| `triangular_solve/n256/b1` | 0.0103 | 0.0187 | 0.0155 |
| `triangular_solve/n256/b4` | 0.0468 | 0.0619 | 0.0753 |
| `triangular_solve/n512/b1` | 0.0342 | 0.0419 | 0.0568 |
| `triangular_solve/n512/b4` | 0.1611 | 0.1786 | 0.2575 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7046 | - | 1.0893 |
| `cholesky/n256/b4` | 2.8413 | - | 4.4379 |
| `cholesky/n512/b1` | 4.8279 | - | 7.5419 |
| `cholesky/n512/b4` | 19.4847 | - | 26.2477 |
| `eigh/n256/b1` | 10.2832 | - | 20.8325 |
| `eigh/n256/b4` | 41.2539 | - | 84.5114 |
| `eigh/n512/b1` | 62.7608 | - | 153.6271 |
| `eigh/n512/b4` | 252.6157 | - | 610.4404 |
| `eigvalsh/n256/b1` | 4.9685 | - | 8.1104 |
| `eigvalsh/n256/b4` | 19.9016 | - | 32.5945 |
| `eigvalsh/n512/b1` | 29.5769 | - | 58.0475 |
| `eigvalsh/n512/b4` | 118.8621 | - | 232.2968 |
| `householder_apply/n256/b1` | 3.3795 | - | 6.3156 |
| `householder_apply/n256/b4` | 13.5514 | - | 24.7221 |
| `householder_apply/n512/b1` | 24.6468 | - | 36.9511 |
| `householder_apply/n512/b4` | 99.1108 | - | 151.9129 |
| `householder_factor/n256/b1` | 2.3204 | - | 3.2909 |
| `householder_factor/n256/b4` | 9.3083 | - | 13.2771 |
| `householder_factor/n512/b1` | 16.6166 | - | 22.7022 |
| `householder_factor/n512/b4` | 66.6430 | - | 92.0529 |
| `lu/n256/b1` | 1.2681 | - | 1.6292 |
| `lu/n256/b4` | 5.1757 | - | 6.8560 |
| `lu/n512/b1` | 8.6659 | - | 11.1166 |
| `lu/n512/b4` | 34.7870 | - | 44.6634 |
| `lu_factor/n256/b1` | 1.1195 | - | 1.5466 |
| `lu_factor/n256/b4` | 4.5083 | - | 6.2694 |
| `lu_factor/n512/b1` | 8.0220 | - | 10.2984 |
| `lu_factor/n512/b4` | 32.5950 | - | 42.2426 |
| `lu_factor_solve/n256/b1` | 1.1836 | - | 1.6737 |
| `lu_factor_solve/n256/b4` | 4.7551 | - | 6.8200 |
| `lu_factor_solve/n512/b1` | 8.2529 | - | 10.7406 |
| `lu_factor_solve/n512/b4` | 33.7633 | - | 43.2417 |
| `lu_solve_prepared/n256/b1` | 0.0618 | - | 0.1148 |
| `lu_solve_prepared/n256/b4` | 0.2540 | - | 0.5248 |
| `lu_solve_prepared/n512/b1` | 0.2200 | - | 0.4110 |
| `lu_solve_prepared/n512/b4` | 1.0838 | - | 2.1348 |
| `qr/n256/b1` | 6.2290 | - | 7.1945 |
| `qr/n256/b4` | 24.9497 | - | 29.0171 |
| `qr/n512/b1` | 42.4284 | - | 47.3138 |
| `qr/n512/b4` | 168.8909 | - | 191.7525 |
| `rank_revealing_qr/n256/b1` | 6.7584 | - | 10.2653 |
| `rank_revealing_qr/n256/b4` | 27.0697 | - | 41.3053 |
| `rank_revealing_qr/n512/b1` | 47.7370 | - | 64.4586 |
| `rank_revealing_qr/n512/b4` | 190.1949 | - | 261.0960 |
| `solve/n256/b1` | 1.1734 | - | 1.7212 |
| `solve/n256/b4` | 4.6687 | - | 6.8168 |
| `solve/n512/b1` | 8.1907 | - | 11.2440 |
| `solve/n512/b4` | 32.6862 | - | 43.7125 |
| `svd_thin/n256/b1` | 24.0407 | - | 26.9218 |
| `svd_thin/n256/b4` | 97.2402 | - | 111.4664 |
| `svd_thin/n512/b1` | 153.1557 | - | 189.4960 |
| `svd_thin/n512/b4` | 610.6983 | - | 751.6553 |
| `svd_values/n256/b1` | 11.0254 | - | 11.7473 |
| `svd_values/n256/b4` | 44.2626 | - | 48.5378 |
| `svd_values/n512/b1` | 66.2008 | - | 90.5634 |
| `svd_values/n512/b4` | 266.2558 | - | 376.0056 |
| `triangular_solve/n256/b1` | 0.0337 | - | 0.0635 |
| `triangular_solve/n256/b4` | 0.1476 | - | 0.2634 |
| `triangular_solve/n512/b1` | 0.1166 | - | 0.2417 |
| `triangular_solve/n512/b4` | 0.6004 | - | 1.0321 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6992 | 0.4937 | 0.3536 |
| `cholesky/n256/b4` | 2.8384 | 2.0200 | 1.4608 |
| `cholesky/n512/b1` | 4.8195 | 2.4879 | 1.9597 |
| `cholesky/n512/b4` | 19.7106 | 10.4396 | 9.0507 |
| `eigh/n256/b1` | 10.2531 | 7.1325 | 9.6672 |
| `eigh/n256/b4` | 41.1198 | 31.9611 | 38.7616 |
| `eigh/n512/b1` | 62.8137 | 28.8355 | 54.8607 |
| `eigh/n512/b4` | 252.0410 | 116.1898 | 219.8621 |
| `eigvalsh/n256/b1` | 4.9662 | 5.0036 | 3.9469 |
| `eigvalsh/n256/b4` | 19.8674 | 19.8497 | 15.8780 |
| `eigvalsh/n512/b1` | 29.5735 | 19.6223 | 21.5067 |
| `eigvalsh/n512/b4` | 118.2519 | 79.9013 | 86.2404 |
| `householder_apply/n256/b1` | 3.3756 | 1.0419 | 1.6886 |
| `householder_apply/n256/b4` | 13.5773 | 4.2513 | 6.8382 |
| `householder_apply/n512/b1` | 24.6539 | 6.7145 | 9.7583 |
| `householder_apply/n512/b4` | 97.1887 | 26.7980 | 39.3087 |
| `householder_factor/n256/b1` | 2.3373 | 0.9502 | 0.9575 |
| `householder_factor/n256/b4` | 9.2966 | 3.8046 | 3.8106 |
| `householder_factor/n512/b1` | 16.6827 | 5.3114 | 6.8149 |
| `householder_factor/n512/b4` | 67.0264 | 21.4959 | 27.3565 |
| `lu/n256/b1` | 1.2562 | 0.8430 | 0.5420 |
| `lu/n256/b4` | 5.1074 | 3.4936 | 2.4312 |
| `lu/n512/b1` | 8.7629 | 3.9179 | 3.7862 |
| `lu/n512/b4` | 34.8201 | 15.6933 | 14.3719 |
| `lu_factor/n256/b1` | 1.1141 | 0.6793 | 0.4318 |
| `lu_factor/n256/b4` | 4.5040 | 1.7276 | 1.7373 |
| `lu_factor/n512/b1` | 8.0227 | 3.1182 | 3.0179 |
| `lu_factor/n512/b4` | 32.7810 | 9.0725 | 12.1611 |
| `lu_factor_solve/n256/b1` | 1.1782 | 0.7361 | 0.4889 |
| `lu_factor_solve/n256/b4` | 4.7559 | 1.2185 | 1.9771 |
| `lu_factor_solve/n512/b1` | 8.3075 | 3.2636 | 3.2701 |
| `lu_factor_solve/n512/b4` | 33.6162 | 9.5409 | 13.1408 |
| `lu_solve_prepared/n256/b1` | 0.0648 | 0.0614 | 0.0525 |
| `lu_solve_prepared/n256/b4` | 0.2562 | 0.0692 | 0.2176 |
| `lu_solve_prepared/n512/b1` | 0.2096 | 0.1595 | 0.2027 |
| `lu_solve_prepared/n512/b4` | 1.0968 | 0.3393 | 1.2058 |
| `qr/n256/b1` | 6.2338 | 3.1673 | 2.8007 |
| `qr/n256/b4` | 24.9097 | 12.4846 | 11.3610 |
| `qr/n512/b1` | 42.3480 | 14.8045 | 16.8441 |
| `qr/n512/b4` | 169.4178 | 58.9977 | 68.1393 |
| `rank_revealing_qr/n256/b1` | 6.7515 | 3.9599 | 7.8506 |
| `rank_revealing_qr/n256/b4` | 27.0971 | 16.0061 | 31.7269 |
| `rank_revealing_qr/n512/b1` | 47.9817 | 16.5387 | 45.2753 |
| `rank_revealing_qr/n512/b4` | 191.8916 | 67.8516 | 181.5246 |
| `solve/n256/b1` | 1.1713 | 0.7411 | 0.5207 |
| `solve/n256/b4` | 4.6592 | 2.9936 | 2.1538 |
| `solve/n512/b1` | 8.2027 | 3.3973 | 3.3171 |
| `solve/n512/b4` | 32.7911 | 13.3705 | 13.7512 |
| `svd_thin/n256/b1` | 24.0222 | 15.8341 | 13.4393 |
| `svd_thin/n256/b4` | 96.3147 | 62.0326 | 54.0674 |
| `svd_thin/n512/b1` | 153.1100 | 68.1532 | 75.1813 |
| `svd_thin/n512/b4` | 610.9811 | 269.0164 | 280.6704 |
| `svd_values/n256/b1` | 11.0816 | 10.9501 | 7.4180 |
| `svd_values/n256/b4` | 44.6821 | 43.5866 | 28.7099 |
| `svd_values/n512/b1` | 66.5006 | 41.9187 | 40.1507 |
| `svd_values/n512/b4` | 265.3135 | 168.0561 | 154.3261 |
| `triangular_solve/n256/b1` | 0.0335 | 0.0332 | 0.0263 |
| `triangular_solve/n256/b4` | 0.1353 | 0.1297 | 0.1124 |
| `triangular_solve/n512/b1` | 0.1139 | 0.0850 | 0.1007 |
| `triangular_solve/n512/b4` | 0.5077 | 0.3705 | 0.5531 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6885 | 0.4648 | 0.2669 |
| `cholesky/n256/b4` | 2.8650 | 1.9853 | 1.1503 |
| `cholesky/n512/b1` | 4.7715 | 1.8133 | 1.0778 |
| `cholesky/n512/b4` | 19.8304 | 7.8662 | 5.3931 |
| `eigh/n256/b1` | 10.2835 | 6.8908 | 7.8247 |
| `eigh/n256/b4` | 41.4511 | 27.9176 | 31.9121 |
| `eigh/n512/b1` | 63.2483 | 24.2579 | 39.3343 |
| `eigh/n512/b4` | 254.9801 | 97.7591 | 160.9205 |
| `eigvalsh/n256/b1` | 4.9872 | 5.0168 | 3.5682 |
| `eigvalsh/n256/b4` | 19.9311 | 19.8686 | 14.3417 |
| `eigvalsh/n512/b1` | 29.7600 | 17.8305 | 17.4504 |
| `eigvalsh/n512/b4` | 119.5861 | 72.0102 | 69.9089 |
| `householder_apply/n256/b1` | 3.3846 | 0.9228 | 0.8645 |
| `householder_apply/n256/b4` | 13.4558 | 3.7737 | 3.6082 |
| `householder_apply/n512/b1` | 24.8699 | 4.5952 | 5.0555 |
| `householder_apply/n512/b4` | 99.0148 | 18.6113 | 20.5992 |
| `householder_factor/n256/b1` | 2.3250 | 0.9728 | 0.9505 |
| `householder_factor/n256/b4` | 9.3300 | 3.9276 | 3.8353 |
| `householder_factor/n512/b1` | 16.6732 | 4.3936 | 3.4248 |
| `householder_factor/n512/b4` | 65.8570 | 17.4321 | 13.4025 |
| `lu/n256/b1` | 1.2691 | 0.8210 | 0.4070 |
| `lu/n256/b4` | 5.0711 | 3.4827 | 1.7823 |
| `lu/n512/b1` | 8.6942 | 3.3482 | 2.3948 |
| `lu/n512/b4` | 34.8754 | 13.2088 | 9.6067 |
| `lu_factor/n256/b1` | 1.1073 | 0.6615 | 0.2927 |
| `lu_factor/n256/b4` | 4.4620 | 2.6764 | 1.1926 |
| `lu_factor/n512/b1` | 8.0133 | 2.5833 | 1.7099 |
| `lu_factor/n512/b4` | 32.6621 | 10.4384 | 6.9984 |
| `lu_factor_solve/n256/b1` | 1.1751 | 0.7278 | 0.3540 |
| `lu_factor_solve/n256/b4` | 4.7359 | 2.9610 | 1.4446 |
| `lu_factor_solve/n512/b1` | 8.1923 | 2.6827 | 1.9350 |
| `lu_factor_solve/n512/b4` | 33.6115 | 11.0682 | 7.9948 |
| `lu_solve_prepared/n256/b1` | 0.0637 | 0.0668 | 0.0526 |
| `lu_solve_prepared/n256/b4` | 0.2738 | 0.2834 | 0.2171 |
| `lu_solve_prepared/n512/b1` | 0.2220 | 0.1719 | 0.2034 |
| `lu_solve_prepared/n512/b4` | 1.2939 | 0.9604 | 1.2713 |
| `qr/n256/b1` | 6.1987 | 3.5216 | 2.2162 |
| `qr/n256/b4` | 25.0330 | 14.0910 | 9.0589 |
| `qr/n512/b1` | 42.3282 | 12.4642 | 9.3997 |
| `qr/n512/b4` | 169.7997 | 50.5692 | 38.5608 |
| `rank_revealing_qr/n256/b1` | 6.7389 | 3.9617 | 6.4143 |
| `rank_revealing_qr/n256/b4` | 27.1654 | 15.3923 | 25.8399 |
| `rank_revealing_qr/n512/b1` | 47.7543 | 12.0658 | 37.1360 |
| `rank_revealing_qr/n512/b4` | 192.1951 | 48.6726 | 148.6736 |
| `solve/n256/b1` | 1.1797 | 0.7509 | 0.3921 |
| `solve/n256/b4` | 4.6654 | 3.0012 | 1.6114 |
| `solve/n512/b1` | 8.2408 | 2.8341 | 2.0216 |
| `solve/n512/b4` | 32.7564 | 11.1891 | 8.5076 |
| `svd_thin/n256/b1` | 23.8960 | 14.6954 | 10.7262 |
| `svd_thin/n256/b4` | 97.1974 | 58.6275 | 43.1667 |
| `svd_thin/n512/b1` | 153.3460 | 55.3001 | 52.7431 |
| `svd_thin/n512/b4` | 610.9499 | 222.1294 | 212.1885 |
| `svd_values/n256/b1` | 11.1340 | 10.8131 | 5.7987 |
| `svd_values/n256/b4` | 44.7513 | 43.2874 | 24.0518 |
| `svd_values/n512/b1` | 66.5496 | 39.9196 | 25.7117 |
| `svd_values/n512/b4` | 265.5761 | 160.2286 | 109.8565 |
| `triangular_solve/n256/b1` | 0.0330 | 0.0370 | 0.0260 |
| `triangular_solve/n256/b4` | 0.1426 | 0.1435 | 0.1154 |
| `triangular_solve/n512/b1` | 0.1134 | 0.1070 | 0.1010 |
| `triangular_solve/n512/b4` | 0.5587 | 0.3844 | 0.6705 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3305 | - | 0.4430 |
| `householder_factor/4096x256/b1` | 13.9813 | - | 17.4697 |
| `qr/1024x64/b1` | 0.9796 | - | 0.9182 |
| `qr/4096x256/b1` | 40.9058 | - | 41.5472 |
| `rank_revealing_qr/1024x64/b1` | 0.9653 | - | 1.1824 |
| `rank_revealing_qr/4096x256/b1` | 64.6241 | - | 60.3437 |
| `svd_thin/1024x64/b1` | 1.4537 | - | 1.6547 |
| `svd_thin/4096x256/b1` | 72.0077 | - | 67.2407 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3281 | 0.3060 | 0.2379 |
| `householder_factor/4096x256/b1` | 14.1337 | 6.6376 | 6.6266 |
| `qr/1024x64/b1` | 0.9808 | 0.9185 | 0.5817 |
| `qr/4096x256/b1` | 41.3024 | 20.8060 | 16.1651 |
| `rank_revealing_qr/1024x64/b1` | 0.9706 | 0.7703 | 1.0171 |
| `rank_revealing_qr/4096x256/b1` | 65.6457 | 24.3502 | 42.3363 |
| `svd_thin/1024x64/b1` | 1.4562 | 1.3750 | 1.0918 |
| `svd_thin/4096x256/b1` | 72.5918 | 41.4855 | 28.7756 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3282 | 0.3527 | 0.1689 |
| `householder_factor/4096x256/b1` | 14.0798 | 5.5221 | 3.7441 |
| `qr/1024x64/b1` | 0.9792 | 1.1262 | 0.4954 |
| `qr/4096x256/b1` | 41.3454 | 18.5374 | 11.2488 |
| `rank_revealing_qr/1024x64/b1` | 0.9692 | 0.7778 | 1.0070 |
| `rank_revealing_qr/4096x256/b1` | 65.2722 | 18.7505 | 39.1589 |
| `svd_thin/1024x64/b1` | 1.4550 | 1.6660 | 0.9849 |
| `svd_thin/4096x256/b1` | 73.2535 | 30.5548 | 22.0498 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.9925 | - | 1.3264 |
| `householder_factor/4096x256/b1` | 53.5490 | - | 66.7334 |
| `qr/1024x64/b1` | 2.8449 | - | 2.8457 |
| `qr/4096x256/b1` | 146.7285 | - | 133.8571 |
| `rank_revealing_qr/1024x64/b1` | 2.8641 | - | 3.8569 |
| `rank_revealing_qr/4096x256/b1` | 244.5515 | - | 185.5013 |
| `svd_thin/1024x64/b1` | 3.5566 | - | 4.9144 |
| `svd_thin/4096x256/b1` | 231.4558 | - | 220.9679 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.9934 | 0.6464 | 0.7861 |
| `householder_factor/4096x256/b1` | 53.2061 | 20.5444 | 19.0073 |
| `qr/1024x64/b1` | 2.8437 | 1.6065 | 1.7928 |
| `qr/4096x256/b1` | 146.3858 | 58.0335 | 47.9399 |
| `rank_revealing_qr/1024x64/b1` | 2.8477 | 1.8072 | 3.1880 |
| `rank_revealing_qr/4096x256/b1` | 246.9239 | 84.1568 | 131.2358 |
| `svd_thin/1024x64/b1` | 3.5499 | 2.2948 | 3.0504 |
| `svd_thin/4096x256/b1` | 232.3005 | 104.4172 | 82.6389 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0035 | 0.6459 | 0.4852 |
| `householder_factor/4096x256/b1` | 54.4969 | 15.8635 | 11.1059 |
| `qr/1024x64/b1` | 2.8437 | 1.6814 | 1.3247 |
| `qr/4096x256/b1` | 147.0694 | 42.7620 | 29.8104 |
| `rank_revealing_qr/1024x64/b1` | 2.8459 | 1.6688 | 2.9548 |
| `rank_revealing_qr/4096x256/b1` | 246.5043 | 51.6836 | 115.4527 |
| `svd_thin/1024x64/b1` | 3.5399 | 2.3343 | 2.4184 |
| `svd_thin/4096x256/b1` | 232.5407 | 85.1143 | 51.6270 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
