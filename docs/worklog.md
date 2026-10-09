# Worklog

Decisions, fixed failures and open items for this campaign. Newest first.

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
