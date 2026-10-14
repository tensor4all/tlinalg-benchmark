# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `bf88c0a6e568b70d5bc724d925da3e99b1601609`
- features: `tlinalg-bench/link-mkl`
- faer provider: `faer` 0.24.4 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.4 @ `22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=22f23cf#22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5); `t4a-faer-traits` 0.24.0 @ `22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=22f23cf#22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5)
- harness commit: `2716cd0529058e0080fd6ac5d1472791d653818e`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-14T01:01:18.015926Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --checkout /tmp/tl-region-before --vendor mkl --regimes medium,large,tall --threads 8 --families qr,householder_factor,householder_apply --dtypes f64,c64 --reps 5 --prime-ms 500 --label region-floor-before`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261014T005727Z-region-floor-before/`

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
    As measured: `faer` 0.24.4 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.4 @ `22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=22f23cf#22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5); `t4a-faer-traits` 0.24.0 @ `22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=22f23cf#22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `faer` 0.24.4 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.4 @ `22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=22f23cf#22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5); `t4a-faer-traits` 0.24.0 @ `22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=22f23cf#22f23cfd42383fe8d9d2f5816ea49e045f0d0ef5)
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
- CPU sets: 8T -> `4-11`

Every row below passed `tlbench verify` on the same grid before timing: the two
providers' factorizations are checked against each provider's documented convention
(reconstruction, orthonormality, residuals), not against each other's floating-point
output. Times are milliseconds, the best wall time per case and engine row; with more
than one complete set repeat the table shows the best repeat, and the A/A spread is
reported at its foot.

## medium, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_apply/n128/b1` | 0.1286 | 0.1847 | 0.0598 |
| `householder_apply/n128/b128` | 17.5432 | 24.5529 | 7.5044 |
| `householder_apply/n32/b1` | 0.0109 | 0.0133 | 0.0075 |
| `householder_apply/n32/b128` | 1.4028 | 0.1826 | 0.9218 |
| `householder_factor/n128/b1` | 0.1063 | 0.1685 | 0.0841 |
| `householder_factor/n128/b128` | 13.8613 | 22.4209 | 11.0822 |
| `householder_factor/n32/b1` | 0.0073 | 0.0097 | 0.0068 |
| `householder_factor/n32/b128` | 0.9328 | 0.2392 | 0.8905 |
| `qr/n128/b1` | 0.3509 | 0.9422 | 0.2381 |
| `qr/n128/b128` | 45.5260 | 121.7733 | 39.1632 |
| `qr/n32/b1` | 0.0215 | 0.0668 | 0.0120 |
| `qr/n32/b128` | 2.6903 | 0.6748 | 1.5554 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_apply/n128/b1` | 0.4856 | 0.3303 | 0.1780 |
| `householder_apply/n128/b128` | 64.2607 | 44.4352 | 20.5249 |
| `householder_apply/n32/b1` | 0.0143 | 0.0175 | 0.0196 |
| `householder_apply/n32/b128` | 1.8577 | 0.2460 | 2.5396 |
| `householder_factor/n128/b1` | 0.3498 | 0.2810 | 0.1794 |
| `householder_factor/n128/b128` | 45.6085 | 36.6641 | 23.3976 |
| `householder_factor/n32/b1` | 0.0113 | 0.0141 | 0.0155 |
| `householder_factor/n32/b128` | 1.4547 | 0.3654 | 2.0047 |
| `qr/n128/b1` | 0.9716 | 1.1960 | 0.4367 |
| `qr/n128/b128` | 125.0989 | 156.1581 | 57.9357 |
| `qr/n32/b1` | 0.0426 | 0.0898 | 0.0287 |
| `qr/n32/b128` | 5.3956 | 1.3707 | 3.6685 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_apply/n256/b1` | 0.8227 | 0.3509 | 0.3167 |
| `householder_apply/n256/b4` | 3.3114 | 1.3979 | 1.2194 |
| `householder_apply/n512/b1` | 6.0163 | 1.6420 | 1.8927 |
| `householder_apply/n512/b4` | 25.5233 | 7.0794 | 7.8702 |
| `householder_factor/n256/b1` | 0.6209 | 0.3947 | 0.3254 |
| `householder_factor/n256/b4` | 2.5055 | 1.5766 | 1.3044 |
| `householder_factor/n512/b1` | 4.2664 | 1.5864 | 1.2802 |
| `householder_factor/n512/b4` | 17.4334 | 6.5112 | 5.2671 |
| `qr/n256/b1` | 1.8798 | 2.3740 | 1.0049 |
| `qr/n256/b4` | 7.5209 | 9.6796 | 4.0557 |
| `qr/n512/b1` | 11.7316 | 6.9395 | 5.3096 |
| `qr/n512/b4` | 47.0464 | 27.6736 | 21.4688 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_apply/n256/b1` | 3.3015 | 0.8225 | 0.8747 |
| `householder_apply/n256/b4` | 13.5842 | 3.4394 | 3.5031 |
| `householder_apply/n512/b1` | 24.1936 | 4.1355 | 5.0617 |
| `householder_apply/n512/b4` | 97.3824 | 17.1137 | 20.7776 |
| `householder_factor/n256/b1` | 2.2870 | 0.9137 | 0.9253 |
| `householder_factor/n256/b4` | 9.1636 | 3.6513 | 3.7007 |
| `householder_factor/n512/b1` | 16.3351 | 4.0762 | 3.2832 |
| `householder_factor/n512/b4` | 67.1769 | 16.8500 | 13.7671 |
| `qr/n256/b1` | 6.2175 | 3.4498 | 2.2055 |
| `qr/n256/b4` | 24.9425 | 13.9327 | 8.9393 |
| `qr/n512/b1` | 42.3053 | 12.4234 | 9.4771 |
| `qr/n512/b4` | 169.2009 | 49.6447 | 38.2519 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3317 | 0.3117 | 0.1661 |
| `householder_factor/4096x256/b1` | 14.1403 | 4.8554 | 3.7689 |
| `qr/1024x64/b1` | 0.9839 | 0.9902 | 0.4836 |
| `qr/4096x256/b1` | 41.1203 | 15.1987 | 11.3294 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0405 | 0.5455 | 0.4904 |
| `householder_factor/4096x256/b1` | 55.5087 | 13.4311 | 11.2815 |
| `qr/1024x64/b1` | 2.8519 | 1.4549 | 1.3352 |
| `qr/4096x256/b1` | 146.9434 | 36.8801 | 28.5970 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
