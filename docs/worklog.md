# Worklog

Decisions, fixed failures and open items for this campaign. Newest first.

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
