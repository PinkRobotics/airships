# fixtures — the 2026-10-01 fire capture and the 2026-10-02 evacuation capture, trimmed

Every file here is a trimmed copy of a raw response the stop-gap captured, so the tests
replay the exact shapes the real service returns without asking it for anything.
`check.py` serves these from a fixture server on 127.0.0.1.

The two fire layers (`incidents.*`, `perimeters.*`) are trimmed from the dated capture
of 2026-10-01; the evacuation layer (`evacuations.*`) is trimmed from the hand capture of
the public evacuation layer taken 2026-10-02T07:08:47Z (16 features, one page). The two
days are mixed in one fixture set because the capture tool treats every layer the same
way and cares only about each layer's own shape.

What was kept and what was adjusted:

- **Features are real.** Incidents OBJECTIDs 1, 2, 178, 1069, 1071 and perimeters OBJECTIDs
  1, 14, 28 are real features from that day's pages, chosen to include four of the five
  statuses ("Out" twice plus "Under Control", "Out of Control" and "Being Held" once each).
  Attribute values are unaltered; the attribute set is trimmed to the fields the layer
  descriptions here still declare.
- **`incidents.layer.json` has `maxRecordCount: 3`** (the real layer says 1000). Five
  features at three per page is still a two-page capture, so paging is exercised by a
  fixture of under 2 kB. `perimeters.layer.json` keeps the real 1000, so three features
  fit on one page, exactly as they did on the real day.
- **Counts were adjusted to match the trimmed feature sets**: incidents count 5 (3 + 2),
  perimeters count 3, and each `by-status` tally sums to its count using the statuses the
  kept features actually carry.
- **Perimeter geometries are synthetic.** Real perimeter rings run to tens of thousands of
  points; each kept feature carries a tiny closed triangle at roughly the real fire's
  location instead. Incident geometries (points) are the real coordinates.
- **Page shape is the real one**: page-000 of a multi-page layer carries
  `properties.exceededTransferLimit: true` and the last page carries no `properties` at
  all, which is what the service actually did on 2026-10-01.

The evacuation layer (`evacuations.*`), trimmed from the 2026-10-02 capture:

- **All 16 features are real, with their `OBJECTID`, `EVENT_TYPE`, `EVENT_NUMBER`,
  `ORDER_ALERT_STATUS`, `DATE_MODIFIED` and `EVENT_START_DATE` values unaltered.** Six
  are fire events (by number: one alert-only, one order-and-alert, three order-only with
  multiple order features or multi-patch areas); ten are landslide and flood events with
  no fire number.
- **Geometry is kept for exactly two features** — `OBJECTID` 8 (a fire order whose 35
  rings are many small disjoint patches) and 9 (a fire alert whose first ring is one
  patch of fourteen) — so the multi-patch shape the layer really serves is exercised.
  Every other feature carries `geometry: null`.
- **The homes-count, population-count, issuing-agency, order-name, centre-code and
  internal-id attributes were removed**, and with them the event's free-text name (which
  carries road addresses and community names). The capture tool does not read them; the
  derivation that runs on the capture (pipeline/season.py) is barred from publishing
  them, and a fixture that carried them would put them in this repository.
- **`evacuations.layer.json` keeps the real `maxRecordCount` (1000) and the real
  `copyrightText` (empty)**, with the field list trimmed to the six attributes above; the
  count file is the captured bytes, unmodified (16).
