# Worklog

Decisions, fixed failures and open items for this campaign. Newest first.

## 2026-10-12 — the compact Householder pair is blocked; both arms are re-recorded at `6a873e6`

**What the record said.** At `9e0796c` the faer rows lost `householder_factor` and
`householder_apply` by more than any other family: at 8T, `householder_factor` 4096x256 b1 was
127.8 ms in c64 against OpenBLAS's 12.5 (10.2x) and MKL's 11.15 (11.5x); the loss was there at 1T
too (128.8 ms against 68.7, 1.9x), and it grew with the thread count rather than shrinking. The
signature was in the page itself: `faer-pool` equalled `faer-1lane` to the digit at every shape and
every thread budget -- a pooled row that used no threads at all.

**The cause.** The two kernels applied one reflector at a time, each as a rank-one update, which is
level-2 work over the whole matrix per reflector, where LAPACK's `?geqrf` is blocked and level-3.
Nothing could parallelise it either: the single-reflector apply is faer's `N == 1` path, and that
path does not read the `faer::Par` argument it is handed, so the thread budget reached the batch
lane policy and stopped there.

**The fix, in two steps.** `tensor4all/tlinalg-rs#44` moved both kernels to the compact-WY form: a
panel of `recommended_block_size` columns is factored in place, `upgrade_householder_factor` builds
`T` from the coefficients the panel leaves in the scratch diagonal, and one transpose-form block
apply carries the whole panel to the trailing columns. The forward form is the wrong order -- QR
applies `H_0` first, so the trailing columns take `H_(b-1) ... H_0` -- and is quietly wrong, which is
why faer's own blocked QR uses the transpose form. The stored state is unchanged and the campaign's
own `verify` gate passed it unchanged. `#45` then fixed a regression the first record of the change
showed: at 32x32 faer recommends a block of 4 and the compact-WY factor costs more than the trailing
update it buys, so `medium` 32x32 was 1.4x (batch 1) and 1.7x (batch 128) slower at 1T than before.
Blocking is now off at or below `rows * cols == 48 * 48`, faer's own `QrParams::blocking_threshold`.
That first record was taken at `74f07d3` and is **not published**: the page it would have carried is
superseded by this one, and the revision is one commit behind the pin. Both arms below were measured
from scratch at `6a873e6`.

**What the pair says.** Median `faer-1lane` after/before over each regime's cells, 1T, with the
OpenBLAS rows of the same two runs as the floor (an unchanged binary, so they measure the machine
and nothing else):

| regime | cells | faer median | faer p10-p90 | OpenBLAS median | OpenBLAS p10-p90 |
|---|---|---|---|---|---|
| `small` | 239 | 1.007 | 0.976-1.082 | 1.001 | 0.972-1.023 |
| `medium` | 120 | 1.003 | 0.974-1.033 | 1.000 | 0.988-1.014 |
| `large` | 120 | 0.998 | **0.624**-1.011 | 0.999 | 0.993-1.006 |
| `tall` | 16 | 0.999 | **0.418**-1.003 | 0.999 | 0.991-1.008 |

So the change is exactly where the work was aimed and nowhere else: the large and tall cells move
by up to 2.4x and 2.4x at the fast end of their spread, every other regime's median is inside the
floor its own vendor rows establish, and one small-regime tail (+8% at p90) is the extra call per
reflector that the blocked path pays where it does not block. No small or medium cell loses to
OpenBLAS.

The cells themselves (`faer-1lane` at 1T, then `faer-pool` at 8T, against both vendors' same-run
rows):

| case (c64) | before 1T / 8T | after 1T / 8T | OpenBLAS 1T / 8T | MKL 1T / 8T |
|---|---|---|---|---|
| `householder_factor` 128x128 b1 | 0.46 / 0.46 | **0.35 / 0.28** | 0.44 / 0.38 | 0.54 / 0.18 |
| `householder_factor` 512x512 b1 | 29.4 / 29.7 | **16.7 / 4.4** | 20.8 / 6.5 | 22.7 / 3.4 |
| `householder_factor` 512x512 b4 | 119 / 119 | **67.3 / 17.8** | 83.6 / 26.2 | 92.2 / 13.4 |
| `householder_factor` 1024x64 b1 | 1.34 / 1.32 | **0.99 / 0.67** | 1.06 / 0.35 | 1.32 / 0.48 |
| `householder_factor` 4096x256 b1 | 128.8 / 127.7 | **53.9 / 19.3** | 69.2 / 12.5 | 66.1 / 11.1 |
| `householder_apply` 512x512 b4 | 181 / 181 | **97.2 / 18.4** | 129 / 35.5 | 152 / 20.5 |

`householder_factor` f64 reads the same way at 1T (4096x256 b1 42.0 -> 14.1 against OpenBLAS 23.3
and MKL 17.5) and at 8T its pool now leads OpenBLAS (6.7 against 10.9) while MKL's 3.7 still leads
faer.

**What remains.** The tall c64 shapes are the only place the pooled rows still lose: 4096x256 b1 at
8T is 19.3 ms against OpenBLAS's 12.5 (1.54x) and MKL's 11.1 (1.75x), and 1024x64 b1 at 8T is 0.67
against 0.35. That is faer's GEMM scaling on a tall panel rather than the blocking -- the same shape
in f64 leads OpenBLAS, and every square c64 case leads -- so it is not a reason to reopen this
change. It is an open item if the tall c64 cells are ever a target.

**Not established here.** The blocked path's allocation count is deliberately not pinned: its
trailing update goes through faer's GEMM, which costs the same two allocations per call from batch 1
to 64 on `x86_64-linux` but about twelve per item on `aarch64-darwin`, inside `nano-gemm`'s packing.
That is the backend's count, not the crate's, and the record says so rather than pinning a number no
other target would reproduce. The priming and guard behaviour of this revision is unchanged: the
OpenBLAS rows of the two runs agree to 1.001 median, so the harness measured machine and nothing
else.

## 2026-10-11 — the harness measured its own fixture for seven rows; both arms are re-recorded

**What the record said.** The first pages at `b135f0d` and `7dbed2f` showed faer's `eigvalsh` at
8.2x slower than OpenBLAS (470.97 ms vs 57.21 ms at n=512 batch 4 f64 1T), values-only slower than
faer's own `eigh`, and no scaling at 8T. An independent review of the 7dbed2f record was assigned to
find why, and direct measurement of faer acquitted it: `self_adjoint_evd(A, s, None, ..)` at n=512 is
1.9x *faster* than the same call with `Some(vectors)`, both with the harness's exact generated input
and with a random symmetric one. faer's fork is untouched.

**The defect.** `Prepared::faer` sent `svd_values`, `eigvalsh`, `eig` and `eigvals` to the generic
`call::<T>` helper, and `Prepared::lapack` sent `svd_thin`, `svd_full`, `svd_values`, `eig` and
`eigvals` to `call_lapack`. Both helpers rebuild their inputs and a fresh workspace **inside the
timed region**; for `eigvalsh` the input is `Batch::hpd` = `B B^H + n I`, an n^3 product. The other
families, and the LAPACK arm of the *same* family, measure the prepared `self.op` and `self.ws`. So
what a row meant depended on the family and on the arm: the comparison that read "faer loses 8.2x" was
a fixture build measured against a solve measured.

**The fix**, `tensor4all/tlinalg-rs#41` -> `9e0796c` (merge commit), in
`crates/tlinalg-bench/src/harness/rows.rs`: those seven rows now take the prepared fixture and, where
the output type allows, the prepared buffers (`u`/`vt` into `out`/`out2`; singular values and `eig`'s
outputs stay local because their `T::Real`/`T::Complex` types are not nameable for a generic `T` on
the faer side, and on the vendor side they are nameable through `tlinalg_blas::symbols::Symbols` but
preparing them is a documented follow-up). An independent review found no blocker; the rows that were
already prepared are unchanged, which is the check the change only moved the delegating rows.

**The retraction is published with this record.** At the same case, with the campaign's own protocol
(n=512, batch 4, f64, 1T): `eigvalsh` is now faer 57.53 ms vs OpenBLAS 57.63 ms vs MKL 66.32 ms --
parity with OpenBLAS, not an 8.2x loss. `eigh` (115.9 vs 121.9 vs 145.7), `qr`, `rank_revealing_qr`
and `svd_thin` are faer-favourable or parity; `svd_values` is OpenBLAS-favourable by 1.2x, the
remaining mild values-only gap. The rankings that used already-prepared rows -- the faer loss at 8T on
`householder_factor`/`householder_apply` in c64, and the small-regime faer wins on batch throughput --
are unchanged.

Both arms are re-recorded at `9e0796c` (the fix is in the harness, so the whole cell was invalidated;
a partial run would not have displaced the pages whose faer rows carried the fixture). The pages at
`b135f0d` and `7dbed2f` stay as history and remain citable only for the rows that were prepared.
The pin moves to `9e0796c`.

## 2026-10-11 — the record moves to the merged revision

`tlinalg-rs#39` is merged, as a merge commit (`7dbed2f`) rather than a squash, so the revision the
first record was taken at stays reachable and its manifests keep resolving. The pin moves to that
merge commit.

`main` had meanwhile gained three commits this suite declares invalidating -- `fix(svd): give a
values-only complex ?gesdd the pre-3.7 real workspace` and two strided-rs pin bumps -- so the first
record read `3 behind` rather than `current`, and its `c64` SVD rows were measured before that fix.
Both arms were therefore re-recorded at the new revision, one complete set each, and both cells now
read `full` and `current`. The earlier pages are kept: a record that was correct when it was taken is
not deleted because a later one exists, and the index still shows it, `3 behind`, with its own
commit.

What the two arms say at 8T on the large shapes, as a median of the MKL/OpenBLAS ratio over each
family's four shapes: MKL is faster on most decompositions -- `householder_apply` 0.31,
`householder_factor` 0.35, `qr` 0.66, `eigh` 0.68, `svd_thin` 0.70, `lu_factor` 0.73 -- and slower on
`triangular_solve` (1.13) and `eigvalsh` (1.04). `rank_revealing_qr` is where the two disagree in the
other direction, 1.01 in f64 and 2.13 in c64, and it is the one family whose MKL result would need a
paired repeat before it is quoted. At 1T MKL is slower nearly everywhere (1.03-1.2 in f64, up to 1.5
in c64), which is the opposite of what the 8T columns show and is consistent with OpenBLAS
dispatching to a Cooperlake AVX-512 kernel while MKL's single-threaded path does not.

## 2026-10-11 — MKL is a second vendor arm, and the grid is sampled at its ends

**Why an arm and not an engine string.** MKL and OpenBLAS define the same BLAS/LAPACK symbols, so
one process resolves them to one library: an arm is a *build*, and a run is one arm. The harness now
names the LAPACK row after the library it linked (`lapack-mkl`, `lapack-openblas`) instead of after
a literal, and `tlinalg-blas` refuses a build that asks for both vendors. Two arms at the same
revision are two pages, compared side by side, each carrying its own faer rows and its own vendor
identity. A single page carrying both was the other candidate; it was rejected because it would
have needed the manifest to describe two builds' features, environments and result files at once,
which is more provenance machinery than it saves, and because "one manifest is one build" is worth
keeping. The consequence is deliberate: two arms mean two recorders run sequentially, and no page
holds a vendor comparison that was not measured in one process.

**What MKL needs that OpenBLAS does not.** The installed library, named by `MKLROOT`, not
`blas-src`'s route through `intel-mkl-src` (which would fetch its own MKL tree, and whose features
are additive with the OpenBLAS source this crate already activates). A `build.rs` in `tlinalg-blas`
emits the library side, and one in `tlinalg-bench` -- the package the executable belongs to -- the
final-link side, because `rustc-link-arg` does not reach another package's binary. That side is
load-bearing: `libmkl_intel_thread.so` enters with an undefined `omp_get_num_procs`, and nothing
references `libiomp5`'s symbols, so `--as-needed` drops it unless the link says otherwise; and
`rustc` does not turn a search path into an `-rpath`, so without one the harness only runs with
`LD_LIBRARY_PATH` arranged for it. MKL's interface layer is an ABI, and the environment can choose
it, so the harness pins LP64 and the Intel OpenMP layer before its first MKL call and refuses to
continue if the library will not take them. It reports no dispatched kernel and no processor count,
so those stay empty in the manifest.

**The grid is sampled at the ends, not across it.** Priming is 0.5 s per engine row per case and does
not scale with the shape, so a middle point costs exactly what an end point costs while adding the
least information: batch 1 is latency and batch 1024 is throughput, and the batch between them is
neither, while n=8 sits between two sizes that are already there. Dropping the middle of each axis
took the declared grid from 383 cases to 248 -- 3,968 engine rows per complete set per arm, about
33 minutes of priming each, where the middle points alone were 135 cases. This is a declared
reduction, not a partial run: the shape grid in the suite file *is* what a full-coverage page must
cover, and the workload says in its own words that a cost visible only in the middle of a range is
not covered.

**The large end is affordable, which the earlier worklog flagged as a pilot rather than an
assumption.** Measured on `zen5-cpu` at revision `6d55cb6f68bd` with the OpenBLAS arm (one repeat,
200 ms priming, unpinned and therefore not a published number): `svd_thin` 512x512 batch 4 at 8T is
182 / 129 / 166 ms for faer-1lane / faer-pool / lapack-openblas, and the whole `tall` regime at
4096x256 batch 1 is 20-156 ms per row. The undeclared n=1024 costs 186-386 ms for the same families.
The `large` and `tall` regimes are minutes of wall time; it is the number of rows, not the size of
the matrix, that decides the session.

**Fixed here, because the new records would otherwise be published wrongly.** A partial run no
longer displaces a full-coverage page *without checking that the page it would displace is full*;
the index reads which run a page was actually generated from instead of taking the newest manifest
that would have written that path, so a run the publisher refused can no longer describe a page;
a revision *ahead* of the pin is `current` rather than `diverged`; the validator's
vendor-identity and commit-resolution checks now run even when the declaration has drifted, instead
of being skipped with the declaration-derived ones; and a row the harness recorded as `failed` is no
longer publishable, which the recorders previously accepted as a successful run. `zen5-cpu` is now
a required profile, which the first recorded cell made due.

**The review of this change found more than the change itself.** An independent review of the
finished diff found one blocker and eight important items, and each one was checked against the
source before it was acted on. The blocker was real: the declaration-drift early return still sat
above both commit resolution and the new failed-row check, so a suite edit would have switched those
off for every manifest in the tree -- the drift branch now skips only the declaration-derived checks,
and a synthetic manifest with an unresolvable commit under a drifted declaration is rejected.
The rest: the publisher decides fullness by the same content rule as the index rather than by the
recorded flag, so the two can no longer disagree about what `full` means (and an edited sentence no
longer reads as a moved declaration); a page whose provenance cannot be read is reported rather than
attributed to the newest manifest, and is not overwritten by a partial run; the required-cell gate
checks the cell's selected page instead of every page ever published for it; the report and the
comparator read exactly the files the manifest names, so validation and publication consume the same
evidence, and a hand-run publication now meets the same validate-first bar; `compare_runs.py`
refuses to compare two different arms, keeps the engine in its family aggregation, and says which
arm it compared; the MKL discovery loop sees every installation, records a resolved versioned path
instead of a symlink, and the recorder reads the builder's `%q`-quoted output as shell words rather
than stripping quotes from it; and the enumerated environment now covers the OpenMP placement and
limit variables and `MKL_CBWR`, which the read-back of a thread count was never evidence about.

Two findings were dismissed with reasons: `VENDOR_ARMS` (the build script would reject an unknown
arm, but only after Cargo has been invoked, and the recorder's own vocabulary is worth the two
lines) and the index's newest-manifest tie-break (page provenance is *reported* when it cannot be
read, not required, so a tie is still possible).

**Not done here.** The pin still names `8276e097c214`; it moves to the revision that contains the MKL
arm once that is merged -- with a merge commit, so that the revision the two arms were recorded at
stays reachable -- and both arms are already recorded against it.

## 2026-10-08 — the faer provider is named in the manifest

tlinalg can now be built against tensor4all's fork of faer, published as
`t4a-faer` (with `t4a-faer-traits`). The fork is an experiment bench whose patches
can change numerical behaviour, so two pages could differ only in the faer they
were built against and nothing in the manifest would say so. It is recorded first
because every later measurement depends on it.

The recorder now reads `faer`/`t4a-faer` (and their `-traits` crates) out of the
*measured checkout's* `Cargo.lock` and records each as a `providers[]` entry using
the existing item shape: name and version for a registry source, the revision in
`commit` for a git source, and the source string in the note. The report prints
the faer identity in its provenance block and under the `faer` rows next to the
vendor's `As measured` line, so the page says which faer produced the numbers.

The entry keeps the package's own name (`faer` or `t4a-faer`), never the engine's
provider name: `PROVIDER_OF_ENGINE` maps the `faer-*` engine rows to `tlinalg`,
which is the provider that computes, while `t4a-faer` is a dependency it links.
They are different axes, and the manifest keeps them distinct.

It is recorded, not yet enforced: `validate_run.py` accepts a manifest without a
faer entry, so the one existing baseline page is unchanged. Whether to refuse a
`tlinalg` run that names no faer is a follow-up once a fork-built cell exists to
validate against.

## 2026-10-09 — #21 adopted as a duplication removal, not a measured change

tlinalg-rs#34 removed the two kinds of redundant zero-fill behind #21: the native lane scratch is no
longer reset before the first item (it was zeroed when built), and the LAPACK real-input eig
conversion no longer grows the eigenvector output with `n * n` zeros before overwriting every entry.

This repository cannot adjudicate it, and says so rather than implying otherwise. The native resets
are one O(n^2) pass per *call* against an O(n^3) decomposition — about 1/n, under 0.4% at n = 512
against the three-to-five per cent a 1T cell reproduces to — and the LAPACK one removes a second pass
over output the same routine writes anyway. The allocation counts are unchanged, deliberately, since
resetting allocates nothing. So #21 is closed as a removal of provably duplicate work, with the
correctness gate as its check.

The last loose end of #28 closed with it: the wide case in `nearly_dependent_columns` was
`#[ignore]`d while it disagreed with both faer and the harness, and the disagreement turned out to be
the test's own indexing — the transposed matrix was built with `3` as the column stride instead of
`m`, so the QR ran on a 3x1000 matrix that was mostly zeros. It is enabled and passing, and it is
coverage rather than a regression: at three rows the fixture's perturbations sit far above faer's
skip threshold, and it passes against 0.24.4 too. The tall case remains the one that reproduced #28.

## 2026-10-09 — the first before/after pair, on the small regime

Two recorded pages and the ratio between them: `6d55cb6` (crates.io faer 0.24.4) against `8276e09`
(the fork at `d16929b`, plus the storage/marshalling batch #18, #22, #17, #19), `small` regime,
1T and 8T, one complete set before and two after.

Per-family medians of `after / before` at 1T, over the 18 cells of each family and dtype (so a value
of 0.90 is a tenth faster):

| family | c64 | f64 |
|---|---|---|
| `cholesky` | **0.906** | **0.888** |
| `triangular_solve` | 0.969 | 0.997 |
| `solve` | 0.977 | 0.989 |
| `full_piv_lu` | 0.989 | 0.988 |
| `full_piv_lu_solve` | 0.991 | 0.995 |
| `eigh` | 0.990 | 0.995 |
| `svd_full` | 0.992 | 0.997 |
| `svd_thin` | 0.994 | 0.997 |
| `svd_values` | 0.996 | 0.996 |
| `eigvals` | 0.996 | 1.000 |
| `eig` | 0.998 | 0.999 |
| `eigvalsh` | 0.999 | 1.001 |
| `rank_revealing_qr` | 1.012 | 1.002 |

The 8T rows are the same story with a wider spread, as the timing policy says they must be.

**What the pair establishes.** The Cholesky change (#18) is real and attributable: it is about ten
per cent, consistent across both dtypes and both thread counts, and it cannot come from the fork,
which changed only the QR that Cholesky never calls. Everything else is inside the ±3% a 1T row
reproduces to, so the pair says two things about the rest: the fork's QR repair does **not** cost
anything measurable in the SVD and QR families it passes through, and the two changes kept on smoke
evidence — borrowing the compact reflector column (#17) and solving the right side on a transposed
view (#19) — show **no measurable effect at `n = 4..16`**. They are not wrong: #17 also removes a
per-lane allocation (the allocation counts in `tlinalg` moved from 3 to 2 for `compact_factor`) and
#19 removes a copy of `B`. But at these sizes the copies are not what the clock is measuring, so
the honest verdict is "kept, unproven", and the population that would settle it is a large single
matrix or a wide right-hand side, which this cell does not contain.

**The pair is a combined treatment, not two single-variable pairs.** The fork revision and the batch
landed in the same measured revision, so a reader may only conclude what the two together did. The
Cholesky attribution above is the exception and it rests on the fork having no Cholesky path at all.

**A/A.** The after run took two complete sets, so it carries its own floor. Over the 360 cells of
each `(threads, row)`, the ratio between the two sets has a median of 1.006 to 1.009, a p10-p90 of
1.001 to 1.05 for the lanes, and 1.004 to 1.63 for the 8T pooled rows. A 1T cell is therefore
reproducible to about three to five per cent, which is the yardstick the Cholesky ten per cent is
read against — and why nothing else in the table is called a change.

## 2026-10-08 — the noise floor, measured before any claim was made

A recording run died at its manifest step (a missing `import csv`), which left a complete set of
CSVs with no manifest. They turned out to be worth keeping: comparing them with the successful
re-run of the *same* revision is an A/A pair, and it says which rows a per-cell claim may be made
on.

| threads | row | median | p10-p90 | cells off by more than 15% |
|---|---|---|---|---|
| 1T | `faer-1lane` | 1.002 | 0.972-1.029 | 1.1% |
| 1T | `lapack-openblas` | 1.000 | 0.985-1.018 | 0.0% |
| 8T | `faer-1lane` | 1.005 | 0.983-1.038 | 1.1% |
| 8T | `faer-pool` | 1.007 | 0.771-1.463 | 28.9% |
| 8T | `lapack-openblas` | 0.998 | 0.972-1.030 | 5.3% |

The 1T rows reproduce to about 3%, so the perf work can be adjudicated on them; the pooled 8T rows
move by up to 2.5x on identical code, so a pooled cell without its spread is machine state. The
policy now says so, and `scripts/compare_runs.py` reports the ratios with the spread instead of a
bare table.

The first real cell was recorded in the same pass: `zen5-cpu`, `small` regime, 1T and 8T, 1800 rows
at `6d55cb6`, with the vendor budget set and read back and the idle gate covering the SMT siblings
of the measured cores. The manifest names what produced it — OpenBLAS 0.3.32 linked statically,
built with `DYNAMIC_ARCH` and dispatched at run time to `Cooperlake`, pthread threading — and the
coverage is `partial`, because the small regime is one of four declared populations.

What the baseline says about where to work, in faer-1lane vs lapack-openblas at 1T on `n=4..16`:
the native provider is *slower* than LAPACK for `eigvalsh` (1.4-2.3x), `svd_values` (1.0-1.5x),
`eig` in f64 (1.2-1.35x) and `lu_factor` at `batch=1` (1.8-2.1x), and *faster* for cholesky, qr,
solve, full-pivot LU and the Householder pair. So the workload need for the zero-fill and
direct-output issues is established in the grid already measured, while the reflector-copy and
right-side-solve candidates are not — which is what those issues themselves said to check first.

## 2026-10-08 — the linked-LAPACK gate was red, and the cause was the cache's provenance

Before any cell could be recorded, `tlinalg-rs`'s own linked-LAPACK gate was failing: `tlinalg-blas
--test alloc_counts` died with SIGILL, reproducibly. The first guess was the from-source OpenBLAS
build target, which is undeclared (`getarch` guesses from the build host; here `COOPERLAKE`), and
`DYNAMIC_ARCH=1` was declared for it — which did not fix it. A diagnostic step added to the CI job
(on failure: print the runner's CPU and the linked OpenBLAS configuration) then said what was
actually happening:

- the runner was an **AMD EPYC 7763 (Milan, Zen 3, no AVX-512)**, and the linked library was a
  **`CORE=SAPPHIRERAPIDS`** build;
- the job's log contained **no OpenBLAS build at all**: `Swatinem/rust-cache` had restored a
  `target/` built on a Sapphire Rapids runner and this host executed it.

A vendor library belongs to the machine that built it, which is the same reason the harness is
built out of the measured checkout. The fix is a cache key scoped to the runner's CPU model, plus
`DYNAMIC_ARCH=1` so a fresh build dispatches on CPUID with the required features checked per core.
Merged as `tensor4all/tlinalg-rs#26`; the gate is green.

Two things this changes here: every measurement this campaign publishes has to state the kernel
the vendor runtime *dispatched to*, not the target that was configured — which `run.yaml` already
does — and the same class of mistake (a build from another host) is why `build_for_tlinalg_rev.sh`
keys its target directory by revision and records the build environment.

## 2026-10-08 — issue #13 is fixed upstream

`tlinalg-rs#13` (a spurious singular value and inaccurate factors from faer's divide-and-conquer
SVD on a rank-deficient matrix with clustered singular values) is closed by
`tensor4all/tlinalg-rs#14`, which checks the factors against the input by the Frobenius residual and
repeats with the QR algorithm when the check fails, at a measured cost of 6-25% of a decomposition.
This matters to the campaign in two ways: the SVD rows this suite declares are now measuring fixed
code, and the `verify` gate of `tlbench` is exactly the kind of check that would have caught it.

## 2026-10-08 — the campaign repository is created

**Scope.** A campaign for `tlinalg-rs` on the model of `tprims-benchmark`: the
declarations, the revision pin, the run manifests, the published reports and a
generated staleness index. The harness itself stays in `tlinalg-rs`, because it
must be built out of the same checkout as the library it measures.

**Fixed in the port rather than inherited.**

- *The vendor is named and its budget is enforced.* The interface is provided by
  two crates — faer-backed `tlinalg` and LAPACK/BLAS-backed `tlinalg-blas` — and
  the second one's threading belongs to the vendor library. A row labelled `1T`
  therefore requires setting the vendor's own thread count and reading it back;
  `tlbench` does that, and `run.yaml` records the vendor's version, build
  configuration and the kernel its runtime dispatched to (`vendor`).
- *Priming is time-based and measured.* The reference harness in `tprims-rs`
  records 500 ms of priming while its timer performs a single warm-up call. The
  claim and the code disagree there; here the priming time is measured, so the
  manifest's number is one the harness would have to lie about to produce.
- *The idle gate includes SMT siblings.* `tprims-rs`'s `idle_cpus.py check` looks
  only at the listed logical CPUs, so load on a sibling can contend with the
  physical core being measured without being seen. The copy in `tlinalg-rs`
  expands the set with `thread_siblings_list`, and `run.yaml` states that it did.
- *Coverage is a population, not a scalar size knob.* The upstream suite declares
  a single nominal tensor size (`sizes_mib`); this library's workloads are matrix
  dimensions and batch extents, so a suite declares populations — regime × family
  group × shape grid × batch grid — and `run_spec` records the resolved
  populations plus every case the harness reported as `skipped`.

**Vendor build, first slice.** OpenBLAS, linked **statically** through a new
`tlinalg-blas/link-openblas-static` feature, so the recorder can execute the built
harness directly with no loader search path to arrange. An unqualified build from
source on this host selects `CORE=COOPERLAKE` (an Intel AVX-512 target) with
pthread threading and `NO_AFFINITY`, i.e. not a Zen-tuned kernel; the runtime's
own answer (`openblas_get_corename`) is recorded either way, and no page claims a
Zen kernel was used. BLIS is a later arm: `blas-src` exposes a BLIS source but
`lapack-src` has no BLIS feature, so a BLIS arm is necessarily BLIS BLAS with
reference netlib LAPACK, and a third configuration (OpenBLAS BLAS with netlib
LAPACK) would be needed to separate BLAS from LAPACK contribution. That needs its
own reviewed linkage decision, not another engine string.

**Not yet done.**

- The `smoke` CI job (build the pinned harness) is added together with the first
  pin that contains `tlbench`; until then only the declaration, manifest and index
  checks run, and `required_profiles` is empty so that the missing first cell is
  not an error. The first recorded `(zen5-cpu, tlinalg-kernels)` cell moves
  `zen5-cpu` into `required_profiles`.
- The grid's large regime stops at `n=512` with batch 1 and 4, and `n=1024` is not
  declared anywhere: a universal product over every family and shape is dominated
  by priming alone (an earlier draft of this declaration implied ~7300 rows,
  ~60 minutes of priming before any timed repetition). Whether 1024 and the tall
  full-SVD route are affordable is a pilot, not an assumption.
- Which perf issues this campaign can settle first: the self-contained ones
  (`tlinalg-rs#17`, `#22`, `#23`) and, before any of them, the SVD correctness
  work in `#13`/PR #14.
