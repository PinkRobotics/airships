# The evacuation fixtures

`hand-capture/` is a trimmed copy of the one real capture of the province's public evacuation
layer (taken 2026-10-02T07:08:47Z, 16 features; the raw original lives outside the repository
at `inputs/evac-capture/`, untracked). It exists so this gate can prove the derived record
regenerates from a captured day without the raw inputs.

What was kept and what was dropped, deliberately:

- every one of the 16 features, with the properties the reader reads
  (`OBJECTID`, `EVENT_TYPE`, `EVENT_NUMBER`, `ORDER_ALERT_STATUS`, `DATE_MODIFIED`,
  `EVENT_START_DATE`) and **geometry only for the five fire-order features** — the only
  geometry the derivation reads. Alert and non-fire features carry `geometry: null`.
- the layer's counts of homes and population, the issuing agency, and every free-text name
  are dropped here exactly as they are dropped by the derivation: they are published in no
  file this repository carries, fixture or not.
- `evac.layer.json` is the layer definition trimmed to the same fields plus the
  `dateFieldsTimeReference` marker the reader requires; `MANIFEST.json` is the hand-captured
  shape (flat: `base`, `count`, `fetched`, `requests` with true sha256s of the files here).

`expected/` is the pair `pipeline/season.py` builds from `hand-capture/`
(`build_evac_files(2026, evac_facts([read_evac_capture(hand-capture)]))`), committed so the
regeneration is compared against pinned bytes. Its `fires` and `counts` are the committed
`data/season/2026.evac.json`'s own — the fixture is the real capture's shape, so the same
facts come out — and its `days[0]` differs only in the manifest and file hashes, which name
these fixture files rather than the raw ones.

Nothing here was fetched: the fixture is a local trim of the capture the lead took.
