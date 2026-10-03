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
The [inertia table](../research/analysis/energy-motion.md) compares omitted inertia with simultaneous rotor reserve.
The feasible-profile records also contain that comparison for every phase.

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
The drop altitude, terrain clearance and cable reach stay fixed.
The approach remains stationary.
Segment time and ground distance are integrated; energy uses the same instantaneous ledger.
A profile exceeding the route distance is refused.

Retained water is searched at five-percent payload steps and at each bisected first closing threshold.
Printed requirements round upward at the verdict resolution and replay through the model.
The older whole-phase dilation is named `movingPhaseRateMultiplier`; the new search does not use it.

| Class | km | Basis | As drawn | Minutes | Supplied MWh | kWh/planned tonne | Battery-hours quotient |
|---|---|---|---|---|---|---|---|
| P100 | 15 | record | does not close | 34.196 | 8.192 | 81.923 | 1.418 |
| P100 | 15 | favourable | does not close | 34.196 | 6.402 | 64.017 | 1.824 |
| P100 | 60 | record | closes | 104.784 | 20.521 | 205.214 | 1.742 |
| P100 | 60 | favourable | closes | 104.784 | 14.764 | 147.639 | 2.444 |
| P1000 | 15 | record | does not close | 35.362 | 62.314 | 62.314 | 1.149 |
| P1000 | 15 | favourable | does not close | 35.362 | 61.155 | 61.155 | 1.171 |
| P1000 | 60 | record | does not close | 93.116 | 141.533 | 141.533 | 1.334 |
| P1000 | 60 | favourable | does not close | 93.116 | 142.153 | 142.153 | 1.328 |
| P10000 | 15 | record | does not close | 45.512 | 694.378 | 69.438 | 2.198 |
| P10000 | 15 | favourable | does not close | 45.512 | 757.615 | 75.761 | 2.013 |
| P10000 | 60 | record | does not close | 94.381 | 1113.855 | 111.385 | 2.846 |
| P10000 | 60 | favourable | does not close | 94.381 | 1373.402 | 137.340 | 2.305 |

## Independent stationary cross-check

The analysis full bus means battery plus generator rating. The cycle instead receives the nitrogen recovery available in that phase, plus day-average solar.

| Class | Mode | Full-bus model / independent t | Actual mode bus MW | Other draw MW | Mode thrust model / independent t | Full-bus empty floor t |
|---|---|---|---|---|---|---|
| P100 | rapid | 159.325 / 159.325 | 31.301 | 2.122 | 133.601 / 133.601 | 0.000 |
| P100 | balanced | 159.325 / 159.325 | 32.345 | 2.122 | 136.769 / 136.769 | 0.000 |
| P100 | endurance | 159.325 / 159.325 | 33.976 | 2.122 | 141.645 / 141.645 | 0.000 |
| P1000 | rapid | 785.857 / 785.857 | 153.791 | 12.572 | 644.818 / 644.818 | 588.503 |
| P1000 | balanced | 785.857 / 785.857 | 156.354 | 12.572 | 652.596 / 652.596 | 588.503 |
| P1000 | endurance | 785.857 / 785.857 | 160.356 | 12.572 | 664.651 / 664.651 | 588.503 |
| P10000 | rapid | 7551.654 / 7551.654 | 1408.970 | 61.860 | 6877.378 / 6877.378 | 6191.946 |
| P10000 | balanced | 7551.654 / 7551.654 | 1412.584 | 61.860 | 6889.674 / 6889.674 | 6191.946 |
| P10000 | endurance | 7551.654 / 7551.654 | 1418.228 | 61.860 | 6908.854 / 6908.854 | 6191.946 |

A retained-water floor depends on altitude, available supply and the other loads aboard. The generated cross-check names nitrogen, newly loaded water and bag support at the stationary fill instant.

## Retained-water floor at the stationary fill

| Class | km | Basis | Profile | Kept t | Independent floor t | Other support t |
|---|---|---|---|---|---|---|
| P100 | 15 | record | cheapest | 35.000 | 0.000 | newWaterT 19.500; nitrogenT 0.594 |
| P100 | 15 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 3.270 |
| P100 | 15 | favourable | cheapest | 35.000 | 0.000 | newWaterT 19.500; nitrogenT 0.594 |
| P100 | 15 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 2.967 |
| P100 | 60 | record | cheapest | 1.618 | 0.000 | newWaterT 29.515; nitrogenT 1.188 |
| P100 | 60 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 1.426 |
| P100 | 60 | favourable | cheapest | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 1.426 |
| P100 | 60 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 1.426 |
| P1000 | 15 | record | cheapest | 784.409 | 584.761 | newWaterT 64.677; nitrogenT 4.367 |
| P1000 | 15 | favourable | cheapest | 784.409 | 584.761 | newWaterT 64.677; nitrogenT 4.367 |
| P1000 | 60 | record | cheapest | 729.494 | 521.392 | newWaterT 81.152; nitrogenT 17.469 |
| P1000 | 60 | favourable | cheapest | 729.494 | 521.392 | newWaterT 81.152; nitrogenT 17.469 |
| P10000 | 15 | record | cheapest | 7373.800 | 6049.412 | newWaterT 787.860; nitrogenT 4.113 |
| P10000 | 15 | favourable | cheapest | 7373.800 | 6049.412 | newWaterT 787.860; nitrogenT 4.113 |
| P10000 | 60 | record | cheapest | 6990.703 | 5684.660 | newWaterT 902.789; nitrogenT 33.110 |
| P10000 | 60 | favourable | cheapest | 6990.703 | 5684.660 | newWaterT 902.789; nitrogenT 33.110 |
| P100 | 2.55029 | record | cheapest | 45.000 | 0.000 | newWaterT 16.500; nitrogenT 0.052 |
| P100 | 2.55029 | favourable | cheapest | 50.000 | 0.000 | newWaterT 15.000; nitrogenT 0.076 |
| P100 | 7.480511 | record | cheapest | 30.000 | 0.000 | newWaterT 21.000; nitrogenT 0.148 |
| P100 | 7.480511 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 3.447 |
| P100 | 7.480511 | favourable | cheapest | 30.000 | 0.000 | newWaterT 21.000; nitrogenT 0.148 |
| P100 | 7.480511 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 3.447 |
| P100 | 51.913032 | record | cheapest | 2.771 | 0.000 | newWaterT 29.169; nitrogenT 1.028 |
| P100 | 51.913032 | record | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 2.069 |
| P100 | 51.913032 | favourable | cheapest | 1.291 | 0.000 | newWaterT 29.613; nitrogenT 1.234 |
| P100 | 51.913032 | favourable | full delivery | 0.000 | 0.000 | newWaterT 30.000; nitrogenT 2.069 |
| P1000 | 2.55029 | record | cheapest | 833.024 | 674.034 | newWaterT 50.093; nitrogenT 0.499 |
| P1000 | 2.55029 | favourable | cheapest | 833.024 | 674.034 | newWaterT 50.093; nitrogenT 0.499 |
| P1000 | 7.480511 | record | cheapest | 829.708 | 654.860 | newWaterT 51.088; nitrogenT 1.220 |
| P1000 | 7.480511 | favourable | cheapest | 793.667 | 629.062 | newWaterT 61.900; nitrogenT 2.178 |
| P1000 | 51.913032 | record | cheapest | 739.303 | 526.689 | newWaterT 78.209; nitrogenT 15.114 |
| P1000 | 51.913032 | favourable | cheapest | 739.303 | 526.689 | newWaterT 78.209; nitrogenT 15.114 |
| P10000 | 2.55029 | record | cheapest | 7386.698 | 6085.633 | newWaterT 783.991; nitrogenT 0.871 |
| P10000 | 2.55029 | favourable | cheapest | 7386.698 | 6085.633 | newWaterT 783.991; nitrogenT 0.871 |
| P10000 | 7.480511 | record | cheapest | 7382.002 | 6072.408 | newWaterT 785.399; nitrogenT 2.051 |
| P10000 | 7.480511 | favourable | cheapest | 7382.002 | 6072.408 | newWaterT 785.399; nitrogenT 2.051 |
| P10000 | 51.913032 | record | cheapest | 7006.985 | 5727.276 | newWaterT 897.904; nitrogenT 28.647 |
| P10000 | 51.913032 | favourable | cheapest | 7006.985 | 5727.276 | newWaterT 897.904; nitrogenT 28.647 |

## Interfaces

`planCycle(class, mode, distance, wind, options)` computes a cycle. `drawAt` supplies each instantaneous ledger.
`cheapestFeasible` performs the slow stated-space search; it is not suitable for a page-load fleet search.
Generated tables cover only their printed distances; they do not promise interpolation. The monitor is not yet bound to feasible profiles.
<!-- energy:model:end -->
