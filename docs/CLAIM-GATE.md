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

Motion vocabulary lives in `tools/float_text.py`. It applies to prose, including
Markdown and generated text, while style and script code remain outside that rule.
Existing display-string checks retain their coverage.

A plain `python3 tools/update_float_records.py` refresh preserves existing dated
freezes. A new dated verdict block requires an explicit `entries` decision in
`tools/float_dispositions.json`, identifying its file and text hash, with class
`history`, the file date and a reviewed reason. This is the same catalogue used
for reviewed live replacements; dated history still cannot be replaced.
The writer names any new block requiring review before it writes records.

`tools/review_gate_motion.py` replays the reviewed decisions for the widened
inventory. Run it, then run `tools/update_float_records.py` twice and verify that
the second run changes no record bytes. These scripts are intentional maintenance
steps, never gate prerequisites.
