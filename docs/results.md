# Result layout

`suite_id` identifies the workload; `target_profile` identifies the machine
(`benchmarks/profiles.yaml`). They are the two axes of every cell. The body of a
profile is a fact about a machine, so it lives in `campaign-toolkit`
(`campaign_toolkit/profiles/`); this repository's `profiles.yaml` names the
profiles it measures.

```text
data/results/<profile>/<suite>/<timestamp>/     raw: run.yaml, verify-*.txt, run*.csv, *.guard, report.md
result/<profile>/<suite>/<commit12>[-version][-vendor][-dirty].md   one page per measured run
result/INDEX.md                                 generated table of contents over those pages
```

A result page is one `(suite, hardware profile, measured revision, vendor arm)`, and it
carries that revision and the hardware itself: commit, version when the measured
project has one, features, harness commit, host CPU, logical CPU count, L3, OS
and arch, the CPU set used at each thread count, the timing policy, the faer
crates the measured provider was built against, the vendor library and its
kernel, and the guarantees. Measuring a new revision adds a page rather than
replacing the previous one. A dirty checkout gets its own `-dirty` page, because
those numbers are not comparable with a clean build of the same commit.

**One vendor per page.** LAPACK and BLAS own their symbols, so a binary that
links OpenBLAS and a binary that links MKL cannot be the same binary: an *arm* is
a build, and a run is one arm. Two arms at the same revision are therefore two
pages, compared side by side, each carrying its own faer rows and its own vendor
identity. The vendor is in the page name because it is part of what was measured,
and the engine rows are named after the vendor the binary actually linked --
`lapack-mkl`, not a label chosen when the row was written.

## run.yaml

Validated against the run schema shipped by `campaign-toolkit`
(`campaign_toolkit/schemas/benchmark-run.schema.json`) before it is written. It
records:

- the profile, suite, suite file and its hash, timestamp and the exact command;
- `library`: path, commit, dirty state and features of the checkout that was
  measured and that the harness was built from;
- `vendor`: the BLAS/LAPACK library the vendor arm was linked against — name,
  linkage, version, build configuration, the kernel its runtime dispatched to,
  and its threading implementation. A measurement whose vendor cannot be named is
  not evidence, so the validator refuses a manifest that declares a vendor arm
  without one;
- `harness`: commit and dirty state;
- `host`: CPU, logical CPU count, OS, arch, L3 geometry;
- `threads`: the counts, the CPU set used for each, the ambient thread variables
  (removed for the measured process), and how the budget was enforced;
- `timing_policy`: version, priming, statistic, repetitions;
- `providers`: what was compared against, with versions or commits — the
  `tlinalg` provider and the `faer`/`t4a-faer` crates it links, read from the
  measured checkout's `Cargo.lock` (a registry dependency by name and version, a
  git dependency by revision), plus the `openblas` vendor arm. Which faer was
  linked is provenance: the fork's patches can move numbers, so a page that names
  the tlinalg commit but not its faer is not comparable with one built against a
  different faer;
- `guards`: the idle window including the sibling check, the busy threshold, the
  attempt budget, the log files;
- `run_spec`: the resolved populations this run covered — regime, families,
  shape grid, batch grid, and the cases the harness reported as `skipped` —
  and whether that is the whole declaration.

## Coverage and staleness

`result/INDEX.md` is generated and has two tables: the newest full-coverage page
per cell with its currency, and every published page keyed by revision and
hardware. Its point is that reports are self-describing but the *set* of them was
not: with one tracked file per cell, a cell that has not been re-measured keeps
an old file, and a reader sees a commit hash and a table without being able to
tell whether that cell reflects the current library.

`status` is computed against `pins/tlinalg-rs.rev`:

| status | meaning |
|---|---|
| `missing` | no run recorded for this cell |
| `current` | measured at the reference revision, or at a descendant |
| `N behind` | N commits touching the suite's `invalidated_by` paths lie between the measured revision and the reference |
| `stale` | as `behind`, but N exceeds the suite's `stale_after` |
| `dirty` | the measured checkout had uncommitted changes; never comparable |
| `diverged` | the measured revision is neither an ancestor nor a descendant of the reference |

`behind` counts *invalidating* commits, not raw distance: a suite declaring only
`crates/` is not out of date because a document changed. A revision *ahead* of the
reference is `current` rather than `diverged`: it already contains everything the
reference names.

`coverage` is `full` when the cell was measured over the suite's whole declared spec
*for that vendor arm* and the declaration has not moved since, `partial` when it
covered a subset, and `declaration-changed` when the declaration itself changed after
the measurement, so the two have to be compared by hand. "The whole declared spec for
that arm" is the faer engines the declaration names plus that arm's own LAPACK row:
vendor arms are mutually exclusive binaries, so no single run could measure two of
them, and measuring the projection is what makes a vendor cell full instead of partial
for ever. `scripts/campaign.py` holds that projection, and the recorder and the
validator both call it, so the two cannot disagree about what coverage means. A
partial or declaration-changed page never displaces a full-coverage one, and
`publish_report.py` checks that the page already there really is full-coverage before
it declines to replace it -- a page that only *would* have been written from the newest
run is not the same thing as the run the page holds.

## Comparing two revisions

A change is judged from two recorded pages, not from one run read twice. The procedure, which is
also what the perf work on `tlinalg-rs#16`-`#25` follows:

0. **One arm at a time**, chosen with `--vendor`, because one binary links one vendor library. A
   vendor comparison is two pages at the same revision, not one page with two tables: the two arms
   were built separately, and each page says what its own build linked.

1. A **clean checkout per revision**, so neither is recorded dirty: `git worktree add --detach
   /tmp/tlinalg-base <before-commit>` (and one for the change), and no edits in either while it is
   measured.
2. The same populations, thread counts and dtypes on both sides, into the *same* suite declaration,
   so the two runs are the same cells: `scripts/record_run.py zen5-cpu <suite> --regimes
   ... --threads ... --checkout <worktree>`.
3. **At least two complete sets** (`--aa 2`) for anything that will be claimed as a performance
   change, because the timing policy's measured noise floor makes a single set insufficient for the
   pooled rows and only marginal for the rest.
4. `scripts/compare_runs.py <before-run-dir> <after-run-dir>`, which reports per-cell ratios, the
   per-family medians and the A/A spread, and says plainly when it is a scan rather than a paired
   comparison.
5. Both runs are recorded as pages even when one is a regression: a page that only shows the
   improvement is a page that hides the rest of the grid.
