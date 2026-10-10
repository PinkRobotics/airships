# Retained-water and operating-reserve evidence

This is a prospective evidence map for [question 4](../../../docs/OPEN-QUESTIONS.md#4-how-much-delivery-can-be-retained-while-holding-the-hull) and existing [issue 4](https://github.com/PinkRobotics/airships/issues/4), as linked by the [filed-issue record](../../program/OPEN-QUESTION-ISSUES.md#filed-issues--2026-10-09). The local source records that tracking link; its current remote state is not checked or changed here.

The question supplies conditional quasi-static force-and-bus model bookkeeping. It leaves vertical dynamics, suspended-load control and sufficient stored energy for mission completion unestablished. Rotor energy and power depend on constant hover merit times drive efficiency at every thrust and speed, without separately specified blade profile power or blade, speed and pitch policy. A physical reserve requirement beyond the first model closing threshold remains unresolved.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) identifies each published model-row context by source line/hash and maps it to prospective observations. Class, distance, basis and profile identify the source scenario; they are not measured capability. Existing table numbers remain in the original source and are not recomputed here. [PROVENANCE.json](PROVENANCE.json) pins the question, filed-issue record and [verification plan](../../../docs/VERIFICATION-PLAN.md).

| Evidence row | Requirement | Units | Current status |
|---|---|---|---|
| delivery-boundary | Define the delivery observation boundary | kg; location and time identifiers | UNKNOWN |
| loaded-water | Loaded water and tank tare | kg; K | UNKNOWN |
| release-series | Release and delivery accounting | kg; kg/s; s | UNKNOWN |
| retained-series | Retained water throughout the cycle | kg; s; m | UNKNOWN |
| mass-accounting | Water mass reconciliation | kg; kg/s; s | UNKNOWN |
| holding-state | Hull holding and load context | kg; N; Pa; K; m/s | UNKNOWN |
| vertical-dynamics | Vertical dynamics applicability | m; m/s; m/s^2; N; s | UNKNOWN |
| suspended-load | Suspended-load control | m; N; s | UNKNOWN |
| rotor-assumption | Actual rotor efficiency and policy | N; W; rad/s; deg | UNKNOWN |
| bus-power | Bus and transient limits | W; V; A; s | UNKNOWN |
| accessible-energy | Accessible stored energy | J; W; K; s | UNKNOWN |
| reserve-requirement | Operating reserve requirement | J; W; s; requirement identifiers | UNKNOWN |
| reserve-observation | Reserve available under the declared context | J; W; kg; s | UNKNOWN |
| cycle-completion | Complete-cycle applicability | record identifiers; s | UNKNOWN |
| uncertainty | Measurement and source identity | record identifiers; applicable SI units | UNKNOWN |

Water released from a tank, water retained onboard and water received at a declared delivery boundary require distinct observations. Losses, tare, inaccessible water and timing belong in the same mass-accounting boundary. Model-labelled delivery does not establish ground deposition, coverage or fire effectiveness; those interpretations need their own applicable evidence.

Holding the hull needs compatible article mass, ambient state, force owners and water/load observations through the cycle. Quasi-static bookkeeping does not supply measured dynamics or suspended-load control. Nominal power and accumulated energy also do not establish transient bus capability or usable storage under actual conditions.

Every physical value, evidence identifier and operational acceptance criterion here remains null/UNKNOWN. The intended requirement owner must adopt an applicable reserve contingency and criterion before reserve acceptance; no numeric margin, reserve amount or physical threshold is invented. No trajectory, retention, capacity or mission-completion prediction, source modification, physical test or remote issue action is performed.
