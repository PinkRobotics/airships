# Mapped water and the evidence needed for operational drafting

This paper maps [the published question](../../../docs/OPEN-QUESTIONS.md#13-water-geometry-is-measured-operational-availability-remains-open) and [its existing tracking issue](https://github.com/PinkRobotics/airships/issues/12) to missing observations using the [verification plan](../../../docs/VERIFICATION-PLAN.md). The question remains open. No measurement, operational capability or hardware qualification is established.

| Evidence boundary | Existing limitation | Prospective custodian role |
|---|---|---|
| mapped-proximity | Published shoreline proximity is a simplified-outline closest-vertex/centroid proxy. Freshwater Atlas area is not depth; straight-line geometric distance is not a flown route or usable-source observation. | Geospatial and source-applicability evidence custodians |
| generated-station | Generated intake/alternate points use geometric inset/chord/centroid heuristics, filtered by class radius and area-weighted selection. Generated exercise stations are not surveyed stations or a depth/permission/sustainability check. | Draft-site geometry and access evidence custodians |
| depth-and-clearance | Published bag-depth requirements follow assumed filled-bag geometry. They are not surveyed lake depths; the source dataset carries area, not bathymetry. | Bathymetry and intake-geometry evidence custodians |
| access-and-permission | Legal right, site access, habitat/season restrictions, ice and actual availability are missing operational evidence. This map makes no current legal ruling or grant. | Access and permissions evidence custodian |
| sustainable-draw | Historical geometric coverage and hypothetical drawdown are not sustainable-source yield. Area is not stored usable volume or a guarantee of replenishment. | Water-supply and environmental evidence custodians |
| station-keeping | Geometry and still-air model records do not establish station keeping with suspended pickup. Horizontal actuator power, control response and load transients remain unestablished. | Station-keeping and suspended-load evidence custodians |

The published study is preserved as historical geometric evidence. Its shore-distance proxy, radius-filtered generated stations and conditional accepted-plan diagnostics answer different questions. Their denominators and refused legs remain source-specific. Generated exercise incidents are not flown aircraft records, and centroid/perimeter studies are not operational dispatch observations.

The station generator uses polygon geometry and area heuristics, including centroid fallbacks. It does not check bathymetry, legal access, seasonal water level, sustainable withdrawal or station keeping. Mapped shore proximity therefore cannot be relabelled operationally usable water. No new spatial join, usable-water fraction or route prediction is made.

Depth evidence would need a matched station, bed and water-level state plus actual intake/bag geometry and clearance. Access evidence would need a responsible authorization record with activity, spatial and temporal scope. Supply evidence would need sustained withdrawal and refill observations with applicable constraints. Those prospective fields remain empty; a polygon does not supply them. This is an evidence-requirements map, not a legal determination or an instruction to survey or draw water.

Wind, waves, flow, suspended pickup and control response belong to physical station-keeping evidence. A still-air geometric plan cannot establish them. This paper preserves the old study's coverage and drawdown text without converting either into a usable-source claim.

[CROSSWALK.json](CROSSWALK.json) records source destinations, prospective observations and units, insufficient or disconfirming evidence, and the verbatim published question. Actual observations, evidence identifiers, matched configurations, uncertainty and physical acceptance criteria are NULL/UNKNOWN. Custodian roles are prospective and remain UNASSIGNED. A criterion must be traceable to the matched physical question before any closure decision; no numeric tolerance or owner appointment is made here.

[PROVENANCE.json](PROVENANCE.json) pins every local source to the actual baseline revision. Preexisting source bytes, printed failures and conditional results remain unchanged. This paper does not execute a solver, experiment, campaign, field action or remote issue update.
