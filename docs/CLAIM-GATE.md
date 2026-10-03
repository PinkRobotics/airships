# Claim gate maintenance

Changes to the gate tools (`tools/check_float_ledger.py`, `tools/float_text.py`,
`tools/float_claims.py`, `tools/float_regions.py`, `tools/float_qualifiers.py`,
`tools/update_float_records.py`), record schema or plants must run
`make floatplants` before hand-up.

`make ledgercheck-selftest`, included in `make check`, runs the record contracts,
one plant per finding class and all controls. The complete suite runs separately
as `make floatplants`, including on every push and pull request in CI.

Cases use independent temporary copies. `FLOAT_PLANT_WORKERS` selects a positive
worker count, capped at eight; its default is the CPU count capped at eight.
Reports retain whole command output per case in a fixed registration order.
