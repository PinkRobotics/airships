# Model and viewer contract evidence

This read-only paper follows [question 16](../../../docs/OPEN-QUESTIONS.md#16-nine-constants-cross-the-sim3d-boundary-unchecked-and-two-are-already-wrong--partly-fixed-2026-10-01) and existing [issue 15](https://github.com/PinkRobotics/airships/issues/15), recorded in the [local filed-issue table](../../program/OPEN-QUESTION-ISSUES.md#filed-issues--2026-10-09). The published status remains PARTLY FIXED. The remote issue is not rechecked or changed.

The assignment names `sim/spec.js`, which is absent on this observed base. The published question and parity imports identify the existing [model configuration](../../../sim/config.js). This paper records the absent assigned path and traces that declared implementation read-only alongside [the viewer configuration](../../../3d/model/config.js); it creates or repairs neither source. [PROVENANCE.json](PROVENANCE.json) pins both the absence and the existing dependency trace.

The [import boundary](../../../tools/check_boundaries.py) keeps model and viewer standalone. [Parity source](../../../tests/cases/spec-parity.cases.js) enumerates numeric partners and explicit exemptions, including evaluated-consumer checks and illustration-only fields. [EVIDENCE-MAP.json](EVIDENCE-MAP.json) retains those source contracts and the published corrected-discrepancy history without executing them. A historical correction or declared test is not a newly reproduced result or physical qualification.

The published station/pair decision and illustrated area allowance remain source context. Parity exemption and test wording still describes that layout as pending/unresolved; the map keeps these differently dated statements separately. It does not harmonize them, change a mesh/count/rotor, or establish installed aerodynamic capacity.

[The adapter](../../../3d/adapter/fable.js) translates host model fields into [viewer state](../../../3d/physics/state.js), retaining host-supplied altitude, speed, duty, force and electrical channels where present. It maps mass to fractions and model power to drawing channels; those model fields are not physical telemetry. Local shape/fallback channels and missing-host behavior retain their own source scope.

The host phase list and [standalone mission](../../../3d/anim/mission.js) have different phase and timing contracts. Host hose work overlaps flown phases at the adapter seam; standalone hose phases remain separate. Sharing constants cannot establish equal mission duration, workload or operating capability. The map retains the dated power-share statement alongside the current [energy consumer](../../../3d/physics/energy.js): missing electrical channels stay null and the graph can be unavailable. Adapter fallback values are separately recorded code behavior, not measured zero or generation.

[The driver](../../../3d/anim/driver.js) uses supplied hose and release progress. The published stowed-hose/anchor checks and short hull-relative spray remain limited illustration history: a release-height change does not deploy or lengthen a hose, and a curtain without ground-water simulation does not establish deposition, fire effectiveness or a physical pickup/release process.

| Evidence row | Requirement | Units | Current status |
|---|---|---|---|
| declared-source | Bind the authoritative model and declared viewer copy | identifiers | UNKNOWN |
| import-boundary | Retain the standalone dependency boundary | module identifiers | UNKNOWN |
| paired-coverage | Trace numeric partners and explicit exemptions | key and contract identifiers | UNKNOWN |
| corrected-history | Preserve the published corrected discrepancies | historical source context | UNKNOWN |
| station-pair | Keep stations, paired rotors and illustrated area distinct | count and area convention identifiers | UNKNOWN |
| host-precedence | Trace host-state precedence and unit mapping | t; fractions; MW; m; km/h; m/s; state identifiers | UNKNOWN |
| mission-scope | Preserve distinct host and standalone cycles | phase identifiers; s; min | UNKNOWN |
| power-scope | Distinguish dated power-share scope from current channel availability | MW; channel and source identifiers | UNKNOWN |
| hose-anchor | Keep release height separate from hose/anchor deployment | m; progress and state identifiers | UNKNOWN |
| spray-illustration | Keep the drawn spray separate from ground delivery | m; release progress; scope identifiers | UNKNOWN |
| physical-applicability | Specify missing physical applicability records | record identifiers; quantity-specific units | UNKNOWN |
| acceptance-custody | Separate source contracts, repository checks and physical acceptance | status and owner identifiers | UNKNOWN |

All prospective physical observations, evidence identifiers, adopted acceptance criteria and named owners remain null/UNKNOWN. Applicable measurements need exact configuration/state, calibrated raw custody and uncertainty under separate authorization. [The verification plan](../../../docs/VERIFICATION-PLAN.md#what-is-still-missing-entirely) gives the broader missing-evidence context. Repository gates and officer landing signatures cannot settle physical applicability.

This paper runs no numerical comparison, mutation/parity experiment, generator, animation or simulator and repairs no code, constants or defaults. It introduces no new prediction, physical observation or remote issue action and does not repeat the atmosphere or failure-button papers.
