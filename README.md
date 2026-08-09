# airships

A browser simulation of a fleet of imagined water-carrying airships working the wildfires that
are actually burning in British Columbia right now: the fire data is live and real, the aircraft
are not and no such aircraft exists. It is not a design, a proposal or a validated model — it is
first-order arithmetic on stated assumptions, published in full so the arithmetic can be checked
and, where it is wrong, corrected.

Live: **<https://pinkrobotics.ca/airships/>** — the monitor. Also
[how it works](https://pinkrobotics.ca/airships/concept/) and the
[3D model lab](https://pinkrobotics.ca/airships/model-lab/).

## Run it yourself

```sh
python3 -m http.server 8875        # from the repository root
```

Then open <http://127.0.0.1:8875/>. There is no build step, no bundler, no `package.json` and no
dependency to install: every page is static HTML importing ES modules directly. A fresh clone has
no `data/live/` mirror, so the page goes to the public feeds and falls back to the dated snapshot
in `data/` if it cannot reach them. Append `?data=snapshot` to take every model input from files in
the repository instead; the only thing still fetched then is the satellite basemap, which is a
layer you can switch off.

## Where the arithmetic is

Every physical figure the site publishes is computed in `sim/`, which is fifteen ES modules with no
DOM, no network, no wall clock and no globals. Nothing outside `sim/` recomputes one. The single
modelling decision that lives in `app/` is which of the sixteen hulls is sent to which fire, because
that depends on the live fire list rather than on physics.

| Published quantity | Computed by | File |
|---|---|---|
| Water delivered per hour (t/h) | `planCycle(cls, mode, oneWayKm, wind).tph` | `sim/plan.js` |
| Minutes per delivery cycle, and per phase | `planCycle(...).cycleMin`, `.dur` | `sim/plan.js` |
| Drops per hour | `planCycle(...).dropsPerHour` | `sim/plan.js` |
| Energy per cycle (MWh) | `planCycle(...).eCycleMWh` | `sim/plan.js` |
| Energy per delivered tonne (kWh/t) | `planCycle(...).kwhPerTonne` | `sim/plan.js` |
| Drop-pass count | `planCycle(...).passes` | `sim/plan.js` |
| The binding constraint | `planCycle(...).bottleneck` | `sim/plan.js` |
| Tonnes delivered, tonnes retained as descent ballast | `planCycle(...).deliveredT`, `.retainedT` | `sim/plan.js` |
| Nitrogen liquefied per cycle, and whether the plant is the limit | `planCycle(...).ln2MakeT`, `.cryoLimited` | `sim/plan.js` |
| Ground speed out and back under a live wind | `planCycle(...).gsOut`, `.gsRet`, `.tailOut` | `sim/plan.js` |
| Maximum downward force the rotors can produce | `rotorMaxT`, inside `planCycle` | `sim/plan.js` |
| Pump shaft power (ρgQh/η) | `pumpMW(cls)` | `sim/physics.js` |
| Cruise drag power (½ρCdAv³/η) | `dragMW(cls, mode)` | `sim/physics.js` |
| Rotor power for a demanded thrust (momentum theory) | `diskMW(cls, thrustN)` | `sim/physics.js` |
| Buoyancy ledger: displaced tonnes, structure, reserve, surplus | `ledger(cls)` | `sim/physics.js` |
| Which class of ship a fire gets | `sizeTier(fire)`, `assign(fire, water)` | `sim/assign.js` |
| Which lake or reservoir, and how far away | `findSource(fireLL, cls, water)` | `sim/water.js` |
| Where over that water the hose goes down | `intakePoint(w, fireLL)` | `sim/water.js` |
| The drop line each cycle attacks | `dropSeg`, `planTargets`, `segAt` | `sim/targets.js` |
| The leg actually flown, which the plan is timed on | `legKmFor(m)` | `sim/targets.js` |
| Position, heading, altitude, tank levels, instantaneous draw | `stateAt(m, t)` | `sim/state.js` |
| A whole mission — fire, source, plan, drop lines | `buildMission(fire, water, modeId)` | `sim/mission.js` |
| Which of the sixteen hulls goes where | `FLEET`, `rebuildMissions()` | `app/fleet.js` |
| The prose on a ship's panel | `narrate(m, st)` | `sim/narrate.js` |
| Every assumption, in one file | `DEFAULTS`, `CLASSES`, `MODES` | `sim/config.js` |

On the shipped defaults, balanced mode, 15 km one way, that machinery currently says:

| | P-100 | P-1000 | P-10000 |
|---|---|---|---|
| Payload | 100 t | 1,000 t | 10,000 t |
| Cycle | 36.2 min | 38.9 min | 50.8 min |
| Delivered | 166 t/h | 1,543 t/h | 11,820 t/h |
| Energy | 1.7 MWh/cycle | 11.9 MWh/cycle | 82.5 MWh/cycle |
| Per tonne | 17 kWh/t | 12 kWh/t | 8 kWh/t |
| Binding constraint | transit distance | transit distance | descent authority |

Both energy rows are affected by defects 2 and 3 below, so treat them as the current output of the
code rather than as a claim we stand behind. The pass count is 3 for every one of the 135
class/mode/distance/wind combinations in the golden grid, which means it is not currently doing any
work either.

## Deterministic replay

Two URL parameters make a run exactly reproducible:

- `?seed=N` pins the model's pseudo-random choices — the phase offset each hull starts on, the
  drop-line jitter where a fire has no mapped perimeter. Read in `app/main.js`, applied through
  `setSeed` in `sim/rng.js`; nothing in `sim/` knows a URL exists.
- `?data=snapshot` pins the inputs to the dataset committed to this repository: fires, perimeters
  and satellite heat from `data/snapshot*.json`, and still air, because a wind forecast cannot be
  replayed honestly from a file and replay mode declines to pretend. Read in `app/feeds.js`.

Together they buy three things. A link shows another person exactly what you were looking at. The
golden tests compare numbers rather than screenshots. And the model runs with no feed reachable.

```
http://127.0.0.1:8875/index.html?seed=7&data=snapshot
```

is the run that `tests/golden/seed7-snapshot.json` and `tests/golden/ui-seed7-snapshot.json` were
recorded from. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to reproduce and diff them.

## Known defects

These were found by audit and are open and tracked. They are listed here rather than fixed
quietly because a model that hides its faults is worth less than one that publishes them.

**1. Sea-level lift, 1,500 m cruise.** `ledger()` in `sim/physics.js` computes displacement lift at
`CFG.rhoSL` = 1.225 kg/m³ while the ships cruise at `ALT.cruise` = 1,500 m above ground. Every
class carries a structure allowance equal to its payload, so the all-up mass is exactly twice the
payload and the break-even air density is 1.111 kg/m³ for all three — roughly ISA density at
1,000 m above sea level. At the model's own working-band density (`CFG.rhoAir` = 1.10) the P-100 is
2 t heavy, the P-1000 20 t and the P-10000 200 t, and over BC terrain at 1,500 m AGL the deficit is
larger. That contradicts the page's claim that the rotors only ever push down. Fixing it means the
rotors must hold the hull *up* for part of every cycle, which is a cost the energy figures do not
currently carry.

**2. Two power models that disagree by 2.6×.** `planCycle` builds an energy budget from five terms
and reports 82.5 MWh for a P-10000 cycle at 15 km. Integrating `stateAt`'s per-system draw over the
same cycle gives about 210 MWh. Both are shipped; the page shows the first as the headline energy
figure and the second on the instruments. At least one is wrong and they cannot both be right.

**3. An unexplained window sets more than half the energy.** The letdown term is
`E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60` in `sim/plan.js`. Neither the
6-minute cap nor the 0.2 fraction has a stated justification, and that one line is 53% of the
P-10000's published 82.5 MWh at 15 km, rising to 61% at 45 km. The cap starts to bind beyond about
55 km one way, after which the descent costs essentially the same energy however far the ship flew.

Also, and in the same spirit:

- **Retained descent ballast is zero by construction.** `retainedT` is 0 for every class, mode,
  distance and wind in the golden grid, because `rotorMaxT / 0.6` exceeds the buoyant surplus in
  all three classes. The copy, the `bottleneck` string and the narration all describe retained
  ballast as a live constraint. It is not one.
- **The cryogenic plant is numerically inert.** For the same reason, `ln2MakeT` never changes how
  much water is delivered; it only moves energy between two terms, at the round-trip loss. The
  copy describes it as load-bearing.

## Layout

```
index.html       the live fleet monitor — markup only; the application is app/main.js
concept/         how it works: class cards, assumption dials, the worked example
model-lab/       the 3D development lab, where every class, camera and clip can be driven
sim/             THE MODEL. 15 pure ES modules: no DOM, no network, no globals
3d/              the WebGL vehicle library — its own README, tests and scripts
app/             18 modules that turn model output into a page: map, cockpit, feeds, loop
data/            terrain raster, water extract, roads, BC outline, and the pinned snapshot
pipeline/        the Python that generates data/: live.py water.py terrain.py figures.py
tools/           headless JS eval, golden diff, the boundary checker, screenshots
tests/golden/    the dump scripts and the baselines they are compared against
```

## Checking a number without cloning anything

Open <https://pinkrobotics.ca/airships/>, open devtools, and use the `AIRSHIPS` object the page
publishes deliberately for this purpose:

```js
AIRSHIPS.sim.selftest()
// "SELFTEST PASS (17 checks)" — or it throws, naming the assertion that failed

AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P10000, AIRSHIPS.sim.MODES.balanced, 15)
// the whole cycle: durations, energy, delivered tonnes, the binding constraint

AIRSHIPS.sim.ledger(AIRSHIPS.sim.CLASSES.P100)
// {liftT: 220.5, dryT: 100, reserveT: 20.5, surplusT: 120.5} — defect 1 lives here

AIRSHIPS.sim.CFG            // every tunable, as the page's sliders have left it
AIRSHIPS.app.missions       // the fleet as currently allocated
```

`?selftest=1` runs the same assertions on load and appends the result to the document title.
Arithmetic nobody can re-run is just a claim.

## Data

The wildfire data is real, live and other people's work. Sources, their licences and the exact
queries used are in [DATA-SOURCES.md](DATA-SOURCES.md), which is authoritative; this file does not
restate them. In outline: fire points and perimeters from the BC Wildfire Service, hotspots from
CWFIS, lakes and reservoirs from the BC Freshwater Atlas, 850 hPa winds from Open-Meteo, terrain
from Mapzen/AWS Terrain Tiles, satellite imagery from Esri. `pipeline/live.py` mirrors the
emergency feeds server-side on a timer so that page traffic never multiplies load on emergency
infrastructure — one fetch per interval for the whole site, not one per viewer.

The code licence is in [LICENSE](LICENSE).

## What would change our minds

The concept rests on a small number of load-bearing claims. Each has a result that would sink it,
and we would rather be shown one than not.

- **Shell mass.** The ledger assumes structure mass equals payload mass — that a P-10000 hull
  enclosing 18 million m³ of vacuum weighs 10,000 t. A buckling analysis showing that no plausible
  material and geometry gets the evacuated shell below the mass of the air it displaces would end
  the concept, not amend it. This is the single most likely place for it to be wrong.
- **Lift at altitude.** If defect 1 is fixed honestly and the classes cannot be made net buoyant at
  a working altitude that clears BC terrain, then the aircraft is a helicopter with an expensive
  balloon attached, and the energy argument goes with it.
- **Energy per tonne.** If the honest per-cycle energy — once defects 2 and 3 are resolved — puts
  kWh per delivered tonne above what conventional air tankers and ground crews achieve, there is no
  case. The current 8–17 kWh/t is the number to attack; the comparison should be against real
  suppression logistics, not against nothing.
- **Sustainment.** Every class already runs a per-cycle deficit on these assumptions: solar at
  200 W/m² plus nitrogen recovery does not cover propulsion, pumping and the cryogenic plant, and
  `selftest()` asserts that this stays visibly true. If no plausible energy import chain closes the
  gap at the cycle rates claimed, the throughput figures are fiction.
- **What arrives.** Tonnes delivered is not fire extinguished. Evidence that 10,000 t released from
  450 m over a convective column arrives as drift rather than as water on fuel would make the
  headline metric the wrong metric.
- **Downwash.** Nothing in this model accounts for what an 820 m hull trimming on rotors 450 m above
  a fire does to the fire's own air. A credible estimate that the downwash spreads more fire than
  the water suppresses would invert the whole idea.
- **Water.** Surface area is used as a proxy for a lake being drawable. Evidence that repeated
  full-payload draws from the mapped bodies are hydrologically, ecologically or legally impossible
  breaks the logistics chain regardless of whether the aircraft flies.

If you have one of these, [CONTRIBUTING.md](CONTRIBUTING.md) explains the one thing we ask: bring
the number you computed and how you computed it.
