#!/usr/bin/env bash
# Materialise extern/tlinalg-rs.
#
#   setup_extern_deps.sh            # from pins/tlinalg-rs.rev, via a clone
#   setup_extern_deps.sh <dir>      # symlink an existing checkout at <dir>
#
# The harness is built out of this checkout, so it has to exist before any
# build.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LINK="$PROJECT_DIR/extern/tlinalg-rs"
if [[ $# -ge 1 ]]; then
    DIR="$(cd "$1" && pwd -P)"
    [[ -d "$DIR/crates/tlinalg" ]] || { echo "ERROR: $DIR is not a tlinalg-rs checkout" >&2; exit 1; }
    rm -rf "$LINK"
    ln -sfn "$DIR" "$LINK"
    echo "extern/tlinalg-rs -> $DIR ($(git -C "$DIR" rev-parse --short HEAD), dirty=$( [[ -n "$(git -C "$DIR" status --porcelain --untracked-files=no)" ]] && echo true || echo false ))"
    exit 0
fi
REV="$(tr -d '[:space:]' < "$PROJECT_DIR/pins/tlinalg-rs.rev")"
[[ -n "$REV" ]] || { echo "ERROR: pins/tlinalg-rs.rev is empty" >&2; exit 1; }
if [[ -d "$LINK/.git" ]]; then
    git -C "$LINK" fetch -q origin
else
    rm -f "$LINK"
    git clone -q https://github.com/tensor4all/tlinalg-rs "$LINK"
fi
git -C "$LINK" checkout -q "$REV"
echo "extern/tlinalg-rs at $REV ($(git -C "$LINK" log --oneline -1))"
