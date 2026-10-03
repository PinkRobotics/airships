> **2026-10-01 correction: record basis, INFEASIBLE.** The older discussion below is preserved as history. Current force ownership and both bases are in `docs/ENERGY-CLOSURE-2026-10.md`. These are supplied-effort figures, not feasible flights.

| Current quantity | Model value |
|---|---:|
| P100 letdown MWh | 2.296 |
| P100 letdown percent of supplied effort | 28.5 |
| P1000 rotor-only crossing AGL m | 3,000 |
| P1000 letdown clipping min | 5.02 |
| P10000 bag credit percent of supplied effort | 6.9 |
| P10000 bare-bag supplied-effort cost change percent | -6.9 |
| P10000 planned delivery change t (neither flight feasible) | 0.0 |

# What the descent costs — read out of the one model

Until 2026-10-01 this note was the counter-argument. The ledger charged the letdown at an
anchor-assisted power over a window set by two undefined constants, `stateAt` charged it blind
to the anchor, and the two disagreed by 20–30× in the phase the anchor was invented for — so
this file integrated the descent on its own and reported how far the budget was from it.

That budget no longer exists. `sim/power.js` prices every instant of the cycle once
(`drawAt`), `planCycle`'s energy is the integral of it (`integrateCycle`), and `stateAt` shows
the same draw. The letdown is whatever the rotors drew over the descent the ship actually
flies: Glauert momentum theory with the airspeed through the disks and the rate of descent in
the axial term, the surplus read from `ledger` at the altitude the ship is at, the bag's pull
subtracted before the rotors are asked, and the rotors clamped to the bus that is really there.
`docs/ENERGY-MODEL-2026-10.md` publishes every number that moved; `docs/OPEN-QUESTIONS.md` #3,
#14 and #15 record the closure.

So this is no longer an alternative integral. `research/analysis/descent.js` lays out the
model's own descent — the profile the ship flies down, what the rotors are asked for at each
point, what the bus gives them, where the bag comes in — and prices the two counterfactuals
the model exposes switches for: the rotors blind to the bag, and the bag removed. Every number
below is read from `descent.json`; the manifest in `tools/check_analysis.py` holds this prose
to it.

## The result

Worked example, 15 km, balanced:

| | letdown | of the cycle | peak rotor draw | clipped by the bus | rotors, whole cycle |
|---|---|---|---|---|---|
| P-100 | **0.390 MWh** | **19.3%** | 11.8 MW, in the approach | no | 0.620 MWh, 30.7% |
| P-1000 | 4.279 MWh | 23.6% | 146.3 MW, in the approach | **yes — 0.16 min, 0.015 MWh** | 9.432 MWh, 52.0% |
| P-10000 | 35.398 MWh | 20.1% | 1,157.3 MW, in the approach | no | 115.803 MWh, 65.8% |

"Letdown" is the last 28% of the return leg (the descent from the cruise ceiling to the hold
altitude) plus the whole source approach (close the track, stop, sink onto the lake). The
budget used to carry it at 0.012 / 0.161 / 1.420 MWh. It is a fifth of the cycle, and on the
two larger classes the rotors are the largest channel in the budget.

## Where it goes

The expensive part is not the sinking. It is the **stop at the hold altitude before the bag is
in**: the ship slows from cruise to a hover with the bag still stowed, and as the airspeed
through the disks falls the induced power rises — the rotors are holding the whole surplus at
full share (`SHARE_MAX` 0.60) in still air. Ten points through each class's descent, from
`descent.json` `profile`:

**P-100** (hold 430 m AGL, fill 300 m, cable 350 m). Return leg: 1,393 m → 430 m at up to 8.9 m/s
down, rotors 1 → 12 MW as the share schedule ramps and the airspeed falls. Approach: 12 MW at
the stop, falling to 1.3–1.5 MW as the ship sinks at ~2 m/s; the bag is in the water only below
322 m, which is the last tenth of the approach, and it carries 57.4 t of its 125 t when the fill
begins. The rotors never reach the bus ceiling (30 MW battery, 31.5 MW with regen).

**P-1000** (hold 960 m, cable 600 m). At the hold the surplus is 1,215.7 t and the rotors' cap
on the honest bus is 1,107.5 t, so at full share they are asked 155.8 MW against a ceiling of
142.5 MW (return leg, battery alone) and 146.3 MW (approach, battery plus the nitrogen store's
return). That is the clip: **0.16** minutes, 0.015 MWh short, which is what `battLimited` now
means and why the class's headline bottleneck reads `descent authority`. The bag reaches the
water at 431 m, four fifths of the way through the approach; the rotors fall from 27 MW to 1 MW
when it does.

**P-10000** (hold 1,210 m, cable 850 m). The hold altitude is *above* the cruise ceiling
(1,180 m): the "letdown" quarter of the return leg is a 30 m climb at 130 km/h, and the whole
descent happens in the approach. Stopped at 1,210 m the rotors hold 6,995 t at 1,180 MW on a
1,407 MW bus — not clipped, but 84% of the ceiling. The bag goes in between 658 m (half) and
480 m (full), and the rotors drop 217 → 92 → 9 MW.

## Where the rotors stop managing alone, and where the bag can reach

| | cable | bag in the water below | rotors alone fail below | band where neither can hold | hold altitude | bag engages from (plan) |
|---|---|---|---|---|---|---|
| P-100 | 350 m | 322 m AGL | never | — | 430 m | 300 m |
| P-1000 | 600 m | 540 m AGL | **1,450 m AGL** | 910 m | 960 m | 900 m (the cable top) |
| P-10000 | 850 m | 722 m AGL | 1,290 m AGL | 568 m | 1,210 m | 1,150 m (the cable top) |

"Rotors alone fail below" is the highest altitude at which the empty hull's surplus, less the
nitrogen aboard, exceeds what the rotors can hold at full share on the honest bus; below it they
cannot hold the hull by themselves. For the two larger classes that altitude is above the cable
top, so there is a band — 910 m and 568 m of it — where neither the rotors at full share nor the
bag can hold the ship. The model flies through that band because its hold schedule hands
everything above the rotors' share to aero trim, including when the ship is stopped. That
assumption is older than this change and it is the largest lever left on the rotor channel; it
is named under "what remains" below, not settled here.

## The bag, priced two ways

*Blind.* The same flight with the rotors asked to hold the whole surplus as if the bag were not
pulling — what `stateAt` did until this change (OPEN-QUESTIONS #14):

| | letdown, blind | letdown, credited | the credit is worth |
|---|---|---|---|
| P-100 | 0.393 MWh | 0.390 MWh | 0.014 MWh, 0.7% of the cycle |
| P-1000 | 4.569 MWh | 4.279 MWh | 0.556 MWh, 3.0% |
| P-10000 | 40.393 MWh | 35.398 MWh | 9.588 MWh, **5.2%** |

*Bare.* No bag at all. The plan then keeps lake water aboard as ballast to close the descent,
and the hull is heavier on every phase — cheaper to hold down everywhere, and it delivers less:

| | kept aboard | delivered | cycle with bag → without | per tonne with → without | the bag |
|---|---|---|---|---|---|
| P-100 | 0 t | 100 t | 2.023 → 2.034 MWh | 20.23 → 20.34 kWh/t | saves 0.6%, buys nothing |
| P-1000 | 259.3 t | 740.7 t | 18.149 → 13.576 MWh | 18.15 → 18.33 kWh/t | costs 33.7% of the cycle, 1.0% cheaper per tonne, buys 259.3 t |
| P-10000 | 2,247.9 t | 7,752.1 t | 176.000 → 121.950 MWh | 17.60 → 15.73 kWh/t | costs 44.3% of the cycle and **11.9%** per tonne, buys **2,247.9 t** |

That is the honest statement of what the anchor is for. The earlier version of this note said
the bag saved 27.6% and 49.2% of the letdown on the two larger classes; the test suite carried
the same claim. Under one model the bag's effect on the energy is a few percent and of either
sign — what it buys is water. On the P-10000 it buys 2,248 t a cycle at 11.9% more energy per
tonne delivered; on the P-1000 it buys 259 t at no cost per tonne; on the P-100 it is a 0.6%
saving on a descent the rotors manage alone.

The hoist is what it always was — `m g h / η` for 15 m at 5 m/s — now priced as winch power in
the integral: 0.003 / 0.059 / 0.596 MWh. The P-100 figure is half the formula's 0.006 because its
bag is only half in the water when the fill begins.

## What the earlier note got right, and what it got wrong

Right, and now in the model: the cable does not reach for most of the descent; `diskMW` was
hover theory and the descent is the axial case; the letdown was carried at a small fraction of
its size. Right, and still open: the flat `CFG.rhoAir` for every rotor calculation; the 0.6
share. Wrong: the "honest integral" of 0.634 / 6.952 / 42.245 MWh was itself blind to forward
flight, to the hold before the bag goes in, and to the bus; and "the bag saves 27–49%" was a
statement about a bag the rotors had been asked to ignore.

The disc area, OPEN-QUESTIONS #8: it was retired as inert when ±20% moved the cycle by ∓0.4%,
and the earlier note argued that measurement was taken against a letdown too small to see it.
It was. With the rotors priced over the whole flight, ±20% on `diskM2` now moves the P-10000
cycle by +9.6% / −5.8% (`research/figures.json`, `sensitivity.diskM2`). The rotors are for the
descent, and they are now the largest channel in the budget.

## What remains

1. **The share schedule.** `sim/power.js` hands the rotors 12% of the surplus at cruise, rising
   to 60% at the stop, and aero trim the rest — including 40% of the surplus with the ship
   stopped. No derivation supports that; it is the pre-existing assumption that lets the model
   fly through the band above. Removing it multiplies the rotor channel by up to 1/0.6^1.5.
2. **The crossing is above the cable.** For the P-1000 and P-10000 the rotors stop managing alone
   1,450 / 1,290 m AGL up, and the bag cannot reach the water until 540 / 722 m. Lengthening the
   cable (the earlier note's suggestion) or lowering the hold would close the band; neither is
   modelled.
3. **The P-10000 holds above its ceiling.** `holdAgl` is the bag's engagement altitude plus
   60 m, which lands above the cruise ceiling; the "letdown" is a climb. Harmless to the energy
   and odd as choreography.
4. `CFG.rhoAir` is a flat 1.10 kg/m³ for every rotor calculation while the descent runs through
   the densest air the ship sees.

## What to verify, and by whom

| question | discipline | what would settle it |
|---|---|---|
| Can aero trim carry 40% of the surplus at zero airspeed? | rotor aerodynamics / flight dynamics | a derivation of the share schedule, or its deletion and the rotors sized for the whole hold |
| Is a long cable with the bag under the hull dynamically stable? | flight dynamics / marine towing | a pendulum and vortex-shedding analysis; deep-tow oceanography is the nearest prior art |
| What does the winch cost at a longer cable and 5 m/s? | mechanisms | a mass and power estimate for the drum and its stowage |
| Is a vertical letdown over the source operationally acceptable? | operations | a trajectory study against real lake geometry and airspace |

None of these is a physics objection. But this entry still makes the concept more expensive
than the site says it is, and it should be carried into the reports at its full size.
