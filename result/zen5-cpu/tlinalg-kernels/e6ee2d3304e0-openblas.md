<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261013T071911Z/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `e6ee2d3304e042926c77cda7b81e58c871a98919`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.24.4 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8); `t4a-faer-traits` 0.24.0 @ `67c642111e2a11fccbb581403a8d88e8ab6f94c8` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=67c642111e2a11fccbb581403a8d88e8ab6f94c8#67c642111e2a11fccbb581403a8d88e8ab6f94c8)
- harness commit: `3e6ac30e0a55227312b3852f8d6050e8bbcdd317`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-13T08:21:13.071941Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261013T071911Z/`

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
| `cholesky/n16/b1024` | 0.5270 | - | 0.6180 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1051 | - | 0.1147 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2160 | - | 0.2416 |
| `eig/n16/b1` | 0.0539 | - | 0.0404 |
| `eig/n16/b1024` | 56.2629 | - | 41.9206 |
| `eig/n4/b1` | 0.0040 | - | 0.0038 |
| `eig/n4/b1024` | 3.5520 | - | 3.3272 |
| `eig/n8/b1` | 0.0144 | - | 0.0112 |
| `eig/n8/b1024` | 13.8287 | - | 10.6463 |
| `eigh/n16/b1` | 0.0177 | - | 0.0230 |
| `eigh/n16/b1024` | 18.0507 | - | 24.1268 |
| `eigh/n4/b1` | 0.0016 | - | 0.0019 |
| `eigh/n4/b1024` | 1.4795 | - | 1.7922 |
| `eigh/n8/b1` | 0.0052 | - | 0.0064 |
| `eigh/n8/b1024` | 5.0940 | - | 6.4938 |
| `eigvals/n16/b1` | 0.0371 | - | 0.0292 |
| `eigvals/n16/b1024` | 39.1922 | - | 30.3286 |
| `eigvals/n4/b1` | 0.0023 | - | 0.0025 |
| `eigvals/n4/b1024` | 1.8885 | - | 2.0583 |
| `eigvals/n8/b1` | 0.0098 | - | 0.0086 |
| `eigvals/n8/b1024` | 9.1818 | - | 7.9830 |
| `eigvalsh/n16/b1` | 0.0132 | - | 0.0084 |
| `eigvalsh/n16/b1024` | 13.2245 | - | 8.7628 |
| `eigvalsh/n4/b1` | 0.0013 | - | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1799 | - | 0.8444 |
| `eigvalsh/n8/b1` | 0.0042 | - | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0495 | - | 2.7264 |
| `full_piv_lu/n16/b1` | 0.0026 | - | 0.0026 |
| `full_piv_lu/n16/b1024` | 2.0429 | - | 2.9274 |
| `full_piv_lu/n4/b1` | 0.0007 | - | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2225 | - | 0.2193 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6102 | - | 0.6108 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | - | 0.0038 |
| `full_piv_lu_solve/n16/b1024` | 2.0998 | - | 3.8137 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0006 |
| `full_piv_lu_solve/n4/b1024` | 0.3309 | - | 0.4234 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0012 |
| `full_piv_lu_solve/n8/b1024` | 0.8074 | - | 1.0140 |
| `householder_apply/n16/b1` | 0.0029 | - | 0.0030 |
| `householder_apply/n16/b1024` | 2.9263 | - | 2.6854 |
| `householder_apply/n4/b1` | 0.0004 | - | 0.0006 |
| `householder_apply/n4/b1024` | 0.2179 | - | 0.2511 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0011 |
| `householder_apply/n8/b1024` | 0.7379 | - | 0.7258 |
| `householder_factor/n16/b1` | 0.0023 | - | 0.0028 |
| `householder_factor/n16/b1024` | 2.2750 | - | 2.6177 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.2618 | - | 0.3240 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0011 |
| `householder_factor/n8/b1024` | 0.7302 | - | 0.9051 |
| `lu/n16/b1` | 0.0019 | - | 0.0017 |
| `lu/n16/b1024` | 1.5484 | - | 1.4516 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.1677 | - | 0.1919 |
| `lu/n8/b1` | 0.0007 | - | 0.0007 |
| `lu/n8/b1024` | 0.4808 | - | 0.4989 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0011 |
| `lu_factor/n16/b1024` | 1.1079 | - | 1.0874 |
| `lu_factor/n4/b1` | 0.0003 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1335 | - | 0.1300 |
| `lu_factor/n8/b1` | 0.0005 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3444 | - | 0.3383 |
| `lu_factor_solve/n16/b1` | 0.0017 | - | 0.0020 |
| `lu_factor_solve/n16/b1024` | 1.4264 | - | 1.8987 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.1663 | - | 0.3168 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0007 |
| `lu_factor_solve/n8/b1024` | 0.4718 | - | 0.6484 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0008 |
| `lu_solve_prepared/n16/b1024` | 0.3576 | - | 0.7052 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0407 | - | 0.1863 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0003 |
| `lu_solve_prepared/n8/b1024` | 0.1369 | - | 0.3114 |
| `qr/n16/b1` | 0.0056 | - | 0.0049 |
| `qr/n16/b1024` | 5.4319 | - | 4.7710 |
| `qr/n4/b1` | 0.0008 | - | 0.0008 |
| `qr/n4/b1024` | 0.4387 | - | 0.5754 |
| `qr/n8/b1` | 0.0016 | - | 0.0018 |
| `qr/n8/b1024` | 1.4053 | - | 1.5825 |
| `rank_revealing_qr/n16/b1` | 0.0066 | - | 0.0060 |
| `rank_revealing_qr/n16/b1024` | 6.2404 | - | 5.6453 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7153 | - | 0.7068 |
| `rank_revealing_qr/n8/b1` | 0.0023 | - | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.9253 | - | 1.8493 |
| `solve/n16/b1` | 0.0020 | - | 0.0025 |
| `solve/n16/b1024` | 1.5338 | - | 1.9589 |
| `solve/n4/b1` | 0.0006 | - | 0.0005 |
| `solve/n4/b1024` | 0.2213 | - | 0.3468 |
| `solve/n8/b1` | 0.0009 | - | 0.0009 |
| `solve/n8/b1024` | 0.5462 | - | 0.6940 |
| `svd_full/n16/b1` | 0.0330 | - | 0.0489 |
| `svd_full/n16/b1024` | 33.8033 | - | 48.7084 |
| `svd_full/n4/b1` | 0.0028 | - | 0.0044 |
| `svd_full/n4/b1024` | 2.7092 | - | 3.8860 |
| `svd_full/n8/b1` | 0.0090 | - | 0.0125 |
| `svd_full/n8/b1024` | 9.1144 | - | 12.8483 |
| `svd_thin/n16/b1` | 0.0331 | - | 0.0489 |
| `svd_thin/n16/b1024` | 33.8137 | - | 48.7607 |
| `svd_thin/n4/b1` | 0.0029 | - | 0.0044 |
| `svd_thin/n4/b1024` | 2.5778 | - | 3.9050 |
| `svd_thin/n8/b1` | 0.0091 | - | 0.0126 |
| `svd_thin/n8/b1024` | 9.1681 | - | 12.8482 |
| `svd_values/n16/b1` | 0.0240 | - | 0.0150 |
| `svd_values/n16/b1024` | 24.6704 | - | 15.1630 |
| `svd_values/n4/b1` | 0.0021 | - | 0.0026 |
| `svd_values/n4/b1024` | 1.9061 | - | 2.1120 |
| `svd_values/n8/b1` | 0.0069 | - | 0.0056 |
| `svd_values/n8/b1024` | 6.7726 | - | 5.3800 |
| `triangular_solve/n16/b1` | 0.0005 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3068 | - | 0.3931 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0509 | - | 0.1193 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n8/b1024` | 0.1309 | - | 0.1837 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0027 | 0.0007 |
| `cholesky/n16/b1024` | 0.5202 | 0.2648 | 0.6064 |
| `cholesky/n4/b1` | 0.0002 | 0.0026 | 0.0002 |
| `cholesky/n4/b1024` | 0.1070 | 0.0329 | 0.1162 |
| `cholesky/n8/b1` | 0.0003 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2147 | 0.1115 | 0.2396 |
| `eig/n16/b1` | 0.0535 | 0.0564 | 0.0404 |
| `eig/n16/b1024` | 56.0472 | 18.6761 | 41.6941 |
| `eig/n4/b1` | 0.0040 | 0.0056 | 0.0038 |
| `eig/n4/b1024` | 3.5465 | 1.6797 | 3.2832 |
| `eig/n8/b1` | 0.0142 | 0.0170 | 0.0112 |
| `eig/n8/b1024` | 13.7835 | 3.4862 | 10.6536 |
| `eigh/n16/b1` | 0.0175 | 0.0207 | 0.0235 |
| `eigh/n16/b1024` | 17.7122 | 7.5590 | 24.2365 |
| `eigh/n4/b1` | 0.0016 | 0.0041 | 0.0019 |
| `eigh/n4/b1024` | 1.4742 | 0.3731 | 1.8116 |
| `eigh/n8/b1` | 0.0051 | 0.0076 | 0.0065 |
| `eigh/n8/b1024` | 5.0907 | 2.5679 | 6.5579 |
| `eigvals/n16/b1` | 0.0372 | 0.0403 | 0.0293 |
| `eigvals/n16/b1024` | 38.8802 | 14.0738 | 29.9781 |
| `eigvals/n4/b1` | 0.0023 | 0.0049 | 0.0025 |
| `eigvals/n4/b1024` | 1.9163 | 0.9630 | 2.0467 |
| `eigvals/n8/b1` | 0.0097 | 0.0127 | 0.0085 |
| `eigvals/n8/b1024` | 9.2276 | 2.3495 | 7.9668 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0162 | 0.0084 |
| `eigvalsh/n16/b1024` | 13.1995 | 4.0799 | 8.7292 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0028 | 0.0010 |
| `eigvalsh/n4/b1024` | 1.1799 | 0.5969 | 0.8431 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0081 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0434 | 1.7389 | 2.7209 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0050 | 0.0026 |
| `full_piv_lu/n16/b1024` | 2.0529 | 1.0369 | 2.7034 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0022 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2250 | 0.0601 | 0.2222 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0032 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6521 | 0.3064 | 0.5883 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0048 | 0.0039 |
| `full_piv_lu_solve/n16/b1024` | 2.0791 | 0.5428 | 3.7957 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0024 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3319 | 0.1729 | 0.5556 |
| `full_piv_lu_solve/n8/b1` | 0.0013 | 0.0036 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.8133 | 0.4087 | 1.2029 |
| `householder_apply/n16/b1` | 0.0028 | 0.0044 | 0.0030 |
| `householder_apply/n16/b1024` | 2.8029 | 0.7362 | 2.6695 |
| `householder_apply/n4/b1` | 0.0003 | 0.0021 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2112 | 0.0614 | 0.2515 |
| `householder_apply/n8/b1` | 0.0008 | 0.0026 | 0.0011 |
| `householder_apply/n8/b1024` | 0.7039 | 0.1829 | 0.7283 |
| `householder_factor/n16/b1` | 0.0023 | 0.0039 | 0.0027 |
| `householder_factor/n16/b1024` | 2.1630 | 0.5639 | 2.6104 |
| `householder_factor/n4/b1` | 0.0004 | 0.0026 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2657 | 0.0741 | 0.3220 |
| `householder_factor/n8/b1` | 0.0008 | 0.0037 | 0.0010 |
| `householder_factor/n8/b1024` | 0.7087 | 0.3577 | 0.9066 |
| `lu/n16/b1` | 0.0019 | 0.0037 | 0.0017 |
| `lu/n16/b1024` | 1.5495 | 0.4083 | 1.4546 |
| `lu/n4/b1` | 0.0004 | 0.0026 | 0.0004 |
| `lu/n4/b1024` | 0.1719 | 0.0909 | 0.1912 |
| `lu/n8/b1` | 0.0007 | 0.0024 | 0.0007 |
| `lu/n8/b1024` | 0.4807 | 0.2416 | 0.4831 |
| `lu_factor/n16/b1` | 0.0013 | 0.0038 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1291 | 0.5627 | 1.0893 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1342 | 0.0392 | 0.1290 |
| `lu_factor/n8/b1` | 0.0006 | 0.0028 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3557 | 0.0919 | 0.3417 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0042 | 0.0022 |
| `lu_factor_solve/n16/b1024` | 1.4276 | 0.7211 | 2.3207 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0020 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1656 | 0.0539 | 0.8331 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0033 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.4793 | 0.2426 | 1.2701 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0023 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3672 | 0.1059 | 0.9095 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | 0.0203 | 0.5869 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0029 | 0.0008 |
| `lu_solve_prepared/n8/b1024` | 0.1373 | 0.0457 | 0.7302 |
| `qr/n16/b1` | 0.0053 | 0.0078 | 0.0049 |
| `qr/n16/b1024` | 5.3128 | 1.8614 | 4.7548 |
| `qr/n4/b1` | 0.0008 | 0.0022 | 0.0008 |
| `qr/n4/b1024` | 0.4431 | 0.2224 | 0.5746 |
| `qr/n8/b1` | 0.0016 | 0.0039 | 0.0019 |
| `qr/n8/b1024` | 1.3631 | 0.6925 | 1.6036 |
| `rank_revealing_qr/n16/b1` | 0.0064 | 0.0096 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.0225 | 3.0867 | 5.6186 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0034 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7176 | 0.3605 | 0.7064 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0043 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8819 | 0.9387 | 1.8496 |
| `solve/n16/b1` | 0.0021 | 0.0038 | 0.0022 |
| `solve/n16/b1024` | 1.5465 | 0.3993 | 2.2198 |
| `solve/n4/b1` | 0.0006 | 0.0029 | 0.0008 |
| `solve/n4/b1024` | 0.2223 | 0.0584 | 0.7427 |
| `solve/n8/b1` | 0.0009 | 0.0034 | 0.0011 |
| `solve/n8/b1024` | 0.5447 | 0.1416 | 0.9035 |
| `svd_full/n16/b1` | 0.0328 | 0.0355 | 0.0489 |
| `svd_full/n16/b1024` | 33.4773 | 8.6935 | 49.5288 |
| `svd_full/n4/b1` | 0.0028 | 0.0046 | 0.0043 |
| `svd_full/n4/b1024` | 2.5384 | 0.6388 | 3.8453 |
| `svd_full/n8/b1` | 0.0103 | 0.0115 | 0.0125 |
| `svd_full/n8/b1024` | 8.9790 | 2.2974 | 12.8547 |
| `svd_thin/n16/b1` | 0.0330 | 0.0357 | 0.0490 |
| `svd_thin/n16/b1024` | 33.4147 | 8.9225 | 48.9371 |
| `svd_thin/n4/b1` | 0.0028 | 0.0049 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5181 | 1.2965 | 3.8538 |
| `svd_thin/n8/b1` | 0.0089 | 0.0118 | 0.0125 |
| `svd_thin/n8/b1024` | 9.0942 | 2.3000 | 12.8448 |
| `svd_values/n16/b1` | 0.0239 | 0.0270 | 0.0150 |
| `svd_values/n16/b1024` | 24.5422 | 10.6962 | 15.0434 |
| `svd_values/n4/b1` | 0.0021 | 0.0041 | 0.0026 |
| `svd_values/n4/b1024` | 1.9054 | 0.9614 | 2.0803 |
| `svd_values/n8/b1` | 0.0069 | 0.0096 | 0.0056 |
| `svd_values/n8/b1024` | 6.8916 | 3.4749 | 5.3978 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0029 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.2988 | 0.0806 | 0.6544 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0026 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0515 | 0.0291 | 0.4022 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0027 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1299 | 0.0412 | 0.5290 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0034 | 0.0007 |
| `cholesky/n16/b1024` | 0.5128 | 0.1342 | 0.6206 |
| `cholesky/n4/b1` | 0.0002 | 0.0023 | 0.0002 |
| `cholesky/n4/b1024` | 0.1066 | 0.0216 | 0.1184 |
| `cholesky/n8/b1` | 0.0003 | 0.0037 | 0.0003 |
| `cholesky/n8/b1024` | 0.2140 | 0.0353 | 0.2366 |
| `eig/n16/b1` | 0.0541 | 0.0577 | 0.0404 |
| `eig/n16/b1024` | 56.3904 | 8.1148 | 42.2845 |
| `eig/n4/b1` | 0.0040 | 0.0072 | 0.0037 |
| `eig/n4/b1024` | 3.6273 | 0.4796 | 3.2472 |
| `eig/n8/b1` | 0.0146 | 0.0172 | 0.0112 |
| `eig/n8/b1024` | 13.9633 | 2.0954 | 10.6460 |
| `eigh/n16/b1` | 0.0175 | 0.0206 | 0.0232 |
| `eigh/n16/b1024` | 17.7546 | 2.2503 | 24.1642 |
| `eigh/n4/b1` | 0.0017 | 0.0047 | 0.0019 |
| `eigh/n4/b1024` | 1.4713 | 0.3772 | 1.8269 |
| `eigh/n8/b1` | 0.0051 | 0.0082 | 0.0064 |
| `eigh/n8/b1024` | 5.0537 | 1.1016 | 6.5452 |
| `eigvals/n16/b1` | 0.0371 | 0.0399 | 0.0292 |
| `eigvals/n16/b1024` | 38.9584 | 5.3401 | 29.9050 |
| `eigvals/n4/b1` | 0.0023 | 0.0056 | 0.0025 |
| `eigvals/n4/b1024` | 1.8835 | 0.4781 | 2.0551 |
| `eigvals/n8/b1` | 0.0098 | 0.0233 | 0.0086 |
| `eigvals/n8/b1024` | 9.1582 | 1.7309 | 7.9606 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0163 | 0.0085 |
| `eigvalsh/n16/b1024` | 13.2388 | 1.7038 | 8.7875 |
| `eigvalsh/n4/b1` | 0.0014 | 0.0052 | 0.0011 |
| `eigvalsh/n4/b1024` | 1.1849 | 0.3029 | 0.8759 |
| `eigvalsh/n8/b1` | 0.0044 | 0.0073 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0422 | 1.0168 | 2.7628 |
| `full_piv_lu/n16/b1` | 0.0027 | 0.0058 | 0.0027 |
| `full_piv_lu/n16/b1024` | 2.0967 | 0.2788 | 2.7421 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0025 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2229 | 0.0623 | 0.2336 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0044 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6067 | 0.1631 | 0.5793 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0056 | 0.0040 |
| `full_piv_lu_solve/n16/b1024` | 2.0760 | 0.5353 | 3.8975 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0043 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3200 | 0.0588 | 0.5670 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0044 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7937 | 0.2057 | 1.2031 |
| `householder_apply/n16/b1` | 0.0029 | 0.0058 | 0.0030 |
| `householder_apply/n16/b1024` | 2.8325 | 0.7058 | 2.6516 |
| `householder_apply/n4/b1` | 0.0003 | 0.0035 | 0.0006 |
| `householder_apply/n4/b1024` | 0.2105 | 0.0583 | 0.2509 |
| `householder_apply/n8/b1` | 0.0008 | 0.0033 | 0.0011 |
| `householder_apply/n8/b1024` | 0.7014 | 0.1897 | 0.7264 |
| `householder_factor/n16/b1` | 0.0023 | 0.0051 | 0.0027 |
| `householder_factor/n16/b1024` | 2.1682 | 0.3776 | 2.6347 |
| `householder_factor/n4/b1` | 0.0003 | 0.0026 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2607 | 0.0441 | 0.3225 |
| `householder_factor/n8/b1` | 0.0008 | 0.0034 | 0.0010 |
| `householder_factor/n8/b1024` | 0.7295 | 0.1913 | 0.9062 |
| `lu/n16/b1` | 0.0019 | 0.0045 | 0.0017 |
| `lu/n16/b1024` | 1.5501 | 0.3928 | 1.4643 |
| `lu/n4/b1` | 0.0004 | 0.0021 | 0.0004 |
| `lu/n4/b1024` | 0.1673 | 0.0301 | 0.1927 |
| `lu/n8/b1` | 0.0007 | 0.0043 | 0.0007 |
| `lu/n8/b1024` | 0.4765 | 0.0663 | 0.4871 |
| `lu_factor/n16/b1` | 0.0013 | 0.0032 | 0.0011 |
| `lu_factor/n16/b1024` | 1.0717 | 0.2831 | 1.1091 |
| `lu_factor/n4/b1` | 0.0004 | 0.0045 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1323 | 0.0388 | 0.1305 |
| `lu_factor/n8/b1` | 0.0006 | 0.0031 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3454 | 0.0938 | 0.3407 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0041 | 0.0022 |
| `lu_factor_solve/n16/b1024` | 1.3884 | 0.3571 | 2.2831 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0019 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1641 | 0.0467 | 0.7736 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0039 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.4711 | 0.1270 | 1.2199 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0022 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3618 | 0.1057 | 0.9410 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0034 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | 0.0187 | 0.5740 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0022 | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.1402 | 0.0365 | 0.7592 |
| `qr/n16/b1` | 0.0056 | 0.0085 | 0.0050 |
| `qr/n16/b1024` | 5.3305 | 1.3337 | 4.7269 |
| `qr/n4/b1` | 0.0007 | 0.0040 | 0.0008 |
| `qr/n4/b1024` | 0.4388 | 0.0610 | 0.5768 |
| `qr/n8/b1` | 0.0016 | 0.0049 | 0.0019 |
| `qr/n8/b1024` | 1.3859 | 0.3541 | 1.5896 |
| `rank_revealing_qr/n16/b1` | 0.0066 | 0.0098 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.1486 | 1.5219 | 5.5984 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0034 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7028 | 0.0945 | 0.6950 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0048 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8807 | 0.4718 | 1.8332 |
| `solve/n16/b1` | 0.0021 | 0.0046 | 0.0023 |
| `solve/n16/b1024` | 1.5225 | 0.3917 | 2.2975 |
| `solve/n4/b1` | 0.0006 | 0.0037 | 0.0008 |
| `solve/n4/b1024` | 0.2205 | 0.0607 | 0.7546 |
| `solve/n8/b1` | 0.0009 | 0.0035 | 0.0012 |
| `solve/n8/b1024` | 0.5369 | 0.1411 | 1.2485 |
| `svd_full/n16/b1` | 0.0327 | 0.0357 | 0.0489 |
| `svd_full/n16/b1024` | 33.5955 | 5.0040 | 48.7906 |
| `svd_full/n4/b1` | 0.0029 | 0.0059 | 0.0043 |
| `svd_full/n4/b1024` | 2.5566 | 0.3620 | 3.8233 |
| `svd_full/n8/b1` | 0.0095 | 0.0118 | 0.0125 |
| `svd_full/n8/b1024` | 9.0499 | 2.2885 | 12.9003 |
| `svd_thin/n16/b1` | 0.0329 | 0.0358 | 0.0488 |
| `svd_thin/n16/b1024` | 34.5728 | 7.9958 | 48.4509 |
| `svd_thin/n4/b1` | 0.0029 | 0.0059 | 0.0043 |
| `svd_thin/n4/b1024` | 2.5261 | 0.6421 | 3.8211 |
| `svd_thin/n8/b1` | 0.0089 | 0.0119 | 0.0124 |
| `svd_thin/n8/b1024` | 9.0284 | 1.1537 | 12.8006 |
| `svd_values/n16/b1` | 0.0240 | 0.0268 | 0.0150 |
| `svd_values/n16/b1024` | 24.6778 | 3.0979 | 14.9895 |
| `svd_values/n4/b1` | 0.0021 | 0.0050 | 0.0026 |
| `svd_values/n4/b1024` | 1.9270 | 0.4872 | 2.0743 |
| `svd_values/n8/b1` | 0.0068 | 0.0173 | 0.0056 |
| `svd_values/n8/b1024` | 6.7808 | 0.8979 | 5.3787 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0027 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3051 | 0.0811 | 0.5372 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0022 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0508 | 0.0151 | 0.4462 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0039 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.1308 | 0.0300 | 0.5410 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0010 |
| `cholesky/n16/b1024` | 0.8005 | - | 0.9168 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1178 | - | 0.1349 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2526 | - | 0.2913 |
| `eig/n16/b1` | 0.0717 | - | 0.1006 |
| `eig/n16/b1024` | 76.0672 | - | 119.8851 |
| `eig/n4/b1` | 0.0057 | - | 0.0081 |
| `eig/n4/b1024` | 5.7538 | - | 7.9069 |
| `eig/n8/b1` | 0.0199 | - | 0.0261 |
| `eig/n8/b1024` | 20.3966 | - | 27.9841 |
| `eigh/n16/b1` | 0.0180 | - | 0.0261 |
| `eigh/n16/b1024` | 19.4068 | - | 26.9948 |
| `eigh/n4/b1` | 0.0024 | - | 0.0022 |
| `eigh/n4/b1024` | 1.7736 | - | 2.1629 |
| `eigh/n8/b1` | 0.0057 | - | 0.0072 |
| `eigh/n8/b1024` | 5.5049 | - | 7.3975 |
| `eigvals/n16/b1` | 0.0435 | - | 0.0751 |
| `eigvals/n16/b1024` | 46.4964 | - | 89.6142 |
| `eigvals/n4/b1` | 0.0031 | - | 0.0063 |
| `eigvals/n4/b1024` | 2.9418 | - | 6.0292 |
| `eigvals/n8/b1` | 0.0118 | - | 0.0210 |
| `eigvals/n8/b1024` | 12.0336 | - | 22.2495 |
| `eigvalsh/n16/b1` | 0.0136 | - | 0.0116 |
| `eigvalsh/n16/b1024` | 14.1225 | - | 11.5295 |
| `eigvalsh/n4/b1` | 0.0016 | - | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4145 | - | 1.2501 |
| `eigvalsh/n8/b1` | 0.0046 | - | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3568 | - | 3.6408 |
| `full_piv_lu/n16/b1` | 0.0031 | - | 0.0125 |
| `full_piv_lu/n16/b1024` | 2.8943 | - | 20.2487 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2759 | - | 0.5324 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.7388 | - | 2.3457 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | - | 0.0157 |
| `full_piv_lu_solve/n16/b1024` | 3.0697 | - | 22.7290 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4461 | - | 1.1479 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0036 |
| `full_piv_lu_solve/n8/b1024` | 1.1013 | - | 3.6495 |
| `householder_apply/n16/b1` | 0.0028 | - | 0.0047 |
| `householder_apply/n16/b1024` | 3.3714 | - | 4.4517 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0008 |
| `householder_apply/n4/b1024` | 0.2087 | - | 0.2673 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0015 |
| `householder_apply/n8/b1024` | 0.7023 | - | 0.9046 |
| `householder_factor/n16/b1` | 0.0027 | - | 0.0045 |
| `householder_factor/n16/b1024` | 2.7188 | - | 4.4474 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0007 |
| `householder_factor/n4/b1024` | 0.3242 | - | 0.5497 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0016 |
| `householder_factor/n8/b1024` | 0.8678 | - | 1.4181 |
| `lu/n16/b1` | 0.0021 | - | 0.0023 |
| `lu/n16/b1024` | 1.8528 | - | 2.5577 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.2103 | - | 0.2327 |
| `lu/n8/b1` | 0.0008 | - | 0.0008 |
| `lu/n8/b1024` | 0.5870 | - | 0.6290 |
| `lu_factor/n16/b1` | 0.0015 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2447 | - | 1.6235 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1654 | - | 0.1621 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0005 |
| `lu_factor/n8/b1024` | 0.4206 | - | 0.4590 |
| `lu_factor_solve/n16/b1` | 0.0024 | - | 0.0026 |
| `lu_factor_solve/n16/b1024` | 2.0225 | - | 2.6449 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0005 |
| `lu_factor_solve/n4/b1024` | 0.2554 | - | 0.4118 |
| `lu_factor_solve/n8/b1` | 0.0010 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.7107 | - | 0.9274 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7719 | - | 1.0437 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0972 | - | 0.2445 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.2869 | - | 0.4686 |
| `qr/n16/b1` | 0.0067 | - | 0.0077 |
| `qr/n16/b1024` | 6.6335 | - | 7.7480 |
| `qr/n4/b1` | 0.0007 | - | 0.0011 |
| `qr/n4/b1024` | 0.5233 | - | 0.8605 |
| `qr/n8/b1` | 0.0018 | - | 0.0026 |
| `qr/n8/b1024` | 1.5931 | - | 2.2881 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.5323 | - | 10.0845 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8198 | - | 1.0983 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.2298 | - | 3.0095 |
| `solve/n16/b1` | 0.0029 | - | 0.0030 |
| `solve/n16/b1024` | 2.1555 | - | 2.8268 |
| `solve/n4/b1` | 0.0007 | - | 0.0007 |
| `solve/n4/b1024` | 0.3151 | - | 0.4504 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7998 | - | 0.9951 |
| `svd_full/n16/b1` | 0.0349 | - | 0.0546 |
| `svd_full/n16/b1024` | 36.9010 | - | 56.4032 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_full/n4/b1024` | 3.0205 | - | 4.7554 |
| `svd_full/n8/b1` | 0.0097 | - | 0.0147 |
| `svd_full/n8/b1024` | 10.1478 | - | 14.9827 |
| `svd_thin/n16/b1` | 0.0348 | - | 0.0548 |
| `svd_thin/n16/b1024` | 36.7818 | - | 56.2664 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0053 |
| `svd_thin/n4/b1024` | 3.0233 | - | 4.7511 |
| `svd_thin/n8/b1` | 0.0097 | - | 0.0146 |
| `svd_thin/n8/b1024` | 10.3855 | - | 14.9853 |
| `svd_values/n16/b1` | 0.0261 | - | 0.0199 |
| `svd_values/n16/b1024` | 27.3632 | - | 20.1089 |
| `svd_values/n4/b1` | 0.0025 | - | 0.0032 |
| `svd_values/n4/b1024` | 2.2820 | - | 2.7883 |
| `svd_values/n8/b1` | 0.0076 | - | 0.0070 |
| `svd_values/n8/b1024` | 7.8205 | - | 6.7967 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0007 |
| `triangular_solve/n16/b1024` | 0.5947 | - | 0.5968 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0956 | - | 0.1562 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.2382 | - | 0.2679 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0037 | 0.0010 |
| `cholesky/n16/b1024` | 0.8002 | 0.4033 | 0.9716 |
| `cholesky/n4/b1` | 0.0003 | 0.0026 | 0.0002 |
| `cholesky/n4/b1024` | 0.1175 | 0.0371 | 0.1364 |
| `cholesky/n8/b1` | 0.0004 | 0.0026 | 0.0004 |
| `cholesky/n8/b1024` | 0.2500 | 0.1275 | 0.2921 |
| `eig/n16/b1` | 0.0721 | 0.0765 | 0.0999 |
| `eig/n16/b1024` | 76.1998 | 23.9631 | 119.5009 |
| `eig/n4/b1` | 0.0059 | 0.0096 | 0.0081 |
| `eig/n4/b1024` | 5.8125 | 2.9595 | 7.9123 |
| `eig/n8/b1` | 0.0200 | 0.0231 | 0.0262 |
| `eig/n8/b1024` | 20.6229 | 8.9805 | 27.9487 |
| `eigh/n16/b1` | 0.0180 | 0.0210 | 0.0260 |
| `eigh/n16/b1024` | 19.4561 | 6.4637 | 27.0351 |
| `eigh/n4/b1` | 0.0020 | 0.0045 | 0.0023 |
| `eigh/n4/b1024` | 1.7699 | 0.4534 | 2.1595 |
| `eigh/n8/b1` | 0.0056 | 0.0082 | 0.0073 |
| `eigh/n8/b1024` | 5.4852 | 1.4148 | 7.4263 |
| `eigvals/n16/b1` | 0.0439 | 0.0468 | 0.0749 |
| `eigvals/n16/b1024` | 46.7838 | 15.0028 | 89.7399 |
| `eigvals/n4/b1` | 0.0031 | 0.0047 | 0.0063 |
| `eigvals/n4/b1024` | 2.9681 | 1.3920 | 6.0226 |
| `eigvals/n8/b1` | 0.0117 | 0.0143 | 0.0210 |
| `eigvals/n8/b1024` | 11.9104 | 2.9987 | 22.1789 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0166 | 0.0115 |
| `eigvalsh/n16/b1024` | 14.2000 | 3.9242 | 11.5189 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0041 | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4187 | 0.3656 | 1.2523 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0070 | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3560 | 2.2238 | 3.6540 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0053 | 0.0119 |
| `full_piv_lu/n16/b1024` | 2.9000 | 1.4553 | 20.2813 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2676 | 0.1376 | 0.5503 |
| `full_piv_lu/n8/b1` | 0.0012 | 0.0038 | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.7734 | 0.3742 | 2.2679 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0053 | 0.0158 |
| `full_piv_lu_solve/n16/b1024` | 3.0605 | 0.7972 | 22.6488 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0027 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4454 | 0.2291 | 1.2692 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0041 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.0610 | 0.3022 | 3.6993 |
| `householder_apply/n16/b1` | 0.0027 | 0.0056 | 0.0046 |
| `householder_apply/n16/b1024` | 3.5281 | 0.9141 | 4.5026 |
| `householder_apply/n4/b1` | 0.0003 | 0.0027 | 0.0008 |
| `householder_apply/n4/b1024` | 0.2009 | 0.0597 | 0.2669 |
| `householder_apply/n8/b1` | 0.0007 | 0.0033 | 0.0015 |
| `householder_apply/n8/b1024` | 0.6697 | 0.3296 | 0.8943 |
| `householder_factor/n16/b1` | 0.0027 | 0.0047 | 0.0045 |
| `householder_factor/n16/b1024` | 2.7186 | 1.3797 | 4.4632 |
| `householder_factor/n4/b1` | 0.0004 | 0.0025 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3249 | 0.0858 | 0.5477 |
| `householder_factor/n8/b1` | 0.0009 | 0.0034 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8556 | 0.4371 | 1.4345 |
| `lu/n16/b1` | 0.0021 | 0.0046 | 0.0023 |
| `lu/n16/b1024` | 1.8184 | 0.8980 | 2.6688 |
| `lu/n4/b1` | 0.0004 | 0.0022 | 0.0004 |
| `lu/n4/b1024` | 0.2159 | 0.1110 | 0.2340 |
| `lu/n8/b1` | 0.0008 | 0.0034 | 0.0008 |
| `lu/n8/b1024` | 0.5793 | 0.2877 | 0.6231 |
| `lu_factor/n16/b1` | 0.0015 | 0.0033 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2526 | 0.5246 | 1.6226 |
| `lu_factor/n4/b1` | 0.0004 | 0.0021 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1653 | 0.0460 | 0.1600 |
| `lu_factor/n8/b1` | 0.0006 | 0.0023 | 0.0005 |
| `lu_factor/n8/b1024` | 0.4096 | 0.1086 | 0.4538 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0052 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0434 | 0.5357 | 3.0420 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0026 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2576 | 0.0693 | 0.8557 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0032 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.7079 | 0.2099 | 1.2897 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0038 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.7927 | 0.2045 | 1.1606 |
| `lu_solve_prepared/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0969 | 0.0349 | 0.6016 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0028 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2872 | 0.0835 | 0.6404 |
| `qr/n16/b1` | 0.0067 | 0.0098 | 0.0077 |
| `qr/n16/b1024` | 6.5480 | 3.3131 | 7.6991 |
| `qr/n4/b1` | 0.0007 | 0.0033 | 0.0011 |
| `qr/n4/b1024` | 0.5120 | 0.2636 | 0.8651 |
| `qr/n8/b1` | 0.0018 | 0.0041 | 0.0025 |
| `qr/n8/b1024` | 1.5541 | 0.7916 | 2.2838 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0103 | 0.0098 |
| `rank_revealing_qr/n16/b1024` | 7.4783 | 2.3663 | 10.1090 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0033 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8166 | 0.4129 | 1.0932 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0049 | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.1889 | 1.0961 | 3.0078 |
| `solve/n16/b1` | 0.0029 | 0.0053 | 0.0031 |
| `solve/n16/b1024` | 2.1987 | 0.5597 | 3.1741 |
| `solve/n4/b1` | 0.0007 | 0.0028 | 0.0009 |
| `solve/n4/b1024` | 0.3382 | 0.0867 | 0.8688 |
| `solve/n8/b1` | 0.0013 | 0.0036 | 0.0014 |
| `solve/n8/b1024` | 0.8204 | 0.2142 | 1.2132 |
| `svd_full/n16/b1` | 0.0348 | 0.0380 | 0.0547 |
| `svd_full/n16/b1024` | 36.7522 | 15.3502 | 56.3831 |
| `svd_full/n4/b1` | 0.0031 | 0.0054 | 0.0053 |
| `svd_full/n4/b1024` | 3.0070 | 0.7572 | 4.7667 |
| `svd_full/n8/b1` | 0.0097 | 0.0123 | 0.0145 |
| `svd_full/n8/b1024` | 10.1050 | 5.0785 | 15.1963 |
| `svd_thin/n16/b1` | 0.0348 | 0.0381 | 0.0549 |
| `svd_thin/n16/b1024` | 37.5811 | 15.0138 | 56.4799 |
| `svd_thin/n4/b1` | 0.0031 | 0.0047 | 0.0053 |
| `svd_thin/n4/b1024` | 2.9974 | 1.5376 | 4.7971 |
| `svd_thin/n8/b1` | 0.0096 | 0.0120 | 0.0147 |
| `svd_thin/n8/b1024` | 10.1394 | 2.5366 | 15.0035 |
| `svd_values/n16/b1` | 0.0261 | 0.0290 | 0.0197 |
| `svd_values/n16/b1024` | 27.5174 | 6.9873 | 20.1361 |
| `svd_values/n4/b1` | 0.0024 | 0.0048 | 0.0033 |
| `svd_values/n4/b1024` | 2.2798 | 0.5741 | 2.8049 |
| `svd_values/n8/b1` | 0.0076 | 0.0103 | 0.0071 |
| `svd_values/n8/b1024` | 7.8035 | 3.9385 | 6.8518 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0037 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.6062 | 0.2968 | 0.8244 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0022 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0972 | 0.0295 | 0.4713 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0022 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2358 | 0.0645 | 0.5950 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0041 | 0.0010 |
| `cholesky/n16/b1024` | 0.7750 | 0.1992 | 0.9313 |
| `cholesky/n4/b1` | 0.0002 | 0.0026 | 0.0002 |
| `cholesky/n4/b1024` | 0.1182 | 0.0233 | 0.1408 |
| `cholesky/n8/b1` | 0.0004 | 0.0024 | 0.0004 |
| `cholesky/n8/b1024` | 0.2583 | 0.0374 | 0.2994 |
| `eig/n16/b1` | 0.0720 | 0.0771 | 0.1000 |
| `eig/n16/b1024` | 76.1745 | 15.9807 | 119.7953 |
| `eig/n4/b1` | 0.0058 | 0.0088 | 0.0082 |
| `eig/n4/b1024` | 5.7562 | 0.7456 | 7.9651 |
| `eig/n8/b1` | 0.0200 | 0.0230 | 0.0262 |
| `eig/n8/b1024` | 20.4903 | 2.6327 | 28.0013 |
| `eigh/n16/b1` | 0.0180 | 0.0210 | 0.0261 |
| `eigh/n16/b1024` | 19.4370 | 2.8086 | 27.3016 |
| `eigh/n4/b1` | 0.0020 | 0.0050 | 0.0023 |
| `eigh/n4/b1024` | 1.7708 | 0.4504 | 2.1861 |
| `eigh/n8/b1` | 0.0056 | 0.0083 | 0.0073 |
| `eigh/n8/b1024` | 5.4948 | 0.7304 | 7.4685 |
| `eigvals/n16/b1` | 0.0433 | 0.0466 | 0.0747 |
| `eigvals/n16/b1024` | 46.7416 | 9.1927 | 89.7017 |
| `eigvals/n4/b1` | 0.0030 | 0.0064 | 0.0063 |
| `eigvals/n4/b1024` | 2.8383 | 0.7177 | 6.0763 |
| `eigvals/n8/b1` | 0.0116 | 0.0144 | 0.0210 |
| `eigvals/n8/b1024` | 11.8427 | 1.5091 | 22.1914 |
| `eigvalsh/n16/b1` | 0.0135 | 0.0166 | 0.0116 |
| `eigvalsh/n16/b1024` | 14.1030 | 1.8487 | 11.6049 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0049 | 0.0015 |
| `eigvalsh/n4/b1024` | 1.4141 | 0.1816 | 1.2706 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0074 | 0.0039 |
| `eigvalsh/n8/b1024` | 4.3515 | 0.5612 | 3.6842 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0061 | 0.0118 |
| `full_piv_lu/n16/b1024` | 3.0219 | 0.7139 | 20.2886 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0035 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2641 | 0.0725 | 0.5500 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0050 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7488 | 0.1904 | 2.3217 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0064 | 0.0158 |
| `full_piv_lu_solve/n16/b1024` | 3.0760 | 0.7675 | 22.6498 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0032 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4452 | 0.0752 | 1.2880 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0044 | 0.0038 |
| `full_piv_lu_solve/n8/b1024` | 1.0736 | 0.2802 | 3.6938 |
| `householder_apply/n16/b1` | 0.0028 | 0.0060 | 0.0047 |
| `householder_apply/n16/b1024` | 3.4493 | 0.7418 | 4.3067 |
| `householder_apply/n4/b1` | 0.0003 | 0.0033 | 0.0008 |
| `householder_apply/n4/b1024` | 0.2044 | 0.0578 | 0.2802 |
| `householder_apply/n8/b1` | 0.0008 | 0.0024 | 0.0016 |
| `householder_apply/n8/b1024` | 0.6720 | 0.1712 | 0.9004 |
| `householder_factor/n16/b1` | 0.0027 | 0.0056 | 0.0045 |
| `householder_factor/n16/b1024` | 2.7310 | 0.6843 | 4.4851 |
| `householder_factor/n4/b1` | 0.0004 | 0.0033 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3222 | 0.0858 | 0.5507 |
| `householder_factor/n8/b1` | 0.0009 | 0.0039 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8629 | 0.2249 | 1.4362 |
| `lu/n16/b1` | 0.0022 | 0.0052 | 0.0023 |
| `lu/n16/b1024` | 1.8559 | 0.4796 | 2.6318 |
| `lu/n4/b1` | 0.0004 | 0.0043 | 0.0004 |
| `lu/n4/b1024` | 0.2133 | 0.0357 | 0.2358 |
| `lu/n8/b1` | 0.0008 | 0.0039 | 0.0008 |
| `lu/n8/b1024` | 0.5703 | 0.0841 | 0.6314 |
| `lu_factor/n16/b1` | 0.0015 | 0.0045 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2183 | 0.3171 | 1.6419 |
| `lu_factor/n4/b1` | 0.0004 | 0.0029 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1664 | 0.0451 | 0.1635 |
| `lu_factor/n8/b1` | 0.0006 | 0.0023 | 0.0005 |
| `lu_factor/n8/b1024` | 0.4153 | 0.1113 | 0.4534 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0053 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0137 | 0.4944 | 3.0168 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0030 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2555 | 0.0414 | 0.8035 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0040 | 0.0011 |
| `lu_factor_solve/n8/b1024` | 0.6941 | 0.1834 | 1.4394 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0043 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.8232 | 0.2254 | 1.1545 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0022 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0991 | 0.0351 | 0.5986 |
| `lu_solve_prepared/n8/b1` | 0.0005 | 0.0030 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2875 | 0.0861 | 0.8210 |
| `qr/n16/b1` | 0.0068 | 0.0094 | 0.0078 |
| `qr/n16/b1024` | 6.5939 | 0.8678 | 7.6641 |
| `qr/n4/b1` | 0.0007 | 0.0033 | 0.0011 |
| `qr/n4/b1024` | 0.5308 | 0.1353 | 0.8591 |
| `qr/n8/b1` | 0.0018 | 0.0048 | 0.0025 |
| `qr/n8/b1024` | 1.5715 | 0.2075 | 2.2957 |
| `rank_revealing_qr/n16/b1` | 0.0078 | 0.0191 | 0.0098 |
| `rank_revealing_qr/n16/b1024` | 7.6170 | 1.8889 | 10.1004 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0044 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8216 | 0.1133 | 1.1015 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0055 | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1972 | 0.3074 | 3.0095 |
| `solve/n16/b1` | 0.0029 | 0.0057 | 0.0031 |
| `solve/n16/b1024` | 2.1349 | 0.5436 | 3.1980 |
| `solve/n4/b1` | 0.0007 | 0.0043 | 0.0009 |
| `solve/n4/b1024` | 0.3227 | 0.0847 | 0.8925 |
| `solve/n8/b1` | 0.0013 | 0.0048 | 0.0014 |
| `solve/n8/b1024` | 0.7889 | 0.2049 | 1.2506 |
| `svd_full/n16/b1` | 0.0349 | 0.0379 | 0.0549 |
| `svd_full/n16/b1024` | 36.9218 | 7.8973 | 56.6695 |
| `svd_full/n4/b1` | 0.0031 | 0.0061 | 0.0053 |
| `svd_full/n4/b1024` | 3.0397 | 0.3834 | 4.8170 |
| `svd_full/n8/b1` | 0.0097 | 0.0127 | 0.0147 |
| `svd_full/n8/b1024` | 10.1328 | 1.8055 | 15.0253 |
| `svd_thin/n16/b1` | 0.0348 | 0.0378 | 0.0548 |
| `svd_thin/n16/b1024` | 36.7074 | 7.9786 | 56.2550 |
| `svd_thin/n4/b1` | 0.0031 | 0.0061 | 0.0053 |
| `svd_thin/n4/b1024` | 3.0206 | 0.7635 | 4.8013 |
| `svd_thin/n8/b1` | 0.0097 | 0.0127 | 0.0147 |
| `svd_thin/n8/b1024` | 10.1294 | 2.3839 | 15.0304 |
| `svd_values/n16/b1` | 0.0261 | 0.0290 | 0.0199 |
| `svd_values/n16/b1024` | 27.3352 | 4.1523 | 20.2313 |
| `svd_values/n4/b1` | 0.0024 | 0.0054 | 0.0032 |
| `svd_values/n4/b1024` | 2.2827 | 0.2970 | 2.8188 |
| `svd_values/n8/b1` | 0.0075 | 0.0107 | 0.0072 |
| `svd_values/n8/b1024` | 7.8015 | 1.9819 | 6.8580 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0039 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5890 | 0.1517 | 0.7679 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0038 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0976 | 0.0236 | 0.4874 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0031 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2390 | 0.0644 | 0.6197 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0396 | - | 0.0405 |
| `cholesky/n128/b128` | 5.4873 | - | 6.2140 |
| `cholesky/n32/b1` | 0.0021 | - | 0.0020 |
| `cholesky/n32/b128` | 0.2580 | - | 0.2589 |
| `eigh/n128/b1` | 1.2721 | - | 1.1251 |
| `eigh/n128/b128` | 163.9902 | - | 147.9715 |
| `eigh/n32/b1` | 0.0653 | - | 0.0778 |
| `eigh/n32/b128` | 8.5461 | - | 9.9468 |
| `eigvalsh/n128/b1` | 0.7037 | - | 0.4985 |
| `eigvalsh/n128/b128` | 91.7875 | - | 64.8356 |
| `eigvalsh/n32/b1` | 0.0497 | - | 0.0289 |
| `eigvalsh/n32/b128` | 6.5250 | - | 3.7589 |
| `householder_apply/n128/b1` | 0.1311 | - | 0.2622 |
| `householder_apply/n128/b128` | 17.7783 | - | 34.2212 |
| `householder_apply/n32/b1` | 0.0112 | - | 0.0110 |
| `householder_apply/n32/b128` | 1.3927 | - | 1.3573 |
| `householder_factor/n128/b1` | 0.1055 | - | 0.2200 |
| `householder_factor/n128/b128` | 13.7673 | - | 28.6370 |
| `householder_factor/n32/b1` | 0.0076 | - | 0.0085 |
| `householder_factor/n32/b128` | 0.9541 | - | 1.0639 |
| `lu/n128/b1` | 0.0896 | - | 0.0872 |
| `lu/n128/b128` | 12.1276 | - | 13.6211 |
| `lu/n32/b1` | 0.0055 | - | 0.0050 |
| `lu/n32/b128` | 0.6357 | - | 0.6176 |
| `lu_factor/n128/b1` | 0.0559 | - | 0.0782 |
| `lu_factor/n128/b128` | 8.2369 | - | 11.1161 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0039 |
| `lu_factor/n32/b128` | 0.3817 | - | 0.4988 |
| `lu_factor_solve/n128/b1` | 0.0637 | - | 0.0902 |
| `lu_factor_solve/n128/b128` | 9.0037 | - | 12.3597 |
| `lu_factor_solve/n32/b1` | 0.0041 | - | 0.0056 |
| `lu_factor_solve/n32/b128` | 0.4816 | - | 0.7099 |
| `lu_solve_prepared/n128/b1` | 0.0058 | - | 0.0117 |
| `lu_solve_prepared/n128/b128` | 1.6011 | - | 2.7075 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0016 |
| `lu_solve_prepared/n32/b128` | 0.1139 | - | 0.2068 |
| `qr/n128/b1` | 0.3443 | - | 0.4361 |
| `qr/n128/b128` | 43.8655 | - | 57.0156 |
| `qr/n32/b1` | 0.0208 | - | 0.0159 |
| `qr/n32/b128` | 2.6163 | - | 2.0170 |
| `rank_revealing_qr/n128/b1` | 0.3488 | - | 0.4913 |
| `rank_revealing_qr/n128/b128` | 44.9734 | - | 64.6988 |
| `rank_revealing_qr/n32/b1` | 0.0210 | - | 0.0200 |
| `rank_revealing_qr/n32/b128` | 2.6050 | - | 2.5093 |
| `solve/n128/b1` | 0.0664 | - | 0.0937 |
| `solve/n128/b128` | 8.7649 | - | 12.7567 |
| `solve/n32/b1` | 0.0049 | - | 0.0062 |
| `solve/n32/b128` | 0.5377 | - | 0.7363 |
| `svd_thin/n128/b1` | 2.4218 | - | 2.0217 |
| `svd_thin/n128/b128` | 307.8163 | - | 264.6678 |
| `svd_thin/n32/b1` | 0.1179 | - | 0.1404 |
| `svd_thin/n32/b128` | 15.2468 | - | 17.8865 |
| `svd_values/n128/b1` | 1.4069 | - | 0.8120 |
| `svd_values/n128/b128` | 181.2872 | - | 106.3272 |
| `svd_values/n32/b1` | 0.0928 | - | 0.0459 |
| `svd_values/n32/b128` | 12.1148 | - | 5.9815 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0062 |
| `triangular_solve/n128/b128` | 1.1620 | - | 1.6092 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0010 |
| `triangular_solve/n32/b128` | 0.0899 | - | 0.1082 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0396 | 0.0496 | 0.0452 |
| `cholesky/n128/b128` | 6.0162 | 6.9721 | 6.8271 |
| `cholesky/n32/b1` | 0.0022 | 0.0043 | 0.0021 |
| `cholesky/n32/b128` | 0.2557 | 0.1325 | 0.2607 |
| `eigh/n128/b1` | 1.2571 | 1.2863 | 0.9099 |
| `eigh/n128/b128` | 162.6142 | 162.8973 | 115.3623 |
| `eigh/n32/b1` | 0.0642 | 0.0693 | 0.0706 |
| `eigh/n32/b128` | 8.4716 | 2.1437 | 9.0374 |
| `eigvalsh/n128/b1` | 0.6922 | 0.7015 | 0.4838 |
| `eigvalsh/n128/b128` | 90.5622 | 90.6248 | 62.0596 |
| `eigvalsh/n32/b1` | 0.0487 | 0.0524 | 0.0288 |
| `eigvalsh/n32/b128` | 6.4122 | 1.6298 | 3.7459 |
| `householder_apply/n128/b1` | 0.1295 | 0.1274 | 0.2337 |
| `householder_apply/n128/b128` | 17.3707 | 17.1030 | 31.7741 |
| `householder_apply/n32/b1` | 0.0109 | 0.0141 | 0.0112 |
| `householder_apply/n32/b128` | 1.3692 | 0.3452 | 1.3435 |
| `householder_factor/n128/b1` | 0.1051 | 0.1225 | 0.2290 |
| `householder_factor/n128/b128` | 13.8902 | 16.4841 | 30.3612 |
| `householder_factor/n32/b1` | 0.0073 | 0.0101 | 0.0085 |
| `householder_factor/n32/b128` | 0.9300 | 0.2412 | 1.0882 |
| `lu/n128/b1` | 0.0898 | 0.1057 | 0.0872 |
| `lu/n128/b128` | 12.1754 | 14.1329 | 13.5452 |
| `lu/n32/b1` | 0.0053 | 0.0089 | 0.0051 |
| `lu/n32/b128` | 0.6310 | 0.3177 | 0.6135 |
| `lu_factor/n128/b1` | 0.0574 | 0.0721 | 0.0779 |
| `lu_factor/n128/b128` | 8.2833 | 2.5235 | 11.0660 |
| `lu_factor/n32/b1` | 0.0032 | 0.0056 | 0.0039 |
| `lu_factor/n32/b128` | 0.3941 | 0.1175 | 0.5000 |
| `lu_factor_solve/n128/b1` | 0.0622 | 0.0775 | 0.0876 |
| `lu_factor_solve/n128/b128` | 8.9831 | 2.9926 | 12.3491 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0068 | 0.0054 |
| `lu_factor_solve/n32/b128` | 0.4962 | 0.1369 | 0.7199 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0087 | 0.0073 |
| `lu_solve_prepared/n128/b128` | 1.8794 | 0.5302 | 2.2423 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0026 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1135 | 0.0346 | 0.1457 |
| `qr/n128/b1` | 0.3452 | 0.6086 | 0.4590 |
| `qr/n128/b128` | 44.4400 | 79.1714 | 60.4927 |
| `qr/n32/b1` | 0.0208 | 0.0447 | 0.0160 |
| `qr/n32/b128` | 2.6068 | 0.6640 | 2.0248 |
| `rank_revealing_qr/n128/b1` | 0.3524 | 0.3696 | 0.5149 |
| `rank_revealing_qr/n128/b128` | 45.5951 | 48.5264 | 67.7185 |
| `rank_revealing_qr/n32/b1` | 0.0208 | 0.0478 | 0.0198 |
| `rank_revealing_qr/n32/b128` | 2.6267 | 1.3234 | 2.4784 |
| `solve/n128/b1` | 0.0663 | 0.0799 | 0.0928 |
| `solve/n128/b128` | 8.7909 | 10.4287 | 12.3924 |
| `solve/n32/b1` | 0.0047 | 0.0071 | 0.0058 |
| `solve/n32/b128` | 0.5200 | 0.2675 | 0.6950 |
| `svd_thin/n128/b1` | 2.4197 | 1.8196 | 2.0098 |
| `svd_thin/n128/b128` | 307.6739 | 231.5395 | 260.8716 |
| `svd_thin/n32/b1` | 0.1172 | 0.1218 | 0.1412 |
| `svd_thin/n32/b128` | 15.1062 | 6.0429 | 17.9114 |
| `svd_values/n128/b1` | 1.4087 | 1.4345 | 0.8347 |
| `svd_values/n128/b128` | 179.9956 | 180.1467 | 108.3083 |
| `svd_values/n32/b1` | 0.0928 | 0.0969 | 0.0463 |
| `svd_values/n32/b128` | 11.9614 | 6.0093 | 5.9923 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0068 | 0.0038 |
| `triangular_solve/n128/b128` | 0.9548 | 1.1157 | 1.2313 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0035 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0879 | 0.0265 | 0.1049 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0373 | 0.0544 | 0.0467 |
| `cholesky/n128/b128` | 5.9848 | 7.2874 | 6.9976 |
| `cholesky/n32/b1` | 0.0021 | 0.0052 | 0.0021 |
| `cholesky/n32/b128` | 0.2529 | 0.0682 | 0.2641 |
| `eigh/n128/b1` | 1.2621 | 1.2360 | 0.8525 |
| `eigh/n128/b128` | 161.8930 | 159.9924 | 112.7440 |
| `eigh/n32/b1` | 0.0649 | 0.0695 | 0.0712 |
| `eigh/n32/b128` | 8.4687 | 2.1666 | 8.8046 |
| `eigvalsh/n128/b1` | 0.6912 | 0.7037 | 0.4740 |
| `eigvalsh/n128/b128` | 90.2821 | 90.2146 | 61.5889 |
| `eigvalsh/n32/b1` | 0.0490 | 0.0518 | 0.0295 |
| `eigvalsh/n32/b128` | 6.4678 | 1.6506 | 3.7593 |
| `householder_apply/n128/b1` | 0.1296 | 0.1861 | 0.2349 |
| `householder_apply/n128/b128` | 17.7513 | 24.8386 | 31.0181 |
| `householder_apply/n32/b1` | 0.0108 | 0.0134 | 0.0110 |
| `householder_apply/n32/b128` | 1.3672 | 0.3497 | 1.3400 |
| `householder_factor/n128/b1` | 0.1036 | 0.1660 | 0.2263 |
| `householder_factor/n128/b128` | 13.7133 | 22.5205 | 29.8012 |
| `householder_factor/n32/b1` | 0.0073 | 0.0100 | 0.0085 |
| `householder_factor/n32/b128` | 0.9413 | 0.2400 | 1.0843 |
| `lu/n128/b1` | 0.0904 | 0.1186 | 0.0871 |
| `lu/n128/b128` | 12.3259 | 15.4825 | 13.5713 |
| `lu/n32/b1` | 0.0055 | 0.0083 | 0.0051 |
| `lu/n32/b128` | 0.6345 | 0.1642 | 0.6247 |
| `lu_factor/n128/b1` | 0.0575 | 0.0848 | 0.0786 |
| `lu_factor/n128/b128` | 8.2423 | 2.5989 | 11.2290 |
| `lu_factor/n32/b1` | 0.0033 | 0.0060 | 0.0039 |
| `lu_factor/n32/b128` | 0.3854 | 0.1071 | 0.5037 |
| `lu_factor_solve/n128/b1` | 0.0633 | 0.0881 | 0.0886 |
| `lu_factor_solve/n128/b128` | 8.8545 | 1.6061 | 12.2925 |
| `lu_factor_solve/n32/b1` | 0.0043 | 0.0074 | 0.0053 |
| `lu_factor_solve/n32/b128` | 0.4941 | 0.1349 | 0.7376 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0089 | 0.0074 |
| `lu_solve_prepared/n128/b128` | 2.0868 | 0.5235 | 2.0390 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0037 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1144 | 0.0340 | 0.1606 |
| `qr/n128/b1` | 0.3446 | 0.9290 | 0.4519 |
| `qr/n128/b128` | 44.4283 | 123.1714 | 59.2792 |
| `qr/n32/b1` | 0.0209 | 0.0658 | 0.0160 |
| `qr/n32/b128` | 2.6053 | 0.3567 | 2.0121 |
| `rank_revealing_qr/n128/b1` | 0.3525 | 0.4460 | 0.5166 |
| `rank_revealing_qr/n128/b128` | 45.2990 | 56.8350 | 68.0340 |
| `rank_revealing_qr/n32/b1` | 0.0209 | 0.0663 | 0.0199 |
| `rank_revealing_qr/n32/b128` | 2.6423 | 0.6601 | 2.4827 |
| `solve/n128/b1` | 0.0657 | 0.0921 | 0.0922 |
| `solve/n128/b128` | 8.6589 | 11.8491 | 12.3404 |
| `solve/n32/b1` | 0.0048 | 0.0078 | 0.0058 |
| `solve/n32/b128` | 0.5284 | 0.0736 | 0.7266 |
| `svd_thin/n128/b1` | 2.4271 | 1.8476 | 1.9836 |
| `svd_thin/n128/b128` | 309.4838 | 238.6979 | 256.8254 |
| `svd_thin/n32/b1` | 0.1171 | 0.1220 | 0.1391 |
| `svd_thin/n32/b128` | 15.1632 | 2.0633 | 17.8265 |
| `svd_values/n128/b1` | 1.4155 | 1.4335 | 0.8106 |
| `svd_values/n128/b128` | 181.6985 | 180.0796 | 106.7175 |
| `svd_values/n32/b1` | 0.0925 | 0.0968 | 0.0455 |
| `svd_values/n32/b128` | 11.9507 | 3.0225 | 5.9194 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0072 | 0.0040 |
| `triangular_solve/n128/b128` | 0.8921 | 0.8872 | 1.2451 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0031 | 0.0008 |
| `triangular_solve/n32/b128` | 0.0880 | 0.0258 | 0.1049 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1065 | - | 0.1075 |
| `cholesky/n128/b128` | 16.0768 | - | 15.5498 |
| `cholesky/n32/b1` | 0.0034 | - | 0.0034 |
| `cholesky/n32/b128` | 0.4231 | - | 0.4377 |
| `eigh/n128/b1` | 1.8540 | - | 3.2663 |
| `eigh/n128/b128` | 241.0656 | - | 422.1582 |
| `eigh/n32/b1` | 0.0810 | - | 0.1085 |
| `eigh/n32/b128` | 10.5739 | - | 14.0846 |
| `eigvalsh/n128/b1` | 0.9285 | - | 0.9483 |
| `eigvalsh/n128/b128` | 121.4433 | - | 123.5446 |
| `eigvalsh/n32/b1` | 0.0523 | - | 0.0419 |
| `eigvalsh/n32/b128` | 6.9003 | - | 5.4238 |
| `householder_apply/n128/b1` | 0.4838 | - | 0.6886 |
| `householder_apply/n128/b128` | 64.4387 | - | 91.9745 |
| `householder_apply/n32/b1` | 0.0150 | - | 0.0197 |
| `householder_apply/n32/b128` | 1.8954 | - | 2.4820 |
| `householder_factor/n128/b1` | 0.3498 | - | 0.4363 |
| `householder_factor/n128/b128` | 45.6902 | - | 57.9227 |
| `householder_factor/n32/b1` | 0.0116 | - | 0.0160 |
| `householder_factor/n32/b128` | 1.4881 | - | 2.0017 |
| `lu/n128/b1` | 0.2045 | - | 0.2137 |
| `lu/n128/b128` | 27.6216 | - | 31.5650 |
| `lu/n32/b1` | 0.0079 | - | 0.0081 |
| `lu/n32/b128` | 1.0155 | - | 1.1104 |
| `lu_factor/n128/b1` | 0.1563 | - | 0.1921 |
| `lu_factor/n128/b128` | 21.8968 | - | 25.6059 |
| `lu_factor/n32/b1` | 0.0055 | - | 0.0063 |
| `lu_factor/n32/b128` | 0.6519 | - | 0.8170 |
| `lu_factor_solve/n128/b1` | 0.1765 | - | 0.2224 |
| `lu_factor_solve/n128/b128` | 24.3894 | - | 29.2890 |
| `lu_factor_solve/n32/b1` | 0.0075 | - | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9278 | - | 1.1186 |
| `lu_solve_prepared/n128/b1` | 0.0188 | - | 0.0289 |
| `lu_solve_prepared/n128/b128` | 4.2307 | - | 5.1593 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.2794 | - | 0.3069 |
| `qr/n128/b1` | 0.9573 | - | 0.8693 |
| `qr/n128/b128` | 124.9873 | - | 113.5308 |
| `qr/n32/b1` | 0.0423 | - | 0.0290 |
| `qr/n32/b128` | 5.3785 | - | 3.6523 |
| `rank_revealing_qr/n128/b1` | 1.0048 | - | 0.9927 |
| `rank_revealing_qr/n128/b128` | 130.3740 | - | 131.9587 |
| `rank_revealing_qr/n32/b1` | 0.0394 | - | 0.0366 |
| `rank_revealing_qr/n32/b128` | 5.0302 | - | 4.8827 |
| `solve/n128/b1` | 0.1810 | - | 0.2241 |
| `solve/n128/b128` | 23.8705 | - | 29.9173 |
| `solve/n32/b1` | 0.0083 | - | 0.0095 |
| `solve/n32/b128` | 0.9759 | - | 1.1710 |
| `svd_thin/n128/b1` | 3.9219 | - | 3.5254 |
| `svd_thin/n128/b128` | 508.9096 | - | 456.9253 |
| `svd_thin/n32/b1` | 0.1508 | - | 0.1691 |
| `svd_thin/n32/b128` | 19.6477 | - | 22.2206 |
| `svd_values/n128/b1` | 1.8865 | - | 1.4189 |
| `svd_values/n128/b128` | 245.2740 | - | 179.5517 |
| `svd_values/n32/b1` | 0.1012 | - | 0.0649 |
| `svd_values/n32/b128` | 13.3571 | - | 8.4016 |
| `triangular_solve/n128/b1` | 0.0110 | - | 0.0133 |
| `triangular_solve/n128/b128` | 2.2838 | - | 2.9623 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0014 |
| `triangular_solve/n32/b128` | 0.1928 | - | 0.1604 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1091 | 0.1107 | 0.0800 |
| `cholesky/n128/b128` | 16.1238 | 15.8333 | 11.1124 |
| `cholesky/n32/b1` | 0.0034 | 0.0064 | 0.0034 |
| `cholesky/n32/b128` | 0.4302 | 0.2189 | 0.4415 |
| `eigh/n128/b1` | 1.8561 | 1.7651 | 3.1600 |
| `eigh/n128/b128` | 242.1516 | 210.1593 | 408.1861 |
| `eigh/n32/b1` | 0.0807 | 0.0859 | 0.1085 |
| `eigh/n32/b128` | 10.5170 | 3.2540 | 13.9074 |
| `eigvalsh/n128/b1` | 0.9284 | 0.9311 | 0.8853 |
| `eigvalsh/n128/b128` | 121.8281 | 121.1582 | 115.3701 |
| `eigvalsh/n32/b1` | 0.0524 | 0.0568 | 0.0419 |
| `eigvalsh/n32/b128` | 6.8906 | 1.7493 | 5.4983 |
| `householder_apply/n128/b1` | 0.4853 | 0.2585 | 0.3692 |
| `householder_apply/n128/b128` | 64.2190 | 34.9673 | 50.0827 |
| `householder_apply/n32/b1` | 0.0145 | 0.0176 | 0.0197 |
| `householder_apply/n32/b128` | 1.8515 | 0.9314 | 2.5064 |
| `householder_factor/n128/b1` | 0.3516 | 0.2289 | 0.3897 |
| `householder_factor/n128/b128` | 45.6852 | 29.4138 | 50.4789 |
| `householder_factor/n32/b1` | 0.0115 | 0.0138 | 0.0157 |
| `householder_factor/n32/b128` | 1.4509 | 0.7448 | 2.0069 |
| `lu/n128/b1` | 0.1960 | 0.1886 | 0.1445 |
| `lu/n128/b128` | 28.0431 | 25.7913 | 21.7626 |
| `lu/n32/b1` | 0.0078 | 0.0106 | 0.0081 |
| `lu/n32/b128` | 1.0238 | 0.2527 | 1.1102 |
| `lu_factor/n128/b1` | 0.1559 | 0.1495 | 0.1187 |
| `lu_factor/n128/b128` | 21.8624 | 6.1896 | 15.5635 |
| `lu_factor/n32/b1` | 0.0054 | 0.0084 | 0.0064 |
| `lu_factor/n32/b128` | 0.6483 | 0.3382 | 0.8215 |
| `lu_factor_solve/n128/b1` | 0.1748 | 0.1662 | 0.1386 |
| `lu_factor_solve/n128/b128` | 24.3208 | 6.5721 | 18.1129 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0107 | 0.0087 |
| `lu_factor_solve/n32/b128` | 0.9288 | 0.4800 | 1.1228 |
| `lu_solve_prepared/n128/b1` | 0.0189 | 0.0222 | 0.0180 |
| `lu_solve_prepared/n128/b128` | 4.2756 | 2.3029 | 4.1308 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0045 | 0.0018 |
| `lu_solve_prepared/n32/b128` | 0.2846 | 0.0765 | 0.2326 |
| `qr/n128/b1` | 0.9707 | 0.8581 | 0.7740 |
| `qr/n128/b128` | 125.2289 | 111.4092 | 100.8582 |
| `qr/n32/b1` | 0.0426 | 0.0693 | 0.0285 |
| `qr/n32/b128` | 5.4494 | 1.9264 | 3.7522 |
| `rank_revealing_qr/n128/b1` | 1.0168 | 0.7951 | 0.9119 |
| `rank_revealing_qr/n128/b128` | 130.6896 | 103.8066 | 121.3967 |
| `rank_revealing_qr/n32/b1` | 0.0395 | 0.0656 | 0.0366 |
| `rank_revealing_qr/n32/b128` | 5.0059 | 1.2643 | 4.8491 |
| `solve/n128/b1` | 0.1805 | 0.1714 | 0.1505 |
| `solve/n128/b128` | 23.8617 | 22.1322 | 19.3178 |
| `solve/n32/b1` | 0.0082 | 0.0111 | 0.0094 |
| `solve/n32/b128` | 0.9724 | 0.4904 | 1.1793 |
| `svd_thin/n128/b1` | 3.9250 | 2.7036 | 3.0178 |
| `svd_thin/n128/b128` | 508.3222 | 349.3424 | 392.5873 |
| `svd_thin/n32/b1` | 0.1502 | 0.1543 | 0.1666 |
| `svd_thin/n32/b128` | 19.6190 | 8.1438 | 22.1041 |
| `svd_values/n128/b1` | 1.8860 | 1.9043 | 1.5195 |
| `svd_values/n128/b128` | 245.0676 | 243.3150 | 193.5009 |
| `svd_values/n32/b1` | 0.1011 | 0.1056 | 0.0635 |
| `svd_values/n32/b128` | 13.3033 | 4.1744 | 8.2223 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0137 | 0.0080 |
| `triangular_solve/n128/b128` | 2.3528 | 2.4459 | 2.4765 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0037 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1912 | 0.0510 | 0.1726 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1075 | 0.1141 | 0.0949 |
| `cholesky/n128/b128` | 16.0337 | 16.2145 | 13.8278 |
| `cholesky/n32/b1` | 0.0034 | 0.0063 | 0.0034 |
| `cholesky/n32/b128` | 0.4108 | 0.0571 | 0.4381 |
| `eigh/n128/b1` | 1.8519 | 1.6258 | 3.1672 |
| `eigh/n128/b128` | 241.7505 | 211.9440 | 408.4856 |
| `eigh/n32/b1` | 0.0803 | 0.0856 | 0.1081 |
| `eigh/n32/b128` | 10.5059 | 1.3456 | 13.9733 |
| `eigvalsh/n128/b1` | 0.9312 | 0.9368 | 0.8894 |
| `eigvalsh/n128/b128` | 121.6874 | 120.8504 | 115.2360 |
| `eigvalsh/n32/b1` | 0.0524 | 0.0559 | 0.0420 |
| `eigvalsh/n32/b128` | 6.9332 | 0.8885 | 5.4533 |
| `householder_apply/n128/b1` | 0.4752 | 0.3273 | 0.3226 |
| `householder_apply/n128/b128` | 64.5159 | 44.6957 | 44.5994 |
| `householder_apply/n32/b1` | 0.0147 | 0.0183 | 0.0197 |
| `householder_apply/n32/b128` | 1.8777 | 0.4727 | 2.4719 |
| `householder_factor/n128/b1` | 0.3446 | 0.2817 | 0.3798 |
| `householder_factor/n128/b128` | 45.6215 | 36.9859 | 49.8230 |
| `householder_factor/n32/b1` | 0.0117 | 0.0142 | 0.0158 |
| `householder_factor/n32/b128` | 1.4548 | 0.3696 | 1.9843 |
| `lu/n128/b1` | 0.1981 | 0.1963 | 0.1371 |
| `lu/n128/b128` | 27.7452 | 28.8386 | 21.5419 |
| `lu/n32/b1` | 0.0078 | 0.0109 | 0.0080 |
| `lu/n32/b128` | 1.0256 | 0.2329 | 1.1905 |
| `lu_factor/n128/b1` | 0.1551 | 0.1519 | 0.1122 |
| `lu_factor/n128/b128` | 21.8948 | 3.2572 | 14.7687 |
| `lu_factor/n32/b1` | 0.0053 | 0.0086 | 0.0065 |
| `lu_factor/n32/b128` | 0.6502 | 0.1737 | 0.8320 |
| `lu_factor_solve/n128/b1` | 0.1740 | 0.1710 | 0.1301 |
| `lu_factor_solve/n128/b128` | 24.2695 | 3.6154 | 17.6742 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0101 | 0.0087 |
| `lu_factor_solve/n32/b128` | 0.9226 | 0.1311 | 1.1451 |
| `lu_solve_prepared/n128/b1` | 0.0188 | 0.0218 | 0.0151 |
| `lu_solve_prepared/n128/b128` | 4.2058 | 0.9294 | 4.0496 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0054 | 0.0021 |
| `lu_solve_prepared/n32/b128` | 0.2871 | 0.0482 | 0.2328 |
| `qr/n128/b1` | 0.9679 | 1.1881 | 0.7670 |
| `qr/n128/b128` | 125.1632 | 155.1750 | 100.0050 |
| `qr/n32/b1` | 0.0423 | 0.0867 | 0.0286 |
| `qr/n32/b128` | 5.4423 | 0.6933 | 3.6403 |
| `rank_revealing_qr/n128/b1` | 1.0102 | 0.8738 | 0.9037 |
| `rank_revealing_qr/n128/b128` | 130.4418 | 114.2305 | 120.0029 |
| `rank_revealing_qr/n32/b1` | 0.0393 | 0.0864 | 0.0365 |
| `rank_revealing_qr/n32/b128` | 4.9935 | 0.6402 | 4.8317 |
| `solve/n128/b1` | 0.1800 | 0.1792 | 0.1391 |
| `solve/n128/b128` | 23.9190 | 23.4777 | 19.4522 |
| `solve/n32/b1` | 0.0081 | 0.0105 | 0.0094 |
| `solve/n32/b128` | 0.9623 | 0.2475 | 1.3226 |
| `svd_thin/n128/b1` | 3.9239 | 2.7494 | 3.0043 |
| `svd_thin/n128/b128` | 506.0867 | 356.9959 | 388.5895 |
| `svd_thin/n32/b1` | 0.1510 | 0.1562 | 0.1674 |
| `svd_thin/n32/b128` | 19.9250 | 2.5647 | 22.1005 |
| `svd_values/n128/b1` | 1.8765 | 1.9102 | 1.5890 |
| `svd_values/n128/b128` | 243.9478 | 243.0059 | 203.8928 |
| `svd_values/n32/b1` | 0.1008 | 0.1049 | 0.0634 |
| `svd_values/n32/b128` | 13.3257 | 2.4334 | 8.2243 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0165 | 0.0089 |
| `triangular_solve/n128/b128` | 2.2052 | 2.1380 | 2.5194 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0050 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1895 | 0.0494 | 0.1689 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1963 | - | 0.2319 |
| `cholesky/n256/b4` | 0.7996 | - | 0.9334 |
| `cholesky/n512/b1` | 1.2556 | - | 1.5725 |
| `cholesky/n512/b4` | 5.6356 | - | 6.6093 |
| `eigh/n256/b1` | 5.5727 | - | 5.3767 |
| `eigh/n256/b4` | 22.3104 | - | 21.4933 |
| `eigh/n512/b1` | 28.6253 | - | 30.2676 |
| `eigh/n512/b4` | 115.5761 | - | 121.7069 |
| `eigvalsh/n256/b1` | 2.9302 | - | 2.4731 |
| `eigvalsh/n256/b4` | 12.2333 | - | 9.8401 |
| `eigvalsh/n512/b1` | 14.1510 | - | 14.2081 |
| `eigvalsh/n512/b4` | 57.3883 | - | 56.6694 |
| `householder_apply/n256/b1` | 0.8261 | - | 1.6366 |
| `householder_apply/n256/b4` | 3.3384 | - | 6.6081 |
| `householder_apply/n512/b1` | 6.1217 | - | 11.7313 |
| `householder_apply/n512/b4` | 24.6303 | - | 47.3843 |
| `householder_factor/n256/b1` | 0.6249 | - | 1.0966 |
| `householder_factor/n256/b4` | 2.4953 | - | 4.3980 |
| `householder_factor/n512/b1` | 4.3478 | - | 7.4145 |
| `householder_factor/n512/b4` | 17.5099 | - | 29.6838 |
| `lu/n256/b1` | 0.4752 | - | 0.4838 |
| `lu/n256/b4` | 1.9629 | - | 2.0640 |
| `lu/n512/b1` | 3.2771 | - | 3.1878 |
| `lu/n512/b4` | 12.8985 | - | 13.0927 |
| `lu_factor/n256/b1` | 0.3545 | - | 0.4454 |
| `lu_factor/n256/b4` | 1.5276 | - | 1.7824 |
| `lu_factor/n512/b1` | 2.8266 | - | 2.8870 |
| `lu_factor/n512/b4` | 11.7739 | - | 11.8117 |
| `lu_factor_solve/n256/b1` | 0.3717 | - | 0.4869 |
| `lu_factor_solve/n256/b4` | 1.4924 | - | 1.9464 |
| `lu_factor_solve/n512/b1` | 2.8868 | - | 3.0329 |
| `lu_factor_solve/n512/b4` | 11.9797 | - | 12.3806 |
| `lu_solve_prepared/n256/b1` | 0.0170 | - | 0.0427 |
| `lu_solve_prepared/n256/b4` | 0.0783 | - | 0.1837 |
| `lu_solve_prepared/n512/b1` | 0.0622 | - | 0.1432 |
| `lu_solve_prepared/n512/b4` | 0.4372 | - | 1.0350 |
| `qr/n256/b1` | 1.8481 | - | 2.1843 |
| `qr/n256/b4` | 7.4176 | - | 8.8154 |
| `qr/n512/b1` | 11.5097 | - | 14.8060 |
| `qr/n512/b4` | 46.1211 | - | 60.1591 |
| `rank_revealing_qr/n256/b1` | 2.1149 | - | 2.6191 |
| `rank_revealing_qr/n256/b4` | 8.5208 | - | 10.6544 |
| `rank_revealing_qr/n512/b1` | 14.8078 | - | 18.6971 |
| `rank_revealing_qr/n512/b4` | 59.4081 | - | 75.9403 |
| `solve/n256/b1` | 0.3857 | - | 0.4937 |
| `solve/n256/b4` | 1.5483 | - | 1.9973 |
| `solve/n512/b1` | 2.8473 | - | 3.0562 |
| `solve/n512/b4` | 11.3574 | - | 12.3720 |
| `svd_thin/n256/b1` | 12.2120 | - | 11.1222 |
| `svd_thin/n256/b4` | 48.8376 | - | 44.1911 |
| `svd_thin/n512/b1` | 70.8001 | - | 72.6147 |
| `svd_thin/n512/b4` | 282.6542 | - | 290.4044 |
| `svd_values/n256/b1` | 6.9634 | - | 4.5740 |
| `svd_values/n256/b4` | 27.7066 | - | 18.6757 |
| `svd_values/n512/b1` | 38.7395 | - | 31.1151 |
| `svd_values/n512/b4` | 155.0372 | - | 127.0505 |
| `triangular_solve/n256/b1` | 0.0106 | - | 0.0203 |
| `triangular_solve/n256/b4` | 0.0465 | - | 0.0845 |
| `triangular_solve/n512/b1` | 0.0342 | - | 0.0755 |
| `triangular_solve/n512/b4` | 0.1370 | - | 0.3512 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1955 | 0.1809 | 0.1554 |
| `cholesky/n256/b4` | 0.7977 | 0.7813 | 0.6371 |
| `cholesky/n512/b1` | 1.2812 | 0.8071 | 0.7583 |
| `cholesky/n512/b4` | 5.7276 | 3.6595 | 3.4408 |
| `eigh/n256/b1` | 5.6154 | 4.2279 | 3.5969 |
| `eigh/n256/b4` | 22.6025 | 17.0027 | 14.3290 |
| `eigh/n512/b1` | 28.5998 | 15.9841 | 16.2272 |
| `eigh/n512/b4` | 114.9038 | 63.9046 | 65.4523 |
| `eigvalsh/n256/b1` | 2.9610 | 3.0144 | 1.9114 |
| `eigvalsh/n256/b4` | 11.7961 | 12.1552 | 7.6551 |
| `eigvalsh/n512/b1` | 14.0557 | 11.9536 | 7.5101 |
| `eigvalsh/n512/b4` | 57.1945 | 47.8533 | 30.2351 |
| `householder_apply/n256/b1` | 0.8237 | 0.2968 | 1.1100 |
| `householder_apply/n256/b4` | 3.3321 | 1.1922 | 4.4865 |
| `householder_apply/n512/b1` | 6.1747 | 1.7036 | 6.8551 |
| `householder_apply/n512/b4` | 24.8786 | 7.0685 | 27.7874 |
| `householder_factor/n256/b1` | 0.6206 | 0.3225 | 0.8521 |
| `householder_factor/n256/b4` | 2.4977 | 1.2815 | 3.4276 |
| `householder_factor/n512/b1` | 4.3608 | 1.5739 | 4.5204 |
| `householder_factor/n512/b4` | 17.5556 | 6.3852 | 18.2876 |
| `lu/n256/b1` | 0.4945 | 0.4467 | 0.2862 |
| `lu/n256/b4` | 1.9963 | 1.8193 | 1.2547 |
| `lu/n512/b1` | 3.2202 | 1.9546 | 1.6706 |
| `lu/n512/b4` | 12.8795 | 7.7431 | 6.9877 |
| `lu_factor/n256/b1` | 0.3538 | 0.3129 | 0.2411 |
| `lu_factor/n256/b4` | 1.5238 | 0.7748 | 0.9709 |
| `lu_factor/n512/b1` | 2.8244 | 1.4718 | 1.3625 |
| `lu_factor/n512/b4` | 11.7567 | 5.9919 | 5.5413 |
| `lu_factor_solve/n256/b1` | 0.3720 | 0.3330 | 0.2710 |
| `lu_factor_solve/n256/b4` | 1.4983 | 0.3938 | 1.0994 |
| `lu_factor_solve/n512/b1` | 2.8986 | 1.5344 | 1.4745 |
| `lu_factor_solve/n512/b4` | 11.9982 | 3.7148 | 6.1467 |
| `lu_solve_prepared/n256/b1` | 0.0172 | 0.0236 | 0.0265 |
| `lu_solve_prepared/n256/b4` | 0.0824 | 0.0244 | 0.1289 |
| `lu_solve_prepared/n512/b1` | 0.0719 | 0.0646 | 0.0963 |
| `lu_solve_prepared/n512/b4` | 0.4353 | 0.2017 | 0.8508 |
| `qr/n256/b1` | 1.8559 | 1.7626 | 1.6893 |
| `qr/n256/b4` | 7.3917 | 7.0575 | 6.7872 |
| `qr/n512/b1` | 11.4841 | 6.0239 | 9.0662 |
| `qr/n512/b4` | 46.3038 | 24.0329 | 36.8211 |
| `rank_revealing_qr/n256/b1` | 2.1262 | 1.4601 | 2.3199 |
| `rank_revealing_qr/n256/b4` | 8.4001 | 5.8416 | 9.3975 |
| `rank_revealing_qr/n512/b1` | 14.7294 | 6.1466 | 14.7333 |
| `rank_revealing_qr/n512/b4` | 59.9490 | 24.5372 | 59.5126 |
| `solve/n256/b1` | 0.3834 | 0.3737 | 0.2829 |
| `solve/n256/b4` | 1.5362 | 1.4120 | 1.1486 |
| `solve/n512/b1` | 2.8646 | 1.5570 | 1.5297 |
| `solve/n512/b4` | 11.3942 | 6.2641 | 6.1860 |
| `svd_thin/n256/b1` | 12.2806 | 8.7629 | 9.3493 |
| `svd_thin/n256/b4` | 48.9593 | 35.7080 | 37.4881 |
| `svd_thin/n512/b1` | 70.6943 | 40.5454 | 55.2993 |
| `svd_thin/n512/b4` | 282.0805 | 162.3153 | 219.6351 |
| `svd_values/n256/b1` | 6.9394 | 7.0470 | 4.4275 |
| `svd_values/n256/b4` | 27.8035 | 28.1932 | 17.9755 |
| `svd_values/n512/b1` | 38.7398 | 31.7735 | 28.6324 |
| `svd_values/n512/b4` | 155.0221 | 126.6696 | 116.0350 |
| `triangular_solve/n256/b1` | 0.0106 | 0.0155 | 0.0128 |
| `triangular_solve/n256/b4` | 0.0454 | 0.0581 | 0.0606 |
| `triangular_solve/n512/b1` | 0.0343 | 0.0364 | 0.0505 |
| `triangular_solve/n512/b4` | 0.1581 | 0.1478 | 0.2738 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1984 | 0.1951 | 0.1594 |
| `cholesky/n256/b4` | 0.8061 | 0.8264 | 0.6480 |
| `cholesky/n512/b1` | 1.3073 | 0.7218 | 0.6843 |
| `cholesky/n512/b4` | 5.6248 | 3.2693 | 3.0865 |
| `eigh/n256/b1` | 5.6180 | 4.1645 | 3.3176 |
| `eigh/n256/b4` | 22.5331 | 16.8917 | 13.4930 |
| `eigh/n512/b1` | 28.6551 | 14.8957 | 14.1525 |
| `eigh/n512/b4` | 114.5570 | 59.8530 | 56.9695 |
| `eigvalsh/n256/b1` | 2.9656 | 2.9589 | 1.8727 |
| `eigvalsh/n256/b4` | 11.7385 | 11.9106 | 7.4931 |
| `eigvalsh/n512/b1` | 14.0167 | 11.3813 | 6.7675 |
| `eigvalsh/n512/b4` | 57.1363 | 46.3207 | 27.0976 |
| `householder_apply/n256/b1` | 0.8275 | 0.3569 | 1.0567 |
| `householder_apply/n256/b4` | 3.3202 | 1.4315 | 4.1882 |
| `householder_apply/n512/b1` | 6.1569 | 1.7194 | 6.0099 |
| `householder_apply/n512/b4` | 24.9648 | 7.0993 | 24.7309 |
| `householder_factor/n256/b1` | 0.6253 | 0.3989 | 0.8418 |
| `householder_factor/n256/b4` | 2.4681 | 1.5463 | 3.2956 |
| `householder_factor/n512/b1` | 4.3543 | 1.6194 | 4.0754 |
| `householder_factor/n512/b4` | 17.4855 | 6.5941 | 16.2974 |
| `lu/n256/b1` | 0.4755 | 0.4606 | 0.2471 |
| `lu/n256/b4` | 1.9703 | 1.9730 | 1.0844 |
| `lu/n512/b1` | 3.2844 | 2.0028 | 1.1578 |
| `lu/n512/b4` | 12.9236 | 7.9246 | 4.8546 |
| `lu_factor/n256/b1` | 0.3804 | 0.3642 | 0.2048 |
| `lu_factor/n256/b4` | 1.5392 | 1.4656 | 0.8265 |
| `lu_factor/n512/b1` | 2.8430 | 1.5214 | 0.8522 |
| `lu_factor/n512/b4` | 11.7789 | 6.2580 | 3.4613 |
| `lu_factor_solve/n256/b1` | 0.3965 | 0.3863 | 0.2379 |
| `lu_factor_solve/n256/b4` | 1.4836 | 1.4911 | 0.9427 |
| `lu_factor_solve/n512/b1` | 2.9017 | 1.5819 | 0.9677 |
| `lu_factor_solve/n512/b4` | 12.0219 | 6.5228 | 3.9496 |
| `lu_solve_prepared/n256/b1` | 0.0172 | 0.0292 | 0.0262 |
| `lu_solve_prepared/n256/b4` | 0.0756 | 0.1083 | 0.1228 |
| `lu_solve_prepared/n512/b1` | 0.0735 | 0.0801 | 0.1085 |
| `lu_solve_prepared/n512/b4` | 0.3777 | 0.3875 | 0.7801 |
| `qr/n256/b1` | 1.8577 | 2.3535 | 1.6673 |
| `qr/n256/b4` | 7.4146 | 9.5949 | 6.7318 |
| `qr/n512/b1` | 11.5423 | 6.8353 | 8.1441 |
| `qr/n512/b4` | 46.1201 | 27.5853 | 32.7820 |
| `rank_revealing_qr/n256/b1` | 2.1370 | 1.5478 | 2.3084 |
| `rank_revealing_qr/n256/b4` | 8.3782 | 6.1447 | 9.3050 |
| `rank_revealing_qr/n512/b1` | 14.7443 | 5.7088 | 13.8067 |
| `rank_revealing_qr/n512/b4` | 58.8765 | 22.6379 | 56.6137 |
| `solve/n256/b1` | 0.3868 | 0.4203 | 0.2532 |
| `solve/n256/b4` | 1.5334 | 1.6077 | 1.0160 |
| `solve/n512/b1` | 2.8467 | 1.6314 | 1.0298 |
| `solve/n512/b4` | 11.3453 | 6.5691 | 4.2666 |
| `svd_thin/n256/b1` | 12.2350 | 8.9943 | 9.2045 |
| `svd_thin/n256/b4` | 48.9095 | 35.9081 | 36.8342 |
| `svd_thin/n512/b1` | 70.9622 | 38.9914 | 52.1647 |
| `svd_thin/n512/b4` | 282.6054 | 154.0504 | 210.6960 |
| `svd_values/n256/b1` | 6.9466 | 7.1871 | 4.4581 |
| `svd_values/n256/b4` | 27.7350 | 28.7884 | 18.0385 |
| `svd_values/n512/b1` | 38.7721 | 32.2827 | 28.3525 |
| `svd_values/n512/b4` | 154.7103 | 128.2200 | 116.2287 |
| `triangular_solve/n256/b1` | 0.0106 | 0.0190 | 0.0128 |
| `triangular_solve/n256/b4` | 0.0437 | 0.0620 | 0.0619 |
| `triangular_solve/n512/b1` | 0.0365 | 0.0429 | 0.0553 |
| `triangular_solve/n512/b4` | 0.1728 | 0.1788 | 0.3221 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7065 | - | 0.7639 |
| `cholesky/n256/b4` | 2.7866 | - | 3.0625 |
| `cholesky/n512/b1` | 4.7489 | - | 5.4295 |
| `cholesky/n512/b4` | 19.7437 | - | 22.6383 |
| `eigh/n256/b1` | 10.2502 | - | 21.6433 |
| `eigh/n256/b4` | 41.3815 | - | 86.2636 |
| `eigh/n512/b1` | 63.1485 | - | 157.7829 |
| `eigh/n512/b4` | 252.9922 | - | 631.2049 |
| `eigvalsh/n256/b1` | 4.9834 | - | 5.6356 |
| `eigvalsh/n256/b4` | 19.9373 | - | 22.6047 |
| `eigvalsh/n512/b1` | 29.6037 | - | 37.3917 |
| `eigvalsh/n512/b4` | 118.5833 | - | 150.2387 |
| `householder_apply/n256/b1` | 3.3654 | - | 4.7403 |
| `householder_apply/n256/b4` | 13.5837 | - | 19.1444 |
| `householder_apply/n512/b1` | 24.5730 | - | 32.2338 |
| `householder_apply/n512/b4` | 97.0643 | - | 129.1264 |
| `householder_factor/n256/b1` | 2.3661 | - | 3.0034 |
| `householder_factor/n256/b4` | 9.4059 | - | 12.0355 |
| `householder_factor/n512/b1` | 16.7179 | - | 20.7833 |
| `householder_factor/n512/b4` | 67.2940 | - | 83.7415 |
| `lu/n256/b1` | 1.2537 | - | 1.4202 |
| `lu/n256/b4` | 5.0973 | - | 5.9583 |
| `lu/n512/b1` | 8.7022 | - | 10.2733 |
| `lu/n512/b4` | 34.7945 | - | 41.2475 |
| `lu_factor/n256/b1` | 1.1154 | - | 1.3357 |
| `lu_factor/n256/b4` | 4.5103 | - | 5.3444 |
| `lu_factor/n512/b1` | 8.0240 | - | 9.5247 |
| `lu_factor/n512/b4` | 32.7410 | - | 38.2504 |
| `lu_factor_solve/n256/b1` | 1.1826 | - | 1.4560 |
| `lu_factor_solve/n256/b4` | 4.7734 | - | 5.7837 |
| `lu_factor_solve/n512/b1` | 8.2272 | - | 9.9782 |
| `lu_factor_solve/n512/b4` | 33.7502 | - | 40.0849 |
| `lu_solve_prepared/n256/b1` | 0.0632 | - | 0.1359 |
| `lu_solve_prepared/n256/b4` | 0.2639 | - | 0.4467 |
| `lu_solve_prepared/n512/b1` | 0.2083 | - | 0.4627 |
| `lu_solve_prepared/n512/b4` | 1.1251 | - | 1.9358 |
| `qr/n256/b1` | 6.2417 | - | 6.0290 |
| `qr/n256/b4` | 24.8834 | - | 24.2042 |
| `qr/n512/b1` | 42.3234 | - | 41.7528 |
| `qr/n512/b4` | 169.6720 | - | 168.5124 |
| `rank_revealing_qr/n256/b1` | 6.7774 | - | 6.4264 |
| `rank_revealing_qr/n256/b4` | 26.9673 | - | 26.1905 |
| `rank_revealing_qr/n512/b1` | 47.5595 | - | 44.7872 |
| `rank_revealing_qr/n512/b4` | 192.1377 | - | 179.5408 |
| `solve/n256/b1` | 1.1747 | - | 1.4853 |
| `solve/n256/b4` | 4.7267 | - | 5.9362 |
| `solve/n512/b1` | 8.2574 | - | 10.0204 |
| `solve/n512/b4` | 32.9912 | - | 40.5118 |
| `svd_thin/n256/b1` | 24.1767 | - | 22.6190 |
| `svd_thin/n256/b4` | 95.8689 | - | 90.3491 |
| `svd_thin/n512/b1` | 152.0696 | - | 143.7036 |
| `svd_thin/n512/b4` | 607.9446 | - | 575.7531 |
| `svd_values/n256/b1` | 11.1360 | - | 9.7242 |
| `svd_values/n256/b4` | 44.2572 | - | 39.0364 |
| `svd_values/n512/b1` | 65.6960 | - | 59.8384 |
| `svd_values/n512/b4` | 264.1975 | - | 239.8066 |
| `triangular_solve/n256/b1` | 0.0339 | - | 0.0650 |
| `triangular_solve/n256/b4` | 0.1373 | - | 0.2572 |
| `triangular_solve/n512/b1` | 0.1121 | - | 0.2074 |
| `triangular_solve/n512/b4` | 0.5088 | - | 0.8638 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7079 | 0.5044 | 0.3703 |
| `cholesky/n256/b4` | 2.7874 | 1.9548 | 1.3833 |
| `cholesky/n512/b1` | 4.7411 | 2.4689 | 2.0834 |
| `cholesky/n512/b4` | 19.6527 | 10.3611 | 9.3435 |
| `eigh/n256/b1` | 10.2212 | 7.7483 | 19.6047 |
| `eigh/n256/b4` | 41.2670 | 31.9830 | 78.4850 |
| `eigh/n512/b1` | 62.9892 | 28.7106 | 128.5984 |
| `eigh/n512/b4` | 252.7759 | 116.2222 | 516.0043 |
| `eigvalsh/n256/b1` | 4.9596 | 4.9935 | 4.9434 |
| `eigvalsh/n256/b4` | 19.7772 | 19.8640 | 19.6844 |
| `eigvalsh/n512/b1` | 29.4883 | 19.8366 | 20.5168 |
| `eigvalsh/n512/b4` | 118.6157 | 79.7225 | 81.9425 |
| `householder_apply/n256/b1` | 3.3812 | 0.9841 | 2.2534 |
| `householder_apply/n256/b4` | 13.6166 | 4.0033 | 9.0060 |
| `householder_apply/n512/b1` | 24.8119 | 6.4882 | 12.3827 |
| `householder_apply/n512/b4` | 96.7476 | 26.0558 | 49.2695 |
| `householder_factor/n256/b1` | 2.3348 | 0.9143 | 1.7182 |
| `householder_factor/n256/b4` | 9.3971 | 3.6797 | 6.8950 |
| `householder_factor/n512/b1` | 16.7416 | 5.1941 | 8.5043 |
| `householder_factor/n512/b4` | 67.2781 | 20.8911 | 34.7385 |
| `lu/n256/b1` | 1.2630 | 0.8353 | 0.7762 |
| `lu/n256/b4` | 5.1456 | 3.3555 | 3.3157 |
| `lu/n512/b1` | 8.6986 | 3.8876 | 3.6772 |
| `lu/n512/b4` | 34.8768 | 15.3178 | 14.9123 |
| `lu_factor/n256/b1` | 1.1119 | 0.6768 | 0.6638 |
| `lu_factor/n256/b4` | 4.5044 | 2.3045 | 2.6547 |
| `lu_factor/n512/b1` | 8.0041 | 3.0866 | 2.9903 |
| `lu_factor/n512/b4` | 32.7156 | 9.0068 | 11.9963 |
| `lu_factor_solve/n256/b1` | 1.1806 | 0.7232 | 0.7586 |
| `lu_factor_solve/n256/b4` | 4.7674 | 1.7550 | 3.0075 |
| `lu_factor_solve/n512/b1` | 8.2174 | 3.2549 | 3.3839 |
| `lu_factor_solve/n512/b4` | 33.7504 | 9.5648 | 13.5577 |
| `lu_solve_prepared/n256/b1` | 0.0628 | 0.0592 | 0.0929 |
| `lu_solve_prepared/n256/b4` | 0.2493 | 0.0686 | 0.3316 |
| `lu_solve_prepared/n512/b1` | 0.2138 | 0.1634 | 0.3586 |
| `lu_solve_prepared/n512/b4` | 1.3082 | 0.3807 | 1.8014 |
| `qr/n256/b1` | 6.2583 | 3.0561 | 3.4415 |
| `qr/n256/b4` | 24.9210 | 12.1944 | 13.9313 |
| `qr/n512/b1` | 42.5021 | 14.4763 | 17.4191 |
| `qr/n512/b4` | 170.1538 | 57.8936 | 69.8711 |
| `rank_revealing_qr/n256/b1` | 6.7736 | 3.9256 | 3.8681 |
| `rank_revealing_qr/n256/b4` | 26.9709 | 15.9448 | 15.9040 |
| `rank_revealing_qr/n512/b1` | 47.9102 | 16.2980 | 19.1624 |
| `rank_revealing_qr/n512/b4` | 191.7480 | 64.8149 | 76.6281 |
| `solve/n256/b1` | 1.1738 | 0.7593 | 0.8125 |
| `solve/n256/b4` | 4.6891 | 3.0180 | 3.2168 |
| `solve/n512/b1` | 8.2441 | 3.3824 | 3.4295 |
| `solve/n512/b4` | 32.7653 | 13.3745 | 14.1028 |
| `svd_thin/n256/b1` | 24.1443 | 15.0625 | 14.4084 |
| `svd_thin/n256/b4` | 97.1113 | 59.7541 | 57.7914 |
| `svd_thin/n512/b1` | 152.0500 | 66.9957 | 71.0245 |
| `svd_thin/n512/b4` | 607.6200 | 268.7804 | 288.9464 |
| `svd_values/n256/b1` | 11.0788 | 10.7738 | 7.2361 |
| `svd_values/n256/b4` | 44.3219 | 43.3630 | 29.0749 |
| `svd_values/n512/b1` | 65.6709 | 41.8355 | 32.1426 |
| `svd_values/n512/b4` | 263.8510 | 166.7776 | 129.1198 |
| `triangular_solve/n256/b1` | 0.0338 | 0.0341 | 0.0477 |
| `triangular_solve/n256/b4` | 0.1488 | 0.1333 | 0.2220 |
| `triangular_solve/n512/b1` | 0.1124 | 0.0840 | 0.1496 |
| `triangular_solve/n512/b4` | 0.5431 | 0.3684 | 0.7937 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7023 | 0.4912 | 0.3396 |
| `cholesky/n256/b4` | 2.8196 | 1.9489 | 1.3234 |
| `cholesky/n512/b1` | 4.7859 | 1.8399 | 1.4567 |
| `cholesky/n512/b4` | 19.7173 | 7.9698 | 6.5601 |
| `eigh/n256/b1` | 10.2314 | 6.9434 | 19.4885 |
| `eigh/n256/b4` | 41.3199 | 27.9162 | 77.2879 |
| `eigh/n512/b1` | 63.0999 | 23.9437 | 123.0937 |
| `eigh/n512/b4` | 251.4653 | 98.1612 | 494.8621 |
| `eigvalsh/n256/b1` | 4.9650 | 5.0030 | 4.8227 |
| `eigvalsh/n256/b4` | 19.8740 | 19.8536 | 19.4813 |
| `eigvalsh/n512/b1` | 29.6065 | 17.9011 | 17.8709 |
| `eigvalsh/n512/b4` | 118.5914 | 71.7060 | 71.9314 |
| `householder_apply/n256/b1` | 3.3186 | 0.8193 | 1.7681 |
| `householder_apply/n256/b4` | 13.5425 | 3.3859 | 7.2488 |
| `householder_apply/n512/b1` | 24.6216 | 4.2357 | 8.5985 |
| `householder_apply/n512/b4` | 98.8997 | 17.3001 | 35.6278 |
| `householder_factor/n256/b1` | 2.3402 | 0.9227 | 1.5221 |
| `householder_factor/n256/b4` | 9.1838 | 3.6551 | 6.0744 |
| `householder_factor/n512/b1` | 16.7177 | 4.1722 | 6.5257 |
| `householder_factor/n512/b4` | 67.2659 | 16.8555 | 26.1916 |
| `lu/n256/b1` | 1.2489 | 0.8182 | 0.5514 |
| `lu/n256/b4` | 5.1383 | 3.6813 | 2.4686 |
| `lu/n512/b1` | 8.7267 | 3.3318 | 2.2982 |
| `lu/n512/b4` | 34.8181 | 13.2129 | 9.2510 |
| `lu_factor/n256/b1` | 1.1111 | 0.6527 | 0.4530 |
| `lu_factor/n256/b4` | 4.3393 | 2.5882 | 1.7751 |
| `lu_factor/n512/b1` | 8.0074 | 2.5594 | 1.6369 |
| `lu_factor/n512/b4` | 32.6715 | 10.3985 | 6.6516 |
| `lu_factor_solve/n256/b1` | 1.1729 | 0.7305 | 0.5591 |
| `lu_factor_solve/n256/b4` | 4.6010 | 2.8288 | 2.0703 |
| `lu_factor_solve/n512/b1` | 8.2533 | 2.7301 | 2.0046 |
| `lu_factor_solve/n512/b4` | 33.6582 | 11.1511 | 8.0393 |
| `lu_solve_prepared/n256/b1` | 0.0632 | 0.0674 | 0.1037 |
| `lu_solve_prepared/n256/b4` | 0.2619 | 0.2697 | 0.3147 |
| `lu_solve_prepared/n512/b1` | 0.2212 | 0.1659 | 0.3410 |
| `lu_solve_prepared/n512/b4` | 1.0545 | 0.8709 | 1.5711 |
| `qr/n256/b1` | 6.2151 | 3.4547 | 3.0613 |
| `qr/n256/b4` | 24.9289 | 13.7933 | 12.3646 |
| `qr/n512/b1` | 42.4061 | 12.1670 | 13.1910 |
| `qr/n512/b4` | 171.1608 | 48.4569 | 53.5252 |
| `rank_revealing_qr/n256/b1` | 6.7902 | 3.9594 | 3.5263 |
| `rank_revealing_qr/n256/b4` | 27.0399 | 15.2744 | 14.4124 |
| `rank_revealing_qr/n512/b1` | 47.7354 | 11.7694 | 14.8708 |
| `rank_revealing_qr/n512/b4` | 191.1076 | 46.8497 | 59.9260 |
| `solve/n256/b1` | 1.1835 | 0.7443 | 0.5878 |
| `solve/n256/b4` | 4.7033 | 2.9967 | 2.4332 |
| `solve/n512/b1` | 8.2292 | 2.9717 | 2.1235 |
| `solve/n512/b4` | 32.9469 | 11.2683 | 8.7719 |
| `svd_thin/n256/b1` | 23.9857 | 14.7837 | 13.3427 |
| `svd_thin/n256/b4` | 97.2081 | 59.3606 | 53.7980 |
| `svd_thin/n512/b1` | 151.5299 | 55.9108 | 59.9837 |
| `svd_thin/n512/b4` | 608.2183 | 223.1453 | 245.5976 |
| `svd_values/n256/b1` | 11.0267 | 10.7738 | 7.1737 |
| `svd_values/n256/b4` | 44.3335 | 43.0855 | 28.6241 |
| `svd_values/n512/b1` | 65.1219 | 39.6384 | 28.6677 |
| `svd_values/n512/b4` | 261.5466 | 159.8425 | 116.1147 |
| `triangular_solve/n256/b1` | 0.0341 | 0.0376 | 0.0450 |
| `triangular_solve/n256/b4` | 0.1428 | 0.1468 | 0.2027 |
| `triangular_solve/n512/b1` | 0.1151 | 0.0873 | 0.1552 |
| `triangular_solve/n512/b4` | 0.5000 | 0.4042 | 0.8192 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3243 | - | 0.5505 |
| `householder_factor/4096x256/b1` | 14.3815 | - | 23.4095 |
| `qr/1024x64/b1` | 0.9859 | - | 1.0746 |
| `qr/4096x256/b1` | 41.3605 | - | 46.9767 |
| `rank_revealing_qr/1024x64/b1` | 0.9733 | - | 1.1679 |
| `rank_revealing_qr/4096x256/b1` | 65.1548 | - | 57.7986 |
| `svd_thin/1024x64/b1` | 1.4585 | - | 1.9717 |
| `svd_thin/4096x256/b1` | 72.8760 | - | 74.6105 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3304 | 0.2778 | 0.5943 |
| `householder_factor/4096x256/b1` | 14.2865 | 5.9152 | 12.4017 |
| `qr/1024x64/b1` | 0.9838 | 0.8069 | 1.1337 |
| `qr/4096x256/b1` | 41.4964 | 18.1259 | 24.5909 |
| `rank_revealing_qr/1024x64/b1` | 0.9756 | 0.7230 | 1.2329 |
| `rank_revealing_qr/4096x256/b1` | 65.9373 | 22.4504 | 28.0891 |
| `svd_thin/1024x64/b1` | 1.4513 | 1.2930 | 1.9017 |
| `svd_thin/4096x256/b1` | 72.1493 | 30.8644 | 41.8712 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3311 | 0.3110 | 0.6040 |
| `householder_factor/4096x256/b1` | 14.1784 | 4.9046 | 10.7397 |
| `qr/1024x64/b1` | 0.9779 | 0.9503 | 1.1451 |
| `qr/4096x256/b1` | 41.1465 | 15.0257 | 21.6367 |
| `rank_revealing_qr/1024x64/b1` | 0.9745 | 0.7033 | 1.2653 |
| `rank_revealing_qr/4096x256/b1` | 65.7953 | 15.9035 | 24.2847 |
| `svd_thin/1024x64/b1` | 1.4537 | 1.4505 | 1.8927 |
| `svd_thin/4096x256/b1` | 72.7379 | 26.8921 | 37.1135 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0229 | - | 1.0535 |
| `householder_factor/4096x256/b1` | 55.7803 | - | 68.9617 |
| `qr/1024x64/b1` | 2.8471 | - | 2.0838 |
| `qr/4096x256/b1` | 146.5812 | - | 138.4129 |
| `rank_revealing_qr/1024x64/b1` | 2.8679 | - | 2.2536 |
| `rank_revealing_qr/4096x256/b1` | 245.9065 | - | 171.8842 |
| `svd_thin/1024x64/b1` | 3.5376 | - | 3.9460 |
| `svd_thin/4096x256/b1` | 231.4153 | - | 218.2909 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0434 | 0.5664 | 0.4364 |
| `householder_factor/4096x256/b1` | 54.5004 | 18.3846 | 20.0266 |
| `qr/1024x64/b1` | 2.8465 | 1.4920 | 0.8067 |
| `qr/4096x256/b1` | 147.1238 | 52.8439 | 40.0857 |
| `rank_revealing_qr/1024x64/b1` | 2.8715 | 1.5975 | 1.0330 |
| `rank_revealing_qr/4096x256/b1` | 249.3921 | 77.6355 | 54.9511 |
| `svd_thin/1024x64/b1` | 3.5352 | 2.1491 | 2.1000 |
| `svd_thin/4096x256/b1` | 232.4511 | 83.0021 | 75.7023 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0423 | 0.5481 | 0.3444 |
| `householder_factor/4096x256/b1` | 55.8448 | 13.3508 | 12.3337 |
| `qr/1024x64/b1` | 2.8470 | 1.4480 | 0.6244 |
| `qr/4096x256/b1` | 146.6956 | 36.8684 | 25.7360 |
| `rank_revealing_qr/1024x64/b1` | 2.8782 | 1.3854 | 0.8690 |
| `rank_revealing_qr/4096x256/b1` | 244.2569 | 44.7840 | 34.0707 |
| `svd_thin/1024x64/b1` | 3.5342 | 2.1114 | 1.8290 |
| `svd_thin/4096x256/b1` | 231.2275 | 76.3407 | 53.2286 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
