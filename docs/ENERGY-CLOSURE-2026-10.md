<!-- energy:closure:start -->
# Energy closure, 2026-10-02

No aircraft has flown. The fleet is simulated. Nothing here says a past fire would have burned differently.

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. Rotor energy and power figures are conditional on a constant hover merit times drive efficiency at every thrust and speed, with no separate blade profile power and no specified blade, rotor-speed or pitch policy. A separated model can move these figures in either direction. An infeasible row prices supplied effort along an unsupported profile. Its energy and battery-hours quotient do not establish delivery or endurance.

| Class | km | Basis | Profile | Delivered t | Kept t | Minutes | MWh | kWh/delivered tonne | Profile note |
|---|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | as drawn: does not close | 100.000 | 0.000 | 34.196 | 7.812 | 78.122 |  |
| P100 | 15 | record | cheapest reserve-eligible profile found in the stated space | 70.948 | 29.052 | 40.108 | 6.622 | 93.338 | quasi-static closure; dynamic profile unresolved |
| P100 | 15 | favourable | as drawn: does not close | 100.000 | 0.000 | 34.196 | 6.024 | 60.241 |  |
| P100 | 15 | favourable | cheapest reserve-eligible profile found in the stated space | 70.000 | 30.000 | 40.076 | 4.843 | 69.192 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | record | as drawn: closes | 100.000 | 0.000 | 104.784 | 20.150 | 201.503 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | record | cheapest reserve-eligible profile found in the stated space | 89.304 | 10.696 | 63.815 | 12.706 | 142.281 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | favourable | as drawn: closes | 100.000 | 0.000 | 104.784 | 14.393 | 143.928 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | favourable | cheapest reserve-eligible profile found in the stated space | 90.930 | 9.070 | 74.835 | 10.035 | 110.357 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | record | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 61.680 | 61.680 |  |
| P1000 | 15 | record | cheapest reserve-eligible profile found in the stated space | 191.775 | 808.225 | 25.483 | 24.472 | 127.610 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | favourable | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 60.689 | 60.689 |  |
| P1000 | 15 | favourable | cheapest reserve-eligible profile found in the stated space | 191.775 | 808.225 | 25.483 | 19.815 | 103.325 | quasi-static closure; dynamic profile unresolved |
| P1000 | 60 | record | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 140.806 | 140.806 | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | cheapest reserve-eligible profile found in the stated space | 244.826 | 755.174 | 73.907 | 65.351 | 266.928 | quasi-static closure; dynamic profile unresolved |
| P1000 | 60 | favourable | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 141.626 | 141.626 | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | cheapest reserve-eligible profile found in the stated space | 244.826 | 755.174 | 73.907 | 54.099 | 220.969 | quasi-static closure; dynamic profile unresolved |
| P10000 | 15 | record | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 679.093 | 67.909 |  |
| P10000 | 15 | record | cheapest reserve-eligible profile found in the stated space | 2945.496 | 7054.504 | 24.022 | 202.102 | 68.614 | quasi-static closure; dynamic profile unresolved |
| P10000 | 15 | favourable | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 750.823 | 75.082 |  |
| P10000 | 15 | favourable | cheapest reserve-eligible profile found in the stated space | 2945.496 | 7054.504 | 24.022 | 184.209 | 62.539 | quasi-static closure; dynamic profile unresolved |
| P10000 | 60 | record | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1098.254 | 109.825 |  |
| P10000 | 60 | record | cheapest reserve-eligible profile found in the stated space | 2993.634 | 7006.366 | 58.071 | 402.745 | 134.534 | quasi-static closure; dynamic profile unresolved |
| P10000 | 60 | favourable | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1370.397 | 137.040 |  |
| P10000 | 60 | favourable | cheapest reserve-eligible profile found in the stated space | 3009.668 | 6990.332 | 70.313 | 368.571 | 122.462 | quasi-static closure; dynamic profile unresolved |

## Zero-sunlight sensitivity of the selected profiles

Replay every printed selected profile at the same hardware, collecting area, route, basis, mode and controls, changing only solarWPerM2 to zero. Averaged sunlight is credited to instantaneous bus supply before rotor thrust allocation. Unsupported energy is diagnostic supplied effort.

No night search was run. This record does not show that no profile closes at night, and establishes no flight performance.

| Class | km | Basis | Mode | Averaged solar MW | Current verdict | Zero-sunlight verdict | Zero-sunlight worst unheld tf / phase | Zero-sunlight supplied MWh | Storage note |
|---|---|---|---|---|---|---|---|---|---|
| P100 | selected 15 km | record | balanced | 0.207 MW bus input | closes | closes | 0.000 / SOURCE_APPROACH | 6.622 MWh zero-sunlight replay |  |
| P100 | selected 15 km | favourable | balanced | 0.207 MW bus input | closes | closes | 0.000 / SOURCE_APPROACH | 4.843 MWh zero-sunlight replay |  |
| P100 | selected 60 km | record | rapid | 0.207 MW bus input | closes | closes | 0.000 / SOURCE_APPROACH | 12.706 MWh zero-sunlight replay |  |
| P100 | selected 60 km | favourable | rapid | 0.207 MW bus input | closes | closes | 0.000 / SOURCE_APPROACH | 10.035 MWh zero-sunlight replay |  |
| P1000 | selected 15 km | record | endurance | 0.967 MW bus input | closes | closes | 0.000 / SOURCE_APPROACH | 24.472 MWh zero-sunlight replay |  |
| P1000 | selected 15 km | favourable | endurance | 0.967 MW bus input | closes | closes | -0.000 / WATER_RELEASE | 19.815 MWh zero-sunlight replay |  |
| P1000 | selected 60 km | record | endurance | 0.967 MW bus input | closes | closes | 0.000 / SOURCE_APPROACH | 65.351 MWh zero-sunlight replay |  |
| P1000 | selected 60 km | favourable | endurance | 0.967 MW bus input | closes | closes | 0.000 / SOURCE_APPROACH | 54.099 MWh zero-sunlight replay |  |
| P10000 | selected 15 km | record | rapid | 4.476 MW bus input | closes | closes | -0.000 / SOURCE_APPROACH | 202.102 MWh zero-sunlight replay |  |
| P10000 | selected 15 km | favourable | rapid | 4.476 MW bus input | closes | closes | -0.000 / SOURCE_APPROACH | 184.209 MWh zero-sunlight replay |  |
| P10000 | selected 60 km | record | rapid | 4.476 MW bus input | closes | closes | -0.000 / SOURCE_APPROACH | 402.745 MWh zero-sunlight replay |  |
| P10000 | selected 60 km | favourable | rapid | 4.476 MW bus input | closes | closes | -0.000 / SOURCE_APPROACH | 368.571 MWh zero-sunlight replay |  |

P100, balanced, 15 km record: averaged sunlight closes; zero sunlight closes. P1000, endurance, 15 km record: averaged sunlight closes; zero sunlight closes. P10000, rapid, 15 km record: averaged sunlight closes; zero sunlight closes.

Record: `research/analysis/energy-zero-sun.json`; generator: `research/analysis/energy-zero-sun.mjs`.

## Where the prescribed hull is unheld

Generated by `node research/analysis/energy-unheld.mjs`. Largest absolute signed unheld force in each failing phase, using the verdict mesh, refined extrema and both sides of seams from cycleLimits, with additional local refinement for the printed phase peak. Positive is unsupported surplus lift; negative requires unavailable upward authority.

| Class | km | Basis | Profile | Phase | Signed unheld, t | Progress | Cycle minute | Airspeed, m/s | Vertical speed, m/s | Limits | Storage note |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---|---|
| P100 | 15 | record | as drawn | SOURCE_APPROACH | 2.334 | 0.604878 | 1.210 | 0.000 | -2.283 | bus power, anchor cable reach |  |
| P100 | 15 | record | as drawn | OUTBOUND_TRANSIT | -5.714 | 0.222832 | 7.955 | 25.000 | 9.745 | upward authority unavailable |  |
| P100 | 15 | record | as drawn | RETURN_TRANSIT | 34.759 | 0.810716 | 31.969 | 25.000 | -8.821 | bus power |  |
| P100 | 15 | favourable | as drawn | SOURCE_APPROACH | 2.334 | 0.604878 | 1.210 | 0.000 | -2.283 | bus power, aerodynamic coefficient, anchor cable reach |  |
| P100 | 15 | favourable | as drawn | OUTBOUND_TRANSIT | -5.714 | 0.222832 | 7.955 | 25.000 | 9.745 | upward authority unavailable |  |
| P100 | 60 | record | as drawn | no unheld phase | 0 | | | | | |  |
| P100 | 60 | favourable | as drawn | no unheld phase | 0 | | | | | |  |
| P1000 | 15 | record | as drawn | SOURCE_APPROACH | 800.681 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, anchor cable reach |  |
| P1000 | 15 | record | as drawn | WATER_FILL | 418.983 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |  |
| P1000 | 15 | record | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 23.737 | 0.000 | 0.052 | bus power, rotor thrust |  |
| P1000 | 15 | record | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 23.737 | 0.000 | 0.011 | bus power, rotor thrust |  |
| P1000 | 15 | record | as drawn | RETURN_TRANSIT | 588.712 | 1.000000 | 35.362 | 9.167 | -0.000 | bus power, rotor thrust |  |
| P1000 | 15 | favourable | as drawn | SOURCE_APPROACH | 800.681 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P1000 | 15 | favourable | as drawn | WATER_FILL | 418.983 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P1000 | 15 | favourable | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 23.737 | 0.000 | 0.052 | bus power, rotor thrust, aerodynamic coefficient |  |
| P1000 | 15 | favourable | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 23.737 | 0.000 | 0.011 | bus power, rotor thrust, aerodynamic coefficient |  |
| P1000 | 15 | favourable | as drawn | RETURN_TRANSIT | 504.128 | 1.000000 | 35.362 | 9.167 | -0.000 | bus power, rotor thrust, aerodynamic coefficient |  |
| P1000 | 60 | record | as drawn | SOURCE_APPROACH | 750.235 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | WATER_FILL | 362.490 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 52.614 | 0.000 | 0.052 | bus power, rotor thrust | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 52.614 | 0.000 | 0.014 | bus power, rotor thrust | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | RETURN_TRANSIT | 566.252 | 1.000000 | 93.116 | 9.167 | -0.000 | bus power, rotor thrust | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | SOURCE_APPROACH | 750.235 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | WATER_FILL | 362.490 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 52.614 | 0.000 | 0.052 | bus power, rotor thrust, aerodynamic coefficient | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 52.614 | 0.000 | 0.014 | bus power, rotor thrust, aerodynamic coefficient | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | RETURN_TRANSIT | 481.668 | 1.000000 | 93.116 | 9.167 | -0.000 | bus power, rotor thrust, aerodynamic coefficient | unsupported profile; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | as drawn | SOURCE_APPROACH | 6366.280 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 15 | record | as drawn | WATER_FILL | 3846.724 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 15 | record | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 35.367 | 0.000 | 0.026 | bus power, rotor thrust |  |
| P10000 | 15 | record | as drawn | BUOYANCY_ESCAPE | 6096.904 | 0.000000 | 35.367 | 0.000 | 0.008 | bus power, rotor thrust |  |
| P10000 | 15 | record | as drawn | RETURN_TRANSIT | 4994.044 | 0.000000 | 37.367 | 30.694 | 0.000 | rotor thrust |  |
| P10000 | 15 | favourable | as drawn | SOURCE_APPROACH | 6366.280 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 15 | favourable | as drawn | WATER_FILL | 3846.724 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 15 | favourable | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 35.367 | 0.000 | 0.026 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 15 | favourable | as drawn | BUOYANCY_ESCAPE | 6096.904 | 0.000000 | 35.367 | 0.000 | 0.008 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 15 | favourable | as drawn | RETURN_TRANSIT | 3959.850 | 1.000000 | 45.512 | 10.833 | 0.000 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 60 | record | as drawn | SOURCE_APPROACH | 6250.297 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 60 | record | as drawn | WATER_FILL | 3742.576 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 60 | record | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 59.801 | 0.000 | 0.026 | bus power, rotor thrust |  |
| P10000 | 60 | record | as drawn | BUOYANCY_ESCAPE | 6096.903 | 0.000000 | 59.801 | 0.000 | 0.014 | bus power, rotor thrust |  |
| P10000 | 60 | record | as drawn | RETURN_TRANSIT | 4518.750 | 0.000000 | 61.801 | 30.694 | 0.000 | rotor thrust |  |
| P10000 | 60 | favourable | as drawn | SOURCE_APPROACH | 6250.297 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 60 | favourable | as drawn | WATER_FILL | 3742.576 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 60 | favourable | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 59.801 | 0.000 | 0.026 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 60 | favourable | as drawn | BUOYANCY_ESCAPE | 6096.903 | 0.000000 | 59.801 | 0.000 | 0.014 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 60 | favourable | as drawn | RETURN_TRANSIT | 3896.501 | 1.000000 | 94.381 | 10.833 | -0.000 | bus power, rotor thrust, aerodynamic coefficient |  |

The cheapest feasible profiles found in the stated space, including their minutes and delivery, are in [the profile table](../research/analysis/energy-profiles.md).

Neither larger class delivers its nameplate payload on the drawn hardware in this search; its delivered and retained figures appear above on both bases.

## Full payload where the search finds it

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. Rotor energy and power figures are conditional on a constant hover merit times drive efficiency at every thrust and speed, with no separate blade profile power and no specified blade, rotor-speed or pitch policy. A separated model can move these figures in either direction.

No full-payload profile meets the control reserve target in this stated search.

| Class | km | Basis | Full-payload mode | Delivered t | Minutes | MWh | kWh/t | Profile note |
|---|---|---|---|---|---|---|---|---|


## What would close the gap

First consider a slower letdown at lower airspeed and a climb the surplus can drive.
Then consider water kept aboard, with its cost in delivered tonnes.
The battery-and-thrust requirements come next, with their implied mass.

## What the model would require

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. Rotor energy and power figures are conditional on a constant hover merit times drive efficiency at every thrust and speed, with no separate blade profile power and no specified blade, rotor-speed or pitch policy. A separated model can move these figures in either direction.

Generated by `node research/analysis/energy-tables.mjs`. Each printed closing value is rounded up to three decimals and replayed at the verdict resolution.

| Class | km | Basis | As drawn | Minutes: drawn / kept / power pair | Water kept, t | Delivered, t | kWh/t | Required battery, MW | Rotor thrust, t | Battery mass, t (500 / 300 / 149 Wh/kg) | Storage notes |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|
| P100 | 15 | record | does not close | 34.196 / none / none | none | none | none | none | none | none |  |
| P100 | 15 | favourable | does not close | 34.196 / none / none | none | none | none | none | none | none |  |
| P100 | 60 | record | closes | 104.784 / 104.784 / 104.784 | 0.000 | 100.000 | 201.503 | 29.850 | 131.166 | 39.800 / 66.333 / 133.557 (exceeds dry target) | retained-water: ; power pair:  |
| P100 | 60 | favourable | closes | 104.784 / 104.784 / 104.784 | 0.000 | 100.000 | 143.928 | 28.658 | 131.166 | 38.211 / 63.684 / 128.224 (exceeds dry target) | retained-water: ; power pair:  |
| P1000 | 15 | record | does not close | 35.362 / 28.389 / 35.362 | 800.681 | 199.319 | 123.582 | 521.681 | 1367.262 | 834.690 / 1391.149 (exceeds dry target) / 2800.972 (exceeds dry target) | retained-water: ; power pair:  |
| P1000 | 15 | favourable | does not close | 35.362 / 28.389 / 35.362 | 800.681 | 199.319 | 96.228 | 521.681 | 1367.262 | 834.690 / 1391.149 (exceeds dry target) / 2800.972 (exceeds dry target) | retained-water: ; power pair:  |
| P1000 | 60 | record | does not close | 93.116 / 86.423 / 93.116 | 750.235 | 249.765 | 267.061 | 499.667 | 1349.041 | 799.467 / 1332.445 (exceeds dry target) / 2682.776 (exceeds dry target) | unsupported profile; exceeds nominal storage in an ideal cycle; retained-water: ; power pair: quasi-static closure; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | does not close | 93.116 / 86.423 / 93.116 | 750.235 | 249.765 | 208.265 | 499.667 | 1349.041 | 799.467 / 1332.445 (exceeds dry target) / 2682.776 (exceeds dry target) | unsupported profile; exceeds nominal storage in an ideal cycle; retained-water: ; power pair: quasi-static closure; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | does not close | 45.512 / 32.455 / 45.512 | 6366.275 | 3633.725 | 79.727 | 3892.845 | 13092.990 | 11122.414 (exceeds dry target) / 18537.357 (exceeds dry target) / 37323.538 (exceeds dry target) | retained-water: ; power pair:  |
| P10000 | 15 | favourable | does not close | 45.512 / 32.455 / 45.512 | 6366.275 | 3633.725 | 71.249 | 3892.845 | 13092.990 | 11122.414 (exceeds dry target) / 18537.357 (exceeds dry target) / 37323.538 (exceeds dry target) | retained-water: ; power pair:  |
| P10000 | 60 | record | does not close | 94.381 / 81.453 / 94.381 | 6250.292 | 3749.708 | 148.256 | 3848.409 | 13092.989 | 10995.454 (exceeds dry target) / 18325.757 (exceeds dry target) / 36897.498 (exceeds dry target) | retained-water: ; power pair:  |
| P10000 | 60 | favourable | does not close | 94.381 / 81.453 / 94.381 | 6250.292 | 3749.708 | 129.694 | 3848.409 | 13092.989 | 10995.454 (exceeds dry target) / 18325.757 (exceeds dry target) / 36897.498 (exceeds dry target) | retained-water: ; power pair:  |

Cycle minutes are printed separately for the prescribed profile, retained-water requirement and power-and-thrust requirement.

The battery masses retain each class's energy-to-peak-power ratio. Power alone does not fix storage mass. These are requirements, never equipment options.

Specific energies and their source qualifications bind to `research/analysis/mass-budget.json`. Values that exceed the entire dry-mass target are marked.

The bag counts when the cable carries water; the hoist remains priced. Delaying force credit until hoisting finishes changes the retained-water requirement as follows.

| Class | km | Basis | Extra water kept under stricter rule, t |
|---|---:|---|---:|
| P100 | 15 | record | none |
| P100 | 15 | favourable | none |
| P100 | 60 | record | 0.000 |
| P100 | 60 | favourable | 0.000 |
| P1000 | 15 | record | 61.681 |
| P1000 | 15 | favourable | 61.681 |
| P1000 | 60 | record | 60.430 |
| P1000 | 60 | favourable | 60.430 |
| P10000 | 15 | record | 388.207 |
| P10000 | 15 | favourable | 388.207 |
| P10000 | 60 | record | 386.953 |
| P10000 | 60 | favourable | 386.953 |

## Broadside-drag range

Each entry gives the signed worst unheld force in tonnes and the feasibility verdict. Negative force needs upward authority, which is unavailable.

| Class | km | Basis | Coefficient 0 | Coefficient 1 | Coefficient 2 |
|---|---:|---|---|---|---|
| P100 | 15 | record | 13.274; does not close;  | 34.759; does not close;  | 56.679; does not close;  |
| P100 | 15 | favourable | 0.798; does not close;  | -5.714; does not close;  | -32.818; does not close;  |
| P100 | 60 | record | 0.000; closes;  | -0.000; closes;  | -0.000; closes;  |
| P100 | 60 | favourable | 0.000; closes;  | -0.000; closes;  | -0.000; closes;  |
| P1000 | 15 | record | 718.423; does not close;  | 800.681; does not close;  | 882.939; does not close;  |
| P1000 | 15 | favourable | 718.423; does not close;  | 800.681; does not close;  | 882.939; does not close;  |
| P1000 | 60 | record | 667.977; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 750.235; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 832.493; does not close; unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | 667.977; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 750.235; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 832.493; does not close; unsupported profile; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | 6167.429; does not close;  | 6366.280; does not close;  | 6565.131; does not close;  |
| P10000 | 15 | favourable | 6167.429; does not close;  | 6366.280; does not close;  | 6565.131; does not close;  |
| P10000 | 60 | record | 6096.904; does not close;  | 6250.297; does not close;  | 6449.148; does not close;  |
| P10000 | 60 | favourable | 6096.904; does not close;  | 6250.297; does not close;  | 6449.148; does not close;  |

## Rotor-efficiency range

Rotor energy and power figures are conditional on a constant hover merit times drive efficiency at every thrust and speed, with no separate blade profile power and no specified blade, rotor-speed or pitch policy. A separated model can move these figures in either direction. Hold-down descent is priced as climb, on the conservative side; climb against hold-down thrust is priced as level flight, with no bound claimed.

| Class | km | Basis | Efficiency | Static thrust cap over local densities, t | Worst unheld force, t | Verdict | Storage note |
|---|---:|---|---:|---|---:|---|---|
| P100 | 15 | record | 0.55 | 130.327 to 135.663 | 47.665 | does not close |  |
| P100 | 15 | record | 0.7 | 153.059 to 159.325 | 34.759 | does not close |  |
| P100 | 15 | favourable | 0.55 | 130.327 to 135.663 | 47.665 | does not close |  |
| P100 | 15 | favourable | 0.7 | 153.059 to 159.325 | -5.714 | does not close |  |
| P100 | 60 | record | 0.55 | 130.327 to 135.663 | 17.748 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P100 | 60 | record | 0.7 | 153.059 to 159.325 | -0.000 | closes |  |
| P100 | 60 | favourable | 0.55 | 130.327 to 135.663 | 15.997 | does not close |  |
| P100 | 60 | favourable | 0.7 | 153.059 to 159.325 | -0.000 | closes |  |
| P1000 | 15 | record | 0.55 | 646.328 to 669.145 | 892.273 | does not close |  |
| P1000 | 15 | record | 0.7 | 759.061 to 785.857 | 800.681 | does not close |  |
| P1000 | 15 | favourable | 0.55 | 646.328 to 669.145 | 892.273 | does not close |  |
| P1000 | 15 | favourable | 0.7 | 759.061 to 785.857 | 800.681 | does not close |  |
| P1000 | 60 | record | 0.55 | 642.828 to 669.145 | 846.818 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | 0.7 | 754.950 to 785.857 | 750.235 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | 0.55 | 642.828 to 669.145 | 846.818 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | 0.7 | 754.950 to 785.857 | 750.235 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | 0.55 | 6238.062 to 6430.112 | 7322.061 | does not close |  |
| P10000 | 15 | record | 0.7 | 7326.107 to 7551.654 | 6366.280 | does not close |  |
| P10000 | 15 | favourable | 0.55 | 6238.062 to 6430.112 | 7322.061 | does not close |  |
| P10000 | 15 | favourable | 0.7 | 7326.107 to 7551.654 | 6366.280 | does not close |  |
| P10000 | 60 | record | 0.55 | 6177.222 to 6430.112 | 7215.718 | does not close |  |
| P10000 | 60 | record | 0.7 | 7254.655 to 7551.654 | 6250.297 | does not close |  |
| P10000 | 60 | favourable | 0.55 | 6177.222 to 6430.112 | 7215.718 | does not close |  |
| P10000 | 60 | favourable | 0.7 | 7254.655 to 7551.654 | 6250.297 | does not close |  |

A different vehicle is a separate question. The [payload-exchange study](../research/analysis/payload-exchange.md) is analysis, not design.
Its half-load hull gives up fail-safe float-up and needs upward thrust, which the drawn rotors lack.
An approach at airspeed needs a demonstrated hand-over to the bag. Variable displacement needs changing sealed cells; cryogenic ballast needs added energy and plant mass.

## Earlier published figures beside the model

Earlier figures remain dated history and are outside the current necessary-energy diagnostic; current prescribed cells are covered. They used incomplete force allocation. The intermediate steps are preserved in `energy-closure-history.json`.

| Class | km | Quantity | Earlier published | Intermediate published | Record as drawn | Favourable as drawn | Reason | Current record / favourable storage notes |
|---|---|---|---|---|---|---|---|---|
| P100 | 15 | cycleMWh | 1.391 | 2.023 | 7.812 | 6.024 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P100 | 15 | kwhPerTonne | 13.913 | 20.230 | 78.122 | 60.241 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P100 | 15 | peakRotorMW | 0.300 | 11.806 | 31.411 | 31.411 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P100 | 15 | hoursOnBattery | 9.211 | 6.098 | 1.481 | 1.930 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P100 | 60 | cycleMWh | 4.884 | 6.094 | 20.150 | 14.393 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P100 | 60 | kwhPerTonne | 48.840 | 60.937 | 201.503 | 143.928 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P100 | 60 | peakRotorMW | 0.101 | 11.035 | 30.669 | 30.669 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P100 | 60 | hoursOnBattery | 7.916 | 6.213 | 1.765 | 2.489 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P1000 | 15 | cycleMWh | 8.454 | 18.149 | 61.680 | 60.689 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P1000 | 15 | kwhPerTonne | 8.454 | 18.149 | 61.680 | 60.689 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P1000 | 15 | peakRotorMW | 5.017 | 146.341 | 153.504 | 153.504 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P1000 | 15 | hoursOnBattery | 9.171 | 4.063 | 1.157 | 1.176 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P1000 | 60 | cycleMWh | 26.812 | 43.193 | 140.806 | 141.626 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile | unsupported profile; exceeds nominal storage in an ideal cycle / unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | kwhPerTonne | 26.812 | 43.193 | 140.806 | 141.626 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile | unsupported profile; exceeds nominal storage in an ideal cycle / unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | peakRotorMW | 3.642 | 148.475 | 165.632 | 165.632 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile | unsupported profile; exceeds nominal storage in an ideal cycle / unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | hoursOnBattery | 7.492 | 4.516 | 1.337 | 1.329 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile | unsupported profile; exceeds nominal storage in an ideal cycle / unsupported profile; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | cycleMWh | 54.325 | 176.000 | 679.093 | 750.823 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P10000 | 15 | kwhPerTonne | 5.433 | 17.600 | 67.909 | 75.082 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P10000 | 15 | peakRotorMW | 52.293 | 1157.272 | 1404.786 | 1404.786 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P10000 | 15 | hoursOnBattery | 30.203 | 8.825 | 2.245 | 2.030 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P10000 | 60 | cycleMWh | 143.117 | 302.894 | 1098.254 | 1370.397 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P10000 | 60 | kwhPerTonne | 14.312 | 30.289 | 109.825 | 137.040 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P10000 | 60 | peakRotorMW | 48.581 | 1146.957 | 1425.310 | 1425.310 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |
| P10000 | 60 | hoursOnBattery | 23.369 | 10.686 | 2.883 | 2.308 | Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile |  /  |

| Class | km | Basis | Kept t: earlier / current | Delivered t: earlier / current | Minutes: earlier / current | kWh/t: earlier / current | Effect |
|---|---|---|---|---|---|---|---|
| P100 | 15 | record | 30.000 / 35.000 | 70.000 / 65.000 | 28.031 / 34.914 | 72.532 / 80.021 | Higher cost in this changed search space |
| P100 | 15 | favourable | 30.000 / 35.000 | 70.000 / 65.000 | 28.031 / 34.914 | 57.219 / 58.359 | Higher cost in this changed search space |
| P100 | 60 | record | 1.618 / 1.618 | 98.382 / 98.382 | 64.420 / 64.420 | 143.315 / 143.315 | Same cost at printed precision |
| P100 | 60 | favourable | 0.000 / 0.000 | 100.000 / 100.000 | 75.440 / 75.440 | 112.630 / 112.630 | Same cost at printed precision |
| P1000 | 15 | record | 799.036 / 784.409 | 200.964 / 215.591 | 23.872 / 25.616 | 116.671 / 122.866 | Higher cost in this changed search space |
| P1000 | 15 | favourable | 799.036 / 784.409 | 200.964 / 215.591 | 23.872 / 25.616 | 95.043 / 99.905 | Higher cost in this changed search space |
| P1000 | 60 | record | 778.328 / 729.494 | 221.672 / 270.506 | 68.628 / 74.049 | 247.515 / 254.583 | Higher cost in this changed search space |
| P1000 | 60 | favourable | 724.819 / 729.494 | 275.181 / 270.506 | 79.338 / 74.049 | 197.732 / 209.457 | Higher cost in this changed search space |
| P10000 | 15 | record | 7373.800 / 7373.800 | 2626.200 / 2626.200 | 23.667 / 23.667 | 76.200 / 76.200 | Same cost at printed precision |
| P10000 | 15 | favourable | 7373.800 / 7373.800 | 2626.200 / 2626.200 | 23.667 / 23.667 | 69.842 / 69.842 | Same cost at printed precision |
| P10000 | 60 | record | 6871.083 / 6990.703 | 3128.917 / 3009.297 | 66.276 / 66.573 | 145.503 / 146.164 | Higher cost in this changed search space |
| P10000 | 60 | favourable | 6871.083 / 6990.703 | 3128.917 / 3009.297 | 66.276 / 66.573 | 131.650 / 132.178 | Higher cost in this changed search space |
| P100 | 2.55029 | record | 45.000 / 45.000 | 55.000 / 55.000 | 9.987 / 9.987 | 34.444 / 34.444 | Same cost at printed precision |
| P100 | 2.55029 | favourable | 50.000 / 50.000 | 50.000 / 50.000 | 10.193 / 10.193 | 28.196 / 28.196 | Same cost at printed precision |
| P100 | 7.480511 | record | 30.000 / 30.000 | 70.000 / 70.000 | 14.769 / 14.769 | 45.770 / 45.770 | Same cost at printed precision |
| P100 | 7.480511 | favourable | 30.000 / 30.000 | 70.000 / 70.000 | 14.769 / 14.769 | 38.318 / 38.318 | Same cost at printed precision |
| P100 | 51.913032 | record | 2.771 / 2.771 | 97.229 / 97.229 | 56.989 / 56.989 | 129.305 / 129.305 | Same cost at printed precision |
| P100 | 51.913032 | favourable | 1.291 / 1.291 | 98.709 / 98.709 | 66.529 / 66.529 | 101.739 / 101.739 | Same cost at printed precision |
| P1000 | 2.55029 | record | 804.475 / 833.024 | 195.525 / 166.976 | 13.895 / 12.461 | 73.938 / 74.378 | Higher cost in this changed search space |
| P1000 | 2.55029 | favourable | 804.475 / 833.024 | 195.525 / 166.976 | 13.895 / 12.461 | 62.215 / 62.452 | Higher cost in this changed search space |
| P1000 | 7.480511 | record | 802.509 / 829.708 | 197.491 / 170.292 | 16.394 / 14.367 | 86.216 / 91.018 | Higher cost in this changed search space |
| P1000 | 7.480511 | favourable | 802.509 / 793.667 | 197.491 / 206.333 | 16.394 / 17.522 | 71.504 / 76.873 | Higher cost in this changed search space |
| P1000 | 51.913032 | record | 782.040 / 739.303 | 217.960 / 260.697 | 60.585 / 65.346 | 224.340 / 232.813 | Higher cost in this changed search space |
| P1000 | 51.913032 | favourable | 731.604 / 739.303 | 268.396 / 260.697 | 70.075 / 65.346 | 180.217 / 191.790 | Higher cost in this changed search space |
| P10000 | 2.55029 | record | 7386.698 / 7386.698 | 2613.302 / 2613.302 | 17.041 / 17.041 | 57.040 / 57.040 | Same cost at printed precision |
| P10000 | 2.55029 | favourable | 7386.698 / 7386.698 | 2613.302 / 2613.302 | 17.041 / 17.041 | 53.249 / 53.249 | Same cost at printed precision |
| P10000 | 7.480511 | record | 7382.002 / 7382.002 | 2617.998 / 2617.998 | 18.672 / 18.672 | 62.341 / 62.341 | Same cost at printed precision |
| P10000 | 7.480511 | favourable | 7382.002 / 7382.002 | 2617.998 / 2617.998 | 18.672 / 18.672 | 57.820 / 57.820 | Same cost at printed precision |
| P10000 | 51.913032 | record | 6879.541 / 7006.985 | 3120.459 / 2993.015 | 59.466 / 59.529 | 134.041 / 134.248 | Higher cost in this changed search space |
| P10000 | 51.913032 | favourable | 6879.541 / 7006.985 | 3120.459 / 2993.015 | 59.466 / 59.529 | 121.313 / 121.437 | Higher cost in this changed search space |

Independent vertical controls and smooth joins change the finite search space. Neither comparison proves a global minimum.

| Earlier publication (outside storage diagnostic) | Quantity | Earlier value | Current record / favourable | Cause and effect |
|---|---|---|---|---|
| PHYSICS section 6 | P100 balanced cruise MW | 1.06 | 1.269 / 1.269 | Capsule frontal area and local density; higher hull drag |
| PHYSICS section 6 | P1000 balanced cruise MW | 9.16 | 10.843 / 10.843 | Capsule frontal area and local density; higher hull drag |
| PHYSICS section 6 | P10000 balanced cruise MW | 69.68 | 82.829 / 82.829 | Capsule frontal area and local density; higher hull drag |
| PHYSICS section 5 | P100 electrical fill MWh | 0.091 | 0.109 / 0.109 | Correct head in the published arithmetic; higher pumping bill |
| PHYSICS section 5 | P10000 electrical fill MWh | 9.08 | 10.900 / 10.900 | Correct head in the published arithmetic; higher pumping bill |
| PHYSICS section 5 | P100 ideal fill MWh | 0.068 | 0.082 / 0.082 | Correct head; higher potential energy |
| PHYSICS section 8, superseded peak-solar record dated 2026-08-09 | P100 ground-surplus lossless energy quotient, days | 2.6 | 58.189 / 58.189 | Day-average solar replaces retired peak assumption; longer lossless quotient, accumulation and retention unshown |
| PHYSICS section 8, superseded peak-solar record dated 2026-08-09 | P1000 ground-surplus lossless energy quotient, days | 5.7 | 162.233 / 162.233 | Day-average solar replaces retired peak assumption; longer lossless quotient, accumulation and retention unshown |
| PHYSICS section 8, superseded peak-solar record dated 2026-08-09 | P10000 ground-surplus lossless energy quotient, days | 12.9 | 183.696 / 183.696 | Day-average solar replaces retired peak assumption; longer lossless quotient, accumulation and retention unshown |
| PHYSICS section 8 | P100 full tank MWh | 65 | 69.750 / 69.750 | Earlier energy used ground surplus, not tank capacity; higher tank bill |
| PHYSICS section 8 | P1000 full tank MWh | 651 | 697.500 / 697.500 | Earlier energy used ground surplus, not tank capacity; higher tank bill |
| PHYSICS section 8 | P10000 full tank MWh | 6505 | 6975.000 / 6975.000 | Earlier energy used ground surplus, not tank capacity; higher tank bill |
| sim README | P100 hull dimensions m | 190 × 47 | 110 × 55 | Configured capsule; shorter and wider, no performance conclusion |
| sim README | P1000 hull dimensions m | 404 × 102 | 238 × 119 | Configured capsule; shorter and wider, no performance conclusion |
| sim README | P10000 hull dimensions m | 876 × 219 | 512 × 256 | Configured capsule; shorter and wider, no performance conclusion |
| sim README | Nitrogen recovery fraction | 0.5 | 0.2 / 0.2 | Storage recovery constrained by exergy; less recovered energy |
| Earlier physics reading | P10000 cycle MWh | 88.2 | 679.093 / 750.823 | No reproducible old mode or snapshot; current unsupported-cycle effort is larger |

| Report and former line (historical cells outside storage diagnostic) | Generated field | Earlier printed | Earlier correction | Current record | Current favourable | Reason | Current record / favourable storage notes |
|---|---|---|---|---|---|---|---|
| research/reports/01-brief.md:45 | P100.cycle.kwhPerTonne | 80.4 | 81.9 | 78.122 | 60.241 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/01-brief.md:62 | P100.cycle.kwhPerTonne | 80.4 | 81.9 | 78.122 | 60.241 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/01-brief.md:63 | P1000.cycle.kwhPerTonne | 62.5 | 62.3 | 61.680 | 60.689 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/01-brief.md:63 | P10000.cycle.kwhPerTonne | 69.8 | 69.4 | 67.909 | 75.082 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/01-brief.md:105 | P10000.descent.rotorCapT | 7,124 | 7,079 | 7079.204 | 7079.204 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:173 | P100.descent.rotorCapT | 141.4 | 140.5 | 140.542 | 140.542 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:173 | P1000.descent.rotorCapT | 687.6 | 683.3 | 683.286 | 683.286 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:173 | P10000.descent.rotorCapT | 7,124.3 | 7,079.2 | 7079.204 | 7079.204 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:217 | P10000.energy.letdownMWh | 117.284 | 117.219 | 102.086 | 101.388 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:227 | P100.cycle.eCycleMWh | 8.042 | 8.192 | 7.812 | 6.024 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:254 | P10000.energy.ledgerMWh.RETURN_TRANSIT | 112.360 | 114.038 | 114.037 | 190.653 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:255 | P10000.energy.ledgerMWh.WATER_FILL | 213.327 | 214.046 | 213.959 | 213.959 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:257 | P10000.energy.ledgerMWh.OUTBOUND_TRANSIT | 34.838 | 34.345 | 34.345 | 28.129 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:258 | P10000.energy.letdownMWh | 117.284 | 117.219 | 102.086 | 101.388 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:261 | P10000.cycle.eCycleMWh | 697.586 | 694.378 | 679.093 | 750.823 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:274 | P100.cycle.kwhPerTonne | 80.42 | 81.92 | 78.122 | 60.241 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:275 | P1000.cycle.kwhPerTonne | 62.50 | 62.31 | 61.680 | 60.689 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:275 | P10000.cycle.kwhPerTonne | 69.76 | 69.44 | 67.909 | 75.082 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:309 | P100.cycle.eCycleMWh | 8.042 | 8.192 | 7.812 | 6.024 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:309 | P100.energy.deficitPerCycleMWh | 7.89 | 8.04 | 7.694 | 5.906 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:310 | P1000.cycle.eCycleMWh | 62.500 | 62.314 | 61.680 | 60.689 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:310 | P1000.energy.deficitPerCycleMWh | 61.76 | 61.57 | 61.110 | 60.119 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:311 | P10000.cycle.eCycleMWh | 697.586 | 694.378 | 679.093 | 750.823 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:311 | P10000.energy.deficitPerCycleMWh | 693.49 | 690.28 | 675.698 | 747.428 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:377 | P100.energy.deficitPerCycleMWh | 7.89 | 8.04 | 7.694 | 5.906 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:378 | P1000.energy.deficitPerCycleMWh | 61.76 | 61.57 | 61.110 | 60.119 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:379 | P10000.energy.deficitPerCycleMWh | 693.49 | 690.28 | 675.698 | 747.428 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/02-paper.md:404 | P10000.cycle.eCycleMWh | 697.586 | 694.378 | 679.093 | 750.823 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:50 | P100.cycle.kwhPerTonne | 80.42 | 81.92 | 78.122 | 60.241 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:69 | P100.cycle.kwhPerTonne | 80.42 | 81.92 | 78.122 | 60.241 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:70 | P10000.cycle.kwhPerTonne | 69.76 | 69.44 | 67.909 | 75.082 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:133 | P100.cycle.kwhPerTonne | 80.42 | 81.92 | 78.122 | 60.241 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:133 | P1000.cycle.kwhPerTonne | 62.50 | 62.31 | 61.680 | 60.689 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:133 | P10000.cycle.kwhPerTonne | 69.76 | 69.44 | 67.909 | 75.082 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:134 | P100.cycle.eCycleMWh | 8.042 | 8.192 | 7.812 | 6.024 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:134 | P1000.cycle.eCycleMWh | 62.500 | 62.314 | 61.680 | 60.689 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:134 | P10000.cycle.eCycleMWh | 697.586 | 694.378 | 679.093 | 750.823 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:156 | P100.descent.rotorCapT | 141.4 | 140.5 | 140.542 | 140.542 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:156 | P1000.descent.rotorCapT | 687.6 | 683.3 | 683.286 | 683.286 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:156 | P10000.descent.rotorCapT | 7,124.3 | 7,079.2 | 7079.204 | 7079.204 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:172 | P10000.energy.letdownMWh | 117.284 | 117.219 | 102.086 | 101.388 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:260 | P100.energy.deficitPerCycleMWh | 7.89 | 8.04 | 7.694 | 5.906 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:261 | P1000.energy.deficitPerCycleMWh | 61.76 | 61.57 | 61.110 | 60.119 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:262 | P10000.energy.deficitPerCycleMWh | 693.49 | 690.28 | 675.698 | 747.428 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:284 | P10000.cycle.eCycleMWh | 697.586 | 694.378 | 679.093 | 750.823 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:354 | P100.energy.ledgerMWh.RETURN_TRANSIT | 4.212 | 4.409 | 4.407 | 3.061 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:355 | P100.energy.ledgerMWh.OUTBOUND_TRANSIT | 0.632 | 0.576 | 0.576 | 0.396 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:357 | P100.energy.ledgerMWh.WATER_FILL | 0.857 | 0.864 | 0.734 | 0.734 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:358 | P100.energy.letdownMWh | 2.296 | 2.305 | 2.052 | 1.192 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:361 | P100.cycle.eCycleMWh | 8.042 | 8.192 | 7.812 | 6.024 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:374 | P100.energy.deficitPerCycleMWh | 7.89 | 8.04 | 7.694 | 5.906 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:375 | P1000.energy.deficitPerCycleMWh | 61.76 | 61.57 | 61.110 | 60.119 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:376 | P10000.energy.deficitPerCycleMWh | 693.49 | 690.28 | 675.698 | 747.428 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:393 | P100.cycle.eCycleMWh | 8.042 | 8.192 | 7.812 | 6.024 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |
| research/reports/03-diligence.md:397 | P100.cycle.kwhPerTonne | 80.42 | 81.92 | 78.122 | 60.241 | Local density, paid bag inventory and smooth prescribed motion in the integrated force ledger. |  /  |

The [superseded document record](../research/analysis/energy-document-history.json) preserves the replaced energy text and its historical numbers. It is dated history, not a current model reading.

## What this model leaves out

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. Rotor energy and power figures are conditional on a constant hover merit times drive efficiency at every thrust and speed, with no separate blade profile power and no specified blade, rotor-speed or pitch policy. A separated model can move these figures in either direction.

Generated by `node research/analysis/energy-omissions.mjs`. These loads are not silently absorbed into a closing claim.

| Class | Beam-wind side force, t | Cable mass, t (floor / credible / demonstrated) | Battery mass, t (same cases) | Dry target, t | Bag, t | Cable, m | Pendulum period, s | Day-average solar, MW |
|---|---:|---|---|---:|---:|---:|---:|---:|
| P100 | 29.709 | 0.644 / 1.431 / 2.146 | 40.000 / 66.667 / 134.228 | 100 | 125 | 350 | 37.530 | 0.207 |
| P1000 | 139.077 | 11.036 / 24.525 / 36.788 | 240.000 / 400.000 / 805.369 | 1000 | 1250 | 600 | 49.138 | 0.967 |
| P10000 | 643.635 | 155.096 / 344.658 / 516.987 | 4000.000 / 6666.667 / 13422.819 | 10000 | 12400 | 850 | 58.486 | 4.476 |

| Class | Design displacement, m³ | Geometric capsule, m³ | Difference from design, % |
|---|---:|---:|---:|
| P100 | 220000.000 | 217784.366 | -1.007 |
| P1000 | 2200000.000 | 2205867.973 | 0.267 |
| P10000 | 22000000.000 | 21961324.389 | -0.176 |

Buoyancy uses the declared design displacement. The capsule comparison is a geometry difference, not a change to lift or the class constants.

The beam wind is 10 m/s, with an unverified side-drag coefficient of 1 and local source density. No horizontal actuator or station-keeping power is priced.

Cable and battery estimates bind to `research/analysis/mass-budget.json`. Cable mass is not added to the energy model's dry target.

Storage cases use 500, 300, 149 Wh/kg, respectively. Their source qualifications remain in the mass-budget record.

The bag is a moving pendulum; its ideal small-angle period is shown, but swing, damping and winch transients are unpriced. The steady hoist bill does not bound pickup shock.

Solar is credited at its day average at every instant, including night. Dry mass is a target equal to payload, not an assembled mass ledger; see [the float analysis](../float/).

## Signed vertical authority screen of the served candidates

Central second difference of altitude with progress step 0.0001, clamped inside each phase at its endpoints. Peak means largest absolute vertical acceleration; signed rotor demand is checked at every sampled instant.

Hull dry-mass target plus water and nitrogen aboard; added mass is coefficient times local displaced-air mass. The 0.70 and 1.00 coefficients are a sensitivity pair, not measured capsule values. Hull-only: hanging-bag, actuator and controller dynamics are excluded.

Upward acceleration is positive. I = (m_onboard + C * m_displaced_air) * a_z / g; T_required = T_quasi + unheld - I. Accept the sampled rotor demand only if 0 <= T_required <= T_available. Gap = max(0, -T_required, T_required - T_available). Aerodynamic force, bag support, drag and other electrical loads remain fixed. Buoyancy is already in the ledger; shedding hold-down is an upward increment, not new buoyancy.

Source: [Munk, The Aerodynamic Forces on Airship Hulls, NACA Report 184 (1924)](https://ntrs.nasa.gov/citations/19930091249), printed page 20, table; PDF page 21, Table I. This potential-flow spheroid surrogate is not a measurement of the capsule hull.

Dated measurement at landing 16, 2026-10-05: absolute inertial force minus the additional downward rotor reserve at the same samples and coefficients. Withdrawn because it misses upward authority that cannot be obtained by shedding the existing downward thrust. Recomputed here solely to preserve that measurement.

| Population | Cases | Quasi-static feasible | Signed gaps C=0.70 / C=1.00 / either | Withdrawn absolute gaps C=0.70 / C=1.00 / either | Signed only / absolute only |
|---|---|---|---|---|---|
| candidates | 476 | 303 | 303 / 303 / 303 | 205 / 205 / 205 | 98 / 0 |
| capturedMissions | 20 | 20 | 20 / 20 / 20 | 6 / 6 / 6 | 14 / 0 |

The 20 captures select the same ready controls. The signed screen flags 20; the other 0 are not validated by a hull-only sampled screen either. No quasi-static verdict changes.

| Case | Class / km / basis | C | Phase / progress | Acceleration m/s² | Signed demand tf | Required rotor tf | Thrust to shed tf | Additional downward reserve tf | Signed gap tf / direction | Withdrawn absolute gap tf | Storage note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| exercise / 0 (zero-based) | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| exercise / 0 (zero-based) | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| exercise / 1 (zero-based) | P1000 / 15.639184 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| exercise / 1 (zero-based) | P1000 / 15.639184 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| exercise / 2 (zero-based) | P1000 / 14.300045 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| exercise / 2 (zero-based) | P1000 / 14.300045 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| exercise / 3 (zero-based) | P1000 / 28.870139 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| exercise / 3 (zero-based) | P1000 / 28.870139 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| exercise / 4 (zero-based) | P1000 / 32.629354 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| exercise / 4 (zero-based) | P1000 / 32.629354 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| exercise / 5 (zero-based) | P1000 / 27.253677 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| exercise / 5 (zero-based) | P1000 / 27.253677 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| exercise / 6 (zero-based) | P100 / 19.302441 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.351 | -3.351 | 0.000 | 143.453 | 3.351 / upward authority short | 0.000 |  |
| exercise / 6 (zero-based) | P100 / 19.302441 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.153 | -4.153 | 0.000 | 143.453 | 4.153 / upward authority short | 0.000 |  |
| exercise / 7 (zero-based) | P100 / 20.054737 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.352 | -3.352 | 0.000 | 143.745 | 3.352 / upward authority short | 0.000 |  |
| exercise / 7 (zero-based) | P100 / 20.054737 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.154 | -4.154 | 0.000 | 143.745 | 4.154 / upward authority short | 0.000 |  |
| exercise / 8 (zero-based) | P100 / 5.730096 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.583 | 2.305 / upward authority short | 0.000 |  |
| exercise / 8 (zero-based) | P100 / 5.730096 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.583 | 2.849 / upward authority short | 0.000 |  |
| exercise / 9 (zero-based) | P100 / 7.331041 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.819 | 2.305 / upward authority short | 0.000 |  |
| exercise / 9 (zero-based) | P100 / 7.331041 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.819 | 2.849 / upward authority short | 0.000 |  |
| exercise / 10 (zero-based) | P100 / 13.980788 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.309 | -2.309 | 0.000 | 140.066 | 2.309 / upward authority short | 0.000 |  |
| exercise / 10 (zero-based) | P100 / 13.980788 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.066 | 2.854 / upward authority short | 0.000 |  |
| exercise / 11 (zero-based) | P100 / 9.775576 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.306 | -2.306 | 0.000 | 138.377 | 2.306 / upward authority short | 0.000 |  |
| exercise / 11 (zero-based) | P100 / 9.775576 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.850 | -2.850 | 0.000 | 138.377 | 2.850 / upward authority short | 0.000 |  |
| exercise / 12 (zero-based) | P100 / 5.541040 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.555 | 2.305 / upward authority short | 0.000 |  |
| exercise / 12 (zero-based) | P100 / 5.541040 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.555 | 2.849 / upward authority short | 0.000 |  |
| exercise / 13 (zero-based) | P100 / 9.470465 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.306 | -2.306 | 0.000 | 138.217 | 2.306 / upward authority short | 0.000 |  |
| exercise / 13 (zero-based) | P100 / 9.470465 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.850 | -2.850 | 0.000 | 138.217 | 2.850 / upward authority short | 0.000 |  |
| exercise / 14 (zero-based) | P100 / 5.200784 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.505 | 2.304 / upward authority short | 0.000 |  |
| exercise / 14 (zero-based) | P100 / 5.200784 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.505 | 2.849 / upward authority short | 0.000 |  |
| exercise / 15 (zero-based) | P100 / 4.938018 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.466 | 2.304 / upward authority short | 0.000 |  |
| exercise / 15 (zero-based) | P100 / 4.938018 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.466 | 2.849 / upward authority short | 0.000 |  |
| replay / 0 (zero-based) | P100 / 6.872958 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.752 | 2.305 / upward authority short | 0.000 |  |
| replay / 0 (zero-based) | P100 / 6.872958 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.752 | 2.849 / upward authority short | 0.000 |  |
| replay / 1 (zero-based) | P100 / 14.714511 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.381 | -3.381 | 0.000 | 141.667 | 3.381 / upward authority short | 0.000 |  |
| replay / 1 (zero-based) | P100 / 14.714511 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.183 | -4.183 | 0.000 | 141.667 | 4.183 / upward authority short | 0.000 |  |
| replay / 2 (zero-based) | P100 / 19.388471 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.351 | -3.351 | 0.000 | 143.486 | 3.351 / upward authority short | 0.000 |  |
| replay / 2 (zero-based) | P100 / 19.388471 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.153 | -4.153 | 0.000 | 143.486 | 4.153 / upward authority short | 0.000 |  |
| replay / 3 (zero-based) | P100 / 22.610555 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.355 | -3.355 | 0.000 | 144.734 | 3.355 / upward authority short | 0.000 |  |
| replay / 3 (zero-based) | P100 / 22.610555 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.158 | -4.158 | 0.000 | 144.734 | 4.158 / upward authority short | 0.000 |  |

Every candidate is replayed in still air at every printed or captured distance for its class, on both bases. Infeasible cases remain diagnostics. The JSON also records each phase and both simultaneous authorities at its largest signed gap.

| Case | Class / km / basis | C | Phase / progress | Acceleration m/s² | Signed demand tf | Required rotor tf | Thrust to shed tf | Additional downward reserve tf | Signed gap tf / direction | Withdrawn absolute gap tf | Storage note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| candidate 1 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.016122 | -0.477 | 118.815 | 109.850 | 0.000 | 8.965 / downward authority short | 9.067 |  |
| candidate 1 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.024183 | -0.884 | 118.997 | 109.892 | 0.000 | 9.105 / downward authority short | 11.300 |  |
| candidate 1 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 15.219 | -8.867 | 6.353 | 152.368 | 8.867 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 18.161 | -11.809 | 6.353 | 152.368 | 11.809 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.016122 | -0.477 | 118.815 | 109.850 | 0.000 | 8.965 / downward authority short | 9.067 |  |
| candidate 1 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.024183 | -0.884 | 118.997 | 109.892 | 0.000 | 9.105 / downward authority short | 11.300 |  |
| candidate 1 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 15.219 | -8.867 | 6.353 | 152.368 | 8.867 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 18.161 | -11.809 | 6.353 | 152.368 | 11.809 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 5.200784 / record | 0.70 | RETURN_TRANSIT / 0.793500 | -0.012434 | -0.367 | 118.953 | 109.312 | 0.000 | 9.641 / downward authority short | 9.028 |  |
| candidate 1 | P100 / 5.200784 / record | 1.00 | RETURN_TRANSIT / 0.791000 | -0.020205 | -0.738 | 119.097 | 109.343 | 0.000 | 9.754 / downward authority short | 11.180 |  |
| candidate 1 | P100 / 5.200784 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.389098 | 14.446 | -8.160 | 6.286 | 152.403 | 8.160 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 5.200784 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.389098 | 17.238 | -10.951 | 6.286 | 152.403 | 10.951 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 5.541040 / record | 0.70 | RETURN_TRANSIT / 0.794500 | -0.008905 | -0.263 | 119.078 | 108.695 | 0.000 | 10.384 / downward authority short | 8.619 |  |
| candidate 1 | P100 / 5.541040 / record | 1.00 | RETURN_TRANSIT / 0.792500 | -0.014842 | -0.542 | 119.175 | 108.709 | 0.000 | 10.466 / downward authority short | 10.673 |  |
| candidate 1 | P100 / 5.541040 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.365205 | 13.554 | -7.354 | 6.201 | 152.447 | 7.354 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 5.541040 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.365205 | 16.173 | -9.972 | 6.201 | 152.447 | 9.972 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 5.730096 / record | 0.70 | RETURN_TRANSIT / 0.795500 | -0.005791 | -0.171 | 119.124 | 108.384 | 0.000 | 10.740 / downward authority short | 8.406 |  |
| candidate 1 | P100 / 5.730096 / record | 1.00 | RETURN_TRANSIT / 0.793000 | -0.013029 | -0.475 | 119.201 | 108.394 | 0.000 | 10.807 / downward authority short | 10.408 |  |
| candidate 1 | P100 / 5.730096 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.353156 | 13.105 | -6.951 | 6.153 | 152.471 | 6.951 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 5.730096 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.353156 | 15.635 | -9.482 | 6.153 | 152.471 | 9.482 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 6.872958 / record | 0.70 | RETURN_TRANSIT / 0.798500 | 0.002515 | 0.074 | 119.116 | 106.883 | 0.000 | 12.233 / downward authority short | 7.294 |  |
| candidate 1 | P100 / 6.872958 / record | 1.00 | RETURN_TRANSIT / 0.796500 | -0.002515 | -0.091 | 119.095 | 106.861 | 0.000 | 12.234 / downward authority short | 9.028 |  |
| candidate 1 | P100 / 6.872958 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.294432 | 10.913 | -5.046 | 5.866 | 152.619 | 5.046 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 6.872958 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.294432 | 13.017 | -7.151 | 5.866 | 152.619 | 7.151 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 7.331041 / record | 0.70 | RETURN_TRANSIT / 0.799500 | 0.004775 | 0.140 | 119.004 | 106.415 | 0.000 | 12.590 / downward authority short | 6.922 |  |
| candidate 1 | P100 / 7.331041 / record | 1.00 | RETURN_TRANSIT / 0.798000 | 0.001194 | 0.043 | 118.960 | 106.390 | 0.000 | 12.571 / downward authority short | 8.566 |  |
| candidate 1 | P100 / 7.331041 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.276034 | 10.226 | -4.475 | 5.751 | 152.678 | 4.475 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 7.331041 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.276034 | 12.197 | -6.445 | 5.751 | 152.678 | 6.445 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 9.470465 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012488 | 0.366 | 116.942 | 105.633 | 0.000 | 11.310 / downward authority short | 5.442 |  |
| candidate 1 | P100 / 9.470465 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.009791 | 0.354 | 116.807 | 105.574 | 0.000 | 11.233 / downward authority short | 6.730 |  |
| candidate 1 | P100 / 9.470465 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.208000 | -0.012057 | -0.439 | -6.564 | 0.000 | 156.342 | 6.564 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 9.470465 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.206000 | -0.007673 | -0.332 | -6.497 | 0.000 | 156.408 | 6.497 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 9.775576 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012634 | 0.370 | 116.618 | 105.543 | 0.000 | 11.075 / downward authority short | 5.279 |  |
| candidate 1 | P100 / 9.775576 / record | 1.00 | RETURN_TRANSIT / 0.800500 | 0.010898 | 0.394 | 116.495 | 105.501 | 0.000 | 10.993 / downward authority short | 6.529 |  |
| candidate 1 | P100 / 9.775576 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.208500 | -0.012743 | -0.463 | -6.934 | 0.000 | 156.230 | 6.934 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 9.775576 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.207000 | -0.009557 | -0.413 | -6.857 | 0.000 | 156.280 | 6.857 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 13.980788 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.344 | -3.344 | 0.000 | 141.380 | 3.344 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 13.980788 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.147 | -4.147 | 0.000 | 141.380 | 4.147 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 13.980788 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.344 | -3.344 | 0.000 | 141.380 | 3.344 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 13.980788 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.147 | -4.147 | 0.000 | 141.380 | 4.147 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.140417 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.344 | -3.344 | 0.000 | 141.443 | 3.344 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.140417 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.147 | -4.147 | 0.000 | 141.443 | 4.147 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.140417 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.344 | -3.344 | 0.000 | 141.443 | 3.344 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.140417 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.147 | -4.147 | 0.000 | 141.443 | 4.147 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.714511 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.345 | -3.345 | 0.000 | 141.667 | 3.345 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.714511 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.147 | -4.147 | 0.000 | 141.667 | 4.147 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.714511 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.345 | -3.345 | 0.000 | 141.667 | 3.345 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 14.714511 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.147 | -4.147 | 0.000 | 141.667 | 4.147 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 15.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.345 | -3.345 | 0.000 | 141.778 | 3.345 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 15.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.148 | -4.148 | 0.000 | 141.778 | 4.148 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 15.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.345 | -3.345 | 0.000 | 141.778 | 3.345 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 15.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.148 | -4.148 | 0.000 | 141.778 | 4.148 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.302441 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.351 | -3.351 | 0.000 | 143.453 | 3.351 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.302441 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.153 | -4.153 | 0.000 | 143.453 | 4.153 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.302441 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.351 | -3.351 | 0.000 | 143.453 | 3.351 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.302441 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.153 | -4.153 | 0.000 | 143.453 | 4.153 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.388471 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.351 | -3.351 | 0.000 | 143.486 | 3.351 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.388471 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.153 | -4.153 | 0.000 | 143.486 | 4.153 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.388471 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.351 | -3.351 | 0.000 | 143.486 | 3.351 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 19.388471 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.153 | -4.153 | 0.000 | 143.486 | 4.153 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 20.054737 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.352 | -3.352 | 0.000 | 143.745 | 3.352 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 20.054737 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.154 | -4.154 | 0.000 | 143.745 | 4.154 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 20.054737 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.352 | -3.352 | 0.000 | 143.745 | 3.352 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 20.054737 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.154 | -4.154 | 0.000 | 143.745 | 4.154 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 22.610555 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.355 | -3.355 | 0.000 | 144.734 | 3.355 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 22.610555 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.158 | -4.158 | 0.000 | 144.734 | 4.158 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 22.610555 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.355 | -3.355 | 0.000 | 144.734 | 3.355 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 22.610555 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.158 | -4.158 | 0.000 | 144.734 | 4.158 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 47.389863 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.387 | -3.387 | 0.000 | 154.156 | 3.387 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 47.389863 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.189 | -4.189 | 0.000 | 154.156 | 4.189 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 47.389863 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.387 | -3.387 | 0.000 | 154.156 | 3.387 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 47.389863 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.189 | -4.189 | 0.000 | 154.156 | 4.189 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 60.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.403 | -3.403 | 0.000 | 158.842 | 3.403 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 60.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.206 | -4.206 | 0.000 | 158.842 | 4.206 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 60.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.403 | -3.403 | 0.000 | 158.842 | 3.403 / upward authority short | 0.000 |  |
| candidate 1 | P100 / 60.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.206 | -4.206 | 0.000 | 158.842 | 4.206 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.016122 | -0.478 | 117.869 | 109.850 | 0.000 | 8.018 / downward authority short | 8.149 |  |
| candidate 2 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.024183 | -0.887 | 118.051 | 109.892 | 0.000 | 8.159 / downward authority short | 10.383 |  |
| candidate 2 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 15.219 | -8.867 | 6.353 | 152.368 | 8.867 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 18.161 | -11.809 | 6.353 | 152.368 | 11.809 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.016122 | -0.478 | 117.869 | 109.850 | 0.000 | 8.018 / downward authority short | 8.149 |  |
| candidate 2 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.024183 | -0.887 | 118.051 | 109.892 | 0.000 | 8.159 / downward authority short | 10.383 |  |
| candidate 2 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 15.219 | -8.867 | 6.353 | 152.368 | 8.867 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 18.161 | -11.809 | 6.353 | 152.368 | 11.809 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 5.200784 / record | 0.70 | RETURN_TRANSIT / 0.793500 | -0.012434 | -0.369 | 118.006 | 109.312 | 0.000 | 8.695 / downward authority short | 8.472 |  |
| candidate 2 | P100 / 5.200784 / record | 1.00 | RETURN_TRANSIT / 0.791000 | -0.020205 | -0.740 | 118.151 | 109.343 | 0.000 | 8.808 / downward authority short | 10.624 |  |
| candidate 2 | P100 / 5.200784 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.389098 | 14.446 | -8.160 | 6.286 | 152.403 | 8.160 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 5.200784 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.389098 | 17.238 | -10.951 | 6.286 | 152.403 | 10.951 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 5.541040 / record | 0.70 | RETURN_TRANSIT / 0.794500 | -0.008905 | -0.264 | 118.131 | 108.695 | 0.000 | 9.437 / downward authority short | 8.647 |  |
| candidate 2 | P100 / 5.541040 / record | 1.00 | RETURN_TRANSIT / 0.792500 | -0.014842 | -0.543 | 118.228 | 108.709 | 0.000 | 9.519 / downward authority short | 10.701 |  |
| candidate 2 | P100 / 5.541040 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.365205 | 13.554 | -7.354 | 6.201 | 152.447 | 7.354 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 5.541040 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.365205 | 16.173 | -9.972 | 6.201 | 152.447 | 9.972 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 5.730096 / record | 0.70 | RETURN_TRANSIT / 0.795500 | -0.005791 | -0.172 | 118.176 | 108.384 | 0.000 | 9.792 / downward authority short | 8.433 |  |
| candidate 2 | P100 / 5.730096 / record | 1.00 | RETURN_TRANSIT / 0.793000 | -0.013029 | -0.477 | 118.254 | 108.394 | 0.000 | 9.861 / downward authority short | 10.435 |  |
| candidate 2 | P100 / 5.730096 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.353156 | 13.105 | -6.951 | 6.153 | 152.471 | 6.951 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 5.730096 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.353156 | 15.635 | -9.482 | 6.153 | 152.471 | 9.482 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 6.872958 / record | 0.70 | RETURN_TRANSIT / 0.798500 | 0.002515 | 0.074 | 118.168 | 106.883 | 0.000 | 11.285 / downward authority short | 7.318 |  |
| candidate 2 | P100 / 6.872958 / record | 1.00 | RETURN_TRANSIT / 0.796500 | -0.002515 | -0.092 | 118.147 | 106.861 | 0.000 | 11.286 / downward authority short | 9.052 |  |
| candidate 2 | P100 / 6.872958 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.294432 | 10.913 | -5.046 | 5.866 | 152.619 | 5.046 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 6.872958 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.294432 | 13.017 | -7.151 | 5.866 | 152.619 | 7.151 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 7.331041 / record | 0.70 | RETURN_TRANSIT / 0.799500 | 0.004775 | 0.141 | 118.056 | 106.415 | 0.000 | 11.641 / downward authority short | 6.944 |  |
| candidate 2 | P100 / 7.331041 / record | 1.00 | RETURN_TRANSIT / 0.798000 | 0.001194 | 0.043 | 118.012 | 106.390 | 0.000 | 11.622 / downward authority short | 8.589 |  |
| candidate 2 | P100 / 7.331041 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.276034 | 10.226 | -4.475 | 5.751 | 152.678 | 4.475 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 7.331041 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.276034 | 12.197 | -6.445 | 5.751 | 152.678 | 6.445 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 9.470465 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012488 | 0.367 | 115.993 | 105.633 | 0.000 | 10.360 / downward authority short | 5.459 |  |
| candidate 2 | P100 / 9.470465 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.009791 | 0.355 | 115.858 | 105.574 | 0.000 | 10.284 / downward authority short | 6.748 |  |
| candidate 2 | P100 / 9.470465 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.208000 | -0.012057 | -0.439 | -6.564 | 0.000 | 156.342 | 6.564 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 9.470465 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.206000 | -0.007673 | -0.332 | -6.497 | 0.000 | 156.408 | 6.497 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 9.775576 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012634 | 0.371 | 115.669 | 105.543 | 0.000 | 10.126 / downward authority short | 5.296 |  |
| candidate 2 | P100 / 9.775576 / record | 1.00 | RETURN_TRANSIT / 0.800500 | 0.010898 | 0.395 | 115.546 | 105.501 | 0.000 | 10.044 / downward authority short | 6.546 |  |
| candidate 2 | P100 / 9.775576 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.208500 | -0.012743 | -0.463 | -6.934 | 0.000 | 156.230 | 6.934 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 9.775576 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.207000 | -0.009557 | -0.413 | -6.857 | 0.000 | 156.280 | 6.857 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 13.980788 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.355 | -3.355 | 0.000 | 141.380 | 3.355 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 13.980788 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.157 | -4.157 | 0.000 | 141.380 | 4.157 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 13.980788 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.355 | -3.355 | 0.000 | 141.380 | 3.355 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 13.980788 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.157 | -4.157 | 0.000 | 141.380 | 4.157 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.140417 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.355 | -3.355 | 0.000 | 141.443 | 3.355 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.140417 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.157 | -4.157 | 0.000 | 141.443 | 4.157 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.140417 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.355 | -3.355 | 0.000 | 141.443 | 3.355 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.140417 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.157 | -4.157 | 0.000 | 141.443 | 4.157 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.714511 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.356 | -3.356 | 0.000 | 141.667 | 3.356 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.714511 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.158 | -4.158 | 0.000 | 141.667 | 4.158 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.714511 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.356 | -3.356 | 0.000 | 141.667 | 3.356 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 14.714511 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.158 | -4.158 | 0.000 | 141.667 | 4.158 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 15.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.356 | -3.356 | 0.000 | 141.778 | 3.356 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 15.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.159 | -4.159 | 0.000 | 141.778 | 4.159 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 15.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.356 | -3.356 | 0.000 | 141.778 | 3.356 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 15.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.159 | -4.159 | 0.000 | 141.778 | 4.159 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.302441 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.362 | -3.362 | 0.000 | 143.453 | 3.362 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.302441 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.164 | -4.164 | 0.000 | 143.453 | 4.164 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.302441 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.362 | -3.362 | 0.000 | 143.453 | 3.362 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.302441 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.164 | -4.164 | 0.000 | 143.453 | 4.164 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.388471 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.362 | -3.362 | 0.000 | 143.486 | 3.362 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.388471 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.164 | -4.164 | 0.000 | 143.486 | 4.164 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.388471 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.362 | -3.362 | 0.000 | 143.486 | 3.362 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 19.388471 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.164 | -4.164 | 0.000 | 143.486 | 4.164 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 20.054737 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.363 | -3.363 | 0.000 | 143.745 | 3.363 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 20.054737 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.165 | -4.165 | 0.000 | 143.745 | 4.165 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 20.054737 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.363 | -3.363 | 0.000 | 143.745 | 3.363 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 20.054737 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.165 | -4.165 | 0.000 | 143.745 | 4.165 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 22.610555 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.366 | -3.366 | 0.000 | 144.734 | 3.366 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 22.610555 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.168 | -4.168 | 0.000 | 144.734 | 4.168 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 22.610555 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.366 | -3.366 | 0.000 | 144.734 | 3.366 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 22.610555 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.168 | -4.168 | 0.000 | 144.734 | 4.168 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 47.389863 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.398 | -3.398 | 0.000 | 154.156 | 3.398 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 47.389863 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.200 | -4.200 | 0.000 | 154.156 | 4.200 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 47.389863 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.398 | -3.398 | 0.000 | 154.156 | 3.398 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 47.389863 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.200 | -4.200 | 0.000 | 154.156 | 4.200 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 60.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.414 | -3.414 | 0.000 | 158.842 | 3.414 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 60.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.216 | -4.216 | 0.000 | 158.842 | 4.216 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 60.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.414 | -3.414 | 0.000 | 158.842 | 3.414 / upward authority short | 0.000 |  |
| candidate 2 | P100 / 60.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.216 | -4.216 | 0.000 | 158.842 | 4.216 / upward authority short | 0.000 |  |
| candidate 3 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.191000 | -0.125406 | -3.463 | 144.944 | 108.292 | 0.000 | 36.652 / downward authority short | 22.416 |  |
| candidate 3 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.149500 | -0.813923 | -28.085 | 160.743 | 118.534 | 0.000 | 42.209 / downward authority short | 28.085 |  |
| candidate 3 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 35.106 | -28.053 | 7.053 | 152.009 | 28.053 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 41.916 | -34.863 | 7.053 | 152.009 | 34.863 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.191000 | -0.125406 | -3.463 | 144.944 | 108.292 | 0.000 | 36.652 / downward authority short | 22.416 |  |
| candidate 3 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.149500 | -0.813923 | -28.085 | 160.743 | 118.534 | 0.000 | 42.209 / downward authority short | 28.085 |  |
| candidate 3 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 35.106 | -28.053 | 7.053 | 152.009 | 28.053 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 41.916 | -34.863 | 7.053 | 152.009 | 34.863 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 5.200784 / record | 0.70 | RETURN_TRANSIT / 0.149500 | -0.717025 | -19.747 | 150.729 | 121.299 | 0.000 | 29.429 / downward authority short | 19.747 |  |
| candidate 3 | P100 / 5.200784 / record | 1.00 | RETURN_TRANSIT / 0.149500 | -0.717025 | -24.742 | 155.723 | 121.299 | 0.000 | 34.424 / downward authority short | 24.742 |  |
| candidate 3 | P100 / 5.200784 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.894926 | 33.329 | -26.304 | 7.024 | 152.024 | 26.304 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 5.200784 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.894926 | 39.793 | -32.769 | 7.024 | 152.024 | 32.769 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 5.541040 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 31.277 | -17.651 | 13.626 | 145.404 | 17.651 / upward authority short | 15.097 |  |
| candidate 3 | P100 / 5.541040 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 37.342 | -23.716 | 13.626 | 145.404 | 23.716 / upward authority short | 19.136 |  |
| candidate 3 | P100 / 5.541040 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 31.277 | -24.290 | 6.987 | 152.043 | 24.290 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 5.541040 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 37.342 | -30.356 | 6.987 | 152.043 | 30.356 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 5.730096 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 30.243 | -16.657 | 13.586 | 145.434 | 16.657 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 5.730096 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 36.107 | -22.521 | 13.586 | 145.434 | 22.521 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 5.730096 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 30.243 | -23.277 | 6.966 | 152.054 | 23.277 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 5.730096 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 36.107 | -29.141 | 6.966 | 152.054 | 29.141 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 6.872958 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 25.201 | -11.860 | 13.341 | 145.618 | 11.860 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 6.872958 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 30.084 | -16.743 | 13.341 | 145.618 | 16.743 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 6.872958 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 25.201 | -18.360 | 6.841 | 152.119 | 18.360 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 6.872958 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 30.084 | -23.244 | 6.841 | 152.119 | 23.244 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 7.331041 / record | 0.70 | RETURN_TRANSIT / 0.788500 | -0.037452 | -1.042 | 134.688 | 123.188 | 0.000 | 11.500 / downward authority short | 10.768 |  |
| candidate 3 | P100 / 7.331041 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 7.331041 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.634878 | 23.621 | -16.831 | 6.790 | 152.145 | 16.831 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 7.331041 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.634878 | 28.197 | -21.407 | 6.790 | 152.145 | 21.407 / upward authority short | 15.398 |  |
| candidate 3 | P100 / 9.470465 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.018163 | -0.504 | 136.523 | 117.108 | 0.000 | 19.414 / downward authority short | 9.889 |  |
| candidate 3 | P100 / 9.470465 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.027245 | -0.948 | 136.782 | 117.204 | 0.000 | 19.578 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 9.470465 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.332938 | 12.310 | -12.310 | 0.000 | 134.711 | 12.310 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 9.470465 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 9.775576 / record | 0.70 | RETURN_TRANSIT / 0.793000 | -0.016028 | -0.445 | 136.700 | 116.486 | 0.000 | 20.214 / downward authority short | 9.695 |  |
| candidate 3 | P100 / 9.775576 / record | 1.00 | RETURN_TRANSIT / 0.790500 | -0.024933 | -0.867 | 136.937 | 116.575 | 0.000 | 20.362 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 9.775576 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.327339 | 12.101 | -12.101 | 0.000 | 133.980 | 12.101 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 9.775576 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 13.980788 / record | 0.70 | RETURN_TRANSIT / 0.798000 | 0.001384 | 0.038 | 137.867 | 110.984 | 0.000 | 26.882 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 13.980788 / record | 1.00 | RETURN_TRANSIT / 0.796000 | -0.004153 | -0.144 | 137.882 | 110.991 | 0.000 | 26.891 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 13.980788 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.260170 | 9.600 | -9.600 | 0.000 | 127.390 | 9.600 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 13.980788 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 14.140417 / record | 0.70 | RETURN_TRANSIT / 0.798000 | 0.001372 | 0.038 | 137.876 | 110.847 | 0.000 | 27.029 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 14.140417 / record | 1.00 | RETURN_TRANSIT / 0.796500 | -0.002745 | -0.095 | 137.884 | 110.850 | 0.000 | 27.034 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 14.140417 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.258045 | 9.521 | -9.520 | 0.000 | 127.224 | 9.520 / upward authority short | 9.284 |  |
| candidate 3 | P100 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 14.714511 / record | 0.70 | RETURN_TRANSIT / 0.798500 | 0.002661 | 0.073 | 137.896 | 110.384 | 0.000 | 27.512 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 14.714511 / record | 1.00 | RETURN_TRANSIT / 0.797000 | -0.001331 | -0.046 | 137.888 | 110.381 | 0.000 | 27.506 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 14.714511 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 14.714511 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 15.000000 / record | 0.70 | RETURN_TRANSIT / 0.799000 | 0.003932 | 0.108 | 137.899 | 110.170 | 0.000 | 27.729 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 15.000000 / record | 1.00 | RETURN_TRANSIT / 0.797500 | 0.000000 | 0.000 | 137.881 | 110.163 | 0.000 | 27.718 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 19.302441 / record | 0.70 | RETURN_TRANSIT / 0.801000 | 0.010439 | 0.287 | 136.888 | 108.447 | 0.000 | 28.441 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 19.302441 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.008382 | 0.288 | 136.795 | 108.419 | 0.000 | 28.376 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 19.302441 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 19.302441 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 19.388471 / record | 0.70 | RETURN_TRANSIT / 0.801000 | 0.010497 | 0.288 | 136.852 | 108.434 | 0.000 | 28.418 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 19.388471 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.008450 | 0.290 | 136.758 | 108.405 | 0.000 | 28.353 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 19.388471 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 19.388471 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 20.054737 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.011880 | 0.326 | 136.590 | 108.352 | 0.000 | 28.238 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 20.054737 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.008923 | 0.306 | 136.471 | 108.303 | 0.000 | 28.167 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 20.054737 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 20.054737 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 22.610555 / record | 0.70 | RETURN_TRANSIT / 0.802000 | 0.013519 | 0.370 | 135.514 | 108.063 | 0.000 | 27.451 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 22.610555 / record | 1.00 | RETURN_TRANSIT / 0.801000 | 0.011793 | 0.403 | 135.382 | 108.019 | 0.000 | 27.364 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 22.610555 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 22.610555 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 3 | P100 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865635 | -24.032 | 144.264 | 120.232 | 14.748 | 9.284 / downward authority short | 9.284 |  |
| candidate 3 | P100 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865635 | -30.145 | 150.377 | 120.232 | 14.748 | 15.398 / downward authority short | 15.398 |  |
| candidate 4 | P100 / 4.938018 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -15.698 | 13.544 | 145.466 | 15.698 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 4.938018 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -21.368 | 13.544 | 145.466 | 21.368 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -22.297 | 6.945 | 152.065 | 22.297 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -27.967 | 6.945 | 152.065 | 27.967 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 4.938018 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -15.698 | 13.544 | 145.466 | 15.698 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 4.938018 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -21.368 | 13.544 | 145.466 | 21.368 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -22.297 | 6.945 | 152.065 | 22.297 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -27.967 | 6.945 | 152.065 | 27.967 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 5.200784 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 27.761 | -14.284 | 13.476 | 145.517 | 14.284 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 5.200784 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 33.142 | -19.666 | 13.476 | 145.517 | 19.666 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 5.200784 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 27.761 | -20.851 | 6.910 | 152.083 | 20.851 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 5.200784 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 33.142 | -26.232 | 6.910 | 152.083 | 26.232 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 5.541040 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 26.051 | -12.662 | 13.389 | 145.582 | 12.662 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 5.541040 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 31.100 | -17.711 | 13.389 | 145.582 | 17.711 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 5.541040 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 26.051 | -19.186 | 6.865 | 152.106 | 19.186 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 5.541040 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 31.100 | -24.235 | 6.865 | 152.106 | 24.235 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 5.730096 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.676882 | 25.189 | -11.849 | 13.340 | 145.619 | 11.849 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 5.730096 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 5.730096 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.676882 | 25.189 | -18.349 | 6.840 | 152.119 | 18.349 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 5.730096 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.676882 | 30.070 | -23.230 | 6.840 | 152.119 | 23.230 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 6.872958 / record | 0.70 | RETURN_TRANSIT / 0.789500 | -0.031450 | -0.869 | 137.273 | 126.058 | 0.000 | 11.215 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 6.872958 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 6.872958 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.564327 | 20.988 | -14.298 | 6.690 | 152.196 | 14.298 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 6.872958 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.564327 | 25.051 | -18.361 | 6.690 | 152.196 | 18.361 / upward authority short | 16.879 |  |
| candidate 4 | P100 / 7.331041 / record | 0.70 | RETURN_TRANSIT / 0.790500 | -0.026561 | -0.733 | 137.718 | 124.677 | 0.000 | 13.041 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 7.331041 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 7.331041 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.529065 | 19.671 | -13.041 | 6.630 | 152.227 | 13.041 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 7.331041 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 9.470465 / record | 0.70 | RETURN_TRANSIT / 0.794500 | -0.009669 | -0.266 | 139.022 | 120.143 | 0.000 | 18.879 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 9.470465 / record | 1.00 | RETURN_TRANSIT / 0.792500 | -0.016115 | -0.556 | 139.152 | 120.180 | 0.000 | 18.972 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 9.470465 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.299464 | 11.062 | -11.062 | 0.000 | 134.700 | 11.062 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 9.470465 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 9.775576 / record | 0.70 | RETURN_TRANSIT / 0.795000 | -0.007880 | -0.217 | 139.130 | 119.673 | 0.000 | 19.457 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 9.775576 / record | 1.00 | RETURN_TRANSIT / 0.793000 | -0.014184 | -0.489 | 139.240 | 119.704 | 0.000 | 19.536 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 9.775576 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.293446 | 10.838 | -10.838 | 0.000 | 134.158 | 10.838 / upward authority short | 10.766 |  |
| candidate 4 | P100 / 9.775576 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 13.980788 / record | 0.70 | RETURN_TRANSIT / 0.800000 | 0.005993 | 0.164 | 139.427 | 115.433 | 0.000 | 23.993 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 13.980788 / record | 1.00 | RETURN_TRANSIT / 0.798500 | 0.002397 | 0.082 | 139.371 | 115.407 | 0.000 | 23.964 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 13.980788 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 13.980788 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 14.140417 / record | 0.70 | RETURN_TRANSIT / 0.800000 | 0.005938 | 0.162 | 139.404 | 115.322 | 0.000 | 24.081 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 14.140417 / record | 1.00 | RETURN_TRANSIT / 0.798500 | 0.002375 | 0.081 | 139.346 | 115.296 | 0.000 | 24.049 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 14.714511 / record | 0.70 | RETURN_TRANSIT / 0.800500 | 0.007840 | 0.214 | 139.173 | 115.138 | 0.000 | 24.035 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 14.714511 / record | 1.00 | RETURN_TRANSIT / 0.799000 | 0.004428 | 0.152 | 139.098 | 115.103 | 0.000 | 23.995 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 14.714511 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 14.714511 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 15.000000 / record | 0.70 | RETURN_TRANSIT / 0.800500 | 0.008233 | 0.225 | 139.035 | 115.064 | 0.000 | 23.971 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 15.000000 / record | 1.00 | RETURN_TRANSIT / 0.799000 | 0.004894 | 0.167 | 138.954 | 115.027 | 0.000 | 23.927 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 19.302441 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012734 | 0.346 | 136.873 | 114.266 | 0.000 | 22.607 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 19.302441 / record | 1.00 | RETURN_TRANSIT / 0.800500 | 0.011053 | 0.376 | 136.740 | 114.216 | 0.000 | 22.524 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 19.302441 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 19.302441 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 19.388471 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012746 | 0.346 | 136.827 | 114.253 | 0.000 | 22.575 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 19.388471 / record | 1.00 | RETURN_TRANSIT / 0.800500 | 0.011073 | 0.376 | 136.694 | 114.203 | 0.000 | 22.491 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 19.388471 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 19.388471 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 20.054737 / record | 0.70 | RETURN_TRANSIT / 0.802000 | 0.013619 | 0.370 | 136.500 | 114.183 | 0.000 | 22.316 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 20.054737 / record | 1.00 | RETURN_TRANSIT / 0.801000 | 0.012007 | 0.408 | 136.357 | 114.128 | 0.000 | 22.229 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 20.054737 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 20.054737 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 22.610555 / record | 0.70 | RETURN_TRANSIT / 0.807000 | 0.013427 | 0.365 | 133.224 | 117.727 | 0.000 | 15.496 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 22.610555 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 22.610555 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 22.610555 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 4 | P100 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865616 | -23.888 | 145.746 | 121.858 | 13.122 | 10.766 / downward authority short | 10.766 |  |
| candidate 4 | P100 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865616 | -30.001 | 151.859 | 121.858 | 13.122 | 16.879 / downward authority short | 16.879 |  |
| candidate 5 | P100 / 4.938018 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.466 | 2.304 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 4.938018 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.466 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 4.938018 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.466 | 2.304 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 4.938018 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.466 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 4.938018 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.466 | 2.304 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 4.938018 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.466 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 4.938018 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.466 | 2.304 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 4.938018 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.466 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.200784 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.505 | 2.304 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.200784 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.505 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.200784 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.304 | -2.304 | 0.000 | 137.505 | 2.304 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.200784 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.505 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.541040 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.555 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.541040 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.555 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.541040 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.555 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.541040 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.555 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.730096 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.583 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.730096 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.583 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.730096 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.583 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 5.730096 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.583 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 6.872958 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.752 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 6.872958 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.752 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 6.872958 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.752 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 6.872958 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.752 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 7.331041 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.819 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 7.331041 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.819 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 7.331041 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.305 | -2.305 | 0.000 | 137.819 | 2.305 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 7.331041 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.849 | -2.849 | 0.000 | 137.819 | 2.849 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.470465 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.306 | -2.306 | 0.000 | 138.217 | 2.306 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.470465 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.850 | -2.850 | 0.000 | 138.217 | 2.850 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.470465 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.306 | -2.306 | 0.000 | 138.217 | 2.306 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.470465 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.850 | -2.850 | 0.000 | 138.217 | 2.850 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.775576 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.306 | -2.306 | 0.000 | 138.377 | 2.306 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.775576 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.850 | -2.850 | 0.000 | 138.377 | 2.850 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.775576 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.306 | -2.306 | 0.000 | 138.377 | 2.306 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 9.775576 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.850 | -2.850 | 0.000 | 138.377 | 2.850 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 13.980788 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.309 | -2.309 | 0.000 | 140.066 | 2.309 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 13.980788 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.066 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 13.980788 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.309 | -2.309 | 0.000 | 140.066 | 2.309 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 13.980788 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.066 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.140417 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.309 | -2.309 | 0.000 | 140.133 | 2.309 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.140417 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.133 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.140417 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.309 | -2.309 | 0.000 | 140.133 | 2.309 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.140417 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.133 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.714511 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.310 | -2.310 | 0.000 | 140.352 | 2.310 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.714511 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.352 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.714511 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.310 | -2.310 | 0.000 | 140.352 | 2.310 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 14.714511 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.352 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 15.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.310 | -2.310 | 0.000 | 140.439 | 2.310 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 15.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.439 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 15.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.310 | -2.310 | 0.000 | 140.439 | 2.310 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 15.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.854 | -2.854 | 0.000 | 140.439 | 2.854 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.302441 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.312 | -2.312 | 0.000 | 141.743 | 2.312 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.302441 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.857 | -2.857 | 0.000 | 141.743 | 2.857 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.302441 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.312 | -2.312 | 0.000 | 141.743 | 2.312 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.302441 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.857 | -2.857 | 0.000 | 141.743 | 2.857 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.388471 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.313 | -2.313 | 0.000 | 141.769 | 2.313 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.388471 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.857 | -2.857 | 0.000 | 141.769 | 2.857 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.388471 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.313 | -2.313 | 0.000 | 141.769 | 2.313 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 19.388471 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.857 | -2.857 | 0.000 | 141.769 | 2.857 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 20.054737 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.313 | -2.313 | 0.000 | 141.970 | 2.313 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 20.054737 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.857 | -2.857 | 0.000 | 141.970 | 2.857 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 20.054737 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.313 | -2.313 | 0.000 | 141.970 | 2.313 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 20.054737 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.857 | -2.857 | 0.000 | 141.970 | 2.857 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 22.610555 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.314 | -2.314 | 0.000 | 142.741 | 2.314 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 22.610555 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.859 | -2.859 | 0.000 | 142.741 | 2.859 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 22.610555 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.314 | -2.314 | 0.000 | 142.741 | 2.314 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 22.610555 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.859 | -2.859 | 0.000 | 142.741 | 2.859 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 47.389863 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.322 | -2.322 | 0.000 | 146.818 | 2.322 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 47.389863 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.866 | -2.866 | 0.000 | 146.818 | 2.866 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 47.389863 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.322 | -2.322 | 0.000 | 146.818 | 2.322 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 47.389863 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.866 | -2.866 | 0.000 | 146.818 | 2.866 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 60.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.326 | -2.326 | 0.000 | 148.721 | 2.326 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 60.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.870 | -2.870 | 0.000 | 148.721 | 2.870 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 60.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.326 | -2.326 | 0.000 | 148.721 | 2.326 / upward authority short | 0.000 |  |
| candidate 5 | P100 / 60.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.074956 | 2.870 | -2.870 | 0.000 | 148.721 | 2.870 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.016122 | -0.482 | 115.640 | 109.850 | 0.000 | 5.790 / downward authority short | 5.989 |  |
| candidate 6 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.024183 | -0.892 | 115.825 | 109.892 | 0.000 | 5.933 / downward authority short | 8.222 |  |
| candidate 6 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 15.219 | -8.867 | 6.353 | 152.368 | 8.867 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 18.161 | -11.809 | 6.353 | 152.368 | 11.809 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.016122 | -0.482 | 115.640 | 109.850 | 0.000 | 5.790 / downward authority short | 5.989 |  |
| candidate 6 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.024183 | -0.892 | 115.825 | 109.892 | 0.000 | 5.933 / downward authority short | 8.222 |  |
| candidate 6 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 15.219 | -8.867 | 6.353 | 152.368 | 8.867 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.409803 | 18.161 | -11.809 | 6.353 | 152.368 | 11.809 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 5.200784 / record | 0.70 | RETURN_TRANSIT / 0.793500 | -0.012434 | -0.372 | 115.777 | 109.312 | 0.000 | 6.465 / downward authority short | 6.309 |  |
| candidate 6 | P100 / 5.200784 / record | 1.00 | RETURN_TRANSIT / 0.791000 | -0.020205 | -0.745 | 115.924 | 109.343 | 0.000 | 6.581 / downward authority short | 8.461 |  |
| candidate 6 | P100 / 5.200784 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.389098 | 14.446 | -8.160 | 6.286 | 152.403 | 8.160 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 5.200784 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.389098 | 17.238 | -10.951 | 6.286 | 152.403 | 10.951 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 5.541040 / record | 0.70 | RETURN_TRANSIT / 0.794500 | -0.008905 | -0.266 | 115.901 | 108.695 | 0.000 | 7.207 / downward authority short | 6.642 |  |
| candidate 6 | P100 / 5.541040 / record | 1.00 | RETURN_TRANSIT / 0.792500 | -0.014842 | -0.547 | 116.000 | 108.709 | 0.000 | 7.291 / downward authority short | 8.695 |  |
| candidate 6 | P100 / 5.541040 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.365205 | 13.554 | -7.354 | 6.201 | 152.447 | 7.354 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 5.541040 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.365205 | 16.173 | -9.972 | 6.201 | 152.447 | 9.972 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 5.730096 / record | 0.70 | RETURN_TRANSIT / 0.795000 | -0.007238 | -0.216 | 115.946 | 108.384 | 0.000 | 7.562 / downward authority short | 6.792 |  |
| candidate 6 | P100 / 5.730096 / record | 1.00 | RETURN_TRANSIT / 0.793000 | -0.013029 | -0.480 | 116.025 | 108.394 | 0.000 | 7.631 / downward authority short | 8.794 |  |
| candidate 6 | P100 / 5.730096 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.353156 | 13.105 | -6.951 | 6.153 | 152.471 | 6.951 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 5.730096 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.353156 | 15.635 | -9.482 | 6.153 | 152.471 | 9.482 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 6.872958 / record | 0.70 | RETURN_TRANSIT / 0.798500 | 0.002515 | 0.075 | 115.936 | 106.883 | 0.000 | 9.053 / downward authority short | 7.333 |  |
| candidate 6 | P100 / 6.872958 / record | 1.00 | RETURN_TRANSIT / 0.796500 | -0.002515 | -0.092 | 115.916 | 106.861 | 0.000 | 9.054 / downward authority short | 9.067 |  |
| candidate 6 | P100 / 6.872958 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.294432 | 10.913 | -5.046 | 5.866 | 152.619 | 5.046 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 6.872958 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.294432 | 13.017 | -7.151 | 5.866 | 152.619 | 7.151 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 7.331041 / record | 0.70 | RETURN_TRANSIT / 0.799500 | 0.004775 | 0.142 | 115.823 | 106.415 | 0.000 | 9.408 / downward authority short | 6.997 |  |
| candidate 6 | P100 / 7.331041 / record | 1.00 | RETURN_TRANSIT / 0.797500 | 0.000000 | 0.000 | 115.774 | 106.383 | 0.000 | 9.390 / downward authority short | 8.642 |  |
| candidate 6 | P100 / 7.331041 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.276034 | 10.226 | -4.475 | 5.751 | 152.678 | 4.475 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 7.331041 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.276034 | 12.197 | -6.445 | 5.751 | 152.678 | 6.445 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 9.470465 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012488 | 0.370 | 113.758 | 105.633 | 0.000 | 8.126 / downward authority short | 5.024 |  |
| candidate 6 | P100 / 9.470465 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.009791 | 0.357 | 113.624 | 105.574 | 0.000 | 8.050 / downward authority short | 6.313 |  |
| candidate 6 | P100 / 9.470465 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.208000 | -0.012057 | -0.439 | -6.564 | 0.000 | 156.342 | 6.564 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 9.470465 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.206000 | -0.007673 | -0.332 | -6.497 | 0.000 | 156.408 | 6.497 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 9.775576 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012634 | 0.374 | 113.434 | 105.543 | 0.000 | 7.891 / downward authority short | 4.705 |  |
| candidate 6 | P100 / 9.775576 / record | 1.00 | RETURN_TRANSIT / 0.800500 | 0.010898 | 0.397 | 113.311 | 105.501 | 0.000 | 7.810 / downward authority short | 5.955 |  |
| candidate 6 | P100 / 9.775576 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.208500 | -0.012743 | -0.463 | -6.934 | 0.000 | 156.230 | 6.934 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 9.775576 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.207000 | -0.009557 | -0.413 | -6.857 | 0.000 | 156.280 | 6.857 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 13.980788 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.380 | -3.380 | 0.000 | 141.380 | 3.380 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 13.980788 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.182 | -4.182 | 0.000 | 141.380 | 4.182 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 13.980788 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.380 | -3.380 | 0.000 | 141.380 | 3.380 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 13.980788 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.182 | -4.182 | 0.000 | 141.380 | 4.182 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.140417 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.380 | -3.380 | 0.000 | 141.443 | 3.380 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.140417 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.183 | -4.183 | 0.000 | 141.443 | 4.183 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.140417 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.380 | -3.380 | 0.000 | 141.443 | 3.380 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.140417 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.183 | -4.183 | 0.000 | 141.443 | 4.183 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.714511 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.381 | -3.381 | 0.000 | 141.667 | 3.381 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.714511 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.183 | -4.183 | 0.000 | 141.667 | 4.183 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.714511 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.381 | -3.381 | 0.000 | 141.667 | 3.381 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 14.714511 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.183 | -4.183 | 0.000 | 141.667 | 4.183 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 15.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.381 | -3.381 | 0.000 | 141.778 | 3.381 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 15.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.184 | -4.184 | 0.000 | 141.778 | 4.184 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 15.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.381 | -3.381 | 0.000 | 141.778 | 3.381 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 15.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.184 | -4.184 | 0.000 | 141.778 | 4.184 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.302441 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.387 | -3.387 | 0.000 | 143.453 | 3.387 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.302441 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.189 | -4.189 | 0.000 | 143.453 | 4.189 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.302441 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.387 | -3.387 | 0.000 | 143.453 | 3.387 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.302441 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.189 | -4.189 | 0.000 | 143.453 | 4.189 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.388471 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.387 | -3.387 | 0.000 | 143.486 | 3.387 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.388471 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.189 | -4.189 | 0.000 | 143.486 | 4.189 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.388471 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.387 | -3.387 | 0.000 | 143.486 | 3.387 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 19.388471 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.189 | -4.189 | 0.000 | 143.486 | 4.189 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 20.054737 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.388 | -3.388 | 0.000 | 143.745 | 3.388 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 20.054737 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.190 | -4.190 | 0.000 | 143.745 | 4.190 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 20.054737 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.388 | -3.388 | 0.000 | 143.745 | 3.388 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 20.054737 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.190 | -4.190 | 0.000 | 143.745 | 4.190 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 22.610555 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.391 | -3.391 | 0.000 | 144.734 | 3.391 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 22.610555 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.193 | -4.193 | 0.000 | 144.734 | 4.193 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 22.610555 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.391 | -3.391 | 0.000 | 144.734 | 3.391 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 22.610555 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.193 | -4.193 | 0.000 | 144.734 | 4.193 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 47.389863 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.423 | -3.423 | 0.000 | 154.156 | 3.423 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 47.389863 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.225 | -4.225 | 0.000 | 154.156 | 4.225 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 47.389863 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.423 | -3.423 | 0.000 | 154.156 | 3.423 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 47.389863 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.225 | -4.225 | 0.000 | 154.156 | 4.225 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 60.000000 / record | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.439 | -3.439 | 0.000 | 158.842 | 3.439 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 60.000000 / record | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.241 | -4.241 | 0.000 | 158.842 | 4.241 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 60.000000 / favourable | 0.70 | SOURCE_APPROACH / 1.000000 | 0.110513 | 3.439 | -3.439 | 0.000 | 158.842 | 3.439 / upward authority short | 0.000 |  |
| candidate 6 | P100 / 60.000000 / favourable | 1.00 | SOURCE_APPROACH / 1.000000 | 0.110513 | 4.241 | -4.241 | 0.000 | 158.842 | 4.241 / upward authority short | 0.000 |  |
| candidate 7 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.149500 | -0.813923 | -22.558 | 153.500 | 118.534 | 0.000 | 34.966 / downward authority short | 22.558 |  |
| candidate 7 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.149500 | -0.813923 | -28.228 | 159.169 | 118.534 | 0.000 | 40.635 / downward authority short | 28.228 |  |
| candidate 7 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 35.106 | -28.053 | 7.053 | 152.009 | 28.053 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 41.916 | -34.863 | 7.053 | 152.009 | 34.863 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 4.938018 / record | 0.70 | RETURN_TRANSIT / 0.149500 | -0.813923 | -22.558 | 153.500 | 118.534 | 0.000 | 34.966 / downward authority short | 22.558 |  |
| candidate 7 | P100 / 4.938018 / record | 1.00 | RETURN_TRANSIT / 0.149500 | -0.813923 | -28.228 | 159.169 | 118.534 | 0.000 | 40.635 / downward authority short | 28.228 |  |
| candidate 7 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 35.106 | -28.053 | 7.053 | 152.009 | 28.053 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.942548 | 41.916 | -34.863 | 7.053 | 152.009 | 34.863 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 5.200784 / record | 0.70 | RETURN_TRANSIT / 0.149500 | -0.717025 | -19.873 | 149.138 | 121.299 | 0.000 | 27.838 / downward authority short | 19.873 |  |
| candidate 7 | P100 / 5.200784 / record | 1.00 | RETURN_TRANSIT / 0.149500 | -0.717025 | -24.867 | 154.133 | 121.299 | 0.000 | 32.833 / downward authority short | 24.867 |  |
| candidate 7 | P100 / 5.200784 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.894926 | 33.329 | -26.304 | 7.024 | 152.024 | 26.304 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 5.200784 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.894926 | 39.793 | -32.769 | 7.024 | 152.024 | 32.769 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 5.541040 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 31.277 | -17.651 | 13.626 | 145.404 | 17.651 / upward authority short | 13.482 |  |
| candidate 7 | P100 / 5.541040 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 37.342 | -23.716 | 13.626 | 145.404 | 23.716 / upward authority short | 17.522 |  |
| candidate 7 | P100 / 5.541040 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 31.277 | -24.290 | 6.987 | 152.043 | 24.290 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 5.541040 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.839972 | 37.342 | -30.356 | 6.987 | 152.043 | 30.356 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 5.730096 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 30.243 | -16.657 | 13.586 | 145.434 | 16.657 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 5.730096 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 36.107 | -22.521 | 13.586 | 145.434 | 22.521 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 5.730096 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 30.243 | -23.277 | 6.966 | 152.054 | 23.277 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 5.730096 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.812258 | 36.107 | -29.141 | 6.966 | 152.054 | 29.141 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 6.872958 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 25.201 | -11.860 | 13.341 | 145.618 | 11.860 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 6.872958 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 30.084 | -16.743 | 13.341 | 145.618 | 16.743 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 6.872958 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 25.201 | -18.360 | 6.841 | 152.119 | 18.360 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 6.872958 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.677193 | 30.084 | -23.244 | 6.841 | 152.119 | 23.244 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 7.331041 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.634878 | 23.621 | -10.378 | 13.243 | 145.692 | 10.378 / upward authority short | 9.123 |  |
| candidate 7 | P100 / 7.331041 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.634878 | 28.197 | -14.954 | 13.243 | 145.692 | 14.954 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 7.331041 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.634878 | 23.621 | -16.831 | 6.790 | 152.145 | 16.831 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 7.331041 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.634878 | 28.197 | -21.407 | 6.790 | 152.145 | 21.407 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 9.470465 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.018163 | -0.507 | 134.810 | 117.108 | 0.000 | 17.701 / downward authority short | 9.951 |  |
| candidate 7 | P100 / 9.470465 / record | 1.00 | RETURN_TRANSIT / 0.790000 | -0.027245 | -0.952 | 135.071 | 117.204 | 0.000 | 17.867 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 9.470465 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.332938 | 12.310 | -12.310 | 0.000 | 134.711 | 12.310 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 9.470465 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.491456 | 21.802 | -15.246 | 6.556 | 152.266 | 15.246 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 9.775576 / record | 0.70 | RETURN_TRANSIT / 0.792500 | -0.017809 | -0.497 | 135.002 | 116.501 | 0.000 | 18.501 / downward authority short | 9.755 |  |
| candidate 7 | P100 / 9.775576 / record | 1.00 | RETURN_TRANSIT / 0.790500 | -0.024933 | -0.871 | 135.225 | 116.575 | 0.000 | 18.650 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 9.775576 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.327339 | 12.101 | -12.101 | 0.000 | 133.980 | 12.101 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 9.775576 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.476117 | 21.118 | -14.596 | 6.522 | 152.283 | 14.596 / upward authority short | 13.834 |  |
| candidate 7 | P100 / 13.980788 / record | 0.70 | RETURN_TRANSIT / 0.798000 | 0.001384 | 0.038 | 136.150 | 110.984 | 0.000 | 25.166 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 13.980788 / record | 1.00 | RETURN_TRANSIT / 0.796000 | -0.004153 | -0.144 | 136.166 | 110.991 | 0.000 | 25.175 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 13.980788 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.260170 | 9.600 | -9.600 | 0.000 | 127.390 | 9.600 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 13.980788 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 14.140417 / record | 0.70 | RETURN_TRANSIT / 0.798000 | 0.001372 | 0.038 | 136.160 | 110.847 | 0.000 | 25.312 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 14.140417 / record | 1.00 | RETURN_TRANSIT / 0.796500 | -0.002745 | -0.095 | 136.168 | 110.850 | 0.000 | 25.318 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 14.140417 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.258045 | 9.521 | -9.520 | 0.000 | 127.224 | 9.520 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 14.714511 / record | 0.70 | RETURN_TRANSIT / 0.798500 | 0.002661 | 0.074 | 136.179 | 110.384 | 0.000 | 25.796 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 14.714511 / record | 1.00 | RETURN_TRANSIT / 0.797000 | -0.001331 | -0.046 | 136.172 | 110.381 | 0.000 | 25.791 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 14.714511 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.250643 | 9.245 | -9.245 | 0.000 | 126.658 | 9.245 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 14.714511 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 15.000000 / record | 0.70 | RETURN_TRANSIT / 0.799000 | 0.003932 | 0.109 | 136.183 | 110.170 | 0.000 | 26.013 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 15.000000 / record | 1.00 | RETURN_TRANSIT / 0.797500 | 0.000000 | 0.000 | 136.165 | 110.163 | 0.000 | 26.002 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 15.000000 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.247099 | 9.113 | -9.113 | 0.000 | 126.394 | 9.113 / upward authority short | 7.720 |  |
| candidate 7 | P100 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 19.302441 / record | 0.70 | RETURN_TRANSIT / 0.801000 | 0.010439 | 0.288 | 135.170 | 108.447 | 0.000 | 26.723 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 19.302441 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.008382 | 0.289 | 135.077 | 108.419 | 0.000 | 26.659 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 19.302441 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 19.302441 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 19.388471 / record | 0.70 | RETURN_TRANSIT / 0.801000 | 0.010497 | 0.290 | 135.134 | 108.434 | 0.000 | 26.701 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 19.388471 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.008450 | 0.292 | 135.040 | 108.405 | 0.000 | 26.635 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 19.388471 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 19.388471 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 20.054737 / record | 0.70 | RETURN_TRANSIT / 0.801000 | 0.010894 | 0.301 | 134.854 | 108.335 | 0.000 | 26.520 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 20.054737 / record | 1.00 | RETURN_TRANSIT / 0.800000 | 0.008923 | 0.308 | 134.753 | 108.303 | 0.000 | 26.450 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 20.054737 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 20.054737 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 22.610555 / record | 0.70 | RETURN_TRANSIT / 0.802000 | 0.013519 | 0.372 | 133.796 | 108.063 | 0.000 | 25.732 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 22.610555 / record | 1.00 | RETURN_TRANSIT / 0.801000 | 0.011793 | 0.405 | 133.664 | 108.019 | 0.000 | 25.646 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 22.610555 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 22.610555 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 7 | P100 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865655 | -24.184 | 142.700 | 118.516 | 16.463 | 7.720 / downward authority short | 7.720 |  |
| candidate 7 | P100 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865655 | -30.297 | 148.814 | 118.516 | 16.463 | 13.834 / downward authority short | 13.834 |  |
| candidate 8 | P100 / 4.938018 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -15.698 | 13.544 | 145.466 | 15.698 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 4.938018 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -21.368 | 13.544 | 145.466 | 21.368 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -22.297 | 6.945 | 152.065 | 22.297 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -27.967 | 6.945 | 152.065 | 27.967 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 4.938018 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -15.698 | 13.544 | 145.466 | 15.698 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 4.938018 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -21.368 | 13.544 | 145.466 | 21.368 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 4.938018 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 29.242 | -22.297 | 6.945 | 152.065 | 22.297 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 4.938018 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.785456 | 34.912 | -27.967 | 6.945 | 152.065 | 27.967 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 5.200784 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 27.761 | -14.284 | 13.476 | 145.517 | 14.284 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 5.200784 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 33.142 | -19.666 | 13.476 | 145.517 | 19.666 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 5.200784 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 27.761 | -20.851 | 6.910 | 152.083 | 20.851 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 5.200784 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.745772 | 33.142 | -26.232 | 6.910 | 152.083 | 26.232 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 5.541040 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 26.051 | -12.662 | 13.389 | 145.582 | 12.662 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 5.541040 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 31.100 | -17.711 | 13.389 | 145.582 | 17.711 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 5.541040 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 26.051 | -19.186 | 6.865 | 152.106 | 19.186 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 5.541040 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.699977 | 31.100 | -24.235 | 6.865 | 152.106 | 24.235 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 5.730096 / record | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.676882 | 25.189 | -11.849 | 13.340 | 145.619 | 11.849 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 5.730096 / record | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.676882 | 30.070 | -16.730 | 13.340 | 145.619 | 16.730 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 5.730096 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.676882 | 25.189 | -18.349 | 6.840 | 152.119 | 18.349 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 5.730096 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.676882 | 30.070 | -23.230 | 6.840 | 152.119 | 23.230 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 6.872958 / record | 0.70 | RETURN_TRANSIT / 0.789500 | -0.031450 | -0.875 | 135.227 | 126.058 | 0.000 | 9.169 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 6.872958 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 6.872958 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.564327 | 20.988 | -14.298 | 6.690 | 152.196 | 14.298 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 6.872958 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.564327 | 25.051 | -18.361 | 6.690 | 152.196 | 18.361 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 7.331041 / record | 0.70 | RETURN_TRANSIT / 0.790500 | -0.026561 | -0.739 | 135.671 | 124.677 | 0.000 | 10.995 / downward authority short | 9.542 |  |
| candidate 8 | P100 / 7.331041 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 7.331041 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.149500 | 0.529065 | 19.671 | -13.041 | 6.630 | 152.227 | 13.041 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 7.331041 / favourable | 1.00 | OUTBOUND_TRANSIT / 0.149500 | 0.529065 | 23.479 | -16.849 | 6.630 | 152.227 | 16.849 / upward authority short | 15.009 |  |
| candidate 8 | P100 / 9.470465 / record | 0.70 | RETURN_TRANSIT / 0.794500 | -0.009669 | -0.268 | 136.972 | 120.143 | 0.000 | 16.829 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 9.470465 / record | 1.00 | RETURN_TRANSIT / 0.792500 | -0.016115 | -0.560 | 137.103 | 120.180 | 0.000 | 16.923 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 9.470465 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.299464 | 11.062 | -11.062 | 0.000 | 134.700 | 11.062 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 9.470465 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 9.775576 / record | 0.70 | RETURN_TRANSIT / 0.795000 | -0.007880 | -0.218 | 137.079 | 119.673 | 0.000 | 17.406 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 9.775576 / record | 1.00 | RETURN_TRANSIT / 0.793000 | -0.014184 | -0.492 | 137.191 | 119.704 | 0.000 | 17.487 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 9.775576 / favourable | 0.70 | OUTBOUND_TRANSIT / 0.850500 | 0.293446 | 10.838 | -10.838 | 0.000 | 134.158 | 10.838 / upward authority short | 8.896 |  |
| candidate 8 | P100 / 9.775576 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 13.980788 / record | 0.70 | RETURN_TRANSIT / 0.800000 | 0.005993 | 0.165 | 137.373 | 115.433 | 0.000 | 21.940 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 13.980788 / record | 1.00 | RETURN_TRANSIT / 0.798500 | 0.002397 | 0.083 | 137.319 | 115.407 | 0.000 | 21.912 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 13.980788 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 13.980788 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 14.140417 / record | 0.70 | RETURN_TRANSIT / 0.800000 | 0.005938 | 0.164 | 137.350 | 115.322 | 0.000 | 22.028 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 14.140417 / record | 1.00 | RETURN_TRANSIT / 0.798500 | 0.002375 | 0.082 | 137.293 | 115.296 | 0.000 | 21.997 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 14.714511 / record | 0.70 | RETURN_TRANSIT / 0.800500 | 0.007840 | 0.216 | 137.119 | 115.138 | 0.000 | 21.981 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 14.714511 / record | 1.00 | RETURN_TRANSIT / 0.799000 | 0.004428 | 0.152 | 137.045 | 115.103 | 0.000 | 21.942 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 14.714511 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 14.714511 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 15.000000 / record | 0.70 | RETURN_TRANSIT / 0.800500 | 0.008233 | 0.227 | 136.981 | 115.064 | 0.000 | 21.917 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 15.000000 / record | 1.00 | RETURN_TRANSIT / 0.799000 | 0.004894 | 0.168 | 136.901 | 115.027 | 0.000 | 21.874 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 19.302441 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012734 | 0.349 | 134.818 | 114.266 | 0.000 | 20.553 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 19.302441 / record | 1.00 | RETURN_TRANSIT / 0.800500 | 0.011053 | 0.378 | 134.686 | 114.216 | 0.000 | 20.470 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 19.302441 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 19.302441 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 19.388471 / record | 0.70 | RETURN_TRANSIT / 0.801500 | 0.012746 | 0.349 | 134.773 | 114.253 | 0.000 | 20.520 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 19.388471 / record | 1.00 | RETURN_TRANSIT / 0.800500 | 0.011073 | 0.379 | 134.639 | 114.203 | 0.000 | 20.436 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 19.388471 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 19.388471 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 20.054737 / record | 0.70 | RETURN_TRANSIT / 0.802000 | 0.013619 | 0.373 | 134.445 | 114.183 | 0.000 | 20.262 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 20.054737 / record | 1.00 | RETURN_TRANSIT / 0.801000 | 0.012007 | 0.410 | 134.303 | 114.128 | 0.000 | 20.174 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 20.054737 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 20.054737 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 22.610555 / record | 0.70 | RETURN_TRANSIT / 0.807000 | 0.013427 | 0.367 | 131.169 | 117.727 | 0.000 | 13.441 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 22.610555 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 22.610555 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 22.610555 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 8 | P100 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865640 | -24.070 | 143.876 | 119.806 | 15.174 | 8.896 / downward authority short | 8.896 |  |
| candidate 8 | P100 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865640 | -30.183 | 149.989 | 119.806 | 15.174 | 15.009 / downward authority short | 15.009 |  |
| candidate 1 | P1000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 14.300045 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 14.300045 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 14.300045 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 14.300045 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 15.639184 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 15.639184 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 15.639184 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 15.639184 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 27.253677 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 27.253677 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 27.253677 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 27.253677 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 28.870139 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 28.870139 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 28.870139 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 28.870139 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 32.629354 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 32.629354 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 32.629354 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 32.629354 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 1 | P1000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.253 | 803.323 | 501.069 | 164.514 | 137.739 / downward authority short | 137.739 |  |
| candidate 1 | P1000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.396 | 864.466 | 501.069 | 164.514 | 198.882 / downward authority short | 198.882 |  |
| candidate 2 | P1000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 14.300045 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 14.300045 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 14.300045 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 14.300045 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 15.639184 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 15.639184 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 15.639184 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 15.639184 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 27.253677 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 27.253677 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 27.253677 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 27.253677 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 28.870139 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 28.870139 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 28.870139 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 28.870139 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 32.629354 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 32.629354 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 32.629354 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 32.629354 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 2 | P1000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -297.571 | 851.692 | 554.120 | 111.463 | 186.108 / downward authority short | 186.108 |  |
| candidate 2 | P1000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -358.714 | 912.835 | 554.120 | 111.463 | 247.251 / downward authority short | 247.251 |  |
| candidate 3 | P1000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 14.300045 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 14.300045 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 14.300045 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 14.300045 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 15.639184 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 15.639184 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 15.639184 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 15.639184 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 27.253677 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 27.253677 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 27.253677 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 27.253677 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 28.870139 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 28.870139 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 28.870139 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 28.870139 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 32.629354 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 32.629354 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 32.629354 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 32.629354 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 3 | P1000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -303.310 | 792.410 | 489.100 | 176.483 | 126.827 / downward authority short | 126.827 |  |
| candidate 3 | P1000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -364.453 | 853.553 | 489.100 | 176.483 | 187.970 / downward authority short | 187.970 |  |
| candidate 4 | P1000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 14.300045 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 14.300045 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 14.300045 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 14.300045 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 15.639184 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 15.639184 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 15.639184 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 15.639184 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 27.253677 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 27.253677 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 27.253677 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 27.253677 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 28.870139 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 28.870139 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 28.870139 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 28.870139 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 32.629354 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 32.629354 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 32.629354 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 32.629354 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 4 | P1000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -302.343 | 802.392 | 500.048 | 165.535 | 136.809 / downward authority short | 136.809 |  |
| candidate 4 | P1000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -363.486 | 863.535 | 500.048 | 165.535 | 197.951 / downward authority short | 197.951 |  |
| candidate 5 | P1000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 14.300045 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 14.300045 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 14.300045 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 14.300045 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 15.639184 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 15.639184 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 15.639184 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 15.639184 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 27.253677 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 27.253677 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 27.253677 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 27.253677 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 28.870139 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 28.870139 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 28.870139 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 28.870139 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 32.629354 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 32.629354 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 32.629354 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 32.629354 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 5 | P1000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.865791 | -298.877 | 838.206 | 539.329 | 126.254 | 172.623 / downward authority short | 172.623 |  |
| candidate 5 | P1000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.865791 | -360.020 | 899.349 | 539.329 | 126.254 | 233.766 / downward authority short | 233.766 |  |
| candidate 1 | P10000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 1 | P10000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.825 | 8597.283 | 6038.458 | 957.641 | 1601.184 / downward authority short | 1601.184 |  |
| candidate 1 | P10000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.464 | 9130.922 | 6038.458 | 957.641 | 2134.823 / downward authority short | 2134.823 |  |
| candidate 2 | P10000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 2 | P10000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2555.117 | 8641.713 | 6086.596 | 909.503 | 1645.614 / downward authority short | 1645.614 |  |
| candidate 2 | P10000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3088.756 | 9175.352 | 6086.596 | 909.503 | 2179.253 / downward authority short | 2179.253 |  |
| candidate 3 | P10000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 3 | P10000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.483610 | -1634.484 | 7737.129 | 6102.645 | 893.454 | 741.030 / downward authority short | 741.030 |  |
| candidate 3 | P10000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.483610 | -1976.013 | 8078.658 | 6102.645 | 893.454 | 1082.559 / downward authority short | 1082.559 |  |
| candidate 4 | P10000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 4 | P10000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2559.654 | 8587.341 | 6027.687 | 968.412 | 1591.243 / downward authority short | 1591.243 |  |
| candidate 4 | P10000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3093.294 | 9120.981 | 6027.687 | 968.412 | 2124.882 / downward authority short | 2124.882 |  |
| candidate 5 | P10000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 5 | P10000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2558.896 | 8596.434 | 6037.538 | 958.561 | 1600.335 / downward authority short | 1600.335 |  |
| candidate 5 | P10000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3092.535 | 9130.073 | 6037.538 | 958.561 | 2133.974 / downward authority short | 2133.974 |  |
| candidate 6 | P10000 / 4.938018 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 4.938018 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 4.938018 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 4.938018 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 14.140417 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 14.140417 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 14.140417 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 14.140417 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 15.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 15.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 15.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 15.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 47.389863 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 47.389863 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 47.389863 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 47.389863 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 60.000000 / record | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 60.000000 / record | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |
| candidate 6 | P10000 / 60.000000 / favourable | 0.70 | WATER_RELEASE / 1.000000 | -0.755640 | -2556.155 | 8629.267 | 6073.112 | 922.987 | 1633.169 / downward authority short | 1633.169 |  |
| candidate 6 | P10000 / 60.000000 / favourable | 1.00 | WATER_RELEASE / 1.000000 | -0.755640 | -3089.795 | 9162.907 | 6073.112 | 922.987 | 2166.808 / downward authority short | 2166.808 |  |


## Necessary stored energy, ideal accounting

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. Rotor energy and power figures are conditional on a constant hover merit times drive efficiency at every thrust and speed, with no separate blade profile power and no specified blade, rotor-speed or pitch policy. A separated model can move these figures in either direction.

Ideal, lossless chronological accounting with nominal class storage fully usable and the plan initial nitrogen inventory charged. No losses, health, state-of-charge window, reserve, external recharge or thermal limit. This is not an endurance rule, a mission-completion verdict or a battery model. Solar and nitrogen recovery are the existing bus inputs, not a promised recharge system.

Integrate the existing drawAt electrical.batteryPowerMW at 2000 midpoint samples per phase, in PHASES order. Record cumulative draw at every phase end; interpolate the first nominal-storage crossing inside its sample.

| Captured mission or printed profile | Class / km / basis | Draw MWh | Nominal storage MWh | First empty min | Shortage MWh | Pages |
|---|---|---|---|---|---|---|
| energy-profiles row 6 asDrawn | P1000 / 60.000000 / record | 139.3 MWh | 120 MWh | 85.4 min | 19.3 MWh | research/analysis/energy-profiles.md; research/analysis/energy-requirements.md; docs/ENERGY-MODEL-2026-10.md; docs/ENERGY-CLOSURE-2026-10.md; docs/PHYSICS.md; sim/README.md |
| energy-profiles row 7 asDrawn | P1000 / 60.000000 / favourable | 140.1 MWh | 120 MWh | 85.1 min | 20.1 MWh | research/analysis/energy-profiles.md; research/analysis/energy-requirements.md; docs/ENERGY-MODEL-2026-10.md; docs/ENERGY-CLOSURE-2026-10.md; docs/PHYSICS.md; sim/README.md |
| power-and-thrust requirement (nominal class energy capacity) | P1000 / 60.000000 / record | 246.0 MWh | 120 MWh | 64.8 min | 126.0 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / record | 139.2 MWh | 120 MWh | 85.4 min | 19.2 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / record | 139.3 MWh | 120 MWh | 85.4 min | 19.3 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / record | 139.5 MWh | 120 MWh | 85.3 min | 19.5 MWh | research/analysis/energy-requirements.md |
| power-and-thrust requirement (nominal class energy capacity) | P1000 / 60.000000 / favourable | 175.3 MWh | 120 MWh | 74.8 min | 55.3 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / favourable | 140.0 MWh | 120 MWh | 85.1 min | 20.0 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / favourable | 140.1 MWh | 120 MWh | 85.1 min | 20.1 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / favourable | 140.3 MWh | 120 MWh | 85.0 min | 20.3 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P100 / 60.000000 / record | 23.6 MWh | 20 MWh | 97.5 min | 3.6 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / record | 140.1 MWh | 120 MWh | 84.9 min | 20.1 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / record | 139.3 MWh | 120 MWh | 85.4 min | 19.3 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / favourable | 143.3 MWh | 120 MWh | 83.8 min | 23.3 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / favourable | 140.1 MWh | 120 MWh | 85.1 min | 20.1 MWh | research/analysis/energy-requirements.md |
| ready selector | P1000 / 400.000000 / record | 322.3 MWh | 120 MWh | 233.6 min | 202.3 MWh | concept/energy-analysis.html |

Of 20 captured cycles, 0 exceed nominal storage; every other captured cycle stays inside it for one ideal cycle. The full JSON records cumulative draw in phase order for 926 deduplicated current profiles, including unsupported paths as diagnostics and every shortage found. Earlier historical cells, the payload-exchange study and static component-only scans are outside this planCycle storage diagnostic. Current prescribed, selected, full-delivery, coefficient, single-input, requirement, descent and served-candidate profile tables are covered, including unsupported paths as supplied-effort diagnostics. Initial nitrogen is charged storage, not free energy. The 400 km P1000 ready-selector result is printed on concept/energy-analysis.html; it is outside the worked-example slider range.

Records: `research/analysis/energy-necessary.json`; generator: `research/analysis/energy-necessary.mjs`. No operational horizon or completion gate is added.

## How this was checked

Two ledger implementations used gpt-6-astra and gpt-6-sol.
Execution tests and a second reading used muse-spark-1.3; a number-by-number comparison used claude-fable-5-1.
Claude-opus-5-5 ruled on the supported claims.
A second model family, glm-5.3, read the physics document; claude-fable-5-1 wrote the payload-exchange analysis.
A person directs the project; no person checked the arithmetic.

Run `make energycheck energydoccheck`.
Independent equations check force, power, supply, smoothness and printed-row replay.
The checks do not validate a hull or rotor in flight.
<!-- energy:closure:end -->
