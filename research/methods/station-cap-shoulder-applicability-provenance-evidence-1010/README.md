# Station-aware cap and shoulder applicability provenance

[Station-aware cap and shoulder checks](../../../docs/OPEN-QUESTIONS.md#station-aware-cap-and-shoulder-checks) asks what would resolve station radius, member length, connection stiffness and transfer across each shoulder, and which analysis and physical measurements would establish applicability of a replacement check. This paper preserves those unresolved questions and the billed-versus-drawn discrepancy. No replacement check, load case, geometry, section, material, criterion or physical procedure is chosen.

The [member census](../../../docs/MEMBER-CENSUS.md) says the current checks use smeared areas at full radius and do not resolve station lengths, sections or connections. Rendering segments are not physical member counts. Source prices use unchanged sections and allowances without resizing or checking those sections. Generated representation/accounting measurements are not observed physical structure or proof that a check applies to a real configuration.

[CROSSWALK.json](CROSSWALK.json) explicitly preserves source identities without copying numerical lengths, counts, masses, margins or safety factors:

| Source counterpart | Unresolved applicability boundary |
|---|---|
| innerRings / hoopsInner | Barrel/cap family correspondence lacks actual station/section evidence. |
| junctionShear / junctions | Shoulder section is inferred from the smeared bill, not a measured connection. |
| longerons / longs | Barrel/shoulder overlap identifies a region, not actual transfer or complete inventory. |
| capGrid | Area allowance has no explicit drawing topology or complete allocation. |
| cap-hoops / cap-bars | Drawn families lack station-mapped bill counterparts. |
| Section families | Inner-ring, fan, theta and junction display sections are schematic. |
| Fitting symbols | Close-up clamp/joint depiction is not a whole-hull connection census. |
| tiJoints | Separate joint allowance and patch-only counterpart remain unallocated. |

The source inner-ring and shoulder-diagonal discrepancies and separate joint allowance remain authoritative, with every numeric operand left in the unchanged source. No billed/drawn length sum, price, mass, load, stiffness, strength or margin is recomputed. A source comparison cannot silently fill missing stations, actual sections, physical connection population or transfer paths. Unknown mass is not zero.

Prospective applicability records would need exact source/domain/revision and station/member/connection/shoulder/section/boundary identities, original unit/frame and inclusion/exclusion conventions, applicable matched actual configuration and source observation records, calibration, uncertainty, raw custody and responsible criterion/check adoption provenance. Missing or incomparable coverage must remain visible before interpreting a representation as an actual structure. The requirement rows map station radius, member length/sections, connection stiffness, shoulder transfer and replacement-check applicability separately.

Actual configuration, station/member/connection/shoulder/section/boundary records, raw and matched comparison records, calibration, uncertainty, applicability, assigned owners, adopted criteria and replacement check remain NULL/UNKNOWN. Role names are proposals only, UNASSIGNED. [PROVENANCE.json](PROVENANCE.json) pins the authoritative inputs to the baseline revision and declares one-based line/character starts with exclusive character ends for the fragment locators.

StageB cell/joint installation geometry, P16 collapse, P45 assumed cord stiffness, Q11 mass accounting, rim bending, sag-volume and reserve inclusion remain separate. This paper concerns only the published station/shoulder transfer comparison provenance. Existing source/model/schema/catalogue/code/test/data remain unchanged. No code, viewer, model, fixture, generator or solver is run; no actual coordinates, stiffness, loading, section, measurements or scientific results are invented. The root README says no aircraft has been built or flown; a representation or passing software check cannot establish physical applicability, feasibility, benefit, qualification or safety.
