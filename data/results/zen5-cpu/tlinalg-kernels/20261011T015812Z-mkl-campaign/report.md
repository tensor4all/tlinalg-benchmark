# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `b135f0d7e66662716e81cfd7aec2752bc4e605d7`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
- harness commit: `708744f86fe8c3f122e303542707802488cb74d0`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-11T02:53:12.379982Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor mkl --checkout /tmp/tl-mkl --aa 1 --label mkl-campaign`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261011T015812Z-mkl-campaign/`

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
| `cholesky/n16/b1024` | 0.5543 | - | 0.6373 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1068 | - | 0.0732 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2141 | - | 0.1986 |
| `eig/n16/b1` | 0.0566 | - | 0.0340 |
| `eig/n16/b1024` | 60.4684 | - | 36.4943 |
| `eig/n4/b1` | 0.0042 | - | 0.0027 |
| `eig/n4/b1024` | 3.7824 | - | 2.0022 |
| `eig/n8/b1` | 0.0152 | - | 0.0085 |
| `eig/n8/b1024` | 14.5733 | - | 7.8488 |
| `eigh/n16/b1` | 0.0176 | - | 0.0136 |
| `eigh/n16/b1024` | 17.7241 | - | 14.1256 |
| `eigh/n4/b1` | 0.0016 | - | 0.0020 |
| `eigh/n4/b1024` | 1.4390 | - | 1.7244 |
| `eigh/n8/b1` | 0.0052 | - | 0.0049 |
| `eigh/n8/b1024` | 5.0331 | - | 4.6647 |
| `eigvals/n16/b1` | 0.0403 | - | 0.0243 |
| `eigvals/n16/b1024` | 41.9261 | - | 24.7167 |
| `eigvals/n4/b1` | 0.0026 | - | 0.0023 |
| `eigvals/n4/b1024` | 2.1647 | - | 1.5332 |
| `eigvals/n8/b1` | 0.0106 | - | 0.0070 |
| `eigvals/n8/b1024` | 10.0153 | - | 6.1848 |
| `eigvalsh/n16/b1` | 0.0197 | - | 0.0078 |
| `eigvalsh/n16/b1024` | 20.3323 | - | 7.8002 |
| `eigvalsh/n4/b1` | 0.0019 | - | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5532 | - | 0.8881 |
| `eigvalsh/n8/b1` | 0.0058 | - | 0.0029 |
| `eigvalsh/n8/b1024` | 5.3443 | - | 2.6551 |
| `full_piv_lu/n16/b1` | 0.0027 | - | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.0886 | - | 2.4429 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2345 | - | 0.2605 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6376 | - | 0.5909 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | - | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 1.9879 | - | 3.4797 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | - | 0.0010 |
| `full_piv_lu_solve/n4/b1024` | 0.3040 | - | 0.6657 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7070 | - | 1.1616 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0018 |
| `householder_apply/n16/b1024` | 2.5754 | - | 1.6298 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.1778 | - | 0.2026 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0008 |
| `householder_apply/n8/b1024` | 0.6431 | - | 0.4943 |
| `householder_factor/n16/b1` | 0.0021 | - | 0.0018 |
| `householder_factor/n16/b1024` | 2.0665 | - | 1.7781 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0003 |
| `householder_factor/n4/b1024` | 0.2374 | - | 0.1842 |
| `householder_factor/n8/b1` | 0.0007 | - | 0.0006 |
| `householder_factor/n8/b1024` | 0.6691 | - | 0.5029 |
| `lu/n16/b1` | 0.0020 | - | 0.0013 |
| `lu/n16/b1024` | 1.6686 | - | 1.0725 |
| `lu/n4/b1` | 0.0004 | - | 0.0003 |
| `lu/n4/b1024` | 0.1787 | - | 0.1041 |
| `lu/n8/b1` | 0.0007 | - | 0.0005 |
| `lu/n8/b1024` | 0.5127 | - | 0.3043 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0008 |
| `lu_factor/n16/b1024` | 1.1107 | - | 0.7526 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0001 |
| `lu_factor/n4/b1024` | 0.1340 | - | 0.0375 |
| `lu_factor/n8/b1` | 0.0005 | - | 0.0002 |
| `lu_factor/n8/b1024` | 0.3526 | - | 0.1579 |
| `lu_factor_solve/n16/b1` | 0.0017 | - | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4109 | - | 1.4078 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1681 | - | 0.1071 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4857 | - | 0.4910 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3589 | - | 0.6194 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | - | 0.0786 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1365 | - | 0.3491 |
| `qr/n16/b1` | 0.0054 | - | 0.0034 |
| `qr/n16/b1024` | 5.1946 | - | 3.1873 |
| `qr/n4/b1` | 0.0007 | - | 0.0007 |
| `qr/n4/b1024` | 0.4327 | - | 0.4170 |
| `qr/n8/b1` | 0.0016 | - | 0.0013 |
| `qr/n8/b1024` | 1.3958 | - | 1.0184 |
| `rank_revealing_qr/n16/b1` | 0.0065 | - | 0.0054 |
| `rank_revealing_qr/n16/b1024` | 6.1573 | - | 5.0117 |
| `rank_revealing_qr/n4/b1` | 0.0010 | - | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.6877 | - | 0.7178 |
| `rank_revealing_qr/n8/b1` | 0.0022 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8724 | - | 1.7515 |
| `solve/n16/b1` | 0.0021 | - | 0.0018 |
| `solve/n16/b1024` | 1.5738 | - | 1.4636 |
| `solve/n4/b1` | 0.0006 | - | 0.0003 |
| `solve/n4/b1024` | 0.2144 | - | 0.1421 |
| `solve/n8/b1` | 0.0010 | - | 0.0007 |
| `solve/n8/b1024` | 0.5358 | - | 0.5360 |
| `svd_full/n16/b1` | 0.0329 | - | 0.0338 |
| `svd_full/n16/b1024` | 34.7968 | - | 35.6385 |
| `svd_full/n4/b1` | 0.0028 | - | 0.0044 |
| `svd_full/n4/b1024` | 2.4809 | - | 3.9224 |
| `svd_full/n8/b1` | 0.0089 | - | 0.0117 |
| `svd_full/n8/b1024` | 9.0293 | - | 11.9315 |
| `svd_thin/n16/b1` | 0.0325 | - | 0.0338 |
| `svd_thin/n16/b1024` | 33.3675 | - | 35.6866 |
| `svd_thin/n4/b1` | 0.0027 | - | 0.0045 |
| `svd_thin/n4/b1024` | 2.5386 | - | 3.9387 |
| `svd_thin/n8/b1` | 0.0089 | - | 0.0118 |
| `svd_thin/n8/b1024` | 8.9907 | - | 11.9928 |
| `svd_values/n16/b1` | 0.0269 | - | 0.0144 |
| `svd_values/n16/b1024` | 27.9864 | - | 15.2547 |
| `svd_values/n4/b1` | 0.0025 | - | 0.0023 |
| `svd_values/n4/b1024` | 2.1492 | - | 1.8555 |
| `svd_values/n8/b1` | 0.0079 | - | 0.0051 |
| `svd_values/n8/b1024` | 7.5507 | - | 4.8639 |
| `triangular_solve/n16/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3023 | - | 0.3498 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0511 | - | 0.1860 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1296 | - | 0.2356 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0025 | 0.0007 |
| `cholesky/n16/b1024` | 0.5627 | 0.2799 | 0.6475 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1071 | 0.0344 | 0.0719 |
| `cholesky/n8/b1` | 0.0003 | 0.0027 | 0.0003 |
| `cholesky/n8/b1024` | 0.2182 | 0.0593 | 0.1889 |
| `eig/n16/b1` | 0.0568 | 0.0612 | 0.0339 |
| `eig/n16/b1024` | 60.2363 | 18.7037 | 36.6719 |
| `eig/n4/b1` | 0.0043 | 0.0073 | 0.0027 |
| `eig/n4/b1024` | 3.7849 | 1.1694 | 1.9990 |
| `eig/n8/b1` | 0.0152 | 0.0183 | 0.0085 |
| `eig/n8/b1024` | 14.4754 | 4.3193 | 7.8529 |
| `eigh/n16/b1` | 0.0175 | 0.0207 | 0.0136 |
| `eigh/n16/b1024` | 17.7546 | 8.0249 | 14.0982 |
| `eigh/n4/b1` | 0.0016 | 0.0037 | 0.0020 |
| `eigh/n4/b1024` | 1.4213 | 0.3612 | 1.6978 |
| `eigh/n8/b1` | 0.0051 | 0.0075 | 0.0049 |
| `eigh/n8/b1024` | 5.0806 | 2.5594 | 4.6635 |
| `eigvals/n16/b1` | 0.0401 | 0.0433 | 0.0243 |
| `eigvals/n16/b1024` | 41.8172 | 13.1331 | 24.5805 |
| `eigvals/n4/b1` | 0.0027 | 0.0048 | 0.0023 |
| `eigvals/n4/b1024` | 2.1584 | 0.7538 | 1.5411 |
| `eigvals/n8/b1` | 0.0106 | 0.0137 | 0.0070 |
| `eigvals/n8/b1024` | 10.0155 | 3.7345 | 6.1818 |
| `eigvalsh/n16/b1` | 0.0197 | 0.0243 | 0.0078 |
| `eigvalsh/n16/b1024` | 20.4170 | 10.9773 | 7.8686 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0043 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5402 | 0.7087 | 0.8796 |
| `eigvalsh/n8/b1` | 0.0056 | 0.0082 | 0.0029 |
| `eigvalsh/n8/b1024` | 5.3581 | 2.7977 | 2.6397 |
| `full_piv_lu/n16/b1` | 0.0026 | 0.0052 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.0877 | 1.0739 | 2.3746 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2293 | 0.0634 | 0.2635 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0037 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6338 | 0.1928 | 0.5883 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0055 | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0008 | 0.5140 | 3.4787 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0029 | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3069 | 0.1602 | 0.6584 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0036 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7462 | 0.3602 | 1.1567 |
| `householder_apply/n16/b1` | 0.0025 | 0.0045 | 0.0018 |
| `householder_apply/n16/b1024` | 2.5309 | 0.6748 | 1.6261 |
| `householder_apply/n4/b1` | 0.0004 | 0.0026 | 0.0004 |
| `householder_apply/n4/b1024` | 0.1771 | 0.0492 | 0.1937 |
| `householder_apply/n8/b1` | 0.0007 | 0.0032 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6482 | 0.1737 | 0.4740 |
| `householder_factor/n16/b1` | 0.0021 | 0.0042 | 0.0018 |
| `householder_factor/n16/b1024` | 2.0699 | 0.5313 | 1.7664 |
| `householder_factor/n4/b1` | 0.0003 | 0.0026 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2393 | 0.0656 | 0.1839 |
| `householder_factor/n8/b1` | 0.0007 | 0.0033 | 0.0007 |
| `householder_factor/n8/b1024` | 0.6603 | 0.1718 | 0.5036 |
| `lu/n16/b1` | 0.0021 | 0.0045 | 0.0012 |
| `lu/n16/b1024` | 1.7483 | 0.8799 | 1.1154 |
| `lu/n4/b1` | 0.0004 | 0.0028 | 0.0003 |
| `lu/n4/b1024` | 0.1779 | 0.0909 | 0.1019 |
| `lu/n8/b1` | 0.0007 | 0.0036 | 0.0005 |
| `lu/n8/b1024` | 0.5193 | 0.2639 | 0.2938 |
| `lu_factor/n16/b1` | 0.0013 | 0.0036 | 0.0007 |
| `lu_factor/n16/b1024` | 1.1022 | 0.2853 | 0.6985 |
| `lu_factor/n4/b1` | 0.0004 | 0.0021 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1313 | 0.0390 | 0.0393 |
| `lu_factor/n8/b1` | 0.0005 | 0.0029 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3508 | 0.1782 | 0.1560 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0045 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4547 | 0.3693 | 1.4414 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0020 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1668 | 0.0516 | 0.1082 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0034 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4760 | 0.1252 | 0.4941 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0022 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3579 | 0.1048 | 0.6232 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0028 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0401 | 0.0205 | 0.0791 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0023 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1364 | 0.0456 | 0.3532 |
| `qr/n16/b1` | 0.0055 | 0.0087 | 0.0034 |
| `qr/n16/b1024` | 5.2933 | 2.6521 | 3.1562 |
| `qr/n4/b1` | 0.0008 | 0.0024 | 0.0007 |
| `qr/n4/b1024` | 0.4344 | 0.2240 | 0.4332 |
| `qr/n8/b1` | 0.0016 | 0.0039 | 0.0013 |
| `qr/n8/b1024` | 1.3721 | 0.7062 | 1.0213 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0094 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 5.9343 | 3.0075 | 4.9466 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0035 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.6817 | 0.3475 | 0.7240 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0044 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8259 | 0.9199 | 1.7386 |
| `solve/n16/b1` | 0.0021 | 0.0046 | 0.0019 |
| `solve/n16/b1024` | 1.5647 | 0.4007 | 1.4827 |
| `solve/n4/b1` | 0.0006 | 0.0028 | 0.0003 |
| `solve/n4/b1024` | 0.2168 | 0.0606 | 0.1421 |
| `solve/n8/b1` | 0.0010 | 0.0036 | 0.0007 |
| `solve/n8/b1024` | 0.5424 | 0.1432 | 0.5339 |
| `svd_full/n16/b1` | 0.0327 | 0.0371 | 0.0336 |
| `svd_full/n16/b1024` | 33.2539 | 9.4948 | 35.6267 |
| `svd_full/n4/b1` | 0.0027 | 0.0042 | 0.0044 |
| `svd_full/n4/b1024` | 2.4726 | 0.6336 | 3.9081 |
| `svd_full/n8/b1` | 0.0090 | 0.0116 | 0.0118 |
| `svd_full/n8/b1024` | 8.9577 | 2.2622 | 11.9066 |
| `svd_thin/n16/b1` | 0.0324 | 0.0354 | 0.0339 |
| `svd_thin/n16/b1024` | 33.4098 | 11.7265 | 35.7350 |
| `svd_thin/n4/b1` | 0.0028 | 0.0050 | 0.0044 |
| `svd_thin/n4/b1024` | 2.4927 | 1.2732 | 3.9143 |
| `svd_thin/n8/b1` | 0.0090 | 0.0113 | 0.0117 |
| `svd_thin/n8/b1024` | 8.9846 | 4.5469 | 11.9639 |
| `svd_values/n16/b1` | 0.0267 | 0.0299 | 0.0144 |
| `svd_values/n16/b1024` | 28.0537 | 10.9542 | 15.3550 |
| `svd_values/n4/b1` | 0.0025 | 0.0051 | 0.0023 |
| `svd_values/n4/b1024` | 2.1517 | 1.1874 | 1.8451 |
| `svd_values/n8/b1` | 0.0077 | 0.0105 | 0.0051 |
| `svd_values/n8/b1024` | 7.6144 | 2.9911 | 4.8287 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0027 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3015 | 0.1557 | 0.3606 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0511 | 0.0293 | 0.1943 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0029 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1314 | 0.0380 | 0.2467 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0024 | 0.0007 |
| `cholesky/n16/b1024` | 0.5467 | 0.1412 | 0.6429 |
| `cholesky/n4/b1` | 0.0002 | 0.0025 | 0.0002 |
| `cholesky/n4/b1024` | 0.1064 | 0.0219 | 0.0702 |
| `cholesky/n8/b1` | 0.0003 | 0.0034 | 0.0003 |
| `cholesky/n8/b1024` | 0.2219 | 0.0583 | 0.1896 |
| `eig/n16/b1` | 0.0562 | 0.0619 | 0.0338 |
| `eig/n16/b1024` | 60.3114 | 11.7039 | 36.6279 |
| `eig/n4/b1` | 0.0042 | 0.0069 | 0.0027 |
| `eig/n4/b1024` | 3.7811 | 1.1626 | 1.9949 |
| `eig/n8/b1` | 0.0151 | 0.0179 | 0.0085 |
| `eig/n8/b1024` | 14.5190 | 2.9807 | 7.8489 |
| `eigh/n16/b1` | 0.0176 | 0.0205 | 0.0136 |
| `eigh/n16/b1024` | 17.7797 | 2.2497 | 14.1086 |
| `eigh/n4/b1` | 0.0016 | 0.0047 | 0.0020 |
| `eigh/n4/b1024` | 1.4317 | 0.1868 | 1.7006 |
| `eigh/n8/b1` | 0.0051 | 0.0083 | 0.0049 |
| `eigh/n8/b1024` | 5.0120 | 1.2719 | 4.6403 |
| `eigvals/n16/b1` | 0.0404 | 0.0431 | 0.0242 |
| `eigvals/n16/b1024` | 41.8001 | 8.1634 | 24.7033 |
| `eigvals/n4/b1` | 0.0026 | 0.0060 | 0.0023 |
| `eigvals/n4/b1024` | 2.1670 | 0.7596 | 1.5246 |
| `eigvals/n8/b1` | 0.0106 | 0.0137 | 0.0070 |
| `eigvals/n8/b1024` | 9.9729 | 2.4063 | 6.1792 |
| `eigvalsh/n16/b1` | 0.0197 | 0.0232 | 0.0077 |
| `eigvalsh/n16/b1024` | 20.2571 | 9.9361 | 7.8125 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0053 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5500 | 0.7037 | 0.8801 |
| `eigvalsh/n8/b1` | 0.0057 | 0.0089 | 0.0029 |
| `eigvalsh/n8/b1024` | 5.3501 | 2.1851 | 2.6442 |
| `full_piv_lu/n16/b1` | 0.0027 | 0.0056 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.1057 | 0.2853 | 2.4511 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0043 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2293 | 0.0767 | 0.2631 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0041 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6661 | 0.0894 | 0.5870 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0057 | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 1.9703 | 0.5080 | 3.4814 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0040 | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3031 | 0.0830 | 0.6541 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0047 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7050 | 0.1803 | 1.1525 |
| `householder_apply/n16/b1` | 0.0026 | 0.0055 | 0.0018 |
| `householder_apply/n16/b1024` | 2.5097 | 0.3376 | 1.6211 |
| `householder_apply/n4/b1` | 0.0004 | 0.0038 | 0.0004 |
| `householder_apply/n4/b1024` | 0.1793 | 0.0291 | 0.1934 |
| `householder_apply/n8/b1` | 0.0007 | 0.0034 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6465 | 0.1649 | 0.4753 |
| `householder_factor/n16/b1` | 0.0021 | 0.0050 | 0.0018 |
| `householder_factor/n16/b1024` | 2.0614 | 0.5204 | 1.7746 |
| `householder_factor/n4/b1` | 0.0003 | 0.0023 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2418 | 0.0658 | 0.1829 |
| `householder_factor/n8/b1` | 0.0007 | 0.0037 | 0.0006 |
| `householder_factor/n8/b1024` | 0.6705 | 0.0898 | 0.5030 |
| `lu/n16/b1` | 0.0020 | 0.0056 | 0.0012 |
| `lu/n16/b1024` | 1.6873 | 0.4245 | 1.1400 |
| `lu/n4/b1` | 0.0004 | 0.0034 | 0.0003 |
| `lu/n4/b1024` | 0.1769 | 0.0494 | 0.1022 |
| `lu/n8/b1` | 0.0007 | 0.0037 | 0.0004 |
| `lu/n8/b1024` | 0.5172 | 0.1375 | 0.2890 |
| `lu_factor/n16/b1` | 0.0013 | 0.0050 | 0.0007 |
| `lu_factor/n16/b1024` | 1.1121 | 0.2872 | 0.7302 |
| `lu_factor/n4/b1` | 0.0003 | 0.0024 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1343 | 0.0250 | 0.0376 |
| `lu_factor/n8/b1` | 0.0006 | 0.0038 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3510 | 0.0941 | 0.1588 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0050 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4378 | 0.3671 | 1.4451 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0039 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1689 | 0.0330 | 0.1069 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0024 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4653 | 0.1294 | 0.4948 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0029 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3631 | 0.1059 | 0.6416 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0037 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0400 | 0.0191 | 0.0786 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0043 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1422 | 0.0328 | 0.3512 |
| `qr/n16/b1` | 0.0056 | 0.0081 | 0.0034 |
| `qr/n16/b1024` | 5.3391 | 0.6714 | 3.1531 |
| `qr/n4/b1` | 0.0008 | 0.0043 | 0.0007 |
| `qr/n4/b1024` | 0.4419 | 0.0597 | 0.4065 |
| `qr/n8/b1` | 0.0016 | 0.0046 | 0.0013 |
| `qr/n8/b1024` | 1.3593 | 0.3455 | 1.0010 |
| `rank_revealing_qr/n16/b1` | 0.0064 | 0.0098 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.0537 | 1.5194 | 4.9554 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0036 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.6906 | 0.0919 | 0.7095 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0054 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8617 | 0.4613 | 1.7203 |
| `solve/n16/b1` | 0.0022 | 0.0053 | 0.0018 |
| `solve/n16/b1024` | 1.6005 | 0.3961 | 1.5418 |
| `solve/n4/b1` | 0.0006 | 0.0030 | 0.0003 |
| `solve/n4/b1024` | 0.2184 | 0.0614 | 0.1418 |
| `solve/n8/b1` | 0.0010 | 0.0043 | 0.0007 |
| `solve/n8/b1024` | 0.5358 | 0.1402 | 0.5343 |
| `svd_full/n16/b1` | 0.0325 | 0.0365 | 0.0339 |
| `svd_full/n16/b1024` | 33.1678 | 7.5660 | 35.7840 |
| `svd_full/n4/b1` | 0.0027 | 0.0059 | 0.0044 |
| `svd_full/n4/b1024` | 2.4923 | 0.6328 | 3.8848 |
| `svd_full/n8/b1` | 0.0089 | 0.0115 | 0.0117 |
| `svd_full/n8/b1024` | 9.4610 | 1.1656 | 11.9179 |
| `svd_thin/n16/b1` | 0.0324 | 0.0362 | 0.0338 |
| `svd_thin/n16/b1024` | 33.2025 | 4.2792 | 35.6914 |
| `svd_thin/n4/b1` | 0.0027 | 0.0056 | 0.0044 |
| `svd_thin/n4/b1024` | 2.4693 | 0.6257 | 3.8976 |
| `svd_thin/n8/b1` | 0.0089 | 0.0114 | 0.0118 |
| `svd_thin/n8/b1024` | 9.0191 | 1.6886 | 11.9291 |
| `svd_values/n16/b1` | 0.0268 | 0.0300 | 0.0145 |
| `svd_values/n16/b1024` | 27.9543 | 7.9064 | 15.1908 |
| `svd_values/n4/b1` | 0.0025 | 0.0056 | 0.0023 |
| `svd_values/n4/b1024` | 2.1686 | 0.7656 | 1.8518 |
| `svd_values/n8/b1` | 0.0077 | 0.0183 | 0.0051 |
| `svd_values/n8/b1024` | 7.5698 | 1.7301 | 4.8735 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0035 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.2981 | 0.0491 | 0.3674 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0024 | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0511 | 0.0151 | 0.1934 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0033 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1316 | 0.0368 | 0.2446 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0011 |
| `cholesky/n16/b1024` | 0.7914 | - | 1.0748 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1201 | - | 0.1082 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2737 | - | 0.2831 |
| `eig/n16/b1` | 0.0759 | - | 0.1037 |
| `eig/n16/b1024` | 81.7504 | - | 111.9759 |
| `eig/n4/b1` | 0.0067 | - | 0.0085 |
| `eig/n4/b1024` | 6.1593 | - | 7.7807 |
| `eig/n8/b1` | 0.0212 | - | 0.0265 |
| `eig/n8/b1024` | 21.5516 | - | 27.0676 |
| `eigh/n16/b1` | 0.0180 | - | 0.0185 |
| `eigh/n16/b1024` | 19.6113 | - | 19.3820 |
| `eigh/n4/b1` | 0.0019 | - | 0.0019 |
| `eigh/n4/b1024` | 1.7177 | - | 1.6949 |
| `eigh/n8/b1` | 0.0057 | - | 0.0054 |
| `eigh/n8/b1024` | 5.4041 | - | 5.3579 |
| `eigvals/n16/b1` | 0.0470 | - | 0.0724 |
| `eigvals/n16/b1024` | 51.8497 | - | 80.6613 |
| `eigvals/n4/b1` | 0.0036 | - | 0.0068 |
| `eigvals/n4/b1024` | 3.2138 | - | 6.0825 |
| `eigvals/n8/b1` | 0.0128 | - | 0.0211 |
| `eigvals/n8/b1024` | 12.8696 | - | 21.6794 |
| `eigvalsh/n16/b1` | 0.0206 | - | 0.0109 |
| `eigvalsh/n16/b1024` | 23.4129 | - | 11.0237 |
| `eigvalsh/n4/b1` | 0.0022 | - | 0.0014 |
| `eigvalsh/n4/b1024` | 1.8715 | - | 1.0854 |
| `eigvalsh/n8/b1` | 0.0063 | - | 0.0036 |
| `eigvalsh/n8/b1024` | 5.8436 | - | 3.3564 |
| `full_piv_lu/n16/b1` | 0.0031 | - | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.8345 | - | 3.6293 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2851 | - | 0.3176 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7621 | - | 0.7403 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | - | 0.0054 |
| `full_piv_lu_solve/n16/b1024` | 3.1388 | - | 5.1423 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4568 | - | 0.9544 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1567 | - | 1.9057 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0035 |
| `householder_apply/n16/b1024` | 3.2736 | - | 4.0737 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.1788 | - | 0.2586 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0010 |
| `householder_apply/n8/b1024` | 0.6259 | - | 0.7542 |
| `householder_factor/n16/b1` | 0.0025 | - | 0.0037 |
| `householder_factor/n16/b1024` | 2.5696 | - | 3.7651 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.3094 | - | 0.3101 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.8209 | - | 0.8895 |
| `lu/n16/b1` | 0.0022 | - | 0.0022 |
| `lu/n16/b1024` | 1.8309 | - | 2.1674 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.2135 | - | 0.1834 |
| `lu/n8/b1` | 0.0008 | - | 0.0007 |
| `lu/n8/b1024` | 0.5476 | - | 0.5302 |
| `lu_factor/n16/b1` | 0.0014 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.1944 | - | 1.5776 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1610 | - | 0.1102 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3849 | - | 0.3702 |
| `lu_factor_solve/n16/b1` | 0.0024 | - | 0.0031 |
| `lu_factor_solve/n16/b1024` | 2.0063 | - | 3.1889 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2496 | - | 0.2491 |
| `lu_factor_solve/n8/b1` | 0.0009 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6914 | - | 0.9969 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7795 | - | 1.5587 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0974 | - | 0.1450 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2882 | - | 0.6420 |
| `qr/n16/b1` | 0.0068 | - | 0.0064 |
| `qr/n16/b1024` | 6.6638 | - | 6.4307 |
| `qr/n4/b1` | 0.0007 | - | 0.0009 |
| `qr/n4/b1024` | 0.5135 | - | 0.5886 |
| `qr/n8/b1` | 0.0018 | - | 0.0019 |
| `qr/n8/b1024` | 1.5678 | - | 1.6032 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0094 |
| `rank_revealing_qr/n16/b1024` | 7.3046 | - | 9.5977 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8266 | - | 1.0911 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1781 | - | 2.8672 |
| `solve/n16/b1` | 0.0029 | - | 0.0036 |
| `solve/n16/b1024` | 2.1583 | - | 3.3018 |
| `solve/n4/b1` | 0.0007 | - | 0.0005 |
| `solve/n4/b1024` | 0.3093 | - | 0.2889 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7572 | - | 1.0490 |
| `svd_full/n16/b1` | 0.0348 | - | 0.0437 |
| `svd_full/n16/b1024` | 36.6300 | - | 48.8048 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_full/n4/b1024` | 3.0069 | - | 4.8076 |
| `svd_full/n8/b1` | 0.0097 | - | 0.0140 |
| `svd_full/n8/b1024` | 10.0572 | - | 14.4305 |
| `svd_thin/n16/b1` | 0.0347 | - | 0.0432 |
| `svd_thin/n16/b1024` | 36.4597 | - | 48.3490 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_thin/n4/b1024` | 2.9849 | - | 4.8044 |
| `svd_thin/n8/b1` | 0.0097 | - | 0.0141 |
| `svd_thin/n8/b1024` | 10.0501 | - | 14.3492 |
| `svd_values/n16/b1` | 0.0297 | - | 0.0205 |
| `svd_values/n16/b1024` | 32.8682 | - | 22.5528 |
| `svd_values/n4/b1` | 0.0029 | - | 0.0029 |
| `svd_values/n4/b1024` | 2.6475 | - | 2.4285 |
| `svd_values/n8/b1` | 0.0087 | - | 0.0067 |
| `svd_values/n8/b1024` | 8.7790 | - | 6.5081 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5995 | - | 0.8286 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0967 | - | 0.1796 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2374 | - | 0.3448 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0024 | 0.0011 |
| `cholesky/n16/b1024` | 0.7874 | 0.3999 | 1.1061 |
| `cholesky/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1180 | 0.0630 | 0.1067 |
| `cholesky/n8/b1` | 0.0004 | 0.0020 | 0.0004 |
| `cholesky/n8/b1024` | 0.2597 | 0.0692 | 0.2819 |
| `eig/n16/b1` | 0.0755 | 0.0808 | 0.0990 |
| `eig/n16/b1024` | 81.3096 | 24.6646 | 107.2522 |
| `eig/n4/b1` | 0.0064 | 0.0090 | 0.0085 |
| `eig/n4/b1024` | 6.0996 | 3.6054 | 7.7958 |
| `eig/n8/b1` | 0.0210 | 0.0242 | 0.0264 |
| `eig/n8/b1024` | 21.3005 | 6.8106 | 26.9607 |
| `eigh/n16/b1` | 0.0180 | 0.0212 | 0.0187 |
| `eigh/n16/b1024` | 19.4148 | 7.9689 | 19.4723 |
| `eigh/n4/b1` | 0.0019 | 0.0037 | 0.0019 |
| `eigh/n4/b1024` | 1.7124 | 0.8680 | 1.6902 |
| `eigh/n8/b1` | 0.0057 | 0.0073 | 0.0054 |
| `eigh/n8/b1024` | 5.4109 | 2.2244 | 5.3759 |
| `eigvals/n16/b1` | 0.0469 | 0.0505 | 0.0724 |
| `eigvals/n16/b1024` | 51.8520 | 17.9397 | 80.5837 |
| `eigvals/n4/b1` | 0.0036 | 0.0059 | 0.0068 |
| `eigvals/n4/b1024` | 3.1546 | 2.0974 | 6.0763 |
| `eigvals/n8/b1` | 0.0127 | 0.0160 | 0.0210 |
| `eigvals/n8/b1024` | 12.8030 | 4.9343 | 21.6383 |
| `eigvalsh/n16/b1` | 0.0207 | 0.0258 | 0.0110 |
| `eigvalsh/n16/b1024` | 23.3733 | 13.0188 | 11.0806 |
| `eigvalsh/n4/b1` | 0.0023 | 0.0046 | 0.0014 |
| `eigvalsh/n4/b1024` | 1.8621 | 1.1875 | 1.0784 |
| `eigvalsh/n8/b1` | 0.0063 | 0.0081 | 0.0036 |
| `eigvalsh/n8/b1024` | 5.8050 | 3.1719 | 3.3599 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0062 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.7626 | 1.3932 | 3.5844 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0024 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2712 | 0.0740 | 0.3230 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0036 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7344 | 0.3552 | 0.7594 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0071 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1552 | 0.8001 | 5.0428 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0035 | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4570 | 0.2368 | 0.9546 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0045 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1345 | 0.3039 | 1.8832 |
| `householder_apply/n16/b1` | 0.0026 | 0.0056 | 0.0036 |
| `householder_apply/n16/b1024` | 3.1576 | 1.5951 | 3.8861 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1783 | 0.0536 | 0.2509 |
| `householder_apply/n8/b1` | 0.0007 | 0.0035 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6211 | 0.3023 | 0.7561 |
| `householder_factor/n16/b1` | 0.0025 | 0.0049 | 0.0038 |
| `householder_factor/n16/b1024` | 2.5702 | 1.2524 | 3.7579 |
| `householder_factor/n4/b1` | 0.0004 | 0.0026 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3046 | 0.0856 | 0.3094 |
| `householder_factor/n8/b1` | 0.0009 | 0.0034 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8093 | 0.2076 | 0.8886 |
| `lu/n16/b1` | 0.0023 | 0.0048 | 0.0022 |
| `lu/n16/b1024` | 1.9181 | 0.9417 | 2.1465 |
| `lu/n4/b1` | 0.0005 | 0.0021 | 0.0004 |
| `lu/n4/b1024` | 0.2071 | 0.0594 | 0.1820 |
| `lu/n8/b1` | 0.0008 | 0.0034 | 0.0008 |
| `lu/n8/b1024` | 0.5414 | 0.2805 | 0.5228 |
| `lu_factor/n16/b1` | 0.0014 | 0.0037 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2502 | 0.5573 | 1.5853 |
| `lu_factor/n4/b1` | 0.0004 | 0.0021 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1717 | 0.0455 | 0.1100 |
| `lu_factor/n8/b1` | 0.0006 | 0.0031 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3962 | 0.1025 | 0.3709 |
| `lu_factor_solve/n16/b1` | 0.0025 | 0.0050 | 0.0031 |
| `lu_factor_solve/n16/b1024` | 2.0251 | 1.0310 | 3.1798 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0021 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2514 | 0.0686 | 0.2503 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0035 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6876 | 0.3508 | 0.9979 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0036 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7984 | 0.2214 | 1.5830 |
| `lu_solve_prepared/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0991 | 0.0351 | 0.1455 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0027 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2872 | 0.0837 | 0.6434 |
| `qr/n16/b1` | 0.0067 | 0.0084 | 0.0064 |
| `qr/n16/b1024` | 6.5354 | 3.3294 | 6.3735 |
| `qr/n4/b1` | 0.0007 | 0.0024 | 0.0009 |
| `qr/n4/b1024` | 0.5093 | 0.1327 | 0.5857 |
| `qr/n8/b1` | 0.0019 | 0.0047 | 0.0019 |
| `qr/n8/b1024` | 1.5680 | 0.7899 | 1.6133 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0102 | 0.0094 |
| `rank_revealing_qr/n16/b1024` | 7.2803 | 1.8624 | 9.5460 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0038 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8183 | 0.4191 | 1.0789 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0049 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1590 | 1.0883 | 2.8700 |
| `solve/n16/b1` | 0.0029 | 0.0061 | 0.0036 |
| `solve/n16/b1024` | 2.1389 | 1.0682 | 3.3244 |
| `solve/n4/b1` | 0.0007 | 0.0024 | 0.0005 |
| `solve/n4/b1024` | 0.3107 | 0.1627 | 0.2857 |
| `solve/n8/b1` | 0.0012 | 0.0037 | 0.0012 |
| `solve/n8/b1024` | 0.7686 | 0.1980 | 1.0592 |
| `svd_full/n16/b1` | 0.0365 | 0.0378 | 0.0433 |
| `svd_full/n16/b1024` | 36.3248 | 14.7571 | 48.2580 |
| `svd_full/n4/b1` | 0.0031 | 0.0059 | 0.0053 |
| `svd_full/n4/b1024` | 2.9849 | 1.2715 | 4.7689 |
| `svd_full/n8/b1` | 0.0097 | 0.0126 | 0.0141 |
| `svd_full/n8/b1024` | 10.0395 | 3.6428 | 14.3429 |
| `svd_thin/n16/b1` | 0.0347 | 0.0379 | 0.0434 |
| `svd_thin/n16/b1024` | 36.4641 | 9.8027 | 48.3687 |
| `svd_thin/n4/b1` | 0.0031 | 0.0065 | 0.0053 |
| `svd_thin/n4/b1024` | 2.9859 | 1.5264 | 4.7632 |
| `svd_thin/n8/b1` | 0.0097 | 0.0128 | 0.0141 |
| `svd_thin/n8/b1024` | 10.0194 | 3.1472 | 14.3415 |
| `svd_values/n16/b1` | 0.0299 | 0.0332 | 0.0204 |
| `svd_values/n16/b1024` | 32.8200 | 13.1962 | 22.6139 |
| `svd_values/n4/b1` | 0.0029 | 0.0046 | 0.0030 |
| `svd_values/n4/b1024` | 2.6253 | 1.6854 | 2.4880 |
| `svd_values/n8/b1` | 0.0087 | 0.0112 | 0.0068 |
| `svd_values/n8/b1024` | 8.7689 | 3.9255 | 6.5378 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0025 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5914 | 0.1560 | 0.8309 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0963 | 0.0326 | 0.1818 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0026 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2442 | 0.0701 | 0.3469 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0041 | 0.0011 |
| `cholesky/n16/b1024` | 0.8044 | 0.1998 | 1.1031 |
| `cholesky/n4/b1` | 0.0002 | 0.0037 | 0.0002 |
| `cholesky/n4/b1024` | 0.1181 | 0.0335 | 0.1071 |
| `cholesky/n8/b1` | 0.0004 | 0.0039 | 0.0004 |
| `cholesky/n8/b1024` | 0.2698 | 0.0403 | 0.2949 |
| `eig/n16/b1` | 0.0755 | 0.0802 | 0.1016 |
| `eig/n16/b1024` | 81.8434 | 15.3532 | 110.1291 |
| `eig/n4/b1` | 0.0064 | 0.0097 | 0.0085 |
| `eig/n4/b1024` | 6.1441 | 1.0955 | 7.8047 |
| `eig/n8/b1` | 0.0211 | 0.0243 | 0.0264 |
| `eig/n8/b1024` | 21.5061 | 3.9919 | 26.9708 |
| `eigh/n16/b1` | 0.0180 | 0.0399 | 0.0187 |
| `eigh/n16/b1024` | 19.3071 | 2.4297 | 19.3964 |
| `eigh/n4/b1` | 0.0019 | 0.0051 | 0.0019 |
| `eigh/n4/b1024` | 1.7317 | 0.4406 | 1.7068 |
| `eigh/n8/b1` | 0.0056 | 0.0082 | 0.0054 |
| `eigh/n8/b1024` | 5.4075 | 1.3883 | 5.3356 |
| `eigvals/n16/b1` | 0.0470 | 0.0506 | 0.0722 |
| `eigvals/n16/b1024` | 51.8534 | 12.1926 | 80.4049 |
| `eigvals/n4/b1` | 0.0034 | 0.0070 | 0.0069 |
| `eigvals/n4/b1024` | 3.1627 | 1.0905 | 6.0701 |
| `eigvals/n8/b1` | 0.0128 | 0.0155 | 0.0210 |
| `eigvals/n8/b1024` | 12.9072 | 2.9578 | 21.6411 |
| `eigvalsh/n16/b1` | 0.0206 | 0.0240 | 0.0109 |
| `eigvalsh/n16/b1024` | 23.4525 | 11.9900 | 10.9916 |
| `eigvalsh/n4/b1` | 0.0023 | 0.0055 | 0.0014 |
| `eigvalsh/n4/b1024` | 1.8628 | 0.8317 | 1.0970 |
| `eigvalsh/n8/b1` | 0.0062 | 0.0095 | 0.0036 |
| `eigvalsh/n8/b1024` | 5.8536 | 3.9615 | 3.3272 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0061 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.8341 | 0.4433 | 3.6717 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0040 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2778 | 0.0405 | 0.3147 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0041 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7575 | 0.1265 | 0.7336 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0067 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1379 | 0.4134 | 5.0464 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0036 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4726 | 0.1213 | 0.9439 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0043 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1365 | 0.2942 | 1.8817 |
| `householder_apply/n16/b1` | 0.0026 | 0.0055 | 0.0035 |
| `householder_apply/n16/b1024` | 3.2149 | 0.6902 | 4.0217 |
| `householder_apply/n4/b1` | 0.0003 | 0.0024 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1847 | 0.0493 | 0.2494 |
| `householder_apply/n8/b1` | 0.0007 | 0.0023 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6204 | 0.1592 | 0.7720 |
| `householder_factor/n16/b1` | 0.0025 | 0.0053 | 0.0037 |
| `householder_factor/n16/b1024` | 2.5588 | 0.6461 | 3.7596 |
| `householder_factor/n4/b1` | 0.0004 | 0.0040 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3074 | 0.0535 | 0.3098 |
| `householder_factor/n8/b1` | 0.0009 | 0.0034 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8122 | 0.2125 | 0.9101 |
| `lu/n16/b1` | 0.0022 | 0.0055 | 0.0022 |
| `lu/n16/b1024` | 1.9188 | 0.2992 | 2.1605 |
| `lu/n4/b1` | 0.0004 | 0.0031 | 0.0004 |
| `lu/n4/b1024` | 0.2145 | 0.0356 | 0.1818 |
| `lu/n8/b1` | 0.0008 | 0.0038 | 0.0007 |
| `lu/n8/b1024` | 0.5550 | 0.0789 | 0.5293 |
| `lu_factor/n16/b1` | 0.0015 | 0.0047 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2159 | 0.3229 | 1.5818 |
| `lu_factor/n4/b1` | 0.0004 | 0.0036 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1606 | 0.0291 | 0.1102 |
| `lu_factor/n8/b1` | 0.0006 | 0.0038 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3867 | 0.1043 | 0.3759 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0055 | 0.0031 |
| `lu_factor_solve/n16/b1024` | 2.0396 | 0.5198 | 3.1858 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0035 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2517 | 0.0437 | 0.2504 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0026 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6931 | 0.0943 | 1.0002 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0046 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7883 | 0.2116 | 1.5799 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0022 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0972 | 0.0340 | 0.1438 |
| `lu_solve_prepared/n8/b1` | 0.0005 | 0.0022 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.3008 | 0.0857 | 0.6385 |
| `qr/n16/b1` | 0.0067 | 0.0169 | 0.0064 |
| `qr/n16/b1024` | 6.5694 | 0.8407 | 6.3332 |
| `qr/n4/b1` | 0.0007 | 0.0041 | 0.0009 |
| `qr/n4/b1024` | 0.5146 | 0.0708 | 0.5865 |
| `qr/n8/b1` | 0.0018 | 0.0043 | 0.0019 |
| `qr/n8/b1024` | 1.5558 | 0.3971 | 1.5871 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0100 | 0.0093 |
| `rank_revealing_qr/n16/b1024` | 7.2784 | 0.9565 | 9.5244 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0040 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8231 | 0.2106 | 1.0747 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0056 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1824 | 0.5490 | 2.8560 |
| `solve/n16/b1` | 0.0029 | 0.0062 | 0.0035 |
| `solve/n16/b1024` | 2.1672 | 0.2790 | 3.3410 |
| `solve/n4/b1` | 0.0007 | 0.0042 | 0.0005 |
| `solve/n4/b1024` | 0.3101 | 0.0522 | 0.2880 |
| `solve/n8/b1` | 0.0012 | 0.0048 | 0.0012 |
| `solve/n8/b1024` | 0.7600 | 0.1981 | 1.0595 |
| `svd_full/n16/b1` | 0.0347 | 0.0381 | 0.0434 |
| `svd_full/n16/b1024` | 36.5239 | 4.7189 | 48.5588 |
| `svd_full/n4/b1` | 0.0030 | 0.0060 | 0.0053 |
| `svd_full/n4/b1024` | 2.9953 | 0.7515 | 4.7555 |
| `svd_full/n8/b1` | 0.0098 | 0.0125 | 0.0139 |
| `svd_full/n8/b1024` | 10.1224 | 1.8149 | 14.3163 |
| `svd_thin/n16/b1` | 0.0347 | 0.0378 | 0.0432 |
| `svd_thin/n16/b1024` | 36.4726 | 4.7302 | 48.3654 |
| `svd_thin/n4/b1` | 0.0031 | 0.0064 | 0.0053 |
| `svd_thin/n4/b1024` | 2.9787 | 0.7500 | 4.7329 |
| `svd_thin/n8/b1` | 0.0098 | 0.0121 | 0.0140 |
| `svd_thin/n8/b1024` | 10.0194 | 1.7059 | 14.3001 |
| `svd_values/n16/b1` | 0.0299 | 0.0329 | 0.0204 |
| `svd_values/n16/b1024` | 32.7810 | 9.8827 | 22.6212 |
| `svd_values/n4/b1` | 0.0029 | 0.0058 | 0.0030 |
| `svd_values/n4/b1024` | 2.6269 | 0.9362 | 2.4337 |
| `svd_values/n8/b1` | 0.0087 | 0.0111 | 0.0067 |
| `svd_values/n8/b1024` | 8.7778 | 2.9998 | 6.5176 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0038 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5982 | 0.1512 | 0.8620 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0026 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0964 | 0.0285 | 0.1810 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0029 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2415 | 0.0427 | 0.3476 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0417 | - | 0.0566 |
| `cholesky/n128/b128` | 5.8781 | - | 8.2492 |
| `cholesky/n32/b1` | 0.0022 | - | 0.0022 |
| `cholesky/n32/b128` | 0.2683 | - | 0.2604 |
| `eigh/n128/b1` | 1.2557 | - | 1.0788 |
| `eigh/n128/b128` | 161.8250 | - | 144.7089 |
| `eigh/n32/b1` | 0.0639 | - | 0.0554 |
| `eigh/n32/b128` | 8.4039 | - | 7.0538 |
| `eigvalsh/n128/b1` | 2.4276 | - | 0.4539 |
| `eigvalsh/n128/b128` | 320.7508 | - | 58.8758 |
| `eigvalsh/n32/b1` | 0.0831 | - | 0.0249 |
| `eigvalsh/n32/b128` | 10.7954 | - | 3.2215 |
| `householder_apply/n128/b1` | 0.3167 | - | 0.3124 |
| `householder_apply/n128/b128` | 42.4617 | - | 42.4786 |
| `householder_apply/n32/b1` | 0.0111 | - | 0.0074 |
| `householder_apply/n32/b128` | 1.3709 | - | 0.9204 |
| `householder_factor/n128/b1` | 0.1959 | - | 0.1962 |
| `householder_factor/n128/b128` | 25.2215 | - | 25.6542 |
| `householder_factor/n32/b1` | 0.0073 | - | 0.0068 |
| `householder_factor/n32/b128` | 0.9203 | - | 0.8854 |
| `lu/n128/b1` | 0.1013 | - | 0.0818 |
| `lu/n128/b128` | 12.8499 | - | 12.9346 |
| `lu/n32/b1` | 0.0060 | - | 0.0062 |
| `lu/n32/b128` | 0.6873 | - | 0.7828 |
| `lu_factor/n128/b1` | 0.0569 | - | 0.0730 |
| `lu_factor/n128/b128` | 8.2261 | - | 10.0456 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0051 |
| `lu_factor/n32/b128` | 0.3804 | - | 0.6525 |
| `lu_factor_solve/n128/b1` | 0.0626 | - | 0.0853 |
| `lu_factor_solve/n128/b128` | 8.8223 | - | 11.5760 |
| `lu_factor_solve/n32/b1` | 0.0042 | - | 0.0067 |
| `lu_factor_solve/n32/b128` | 0.4921 | - | 0.8471 |
| `lu_solve_prepared/n128/b1` | 0.0059 | - | 0.0122 |
| `lu_solve_prepared/n128/b128` | 2.0196 | - | 2.5412 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0014 |
| `lu_solve_prepared/n32/b128` | 0.1151 | - | 0.1728 |
| `qr/n128/b1` | 0.3400 | - | 0.3946 |
| `qr/n128/b128` | 44.2668 | - | 52.2386 |
| `qr/n32/b1` | 0.0211 | - | 0.0121 |
| `qr/n32/b128` | 2.6421 | - | 1.5629 |
| `rank_revealing_qr/n128/b1` | 0.3453 | - | 0.4785 |
| `rank_revealing_qr/n128/b128` | 45.3466 | - | 63.2634 |
| `rank_revealing_qr/n32/b1` | 0.0212 | - | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6386 | - | 2.2828 |
| `solve/n128/b1` | 0.0686 | - | 0.0879 |
| `solve/n128/b128` | 8.8302 | - | 12.0691 |
| `solve/n32/b1` | 0.0050 | - | 0.0071 |
| `solve/n32/b128` | 0.5394 | - | 0.8764 |
| `svd_thin/n128/b1` | 2.4159 | - | 2.1847 |
| `svd_thin/n128/b128` | 308.4760 | - | 300.7808 |
| `svd_thin/n32/b1` | 0.1199 | - | 0.1172 |
| `svd_thin/n32/b128` | 15.2370 | - | 15.1014 |
| `svd_values/n128/b1` | 1.5554 | - | 0.8540 |
| `svd_values/n128/b128` | 206.5080 | - | 118.6458 |
| `svd_values/n32/b1` | 0.1027 | - | 0.0473 |
| `svd_values/n32/b128` | 13.1819 | - | 6.1029 |
| `triangular_solve/n128/b1` | 0.0040 | - | 0.0071 |
| `triangular_solve/n128/b128` | 0.8813 | - | 1.2845 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0008 |
| `triangular_solve/n32/b128` | 0.0898 | - | 0.0869 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0418 | 0.0518 | 0.0570 |
| `cholesky/n128/b128` | 5.8890 | 6.8362 | 8.2039 |
| `cholesky/n32/b1` | 0.0022 | 0.0043 | 0.0022 |
| `cholesky/n32/b128` | 0.2727 | 0.0710 | 0.2621 |
| `eigh/n128/b1` | 1.2655 | 1.2304 | 0.6249 |
| `eigh/n128/b128` | 161.7648 | 163.1475 | 84.4541 |
| `eigh/n32/b1` | 0.0640 | 0.0690 | 0.0581 |
| `eigh/n32/b128` | 8.4681 | 2.5455 | 7.4796 |
| `eigvalsh/n128/b1` | 2.4343 | 2.8714 | 0.4379 |
| `eigvalsh/n128/b128` | 320.4763 | 322.0015 | 56.5044 |
| `eigvalsh/n32/b1` | 0.0832 | 0.0893 | 0.0249 |
| `eigvalsh/n32/b128` | 10.8138 | 6.3561 | 3.2320 |
| `householder_apply/n128/b1` | 0.3212 | 0.3252 | 0.0875 |
| `householder_apply/n128/b128` | 42.2914 | 42.9092 | 11.6759 |
| `householder_apply/n32/b1` | 0.0107 | 0.0139 | 0.0074 |
| `householder_apply/n32/b128` | 1.3834 | 0.3513 | 0.9129 |
| `householder_factor/n128/b1` | 0.1959 | 0.2000 | 0.1074 |
| `householder_factor/n128/b128` | 25.9077 | 26.3682 | 14.2628 |
| `householder_factor/n32/b1` | 0.0075 | 0.0096 | 0.0068 |
| `householder_factor/n32/b128` | 0.9426 | 0.2500 | 0.8915 |
| `lu/n128/b1` | 0.0921 | 0.1213 | 0.0823 |
| `lu/n128/b128` | 12.8109 | 14.8603 | 12.9658 |
| `lu/n32/b1` | 0.0060 | 0.0100 | 0.0062 |
| `lu/n32/b128` | 0.6928 | 0.3536 | 0.7654 |
| `lu_factor/n128/b1` | 0.0568 | 0.0701 | 0.0732 |
| `lu_factor/n128/b128` | 8.1877 | 2.5397 | 10.0123 |
| `lu_factor/n32/b1` | 0.0032 | 0.0064 | 0.0052 |
| `lu_factor/n32/b128` | 0.3874 | 0.1092 | 0.6583 |
| `lu_factor_solve/n128/b1` | 0.0631 | 0.0772 | 0.0867 |
| `lu_factor_solve/n128/b128` | 8.9469 | 2.7304 | 11.8559 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0068 | 0.0078 |
| `lu_factor_solve/n32/b128` | 0.4929 | 0.1306 | 0.9762 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0087 | 0.0099 |
| `lu_solve_prepared/n128/b128` | 1.9216 | 0.5249 | 2.2370 |
| `lu_solve_prepared/n32/b1` | 0.0011 | 0.0035 | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.1133 | 0.0347 | 0.3001 |
| `qr/n128/b1` | 0.3420 | 0.6230 | 0.2586 |
| `qr/n128/b128` | 43.9657 | 81.1845 | 39.8832 |
| `qr/n32/b1` | 0.0210 | 0.0457 | 0.0120 |
| `qr/n32/b128` | 2.6023 | 1.3333 | 1.5519 |
| `rank_revealing_qr/n128/b1` | 0.3508 | 0.3762 | 0.4631 |
| `rank_revealing_qr/n128/b128` | 44.9532 | 47.4865 | 60.9326 |
| `rank_revealing_qr/n32/b1` | 0.0212 | 0.0477 | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6294 | 1.3502 | 2.2535 |
| `solve/n128/b1` | 0.0690 | 0.0824 | 0.0907 |
| `solve/n128/b128` | 8.8402 | 10.7516 | 12.0801 |
| `solve/n32/b1` | 0.0051 | 0.0075 | 0.0081 |
| `solve/n32/b128` | 0.5486 | 0.2795 | 1.0363 |
| `svd_thin/n128/b1` | 2.4262 | 1.8193 | 1.7617 |
| `svd_thin/n128/b128` | 308.5781 | 231.3353 | 246.0334 |
| `svd_thin/n32/b1` | 0.1175 | 0.1222 | 0.1219 |
| `svd_thin/n32/b128` | 15.1578 | 4.6971 | 15.7060 |
| `svd_values/n128/b1` | 1.5609 | 1.8019 | 0.8361 |
| `svd_values/n128/b128` | 207.0777 | 208.9014 | 116.9444 |
| `svd_values/n32/b1` | 0.1032 | 0.1095 | 0.0474 |
| `svd_values/n32/b128` | 13.2213 | 4.9017 | 6.1201 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0064 | 0.0059 |
| `triangular_solve/n128/b128` | 0.7647 | 0.7757 | 1.3691 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0027 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0869 | 0.0464 | 0.1636 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0412 | 0.0545 | 0.0552 |
| `cholesky/n128/b128` | 5.9101 | 7.3773 | 8.2698 |
| `cholesky/n32/b1` | 0.0022 | 0.0055 | 0.0022 |
| `cholesky/n32/b128` | 0.2631 | 0.0419 | 0.2596 |
| `eigh/n128/b1` | 1.2604 | 1.2401 | 0.5915 |
| `eigh/n128/b128` | 161.9965 | 160.0115 | 79.3087 |
| `eigh/n32/b1` | 0.0639 | 0.0681 | 0.0591 |
| `eigh/n32/b128` | 8.4431 | 2.1364 | 7.5245 |
| `eigvalsh/n128/b1` | 2.4374 | 3.1394 | 0.4490 |
| `eigvalsh/n128/b128` | 323.0869 | 324.4376 | 58.4838 |
| `eigvalsh/n32/b1` | 0.0832 | 0.0887 | 0.0248 |
| `eigvalsh/n32/b128` | 10.8016 | 5.9278 | 3.2214 |
| `householder_apply/n128/b1` | 0.3113 | 0.3303 | 0.0565 |
| `householder_apply/n128/b128` | 40.6151 | 43.2439 | 7.4058 |
| `householder_apply/n32/b1` | 0.0106 | 0.0132 | 0.0074 |
| `householder_apply/n32/b128` | 1.3316 | 0.3320 | 0.9209 |
| `householder_factor/n128/b1` | 0.1926 | 0.1986 | 0.0849 |
| `householder_factor/n128/b128` | 25.1665 | 25.2970 | 11.5372 |
| `householder_factor/n32/b1` | 0.0071 | 0.0095 | 0.0068 |
| `householder_factor/n32/b128` | 0.8937 | 0.2334 | 0.8806 |
| `lu/n128/b1` | 0.0994 | 0.1269 | 0.0827 |
| `lu/n128/b128` | 12.8130 | 16.8396 | 12.9502 |
| `lu/n32/b1` | 0.0061 | 0.0087 | 0.0063 |
| `lu/n32/b128` | 0.6927 | 0.1734 | 0.7702 |
| `lu_factor/n128/b1` | 0.0563 | 0.0818 | 0.0727 |
| `lu_factor/n128/b128` | 8.2369 | 1.4741 | 10.0517 |
| `lu_factor/n32/b1` | 0.0033 | 0.0058 | 0.0051 |
| `lu_factor/n32/b128` | 0.3904 | 0.1071 | 0.6539 |
| `lu_factor_solve/n128/b1` | 0.0619 | 0.0873 | 0.0868 |
| `lu_factor_solve/n128/b128` | 8.9564 | 1.5741 | 11.9346 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0068 | 0.0077 |
| `lu_factor_solve/n32/b128` | 0.5011 | 0.1365 | 1.0167 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0093 | 0.0100 |
| `lu_solve_prepared/n128/b128` | 2.0414 | 0.2930 | 2.3038 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0038 | 0.0023 |
| `lu_solve_prepared/n32/b128` | 0.1155 | 0.0343 | 0.3341 |
| `qr/n128/b1` | 0.3432 | 0.9387 | 0.2980 |
| `qr/n128/b128` | 44.1728 | 120.8746 | 31.1723 |
| `qr/n32/b1` | 0.0211 | 0.0643 | 0.0119 |
| `qr/n32/b128` | 2.6225 | 0.3616 | 1.5347 |
| `rank_revealing_qr/n128/b1` | 0.3542 | 0.4408 | 0.4876 |
| `rank_revealing_qr/n128/b128` | 45.5063 | 56.9872 | 63.4722 |
| `rank_revealing_qr/n32/b1` | 0.0210 | 0.0667 | 0.0179 |
| `rank_revealing_qr/n32/b128` | 2.6221 | 0.3348 | 2.2624 |
| `solve/n128/b1` | 0.0685 | 0.0943 | 0.0901 |
| `solve/n128/b128` | 8.9124 | 12.1269 | 12.1894 |
| `solve/n32/b1` | 0.0049 | 0.0074 | 0.0079 |
| `solve/n32/b128` | 0.5445 | 0.1436 | 0.9995 |
| `svd_thin/n128/b1` | 2.4201 | 1.8690 | 1.6955 |
| `svd_thin/n128/b128` | 308.5808 | 238.3175 | 237.2262 |
| `svd_thin/n32/b1` | 0.1172 | 0.1216 | 0.1235 |
| `svd_thin/n32/b128` | 15.2279 | 1.9809 | 15.9169 |
| `svd_values/n128/b1` | 1.5659 | 1.7471 | 0.8432 |
| `svd_values/n128/b128` | 206.9627 | 208.5234 | 116.7890 |
| `svd_values/n32/b1` | 0.1029 | 0.1087 | 0.0473 |
| `svd_values/n32/b128` | 13.2365 | 3.9612 | 6.1146 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0068 | 0.0061 |
| `triangular_solve/n128/b128` | 0.9827 | 1.0458 | 1.3910 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0025 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0901 | 0.0257 | 0.1870 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1089 | - | 0.2415 |
| `cholesky/n128/b128` | 15.9271 | - | 32.7810 |
| `cholesky/n32/b1` | 0.0034 | - | 0.0047 |
| `cholesky/n32/b128` | 0.4233 | - | 0.6294 |
| `eigh/n128/b1` | 1.8550 | - | 2.9683 |
| `eigh/n128/b128` | 241.1758 | - | 384.8122 |
| `eigh/n32/b1` | 0.0808 | - | 0.0867 |
| `eigh/n32/b128` | 10.4804 | - | 11.3912 |
| `eigvalsh/n128/b1` | 2.7151 | - | 1.2668 |
| `eigvalsh/n128/b128` | 369.8996 | - | 163.6250 |
| `eigvalsh/n32/b1` | 0.0897 | - | 0.0444 |
| `eigvalsh/n32/b128` | 11.7261 | - | 5.7648 |
| `householder_apply/n128/b1` | 0.6982 | - | 0.9656 |
| `householder_apply/n128/b128` | 92.6096 | - | 126.7661 |
| `householder_apply/n32/b1` | 0.0145 | - | 0.0196 |
| `householder_apply/n32/b128` | 1.8873 | - | 2.5485 |
| `householder_factor/n128/b1` | 0.4532 | - | 0.5427 |
| `householder_factor/n128/b128` | 58.8590 | - | 70.5811 |
| `householder_factor/n32/b1` | 0.0111 | - | 0.0155 |
| `householder_factor/n32/b128` | 1.4277 | - | 2.0067 |
| `lu/n128/b1` | 0.2017 | - | 0.2705 |
| `lu/n128/b128` | 28.1070 | - | 38.5691 |
| `lu/n32/b1` | 0.0079 | - | 0.0106 |
| `lu/n32/b128` | 1.0067 | - | 1.4353 |
| `lu_factor/n128/b1` | 0.1563 | - | 0.2484 |
| `lu_factor/n128/b128` | 21.8147 | - | 32.8260 |
| `lu_factor/n32/b1` | 0.0053 | - | 0.0090 |
| `lu_factor/n32/b128` | 0.6489 | - | 1.1477 |
| `lu_factor_solve/n128/b1` | 0.1747 | - | 0.2828 |
| `lu_factor_solve/n128/b128` | 24.2437 | - | 36.8538 |
| `lu_factor_solve/n32/b1` | 0.0075 | - | 0.0134 |
| `lu_factor_solve/n32/b128` | 0.9113 | - | 1.7102 |
| `lu_solve_prepared/n128/b1` | 0.0188 | - | 0.0317 |
| `lu_solve_prepared/n128/b128` | 4.1232 | - | 5.7783 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0044 |
| `lu_solve_prepared/n32/b128` | 0.2819 | - | 0.5617 |
| `qr/n128/b1` | 0.9697 | - | 1.1403 |
| `qr/n128/b128` | 125.0269 | - | 147.7505 |
| `qr/n32/b1` | 0.0428 | - | 0.0284 |
| `qr/n32/b128` | 5.4255 | - | 3.6484 |
| `rank_revealing_qr/n128/b1` | 1.0089 | - | 1.5961 |
| `rank_revealing_qr/n128/b128` | 129.8630 | - | 207.4222 |
| `rank_revealing_qr/n32/b1` | 0.0389 | - | 0.0391 |
| `rank_revealing_qr/n32/b128` | 4.9575 | - | 5.1178 |
| `solve/n128/b1` | 0.1815 | - | 0.2861 |
| `solve/n128/b128` | 23.6575 | - | 37.4867 |
| `solve/n32/b1` | 0.0083 | - | 0.0140 |
| `solve/n32/b128` | 0.9623 | - | 1.7614 |
| `svd_thin/n128/b1` | 3.9200 | - | 4.3965 |
| `svd_thin/n128/b128` | 506.1853 | - | 600.7505 |
| `svd_thin/n32/b1` | 0.1505 | - | 0.1658 |
| `svd_thin/n32/b128` | 19.6774 | - | 22.3693 |
| `svd_values/n128/b1` | 2.0759 | - | 1.7842 |
| `svd_values/n128/b128` | 289.3674 | - | 250.8823 |
| `svd_values/n32/b1` | 0.1135 | - | 0.0736 |
| `svd_values/n32/b128` | 14.9512 | - | 9.5646 |
| `triangular_solve/n128/b1` | 0.0109 | - | 0.0148 |
| `triangular_solve/n128/b128` | 2.3003 | - | 2.8214 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0021 |
| `triangular_solve/n32/b128` | 0.1916 | - | 0.2601 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1076 | 0.1081 | 0.2442 |
| `cholesky/n128/b128` | 16.2112 | 15.9291 | 32.8822 |
| `cholesky/n32/b1` | 0.0033 | 0.0060 | 0.0049 |
| `cholesky/n32/b128` | 0.4243 | 0.1148 | 0.6317 |
| `eigh/n128/b1` | 1.8499 | 1.7486 | 1.8010 |
| `eigh/n128/b128` | 240.8253 | 207.9796 | 235.8118 |
| `eigh/n32/b1` | 0.0806 | 0.0851 | 0.0865 |
| `eigh/n32/b128` | 10.5083 | 2.6962 | 11.3543 |
| `eigvalsh/n128/b1` | 2.7089 | 3.9995 | 0.8129 |
| `eigvalsh/n128/b128` | 371.0339 | 372.3149 | 106.4168 |
| `eigvalsh/n32/b1` | 0.0897 | 0.0953 | 0.0443 |
| `eigvalsh/n32/b128` | 11.6828 | 6.9573 | 5.7743 |
| `householder_apply/n128/b1` | 0.6905 | 0.6935 | 0.2761 |
| `householder_apply/n128/b128` | 93.0767 | 93.3483 | 35.5847 |
| `householder_apply/n32/b1` | 0.0146 | 0.0172 | 0.0197 |
| `householder_apply/n32/b128` | 1.8391 | 0.4699 | 2.5390 |
| `householder_factor/n128/b1` | 0.4586 | 0.4607 | 0.2585 |
| `householder_factor/n128/b128` | 59.2099 | 59.0686 | 33.8493 |
| `householder_factor/n32/b1` | 0.0111 | 0.0141 | 0.0155 |
| `householder_factor/n32/b128` | 1.4308 | 0.7071 | 2.0116 |
| `lu/n128/b1` | 0.2017 | 0.1906 | 0.2727 |
| `lu/n128/b128` | 28.1887 | 26.2152 | 38.8448 |
| `lu/n32/b1` | 0.0080 | 0.0109 | 0.0105 |
| `lu/n32/b128` | 1.0243 | 0.5081 | 1.4343 |
| `lu_factor/n128/b1` | 0.1569 | 0.1486 | 0.2484 |
| `lu_factor/n128/b128` | 21.7744 | 6.2080 | 32.6756 |
| `lu_factor/n32/b1` | 0.0052 | 0.0086 | 0.0090 |
| `lu_factor/n32/b128` | 0.6421 | 0.3313 | 1.1434 |
| `lu_factor_solve/n128/b1` | 0.1759 | 0.1652 | 0.2681 |
| `lu_factor_solve/n128/b128` | 24.2061 | 6.5087 | 35.3335 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0107 | 0.0118 |
| `lu_factor_solve/n32/b128` | 0.9151 | 0.4675 | 1.5399 |
| `lu_solve_prepared/n128/b1` | 0.0188 | 0.0220 | 0.0150 |
| `lu_solve_prepared/n128/b128` | 4.1350 | 1.4509 | 3.7648 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0038 | 0.0026 |
| `lu_solve_prepared/n32/b128` | 0.2849 | 0.0753 | 0.3493 |
| `qr/n128/b1` | 0.9606 | 0.8451 | 0.5939 |
| `qr/n128/b128` | 124.8890 | 113.2060 | 77.9435 |
| `qr/n32/b1` | 0.0430 | 0.0663 | 0.0285 |
| `qr/n32/b128` | 5.4898 | 2.7557 | 3.6686 |
| `rank_revealing_qr/n128/b1` | 1.0033 | 0.7933 | 1.3740 |
| `rank_revealing_qr/n128/b128` | 130.4457 | 104.2855 | 178.4998 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0660 | 0.0390 |
| `rank_revealing_qr/n32/b128` | 4.9475 | 1.2640 | 5.1272 |
| `solve/n128/b1` | 0.1817 | 0.1690 | 0.2795 |
| `solve/n128/b128` | 23.6135 | 22.0207 | 36.3600 |
| `solve/n32/b1` | 0.0083 | 0.0104 | 0.0125 |
| `solve/n32/b128` | 0.9553 | 0.2489 | 1.5826 |
| `svd_thin/n128/b1` | 3.9140 | 2.7086 | 2.7165 |
| `svd_thin/n128/b128` | 504.7863 | 349.6094 | 386.9606 |
| `svd_thin/n32/b1` | 0.1497 | 0.1547 | 0.1723 |
| `svd_thin/n32/b128` | 19.5778 | 7.7951 | 22.9450 |
| `svd_values/n128/b1` | 2.0758 | 2.3425 | 1.4114 |
| `svd_values/n128/b128` | 288.0372 | 288.3055 | 201.9705 |
| `svd_values/n32/b1` | 0.1138 | 0.1214 | 0.0735 |
| `svd_values/n32/b128` | 14.9288 | 5.7271 | 9.5599 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0139 | 0.0078 |
| `triangular_solve/n128/b128` | 2.3582 | 2.2673 | 2.2294 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0038 | 0.0015 |
| `triangular_solve/n32/b128` | 0.1906 | 0.0514 | 0.1901 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1089 | 0.1170 | 0.2441 |
| `cholesky/n128/b128` | 15.9515 | 16.3940 | 32.9296 |
| `cholesky/n32/b1` | 0.0032 | 0.0066 | 0.0049 |
| `cholesky/n32/b128` | 0.4065 | 0.0575 | 0.6269 |
| `eigh/n128/b1` | 1.8423 | 1.6190 | 1.6123 |
| `eigh/n128/b128` | 241.2652 | 212.6117 | 210.8607 |
| `eigh/n32/b1` | 0.0808 | 0.0849 | 0.0871 |
| `eigh/n32/b128` | 10.5471 | 1.3782 | 11.3196 |
| `eigvalsh/n128/b1` | 2.7149 | 3.9115 | 0.7388 |
| `eigvalsh/n128/b128` | 369.7375 | 370.8963 | 96.5599 |
| `eigvalsh/n32/b1` | 0.0898 | 0.0948 | 0.0445 |
| `eigvalsh/n32/b128` | 11.6893 | 6.1114 | 5.7827 |
| `householder_apply/n128/b1` | 0.6840 | 0.6920 | 0.1753 |
| `householder_apply/n128/b128` | 92.9222 | 93.3371 | 21.8274 |
| `householder_apply/n32/b1` | 0.0142 | 0.0176 | 0.0197 |
| `householder_apply/n32/b128` | 1.8682 | 0.4615 | 2.5593 |
| `householder_factor/n128/b1` | 0.4595 | 0.4617 | 0.1812 |
| `householder_factor/n128/b128` | 59.3192 | 59.0626 | 23.4504 |
| `householder_factor/n32/b1` | 0.0112 | 0.0136 | 0.0155 |
| `householder_factor/n32/b128` | 1.4049 | 0.1840 | 2.0170 |
| `lu/n128/b1` | 0.2036 | 0.2021 | 0.2716 |
| `lu/n128/b128` | 28.1109 | 28.0521 | 38.6741 |
| `lu/n32/b1` | 0.0080 | 0.0107 | 0.0105 |
| `lu/n32/b128` | 0.9997 | 0.2481 | 1.4130 |
| `lu_factor/n128/b1` | 0.1550 | 0.1525 | 0.2466 |
| `lu_factor/n128/b128` | 21.9211 | 3.2861 | 32.6191 |
| `lu_factor/n32/b1` | 0.0054 | 0.0086 | 0.0090 |
| `lu_factor/n32/b128` | 0.6574 | 0.1735 | 1.1391 |
| `lu_factor_solve/n128/b1` | 0.1732 | 0.1709 | 0.2669 |
| `lu_factor_solve/n128/b128` | 24.2917 | 3.5824 | 35.4181 |
| `lu_factor_solve/n32/b1` | 0.0074 | 0.0100 | 0.0119 |
| `lu_factor_solve/n32/b128` | 0.9254 | 0.2441 | 1.5654 |
| `lu_solve_prepared/n128/b1` | 0.0187 | 0.0214 | 0.0153 |
| `lu_solve_prepared/n128/b128` | 4.2866 | 0.7378 | 3.7495 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0053 | 0.0027 |
| `lu_solve_prepared/n32/b128` | 0.2833 | 0.0483 | 0.3738 |
| `qr/n128/b1` | 0.9717 | 1.2091 | 0.4427 |
| `qr/n128/b128` | 124.7748 | 153.7513 | 57.7417 |
| `qr/n32/b1` | 0.0427 | 0.0892 | 0.0285 |
| `qr/n32/b128` | 5.4593 | 0.7183 | 3.6826 |
| `rank_revealing_qr/n128/b1` | 1.0131 | 0.8952 | 1.2380 |
| `rank_revealing_qr/n128/b128` | 130.2771 | 114.1342 | 160.3207 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0882 | 0.0391 |
| `rank_revealing_qr/n32/b128` | 4.9855 | 0.6292 | 5.1393 |
| `solve/n128/b1` | 0.1820 | 0.1797 | 0.2795 |
| `solve/n128/b128` | 23.5928 | 23.5496 | 36.4482 |
| `solve/n32/b1` | 0.0083 | 0.0110 | 0.0127 |
| `solve/n32/b128` | 0.9697 | 0.1524 | 1.6151 |
| `svd_thin/n128/b1` | 3.9342 | 2.7545 | 2.4137 |
| `svd_thin/n128/b128` | 507.7277 | 363.8029 | 346.8201 |
| `svd_thin/n32/b1` | 0.1499 | 0.1530 | 0.1732 |
| `svd_thin/n32/b128` | 19.6663 | 2.4704 | 23.1907 |
| `svd_values/n128/b1` | 2.0802 | 2.3377 | 1.3707 |
| `svd_values/n128/b128` | 289.2527 | 288.8930 | 196.2948 |
| `svd_values/n32/b1` | 0.1132 | 0.1216 | 0.0738 |
| `svd_values/n32/b128` | 14.8967 | 3.9979 | 9.5400 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0138 | 0.0078 |
| `triangular_solve/n128/b128` | 2.4038 | 2.2752 | 2.2869 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0047 | 0.0016 |
| `triangular_solve/n32/b128` | 0.1937 | 0.0501 | 0.1828 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2091 | - | 0.2670 |
| `cholesky/n256/b4` | 0.8458 | - | 1.0694 |
| `cholesky/n512/b1` | 1.3275 | - | 1.9966 |
| `cholesky/n512/b4` | 5.5272 | - | 8.4061 |
| `eigh/n256/b1` | 5.5892 | - | 5.9125 |
| `eigh/n256/b4` | 22.4341 | - | 23.8488 |
| `eigh/n512/b1` | 28.8587 | - | 36.5423 |
| `eigh/n512/b4` | 115.6944 | - | 146.3124 |
| `eigvalsh/n256/b1` | 16.0823 | - | 2.5634 |
| `eigvalsh/n256/b4` | 64.4857 | - | 10.3313 |
| `eigvalsh/n512/b1` | 117.6220 | - | 16.5262 |
| `eigvalsh/n512/b4` | 478.9712 | - | 66.2560 |
| `householder_apply/n256/b1` | 2.2570 | - | 1.9170 |
| `householder_apply/n256/b4` | 9.6961 | - | 7.7834 |
| `householder_apply/n512/b1` | 18.9505 | - | 12.8488 |
| `householder_apply/n512/b4` | 75.7851 | - | 52.1157 |
| `householder_factor/n256/b1` | 1.4662 | - | 1.1162 |
| `householder_factor/n256/b4` | 5.9138 | - | 4.5251 |
| `householder_factor/n512/b1` | 12.0569 | - | 8.0793 |
| `householder_factor/n512/b4` | 48.2801 | - | 32.6392 |
| `lu/n256/b1` | 0.5043 | - | 0.4982 |
| `lu/n256/b4` | 2.0910 | - | 2.1283 |
| `lu/n512/b1` | 3.2848 | - | 3.3181 |
| `lu/n512/b4` | 13.2163 | - | 13.5197 |
| `lu_factor/n256/b1` | 0.3523 | - | 0.4547 |
| `lu_factor/n256/b4` | 1.5307 | - | 1.8387 |
| `lu_factor/n512/b1` | 2.7508 | - | 3.0019 |
| `lu_factor/n512/b4` | 11.7440 | - | 12.3557 |
| `lu_factor_solve/n256/b1` | 0.3694 | - | 0.4978 |
| `lu_factor_solve/n256/b4` | 1.5886 | - | 2.0011 |
| `lu_factor_solve/n512/b1` | 2.8056 | - | 3.1699 |
| `lu_factor_solve/n512/b4` | 11.9808 | - | 13.1041 |
| `lu_solve_prepared/n256/b1` | 0.0169 | - | 0.0399 |
| `lu_solve_prepared/n256/b4` | 0.0814 | - | 0.1735 |
| `lu_solve_prepared/n512/b1` | 0.0709 | - | 0.1921 |
| `lu_solve_prepared/n512/b4` | 0.3713 | - | 0.9679 |
| `qr/n256/b1` | 1.8575 | - | 2.3754 |
| `qr/n256/b4` | 7.4047 | - | 9.5695 |
| `qr/n512/b1` | 11.4993 | - | 17.0969 |
| `qr/n512/b4` | 46.0849 | - | 69.4061 |
| `rank_revealing_qr/n256/b1` | 2.1327 | - | 2.9293 |
| `rank_revealing_qr/n256/b4` | 8.4428 | - | 11.8507 |
| `rank_revealing_qr/n512/b1` | 14.8638 | - | 21.3196 |
| `rank_revealing_qr/n512/b4` | 59.2780 | - | 86.2097 |
| `solve/n256/b1` | 0.3998 | - | 0.5085 |
| `solve/n256/b4` | 1.5728 | - | 2.0492 |
| `solve/n512/b1` | 2.8621 | - | 3.2271 |
| `solve/n512/b4` | 11.4111 | - | 12.9438 |
| `svd_thin/n256/b1` | 12.2386 | - | 11.4566 |
| `svd_thin/n256/b4` | 48.7802 | - | 46.2151 |
| `svd_thin/n512/b1` | 70.5183 | - | 73.5570 |
| `svd_thin/n512/b4` | 283.2525 | - | 304.4284 |
| `svd_values/n256/b1` | 7.5333 | - | 4.7066 |
| `svd_values/n256/b4` | 30.0318 | - | 18.9820 |
| `svd_values/n512/b1` | 40.8915 | - | 30.7250 |
| `svd_values/n512/b4` | 167.6462 | - | 127.7406 |
| `triangular_solve/n256/b1` | 0.0104 | - | 0.0236 |
| `triangular_solve/n256/b4` | 0.0442 | - | 0.1097 |
| `triangular_solve/n512/b1` | 0.0340 | - | 0.0944 |
| `triangular_solve/n512/b4` | 0.1426 | - | 0.4033 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2101 | 0.1978 | 0.1619 |
| `cholesky/n256/b4` | 0.8349 | 0.7702 | 0.5838 |
| `cholesky/n512/b1` | 1.3030 | 0.8362 | 0.8312 |
| `cholesky/n512/b4` | 5.6569 | 3.6293 | 3.9941 |
| `eigh/n256/b1` | 5.5854 | 4.1631 | 2.7867 |
| `eigh/n256/b4` | 22.3656 | 16.9428 | 11.2871 |
| `eigh/n512/b1` | 28.6757 | 16.0155 | 13.2676 |
| `eigh/n512/b4` | 114.8207 | 63.9016 | 53.0419 |
| `eigvalsh/n256/b1` | 16.0336 | 17.0016 | 1.8763 |
| `eigvalsh/n256/b4` | 64.5766 | 65.9797 | 7.4955 |
| `eigvalsh/n512/b1` | 116.5367 | 114.9474 | 8.9222 |
| `eigvalsh/n512/b4` | 470.0978 | 462.1409 | 35.9808 |
| `householder_apply/n256/b1` | 2.3699 | 2.3997 | 0.5700 |
| `householder_apply/n256/b4` | 9.7414 | 9.8006 | 2.2869 |
| `householder_apply/n512/b1` | 18.7484 | 18.6717 | 3.5201 |
| `householder_apply/n512/b4` | 84.0302 | 83.2965 | 14.2143 |
| `householder_factor/n256/b1` | 1.4812 | 1.5069 | 0.3664 |
| `householder_factor/n256/b4` | 5.9167 | 5.9599 | 1.4641 |
| `householder_factor/n512/b1` | 12.0855 | 12.0363 | 2.1714 |
| `householder_factor/n512/b4` | 48.6312 | 48.5019 | 8.8068 |
| `lu/n256/b1` | 0.4950 | 0.4674 | 0.1990 |
| `lu/n256/b4` | 2.0061 | 1.9235 | 0.9013 |
| `lu/n512/b1` | 3.2556 | 2.0426 | 1.1614 |
| `lu/n512/b4` | 13.1702 | 8.0189 | 4.9755 |
| `lu_factor/n256/b1` | 0.3776 | 0.3237 | 0.1612 |
| `lu_factor/n256/b4` | 1.5315 | 0.7725 | 0.6529 |
| `lu_factor/n512/b1` | 2.8262 | 1.4627 | 0.8479 |
| `lu_factor/n512/b4` | 11.7631 | 3.6315 | 3.4877 |
| `lu_factor_solve/n256/b1` | 0.3743 | 0.3337 | 0.1925 |
| `lu_factor_solve/n256/b4` | 1.4936 | 0.3852 | 0.7823 |
| `lu_factor_solve/n512/b1` | 2.8897 | 1.5249 | 0.9559 |
| `lu_factor_solve/n512/b4` | 12.0116 | 4.9824 | 3.9391 |
| `lu_solve_prepared/n256/b1` | 0.0172 | 0.0237 | 0.0246 |
| `lu_solve_prepared/n256/b4` | 0.0797 | 0.0236 | 0.1268 |
| `lu_solve_prepared/n512/b1` | 0.0614 | 0.0655 | 0.0968 |
| `lu_solve_prepared/n512/b4` | 0.4344 | 0.2018 | 0.5601 |
| `qr/n256/b1` | 1.8574 | 1.8220 | 1.1547 |
| `qr/n256/b4` | 7.3823 | 7.1079 | 4.6436 |
| `qr/n512/b1` | 11.5767 | 6.0706 | 6.8808 |
| `qr/n512/b4` | 45.9776 | 24.4519 | 27.9911 |
| `rank_revealing_qr/n256/b1` | 2.1335 | 1.4720 | 2.3192 |
| `rank_revealing_qr/n256/b4` | 8.4050 | 5.8760 | 9.3368 |
| `rank_revealing_qr/n512/b1` | 14.8926 | 6.2393 | 15.7171 |
| `rank_revealing_qr/n512/b4` | 59.7831 | 25.0786 | 63.4732 |
| `solve/n256/b1` | 0.3957 | 0.3601 | 0.2102 |
| `solve/n256/b4` | 1.5762 | 1.4417 | 0.8460 |
| `solve/n512/b1` | 2.8714 | 1.6006 | 1.0197 |
| `solve/n512/b4` | 11.4356 | 6.2345 | 4.1940 |
| `svd_thin/n256/b1` | 12.2501 | 8.7669 | 8.2568 |
| `svd_thin/n256/b4` | 48.8570 | 35.9762 | 33.2896 |
| `svd_thin/n512/b1` | 71.2735 | 40.2380 | 39.2031 |
| `svd_thin/n512/b4` | 285.3597 | 159.9328 | 168.9875 |
| `svd_values/n256/b1` | 7.5266 | 8.2197 | 4.3228 |
| `svd_values/n256/b4` | 29.9928 | 31.8535 | 17.3662 |
| `svd_values/n512/b1` | 41.0327 | 34.5445 | 17.8640 |
| `svd_values/n512/b4` | 167.8617 | 140.0308 | 75.5294 |
| `triangular_solve/n256/b1` | 0.0103 | 0.0157 | 0.0155 |
| `triangular_solve/n256/b4` | 0.0457 | 0.0556 | 0.0747 |
| `triangular_solve/n512/b1` | 0.0341 | 0.0353 | 0.0568 |
| `triangular_solve/n512/b4` | 0.1575 | 0.1483 | 0.2492 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2093 | 0.2079 | 0.1609 |
| `cholesky/n256/b4` | 0.8312 | 0.8353 | 0.4823 |
| `cholesky/n512/b1` | 1.2805 | 0.7186 | 0.5600 |
| `cholesky/n512/b4` | 5.6986 | 3.2063 | 2.6980 |
| `eigh/n256/b1` | 5.5471 | 4.1976 | 2.3200 |
| `eigh/n256/b4` | 22.4792 | 17.2017 | 9.4117 |
| `eigh/n512/b1` | 28.9468 | 14.9377 | 9.2968 |
| `eigh/n512/b4` | 114.6733 | 59.5921 | 37.4658 |
| `eigvalsh/n256/b1` | 16.1521 | 17.1781 | 1.7812 |
| `eigvalsh/n256/b4` | 64.7857 | 65.9443 | 7.1422 |
| `eigvalsh/n512/b1` | 117.8591 | 115.8129 | 7.6037 |
| `eigvalsh/n512/b4` | 471.4606 | 461.0130 | 30.5576 |
| `householder_apply/n256/b1` | 2.3975 | 2.4270 | 0.3133 |
| `householder_apply/n256/b4` | 9.7615 | 9.8345 | 1.2288 |
| `householder_apply/n512/b1` | 18.9383 | 19.2398 | 1.9222 |
| `householder_apply/n512/b4` | 82.9879 | 83.7434 | 7.7990 |
| `householder_factor/n256/b1` | 1.4707 | 1.5064 | 0.3173 |
| `householder_factor/n256/b4` | 5.9573 | 5.9907 | 1.2765 |
| `householder_factor/n512/b1` | 12.0925 | 12.1613 | 1.3079 |
| `householder_factor/n512/b4` | 48.1976 | 49.4057 | 5.3778 |
| `lu/n256/b1` | 0.5054 | 0.5313 | 0.1883 |
| `lu/n256/b4` | 2.0328 | 2.0357 | 0.8526 |
| `lu/n512/b1` | 3.2618 | 2.0984 | 0.8892 |
| `lu/n512/b4` | 13.0029 | 8.3314 | 3.8726 |
| `lu_factor/n256/b1` | 0.3792 | 0.3610 | 0.1514 |
| `lu_factor/n256/b4` | 1.5388 | 1.4515 | 0.6172 |
| `lu_factor/n512/b1` | 2.8277 | 1.5157 | 0.6188 |
| `lu_factor/n512/b4` | 11.7589 | 6.2758 | 2.4499 |
| `lu_factor_solve/n256/b1` | 0.3723 | 0.3862 | 0.1906 |
| `lu_factor_solve/n256/b4` | 1.4993 | 1.4813 | 0.7680 |
| `lu_factor_solve/n512/b1` | 2.8897 | 1.5917 | 0.7382 |
| `lu_factor_solve/n512/b4` | 12.1532 | 6.5769 | 3.0031 |
| `lu_solve_prepared/n256/b1` | 0.0171 | 0.0270 | 0.0248 |
| `lu_solve_prepared/n256/b4` | 0.0820 | 0.1131 | 0.1215 |
| `lu_solve_prepared/n512/b1` | 0.0726 | 0.0727 | 0.0965 |
| `lu_solve_prepared/n512/b4` | 0.4375 | 0.3851 | 0.6053 |
| `qr/n256/b1` | 1.8584 | 2.4658 | 1.1102 |
| `qr/n256/b4` | 7.3868 | 9.8738 | 4.4517 |
| `qr/n512/b1` | 11.4842 | 6.9436 | 5.3036 |
| `qr/n512/b4` | 46.1620 | 28.2413 | 21.5511 |
| `rank_revealing_qr/n256/b1` | 2.1068 | 1.5677 | 2.2049 |
| `rank_revealing_qr/n256/b4` | 8.4375 | 6.2409 | 8.8476 |
| `rank_revealing_qr/n512/b1` | 14.7687 | 5.8307 | 14.8454 |
| `rank_revealing_qr/n512/b4` | 59.5042 | 23.4448 | 59.5904 |
| `solve/n256/b1` | 0.3940 | 0.4050 | 0.2104 |
| `solve/n256/b4` | 1.5787 | 1.6222 | 0.8349 |
| `solve/n512/b1` | 2.8741 | 1.6612 | 0.7625 |
| `solve/n512/b4` | 11.4287 | 6.5674 | 3.2289 |
| `svd_thin/n256/b1` | 12.2510 | 9.0207 | 7.6729 |
| `svd_thin/n256/b4` | 48.8098 | 36.0658 | 30.9604 |
| `svd_thin/n512/b1` | 70.5881 | 38.3048 | 32.6937 |
| `svd_thin/n512/b4` | 282.9567 | 153.8860 | 142.7164 |
| `svd_values/n256/b1` | 7.5132 | 8.4109 | 4.2596 |
| `svd_values/n256/b4` | 29.9604 | 31.3309 | 17.0868 |
| `svd_values/n512/b1` | 41.0575 | 35.2253 | 15.7788 |
| `svd_values/n512/b4` | 168.4232 | 142.8107 | 67.1745 |
| `triangular_solve/n256/b1` | 0.0103 | 0.0187 | 0.0154 |
| `triangular_solve/n256/b4` | 0.0458 | 0.0630 | 0.0724 |
| `triangular_solve/n512/b1` | 0.0343 | 0.0433 | 0.0560 |
| `triangular_solve/n512/b4` | 0.1333 | 0.1739 | 0.2510 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7051 | - | 1.0968 |
| `cholesky/n256/b4` | 2.8869 | - | 4.4334 |
| `cholesky/n512/b1` | 4.7395 | - | 7.5289 |
| `cholesky/n512/b4` | 19.3736 | - | 26.2223 |
| `eigh/n256/b1` | 10.2418 | - | 20.8328 |
| `eigh/n256/b4` | 41.0295 | - | 84.1763 |
| `eigh/n512/b1` | 62.7090 | - | 153.9508 |
| `eigh/n512/b4` | 251.7287 | - | 608.2381 |
| `eigvalsh/n256/b1` | 18.2445 | - | 8.1390 |
| `eigvalsh/n256/b4` | 73.3196 | - | 32.5585 |
| `eigvalsh/n512/b1` | 133.1942 | - | 58.0387 |
| `eigvalsh/n512/b4` | 531.5165 | - | 231.5135 |
| `householder_apply/n256/b1` | 5.0909 | - | 6.2628 |
| `householder_apply/n256/b4` | 21.4974 | - | 25.4282 |
| `householder_apply/n512/b1` | 42.6063 | - | 37.7289 |
| `householder_apply/n512/b4` | 176.0257 | - | 148.6961 |
| `householder_factor/n256/b1` | 3.3137 | - | 3.2993 |
| `householder_factor/n256/b4` | 13.3377 | - | 13.3756 |
| `householder_factor/n512/b1` | 27.5210 | - | 22.9721 |
| `householder_factor/n512/b4` | 111.3338 | - | 90.9522 |
| `lu/n256/b1` | 1.2651 | - | 1.6101 |
| `lu/n256/b4` | 5.1698 | - | 6.7473 |
| `lu/n512/b1` | 8.6729 | - | 11.1354 |
| `lu/n512/b4` | 34.6499 | - | 44.5809 |
| `lu_factor/n256/b1` | 1.1220 | - | 1.5348 |
| `lu_factor/n256/b4` | 4.4849 | - | 6.2667 |
| `lu_factor/n512/b1` | 8.0279 | - | 10.3115 |
| `lu_factor/n512/b4` | 32.5523 | - | 42.1577 |
| `lu_factor_solve/n256/b1` | 1.1871 | - | 1.6523 |
| `lu_factor_solve/n256/b4` | 4.7477 | - | 6.8038 |
| `lu_factor_solve/n512/b1` | 8.2407 | - | 10.7533 |
| `lu_factor_solve/n512/b4` | 33.8510 | - | 43.2424 |
| `lu_solve_prepared/n256/b1` | 0.0622 | - | 0.1150 |
| `lu_solve_prepared/n256/b4` | 0.2627 | - | 0.5234 |
| `lu_solve_prepared/n512/b1` | 0.2217 | - | 0.4168 |
| `lu_solve_prepared/n512/b4` | 1.0663 | - | 2.1273 |
| `qr/n256/b1` | 6.2151 | - | 7.2864 |
| `qr/n256/b4` | 24.9313 | - | 28.9526 |
| `qr/n512/b1` | 42.3039 | - | 47.1943 |
| `qr/n512/b4` | 168.6610 | - | 188.5816 |
| `rank_revealing_qr/n256/b1` | 6.7387 | - | 10.3445 |
| `rank_revealing_qr/n256/b4` | 27.1077 | - | 41.7006 |
| `rank_revealing_qr/n512/b1` | 47.6703 | - | 65.1360 |
| `rank_revealing_qr/n512/b4` | 189.4771 | - | 258.1221 |
| `solve/n256/b1` | 1.1795 | - | 1.7211 |
| `solve/n256/b4` | 4.7006 | - | 6.7962 |
| `solve/n512/b1` | 8.1945 | - | 11.2240 |
| `solve/n512/b4` | 32.7081 | - | 43.7169 |
| `svd_thin/n256/b1` | 23.8388 | - | 27.0019 |
| `svd_thin/n256/b4` | 95.7926 | - | 114.7107 |
| `svd_thin/n512/b1` | 151.8001 | - | 188.2873 |
| `svd_thin/n512/b4` | 606.2961 | - | 772.8305 |
| `svd_values/n256/b1` | 11.7922 | - | 12.5380 |
| `svd_values/n256/b4` | 47.3535 | - | 52.7328 |
| `svd_values/n512/b1` | 68.6899 | - | 93.1021 |
| `svd_values/n512/b4` | 282.2816 | - | 393.5631 |
| `triangular_solve/n256/b1` | 0.0338 | - | 0.0675 |
| `triangular_solve/n256/b4` | 0.1470 | - | 0.2627 |
| `triangular_solve/n512/b1` | 0.1159 | - | 0.2410 |
| `triangular_solve/n512/b4` | 0.5898 | - | 1.0295 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6883 | 0.4842 | 0.3410 |
| `cholesky/n256/b4` | 2.7840 | 1.9869 | 1.3775 |
| `cholesky/n512/b1` | 4.7337 | 2.4312 | 1.9024 |
| `cholesky/n512/b4` | 19.5464 | 10.3457 | 9.1740 |
| `eigh/n256/b1` | 10.2779 | 7.9660 | 9.6690 |
| `eigh/n256/b4` | 41.2257 | 31.9844 | 38.6806 |
| `eigh/n512/b1` | 62.9705 | 28.7901 | 54.5879 |
| `eigh/n512/b4` | 251.4420 | 115.9593 | 219.6760 |
| `eigvalsh/n256/b1` | 18.2835 | 19.1830 | 3.9421 |
| `eigvalsh/n256/b4` | 73.6706 | 74.2074 | 15.8720 |
| `eigvalsh/n512/b1` | 132.8556 | 123.8135 | 21.4776 |
| `eigvalsh/n512/b4` | 531.9241 | 493.0119 | 85.8404 |
| `householder_apply/n256/b1` | 5.1171 | 5.1039 | 1.6769 |
| `householder_apply/n256/b4` | 21.2116 | 21.0649 | 6.8037 |
| `householder_apply/n512/b1` | 42.6925 | 42.5031 | 9.7201 |
| `householder_apply/n512/b4` | 170.8251 | 170.3867 | 39.3419 |
| `householder_factor/n256/b1` | 3.3357 | 3.3817 | 0.9427 |
| `householder_factor/n256/b4` | 13.3444 | 13.4597 | 3.7862 |
| `householder_factor/n512/b1` | 27.5028 | 27.5568 | 6.8225 |
| `householder_factor/n512/b4` | 111.3677 | 111.5633 | 27.4644 |
| `lu/n256/b1` | 1.2631 | 0.8462 | 0.5419 |
| `lu/n256/b4` | 5.1501 | 3.4902 | 2.3683 |
| `lu/n512/b1` | 8.6628 | 3.8761 | 3.8012 |
| `lu/n512/b4` | 34.5410 | 15.3603 | 14.6601 |
| `lu_factor/n256/b1` | 1.1100 | 0.6604 | 0.4339 |
| `lu_factor/n256/b4` | 4.4795 | 1.7213 | 1.7505 |
| `lu_factor/n512/b1` | 7.9809 | 3.0929 | 3.0524 |
| `lu_factor/n512/b4` | 32.6762 | 9.1014 | 12.2735 |
| `lu_factor_solve/n256/b1` | 1.1816 | 0.7305 | 0.4881 |
| `lu_factor_solve/n256/b4` | 4.7382 | 1.6144 | 1.9741 |
| `lu_factor_solve/n512/b1` | 8.1802 | 3.2394 | 3.2895 |
| `lu_factor_solve/n512/b4` | 33.5549 | 9.6029 | 13.3090 |
| `lu_solve_prepared/n256/b1` | 0.0629 | 0.0595 | 0.0520 |
| `lu_solve_prepared/n256/b4` | 0.2698 | 0.0709 | 0.2155 |
| `lu_solve_prepared/n512/b1` | 0.2083 | 0.1606 | 0.2015 |
| `lu_solve_prepared/n512/b4` | 1.1377 | 0.5602 | 1.2106 |
| `qr/n256/b1` | 6.1875 | 3.1373 | 2.7595 |
| `qr/n256/b4` | 24.7962 | 12.6440 | 11.2062 |
| `qr/n512/b1` | 42.1745 | 14.5552 | 16.7136 |
| `qr/n512/b4` | 169.6492 | 58.7082 | 67.8098 |
| `rank_revealing_qr/n256/b1` | 6.7130 | 3.7896 | 7.8336 |
| `rank_revealing_qr/n256/b4` | 27.0486 | 15.8562 | 31.5757 |
| `rank_revealing_qr/n512/b1` | 47.8753 | 16.7318 | 45.4940 |
| `rank_revealing_qr/n512/b4` | 192.0005 | 67.1783 | 181.1121 |
| `solve/n256/b1` | 1.1771 | 0.7454 | 0.5147 |
| `solve/n256/b4` | 4.7003 | 3.0062 | 2.1439 |
| `solve/n512/b1` | 8.1884 | 3.3577 | 3.2559 |
| `solve/n512/b4` | 32.5961 | 13.3075 | 13.8552 |
| `svd_thin/n256/b1` | 24.1620 | 15.0774 | 14.4577 |
| `svd_thin/n256/b4` | 95.5616 | 61.5374 | 57.5820 |
| `svd_thin/n512/b1` | 151.3103 | 66.5785 | 78.5365 |
| `svd_thin/n512/b4` | 606.0956 | 267.0067 | 330.0910 |
| `svd_values/n256/b1` | 11.8418 | 11.9387 | 7.3544 |
| `svd_values/n256/b4` | 47.5243 | 47.1353 | 31.7724 |
| `svd_values/n512/b1` | 68.9705 | 45.4565 | 36.1696 |
| `svd_values/n512/b4` | 285.8147 | 188.8654 | 175.0550 |
| `triangular_solve/n256/b1` | 0.0328 | 0.0332 | 0.0260 |
| `triangular_solve/n256/b4` | 0.1406 | 0.1305 | 0.1127 |
| `triangular_solve/n512/b1` | 0.1124 | 0.0842 | 0.1003 |
| `triangular_solve/n512/b4` | 0.5057 | 0.3722 | 0.5808 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6909 | 0.4731 | 0.2667 |
| `cholesky/n256/b4` | 2.8875 | 1.9666 | 1.1613 |
| `cholesky/n512/b1` | 4.7276 | 1.8132 | 1.0830 |
| `cholesky/n512/b4` | 19.7027 | 7.7017 | 5.3679 |
| `eigh/n256/b1` | 10.2498 | 7.0304 | 7.8065 |
| `eigh/n256/b4` | 41.3266 | 29.5709 | 31.7687 |
| `eigh/n512/b1` | 63.1546 | 24.1328 | 39.2703 |
| `eigh/n512/b4` | 253.0790 | 97.5320 | 157.7262 |
| `eigvalsh/n256/b1` | 18.3695 | 19.1768 | 3.5503 |
| `eigvalsh/n256/b4` | 73.4387 | 74.2050 | 14.3030 |
| `eigvalsh/n512/b1` | 133.1272 | 122.0654 | 17.4134 |
| `eigvalsh/n512/b4` | 533.3641 | 487.1132 | 69.6797 |
| `householder_apply/n256/b1` | 5.2447 | 5.2824 | 0.8643 |
| `householder_apply/n256/b4` | 21.4301 | 21.4664 | 3.6001 |
| `householder_apply/n512/b1` | 41.8649 | 41.8619 | 5.0593 |
| `householder_apply/n512/b4` | 173.6913 | 174.7808 | 20.6180 |
| `householder_factor/n256/b1` | 3.3280 | 3.3849 | 0.9494 |
| `householder_factor/n256/b4` | 13.3569 | 13.3806 | 3.8040 |
| `householder_factor/n512/b1` | 27.5217 | 27.4180 | 3.4164 |
| `householder_factor/n512/b4` | 111.0698 | 111.0064 | 13.5191 |
| `lu/n256/b1` | 1.2721 | 0.8387 | 0.4021 |
| `lu/n256/b4` | 5.0807 | 3.4626 | 1.7796 |
| `lu/n512/b1` | 8.7021 | 3.3253 | 2.3908 |
| `lu/n512/b4` | 34.7371 | 13.2863 | 9.5925 |
| `lu_factor/n256/b1` | 1.1083 | 0.6567 | 0.2893 |
| `lu_factor/n256/b4` | 4.4645 | 2.6410 | 1.1819 |
| `lu_factor/n512/b1` | 7.9789 | 2.5602 | 1.7185 |
| `lu_factor/n512/b4` | 32.5945 | 10.3110 | 6.9687 |
| `lu_factor_solve/n256/b1` | 1.1772 | 0.7277 | 0.3540 |
| `lu_factor_solve/n256/b4` | 4.7463 | 2.9624 | 1.4364 |
| `lu_factor_solve/n512/b1` | 8.2018 | 2.6853 | 1.9376 |
| `lu_factor_solve/n512/b4` | 33.5876 | 11.0430 | 8.0018 |
| `lu_solve_prepared/n256/b1` | 0.0630 | 0.0664 | 0.0523 |
| `lu_solve_prepared/n256/b4` | 0.2726 | 0.2786 | 0.2166 |
| `lu_solve_prepared/n512/b1` | 0.2222 | 0.1727 | 0.2024 |
| `lu_solve_prepared/n512/b4` | 1.3141 | 0.9775 | 1.2500 |
| `qr/n256/b1` | 6.2169 | 3.5160 | 2.2145 |
| `qr/n256/b4` | 24.9875 | 13.9691 | 8.9857 |
| `qr/n512/b1` | 42.3772 | 12.3694 | 9.2820 |
| `qr/n512/b4` | 169.3162 | 49.5414 | 38.3367 |
| `rank_revealing_qr/n256/b1` | 6.6979 | 3.8794 | 6.3652 |
| `rank_revealing_qr/n256/b4` | 27.0416 | 15.9644 | 25.6810 |
| `rank_revealing_qr/n512/b1` | 47.6072 | 12.1937 | 36.5922 |
| `rank_revealing_qr/n512/b4` | 190.6270 | 49.0564 | 145.9984 |
| `solve/n256/b1` | 1.1775 | 0.7404 | 0.3902 |
| `solve/n256/b4` | 4.7073 | 3.0161 | 1.6103 |
| `solve/n512/b1` | 8.1927 | 2.8704 | 2.0010 |
| `solve/n512/b4` | 32.7567 | 11.2757 | 8.4891 |
| `svd_thin/n256/b1` | 23.8756 | 14.4175 | 11.5755 |
| `svd_thin/n256/b4` | 96.8986 | 59.7382 | 46.2002 |
| `svd_thin/n512/b1` | 151.7312 | 55.8372 | 56.5785 |
| `svd_thin/n512/b4` | 607.3857 | 224.6560 | 239.8221 |
| `svd_values/n256/b1` | 11.7910 | 11.9851 | 6.5584 |
| `svd_values/n256/b4` | 47.2382 | 47.8080 | 27.1109 |
| `svd_values/n512/b1` | 68.3993 | 43.7014 | 28.7512 |
| `svd_values/n512/b4` | 281.8160 | 180.8051 | 130.1444 |
| `triangular_solve/n256/b1` | 0.0333 | 0.0370 | 0.0261 |
| `triangular_solve/n256/b4` | 0.1437 | 0.1469 | 0.1160 |
| `triangular_solve/n512/b1` | 0.1117 | 0.0903 | 0.0998 |
| `triangular_solve/n512/b4` | 0.5357 | 0.3854 | 0.6847 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5374 | - | 0.4441 |
| `householder_factor/4096x256/b1` | 41.6531 | - | 17.5295 |
| `qr/1024x64/b1` | 0.9742 | - | 0.9193 |
| `qr/4096x256/b1` | 41.0513 | - | 41.7591 |
| `rank_revealing_qr/1024x64/b1` | 0.9741 | - | 1.1878 |
| `rank_revealing_qr/4096x256/b1` | 64.6424 | - | 61.8952 |
| `svd_thin/1024x64/b1` | 1.4590 | - | 2.2669 |
| `svd_thin/4096x256/b1` | 72.1545 | - | 76.9075 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5362 | 0.5438 | 0.2375 |
| `householder_factor/4096x256/b1` | 42.1032 | 42.4024 | 6.7007 |
| `qr/1024x64/b1` | 0.9771 | 0.8749 | 0.5714 |
| `qr/4096x256/b1` | 41.6493 | 20.4525 | 16.0959 |
| `rank_revealing_qr/1024x64/b1` | 0.9705 | 0.7393 | 1.0198 |
| `rank_revealing_qr/4096x256/b1` | 66.0220 | 24.2217 | 41.8014 |
| `svd_thin/1024x64/b1` | 1.4524 | 1.3636 | 1.7108 |
| `svd_thin/4096x256/b1` | 72.6085 | 40.7069 | 47.7379 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5367 | 0.5450 | 0.1686 |
| `householder_factor/4096x256/b1` | 41.8368 | 41.9476 | 3.7908 |
| `qr/1024x64/b1` | 0.9789 | 1.1276 | 0.5002 |
| `qr/4096x256/b1` | 41.9986 | 19.6002 | 11.4653 |
| `rank_revealing_qr/1024x64/b1` | 0.9742 | 0.7624 | 1.0086 |
| `rank_revealing_qr/4096x256/b1` | 65.9588 | 18.6717 | 39.0679 |
| `svd_thin/1024x64/b1` | 1.4554 | 1.6524 | 1.5618 |
| `svd_thin/4096x256/b1` | 72.9310 | 34.4666 | 41.3333 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1681 | - | 1.3235 |
| `householder_factor/4096x256/b1` | 121.5056 | - | 66.4083 |
| `qr/1024x64/b1` | 2.8762 | - | 2.8470 |
| `qr/4096x256/b1` | 146.9377 | - | 135.5811 |
| `rank_revealing_qr/1024x64/b1` | 2.8610 | - | 3.8741 |
| `rank_revealing_qr/4096x256/b1` | 244.3036 | - | 185.0718 |
| `svd_thin/1024x64/b1` | 3.5349 | - | 5.6413 |
| `svd_thin/4096x256/b1` | 230.9942 | - | 251.2919 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1685 | 1.1946 | 0.7869 |
| `householder_factor/4096x256/b1` | 120.6700 | 121.3590 | 19.5138 |
| `qr/1024x64/b1` | 2.8614 | 1.6091 | 1.8031 |
| `qr/4096x256/b1` | 147.9680 | 57.7896 | 46.5903 |
| `rank_revealing_qr/1024x64/b1` | 2.8433 | 1.7597 | 3.1611 |
| `rank_revealing_qr/4096x256/b1` | 243.3747 | 83.3592 | 128.8287 |
| `svd_thin/1024x64/b1` | 3.5628 | 2.2982 | 3.8307 |
| `svd_thin/4096x256/b1` | 232.2037 | 103.6844 | 113.8259 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1712 | 1.2040 | 0.4823 |
| `householder_factor/4096x256/b1` | 121.9635 | 122.1131 | 11.0893 |
| `qr/1024x64/b1` | 2.8554 | 1.7627 | 1.3214 |
| `qr/4096x256/b1` | 147.2467 | 46.5744 | 28.4018 |
| `rank_revealing_qr/1024x64/b1` | 2.8510 | 1.7231 | 2.9579 |
| `rank_revealing_qr/4096x256/b1` | 245.3394 | 52.8089 | 114.4083 |
| `svd_thin/1024x64/b1` | 3.5352 | 2.4867 | 3.2252 |
| `svd_thin/4096x256/b1` | 232.2430 | 75.7346 | 82.1590 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
