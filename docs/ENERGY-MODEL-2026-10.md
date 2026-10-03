> **Dated earlier energy record, superseded by the force ledger.** Its arithmetic comparison remains evidence. These cycles had unowned force and were not demonstrated feasible flights. Current record/favourable figures and requirements are in [ENERGY-CLOSURE-2026-10.md](ENERGY-CLOSURE-2026-10.md).

# The energy model, 2026-10-01 — one model, and every number that moved

Companion data: `research/analysis/energy-model-change.json`, produced by
`node research/analysis/energy-model-change.mjs` from the base commit's `research/figures.json`
and the current one. Every number in this document is read from that file or from
`research/figures.json` and `research/analysis/descent.json`; nothing here is typed. Where this
document and the JSON disagree, the JSON is right and this document is stale.

## What changed

Five entries on `docs/OPEN-QUESTIONS.md` were closed by one change, so that every headline moved
once and the old and new figures could be published together:

- **#2 — two power models that disagreed.** `planCycle` carried a hand-built budget and
  `stateAt` reported an independent per-system draw; on the fixture missions they disagreed by
  1.55× / 2.43× / 3.80× (P-100 / P-1000 / P-10000). Now `sim/power.js → drawAt` prices one
  instant, `integrateCycle` sums it, and that integral IS the budget; `stateAt` reads `drawAt`
  and adds only geometry. The rotor model is Glauert momentum theory with the airspeed through
  the disks and the rate of descent in the axial term.
- **#3 and #15 — the letdown was a window constant.** `E.letdown = downMW × min(6, 0.2 × return)`,
  with `downMW` the bag-assisted residual applied to a descent the bag could not reach most of.
  Gone, with the `0.92` threshold and the `1.12` stretch. The letdown is the rotor energy
  integrated over the flown descent.
- **#14 — the instruments could not see the anchor.** `stateAt` asked the rotors to hold the
  whole surplus while 12,400 t of lake water was already pulling the hull down. The bag is
  subtracted before the rotors are asked.
- **#6 — the generators supplied thrust and no energy.** They are the nitrogen expansion path:
  storage, not a source. Their output is the store's energy, bounded by their rating; the bus
  the rotors are clamped to is the battery plus that return, not the nameplate.

Nothing was tuned. No constant was moved to make the budget and the integral agree; they agree
because they are the same code (within quadrature: worst 0.08% across the 135 golden
combinations at 4,000 samples, test tolerance 0.5%).

## The headline, per class

Worked example: 15 km one way, balanced mode, still air. "Old" is the base commit's
`research/figures.json`; "new" is the regenerated one.

### P-100

| figure | old | new | change | defect |
|---|---:|---:|---:|---|
| MWh per cycle | 1.391 | **2.023** | +45.4% | 2, 3, 6, 14, 15 |
| kWh per tonne delivered | 13.91 | **20.23** | +45.4% | same |
| deficit per cycle, MWh | 1.24 | **1.87** | +50.8% | same |
| hours on battery | 9.2 | **6.1** | −33.7% | same |
| cycles on battery | 16.2 | 10.7 | −34.0% | same |
| peak rotor draw, MW | 0.3 | 11.8 (in the approach) | | 15, 14, 6 |
| letdown, MWh | 0.012 | 0.390 | ×32 | 3, 15 |
| anchor hoist, MWh | 0.006 | 0.003 | | the bag is half in the water when the fill begins |
| rotor capability `rotorCapT`, t | 267.2 | 227.8 | −14.7% | 6 |
| descent bus, MW | 38 | 31.48 | | 6 |
| scan cutoff, m AGL (not engagement) | 300 | 300 | | |
| `battLimited` / bottleneck | false / transit distance | false / transit distance | | |
| cycle minutes / t per hour | 34.2 / 175 | 34.2 / 175 | 0 | |

### P-1000

| figure | old | new | change | defect |
|---|---:|---:|---:|---|
| MWh per cycle | 8.454 | **18.149** | +114.7% | 2, 3, 6, 14, 15 |
| kWh per tonne delivered | 8.45 | **18.15** | +114.8% | same |
| deficit per cycle, MWh | 7.71 | **17.41** | +125.8% | same |
| hours on battery | 9.2 | **4.1** | −55.4% | same |
| cycles on battery | 15.6 | 6.9 | −55.8% | same |
| peak rotor draw, MW | 5.0 | 146.3 (in the approach) | | 15, 14, 6 |
| letdown, MWh | 0.161 | 4.279 | ×27 | 3, 15 |
| anchor hoist, MWh | 0.060 | 0.059 | | |
| rotor capability `rotorCapT`, t | 1,318.1 | 1,107.5 | −16.0% | 6 |
| descent bus, MW | 190 | 154.04 | | 6 |
| scan cutoff, m AGL (not engagement) | 500 | 900 (scan ceiling) | | 6 |
| `battLimited` / bottleneck | false / transit distance | **true / descent authority** | | 3, 6 |
| cycle minutes / t per hour | 35.36 / 1,697 | 35.36 / 1,697 | 0 | |

### P-10000

| figure | old | new | change | defect |
|---|---:|---:|---:|---|
| MWh per cycle | 54.325 | **176.000** | +224.0% | 2, 3, 6, 14, 15 |
| kWh per tonne delivered | 5.43 | **17.60** | +224.1% | same |
| deficit per cycle, MWh | 50.23 | **171.9** | +242.2% | same |
| hours on battery | 30.2 | **8.8** | −70.9% | same |
| cycles on battery | 39.8 | 11.6 | −70.9% | same |
| peak rotor draw, MW | 52.3 | 1,157.3 (in the approach) | | 15, 14, 6 |
| letdown, MWh | 1.420 | 35.398 | ×25 | 3, 15 |
| anchor hoist, MWh | 0.596 | 0.596 | 0 | |
| rotor capability `rotorCapT`, t | 12,666.2 | 11,474.6 | −9.4% | 6 |
| descent bus, MW | 1,550 | 1,406.84 | | 6 |
| scan cutoff, m AGL (not engagement) | 750 | 1,150 (scan ceiling) | | 6 |
| `battLimited` / bottleneck | false / transit distance | false / transit distance | | |
| cycle minutes / t per hour | 45.51 / 13,183 | 45.51 / 13,183 | 0 | |

Durations, delivered tonnes and throughput did not move: they are kinematic, and the `1.12`
stretch that could have moved them never fired at the worked example.

## Where the energy came from — the attribution

The same flown cycle, re-priced with the counterfactual switches `drawAt` exposes, walking from
the old model's assumptions to the new one's. Step 1 is the one model with the OLD physics in it
— hover-priced rotors, blind to the bag, on the nameplate bus — so the difference between step 0
and step 1 is what pricing the hold-down wherever the ship is costs (defects 3 and 15); the
later steps are what each physics correction gives back. The old descent closure (`rotorCapT`,
`anchorFromAglM`) is replicated in the script and asserted equal to the old published values
before any step is taken, and the steps telescope exactly to the published difference.

| step | | P-100 | P-1000 | P-10000 |
|---|---|---:|---:|---:|
| 0 | the old budget as published | 1.391 | 8.454 | 54.325 |
| 1 | one model, hold-down priced over the whole flight (3 + 15) | 2.175 (+56.4%) | 21.592 (+155.4%) | 220.927 (+306.7%) |
| 2 | Glauert: forward flight and axial descent in the rotor model (2) | 2.037 (−10.0%) | 19.449 (−25.3%) | 192.173 (−53.0%) |
| 3 | the anchor credited before the rotors (14) | 2.023 (−1.0%) | 18.693 (−9.0%) | 180.747 (−21.0%) |
| 4 | the honest bus clamp (6) | 2.023 (0) | 18.600 (−1.1%) | 180.747 (0) |
| 5 | the closure struck on the honest bus (6) | **2.023** (0) | **18.149** (−5.3%) | **176.000** (−8.7%) |

Percentages are of the old cycle. Three readings. First, the whole increase is one thing:
charging the rotors for holding the hull down wherever it is held down — at the stop before the
bag goes in, along the drop line as the water leaves, during the fill — instead of for
`min(6, 0.2 × return)` minutes at the bag-assisted residual. Second, every physics correction
is a saving relative to that, and the largest is Glauert: forward flight is much cheaper than
hover, which is what the old `stateAt` had been charging at cruise. Third, the honest bus is
nearly free on the energy side: it binds only on the P-1000 (step 4), and the closure it changes
(step 5) saves energy because the hold altitude changes and the approach before engagement happens in
thinner air.

## The ledger, old and new

The old ledger had seven lines, three of which (`letdown`, `anchor`, `other`) were not phases.
The new one is the six phases plus `recovery`, and the same integral grouped by channel.

| MWh | P-100 old | P-100 new | P-1000 old | P-1000 new | P-10000 old | P-10000 new |
|---|---:|---:|---:|---:|---:|---:|
| `SOURCE_APPROACH` | — | 0.126 | — | 2.189 | — | 27.323 |
| `WATER_FILL` | 0.109 | 0.143 | 1.090 | 1.779 | 10.900 | 22.176 |
| `OUTBOUND_TRANSIT` | 0.286 | 0.332 | 2.000 | 2.257 | 12.926 | 14.307 |
| `WATER_RELEASE` | — | 0.239 | — | 5.018 | — | 82.045 |
| `BUOYANCY_ESCAPE` | — | 0.021 | — | 0.276 | — | 1.849 |
| `RETURN_TRANSIT` | 0.981 | 1.326 | 4.469 | 7.303 | 16.611 | 30.201 |
| `letdown` (old line) | 0.012 | — | 0.161 | — | 1.420 | — |
| `anchor` (old line) | 0.006 | — | 0.060 | — | 0.596 | — |
| `other` (old line) | 0.162 | — | 1.349 | — | 13.772 | — |
| `recovery` | −0.165 | −0.165 | −0.674 | −0.674 | −1.900 | −1.900 |
| **total** | **1.391** | **2.023** | **8.454** | **18.149** | **54.325** | **176.000** |

| by channel, MWh | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| rotors | 0.620 (30.7%) | 9.432 (52.0%) | 115.803 (65.8%) |
| prop | 0.490 | 3.748 | 29.469 |
| cryo | 0.824 | 3.369 | 9.502 |
| pumps | 0.109 | 1.090 | 10.900 |
| fans | 0.043 | 0.598 | 8.975 |
| hotel | 0.091 | 0.471 | 2.276 |
| winch | 0.011 | 0.115 | 0.975 |

The letdown and the hoist are still reported, as `energy.letdownMWh` (0.390 / 4.279 / 35.398,
which is 19.3 / 23.6 / 20.1% of the cycle) and `energy.anchorHoistMWh` (0.003 / 0.059 / 0.596);
they are slices of the rotor and winch channels, not lines of their own. The old `other` line
has no equivalent.

## The deficit is larger, and in plain words

Solar is unchanged at 45 W/m². The cycle grew, so the deficit grew with it:

| | solar per cycle | spend, old → new | deficit, old → new | hours on battery, old → new |
|---|---:|---:|---:|---:|
| P-100 | 0.154 MWh | 1.391 → 2.023 | 1.24 → **1.87** | 9.2 → **6.1** |
| P-1000 | 0.743 MWh | 8.454 → 18.149 | 7.71 → **17.41** | 9.2 → **4.1** |
| P-10000 | 4.096 MWh | 54.325 → 176.000 | 50.23 → **171.9** | 30.2 → **8.8** |

The open possibility that OPEN-QUESTIONS #6 carried — that the published deficit was an
artefact of leaving the generators out — is closed in the other direction. The generators are
counted now, as what they are: a store that returns a fifth of what the cryo plant spent
liquefying nitrogen (0.165 / 0.674 / 1.900 MWh per cycle), and only when there is nitrogen to
expand. That credit was already in the old ledger as `recovery`. Crediting the generators
honestly adds nothing to the energy side and takes 6.5 / 36 / 143 MW off the bus the rotors
can draw on, which is what clips the P-1000's letdown. The fleet is a battery being spent,
faster than the page said: 6.1, 4.1 and 8.8 hours of work in a full charge.

## The bag's trade

Priced two ways in `research/analysis/descent.json`. *Blind*: the same flight with the rotors
asked to hold the whole surplus as if the bag were not pulling (what `stateAt` did until this
change). *Bare*: no bag, so the plan keeps lake water aboard as ballast to close the descent.

| | credit the bag earns the rotors | without the bag: kept aboard | delivered | cycle | per tonne |
|---|---:|---:|---:|---:|---:|
| P-100 | 0.014 MWh, 0.7% of the cycle | 0 t | 100 t | 2.023 → 2.034 MWh | 20.23 → 20.34 kWh/t |
| P-1000 | 0.556 MWh, 3.0% | 259.3 t | 740.7 t | 18.149 → 13.576 MWh | 18.15 → 18.33 kWh/t |
| P-10000 | 9.588 MWh, 5.2% | 2,247.9 t | 7,752.1 t | 176.000 → 121.950 MWh | 17.60 → 15.73 kWh/t |

What the bag buys is water. On the P-10000 it buys 2,248 t a cycle at 11.9% more energy per
tonne delivered; on the P-1000 it buys 259 t at 1.0% less per tonne; on the P-100 it saves 0.6%
of a descent the rotors manage alone. The earlier claims — "the anchor removes 96% of the rotor
work", "the bag saves 27.6% / 49.2% of the letdown", "fifty-eight to one" — were statements about
a letdown that was mispriced, and they are withdrawn with it.

## The P-1000 reads "descent authority"

On the honest bus the P-1000's rotors can hold 1,107.5 t at full share, and at its hold altitude
(960 m AGL) the empty hull's surplus is 1,215.7 t. The rotors-alone crossing is at 1,450 m AGL;
the bag cannot be in the water above 540 m. So during the approach before the bag goes in the rotors
are asked 155.8 MW against a ceiling of 142.5 MW (battery alone) or 146.3 MW (with the store's
return), and the clamp holds them for **0.16 minutes, 0.015 MWh short**. That is what
`battLimited` means now, and it is why the class's headline bottleneck changed from "transit
distance" to "descent authority". It is ten seconds, and it is real: the model is saying the
P-1000's cable is too short for its hull, which is a finding about the vehicle and not about
the arithmetic. The old `0.92` threshold on the nameplate bus never saw it.

## Mode ordering at 60 km flipped — the eighth time

| P-10000, 60 km | rapid | balanced | endurance | cheapest |
|---|---:|---:|---:|---|
| old pins | 158.0 | 143.1 | 133.4 | endurance |
| new | 306.924 | 302.894 | 317.816 | **balanced** |
| of which rotors | 142.145 | 157.088 | 184.752 | |
| of which prop | 119.789 | 89.574 | 56.302 | |
| of which cryo | 18.886 | 38.009 | 67.873 | |

Endurance mode flies slower and runs more cryo; under one model the slower cruise is more time
holding the hull down and the extra nitrogen buys little hold-down, so it is no longer the
cheapest. The test pins all three.

## Sensitivity, old and new

P-10000 at 15 km, balanced, still air; each constant ±20%; the effect on energy per cycle.
From `research/figures.json` `sensitivity` (old and new side by side in the JSON).

| | old −20% | old +20% | new −20% | new +20% |
|---|---:|---:|---:|---:|
| `propEta` | +15.2% | −10.1% | +21.8% | −12.9% |
| `Cd` | −11.6% | +11.6% | −4.4% | +4.4% |
| `rhoAir` | −11.3% | +11.4% | +5.2% | −1.4% |
| `pumpEta` | +5.0% | −3.3% | +1.6% | −1.1% |
| `hoseMul` | −3.6% | +3.6% | −1.0% | +1.0% |
| `rhoSL` | −2.9% | +23.1% | −35.5% | +45.8% |
| `rtLN2` | +0.7% | −0.7% | +0.2% | −0.2% |
| `eLN2` | 0 | 0 | 0 | 0 |
| `solarWPerM2` | 0 | 0 | 0 | 0 |
| `cruiseKph` | −19.1% | +28.6% | −3.1% | +9.3% |
| `anchorBagT` | +9.9% | −2.5% | +0.7% | −0.3% |
| `fillM3s` | +3.8% | −2.5% | +15.3% | −10.2% |
| `dispM3` | −2.9% | +23.1% | −35.5% | +45.8% |
| `diskM2` | +0.3% | −0.2% | +9.6% | −5.8% |
| `battMW` | 0 | 0 | −0.1% | +2.3% |
| `solarM2` | 0 | 0 | 0 | 0 |
| `oneWayKm` | −11.0% | +11.0% | −4.7% | +5.5% |
| `dropKm` | 0 | 0 | +1.7% | −1.7% |

The table is about buoyancy now: `rhoSL` and `dispM3` (a product in the model) are the top lever,
because every tonne of surplus is held down by rotors somewhere in the cycle and rotor power goes
as thrust^1.5. `diskM2` and `battMW` — retired as inert by OPEN-QUESTIONS #8 — are alive again.
`rhoAir` changed sign: thinner air costs energy, because induced power goes as 1/√ρ and the
rotors now outweigh the drag that goes as ρ. `anchorBagT` fell from the second most powerful lever
to a rounding error. `docs/PHYSICS.md` §10 discusses the rest.

## What did not move

Cycle minutes, delivered tonnes and t/h (kinematic). Solar. The nitrogen return (`eBack`):
the generators' rating does not bind at 15 km, so the credit is the whole store at a 20% round
trip, exactly as before; it binds on long endurance legs, where the test shows the store
returning at `genMW` for the whole fill. The anchor hoist on the two larger classes.

## How this was verified

The checks below were run on this change.

- `node tests/node/run.mjs` — `harness: 221 passed, 0 failed, 1 known-failing across 43 suites`
  (the known-failing is the pre-existing `windUsed` flag, unrelated). The two `knownFail`
  markers that recorded #2 and #3 are gone; their suites assert the fixed behaviour.
- `python3 tests/browser/run.py` — the same 221 in the browser.
- `python3 tests/golden/check.py` — IDENTICAL on both baselines after re-recording.
- `/usr/bin/grep -rn 'Math.min(6' sim/` — prints nothing; a test fails if a window returns.
- `python3 tools/check_figures_fresh.py` — `figures.json matches the live model (299 figures)`.
- `node research/analysis/energy-model-change.mjs` — the attribution above, telescoping
  exactly, with the old closure replicated and checked against the old figures.

## Where the old numbers still stand

The reports under `research/reports/` cite the old figures by `<!-- f:… -->` marker
(`tools/check_figures.py` lists every stale or dangling one — 85 lines at the time of writing,
including the retired `energy.ledgerMWh.letdown / anchor / other` keys), the PDF charts read the
old ledger keys, and `README.md` and `research/evidence-map.md` quote the selftest at 19 checks
where it now has 20. Those are updated separately from this change, so that this one moves
every model number exactly once.

Correction to the earlier-model explanation: physical engagement remained about 540.5 m and 722 m AGL on the two larger classes. The 500 → 900 / 750 → 1,150 m quantities were scan cutoffs, not cable tops or higher water contact.
