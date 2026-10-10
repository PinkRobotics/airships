# Pickup, suspended-load control and station-keeping evidence boundaries

This paper maps [the published question](../../../docs/OPEN-QUESTIONS.md#14-can-the-bag-be-picked-up-and-released-at-this-scale) and [its existing tracking issue](https://github.com/PinkRobotics/airships/issues/13) to missing observations using the [verification plan](../../../docs/VERIFICATION-PLAN.md). The question remains open. No measurement, operational capability or hardware qualification is established.

| Evidence boundary | Existing limitation | Prospective custodian role |
|---|---|---|
| matched-load-transfer | Anchor reach, achieved bag inventory and quasi-static support/steady hoist are represented. Cable reach is not immersion or pickup-load evidence; pickup shock is not bounded by the steady hoist bill. | Pickup load-path and winch evidence custodians |
| pendulum-motion | The printed ideal small-angle pendulum period is an existing diagnostic. Swing, damping and winch transients are unpriced; a period is not a coupled controlled response. | Suspended-load dynamics evidence custodian |
| control-response | The fixed choreography is checked quasi-statically, not integrated as observed vertical dynamics. Unsupported instants refuse the plan; source failure/UNKNOWN records remain. | Flight-controls and instrumentation evidence custodians |
| beam-wind-station-keeping | The published beam-wind side force uses a stipulated wind and unverified side-drag coefficient with local density. No horizontal actuator or station-keeping power is priced. A force diagnostic is not available horizontal power. | Wind-load and station-keeping evidence custodians |
| evidence-applicability | Printed cable/battery policies and the dry-equals-payload target do not qualify an installed pickup system. The existing material-strength crosswalk is separate; no repetition or cable/control selection occurs here. | Evidence configuration and acceptance-criteria custodian |

The published pickup question asks for cable, winch and control measurements and missing beam-wind station-keeping power. Current force/bus checks apply to fixed choreography under quasi-static assumptions. They do not establish observed vertical dynamics, suspended-load control or mission-completion energy. Unsupported instants remain refused. The verification plan also records that its prescribed record-basis cycles do not close; the descent and bag-credit entries are diagnostic effort comparisons, with no established operational saving.

Anchor reach and credited water inventory are not pickup shock evidence. The steady hoist bill does not bound load transfer out of the water. A matched prospective record would retain hull/attachment, cable, winch, bag and water states with synchronized force, motion and command histories. This paper records those requirements without calculating loads or selecting hardware.

The printed ideal small-angle pendulum period is a diagnostic, while swing, damping and winch transients remain unpriced. A period alone cannot demonstrate a controlled response. Control evidence would need command/measurement timing, sensor configuration, response/saturation history, directional actuator limits and the corresponding disturbance and suspended-load state.

The historical beam-wind table is a side-force diagnostic with stipulated wind and an unverified coefficient. No horizontal actuator or station-keeping power is priced. Existing vertical force/bus and day-average solar fields cannot be claimed as available horizontal power. No load/power/trajectory calculation or table regeneration occurs. Existing material and cable-strength crosswalks remain separate; this unit does not select a cable, controller or fail-safe policy.

[CROSSWALK.json](CROSSWALK.json) records source destinations, prospective observations and units, insufficient or disconfirming evidence, and the verbatim published question. Actual observations, evidence identifiers, matched configurations, uncertainty and physical acceptance criteria are NULL/UNKNOWN. Custodian roles are prospective and remain UNASSIGNED. A criterion must be traceable to the matched physical question before any closure decision; no numeric tolerance or owner appointment is made here.

[PROVENANCE.json](PROVENANCE.json) pins every local source to the actual baseline revision. Preexisting source bytes, printed failures and conditional results remain unchanged. This paper does not execute a solver, experiment, campaign, field action or remote issue update.
