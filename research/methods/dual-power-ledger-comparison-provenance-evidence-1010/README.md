# Published power-accounting disagreement and comparison provenance

The [published known-defect section](../../../docs/OPEN-QUESTIONS.md#known-defects) retains its historical disagreement between planCycle headline energy and stateAt instrument accounting. Its old numerical values, ratio and sampled schedule remain solely in the unchanged source. Neither historical accounting is quietly chosen, and this paper supplies no repaired headline, reconciliation result or physical feasibility assertion.

Current code must be traced separately from that historical description. [planCycle](../../../sim/plan.js) delegates to integrateCycle in [power.js](../../../sim/power.js), returning its phase ledger, gross channel ledger, recovery magnitude and aggregate energy. [stateAt](../../../sim/state.js) obtains instantaneous power from the same drawAt and passes through draw/gen/electrical in running states. The state source calls that shared path the defect's fix, and the [root README](../../../README.md#model-output-and-limits) says force and energy integrals share a calculation. The OPEN-QUESTIONS current-register note explicitly treats the older framing as historical and says the power question now extends beyond earlier arithmetic fixes. Those current statements are retained alongside the published historical dispute. This paper neither asserts a currently independent second power implementation nor declares the historical comparison reconciled or either path physically validated. Original matched records and a responsible adopted disposition remain unknown.

[CROSSWALK.json](CROSSWALK.json) explicitly maps the declared terms rather than substituting generic record requirements for the code identities:

| Source identity | Accounting boundary |
|---|---|
| draw.hotel | Hotel draw under source assumptions, distinct from generation. |
| draw.prop | Zero-lift plus induced-drag draw; combined with rotors in electrical propulsion. |
| draw.rotors | Supplied rotor draw, distinct from requested demand and clipping diagnostics. |
| draw.winch | Conditional handling/hoist draw; hoist subset cannot be added twice. |
| draw.pumps | Fill pump channel from the declared pump relation. |
| draw.cryo | Production-only return draw; startup, standby and restart are omitted. |
| gen.solar | Model supply enters bus and instantaneous battery accounting; aggregate E has no solar subtraction. |
| gen.regen, eBack, E.recovery | Recovery supply, separate magnitude and signed negative aggregate credit. |
| electrical.generatorPowerMW | No independent generator-nameplate fuel supply booked in this electrical output. |
| E, Echan, eCycleMWh | Phase entries, gross channel accumulation and recovery-adjusted aggregate are distinct views. |
| letdownMWh, anchorHoistMWh, rotorClipMWh | Subset or requested-minus-supplied diagnostics, not extra independent energy terms. |
| stateAt draw/gen/electrical | Running pass-through differs from early inactive returns and stopped state. |
| ledger, dragMW, diskMW, pumpMW | Source helper identities and assumptions, not additional acquired energy channels. |

The current aggregate accumulates draw channels and subtracts nitrogen recovery. Instantaneous electrical batteryPowerMW separately subtracts solar and recovery supply. Those are source boundary descriptions, not an evaluated difference or a newly diagnosed fix request. Gross channel entries, phase entries, generation and diagnostics require explicit sign/inclusion conventions before comparison. The historical description's term count cannot establish historical term identities; this paper does not invent them from the current code.

Current stateAt derives phase/progress from mission time, class/mode/plan and status. Inactive early returns have different available fields. The stopped branch empties draw and returns null electrical while continuing to pass through gen; an empty draw cannot be equated with a complete matched energy record or measured generation. Current integration uses an energy quadrature separately from the seam-inclusive limit/extrema mesh. No mesh, time interval, schedule, phase duration or numerical input is copied, selected, executed or integrated here.

Prospective comparisons require matched source/configuration and actual component/meter identities, applicable mission state and interval, original units/reference and gross/net/sign conventions, all declared inclusions/exclusions and loss boundaries, unmodified source observation/energy records, calibration, uncertainty and responsible adoption provenance. Role names are proposals only. Actual observations, meter records, matched configuration/state/interval, reference/component/inclusion records, calibration, uncertainty, matched comparisons, assigned owners and adopted reconciliation criteria remain NULL/UNKNOWN; roles are UNASSIGNED.

[PROVENANCE.json](PROVENANCE.json) pins the task inputs and the explicitly supplemental current imported power/state modules. Existing source text, dispute history, model code and schemas remain unchanged. Q7 constant justification, general mission timebase, Q16 viewer geometry, Q6 nitrogen qualification and external energy supply-chain work remain separate; this map concerns only these named accounting boundaries.

No model or fixture is run, integrated or simulated. No numeric results, ratios, constants, schedules, projections, benefit calculation, measurements, selected configuration/threshold/physics or physical procedure are supplied. The root README says no aircraft has been built or flown. Shared code and passing repository checks do not supply missing physical evidence, a model winner, reconciliation, feasibility, qualification, safety or performance.
