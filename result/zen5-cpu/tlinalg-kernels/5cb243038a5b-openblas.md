<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261012T223213Z/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `5cb243038a5be260a77a62cfcd4a73bb60d5f9c0`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.24.4 @ `4f691336c74814369ab23cce9391801ecf429bfa` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=4f691336c74814369ab23cce9391801ecf429bfa#4f691336c74814369ab23cce9391801ecf429bfa); `t4a-faer-traits` 0.24.0 @ `4f691336c74814369ab23cce9391801ecf429bfa` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=4f691336c74814369ab23cce9391801ecf429bfa#4f691336c74814369ab23cce9391801ecf429bfa)
- harness commit: `26fa64b218e1dbb5942c82db1803551d1c34944c`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-12T23:28:11.043169Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261012T223213Z/`

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
    As measured: `t4a-faer` 0.24.4 @ `4f691336c74814369ab23cce9391801ecf429bfa` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=4f691336c74814369ab23cce9391801ecf429bfa#4f691336c74814369ab23cce9391801ecf429bfa); `t4a-faer-traits` 0.24.0 @ `4f691336c74814369ab23cce9391801ecf429bfa` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=4f691336c74814369ab23cce9391801ecf429bfa#4f691336c74814369ab23cce9391801ecf429bfa)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `t4a-faer` 0.24.4 @ `4f691336c74814369ab23cce9391801ecf429bfa` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=4f691336c74814369ab23cce9391801ecf429bfa#4f691336c74814369ab23cce9391801ecf429bfa); `t4a-faer-traits` 0.24.0 @ `4f691336c74814369ab23cce9391801ecf429bfa` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=4f691336c74814369ab23cce9391801ecf429bfa#4f691336c74814369ab23cce9391801ecf429bfa)
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
| `cholesky/n16/b1024` | 0.5270 | - | 0.6235 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1065 | - | 0.1141 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2121 | - | 0.2411 |
| `eig/n16/b1` | 0.0535 | - | 0.0404 |
| `eig/n16/b1024` | 55.7718 | - | 41.4883 |
| `eig/n4/b1` | 0.0039 | - | 0.0037 |
| `eig/n4/b1024` | 3.5182 | - | 3.2925 |
| `eig/n8/b1` | 0.0141 | - | 0.0112 |
| `eig/n8/b1024` | 13.8283 | - | 10.6626 |
| `eigh/n16/b1` | 0.0176 | - | 0.0232 |
| `eigh/n16/b1024` | 17.8501 | - | 24.0658 |
| `eigh/n4/b1` | 0.0017 | - | 0.0019 |
| `eigh/n4/b1024` | 1.4517 | - | 1.7947 |
| `eigh/n8/b1` | 0.0051 | - | 0.0063 |
| `eigh/n8/b1024` | 5.0700 | - | 6.4866 |
| `eigvals/n16/b1` | 0.0371 | - | 0.0291 |
| `eigvals/n16/b1024` | 38.9864 | - | 29.9116 |
| `eigvals/n4/b1` | 0.0024 | - | 0.0026 |
| `eigvals/n4/b1024` | 2.0089 | - | 2.0953 |
| `eigvals/n8/b1` | 0.0098 | - | 0.0086 |
| `eigvals/n8/b1024` | 9.1750 | - | 8.0134 |
| `eigvalsh/n16/b1` | 0.0132 | - | 0.0084 |
| `eigvalsh/n16/b1024` | 13.2701 | - | 8.6607 |
| `eigvalsh/n4/b1` | 0.0013 | - | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1653 | - | 0.8331 |
| `eigvalsh/n8/b1` | 0.0042 | - | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0643 | - | 2.7102 |
| `full_piv_lu/n16/b1` | 0.0024 | - | 0.0027 |
| `full_piv_lu/n16/b1024` | 1.9478 | - | 2.9448 |
| `full_piv_lu/n4/b1` | 0.0005 | - | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2221 | - | 0.2226 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6075 | - | 0.6147 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | - | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0902 | - | 3.7545 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | - | 0.0006 |
| `full_piv_lu_solve/n4/b1024` | 0.3069 | - | 0.4146 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0012 |
| `full_piv_lu_solve/n8/b1024` | 0.7838 | - | 0.9967 |
| `householder_apply/n16/b1` | 0.0029 | - | 0.0029 |
| `householder_apply/n16/b1024` | 2.9026 | - | 2.6592 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0006 |
| `householder_apply/n4/b1024` | 0.2147 | - | 0.2505 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0011 |
| `householder_apply/n8/b1024` | 0.6978 | - | 0.7280 |
| `householder_factor/n16/b1` | 0.0023 | - | 0.0027 |
| `householder_factor/n16/b1024` | 2.2253 | - | 2.6064 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.2627 | - | 0.3220 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.7096 | - | 0.9026 |
| `lu/n16/b1` | 0.0019 | - | 0.0017 |
| `lu/n16/b1024` | 1.5621 | - | 1.4322 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.1683 | - | 0.1935 |
| `lu/n8/b1` | 0.0007 | - | 0.0006 |
| `lu/n8/b1024` | 0.4904 | - | 0.4811 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0011 |
| `lu_factor/n16/b1024` | 1.0793 | - | 1.0857 |
| `lu_factor/n4/b1` | 0.0003 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1332 | - | 0.1285 |
| `lu_factor/n8/b1` | 0.0005 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3516 | - | 0.3380 |
| `lu_factor_solve/n16/b1` | 0.0017 | - | 0.0019 |
| `lu_factor_solve/n16/b1024` | 1.4110 | - | 1.8318 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.1643 | - | 0.3139 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0007 |
| `lu_factor_solve/n8/b1024` | 0.4806 | - | 0.6419 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0008 |
| `lu_solve_prepared/n16/b1024` | 0.3551 | - | 0.7187 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | - | 0.1913 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1368 | - | 0.3093 |
| `qr/n16/b1` | 0.0054 | - | 0.0048 |
| `qr/n16/b1024` | 5.2576 | - | 4.6801 |
| `qr/n4/b1` | 0.0008 | - | 0.0008 |
| `qr/n4/b1024` | 0.4479 | - | 0.5744 |
| `qr/n8/b1` | 0.0016 | - | 0.0018 |
| `qr/n8/b1024` | 1.3829 | - | 1.5797 |
| `rank_revealing_qr/n16/b1` | 0.0065 | - | 0.0060 |
| `rank_revealing_qr/n16/b1024` | 6.1408 | - | 5.6129 |
| `rank_revealing_qr/n4/b1` | 0.0010 | - | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6924 | - | 0.6944 |
| `rank_revealing_qr/n8/b1` | 0.0022 | - | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8563 | - | 1.8152 |
| `solve/n16/b1` | 0.0021 | - | 0.0024 |
| `solve/n16/b1024` | 1.5232 | - | 1.9123 |
| `solve/n4/b1` | 0.0006 | - | 0.0006 |
| `solve/n4/b1024` | 0.2203 | - | 0.3373 |
| `solve/n8/b1` | 0.0009 | - | 0.0010 |
| `solve/n8/b1024` | 0.5265 | - | 0.6700 |
| `svd_full/n16/b1` | 0.0327 | - | 0.0491 |
| `svd_full/n16/b1024` | 33.5078 | - | 48.7887 |
| `svd_full/n4/b1` | 0.0027 | - | 0.0043 |
| `svd_full/n4/b1024` | 2.5047 | - | 3.8689 |
| `svd_full/n8/b1` | 0.0089 | - | 0.0126 |
| `svd_full/n8/b1024` | 8.9943 | - | 12.7924 |
| `svd_thin/n16/b1` | 0.0326 | - | 0.0489 |
| `svd_thin/n16/b1024` | 33.6056 | - | 48.7405 |
| `svd_thin/n4/b1` | 0.0029 | - | 0.0043 |
| `svd_thin/n4/b1024` | 2.5035 | - | 3.8505 |
| `svd_thin/n8/b1` | 0.0091 | - | 0.0125 |
| `svd_thin/n8/b1024` | 9.0650 | - | 12.8511 |
| `svd_values/n16/b1` | 0.0239 | - | 0.0149 |
| `svd_values/n16/b1024` | 24.5043 | - | 15.0679 |
| `svd_values/n4/b1` | 0.0021 | - | 0.0026 |
| `svd_values/n4/b1024` | 1.8904 | - | 2.1307 |
| `svd_values/n8/b1` | 0.0068 | - | 0.0056 |
| `svd_values/n8/b1024` | 6.7396 | - | 5.3966 |
| `triangular_solve/n16/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3012 | - | 0.3980 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0514 | - | 0.1182 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1304 | - | 0.1810 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0022 | 0.0007 |
| `cholesky/n16/b1024` | 0.5146 | 0.2626 | 0.6024 |
| `cholesky/n4/b1` | 0.0002 | 0.0028 | 0.0002 |
| `cholesky/n4/b1024` | 0.1075 | 0.0316 | 0.1172 |
| `cholesky/n8/b1` | 0.0003 | 0.0027 | 0.0003 |
| `cholesky/n8/b1024` | 0.2270 | 0.0579 | 0.2328 |
| `eig/n16/b1` | 0.0535 | 0.0577 | 0.0410 |
| `eig/n16/b1024` | 55.7074 | 14.0381 | 41.8520 |
| `eig/n4/b1` | 0.0039 | 0.0063 | 0.0037 |
| `eig/n4/b1024` | 3.5110 | 1.1870 | 3.3313 |
| `eig/n8/b1` | 0.0143 | 0.0171 | 0.0113 |
| `eig/n8/b1024` | 13.6301 | 3.4403 | 10.6680 |
| `eigh/n16/b1` | 0.0178 | 0.0207 | 0.0236 |
| `eigh/n16/b1024` | 18.0205 | 7.6765 | 23.9780 |
| `eigh/n4/b1` | 0.0017 | 0.0041 | 0.0019 |
| `eigh/n4/b1024` | 1.4503 | 0.7272 | 1.8074 |
| `eigh/n8/b1` | 0.0052 | 0.0070 | 0.0064 |
| `eigh/n8/b1024` | 5.0632 | 1.2903 | 6.6078 |
| `eigvals/n16/b1` | 0.0371 | 0.0400 | 0.0292 |
| `eigvals/n16/b1024` | 38.9423 | 15.9860 | 30.0075 |
| `eigvals/n4/b1` | 0.0024 | 0.0046 | 0.0026 |
| `eigvals/n4/b1024` | 1.9177 | 0.9651 | 2.0965 |
| `eigvals/n8/b1` | 0.0098 | 0.0126 | 0.0086 |
| `eigvals/n8/b1024` | 9.1696 | 3.0906 | 7.9922 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0161 | 0.0084 |
| `eigvalsh/n16/b1024` | 13.2269 | 6.2147 | 8.6841 |
| `eigvalsh/n4/b1` | 0.0014 | 0.0033 | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1633 | 0.5883 | 0.8288 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0070 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0267 | 1.9341 | 2.7271 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0050 | 0.0026 |
| `full_piv_lu/n16/b1024` | 1.9305 | 1.0174 | 2.8230 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0022 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2249 | 0.1192 | 0.2203 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0034 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6124 | 0.3128 | 0.6086 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0049 | 0.0040 |
| `full_piv_lu_solve/n16/b1024` | 2.1069 | 0.6652 | 3.9149 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0025 | 0.0007 |
| `full_piv_lu_solve/n4/b1024` | 0.3074 | 0.0933 | 0.5559 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0037 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7829 | 0.4024 | 1.2007 |
| `householder_apply/n16/b1` | 0.0028 | 0.0051 | 0.0030 |
| `householder_apply/n16/b1024` | 2.8721 | 0.7575 | 2.6724 |
| `householder_apply/n4/b1` | 0.0003 | 0.0025 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2104 | 0.0613 | 0.2496 |
| `householder_apply/n8/b1` | 0.0008 | 0.0033 | 0.0011 |
| `householder_apply/n8/b1024` | 0.7054 | 0.1972 | 0.7258 |
| `householder_factor/n16/b1` | 0.0022 | 0.0043 | 0.0027 |
| `householder_factor/n16/b1024` | 2.1686 | 0.5500 | 2.6078 |
| `householder_factor/n4/b1` | 0.0003 | 0.0027 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2599 | 0.0715 | 0.3219 |
| `householder_factor/n8/b1` | 0.0008 | 0.0033 | 0.0011 |
| `householder_factor/n8/b1024` | 0.7325 | 0.1878 | 0.9042 |
| `lu/n16/b1` | 0.0019 | 0.0043 | 0.0017 |
| `lu/n16/b1024` | 1.5663 | 0.7949 | 1.4152 |
| `lu/n4/b1` | 0.0004 | 0.0027 | 0.0003 |
| `lu/n4/b1024` | 0.1689 | 0.0892 | 0.1944 |
| `lu/n8/b1` | 0.0007 | 0.0032 | 0.0006 |
| `lu/n8/b1024` | 0.4723 | 0.2484 | 0.4820 |
| `lu_factor/n16/b1` | 0.0014 | 0.0039 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1290 | 0.2903 | 1.0771 |
| `lu_factor/n4/b1` | 0.0004 | 0.0023 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1333 | 0.0416 | 0.1286 |
| `lu_factor/n8/b1` | 0.0006 | 0.0029 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3563 | 0.0937 | 0.3392 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0044 | 0.0021 |
| `lu_factor_solve/n16/b1024` | 1.4610 | 0.3705 | 2.0441 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0027 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1693 | 0.0470 | 0.6702 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0024 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.4880 | 0.1380 | 0.8968 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0027 | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.3562 | 0.1917 | 0.6847 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0400 | 0.0202 | 0.5043 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0030 | 0.0008 |
| `lu_solve_prepared/n8/b1024` | 0.1372 | 0.0465 | 0.4861 |
| `qr/n16/b1` | 0.0056 | 0.0087 | 0.0049 |
| `qr/n16/b1024` | 5.3207 | 2.6957 | 4.7548 |
| `qr/n4/b1` | 0.0007 | 0.0023 | 0.0008 |
| `qr/n4/b1024` | 0.4452 | 0.1144 | 0.5748 |
| `qr/n8/b1` | 0.0016 | 0.0033 | 0.0018 |
| `qr/n8/b1024` | 1.4524 | 0.3729 | 1.5853 |
| `rank_revealing_qr/n16/b1` | 0.0067 | 0.0096 | 0.0060 |
| `rank_revealing_qr/n16/b1024` | 6.2082 | 3.1448 | 5.6060 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0036 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6932 | 0.3532 | 0.6982 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0045 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8859 | 0.4951 | 1.8181 |
| `solve/n16/b1` | 0.0022 | 0.0038 | 0.0023 |
| `solve/n16/b1024` | 1.5757 | 0.3975 | 1.9653 |
| `solve/n4/b1` | 0.0006 | 0.0025 | 0.0008 |
| `solve/n4/b1024` | 0.2135 | 0.0636 | 0.7828 |
| `solve/n8/b1` | 0.0010 | 0.0035 | 0.0011 |
| `solve/n8/b1024` | 0.5413 | 0.2751 | 1.1654 |
| `svd_full/n16/b1` | 0.0329 | 0.0357 | 0.0489 |
| `svd_full/n16/b1024` | 33.5410 | 15.6387 | 48.4680 |
| `svd_full/n4/b1` | 0.0028 | 0.0053 | 0.0043 |
| `svd_full/n4/b1024` | 2.5154 | 1.0866 | 3.8409 |
| `svd_full/n8/b1` | 0.0090 | 0.0119 | 0.0126 |
| `svd_full/n8/b1024` | 9.0791 | 4.5576 | 13.0347 |
| `svd_thin/n16/b1` | 0.0326 | 0.0359 | 0.0487 |
| `svd_thin/n16/b1024` | 33.8624 | 8.9126 | 48.7987 |
| `svd_thin/n4/b1` | 0.0031 | 0.0047 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5383 | 0.6318 | 3.8530 |
| `svd_thin/n8/b1` | 0.0091 | 0.0117 | 0.0125 |
| `svd_thin/n8/b1024` | 9.0920 | 4.5770 | 12.9532 |
| `svd_values/n16/b1` | 0.0239 | 0.0268 | 0.0150 |
| `svd_values/n16/b1024` | 24.3633 | 7.6687 | 15.1583 |
| `svd_values/n4/b1` | 0.0021 | 0.0043 | 0.0025 |
| `svd_values/n4/b1024` | 1.8855 | 0.4788 | 2.1470 |
| `svd_values/n8/b1` | 0.0068 | 0.0097 | 0.0056 |
| `svd_values/n8/b1024` | 6.7079 | 3.3904 | 5.4217 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0027 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3019 | 0.1560 | 0.6796 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0029 | 0.0005 |
| `triangular_solve/n4/b1024` | 0.0509 | 0.0292 | 0.4385 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0027 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.1304 | 0.0414 | 0.5434 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0025 | 0.0007 |
| `cholesky/n16/b1024` | 0.5319 | 0.0710 | 0.6136 |
| `cholesky/n4/b1` | 0.0002 | 0.0025 | 0.0002 |
| `cholesky/n4/b1024` | 0.1062 | 0.0216 | 0.1182 |
| `cholesky/n8/b1` | 0.0003 | 0.0028 | 0.0003 |
| `cholesky/n8/b1024` | 0.2179 | 0.0357 | 0.2448 |
| `eig/n16/b1` | 0.0535 | 0.0567 | 0.0407 |
| `eig/n16/b1024` | 55.9339 | 7.5390 | 41.4756 |
| `eig/n4/b1` | 0.0039 | 0.0073 | 0.0037 |
| `eig/n4/b1024` | 3.5231 | 0.8904 | 3.3405 |
| `eig/n8/b1` | 0.0143 | 0.0171 | 0.0112 |
| `eig/n8/b1024` | 13.7171 | 3.4560 | 10.6978 |
| `eigh/n16/b1` | 0.0183 | 0.0206 | 0.0231 |
| `eigh/n16/b1024` | 17.7338 | 2.2840 | 24.0858 |
| `eigh/n4/b1` | 0.0016 | 0.0044 | 0.0019 |
| `eigh/n4/b1024` | 1.4591 | 0.3664 | 1.8284 |
| `eigh/n8/b1` | 0.0051 | 0.0084 | 0.0064 |
| `eigh/n8/b1024` | 5.0464 | 0.9225 | 6.5135 |
| `eigvals/n16/b1` | 0.0372 | 0.0401 | 0.0292 |
| `eigvals/n16/b1024` | 38.8867 | 5.4843 | 29.9322 |
| `eigvals/n4/b1` | 0.0023 | 0.0058 | 0.0026 |
| `eigvals/n4/b1024` | 1.9350 | 0.2473 | 2.1016 |
| `eigvals/n8/b1` | 0.0098 | 0.0130 | 0.0086 |
| `eigvals/n8/b1024` | 9.1982 | 1.6131 | 8.0098 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0163 | 0.0085 |
| `eigvalsh/n16/b1024` | 13.2102 | 3.3363 | 8.7715 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0045 | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1630 | 0.2997 | 0.8371 |
| `eigvalsh/n8/b1` | 0.0042 | 0.0073 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0545 | 1.0229 | 2.7415 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0056 | 0.0026 |
| `full_piv_lu/n16/b1024` | 1.9571 | 0.4852 | 2.8001 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0036 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2253 | 0.0639 | 0.2215 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0044 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6154 | 0.0835 | 0.5966 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0056 | 0.0040 |
| `full_piv_lu_solve/n16/b1024` | 2.0407 | 0.5296 | 4.0450 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0024 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3020 | 0.0837 | 0.5718 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0038 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7784 | 0.2032 | 1.1940 |
| `householder_apply/n16/b1` | 0.0027 | 0.0060 | 0.0029 |
| `householder_apply/n16/b1024` | 2.7281 | 0.3604 | 2.7254 |
| `householder_apply/n4/b1` | 0.0003 | 0.0035 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2022 | 0.0541 | 0.2508 |
| `householder_apply/n8/b1` | 0.0008 | 0.0040 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6735 | 0.1809 | 0.7230 |
| `householder_factor/n16/b1` | 0.0022 | 0.0056 | 0.0028 |
| `householder_factor/n16/b1024` | 2.1663 | 0.5428 | 2.6122 |
| `householder_factor/n4/b1` | 0.0003 | 0.0039 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2608 | 0.0709 | 0.3207 |
| `householder_factor/n8/b1` | 0.0008 | 0.0028 | 0.0011 |
| `householder_factor/n8/b1024` | 0.7091 | 0.1863 | 0.9000 |
| `lu/n16/b1` | 0.0019 | 0.0049 | 0.0017 |
| `lu/n16/b1024` | 1.5654 | 0.4071 | 1.4215 |
| `lu/n4/b1` | 0.0004 | 0.0028 | 0.0004 |
| `lu/n4/b1024` | 0.1697 | 0.0479 | 0.1937 |
| `lu/n8/b1` | 0.0007 | 0.0039 | 0.0006 |
| `lu/n8/b1024` | 0.4795 | 0.0658 | 0.4805 |
| `lu_factor/n16/b1` | 0.0013 | 0.0045 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1081 | 0.2837 | 1.0945 |
| `lu_factor/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1305 | 0.0383 | 0.1308 |
| `lu_factor/n8/b1` | 0.0005 | 0.0030 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3491 | 0.0938 | 0.3418 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0050 | 0.0019 |
| `lu_factor_solve/n16/b1024` | 1.4189 | 0.3617 | 2.2812 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0021 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1643 | 0.0335 | 0.6935 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0037 | 0.0009 |
| `lu_factor_solve/n8/b1024` | 0.4864 | 0.1251 | 1.1971 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0045 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3543 | 0.1053 | 0.9412 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0038 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0404 | 0.0199 | 0.4913 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0024 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.1370 | 0.0446 | 0.7463 |
| `qr/n16/b1` | 0.0053 | 0.0080 | 0.0049 |
| `qr/n16/b1024` | 5.1912 | 0.6636 | 4.6983 |
| `qr/n4/b1` | 0.0007 | 0.0046 | 0.0008 |
| `qr/n4/b1024` | 0.4300 | 0.0638 | 0.5777 |
| `qr/n8/b1` | 0.0016 | 0.0043 | 0.0018 |
| `qr/n8/b1024` | 1.3741 | 0.3421 | 1.5772 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0097 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.1193 | 1.2531 | 5.6862 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0033 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.6948 | 0.1797 | 0.6919 |
| `rank_revealing_qr/n8/b1` | 0.0023 | 0.0053 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8798 | 0.4666 | 1.8086 |
| `solve/n16/b1` | 0.0022 | 0.0053 | 0.0023 |
| `solve/n16/b1024` | 1.5492 | 0.3954 | 2.2011 |
| `solve/n4/b1` | 0.0006 | 0.0041 | 0.0009 |
| `solve/n4/b1024` | 0.2171 | 0.0597 | 0.8407 |
| `solve/n8/b1` | 0.0010 | 0.0027 | 0.0010 |
| `solve/n8/b1024` | 0.5451 | 0.0754 | 1.2023 |
| `svd_full/n16/b1` | 0.0326 | 0.0384 | 0.0486 |
| `svd_full/n16/b1024` | 33.3036 | 5.6347 | 48.5239 |
| `svd_full/n4/b1` | 0.0029 | 0.0061 | 0.0043 |
| `svd_full/n4/b1024` | 2.4958 | 0.3481 | 3.8820 |
| `svd_full/n8/b1` | 0.0089 | 0.0113 | 0.0126 |
| `svd_full/n8/b1024` | 9.0411 | 1.1552 | 12.9945 |
| `svd_thin/n16/b1` | 0.0331 | 0.0389 | 0.0487 |
| `svd_thin/n16/b1024` | 33.2190 | 7.4533 | 48.5273 |
| `svd_thin/n4/b1` | 0.0028 | 0.0060 | 0.0043 |
| `svd_thin/n4/b1024` | 2.4964 | 0.3194 | 3.8949 |
| `svd_thin/n8/b1` | 0.0089 | 0.0120 | 0.0125 |
| `svd_thin/n8/b1024` | 9.1074 | 1.1765 | 12.7447 |
| `svd_values/n16/b1` | 0.0240 | 0.0272 | 0.0150 |
| `svd_values/n16/b1024` | 24.5495 | 4.1366 | 15.0495 |
| `svd_values/n4/b1` | 0.0021 | 0.0056 | 0.0026 |
| `svd_values/n4/b1024` | 1.8986 | 0.2461 | 2.1645 |
| `svd_values/n8/b1` | 0.0069 | 0.0103 | 0.0056 |
| `svd_values/n8/b1024` | 6.7387 | 1.3967 | 5.4361 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0024 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.2992 | 0.0491 | 0.5326 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0033 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0509 | 0.0170 | 0.4333 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0035 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1303 | 0.0367 | 0.4947 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | - | 0.0010 |
| `cholesky/n16/b1024` | 0.7565 | - | 0.9217 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1183 | - | 0.1360 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2500 | - | 0.2893 |
| `eig/n16/b1` | 0.0718 | - | 0.1000 |
| `eig/n16/b1024` | 75.9306 | - | 119.5399 |
| `eig/n4/b1` | 0.0061 | - | 0.0081 |
| `eig/n4/b1024` | 5.8283 | - | 7.9332 |
| `eig/n8/b1` | 0.0202 | - | 0.0260 |
| `eig/n8/b1024` | 20.6685 | - | 28.0320 |
| `eigh/n16/b1` | 0.0181 | - | 0.0260 |
| `eigh/n16/b1024` | 19.5541 | - | 27.0299 |
| `eigh/n4/b1` | 0.0020 | - | 0.0022 |
| `eigh/n4/b1024` | 1.7346 | - | 2.1216 |
| `eigh/n8/b1` | 0.0056 | - | 0.0071 |
| `eigh/n8/b1024` | 5.4272 | - | 7.3643 |
| `eigvals/n16/b1` | 0.0436 | - | 0.0753 |
| `eigvals/n16/b1024` | 46.5910 | - | 90.0298 |
| `eigvals/n4/b1` | 0.0031 | - | 0.0064 |
| `eigvals/n4/b1024` | 2.8652 | - | 6.0363 |
| `eigvals/n8/b1` | 0.0118 | - | 0.0211 |
| `eigvals/n8/b1024` | 12.0246 | - | 22.2883 |
| `eigvalsh/n16/b1` | 0.0136 | - | 0.0115 |
| `eigvalsh/n16/b1024` | 14.3015 | - | 11.5575 |
| `eigvalsh/n4/b1` | 0.0016 | - | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4259 | - | 1.2466 |
| `eigvalsh/n8/b1` | 0.0046 | - | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3777 | - | 3.6520 |
| `full_piv_lu/n16/b1` | 0.0029 | - | 0.0125 |
| `full_piv_lu/n16/b1024` | 2.5921 | - | 20.1693 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2643 | - | 0.5324 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7330 | - | 2.3321 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | - | 0.0152 |
| `full_piv_lu_solve/n16/b1024` | 3.1525 | - | 22.5192 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4476 | - | 1.1520 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0036 |
| `full_piv_lu_solve/n8/b1024` | 1.1831 | - | 3.5938 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0045 |
| `householder_apply/n16/b1024` | 3.3110 | - | 4.2864 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0008 |
| `householder_apply/n4/b1024` | 0.2027 | - | 0.2578 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0014 |
| `householder_apply/n8/b1024` | 0.6652 | - | 0.8919 |
| `householder_factor/n16/b1` | 0.0028 | - | 0.0045 |
| `householder_factor/n16/b1024` | 2.6805 | - | 4.4333 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0007 |
| `householder_factor/n4/b1024` | 0.3248 | - | 0.5547 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0016 |
| `householder_factor/n8/b1024` | 0.8549 | - | 1.4168 |
| `lu/n16/b1` | 0.0021 | - | 0.0024 |
| `lu/n16/b1024` | 1.9147 | - | 2.5500 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.2124 | - | 0.2271 |
| `lu/n8/b1` | 0.0008 | - | 0.0008 |
| `lu/n8/b1024` | 0.5469 | - | 0.6494 |
| `lu_factor/n16/b1` | 0.0014 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2436 | - | 1.6491 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1681 | - | 0.1625 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0005 |
| `lu_factor/n8/b1024` | 0.3957 | - | 0.4532 |
| `lu_factor_solve/n16/b1` | 0.0023 | - | 0.0026 |
| `lu_factor_solve/n16/b1024` | 2.0345 | - | 2.6731 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0005 |
| `lu_factor_solve/n4/b1024` | 0.2483 | - | 0.4074 |
| `lu_factor_solve/n8/b1` | 0.0009 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6679 | - | 0.9186 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.8066 | - | 1.0444 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0979 | - | 0.2439 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.2897 | - | 0.4524 |
| `qr/n16/b1` | 0.0068 | - | 0.0077 |
| `qr/n16/b1024` | 6.6565 | - | 7.6965 |
| `qr/n4/b1` | 0.0007 | - | 0.0011 |
| `qr/n4/b1024` | 0.5149 | - | 0.8712 |
| `qr/n8/b1` | 0.0017 | - | 0.0026 |
| `qr/n8/b1024` | 1.5803 | - | 2.2870 |
| `rank_revealing_qr/n16/b1` | 0.0075 | - | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.3492 | - | 10.1140 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8162 | - | 1.0970 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.2077 | - | 3.0046 |
| `solve/n16/b1` | 0.0027 | - | 0.0030 |
| `solve/n16/b1024` | 2.2262 | - | 2.7881 |
| `solve/n4/b1` | 0.0007 | - | 0.0007 |
| `solve/n4/b1024` | 0.3282 | - | 0.4597 |
| `solve/n8/b1` | 0.0012 | - | 0.0013 |
| `solve/n8/b1024` | 0.8098 | - | 0.9817 |
| `svd_full/n16/b1` | 0.0354 | - | 0.0551 |
| `svd_full/n16/b1024` | 37.1234 | - | 56.5666 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0052 |
| `svd_full/n4/b1024` | 2.9914 | - | 4.7125 |
| `svd_full/n8/b1` | 0.0097 | - | 0.0146 |
| `svd_full/n8/b1024` | 10.1094 | - | 14.9131 |
| `svd_thin/n16/b1` | 0.0350 | - | 0.0549 |
| `svd_thin/n16/b1024` | 36.9887 | - | 56.4229 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0052 |
| `svd_thin/n4/b1024` | 3.0051 | - | 4.7214 |
| `svd_thin/n8/b1` | 0.0097 | - | 0.0145 |
| `svd_thin/n8/b1024` | 10.1194 | - | 14.9558 |
| `svd_values/n16/b1` | 0.0260 | - | 0.0198 |
| `svd_values/n16/b1024` | 27.1904 | - | 20.1293 |
| `svd_values/n4/b1` | 0.0026 | - | 0.0032 |
| `svd_values/n4/b1024` | 2.2997 | - | 2.7530 |
| `svd_values/n8/b1` | 0.0076 | - | 0.0071 |
| `svd_values/n8/b1024` | 7.7199 | - | 6.7822 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0007 |
| `triangular_solve/n16/b1024` | 0.6182 | - | 0.5904 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0967 | - | 0.1539 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.2407 | - | 0.2851 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0033 | 0.0010 |
| `cholesky/n16/b1024` | 0.7664 | 0.3813 | 0.9720 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1172 | 0.0634 | 0.1364 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2474 | 0.0686 | 0.2936 |
| `eig/n16/b1` | 0.0715 | 0.0759 | 0.1005 |
| `eig/n16/b1024` | 75.8871 | 28.1687 | 119.3760 |
| `eig/n4/b1` | 0.0059 | 0.0093 | 0.0082 |
| `eig/n4/b1024` | 5.8888 | 2.9946 | 8.0129 |
| `eig/n8/b1` | 0.0198 | 0.0230 | 0.0262 |
| `eig/n8/b1024` | 20.3594 | 8.6798 | 28.2858 |
| `eigh/n16/b1` | 0.0181 | 0.0211 | 0.0259 |
| `eigh/n16/b1024` | 19.4450 | 7.8266 | 26.9933 |
| `eigh/n4/b1` | 0.0019 | 0.0037 | 0.0022 |
| `eigh/n4/b1024` | 1.7089 | 0.8633 | 2.1570 |
| `eigh/n8/b1` | 0.0057 | 0.0081 | 0.0072 |
| `eigh/n8/b1024` | 5.4433 | 2.7494 | 7.3954 |
| `eigvals/n16/b1` | 0.0440 | 0.0466 | 0.0750 |
| `eigvals/n16/b1024` | 46.8344 | 11.6947 | 89.5206 |
| `eigvals/n4/b1` | 0.0031 | 0.0061 | 0.0064 |
| `eigvals/n4/b1024` | 2.8191 | 1.4426 | 6.0351 |
| `eigvals/n8/b1` | 0.0117 | 0.0148 | 0.0210 |
| `eigvals/n8/b1024` | 12.0125 | 3.7028 | 22.2589 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0167 | 0.0116 |
| `eigvalsh/n16/b1024` | 14.2416 | 6.0191 | 11.5296 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0031 | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4202 | 0.7112 | 1.2520 |
| `eigvalsh/n8/b1` | 0.0046 | 0.0070 | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3663 | 2.0516 | 3.6768 |
| `full_piv_lu/n16/b1` | 0.0030 | 0.0058 | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.6798 | 1.3109 | 20.1568 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0025 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2731 | 0.1368 | 0.5399 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0037 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7227 | 0.3740 | 2.3209 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0072 | 0.0154 |
| `full_piv_lu_solve/n16/b1024` | 3.1184 | 1.3090 | 22.7931 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0025 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4438 | 0.2288 | 1.2752 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0048 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.2055 | 0.3252 | 3.6711 |
| `householder_apply/n16/b1` | 0.0028 | 0.0056 | 0.0046 |
| `householder_apply/n16/b1024` | 3.5398 | 0.9678 | 4.3767 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0008 |
| `householder_apply/n4/b1024` | 0.2014 | 0.0578 | 0.2585 |
| `householder_apply/n8/b1` | 0.0008 | 0.0025 | 0.0015 |
| `householder_apply/n8/b1024` | 0.6728 | 0.3364 | 0.8957 |
| `householder_factor/n16/b1` | 0.0027 | 0.0048 | 0.0045 |
| `householder_factor/n16/b1024` | 2.7137 | 1.3840 | 4.4771 |
| `householder_factor/n4/b1` | 0.0004 | 0.0020 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3291 | 0.0876 | 0.5580 |
| `householder_factor/n8/b1` | 0.0009 | 0.0031 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8685 | 0.4379 | 1.4257 |
| `lu/n16/b1` | 0.0021 | 0.0051 | 0.0024 |
| `lu/n16/b1024` | 1.9108 | 0.9781 | 2.5835 |
| `lu/n4/b1` | 0.0005 | 0.0022 | 0.0004 |
| `lu/n4/b1024` | 0.2109 | 0.0576 | 0.2446 |
| `lu/n8/b1` | 0.0008 | 0.0032 | 0.0009 |
| `lu/n8/b1024` | 0.5559 | 0.2816 | 0.6371 |
| `lu_factor/n16/b1` | 0.0015 | 0.0031 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2475 | 0.6465 | 1.6493 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1611 | 0.0448 | 0.1609 |
| `lu_factor/n8/b1` | 0.0006 | 0.0024 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3978 | 0.2024 | 0.4535 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0046 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0408 | 0.5327 | 3.0358 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0032 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2492 | 0.0679 | 0.8162 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0033 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6790 | 0.1743 | 1.4123 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0034 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7798 | 0.2140 | 1.1967 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0028 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0979 | 0.0348 | 0.5995 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0027 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2873 | 0.0835 | 0.8099 |
| `qr/n16/b1` | 0.0068 | 0.0097 | 0.0077 |
| `qr/n16/b1024` | 6.6442 | 3.3104 | 7.6781 |
| `qr/n4/b1` | 0.0007 | 0.0035 | 0.0011 |
| `qr/n4/b1024` | 0.5092 | 0.2591 | 0.8800 |
| `qr/n8/b1` | 0.0018 | 0.0043 | 0.0026 |
| `qr/n8/b1024` | 1.5670 | 0.4002 | 2.2812 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0104 | 0.0100 |
| `rank_revealing_qr/n16/b1024` | 7.3560 | 3.0907 | 10.0636 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0035 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8135 | 0.4113 | 1.1023 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0050 | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.2407 | 1.1398 | 2.9905 |
| `solve/n16/b1` | 0.0027 | 0.0050 | 0.0031 |
| `solve/n16/b1024` | 2.2101 | 1.1105 | 2.9832 |
| `solve/n4/b1` | 0.0007 | 0.0030 | 0.0009 |
| `solve/n4/b1024` | 0.3261 | 0.0885 | 0.6638 |
| `solve/n8/b1` | 0.0013 | 0.0036 | 0.0014 |
| `solve/n8/b1024` | 0.8101 | 0.2054 | 1.1828 |
| `svd_full/n16/b1` | 0.0348 | 0.0388 | 0.0556 |
| `svd_full/n16/b1024` | 36.7543 | 15.9387 | 58.1282 |
| `svd_full/n4/b1` | 0.0031 | 0.0050 | 0.0053 |
| `svd_full/n4/b1024` | 3.0042 | 0.7583 | 4.7477 |
| `svd_full/n8/b1` | 0.0097 | 0.0127 | 0.0148 |
| `svd_full/n8/b1024` | 10.1056 | 3.0231 | 15.0784 |
| `svd_thin/n16/b1` | 0.0361 | 0.0385 | 0.0557 |
| `svd_thin/n16/b1024` | 36.6597 | 9.5927 | 57.2281 |
| `svd_thin/n4/b1` | 0.0032 | 0.0060 | 0.0053 |
| `svd_thin/n4/b1024` | 2.9988 | 0.7836 | 4.7409 |
| `svd_thin/n8/b1` | 0.0098 | 0.0129 | 0.0147 |
| `svd_thin/n8/b1024` | 10.1442 | 2.5596 | 15.0423 |
| `svd_values/n16/b1` | 0.0260 | 0.0292 | 0.0198 |
| `svd_values/n16/b1024` | 27.2402 | 7.4442 | 20.1715 |
| `svd_values/n4/b1` | 0.0025 | 0.0048 | 0.0033 |
| `svd_values/n4/b1024` | 2.3029 | 1.0142 | 2.7761 |
| `svd_values/n8/b1` | 0.0077 | 0.0103 | 0.0071 |
| `svd_values/n8/b1024` | 7.7668 | 3.3467 | 6.8155 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0024 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6004 | 0.1580 | 0.8442 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0964 | 0.0294 | 0.4718 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0029 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2381 | 0.0650 | 0.5989 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0044 | 0.0010 |
| `cholesky/n16/b1024` | 0.7579 | 0.1924 | 0.9329 |
| `cholesky/n4/b1` | 0.0003 | 0.0032 | 0.0002 |
| `cholesky/n4/b1024` | 0.1171 | 0.0233 | 0.1400 |
| `cholesky/n8/b1` | 0.0004 | 0.0037 | 0.0004 |
| `cholesky/n8/b1024` | 0.2478 | 0.0390 | 0.2943 |
| `eig/n16/b1` | 0.0717 | 0.0768 | 0.1006 |
| `eig/n16/b1024` | 75.7878 | 9.6001 | 120.2308 |
| `eig/n4/b1` | 0.0059 | 0.0094 | 0.0082 |
| `eig/n4/b1024` | 5.8529 | 1.4991 | 7.9865 |
| `eig/n8/b1` | 0.0199 | 0.0226 | 0.0264 |
| `eig/n8/b1024` | 20.3722 | 2.6604 | 28.0188 |
| `eigh/n16/b1` | 0.0181 | 0.0212 | 0.0262 |
| `eigh/n16/b1024` | 19.3220 | 2.4438 | 27.1036 |
| `eigh/n4/b1` | 0.0020 | 0.0057 | 0.0023 |
| `eigh/n4/b1024` | 1.7205 | 0.4324 | 2.1507 |
| `eigh/n8/b1` | 0.0056 | 0.0087 | 0.0072 |
| `eigh/n8/b1024` | 5.4192 | 0.6861 | 7.4197 |
| `eigvals/n16/b1` | 0.0433 | 0.0466 | 0.0747 |
| `eigvals/n16/b1024` | 46.4331 | 9.1510 | 89.8472 |
| `eigvals/n4/b1` | 0.0031 | 0.0066 | 0.0064 |
| `eigvals/n4/b1024` | 2.8250 | 0.7166 | 6.0318 |
| `eigvals/n8/b1` | 0.0119 | 0.0143 | 0.0210 |
| `eigvals/n8/b1024` | 11.9050 | 2.9978 | 22.2516 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0166 | 0.0116 |
| `eigvalsh/n16/b1024` | 14.2697 | 2.3986 | 11.6057 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0048 | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4223 | 0.2110 | 1.2668 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0077 | 0.0040 |
| `eigvalsh/n8/b1024` | 4.3762 | 1.0977 | 3.6975 |
| `full_piv_lu/n16/b1` | 0.0030 | 0.0062 | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.6734 | 0.4568 | 20.2349 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0038 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2675 | 0.0426 | 0.5360 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0044 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7466 | 0.1900 | 2.2615 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0069 | 0.0154 |
| `full_piv_lu_solve/n16/b1024` | 3.1329 | 0.7919 | 22.6608 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0040 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4497 | 0.1214 | 1.2984 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0050 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1659 | 0.2955 | 3.7072 |
| `householder_apply/n16/b1` | 0.0027 | 0.0059 | 0.0047 |
| `householder_apply/n16/b1024` | 3.4696 | 0.7291 | 4.7544 |
| `householder_apply/n4/b1` | 0.0003 | 0.0038 | 0.0008 |
| `householder_apply/n4/b1024` | 0.2054 | 0.0553 | 0.2574 |
| `householder_apply/n8/b1` | 0.0007 | 0.0038 | 0.0014 |
| `householder_apply/n8/b1024` | 0.6679 | 0.1714 | 0.8846 |
| `householder_factor/n16/b1` | 0.0027 | 0.0055 | 0.0045 |
| `householder_factor/n16/b1024` | 2.6700 | 0.6782 | 4.4509 |
| `householder_factor/n4/b1` | 0.0004 | 0.0030 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3252 | 0.0532 | 0.5540 |
| `householder_factor/n8/b1` | 0.0009 | 0.0035 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8614 | 0.2229 | 1.4288 |
| `lu/n16/b1` | 0.0021 | 0.0057 | 0.0023 |
| `lu/n16/b1024` | 1.9208 | 0.4844 | 2.4409 |
| `lu/n4/b1` | 0.0004 | 0.0039 | 0.0004 |
| `lu/n4/b1024` | 0.2108 | 0.0357 | 0.2383 |
| `lu/n8/b1` | 0.0008 | 0.0033 | 0.0009 |
| `lu/n8/b1024` | 0.5432 | 0.1481 | 0.6432 |
| `lu_factor/n16/b1` | 0.0014 | 0.0045 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2184 | 0.3196 | 1.6636 |
| `lu_factor/n4/b1` | 0.0004 | 0.0035 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1654 | 0.0449 | 0.1638 |
| `lu_factor/n8/b1` | 0.0006 | 0.0040 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3884 | 0.1090 | 0.4567 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0053 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0095 | 0.5181 | 3.0230 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0037 | 0.0009 |
| `lu_factor_solve/n4/b1024` | 0.2474 | 0.0697 | 0.8321 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0031 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6631 | 0.1759 | 1.4281 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0043 | 0.0012 |
| `lu_solve_prepared/n16/b1024` | 0.7872 | 0.2088 | 1.1724 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0041 | 0.0005 |
| `lu_solve_prepared/n4/b1024` | 0.0986 | 0.0264 | 0.6631 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0029 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2876 | 0.0846 | 0.7972 |
| `qr/n16/b1` | 0.0068 | 0.0099 | 0.0077 |
| `qr/n16/b1024` | 6.5973 | 0.8425 | 7.6126 |
| `qr/n4/b1` | 0.0007 | 0.0038 | 0.0011 |
| `qr/n4/b1024` | 0.5038 | 0.0716 | 0.8675 |
| `qr/n8/b1` | 0.0018 | 0.0050 | 0.0025 |
| `qr/n8/b1024` | 1.5514 | 0.3931 | 2.2801 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0103 | 0.0098 |
| `rank_revealing_qr/n16/b1024` | 7.3579 | 0.9366 | 10.1532 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0043 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8122 | 0.2088 | 1.0998 |
| `rank_revealing_qr/n8/b1` | 0.0024 | 0.0057 | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.2014 | 0.5535 | 2.9905 |
| `solve/n16/b1` | 0.0027 | 0.0058 | 0.0032 |
| `solve/n16/b1024` | 2.1731 | 0.5509 | 2.9811 |
| `solve/n4/b1` | 0.0007 | 0.0033 | 0.0009 |
| `solve/n4/b1024` | 0.3240 | 0.0528 | 0.6926 |
| `solve/n8/b1` | 0.0013 | 0.0044 | 0.0013 |
| `solve/n8/b1024` | 0.7973 | 0.2040 | 1.2307 |
| `svd_full/n16/b1` | 0.0347 | 0.0385 | 0.0547 |
| `svd_full/n16/b1024` | 36.5170 | 7.8107 | 56.3883 |
| `svd_full/n4/b1` | 0.0031 | 0.0061 | 0.0052 |
| `svd_full/n4/b1024` | 2.9982 | 0.7559 | 4.7363 |
| `svd_full/n8/b1` | 0.0097 | 0.0120 | 0.0145 |
| `svd_full/n8/b1024` | 10.0856 | 1.8244 | 14.9283 |
| `svd_thin/n16/b1` | 0.0349 | 0.0388 | 0.0550 |
| `svd_thin/n16/b1024` | 36.4630 | 6.2060 | 56.4098 |
| `svd_thin/n4/b1` | 0.0031 | 0.0060 | 0.0053 |
| `svd_thin/n4/b1024` | 2.9927 | 0.7562 | 4.7093 |
| `svd_thin/n8/b1` | 0.0097 | 0.0124 | 0.0145 |
| `svd_thin/n8/b1024` | 10.1436 | 2.0559 | 14.9638 |
| `svd_values/n16/b1` | 0.0291 | 0.0292 | 0.0196 |
| `svd_values/n16/b1024` | 27.1721 | 4.2613 | 20.1071 |
| `svd_values/n4/b1` | 0.0026 | 0.0055 | 0.0032 |
| `svd_values/n4/b1024` | 2.2950 | 0.5799 | 2.7545 |
| `svd_values/n8/b1` | 0.0076 | 0.0106 | 0.0070 |
| `svd_values/n8/b1024` | 7.7491 | 1.0047 | 6.7747 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0040 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6220 | 0.1558 | 0.8363 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0035 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0958 | 0.0283 | 0.4502 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0023 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2378 | 0.0655 | 0.5235 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0397 | - | 0.0400 |
| `cholesky/n128/b128` | 6.0317 | - | 6.3419 |
| `cholesky/n32/b1` | 0.0021 | - | 0.0021 |
| `cholesky/n32/b128` | 0.2658 | - | 0.2568 |
| `eigh/n128/b1` | 1.2605 | - | 1.1289 |
| `eigh/n128/b128` | 162.4212 | - | 148.5730 |
| `eigh/n32/b1` | 0.0642 | - | 0.0776 |
| `eigh/n32/b128` | 8.4611 | - | 9.9925 |
| `eigvalsh/n128/b1` | 0.6999 | - | 0.4971 |
| `eigvalsh/n128/b128` | 90.7690 | - | 64.5686 |
| `eigvalsh/n32/b1` | 0.0490 | - | 0.0288 |
| `eigvalsh/n32/b128` | 6.4235 | - | 3.7451 |
| `householder_apply/n128/b1` | 0.1289 | - | 0.2556 |
| `householder_apply/n128/b128` | 17.3642 | - | 34.0146 |
| `householder_apply/n32/b1` | 0.0112 | - | 0.0109 |
| `householder_apply/n32/b128` | 1.4171 | - | 1.3510 |
| `householder_factor/n128/b1` | 0.1054 | - | 0.2202 |
| `householder_factor/n128/b128` | 13.5689 | - | 28.3583 |
| `householder_factor/n32/b1` | 0.0076 | - | 0.0085 |
| `householder_factor/n32/b128` | 0.9670 | - | 1.0899 |
| `lu/n128/b1` | 0.0890 | - | 0.0869 |
| `lu/n128/b128` | 12.2997 | - | 13.6181 |
| `lu/n32/b1` | 0.0055 | - | 0.0050 |
| `lu/n32/b128` | 0.6069 | - | 0.6034 |
| `lu_factor/n128/b1` | 0.0578 | - | 0.0784 |
| `lu_factor/n128/b128` | 8.4266 | - | 11.0358 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0039 |
| `lu_factor/n32/b128` | 0.3863 | - | 0.4947 |
| `lu_factor_solve/n128/b1` | 0.0632 | - | 0.0904 |
| `lu_factor_solve/n128/b128` | 8.8686 | - | 12.4297 |
| `lu_factor_solve/n32/b1` | 0.0043 | - | 0.0056 |
| `lu_factor_solve/n32/b128` | 0.4967 | - | 0.7099 |
| `lu_solve_prepared/n128/b1` | 0.0060 | - | 0.0120 |
| `lu_solve_prepared/n128/b128` | 1.7393 | - | 2.7667 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0017 |
| `lu_solve_prepared/n32/b128` | 0.1133 | - | 0.2038 |
| `qr/n128/b1` | 0.3371 | - | 0.4288 |
| `qr/n128/b128` | 43.6147 | - | 57.0558 |
| `qr/n32/b1` | 0.0205 | - | 0.0161 |
| `qr/n32/b128` | 2.5473 | - | 2.0120 |
| `rank_revealing_qr/n128/b1` | 0.3498 | - | 0.4901 |
| `rank_revealing_qr/n128/b128` | 45.3898 | - | 64.7125 |
| `rank_revealing_qr/n32/b1` | 0.0203 | - | 0.0199 |
| `rank_revealing_qr/n32/b128` | 2.5765 | - | 2.5080 |
| `solve/n128/b1` | 0.0663 | - | 0.0926 |
| `solve/n128/b128` | 8.8116 | - | 12.6518 |
| `solve/n32/b1` | 0.0048 | - | 0.0061 |
| `solve/n32/b128` | 0.5286 | - | 0.7280 |
| `svd_thin/n128/b1` | 2.4075 | - | 2.0034 |
| `svd_thin/n128/b128` | 308.2049 | - | 260.1766 |
| `svd_thin/n32/b1` | 0.1179 | - | 0.1400 |
| `svd_thin/n32/b128` | 15.1741 | - | 17.9738 |
| `svd_values/n128/b1` | 1.4071 | - | 0.8161 |
| `svd_values/n128/b128` | 180.5504 | - | 105.4682 |
| `svd_values/n32/b1` | 0.0926 | - | 0.0461 |
| `svd_values/n32/b128` | 11.9788 | - | 5.9889 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0062 |
| `triangular_solve/n128/b128` | 0.7552 | - | 1.3452 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0010 |
| `triangular_solve/n32/b128` | 0.0883 | - | 0.1067 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0379 | 0.0502 | 0.0447 |
| `cholesky/n128/b128` | 6.0429 | 6.8615 | 6.8963 |
| `cholesky/n32/b1` | 0.0021 | 0.0037 | 0.0020 |
| `cholesky/n32/b128` | 0.2775 | 0.0695 | 0.2593 |
| `eigh/n128/b1` | 1.2619 | 1.2405 | 0.9098 |
| `eigh/n128/b128` | 162.8813 | 164.1632 | 115.2174 |
| `eigh/n32/b1` | 0.0642 | 0.0688 | 0.0711 |
| `eigh/n32/b128` | 8.4431 | 2.6862 | 9.0639 |
| `eigvalsh/n128/b1` | 0.6999 | 0.7033 | 0.4767 |
| `eigvalsh/n128/b128` | 90.8926 | 90.7641 | 61.4669 |
| `eigvalsh/n32/b1` | 0.0490 | 0.0516 | 0.0287 |
| `eigvalsh/n32/b128` | 6.4358 | 1.9912 | 3.7637 |
| `householder_apply/n128/b1` | 0.1250 | 0.1308 | 0.2353 |
| `householder_apply/n128/b128` | 17.1217 | 17.3449 | 31.9460 |
| `householder_apply/n32/b1` | 0.0113 | 0.0143 | 0.0108 |
| `householder_apply/n32/b128` | 1.4255 | 0.3713 | 1.3657 |
| `householder_factor/n128/b1` | 0.1030 | 0.1234 | 0.2288 |
| `householder_factor/n128/b128` | 13.6378 | 16.8092 | 30.4318 |
| `householder_factor/n32/b1` | 0.0075 | 0.0102 | 0.0084 |
| `householder_factor/n32/b128` | 0.9450 | 0.2678 | 1.0742 |
| `lu/n128/b1` | 0.0899 | 0.1044 | 0.0872 |
| `lu/n128/b128` | 12.1948 | 14.0144 | 13.6429 |
| `lu/n32/b1` | 0.0055 | 0.0087 | 0.0051 |
| `lu/n32/b128` | 0.6245 | 0.3271 | 0.6120 |
| `lu_factor/n128/b1` | 0.0565 | 0.0731 | 0.0796 |
| `lu_factor/n128/b128` | 8.1492 | 2.5471 | 11.2036 |
| `lu_factor/n32/b1` | 0.0033 | 0.0052 | 0.0040 |
| `lu_factor/n32/b128` | 0.3975 | 0.1062 | 0.5114 |
| `lu_factor_solve/n128/b1` | 0.0633 | 0.0779 | 0.0890 |
| `lu_factor_solve/n128/b128` | 8.9207 | 2.7654 | 12.2126 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0066 | 0.0054 |
| `lu_factor_solve/n32/b128` | 0.5020 | 0.1322 | 0.7357 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0085 | 0.0073 |
| `lu_solve_prepared/n128/b128` | 2.0220 | 0.5440 | 2.0528 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0027 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1156 | 0.0348 | 0.1665 |
| `qr/n128/b1` | 0.3371 | 0.6162 | 0.4484 |
| `qr/n128/b128` | 43.4554 | 80.8648 | 58.9357 |
| `qr/n32/b1` | 0.0203 | 0.0461 | 0.0157 |
| `qr/n32/b128` | 2.5570 | 1.0120 | 2.0133 |
| `rank_revealing_qr/n128/b1` | 0.3449 | 0.3608 | 0.5136 |
| `rank_revealing_qr/n128/b128` | 44.5437 | 46.9500 | 67.0911 |
| `rank_revealing_qr/n32/b1` | 0.0206 | 0.0467 | 0.0197 |
| `rank_revealing_qr/n32/b128` | 2.5556 | 0.7047 | 2.4761 |
| `solve/n128/b1` | 0.0669 | 0.0795 | 0.0916 |
| `solve/n128/b128` | 8.7823 | 10.5749 | 12.3614 |
| `solve/n32/b1` | 0.0047 | 0.0087 | 0.0058 |
| `solve/n32/b128` | 0.5283 | 0.2745 | 0.7251 |
| `svd_thin/n128/b1` | 2.3997 | 1.8075 | 1.9835 |
| `svd_thin/n128/b128` | 306.1804 | 230.7166 | 260.4896 |
| `svd_thin/n32/b1` | 0.1182 | 0.1218 | 0.1399 |
| `svd_thin/n32/b128` | 15.3747 | 3.8529 | 17.7838 |
| `svd_values/n128/b1` | 1.4085 | 1.4334 | 0.8227 |
| `svd_values/n128/b128` | 180.2350 | 180.6877 | 108.2191 |
| `svd_values/n32/b1` | 0.0920 | 0.0965 | 0.0461 |
| `svd_values/n32/b128` | 11.8756 | 3.0138 | 6.0261 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0062 | 0.0041 |
| `triangular_solve/n128/b128` | 0.9368 | 1.0037 | 1.3176 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0025 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0871 | 0.0456 | 0.1048 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0397 | 0.0539 | 0.0431 |
| `cholesky/n128/b128` | 5.3384 | 6.7514 | 6.6045 |
| `cholesky/n32/b1` | 0.0021 | 0.0054 | 0.0020 |
| `cholesky/n32/b128` | 0.2755 | 0.0585 | 0.2526 |
| `eigh/n128/b1` | 1.2625 | 1.2469 | 0.8678 |
| `eigh/n128/b128` | 163.9003 | 160.0202 | 113.3517 |
| `eigh/n32/b1` | 0.0639 | 0.0685 | 0.0700 |
| `eigh/n32/b128` | 8.4544 | 1.5831 | 8.7966 |
| `eigvalsh/n128/b1` | 0.6958 | 0.7025 | 0.4797 |
| `eigvalsh/n128/b128` | 90.3397 | 90.8756 | 61.8017 |
| `eigvalsh/n32/b1` | 0.0488 | 0.0529 | 0.0291 |
| `eigvalsh/n32/b128` | 6.4491 | 1.4511 | 3.7592 |
| `householder_apply/n128/b1` | 0.1251 | 0.1850 | 0.2356 |
| `householder_apply/n128/b128` | 17.1911 | 24.7465 | 31.4491 |
| `householder_apply/n32/b1` | 0.0111 | 0.0259 | 0.0108 |
| `householder_apply/n32/b128` | 1.3503 | 0.2039 | 1.3249 |
| `householder_factor/n128/b1` | 0.1045 | 0.1677 | 0.2333 |
| `householder_factor/n128/b128` | 13.4902 | 22.4271 | 29.8129 |
| `householder_factor/n32/b1` | 0.0074 | 0.0103 | 0.0085 |
| `householder_factor/n32/b128` | 0.9298 | 0.2399 | 1.0797 |
| `lu/n128/b1` | 0.0891 | 0.1154 | 0.0869 |
| `lu/n128/b128` | 12.3382 | 15.3637 | 13.6335 |
| `lu/n32/b1` | 0.0053 | 0.0079 | 0.0050 |
| `lu/n32/b128` | 0.5962 | 0.1592 | 0.6141 |
| `lu_factor/n128/b1` | 0.0567 | 0.0841 | 0.0786 |
| `lu_factor/n128/b128` | 8.2622 | 1.4231 | 11.1108 |
| `lu_factor/n32/b1` | 0.0033 | 0.0059 | 0.0039 |
| `lu_factor/n32/b128` | 0.3839 | 0.1069 | 0.5004 |
| `lu_factor_solve/n128/b1` | 0.0621 | 0.0886 | 0.0881 |
| `lu_factor_solve/n128/b128` | 8.9103 | 2.6568 | 12.1699 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0075 | 0.0053 |
| `lu_factor_solve/n32/b128` | 0.4869 | 0.0724 | 0.7454 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0091 | 0.0073 |
| `lu_solve_prepared/n128/b128` | 1.8657 | 0.3138 | 1.9575 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0040 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1120 | 0.0340 | 0.1672 |
| `qr/n128/b1` | 0.3372 | 0.9453 | 0.4476 |
| `qr/n128/b128` | 43.3545 | 120.9690 | 59.5776 |
| `qr/n32/b1` | 0.0204 | 0.0658 | 0.0159 |
| `qr/n32/b128` | 2.5409 | 0.3245 | 2.0005 |
| `rank_revealing_qr/n128/b1` | 0.3471 | 0.4285 | 0.5188 |
| `rank_revealing_qr/n128/b128` | 44.5337 | 54.9613 | 67.6730 |
| `rank_revealing_qr/n32/b1` | 0.0204 | 0.0683 | 0.0199 |
| `rank_revealing_qr/n32/b128` | 2.5303 | 0.3212 | 2.4694 |
| `solve/n128/b1` | 0.0660 | 0.0934 | 0.0926 |
| `solve/n128/b128` | 8.7673 | 11.9987 | 12.3194 |
| `solve/n32/b1` | 0.0047 | 0.0078 | 0.0059 |
| `solve/n32/b128` | 0.5252 | 0.1377 | 0.7423 |
| `svd_thin/n128/b1` | 2.4024 | 1.8345 | 1.9981 |
| `svd_thin/n128/b128` | 306.6288 | 237.7622 | 260.4017 |
| `svd_thin/n32/b1` | 0.1172 | 0.1212 | 0.1385 |
| `svd_thin/n32/b128` | 15.3190 | 1.9134 | 17.8799 |
| `svd_values/n128/b1` | 1.4113 | 1.4387 | 0.8232 |
| `svd_values/n128/b128` | 180.5224 | 180.9780 | 108.3292 |
| `svd_values/n32/b1` | 0.0917 | 0.0965 | 0.0459 |
| `svd_values/n32/b128` | 11.8539 | 3.0081 | 6.0189 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0072 | 0.0039 |
| `triangular_solve/n128/b128` | 0.8240 | 0.8161 | 1.1693 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0040 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0898 | 0.0254 | 0.1031 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1078 | - | 0.1085 |
| `cholesky/n128/b128` | 15.7977 | - | 15.4796 |
| `cholesky/n32/b1` | 0.0031 | - | 0.0034 |
| `cholesky/n32/b128` | 0.4081 | - | 0.4343 |
| `eigh/n128/b1` | 1.8396 | - | 3.2937 |
| `eigh/n128/b128` | 241.4693 | - | 424.7998 |
| `eigh/n32/b1` | 0.0801 | - | 0.1096 |
| `eigh/n32/b128` | 10.4907 | - | 14.2037 |
| `eigvalsh/n128/b1` | 0.9293 | - | 0.9525 |
| `eigvalsh/n128/b128` | 122.0359 | - | 123.5685 |
| `eigvalsh/n32/b1` | 0.0526 | - | 0.0418 |
| `eigvalsh/n32/b128` | 6.9477 | - | 5.4440 |
| `householder_apply/n128/b1` | 0.4853 | - | 0.6925 |
| `householder_apply/n128/b128` | 64.0570 | - | 92.7118 |
| `householder_apply/n32/b1` | 0.0146 | - | 0.0197 |
| `householder_apply/n32/b128` | 1.9096 | - | 2.5167 |
| `householder_factor/n128/b1` | 0.3499 | - | 0.4401 |
| `householder_factor/n128/b128` | 45.4887 | - | 57.4921 |
| `householder_factor/n32/b1` | 0.0115 | - | 0.0156 |
| `householder_factor/n32/b128` | 1.4469 | - | 2.0184 |
| `lu/n128/b1` | 0.2055 | - | 0.2119 |
| `lu/n128/b128` | 27.7395 | - | 31.2963 |
| `lu/n32/b1` | 0.0081 | - | 0.0080 |
| `lu/n32/b128` | 1.0687 | - | 1.1240 |
| `lu_factor/n128/b1` | 0.1570 | - | 0.1923 |
| `lu_factor/n128/b128` | 22.0535 | - | 25.4403 |
| `lu_factor/n32/b1` | 0.0054 | - | 0.0064 |
| `lu_factor/n32/b128` | 0.6704 | - | 0.8228 |
| `lu_factor_solve/n128/b1` | 0.1757 | - | 0.2199 |
| `lu_factor_solve/n128/b128` | 24.5547 | - | 29.2587 |
| `lu_factor_solve/n32/b1` | 0.0077 | - | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9430 | - | 1.1302 |
| `lu_solve_prepared/n128/b1` | 0.0188 | - | 0.0286 |
| `lu_solve_prepared/n128/b128` | 4.1292 | - | 5.1698 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0023 |
| `lu_solve_prepared/n32/b128` | 0.2866 | - | 0.3134 |
| `qr/n128/b1` | 0.9713 | - | 0.8671 |
| `qr/n128/b128` | 125.3533 | - | 113.0863 |
| `qr/n32/b1` | 0.0426 | - | 0.0289 |
| `qr/n32/b128` | 5.4306 | - | 3.6847 |
| `rank_revealing_qr/n128/b1` | 1.0112 | - | 0.9895 |
| `rank_revealing_qr/n128/b128` | 130.1209 | - | 131.8312 |
| `rank_revealing_qr/n32/b1` | 0.0388 | - | 0.0367 |
| `rank_revealing_qr/n32/b128` | 4.9798 | - | 4.8554 |
| `solve/n128/b1` | 0.1814 | - | 0.2292 |
| `solve/n128/b128` | 24.1046 | - | 29.3418 |
| `solve/n32/b1` | 0.0084 | - | 0.0095 |
| `solve/n32/b128` | 0.9942 | - | 1.1799 |
| `svd_thin/n128/b1` | 3.9366 | - | 3.5014 |
| `svd_thin/n128/b128` | 506.7532 | - | 458.9113 |
| `svd_thin/n32/b1` | 0.1495 | - | 0.1675 |
| `svd_thin/n32/b128` | 19.5480 | - | 22.1526 |
| `svd_values/n128/b1` | 1.8783 | - | 1.3981 |
| `svd_values/n128/b128` | 244.2765 | - | 179.5038 |
| `svd_values/n32/b1` | 0.1010 | - | 0.0640 |
| `svd_values/n32/b128` | 13.2548 | - | 8.2977 |
| `triangular_solve/n128/b1` | 0.0110 | - | 0.0145 |
| `triangular_solve/n128/b128` | 2.1858 | - | 2.9522 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0013 |
| `triangular_solve/n32/b128` | 0.1893 | - | 0.1536 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1078 | 0.1087 | 0.0794 |
| `cholesky/n128/b128` | 15.8676 | 15.4861 | 11.1392 |
| `cholesky/n32/b1` | 0.0033 | 0.0052 | 0.0034 |
| `cholesky/n32/b128` | 0.3902 | 0.1019 | 0.4387 |
| `eigh/n128/b1` | 1.8484 | 1.7524 | 3.1624 |
| `eigh/n128/b128` | 244.7484 | 228.4513 | 419.0638 |
| `eigh/n32/b1` | 0.0805 | 0.0849 | 0.1084 |
| `eigh/n32/b128` | 10.5110 | 2.6259 | 14.0552 |
| `eigvalsh/n128/b1` | 0.9362 | 0.9324 | 0.8877 |
| `eigvalsh/n128/b128` | 122.7925 | 121.8684 | 115.4688 |
| `eigvalsh/n32/b1` | 0.0529 | 0.0570 | 0.0417 |
| `eigvalsh/n32/b128` | 6.9734 | 2.3781 | 5.4195 |
| `householder_apply/n128/b1` | 0.4870 | 0.2617 | 0.3700 |
| `householder_apply/n128/b128` | 65.3075 | 35.4894 | 51.0144 |
| `householder_apply/n32/b1` | 0.0149 | 0.0172 | 0.0197 |
| `householder_apply/n32/b128` | 1.9499 | 0.4770 | 2.5120 |
| `householder_factor/n128/b1` | 0.3519 | 0.2268 | 0.4059 |
| `householder_factor/n128/b128` | 46.2629 | 29.7170 | 50.3579 |
| `householder_factor/n32/b1` | 0.0114 | 0.0143 | 0.0156 |
| `householder_factor/n32/b128` | 1.4654 | 0.3708 | 2.0326 |
| `lu/n128/b1` | 0.1965 | 0.1878 | 0.1432 |
| `lu/n128/b128` | 27.5270 | 26.2883 | 22.0372 |
| `lu/n32/b1` | 0.0081 | 0.0109 | 0.0081 |
| `lu/n32/b128` | 1.0450 | 0.4998 | 1.1152 |
| `lu_factor/n128/b1` | 0.1555 | 0.1433 | 0.1183 |
| `lu_factor/n128/b128` | 22.0042 | 6.2503 | 15.5944 |
| `lu_factor/n32/b1` | 0.0054 | 0.0088 | 0.0063 |
| `lu_factor/n32/b128` | 0.6585 | 0.3449 | 0.8164 |
| `lu_factor_solve/n128/b1` | 0.1745 | 0.1634 | 0.1344 |
| `lu_factor_solve/n128/b128` | 24.5659 | 6.5721 | 18.1374 |
| `lu_factor_solve/n32/b1` | 0.0077 | 0.0106 | 0.0086 |
| `lu_factor_solve/n32/b128` | 0.9389 | 0.4786 | 1.1526 |
| `lu_solve_prepared/n128/b1` | 0.0186 | 0.0217 | 0.0152 |
| `lu_solve_prepared/n128/b128` | 4.1564 | 1.2195 | 4.1372 |
| `lu_solve_prepared/n32/b1` | 0.0022 | 0.0049 | 0.0017 |
| `lu_solve_prepared/n32/b128` | 0.2854 | 0.1495 | 0.2554 |
| `qr/n128/b1` | 0.9711 | 0.8595 | 0.7685 |
| `qr/n128/b128` | 125.2444 | 111.1741 | 101.3318 |
| `qr/n32/b1` | 0.0424 | 0.0679 | 0.0286 |
| `qr/n32/b128` | 5.4139 | 2.1405 | 3.6404 |
| `rank_revealing_qr/n128/b1` | 1.0135 | 0.7975 | 0.9026 |
| `rank_revealing_qr/n128/b128` | 130.4118 | 104.2950 | 120.3463 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0659 | 0.0365 |
| `rank_revealing_qr/n32/b128` | 4.9300 | 2.3169 | 4.8269 |
| `solve/n128/b1` | 0.1798 | 0.1697 | 0.1484 |
| `solve/n128/b128` | 24.0554 | 22.3677 | 19.8876 |
| `solve/n32/b1` | 0.0083 | 0.0108 | 0.0094 |
| `solve/n32/b128` | 0.9907 | 0.2509 | 1.1785 |
| `svd_thin/n128/b1` | 3.9239 | 2.7039 | 3.0091 |
| `svd_thin/n128/b128` | 506.0445 | 350.2771 | 388.7669 |
| `svd_thin/n32/b1` | 0.1494 | 0.1538 | 0.1686 |
| `svd_thin/n32/b128` | 19.5325 | 8.4102 | 22.4019 |
| `svd_values/n128/b1` | 1.8707 | 1.9021 | 1.5133 |
| `svd_values/n128/b128` | 243.4965 | 243.3032 | 194.4557 |
| `svd_values/n32/b1` | 0.1005 | 0.1048 | 0.0636 |
| `svd_values/n32/b128` | 13.2835 | 4.5132 | 8.2492 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0138 | 0.0092 |
| `triangular_solve/n128/b128` | 2.2584 | 2.1900 | 2.5275 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0040 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1941 | 0.0522 | 0.1596 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1079 | 0.1151 | 0.0967 |
| `cholesky/n128/b128` | 15.8211 | 16.4650 | 13.6926 |
| `cholesky/n32/b1` | 0.0031 | 0.0063 | 0.0034 |
| `cholesky/n32/b128` | 0.3952 | 0.1032 | 0.4345 |
| `eigh/n128/b1` | 1.8436 | 1.6142 | 3.1568 |
| `eigh/n128/b128` | 241.3372 | 211.8588 | 408.4582 |
| `eigh/n32/b1` | 0.0804 | 0.0850 | 0.1075 |
| `eigh/n32/b128` | 10.5651 | 2.6562 | 13.9479 |
| `eigvalsh/n128/b1` | 0.9326 | 0.9322 | 0.8855 |
| `eigvalsh/n128/b128` | 121.7505 | 121.8376 | 115.3904 |
| `eigvalsh/n32/b1` | 0.0526 | 0.0573 | 0.0421 |
| `eigvalsh/n32/b128` | 6.9241 | 0.8880 | 5.4672 |
| `householder_apply/n128/b1` | 0.4860 | 0.3314 | 0.3241 |
| `householder_apply/n128/b128` | 64.3355 | 44.3674 | 45.2827 |
| `householder_apply/n32/b1` | 0.0148 | 0.0176 | 0.0198 |
| `householder_apply/n32/b128` | 1.8865 | 0.4768 | 2.4713 |
| `householder_factor/n128/b1` | 0.3501 | 0.2825 | 0.3793 |
| `householder_factor/n128/b128` | 45.4938 | 36.4767 | 49.8601 |
| `householder_factor/n32/b1` | 0.0114 | 0.0142 | 0.0156 |
| `householder_factor/n32/b128` | 1.4437 | 0.3720 | 1.9934 |
| `lu/n128/b1` | 0.2054 | 0.1954 | 0.1373 |
| `lu/n128/b128` | 27.8013 | 27.4108 | 21.3774 |
| `lu/n32/b1` | 0.0080 | 0.0108 | 0.0080 |
| `lu/n32/b128` | 1.0640 | 0.1310 | 1.0993 |
| `lu_factor/n128/b1` | 0.1564 | 0.1564 | 0.1132 |
| `lu_factor/n128/b128` | 21.9584 | 3.3860 | 14.7792 |
| `lu_factor/n32/b1` | 0.0054 | 0.0092 | 0.0064 |
| `lu_factor/n32/b128` | 0.6478 | 0.1744 | 0.8209 |
| `lu_factor_solve/n128/b1` | 0.1754 | 0.1766 | 0.1401 |
| `lu_factor_solve/n128/b128` | 24.5493 | 3.7417 | 17.4097 |
| `lu_factor_solve/n32/b1` | 0.0077 | 0.0110 | 0.0087 |
| `lu_factor_solve/n32/b128` | 0.9299 | 0.1730 | 1.1438 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0221 | 0.0180 |
| `lu_solve_prepared/n128/b128` | 4.1762 | 1.1221 | 4.1762 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0055 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2841 | 0.0775 | 0.2605 |
| `qr/n128/b1` | 0.9763 | 1.2027 | 0.7576 |
| `qr/n128/b128` | 125.5569 | 156.7206 | 99.3629 |
| `qr/n32/b1` | 0.0424 | 0.0890 | 0.0287 |
| `qr/n32/b128` | 5.3957 | 1.3780 | 3.6462 |
| `rank_revealing_qr/n128/b1` | 1.0147 | 0.8832 | 0.9023 |
| `rank_revealing_qr/n128/b128` | 130.4898 | 113.2194 | 120.4560 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0863 | 0.0364 |
| `rank_revealing_qr/n32/b128` | 4.9513 | 0.6362 | 4.8520 |
| `solve/n128/b1` | 0.1803 | 0.1804 | 0.1463 |
| `solve/n128/b128` | 24.0251 | 23.7193 | 19.0916 |
| `solve/n32/b1` | 0.0085 | 0.0109 | 0.0095 |
| `solve/n32/b128` | 0.9804 | 0.2498 | 1.2041 |
| `svd_thin/n128/b1` | 3.9526 | 2.7664 | 2.9840 |
| `svd_thin/n128/b128` | 509.4642 | 355.3780 | 387.5000 |
| `svd_thin/n32/b1` | 0.1502 | 0.1545 | 0.1672 |
| `svd_thin/n32/b128` | 19.5832 | 4.9309 | 22.1128 |
| `svd_values/n128/b1` | 1.8733 | 1.9056 | 1.5558 |
| `svd_values/n128/b128` | 243.9719 | 242.8508 | 200.9977 |
| `svd_values/n32/b1` | 0.1005 | 0.1046 | 0.0635 |
| `svd_values/n32/b128` | 13.2340 | 3.0307 | 8.2672 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0140 | 0.0091 |
| `triangular_solve/n128/b128` | 2.2167 | 2.1913 | 2.5517 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0056 | 0.0012 |
| `triangular_solve/n32/b128` | 0.1903 | 0.0348 | 0.1713 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1991 | - | 0.2314 |
| `cholesky/n256/b4` | 0.8120 | - | 0.9335 |
| `cholesky/n512/b1` | 1.2593 | - | 1.5850 |
| `cholesky/n512/b4` | 5.7719 | - | 6.6516 |
| `eigh/n256/b1` | 5.6074 | - | 5.4182 |
| `eigh/n256/b4` | 22.5314 | - | 21.6205 |
| `eigh/n512/b1` | 28.6844 | - | 30.4780 |
| `eigh/n512/b4` | 115.2547 | - | 121.7146 |
| `eigvalsh/n256/b1` | 2.9377 | - | 2.4978 |
| `eigvalsh/n256/b4` | 11.8164 | - | 9.9728 |
| `eigvalsh/n512/b1` | 14.0817 | - | 14.2849 |
| `eigvalsh/n512/b4` | 56.6924 | - | 57.8705 |
| `householder_apply/n256/b1` | 0.8259 | - | 1.6380 |
| `householder_apply/n256/b4` | 3.3318 | - | 6.6119 |
| `householder_apply/n512/b1` | 6.1725 | - | 11.9470 |
| `householder_apply/n512/b4` | 24.9701 | - | 47.3248 |
| `householder_factor/n256/b1` | 0.6227 | - | 1.0966 |
| `householder_factor/n256/b4` | 2.4876 | - | 4.4028 |
| `householder_factor/n512/b1` | 4.3201 | - | 7.4207 |
| `householder_factor/n512/b4` | 17.4789 | - | 29.9089 |
| `lu/n256/b1` | 0.4757 | - | 0.4846 |
| `lu/n256/b4` | 1.9542 | - | 2.0648 |
| `lu/n512/b1` | 3.2208 | - | 3.1869 |
| `lu/n512/b4` | 12.8254 | - | 13.0126 |
| `lu_factor/n256/b1` | 0.3566 | - | 0.4435 |
| `lu_factor/n256/b4` | 1.5349 | - | 1.7831 |
| `lu_factor/n512/b1` | 2.8189 | - | 2.8879 |
| `lu_factor/n512/b4` | 11.7232 | - | 11.7781 |
| `lu_factor_solve/n256/b1` | 0.3713 | - | 0.4902 |
| `lu_factor_solve/n256/b4` | 1.4926 | - | 1.9513 |
| `lu_factor_solve/n512/b1` | 2.8779 | - | 3.0347 |
| `lu_factor_solve/n512/b4` | 12.0509 | - | 12.3900 |
| `lu_solve_prepared/n256/b1` | 0.0174 | - | 0.0426 |
| `lu_solve_prepared/n256/b4` | 0.0787 | - | 0.1928 |
| `lu_solve_prepared/n512/b1` | 0.0620 | - | 0.1482 |
| `lu_solve_prepared/n512/b4` | 0.4257 | - | 1.0216 |
| `qr/n256/b1` | 1.8486 | - | 2.1780 |
| `qr/n256/b4` | 7.3645 | - | 8.7914 |
| `qr/n512/b1` | 11.4564 | - | 14.8227 |
| `qr/n512/b4` | 46.0366 | - | 60.4003 |
| `rank_revealing_qr/n256/b1` | 2.0932 | - | 2.6138 |
| `rank_revealing_qr/n256/b4` | 8.3827 | - | 10.5748 |
| `rank_revealing_qr/n512/b1` | 14.6450 | - | 18.7784 |
| `rank_revealing_qr/n512/b4` | 58.8728 | - | 75.8363 |
| `solve/n256/b1` | 0.3898 | - | 0.4966 |
| `solve/n256/b4` | 1.5482 | - | 2.0094 |
| `solve/n512/b1` | 2.8507 | - | 3.0587 |
| `solve/n512/b4` | 11.3210 | - | 12.3486 |
| `svd_thin/n256/b1` | 12.2183 | - | 10.9770 |
| `svd_thin/n256/b4` | 48.9114 | - | 44.1774 |
| `svd_thin/n512/b1` | 70.7091 | - | 71.5101 |
| `svd_thin/n512/b4` | 283.4541 | - | 292.5011 |
| `svd_values/n256/b1` | 6.9306 | - | 4.6027 |
| `svd_values/n256/b4` | 27.6263 | - | 18.6060 |
| `svd_values/n512/b1` | 38.5867 | - | 31.2647 |
| `svd_values/n512/b4` | 154.3988 | - | 127.2132 |
| `triangular_solve/n256/b1` | 0.0105 | - | 0.0206 |
| `triangular_solve/n256/b4` | 0.0439 | - | 0.0842 |
| `triangular_solve/n512/b1` | 0.0338 | - | 0.0760 |
| `triangular_solve/n512/b4` | 0.1397 | - | 0.3449 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1994 | 0.1845 | 0.1571 |
| `cholesky/n256/b4` | 0.8105 | 0.7651 | 0.6410 |
| `cholesky/n512/b1` | 1.2607 | 0.8016 | 0.7755 |
| `cholesky/n512/b4` | 5.7130 | 3.6680 | 3.4223 |
| `eigh/n256/b1` | 5.6090 | 4.2562 | 3.6183 |
| `eigh/n256/b4` | 22.5316 | 18.7744 | 14.3968 |
| `eigh/n512/b1` | 29.1488 | 16.0002 | 16.2678 |
| `eigh/n512/b4` | 116.6325 | 64.4270 | 65.6761 |
| `eigvalsh/n256/b1` | 2.9453 | 2.9692 | 1.9153 |
| `eigvalsh/n256/b4` | 11.7699 | 11.9446 | 7.6811 |
| `eigvalsh/n512/b1` | 14.4572 | 11.9291 | 7.4916 |
| `eigvalsh/n512/b4` | 58.1380 | 48.0145 | 30.2634 |
| `householder_apply/n256/b1` | 0.8215 | 0.3222 | 1.0945 |
| `householder_apply/n256/b4` | 3.3353 | 1.3473 | 4.4857 |
| `householder_apply/n512/b1` | 6.1943 | 1.8248 | 6.9903 |
| `householder_apply/n512/b4` | 24.8708 | 7.5874 | 27.8290 |
| `householder_factor/n256/b1` | 0.6186 | 0.3411 | 0.8508 |
| `householder_factor/n256/b4` | 2.4884 | 1.3806 | 3.4342 |
| `householder_factor/n512/b1` | 4.3334 | 1.6489 | 4.5657 |
| `householder_factor/n512/b4` | 17.5140 | 6.7472 | 18.3165 |
| `lu/n256/b1` | 0.4783 | 0.4497 | 0.2853 |
| `lu/n256/b4` | 1.9652 | 1.8198 | 1.2517 |
| `lu/n512/b1` | 3.2881 | 1.9623 | 1.6710 |
| `lu/n512/b4` | 13.3130 | 7.7319 | 6.9795 |
| `lu_factor/n256/b1` | 0.3523 | 0.3117 | 0.2385 |
| `lu_factor/n256/b4` | 1.5225 | 0.7710 | 0.9661 |
| `lu_factor/n512/b1` | 2.8447 | 1.4706 | 1.3602 |
| `lu_factor/n512/b4` | 11.8705 | 3.5238 | 5.5434 |
| `lu_factor_solve/n256/b1` | 0.3687 | 0.3375 | 0.2694 |
| `lu_factor_solve/n256/b4` | 1.4901 | 0.3947 | 1.0992 |
| `lu_factor_solve/n512/b1` | 2.9180 | 1.5305 | 1.4846 |
| `lu_factor_solve/n512/b4` | 12.1420 | 3.5678 | 6.1208 |
| `lu_solve_prepared/n256/b1` | 0.0173 | 0.0234 | 0.0267 |
| `lu_solve_prepared/n256/b4` | 0.0816 | 0.0227 | 0.1291 |
| `lu_solve_prepared/n512/b1` | 0.0727 | 0.0677 | 0.1035 |
| `lu_solve_prepared/n512/b4` | 0.4426 | 0.1988 | 0.8619 |
| `qr/n256/b1` | 1.8466 | 1.7837 | 1.6851 |
| `qr/n256/b4` | 7.3682 | 7.2270 | 6.8193 |
| `qr/n512/b1` | 11.4579 | 6.1029 | 9.0064 |
| `qr/n512/b4` | 46.0516 | 24.4915 | 36.9611 |
| `rank_revealing_qr/n256/b1` | 2.0959 | 1.5007 | 2.3274 |
| `rank_revealing_qr/n256/b4` | 8.3898 | 5.9495 | 9.4020 |
| `rank_revealing_qr/n512/b1` | 14.8981 | 6.3139 | 14.7587 |
| `rank_revealing_qr/n512/b4` | 60.1194 | 25.1366 | 59.4529 |
| `solve/n256/b1` | 0.3860 | 0.3741 | 0.2839 |
| `solve/n256/b4` | 1.5424 | 1.3986 | 1.1451 |
| `solve/n512/b1` | 2.8706 | 1.5782 | 1.5331 |
| `solve/n512/b4` | 11.4642 | 6.3158 | 6.1738 |
| `svd_thin/n256/b1` | 12.2764 | 9.1462 | 9.3534 |
| `svd_thin/n256/b4` | 49.0068 | 35.7726 | 37.5443 |
| `svd_thin/n512/b1` | 71.7178 | 40.0988 | 55.3979 |
| `svd_thin/n512/b4` | 284.8375 | 160.1738 | 222.9346 |
| `svd_values/n256/b1` | 6.9377 | 7.0939 | 4.4220 |
| `svd_values/n256/b4` | 27.6966 | 28.0766 | 18.0259 |
| `svd_values/n512/b1` | 38.5317 | 31.8798 | 28.6576 |
| `svd_values/n512/b4` | 154.0844 | 126.5538 | 118.1019 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0155 | 0.0126 |
| `triangular_solve/n256/b4` | 0.0451 | 0.0593 | 0.0608 |
| `triangular_solve/n512/b1` | 0.0327 | 0.0357 | 0.0495 |
| `triangular_solve/n512/b4` | 0.1376 | 0.1397 | 0.2554 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1956 | 0.1945 | 0.1606 |
| `cholesky/n256/b4` | 0.8106 | 0.8538 | 0.6547 |
| `cholesky/n512/b1` | 1.2879 | 0.7172 | 0.6896 |
| `cholesky/n512/b4` | 5.6025 | 3.2655 | 3.0787 |
| `eigh/n256/b1` | 5.6005 | 4.1744 | 3.3150 |
| `eigh/n256/b4` | 22.5078 | 16.5955 | 13.4820 |
| `eigh/n512/b1` | 29.0507 | 14.8583 | 14.2193 |
| `eigh/n512/b4` | 116.9026 | 60.2375 | 56.4623 |
| `eigvalsh/n256/b1` | 2.9425 | 2.9631 | 1.8751 |
| `eigvalsh/n256/b4` | 11.7438 | 11.9407 | 7.4922 |
| `eigvalsh/n512/b1` | 14.2867 | 11.5672 | 6.7503 |
| `eigvalsh/n512/b4` | 57.5681 | 47.0652 | 27.1336 |
| `householder_apply/n256/b1` | 0.8229 | 0.3988 | 1.0544 |
| `householder_apply/n256/b4` | 3.3130 | 1.6832 | 4.2152 |
| `householder_apply/n512/b1` | 6.0684 | 1.8386 | 5.9508 |
| `householder_apply/n512/b4` | 25.0726 | 7.6149 | 24.4962 |
| `householder_factor/n256/b1` | 0.6255 | 0.4315 | 0.8325 |
| `householder_factor/n256/b4` | 2.4621 | 1.6977 | 3.2890 |
| `householder_factor/n512/b1` | 4.3289 | 1.7246 | 4.0823 |
| `householder_factor/n512/b4` | 17.3733 | 7.1139 | 16.4049 |
| `lu/n256/b1` | 0.4773 | 0.4987 | 0.2489 |
| `lu/n256/b4` | 1.9602 | 1.9984 | 1.1027 |
| `lu/n512/b1` | 3.2946 | 2.0247 | 1.1422 |
| `lu/n512/b4` | 12.9155 | 8.1838 | 4.8364 |
| `lu_factor/n256/b1` | 0.3781 | 0.3523 | 0.2048 |
| `lu_factor/n256/b4` | 1.5198 | 1.4896 | 0.8253 |
| `lu_factor/n512/b1` | 2.8454 | 1.5194 | 0.8544 |
| `lu_factor/n512/b4` | 11.7559 | 6.2503 | 3.4580 |
| `lu_factor_solve/n256/b1` | 0.3922 | 0.3887 | 0.2387 |
| `lu_factor_solve/n256/b4` | 1.4848 | 1.4270 | 0.9444 |
| `lu_factor_solve/n512/b1` | 2.9044 | 1.6167 | 0.9649 |
| `lu_factor_solve/n512/b4` | 12.0344 | 6.5929 | 3.9425 |
| `lu_solve_prepared/n256/b1` | 0.0173 | 0.0279 | 0.0263 |
| `lu_solve_prepared/n256/b4` | 0.0760 | 0.1076 | 0.1236 |
| `lu_solve_prepared/n512/b1` | 0.0723 | 0.0768 | 0.1092 |
| `lu_solve_prepared/n512/b4` | 0.3744 | 0.3924 | 0.7851 |
| `qr/n256/b1` | 1.8504 | 2.4558 | 1.6678 |
| `qr/n256/b4` | 7.3968 | 9.8378 | 6.6949 |
| `qr/n512/b1` | 11.4919 | 7.0021 | 8.1245 |
| `qr/n512/b4` | 46.1826 | 27.9598 | 32.9642 |
| `rank_revealing_qr/n256/b1` | 2.1353 | 1.5816 | 2.2970 |
| `rank_revealing_qr/n256/b4` | 8.3839 | 6.2758 | 9.2996 |
| `rank_revealing_qr/n512/b1` | 14.9789 | 5.9005 | 13.9177 |
| `rank_revealing_qr/n512/b4` | 59.9465 | 22.9908 | 56.4518 |
| `solve/n256/b1` | 0.3862 | 0.3895 | 0.2533 |
| `solve/n256/b4` | 1.5433 | 1.5765 | 1.0117 |
| `solve/n512/b1` | 2.8584 | 1.6548 | 1.0307 |
| `solve/n512/b4` | 11.3602 | 6.6542 | 4.2777 |
| `svd_thin/n256/b1` | 12.2179 | 8.9765 | 9.2206 |
| `svd_thin/n256/b4` | 48.9267 | 35.8996 | 36.9327 |
| `svd_thin/n512/b1` | 70.9239 | 37.9194 | 52.6010 |
| `svd_thin/n512/b4` | 283.0754 | 154.2315 | 211.3131 |
| `svd_values/n256/b1` | 6.9365 | 7.1794 | 4.4644 |
| `svd_values/n256/b4` | 27.6135 | 28.6539 | 18.0265 |
| `svd_values/n512/b1` | 38.7556 | 32.3143 | 28.3950 |
| `svd_values/n512/b4` | 153.9466 | 128.5624 | 116.5474 |
| `triangular_solve/n256/b1` | 0.0106 | 0.0191 | 0.0127 |
| `triangular_solve/n256/b4` | 0.0465 | 0.0639 | 0.0623 |
| `triangular_solve/n512/b1` | 0.0365 | 0.0442 | 0.0549 |
| `triangular_solve/n512/b4` | 0.1753 | 0.1873 | 0.3187 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7037 | - | 0.7673 |
| `cholesky/n256/b4` | 2.7751 | - | 3.0841 |
| `cholesky/n512/b1` | 4.6002 | - | 5.4336 |
| `cholesky/n512/b4` | 19.6484 | - | 22.6853 |
| `eigh/n256/b1` | 10.2415 | - | 21.6776 |
| `eigh/n256/b4` | 41.3033 | - | 86.3177 |
| `eigh/n512/b1` | 63.0230 | - | 157.0776 |
| `eigh/n512/b4` | 252.8772 | - | 630.7378 |
| `eigvalsh/n256/b1` | 4.9704 | - | 5.6467 |
| `eigvalsh/n256/b4` | 19.8652 | - | 22.5932 |
| `eigvalsh/n512/b1` | 29.5456 | - | 37.4891 |
| `eigvalsh/n512/b4` | 118.1538 | - | 149.7390 |
| `householder_apply/n256/b1` | 3.3730 | - | 4.7371 |
| `householder_apply/n256/b4` | 13.6977 | - | 19.2091 |
| `householder_apply/n512/b1` | 24.5427 | - | 32.2520 |
| `householder_apply/n512/b4` | 96.6104 | - | 129.1224 |
| `householder_factor/n256/b1` | 2.3392 | - | 3.0090 |
| `householder_factor/n256/b4` | 9.3630 | - | 12.0821 |
| `householder_factor/n512/b1` | 16.6841 | - | 20.7973 |
| `householder_factor/n512/b4` | 67.1330 | - | 83.8720 |
| `lu/n256/b1` | 1.2471 | - | 1.4386 |
| `lu/n256/b4` | 5.1388 | - | 6.0459 |
| `lu/n512/b1` | 8.6865 | - | 10.2893 |
| `lu/n512/b4` | 34.8333 | - | 41.2019 |
| `lu_factor/n256/b1` | 1.1195 | - | 1.3373 |
| `lu_factor/n256/b4` | 4.5059 | - | 5.3504 |
| `lu_factor/n512/b1` | 8.0018 | - | 9.5276 |
| `lu_factor/n512/b4` | 32.6824 | - | 38.2609 |
| `lu_factor_solve/n256/b1` | 1.1886 | - | 1.4769 |
| `lu_factor_solve/n256/b4` | 4.7622 | - | 5.7912 |
| `lu_factor_solve/n512/b1` | 8.2159 | - | 9.9994 |
| `lu_factor_solve/n512/b4` | 33.8370 | - | 40.1033 |
| `lu_solve_prepared/n256/b1` | 0.0629 | - | 0.1320 |
| `lu_solve_prepared/n256/b4` | 0.2617 | - | 0.4448 |
| `lu_solve_prepared/n512/b1` | 0.2082 | - | 0.5056 |
| `lu_solve_prepared/n512/b4` | 1.3117 | - | 2.1221 |
| `qr/n256/b1` | 6.2533 | - | 6.0289 |
| `qr/n256/b4` | 24.9471 | - | 24.1331 |
| `qr/n512/b1` | 42.4233 | - | 41.7667 |
| `qr/n512/b4` | 169.4954 | - | 168.7544 |
| `rank_revealing_qr/n256/b1` | 6.7406 | - | 6.4447 |
| `rank_revealing_qr/n256/b4` | 26.9388 | - | 26.0851 |
| `rank_revealing_qr/n512/b1` | 47.4726 | - | 44.7305 |
| `rank_revealing_qr/n512/b4` | 190.5734 | - | 180.6664 |
| `solve/n256/b1` | 1.1779 | - | 1.4854 |
| `solve/n256/b4` | 4.7162 | - | 5.9625 |
| `solve/n512/b1` | 8.2263 | - | 10.0281 |
| `solve/n512/b4` | 32.9121 | - | 40.5333 |
| `svd_thin/n256/b1` | 24.1261 | - | 22.5206 |
| `svd_thin/n256/b4` | 96.5262 | - | 89.6450 |
| `svd_thin/n512/b1` | 151.8711 | - | 144.1562 |
| `svd_thin/n512/b4` | 607.7499 | - | 576.8440 |
| `svd_values/n256/b1` | 11.0499 | - | 9.7725 |
| `svd_values/n256/b4` | 44.2513 | - | 38.6353 |
| `svd_values/n512/b1` | 65.8573 | - | 59.4210 |
| `svd_values/n512/b4` | 263.8891 | - | 237.0852 |
| `triangular_solve/n256/b1` | 0.0341 | - | 0.0631 |
| `triangular_solve/n256/b4` | 0.1379 | - | 0.2593 |
| `triangular_solve/n512/b1` | 0.1122 | - | 0.2196 |
| `triangular_solve/n512/b4` | 0.5087 | - | 0.8670 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7043 | 0.5034 | 0.3695 |
| `cholesky/n256/b4` | 2.7754 | 1.9485 | 1.3885 |
| `cholesky/n512/b1` | 4.7395 | 2.4576 | 2.0777 |
| `cholesky/n512/b4` | 19.6924 | 10.3788 | 9.3327 |
| `eigh/n256/b1` | 10.2397 | 7.7651 | 19.4846 |
| `eigh/n256/b4` | 41.3263 | 31.9272 | 78.1819 |
| `eigh/n512/b1` | 63.1446 | 28.6351 | 126.9294 |
| `eigh/n512/b4` | 253.0289 | 116.8154 | 522.9494 |
| `eigvalsh/n256/b1` | 4.9982 | 5.0272 | 4.9252 |
| `eigvalsh/n256/b4` | 19.8439 | 19.9420 | 19.6770 |
| `eigvalsh/n512/b1` | 29.6683 | 19.8063 | 20.4939 |
| `eigvalsh/n512/b4` | 118.6129 | 79.8617 | 82.2914 |
| `householder_apply/n256/b1` | 3.3751 | 1.0418 | 2.2456 |
| `householder_apply/n256/b4` | 13.6936 | 4.2923 | 9.0905 |
| `householder_apply/n512/b1` | 24.7193 | 6.7608 | 12.1761 |
| `householder_apply/n512/b4` | 97.3922 | 26.8409 | 49.4929 |
| `householder_factor/n256/b1` | 2.3345 | 0.9626 | 1.7117 |
| `householder_factor/n256/b4` | 9.3876 | 3.8426 | 6.9128 |
| `householder_factor/n512/b1` | 16.7923 | 5.3974 | 8.5119 |
| `householder_factor/n512/b4` | 66.9998 | 21.6078 | 34.6923 |
| `lu/n256/b1` | 1.2534 | 0.8276 | 0.7767 |
| `lu/n256/b4` | 5.0442 | 3.3586 | 3.2981 |
| `lu/n512/b1` | 9.1366 | 3.9347 | 3.7171 |
| `lu/n512/b4` | 36.6797 | 15.5175 | 14.9215 |
| `lu_factor/n256/b1` | 1.1135 | 0.6821 | 0.6665 |
| `lu_factor/n256/b4` | 4.5189 | 1.1755 | 2.6715 |
| `lu_factor/n512/b1` | 8.0681 | 3.1478 | 2.9815 |
| `lu_factor/n512/b4` | 32.9567 | 9.0433 | 12.0241 |
| `lu_factor_solve/n256/b1` | 1.1786 | 0.7308 | 0.7482 |
| `lu_factor_solve/n256/b4` | 4.7873 | 1.2501 | 3.0040 |
| `lu_factor_solve/n512/b1` | 8.3008 | 3.2713 | 3.3643 |
| `lu_factor_solve/n512/b4` | 34.0506 | 9.4868 | 13.5232 |
| `lu_solve_prepared/n256/b1` | 0.0630 | 0.0596 | 0.0923 |
| `lu_solve_prepared/n256/b4` | 0.2499 | 0.0686 | 0.3134 |
| `lu_solve_prepared/n512/b1` | 0.2095 | 0.1566 | 0.3590 |
| `lu_solve_prepared/n512/b4` | 1.3203 | 0.6477 | 2.1577 |
| `qr/n256/b1` | 6.2531 | 3.1182 | 3.4425 |
| `qr/n256/b4` | 24.8764 | 12.1913 | 13.9236 |
| `qr/n512/b1` | 42.3662 | 14.5916 | 17.3461 |
| `qr/n512/b4` | 169.7922 | 58.4151 | 69.9489 |
| `rank_revealing_qr/n256/b1` | 6.7906 | 3.9704 | 3.8756 |
| `rank_revealing_qr/n256/b4` | 26.8422 | 15.9557 | 15.8813 |
| `rank_revealing_qr/n512/b1` | 47.8666 | 16.7586 | 19.2750 |
| `rank_revealing_qr/n512/b4` | 191.4543 | 67.9582 | 77.0046 |
| `solve/n256/b1` | 1.1782 | 0.7563 | 0.8089 |
| `solve/n256/b4` | 4.6914 | 3.0223 | 3.1966 |
| `solve/n512/b1` | 8.3507 | 3.3956 | 3.4416 |
| `solve/n512/b4` | 33.3534 | 13.3908 | 14.1571 |
| `svd_thin/n256/b1` | 24.2621 | 15.1667 | 14.4100 |
| `svd_thin/n256/b4` | 96.7281 | 62.0256 | 57.7827 |
| `svd_thin/n512/b1` | 153.6388 | 66.7495 | 71.1957 |
| `svd_thin/n512/b4` | 608.1988 | 267.9118 | 291.1476 |
| `svd_values/n256/b1` | 11.0123 | 10.6507 | 7.2855 |
| `svd_values/n256/b4` | 44.0331 | 43.0789 | 29.0237 |
| `svd_values/n512/b1` | 65.2141 | 41.3600 | 32.1082 |
| `svd_values/n512/b4` | 261.6102 | 166.8833 | 129.5706 |
| `triangular_solve/n256/b1` | 0.0341 | 0.0344 | 0.0471 |
| `triangular_solve/n256/b4` | 0.1487 | 0.1345 | 0.2158 |
| `triangular_solve/n512/b1` | 0.1124 | 0.0835 | 0.1500 |
| `triangular_solve/n512/b4` | 0.5058 | 0.3760 | 0.8106 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6992 | 0.4816 | 0.3405 |
| `cholesky/n256/b4` | 2.8053 | 1.9693 | 1.3367 |
| `cholesky/n512/b1` | 4.7957 | 1.8617 | 1.4437 |
| `cholesky/n512/b4` | 19.7214 | 7.9719 | 6.5121 |
| `eigh/n256/b1` | 10.2909 | 7.0986 | 19.2758 |
| `eigh/n256/b4` | 41.3934 | 28.0060 | 77.6060 |
| `eigh/n512/b1` | 63.2461 | 24.2147 | 123.0145 |
| `eigh/n512/b4` | 251.9026 | 97.3921 | 496.2278 |
| `eigvalsh/n256/b1` | 4.9839 | 5.0424 | 4.8423 |
| `eigvalsh/n256/b4` | 19.8402 | 19.9238 | 19.4064 |
| `eigvalsh/n512/b1` | 29.5483 | 17.9010 | 17.9422 |
| `eigvalsh/n512/b4` | 118.0313 | 71.5700 | 72.1583 |
| `householder_apply/n256/b1` | 3.3136 | 0.9044 | 1.7656 |
| `householder_apply/n256/b4` | 13.5087 | 3.8470 | 7.2258 |
| `householder_apply/n512/b1` | 24.5782 | 4.4983 | 8.5730 |
| `householder_apply/n512/b4` | 98.9296 | 18.4693 | 35.5755 |
| `householder_factor/n256/b1` | 2.3399 | 0.9861 | 1.5273 |
| `householder_factor/n256/b4` | 9.1902 | 3.8960 | 6.0906 |
| `householder_factor/n512/b1` | 16.7196 | 4.4667 | 6.4720 |
| `householder_factor/n512/b4` | 67.0482 | 18.0110 | 26.1403 |
| `lu/n256/b1` | 1.2459 | 0.8265 | 0.5519 |
| `lu/n256/b4` | 5.1459 | 3.3821 | 2.4311 |
| `lu/n512/b1` | 8.7211 | 3.3858 | 2.3009 |
| `lu/n512/b4` | 34.6942 | 13.2876 | 9.2831 |
| `lu_factor/n256/b1` | 1.1069 | 0.6555 | 0.4555 |
| `lu_factor/n256/b4` | 4.3564 | 2.5806 | 1.7746 |
| `lu_factor/n512/b1` | 8.0405 | 2.5327 | 1.6477 |
| `lu_factor/n512/b4` | 32.6956 | 10.4605 | 6.6109 |
| `lu_factor_solve/n256/b1` | 1.1721 | 0.7290 | 0.5513 |
| `lu_factor_solve/n256/b4` | 4.5877 | 2.8158 | 2.0317 |
| `lu_factor_solve/n512/b1` | 8.2391 | 2.7375 | 1.9803 |
| `lu_factor_solve/n512/b4` | 33.7437 | 11.0844 | 8.0090 |
| `lu_solve_prepared/n256/b1` | 0.0634 | 0.0678 | 0.1032 |
| `lu_solve_prepared/n256/b4` | 0.2452 | 0.2677 | 0.2677 |
| `lu_solve_prepared/n512/b1` | 0.2218 | 0.1704 | 0.3411 |
| `lu_solve_prepared/n512/b4` | 1.1070 | 0.8617 | 1.5859 |
| `qr/n256/b1` | 6.2128 | 3.5298 | 3.0431 |
| `qr/n256/b4` | 24.8730 | 14.1545 | 12.3081 |
| `qr/n512/b1` | 42.4517 | 12.5381 | 13.1495 |
| `qr/n512/b4` | 170.0366 | 49.2119 | 53.4378 |
| `rank_revealing_qr/n256/b1` | 6.7483 | 3.9560 | 3.5083 |
| `rank_revealing_qr/n256/b4` | 26.9426 | 15.9129 | 14.2771 |
| `rank_revealing_qr/n512/b1` | 47.5838 | 12.3513 | 14.8378 |
| `rank_revealing_qr/n512/b4` | 190.8971 | 48.7824 | 59.9203 |
| `solve/n256/b1` | 1.1792 | 0.7505 | 0.5849 |
| `solve/n256/b4` | 4.6954 | 2.9825 | 2.4252 |
| `solve/n512/b1` | 8.2143 | 2.9381 | 2.1017 |
| `solve/n512/b4` | 32.8752 | 11.4825 | 8.6858 |
| `svd_thin/n256/b1` | 24.0844 | 14.4273 | 13.3315 |
| `svd_thin/n256/b4` | 96.5770 | 59.5743 | 53.7780 |
| `svd_thin/n512/b1` | 151.8290 | 55.1056 | 61.3554 |
| `svd_thin/n512/b4` | 607.0892 | 221.2391 | 245.9518 |
| `svd_values/n256/b1` | 10.9956 | 10.7930 | 7.1788 |
| `svd_values/n256/b4` | 44.2124 | 43.2078 | 28.6543 |
| `svd_values/n512/b1` | 64.8985 | 39.5251 | 28.6553 |
| `svd_values/n512/b4` | 261.2534 | 159.6489 | 115.7450 |
| `triangular_solve/n256/b1` | 0.0337 | 0.0378 | 0.0431 |
| `triangular_solve/n256/b4` | 0.1419 | 0.1468 | 0.1719 |
| `triangular_solve/n512/b1` | 0.1141 | 0.0895 | 0.1543 |
| `triangular_solve/n512/b4` | 0.5270 | 0.4049 | 0.8224 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3233 | - | 0.5516 |
| `householder_factor/4096x256/b1` | 14.1812 | - | 23.3509 |
| `qr/1024x64/b1` | 0.9838 | - | 1.0749 |
| `qr/4096x256/b1` | 41.3732 | - | 46.7594 |
| `rank_revealing_qr/1024x64/b1` | 0.9692 | - | 1.1645 |
| `rank_revealing_qr/4096x256/b1` | 64.2346 | - | 57.4262 |
| `svd_thin/1024x64/b1` | 1.4577 | - | 1.9688 |
| `svd_thin/4096x256/b1` | 72.6956 | - | 74.4616 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3297 | 0.2516 | 0.5919 |
| `householder_factor/4096x256/b1` | 14.1898 | 5.7896 | 12.5308 |
| `qr/1024x64/b1` | 0.9817 | 0.9228 | 1.1270 |
| `qr/4096x256/b1` | 40.9895 | 20.1717 | 24.6869 |
| `rank_revealing_qr/1024x64/b1` | 0.9726 | 0.7325 | 1.2341 |
| `rank_revealing_qr/4096x256/b1` | 64.5689 | 23.7557 | 28.3120 |
| `svd_thin/1024x64/b1` | 1.4530 | 1.3938 | 1.8985 |
| `svd_thin/4096x256/b1` | 72.3605 | 40.6180 | 41.7723 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3287 | 0.3082 | 0.5892 |
| `householder_factor/4096x256/b1` | 14.1753 | 5.9556 | 11.1355 |
| `qr/1024x64/b1` | 0.9744 | 1.1220 | 1.1322 |
| `qr/4096x256/b1` | 41.2669 | 19.5670 | 21.7554 |
| `rank_revealing_qr/1024x64/b1` | 0.9641 | 0.7524 | 1.2366 |
| `rank_revealing_qr/4096x256/b1` | 65.4508 | 18.4416 | 24.3770 |
| `svd_thin/1024x64/b1` | 1.4516 | 1.6167 | 1.8563 |
| `svd_thin/4096x256/b1` | 72.5896 | 34.7635 | 37.6206 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0251 | - | 1.0599 |
| `householder_factor/4096x256/b1` | 55.0984 | - | 69.5654 |
| `qr/1024x64/b1` | 2.8727 | - | 2.0858 |
| `qr/4096x256/b1` | 146.7275 | - | 138.3202 |
| `rank_revealing_qr/1024x64/b1` | 2.8807 | - | 2.2675 |
| `rank_revealing_qr/4096x256/b1` | 244.9525 | - | 172.8553 |
| `svd_thin/1024x64/b1` | 3.5645 | - | 3.9500 |
| `svd_thin/4096x256/b1` | 231.4869 | - | 218.9538 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0432 | 0.6005 | 0.4334 |
| `householder_factor/4096x256/b1` | 54.6100 | 18.6665 | 20.0065 |
| `qr/1024x64/b1` | 2.8624 | 1.6155 | 0.8089 |
| `qr/4096x256/b1` | 147.1528 | 57.4165 | 40.3167 |
| `rank_revealing_qr/1024x64/b1` | 2.8717 | 1.7608 | 1.0335 |
| `rank_revealing_qr/4096x256/b1` | 244.0582 | 82.7810 | 55.6316 |
| `svd_thin/1024x64/b1` | 3.5623 | 2.2693 | 2.0923 |
| `svd_thin/4096x256/b1` | 231.8154 | 103.3197 | 75.4157 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0423 | 0.6344 | 0.3443 |
| `householder_factor/4096x256/b1` | 55.1123 | 17.0369 | 12.5560 |
| `qr/1024x64/b1` | 2.8584 | 1.7611 | 0.6191 |
| `qr/4096x256/b1` | 147.2513 | 46.3263 | 25.4343 |
| `rank_revealing_qr/1024x64/b1` | 2.8539 | 1.7130 | 0.8561 |
| `rank_revealing_qr/4096x256/b1` | 244.8054 | 52.5691 | 34.0580 |
| `svd_thin/1024x64/b1` | 3.5495 | 2.4842 | 1.8208 |
| `svd_thin/4096x256/b1` | 232.4131 | 76.9474 | 53.8187 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
