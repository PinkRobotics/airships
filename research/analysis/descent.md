# What the descent actually costs

`docs/OPEN-QUESTIONS.md` #3, #14 and #15 are three entries about one fact: **nobody has priced
the letdown.** The ledger charges it at the anchor-assisted power over a window set by two
undefined constants; `stateAt` charges it with no anchor term at all and over-reads by ~33×;
and the two disagree by 20–30× in the phase the anchor was invented for.

`research/analysis/descent.js` integrates it, in 10 m steps from cruise down to the fill
altitude, using the model's own `ledger` for the surplus at each altitude and its own `diskMW`
for the power to hold it down. It changes exactly two things about the ledger's treatment: it
respects **altitude** — the empty hull's surplus grows **24%** as it falls into denser air,
110.5 t at 2,500 m MSL against 137.4 t at 1,300 m — and it
respects **cable reach**, so the bag only helps where it can physically be in the water.

## The result, and it is not good

| | ledger's letdown | honest integral | understated by | anchor saves | config claims |
|---|---|---|---|---|---|
| P-100 | 0.012 MWh | **0.634 MWh** | **53.8×** | **4.7%** | 96% |
| P-1000 | 0.161 MWh | **6.952 MWh** | **43.2×** | 27.6% | 96% |
| P-10000 | 1.420 MWh | **42.245 MWh** | **29.8×** | 49.2% | 96% |

Cycle energy, corrected for this line alone:

| | published | corrected | change | kWh/tonne |
|---|---|---|---|---|
| P-100 | 1.253 MWh | **1.875 MWh** | +50% | 12.53 → 18.75 |
| P-1000 | 7.399 MWh | **14.190 MWh** | +92% | 7.40 → 14.19 |
| P-10000 | 45.869 MWh | **86.694 MWh** | +89% | 4.59 → 8.67 |

The honest letdown is **34% / 49% / 49%** of the corrected cycle. It is not a small term that
was approximated; it is the largest single item in the budget and it was carried at 1%.

## Why: the cable does not reach for most of the descent

The letdown runs from 1,500 m AGL to the fill altitude at 300 m — 1,200 m of descent, 3.3
minutes. The bag can only be in the water when the ship is within a cable length of the
surface:

| | cable | covers | rotors alone fail below | anchor reaches first? |
|---|---|---|---|---|
| P-100 | 350 m | **4.2%** of the descent | never | n/a |
| P-1000 | 600 m | 25.0% | 540 m AGL | yes |
| P-10000 | 850 m | 45.8% | 760 m AGL | yes |

**The authority argument is sound and the energy argument is not.** In every class the cable
reaches before the rotors run out of thrust, so the ship can always get down — that was the
question `sim/config.js` was answering when it sized `anchorM`, and it answered it correctly.
But the cable was sized to arrive *just in time*, and for 54–96% of the descent the ship is
pushing its own buoyancy down on rotors alone at up to 14 / 202 / 1,747 MW.

**The P-100's anchor is nearly ornamental.** It saves 4.7% of the descent energy — and the
reason is sharper than "a short cable": the letdown *stops at 300 m AGL*, where the ship begins
its fill, so a 350 m cable only has the bag in the water for the last **50 m** of a 1,200 m
descent. 4.2% of the fall, 4.7% of the energy. `sim/config.js` keeps it on that class explicitly
— "not because that class needs holding down but because a bucket is cheaper than thrust
everywhere". On these numbers it is cheaper than thrust for 4% of the way down.

## The constructive half: the cable is the cheap part

Rotor power goes as thrust^1.5, which is why the bag pays superlinearly — and the same
arithmetic says the bag should be in the water for *longer*, not that it should be bigger. The
bag is already sized at 90% of the hold. The cable is not sized at all; it is sized to be just
sufficient.

UHMWPE at a realised 2.0 N/tex and a safety factor of 3:

| | bag pull | cable | as fitted | full-descent cable | extra mass |
|---|---|---|---|---|---|
| P-100 | 1.2 MN | 1.84 kg/m | 350 m, 0.64 t | 1,500 m, 2.76 t | **+2.12 t** |
| P-1000 | 12.3 MN | 18.39 kg/m | 600 m, 11.04 t | 1,500 m, 27.59 t | +16.55 t |
| P-10000 | 121.6 MN | 182.47 kg/m | 850 m, 155.10 t | 1,500 m, 273.71 t | +118.61 t |

**On the reference ship, about 2 tonnes of rope — 2% of the dry allowance — would put the bag
in the water for the whole letdown instead of the last 4% of it.** The cable has to be 1,500 m,
not 1,200: the bag must already be wet at the *top* of the descent, which is 1,500 m AGL. And
the rope figure is the optimistic end of a band — realised UHMWPE rope tenacity falls from
about 2.0 N/tex at small diameters to nearer 1.2 at the sizes a real tether uses, and a
permanently-loaded tether is bound by creep rupture rather than by single-pull break.

Even at the pessimistic end it is a few tonnes, and the saving is most of 0.634 MWh per cycle
against a corrected cycle of 1.875. Nothing else in this project offers that ratio.

There is a condition attached, and it is a real one: **the bag only works over water.** As
modelled the ship descends while flying toward the lake, so a long cable would be dragging a
bag over terrain. Taking this would mean flying the letdown as a vertical descent over the
source instead of a gliding approach — 1,200 m at 6 m/s is 3.3 minutes, which is what the
cycle already budgets, so it costs time only if the geometry forces a detour.

## This reopens #8: the disc area is not inert after all

Checked independently of the model — average surplus over the descent, momentum theory, the
same 0.6 share and 0.70 propulsive efficiency — the P-100's letdown comes out at 0.667 MWh
against the integral's 0.634. The 5% difference is the anchor's last 50 m. The number is
real.

What that hand check exposes is **where the energy goes**. The work actually done against
buoyancy, charged at the same 0.6 thrust share the rotors are charged at, is 0.243 MWh; the
rotors spend 0.634. The difference is induced loss, because a
2,500 m² disc holding 0.73 MN is loaded at 292 N/m² and its induced velocity is 11.5 m/s.
Hovering is expensive, and pushing a buoyant hull down is hovering.

Induced power goes as 1/√A, so:

| disc area | letdown | cycle | change |
|---|---|---|---|
| as built, 2,500 m² | 0.634 MWh | 1.875 MWh | — |
| ×2 | 0.448 MWh | 1.689 MWh | **−9.9%** |
| ×4 | 0.317 MWh | 1.558 MWh | −16.9% |

`OPEN-QUESTIONS` #8 retired `diskM2` as inert on the measurement that ±20% moved cycle energy
by ∓0.4%. **That measurement was taken against a letdown term 53× too small.** With the
letdown at its honest size, disc area is a first-order design variable again, and #8's question
— what are the primary rotors actually for — has an answer it did not have before: they are for
the descent, and they should be sized for it.

## What this analysis is still carrying that it should not

Three things push the same way, and all three make the numbers above **optimistic**:

1. **The 0.6 thrust share.** `plan.js` charges the rotors 60% of the force they are holding,
   with no justification anywhere. It is carried here unchanged so that this integral differs
   from the ledger in altitude and cable reach only. Since power goes as thrust^1.5, removing
   it multiplies every figure above by 1/0.6^1.5 = **2.15×**.
2. **`diskMW` is hover momentum theory.** The rotors move in the direction of their own
   thrust, so this is the axial-climb case, P = T(V + v) with v = −V/2 + √((V/2)² + v_h²), and
   hover theory understates it. Recomputing the integral with the true expression raises it by
   **+29.6% / +20.4% / +24.8%** — the P-100's letdown goes 0.634 → 0.822 MWh.
3. **`CFG.rhoAir` is a flat 1.10 kg/m³** for every rotor calculation, ISA at about 1,107 m,
   while this descent runs from 2,500 m down to 1,300 m. Density is what the disc has to work
   against.

## Where this leaves the anchor

Not where the page currently puts it. The mechanism is real, its authority argument holds, and
it is still the reason the larger classes can descend at all. But "reduces the letdown by 96%"
is a statement about a bag that is in the water for the whole descent, and no class has a cable
long enough for that. **The published figure describes a ship we have not specified.**

The fix is cheap and it is a design change rather than a correction: lengthen the cables, fly
the letdown over the water, and re-derive `E.letdown` as this integral instead of as
`downMW × min(6, RETURN_TRANSIT × 0.2)`.

## What to verify, and by whom

| question | discipline | what would settle it |
|---|---|---|
| Is a 1,200 m cable with a 125 t bag under a 190 m hull dynamically stable? | flight dynamics / marine towing | a pendulum and vortex-shedding analysis; deep-tow oceanography is the nearest prior art |
| What does the winch cost at 1,200 m and 5 m/s? | mechanisms | a mass and power estimate for the drum and its cable stowage |
| Is a vertical letdown over the source operationally acceptable? | operations | trajectory study against real lake geometry and airspace |
| Is the 0.6 thrust share defensible at all? | rotor aerodynamics | a derivation, or its deletion |

None of these is a physics objection either. But unlike the rest of this analysis folder, this
entry makes the concept **worse**, and it should be carried into the reports at its full size
before anyone is asked to believe the rest.
