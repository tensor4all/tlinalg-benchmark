#!/bin/sh
# One publication of this campaign: the competition suite on both vendor arms, then the
# scaling suite (which has no vendor row), then the site.
#
# The routine (campaign_toolkit.publish) preflights the machine and the trees, runs this,
# commits what it wrote and pushes.
set -eu
REV=$(grep -v '^#' pins/tlinalg-rs.rev | grep -E '^[0-9a-f]{40}' | head -1)
LABEL="pub-$(echo "$REV" | cut -c1-8)-$(date -u +%Y%m%d)"
TASKSET="taskset -c 0-3,12-15"

# Each arm measures two engines (the library row plus this vendor's row), so the
# process-set count has to be a multiple of two for a complete rotation cycle.
for vendor in mkl openblas; do
    $TASKSET python3 scripts/record_run.py zen5-cpu tlinalg-competition --vendor $vendor \
        --aa 4 --reps 5 --prime-ms 250 --label "$LABEL-competition-$vendor"
done
$TASKSET python3 scripts/record_run.py zen5-cpu tlinalg-scaling --vendor mkl \
    --aa 4 --reps 5 --prime-ms 250 --label "$LABEL-scaling"
python3 scripts/gen_site.py
