# Closed Q17 flag correction versus measured wind/bearing input provenance

[Q17](../../../docs/OPEN-QUESTIONS.md#17-windused-requires-a-route-bearing) remains CLOSED, with its published closure date preserved as source metadata in CROSSWALK.json. The returned flag correction and ordinary regression establish a software input-contract distinction. They supply no measured meteorology, actual route bearing, flight, performance or physical qualification. This paper neither reopens the fixed bug nor changes its code or tests.

The current [plan](../../../sim/plan.js) delegates trackWind and windBasis to the imported [wind helper](../../../sim/wind.js). The helper checks non-null wind and non-null bearing, rather than bearing truthiness, and separately guards finite used-vector speed, direction and bearing. The presence flag can remain true for valid zero speed; it describes input use rather than measured wind magnitude or quality. The published historical speed-and-bearing wording remains unchanged, while this paper pins the current implementation and delegation.

The existing [regression case](../../../tests/cases/sim-plan.cases.js) distinguishes null and missing bearings from a valid zero-degree bearing. Missing is not zero; zero is not missing. CROSSWALK.json records these source categories and expected Boolean flags without copying the numerical fixture inputs, projecting a vector or executing the fixture. The earlier numerical reproduction stays only in the unchanged source.

| Evidence boundary | Required distinction |
|---|---|
| Closed correction | Software regression closure differs from physical or meteorological evidence. |
| Bearing presence | Null/missing input differs from valid zero, without choosing a bearing. |
| Current source contract | Plan delegation and helper validity differ from the historical code location. |
| Frame and angle | Source angular convention differs from actual geographic/frame provenance. |
| Wind and bearing records | A model input/basis label differs from an acquired applicable record. |
| Interval and calibration | Actual observations, uncertainty and comparisons remain unsupplied. |
| Custody and criterion | Responsible record custody and adopted physical criteria remain unknown. |

The helper's source transformation reverses direction before route-bearing comparison and uses angular conversion. That is a model convention, not proof of actual geographic, true/magnetic or meteorological reference provenance. Its basis label describes a pressure-level vector and straight legs, with shear, turns, gusts and vertical air motion outside that basis. No selected angle, direction, route, site, observation period, forecast or schedule is supplied here.

Prospective evidence would need original wind/bearing/source/configuration records, source-declared speed and angular units/orientation/frame/reference provenance, actual observation intervals, and applicable acquisition/calibration/uncertainty and comparison records. The source input-field identities are metadata; they supply no actual values. Missing or incomparable records remain visible before any interpretation. Gust structural loads, Q3 dynamics, Q18 atmosphere and generic mission timebase work remain separate.

[CROSSWALK.json](CROSSWALK.json) retains CLOSED metadata and prospective custodian roles. Actual wind/bearing inputs, configuration/frame/convention, observation interval/records, comparisons, calibration, uncertainty, assigned owners and adopted acceptance criteria are NULL/UNKNOWN. Roles are UNASSIGNED. [PROVENANCE.json](PROVENANCE.json) pins the authoritative inputs and the read-only imported helper to the baseline revision.

This paper performs no fixture execution, simulation, solver, physical action, measurement, wind projection, groundspeed/performance or uncertainty computation. It changes no code, model, test, schema, source or remote issue and provides no route/navigation/weather/operating guidance, forecast or external lookup. The root README says no aircraft has been built or flown; a repository check and a CLOSED flag correction supply no missing physical evidence or safety/benefit claim.
