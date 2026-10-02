# fixtures — the 2026-10-01 capture, trimmed

Every file here is a trimmed copy of a raw response in the dated capture the stop-gap
script made on 2026-10-01, so the tests replay the exact shapes the real service returns
without asking it for anything. `check.py` serves these from a fixture server on 127.0.0.1.

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
