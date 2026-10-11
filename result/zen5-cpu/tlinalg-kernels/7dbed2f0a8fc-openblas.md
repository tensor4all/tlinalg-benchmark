<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261011T051910Z-mkl-pin/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `7dbed2f0a8fce26577e358c21433eace8fd72ecb`
- features: `tlinalg-bench/link-openblas-static`
- faer provider: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
- harness commit: `b644d9588cda5b07e6609dee6cc5147080be397c`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-11T06:14:26.240862Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor openblas --checkout /tmp/tl-pin --aa 1 --label mkl-pin`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261011T051910Z-mkl-pin/`

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
| `cholesky/n16/b1024` | 0.5237 | - | 0.6043 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1066 | - | 0.1149 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2140 | - | 0.2285 |
| `eig/n16/b1` | 0.0564 | - | 0.0439 |
| `eig/n16/b1024` | 60.8470 | - | 46.3034 |
| `eig/n4/b1` | 0.0043 | - | 0.0044 |
| `eig/n4/b1024` | 3.9052 | - | 3.5092 |
| `eig/n8/b1` | 0.0152 | - | 0.0124 |
| `eig/n8/b1024` | 14.6133 | - | 11.3485 |
| `eigh/n16/b1` | 0.0177 | - | 0.0231 |
| `eigh/n16/b1024` | 18.0188 | - | 24.1991 |
| `eigh/n4/b1` | 0.0016 | - | 0.0021 |
| `eigh/n4/b1024` | 1.4721 | - | 1.8467 |
| `eigh/n8/b1` | 0.0052 | - | 0.0065 |
| `eigh/n8/b1024` | 5.0698 | - | 6.5170 |
| `eigvals/n16/b1` | 0.0403 | - | 0.0324 |
| `eigvals/n16/b1024` | 42.1451 | - | 32.7628 |
| `eigvals/n4/b1` | 0.0026 | - | 0.0033 |
| `eigvals/n4/b1024` | 2.2259 | - | 2.3160 |
| `eigvals/n8/b1` | 0.0106 | - | 0.0099 |
| `eigvals/n8/b1024` | 10.0177 | - | 8.7539 |
| `eigvalsh/n16/b1` | 0.0196 | - | 0.0086 |
| `eigvalsh/n16/b1024` | 20.4534 | - | 8.6798 |
| `eigvalsh/n4/b1` | 0.0019 | - | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5949 | - | 0.8313 |
| `eigvalsh/n8/b1` | 0.0057 | - | 0.0030 |
| `eigvalsh/n8/b1024` | 5.4042 | - | 2.7129 |
| `full_piv_lu/n16/b1` | 0.0026 | - | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.0608 | - | 2.7014 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2187 | - | 0.2192 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.5986 | - | 0.6089 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | - | 0.0039 |
| `full_piv_lu_solve/n16/b1024` | 2.0557 | - | 3.6706 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | - | 0.0006 |
| `full_piv_lu_solve/n4/b1024` | 0.3194 | - | 0.4139 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0012 |
| `full_piv_lu_solve/n8/b1024` | 0.7752 | - | 0.9964 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0030 |
| `householder_apply/n16/b1024` | 2.7917 | - | 2.7507 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0006 |
| `householder_apply/n4/b1024` | 0.1900 | - | 0.2559 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0011 |
| `householder_apply/n8/b1024` | 0.6749 | - | 0.7439 |
| `householder_factor/n16/b1` | 0.0021 | - | 0.0027 |
| `householder_factor/n16/b1024` | 2.1391 | - | 2.6119 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.2363 | - | 0.3181 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.6971 | - | 0.9033 |
| `lu/n16/b1` | 0.0020 | - | 0.0017 |
| `lu/n16/b1024` | 1.5345 | - | 1.4004 |
| `lu/n4/b1` | 0.0004 | - | 0.0004 |
| `lu/n4/b1024` | 0.1671 | - | 0.1939 |
| `lu/n8/b1` | 0.0007 | - | 0.0006 |
| `lu/n8/b1024` | 0.4662 | - | 0.4883 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0011 |
| `lu_factor/n16/b1024` | 1.0926 | - | 1.0896 |
| `lu_factor/n4/b1` | 0.0003 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1324 | - | 0.1296 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.3500 | - | 0.3392 |
| `lu_factor_solve/n16/b1` | 0.0017 | - | 0.0020 |
| `lu_factor_solve/n16/b1024` | 1.4010 | - | 1.9437 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0004 |
| `lu_factor_solve/n4/b1024` | 0.1659 | - | 0.3353 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0007 |
| `lu_factor_solve/n8/b1024` | 0.4638 | - | 0.6672 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3580 | - | 0.7131 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0404 | - | 0.1881 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0003 |
| `lu_solve_prepared/n8/b1024` | 0.1374 | - | 0.3079 |
| `qr/n16/b1` | 0.0055 | - | 0.0049 |
| `qr/n16/b1024` | 5.3916 | - | 4.7015 |
| `qr/n4/b1` | 0.0007 | - | 0.0008 |
| `qr/n4/b1024` | 0.4372 | - | 0.5713 |
| `qr/n8/b1` | 0.0016 | - | 0.0018 |
| `qr/n8/b1024` | 1.4002 | - | 1.5833 |
| `rank_revealing_qr/n16/b1` | 0.0067 | - | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.2851 | - | 5.6272 |
| `rank_revealing_qr/n4/b1` | 0.0010 | - | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7172 | - | 0.7053 |
| `rank_revealing_qr/n8/b1` | 0.0023 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.9087 | - | 1.8292 |
| `solve/n16/b1` | 0.0021 | - | 0.0024 |
| `solve/n16/b1024` | 1.5278 | - | 2.0283 |
| `solve/n4/b1` | 0.0005 | - | 0.0006 |
| `solve/n4/b1024` | 0.2157 | - | 0.3654 |
| `solve/n8/b1` | 0.0009 | - | 0.0010 |
| `solve/n8/b1024` | 0.5507 | - | 0.6790 |
| `svd_full/n16/b1` | 0.0329 | - | 0.0522 |
| `svd_full/n16/b1024` | 33.8687 | - | 53.7774 |
| `svd_full/n4/b1` | 0.0030 | - | 0.0049 |
| `svd_full/n4/b1024` | 2.5672 | - | 4.0813 |
| `svd_full/n8/b1` | 0.0091 | - | 0.0137 |
| `svd_full/n8/b1024` | 9.1386 | - | 13.6444 |
| `svd_thin/n16/b1` | 0.0331 | - | 0.0523 |
| `svd_thin/n16/b1024` | 33.9090 | - | 53.7503 |
| `svd_thin/n4/b1` | 0.0028 | - | 0.0049 |
| `svd_thin/n4/b1024` | 2.5698 | - | 4.0702 |
| `svd_thin/n8/b1` | 0.0092 | - | 0.0137 |
| `svd_thin/n8/b1024` | 9.1775 | - | 13.6235 |
| `svd_values/n16/b1` | 0.0268 | - | 0.0180 |
| `svd_values/n16/b1024` | 28.2268 | - | 18.6095 |
| `svd_values/n4/b1` | 0.0025 | - | 0.0031 |
| `svd_values/n4/b1024` | 2.2203 | - | 2.3317 |
| `svd_values/n8/b1` | 0.0078 | - | 0.0067 |
| `svd_values/n8/b1024` | 7.6541 | - | 6.1649 |
| `triangular_solve/n16/b1` | 0.0004 | - | 0.0006 |
| `triangular_solve/n16/b1024` | 0.3034 | - | 0.3963 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0517 | - | 0.1195 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1309 | - | 0.1893 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0022 | 0.0007 |
| `cholesky/n16/b1024` | 0.5249 | 0.2664 | 0.5953 |
| `cholesky/n4/b1` | 0.0002 | 0.0025 | 0.0002 |
| `cholesky/n4/b1024` | 0.1063 | 0.0339 | 0.1160 |
| `cholesky/n8/b1` | 0.0003 | 0.0026 | 0.0003 |
| `cholesky/n8/b1024` | 0.2176 | 0.0611 | 0.2338 |
| `eig/n16/b1` | 0.0565 | 0.0607 | 0.0437 |
| `eig/n16/b1024` | 60.8504 | 18.9067 | 46.2238 |
| `eig/n4/b1` | 0.0045 | 0.0071 | 0.0044 |
| `eig/n4/b1024` | 3.8886 | 2.4047 | 3.5160 |
| `eig/n8/b1` | 0.0152 | 0.0181 | 0.0124 |
| `eig/n8/b1024` | 14.6271 | 4.8219 | 11.4179 |
| `eigh/n16/b1` | 0.0177 | 0.0208 | 0.0231 |
| `eigh/n16/b1024` | 17.8150 | 4.5320 | 24.3582 |
| `eigh/n4/b1` | 0.0016 | 0.0038 | 0.0021 |
| `eigh/n4/b1024` | 1.4605 | 0.7350 | 1.8820 |
| `eigh/n8/b1` | 0.0051 | 0.0076 | 0.0067 |
| `eigh/n8/b1024` | 5.0678 | 2.5671 | 6.5568 |
| `eigvals/n16/b1` | 0.0403 | 0.0437 | 0.0326 |
| `eigvals/n16/b1024` | 42.0803 | 13.1183 | 32.8721 |
| `eigvals/n4/b1` | 0.0026 | 0.0053 | 0.0033 |
| `eigvals/n4/b1024` | 2.1941 | 1.2582 | 2.3084 |
| `eigvals/n8/b1` | 0.0106 | 0.0133 | 0.0099 |
| `eigvals/n8/b1024` | 10.0538 | 3.6696 | 8.7488 |
| `eigvalsh/n16/b1` | 0.0195 | 0.0244 | 0.0086 |
| `eigvalsh/n16/b1024` | 20.5182 | 10.9334 | 8.7405 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0036 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5771 | 1.0231 | 0.8742 |
| `eigvalsh/n8/b1` | 0.0057 | 0.0084 | 0.0030 |
| `eigvalsh/n8/b1024` | 5.3743 | 2.9441 | 2.7648 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0041 | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.0965 | 1.0393 | 2.8458 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0027 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2216 | 0.0627 | 0.2197 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0033 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.5939 | 0.3092 | 0.5880 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0050 | 0.0039 |
| `full_piv_lu_solve/n16/b1024` | 2.0542 | 0.5463 | 3.8884 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0024 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3466 | 0.1788 | 0.5479 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0029 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7686 | 0.3847 | 1.2025 |
| `householder_apply/n16/b1` | 0.0028 | 0.0044 | 0.0030 |
| `householder_apply/n16/b1024` | 2.6141 | 0.6931 | 2.6672 |
| `householder_apply/n4/b1` | 0.0004 | 0.0023 | 0.0006 |
| `householder_apply/n4/b1024` | 0.1803 | 0.0504 | 0.2467 |
| `householder_apply/n8/b1` | 0.0007 | 0.0034 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6551 | 0.1741 | 0.7214 |
| `householder_factor/n16/b1` | 0.0021 | 0.0050 | 0.0027 |
| `householder_factor/n16/b1024` | 2.0531 | 0.5494 | 2.6041 |
| `householder_factor/n4/b1` | 0.0003 | 0.0020 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2373 | 0.0695 | 0.3188 |
| `householder_factor/n8/b1` | 0.0007 | 0.0032 | 0.0010 |
| `householder_factor/n8/b1024` | 0.6732 | 0.3442 | 0.9035 |
| `lu/n16/b1` | 0.0019 | 0.0042 | 0.0017 |
| `lu/n16/b1024` | 1.5181 | 0.4050 | 1.4301 |
| `lu/n4/b1` | 0.0004 | 0.0026 | 0.0004 |
| `lu/n4/b1024` | 0.1718 | 0.0889 | 0.1939 |
| `lu/n8/b1` | 0.0007 | 0.0035 | 0.0007 |
| `lu/n8/b1024` | 0.4725 | 0.2385 | 0.4801 |
| `lu_factor/n16/b1` | 0.0013 | 0.0039 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1339 | 0.2984 | 1.0756 |
| `lu_factor/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1320 | 0.0417 | 0.1282 |
| `lu_factor/n8/b1` | 0.0006 | 0.0027 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3500 | 0.0918 | 0.3392 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0034 | 0.0019 |
| `lu_factor_solve/n16/b1024` | 1.4189 | 0.3666 | 2.2925 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0025 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.1651 | 0.0475 | 0.7822 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0036 | 0.0011 |
| `lu_factor_solve/n8/b1024` | 0.4773 | 0.1313 | 1.2193 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0028 | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.3597 | 0.1905 | 0.9083 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0005 |
| `lu_solve_prepared/n4/b1024` | 0.0403 | 0.0205 | 0.4790 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0026 | 0.0008 |
| `lu_solve_prepared/n8/b1024` | 0.1368 | 0.0763 | 0.7455 |
| `qr/n16/b1` | 0.0055 | 0.0080 | 0.0048 |
| `qr/n16/b1024` | 5.4594 | 2.6299 | 4.6979 |
| `qr/n4/b1` | 0.0008 | 0.0028 | 0.0008 |
| `qr/n4/b1024` | 0.4282 | 0.2214 | 0.5842 |
| `qr/n8/b1` | 0.0016 | 0.0039 | 0.0018 |
| `qr/n8/b1024` | 1.3634 | 0.3829 | 1.5711 |
| `rank_revealing_qr/n16/b1` | 0.0066 | 0.0093 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.1480 | 3.0538 | 5.6312 |
| `rank_revealing_qr/n4/b1` | 0.0012 | 0.0033 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7037 | 0.3553 | 0.7110 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0041 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8205 | 0.4712 | 1.8392 |
| `solve/n16/b1` | 0.0021 | 0.0037 | 0.0023 |
| `solve/n16/b1024` | 1.5501 | 0.7712 | 2.2706 |
| `solve/n4/b1` | 0.0007 | 0.0022 | 0.0008 |
| `solve/n4/b1024` | 0.2181 | 0.0626 | 0.8139 |
| `solve/n8/b1` | 0.0009 | 0.0037 | 0.0013 |
| `solve/n8/b1024` | 0.5427 | 0.1412 | 1.1766 |
| `svd_full/n16/b1` | 0.0326 | 0.0356 | 0.0521 |
| `svd_full/n16/b1024` | 33.3832 | 8.5841 | 53.4861 |
| `svd_full/n4/b1` | 0.0030 | 0.0050 | 0.0048 |
| `svd_full/n4/b1024` | 2.7394 | 0.6769 | 4.0685 |
| `svd_full/n8/b1` | 0.0091 | 0.0126 | 0.0136 |
| `svd_full/n8/b1024` | 9.0822 | 4.5770 | 13.7826 |
| `svd_thin/n16/b1` | 0.0332 | 0.0357 | 0.0528 |
| `svd_thin/n16/b1024` | 33.5536 | 8.4649 | 53.6396 |
| `svd_thin/n4/b1` | 0.0027 | 0.0045 | 0.0048 |
| `svd_thin/n4/b1024` | 2.5293 | 1.2906 | 4.1148 |
| `svd_thin/n8/b1` | 0.0090 | 0.0117 | 0.0136 |
| `svd_thin/n8/b1024` | 9.0383 | 4.5566 | 13.7701 |
| `svd_values/n16/b1` | 0.0268 | 0.0299 | 0.0181 |
| `svd_values/n16/b1024` | 28.2397 | 10.8580 | 18.7118 |
| `svd_values/n4/b1` | 0.0026 | 0.0055 | 0.0031 |
| `svd_values/n4/b1024` | 2.1783 | 1.2460 | 2.3499 |
| `svd_values/n8/b1` | 0.0077 | 0.0107 | 0.0067 |
| `svd_values/n8/b1024` | 7.6035 | 2.9739 | 6.2300 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0027 | 0.0007 |
| `triangular_solve/n16/b1024` | 0.3025 | 0.0846 | 0.6023 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0510 | 0.0293 | 0.4162 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0028 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1315 | 0.0415 | 0.4803 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0007 | 0.0042 | 0.0007 |
| `cholesky/n16/b1024` | 0.5299 | 0.0705 | 0.6253 |
| `cholesky/n4/b1` | 0.0002 | 0.0026 | 0.0002 |
| `cholesky/n4/b1024` | 0.1163 | 0.0218 | 0.1203 |
| `cholesky/n8/b1` | 0.0003 | 0.0022 | 0.0003 |
| `cholesky/n8/b1024` | 0.2323 | 0.0354 | 0.2316 |
| `eig/n16/b1` | 0.0560 | 0.0611 | 0.0441 |
| `eig/n16/b1024` | 61.0450 | 11.9323 | 46.1098 |
| `eig/n4/b1` | 0.0043 | 0.0076 | 0.0045 |
| `eig/n4/b1024` | 3.9147 | 1.2006 | 3.5043 |
| `eig/n8/b1` | 0.0153 | 0.0182 | 0.0125 |
| `eig/n8/b1024` | 14.5569 | 2.9837 | 11.4092 |
| `eigh/n16/b1` | 0.0176 | 0.0208 | 0.0232 |
| `eigh/n16/b1024` | 17.8401 | 2.2609 | 24.2139 |
| `eigh/n4/b1` | 0.0016 | 0.0046 | 0.0021 |
| `eigh/n4/b1024` | 1.4702 | 0.1919 | 1.8453 |
| `eigh/n8/b1` | 0.0052 | 0.0084 | 0.0067 |
| `eigh/n8/b1024` | 5.0640 | 1.2905 | 6.5486 |
| `eigvals/n16/b1` | 0.0402 | 0.0435 | 0.0324 |
| `eigvals/n16/b1024` | 42.0891 | 9.5456 | 32.7962 |
| `eigvals/n4/b1` | 0.0026 | 0.0060 | 0.0033 |
| `eigvals/n4/b1024` | 2.1864 | 0.7789 | 2.3036 |
| `eigvals/n8/b1` | 0.0105 | 0.0138 | 0.0099 |
| `eigvals/n8/b1024` | 10.0343 | 3.9916 | 8.7516 |
| `eigvalsh/n16/b1` | 0.0198 | 0.0229 | 0.0086 |
| `eigvalsh/n16/b1024` | 20.5702 | 9.2247 | 8.7541 |
| `eigvalsh/n4/b1` | 0.0019 | 0.0059 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.5823 | 0.7386 | 0.8396 |
| `eigvalsh/n8/b1` | 0.0059 | 0.0091 | 0.0030 |
| `eigvalsh/n8/b1024` | 5.3895 | 2.8840 | 2.7421 |
| `full_piv_lu/n16/b1` | 0.0025 | 0.0057 | 0.0025 |
| `full_piv_lu/n16/b1024` | 2.0844 | 0.2884 | 2.7992 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0040 | 0.0004 |
| `full_piv_lu/n4/b1024` | 0.2219 | 0.0605 | 0.2191 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0046 | 0.0007 |
| `full_piv_lu/n8/b1024` | 0.6149 | 0.1600 | 0.5867 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | 0.0056 | 0.0038 |
| `full_piv_lu_solve/n16/b1024` | 2.0856 | 0.5191 | 3.8358 |
| `full_piv_lu_solve/n4/b1` | 0.0007 | 0.0038 | 0.0008 |
| `full_piv_lu_solve/n4/b1024` | 0.3177 | 0.0885 | 0.5717 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0046 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7755 | 0.2029 | 1.1902 |
| `householder_apply/n16/b1` | 0.0027 | 0.0057 | 0.0029 |
| `householder_apply/n16/b1024` | 2.6561 | 0.3595 | 2.6497 |
| `householder_apply/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `householder_apply/n4/b1024` | 0.1821 | 0.0498 | 0.2471 |
| `householder_apply/n8/b1` | 0.0008 | 0.0028 | 0.0011 |
| `householder_apply/n8/b1024` | 0.6501 | 0.1735 | 0.7190 |
| `householder_factor/n16/b1` | 0.0021 | 0.0048 | 0.0027 |
| `householder_factor/n16/b1024` | 2.0967 | 0.5302 | 2.5984 |
| `householder_factor/n4/b1` | 0.0003 | 0.0021 | 0.0005 |
| `householder_factor/n4/b1024` | 0.2409 | 0.0633 | 0.3270 |
| `householder_factor/n8/b1` | 0.0007 | 0.0039 | 0.0010 |
| `householder_factor/n8/b1024` | 0.6987 | 0.1803 | 0.9029 |
| `lu/n16/b1` | 0.0020 | 0.0053 | 0.0017 |
| `lu/n16/b1024` | 1.5089 | 0.3911 | 1.4133 |
| `lu/n4/b1` | 0.0004 | 0.0041 | 0.0004 |
| `lu/n4/b1024` | 0.1688 | 0.0474 | 0.2098 |
| `lu/n8/b1` | 0.0007 | 0.0038 | 0.0006 |
| `lu/n8/b1024` | 0.4687 | 0.0650 | 0.4811 |
| `lu_factor/n16/b1` | 0.0013 | 0.0046 | 0.0011 |
| `lu_factor/n16/b1024` | 1.1191 | 0.2863 | 1.0875 |
| `lu_factor/n4/b1` | 0.0003 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1326 | 0.0387 | 0.1300 |
| `lu_factor/n8/b1` | 0.0006 | 0.0038 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3412 | 0.0955 | 0.3429 |
| `lu_factor_solve/n16/b1` | 0.0018 | 0.0049 | 0.0024 |
| `lu_factor_solve/n16/b1024` | 1.4245 | 0.3659 | 2.0668 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0036 | 0.0007 |
| `lu_factor_solve/n4/b1024` | 0.1665 | 0.0299 | 0.6857 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0041 | 0.0009 |
| `lu_factor_solve/n8/b1024` | 0.4620 | 0.1280 | 0.9199 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0023 | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.3581 | 0.1058 | 0.7025 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0025 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0404 | 0.0191 | 0.5175 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0041 | 0.0008 |
| `lu_solve_prepared/n8/b1024` | 0.1385 | 0.0368 | 0.4753 |
| `qr/n16/b1` | 0.0056 | 0.0151 | 0.0048 |
| `qr/n16/b1024` | 5.3842 | 0.7041 | 4.7115 |
| `qr/n4/b1` | 0.0006 | 0.0022 | 0.0008 |
| `qr/n4/b1024` | 0.4375 | 0.0612 | 0.5682 |
| `qr/n8/b1` | 0.0016 | 0.0043 | 0.0018 |
| `qr/n8/b1024` | 1.3970 | 0.3491 | 1.5691 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0093 | 0.0059 |
| `rank_revealing_qr/n16/b1024` | 6.1179 | 1.5477 | 5.6008 |
| `rank_revealing_qr/n4/b1` | 0.0010 | 0.0046 | 0.0011 |
| `rank_revealing_qr/n4/b1024` | 0.7129 | 0.0977 | 0.7054 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0052 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8729 | 0.4666 | 1.8349 |
| `solve/n16/b1` | 0.0021 | 0.0051 | 0.0024 |
| `solve/n16/b1024` | 1.5267 | 0.3865 | 2.0203 |
| `solve/n4/b1` | 0.0006 | 0.0040 | 0.0010 |
| `solve/n4/b1024` | 0.2171 | 0.0603 | 0.8322 |
| `solve/n8/b1` | 0.0009 | 0.0035 | 0.0011 |
| `solve/n8/b1024` | 0.5481 | 0.1423 | 1.2382 |
| `svd_full/n16/b1` | 0.0330 | 0.0363 | 0.0527 |
| `svd_full/n16/b1024` | 33.6371 | 4.4255 | 53.7982 |
| `svd_full/n4/b1` | 0.0029 | 0.0060 | 0.0048 |
| `svd_full/n4/b1024` | 2.5369 | 0.6372 | 4.0766 |
| `svd_full/n8/b1` | 0.0090 | 0.0121 | 0.0137 |
| `svd_full/n8/b1024` | 9.0507 | 2.3004 | 13.7374 |
| `svd_thin/n16/b1` | 0.0336 | 0.0363 | 0.0519 |
| `svd_thin/n16/b1024` | 33.5546 | 7.3483 | 53.2617 |
| `svd_thin/n4/b1` | 0.0027 | 0.0058 | 0.0048 |
| `svd_thin/n4/b1024` | 2.5741 | 0.6416 | 4.0666 |
| `svd_thin/n8/b1` | 0.0090 | 0.0115 | 0.0137 |
| `svd_thin/n8/b1024` | 9.0960 | 2.2953 | 13.5806 |
| `svd_values/n16/b1` | 0.0268 | 0.0301 | 0.0180 |
| `svd_values/n16/b1024` | 28.1363 | 7.2580 | 18.6378 |
| `svd_values/n4/b1` | 0.0025 | 0.0056 | 0.0031 |
| `svd_values/n4/b1024` | 2.1755 | 0.7728 | 2.3282 |
| `svd_values/n8/b1` | 0.0079 | 0.0103 | 0.0067 |
| `svd_values/n8/b1024` | 7.5884 | 2.0314 | 6.1665 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0037 | 0.0007 |
| `triangular_solve/n16/b1024` | 0.3057 | 0.0826 | 0.6806 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0033 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0514 | 0.0155 | 0.4633 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0024 | 0.0006 |
| `triangular_solve/n8/b1024` | 0.1306 | 0.0277 | 0.5252 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0010 |
| `cholesky/n16/b1024` | 0.7772 | - | 0.9490 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1182 | - | 0.1355 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2543 | - | 0.2888 |
| `eig/n16/b1` | 0.0760 | - | 0.1051 |
| `eig/n16/b1024` | 81.8152 | - | 125.7939 |
| `eig/n4/b1` | 0.0065 | - | 0.0091 |
| `eig/n4/b1024` | 6.3356 | - | 8.2377 |
| `eig/n8/b1` | 0.0209 | - | 0.0279 |
| `eig/n8/b1024` | 21.4879 | - | 29.0892 |
| `eigh/n16/b1` | 0.0181 | - | 0.0263 |
| `eigh/n16/b1024` | 19.4759 | - | 27.3312 |
| `eigh/n4/b1` | 0.0020 | - | 0.0024 |
| `eigh/n4/b1024` | 1.7359 | - | 2.1459 |
| `eigh/n8/b1` | 0.0057 | - | 0.0073 |
| `eigh/n8/b1024` | 5.4582 | - | 7.3852 |
| `eigvals/n16/b1` | 0.0474 | - | 0.0794 |
| `eigvals/n16/b1024` | 52.6301 | - | 96.0800 |
| `eigvals/n4/b1` | 0.0036 | - | 0.0073 |
| `eigvals/n4/b1024` | 3.1485 | - | 6.3684 |
| `eigvals/n8/b1` | 0.0128 | - | 0.0227 |
| `eigvals/n8/b1024` | 12.9519 | - | 23.2729 |
| `eigvalsh/n16/b1` | 0.0208 | - | 0.0118 |
| `eigvalsh/n16/b1024` | 23.6438 | - | 11.5480 |
| `eigvalsh/n4/b1` | 0.0023 | - | 0.0016 |
| `eigvalsh/n4/b1024` | 1.8910 | - | 1.2554 |
| `eigvalsh/n8/b1` | 0.0064 | - | 0.0041 |
| `eigvalsh/n8/b1024` | 5.9080 | - | 3.6657 |
| `full_piv_lu/n16/b1` | 0.0031 | - | 0.0125 |
| `full_piv_lu/n16/b1024` | 2.8246 | - | 20.1953 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2675 | - | 0.5528 |
| `full_piv_lu/n8/b1` | 0.0011 | - | 0.0023 |
| `full_piv_lu/n8/b1024` | 0.7475 | - | 2.3345 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | - | 0.0156 |
| `full_piv_lu_solve/n16/b1024` | 3.1100 | - | 22.7209 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4801 | - | 1.1492 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | - | 0.0036 |
| `full_piv_lu_solve/n8/b1024` | 1.1660 | - | 3.5869 |
| `householder_apply/n16/b1` | 0.0026 | - | 0.0045 |
| `householder_apply/n16/b1024` | 3.4949 | - | 4.4307 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0009 |
| `householder_apply/n4/b1024` | 0.1762 | - | 0.2682 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0016 |
| `householder_apply/n8/b1024` | 0.6233 | - | 0.9016 |
| `householder_factor/n16/b1` | 0.0026 | - | 0.0045 |
| `householder_factor/n16/b1024` | 2.6002 | - | 4.4227 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0007 |
| `householder_factor/n4/b1024` | 0.3055 | - | 0.5542 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0016 |
| `householder_factor/n8/b1024` | 0.8069 | - | 1.4230 |
| `lu/n16/b1` | 0.0021 | - | 0.0023 |
| `lu/n16/b1024` | 1.7839 | - | 2.4436 |
| `lu/n4/b1` | 0.0005 | - | 0.0004 |
| `lu/n4/b1024` | 0.2079 | - | 0.2261 |
| `lu/n8/b1` | 0.0008 | - | 0.0008 |
| `lu/n8/b1024` | 0.5597 | - | 0.6198 |
| `lu_factor/n16/b1` | 0.0015 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2250 | - | 1.6104 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1630 | - | 0.1599 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0005 |
| `lu_factor/n8/b1024` | 0.4107 | - | 0.4478 |
| `lu_factor_solve/n16/b1` | 0.0024 | - | 0.0027 |
| `lu_factor_solve/n16/b1024` | 2.0040 | - | 2.6656 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0005 |
| `lu_factor_solve/n4/b1024` | 0.2495 | - | 0.4056 |
| `lu_factor_solve/n8/b1` | 0.0010 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6870 | - | 0.9017 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0010 |
| `lu_solve_prepared/n16/b1024` | 0.7825 | - | 1.0231 |
| `lu_solve_prepared/n4/b1` | 0.0003 | - | 0.0003 |
| `lu_solve_prepared/n4/b1024` | 0.0972 | - | 0.2465 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0005 |
| `lu_solve_prepared/n8/b1024` | 0.2817 | - | 0.4531 |
| `qr/n16/b1` | 0.0067 | - | 0.0077 |
| `qr/n16/b1024` | 6.6530 | - | 7.6317 |
| `qr/n4/b1` | 0.0007 | - | 0.0011 |
| `qr/n4/b1024` | 0.5062 | - | 0.8683 |
| `qr/n8/b1` | 0.0018 | - | 0.0026 |
| `qr/n8/b1024` | 1.5423 | - | 2.2923 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.2373 | - | 10.1286 |
| `rank_revealing_qr/n4/b1` | 0.0012 | - | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8095 | - | 1.1513 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1514 | - | 3.0350 |
| `solve/n16/b1` | 0.0028 | - | 0.0030 |
| `solve/n16/b1024` | 2.1293 | - | 2.8366 |
| `solve/n4/b1` | 0.0007 | - | 0.0007 |
| `solve/n4/b1024` | 0.3111 | - | 0.4470 |
| `solve/n8/b1` | 0.0013 | - | 0.0012 |
| `solve/n8/b1024` | 0.7557 | - | 0.9716 |
| `svd_full/n16/b1` | 0.0349 | - | 0.0593 |
| `svd_full/n16/b1024` | 36.7054 | - | 64.5590 |
| `svd_full/n4/b1` | 0.0030 | - | 0.0060 |
| `svd_full/n4/b1024` | 3.0013 | - | 5.0562 |
| `svd_full/n8/b1` | 0.0102 | - | 0.0160 |
| `svd_full/n8/b1024` | 10.1075 | - | 16.0147 |
| `svd_thin/n16/b1` | 0.0347 | - | 0.0594 |
| `svd_thin/n16/b1024` | 36.7739 | - | 64.9705 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0062 |
| `svd_thin/n4/b1024` | 2.9943 | - | 5.0614 |
| `svd_thin/n8/b1` | 0.0096 | - | 0.0163 |
| `svd_thin/n8/b1024` | 10.0594 | - | 16.0577 |
| `svd_values/n16/b1` | 0.0300 | - | 0.0241 |
| `svd_values/n16/b1024` | 33.4888 | - | 26.0954 |
| `svd_values/n4/b1` | 0.0029 | - | 0.0040 |
| `svd_values/n4/b1024` | 2.6256 | - | 3.1138 |
| `svd_values/n8/b1` | 0.0087 | - | 0.0086 |
| `svd_values/n8/b1024` | 8.8310 | - | 7.8519 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0007 |
| `triangular_solve/n16/b1024` | 0.5867 | - | 0.5770 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0003 |
| `triangular_solve/n4/b1024` | 0.0956 | - | 0.1554 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.2355 | - | 0.2656 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0035 | 0.0010 |
| `cholesky/n16/b1024` | 0.8149 | 0.4084 | 0.9367 |
| `cholesky/n4/b1` | 0.0002 | 0.0026 | 0.0002 |
| `cholesky/n4/b1024` | 0.1190 | 0.0342 | 0.1351 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2549 | 0.1332 | 0.2914 |
| `eig/n16/b1` | 0.0758 | 0.0810 | 0.1045 |
| `eig/n16/b1024` | 81.9575 | 24.6810 | 125.2930 |
| `eig/n4/b1` | 0.0064 | 0.0095 | 0.0089 |
| `eig/n4/b1024` | 6.0668 | 2.3278 | 8.2420 |
| `eig/n8/b1` | 0.0213 | 0.0246 | 0.0278 |
| `eig/n8/b1024` | 21.5029 | 6.8330 | 29.0356 |
| `eigh/n16/b1` | 0.0181 | 0.0210 | 0.0261 |
| `eigh/n16/b1024` | 19.4025 | 5.3970 | 27.1020 |
| `eigh/n4/b1` | 0.0020 | 0.0050 | 0.0024 |
| `eigh/n4/b1024` | 1.7316 | 0.8737 | 2.1688 |
| `eigh/n8/b1` | 0.0056 | 0.0075 | 0.0074 |
| `eigh/n8/b1024` | 5.4761 | 2.1527 | 7.3895 |
| `eigvals/n16/b1` | 0.0473 | 0.0510 | 0.0790 |
| `eigvals/n16/b1024` | 52.6226 | 18.0732 | 95.5356 |
| `eigvals/n4/b1` | 0.0036 | 0.0073 | 0.0072 |
| `eigvals/n4/b1024` | 3.1397 | 1.7999 | 6.3883 |
| `eigvals/n8/b1` | 0.0128 | 0.0155 | 0.0227 |
| `eigvals/n8/b1024` | 12.8869 | 4.4088 | 23.2839 |
| `eigvalsh/n16/b1` | 0.0207 | 0.0255 | 0.0118 |
| `eigvalsh/n16/b1024` | 23.7093 | 13.9372 | 11.5607 |
| `eigvalsh/n4/b1` | 0.0023 | 0.0047 | 0.0016 |
| `eigvalsh/n4/b1024` | 1.8827 | 0.8380 | 1.2601 |
| `eigvalsh/n8/b1` | 0.0063 | 0.0097 | 0.0040 |
| `eigvalsh/n8/b1024` | 5.9109 | 3.2105 | 3.6540 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0049 | 0.0122 |
| `full_piv_lu/n16/b1024` | 2.8793 | 1.3785 | 20.2000 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0024 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2623 | 0.1362 | 0.5370 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0034 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7562 | 0.3942 | 2.2827 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0060 | 0.0157 |
| `full_piv_lu_solve/n16/b1024` | 3.0575 | 0.8022 | 22.8427 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0036 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4749 | 0.2471 | 1.2713 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0039 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1596 | 0.5844 | 3.6457 |
| `householder_apply/n16/b1` | 0.0027 | 0.0050 | 0.0047 |
| `householder_apply/n16/b1024` | 3.3061 | 0.8859 | 4.5063 |
| `householder_apply/n4/b1` | 0.0003 | 0.0027 | 0.0009 |
| `householder_apply/n4/b1024` | 0.1756 | 0.0504 | 0.2579 |
| `householder_apply/n8/b1` | 0.0007 | 0.0032 | 0.0015 |
| `householder_apply/n8/b1024` | 0.6209 | 0.1617 | 0.9154 |
| `householder_factor/n16/b1` | 0.0026 | 0.0048 | 0.0045 |
| `householder_factor/n16/b1024` | 2.5843 | 0.7651 | 4.4552 |
| `householder_factor/n4/b1` | 0.0004 | 0.0026 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3083 | 0.0828 | 0.5530 |
| `householder_factor/n8/b1` | 0.0009 | 0.0032 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8164 | 0.2112 | 1.4240 |
| `lu/n16/b1` | 0.0021 | 0.0041 | 0.0036 |
| `lu/n16/b1024` | 1.7846 | 0.4703 | 2.5387 |
| `lu/n4/b1` | 0.0005 | 0.0028 | 0.0004 |
| `lu/n4/b1024` | 0.2094 | 0.1099 | 0.2264 |
| `lu/n8/b1` | 0.0009 | 0.0033 | 0.0008 |
| `lu/n8/b1024` | 0.5436 | 0.2895 | 0.6200 |
| `lu_factor/n16/b1` | 0.0015 | 0.0032 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2387 | 0.6197 | 1.6097 |
| `lu_factor/n4/b1` | 0.0004 | 0.0026 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1624 | 0.0460 | 0.1605 |
| `lu_factor/n8/b1` | 0.0006 | 0.0023 | 0.0005 |
| `lu_factor/n8/b1024` | 0.4207 | 0.1093 | 0.4485 |
| `lu_factor_solve/n16/b1` | 0.0024 | 0.0049 | 0.0029 |
| `lu_factor_solve/n16/b1024` | 2.0051 | 0.9975 | 3.0573 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0026 | 0.0009 |
| `lu_factor_solve/n4/b1024` | 0.2674 | 0.1305 | 0.8944 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0033 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6869 | 0.3437 | 1.4069 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0035 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7702 | 0.3923 | 1.1951 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0028 | 0.0006 |
| `lu_solve_prepared/n4/b1024` | 0.0957 | 0.0340 | 0.6365 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0028 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2821 | 0.0817 | 0.7960 |
| `qr/n16/b1` | 0.0067 | 0.0091 | 0.0077 |
| `qr/n16/b1024` | 6.6617 | 3.3224 | 7.6162 |
| `qr/n4/b1` | 0.0007 | 0.0025 | 0.0012 |
| `qr/n4/b1024` | 0.5031 | 0.1336 | 0.8496 |
| `qr/n8/b1` | 0.0018 | 0.0034 | 0.0026 |
| `qr/n8/b1024` | 1.5334 | 0.7766 | 2.2798 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0104 | 0.0100 |
| `rank_revealing_qr/n16/b1024` | 7.3062 | 3.6690 | 10.1975 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0032 | 0.0017 |
| `rank_revealing_qr/n4/b1024` | 0.8132 | 0.4108 | 1.1659 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0051 | 0.0034 |
| `rank_revealing_qr/n8/b1024` | 2.1681 | 1.0825 | 3.0467 |
| `solve/n16/b1` | 0.0027 | 0.0049 | 0.0031 |
| `solve/n16/b1024` | 2.1802 | 0.5428 | 3.0526 |
| `solve/n4/b1` | 0.0007 | 0.0023 | 0.0009 |
| `solve/n4/b1024` | 0.3086 | 0.0864 | 0.6669 |
| `solve/n8/b1` | 0.0013 | 0.0036 | 0.0015 |
| `solve/n8/b1024` | 0.7724 | 0.2085 | 1.2551 |
| `svd_full/n16/b1` | 0.0347 | 0.0376 | 0.0592 |
| `svd_full/n16/b1024` | 36.5639 | 9.4638 | 64.3661 |
| `svd_full/n4/b1` | 0.0032 | 0.0052 | 0.0060 |
| `svd_full/n4/b1024` | 3.0171 | 0.7907 | 5.0585 |
| `svd_full/n8/b1` | 0.0097 | 0.0125 | 0.0161 |
| `svd_full/n8/b1024` | 10.0880 | 2.9999 | 16.0767 |
| `svd_thin/n16/b1` | 0.0347 | 0.0378 | 0.0591 |
| `svd_thin/n16/b1024` | 36.5804 | 9.3487 | 64.4802 |
| `svd_thin/n4/b1` | 0.0031 | 0.0059 | 0.0060 |
| `svd_thin/n4/b1024` | 2.9989 | 1.5262 | 5.1214 |
| `svd_thin/n8/b1` | 0.0097 | 0.0122 | 0.0161 |
| `svd_thin/n8/b1024` | 10.0468 | 2.9949 | 15.9859 |
| `svd_values/n16/b1` | 0.0302 | 0.0337 | 0.0240 |
| `svd_values/n16/b1024` | 33.2671 | 13.2254 | 25.8212 |
| `svd_values/n4/b1` | 0.0029 | 0.0054 | 0.0040 |
| `svd_values/n4/b1024` | 2.6270 | 1.3441 | 3.0949 |
| `svd_values/n8/b1` | 0.0088 | 0.0116 | 0.0085 |
| `svd_values/n8/b1024` | 8.8704 | 3.3599 | 7.8137 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0024 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5969 | 0.1555 | 0.8276 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0957 | 0.0293 | 0.4074 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0040 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2330 | 0.0673 | 0.6101 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0031 | 0.0010 |
| `cholesky/n16/b1024` | 0.7828 | 0.1143 | 0.9253 |
| `cholesky/n4/b1` | 0.0002 | 0.0034 | 0.0002 |
| `cholesky/n4/b1024` | 0.1172 | 0.0233 | 0.1404 |
| `cholesky/n8/b1` | 0.0004 | 0.0022 | 0.0004 |
| `cholesky/n8/b1024` | 0.2531 | 0.0678 | 0.2937 |
| `eig/n16/b1` | 0.0754 | 0.0811 | 0.1050 |
| `eig/n16/b1024` | 81.5088 | 14.9976 | 125.5574 |
| `eig/n4/b1` | 0.0064 | 0.0097 | 0.0091 |
| `eig/n4/b1024` | 6.1206 | 2.1864 | 8.2440 |
| `eig/n8/b1` | 0.0211 | 0.0246 | 0.0277 |
| `eig/n8/b1024` | 21.5200 | 3.9487 | 29.0039 |
| `eigh/n16/b1` | 0.0182 | 0.0212 | 0.0264 |
| `eigh/n16/b1024` | 19.6565 | 3.0698 | 27.3080 |
| `eigh/n4/b1` | 0.0019 | 0.0046 | 0.0024 |
| `eigh/n4/b1024` | 1.7382 | 0.2494 | 2.1684 |
| `eigh/n8/b1` | 0.0057 | 0.0081 | 0.0074 |
| `eigh/n8/b1024` | 5.5396 | 1.4118 | 7.4611 |
| `eigvals/n16/b1` | 0.0472 | 0.0510 | 0.0790 |
| `eigvals/n16/b1024` | 52.0094 | 12.1308 | 95.5876 |
| `eigvals/n4/b1` | 0.0035 | 0.0065 | 0.0073 |
| `eigvals/n4/b1024` | 3.1305 | 1.0761 | 6.3566 |
| `eigvals/n8/b1` | 0.0128 | 0.0160 | 0.0226 |
| `eigvals/n8/b1024` | 12.8852 | 2.9471 | 23.2574 |
| `eigvalsh/n16/b1` | 0.0208 | 0.0259 | 0.0118 |
| `eigvalsh/n16/b1024` | 23.5205 | 11.9033 | 11.6279 |
| `eigvalsh/n4/b1` | 0.0023 | 0.0054 | 0.0017 |
| `eigvalsh/n4/b1024` | 1.8867 | 0.6707 | 1.2701 |
| `eigvalsh/n8/b1` | 0.0063 | 0.0091 | 0.0040 |
| `eigvalsh/n8/b1024` | 5.9040 | 2.7251 | 3.6884 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0064 | 0.0117 |
| `full_piv_lu/n16/b1024` | 2.8401 | 0.4418 | 20.3267 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0037 | 0.0007 |
| `full_piv_lu/n4/b1024` | 0.2736 | 0.0496 | 0.5356 |
| `full_piv_lu/n8/b1` | 0.0011 | 0.0029 | 0.0022 |
| `full_piv_lu/n8/b1024` | 0.7661 | 0.1038 | 2.2798 |
| `full_piv_lu_solve/n16/b1` | 0.0036 | 0.0066 | 0.0158 |
| `full_piv_lu_solve/n16/b1024` | 3.0562 | 0.7727 | 22.7038 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0041 | 0.0014 |
| `full_piv_lu_solve/n4/b1024` | 0.4767 | 0.0677 | 1.2770 |
| `full_piv_lu_solve/n8/b1` | 0.0016 | 0.0049 | 0.0037 |
| `full_piv_lu_solve/n8/b1024` | 1.1629 | 0.2969 | 3.6527 |
| `householder_apply/n16/b1` | 0.0027 | 0.0056 | 0.0047 |
| `householder_apply/n16/b1024` | 3.2015 | 0.6367 | 4.3337 |
| `householder_apply/n4/b1` | 0.0003 | 0.0024 | 0.0008 |
| `householder_apply/n4/b1024` | 0.1874 | 0.0511 | 0.2581 |
| `householder_apply/n8/b1` | 0.0007 | 0.0031 | 0.0014 |
| `householder_apply/n8/b1024` | 0.6257 | 0.0854 | 0.8905 |
| `householder_factor/n16/b1` | 0.0027 | 0.0057 | 0.0045 |
| `householder_factor/n16/b1024` | 2.7045 | 0.6589 | 4.4503 |
| `householder_factor/n4/b1` | 0.0004 | 0.0037 | 0.0007 |
| `householder_factor/n4/b1024` | 0.3061 | 0.0470 | 0.5544 |
| `householder_factor/n8/b1` | 0.0009 | 0.0042 | 0.0016 |
| `householder_factor/n8/b1024` | 0.8151 | 0.1113 | 1.4244 |
| `lu/n16/b1` | 0.0021 | 0.0054 | 0.0023 |
| `lu/n16/b1024` | 1.8385 | 0.2894 | 2.7270 |
| `lu/n4/b1` | 0.0005 | 0.0031 | 0.0004 |
| `lu/n4/b1024` | 0.2045 | 0.0580 | 0.2334 |
| `lu/n8/b1` | 0.0008 | 0.0034 | 0.0008 |
| `lu/n8/b1024` | 0.5772 | 0.1490 | 0.6449 |
| `lu_factor/n16/b1` | 0.0014 | 0.0048 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2478 | 0.3185 | 1.6290 |
| `lu_factor/n4/b1` | 0.0004 | 0.0025 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1643 | 0.0458 | 0.1646 |
| `lu_factor/n8/b1` | 0.0006 | 0.0032 | 0.0005 |
| `lu_factor/n8/b1024` | 0.4094 | 0.1103 | 0.4505 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0055 | 0.0028 |
| `lu_factor_solve/n16/b1024` | 1.9815 | 0.5112 | 3.0491 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0038 | 0.0008 |
| `lu_factor_solve/n4/b1024` | 0.2486 | 0.0713 | 0.8406 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0035 | 0.0012 |
| `lu_factor_solve/n8/b1024` | 0.6828 | 0.1783 | 1.4113 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0041 | 0.0011 |
| `lu_solve_prepared/n16/b1024` | 0.7686 | 0.2050 | 1.1960 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0025 | 0.0005 |
| `lu_solve_prepared/n4/b1024` | 0.0976 | 0.0301 | 0.6137 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0038 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2826 | 0.0843 | 0.8229 |
| `qr/n16/b1` | 0.0068 | 0.0097 | 0.0076 |
| `qr/n16/b1024` | 6.7370 | 0.8457 | 7.5744 |
| `qr/n4/b1` | 0.0007 | 0.0043 | 0.0011 |
| `qr/n4/b1024` | 0.5069 | 0.1326 | 0.8458 |
| `qr/n8/b1` | 0.0018 | 0.0050 | 0.0026 |
| `qr/n8/b1024` | 1.5661 | 0.3958 | 2.2642 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0188 | 0.0099 |
| `rank_revealing_qr/n16/b1024` | 7.3286 | 0.9363 | 10.2132 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0035 | 0.0016 |
| `rank_revealing_qr/n4/b1024` | 0.8390 | 0.1103 | 1.1592 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0052 | 0.0033 |
| `rank_revealing_qr/n8/b1024` | 2.1550 | 0.5634 | 3.0569 |
| `solve/n16/b1` | 0.0028 | 0.0058 | 0.0032 |
| `solve/n16/b1024` | 2.1182 | 0.2858 | 2.9936 |
| `solve/n4/b1` | 0.0007 | 0.0031 | 0.0009 |
| `solve/n4/b1024` | 0.3105 | 0.0840 | 0.7044 |
| `solve/n8/b1` | 0.0013 | 0.0049 | 0.0014 |
| `solve/n8/b1024` | 0.7700 | 0.2000 | 1.2497 |
| `svd_full/n16/b1` | 0.0349 | 0.0381 | 0.0591 |
| `svd_full/n16/b1024` | 38.0223 | 5.9850 | 64.5087 |
| `svd_full/n4/b1` | 0.0031 | 0.0061 | 0.0061 |
| `svd_full/n4/b1024` | 3.0350 | 0.3811 | 5.0373 |
| `svd_full/n8/b1` | 0.0096 | 0.0126 | 0.0161 |
| `svd_full/n8/b1024` | 10.1001 | 1.3310 | 16.0109 |
| `svd_thin/n16/b1` | 0.0347 | 0.0379 | 0.0591 |
| `svd_thin/n16/b1024` | 37.3190 | 5.2651 | 64.7760 |
| `svd_thin/n4/b1` | 0.0031 | 0.0064 | 0.0061 |
| `svd_thin/n4/b1024` | 3.0200 | 0.3849 | 5.0747 |
| `svd_thin/n8/b1` | 0.0098 | 0.0125 | 0.0163 |
| `svd_thin/n8/b1024` | 10.3245 | 1.6697 | 15.9621 |
| `svd_values/n16/b1` | 0.0298 | 0.0331 | 0.0240 |
| `svd_values/n16/b1024` | 32.9911 | 9.9110 | 25.7411 |
| `svd_values/n4/b1` | 0.0029 | 0.0062 | 0.0040 |
| `svd_values/n4/b1024` | 2.6345 | 0.6624 | 3.0841 |
| `svd_values/n8/b1` | 0.0087 | 0.0113 | 0.0085 |
| `svd_values/n8/b1024` | 8.8652 | 2.9102 | 7.8093 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0036 | 0.0010 |
| `triangular_solve/n16/b1024` | 0.5820 | 0.1549 | 0.8179 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0006 |
| `triangular_solve/n4/b1024` | 0.0955 | 0.0236 | 0.4433 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0025 | 0.0007 |
| `triangular_solve/n8/b1024` | 0.2353 | 0.0642 | 0.6377 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0393 | - | 0.0400 |
| `cholesky/n128/b128` | 5.9980 | - | 6.3153 |
| `cholesky/n32/b1` | 0.0021 | - | 0.0020 |
| `cholesky/n32/b128` | 0.2580 | - | 0.2553 |
| `eigh/n128/b1` | 1.2670 | - | 1.1349 |
| `eigh/n128/b128` | 163.0245 | - | 148.1688 |
| `eigh/n32/b1` | 0.0644 | - | 0.0783 |
| `eigh/n32/b128` | 8.4905 | - | 9.9268 |
| `eigvalsh/n128/b1` | 2.4442 | - | 0.4967 |
| `eigvalsh/n128/b128` | 324.3106 | - | 64.3684 |
| `eigvalsh/n32/b1` | 0.0833 | - | 0.0287 |
| `eigvalsh/n32/b128` | 10.9067 | - | 3.7392 |
| `householder_apply/n128/b1` | 0.3006 | - | 0.2564 |
| `householder_apply/n128/b128` | 41.0412 | - | 33.8991 |
| `householder_apply/n32/b1` | 0.0106 | - | 0.0113 |
| `householder_apply/n32/b128` | 1.3558 | - | 1.3266 |
| `householder_factor/n128/b1` | 0.1961 | - | 0.2182 |
| `householder_factor/n128/b128` | 24.9190 | - | 28.1971 |
| `householder_factor/n32/b1` | 0.0071 | - | 0.0085 |
| `householder_factor/n32/b128` | 0.9005 | - | 1.0733 |
| `lu/n128/b1` | 0.0903 | - | 0.0879 |
| `lu/n128/b128` | 12.4026 | - | 13.5925 |
| `lu/n32/b1` | 0.0053 | - | 0.0050 |
| `lu/n32/b128` | 0.6036 | - | 0.6098 |
| `lu_factor/n128/b1` | 0.0572 | - | 0.0783 |
| `lu_factor/n128/b128` | 8.2838 | - | 11.2178 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0039 |
| `lu_factor/n32/b128` | 0.3848 | - | 0.4977 |
| `lu_factor_solve/n128/b1` | 0.0621 | - | 0.0905 |
| `lu_factor_solve/n128/b128` | 8.8146 | - | 12.4327 |
| `lu_factor_solve/n32/b1` | 0.0041 | - | 0.0057 |
| `lu_factor_solve/n32/b128` | 0.4922 | - | 0.7187 |
| `lu_solve_prepared/n128/b1` | 0.0060 | - | 0.0119 |
| `lu_solve_prepared/n128/b128` | 1.7942 | - | 2.7532 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0016 |
| `lu_solve_prepared/n32/b128` | 0.1143 | - | 0.2004 |
| `qr/n128/b1` | 0.3418 | - | 0.4335 |
| `qr/n128/b128` | 44.0519 | - | 56.9145 |
| `qr/n32/b1` | 0.0210 | - | 0.0159 |
| `qr/n32/b128` | 2.6304 | - | 2.0123 |
| `rank_revealing_qr/n128/b1` | 0.3472 | - | 0.4912 |
| `rank_revealing_qr/n128/b128` | 45.1299 | - | 64.7442 |
| `rank_revealing_qr/n32/b1` | 0.0207 | - | 0.0197 |
| `rank_revealing_qr/n32/b128` | 2.5954 | - | 2.4913 |
| `solve/n128/b1` | 0.0662 | - | 0.0917 |
| `solve/n128/b128` | 8.7654 | - | 12.6046 |
| `solve/n32/b1` | 0.0048 | - | 0.0061 |
| `solve/n32/b128` | 0.5194 | - | 0.7412 |
| `svd_thin/n128/b1` | 2.4059 | - | 2.1492 |
| `svd_thin/n128/b128` | 306.7535 | - | 298.9313 |
| `svd_thin/n32/b1` | 0.1178 | - | 0.1493 |
| `svd_thin/n32/b128` | 15.0506 | - | 19.0691 |
| `svd_values/n128/b1` | 1.5635 | - | 0.9655 |
| `svd_values/n128/b128` | 208.7715 | - | 130.1236 |
| `svd_values/n32/b1` | 0.1026 | - | 0.0561 |
| `svd_values/n32/b128` | 13.2467 | - | 7.2326 |
| `triangular_solve/n128/b1` | 0.0039 | - | 0.0061 |
| `triangular_solve/n128/b128` | 0.7730 | - | 1.3047 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0010 |
| `triangular_solve/n32/b128` | 0.0888 | - | 0.1077 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0374 | 0.0505 | 0.0460 |
| `cholesky/n128/b128` | 5.7242 | 6.9073 | 6.9351 |
| `cholesky/n32/b1` | 0.0021 | 0.0043 | 0.0020 |
| `cholesky/n32/b128` | 0.2557 | 0.1322 | 0.2541 |
| `eigh/n128/b1` | 1.2656 | 1.2346 | 0.9047 |
| `eigh/n128/b128` | 162.9760 | 164.2970 | 117.7870 |
| `eigh/n32/b1` | 0.0641 | 0.0692 | 0.0710 |
| `eigh/n32/b128` | 8.4291 | 2.1712 | 8.8368 |
| `eigvalsh/n128/b1` | 2.4435 | 3.2029 | 0.4722 |
| `eigvalsh/n128/b128` | 322.8229 | 324.8380 | 61.6399 |
| `eigvalsh/n32/b1` | 0.0832 | 0.0906 | 0.0291 |
| `eigvalsh/n32/b128` | 10.7969 | 6.8514 | 3.7787 |
| `householder_apply/n128/b1` | 0.3048 | 0.3095 | 0.2311 |
| `householder_apply/n128/b128` | 41.9018 | 44.2505 | 31.4535 |
| `householder_apply/n32/b1` | 0.0107 | 0.0132 | 0.0109 |
| `householder_apply/n32/b128` | 1.3469 | 0.3414 | 1.3425 |
| `householder_factor/n128/b1` | 0.1941 | 0.1996 | 0.2275 |
| `householder_factor/n128/b128` | 25.1181 | 25.2801 | 29.6073 |
| `householder_factor/n32/b1` | 0.0071 | 0.0097 | 0.0085 |
| `householder_factor/n32/b128` | 0.9134 | 0.2354 | 1.0776 |
| `lu/n128/b1` | 0.0865 | 0.1007 | 0.0878 |
| `lu/n128/b128` | 12.0014 | 13.6377 | 13.6936 |
| `lu/n32/b1` | 0.0053 | 0.0079 | 0.0050 |
| `lu/n32/b128` | 0.5893 | 0.3139 | 0.6148 |
| `lu_factor/n128/b1` | 0.0572 | 0.0711 | 0.0783 |
| `lu_factor/n128/b128` | 8.2127 | 2.5446 | 11.1514 |
| `lu_factor/n32/b1` | 0.0033 | 0.0055 | 0.0039 |
| `lu_factor/n32/b128` | 0.3900 | 0.2049 | 0.5007 |
| `lu_factor_solve/n128/b1` | 0.0631 | 0.0764 | 0.0884 |
| `lu_factor_solve/n128/b128` | 8.7956 | 2.7436 | 12.2897 |
| `lu_factor_solve/n32/b1` | 0.0044 | 0.0065 | 0.0055 |
| `lu_factor_solve/n32/b128` | 0.4922 | 0.2542 | 0.7466 |
| `lu_solve_prepared/n128/b1` | 0.0059 | 0.0098 | 0.0072 |
| `lu_solve_prepared/n128/b128` | 1.6056 | 0.4852 | 2.2386 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0034 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1146 | 0.0354 | 0.1543 |
| `qr/n128/b1` | 0.3427 | 0.6041 | 0.4481 |
| `qr/n128/b128` | 44.2684 | 81.4212 | 59.6505 |
| `qr/n32/b1` | 0.0209 | 0.0500 | 0.0160 |
| `qr/n32/b128` | 2.6083 | 0.6596 | 2.0147 |
| `rank_revealing_qr/n128/b1` | 0.3496 | 0.3723 | 0.5161 |
| `rank_revealing_qr/n128/b128` | 45.6736 | 47.8036 | 68.2787 |
| `rank_revealing_qr/n32/b1` | 0.0208 | 0.0448 | 0.0196 |
| `rank_revealing_qr/n32/b128` | 2.5788 | 0.6559 | 2.4800 |
| `solve/n128/b1` | 0.0657 | 0.0818 | 0.0929 |
| `solve/n128/b128` | 8.6849 | 10.6473 | 12.3671 |
| `solve/n32/b1` | 0.0048 | 0.0083 | 0.0059 |
| `solve/n32/b128` | 0.5280 | 0.2704 | 0.7300 |
| `svd_thin/n128/b1` | 2.4199 | 1.8067 | 2.1581 |
| `svd_thin/n128/b128` | 307.8029 | 230.2415 | 296.1431 |
| `svd_thin/n32/b1` | 0.1166 | 0.1215 | 0.1497 |
| `svd_thin/n32/b128` | 16.5311 | 3.7931 | 19.0162 |
| `svd_values/n128/b1` | 1.5535 | 1.7492 | 0.9674 |
| `svd_values/n128/b128` | 206.9201 | 209.2611 | 134.4211 |
| `svd_values/n32/b1` | 0.1029 | 0.1089 | 0.0566 |
| `svd_values/n32/b128` | 13.1300 | 5.0268 | 7.2509 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0060 | 0.0040 |
| `triangular_solve/n128/b128` | 0.8887 | 0.9778 | 1.2411 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0034 | 0.0009 |
| `triangular_solve/n32/b128` | 0.0918 | 0.0459 | 0.0995 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0390 | 0.0531 | 0.0425 |
| `cholesky/n128/b128` | 5.9178 | 7.2458 | 6.5317 |
| `cholesky/n32/b1` | 0.0021 | 0.0054 | 0.0020 |
| `cholesky/n32/b128` | 0.2469 | 0.0676 | 0.2549 |
| `eigh/n128/b1` | 1.2610 | 1.2502 | 0.8769 |
| `eigh/n128/b128` | 163.4980 | 160.7930 | 113.0006 |
| `eigh/n32/b1` | 0.0640 | 0.0684 | 0.0692 |
| `eigh/n32/b128` | 8.4210 | 1.5066 | 8.8926 |
| `eigvalsh/n128/b1` | 2.4517 | 3.1831 | 0.4770 |
| `eigvalsh/n128/b128` | 323.5269 | 324.1241 | 61.4402 |
| `eigvalsh/n32/b1` | 0.0828 | 0.0886 | 0.0291 |
| `eigvalsh/n32/b128` | 10.8045 | 5.9828 | 3.7596 |
| `householder_apply/n128/b1` | 0.3097 | 0.3163 | 0.2335 |
| `householder_apply/n128/b128` | 42.7598 | 43.3557 | 31.5812 |
| `householder_apply/n32/b1` | 0.0104 | 0.0137 | 0.0108 |
| `householder_apply/n32/b128` | 1.3346 | 0.3421 | 1.3249 |
| `householder_factor/n128/b1` | 0.1978 | 0.2034 | 0.2315 |
| `householder_factor/n128/b128` | 25.2900 | 25.9624 | 30.1432 |
| `householder_factor/n32/b1` | 0.0071 | 0.0177 | 0.0085 |
| `householder_factor/n32/b128` | 0.9040 | 0.2340 | 1.0748 |
| `lu/n128/b1` | 0.0858 | 0.1173 | 0.0877 |
| `lu/n128/b128` | 12.2246 | 15.4136 | 13.6546 |
| `lu/n32/b1` | 0.0050 | 0.0083 | 0.0050 |
| `lu/n32/b128` | 0.6153 | 0.1587 | 0.6180 |
| `lu_factor/n128/b1` | 0.0555 | 0.0814 | 0.0778 |
| `lu_factor/n128/b128` | 8.2057 | 1.5526 | 11.1671 |
| `lu_factor/n32/b1` | 0.0032 | 0.0061 | 0.0039 |
| `lu_factor/n32/b128` | 0.3878 | 0.1073 | 0.5066 |
| `lu_factor_solve/n128/b1` | 0.0627 | 1.6863 | 0.0883 |
| `lu_factor_solve/n128/b128` | 8.9491 | 1.5405 | 12.2018 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0070 | 0.0056 |
| `lu_factor_solve/n32/b128` | 0.4883 | 0.1316 | 0.7339 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0094 | 0.0074 |
| `lu_solve_prepared/n128/b128` | 2.0007 | 0.4926 | 2.0492 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0036 | 0.0012 |
| `lu_solve_prepared/n32/b128` | 0.1133 | 0.0346 | 0.1684 |
| `qr/n128/b1` | 0.3428 | 0.9474 | 0.4622 |
| `qr/n128/b128` | 44.3049 | 121.7280 | 60.5704 |
| `qr/n32/b1` | 0.0210 | 0.0637 | 0.0159 |
| `qr/n32/b128` | 2.6132 | 0.6575 | 1.9993 |
| `rank_revealing_qr/n128/b1` | 0.3483 | 0.4343 | 0.5176 |
| `rank_revealing_qr/n128/b128` | 44.9449 | 56.6451 | 67.2054 |
| `rank_revealing_qr/n32/b1` | 0.0203 | 0.0649 | 0.0196 |
| `rank_revealing_qr/n32/b128` | 2.5976 | 0.3284 | 2.4545 |
| `solve/n128/b1` | 0.0664 | 0.0927 | 0.0924 |
| `solve/n128/b128` | 8.8285 | 11.8400 | 12.3855 |
| `solve/n32/b1` | 0.0048 | 0.0077 | 0.0059 |
| `solve/n32/b128` | 0.5238 | 0.0745 | 0.7793 |
| `svd_thin/n128/b1` | 2.4162 | 1.8752 | 2.1281 |
| `svd_thin/n128/b128` | 307.7921 | 237.2103 | 293.3016 |
| `svd_thin/n32/b1` | 0.1166 | 0.1214 | 0.1497 |
| `svd_thin/n32/b128` | 15.1326 | 1.9472 | 18.9595 |
| `svd_values/n128/b1` | 1.5512 | 1.7058 | 0.9756 |
| `svd_values/n128/b128` | 207.2766 | 208.2330 | 135.2254 |
| `svd_values/n32/b1` | 0.1022 | 0.1088 | 0.0557 |
| `svd_values/n32/b128` | 13.1241 | 3.9896 | 7.2527 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0065 | 0.0039 |
| `triangular_solve/n128/b128` | 0.7556 | 0.8426 | 1.1450 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0038 | 0.0008 |
| `triangular_solve/n32/b128` | 0.0893 | 0.0224 | 0.1067 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1089 | - | 0.1085 |
| `cholesky/n128/b128` | 15.9657 | - | 15.4869 |
| `cholesky/n32/b1` | 0.0034 | - | 0.0034 |
| `cholesky/n32/b128` | 0.4333 | - | 0.4320 |
| `eigh/n128/b1` | 1.8502 | - | 3.2665 |
| `eigh/n128/b128` | 242.5335 | - | 422.1758 |
| `eigh/n32/b1` | 0.0806 | - | 0.1083 |
| `eigh/n32/b128` | 10.5517 | - | 14.0455 |
| `eigvalsh/n128/b1` | 2.7206 | - | 0.9480 |
| `eigvalsh/n128/b128` | 371.6058 | - | 123.8108 |
| `eigvalsh/n32/b1` | 0.0899 | - | 0.0419 |
| `eigvalsh/n32/b128` | 11.6880 | - | 5.4308 |
| `householder_apply/n128/b1` | 0.6858 | - | 0.6907 |
| `householder_apply/n128/b128` | 93.0447 | - | 91.5514 |
| `householder_apply/n32/b1` | 0.0143 | - | 0.0195 |
| `householder_apply/n32/b128` | 1.8472 | - | 2.4847 |
| `householder_factor/n128/b1` | 0.4585 | - | 0.4347 |
| `householder_factor/n128/b128` | 59.1475 | - | 57.3638 |
| `householder_factor/n32/b1` | 0.0113 | - | 0.0158 |
| `householder_factor/n32/b128` | 1.4418 | - | 2.0072 |
| `lu/n128/b1` | 0.1956 | - | 0.2126 |
| `lu/n128/b128` | 29.2957 | - | 31.4003 |
| `lu/n32/b1` | 0.0076 | - | 0.0080 |
| `lu/n32/b128` | 0.9951 | - | 1.1334 |
| `lu_factor/n128/b1` | 0.1559 | - | 0.1927 |
| `lu_factor/n128/b128` | 21.8117 | - | 25.5015 |
| `lu_factor/n32/b1` | 0.0054 | - | 0.0064 |
| `lu_factor/n32/b128` | 0.6498 | - | 0.8168 |
| `lu_factor_solve/n128/b1` | 0.1749 | - | 0.2218 |
| `lu_factor_solve/n128/b128` | 24.3355 | - | 29.2002 |
| `lu_factor_solve/n32/b1` | 0.0076 | - | 0.0088 |
| `lu_factor_solve/n32/b128` | 0.9299 | - | 1.1229 |
| `lu_solve_prepared/n128/b1` | 0.0187 | - | 0.0295 |
| `lu_solve_prepared/n128/b128` | 4.0386 | - | 5.1699 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0024 |
| `lu_solve_prepared/n32/b128` | 0.2833 | - | 0.3083 |
| `qr/n128/b1` | 0.9657 | - | 0.8649 |
| `qr/n128/b128` | 124.6977 | - | 113.0080 |
| `qr/n32/b1` | 0.0424 | - | 0.0285 |
| `qr/n32/b128` | 5.4184 | - | 3.6782 |
| `rank_revealing_qr/n128/b1` | 1.0101 | - | 0.9867 |
| `rank_revealing_qr/n128/b128` | 130.3093 | - | 131.5104 |
| `rank_revealing_qr/n32/b1` | 0.0387 | - | 0.0366 |
| `rank_revealing_qr/n32/b128` | 4.9328 | - | 4.8733 |
| `solve/n128/b1` | 0.1799 | - | 0.2293 |
| `solve/n128/b128` | 23.8083 | - | 29.9799 |
| `solve/n32/b1` | 0.0083 | - | 0.0094 |
| `solve/n32/b128` | 0.9580 | - | 1.1726 |
| `svd_thin/n128/b1` | 3.9800 | - | 3.7316 |
| `svd_thin/n128/b128` | 513.1515 | - | 516.3162 |
| `svd_thin/n32/b1` | 0.1507 | - | 0.1814 |
| `svd_thin/n32/b128` | 19.6421 | - | 23.8813 |
| `svd_values/n128/b1` | 2.1374 | - | 1.5901 |
| `svd_values/n128/b128` | 297.0680 | - | 224.4659 |
| `svd_values/n32/b1` | 0.1143 | - | 0.0774 |
| `svd_values/n32/b128` | 14.9776 | - | 9.9134 |
| `triangular_solve/n128/b1` | 0.0109 | - | 0.0134 |
| `triangular_solve/n128/b128` | 2.1813 | - | 2.9604 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0013 |
| `triangular_solve/n32/b128` | 0.1928 | - | 0.1592 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1092 | 0.1098 | 0.0797 |
| `cholesky/n128/b128` | 16.0299 | 15.9801 | 11.3002 |
| `cholesky/n32/b1` | 0.0033 | 0.0049 | 0.0034 |
| `cholesky/n32/b128` | 0.4144 | 0.1067 | 0.4326 |
| `eigh/n128/b1` | 1.8638 | 1.6056 | 3.1715 |
| `eigh/n128/b128` | 241.8697 | 228.8216 | 410.2984 |
| `eigh/n32/b1` | 0.0811 | 0.0856 | 0.1085 |
| `eigh/n32/b128` | 10.5598 | 2.6568 | 14.0571 |
| `eigvalsh/n128/b1` | 2.7199 | 3.9722 | 0.8940 |
| `eigvalsh/n128/b128` | 371.3394 | 372.6839 | 115.8052 |
| `eigvalsh/n32/b1` | 0.0898 | 0.0953 | 0.0422 |
| `eigvalsh/n32/b128` | 11.6501 | 7.0071 | 5.4534 |
| `householder_apply/n128/b1` | 0.6952 | 0.7013 | 0.3667 |
| `householder_apply/n128/b128` | 92.8995 | 93.3612 | 50.7649 |
| `householder_apply/n32/b1` | 0.0145 | 0.0175 | 0.0196 |
| `householder_apply/n32/b128` | 1.8182 | 0.4600 | 2.4813 |
| `householder_factor/n128/b1` | 0.4587 | 0.4612 | 0.3861 |
| `householder_factor/n128/b128` | 59.2695 | 59.2318 | 50.0658 |
| `householder_factor/n32/b1` | 0.0113 | 0.0135 | 0.0159 |
| `householder_factor/n32/b128` | 1.4322 | 0.7238 | 2.0019 |
| `lu/n128/b1` | 0.1957 | 0.1951 | 0.1445 |
| `lu/n128/b128` | 27.5979 | 26.7628 | 22.1170 |
| `lu/n32/b1` | 0.0076 | 0.0103 | 0.0080 |
| `lu/n32/b128` | 0.9850 | 0.4815 | 1.1230 |
| `lu_factor/n128/b1` | 0.1566 | 0.1471 | 0.1190 |
| `lu_factor/n128/b128` | 21.8549 | 6.2566 | 15.5178 |
| `lu_factor/n32/b1` | 0.0054 | 0.0089 | 0.0064 |
| `lu_factor/n32/b128` | 0.6378 | 0.1673 | 0.8178 |
| `lu_factor_solve/n128/b1` | 0.1750 | 0.1647 | 0.1376 |
| `lu_factor_solve/n128/b128` | 24.3306 | 6.5771 | 18.0452 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0099 | 0.0085 |
| `lu_factor_solve/n32/b128` | 0.9137 | 0.2360 | 1.1331 |
| `lu_solve_prepared/n128/b1` | 0.0188 | 0.0218 | 0.0177 |
| `lu_solve_prepared/n128/b128` | 4.2206 | 1.3012 | 4.0737 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0044 | 0.0019 |
| `lu_solve_prepared/n32/b128` | 0.2819 | 0.0744 | 0.2328 |
| `qr/n128/b1` | 0.9738 | 0.8725 | 0.7699 |
| `qr/n128/b128` | 125.3442 | 112.7907 | 101.2098 |
| `qr/n32/b1` | 0.0423 | 0.0671 | 0.0286 |
| `qr/n32/b128` | 5.4501 | 1.3711 | 3.6341 |
| `rank_revealing_qr/n128/b1` | 1.0130 | 0.8080 | 0.9008 |
| `rank_revealing_qr/n128/b128` | 130.2365 | 103.8917 | 120.2713 |
| `rank_revealing_qr/n32/b1` | 0.0387 | 0.0628 | 0.0365 |
| `rank_revealing_qr/n32/b128` | 4.8891 | 1.9230 | 4.8235 |
| `solve/n128/b1` | 0.1800 | 0.1688 | 0.1494 |
| `solve/n128/b128` | 23.7660 | 22.0765 | 19.1758 |
| `solve/n32/b1` | 0.0082 | 0.0110 | 0.0094 |
| `solve/n32/b128` | 0.9534 | 0.2490 | 1.1704 |
| `svd_thin/n128/b1` | 3.9794 | 2.7594 | 3.2132 |
| `svd_thin/n128/b128` | 513.2534 | 359.2430 | 449.5196 |
| `svd_thin/n32/b1` | 0.1522 | 0.1545 | 0.1804 |
| `svd_thin/n32/b128` | 19.7168 | 6.7400 | 24.0295 |
| `svd_values/n128/b1` | 2.1288 | 2.2404 | 1.7038 |
| `svd_values/n128/b128` | 296.6547 | 296.8570 | 239.2665 |
| `svd_values/n32/b1` | 0.1137 | 0.1219 | 0.0770 |
| `svd_values/n32/b128` | 15.0122 | 5.7995 | 9.9190 |
| `triangular_solve/n128/b1` | 0.0108 | 0.0135 | 0.0076 |
| `triangular_solve/n128/b128` | 2.1757 | 2.2119 | 2.5249 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0038 | 0.0013 |
| `triangular_solve/n32/b128` | 0.1887 | 0.0962 | 0.1523 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1074 | 0.1145 | 0.0941 |
| `cholesky/n128/b128` | 16.0351 | 16.7369 | 13.8037 |
| `cholesky/n32/b1` | 0.0034 | 0.0062 | 0.0034 |
| `cholesky/n32/b128` | 0.4287 | 0.0585 | 0.4339 |
| `eigh/n128/b1` | 1.8486 | 1.6362 | 3.1658 |
| `eigh/n128/b128` | 243.0595 | 212.3601 | 413.5091 |
| `eigh/n32/b1` | 0.0803 | 0.0855 | 0.1081 |
| `eigh/n32/b128` | 10.5253 | 1.3815 | 13.9493 |
| `eigvalsh/n128/b1` | 2.7241 | 3.7558 | 0.8926 |
| `eigvalsh/n128/b128` | 371.3940 | 372.1315 | 115.9798 |
| `eigvalsh/n32/b1` | 0.0894 | 0.0952 | 0.0422 |
| `eigvalsh/n32/b128` | 11.6537 | 6.1765 | 5.4921 |
| `householder_apply/n128/b1` | 0.7035 | 0.7127 | 0.3247 |
| `householder_apply/n128/b128` | 93.2276 | 93.6053 | 44.2459 |
| `householder_apply/n32/b1` | 0.0145 | 0.0177 | 0.0196 |
| `householder_apply/n32/b128` | 1.8483 | 0.4618 | 2.4853 |
| `householder_factor/n128/b1` | 0.4596 | 0.4615 | 0.3850 |
| `householder_factor/n128/b128` | 59.5899 | 59.1305 | 49.5274 |
| `householder_factor/n32/b1` | 0.0113 | 0.0140 | 0.0159 |
| `householder_factor/n32/b128` | 1.4327 | 0.1853 | 2.0263 |
| `lu/n128/b1` | 0.1980 | 0.1955 | 0.1402 |
| `lu/n128/b128` | 27.5840 | 27.6319 | 21.4528 |
| `lu/n32/b1` | 0.0077 | 0.0107 | 0.0081 |
| `lu/n32/b128` | 0.9948 | 0.2308 | 1.1257 |
| `lu_factor/n128/b1` | 0.1565 | 0.1560 | 0.1141 |
| `lu_factor/n128/b128` | 21.8168 | 3.3158 | 14.7934 |
| `lu_factor/n32/b1` | 0.0053 | 0.0085 | 0.0064 |
| `lu_factor/n32/b128` | 0.6543 | 0.1725 | 0.8232 |
| `lu_factor_solve/n128/b1` | 0.1752 | 0.1737 | 0.1505 |
| `lu_factor_solve/n128/b128` | 24.3478 | 5.3437 | 17.5593 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0106 | 0.0086 |
| `lu_factor_solve/n32/b128` | 0.9308 | 0.1263 | 1.1454 |
| `lu_solve_prepared/n128/b1` | 0.0188 | 0.0219 | 0.0181 |
| `lu_solve_prepared/n128/b128` | 4.1266 | 1.1185 | 4.0305 |
| `lu_solve_prepared/n32/b1` | 0.0023 | 0.0053 | 0.0017 |
| `lu_solve_prepared/n32/b128` | 0.2792 | 0.0761 | 0.2592 |
| `qr/n128/b1` | 0.9674 | 1.1988 | 0.7607 |
| `qr/n128/b128` | 124.7715 | 155.2680 | 100.2592 |
| `qr/n32/b1` | 0.0424 | 0.0887 | 0.0285 |
| `qr/n32/b128` | 5.4143 | 1.3550 | 3.6507 |
| `rank_revealing_qr/n128/b1` | 1.0113 | 0.8687 | 0.9002 |
| `rank_revealing_qr/n128/b128` | 130.5747 | 113.5403 | 121.1427 |
| `rank_revealing_qr/n32/b1` | 0.0389 | 0.0861 | 0.0365 |
| `rank_revealing_qr/n32/b128` | 4.9331 | 0.6640 | 4.8863 |
| `solve/n128/b1` | 0.1791 | 0.1802 | 0.1435 |
| `solve/n128/b128` | 23.7897 | 23.5329 | 19.0876 |
| `solve/n32/b1` | 0.0084 | 0.0110 | 0.0094 |
| `solve/n32/b128` | 0.9694 | 0.2464 | 1.2086 |
| `svd_thin/n128/b1` | 3.9800 | 2.8307 | 3.2027 |
| `svd_thin/n128/b128` | 513.4195 | 363.1364 | 447.8796 |
| `svd_thin/n32/b1` | 0.1501 | 0.1541 | 0.1815 |
| `svd_thin/n32/b128` | 19.6002 | 2.5418 | 23.8862 |
| `svd_values/n128/b1` | 2.1425 | 2.4063 | 1.7591 |
| `svd_values/n128/b128` | 295.9654 | 296.7992 | 245.8359 |
| `svd_values/n32/b1` | 0.1140 | 0.1228 | 0.0774 |
| `svd_values/n32/b128` | 15.0027 | 3.9899 | 9.9396 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0133 | 0.0089 |
| `triangular_solve/n128/b128` | 2.1738 | 2.2014 | 2.4703 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0046 | 0.0013 |
| `triangular_solve/n32/b128` | 0.1916 | 0.0312 | 0.1746 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1963 | - | 0.2312 |
| `cholesky/n256/b4` | 0.7976 | - | 0.9289 |
| `cholesky/n512/b1` | 1.2692 | - | 1.5852 |
| `cholesky/n512/b4` | 5.5565 | - | 6.6102 |
| `eigh/n256/b1` | 5.6078 | - | 5.4272 |
| `eigh/n256/b4` | 22.5146 | - | 21.6214 |
| `eigh/n512/b1` | 28.5604 | - | 30.1819 |
| `eigh/n512/b4` | 114.8038 | - | 121.0377 |
| `eigvalsh/n256/b1` | 16.7424 | - | 2.4831 |
| `eigvalsh/n256/b4` | 67.4537 | - | 9.8649 |
| `eigvalsh/n512/b1` | 118.1192 | - | 14.2893 |
| `eigvalsh/n512/b4` | 470.9662 | - | 57.2139 |
| `householder_apply/n256/b1` | 2.2905 | - | 1.6407 |
| `householder_apply/n256/b4` | 9.7749 | - | 6.6539 |
| `householder_apply/n512/b1` | 18.8381 | - | 11.7094 |
| `householder_apply/n512/b4` | 82.3650 | - | 47.3047 |
| `householder_factor/n256/b1` | 1.4826 | - | 1.0931 |
| `householder_factor/n256/b4` | 5.9249 | - | 4.3979 |
| `householder_factor/n512/b1` | 12.1109 | - | 7.4449 |
| `householder_factor/n512/b4` | 48.5299 | - | 29.8862 |
| `lu/n256/b1` | 0.4641 | - | 0.4842 |
| `lu/n256/b4` | 1.9216 | - | 2.0788 |
| `lu/n512/b1` | 3.1793 | - | 3.2087 |
| `lu/n512/b4` | 12.7447 | - | 13.1244 |
| `lu_factor/n256/b1` | 0.3536 | - | 0.4440 |
| `lu_factor/n256/b4` | 1.5196 | - | 1.7824 |
| `lu_factor/n512/b1` | 2.8161 | - | 2.8863 |
| `lu_factor/n512/b4` | 11.7390 | - | 11.7654 |
| `lu_factor_solve/n256/b1` | 0.3725 | - | 0.4878 |
| `lu_factor_solve/n256/b4` | 1.4805 | - | 1.9530 |
| `lu_factor_solve/n512/b1` | 2.8834 | - | 3.0404 |
| `lu_factor_solve/n512/b4` | 11.9762 | - | 12.3796 |
| `lu_solve_prepared/n256/b1` | 0.0174 | - | 0.0410 |
| `lu_solve_prepared/n256/b4` | 0.0781 | - | 0.1848 |
| `lu_solve_prepared/n512/b1` | 0.0622 | - | 0.1426 |
| `lu_solve_prepared/n512/b4` | 0.4398 | - | 1.0083 |
| `qr/n256/b1` | 1.8476 | - | 2.1699 |
| `qr/n256/b4` | 7.3851 | - | 8.7571 |
| `qr/n512/b1` | 11.4935 | - | 14.8162 |
| `qr/n512/b4` | 46.0802 | - | 60.2527 |
| `rank_revealing_qr/n256/b1` | 2.1248 | - | 2.6223 |
| `rank_revealing_qr/n256/b4` | 8.3552 | - | 10.6335 |
| `rank_revealing_qr/n512/b1` | 14.7394 | - | 18.7081 |
| `rank_revealing_qr/n512/b4` | 59.0565 | - | 76.2855 |
| `solve/n256/b1` | 0.3874 | - | 0.4947 |
| `solve/n256/b4` | 1.5435 | - | 2.0073 |
| `solve/n512/b1` | 2.8564 | - | 3.0610 |
| `solve/n512/b4` | 11.3775 | - | 12.4366 |
| `svd_thin/n256/b1` | 12.2364 | - | 11.5556 |
| `svd_thin/n256/b4` | 49.0065 | - | 46.7487 |
| `svd_thin/n512/b1` | 70.8667 | - | 74.1638 |
| `svd_thin/n512/b4` | 283.3917 | - | 310.9588 |
| `svd_values/n256/b1` | 7.5235 | - | 5.1836 |
| `svd_values/n256/b4` | 30.1398 | - | 21.2290 |
| `svd_values/n512/b1` | 41.1074 | - | 33.6328 |
| `svd_values/n512/b4` | 168.8260 | - | 140.8842 |
| `triangular_solve/n256/b1` | 0.0105 | - | 0.0205 |
| `triangular_solve/n256/b4` | 0.0462 | - | 0.0844 |
| `triangular_solve/n512/b1` | 0.0343 | - | 0.0757 |
| `triangular_solve/n512/b4` | 0.1369 | - | 0.3276 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1972 | 0.1810 | 0.1571 |
| `cholesky/n256/b4` | 0.7979 | 0.7655 | 0.6346 |
| `cholesky/n512/b1` | 1.2648 | 0.8053 | 0.7623 |
| `cholesky/n512/b4` | 5.6497 | 3.5905 | 3.4087 |
| `eigh/n256/b1` | 5.6722 | 4.2257 | 3.6014 |
| `eigh/n256/b4` | 22.5450 | 16.9017 | 14.3934 |
| `eigh/n512/b1` | 28.5925 | 15.7745 | 16.3750 |
| `eigh/n512/b4` | 115.4632 | 64.6014 | 65.4169 |
| `eigvalsh/n256/b1` | 16.9405 | 18.0767 | 1.9090 |
| `eigvalsh/n256/b4` | 67.2456 | 68.9563 | 7.6590 |
| `eigvalsh/n512/b1` | 116.7113 | 115.9627 | 7.4839 |
| `eigvalsh/n512/b4` | 470.3454 | 462.1069 | 30.2406 |
| `householder_apply/n256/b1` | 2.3418 | 2.3977 | 1.0919 |
| `householder_apply/n256/b4` | 9.7546 | 9.8610 | 4.5180 |
| `householder_apply/n512/b1` | 18.9567 | 18.8830 | 6.8710 |
| `householder_apply/n512/b4` | 83.5238 | 83.2821 | 27.9325 |
| `householder_factor/n256/b1` | 1.4792 | 1.5053 | 0.8504 |
| `householder_factor/n256/b4` | 5.9426 | 5.9787 | 3.4281 |
| `householder_factor/n512/b1` | 12.2310 | 12.0733 | 4.5069 |
| `householder_factor/n512/b4` | 48.9250 | 48.3815 | 18.3454 |
| `lu/n256/b1` | 0.4780 | 0.4529 | 0.2857 |
| `lu/n256/b4` | 1.9077 | 1.7762 | 1.2528 |
| `lu/n512/b1` | 3.1915 | 1.9235 | 1.6811 |
| `lu/n512/b4` | 12.7176 | 7.5940 | 7.0010 |
| `lu_factor/n256/b1` | 0.3542 | 0.3116 | 0.2395 |
| `lu_factor/n256/b4` | 1.5455 | 0.7768 | 0.9666 |
| `lu_factor/n512/b1` | 2.8251 | 1.4759 | 1.3597 |
| `lu_factor/n512/b4` | 11.7661 | 4.3178 | 5.5350 |
| `lu_factor_solve/n256/b1` | 0.3693 | 0.3301 | 0.2706 |
| `lu_factor_solve/n256/b4` | 1.4947 | 0.7196 | 1.0997 |
| `lu_factor_solve/n512/b1` | 2.8793 | 1.6347 | 1.4708 |
| `lu_factor_solve/n512/b4` | 12.1155 | 5.4511 | 6.0917 |
| `lu_solve_prepared/n256/b1` | 0.0171 | 0.0238 | 0.0270 |
| `lu_solve_prepared/n256/b4` | 0.0804 | 0.0226 | 0.1280 |
| `lu_solve_prepared/n512/b1` | 0.0717 | 0.0695 | 0.1051 |
| `lu_solve_prepared/n512/b4` | 0.4378 | 0.2036 | 0.8375 |
| `qr/n256/b1` | 1.8481 | 1.7842 | 1.6837 |
| `qr/n256/b4` | 7.3844 | 7.1522 | 6.8579 |
| `qr/n512/b1` | 11.4746 | 5.9449 | 9.0200 |
| `qr/n512/b4` | 45.9952 | 24.4494 | 36.9310 |
| `rank_revealing_qr/n256/b1` | 2.0913 | 1.4946 | 2.3206 |
| `rank_revealing_qr/n256/b4` | 8.4646 | 5.9817 | 9.3304 |
| `rank_revealing_qr/n512/b1` | 14.8904 | 6.2681 | 14.6944 |
| `rank_revealing_qr/n512/b4` | 59.7058 | 25.1128 | 59.6510 |
| `solve/n256/b1` | 0.3842 | 0.3564 | 0.2830 |
| `solve/n256/b4` | 1.5412 | 1.4288 | 1.1513 |
| `solve/n512/b1` | 2.8591 | 1.5821 | 1.5302 |
| `solve/n512/b4` | 11.3713 | 6.2812 | 6.1855 |
| `svd_thin/n256/b1` | 12.2531 | 8.7780 | 9.9459 |
| `svd_thin/n256/b4` | 48.9710 | 36.0119 | 40.1019 |
| `svd_thin/n512/b1` | 70.8705 | 39.8474 | 57.5568 |
| `svd_thin/n512/b4` | 283.4858 | 161.5527 | 244.5872 |
| `svd_values/n256/b1` | 7.5192 | 8.2522 | 5.0203 |
| `svd_values/n256/b4` | 29.9209 | 31.3488 | 20.3129 |
| `svd_values/n512/b1` | 41.2350 | 34.6451 | 31.2257 |
| `svd_values/n512/b4` | 169.3280 | 140.6159 | 131.4246 |
| `triangular_solve/n256/b1` | 0.0105 | 0.0155 | 0.0128 |
| `triangular_solve/n256/b4` | 0.0457 | 0.0592 | 0.0614 |
| `triangular_solve/n512/b1` | 0.0346 | 0.0367 | 0.0519 |
| `triangular_solve/n512/b4` | 0.1594 | 0.1487 | 0.2440 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1991 | 0.1973 | 0.1615 |
| `cholesky/n256/b4` | 0.8073 | 0.8069 | 0.6468 |
| `cholesky/n512/b1` | 1.3149 | 0.7153 | 0.6923 |
| `cholesky/n512/b4` | 5.6458 | 3.2632 | 3.1025 |
| `eigh/n256/b1` | 5.5993 | 4.1805 | 3.3134 |
| `eigh/n256/b4` | 22.3922 | 16.9288 | 13.4277 |
| `eigh/n512/b1` | 28.5732 | 14.5280 | 14.1530 |
| `eigh/n512/b4` | 114.6965 | 59.4975 | 56.0066 |
| `eigvalsh/n256/b1` | 16.9662 | 18.0875 | 1.8765 |
| `eigvalsh/n256/b4` | 67.5489 | 68.9503 | 7.4452 |
| `eigvalsh/n512/b1` | 118.2595 | 116.4875 | 6.7332 |
| `eigvalsh/n512/b4` | 472.2555 | 461.9520 | 27.0617 |
| `householder_apply/n256/b1` | 2.3413 | 2.3704 | 1.0569 |
| `householder_apply/n256/b4` | 9.7968 | 9.8060 | 4.1939 |
| `householder_apply/n512/b1` | 18.9481 | 19.0370 | 5.9955 |
| `householder_apply/n512/b4` | 82.8977 | 83.2469 | 24.5637 |
| `householder_factor/n256/b1` | 1.4750 | 1.4970 | 0.8331 |
| `householder_factor/n256/b4` | 5.8991 | 5.9487 | 3.2952 |
| `householder_factor/n512/b1` | 12.1980 | 12.2050 | 4.0737 |
| `householder_factor/n512/b4` | 48.6693 | 48.7943 | 16.2448 |
| `lu/n256/b1` | 0.4616 | 0.4707 | 0.2493 |
| `lu/n256/b4` | 1.9221 | 1.9918 | 1.1032 |
| `lu/n512/b1` | 3.1888 | 1.9929 | 1.1645 |
| `lu/n512/b4` | 12.7389 | 7.8578 | 4.8755 |
| `lu_factor/n256/b1` | 0.3790 | 0.3515 | 0.2055 |
| `lu_factor/n256/b4` | 1.5382 | 1.4583 | 0.8224 |
| `lu_factor/n512/b1` | 2.8421 | 1.5313 | 0.8571 |
| `lu_factor/n512/b4` | 11.7741 | 6.3033 | 3.4612 |
| `lu_factor_solve/n256/b1` | 0.3950 | 0.3897 | 0.2377 |
| `lu_factor_solve/n256/b4` | 1.4854 | 1.4990 | 0.9372 |
| `lu_factor_solve/n512/b1` | 2.9016 | 1.6156 | 0.9887 |
| `lu_factor_solve/n512/b4` | 12.0080 | 6.5362 | 3.9488 |
| `lu_solve_prepared/n256/b1` | 0.0176 | 0.0294 | 0.0260 |
| `lu_solve_prepared/n256/b4` | 0.0770 | 0.1086 | 0.1197 |
| `lu_solve_prepared/n512/b1` | 0.0727 | 0.0757 | 0.1126 |
| `lu_solve_prepared/n512/b4` | 0.3808 | 0.3790 | 0.7940 |
| `qr/n256/b1` | 1.8518 | 2.4599 | 1.6647 |
| `qr/n256/b4` | 7.3980 | 9.8988 | 6.7042 |
| `qr/n512/b1` | 11.5176 | 6.8981 | 8.1191 |
| `qr/n512/b4` | 46.1317 | 28.2031 | 32.8994 |
| `rank_revealing_qr/n256/b1` | 2.1238 | 1.5914 | 2.2910 |
| `rank_revealing_qr/n256/b4` | 8.5278 | 6.3366 | 9.2549 |
| `rank_revealing_qr/n512/b1` | 14.8862 | 5.9171 | 13.8161 |
| `rank_revealing_qr/n512/b4` | 59.8186 | 23.7264 | 56.5734 |
| `solve/n256/b1` | 0.3855 | 0.3927 | 0.2516 |
| `solve/n256/b4` | 1.5443 | 1.6136 | 1.0049 |
| `solve/n512/b1` | 2.8560 | 1.6951 | 1.0379 |
| `solve/n512/b4` | 11.3918 | 6.5624 | 4.1837 |
| `svd_thin/n256/b1` | 12.2139 | 8.9482 | 9.8206 |
| `svd_thin/n256/b4` | 48.7512 | 36.8747 | 39.7244 |
| `svd_thin/n512/b1` | 70.6491 | 38.3848 | 55.3051 |
| `svd_thin/n512/b4` | 281.7207 | 152.8994 | 234.5626 |
| `svd_values/n256/b1` | 7.5112 | 8.4291 | 5.0932 |
| `svd_values/n256/b4` | 29.9185 | 31.7454 | 20.7292 |
| `svd_values/n512/b1` | 41.0572 | 35.3138 | 31.1318 |
| `svd_values/n512/b4` | 168.6698 | 143.3681 | 131.8695 |
| `triangular_solve/n256/b1` | 0.0105 | 0.0190 | 0.0127 |
| `triangular_solve/n256/b4` | 0.0463 | 0.0638 | 0.0615 |
| `triangular_solve/n512/b1` | 0.0339 | 0.0414 | 0.0553 |
| `triangular_solve/n512/b4` | 0.1710 | 0.1870 | 0.3260 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7037 | - | 0.7720 |
| `cholesky/n256/b4` | 2.7806 | - | 3.0698 |
| `cholesky/n512/b1` | 4.5997 | - | 5.4140 |
| `cholesky/n512/b4` | 19.7014 | - | 22.5992 |
| `eigh/n256/b1` | 10.2565 | - | 21.5423 |
| `eigh/n256/b4` | 41.2905 | - | 86.0028 |
| `eigh/n512/b1` | 62.9667 | - | 156.8702 |
| `eigh/n512/b4` | 252.4530 | - | 628.2919 |
| `eigvalsh/n256/b1` | 18.7387 | - | 5.6538 |
| `eigvalsh/n256/b4` | 76.7414 | - | 22.7685 |
| `eigvalsh/n512/b1` | 132.9466 | - | 37.3647 |
| `eigvalsh/n512/b4` | 532.1720 | - | 149.8061 |
| `householder_apply/n256/b1` | 5.2541 | - | 4.7092 |
| `householder_apply/n256/b4` | 21.6548 | - | 19.1291 |
| `householder_apply/n512/b1` | 45.1301 | - | 32.0090 |
| `householder_apply/n512/b4` | 180.0895 | - | 128.6628 |
| `householder_factor/n256/b1` | 3.4662 | - | 3.0071 |
| `householder_factor/n256/b4` | 13.8891 | - | 12.0265 |
| `householder_factor/n512/b1` | 29.3601 | - | 20.7680 |
| `householder_factor/n512/b4` | 118.7297 | - | 83.4851 |
| `lu/n256/b1` | 1.2434 | - | 1.4310 |
| `lu/n256/b4` | 5.1139 | - | 6.0529 |
| `lu/n512/b1` | 8.6908 | - | 10.2934 |
| `lu/n512/b4` | 34.5648 | - | 41.2095 |
| `lu_factor/n256/b1` | 1.1181 | - | 1.3398 |
| `lu_factor/n256/b4` | 4.5054 | - | 5.3248 |
| `lu_factor/n512/b1` | 8.0001 | - | 9.4893 |
| `lu_factor/n512/b4` | 32.6562 | - | 38.1740 |
| `lu_factor_solve/n256/b1` | 1.1834 | - | 1.4686 |
| `lu_factor_solve/n256/b4` | 4.7516 | - | 5.7809 |
| `lu_factor_solve/n512/b1` | 8.2144 | - | 9.9707 |
| `lu_factor_solve/n512/b4` | 33.6274 | - | 40.0283 |
| `lu_solve_prepared/n256/b1` | 0.0629 | - | 0.1345 |
| `lu_solve_prepared/n256/b4` | 0.2639 | - | 0.4924 |
| `lu_solve_prepared/n512/b1` | 0.2094 | - | 0.5066 |
| `lu_solve_prepared/n512/b4` | 1.3091 | - | 2.1206 |
| `qr/n256/b1` | 6.2377 | - | 6.0248 |
| `qr/n256/b4` | 24.9110 | - | 24.1105 |
| `qr/n512/b1` | 42.2617 | - | 41.6499 |
| `qr/n512/b4` | 169.4595 | - | 168.2333 |
| `rank_revealing_qr/n256/b1` | 6.7423 | - | 6.4173 |
| `rank_revealing_qr/n256/b4` | 27.0454 | - | 26.3178 |
| `rank_revealing_qr/n512/b1` | 47.5986 | - | 44.8347 |
| `rank_revealing_qr/n512/b4` | 190.3409 | - | 180.8059 |
| `solve/n256/b1` | 1.1750 | - | 1.4779 |
| `solve/n256/b4` | 4.7097 | - | 6.0351 |
| `solve/n512/b1` | 8.2290 | - | 9.9863 |
| `solve/n512/b4` | 32.7661 | - | 40.5018 |
| `svd_thin/n256/b1` | 24.3686 | - | 23.1169 |
| `svd_thin/n256/b4` | 98.3167 | - | 93.5451 |
| `svd_thin/n512/b1` | 154.3535 | - | 147.9169 |
| `svd_thin/n512/b4` | 617.5513 | - | 604.2730 |
| `svd_values/n256/b1` | 12.2534 | - | 10.4764 |
| `svd_values/n256/b4` | 49.2137 | - | 42.2386 |
| `svd_values/n512/b1` | 71.4795 | - | 62.1510 |
| `svd_values/n512/b4` | 294.5004 | - | 261.9035 |
| `triangular_solve/n256/b1` | 0.0338 | - | 0.0626 |
| `triangular_solve/n256/b4` | 0.1373 | - | 0.2581 |
| `triangular_solve/n512/b1` | 0.1118 | - | 0.2225 |
| `triangular_solve/n512/b4` | 0.5055 | - | 0.9754 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7035 | 0.4950 | 0.3713 |
| `cholesky/n256/b4` | 2.7742 | 1.9656 | 1.3814 |
| `cholesky/n512/b1` | 4.7688 | 2.4664 | 2.0847 |
| `cholesky/n512/b4` | 19.8532 | 10.4741 | 9.3298 |
| `eigh/n256/b1` | 10.2560 | 7.0637 | 19.5108 |
| `eigh/n256/b4` | 41.3318 | 31.8789 | 78.1185 |
| `eigh/n512/b1` | 63.0311 | 28.6140 | 127.2858 |
| `eigh/n512/b4` | 252.9712 | 116.0956 | 514.1531 |
| `eigvalsh/n256/b1` | 18.9730 | 20.0221 | 4.9261 |
| `eigvalsh/n256/b4` | 76.7407 | 77.9228 | 19.8590 |
| `eigvalsh/n512/b1` | 133.0341 | 124.1307 | 20.4563 |
| `eigvalsh/n512/b4` | 532.3292 | 494.3368 | 81.9343 |
| `householder_apply/n256/b1` | 5.2397 | 5.2984 | 2.2355 |
| `householder_apply/n256/b4` | 21.8417 | 21.8447 | 9.1976 |
| `householder_apply/n512/b1` | 45.0987 | 45.1066 | 12.1198 |
| `householder_apply/n512/b4` | 179.7874 | 179.8039 | 49.3569 |
| `householder_factor/n256/b1` | 3.4661 | 3.5116 | 1.7083 |
| `householder_factor/n256/b4` | 13.9949 | 13.9849 | 6.9171 |
| `householder_factor/n512/b1` | 29.7153 | 29.5975 | 8.5082 |
| `householder_factor/n512/b4` | 119.1973 | 118.9367 | 34.6946 |
| `lu/n256/b1` | 1.2427 | 0.8146 | 0.7719 |
| `lu/n256/b4` | 5.1011 | 3.4722 | 3.3073 |
| `lu/n512/b1` | 8.6532 | 3.9051 | 3.7157 |
| `lu/n512/b4` | 34.4632 | 15.3969 | 14.9154 |
| `lu_factor/n256/b1` | 1.1155 | 0.6796 | 0.6662 |
| `lu_factor/n256/b4` | 4.5243 | 1.1783 | 2.6635 |
| `lu_factor/n512/b1` | 7.9880 | 3.0950 | 2.9844 |
| `lu_factor/n512/b4` | 32.6307 | 9.0258 | 11.9732 |
| `lu_factor_solve/n256/b1` | 1.1803 | 0.7396 | 0.7592 |
| `lu_factor_solve/n256/b4` | 4.7654 | 1.2378 | 2.9936 |
| `lu_factor_solve/n512/b1` | 8.2116 | 3.2486 | 3.3548 |
| `lu_factor_solve/n512/b4` | 33.6619 | 9.4355 | 13.5048 |
| `lu_solve_prepared/n256/b1` | 0.0625 | 0.0597 | 0.0938 |
| `lu_solve_prepared/n256/b4` | 0.2619 | 0.0670 | 0.3017 |
| `lu_solve_prepared/n512/b1` | 0.2081 | 0.1552 | 0.3593 |
| `lu_solve_prepared/n512/b4` | 1.3156 | 0.3665 | 1.8991 |
| `qr/n256/b1` | 6.2386 | 3.1370 | 3.4336 |
| `qr/n256/b4` | 24.8683 | 12.4699 | 13.8918 |
| `qr/n512/b1` | 42.3679 | 14.5874 | 17.3336 |
| `qr/n512/b4` | 169.5186 | 58.2784 | 69.7553 |
| `rank_revealing_qr/n256/b1` | 6.7486 | 3.9205 | 3.8654 |
| `rank_revealing_qr/n256/b4` | 26.9002 | 15.9552 | 15.8833 |
| `rank_revealing_qr/n512/b1` | 47.6518 | 16.3559 | 18.9819 |
| `rank_revealing_qr/n512/b4` | 191.4548 | 67.8378 | 76.5952 |
| `solve/n256/b1` | 1.1798 | 0.7582 | 0.8144 |
| `solve/n256/b4` | 4.7089 | 3.0349 | 3.2279 |
| `solve/n512/b1` | 8.2456 | 3.3885 | 3.4366 |
| `solve/n512/b4` | 32.8852 | 13.3813 | 14.1356 |
| `svd_thin/n256/b1` | 24.6547 | 15.6922 | 15.1821 |
| `svd_thin/n256/b4` | 98.5234 | 62.1059 | 61.1326 |
| `svd_thin/n512/b1` | 154.1700 | 68.7631 | 75.7749 |
| `svd_thin/n512/b4` | 615.7202 | 272.8485 | 318.6937 |
| `svd_values/n256/b1` | 12.2521 | 12.5391 | 8.0523 |
| `svd_values/n256/b4` | 49.3770 | 48.9016 | 32.4067 |
| `svd_values/n512/b1` | 71.0370 | 46.8358 | 35.3108 |
| `svd_values/n512/b4` | 293.5436 | 192.9078 | 149.7881 |
| `triangular_solve/n256/b1` | 0.0335 | 0.0338 | 0.0480 |
| `triangular_solve/n256/b4` | 0.1448 | 0.1338 | 0.2169 |
| `triangular_solve/n512/b1` | 0.1121 | 0.0835 | 0.1490 |
| `triangular_solve/n512/b4` | 0.5420 | 0.3727 | 0.8198 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7023 | 0.4925 | 0.3417 |
| `cholesky/n256/b4` | 2.8385 | 1.9654 | 1.3332 |
| `cholesky/n512/b1` | 4.6997 | 1.8371 | 1.4588 |
| `cholesky/n512/b4` | 19.8288 | 8.0009 | 6.5529 |
| `eigh/n256/b1` | 10.2632 | 6.8915 | 19.3134 |
| `eigh/n256/b4` | 41.2428 | 27.8134 | 77.3280 |
| `eigh/n512/b1` | 63.0210 | 24.0705 | 124.0555 |
| `eigh/n512/b4` | 251.6832 | 97.3580 | 498.3241 |
| `eigvalsh/n256/b1` | 19.0708 | 20.0081 | 4.8081 |
| `eigvalsh/n256/b4` | 76.9626 | 77.9512 | 19.3138 |
| `eigvalsh/n512/b1` | 132.5222 | 121.6147 | 17.9120 |
| `eigvalsh/n512/b4` | 530.7804 | 484.6835 | 71.9399 |
| `householder_apply/n256/b1` | 5.2399 | 5.3395 | 1.7598 |
| `householder_apply/n256/b4` | 21.5053 | 21.7500 | 7.2664 |
| `householder_apply/n512/b1` | 44.8872 | 44.8564 | 8.5232 |
| `householder_apply/n512/b4` | 179.2533 | 178.7937 | 35.4088 |
| `householder_factor/n256/b1` | 3.4493 | 3.5266 | 1.5165 |
| `householder_factor/n256/b4` | 13.9899 | 14.1835 | 6.0702 |
| `householder_factor/n512/b1` | 29.6795 | 29.8603 | 6.5445 |
| `householder_factor/n512/b4` | 118.9990 | 118.9012 | 26.1235 |
| `lu/n256/b1` | 1.2494 | 0.8237 | 0.5530 |
| `lu/n256/b4` | 5.1277 | 3.3421 | 2.4733 |
| `lu/n512/b1` | 8.6472 | 3.3103 | 2.3003 |
| `lu/n512/b4` | 34.7848 | 13.0205 | 9.2586 |
| `lu_factor/n256/b1` | 1.1113 | 0.6656 | 0.4585 |
| `lu_factor/n256/b4` | 4.3484 | 2.5715 | 1.7780 |
| `lu_factor/n512/b1` | 8.0120 | 2.6067 | 1.6339 |
| `lu_factor/n512/b4` | 32.6490 | 10.4312 | 6.6334 |
| `lu_factor_solve/n256/b1` | 1.1748 | 0.7203 | 0.5616 |
| `lu_factor_solve/n256/b4` | 4.5911 | 2.8362 | 2.0843 |
| `lu_factor_solve/n512/b1` | 8.2554 | 2.7390 | 2.0125 |
| `lu_factor_solve/n512/b4` | 33.7097 | 11.1579 | 8.0675 |
| `lu_solve_prepared/n256/b1` | 0.0630 | 0.0672 | 0.1024 |
| `lu_solve_prepared/n256/b4` | 0.2607 | 0.2576 | 0.3128 |
| `lu_solve_prepared/n512/b1` | 0.2248 | 0.1719 | 0.3453 |
| `lu_solve_prepared/n512/b4` | 1.1152 | 0.8836 | 1.5818 |
| `qr/n256/b1` | 6.2160 | 3.4510 | 3.0423 |
| `qr/n256/b4` | 24.8934 | 14.2191 | 12.3448 |
| `qr/n512/b1` | 42.4015 | 12.3535 | 13.2019 |
| `qr/n512/b4` | 169.7547 | 50.1194 | 53.2577 |
| `rank_revealing_qr/n256/b1` | 6.7368 | 3.8954 | 3.4835 |
| `rank_revealing_qr/n256/b4` | 27.0522 | 15.1471 | 14.3644 |
| `rank_revealing_qr/n512/b1` | 47.4988 | 12.1832 | 14.8074 |
| `rank_revealing_qr/n512/b4` | 191.0750 | 49.1179 | 59.6893 |
| `solve/n256/b1` | 1.1826 | 0.7544 | 0.5878 |
| `solve/n256/b4` | 4.7078 | 3.0417 | 2.4368 |
| `solve/n512/b1` | 8.2081 | 2.9419 | 2.1259 |
| `solve/n512/b4` | 32.8033 | 11.3388 | 8.6774 |
| `svd_thin/n256/b1` | 24.5069 | 14.8250 | 14.2436 |
| `svd_thin/n256/b4` | 98.2777 | 60.9248 | 56.7660 |
| `svd_thin/n512/b1` | 154.2915 | 55.4601 | 63.5572 |
| `svd_thin/n512/b4` | 617.3204 | 224.1340 | 272.1750 |
| `svd_values/n256/b1` | 12.2348 | 12.3156 | 7.9775 |
| `svd_values/n256/b4` | 48.9671 | 48.8749 | 31.9050 |
| `svd_values/n512/b1` | 71.1488 | 43.8232 | 32.1126 |
| `svd_values/n512/b4` | 294.0498 | 181.9379 | 135.7774 |
| `triangular_solve/n256/b1` | 0.0333 | 0.0374 | 0.0415 |
| `triangular_solve/n256/b4` | 0.1419 | 0.1464 | 0.1710 |
| `triangular_solve/n512/b1` | 0.1147 | 0.0905 | 0.1557 |
| `triangular_solve/n512/b4` | 0.5774 | 0.4094 | 0.8277 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5397 | - | 0.5510 |
| `householder_factor/4096x256/b1` | 42.2500 | - | 23.6016 |
| `qr/1024x64/b1` | 0.9827 | - | 1.0778 |
| `qr/4096x256/b1` | 41.5207 | - | 46.9324 |
| `rank_revealing_qr/1024x64/b1` | 0.9733 | - | 1.1651 |
| `rank_revealing_qr/4096x256/b1` | 65.4628 | - | 57.9107 |
| `svd_thin/1024x64/b1` | 1.4552 | - | 2.9240 |
| `svd_thin/4096x256/b1` | 72.6543 | - | 93.8247 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5369 | 0.5441 | 0.5942 |
| `householder_factor/4096x256/b1` | 41.3096 | 41.3111 | 12.5657 |
| `qr/1024x64/b1` | 0.9837 | 0.8755 | 1.1524 |
| `qr/4096x256/b1` | 41.1079 | 20.1227 | 24.7671 |
| `rank_revealing_qr/1024x64/b1` | 0.9726 | 0.7375 | 1.2599 |
| `rank_revealing_qr/4096x256/b1` | 64.8343 | 23.7481 | 28.1446 |
| `svd_thin/1024x64/b1` | 1.4476 | 1.3805 | 2.8494 |
| `svd_thin/4096x256/b1` | 72.6441 | 39.9937 | 61.1315 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5364 | 0.5458 | 0.5983 |
| `householder_factor/4096x256/b1` | 41.7770 | 41.9431 | 10.9468 |
| `qr/1024x64/b1` | 0.9828 | 1.1291 | 1.1457 |
| `qr/4096x256/b1` | 41.2000 | 19.3225 | 21.5013 |
| `rank_revealing_qr/1024x64/b1` | 0.9724 | 0.7604 | 1.2557 |
| `rank_revealing_qr/4096x256/b1` | 66.4643 | 18.6783 | 24.0632 |
| `svd_thin/1024x64/b1` | 1.4586 | 1.6253 | 2.8125 |
| `svd_thin/4096x256/b1` | 72.5472 | 34.7288 | 56.5965 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.3320 | - | 1.0541 |
| `householder_factor/4096x256/b1` | 128.0753 | - | 68.6006 |
| `qr/1024x64/b1` | 2.8526 | - | 2.0623 |
| `qr/4096x256/b1` | 147.0357 | - | 137.5810 |
| `rank_revealing_qr/1024x64/b1` | 2.8608 | - | 2.2604 |
| `rank_revealing_qr/4096x256/b1` | 245.3587 | - | 173.3861 |
| `svd_thin/1024x64/b1` | 3.5603 | - | 4.8146 |
| `svd_thin/4096x256/b1` | 232.0440 | - | 250.2749 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.3318 | 1.3707 | 0.4342 |
| `householder_factor/4096x256/b1` | 128.8770 | 128.2119 | 20.0268 |
| `qr/1024x64/b1` | 2.8490 | 1.6057 | 0.8059 |
| `qr/4096x256/b1` | 146.7751 | 57.2695 | 40.2105 |
| `rank_revealing_qr/1024x64/b1` | 2.8699 | 1.7553 | 1.0311 |
| `rank_revealing_qr/4096x256/b1` | 245.4363 | 82.7151 | 55.3650 |
| `svd_thin/1024x64/b1` | 3.5516 | 2.2913 | 2.9539 |
| `svd_thin/4096x256/b1` | 232.1638 | 103.5980 | 107.7095 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-openblas (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.3273 | 1.3702 | 0.3446 |
| `householder_factor/4096x256/b1` | 128.8115 | 128.5646 | 12.4687 |
| `qr/1024x64/b1` | 2.8604 | 1.7584 | 0.6271 |
| `qr/4096x256/b1` | 147.1445 | 46.0896 | 25.6223 |
| `rank_revealing_qr/1024x64/b1` | 2.8523 | 1.7201 | 0.8650 |
| `rank_revealing_qr/4096x256/b1` | 244.4399 | 52.3611 | 34.2703 |
| `svd_thin/1024x64/b1` | 3.5456 | 2.4270 | 2.6767 |
| `svd_thin/4096x256/b1` | 232.6486 | 85.5538 | 85.8172 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
