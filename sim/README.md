# `sim/` — the model, and an index to every number it publishes

This directory is the entire simulation. Fifteen ES modules, no DOM, no network, no wall
clock, no globals. Every figure the site prints — every tonne, minute, megawatt and
megawatt-hour — is computed by a function in here, and this file says which one.

The point of the separation is auditability. A reader who wants to attack a published
number should be able to find the line that produces it, the equation behind it, and the
assumption it rests on, without reading the website. The tables below are for that. Find
your quantity, read across, open the file.

Read `../docs/PHYSICS.md` for the reasoning, the constants and their provenance, and the
model's known defects. Read `../docs/ARCHITECTURE.md` for why the code is shaped this way.

---

## Re-running any of it yourself

The model is published as `window.AIRSHIPS.sim` on the live page. Nothing needs to be
cloned or built:

```js
AIRSHIPS.sim.selftest()                                       // every shipped assertion
AIRSHIPS.sim.ledger(AIRSHIPS.sim.CLASSES.P10000)              // the mass ledger
AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P10000,
                       AIRSHIPS.sim.MODES.balanced, 15)       // a whole cycle
```

`?selftest=1` on any page runs the assertions at load and appends the result to the
document title. `?seed=N` pins the model's random choices; `?data=snapshot` pins its
inputs. Together they make a run exactly reproducible, which is what
`tests/golden/seed7-snapshot.json` compares against.

Arithmetic nobody can re-run is a claim, not a calculation. Everything below can be
re-run.

---

## The modules

| File | Lines | What it owns |
|---|---:|---|
| `config.js` | 136 | Every tunable and every vehicle assumption. Nothing here is measured. |
| `physics.js` | 30 | The four first-order relations: pump, drag, actuator disk, mass ledger. |
| `plan.js` | 104 | `planCycle` — phase durations, water delivered, energy per cycle. |
| `state.js` | 254 | `stateAt` — where a ship is and what it is doing at one moment. |
| `mission.js` | 83 | Assembling a fire, a source, a plan and a set of drop lines. |
| `assign.js` | 68 | Which class a fire gets, and the logistics override. |
| `water.js` | 129 | Choosing a lake; choosing where over the lake to hover. |
| `targets.js` | 196 | Candidate drop lines, scoring, sequencing, per-cycle jitter. |
| `communities.js` | 43 | Populated places, as a physical input to target scoring. |
| `geo.js` | 60 | Distance, bearing, Bézier paths, easing. |
| `rng.js` | 30 | The seed and the stable hash. |
| `narrate.js` | 53 | The mission trace in prose. |
| `format.js` | 17 | Number and unit formatting (en-CA). |
| `selftest.js` | 84 | Seventeen assertions, shipped so a reader can run them. |
| `index.js` | 49 | The single import surface. |

Units are SI internally — kg, m, s, N, W — surfaced as tonnes, kilometres, minutes,
megawatts and megawatt-hours. One tonne of water is one cubic metre.

---

## Audit index: mass and lift

| Quantity | Units | Computed in | Equation | Rests on | Set in |
|---|---|---|---|---|---|
| `liftT` | t | `physics.js` → `ledger` | `dispM3 × rhoSL / 1000` | air displaced at **sea level**, at every altitude | `config.js` `CLASSES[*].dispM3`, `DEFAULTS.rhoSL = 1.225` |
| `dryT` | t | `physics.js` → `ledger` | `= payloadT` | structure, machinery, batteries and plant together weigh exactly one payload | `config.js` `CLASSES[*].payloadT` |
| `surplusT` | t | `physics.js` → `ledger` | `liftT − dryT` | both of the above | as above |
| `reserveT` (ledger) | t | `physics.js` → `ledger` | `liftT − dryT − payloadT` | both of the above | as above |
| `massT` | t | `state.js` → `stateAt` | `dryT + water + ln2` | the ledger; the phase's water and nitrogen curves | `state.js` per-phase blocks |
| `buoyN` | N | `state.js` → `stateAt` | `liftT × 1000 × 9.81` | `liftT` | — |
| `weightN` | N | `state.js` → `stateAt` | `massT × 1000 × 9.81` | `massT` | — |
| `netN` | N | `state.js` → `stateAt` | `buoyN − weightN` | both | — |
| `netFrac` | — | `state.js` → `stateAt` | `clamp₀¹((liftT − massT) / (liftT − dryT))` | the ledger | — |
| `vert` | — | `state.js` → `stateAt` | `−hold × netFrac`; `hold` is a per-phase curve | the ledger; the phase curves | `state.js`, the `hold`/`share` block |

**Trap.** Two different quantities are called *reserve*. `ledger().reserveT` is
`liftT − dryT − payloadT` (20.5 t on a P-100) and is what the concept page prints. The
local `reserveT` inside `stateAt` is `liftT − dryT` (120.5 t on a P-100) and is the
denominator of `netFrac` and the scale of every rotor thrust. They differ by one payload.

**Known defect.** `ledger` uses `rhoSL`, sea-level density, while the ships work between
300 m and about 1,180 m above ground over terrain that is itself 500–1,500 m up. See
`../docs/PHYSICS.md` §"Defect 1".

---

## Audit index: the delivery cycle

Everything in this table comes from `plan.js` → `planCycle(cls, mode, oneWayKm, wind)`.
`kph = cruiseKph × mode.speed × speedMul`; `fill = fillM3s × fillMul`; `rampF = 1/0.85`.

| Quantity | Units | Equation | Rests on | Set in |
|---|---|---|---|---|
| `gsOut`, `gsRet` | km/h | `clamp(kph + wind·cos(track), 0.35 kph, 1.8 kph)` | the 850 hPa wind is the wind the whole leg flies in | `app/feeds.js` (live), `config.js` `cruiseKph` |
| `dur.SOURCE_APPROACH` | min | `max(1.5 × fixed, hoseDeployMin × 0.5 × hose)` | hose deployment overlaps the flown approach, so only half of it is charged | `config.js` `hoseDeployMin`, `MODES[*].hose`, `MODES[*].fixed` |
| `dur.WATER_FILL` | min | `deliveredT / fill / 60` | the pump runs at its rated rate from first contact | `config.js` `fillM3s`, `DEFAULTS.fillMul` |
| `dur.OUTBOUND_TRANSIT` | min | `max(oneWayKm / gsOut × 60 × rampF, hoseRetractMin × 0.4 × hose + 0.8)` | a leg is a trapezoid: 15% accelerating, 15% braking | `plan.js`, the `rampF` constant |
| `dur.WATER_RELEASE` | min | `max(0.8, dropKm / (kph × 0.45) × 60) × passes` | the drop run is flown at 45% of cruise | `config.js` `dropKm`; the 0.45 is set in `plan.js` |
| `passes` | count | `ceil(deliveredT / fill / 60 / lineMin)`, rounded up to the next odd number | sprayers meter the dump at the fill rate; an odd count ends the run at the far end | `plan.js` |
| `dur.BUOYANCY_ESCAPE` | min | `2 × mode.fixed` | flat two minutes, not derived | `config.js` `MODES[*].fixed` |
| `dur.RETURN_TRANSIT` | min | `max(1.2, oneWayKm / gsRet × 60 × rampF)`, then `× 1.12` if `battLimited` | as outbound; the 1.12 is a longer, shallower letdown | `plan.js` |
| `cycleMin` | min | sum of the six phase durations | — | — |
| `dropsPerHour` | 1/h | `60 / cycleMin` | — | — |
| `tph` | t/h | `deliveredT × 60 / cycleMin` | — | — |
| `bottleneck` | label | a cascade of tests on handling vs transit, `cryoLimited`, `battLimited`, `retainedT` | — | `plan.js`, end of function |

The mission's own leg length is not `oneWayKm` from the source centroid to the fire
centroid. `mission.js` → `buildMission` computes `m.legKm` from `targets.js` → `legKmFor`,
which averages hose-station-to-line-head plus line-tail-to-next-station over the target
rotation, and passes *that* to `planCycle`. It is routinely 40% longer than the centroid
distance. The panels still display `oneWayKm`.

---

## Audit index: water and ballast

| Quantity | Units | Computed in | Equation | Rests on | Set in |
|---|---|---|---|---|---|
| `rotorMaxT` | t | `plan.js` → `planCycle` | `((battMW + genMW) × 1e6 × propEta × √(2 ρ_air A_disk))^(2/3) / 9.81 / 1000` | the inverse of the actuator-disk relation at full bus power | `config.js` `battMW`, `genMW`, `diskM2`, `DEFAULTS.propEta`, `DEFAULTS.rhoAir` |
| `ln2NeedT` | t | `plan.js` → `planCycle` | `min(surplusT × 0.8, ln2CapT)` | 80% of surplus buoyancy is the ballast target | `config.js` `ln2CapT`; the 0.8 is set in `plan.js` |
| `ln2MakeT` | t | `plan.js` → `planCycle` | `min(ln2NeedT, cryoMW × cryoMul × cryoShare × (dur.RETURN_TRANSIT / 60) / eLN2)` | the plant runs only on the return leg | `config.js` `cryoMW`, `DEFAULTS.cryoMul`, `MODES[*].cryoShare`, `DEFAULTS.eLN2` |
| `retainedT` | t | `plan.js` → `planCycle` | `max(0, surplusT − ln2MakeT − rotorMaxT / 0.6)` | rotors carry 60% of the residual, aerodynamic trim the rest | the 0.6 is set in `plan.js` |
| `deliveredT` | t | `plan.js` → `planCycle` | `payloadT − retainedT` | — | — |
| `resid` | t | `plan.js` → `planCycle` | `max(0, surplusT − ln2MakeT − retainedT)` | — | — |
| `downMW` | MW | `plan.js` → `planCycle` | `diskMW(cls, resid × 1000 × 9.81 × 0.6)` | as `retainedT` | — |
| `battLimited` | bool | `plan.js` → `planCycle` | `downMW > (battMW + genMW) × 0.92` | 92% of the bus is the working ceiling | `plan.js` |
| water aboard | t | `state.js` → `stateAt` | fill: `retainedT + deliveredT × prog`; release: `payloadT − deliveredT × (pass fraction)`; elsewhere `retainedT` or `payloadT` | — | `state.js` per-phase blocks |
| `ln2` aboard | t | `state.js` → `stateAt` | return: `ln2MakeT × min(1, prog/0.85)`; decays over approach and fill | — | `state.js` per-phase blocks |

**Ordering matters.** `ln2MakeT` is computed *before* the `battLimited` 1.12 stretch is
applied to `dur.RETURN_TRANSIT`, so the plant is credited with the shorter leg while the
letdown energy is charged over the longer one. On a P-10000 at 15 km that is 21.116 t of
nitrogen from an 8.145-minute leg, not the 23.65 t the 9.122-minute leg would give.

**Known defects.** `retainedT` is exactly zero for every class, every mode, every
distance and every position of every dial the page exposes — the described descent
ballast never exists. `ln2MakeT` is 21.1 t against a 12,050 t surplus and a 5,000 t tank.
See `../docs/PHYSICS.md` §"Defect 4" and §"Defect 5".

---

## Audit index: power

| Quantity | Units | Computed in | Equation | Rests on | Set in |
|---|---|---|---|---|---|
| `pumpMW` | MW | `physics.js` → `pumpMW` | `ρ_w g Q h / η_pump / 1e6`, `ρ_w = 1000` | one lumped efficiency covers pump, hose friction and electrics | `config.js` `DEFAULTS.hoseHead = 250`, `DEFAULTS.pumpEta = 0.75`, `CLASSES[*].fillM3s` |
| `dragMW` | MW | `physics.js` → `dragMW` | `½ ρ_air C_d A v³ / η_prop / 1e6`, `A = π(diaM/2)²`, `v = kph/3.6` | drag referenced to frontal area; cube law in speed | `config.js` `DEFAULTS.Cd = 0.05`, `DEFAULTS.rhoAir = 1.10`, `DEFAULTS.propEta = 0.70` |
| `diskMW` | MW | `physics.js` → `diskMW` | `T^{3/2} / √(2 ρ_air A_disk) / η_prop / 1e6` | ideal actuator-disk induced power **in hover** | `config.js` `CLASSES[*].diskM2`, `DEFAULTS.rhoAir`, `DEFAULTS.propEta` |
| `hotelMW` | MW | `plan.js`, `state.js` | `genMW × 0.02` | baseline load is 2% of generation | `plan.js` and `state.js`, independently |
| `draw.prop` | MW | `state.js` → `stateAt` | `dragMW × k`, `k` = 0.3 approach, 1.0 outbound, 0.4 release, 0.55 return | — | `state.js` per-phase blocks |
| `draw.fans` | MW | `state.js` → `stateAt` | `dragMW × 0.5` release, `× 0.12` escape | — | `state.js` |
| `draw.winch` | MW | `state.js` → `stateAt` | `pumpMW × 0.06` | — | `state.js` |
| `draw.pumps` | MW | `state.js` → `stateAt` | `= plan.pumpMW` during the fill | — | — |
| `draw.cryo` | MW | `state.js` → `stateAt` | `cryoMW × cryoMul × cryoShare`, first 85% of the return leg | — | `config.js`, `MODES[*].cryoShare` |
| `draw.rotors` | MW | `state.js` → `stateAt` | `min((battMW + genMW) × 0.95, diskMW(cls, abs(vert) × (liftT − dryT) × 1000 × 9.81 × share))` | hover disk theory applied at every airspeed | `state.js`, the `hold`/`share` block |
| `gen.solar` | MW | `state.js` → `stateAt` | `solarM2 × 200 / 1e6` | 200 W/m² of hull skin, constant, day and night | `config.js` `CLASSES[*].solarM2`; the 200 is set in `state.js` |
| `gen.regen` | MW | `state.js` → `stateAt` | `eBack / (dur.WATER_FILL / 60)` during the fill | nitrogen returns its energy while water replaces it | — |
| `gs` | km/h | `state.js` → `stateAt` | per-phase profiles; the release needle is the derivative of the eased shuttle | — | `state.js`, the `gs` block |
| `alt` | m AGL | `state.js` → `stateAt` | per-phase profiles between `ALT.source`, `ALT.drop`, `ALT_DROP_TOP` and `altTop` | — | `config.js` `ALT`, `ALT_DROP_TOP`, `VZ_MAX` |
| `altTop` | m AGL | `state.js` → `stateAt` | `min(ALT.cruise, ALT.source + VZ_MAX × 0.30 × 60 × min(dur.OUTBOUND, dur.RETURN))` | a short leg cannot reach the nominal ceiling at a sane climb rate | `config.js` `ALT.cruise = 1500`, `VZ_MAX = 6` |

`ALT.cruise = 1500` is a ceiling, not a cruise altitude. The achieved ceiling is
`300 + 108 × (shorter leg in minutes)` metres and only reaches 1,500 m when the shorter
transit leg exceeds 11.1 minutes. A P-10000 at 15 km tops out at 1,180 m above ground.

---

## Audit index: energy

All from `plan.js` → `planCycle`. `eCryo = ln2MakeT × eLN2` MWh; `eBack = eCryo × rtLN2`.

| Term | Units | Equation | Note |
|---|---|---|---|
| `E.WATER_FILL` | MWh | `max(0, pumpMW × dur.WATER_FILL / 60 − eBack)` | the clamp discards surplus nitrogen credit: 0.32 MWh on a P-100, 0.78 MWh on a P-1000 |
| `E.OUTBOUND_TRANSIT` | MWh | `dragMW × dur.OUTBOUND_TRANSIT / 60` | full ship, full drag |
| `E.RETURN_TRANSIT` | MWh | `dragMW × 0.55 × dur.RETURN_TRANSIT / 60 + eCryo` | lighter ship charged 55% of cruise drag; liquefaction charged here |
| `E.letdown` | MWh | `downMW × min(6, dur.RETURN_TRANSIT × 0.2) / 60` | **the largest term for the P-10000.** See "Defect 3" |
| `E.other` | MWh | `hotelMW × cycleMin / 60 + dragMW × 0.4 × (approach + escape + release) / 60` | — |
| `eCycleMWh` | MWh | sum of the five | the site's "energy per cycle" tile |
| `kwhPerTonne` | kWh/t | `eCycleMWh × 1000 / max(1, deliveredT)` | the site's "per delivered tonne" tile |

The P-10000 at 15 km, balanced, still air:

| Term | MWh | share |
|---|---:|---:|
| `E.letdown` | 43.619 | 52.9% |
| `E.RETURN_TRANSIT` | 14.608 | 17.7% |
| `E.other` | 11.650 | 14.1% |
| `E.OUTBOUND_TRANSIT` | 8.289 | 10.0% |
| `E.WATER_FILL` | 4.332 | 5.3% |
| **total** | **82.498** | |

There is a second, disagreeing energy model. `app/loop.js` integrates
`Σ stateAt().draw − Σ stateAt().gen` in simulated time to drive the storage gauge and the
depletion behaviour. Over the same cycle it spends **211.18 MWh**, 2.56 times what
`planCycle` publishes. Both numbers are on the page at once. See §"Defect 2".

---

## Audit index: selection, routing and targeting

| Decision | Computed in | Rule | Set in |
|---|---|---|---|
| class from fire size | `assign.js` → `sizeTier`, `assign` | tier 0 below 1,000 ha; tier 1 at 1,000 ha or a fire of note; tier 2 at 10,000 ha; +1 tier if "Out of Control" | `assign.js` |
| logistics override | `assign.js` → `assign` | the out-of-control bump is dropped if the bigger ship's water is beyond `max(40 km, 3 × the smaller ship's)` | `assign.js` |
| proximity relaxation | `assign.js` → `assign` | beyond 30 km, accept a body a third the minimum area at a third the distance | `assign.js` |
| which lake | `water.js` → `findSource` | minimise `d / min(12, (areaHa / minSourceHa)^0.35)`, where `d` is distance to the outline's closest point | `water.js`; `config.js` `minSourceHa`, `searchKm` |
| where over the lake | `water.js` → `intakePoint` | principal axis of the outline, station nearest the fire, clamped 20% off each end, then moved to the mid-point of the cross-lake chord and verified inside the polygon | `water.js` |
| drop line geometry | `targets.js` → `dropSeg` | a `dropKm` segment perpendicular to the intake→target bearing, shrunk until both ends are inside the fire | `config.js` `dropKm` |
| which line, in what order | `targets.js` → `planTargets` | `2 cos(align to head fire) + min(2, Σheat/150) + min(3.5, 12 × risk) + jitter`, then a nearest-neighbour chain | `targets.js`; `communities.js` `CITIES` |
| community risk | `targets.js` → `planTargets` | `(3 city / 2 town / 1 village) / max(2, d_km)`, tripled if the fire heads at it, ignored beyond 40 km | `communities.js` |
| per-cycle jitter | `targets.js` → `segAt` | ±(0.30 heat / 0.15 geometric) × line length across, ±0.125 × length along | `targets.js`; `rng.js` `SEED` |
| flown leg length | `targets.js` → `legKmFor` | mean of station→line-head and line-tail→next-station over the rotation | — |
| fleet allocation | **`app/fleet.js`**, not `sim/` | sixteen fixed hulls, largest class first, scored on priority minus distance | `app/fleet.js` `FLEET` |

---

## The assumptions, all of them

`config.js` `DEFAULTS` — the sliders on the concept page write here; `resetConfig()`
restores them.

| Key | Value | Units | Status |
|---|---:|---|---|
| `eLN2` | 0.45 | kWh/kg | assumption. Real air-separation plants sit near 0.4–0.5 kWh/kg for gaseous N₂ and higher for liquid; the page's dial spans 0.30–0.80. |
| `rtLN2` | 0.50 | — | assumption. Electrical round trip of the nitrogen store. Dial spans 0.35–0.60. |
| `hoseHead` | 250 | m | assumption. Sets both the pumping work and the source hover altitude. Dial spans 100–500. |
| `pumpEta` | 0.75 | — | assumption, all-in: pump, hose friction, electrics. Dial spans 0.50–0.90. |
| `propEta` | 0.70 | — | assumption. Applied to drag power *and* to disk power. **No dial.** |
| `Cd` | 0.05 | — | assumption, referenced to frontal area. Equivalent to a volumetric `C_dv` of 0.024, which is a defensible bare-hull figure and charges nothing for rotor installations, fins or the hose pod. Dial spans 0.03–0.12. |
| `rhoAir` | 1.10 | kg/m³ | assumption, labelled "the working band (~1000 m)". Used for drag and every rotor calculation. **No dial.** |
| `rhoSL` | 1.225 | kg/m³ | ISA sea level. Correct as a number; wrong as the buoyancy reference. **No dial.** |
| `speedMul` | 1.0 | — | dial, 0.60–1.40 |
| `fillMul` | 1.0 | — | dial, 0.50–2.00 |
| `cryoMul` | 1.0 | — | dial, 0.50–2.00 |
| `exampleKm` | 15 | km | dial, 3–150 |

`config.js` `CLASSES` — the three vehicles. Every field is a demonstration assumption.
The hull geometries are self-consistent: `(4/3)π(len/2)(dia/2)²` reproduces `dispM3` to
better than 0.4% for all three, at a fineness ratio of 4.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| payload / dry allowance | 100 t | 1,000 t | 10,000 t |
| displacement | 180,000 m³ | 1,800,000 m³ | 18,000,000 m³ |
| length × diameter | 177 × 44 m | 380 × 95 m | 820 × 205 m |
| wetted area (derived) | 19,707 m² | 91,372 m² | 425,477 m² |
| implied areal density | 5.07 kg/m² | 10.94 kg/m² | 23.50 kg/m² |
| cruise | 90 km/h | 110 km/h | 130 km/h |
| fill rate | 0.5 m³/s | 3 m³/s | 15 m³/s |
| generation | 8 MW | 40 MW | 150 MW |
| storage | 20 MWh | 120 MWh | 2,000 MWh |
| bus peak | 30 MW | 150 MW | 1,400 MW |
| cryogenic plant | 6 MW | 30 MW | 100 MW |
| rotors / total disk | 4 / 2,500 m² | 6 / 12,000 m² | 14 / 160,000 m² |
| per-rotor diameter (derived) | 28.2 m | 50.5 m | 120.6 m |

`config.js` `MODES` — three operating postures, applied as multipliers.

| | speed | hose | climb | cryoShare | fixed |
|---|---:|---:|---:|---:|---:|
| rapid | 1.15 | 0.85 | 1.40 | 0.40 | 0.80 |
| balanced | 1.00 | 1.00 | 1.00 | 0.70 | 1.00 |
| endurance | 0.80 | 1.15 | 0.70 | 1.00 | 1.20 |

`climb` is declared and never read. Nothing in `sim/` uses `MODES[*].climb`.

`config.js` altitudes and rates: `ALT = { cruise: 1500, source: 300, drop: 450 }` metres
above ground; `ALT_DROP_TOP = 580`; `VZ_MAX = 6` m/s.

Numbers that are assumptions but do not live in `DEFAULTS`, and so cannot be moved from
the page:

| Value | Where | What it decides |
|---|---|---|
| `200` W/m² | `state.js`, `gen.solar` | all generation the fleet ever has |
| `0.02` | `plan.js`, `state.js` | hotel load as a fraction of `genMW`, written out twice |
| `0.6` | `plan.js`, twice | the rotors' share of residual buoyancy on descent |
| `0.8` | `plan.js` | nitrogen ballast target as a fraction of surplus |
| `0.92` | `plan.js` | the bus ceiling that raises `battLimited` |
| `1.12` | `plan.js` | how much longer an authority-limited return leg takes |
| `0.2` and `min(6, …)` | `plan.js`, `E.letdown` | 53% of the P-10000's published cycle energy |
| `0.55`, `0.4` | `plan.js` | return-leg and manoeuvring drag fractions |
| `1/0.85` | `plan.js` | the trapezoidal-leg ramp factor |
| `0.45` | `plan.js` | drop-run speed as a fraction of cruise |
| `0.12` / `0.60` | `state.js` | rotor share of trim, cruising vs driving the hull down |
| `0.95` | `state.js` | rotor draw ceiling as a fraction of the bus |
| `0.06` | `state.js` | winch power as a fraction of `pumpMW` |
| `0.09` | `mission.js`, `state.js`, `targets.js` | the Bézier bow that makes out and back distinct |

---

## What is *not* in here

- **The storage ledger.** `app/loop.js` integrates the `stateAt` draws to produce the
  storage gauge and the power-exhaustion behaviour. It is model arithmetic living in the
  application, and it uses the second of the two disagreeing energy models.
- **Fleet allocation.** `app/fleet.js` decides which of sixteen hulls goes to which fire.
  `sim/` only knows how to build one mission.
- **The feeds.** `app/feeds.js` fetches and normalises fires, perimeters, satellite heat
  and wind. `sim/` takes them as arguments; `planTargets(m, heat)` is passed its heat
  rather than reading it, so the model runs with no feed at all.
- **A second copy of the assumptions.** `3d/model/config.js` exports its own `ASSUMPTIONS`
  with the same values, because the boundary rule forbids `3d/` importing `sim/`. The two
  agree today and are kept in step by hand.

---

## Known defects

Found by audit, open, tracked, and written up with numbers in `../docs/PHYSICS.md`:

1. **Buoyancy is computed at sea level.** Loaded, at working altitude, all three classes
   are net heavy, which contradicts the page's claim that the rotors only push down.
2. **Two disagreeing power models.** `planCycle` says 82.5 MWh per P-10000 cycle;
   integrating `stateAt` over the same cycle gives 211.2 MWh.
3. **An unexplained window sets the largest energy term.** `min(6, RETURN × 0.2)` in
   `E.letdown` accounts for 52.9% of the P-10000's published cycle energy, and the 6-minute
   cap is inactive below about 55 km one-way, so the number is really the bare 0.2.
4. **Retained descent ballast is always zero.** Deliberately so — the P-10000's disk area
   and bus were sized to make it so, and `selftest.js` enforces it. But the narration, the
   panel copy and one bottleneck label all describe retention as something that happens,
   and none of those branches can be reached. The margin is also thin: a 7.5% cut in bus
   power or propulsive efficiency, or a 14.3% cut in disk area, starts the P-10000
   retaining water.
5. **The cryogenic plant is numerically inert.** 21.1 t of nitrogen against a 12,050 t
   buoyancy surplus and a 5,000 t tank — 0.2% of the stated job — while costing 11.5% of
   the cycle's published energy.
