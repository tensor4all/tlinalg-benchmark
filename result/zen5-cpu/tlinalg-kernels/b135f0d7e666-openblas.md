<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261011T010342Z-mkl-campaign/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `b135f0d7e66662716e81cfd7aec2752bc4e605d7`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
- harness commit: `708744f86fe8c3f122e303542707802488cb74d0`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-11T01:58:11.591462Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas --checkout /tmp/tl-mkl --aa 1 --label mkl-campaign`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261011T010342Z-mkl-campaign/`

## What was measured

- **Workload** — Square and rectangular dense matrices in a batch: one call per batch over a rank-2+B descriptor, `n x n` or `m x n` per item. Sizes are the matrix dimension, not a memory budget, so a case name says exactly what was factored; the batch extent is a separate axis and is never collapsed.
  Source: The library's own kernel inventory (crates/tlinalg/src, crates/tlinalg-blas/src). Inputs are seeded from the case, so `verify` and `run` measure the same matrices and a rerun is reproducible.
  Known blind spot: Only the kernel entry points are measured. Tensor construction, dtype dispatch, session entry and pool checkout are tenferro's and are out of scope.
  Known blind spot: Batch extents are declared per regime, so a cost proportional to batch elements is visible only where the regime says so.
  Known blind spot: The providers are compared at the thread budgets declared here; a budget the vendor threads itself by, outside that set, is not covered.
  Known blind spot: A vendor arm records the vendor library, but only OpenBLAS reports the kernel its runtime dispatched to. MKL's manifest records its own version and the threading layer the harness pins; it names no kernel, because MKL exposes none to name.
  Known blind spot: Each axis is sampled at two ends, not across it: n=8 in the small regime and n=64 in the medium regime are not measured, and neither is the batch between 1 and 1024. A cost that is only visible in the middle of a range is not covered here.
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
| `cholesky/n16/b1024` | 0.5262 | - | 0.6119 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1078 | - | 0.1162 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2164 | - | 0.2301 |
| `eig/n16/b1` | 0.0565 | - | 0.0436 |
| `eig/n16/b1024` | 60.4312 | - | 46.1573 |
| `eig/n4/b1` | 0.0043 | - | 0.0044 |
| `eig/n4/b1024` | 3.8401 | - | 3.4608 |
| `eig/n8/b1` | 0.0151 | - | 0.0124 |
| `eig/n8/b1024` | 14.6148 | - | 11.3834 |
| `eigh/n16/b1` | 0.0178 | - | 0.0232 |
| `eigh/n16/b1024` | 17.8824 | - | 24.0816 |
| `eigh/n4/b1` | 0.0017 | - | 0.0020 |
| `eigh/n4/b1024` | 1.4717 | - | 1.8258 |
| `eigh/n8/b1` | 0.0052 | - | 0.0065 |
| `eigh/n8/b1024` | 5.0800 | - | 6.5363 |
| `eigvals/n16/b1` | 0.0400 | - | 0.0324 |
| `eigvals/n16/b1024` | 41.7229 | - | 32.5593 |
| `eigvals/n4/b1` | 0.0027 | - | 0.0032 |
| `eigvals/n4/b1024` | 2.1655 | - | 2.3011 |
| `eigvals/n8/b1` | 0.0106 | - | 0.0098 |
| `eigvals/n8/b1024` | 10.0202 | - | 8.8010 |
| `eigvalsh/n16/b1` | 0.0195 | - | 0.0087 |
| `eigvalsh/n16/b1024` | 20.3383 | - | 8.7076 |
| `eigvalsh/n4/b1` | 0.0019 | - | 0.0011 |
| `eigvalsh/n4/b1024` | 1.5552 | - | 0.8496 |
| `eigvalsh/n8/b1` | 0.0059 | - | 0.0030 |
| `eigvalsh/n8/b1024` | 5.3434 | - | 2.7213 |
| `full_piv_lu/n16/b1` | 0.0025 | - | 0.0026 |
| `full_piv_lu/n16/b1024` | 2.0932 | - | 2.7169 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2186 | - | 0.2188 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0007 |
| `full_piv_lu/n8/b1024` | 0.6383 | - | 0.5859 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | - | 0.0038 |
| `full_piv_lu_solve/n16/b1024` | 2.0521 | - | 3.7655 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | - | 0.0006 |
| `full_piv_lu_solve/n4/b1024` | 0.3237 | - | 0.4114 |
| `full_piv_lu_solve/n8/b1` | 0.0013 | - | 0.0012 |
| `full_piv_lu_solve/n8/b1024` | 0.7393 | - | 0.9964 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0030 |
| `householder_apply/n16/b1024` | 2.7189 | - | 2.7079 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0007 |
| `householder_apply/n4/b1024` | 0.1785 | - | 0.2492 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0011 |
| `householder_apply/n8/b1024` | 0.6802 | - | 0.7237 |
| `householder_factor/n16/b1` | 0.0020 | - | 0.0027 |
| `householder_factor/n16/b1024` | 2.0465 | - | 2.6127 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.2425 | - | 0.3197 |
| `householder_factor/n8/b1` | 0.0007 | - | 0.0011 |
| `householder_factor/n8/b1024` | 0.6610 | - | 0.9015 |
| `lu/n16/b1` | 0.0019 | - | 0.0016 |
| `lu/n16/b1024` | 1.4527 | - | 1.4560 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.1670 | - | 0.1924 |
| `lu/n8/b1` | 0.0007 | - | 0.0007 |
| `lu/n8/b1024` | 0.4627 | - | 0.4766 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0011 |
| `lu_factor/n16/b1024` | 1.0999 | - | 1.1074 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1325 | - | 0.1295 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3424 | - | 0.3403 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0020 |
| `lu_factor_solve/n16/b1024` | 1.4168 | - | 1.9574 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.1662 | - | 0.3144 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0007 |
| `lu_factor_solve/n8/b1024` | 0.4719 | - | 0.6588 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0008 |
| `lu_solve_prepared/n16/b1024` | 0.3581 | - | 0.7154 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0404 | - | 0.1898 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0003 |
| `lu_solve_prepared/n8/b1024` | 0.1380 | - | 0.3102 |
| `qr/n16/b1` | 0.0055 | - | 0.0049 |
| `qr/n16/b1024` | 5.3216 | - | 4.7370 |
| `qr/n4/b1` | 0.0008 | - | 0.0008 |
| `qr/n4/b1024` | 0.4274 | - | 0.5749 |
| `qr/n8/b1` | 0.0016 | - | 0.0018 |
| `qr/n8/b1024` | 1.3994 | - | 1.5798 |
| `rank_revealing_qr/n16/b1` | 0.0065 | - | 0.0060 |
| `rank_revealing_qr/n16/b1024` | 6.1344 | - | 5.6217 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6847 | - | 0.7048 |
| `rank_revealing_qr/n8/b1` | 0.0022 | - | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8547 | - | 1.8186 |
| `solve/n16/b1` | 0.0021 | - | 0.0024 |
| `solve/n16/b1024` | 1.5243 | - | 2.0475 |
| `solve/n4/b1` | 0.0006 | - | 0.0006 |
| `solve/n4/b1024` | 0.2173 | - | 0.3346 |
| `solve/n8/b1` | 0.0009 | - | 0.0010 |
| `solve/n8/b1024` | 0.5419 | - | 0.6988 |
| `svd_full/n16/b1` | 0.0325 | - | 0.0519 |
| `svd_full/n16/b1024` | 33.2730 | - | 53.0413 |
| `svd_full/n4/b1` | 0.0029 | - | 0.0049 |
| `svd_full/n4/b1024` | 2.5166 | - | 4.0545 |
| `svd_full/n8/b1` | 0.0090 | - | 0.0136 |
| `svd_full/n8/b1024` | 9.0127 | - | 13.5023 |
| `svd_thin/n16/b1` | 0.0327 | - | 0.0520 |
| `svd_thin/n16/b1024` | 33.4000 | - | 53.2760 |
| `svd_thin/n4/b1` | 0.0027 | - | 0.0049 |
| `svd_thin/n4/b1024` | 2.5158 | - | 4.0661 |
| `svd_thin/n8/b1` | 0.0090 | - | 0.0135 |
| `svd_thin/n8/b1024` | 8.9826 | - | 13.6539 |
| `svd_values/n16/b1` | 0.0268 | - | 0.0179 |
| `svd_values/n16/b1024` | 28.0124 | - | 18.4946 |
| `svd_values/n4/b1` | 0.0025 | - | 0.0031 |
| `svd_values/n4/b1024` | 2.1393 | - | 2.2981 |
| `svd_values/n8/b1` | 0.0077 | - | 0.0066 |
| `svd_values/n8/b1024` | 7.5068 | - | 6.1285 |
| `triangular_solve/n16/b1` | 0.0004 | - | 0.0006 |
| `triangular_solve/n16/b1024` | 0.2995 | - | 0.3883 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0509 | - | 0.1197 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1302 | - | 0.1824 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0023 | 0.0007 |
| `cholesky/n16/b1024` | 0.5214 | 0.1341 | 0.6028 |
| `cholesky/n4/b1` | 0.0002 | 0.0026 | 0.0002 |
| `cholesky/n4/b1024` | 0.1052 | 0.0568 | 0.1164 |
| `cholesky/n8/b1` | 0.0003 | 0.0021 | 0.0003 |
| `cholesky/n8/b1024` | 0.2204 | 0.0583 | 0.2316 |
| `eig/n16/b1` | 0.0562 | 0.0598 | 0.0444 |
| `eig/n16/b1024` | 60.2026 | 18.5847 | 45.8859 |
| `eig/n4/b1` | 0.0044 | 0.0074 | 0.0044 |
| `eig/n4/b1024` | 3.8376 | 2.3622 | 3.5090 |
| `eig/n8/b1` | 0.0152 | 0.0182 | 0.0124 |
| `eig/n8/b1024` | 14.6039 | 4.7349 | 11.4153 |
| `eigh/n16/b1` | 0.0174 | 0.0209 | 0.0229 |
| `eigh/n16/b1024` | 17.8437 | 7.5616 | 23.8810 |
| `eigh/n4/b1` | 0.0016 | 0.0039 | 0.0020 |
| `eigh/n4/b1024` | 1.4647 | 0.7391 | 1.8318 |
| `eigh/n8/b1` | 0.0051 | 0.0077 | 0.0065 |
| `eigh/n8/b1024` | 5.0447 | 2.5587 | 6.5117 |
| `eigvals/n16/b1` | 0.0399 | 0.0433 | 0.0322 |
| `eigvals/n16/b1024` | 41.6333 | 12.8761 | 32.4470 |
| `eigvals/n4/b1` | 0.0027 | 0.0054 | 0.0032 |
| `eigvals/n4/b1024` | 2.1794 | 1.3177 | 2.2911 |
| `eigvals/n8/b1` | 0.0106 | 0.0140 | 0.0097 |
| `eigvals/n8/b1024` | 9.9667 | 3.4911 | 8.7011 |
| `eigvalsh/n16/b1` | 0.0194 | 0.0239 | 0.0086 |
| `eigvalsh/n16/b1024` | 20.2067 | 10.8719 | 8.7099 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0042 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5634 | 0.9250 | 0.8659 |
| `eigvalsh/n8/b1` | 0.0057 | 0.0092 | 0.0030 |
| `eigvalsh/n8/b1024` | 5.3928 | 2.9069 | 2.7639 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0044 | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.1133 | 1.0290 | 2.8216 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0023 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2145 | 0.0588 | 0.2197 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0036 | 0.0007 |
| `full_piv_lu/n8/b1024` | 0.5985 | 0.3165 | 0.6078 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0049 | 0.0038 |
| `full_piv_lu_solve/n16/b1024` | 2.0599 | 0.5294 | 3.7838 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0034 | 0.0007 |
| `full_piv_lu_solve/n4/b1024` | 0.3242 | 0.1691 | 0.5480 |
| `full_piv_lu_solve/n8/b1` | 0.0013 | 0.0035 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7420 | 0.3806 | 1.1776 |
| `householder_apply/n16/b1` | 0.0025 | 0.0050 | 0.0031 |
| `householder_apply/n16/b1024` | 2.5576 | 0.6831 | 2.7320 |
| `householder_apply/n4/b1` | 0.0003 | 0.0027 | 0.0006 |
| `householder_apply/n4/b1024` | 0.1759 | 0.0474 | 0.2468 |
| `householder_apply/n8/b1` | 0.0007 | 0.0033 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6398 | 0.1717 | 0.7218 |
| `householder_factor/n16/b1` | 0.0020 | 0.0040 | 0.0028 |
| `householder_factor/n16/b1024` | 2.0677 | 0.5194 | 2.6418 |
| `householder_factor/n4/b1` | 0.0003 | 0.0027 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2432 | 0.1251 | 0.3215 |
| `householder_factor/n8/b1` | 0.0007 | 0.0033 | 0.0011 |
| `householder_factor/n8/b1024` | 0.6799 | 0.1698 | 0.9025 |
| `lu/n16/b1` | 0.0020 | 0.0045 | 0.0017 |
| `lu/n16/b1024` | 1.5857 | 0.7921 | 1.5098 |
| `lu/n4/b1` | 0.0004 | 0.0025 | 0.0004 |
| `lu/n4/b1024` | 0.1688 | 0.0903 | 0.1928 |
| `lu/n8/b1` | 0.0007 | 0.0035 | 0.0007 |
| `lu/n8/b1024` | 0.4767 | 0.1261 | 0.4820 |
| `lu_factor/n16/b1` | 0.0013 | 0.0037 | 0.0011 |
| `lu_factor/n16/b1024` | 1.0946 | 0.2857 | 1.1171 |
| `lu_factor/n4/b1` | 0.0003 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1338 | 0.0388 | 0.1292 |
| `lu_factor/n8/b1` | 0.0006 | 0.0027 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3528 | 0.0945 | 0.3395 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0042 | 0.0023 |
| `lu_factor_solve/n16/b1024` | 1.4366 | 0.3649 | 2.2608 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0021 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1641 | 0.0471 | 0.7627 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0035 | 0.0011 |
| `lu_factor_solve/n8/b1024` | 0.4792 | 0.1231 | 1.2090 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0027 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3612 | 0.1935 | 0.8709 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0402 | 0.0205 | 0.6162 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0028 | 0.0008 |
| `lu_solve_prepared/n8/b1024` | 0.1372 | 0.0459 | 0.7416 |
| `qr/n16/b1` | 0.0055 | 0.0085 | 0.0049 |
| `qr/n16/b1024` | 5.2527 | 2.6668 | 4.7411 |
| `qr/n4/b1` | 0.0008 | 0.0024 | 0.0008 |
| `qr/n4/b1024` | 0.4320 | 0.1122 | 0.5718 |
| `qr/n8/b1` | 0.0016 | 0.0039 | 0.0018 |
| `qr/n8/b1024` | 1.3764 | 0.6949 | 1.5812 |
| `rank_revealing_qr/n16/b1` | 0.0064 | 0.0100 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.0468 | 2.6572 | 5.5899 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0034 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6853 | 0.3479 | 0.7062 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0045 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8136 | 0.9247 | 1.8389 |
| `solve/n16/b1` | 0.0022 | 0.0049 | 0.0024 |
| `solve/n16/b1024` | 1.5627 | 0.4014 | 2.3889 |
| `solve/n4/b1` | 0.0007 | 0.0022 | 0.0009 |
| `solve/n4/b1024` | 0.2243 | 0.0641 | 0.6718 |
| `solve/n8/b1` | 0.0009 | 0.0035 | 0.0011 |
| `solve/n8/b1024` | 0.5424 | 0.2774 | 0.9000 |
| `svd_full/n16/b1` | 0.0326 | 0.0353 | 0.0521 |
| `svd_full/n16/b1024` | 33.3089 | 15.3511 | 53.5858 |
| `svd_full/n4/b1` | 0.0027 | 0.0043 | 0.0050 |
| `svd_full/n4/b1024` | 2.5126 | 1.2678 | 4.0536 |
| `svd_full/n8/b1` | 0.0090 | 0.0118 | 0.0136 |
| `svd_full/n8/b1024` | 10.5519 | 4.5095 | 13.5168 |
| `svd_thin/n16/b1` | 0.0326 | 0.0357 | 0.0516 |
| `svd_thin/n16/b1024` | 33.2805 | 12.2248 | 53.0497 |
| `svd_thin/n4/b1` | 0.0027 | 0.0045 | 0.0048 |
| `svd_thin/n4/b1024` | 2.5156 | 0.6328 | 4.0508 |
| `svd_thin/n8/b1` | 0.0090 | 0.0114 | 0.0135 |
| `svd_thin/n8/b1024` | 9.0238 | 2.3055 | 13.5486 |
| `svd_values/n16/b1` | 0.0265 | 0.0299 | 0.0177 |
| `svd_values/n16/b1024` | 27.9647 | 9.9953 | 18.2912 |
| `svd_values/n4/b1` | 0.0025 | 0.0041 | 0.0030 |
| `svd_values/n4/b1024` | 2.1552 | 1.2301 | 2.3184 |
| `svd_values/n8/b1` | 0.0076 | 0.0099 | 0.0066 |
| `svd_values/n8/b1024` | 7.5407 | 2.9760 | 6.1512 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0036 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3123 | 0.0848 | 0.6606 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0028 | 0.0005 |
| `triangular_solve/n4/b1024` | 0.0515 | 0.0201 | 0.3831 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0031 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.1333 | 0.0380 | 0.4792 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0038 | 0.0007 |
| `cholesky/n16/b1024` | 0.5291 | 0.0698 | 0.6188 |
| `cholesky/n4/b1` | 0.0002 | 0.0030 | 0.0002 |
| `cholesky/n4/b1024` | 0.1062 | 0.0216 | 0.1177 |
| `cholesky/n8/b1` | 0.0003 | 0.0024 | 0.0003 |
| `cholesky/n8/b1024` | 0.2181 | 0.0354 | 0.2316 |
| `eig/n16/b1` | 0.0567 | 0.0607 | 0.0440 |
| `eig/n16/b1024` | 60.3404 | 11.5509 | 46.3378 |
| `eig/n4/b1` | 0.0044 | 0.0076 | 0.0044 |
| `eig/n4/b1024` | 3.8277 | 1.1754 | 3.4659 |
| `eig/n8/b1` | 0.0152 | 0.0182 | 0.0123 |
| `eig/n8/b1024` | 14.5085 | 2.9964 | 11.3599 |
| `eigh/n16/b1` | 0.0175 | 0.0208 | 0.0232 |
| `eigh/n16/b1024` | 17.5527 | 2.2355 | 24.1041 |
| `eigh/n4/b1` | 0.0017 | 0.0052 | 0.0020 |
| `eigh/n4/b1024` | 1.4603 | 0.3767 | 1.8070 |
| `eigh/n8/b1` | 0.0051 | 0.0078 | 0.0065 |
| `eigh/n8/b1024` | 5.0201 | 0.9468 | 6.5100 |
| `eigvals/n16/b1` | 0.0399 | 0.0434 | 0.0324 |
| `eigvals/n16/b1024` | 41.6862 | 8.0871 | 32.7546 |
| `eigvals/n4/b1` | 0.0027 | 0.0057 | 0.0032 |
| `eigvals/n4/b1024` | 2.1811 | 0.7566 | 2.2956 |
| `eigvals/n8/b1` | 0.0106 | 0.0135 | 0.0098 |
| `eigvals/n8/b1024` | 9.9674 | 2.4682 | 8.8255 |
| `eigvalsh/n16/b1` | 0.0194 | 0.0229 | 0.0086 |
| `eigvalsh/n16/b1024` | 20.2223 | 9.1134 | 8.7533 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0047 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5596 | 0.5720 | 0.8450 |
| `eigvalsh/n8/b1` | 0.0057 | 0.0084 | 0.0031 |
| `eigvalsh/n8/b1024` | 5.3647 | 2.2490 | 2.7398 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0056 | 0.0027 |
| `full_piv_lu/n16/b1024` | 2.0489 | 0.5118 | 2.7846 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2148 | 0.0345 | 0.2214 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0039 | 0.0007 |
| `full_piv_lu/n8/b1024` | 0.5917 | 0.0904 | 0.6108 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0055 | 0.0039 |
| `full_piv_lu_solve/n16/b1024` | 1.9978 | 0.5126 | 3.7494 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0043 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3234 | 0.0875 | 0.5656 |
| `full_piv_lu_solve/n8/b1` | 0.0013 | 0.0036 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7464 | 0.0989 | 1.1804 |
| `householder_apply/n16/b1` | 0.0025 | 0.0055 | 0.0030 |
| `householder_apply/n16/b1024` | 2.5787 | 0.3461 | 2.6816 |
| `householder_apply/n4/b1` | 0.0003 | 0.0022 | 0.0006 |
| `householder_apply/n4/b1024` | 0.1758 | 0.0497 | 0.2484 |
| `householder_apply/n8/b1` | 0.0007 | 0.0036 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6362 | 0.1675 | 0.7195 |
| `householder_factor/n16/b1` | 0.0020 | 0.0053 | 0.0027 |
| `householder_factor/n16/b1024` | 2.0381 | 0.5222 | 2.6153 |
| `householder_factor/n4/b1` | 0.0003 | 0.0036 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2358 | 0.0665 | 0.3195 |
| `householder_factor/n8/b1` | 0.0007 | 0.0040 | 0.0011 |
| `householder_factor/n8/b1024` | 0.6568 | 0.1715 | 0.8960 |
| `lu/n16/b1` | 0.0020 | 0.0050 | 0.0017 |
| `lu/n16/b1024` | 1.5397 | 0.4019 | 1.4877 |
| `lu/n4/b1` | 0.0004 | 0.0028 | 0.0004 |
| `lu/n4/b1024` | 0.1738 | 0.0474 | 0.1973 |
| `lu/n8/b1` | 0.0007 | 0.0027 | 0.0007 |
| `lu/n8/b1024` | 0.4629 | 0.1204 | 0.4844 |
| `lu_factor/n16/b1` | 0.0013 | 0.0039 | 0.0011 |
| `lu_factor/n16/b1024` | 1.0742 | 0.2804 | 1.0932 |
| `lu_factor/n4/b1` | 0.0003 | 0.0021 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1340 | 0.0385 | 0.1297 |
| `lu_factor/n8/b1` | 0.0006 | 0.0043 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3461 | 0.0927 | 0.3414 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0048 | 0.0022 |
| `lu_factor_solve/n16/b1024` | 1.4382 | 0.3632 | 2.3575 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0020 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.1686 | 0.0468 | 0.8064 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0035 | 0.0011 |
| `lu_factor_solve/n8/b1024` | 0.4769 | 0.1267 | 1.2228 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0033 | 0.0009 |
| `lu_solve_prepared/n16/b1024` | 0.3608 | 0.1060 | 0.9333 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0026 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0404 | 0.0231 | 0.6502 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0030 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.1368 | 0.0450 | 0.7746 |
| `qr/n16/b1` | 0.0054 | 0.0088 | 0.0049 |
| `qr/n16/b1024` | 5.2007 | 0.6813 | 4.7154 |
| `qr/n4/b1` | 0.0007 | 0.0032 | 0.0008 |
| `qr/n4/b1024` | 0.4226 | 0.0633 | 0.5763 |
| `qr/n8/b1` | 0.0016 | 0.0050 | 0.0018 |
| `qr/n8/b1024` | 1.3553 | 0.1787 | 1.5781 |
| `rank_revealing_qr/n16/b1` | 0.0064 | 0.0163 | 0.0060 |
| `rank_revealing_qr/n16/b1024` | 5.9318 | 1.5116 | 5.5459 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0032 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.6941 | 0.0912 | 0.7042 |
| `rank_revealing_qr/n8/b1` | 0.0021 | 0.0053 | 0.0023 |
| `rank_revealing_qr/n8/b1024` | 1.8299 | 0.4636 | 1.8182 |
| `solve/n16/b1` | 0.0021 | 0.0052 | 0.0024 |
| `solve/n16/b1024` | 1.5886 | 0.4002 | 2.4976 |
| `solve/n4/b1` | 0.0006 | 0.0040 | 0.0011 |
| `solve/n4/b1024` | 0.2180 | 0.0607 | 0.7702 |
| `solve/n8/b1` | 0.0009 | 0.0044 | 0.0011 |
| `solve/n8/b1024` | 0.5668 | 0.0869 | 0.9354 |
| `svd_full/n16/b1` | 0.0324 | 0.0359 | 0.0518 |
| `svd_full/n16/b1024` | 33.2063 | 4.2829 | 53.0234 |
| `svd_full/n4/b1` | 0.0027 | 0.0056 | 0.0049 |
| `svd_full/n4/b1024` | 2.5299 | 0.6361 | 4.0881 |
| `svd_full/n8/b1` | 0.0090 | 0.0112 | 0.0137 |
| `svd_full/n8/b1024` | 8.9792 | 1.1811 | 13.5397 |
| `svd_thin/n16/b1` | 0.0328 | 0.0354 | 0.0521 |
| `svd_thin/n16/b1024` | 33.1294 | 4.1929 | 53.1929 |
| `svd_thin/n4/b1` | 0.0027 | 0.0056 | 0.0049 |
| `svd_thin/n4/b1024` | 2.7494 | 0.3195 | 4.0437 |
| `svd_thin/n8/b1` | 0.0091 | 0.0112 | 0.0137 |
| `svd_thin/n8/b1024` | 8.9897 | 1.1625 | 13.5383 |
| `svd_values/n16/b1` | 0.0265 | 0.0305 | 0.0181 |
| `svd_values/n16/b1024` | 27.9364 | 7.8967 | 18.5825 |
| `svd_values/n4/b1` | 0.0025 | 0.0063 | 0.0032 |
| `svd_values/n4/b1024` | 2.1386 | 0.7537 | 2.2930 |
| `svd_values/n8/b1` | 0.0079 | 0.0102 | 0.0067 |
| `svd_values/n8/b1024` | 7.5431 | 2.1142 | 6.1257 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0025 | 0.0008 |
| `triangular_solve/n16/b1024` | 0.3001 | 0.0808 | 0.6891 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0022 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0510 | 0.0158 | 0.4160 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0039 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1303 | 0.0370 | 0.5415 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | - | 0.0010 |
| `cholesky/n16/b1024` | 0.7793 | - | 0.9294 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n4/b1024` | 0.1175 | - | 0.1354 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2601 | - | 0.2942 |
| `eig/n16/b1` | 0.0752 | - | 0.1045 |
| `eig/n16/b1024` | 81.0932 | - | 124.7523 |
| `eig/n4/b1` | 0.0064 | - | 0.0090 |
| `eig/n4/b1024` | 6.2259 | - | 8.2061 |
| `eig/n8/b1` | 0.0213 | - | 0.0276 |
| `eig/n8/b1024` | 21.4510 | - | 28.9703 |
| `eigh/n16/b1` | 0.0180 | - | 0.0263 |
| `eigh/n16/b1024` | 19.3801 | - | 27.1388 |
| `eigh/n4/b1` | 0.0020 | - | 0.0024 |
| `eigh/n4/b1024` | 1.7241 | - | 2.1704 |
| `eigh/n8/b1` | 0.0057 | - | 0.0074 |
| `eigh/n8/b1024` | 5.4489 | - | 7.4606 |
| `eigvals/n16/b1` | 0.0472 | - | 0.0789 |
| `eigvals/n16/b1024` | 52.1237 | - | 95.4735 |
| `eigvals/n4/b1` | 0.0036 | - | 0.0071 |
| `eigvals/n4/b1024` | 3.1389 | - | 6.3422 |
| `eigvals/n8/b1` | 0.0128 | - | 0.0226 |
| `eigvals/n8/b1024` | 12.9605 | - | 23.2238 |
| `eigvalsh/n16/b1` | 0.0207 | - | 0.0117 |
| `eigvalsh/n16/b1024` | 23.4893 | - | 11.5519 |
| `eigvalsh/n4/b1` | 0.0023 | - | 0.0016 |
| `eigvalsh/n4/b1024` | 1.8908 | - | 1.2813 |
| `eigvalsh/n8/b1` | 0.0064 | - | 0.0041 |
| `eigvalsh/n8/b1024` | 5.9531 | - | 3.6920 |
| `full_piv_lu/n16/b1` | 0.0031 | - | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.7803 | - | 20.0714 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2660 | - | 0.5320 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.7344 | - | 2.3086 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | - | 0.0152 |
| `full_piv_lu_solve/n16/b1024` | 3.1099 | - | 22.5125 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4760 | - | 1.1501 |
| `full_piv_lu_solve/n8/b1` | 0.0017 | - | 0.0036 |
| `full_piv_lu_solve/n8/b1024` | 1.1784 | - | 3.5634 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0045 |
| `householder_apply/n16/b1024` | 3.4420 | - | 4.8730 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0009 |
| `householder_apply/n4/b1024` | 0.1780 | - | 0.2609 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0015 |
| `householder_apply/n8/b1024` | 0.6183 | - | 0.8957 |
| `householder_factor/n16/b1` | 0.0026 | - | 0.0045 |
| `householder_factor/n16/b1024` | 2.5807 | - | 4.4365 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0007 |
| `householder_factor/n4/b1024` | 0.3060 | - | 0.5558 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0016 |
| `householder_factor/n8/b1024` | 0.8149 | - | 1.4204 |
| `lu/n16/b1` | 0.0021 | - | 0.0023 |
| `lu/n16/b1024` | 1.8204 | - | 2.3933 |
| `lu/n4/b1` | 0.0005 | - | 0.0004 |
| `lu/n4/b1024` | 0.2072 | - | 0.2281 |
| `lu/n8/b1` | 0.0008 | - | 0.0008 |
| `lu/n8/b1024` | 0.5357 | - | 0.6267 |
| `lu_factor/n16/b1` | 0.0014 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2175 | - | 1.6028 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1627 | - | 0.1601 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0005 |
| `lu_factor/n8/b1024` | 0.3963 | - | 0.4492 |
| `lu_factor_solve/n16/b1` | 0.0023 | - | 0.0027 |
| `lu_factor_solve/n16/b1024` | 1.9707 | - | 2.6439 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0005 |
| `lu_factor_solve/n4/b1024` | 0.2482 | - | 0.4024 |
| `lu_factor_solve/n8/b1` | 0.0009 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6627 | - | 0.8996 |
| `lu_solve_prepared/n16/b1` | 0.0010 | - | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7827 | - | 1.0162 |
| `lu_solve_prepared/n4/b1` | 0.0003 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0964 | - | 0.2422 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.2814 | - | 0.4511 |
| `qr/n16/b1` | 0.0066 | - | 0.0077 |
| `qr/n16/b1024` | 6.4663 | - | 7.6094 |
| `qr/n4/b1` | 0.0007 | - | 0.0012 |
| `qr/n4/b1024` | 0.5068 | - | 0.8613 |
| `qr/n8/b1` | 0.0018 | - | 0.0026 |
| `qr/n8/b1024` | 1.5477 | - | 2.3150 |
| `rank_revealing_qr/n16/b1` | 0.0075 | - | 0.0100 |
| `rank_revealing_qr/n16/b1024` | 7.2050 | - | 10.1759 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8475 | - | 1.1228 |
| `rank_revealing_qr/n8/b1` | 0.0024 | - | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.1883 | - | 3.0637 |
| `solve/n16/b1` | 0.0027 | - | 0.0031 |
| `solve/n16/b1024` | 2.1360 | - | 2.8099 |
| `solve/n4/b1` | 0.0007 | - | 0.0007 |
| `solve/n4/b1024` | 0.3100 | - | 0.4386 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7508 | - | 0.9557 |
| `svd_full/n16/b1` | 0.0348 | - | 0.0589 |
| `svd_full/n16/b1024` | 36.4306 | - | 64.5668 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0060 |
| `svd_full/n4/b1024` | 2.9913 | - | 5.0578 |
| `svd_full/n8/b1` | 0.0096 | - | 0.0161 |
| `svd_full/n8/b1024` | 10.0917 | - | 15.9778 |
| `svd_thin/n16/b1` | 0.0348 | - | 0.0590 |
| `svd_thin/n16/b1024` | 36.7102 | - | 64.2498 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0062 |
| `svd_thin/n4/b1024` | 2.9954 | - | 5.0477 |
| `svd_thin/n8/b1` | 0.0097 | - | 0.0161 |
| `svd_thin/n8/b1024` | 10.0547 | - | 16.0076 |
| `svd_values/n16/b1` | 0.0298 | - | 0.0237 |
| `svd_values/n16/b1024` | 32.9677 | - | 25.6607 |
| `svd_values/n4/b1` | 0.0029 | - | 0.0040 |
| `svd_values/n4/b1024` | 2.6366 | - | 3.1241 |
| `svd_values/n8/b1` | 0.0087 | - | 0.0085 |
| `svd_values/n8/b1024` | 8.8310 | - | 7.8476 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0007 |
| `triangular_solve/n16/b1024` | 0.5851 | - | 0.6112 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0952 | - | 0.1534 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2357 | - | 0.2707 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0033 | 0.0010 |
| `cholesky/n16/b1024` | 0.7699 | 0.3969 | 0.9121 |
| `cholesky/n4/b1` | 0.0002 | 0.0022 | 0.0002 |
| `cholesky/n4/b1024` | 0.1199 | 0.0351 | 0.1368 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2491 | 0.0684 | 0.2937 |
| `eig/n16/b1` | 0.0760 | 0.0795 | 0.1047 |
| `eig/n16/b1024` | 81.5837 | 24.6920 | 124.6403 |
| `eig/n4/b1` | 0.0063 | 0.0089 | 0.0090 |
| `eig/n4/b1024` | 6.1673 | 3.6423 | 8.2157 |
| `eig/n8/b1` | 0.0211 | 0.0244 | 0.0276 |
| `eig/n8/b1024` | 21.5436 | 6.8347 | 28.9832 |
| `eigh/n16/b1` | 0.0181 | 0.0213 | 0.0263 |
| `eigh/n16/b1024` | 19.2442 | 8.1769 | 27.0929 |
| `eigh/n4/b1` | 0.0019 | 0.0037 | 0.0024 |
| `eigh/n4/b1024` | 1.7413 | 0.8780 | 2.1687 |
| `eigh/n8/b1` | 0.0057 | 0.0080 | 0.0074 |
| `eigh/n8/b1024` | 5.4472 | 2.5750 | 7.4881 |
| `eigvals/n16/b1` | 0.0473 | 0.0506 | 0.0788 |
| `eigvals/n16/b1024` | 52.1312 | 17.9943 | 95.2519 |
| `eigvals/n4/b1` | 0.0036 | 0.0050 | 0.0072 |
| `eigvals/n4/b1024` | 3.1431 | 1.7317 | 6.3457 |
| `eigvals/n8/b1` | 0.0128 | 0.0161 | 0.0224 |
| `eigvals/n8/b1024` | 13.0194 | 4.8875 | 23.1766 |
| `eigvalsh/n16/b1` | 0.0207 | 0.0254 | 0.0117 |
| `eigvalsh/n16/b1024` | 23.3671 | 13.1338 | 11.5505 |
| `eigvalsh/n4/b1` | 0.0022 | 0.0048 | 0.0016 |
| `eigvalsh/n4/b1024` | 1.8820 | 1.5742 | 1.2737 |
| `eigvalsh/n8/b1` | 0.0064 | 0.0095 | 0.0040 |
| `eigvalsh/n8/b1024` | 5.9142 | 3.2328 | 3.7027 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0056 | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.9222 | 1.4476 | 20.3599 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0028 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2619 | 0.1379 | 0.5521 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0035 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7487 | 0.3816 | 2.2727 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0063 | 0.0153 |
| `full_piv_lu_solve/n16/b1024` | 3.1085 | 1.5768 | 22.9304 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0027 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4833 | 0.2429 | 1.2710 |
| `full_piv_lu_solve/n8/b1` | 0.0017 | 0.0038 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1727 | 0.3035 | 3.6918 |
| `householder_apply/n16/b1` | 0.0026 | 0.0048 | 0.0046 |
| `householder_apply/n16/b1024` | 3.1916 | 1.2303 | 4.5412 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0009 |
| `householder_apply/n4/b1024` | 0.1807 | 0.0511 | 0.2581 |
| `householder_apply/n8/b1` | 0.0007 | 0.0036 | 0.0015 |
| `householder_apply/n8/b1024` | 0.6233 | 0.1618 | 0.8856 |
| `householder_factor/n16/b1` | 0.0025 | 0.0049 | 0.0045 |
| `householder_factor/n16/b1024` | 2.5274 | 1.2866 | 4.4291 |
| `householder_factor/n4/b1` | 0.0004 | 0.0027 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3054 | 0.0853 | 0.5501 |
| `householder_factor/n8/b1` | 0.0009 | 0.0034 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8069 | 0.2070 | 1.4192 |
| `lu/n16/b1` | 0.0021 | 0.0051 | 0.0023 |
| `lu/n16/b1024` | 1.8569 | 0.9002 | 2.3154 |
| `lu/n4/b1` | 0.0005 | 0.0020 | 0.0004 |
| `lu/n4/b1024` | 0.2056 | 0.0574 | 0.2294 |
| `lu/n8/b1` | 0.0008 | 0.0033 | 0.0008 |
| `lu/n8/b1024` | 0.5415 | 0.2785 | 0.6311 |
| `lu_factor/n16/b1` | 0.0014 | 0.0037 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2014 | 0.6186 | 1.6100 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1597 | 0.0457 | 0.1606 |
| `lu_factor/n8/b1` | 0.0006 | 0.0025 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3937 | 0.2051 | 0.4489 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0047 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 1.9708 | 0.9986 | 3.0349 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0023 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2493 | 0.0709 | 0.8080 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0033 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6685 | 0.3421 | 1.4015 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0028 | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7825 | 0.4009 | 1.1730 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0028 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0966 | 0.0347 | 0.5906 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0028 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2812 | 0.0818 | 0.8155 |
| `qr/n16/b1` | 0.0066 | 0.0092 | 0.0077 |
| `qr/n16/b1024` | 6.4449 | 3.2457 | 7.6100 |
| `qr/n4/b1` | 0.0007 | 0.0033 | 0.0012 |
| `qr/n4/b1024` | 0.4994 | 0.2563 | 0.8663 |
| `qr/n8/b1` | 0.0018 | 0.0041 | 0.0026 |
| `qr/n8/b1024` | 1.5507 | 0.7745 | 2.3035 |
| `rank_revealing_qr/n16/b1` | 0.0077 | 0.0104 | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.1295 | 2.4580 | 10.1183 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0035 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8143 | 0.4188 | 1.1157 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0055 | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1515 | 1.1057 | 3.0440 |
| `solve/n16/b1` | 0.0027 | 0.0051 | 0.0031 |
| `solve/n16/b1024` | 2.0838 | 0.5413 | 3.1479 |
| `solve/n4/b1` | 0.0007 | 0.0024 | 0.0008 |
| `solve/n4/b1024` | 0.3140 | 0.0846 | 0.8384 |
| `solve/n8/b1` | 0.0012 | 0.0036 | 0.0014 |
| `solve/n8/b1024` | 0.7667 | 0.3865 | 1.3712 |
| `svd_full/n16/b1` | 0.0347 | 0.0379 | 0.0595 |
| `svd_full/n16/b1024` | 36.2763 | 14.6063 | 64.2878 |
| `svd_full/n4/b1` | 0.0031 | 0.0063 | 0.0060 |
| `svd_full/n4/b1024` | 3.0061 | 1.1396 | 5.0416 |
| `svd_full/n8/b1` | 0.0097 | 0.0122 | 0.0161 |
| `svd_full/n8/b1024` | 10.2137 | 2.5392 | 16.0802 |
| `svd_thin/n16/b1` | 0.0349 | 0.0379 | 0.0591 |
| `svd_thin/n16/b1024` | 36.3323 | 9.2649 | 64.2875 |
| `svd_thin/n4/b1` | 0.0031 | 0.0055 | 0.0059 |
| `svd_thin/n4/b1024` | 3.0070 | 0.7544 | 5.0667 |
| `svd_thin/n8/b1` | 0.0096 | 0.0122 | 0.0160 |
| `svd_thin/n8/b1024` | 10.1365 | 2.5743 | 16.0415 |
| `svd_values/n16/b1` | 0.0296 | 0.0332 | 0.0234 |
| `svd_values/n16/b1024` | 32.9866 | 13.3000 | 25.6040 |
| `svd_values/n4/b1` | 0.0029 | 0.0052 | 0.0039 |
| `svd_values/n4/b1024` | 2.6432 | 1.7532 | 3.0912 |
| `svd_values/n8/b1` | 0.0088 | 0.0116 | 0.0084 |
| `svd_values/n8/b1024` | 8.8077 | 3.6224 | 7.8304 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0029 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5863 | 0.2954 | 0.7534 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0958 | 0.0512 | 0.4170 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0029 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2359 | 0.1224 | 0.5243 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0027 | 0.0010 |
| `cholesky/n16/b1024` | 0.7970 | 0.2014 | 1.0041 |
| `cholesky/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1204 | 0.0238 | 0.1392 |
| `cholesky/n8/b1` | 0.0004 | 0.0034 | 0.0004 |
| `cholesky/n8/b1024` | 0.2579 | 0.0664 | 0.2945 |
| `eig/n16/b1` | 0.0750 | 0.0805 | 0.1044 |
| `eig/n16/b1024` | 81.3305 | 15.0900 | 125.5854 |
| `eig/n4/b1` | 0.0063 | 0.0091 | 0.0091 |
| `eig/n4/b1024` | 6.0958 | 1.6315 | 8.2829 |
| `eig/n8/b1` | 0.0209 | 0.0245 | 0.0278 |
| `eig/n8/b1024` | 21.5047 | 4.8562 | 29.0229 |
| `eigh/n16/b1` | 0.0180 | 0.0209 | 0.0265 |
| `eigh/n16/b1024` | 19.3544 | 2.8702 | 27.1863 |
| `eigh/n4/b1` | 0.0020 | 0.0052 | 0.0024 |
| `eigh/n4/b1024` | 1.7422 | 0.4442 | 2.2307 |
| `eigh/n8/b1` | 0.0057 | 0.0083 | 0.0075 |
| `eigh/n8/b1024` | 5.4610 | 0.7325 | 7.5269 |
| `eigvals/n16/b1` | 0.0474 | 0.0509 | 0.0789 |
| `eigvals/n16/b1024` | 52.3644 | 12.2823 | 95.2759 |
| `eigvals/n4/b1` | 0.0036 | 0.0060 | 0.0072 |
| `eigvals/n4/b1024` | 3.1396 | 1.0673 | 6.3562 |
| `eigvals/n8/b1` | 0.0128 | 0.0160 | 0.0226 |
| `eigvals/n8/b1024` | 13.0740 | 2.9771 | 23.1588 |
| `eigvalsh/n16/b1` | 0.0207 | 0.0259 | 0.0118 |
| `eigvalsh/n16/b1024` | 23.4110 | 11.9318 | 11.6338 |
| `eigvalsh/n4/b1` | 0.0023 | 0.0055 | 0.0016 |
| `eigvalsh/n4/b1024` | 1.8750 | 0.8453 | 1.2736 |
| `eigvalsh/n8/b1` | 0.0064 | 0.0091 | 0.0041 |
| `eigvalsh/n8/b1024` | 5.8971 | 2.7228 | 3.7243 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0065 | 0.0121 |
| `full_piv_lu/n16/b1024` | 2.8857 | 0.7321 | 20.1092 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0023 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2654 | 0.0721 | 0.5440 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0037 | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.7655 | 0.2003 | 2.3478 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0060 | 0.0154 |
| `full_piv_lu_solve/n16/b1024` | 3.0892 | 0.4003 | 22.6382 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0039 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4779 | 0.0723 | 1.2841 |
| `full_piv_lu_solve/n8/b1` | 0.0017 | 0.0048 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1502 | 0.3057 | 3.6829 |
| `householder_apply/n16/b1` | 0.0026 | 0.0049 | 0.0045 |
| `householder_apply/n16/b1024` | 3.2030 | 0.6783 | 4.5123 |
| `householder_apply/n4/b1` | 0.0003 | 0.0025 | 0.0009 |
| `householder_apply/n4/b1024` | 0.1809 | 0.0339 | 0.2593 |
| `householder_apply/n8/b1` | 0.0007 | 0.0031 | 0.0015 |
| `householder_apply/n8/b1024` | 0.6178 | 0.1574 | 0.8866 |
| `householder_factor/n16/b1` | 0.0026 | 0.0053 | 0.0045 |
| `householder_factor/n16/b1024` | 2.5417 | 0.4737 | 4.4057 |
| `householder_factor/n4/b1` | 0.0004 | 0.0025 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3052 | 0.0482 | 0.5550 |
| `householder_factor/n8/b1` | 0.0009 | 0.0039 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8015 | 0.2100 | 1.4243 |
| `lu/n16/b1` | 0.0021 | 0.0054 | 0.0023 |
| `lu/n16/b1024` | 1.8472 | 0.4587 | 2.2852 |
| `lu/n4/b1` | 0.0005 | 0.0023 | 0.0004 |
| `lu/n4/b1024` | 0.2047 | 0.0355 | 0.2337 |
| `lu/n8/b1` | 0.0008 | 0.0032 | 0.0008 |
| `lu/n8/b1024` | 0.5240 | 0.0735 | 0.6481 |
| `lu_factor/n16/b1` | 0.0014 | 0.0042 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2466 | 0.3168 | 1.6300 |
| `lu_factor/n4/b1` | 0.0004 | 0.0022 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1626 | 0.0455 | 0.1632 |
| `lu_factor/n8/b1` | 0.0006 | 0.0039 | 0.0005 |
| `lu_factor/n8/b1024` | 0.3924 | 0.1070 | 0.4559 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0053 | 0.0027 |
| `lu_factor_solve/n16/b1024` | 1.9923 | 0.5030 | 3.0266 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0025 | 0.0009 |
| `lu_factor_solve/n4/b1024` | 0.2529 | 0.0702 | 0.8772 |
| `lu_factor_solve/n8/b1` | 0.0009 | 0.0040 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6675 | 0.1742 | 1.4083 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0040 | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7757 | 0.2060 | 1.1808 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0039 | 0.0007 |
| `lu_solve_prepared/n4/b1024` | 0.0967 | 0.0304 | 0.6088 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0024 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2825 | 0.0846 | 0.7940 |
| `qr/n16/b1` | 0.0067 | 0.0099 | 0.0078 |
| `qr/n16/b1024` | 6.5319 | 1.3649 | 7.6225 |
| `qr/n4/b1` | 0.0007 | 0.0038 | 0.0012 |
| `qr/n4/b1024` | 0.5010 | 0.0716 | 0.8747 |
| `qr/n8/b1` | 0.0019 | 0.0046 | 0.0026 |
| `qr/n8/b1024` | 1.5363 | 0.2291 | 2.3129 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0105 | 0.0100 |
| `rank_revealing_qr/n16/b1024` | 7.2203 | 1.8342 | 10.1733 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0042 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8163 | 0.2124 | 1.1219 |
| `rank_revealing_qr/n8/b1` | 0.0024 | 0.0056 | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1620 | 0.2752 | 3.0425 |
| `solve/n16/b1` | 0.0027 | 0.0058 | 0.0030 |
| `solve/n16/b1024` | 2.1205 | 0.5337 | 3.2243 |
| `solve/n4/b1` | 0.0007 | 0.0025 | 0.0009 |
| `solve/n4/b1024` | 0.3111 | 0.0837 | 0.8963 |
| `solve/n8/b1` | 0.0012 | 0.0040 | 0.0015 |
| `solve/n8/b1024` | 0.7515 | 0.1967 | 1.4269 |
| `svd_full/n16/b1` | 0.0347 | 0.0374 | 0.0588 |
| `svd_full/n16/b1024` | 36.9241 | 7.6402 | 64.0654 |
| `svd_full/n4/b1` | 0.0031 | 0.0061 | 0.0060 |
| `svd_full/n4/b1024` | 2.9834 | 0.7558 | 5.0344 |
| `svd_full/n8/b1` | 0.0097 | 0.0130 | 0.0160 |
| `svd_full/n8/b1024` | 10.1382 | 1.3222 | 15.9129 |
| `svd_thin/n16/b1` | 0.0347 | 0.0377 | 0.0592 |
| `svd_thin/n16/b1024` | 36.3721 | 4.7108 | 64.3718 |
| `svd_thin/n4/b1` | 0.0031 | 0.0060 | 0.0061 |
| `svd_thin/n4/b1024` | 2.9906 | 0.7556 | 5.0388 |
| `svd_thin/n8/b1` | 0.0096 | 0.0126 | 0.0161 |
| `svd_thin/n8/b1024` | 10.0700 | 1.3120 | 15.9564 |
| `svd_values/n16/b1` | 0.0295 | 0.0333 | 0.0236 |
| `svd_values/n16/b1024` | 33.0844 | 9.9084 | 25.6453 |
| `svd_values/n4/b1` | 0.0030 | 0.0059 | 0.0039 |
| `svd_values/n4/b1024` | 2.6334 | 0.6474 | 3.1569 |
| `svd_values/n8/b1` | 0.0087 | 0.0116 | 0.0084 |
| `svd_values/n8/b1024` | 8.8130 | 2.9470 | 7.7792 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0031 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5895 | 0.1538 | 0.8343 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0023 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0950 | 0.0283 | 0.4617 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0030 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2362 | 0.0412 | 0.5914 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0398 | - | 0.0409 |
| `cholesky/n128/b128` | 5.9539 | - | 6.3138 |
| `cholesky/n32/b1` | 0.0021 | - | 0.0020 |
| `cholesky/n32/b128` | 0.2558 | - | 0.2534 |
| `eigh/n128/b1` | 1.2625 | - | 1.1253 |
| `eigh/n128/b128` | 162.2699 | - | 147.7231 |
| `eigh/n32/b1` | 0.0641 | - | 0.0783 |
| `eigh/n32/b128` | 8.4312 | - | 9.9902 |
| `eigvalsh/n128/b1` | 2.4408 | - | 0.5031 |
| `eigvalsh/n128/b128` | 322.2803 | - | 65.2274 |
| `eigvalsh/n32/b1` | 0.0830 | - | 0.0291 |
| `eigvalsh/n32/b128` | 10.7500 | - | 3.7758 |
| `householder_apply/n128/b1` | 0.3025 | - | 0.2510 |
| `householder_apply/n128/b128` | 41.1213 | - | 34.6278 |
| `householder_apply/n32/b1` | 0.0106 | - | 0.0110 |
| `householder_apply/n32/b128` | 1.3472 | - | 1.3661 |
| `householder_factor/n128/b1` | 0.1939 | - | 0.2180 |
| `householder_factor/n128/b128` | 25.2740 | - | 28.5902 |
| `householder_factor/n32/b1` | 0.0071 | - | 0.0085 |
| `householder_factor/n32/b128` | 0.8965 | - | 1.0770 |
| `lu/n128/b1` | 0.0893 | - | 0.0881 |
| `lu/n128/b128` | 12.1839 | - | 13.5925 |
| `lu/n32/b1` | 0.0053 | - | 0.0051 |
| `lu/n32/b128` | 0.6000 | - | 0.6192 |
| `lu_factor/n128/b1` | 0.0562 | - | 0.0777 |
| `lu_factor/n128/b128` | 8.2253 | - | 11.1212 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0040 |
| `lu_factor/n32/b128` | 0.3831 | - | 0.5055 |
| `lu_factor_solve/n128/b1` | 0.0627 | - | 0.0904 |
| `lu_factor_solve/n128/b128` | 8.9590 | - | 12.5006 |
| `lu_factor_solve/n32/b1` | 0.0041 | - | 0.0057 |
| `lu_factor_solve/n32/b128` | 0.4868 | - | 0.7301 |
| `lu_solve_prepared/n128/b1` | 0.0060 | - | 0.0119 |
| `lu_solve_prepared/n128/b128` | 1.8678 | - | 2.7528 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0016 |
| `lu_solve_prepared/n32/b128` | 0.1153 | - | 0.2001 |
| `qr/n128/b1` | 0.3426 | - | 0.4331 |
| `qr/n128/b128` | 44.1530 | - | 57.3188 |
| `qr/n32/b1` | 0.0209 | - | 0.0161 |
| `qr/n32/b128` | 2.6249 | - | 2.0284 |
| `rank_revealing_qr/n128/b1` | 0.3492 | - | 0.4912 |
| `rank_revealing_qr/n128/b128` | 45.4987 | - | 64.9333 |
| `rank_revealing_qr/n32/b1` | 0.0210 | - | 0.0199 |
| `rank_revealing_qr/n32/b128` | 2.5916 | - | 2.4602 |
| `solve/n128/b1` | 0.0662 | - | 0.0937 |
| `solve/n128/b128` | 8.7588 | - | 12.7364 |
| `solve/n32/b1` | 0.0048 | - | 0.0062 |
| `solve/n32/b128` | 0.5166 | - | 0.7579 |
| `svd_thin/n128/b1` | 2.4106 | - | 2.1683 |
| `svd_thin/n128/b128` | 307.1038 | - | 299.7880 |
| `svd_thin/n32/b1` | 0.1180 | - | 0.1491 |
| `svd_thin/n32/b128` | 15.1706 | - | 19.0493 |
| `svd_values/n128/b1` | 1.5492 | - | 0.9321 |
| `svd_values/n128/b128` | 206.0001 | - | 131.7407 |
| `svd_values/n32/b1` | 0.1022 | - | 0.0552 |
| `svd_values/n32/b128` | 13.0903 | - | 7.1336 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0061 |
| `triangular_solve/n128/b128` | 1.1015 | - | 1.4761 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0010 |
| `triangular_solve/n32/b128` | 0.0882 | - | 0.1082 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0394 | 0.0493 | 0.0465 |
| `cholesky/n128/b128` | 5.9257 | 7.0043 | 6.9642 |
| `cholesky/n32/b1` | 0.0021 | 0.0044 | 0.0020 |
| `cholesky/n32/b128` | 0.2561 | 0.1299 | 0.2496 |
| `eigh/n128/b1` | 1.2592 | 1.2306 | 0.9037 |
| `eigh/n128/b128` | 161.9743 | 163.9229 | 117.2251 |
| `eigh/n32/b1` | 0.0644 | 0.0674 | 0.0695 |
| `eigh/n32/b128` | 8.4352 | 2.7279 | 8.9955 |
| `eigvalsh/n128/b1` | 2.4392 | 3.1723 | 0.4763 |
| `eigvalsh/n128/b128` | 321.5907 | 322.9014 | 61.7468 |
| `eigvalsh/n32/b1` | 0.0828 | 0.0884 | 0.0291 |
| `eigvalsh/n32/b128` | 10.7379 | 6.2975 | 3.7539 |
| `householder_apply/n128/b1` | 0.3048 | 0.3083 | 0.2327 |
| `householder_apply/n128/b128` | 42.0835 | 42.3590 | 31.4845 |
| `householder_apply/n32/b1` | 0.0103 | 0.0129 | 0.0110 |
| `householder_apply/n32/b128` | 1.2992 | 0.3365 | 1.3617 |
| `householder_factor/n128/b1` | 0.1939 | 0.1997 | 0.2276 |
| `householder_factor/n128/b128` | 25.0642 | 25.2402 | 29.4847 |
| `householder_factor/n32/b1` | 0.0071 | 0.0098 | 0.0087 |
| `householder_factor/n32/b128` | 0.8782 | 0.2303 | 1.0861 |
| `lu/n128/b1` | 0.0867 | 0.1018 | 0.0875 |
| `lu/n128/b128` | 12.3824 | 13.7880 | 13.6616 |
| `lu/n32/b1` | 0.0053 | 0.0085 | 0.0051 |
| `lu/n32/b128` | 0.6033 | 0.3035 | 0.6196 |
| `lu_factor/n128/b1` | 0.0566 | 0.0699 | 0.0787 |
| `lu_factor/n128/b128` | 8.2658 | 2.5123 | 11.2199 |
| `lu_factor/n32/b1` | 0.0033 | 0.0049 | 0.0040 |
| `lu_factor/n32/b128` | 0.3874 | 0.2048 | 0.5182 |
| `lu_factor_solve/n128/b1` | 0.0624 | 0.0776 | 0.0882 |
| `lu_factor_solve/n128/b128` | 8.9112 | 5.0003 | 12.2874 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0077 | 0.0054 |
| `lu_factor_solve/n32/b128` | 0.4933 | 0.2580 | 0.7259 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0085 | 0.0071 |
| `lu_solve_prepared/n128/b128` | 1.7486 | 0.5018 | 2.2138 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0034 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1144 | 0.0351 | 0.1472 |
| `qr/n128/b1` | 0.3411 | 0.6153 | 0.4556 |
| `qr/n128/b128` | 43.9041 | 81.1480 | 59.8674 |
| `qr/n32/b1` | 0.0208 | 0.0471 | 0.0160 |
| `qr/n32/b128` | 2.6042 | 0.6553 | 1.9854 |
| `rank_revealing_qr/n128/b1` | 0.3472 | 0.3651 | 0.5162 |
| `rank_revealing_qr/n128/b128` | 44.6026 | 47.8994 | 67.4411 |
| `rank_revealing_qr/n32/b1` | 0.0207 | 0.0447 | 0.0196 |
| `rank_revealing_qr/n32/b128` | 2.5803 | 0.6499 | 2.4732 |
| `solve/n128/b1` | 0.0667 | 0.0808 | 0.0909 |
| `solve/n128/b128` | 8.7248 | 10.4688 | 12.3714 |
| `solve/n32/b1` | 0.0047 | 0.0084 | 0.0059 |
| `solve/n32/b128` | 0.5188 | 0.2664 | 0.7369 |
| `svd_thin/n128/b1` | 2.4084 | 1.8166 | 2.1368 |
| `svd_thin/n128/b128` | 306.4820 | 230.7493 | 295.0495 |
| `svd_thin/n32/b1` | 0.1167 | 0.1240 | 0.1479 |
| `svd_thin/n32/b128` | 15.0452 | 3.8552 | 18.9760 |
| `svd_values/n128/b1` | 1.5474 | 1.6848 | 0.9614 |
| `svd_values/n128/b128` | 205.4288 | 208.7604 | 133.8058 |
| `svd_values/n32/b1` | 0.1011 | 0.1083 | 0.0551 |
| `svd_values/n32/b128` | 13.0306 | 4.9639 | 7.1124 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0068 | 0.0040 |
| `triangular_solve/n128/b128` | 1.0805 | 1.1607 | 1.3539 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0035 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0877 | 0.0271 | 0.0995 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0398 | 0.0551 | 0.0466 |
| `cholesky/n128/b128` | 5.9345 | 7.2945 | 6.9426 |
| `cholesky/n32/b1` | 0.0021 | 0.0053 | 0.0020 |
| `cholesky/n32/b128` | 0.2558 | 0.0365 | 0.2524 |
| `eigh/n128/b1` | 1.2611 | 1.2393 | 0.8708 |
| `eigh/n128/b128` | 162.7890 | 159.9707 | 112.7956 |
| `eigh/n32/b1` | 0.0638 | 0.0670 | 0.0703 |
| `eigh/n32/b128` | 8.4117 | 1.1271 | 8.8895 |
| `eigvalsh/n128/b1` | 2.4380 | 3.1158 | 0.4719 |
| `eigvalsh/n128/b128` | 322.2339 | 323.9766 | 60.9440 |
| `eigvalsh/n32/b1` | 0.0826 | 0.0883 | 0.0289 |
| `eigvalsh/n32/b128` | 10.7489 | 5.9519 | 3.7622 |
| `householder_apply/n128/b1` | 0.3122 | 0.3205 | 0.2373 |
| `householder_apply/n128/b128` | 41.2081 | 42.0258 | 31.5290 |
| `householder_apply/n32/b1` | 0.0105 | 0.0244 | 0.0107 |
| `householder_apply/n32/b128` | 1.3104 | 0.3325 | 1.3334 |
| `householder_factor/n128/b1` | 0.1968 | 0.2011 | 0.2325 |
| `householder_factor/n128/b128` | 25.3300 | 25.4866 | 30.0938 |
| `householder_factor/n32/b1` | 0.0070 | 0.0100 | 0.0086 |
| `householder_factor/n32/b128` | 0.8832 | 0.2314 | 1.0801 |
| `lu/n128/b1` | 0.0863 | 0.1112 | 0.0869 |
| `lu/n128/b128` | 12.2781 | 15.2471 | 13.5563 |
| `lu/n32/b1` | 0.0052 | 0.0086 | 0.0050 |
| `lu/n32/b128` | 0.5690 | 0.1589 | 0.6213 |
| `lu_factor/n128/b1` | 0.0556 | 0.0821 | 0.0780 |
| `lu_factor/n128/b128` | 8.2170 | 1.9948 | 11.2051 |
| `lu_factor/n32/b1` | 0.0032 | 0.0055 | 0.0040 |
| `lu_factor/n32/b128` | 0.3899 | 0.1084 | 0.5088 |
| `lu_factor_solve/n128/b1` | 0.0624 | 0.0894 | 0.0874 |
| `lu_factor_solve/n128/b128` | 8.9575 | 1.5663 | 12.2609 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0076 | 0.0055 |
| `lu_factor_solve/n32/b128` | 0.4914 | 0.1314 | 0.7399 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0086 | 0.0071 |
| `lu_solve_prepared/n128/b128` | 2.0575 | 0.3143 | 2.1088 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0036 | 0.0011 |
| `lu_solve_prepared/n32/b128` | 0.1138 | 0.0335 | 0.1588 |
| `qr/n128/b1` | 0.3414 | 0.9070 | 0.4686 |
| `qr/n128/b128` | 43.8742 | 122.1916 | 60.1904 |
| `qr/n32/b1` | 0.0207 | 0.0647 | 0.0157 |
| `qr/n32/b128` | 2.5884 | 0.6178 | 1.9924 |
| `rank_revealing_qr/n128/b1` | 0.3537 | 0.4289 | 0.5288 |
| `rank_revealing_qr/n128/b128` | 45.1948 | 56.5447 | 67.5814 |
| `rank_revealing_qr/n32/b1` | 0.0206 | 0.0669 | 0.0197 |
| `rank_revealing_qr/n32/b128` | 2.5722 | 0.3394 | 2.4678 |
| `solve/n128/b1` | 0.0670 | 0.0946 | 0.0924 |
| `solve/n128/b128` | 8.7622 | 11.9458 | 12.3503 |
| `solve/n32/b1` | 0.0048 | 0.0074 | 0.0060 |
| `solve/n32/b128` | 0.5297 | 0.0752 | 0.7386 |
| `svd_thin/n128/b1` | 2.4171 | 1.8599 | 2.1560 |
| `svd_thin/n128/b128` | 307.1959 | 238.0907 | 292.2434 |
| `svd_thin/n32/b1` | 0.1166 | 0.1224 | 0.1492 |
| `svd_thin/n32/b128` | 15.0382 | 2.2771 | 19.0864 |
| `svd_values/n128/b1` | 1.5473 | 1.7523 | 0.9930 |
| `svd_values/n128/b128` | 205.8239 | 209.0225 | 134.6402 |
| `svd_values/n32/b1` | 0.1016 | 0.1090 | 0.0554 |
| `svd_values/n32/b128` | 13.0817 | 3.9212 | 7.1492 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0066 | 0.0041 |
| `triangular_solve/n128/b128` | 0.8958 | 0.9138 | 1.1684 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0044 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0902 | 0.0256 | 0.1059 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1087 | - | 0.1077 |
| `cholesky/n128/b128` | 16.0244 | - | 15.4682 |
| `cholesky/n32/b1` | 0.0034 | - | 0.0034 |
| `cholesky/n32/b128` | 0.4298 | - | 0.4349 |
| `eigh/n128/b1` | 1.8507 | - | 3.2655 |
| `eigh/n128/b128` | 241.4653 | - | 421.7787 |
| `eigh/n32/b1` | 0.0804 | - | 0.1081 |
| `eigh/n32/b128` | 10.4699 | - | 13.9807 |
| `eigvalsh/n128/b1` | 2.7181 | - | 0.9518 |
| `eigvalsh/n128/b128` | 371.3169 | - | 123.4835 |
| `eigvalsh/n32/b1` | 0.0898 | - | 0.0422 |
| `eigvalsh/n32/b128` | 11.6762 | - | 5.4701 |
| `householder_apply/n128/b1` | 0.6847 | - | 0.6905 |
| `householder_apply/n128/b128` | 92.7050 | - | 91.4551 |
| `householder_apply/n32/b1` | 0.0143 | - | 0.0198 |
| `householder_apply/n32/b128` | 1.8185 | - | 2.5062 |
| `householder_factor/n128/b1` | 0.4528 | - | 0.4350 |
| `householder_factor/n128/b128` | 58.7048 | - | 57.1607 |
| `householder_factor/n32/b1` | 0.0111 | - | 0.0159 |
| `householder_factor/n32/b128` | 1.4041 | - | 2.0072 |
| `lu/n128/b1` | 0.2010 | - | 0.2115 |
| `lu/n128/b128` | 28.2883 | - | 31.3894 |
| `lu/n32/b1` | 0.0076 | - | 0.0080 |
| `lu/n32/b128` | 0.9919 | - | 1.0984 |
| `lu_factor/n128/b1` | 0.1551 | - | 0.1917 |
| `lu_factor/n128/b128` | 21.8012 | - | 25.4894 |
| `lu_factor/n32/b1` | 0.0053 | - | 0.0064 |
| `lu_factor/n32/b128` | 0.6444 | - | 0.8161 |
| `lu_factor_solve/n128/b1` | 0.1734 | - | 0.2176 |
| `lu_factor_solve/n128/b128` | 24.2779 | - | 29.2064 |
| `lu_factor_solve/n32/b1` | 0.0075 | - | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9151 | - | 1.1304 |
| `lu_solve_prepared/n128/b1` | 0.0187 | - | 0.0266 |
| `lu_solve_prepared/n128/b128` | 4.2145 | - | 5.1730 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.2853 | - | 0.3120 |
| `qr/n128/b1` | 0.9685 | - | 0.8634 |
| `qr/n128/b128` | 124.9870 | - | 115.1135 |
| `qr/n32/b1` | 0.0425 | - | 0.0290 |
| `qr/n32/b128` | 5.4221 | - | 3.7217 |
| `rank_revealing_qr/n128/b1` | 1.0120 | - | 0.9884 |
| `rank_revealing_qr/n128/b128` | 130.2093 | - | 132.3904 |
| `rank_revealing_qr/n32/b1` | 0.0388 | - | 0.0367 |
| `rank_revealing_qr/n32/b128` | 4.9358 | - | 4.9048 |
| `solve/n128/b1` | 0.1799 | - | 0.2289 |
| `solve/n128/b128` | 23.7798 | - | 29.8444 |
| `solve/n32/b1` | 0.0083 | - | 0.0094 |
| `solve/n32/b128` | 0.9591 | - | 1.1747 |
| `svd_thin/n128/b1` | 3.9121 | - | 3.7277 |
| `svd_thin/n128/b128` | 504.6152 | - | 520.3187 |
| `svd_thin/n32/b1` | 0.1515 | - | 0.1805 |
| `svd_thin/n32/b128` | 19.7512 | - | 23.9593 |
| `svd_values/n128/b1` | 2.0867 | - | 1.5966 |
| `svd_values/n128/b128` | 289.6570 | - | 227.3916 |
| `svd_values/n32/b1` | 0.1136 | - | 0.0768 |
| `svd_values/n32/b128` | 14.8770 | - | 9.8947 |
| `triangular_solve/n128/b1` | 0.0109 | - | 0.0141 |
| `triangular_solve/n128/b128` | 2.2841 | - | 2.9489 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0013 |
| `triangular_solve/n32/b128` | 0.1913 | - | 0.1613 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1062 | 0.1065 | 0.0705 |
| `cholesky/n128/b128` | 15.9796 | 15.4967 | 11.3247 |
| `cholesky/n32/b1` | 0.0033 | 0.0060 | 0.0034 |
| `cholesky/n32/b128` | 0.4312 | 0.2212 | 0.4351 |
| `eigh/n128/b1` | 1.8525 | 1.5915 | 3.1674 |
| `eigh/n128/b128` | 242.2083 | 228.3280 | 409.2326 |
| `eigh/n32/b1` | 0.0803 | 0.0848 | 0.1081 |
| `eigh/n32/b128` | 10.4737 | 2.6948 | 14.0123 |
| `eigvalsh/n128/b1` | 2.7203 | 3.9592 | 0.8914 |
| `eigvalsh/n128/b128` | 371.3112 | 372.4048 | 115.7114 |
| `eigvalsh/n32/b1` | 0.0898 | 0.0963 | 0.0421 |
| `eigvalsh/n32/b128` | 11.6727 | 6.9856 | 5.4441 |
| `householder_apply/n128/b1` | 0.6847 | 0.6870 | 0.3711 |
| `householder_apply/n128/b128` | 92.4787 | 93.1572 | 50.2183 |
| `householder_apply/n32/b1` | 0.0141 | 0.0173 | 0.0197 |
| `householder_apply/n32/b128` | 1.8077 | 0.4524 | 2.4586 |
| `householder_factor/n128/b1` | 0.4578 | 0.4600 | 0.3824 |
| `householder_factor/n128/b128` | 59.0632 | 59.0266 | 50.3251 |
| `householder_factor/n32/b1` | 0.0111 | 0.0138 | 0.0158 |
| `householder_factor/n32/b128` | 1.4191 | 0.7165 | 1.9765 |
| `lu/n128/b1` | 0.1958 | 0.1852 | 0.1449 |
| `lu/n128/b128` | 27.5063 | 25.8463 | 22.0364 |
| `lu/n32/b1` | 0.0074 | 0.0104 | 0.0080 |
| `lu/n32/b128` | 0.9688 | 0.4724 | 1.1066 |
| `lu_factor/n128/b1` | 0.1556 | 0.1447 | 0.1187 |
| `lu_factor/n128/b128` | 21.8292 | 6.1543 | 15.4724 |
| `lu_factor/n32/b1` | 0.0053 | 0.0084 | 0.0065 |
| `lu_factor/n32/b128` | 0.6513 | 0.3322 | 0.8241 |
| `lu_factor_solve/n128/b1` | 0.1743 | 0.1642 | 0.1380 |
| `lu_factor_solve/n128/b128` | 24.2483 | 6.5709 | 18.1260 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0107 | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9220 | 0.4678 | 1.1470 |
| `lu_solve_prepared/n128/b1` | 0.0187 | 0.0218 | 0.0177 |
| `lu_solve_prepared/n128/b128` | 4.2526 | 1.2213 | 4.0488 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0052 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2849 | 0.0797 | 0.2320 |
| `qr/n128/b1` | 0.9681 | 0.8764 | 0.7672 |
| `qr/n128/b128` | 124.8203 | 113.8305 | 101.1236 |
| `qr/n32/b1` | 0.0424 | 0.0699 | 0.0290 |
| `qr/n32/b128` | 5.3873 | 1.7856 | 3.6641 |
| `rank_revealing_qr/n128/b1` | 1.0139 | 0.8072 | 0.9059 |
| `rank_revealing_qr/n128/b128` | 130.5666 | 104.5980 | 121.2122 |
| `rank_revealing_qr/n32/b1` | 0.0387 | 0.0629 | 0.0365 |
| `rank_revealing_qr/n32/b128` | 4.8808 | 2.4861 | 4.8616 |
| `solve/n128/b1` | 0.1791 | 0.1685 | 0.1446 |
| `solve/n128/b128` | 23.7057 | 22.0652 | 19.1118 |
| `solve/n32/b1` | 0.0082 | 0.0111 | 0.0094 |
| `solve/n32/b128` | 0.9737 | 0.4861 | 1.2062 |
| `svd_thin/n128/b1` | 3.9203 | 2.7110 | 3.2230 |
| `svd_thin/n128/b128` | 505.3592 | 349.8475 | 451.9911 |
| `svd_thin/n32/b1` | 0.1496 | 0.1544 | 0.1801 |
| `svd_thin/n32/b128` | 19.4828 | 4.8934 | 23.7976 |
| `svd_values/n128/b1` | 2.0773 | 2.3262 | 1.7139 |
| `svd_values/n128/b128` | 290.1356 | 288.0490 | 238.6224 |
| `svd_values/n32/b1` | 0.1136 | 0.1210 | 0.0764 |
| `svd_values/n32/b128` | 14.8484 | 6.0007 | 9.8593 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0138 | 0.0090 |
| `triangular_solve/n128/b128` | 2.2656 | 2.1321 | 2.5560 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0035 | 0.0014 |
| `triangular_solve/n32/b128` | 0.1924 | 0.0990 | 0.1705 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1070 | 0.1148 | 0.0939 |
| `cholesky/n128/b128` | 15.9506 | 16.6476 | 13.7969 |
| `cholesky/n32/b1` | 0.0033 | 0.0064 | 0.0034 |
| `cholesky/n32/b128` | 0.4227 | 0.0579 | 0.4348 |
| `eigh/n128/b1` | 1.8527 | 1.6207 | 3.1752 |
| `eigh/n128/b128` | 241.7347 | 212.4712 | 408.6145 |
| `eigh/n32/b1` | 0.0798 | 0.0849 | 0.1085 |
| `eigh/n32/b128` | 10.4911 | 2.1521 | 14.0339 |
| `eigvalsh/n128/b1` | 2.7249 | 3.9642 | 0.8896 |
| `eigvalsh/n128/b128` | 371.1710 | 371.9222 | 115.2226 |
| `eigvalsh/n32/b1` | 0.0900 | 0.0977 | 0.0422 |
| `eigvalsh/n32/b128` | 11.6602 | 6.0775 | 5.4883 |
| `householder_apply/n128/b1` | 0.6862 | 0.6926 | 0.3270 |
| `householder_apply/n128/b128` | 92.9609 | 93.2163 | 44.6037 |
| `householder_apply/n32/b1` | 0.0142 | 0.0171 | 0.0196 |
| `householder_apply/n32/b128` | 1.8418 | 0.2362 | 2.4890 |
| `householder_factor/n128/b1` | 0.4569 | 0.4632 | 0.3835 |
| `householder_factor/n128/b128` | 59.1646 | 59.0348 | 50.1390 |
| `householder_factor/n32/b1` | 0.0112 | 0.0134 | 0.0158 |
| `householder_factor/n32/b128` | 1.4163 | 0.3585 | 1.9910 |
| `lu/n128/b1` | 0.1949 | 0.1945 | 0.1418 |
| `lu/n128/b128` | 27.6474 | 27.3904 | 21.4989 |
| `lu/n32/b1` | 0.0076 | 0.0103 | 0.0080 |
| `lu/n32/b128` | 0.9813 | 0.2290 | 1.0995 |
| `lu_factor/n128/b1` | 0.1558 | 0.1556 | 0.1140 |
| `lu_factor/n128/b128` | 21.7892 | 3.4087 | 14.7884 |
| `lu_factor/n32/b1` | 0.0053 | 0.0088 | 0.0064 |
| `lu_factor/n32/b128` | 0.6425 | 0.1720 | 0.8206 |
| `lu_factor_solve/n128/b1` | 0.1748 | 0.1747 | 0.1343 |
| `lu_factor_solve/n128/b128` | 24.2373 | 3.5476 | 17.4618 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0100 | 0.0086 |
| `lu_factor_solve/n32/b128` | 0.9144 | 0.2388 | 1.1453 |
| `lu_solve_prepared/n128/b1` | 0.0188 | 0.0217 | 0.0177 |
| `lu_solve_prepared/n128/b128` | 4.2288 | 0.9124 | 4.0683 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0052 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2804 | 0.0436 | 0.2543 |
| `qr/n128/b1` | 0.9689 | 1.2056 | 0.7546 |
| `qr/n128/b128` | 125.0023 | 153.8109 | 99.4292 |
| `qr/n32/b1` | 0.0423 | 0.0886 | 0.0287 |
| `qr/n32/b128` | 5.3788 | 0.6801 | 3.6554 |
| `rank_revealing_qr/n128/b1` | 1.0115 | 0.8809 | 0.8988 |
| `rank_revealing_qr/n128/b128` | 130.2945 | 114.4086 | 120.1601 |
| `rank_revealing_qr/n32/b1` | 0.0387 | 0.0843 | 0.0363 |
| `rank_revealing_qr/n32/b128` | 4.9422 | 0.6193 | 4.8506 |
| `solve/n128/b1` | 0.1803 | 0.1809 | 0.1428 |
| `solve/n128/b128` | 23.8146 | 23.5177 | 19.2057 |
| `solve/n32/b1` | 0.0082 | 0.0110 | 0.0096 |
| `solve/n32/b128` | 0.9547 | 0.2456 | 1.2062 |
| `svd_thin/n128/b1` | 3.9201 | 2.7481 | 3.1747 |
| `svd_thin/n128/b128` | 506.3457 | 356.9608 | 446.9430 |
| `svd_thin/n32/b1` | 0.1520 | 0.1546 | 0.1802 |
| `svd_thin/n32/b128` | 19.5645 | 2.4740 | 23.8382 |
| `svd_values/n128/b1` | 2.0783 | 2.3265 | 1.7613 |
| `svd_values/n128/b128` | 288.2303 | 288.0175 | 244.2548 |
| `svd_values/n32/b1` | 0.1141 | 0.1207 | 0.0767 |
| `svd_values/n32/b128` | 14.8632 | 3.9871 | 9.9124 |
| `triangular_solve/n128/b1` | 0.0110 | 0.0136 | 0.0093 |
| `triangular_solve/n128/b128` | 2.2298 | 2.1973 | 2.4554 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0043 | 0.0015 |
| `triangular_solve/n32/b128` | 0.1920 | 0.0347 | 0.1584 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1966 | - | 0.2336 |
| `cholesky/n256/b4` | 0.7998 | - | 0.9415 |
| `cholesky/n512/b1` | 1.2857 | - | 1.5803 |
| `cholesky/n512/b4` | 5.6511 | - | 6.6550 |
| `eigh/n256/b1` | 5.6082 | - | 5.4152 |
| `eigh/n256/b4` | 22.4554 | - | 21.6456 |
| `eigh/n512/b1` | 28.9617 | - | 30.4579 |
| `eigh/n512/b4` | 116.1122 | - | 121.6984 |
| `eigvalsh/n256/b1` | 16.5068 | - | 2.4694 |
| `eigvalsh/n256/b4` | 67.1249 | - | 9.9301 |
| `eigvalsh/n512/b1` | 117.4919 | - | 14.1177 |
| `eigvalsh/n512/b4` | 470.9436 | - | 56.5953 |
| `householder_apply/n256/b1` | 2.2555 | - | 1.6397 |
| `householder_apply/n256/b4` | 9.8028 | - | 6.6083 |
| `householder_apply/n512/b1` | 18.7948 | - | 11.7929 |
| `householder_apply/n512/b4` | 82.4908 | - | 47.3751 |
| `householder_factor/n256/b1` | 1.4820 | - | 1.1016 |
| `householder_factor/n256/b4` | 5.9403 | - | 4.3845 |
| `householder_factor/n512/b1` | 12.0231 | - | 7.4242 |
| `householder_factor/n512/b4` | 48.1427 | - | 29.7458 |
| `lu/n256/b1` | 0.4774 | - | 0.4860 |
| `lu/n256/b4` | 1.9500 | - | 2.0773 |
| `lu/n512/b1` | 3.1933 | - | 3.2012 |
| `lu/n512/b4` | 12.7697 | - | 13.0916 |
| `lu_factor/n256/b1` | 0.3570 | - | 0.4469 |
| `lu_factor/n256/b4` | 1.5266 | - | 1.7956 |
| `lu_factor/n512/b1` | 2.8250 | - | 2.8905 |
| `lu_factor/n512/b4` | 11.7627 | - | 11.7988 |
| `lu_factor_solve/n256/b1` | 0.3727 | - | 0.4905 |
| `lu_factor_solve/n256/b4` | 1.4823 | - | 1.9623 |
| `lu_factor_solve/n512/b1` | 2.8859 | - | 3.0404 |
| `lu_factor_solve/n512/b4` | 11.9519 | - | 12.4022 |
| `lu_solve_prepared/n256/b1` | 0.0171 | - | 0.0428 |
| `lu_solve_prepared/n256/b4` | 0.0726 | - | 0.1754 |
| `lu_solve_prepared/n512/b1` | 0.0724 | - | 0.1599 |
| `lu_solve_prepared/n512/b4` | 0.3617 | - | 0.8695 |
| `qr/n256/b1` | 1.8447 | - | 2.1775 |
| `qr/n256/b4` | 7.3808 | - | 8.7088 |
| `qr/n512/b1` | 11.6342 | - | 14.7733 |
| `qr/n512/b4` | 46.0743 | - | 60.1100 |
| `rank_revealing_qr/n256/b1` | 2.1148 | - | 2.6108 |
| `rank_revealing_qr/n256/b4` | 8.3704 | - | 10.6119 |
| `rank_revealing_qr/n512/b1` | 15.0365 | - | 18.7511 |
| `rank_revealing_qr/n512/b4` | 59.9824 | - | 75.5694 |
| `solve/n256/b1` | 0.3858 | - | 0.4933 |
| `solve/n256/b4` | 1.5416 | - | 2.0010 |
| `solve/n512/b1` | 2.8563 | - | 3.0669 |
| `solve/n512/b4` | 11.3856 | - | 12.3846 |
| `svd_thin/n256/b1` | 12.2384 | - | 11.5399 |
| `svd_thin/n256/b4` | 48.9372 | - | 46.6271 |
| `svd_thin/n512/b1` | 70.8697 | - | 74.6372 |
| `svd_thin/n512/b4` | 282.6974 | - | 310.9085 |
| `svd_values/n256/b1` | 7.5296 | - | 5.1414 |
| `svd_values/n256/b4` | 29.9783 | - | 21.0806 |
| `svd_values/n512/b1` | 40.8047 | - | 33.2981 |
| `svd_values/n512/b4` | 167.5941 | - | 139.3820 |
| `triangular_solve/n256/b1` | 0.0106 | - | 0.0204 |
| `triangular_solve/n256/b4` | 0.0456 | - | 0.0902 |
| `triangular_solve/n512/b1` | 0.0345 | - | 0.0763 |
| `triangular_solve/n512/b4` | 0.1382 | - | 0.3585 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1989 | 0.1890 | 0.1580 |
| `cholesky/n256/b4` | 0.8100 | 0.7496 | 0.6462 |
| `cholesky/n512/b1` | 1.3321 | 0.8006 | 0.7630 |
| `cholesky/n512/b4` | 5.6676 | 3.6024 | 3.4822 |
| `eigh/n256/b1` | 5.5651 | 4.1817 | 3.5508 |
| `eigh/n256/b4` | 22.3325 | 16.9502 | 14.3868 |
| `eigh/n512/b1` | 28.8573 | 16.0253 | 16.3227 |
| `eigh/n512/b4` | 115.8457 | 64.5500 | 65.0446 |
| `eigvalsh/n256/b1` | 16.8471 | 17.9601 | 1.9042 |
| `eigvalsh/n256/b4` | 66.9998 | 68.2566 | 7.5905 |
| `eigvalsh/n512/b1` | 117.4109 | 115.9226 | 7.5431 |
| `eigvalsh/n512/b4` | 470.6561 | 461.9510 | 30.3843 |
| `householder_apply/n256/b1` | 2.3351 | 2.3865 | 1.1035 |
| `householder_apply/n256/b4` | 9.8138 | 9.8474 | 4.4228 |
| `householder_apply/n512/b1` | 19.1190 | 18.9565 | 6.7653 |
| `householder_apply/n512/b4` | 83.3420 | 82.9795 | 27.9082 |
| `householder_factor/n256/b1` | 1.4750 | 1.4890 | 0.8437 |
| `householder_factor/n256/b4` | 5.8899 | 5.9477 | 3.3839 |
| `householder_factor/n512/b1` | 12.1062 | 12.0885 | 4.5250 |
| `householder_factor/n512/b4` | 48.8838 | 48.6149 | 18.1248 |
| `lu/n256/b1` | 0.4771 | 0.4371 | 0.2851 |
| `lu/n256/b4` | 1.9516 | 1.8243 | 1.2447 |
| `lu/n512/b1` | 3.1892 | 1.9209 | 1.6749 |
| `lu/n512/b4` | 12.7799 | 7.7326 | 6.9577 |
| `lu_factor/n256/b1` | 0.3792 | 0.3321 | 0.2406 |
| `lu_factor/n256/b4` | 1.5202 | 0.7796 | 0.9667 |
| `lu_factor/n512/b1` | 2.8413 | 1.4880 | 1.3664 |
| `lu_factor/n512/b4` | 11.7510 | 6.0259 | 5.5341 |
| `lu_factor_solve/n256/b1` | 0.3968 | 0.3471 | 0.2727 |
| `lu_factor_solve/n256/b4` | 1.4896 | 0.3837 | 1.0835 |
| `lu_factor_solve/n512/b1` | 2.8979 | 1.5481 | 1.4925 |
| `lu_factor_solve/n512/b4` | 12.0860 | 6.1854 | 6.0322 |
| `lu_solve_prepared/n256/b1` | 0.0174 | 0.0236 | 0.0284 |
| `lu_solve_prepared/n256/b4` | 0.0741 | 0.0236 | 0.1241 |
| `lu_solve_prepared/n512/b1` | 0.0722 | 0.0682 | 0.1107 |
| `lu_solve_prepared/n512/b4` | 0.3797 | 0.1094 | 0.7898 |
| `qr/n256/b1` | 1.8533 | 1.7835 | 1.6955 |
| `qr/n256/b4` | 7.4269 | 7.2012 | 6.8204 |
| `qr/n512/b1` | 11.5511 | 6.0971 | 9.0767 |
| `qr/n512/b4` | 46.1353 | 23.8707 | 36.7466 |
| `rank_revealing_qr/n256/b1` | 2.1286 | 1.4903 | 2.3252 |
| `rank_revealing_qr/n256/b4` | 8.4908 | 5.9655 | 9.2367 |
| `rank_revealing_qr/n512/b1` | 15.0208 | 6.3061 | 14.5634 |
| `rank_revealing_qr/n512/b4` | 60.1008 | 25.0312 | 59.1386 |
| `solve/n256/b1` | 0.3848 | 0.3435 | 0.2897 |
| `solve/n256/b4` | 1.5332 | 1.4072 | 1.1450 |
| `solve/n512/b1` | 2.8469 | 1.5903 | 1.5371 |
| `solve/n512/b4` | 11.3593 | 6.2514 | 6.3190 |
| `svd_thin/n256/b1` | 12.1885 | 8.7502 | 9.9252 |
| `svd_thin/n256/b4` | 48.7450 | 35.9697 | 39.8784 |
| `svd_thin/n512/b1` | 70.8498 | 39.9514 | 57.0474 |
| `svd_thin/n512/b4` | 282.2620 | 159.4705 | 242.4921 |
| `svd_values/n256/b1` | 7.4938 | 7.6540 | 5.0288 |
| `svd_values/n256/b4` | 30.0084 | 31.0344 | 20.2632 |
| `svd_values/n512/b1` | 40.7525 | 34.9567 | 31.3804 |
| `svd_values/n512/b4` | 168.0943 | 140.4650 | 130.6107 |
| `triangular_solve/n256/b1` | 0.0106 | 0.0156 | 0.0126 |
| `triangular_solve/n256/b4` | 0.0451 | 0.0569 | 0.0623 |
| `triangular_solve/n512/b1` | 0.0365 | 0.0376 | 0.0544 |
| `triangular_solve/n512/b4` | 0.1765 | 0.1566 | 0.3134 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1972 | 0.1982 | 0.1579 |
| `cholesky/n256/b4` | 0.8048 | 0.8004 | 0.6421 |
| `cholesky/n512/b1` | 1.2935 | 0.6960 | 0.6919 |
| `cholesky/n512/b4` | 5.6545 | 3.2141 | 3.1004 |
| `eigh/n256/b1` | 5.5850 | 4.0704 | 3.3348 |
| `eigh/n256/b4` | 22.4345 | 16.4198 | 13.4667 |
| `eigh/n512/b1` | 28.5973 | 14.5579 | 14.2664 |
| `eigh/n512/b4` | 114.8073 | 59.7125 | 56.4719 |
| `eigvalsh/n256/b1` | 16.8513 | 17.8787 | 1.8838 |
| `eigvalsh/n256/b4` | 67.3389 | 68.2660 | 7.5052 |
| `eigvalsh/n512/b1` | 117.7142 | 115.9281 | 6.7139 |
| `eigvalsh/n512/b4` | 470.6601 | 461.4057 | 27.0891 |
| `householder_apply/n256/b1` | 2.3228 | 2.3653 | 1.0387 |
| `householder_apply/n256/b4` | 9.7342 | 9.8238 | 4.2524 |
| `householder_apply/n512/b1` | 18.8243 | 18.8033 | 5.9987 |
| `householder_apply/n512/b4` | 82.4636 | 82.3447 | 24.5534 |
| `householder_factor/n256/b1` | 1.4846 | 1.5099 | 0.8414 |
| `householder_factor/n256/b4` | 5.9216 | 5.9495 | 3.3620 |
| `householder_factor/n512/b1` | 12.0575 | 12.0153 | 4.0899 |
| `householder_factor/n512/b4` | 48.4114 | 48.2063 | 16.3328 |
| `lu/n256/b1` | 0.4793 | 0.4694 | 0.2486 |
| `lu/n256/b4` | 1.9605 | 1.9904 | 1.1003 |
| `lu/n512/b1` | 3.1835 | 2.0235 | 1.1633 |
| `lu/n512/b4` | 13.0236 | 8.1122 | 4.8788 |
| `lu_factor/n256/b1` | 0.3531 | 0.3461 | 0.2029 |
| `lu_factor/n256/b4` | 1.5267 | 1.5102 | 0.8204 |
| `lu_factor/n512/b1` | 2.8250 | 1.5496 | 0.8600 |
| `lu_factor/n512/b4` | 11.7609 | 6.2787 | 3.4455 |
| `lu_factor_solve/n256/b1` | 0.3738 | 0.3786 | 0.2348 |
| `lu_factor_solve/n256/b4` | 1.4890 | 1.4975 | 0.9541 |
| `lu_factor_solve/n512/b1` | 2.8907 | 1.6152 | 0.9691 |
| `lu_factor_solve/n512/b4` | 11.9553 | 6.5414 | 3.9305 |
| `lu_solve_prepared/n256/b1` | 0.0176 | 0.0290 | 0.0288 |
| `lu_solve_prepared/n256/b4` | 0.0805 | 0.1117 | 0.1148 |
| `lu_solve_prepared/n512/b1` | 0.0734 | 0.0804 | 0.1143 |
| `lu_solve_prepared/n512/b4` | 0.3685 | 0.3816 | 0.7514 |
| `qr/n256/b1` | 1.8465 | 2.4530 | 1.6582 |
| `qr/n256/b4` | 7.3744 | 9.7292 | 6.6740 |
| `qr/n512/b1` | 11.4778 | 6.9958 | 8.0958 |
| `qr/n512/b4` | 46.0873 | 27.8472 | 32.8703 |
| `rank_revealing_qr/n256/b1` | 2.1191 | 1.5531 | 2.2951 |
| `rank_revealing_qr/n256/b4` | 8.3609 | 6.2159 | 9.2688 |
| `rank_revealing_qr/n512/b1` | 14.7044 | 5.8706 | 13.8175 |
| `rank_revealing_qr/n512/b4` | 58.9457 | 23.2748 | 56.7123 |
| `solve/n256/b1` | 0.3854 | 0.4166 | 0.2502 |
| `solve/n256/b4` | 1.5405 | 1.5948 | 1.0190 |
| `solve/n512/b1` | 2.8584 | 1.7074 | 1.0258 |
| `solve/n512/b4` | 11.4026 | 6.4994 | 4.1962 |
| `svd_thin/n256/b1` | 12.2294 | 8.9992 | 9.7419 |
| `svd_thin/n256/b4` | 48.8299 | 35.9299 | 39.3379 |
| `svd_thin/n512/b1` | 70.8109 | 37.9592 | 54.1899 |
| `svd_thin/n512/b4` | 284.5655 | 152.8874 | 231.8672 |
| `svd_values/n256/b1` | 7.5147 | 8.0189 | 4.9861 |
| `svd_values/n256/b4` | 30.0861 | 31.9089 | 20.2363 |
| `svd_values/n512/b1` | 40.8117 | 35.5405 | 30.6007 |
| `svd_values/n512/b4` | 168.0681 | 142.1762 | 129.1408 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0190 | 0.0128 |
| `triangular_solve/n256/b4` | 0.0469 | 0.0642 | 0.0616 |
| `triangular_solve/n512/b1` | 0.0346 | 0.0428 | 0.0518 |
| `triangular_solve/n512/b4` | 0.1625 | 0.1769 | 0.2941 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7052 | - | 0.7649 |
| `cholesky/n256/b4` | 2.8114 | - | 3.0726 |
| `cholesky/n512/b1` | 4.7626 | - | 5.4127 |
| `cholesky/n512/b4` | 19.7614 | - | 22.6615 |
| `eigh/n256/b1` | 10.2518 | - | 21.5226 |
| `eigh/n256/b4` | 41.2746 | - | 86.0257 |
| `eigh/n512/b1` | 63.0587 | - | 156.9409 |
| `eigh/n512/b4` | 252.3067 | - | 630.0202 |
| `eigvalsh/n256/b1` | 19.1891 | - | 5.6450 |
| `eigvalsh/n256/b4` | 76.4734 | - | 22.6428 |
| `eigvalsh/n512/b1` | 133.1768 | - | 37.3944 |
| `eigvalsh/n512/b4` | 531.6253 | - | 149.5907 |
| `householder_apply/n256/b1` | 5.0934 | - | 4.7192 |
| `householder_apply/n256/b4` | 21.2040 | - | 19.0853 |
| `householder_apply/n512/b1` | 40.6930 | - | 32.0102 |
| `householder_apply/n512/b4` | 169.7884 | - | 128.8579 |
| `householder_factor/n256/b1` | 3.3516 | - | 3.0108 |
| `householder_factor/n256/b4` | 13.3119 | - | 12.0490 |
| `householder_factor/n512/b1` | 26.1202 | - | 20.8236 |
| `householder_factor/n512/b4` | 105.7531 | - | 83.5471 |
| `lu/n256/b1` | 1.2493 | - | 1.4302 |
| `lu/n256/b4` | 5.1260 | - | 5.9594 |
| `lu/n512/b1` | 8.6797 | - | 10.2624 |
| `lu/n512/b4` | 34.4481 | - | 41.1420 |
| `lu_factor/n256/b1` | 1.1165 | - | 1.3400 |
| `lu_factor/n256/b4` | 4.5237 | - | 5.3287 |
| `lu_factor/n512/b1` | 7.9886 | - | 9.4813 |
| `lu_factor/n512/b4` | 32.6549 | - | 38.2438 |
| `lu_factor_solve/n256/b1` | 1.1836 | - | 1.4774 |
| `lu_factor_solve/n256/b4` | 4.7711 | - | 5.7692 |
| `lu_factor_solve/n512/b1` | 8.2067 | - | 9.9846 |
| `lu_factor_solve/n512/b4` | 33.6421 | - | 39.9494 |
| `lu_solve_prepared/n256/b1` | 0.0628 | - | 0.1340 |
| `lu_solve_prepared/n256/b4` | 0.2498 | - | 0.4439 |
| `lu_solve_prepared/n512/b1` | 0.2242 | - | 0.5033 |
| `lu_solve_prepared/n512/b4` | 1.1183 | - | 1.9322 |
| `qr/n256/b1` | 6.2479 | - | 5.9953 |
| `qr/n256/b4` | 24.8063 | - | 24.1023 |
| `qr/n512/b1` | 42.2759 | - | 41.5591 |
| `qr/n512/b4` | 169.6638 | - | 168.1016 |
| `rank_revealing_qr/n256/b1` | 6.8000 | - | 6.4256 |
| `rank_revealing_qr/n256/b4` | 26.9604 | - | 25.9980 |
| `rank_revealing_qr/n512/b1` | 47.5493 | - | 44.8871 |
| `rank_revealing_qr/n512/b4` | 191.1593 | - | 179.8829 |
| `solve/n256/b1` | 1.1793 | - | 1.4821 |
| `solve/n256/b4` | 4.7032 | - | 5.9395 |
| `solve/n512/b1` | 8.2156 | - | 10.0044 |
| `solve/n512/b4` | 32.7112 | - | 40.5213 |
| `svd_thin/n256/b1` | 24.0072 | - | 23.3520 |
| `svd_thin/n256/b4` | 96.4260 | - | 92.7150 |
| `svd_thin/n512/b1` | 151.8016 | - | 146.7724 |
| `svd_thin/n512/b4` | 607.8341 | - | 604.5505 |
| `svd_values/n256/b1` | 11.8864 | - | 10.4652 |
| `svd_values/n256/b4` | 47.4568 | - | 41.8053 |
| `svd_values/n512/b1` | 68.9728 | - | 62.2680 |
| `svd_values/n512/b4` | 285.1431 | - | 259.0683 |
| `triangular_solve/n256/b1` | 0.0339 | - | 0.0660 |
| `triangular_solve/n256/b4` | 0.1458 | - | 0.2920 |
| `triangular_solve/n512/b1` | 0.1127 | - | 0.2227 |
| `triangular_solve/n512/b4` | 0.5170 | - | 0.8703 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7047 | 0.4969 | 0.3685 |
| `cholesky/n256/b4` | 2.8213 | 1.9887 | 1.4556 |
| `cholesky/n512/b1` | 4.7741 | 2.4424 | 2.1268 |
| `cholesky/n512/b4` | 19.8118 | 10.4897 | 9.3239 |
| `eigh/n256/b1` | 10.2660 | 7.9286 | 19.4778 |
| `eigh/n256/b4` | 41.4328 | 31.9725 | 78.4452 |
| `eigh/n512/b1` | 63.1640 | 29.1267 | 127.6762 |
| `eigh/n512/b4` | 252.5562 | 116.9749 | 511.7856 |
| `eigvalsh/n256/b1` | 18.7567 | 19.9658 | 4.9175 |
| `eigvalsh/n256/b4` | 76.2840 | 77.1248 | 19.6938 |
| `eigvalsh/n512/b1` | 132.9973 | 124.3392 | 20.4291 |
| `eigvalsh/n512/b4` | 532.7746 | 494.1252 | 81.7683 |
| `householder_apply/n256/b1` | 5.0918 | 5.0900 | 2.2070 |
| `householder_apply/n256/b4` | 21.4446 | 21.3364 | 8.9807 |
| `householder_apply/n512/b1` | 40.8616 | 40.7270 | 12.1954 |
| `householder_apply/n512/b4` | 170.3115 | 170.3303 | 49.3223 |
| `householder_factor/n256/b1` | 3.3263 | 3.3610 | 1.7010 |
| `householder_factor/n256/b4` | 13.3010 | 13.3241 | 6.8651 |
| `householder_factor/n512/b1` | 26.2274 | 26.1585 | 8.5989 |
| `householder_factor/n512/b4` | 105.1457 | 105.6071 | 34.2987 |
| `lu/n256/b1` | 1.2693 | 0.8261 | 0.7688 |
| `lu/n256/b4` | 5.1442 | 3.4305 | 3.2725 |
| `lu/n512/b1` | 8.6379 | 3.8556 | 3.6912 |
| `lu/n512/b4` | 34.5371 | 15.2479 | 14.9348 |
| `lu_factor/n256/b1` | 1.1047 | 0.6657 | 0.6685 |
| `lu_factor/n256/b4` | 4.3575 | 1.4941 | 2.6496 |
| `lu_factor/n512/b1` | 8.0133 | 3.1197 | 2.9911 |
| `lu_factor/n512/b4` | 32.7080 | 8.9777 | 12.0048 |
| `lu_factor_solve/n256/b1` | 1.1745 | 0.7296 | 0.7673 |
| `lu_factor_solve/n256/b4` | 4.6070 | 1.1936 | 2.9461 |
| `lu_factor_solve/n512/b1` | 8.2221 | 3.2854 | 3.3436 |
| `lu_factor_solve/n512/b4` | 33.6813 | 13.9499 | 13.3245 |
| `lu_solve_prepared/n256/b1` | 0.0630 | 0.0599 | 0.1036 |
| `lu_solve_prepared/n256/b4` | 0.2457 | 0.1281 | 0.2686 |
| `lu_solve_prepared/n512/b1` | 0.2216 | 0.1600 | 0.3361 |
| `lu_solve_prepared/n512/b4` | 1.0915 | 0.4436 | 1.5885 |
| `qr/n256/b1` | 6.2273 | 3.1100 | 3.4448 |
| `qr/n256/b4` | 24.8353 | 12.4552 | 13.9279 |
| `qr/n512/b1` | 42.3160 | 14.6018 | 17.2195 |
| `qr/n512/b4` | 169.6512 | 58.4350 | 69.9486 |
| `rank_revealing_qr/n256/b1` | 6.7542 | 3.7797 | 3.8470 |
| `rank_revealing_qr/n256/b4` | 27.1586 | 15.9440 | 15.7255 |
| `rank_revealing_qr/n512/b1` | 47.6749 | 16.7686 | 18.9848 |
| `rank_revealing_qr/n512/b4` | 191.2092 | 67.7619 | 76.6130 |
| `solve/n256/b1` | 1.1715 | 0.7435 | 0.7938 |
| `solve/n256/b4` | 4.7111 | 3.0178 | 3.2060 |
| `solve/n512/b1` | 8.2133 | 3.4060 | 3.4545 |
| `solve/n512/b4` | 32.8132 | 13.4093 | 14.0767 |
| `svd_thin/n256/b1` | 24.1612 | 14.8960 | 15.1961 |
| `svd_thin/n256/b4` | 96.8108 | 60.6836 | 60.9066 |
| `svd_thin/n512/b1` | 151.4831 | 67.3121 | 75.0968 |
| `svd_thin/n512/b4` | 607.5896 | 267.2678 | 318.9564 |
| `svd_values/n256/b1` | 11.8422 | 11.9853 | 8.0070 |
| `svd_values/n256/b4` | 47.1921 | 46.8522 | 32.0566 |
| `svd_values/n512/b1` | 68.7084 | 45.4955 | 35.3991 |
| `svd_values/n512/b4` | 284.3103 | 187.9079 | 151.0290 |
| `triangular_solve/n256/b1` | 0.0336 | 0.0339 | 0.0415 |
| `triangular_solve/n256/b4` | 0.1449 | 0.1321 | 0.2014 |
| `triangular_solve/n512/b1` | 0.1145 | 0.0848 | 0.1527 |
| `triangular_solve/n512/b4` | 0.5786 | 0.3807 | 0.8101 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7049 | 0.4947 | 0.3333 |
| `cholesky/n256/b4` | 2.7772 | 1.9793 | 1.2672 |
| `cholesky/n512/b1` | 4.7685 | 1.8807 | 1.4074 |
| `cholesky/n512/b4` | 19.7506 | 7.9350 | 6.5310 |
| `eigh/n256/b1` | 10.2322 | 6.9391 | 19.2729 |
| `eigh/n256/b4` | 41.3459 | 27.9580 | 77.2101 |
| `eigh/n512/b1` | 63.1044 | 24.0742 | 123.4757 |
| `eigh/n512/b4` | 251.7958 | 97.9845 | 492.0412 |
| `eigvalsh/n256/b1` | 19.0177 | 20.0390 | 4.8681 |
| `eigvalsh/n256/b4` | 76.6796 | 77.8301 | 19.3348 |
| `eigvalsh/n512/b1` | 132.7896 | 121.9261 | 17.9072 |
| `eigvalsh/n512/b4` | 531.5936 | 485.1137 | 72.0908 |
| `householder_apply/n256/b1` | 5.0614 | 5.1360 | 1.7681 |
| `householder_apply/n256/b4` | 21.1408 | 21.1865 | 7.2726 |
| `householder_apply/n512/b1` | 40.7289 | 41.8118 | 8.5533 |
| `householder_apply/n512/b4` | 169.9756 | 169.3224 | 35.2708 |
| `householder_factor/n256/b1` | 3.3045 | 3.3570 | 1.5308 |
| `householder_factor/n256/b4` | 13.2847 | 13.2989 | 6.1031 |
| `householder_factor/n512/b1` | 27.4871 | 26.2637 | 6.4970 |
| `householder_factor/n512/b4` | 105.9364 | 105.4341 | 26.0986 |
| `lu/n256/b1` | 1.2359 | 0.8175 | 0.5582 |
| `lu/n256/b4` | 5.0220 | 3.3557 | 2.4608 |
| `lu/n512/b1` | 8.6729 | 3.3190 | 2.3033 |
| `lu/n512/b4` | 34.5590 | 12.9832 | 9.2532 |
| `lu_factor/n256/b1` | 1.1222 | 0.6629 | 0.4554 |
| `lu_factor/n256/b4` | 4.5027 | 2.7014 | 1.7857 |
| `lu_factor/n512/b1` | 8.0073 | 2.5089 | 1.6426 |
| `lu_factor/n512/b4` | 32.6554 | 10.3760 | 6.6328 |
| `lu_factor_solve/n256/b1` | 1.1783 | 0.7391 | 0.5443 |
| `lu_factor_solve/n256/b4` | 4.7725 | 3.0065 | 2.0888 |
| `lu_factor_solve/n512/b1` | 8.2058 | 2.7065 | 2.0049 |
| `lu_factor_solve/n512/b4` | 33.5632 | 11.0110 | 8.1257 |
| `lu_solve_prepared/n256/b1` | 0.0629 | 0.0666 | 0.0943 |
| `lu_solve_prepared/n256/b4` | 0.2508 | 0.2651 | 0.2967 |
| `lu_solve_prepared/n512/b1` | 0.2274 | 0.1743 | 0.3602 |
| `lu_solve_prepared/n512/b4` | 1.1128 | 0.9128 | 1.6372 |
| `qr/n256/b1` | 6.2349 | 3.5083 | 3.0579 |
| `qr/n256/b4` | 24.7804 | 13.8939 | 12.3905 |
| `qr/n512/b1` | 42.2760 | 12.2834 | 13.1609 |
| `qr/n512/b4` | 169.3574 | 49.8329 | 53.3069 |
| `rank_revealing_qr/n256/b1` | 6.7526 | 3.9596 | 3.5125 |
| `rank_revealing_qr/n256/b4` | 26.8943 | 14.8898 | 14.3245 |
| `rank_revealing_qr/n512/b1` | 47.7732 | 11.9248 | 14.8733 |
| `rank_revealing_qr/n512/b4` | 191.7581 | 48.2488 | 59.7887 |
| `solve/n256/b1` | 1.1807 | 0.7626 | 0.5942 |
| `solve/n256/b4` | 4.6768 | 3.0050 | 2.3914 |
| `solve/n512/b1` | 8.2105 | 2.8446 | 2.1186 |
| `solve/n512/b4` | 32.8460 | 11.1674 | 8.8683 |
| `svd_thin/n256/b1` | 24.0134 | 14.5800 | 14.1722 |
| `svd_thin/n256/b4` | 96.3375 | 59.6848 | 57.3093 |
| `svd_thin/n512/b1` | 151.4148 | 54.9732 | 64.4241 |
| `svd_thin/n512/b4` | 605.9990 | 221.7066 | 271.9789 |
| `svd_values/n256/b1` | 11.8532 | 11.9608 | 7.9284 |
| `svd_values/n256/b4` | 47.2160 | 47.4803 | 31.9021 |
| `svd_values/n512/b1` | 68.4319 | 43.7880 | 31.6925 |
| `svd_values/n512/b4` | 282.2782 | 179.5639 | 135.9023 |
| `triangular_solve/n256/b1` | 0.0336 | 0.0379 | 0.0473 |
| `triangular_solve/n256/b4` | 0.1476 | 0.1441 | 0.1854 |
| `triangular_solve/n512/b1` | 0.1126 | 0.0886 | 0.1476 |
| `triangular_solve/n512/b4` | 0.5132 | 0.3944 | 0.8091 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5407 | - | 0.5540 |
| `householder_factor/4096x256/b1` | 41.6641 | - | 23.5541 |
| `qr/1024x64/b1` | 0.9832 | - | 1.0746 |
| `qr/4096x256/b1` | 41.3781 | - | 46.5685 |
| `rank_revealing_qr/1024x64/b1` | 0.9791 | - | 1.1704 |
| `rank_revealing_qr/4096x256/b1` | 64.5988 | - | 56.8883 |
| `svd_thin/1024x64/b1` | 1.4588 | - | 2.9018 |
| `svd_thin/4096x256/b1` | 72.6052 | - | 92.9886 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5389 | 0.5442 | 0.5942 |
| `householder_factor/4096x256/b1` | 41.5702 | 41.6807 | 12.4203 |
| `qr/1024x64/b1` | 0.9856 | 0.9214 | 1.1405 |
| `qr/4096x256/b1` | 41.4084 | 20.2243 | 24.4804 |
| `rank_revealing_qr/1024x64/b1` | 0.9786 | 0.7436 | 1.2537 |
| `rank_revealing_qr/4096x256/b1` | 65.8771 | 23.9540 | 28.4647 |
| `svd_thin/1024x64/b1` | 1.4591 | 1.3918 | 2.8179 |
| `svd_thin/4096x256/b1` | 72.4873 | 40.6033 | 60.1315 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5437 | 0.5520 | 0.5992 |
| `householder_factor/4096x256/b1` | 41.7569 | 41.6343 | 10.9268 |
| `qr/1024x64/b1` | 0.9865 | 1.1373 | 1.1517 |
| `qr/4096x256/b1` | 40.9735 | 19.8132 | 21.9589 |
| `rank_revealing_qr/1024x64/b1` | 0.9821 | 0.7553 | 1.2308 |
| `rank_revealing_qr/4096x256/b1` | 63.5530 | 18.6381 | 24.0056 |
| `svd_thin/1024x64/b1` | 1.4575 | 1.6330 | 2.8137 |
| `svd_thin/4096x256/b1` | 72.6865 | 32.8154 | 55.8414 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1746 | - | 1.0587 |
| `householder_factor/4096x256/b1` | 120.0828 | - | 69.0621 |
| `qr/1024x64/b1` | 2.8668 | - | 2.0801 |
| `qr/4096x256/b1` | 146.6742 | - | 137.9627 |
| `rank_revealing_qr/1024x64/b1` | 2.8645 | - | 2.2467 |
| `rank_revealing_qr/4096x256/b1` | 243.7740 | - | 171.6489 |
| `svd_thin/1024x64/b1` | 3.5292 | - | 4.8131 |
| `svd_thin/4096x256/b1` | 231.3117 | - | 250.4291 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1444 | 1.1550 | 0.4370 |
| `householder_factor/4096x256/b1` | 120.1273 | 119.7785 | 19.9004 |
| `qr/1024x64/b1` | 2.8499 | 1.6402 | 0.8118 |
| `qr/4096x256/b1` | 147.0971 | 57.4921 | 40.3350 |
| `rank_revealing_qr/1024x64/b1` | 2.8694 | 1.7650 | 1.0363 |
| `rank_revealing_qr/4096x256/b1` | 243.9502 | 81.9208 | 55.5174 |
| `svd_thin/1024x64/b1` | 3.5428 | 2.2763 | 2.9106 |
| `svd_thin/4096x256/b1` | 231.8428 | 103.2886 | 107.8874 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1442 | 1.2082 | 0.3475 |
| `householder_factor/4096x256/b1` | 120.4861 | 120.9688 | 12.4358 |
| `qr/1024x64/b1` | 2.8704 | 1.7498 | 0.6253 |
| `qr/4096x256/b1` | 147.3258 | 46.5909 | 25.6381 |
| `rank_revealing_qr/1024x64/b1` | 2.8716 | 1.7330 | 0.8587 |
| `rank_revealing_qr/4096x256/b1` | 245.4178 | 52.2487 | 34.3456 |
| `svd_thin/1024x64/b1` | 3.5306 | 2.4480 | 2.6405 |
| `svd_thin/4096x256/b1` | 231.9997 | 76.0367 | 85.8300 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
