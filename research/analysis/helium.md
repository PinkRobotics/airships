# Why vacuum, when helium exists?

The question this project keeps being asked, answered with generated numbers. Computed by
`research/analysis/helium.py` from `vacuum-cell.json`'s structure figures and the US Standard
Atmosphere; market figures carry their sources in the script, USGS Mineral Commodity
Summaries being public-domain primary data (stored in `research/papers/`, notes in
`research/notes/helium-and-hydrogen.md`).

> **The decision is vacuum. This page exists so the decision is never argued from a false
> premise.** A vacuum cell does not beat a gas envelope on lift — a perfect massless vacuum
> shell out-lifts pure hydrogen by only 7.5%, so any structure heavier than 0.067 kg/m³
> loses the pure-lift comparison, and even the deepest hierarchy level is six times that.
> The reasons to build vacuum are the mission's, not the aerostatics': **no feedstock at
> all** in a fleet whose gas bill would move the market it depends on; **no gas logistics
> tail** at remote fire bases, for decades; **crush-safe, fixed displacement** in the one
> place an envelope is at its worst — the convective column over a fire; and **the cell
> array is the airframe**, a trade no envelope can make. The challenge those benefits set
> is structural, it is priced below honestly, and the path to it is the rest of this
> repository.

## The gas ledger

At 2,500 m (air 0.9569 kg/m³), net lift per m³ before any airframe:

| architecture | gas | structure | net |
|---|---|---|---|
| vacuum, ideal massless shell | 0 | 0 | +0.957 |
| vacuum, single-level lattice (demonstrable) | 0 | 1.306 | **-0.349** |
| vacuum, level-2 hierarchy (the target) | 0 | 0.538 | +0.419 |
| hydrogen, pure | 0.067 | envelope extra | +0.890 |
| helium, pure | 0.132 | envelope extra | +0.825 |
| helium at 97% operating purity | 0.157 | envelope extra | +0.800 |

**The break-even structure to tie hydrogen is 0.067 kg/m³** — out of reach at any hierarchy
level this project has modelled. The demonstrable single-level design does not float at all,
while a helium fabric ship floats today. The path runs through the level-2 target, and
nothing about that is hidden: it is a prediction of this project's model, and experiment E5
in `docs/VERIFICATION-PLAN.md` is the cheap test that moves it.

## What the trade actually buys

**Structure double-duty.** A gas ship's gas is not its only overhead — it needs an envelope
and, at scale, a frame that the cell array already is. Structure-included useful fractions:
the level-2 vacuum target delivers **43.7%** of gross lift as useful lift, against the
*Hindenburg*'s demonstrated 49% on hydrogen (dead weight 0.590 kg/m³ of volume) and 41% for
the same LZ-126 hull flown on helium as USS *Los Angeles* (airships.net flight ledger).
Since the classical 0.605 coefficient landed (2026-08-12) that figure sits BETWEEN the two
gas ships rather than above both — the honest price of the correction: level 2 now beats
the helium hull it must replace and trails the hydrogen one nobody will fly again. The
margin the argument needs is still on the ladder above level 2, and hierarchy has to earn
it under real loads. The figure excludes deviatoric load, creep, ground handling and
packing fraction, and `vacuum-cell.md` says so.

**Supply independence is a fleet property, and this fleet is the point.** One P-100 fill is
171,844 standard m³ ≈ **$2.4M** at the 2024 USGS Grade-A base price of $14/m³ (up from
$7.57 in 2021 — **+85% in two years**), with make-up around 3.7%/yr ≈ $90k/yr. Helium
logistics do not hurt one ship; they hurt a hundred: **17 Mm³ held as inventory — 31% of US
annual consumption, 10% of world production** — in a market that lost its 90-year federal
buffer to a single private buyer in June 2024 (USGS MCS 2025), where lifting gas is already
18% of US use. A fleet-scale program on helium is not a price-taker; it moves the market it
depends on. Vacuum is the only lifting principle with no feedstock at all.

**Fixed displacement where an envelope suffers most.** Sealed cells cannot burst, cannot
over-expand on climb, need no superheat management, and hold their displacement identically
at any altitude and temperature — over a fire, in the turbulence and radiant load where this
vehicle earns its keep, those are the properties that matter. The honest cost on the other
side of the ledger: a gas ship's ballonet is reversible and nearly free, while the
sealed-cell hull's made ballast is the cryogenic plant — carrying the project's
worst-sourced mass number — plus the anchor. That trade is bought deliberately, for the
properties above.

**Permanence.** A gas ship is a standing gas operation: permeation make-up, purity
management, inflation headroom, hangars, trained crew, tube trailers to wherever the ship is
based. The vacuum cell's promise is a solid object, sealed at manufacture for the life of
the airframe. That promise is a design intent, not yet a demonstrated property: permeation
for life with no pump aboard, creep, and the breach case are precisely what
`docs/VERIFICATION-PLAN.md` exists to test.

## The question the project will be asked

**"Why not an uncrewed, compartmentalised hydrogen ship?"** It shares real strategic ground
with the vacuum architecture — no helium dependence, gas producible on site, 93% of gross
lift — at fabric-ship technology readiness, with fills 20–150× cheaper than helium. The
answer this project gives: a wildfire is the hardest environment there is to argue
flammability away; a hydrogen envelope inherits every envelope fragility exactly where the
mission lives; and permanence — sealed-for-life cells with no gas farm — is a property
hydrogen cannot have at any price. What still needs doing to make that answer complete:
read the certification rule rather than remember it (FAA-P-8110-2's non-flammable
lifting-gas requirement is currently cited from memory), and pin the hydrogen $/kg to a
current IEA/DOE figure.

## What must be true before this page hardens

1. FAA-P-8110-2 (or its successor) read, not remembered.
2. The ~1 L/m²/day envelope-permeability spec traced to a readable source (Liao & Pasternak
   2009 is paywalled; the figure here is order-of-magnitude).
3. Hydrogen $/kg pinned to a current IEA/DOE figure.
4. The level-2 coefficient demonstrated — the useful-fraction argument stands on
   0.538 kg/m³, a prediction of this project's model; E5 is the test.
