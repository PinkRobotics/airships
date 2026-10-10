# Nitrogen-recovery fraction and equipment evidence

This prospective map follows [question 10](../../../docs/OPEN-QUESTIONS.md#10-what-nitrogen-recovery-fraction-is-demonstrable) and existing [issue 9](https://github.com/PinkRobotics/airships/issues/9), as recorded in the [local filed-issue table](../../program/OPEN-QUESTION-ISSUES.md#filed-issues--2026-10-09). The current remote issue state is not rechecked or changed here.

The published question assumes a liquefaction investment and a fraction returned on recovery. It asks whether a complete airborne system can reproduce that fraction without an external heat source, which complete plant and tank masses belong in the dry ledger, and what duty cycle they can sustain. Those source assumptions remain comparison context, not physical observations, selected hardware or a demonstrated operating plant.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) preserves the already-public assumption values with exact source identity and links them to prospective process records. Every measurement, evidence identifier and adopted system acceptance criterion remains null/UNKNOWN. [PROVENANCE.json](PROVENANCE.json) pins the question, issue-filing record and [verification plan](../../../docs/VERIFICATION-PLAN.md#what-is-still-missing-entirely).

| Evidence row | Requirement | Units | Current status |
|---|---|---|---|
| fraction-definition | Define the recovery fraction boundary | definition identifiers; J; kg | UNKNOWN |
| liquefaction-input | Observe complete liquefaction investment | J; W; kg; s | UNKNOWN |
| recovery-output | Observe useful recovered output | J; W; s | UNKNOWN |
| nitrogen-inventory | Match the nitrogen inventory | kg; kg/s; s | UNKNOWN |
| process-state | Document process states and applicability | Pa; K; state identifiers; s | UNKNOWN |
| thermal-boundary | Disclose heat sources and heat rejection | J; W; K; s | UNKNOWN |
| loss-accounting | Separate ideal bookkeeping from process losses | J; W; s | UNKNOWN |
| plant-bill | Identify the complete plant mass boundary | part/configuration identifiers; kg | UNKNOWN |
| tank-bill | Identify the complete tank mass boundary | part/configuration identifiers; kg | UNKNOWN |
| weighed-mass | Observe plant/tank mass and reconcile the dry ledger | kg | UNKNOWN |
| duty-cycle | Observe a complete repeatable duty cycle | s; W; J; kg/s; K | UNKNOWN |
| airborne-integration | Establish airborne system applicability | configuration identifiers; Pa; K; W; kg | UNKNOWN |
| measurement-quality | Retain raw observations and uncertainty | record identifiers; applicable units | UNKNOWN |
| system-comparison | Keep fraction, mass and duty-cycle acceptance distinct | dimensionless; kg; s; status records | UNKNOWN |

The fraction needs a declared numerator, denominator, nitrogen inventory and conditioning boundary. Gross expansion output, net useful recovered energy, auxiliary consumption and external heat are separate quantities. Any lossless bookkeeping identity remains distinct from observed system evidence after thermal, mechanical, electrical and distribution losses. No fraction is calculated here.

Complete plant/tank mass needs an installed bill, actual conditioned weighing and a dry-versus-fluid inventory definition. Core machine or empty-vessel mass alone cannot settle it. Shared equipment must be allocated once; no component, production or plant-mass estimate is supplied.

A sustainable duty-cycle record needs startup, operating, transient, shutdown and turnaround states with compatible thermal, storage and inventory boundaries across repeated episodes. A single steady operating point cannot establish that record. Fraction evidence, complete equipment mass and duty-cycle applicability remain separate unresolved requirements; success in one would not close the others.

This paper specifies evidence to seek under separate authorization. It performs no process calculation, hardware selection, physical test, native solver, scientific output recomputation, source modification or remote issue action.
