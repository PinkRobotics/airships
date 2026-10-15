# Server-side feed mirror — RETIRED

The mirror stopped on 2026-10-14, by the operator's ruling: this site no longer queries
the BC Wildfire Service feeds, satellite heat or forecast wind, live or mirrored. Every
view the page shows is a replay of the published record under `data/season/`, and the
browser reads only files this repository itself serves.

Nothing here was ever committed: the generated files (`fires.json`, `perims.json`,
`heat.json`, `wind.json`) were gitignored and excluded from publication. Any copy still
sitting on a server is a historical artifact of the retired service, not a live input;
the host timers that wrote them are disabled and are deliberately left in place.

`pipeline/live.py` remains in the tree as the capture pipeline of record: it is how the
dated season days were taken, and `tests/season/check.py` still pins the day files'
fields against it. It is not run by anything.

The browser still never contacts an agency or forecast provider. See `pipeline/README.md`
for the retired operator configuration and `DATA-SOURCES.md` for attribution and API
terms.
