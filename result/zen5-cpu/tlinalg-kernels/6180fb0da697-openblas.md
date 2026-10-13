<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261013T040624Z/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `6180fb0da69717891fe09bc67a76c3e7b74fba02`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.24.4 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c); `t4a-faer-traits` 0.24.0 @ `d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c#d6a20b0c099766ebcbb3a48eb9516ecbf2ae0a3c)
- harness commit: `27a223546fc69ec3d102ce004d5f4d60e0f69db9`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-13T05:02:14.149772Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261013T040624Z/`

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
| `cholesky/n16/b1024` | 0.5018 | - | 0.6100 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1070 | - | 0.1137 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2174 | - | 0.2344 |
| `eig/n16/b1` | 0.0534 | - | 0.0404 |
| `eig/n16/b1024` | 55.9937 | - | 41.8246 |
| `eig/n4/b1` | 0.0039 | - | 0.0037 |
| `eig/n4/b1024` | 3.5656 | - | 3.2706 |
| `eig/n8/b1` | 0.0143 | - | 0.0111 |
| `eig/n8/b1024` | 13.7510 | - | 10.5354 |
| `eigh/n16/b1` | 0.0177 | - | 0.0229 |
| `eigh/n16/b1024` | 17.8913 | - | 24.1241 |
| `eigh/n4/b1` | 0.0016 | - | 0.0020 |
| `eigh/n4/b1024` | 1.4617 | - | 1.8471 |
| `eigh/n8/b1` | 0.0052 | - | 0.0063 |
| `eigh/n8/b1024` | 5.0873 | - | 6.5126 |
| `eigvals/n16/b1` | 0.0370 | - | 0.0292 |
| `eigvals/n16/b1024` | 39.0217 | - | 30.0023 |
| `eigvals/n4/b1` | 0.0023 | - | 0.0025 |
| `eigvals/n4/b1024` | 1.8853 | - | 2.0673 |
| `eigvals/n8/b1` | 0.0096 | - | 0.0086 |
| `eigvals/n8/b1024` | 9.1401 | - | 8.0020 |
| `eigvalsh/n16/b1` | 0.0133 | - | 0.0084 |
| `eigvalsh/n16/b1024` | 13.3306 | - | 8.6961 |
| `eigvalsh/n4/b1` | 0.0013 | - | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1881 | - | 0.8351 |
| `eigvalsh/n8/b1` | 0.0044 | - | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0534 | - | 2.7013 |
| `full_piv_lu/n16/b1` | 0.0027 | - | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.1082 | - | 2.8462 |
| `full_piv_lu/n4/b1` | 0.0007 | - | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2183 | - | 0.2192 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6130 | - | 0.5908 |
| `full_piv_lu_solve/n16/b1` | 0.0028 | - | 0.0037 |
| `full_piv_lu_solve/n16/b1024` | 2.0085 | - | 3.8787 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0006 |
| `full_piv_lu_solve/n4/b1024` | 0.3078 | - | 0.4156 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0012 |
| `full_piv_lu_solve/n8/b1024` | 0.7154 | - | 0.9848 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0029 |
| `householder_apply/n16/b1024` | 2.7123 | - | 2.6979 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0006 |
| `householder_apply/n4/b1024` | 0.2067 | - | 0.2478 |
| `householder_apply/n8/b1` | 0.0009 | - | 0.0011 |
| `householder_apply/n8/b1024` | 0.6792 | - | 0.7210 |
| `householder_factor/n16/b1` | 0.0022 | - | 0.0027 |
| `householder_factor/n16/b1024` | 2.1923 | - | 2.6116 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.2657 | - | 0.3186 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.7176 | - | 0.8998 |
| `lu/n16/b1` | 0.0019 | - | 0.0017 |
| `lu/n16/b1024` | 1.5364 | - | 1.4449 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.1702 | - | 0.1929 |
| `lu/n8/b1` | 0.0007 | - | 0.0007 |
| `lu/n8/b1024` | 0.4665 | - | 0.4780 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0011 |
| `lu_factor/n16/b1024` | 1.0876 | - | 1.0961 |
| `lu_factor/n4/b1` | 0.0003 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1312 | - | 0.1294 |
| `lu_factor/n8/b1` | 0.0005 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3547 | - | 0.3428 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0020 |
| `lu_factor_solve/n16/b1024` | 1.4304 | - | 1.8841 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.1640 | - | 0.3150 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0007 |
| `lu_factor_solve/n8/b1024` | 0.4852 | - | 0.6467 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3615 | - | 0.7123 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0401 | - | 0.1883 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1369 | - | 0.3073 |
| `qr/n16/b1` | 0.0055 | - | 0.0048 |
| `qr/n16/b1024` | 5.2162 | - | 4.6649 |
| `qr/n4/b1` | 0.0007 | - | 0.0008 |
| `qr/n4/b1024` | 0.4334 | - | 0.5721 |
| `qr/n8/b1` | 0.0016 | - | 0.0018 |
| `qr/n8/b1024` | 1.3978 | - | 1.5727 |
| `rank_revealing_qr/n16/b1` | 0.0066 | - | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.3344 | - | 5.5770 |
| `rank_revealing_qr/n4/b1` | 0.0010 | - | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7136 | - | 0.6896 |
| `rank_revealing_qr/n8/b1` | 0.0022 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.9119 | - | 1.8264 |
| `solve/n16/b1` | 0.0021 | - | 0.0023 |
| `solve/n16/b1024` | 1.5435 | - | 1.9453 |
| `solve/n4/b1` | 0.0006 | - | 0.0006 |
| `solve/n4/b1024` | 0.2159 | - | 0.3461 |
| `solve/n8/b1` | 0.0010 | - | 0.0009 |
| `solve/n8/b1024` | 0.5332 | - | 0.6785 |
| `svd_full/n16/b1` | 0.0327 | - | 0.0487 |
| `svd_full/n16/b1024` | 33.4781 | - | 48.7734 |
| `svd_full/n4/b1` | 0.0028 | - | 0.0043 |
| `svd_full/n4/b1024` | 2.5558 | - | 3.7752 |
| `svd_full/n8/b1` | 0.0089 | - | 0.0124 |
| `svd_full/n8/b1024` | 9.2149 | - | 12.7385 |
| `svd_thin/n16/b1` | 0.0326 | - | 0.0489 |
| `svd_thin/n16/b1024` | 34.7383 | - | 48.7126 |
| `svd_thin/n4/b1` | 0.0028 | - | 0.0043 |
| `svd_thin/n4/b1024` | 2.5382 | - | 3.7710 |
| `svd_thin/n8/b1` | 0.0089 | - | 0.0125 |
| `svd_thin/n8/b1024` | 9.0450 | - | 12.9725 |
| `svd_values/n16/b1` | 0.0238 | - | 0.0149 |
| `svd_values/n16/b1024` | 24.3750 | - | 15.0370 |
| `svd_values/n4/b1` | 0.0021 | - | 0.0026 |
| `svd_values/n4/b1024` | 1.9202 | - | 2.0578 |
| `svd_values/n8/b1` | 0.0067 | - | 0.0056 |
| `svd_values/n8/b1024` | 6.7580 | - | 5.3582 |
| `triangular_solve/n16/b1` | 0.0004 | - | 0.0006 |
| `triangular_solve/n16/b1024` | 0.3069 | - | 0.3960 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0515 | - | 0.1176 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1310 | - | 0.1797 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0027 | 0.0007 |
| `cholesky/n16/b1024` | 0.5038 | 0.2593 | 0.6041 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1078 | 0.0330 | 0.1173 |
| `cholesky/n8/b1` | 0.0003 | 0.0027 | 0.0003 |
| `cholesky/n8/b1024` | 0.2212 | 0.0575 | 0.2291 |
| `eig/n16/b1` | 0.0540 | 0.0571 | 0.0400 |
| `eig/n16/b1024` | 57.0947 | 14.7866 | 41.7970 |
| `eig/n4/b1` | 0.0040 | 0.0055 | 0.0037 |
| `eig/n4/b1024` | 3.5576 | 1.2669 | 3.2298 |
| `eig/n8/b1` | 0.0141 | 0.0168 | 0.0111 |
| `eig/n8/b1024` | 13.8204 | 3.4807 | 10.5787 |
| `eigh/n16/b1` | 0.0175 | 0.0208 | 0.0230 |
| `eigh/n16/b1024` | 17.9402 | 4.5521 | 24.2689 |
| `eigh/n4/b1` | 0.0016 | 0.0033 | 0.0020 |
| `eigh/n4/b1024` | 1.4673 | 0.7382 | 1.8857 |
| `eigh/n8/b1` | 0.0052 | 0.0084 | 0.0064 |
| `eigh/n8/b1024` | 5.0859 | 2.5666 | 6.6645 |
| `eigvals/n16/b1` | 0.0372 | 0.0402 | 0.0290 |
| `eigvals/n16/b1024` | 38.9691 | 15.9776 | 29.7592 |
| `eigvals/n4/b1` | 0.0022 | 0.0045 | 0.0025 |
| `eigvals/n4/b1024` | 1.8940 | 0.9563 | 2.0309 |
| `eigvals/n8/b1` | 0.0095 | 0.0121 | 0.0086 |
| `eigvals/n8/b1024` | 9.1440 | 2.3226 | 7.9146 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0162 | 0.0084 |
| `eigvalsh/n16/b1024` | 13.3384 | 6.4999 | 8.8230 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0040 | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1823 | 0.5962 | 0.8329 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0063 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0651 | 2.0730 | 2.7122 |
| `full_piv_lu/n16/b1` | 0.0027 | 0.0052 | 0.0026 |
| `full_piv_lu/n16/b1024` | 2.0529 | 1.0834 | 2.6912 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0023 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2195 | 0.0654 | 0.2338 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0033 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6006 | 0.3157 | 0.6164 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0049 | 0.0039 |
| `full_piv_lu_solve/n16/b1024` | 2.0739 | 0.5255 | 3.7862 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0036 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3063 | 0.1596 | 0.5488 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0028 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7132 | 0.3640 | 1.1896 |
| `householder_apply/n16/b1` | 0.0028 | 0.0051 | 0.0030 |
| `householder_apply/n16/b1024` | 2.7223 | 0.6973 | 2.6525 |
| `householder_apply/n4/b1` | 0.0003 | 0.0027 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2006 | 0.0601 | 0.2559 |
| `householder_apply/n8/b1` | 0.0008 | 0.0033 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6761 | 0.3470 | 0.7185 |
| `householder_factor/n16/b1` | 0.0022 | 0.0046 | 0.0027 |
| `householder_factor/n16/b1024` | 2.1405 | 0.5481 | 2.6028 |
| `householder_factor/n4/b1` | 0.0003 | 0.0027 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2692 | 0.0775 | 0.3187 |
| `householder_factor/n8/b1` | 0.0008 | 0.0032 | 0.0011 |
| `householder_factor/n8/b1024` | 0.6941 | 0.1797 | 0.8980 |
| `lu/n16/b1` | 0.0018 | 0.0043 | 0.0017 |
| `lu/n16/b1024` | 1.5070 | 0.7805 | 1.4596 |
| `lu/n4/b1` | 0.0004 | 0.0021 | 0.0004 |
| `lu/n4/b1024` | 0.1697 | 0.0481 | 0.1950 |
| `lu/n8/b1` | 0.0007 | 0.0033 | 0.0006 |
| `lu/n8/b1024` | 0.4904 | 0.2378 | 0.4793 |
| `lu_factor/n16/b1` | 0.0013 | 0.0036 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1265 | 0.2850 | 1.0895 |
| `lu_factor/n4/b1` | 0.0003 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1319 | 0.0711 | 0.1299 |
| `lu_factor/n8/b1` | 0.0006 | 0.0027 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3436 | 0.0940 | 0.3387 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0033 | 0.0021 |
| `lu_factor_solve/n16/b1024` | 1.3877 | 0.7174 | 2.0276 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0027 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1658 | 0.0471 | 0.6999 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0034 | 0.0009 |
| `lu_factor_solve/n8/b1024` | 0.4791 | 0.1260 | 0.9222 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0022 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3599 | 0.1937 | 0.6500 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0401 | 0.0203 | 0.5132 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0028 | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.1394 | 0.0460 | 0.4422 |
| `qr/n16/b1` | 0.0056 | 0.0073 | 0.0047 |
| `qr/n16/b1024` | 5.2057 | 2.6629 | 4.6779 |
| `qr/n4/b1` | 0.0007 | 0.0039 | 0.0008 |
| `qr/n4/b1024` | 0.4472 | 0.2232 | 0.5817 |
| `qr/n8/b1` | 0.0016 | 0.0040 | 0.0018 |
| `qr/n8/b1024` | 1.3905 | 0.7024 | 1.5634 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0096 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.1792 | 2.1928 | 5.5547 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0033 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7018 | 0.3536 | 0.7011 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0040 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8710 | 0.9482 | 1.8092 |
| `solve/n16/b1` | 0.0021 | 0.0037 | 0.0023 |
| `solve/n16/b1024` | 1.5230 | 0.4013 | 1.9164 |
| `solve/n4/b1` | 0.0006 | 0.0023 | 0.0008 |
| `solve/n4/b1024` | 0.2173 | 0.1119 | 0.7852 |
| `solve/n8/b1` | 0.0009 | 0.0034 | 0.0011 |
| `solve/n8/b1024` | 0.5413 | 0.1418 | 1.1690 |
| `svd_full/n16/b1` | 0.0335 | 0.0359 | 0.0495 |
| `svd_full/n16/b1024` | 33.4620 | 10.5427 | 48.4118 |
| `svd_full/n4/b1` | 0.0029 | 0.0049 | 0.0043 |
| `svd_full/n4/b1024` | 2.6346 | 1.3046 | 3.8586 |
| `svd_full/n8/b1` | 0.0090 | 0.0116 | 0.0126 |
| `svd_full/n8/b1024` | 9.1443 | 2.2956 | 12.7507 |
| `svd_thin/n16/b1` | 0.0326 | 0.0356 | 0.0490 |
| `svd_thin/n16/b1024` | 33.4358 | 8.5198 | 48.7927 |
| `svd_thin/n4/b1` | 0.0028 | 0.0049 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5510 | 1.2863 | 3.8373 |
| `svd_thin/n8/b1` | 0.0091 | 0.0119 | 0.0125 |
| `svd_thin/n8/b1024` | 9.0224 | 4.6006 | 12.7560 |
| `svd_values/n16/b1` | 0.0238 | 0.0268 | 0.0150 |
| `svd_values/n16/b1024` | 24.4173 | 10.1072 | 15.0698 |
| `svd_values/n4/b1` | 0.0021 | 0.0037 | 0.0026 |
| `svd_values/n4/b1024` | 1.9089 | 0.9678 | 2.0668 |
| `svd_values/n8/b1` | 0.0069 | 0.0091 | 0.0056 |
| `svd_values/n8/b1024` | 6.7641 | 2.2180 | 5.3469 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0021 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3086 | 0.0813 | 0.6992 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0005 |
| `triangular_solve/n4/b1024` | 0.0512 | 0.0214 | 0.4622 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0022 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1331 | 0.0384 | 0.5429 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0023 | 0.0007 |
| `cholesky/n16/b1024` | 0.5070 | 0.1298 | 0.6354 |
| `cholesky/n4/b1` | 0.0003 | 0.0028 | 0.0002 |
| `cholesky/n4/b1024` | 0.1071 | 0.0313 | 0.1188 |
| `cholesky/n8/b1` | 0.0003 | 0.0030 | 0.0003 |
| `cholesky/n8/b1024` | 0.2137 | 0.0359 | 0.2343 |
| `eig/n16/b1` | 0.0537 | 0.0569 | 0.0402 |
| `eig/n16/b1024` | 55.9666 | 11.0711 | 41.7643 |
| `eig/n4/b1` | 0.0040 | 0.0074 | 0.0037 |
| `eig/n4/b1024` | 3.5452 | 0.8971 | 3.2442 |
| `eig/n8/b1` | 0.0143 | 0.0171 | 0.0111 |
| `eig/n8/b1024` | 13.6939 | 3.4639 | 10.6349 |
| `eigh/n16/b1` | 0.0177 | 0.0204 | 0.0231 |
| `eigh/n16/b1024` | 17.8419 | 2.2647 | 24.5356 |
| `eigh/n4/b1` | 0.0017 | 0.0043 | 0.0020 |
| `eigh/n4/b1024` | 1.4661 | 0.3708 | 1.8592 |
| `eigh/n8/b1` | 0.0052 | 0.0083 | 0.0064 |
| `eigh/n8/b1024` | 5.0469 | 0.6417 | 6.5277 |
| `eigvals/n16/b1` | 0.0372 | 0.0404 | 0.0290 |
| `eigvals/n16/b1024` | 38.9946 | 5.4458 | 29.6592 |
| `eigvals/n4/b1` | 0.0023 | 0.0054 | 0.0025 |
| `eigvals/n4/b1024` | 1.8874 | 0.4773 | 2.0332 |
| `eigvals/n8/b1` | 0.0098 | 0.0121 | 0.0085 |
| `eigvals/n8/b1024` | 9.2026 | 1.5158 | 7.9136 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0162 | 0.0085 |
| `eigvalsh/n16/b1024` | 13.2557 | 2.2114 | 8.7778 |
| `eigvalsh/n4/b1` | 0.0014 | 0.0040 | 0.0011 |
| `eigvalsh/n4/b1024` | 1.1825 | 0.1697 | 0.8460 |
| `eigvalsh/n8/b1` | 0.0044 | 0.0072 | 0.0030 |
| `eigvalsh/n8/b1024` | 4.0584 | 1.0225 | 2.7800 |
| `full_piv_lu/n16/b1` | 0.0026 | 0.0056 | 0.0027 |
| `full_piv_lu/n16/b1024` | 2.0780 | 0.5100 | 2.7319 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0031 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2303 | 0.0368 | 0.2220 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0043 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6112 | 0.1611 | 0.5917 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0059 | 0.0040 |
| `full_piv_lu_solve/n16/b1024` | 2.0284 | 0.2741 | 3.7644 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0033 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3148 | 0.0654 | 0.5794 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0042 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7170 | 0.1873 | 1.1791 |
| `householder_apply/n16/b1` | 0.0027 | 0.0056 | 0.0030 |
| `householder_apply/n16/b1024` | 2.6898 | 0.6737 | 2.7536 |
| `householder_apply/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2016 | 0.0553 | 0.2472 |
| `householder_apply/n8/b1` | 0.0008 | 0.0033 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6809 | 0.1345 | 0.7186 |
| `householder_factor/n16/b1` | 0.0022 | 0.0054 | 0.0027 |
| `householder_factor/n16/b1024` | 2.1162 | 0.5409 | 2.6424 |
| `householder_factor/n4/b1` | 0.0004 | 0.0038 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2617 | 0.0707 | 0.3205 |
| `householder_factor/n8/b1` | 0.0008 | 0.0038 | 0.0011 |
| `householder_factor/n8/b1024` | 0.7015 | 0.1848 | 0.9050 |
| `lu/n16/b1` | 0.0019 | 0.0052 | 0.0017 |
| `lu/n16/b1024` | 1.4964 | 0.3826 | 1.4400 |
| `lu/n4/b1` | 0.0004 | 0.0028 | 0.0004 |
| `lu/n4/b1024` | 0.1797 | 0.0479 | 0.1958 |
| `lu/n8/b1` | 0.0007 | 0.0033 | 0.0007 |
| `lu/n8/b1024` | 0.4786 | 0.1283 | 0.4771 |
| `lu_factor/n16/b1` | 0.0013 | 0.0043 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1143 | 0.2794 | 1.0907 |
| `lu_factor/n4/b1` | 0.0003 | 0.0023 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1325 | 0.0246 | 0.1303 |
| `lu_factor/n8/b1` | 0.0005 | 0.0029 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3447 | 0.0953 | 0.3408 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0051 | 0.0021 |
| `lu_factor_solve/n16/b1024` | 1.3956 | 0.3550 | 2.0253 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0034 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.1687 | 0.0467 | 0.6599 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0039 | 0.0011 |
| `lu_factor_solve/n8/b1024` | 0.4801 | 0.0664 | 0.9011 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0032 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3605 | 0.1061 | 0.6720 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0035 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | 0.0194 | 0.5034 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0029 | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.1378 | 0.0449 | 0.4737 |
| `qr/n16/b1` | 0.0054 | 0.0080 | 0.0048 |
| `qr/n16/b1024` | 5.2372 | 1.3160 | 4.7535 |
| `qr/n4/b1` | 0.0008 | 0.0036 | 0.0008 |
| `qr/n4/b1024` | 0.4310 | 0.0866 | 0.5670 |
| `qr/n8/b1` | 0.0016 | 0.0050 | 0.0018 |
| `qr/n8/b1024` | 1.3815 | 0.3531 | 1.5655 |
| `rank_revealing_qr/n16/b1` | 0.0066 | 0.0102 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.3087 | 1.5362 | 5.5880 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0047 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6990 | 0.1843 | 0.6953 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0053 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.9027 | 0.4708 | 1.8041 |
| `solve/n16/b1` | 0.0021 | 0.0055 | 0.0023 |
| `solve/n16/b1024` | 1.5204 | 0.2141 | 1.9778 |
| `solve/n4/b1` | 0.0006 | 0.0039 | 0.0011 |
| `solve/n4/b1024` | 0.2185 | 0.0589 | 0.8235 |
| `solve/n8/b1` | 0.0010 | 0.0038 | 0.0011 |
| `solve/n8/b1024` | 0.5448 | 0.1406 | 1.2361 |
| `svd_full/n16/b1` | 0.0340 | 0.0354 | 0.0495 |
| `svd_full/n16/b1024` | 33.9454 | 5.0016 | 48.1911 |
| `svd_full/n4/b1` | 0.0027 | 0.0057 | 0.0042 |
| `svd_full/n4/b1024` | 2.5705 | 0.3437 | 3.8323 |
| `svd_full/n8/b1` | 0.0090 | 0.0118 | 0.0125 |
| `svd_full/n8/b1024` | 9.0465 | 1.1557 | 12.7741 |
| `svd_thin/n16/b1` | 0.0325 | 0.0364 | 0.0488 |
| `svd_thin/n16/b1024` | 33.4418 | 7.9944 | 48.3099 |
| `svd_thin/n4/b1` | 0.0029 | 0.0056 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5483 | 0.6425 | 3.8061 |
| `svd_thin/n8/b1` | 0.0095 | 0.0117 | 0.0124 |
| `svd_thin/n8/b1024` | 8.9720 | 1.1898 | 12.6774 |
| `svd_values/n16/b1` | 0.0238 | 0.0268 | 0.0150 |
| `svd_values/n16/b1024` | 24.6980 | 3.1075 | 15.0113 |
| `svd_values/n4/b1` | 0.0021 | 0.0052 | 0.0026 |
| `svd_values/n4/b1024` | 1.9252 | 0.4841 | 2.0582 |
| `svd_values/n8/b1` | 0.0068 | 0.0097 | 0.0055 |
| `svd_values/n8/b1024` | 6.7831 | 1.7196 | 5.3422 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0041 | 0.0007 |
| `triangular_solve/n16/b1024` | 0.3047 | 0.0509 | 0.7054 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0036 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0519 | 0.0142 | 0.4609 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0028 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1316 | 0.0369 | 0.5576 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | - | 0.0010 |
| `cholesky/n16/b1024` | 0.7746 | - | 0.9521 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1180 | - | 0.1360 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2546 | - | 0.2958 |
| `eig/n16/b1` | 0.0723 | - | 0.1005 |
| `eig/n16/b1024` | 76.5991 | - | 119.6718 |
| `eig/n4/b1` | 0.0059 | - | 0.0082 |
| `eig/n4/b1024` | 5.9124 | - | 7.9341 |
| `eig/n8/b1` | 0.0202 | - | 0.0263 |
| `eig/n8/b1024` | 20.5374 | - | 28.1420 |
| `eigh/n16/b1` | 0.0180 | - | 0.0259 |
| `eigh/n16/b1024` | 19.3679 | - | 27.0545 |
| `eigh/n4/b1` | 0.0019 | - | 0.0022 |
| `eigh/n4/b1024` | 1.7362 | - | 2.1263 |
| `eigh/n8/b1` | 0.0056 | - | 0.0072 |
| `eigh/n8/b1024` | 5.4563 | - | 7.4028 |
| `eigvals/n16/b1` | 0.0435 | - | 0.0749 |
| `eigvals/n16/b1024` | 46.3165 | - | 89.9945 |
| `eigvals/n4/b1` | 0.0030 | - | 0.0063 |
| `eigvals/n4/b1024` | 2.8324 | - | 6.0641 |
| `eigvals/n8/b1` | 0.0118 | - | 0.0211 |
| `eigvals/n8/b1024` | 11.8923 | - | 22.2464 |
| `eigvalsh/n16/b1` | 0.0136 | - | 0.0115 |
| `eigvalsh/n16/b1024` | 14.2354 | - | 11.4866 |
| `eigvalsh/n4/b1` | 0.0016 | - | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4138 | - | 1.2471 |
| `eigvalsh/n8/b1` | 0.0046 | - | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3720 | - | 3.6434 |
| `full_piv_lu/n16/b1` | 0.0032 | - | 0.0124 |
| `full_piv_lu/n16/b1024` | 2.9580 | - | 20.7020 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2670 | - | 0.5321 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7307 | - | 2.2695 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | - | 0.0156 |
| `full_piv_lu_solve/n16/b1024` | 3.1359 | - | 22.8998 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4703 | - | 1.1636 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0036 |
| `full_piv_lu_solve/n8/b1024` | 1.1395 | - | 3.6178 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0046 |
| `householder_apply/n16/b1024` | 3.3159 | - | 4.4730 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0008 |
| `householder_apply/n4/b1024` | 0.2030 | - | 0.2617 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0014 |
| `householder_apply/n8/b1024` | 0.6809 | - | 0.8928 |
| `householder_factor/n16/b1` | 0.0027 | - | 0.0045 |
| `householder_factor/n16/b1024` | 2.7373 | - | 4.4434 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0007 |
| `householder_factor/n4/b1024` | 0.3217 | - | 0.5497 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0016 |
| `householder_factor/n8/b1024` | 0.8503 | - | 1.4215 |
| `lu/n16/b1` | 0.0021 | - | 0.0023 |
| `lu/n16/b1024` | 1.8594 | - | 2.4844 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.2097 | - | 0.2301 |
| `lu/n8/b1` | 0.0008 | - | 0.0008 |
| `lu/n8/b1024` | 0.5233 | - | 0.6225 |
| `lu_factor/n16/b1` | 0.0015 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2169 | - | 1.6358 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1600 | - | 0.1636 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0005 |
| `lu_factor/n8/b1024` | 0.3920 | - | 0.4575 |
| `lu_factor_solve/n16/b1` | 0.0023 | - | 0.0026 |
| `lu_factor_solve/n16/b1024` | 2.0419 | - | 2.6202 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0005 |
| `lu_factor_solve/n4/b1024` | 0.2613 | - | 0.4063 |
| `lu_factor_solve/n8/b1` | 0.0010 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6768 | - | 0.9093 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7874 | - | 1.0176 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0971 | - | 0.2436 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.2863 | - | 0.4544 |
| `qr/n16/b1` | 0.0067 | - | 0.0077 |
| `qr/n16/b1024` | 6.6143 | - | 7.5941 |
| `qr/n4/b1` | 0.0007 | - | 0.0012 |
| `qr/n4/b1024` | 0.5100 | - | 0.8269 |
| `qr/n8/b1` | 0.0018 | - | 0.0026 |
| `qr/n8/b1024` | 1.5494 | - | 2.2283 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.4200 | - | 10.1248 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8437 | - | 1.0961 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1786 | - | 3.0235 |
| `solve/n16/b1` | 0.0027 | - | 0.0030 |
| `solve/n16/b1024` | 2.3086 | - | 2.7608 |
| `solve/n4/b1` | 0.0007 | - | 0.0007 |
| `solve/n4/b1024` | 0.3209 | - | 0.4375 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7857 | - | 0.9693 |
| `svd_full/n16/b1` | 0.0347 | - | 0.0549 |
| `svd_full/n16/b1024` | 37.7850 | - | 56.4853 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_full/n4/b1024` | 3.0278 | - | 4.7361 |
| `svd_full/n8/b1` | 0.0096 | - | 0.0147 |
| `svd_full/n8/b1024` | 10.0963 | - | 14.9583 |
| `svd_thin/n16/b1` | 0.0346 | - | 0.0554 |
| `svd_thin/n16/b1024` | 36.5400 | - | 56.3719 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_thin/n4/b1024` | 3.0221 | - | 4.8218 |
| `svd_thin/n8/b1` | 0.0096 | - | 0.0147 |
| `svd_thin/n8/b1024` | 10.0953 | - | 14.9711 |
| `svd_values/n16/b1` | 0.0260 | - | 0.0199 |
| `svd_values/n16/b1024` | 27.3836 | - | 20.0857 |
| `svd_values/n4/b1` | 0.0026 | - | 0.0032 |
| `svd_values/n4/b1024` | 2.3002 | - | 2.7645 |
| `svd_values/n8/b1` | 0.0076 | - | 0.0071 |
| `svd_values/n8/b1024` | 7.7526 | - | 6.7633 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0007 |
| `triangular_solve/n16/b1024` | 0.5856 | - | 0.6081 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0972 | - | 0.1676 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.2402 | - | 0.2701 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0033 | 0.0010 |
| `cholesky/n16/b1024` | 0.7630 | 0.3239 | 0.9318 |
| `cholesky/n4/b1` | 0.0003 | 0.0028 | 0.0002 |
| `cholesky/n4/b1024` | 0.1175 | 0.0632 | 0.1368 |
| `cholesky/n8/b1` | 0.0004 | 0.0026 | 0.0004 |
| `cholesky/n8/b1024` | 0.2486 | 0.0656 | 0.2872 |
| `eig/n16/b1` | 0.0722 | 0.0763 | 0.1006 |
| `eig/n16/b1024` | 76.2715 | 19.7854 | 120.0614 |
| `eig/n4/b1` | 0.0059 | 0.0085 | 0.0081 |
| `eig/n4/b1024` | 5.9199 | 2.7946 | 7.9755 |
| `eig/n8/b1` | 0.0199 | 0.0227 | 0.0261 |
| `eig/n8/b1024` | 20.4311 | 8.4278 | 27.9920 |
| `eigh/n16/b1` | 0.0179 | 0.0206 | 0.0260 |
| `eigh/n16/b1024` | 19.5318 | 5.5647 | 26.9267 |
| `eigh/n4/b1` | 0.0019 | 0.0045 | 0.0022 |
| `eigh/n4/b1024` | 1.7387 | 0.8896 | 2.1387 |
| `eigh/n8/b1` | 0.0057 | 0.0089 | 0.0072 |
| `eigh/n8/b1024` | 5.4569 | 1.6957 | 7.3973 |
| `eigvals/n16/b1` | 0.0432 | 0.0464 | 0.0746 |
| `eigvals/n16/b1024` | 46.4429 | 11.6542 | 90.2812 |
| `eigvals/n4/b1` | 0.0030 | 0.0052 | 0.0064 |
| `eigvals/n4/b1024` | 2.8364 | 1.4501 | 6.0510 |
| `eigvals/n8/b1` | 0.0116 | 0.0147 | 0.0211 |
| `eigvals/n8/b1024` | 11.8398 | 4.0258 | 22.2255 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0166 | 0.0116 |
| `eigvalsh/n16/b1024` | 14.2744 | 6.9870 | 11.4981 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0040 | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4203 | 0.7241 | 1.2499 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0063 | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3625 | 2.2199 | 3.6638 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0056 | 0.0118 |
| `full_piv_lu/n16/b1024` | 2.9491 | 1.3703 | 20.3392 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0023 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2611 | 0.1367 | 0.5485 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0035 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7433 | 0.3645 | 2.2917 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0066 | 0.0157 |
| `full_piv_lu_solve/n16/b1024` | 3.1966 | 0.7979 | 22.8090 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0034 | 0.0015 |
| `full_piv_lu_solve/n4/b1024` | 0.4652 | 0.1257 | 1.2758 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0038 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1357 | 0.2934 | 3.6852 |
| `householder_apply/n16/b1` | 0.0028 | 0.0052 | 0.0045 |
| `householder_apply/n16/b1024` | 3.6221 | 0.9977 | 4.4998 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0008 |
| `householder_apply/n4/b1024` | 0.2049 | 0.0599 | 0.2574 |
| `householder_apply/n8/b1` | 0.0007 | 0.0032 | 0.0016 |
| `householder_apply/n8/b1024` | 0.6581 | 0.1723 | 0.9220 |
| `householder_factor/n16/b1` | 0.0027 | 0.0042 | 0.0046 |
| `householder_factor/n16/b1024` | 2.6840 | 1.3718 | 4.4403 |
| `householder_factor/n4/b1` | 0.0004 | 0.0025 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3225 | 0.0866 | 0.5517 |
| `householder_factor/n8/b1` | 0.0009 | 0.0033 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8488 | 0.2187 | 1.4457 |
| `lu/n16/b1` | 0.0021 | 0.0046 | 0.0023 |
| `lu/n16/b1024` | 1.8495 | 0.9017 | 2.4522 |
| `lu/n4/b1` | 0.0004 | 0.0027 | 0.0004 |
| `lu/n4/b1024` | 0.2007 | 0.0605 | 0.2377 |
| `lu/n8/b1` | 0.0007 | 0.0027 | 0.0008 |
| `lu/n8/b1024` | 0.5240 | 0.2734 | 0.6544 |
| `lu_factor/n16/b1` | 0.0015 | 0.0030 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2150 | 0.4518 | 1.6118 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1617 | 0.0468 | 0.1619 |
| `lu_factor/n8/b1` | 0.0006 | 0.0023 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3905 | 0.1030 | 0.4480 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0049 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0244 | 1.0520 | 3.0280 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0022 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2527 | 0.0685 | 0.8365 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0033 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6835 | 0.3448 | 1.4154 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0034 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7859 | 0.2073 | 1.2117 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0971 | 0.0335 | 0.6232 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0026 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2875 | 0.0838 | 0.8131 |
| `qr/n16/b1` | 0.0067 | 0.0098 | 0.0076 |
| `qr/n16/b1024` | 6.6813 | 2.6451 | 7.6598 |
| `qr/n4/b1` | 0.0007 | 0.0024 | 0.0011 |
| `qr/n4/b1024` | 0.5068 | 0.1307 | 0.8247 |
| `qr/n8/b1` | 0.0018 | 0.0034 | 0.0026 |
| `qr/n8/b1024` | 1.5558 | 0.7843 | 2.2416 |
| `rank_revealing_qr/n16/b1` | 0.0074 | 0.0099 | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.3274 | 1.8393 | 10.0718 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0034 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8117 | 0.4156 | 1.0961 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0048 | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.1790 | 1.1203 | 3.0291 |
| `solve/n16/b1` | 0.0028 | 0.0054 | 0.0031 |
| `solve/n16/b1024` | 2.2064 | 0.5799 | 3.0145 |
| `solve/n4/b1` | 0.0007 | 0.0032 | 0.0009 |
| `solve/n4/b1024` | 0.3178 | 0.0847 | 0.6686 |
| `solve/n8/b1` | 0.0012 | 0.0035 | 0.0013 |
| `solve/n8/b1024` | 0.7841 | 0.2017 | 1.2128 |
| `svd_full/n16/b1` | 0.0347 | 0.0377 | 0.0546 |
| `svd_full/n16/b1024` | 36.6120 | 9.5827 | 56.4423 |
| `svd_full/n4/b1` | 0.0031 | 0.0051 | 0.0053 |
| `svd_full/n4/b1024` | 3.0165 | 1.1958 | 4.7463 |
| `svd_full/n8/b1` | 0.0097 | 0.0124 | 0.0147 |
| `svd_full/n8/b1024` | 10.2646 | 3.5872 | 14.9806 |
| `svd_thin/n16/b1` | 0.0349 | 0.0377 | 0.0550 |
| `svd_thin/n16/b1024` | 36.6910 | 9.5803 | 56.4999 |
| `svd_thin/n4/b1` | 0.0031 | 0.0052 | 0.0053 |
| `svd_thin/n4/b1024` | 3.0181 | 1.5390 | 4.7214 |
| `svd_thin/n8/b1` | 0.0097 | 0.0125 | 0.0146 |
| `svd_thin/n8/b1024` | 10.1117 | 2.5715 | 14.9962 |
| `svd_values/n16/b1` | 0.0262 | 0.0290 | 0.0198 |
| `svd_values/n16/b1024` | 27.3511 | 7.0403 | 20.2225 |
| `svd_values/n4/b1` | 0.0025 | 0.0052 | 0.0033 |
| `svd_values/n4/b1024` | 2.3157 | 0.5827 | 2.7761 |
| `svd_values/n8/b1` | 0.0076 | 0.0103 | 0.0072 |
| `svd_values/n8/b1024` | 7.7491 | 3.2791 | 6.7981 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0024 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6021 | 0.3049 | 0.8254 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0966 | 0.0326 | 0.4060 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0021 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2391 | 0.1249 | 0.6024 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0040 | 0.0010 |
| `cholesky/n16/b1024` | 0.7804 | 0.2020 | 0.9707 |
| `cholesky/n4/b1` | 0.0003 | 0.0034 | 0.0003 |
| `cholesky/n4/b1024` | 0.1209 | 0.0344 | 0.1394 |
| `cholesky/n8/b1` | 0.0004 | 0.0023 | 0.0004 |
| `cholesky/n8/b1024` | 0.2532 | 0.0687 | 0.2915 |
| `eig/n16/b1` | 0.0720 | 0.0764 | 0.1001 |
| `eig/n16/b1024` | 76.2516 | 15.7983 | 119.4723 |
| `eig/n4/b1` | 0.0058 | 0.0092 | 0.0082 |
| `eig/n4/b1024` | 5.8075 | 0.7738 | 8.0044 |
| `eig/n8/b1` | 0.0200 | 0.0230 | 0.0262 |
| `eig/n8/b1024` | 20.5261 | 2.6482 | 27.8643 |
| `eigh/n16/b1` | 0.0180 | 0.0210 | 0.0265 |
| `eigh/n16/b1024` | 19.3947 | 3.3633 | 27.3406 |
| `eigh/n4/b1` | 0.0020 | 0.0054 | 0.0023 |
| `eigh/n4/b1024` | 1.7348 | 0.4457 | 2.1629 |
| `eigh/n8/b1` | 0.0057 | 0.0081 | 0.0073 |
| `eigh/n8/b1024` | 5.4466 | 0.7018 | 7.4691 |
| `eigvals/n16/b1` | 0.0437 | 0.0466 | 0.0748 |
| `eigvals/n16/b1024` | 46.7461 | 6.2927 | 89.9257 |
| `eigvals/n4/b1` | 0.0031 | 0.0059 | 0.0064 |
| `eigvals/n4/b1024` | 2.8296 | 0.7139 | 6.0136 |
| `eigvals/n8/b1` | 0.0118 | 0.0145 | 0.0210 |
| `eigvals/n8/b1024` | 11.9630 | 2.1110 | 22.2115 |
| `eigvalsh/n16/b1` | 0.0135 | 0.0165 | 0.0116 |
| `eigvalsh/n16/b1024` | 14.2521 | 3.5883 | 11.6867 |
| `eigvalsh/n4/b1` | 0.0017 | 0.0048 | 0.0016 |
| `eigvalsh/n4/b1024` | 1.4215 | 0.2013 | 1.2831 |
| `eigvalsh/n8/b1` | 0.0046 | 0.0078 | 0.0040 |
| `eigvalsh/n8/b1024` | 4.4001 | 0.5556 | 3.7036 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0061 | 0.0118 |
| `full_piv_lu/n16/b1024` | 2.9299 | 0.4596 | 20.1891 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0047 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2612 | 0.0726 | 0.5392 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0041 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7389 | 0.1902 | 2.2659 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0067 | 0.0153 |
| `full_piv_lu_solve/n16/b1024` | 3.1056 | 0.4293 | 22.7714 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0041 | 0.0015 |
| `full_piv_lu_solve/n4/b1024` | 0.4685 | 0.0675 | 1.2873 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0040 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1331 | 0.2954 | 3.7399 |
| `householder_apply/n16/b1` | 0.0027 | 0.0059 | 0.0047 |
| `householder_apply/n16/b1024` | 3.4972 | 0.7265 | 4.3824 |
| `householder_apply/n4/b1` | 0.0003 | 0.0040 | 0.0008 |
| `householder_apply/n4/b1024` | 0.2004 | 0.0547 | 0.2574 |
| `householder_apply/n8/b1` | 0.0008 | 0.0031 | 0.0016 |
| `householder_apply/n8/b1024` | 0.6583 | 0.1696 | 0.8825 |
| `householder_factor/n16/b1` | 0.0027 | 0.0055 | 0.0044 |
| `householder_factor/n16/b1024` | 2.6680 | 0.6756 | 4.4468 |
| `householder_factor/n4/b1` | 0.0004 | 0.0031 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3209 | 0.0521 | 0.5498 |
| `householder_factor/n8/b1` | 0.0010 | 0.0047 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8481 | 0.1175 | 1.4169 |
| `lu/n16/b1` | 0.0020 | 0.0054 | 0.0023 |
| `lu/n16/b1024` | 1.8120 | 0.2989 | 2.6720 |
| `lu/n4/b1` | 0.0004 | 0.0036 | 0.0004 |
| `lu/n4/b1024` | 0.2062 | 0.0580 | 0.2399 |
| `lu/n8/b1` | 0.0007 | 0.0033 | 0.0008 |
| `lu/n8/b1024` | 0.5348 | 0.0779 | 0.6256 |
| `lu_factor/n16/b1` | 0.0015 | 0.0046 | 0.0016 |
| `lu_factor/n16/b1024` | 1.1838 | 0.2578 | 1.6114 |
| `lu_factor/n4/b1` | 0.0004 | 0.0038 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1585 | 0.0450 | 0.1648 |
| `lu_factor/n8/b1` | 0.0006 | 0.0037 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3840 | 0.1075 | 0.4553 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0056 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0187 | 0.5161 | 3.0192 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0037 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2544 | 0.0693 | 0.8392 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0035 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6768 | 0.1779 | 1.4033 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0041 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7940 | 0.2091 | 1.1844 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0025 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0962 | 0.0336 | 0.6168 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0037 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2865 | 0.0854 | 0.8120 |
| `qr/n16/b1` | 0.0068 | 0.0098 | 0.0076 |
| `qr/n16/b1024` | 6.7027 | 1.6689 | 7.5872 |
| `qr/n4/b1` | 0.0007 | 0.0028 | 0.0012 |
| `qr/n4/b1024` | 0.5013 | 0.0724 | 0.8302 |
| `qr/n8/b1` | 0.0018 | 0.0051 | 0.0025 |
| `qr/n8/b1024` | 1.5546 | 0.3925 | 2.2284 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0100 | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.3120 | 0.9493 | 10.0181 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0038 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8163 | 0.1133 | 1.0948 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0057 | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1861 | 0.5496 | 3.0109 |
| `solve/n16/b1` | 0.0028 | 0.0057 | 0.0031 |
| `solve/n16/b1024` | 2.1766 | 0.4500 | 3.2244 |
| `solve/n4/b1` | 0.0007 | 0.0042 | 0.0009 |
| `solve/n4/b1024` | 0.3119 | 0.0843 | 0.8727 |
| `solve/n8/b1` | 0.0012 | 0.0045 | 0.0014 |
| `solve/n8/b1024` | 0.7830 | 0.2034 | 1.4087 |
| `svd_full/n16/b1` | 0.0348 | 0.0376 | 0.0545 |
| `svd_full/n16/b1024` | 36.4390 | 5.1411 | 56.3363 |
| `svd_full/n4/b1` | 0.0031 | 0.0062 | 0.0053 |
| `svd_full/n4/b1024` | 3.1202 | 0.7616 | 4.7238 |
| `svd_full/n8/b1` | 0.0096 | 0.0122 | 0.0148 |
| `svd_full/n8/b1024` | 10.2893 | 1.3152 | 14.9355 |
| `svd_thin/n16/b1` | 0.0350 | 0.0376 | 0.0550 |
| `svd_thin/n16/b1024` | 36.4779 | 5.3345 | 56.3913 |
| `svd_thin/n4/b1` | 0.0031 | 0.0060 | 0.0053 |
| `svd_thin/n4/b1024` | 3.0252 | 0.7622 | 4.7386 |
| `svd_thin/n8/b1` | 0.0098 | 0.0124 | 0.0146 |
| `svd_thin/n8/b1024` | 10.0858 | 1.3173 | 14.9395 |
| `svd_values/n16/b1` | 0.0260 | 0.0292 | 0.0198 |
| `svd_values/n16/b1024` | 27.2132 | 6.5703 | 20.1331 |
| `svd_values/n4/b1` | 0.0025 | 0.0050 | 0.0033 |
| `svd_values/n4/b1024` | 2.3028 | 0.5828 | 2.7678 |
| `svd_values/n8/b1` | 0.0076 | 0.0107 | 0.0072 |
| `svd_values/n8/b1024` | 7.7473 | 1.9752 | 6.8506 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0037 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5944 | 0.1533 | 0.7494 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0037 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0972 | 0.0282 | 0.4555 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0038 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2374 | 0.0641 | 0.5280 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0375 | - | 0.0402 |
| `cholesky/n128/b128` | 5.7169 | - | 6.3237 |
| `cholesky/n32/b1` | 0.0020 | - | 0.0020 |
| `cholesky/n32/b128` | 0.2421 | - | 0.2550 |
| `eigh/n128/b1` | 1.2564 | - | 1.1245 |
| `eigh/n128/b128` | 161.7992 | - | 148.2249 |
| `eigh/n32/b1` | 0.0634 | - | 0.0780 |
| `eigh/n32/b128` | 8.3738 | - | 10.0010 |
| `eigvalsh/n128/b1` | 0.7022 | - | 0.4999 |
| `eigvalsh/n128/b128` | 91.0030 | - | 64.6046 |
| `eigvalsh/n32/b1` | 0.0491 | - | 0.0289 |
| `eigvalsh/n32/b128` | 6.4849 | - | 3.7573 |
| `householder_apply/n128/b1` | 0.1276 | - | 0.2564 |
| `householder_apply/n128/b128` | 17.3067 | - | 33.9919 |
| `householder_apply/n32/b1` | 0.0108 | - | 0.0110 |
| `householder_apply/n32/b128` | 1.3585 | - | 1.3469 |
| `householder_factor/n128/b1` | 0.1091 | - | 0.2185 |
| `householder_factor/n128/b128` | 14.0473 | - | 28.5243 |
| `householder_factor/n32/b1` | 0.0075 | - | 0.0085 |
| `householder_factor/n32/b128` | 0.9415 | - | 1.0727 |
| `lu/n128/b1` | 0.0900 | - | 0.0872 |
| `lu/n128/b128` | 12.2402 | - | 13.5486 |
| `lu/n32/b1` | 0.0053 | - | 0.0050 |
| `lu/n32/b128` | 0.5829 | - | 0.6037 |
| `lu_factor/n128/b1` | 0.0561 | - | 0.0785 |
| `lu_factor/n128/b128` | 8.2450 | - | 11.1777 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0039 |
| `lu_factor/n32/b128` | 0.3802 | - | 0.4989 |
| `lu_factor_solve/n128/b1` | 0.0627 | - | 0.0905 |
| `lu_factor_solve/n128/b128` | 8.9239 | - | 12.4684 |
| `lu_factor_solve/n32/b1` | 0.0041 | - | 0.0058 |
| `lu_factor_solve/n32/b128` | 0.4833 | - | 0.7139 |
| `lu_solve_prepared/n128/b1` | 0.0060 | - | 0.0119 |
| `lu_solve_prepared/n128/b128` | 1.7749 | - | 2.7587 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0016 |
| `lu_solve_prepared/n32/b128` | 0.1141 | - | 0.2032 |
| `qr/n128/b1` | 0.3358 | - | 0.4264 |
| `qr/n128/b128` | 43.7441 | - | 56.9932 |
| `qr/n32/b1` | 0.0208 | - | 0.0159 |
| `qr/n32/b128` | 2.6074 | - | 2.0045 |
| `rank_revealing_qr/n128/b1` | 0.3457 | - | 0.4915 |
| `rank_revealing_qr/n128/b128` | 44.9404 | - | 64.9943 |
| `rank_revealing_qr/n32/b1` | 0.0204 | - | 0.0198 |
| `rank_revealing_qr/n32/b128` | 2.5776 | - | 2.4757 |
| `solve/n128/b1` | 0.0660 | - | 0.0919 |
| `solve/n128/b128` | 8.9005 | - | 12.5279 |
| `solve/n32/b1` | 0.0048 | - | 0.0062 |
| `solve/n32/b128` | 0.5305 | - | 0.7296 |
| `svd_thin/n128/b1` | 2.4122 | - | 2.0013 |
| `svd_thin/n128/b128` | 307.9531 | - | 259.9657 |
| `svd_thin/n32/b1` | 0.1168 | - | 0.1390 |
| `svd_thin/n32/b128` | 15.1513 | - | 17.9271 |
| `svd_values/n128/b1` | 1.4078 | - | 0.8117 |
| `svd_values/n128/b128` | 180.0967 | - | 105.4905 |
| `svd_values/n32/b1` | 0.0921 | - | 0.0461 |
| `svd_values/n32/b128` | 11.8588 | - | 5.9923 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0062 |
| `triangular_solve/n128/b128` | 0.8507 | - | 1.3133 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0010 |
| `triangular_solve/n32/b128` | 0.0889 | - | 0.1069 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0351 | 0.0436 | 0.0460 |
| `cholesky/n128/b128` | 5.2696 | 6.6689 | 6.8601 |
| `cholesky/n32/b1` | 0.0019 | 0.0045 | 0.0020 |
| `cholesky/n32/b128` | 0.2417 | 0.1223 | 0.2701 |
| `eigh/n128/b1` | 1.2655 | 1.2331 | 0.9025 |
| `eigh/n128/b128` | 163.3596 | 164.4778 | 117.5700 |
| `eigh/n32/b1` | 0.0641 | 0.0681 | 0.0707 |
| `eigh/n32/b128` | 8.4431 | 4.2355 | 9.0843 |
| `eigvalsh/n128/b1` | 0.7052 | 0.7016 | 0.4734 |
| `eigvalsh/n128/b128` | 91.6180 | 90.5610 | 61.8782 |
| `eigvalsh/n32/b1` | 0.0485 | 0.0515 | 0.0289 |
| `eigvalsh/n32/b128` | 6.3990 | 3.2316 | 3.7714 |
| `householder_apply/n128/b1` | 0.1257 | 0.1257 | 0.2333 |
| `householder_apply/n128/b128` | 17.3562 | 17.5804 | 31.4318 |
| `householder_apply/n32/b1` | 0.0109 | 0.0141 | 0.0109 |
| `householder_apply/n32/b128` | 1.3315 | 0.3486 | 1.3435 |
| `householder_factor/n128/b1` | 0.1050 | 0.1239 | 0.2293 |
| `householder_factor/n128/b128` | 13.6722 | 16.8392 | 29.9722 |
| `householder_factor/n32/b1` | 0.0075 | 0.0102 | 0.0086 |
| `householder_factor/n32/b128` | 0.9284 | 0.2424 | 1.0716 |
| `lu/n128/b1` | 0.0862 | 0.1026 | 0.0861 |
| `lu/n128/b128` | 12.0911 | 14.0570 | 13.6088 |
| `lu/n32/b1` | 0.0053 | 0.0084 | 0.0049 |
| `lu/n32/b128` | 0.5776 | 0.3028 | 0.6028 |
| `lu_factor/n128/b1` | 0.0554 | 0.0728 | 0.0774 |
| `lu_factor/n128/b128` | 8.3063 | 3.7613 | 11.0705 |
| `lu_factor/n32/b1` | 0.0032 | 0.0057 | 0.0038 |
| `lu_factor/n32/b128` | 0.3861 | 0.2035 | 0.4969 |
| `lu_factor_solve/n128/b1` | 0.0618 | 0.0772 | 0.0874 |
| `lu_factor_solve/n128/b128` | 8.9661 | 2.8875 | 12.1445 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0072 | 0.0053 |
| `lu_factor_solve/n32/b128` | 0.4889 | 0.2534 | 0.7332 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0090 | 0.0071 |
| `lu_solve_prepared/n128/b128` | 1.8711 | 0.9744 | 2.1112 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0041 | 0.0011 |
| `lu_solve_prepared/n32/b128` | 0.1137 | 0.0352 | 0.1600 |
| `qr/n128/b1` | 0.3385 | 0.6265 | 0.4546 |
| `qr/n128/b128` | 43.7638 | 80.0040 | 59.8439 |
| `qr/n32/b1` | 0.0208 | 0.0437 | 0.0160 |
| `qr/n32/b128` | 2.6048 | 0.6577 | 2.0173 |
| `rank_revealing_qr/n128/b1` | 0.3466 | 0.3595 | 0.5122 |
| `rank_revealing_qr/n128/b128` | 45.1980 | 48.3432 | 67.1354 |
| `rank_revealing_qr/n32/b1` | 0.0203 | 0.0461 | 0.0198 |
| `rank_revealing_qr/n32/b128` | 2.5292 | 0.6430 | 2.4745 |
| `solve/n128/b1` | 0.0668 | 0.0809 | 0.0918 |
| `solve/n128/b128` | 8.8491 | 10.6812 | 12.3703 |
| `solve/n32/b1` | 0.0047 | 0.0074 | 0.0058 |
| `solve/n32/b128` | 0.5223 | 0.2736 | 0.7019 |
| `svd_thin/n128/b1` | 2.4081 | 1.8132 | 2.0060 |
| `svd_thin/n128/b128` | 308.3503 | 231.0445 | 261.1006 |
| `svd_thin/n32/b1` | 0.1164 | 0.1215 | 0.1394 |
| `svd_thin/n32/b128` | 15.6151 | 6.9770 | 17.9227 |
| `svd_values/n128/b1` | 1.4050 | 1.4367 | 0.8282 |
| `svd_values/n128/b128` | 181.4928 | 180.7755 | 106.2775 |
| `svd_values/n32/b1` | 0.0916 | 0.0961 | 0.0459 |
| `svd_values/n32/b128` | 11.8298 | 5.1632 | 5.9974 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0072 | 0.0039 |
| `triangular_solve/n128/b128` | 1.0934 | 1.1347 | 1.2195 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0034 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0912 | 0.0473 | 0.1072 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0345 | 0.0517 | 0.0431 |
| `cholesky/n128/b128` | 5.3262 | 6.6644 | 6.5926 |
| `cholesky/n32/b1` | 0.0018 | 0.0047 | 0.0020 |
| `cholesky/n32/b128` | 0.2151 | 0.0376 | 0.2503 |
| `eigh/n128/b1` | 1.2607 | 1.2425 | 0.8693 |
| `eigh/n128/b128` | 162.2328 | 160.0110 | 112.9499 |
| `eigh/n32/b1` | 0.0631 | 0.0685 | 0.0692 |
| `eigh/n32/b128` | 8.4284 | 2.1373 | 8.9143 |
| `eigvalsh/n128/b1` | 0.6969 | 0.7027 | 0.4732 |
| `eigvalsh/n128/b128` | 90.3746 | 90.8699 | 61.5816 |
| `eigvalsh/n32/b1` | 0.0486 | 0.0521 | 0.0290 |
| `eigvalsh/n32/b128` | 6.3973 | 1.5461 | 3.7717 |
| `householder_apply/n128/b1` | 0.1238 | 0.1870 | 0.2324 |
| `householder_apply/n128/b128` | 17.1539 | 24.8007 | 31.3571 |
| `householder_apply/n32/b1` | 0.0109 | 0.0132 | 0.0106 |
| `householder_apply/n32/b128` | 1.3750 | 0.3459 | 1.3270 |
| `householder_factor/n128/b1` | 0.1041 | 0.1646 | 0.2286 |
| `householder_factor/n128/b128` | 13.5060 | 22.9202 | 29.8874 |
| `householder_factor/n32/b1` | 0.0072 | 0.0103 | 0.0085 |
| `householder_factor/n32/b128` | 0.9221 | 0.2396 | 1.0756 |
| `lu/n128/b1` | 0.0900 | 0.1163 | 0.0868 |
| `lu/n128/b128` | 12.1712 | 15.5506 | 13.5158 |
| `lu/n32/b1` | 0.0052 | 0.0080 | 0.0050 |
| `lu/n32/b128` | 0.5926 | 0.0861 | 0.6047 |
| `lu_factor/n128/b1` | 0.0562 | 0.0822 | 0.0780 |
| `lu_factor/n128/b128` | 8.2371 | 1.4678 | 11.0625 |
| `lu_factor/n32/b1` | 0.0032 | 0.0068 | 0.0039 |
| `lu_factor/n32/b128` | 0.3802 | 0.1060 | 0.4986 |
| `lu_factor_solve/n128/b1` | 0.0628 | 0.0897 | 0.0877 |
| `lu_factor_solve/n128/b128` | 8.9342 | 1.5896 | 12.2276 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0074 | 0.0053 |
| `lu_factor_solve/n32/b128` | 0.4849 | 0.1321 | 0.7372 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0091 | 0.0073 |
| `lu_solve_prepared/n128/b128` | 1.7599 | 0.4743 | 2.1914 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0035 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1136 | 0.0238 | 0.1631 |
| `qr/n128/b1` | 0.3353 | 0.9413 | 0.4463 |
| `qr/n128/b128` | 43.2057 | 122.5115 | 59.0643 |
| `qr/n32/b1` | 0.0208 | 0.0642 | 0.0159 |
| `qr/n32/b128` | 2.6321 | 0.3289 | 1.9891 |
| `rank_revealing_qr/n128/b1` | 0.3469 | 0.4175 | 0.5188 |
| `rank_revealing_qr/n128/b128` | 44.5821 | 55.9265 | 67.6053 |
| `rank_revealing_qr/n32/b1` | 0.0206 | 0.0692 | 0.0198 |
| `rank_revealing_qr/n32/b128` | 2.5351 | 0.6406 | 2.4550 |
| `solve/n128/b1` | 0.0671 | 0.0948 | 0.0922 |
| `solve/n128/b128` | 8.8997 | 12.0648 | 12.2594 |
| `solve/n32/b1` | 0.0048 | 0.0078 | 0.0058 |
| `solve/n32/b128` | 0.5302 | 0.1389 | 0.7125 |
| `svd_thin/n128/b1` | 2.4150 | 1.8460 | 1.9966 |
| `svd_thin/n128/b128` | 308.3946 | 237.5782 | 260.6816 |
| `svd_thin/n32/b1` | 0.1164 | 0.1228 | 0.1398 |
| `svd_thin/n32/b128` | 15.0172 | 2.4752 | 17.7664 |
| `svd_values/n128/b1` | 1.4111 | 1.4324 | 0.8198 |
| `svd_values/n128/b128` | 181.0202 | 180.2366 | 108.3236 |
| `svd_values/n32/b1` | 0.0920 | 0.0964 | 0.0460 |
| `svd_values/n32/b128` | 11.8687 | 2.0239 | 5.9927 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0070 | 0.0039 |
| `triangular_solve/n128/b128` | 0.8286 | 0.8241 | 1.2015 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0036 | 0.0008 |
| `triangular_solve/n32/b128` | 0.0889 | 0.0252 | 0.1025 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1083 | - | 0.1090 |
| `cholesky/n128/b128` | 16.0224 | - | 15.6357 |
| `cholesky/n32/b1` | 0.0033 | - | 0.0035 |
| `cholesky/n32/b128` | 0.4199 | - | 0.4374 |
| `eigh/n128/b1` | 1.8494 | - | 3.2680 |
| `eigh/n128/b128` | 241.5512 | - | 422.5061 |
| `eigh/n32/b1` | 0.0812 | - | 0.1085 |
| `eigh/n32/b128` | 10.6466 | - | 14.0356 |
| `eigvalsh/n128/b1` | 0.9323 | - | 0.9494 |
| `eigvalsh/n128/b128` | 122.2396 | - | 123.7688 |
| `eigvalsh/n32/b1` | 0.0529 | - | 0.0418 |
| `eigvalsh/n32/b128` | 6.9854 | - | 5.4270 |
| `householder_apply/n128/b1` | 0.4845 | - | 0.6904 |
| `householder_apply/n128/b128` | 64.4947 | - | 91.8530 |
| `householder_apply/n32/b1` | 0.0145 | - | 0.0196 |
| `householder_apply/n32/b128` | 1.8711 | - | 2.4998 |
| `householder_factor/n128/b1` | 0.3512 | - | 0.4348 |
| `householder_factor/n128/b128` | 46.3206 | - | 57.4770 |
| `householder_factor/n32/b1` | 0.0114 | - | 0.0158 |
| `householder_factor/n32/b128` | 1.4418 | - | 2.0251 |
| `lu/n128/b1` | 0.1922 | - | 0.2127 |
| `lu/n128/b128` | 27.3940 | - | 31.2652 |
| `lu/n32/b1` | 0.0075 | - | 0.0080 |
| `lu/n32/b128` | 1.0165 | - | 1.1225 |
| `lu_factor/n128/b1` | 0.1561 | - | 0.1918 |
| `lu_factor/n128/b128` | 21.8398 | - | 25.6536 |
| `lu_factor/n32/b1` | 0.0054 | - | 0.0065 |
| `lu_factor/n32/b128` | 0.6682 | - | 0.8299 |
| `lu_factor_solve/n128/b1` | 0.1746 | - | 0.2211 |
| `lu_factor_solve/n128/b128` | 24.3431 | - | 29.3532 |
| `lu_factor_solve/n32/b1` | 0.0076 | - | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9370 | - | 1.1334 |
| `lu_solve_prepared/n128/b1` | 0.0187 | - | 0.0284 |
| `lu_solve_prepared/n128/b128` | 4.0845 | - | 5.1630 |
| `lu_solve_prepared/n32/b1` | 0.0022 | - | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.2847 | - | 0.3206 |
| `qr/n128/b1` | 0.9617 | - | 0.8648 |
| `qr/n128/b128` | 125.1920 | - | 113.6311 |
| `qr/n32/b1` | 0.0426 | - | 0.0288 |
| `qr/n32/b128` | 5.4421 | - | 3.6353 |
| `rank_revealing_qr/n128/b1` | 0.9997 | - | 0.9881 |
| `rank_revealing_qr/n128/b128` | 130.1939 | - | 131.6621 |
| `rank_revealing_qr/n32/b1` | 0.0396 | - | 0.0365 |
| `rank_revealing_qr/n32/b128` | 5.0351 | - | 4.8320 |
| `solve/n128/b1` | 0.1805 | - | 0.2289 |
| `solve/n128/b128` | 23.8363 | - | 29.4193 |
| `solve/n32/b1` | 0.0084 | - | 0.0095 |
| `solve/n32/b128` | 0.9895 | - | 1.1710 |
| `svd_thin/n128/b1` | 3.9196 | - | 3.4977 |
| `svd_thin/n128/b128` | 506.7365 | - | 453.3497 |
| `svd_thin/n32/b1` | 0.1512 | - | 0.1678 |
| `svd_thin/n32/b128` | 19.7805 | - | 22.1902 |
| `svd_values/n128/b1` | 1.8835 | - | 1.3900 |
| `svd_values/n128/b128` | 244.5816 | - | 182.2489 |
| `svd_values/n32/b1` | 0.1007 | - | 0.0638 |
| `svd_values/n32/b128` | 13.3372 | - | 8.2219 |
| `triangular_solve/n128/b1` | 0.0110 | - | 0.0144 |
| `triangular_solve/n128/b128` | 2.1807 | - | 2.9671 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0014 |
| `triangular_solve/n32/b128` | 0.1890 | - | 0.1573 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1083 | 0.1087 | 0.0788 |
| `cholesky/n128/b128` | 15.9892 | 15.6503 | 11.1521 |
| `cholesky/n32/b1` | 0.0033 | 0.0063 | 0.0034 |
| `cholesky/n32/b128` | 0.4251 | 0.2185 | 0.4379 |
| `eigh/n128/b1` | 1.8558 | 1.5969 | 3.1683 |
| `eigh/n128/b128` | 241.3382 | 209.8366 | 408.8993 |
| `eigh/n32/b1` | 0.0813 | 0.0857 | 0.1088 |
| `eigh/n32/b128` | 10.6243 | 2.6662 | 14.0392 |
| `eigvalsh/n128/b1` | 0.9286 | 0.9613 | 0.8885 |
| `eigvalsh/n128/b128` | 121.8961 | 121.8058 | 115.6514 |
| `eigvalsh/n32/b1` | 0.0528 | 0.0568 | 0.0421 |
| `eigvalsh/n32/b128` | 6.9643 | 2.4960 | 5.4461 |
| `householder_apply/n128/b1` | 0.4864 | 0.2648 | 0.3702 |
| `householder_apply/n128/b128` | 64.3807 | 35.0631 | 50.2352 |
| `householder_apply/n32/b1` | 0.0147 | 0.0176 | 0.0197 |
| `householder_apply/n32/b128` | 1.8924 | 0.4666 | 2.5652 |
| `householder_factor/n128/b1` | 0.3519 | 0.2255 | 0.3867 |
| `householder_factor/n128/b128` | 45.6271 | 29.4074 | 50.2338 |
| `householder_factor/n32/b1` | 0.0118 | 0.0143 | 0.0157 |
| `householder_factor/n32/b128` | 1.5054 | 0.3786 | 2.0019 |
| `lu/n128/b1` | 0.1933 | 0.1871 | 0.1453 |
| `lu/n128/b128` | 27.6203 | 26.0797 | 21.9055 |
| `lu/n32/b1` | 0.0075 | 0.0105 | 0.0080 |
| `lu/n32/b128` | 1.0186 | 0.4867 | 1.1282 |
| `lu_factor/n128/b1` | 0.1566 | 0.1424 | 0.1183 |
| `lu_factor/n128/b128` | 21.8786 | 6.1863 | 15.4917 |
| `lu_factor/n32/b1` | 0.0054 | 0.0087 | 0.0063 |
| `lu_factor/n32/b128` | 0.6488 | 0.3310 | 0.8174 |
| `lu_factor_solve/n128/b1` | 0.1755 | 0.1656 | 0.1384 |
| `lu_factor_solve/n128/b128` | 24.3751 | 6.5648 | 18.0693 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0109 | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9299 | 0.4740 | 1.1342 |
| `lu_solve_prepared/n128/b1` | 0.0190 | 0.0222 | 0.0179 |
| `lu_solve_prepared/n128/b128` | 4.2809 | 1.2265 | 4.0502 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0048 | 0.0018 |
| `lu_solve_prepared/n32/b128` | 0.2805 | 0.0757 | 0.2578 |
| `qr/n128/b1` | 0.9702 | 0.8605 | 0.7779 |
| `qr/n128/b128` | 125.2860 | 113.8379 | 101.7495 |
| `qr/n32/b1` | 0.0421 | 0.0672 | 0.0288 |
| `qr/n32/b128` | 5.4433 | 1.3637 | 3.7009 |
| `rank_revealing_qr/n128/b1` | 1.0157 | 0.8077 | 0.9055 |
| `rank_revealing_qr/n128/b128` | 130.7180 | 103.7912 | 121.6068 |
| `rank_revealing_qr/n32/b1` | 0.0395 | 0.0661 | 0.0366 |
| `rank_revealing_qr/n32/b128` | 5.0455 | 1.2573 | 4.8609 |
| `solve/n128/b1` | 0.1805 | 0.1682 | 0.1439 |
| `solve/n128/b128` | 23.8347 | 22.2206 | 19.1546 |
| `solve/n32/b1` | 0.0083 | 0.0114 | 0.0096 |
| `solve/n32/b128` | 0.9867 | 0.2510 | 1.1974 |
| `svd_thin/n128/b1` | 3.9279 | 2.7045 | 3.0287 |
| `svd_thin/n128/b128` | 506.0797 | 349.0014 | 390.5106 |
| `svd_thin/n32/b1` | 0.1624 | 0.1552 | 0.1682 |
| `svd_thin/n32/b128` | 19.7874 | 4.9393 | 22.1364 |
| `svd_values/n128/b1` | 1.8828 | 1.9081 | 1.5035 |
| `svd_values/n128/b128` | 244.5913 | 243.4111 | 193.5736 |
| `svd_values/n32/b1` | 0.1009 | 0.1059 | 0.0634 |
| `svd_values/n32/b128` | 13.2954 | 3.9346 | 8.2321 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0138 | 0.0090 |
| `triangular_solve/n128/b128` | 2.3260 | 2.2742 | 2.5919 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0032 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1912 | 0.0973 | 0.1722 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1066 | 0.1141 | 0.0945 |
| `cholesky/n128/b128` | 15.9402 | 16.5168 | 13.8049 |
| `cholesky/n32/b1` | 0.0033 | 0.0067 | 0.0034 |
| `cholesky/n32/b128` | 0.4247 | 0.0583 | 0.4402 |
| `eigh/n128/b1` | 1.8480 | 1.6268 | 3.1563 |
| `eigh/n128/b128` | 241.1846 | 213.0512 | 406.7762 |
| `eigh/n32/b1` | 0.0807 | 0.0843 | 0.1082 |
| `eigh/n32/b128` | 10.5722 | 2.6834 | 13.9849 |
| `eigvalsh/n128/b1` | 0.9284 | 0.9318 | 0.8875 |
| `eigvalsh/n128/b128` | 121.8506 | 121.2826 | 115.6060 |
| `eigvalsh/n32/b1` | 0.0529 | 0.0563 | 0.0422 |
| `eigvalsh/n32/b128` | 7.0321 | 0.9171 | 5.4788 |
| `householder_apply/n128/b1` | 0.4860 | 0.3292 | 0.3238 |
| `householder_apply/n128/b128` | 64.4789 | 43.6675 | 44.6791 |
| `householder_apply/n32/b1` | 0.0147 | 0.0176 | 0.0199 |
| `householder_apply/n32/b128` | 1.8541 | 0.4673 | 2.5099 |
| `householder_factor/n128/b1` | 0.3504 | 0.2848 | 0.3826 |
| `householder_factor/n128/b128` | 45.6963 | 36.7941 | 50.1032 |
| `householder_factor/n32/b1` | 0.0114 | 0.0137 | 0.0158 |
| `householder_factor/n32/b128` | 1.4628 | 0.3746 | 2.0114 |
| `lu/n128/b1` | 0.1997 | 0.1956 | 0.1422 |
| `lu/n128/b128` | 27.7459 | 27.3247 | 21.1226 |
| `lu/n32/b1` | 0.0073 | 0.0105 | 0.0080 |
| `lu/n32/b128` | 0.9787 | 0.2322 | 1.1706 |
| `lu_factor/n128/b1` | 0.1566 | 0.1584 | 0.1139 |
| `lu_factor/n128/b128` | 21.8296 | 6.1820 | 14.6424 |
| `lu_factor/n32/b1` | 0.0054 | 0.0087 | 0.0064 |
| `lu_factor/n32/b128` | 0.6487 | 0.1721 | 0.8214 |
| `lu_factor_solve/n128/b1` | 0.1759 | 0.1760 | 0.1358 |
| `lu_factor_solve/n128/b128` | 24.3830 | 3.5712 | 17.5425 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0109 | 0.0087 |
| `lu_factor_solve/n32/b128` | 0.9301 | 0.2418 | 1.1548 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0220 | 0.0180 |
| `lu_solve_prepared/n128/b128` | 4.0343 | 0.7353 | 4.0044 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0052 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2796 | 0.0761 | 0.2566 |
| `qr/n128/b1` | 0.9729 | 1.2080 | 0.7657 |
| `qr/n128/b128` | 125.5360 | 154.3718 | 99.8532 |
| `qr/n32/b1` | 0.0425 | 0.0892 | 0.0290 |
| `qr/n32/b128` | 5.4148 | 0.6916 | 3.6739 |
| `rank_revealing_qr/n128/b1` | 1.0095 | 0.8846 | 0.8935 |
| `rank_revealing_qr/n128/b128` | 130.0470 | 113.9294 | 121.4409 |
| `rank_revealing_qr/n32/b1` | 0.0397 | 0.0873 | 0.0366 |
| `rank_revealing_qr/n32/b128` | 5.0556 | 0.6402 | 4.8446 |
| `solve/n128/b1` | 0.1801 | 0.1796 | 0.1494 |
| `solve/n128/b128` | 23.8228 | 23.6893 | 19.0769 |
| `solve/n32/b1` | 0.0083 | 0.0110 | 0.0095 |
| `solve/n32/b128` | 0.9756 | 0.2537 | 1.1771 |
| `svd_thin/n128/b1` | 3.9231 | 2.7667 | 3.0141 |
| `svd_thin/n128/b128` | 506.6976 | 358.3268 | 387.7048 |
| `svd_thin/n32/b1` | 0.1508 | 0.1547 | 0.1672 |
| `svd_thin/n32/b128` | 19.7839 | 2.4992 | 22.3102 |
| `svd_values/n128/b1` | 1.8891 | 1.9065 | 1.5633 |
| `svd_values/n128/b128` | 244.7767 | 243.4106 | 200.4838 |
| `svd_values/n32/b1` | 0.1007 | 0.1052 | 0.0636 |
| `svd_values/n32/b128` | 13.2915 | 3.4185 | 8.2464 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0138 | 0.0092 |
| `triangular_solve/n128/b128` | 2.1993 | 2.2899 | 2.5693 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0051 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1909 | 0.0353 | 0.1733 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1949 | - | 0.2324 |
| `cholesky/n256/b4` | 0.8006 | - | 0.9369 |
| `cholesky/n512/b1` | 1.2593 | - | 1.5869 |
| `cholesky/n512/b4` | 5.5385 | - | 6.6200 |
| `eigh/n256/b1` | 5.6266 | - | 5.4411 |
| `eigh/n256/b4` | 22.6052 | - | 21.6343 |
| `eigh/n512/b1` | 28.6055 | - | 30.3979 |
| `eigh/n512/b4` | 114.6925 | - | 122.2494 |
| `eigvalsh/n256/b1` | 2.9452 | - | 2.4945 |
| `eigvalsh/n256/b4` | 11.8631 | - | 9.9170 |
| `eigvalsh/n512/b1` | 14.0172 | - | 14.3246 |
| `eigvalsh/n512/b4` | 56.9503 | - | 57.1790 |
| `householder_apply/n256/b1` | 0.8243 | - | 1.6372 |
| `householder_apply/n256/b4` | 3.3205 | - | 6.6921 |
| `householder_apply/n512/b1` | 6.1824 | - | 11.8671 |
| `householder_apply/n512/b4` | 25.0434 | - | 47.3025 |
| `householder_factor/n256/b1` | 0.6226 | - | 1.0951 |
| `householder_factor/n256/b4` | 2.4867 | - | 4.4025 |
| `householder_factor/n512/b1` | 4.3314 | - | 7.4256 |
| `householder_factor/n512/b4` | 17.5397 | - | 29.9046 |
| `lu/n256/b1` | 0.4817 | - | 0.4849 |
| `lu/n256/b4` | 1.9894 | - | 2.0810 |
| `lu/n512/b1` | 3.2247 | - | 3.2133 |
| `lu/n512/b4` | 12.8999 | - | 13.1419 |
| `lu_factor/n256/b1` | 0.3550 | - | 0.4453 |
| `lu_factor/n256/b4` | 1.5250 | - | 1.7786 |
| `lu_factor/n512/b1` | 2.8222 | - | 2.8775 |
| `lu_factor/n512/b4` | 11.7892 | - | 11.7956 |
| `lu_factor_solve/n256/b1` | 0.3717 | - | 0.4862 |
| `lu_factor_solve/n256/b4` | 1.4892 | - | 1.9416 |
| `lu_factor_solve/n512/b1` | 2.8833 | - | 3.0302 |
| `lu_factor_solve/n512/b4` | 12.0248 | - | 12.3804 |
| `lu_solve_prepared/n256/b1` | 0.0174 | - | 0.0404 |
| `lu_solve_prepared/n256/b4` | 0.0797 | - | 0.1854 |
| `lu_solve_prepared/n512/b1` | 0.0626 | - | 0.1433 |
| `lu_solve_prepared/n512/b4` | 0.4327 | - | 0.8632 |
| `qr/n256/b1` | 1.8461 | - | 2.1745 |
| `qr/n256/b4` | 7.3836 | - | 8.8099 |
| `qr/n512/b1` | 11.4704 | - | 14.8417 |
| `qr/n512/b4` | 46.0787 | - | 60.2904 |
| `rank_revealing_qr/n256/b1` | 2.1233 | - | 2.6151 |
| `rank_revealing_qr/n256/b4` | 8.3732 | - | 10.5947 |
| `rank_revealing_qr/n512/b1` | 14.6628 | - | 18.6790 |
| `rank_revealing_qr/n512/b4` | 58.7384 | - | 75.6442 |
| `solve/n256/b1` | 0.3893 | - | 0.4941 |
| `solve/n256/b4` | 1.5575 | - | 1.9987 |
| `solve/n512/b1` | 2.8575 | - | 3.0751 |
| `solve/n512/b4` | 11.3669 | - | 12.3966 |
| `svd_thin/n256/b1` | 12.2159 | - | 10.9647 |
| `svd_thin/n256/b4` | 48.9303 | - | 44.2039 |
| `svd_thin/n512/b1` | 70.7503 | - | 72.4809 |
| `svd_thin/n512/b4` | 283.5542 | - | 291.4244 |
| `svd_values/n256/b1` | 6.9540 | - | 4.5872 |
| `svd_values/n256/b4` | 27.7418 | - | 18.6168 |
| `svd_values/n512/b1` | 38.6245 | - | 30.9694 |
| `svd_values/n512/b4` | 153.7554 | - | 127.6224 |
| `triangular_solve/n256/b1` | 0.0105 | - | 0.0201 |
| `triangular_solve/n256/b4` | 0.0436 | - | 0.0839 |
| `triangular_solve/n512/b1` | 0.0345 | - | 0.0740 |
| `triangular_solve/n512/b4` | 0.1363 | - | 0.3016 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1967 | 0.1784 | 0.1570 |
| `cholesky/n256/b4` | 0.7936 | 0.7487 | 0.6408 |
| `cholesky/n512/b1` | 1.2811 | 0.8013 | 0.7605 |
| `cholesky/n512/b4` | 5.5738 | 3.5902 | 3.3815 |
| `eigh/n256/b1` | 5.5683 | 4.1939 | 3.6002 |
| `eigh/n256/b4` | 22.3650 | 16.9510 | 14.3645 |
| `eigh/n512/b1` | 28.7396 | 15.7135 | 16.4258 |
| `eigh/n512/b4` | 116.9320 | 63.8478 | 65.7973 |
| `eigvalsh/n256/b1` | 2.9090 | 2.9631 | 1.9255 |
| `eigvalsh/n256/b4` | 11.9356 | 11.9273 | 7.6500 |
| `eigvalsh/n512/b1` | 14.1423 | 11.9138 | 7.5143 |
| `eigvalsh/n512/b4` | 56.0975 | 47.8846 | 30.3947 |
| `householder_apply/n256/b1` | 0.8205 | 0.3240 | 1.0975 |
| `householder_apply/n256/b4` | 3.3271 | 1.3275 | 4.5154 |
| `householder_apply/n512/b1` | 6.1515 | 1.8217 | 6.9445 |
| `householder_apply/n512/b4` | 24.9332 | 7.5970 | 28.0642 |
| `householder_factor/n256/b1` | 0.6166 | 0.3456 | 0.8498 |
| `householder_factor/n256/b4` | 2.4863 | 1.3765 | 3.4435 |
| `householder_factor/n512/b1` | 4.3311 | 1.6489 | 4.4911 |
| `householder_factor/n512/b4` | 17.5228 | 6.7021 | 18.2584 |
| `lu/n256/b1` | 0.4663 | 0.4435 | 0.2854 |
| `lu/n256/b4` | 1.9419 | 1.8569 | 1.2916 |
| `lu/n512/b1` | 3.2073 | 1.9886 | 1.6777 |
| `lu/n512/b4` | 12.7470 | 7.5749 | 6.9923 |
| `lu_factor/n256/b1` | 0.3539 | 0.3120 | 0.2387 |
| `lu_factor/n256/b4` | 1.5202 | 0.7736 | 0.9644 |
| `lu_factor/n512/b1` | 2.8263 | 1.4762 | 1.3603 |
| `lu_factor/n512/b4` | 11.7464 | 6.0321 | 5.5671 |
| `lu_factor_solve/n256/b1` | 0.3685 | 0.3289 | 0.2678 |
| `lu_factor_solve/n256/b4` | 1.5006 | 0.7602 | 1.0968 |
| `lu_factor_solve/n512/b1` | 2.8829 | 1.5325 | 1.4784 |
| `lu_factor_solve/n512/b4` | 12.1126 | 3.5104 | 6.1153 |
| `lu_solve_prepared/n256/b1` | 0.0171 | 0.0238 | 0.0254 |
| `lu_solve_prepared/n256/b4` | 0.0800 | 0.0224 | 0.1265 |
| `lu_solve_prepared/n512/b1` | 0.0725 | 0.0654 | 0.0978 |
| `lu_solve_prepared/n512/b4` | 0.4442 | 0.2041 | 0.8591 |
| `qr/n256/b1` | 1.8513 | 1.8013 | 1.6706 |
| `qr/n256/b4` | 7.3705 | 7.1384 | 6.7566 |
| `qr/n512/b1` | 11.6232 | 6.0609 | 9.0042 |
| `qr/n512/b4` | 46.1704 | 23.8530 | 36.7093 |
| `rank_revealing_qr/n256/b1` | 2.1053 | 1.5036 | 2.3199 |
| `rank_revealing_qr/n256/b4` | 8.4672 | 6.0047 | 9.3335 |
| `rank_revealing_qr/n512/b1` | 14.6553 | 6.3098 | 14.6948 |
| `rank_revealing_qr/n512/b4` | 59.0754 | 25.1610 | 58.8735 |
| `solve/n256/b1` | 0.3895 | 0.3688 | 0.2849 |
| `solve/n256/b4` | 1.5588 | 1.4309 | 1.1553 |
| `solve/n512/b1` | 2.8591 | 1.5979 | 1.5340 |
| `solve/n512/b4` | 11.3479 | 6.2981 | 6.1821 |
| `svd_thin/n256/b1` | 12.2373 | 8.7751 | 9.3076 |
| `svd_thin/n256/b4` | 48.8237 | 36.0834 | 37.3489 |
| `svd_thin/n512/b1` | 71.1333 | 40.0879 | 54.7465 |
| `svd_thin/n512/b4` | 283.0893 | 159.6617 | 221.8875 |
| `svd_values/n256/b1` | 6.9580 | 7.1087 | 4.4205 |
| `svd_values/n256/b4` | 27.6806 | 28.0262 | 17.9436 |
| `svd_values/n512/b1` | 38.6676 | 31.6907 | 28.6120 |
| `svd_values/n512/b4` | 154.8235 | 126.5195 | 117.4154 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0154 | 0.0127 |
| `triangular_solve/n256/b4` | 0.0458 | 0.0555 | 0.0614 |
| `triangular_solve/n512/b1` | 0.0348 | 0.0353 | 0.0508 |
| `triangular_solve/n512/b4` | 0.1602 | 0.1515 | 0.2731 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.2003 | 0.2126 | 0.1575 |
| `cholesky/n256/b4` | 0.8177 | 0.8369 | 0.6390 |
| `cholesky/n512/b1` | 1.2854 | 0.7266 | 0.6859 |
| `cholesky/n512/b4` | 5.6483 | 3.2598 | 3.0774 |
| `eigh/n256/b1` | 5.6154 | 4.1569 | 3.3090 |
| `eigh/n256/b4` | 22.6768 | 16.6064 | 13.4544 |
| `eigh/n512/b1` | 28.6157 | 14.3592 | 14.1074 |
| `eigh/n512/b4` | 115.0703 | 59.4982 | 56.0564 |
| `eigvalsh/n256/b1` | 2.9749 | 2.9299 | 1.8695 |
| `eigvalsh/n256/b4` | 11.8920 | 11.7875 | 7.4753 |
| `eigvalsh/n512/b1` | 14.0513 | 11.4499 | 6.7438 |
| `eigvalsh/n512/b4` | 56.6168 | 46.5520 | 27.0895 |
| `householder_apply/n256/b1` | 0.8276 | 0.4122 | 1.0548 |
| `householder_apply/n256/b4` | 3.3110 | 1.7069 | 4.2582 |
| `householder_apply/n512/b1` | 6.1543 | 1.8654 | 5.9209 |
| `householder_apply/n512/b4` | 24.9818 | 7.8525 | 24.4187 |
| `householder_factor/n256/b1` | 0.6244 | 0.4276 | 0.8357 |
| `householder_factor/n256/b4` | 2.4626 | 1.6978 | 3.3000 |
| `householder_factor/n512/b1` | 4.3320 | 1.7474 | 4.0654 |
| `householder_factor/n512/b4` | 17.4705 | 7.1500 | 16.2984 |
| `lu/n256/b1` | 0.4832 | 0.4595 | 0.2500 |
| `lu/n256/b4` | 1.9416 | 1.9771 | 1.1036 |
| `lu/n512/b1` | 3.1867 | 2.0018 | 1.1520 |
| `lu/n512/b4` | 12.7210 | 8.1925 | 4.8465 |
| `lu_factor/n256/b1` | 0.3788 | 0.3624 | 0.2045 |
| `lu_factor/n256/b4` | 1.5192 | 1.4483 | 0.8252 |
| `lu_factor/n512/b1` | 2.8373 | 1.5344 | 0.8486 |
| `lu_factor/n512/b4` | 11.7418 | 6.3691 | 3.4434 |
| `lu_factor_solve/n256/b1` | 0.4008 | 0.3943 | 0.2373 |
| `lu_factor_solve/n256/b4` | 1.4838 | 1.5020 | 0.9479 |
| `lu_factor_solve/n512/b1` | 2.9046 | 1.6170 | 0.9784 |
| `lu_factor_solve/n512/b4` | 11.9888 | 6.5715 | 3.9502 |
| `lu_solve_prepared/n256/b1` | 0.0176 | 0.0291 | 0.0276 |
| `lu_solve_prepared/n256/b4` | 0.0748 | 0.1079 | 0.1174 |
| `lu_solve_prepared/n512/b1` | 0.0726 | 0.0760 | 0.1091 |
| `lu_solve_prepared/n512/b4` | 0.3767 | 0.3916 | 0.7805 |
| `qr/n256/b1` | 1.8486 | 2.4640 | 1.6786 |
| `qr/n256/b4` | 7.4031 | 9.4772 | 6.6951 |
| `qr/n512/b1` | 11.5253 | 7.0710 | 8.1433 |
| `qr/n512/b4` | 45.9919 | 28.0591 | 32.9499 |
| `rank_revealing_qr/n256/b1` | 2.1177 | 1.5716 | 2.2869 |
| `rank_revealing_qr/n256/b4` | 8.3949 | 6.2257 | 9.1799 |
| `rank_revealing_qr/n512/b1` | 14.8629 | 5.7502 | 13.9443 |
| `rank_revealing_qr/n512/b4` | 59.2822 | 23.6822 | 57.1400 |
| `solve/n256/b1` | 0.3903 | 0.4071 | 0.2520 |
| `solve/n256/b4` | 1.5537 | 1.6346 | 1.0069 |
| `solve/n512/b1` | 2.8491 | 1.6827 | 1.0375 |
| `solve/n512/b4` | 11.3829 | 6.7039 | 4.1827 |
| `svd_thin/n256/b1` | 12.2932 | 8.9131 | 9.2235 |
| `svd_thin/n256/b4` | 48.8995 | 35.9310 | 37.0032 |
| `svd_thin/n512/b1` | 71.1811 | 37.5665 | 52.5909 |
| `svd_thin/n512/b4` | 283.1852 | 151.8514 | 213.7099 |
| `svd_values/n256/b1` | 6.9414 | 7.2022 | 4.4633 |
| `svd_values/n256/b4` | 27.8108 | 28.7431 | 18.0775 |
| `svd_values/n512/b1` | 38.7387 | 32.1601 | 28.2980 |
| `svd_values/n512/b4` | 153.6350 | 128.1944 | 116.6659 |
| `triangular_solve/n256/b1` | 0.0106 | 0.0186 | 0.0126 |
| `triangular_solve/n256/b4` | 0.0468 | 0.0673 | 0.0626 |
| `triangular_solve/n512/b1` | 0.0358 | 0.0436 | 0.0541 |
| `triangular_solve/n512/b4` | 0.1780 | 0.1904 | 0.3343 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7047 | - | 0.7661 |
| `cholesky/n256/b4` | 2.7892 | - | 3.0728 |
| `cholesky/n512/b1` | 4.7507 | - | 5.4589 |
| `cholesky/n512/b4` | 19.6584 | - | 22.6187 |
| `eigh/n256/b1` | 10.2519 | - | 21.4612 |
| `eigh/n256/b4` | 41.3606 | - | 86.1148 |
| `eigh/n512/b1` | 63.0994 | - | 157.3325 |
| `eigh/n512/b4` | 252.6574 | - | 630.3860 |
| `eigvalsh/n256/b1` | 5.0001 | - | 5.6739 |
| `eigvalsh/n256/b4` | 19.8998 | - | 22.6994 |
| `eigvalsh/n512/b1` | 29.5691 | - | 37.4611 |
| `eigvalsh/n512/b4` | 118.5060 | - | 150.3320 |
| `householder_apply/n256/b1` | 3.3654 | - | 4.7320 |
| `householder_apply/n256/b4` | 13.6879 | - | 19.1412 |
| `householder_apply/n512/b1` | 24.6878 | - | 32.1766 |
| `householder_apply/n512/b4` | 97.4364 | - | 129.2244 |
| `householder_factor/n256/b1` | 2.3434 | - | 3.0017 |
| `householder_factor/n256/b4` | 9.3870 | - | 12.0665 |
| `householder_factor/n512/b1` | 16.7515 | - | 20.8092 |
| `householder_factor/n512/b4` | 67.4323 | - | 83.8667 |
| `lu/n256/b1` | 1.2529 | - | 1.4288 |
| `lu/n256/b4` | 5.1174 | - | 6.0387 |
| `lu/n512/b1` | 8.6624 | - | 10.2859 |
| `lu/n512/b4` | 34.7795 | - | 41.2792 |
| `lu_factor/n256/b1` | 1.1174 | - | 1.3357 |
| `lu_factor/n256/b4` | 4.4994 | - | 5.3403 |
| `lu_factor/n512/b1` | 7.9944 | - | 9.5271 |
| `lu_factor/n512/b4` | 32.6531 | - | 38.1826 |
| `lu_factor_solve/n256/b1` | 1.1832 | - | 1.4692 |
| `lu_factor_solve/n256/b4` | 4.7556 | - | 5.7923 |
| `lu_factor_solve/n512/b1` | 8.2387 | - | 10.0088 |
| `lu_factor_solve/n512/b4` | 33.6566 | - | 39.9982 |
| `lu_solve_prepared/n256/b1` | 0.0633 | - | 0.1353 |
| `lu_solve_prepared/n256/b4` | 0.2642 | - | 0.4447 |
| `lu_solve_prepared/n512/b1` | 0.2081 | - | 0.5019 |
| `lu_solve_prepared/n512/b4` | 1.3050 | - | 2.1294 |
| `qr/n256/b1` | 6.2352 | - | 6.0295 |
| `qr/n256/b4` | 24.8435 | - | 24.1029 |
| `qr/n512/b1` | 42.3555 | - | 41.6835 |
| `qr/n512/b4` | 169.6323 | - | 168.4741 |
| `rank_revealing_qr/n256/b1` | 6.7852 | - | 6.4385 |
| `rank_revealing_qr/n256/b4` | 26.9801 | - | 25.9704 |
| `rank_revealing_qr/n512/b1` | 47.5291 | - | 45.1744 |
| `rank_revealing_qr/n512/b4` | 191.7536 | - | 180.1919 |
| `solve/n256/b1` | 1.1703 | - | 1.5038 |
| `solve/n256/b4` | 4.6933 | - | 6.0592 |
| `solve/n512/b1` | 8.2233 | - | 10.0293 |
| `solve/n512/b4` | 32.8305 | - | 40.6141 |
| `svd_thin/n256/b1` | 24.1932 | - | 22.5568 |
| `svd_thin/n256/b4` | 96.9529 | - | 90.4345 |
| `svd_thin/n512/b1` | 152.4960 | - | 143.9974 |
| `svd_thin/n512/b4` | 610.7613 | - | 573.8650 |
| `svd_values/n256/b1` | 11.0142 | - | 9.7127 |
| `svd_values/n256/b4` | 44.1958 | - | 38.8827 |
| `svd_values/n512/b1` | 65.8992 | - | 59.0331 |
| `svd_values/n512/b4` | 264.2565 | - | 239.1813 |
| `triangular_solve/n256/b1` | 0.0339 | - | 0.0664 |
| `triangular_solve/n256/b4` | 0.1369 | - | 0.2594 |
| `triangular_solve/n512/b1` | 0.1118 | - | 0.2209 |
| `triangular_solve/n512/b4` | 0.5073 | - | 0.8639 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7050 | 0.4957 | 0.3680 |
| `cholesky/n256/b4` | 2.7773 | 1.9663 | 1.3780 |
| `cholesky/n512/b1` | 4.7660 | 2.3990 | 2.1019 |
| `cholesky/n512/b4` | 19.6599 | 10.3910 | 9.3520 |
| `eigh/n256/b1` | 10.2357 | 7.9425 | 19.4916 |
| `eigh/n256/b4` | 41.2452 | 31.9690 | 78.1581 |
| `eigh/n512/b1` | 62.9481 | 28.6854 | 128.1609 |
| `eigh/n512/b4` | 252.5346 | 115.7911 | 512.2233 |
| `eigvalsh/n256/b1` | 4.9900 | 5.0037 | 4.8920 |
| `eigvalsh/n256/b4` | 19.8071 | 19.8479 | 19.6911 |
| `eigvalsh/n512/b1` | 29.5972 | 19.5095 | 20.4381 |
| `eigvalsh/n512/b4` | 118.9127 | 79.8398 | 81.8296 |
| `householder_apply/n256/b1` | 3.3712 | 1.0445 | 2.2334 |
| `householder_apply/n256/b4` | 13.6923 | 4.3294 | 9.2212 |
| `householder_apply/n512/b1` | 24.6920 | 6.7450 | 12.3772 |
| `householder_apply/n512/b4` | 97.2414 | 26.8220 | 49.3849 |
| `householder_factor/n256/b1` | 2.3316 | 0.9593 | 1.7068 |
| `householder_factor/n256/b4` | 9.4085 | 3.8746 | 6.8872 |
| `householder_factor/n512/b1` | 16.7979 | 5.4185 | 8.5030 |
| `householder_factor/n512/b4` | 67.6475 | 21.9437 | 34.5109 |
| `lu/n256/b1` | 1.2478 | 0.8299 | 0.7924 |
| `lu/n256/b4` | 5.1930 | 3.3419 | 3.3034 |
| `lu/n512/b1` | 8.6887 | 3.8660 | 3.7101 |
| `lu/n512/b4` | 34.5312 | 15.2425 | 14.9391 |
| `lu_factor/n256/b1` | 1.1100 | 0.6687 | 0.6643 |
| `lu_factor/n256/b4` | 4.5315 | 1.1741 | 2.6631 |
| `lu_factor/n512/b1` | 8.0001 | 3.0847 | 3.0031 |
| `lu_factor/n512/b4` | 32.7221 | 8.8558 | 12.0463 |
| `lu_factor_solve/n256/b1` | 1.1716 | 0.7292 | 0.7474 |
| `lu_factor_solve/n256/b4` | 4.8038 | 1.2226 | 2.9991 |
| `lu_factor_solve/n512/b1` | 8.2156 | 3.3152 | 3.3760 |
| `lu_factor_solve/n512/b4` | 33.6851 | 9.5448 | 13.5241 |
| `lu_solve_prepared/n256/b1` | 0.0626 | 0.0596 | 0.0927 |
| `lu_solve_prepared/n256/b4` | 0.2656 | 0.0771 | 0.3230 |
| `lu_solve_prepared/n512/b1` | 0.2109 | 0.1613 | 0.3603 |
| `lu_solve_prepared/n512/b4` | 1.3253 | 0.4445 | 1.7399 |
| `qr/n256/b1` | 6.2393 | 3.1018 | 3.4490 |
| `qr/n256/b4` | 24.8897 | 12.3677 | 13.8614 |
| `qr/n512/b1` | 42.2431 | 14.5896 | 17.4509 |
| `qr/n512/b4` | 169.3724 | 58.3591 | 69.8164 |
| `rank_revealing_qr/n256/b1` | 6.7444 | 3.7839 | 3.8633 |
| `rank_revealing_qr/n256/b4` | 26.9136 | 15.9684 | 15.8431 |
| `rank_revealing_qr/n512/b1` | 47.8040 | 16.4294 | 19.0522 |
| `rank_revealing_qr/n512/b4` | 191.6552 | 66.9550 | 76.2392 |
| `solve/n256/b1` | 1.1718 | 0.7513 | 0.8235 |
| `solve/n256/b4` | 4.7001 | 3.0131 | 3.2267 |
| `solve/n512/b1` | 8.2426 | 3.3835 | 3.4301 |
| `solve/n512/b4` | 32.8798 | 13.4235 | 14.1607 |
| `svd_thin/n256/b1` | 23.9870 | 14.7504 | 14.4251 |
| `svd_thin/n256/b4` | 96.6996 | 61.1015 | 58.1069 |
| `svd_thin/n512/b1` | 152.6103 | 67.3659 | 72.0739 |
| `svd_thin/n512/b4` | 609.9496 | 267.4937 | 289.1946 |
| `svd_values/n256/b1` | 11.1065 | 10.6401 | 7.2411 |
| `svd_values/n256/b4` | 44.1098 | 43.3281 | 29.0488 |
| `svd_values/n512/b1` | 66.4792 | 41.7800 | 32.4640 |
| `svd_values/n512/b4` | 266.8747 | 167.5939 | 129.5591 |
| `triangular_solve/n256/b1` | 0.0343 | 0.0347 | 0.0481 |
| `triangular_solve/n256/b4` | 0.1516 | 0.1370 | 0.2174 |
| `triangular_solve/n512/b1` | 0.1129 | 0.0842 | 0.1490 |
| `triangular_solve/n512/b4` | 0.5457 | 0.3691 | 0.7957 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7002 | 0.4744 | 0.3399 |
| `cholesky/n256/b4` | 2.8435 | 2.0086 | 1.3281 |
| `cholesky/n512/b1` | 4.7856 | 1.8780 | 1.4538 |
| `cholesky/n512/b4` | 19.7090 | 7.9007 | 6.5200 |
| `eigh/n256/b1` | 10.2131 | 6.9133 | 19.3219 |
| `eigh/n256/b4` | 41.2606 | 28.0231 | 77.2132 |
| `eigh/n512/b1` | 62.9875 | 24.2411 | 123.4431 |
| `eigh/n512/b4` | 251.8994 | 96.9840 | 496.3585 |
| `eigvalsh/n256/b1` | 4.9575 | 5.0009 | 4.8152 |
| `eigvalsh/n256/b4` | 19.8334 | 19.8666 | 19.2964 |
| `eigvalsh/n512/b1` | 29.3608 | 17.9142 | 17.9182 |
| `eigvalsh/n512/b4` | 118.1847 | 71.6339 | 72.0858 |
| `householder_apply/n256/b1` | 3.3267 | 0.9137 | 1.7845 |
| `householder_apply/n256/b4` | 13.5406 | 3.7608 | 7.1911 |
| `householder_apply/n512/b1` | 24.6351 | 4.5165 | 8.5549 |
| `householder_apply/n512/b4` | 99.0183 | 18.4184 | 35.4579 |
| `householder_factor/n256/b1` | 2.3370 | 0.9850 | 1.5332 |
| `householder_factor/n256/b4` | 9.1711 | 3.8714 | 6.0619 |
| `householder_factor/n512/b1` | 16.7356 | 4.4908 | 6.4905 |
| `householder_factor/n512/b4` | 67.2157 | 18.1179 | 26.1533 |
| `lu/n256/b1` | 1.2600 | 0.8174 | 0.5495 |
| `lu/n256/b4` | 5.0670 | 3.3921 | 2.4668 |
| `lu/n512/b1` | 8.6747 | 3.2839 | 2.2962 |
| `lu/n512/b4` | 34.6335 | 13.1394 | 9.2294 |
| `lu_factor/n256/b1` | 1.1085 | 0.6654 | 0.4563 |
| `lu_factor/n256/b4` | 4.3529 | 2.5886 | 1.7757 |
| `lu_factor/n512/b1` | 8.0154 | 2.6166 | 1.6518 |
| `lu_factor/n512/b4` | 32.7196 | 10.5360 | 6.6227 |
| `lu_factor_solve/n256/b1` | 1.1730 | 0.7336 | 0.5506 |
| `lu_factor_solve/n256/b4` | 4.5966 | 2.8317 | 2.0631 |
| `lu_factor_solve/n512/b1` | 8.2497 | 2.7764 | 2.0019 |
| `lu_factor_solve/n512/b4` | 33.6626 | 11.1522 | 8.0570 |
| `lu_solve_prepared/n256/b1` | 0.0624 | 0.0675 | 0.1021 |
| `lu_solve_prepared/n256/b4` | 0.2602 | 0.2712 | 0.3137 |
| `lu_solve_prepared/n512/b1` | 0.2218 | 0.1691 | 0.3423 |
| `lu_solve_prepared/n512/b4` | 1.0888 | 0.9134 | 1.5858 |
| `qr/n256/b1` | 6.2319 | 3.5475 | 3.0817 |
| `qr/n256/b4` | 24.9287 | 14.0816 | 12.3683 |
| `qr/n512/b1` | 42.4579 | 12.5524 | 13.2428 |
| `qr/n512/b4` | 169.6791 | 49.8879 | 53.4148 |
| `rank_revealing_qr/n256/b1` | 6.7238 | 3.9802 | 3.5119 |
| `rank_revealing_qr/n256/b4` | 26.9506 | 15.3622 | 14.3220 |
| `rank_revealing_qr/n512/b1` | 47.5230 | 12.8428 | 14.9505 |
| `rank_revealing_qr/n512/b4` | 191.0948 | 48.2934 | 60.4900 |
| `solve/n256/b1` | 1.1711 | 0.7520 | 0.5815 |
| `solve/n256/b4` | 4.6838 | 3.0373 | 2.3761 |
| `solve/n512/b1` | 8.2251 | 2.9012 | 2.1317 |
| `solve/n512/b4` | 32.8486 | 11.5133 | 8.6905 |
| `svd_thin/n256/b1` | 24.0029 | 14.3207 | 13.2701 |
| `svd_thin/n256/b4` | 95.9926 | 58.6697 | 53.5723 |
| `svd_thin/n512/b1` | 152.3657 | 55.2564 | 60.7367 |
| `svd_thin/n512/b4` | 608.8592 | 221.5816 | 243.4445 |
| `svd_values/n256/b1` | 11.0674 | 10.9343 | 7.1303 |
| `svd_values/n256/b4` | 44.2401 | 43.1960 | 28.6043 |
| `svd_values/n512/b1` | 66.4038 | 39.6052 | 28.5561 |
| `svd_values/n512/b4` | 266.9223 | 159.2758 | 115.2370 |
| `triangular_solve/n256/b1` | 0.0337 | 0.0373 | 0.0425 |
| `triangular_solve/n256/b4` | 0.1390 | 0.1474 | 0.1719 |
| `triangular_solve/n512/b1` | 0.1143 | 0.0903 | 0.1547 |
| `triangular_solve/n512/b4` | 0.5810 | 0.4223 | 0.8141 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3224 | - | 0.5496 |
| `householder_factor/4096x256/b1` | 14.0966 | - | 23.4441 |
| `qr/1024x64/b1` | 0.9811 | - | 1.0739 |
| `qr/4096x256/b1` | 41.4086 | - | 46.3463 |
| `rank_revealing_qr/1024x64/b1` | 0.9721 | - | 1.1656 |
| `rank_revealing_qr/4096x256/b1` | 64.2270 | - | 57.3155 |
| `svd_thin/1024x64/b1` | 1.4622 | - | 1.9700 |
| `svd_thin/4096x256/b1` | 72.5927 | - | 74.1608 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3285 | 0.3038 | 0.5907 |
| `householder_factor/4096x256/b1` | 14.1882 | 6.5716 | 12.5578 |
| `qr/1024x64/b1` | 0.9837 | 0.8917 | 1.1269 |
| `qr/4096x256/b1` | 41.1816 | 20.7148 | 24.3055 |
| `rank_revealing_qr/1024x64/b1` | 0.9737 | 0.7824 | 1.2279 |
| `rank_revealing_qr/4096x256/b1` | 63.7458 | 24.0214 | 28.0289 |
| `svd_thin/1024x64/b1` | 1.4458 | 1.3937 | 1.8975 |
| `svd_thin/4096x256/b1` | 72.5116 | 41.2841 | 41.6361 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3286 | 0.3519 | 0.6004 |
| `householder_factor/4096x256/b1` | 14.2888 | 5.6328 | 10.9506 |
| `qr/1024x64/b1` | 0.9832 | 1.1440 | 1.1535 |
| `qr/4096x256/b1` | 41.4710 | 18.4276 | 22.0209 |
| `rank_revealing_qr/1024x64/b1` | 0.9654 | 0.7741 | 1.2595 |
| `rank_revealing_qr/4096x256/b1` | 64.2865 | 18.6124 | 24.0136 |
| `svd_thin/1024x64/b1` | 1.4503 | 1.6148 | 1.8936 |
| `svd_thin/4096x256/b1` | 73.0402 | 34.3789 | 37.3921 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0242 | - | 1.0645 |
| `householder_factor/4096x256/b1` | 55.6358 | - | 69.1016 |
| `qr/1024x64/b1` | 2.8568 | - | 2.0639 |
| `qr/4096x256/b1` | 146.8516 | - | 139.3757 |
| `rank_revealing_qr/1024x64/b1` | 2.8864 | - | 2.2518 |
| `rank_revealing_qr/4096x256/b1` | 246.0679 | - | 172.1013 |
| `svd_thin/1024x64/b1` | 3.5495 | - | 3.9611 |
| `svd_thin/4096x256/b1` | 231.6524 | - | 218.1904 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0424 | 0.6631 | 0.4351 |
| `householder_factor/4096x256/b1` | 54.4095 | 20.5265 | 19.9120 |
| `qr/1024x64/b1` | 2.8576 | 1.6315 | 0.8083 |
| `qr/4096x256/b1` | 146.9561 | 57.3102 | 40.4947 |
| `rank_revealing_qr/1024x64/b1` | 2.8571 | 1.8004 | 1.0334 |
| `rank_revealing_qr/4096x256/b1` | 247.5636 | 83.9954 | 54.7181 |
| `svd_thin/1024x64/b1` | 3.5481 | 2.3346 | 2.0874 |
| `svd_thin/4096x256/b1` | 232.3126 | 104.5447 | 75.3653 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0427 | 0.6658 | 0.3450 |
| `householder_factor/4096x256/b1` | 55.4778 | 16.0465 | 12.4951 |
| `qr/1024x64/b1` | 2.8721 | 1.7292 | 0.6288 |
| `qr/4096x256/b1` | 147.0104 | 42.7564 | 25.5730 |
| `rank_revealing_qr/1024x64/b1` | 2.8725 | 1.6864 | 0.8586 |
| `rank_revealing_qr/4096x256/b1` | 244.5488 | 52.0630 | 34.1095 |
| `svd_thin/1024x64/b1` | 3.5904 | 2.3682 | 1.8545 |
| `svd_thin/4096x256/b1` | 232.3002 | 84.7652 | 54.2974 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
