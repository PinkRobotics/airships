# Atmosphere constant and altitude-contract evidence

This prospective map follows [question 18](../../../docs/OPEN-QUESTIONS.md#18-three-atmosphere-implementations-that-do-not-agree-to-the-last-digit) and existing [issue 16](https://github.com/PinkRobotics/airships/issues/16), recorded in the [local filed-issue table](../../program/OPEN-QUESTION-ISSUES.md#filed-issues--2026-10-09). Its current remote state is not checked or changed.

The existing implementations are [the browser atmosphere](../../../sim/atmosphere.js), [vacuum-cell analysis](../../analysis/vacuum-cell.py) and [helium analysis](../../analysis/helium.py). Their dry-air constants differ, and all apply the geopotential lapse directly. The browser interface describes metres above mean sea level, including its inverse density interface, without a geometric conversion. That label alone does not settle the geometric versus geopotential contract.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) traces the existing functions and copies the already-published atmosphere rows, mutual comparisons, source table records and frozen tolerances without executing the implementations. These are historical source values. The [existing report](../../validation/report.md#air-density-with-altitude) retains its aggregate MISS and the failed mutual-parity comparisons. Agreement with a coarser printed table and agreement between implementations at roundoff are separate decisions. No row or verdict moves here.

The [reference records](../../validation/sources.json) preserve printed digits, units, locators, defining-model limitations and excluded source errors. The [tolerances](../../validation/tolerances.json) were set before the first model run; their printed-precision and roundoff limits are comparison policies, not physical measurement uncertainty. The standard atmosphere is stipulated; it does not observe weather. The recorded geometric-row contrast remains source context, and a rounded geometric table column is not a conversion algorithm.

Every prospective observation, evidence identifier, adopted physical acceptance criterion, new altitude/constant decision and named assignee remains null/UNKNOWN. [PROVENANCE.json](PROVENANCE.json) pins the unchanged public sources and code. The [verification plan](../../../docs/VERIFICATION-PLAN.md#what-is-still-missing-entirely) supplies the wider missing-evidence context.

| Evidence row | Requirement | Units | Current status |
|---|---|---|---|
| implementation-identity | Bind all three implementation identities | identifiers | UNKNOWN |
| constant-provenance | Resolve the constant decision with the altitude contract | J/(kg K); K; Pa; m/s^2; K/m | UNKNOWN |
| altitude-contract | Resolve geometric versus geopotential altitude | m; datum and contract identifiers | UNKNOWN |
| reference-state | Match the frozen reference state | m; K; Pa; kg/m^3 | UNKNOWN |
| printed-reference | Preserve the reference and printed precision | K; mb; Pa; kg/m^3 | UNKNOWN |
| external-comparison | Preserve historical comparison with the standard | K; Pa; kg/m^3 | UNKNOWN |
| implementation-parity | Keep mutual parity separate from reference agreement | K; Pa; kg/m^3 | UNKNOWN |
| uncertainty | Separate precision and numerical tolerances from measurement uncertainty | record identifiers; K; Pa; kg/m^3; m | UNKNOWN |
| physical-state | Specify prospective matched physical records | Pa; K; composition units; m; time/location identifiers | UNKNOWN |
| acceptance-owner | Keep decisions and acceptance ownership explicit | decision and owner identifiers | UNKNOWN |
| downstream-custody | Document consequences before any separately authorized change | artifact and consumer identifiers | UNKNOWN |
| complete-disposition | Keep incompatible contracts and missing observations unresolved | status and evidence identifiers | UNKNOWN |

Prospective physical records need a matched state, time/location, vertical datum, pressure, temperature, composition/humidity, density anchor, calibrated raw observations and applicable uncertainty. A density dial, standard table or numerical tolerance cannot supply those missing observations. First-layer scope and forward/inverse caller contracts need explicit applicability.

A future atmosphere-contract owner must decide the dry-air constant and altitude policy together, publish the source and old/new consequences, and identify the applicable verification acceptance owner. Named assignees and adopted decisions are unavailable here. Repository gate success and officer landing signatures do not establish scientific or physical acceptance.

The published question identifies the cell parity mirror and generated analysis figures as affected downstream surfaces. This map records that custody requirement without changing their sources, computing the consequences or regenerating outputs. Historical failures remain published until separate authorized work and an applicable adopted contract justify a new record.
