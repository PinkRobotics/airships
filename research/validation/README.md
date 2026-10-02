# Labelled comparisons

Run with Python 3 and Node 22:

    make labelledcheck
    python3 -B research/validation/check.py --update
    python3 -B research/validation/check.py --schema-only
    python3 -B -m unittest discover -s research/validation -p 'test_*.py' -v
    node --test research/validation/test_lift.mjs

Set TMPDIR to an explicit writable scratch directory before tests. The checker imports actual
project functions; its adapter follows stamped dependencies so it changes the model's actual
configuration singleton. It does not fetch references or emergency feeds. The default target
regenerates JSON and Markdown in memory and compares bytes. A broken model, schema failure or
stale report fails. A numerical MISS or failed bound remains published and is not a gate error.

The original 35 source records and their printed digits are retained, including record 6's
excluded gas-constant exponent. One primary hover-flight-test record was added as record 35;
[hover-search.md](hover-search.md) records the search, successful and failed retrievals, and
selection of the point before its comparison. `schema.py` checks source coverage, normalized
shapes, short quotations and public-safe text. The same public-text check guards generated output.
The reference conventions follow [the research guide](../README.md); the local atmosphere and
shell papers retain their catalogue, document and provenance links in the report JSON.

Order 9c adds callable gas-state questions without changing the old class lift or helium ledger.
`sim/physics.js:grossLiftKg` is the implementation used by `ledger`; optional calibrated air
density preserves the existing density dial and bit-level arithmetic. Helium's `gas_density`
and `net_lift` are also used by its unchanged-output main program. CL-415 compares only the
cruise-speed quotient and scoop replay; climb-out, circuit and drop run are unmapped. The hover
comparison calls public `diskMW`, with its efficiency unchanged, at the primary XH-59A state.
The CH-47D ratings and Zeppelin static capacity remain inequalities, not measurements of lift
or hover power. Re-run after the energy-model worker's changes.

[The shell reproduction note](../analysis/reproductions.md) distinguishes paper terms from
project primitives. A literal sandwich mass calculation can miss; the miss is retained.
Jenett's local member sizing runs, but Table 2 stays not comparable because its member inventory
and geometry/end-condition conventions are not fully specified. No constant is fitted.

Every order-9b tolerance is unchanged. The `order_9c_before_first_comparison` section was written
before implementing or evaluating any new comparison, including the 5% hover screen before
selecting the flight-test point. A bound uses its stated inequality and allowance; it never
becomes agreement simply because its numbers happen to be close.

`test_check.py` perturbs reference inputs and actual model functions in disposable copies, runs
the real Make target, verifies changed numerical rows/diagnostics, restores and proves green.
`test_apis.py` exercises state behavior and both directions of inequalities. `test_lift.mjs`
compares complete ledgers with the previous arithmetic over the altitude/density domain.

For the unlanded constant counterfactual, run:

    python3 -B research/validation/constant_study.py --out "$TMPDIR/constant-study.json"

This takes two disposable copies of HEAD, regenerates the published figures, six analyses,
skin outputs and the original validation report, and lists every changed field. Only those
copies unify dry-air R to the 1976 prose constant divided by the dry-air molar mass. Existing
density dials and gas-specific constants stay unchanged. Its output includes any baseline
regeneration drift, so pre-existing cache differences cannot be mistaken for constant effects.
It serves bundled snapshot data on loopback, starts its own browser, and never runs `make stamp`.
