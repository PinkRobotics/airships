> **2026-10-01 correction:** `power.js` now returns named vertical owners, limits, `unheldT`, basis and feasibility. `planCycle(cls, mode, km, wind, {basis})` uses a fifth options argument; default is record. `requirements.js` computes explicit ballast and power/thrust requirements. The older audit index below is historical where it names hold/share or a 95% bus allocation; use `docs/PHYSICS.md` §§7 and 9 and the generated `docs/ENERGY-CLOSURE-2026-10.md` for the current equations and numbers.

# `sim/` — the model, and an index to every number it publishes

This directory is the entire simulation. Sixteen ES modules, no DOM, no network, no wall
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
AIRSHIPS.sim.ledger(AIRSHIPS.sim.CLASSES.P10000,
                    AIRSHIPS.sim.WORK_ALT_MSL)                // the mass ledger, at 2,500 m
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
| `config.js` | 335 | Every tunable and every vehicle assumption. Nothing here is measured. |
| `atmosphere.js` | 99 | Air density against altitude. ISA troposphere, constants sourced. |
| `physics.js` | 41 | The four first-order relations: pump, drag, actuator disk, mass ledger. |
| `power.js` | 434 | `drawAt` — every channel's draw at one instant, the bus, the nitrogen return, the anchor; `integrateCycle` — the budget as the integral of it. |
| `plan.js` | 220 | `planCycle` — phase durations, water delivered, the descent closure, energy per cycle (from `power.js`). |
| `state.js` | 211 | `stateAt` — where a ship is and what it is doing at one moment; the draw is `power.js`'s. |
| `mission.js` | 83 | Assembling a fire, a source, a plan and a set of drop lines. |
| `assign.js` | 68 | Which class a fire gets, and the logistics override. |
| `water.js` | 129 | Choosing a lake; choosing where over the lake to hover. |
| `targets.js` | 196 | Candidate drop lines, scoring, sequencing, per-cycle jitter. |
| `communities.js` | 43 | Populated places, as a physical input to target scoring. |
| `geo.js` | 60 | Distance, bearing, Bézier paths, easing. |
| `rng.js` | 30 | The seed and the stable hash. |
| `narrate.js` | 53 | The mission trace in prose. |
| `format.js` | 17 | Number and unit formatting (en-CA). |
| `selftest.js` | 134 | Twenty assertions, shipped so a reader can run them. |
| `index.js` | 60 | The single import surface. |

Units are SI internally — kg, m, s, N, W — surfaced as tonnes, kilometres, minutes,
megawatts and megawatt-hours. One tonne of water is one cubic metre.

---

## Audit index: mass and lift

| Quantity | Units | Computed in | Equation | Rests on | Set in |
|---|---|---|---|---|---|
| `rho` | kg/m³ | `atmosphere.js` → `airDensity` | ISA troposphere, anchored at `CFG.rhoSL` | ISO 2533:1975 | `atmosphere.js` `ISA`, `DEFAULTS.rhoSL = 1.225` |
| `liftT` | t | `physics.js` → `ledger` | `dispM3 × airDensity(altMslM, rhoSL) / 1000` | air displaced **at the altitude passed in**; there is no default | `config.js` `CLASSES[*].dispM3`, `TERRAIN_MSL`, `WORK_ALT_MSL` |
| `dryT` | t | `physics.js` → `ledger` | `= payloadT` | structure, machinery, batteries and plant together weigh exactly one payload | `config.js` `CLASSES[*].payloadT` |
| `surplusT` | t | `physics.js` → `ledger` | `liftT − dryT` | both of the above | as above |
| `reserveT` (ledger) | t | `physics.js` → `ledger` | `liftT − dryT − payloadT` | both of the above | as above |
| `massT` | t | `power.js` → `drawAt` | `dryT + water + ln2` | the ledger; the phase's water and nitrogen curves (`power.js → loadAt`) | `state.js` per-phase blocks |
| `buoyN` | N | `state.js` → `stateAt` | `liftT × 1000 × 9.81` | `liftT` | — |
| `weightN` | N | `state.js` → `stateAt` | `massT × 1000 × 9.81` | `massT` | — |
| `netN` | N | `state.js` → `stateAt` | `buoyN − weightN` | both | — |
| `netFrac` | — | `state.js` → `stateAt` | `clamp₀¹((liftT − massT) / (liftT − dryT))` | the ledger | — |
| `vert` | — | `state.js` → `stateAt` | `−hold × netFrac`; `hold` is a per-phase curve | the ledger; the phase curves | `state.js`, the `hold`/`share` block |

**Trap.** Two different quantities are called *reserve*. `ledger().reserveT` is
`liftT − dryT − payloadT` (10.5 t on a P-100 at its working altitude) and is what the concept
page prints. The local `reserveT` inside `stateAt` is `liftT − dryT` (110.5 t at the same
altitude, 137.4 t over the lake) and is the denominator of `netFrac` and the scale of every
rotor thrust. They differ by one payload, and both now depend on where the ship is.

**Where each caller evaluates it.** `planCycle` uses `WORK_ALT_MSL` = 2,500 m, the thinnest
air of the cycle, and publishes that as `plan.led`. `stateAt` uses `TERRAIN_MSL + alt` at
every instant, so `liftT`, `surplusT`, `netFrac`, `buoyN` and every rotor draw move through
the cycle: a P-100 displaces 237 t over the lake and 211 t at its ceiling. The two differ on
purpose and `plan.led` is the design point, not the instantaneous truth.

**Fixed defect, 2026-08-09.** `ledger` used to evaluate at `rhoSL` and hand the answer to
every altitude, which made all three classes net heavy wherever they actually flew. It now
takes an altitude and throws without one, and the hulls were resized so that lift at the
working altitude covers dry mass plus a full payload with 5.25% to spare. See
`../docs/PHYSICS.md` §"Defect 1" and `../docs/OPEN-QUESTIONS.md` #0.

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
| `dur.RETURN_TRANSIT` | min | `max(1.2, oneWayKm / gsRet × 60 × rampF)` | as outbound; the authority-limited `× 1.12` stretch is gone since 2026-10-01 — a slower letdown costs more, not less | `plan.js` |
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
| `busMW` | MW | `power.js` → `descentBusMW` | `battMW + min(genMW, regenMW(approach))` | the battery plus what the nitrogen store returns while the approach vents — not the nameplate | `config.js` `battMW`, `genMW`; `power.js` `VENT_APPROACH` |
| `rotorMaxT` | t | `power.js` → `rotorMaxTonnes` | `(BUS_CEILING × busMW × 1e6 × propEta × √(2 ρ_air A_disk))^(2/3) / 9.81 / 1000` | the inverse of the actuator-disk relation at the working ceiling of the honest bus — the same clamp `drawAt` enforces | `config.js` `diskM2`, `DEFAULTS.propEta`, `DEFAULTS.rhoAir`; `power.js` `BUS_CEILING = 0.95` |
| `ln2NeedT` | t | `plan.js` → `planCycle` | `min(surplusT × 0.8, ln2CapT)` | 80% of surplus buoyancy is the ballast target; `surplusT` is now the surplus at 2,500 m | `config.js` `ln2CapT`; the 0.8 is set in `plan.js` |
| `ln2MakeT` | t | `plan.js` → `planCycle` | `min(ln2NeedT, cryoMW × cryoMul × cryoShare × (dur.RETURN_TRANSIT / 60) / eLN2)` | the plant runs only on the return leg | `config.js` `cryoMW`, `DEFAULTS.cryoMul`, `MODES[*].cryoShare`, `DEFAULTS.eLN2` |
| `holdT` | t | `plan.js` → `planCycle` | `max(0, surplusT at the source − ln2MakeT)` | everything the ship must hold down at the lake | — |
| `anchorT` | t | `plan.js` → `planCycle` | `min(anchorBagT, holdT)` | the bag goes first and takes all it will hold; it cannot exceed the surplus that lifts it | `config.js` `anchorBagT` |
| `anchorFromAglM` | m AGL | `plan.js` → `planCycle` | scanned up from the fill altitude in 10 m steps as far as the cable reaches: the highest altitude where `surplus − ln2MakeT > rotorMaxT / SHARE_MAX`; the scan ceiling when the crossing is above it (not physical cable reach) | below it the rotors cannot hold the hull alone, so the transit levels off 60 m above it (`power.js → cycleGeometry`, `holdAgl`) | `config.js` `anchorM`; `power.js` `SHARE_MAX = 0.60` |
| `shortfallT` | t | `plan.js` → `planCycle` | `max(0, holdT − anchorT − rotorMaxT / SHARE_MAX)` | what neither the rotors at full share nor the bag can hold | — |
| `retainedT` | t | `plan.js` → `planCycle` | `min(payloadT, shortfallT)` | rotors first, then the bag, then retention — zero on the shipped numbers | — |
| `deliveredT` | t | `plan.js` → `planCycle` | `payloadT − retainedT` | — | — |
| `downMW` | MW | `power.js` → `integrateCycle` | `max_t draw.rotors` over the flown cycle, with `downMWPhase` | the rotors' peak draw, not a hold-down estimate | — |
| `battLimited` | bool | `plan.js` → `planCycle` | `letdownClipMin > 0` | the bus clamp held the rotors below what the hold asked for at some point in the letdown | `power.js` `BUS_CEILING`, `LETDOWN_FROM` |
| water aboard | t | `power.js` → `loadAt` | fill: `retainedT + deliveredT × prog`; release: `payloadT − deliveredT × (pass fraction)`; elsewhere `retainedT` or `payloadT` | — | `power.js` per-phase blocks |
| `ln2` aboard | t | `power.js` → `loadAt` | return: `ln2MakeT × min(1, prog / cryoOnFrac)`; the approach vents `VENT_APPROACH` (30%) of it, the fill the rest | what is vented is what the generators return as `gen.regen` | `power.js` `VENT_APPROACH` |

**The plant and the leg agree by construction.** `ln2MakeT` is computed from the kinematic
return leg, and `power.js → drawAt` runs the plant for `cryoOnFrac` of that same leg — the
fraction that makes exactly `ln2MakeT`, which is 1 on every combination checked because the
plant is capacity-bound — so the tonnes credited and the energy charged are the same 21.1 t on
a P-10000 at 15 km. Until 2026-10-01 the plant was credited with a shorter leg than the letdown
was billed over.

**Known defects.** `retainedT` is exactly zero for every class, every mode, every
distance and every position of every dial the page exposes — the described descent
ballast never exists, and the 2026-08-09 resize widened the margin rather than closing it.
`ln2MakeT` is 21.1 t against an 11,051 t surplus and a 15,500 t tank. See
`../docs/PHYSICS.md` §"Defect 4" and §"Defect 5". The tank is no longer arbitrary: it is
sized so an empty hull can be made heavy enough to LAND with no rotor authority, which is a
job the plant does over days rather than over a cycle.

---

## Audit index: power

Since 2026-10-01 every instantaneous draw is priced in one place, `power.js → drawAt(cls, mode,
plan, phase, prog)`, and `state.js → stateAt` only adds geometry to it. `plan.js` integrates the
same function (`power.js → integrateCycle`, 96 midpoint steps per phase) to make the budget.

| Quantity | Units | Computed in | Equation | Rests on | Set in |
|---|---|---|---|---|---|
| `pumpMW` | MW | `physics.js` → `pumpMW` | `ρ_w g Q h / η_pump / 1e6`, `ρ_w = 1000` | one lumped efficiency covers pump, hose friction and electrics | `config.js` `CLASSES[*].hoseM` (300/1,100/1,350 m) × `DEFAULTS.hoseMul = 1`, `DEFAULTS.pumpEta = 0.75`, `CLASSES[*].fillM3s` |
| `dragMW` | MW | `physics.js` → `dragMW` | `½ ρ_air C_d A v³ / η_prop / 1e6`, `A = π(diaM/2)²`, `v = kph/3.6` | drag referenced to frontal area; cube law in speed | `config.js` `DEFAULTS.Cd = 0.05`, `DEFAULTS.rhoAir = 1.10`, `DEFAULTS.propEta = 0.70` |
| `diskMW` | MW | `physics.js` → `diskMW` | `T^{3/2} / √(2 ρ_air A_disk) / η_prop / 1e6` | ideal actuator-disk induced power **in hover**; the still-air limit of `inducedMW` | `config.js` `CLASSES[*].diskM2`, `DEFAULTS.rhoAir`, `DEFAULTS.propEta` |
| `inducedMW` | MW | `power.js` → `inducedMW` | Glauert: `v_i √(V² + (v_c + v_i)²) = T / 2ρA`, solved by bisection; `P = T (v_c + v_i) / η_prop` | momentum theory in forward flight and axial descent; `V` = airspeed through the disks, `v_c = max(0, −v_z)`; a climb is priced as level | the same |
| `draw.hotel` | MW | `power.js` → `drawAt` | `genMW × HOTEL_FRAC` (0.02) | baseline load is 2% of generation | `power.js` |
| `draw.prop` | MW | `power.js` → `drawAt` | `dragMW × k`, `k` = 0.3 approach, 1.0 outbound, 0.4 release, 0.55 return | — | `power.js` per-phase blocks |
| `draw.fans` | MW | `power.js` → `drawAt` | `dragMW × 0.5` release, `× 0.05` escape (trim only: the climb is bought with buoyancy) | — | `power.js` |
| `draw.winch` | MW | `power.js` → `drawAt` | `pumpMW × WINCH_IDLE_FRAC` (0.06) through the approach (cable out) and the first 18% of the outbound leg (hose winding up), plus the hoist `Δm_bag g × HOIST_M / WINCH_ETA` spread over `HOIST_M / WINCH_MPS` seconds as the bag breaks the surface | the hoist is a 3 s pulse at the winch speed, not a step | `power.js` `HOIST_M = 15`, `WINCH_ETA = 0.85`, `WINCH_MPS = 5` |
| `draw.pumps` | MW | `power.js` → `drawAt` | `= plan.pumpMW` during the fill | — | — |
| `draw.cryo` | MW | `power.js` → `drawAt` | `cryoMW × cryoMul × cryoShare` for the first `cryoOnFrac` of the return leg, `cryoOnFrac = min(1, ln2MakeT × eLN2 / (cryoCapMW × t_return))` | the plant's integral equals the plan's `eCryo` exactly; the fraction is 1 on every combination checked, because the plant is capacity-bound (`cryoLimited`) | `config.js`, `MODES[*].cryoShare` |
| `draw.rotors` | MW | `power.js` → `drawAt` | `min(BUS_CEILING × busMW, inducedMW(cls, |vert| × reserveT × g × share, V, v_c))`, `netFrac = (liftT − massT − anchor.tonnes) / reserveT` clamped to [0, 1], `vert = −hold × netFrac` | the bag is subtracted before the rotors are asked; the clamp is to the honest bus | `power.js` `BUS_CEILING = 0.95`, `SHARE_MIN = 0.12`, `SHARE_MAX = 0.60`, the `hold`/`share` block |
| `busMW` | MW | `power.js` → `drawAt` | `battMW + min(genMW, regen)` | the generators are the nitrogen expansion path: storage, not a source | `config.js` `CLASSES[*].battMW`, `genMW` |
| `gen.solar` | MW | `power.js` → `drawAt` | `solarM2 × solarWPerM2 / 1e6` | 45 W/m² of hull skin, constant, day and night | `config.js` `CLASSES[*].solarM2`, `DEFAULTS.solarWPerM2` |
| `gen.regen` | MW | `power.js` → `regenMW` | `min(genMW, ventTph × eLN2 × rtLN2)`; the store vents 30% in the approach and 70% in the fill | nitrogen returns its energy while water replaces it, at the generators' rating at most | `power.js` `VENT_APPROACH = 0.30` |
| `gs` | km/h | `power.js` → `gsAt` | per-phase profiles; the release needle is the derivative of the eased shuttle | — | `power.js`, the `gs` block |
| `alt` | m AGL | `power.js` → `altAt` | per-phase profiles between `sourceAltM(cls)`, `ALT.drop`, `ALT_DROP_TOP`, `holdAgl` and `altTop` | — | `config.js` `ALT`, `ALT_DROP_TOP`, `VZ_MAX`; `power.js → cycleGeometry` |
| `altTop` | m AGL | `power.js` → `cycleGeometry` | `min(ALT.cruise, sourceAltM(cls) + VZ_MAX × 0.30 × 60 × min(dur.OUTBOUND, dur.RETURN))` | a short leg cannot reach the nominal ceiling at a sane climb rate | `config.js` `ALT.cruise = 1500`, `VZ_MAX = 6`, `CLASSES[*].hoseM` |
| `holdAgl` | m AGL | `power.js` → `cycleGeometry` | `max(sourceAltM + 130, anchorFromAglM + 60)` | the ship stops above where the bag engages; on the P-10000 at 15 km that is above `altTop`, so its "letdown" is a 30 m climb | `power.js` |

**Fixed 2026-10-01.** `gen` still has two entries, and that is now correct: the generators are
the nitrogen expansion path and appear as `gen.regen`, bounded by the store and by `genMW`;
`rotorMaxT` and the bus clamp are computed from `battMW + min(genMW, regen)`, not the nameplate.
See `../docs/PHYSICS.md` §"Defect 6".

`ALT.cruise = 1500` is a ceiling, not a cruise altitude. The achieved ceiling is
`300 + 108 × (shorter leg in minutes)` metres and only reaches 1,500 m when the shorter
transit leg exceeds 11.1 minutes. A P-10000 at 15 km tops out at 1,180 m above ground. The
hulls are nonetheless sized at the full 1,500 m, because a class must be safe at the highest
altitude it is allowed to fly and not only at the one a particular mission reaches.

---

## Audit index: energy

All from `plan.js` → `planCycle`, which calls `power.js → integrateCycle` — the midpoint rule
over `drawAt`, `PLAN_STEPS = 96` per phase. `eCryo = ln2MakeT × eLN2` MWh; `eBack = ∫ gen.regen`,
never more than `eCryo × rtLN2`.

| Term | Units | Equation | Note |
|---|---|---|---|
| `E[phase]` | MWh | `Σ_steps Σ_channels draw × dt` for each of the six phases | the phase ledger; `E.recovery = −eBack` is the seventh line |
| `Echan[channel]` | MWh | the same integral grouped by channel (`hotel`, `prop`, `fans`, `winch`, `pumps`, `cryo`, `rotors`) | the two ledgers sum to the same gross |
| `letdownMWh` | MWh | `∫ draw.rotors` over `SOURCE_APPROACH` and the last `1 − LETDOWN_FROM` (28%) of `RETURN_TRANSIT` | no window; see "Defect 3" |
| `anchorHoistMWh` | MWh | `∫` the hoist pulse in `draw.winch` | `m_bag g × 15 m / 0.85` as the bag fills |
| `downMW` | MW | `max_t draw.rotors`, with `downMWPhase` | the peak over the flown cycle, not a hold-down estimate |
| `letdownClipMin`, `rotorClipMWh` | min, MWh | time and energy the bus clamp held the rotors below the ask during the letdown | `battLimited = letdownClipMin > 0` |
| `eCycleMWh` | MWh | `Σ E` over all seven lines — the six phases plus `recovery`, which is negative | the site's "energy per cycle" tile; the channels sum to `eCycleMWh + eBack`, the gross |
| `kwhPerTonne` | kWh/t | `eCycleMWh × 1000 / max(1, deliveredT)` | the site's "per delivered tonne" tile |

The P-10000 at 15 km, balanced, still air (`research/figures.json`):

| Phase | MWh | share | | Channel | MWh | share |
|---|---:|---:|---|---|---:|---:|
| `WATER_RELEASE` | 82.045 | 46.6% | | rotors | 115.803 | 65.8% |
| `RETURN_TRANSIT` | 30.201 | 17.2% | | prop | 29.469 | 16.7% |
| `SOURCE_APPROACH` | 27.323 | 15.5% | | pumps | 10.900 | 6.2% |
| `WATER_FILL` | 22.176 | 12.6% | | cryo | 9.502 | 5.4% |
| `OUTBOUND_TRANSIT` | 14.307 | 8.1% | | fans | 8.975 | 5.1% |
| `BUOYANCY_ESCAPE` | 1.849 | 1.1% | | hotel | 2.276 | 1.3% |
| recovery | −1.900 | −1.1% | | winch | 0.975 | 0.6% |
| **total** | **176.000** | | | | | |

There is no second energy model. `app/loop.js` integrates `Σ stateAt().draw − Σ stateAt().gen`
in simulated time to drive the storage gauge, and `stateAt` reads `drawAt`, so the gauge drains
at the rate the budget says: integrated over a cycle at 4,000 samples it agrees with
`eCycleMWh` within 0.08% on every golden combination (the test allows 0.5%). Before 2026-10-01
it spent 255.45 MWh against the 90.18 the plan published for the same flight. See §"Defect 2"
and `../docs/ENERGY-MODEL-2026-10.md`.

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
| per-cycle jitter | `targets.js` → `segAt` | ±(0.15 heat / 0.075 geometric) × line length across, ±0.125 × length along; the code writes the across term as a full-width amplitude of 0.30 or 0.15 and takes a signed half of it | `targets.js`; `rng.js` `SEED` |
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
| `hoseMul` | 1 | × | scales every class's hose. The LENGTH is per class (`hoseM`), and it sets the pumping work, the fill altitude and therefore whether the ship must keep ballast. Dial spans 0.4–1.6. |
| `pumpEta` | 0.75 | — | assumption, all-in: pump, hose friction, electrics. Dial spans 0.50–0.90. |
| `propEta` | 0.70 | — | assumption. Applied to drag power *and* to disk power. **No dial.** |
| `Cd` | 0.05 | — | assumption, referenced to frontal area. Equivalent to a volumetric `C_dv` of 0.024, which is a defensible bare-hull figure and charges nothing for rotor installations, fins or the hose pod. Dial spans 0.03–0.12. |
| `rhoAir` | 1.10 | kg/m³ | assumption. Used for drag and every rotor calculation, and it is ISA at about 990 m against a 2,500 m working altitude, so drag is 15% high and induced power 7% low. Defect 2's to fix. **No dial.** |
| `rhoSL` | 1.225 | kg/m³ | ISA sea level. The ANCHOR of the density column `atmosphere.js` scales, not the density anything is weighed in. **No dial.** |
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
| displacement | 220,000 m³ | 2,200,000 m³ | 22,000,000 m³ |
| length × diameter | 190 × 47 m | 404 × 102 m | 876 × 219 m |
| wetted area (derived) | 22,592 m² | 104,349 m² | 485,575 m² |
| implied areal density | 4.43 kg/m² | 9.58 kg/m² | 20.59 kg/m² |
| lift at 2,500 m / loaded mass | 210.5 / 200 t | 2,105 / 2,000 t | 21,051 / 20,000 t |
| cruise | 90 km/h | 110 km/h | 130 km/h |
| fill rate | 0.5 m³/s | 3 m³/s | 15 m³/s |
| generation | 8 MW | 40 MW | 150 MW |
| storage | 20 MWh | 120 MWh | 2,000 MWh |
| bus peak | 30 MW | 150 MW | 1,400 MW |
| cryogenic plant | 6 MW | 30 MW | 100 MW |
| nitrogen tank | 155 t | 1,550 t | 15,500 t |
| rotor units / total disk | 4 / 2,500 m² | 6 / 12,000 m² | 14 / 160,000 m² |
| disc diameter if one per unit (derived) | 28.2 m | 50.5 m | 120.6 m |

Displacement, length and diameter grew 22.2% / 6.9% / 6.9% on 2026-08-09, and the nitrogen
tanks by a factor of about three, when the ledger stopped buying its lift at sea level.
Both are sizing requirements now rather than round numbers: the envelope must float a fully
loaded hull at 2,500 m MSL with 5% to spare, and the tank must hold enough nitrogen to land
an empty one with no rotor authority. `../docs/OPEN-QUESTIONS.md` #0 has the arithmetic.

`rotors` is a count of thrust units, and the model never uses it: only `diskM2` enters
`diskMW`. The derived diameter is therefore what one disc per unit would have to be, not a
dimension anything asserts. `3d/model/config.js` resolves the same disc areas as two
smaller rotors per station — 20 / 36 / 85 m across 4 / 6 / 14 stations — and the two files
disagree about the disc count while agreeing about the area to within 1.8%.

`config.js` `MODES` — three operating postures, applied as multipliers.

| | speed | hose | climb | cryoShare | fixed |
|---|---:|---:|---:|---:|---:|
| rapid | 1.15 | 0.85 | 1.40 | 0.40 | 0.80 |
| balanced | 1.00 | 1.00 | 1.00 | 0.70 | 1.00 |
| endurance | 0.80 | 1.15 | 0.70 | 1.00 | 1.20 |

`climb` is declared and never read. Nothing in `sim/` uses `MODES[*].climb`.

`config.js` altitudes and rates: `ALT = { cruise: 1500, source: 300, drop: 450 }` metres
above ground; `ALT_DROP_TOP = 580`; `VZ_MAX = 6` m/s. And the two that turn those into
altitudes buoyancy can be evaluated at: `TERRAIN_MSL = 1000` m, one reference elevation for
the interior plateau the fleet works over, and `WORK_ALT_MSL = 2500` m, the cruise ceiling
above it and the altitude every hull is sized at.

Numbers that are assumptions but do not live in `DEFAULTS`, and so cannot be moved from
the page:

| Value | Where | What it decides |
|---|---|---|
| `HOTEL_FRAC = 0.02` | `power.js` | hotel load as a fraction of `genMW`, once |
| `SHARE_MIN = 0.12` / `SHARE_MAX = 0.60` | `power.js` | the rotors' share of the surplus, cruising vs driving the hull down; the descent closure uses `SHARE_MAX`; aero trim is assumed to carry the rest, including with the ship stopped |
| `BUS_CEILING = 0.95` | `power.js` | rotor draw ceiling as a fraction of the bus, in the clamp and in the closure |
| `LETDOWN_FROM = 0.72` | `power.js` | where in the return leg the descent to the hold altitude begins |
| `VENT_APPROACH = 0.30` | `power.js` | the share of the nitrogen store vented (and returned through the generators) during the approach; the rest in the fill |
| `HOIST_M = 15`, `WINCH_ETA = 0.85`, `WINCH_MPS = 5` | `power.js` | the hoist that breaks the bag out of the water, and the speed the cable pays out at |
| `WINCH_IDLE_FRAC = 0.06` | `power.js` | winch idling power as a fraction of `pumpMW` |
| `PLAN_STEPS = 96` | `power.js` | midpoint steps per phase in the budget's integral |
| `0.8` | `plan.js` | nitrogen ballast target as a fraction of surplus |
| `0.3`, `1.0`, `0.4`, `0.55`; `0.5`, `0.05` | `power.js` | per-phase propulsion fractions of cruise drag (approach, outbound, release, return) and fan fractions (release, escape) |
| `0.18` | `power.js` | the fraction of the outbound leg the hose is still winding up, with the winch idling |
| `1/0.85` | `plan.js` | the trapezoidal-leg ramp factor |
| `0.45` | `plan.js` | drop-run speed as a fraction of cruise |
| `0.09` | `mission.js`, `state.js`, `targets.js` | the Bézier bow that makes out and back distinct |

---

## What is *not* in here

- **The storage ledger.** `app/loop.js` integrates the `stateAt` draws to produce the
  storage gauge and the power-exhaustion behaviour. It is model arithmetic living in the
  application, but since 2026-10-01 it integrates the same `drawAt` the budget integrates, so
  it cannot disagree with the plan by more than quadrature.
- **Fleet allocation.** `app/fleet.js` decides which of sixteen hulls goes to which fire.
  `sim/` only knows how to build one mission.
- **The feeds.** `app/feeds.js` fetches and normalises fires, perimeters, satellite heat
  and wind. `sim/` takes them as arguments; `planTargets(m, heat)` is passed its heat
  rather than reading it, so the model runs with no feed at all.
- **A second copy of the assumptions.** `3d/model/config.js` exports its own `ASSUMPTIONS`
  with the same values, because the boundary rule forbids `3d/` importing `sim/`. They are
  no longer kept in step by hand: `tests/cases/spec-parity.cases.js` compares every field
  both files claim to know and fails on any difference. It exists because the copies did
  drift once — a P-10000 respec reached `sim/` and only half-reached the 3D copy, leaving
  the model lab computing descent authority from a 650 MW bus while the page used
  1,550 MW — and the drift was found by review rather than by a test. Two fields are
  deliberately excluded and the exclusion carries a written reason: the disc count, which
  the two files resolve differently (see the class table above). `ln2CapT` used to be the
  second exclusion and is compared now — the 2026-08-09 resize gave the tank a requirement
  instead of a round number, so there is one right answer and no reason for two.

---

## Known defects

Found by audit, tracked, and written up with numbers in `../docs/PHYSICS.md`; five of the six are fixed and kept on the list because the numbers they moved are published:

1. ~~**Buoyancy is computed at sea level.**~~ **FIXED 2026-08-09.** `ledger` takes an
   altitude and refuses to guess one; the hulls were resized so every class is 5.25%
   buoyant fully loaded at 2,500 m MSL. Kept on this list because the numbers it moved are
   published: displacement +22.2%, cruise drag +14%, and the P-10000's 15 km cycle from
   82.50 to 75.58 MWh.
2. ~~**Two disagreeing power models.**~~ **FIXED 2026-10-01.** `power.js → drawAt` is the one
   model; `planCycle` integrates it and `stateAt` reads it. The published cycle rose
   1.391 → 2.023, 8.454 → 18.149 and 54.325 → 176.000 MWh at 15 km; every number that moved is
   in `../docs/ENERGY-MODEL-2026-10.md`.
3. ~~**An unexplained window sets the largest energy term.**~~ **FIXED 2026-10-01.** `E.letdown`,
   `min(6, RETURN × 0.2)`, the `0.92` threshold and the `1.12` stretch are gone; `letdownMWh` is
   the rotor energy over the flown descent (0.390 / 4.279 / 35.398 MWh, a fifth of each cycle).
   `battLimited` now means the bus clamp bound during the letdown, which the P-1000's does for
   0.16 min at 15 km.
4. **Retained descent ballast is always zero.** Deliberately so — the P-10000's disk area
   and bus were sized to make it so, and `selftest.js` enforces it. But the narration, the
   panel copy and one bottleneck label all describe retention as something that happens,
   and none of those branches can be reached. The 2026-08-09 resize widened the margin from
   +5% to +15% on the P-10000 rather than closing it, because the surplus is measured in
   thinner air now. Checking the force balance at the BOTTOM of the letdown instead of at
   the ceiling would revive the mechanism on its own, at about 1,050 t retained.
5. **The cryogenic plant is numerically inert in the cycle.** 21.1 t of nitrogen against an
   11,051 t buoyancy surplus and a 15,500 t tank, while costing 5.4% of the cycle's
   published energy (12.6% of the smaller cycle before 2026-10-01). `cryoLimited` is now true for every one of the 135 golden combinations,
   where one used to escape it. The tank itself is no longer arbitrary — it is sized so an
   empty hull can land itself with no rotors, which takes days.
6. ~~**The generators supply thrust but no energy.**~~ **FIXED 2026-10-01.** They are the
   nitrogen expansion path — storage, not a source. `gen.regen` is bounded by the store and by
   `genMW`, the rotor clamp and the descent closure use `battMW + min(genMW, regen)`, `rotorMaxT`
   fell to 136.7 / 664.5 / 6,884.8 t, and the published deficit got larger
   (1.24 / 7.71 / 50.23 → 1.87 / 17.41 / 171.9 MWh per cycle).
