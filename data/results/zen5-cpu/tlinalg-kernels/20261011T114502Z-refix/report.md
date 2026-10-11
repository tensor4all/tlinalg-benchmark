# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `9e0796cacb99e3374840e06d8ea47279e6ebf838`
- features: `tlinalg-bench/link-mkl`
- faer provider: `t4a-faer` 0.24.4 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9); `t4a-faer-traits` 0.24.0 @ `d16929be4582c6b3679f5ec17223227bbfc289c9` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=d16929be4582c6b3679f5ec17223227bbfc289c9#d16929be4582c6b3679f5ec17223227bbfc289c9)
- harness commit: `73b4f7df95227aba5f47dd4af4a7054491d29d92`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-11T12:39:29.870091Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --vendor mkl --checkout /tmp/tl-pin2 --aa 1 --label refix`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261011T114502Z-refix/`

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
| `cholesky/n16/b1` | 0.0006 | - | 0.0007 |
| `cholesky/n16/b1024` | 0.5160 | - | 0.6329 |
| `cholesky/n4/b1` | 0.0002 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1079 | - | 0.0733 |
| `cholesky/n8/b1` | 0.0003 | - | 0.0003 |
| `cholesky/n8/b1024` | 0.2139 | - | 0.1927 |
| `eig/n16/b1` | 0.0533 | - | 0.0307 |
| `eig/n16/b1024` | 55.6990 | - | 32.0951 |
| `eig/n4/b1` | 0.0040 | - | 0.0022 |
| `eig/n4/b1024` | 3.5257 | - | 1.7480 |
| `eig/n8/b1` | 0.0143 | - | 0.0075 |
| `eig/n8/b1024` | 13.6942 | - | 7.0582 |
| `eigh/n16/b1` | 0.0178 | - | 0.0136 |
| `eigh/n16/b1024` | 18.0388 | - | 14.1145 |
| `eigh/n4/b1` | 0.0016 | - | 0.0019 |
| `eigh/n4/b1024` | 1.4398 | - | 1.7086 |
| `eigh/n8/b1` | 0.0052 | - | 0.0048 |
| `eigh/n8/b1024` | 5.0296 | - | 4.6634 |
| `eigvals/n16/b1` | 0.0372 | - | 0.0211 |
| `eigvals/n16/b1024` | 39.3133 | - | 22.0778 |
| `eigvals/n4/b1` | 0.0024 | - | 0.0017 |
| `eigvals/n4/b1024` | 1.9354 | - | 1.2617 |
| `eigvals/n8/b1` | 0.0098 | - | 0.0059 |
| `eigvals/n8/b1024` | 9.2640 | - | 5.3713 |
| `eigvalsh/n16/b1` | 0.0134 | - | 0.0078 |
| `eigvalsh/n16/b1024` | 13.3028 | - | 7.8275 |
| `eigvalsh/n4/b1` | 0.0013 | - | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1639 | - | 0.8932 |
| `eigvalsh/n8/b1` | 0.0042 | - | 0.0030 |
| `eigvalsh/n8/b1024` | 4.0174 | - | 2.6833 |
| `full_piv_lu/n16/b1` | 0.0028 | - | 0.0024 |
| `full_piv_lu/n16/b1024` | 2.2559 | - | 2.3421 |
| `full_piv_lu/n4/b1` | 0.0006 | - | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2359 | - | 0.2452 |
| `full_piv_lu/n8/b1` | 0.0010 | - | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6271 | - | 0.5869 |
| `full_piv_lu_solve/n16/b1` | 0.0027 | - | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0463 | - | 3.4741 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | - | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3055 | - | 0.6709 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | - | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7304 | - | 1.1730 |
| `householder_apply/n16/b1` | 0.0028 | - | 0.0018 |
| `householder_apply/n16/b1024` | 2.7554 | - | 1.5991 |
| `householder_apply/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.1993 | - | 0.2025 |
| `householder_apply/n8/b1` | 0.0008 | - | 0.0007 |
| `householder_apply/n8/b1024` | 0.6638 | - | 0.4836 |
| `householder_factor/n16/b1` | 0.0022 | - | 0.0018 |
| `householder_factor/n16/b1024` | 2.1550 | - | 1.7647 |
| `householder_factor/n4/b1` | 0.0003 | - | 0.0003 |
| `householder_factor/n4/b1024` | 0.2424 | - | 0.1828 |
| `householder_factor/n8/b1` | 0.0008 | - | 0.0006 |
| `householder_factor/n8/b1024` | 0.6729 | - | 0.5045 |
| `lu/n16/b1` | 0.0020 | - | 0.0012 |
| `lu/n16/b1024` | 1.5569 | - | 1.0521 |
| `lu/n4/b1` | 0.0004 | - | 0.0003 |
| `lu/n4/b1024` | 0.1698 | - | 0.1042 |
| `lu/n8/b1` | 0.0007 | - | 0.0005 |
| `lu/n8/b1024` | 0.4866 | - | 0.3019 |
| `lu_factor/n16/b1` | 0.0013 | - | 0.0007 |
| `lu_factor/n16/b1024` | 1.1380 | - | 0.7025 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0001 |
| `lu_factor/n4/b1024` | 0.1357 | - | 0.0374 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0002 |
| `lu_factor/n8/b1024` | 0.3507 | - | 0.1583 |
| `lu_factor_solve/n16/b1` | 0.0018 | - | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4882 | - | 1.4466 |
| `lu_factor_solve/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1864 | - | 0.1072 |
| `lu_factor_solve/n8/b1` | 0.0007 | - | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4960 | - | 0.4974 |
| `lu_solve_prepared/n16/b1` | 0.0005 | - | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3572 | - | 0.6392 |
| `lu_solve_prepared/n4/b1` | 0.0002 | - | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0402 | - | 0.0786 |
| `lu_solve_prepared/n8/b1` | 0.0003 | - | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1383 | - | 0.3545 |
| `qr/n16/b1` | 0.0057 | - | 0.0034 |
| `qr/n16/b1024` | 5.5048 | - | 3.1657 |
| `qr/n4/b1` | 0.0008 | - | 0.0007 |
| `qr/n4/b1024` | 0.4407 | - | 0.4071 |
| `qr/n8/b1` | 0.0016 | - | 0.0013 |
| `qr/n8/b1024` | 1.4178 | - | 1.0353 |
| `rank_revealing_qr/n16/b1` | 0.0066 | - | 0.0054 |
| `rank_revealing_qr/n16/b1024` | 6.2691 | - | 4.9682 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7155 | - | 0.7369 |
| `rank_revealing_qr/n8/b1` | 0.0023 | - | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.9679 | - | 1.7625 |
| `solve/n16/b1` | 0.0022 | - | 0.0018 |
| `solve/n16/b1024` | 1.5941 | - | 1.4712 |
| `solve/n4/b1` | 0.0006 | - | 0.0003 |
| `solve/n4/b1024` | 0.2172 | - | 0.1432 |
| `solve/n8/b1` | 0.0010 | - | 0.0007 |
| `solve/n8/b1024` | 0.5430 | - | 0.5417 |
| `svd_full/n16/b1` | 0.0332 | - | 0.0306 |
| `svd_full/n16/b1024` | 33.9707 | - | 31.1060 |
| `svd_full/n4/b1` | 0.0028 | - | 0.0039 |
| `svd_full/n4/b1024` | 2.5292 | - | 3.6755 |
| `svd_full/n8/b1` | 0.0090 | - | 0.0108 |
| `svd_full/n8/b1024` | 9.1131 | - | 11.1635 |
| `svd_thin/n16/b1` | 0.0333 | - | 0.0308 |
| `svd_thin/n16/b1024` | 34.1350 | - | 31.0952 |
| `svd_thin/n4/b1` | 0.0027 | - | 0.0039 |
| `svd_thin/n4/b1024` | 2.5293 | - | 3.6949 |
| `svd_thin/n8/b1` | 0.0091 | - | 0.0107 |
| `svd_thin/n8/b1024` | 9.0847 | - | 11.1877 |
| `svd_values/n16/b1` | 0.0240 | - | 0.0113 |
| `svd_values/n16/b1024` | 24.3872 | - | 11.6073 |
| `svd_values/n4/b1` | 0.0022 | - | 0.0019 |
| `svd_values/n4/b1024` | 1.8966 | - | 1.5913 |
| `svd_values/n8/b1` | 0.0068 | - | 0.0041 |
| `svd_values/n8/b1024` | 6.7617 | - | 4.0278 |
| `triangular_solve/n16/b1` | 0.0005 | - | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3016 | - | 0.3509 |
| `triangular_solve/n4/b1` | 0.0002 | - | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0511 | - | 0.1915 |
| `triangular_solve/n8/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1313 | - | 0.2383 |

## small, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0027 | 0.0007 |
| `cholesky/n16/b1024` | 0.4883 | 0.1275 | 0.6247 |
| `cholesky/n4/b1` | 0.0002 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1072 | 0.0341 | 0.0724 |
| `cholesky/n8/b1` | 0.0004 | 0.0028 | 0.0003 |
| `cholesky/n8/b1024` | 0.2156 | 0.1114 | 0.1863 |
| `eig/n16/b1` | 0.0534 | 0.0571 | 0.0307 |
| `eig/n16/b1024` | 55.8079 | 14.0548 | 31.9279 |
| `eig/n4/b1` | 0.0041 | 0.0067 | 0.0022 |
| `eig/n4/b1024` | 3.5614 | 1.7950 | 1.7546 |
| `eig/n8/b1` | 0.0141 | 0.0170 | 0.0075 |
| `eig/n8/b1024` | 13.7289 | 6.4820 | 7.0403 |
| `eigh/n16/b1` | 0.0177 | 0.0207 | 0.0136 |
| `eigh/n16/b1024` | 17.8149 | 4.9150 | 14.1023 |
| `eigh/n4/b1` | 0.0016 | 0.0041 | 0.0019 |
| `eigh/n4/b1024` | 1.4309 | 0.7246 | 1.6713 |
| `eigh/n8/b1` | 0.0051 | 0.0074 | 0.0048 |
| `eigh/n8/b1024` | 4.9773 | 2.5271 | 4.6310 |
| `eigvals/n16/b1` | 0.0372 | 0.0404 | 0.0212 |
| `eigvals/n16/b1024` | 38.9445 | 10.2132 | 21.9645 |
| `eigvals/n4/b1` | 0.0024 | 0.0045 | 0.0017 |
| `eigvals/n4/b1024` | 1.9188 | 0.9624 | 1.2643 |
| `eigvals/n8/b1` | 0.0098 | 0.0125 | 0.0059 |
| `eigvals/n8/b1024` | 9.3749 | 2.3088 | 5.3743 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0161 | 0.0078 |
| `eigvalsh/n16/b1024` | 13.4409 | 6.3055 | 7.7954 |
| `eigvalsh/n4/b1` | 0.0013 | 0.0034 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.1580 | 0.5863 | 0.8872 |
| `eigvalsh/n8/b1` | 0.0043 | 0.0066 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0166 | 2.0388 | 2.6417 |
| `full_piv_lu/n16/b1` | 0.0028 | 0.0047 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.2672 | 1.1506 | 2.3437 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0027 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2269 | 0.0622 | 0.2482 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0037 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6169 | 0.3178 | 0.5751 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0051 | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0686 | 0.5273 | 3.4749 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0024 | 0.0010 |
| `full_piv_lu_solve/n4/b1024` | 0.3061 | 0.1619 | 0.6712 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0034 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7406 | 0.3729 | 1.1772 |
| `householder_apply/n16/b1` | 0.0027 | 0.0044 | 0.0018 |
| `householder_apply/n16/b1024` | 2.6438 | 0.6915 | 1.6368 |
| `householder_apply/n4/b1` | 0.0004 | 0.0026 | 0.0004 |
| `householder_apply/n4/b1024` | 0.1819 | 0.0958 | 0.1927 |
| `householder_apply/n8/b1` | 0.0007 | 0.0035 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6445 | 0.1745 | 0.4699 |
| `householder_factor/n16/b1` | 0.0021 | 0.0037 | 0.0018 |
| `householder_factor/n16/b1024` | 2.0998 | 0.5320 | 1.7673 |
| `householder_factor/n4/b1` | 0.0003 | 0.0026 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2406 | 0.0662 | 0.1836 |
| `householder_factor/n8/b1` | 0.0007 | 0.0023 | 0.0007 |
| `householder_factor/n8/b1024` | 0.6701 | 0.3307 | 0.5033 |
| `lu/n16/b1` | 0.0020 | 0.0035 | 0.0011 |
| `lu/n16/b1024` | 1.5448 | 0.4227 | 1.0252 |
| `lu/n4/b1` | 0.0004 | 0.0020 | 0.0003 |
| `lu/n4/b1024` | 0.1689 | 0.0889 | 0.1027 |
| `lu/n8/b1` | 0.0007 | 0.0035 | 0.0005 |
| `lu/n8/b1024` | 0.4808 | 0.2470 | 0.3018 |
| `lu_factor/n16/b1` | 0.0014 | 0.0037 | 0.0008 |
| `lu_factor/n16/b1024` | 1.1377 | 0.2946 | 0.7359 |
| `lu_factor/n4/b1` | 0.0004 | 0.0027 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1329 | 0.0385 | 0.0397 |
| `lu_factor/n8/b1` | 0.0006 | 0.0024 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3622 | 0.0936 | 0.1590 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0039 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4402 | 0.3629 | 1.4038 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0022 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1634 | 0.0466 | 0.1093 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0035 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4730 | 0.1257 | 0.4962 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0028 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3582 | 0.1879 | 0.6353 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0027 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0401 | 0.0204 | 0.0787 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0028 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1370 | 0.0459 | 0.3519 |
| `qr/n16/b1` | 0.0056 | 0.0079 | 0.0033 |
| `qr/n16/b1024` | 5.1673 | 1.6804 | 3.1581 |
| `qr/n4/b1` | 0.0008 | 0.0028 | 0.0007 |
| `qr/n4/b1024` | 0.4334 | 0.2250 | 0.4065 |
| `qr/n8/b1` | 0.0016 | 0.0040 | 0.0013 |
| `qr/n8/b1024` | 1.4071 | 0.6801 | 0.9926 |
| `rank_revealing_qr/n16/b1` | 0.0065 | 0.0095 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.0062 | 3.0372 | 4.9917 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0033 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7082 | 0.3610 | 0.7312 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0048 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.8910 | 0.9518 | 1.7452 |
| `solve/n16/b1` | 0.0022 | 0.0037 | 0.0018 |
| `solve/n16/b1024` | 1.5623 | 0.3987 | 1.4993 |
| `solve/n4/b1` | 0.0006 | 0.0027 | 0.0003 |
| `solve/n4/b1024` | 0.2161 | 0.0596 | 0.1399 |
| `solve/n8/b1` | 0.0010 | 0.0035 | 0.0007 |
| `solve/n8/b1024` | 0.5416 | 0.2741 | 0.5274 |
| `svd_full/n16/b1` | 0.0324 | 0.0357 | 0.0305 |
| `svd_full/n16/b1024` | 33.2927 | 9.8204 | 30.9565 |
| `svd_full/n4/b1` | 0.0027 | 0.0050 | 0.0039 |
| `svd_full/n4/b1024` | 2.5007 | 1.0984 | 3.6601 |
| `svd_full/n8/b1` | 0.0091 | 0.0121 | 0.0106 |
| `svd_full/n8/b1024` | 9.0647 | 2.3265 | 11.1186 |
| `svd_thin/n16/b1` | 0.0328 | 0.0355 | 0.0306 |
| `svd_thin/n16/b1024` | 33.8378 | 10.2948 | 30.9548 |
| `svd_thin/n4/b1` | 0.0027 | 0.0050 | 0.0039 |
| `svd_thin/n4/b1024` | 2.5228 | 1.2863 | 3.6457 |
| `svd_thin/n8/b1` | 0.0089 | 0.0119 | 0.0106 |
| `svd_thin/n8/b1024` | 9.0192 | 3.4386 | 11.0831 |
| `svd_values/n16/b1` | 0.0242 | 0.0266 | 0.0113 |
| `svd_values/n16/b1024` | 24.4595 | 6.1876 | 11.6386 |
| `svd_values/n4/b1` | 0.0022 | 0.0043 | 0.0019 |
| `svd_values/n4/b1024` | 1.8977 | 0.5074 | 1.5833 |
| `svd_values/n8/b1` | 0.0068 | 0.0093 | 0.0041 |
| `svd_values/n8/b1024` | 6.7412 | 3.4082 | 4.0375 |
| `triangular_solve/n16/b1` | 0.0005 | 0.0028 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.2986 | 0.0802 | 0.3532 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0028 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0511 | 0.0192 | 0.1938 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0028 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1298 | 0.0413 | 0.2393 |

## small, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0006 | 0.0038 | 0.0007 |
| `cholesky/n16/b1024` | 0.4951 | 0.0677 | 0.6280 |
| `cholesky/n4/b1` | 0.0002 | 0.0032 | 0.0002 |
| `cholesky/n4/b1024` | 0.1064 | 0.0217 | 0.0740 |
| `cholesky/n8/b1` | 0.0003 | 0.0040 | 0.0003 |
| `cholesky/n8/b1024` | 0.2189 | 0.0592 | 0.1905 |
| `eig/n16/b1` | 0.0537 | 0.0576 | 0.0306 |
| `eig/n16/b1024` | 55.8068 | 7.4294 | 31.8916 |
| `eig/n4/b1` | 0.0039 | 0.0062 | 0.0022 |
| `eig/n4/b1024` | 3.5387 | 0.8934 | 1.7511 |
| `eig/n8/b1` | 0.0142 | 0.0170 | 0.0075 |
| `eig/n8/b1024` | 13.6283 | 1.7555 | 7.0164 |
| `eigh/n16/b1` | 0.0176 | 0.0208 | 0.0135 |
| `eigh/n16/b1024` | 17.7749 | 2.2672 | 14.0703 |
| `eigh/n4/b1` | 0.0017 | 0.0047 | 0.0020 |
| `eigh/n4/b1024` | 1.4358 | 0.1866 | 1.6985 |
| `eigh/n8/b1` | 0.0052 | 0.0085 | 0.0048 |
| `eigh/n8/b1024` | 5.0083 | 0.6509 | 4.6503 |
| `eigvals/n16/b1` | 0.0370 | 0.0402 | 0.0211 |
| `eigvals/n16/b1024` | 39.0608 | 5.5651 | 21.9819 |
| `eigvals/n4/b1` | 0.0024 | 0.0055 | 0.0017 |
| `eigvals/n4/b1024` | 1.9171 | 0.2456 | 1.2671 |
| `eigvals/n8/b1` | 0.0097 | 0.0121 | 0.0059 |
| `eigvals/n8/b1024` | 9.1226 | 1.7170 | 5.3560 |
| `eigvalsh/n16/b1` | 0.0133 | 0.0163 | 0.0077 |
| `eigvalsh/n16/b1024` | 13.2892 | 1.7031 | 7.7794 |
| `eigvalsh/n4/b1` | 0.0014 | 0.0047 | 0.0012 |
| `eigvalsh/n4/b1024` | 1.2040 | 0.3047 | 0.8855 |
| `eigvalsh/n8/b1` | 0.0044 | 0.0069 | 0.0029 |
| `eigvalsh/n8/b1024` | 4.0268 | 0.5110 | 2.6401 |
| `full_piv_lu/n16/b1` | 0.0028 | 0.0058 | 0.0023 |
| `full_piv_lu/n16/b1024` | 2.2161 | 0.5655 | 2.3610 |
| `full_piv_lu/n4/b1` | 0.0006 | 0.0025 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2182 | 0.0404 | 0.2431 |
| `full_piv_lu/n8/b1` | 0.0010 | 0.0045 | 0.0008 |
| `full_piv_lu/n8/b1024` | 0.6439 | 0.1647 | 0.5786 |
| `full_piv_lu_solve/n16/b1` | 0.0026 | 0.0056 | 0.0036 |
| `full_piv_lu_solve/n16/b1024` | 2.0322 | 0.5199 | 3.4728 |
| `full_piv_lu_solve/n4/b1` | 0.0008 | 0.0025 | 0.0009 |
| `full_piv_lu_solve/n4/b1024` | 0.3050 | 0.0834 | 0.6621 |
| `full_piv_lu_solve/n8/b1` | 0.0012 | 0.0044 | 0.0014 |
| `full_piv_lu_solve/n8/b1024` | 0.7539 | 0.1877 | 1.1649 |
| `householder_apply/n16/b1` | 0.0026 | 0.0056 | 0.0018 |
| `householder_apply/n16/b1024` | 2.7029 | 0.6492 | 1.6201 |
| `householder_apply/n4/b1` | 0.0004 | 0.0025 | 0.0004 |
| `householder_apply/n4/b1024` | 0.1824 | 0.0500 | 0.1942 |
| `householder_apply/n8/b1` | 0.0007 | 0.0024 | 0.0007 |
| `householder_apply/n8/b1024` | 0.6286 | 0.1660 | 0.4729 |
| `householder_factor/n16/b1` | 0.0021 | 0.0051 | 0.0018 |
| `householder_factor/n16/b1024` | 2.1043 | 0.5294 | 1.7715 |
| `householder_factor/n4/b1` | 0.0003 | 0.0021 | 0.0003 |
| `householder_factor/n4/b1024` | 0.2459 | 0.0653 | 0.1835 |
| `householder_factor/n8/b1` | 0.0007 | 0.0035 | 0.0007 |
| `householder_factor/n8/b1024` | 0.6454 | 0.1703 | 0.5042 |
| `lu/n16/b1` | 0.0019 | 0.0051 | 0.0011 |
| `lu/n16/b1024` | 1.5438 | 0.3836 | 1.0085 |
| `lu/n4/b1` | 0.0004 | 0.0031 | 0.0003 |
| `lu/n4/b1024` | 0.1698 | 0.0483 | 0.1040 |
| `lu/n8/b1` | 0.0007 | 0.0046 | 0.0005 |
| `lu/n8/b1024` | 0.4817 | 0.1272 | 0.3116 |
| `lu_factor/n16/b1` | 0.0013 | 0.0043 | 0.0007 |
| `lu_factor/n16/b1024` | 1.1045 | 0.2105 | 0.7390 |
| `lu_factor/n4/b1` | 0.0003 | 0.0038 | 0.0001 |
| `lu_factor/n4/b1024` | 0.1313 | 0.0387 | 0.0374 |
| `lu_factor/n8/b1` | 0.0006 | 0.0030 | 0.0002 |
| `lu_factor/n8/b1024` | 0.3538 | 0.0956 | 0.1579 |
| `lu_factor_solve/n16/b1` | 0.0017 | 0.0051 | 0.0015 |
| `lu_factor_solve/n16/b1024` | 1.4495 | 0.3707 | 1.4268 |
| `lu_factor_solve/n4/b1` | 0.0004 | 0.0023 | 0.0002 |
| `lu_factor_solve/n4/b1024` | 0.1636 | 0.0476 | 0.1076 |
| `lu_factor_solve/n8/b1` | 0.0007 | 0.0038 | 0.0005 |
| `lu_factor_solve/n8/b1024` | 0.4710 | 0.1267 | 0.4951 |
| `lu_solve_prepared/n16/b1` | 0.0005 | 0.0023 | 0.0007 |
| `lu_solve_prepared/n16/b1024` | 0.3572 | 0.1047 | 0.6399 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0032 | 0.0001 |
| `lu_solve_prepared/n4/b1024` | 0.0401 | 0.0190 | 0.0784 |
| `lu_solve_prepared/n8/b1` | 0.0003 | 0.0022 | 0.0004 |
| `lu_solve_prepared/n8/b1024` | 0.1366 | 0.0364 | 0.3509 |
| `qr/n16/b1` | 0.0055 | 0.0082 | 0.0034 |
| `qr/n16/b1024` | 5.1839 | 1.3333 | 3.1790 |
| `qr/n4/b1` | 0.0008 | 0.0039 | 0.0007 |
| `qr/n4/b1024` | 0.4402 | 0.0645 | 0.4068 |
| `qr/n8/b1` | 0.0016 | 0.0050 | 0.0013 |
| `qr/n8/b1024` | 1.3800 | 0.3478 | 0.9916 |
| `rank_revealing_qr/n16/b1` | 0.0064 | 0.0088 | 0.0053 |
| `rank_revealing_qr/n16/b1024` | 6.0098 | 1.1495 | 4.9862 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0040 | 0.0012 |
| `rank_revealing_qr/n4/b1024` | 0.7180 | 0.0989 | 0.7269 |
| `rank_revealing_qr/n8/b1` | 0.0022 | 0.0057 | 0.0022 |
| `rank_revealing_qr/n8/b1024` | 1.9045 | 0.4811 | 1.7424 |
| `solve/n16/b1` | 0.0022 | 0.0052 | 0.0018 |
| `solve/n16/b1024` | 1.5117 | 0.3905 | 1.4754 |
| `solve/n4/b1` | 0.0006 | 0.0041 | 0.0003 |
| `solve/n4/b1024` | 0.2150 | 0.0363 | 0.1414 |
| `solve/n8/b1` | 0.0010 | 0.0034 | 0.0007 |
| `solve/n8/b1024` | 0.5376 | 0.0719 | 0.5428 |
| `svd_full/n16/b1` | 0.0345 | 0.0358 | 0.0305 |
| `svd_full/n16/b1024` | 35.0808 | 7.0225 | 30.9495 |
| `svd_full/n4/b1` | 0.0029 | 0.0057 | 0.0039 |
| `svd_full/n4/b1024` | 2.6440 | 0.3208 | 3.6393 |
| `svd_full/n8/b1` | 0.0091 | 0.0118 | 0.0107 |
| `svd_full/n8/b1024` | 9.1530 | 2.2992 | 11.0691 |
| `svd_thin/n16/b1` | 0.0341 | 0.0356 | 0.0306 |
| `svd_thin/n16/b1024` | 34.8960 | 4.7613 | 30.9969 |
| `svd_thin/n4/b1` | 0.0029 | 0.0060 | 0.0039 |
| `svd_thin/n4/b1024` | 2.6337 | 0.3217 | 3.6542 |
| `svd_thin/n8/b1` | 0.0091 | 0.0118 | 0.0107 |
| `svd_thin/n8/b1024` | 9.1266 | 1.4188 | 11.1181 |
| `svd_values/n16/b1` | 0.0240 | 0.0268 | 0.0112 |
| `svd_values/n16/b1024` | 24.6051 | 6.1444 | 11.5897 |
| `svd_values/n4/b1` | 0.0022 | 0.0049 | 0.0019 |
| `svd_values/n4/b1024` | 1.8910 | 0.4816 | 1.5842 |
| `svd_values/n8/b1` | 0.0069 | 0.0097 | 0.0041 |
| `svd_values/n8/b1024` | 6.7510 | 0.9001 | 4.0300 |
| `triangular_solve/n16/b1` | 0.0004 | 0.0022 | 0.0005 |
| `triangular_solve/n16/b1024` | 0.3086 | 0.0816 | 0.3574 |
| `triangular_solve/n4/b1` | 0.0002 | 0.0027 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0512 | 0.0158 | 0.1955 |
| `triangular_solve/n8/b1` | 0.0003 | 0.0027 | 0.0004 |
| `triangular_solve/n8/b1024` | 0.1312 | 0.0370 | 0.2453 |

## small, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | - | 0.0012 |
| `cholesky/n16/b1024` | 0.8018 | - | 1.1151 |
| `cholesky/n4/b1` | 0.0003 | - | 0.0002 |
| `cholesky/n4/b1024` | 0.1192 | - | 0.1074 |
| `cholesky/n8/b1` | 0.0004 | - | 0.0004 |
| `cholesky/n8/b1024` | 0.2506 | - | 0.2812 |
| `eig/n16/b1` | 0.0718 | - | 0.0991 |
| `eig/n16/b1024` | 76.3753 | - | 107.1414 |
| `eig/n4/b1` | 0.0060 | - | 0.0077 |
| `eig/n4/b1024` | 5.8614 | - | 7.4752 |
| `eig/n8/b1` | 0.0200 | - | 0.0250 |
| `eig/n8/b1024` | 20.5506 | - | 26.0653 |
| `eigh/n16/b1` | 0.0182 | - | 0.0187 |
| `eigh/n16/b1024` | 19.6209 | - | 19.5478 |
| `eigh/n4/b1` | 0.0020 | - | 0.0019 |
| `eigh/n4/b1024` | 1.7545 | - | 1.7022 |
| `eigh/n8/b1` | 0.0057 | - | 0.0054 |
| `eigh/n8/b1024` | 5.4949 | - | 5.3852 |
| `eigvals/n16/b1` | 0.0438 | - | 0.0684 |
| `eigvals/n16/b1024` | 46.5284 | - | 75.2655 |
| `eigvals/n4/b1` | 0.0032 | - | 0.0061 |
| `eigvals/n4/b1024` | 2.8177 | - | 5.7629 |
| `eigvals/n8/b1` | 0.0117 | - | 0.0196 |
| `eigvals/n8/b1024` | 11.8790 | - | 20.6591 |
| `eigvalsh/n16/b1` | 0.0137 | - | 0.0110 |
| `eigvalsh/n16/b1024` | 14.4106 | - | 11.0905 |
| `eigvalsh/n4/b1` | 0.0017 | - | 0.0014 |
| `eigvalsh/n4/b1024` | 1.4618 | - | 1.0925 |
| `eigvalsh/n8/b1` | 0.0047 | - | 0.0036 |
| `eigvalsh/n8/b1024` | 4.4159 | - | 3.3618 |
| `full_piv_lu/n16/b1` | 0.0032 | - | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.7815 | - | 3.4946 |
| `full_piv_lu/n4/b1` | 0.0007 | - | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.3285 | - | 0.3103 |
| `full_piv_lu/n8/b1` | 0.0012 | - | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.8184 | - | 0.7439 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | - | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1276 | - | 5.1375 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | - | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4778 | - | 0.9507 |
| `full_piv_lu_solve/n8/b1` | 0.0017 | - | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1630 | - | 1.9209 |
| `householder_apply/n16/b1` | 0.0027 | - | 0.0035 |
| `householder_apply/n16/b1024` | 3.3414 | - | 4.1562 |
| `householder_apply/n4/b1` | 0.0003 | - | 0.0005 |
| `householder_apply/n4/b1024` | 0.1862 | - | 0.2561 |
| `householder_apply/n8/b1` | 0.0007 | - | 0.0010 |
| `householder_apply/n8/b1024` | 0.6356 | - | 0.7738 |
| `householder_factor/n16/b1` | 0.0026 | - | 0.0038 |
| `householder_factor/n16/b1024` | 2.5966 | - | 3.8148 |
| `householder_factor/n4/b1` | 0.0004 | - | 0.0005 |
| `householder_factor/n4/b1024` | 0.3086 | - | 0.3081 |
| `householder_factor/n8/b1` | 0.0009 | - | 0.0010 |
| `householder_factor/n8/b1024` | 0.8121 | - | 0.8887 |
| `lu/n16/b1` | 0.0022 | - | 0.0022 |
| `lu/n16/b1024` | 1.8935 | - | 2.2586 |
| `lu/n4/b1` | 0.0005 | - | 0.0003 |
| `lu/n4/b1024` | 0.2286 | - | 0.1715 |
| `lu/n8/b1` | 0.0008 | - | 0.0007 |
| `lu/n8/b1024` | 0.5725 | - | 0.5370 |
| `lu_factor/n16/b1` | 0.0015 | - | 0.0016 |
| `lu_factor/n16/b1024` | 1.2469 | - | 1.5894 |
| `lu_factor/n4/b1` | 0.0004 | - | 0.0002 |
| `lu_factor/n4/b1024` | 0.1766 | - | 0.1103 |
| `lu_factor/n8/b1` | 0.0006 | - | 0.0004 |
| `lu_factor/n8/b1024` | 0.4110 | - | 0.3690 |
| `lu_factor_solve/n16/b1` | 0.0024 | - | 0.0031 |
| `lu_factor_solve/n16/b1024` | 2.0080 | - | 3.1646 |
| `lu_factor_solve/n4/b1` | 0.0005 | - | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2582 | - | 0.2512 |
| `lu_factor_solve/n8/b1` | 0.0010 | - | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6869 | - | 1.0017 |
| `lu_solve_prepared/n16/b1` | 0.0009 | - | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7814 | - | 1.5535 |
| `lu_solve_prepared/n4/b1` | 0.0003 | - | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0972 | - | 0.1448 |
| `lu_solve_prepared/n8/b1` | 0.0004 | - | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2893 | - | 0.6486 |
| `qr/n16/b1` | 0.0067 | - | 0.0064 |
| `qr/n16/b1024` | 6.5703 | - | 6.5830 |
| `qr/n4/b1` | 0.0007 | - | 0.0009 |
| `qr/n4/b1024` | 0.5062 | - | 0.5744 |
| `qr/n8/b1` | 0.0017 | - | 0.0019 |
| `qr/n8/b1024` | 1.5449 | - | 1.6089 |
| `rank_revealing_qr/n16/b1` | 0.0076 | - | 0.0094 |
| `rank_revealing_qr/n16/b1024` | 7.3526 | - | 9.5740 |
| `rank_revealing_qr/n4/b1` | 0.0011 | - | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8464 | - | 1.0848 |
| `rank_revealing_qr/n8/b1` | 0.0025 | - | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.2606 | - | 2.9089 |
| `solve/n16/b1` | 0.0029 | - | 0.0036 |
| `solve/n16/b1024` | 2.2788 | - | 3.3486 |
| `solve/n4/b1` | 0.0007 | - | 0.0005 |
| `solve/n4/b1024` | 0.3072 | - | 0.2869 |
| `solve/n8/b1` | 0.0012 | - | 0.0012 |
| `solve/n8/b1024` | 0.7581 | - | 1.0489 |
| `svd_full/n16/b1` | 0.0349 | - | 0.0394 |
| `svd_full/n16/b1024` | 36.8495 | - | 40.8520 |
| `svd_full/n4/b1` | 0.0031 | - | 0.0047 |
| `svd_full/n4/b1024` | 3.0145 | - | 4.4562 |
| `svd_full/n8/b1` | 0.0097 | - | 0.0127 |
| `svd_full/n8/b1024` | 10.1346 | - | 13.2919 |
| `svd_thin/n16/b1` | 0.0348 | - | 0.0393 |
| `svd_thin/n16/b1024` | 36.7679 | - | 40.8869 |
| `svd_thin/n4/b1` | 0.0031 | - | 0.0047 |
| `svd_thin/n4/b1024` | 2.9986 | - | 4.4744 |
| `svd_thin/n8/b1` | 0.0097 | - | 0.0127 |
| `svd_thin/n8/b1024` | 10.1045 | - | 13.3375 |
| `svd_values/n16/b1` | 0.0262 | - | 0.0166 |
| `svd_values/n16/b1024` | 27.4048 | - | 16.9906 |
| `svd_values/n4/b1` | 0.0024 | - | 0.0023 |
| `svd_values/n4/b1024` | 2.2949 | - | 2.1054 |
| `svd_values/n8/b1` | 0.0076 | - | 0.0054 |
| `svd_values/n8/b1024` | 7.7588 | - | 5.4778 |
| `triangular_solve/n16/b1` | 0.0007 | - | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5963 | - | 0.8383 |
| `triangular_solve/n4/b1` | 0.0003 | - | 0.0004 |
| `triangular_solve/n4/b1024` | 0.1022 | - | 0.1780 |
| `triangular_solve/n8/b1` | 0.0004 | - | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2434 | - | 0.3592 |

## small, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0009 | 0.0035 | 0.0011 |
| `cholesky/n16/b1024` | 0.7499 | 0.3832 | 1.0788 |
| `cholesky/n4/b1` | 0.0003 | 0.0027 | 0.0002 |
| `cholesky/n4/b1024` | 0.1177 | 0.0368 | 0.1065 |
| `cholesky/n8/b1` | 0.0004 | 0.0027 | 0.0004 |
| `cholesky/n8/b1024` | 0.2728 | 0.0678 | 0.2832 |
| `eig/n16/b1` | 0.0713 | 0.0754 | 0.0948 |
| `eig/n16/b1024` | 76.3835 | 19.7335 | 102.0448 |
| `eig/n4/b1` | 0.0058 | 0.0088 | 0.0077 |
| `eig/n4/b1024` | 5.7617 | 2.9886 | 7.4437 |
| `eig/n8/b1` | 0.0198 | 0.0227 | 0.0249 |
| `eig/n8/b1024` | 20.3726 | 8.1527 | 25.9840 |
| `eigh/n16/b1` | 0.0180 | 0.0210 | 0.0186 |
| `eigh/n16/b1024` | 19.4018 | 7.7300 | 19.4819 |
| `eigh/n4/b1` | 0.0020 | 0.0043 | 0.0019 |
| `eigh/n4/b1024` | 1.7481 | 0.5774 | 1.6999 |
| `eigh/n8/b1` | 0.0057 | 0.0092 | 0.0054 |
| `eigh/n8/b1024` | 5.4578 | 1.9524 | 5.3654 |
| `eigvals/n16/b1` | 0.0434 | 0.0467 | 0.0682 |
| `eigvals/n16/b1024` | 46.4403 | 12.1367 | 75.0238 |
| `eigvals/n4/b1` | 0.0031 | 0.0062 | 0.0061 |
| `eigvals/n4/b1024` | 2.8124 | 1.4348 | 5.7418 |
| `eigvals/n8/b1` | 0.0118 | 0.0148 | 0.0196 |
| `eigvals/n8/b1024` | 11.7870 | 3.6478 | 20.6110 |
| `eigvalsh/n16/b1` | 0.0136 | 0.0161 | 0.0110 |
| `eigvalsh/n16/b1024` | 14.3479 | 3.5962 | 11.0669 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0038 | 0.0014 |
| `eigvalsh/n4/b1024` | 1.4342 | 0.7274 | 1.0744 |
| `eigvalsh/n8/b1` | 0.0047 | 0.0076 | 0.0036 |
| `eigvalsh/n8/b1024` | 4.3805 | 2.2218 | 3.3378 |
| `full_piv_lu/n16/b1` | 0.0032 | 0.0055 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.8434 | 1.3957 | 3.4707 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0023 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2861 | 0.1485 | 0.3122 |
| `full_piv_lu/n8/b1` | 0.0012 | 0.0029 | 0.0010 |
| `full_piv_lu/n8/b1024` | 0.8392 | 0.4078 | 0.7537 |
| `full_piv_lu_solve/n16/b1` | 0.0037 | 0.0059 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1393 | 0.8133 | 5.1068 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0036 | 0.0012 |
| `full_piv_lu_solve/n4/b1024` | 0.4763 | 0.2412 | 0.9503 |
| `full_piv_lu_solve/n8/b1` | 0.0017 | 0.0039 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1538 | 0.5778 | 1.8910 |
| `householder_apply/n16/b1` | 0.0026 | 0.0052 | 0.0035 |
| `householder_apply/n16/b1024` | 3.1557 | 1.2168 | 3.9802 |
| `householder_apply/n4/b1` | 0.0003 | 0.0026 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1776 | 0.0533 | 0.2558 |
| `householder_apply/n8/b1` | 0.0007 | 0.0023 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6083 | 0.3001 | 0.7576 |
| `householder_factor/n16/b1` | 0.0026 | 0.0047 | 0.0038 |
| `householder_factor/n16/b1024` | 2.5546 | 0.9971 | 3.8200 |
| `householder_factor/n4/b1` | 0.0004 | 0.0020 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3058 | 0.0819 | 0.3084 |
| `householder_factor/n8/b1` | 0.0009 | 0.0032 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8035 | 0.2078 | 0.8939 |
| `lu/n16/b1` | 0.0022 | 0.0039 | 0.0022 |
| `lu/n16/b1024` | 1.8649 | 0.6339 | 2.2263 |
| `lu/n4/b1` | 0.0005 | 0.0021 | 0.0003 |
| `lu/n4/b1024` | 0.2109 | 0.0589 | 0.1704 |
| `lu/n8/b1` | 0.0008 | 0.0026 | 0.0007 |
| `lu/n8/b1024` | 0.5471 | 0.1415 | 0.5328 |
| `lu_factor/n16/b1` | 0.0015 | 0.0038 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2599 | 0.6262 | 1.5953 |
| `lu_factor/n4/b1` | 0.0004 | 0.0021 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1632 | 0.0461 | 0.1105 |
| `lu_factor/n8/b1` | 0.0006 | 0.0030 | 0.0004 |
| `lu_factor/n8/b1024` | 0.3991 | 0.1081 | 0.3693 |
| `lu_factor_solve/n16/b1` | 0.0025 | 0.0051 | 0.0032 |
| `lu_factor_solve/n16/b1024` | 2.0057 | 0.5331 | 3.1816 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0026 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2510 | 0.0693 | 0.2487 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0035 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6854 | 0.1800 | 0.9976 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0034 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7813 | 0.3963 | 1.5650 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0021 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0981 | 0.0350 | 0.1451 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0028 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2878 | 0.0830 | 0.6420 |
| `qr/n16/b1` | 0.0068 | 0.0093 | 0.0064 |
| `qr/n16/b1024` | 6.5507 | 3.2791 | 6.4679 |
| `qr/n4/b1` | 0.0007 | 0.0025 | 0.0009 |
| `qr/n4/b1024` | 0.5086 | 0.1318 | 0.5871 |
| `qr/n8/b1` | 0.0017 | 0.0044 | 0.0018 |
| `qr/n8/b1024` | 1.5372 | 0.7967 | 1.5920 |
| `rank_revealing_qr/n16/b1` | 0.0075 | 0.0103 | 0.0093 |
| `rank_revealing_qr/n16/b1024` | 7.2781 | 3.6817 | 9.5463 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0033 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8530 | 0.2143 | 1.0767 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0049 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1949 | 0.5537 | 2.8750 |
| `solve/n16/b1` | 0.0028 | 0.0057 | 0.0036 |
| `solve/n16/b1024` | 2.1200 | 0.5686 | 3.3350 |
| `solve/n4/b1` | 0.0007 | 0.0024 | 0.0005 |
| `solve/n4/b1024` | 0.3135 | 0.1607 | 0.2873 |
| `solve/n8/b1` | 0.0012 | 0.0035 | 0.0012 |
| `solve/n8/b1024` | 0.7790 | 0.2393 | 1.0472 |
| `svd_full/n16/b1` | 0.0348 | 0.0379 | 0.0392 |
| `svd_full/n16/b1024` | 36.5512 | 10.7154 | 40.6492 |
| `svd_full/n4/b1` | 0.0031 | 0.0056 | 0.0047 |
| `svd_full/n4/b1024` | 2.9981 | 0.7624 | 4.4217 |
| `svd_full/n8/b1` | 0.0099 | 0.0125 | 0.0126 |
| `svd_full/n8/b1024` | 10.0450 | 2.9674 | 13.2383 |
| `svd_thin/n16/b1` | 0.0349 | 0.0377 | 0.0391 |
| `svd_thin/n16/b1024` | 36.5411 | 15.6165 | 40.6801 |
| `svd_thin/n4/b1` | 0.0031 | 0.0053 | 0.0047 |
| `svd_thin/n4/b1024` | 3.0145 | 1.1291 | 4.4193 |
| `svd_thin/n8/b1` | 0.0098 | 0.0125 | 0.0127 |
| `svd_thin/n8/b1024` | 10.0804 | 5.0871 | 13.2747 |
| `svd_values/n16/b1` | 0.0262 | 0.0561 | 0.0164 |
| `svd_values/n16/b1024` | 27.4469 | 7.3754 | 16.9476 |
| `svd_values/n4/b1` | 0.0026 | 0.0043 | 0.0023 |
| `svd_values/n4/b1024` | 2.2932 | 0.5784 | 2.1157 |
| `svd_values/n8/b1` | 0.0076 | 0.0105 | 0.0054 |
| `svd_values/n8/b1024` | 7.7587 | 1.9542 | 5.4928 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0027 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5909 | 0.1519 | 0.8514 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0028 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0955 | 0.0293 | 0.1819 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0027 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2393 | 0.0647 | 0.3525 |

## small, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n16/b1` | 0.0008 | 0.0041 | 0.0011 |
| `cholesky/n16/b1024` | 0.7578 | 0.2008 | 1.1427 |
| `cholesky/n4/b1` | 0.0002 | 0.0031 | 0.0002 |
| `cholesky/n4/b1024` | 0.1171 | 0.0230 | 0.1066 |
| `cholesky/n8/b1` | 0.0004 | 0.0026 | 0.0004 |
| `cholesky/n8/b1024` | 0.2460 | 0.0402 | 0.2809 |
| `eig/n16/b1` | 0.0721 | 0.0765 | 0.0979 |
| `eig/n16/b1024` | 80.1419 | 9.6712 | 105.6628 |
| `eig/n4/b1` | 0.0061 | 0.0089 | 0.0077 |
| `eig/n4/b1024` | 5.9030 | 0.7550 | 7.4876 |
| `eig/n8/b1` | 0.0204 | 0.0227 | 0.0249 |
| `eig/n8/b1024` | 20.9278 | 2.6253 | 25.9360 |
| `eigh/n16/b1` | 0.0181 | 0.0211 | 0.0186 |
| `eigh/n16/b1024` | 19.5303 | 4.8779 | 19.3874 |
| `eigh/n4/b1` | 0.0020 | 0.0047 | 0.0020 |
| `eigh/n4/b1024` | 1.7625 | 0.4447 | 1.6983 |
| `eigh/n8/b1` | 0.0057 | 0.0089 | 0.0054 |
| `eigh/n8/b1024` | 5.4813 | 0.7281 | 5.3641 |
| `eigvals/n16/b1` | 0.0434 | 0.0466 | 0.0680 |
| `eigvals/n16/b1024` | 46.5030 | 9.0010 | 75.1042 |
| `eigvals/n4/b1` | 0.0033 | 0.0060 | 0.0061 |
| `eigvals/n4/b1024` | 2.9897 | 0.7080 | 5.7613 |
| `eigvals/n8/b1` | 0.0118 | 0.0142 | 0.0196 |
| `eigvals/n8/b1024` | 11.8892 | 2.9892 | 20.5927 |
| `eigvalsh/n16/b1` | 0.0137 | 0.0165 | 0.0109 |
| `eigvalsh/n16/b1024` | 14.2212 | 3.4587 | 11.0068 |
| `eigvalsh/n4/b1` | 0.0016 | 0.0048 | 0.0014 |
| `eigvalsh/n4/b1024` | 1.4327 | 0.3664 | 1.0876 |
| `eigvalsh/n8/b1` | 0.0046 | 0.0072 | 0.0036 |
| `eigvalsh/n8/b1024` | 4.3870 | 0.5609 | 3.3497 |
| `full_piv_lu/n16/b1` | 0.0031 | 0.0063 | 0.0028 |
| `full_piv_lu/n16/b1024` | 2.8640 | 0.4363 | 3.5033 |
| `full_piv_lu/n4/b1` | 0.0007 | 0.0040 | 0.0005 |
| `full_piv_lu/n4/b1024` | 0.2891 | 0.0801 | 0.3092 |
| `full_piv_lu/n8/b1` | 0.0012 | 0.0046 | 0.0009 |
| `full_piv_lu/n8/b1024` | 0.8406 | 0.1269 | 0.7594 |
| `full_piv_lu_solve/n16/b1` | 0.0038 | 0.0060 | 0.0053 |
| `full_piv_lu_solve/n16/b1024` | 3.1250 | 0.7785 | 5.1408 |
| `full_piv_lu_solve/n4/b1` | 0.0009 | 0.0033 | 0.0013 |
| `full_piv_lu_solve/n4/b1024` | 0.4839 | 0.0712 | 0.9456 |
| `full_piv_lu_solve/n8/b1` | 0.0017 | 0.0046 | 0.0022 |
| `full_piv_lu_solve/n8/b1024` | 1.1448 | 0.2969 | 1.9077 |
| `householder_apply/n16/b1` | 0.0026 | 0.0054 | 0.0036 |
| `householder_apply/n16/b1024` | 3.2754 | 0.6811 | 4.2592 |
| `householder_apply/n4/b1` | 0.0003 | 0.0021 | 0.0005 |
| `householder_apply/n4/b1024` | 0.1782 | 0.0493 | 0.2545 |
| `householder_apply/n8/b1` | 0.0007 | 0.0025 | 0.0010 |
| `householder_apply/n8/b1024` | 0.6021 | 0.1248 | 0.7850 |
| `householder_factor/n16/b1` | 0.0025 | 0.0057 | 0.0037 |
| `householder_factor/n16/b1024` | 2.5666 | 0.6437 | 3.7810 |
| `householder_factor/n4/b1` | 0.0004 | 0.0038 | 0.0005 |
| `householder_factor/n4/b1024` | 0.3074 | 0.0502 | 0.3076 |
| `householder_factor/n8/b1` | 0.0009 | 0.0045 | 0.0010 |
| `householder_factor/n8/b1024` | 0.8059 | 0.2100 | 0.8880 |
| `lu/n16/b1` | 0.0022 | 0.0053 | 0.0021 |
| `lu/n16/b1024` | 1.8554 | 0.3032 | 2.3138 |
| `lu/n4/b1` | 0.0005 | 0.0037 | 0.0003 |
| `lu/n4/b1024` | 0.2112 | 0.0355 | 0.1734 |
| `lu/n8/b1` | 0.0008 | 0.0041 | 0.0007 |
| `lu/n8/b1024` | 0.5756 | 0.1458 | 0.5298 |
| `lu_factor/n16/b1` | 0.0014 | 0.0053 | 0.0016 |
| `lu_factor/n16/b1024` | 1.2330 | 0.3177 | 1.5868 |
| `lu_factor/n4/b1` | 0.0004 | 0.0039 | 0.0002 |
| `lu_factor/n4/b1024` | 0.1631 | 0.0292 | 0.1101 |
| `lu_factor/n8/b1` | 0.0006 | 0.0030 | 0.0004 |
| `lu_factor/n8/b1024` | 0.4020 | 0.1081 | 0.3690 |
| `lu_factor_solve/n16/b1` | 0.0023 | 0.0057 | 0.0031 |
| `lu_factor_solve/n16/b1024` | 2.0299 | 0.5110 | 3.1796 |
| `lu_factor_solve/n4/b1` | 0.0005 | 0.0030 | 0.0003 |
| `lu_factor_solve/n4/b1024` | 0.2519 | 0.0692 | 0.2510 |
| `lu_factor_solve/n8/b1` | 0.0010 | 0.0038 | 0.0010 |
| `lu_factor_solve/n8/b1024` | 0.6770 | 0.0939 | 0.9984 |
| `lu_solve_prepared/n16/b1` | 0.0009 | 0.0039 | 0.0016 |
| `lu_solve_prepared/n16/b1024` | 0.7850 | 0.2089 | 1.5683 |
| `lu_solve_prepared/n4/b1` | 0.0002 | 0.0025 | 0.0002 |
| `lu_solve_prepared/n4/b1024` | 0.0973 | 0.0342 | 0.1439 |
| `lu_solve_prepared/n8/b1` | 0.0004 | 0.0039 | 0.0007 |
| `lu_solve_prepared/n8/b1024` | 0.2890 | 0.0854 | 0.6390 |
| `qr/n16/b1` | 0.0066 | 0.0091 | 0.0063 |
| `qr/n16/b1024` | 6.4946 | 0.8497 | 6.3377 |
| `qr/n4/b1` | 0.0007 | 0.0029 | 0.0009 |
| `qr/n4/b1024` | 0.5118 | 0.1321 | 0.5719 |
| `qr/n8/b1` | 0.0017 | 0.0052 | 0.0019 |
| `qr/n8/b1024` | 1.5491 | 0.3894 | 1.5918 |
| `rank_revealing_qr/n16/b1` | 0.0076 | 0.0184 | 0.0093 |
| `rank_revealing_qr/n16/b1024` | 7.2625 | 1.8224 | 9.5689 |
| `rank_revealing_qr/n4/b1` | 0.0011 | 0.0037 | 0.0015 |
| `rank_revealing_qr/n4/b1024` | 0.8353 | 0.2172 | 1.0791 |
| `rank_revealing_qr/n8/b1` | 0.0025 | 0.0054 | 0.0032 |
| `rank_revealing_qr/n8/b1024` | 2.1686 | 0.2806 | 2.8751 |
| `solve/n16/b1` | 0.0027 | 0.0053 | 0.0036 |
| `solve/n16/b1024` | 2.1586 | 0.2887 | 3.3362 |
| `solve/n4/b1` | 0.0008 | 0.0039 | 0.0005 |
| `solve/n4/b1024` | 0.3220 | 0.0836 | 0.2871 |
| `solve/n8/b1` | 0.0012 | 0.0041 | 0.0012 |
| `solve/n8/b1024` | 0.7996 | 0.1980 | 1.0754 |
| `svd_full/n16/b1` | 0.0367 | 0.0376 | 0.0393 |
| `svd_full/n16/b1024` | 38.5340 | 5.1261 | 40.8341 |
| `svd_full/n4/b1` | 0.0031 | 0.0060 | 0.0047 |
| `svd_full/n4/b1024` | 3.0716 | 0.3781 | 4.4204 |
| `svd_full/n8/b1` | 0.0097 | 0.0124 | 0.0126 |
| `svd_full/n8/b1024` | 10.1262 | 2.5469 | 13.2410 |
| `svd_thin/n16/b1` | 0.0367 | 0.0378 | 0.0391 |
| `svd_thin/n16/b1024` | 38.5737 | 7.4245 | 40.6939 |
| `svd_thin/n4/b1` | 0.0032 | 0.0062 | 0.0047 |
| `svd_thin/n4/b1024` | 3.0746 | 0.3875 | 4.4272 |
| `svd_thin/n8/b1` | 0.0097 | 0.0124 | 0.0126 |
| `svd_thin/n8/b1024` | 10.1879 | 1.4771 | 13.2448 |
| `svd_values/n16/b1` | 0.0262 | 0.0290 | 0.0164 |
| `svd_values/n16/b1024` | 27.3242 | 6.3185 | 16.9158 |
| `svd_values/n4/b1` | 0.0024 | 0.0056 | 0.0023 |
| `svd_values/n4/b1024` | 2.2910 | 0.2946 | 2.1000 |
| `svd_values/n8/b1` | 0.0077 | 0.0102 | 0.0054 |
| `svd_values/n8/b1024` | 7.7702 | 1.3968 | 5.4606 |
| `triangular_solve/n16/b1` | 0.0007 | 0.0038 | 0.0009 |
| `triangular_solve/n16/b1024` | 0.5959 | 0.1526 | 0.8676 |
| `triangular_solve/n4/b1` | 0.0003 | 0.0025 | 0.0004 |
| `triangular_solve/n4/b1024` | 0.0942 | 0.0281 | 0.1804 |
| `triangular_solve/n8/b1` | 0.0004 | 0.0027 | 0.0005 |
| `triangular_solve/n8/b1024` | 0.2371 | 0.0417 | 0.3490 |

## medium, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0377 | - | 0.0557 |
| `cholesky/n128/b128` | 5.6682 | - | 8.1564 |
| `cholesky/n32/b1` | 0.0020 | - | 0.0022 |
| `cholesky/n32/b128` | 0.2400 | - | 0.2718 |
| `eigh/n128/b1` | 1.2658 | - | 1.0803 |
| `eigh/n128/b128` | 164.0971 | - | 145.6663 |
| `eigh/n32/b1` | 0.0643 | - | 0.0557 |
| `eigh/n32/b128` | 8.7809 | - | 7.0912 |
| `eigvalsh/n128/b1` | 0.6954 | - | 0.4554 |
| `eigvalsh/n128/b128` | 91.7610 | - | 59.0008 |
| `eigvalsh/n32/b1` | 0.0489 | - | 0.0249 |
| `eigvalsh/n32/b128` | 6.5328 | - | 3.2251 |
| `householder_apply/n128/b1` | 0.2993 | - | 0.3256 |
| `householder_apply/n128/b128` | 42.8056 | - | 42.8946 |
| `householder_apply/n32/b1` | 0.0106 | - | 0.0074 |
| `householder_apply/n32/b128` | 1.3437 | - | 0.9091 |
| `householder_factor/n128/b1` | 0.1955 | - | 0.1968 |
| `householder_factor/n128/b128` | 25.5960 | - | 25.8013 |
| `householder_factor/n32/b1` | 0.0072 | - | 0.0068 |
| `householder_factor/n32/b128` | 0.9175 | - | 0.9059 |
| `lu/n128/b1` | 0.0883 | - | 0.0825 |
| `lu/n128/b128` | 12.1632 | - | 12.9323 |
| `lu/n32/b1` | 0.0054 | - | 0.0062 |
| `lu/n32/b128` | 0.6178 | - | 0.7739 |
| `lu_factor/n128/b1` | 0.0567 | - | 0.0727 |
| `lu_factor/n128/b128` | 8.3126 | - | 10.0466 |
| `lu_factor/n32/b1` | 0.0032 | - | 0.0051 |
| `lu_factor/n32/b128` | 0.3975 | - | 0.6553 |
| `lu_factor_solve/n128/b1` | 0.0626 | - | 0.0848 |
| `lu_factor_solve/n128/b128` | 8.9135 | - | 11.4935 |
| `lu_factor_solve/n32/b1` | 0.0041 | - | 0.0066 |
| `lu_factor_solve/n32/b128` | 0.4818 | - | 0.8440 |
| `lu_solve_prepared/n128/b1` | 0.0059 | - | 0.0121 |
| `lu_solve_prepared/n128/b128` | 1.6290 | - | 2.3990 |
| `lu_solve_prepared/n32/b1` | 0.0010 | - | 0.0014 |
| `lu_solve_prepared/n32/b128` | 0.1147 | - | 0.1688 |
| `qr/n128/b1` | 0.3442 | - | 0.3950 |
| `qr/n128/b128` | 43.8573 | - | 52.1597 |
| `qr/n32/b1` | 0.0206 | - | 0.0122 |
| `qr/n32/b128` | 2.5902 | - | 1.5535 |
| `rank_revealing_qr/n128/b1` | 0.3524 | - | 0.4780 |
| `rank_revealing_qr/n128/b128` | 44.4846 | - | 63.0405 |
| `rank_revealing_qr/n32/b1` | 0.0205 | - | 0.0181 |
| `rank_revealing_qr/n32/b128` | 2.5948 | - | 2.2927 |
| `solve/n128/b1` | 0.0663 | - | 0.0878 |
| `solve/n128/b128` | 8.7861 | - | 12.0335 |
| `solve/n32/b1` | 0.0048 | - | 0.0070 |
| `solve/n32/b128` | 0.5207 | - | 0.8833 |
| `svd_thin/n128/b1` | 2.4180 | - | 2.0330 |
| `svd_thin/n128/b128` | 308.6324 | - | 264.0710 |
| `svd_thin/n32/b1` | 0.1174 | - | 0.1069 |
| `svd_thin/n32/b128` | 15.1816 | - | 13.8246 |
| `svd_values/n128/b1` | 1.4173 | - | 0.7015 |
| `svd_values/n128/b128` | 180.5148 | - | 92.5982 |
| `svd_values/n32/b1` | 0.0928 | - | 0.0374 |
| `svd_values/n32/b128` | 11.9843 | - | 4.8772 |
| `triangular_solve/n128/b1` | 0.0040 | - | 0.0071 |
| `triangular_solve/n128/b128` | 0.9936 | - | 1.3226 |
| `triangular_solve/n32/b1` | 0.0008 | - | 0.0008 |
| `triangular_solve/n32/b128` | 0.0901 | - | 0.0878 |

## medium, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0376 | 0.0477 | 0.0549 |
| `cholesky/n128/b128` | 5.7442 | 6.7323 | 8.3969 |
| `cholesky/n32/b1` | 0.0019 | 0.0036 | 0.0022 |
| `cholesky/n32/b128` | 0.2381 | 0.0630 | 0.2657 |
| `eigh/n128/b1` | 1.2711 | 1.2867 | 0.6212 |
| `eigh/n128/b128` | 164.0910 | 165.4116 | 84.4128 |
| `eigh/n32/b1` | 0.0643 | 0.0686 | 0.0587 |
| `eigh/n32/b128` | 8.5666 | 2.2060 | 7.4941 |
| `eigvalsh/n128/b1` | 0.6945 | 0.7027 | 0.4343 |
| `eigvalsh/n128/b128` | 90.2578 | 90.7907 | 56.7143 |
| `eigvalsh/n32/b1` | 0.0490 | 0.0529 | 0.0248 |
| `eigvalsh/n32/b128` | 6.4291 | 1.6277 | 3.2351 |
| `householder_apply/n128/b1` | 0.3124 | 0.3229 | 0.0854 |
| `householder_apply/n128/b128` | 43.0800 | 44.2711 | 11.5885 |
| `householder_apply/n32/b1` | 0.0106 | 0.0139 | 0.0075 |
| `householder_apply/n32/b128` | 1.3345 | 0.3401 | 0.9230 |
| `householder_factor/n128/b1` | 0.1957 | 0.2011 | 0.1139 |
| `householder_factor/n128/b128` | 25.4940 | 25.9333 | 15.0230 |
| `householder_factor/n32/b1` | 0.0071 | 0.0099 | 0.0068 |
| `householder_factor/n32/b128` | 0.9080 | 0.4596 | 0.8890 |
| `lu/n128/b1` | 0.0895 | 0.1043 | 0.0817 |
| `lu/n128/b128` | 12.2556 | 13.9952 | 12.9339 |
| `lu/n32/b1` | 0.0054 | 0.0086 | 0.0062 |
| `lu/n32/b128` | 0.6134 | 0.1605 | 0.7781 |
| `lu_factor/n128/b1` | 0.0570 | 0.0728 | 0.0729 |
| `lu_factor/n128/b128` | 8.3216 | 4.0014 | 10.0356 |
| `lu_factor/n32/b1` | 0.0033 | 0.0050 | 0.0051 |
| `lu_factor/n32/b128` | 0.4032 | 0.1113 | 0.6517 |
| `lu_factor_solve/n128/b1` | 0.0640 | 0.0803 | 0.0868 |
| `lu_factor_solve/n128/b128` | 8.9046 | 2.6333 | 11.7845 |
| `lu_factor_solve/n32/b1` | 0.0041 | 0.0074 | 0.0076 |
| `lu_factor_solve/n32/b128` | 0.4889 | 0.2573 | 1.0145 |
| `lu_solve_prepared/n128/b1` | 0.0060 | 0.0095 | 0.0095 |
| `lu_solve_prepared/n128/b128` | 1.8552 | 0.5086 | 2.2401 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0035 | 0.0023 |
| `lu_solve_prepared/n32/b128` | 0.1137 | 0.0347 | 0.3297 |
| `qr/n128/b1` | 0.3408 | 0.6084 | 0.3038 |
| `qr/n128/b128` | 44.2909 | 80.4990 | 40.0828 |
| `qr/n32/b1` | 0.0208 | 0.0423 | 0.0120 |
| `qr/n32/b128` | 2.5889 | 0.6587 | 1.5421 |
| `rank_revealing_qr/n128/b1` | 0.3484 | 0.3637 | 0.4648 |
| `rank_revealing_qr/n128/b128` | 44.7460 | 47.4356 | 60.9034 |
| `rank_revealing_qr/n32/b1` | 0.0207 | 0.0436 | 0.0181 |
| `rank_revealing_qr/n32/b128` | 2.5826 | 0.6776 | 2.2669 |
| `solve/n128/b1` | 0.0675 | 0.0794 | 0.0898 |
| `solve/n128/b128` | 8.8085 | 10.5178 | 12.1285 |
| `solve/n32/b1` | 0.0048 | 0.0081 | 0.0080 |
| `solve/n32/b128` | 0.5244 | 0.1361 | 1.0264 |
| `svd_thin/n128/b1` | 2.4088 | 1.8118 | 1.6124 |
| `svd_thin/n128/b128` | 306.6814 | 230.7616 | 211.3914 |
| `svd_thin/n32/b1` | 0.1164 | 0.1213 | 0.1119 |
| `svd_thin/n32/b128` | 15.0682 | 4.6213 | 14.4872 |
| `svd_values/n128/b1` | 1.4073 | 1.4319 | 0.6789 |
| `svd_values/n128/b128` | 180.6360 | 180.2341 | 90.1580 |
| `svd_values/n32/b1` | 0.0924 | 0.0967 | 0.0374 |
| `svd_values/n32/b128` | 11.9439 | 5.9992 | 4.8544 |
| `triangular_solve/n128/b1` | 0.0040 | 0.0064 | 0.0062 |
| `triangular_solve/n128/b128` | 1.0087 | 1.0885 | 1.3720 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0025 | 0.0012 |
| `triangular_solve/n32/b128` | 0.0877 | 0.0269 | 0.1828 |

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.0373 | 0.0528 | 0.0569 |
| `cholesky/n128/b128` | 5.5885 | 6.5811 | 8.1767 |
| `cholesky/n32/b1` | 0.0019 | 0.0046 | 0.0022 |
| `cholesky/n32/b128` | 0.2338 | 0.0586 | 0.2646 |
| `eigh/n128/b1` | 1.2671 | 1.2444 | 0.5837 |
| `eigh/n128/b128` | 164.9909 | 161.9705 | 79.6325 |
| `eigh/n32/b1` | 0.0646 | 0.0700 | 0.0589 |
| `eigh/n32/b128` | 8.4064 | 1.8010 | 7.5520 |
| `eigvalsh/n128/b1` | 0.6954 | 0.7052 | 0.4493 |
| `eigvalsh/n128/b128` | 90.1788 | 90.4966 | 58.0682 |
| `eigvalsh/n32/b1` | 0.0488 | 0.0518 | 0.0248 |
| `eigvalsh/n32/b128` | 6.4422 | 0.8212 | 3.2337 |
| `householder_apply/n128/b1` | 0.3107 | 0.3181 | 0.0589 |
| `householder_apply/n128/b128` | 40.9074 | 43.8155 | 7.3091 |
| `householder_apply/n32/b1` | 0.0105 | 0.0137 | 0.0076 |
| `householder_apply/n32/b128` | 1.3307 | 0.3350 | 0.9278 |
| `householder_factor/n128/b1` | 0.1965 | 0.2020 | 0.0855 |
| `householder_factor/n128/b128` | 25.3956 | 25.5935 | 11.5631 |
| `householder_factor/n32/b1` | 0.0073 | 0.0097 | 0.0069 |
| `householder_factor/n32/b128` | 0.9040 | 0.2341 | 0.8817 |
| `lu/n128/b1` | 0.0891 | 0.1166 | 0.0818 |
| `lu/n128/b128` | 12.2468 | 15.8859 | 13.0440 |
| `lu/n32/b1` | 0.0054 | 0.0080 | 0.0062 |
| `lu/n32/b128` | 0.5885 | 0.0815 | 0.7708 |
| `lu_factor/n128/b1` | 0.0556 | 0.0808 | 0.0725 |
| `lu_factor/n128/b128` | 8.3750 | 2.6183 | 10.0337 |
| `lu_factor/n32/b1` | 0.0032 | 0.0056 | 0.0052 |
| `lu_factor/n32/b128` | 0.4000 | 0.1093 | 0.6522 |
| `lu_factor_solve/n128/b1` | 0.0623 | 0.0895 | 0.0866 |
| `lu_factor_solve/n128/b128` | 8.9457 | 1.8943 | 11.7746 |
| `lu_factor_solve/n32/b1` | 0.0042 | 0.0075 | 0.0077 |
| `lu_factor_solve/n32/b128` | 0.4813 | 0.1312 | 1.0257 |
| `lu_solve_prepared/n128/b1` | 0.0058 | 0.0091 | 0.0102 |
| `lu_solve_prepared/n128/b128` | 1.7917 | 0.3614 | 2.2751 |
| `lu_solve_prepared/n32/b1` | 0.0010 | 0.0045 | 0.0023 |
| `lu_solve_prepared/n32/b128` | 0.1123 | 0.0283 | 0.3366 |
| `qr/n128/b1` | 0.3435 | 0.9140 | 0.2363 |
| `qr/n128/b128` | 43.7256 | 121.4404 | 37.5257 |
| `qr/n32/b1` | 0.0207 | 0.0656 | 0.0120 |
| `qr/n32/b128` | 2.5715 | 0.6510 | 1.5662 |
| `rank_revealing_qr/n128/b1` | 0.3514 | 0.4224 | 0.4281 |
| `rank_revealing_qr/n128/b128` | 44.8097 | 55.8956 | 63.5263 |
| `rank_revealing_qr/n32/b1` | 0.0208 | 0.0669 | 0.0180 |
| `rank_revealing_qr/n32/b128` | 2.6228 | 0.3239 | 2.2710 |
| `solve/n128/b1` | 0.0678 | 0.0925 | 0.0907 |
| `solve/n128/b128` | 8.8849 | 12.1727 | 12.1192 |
| `solve/n32/b1` | 0.0049 | 0.0077 | 0.0084 |
| `solve/n32/b128` | 0.5470 | 0.1383 | 1.0414 |
| `svd_thin/n128/b1` | 2.4107 | 1.8767 | 1.5364 |
| `svd_thin/n128/b128` | 307.6031 | 239.2054 | 200.1395 |
| `svd_thin/n32/b1` | 0.1168 | 0.1212 | 0.1129 |
| `svd_thin/n32/b128` | 15.2690 | 1.9279 | 14.5928 |
| `svd_values/n128/b1` | 1.4028 | 1.4293 | 0.6807 |
| `svd_values/n128/b128` | 180.4161 | 180.0772 | 89.9424 |
| `svd_values/n32/b1` | 0.0925 | 0.0967 | 0.0373 |
| `svd_values/n32/b128` | 11.9376 | 3.0219 | 4.8405 |
| `triangular_solve/n128/b1` | 0.0039 | 0.0065 | 0.0060 |
| `triangular_solve/n128/b128` | 1.1007 | 1.1765 | 1.3765 |
| `triangular_solve/n32/b1` | 0.0008 | 0.0035 | 0.0013 |
| `triangular_solve/n32/b128` | 0.0903 | 0.0258 | 0.1840 |

## medium, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1094 | - | 0.2461 |
| `cholesky/n128/b128` | 16.0332 | - | 33.0602 |
| `cholesky/n32/b1` | 0.0032 | - | 0.0048 |
| `cholesky/n32/b128` | 0.4246 | - | 0.6273 |
| `eigh/n128/b1` | 1.8583 | - | 2.9732 |
| `eigh/n128/b128` | 242.6046 | - | 384.9324 |
| `eigh/n32/b1` | 0.0812 | - | 0.0870 |
| `eigh/n32/b128` | 10.5552 | - | 11.3828 |
| `eigvalsh/n128/b1` | 0.9380 | - | 1.2687 |
| `eigvalsh/n128/b128` | 122.8110 | - | 164.1951 |
| `eigvalsh/n32/b1` | 0.0531 | - | 0.0444 |
| `eigvalsh/n32/b128` | 7.0032 | - | 5.7559 |
| `householder_apply/n128/b1` | 0.6862 | - | 0.9666 |
| `householder_apply/n128/b128` | 92.8314 | - | 127.2357 |
| `householder_apply/n32/b1` | 0.0142 | - | 0.0194 |
| `householder_apply/n32/b128` | 1.9165 | - | 2.6490 |
| `householder_factor/n128/b1` | 0.4548 | - | 0.5417 |
| `householder_factor/n128/b128` | 59.0616 | - | 70.5984 |
| `householder_factor/n32/b1` | 0.0110 | - | 0.0155 |
| `householder_factor/n32/b128` | 1.4128 | - | 2.0101 |
| `lu/n128/b1` | 0.1962 | - | 0.2697 |
| `lu/n128/b128` | 27.6011 | - | 38.6444 |
| `lu/n32/b1` | 0.0078 | - | 0.0106 |
| `lu/n32/b128` | 1.0144 | - | 1.4478 |
| `lu_factor/n128/b1` | 0.1547 | - | 0.2476 |
| `lu_factor/n128/b128` | 21.9168 | - | 32.7333 |
| `lu_factor/n32/b1` | 0.0053 | - | 0.0090 |
| `lu_factor/n32/b128` | 0.6529 | - | 1.1459 |
| `lu_factor_solve/n128/b1` | 0.1749 | - | 0.2808 |
| `lu_factor_solve/n128/b128` | 24.4114 | - | 36.8684 |
| `lu_factor_solve/n32/b1` | 0.0075 | - | 0.0134 |
| `lu_factor_solve/n32/b128` | 0.9410 | - | 1.7144 |
| `lu_solve_prepared/n128/b1` | 0.0188 | - | 0.0307 |
| `lu_solve_prepared/n128/b128` | 4.2840 | - | 5.7811 |
| `lu_solve_prepared/n32/b1` | 0.0023 | - | 0.0044 |
| `lu_solve_prepared/n32/b128` | 0.2859 | - | 0.5582 |
| `qr/n128/b1` | 0.9722 | - | 1.1393 |
| `qr/n128/b128` | 125.4833 | - | 148.8441 |
| `qr/n32/b1` | 0.0421 | - | 0.0285 |
| `qr/n32/b128` | 5.4011 | - | 3.6903 |
| `rank_revealing_qr/n128/b1` | 1.0189 | - | 1.5945 |
| `rank_revealing_qr/n128/b128` | 132.2894 | - | 207.5978 |
| `rank_revealing_qr/n32/b1` | 0.0392 | - | 0.0392 |
| `rank_revealing_qr/n32/b128` | 5.0379 | - | 5.1451 |
| `solve/n128/b1` | 0.1806 | - | 0.2883 |
| `solve/n128/b128` | 23.7952 | - | 37.5573 |
| `solve/n32/b1` | 0.0083 | - | 0.0140 |
| `solve/n32/b128` | 0.9700 | - | 1.7622 |
| `svd_thin/n128/b1` | 3.9685 | - | 4.1877 |
| `svd_thin/n128/b128` | 512.5017 | - | 539.9818 |
| `svd_thin/n32/b1` | 0.1516 | - | 0.1533 |
| `svd_thin/n32/b128` | 19.8702 | - | 20.6485 |
| `svd_values/n128/b1` | 1.9485 | - | 1.5961 |
| `svd_values/n128/b128` | 251.1150 | - | 206.1160 |
| `svd_values/n32/b1` | 0.1017 | - | 0.0607 |
| `svd_values/n32/b128` | 13.4288 | - | 7.9707 |
| `triangular_solve/n128/b1` | 0.0109 | - | 0.0149 |
| `triangular_solve/n128/b128` | 2.3603 | - | 2.8294 |
| `triangular_solve/n32/b1` | 0.0016 | - | 0.0021 |
| `triangular_solve/n32/b128` | 0.1916 | - | 0.2657 |

## medium, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1056 | 0.1065 | 0.2452 |
| `cholesky/n128/b128` | 15.9556 | 15.6671 | 32.9236 |
| `cholesky/n32/b1` | 0.0033 | 0.0050 | 0.0049 |
| `cholesky/n32/b128` | 0.4171 | 0.2127 | 0.6252 |
| `eigh/n128/b1` | 1.8614 | 1.6040 | 1.8154 |
| `eigh/n128/b128` | 242.6609 | 209.6678 | 236.0341 |
| `eigh/n32/b1` | 0.0806 | 0.0862 | 0.0869 |
| `eigh/n32/b128` | 10.5768 | 2.6891 | 11.4582 |
| `eigvalsh/n128/b1` | 0.9306 | 0.9407 | 0.8161 |
| `eigvalsh/n128/b128` | 122.4905 | 122.0359 | 106.4637 |
| `eigvalsh/n32/b1` | 0.0532 | 0.0563 | 0.0442 |
| `eigvalsh/n32/b128` | 7.0163 | 1.7608 | 5.7727 |
| `householder_apply/n128/b1` | 0.6816 | 0.6893 | 0.2905 |
| `householder_apply/n128/b128` | 92.6079 | 93.0964 | 35.8273 |
| `householder_apply/n32/b1` | 0.0143 | 0.0171 | 0.0197 |
| `householder_apply/n32/b128` | 1.9226 | 0.4595 | 2.6095 |
| `householder_factor/n128/b1` | 0.4573 | 0.4600 | 0.2638 |
| `householder_factor/n128/b128` | 59.2726 | 58.9848 | 33.8006 |
| `householder_factor/n32/b1` | 0.0111 | 0.0137 | 0.0155 |
| `householder_factor/n32/b128` | 1.4080 | 0.3578 | 2.0196 |
| `lu/n128/b1` | 0.1949 | 0.1842 | 0.2701 |
| `lu/n128/b128` | 27.6445 | 25.7495 | 38.5135 |
| `lu/n32/b1` | 0.0078 | 0.0106 | 0.0105 |
| `lu/n32/b128` | 1.0091 | 0.4975 | 1.4388 |
| `lu_factor/n128/b1` | 0.1556 | 0.1446 | 0.2477 |
| `lu_factor/n128/b128` | 21.8153 | 6.1796 | 32.6949 |
| `lu_factor/n32/b1` | 0.0053 | 0.0079 | 0.0089 |
| `lu_factor/n32/b128` | 0.6448 | 0.3326 | 1.1356 |
| `lu_factor_solve/n128/b1` | 0.1745 | 0.1629 | 0.2668 |
| `lu_factor_solve/n128/b128` | 24.2764 | 6.5321 | 35.3747 |
| `lu_factor_solve/n32/b1` | 0.0075 | 0.0107 | 0.0118 |
| `lu_factor_solve/n32/b128` | 0.9262 | 0.4679 | 1.5550 |
| `lu_solve_prepared/n128/b1` | 0.0188 | 0.0220 | 0.0151 |
| `lu_solve_prepared/n128/b128` | 4.1597 | 1.2440 | 3.7567 |
| `lu_solve_prepared/n32/b1` | 0.0022 | 0.0052 | 0.0026 |
| `lu_solve_prepared/n32/b128` | 0.2821 | 0.0758 | 0.3701 |
| `qr/n128/b1` | 0.9723 | 0.8675 | 0.5946 |
| `qr/n128/b128` | 124.9912 | 112.3335 | 77.3065 |
| `qr/n32/b1` | 0.0423 | 0.0679 | 0.0283 |
| `qr/n32/b128` | 5.4095 | 1.8302 | 3.6794 |
| `rank_revealing_qr/n128/b1` | 1.0185 | 0.7967 | 1.3762 |
| `rank_revealing_qr/n128/b128` | 130.8640 | 104.0435 | 178.7137 |
| `rank_revealing_qr/n32/b1` | 0.0392 | 0.0668 | 0.0392 |
| `rank_revealing_qr/n32/b128` | 4.9651 | 2.5227 | 5.1525 |
| `solve/n128/b1` | 0.1791 | 0.1688 | 0.2775 |
| `solve/n128/b128` | 23.7200 | 22.2049 | 36.2293 |
| `solve/n32/b1` | 0.0083 | 0.0109 | 0.0126 |
| `solve/n32/b128` | 0.9685 | 0.2478 | 1.6157 |
| `svd_thin/n128/b1` | 3.9645 | 2.7571 | 2.5115 |
| `svd_thin/n128/b128` | 511.8602 | 355.5629 | 325.2083 |
| `svd_thin/n32/b1` | 0.1510 | 0.1563 | 0.1578 |
| `svd_thin/n32/b128` | 19.6668 | 8.4488 | 21.3422 |
| `svd_values/n128/b1` | 1.9315 | 1.9504 | 1.2180 |
| `svd_values/n128/b128` | 249.9277 | 249.3725 | 157.6598 |
| `svd_values/n32/b1` | 0.1017 | 0.1058 | 0.0604 |
| `svd_values/n32/b128` | 13.3913 | 4.1997 | 7.9189 |
| `triangular_solve/n128/b1` | 0.0111 | 0.0141 | 0.0078 |
| `triangular_solve/n128/b128` | 2.2405 | 2.2074 | 2.2794 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0042 | 0.0015 |
| `triangular_solve/n32/b128` | 0.1952 | 0.0981 | 0.1893 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n128/b1` | 0.1086 | 0.1172 | 0.2437 |
| `cholesky/n128/b128` | 15.9322 | 16.3423 | 32.8972 |
| `cholesky/n32/b1` | 0.0034 | 0.0068 | 0.0049 |
| `cholesky/n32/b128` | 0.4111 | 0.0565 | 0.6215 |
| `eigh/n128/b1` | 1.8632 | 1.6348 | 1.6232 |
| `eigh/n128/b128` | 242.2340 | 212.4744 | 211.6416 |
| `eigh/n32/b1` | 0.0814 | 0.0857 | 0.0866 |
| `eigh/n32/b128` | 10.5868 | 1.6200 | 11.3443 |
| `eigvalsh/n128/b1` | 0.9363 | 0.9411 | 0.7405 |
| `eigvalsh/n128/b128` | 122.0665 | 121.9563 | 97.1670 |
| `eigvalsh/n32/b1` | 0.0532 | 0.0569 | 0.0444 |
| `eigvalsh/n32/b128` | 6.9780 | 1.7435 | 5.7999 |
| `householder_apply/n128/b1` | 0.6810 | 0.6916 | 0.1752 |
| `householder_apply/n128/b128` | 92.8358 | 93.0311 | 20.5768 |
| `householder_apply/n32/b1` | 0.0143 | 0.0172 | 0.0194 |
| `householder_apply/n32/b128` | 1.8261 | 0.4533 | 2.5888 |
| `householder_factor/n128/b1` | 0.4528 | 0.4613 | 0.1799 |
| `householder_factor/n128/b128` | 59.2236 | 59.0007 | 23.3235 |
| `householder_factor/n32/b1` | 0.0112 | 0.0138 | 0.0156 |
| `householder_factor/n32/b128` | 1.4144 | 0.3599 | 2.0082 |
| `lu/n128/b1` | 0.1979 | 0.1948 | 0.2698 |
| `lu/n128/b128` | 27.7024 | 27.3648 | 38.5193 |
| `lu/n32/b1` | 0.0078 | 0.0110 | 0.0105 |
| `lu/n32/b128` | 1.0081 | 0.2408 | 1.4360 |
| `lu_factor/n128/b1` | 0.1555 | 0.1553 | 0.2488 |
| `lu_factor/n128/b128` | 21.8962 | 3.3440 | 32.6610 |
| `lu_factor/n32/b1` | 0.0053 | 0.0087 | 0.0089 |
| `lu_factor/n32/b128` | 0.6488 | 0.1717 | 1.1363 |
| `lu_factor_solve/n128/b1` | 0.1745 | 0.1734 | 0.2664 |
| `lu_factor_solve/n128/b128` | 24.3696 | 6.0924 | 35.2284 |
| `lu_factor_solve/n32/b1` | 0.0076 | 0.0106 | 0.0120 |
| `lu_factor_solve/n32/b128` | 0.9340 | 0.2445 | 1.5642 |
| `lu_solve_prepared/n128/b1` | 0.0187 | 0.0217 | 0.0152 |
| `lu_solve_prepared/n128/b128` | 4.2657 | 0.7404 | 3.7492 |
| `lu_solve_prepared/n32/b1` | 0.0022 | 0.0054 | 0.0027 |
| `lu_solve_prepared/n32/b128` | 0.2794 | 0.0764 | 0.3666 |
| `qr/n128/b1` | 0.9750 | 1.1921 | 0.4369 |
| `qr/n128/b128` | 125.4880 | 154.3543 | 57.2414 |
| `qr/n32/b1` | 0.0423 | 0.0892 | 0.0285 |
| `qr/n32/b128` | 5.4204 | 0.6842 | 3.6435 |
| `rank_revealing_qr/n128/b1` | 1.0100 | 0.8681 | 1.2173 |
| `rank_revealing_qr/n128/b128` | 130.9899 | 114.1882 | 158.8682 |
| `rank_revealing_qr/n32/b1` | 0.0391 | 0.0852 | 0.0389 |
| `rank_revealing_qr/n32/b128` | 4.9704 | 1.2146 | 5.1181 |
| `solve/n128/b1` | 0.1794 | 0.1778 | 0.2795 |
| `solve/n128/b128` | 23.8062 | 23.4623 | 36.2272 |
| `solve/n32/b1` | 0.0083 | 0.0105 | 0.0125 |
| `solve/n32/b128` | 0.9717 | 0.2452 | 1.6079 |
| `svd_thin/n128/b1` | 3.9896 | 2.7996 | 2.2062 |
| `svd_thin/n128/b128` | 514.7914 | 363.4988 | 286.4783 |
| `svd_thin/n32/b1` | 0.1516 | 0.1594 | 0.1587 |
| `svd_thin/n32/b128` | 19.7629 | 2.7468 | 21.3559 |
| `svd_values/n128/b1` | 1.9228 | 1.9531 | 1.1670 |
| `svd_values/n128/b128` | 251.1303 | 249.1555 | 150.4637 |
| `svd_values/n32/b1` | 0.1013 | 0.1056 | 0.0605 |
| `svd_values/n32/b128` | 13.3541 | 1.6895 | 7.9627 |
| `triangular_solve/n128/b1` | 0.0109 | 0.0140 | 0.0078 |
| `triangular_solve/n128/b128` | 2.2322 | 2.2326 | 2.2306 |
| `triangular_solve/n32/b1` | 0.0016 | 0.0046 | 0.0015 |
| `triangular_solve/n32/b128` | 0.1928 | 0.0501 | 0.1910 |

## large, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1965 | - | 0.2659 |
| `cholesky/n256/b4` | 0.7934 | - | 1.0699 |
| `cholesky/n512/b1` | 1.2861 | - | 1.9932 |
| `cholesky/n512/b4` | 5.5298 | - | 8.4486 |
| `eigh/n256/b1` | 5.5988 | - | 5.9115 |
| `eigh/n256/b4` | 22.4960 | - | 23.8551 |
| `eigh/n512/b1` | 28.7324 | - | 36.4962 |
| `eigh/n512/b4` | 115.3946 | - | 145.6854 |
| `eigvalsh/n256/b1` | 2.9245 | - | 2.5709 |
| `eigvalsh/n256/b4` | 11.9097 | - | 10.3579 |
| `eigvalsh/n512/b1` | 14.1219 | - | 16.5320 |
| `eigvalsh/n512/b4` | 56.8440 | - | 66.3149 |
| `householder_apply/n256/b1` | 2.2629 | - | 1.9346 |
| `householder_apply/n256/b4` | 9.8539 | - | 7.8393 |
| `householder_apply/n512/b1` | 18.8850 | - | 12.9276 |
| `householder_apply/n512/b4` | 76.1717 | - | 52.5716 |
| `householder_factor/n256/b1` | 1.4684 | - | 1.1208 |
| `householder_factor/n256/b4` | 5.9479 | - | 4.5195 |
| `householder_factor/n512/b1` | 12.0410 | - | 8.0488 |
| `householder_factor/n512/b4` | 48.7046 | - | 32.2286 |
| `lu/n256/b1` | 0.4811 | - | 0.4974 |
| `lu/n256/b4` | 1.9548 | - | 2.1431 |
| `lu/n512/b1` | 3.2283 | - | 3.3324 |
| `lu/n512/b4` | 12.9087 | - | 13.5294 |
| `lu_factor/n256/b1` | 0.3532 | - | 0.4569 |
| `lu_factor/n256/b4` | 1.5319 | - | 1.8375 |
| `lu_factor/n512/b1` | 2.7533 | - | 3.0055 |
| `lu_factor/n512/b4` | 11.7907 | - | 12.3790 |
| `lu_factor_solve/n256/b1` | 0.3687 | - | 0.5002 |
| `lu_factor_solve/n256/b4` | 1.5978 | - | 1.9964 |
| `lu_factor_solve/n512/b1` | 2.8108 | - | 3.1765 |
| `lu_factor_solve/n512/b4` | 11.9799 | - | 13.1538 |
| `lu_solve_prepared/n256/b1` | 0.0169 | - | 0.0397 |
| `lu_solve_prepared/n256/b4` | 0.0802 | - | 0.1743 |
| `lu_solve_prepared/n512/b1` | 0.0710 | - | 0.1658 |
| `lu_solve_prepared/n512/b4` | 0.3679 | - | 0.9751 |
| `qr/n256/b1` | 1.8565 | - | 2.3653 |
| `qr/n256/b4` | 7.4064 | - | 9.5934 |
| `qr/n512/b1` | 11.5198 | - | 17.1114 |
| `qr/n512/b4` | 46.1331 | - | 69.3118 |
| `rank_revealing_qr/n256/b1` | 2.1173 | - | 2.9350 |
| `rank_revealing_qr/n256/b4` | 8.3532 | - | 11.8329 |
| `rank_revealing_qr/n512/b1` | 14.7126 | - | 21.2504 |
| `rank_revealing_qr/n512/b4` | 59.2199 | - | 86.1630 |
| `solve/n256/b1` | 0.3864 | - | 0.5087 |
| `solve/n256/b4` | 1.5362 | - | 2.0484 |
| `solve/n512/b1` | 2.8549 | - | 3.2262 |
| `solve/n512/b4` | 11.3788 | - | 12.9633 |
| `svd_thin/n256/b1` | 12.2479 | - | 10.9213 |
| `svd_thin/n256/b4` | 48.9688 | - | 43.5647 |
| `svd_thin/n512/b1` | 70.4104 | - | 71.3588 |
| `svd_thin/n512/b4` | 283.1505 | - | 292.2452 |
| `svd_values/n256/b1` | 6.9643 | - | 4.1155 |
| `svd_values/n256/b4` | 27.6684 | - | 16.5872 |
| `svd_values/n512/b1` | 38.5898 | - | 28.4026 |
| `svd_values/n512/b4` | 154.6384 | - | 114.8360 |
| `triangular_solve/n256/b1` | 0.0104 | - | 0.0234 |
| `triangular_solve/n256/b4` | 0.0425 | - | 0.1104 |
| `triangular_solve/n512/b1` | 0.0340 | - | 0.0945 |
| `triangular_solve/n512/b4` | 0.1433 | - | 0.4071 |

## large, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1978 | 0.1875 | 0.1647 |
| `cholesky/n256/b4` | 0.7949 | 0.7395 | 0.6637 |
| `cholesky/n512/b1` | 1.3218 | 0.8365 | 0.9038 |
| `cholesky/n512/b4` | 5.6443 | 3.6233 | 3.9857 |
| `eigh/n256/b1` | 5.6296 | 4.2281 | 2.7939 |
| `eigh/n256/b4` | 22.5684 | 17.2017 | 11.3172 |
| `eigh/n512/b1` | 28.8243 | 15.9606 | 13.2474 |
| `eigh/n512/b4` | 116.0876 | 64.0074 | 52.8186 |
| `eigvalsh/n256/b1` | 2.9589 | 2.9675 | 1.8773 |
| `eigvalsh/n256/b4` | 11.9888 | 11.9396 | 7.4948 |
| `eigvalsh/n512/b1` | 14.5887 | 11.6596 | 8.9645 |
| `eigvalsh/n512/b4` | 57.7837 | 47.9749 | 36.0763 |
| `householder_apply/n256/b1` | 2.3759 | 2.4028 | 0.5718 |
| `householder_apply/n256/b4` | 9.7569 | 9.7849 | 2.2943 |
| `householder_apply/n512/b1` | 18.9211 | 18.8920 | 3.5214 |
| `householder_apply/n512/b4` | 83.5252 | 83.3502 | 14.2281 |
| `householder_factor/n256/b1` | 1.4760 | 1.5136 | 0.3666 |
| `householder_factor/n256/b4` | 5.9003 | 5.9193 | 1.4521 |
| `householder_factor/n512/b1` | 12.0798 | 12.0659 | 2.1864 |
| `householder_factor/n512/b4` | 48.7311 | 48.6123 | 8.8357 |
| `lu/n256/b1` | 0.4727 | 0.4385 | 0.2020 |
| `lu/n256/b4` | 1.9630 | 1.8295 | 0.9002 |
| `lu/n512/b1` | 3.2519 | 1.9788 | 1.1454 |
| `lu/n512/b4` | 12.9834 | 7.8547 | 4.8591 |
| `lu_factor/n256/b1` | 0.3798 | 0.3248 | 0.1616 |
| `lu_factor/n256/b4` | 1.5235 | 0.7779 | 0.6500 |
| `lu_factor/n512/b1` | 2.8481 | 1.4638 | 0.8492 |
| `lu_factor/n512/b4` | 11.7289 | 6.5168 | 3.4822 |
| `lu_factor_solve/n256/b1` | 0.3720 | 0.3320 | 0.1925 |
| `lu_factor_solve/n256/b4` | 1.4802 | 0.3829 | 0.7609 |
| `lu_factor_solve/n512/b1` | 2.9042 | 1.5334 | 0.9586 |
| `lu_factor_solve/n512/b4` | 12.0643 | 3.7106 | 3.9256 |
| `lu_solve_prepared/n256/b1` | 0.0172 | 0.0237 | 0.0246 |
| `lu_solve_prepared/n256/b4` | 0.0757 | 0.0227 | 0.1249 |
| `lu_solve_prepared/n512/b1` | 0.0618 | 0.0642 | 0.0974 |
| `lu_solve_prepared/n512/b4` | 0.4361 | 0.1705 | 0.5660 |
| `qr/n256/b1` | 1.8521 | 1.7460 | 1.1451 |
| `qr/n256/b4` | 7.4193 | 7.3571 | 4.6827 |
| `qr/n512/b1` | 11.5326 | 6.2049 | 6.8693 |
| `qr/n512/b4` | 46.0784 | 24.5556 | 28.0473 |
| `rank_revealing_qr/n256/b1` | 2.0885 | 1.4885 | 2.2764 |
| `rank_revealing_qr/n256/b4` | 8.4842 | 5.9184 | 9.1916 |
| `rank_revealing_qr/n512/b1` | 14.7117 | 6.2236 | 15.7931 |
| `rank_revealing_qr/n512/b4` | 58.8227 | 24.8966 | 63.8941 |
| `solve/n256/b1` | 0.3862 | 0.3557 | 0.2095 |
| `solve/n256/b4` | 1.5396 | 1.4035 | 0.8439 |
| `solve/n512/b1` | 2.8907 | 1.5668 | 1.0045 |
| `solve/n512/b4` | 11.4104 | 6.2488 | 4.1201 |
| `svd_thin/n256/b1` | 12.2140 | 8.8033 | 7.6812 |
| `svd_thin/n256/b4` | 48.9298 | 35.9348 | 30.8959 |
| `svd_thin/n512/b1` | 70.5518 | 40.0973 | 36.4283 |
| `svd_thin/n512/b4` | 284.3067 | 161.8654 | 146.2295 |
| `svd_values/n256/b1` | 6.9381 | 7.0984 | 3.6875 |
| `svd_values/n256/b4` | 27.6073 | 28.2020 | 14.9531 |
| `svd_values/n512/b1` | 38.6231 | 31.6854 | 15.5705 |
| `svd_values/n512/b4` | 153.6018 | 127.1116 | 62.7075 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0168 | 0.0153 |
| `triangular_solve/n256/b4` | 0.0449 | 0.0553 | 0.0763 |
| `triangular_solve/n512/b1` | 0.0359 | 0.0371 | 0.0562 |
| `triangular_solve/n512/b4` | 0.1402 | 0.1443 | 0.2455 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.1995 | 0.1955 | 0.1648 |
| `cholesky/n256/b4` | 0.7852 | 0.7905 | 0.4806 |
| `cholesky/n512/b1` | 1.2942 | 0.6976 | 0.5545 |
| `cholesky/n512/b4` | 5.6982 | 3.2532 | 2.6876 |
| `eigh/n256/b1` | 5.5640 | 4.1911 | 2.3252 |
| `eigh/n256/b4` | 22.4446 | 16.9854 | 9.3817 |
| `eigh/n512/b1` | 28.7009 | 14.7989 | 9.3818 |
| `eigh/n512/b4` | 115.7501 | 59.8760 | 37.6856 |
| `eigvalsh/n256/b1` | 2.9141 | 2.9357 | 1.7873 |
| `eigvalsh/n256/b4` | 11.9250 | 11.8011 | 7.1830 |
| `eigvalsh/n512/b1` | 14.1796 | 11.5212 | 7.6063 |
| `eigvalsh/n512/b4` | 57.6982 | 47.1255 | 30.6550 |
| `householder_apply/n256/b1` | 2.3929 | 2.4266 | 0.3134 |
| `householder_apply/n256/b4` | 9.7468 | 9.7807 | 1.2305 |
| `householder_apply/n512/b1` | 19.0876 | 19.0913 | 1.9245 |
| `householder_apply/n512/b4` | 83.4880 | 83.6361 | 7.9971 |
| `householder_factor/n256/b1` | 1.4732 | 1.5138 | 0.3188 |
| `householder_factor/n256/b4` | 5.9171 | 5.9859 | 1.2837 |
| `householder_factor/n512/b1` | 12.1184 | 12.1710 | 1.3085 |
| `householder_factor/n512/b4` | 48.4179 | 48.8369 | 5.3889 |
| `lu/n256/b1` | 0.4793 | 0.4743 | 0.1908 |
| `lu/n256/b4` | 1.9876 | 1.9466 | 0.8658 |
| `lu/n512/b1` | 3.2832 | 2.0434 | 0.9237 |
| `lu/n512/b4` | 12.8919 | 8.0884 | 3.8748 |
| `lu_factor/n256/b1` | 0.3763 | 0.3597 | 0.1503 |
| `lu_factor/n256/b4` | 1.5385 | 1.4075 | 0.6215 |
| `lu_factor/n512/b1` | 2.8224 | 1.5394 | 0.6213 |
| `lu_factor/n512/b4` | 11.7836 | 6.2837 | 2.4416 |
| `lu_factor_solve/n256/b1` | 0.3719 | 0.3709 | 0.1900 |
| `lu_factor_solve/n256/b4` | 1.4906 | 1.5161 | 0.7694 |
| `lu_factor_solve/n512/b1` | 2.8856 | 1.5672 | 0.7307 |
| `lu_factor_solve/n512/b4` | 12.1475 | 6.5913 | 2.9970 |
| `lu_solve_prepared/n256/b1` | 0.0171 | 0.0253 | 0.0247 |
| `lu_solve_prepared/n256/b4` | 0.0803 | 0.1122 | 0.1223 |
| `lu_solve_prepared/n512/b1` | 0.0724 | 0.0768 | 0.0948 |
| `lu_solve_prepared/n512/b4` | 0.4403 | 0.4141 | 0.5442 |
| `qr/n256/b1` | 1.8554 | 2.4875 | 1.1236 |
| `qr/n256/b4` | 7.3976 | 9.7833 | 4.5085 |
| `qr/n512/b1` | 11.5256 | 6.9644 | 5.3067 |
| `qr/n512/b4` | 46.3192 | 28.2175 | 21.5296 |
| `rank_revealing_qr/n256/b1` | 2.1048 | 1.5568 | 2.2118 |
| `rank_revealing_qr/n256/b4` | 8.4385 | 6.2235 | 8.9085 |
| `rank_revealing_qr/n512/b1` | 14.9892 | 5.7735 | 14.8476 |
| `rank_revealing_qr/n512/b4` | 60.3626 | 23.3496 | 59.8007 |
| `solve/n256/b1` | 0.3836 | 0.4255 | 0.2108 |
| `solve/n256/b4` | 1.5293 | 1.6009 | 0.8349 |
| `solve/n512/b1` | 2.8575 | 1.6728 | 0.7602 |
| `solve/n512/b4` | 11.3711 | 6.6980 | 3.3234 |
| `svd_thin/n256/b1` | 12.2265 | 9.0072 | 7.1193 |
| `svd_thin/n256/b4` | 48.7733 | 35.6859 | 28.4372 |
| `svd_thin/n512/b1` | 70.8369 | 38.3825 | 30.8327 |
| `svd_thin/n512/b4` | 284.0880 | 153.5735 | 123.5780 |
| `svd_values/n256/b1` | 6.9622 | 7.1970 | 3.6327 |
| `svd_values/n256/b4` | 27.7401 | 28.5317 | 14.6572 |
| `svd_values/n512/b1` | 38.6783 | 32.2632 | 13.4176 |
| `svd_values/n512/b4` | 154.6806 | 128.6505 | 54.6458 |
| `triangular_solve/n256/b1` | 0.0104 | 0.0188 | 0.0155 |
| `triangular_solve/n256/b4` | 0.0451 | 0.0610 | 0.0753 |
| `triangular_solve/n512/b1` | 0.0342 | 0.0422 | 0.0560 |
| `triangular_solve/n512/b4` | 0.1334 | 0.1678 | 0.2522 |

## large, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.7058 | - | 1.0962 |
| `cholesky/n256/b4` | 2.8609 | - | 4.4364 |
| `cholesky/n512/b1` | 4.7079 | - | 7.5810 |
| `cholesky/n512/b4` | 19.5327 | - | 26.2556 |
| `eigh/n256/b1` | 10.2667 | - | 20.7718 |
| `eigh/n256/b4` | 41.2006 | - | 84.3584 |
| `eigh/n512/b1` | 63.0014 | - | 154.7862 |
| `eigh/n512/b4` | 252.4191 | - | 611.7957 |
| `eigvalsh/n256/b1` | 4.9711 | - | 8.1037 |
| `eigvalsh/n256/b4` | 19.9456 | - | 32.5053 |
| `eigvalsh/n512/b1` | 29.6201 | - | 58.1065 |
| `eigvalsh/n512/b4` | 118.8141 | - | 232.5537 |
| `householder_apply/n256/b1` | 5.0307 | - | 6.2642 |
| `householder_apply/n256/b4` | 21.2255 | - | 24.6865 |
| `householder_apply/n512/b1` | 40.8484 | - | 36.9617 |
| `householder_apply/n512/b4` | 170.2230 | - | 151.9478 |
| `householder_factor/n256/b1` | 3.3014 | - | 3.2804 |
| `householder_factor/n256/b4` | 13.2675 | - | 13.3598 |
| `householder_factor/n512/b1` | 26.0840 | - | 22.6834 |
| `householder_factor/n512/b4` | 106.0375 | - | 92.2366 |
| `lu/n256/b1` | 1.2509 | - | 1.6182 |
| `lu/n256/b4` | 5.1144 | - | 6.7435 |
| `lu/n512/b1` | 8.6594 | - | 11.1127 |
| `lu/n512/b4` | 34.6786 | - | 44.5486 |
| `lu_factor/n256/b1` | 1.1207 | - | 1.5380 |
| `lu_factor/n256/b4` | 4.4917 | - | 6.2894 |
| `lu_factor/n512/b1` | 8.0528 | - | 10.3095 |
| `lu_factor/n512/b4` | 32.6959 | - | 42.2683 |
| `lu_factor_solve/n256/b1` | 1.1800 | - | 1.6540 |
| `lu_factor_solve/n256/b4` | 4.7469 | - | 6.7973 |
| `lu_factor_solve/n512/b1` | 8.2821 | - | 10.7876 |
| `lu_factor_solve/n512/b4` | 33.7606 | - | 43.2082 |
| `lu_solve_prepared/n256/b1` | 0.0613 | - | 0.1152 |
| `lu_solve_prepared/n256/b4` | 0.2538 | - | 0.5258 |
| `lu_solve_prepared/n512/b1` | 0.2215 | - | 0.4327 |
| `lu_solve_prepared/n512/b4` | 1.0728 | - | 2.1143 |
| `qr/n256/b1` | 6.2406 | - | 7.2395 |
| `qr/n256/b4` | 24.9107 | - | 29.0384 |
| `qr/n512/b1` | 42.4069 | - | 47.4085 |
| `qr/n512/b4` | 168.9820 | - | 191.5629 |
| `rank_revealing_qr/n256/b1` | 6.7233 | - | 10.2073 |
| `rank_revealing_qr/n256/b4` | 26.9895 | - | 41.1617 |
| `rank_revealing_qr/n512/b1` | 47.7332 | - | 64.9992 |
| `rank_revealing_qr/n512/b4` | 189.9838 | - | 260.6887 |
| `solve/n256/b1` | 1.1715 | - | 1.7200 |
| `solve/n256/b4` | 4.6733 | - | 6.7323 |
| `solve/n512/b1` | 8.2118 | - | 11.2098 |
| `solve/n512/b4` | 32.8445 | - | 43.7830 |
| `svd_thin/n256/b1` | 24.3965 | - | 27.1745 |
| `svd_thin/n256/b4` | 97.6907 | - | 111.4728 |
| `svd_thin/n512/b1` | 154.4072 | - | 189.1721 |
| `svd_thin/n512/b4` | 616.8285 | - | 754.9356 |
| `svd_values/n256/b1` | 11.4284 | - | 11.7941 |
| `svd_values/n256/b4` | 45.7869 | - | 49.3063 |
| `svd_values/n512/b1` | 68.1958 | - | 90.0712 |
| `svd_values/n512/b4` | 271.4686 | - | 375.4643 |
| `triangular_solve/n256/b1` | 0.0340 | - | 0.0640 |
| `triangular_solve/n256/b4` | 0.1468 | - | 0.2645 |
| `triangular_solve/n512/b1` | 0.1165 | - | 0.2428 |
| `triangular_solve/n512/b4` | 0.5994 | - | 1.0307 |

## large, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6968 | 0.4899 | 0.3568 |
| `cholesky/n256/b4` | 2.7789 | 1.9983 | 1.3917 |
| `cholesky/n512/b1` | 4.7700 | 2.4645 | 1.9076 |
| `cholesky/n512/b4` | 19.7539 | 10.4872 | 9.2062 |
| `eigh/n256/b1` | 10.2879 | 7.8871 | 9.5656 |
| `eigh/n256/b4` | 41.3610 | 31.9534 | 38.6274 |
| `eigh/n512/b1` | 63.0367 | 29.1832 | 55.0570 |
| `eigh/n512/b4` | 252.2791 | 116.8161 | 220.0242 |
| `eigvalsh/n256/b1` | 4.9941 | 5.0218 | 3.9511 |
| `eigvalsh/n256/b4` | 19.9892 | 19.9382 | 15.9111 |
| `eigvalsh/n512/b1` | 29.6785 | 19.8896 | 21.4979 |
| `eigvalsh/n512/b4` | 118.5135 | 79.7777 | 86.1821 |
| `householder_apply/n256/b1` | 5.0981 | 5.0690 | 1.6292 |
| `householder_apply/n256/b4` | 21.0890 | 21.0064 | 6.8214 |
| `householder_apply/n512/b1` | 41.8699 | 41.4059 | 9.7509 |
| `householder_apply/n512/b4` | 168.1195 | 167.0964 | 39.4431 |
| `householder_factor/n256/b1` | 3.3400 | 3.3608 | 0.9514 |
| `householder_factor/n256/b4` | 13.3359 | 13.3149 | 3.8001 |
| `householder_factor/n512/b1` | 26.3356 | 26.2339 | 6.8204 |
| `householder_factor/n512/b4` | 106.2559 | 105.8822 | 27.3819 |
| `lu/n256/b1` | 1.2492 | 0.8156 | 0.5399 |
| `lu/n256/b4` | 5.0401 | 3.3920 | 2.4392 |
| `lu/n512/b1` | 9.0120 | 3.8668 | 3.8380 |
| `lu/n512/b4` | 34.8371 | 15.4252 | 14.7322 |
| `lu_factor/n256/b1` | 1.1141 | 0.6685 | 0.4293 |
| `lu_factor/n256/b4` | 4.5099 | 1.1713 | 1.7376 |
| `lu_factor/n512/b1` | 8.0119 | 3.0962 | 3.0215 |
| `lu_factor/n512/b4` | 32.7997 | 9.0854 | 12.4109 |
| `lu_factor_solve/n256/b1` | 1.1794 | 0.7397 | 0.4901 |
| `lu_factor_solve/n256/b4` | 4.7502 | 1.2240 | 1.9656 |
| `lu_factor_solve/n512/b1` | 8.2108 | 3.3039 | 3.2612 |
| `lu_factor_solve/n512/b4` | 33.6200 | 9.5013 | 13.1544 |
| `lu_solve_prepared/n256/b1` | 0.0656 | 0.0619 | 0.0526 |
| `lu_solve_prepared/n256/b4` | 0.2655 | 0.1381 | 0.2149 |
| `lu_solve_prepared/n512/b1` | 0.2080 | 0.1585 | 0.2009 |
| `lu_solve_prepared/n512/b4` | 1.1052 | 0.3545 | 1.2509 |
| `qr/n256/b1` | 6.2291 | 3.0940 | 2.7787 |
| `qr/n256/b4` | 24.8518 | 12.6099 | 11.2444 |
| `qr/n512/b1` | 42.3239 | 14.6788 | 16.7003 |
| `qr/n512/b4` | 169.9092 | 58.8199 | 68.1861 |
| `rank_revealing_qr/n256/b1` | 6.7682 | 3.9773 | 7.8241 |
| `rank_revealing_qr/n256/b4` | 27.0274 | 15.9584 | 31.5002 |
| `rank_revealing_qr/n512/b1` | 47.9304 | 16.8867 | 45.1829 |
| `rank_revealing_qr/n512/b4` | 192.9288 | 67.1224 | 181.5572 |
| `solve/n256/b1` | 1.1787 | 0.7406 | 0.5201 |
| `solve/n256/b4` | 4.6952 | 2.9929 | 2.1533 |
| `solve/n512/b1` | 8.2277 | 3.4163 | 3.2788 |
| `solve/n512/b4` | 32.7802 | 13.5489 | 13.8728 |
| `svd_thin/n256/b1` | 24.6017 | 15.6552 | 13.4262 |
| `svd_thin/n256/b4` | 97.4883 | 63.7787 | 53.9234 |
| `svd_thin/n512/b1` | 154.4648 | 68.0331 | 74.9218 |
| `svd_thin/n512/b4` | 617.2127 | 268.7677 | 305.8075 |
| `svd_values/n256/b1` | 11.4370 | 11.1550 | 7.3810 |
| `svd_values/n256/b4` | 45.9489 | 44.6320 | 28.7003 |
| `svd_values/n512/b1` | 67.9032 | 42.6202 | 33.2093 |
| `svd_values/n512/b4` | 271.9334 | 170.2930 | 153.4783 |
| `triangular_solve/n256/b1` | 0.0335 | 0.0334 | 0.0264 |
| `triangular_solve/n256/b4` | 0.1354 | 0.1286 | 0.1130 |
| `triangular_solve/n512/b1` | 0.1139 | 0.0852 | 0.0996 |
| `triangular_solve/n512/b4` | 0.5112 | 0.3796 | 0.5842 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `cholesky/n256/b1` | 0.6860 | 0.4695 | 0.2645 |
| `cholesky/n256/b4` | 2.8528 | 2.0159 | 1.1555 |
| `cholesky/n512/b1` | 4.7716 | 1.8236 | 1.0863 |
| `cholesky/n512/b4` | 19.7605 | 7.8289 | 5.3730 |
| `eigh/n256/b1` | 10.2918 | 6.8684 | 7.8134 |
| `eigh/n256/b4` | 41.4471 | 28.0567 | 31.9288 |
| `eigh/n512/b1` | 63.1292 | 24.2302 | 39.4021 |
| `eigh/n512/b4` | 253.7012 | 97.1642 | 161.1831 |
| `eigvalsh/n256/b1` | 4.9951 | 5.0345 | 3.5655 |
| `eigvalsh/n256/b4` | 20.0014 | 20.0118 | 14.3529 |
| `eigvalsh/n512/b1` | 29.8102 | 17.9514 | 17.4410 |
| `eigvalsh/n512/b4` | 119.3209 | 71.7773 | 69.8553 |
| `householder_apply/n256/b1` | 5.2028 | 5.2121 | 0.8667 |
| `householder_apply/n256/b4` | 21.4684 | 21.4750 | 3.5887 |
| `householder_apply/n512/b1` | 40.8291 | 40.8593 | 5.0627 |
| `householder_apply/n512/b4` | 170.5361 | 172.2019 | 20.5426 |
| `householder_factor/n256/b1` | 3.2982 | 3.3787 | 0.9459 |
| `householder_factor/n256/b4` | 13.2640 | 13.3935 | 3.8122 |
| `householder_factor/n512/b1` | 26.2556 | 26.1819 | 3.4110 |
| `householder_factor/n512/b4` | 105.5339 | 105.9057 | 13.3137 |
| `lu/n256/b1` | 1.2410 | 0.8208 | 0.4029 |
| `lu/n256/b4` | 5.1130 | 3.3748 | 1.8580 |
| `lu/n512/b1` | 8.6632 | 3.3963 | 2.3949 |
| `lu/n512/b4` | 34.7079 | 13.4095 | 9.6459 |
| `lu_factor/n256/b1` | 1.1123 | 0.6565 | 0.2879 |
| `lu_factor/n256/b4` | 4.4446 | 2.7174 | 1.1822 |
| `lu_factor/n512/b1` | 7.9929 | 2.5764 | 1.7214 |
| `lu_factor/n512/b4` | 32.6126 | 10.4997 | 6.9629 |
| `lu_factor_solve/n256/b1` | 1.1753 | 0.7474 | 0.3514 |
| `lu_factor_solve/n256/b4` | 4.7448 | 2.9678 | 1.4322 |
| `lu_factor_solve/n512/b1` | 8.2074 | 2.7289 | 1.9387 |
| `lu_factor_solve/n512/b4` | 33.5647 | 11.1315 | 7.9748 |
| `lu_solve_prepared/n256/b1` | 0.0628 | 0.0668 | 0.0519 |
| `lu_solve_prepared/n256/b4` | 0.2705 | 0.2785 | 0.2242 |
| `lu_solve_prepared/n512/b1` | 0.2233 | 0.1732 | 0.2022 |
| `lu_solve_prepared/n512/b4` | 1.3049 | 0.9674 | 1.2700 |
| `qr/n256/b1` | 6.1993 | 3.4603 | 2.2150 |
| `qr/n256/b4` | 24.9057 | 14.0648 | 9.0477 |
| `qr/n512/b1` | 42.2099 | 12.5397 | 9.3678 |
| `qr/n512/b4` | 169.8345 | 50.4367 | 38.3772 |
| `rank_revealing_qr/n256/b1` | 6.7327 | 3.8953 | 6.3808 |
| `rank_revealing_qr/n256/b4` | 27.1023 | 15.2674 | 25.8854 |
| `rank_revealing_qr/n512/b1` | 47.9040 | 12.2786 | 36.7153 |
| `rank_revealing_qr/n512/b4` | 191.6607 | 49.5406 | 148.1235 |
| `solve/n256/b1` | 1.1783 | 0.7395 | 0.3900 |
| `solve/n256/b4` | 4.6761 | 3.0075 | 1.6161 |
| `solve/n512/b1` | 8.2291 | 2.8580 | 2.0477 |
| `solve/n512/b4` | 32.8123 | 11.2652 | 8.5167 |
| `svd_thin/n256/b1` | 24.6057 | 14.8108 | 10.7678 |
| `svd_thin/n256/b4` | 97.6221 | 59.6346 | 43.4119 |
| `svd_thin/n512/b1` | 154.3732 | 55.7250 | 52.7037 |
| `svd_thin/n512/b4` | 618.0224 | 225.1837 | 211.6351 |
| `svd_values/n256/b1` | 11.4279 | 11.0607 | 5.7803 |
| `svd_values/n256/b4` | 46.0922 | 44.4624 | 23.9630 |
| `svd_values/n512/b1` | 67.9910 | 40.1327 | 25.8527 |
| `svd_values/n512/b4` | 272.9446 | 160.9860 | 109.3056 |
| `triangular_solve/n256/b1` | 0.0332 | 0.0368 | 0.0259 |
| `triangular_solve/n256/b4` | 0.1423 | 0.1434 | 0.1155 |
| `triangular_solve/n512/b1` | 0.1137 | 0.0897 | 0.1004 |
| `triangular_solve/n512/b4` | 0.5025 | 0.3905 | 0.6608 |

## tall, f64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5442 | - | 0.4512 |
| `householder_factor/4096x256/b1` | 41.7366 | - | 17.3987 |
| `qr/1024x64/b1` | 0.9770 | - | 0.9156 |
| `qr/4096x256/b1` | 41.0475 | - | 42.1477 |
| `rank_revealing_qr/1024x64/b1` | 0.9716 | - | 1.1849 |
| `rank_revealing_qr/4096x256/b1` | 64.5853 | - | 62.3566 |
| `svd_thin/1024x64/b1` | 1.4610 | - | 1.6678 |
| `svd_thin/4096x256/b1` | 72.2171 | - | 67.1778 |

## tall, f64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5380 | 0.5456 | 0.2381 |
| `householder_factor/4096x256/b1` | 42.2233 | 42.4888 | 6.6112 |
| `qr/1024x64/b1` | 0.9804 | 0.8702 | 0.5805 |
| `qr/4096x256/b1` | 41.4095 | 20.7921 | 15.8757 |
| `rank_revealing_qr/1024x64/b1` | 0.9670 | 0.7288 | 1.0217 |
| `rank_revealing_qr/4096x256/b1` | 65.4517 | 24.0529 | 41.0577 |
| `svd_thin/1024x64/b1` | 1.4592 | 1.3700 | 1.0925 |
| `svd_thin/4096x256/b1` | 72.8522 | 40.8140 | 28.3986 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.5392 | 0.5471 | 0.1667 |
| `householder_factor/4096x256/b1` | 41.7857 | 41.8426 | 3.7521 |
| `qr/1024x64/b1` | 0.9796 | 1.1135 | 0.4978 |
| `qr/4096x256/b1` | 41.5791 | 19.5556 | 11.5621 |
| `rank_revealing_qr/1024x64/b1` | 0.9697 | 0.7535 | 1.0101 |
| `rank_revealing_qr/4096x256/b1` | 65.0478 | 18.4424 | 39.0841 |
| `svd_thin/1024x64/b1` | 1.4573 | 1.6338 | 0.9947 |
| `svd_thin/4096x256/b1` | 73.1835 | 35.0415 | 22.2239 |

## tall, c64, 1T (CPU 4)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1639 | - | 1.3289 |
| `householder_factor/4096x256/b1` | 120.9286 | - | 66.3122 |
| `qr/1024x64/b1` | 2.8565 | - | 2.8495 |
| `qr/4096x256/b1` | 147.6854 | - | 132.7333 |
| `rank_revealing_qr/1024x64/b1` | 2.8853 | - | 3.8361 |
| `rank_revealing_qr/4096x256/b1` | 244.2789 | - | 185.7368 |
| `svd_thin/1024x64/b1` | 3.5570 | - | 4.8810 |
| `svd_thin/4096x256/b1` | 232.1298 | - | 218.1109 |

## tall, c64, 4T (CPU 4-7)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1409 | 1.2022 | 0.7833 |
| `householder_factor/4096x256/b1` | 119.9806 | 120.1727 | 19.0254 |
| `qr/1024x64/b1` | 2.8516 | 1.6089 | 1.7964 |
| `qr/4096x256/b1` | 147.0763 | 57.6304 | 47.2080 |
| `rank_revealing_qr/1024x64/b1` | 2.8659 | 1.7891 | 3.1797 |
| `rank_revealing_qr/4096x256/b1` | 244.4681 | 83.9068 | 129.4674 |
| `svd_thin/1024x64/b1` | 3.5510 | 2.3123 | 3.0382 |
| `svd_thin/4096x256/b1` | 233.0140 | 104.0342 | 82.7270 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.1333 | 1.2036 | 0.4820 |
| `householder_factor/4096x256/b1` | 120.2375 | 120.5750 | 11.1477 |
| `qr/1024x64/b1` | 2.8632 | 1.7647 | 1.3281 |
| `qr/4096x256/b1` | 147.9759 | 46.3393 | 30.1873 |
| `rank_revealing_qr/1024x64/b1` | 2.8571 | 1.7491 | 2.9630 |
| `rank_revealing_qr/4096x256/b1` | 247.1862 | 52.7375 | 114.6388 |
| `svd_thin/1024x64/b1` | 3.5275 | 2.4530 | 2.4117 |
| `svd_thin/4096x256/b1` | 232.5261 | 80.2602 | 52.0292 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
