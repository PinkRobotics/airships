# airships

A browser simulation of a fleet of imagined water-carrying airships working the wildfires that
are actually burning in British Columbia right now: the fire data is live and real, the aircraft
are not and no such aircraft exists. It is not a design, a proposal or a validated model — it is
first-order arithmetic on stated assumptions, published in full so the arithmetic can be checked
and, where it is wrong, corrected.

Live: **<https://pinkrobotics.ca/airships/>** — the monitor. Also
[how it works](https://pinkrobotics.ca/airships/concept/), the
[3D viewer that walks the ship joint by joint](https://pinkrobotics.ca/airships/ship/),
the [vacuum cell explainer](https://pinkrobotics.ca/airships/cell/),
and the [3D model lab](https://pinkrobotics.ca/airships/model-lab/).

## Run it yourself

```sh
python3 -m http.server 8875        # from the repository root
```

Then open <http://127.0.0.1:8875/>. There is no build step, no bundler, no `package.json` and no
dependency to install: every page is static HTML importing ES modules directly. A fresh clone has
no `data/live/` mirror, so the page uses the dated snapshot in `data/` and states that fact.
Append `?data=snapshot` to pin every model input to the repository, with still air. The default
backdrop is the bundled terrain hillshade. Every browser load stays on the site that served it.

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

**The P-100 is the reference vehicle** — the smallest of the three, 190 m long, which is smaller
than the Hindenburg. The other two are the same arithmetic extrapolated, kept because energy per
tonne falls with size and because we wanted to know what stops you. It is the descent: a large
enough hull cannot push itself back down into the dense air over a lake. Nobody is proposing to
build a P-10000.

| | **P-100** *(reference)* | P-1000 | P-10000 *(limit)* |
|---|---|---|---|
| Payload | 100 t | 1,000 t | 10,000 t |
| Cycle | 34.2 min | 35.4 min | 45.5 min |
| Delivered | 175 t/h | 1,697 t/h | 13,183 t/h |
| Descent anchor | 125 t | 1,250 t | 12,400 t of lake water |
| Retained as ballast | 0 t | 0 t | 0 t |
| Energy | 1.25 MWh/cycle | 7.4 MWh/cycle | 45.9 MWh/cycle |
| Per tonne | 12.5 kWh/t | 7.4 kWh/t | 4.6 kWh/t |
| Binding constraint | transit distance | transit distance | transit distance |

Both energy rows are affected by defects 2 and 3 below, so treat them as the current output of the
code rather than as a claim we stand behind. A drop is a single pass now — the ship flies one long
release rather than three circuits — so `passes` is 1 in every combination of the golden grid.

175 t/h reads modestly beside a very large airtanker's seventy-tonne drop, and it is not the same
quantity: the airtanker's number is one sortie, this one is every hour, through the night. A
twelve-hour day is about 2,100 t against roughly 560 t for eight sorties.

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

All six are DECIDED. One is done: **#1, lift bought at sea level, was fixed on 2026-08-09**
and its numbers are published below. The other five are awaiting implementation, each with a
test that fails on purpose. The decision, its reasoning and its interactions are written up in
[docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md) — what it costs, the options, and a
recommendation. They are open because fixing them means choosing what the vehicle is,
not just correcting a line.

These were found by audit. They are listed here rather than fixed quietly because a model that
hides its faults is worth less than one that publishes them, and the one that is fixed stays on
the list with its old and new numbers for the same reason.

**1. Sea-level lift, 1,500 m cruise — FIXED 2026-08-09.** `ledger()` in `sim/physics.js` computed
displacement lift at `CFG.rhoSL` = 1.225 kg/m³ and used it at every altitude, while the ships cruise
1,500 m above a plateau that is itself around 1,000 m up. Loaded break-even was 1.111 kg/m³, ISA at
1,005 m, so a full P-10000 was 860 t heavy on its drop run and 2,209 t heavy at its ceiling — the
sign of the net force reversed inside one cycle, against a page that says the rotors only ever push
down. `sim/atmosphere.js` now computes ISA density against altitude; `ledger()` takes an altitude in
metres MSL and throws without one; and the hulls were resized to a stricter requirement than the
defect asked for — FAIL-SAFE FLOAT-UP, buoyant at the working altitude while fully loaded with water
it cannot drop. Displacement grew 22.2% to 220,000 / 2.2M / 22M m³, the P-10000 from 820 to 876 m,
and the margin is +5.25% on all three classes. Cruise drag rose 14%.

The same correction has a second half. Lift depends on where the ship IS, and a cycle crosses
1,200 m of atmosphere, so float-up and descent do not share a worst case: float-up is hardest at the
ceiling, descent is hardest down at the lake where the air is 16% denser and the hull is 24% more
buoyant. `planCycle` was checking the descent balance at the ceiling — the easy end. Checked at the
source instead, the two larger classes could not hold themselves down on rotors and had to keep
water back as ballast, costing about 10% of the delivered figure.

Which raised the obvious question: what actually holds a buoyant ship down? Not ballast it has to
carry, make, or keep back. **It borrows the lake.** The larger classes lower a cable with a bag on
it, fill the bag, and winch it just clear of the surface — 12,400 t of water hanging on a line is
12,400 t of downward force, and it costs the 15 m of lift needed to break the surface, or
0.60 MWh.
When the tanks hold more than the shortfall, the bag is dumped back where it came from. It is a
Bambi bucket, the collapsible helicopter bucket in service since 1983, at a scale nobody has built:
the largest ever made is 9,800 litres, so ours is 1,265 times that.

Retention returns to zero and the whole load is delivered. Then the bag turned out to be worth far
more than the shortfall it was built for. Rotor power goes as thrust^1.5, so moving load onto the
lake pays superlinearly: sized to take 90% of the hold rather than the 8% the descent strictly
needed, it cuts `downMW` from 1,748 to 52 MW and the P-10000's cycle from 79.2 to **45.2 MWh** —
4.3 kWh per delivered tonne, against 7.6 before any of this. Every class carries one for that
reason, including the P-100, whose descent closes on rotors alone and which still saves 29%.

Two changes to how the cycle is flown followed from looking at the animation. The drop is **one
run, flown slowly** rather than three passes over the same line — every turn was an 876 m hull
reversing over the fire it was dropping on, the water lands on the same line either way, and the
turns were 4.3 minutes of pure overhead. And the approach now comes to a **dead stop before it
descends**: a bag of several thousand tonnes cannot be dipped from a ship still making 30 km/h.
Nothing yaws while there is line in the water, so the turn onto the outbound track waits until the
pod is clear.

An earlier attempt gave the big hulls 1,350 m hoses so they could fill from altitude and never meet
the dense air; that worked, and cost 29 MWh a cycle in pump work against a 2 m bore and 140 bar at
the pod. A cable is a much better thing to hang than a pipe: 12,400 t is 122 MN, which is about
440 mm of UHMWPE massing 125 t — and that rope is **not** charged as dry mass anywhere yet.

**2. Two power models that disagree by 2.8×.** `planCycle` builds an energy budget from five terms
and reports 90.2 MWh for the sampled P-10000 mission. Integrating `stateAt`'s per-system draw over
the same cycle gives 255.5 MWh. Both are shipped; the page shows the first as the headline energy
figure and the second on the instruments. At least one is wrong and they cannot both be right, and
fixing #1 widened the gap rather than closing it.

**3. An unexplained window still has no derivation, but no longer decides anything.** The letdown
term is `E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60` in `sim/plan.js`, and
neither the 6-minute cap nor the 0.2 fraction has a stated justification. It used to be 45% of the
P-10000's published cycle — an unexplained constant setting the headline number. The descent anchor
did not explain it; it made it small, because rotor power goes as thrust^1.5 and the bag took the
thrust away. It is now 1.4 MWh of 45.2, or 3.1%, and the test that tracked this defect has come off
its known-failure marker. The constants are still unjustified and still worth deleting.

Also, and in the same spirit:

- **Retained descent ballast — FIXED 2026-08-09, and the fix is a bucket.** `retainedT` used to
  be 0 for every class, mode, distance and wind in the grid, while the copy, the `bottleneck`
  string and the narration all described retained ballast as a live constraint. It was not one.
  The cause was an altitude: the balance was struck at the ceiling, where the air is thinnest,
  when the letdown ends 1,200 m lower in air 16% denser. Struck where the descent happens, the
  P-1000 was 49 t short and the P-10000 1,056 t. The descent anchor pays that with lake water on
  a cable instead of with delivered payload, so retention is back to zero — but the mechanism is
  no longer dead code, and a test removes the anchor and watches the water go back in the tanks.
- **The cryogenic plant is numerically inert in the cycle.** For the same reason, `ln2MakeT` never
  changes how much water is delivered; it only moves energy between two terms, at the round-trip
  loss. The copy describes it as load-bearing. Its TANK is load-bearing as of 2026-08-09: at
  155 / 1,550 / 15,500 t it holds enough nitrogen to bring a dead, empty hull down and land it
  with no rotor authority, which takes 2.6 / 5.7 / 12.9 days on solar alone.
- **The generators supply thrust but never energy.** Each class advertises 8/40/150 MW, and
  `rotorMaxT` in `sim/plan.js` spends it when sizing how hard the rotors can push down. Nothing
  credits it as energy: `stateAt` reports only solar and nitrogen recovery, and the loop drains
  the rest from the battery. That generation is the nitrogen plant — expansion of what was
  liquefied earlier — so it is storage rather than a source, and modelling it honestly should
  make the deficit *larger*, not close it. Today it is doing neither.

All six are decided and none is implemented yet. The decisions matter as much as the defects,
because two of them are choices about what the vehicle is rather than corrections to arithmetic —
the hull is to be sized for fail-safe float-up when fully loaded, and the nitrogen plant, the
ballast doctrine and the generators all stay and must be made to bind. The reasoning, the options
that were rejected and the order the fixes have to happen in are in
[docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md).

## Layout

```
index.html       the live fleet monitor — markup only; the application is app/main.js
concept/         how it works: class cards, assumption dials, the worked example
ship/            the public 3D viewer that walks the structure from the 0.6 mm print
                 track to the whole ship, and the live model it displays
cell/            the vacuum cell working pages: the flat explainer, blueprint, checks
                 and band calculator
model-lab/       the 3D development lab, where every class, camera and clip can be driven
sim/             THE MODEL. 15 pure ES modules: no DOM, no network, no globals
3d/              the WebGL vehicle library — its own README, tests and scripts
app/             18 modules that turn model output into a page: map, cockpit, feeds, loop
data/            terrain raster, water extract, roads, BC outline, and the pinned snapshot
pipeline/        the Python that generates data/: live.py water.py terrain.py figures.py
tools/           headless JS eval, golden diff, the boundary checker, screenshots
tests/golden/    the dump scripts and the baselines they are compared against
research/        the evidence store: 73 catalogued sources, the notes, and three reports
research/pdf/    the LaTeX build that turns those reports into PDFs — one source, two outputs
```

Two of those deserve a sentence. `research/` holds the sources this project rests on *and* the
nine that contradict it, each with a written note saying what it takes away. `research/pdf/`
builds the reports into print without duplicating a word of them: `tools/md2tex.py` converts the
same Markdown, so a PDF cannot disagree with the report it came from.

```
make check      everything CI checks: boundaries, stamps, figures, goldens, tests, interactions
make pdf        the three report PDFs, into research/pdf/out/
make factsheet  regenerate research/figures.json from the live model
```

The line about `sim/` is a checked claim rather than an aspiration. `make lint` fails if anything
under `sim/` imports outside `sim/` — by `import`, by `export … from` or by `import()` — or names
`document`, `fetch`, `Date`, `localStorage`, `console` or `Math.random`, the last with one
documented exception for the default seed in `sim/rng.js`. The checker has its own test suite,
because a guard nobody guards does not fail when it breaks; it starts passing everything.

## Checking a number without cloning anything

Open <https://pinkrobotics.ca/airships/>, open devtools, and use the `AIRSHIPS` object the page
publishes deliberately for this purpose:

```js
AIRSHIPS.sim.selftest()
// "SELFTEST PASS (19 checks)" — or it throws, naming the assertion that failed

AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P10000, AIRSHIPS.sim.MODES.balanced, 15)
// the whole cycle: durations, energy, delivered tonnes, the binding constraint

AIRSHIPS.sim.ledger(AIRSHIPS.sim.CLASSES.P100, AIRSHIPS.sim.WORK_ALT_MSL)
// {rho: 0.9569, altMslM: 2500, liftT: 210.5, dryT: 100, reserveT: 10.5, surplusT: 110.5}
// the altitude is required: call it without one and it throws rather than assume sea level

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
from Mapzen/AWS Terrain Tiles, and map vectors from pinned Natural Earth v5.1.2.
`pipeline/live.py` mirrors wind hourly and emergency feeds server-side on a timer so that page traffic never multiplies load on emergency
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
  case. The current 4.6–12.5 kWh/t is the number to attack; the comparison should be against real
  suppression logistics, not against nothing.
- **Sustainment.** Every class already runs a per-cycle deficit on these assumptions: solar at
  45 W/m² plus nitrogen recovery does not cover propulsion, pumping and the cryogenic plant, and
  `selftest()` asserts that this stays visibly true. The intended answer is battery tender ships
  swapping charged cells for discharged ones at mechanical speed — named, but deliberately not
  modelled here. If no plausible energy import chain closes the gap at the cycle rates claimed,
  the throughput figures are fiction. A related limit, which we would rather state than hide: a
  hull that runs its storage down may be unable to descend until solar, nitrogen expansion or a
  swap restores it.
- **What arrives.** Tonnes delivered is not fire extinguished. Evidence that 10,000 t released from
  450 m over a convective column arrives as drift rather than as water on fuel would make the
  headline metric the wrong metric.
- **Downwash.** Nothing in this model accounts for what an 876 m hull trimming on rotors 450 m above
  a fire does to the fire's own air. A credible estimate that the downwash spreads more fire than
  the water suppresses would invert the whole idea.
- **Water.** Surface area is used as a proxy for a lake being drawable. Evidence that repeated
  full-payload draws from the mapped bodies are hydrologically, ecologically or legally impossible
  breaks the logistics chain regardless of whether the aircraft flies.

If you have one of these, [CONTRIBUTING.md](CONTRIBUTING.md) explains the one thing we ask: bring
the number you computed and how you computed it.
