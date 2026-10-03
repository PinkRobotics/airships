# The payload exchange: what it would take to bring an empty hull back down

**Analysis, not design.** 2 October 2026. Every figure below is a key in `payload-exchange.json`,
written by `payload-exchange.py`, which shares no code with `sim/`. Keys are given in brackets. A prefix such
as `P1000.` stands for `classes.P1000.`, and `*.` stands for every class. Nothing here says the ship flies,
and nothing says it cannot be made to.

## 1. The problem, from the class constants

A fixed-displacement hull has one lift at each altitude and cannot change it. The ship is sized to float
fully loaded at the working altitude with a 5% margin. Once the water is gone it is lighter than the air it
displaces by more than a payload. Something must then push it back down to the lake.

| class | displacement m³ | lift at the lake, 1,300 m MSL | empty surplus at the lake | at the drop, 1,450 m | at the working altitude, 2,500 m | surplus / payload | empty hull floats in balance at |
|---|---:|---:|---:|---:|---:|---:|---:|
| P-100 | 220,000 | 237.4 t | 137.4 t | 133.9 t | 110.5 t | 1.374 | 9,212 m MSL |
| P-1000 | 2,200,000 | 2,374.4 t | 1,374.4 t | 1,339.3 t | 1,105.1 t | 1.374 | 9,212 m MSL |
| P-10000 | 22,000,000 | 23,743.6 t | 13,743.6 t | 13,393.3 t | 11,050.9 t | 1.374 | 9,212 m MSL |

Keys: `*.problem.dispM3`, `*.problem.altitudes.{hold,drop,work}.{liftT,emptySurplusT,emptySurplusOverPayload}`,
`*.problem.balance.emptyAltMslM`. The dry-mass target equals the payload on every class [`*.problem.dryMassTargetT`].
The loaded hull balances at 3,000 m MSL [`*.problem.balance.loadedAltMslM`]. The atmosphere is the standard one,
with the constants of `sim/atmosphere.js` [`constants.ISA`]; catalogue source `noaa-1976-us-standard-atmosphere`.

The baseline's letdown figures reproduce to 0.0001 t at every recorded worst instant: 34.25 t (P-100, 15 km),
868.56 and 816.83 t (P-1000, 15 and 60 km), 7,389.46 and 7,273.49 t (P-10000) [`baselineReproduction[*].unheldMine`,
`.unheldTree`, `.diffT`]. At broadside drag coefficient 0, 1 and 2 the P-1000 gap at 15 km is 790, 869 and 947 t
[`baselineReproduction[1].rangeAtCd`].

<!-- payload-capsule:start -->
The configured hull is a capsule, with a cylinder and hemispherical ends.
Its volumes are 217,784, 2,205,868 and 21,961,324 m³, computed from the configured lengths and diameters
[`*.problem.hull.config.capsuleVolumeM3`].
<!-- payload-capsule:end -->
The earlier published spheroid dimensions remain historical comparators [`*.problem.hull.published`].
The capsule volumes are close to the configured design volumes; their ratios are recorded explicitly
[`*.problem.hull.config.volumeOverDesign`].

The earlier empty P-1000 full-bus hover cap was 790.9 t at fixed density; this analysis gives 785.9 t at local density
[`P1000.routes.a.byEta.0.7.thrustCapT_fullBus_rho110`, `.thrustCapT_fullBus_local`].
The integrated model independently reproduces the local-density value.
Its cycle supplies actual nitrogen recovery and solar, then reserves other loads; it does not assume the generator rating is continuously available.
For the same cycle quantity, pages must use the integrated model's generated tables.
This study's simplified sketch remains labelled analysis and retains its earlier-profile comparison.

## 2. The routes, priced from first principles

All rotor figures use momentum theory with Glauert's inflow and one efficiency on the ideal induced power,
0.70, printed beside 0.55 (rule E17) [`constants.ETAS`]. Density is the local standard atmosphere (rule E13).
The bus is the battery plus the generator rating: 38, 190 and 1,550 MW [`*.problem.busMW`].

### 2a. Rotor hold-down as drawn

| class | hover power to hold the empty hull at the lake (η 0.70 / 0.55) | over the bus | thrust the whole bus buys at hover (η 0.70 / 0.55) | deficit at η 0.70 | disk area that would hold it on the drawn bus (η 0.70 / 0.55) | as a multiple of the hull planform |
|---|---:|---:|---:|---:|---:|---:|
| P-100 | 30.4 / 38.7 MW | 0.80 | 159.3 / 135.7 t | −21.9 t (closes) | 1,605 / 2,599 m² | 0.30 / 0.48 |
| P-1000 | 439.4 / 559.3 MW | 2.31 | 785.9 / 669.1 t | +588.5 t | 64,188 / 103,973 m² | 2.54 / 4.11 |
| P-10000 | 3,805.6 / 4,843.5 MW | 2.46 | 7,551.7 / 6,430.1 t | +6,191.9 t | 964,484 / 1,562,305 m² | 8.24 / 13.35 |

Keys: `*.routes.a.byEta.{0.7,0.55}.{hoverPowerNeededMW_local, powerOverBus, thrustCapT_fullBus_local,
hoverDeficitT_local, diskNeededM2_fullBus, diskNeededOverPlanform}`. At density 1.10 the P-1000 figures are 435.3 MW
and 790.9 t, the baseline's numbers [`P1000.routes.a.byEta.0.7.hoverPowerNeededMW_rho110`, `.thrustCapT_fullBus_rho110`].
The induced velocity through the drawn disk at the P-1000 hold is 22.8 m/s [`P1000.routes.a.byEta.0.7.inducedVelocityAtNeedMps`].

What this says: the P-100 can be held at hover by its drawn rotors. The P-1000 would need disks 2.5 to 4.1
times its own planform, the P-10000 8 to 13 times. Disk area scales with the hull's area and the surplus with
its volume, so this gap grows with size, and no re-tune of the drawn rotors removes it. This study's own cycle
sketch (section 2h) puts the P-1000 letdown gap at 641 t where the earlier profile puts it at 869 t
[`P1000.routes.a.sketch15.worstUnheldT`, `.earlierWorstUnheldT`]. The difference is the letdown rate.

### 2b. Water kept aboard

Water that stays in the hull is ballast the lake supplied for free. The amount needed lies between two bounds:
the hover bound, where a slow letdown lets the whole bus hold the hull at the lake, and the earlier profile.

| class, km | hover bound (η 0.70) | this study's sketch | earlier lever | delivered (sketch) | cycle MWh (sketch) | kWh per delivered tonne (sketch / earlier lever) | minutes added |
|---|---:|---:|---:|---:|---:|---:|---:|
| P-100, 15 | 0 t | 0 t | 34 t on the drawn letdown; no ballast repairs the loaded climb | 100 t | 7.2 | 71.9 / none | 0 |
| P-100, 60 | 0 t | 0 t | 0 t | 100 t | 20.2 | 202.1 / none | 0 |
| P-1000, 15 | 588.5 t | 640.4 t | 869.2 t | 359.6 t | 31.3 | 87.0 / 166.8 | −7.1 |
| P-1000, 60 | 588.5 t | 595.0 t | 817.4 t | 405.0 t | 88.0 | 217.4 / 322.9 | −6.6 |
| P-10000, 15 | 6,191.9 t | 6,538.1 t | 7,396.8 t | 3,461.9 t | 265.4 | 76.7 / 90.8 | −14.5 |
| P-10000, 60 | 6,191.9 t | 6,272.7 t | 7,280.8 t | 3,727.3 t | 560.3 | 150.3 / 164.4 | −13.9 |

Keys: `*.routes.b.keptAtHover_fullBusT.0.7`, `*.routes.b.byKm.{15,60}.0.7.{keptT, deliveredT, cycleMWh,
kwhPerDeliveredT, minutesAdded}`, `*.routes.b.byKm.*.earlierLever`, `*.routes.b.byKm.*.keptRangeT`. At η 0.55 the
P-1000 keeps 752 t and delivers 248 t at 15 km [`P1000.routes.b.byKm.15.0.55.keptT`, `.deliveredT`]. The cycle
energy is the earlier non-rotor channels plus this study's rotor integral [`*.routes.b.byKm.*.0.7.nonRotorMWh_earlier`,
`.rotorMWh`]. Minutes are negative because less water is pumped and released.

What this says: the route closes every class on the drawn vehicle at a price. The P-1000 delivers 13 to 41%
of its payload and the P-10000 24 to 37%, the range being the letdown profile and the rotor efficiency. The
P-100 needs no water kept. Its 34 t gap is the drawn letdown rate, and a slower letdown closes it (section 2h).

### 2c. The approach flown at airspeed

The hull as a lifting body at negative incidence must make the empty surplus as downforce. The planform is
the capsule and the span is the hull diameter, as in the earlier tree; aspect ratio 0.56 [`*.problem.hull.config.aspectRatio`].

| P-1000 at the lake | 15 m/s | 20 m/s | 25 m/s | 30 m/s | 35 m/s |
|---|---:|---:|---:|---:|---:|
| C_L needed on the config planform | 4.39 | 2.47 | 1.58 | 1.10 | 0.81 |
| C_L needed on the published planform | 2.85 | 1.60 | 1.03 | 0.71 | 0.52 |
| induced-drag power, e = 1.0 / 0.7 | 721 / 1,030 MW | 541 / 773 | 433 / 618 | 361 / 515 | 309 / 442 |
| lift over induced drag, e = 1.0 | 0.40 | 0.71 | 1.11 | 1.60 | 2.18 |
| closes on the 190 MW bus | no | no | no | no | no |

Keys: `P1000.routes.c.bySpeed.{15,20,25,30,35}.{clNeeded_configPlanform, clNeeded_publishedPlanform, inducedPowerMW_e1.0,
inducedPowerMW_e0.7, liftOverInducedDrag_e1.0, closesOnBus_e1.0}`. The P-100 closes at every speed from 20 m/s
at both span efficiencies, needing C_L 0.38 to 1.16 [`P100.routes.c.bySpeed.{20,25,30,35}.closesOnBus_e0.7`, `.clNeeded_configPlanform`].
The P-10000 needs 6.5 to 15.6 GW [`P10000.routes.c.bySpeed.{15,35}.inducedPowerMW_e1.0`].

Measured bodies of this shape, converted to a planform basis by this study [`constants.clConversions`], reach
the following. The Akron hull with fins at 20° pitch gives 0.405 on (vol)^(2/3), which is 0.14 on its planform. Its bare hull peaks at 0.115, which is 0.04 (Freeman 1932, NACA Report 432; not in the catalogue).
A fineness-4 finned hull at 35.6° gives a normal-force coefficient of 0.825 on (vol)^(2/3). That is a lift of
0.65, or 0.34 on its planform (Voloshin, Chen and Calay 2012; not in the catalogue). A fineness-4 hybrid
lifting hull gives 0.0067 per degree from a zero-lift angle of −4.2°, about 0.11 at 12° (Ul Haque et al. 2016;
not in the catalogue). The range this study treats as measured is therefore 0.14 to 0.34
[`constants.CL_MEASURED_PLANFORM`]. The earlier tree's 0.5, 1.0 and 1.5 are assumptions [`constants.CL_ASSUMED`].

The table below gives the speed at which the aerodynamic downforce alone holds the empty hull, and the power there.

| class | V at C_L 0.14 | V at C_L 0.34 | power at C_L 0.34, e = 1.0 / 0.7 | closes on the bus |
|---|---:|---:|---:|---|
| P-100 | 57.5 m/s | 36.9 m/s (1.48 × cruise) | 18.5 / 24.4 MW | yes |
| P-1000 | 84.0 m/s | 53.9 m/s (1.76 × cruise) | 268.6 / 354.6 MW | no |
| P-10000 | 123.5 m/s | 79.2 m/s (2.19 × cruise) | 3,940 / 5,204 MW | no |

Keys: `*.routes.c.favourable.{cl0.14,cl0.34}.{VminMps, VminOverCruise, totalPowerMW_e1.0, totalPowerMW_e0.7, closesOnBus_e1.0}`.
With the rotors at their installed cap and the hull at C_L 0.34, the P-1000 is 9 t short in level flight at
35 m/s [`P1000.routes.c.bySpeed.35.split_cl0.34.unheldT`]. At C_L 1.0 it closes [`P1000.routes.c.bySpeed.35.split_cl1.0.unheldT`].
On the record basis the rotors alone, edgewise at 35 m/s, buy 1,088 t against the 786 t installed cap and the
1,374 t surplus [`P1000.routes.c.bySpeed.35.record_rotorThrustAtBusT`, `.record_surrogateCapT`, `.record_unheldT`].

**The hand-over.** The bag must fill in the lake, and a stopped hull loses its downforce. Three forms were
examined; the keys are under `*.routes.c.handOver`.

1. Circling with the cable's lower end near the circle centre, the long-line form (Skop and Choo 1971; not in
the catalogue). The cable hangs 240.5 m below the P-1000 attachment at the hold altitude, so the hull can
circle at most 550 m from the bag [`P1000.routes.c.handOver.cableBelowAttachmentM`, `.circleRadiusMaxM`]. A circle of
two hull lengths, 476 m, puts the cable 63° from vertical [`P1000.routes.c.handOver.circles.2L.cableAngleFromVerticalDeg`].
When the bag leaves the water it is 476 m from under the hull and must swing or orbit. The swing reaches
80 m/s [`P1000.routes.c.handOver.circles.2L.pendulumSpeedMps`], an orbit 22 m/s [`...circles.2L.bagOrbitSpeedIfConicalMps`].
At 53.9 m/s the turn needs 6.5°/s, a bank of 32° or 1,660 t of side force, and the hull's ends see 14° of
local sideslip [`...circles.2L.{turnRateDegPerS, bankForTurnDeg, centripetalForceT, endSideslipDeg}`]. The
effective mass includes the transverse added mass, k2 = 0.702 at fineness 2 (Munk 1924; not in the catalogue)
[`P1000.routes.c.handOver.effectiveMassT`, `.addedMassK2_fineness2`]. A one-length circle brings the cable to 45°
and doubles the turn rate [`...circles.1L.cableAngleFromVerticalDeg`, `.turnRateDegPerS`]. The P-10000 cannot reach
the centre from a two-length circle at all [`P10000.routes.c.handOver.circles.2L.reachable`]. Incoherent as
drawn: the bag's release speed is of the order of the hull's airspeed.

2. A steady head wind, the hull at zero ground speed. The wind would have to equal the speeds in the table
above: 36.9 to 57.5 m/s for the P-100, 53.9 to 84.0 m/s for the P-1000 [`*.routes.c.handOver.headWind`]. No
pendulum, but these are storm winds, and the route then exists only when they blow.

3. Stop over the bag, hover, lower, fill, hoist. The P-100 holds itself at hover with 21.9 t to spare
[`P100.routes.c.handOver.hoverInterval.unheldT_fullBus`]. The P-1000 is 588.5 t light for the interval and
accelerates upward at 2.2 m/s² [`P1000.routes.c.handOver.hoverInterval.unheldT_fullBus`, `.initialAccelMps2`]. It
would rise at a terminal 20.6 m/s [`...hoverInterval.terminalRiseMps_CD1`]. The cable pays out in 48 s and the
hoist takes 3 s [`...hoverInterval.cablePayoutS`, `.hoistS`]. Once the bag hangs, hover closes with 661.5 t to spare
[`...hoverInterval.withBagAtHoverT`]. The interval is the whole problem.

Three things must be shown before this route counts. First, a measured lift curve for this hull at negative
incidence to −20°, at the flight Reynolds number, on a stated reference area. Second, a hand-over that holds
the hull through the interval between airspeed and bag, with the bag's motion bounded. Third, the fin and
bending loads at the turn rates above. In this study's cycle sketch the aerodynamic share changes the water
the P-1000 must keep from 640 t to 638 t, because the gap is in the hover [`P1000.routes.c.sketch15.cl0.34.keptToCloseT`].

### 2d. A hull balanced at half load, rotors pushing both ways

The hull is sized so that it floats at the working altitude with half the payload aboard. For the P-1000 that
is 1,567,630 m³, a change of −28.7%, and a hull area of −20.2% [`*.routes.d.dispM3`, `.dispChange`, `.hullAreaChange`].
The wall may weigh 40% more per cubic metre at the same dry target [`*.routes.d.allowedWallMassPerM3Change`].
The hull is 213 × 106 m [`P1000.routes.d.lenM`, `.diaM`].

| class | push down, empty at the lake | its hover power (η 0.70 / 0.55) | push up, loaded at work | its hover power (η 0.70, ideal / at reverse factor 0.5) | cycle MWh at 15 km, reverse 1.0 / 0.5 | kWh per tonne | closes in the sketch |
|---|---:|---:|---:|---:|---:|---:|---|
| P-100 | 69.2 t | 10.9 / 13.8 MW | 50.0 t | 7.1 / 14.2 MW | 3.4 / 3.9 | 34 / 39 | yes |
| P-1000 | 691.9 t | 157.0 / 199.8 MW | 500.0 t | 102.4 / 204.8 MW | 38.6 / 46.1 | 39 / 46 | yes |
| P-10000 | 6,918.7 t | 1,359.3 / 1,730.0 MW | 5,000.0 t | 886.9 / 1,773.7 MW | 330.7 / 385.8 | 33 / 39 | yes |

Keys: `*.routes.d.byEta.{0.7,0.55}.{downThrustT_emptyAtHold, downHoverMW, upThrustT_loadedAtWork, upHoverMW_ideal,
upHoverMW_reverseRange}`, `*.routes.d.sketch15.{reverse1.0,reverse0.5}.{cycleMWh, kwhPerDeliveredT, closes}`. At 60 km
the P-1000 cycle is 105 to 132 MWh [`P1000.routes.d.sketch60.{reverse1.0,reverse0.5}.cycleMWh`]. At η 0.55 the two
larger classes do not close the down-hover [`P1000.routes.d.byEta.0.55.closesDownAtHover`]. The reverse factor is
an assumption with no source [`constants.REVERSE_THRUST_FACTOR`].

The failure case: a loaded ship whose rotors stop is heavy by 500 t (P-1000). At broadside C_D 1 it sinks at
a terminal 21.7 m/s and reaches the ground from the working altitude in 69 s [`P1000.routes.d.failureCase.heavyT`,
`.terminalSinkMps_CD1`, `.secondsToGroundAtTerminal`]. Shedding the water in that time needs 7.2 m³/s, 2.4 times
the drawn fill rate [`P1000.routes.d.failureCase.dumpRateNeededM3s`, `.dumpRateOverDrawnFill`]. For the P-10000:
32 m/s, 47 s, 106 m³/s [`P10000.routes.d.failureCase`]. This gives up the fail-safe float-up property of the
2026-08-09 decision. The drawn rotors are declared not reversible (rule E10). This route needs an upward
actuator of the loaded deficit at the powers above, so the class record changes [`*.routes.d.ifRotorsNotReversible`].
Direction and size only: no structure is drawn here.

### 2e. Variable displacement

To balance the empty P-1000 at the lake the vacuum volume would shrink by 1,273,435 m³, 57.9% of the hull
[`P1000.routes.e.fullExchange.volumeChangeM3`, `.volumeFraction`]. To bring the surplus down to what the drawn
rotors hold, it would shrink by 545,286 m³, 24.8% [`P1000.routes.e.toRotorCap.volumeChangeM3`, `.volumeFraction`].
The ideal isothermal work to re-establish that vacuum against 86.7 kPa is 30.7 MWh per cycle, or 13.1 MWh for
the partial exchange [`P1000.routes.e.ambientPressurePa`, `P1000.routes.e.{fullExchange,toRotorCap}.idealWorkMWh`].
At an isothermal pump efficiency of 0.30 the electrical energy is 102 and 44 MWh [`P1000.routes.e.{fullExchange,toRotorCap}.electricalMWh_eff030`].
Done inside the fill, the partial exchange is 142 MW ideal and 472 MW at 0.30, against a 190 MW bus
[`P1000.routes.e.toRotorCap.meanPowerInFillMW_15`, `.meanPowerInFillMW_eff030_15`]. Spread over the 15 km cycle it
is 22 and 74 MW [`P1000.routes.e.toRotorCap.meanPowerOverCycleMW_15`, `.meanPowerOverCycleMW_eff030_15`]. The cells
would change volume 41 times a day at 15 km [`P1000.routes.e.toRotorCap.cyclesPer24h_15`]. For the P-10000 the
partial exchange is 138 MWh ideal and 460 MWh electrical [`P10000.routes.e.toRotorCap.idealWorkMWh`, `.electricalMWh_eff030`].

What it asks of permanently sealed cells: a rigid vacuum structure that folds and re-erects by a quarter to
more than half its volume every cycle, under full atmospheric crush, with no valve. The helium analogue is the
constant-volume compression of US patent 9,016,622 (not in the catalogue); a vacuum hull has no gas to compress.
This route is closed by the sealed-cell decision recorded in `air-ballast.md` (retraction of 2026-08-10). It
can be reopened only as a design decision [`*.routes.e.closedBy`].

### 2f. Ballast made on board by the cryogenic plant

The drawn P-1000 plant makes 33 to 70 t of liquid nitrogen an hour at 907 to 430.7 kWh/t, and 66.7 t/h at the
config 450 kWh/t [`P1000.routes.f.tonnesPerHourAtDrawnPlant`]. The specific energies are catalogue sources
`rimpel-2023-liquid-air-combined-cycle` and `arnaiz-del-pozo-2020-nitrogen-liquefaction`. The exchange mass is
the force gap, 588.5 to 868.6 t at 15 km [`P1000.routes.f.byKm.15.gapT`]. Making 868.6 t costs 374 to 788 MWh per
cycle [`P1000.routes.f.byKm.15.earlierWorst.{optimumCollins_arnaizDelPozo2020,standalone_rimpel2023}.energyPerCycleMWh`].
Made in the 22.1 minute window in which the water is aboard, that is 1,015 to 2,138 MW, 5 to 11 times the bus
[`P1000.routes.f.byKm.15.makingWindowMin`, `...earlierWorst.{optimumCollins_arnaizDelPozo2020,standalone_rimpel2023}.powerToMakeInWindowMW`, `.powerOverBus`]. A plant of
that power weighs 2,030 to 4,275 t at the lightest sourced 2 t/MW, above the 1,000 t dry target
[`...earlierWorst.{optimumCollins_arnaizDelPozo2020,standalone_rimpel2023}.plantMassT_range`]. The drawn plant makes 12 to 26 t per cycle [`...earlierWorst.{optimumCollins_arnaizDelPozo2020,standalone_rimpel2023}.tonnesMadeByDrawnPlantPerCycle`].
The P-100's 34 t at 15 km would cost 15 to 31 MWh per cycle against an 8 MWh cycle
[`P100.routes.f.byKm.15.earlierWorst.{optimumCollins_arnaizDelPozo2020,standalone_rimpel2023}.energyPerCycleMWh`, `earlierData.cycles`]. The P-10000 needs 3,183 to 6,702 MWh
per cycle [`P10000.routes.f.byKm.15.earlierWorst.{optimumCollins_arnaizDelPozo2020,standalone_rimpel2023}.energyPerCycleMWh`]. Does not close on any class with a gap.

### 2g. Combinations, P-1000 at 15 km on the drawn bus

| pair | closes | delivered | condition | vehicle change |
|---|---|---:|---|---|
| a + b | yes | 359.6 t (sketch); 130.8 t on the earlier letdown | slow letdown, whole bus on the rotors | no |
| b + c | only if shown | 411.5 t | C_L 0.34 at 53.9 m/s, and a hand-over through the hover interval with 588.5 t aboard | no |
| c + bag | no | | the hover interval has no actuator | no |
| a + f | no | | the drawn plant makes 24.6 t per cycle against 868.6 t | no |
| b + f | yes | 155.4 t | the plant replaces the tonnes it can make | no |
| a + d | yes | 1,000 t | smaller hull, reversible rotors, float-up given up | yes |
| a + e | yes | 1,000 t | cells that change volume by 24.8% every cycle, 44 MWh electrical | yes |

Keys: `P1000.routes.g.{a+b, b+c, c+bag, a+f, b+f, a+d, a+e}`. On the drawn vehicle, nothing closes the P-1000 at
15 km with full delivery.

### 2h. The cycle sketch this study prices with

The sketch integrates the rotor power along a simplified cycle. Its phases are the climb after release, the
cruise at the working altitude, and a letdown at a constant rate over the last 28% of the return plus the
approach. Then come the fill at hover with the bag, the loaded cruise, and the release at hover. Durations are the earlier tree's
[`earlierData.durationsMin`]. The letdown rate is 1,200 m over the letdown time, 3.5 m/s for the P-1000 at 15 km,
where the earlier profile peaks at 7.4 m/s [`baselineReproduction[1].vz`]. The bag is credited when the cable reaches
the water and the ground speed is below 2 m/s, and never beyond the surplus. The rotor energies agree with the
earlier channel to within 7% on the P-1000 and 21% on the P-10000 [`*.routes.a.sketch15.rotorMWh`, `.earlierRotorsMWh`].
The gaps are smaller because the letdown is gentler. Both numbers are supplied effort along an unsupported profile.

## 3. Ranking, and the one next analysis

1. **Water kept aboard (b).** Closes every class on the drawn vehicle and bus. Price: the P-1000 delivers 248 to
412 t of 1,000, the P-10000 2,380 to 3,808 t of 10,000, by the letdown rate and the rotor efficiency.
2. **Half-load hull with two-way rotors (d).** Closes the force balance on the drawn bus with full delivery on all
three classes at η 0.70, with a 29% smaller hull. It changes the vehicle and gives up fail-safe float-up.
3. **Approach at airspeed (c).** Closes the moving legs for the P-100, which needs no help at hover anyway, and
nearly for the P-1000 at measured lift coefficients with the rotors at their cap. The hand-over has no coherent
form at the drawn cable and hull lengths.
4. **Variable displacement (e).** Affordable in energy only for the partial exchange, and only spread over the
cycle. It asks sealed cells to change volume every cycle; closed by a reopenable decision.
5. **Rotor hold-down as drawn (a).** The disk needed is 2.5 to 13 hull planforms on the two larger classes.
6. **Cryogenic ballast (f).** The energy and plant mass to make the ballast inside the cycle exceed the bus and
the dry mass on every class with a gap.

Keys: `ranking`, `nextAnalysis`. Plainly: **neither the P-1000 nor the P-10000 closes with full delivery
without changing the vehicle.** The one next analysis is route d, opened on its failure case first
[`*.routes.d.failureCase`], then on the reversible rotor and the cycle energy, before any hull is drawn. What
closes the force ledger there is a smaller hull that is heavy when loaded, the opposite of the 2026-08-09
sizing rule. That rule has to be re-decided, not worked around.

## 4. Sources

Catalogue entries used:
- `noaa-1976-us-standard-atmosphere`: the standard atmosphere.
- `ardema-1984-lta-missions`: negative aerodynamic lift under way, and circling flight when the wind is below
  the airspeed required. The Heli-stat quadrotor with two rotors pushing down and two up, for which "no ballast
  recovery would be necessary". Ballasting for buoyancy control named as the problem of conventional airships.
- `hochstetler-2016-heavy-lift-airships`: ballast requirements as a mission-tool output.
- `arney-1983-bambi-bucket`: the bag.
- `arnaiz-del-pozo-2020-nitrogen-liquefaction`: 430.7 kWh/t.
- `rimpel-2023-liquid-air-combined-cycle`: 685 to 907 kWh/t standalone.
- `hamdy-2019-liquefaction-exergy`: liquefaction exergy, background.
- `chin-2021-battery-cell-to-pack`, `lvovich-2020-nasa-energy-storage`: battery specific energies, via `mass-budget.json`.
- `suter-2005-rotor-wash`: rotor wash, background.

Outside the catalogue, each marked "not in the catalogue" where used:
- Freeman, H. B. (1932). Force measurements on a 1/40-scale model of the U.S. airship "Akron". NACA Report 432.
  https://ntrs.nasa.gov/citations/19930091505. Taken: Table II-b lift coefficients on (vol)^(2/3) with Mark-II
  fins, 0.405 to 0.411 at 20° pitch, elevator 0°; bare-hull lift to 0.115; fineness 5.9; Reynolds numbers 3.05
  to 4.30 million on (vol)^(1/3).
- Voloshin, V., Chen, Y. K., Calay, R. (2012). A comparison of turbulence models in airship steady-state CFD
  simulations. arXiv:1210.2970. https://arxiv.org/abs/1210.2970. Taken: wind-tunnel coefficients on reference
  area 0.101 m² for a fineness-4 finned hull at 37 m/s: cz 0, 0.233, 0.825 and cx 0.0419, 0.0325, 0.038 at
  −0.4°, 11.62°, 35.62°.
- Ul Haque, A., Asrar, W., Omar, A. A., Suleiman, E. (2016). Wind tunnel testing on a generic model of a hybrid
  lifting hull. J. Aerosp. Technol. Manag. 8(4), 467–474. https://doi.org/10.5028/jatm.v8i4.645. Taken: slope
  0.0067 per degree, zero-lift angle −4.2°, reference area 0.042 m², Re 6.3 × 10⁵, range −8° to +12°.
- Munk, M. M. (1924). The aerodynamic forces on airship hulls. NACA Report 184.
  https://ntrs.nasa.gov/citations/19930091249. Taken: additional-mass coefficients, fineness 2.00: k1 0.209,
  k2 0.702; fineness 3.99: k1 0.082, k2 0.860.
- Skop, R. A., Choo, Y.-I. (1971). The configuration of a cable towed in a circular path. J. Aircraft 8(11),
  856–862. https://doi.org/10.2514/3.44310. Taken: the towed end can sit near the axis of rotation for some
  parameter ranges, which is the long-line form examined in 2c.
- Glauert, H. (1926). A general theory of the autogyro. ARC R&M 1111.
  https://naca.central.cranfield.ac.uk/bitstream/handle/1826.2/1434/arc-rm-1111.pdf. Taken: the inflow relation
  for a rotor in forward and axial flight.
- Johnson, W. (1994). Helicopter Theory. Dover, ISBN 978-0-486-68230-3. Taken: momentum-theory hover power.
- Prandtl, L. (1921). Applications of modern hydrodynamics to aeronautics. NACA Report 116.
  https://ntrs.nasa.gov/citations/19930091180. Taken: the induced drag of a lifting line, L²/(q π b² e).
- Lobner, P. (2026 update). Modern Airships: CargoLifter AG. https://lynceans.org/wp-content/uploads/2020/12/Cargolifter-AG.pdf.
  Taken: the CL-160 load exchange with water ballast, and the 7 May 2002 CL75 AC exchange of 55 t for 55 m³ of
  water in minutes. The hovering ship was rigged to the ground by four cable winches, with a 10 m/s steady-wind
  limit. The precedent for an exchange is a tether to the ground, not an aerodynamic hold.
- Pasternak, I. (2015). Flight system for a constant volume, variable buoyancy air vehicle. US patent 9,016,622 B1.
  https://patents.google.com/patent/US9016622B1. Taken: buoyancy changed by compressing the lifting gas at
  constant hull volume.

Assumptions with no source, named as ranges:
- Turn radius one to three hull lengths [`constants.TURN_RADIUS_LENGTHS`].
- Reverse-thrust power factor 0.5 to 0.8 [`constants.REVERSE_THRUST_FACTOR`].
- Isothermal pump efficiency 0.30 to 1.0 [`constants.ISOTHERMAL_PUMP_EFF`].
- Broadside drag coefficient 0 to 2 [`constants.VERTICAL_CD_RANGE`].
- Span efficiency 0.7 to 1.0 [`constants.E_SPAN`].
- The planform conversions of the measured coefficients [`constants.clConversions`].

## 5. What this study leaves out

The battery mass at the sourced specific energies is 240 to 805 t on the P-1000 and 4,000 to 13,423 t on the
P-10000 [`*.batteryMassT`, `*.batteryMassOverDryTarget`]. The dry targets are 1,000 and 10,000 t, and no route
above changes that. Not priced here: cable mass, the bag's pendulum in the vertical letdown, wind, the inertia
of the letdown, and the rotor regime of a hull climbing against its own hold-down. Rule E18 lists them for the model.
