# Mission state and timebase provenance before evidence comparison

This paper traces existing [mission construction](../../../sim/mission.js), [plan records](../../../sim/plan.js), [served selection](../../../sim/served-plan.js) and [signed-unheld summaries](../../../research/analysis/energy-unheld.json). The [verification plan](../../../docs/VERIFICATION-PLAN.md) remains authoritative for the physical questions. This is a provenance map. It establishes no measured clock alignment, observed trajectory, qualified control response or physical completion.

| Evidence boundary | Required distinction |
|---|---|
| Source and plan identity | Exact source/configuration, route, basis, selected controls and proof precede comparison. |
| Host elapsed clock | Raw acquisition clock, model elapsed time, pause/speed/clamp, phase-step and frozen state differ. |
| Cycle and phase address | Mission offset, cycle/target/station and local phase progress belong to the record. |
| Seam and summary scope | One-sided seams and refined phase extrema are not chronological observed samples. |
| Signed quantities | Authority residual, net force, inventories, display fractions and speed channels retain separate meanings. |
| Coordinates and height | Geographic bearing, local hull axes/origin and atmospheric height datum need explicit provenance. |
| Consumer contract | Host state, standalone demonstration and adapter fallbacks remain source-specific. |
| Prospective clock evidence | Raw clocks, calibration, synchronization and uncertainty remain missing. |

The host frame loop derives a capped interval from browser frame timestamps, scales it by the selected demonstration speed and holds model time while paused. Phase stepping can jump that clock; exhausted storage can freeze a mission at its recorded model time. Displayed T+ therefore does not identify a measured flight clock or uninterrupted wall time. Future raw instrument clocks need their own acquisition origin, units, synchronization, drift, latency and uncertainty provenance before any alignment is justified. Mapping those observations to prescribed model time is a separate applicability decision. No transformation, clock offset or tolerance is calculated here.

The mission converts planned phase minutes to cumulative seconds. Its state function applies a mission offset, wraps the cycle, identifies a local phase and progress, and addresses rotating targets/stations by cycle number. Served selection can replace the plan and bounds or leave a stand-down/unavailable state. The analysis generator instead accumulates phase durations from the prescribed cycle origin. A cycle-minute field from that generator cannot silently become host display time or an observed timestamp. Every comparison needs the original time origin, offset, cycle, phase, seam side and exact plan inputs.

The signed-unheld JSON preserves every original row, failure, sign, limit, phase peak and operand in CROSSWALK.json. Positive residual denotes unsupported surplus lift; negative residual requires unavailable upward authority. The verdict mesh, extrema refinement and both sides of seams remain source procedures, not new sampling performed here. Phase maxima are summary evidence; they cannot be stitched into an observed trajectory. A row without a failing phase does not qualify a real aircraft. The verification plan also retains prescribed-cycle non-closure and labels descent/bag-credit comparisons as diagnostic effort, not operational savings.

The host's netN and unheldT have different owner boundaries. Neither magnitude nor a display force label permits substitution. The adapter converts inventory into fractions and speed units, but its airspeed and ground-speed fields currently share the host ground-speed input; its vertical-speed channel comes from a phase-shape fallback. Those are published consumer contracts, not air-relative or vertical-motion measurements. Supplied, fallback, default and missing fields must be identified separately. Missing telemetry is not zero.

The route-bearing helper declares degrees from north, while the state geometry uses radians from north. Positive model vertical speed follows increasing prescribed altitude. The local model declares nose-forward, port-positive and up-positive axes with an origin at the hull centre of buoyancy. Configuration heights refer to the hull centre above source water or reference ground, while a terrain reference bridges the atmosphere ledger. The published geometric/MSL versus geopotential-height disagreement and atmosphere MISS remain verbatim in the map. No datum, constant or trajectory is repaired or reconciled.

The host's six-phase mission and standalone eleven-phase demonstration retain different timing and illustrative power contracts. The published source explicitly says shared constants do not make them identical. Adapter phase mapping, off-cycle fallback, host-field precedence and illustrative phase shapes must remain visible when comparing records. A common drawing or phase label is insufficient provenance.

[CROSSWALK.json](CROSSWALK.json) maps source locators, units, prospective custodian roles and insufficient evidence. Actual observations, evidence identifiers, matched configurations, clock calibration/alignment, uncertainty and physical acceptance criteria are NULL/UNKNOWN. Roles remain UNASSIGNED. [PROVENANCE.json](PROVENANCE.json) pins all cited local inputs at the baseline revision. Original source bytes and failure records remain unchanged.

This paper supplies comparison requirements only. It does not run the model or an experiment, recompute time/trajectory/force/energy, select a threshold, implement a controller, repair failure-button wiring, or update a remote issue. Dynamics feasibility, pickup control and failure-button behaviour remain separate questions in their existing papers.
