# Worklog

Decisions, fixed failures and open items for this campaign. Newest first.

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
