#!/usr/bin/env bash
# Build the campaign harness out of one tlinalg-rs checkout, into a target
# directory keyed by that checkout's commit.
#
#   build_for_tlinalg_rev.sh <tlinalg-rs-dir> <out-var-file> [bin...]
#
# Writes shell assignments to <out-var-file>:
#   TLINALG_REV, TLINALG_DIRTY, TLINALG_DIR, BIN_DIR, BUILD_FEATURES, BUILD_ENV
#
# Three things this deliberately does *not* do.
#
# It does not build the harness from this repository. The harness is part of
# tlinalg-rs (`crates/tlinalg-bench`, binary `tlbench`) and is compiled out of
# the same checkout as the library it measures, so `run.yaml`'s commit
# describes both. A harness built elsewhere could silently measure a different
# revision of the library than the one it was written against.
#
# It does not let baseline and candidate share a target directory, and it
# clears the compiler cache for the build: a cache keyed on inputs that do not
# include the sibling checkout can mix revisions.
#
# It does not let the environment decide the vendor's thread count. The build
# itself is asked for a static OpenBLAS (`link-openblas-static`), which is what
# lets the recorder execute the binary directly instead of arranging a loader
# search path; `OPENBLAS_NUM_THREADS` is dropped because `openblas-src` folds it
# into the built library, and the thread budget belongs to the measurement, not
# to the build. `OPENBLAS_DYNAMIC_ARCH` is *set* below, because that is the declaration of how
# the vendor was built.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TLINALG_DIR="$(cd "${1:?tlinalg-rs checkout required}" && pwd -P)"
OUT_FILE="${2:?output variable file required}"
shift 2
BINS=("$@")
[[ ${#BINS[@]} -gt 0 ]] || BINS=(tlbench)

[[ -d "$TLINALG_DIR/crates/tlinalg-bench" ]] || { echo "ERROR: $TLINALG_DIR is not a tlinalg-rs checkout with the harness" >&2; exit 1; }
MANIFEST="$TLINALG_DIR/Cargo.toml"
[[ -f "$MANIFEST" ]] || { echo "ERROR: $MANIFEST not found" >&2; exit 1; }

rev="$(git -C "$TLINALG_DIR" rev-parse HEAD)"
dirty=false
[[ -z "$(git -C "$TLINALG_DIR" status --porcelain --untracked-files=no)" ]] || dirty=true
suffix=""; [[ $dirty == true ]] && suffix="-dirty"
target="$PROJECT_DIR/target/tlinalg-rev/${rev:0:12}${suffix}"
profile="${BENCH_BUILD_PROFILE:-release}"

bin_args=(); for bin in "${BINS[@]}"; do bin_args+=(--bin "$bin"); done
profile_flag=(); subdir=debug
if [[ "$profile" == release ]]; then profile_flag=(--release); subdir=release; fi

FEATURES="${BENCH_FEATURES:-tlinalg-bench/link-openblas-static}"
# Declared, not inherited. `openblas-src` reads `OPENBLAS_DYNAMIC_ARCH` at build time; without it
# the from-source OpenBLAS guesses a target from the build host (here `COOPERLAKE`, an Intel
# AVX-512 target), and a guessed target is not one the run-time CPU is obliged to execute -- the
# library's own linked tests died with SIGILL on CI exactly that way. `DYNAMIC_ARCH=1` compiles
# several cores and dispatches on CPUID with the required features checked per core; on this host
# that dispatcher still selects COOPERLAKE, and the manifest records the kernel it dispatched to.
VENDOR_BUILD_ENV="OPENBLAS_DYNAMIC_ARCH=1"
RUSTC_WRAPPER= CARGO_TARGET_DIR="$target" \
    env OPENBLAS_DYNAMIC_ARCH=1 -u OPENBLAS_NUM_THREADS -u OMP_NUM_THREADS -u RAYON_NUM_THREADS \
    cargo build --manifest-path "$MANIFEST" "${profile_flag[@]}" \
    -p tlinalg-bench --features "$FEATURES" "${bin_args[@]}" >&2

bin_dir="$target/$subdir"
{
    printf 'TLINALG_REV=%q\n' "$rev"
    printf 'TLINALG_DIRTY=%q\n' "$dirty"
    printf 'TLINALG_DIR=%q\n' "$TLINALG_DIR"
    printf 'BIN_DIR=%q\n' "$bin_dir"
    printf 'BUILD_FEATURES=%q\n' "$FEATURES"
    printf 'BUILD_ENV=%q\n' "$VENDOR_BUILD_ENV"
} > "$OUT_FILE"
echo "built ${BINS[*]} for tlinalg-rs $rev (dirty=$dirty) in $bin_dir" >&2
