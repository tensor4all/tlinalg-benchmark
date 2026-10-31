# 2026-10-31 zen5-cpu publication recovery

This is the normal periodic publication at frozen library/pin
`53d1f0d9f44378596c4f2bce932e45cc961b0d78`, using the campaign-pinned toolkit
`b71624bef111ce941bddaedcce3fdb6eab40f9eb`. No library, suite, CPU-set, timing-policy,
or driver source was changed. Existing weekly records were not relabelled.

## MKL was reused, NOT remeasured

The first official-driver invocation completed competition-MKL, then refused to start
OpenBLAS because the observer audit found `herdr` using the measured L3 domain.
That refusal, not a measurement/verification failure, stopped the invocation.

**The completed MKL arm was not remeasured. Its existing 51-file evidence was reused.**
All 51 original files remained byte-identical in the original checkout throughout recovery.
The [preserved SHA256 ledger](2026-10-31-mkl-preserved.sha256.json) records that snapshot.
The 49 raw/report/page files in this publication match those original hashes exactly.
The other two original files are `result/INDEX.md` and `result/HISTORY.md`: their original
copies were preserved too; the final aggregate indexes were regenerated in a separate
working copy to include the two newly completed runs. The snapshot hashes for these two
files therefore describe the preserved originals, not the final aggregate indexes.

## Remaining stages and validity

After explicit recovery approval, every `herdr` thread was confined to observer CPUs
`0-3,12-15`. The measured budget remained eight physical cores, CPUs `4-11`, with the
whole measured L3/SMT domain `4-11,16-23` kept free of observers.
A clean working copy used the official driver's existing `root`, `record`, and `publish`
plan fields. The recipe was mechanically filtered only from `for vendor in mkl openblas`
to `for vendor in openblas`; all record commands/options otherwise remained unchanged.
Only **OpenBLAS, then scaling** ran in recovery. No resume feature was added to the driver.

Retained publication runs:
- MKL (reused): `20261031T121942Z-pub-53d1f0d9-20261031-competition-mkl`.
- OpenBLAS: `20261031T125207Z-pub-53d1f0d9-20261031-competition-openblas`.
- Scaling: `20261031T131253Z-pub-53d1f0d9-20261031-scaling`.

The initial invocation took 1217.55 s; recovery took 2497.11 s, including driver overhead.
All three runs have full declared coverage, clean pin-matching libraries, aa4/reps5,
250 ms priming, timing-v2 chronological samples and median validation. All 60 guard logs
passed on attempt 1, with no measurement rejection/retry. All recorded verification
census rows are `ok`; the common faer-pool verification census/statuses match across all
three runs. No contradictory MKL bytes/numbers or failing protocol gate was found.
Report regeneration and all campaign-local CI-equivalent content gates passed before handoff.

APU GPU use was 0% in `rocm-smi` before/after both invocations; all 1217 + 2495 one-second
sysfs samples were 0%. The initial observer-audit refusal is retained in the operator
state at `~/.local/state/tensor4all-publication/20261031T105951Z/tlinalg/publish.log`.
No data was deleted, no root privilege or paid service was used, and today's tenferro
work remained on hold and was not touched.

Execution: pi 1.0.4 / openai/gpt-6.1-sol. This note does not claim cross-vendor equality
of performance timings; it records protocol validity, numerical verification outcomes,
and exact reuse of the original MKL evidence.
