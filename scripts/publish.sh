#!/bin/sh
# One publication of tlinalg-kernels: both vendor arms at the pin, then the site.
set -eu
REV=$(grep -v '^#' pins/tlinalg-rs.rev | grep -E '^[0-9a-f]{40}' | head -1)
LABEL="pub-$(echo "$REV" | cut -c1-8)-$(date -u +%Y%m%d)"
TASKSET="taskset -c 0-3,12-15"
for vendor in mkl openblas; do
    $TASKSET python3 scripts/record_run.py zen5-cpu tlinalg-kernels --vendor $vendor \
        --aa 3 --reps 5 --prime-ms 250 --label "$LABEL-$vendor"
done
python3 scripts/gen_site.py
