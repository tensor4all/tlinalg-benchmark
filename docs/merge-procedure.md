# Merging a candidate into `tlinalg-rs` main

This instantiates the shared procedure in
[campaign-toolkit/docs/merge-procedure.md](https://github.com/tensor4all/campaign-toolkit/blob/main/docs/merge-procedure.md);
the reasoning is there, this page names what is `tlinalg`'s own. Read both before merging.

## The campaign's specifics

| what | where |
| --- | --- |
| measured library | `tlinalg-rs`, pinned by `pins/tlinalg-rs.rev`, checked out in `extern/tlinalg-rs` |
| harness | `tlbench`, **in the measured repository**, so a harness change is a measured change |
| measured paths | the descriptor's `measured` block: the crates the build script links, not the whole tree |
| suites | `benchmarks/suites/`; the declared shapes, dtypes, orders and thread budgets are its populations |
| profiles | `benchmarks/profiles.yaml`; a cell's CPU set comes from the suite's `runs[].cpu_sets` |
| engines | `faer-1lane`, `faer-pool`, and one vendor arm per run (`lapack-openblas` or `lapack-mkl`) |
| adoption pin | `pins/tlinalg-rs.rev` |

## Preconditions beyond the shared ones

1. **The harness moved with the library.** `tlbench` lives in `tlinalg-rs`, so a merge that touches it
   invalidates the numbers exactly as a library change does. If the measured paths of the candidate
   include the harness crate, the pair must be recorded after that change, not before.
2. **The vendor arm is not merged across.** The two vendor arms are two runs, two manifests and two
   pages; a merge does not combine them, and a page still quotes one vendor.
3. **The candidate's affected families are declared from the changed paths** before the pair: a change
   to the packing or the lane policy reaches every family that calls the kernel, and the declaration
   has to say so rather than assuming the family named in the issue.

## The periodic run

"Nothing regressed anywhere" is answered by a full declared-suite run at the frozen revision, one
vendor arm at a time, published as its own page. It is not part of a merge. The last published page
stands for any family a candidate pair did not measure.

## Current candidates

None open at the time of writing. The adoption pin is `06466b1`, recorded before this page existed;
its page and the worklog say what was measured at it.
