# Reproduce CHECK050

Environment used: Python 3.14.4, NumPy 2.3.5, SciPy 1.17.1, Matplotlib 3.11.0. These are measured installed versions, not installation recommendations.

Use a new working directory containing the checker Python files and the unchanged `owner-data`, `inputs`, `brief`, `clarifications` and `sources` directories. Copy the metadata inputs `START.json`, `ORDER.json`, `BRIEF-PINS.json`, `OWNER-DATA-PINS.json`, `UPSTREAM-PINS.json` and `REFINEMENT-TARGETS.json`. Do not copy generated `CHECKED-*` files into a fresh numerical reproduction: the table runner intentionally resumes completed radii.

Run these checker entry points in order. Every command uses the same admission wrapper:

```text
python unpublished-local-ref:6b66f99ebd630954 run --cores 1 --mem 2G -- python <entry-point>
```

1. `check_initial.py`
2. `check_tables.py`
3. `check_days_frozen.py`
4. `check_fixed.py`
5. `check_dew.py`
6. `check_accounts.py`
7. `check_gas.py`
8. `refine_interface.py`
9. `finish_checks.py`

The scripts resolve data relative to their own directory. They import only checker-authored modules and installed numerical libraries, never the owner's executable source. The preserved owner data include comparison answers; the independent models take equations/material inputs and supplied grid axes, then calculate their own states and optima. The broad gas sweep uses supplied finite geometries as inputs and is labelled separately from the owner's scalar sample.

The first filing's `days-frozen-run.log` retains a corrected checker-reader error after all design days had already been saved. `frozen-run.log` records the successful separate frozen-table run. The shipped script has the corrected dictionary access and can run both stages directly.

`refine_interface.py` replays the explicitly selected 1500-point boundary refinements. Its extra marginal-root results remain outside the conservative weather-map domain. `finish_checks.py` rebuilds missing grids, checks all transition/slice records, assembles the exact comparison ledgers and draws the figure if absent.

Logs, manifest hashes and native identity are historical receipts and are not expected to reproduce byte-for-byte. Model comparisons should preserve the displayed numerical conclusions and exact mask classifications within the documented floating-point/optimization tolerances.
