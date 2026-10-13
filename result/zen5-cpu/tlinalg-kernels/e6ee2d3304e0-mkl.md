<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261013T084748Z/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `e6ee2d3304e042926c77cda7b81e58c871a98919`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.24.4 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8); `t4a-faer-traits` 0.24.0 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8)
- harness commit: `3e6ac30e0a55227312b3852f8d6050e8bbcdd317`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-13T09:46:31.157024Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor mkl`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261013T084748Z/`

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
    As measured: `t4a-faer` 0.24.4 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8); `t4a-faer-traits` 0.24.0 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.24.4 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8); `t4a-faer-traits` 0.24.0 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8)
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
| `cholesky/n16/b1024` | 0.5637 | - | 0.6359 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1067 | - | 0.0751 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2177 | - | 0.1922 |
| `eig/n16/b1` | 0.0531 | - | 0.0306 |
| `eig/n16/b1024` | 55.5489 | - | 32.1297 |
| `eig/n4/b1` | 0.0039 | - | 0.0022 |
| `eig/n4/b1024` | 3.5406 | - | 1.7832 |
| `eig/n8/b1` | 0.0141 | - | 0.0075 |
| `eig/n8/b1024` | 13.6341 | - | 7.0730 |
| `eigh/n16/b1` | 0.0176 | - | 0.0135 |
| `eigh/n16/b1024` | 17.7600 | - | 14.1369 |
| `eigh/n4/b1` | 0.0017 | - | 0.0019 |
| `eigh/n4/b1024` | 1.4546 | - | 1.7006 |
| `eigh/n8/b1` | 0.0051 | - | 0.0047 |
| `eigh/n8/b1024` | 5.0413 | - | 4.6506 |
| `eigvals/n16/b1` | 0.0372 | - | 0.0212 |
| `eigvals/n16/b1024` | 38.9311 | - | 21.9802 |
| `eigvals/n4/b1` | 0.0023 | - | 0.0018 |
| `eigvals/n4/b1024` | 1.8806 | - | 1.2750 |
| `eigvals/n8/b1` | 0.0098 | - | 0.0059 |
| `eigvals/n8/b1024` | 9.1736 | - | 5.3607 |
| `eigvalsh/n16/b1` | 0.0133 | - | 0.0076 |
| `eigvalsh/n16/b1024` | 13.3248 | - | 7.8195 |
| `eigvalsh/n4/b1` | 0.0014 | - | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1866 | - | 0.9005 |
| `eigvalsh/n8/b1` | 0.0043 | - | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0268 | - | 2.6860 |
| `full_piv_lu/n16/b1` | 0.0025 | - | 0.0023 |
| `full_piv_lu/n16/b1024` | 1.9904 | - | 2.3692 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2290 | - | 0.2453 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6134 | - | 0.5608 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | - | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0430 | - | 3.4755 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | - | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3118 | - | 0.6686 |
| `full_piv_lu_solve/n8/b1` | 0.0013 | - | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7532 | - | 1.1604 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0018 |
| `householder_apply/n16/b1024` | 2.7746 | - | 1.6179 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.2128 | - | 0.2006 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0008 |
| `householder_apply/n8/b1024` | 0.7077 | - | 0.4800 |
| `householder_factor/n16/b1` | 0.0022 | - | 0.0018 |
| `householder_factor/n16/b1024` | 2.1846 | - | 1.7725 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0003 |
| `householder_factor/n4/b1024` | 0.2664 | - | 0.1829 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0006 |
| `householder_factor/n8/b1024` | 0.7249 | - | 0.5059 |
| `lu/n16/b1` | 0.0021 | - | 0.0011 |
| `lu/n16/b1024` | 1.7607 | - | 1.0281 |
| `lu/n4/b1` | 0.0004 | - | 0.0003 |
| `lu/n4/b1024` | 0.1744 | - | 0.1028 |
| `lu/n8/b1` | 0.0008 | - | 0.0005 |
| `lu/n8/b1024` | 0.5126 | - | 0.2933 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0007 |
| `lu_factor/n16/b1024` | 1.0592 | - | 0.7240 |
| `lu_factor/n4/b1` | 0.0003 | - | 0.0001 |
| `lu_factor/n4/b1024` | 0.1329 | - | 0.0374 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0002 |
| `lu_factor/n8/b1024` | 0.3385 | - | 0.1584 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4369 | - | 1.3722 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1671 | - | 0.1070 |
| `lu_factor_solve/n8/b1` | 0.0008 | - | 0.0006 |
| `lu_factor_solve/n8/b1024` | 0.4678 | - | 0.4948 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3560 | - | 0.6279 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0409 | - | 0.0787 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1376 | - | 0.3548 |
| `qr/n16/b1` | 0.0055 | - | 0.0034 |
| `qr/n16/b1024` | 5.3553 | - | 3.2106 |
| `qr/n4/b1` | 0.0008 | - | 0.0007 |
| `qr/n4/b1024` | 0.4484 | - | 0.4367 |
| `qr/n8/b1` | 0.0017 | - | 0.0013 |
| `qr/n8/b1024` | 1.4489 | - | 1.0301 |
| `rank_revealing_qr/n16/b1` | 0.0065 | - | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.2248 | - | 5.0012 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7154 | - | 0.7384 |
| `rank_revealing_qr/n8/b1` | 0.0022 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.9269 | - | 1.7819 |
| `solve/n16/b1` | 0.0022 | - | 0.0018 |
| `solve/n16/b1024` | 1.6094 | - | 1.4496 |
| `solve/n4/b1` | 0.0006 | - | 0.0003 |
| `solve/n4/b1024` | 0.2173 | - | 0.1408 |
| `solve/n8/b1` | 0.0010 | - | 0.0007 |
| `solve/n8/b1024` | 0.5538 | - | 0.5318 |
| `svd_full/n16/b1` | 0.0326 | - | 0.0306 |
| `svd_full/n16/b1024` | 33.4353 | - | 31.1033 |
| `svd_full/n4/b1` | 0.0029 | - | 0.0039 |
| `svd_full/n4/b1024` | 2.5342 | - | 3.7168 |
| `svd_full/n8/b1` | 0.0090 | - | 0.0107 |
| `svd_full/n8/b1024` | 9.0816 | - | 11.2194 |
| `svd_thin/n16/b1` | 0.0329 | - | 0.0305 |
| `svd_thin/n16/b1024` | 33.4409 | - | 31.0722 |
| `svd_thin/n4/b1` | 0.0028 | - | 0.0039 |
| `svd_thin/n4/b1024` | 2.5159 | - | 3.7026 |
| `svd_thin/n8/b1` | 0.0090 | - | 0.0107 |
| `svd_thin/n8/b1024` | 9.0117 | - | 11.2124 |
| `svd_values/n16/b1` | 0.0238 | - | 0.0112 |
| `svd_values/n16/b1024` | 24.4964 | - | 11.6394 |
| `svd_values/n4/b1` | 0.0021 | - | 0.0018 |
| `svd_values/n4/b1024` | 1.9101 | - | 1.6069 |
| `svd_values/n8/b1` | 0.0068 | - | 0.0041 |
| `svd_values/n8/b1024` | 6.7443 | - | 4.0447 |
| `triangular_solve/n16/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3039 | - | 0.3420 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0511 | - | 0.1725 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1313 | - | 0.2257 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0023 | 0.0007 |
| `cholesky/n16/b1024` | 0.5423 | 0.2772 | 0.6342 |
| `cholesky/n4/b1` | 0.0002 | 0.0021 | 0.0002 |
| `cholesky/n4/b1024` | 0.1060 | 0.0573 | 0.0720 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0003 |
| `cholesky/n8/b1024` | 0.2144 | 0.0595 | 0.1869 |
| `eig/n16/b1` | 0.0531 | 0.0564 | 0.0307 |
| `eig/n16/b1024` | 55.6565 | 18.2493 | 31.9579 |
| `eig/n4/b1` | 0.0039 | 0.0066 | 0.0021 |
| `eig/n4/b1024` | 3.5642 | 1.8115 | 1.7723 |
| `eig/n8/b1` | 0.0141 | 0.0171 | 0.0075 |
| `eig/n8/b1024` | 13.6946 | 6.3620 | 7.1083 |
| `eigh/n16/b1` | 0.0176 | 0.0204 | 0.0134 |
| `eigh/n16/b1024` | 17.6341 | 7.8499 | 14.1199 |
| `eigh/n4/b1` | 0.0018 | 0.0040 | 0.0018 |
| `eigh/n4/b1024` | 1.4525 | 0.7335 | 1.6748 |
| `eigh/n8/b1` | 0.0052 | 0.0083 | 0.0047 |
| `eigh/n8/b1024` | 5.0163 | 2.5482 | 4.6142 |
| `eigvals/n16/b1` | 0.0378 | 0.0402 | 0.0211 |
| `eigvals/n16/b1024` | 38.7504 | 13.3861 | 22.0129 |
| `eigvals/n4/b1` | 0.0023 | 0.0038 | 0.0017 |
| `eigvals/n4/b1024` | 1.8775 | 0.6410 | 1.2697 |
| `eigvals/n8/b1` | 0.0097 | 0.0123 | 0.0060 |
| `eigvals/n8/b1024` | 9.0793 | 2.3363 | 5.3419 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0161 | 0.0076 |
| `eigvalsh/n16/b1024` | 13.2504 | 6.2494 | 7.7888 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0036 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1882 | 0.4289 | 0.8815 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0066 | 0.0028 |
| `eigvalsh/n8/b1024` | 4.0344 | 2.0465 | 2.6521 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0047 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.0084 | 1.0029 | 2.3877 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0028 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2270 | 0.0683 | 0.2431 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0036 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6062 | 0.3063 | 0.5688 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0048 | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0161 | 0.5214 | 3.5049 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0024 | 0.0010 |
| `full_piv_lu_solve/n4/b1024` | 0.3125 | 0.1627 | 0.6591 |
| `full_piv_lu_solve/n8/b1` | 0.0013 | 0.0036 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7268 | 0.1941 | 1.1587 |
| `householder_apply/n16/b1` | 0.0028 | 0.0050 | 0.0018 |
| `householder_apply/n16/b1024` | 2.6796 | 0.6876 | 1.6089 |
| `householder_apply/n4/b1` | 0.0004 | 0.0021 | 0.0004 |
| `householder_apply/n4/b1024` | 0.2067 | 0.1091 | 0.2031 |
| `householder_apply/n8/b1` | 0.0008 | 0.0032 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6874 | 0.1772 | 0.4698 |
| `householder_factor/n16/b1` | 0.0021 | 0.0045 | 0.0018 |
| `householder_factor/n16/b1024` | 2.1647 | 0.5519 | 1.7772 |
| `householder_factor/n4/b1` | 0.0004 | 0.0020 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2646 | 0.0726 | 0.1833 |
| `householder_factor/n8/b1` | 0.0008 | 0.0033 | 0.0006 |
| `householder_factor/n8/b1024` | 0.7084 | 0.1932 | 0.5044 |
| `lu/n16/b1` | 0.0020 | 0.0038 | 0.0012 |
| `lu/n16/b1024` | 1.6674 | 0.8097 | 0.9989 |
| `lu/n4/b1` | 0.0004 | 0.0027 | 0.0003 |
| `lu/n4/b1024` | 0.1800 | 0.0944 | 0.1025 |
| `lu/n8/b1` | 0.0008 | 0.0025 | 0.0005 |
| `lu/n8/b1024` | 0.5103 | 0.2651 | 0.2872 |
| `lu_factor/n16/b1` | 0.0013 | 0.0037 | 0.0008 |
| `lu_factor/n16/b1024` | 1.0806 | 0.2883 | 0.7212 |
| `lu_factor/n4/b1` | 0.0004 | 0.0021 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1336 | 0.0429 | 0.0374 |
| `lu_factor/n8/b1` | 0.0006 | 0.0022 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3439 | 0.0936 | 0.1579 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0043 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4225 | 0.3641 | 1.3775 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1645 | 0.0513 | 0.1068 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0025 | 0.0006 |
| `lu_factor_solve/n8/b1024` | 0.4730 | 0.2453 | 0.4951 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0022 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3550 | 0.1022 | 0.6429 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0405 | 0.0205 | 0.0784 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0028 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1376 | 0.0456 | 0.3514 |
| `qr/n16/b1` | 0.0055 | 0.0084 | 0.0034 |
| `qr/n16/b1024` | 5.4379 | 1.9616 | 3.1970 |
| `qr/n4/b1` | 0.0008 | 0.0028 | 0.0007 |
| `qr/n4/b1024` | 0.4452 | 0.2253 | 0.4398 |
| `qr/n8/b1` | 0.0016 | 0.0040 | 0.0013 |
| `qr/n8/b1024` | 1.4060 | 0.7080 | 1.0160 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0094 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.1663 | 2.8147 | 4.9780 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0037 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7117 | 0.3565 | 0.7314 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0046 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.9439 | 0.9809 | 1.7685 |
| `solve/n16/b1` | 0.0022 | 0.0038 | 0.0018 |
| `solve/n16/b1024` | 1.5708 | 0.4080 | 1.4838 |
| `solve/n4/b1` | 0.0006 | 0.0028 | 0.0003 |
| `solve/n4/b1024` | 0.2174 | 0.0605 | 0.1386 |
| `solve/n8/b1` | 0.0010 | 0.0036 | 0.0007 |
| `solve/n8/b1024` | 0.5521 | 0.2802 | 0.5342 |
| `svd_full/n16/b1` | 0.0330 | 0.0354 | 0.0305 |
| `svd_full/n16/b1024` | 33.4786 | 8.9334 | 31.0045 |
| `svd_full/n4/b1` | 0.0029 | 0.0051 | 0.0039 |
| `svd_full/n4/b1024` | 2.5209 | 1.2853 | 3.6817 |
| `svd_full/n8/b1` | 0.0091 | 0.0114 | 0.0107 |
| `svd_full/n8/b1024` | 9.0554 | 4.5264 | 11.1129 |
| `svd_thin/n16/b1` | 0.0326 | 0.0353 | 0.0305 |
| `svd_thin/n16/b1024` | 33.7477 | 8.5503 | 31.0175 |
| `svd_thin/n4/b1` | 0.0027 | 0.0052 | 0.0039 |
| `svd_thin/n4/b1024` | 2.4990 | 1.2644 | 3.6447 |
| `svd_thin/n8/b1` | 0.0091 | 0.0120 | 0.0107 |
| `svd_thin/n8/b1024` | 9.2989 | 2.8039 | 11.1066 |
| `svd_values/n16/b1` | 0.0240 | 0.0267 | 0.0112 |
| `svd_values/n16/b1024` | 24.4838 | 6.1949 | 11.6193 |
| `svd_values/n4/b1` | 0.0021 | 0.0044 | 0.0018 |
| `svd_values/n4/b1024` | 1.9136 | 0.9628 | 1.5926 |
| `svd_values/n8/b1` | 0.0069 | 0.0094 | 0.0041 |
| `svd_values/n8/b1024` | 6.7679 | 3.0253 | 4.0270 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0028 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.2991 | 0.0799 | 0.3517 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0022 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0511 | 0.0290 | 0.1756 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0023 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1315 | 0.0696 | 0.2384 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0024 | 0.0007 |
| `cholesky/n16/b1024` | 0.5343 | 0.0729 | 0.6257 |
| `cholesky/n4/b1` | 0.0002 | 0.0022 | 0.0002 |
| `cholesky/n4/b1024` | 0.1068 | 0.0215 | 0.0709 |
| `cholesky/n8/b1` | 0.0004 | 0.0026 | 0.0003 |
| `cholesky/n8/b1024` | 0.2187 | 0.0593 | 0.1919 |
| `eig/n16/b1` | 0.0530 | 0.0561 | 0.0306 |
| `eig/n16/b1024` | 55.7811 | 7.0447 | 31.8988 |
| `eig/n4/b1` | 0.0040 | 0.0069 | 0.0022 |
| `eig/n4/b1024` | 3.5694 | 0.8975 | 1.7703 |
| `eig/n8/b1` | 0.0142 | 0.0170 | 0.0074 |
| `eig/n8/b1024` | 13.7022 | 2.4640 | 7.0413 |
| `eigh/n16/b1` | 0.0175 | 0.0206 | 0.0134 |
| `eigh/n16/b1024` | 17.6804 | 2.2343 | 14.1103 |
| `eigh/n4/b1` | 0.0016 | 0.0050 | 0.0018 |
| `eigh/n4/b1024` | 1.4521 | 0.3721 | 1.7012 |
| `eigh/n8/b1` | 0.0051 | 0.0083 | 0.0047 |
| `eigh/n8/b1024` | 4.9999 | 0.6702 | 4.6323 |
| `eigvals/n16/b1` | 0.0373 | 0.0400 | 0.0211 |
| `eigvals/n16/b1024` | 38.7687 | 5.3510 | 21.9245 |
| `eigvals/n4/b1` | 0.0023 | 0.0055 | 0.0017 |
| `eigvals/n4/b1024` | 1.8853 | 0.2678 | 1.2674 |
| `eigvals/n8/b1` | 0.0097 | 0.0125 | 0.0059 |
| `eigvals/n8/b1024` | 9.1239 | 1.7181 | 5.3524 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0164 | 0.0076 |
| `eigvalsh/n16/b1024` | 13.2966 | 1.7310 | 7.8243 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0045 | 0.0011 |
| `eigvalsh/n4/b1024` | 1.1959 | 0.3036 | 0.8792 |
| `eigvalsh/n8/b1` | 0.0044 | 0.0121 | 0.0028 |
| `eigvalsh/n8/b1024` | 4.0396 | 0.5244 | 2.6403 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0057 | 0.0023 |
| `full_piv_lu/n16/b1024` | 1.9336 | 0.5017 | 2.3397 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0031 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2270 | 0.0636 | 0.2546 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0035 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6087 | 0.0816 | 0.5778 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0054 | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0186 | 0.2914 | 3.4648 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0044 | 0.0010 |
| `full_piv_lu_solve/n4/b1024` | 0.3142 | 0.0447 | 0.6857 |
| `full_piv_lu_solve/n8/b1` | 0.0013 | 0.0054 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7289 | 0.0999 | 1.1595 |
| `householder_apply/n16/b1` | 0.0027 | 0.0061 | 0.0018 |
| `householder_apply/n16/b1024` | 2.8478 | 0.3615 | 1.6037 |
| `householder_apply/n4/b1` | 0.0004 | 0.0021 | 0.0004 |
| `householder_apply/n4/b1024` | 0.2051 | 0.0552 | 0.1939 |
| `householder_apply/n8/b1` | 0.0008 | 0.0034 | 0.0007 |
| `householder_apply/n8/b1024` | 0.7034 | 0.1807 | 0.4698 |
| `householder_factor/n16/b1` | 0.0022 | 0.0053 | 0.0018 |
| `householder_factor/n16/b1024` | 2.1548 | 0.5511 | 1.7719 |
| `householder_factor/n4/b1` | 0.0004 | 0.0030 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2718 | 0.0723 | 0.1832 |
| `householder_factor/n8/b1` | 0.0008 | 0.0028 | 0.0006 |
| `householder_factor/n8/b1024` | 0.7086 | 0.1842 | 0.5045 |
| `lu/n16/b1` | 0.0020 | 0.0050 | 0.0011 |
| `lu/n16/b1024` | 1.7396 | 0.4240 | 1.0238 |
| `lu/n4/b1` | 0.0004 | 0.0039 | 0.0003 |
| `lu/n4/b1024` | 0.1736 | 0.0308 | 0.1032 |
| `lu/n8/b1` | 0.0008 | 0.0039 | 0.0005 |
| `lu/n8/b1024` | 0.4964 | 0.0980 | 0.2878 |
| `lu_factor/n16/b1` | 0.0013 | 0.0041 | 0.0008 |
| `lu_factor/n16/b1024` | 1.1114 | 0.2845 | 0.6982 |
| `lu_factor/n4/b1` | 0.0003 | 0.0037 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1339 | 0.0388 | 0.0387 |
| `lu_factor/n8/b1` | 0.0006 | 0.0042 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3522 | 0.0945 | 0.1581 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0054 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4534 | 0.3727 | 1.4278 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0040 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1623 | 0.0481 | 0.1087 |
| `lu_factor_solve/n8/b1` | 0.0008 | 0.0041 | 0.0006 |
| `lu_factor_solve/n8/b1024` | 0.4737 | 0.1290 | 0.4990 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0035 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3545 | 0.1051 | 0.6332 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0022 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0402 | 0.0229 | 0.0783 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0025 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1370 | 0.0452 | 0.3521 |
| `qr/n16/b1` | 0.0055 | 0.0081 | 0.0033 |
| `qr/n16/b1024` | 5.3219 | 1.0904 | 3.1734 |
| `qr/n4/b1` | 0.0008 | 0.0032 | 0.0007 |
| `qr/n4/b1024` | 0.4509 | 0.0608 | 0.4441 |
| `qr/n8/b1` | 0.0016 | 0.0054 | 0.0013 |
| `qr/n8/b1024` | 1.4265 | 0.3502 | 1.0183 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0097 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.1141 | 0.8085 | 4.9877 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0042 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7052 | 0.0941 | 0.7402 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0054 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8898 | 0.4823 | 1.7603 |
| `solve/n16/b1` | 0.0022 | 0.0053 | 0.0018 |
| `solve/n16/b1024` | 1.6052 | 0.2111 | 1.5001 |
| `solve/n4/b1` | 0.0006 | 0.0032 | 0.0003 |
| `solve/n4/b1024` | 0.2167 | 0.0604 | 0.1393 |
| `solve/n8/b1` | 0.0010 | 0.0038 | 0.0007 |
| `solve/n8/b1024` | 0.5472 | 0.0813 | 0.5330 |
| `svd_full/n16/b1` | 0.0327 | 0.0359 | 0.0306 |
| `svd_full/n16/b1024` | 33.2598 | 4.3295 | 30.9111 |
| `svd_full/n4/b1` | 0.0028 | 0.0057 | 0.0039 |
| `svd_full/n4/b1024` | 2.5112 | 0.3615 | 3.6593 |
| `svd_full/n8/b1` | 0.0091 | 0.0254 | 0.0107 |
| `svd_full/n8/b1024` | 8.9889 | 1.8363 | 11.1162 |
| `svd_thin/n16/b1` | 0.0325 | 0.0355 | 0.0305 |
| `svd_thin/n16/b1024` | 33.4404 | 7.8333 | 30.8374 |
| `svd_thin/n4/b1` | 0.0028 | 0.0060 | 0.0039 |
| `svd_thin/n4/b1024` | 2.5280 | 0.3521 | 3.6607 |
| `svd_thin/n8/b1` | 0.0089 | 0.0116 | 0.0106 |
| `svd_thin/n8/b1024` | 9.0642 | 1.5162 | 11.1062 |
| `svd_values/n16/b1` | 0.0238 | 0.0267 | 0.0112 |
| `svd_values/n16/b1024` | 24.4961 | 5.9724 | 11.6007 |
| `svd_values/n4/b1` | 0.0021 | 0.0054 | 0.0018 |
| `svd_values/n4/b1024` | 1.9086 | 0.2656 | 1.5903 |
| `svd_values/n8/b1` | 0.0068 | 0.0098 | 0.0041 |
| `svd_values/n8/b1024` | 6.7715 | 1.2409 | 4.0486 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0029 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.2995 | 0.0493 | 0.3672 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0023 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0511 | 0.0134 | 0.1758 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0031 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1302 | 0.0366 | 0.2372 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0011 |
| `cholesky/n16/b1024` | 0.7999 | - | 1.0952 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1174 | - | 0.1066 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2616 | - | 0.2896 |
| `eig/n16/b1` | 0.0721 | - | 0.0991 |
| `eig/n16/b1024` | 76.1373 | - | 107.0240 |
| `eig/n4/b1` | 0.0059 | - | 0.0077 |
| `eig/n4/b1024` | 5.8003 | - | 7.4596 |
| `eig/n8/b1` | 0.0199 | - | 0.0250 |
| `eig/n8/b1024` | 20.5064 | - | 26.0798 |
| `eigh/n16/b1` | 0.0179 | - | 0.0184 |
| `eigh/n16/b1024` | 19.2557 | - | 19.4221 |
| `eigh/n4/b1` | 0.0019 | - | 0.0018 |
| `eigh/n4/b1024` | 1.7713 | - | 1.7018 |
| `eigh/n8/b1` | 0.0057 | - | 0.0053 |
| `eigh/n8/b1024` | 5.4904 | - | 5.3790 |
| `eigvals/n16/b1` | 0.0435 | - | 0.0684 |
| `eigvals/n16/b1024` | 46.5503 | - | 75.2668 |
| `eigvals/n4/b1` | 0.0030 | - | 0.0061 |
| `eigvals/n4/b1024` | 2.8451 | - | 5.7699 |
| `eigvals/n8/b1` | 0.0117 | - | 0.0196 |
| `eigvals/n8/b1024` | 11.9879 | - | 20.6632 |
| `eigvalsh/n16/b1` | 0.0135 | - | 0.0107 |
| `eigvalsh/n16/b1024` | 14.1333 | - | 11.0220 |
| `eigvalsh/n4/b1` | 0.0016 | - | 0.0013 |
| `eigvalsh/n4/b1024` | 1.4324 | - | 1.0536 |
| `eigvalsh/n8/b1` | 0.0046 | - | 0.0035 |
| `eigvalsh/n8/b1024` | 4.3829 | - | 3.3363 |
| `full_piv_lu/n16/b1` | 0.0030 | - | 0.0029 |
| `full_piv_lu/n16/b1024` | 2.8314 | - | 3.5831 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2712 | - | 0.3401 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0011 |
| `full_piv_lu/n8/b1024` | 0.7177 | - | 0.7933 |
| `full_piv_lu_solve/n16/b1` | 0.0038 | - | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1320 | - | 5.1633 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4507 | - | 1.0028 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1078 | - | 1.9627 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0035 |
| `householder_apply/n16/b1024` | 3.6001 | - | 4.1891 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.2008 | - | 0.2524 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0010 |
| `householder_apply/n8/b1024` | 0.6725 | - | 0.7951 |
| `householder_factor/n16/b1` | 0.0027 | - | 0.0038 |
| `householder_factor/n16/b1024` | 2.6736 | - | 3.7827 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.3239 | - | 0.3076 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.8581 | - | 0.8927 |
| `lu/n16/b1` | 0.0022 | - | 0.0022 |
| `lu/n16/b1024` | 1.9169 | - | 2.2299 |
| `lu/n4/b1` | 0.0005 | - | 0.0004 |
| `lu/n4/b1024` | 0.2152 | - | 0.1710 |
| `lu/n8/b1` | 0.0008 | - | 0.0007 |
| `lu/n8/b1024` | 0.5420 | - | 0.5342 |
| `lu_factor/n16/b1` | 0.0014 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.1966 | - | 1.5877 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0001 |
| `lu_factor/n4/b1024` | 0.1656 | - | 0.1105 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3901 | - | 0.3711 |
| `lu_factor_solve/n16/b1` | 0.0023 | - | 0.0032 |
| `lu_factor_solve/n16/b1024` | 1.9840 | - | 3.1961 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2515 | - | 0.2499 |
| `lu_factor_solve/n8/b1` | 0.0009 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6695 | - | 1.0006 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7793 | - | 1.6255 |
| `lu_solve_prepared/n4/b1` | 0.0003 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0978 | - | 0.1445 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2866 | - | 0.6415 |
| `qr/n16/b1` | 0.0067 | - | 0.0063 |
| `qr/n16/b1024` | 6.5694 | - | 6.3675 |
| `qr/n4/b1` | 0.0007 | - | 0.0009 |
| `qr/n4/b1024` | 0.5014 | - | 0.5865 |
| `qr/n8/b1` | 0.0018 | - | 0.0019 |
| `qr/n8/b1024` | 1.5415 | - | 1.5820 |
| `rank_revealing_qr/n16/b1` | 0.0075 | - | 0.0094 |
| `rank_revealing_qr/n16/b1024` | 7.2917 | - | 9.6383 |
| `rank_revealing_qr/n4/b1` | 0.0012 | - | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8226 | - | 1.0875 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1640 | - | 2.8705 |
| `solve/n16/b1` | 0.0029 | - | 0.0036 |
| `solve/n16/b1024` | 2.2874 | - | 3.3656 |
| `solve/n4/b1` | 0.0007 | - | 0.0005 |
| `solve/n4/b1024` | 0.3142 | - | 0.2897 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7741 | - | 1.0518 |
| `svd_full/n16/b1` | 0.0349 | - | 0.0394 |
| `svd_full/n16/b1024` | 36.7950 | - | 40.8750 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0047 |
| `svd_full/n4/b1024` | 3.0762 | - | 4.4939 |
| `svd_full/n8/b1` | 0.0098 | - | 0.0126 |
| `svd_full/n8/b1024` | 10.2332 | - | 13.3314 |
| `svd_thin/n16/b1` | 0.0350 | - | 0.0394 |
| `svd_thin/n16/b1024` | 36.8383 | - | 40.9273 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0047 |
| `svd_thin/n4/b1024` | 3.0673 | - | 4.4749 |
| `svd_thin/n8/b1` | 0.0098 | - | 0.0127 |
| `svd_thin/n8/b1024` | 10.2191 | - | 13.3539 |
| `svd_values/n16/b1` | 0.0261 | - | 0.0164 |
| `svd_values/n16/b1024` | 27.2893 | - | 16.9291 |
| `svd_values/n4/b1` | 0.0025 | - | 0.0023 |
| `svd_values/n4/b1024` | 2.3222 | - | 2.1072 |
| `svd_values/n8/b1` | 0.0077 | - | 0.0054 |
| `svd_values/n8/b1024` | 7.7868 | - | 5.4784 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5944 | - | 0.8586 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0963 | - | 0.1782 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2371 | - | 0.3427 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0036 | 0.0011 |
| `cholesky/n16/b1024` | 0.8200 | 0.4049 | 1.0714 |
| `cholesky/n4/b1` | 0.0002 | 0.0022 | 0.0002 |
| `cholesky/n4/b1024` | 0.1173 | 0.0357 | 0.1064 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2593 | 0.1351 | 0.2834 |
| `eig/n16/b1` | 0.0715 | 0.0769 | 0.0948 |
| `eig/n16/b1024` | 76.1910 | 19.2518 | 101.8563 |
| `eig/n4/b1` | 0.0060 | 0.0092 | 0.0077 |
| `eig/n4/b1024` | 5.8137 | 1.5416 | 7.4597 |
| `eig/n8/b1` | 0.0199 | 0.0230 | 0.0249 |
| `eig/n8/b1024` | 20.5343 | 5.5352 | 25.9581 |
| `eigh/n16/b1` | 0.0179 | 0.0209 | 0.0185 |
| `eigh/n16/b1024` | 19.3003 | 4.8789 | 19.4142 |
| `eigh/n4/b1` | 0.0019 | 0.0037 | 0.0018 |
| `eigh/n4/b1024` | 1.7505 | 0.8844 | 1.7003 |
| `eigh/n8/b1` | 0.0057 | 0.0088 | 0.0053 |
| `eigh/n8/b1024` | 5.4572 | 2.7644 | 5.3436 |
| `eigvals/n16/b1` | 0.0433 | 0.0467 | 0.0681 |
| `eigvals/n16/b1024` | 46.3465 | 17.6749 | 74.9843 |
| `eigvals/n4/b1` | 0.0030 | 0.0049 | 0.0060 |
| `eigvals/n4/b1024` | 2.8971 | 1.1541 | 5.7481 |
| `eigvals/n8/b1` | 0.0116 | 0.0146 | 0.0196 |
| `eigvals/n8/b1024` | 11.8538 | 3.6766 | 20.5976 |
| `eigvalsh/n16/b1` | 0.0135 | 0.0166 | 0.0107 |
| `eigvalsh/n16/b1024` | 14.2417 | 3.9293 | 11.0399 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0039 | 0.0013 |
| `eigvalsh/n4/b1024` | 1.4386 | 0.3621 | 1.0535 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0075 | 0.0035 |
| `eigvalsh/n8/b1024` | 4.3914 | 2.2113 | 3.3044 |
| `full_piv_lu/n16/b1` | 0.0030 | 0.0052 | 0.0029 |
| `full_piv_lu/n16/b1024` | 2.8355 | 1.3466 | 3.5231 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2888 | 0.1497 | 0.3307 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0034 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7645 | 0.3805 | 0.7729 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0058 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1116 | 1.5962 | 5.1244 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0038 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4530 | 0.2318 | 0.9862 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0041 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1205 | 0.2984 | 1.9583 |
| `householder_apply/n16/b1` | 0.0027 | 0.0049 | 0.0035 |
| `householder_apply/n16/b1024` | 3.3516 | 1.3583 | 3.9946 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0005 |
| `householder_apply/n4/b1024` | 0.2018 | 0.0557 | 0.2473 |
| `householder_apply/n8/b1` | 0.0008 | 0.0035 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6803 | 0.3310 | 0.7568 |
| `householder_factor/n16/b1` | 0.0027 | 0.0048 | 0.0037 |
| `householder_factor/n16/b1024` | 2.6618 | 0.6851 | 3.8158 |
| `householder_factor/n4/b1` | 0.0004 | 0.0025 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3216 | 0.0858 | 0.3079 |
| `householder_factor/n8/b1` | 0.0009 | 0.0034 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8560 | 0.4328 | 0.8931 |
| `lu/n16/b1` | 0.0022 | 0.0049 | 0.0022 |
| `lu/n16/b1024` | 1.9697 | 0.9345 | 2.2034 |
| `lu/n4/b1` | 0.0004 | 0.0021 | 0.0004 |
| `lu/n4/b1024` | 0.2140 | 0.0563 | 0.1707 |
| `lu/n8/b1` | 0.0008 | 0.0036 | 0.0007 |
| `lu/n8/b1024` | 0.5602 | 0.1431 | 0.5412 |
| `lu_factor/n16/b1` | 0.0014 | 0.0030 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2379 | 0.6324 | 1.5851 |
| `lu_factor/n4/b1` | 0.0004 | 0.0021 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1629 | 0.0471 | 0.1101 |
| `lu_factor/n8/b1` | 0.0006 | 0.0023 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3942 | 0.2062 | 0.3690 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0054 | 0.0032 |
| `lu_factor_solve/n16/b1024` | 1.9899 | 1.0221 | 3.2065 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0028 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2518 | 0.0711 | 0.2494 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0034 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6690 | 0.3459 | 0.9957 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0036 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7850 | 0.3948 | 1.5728 |
| `lu_solve_prepared/n4/b1` | 0.0003 | 0.0028 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0980 | 0.0345 | 0.1447 |
| `lu_solve_prepared/n8/b1` | 0.0005 | 0.0031 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2853 | 0.0832 | 0.6409 |
| `qr/n16/b1` | 0.0067 | 0.0095 | 0.0064 |
| `qr/n16/b1024` | 6.5452 | 1.6787 | 6.4612 |
| `qr/n4/b1` | 0.0007 | 0.0036 | 0.0009 |
| `qr/n4/b1024` | 0.4985 | 0.2580 | 0.5801 |
| `qr/n8/b1` | 0.0018 | 0.0040 | 0.0019 |
| `qr/n8/b1024` | 1.5391 | 0.3934 | 1.5768 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0103 | 0.0093 |
| `rank_revealing_qr/n16/b1024` | 7.2713 | 3.6698 | 9.5917 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0038 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8276 | 0.4216 | 1.0825 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0054 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1574 | 1.1122 | 2.8660 |
| `solve/n16/b1` | 0.0028 | 0.0052 | 0.0036 |
| `solve/n16/b1024` | 2.2691 | 0.5792 | 3.3455 |
| `solve/n4/b1` | 0.0007 | 0.0029 | 0.0005 |
| `solve/n4/b1024` | 0.3127 | 0.1617 | 0.2887 |
| `solve/n8/b1` | 0.0012 | 0.0035 | 0.0013 |
| `solve/n8/b1024` | 0.7588 | 0.1987 | 1.0504 |
| `svd_full/n16/b1` | 0.0348 | 0.0378 | 0.0391 |
| `svd_full/n16/b1024` | 36.5031 | 9.9783 | 40.8563 |
| `svd_full/n4/b1` | 0.0031 | 0.0059 | 0.0047 |
| `svd_full/n4/b1024` | 3.0618 | 1.5571 | 4.4252 |
| `svd_full/n8/b1` | 0.0097 | 0.0125 | 0.0126 |
| `svd_full/n8/b1024` | 10.2195 | 2.5573 | 13.3027 |
| `svd_thin/n16/b1` | 0.0348 | 0.0377 | 0.0391 |
| `svd_thin/n16/b1024` | 36.4802 | 14.8302 | 40.5997 |
| `svd_thin/n4/b1` | 0.0031 | 0.0056 | 0.0046 |
| `svd_thin/n4/b1024` | 3.0562 | 1.2911 | 4.4217 |
| `svd_thin/n8/b1` | 0.0097 | 0.0127 | 0.0125 |
| `svd_thin/n8/b1024` | 10.1978 | 2.5818 | 13.3415 |
| `svd_values/n16/b1` | 0.0262 | 0.0293 | 0.0163 |
| `svd_values/n16/b1024` | 27.4463 | 9.8469 | 16.8920 |
| `svd_values/n4/b1` | 0.0025 | 0.0048 | 0.0023 |
| `svd_values/n4/b1024` | 2.3154 | 1.1671 | 2.1081 |
| `svd_values/n8/b1` | 0.0076 | 0.0099 | 0.0054 |
| `svd_values/n8/b1024` | 7.7920 | 1.9733 | 5.4629 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0024 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5941 | 0.2990 | 0.8440 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0022 | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0957 | 0.0297 | 0.1806 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0027 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2380 | 0.0648 | 0.3459 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0042 | 0.0011 |
| `cholesky/n16/b1024` | 0.8083 | 0.2014 | 1.1150 |
| `cholesky/n4/b1` | 0.0003 | 0.0038 | 0.0002 |
| `cholesky/n4/b1024` | 0.1164 | 0.0337 | 0.1061 |
| `cholesky/n8/b1` | 0.0004 | 0.0032 | 0.0004 |
| `cholesky/n8/b1024` | 0.2600 | 0.0463 | 0.2839 |
| `eig/n16/b1` | 0.0723 | 0.0765 | 0.0979 |
| `eig/n16/b1024` | 76.0824 | 10.2762 | 106.0370 |
| `eig/n4/b1` | 0.0061 | 0.0093 | 0.0077 |
| `eig/n4/b1024` | 5.7850 | 1.4696 | 7.4610 |
| `eig/n8/b1` | 0.0199 | 0.0231 | 0.0249 |
| `eig/n8/b1024` | 20.3315 | 2.6456 | 25.9224 |
| `eigh/n16/b1` | 0.0179 | 0.0210 | 0.0185 |
| `eigh/n16/b1024` | 19.1659 | 3.0304 | 19.3603 |
| `eigh/n4/b1` | 0.0020 | 0.0052 | 0.0018 |
| `eigh/n4/b1024` | 1.7602 | 0.4467 | 1.6998 |
| `eigh/n8/b1` | 0.0057 | 0.0090 | 0.0053 |
| `eigh/n8/b1024` | 5.4512 | 0.7018 | 5.3458 |
| `eigvals/n16/b1` | 0.0436 | 0.0465 | 0.0681 |
| `eigvals/n16/b1024` | 46.4503 | 8.6523 | 74.9163 |
| `eigvals/n4/b1` | 0.0031 | 0.0062 | 0.0061 |
| `eigvals/n4/b1024` | 2.8453 | 0.3697 | 5.7472 |
| `eigvals/n8/b1` | 0.0117 | 0.0147 | 0.0195 |
| `eigvals/n8/b1024` | 11.8858 | 2.1888 | 20.6336 |
| `eigvalsh/n16/b1` | 0.0137 | 0.0165 | 0.0107 |
| `eigvalsh/n16/b1024` | 14.2454 | 1.8117 | 10.9952 |
| `eigvalsh/n4/b1` | 0.0017 | 0.0049 | 0.0013 |
| `eigvalsh/n4/b1024` | 1.4341 | 0.1832 | 1.0549 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0077 | 0.0035 |
| `eigvalsh/n8/b1024` | 4.3816 | 0.5730 | 3.3147 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0061 | 0.0029 |
| `full_piv_lu/n16/b1024` | 2.8557 | 0.4218 | 3.5761 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0039 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2691 | 0.0426 | 0.3301 |
| `full_piv_lu/n8/b1` | 0.0012 | 0.0038 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7386 | 0.1908 | 0.8057 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0068 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.0911 | 0.4116 | 5.1322 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0037 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4488 | 0.1201 | 0.9835 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0047 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1119 | 0.2851 | 1.9548 |
| `householder_apply/n16/b1` | 0.0027 | 0.0057 | 0.0035 |
| `householder_apply/n16/b1024` | 3.2381 | 0.7242 | 4.1117 |
| `householder_apply/n4/b1` | 0.0003 | 0.0040 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1978 | 0.0368 | 0.2656 |
| `householder_apply/n8/b1` | 0.0008 | 0.0038 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6629 | 0.1689 | 0.7731 |
| `householder_factor/n16/b1` | 0.0027 | 0.0058 | 0.0037 |
| `householder_factor/n16/b1024` | 2.6750 | 0.6777 | 3.8012 |
| `householder_factor/n4/b1` | 0.0004 | 0.0037 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3233 | 0.0492 | 0.3101 |
| `householder_factor/n8/b1` | 0.0009 | 0.0039 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8648 | 0.2204 | 0.8890 |
| `lu/n16/b1` | 0.0022 | 0.0056 | 0.0022 |
| `lu/n16/b1024` | 1.8913 | 0.2911 | 2.2130 |
| `lu/n4/b1` | 0.0005 | 0.0032 | 0.0004 |
| `lu/n4/b1024` | 0.2085 | 0.0355 | 0.1698 |
| `lu/n8/b1` | 0.0008 | 0.0039 | 0.0007 |
| `lu/n8/b1024` | 0.5484 | 0.1447 | 0.5257 |
| `lu_factor/n16/b1` | 0.0014 | 0.0041 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2264 | 0.3132 | 1.5970 |
| `lu_factor/n4/b1` | 0.0004 | 0.0038 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1617 | 0.0460 | 0.1099 |
| `lu_factor/n8/b1` | 0.0006 | 0.0043 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3931 | 0.0608 | 0.3703 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0055 | 0.0032 |
| `lu_factor_solve/n16/b1024` | 2.0083 | 0.5109 | 3.1927 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0024 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2502 | 0.0703 | 0.2511 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0033 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6844 | 0.1792 | 0.9968 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0037 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7852 | 0.2085 | 1.5643 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0022 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0961 | 0.0331 | 0.1447 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0039 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2866 | 0.0850 | 0.6398 |
| `qr/n16/b1` | 0.0067 | 0.0095 | 0.0063 |
| `qr/n16/b1024` | 6.5761 | 0.8709 | 6.3835 |
| `qr/n4/b1` | 0.0007 | 0.0040 | 0.0009 |
| `qr/n4/b1024` | 0.5033 | 0.0718 | 0.5799 |
| `qr/n8/b1` | 0.0018 | 0.0054 | 0.0019 |
| `qr/n8/b1024` | 1.5422 | 0.3966 | 1.5764 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0184 | 0.0094 |
| `rank_revealing_qr/n16/b1024` | 7.2539 | 1.8628 | 9.6010 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0037 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8293 | 0.1213 | 1.0851 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0058 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1614 | 0.3733 | 2.8362 |
| `solve/n16/b1` | 0.0028 | 0.0058 | 0.0036 |
| `solve/n16/b1024` | 2.3170 | 0.5720 | 3.3436 |
| `solve/n4/b1` | 0.0007 | 0.0037 | 0.0005 |
| `solve/n4/b1024` | 0.3222 | 0.0843 | 0.2903 |
| `solve/n8/b1` | 0.0012 | 0.0044 | 0.0012 |
| `solve/n8/b1024` | 0.7681 | 0.1981 | 1.0629 |
| `svd_full/n16/b1` | 0.0348 | 0.0379 | 0.0392 |
| `svd_full/n16/b1024` | 36.5985 | 7.5337 | 40.8509 |
| `svd_full/n4/b1` | 0.0031 | 0.0064 | 0.0046 |
| `svd_full/n4/b1024` | 3.0574 | 0.7743 | 4.4341 |
| `svd_full/n8/b1` | 0.0098 | 0.0122 | 0.0126 |
| `svd_full/n8/b1024` | 10.1383 | 1.3128 | 13.2090 |
| `svd_thin/n16/b1` | 0.0348 | 0.0378 | 0.0393 |
| `svd_thin/n16/b1024` | 36.5415 | 7.6536 | 40.6736 |
| `svd_thin/n4/b1` | 0.0031 | 0.0063 | 0.0046 |
| `svd_thin/n4/b1024` | 3.0787 | 0.7730 | 4.4262 |
| `svd_thin/n8/b1` | 0.0098 | 0.0123 | 0.0127 |
| `svd_thin/n8/b1024` | 10.1679 | 1.3161 | 13.3381 |
| `svd_values/n16/b1` | 0.0262 | 0.0289 | 0.0164 |
| `svd_values/n16/b1024` | 27.3733 | 4.0378 | 16.8830 |
| `svd_values/n4/b1` | 0.0025 | 0.0055 | 0.0023 |
| `svd_values/n4/b1024` | 2.3304 | 0.5858 | 2.1089 |
| `svd_values/n8/b1` | 0.0077 | 0.0106 | 0.0054 |
| `svd_values/n8/b1024` | 7.8393 | 1.7425 | 5.4684 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0033 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5833 | 0.1527 | 0.8360 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0023 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0961 | 0.0282 | 0.1804 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0038 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2379 | 0.0648 | 0.3579 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0416 | - | 0.0556 |
| `cholesky/n128/b128` | 5.8685 | - | 8.1978 |
| `cholesky/n32/b1` | 0.0022 | - | 0.0022 |
| `cholesky/n32/b128` | 0.2673 | - | 0.2635 |
| `eigh/n128/b1` | 1.2534 | - | 1.0762 |
| `eigh/n128/b128` | 162.1487 | - | 145.6218 |
| `eigh/n32/b1` | 0.0639 | - | 0.0552 |
| `eigh/n32/b128` | 8.5103 | - | 7.0624 |
| `eigvalsh/n128/b1` | 0.6970 | - | 0.4538 |
| `eigvalsh/n128/b128` | 90.6422 | - | 59.0640 |
| `eigvalsh/n32/b1` | 0.0492 | - | 0.0246 |
| `eigvalsh/n32/b128` | 6.4705 | - | 3.2177 |
| `householder_apply/n128/b1` | 0.1296 | - | 0.3150 |
| `householder_apply/n128/b128` | 17.3669 | - | 42.9387 |
| `householder_apply/n32/b1` | 0.0112 | - | 0.0075 |
| `householder_apply/n32/b128` | 1.3918 | - | 0.9406 |
| `householder_factor/n128/b1` | 0.1057 | - | 0.1948 |
| `householder_factor/n128/b128` | 13.6884 | - | 25.7211 |
| `householder_factor/n32/b1` | 0.0075 | - | 0.0068 |
| `householder_factor/n32/b128` | 0.9520 | - | 0.8844 |
| `lu/n128/b1` | 0.1092 | - | 0.0825 |
| `lu/n128/b128` | 12.9341 | - | 12.9726 |
| `lu/n32/b1` | 0.0060 | - | 0.0062 |
| `lu/n32/b128` | 0.6963 | - | 0.7729 |
| `lu_factor/n128/b1` | 0.0557 | - | 0.0729 |
| `lu_factor/n128/b128` | 8.2933 | - | 10.0250 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0051 |
| `lu_factor/n32/b128` | 0.3868 | - | 0.6586 |
| `lu_factor_solve/n128/b1` | 0.0613 | - | 0.0848 |
| `lu_factor_solve/n128/b128` | 8.9276 | - | 11.5081 |
| `lu_factor_solve/n32/b1` | 0.0041 | - | 0.0067 |
| `lu_factor_solve/n32/b128` | 0.4830 | - | 0.8568 |
| `lu_solve_prepared/n128/b1` | 0.0059 | - | 0.0121 |
| `lu_solve_prepared/n128/b128` | 1.5887 | - | 2.4041 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0014 |
| `lu_solve_prepared/n32/b128` | 0.1145 | - | 0.1698 |
| `qr/n128/b1` | 0.3424 | - | 0.3917 |
| `qr/n128/b128` | 43.7207 | - | 52.0112 |
| `qr/n32/b1` | 0.0210 | - | 0.0121 |
| `qr/n32/b128` | 2.6528 | - | 1.5566 |
| `rank_revealing_qr/n128/b1` | 0.3520 | - | 0.4776 |
| `rank_revealing_qr/n128/b128` | 44.4282 | - | 62.9061 |
| `rank_revealing_qr/n32/b1` | 0.0212 | - | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6619 | - | 2.2911 |
| `solve/n128/b1` | 0.0685 | - | 0.0876 |
| `solve/n128/b128` | 8.8419 | - | 12.0005 |
| `solve/n32/b1` | 0.0049 | - | 0.0071 |
| `solve/n32/b128` | 0.5448 | - | 0.8738 |
| `svd_thin/n128/b1` | 2.4244 | - | 2.0388 |
| `svd_thin/n128/b128` | 309.6488 | - | 264.3444 |
| `svd_thin/n32/b1` | 0.1253 | - | 0.1065 |
| `svd_thin/n32/b128` | 15.2660 | - | 13.7564 |
| `svd_values/n128/b1` | 1.4199 | - | 0.7037 |
| `svd_values/n128/b128` | 181.0619 | - | 92.4176 |
| `svd_values/n32/b1` | 0.0932 | - | 0.0373 |
| `svd_values/n32/b128` | 12.0608 | - | 4.8664 |
| `triangular_solve/n128/b1` | 0.0040 | - | 0.0070 |
| `triangular_solve/n128/b128` | 0.9901 | - | 1.3465 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0008 |
| `triangular_solve/n32/b128` | 0.0902 | - | 0.0873 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0413 | 0.0526 | 0.0567 |
| `cholesky/n128/b128` | 5.9414 | 6.5204 | 8.2618 |
| `cholesky/n32/b1` | 0.0022 | 0.0044 | 0.0022 |
| `cholesky/n32/b128` | 0.2686 | 0.0712 | 0.2619 |
| `eigh/n128/b1` | 1.2573 | 1.2246 | 0.6225 |
| `eigh/n128/b128` | 162.7449 | 164.0454 | 84.4250 |
| `eigh/n32/b1` | 0.0644 | 0.0682 | 0.0584 |
| `eigh/n32/b128` | 8.4584 | 4.2865 | 7.4480 |
| `eigvalsh/n128/b1` | 0.6940 | 0.7072 | 0.4342 |
| `eigvalsh/n128/b128` | 90.8525 | 91.3268 | 56.8214 |
| `eigvalsh/n32/b1` | 0.0488 | 0.0517 | 0.0247 |
| `eigvalsh/n32/b128` | 6.4117 | 2.2846 | 3.2328 |
| `householder_apply/n128/b1` | 0.1288 | 0.1317 | 0.0859 |
| `householder_apply/n128/b128` | 17.3720 | 17.6084 | 11.4600 |
| `householder_apply/n32/b1` | 0.0107 | 0.0139 | 0.0074 |
| `householder_apply/n32/b128` | 1.3664 | 0.6844 | 0.9211 |
| `householder_factor/n128/b1` | 0.1082 | 0.1227 | 0.1140 |
| `householder_factor/n128/b128` | 13.6441 | 16.7236 | 15.1048 |
| `householder_factor/n32/b1` | 0.0074 | 0.0101 | 0.0068 |
| `householder_factor/n32/b128` | 0.9346 | 0.2379 | 0.8884 |
| `lu/n128/b1` | 0.0998 | 0.1164 | 0.0822 |
| `lu/n128/b128` | 12.8793 | 16.0028 | 12.9813 |
| `lu/n32/b1` | 0.0060 | 0.0092 | 0.0062 |
| `lu/n32/b128` | 0.6621 | 0.3256 | 0.7680 |
| `lu_factor/n128/b1` | 0.0570 | 0.0733 | 0.0730 |
| `lu_factor/n128/b128` | 8.2130 | 4.0475 | 10.0326 |
| `lu_factor/n32/b1` | 0.0032 | 0.0056 | 0.0052 |
| `lu_factor/n32/b128` | 0.3883 | 0.2050 | 0.6542 |
| `lu_factor_solve/n128/b1` | 0.0628 | 0.0769 | 0.0873 |
| `lu_factor_solve/n128/b128` | 8.9323 | 2.7327 | 11.9650 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0074 | 0.0078 |
| `lu_factor_solve/n32/b128` | 0.4983 | 0.2555 | 0.9859 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0084 | 0.0095 |
| `lu_solve_prepared/n128/b128` | 1.8935 | 0.5311 | 2.3268 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0034 | 0.0023 |
| `lu_solve_prepared/n32/b128` | 0.1138 | 0.0341 | 0.3013 |
| `qr/n128/b1` | 0.3498 | 0.6231 | 0.2618 |
| `qr/n128/b128` | 45.0582 | 81.4862 | 40.1552 |
| `qr/n32/b1` | 0.0213 | 0.0448 | 0.0120 |
| `qr/n32/b128` | 2.6393 | 0.6954 | 1.5642 |
| `rank_revealing_qr/n128/b1` | 0.3493 | 0.3656 | 0.4269 |
| `rank_revealing_qr/n128/b128` | 44.8248 | 47.7021 | 61.0238 |
| `rank_revealing_qr/n32/b1` | 0.0209 | 0.0443 | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6171 | 0.6646 | 2.2875 |
| `solve/n128/b1` | 0.0684 | 0.0836 | 0.0906 |
| `solve/n128/b128` | 8.8952 | 10.7769 | 12.1139 |
| `solve/n32/b1` | 0.0050 | 0.0081 | 0.0082 |
| `solve/n32/b128` | 0.5510 | 0.2839 | 1.0379 |
| `svd_thin/n128/b1` | 2.4365 | 1.8225 | 1.5982 |
| `svd_thin/n128/b128` | 310.8498 | 231.4991 | 210.6209 |
| `svd_thin/n32/b1` | 0.1178 | 0.1223 | 0.1112 |
| `svd_thin/n32/b128` | 15.1669 | 4.2568 | 14.4979 |
| `svd_values/n128/b1` | 1.4118 | 1.4435 | 0.6824 |
| `svd_values/n128/b128` | 180.7823 | 181.2078 | 89.3999 |
| `svd_values/n32/b1` | 0.0925 | 0.0971 | 0.0373 |
| `svd_values/n32/b128` | 11.9246 | 3.0596 | 4.8447 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0062 | 0.0059 |
| `triangular_solve/n128/b128` | 0.7775 | 0.7775 | 1.3843 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0024 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0876 | 0.0456 | 0.1672 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0412 | 0.0562 | 0.0556 |
| `cholesky/n128/b128` | 5.8693 | 7.3516 | 8.3385 |
| `cholesky/n32/b1` | 0.0022 | 0.0053 | 0.0022 |
| `cholesky/n32/b128` | 0.2679 | 0.0711 | 0.2569 |
| `eigh/n128/b1` | 1.2621 | 1.2378 | 0.5863 |
| `eigh/n128/b128` | 162.9376 | 159.9384 | 78.9460 |
| `eigh/n32/b1` | 0.0642 | 0.0687 | 0.0589 |
| `eigh/n32/b128` | 8.4627 | 1.5121 | 7.5020 |
| `eigvalsh/n128/b1` | 0.6981 | 0.7032 | 0.4457 |
| `eigvalsh/n128/b128` | 89.7708 | 90.5421 | 58.4525 |
| `eigvalsh/n32/b1` | 0.0487 | 0.0519 | 0.0247 |
| `eigvalsh/n32/b128` | 6.3964 | 1.5016 | 3.2237 |
| `householder_apply/n128/b1` | 0.1284 | 0.1916 | 0.0574 |
| `householder_apply/n128/b128` | 17.6166 | 24.9399 | 7.4240 |
| `householder_apply/n32/b1` | 0.0112 | 0.0137 | 0.0073 |
| `householder_apply/n32/b128` | 1.3602 | 0.3545 | 0.9090 |
| `householder_factor/n128/b1` | 0.1103 | 0.1772 | 0.0883 |
| `householder_factor/n128/b128` | 14.4481 | 23.2118 | 11.5015 |
| `householder_factor/n32/b1` | 0.0074 | 0.0106 | 0.0067 |
| `householder_factor/n32/b128` | 0.9569 | 0.2433 | 0.8840 |
| `lu/n128/b1` | 0.1083 | 0.1306 | 0.0829 |
| `lu/n128/b128` | 13.1331 | 16.9726 | 12.9955 |
| `lu/n32/b1` | 0.0061 | 0.0091 | 0.0062 |
| `lu/n32/b128` | 0.6837 | 0.1777 | 0.7762 |
| `lu_factor/n128/b1` | 0.0565 | 0.0824 | 0.0726 |
| `lu_factor/n128/b128` | 8.1794 | 1.7246 | 10.0580 |
| `lu_factor/n32/b1` | 0.0033 | 0.0068 | 0.0052 |
| `lu_factor/n32/b128` | 0.3888 | 0.1076 | 0.6570 |
| `lu_factor_solve/n128/b1` | 0.0620 | 0.0885 | 0.0874 |
| `lu_factor_solve/n128/b128` | 8.9236 | 1.6476 | 11.7930 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0072 | 0.0077 |
| `lu_factor_solve/n32/b128` | 0.4896 | 0.1339 | 1.0129 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0086 | 0.0098 |
| `lu_solve_prepared/n128/b128` | 2.0750 | 0.5241 | 2.2930 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0037 | 0.0023 |
| `lu_solve_prepared/n32/b128` | 0.1143 | 0.0237 | 0.3314 |
| `qr/n128/b1` | 0.3422 | 0.9600 | 0.2866 |
| `qr/n128/b128` | 44.5279 | 121.7059 | 31.1472 |
| `qr/n32/b1` | 0.0211 | 0.0639 | 0.0122 |
| `qr/n32/b128` | 2.6246 | 0.6930 | 1.5382 |
| `rank_revealing_qr/n128/b1` | 0.3480 | 0.4248 | 0.4860 |
| `rank_revealing_qr/n128/b128` | 45.3288 | 56.0998 | 63.7707 |
| `rank_revealing_qr/n32/b1` | 0.0213 | 0.0670 | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6317 | 0.3341 | 2.2609 |
| `solve/n128/b1` | 0.0683 | 0.0949 | 0.0897 |
| `solve/n128/b128` | 8.7488 | 12.3297 | 12.2146 |
| `solve/n32/b1` | 0.0049 | 0.0080 | 0.0080 |
| `solve/n32/b128` | 0.5439 | 0.1435 | 1.0285 |
| `svd_thin/n128/b1` | 2.4205 | 1.8633 | 1.5479 |
| `svd_thin/n128/b128` | 308.3374 | 239.1412 | 199.6557 |
| `svd_thin/n32/b1` | 0.1174 | 0.1221 | 0.1131 |
| `svd_thin/n32/b128` | 15.2642 | 2.6456 | 14.5583 |
| `svd_values/n128/b1` | 1.4114 | 1.4327 | 0.6779 |
| `svd_values/n128/b128` | 181.5038 | 180.0999 | 90.4761 |
| `svd_values/n32/b1` | 0.0928 | 0.0973 | 0.0373 |
| `svd_values/n32/b128` | 12.0079 | 1.9644 | 4.8396 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0067 | 0.0064 |
| `triangular_solve/n128/b128` | 0.9343 | 0.9980 | 1.4034 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0033 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0904 | 0.0251 | 0.1831 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1103 | - | 0.2427 |
| `cholesky/n128/b128` | 16.0067 | - | 32.8471 |
| `cholesky/n32/b1` | 0.0034 | - | 0.0048 |
| `cholesky/n32/b128` | 0.4301 | - | 0.6226 |
| `eigh/n128/b1` | 1.8468 | - | 2.9696 |
| `eigh/n128/b128` | 240.7364 | - | 384.7216 |
| `eigh/n32/b1` | 0.0804 | - | 0.0864 |
| `eigh/n32/b128` | 10.5007 | - | 11.3297 |
| `eigvalsh/n128/b1` | 0.9245 | - | 1.2632 |
| `eigvalsh/n128/b128` | 121.9083 | - | 163.5309 |
| `eigvalsh/n32/b1` | 0.0524 | - | 0.0439 |
| `eigvalsh/n32/b128` | 6.9072 | - | 5.7510 |
| `householder_apply/n128/b1` | 0.4745 | - | 0.9647 |
| `householder_apply/n128/b128` | 64.3385 | - | 125.1041 |
| `householder_apply/n32/b1` | 0.0151 | - | 0.0196 |
| `householder_apply/n32/b128` | 1.9347 | - | 2.5434 |
| `householder_factor/n128/b1` | 0.3438 | - | 0.5388 |
| `householder_factor/n128/b128` | 45.4873 | - | 70.5303 |
| `householder_factor/n32/b1` | 0.0114 | - | 0.0156 |
| `householder_factor/n32/b128` | 1.4580 | - | 2.0135 |
| `lu/n128/b1` | 0.2006 | - | 0.2697 |
| `lu/n128/b128` | 27.8251 | - | 38.6991 |
| `lu/n32/b1` | 0.0079 | - | 0.0106 |
| `lu/n32/b128` | 1.0337 | - | 1.4339 |
| `lu_factor/n128/b1` | 0.1556 | - | 0.2476 |
| `lu_factor/n128/b128` | 21.8648 | - | 32.7186 |
| `lu_factor/n32/b1` | 0.0053 | - | 0.0090 |
| `lu_factor/n32/b128` | 0.6534 | - | 1.1443 |
| `lu_factor_solve/n128/b1` | 0.1756 | - | 0.2797 |
| `lu_factor_solve/n128/b128` | 24.3613 | - | 36.9948 |
| `lu_factor_solve/n32/b1` | 0.0076 | - | 0.0133 |
| `lu_factor_solve/n32/b128` | 0.9250 | - | 1.7090 |
| `lu_solve_prepared/n128/b1` | 0.0188 | - | 0.0310 |
| `lu_solve_prepared/n128/b128` | 4.1554 | - | 5.7732 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0044 |
| `lu_solve_prepared/n32/b128` | 0.2834 | - | 0.5579 |
| `qr/n128/b1` | 0.9697 | - | 1.1369 |
| `qr/n128/b128` | 124.7775 | - | 148.2360 |
| `qr/n32/b1` | 0.0425 | - | 0.0284 |
| `qr/n32/b128` | 5.4239 | - | 3.6600 |
| `rank_revealing_qr/n128/b1` | 1.0074 | - | 1.5967 |
| `rank_revealing_qr/n128/b128` | 129.8420 | - | 207.2306 |
| `rank_revealing_qr/n32/b1` | 0.0389 | - | 0.0391 |
| `rank_revealing_qr/n32/b128` | 4.9567 | - | 5.1419 |
| `solve/n128/b1` | 0.1814 | - | 0.2882 |
| `solve/n128/b128` | 23.7871 | - | 37.5839 |
| `solve/n32/b1` | 0.0084 | - | 0.0139 |
| `solve/n32/b128` | 0.9799 | - | 1.7563 |
| `svd_thin/n128/b1` | 3.9741 | - | 4.1805 |
| `svd_thin/n128/b128` | 514.3552 | - | 539.3087 |
| `svd_thin/n32/b1` | 0.1505 | - | 0.1536 |
| `svd_thin/n32/b128` | 19.7144 | - | 20.6771 |
| `svd_values/n128/b1` | 1.9338 | - | 1.5927 |
| `svd_values/n128/b128` | 250.8060 | - | 205.7708 |
| `svd_values/n32/b1` | 0.1026 | - | 0.0609 |
| `svd_values/n32/b128` | 13.3895 | - | 7.9355 |
| `triangular_solve/n128/b1` | 0.0110 | - | 0.0148 |
| `triangular_solve/n128/b128` | 2.3419 | - | 2.8336 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0021 |
| `triangular_solve/n32/b128` | 0.1919 | - | 0.2650 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1078 | 0.1092 | 0.2449 |
| `cholesky/n128/b128` | 15.9328 | 15.7158 | 32.9681 |
| `cholesky/n32/b1` | 0.0034 | 0.0058 | 0.0049 |
| `cholesky/n32/b128` | 0.4208 | 0.1160 | 0.6303 |
| `eigh/n128/b1` | 1.8368 | 1.7471 | 1.8215 |
| `eigh/n128/b128` | 241.2735 | 208.3410 | 235.6227 |
| `eigh/n32/b1` | 0.0803 | 0.0850 | 0.0868 |
| `eigh/n32/b128` | 10.5299 | 2.6442 | 11.3600 |
| `eigvalsh/n128/b1` | 0.9338 | 0.9266 | 0.8176 |
| `eigvalsh/n128/b128` | 123.0000 | 121.3309 | 106.3586 |
| `eigvalsh/n32/b1` | 0.0523 | 0.0556 | 0.0439 |
| `eigvalsh/n32/b128` | 6.8819 | 1.7289 | 5.7722 |
| `householder_apply/n128/b1` | 0.4839 | 0.2613 | 0.2933 |
| `householder_apply/n128/b128` | 64.3243 | 35.1744 | 37.2249 |
| `householder_apply/n32/b1` | 0.0146 | 0.0179 | 0.0194 |
| `householder_apply/n32/b128` | 1.9143 | 0.9465 | 2.5665 |
| `householder_factor/n128/b1` | 0.3503 | 0.2279 | 0.2593 |
| `householder_factor/n128/b128` | 45.5799 | 29.6680 | 33.6702 |
| `householder_factor/n32/b1` | 0.0114 | 0.0141 | 0.0156 |
| `householder_factor/n32/b128` | 1.4465 | 0.3728 | 2.0091 |
| `lu/n128/b1` | 0.2025 | 0.1919 | 0.2723 |
| `lu/n128/b128` | 28.2431 | 26.6258 | 39.0467 |
| `lu/n32/b1` | 0.0080 | 0.0110 | 0.0105 |
| `lu/n32/b128` | 1.0566 | 0.5041 | 1.4357 |
| `lu_factor/n128/b1` | 0.1560 | 0.1465 | 0.2507 |
| `lu_factor/n128/b128` | 21.7786 | 6.2471 | 32.6187 |
| `lu_factor/n32/b1` | 0.0053 | 0.0079 | 0.0090 |
| `lu_factor/n32/b128` | 0.6526 | 0.3342 | 1.1319 |
| `lu_factor_solve/n128/b1` | 0.1754 | 0.1659 | 0.2698 |
| `lu_factor_solve/n128/b128` | 24.2641 | 6.5138 | 35.3536 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0099 | 0.0119 |
| `lu_factor_solve/n32/b128` | 0.9224 | 0.2374 | 1.5491 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0219 | 0.0151 |
| `lu_solve_prepared/n128/b128` | 4.2364 | 1.2347 | 3.7641 |
| `lu_solve_prepared/n32/b1` | 0.0022 | 0.0044 | 0.0026 |
| `lu_solve_prepared/n32/b128` | 0.2784 | 0.0756 | 0.3471 |
| `qr/n128/b1` | 0.9689 | 0.8869 | 0.5925 |
| `qr/n128/b128` | 125.3949 | 114.1540 | 78.2113 |
| `qr/n32/b1` | 0.0425 | 0.0671 | 0.0285 |
| `qr/n32/b128` | 5.4435 | 1.8064 | 3.6674 |
| `rank_revealing_qr/n128/b1` | 1.0114 | 0.7910 | 1.3693 |
| `rank_revealing_qr/n128/b128` | 130.6386 | 104.0761 | 178.2473 |
| `rank_revealing_qr/n32/b1` | 0.0391 | 0.0643 | 0.0390 |
| `rank_revealing_qr/n32/b128` | 4.9505 | 2.5264 | 5.1353 |
| `solve/n128/b1` | 0.1817 | 0.1700 | 0.2764 |
| `solve/n128/b128` | 23.8157 | 22.2983 | 36.5373 |
| `solve/n32/b1` | 0.0084 | 0.0112 | 0.0126 |
| `solve/n32/b128` | 0.9781 | 0.2503 | 1.5917 |
| `svd_thin/n128/b1` | 3.9940 | 2.7608 | 2.5129 |
| `svd_thin/n128/b128` | 515.1627 | 357.4215 | 324.7898 |
| `svd_thin/n32/b1` | 0.1510 | 0.1551 | 0.1577 |
| `svd_thin/n32/b128` | 19.6694 | 8.0408 | 21.2921 |
| `svd_values/n128/b1` | 1.9330 | 1.9570 | 1.2182 |
| `svd_values/n128/b128` | 250.1290 | 249.8369 | 158.0306 |
| `svd_values/n32/b1` | 0.1018 | 0.1055 | 0.0604 |
| `svd_values/n32/b128` | 13.3644 | 6.5003 | 7.9216 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0137 | 0.0078 |
| `triangular_solve/n128/b128` | 2.2885 | 2.1576 | 2.3122 |
| `triangular_solve/n32/b1` | 0.0015 | 0.0040 | 0.0015 |
| `triangular_solve/n32/b128` | 0.1900 | 0.0972 | 0.1792 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1106 | 0.1185 | 0.2462 |
| `cholesky/n128/b128` | 15.9654 | 16.5011 | 33.0432 |
| `cholesky/n32/b1` | 0.0034 | 0.0066 | 0.0048 |
| `cholesky/n32/b128` | 0.4254 | 0.0587 | 0.6260 |
| `eigh/n128/b1` | 1.8338 | 1.6154 | 1.6094 |
| `eigh/n128/b128` | 240.7612 | 210.9845 | 211.6621 |
| `eigh/n32/b1` | 0.0807 | 0.0848 | 0.0868 |
| `eigh/n32/b128` | 10.4664 | 1.6846 | 11.3859 |
| `eigvalsh/n128/b1` | 0.9292 | 0.9326 | 0.7375 |
| `eigvalsh/n128/b128` | 121.3293 | 121.8461 | 96.6284 |
| `eigvalsh/n32/b1` | 0.0524 | 0.0553 | 0.0444 |
| `eigvalsh/n32/b128` | 6.8897 | 1.7557 | 5.7909 |
| `householder_apply/n128/b1` | 0.4877 | 0.3457 | 0.1980 |
| `householder_apply/n128/b128` | 64.5373 | 44.5880 | 21.3422 |
| `householder_apply/n32/b1` | 0.0174 | 0.0180 | 0.0197 |
| `householder_apply/n32/b128` | 2.1897 | 0.3700 | 2.5650 |
| `householder_factor/n128/b1` | 0.3511 | 0.2875 | 0.1823 |
| `householder_factor/n128/b128` | 46.2306 | 36.6943 | 23.5174 |
| `householder_factor/n32/b1` | 0.0131 | 0.0160 | 0.0155 |
| `householder_factor/n32/b128` | 1.6128 | 0.2948 | 2.0141 |
| `lu/n128/b1` | 0.2005 | 0.2024 | 0.2689 |
| `lu/n128/b128` | 28.3804 | 28.1446 | 38.8637 |
| `lu/n32/b1` | 0.0080 | 0.0109 | 0.0105 |
| `lu/n32/b128` | 1.0110 | 0.2440 | 1.4388 |
| `lu_factor/n128/b1` | 0.1571 | 0.1580 | 0.2484 |
| `lu_factor/n128/b128` | 21.8075 | 3.2917 | 32.6766 |
| `lu_factor/n32/b1` | 0.0054 | 0.0089 | 0.0091 |
| `lu_factor/n32/b128` | 0.6435 | 0.1731 | 1.1423 |
| `lu_factor_solve/n128/b1` | 0.1771 | 0.1795 | 0.2685 |
| `lu_factor_solve/n128/b128` | 24.3593 | 3.6167 | 35.3262 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0104 | 0.0119 |
| `lu_factor_solve/n32/b128` | 0.9287 | 0.2443 | 1.5287 |
| `lu_solve_prepared/n128/b1` | 0.0188 | 0.0219 | 0.0152 |
| `lu_solve_prepared/n128/b128` | 4.2229 | 1.1231 | 3.6816 |
| `lu_solve_prepared/n32/b1` | 0.0022 | 0.0054 | 0.0027 |
| `lu_solve_prepared/n32/b128` | 0.2821 | 0.0764 | 0.3503 |
| `qr/n128/b1` | 0.9712 | 1.2212 | 0.4334 |
| `qr/n128/b128` | 124.9589 | 156.6581 | 57.9733 |
| `qr/n32/b1` | 0.0422 | 0.0870 | 0.0284 |
| `qr/n32/b128` | 5.4097 | 0.8743 | 3.6513 |
| `rank_revealing_qr/n128/b1` | 1.0142 | 0.8916 | 1.2223 |
| `rank_revealing_qr/n128/b128` | 130.2352 | 114.1211 | 160.2123 |
| `rank_revealing_qr/n32/b1` | 0.0390 | 0.0888 | 0.0390 |
| `rank_revealing_qr/n32/b128` | 4.9536 | 1.2598 | 5.1849 |
| `solve/n128/b1` | 0.1809 | 0.1822 | 0.2802 |
| `solve/n128/b128` | 23.8235 | 23.6569 | 36.5682 |
| `solve/n32/b1` | 0.0084 | 0.0117 | 0.0126 |
| `solve/n32/b128` | 0.9831 | 0.2510 | 1.6058 |
| `svd_thin/n128/b1` | 3.9766 | 2.8208 | 2.2206 |
| `svd_thin/n128/b128` | 513.8447 | 363.5805 | 288.4485 |
| `svd_thin/n32/b1` | 0.1511 | 0.1556 | 0.1599 |
| `svd_thin/n32/b128` | 21.0347 | 2.5734 | 21.5111 |
| `svd_values/n128/b1` | 1.9290 | 1.9573 | 1.1562 |
| `svd_values/n128/b128` | 250.6817 | 249.8246 | 150.4173 |
| `svd_values/n32/b1` | 0.1013 | 0.1054 | 0.0608 |
| `svd_values/n32/b128` | 13.3666 | 1.7141 | 7.9410 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0139 | 0.0077 |
| `triangular_solve/n128/b128` | 2.2986 | 2.1802 | 2.2961 |
| `triangular_solve/n32/b1` | 0.0015 | 0.0045 | 0.0015 |
| `triangular_solve/n32/b128` | 0.1918 | 0.0496 | 0.1804 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2089 | - | 0.2692 |
| `cholesky/n256/b4` | 0.8495 | - | 1.0903 |
| `cholesky/n512/b1` | 1.3339 | - | 2.0072 |
| `cholesky/n512/b4` | 5.6625 | - | 8.4766 |
| `eigh/n256/b1` | 5.5818 | - | 5.9182 |
| `eigh/n256/b4` | 22.3920 | - | 23.8303 |
| `eigh/n512/b1` | 28.7398 | - | 36.6573 |
| `eigh/n512/b4` | 115.3735 | - | 146.0130 |
| `eigvalsh/n256/b1` | 2.9335 | - | 2.5768 |
| `eigvalsh/n256/b4` | 11.9730 | - | 10.3384 |
| `eigvalsh/n512/b1` | 14.0564 | - | 16.5003 |
| `eigvalsh/n512/b4` | 56.6024 | - | 66.6340 |
| `householder_apply/n256/b1` | 0.8219 | - | 1.9379 |
| `householder_apply/n256/b4` | 3.3013 | - | 7.8508 |
| `householder_apply/n512/b1` | 6.0497 | - | 12.8848 |
| `householder_apply/n512/b4` | 25.3373 | - | 52.3410 |
| `householder_factor/n256/b1` | 0.6160 | - | 1.1200 |
| `householder_factor/n256/b4` | 2.4916 | - | 4.5181 |
| `householder_factor/n512/b1` | 4.3736 | - | 8.1010 |
| `householder_factor/n512/b4` | 17.5602 | - | 32.1853 |
| `lu/n256/b1` | 0.5151 | - | 0.5008 |
| `lu/n256/b4` | 2.0868 | - | 2.1376 |
| `lu/n512/b1` | 3.3066 | - | 3.3284 |
| `lu/n512/b4` | 13.2777 | - | 13.5390 |
| `lu_factor/n256/b1` | 0.3514 | - | 0.4563 |
| `lu_factor/n256/b4` | 1.5341 | - | 1.8401 |
| `lu_factor/n512/b1` | 2.7586 | - | 3.0038 |
| `lu_factor/n512/b4` | 11.7635 | - | 12.3803 |
| `lu_factor_solve/n256/b1` | 0.3705 | - | 0.4994 |
| `lu_factor_solve/n256/b4` | 1.6013 | - | 2.0052 |
| `lu_factor_solve/n512/b1` | 2.8232 | - | 3.1706 |
| `lu_factor_solve/n512/b4` | 12.0054 | - | 13.2115 |
| `lu_solve_prepared/n256/b1` | 0.0168 | - | 0.0400 |
| `lu_solve_prepared/n256/b4` | 0.0810 | - | 0.1740 |
| `lu_solve_prepared/n512/b1` | 0.0694 | - | 0.1890 |
| `lu_solve_prepared/n512/b4` | 0.3731 | - | 0.9687 |
| `qr/n256/b1` | 1.8589 | - | 2.3791 |
| `qr/n256/b4` | 7.4352 | - | 9.6092 |
| `qr/n512/b1` | 11.6032 | - | 17.1267 |
| `qr/n512/b4` | 46.2602 | - | 69.5148 |
| `rank_revealing_qr/n256/b1` | 2.1143 | - | 2.9265 |
| `rank_revealing_qr/n256/b4` | 8.3795 | - | 11.8211 |
| `rank_revealing_qr/n512/b1` | 14.7435 | - | 21.3598 |
| `rank_revealing_qr/n512/b4` | 58.9534 | - | 86.2939 |
| `solve/n256/b1` | 0.3975 | - | 0.5080 |
| `solve/n256/b4` | 1.5744 | - | 2.0371 |
| `solve/n512/b1` | 2.8803 | - | 3.2302 |
| `solve/n512/b4` | 11.4455 | - | 12.9499 |
| `svd_thin/n256/b1` | 12.3010 | - | 10.9468 |
| `svd_thin/n256/b4` | 48.9109 | - | 43.7326 |
| `svd_thin/n512/b1` | 71.0068 | - | 71.6405 |
| `svd_thin/n512/b4` | 285.2323 | - | 288.6680 |
| `svd_values/n256/b1` | 6.9957 | - | 4.1204 |
| `svd_values/n256/b4` | 27.8251 | - | 16.5714 |
| `svd_values/n512/b1` | 38.8945 | - | 28.1584 |
| `svd_values/n512/b4` | 155.0768 | - | 114.7034 |
| `triangular_solve/n256/b1` | 0.0104 | - | 0.0234 |
| `triangular_solve/n256/b4` | 0.0453 | - | 0.0983 |
| `triangular_solve/n512/b1` | 0.0367 | - | 0.1091 |
| `triangular_solve/n512/b4` | 0.1404 | - | 0.3949 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2114 | 0.1920 | 0.1624 |
| `cholesky/n256/b4` | 0.8463 | 0.7970 | 0.6669 |
| `cholesky/n512/b1` | 1.3398 | 0.8349 | 0.8908 |
| `cholesky/n512/b4` | 5.6532 | 3.5945 | 3.9980 |
| `eigh/n256/b1` | 5.5424 | 4.2126 | 2.8052 |
| `eigh/n256/b4` | 22.2606 | 16.9459 | 11.2993 |
| `eigh/n512/b1` | 28.4876 | 15.9214 | 13.2797 |
| `eigh/n512/b4` | 114.7281 | 64.0137 | 53.1387 |
| `eigvalsh/n256/b1` | 2.9003 | 2.9281 | 1.8731 |
| `eigvalsh/n256/b4` | 11.7417 | 11.7723 | 7.5161 |
| `eigvalsh/n512/b1` | 14.1300 | 11.9559 | 8.9675 |
| `eigvalsh/n512/b4` | 56.4276 | 47.9901 | 36.0465 |
| `householder_apply/n256/b1` | 0.8281 | 0.3005 | 0.5674 |
| `householder_apply/n256/b4` | 3.3198 | 1.1828 | 2.2690 |
| `householder_apply/n512/b1` | 6.0955 | 1.6982 | 3.4990 |
| `householder_apply/n512/b4` | 25.3101 | 7.1008 | 14.1364 |
| `householder_factor/n256/b1` | 0.6260 | 0.3192 | 0.3659 |
| `householder_factor/n256/b4` | 2.4868 | 1.2842 | 1.4492 |
| `householder_factor/n512/b1` | 4.3543 | 1.5676 | 2.1807 |
| `householder_factor/n512/b4` | 17.2289 | 6.2967 | 8.8187 |
| `lu/n256/b1` | 0.5123 | 0.4736 | 0.2000 |
| `lu/n256/b4` | 2.1259 | 1.9473 | 0.8969 |
| `lu/n512/b1` | 3.3438 | 2.0275 | 1.1431 |
| `lu/n512/b4` | 13.2921 | 8.1412 | 4.8715 |
| `lu_factor/n256/b1` | 0.3836 | 0.3222 | 0.1601 |
| `lu_factor/n256/b4` | 1.5318 | 0.7772 | 0.6494 |
| `lu_factor/n512/b1` | 2.8351 | 1.4801 | 0.8506 |
| `lu_factor/n512/b4` | 11.7894 | 5.9349 | 3.4789 |
| `lu_factor_solve/n256/b1` | 0.3758 | 0.3349 | 0.1917 |
| `lu_factor_solve/n256/b4` | 1.4891 | 0.3833 | 0.7599 |
| `lu_factor_solve/n512/b1` | 2.8970 | 1.5330 | 0.9581 |
| `lu_factor_solve/n512/b4` | 12.0729 | 6.2235 | 3.8893 |
| `lu_solve_prepared/n256/b1` | 0.0172 | 0.0235 | 0.0245 |
| `lu_solve_prepared/n256/b4` | 0.0744 | 0.0416 | 0.1258 |
| `lu_solve_prepared/n512/b1` | 0.0711 | 0.0665 | 0.0972 |
| `lu_solve_prepared/n512/b4` | 0.4431 | 0.2028 | 0.5683 |
| `qr/n256/b1` | 1.8514 | 1.7361 | 1.1509 |
| `qr/n256/b4` | 7.4198 | 7.1620 | 4.5094 |
| `qr/n512/b1` | 11.5312 | 5.9006 | 6.9694 |
| `qr/n512/b4` | 46.6708 | 24.1012 | 28.1175 |
| `rank_revealing_qr/n256/b1` | 2.1052 | 1.4363 | 2.2878 |
| `rank_revealing_qr/n256/b4` | 8.5129 | 5.7160 | 9.2486 |
| `rank_revealing_qr/n512/b1` | 14.8655 | 6.1160 | 15.6938 |
| `rank_revealing_qr/n512/b4` | 59.8066 | 24.4841 | 63.8454 |
| `solve/n256/b1` | 0.3948 | 0.3590 | 0.2100 |
| `solve/n256/b4` | 1.5757 | 1.4250 | 0.8407 |
| `solve/n512/b1` | 2.9091 | 1.5828 | 1.0116 |
| `solve/n512/b4` | 11.4433 | 6.2504 | 4.1532 |
| `svd_thin/n256/b1` | 12.2196 | 8.7671 | 7.7355 |
| `svd_thin/n256/b4` | 48.8644 | 35.8046 | 31.0377 |
| `svd_thin/n512/b1` | 70.9846 | 40.0759 | 37.2375 |
| `svd_thin/n512/b4` | 283.7123 | 159.8452 | 149.0546 |
| `svd_values/n256/b1` | 6.9894 | 7.1410 | 3.7030 |
| `svd_values/n256/b4` | 27.7398 | 28.0775 | 15.0040 |
| `svd_values/n512/b1` | 38.8478 | 31.6788 | 15.5171 |
| `svd_values/n512/b4` | 155.6027 | 126.5848 | 62.8322 |
| `triangular_solve/n256/b1` | 0.0105 | 0.0166 | 0.0154 |
| `triangular_solve/n256/b4` | 0.0458 | 0.0549 | 0.0691 |
| `triangular_solve/n512/b1` | 0.0357 | 0.0354 | 0.0566 |
| `triangular_solve/n512/b4` | 0.1400 | 0.1397 | 0.2793 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2110 | 0.2174 | 0.1622 |
| `cholesky/n256/b4` | 0.8377 | 0.8870 | 0.4785 |
| `cholesky/n512/b1` | 1.3011 | 0.7141 | 0.5548 |
| `cholesky/n512/b4` | 5.6803 | 3.2170 | 2.6837 |
| `eigh/n256/b1` | 5.5726 | 4.1451 | 2.3237 |
| `eigh/n256/b4` | 22.4266 | 16.7446 | 9.3901 |
| `eigh/n512/b1` | 28.6121 | 14.6283 | 9.3187 |
| `eigh/n512/b4` | 114.9476 | 59.6895 | 37.3798 |
| `eigvalsh/n256/b1` | 2.9434 | 2.9464 | 1.7794 |
| `eigvalsh/n256/b4` | 11.9343 | 11.9085 | 7.1458 |
| `eigvalsh/n512/b1` | 13.9601 | 11.4852 | 7.5911 |
| `eigvalsh/n512/b4` | 56.5219 | 46.6049 | 30.5483 |
| `householder_apply/n256/b1` | 0.8392 | 0.3563 | 0.3118 |
| `householder_apply/n256/b4` | 3.3704 | 1.4412 | 1.2270 |
| `householder_apply/n512/b1` | 6.3077 | 1.7251 | 1.9382 |
| `householder_apply/n512/b4` | 25.2440 | 6.9424 | 7.8226 |
| `householder_factor/n256/b1` | 0.6191 | 0.3930 | 0.3194 |
| `householder_factor/n256/b4` | 2.4969 | 1.5715 | 1.2746 |
| `householder_factor/n512/b1` | 4.3671 | 1.6211 | 1.3017 |
| `householder_factor/n512/b4` | 17.6381 | 6.6698 | 5.3799 |
| `lu/n256/b1` | 0.5040 | 0.5059 | 0.1894 |
| `lu/n256/b4` | 2.1305 | 2.1165 | 0.8525 |
| `lu/n512/b1` | 3.4422 | 2.0719 | 0.8974 |
| `lu/n512/b4` | 13.2779 | 8.1775 | 3.8911 |
| `lu_factor/n256/b1` | 0.3782 | 0.3586 | 0.1523 |
| `lu_factor/n256/b4` | 1.5378 | 1.4553 | 0.6208 |
| `lu_factor/n512/b1` | 2.8294 | 1.5252 | 0.6087 |
| `lu_factor/n512/b4` | 11.7548 | 6.3607 | 2.4392 |
| `lu_factor_solve/n256/b1` | 0.3703 | 0.3886 | 0.1864 |
| `lu_factor_solve/n256/b4` | 1.4928 | 1.4890 | 0.7732 |
| `lu_factor_solve/n512/b1` | 2.8868 | 1.5895 | 0.7337 |
| `lu_factor_solve/n512/b4` | 12.1504 | 6.5295 | 3.0262 |
| `lu_solve_prepared/n256/b1` | 0.0171 | 0.0287 | 0.0242 |
| `lu_solve_prepared/n256/b4` | 0.0816 | 0.1133 | 0.1297 |
| `lu_solve_prepared/n512/b1` | 0.0727 | 0.0802 | 0.0945 |
| `lu_solve_prepared/n512/b4` | 0.4322 | 0.4028 | 0.6117 |
| `qr/n256/b1` | 1.8539 | 2.4081 | 1.1119 |
| `qr/n256/b4` | 7.3951 | 9.5156 | 4.4970 |
| `qr/n512/b1` | 11.4863 | 6.7530 | 5.2750 |
| `qr/n512/b4` | 46.1695 | 26.6293 | 21.5114 |
| `rank_revealing_qr/n256/b1` | 2.1152 | 1.5488 | 2.2103 |
| `rank_revealing_qr/n256/b4` | 8.4587 | 6.0827 | 8.8766 |
| `rank_revealing_qr/n512/b1` | 14.9878 | 5.6885 | 14.8909 |
| `rank_revealing_qr/n512/b4` | 60.1524 | 23.1895 | 59.8703 |
| `solve/n256/b1` | 0.3939 | 0.4137 | 0.2078 |
| `solve/n256/b4` | 1.5778 | 1.5732 | 0.8452 |
| `solve/n512/b1` | 2.8751 | 1.6590 | 0.7578 |
| `solve/n512/b4` | 11.4450 | 6.5236 | 3.2200 |
| `svd_thin/n256/b1` | 12.2789 | 9.0542 | 7.0870 |
| `svd_thin/n256/b4` | 49.2089 | 35.9609 | 28.4452 |
| `svd_thin/n512/b1` | 71.9082 | 38.5111 | 30.7897 |
| `svd_thin/n512/b4` | 286.2546 | 153.1879 | 123.3862 |
| `svd_values/n256/b1` | 6.9532 | 7.2327 | 3.6435 |
| `svd_values/n256/b4` | 27.6751 | 28.6557 | 14.6673 |
| `svd_values/n512/b1` | 38.6681 | 32.2510 | 13.5035 |
| `svd_values/n512/b4` | 155.9539 | 128.9456 | 54.2369 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0189 | 0.0151 |
| `triangular_solve/n256/b4` | 0.0461 | 0.0642 | 0.0744 |
| `triangular_solve/n512/b1` | 0.0340 | 0.0431 | 0.0577 |
| `triangular_solve/n512/b4` | 0.1585 | 0.1787 | 0.2744 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7034 | - | 1.0996 |
| `cholesky/n256/b4` | 2.8580 | - | 4.4599 |
| `cholesky/n512/b1` | 4.8752 | - | 7.5984 |
| `cholesky/n512/b4` | 19.6106 | - | 26.2618 |
| `eigh/n256/b1` | 10.2454 | - | 20.8098 |
| `eigh/n256/b4` | 40.9994 | - | 84.4438 |
| `eigh/n512/b1` | 62.7718 | - | 154.6349 |
| `eigh/n512/b4` | 252.1220 | - | 610.4174 |
| `eigvalsh/n256/b1` | 4.9415 | - | 8.1243 |
| `eigvalsh/n256/b4` | 19.8530 | - | 32.5283 |
| `eigvalsh/n512/b1` | 29.4766 | - | 58.0751 |
| `eigvalsh/n512/b4` | 118.4300 | - | 232.5679 |
| `householder_apply/n256/b1` | 3.3763 | - | 6.3450 |
| `householder_apply/n256/b4` | 13.6071 | - | 24.6559 |
| `householder_apply/n512/b1` | 24.6813 | - | 36.8958 |
| `householder_apply/n512/b4` | 99.2673 | - | 151.9201 |
| `householder_factor/n256/b1` | 2.3390 | - | 3.2922 |
| `householder_factor/n256/b4` | 9.3524 | - | 13.2638 |
| `householder_factor/n512/b1` | 16.7044 | - | 22.7084 |
| `householder_factor/n512/b4` | 67.0081 | - | 92.1425 |
| `lu/n256/b1` | 1.2716 | - | 1.6138 |
| `lu/n256/b4` | 5.1885 | - | 6.7828 |
| `lu/n512/b1` | 8.6836 | - | 11.1388 |
| `lu/n512/b4` | 34.5818 | - | 44.6181 |
| `lu_factor/n256/b1` | 1.1256 | - | 1.5372 |
| `lu_factor/n256/b4` | 4.5063 | - | 6.2641 |
| `lu_factor/n512/b1` | 8.0397 | - | 10.3429 |
| `lu_factor/n512/b4` | 32.6869 | - | 42.2220 |
| `lu_factor_solve/n256/b1` | 1.1903 | - | 1.6536 |
| `lu_factor_solve/n256/b4` | 4.7648 | - | 6.8074 |
| `lu_factor_solve/n512/b1` | 8.2541 | - | 10.7389 |
| `lu_factor_solve/n512/b4` | 33.8168 | - | 43.2976 |
| `lu_solve_prepared/n256/b1` | 0.0620 | - | 0.1150 |
| `lu_solve_prepared/n256/b4` | 0.2645 | - | 0.5247 |
| `lu_solve_prepared/n512/b1` | 0.2197 | - | 0.4137 |
| `lu_solve_prepared/n512/b4` | 1.0733 | - | 2.1177 |
| `qr/n256/b1` | 6.2326 | - | 7.2407 |
| `qr/n256/b4` | 24.9520 | - | 28.9809 |
| `qr/n512/b1` | 42.4502 | - | 47.3489 |
| `qr/n512/b4` | 169.0225 | - | 192.1076 |
| `rank_revealing_qr/n256/b1` | 6.7072 | - | 10.1837 |
| `rank_revealing_qr/n256/b4` | 27.1385 | - | 41.0237 |
| `rank_revealing_qr/n512/b1` | 47.7032 | - | 64.7961 |
| `rank_revealing_qr/n512/b4` | 189.8421 | - | 260.4228 |
| `solve/n256/b1` | 1.1815 | - | 1.7252 |
| `solve/n256/b4` | 4.7053 | - | 6.7624 |
| `solve/n512/b1` | 8.2232 | - | 11.1981 |
| `solve/n512/b4` | 32.7302 | - | 43.7563 |
| `svd_thin/n256/b1` | 24.4334 | - | 27.3609 |
| `svd_thin/n256/b4` | 98.1190 | - | 111.4721 |
| `svd_thin/n512/b1` | 154.7902 | - | 189.3031 |
| `svd_thin/n512/b4` | 618.5348 | - | 747.6142 |
| `svd_values/n256/b1` | 11.4695 | - | 11.8836 |
| `svd_values/n256/b4` | 45.8915 | - | 49.3195 |
| `svd_values/n512/b1` | 67.8957 | - | 90.1184 |
| `svd_values/n512/b4` | 271.9834 | - | 373.5654 |
| `triangular_solve/n256/b1` | 0.0342 | - | 0.0639 |
| `triangular_solve/n256/b4` | 0.1480 | - | 0.2642 |
| `triangular_solve/n512/b1` | 0.1160 | - | 0.2425 |
| `triangular_solve/n512/b4` | 0.6152 | - | 1.0286 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7035 | 0.4971 | 0.3815 |
| `cholesky/n256/b4` | 2.7784 | 1.9902 | 1.3852 |
| `cholesky/n512/b1` | 4.7359 | 2.4596 | 1.9186 |
| `cholesky/n512/b4` | 19.6368 | 10.3629 | 9.2127 |
| `eigh/n256/b1` | 10.2506 | 7.7145 | 9.5679 |
| `eigh/n256/b4` | 41.1387 | 31.9058 | 38.4392 |
| `eigh/n512/b1` | 62.9251 | 28.9661 | 54.4427 |
| `eigh/n512/b4` | 251.7898 | 116.9089 | 218.2885 |
| `eigvalsh/n256/b1` | 4.9774 | 4.9883 | 3.9432 |
| `eigvalsh/n256/b4` | 19.7692 | 19.7934 | 15.8739 |
| `eigvalsh/n512/b1` | 29.4740 | 19.7288 | 21.4767 |
| `eigvalsh/n512/b4` | 118.4181 | 79.9369 | 86.1416 |
| `householder_apply/n256/b1` | 3.3679 | 0.9780 | 1.6238 |
| `householder_apply/n256/b4` | 13.6253 | 3.9595 | 6.8529 |
| `householder_apply/n512/b1` | 24.6283 | 6.4411 | 9.7993 |
| `householder_apply/n512/b4` | 99.2311 | 26.3753 | 39.3207 |
| `householder_factor/n256/b1` | 2.3468 | 0.9151 | 0.9456 |
| `householder_factor/n256/b4` | 9.4181 | 3.6547 | 3.8008 |
| `householder_factor/n512/b1` | 16.7354 | 5.1892 | 6.7920 |
| `householder_factor/n512/b4` | 67.0997 | 20.8239 | 26.9686 |
| `lu/n256/b1` | 1.2709 | 0.8505 | 0.5235 |
| `lu/n256/b4` | 5.1785 | 3.4646 | 2.4534 |
| `lu/n512/b1` | 8.7213 | 3.8977 | 3.8087 |
| `lu/n512/b4` | 34.7377 | 15.6165 | 14.6284 |
| `lu_factor/n256/b1` | 1.1180 | 0.6698 | 0.4346 |
| `lu_factor/n256/b4` | 4.3579 | 1.5149 | 1.6712 |
| `lu_factor/n512/b1` | 8.0114 | 3.1013 | 3.0221 |
| `lu_factor/n512/b4` | 32.7790 | 9.0978 | 12.1401 |
| `lu_factor_solve/n256/b1` | 1.1768 | 0.7307 | 0.4909 |
| `lu_factor_solve/n256/b4` | 4.5963 | 1.1939 | 1.9137 |
| `lu_factor_solve/n512/b1` | 8.2149 | 3.2919 | 3.2495 |
| `lu_factor_solve/n512/b4` | 33.6149 | 9.4874 | 13.1151 |
| `lu_solve_prepared/n256/b1` | 0.0631 | 0.0604 | 0.0523 |
| `lu_solve_prepared/n256/b4` | 0.2619 | 0.1346 | 0.2179 |
| `lu_solve_prepared/n512/b1` | 0.2084 | 0.1588 | 0.2028 |
| `lu_solve_prepared/n512/b4` | 1.0937 | 0.3302 | 1.2175 |
| `qr/n256/b1` | 6.2384 | 3.0759 | 2.8244 |
| `qr/n256/b4` | 24.8378 | 12.3878 | 11.3886 |
| `qr/n512/b1` | 42.4100 | 14.3780 | 16.7052 |
| `qr/n512/b4` | 169.9921 | 58.0413 | 68.6473 |
| `rank_revealing_qr/n256/b1` | 6.7556 | 3.7130 | 7.7822 |
| `rank_revealing_qr/n256/b4` | 27.0177 | 15.8768 | 31.6297 |
| `rank_revealing_qr/n512/b1` | 47.6704 | 16.6325 | 45.3594 |
| `rank_revealing_qr/n512/b4` | 191.7955 | 65.6150 | 182.2436 |
| `solve/n256/b1` | 1.1800 | 0.7529 | 0.5280 |
| `solve/n256/b4` | 4.7333 | 3.0548 | 2.1814 |
| `solve/n512/b1` | 8.2101 | 3.3694 | 3.2723 |
| `solve/n512/b4` | 32.7341 | 13.3441 | 13.8133 |
| `svd_thin/n256/b1` | 24.5035 | 15.6982 | 12.9495 |
| `svd_thin/n256/b4` | 98.8280 | 63.7108 | 54.3717 |
| `svd_thin/n512/b1` | 155.0057 | 68.6089 | 70.4830 |
| `svd_thin/n512/b4` | 619.6852 | 272.3232 | 300.8762 |
| `svd_values/n256/b1` | 11.4772 | 11.2934 | 7.1527 |
| `svd_values/n256/b4` | 45.9845 | 45.1606 | 28.5475 |
| `svd_values/n512/b1` | 68.1342 | 42.7267 | 33.4006 |
| `svd_values/n512/b4` | 272.2810 | 170.6769 | 153.8017 |
| `triangular_solve/n256/b1` | 0.0338 | 0.0339 | 0.0263 |
| `triangular_solve/n256/b4` | 0.1376 | 0.1285 | 0.1118 |
| `triangular_solve/n512/b1` | 0.1134 | 0.0840 | 0.0995 |
| `triangular_solve/n512/b4` | 0.5126 | 0.3758 | 0.6014 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6855 | 0.4732 | 0.2670 |
| `cholesky/n256/b4` | 2.8547 | 2.0494 | 1.1585 |
| `cholesky/n512/b1` | 4.6420 | 1.8398 | 1.0960 |
| `cholesky/n512/b4` | 19.6185 | 7.7411 | 5.3869 |
| `eigh/n256/b1` | 10.2505 | 6.9516 | 7.8453 |
| `eigh/n256/b4` | 41.2616 | 28.9332 | 31.9319 |
| `eigh/n512/b1` | 63.1849 | 23.8400 | 39.2476 |
| `eigh/n512/b4` | 253.5745 | 96.3373 | 160.9235 |
| `eigvalsh/n256/b1` | 4.9502 | 4.9869 | 3.5662 |
| `eigvalsh/n256/b4` | 19.8319 | 19.7773 | 14.3412 |
| `eigvalsh/n512/b1` | 29.6895 | 17.8656 | 17.4518 |
| `eigvalsh/n512/b4` | 119.2602 | 71.8210 | 69.8179 |
| `householder_apply/n256/b1` | 3.4092 | 0.8481 | 0.8677 |
| `householder_apply/n256/b4` | 13.4554 | 3.4144 | 3.5950 |
| `householder_apply/n512/b1` | 24.8847 | 4.3540 | 5.0495 |
| `householder_apply/n512/b4` | 98.9930 | 17.1198 | 20.4807 |
| `householder_factor/n256/b1` | 2.3365 | 0.9165 | 0.9574 |
| `householder_factor/n256/b4` | 9.3824 | 3.7294 | 3.8441 |
| `householder_factor/n512/b1` | 16.8343 | 4.1658 | 3.4138 |
| `householder_factor/n512/b4` | 66.2497 | 16.6726 | 13.3425 |
| `lu/n256/b1` | 1.2706 | 0.8411 | 0.4118 |
| `lu/n256/b4` | 5.2006 | 3.4573 | 1.8547 |
| `lu/n512/b1` | 8.6925 | 3.3775 | 2.3983 |
| `lu/n512/b4` | 34.7787 | 13.2238 | 9.6430 |
| `lu_factor/n256/b1` | 1.1131 | 0.6612 | 0.2909 |
| `lu_factor/n256/b4` | 4.4561 | 2.6906 | 1.1856 |
| `lu_factor/n512/b1` | 7.9922 | 2.5103 | 1.7135 |
| `lu_factor/n512/b4` | 32.7235 | 10.4451 | 6.9649 |
| `lu_factor_solve/n256/b1` | 1.1737 | 0.7277 | 0.3526 |
| `lu_factor_solve/n256/b4` | 4.7862 | 2.9540 | 1.4441 |
| `lu_factor_solve/n512/b1` | 8.2331 | 2.7058 | 1.9459 |
| `lu_factor_solve/n512/b4` | 33.7134 | 11.1830 | 7.9725 |
| `lu_solve_prepared/n256/b1` | 0.0632 | 0.0675 | 0.0523 |
| `lu_solve_prepared/n256/b4` | 0.2719 | 0.2803 | 0.2163 |
| `lu_solve_prepared/n512/b1` | 0.2237 | 0.1698 | 0.2010 |
| `lu_solve_prepared/n512/b4` | 1.2773 | 0.9592 | 1.2642 |
| `qr/n256/b1` | 6.1974 | 3.4209 | 2.2160 |
| `qr/n256/b4` | 24.9026 | 13.7499 | 9.0157 |
| `qr/n512/b1` | 42.2659 | 12.0469 | 9.3127 |
| `qr/n512/b4` | 169.8368 | 49.0098 | 38.6484 |
| `rank_revealing_qr/n256/b1` | 6.7097 | 3.6222 | 6.3868 |
| `rank_revealing_qr/n256/b4` | 26.9927 | 15.1036 | 26.0202 |
| `rank_revealing_qr/n512/b1` | 47.7905 | 11.6399 | 36.7717 |
| `rank_revealing_qr/n512/b4` | 192.3171 | 46.6872 | 147.2573 |
| `solve/n256/b1` | 1.1844 | 0.7581 | 0.3912 |
| `solve/n256/b4` | 4.7038 | 3.0497 | 1.5956 |
| `solve/n512/b1` | 8.2212 | 2.8724 | 2.0021 |
| `solve/n512/b4` | 32.7910 | 11.3575 | 8.4855 |
| `svd_thin/n256/b1` | 24.4993 | 14.7744 | 10.7414 |
| `svd_thin/n256/b4` | 98.3565 | 60.0420 | 43.1163 |
| `svd_thin/n512/b1` | 154.3524 | 56.5704 | 52.6407 |
| `svd_thin/n512/b4` | 617.0177 | 224.1043 | 211.5178 |
| `svd_values/n256/b1` | 11.4586 | 11.1495 | 5.7854 |
| `svd_values/n256/b4` | 45.9194 | 44.6799 | 23.9266 |
| `svd_values/n512/b1` | 67.9108 | 39.8801 | 25.7157 |
| `svd_values/n512/b4` | 272.0569 | 160.1561 | 109.3458 |
| `triangular_solve/n256/b1` | 0.0330 | 0.0369 | 0.0259 |
| `triangular_solve/n256/b4` | 0.1433 | 0.1448 | 0.1172 |
| `triangular_solve/n512/b1` | 0.1134 | 0.0895 | 0.1003 |
| `triangular_solve/n512/b4` | 0.4993 | 0.3906 | 0.6754 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3301 | - | 0.4442 |
| `householder_factor/4096x256/b1` | 14.2459 | - | 17.3611 |
| `qr/1024x64/b1` | 0.9775 | - | 0.9191 |
| `qr/4096x256/b1` | 41.3647 | - | 42.2962 |
| `rank_revealing_qr/1024x64/b1` | 0.9742 | - | 1.2034 |
| `rank_revealing_qr/4096x256/b1` | 64.9076 | - | 60.4049 |
| `svd_thin/1024x64/b1` | 1.4576 | - | 1.6553 |
| `svd_thin/4096x256/b1` | 72.7479 | - | 67.3580 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3310 | 0.2766 | 0.2371 |
| `householder_factor/4096x256/b1` | 14.1853 | 5.9800 | 6.6515 |
| `qr/1024x64/b1` | 0.9861 | 0.8128 | 0.5807 |
| `qr/4096x256/b1` | 41.3936 | 18.2248 | 16.2454 |
| `rank_revealing_qr/1024x64/b1` | 0.9696 | 0.7133 | 1.0231 |
| `rank_revealing_qr/4096x256/b1` | 65.5536 | 22.6945 | 42.8202 |
| `svd_thin/1024x64/b1` | 1.4609 | 1.2775 | 1.0885 |
| `svd_thin/4096x256/b1` | 73.2791 | 33.0900 | 28.9303 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3297 | 0.3162 | 0.1685 |
| `householder_factor/4096x256/b1` | 14.2361 | 4.7643 | 3.7629 |
| `qr/1024x64/b1` | 0.9819 | 0.9747 | 0.4964 |
| `qr/4096x256/b1` | 41.7238 | 15.2019 | 11.5975 |
| `rank_revealing_qr/1024x64/b1` | 0.9666 | 0.6991 | 1.0101 |
| `rank_revealing_qr/4096x256/b1` | 65.2505 | 16.6135 | 38.7940 |
| `svd_thin/1024x64/b1` | 1.4580 | 1.4480 | 0.9956 |
| `svd_thin/4096x256/b1` | 73.4308 | 27.2070 | 22.3061 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0422 | - | 1.3365 |
| `householder_factor/4096x256/b1` | 54.7306 | - | 66.8236 |
| `qr/1024x64/b1` | 2.8504 | - | 2.8573 |
| `qr/4096x256/b1` | 147.9415 | - | 133.8756 |
| `rank_revealing_qr/1024x64/b1` | 2.8606 | - | 3.8434 |
| `rank_revealing_qr/4096x256/b1` | 245.0691 | - | 185.9433 |
| `svd_thin/1024x64/b1` | 3.5398 | - | 4.9251 |
| `svd_thin/4096x256/b1` | 233.0003 | - | 220.3330 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0414 | 0.5652 | 0.7834 |
| `householder_factor/4096x256/b1` | 53.8240 | 18.3964 | 19.1315 |
| `qr/1024x64/b1` | 2.8462 | 1.4980 | 1.7911 |
| `qr/4096x256/b1` | 146.8208 | 52.9351 | 47.3806 |
| `rank_revealing_qr/1024x64/b1` | 2.8589 | 1.5764 | 3.1741 |
| `rank_revealing_qr/4096x256/b1` | 245.1996 | 77.5944 | 131.1118 |
| `svd_thin/1024x64/b1` | 3.5651 | 2.2253 | 3.0335 |
| `svd_thin/4096x256/b1` | 233.4997 | 100.2628 | 82.9739 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0440 | 0.5440 | 0.4821 |
| `householder_factor/4096x256/b1` | 54.3687 | 13.2698 | 11.0986 |
| `qr/1024x64/b1` | 2.8396 | 1.4655 | 1.3402 |
| `qr/4096x256/b1` | 147.2084 | 37.0217 | 30.0004 |
| `rank_revealing_qr/1024x64/b1` | 2.8468 | 1.4185 | 2.9614 |
| `rank_revealing_qr/4096x256/b1` | 246.0536 | 44.9070 | 114.3431 |
| `svd_thin/1024x64/b1` | 3.5208 | 2.1570 | 2.4273 |
| `svd_thin/4096x256/b1` | 232.5781 | 66.1666 | 52.0918 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
