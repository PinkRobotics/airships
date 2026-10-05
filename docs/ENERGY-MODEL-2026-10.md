<!-- energy:model:start -->
# Energy model, 2026-10-02

One ledger owns the modelled force and power. This is an unvalidated simulation, not a flight performance claim.

## Force and energy rules

The ledger subtracts all onboard weight from local buoyant lift.
Its owners are the cable-carried water, downward rotors, permitted aerodynamic downforce and signed vertical drag.
Unheld force stays visible.

Surplus is local displaced-air mass minus dry mass, water and nitrogen.
The signed residual is surplus minus bag support, rotor thrust, aerodynamic downforce and vertical drag.

Glauert momentum pricing solves T = 2 ρ A v_i √(V² + (v_c + v_i)²), then P = T (v_c + v_i) / η.
The vertical drag owner is ρ C_D S v_z |v_z| / (2 g), with upward velocity positive.
The favourable downforce cap is C_L,max q S, and its induced drag is T_aero² / (q π b² e).

The force tolerance is 0.000001 times the larger of unity and absolute surplus.
Constraint sampling uses 1024 intervals per phase, plus seams and internal profile joins.
Energy uses 96 midpoint intervals per phase; constraint peaks are checked separately.

The unverified broadside coefficient is 1; the favourable lift coefficient is 1.
The reported lift-coefficient sweep is 0.5, 1, 1.5; rotor-efficiency endpoints are 0.55, 0.7.
Bag water is credited when carried; its 15 m lift at efficiency 0.85 remains priced.

A cycle closes only when the residual and gross bus draw meet the stated tolerances at every checked instant.
Bus saturation alone is a note.
The rotors have no upward authority.

Record basis credits no aerodynamic hold-down.
Favourable basis chooses the least-power split between capped rotors and capped aerodynamic downforce.
Induced drag is charged to propulsion, and all force and power terms use local ISA density.

Rotor efficiency represents figure of merit times drive efficiency.
Hold-down descent is priced as climb, on the conservative side; climb against hold-down thrust is priced as level flight, with no bound claimed.

The installed thrust cap is an unverified hover surrogate at the battery-plus-generator rating.
A feasible result is quasi-static.
Feasible means quasi-static force and bus closure at every checked instant. Battery hours are reported; they do not determine feasibility. These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.
The [served-candidate inertia diagnostic](../research/analysis/energy-served-inertia.json) checks signed vertical hull demand against rotor authority in both directions at published and captured routes.
The feasible-profile records also contain that comparison for every phase.

## Signed demand, added mass and suspended-load limits

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

With upward acceleration positive and forces in tonnes-force:

`I = (m_onboard + C * m_displaced_air) * a_z / g`

`T_required = T_quasi + unheld - I`

The sampled rotor demand is accepted only inside `0 <= T_required <= T_available`.
A negative required thrust is an upward-authority shortage; a demand above available thrust is a downward-authority shortage.
The screen fixes aerodynamic, bag and drag owners and other electrical loads at the quasi-static values.
Buoyancy is already in the ledger. Shedding hold-down supplies an upward increment; it is not additional buoyancy.
The samples, central second difference and cutoff remain unchanged; a gap-free sample is not continuous-time control evidence.

| Phase | Vertical acceleration and first allocation | Still unresolved |
|---|---|---|
| SOURCE_APPROACH | Downward into descent: add downward thrust; upward braking: shed it | When rotors are zero and the bag carries the surplus, braking needs a different pickup, tension or trajectory schedule |
| WATER_FILL | Constant hull altitude; no hull acceleration demand | Water and nitrogen flow and load transfer |
| OUTBOUND_TRANSIT | Both signs in climb and letdown; shed for upward acceleration, add for downward acceleration | Force allocation follows acceleration, not velocity; aerodynamic response is unvalidated |
| WATER_RELEASE | Upward while starting the rise: shed; downward while stopping it: add | A rising hull can need additional downward force |
| BUOYANCY_ESCAPE | Upward then downward: shed then add | No hanging-water owner is credited |
| RETURN_TRANSIT | Either sign according to endpoint geometry; apply the signed equation | Short-route joins, actuator response and load control |

### Geometry-specific added mass remains open

The coefficients 0.70 and 1.00 are a sensitivity pair for transverse motion of a horizontal capsule of length/diameter 2.
The lower value rounds Munk's 0.702 transverse coefficient for a prolate spheroid of that fineness: [NACA Report 184 (1924)](https://ntrs.nasa.gov/citations/19930091249), Table I, printed p.20 / PDF p.21.
It is a potential-flow surrogate, not a measured capsule coefficient; neither endpoint establishes a physical limit.
The configured capsule has about 25% more volume than the spheroid on the same axes.
Added mass uses local displaced-air mass, not surplus lift. Attitude coupling requires a mass tensor and separate validation.

### Hull and load need separate equations

The current screen covers the hull alone. A minimum load model treats a rigid load on a taut, inextensible cable with prescribed winch length.
In SI units, with upward positive, a vertical schematic at fixed instantaneous mass is:

`(m_h + A_h) * z_h'' = B_h - m_h*g - T - F_rotor - F_aero - D_h + F_flow,h`

`(m_b + A_b) * z_b'' = T + B_b - m_b*g - D_b + F_flow,b`

Here B denotes buoyancy, T tensile cable force, A added mass and F_flow the separately required inventory/flow momentum terms.
The hull feels downward cable tension; bag weight already credited in the quasi-static ledger must not be charged twice.
For the straight taut-cable limit, `z_b = z_h - ell(t)` and `a_b = a_h - ell''`.
For a rigid airborne bag with no other force, `T = m_b * (g + a_h - ell'')`.
Bag buoyancy, water added mass and flow momentum must be supplied through immersion and pickup; dry-air load does not describe an immersed bag.

For peak loads use a one-sided elastic cable with stiffness k, damping c and unloaded winch length ell_0:
`T = 0` when slack; in extension, `T = max(0, k*(d-ell_0) + c*(d'-ell_0'))`.
Lateral motion needs pendulum coordinates: `r_b = r_h + ell*q(theta,phi)`, with q a downward-directed unit vector, and the separate body equations.
Unknown inputs are bag geometry, shell mass and immersion; cable stiffness, damping, distributed mass and slack; initial swing, flow history and winch speed ramps.
No snatch factor or assumed value closes these equations.
This treatment follows [Cicolani and Kanning, NASA TP-3280 (1992)](https://ntrs.nasa.gov/citations/19930003627), section 3, eqs.9b and 10 (PDF pp.14 and 16), and Figure 3 (printed p.15 / PDF p.23). No suspension parameters from another aircraft are transferred.

### Dated withdrawn measurement

Dated measurement at landing 16, 2026-10-05: absolute inertial force minus the additional downward rotor reserve at the same samples and coefficients. Withdrawn because it misses upward authority that cannot be obtained by shedding the existing downward thrust. Recomputed here solely to preserve that measurement.

| Population | Withdrawn absolute / signed | Reason |
|---|---|---|
| candidates | 284 / 354 | Signed demand must fit the authority in its own direction; profiles and verdicts are unchanged |
| capturedMissions | 16 / 21 | Signed demand must fit the authority in its own direction; profiles and verdicts are unchanged |


## Necessary stored energy, ideal accounting

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Ideal, lossless chronological accounting with nominal class storage fully usable and the plan initial nitrogen inventory charged. No losses, health, state-of-charge window, reserve, external recharge or thermal limit. This is not an endurance rule, a mission-completion verdict or a battery model. Solar and nitrogen recovery are the existing bus inputs, not a promised recharge system.

Integrate the existing drawAt electrical.batteryPowerMW at 2000 midpoint samples per phase, in PHASES order. Record cumulative draw at every phase end; interpolate the first nominal-storage crossing inside its sample.

| Captured mission or printed profile | Class / km / basis | Draw MWh | Nominal storage MWh | First empty min | Shortage MWh | Pages |
|---|---|---|---|---|---|---|
| exercise mission 11 (zero-based) | P100 / 13.981185 / record | 41.6 | 20 | 127.9 | 21.6 | index.html |
| exercise mission 12 (zero-based) | P100 / 9.689204 / record | 58.9 | 20 | 169.5 | 38.9 | index.html |
| fullDeliveryBest | P100 / 15.000000 / record | 42.0 | 20 | 129.3 | 22.0 | index.html; concept/index.html |
| fullDeliveryBest | P100 / 15.000000 / favourable | 37.8 | 20 | 123.9 | 17.8 | index.html; concept/index.html |
| asDrawn | P100 / 60.000000 / record | 20.1 | 20 | 104.7 | 0.1 | index.html; concept/index.html |
| ready selector | P1000 / 400.000000 / record | 330.5 | 120 | 233.1 | 210.5 | concept/energy-analysis.html |

Of 32 captured cycles, 2 exceed nominal storage; every other captured cycle stays inside it for one ideal cycle. The full JSON records cumulative draw in phase order and each printed profile, including every shortage found. Initial nitrogen is charged storage, not free energy. The 400 km P1000 ready-selector result is printed on concept/energy-analysis.html; it is outside the worked-example slider range.

Records: `research/analysis/energy-necessary.json`; generator: `research/analysis/energy-necessary.mjs`. No operational horizon or completion gate is added.

## What the profile search means

The prescribed profile is retained as "as drawn".
The result is the cheapest feasible profile found in the stated space, not a global optimum.

Cruise speed multipliers: 0.5, 0.75, 1, 1.25, 1.5.
Modes: rapid, balanced, endurance.

| Independent parameter | Searched values |
|---|---|
| climbRateMps | 0.5, 2 |
| letdownRateMps | 0.5, 2 |
| climbAirspeedMps | 0, 5 |
| letdownAirspeedMps | 0, 5 |

Climb and letdown each have independent peak-rate and peak-airspeed caps.
The slowest peak letdown cap is 0.5 m/s on each class.
This finite bound includes slow descents; smaller caps remain unsearched, not physically excluded.

Short joins take longer when needed for smoothness.
The prescribed return widens its climb and letdown joins using an upper bound on the composed easing derivatives, so each of the 2,001 sampled vertical speeds differs by at most 0.1 m/s. If those joins would overlap, its return time grows instead. This applies to all searched prescribed controls, not one retained-water row.
The drop altitude, terrain clearance and cable reach stay fixed.
The approach remains stationary.
Segment time and ground distance are integrated; energy uses the same instantaneous ledger.
A profile exceeding the route distance is refused.

Retained water is searched at five-percent payload steps and at each bisected first closing threshold.
Printed requirements round upward at the verdict resolution and replay through the model.
The older whole-phase dilation is named `movingPhaseRateMultiplier`; the new search does not use it.

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

| Class | km | Basis | As drawn | Minutes | Supplied MWh | kWh/planned tonne | Battery-hours quotient | Profile note |
|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | does not close | 34.196 | 8.192 | 81.923 | 1.418 |  |
| P100 | 15 | favourable | does not close | 34.196 | 6.402 | 64.017 | 1.824 |  |
| P100 | 60 | record | closes | 104.784 | 20.521 | 205.214 | 1.742 | quasi-static closure; dynamic profile unresolved; quasi-static closure; exceeds nominal storage in one ideal cycle |
| P100 | 60 | favourable | closes | 104.784 | 14.764 | 147.639 | 2.444 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | record | does not close | 35.362 | 62.314 | 62.314 | 1.149 |  |
| P1000 | 15 | favourable | does not close | 35.362 | 61.355 | 61.355 | 1.167 |  |
| P1000 | 60 | record | does not close | 93.116 | 141.533 | 141.533 | 1.334 |  |
| P1000 | 60 | favourable | does not close | 93.116 | 142.484 | 142.484 | 1.325 |  |
| P10000 | 15 | record | does not close | 45.512 | 694.378 | 69.438 | 2.198 |  |
| P10000 | 15 | favourable | does not close | 45.512 | 766.285 | 76.629 | 1.990 |  |
| P10000 | 60 | record | does not close | 94.381 | 1113.855 | 111.385 | 2.846 |  |
| P10000 | 60 | favourable | does not close | 94.381 | 1386.308 | 138.631 | 2.283 |  |

## Corrections from the energy comparison

Each earlier and current value below refers to the same generated field. Infeasible rows remain diagnostic supplied effort. Values that round identically at the published precision are omitted. The JSON preserves exact values.

### Part A

Refined force extrema and both sides of seams replace sampled phase peaks.

| Generated record and field | Earlier | Current |
|---|---|---|
| research/analysis/energy-bag-comparison.json#rows[2].carried.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-bag-comparison.json#rows[2].completed.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-bag-comparison.json#rows[3].carried.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-bag-comparison.json#rows[3].completed.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[0].current.worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-closure.json#rows[0].requirements.baseline.worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-closure.json#rows[0].requirements.clSensitivity[0].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-closure.json#rows[0].requirements.clSensitivity[1].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-closure.json#rows[0].requirements.clSensitivity[2].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-closure.json#rows[0].requirements.dragSensitivity[0].worst.progress | 0.822266 | 0.821818 |
| research/analysis/energy-closure.json#rows[0].requirements.dragSensitivity[1].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-closure.json#rows[0].requirements.dragSensitivity[2].worst.progress | 0.806641 | 0.807042 |
| research/analysis/energy-closure.json#rows[0].requirements.dragSensitivity[2].worst.unheldT | 56.475 | 56.476 |
| research/analysis/energy-closure.json#rows[0].requirements.powerAndThrust.verification.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[1].current.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[1].requirements.baseline.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[1].requirements.clSensitivity[0].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[1].requirements.clSensitivity[1].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[1].requirements.clSensitivity[2].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[1].requirements.dragSensitivity[0].worst.progress | 0.702148 | 0.702318 |
| research/analysis/energy-closure.json#rows[1].requirements.dragSensitivity[1].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[1].requirements.dragSensitivity[2].worst.progress | 0.210938 | 0.211160 |
| research/analysis/energy-closure.json#rows[1].requirements.powerAndThrust.verification.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-closure.json#rows[2].current.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[2].requirements.ballast.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[2].requirements.baseline.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[2].requirements.clSensitivity[0].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[2].requirements.clSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[2].requirements.clSensitivity[2].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[2].requirements.dragSensitivity[0].worst.progress | 0.045898 | 0.180000 |
| research/analysis/energy-closure.json#rows[2].requirements.dragSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[2].requirements.dragSensitivity[2].worst.progress | 0.664063 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].current.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].requirements.ballast.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].requirements.baseline.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].requirements.clSensitivity[0].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].requirements.clSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].requirements.clSensitivity[2].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].requirements.dragSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-closure.json#rows[3].requirements.dragSensitivity[2].worst.progress | 0.664063 | 1.000000 |
| research/analysis/energy-closure.json#rows[4].requirements.dragSensitivity[2].worst.progress | 0.695313 | 0.695516 |
| research/analysis/energy-closure.json#rows[4].requirements.powerAndThrust.batterySearch.printed | 529.177 | 529.178 |
| research/analysis/energy-closure.json#rows[4].requirements.powerAndThrust.requiredBatteryMW | 529.177 | 529.178 |
| research/analysis/energy-closure.json#rows[4].requirements.powerAndThrust.verification.peakRotorMW | 532.973 | 532.974 |
| research/analysis/energy-closure.json#rows[4].requirements.powerAndThrust.verification.worst.progress | 0.701172 | 0.713867 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[2].worst.progress | 0.695313 | 0.695516 |
| research/analysis/energy-closure.json#rows[5].requirements.powerAndThrust.batterySearch.printed | 529.177 | 529.178 |
| research/analysis/energy-closure.json#rows[5].requirements.powerAndThrust.requiredBatteryMW | 529.177 | 529.178 |
| research/analysis/energy-closure.json#rows[5].requirements.powerAndThrust.verification.peakRotorMW | 532.973 | 532.974 |
| research/analysis/energy-closure.json#rows[5].requirements.powerAndThrust.verification.worst.progress | 0.701172 | 0.713867 |
| research/analysis/energy-closure.json#rows[6].requirements.dragSensitivity[2].worst.progress | 0.696289 | 0.695961 |
| research/analysis/energy-closure.json#rows[6].requirements.dragSensitivity[2].worst.unheldT | 847.902 | 847.903 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[2].worst.progress | 0.696289 | 0.695961 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[2].worst.unheldT | 847.902 | 847.903 |
| research/analysis/energy-documents.json#records[0].asDrawn.worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-documents.json#records[1].asDrawn.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-documents.json#records[2].asDrawn.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-documents.json#records[3].asDrawn.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-documents.json#sensitivity[13].rows[0].worstUnheldT | -2743.309 | -2743.310 |
| research/analysis/energy-documents.json#sensitivity[16].rows[1].worstUnheldT | 6998.194 | 7001.267 |
| research/analysis/energy-documents.json#sensitivity[31].rows[0].worstUnheldT | -2743.309 | -2743.310 |
| research/analysis/energy-documents.json#sensitivity[34].rows[1].worstUnheldT | 6998.194 | 7001.267 |
| research/analysis/energy-feasible.json#rows[0].asDrawn.worst.progress | 0.205078 | 0.204787 |
| research/analysis/energy-feasible.json#rows[0].best.sensitivity[3].worst.progress | 0.668945 | 0.669025 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.worst.progress | 0.205078 | 0.204667 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.worst.unheldT | 8.726 | 8.727 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].worst.progress | 0.204102 | 0.203810 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].worst.unheldT | 48.264 | 48.265 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[3].worst.progress | 0.668945 | 0.669031 |
| research/analysis/energy-feasible.json#rows[2].asDrawn.worst.progress | 0.803711 | 0.804140 |
| research/analysis/energy-feasible.json#rows[2].asDrawn.worst.unheldT | 36.155 | 36.156 |
| research/analysis/energy-feasible.json#rows[2].best.sensitivity[2].worst.progress | 0.205078 | 0.204738 |
| research/analysis/energy-feasible.json#rows[2].best.sensitivity[2].worst.unheldT | -32.296 | -32.297 |
| research/analysis/energy-feasible.json#rows[2].best.sensitivity[3].worst.progress | 0.668945 | 0.669055 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.sensitivity[0].worst.progress | 0.051758 | 0.100000 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.sensitivity[1].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.sensitivity[2].worst.progress | 0.746094 | 0.850000 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.sensitivity[4].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.sensitivity[5].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.sensitivity[6].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.sensitivity[7].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[2].fullDeliveryBest.worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[3].asDrawn.worst.progress | 0.684570 | 0.684970 |
| research/analysis/energy-feasible.json#rows[3].best.sensitivity[2].worst.progress | 0.205078 | 0.204738 |
| research/analysis/energy-feasible.json#rows[3].best.sensitivity[2].worst.unheldT | -32.296 | -32.297 |
| research/analysis/energy-feasible.json#rows[3].best.sensitivity[3].worst.progress | 0.668945 | 0.669055 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.sensitivity[0].worst.progress | 0.051758 | 0.100000 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.sensitivity[1].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.sensitivity[2].worst.progress | 0.746094 | 0.850000 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.sensitivity[4].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.sensitivity[5].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.sensitivity[6].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.sensitivity[7].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[3].fullDeliveryBest.worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-feasible.json#rows[4].asDrawn.worst.progress | 0.999023 | 1.000000 |
| research/analysis/energy-feasible.json#rows[4].asDrawn.worst.unheldT | 0.172 | 0.309 |
| research/analysis/energy-feasible.json#rows[4].best.sensitivity[2].worst.progress | 0.671875 | 0.672223 |
| research/analysis/energy-feasible.json#rows[4].best.sensitivity[3].worst.progress | 0.668945 | 0.669336 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[0].worst.progress | 0.073242 | 0.180000 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[1].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[2].worst.progress | 0.462891 | 1.000000 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[3].worst.progress | 0.674805 | 0.674764 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[4].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[5].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[6].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[7].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].asDrawn.worst.progress | 0.825195 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].best.sensitivity[2].worst.progress | 0.672852 | 0.672599 |
| research/analysis/energy-feasible.json#rows[5].best.sensitivity[3].worst.progress | 0.668945 | 0.669402 |
| research/analysis/energy-feasible.json#rows[5].best.sensitivity[3].worst.unheldT | 52.867 | 52.868 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[0].worst.progress | 0.073242 | 0.180000 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[1].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[2].worst.progress | 0.462891 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[3].worst.progress | 0.674805 | 0.674764 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[4].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[5].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[6].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[7].worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.worst.progress | 0.827148 | 1.000000 |
| research/analysis/energy-feasible.json#rows[6].best.sensitivity[2].worst.progress | 0.695313 | 0.695391 |
| research/analysis/energy-feasible.json#rows[7].best.sensitivity[2].worst.progress | 0.695313 | 0.695391 |
| research/analysis/energy-feasible.json#rows[8].best.sensitivity[2].worst.progress | 0.695313 | 0.695420 |
| research/analysis/energy-feasible.json#rows[9].best.sensitivity[2].worst.progress | 0.706055 | 0.706470 |
| research/analysis/energy-feasible.json#rows[10].best.sensitivity[2].worst.progress | 0.707031 | 0.707194 |
| research/analysis/energy-feasible.json#rows[11].best.sensitivity[2].worst.progress | 0.707031 | 0.707194 |
| research/analysis/energy-profiles.json#rows[0].asDrawn.worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-profiles.json#rows[0].best.sensitivity[2].worst.progress | 0.214844 | 0.215163 |
| research/analysis/energy-profiles.json#rows[0].best.sensitivity[2].worst.unheldT | -18.783 | -18.784 |
| research/analysis/energy-profiles.json#rows[0].best.sensitivity[3].worst.progress | 0.668945 | 0.669198 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.sensitivity[0].worst.progress | 0.051758 | 0.100000 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.sensitivity[1].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.sensitivity[2].worst.progress | 0.746094 | 0.940000 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.sensitivity[4].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.sensitivity[5].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.sensitivity[6].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.sensitivity[7].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[0].fullDeliveryBest.worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[1].asDrawn.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-profiles.json#rows[1].best.sensitivity[2].worst.progress | 0.214844 | 0.215163 |
| research/analysis/energy-profiles.json#rows[1].best.sensitivity[2].worst.unheldT | -18.783 | -18.784 |
| research/analysis/energy-profiles.json#rows[1].best.sensitivity[3].worst.progress | 0.668945 | 0.669198 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.sensitivity[1].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.sensitivity[2].worst.progress | 0.748047 | 0.850000 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.sensitivity[4].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.sensitivity[5].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.sensitivity[6].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.sensitivity[7].worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.worst.progress | 0.749023 | 0.750000 |
| research/analysis/energy-profiles.json#rows[2].asDrawn.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-profiles.json#rows[2].best.sensitivity[0].worst.progress | 0.064453 | 0.180000 |
| research/analysis/energy-profiles.json#rows[2].best.sensitivity[2].worst.progress | 0.672852 | 0.672517 |
| research/analysis/energy-profiles.json#rows[2].best.sensitivity[3].worst.progress | 0.668945 | 0.669388 |
| research/analysis/energy-profiles.json#rows[2].fullDeliveryBest.sensitivity[2].worst.progress | 0.672852 | 0.672950 |
| research/analysis/energy-profiles.json#rows[2].fullDeliveryBest.sensitivity[3].worst.progress | 0.669922 | 0.669465 |
| research/analysis/energy-profiles.json#rows[3].asDrawn.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-profiles.json#rows[3].best.sensitivity[2].worst.progress | 0.672852 | 0.672950 |
| research/analysis/energy-profiles.json#rows[3].best.sensitivity[3].worst.progress | 0.669922 | 0.669465 |
| research/analysis/energy-profiles.json#rows[3].fullDeliveryBest.sensitivity[2].worst.progress | 0.672852 | 0.672950 |
| research/analysis/energy-profiles.json#rows[3].fullDeliveryBest.sensitivity[3].worst.progress | 0.669922 | 0.669465 |
| research/analysis/energy-profiles.json#rows[4].best.sensitivity[2].worst.progress | 0.707031 | 0.706591 |
| research/analysis/energy-profiles.json#rows[5].best.sensitivity[2].worst.progress | 0.707031 | 0.706591 |
| research/analysis/energy-profiles.json#rows[6].best.sensitivity[2].worst.progress | 0.707031 | 0.707327 |
| research/analysis/energy-profiles.json#rows[7].best.sensitivity[2].worst.progress | 0.707031 | 0.707327 |
| research/analysis/energy-requirements.json#rows[0].baseline.worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-requirements.json#rows[0].clSensitivity[0].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-requirements.json#rows[0].clSensitivity[1].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-requirements.json#rows[0].clSensitivity[2].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-requirements.json#rows[0].dragSensitivity[0].worst.progress | 0.822266 | 0.821818 |
| research/analysis/energy-requirements.json#rows[0].dragSensitivity[1].worst.progress | 0.810547 | 0.810707 |
| research/analysis/energy-requirements.json#rows[0].dragSensitivity[2].worst.progress | 0.806641 | 0.807042 |
| research/analysis/energy-requirements.json#rows[0].dragSensitivity[2].worst.unheldT | 56.475 | 56.476 |
| research/analysis/energy-requirements.json#rows[0].powerAndThrust.verification.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-requirements.json#rows[1].baseline.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-requirements.json#rows[1].clSensitivity[0].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-requirements.json#rows[1].clSensitivity[1].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-requirements.json#rows[1].clSensitivity[2].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-requirements.json#rows[1].dragSensitivity[0].worst.progress | 0.702148 | 0.702318 |
| research/analysis/energy-requirements.json#rows[1].dragSensitivity[1].worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-requirements.json#rows[1].dragSensitivity[2].worst.progress | 0.210938 | 0.211160 |
| research/analysis/energy-requirements.json#rows[1].powerAndThrust.verification.worst.progress | 0.222656 | 0.222832 |
| research/analysis/energy-requirements.json#rows[2].ballast.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[2].baseline.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[2].clSensitivity[0].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[2].clSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[2].clSensitivity[2].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[2].dragSensitivity[0].worst.progress | 0.045898 | 0.180000 |
| research/analysis/energy-requirements.json#rows[2].dragSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[2].dragSensitivity[2].worst.progress | 0.664063 | 1.000000 |
| research/analysis/energy-requirements.json#rows[3].ballast.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[3].baseline.worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[3].clSensitivity[0].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[3].clSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[3].clSensitivity[2].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[3].dragSensitivity[1].worst.progress | 0.731445 | 1.000000 |
| research/analysis/energy-requirements.json#rows[3].dragSensitivity[2].worst.progress | 0.664063 | 1.000000 |
| research/analysis/energy-requirements.json#rows[4].dragSensitivity[2].worst.progress | 0.695313 | 0.695516 |
| research/analysis/energy-requirements.json#rows[4].powerAndThrust.batterySearch.printed | 529.177 | 529.178 |
| research/analysis/energy-requirements.json#rows[4].powerAndThrust.requiredBatteryMW | 529.177 | 529.178 |
| research/analysis/energy-requirements.json#rows[4].powerAndThrust.verification.peakRotorMW | 532.973 | 532.974 |
| research/analysis/energy-requirements.json#rows[4].powerAndThrust.verification.worst.progress | 0.701172 | 0.713867 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[2].worst.progress | 0.695313 | 0.695516 |
| research/analysis/energy-requirements.json#rows[5].powerAndThrust.batterySearch.printed | 529.177 | 529.178 |
| research/analysis/energy-requirements.json#rows[5].powerAndThrust.requiredBatteryMW | 529.177 | 529.178 |
| research/analysis/energy-requirements.json#rows[5].powerAndThrust.verification.peakRotorMW | 532.973 | 532.974 |
| research/analysis/energy-requirements.json#rows[5].powerAndThrust.verification.worst.progress | 0.701172 | 0.713867 |
| research/analysis/energy-requirements.json#rows[6].dragSensitivity[2].worst.progress | 0.696289 | 0.695961 |
| research/analysis/energy-requirements.json#rows[6].dragSensitivity[2].worst.unheldT | 847.902 | 847.903 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[2].worst.progress | 0.696289 | 0.695961 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[2].worst.unheldT | 847.902 | 847.903 |
| research/analysis/energy-rotor-range.json#rows[4].worstUnheldT | 17.441 | 17.577 |
| research/analysis/energy-unheld.json#rows[0].phases[0].progress | 0.686523 | 0.686342 |
| research/analysis/energy-unheld.json#rows[0].phases[0].secondsIntoPhase | 82.383 | 82.361 |
| research/analysis/energy-unheld.json#rows[0].phases[1].cycleMinute | 7.953 | 7.955 |
| research/analysis/energy-unheld.json#rows[0].phases[1].progress | 0.222656 | 0.222832 |
| research/analysis/energy-unheld.json#rows[0].phases[1].secondsIntoPhase | 157.169 | 157.293 |
| research/analysis/energy-unheld.json#rows[0].phases[1].verticalSpeedMps | 9.750 | 9.745 |
| research/analysis/energy-unheld.json#rows[0].phases[2].cycleMinute | 31.967 | 31.969 |
| research/analysis/energy-unheld.json#rows[0].phases[2].progress | 0.810547 | 0.810707 |
| research/analysis/energy-unheld.json#rows[0].phases[2].secondsIntoPhase | 572.151 | 572.264 |
| research/analysis/energy-unheld.json#rows[0].phases[2].verticalSpeedMps | -8.823 | -8.821 |
| research/analysis/energy-unheld.json#rows[1].phases[0].progress | 0.686523 | 0.686342 |
| research/analysis/energy-unheld.json#rows[1].phases[0].secondsIntoPhase | 82.383 | 82.361 |
| research/analysis/energy-unheld.json#rows[1].phases[1].cycleMinute | 7.953 | 7.955 |
| research/analysis/energy-unheld.json#rows[1].phases[1].progress | 0.222656 | 0.222832 |
| research/analysis/energy-unheld.json#rows[1].phases[1].secondsIntoPhase | 157.169 | 157.293 |
| research/analysis/energy-unheld.json#rows[1].phases[1].verticalSpeedMps | 9.750 | 9.745 |
| research/analysis/energy-unheld.json#rows[4].phases[0].progress | 0.713867 | 0.713996 |
| research/analysis/energy-unheld.json#rows[4].phases[0].secondsIntoPhase | 128.496 | 128.519 |
| research/analysis/energy-unheld.json#rows[4].phases[0].unheldT | 818.462 | 818.465 |
| research/analysis/energy-unheld.json#rows[4].phases[0].verticalSpeedMps | -7.595 | -7.594 |
| research/analysis/energy-unheld.json#rows[4].phases[4].airspeedMps | 9.306 | 9.167 |
| research/analysis/energy-unheld.json#rows[4].phases[4].cycleMinute | 35.353 | 35.362 |
| research/analysis/energy-unheld.json#rows[4].phases[4].progress | 0.999023 | 1.000000 |
| research/analysis/energy-unheld.json#rows[4].phases[4].secondsIntoPhase | 576.976 | 577.540 |
| research/analysis/energy-unheld.json#rows[4].phases[4].unheldT | 586.872 | 587.811 |
| research/analysis/energy-unheld.json#rows[5].phases[0].progress | 0.713867 | 0.713996 |
| research/analysis/energy-unheld.json#rows[5].phases[0].secondsIntoPhase | 128.496 | 128.519 |
| research/analysis/energy-unheld.json#rows[5].phases[0].unheldT | 818.462 | 818.465 |
| research/analysis/energy-unheld.json#rows[5].phases[0].verticalSpeedMps | -7.595 | -7.594 |
| research/analysis/energy-unheld.json#rows[5].phases[4].airspeedMps | 9.306 | 9.167 |
| research/analysis/energy-unheld.json#rows[5].phases[4].cycleMinute | 35.353 | 35.362 |
| research/analysis/energy-unheld.json#rows[5].phases[4].progress | 0.999023 | 1.000000 |
| research/analysis/energy-unheld.json#rows[5].phases[4].secondsIntoPhase | 576.976 | 577.540 |
| research/analysis/energy-unheld.json#rows[5].phases[4].unheldT | 513.460 | 516.352 |
| research/analysis/energy-unheld.json#rows[6].phases[0].progress | 0.713867 | 0.713996 |
| research/analysis/energy-unheld.json#rows[6].phases[0].secondsIntoPhase | 128.496 | 128.519 |
| research/analysis/energy-unheld.json#rows[6].phases[0].unheldT | 768.403 | 768.406 |
| research/analysis/energy-unheld.json#rows[6].phases[0].verticalSpeedMps | -7.595 | -7.594 |
| research/analysis/energy-unheld.json#rows[6].phases[4].airspeedMps | 9.306 | 9.167 |
| research/analysis/energy-unheld.json#rows[6].phases[4].cycleMinute | 93.079 | 93.116 |
| research/analysis/energy-unheld.json#rows[6].phases[4].progress | 0.999023 | 1.000000 |
| research/analysis/energy-unheld.json#rows[6].phases[4].secondsIntoPhase | 2307.904 | 2310.160 |
| research/analysis/energy-unheld.json#rows[6].phases[4].unheldT | 564.434 | 565.351 |
| research/analysis/energy-unheld.json#rows[7].phases[0].progress | 0.713867 | 0.713996 |
| research/analysis/energy-unheld.json#rows[7].phases[0].secondsIntoPhase | 128.496 | 128.519 |
| research/analysis/energy-unheld.json#rows[7].phases[0].unheldT | 768.403 | 768.406 |
| research/analysis/energy-unheld.json#rows[7].phases[0].verticalSpeedMps | -7.595 | -7.594 |
| research/analysis/energy-unheld.json#rows[7].phases[4].airspeedMps | 9.306 | 9.167 |
| research/analysis/energy-unheld.json#rows[7].phases[4].cycleMinute | 93.079 | 93.116 |
| research/analysis/energy-unheld.json#rows[7].phases[4].progress | 0.999023 | 1.000000 |
| research/analysis/energy-unheld.json#rows[7].phases[4].secondsIntoPhase | 2307.904 | 2310.160 |
| research/analysis/energy-unheld.json#rows[7].phases[4].unheldT | 491.022 | 493.892 |
| research/analysis/energy-unheld.json#rows[8].phases[0].cycleMinute | 3.330 | 3.335 |
| research/analysis/energy-unheld.json#rows[8].phases[0].progress | 0.666016 | 0.666936 |
| research/analysis/energy-unheld.json#rows[8].phases[0].secondsIntoPhase | 199.805 | 200.081 |
| research/analysis/energy-unheld.json#rows[8].phases[0].unheldT | 7070.369 | 7073.819 |
| research/analysis/energy-unheld.json#rows[8].phases[0].verticalSpeedMps | -6.486 | -6.485 |
| research/analysis/energy-unheld.json#rows[9].phases[0].cycleMinute | 3.330 | 3.335 |
| research/analysis/energy-unheld.json#rows[9].phases[0].progress | 0.666016 | 0.666936 |
| research/analysis/energy-unheld.json#rows[9].phases[0].secondsIntoPhase | 199.805 | 200.081 |
| research/analysis/energy-unheld.json#rows[9].phases[0].unheldT | 7070.369 | 7073.819 |
| research/analysis/energy-unheld.json#rows[9].phases[0].verticalSpeedMps | -6.486 | -6.485 |
| research/analysis/energy-unheld.json#rows[9].phases[4].airspeedMps | 10.998 | 10.833 |
| research/analysis/energy-unheld.json#rows[9].phases[4].cycleMinute | 45.504 | 45.512 |
| research/analysis/energy-unheld.json#rows[9].phases[4].progress | 0.999023 | 1.000000 |
| research/analysis/energy-unheld.json#rows[9].phases[4].secondsIntoPhase | 488.211 | 488.688 |
| research/analysis/energy-unheld.json#rows[9].phases[4].unheldT | 3940.050 | 3968.748 |
| research/analysis/energy-unheld.json#rows[10].phases[0].cycleMinute | 3.330 | 3.335 |
| research/analysis/energy-unheld.json#rows[10].phases[0].progress | 0.666016 | 0.666936 |
| research/analysis/energy-unheld.json#rows[10].phases[0].secondsIntoPhase | 199.805 | 200.081 |
| research/analysis/energy-unheld.json#rows[10].phases[0].unheldT | 6957.060 | 6960.523 |
| research/analysis/energy-unheld.json#rows[10].phases[0].verticalSpeedMps | -6.486 | -6.485 |
| research/analysis/energy-unheld.json#rows[11].phases[0].cycleMinute | 3.330 | 3.335 |
| research/analysis/energy-unheld.json#rows[11].phases[0].progress | 0.666016 | 0.666936 |
| research/analysis/energy-unheld.json#rows[11].phases[0].secondsIntoPhase | 199.805 | 200.081 |
| research/analysis/energy-unheld.json#rows[11].phases[0].unheldT | 6957.060 | 6960.523 |
| research/analysis/energy-unheld.json#rows[11].phases[0].verticalSpeedMps | -6.486 | -6.485 |
| research/analysis/energy-unheld.json#rows[11].phases[4].airspeedMps | 10.998 | 10.833 |
| research/analysis/energy-unheld.json#rows[11].phases[4].cycleMinute | 94.349 | 94.381 |
| research/analysis/energy-unheld.json#rows[11].phases[4].progress | 0.999023 | 1.000000 |
| research/analysis/energy-unheld.json#rows[11].phases[4].secondsIntoPhase | 1952.842 | 1954.751 |
| research/analysis/energy-unheld.json#rows[11].phases[4].unheldT | 3876.763 | 3905.400 |
| tests/energy/unheld.mjs#namedEndurance.worstUnheldT | 1.686282096 | 2.041455599 |

### Part B

Bisect held force with the least-power split until the available bus is spent.

| Generated record and field | Earlier | Current |
|---|---|---|
| research/analysis/descent.json#classes.P100.withoutTheBag.worst.progress | 0.810547 | 0.810707 |
| research/analysis/descent.json#classes.P100.worst.progress | 0.810547 | 0.810707 |
| research/analysis/descent.json#classes.P1000.withoutTheBag.worst.progress | 0.719727 | 0.719805 |
| research/analysis/descent.json#classes.P10000.withoutTheBag.worst.progress | 0.793945 | 0.793873 |
| research/analysis/descent.json#favourableClasses.P100.withoutTheBag.worst.progress | 0.222656 | 0.222832 |
| research/analysis/descent.json#favourableClasses.P100.worst.progress | 0.222656 | 0.222832 |
| research/analysis/descent.json#favourableClasses.P1000.cycle.eCycleMWh | 61.155 | 61.355 |
| research/analysis/descent.json#favourableClasses.P1000.cycle.kwhPerTonne | 61.160 | 61.360 |
| research/analysis/descent.json#favourableClasses.P1000.letdown.clippedMWh | 9.769 | 9.573 |
| research/analysis/descent.json#favourableClasses.P1000.letdown.mwh | 9.256 | 9.319 |
| research/analysis/descent.json#favourableClasses.P1000.letdown.pctOfCycle | 15.100 | 15.200 |
| research/analysis/descent.json#favourableClasses.P1000.letdown.rotorsPctOfCycle | 70.300 | 70.400 |
| research/analysis/descent.json#favourableClasses.P1000.letdown.rotorsWholeCycleMWh | 42.993 | 43.189 |
| research/analysis/descent.json#favourableClasses.P1000.profile[0].owners.aeroT | 515.436 | 515.492 |
| research/analysis/descent.json#favourableClasses.P1000.profile[0].owners.rotorT | 500.949 | 501.022 |
| research/analysis/descent.json#favourableClasses.P1000.profile[0].thrustT | 500.900 | 501.000 |
| research/analysis/descent.json#favourableClasses.P1000.profile[0].unheldT | 133.628 | 133.500 |
| research/analysis/descent.json#favourableClasses.P1000.profile[1].owners.aeroT | 519.328 | 519.462 |
| research/analysis/descent.json#favourableClasses.P1000.profile[1].owners.rotorT | 473.252 | 473.422 |
| research/analysis/descent.json#favourableClasses.P1000.profile[1].thrustT | 473.300 | 473.400 |
| research/analysis/descent.json#favourableClasses.P1000.profile[1].unheldT | 173.562 | 173.258 |
| research/analysis/descent.json#favourableClasses.P1000.profile[2].owners.aeroT | 522.646 | 522.857 |
| research/analysis/descent.json#favourableClasses.P1000.profile[2].owners.rotorT | 458.341 | 458.611 |
| research/analysis/descent.json#favourableClasses.P1000.profile[2].thrustT | 458.300 | 458.600 |
| research/analysis/descent.json#favourableClasses.P1000.profile[2].unheldT | 201.817 | 201.336 |
| research/analysis/descent.json#favourableClasses.P1000.profile[3].owners.aeroT | 524.664 | 524.914 |
| research/analysis/descent.json#favourableClasses.P1000.profile[3].owners.rotorT | 455.760 | 456.078 |
| research/analysis/descent.json#favourableClasses.P1000.profile[3].rotorsMW | 62.000 | 62.100 |
| research/analysis/descent.json#favourableClasses.P1000.profile[3].thrustT | 455.800 | 456.100 |
| research/analysis/descent.json#favourableClasses.P1000.profile[3].unheldT | 216.892 | 216.325 |
| research/analysis/descent.json#favourableClasses.P1000.profile[4].owners.aeroT | 525.083 | 525.309 |
| research/analysis/descent.json#favourableClasses.P1000.profile[4].owners.rotorT | 465.542 | 465.830 |
| research/analysis/descent.json#favourableClasses.P1000.profile[4].rotorsMW | 62.200 | 62.300 |
| research/analysis/descent.json#favourableClasses.P1000.profile[4].thrustT | 465.500 | 465.800 |
| research/analysis/descent.json#favourableClasses.P1000.profile[4].unheldT | 217.378 | 216.865 |
| research/analysis/descent.json#favourableClasses.P1000.profile[5].owners.aeroT | 512.250 | 512.408 |
| research/analysis/descent.json#favourableClasses.P1000.profile[5].owners.rotorT | 491.834 | 492.041 |
| research/analysis/descent.json#favourableClasses.P1000.profile[5].thrustT | 491.800 | 492.000 |
| research/analysis/descent.json#favourableClasses.P1000.profile[5].unheldT | 208.655 | 208.291 |
| research/analysis/descent.json#favourableClasses.P1000.profile[6].owners.aeroT | 473.962 | 474.113 |
| research/analysis/descent.json#favourableClasses.P1000.profile[6].owners.rotorT | 517.563 | 517.780 |
| research/analysis/descent.json#favourableClasses.P1000.profile[6].rotorsMW | 68.200 | 68.300 |
| research/analysis/descent.json#favourableClasses.P1000.profile[6].thrustT | 517.600 | 517.800 |
| research/analysis/descent.json#favourableClasses.P1000.profile[6].unheldT | 222.193 | 221.826 |
| research/analysis/descent.json#favourableClasses.P1000.profile[7].owners.aeroT | 427.841 | 428.090 |
| research/analysis/descent.json#favourableClasses.P1000.profile[7].owners.rotorT | 525.514 | 525.930 |
| research/analysis/descent.json#favourableClasses.P1000.profile[7].rotorsMW | 72.500 | 72.600 |
| research/analysis/descent.json#favourableClasses.P1000.profile[7].thrustT | 525.500 | 525.900 |
| research/analysis/descent.json#favourableClasses.P1000.profile[7].unheldT | 261.638 | 260.973 |
| research/analysis/descent.json#favourableClasses.P1000.profile[8].owners.aeroT | 367.840 | 371.373 |
| research/analysis/descent.json#favourableClasses.P1000.profile[8].owners.rotorT | 515.146 | 522.524 |
| research/analysis/descent.json#favourableClasses.P1000.profile[8].rotorsMW | 76.300 | 78.300 |
| research/analysis/descent.json#favourableClasses.P1000.profile[8].thrustT | 515.100 | 522.500 |
| research/analysis/descent.json#favourableClasses.P1000.profile[8].unheldT | 332.794 | 321.883 |
| research/analysis/descent.json#favourableClasses.P1000.profile[9].owners.rotorT | 564.979 | 582.697 |
| research/analysis/descent.json#favourableClasses.P1000.profile[9].rotorsMW | 99.600 | 104.900 |
| research/analysis/descent.json#favourableClasses.P1000.profile[9].thrustT | 565.000 | 582.700 |
| research/analysis/descent.json#favourableClasses.P1000.profile[9].unheldT | 425.294 | 407.576 |
| research/analysis/descent.json#favourableClasses.P1000.profile[10].owners.rotorT | 589.923 | 603.074 |
| research/analysis/descent.json#favourableClasses.P1000.profile[10].rotorsMW | 117.000 | 121.200 |
| research/analysis/descent.json#favourableClasses.P1000.profile[10].thrustT | 589.900 | 603.100 |
| research/analysis/descent.json#favourableClasses.P1000.profile[10].unheldT | 516.269 | 503.118 |
| research/analysis/descent.json#favourableClasses.P1000.profile[11].owners.rotorT | 669.814 | 677.139 |
| research/analysis/descent.json#favourableClasses.P1000.profile[11].rotorsMW | 143.000 | 145.500 |
| research/analysis/descent.json#favourableClasses.P1000.profile[11].thrustT | 669.800 | 677.100 |
| research/analysis/descent.json#favourableClasses.P1000.profile[11].unheldT | 436.473 | 429.148 |
| research/analysis/descent.json#favourableClasses.P1000.profile[12].owners.rotorT | 671.721 | 676.667 |
| research/analysis/descent.json#favourableClasses.P1000.profile[12].rotorsMW | 148.700 | 150.400 |
| research/analysis/descent.json#favourableClasses.P1000.profile[12].thrustT | 671.700 | 676.700 |
| research/analysis/descent.json#favourableClasses.P1000.profile[12].unheldT | 484.173 | 479.228 |
| research/analysis/descent.json#favourableClasses.P1000.profile[13].owners.rotorT | 668.807 | 669.658 |
| research/analysis/descent.json#favourableClasses.P1000.profile[13].rotorsMW | 153.400 | 153.700 |
| research/analysis/descent.json#favourableClasses.P1000.profile[13].thrustT | 668.800 | 669.700 |
| research/analysis/descent.json#favourableClasses.P1000.profile[13].unheldT | 539.997 | 539.146 |
| research/analysis/descent.json#favourableClasses.P1000.rotorsBlindToTheBag.eCycleMWh | 63.879 | 64.079 |
| research/analysis/descent.json#favourableClasses.P1000.rotorsBlindToTheBag.letdownMWh | 10.821 | 10.884 |
| research/analysis/descent.json#favourableClasses.P1000.withoutTheBag.eCycleMWh | 63.879 | 64.079 |
| research/analysis/descent.json#favourableClasses.P1000.withoutTheBag.kwhPerTonne | 63.880 | 64.080 |
| research/analysis/descent.json#favourableClasses.P1000.withoutTheBag.letdownMWh | 10.880 | 10.943 |
| research/analysis/descent.json#favourableClasses.P1000.withoutTheBag.worst.progress | 0.719727 | 0.719805 |
| research/analysis/descent.json#favourableClasses.P10000.cycle.eCycleMWh | 757.615 | 766.285 |
| research/analysis/descent.json#favourableClasses.P10000.cycle.kwhPerTonne | 75.760 | 76.630 |
| research/analysis/descent.json#favourableClasses.P10000.letdown.clippedMWh | 41.887 | 41.722 |
| research/analysis/descent.json#favourableClasses.P10000.letdown.mwh | 116.494 | 116.531 |
| research/analysis/descent.json#favourableClasses.P10000.letdown.pctOfCycle | 15.400 | 15.200 |
| research/analysis/descent.json#favourableClasses.P10000.letdown.rotorsPctOfCycle | 83.200 | 82.300 |
| research/analysis/descent.json#favourableClasses.P10000.letdown.rotorsWholeCycleMWh | 630.225 | 630.390 |
| research/analysis/descent.json#favourableClasses.P10000.profile[0].owners.aeroT | 3891.224 | 4033.217 |
| research/analysis/descent.json#favourableClasses.P10000.profile[0].unheldT | 499.351 | 357.359 |
| research/analysis/descent.json#favourableClasses.P10000.profile[1].owners.aeroT | 3893.268 | 4032.311 |
| research/analysis/descent.json#favourableClasses.P10000.profile[1].unheldT | 489.176 | 350.134 |
| research/analysis/descent.json#favourableClasses.P10000.profile[2].owners.aeroT | 3895.663 | 4031.199 |
| research/analysis/descent.json#favourableClasses.P10000.profile[2].unheldT | 477.073 | 341.537 |
| research/analysis/descent.json#favourableClasses.P10000.profile[3].owners.aeroT | 3898.165 | 4029.997 |
| research/analysis/descent.json#favourableClasses.P10000.profile[3].unheldT | 464.280 | 332.448 |
| research/analysis/descent.json#favourableClasses.P10000.profile[4].owners.aeroT | 3900.551 | 4028.823 |
| research/analysis/descent.json#favourableClasses.P10000.profile[4].unheldT | 451.971 | 323.700 |
| research/analysis/descent.json#favourableClasses.P10000.profile[5].owners.aeroT | 3693.330 | 3874.647 |
| research/analysis/descent.json#favourableClasses.P10000.profile[5].unheldT | 650.687 | 469.370 |
| research/analysis/descent.json#favourableClasses.P10000.profile[6].owners.aeroT | 3040.000 | 3379.677 |
| research/analysis/descent.json#favourableClasses.P10000.profile[6].unheldT | 1298.292 | 958.615 |
| research/analysis/descent.json#favourableClasses.P10000.profile[7].owners.aeroT | 2527.132 | 2779.862 |
| research/analysis/descent.json#favourableClasses.P10000.profile[7].owners.rotorT | 7326.286 | 7326.287 |
| research/analysis/descent.json#favourableClasses.P10000.profile[7].unheldT | 1807.845 | 1555.115 |
| research/analysis/descent.json#favourableClasses.P10000.profile[8].owners.aeroT | 2021.597 | 2059.667 |
| research/analysis/descent.json#favourableClasses.P10000.profile[8].unheldT | 2311.689 | 2273.618 |
| research/analysis/descent.json#favourableClasses.P10000.profile[9].owners.rotorT | 7136.099 | 7139.978 |
| research/analysis/descent.json#favourableClasses.P10000.profile[9].rotorsMW | 1148.300 | 1149.400 |
| research/analysis/descent.json#favourableClasses.P10000.profile[9].thrustT | 7136.100 | 7140.000 |
| research/analysis/descent.json#favourableClasses.P10000.profile[9].unheldT | 3100.320 | 3096.440 |
| research/analysis/descent.json#favourableClasses.P10000.profile[10].owners.rotorT | 6999.698 | 7011.721 |
| research/analysis/descent.json#favourableClasses.P10000.profile[10].rotorsMW | 1267.000 | 1270.500 |
| research/analysis/descent.json#favourableClasses.P10000.profile[10].thrustT | 6999.700 | 7011.700 |
| research/analysis/descent.json#favourableClasses.P10000.profile[10].unheldT | 3967.928 | 3955.906 |
| research/analysis/descent.json#favourableClasses.P10000.profile[11].owners.rotorT | 7254.696 | 7257.334 |
| research/analysis/descent.json#favourableClasses.P10000.profile[11].rotorsMW | 1343.100 | 1343.900 |
| research/analysis/descent.json#favourableClasses.P10000.profile[11].thrustT | 7254.700 | 7257.300 |
| research/analysis/descent.json#favourableClasses.P10000.profile[11].unheldT | 3713.531 | 3710.892 |
| research/analysis/descent.json#favourableClasses.P10000.profile[12].owners.rotorT | 7111.485 | 7117.669 |
| research/analysis/descent.json#favourableClasses.P10000.profile[12].rotorsMW | 1378.700 | 1380.600 |
| research/analysis/descent.json#favourableClasses.P10000.profile[12].thrustT | 7111.500 | 7117.700 |
| research/analysis/descent.json#favourableClasses.P10000.profile[12].unheldT | 4168.637 | 4162.453 |
| research/analysis/descent.json#favourableClasses.P10000.profile[13].owners.rotorT | 6900.409 | 6902.707 |
| research/analysis/descent.json#favourableClasses.P10000.profile[13].rotorsMW | 1403.900 | 1404.600 |
| research/analysis/descent.json#favourableClasses.P10000.profile[13].thrustT | 6900.400 | 6902.700 |
| research/analysis/descent.json#favourableClasses.P10000.profile[13].unheldT | 4712.422 | 4710.124 |
| research/analysis/descent.json#favourableClasses.P10000.rotorsBlindToTheBag.creditSavesPctOfCycle | 6.500 | 6.400 |
| research/analysis/descent.json#favourableClasses.P10000.rotorsBlindToTheBag.eCycleMWh | 810.386 | 819.057 |
| research/analysis/descent.json#favourableClasses.P10000.rotorsBlindToTheBag.letdownMWh | 146.520 | 146.557 |
| research/analysis/descent.json#favourableClasses.P10000.withoutTheBag.bagCostsCyclePct | -6.500 | -6.400 |
| research/analysis/descent.json#favourableClasses.P10000.withoutTheBag.bagCostsPerTonnePct | -6.500 | -6.400 |
| research/analysis/descent.json#favourableClasses.P10000.withoutTheBag.eCycleMWh | 810.386 | 819.057 |
| research/analysis/descent.json#favourableClasses.P10000.withoutTheBag.kwhPerTonne | 81.040 | 81.910 |
| research/analysis/descent.json#favourableClasses.P10000.withoutTheBag.letdownMWh | 147.116 | 147.153 |
| research/analysis/descent.json#favourableClasses.P10000.withoutTheBag.worst.progress | 0.793945 | 0.793873 |
| research/analysis/energy-bag-comparison.json#rows[4].completed.lastInfeasible | 871.846 | 871.845 |
| research/analysis/energy-bag-comparison.json#rows[4].completed.threshold | 871.846 | 871.845 |
| research/analysis/energy-bag-comparison.json#rows[5].completed.lastInfeasible | 871.846 | 871.845 |
| research/analysis/energy-bag-comparison.json#rows[5].completed.threshold | 871.846 | 871.845 |
| research/analysis/energy-bag-comparison.json#rows[8].completed.ballastT | 7471.994 | 7471.996 |
| research/analysis/energy-bag-comparison.json#rows[8].completed.deliveredT | 2528.006 | 2528.004 |
| research/analysis/energy-bag-comparison.json#rows[8].completed.lastInfeasible | 7471.994 | 7471.995 |
| research/analysis/energy-bag-comparison.json#rows[8].completed.peakRotorMW | 1288.928 | 1288.927 |
| research/analysis/energy-bag-comparison.json#rows[8].completed.printed | 7471.994 | 7471.996 |
| research/analysis/energy-bag-comparison.json#rows[8].completed.threshold | 7471.994 | 7471.995 |
| research/analysis/energy-bag-comparison.json#rows[8].completed.worst.unheldT | 0.001 | 0.003 |
| research/analysis/energy-bag-comparison.json#rows[8].extraRetainedT | 398.180 | 398.182 |
| research/analysis/energy-bag-comparison.json#rows[9].completed.ballastT | 7471.994 | 7471.996 |
| research/analysis/energy-bag-comparison.json#rows[9].completed.deliveredT | 2528.006 | 2528.004 |
| research/analysis/energy-bag-comparison.json#rows[9].completed.lastInfeasible | 7471.994 | 7471.995 |
| research/analysis/energy-bag-comparison.json#rows[9].completed.peakRotorMW | 1288.928 | 1288.927 |
| research/analysis/energy-bag-comparison.json#rows[9].completed.printed | 7471.994 | 7471.996 |
| research/analysis/energy-bag-comparison.json#rows[9].completed.threshold | 7471.994 | 7471.995 |
| research/analysis/energy-bag-comparison.json#rows[9].completed.worst.unheldT | 0.001 | 0.003 |
| research/analysis/energy-bag-comparison.json#rows[9].extraRetainedT | 398.180 | 398.182 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.ballastT | 7357.170 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.cycleMWh | 445.956 | 445.957 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.deliveredT | 2642.830 | 2642.840 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.lastInfeasible | 7357.169 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.peakRotorMW | 1309.451 | 1309.454 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.printed | 7357.170 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.threshold | 7357.169 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[10].completed.worst.unheldT | 0.004 | 0.000 |
| research/analysis/energy-bag-comparison.json#rows[10].extraRetainedT | 396.652 | 396.642 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.ballastT | 7357.170 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.cycleMWh | 395.165 | 395.166 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.deliveredT | 2642.830 | 2642.840 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.lastInfeasible | 7357.169 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.peakRotorMW | 1309.451 | 1309.454 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.printed | 7357.170 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.threshold | 7357.169 | 7357.160 |
| research/analysis/energy-bag-comparison.json#rows[11].completed.worst.unheldT | 0.004 | 0.000 |
| research/analysis/energy-bag-comparison.json#rows[11].extraRetainedT | 396.652 | 396.642 |
| research/analysis/energy-closure.json#rows[1].requirements.dragSensitivity[0].worst.progress | 0.702318 | 0.702320 |
| research/analysis/energy-closure.json#rows[5].current.cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].current.hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-closure.json#rows[5].current.kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].requirements.baseline.cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].requirements.baseline.hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-closure.json#rows[5].requirements.baseline.kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[0].cycleMWh | 61.517 | 61.758 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[0].hoursOnBattery | 1.164 | 1.159 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[0].kwhPerTonne | 61.517 | 61.758 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[1].cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[1].hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[1].kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[2].cycleMWh | 61.009 | 61.171 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[2].hoursOnBattery | 1.174 | 1.170 |
| research/analysis/energy-closure.json#rows[5].requirements.clSensitivity[2].kwhPerTonne | 61.009 | 61.171 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[0].cycleMWh | 60.962 | 61.162 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[0].hoursOnBattery | 1.174 | 1.171 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[0].kwhPerTonne | 60.962 | 61.162 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[1].cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[1].hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[1].kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[2].cycleMWh | 61.466 | 61.666 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[2].hoursOnBattery | 1.165 | 1.161 |
| research/analysis/energy-closure.json#rows[5].requirements.dragSensitivity[2].kwhPerTonne | 61.466 | 61.666 |
| research/analysis/energy-closure.json#rows[7].current.cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].current.hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-closure.json#rows[7].current.kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].requirements.baseline.cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].requirements.baseline.hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-closure.json#rows[7].requirements.baseline.kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[0].cycleMWh | 142.528 | 143.065 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[0].hoursOnBattery | 1.325 | 1.320 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[0].kwhPerTonne | 142.528 | 143.065 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[1].cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[1].hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[1].kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[2].cycleMWh | 142.027 | 142.241 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[2].hoursOnBattery | 1.330 | 1.328 |
| research/analysis/energy-closure.json#rows[7].requirements.clSensitivity[2].kwhPerTonne | 142.027 | 142.241 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[0].cycleMWh | 142.073 | 142.404 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[0].hoursOnBattery | 1.329 | 1.326 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[0].kwhPerTonne | 142.073 | 142.404 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[1].cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[1].hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[1].kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[2].cycleMWh | 142.232 | 142.562 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[2].hoursOnBattery | 1.328 | 1.324 |
| research/analysis/energy-closure.json#rows[7].requirements.dragSensitivity[2].kwhPerTonne | 142.232 | 142.562 |
| research/analysis/energy-closure.json#rows[9].current.cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-closure.json#rows[9].current.hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-closure.json#rows[9].current.kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-closure.json#rows[9].requirements.baseline.cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-closure.json#rows[9].requirements.baseline.hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-closure.json#rows[9].requirements.baseline.kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[0].cycleMWh | 753.350 | 753.408 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[0].kwhPerTonne | 75.335 | 75.341 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[1].cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[1].hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[1].kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[2].cycleMWh | 754.912 | 765.203 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[2].hoursOnBattery | 2.021 | 1.993 |
| research/analysis/energy-closure.json#rows[9].requirements.clSensitivity[2].kwhPerTonne | 75.491 | 76.520 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[0].cycleMWh | 756.441 | 765.272 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[0].hoursOnBattery | 2.016 | 1.993 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[0].kwhPerTonne | 75.644 | 76.527 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[1].cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[1].hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[1].kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[2].cycleMWh | 758.981 | 767.490 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[2].hoursOnBattery | 2.010 | 1.987 |
| research/analysis/energy-closure.json#rows[9].requirements.dragSensitivity[2].kwhPerTonne | 75.898 | 76.749 |
| research/analysis/energy-closure.json#rows[11].current.cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-closure.json#rows[11].current.hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-closure.json#rows[11].current.kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-closure.json#rows[11].requirements.baseline.cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-closure.json#rows[11].requirements.baseline.hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-closure.json#rows[11].requirements.baseline.kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[0].cycleMWh | 1355.989 | 1356.363 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[0].hoursOnBattery | 2.335 | 2.334 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[0].kwhPerTonne | 135.599 | 135.636 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[1].cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[1].hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[1].kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[2].cycleMWh | 1369.068 | 1385.070 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[2].hoursOnBattery | 2.312 | 2.285 |
| research/analysis/energy-closure.json#rows[11].requirements.clSensitivity[2].kwhPerTonne | 136.907 | 138.507 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[0].cycleMWh | 1372.867 | 1385.795 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[0].hoursOnBattery | 2.306 | 2.284 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[0].kwhPerTonne | 137.287 | 138.579 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[1].cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[1].hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[1].kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[2].cycleMWh | 1373.947 | 1386.831 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[2].hoursOnBattery | 2.304 | 2.282 |
| research/analysis/energy-closure.json#rows[11].requirements.dragSensitivity[2].kwhPerTonne | 137.395 | 138.683 |
| research/analysis/energy-documents.json#readmeExamples[1].cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-documents.json#readmeExamples[1].hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-documents.json#readmeExamples[1].kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-documents.json#readmeExamples[3].cycleMWh | 1168.581 | 1178.889 |
| research/analysis/energy-documents.json#readmeExamples[3].hoursOnBattery | 2.241 | 2.221 |
| research/analysis/energy-documents.json#readmeExamples[3].kwhPerTonne | 116.858 | 117.889 |
| research/analysis/energy-documents.json#records[5].asDrawn.cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-documents.json#records[5].asDrawn.hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-documents.json#records[5].asDrawn.kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-documents.json#records[5].channels.prop | 13.790 | 13.795 |
| research/analysis/energy-documents.json#records[5].channels.rotors | 42.993 | 43.189 |
| research/analysis/energy-documents.json#records[5].letdownMWh | 9.256 | 9.319 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.BUOYANCY_ESCAPE | 4.995 | 5.042 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.RETURN_TRANSIT | 24.216 | 24.266 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.SOURCE_APPROACH | 6.184 | 6.201 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.WATER_RELEASE | 10.639 | 10.726 |
| research/analysis/energy-documents.json#records[7].asDrawn.cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-documents.json#records[7].asDrawn.hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-documents.json#records[7].asDrawn.kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-documents.json#records[7].channels.prop | 48.961 | 48.970 |
| research/analysis/energy-documents.json#records[7].channels.rotors | 79.905 | 80.226 |
| research/analysis/energy-documents.json#records[7].letdownMWh | 19.569 | 19.757 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.BUOYANCY_ESCAPE | 4.996 | 5.042 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.RETURN_TRANSIT | 96.839 | 97.026 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.SOURCE_APPROACH | 6.615 | 6.625 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.WATER_RELEASE | 10.639 | 10.726 |
| research/analysis/energy-documents.json#records[9].asDrawn.cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-documents.json#records[9].asDrawn.hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-documents.json#records[9].asDrawn.kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-documents.json#records[9].channels.prop | 105.637 | 114.142 |
| research/analysis/energy-documents.json#records[9].channels.rotors | 630.225 | 630.390 |
| research/analysis/energy-documents.json#records[9].letdownMWh | 116.494 | 116.531 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.BUOYANCY_ESCAPE | 46.087 | 46.787 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.RETURN_TRANSIT | 182.943 | 190.778 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.SOURCE_APPROACH | 87.636 | 87.661 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.WATER_RELEASE | 200.675 | 200.785 |
| research/analysis/energy-documents.json#records[11].asDrawn.cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-documents.json#records[11].asDrawn.hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-documents.json#records[11].asDrawn.kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-documents.json#records[11].channels.prop | 370.205 | 382.918 |
| research/analysis/energy-documents.json#records[11].channels.rotors | 955.940 | 956.133 |
| research/analysis/energy-documents.json#records[11].letdownMWh | 216.398 | 216.463 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.BUOYANCY_ESCAPE | 46.199 | 46.786 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.RETURN_TRANSIT | 737.130 | 749.322 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.SOURCE_APPROACH | 88.677 | 88.693 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.WATER_RELEASE | 200.675 | 200.785 |
| research/analysis/energy-documents.json#sensitivity[18].rows[0].energyPct | 1.998 | 4.926 |
| research/analysis/energy-documents.json#sensitivity[18].rows[1].energyPct | -6.130 | -7.118 |
| research/analysis/energy-documents.json#sensitivity[19].rows[0].energyPct | -0.167 | -0.243 |
| research/analysis/energy-documents.json#sensitivity[19].rows[1].energyPct | 0.172 | 0.243 |
| research/analysis/energy-documents.json#sensitivity[21].rows[0].energyPct | 0.182 | 0.180 |
| research/analysis/energy-documents.json#sensitivity[21].rows[1].energyPct | -0.122 | -0.120 |
| research/analysis/energy-documents.json#sensitivity[22].rows[0].energyPct | -0.265 | -0.076 |
| research/analysis/energy-documents.json#sensitivity[22].rows[1].energyPct | 0.292 | 0.103 |
| research/analysis/energy-documents.json#sensitivity[23].rows[0].energyPct | -40.815 | -41.471 |
| research/analysis/energy-documents.json#sensitivity[23].rows[1].energyPct | 20.987 | 25.441 |
| research/analysis/energy-documents.json#sensitivity[24].rows[0].energyPct | 0.022 | 0.021 |
| research/analysis/energy-documents.json#sensitivity[24].rows[1].energyPct | -0.022 | -0.021 |
| research/analysis/energy-documents.json#sensitivity[25].rows[0].energyPct | -0.002 | -0.006 |
| research/analysis/energy-documents.json#sensitivity[25].rows[1].energyPct | 0.001 | 0.004 |
| research/analysis/energy-documents.json#sensitivity[26].rows[0].energyPct | -0.064 | -0.058 |
| research/analysis/energy-documents.json#sensitivity[26].rows[1].energyPct | 0.064 | 0.058 |
| research/analysis/energy-documents.json#sensitivity[27].rows[0].energyPct | 5.999 | 6.480 |
| research/analysis/energy-documents.json#sensitivity[27].rows[1].energyPct | -3.638 | -4.149 |
| research/analysis/energy-documents.json#sensitivity[28].rows[0].energyPct | 3.247 | 3.211 |
| research/analysis/energy-documents.json#sensitivity[28].rows[1].energyPct | -1.266 | -1.251 |
| research/analysis/energy-documents.json#sensitivity[29].rows[0].energyPct | 0.612 | 0.610 |
| research/analysis/energy-documents.json#sensitivity[29].rows[1].energyPct | -0.727 | -0.723 |
| research/analysis/energy-documents.json#sensitivity[30].rows[0].energyPct | 14.247 | 14.095 |
| research/analysis/energy-documents.json#sensitivity[30].rows[1].energyPct | -9.592 | -9.490 |
| research/analysis/energy-documents.json#sensitivity[31].rows[0].energyPct | -45.379 | -45.989 |
| research/analysis/energy-documents.json#sensitivity[31].rows[1].energyPct | 22.602 | 26.837 |
| research/analysis/energy-documents.json#sensitivity[32].rows[0].energyPct | 1.911 | 2.471 |
| research/analysis/energy-documents.json#sensitivity[32].rows[1].energyPct | -2.178 | -2.902 |
| research/analysis/energy-documents.json#sensitivity[33].rows[0].energyPct | -18.068 | -15.868 |
| research/analysis/energy-documents.json#sensitivity[33].rows[1].energyPct | 12.281 | 11.090 |
| research/analysis/energy-documents.json#sensitivity[34].rows[0].energyPct | 0.749 | 0.848 |
| research/analysis/energy-documents.json#sensitivity[34].rows[1].energyPct | -0.480 | -0.549 |
| research/analysis/energy-documents.json#sensitivity[35].rows[0].energyPct | -0.064 | -0.058 |
| research/analysis/energy-documents.json#sensitivity[35].rows[1].energyPct | 0.064 | 0.058 |
| research/analysis/energy-feasible.json#rows[0].best.sensitivity[3].worst.progress | 0.669025 | 0.669024 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.kwhPerTonne | 38.684 | 38.685 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.worst.progress | 0.204667 | 0.204662 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.worst.unheldT | 8.727 | 8.686 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].cycleMWh | 1.437 | 1.438 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].worst.progress | 0.203810 | 0.203820 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].worst.unheldT | 48.265 | 46.901 |
| research/analysis/energy-feasible.json#rows[2].asDrawn.worst.progress | 0.804140 | 0.804141 |
| research/analysis/energy-feasible.json#rows[3].asDrawn.worst.progress | 0.684970 | 0.684971 |
| research/analysis/energy-feasible.json#rows[4].best.sensitivity[2].worst.progress | 0.672223 | 0.672224 |
| research/analysis/energy-feasible.json#rows[4].fullDeliveryBest.sensitivity[3].worst.progress | 0.674764 | 0.674763 |
| research/analysis/energy-feasible.json#rows[5].best.sensitivity[2].worst.progress | 0.672599 | 0.672600 |
| research/analysis/energy-feasible.json#rows[5].best.sensitivity[3].cycleMWh | 10.836 | 10.837 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[3].cycleMWh | 11.816 | 11.817 |
| research/analysis/energy-feasible.json#rows[5].fullDeliveryBest.sensitivity[3].worst.progress | 0.674764 | 0.674763 |
| research/analysis/energy-feasible.json#rows[7].asDrawn.cycleMWh | 38.931 | 39.090 |
| research/analysis/energy-feasible.json#rows[7].asDrawn.hoursOnBattery | 1.067 | 1.063 |
| research/analysis/energy-feasible.json#rows[7].asDrawn.kwhPerTonne | 38.931 | 39.090 |
| research/analysis/energy-feasible.json#rows[8].best.sensitivity[2].worst.progress | 0.695420 | 0.695419 |
| research/analysis/energy-feasible.json#rows[9].asDrawn.cycleMWh | 47.601 | 47.776 |
| research/analysis/energy-feasible.json#rows[9].asDrawn.hoursOnBattery | 1.093 | 1.089 |
| research/analysis/energy-feasible.json#rows[9].asDrawn.kwhPerTonne | 47.601 | 47.776 |
| research/analysis/energy-feasible.json#rows[10].best.sensitivity[2].worst.progress | 0.707194 | 0.707193 |
| research/analysis/energy-feasible.json#rows[11].asDrawn.cycleMWh | 127.615 | 127.922 |
| research/analysis/energy-feasible.json#rows[11].asDrawn.hoursOnBattery | 1.315 | 1.311 |
| research/analysis/energy-feasible.json#rows[11].asDrawn.kwhPerTonne | 127.615 | 127.922 |
| research/analysis/energy-feasible.json#rows[11].best.sensitivity[2].worst.progress | 0.707194 | 0.707193 |
| research/analysis/energy-feasible.json#rows[13].asDrawn.cycleMWh | 592.972 | 595.315 |
| research/analysis/energy-feasible.json#rows[13].asDrawn.hoursOnBattery | 1.956 | 1.948 |
| research/analysis/energy-feasible.json#rows[13].asDrawn.kwhPerTonne | 59.297 | 59.532 |
| research/analysis/energy-feasible.json#rows[15].asDrawn.cycleMWh | 652.034 | 658.647 |
| research/analysis/energy-feasible.json#rows[15].asDrawn.hoursOnBattery | 1.919 | 1.900 |
| research/analysis/energy-feasible.json#rows[15].asDrawn.kwhPerTonne | 65.203 | 65.865 |
| research/analysis/energy-feasible.json#rows[17].asDrawn.cycleMWh | 1263.022 | 1274.550 |
| research/analysis/energy-feasible.json#rows[17].asDrawn.hoursOnBattery | 2.273 | 2.252 |
| research/analysis/energy-feasible.json#rows[17].asDrawn.kwhPerTonne | 126.302 | 127.455 |
| research/analysis/energy-model-change.json#currentComparison.rows[5].changeMWh | 43.006 | 43.206 |
| research/analysis/energy-model-change.json#currentComparison.rows[5].currentMWh | 61.155 | 61.355 |
| research/analysis/energy-model-change.json#currentComparison.rows[7].changeMWh | 98.960 | 99.291 |
| research/analysis/energy-model-change.json#currentComparison.rows[7].currentMWh | 142.153 | 142.484 |
| research/analysis/energy-model-change.json#currentComparison.rows[9].changeMWh | 581.615 | 590.285 |
| research/analysis/energy-model-change.json#currentComparison.rows[9].currentMWh | 757.615 | 766.285 |
| research/analysis/energy-model-change.json#currentComparison.rows[11].changeMWh | 1070.508 | 1083.414 |
| research/analysis/energy-model-change.json#currentComparison.rows[11].currentMWh | 1373.402 | 1386.308 |
| research/analysis/energy-motion.json#rows[5].phases[3].peaks[0].marginT | 4.429 | 0.000 |
| research/analysis/energy-motion.json#rows[5].phases[3].peaks[0].worstMarginGapT | 83.105 | 85.233 |
| research/analysis/energy-motion.json#rows[5].phases[3].peaks[1].marginT | 4.429 | 0.000 |
| research/analysis/energy-motion.json#rows[5].phases[3].peaks[1].worstMarginGapT | 105.110 | 107.404 |
| research/analysis/energy-motion.json#rows[5].phases[5].peaks[0].marginT | 0.002 | 0.000 |
| research/analysis/energy-motion.json#rows[5].phases[5].peaks[0].worstMarginGapT | 26.682 | 26.684 |
| research/analysis/energy-motion.json#rows[5].phases[5].peaks[1].marginT | 0.002 | 0.000 |
| research/analysis/energy-motion.json#rows[5].phases[5].peaks[1].worstMarginGapT | 33.525 | 33.528 |
| research/analysis/energy-motion.json#rows[7].phases[3].peaks[0].marginT | 4.429 | 0.000 |
| research/analysis/energy-motion.json#rows[7].phases[3].peaks[0].worstMarginGapT | 83.105 | 85.233 |
| research/analysis/energy-motion.json#rows[7].phases[3].peaks[1].marginT | 4.429 | 0.000 |
| research/analysis/energy-motion.json#rows[7].phases[3].peaks[1].worstMarginGapT | 105.110 | 107.404 |
| research/analysis/energy-motion.json#rows[9].phases[3].peaks[0].marginT | 6.365 | 0.000 |
| research/analysis/energy-motion.json#rows[9].phases[3].peaks[0].worstMarginGapT | 207.763 | 213.082 |
| research/analysis/energy-motion.json#rows[9].phases[3].peaks[1].marginT | 6.365 | 0.000 |
| research/analysis/energy-motion.json#rows[9].phases[3].peaks[1].worstMarginGapT | 262.774 | 268.511 |
| research/analysis/energy-motion.json#rows[11].phases[3].peaks[0].marginT | 6.365 | 0.000 |
| research/analysis/energy-motion.json#rows[11].phases[3].peaks[0].worstMarginGapT | 207.763 | 213.082 |
| research/analysis/energy-motion.json#rows[11].phases[3].peaks[1].marginT | 6.365 | 0.000 |
| research/analysis/energy-motion.json#rows[11].phases[3].peaks[1].worstMarginGapT | 262.774 | 268.511 |
| research/analysis/energy-profiles.json#rows[0].best.sensitivity[3].worst.progress | 0.669198 | 0.669197 |
| research/analysis/energy-profiles.json#rows[1].best.sensitivity[3].worst.progress | 0.669198 | 0.669197 |
| research/analysis/energy-profiles.json#rows[1].fullDeliveryBest.sensitivity[3].cycleMWh | 45.547 | 45.572 |
| research/analysis/energy-profiles.json#rows[2].best.sensitivity[2].worst.progress | 0.672517 | 0.672518 |
| research/analysis/energy-profiles.json#rows[2].fullDeliveryBest.sensitivity[2].worst.progress | 0.672950 | 0.672951 |
| research/analysis/energy-profiles.json#rows[2].fullDeliveryBest.sensitivity[3].worst.progress | 0.669465 | 0.669464 |
| research/analysis/energy-profiles.json#rows[3].best.sensitivity[2].worst.progress | 0.672950 | 0.672951 |
| research/analysis/energy-profiles.json#rows[3].best.sensitivity[3].worst.progress | 0.669465 | 0.669464 |
| research/analysis/energy-profiles.json#rows[3].fullDeliveryBest.sensitivity[2].worst.progress | 0.672950 | 0.672951 |
| research/analysis/energy-profiles.json#rows[3].fullDeliveryBest.sensitivity[3].worst.progress | 0.669465 | 0.669464 |
| research/analysis/energy-profiles.json#rows[5].asDrawn.cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-profiles.json#rows[5].asDrawn.hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-profiles.json#rows[5].asDrawn.kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-profiles.json#rows[7].asDrawn.cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-profiles.json#rows[7].asDrawn.hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-profiles.json#rows[7].asDrawn.kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-profiles.json#rows[9].asDrawn.cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-profiles.json#rows[9].asDrawn.hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-profiles.json#rows[9].asDrawn.kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-profiles.json#rows[11].asDrawn.cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-profiles.json#rows[11].asDrawn.hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-profiles.json#rows[11].asDrawn.kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-requirements.json#rows[1].dragSensitivity[0].worst.progress | 0.702318 | 0.702320 |
| research/analysis/energy-requirements.json#rows[5].baseline.cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-requirements.json#rows[5].baseline.hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-requirements.json#rows[5].baseline.kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[0].cycleMWh | 61.517 | 61.758 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[0].hoursOnBattery | 1.164 | 1.159 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[0].kwhPerTonne | 61.517 | 61.758 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[1].cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[1].hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[1].kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[2].cycleMWh | 61.009 | 61.171 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[2].hoursOnBattery | 1.174 | 1.170 |
| research/analysis/energy-requirements.json#rows[5].clSensitivity[2].kwhPerTonne | 61.009 | 61.171 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[0].cycleMWh | 60.962 | 61.162 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[0].hoursOnBattery | 1.174 | 1.171 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[0].kwhPerTonne | 60.962 | 61.162 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[1].cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[1].hoursOnBattery | 1.171 | 1.167 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[1].kwhPerTonne | 61.155 | 61.355 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[2].cycleMWh | 61.466 | 61.666 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[2].hoursOnBattery | 1.165 | 1.161 |
| research/analysis/energy-requirements.json#rows[5].dragSensitivity[2].kwhPerTonne | 61.466 | 61.666 |
| research/analysis/energy-requirements.json#rows[7].baseline.cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-requirements.json#rows[7].baseline.hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-requirements.json#rows[7].baseline.kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[0].cycleMWh | 142.528 | 143.065 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[0].hoursOnBattery | 1.325 | 1.320 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[0].kwhPerTonne | 142.528 | 143.065 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[1].cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[1].hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[1].kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[2].cycleMWh | 142.027 | 142.241 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[2].hoursOnBattery | 1.330 | 1.328 |
| research/analysis/energy-requirements.json#rows[7].clSensitivity[2].kwhPerTonne | 142.027 | 142.241 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[0].cycleMWh | 142.073 | 142.404 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[0].hoursOnBattery | 1.329 | 1.326 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[0].kwhPerTonne | 142.073 | 142.404 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[1].cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[1].hoursOnBattery | 1.328 | 1.325 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[1].kwhPerTonne | 142.153 | 142.484 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[2].cycleMWh | 142.232 | 142.562 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[2].hoursOnBattery | 1.328 | 1.324 |
| research/analysis/energy-requirements.json#rows[7].dragSensitivity[2].kwhPerTonne | 142.232 | 142.562 |
| research/analysis/energy-requirements.json#rows[9].baseline.cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-requirements.json#rows[9].baseline.hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-requirements.json#rows[9].baseline.kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[0].cycleMWh | 753.350 | 753.408 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[0].kwhPerTonne | 75.335 | 75.341 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[1].cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[1].hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[1].kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[2].cycleMWh | 754.912 | 765.203 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[2].hoursOnBattery | 2.021 | 1.993 |
| research/analysis/energy-requirements.json#rows[9].clSensitivity[2].kwhPerTonne | 75.491 | 76.520 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[0].cycleMWh | 756.441 | 765.272 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[0].hoursOnBattery | 2.016 | 1.993 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[0].kwhPerTonne | 75.644 | 76.527 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[1].cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[1].hoursOnBattery | 2.013 | 1.990 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[1].kwhPerTonne | 75.761 | 76.629 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[2].cycleMWh | 758.981 | 767.490 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[2].hoursOnBattery | 2.010 | 1.987 |
| research/analysis/energy-requirements.json#rows[9].dragSensitivity[2].kwhPerTonne | 75.898 | 76.749 |
| research/analysis/energy-requirements.json#rows[11].baseline.cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-requirements.json#rows[11].baseline.hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-requirements.json#rows[11].baseline.kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[0].cycleMWh | 1355.989 | 1356.363 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[0].hoursOnBattery | 2.335 | 2.334 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[0].kwhPerTonne | 135.599 | 135.636 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[1].cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[1].hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[1].kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[2].cycleMWh | 1369.068 | 1385.070 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[2].hoursOnBattery | 2.312 | 2.285 |
| research/analysis/energy-requirements.json#rows[11].clSensitivity[2].kwhPerTonne | 136.907 | 138.507 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[0].cycleMWh | 1372.867 | 1385.795 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[0].hoursOnBattery | 2.306 | 2.284 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[0].kwhPerTonne | 137.287 | 138.579 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[1].cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[1].hoursOnBattery | 2.305 | 2.283 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[1].kwhPerTonne | 137.340 | 138.631 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[2].cycleMWh | 1373.947 | 1386.831 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[2].hoursOnBattery | 2.304 | 2.282 |
| research/analysis/energy-requirements.json#rows[11].dragSensitivity[2].kwhPerTonne | 137.395 | 138.683 |
| research/analysis/energy-rotor-range.json#rows[6].cycleMWh | 16.423 | 16.424 |
| research/analysis/energy-rotor-range.json#rows[10].cycleMWh | 63.025 | 63.325 |
| research/analysis/energy-rotor-range.json#rows[11].cycleMWh | 61.155 | 61.355 |
| research/analysis/energy-rotor-range.json#rows[14].cycleMWh | 145.115 | 145.623 |
| research/analysis/energy-rotor-range.json#rows[15].cycleMWh | 142.153 | 142.484 |
| research/analysis/energy-rotor-range.json#rows[18].cycleMWh | 783.022 | 801.445 |
| research/analysis/energy-rotor-range.json#rows[19].cycleMWh | 757.615 | 766.285 |
| research/analysis/energy-rotor-range.json#rows[22].cycleMWh | 1394.675 | 1444.127 |
| research/analysis/energy-rotor-range.json#rows[23].cycleMWh | 1373.402 | 1386.308 |
| research/analysis/energy-unheld.json#rows[0].phases[0].progress | 0.686342 | 0.686344 |
| research/analysis/energy-unheld.json#rows[1].phases[0].progress | 0.686342 | 0.686344 |
| research/analysis/energy-unheld.json#rows[5].phases[4].unheldT | 516.352 | 503.207 |
| research/analysis/energy-unheld.json#rows[7].phases[4].unheldT | 493.892 | 480.748 |
| research/analysis/energy-unheld.json#rows[9].phases[4].unheldT | 3968.748 | 3956.719 |
| research/analysis/energy-unheld.json#rows[11].phases[4].unheldT | 3905.400 | 3893.371 |
| research/figures.json#classes.P100.bases.favourable.worst.progress | 0.222656 | 0.222832 |
| research/figures.json#classes.P100.bases.record.worst.progress | 0.810547 | 0.810707 |
| research/figures.json#classes.P100.cycle.worst.progress | 0.810547 | 0.810707 |
| research/figures.json#classes.P1000.bases.favourable.cycleMWh | 61.155 | 61.355 |
| research/figures.json#classes.P1000.bases.favourable.hoursOnBattery | 1.171 | 1.167 |
| research/figures.json#classes.P1000.bases.favourable.kwhPerTonne | 61.155 | 61.355 |
| research/figures.json#classes.P10000.bases.favourable.cycleMWh | 757.615 | 766.285 |
| research/figures.json#classes.P10000.bases.favourable.hoursOnBattery | 2.013 | 1.990 |
| research/figures.json#classes.P10000.bases.favourable.kwhPerTonne | 75.761 | 76.629 |
| tests/energy/unheld.mjs#namedEndurance.worstUnheldT | 2.041455599 | 1.927956588 |

### Part C

Bound return-join acceleration throughout the finite profile search.

| Generated record and field | Earlier | Current |
|---|---|---|
| research/analysis/energy-feasible.json#rows[0].asDrawn.cycleMWh | 4.424 | 4.432 |
| research/analysis/energy-feasible.json#rows[0].asDrawn.hoursOnBattery | 1.122 | 1.120 |
| research/analysis/energy-feasible.json#rows[0].asDrawn.kwhPerTonne | 44.243 | 44.323 |
| research/analysis/energy-feasible.json#rows[0].asDrawn.worst.progress | 0.204787 | 0.229691 |
| research/analysis/energy-feasible.json#rows[0].asDrawn.worst.unheldT | 73.021 | 53.543 |
| research/analysis/energy-feasible.json#rows[0].checked | 2897.000 | 2934.000 |
| research/analysis/energy-feasible.json#rows[0].planCalls | 9795.000 | 9919.000 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.cycleMWh | 3.868 | 3.865 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.hoursOnBattery | 1.286 | 1.287 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.kwhPerTonne | 38.685 | 38.649 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.worst.progress | 0.204662 | 0.684064 |
| research/analysis/energy-feasible.json#rows[1].asDrawn.worst.unheldT | 8.686 | 7.487 |
| research/analysis/energy-feasible.json#rows[1].best.cycleMWh | 1.410 | 1.395 |
| research/analysis/energy-feasible.json#rows[1].best.hoursOnBattery | 2.491 | 2.519 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[0].absT | 73.325 | 38.460 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[0].accelerationMps2 | 2.297 | 1.205 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[0].forceT | 73.325 | 38.460 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[0].marginT | 116.093 | 115.829 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[0].onboardT | 150.051 | 150.066 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[0].progress | 0.329500 | 0.427000 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[0].worstMarginGapT | 8.988 | 0.000 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[1].absT | 89.694 | 47.045 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[1].accelerationMps2 | 2.297 | 1.205 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[1].forceT | 89.694 | 47.045 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[1].marginT | 116.093 | 115.829 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[1].onboardT | 150.051 | 150.066 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[1].progress | 0.329500 | 0.427000 |
| research/analysis/energy-feasible.json#rows[1].best.inertia.phases[5].peaks[1].worstMarginGapT | 21.283 | 0.000 |
| research/analysis/energy-feasible.json#rows[1].best.kwhPerTonne | 28.196 | 27.897 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[0].cycleMWh | 1.372 | 1.376 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[1].cycleMWh | 1.410 | 1.395 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].cycleMWh | 1.438 | 1.421 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].worst.progress | 0.203820 | 0.203792 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[2].worst.unheldT | 46.901 | -25.048 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[4].cycleMWh | 1.410 | 1.395 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[5].cycleMWh | 1.431 | 1.416 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[6].cycleMWh | 1.410 | 1.395 |
| research/analysis/energy-feasible.json#rows[1].best.sensitivity[7].cycleMWh | 1.402 | 1.387 |
| research/analysis/energy-feasible.json#rows[1].checked | 2986.000 | 3047.000 |
| research/analysis/energy-feasible.json#rows[1].planCalls | 9902.000 | 9929.000 |
| research/analysis/energy-feasible.json#rows[2].planCalls | 10381.000 | 10370.000 |
| research/analysis/energy-feasible.json#rows[3].planCalls | 10377.000 | 10370.000 |
| research/analysis/energy-feasible.json#rows[4].planCalls | 9164.000 | 9161.000 |
| research/analysis/energy-feasible.json#rows[5].planCalls | 8854.000 | 8855.000 |
| research/analysis/energy-feasible.json#rows[6].planCalls | 11225.000 | 11222.000 |
| research/analysis/energy-feasible.json#rows[7].planCalls | 11225.000 | 11222.000 |
| research/analysis/energy-feasible.json#rows[12].planCalls | 11956.000 | 11949.000 |
| research/analysis/energy-feasible.json#rows[14].planCalls | 13168.000 | 13159.000 |
| research/analysis/energy-feasible.json#rows[16].planCalls | 13911.000 | 13895.000 |
| research/analysis/energy-profiles.json#rows[0].planCalls | 10872.000 | 10876.000 |
| research/analysis/energy-profiles.json#rows[1].planCalls | 10781.000 | 10775.000 |
| research/analysis/energy-profiles.json#rows[2].planCalls | 8828.000 | 8834.000 |
| research/analysis/energy-profiles.json#rows[3].planCalls | 8697.000 | 8701.000 |
| research/analysis/energy-profiles.json#rows[6].planCalls | 13033.000 | 13032.000 |
| research/analysis/energy-profiles.json#rows[7].planCalls | 13017.000 | 13016.000 |
| research/analysis/energy-profiles.json#rows[8].planCalls | 13626.000 | 13611.000 |
| research/analysis/energy-profiles.json#rows[10].planCalls | 13906.000 | 13890.000 |
| tests/golden/seed7-snapshot.json#plans[5].eCycleMWh | 7.483 | 7.489 |
| tests/golden/seed7-snapshot.json#plans[5].kwhPerTonne | 74.834 | 74.894 |
| tests/golden/seed7-snapshot.json#plans[20].eCycleMWh | 8.761 | 8.771 |
| tests/golden/seed7-snapshot.json#plans[20].kwhPerTonne | 87.611 | 87.711 |
| tests/golden/seed7-snapshot.json#plans[33].eCycleMWh | 7.095 | 7.104 |
| tests/golden/seed7-snapshot.json#plans[33].kwhPerTonne | 70.950 | 71.041 |
| tests/golden/seed7-snapshot.json#plans[35].eCycleMWh | 6.642 | 6.644 |
| tests/golden/seed7-snapshot.json#plans[35].kwhPerTonne | 66.419 | 66.439 |

### Part SOLAR

Projected solar collection is 85% of each current capsule footprint, an unvalidated coverage assumption; physical sheet area remains a separate material-budget assumption. The table gives class and publication summaries; the [complete per-field movement record](../research/analysis/solar-input-changes.json) includes route records and golden snapshots. Regeneration on an integrated tree can include other model corrections; this publication comparison does not isolate their individual effects.

| Generated record and field | Earlier | Current |
|---|---|---|
| research/analysis/energy-documents.json#classes[0].groundSolarDays | 24.641 | 58.189 |
| research/analysis/energy-documents.json#classes[0].solarMW | 0.270 | 0.207 |
| research/analysis/energy-documents.json#classes[0].tankSolarDays | 26.420 | 62.390 |
| research/analysis/energy-documents.json#classes[1].groundSolarDays | 58.924 | 162.233 |
| research/analysis/energy-documents.json#classes[1].solarMW | 1.260 | 0.967 |
| research/analysis/energy-documents.json#classes[1].tankSolarDays | 63.179 | 173.948 |
| research/analysis/energy-documents.json#classes[2].groundSolarDays | 112.939 | 183.696 |
| research/analysis/energy-documents.json#classes[2].solarMW | 5.400 | 4.476 |
| research/analysis/energy-documents.json#classes[2].tankSolarDays | 121.094 | 196.960 |
| research/analysis/energy-documents.json#readmeExamples[0].cycleMWh | 694.378 | 694.174 |
| research/analysis/energy-documents.json#readmeExamples[0].hoursOnBattery | 2.198 | 2.196 |
| research/analysis/energy-documents.json#readmeExamples[0].kwhPerTonne | 69.438 | 69.417 |
| research/analysis/energy-documents.json#readmeExamples[0].peakRotorMW | 1405.710 | 1404.786 |
| research/analysis/energy-documents.json#readmeExamples[0].worst.unheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#readmeExamples[1].cycleMWh | 766.285 | 765.904 |
| research/analysis/energy-documents.json#readmeExamples[1].kwhPerTonne | 76.629 | 76.590 |
| research/analysis/energy-documents.json#readmeExamples[1].peakRotorMW | 1405.710 | 1404.786 |
| research/analysis/energy-documents.json#readmeExamples[1].worst.unheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#readmeExamples[2].cycleMWh | 976.506 | 976.302 |
| research/analysis/energy-documents.json#readmeExamples[2].hoursOnBattery | 2.685 | 2.682 |
| research/analysis/energy-documents.json#readmeExamples[2].kwhPerTonne | 97.651 | 97.630 |
| research/analysis/energy-documents.json#readmeExamples[2].peakRotorMW | 1419.393 | 1418.469 |
| research/analysis/energy-documents.json#readmeExamples[2].worst.unheldT | 6998.258 | 7001.076 |
| research/analysis/energy-documents.json#readmeExamples[3].cycleMWh | 1178.889 | 1178.435 |
| research/analysis/energy-documents.json#readmeExamples[3].hoursOnBattery | 2.221 | 2.220 |
| research/analysis/energy-documents.json#readmeExamples[3].kwhPerTonne | 117.889 | 117.844 |
| research/analysis/energy-documents.json#readmeExamples[3].peakRotorMW | 1419.393 | 1418.469 |
| research/analysis/energy-documents.json#readmeExamples[3].worst.unheldT | 6998.258 | 7001.076 |
| research/analysis/energy-documents.json#records[0].asDrawn.cycleMWh | 8.192 | 8.189 |
| research/analysis/energy-documents.json#records[0].asDrawn.hoursOnBattery | 1.418 | 1.412 |
| research/analysis/energy-documents.json#records[0].asDrawn.kwhPerTonne | 81.923 | 81.892 |
| research/analysis/energy-documents.json#records[0].asDrawn.peakRotorMW | 31.475 | 31.411 |
| research/analysis/energy-documents.json#records[0].asDrawn.worst.progress | 0.810707 | 0.810716 |
| research/analysis/energy-documents.json#records[0].asDrawn.worst.unheldT | 34.556 | 34.759 |
| research/analysis/energy-documents.json#records[0].channels.rotors | 6.896 | 6.893 |
| research/analysis/energy-documents.json#records[0].letdownMWh | 2.305 | 2.302 |
| research/analysis/energy-documents.json#records[0].phaseEnergy.RETURN_TRANSIT | 4.409 | 4.407 |
| research/analysis/energy-documents.json#records[0].solarMWh | 0.154 | 0.118 |
| research/analysis/energy-documents.json#records[1].asDrawn.cycleMWh | 6.402 | 6.401 |
| research/analysis/energy-documents.json#records[1].asDrawn.hoursOnBattery | 1.824 | 1.814 |
| research/analysis/energy-documents.json#records[1].asDrawn.kwhPerTonne | 64.017 | 64.011 |
| research/analysis/energy-documents.json#records[1].asDrawn.peakRotorMW | 31.475 | 31.411 |
| research/analysis/energy-documents.json#records[1].letdownMWh | 1.443 | 1.442 |
| research/analysis/energy-documents.json#records[1].phaseEnergy.SOURCE_APPROACH | 0.934 | 0.933 |
| research/analysis/energy-documents.json#records[1].solarMWh | 0.154 | 0.118 |
| research/analysis/energy-documents.json#records[2].asDrawn.hoursOnBattery | 1.742 | 1.732 |
| research/analysis/energy-documents.json#records[2].solarMWh | 0.472 | 0.361 |
| research/analysis/energy-documents.json#records[3].asDrawn.hoursOnBattery | 2.444 | 2.425 |
| research/analysis/energy-documents.json#records[3].solarMWh | 0.472 | 0.361 |
| research/analysis/energy-documents.json#records[4].asDrawn.cycleMWh | 62.314 | 62.251 |
| research/analysis/energy-documents.json#records[4].asDrawn.hoursOnBattery | 1.149 | 1.147 |
| research/analysis/energy-documents.json#records[4].asDrawn.kwhPerTonne | 62.314 | 62.251 |
| research/analysis/energy-documents.json#records[4].asDrawn.peakRotorMW | 153.796 | 153.504 |
| research/analysis/energy-documents.json#records[4].asDrawn.worst.unheldT | 818.465 | 819.257 |
| research/analysis/energy-documents.json#records[4].channels.rotors | 54.910 | 54.846 |
| research/analysis/energy-documents.json#records[4].letdownMWh | 11.572 | 11.548 |
| research/analysis/energy-documents.json#records[4].phaseEnergy.BUOYANCY_ESCAPE | 4.950 | 4.943 |
| research/analysis/energy-documents.json#records[4].phaseEnergy.RETURN_TRANSIT | 22.956 | 22.942 |
| research/analysis/energy-documents.json#records[4].phaseEnergy.SOURCE_APPROACH | 6.201 | 6.189 |
| research/analysis/energy-documents.json#records[4].phaseEnergy.WATER_FILL | 12.217 | 12.202 |
| research/analysis/energy-documents.json#records[4].phaseEnergy.WATER_RELEASE | 11.501 | 11.485 |
| research/analysis/energy-documents.json#records[4].solarMWh | 0.743 | 0.570 |
| research/analysis/energy-documents.json#records[5].asDrawn.cycleMWh | 61.355 | 61.259 |
| research/analysis/energy-documents.json#records[5].asDrawn.hoursOnBattery | 1.167 | 1.165 |
| research/analysis/energy-documents.json#records[5].asDrawn.kwhPerTonne | 61.355 | 61.259 |
| research/analysis/energy-documents.json#records[5].asDrawn.peakRotorMW | 153.796 | 153.504 |
| research/analysis/energy-documents.json#records[5].asDrawn.worst.unheldT | 818.465 | 819.257 |
| research/analysis/energy-documents.json#records[5].channels.prop | 13.795 | 13.774 |
| research/analysis/energy-documents.json#records[5].channels.rotors | 43.189 | 43.113 |
| research/analysis/energy-documents.json#records[5].letdownMWh | 9.319 | 9.299 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.BUOYANCY_ESCAPE | 5.042 | 5.032 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.RETURN_TRANSIT | 24.266 | 24.219 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.SOURCE_APPROACH | 6.201 | 6.189 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.WATER_FILL | 12.217 | 12.202 |
| research/analysis/energy-documents.json#records[5].phaseEnergy.WATER_RELEASE | 10.726 | 10.712 |
| research/analysis/energy-documents.json#records[5].solarMWh | 0.743 | 0.570 |
| research/analysis/energy-documents.json#records[6].asDrawn.cycleMWh | 141.533 | 141.451 |
| research/analysis/energy-documents.json#records[6].asDrawn.hoursOnBattery | 1.334 | 1.331 |
| research/analysis/energy-documents.json#records[6].asDrawn.kwhPerTonne | 141.533 | 141.451 |
| research/analysis/energy-documents.json#records[6].asDrawn.peakRotorMW | 165.925 | 165.632 |
| research/analysis/energy-documents.json#records[6].asDrawn.worst.unheldT | 768.406 | 769.180 |
| research/analysis/energy-documents.json#records[6].channels.rotors | 116.474 | 116.391 |
| research/analysis/energy-documents.json#records[6].letdownMWh | 28.433 | 28.387 |
| research/analysis/energy-documents.json#records[6].phaseEnergy.BUOYANCY_ESCAPE | 4.952 | 4.945 |
| research/analysis/energy-documents.json#records[6].phaseEnergy.RETURN_TRANSIT | 91.689 | 91.654 |
| research/analysis/energy-documents.json#records[6].phaseEnergy.SOURCE_APPROACH | 6.625 | 6.614 |
| research/analysis/energy-documents.json#records[6].phaseEnergy.WATER_FILL | 12.870 | 12.857 |
| research/analysis/energy-documents.json#records[6].phaseEnergy.WATER_RELEASE | 11.501 | 11.485 |
| research/analysis/energy-documents.json#records[6].solarMWh | 1.955 | 1.501 |
| research/analysis/energy-documents.json#records[7].asDrawn.cycleMWh | 142.484 | 142.271 |
| research/analysis/energy-documents.json#records[7].asDrawn.hoursOnBattery | 1.325 | 1.323 |
| research/analysis/energy-documents.json#records[7].asDrawn.kwhPerTonne | 142.484 | 142.271 |
| research/analysis/energy-documents.json#records[7].asDrawn.peakRotorMW | 165.925 | 165.632 |
| research/analysis/energy-documents.json#records[7].asDrawn.worst.unheldT | 768.406 | 769.180 |
| research/analysis/energy-documents.json#records[7].channels.prop | 48.970 | 48.902 |
| research/analysis/energy-documents.json#records[7].channels.rotors | 80.226 | 80.081 |
| research/analysis/energy-documents.json#records[7].letdownMWh | 19.757 | 19.711 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.BUOYANCY_ESCAPE | 5.042 | 5.032 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.RETURN_TRANSIT | 97.026 | 96.860 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.SOURCE_APPROACH | 6.625 | 6.614 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.WATER_FILL | 12.870 | 12.857 |
| research/analysis/energy-documents.json#records[7].phaseEnergy.WATER_RELEASE | 10.726 | 10.712 |
| research/analysis/energy-documents.json#records[7].solarMWh | 1.955 | 1.501 |
| research/analysis/energy-documents.json#records[8].asDrawn.cycleMWh | 694.378 | 694.174 |
| research/analysis/energy-documents.json#records[8].asDrawn.hoursOnBattery | 2.198 | 2.196 |
| research/analysis/energy-documents.json#records[8].asDrawn.kwhPerTonne | 69.438 | 69.417 |
| research/analysis/energy-documents.json#records[8].asDrawn.peakRotorMW | 1405.710 | 1404.786 |
| research/analysis/energy-documents.json#records[8].asDrawn.worst.unheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#records[8].channels.rotors | 652.671 | 652.467 |
| research/analysis/energy-documents.json#records[8].letdownMWh | 117.219 | 117.168 |
| research/analysis/energy-documents.json#records[8].phaseEnergy.BUOYANCY_ESCAPE | 41.117 | 41.103 |
| research/analysis/energy-documents.json#records[8].phaseEnergy.RETURN_TRANSIT | 114.038 | 114.037 |
| research/analysis/energy-documents.json#records[8].phaseEnergy.SOURCE_APPROACH | 87.524 | 87.475 |
| research/analysis/energy-documents.json#records[8].phaseEnergy.WATER_FILL | 214.046 | 213.959 |
| research/analysis/energy-documents.json#records[8].phaseEnergy.WATER_RELEASE | 205.208 | 205.156 |
| research/analysis/energy-documents.json#records[8].solarMWh | 4.096 | 3.395 |
| research/analysis/energy-documents.json#records[9].asDrawn.cycleMWh | 766.285 | 765.904 |
| research/analysis/energy-documents.json#records[9].asDrawn.kwhPerTonne | 76.629 | 76.590 |
| research/analysis/energy-documents.json#records[9].asDrawn.peakRotorMW | 1405.710 | 1404.786 |
| research/analysis/energy-documents.json#records[9].asDrawn.worst.unheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#records[9].channels.prop | 114.142 | 114.014 |
| research/analysis/energy-documents.json#records[9].channels.rotors | 630.390 | 630.138 |
| research/analysis/energy-documents.json#records[9].letdownMWh | 116.531 | 116.470 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.BUOYANCY_ESCAPE | 46.787 | 46.761 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.RETURN_TRANSIT | 190.778 | 190.653 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.SOURCE_APPROACH | 87.661 | 87.606 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.WATER_FILL | 214.046 | 213.959 |
| research/analysis/energy-documents.json#records[9].phaseEnergy.WATER_RELEASE | 200.785 | 200.698 |
| research/analysis/energy-documents.json#records[9].solarMWh | 4.096 | 3.395 |
| research/analysis/energy-documents.json#records[10].asDrawn.cycleMWh | 1113.855 | 1113.650 |
| research/analysis/energy-documents.json#records[10].asDrawn.hoursOnBattery | 2.846 | 2.843 |
| research/analysis/energy-documents.json#records[10].asDrawn.kwhPerTonne | 111.385 | 111.365 |
| research/analysis/energy-documents.json#records[10].asDrawn.peakRotorMW | 1426.235 | 1425.310 |
| research/analysis/energy-documents.json#records[10].asDrawn.worst.unheldT | 6960.523 | 6963.338 |
| research/analysis/energy-documents.json#records[10].channels.rotors | 990.500 | 990.295 |
| research/analysis/energy-documents.json#records[10].letdownMWh | 218.149 | 218.096 |
| research/analysis/energy-documents.json#records[10].phaseEnergy.BUOYANCY_ESCAPE | 41.182 | 41.168 |
| research/analysis/energy-documents.json#records[10].phaseEnergy.RETURN_TRANSIT | 465.681 | 465.676 |
| research/analysis/energy-documents.json#records[10].phaseEnergy.SOURCE_APPROACH | 88.429 | 88.380 |
| research/analysis/energy-documents.json#records[10].phaseEnergy.WATER_FILL | 215.650 | 215.565 |
| research/analysis/energy-documents.json#records[10].phaseEnergy.WATER_RELEASE | 205.208 | 205.156 |
| research/analysis/energy-documents.json#records[10].solarMWh | 8.494 | 7.040 |
| research/analysis/energy-documents.json#records[11].asDrawn.cycleMWh | 1386.308 | 1385.793 |
| research/analysis/energy-documents.json#records[11].asDrawn.hoursOnBattery | 2.283 | 2.282 |
| research/analysis/energy-documents.json#records[11].asDrawn.kwhPerTonne | 138.631 | 138.579 |
| research/analysis/energy-documents.json#records[11].asDrawn.peakRotorMW | 1426.235 | 1425.310 |
| research/analysis/energy-documents.json#records[11].asDrawn.worst.unheldT | 6960.523 | 6963.338 |
| research/analysis/energy-documents.json#records[11].channels.prop | 382.918 | 382.673 |
| research/analysis/energy-documents.json#records[11].channels.rotors | 956.133 | 955.863 |
| research/analysis/energy-documents.json#records[11].letdownMWh | 216.463 | 216.383 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.BUOYANCY_ESCAPE | 46.786 | 46.760 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.RETURN_TRANSIT | 749.322 | 749.061 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.SOURCE_APPROACH | 88.693 | 88.638 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.WATER_FILL | 215.650 | 215.565 |
| research/analysis/energy-documents.json#records[11].phaseEnergy.WATER_RELEASE | 200.785 | 200.698 |
| research/analysis/energy-documents.json#records[11].solarMWh | 8.494 | 7.040 |
| research/analysis/energy-documents.json#sensitivity[0].rows[0].worstUnheldT | 7962.261 | 7964.681 |
| research/analysis/energy-documents.json#sensitivity[0].rows[1].energyPct | -4.070 | -4.069 |
| research/analysis/energy-documents.json#sensitivity[0].rows[1].worstUnheldT | 6238.393 | 6241.601 |
| research/analysis/energy-documents.json#sensitivity[1].rows[0].energyPct | -0.573 | -0.574 |
| research/analysis/energy-documents.json#sensitivity[1].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[1].rows[1].energyPct | 0.573 | 0.574 |
| research/analysis/energy-documents.json#sensitivity[1].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[2].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[2].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[3].rows[0].worstUnheldT | 7076.519 | 7079.347 |
| research/analysis/energy-documents.json#sensitivity[3].rows[1].worstUnheldT | 7072.019 | 7074.846 |
| research/analysis/energy-documents.json#sensitivity[4].rows[0].worstUnheldT | 7072.661 | 7075.487 |
| research/analysis/energy-documents.json#sensitivity[4].rows[1].worstUnheldT | 7050.832 | 7053.663 |
| research/analysis/energy-documents.json#sensitivity[5].rows[0].energyPct | -33.632 | -33.629 |
| research/analysis/energy-documents.json#sensitivity[5].rows[0].worstUnheldT | 2825.763 | 2828.403 |
| research/analysis/energy-documents.json#sensitivity[5].rows[1].energyPct | 27.982 | 27.970 |
| research/analysis/energy-documents.json#sensitivity[5].rows[1].worstUnheldT | 11375.223 | 11378.211 |
| research/analysis/energy-documents.json#sensitivity[6].rows[0].worstUnheldT | 7078.004 | 7080.832 |
| research/analysis/energy-documents.json#sensitivity[6].rows[1].worstUnheldT | 7069.636 | 7072.462 |
| research/analysis/energy-documents.json#sensitivity[7].rows[0].worstUnheldT | 7069.596 | 7072.423 |
| research/analysis/energy-documents.json#sensitivity[7].rows[1].worstUnheldT | 7076.634 | 7079.461 |
| research/analysis/energy-documents.json#sensitivity[8].rows[0].energyPct | -0.034 | -0.028 |
| research/analysis/energy-documents.json#sensitivity[8].rows[0].worstUnheldT | 7077.122 | 7079.384 |
| research/analysis/energy-documents.json#sensitivity[8].rows[1].energyPct | 0.034 | 0.028 |
| research/analysis/energy-documents.json#sensitivity[8].rows[1].worstUnheldT | 7070.517 | 7073.909 |
| research/analysis/energy-documents.json#sensitivity[9].rows[0].energyPct | 8.241 | 8.243 |
| research/analysis/energy-documents.json#sensitivity[9].rows[0].worstUnheldT | 7064.367 | 7067.193 |
| research/analysis/energy-documents.json#sensitivity[9].rows[1].worstUnheldT | 7080.121 | 7082.949 |
| research/analysis/energy-documents.json#sensitivity[10].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[10].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[11].rows[0].energyPct | 0.632 | 0.626 |
| research/analysis/energy-documents.json#sensitivity[11].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[11].rows[1].energyPct | -0.945 | -0.943 |
| research/analysis/energy-documents.json#sensitivity[11].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[12].rows[0].energyPct | 15.662 | 15.654 |
| research/analysis/energy-documents.json#sensitivity[12].rows[0].worstUnheldT | 7071.659 | 7074.486 |
| research/analysis/energy-documents.json#sensitivity[12].rows[1].energyPct | -10.700 | -10.699 |
| research/analysis/energy-documents.json#sensitivity[12].rows[1].worstUnheldT | 7075.979 | 7078.806 |
| research/analysis/energy-documents.json#sensitivity[13].rows[0].energyPct | -36.384 | -36.380 |
| research/analysis/energy-documents.json#sensitivity[13].rows[1].energyPct | 29.956 | 29.942 |
| research/analysis/energy-documents.json#sensitivity[13].rows[1].worstUnheldT | 11627.482 | 11630.309 |
| research/analysis/energy-documents.json#sensitivity[14].rows[0].energyPct | 4.035 | 4.034 |
| research/analysis/energy-documents.json#sensitivity[14].rows[0].worstUnheldT | 7431.335 | 7433.975 |
| research/analysis/energy-documents.json#sensitivity[14].rows[1].energyPct | -3.384 | -3.382 |
| research/analysis/energy-documents.json#sensitivity[14].rows[1].worstUnheldT | 6769.651 | 6772.639 |
| research/analysis/energy-documents.json#sensitivity[15].rows[0].energyPct | -15.229 | -15.237 |
| research/analysis/energy-documents.json#sensitivity[15].rows[0].worstUnheldT | 7958.524 | 7961.549 |
| research/analysis/energy-documents.json#sensitivity[15].rows[1].energyPct | 14.003 | 14.011 |
| research/analysis/energy-documents.json#sensitivity[15].rows[1].worstUnheldT | 6241.696 | 6244.370 |
| research/analysis/energy-documents.json#sensitivity[16].rows[0].worstUnheldT | 7103.872 | 7106.767 |
| research/analysis/energy-documents.json#sensitivity[16].rows[1].energyPct | -0.594 | -0.593 |
| research/analysis/energy-documents.json#sensitivity[16].rows[1].worstUnheldT | 7001.267 | 7004.036 |
| research/analysis/energy-documents.json#sensitivity[17].rows[0].energyPct | -0.034 | -0.028 |
| research/analysis/energy-documents.json#sensitivity[17].rows[0].worstUnheldT | 7077.122 | 7079.384 |
| research/analysis/energy-documents.json#sensitivity[17].rows[1].energyPct | 0.034 | 0.028 |
| research/analysis/energy-documents.json#sensitivity[17].rows[1].worstUnheldT | 7070.517 | 7073.909 |
| research/analysis/energy-documents.json#sensitivity[18].rows[0].energyPct | 4.926 | 4.924 |
| research/analysis/energy-documents.json#sensitivity[18].rows[0].worstUnheldT | 7962.261 | 7964.681 |
| research/analysis/energy-documents.json#sensitivity[18].rows[1].energyPct | -7.118 | -7.104 |
| research/analysis/energy-documents.json#sensitivity[18].rows[1].worstUnheldT | 6238.393 | 6241.601 |
| research/analysis/energy-documents.json#sensitivity[19].rows[0].energyPct | -0.243 | -0.244 |
| research/analysis/energy-documents.json#sensitivity[19].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[19].rows[1].energyPct | 0.243 | 0.244 |
| research/analysis/energy-documents.json#sensitivity[19].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[20].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[20].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[21].rows[0].worstUnheldT | 7076.519 | 7079.347 |
| research/analysis/energy-documents.json#sensitivity[21].rows[1].worstUnheldT | 7072.019 | 7074.846 |
| research/analysis/energy-documents.json#sensitivity[22].rows[0].worstUnheldT | 7072.661 | 7075.487 |
| research/analysis/energy-documents.json#sensitivity[22].rows[1].worstUnheldT | 7050.832 | 7053.663 |
| research/analysis/energy-documents.json#sensitivity[23].rows[0].energyPct | -41.471 | -41.457 |
| research/analysis/energy-documents.json#sensitivity[23].rows[0].worstUnheldT | 2825.763 | 2828.403 |
| research/analysis/energy-documents.json#sensitivity[23].rows[1].energyPct | 25.441 | 25.432 |
| research/analysis/energy-documents.json#sensitivity[23].rows[1].worstUnheldT | 11375.223 | 11378.211 |
| research/analysis/energy-documents.json#sensitivity[24].rows[0].worstUnheldT | 7078.004 | 7080.832 |
| research/analysis/energy-documents.json#sensitivity[24].rows[1].worstUnheldT | 7069.636 | 7072.462 |
| research/analysis/energy-documents.json#sensitivity[25].rows[0].worstUnheldT | 7069.596 | 7072.423 |
| research/analysis/energy-documents.json#sensitivity[25].rows[1].worstUnheldT | 7076.634 | 7079.461 |
| research/analysis/energy-documents.json#sensitivity[26].rows[0].energyPct | -0.058 | -0.048 |
| research/analysis/energy-documents.json#sensitivity[26].rows[0].worstUnheldT | 7077.122 | 7079.384 |
| research/analysis/energy-documents.json#sensitivity[26].rows[1].energyPct | 0.058 | 0.048 |
| research/analysis/energy-documents.json#sensitivity[26].rows[1].worstUnheldT | 7070.517 | 7073.909 |
| research/analysis/energy-documents.json#sensitivity[27].rows[0].worstUnheldT | 7064.367 | 7067.193 |
| research/analysis/energy-documents.json#sensitivity[27].rows[1].energyPct | -4.149 | -4.146 |
| research/analysis/energy-documents.json#sensitivity[27].rows[1].worstUnheldT | 7080.121 | 7082.949 |
| research/analysis/energy-documents.json#sensitivity[28].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[28].rows[1].energyPct | -1.251 | -1.252 |
| research/analysis/energy-documents.json#sensitivity[28].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[29].rows[0].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[29].rows[1].energyPct | -0.723 | -0.720 |
| research/analysis/energy-documents.json#sensitivity[29].rows[1].worstUnheldT | 7073.819 | 7076.646 |
| research/analysis/energy-documents.json#sensitivity[30].rows[0].energyPct | 14.095 | 14.096 |
| research/analysis/energy-documents.json#sensitivity[30].rows[0].worstUnheldT | 7071.659 | 7074.486 |
| research/analysis/energy-documents.json#sensitivity[30].rows[1].energyPct | -9.490 | -9.488 |
| research/analysis/energy-documents.json#sensitivity[30].rows[1].worstUnheldT | 7075.979 | 7078.806 |
| research/analysis/energy-documents.json#sensitivity[31].rows[0].energyPct | -45.989 | -45.974 |
| research/analysis/energy-documents.json#sensitivity[31].rows[1].energyPct | 26.837 | 26.827 |
| research/analysis/energy-documents.json#sensitivity[31].rows[1].worstUnheldT | 11627.482 | 11630.309 |
| research/analysis/energy-documents.json#sensitivity[32].rows[0].energyPct | 2.471 | 2.470 |
| research/analysis/energy-documents.json#sensitivity[32].rows[0].worstUnheldT | 7431.335 | 7433.975 |
| research/analysis/energy-documents.json#sensitivity[32].rows[1].energyPct | -2.902 | -2.888 |
| research/analysis/energy-documents.json#sensitivity[32].rows[1].worstUnheldT | 6769.651 | 6772.639 |
| research/analysis/energy-documents.json#sensitivity[33].rows[0].energyPct | -15.868 | -15.881 |
| research/analysis/energy-documents.json#sensitivity[33].rows[0].worstUnheldT | 7958.524 | 7961.549 |
| research/analysis/energy-documents.json#sensitivity[33].rows[1].energyPct | 11.090 | 11.113 |
| research/analysis/energy-documents.json#sensitivity[33].rows[1].worstUnheldT | 6241.696 | 6244.370 |
| research/analysis/energy-documents.json#sensitivity[34].rows[0].energyPct | 0.848 | 0.847 |
| research/analysis/energy-documents.json#sensitivity[34].rows[0].worstUnheldT | 7103.872 | 7106.767 |
| research/analysis/energy-documents.json#sensitivity[34].rows[1].worstUnheldT | 7001.267 | 7004.036 |
| research/analysis/energy-documents.json#sensitivity[35].rows[0].energyPct | -0.058 | -0.048 |
| research/analysis/energy-documents.json#sensitivity[35].rows[0].worstUnheldT | 7077.122 | 7079.384 |
| research/analysis/energy-documents.json#sensitivity[35].rows[1].energyPct | 0.058 | 0.048 |
| research/analysis/energy-documents.json#sensitivity[35].rows[1].worstUnheldT | 7070.517 | 7073.909 |
| research/figures.json#classes.P100.bases.favourable.cycleMWh | 6.402 | 6.401 |
| research/figures.json#classes.P100.bases.favourable.hoursOnBattery | 1.824 | 1.814 |
| research/figures.json#classes.P100.bases.favourable.kwhPerTonne | 64.017 | 64.011 |
| research/figures.json#classes.P100.bases.favourable.peakRotorMW | 31.475 | 31.411 |
| research/figures.json#classes.P100.bases.record.cycleMWh | 8.192 | 8.189 |
| research/figures.json#classes.P100.bases.record.hoursOnBattery | 1.418 | 1.412 |
| research/figures.json#classes.P100.bases.record.kwhPerTonne | 81.923 | 81.892 |
| research/figures.json#classes.P100.bases.record.peakRotorMW | 31.475 | 31.411 |
| research/figures.json#classes.P100.bases.record.worst.progress | 0.810707 | 0.810716 |
| research/figures.json#classes.P100.bases.record.worst.unheldT | 34.556 | 34.759 |
| research/figures.json#classes.P100.cycle.eCycleMWh | 8.192 | 8.189 |
| research/figures.json#classes.P100.cycle.kwhPerTonne | 81.920 | 81.890 |
| research/figures.json#classes.P100.cycle.worst.progress | 0.810707 | 0.810716 |
| research/figures.json#classes.P100.cycle.worst.unheldT | 34.556 | 34.759 |
| research/figures.json#classes.P100.descent.letdownClipMin | 3.010 | 3.050 |
| research/figures.json#classes.P100.descent.rotorClipMWh | 0.252 | 0.255 |
| research/figures.json#classes.P100.descent.rotorClipMin | 3.010 | 3.050 |
| research/figures.json#classes.P100.energy.deficitPerCycleMWh | 8.040 | 8.070 |
| research/figures.json#classes.P100.energy.downMW | 31.500 | 31.400 |
| research/figures.json#classes.P100.energy.ledgerByChannelMWh.rotors | 6.896 | 6.893 |
| research/figures.json#classes.P100.energy.ledgerMWh.RETURN_TRANSIT | 4.409 | 4.407 |
| research/figures.json#classes.P100.energy.letdownMWh | 2.305 | 2.302 |
| research/figures.json#classes.P100.energy.solarMW | 0.270 | 0.210 |
| research/figures.json#classes.P100.energy.solarPerCycleMWh | 0.150 | 0.120 |
| research/figures.json#classes.P100.spec.solarM2 | 6000.000 | 4590.705 |
| research/figures.json#classes.P1000.bases.favourable.cycleMWh | 61.355 | 61.259 |
| research/figures.json#classes.P1000.bases.favourable.hoursOnBattery | 1.167 | 1.165 |
| research/figures.json#classes.P1000.bases.favourable.kwhPerTonne | 61.355 | 61.259 |
| research/figures.json#classes.P1000.bases.favourable.peakRotorMW | 153.796 | 153.504 |
| research/figures.json#classes.P1000.bases.favourable.worst.unheldT | 818.465 | 819.257 |
| research/figures.json#classes.P1000.bases.record.cycleMWh | 62.314 | 62.251 |
| research/figures.json#classes.P1000.bases.record.hoursOnBattery | 1.149 | 1.147 |
| research/figures.json#classes.P1000.bases.record.kwhPerTonne | 62.314 | 62.251 |
| research/figures.json#classes.P1000.bases.record.peakRotorMW | 153.796 | 153.504 |
| research/figures.json#classes.P1000.bases.record.worst.unheldT | 818.465 | 819.257 |
| research/figures.json#classes.P1000.cycle.eCycleMWh | 62.314 | 62.251 |
| research/figures.json#classes.P1000.cycle.kwhPerTonne | 62.310 | 62.250 |
| research/figures.json#classes.P1000.cycle.worst.unheldT | 818.465 | 819.257 |
| research/figures.json#classes.P1000.descent.rotorClipMWh | 7.349 | 7.413 |
| research/figures.json#classes.P1000.descent.rotorClipMin | 13.080 | 13.100 |
| research/figures.json#classes.P1000.energy.deficitPerCycleMWh | 61.570 | 61.680 |
| research/figures.json#classes.P1000.energy.downMW | 153.800 | 153.500 |
| research/figures.json#classes.P1000.energy.ledgerByChannelMWh.rotors | 54.910 | 54.846 |
| research/figures.json#classes.P1000.energy.ledgerMWh.BUOYANCY_ESCAPE | 4.950 | 4.943 |
| research/figures.json#classes.P1000.energy.ledgerMWh.RETURN_TRANSIT | 22.956 | 22.942 |
| research/figures.json#classes.P1000.energy.ledgerMWh.SOURCE_APPROACH | 6.201 | 6.189 |
| research/figures.json#classes.P1000.energy.ledgerMWh.WATER_FILL | 12.217 | 12.202 |
| research/figures.json#classes.P1000.energy.ledgerMWh.WATER_RELEASE | 11.501 | 11.485 |
| research/figures.json#classes.P1000.energy.letdownMWh | 11.572 | 11.548 |
| research/figures.json#classes.P1000.energy.solarMW | 1.260 | 0.970 |
| research/figures.json#classes.P1000.energy.solarPerCycleMWh | 0.740 | 0.570 |
| research/figures.json#classes.P1000.spec.solarM2 | 28000.000 | 21490.570 |
| research/figures.json#classes.P10000.bases.favourable.cycleMWh | 766.285 | 765.904 |
| research/figures.json#classes.P10000.bases.favourable.kwhPerTonne | 76.629 | 76.590 |
| research/figures.json#classes.P10000.bases.favourable.peakRotorMW | 1405.710 | 1404.786 |
| research/figures.json#classes.P10000.bases.favourable.worst.unheldT | 7073.819 | 7076.646 |
| research/figures.json#classes.P10000.bases.record.cycleMWh | 694.378 | 694.174 |
| research/figures.json#classes.P10000.bases.record.hoursOnBattery | 2.198 | 2.196 |
| research/figures.json#classes.P10000.bases.record.kwhPerTonne | 69.438 | 69.417 |
| research/figures.json#classes.P10000.bases.record.peakRotorMW | 1405.710 | 1404.786 |
| research/figures.json#classes.P10000.bases.record.worst.unheldT | 7073.819 | 7076.646 |
| research/figures.json#classes.P10000.cycle.eCycleMWh | 694.378 | 694.174 |
| research/figures.json#classes.P10000.cycle.kwhPerTonne | 69.440 | 69.420 |
| research/figures.json#classes.P10000.cycle.worst.unheldT | 7073.819 | 7076.646 |
| research/figures.json#classes.P10000.descent.letdownClipMin | 3.250 | 3.260 |
| research/figures.json#classes.P10000.descent.rotorClipMWh | 39.209 | 39.413 |
| research/figures.json#classes.P10000.descent.rotorClipMin | 13.100 | 13.140 |
| research/figures.json#classes.P10000.energy.deficitPerCycleMWh | 690.280 | 690.780 |
| research/figures.json#classes.P10000.energy.downMW | 1405.700 | 1404.800 |
| research/figures.json#classes.P10000.energy.ledgerByChannelMWh.rotors | 652.671 | 652.467 |
| research/figures.json#classes.P10000.energy.ledgerMWh.BUOYANCY_ESCAPE | 41.117 | 41.103 |
| research/figures.json#classes.P10000.energy.ledgerMWh.RETURN_TRANSIT | 114.038 | 114.037 |
| research/figures.json#classes.P10000.energy.ledgerMWh.SOURCE_APPROACH | 87.524 | 87.475 |
| research/figures.json#classes.P10000.energy.ledgerMWh.WATER_FILL | 214.046 | 213.959 |
| research/figures.json#classes.P10000.energy.ledgerMWh.WATER_RELEASE | 205.208 | 205.156 |
| research/figures.json#classes.P10000.energy.letdownMWh | 117.219 | 117.168 |
| research/figures.json#classes.P10000.energy.solarMW | 5.400 | 4.480 |
| research/figures.json#classes.P10000.energy.solarPerCycleMWh | 4.100 | 3.390 |
| research/figures.json#classes.P10000.spec.solarM2 | 120000.000 | 99456.676 |
| research/figures.json#sensitivity.dispM3.hi | 30.000 | 29.900 |
| research/analysis/water-availability.json#classes.P100.throughputTph.meanOverFires | 225.800 | 225.300 |
| research/analysis/water-availability.json#classes.P100.throughputTph.meanOverHectares | 244.700 | 243.100 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByFire.cycleMin | 21.329 | 21.325 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByFire.options.ballastT | 793.667 | 794.471 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByFire.releasedT | 206.333 | 205.529 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByFire.retainedT | 793.667 | 794.471 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByFire.suppliedMWh | 22.656 | 22.616 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByFire.tph | 580.429 | 578.288 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByHectare.cycleMin | 24.153 | 24.148 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByHectare.options.ballastT | 793.667 | 794.471 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByHectare.releasedT | 206.333 | 205.529 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByHectare.retainedT | 793.667 | 794.471 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByHectare.suppliedMWh | 24.940 | 24.897 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.medianByHectare.tph | 512.574 | 510.671 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.workedExample.cycleMin | 25.616 | 25.611 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.workedExample.options.ballastT | 784.409 | 785.210 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.workedExample.releasedT | 215.591 | 214.790 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.workedExample.retainedT | 784.409 | 785.210 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.workedExample.suppliedMWh | 26.489 | 26.444 |
| research/analysis/water-availability.json#classes.P1000.acceptedPlans.workedExample.tph | 504.981 | 503.192 |
| research/analysis/water-availability.json#classes.P1000.throughputTph.atMedianByFire | 580.400 | 578.300 |
| research/analysis/water-availability.json#classes.P1000.throughputTph.atMedianByHectare | 512.600 | 510.700 |
| research/analysis/water-availability.json#classes.P1000.throughputTph.atWorkedExample15km | 505.000 | 503.200 |
| research/analysis/water-availability.json#classes.P1000.throughputTph.meanOverFires | 531.100 | 528.900 |
| research/analysis/water-availability.json#classes.P1000.throughputTph.meanOverHectares | 495.900 | 493.900 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByFire.cycleMin | 30.429 | 30.426 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByFire.options.ballastT | 7373.800 | 7376.587 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByFire.releasedT | 2626.200 | 2623.413 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByFire.retainedT | 7373.800 | 7376.587 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByFire.suppliedMWh | 237.750 | 237.606 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByFire.tph | 5178.401 | 5173.432 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByHectare.cycleMin | 37.900 | 37.897 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByHectare.options.ballastT | 7373.800 | 7376.587 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByHectare.releasedT | 2626.200 | 2623.413 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByHectare.retainedT | 7373.800 | 7376.587 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByHectare.suppliedMWh | 278.075 | 277.918 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.medianByHectare.tph | 4157.551 | 4153.479 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.workedExample.cycleMin | 23.667 | 23.664 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.workedExample.options.ballastT | 7373.800 | 7376.587 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.workedExample.releasedT | 2626.200 | 2623.413 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.workedExample.retainedT | 7373.800 | 7376.587 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.workedExample.suppliedMWh | 200.116 | 199.983 |
| research/analysis/water-availability.json#classes.P10000.acceptedPlans.workedExample.tph | 6657.783 | 6651.588 |
| research/analysis/water-availability.json#classes.P10000.throughputTph.atMedianByFire | 5178.400 | 5173.400 |
| research/analysis/water-availability.json#classes.P10000.throughputTph.atMedianByHectare | 4157.600 | 4153.500 |
| research/analysis/water-availability.json#classes.P10000.throughputTph.atWorkedExample15km | 6657.800 | 6651.600 |
| research/analysis/water-availability.json#classes.P10000.throughputTph.meanOverFires | 5489.300 | 5484.200 |
| research/analysis/water-availability.json#classes.P10000.throughputTph.meanOverHectares | 4473.700 | 4469.500 |
| research/analysis/water-availability.json#geometry.P1000.drawTonnesPer12h | 6060.000 | 6038.000 |
| research/analysis/water-availability.json#geometry.P10000.drawTonnesPer12h | 79893.000 | 79819.000 |
| research/analysis/delivery.json#classes.P1000._lineKmAtCL4.20 m swath | 6.610 | 6.590 |
| research/analysis/delivery.json#classes.P1000._lineKmAtCL4.30 m swath | 4.410 | 4.390 |
| research/analysis/delivery.json#classes.P1000._lineKmAtCL4.50 m swath | 2.650 | 2.640 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.latLoadsPer24h | 1227.000 | 1223.000 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.lineKmPer24hAtCL2_30mSwath | 569.800 | 567.700 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.lineKmPer24hAtCL4_30mSwath | 284.900 | 283.900 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.lineKmPer24hAtCL6_30mSwath | 189.900 | 189.200 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.lineKmPer24hAtCL8_30mSwath | 142.500 | 141.900 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.plan.cycleMin | 21.329 | 21.325 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.plan.options.ballastT | 793.667 | 794.471 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.plan.releasedT | 206.333 | 205.529 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.plan.retainedT | 793.667 | 794.471 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.plan.suppliedMWh | 22.656 | 22.616 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.plan.tph | 580.429 | 578.288 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.suppliedMWhPer24h | 1529.619 | 1527.184 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.tonnesPer24h | 13930.000 | 13879.000 |
| research/analysis/delivery.json#classes.P1000.atRealMedianLeg.tph | 580.429 | 578.288 |
| research/analysis/delivery.json#classes.P1000.coverageLevelBySwath.20 m | 10.600 | 10.500 |
| research/analysis/delivery.json#classes.P1000.coverageLevelBySwath.30 m | 7.100 | 7.000 |
| research/analysis/delivery.json#classes.P1000.equivalentLoads.LAT (BAe-146) | 19.000 | 18.900 |
| research/analysis/delivery.json#classes.P1000.equivalentLoads.SEAT | 71.200 | 70.900 |
| research/analysis/delivery.json#classes.P1000.lineKmAtCL.CL2, 30 m swath | 8.820 | 8.790 |
| research/analysis/delivery.json#classes.P1000.lineKmAtCL.CL4, 30 m swath | 4.410 | 4.390 |
| research/analysis/delivery.json#classes.P1000.payloadT | 215.591 | 214.790 |
| research/analysis/delivery.json#classes.P1000.releaseRateM3s | 1.423 | 1.418 |
| research/analysis/delivery.json#classes.P1000.workedExamplePlan.cycleMin | 25.616 | 25.611 |
| research/analysis/delivery.json#classes.P1000.workedExamplePlan.options.ballastT | 784.409 | 785.210 |
| research/analysis/delivery.json#classes.P1000.workedExamplePlan.releasedT | 215.591 | 214.790 |
| research/analysis/delivery.json#classes.P1000.workedExamplePlan.retainedT | 784.409 | 785.210 |
| research/analysis/delivery.json#classes.P1000.workedExamplePlan.suppliedMWh | 26.489 | 26.444 |
| research/analysis/delivery.json#classes.P1000.workedExamplePlan.tph | 504.981 | 503.192 |
| research/analysis/delivery.json#classes.P10000._lineKmAtCL4.20 m swath | 80.570 | 80.480 |
| research/analysis/delivery.json#classes.P10000._lineKmAtCL4.30 m swath | 53.710 | 53.650 |
| research/analysis/delivery.json#classes.P10000._lineKmAtCL4.50 m swath | 32.230 | 32.190 |
| research/analysis/delivery.json#classes.P10000._lineKmAtCL4.80 m swath | 20.140 | 20.120 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.latLoadsPer24h | 10950.000 | 10939.000 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.lineKmPer24hAtCL2_30mSwath | 5083.600 | 5078.700 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.lineKmPer24hAtCL4_30mSwath | 2541.800 | 2539.400 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.lineKmPer24hAtCL6_30mSwath | 1694.500 | 1692.900 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.lineKmPer24hAtCL8_30mSwath | 1270.900 | 1269.700 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.plan.cycleMin | 30.429 | 30.426 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.plan.options.ballastT | 7373.800 | 7376.587 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.plan.releasedT | 2626.200 | 2623.413 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.plan.retainedT | 7373.800 | 7376.587 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.plan.suppliedMWh | 237.750 | 237.606 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.plan.tph | 5178.401 | 5173.432 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.suppliedMWhPer24h | 11251.221 | 11245.542 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.tonnesPer24h | 124282.000 | 124162.000 |
| research/analysis/delivery.json#classes.P10000.atRealMedianLeg.tph | 5178.401 | 5173.432 |
| research/analysis/delivery.json#classes.P10000.coverageLevelBySwath.20 m | 64.500 | 64.400 |
| research/analysis/delivery.json#classes.P10000.coverageLevelBySwath.30 m | 43.000 | 42.900 |
| research/analysis/delivery.json#classes.P10000.equivalentLoads.LAT (BAe-146) | 231.400 | 231.100 |
| research/analysis/delivery.json#classes.P10000.equivalentLoads.SEAT | 867.300 | 866.400 |
| research/analysis/delivery.json#classes.P10000.lineKmAtCL.CL2, 30 m swath | 107.420 | 107.310 |
| research/analysis/delivery.json#classes.P10000.lineKmAtCL.CL4, 30 m swath | 53.710 | 53.650 |
| research/analysis/delivery.json#classes.P10000.lineKmAtCL.CL8, 30 m swath | 26.860 | 26.830 |
| research/analysis/delivery.json#classes.P10000.payloadT | 2626.200 | 2623.413 |
| research/analysis/delivery.json#classes.P10000.releaseRateM3s | 12.269 | 12.256 |
| research/analysis/delivery.json#classes.P10000.workedExamplePlan.cycleMin | 23.667 | 23.664 |
| research/analysis/delivery.json#classes.P10000.workedExamplePlan.options.ballastT | 7373.800 | 7376.587 |
| research/analysis/delivery.json#classes.P10000.workedExamplePlan.releasedT | 2626.200 | 2623.413 |
| research/analysis/delivery.json#classes.P10000.workedExamplePlan.retainedT | 7373.800 | 7376.587 |
| research/analysis/delivery.json#classes.P10000.workedExamplePlan.suppliedMWh | 200.116 | 199.983 |
| research/analysis/delivery.json#classes.P10000.workedExamplePlan.tph | 6657.783 | 6651.588 |
| tests/energy/unheld.mjs#namedEndurance.worstUnheldT | 1.927956588 | 2.135058508 |

## Independent stationary cross-check

The stationary-fill anchors are at 300 m above ground, 1,300 m above sea level, with local ISA density 1.0793 kg/m³. The analysis full bus means battery plus generator rating. The cycle instead receives the nitrogen recovery available in that phase, plus day-average solar.

| Class | Mode | Full-bus model / independent t | Actual mode bus MW | Other draw MW | Mode thrust model / independent t | Full-bus empty floor t |
|---|---|---|---|---|---|---|
| P100 | rapid | 159.325 / 159.325 | 31.238 | 2.122 | 133.407 / 133.407 | 0.000 |
| P100 | balanced | 159.325 / 159.325 | 32.282 | 2.122 | 136.578 / 136.578 | 0.000 |
| P100 | endurance | 159.325 / 159.325 | 33.912 | 2.122 | 141.457 / 141.457 | 0.000 |
| P1000 | rapid | 785.857 / 785.857 | 153.498 | 12.572 | 643.926 / 643.926 | 588.503 |
| P1000 | balanced | 785.857 / 785.857 | 156.061 | 12.572 | 651.709 / 651.709 | 588.503 |
| P1000 | endurance | 785.857 / 785.857 | 160.063 | 12.572 | 663.772 / 663.772 | 588.503 |
| P10000 | rapid | 7551.654 / 7551.654 | 1408.045 | 61.860 | 6874.232 / 6874.232 | 6191.946 |
| P10000 | balanced | 7551.654 / 7551.654 | 1411.659 | 61.860 | 6886.530 / 6886.530 | 6191.946 |
| P10000 | endurance | 7551.654 / 7551.654 | 1417.304 | 61.860 | 6905.714 / 6905.714 | 6191.946 |

A retained-water floor depends on altitude, available supply and the other loads aboard. The generated cross-check names nitrogen, newly loaded water and bag support at the stationary fill instant.

## Retained-water floor at the stationary fill

| Class | km | Basis | Profile | Kept t | Independent floor t | Other support t |
|---|---|---|---|---|---|---|
| P100 | 15 | record | cheapest | 35.000 | 0.000 | newWaterT 19.500; nitrogenT 0.594 |
| P100 | 15 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 3.270 |
| P100 | 15 | favourable | cheapest | 35.000 | 0.000 | newWaterT 19.500; nitrogenT 0.594 |
| P100 | 15 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 3.270 |
| P100 | 60 | record | cheapest | 1.800 | 0.000 | newWaterT 29.460; nitrogenT 1.188 |
| P100 | 60 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 2.391 |
| P100 | 60 | favourable | cheapest | 0.093 | 0.000 | newWaterT 29.972; nitrogenT 1.426 |
| P100 | 60 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 2.391 |
| P1000 | 15 | record | cheapest | 785.210 | 585.543 | newWaterT 64.437; nitrogenT 4.367 |
| P1000 | 15 | favourable | cheapest | 785.210 | 585.543 | newWaterT 64.437; nitrogenT 4.367 |
| P1000 | 60 | record | cheapest | 730.276 | 522.451 | newWaterT 80.917; nitrogenT 17.469 |
| P1000 | 60 | favourable | cheapest | 730.276 | 522.451 | newWaterT 80.917; nitrogenT 17.469 |
| P10000 | 15 | record | cheapest | 7376.587 | 6053.350 | newWaterT 787.024; nitrogenT 4.113 |
| P10000 | 15 | favourable | cheapest | 7376.587 | 6053.350 | newWaterT 787.024; nitrogenT 4.113 |
| P10000 | 60 | record | cheapest | 6993.521 | 5688.357 | newWaterT 901.944; nitrogenT 33.110 |
| P10000 | 60 | favourable | cheapest | 6993.521 | 5688.357 | newWaterT 901.944; nitrogenT 33.110 |
| P100 | 2.55029 | record | cheapest | 45.000 | 0.000 | newWaterT 16.500; nitrogenT 0.052 |
| P100 | 2.55029 | favourable | cheapest | 50.000 | 0.000 | newWaterT 15.000; nitrogenT 0.076 |
| P100 | 7.480511 | record | cheapest | 30.000 | 0.000 | newWaterT 21.000; nitrogenT 0.148 |
| P100 | 7.480511 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 3.447 |
| P100 | 7.480511 | favourable | cheapest | 30.000 | 0.000 | newWaterT 21.000; nitrogenT 0.148 |
| P100 | 7.480511 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 3.447 |
| P100 | 51.913032 | record | cheapest | 2.953 | 0.000 | newWaterT 29.114; nitrogenT 1.028 |
| P100 | 51.913032 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 2.069 |
| P100 | 51.913032 | favourable | cheapest | 1.473 | 0.000 | newWaterT 29.558; nitrogenT 1.234 |
| P100 | 51.913032 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 2.069 |
| P1000 | 2.55029 | record | cheapest | 833.822 | 675.101 | newWaterT 49.853; nitrogenT 0.499 |
| P1000 | 2.55029 | favourable | cheapest | 833.822 | 675.101 | newWaterT 49.853; nitrogenT 0.499 |
| P1000 | 7.480511 | record | cheapest | 830.505 | 655.836 | newWaterT 50.848; nitrogenT 1.220 |
| P1000 | 7.480511 | favourable | cheapest | 794.471 | 630.001 | newWaterT 61.659; nitrogenT 2.178 |
| P1000 | 51.913032 | record | cheapest | 740.088 | 527.749 | newWaterT 77.974; nitrogenT 15.114 |
| P1000 | 51.913032 | favourable | cheapest | 740.088 | 527.749 | newWaterT 77.974; nitrogenT 15.114 |
| P10000 | 2.55029 | record | cheapest | 7389.486 | 6089.609 | newWaterT 783.154; nitrogenT 0.871 |
| P10000 | 2.55029 | favourable | cheapest | 7389.486 | 6089.609 | newWaterT 783.154; nitrogenT 0.871 |
| P10000 | 7.480511 | record | cheapest | 7384.791 | 6076.370 | newWaterT 784.563; nitrogenT 2.051 |
| P10000 | 7.480511 | favourable | cheapest | 7384.791 | 6076.370 | newWaterT 784.563; nitrogenT 2.051 |
| P10000 | 51.913032 | record | cheapest | 7009.805 | 5731.011 | newWaterT 897.059; nitrogenT 28.647 |
| P10000 | 51.913032 | favourable | cheapest | 7009.805 | 5731.011 | newWaterT 897.059; nitrogenT 28.647 |

## Interfaces

`planCycle(class, mode, distance, wind, options)` computes a cycle. `drawAt` supplies each instantaneous ledger.
`cheapestFeasible` performs the slow stated-space search; it is not suitable for a page-load fleet search.
Generated tables cover only their printed distances; they do not promise interpolation. The monitor replays each candidate at the mission’s exact distance, wind and mode and serves only a profile that closes.
<!-- energy:model:end -->
