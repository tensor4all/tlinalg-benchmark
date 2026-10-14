<!-- generated from data/results/zen5-cpu/tlinalg-kernels/20261014T011937Z-region-floor-after/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tlinalg-kernels` on `zen5-cpu`

- tlinalg-rs commit: `7fdba8a53ba35fd36a088695741bef270c3548ce`
- features: `tlinalg-bench/link-mkl`
- faer provider: `faer` 0.24.4 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.4 @ `6e8e178bef2f51e21cc52d8e17d8ccdd228924f6` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=6e8e178#6e8e178bef2f51e21cc52d8e17d8ccdd228924f6); `t4a-faer-traits` 0.24.0 @ `6e8e178bef2f51e21cc52d8e17d8ccdd228924f6` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=6e8e178#6e8e178bef2f51e21cc52d8e17d8ccdd228924f6)
- harness commit: `2716cd0529058e0080fd6ac5d1472791d653818e`
- hardware profile: `zen5-cpu`
- timestamp: `2026-10-14T01:24:17.770694Z`
- timing policy: v1, best of 5 reps, priming 500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/record_run.py zen5-cpu tlinalg-kernels --checkout /tmp/tl-region-after --vendor mkl --regimes medium,large,tall --threads 8 --families qr,householder_factor,householder_apply --dtypes f64,c64 --reps 5 --prime-ms 500 --label region-floor-after`
- raw data: `data/results/zen5-cpu/tlinalg-kernels/20261014T011937Z-region-floor-after/`

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
    As measured: `faer` 0.24.4 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.4 @ `6e8e178bef2f51e21cc52d8e17d8ccdd228924f6` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=6e8e178#6e8e178bef2f51e21cc52d8e17d8ccdd228924f6); `t4a-faer-traits` 0.24.0 @ `6e8e178bef2f51e21cc52d8e17d8ccdd228924f6` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=6e8e178#6e8e178bef2f51e21cc52d8e17d8ccdd228924f6)
  - `faer-pool` — The same provider on a host-owned Rayon pool of the row's thread budget, with the library choosing its batch lanes. The thread count is a column, not part of the row name.
    Identity: tlinalg-rs (this repository's pinned revision)
    Caveat: A faer count hint is not a hard active-thread limit; see the `Parallel` budget contract in tlinalg.
    As measured: `faer` 0.24.4 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `faer-traits` 0.24.0 (linked dependency of the tlinalg provider; source registry+https://github.com/rust-lang/crates.io-index); `t4a-faer` 0.24.4 @ `6e8e178bef2f51e21cc52d8e17d8ccdd228924f6` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=6e8e178#6e8e178bef2f51e21cc52d8e17d8ccdd228924f6); `t4a-faer-traits` 0.24.0 @ `6e8e178bef2f51e21cc52d8e17d8ccdd228924f6` (linked dependency of the tlinalg provider; source git+https://github.com/tensor4all/faer.git?rev=6e8e178#6e8e178bef2f51e21cc52d8e17d8ccdd228924f6)
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
| `householder_apply/n128/b1` | 0.1273 | 0.0988 | 0.0599 |
| `householder_apply/n128/b128` | 17.3008 | 13.9929 | 7.6105 |
| `householder_apply/n32/b1` | 0.0108 | 0.0137 | 0.0073 |
| `householder_apply/n32/b128` | 1.3605 | 0.1828 | 0.9249 |
| `householder_factor/n128/b1` | 0.1044 | 0.0952 | 0.0845 |
| `householder_factor/n128/b128` | 13.7030 | 12.9863 | 11.0692 |
| `householder_factor/n32/b1` | 0.0073 | 0.0100 | 0.0068 |
| `householder_factor/n32/b128` | 0.9257 | 0.1287 | 0.8848 |
| `qr/n128/b1` | 0.3412 | 0.3165 | 0.2433 |
| `qr/n128/b128` | 44.2073 | 40.7928 | 39.2858 |
| `qr/n32/b1` | 0.0211 | 0.0244 | 0.0121 |
| `qr/n32/b128` | 2.6524 | 0.6720 | 1.5536 |

## medium, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_apply/n128/b1` | 0.4855 | 0.2512 | 0.1790 |
| `householder_apply/n128/b128` | 64.2469 | 34.0966 | 20.5549 |
| `householder_apply/n32/b1` | 0.0142 | 0.0177 | 0.0195 |
| `householder_apply/n32/b128` | 1.8461 | 0.4722 | 2.5576 |
| `householder_factor/n128/b1` | 0.3497 | 0.2060 | 0.1809 |
| `householder_factor/n128/b128` | 45.4347 | 27.0907 | 23.2604 |
| `householder_factor/n32/b1` | 0.0113 | 0.0142 | 0.0154 |
| `householder_factor/n32/b128` | 1.4137 | 0.3709 | 2.0077 |
| `qr/n128/b1` | 0.9697 | 0.6154 | 0.4374 |
| `qr/n128/b128` | 124.8894 | 80.2347 | 58.0223 |
| `qr/n32/b1` | 0.0428 | 0.0463 | 0.0282 |
| `qr/n32/b128` | 5.5134 | 1.3719 | 3.6384 |

## large, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_apply/n256/b1` | 0.8201 | 0.3392 | 0.3132 |
| `householder_apply/n256/b4` | 3.3017 | 1.3753 | 1.2219 |
| `householder_apply/n512/b1` | 6.0277 | 1.6676 | 1.9188 |
| `householder_apply/n512/b4` | 25.6098 | 7.0992 | 7.7863 |
| `householder_factor/n256/b1` | 0.6234 | 0.3880 | 0.3281 |
| `householder_factor/n256/b4` | 2.5074 | 1.5498 | 1.2784 |
| `householder_factor/n512/b1` | 4.2819 | 1.5897 | 1.2771 |
| `householder_factor/n512/b4` | 17.3375 | 6.5577 | 5.2666 |
| `qr/n256/b1` | 1.8666 | 1.1566 | 1.0018 |
| `qr/n256/b4` | 7.4367 | 4.6192 | 4.0661 |
| `qr/n512/b1` | 11.5930 | 4.6365 | 5.3162 |
| `qr/n512/b4` | 46.4458 | 18.4000 | 21.4564 |

## large, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_apply/n256/b1` | 3.2961 | 0.8229 | 0.8887 |
| `householder_apply/n256/b4` | 13.5469 | 3.3805 | 3.4955 |
| `householder_apply/n512/b1` | 24.0233 | 4.1111 | 5.0651 |
| `householder_apply/n512/b4` | 96.8326 | 17.0080 | 20.7959 |
| `householder_factor/n256/b1` | 2.2737 | 0.8949 | 0.9245 |
| `householder_factor/n256/b4` | 9.1114 | 3.5692 | 3.7006 |
| `householder_factor/n512/b1` | 16.2744 | 4.0874 | 3.2864 |
| `householder_factor/n512/b4` | 67.1225 | 16.6238 | 13.7179 |
| `qr/n256/b1` | 6.2335 | 2.3026 | 2.2121 |
| `qr/n256/b4` | 24.9646 | 9.0667 | 8.9139 |
| `qr/n512/b1` | 42.4775 | 10.1421 | 9.4734 |
| `qr/n512/b4` | 169.7286 | 40.5812 | 38.2003 |

## tall, f64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 0.3311 | 0.3067 | 0.1663 |
| `householder_factor/4096x256/b1` | 14.1083 | 4.8556 | 3.7394 |
| `qr/1024x64/b1` | 0.9768 | 0.7722 | 0.4825 |
| `qr/4096x256/b1` | 41.2786 | 15.1244 | 11.4574 |

## tall, c64, 8T (CPU 4-11)

| case | faer-1lane (ms) | faer-pool (ms) | lapack-mkl (ms) |
|---|---|---|---|
| `householder_factor/1024x64/b1` | 1.0009 | 0.5295 | 0.4874 |
| `householder_factor/4096x256/b1` | 54.2397 | 13.5859 | 11.0531 |
| `qr/1024x64/b1` | 2.8628 | 1.3241 | 1.3340 |
| `qr/4096x256/b1` | 147.0773 | 36.6200 | 28.4530 |

This run made a single complete set, so it carries no A/A: it is a scan, not a paired comparison.
