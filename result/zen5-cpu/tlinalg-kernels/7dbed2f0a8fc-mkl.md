<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261011T061457Z-mkl-pin/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `7dbed2f0a8fce26577e358c21433eace8fd72ecb`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
- harness commit: `b644d9588cda5b07e6609dee6cc5147080be397c`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-11T07:12:36.612342Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor mkl --checkout /tmp/tl-pin --aa 1 --label mkl-pin`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261011T061457Z-mkl-pin/`

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
| `cholesky/n16/b1024` | 0.5659 | - | 0.6327 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1067 | - | 0.0729 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2137 | - | 0.1910 |
| `eig/n16/b1` | 0.0568 | - | 0.0340 |
| `eig/n16/b1024` | 60.9495 | - | 37.0084 |
| `eig/n4/b1` | 0.0043 | - | 0.0027 |
| `eig/n4/b1024` | 3.7943 | - | 1.9919 |
| `eig/n8/b1` | 0.0150 | - | 0.0086 |
| `eig/n8/b1024` | 14.5083 | - | 7.8922 |
| `eigh/n16/b1` | 0.0176 | - | 0.0136 |
| `eigh/n16/b1024` | 17.8152 | - | 14.1150 |
| `eigh/n4/b1` | 0.0016 | - | 0.0020 |
| `eigh/n4/b1024` | 1.4201 | - | 1.7344 |
| `eigh/n8/b1` | 0.0051 | - | 0.0049 |
| `eigh/n8/b1024` | 5.0136 | - | 4.6876 |
| `eigvals/n16/b1` | 0.0404 | - | 0.0244 |
| `eigvals/n16/b1024` | 41.9668 | - | 24.6922 |
| `eigvals/n4/b1` | 0.0026 | - | 0.0023 |
| `eigvals/n4/b1024` | 2.1445 | - | 1.5333 |
| `eigvals/n8/b1` | 0.0105 | - | 0.0070 |
| `eigvals/n8/b1024` | 9.9649 | - | 6.1976 |
| `eigvalsh/n16/b1` | 0.0197 | - | 0.0078 |
| `eigvalsh/n16/b1024` | 20.4568 | - | 7.8379 |
| `eigvalsh/n4/b1` | 0.0019 | - | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5548 | - | 0.8952 |
| `eigvalsh/n8/b1` | 0.0058 | - | 0.0030 |
| `eigvalsh/n8/b1024` | 5.3541 | - | 2.6690 |
| `full_piv_lu/n16/b1` | 0.0026 | - | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.0951 | - | 2.3347 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2302 | - | 0.2472 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6587 | - | 0.5727 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | - | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0449 | - | 3.4806 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | - | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3019 | - | 0.6652 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7351 | - | 1.1588 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0018 |
| `householder_apply/n16/b1024` | 2.6649 | - | 1.6162 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.1827 | - | 0.2086 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0008 |
| `householder_apply/n8/b1024` | 0.6362 | - | 0.4768 |
| `householder_factor/n16/b1` | 0.0021 | - | 0.0018 |
| `householder_factor/n16/b1024` | 2.0804 | - | 1.7683 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0003 |
| `householder_factor/n4/b1024` | 0.2359 | - | 0.1850 |
| `householder_factor/n8/b1` | 0.0007 | - | 0.0006 |
| `householder_factor/n8/b1024` | 0.6653 | - | 0.5048 |
| `lu/n16/b1` | 0.0021 | - | 0.0012 |
| `lu/n16/b1024` | 1.6811 | - | 1.0122 |
| `lu/n4/b1` | 0.0004 | - | 0.0003 |
| `lu/n4/b1024` | 0.1777 | - | 0.1031 |
| `lu/n8/b1` | 0.0007 | - | 0.0005 |
| `lu/n8/b1024` | 0.5186 | - | 0.3131 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0007 |
| `lu_factor/n16/b1024` | 1.0871 | - | 0.7625 |
| `lu_factor/n4/b1` | 0.0003 | - | 0.0001 |
| `lu_factor/n4/b1024` | 0.1308 | - | 0.0398 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0002 |
| `lu_factor/n8/b1024` | 0.3446 | - | 0.1583 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4309 | - | 1.3897 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1675 | - | 0.1086 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4718 | - | 0.4961 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3581 | - | 0.6326 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0405 | - | 0.0804 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1364 | - | 0.3552 |
| `qr/n16/b1` | 0.0056 | - | 0.0034 |
| `qr/n16/b1024` | 5.3533 | - | 3.1970 |
| `qr/n4/b1` | 0.0006 | - | 0.0007 |
| `qr/n4/b1024` | 0.4304 | - | 0.4207 |
| `qr/n8/b1` | 0.0016 | - | 0.0013 |
| `qr/n8/b1024` | 1.4030 | - | 1.0204 |
| `rank_revealing_qr/n16/b1` | 0.0066 | - | 0.0054 |
| `rank_revealing_qr/n16/b1024` | 6.1052 | - | 4.9960 |
| `rank_revealing_qr/n4/b1` | 0.0010 | - | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.6898 | - | 0.7389 |
| `rank_revealing_qr/n8/b1` | 0.0022 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8586 | - | 1.7898 |
| `solve/n16/b1` | 0.0022 | - | 0.0018 |
| `solve/n16/b1024` | 1.5651 | - | 1.4646 |
| `solve/n4/b1` | 0.0006 | - | 0.0003 |
| `solve/n4/b1024` | 0.2207 | - | 0.1407 |
| `solve/n8/b1` | 0.0010 | - | 0.0007 |
| `solve/n8/b1024` | 0.5481 | - | 0.5374 |
| `svd_full/n16/b1` | 0.0325 | - | 0.0337 |
| `svd_full/n16/b1024` | 33.2495 | - | 35.9269 |
| `svd_full/n4/b1` | 0.0028 | - | 0.0044 |
| `svd_full/n4/b1024` | 2.4936 | - | 3.9251 |
| `svd_full/n8/b1` | 0.0090 | - | 0.0119 |
| `svd_full/n8/b1024` | 8.9926 | - | 11.9607 |
| `svd_thin/n16/b1` | 0.0327 | - | 0.0340 |
| `svd_thin/n16/b1024` | 33.5789 | - | 36.0276 |
| `svd_thin/n4/b1` | 0.0027 | - | 0.0044 |
| `svd_thin/n4/b1024` | 2.4810 | - | 3.9358 |
| `svd_thin/n8/b1` | 0.0089 | - | 0.0119 |
| `svd_thin/n8/b1024` | 8.9671 | - | 12.0095 |
| `svd_values/n16/b1` | 0.0268 | - | 0.0143 |
| `svd_values/n16/b1024` | 28.1535 | - | 15.2546 |
| `svd_values/n4/b1` | 0.0025 | - | 0.0024 |
| `svd_values/n4/b1024` | 2.1565 | - | 1.8602 |
| `svd_values/n8/b1` | 0.0079 | - | 0.0052 |
| `svd_values/n8/b1024` | 7.5921 | - | 4.8680 |
| `triangular_solve/n16/b1` | 0.0005 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3016 | - | 0.3444 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0514 | - | 0.1739 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1299 | - | 0.2303 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0022 | 0.0007 |
| `cholesky/n16/b1024` | 0.5782 | 0.2778 | 0.6331 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1059 | 0.0569 | 0.0708 |
| `cholesky/n8/b1` | 0.0003 | 0.0027 | 0.0003 |
| `cholesky/n8/b1024` | 0.2138 | 0.1122 | 0.1867 |
| `eig/n16/b1` | 0.0563 | 0.0596 | 0.0338 |
| `eig/n16/b1024` | 60.8487 | 19.2418 | 36.6755 |
| `eig/n4/b1` | 0.0043 | 0.0068 | 0.0027 |
| `eig/n4/b1024` | 3.7755 | 2.0492 | 1.9987 |
| `eig/n8/b1` | 0.0155 | 0.0181 | 0.0085 |
| `eig/n8/b1024` | 14.4753 | 7.9815 | 7.8326 |
| `eigh/n16/b1` | 0.0176 | 0.0205 | 0.0136 |
| `eigh/n16/b1024` | 17.7308 | 4.4723 | 14.0984 |
| `eigh/n4/b1` | 0.0016 | 0.0038 | 0.0020 |
| `eigh/n4/b1024` | 1.4375 | 0.7255 | 1.6824 |
| `eigh/n8/b1` | 0.0051 | 0.0074 | 0.0048 |
| `eigh/n8/b1024` | 5.0460 | 2.0594 | 4.6714 |
| `eigvals/n16/b1` | 0.0404 | 0.0436 | 0.0244 |
| `eigvals/n16/b1024` | 42.0416 | 13.1643 | 24.7155 |
| `eigvals/n4/b1` | 0.0026 | 0.0054 | 0.0023 |
| `eigvals/n4/b1024` | 2.1524 | 1.2346 | 1.5290 |
| `eigvals/n8/b1` | 0.0106 | 0.0137 | 0.0070 |
| `eigvals/n8/b1024` | 9.9952 | 3.7698 | 6.2069 |
| `eigvalsh/n16/b1` | 0.0198 | 0.0241 | 0.0078 |
| `eigvalsh/n16/b1024` | 20.4131 | 10.8968 | 7.8241 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0035 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5552 | 1.0633 | 0.8870 |
| `eigvalsh/n8/b1` | 0.0058 | 0.0073 | 0.0029 |
| `eigvalsh/n8/b1024` | 5.3495 | 2.9790 | 2.6750 |
| `full_piv_lu/n16/b1` | 0.0026 | 0.0050 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.0578 | 0.5670 | 2.3639 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0027 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2316 | 0.0628 | 0.2449 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0037 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6510 | 0.3339 | 0.5667 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0049 | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0577 | 0.7806 | 3.4563 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0025 | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3006 | 0.1621 | 0.6589 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0037 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7371 | 0.3738 | 1.1776 |
| `householder_apply/n16/b1` | 0.0026 | 0.0050 | 0.0018 |
| `householder_apply/n16/b1024` | 2.7026 | 0.6744 | 1.6121 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0004 |
| `householder_apply/n4/b1024` | 0.1768 | 0.0532 | 0.1952 |
| `householder_apply/n8/b1` | 0.0007 | 0.0024 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6260 | 0.1693 | 0.4714 |
| `householder_factor/n16/b1` | 0.0021 | 0.0047 | 0.0018 |
| `householder_factor/n16/b1024` | 2.0984 | 0.5303 | 1.7697 |
| `householder_factor/n4/b1` | 0.0003 | 0.0025 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2363 | 0.0650 | 0.1843 |
| `householder_factor/n8/b1` | 0.0007 | 0.0035 | 0.0006 |
| `householder_factor/n8/b1024` | 0.6621 | 0.1733 | 0.5028 |
| `lu/n16/b1` | 0.0021 | 0.0044 | 0.0011 |
| `lu/n16/b1024` | 1.6812 | 0.8577 | 1.1125 |
| `lu/n4/b1` | 0.0004 | 0.0026 | 0.0003 |
| `lu/n4/b1024` | 0.1774 | 0.0480 | 0.1018 |
| `lu/n8/b1` | 0.0007 | 0.0034 | 0.0004 |
| `lu/n8/b1024` | 0.5191 | 0.2586 | 0.2935 |
| `lu_factor/n16/b1` | 0.0013 | 0.0031 | 0.0007 |
| `lu_factor/n16/b1024` | 1.0924 | 0.5677 | 0.7376 |
| `lu_factor/n4/b1` | 0.0004 | 0.0020 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1347 | 0.0403 | 0.0393 |
| `lu_factor/n8/b1` | 0.0006 | 0.0023 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3534 | 0.0952 | 0.1557 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0042 | 0.0016 |
| `lu_factor_solve/n16/b1024` | 1.4542 | 0.3742 | 1.4006 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0021 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1626 | 0.0883 | 0.1084 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0033 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4840 | 0.1281 | 0.4938 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0026 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3587 | 0.1046 | 0.6426 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0397 | 0.0203 | 0.0787 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0023 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1371 | 0.0458 | 0.3517 |
| `qr/n16/b1` | 0.0055 | 0.0081 | 0.0033 |
| `qr/n16/b1024` | 5.1791 | 2.6355 | 3.1684 |
| `qr/n4/b1` | 0.0007 | 0.0024 | 0.0007 |
| `qr/n4/b1024` | 0.4308 | 0.2216 | 0.4137 |
| `qr/n8/b1` | 0.0016 | 0.0040 | 0.0013 |
| `qr/n8/b1024` | 1.4102 | 0.6957 | 1.0059 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0088 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.0611 | 3.0245 | 4.9484 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0025 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.6836 | 0.3431 | 0.7245 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0047 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8347 | 0.9295 | 1.7473 |
| `solve/n16/b1` | 0.0021 | 0.0037 | 0.0018 |
| `solve/n16/b1024` | 1.5781 | 0.4017 | 1.5581 |
| `solve/n4/b1` | 0.0006 | 0.0027 | 0.0003 |
| `solve/n4/b1024` | 0.2190 | 0.1115 | 0.1408 |
| `solve/n8/b1` | 0.0010 | 0.0035 | 0.0007 |
| `solve/n8/b1024` | 0.5393 | 0.1729 | 0.5352 |
| `svd_full/n16/b1` | 0.0327 | 0.0361 | 0.0338 |
| `svd_full/n16/b1024` | 33.4227 | 8.5212 | 35.6868 |
| `svd_full/n4/b1` | 0.0027 | 0.0050 | 0.0044 |
| `svd_full/n4/b1024` | 2.5078 | 1.2561 | 3.8848 |
| `svd_full/n8/b1` | 0.0089 | 0.0117 | 0.0118 |
| `svd_full/n8/b1024` | 8.9638 | 4.5526 | 11.8985 |
| `svd_thin/n16/b1` | 0.0327 | 0.0366 | 0.0337 |
| `svd_thin/n16/b1024` | 33.3030 | 11.7337 | 35.9315 |
| `svd_thin/n4/b1` | 0.0028 | 0.0059 | 0.0044 |
| `svd_thin/n4/b1024` | 2.4971 | 0.6290 | 3.8856 |
| `svd_thin/n8/b1` | 0.0089 | 0.0116 | 0.0118 |
| `svd_thin/n8/b1024` | 8.9951 | 2.3236 | 11.8849 |
| `svd_values/n16/b1` | 0.0267 | 0.0299 | 0.0142 |
| `svd_values/n16/b1024` | 28.0384 | 10.8179 | 15.2386 |
| `svd_values/n4/b1` | 0.0025 | 0.0056 | 0.0024 |
| `svd_values/n4/b1024` | 2.1556 | 0.7587 | 1.8634 |
| `svd_values/n8/b1` | 0.0077 | 0.0107 | 0.0051 |
| `svd_values/n8/b1024` | 7.5830 | 2.9666 | 4.8587 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0027 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3015 | 0.1549 | 0.3530 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0028 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0512 | 0.0289 | 0.1764 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0028 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1299 | 0.0687 | 0.2300 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0037 | 0.0007 |
| `cholesky/n16/b1024` | 0.5600 | 0.0732 | 0.6357 |
| `cholesky/n4/b1` | 0.0002 | 0.0024 | 0.0002 |
| `cholesky/n4/b1024` | 0.1068 | 0.0217 | 0.0707 |
| `cholesky/n8/b1` | 0.0003 | 0.0036 | 0.0003 |
| `cholesky/n8/b1024` | 0.2225 | 0.0364 | 0.1892 |
| `eig/n16/b1` | 0.0569 | 0.0614 | 0.0338 |
| `eig/n16/b1024` | 60.7633 | 12.0735 | 36.7940 |
| `eig/n4/b1` | 0.0042 | 0.0073 | 0.0027 |
| `eig/n4/b1024` | 3.7798 | 0.7384 | 1.9954 |
| `eig/n8/b1` | 0.0152 | 0.0184 | 0.0085 |
| `eig/n8/b1024` | 14.4787 | 4.9864 | 7.8652 |
| `eigh/n16/b1` | 0.0175 | 0.0205 | 0.0136 |
| `eigh/n16/b1024` | 17.7133 | 4.4814 | 14.0762 |
| `eigh/n4/b1` | 0.0016 | 0.0050 | 0.0020 |
| `eigh/n4/b1024` | 1.4285 | 0.3644 | 1.6976 |
| `eigh/n8/b1` | 0.0051 | 0.0080 | 0.0048 |
| `eigh/n8/b1024` | 5.0393 | 0.6376 | 4.6405 |
| `eigvals/n16/b1` | 0.0400 | 0.0436 | 0.0243 |
| `eigvals/n16/b1024` | 42.0813 | 8.3063 | 24.7373 |
| `eigvals/n4/b1` | 0.0026 | 0.0057 | 0.0023 |
| `eigvals/n4/b1024` | 2.1522 | 0.5289 | 1.5308 |
| `eigvals/n8/b1` | 0.0106 | 0.0136 | 0.0070 |
| `eigvals/n8/b1024` | 10.0568 | 2.4257 | 6.2058 |
| `eigvalsh/n16/b1` | 0.0197 | 0.0229 | 0.0078 |
| `eigvalsh/n16/b1024` | 20.2986 | 9.2278 | 7.7886 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0048 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5570 | 0.7134 | 0.8849 |
| `eigvalsh/n8/b1` | 0.0057 | 0.0079 | 0.0030 |
| `eigvalsh/n8/b1024` | 5.3471 | 2.4021 | 2.6439 |
| `full_piv_lu/n16/b1` | 0.0026 | 0.0057 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.1016 | 0.2871 | 2.4001 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0022 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2285 | 0.0631 | 0.2483 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0042 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6676 | 0.1747 | 0.5694 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0058 | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0353 | 0.5041 | 3.5074 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0026 | 0.0010 |
| `full_piv_lu_solve/n4/b1024` | 0.3003 | 0.0487 | 0.6540 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0040 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7426 | 0.1898 | 1.1763 |
| `householder_apply/n16/b1` | 0.0026 | 0.0048 | 0.0018 |
| `householder_apply/n16/b1024` | 2.5521 | 0.3381 | 1.5948 |
| `householder_apply/n4/b1` | 0.0003 | 0.0021 | 0.0004 |
| `householder_apply/n4/b1024` | 0.1734 | 0.0484 | 0.1937 |
| `householder_apply/n8/b1` | 0.0008 | 0.0037 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6472 | 0.1618 | 0.4778 |
| `householder_factor/n16/b1` | 0.0020 | 0.0046 | 0.0018 |
| `householder_factor/n16/b1024` | 2.0302 | 0.5222 | 1.7694 |
| `householder_factor/n4/b1` | 0.0003 | 0.0033 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2375 | 0.0645 | 0.1828 |
| `householder_factor/n8/b1` | 0.0007 | 0.0031 | 0.0006 |
| `householder_factor/n8/b1024` | 0.6654 | 0.1756 | 0.5022 |
| `lu/n16/b1` | 0.0021 | 0.0051 | 0.0011 |
| `lu/n16/b1024` | 1.7012 | 0.2223 | 1.0109 |
| `lu/n4/b1` | 0.0004 | 0.0039 | 0.0003 |
| `lu/n4/b1024` | 0.1732 | 0.0489 | 0.1016 |
| `lu/n8/b1` | 0.0007 | 0.0040 | 0.0005 |
| `lu/n8/b1024` | 0.5123 | 0.0694 | 0.2919 |
| `lu_factor/n16/b1` | 0.0013 | 0.0044 | 0.0007 |
| `lu_factor/n16/b1024` | 1.1170 | 0.2813 | 0.7229 |
| `lu_factor/n4/b1` | 0.0003 | 0.0031 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1366 | 0.0401 | 0.0390 |
| `lu_factor/n8/b1` | 0.0006 | 0.0040 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3556 | 0.0965 | 0.1562 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0049 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4605 | 0.3614 | 1.3816 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0032 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1656 | 0.0326 | 0.1078 |
| `lu_factor_solve/n8/b1` | 0.0008 | 0.0040 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4897 | 0.1264 | 0.4953 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0039 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3571 | 0.1046 | 0.6223 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0024 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | 0.0189 | 0.0790 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0032 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1366 | 0.0330 | 0.3529 |
| `qr/n16/b1` | 0.0055 | 0.0080 | 0.0034 |
| `qr/n16/b1024` | 5.2527 | 0.6741 | 3.1741 |
| `qr/n4/b1` | 0.0007 | 0.0036 | 0.0007 |
| `qr/n4/b1024` | 0.4355 | 0.0705 | 0.4144 |
| `qr/n8/b1` | 0.0016 | 0.0048 | 0.0013 |
| `qr/n8/b1024` | 1.4070 | 0.3448 | 1.0239 |
| `rank_revealing_qr/n16/b1` | 0.0063 | 0.0096 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.0116 | 0.7740 | 4.9665 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0035 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7113 | 0.1790 | 0.7220 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0054 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8677 | 0.4657 | 1.7549 |
| `solve/n16/b1` | 0.0021 | 0.0047 | 0.0018 |
| `solve/n16/b1024` | 1.5192 | 0.4002 | 1.5011 |
| `solve/n4/b1` | 0.0006 | 0.0037 | 0.0003 |
| `solve/n4/b1024` | 0.2182 | 0.0392 | 0.1419 |
| `solve/n8/b1` | 0.0010 | 0.0037 | 0.0007 |
| `solve/n8/b1024` | 0.5402 | 0.0751 | 0.5313 |
| `svd_full/n16/b1` | 0.0326 | 0.0360 | 0.0337 |
| `svd_full/n16/b1024` | 33.3846 | 4.3205 | 36.1165 |
| `svd_full/n4/b1` | 0.0028 | 0.0056 | 0.0044 |
| `svd_full/n4/b1024` | 2.4901 | 0.6282 | 3.8961 |
| `svd_full/n8/b1` | 0.0089 | 0.0113 | 0.0117 |
| `svd_full/n8/b1024` | 9.0002 | 1.8001 | 11.9494 |
| `svd_thin/n16/b1` | 0.0327 | 0.0365 | 0.0338 |
| `svd_thin/n16/b1024` | 33.3777 | 4.3399 | 35.7885 |
| `svd_thin/n4/b1` | 0.0027 | 0.0059 | 0.0044 |
| `svd_thin/n4/b1024` | 2.4789 | 0.6299 | 3.8901 |
| `svd_thin/n8/b1` | 0.0089 | 0.0114 | 0.0119 |
| `svd_thin/n8/b1024` | 9.0554 | 1.1829 | 11.9372 |
| `svd_values/n16/b1` | 0.0268 | 0.0301 | 0.0144 |
| `svd_values/n16/b1024` | 27.8461 | 7.9546 | 15.2935 |
| `svd_values/n4/b1` | 0.0025 | 0.0060 | 0.0023 |
| `svd_values/n4/b1024` | 2.1531 | 0.7673 | 1.8412 |
| `svd_values/n8/b1` | 0.0077 | 0.0107 | 0.0051 |
| `svd_values/n8/b1024` | 7.5742 | 1.9737 | 4.8696 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0024 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3023 | 0.0796 | 0.3646 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0514 | 0.0169 | 0.1909 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0026 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1303 | 0.0368 | 0.2322 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0011 |
| `cholesky/n16/b1024` | 0.8050 | - | 1.1152 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1163 | - | 0.1078 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2619 | - | 0.2823 |
| `eig/n16/b1` | 0.0756 | - | 0.1033 |
| `eig/n16/b1024` | 82.9538 | - | 112.3729 |
| `eig/n4/b1` | 0.0065 | - | 0.0085 |
| `eig/n4/b1024` | 6.1637 | - | 7.7945 |
| `eig/n8/b1` | 0.0209 | - | 0.0264 |
| `eig/n8/b1024` | 21.4917 | - | 26.9965 |
| `eigh/n16/b1` | 0.0180 | - | 0.0187 |
| `eigh/n16/b1024` | 19.4257 | - | 19.6261 |
| `eigh/n4/b1` | 0.0020 | - | 0.0020 |
| `eigh/n4/b1024` | 1.7243 | - | 1.7403 |
| `eigh/n8/b1` | 0.0056 | - | 0.0055 |
| `eigh/n8/b1024` | 5.4389 | - | 5.4409 |
| `eigvals/n16/b1` | 0.0476 | - | 0.0724 |
| `eigvals/n16/b1024` | 52.7842 | - | 81.1417 |
| `eigvals/n4/b1` | 0.0038 | - | 0.0069 |
| `eigvals/n4/b1024` | 3.4015 | - | 6.0765 |
| `eigvals/n8/b1` | 0.0132 | - | 0.0211 |
| `eigvals/n8/b1024` | 13.3021 | - | 21.6764 |
| `eigvalsh/n16/b1` | 0.0208 | - | 0.0111 |
| `eigvalsh/n16/b1024` | 23.5203 | - | 11.1310 |
| `eigvalsh/n4/b1` | 0.0023 | - | 0.0014 |
| `eigvalsh/n4/b1024` | 1.8648 | - | 1.0884 |
| `eigvalsh/n8/b1` | 0.0063 | - | 0.0036 |
| `eigvalsh/n8/b1024` | 5.8518 | - | 3.3611 |
| `full_piv_lu/n16/b1` | 0.0031 | - | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.7703 | - | 3.6198 |
| `full_piv_lu/n4/b1` | 0.0007 | - | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2754 | - | 0.3134 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7434 | - | 0.7362 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | - | 0.0054 |
| `full_piv_lu_solve/n16/b1024` | 3.3237 | - | 5.1383 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4510 | - | 0.9639 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0023 |
| `full_piv_lu_solve/n8/b1024` | 1.1385 | - | 1.9184 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0036 |
| `householder_apply/n16/b1024` | 3.3415 | - | 3.9796 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.1770 | - | 0.2570 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0010 |
| `householder_apply/n8/b1024` | 0.6195 | - | 0.7867 |
| `householder_factor/n16/b1` | 0.0026 | - | 0.0037 |
| `householder_factor/n16/b1024` | 2.5728 | - | 3.7810 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.3075 | - | 0.3082 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.8279 | - | 0.8881 |
| `lu/n16/b1` | 0.0022 | - | 0.0022 |
| `lu/n16/b1024` | 1.9190 | - | 2.2690 |
| `lu/n4/b1` | 0.0005 | - | 0.0004 |
| `lu/n4/b1024` | 0.2121 | - | 0.1746 |
| `lu/n8/b1` | 0.0008 | - | 0.0007 |
| `lu/n8/b1024` | 0.5369 | - | 0.5444 |
| `lu_factor/n16/b1` | 0.0014 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2006 | - | 1.6108 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1615 | - | 0.1106 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3904 | - | 0.3713 |
| `lu_factor_solve/n16/b1` | 0.0025 | - | 0.0032 |
| `lu_factor_solve/n16/b1024` | 2.0550 | - | 3.1965 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2624 | - | 0.2490 |
| `lu_factor_solve/n8/b1` | 0.0010 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.7060 | - | 0.9998 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7817 | - | 1.5777 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0969 | - | 0.1450 |
| `lu_solve_prepared/n8/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2889 | - | 0.6423 |
| `qr/n16/b1` | 0.0067 | - | 0.0064 |
| `qr/n16/b1024` | 6.6588 | - | 6.4035 |
| `qr/n4/b1` | 0.0007 | - | 0.0009 |
| `qr/n4/b1024` | 0.5081 | - | 0.5771 |
| `qr/n8/b1` | 0.0018 | - | 0.0019 |
| `qr/n8/b1024` | 1.5660 | - | 1.6019 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0095 |
| `rank_revealing_qr/n16/b1024` | 7.3325 | - | 9.7019 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8224 | - | 1.0814 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1988 | - | 2.8447 |
| `solve/n16/b1` | 0.0029 | - | 0.0035 |
| `solve/n16/b1024` | 2.1601 | - | 3.3447 |
| `solve/n4/b1` | 0.0007 | - | 0.0005 |
| `solve/n4/b1024` | 0.3157 | - | 0.2882 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7617 | - | 1.0623 |
| `svd_full/n16/b1` | 0.0346 | - | 0.0435 |
| `svd_full/n16/b1024` | 36.5407 | - | 49.0734 |
| `svd_full/n4/b1` | 0.0030 | - | 0.0053 |
| `svd_full/n4/b1024` | 2.9775 | - | 4.8114 |
| `svd_full/n8/b1` | 0.0097 | - | 0.0141 |
| `svd_full/n8/b1024` | 10.0634 | - | 14.3474 |
| `svd_thin/n16/b1` | 0.0355 | - | 0.0433 |
| `svd_thin/n16/b1024` | 36.5782 | - | 48.9176 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_thin/n4/b1024` | 2.9828 | - | 4.7774 |
| `svd_thin/n8/b1` | 0.0096 | - | 0.0140 |
| `svd_thin/n8/b1024` | 10.0626 | - | 14.3548 |
| `svd_values/n16/b1` | 0.0296 | - | 0.0203 |
| `svd_values/n16/b1024` | 32.9838 | - | 22.7614 |
| `svd_values/n4/b1` | 0.0029 | - | 0.0029 |
| `svd_values/n4/b1024` | 2.6391 | - | 2.4439 |
| `svd_values/n8/b1` | 0.0087 | - | 0.0068 |
| `svd_values/n8/b1024` | 8.8062 | - | 6.5440 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6001 | - | 0.8646 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0958 | - | 0.1781 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2371 | - | 0.3457 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0034 | 0.0011 |
| `cholesky/n16/b1024` | 0.8129 | 0.4112 | 1.1297 |
| `cholesky/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1174 | 0.0353 | 0.1068 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2489 | 0.1311 | 0.2825 |
| `eig/n16/b1` | 0.0751 | 0.0800 | 0.0993 |
| `eig/n16/b1024` | 83.4342 | 24.6368 | 108.2838 |
| `eig/n4/b1` | 0.0063 | 0.0096 | 0.0084 |
| `eig/n4/b1024` | 6.1129 | 3.6593 | 7.7980 |
| `eig/n8/b1` | 0.0208 | 0.0244 | 0.0263 |
| `eig/n8/b1024` | 21.4501 | 6.7474 | 27.0982 |
| `eigh/n16/b1` | 0.0179 | 0.0211 | 0.0186 |
| `eigh/n16/b1024` | 19.4293 | 5.4179 | 19.4821 |
| `eigh/n4/b1` | 0.0019 | 0.0044 | 0.0020 |
| `eigh/n4/b1024` | 1.7199 | 0.8707 | 1.6880 |
| `eigh/n8/b1` | 0.0056 | 0.0088 | 0.0054 |
| `eigh/n8/b1024` | 5.4200 | 2.7514 | 5.3555 |
| `eigvals/n16/b1` | 0.0468 | 0.0504 | 0.0725 |
| `eigvals/n16/b1024` | 51.8170 | 17.9274 | 80.6831 |
| `eigvals/n4/b1` | 0.0035 | 0.0053 | 0.0068 |
| `eigvals/n4/b1024` | 3.1365 | 2.0890 | 6.0659 |
| `eigvals/n8/b1` | 0.0128 | 0.0153 | 0.0211 |
| `eigvals/n8/b1024` | 12.8010 | 4.9700 | 21.6647 |
| `eigvalsh/n16/b1` | 0.0206 | 0.0257 | 0.0109 |
| `eigvalsh/n16/b1024` | 23.3800 | 13.2447 | 11.0555 |
| `eigvalsh/n4/b1` | 0.0022 | 0.0049 | 0.0014 |
| `eigvalsh/n4/b1024` | 1.8568 | 1.1857 | 1.0820 |
| `eigvalsh/n8/b1` | 0.0064 | 0.0095 | 0.0036 |
| `eigvalsh/n8/b1024` | 5.8310 | 3.1439 | 3.3339 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0056 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.8022 | 1.2437 | 3.4504 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0029 | 0.0006 |
| `full_piv_lu/n4/b1024` | 0.2756 | 0.0724 | 0.3112 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0036 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7602 | 0.3737 | 0.7339 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0061 | 0.0052 |
| `full_piv_lu_solve/n16/b1024` | 3.1669 | 0.8155 | 5.1049 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0034 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4704 | 0.1209 | 0.9583 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0041 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1617 | 0.3043 | 1.9269 |
| `householder_apply/n16/b1` | 0.0026 | 0.0047 | 0.0035 |
| `householder_apply/n16/b1024` | 3.2406 | 0.8277 | 4.0084 |
| `householder_apply/n4/b1` | 0.0003 | 0.0027 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1767 | 0.0497 | 0.2455 |
| `householder_apply/n8/b1` | 0.0007 | 0.0032 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6158 | 0.3075 | 0.7620 |
| `householder_factor/n16/b1` | 0.0025 | 0.0047 | 0.0037 |
| `householder_factor/n16/b1024` | 2.5987 | 0.6516 | 3.8094 |
| `householder_factor/n4/b1` | 0.0004 | 0.0020 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3047 | 0.0824 | 0.3093 |
| `householder_factor/n8/b1` | 0.0009 | 0.0037 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8125 | 0.2453 | 0.8864 |
| `lu/n16/b1` | 0.0022 | 0.0047 | 0.0022 |
| `lu/n16/b1024` | 1.8739 | 0.7036 | 2.2410 |
| `lu/n4/b1` | 0.0004 | 0.0022 | 0.0004 |
| `lu/n4/b1024` | 0.2101 | 0.1104 | 0.1731 |
| `lu/n8/b1` | 0.0008 | 0.0025 | 0.0007 |
| `lu/n8/b1024` | 0.5316 | 0.2800 | 0.5446 |
| `lu_factor/n16/b1` | 0.0014 | 0.0041 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2401 | 0.6315 | 1.5766 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1638 | 0.0459 | 0.1102 |
| `lu_factor/n8/b1` | 0.0006 | 0.0028 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3991 | 0.1049 | 0.3693 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0049 | 0.0032 |
| `lu_factor_solve/n16/b1024` | 2.0443 | 1.0306 | 3.2068 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0020 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2590 | 0.0708 | 0.2506 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0033 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.7090 | 0.1830 | 0.9967 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0036 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7840 | 0.3997 | 1.5782 |
| `lu_solve_prepared/n4/b1` | 0.0003 | 0.0028 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0976 | 0.0345 | 0.1446 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0027 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2887 | 0.0842 | 0.6422 |
| `qr/n16/b1` | 0.0068 | 0.0095 | 0.0064 |
| `qr/n16/b1024` | 6.6810 | 3.3227 | 6.4351 |
| `qr/n4/b1` | 0.0007 | 0.0024 | 0.0009 |
| `qr/n4/b1024` | 0.5099 | 0.2595 | 0.5732 |
| `qr/n8/b1` | 0.0018 | 0.0042 | 0.0019 |
| `qr/n8/b1024` | 1.5762 | 0.7875 | 1.5930 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0102 | 0.0094 |
| `rank_revealing_qr/n16/b1024` | 7.2364 | 3.3022 | 9.6161 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0031 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8270 | 0.4131 | 1.0756 |
| `rank_revealing_qr/n8/b1` | 0.0024 | 0.0049 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1882 | 1.0935 | 2.8544 |
| `solve/n16/b1` | 0.0028 | 0.0051 | 0.0036 |
| `solve/n16/b1024` | 2.1432 | 0.5533 | 3.3643 |
| `solve/n4/b1` | 0.0008 | 0.0024 | 0.0005 |
| `solve/n4/b1024` | 0.3110 | 0.0873 | 0.2870 |
| `solve/n8/b1` | 0.0013 | 0.0041 | 0.0012 |
| `solve/n8/b1024` | 0.7689 | 0.2076 | 1.0458 |
| `svd_full/n16/b1` | 0.0347 | 0.0378 | 0.0432 |
| `svd_full/n16/b1024` | 36.6361 | 14.9834 | 48.4331 |
| `svd_full/n4/b1` | 0.0030 | 0.0060 | 0.0053 |
| `svd_full/n4/b1024` | 2.9795 | 0.7787 | 4.7570 |
| `svd_full/n8/b1` | 0.0096 | 0.0124 | 0.0139 |
| `svd_full/n8/b1024` | 10.0270 | 5.0871 | 14.3137 |
| `svd_thin/n16/b1` | 0.0346 | 0.0376 | 0.0431 |
| `svd_thin/n16/b1024` | 36.4170 | 9.2773 | 48.1957 |
| `svd_thin/n4/b1` | 0.0031 | 0.0056 | 0.0053 |
| `svd_thin/n4/b1024` | 3.0008 | 0.7758 | 4.7576 |
| `svd_thin/n8/b1` | 0.0097 | 0.0128 | 0.0139 |
| `svd_thin/n8/b1024` | 10.0196 | 4.4577 | 14.3222 |
| `svd_values/n16/b1` | 0.0297 | 0.0333 | 0.0203 |
| `svd_values/n16/b1024` | 32.9508 | 13.1679 | 22.5538 |
| `svd_values/n4/b1` | 0.0029 | 0.0054 | 0.0029 |
| `svd_values/n4/b1024` | 2.6289 | 1.2642 | 2.4720 |
| `svd_values/n8/b1` | 0.0087 | 0.0115 | 0.0067 |
| `svd_values/n8/b1024` | 8.7975 | 3.4916 | 6.5428 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0025 | 0.0010 |
| `triangular_solve/n16/b1024` | 0.5953 | 0.1828 | 0.8385 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0961 | 0.0293 | 0.1839 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0022 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2383 | 0.0670 | 0.3577 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0040 | 0.0011 |
| `cholesky/n16/b1024` | 0.8092 | 0.2075 | 1.0891 |
| `cholesky/n4/b1` | 0.0003 | 0.0030 | 0.0002 |
| `cholesky/n4/b1024` | 0.1174 | 0.0232 | 0.1074 |
| `cholesky/n8/b1` | 0.0004 | 0.0035 | 0.0004 |
| `cholesky/n8/b1024` | 0.2633 | 0.0544 | 0.2811 |
| `eig/n16/b1` | 0.0754 | 0.0800 | 0.1020 |
| `eig/n16/b1024` | 81.4132 | 15.3666 | 110.3532 |
| `eig/n4/b1` | 0.0063 | 0.0098 | 0.0085 |
| `eig/n4/b1024` | 6.1012 | 1.1148 | 7.7625 |
| `eig/n8/b1` | 0.0209 | 0.0240 | 0.0264 |
| `eig/n8/b1024` | 21.3985 | 3.9876 | 26.9644 |
| `eigh/n16/b1` | 0.0181 | 0.0398 | 0.0186 |
| `eigh/n16/b1024` | 19.4565 | 3.1007 | 19.4279 |
| `eigh/n4/b1` | 0.0019 | 0.0046 | 0.0020 |
| `eigh/n4/b1024` | 1.7189 | 0.4357 | 1.6899 |
| `eigh/n8/b1` | 0.0057 | 0.0082 | 0.0055 |
| `eigh/n8/b1024` | 5.4743 | 1.3966 | 5.3386 |
| `eigvals/n16/b1` | 0.0471 | 0.0508 | 0.0725 |
| `eigvals/n16/b1024` | 51.9652 | 12.1523 | 81.0244 |
| `eigvals/n4/b1` | 0.0035 | 0.0065 | 0.0069 |
| `eigvals/n4/b1024` | 3.1325 | 1.0738 | 6.0935 |
| `eigvals/n8/b1` | 0.0128 | 0.0154 | 0.0210 |
| `eigvals/n8/b1024` | 12.8844 | 2.9755 | 21.6836 |
| `eigvalsh/n16/b1` | 0.0207 | 0.0243 | 0.0109 |
| `eigvalsh/n16/b1024` | 23.5133 | 11.3109 | 11.0156 |
| `eigvalsh/n4/b1` | 0.0022 | 0.0059 | 0.0014 |
| `eigvalsh/n4/b1024` | 1.8806 | 0.8341 | 1.0859 |
| `eigvalsh/n8/b1` | 0.0064 | 0.0095 | 0.0036 |
| `eigvalsh/n8/b1024` | 5.8051 | 2.6600 | 3.3311 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0062 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.7897 | 0.4520 | 3.6448 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0031 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2699 | 0.0742 | 0.3145 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0049 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.7383 | 0.1919 | 0.7490 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0064 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1077 | 0.4085 | 5.0759 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0036 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4507 | 0.1193 | 0.9649 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0046 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1545 | 0.2960 | 1.9107 |
| `householder_apply/n16/b1` | 0.0026 | 0.0056 | 0.0035 |
| `householder_apply/n16/b1024` | 3.1773 | 0.6957 | 4.2126 |
| `householder_apply/n4/b1` | 0.0003 | 0.0039 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1796 | 0.0314 | 0.2525 |
| `householder_apply/n8/b1` | 0.0007 | 0.0040 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6119 | 0.0938 | 0.7576 |
| `householder_factor/n16/b1` | 0.0025 | 0.0057 | 0.0037 |
| `householder_factor/n16/b1024` | 2.5394 | 0.6422 | 3.7673 |
| `householder_factor/n4/b1` | 0.0004 | 0.0025 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3072 | 0.0470 | 0.3091 |
| `householder_factor/n8/b1` | 0.0009 | 0.0031 | 0.0010 |
| `householder_factor/n8/b1024` | 0.7996 | 0.2101 | 0.8838 |
| `lu/n16/b1` | 0.0022 | 0.0053 | 0.0022 |
| `lu/n16/b1024` | 1.8850 | 0.2952 | 2.2393 |
| `lu/n4/b1` | 0.0004 | 0.0041 | 0.0004 |
| `lu/n4/b1024` | 0.2100 | 0.0363 | 0.1718 |
| `lu/n8/b1` | 0.0008 | 0.0037 | 0.0007 |
| `lu/n8/b1024` | 0.5574 | 0.1447 | 0.5357 |
| `lu_factor/n16/b1` | 0.0014 | 0.0051 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2113 | 0.3108 | 1.5868 |
| `lu_factor/n4/b1` | 0.0004 | 0.0022 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1711 | 0.0448 | 0.1102 |
| `lu_factor/n8/b1` | 0.0006 | 0.0030 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3956 | 0.1054 | 0.3719 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0055 | 0.0032 |
| `lu_factor_solve/n16/b1024` | 2.0502 | 0.5152 | 3.1872 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0035 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2586 | 0.0427 | 0.2512 |
| `lu_factor_solve/n8/b1` | 0.0012 | 0.0040 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.7109 | 0.1867 | 0.9960 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0043 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7895 | 0.2107 | 1.5833 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0024 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.1022 | 0.0338 | 0.1446 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0040 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2887 | 0.0573 | 0.6411 |
| `qr/n16/b1` | 0.0067 | 0.0099 | 0.0063 |
| `qr/n16/b1024` | 6.5568 | 0.8285 | 6.3948 |
| `qr/n4/b1` | 0.0007 | 0.0033 | 0.0009 |
| `qr/n4/b1024` | 0.5084 | 0.0728 | 0.5707 |
| `qr/n8/b1` | 0.0019 | 0.0042 | 0.0019 |
| `qr/n8/b1024` | 1.5691 | 0.3976 | 1.5866 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0105 | 0.0093 |
| `rank_revealing_qr/n16/b1024` | 7.2357 | 1.3385 | 9.4759 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0038 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8142 | 0.1076 | 1.0700 |
| `rank_revealing_qr/n8/b1` | 0.0024 | 0.0055 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1878 | 0.5463 | 2.8535 |
| `solve/n16/b1` | 0.0029 | 0.0058 | 0.0036 |
| `solve/n16/b1024` | 2.1792 | 0.2794 | 3.3338 |
| `solve/n4/b1` | 0.0007 | 0.0039 | 0.0005 |
| `solve/n4/b1024` | 0.3115 | 0.0487 | 0.2865 |
| `solve/n8/b1` | 0.0012 | 0.0052 | 0.0012 |
| `solve/n8/b1024` | 0.7817 | 0.1068 | 1.0529 |
| `svd_full/n16/b1` | 0.0348 | 0.0377 | 0.0433 |
| `svd_full/n16/b1024` | 37.0383 | 5.5703 | 48.9057 |
| `svd_full/n4/b1` | 0.0031 | 0.0062 | 0.0054 |
| `svd_full/n4/b1024` | 3.0303 | 0.7603 | 4.7662 |
| `svd_full/n8/b1` | 0.0097 | 0.0128 | 0.0141 |
| `svd_full/n8/b1024` | 10.1264 | 1.3042 | 14.3482 |
| `svd_thin/n16/b1` | 0.0347 | 0.0376 | 0.0435 |
| `svd_thin/n16/b1024` | 36.5003 | 6.8242 | 48.4009 |
| `svd_thin/n4/b1` | 0.0031 | 0.0060 | 0.0053 |
| `svd_thin/n4/b1024` | 2.9860 | 0.3961 | 4.7656 |
| `svd_thin/n8/b1` | 0.0104 | 0.0126 | 0.0140 |
| `svd_thin/n8/b1024` | 10.0728 | 1.3736 | 14.3783 |
| `svd_values/n16/b1` | 0.0299 | 0.0329 | 0.0203 |
| `svd_values/n16/b1024` | 32.9509 | 9.7922 | 22.4707 |
| `svd_values/n4/b1` | 0.0030 | 0.0060 | 0.0029 |
| `svd_values/n4/b1024` | 2.6546 | 0.9419 | 2.4324 |
| `svd_values/n8/b1` | 0.0087 | 0.0115 | 0.0067 |
| `svd_values/n8/b1024` | 8.8042 | 2.9898 | 6.5164 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0035 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5987 | 0.1581 | 0.8345 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0024 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0967 | 0.0283 | 0.1823 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0026 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2407 | 0.0429 | 0.3502 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0413 | - | 0.0549 |
| `cholesky/n128/b128` | 5.8306 | - | 8.0956 |
| `cholesky/n32/b1` | 0.0022 | - | 0.0021 |
| `cholesky/n32/b128` | 0.4010 | - | 0.2654 |
| `eigh/n128/b1` | 1.2576 | - | 1.0806 |
| `eigh/n128/b128` | 162.2376 | - | 144.9693 |
| `eigh/n32/b1` | 0.0641 | - | 0.0554 |
| `eigh/n32/b128` | 8.4629 | - | 7.0477 |
| `eigvalsh/n128/b1` | 2.4360 | - | 0.4552 |
| `eigvalsh/n128/b128` | 322.1576 | - | 58.9937 |
| `eigvalsh/n32/b1` | 0.0832 | - | 0.0249 |
| `eigvalsh/n32/b128` | 10.8237 | - | 3.2141 |
| `householder_apply/n128/b1` | 0.3087 | - | 0.3108 |
| `householder_apply/n128/b128` | 42.7774 | - | 42.8637 |
| `householder_apply/n32/b1` | 0.0106 | - | 0.0076 |
| `householder_apply/n32/b128` | 1.3205 | - | 0.9244 |
| `householder_factor/n128/b1` | 0.1958 | - | 0.1936 |
| `householder_factor/n128/b128` | 25.2763 | - | 25.7370 |
| `householder_factor/n32/b1` | 0.0072 | - | 0.0069 |
| `householder_factor/n32/b128` | 0.8941 | - | 0.8976 |
| `lu/n128/b1` | 0.1005 | - | 0.0825 |
| `lu/n128/b128` | 13.1140 | - | 12.8876 |
| `lu/n32/b1` | 0.0060 | - | 0.0062 |
| `lu/n32/b128` | 0.6981 | - | 0.7727 |
| `lu_factor/n128/b1` | 0.0554 | - | 0.0727 |
| `lu_factor/n128/b128` | 8.1938 | - | 10.0230 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0051 |
| `lu_factor/n32/b128` | 0.3926 | - | 0.6562 |
| `lu_factor_solve/n128/b1` | 0.0611 | - | 0.0847 |
| `lu_factor_solve/n128/b128` | 8.9405 | - | 11.4969 |
| `lu_factor_solve/n32/b1` | 0.0042 | - | 0.0095 |
| `lu_factor_solve/n32/b128` | 0.4923 | - | 0.8498 |
| `lu_solve_prepared/n128/b1` | 0.0058 | - | 0.0120 |
| `lu_solve_prepared/n128/b128` | 1.5937 | - | 2.3914 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0014 |
| `lu_solve_prepared/n32/b128` | 0.1144 | - | 0.1688 |
| `qr/n128/b1` | 0.3425 | - | 0.3924 |
| `qr/n128/b128` | 44.1393 | - | 52.3809 |
| `qr/n32/b1` | 0.0209 | - | 0.0122 |
| `qr/n32/b128` | 2.6185 | - | 1.5650 |
| `rank_revealing_qr/n128/b1` | 0.3520 | - | 0.4768 |
| `rank_revealing_qr/n128/b128` | 45.4534 | - | 62.8373 |
| `rank_revealing_qr/n32/b1` | 0.0211 | - | 0.0181 |
| `rank_revealing_qr/n32/b128` | 2.6385 | - | 2.2800 |
| `solve/n128/b1` | 0.0685 | - | 0.0882 |
| `solve/n128/b128` | 8.8548 | - | 11.9958 |
| `solve/n32/b1` | 0.0049 | - | 0.0069 |
| `solve/n32/b128` | 0.5434 | - | 0.8699 |
| `svd_thin/n128/b1` | 2.4222 | - | 2.1814 |
| `svd_thin/n128/b128` | 307.4127 | - | 300.7269 |
| `svd_thin/n32/b1` | 0.1174 | - | 0.1168 |
| `svd_thin/n32/b128` | 15.4259 | - | 15.1393 |
| `svd_values/n128/b1` | 1.5553 | - | 0.8504 |
| `svd_values/n128/b128` | 206.1733 | - | 118.5731 |
| `svd_values/n32/b1` | 0.1027 | - | 0.0474 |
| `svd_values/n32/b128` | 13.1744 | - | 6.1093 |
| `triangular_solve/n128/b1` | 0.0040 | - | 0.0070 |
| `triangular_solve/n128/b128` | 1.0072 | - | 1.3074 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0008 |
| `triangular_solve/n32/b128` | 0.0906 | - | 0.0859 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0416 | 0.0518 | 0.0570 |
| `cholesky/n128/b128` | 5.8682 | 6.9338 | 8.2223 |
| `cholesky/n32/b1` | 0.0022 | 0.0052 | 0.0022 |
| `cholesky/n32/b128` | 0.2475 | 0.1295 | 0.2620 |
| `eigh/n128/b1` | 1.2618 | 1.2315 | 0.6231 |
| `eigh/n128/b128` | 162.2675 | 163.0692 | 84.4621 |
| `eigh/n32/b1` | 0.0645 | 0.0689 | 0.0587 |
| `eigh/n32/b128` | 8.4795 | 2.1786 | 7.4684 |
| `eigvalsh/n128/b1` | 2.4418 | 2.8729 | 0.4362 |
| `eigvalsh/n128/b128` | 322.0080 | 323.1112 | 56.7804 |
| `eigvalsh/n32/b1` | 0.0836 | 0.0888 | 0.0248 |
| `eigvalsh/n32/b128` | 10.8182 | 6.7779 | 3.2336 |
| `householder_apply/n128/b1` | 0.3014 | 0.3052 | 0.0878 |
| `householder_apply/n128/b128` | 42.2028 | 42.4613 | 11.4740 |
| `householder_apply/n32/b1` | 0.0102 | 0.0136 | 0.0074 |
| `householder_apply/n32/b128` | 1.3084 | 0.3357 | 0.9225 |
| `householder_factor/n128/b1` | 0.1945 | 0.1978 | 0.1127 |
| `householder_factor/n128/b128` | 24.8897 | 25.3121 | 15.0012 |
| `householder_factor/n32/b1` | 0.0071 | 0.0094 | 0.0068 |
| `householder_factor/n32/b128` | 0.8967 | 0.4546 | 0.8860 |
| `lu/n128/b1` | 0.1003 | 0.1129 | 0.0814 |
| `lu/n128/b128` | 12.8905 | 16.1133 | 12.9815 |
| `lu/n32/b1` | 0.0061 | 0.0083 | 0.0062 |
| `lu/n32/b128` | 0.6523 | 0.3504 | 0.7678 |
| `lu_factor/n128/b1` | 0.0563 | 0.0721 | 0.0730 |
| `lu_factor/n128/b128` | 8.1250 | 2.5638 | 10.0348 |
| `lu_factor/n32/b1` | 0.0032 | 0.0049 | 0.0052 |
| `lu_factor/n32/b128` | 0.3994 | 0.2057 | 0.6541 |
| `lu_factor_solve/n128/b1` | 0.0622 | 0.0785 | 0.0867 |
| `lu_factor_solve/n128/b128` | 8.9175 | 2.8210 | 11.9673 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0073 | 0.0074 |
| `lu_factor_solve/n32/b128` | 0.4904 | 0.1299 | 0.9813 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0084 | 0.0098 |
| `lu_solve_prepared/n128/b128` | 1.9549 | 0.5359 | 2.3899 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0033 | 0.0022 |
| `lu_solve_prepared/n32/b128` | 0.1131 | 0.0340 | 0.2966 |
| `qr/n128/b1` | 0.3425 | 0.6113 | 0.2594 |
| `qr/n128/b128` | 44.1405 | 83.5740 | 39.8951 |
| `qr/n32/b1` | 0.0209 | 0.0459 | 0.0120 |
| `qr/n32/b128` | 2.6197 | 0.6656 | 1.5601 |
| `rank_revealing_qr/n128/b1` | 0.3562 | 0.3698 | 0.4294 |
| `rank_revealing_qr/n128/b128` | 44.7092 | 48.4513 | 60.9737 |
| `rank_revealing_qr/n32/b1` | 0.0211 | 0.0466 | 0.0179 |
| `rank_revealing_qr/n32/b128` | 2.6351 | 1.3258 | 2.2879 |
| `solve/n128/b1` | 0.0686 | 0.0822 | 0.0909 |
| `solve/n128/b128` | 8.8745 | 10.6029 | 12.1209 |
| `solve/n32/b1` | 0.0049 | 0.0078 | 0.0082 |
| `solve/n32/b128` | 0.5515 | 0.2749 | 0.9961 |
| `svd_thin/n128/b1` | 2.4267 | 1.8170 | 1.7663 |
| `svd_thin/n128/b128` | 308.8997 | 230.9101 | 245.3731 |
| `svd_thin/n32/b1` | 0.1175 | 0.1218 | 0.1220 |
| `svd_thin/n32/b128` | 15.0928 | 4.9432 | 15.7122 |
| `svd_values/n128/b1` | 1.5638 | 1.7382 | 0.8352 |
| `svd_values/n128/b128` | 208.3916 | 208.4407 | 118.0614 |
| `svd_values/n32/b1` | 0.1028 | 0.1088 | 0.0474 |
| `svd_values/n32/b128` | 13.1874 | 5.0034 | 6.1075 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0067 | 0.0057 |
| `triangular_solve/n128/b128` | 0.8426 | 0.8369 | 1.3749 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0025 | 0.0014 |
| `triangular_solve/n32/b128` | 0.0896 | 0.0273 | 0.1656 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0374 | 0.0550 | 0.0556 |
| `cholesky/n128/b128` | 5.4991 | 7.0288 | 8.3226 |
| `cholesky/n32/b1` | 0.0022 | 0.0056 | 0.0022 |
| `cholesky/n32/b128` | 0.2717 | 0.0711 | 0.2584 |
| `eigh/n128/b1` | 1.2624 | 1.2430 | 0.5890 |
| `eigh/n128/b128` | 162.0591 | 159.9712 | 79.0753 |
| `eigh/n32/b1` | 0.0646 | 0.0693 | 0.0596 |
| `eigh/n32/b128` | 8.4730 | 2.1561 | 7.5678 |
| `eigvalsh/n128/b1` | 2.4494 | 3.1001 | 0.4458 |
| `eigvalsh/n128/b128` | 321.7005 | 323.0038 | 57.9024 |
| `eigvalsh/n32/b1` | 0.0830 | 0.0896 | 0.0248 |
| `eigvalsh/n32/b128` | 10.8300 | 5.9409 | 3.2269 |
| `householder_apply/n128/b1` | 0.3157 | 0.3319 | 0.0578 |
| `householder_apply/n128/b128` | 40.6709 | 42.8145 | 7.3894 |
| `householder_apply/n32/b1` | 0.0103 | 0.0134 | 0.0075 |
| `householder_apply/n32/b128` | 1.3229 | 0.3342 | 0.9226 |
| `householder_factor/n128/b1` | 0.1916 | 0.1966 | 0.0882 |
| `householder_factor/n128/b128` | 25.2242 | 25.3872 | 11.6682 |
| `householder_factor/n32/b1` | 0.0071 | 0.0175 | 0.0068 |
| `householder_factor/n32/b128` | 0.8944 | 0.2314 | 0.8813 |
| `lu/n128/b1` | 0.0981 | 0.1256 | 0.0824 |
| `lu/n128/b128` | 14.1967 | 16.4439 | 12.9697 |
| `lu/n32/b1` | 0.0059 | 0.0090 | 0.0062 |
| `lu/n32/b128` | 0.6719 | 0.1805 | 0.7860 |
| `lu_factor/n128/b1` | 0.0566 | 0.0827 | 0.0727 |
| `lu_factor/n128/b128` | 8.1905 | 1.5247 | 10.0429 |
| `lu_factor/n32/b1` | 0.0032 | 0.0066 | 0.0052 |
| `lu_factor/n32/b128` | 0.3847 | 0.1090 | 0.6498 |
| `lu_factor_solve/n128/b1` | 0.0618 | 0.0882 | 0.0860 |
| `lu_factor_solve/n128/b128` | 8.9990 | 1.5576 | 11.8699 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0072 | 0.0078 |
| `lu_factor_solve/n32/b128` | 0.5075 | 0.1330 | 1.0138 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0088 | 0.0097 |
| `lu_solve_prepared/n128/b128` | 2.1359 | 0.5353 | 2.3038 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0037 | 0.0025 |
| `lu_solve_prepared/n32/b128` | 0.1132 | 0.0348 | 0.3297 |
| `qr/n128/b1` | 0.3431 | 0.9665 | 0.2973 |
| `qr/n128/b128` | 44.2503 | 120.8206 | 31.3846 |
| `qr/n32/b1` | 0.0208 | 0.0625 | 0.0120 |
| `qr/n32/b128` | 2.6332 | 0.3325 | 1.5415 |
| `rank_revealing_qr/n128/b1` | 0.3538 | 0.4300 | 0.4797 |
| `rank_revealing_qr/n128/b128` | 45.5133 | 57.5387 | 63.7599 |
| `rank_revealing_qr/n32/b1` | 0.0211 | 0.0664 | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6140 | 0.6593 | 2.2619 |
| `solve/n128/b1` | 0.0681 | 0.0936 | 0.0899 |
| `solve/n128/b128` | 8.8506 | 12.1409 | 12.1525 |
| `solve/n32/b1` | 0.0049 | 0.0074 | 0.0081 |
| `solve/n32/b128` | 0.5476 | 0.0800 | 1.0255 |
| `svd_thin/n128/b1` | 2.4287 | 1.8572 | 1.6943 |
| `svd_thin/n128/b128` | 308.6082 | 238.5663 | 237.6516 |
| `svd_thin/n32/b1` | 0.1179 | 0.1222 | 0.1226 |
| `svd_thin/n32/b128` | 15.2034 | 3.8103 | 15.8434 |
| `svd_values/n128/b1` | 1.5567 | 1.7259 | 0.8330 |
| `svd_values/n128/b128` | 207.4383 | 208.8401 | 116.6305 |
| `svd_values/n32/b1` | 0.1025 | 0.1098 | 0.0474 |
| `svd_values/n32/b128` | 13.1766 | 3.9368 | 6.1033 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0067 | 0.0061 |
| `triangular_solve/n128/b128` | 0.9681 | 1.0036 | 1.3842 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0038 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0899 | 0.0257 | 0.1841 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1073 | - | 0.2432 |
| `cholesky/n128/b128` | 15.8823 | - | 32.8126 |
| `cholesky/n32/b1` | 0.0033 | - | 0.0049 |
| `cholesky/n32/b128` | 0.4199 | - | 0.6225 |
| `eigh/n128/b1` | 1.8489 | - | 2.9560 |
| `eigh/n128/b128` | 241.3796 | - | 384.1148 |
| `eigh/n32/b1` | 0.0806 | - | 0.0868 |
| `eigh/n32/b128` | 10.5311 | - | 11.3334 |
| `eigvalsh/n128/b1` | 2.7108 | - | 1.2649 |
| `eigvalsh/n128/b128` | 370.7261 | - | 163.2535 |
| `eigvalsh/n32/b1` | 0.0898 | - | 0.0442 |
| `eigvalsh/n32/b128` | 11.7402 | - | 5.7486 |
| `householder_apply/n128/b1` | 0.6841 | - | 0.9573 |
| `householder_apply/n128/b128` | 92.6768 | - | 126.1166 |
| `householder_apply/n32/b1` | 0.0142 | - | 0.0197 |
| `householder_apply/n32/b128` | 1.8699 | - | 2.7107 |
| `householder_factor/n128/b1` | 0.4538 | - | 0.5400 |
| `householder_factor/n128/b128` | 58.6408 | - | 70.5666 |
| `householder_factor/n32/b1` | 0.0111 | - | 0.0156 |
| `householder_factor/n32/b128` | 1.4318 | - | 2.0167 |
| `lu/n128/b1` | 0.2011 | - | 0.2710 |
| `lu/n128/b128` | 27.9833 | - | 38.6499 |
| `lu/n32/b1` | 0.0080 | - | 0.0105 |
| `lu/n32/b128` | 1.0395 | - | 1.4281 |
| `lu_factor/n128/b1` | 0.1571 | - | 0.2485 |
| `lu_factor/n128/b128` | 21.7578 | - | 32.6797 |
| `lu_factor/n32/b1` | 0.0053 | - | 0.0089 |
| `lu_factor/n32/b128` | 0.6416 | - | 1.1444 |
| `lu_factor_solve/n128/b1` | 0.1740 | - | 0.2799 |
| `lu_factor_solve/n128/b128` | 24.2244 | - | 36.8112 |
| `lu_factor_solve/n32/b1` | 0.0074 | - | 0.0133 |
| `lu_factor_solve/n32/b128` | 0.9211 | - | 1.7060 |
| `lu_solve_prepared/n128/b1` | 0.0186 | - | 0.0307 |
| `lu_solve_prepared/n128/b128` | 4.2135 | - | 5.7317 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0044 |
| `lu_solve_prepared/n32/b128` | 0.2832 | - | 0.5587 |
| `qr/n128/b1` | 0.9675 | - | 1.1374 |
| `qr/n128/b128` | 124.6845 | - | 148.0452 |
| `qr/n32/b1` | 0.0426 | - | 0.0283 |
| `qr/n32/b128` | 5.4349 | - | 3.6577 |
| `rank_revealing_qr/n128/b1` | 1.0053 | - | 1.5926 |
| `rank_revealing_qr/n128/b128` | 129.7514 | - | 207.4598 |
| `rank_revealing_qr/n32/b1` | 0.0388 | - | 0.0391 |
| `rank_revealing_qr/n32/b128` | 4.9320 | - | 5.1428 |
| `solve/n128/b1` | 0.1810 | - | 0.2849 |
| `solve/n128/b128` | 23.7132 | - | 37.6177 |
| `solve/n32/b1` | 0.0083 | - | 0.0140 |
| `solve/n32/b128` | 0.9591 | - | 1.7605 |
| `svd_thin/n128/b1` | 3.9197 | - | 4.3723 |
| `svd_thin/n128/b128` | 505.5358 | - | 602.3557 |
| `svd_thin/n32/b1` | 0.1499 | - | 0.1663 |
| `svd_thin/n32/b128` | 19.5691 | - | 22.5262 |
| `svd_values/n128/b1` | 2.0713 | - | 1.7906 |
| `svd_values/n128/b128` | 288.3868 | - | 251.2805 |
| `svd_values/n32/b1` | 0.1134 | - | 0.0744 |
| `svd_values/n32/b128` | 14.8939 | - | 9.6287 |
| `triangular_solve/n128/b1` | 0.0109 | - | 0.0148 |
| `triangular_solve/n128/b128` | 2.3050 | - | 2.8312 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0021 |
| `triangular_solve/n32/b128` | 0.1942 | - | 0.2620 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1095 | 0.1114 | 0.2442 |
| `cholesky/n128/b128` | 15.8523 | 15.6525 | 32.8129 |
| `cholesky/n32/b1` | 0.0034 | 0.0061 | 0.0049 |
| `cholesky/n32/b128` | 0.4243 | 0.2162 | 0.6223 |
| `eigh/n128/b1` | 1.8401 | 1.5813 | 1.8235 |
| `eigh/n128/b128` | 243.0348 | 228.2135 | 235.5097 |
| `eigh/n32/b1` | 0.0806 | 0.0852 | 0.0867 |
| `eigh/n32/b128` | 10.4826 | 2.6482 | 11.3200 |
| `eigvalsh/n128/b1` | 2.7196 | 3.8852 | 0.8155 |
| `eigvalsh/n128/b128` | 370.6644 | 371.3370 | 106.5665 |
| `eigvalsh/n32/b1` | 0.0896 | 0.0956 | 0.0443 |
| `eigvalsh/n32/b128` | 11.7179 | 7.0217 | 5.7734 |
| `householder_apply/n128/b1` | 0.6879 | 0.6906 | 0.2903 |
| `householder_apply/n128/b128` | 93.1519 | 93.2314 | 37.6606 |
| `householder_apply/n32/b1` | 0.0145 | 0.0173 | 0.0197 |
| `householder_apply/n32/b128` | 1.8487 | 0.4630 | 2.5546 |
| `householder_factor/n128/b1` | 0.4554 | 0.4614 | 0.2613 |
| `householder_factor/n128/b128` | 59.2848 | 59.0709 | 33.8433 |
| `householder_factor/n32/b1` | 0.0113 | 0.0138 | 0.0154 |
| `householder_factor/n32/b128` | 1.4318 | 0.7002 | 2.0065 |
| `lu/n128/b1` | 0.2016 | 0.1920 | 0.2709 |
| `lu/n128/b128` | 28.5549 | 26.4486 | 38.7030 |
| `lu/n32/b1` | 0.0078 | 0.0109 | 0.0105 |
| `lu/n32/b128` | 1.0178 | 0.2658 | 1.4329 |
| `lu_factor/n128/b1` | 0.1548 | 0.1440 | 0.2467 |
| `lu_factor/n128/b128` | 21.7305 | 6.1706 | 32.6104 |
| `lu_factor/n32/b1` | 0.0053 | 0.0082 | 0.0089 |
| `lu_factor/n32/b128` | 0.6405 | 0.3310 | 1.1349 |
| `lu_factor_solve/n128/b1` | 0.1737 | 0.1627 | 0.2657 |
| `lu_factor_solve/n128/b128` | 24.1480 | 6.5699 | 35.2934 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0106 | 0.0119 |
| `lu_factor_solve/n32/b128` | 0.9247 | 0.4707 | 1.5619 |
| `lu_solve_prepared/n128/b1` | 0.0187 | 0.0217 | 0.0152 |
| `lu_solve_prepared/n128/b128` | 4.1172 | 1.3795 | 3.7709 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0039 | 0.0026 |
| `lu_solve_prepared/n32/b128` | 0.2798 | 0.0797 | 0.3591 |
| `qr/n128/b1` | 0.9691 | 0.8724 | 0.5994 |
| `qr/n128/b128` | 125.1816 | 114.2824 | 77.9719 |
| `qr/n32/b1` | 0.0426 | 0.0706 | 0.0284 |
| `qr/n32/b128` | 5.4261 | 2.0757 | 3.6732 |
| `rank_revealing_qr/n128/b1` | 1.0177 | 0.7910 | 1.3783 |
| `rank_revealing_qr/n128/b128` | 132.1142 | 103.5636 | 179.3361 |
| `rank_revealing_qr/n32/b1` | 0.0392 | 0.0637 | 0.0389 |
| `rank_revealing_qr/n32/b128` | 5.0053 | 2.0247 | 5.1215 |
| `solve/n128/b1` | 0.1807 | 0.1688 | 0.2803 |
| `solve/n128/b128` | 23.6809 | 22.2807 | 36.4318 |
| `solve/n32/b1` | 0.0083 | 0.0112 | 0.0125 |
| `solve/n32/b128` | 0.9668 | 0.2480 | 1.6178 |
| `svd_thin/n128/b1` | 3.9275 | 2.7123 | 2.7184 |
| `svd_thin/n128/b128` | 506.9470 | 349.5397 | 384.5975 |
| `svd_thin/n32/b1` | 0.1506 | 0.1547 | 0.1711 |
| `svd_thin/n32/b128` | 19.6510 | 4.9675 | 23.0782 |
| `svd_values/n128/b1` | 2.0764 | 2.3545 | 1.4110 |
| `svd_values/n128/b128` | 288.9337 | 288.9936 | 202.2931 |
| `svd_values/n32/b1` | 0.1129 | 0.1209 | 0.0738 |
| `svd_values/n32/b128` | 14.8736 | 5.7372 | 9.5715 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0139 | 0.0077 |
| `triangular_solve/n128/b128` | 2.2138 | 2.1854 | 2.2721 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0039 | 0.0015 |
| `triangular_solve/n32/b128` | 0.1919 | 0.0556 | 0.1788 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1089 | 0.1173 | 0.2441 |
| `cholesky/n128/b128` | 15.8822 | 16.5230 | 33.0581 |
| `cholesky/n32/b1` | 0.0034 | 0.0059 | 0.0049 |
| `cholesky/n32/b128` | 0.4095 | 0.0576 | 0.6283 |
| `eigh/n128/b1` | 1.8413 | 1.6196 | 1.6079 |
| `eigh/n128/b128` | 241.6746 | 211.7136 | 211.3367 |
| `eigh/n32/b1` | 0.0806 | 0.0854 | 0.0871 |
| `eigh/n32/b128` | 10.4992 | 1.7147 | 11.3342 |
| `eigvalsh/n128/b1` | 2.7192 | 3.9974 | 0.7381 |
| `eigvalsh/n128/b128` | 370.9651 | 371.3961 | 96.3400 |
| `eigvalsh/n32/b1` | 0.0896 | 0.0959 | 0.0443 |
| `eigvalsh/n32/b128` | 11.6839 | 6.1492 | 5.7681 |
| `householder_apply/n128/b1` | 0.6793 | 0.6922 | 0.1763 |
| `householder_apply/n128/b128` | 92.7045 | 93.0881 | 21.8195 |
| `householder_apply/n32/b1` | 0.0144 | 0.0175 | 0.0196 |
| `householder_apply/n32/b128` | 1.8337 | 0.4582 | 2.5501 |
| `householder_factor/n128/b1` | 0.4578 | 0.4624 | 0.1803 |
| `householder_factor/n128/b128` | 59.4764 | 59.0639 | 23.4297 |
| `householder_factor/n32/b1` | 0.0111 | 0.0140 | 0.0155 |
| `householder_factor/n32/b128` | 1.4466 | 0.3624 | 2.0048 |
| `lu/n128/b1` | 0.2011 | 0.1995 | 0.2716 |
| `lu/n128/b128` | 28.2574 | 27.9428 | 38.7438 |
| `lu/n32/b1` | 0.0080 | 0.0104 | 0.0106 |
| `lu/n32/b128` | 1.0205 | 0.2452 | 1.4204 |
| `lu_factor/n128/b1` | 0.1541 | 0.1520 | 0.2473 |
| `lu_factor/n128/b128` | 21.8373 | 3.3569 | 32.6350 |
| `lu_factor/n32/b1` | 0.0053 | 0.0083 | 0.0089 |
| `lu_factor/n32/b128` | 0.6518 | 0.1703 | 1.1338 |
| `lu_factor_solve/n128/b1` | 0.1732 | 0.1754 | 0.2663 |
| `lu_factor_solve/n128/b128` | 24.3916 | 3.6868 | 35.4540 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0107 | 0.0119 |
| `lu_factor_solve/n32/b128` | 0.9258 | 0.1255 | 1.5640 |
| `lu_solve_prepared/n128/b1` | 0.0187 | 0.0217 | 0.0151 |
| `lu_solve_prepared/n128/b128` | 4.2730 | 0.7935 | 3.7336 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0054 | 0.0027 |
| `lu_solve_prepared/n32/b128` | 0.2826 | 0.0452 | 0.3676 |
| `qr/n128/b1` | 0.9700 | 1.1977 | 0.4462 |
| `qr/n128/b128` | 124.7220 | 153.3057 | 58.0749 |
| `qr/n32/b1` | 0.0425 | 0.0931 | 0.0284 |
| `qr/n32/b128` | 5.4277 | 1.3921 | 3.6769 |
| `rank_revealing_qr/n128/b1` | 1.0126 | 0.8832 | 1.2328 |
| `rank_revealing_qr/n128/b128` | 130.2741 | 114.9762 | 159.6029 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0849 | 0.0389 |
| `rank_revealing_qr/n32/b128` | 4.9799 | 0.6221 | 5.1225 |
| `solve/n128/b1` | 0.1809 | 0.1806 | 0.2786 |
| `solve/n128/b128` | 23.8502 | 23.5791 | 36.3994 |
| `solve/n32/b1` | 0.0084 | 0.0111 | 0.0128 |
| `solve/n32/b128` | 0.9630 | 0.2483 | 1.6151 |
| `svd_thin/n128/b1` | 3.9470 | 2.7942 | 2.4215 |
| `svd_thin/n128/b128` | 507.8142 | 360.1184 | 346.7422 |
| `svd_thin/n32/b1` | 0.1508 | 0.1558 | 0.1724 |
| `svd_thin/n32/b128` | 19.7351 | 2.4723 | 23.1831 |
| `svd_values/n128/b1` | 2.0831 | 2.3355 | 1.3589 |
| `svd_values/n128/b128` | 288.9645 | 288.2333 | 194.2710 |
| `svd_values/n32/b1` | 0.1144 | 0.1203 | 0.0737 |
| `svd_values/n32/b128` | 14.9340 | 3.9831 | 9.5744 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0134 | 0.0077 |
| `triangular_solve/n128/b128` | 2.3661 | 2.2009 | 2.2727 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0047 | 0.0016 |
| `triangular_solve/n32/b128` | 0.1938 | 0.0504 | 0.1892 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2093 | - | 0.2664 |
| `cholesky/n256/b4` | 0.8534 | - | 1.0704 |
| `cholesky/n512/b1` | 1.3043 | - | 1.9914 |
| `cholesky/n512/b4` | 5.6393 | - | 8.3786 |
| `eigh/n256/b1` | 5.5874 | - | 5.9157 |
| `eigh/n256/b4` | 22.4441 | - | 23.8458 |
| `eigh/n512/b1` | 28.6956 | - | 36.6968 |
| `eigh/n512/b4` | 115.5506 | - | 145.9974 |
| `eigvalsh/n256/b1` | 16.1027 | - | 2.5697 |
| `eigvalsh/n256/b4` | 64.7004 | - | 10.3357 |
| `eigvalsh/n512/b1` | 118.0142 | - | 16.5337 |
| `eigvalsh/n512/b4` | 478.4248 | - | 66.1027 |
| `householder_apply/n256/b1` | 2.2268 | - | 1.9290 |
| `householder_apply/n256/b4` | 9.7435 | - | 7.7833 |
| `householder_apply/n512/b1` | 19.1042 | - | 12.8701 |
| `householder_apply/n512/b4` | 76.7255 | - | 52.2722 |
| `householder_factor/n256/b1` | 1.4614 | - | 1.1147 |
| `householder_factor/n256/b4` | 5.9253 | - | 4.5277 |
| `householder_factor/n512/b1` | 12.1329 | - | 8.0371 |
| `householder_factor/n512/b4` | 48.6742 | - | 32.0814 |
| `lu/n256/b1` | 0.5133 | - | 0.4972 |
| `lu/n256/b4` | 2.0966 | - | 2.1399 |
| `lu/n512/b1` | 3.3039 | - | 3.3210 |
| `lu/n512/b4` | 14.6014 | - | 13.5405 |
| `lu_factor/n256/b1` | 0.3519 | - | 0.4557 |
| `lu_factor/n256/b4` | 1.5313 | - | 1.8374 |
| `lu_factor/n512/b1` | 2.7545 | - | 3.0011 |
| `lu_factor/n512/b4` | 11.7239 | - | 12.3480 |
| `lu_factor_solve/n256/b1` | 0.3701 | - | 0.5004 |
| `lu_factor_solve/n256/b4` | 1.5952 | - | 2.0056 |
| `lu_factor_solve/n512/b1` | 2.8057 | - | 3.1698 |
| `lu_factor_solve/n512/b4` | 11.9606 | - | 13.1174 |
| `lu_solve_prepared/n256/b1` | 0.0170 | - | 0.0409 |
| `lu_solve_prepared/n256/b4` | 0.0800 | - | 0.1737 |
| `lu_solve_prepared/n512/b1` | 0.0711 | - | 0.1898 |
| `lu_solve_prepared/n512/b4` | 0.3636 | - | 0.9637 |
| `qr/n256/b1` | 1.8547 | - | 2.3773 |
| `qr/n256/b4` | 7.4074 | - | 9.5741 |
| `qr/n512/b1` | 11.4996 | - | 17.1251 |
| `qr/n512/b4` | 46.4976 | - | 69.2402 |
| `rank_revealing_qr/n256/b1` | 2.1343 | - | 2.9296 |
| `rank_revealing_qr/n256/b4` | 8.4307 | - | 11.8627 |
| `rank_revealing_qr/n512/b1` | 14.7948 | - | 21.3287 |
| `rank_revealing_qr/n512/b4` | 59.3476 | - | 85.7282 |
| `solve/n256/b1` | 0.3982 | - | 0.5068 |
| `solve/n256/b4` | 1.5812 | - | 2.0518 |
| `solve/n512/b1` | 2.8675 | - | 3.2314 |
| `solve/n512/b4` | 11.4376 | - | 12.9552 |
| `svd_thin/n256/b1` | 12.2437 | - | 11.4808 |
| `svd_thin/n256/b4` | 48.7330 | - | 46.2829 |
| `svd_thin/n512/b1` | 70.8128 | - | 73.5946 |
| `svd_thin/n512/b4` | 284.6772 | - | 303.9562 |
| `svd_values/n256/b1` | 7.5060 | - | 4.7209 |
| `svd_values/n256/b4` | 29.9642 | - | 18.9910 |
| `svd_values/n512/b1` | 40.8987 | - | 30.5980 |
| `svd_values/n512/b4` | 168.2713 | - | 127.3465 |
| `triangular_solve/n256/b1` | 0.0104 | - | 0.0236 |
| `triangular_solve/n256/b4` | 0.0449 | - | 0.1100 |
| `triangular_solve/n512/b1` | 0.0343 | - | 0.0948 |
| `triangular_solve/n512/b4` | 0.1418 | - | 0.3964 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2111 | 0.2011 | 0.1724 |
| `cholesky/n256/b4` | 0.8551 | 0.7944 | 0.6578 |
| `cholesky/n512/b1` | 1.3046 | 0.8197 | 0.8964 |
| `cholesky/n512/b4` | 5.6539 | 3.5932 | 4.0369 |
| `eigh/n256/b1` | 5.5865 | 4.2186 | 2.8024 |
| `eigh/n256/b4` | 22.4417 | 17.1799 | 11.2988 |
| `eigh/n512/b1` | 28.6563 | 15.7575 | 13.2218 |
| `eigh/n512/b4` | 115.2559 | 63.1849 | 53.2055 |
| `eigvalsh/n256/b1` | 16.0928 | 17.0276 | 1.8696 |
| `eigvalsh/n256/b4` | 64.8831 | 65.9053 | 7.4609 |
| `eigvalsh/n512/b1` | 116.7003 | 115.4271 | 8.9364 |
| `eigvalsh/n512/b4` | 470.4753 | 462.0874 | 36.0464 |
| `householder_apply/n256/b1` | 2.3541 | 2.3890 | 0.5648 |
| `householder_apply/n256/b4` | 9.7331 | 9.8217 | 2.2793 |
| `householder_apply/n512/b1` | 18.9207 | 18.9151 | 3.5242 |
| `householder_apply/n512/b4` | 83.6770 | 83.4247 | 14.2318 |
| `householder_factor/n256/b1` | 1.4855 | 1.5061 | 0.3653 |
| `householder_factor/n256/b4` | 5.9125 | 5.9467 | 1.4557 |
| `householder_factor/n512/b1` | 12.0391 | 12.0956 | 2.1776 |
| `householder_factor/n512/b4` | 48.4849 | 48.5113 | 8.8126 |
| `lu/n256/b1` | 0.4978 | 0.4642 | 0.2016 |
| `lu/n256/b4` | 2.1010 | 1.9343 | 0.8841 |
| `lu/n512/b1` | 3.7000 | 2.0435 | 1.1446 |
| `lu/n512/b4` | 13.3349 | 8.0811 | 4.8447 |
| `lu_factor/n256/b1` | 0.3806 | 0.3279 | 0.1604 |
| `lu_factor/n256/b4` | 1.5187 | 0.7741 | 0.6503 |
| `lu_factor/n512/b1` | 2.8390 | 1.4798 | 0.8505 |
| `lu_factor/n512/b4` | 11.7397 | 5.2059 | 3.4595 |
| `lu_factor_solve/n256/b1` | 0.3728 | 0.3313 | 0.1927 |
| `lu_factor_solve/n256/b4` | 1.4845 | 0.3925 | 0.7645 |
| `lu_factor_solve/n512/b1` | 2.8984 | 1.5431 | 0.9555 |
| `lu_factor_solve/n512/b4` | 12.0485 | 6.0394 | 3.8869 |
| `lu_solve_prepared/n256/b1` | 0.0172 | 0.0238 | 0.0244 |
| `lu_solve_prepared/n256/b4` | 0.0744 | 0.0247 | 0.1253 |
| `lu_solve_prepared/n512/b1` | 0.0716 | 0.0663 | 0.0972 |
| `lu_solve_prepared/n512/b4` | 0.4412 | 0.1140 | 0.5678 |
| `qr/n256/b1` | 1.8571 | 1.7518 | 1.1529 |
| `qr/n256/b4` | 7.4335 | 7.2363 | 4.7172 |
| `qr/n512/b1` | 11.5138 | 6.0674 | 6.8808 |
| `qr/n512/b4` | 46.1776 | 24.5175 | 28.0371 |
| `rank_revealing_qr/n256/b1` | 2.1248 | 1.4712 | 2.2652 |
| `rank_revealing_qr/n256/b4` | 8.4144 | 5.9210 | 9.1506 |
| `rank_revealing_qr/n512/b1` | 15.0286 | 6.3160 | 15.7536 |
| `rank_revealing_qr/n512/b4` | 59.9582 | 25.0343 | 63.8502 |
| `solve/n256/b1` | 0.3959 | 0.3643 | 0.2113 |
| `solve/n256/b4` | 1.5778 | 1.4359 | 0.8464 |
| `solve/n512/b1` | 2.8956 | 1.5886 | 1.0107 |
| `solve/n512/b4` | 11.4730 | 6.7211 | 4.1223 |
| `svd_thin/n256/b1` | 12.2061 | 8.7819 | 8.2534 |
| `svd_thin/n256/b4` | 48.8361 | 35.6992 | 33.2991 |
| `svd_thin/n512/b1` | 70.6352 | 40.0155 | 38.9643 |
| `svd_thin/n512/b4` | 283.2151 | 160.9771 | 161.0292 |
| `svd_values/n256/b1` | 7.5339 | 8.3014 | 4.3114 |
| `svd_values/n256/b4` | 30.0152 | 31.0932 | 17.4024 |
| `svd_values/n512/b1` | 41.0637 | 34.6538 | 17.7692 |
| `svd_values/n512/b4` | 168.7108 | 140.7966 | 76.1136 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0159 | 0.0151 |
| `triangular_solve/n256/b4` | 0.0457 | 0.0582 | 0.0761 |
| `triangular_solve/n512/b1` | 0.0358 | 0.0363 | 0.0568 |
| `triangular_solve/n512/b4` | 0.1484 | 0.1439 | 0.2586 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2102 | 0.2170 | 0.1629 |
| `cholesky/n256/b4` | 0.8395 | 0.8350 | 0.4828 |
| `cholesky/n512/b1` | 1.3116 | 0.7171 | 0.5471 |
| `cholesky/n512/b4` | 5.6802 | 3.2035 | 2.7404 |
| `eigh/n256/b1` | 5.5878 | 4.1061 | 2.3194 |
| `eigh/n256/b4` | 22.3894 | 16.4515 | 9.3600 |
| `eigh/n512/b1` | 28.7936 | 14.8029 | 9.3338 |
| `eigh/n512/b4` | 115.9702 | 58.3872 | 37.4826 |
| `eigvalsh/n256/b1` | 16.0895 | 17.1307 | 1.7898 |
| `eigvalsh/n256/b4` | 64.7311 | 65.9462 | 7.1567 |
| `eigvalsh/n512/b1` | 117.1440 | 115.3098 | 7.6099 |
| `eigvalsh/n512/b4` | 470.2707 | 460.7743 | 30.5720 |
| `householder_apply/n256/b1` | 2.3839 | 2.4346 | 0.3118 |
| `householder_apply/n256/b4` | 9.7051 | 9.8172 | 1.2265 |
| `householder_apply/n512/b1` | 18.7665 | 19.1634 | 1.9193 |
| `householder_apply/n512/b4` | 82.9838 | 83.7545 | 7.8085 |
| `householder_factor/n256/b1` | 1.4766 | 1.5095 | 0.3184 |
| `householder_factor/n256/b4` | 5.9524 | 6.0072 | 1.2812 |
| `householder_factor/n512/b1` | 12.1379 | 12.2506 | 1.2974 |
| `householder_factor/n512/b4` | 48.3327 | 49.1407 | 5.3690 |
| `lu/n256/b1` | 0.5124 | 0.4946 | 0.1890 |
| `lu/n256/b4` | 2.0797 | 2.1148 | 0.8495 |
| `lu/n512/b1` | 3.2941 | 2.0767 | 0.8958 |
| `lu/n512/b4` | 13.1488 | 8.3522 | 3.8775 |
| `lu_factor/n256/b1` | 0.3800 | 0.3520 | 0.1511 |
| `lu_factor/n256/b4` | 1.5405 | 1.4874 | 0.6229 |
| `lu_factor/n512/b1` | 2.8249 | 1.5400 | 0.6111 |
| `lu_factor/n512/b4` | 11.7236 | 6.3183 | 2.4496 |
| `lu_factor_solve/n256/b1` | 0.3715 | 0.3746 | 0.1906 |
| `lu_factor_solve/n256/b4` | 1.4966 | 1.5028 | 0.7698 |
| `lu_factor_solve/n512/b1` | 2.8876 | 1.5939 | 0.7241 |
| `lu_factor_solve/n512/b4` | 12.1523 | 6.5345 | 2.9554 |
| `lu_solve_prepared/n256/b1` | 0.0171 | 0.0276 | 0.0245 |
| `lu_solve_prepared/n256/b4` | 0.0809 | 0.1117 | 0.1135 |
| `lu_solve_prepared/n512/b1` | 0.0728 | 0.0764 | 0.0958 |
| `lu_solve_prepared/n512/b4` | 0.4290 | 0.3847 | 0.5500 |
| `qr/n256/b1` | 1.8528 | 2.4560 | 1.1229 |
| `qr/n256/b4` | 7.3754 | 9.8542 | 4.4717 |
| `qr/n512/b1` | 11.5094 | 7.0205 | 5.2661 |
| `qr/n512/b4` | 46.1765 | 27.8652 | 21.5701 |
| `rank_revealing_qr/n256/b1` | 2.1352 | 1.5661 | 2.2142 |
| `rank_revealing_qr/n256/b4` | 8.3753 | 6.2084 | 8.9186 |
| `rank_revealing_qr/n512/b1` | 15.2237 | 5.8589 | 14.8853 |
| `rank_revealing_qr/n512/b4` | 60.6282 | 23.4307 | 59.5078 |
| `solve/n256/b1` | 0.3960 | 0.4018 | 0.2085 |
| `solve/n256/b4` | 1.5787 | 1.6085 | 0.8321 |
| `solve/n512/b1` | 2.8718 | 1.7082 | 0.7564 |
| `solve/n512/b4` | 11.4436 | 6.6468 | 3.1859 |
| `svd_thin/n256/b1` | 12.2650 | 9.0364 | 7.6775 |
| `svd_thin/n256/b4` | 48.8943 | 36.0297 | 30.9870 |
| `svd_thin/n512/b1` | 70.9188 | 38.0659 | 32.6533 |
| `svd_thin/n512/b4` | 285.2033 | 153.0082 | 142.6568 |
| `svd_values/n256/b1` | 7.5213 | 8.3836 | 4.2443 |
| `svd_values/n256/b4` | 30.0667 | 31.3605 | 17.0695 |
| `svd_values/n512/b1` | 40.8350 | 35.4161 | 15.8228 |
| `svd_values/n512/b4` | 167.9492 | 142.8730 | 67.1570 |
| `triangular_solve/n256/b1` | 0.0103 | 0.0191 | 0.0151 |
| `triangular_solve/n256/b4` | 0.0454 | 0.0643 | 0.0747 |
| `triangular_solve/n512/b1` | 0.0342 | 0.0443 | 0.0569 |
| `triangular_solve/n512/b4` | 0.1593 | 0.1717 | 0.2600 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7044 | - | 1.0919 |
| `cholesky/n256/b4` | 2.8834 | - | 4.4261 |
| `cholesky/n512/b1` | 4.7975 | - | 7.5341 |
| `cholesky/n512/b4` | 19.3406 | - | 26.2238 |
| `eigh/n256/b1` | 10.2670 | - | 20.8155 |
| `eigh/n256/b4` | 41.2117 | - | 84.3893 |
| `eigh/n512/b1` | 62.9383 | - | 153.7338 |
| `eigh/n512/b4` | 252.6512 | - | 608.8685 |
| `eigvalsh/n256/b1` | 18.3557 | - | 8.0993 |
| `eigvalsh/n256/b4` | 73.6821 | - | 32.5244 |
| `eigvalsh/n512/b1` | 133.2473 | - | 58.0310 |
| `eigvalsh/n512/b4` | 532.8075 | - | 232.9779 |
| `householder_apply/n256/b1` | 5.0574 | - | 6.3137 |
| `householder_apply/n256/b4` | 21.5697 | - | 24.6524 |
| `householder_apply/n512/b1` | 43.0655 | - | 37.0734 |
| `householder_apply/n512/b4` | 175.9385 | - | 151.6826 |
| `householder_factor/n256/b1` | 3.3252 | - | 3.2975 |
| `householder_factor/n256/b4` | 13.4340 | - | 13.3278 |
| `householder_factor/n512/b1` | 27.5968 | - | 22.6784 |
| `householder_factor/n512/b4` | 111.6567 | - | 92.1742 |
| `lu/n256/b1` | 1.2724 | - | 1.6262 |
| `lu/n256/b4` | 5.2060 | - | 6.8443 |
| `lu/n512/b1` | 8.7133 | - | 11.1241 |
| `lu/n512/b4` | 34.6376 | - | 44.3824 |
| `lu_factor/n256/b1` | 1.1236 | - | 1.5413 |
| `lu_factor/n256/b4` | 4.4947 | - | 6.2779 |
| `lu_factor/n512/b1` | 8.0298 | - | 10.3314 |
| `lu_factor/n512/b4` | 32.6573 | - | 42.1760 |
| `lu_factor_solve/n256/b1` | 1.1881 | - | 1.6666 |
| `lu_factor_solve/n256/b4` | 4.7424 | - | 6.8132 |
| `lu_factor_solve/n512/b1` | 8.2465 | - | 10.7579 |
| `lu_factor_solve/n512/b4` | 33.7713 | - | 43.2393 |
| `lu_solve_prepared/n256/b1` | 0.0618 | - | 0.1148 |
| `lu_solve_prepared/n256/b4` | 0.2644 | - | 0.5238 |
| `lu_solve_prepared/n512/b1` | 0.2199 | - | 0.4157 |
| `lu_solve_prepared/n512/b4` | 1.0654 | - | 2.1180 |
| `qr/n256/b1` | 6.2205 | - | 7.2470 |
| `qr/n256/b4` | 24.8823 | - | 28.9889 |
| `qr/n512/b1` | 42.4086 | - | 47.1938 |
| `qr/n512/b4` | 168.7441 | - | 191.1973 |
| `rank_revealing_qr/n256/b1` | 6.7126 | - | 10.2556 |
| `rank_revealing_qr/n256/b4` | 26.9433 | - | 41.2699 |
| `rank_revealing_qr/n512/b1` | 47.7658 | - | 65.3558 |
| `rank_revealing_qr/n512/b4` | 189.8034 | - | 258.1951 |
| `solve/n256/b1` | 1.1789 | - | 1.7508 |
| `solve/n256/b4` | 4.6892 | - | 6.7834 |
| `solve/n512/b1` | 8.2137 | - | 11.1976 |
| `solve/n512/b4` | 32.7261 | - | 43.7226 |
| `svd_thin/n256/b1` | 23.8003 | - | 26.8471 |
| `svd_thin/n256/b4` | 95.6450 | - | 113.8571 |
| `svd_thin/n512/b1` | 152.0536 | - | 188.5526 |
| `svd_thin/n512/b4` | 606.7041 | - | 770.0631 |
| `svd_values/n256/b1` | 11.7637 | - | 12.4954 |
| `svd_values/n256/b4` | 47.1905 | - | 52.4830 |
| `svd_values/n512/b1` | 68.8469 | - | 93.0480 |
| `svd_values/n512/b4` | 280.7638 | - | 392.0705 |
| `triangular_solve/n256/b1` | 0.0338 | - | 0.0640 |
| `triangular_solve/n256/b4` | 0.1470 | - | 0.2651 |
| `triangular_solve/n512/b1` | 0.1158 | - | 0.2423 |
| `triangular_solve/n512/b4` | 0.5943 | - | 1.0352 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6987 | 0.4919 | 0.3549 |
| `cholesky/n256/b4` | 2.7944 | 1.9462 | 1.3782 |
| `cholesky/n512/b1` | 4.7200 | 2.4352 | 1.8997 |
| `cholesky/n512/b4` | 19.6209 | 10.3163 | 9.1720 |
| `eigh/n256/b1` | 10.2578 | 7.9518 | 9.5645 |
| `eigh/n256/b4` | 41.2300 | 31.9605 | 38.6719 |
| `eigh/n512/b1` | 62.9365 | 28.9809 | 54.6412 |
| `eigh/n512/b4` | 251.7707 | 115.9491 | 219.6780 |
| `eigvalsh/n256/b1` | 18.2928 | 19.1810 | 3.9500 |
| `eigvalsh/n256/b4` | 73.8301 | 74.9141 | 15.8660 |
| `eigvalsh/n512/b1` | 133.2147 | 123.9754 | 21.4917 |
| `eigvalsh/n512/b4` | 532.2259 | 494.0737 | 85.9844 |
| `householder_apply/n256/b1` | 5.0928 | 5.1478 | 1.6326 |
| `householder_apply/n256/b4` | 21.3441 | 21.2917 | 6.8236 |
| `householder_apply/n512/b1` | 43.1890 | 42.6675 | 9.7408 |
| `householder_apply/n512/b4` | 171.8230 | 171.5240 | 39.4417 |
| `householder_factor/n256/b1` | 3.3347 | 3.3883 | 0.9467 |
| `householder_factor/n256/b4` | 13.3475 | 13.3744 | 3.7757 |
| `householder_factor/n512/b1` | 27.8837 | 27.5890 | 6.7985 |
| `householder_factor/n512/b4` | 112.1064 | 111.6637 | 27.3222 |
| `lu/n256/b1` | 1.2739 | 0.8245 | 0.5397 |
| `lu/n256/b4` | 5.0577 | 3.3278 | 2.3647 |
| `lu/n512/b1` | 8.7097 | 3.9080 | 3.8168 |
| `lu/n512/b4` | 34.6298 | 15.3631 | 14.6833 |
| `lu_factor/n256/b1` | 1.1171 | 0.6660 | 0.4306 |
| `lu_factor/n256/b4` | 4.5020 | 2.3025 | 1.7325 |
| `lu_factor/n512/b1` | 8.0371 | 3.0984 | 3.0307 |
| `lu_factor/n512/b4` | 32.9756 | 9.1062 | 12.3297 |
| `lu_factor_solve/n256/b1` | 1.1848 | 0.7354 | 0.4869 |
| `lu_factor_solve/n256/b4` | 4.7476 | 1.2351 | 1.9580 |
| `lu_factor_solve/n512/b1` | 8.2078 | 3.2892 | 3.2579 |
| `lu_factor_solve/n512/b4` | 33.6102 | 9.5457 | 13.1249 |
| `lu_solve_prepared/n256/b1` | 0.0651 | 0.0615 | 0.0535 |
| `lu_solve_prepared/n256/b4` | 0.2645 | 0.0697 | 0.2152 |
| `lu_solve_prepared/n512/b1` | 0.2076 | 0.1590 | 0.2030 |
| `lu_solve_prepared/n512/b4` | 1.0984 | 0.3453 | 1.2469 |
| `qr/n256/b1` | 6.2411 | 3.1386 | 2.7983 |
| `qr/n256/b4` | 24.8717 | 12.5592 | 11.2289 |
| `qr/n512/b1` | 42.2603 | 14.5279 | 16.7146 |
| `qr/n512/b4` | 169.6457 | 58.6181 | 68.1266 |
| `rank_revealing_qr/n256/b1` | 6.7869 | 3.7925 | 7.8297 |
| `rank_revealing_qr/n256/b4` | 27.1053 | 15.6832 | 31.5182 |
| `rank_revealing_qr/n512/b1` | 47.7584 | 16.9040 | 45.0697 |
| `rank_revealing_qr/n512/b4` | 192.3543 | 68.1180 | 182.4953 |
| `solve/n256/b1` | 1.1800 | 0.7522 | 0.5241 |
| `solve/n256/b4` | 4.6745 | 2.9854 | 2.1495 |
| `solve/n512/b1` | 8.1894 | 3.3611 | 3.2896 |
| `solve/n512/b4` | 32.7580 | 13.3284 | 13.9334 |
| `svd_thin/n256/b1` | 23.9585 | 15.4131 | 13.6902 |
| `svd_thin/n256/b4` | 95.9462 | 61.0880 | 57.4359 |
| `svd_thin/n512/b1` | 151.6201 | 66.6555 | 79.8434 |
| `svd_thin/n512/b4` | 607.2824 | 267.8222 | 329.2537 |
| `svd_values/n256/b1` | 11.8323 | 11.9632 | 8.1475 |
| `svd_values/n256/b4` | 47.3371 | 47.2662 | 31.8371 |
| `svd_values/n512/b1` | 68.3946 | 45.2191 | 36.3560 |
| `svd_values/n512/b4` | 284.0903 | 189.1949 | 175.2737 |
| `triangular_solve/n256/b1` | 0.0336 | 0.0333 | 0.0261 |
| `triangular_solve/n256/b4` | 0.1356 | 0.1301 | 0.1123 |
| `triangular_solve/n512/b1` | 0.1144 | 0.0850 | 0.1001 |
| `triangular_solve/n512/b4` | 0.5175 | 0.3779 | 0.5611 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6883 | 0.4782 | 0.2657 |
| `cholesky/n256/b4` | 2.8521 | 1.9788 | 1.1523 |
| `cholesky/n512/b1` | 4.7376 | 1.8164 | 1.0907 |
| `cholesky/n512/b4` | 19.6825 | 7.7226 | 5.3646 |
| `eigh/n256/b1` | 10.3190 | 6.8998 | 7.8238 |
| `eigh/n256/b4` | 41.3072 | 28.0217 | 31.8268 |
| `eigh/n512/b1` | 63.3200 | 23.9791 | 39.4118 |
| `eigh/n512/b4` | 253.0727 | 96.9084 | 159.2055 |
| `eigvalsh/n256/b1` | 18.3028 | 19.1821 | 3.5648 |
| `eigvalsh/n256/b4` | 73.7876 | 74.8426 | 14.3441 |
| `eigvalsh/n512/b1` | 133.3239 | 122.4697 | 17.4356 |
| `eigvalsh/n512/b4` | 534.9427 | 488.0139 | 69.7976 |
| `householder_apply/n256/b1` | 5.2014 | 5.2298 | 0.8698 |
| `householder_apply/n256/b4` | 21.4104 | 21.4770 | 3.6069 |
| `householder_apply/n512/b1` | 41.7209 | 41.1848 | 5.0561 |
| `householder_apply/n512/b4` | 174.4690 | 174.5069 | 20.6605 |
| `householder_factor/n256/b1` | 3.3402 | 3.3861 | 0.9476 |
| `householder_factor/n256/b4` | 13.4161 | 13.4774 | 3.8239 |
| `householder_factor/n512/b1` | 27.0458 | 26.7864 | 3.4084 |
| `householder_factor/n512/b4` | 108.7575 | 108.8231 | 13.5134 |
| `lu/n256/b1` | 1.2596 | 0.8469 | 0.4094 |
| `lu/n256/b4` | 5.1787 | 3.4728 | 1.7840 |
| `lu/n512/b1` | 8.6792 | 3.3367 | 2.4049 |
| `lu/n512/b4` | 34.7908 | 13.3253 | 9.7343 |
| `lu_factor/n256/b1` | 1.1118 | 0.6595 | 0.2938 |
| `lu_factor/n256/b4` | 4.4531 | 2.6719 | 1.1744 |
| `lu_factor/n512/b1` | 7.9952 | 2.5743 | 1.7194 |
| `lu_factor/n512/b4` | 32.6356 | 10.3910 | 6.9819 |
| `lu_factor_solve/n256/b1` | 1.1773 | 0.7296 | 0.3523 |
| `lu_factor_solve/n256/b4` | 4.7332 | 2.9225 | 1.4299 |
| `lu_factor_solve/n512/b1` | 8.1985 | 2.6898 | 1.9496 |
| `lu_factor_solve/n512/b4` | 33.5862 | 11.1121 | 7.9287 |
| `lu_solve_prepared/n256/b1` | 0.0635 | 0.0675 | 0.0520 |
| `lu_solve_prepared/n256/b4` | 0.2530 | 0.2813 | 0.2174 |
| `lu_solve_prepared/n512/b1` | 0.2214 | 0.1729 | 0.2010 |
| `lu_solve_prepared/n512/b4` | 1.3023 | 0.9699 | 1.2695 |
| `qr/n256/b1` | 6.1989 | 3.4899 | 2.2093 |
| `qr/n256/b4` | 24.9382 | 14.0523 | 8.9854 |
| `qr/n512/b1` | 42.3880 | 12.4673 | 9.2965 |
| `qr/n512/b4` | 169.5678 | 49.5569 | 38.5087 |
| `rank_revealing_qr/n256/b1` | 6.7443 | 3.9462 | 6.4075 |
| `rank_revealing_qr/n256/b4` | 27.1471 | 15.8950 | 25.6292 |
| `rank_revealing_qr/n512/b1` | 48.0800 | 12.1900 | 36.5319 |
| `rank_revealing_qr/n512/b4` | 192.1298 | 49.3192 | 146.2336 |
| `solve/n256/b1` | 1.1742 | 0.7548 | 0.4127 |
| `solve/n256/b4` | 4.6890 | 2.9982 | 1.6076 |
| `solve/n512/b1` | 8.1953 | 2.8601 | 2.0342 |
| `solve/n512/b4` | 32.7304 | 11.2930 | 8.5207 |
| `svd_thin/n256/b1` | 24.0515 | 14.5035 | 11.5511 |
| `svd_thin/n256/b4` | 95.9100 | 59.9573 | 46.3052 |
| `svd_thin/n512/b1` | 151.5592 | 55.3214 | 57.0365 |
| `svd_thin/n512/b4` | 606.5448 | 221.0807 | 241.1148 |
| `svd_values/n256/b1` | 11.7773 | 12.0995 | 6.5439 |
| `svd_values/n256/b4` | 47.3364 | 47.7684 | 27.1361 |
| `svd_values/n512/b1` | 68.6726 | 43.8140 | 28.8276 |
| `svd_values/n512/b4` | 283.4378 | 181.1208 | 130.3924 |
| `triangular_solve/n256/b1` | 0.0333 | 0.0371 | 0.0261 |
| `triangular_solve/n256/b4` | 0.1430 | 0.1448 | 0.1153 |
| `triangular_solve/n512/b1` | 0.1129 | 0.0901 | 0.0998 |
| `triangular_solve/n512/b4` | 0.5414 | 0.4093 | 0.6835 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5381 | - | 0.4441 |
| `householder_factor/4096x256/b1` | 41.0049 | - | 17.5351 |
| `qr/1024x64/b1` | 0.9753 | - | 0.9186 |
| `qr/4096x256/b1` | 40.9342 | - | 41.9949 |
| `rank_revealing_qr/1024x64/b1` | 0.9711 | - | 1.1904 |
| `rank_revealing_qr/4096x256/b1` | 65.1845 | - | 60.6620 |
| `svd_thin/1024x64/b1` | 1.4532 | - | 2.2696 |
| `svd_thin/4096x256/b1` | 72.1550 | - | 77.0011 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5366 | 0.5423 | 0.2369 |
| `householder_factor/4096x256/b1` | 41.4993 | 41.5474 | 6.7326 |
| `qr/1024x64/b1` | 0.9806 | 0.8879 | 0.5731 |
| `qr/4096x256/b1` | 41.2806 | 20.2589 | 16.0743 |
| `rank_revealing_qr/1024x64/b1` | 0.9735 | 0.7356 | 1.0113 |
| `rank_revealing_qr/4096x256/b1` | 64.0542 | 23.9703 | 40.6154 |
| `svd_thin/1024x64/b1` | 1.4592 | 1.3689 | 1.6932 |
| `svd_thin/4096x256/b1` | 72.7830 | 40.7877 | 47.8313 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5369 | 0.5468 | 0.1668 |
| `householder_factor/4096x256/b1` | 42.0763 | 42.0618 | 3.7518 |
| `qr/1024x64/b1` | 0.9769 | 1.1334 | 0.5022 |
| `qr/4096x256/b1` | 41.8669 | 19.8958 | 11.5034 |
| `rank_revealing_qr/1024x64/b1` | 0.9722 | 0.7619 | 1.0108 |
| `rank_revealing_qr/4096x256/b1` | 66.5780 | 18.6573 | 38.8454 |
| `svd_thin/1024x64/b1` | 1.4567 | 1.6122 | 1.5605 |
| `svd_thin/4096x256/b1` | 72.3876 | 32.9868 | 41.1491 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1642 | - | 1.3228 |
| `householder_factor/4096x256/b1` | 121.5997 | - | 66.6939 |
| `qr/1024x64/b1` | 2.8727 | - | 2.8547 |
| `qr/4096x256/b1` | 146.2504 | - | 135.6972 |
| `rank_revealing_qr/1024x64/b1` | 2.8593 | - | 3.7939 |
| `rank_revealing_qr/4096x256/b1` | 244.4570 | - | 186.6904 |
| `svd_thin/1024x64/b1` | 3.5330 | - | 5.6544 |
| `svd_thin/4096x256/b1` | 230.6990 | - | 250.6100 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1602 | 1.1960 | 0.7857 |
| `householder_factor/4096x256/b1` | 121.3561 | 121.5327 | 19.5146 |
| `qr/1024x64/b1` | 2.8385 | 1.6287 | 1.7980 |
| `qr/4096x256/b1` | 147.5708 | 57.9210 | 46.9596 |
| `rank_revealing_qr/1024x64/b1` | 2.8597 | 1.7661 | 3.1740 |
| `rank_revealing_qr/4096x256/b1` | 245.7929 | 82.9418 | 130.2305 |
| `svd_thin/1024x64/b1` | 3.5311 | 2.2799 | 3.8231 |
| `svd_thin/4096x256/b1` | 231.2053 | 103.6857 | 113.8783 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1640 | 1.2091 | 0.4812 |
| `householder_factor/4096x256/b1` | 120.9450 | 121.1379 | 11.2044 |
| `qr/1024x64/b1` | 2.8314 | 1.7327 | 1.3211 |
| `qr/4096x256/b1` | 146.2977 | 45.9939 | 28.5108 |
| `rank_revealing_qr/1024x64/b1` | 2.8422 | 1.7008 | 2.9476 |
| `rank_revealing_qr/4096x256/b1` | 242.7963 | 52.6741 | 113.2724 |
| `svd_thin/1024x64/b1` | 3.5440 | 2.4904 | 3.2511 |
| `svd_thin/4096x256/b1` | 230.5500 | 79.8390 | 82.4840 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
