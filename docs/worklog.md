# Worklog

Decisions, fixed failures and open items for this campaign. Newest first.

## 2026-10-13 (later) — the compact-WY factor's own reduction is split too; both arms re-recorded at `e6ee2d3`

**What the previous record left.** With the block apply's reduction split, the tall c64
`householder_factor` cell was 16.05 ms against OpenBLAS's 12.50. Separating that call's three phases
again showed 43% of the pooled row was still serial: the panel (5.0 ms, and it stops scaling at four
threads) and the compact-WY factor build (2.7 ms, no scaling at all). The factor build was the same
defect as the one just fixed, one layer up: `upgrade_householder_factor`'s flat branch computes
`T = diag(tau) + strict_upper(V^H V)`, and its second product reduces over every row below the
basis' diagonal with an `n x n` output -- one serial kernel per task, measured at 0.271 ms for
`m = 4096, n = 16` at eight threads.

**The fix.** `tensor4all/faer#6` splits that reduction's rows as well. Unlike the block apply's, it
needs no depth-against-width gate: its partials are `n x n` each and only the strict upper triangle is
stored (the diagonal is the caller's `tau`), so the split costs almost nothing at any size -- 6.7x at
`m = 4096, n = 16`, 7.4x at `m = 8192`, 4.6x at `m = 1024`, and 3.0x at `m = 512`, where the previous
gate would have refused it. `tensor4all/tlinalg-rs#50` consumes it.

**What the record says.** Both arms were re-recorded from scratch at `e6ee2d3`, one complete set
each, and both cells read `full` and `current`. Medians of `after / before` over each regime's cells,
against the four vendor rows of the two pairs as the floor (unchanged binaries, ~490 cells each):

| rows | `small` | `medium` | `large` | `tall` | vendor floor |
|---|---|---|---|---|---|
| `faer-1lane` at 1T | 1.005 | 1.004 | 1.001 | 0.999 | 1.001 / 1.000, p10-p90 0.987-1.021 |
| `faer-pool` at 8T | 1.003 | 1.001 | 0.993 | **0.857** (p10 0.815) | 1.002 / 1.000, p10-p90 0.983-1.023 |

The change is wider than the cell it was aimed at, because every blocked QR path builds this factor:
at 8T, `householder_factor` 4096x256 b1 c64 16.05 -> **13.35 ms** (f64 5.63 -> 4.90), `qr` c64
42.76 -> **36.87**, `rank_revealing_qr` c64 52.06 -> 44.78, `svd_thin` c64 84.77 -> 76.34 and f64
34.38 -> **26.89**; and the `large` and `1024x64` cells improve with them (`householder_factor`
512x512 b1 c64 4.49 -> 4.17, f64 1.75 -> 1.62, 256x256 c64 0.98 -> 0.92, `householder_apply`
256x256 f64 1.71 -> 1.43). Every 1T row is unchanged, and the families that do not build a
compact-WY factor (`lu_*`, `cholesky`, `eigh*`, `svd_values`, `triangular_solve`) are within the
floor.

**Where this leaves the family that started it.** `householder_factor` 4096x256 b1 was 10.2x behind
OpenBLAS at 8T when this campaign first recorded it, 1.55x after the blocking, and is now **1.08x**
in c64 and **0.46x** in f64, i.e. 2.2x faster than OpenBLAS. `svd_thin` f64 is 0.72x. The tall c64
cells that still lose are `qr` (1.43x OpenBLAS, 1.23x MKL) and `rank_revealing_qr`, which do not go
through tlinalg's kernels at all: they call faer's own blocked QR.

**What remains.** The panel: about 5 ms of that cell's 13.4, and it stops scaling at four threads
because its grain is one reflector (a `4096 x 15` rank-one update), where OpenBLAS's `?gemv`/`?geru`
pair reaches 2.3x on the same cores against faer's 1.17x. That is two halves -- the unblocked panel
is tlinalg's structure, the fine-grain dispatch is faer's (its per-call task spawn, the "thread
policy" row of the fork's ledger) -- and the fork's `PATCHSET.md` carries it as the open item, with
the phase split and the isolation numbers.

## 2026-10-13 — the fork's block apply splits the reduction's rows, gated on the reduction's shape; both arms re-recorded at `6180fb0`

**What the previous record left.** With the rank-one apply fixed, the tall c64 cells were still behind
OpenBLAS. Isolating the three steps of the trailing compact-WY update on the shapes the kernels see
settled which one it was, and it was not the one assumed: `tmp = V^H C` -- an `N x K` output reduced
over every row of a long target -- was 2.03 ms at 8T where OpenBLAS's `?gemm` on the same shape is
0.53-0.71, while the other two were already fine or better (`C -= V tmp` 0.67 ms against
OpenBLAS's 1.25-1.40, the solve 0.01 in both). The column split that faer's generic path uses caps at
`min(par, K, 4)` and cannot use the depth, and inside one column task that reduction ran as one
serial kernel.

**The fix, two changes and one gate.** `tensor4all/faer#4` splits the rows of that reduction when the
call is threaded and the target is tall: one `N x K` partial per thread, then the partials added.
`tensor4all/faer#5` then gated it, because the first record of #4 showed what an ungated split costs
-- `householder_factor` and `householder_apply` at 512x512 lost 4-6% at 8T. Splitting the reduction's
rows is a split along the depth, and the split itself adds `threads` partials of `N x K` to write,
read and add, so it pays only while the serial kernel it replaces is depth-bound. A sweep of the
reduction alone over `M` against `K` at eight threads puts the crossover at `M ~ 2 K`: at
`M = 4096, K = 240` it is 3.7x (2.04 -> 0.55 ms), and at `M = 512, K = 496` -- the 512x512 trailing
update -- it is 0.14 -> 0.26. The gate is that one shape inequality plus a thread floor and a work
floor. `tensor4all/tlinalg-rs#48` and `#49` consume the two revisions in turn.

**What the record says.** Both arms were re-recorded from scratch at `6180fb0`, one complete set
each, and both cells read `full` and `current`. Medians of `after / before` over each regime's cells,
against the four vendor rows of the two pairs as the floor (unchanged binaries, ~490 cells each):

| rows | `small` | `medium` | `large` | `tall` | vendor floor |
|---|---|---|---|---|---|
| `faer-1lane` at 1T | 1.000 | 0.997 | 1.001 | 1.000 | 1.000, p10-p90 0.984-1.014 |
| `faer-pool` at 8T | 0.996 | 1.000 | 1.001 | 0.990 | 1.000, p10-p90 0.980-1.019 |

The cells the row split serves, and the cells the gate protects, at 8T:

| cell | before | after | OpenBLAS | MKL |
|---|---|---|---|---|
| `householder_factor` 4096x256 b1 c64 | 17.04 | **16.05** | 12.50 (1.28x) | 11.11 (1.44x) |
| `householder_factor` 4096x256 b1 f64 | 5.96 | **5.63** | 10.95 (0.51x) | 3.74 (1.50x) |
| `qr` 4096x256 b1 c64 | 46.33 | **42.76** | 25.57 (1.67x) | 29.81 (1.43x) |
| `householder_factor` 512x512 b1 c64 | 4.47 | 4.49 (+0.5%) | 6.49 (0.69x) | 3.42 (1.31x) |
| `householder_factor` 512x512 b1 f64 | 1.72 | 1.75 (+1.3%) | 4.07 (0.43x) | 1.30 (1.34x) |
| `qr` 512x512 b1 c64 | 12.54 | 12.55 | 13.24 (0.95x) | 9.40 (1.34x) |

Every 512x512 and 256x256 cell of the two householder families is within 3% of the previous record
and mostly within 1% -- the ungated split's 4-6% cost is gone -- while the tall cells keep 5-8%. Every
1T row is unchanged, which is the check that the split is only taken when the call is threaded.
`svd_thin` c64 at 4096x256 reads 76.95 -> 84.77 here, which is the one cell that moves the wrong way
and is inside the tall pooled spread rather than attributable: the same cell read 85.02 at `6a873e6`,
76.95 at `5cb2430` and 85.06 in the unrecorded ungated run, and the isolated reduction it depends on
is 3.7x faster.

**How this class is prevented generally, which is the part worth keeping.** There is no version of a
split-K decision without constants -- OpenBLAS and MKL both carry measured crossovers per kernel and
architecture -- so "general" cannot mean "no numbers". It means (a) the decision is *one* inequality
in the shape with a name that says what it is (depth against width, plus a work quantum and a thread
floor), not a growing table of remembered shapes; (b) the constant comes from a sweep across the
crossover (the table above) rather than from the cell that regressed; and (c) something *spans* the
crossover so a wrong constant cannot pass unnoticed -- which is this grid, where `large` is `M ~ K`
and is exactly how the 4-6% showed up before it was published. The overhead itself could also be made
sub-linear in the thread count (a tree combine, and no zero fill of the partials) instead of being
thresholded away; that changes the scratch story, so it is an open item rather than part of this.

**What remains.** The `?larfb` trio is now within reach of the vendors' on the tall shape: faer's
apply 2.42 ms at 8T against OpenBLAS's 1.83-2.14 before this change, and its two halves are 0.55 and
0.67 against the vendors' 0.53-0.71 and 1.25-1.40. `householder_factor` tall c64 is 1.28x OpenBLAS and
1.44x MKL, `qr` tall c64 1.67x OpenBLAS, and the rest of the tall family is in the same range; the
remaining gap is the serial panel and the compact-WY factor build, which no vendor row exposes
separately and which the `faer#5` ledger row leaves as "the scratch story" item.

## 2026-10-12 (later) — the fork's rank-one apply now honors `par`; both arms re-recorded at `5cb2430`

**What the previous record left.** The tall c64 cells were the one place the blocked pair still lost
(`householder_factor` 4096x256 b1 at 8T, 1.55x behind OpenBLAS). Separating that call into its phases
showed the pooled row was 43% serial work -- the panel and the compact-WY factor, both linear in the
block width -- and 57% a level-3 trailing update that reaches only 3.5x on eight threads. Isolating
the vendors' own kernels settled which of the two was fixable: on the same cores, OpenBLAS's
level-2 panel (`?gemv`/`?geru`, which is what a blocked QR's panel is) goes 5.97 ms at 1T to 2.58 ms
at 8T, MKL's does not move at all (6.97 throughout), and faer's was 5.96 to 6.31 -- at parity at 1T
and **no threading at all** at 8T. `?larfb` itself was not the deficit: the vendor trio on the same
shapes is 1.83-2.14 ms at 8T against faer's 2.45.

**The cause and the fix.** The `N == 1` arm of `apply_block_householder_on_the_left_in_place_generic`
is one sequential rank-one update per target column -- its SIMD kernel -- and it never reads `par`.
In `tensor4all/faer#3` (merged as `4f69133`) that arm is skipped when the caller asks for threads and
the update is at least 8192 elements, so the generic path takes it: that path partitions the target's
columns and threads its two products. `tensor4all/tlinalg-rs#47` moves the dependency to that
revision; nothing else in this campaign changed. No OpenBLAS or MKL source was used or adapted -- the
vendors' timings are the target, not the code -- and the fork's `PATCHSET.md` says so.

**What the record moved.** Both arms were re-recorded from scratch, one complete set each, and both
cells read `full` and `current`. Medians of `after / before` over each regime's cells, with the four
vendor rows of the two pairs as the floor (unchanged binaries, so they measure the machine):

| rows | `small` | `medium` | `large` | `tall` | vendor floor (1T / 8T) |
|---|---|---|---|---|---|
| `faer-1lane` at 1T | 0.993 | 0.999 | 0.998 | 1.003 | 1.000 / 1.000, p10-p90 0.988-1.014 |
| `faer-pool` at 8T | 1.001 | 1.002 | 0.999 | 0.992 | 1.000 / 1.000, p10-p90 0.980-1.021 |

Inside that floor the change is where it was aimed and nowhere else: at 8T, `householder_factor`
4096x256 b1 is 6.73 -> 5.96 ms in f64 (`-11.5%`) and 19.31 -> 17.04 in c64 (`-11.8%`), with
`svd_thin` c64 85.02 -> 76.95 (`-9.5%`) as a side effect of the same arm; the 1T rows of those cells
do not move (14.14 -> 14.18 and 53.91 -> 55.10, within the floor), which is the check that the arm is
only skipped when the call is threaded. The pooled c64 cell now reads 1.36x OpenBLAS (was 1.55x) and
1.54x MKL; the f64 cell reads 0.53x OpenBLAS, i.e. 1.9x faster than it. `svd_thin` f64 at 8T moved
the other way (32.55 -> 34.76, `+6.8%`), which is inside the tall pooled spread rather than a
regression this change can explain: the arm it touches is the rank-one apply, and that row's 1T
sibling is unchanged.

**What remains.** The trailing update. It is 57% of that call at 8T and its own parallel ceiling is
3.5-3.9x -- measured in isolation, faer's own threading reaches 3.56x and a hand-rolled split of its
target columns 3.87x, so the ceiling is the kernel on a DRAM-bound tall panel, not the decomposition.
The eight threads of the `8T` cell are eight physical Zen 5c cores sharing 8 MiB of L3, and a
4096 x 240 c64 target is 16.8 MB. That is still the open item, and it is now the *only* one: with
this record, the tall c64 `householder_factor` cell is the last place any faer row loses to OpenBLAS
on this profile.

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

**What the remaining tall gap is made of.** The pooled c64 tall cells are the one place the pair
still loses, and it is worth recording where the time goes rather than calling it "faer's GEMM" and
leaving it. Measured on this host at `6a873e6` with the blocked path's three phases separated by
running the same call with the trailing update and then the whole block update switched off, for
`householder_factor` 4096x256 b1 c64 (block 16):

| phase | 1T | 8T pool | scaling | share of 8T |
|---|---|---|---|---|
| panel (16 reflectors against the panel, level-2) | 5.96 | 6.31 | 0.94x | 28% |
| compact-WY factor `T` (level-3, 16x16 output) | 2.57 | 3.57 | 0.72x | 16% |
| trailing block apply (level-3, 4096 x <=240 target) | 45.3 | 13.0 | 3.5x | 57% |
| whole call | 53.8 | 22.9 | 2.4x | |

So the pooled row is 43% *serial* work that is linear in the block width, and the remaining 57% is a
level-3 update that only reaches 3.5x on eight threads. Isolated, that update is 8.72 ms at 1T and
2.45 ms under faer's own eight-thread budget (3.56x); splitting its target columns ourselves into
four two-thread calls gives 2.27 ms and into eight single-thread calls 2.25 ms -- 3.87x, which is
where a caller-side split saturates. The eight threads of the `8T` cell are eight *physical* Zen 5c
cores (CPUs 4-11, `core_id` 8-15) sharing 8 MiB of L3, and a 4096 x 240 c64 target is 16.8 MB, so
that update is DRAM-bound and the ceiling is the kernel's packing, not the parallel decomposition.
OpenBLAS reaches 5.5x on the same cores for the same factorization, and its rows are the evidence.

Three tlinalg-side levers were measured and rejected: a block of 8 instead of 16 gains 5% on this
shape at 8T and loses 12% at 1T (the grid has both); one level of panel blocking (leaf of 8 columns
at block 16) gains 5% on tall and loses 6% on 512x512 at 8T; and handing `upgrade_householder_factor`
`Par::Seq` rather than the row's budget is a wash (2.57 against 3.57 ms is a differencing artefact of
the same noise the whole-call A/B does not reproduce). None of them is worth the churn, so the tall
c64 cells stay as they are: `householder_factor` 4096x256 b1 c64 reads 0.78x OpenBLAS at 1T, 1.07x at
4T and 1.55x at 8T, while its f64 sibling leads at every budget and every other family's tall c64
rows are inside 1.6x. The shape and the phase split are the reproducer if this is ever pursued
upstream in faer.

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
