# The dry-mass budget, line by line

`docs/OPEN-QUESTIONS.md` #11 is the largest question in the project, and until now the argument
against `dryT = payloadT` was two citations. Citations can be argued with one at a time. A
budget cannot: it says what every part of the ship weighs, where the number came from, and how
far the total is from the allowance.

`research/analysis/mass-budget.py` builds it. Every vehicle quantity is read from
`research/figures.json`, which `make factsheet` regenerates from the live model and
`tools/check_figures_fresh.py` refuses to let drift. The only things typed in are the external
specific masses, and each carries its source.

**2026-10-02 correction:** nominal fleet areas now use the model’s capsule surface.
The [regeneration audit](../../docs/audit/26-10-02-analysis-regeneration.md) records every old and new number and its cause.
These conditional equipment budgets do not validate a drawn hull.

## The requirement, as the model states it

The P-100 allows **100 t** of everything that is not water, inside **220,000 m³** of hull —
**0.4545 kg per m³** enclosed, or **5.261 kg per m²** of the 19,007 m² capsule skin.

## Three columns, and the left one is the argument

`floor` takes the single most favourable published or derivable number for **every line
simultaneously** — a vehicle that gets the best of everything at once, which no real vehicle
does. `credible` is what an engineer would plan against. `demonstrated` is what has been built
and flown.

| line | floor | credible | demonstrated |
|---|---|---|---|
| Vacuum shell (lattice) | 111.8 | 165.0 | 255.2 |
| Gas barrier skin | 0.8 | 8.2 | 65.6 |
| Solar skin | 2.2 | 3.9 | 7.2 |
| Battery pack | 40.0 | 66.7 | 134.2 |
| Propulsion motors | 1.9 | 2.3 | 6.0 |
| Drives, cabling, thermal | 1.9 | 2.7 | 9.0 |
| Rotors and hubs | 13.2 | 17.5 | 22.5 |
| **Cryogenic plant** | **12.0** | **120.0** | **390.0** |
| LN₂ tankage | 7.8 | 12.4 | 23.2 |
| Water tanks and plumbing | 2.1 | 2.2 | 2.3 |
| Pump | 0.2 | 0.3 | 0.8 |
| Hose | 1.1 | 1.8 | 2.7 |
| Anchor cable | 0.6 | 1.4 | 2.1 |
| Anchor bag | 0.1 | 0.2 | 0.3 |
| Winch | 0.8 | 0.9 | 2.5 |
| Sundries and margin | 19.6 | 60.8 | 184.7 |
| **TOTAL** | **216.1** | 466.4 | 1108.3 |
| × the 100 t allowance | **2.16×** | 4.66× | 11.08× |

Right-sizing the battery to the mission rather than to eighteen cycles of endurance takes the
floor to **181.3 t, 1.81×**. The cryogenic plant stays: see the retraction in `air-ballast.md`.

**The cryogenic line is now the second-largest item in the vehicle and the worst-supported.**
Published skid-mounted liquefiers run about 65 t/MW (Stirling StirLIN-2: 34 kW in 2,200 kg),
and NASA's own mass-optimised *flight* concept — reverse turbo-Brayton, the most mass-efficient
cryocooler class known — is 68.6 t/MW. The floor of 2.0 t/MW in this table is **34× better than
the best flight design NASA has published**, and it is kept at that value only so a reader can
see exactly what the budget is being given for free. At the demonstrated figure the plant alone
is 390 t on a 100 t allowance.

## But the allowance is not a law, and this is the correction that matters

**Displacement is a design variable and the payload is the requirement.** Asking "what must a
cubic metre of vacuum cost to fit inside 220,000 m³" is the question backwards. Ask it forwards:

> Net lift per m³ = ρ_air − shell_kg/m³, and **it does not change with size** — Jenett's design
> rules are ratios, so a lattice shell costs the same per enclosed cubic metre at every radius.
> A fixed payload divided by a constant net lift per m³ therefore always has a solution.

So the hull grows until it closes, and the only thing that can prevent it is the shell being
heavier than the air it displaces. **That is the real go/no-go, it is one number, and it is
written down nowhere in this project:**

> ## A vacuum shell must mass less than 0.957 kg per m³ of enclosed volume.
> That is ISA air density at the 2,500 m working altitude. Above it there is no net lift at
> any size, at any scale, ever.

Against that wall, the literature separates:

| source | shell | verdict |
|---|---|---|
| Jenett et al. 2019, discrete lattice | 0.508 kg/m³ | **passes, with 47% margin** |
| Jenett + 50% for joints and skin | 0.75 kg/m³ | passes, with 22% |
| Metlen 2013, frame with a real membrane | ≈0.94 kg/m³ equivalent | **passes by 2%** |
| Akhmeteli & Gavrilin 2021, sandwich sphere | 1.16 kg/m³ | **fails outright** |

And the hull that closes, in the floor case:

| shell | volume that closes | × baseline | hull |
|---|---|---|---|
| 0.264 kg/m³ | 228,644 m³ | 1.04× | 111 × 56 m |
| 0.350 | 261,566 m³ | 1.19× | 117 × 58 m |
| **0.508 (Jenett, published)** | **355,499 m³** | **1.62×** | **129 × 65 m** |
| 0.600 | 449,285 m³ | 2.04× | 140 × 70 m |
| 0.750 | 786,622 m³ | 3.58× | 168 × 84 m |
| 0.900 | 3,060,477 m³ | 13.91× | 265 × 132 m |

**At the best published shell density the reference ship closes at 129 × 65 m — still shorter
than the Hindenburg.** The previous headline here, that the shell must be 1.9× lighter than
anything ever designed, was an artefact of holding the hull size fixed. The honest statement is
that **the reference hull is undersized by about 1.6×**, which is a sizing decision, not a
physics wall.

The curve is brutally non-linear near the wall, though: 0.508 → 0.75 nearly triples the hull,
and 0.90 multiplies it twentyfold. Every kilogram per cubic metre bought back is worth much
more than it looks.

## The sealed-cell architecture is the answer to the shape problem — and it has a price

The hull is not one evacuated envelope. **It is many permanently sealed vacuum cells**, which
this project has never written down anywhere and which changes the structural argument twice:

**It removes the shape penalty.** Every vacuum design in the literature is a sphere, because a
sphere is optimal against external pressure, and our hulls are fineness-4 bodies of revolution.
On a monocoque that is expensive: the mid-body's principal radii are 384 m and 23.5 m, so the
equivalent buckling radius is ≈95 m against 37.4 m for the equal-volume sphere, and a
first-order (t/R)² scaling puts the shell penalty near 2.45× — which would take Jenett's 0.508
to 1.25 and **over the wall, where nothing closes at any size**. With the pressure held in
small cells, the buckling radius is the *cell's*, the outer body is a fairing rather than a
pressure vessel, and the penalty largely goes away.

**It costs packing.** Space between cells sits at ambient and lifts nothing, so displacement is
scaled by the packing fraction φ:

| | φ = 0.74 (close-packed spheres) | φ = 0.85 | φ = 1.0 (space-filling cells) |
|---|---|---|---|
| effective wall | 0.708 kg/m³ | 0.813 kg/m³ | 0.957 kg/m³ |
| hull at shell 0.264 | 359,402 m³, 130 × 65 m | 289,426 m³, 121 × 60 m | 228,644 m³, 111 × 56 m |
| hull at shell 0.508 | 814,181 m³, 170 × 85 m | 527,049 m³, 147 × 74 m | 355,499 m³, 129 × 65 m |
| hull at shell 0.750 | **never** | 2,725,487 m³, 255 × 127 m | 786,622 m³, 168 × 84 m |

**Packing fraction is now a first-order design parameter and nobody has chosen it.** A
space-filling cell (rhombic dodecahedron, truncated octahedron) approaches φ = 1 but is a worse
pressure shape; spheres are the best pressure shape and waste 26% of the hull. The trade
between the two is the single most valuable piece of structural work available to this project,
and it is a geometry exercise before it is an experiment.

It also buys the thing that has no other answer: **failure containment.** One cell losing
vacuum costs one cell's lift, not the ship.

## What the budget still says, and it is not nothing

Even with the hull free to grow, the line items are what set how much it must grow, and two
of them are unsourced:

- **The cryogenic plant** — 12 to 390 t across the columns, the widest spread in the budget,
  and **no published figure prices a 6 MW airborne nitrogen liquefier**. It is now known to be
  necessary (it is the only emergency ballast source a sealed-cell hull has), which makes the
  absence of a mass estimate the single worst-supported number in the vehicle.
- **Thermal management** — largely a false alarm, and worth recording as one. Machinery does
  not sit inside a vacuum cell; it sits in ambient-pressure bays within the hull, so convection
  works and this is an ordinary aircraft cooling problem with a modest altitude derate (air at
  the working altitude is 78% of sea-level density). Had the machinery been inboard of the
  vacuum it would have been a spacecraft thermal design: ~1.8 MW of waste heat needing 1,750 to
  7,000 m² of radiator, **5 to 56 t**. There is still no line for the ducting, coolant loops and
  bay ventilation, and it should be small — but it is not zero and it is not written down.

Also missing: a mass line for `genMW` (8 MW of generation that `plan.js` uses in the thrust
budget), load diffusion for a 1.2 MN anchor point into a shell designed for uniform pressure,
and a realistic mass growth allowance — `sundries_frac` is 5% at the floor where conceptual
design practice is 25–30%.

And a physical one worth stating: **water boils at ambient temperature in vacuum**, so a
payload tank inside the envelope is a pressure boundary carrying an atmosphere outward, not the
limp bladder this budget prices.

## Where the barrier number comes from, since it is the one derivation here

`barrier_floor()` sizes a film that only has to **seal**, with load-carrying left to the lattice
under it: a film bulging into a lattice cell carries the atmosphere as membrane tension,
σ = pR/2t. At a quarter-width bulge, a safety factor of 4 on Zylon and 50% realised fibre
strength, that is **43 g/m²** — about 1 t on a P-100.

Metlen measured 3.45 kg/m² for a real membrane, eighty times more, because his membrane was
*also* the structure. That gap is the whole question of whether the two functions separate, and
it is a materials test, not an analysis.

## What must be verified, and by whom

| question | discipline | what would settle it |
|---|---|---|
| **What is the shell density of a real sealed cell — lattice, skin, seal, and the joint to its neighbours?** | structures / architected materials | a gram-level breakdown of one complete cell, and one built and evacuated |
| **What packing fraction is achievable, and what does a space-filling cell cost against a spherical one?** | geometry / pressure vessels | a trade study; no hardware needed |
| What is a realistic pack density for a few MWh that is neither an aviation pack nor a vendor cell claim? | battery engineering | an independent pack-level estimate |
| **What does 30 MW of drives need to reject heat with no convection?** | spacecraft thermal | a radiator or conduction-path mass estimate |
| What does a 6 MW airborne liquefier weigh? | cryogenic plant | a vendor or first-principles estimate — there is no published one |

## The honest summary

The budget as specified fails by 2.16× at its most favourable, and 1.81× with the battery
right-sized. But the vehicle is not the specification: **at the best published shell density the
concept closes at 1.62× the reference volume, a 129 m hull — and the true go/no-go is a single
number, 0.957 kg/m³, that the project had never written down.**

What decides it now is not "can the shell be twice as light as anything designed". It is:

1. **the shell density of one sealed cell**, including its seal and its joints, and
2. **the packing fraction**, which multiplies the wall directly and which nobody has chosen.

Both are answerable, one of them on paper. That is a substantially better position than the
previous page described, and it is the sealed-cell architecture — undocumented until today —
that puts it there.
