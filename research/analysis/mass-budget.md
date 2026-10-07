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
The [energy correction](../../docs/audit/26-10-02-energy-carry.md) records the new battery-sizing figures and their cause.

## The requirement, as the model states it

The P-100 allows **100 t** of everything that is not water, inside **220,000 m³** of hull —
**0.4545 kg per m³** enclosed, or **5.261 kg per m²** of the 19,007 m² capsule skin.

## Three columns, and the left one is the argument

`floor` takes the single most favourable published or derivable number for **every line
simultaneously**. `credible` is a planning case. `demonstrated` combines literature
calculations, component and bench evidence, and installed or unsourced allowances;
it does not describe a built or flown vehicle. Masses below are tonnes. The last column
names the evidence behind each `demonstrated` line, including its sizing allowances.

| line | floor | credible | demonstrated | demonstrated evidence class |
|---|---|---|---|---|
| Vacuum shell (lattice) | 111.8 | 165.0 | 255.2 | literature FEA |
| Gas barrier skin | 0.8 | 8.2 | 65.6 | literature membrane |
| Solar skin | 2.2 | 3.9 | 7.2 | installed allowance |
| Battery pack | 40.0 | 66.7 | 134.2 | literature pack |
| Propulsion motors | 1.9 | 2.3 | 6.0 | bench component |
| Drives, cabling, thermal | 1.9 | 2.7 | 9.0 | unsourced fraction |
| Rotors and hubs | 13.2 | 17.5 | 22.5 | rotorcraft practice |
| Cryogenic plant | 12.0 | 120.0 | 390.0 | ground hardware + surface-system estimate |
| LN2 tankage | 7.8 | 12.4 | 23.2 | cryotank practice |
| Water tanks and plumbing | 2.1 | 2.2 | 2.3 | fabric practice + plumbing allowance |
| Pump | 0.2 | 0.3 | 0.8 | bench motor + wet-end allowance |
| Hose | 1.1 | 1.8 | 2.7 | hose practice |
| Anchor cable | 0.6 | 1.4 | 2.1 | rope datasheet + assumed safety factor |
| Anchor bag | 0.1 | 0.2 | 0.3 | fabric practice |
| Winch | 0.8 | 0.9 | 2.5 | bench motor + sizing allowance |
| Sundries and margin | 19.6 | 60.8 | 184.7 | airship weight statement + mass-growth allowance |
| **TOTAL** | 216.1 | 466.4 | 1108.3 | mixed evidence above |
| × the 100 t allowance | 2.16× | 4.66× | 11.08× | |

<!-- mass-budget:floor:start -->
Sizing the battery to three prescribed cycles raises the floor from **216.1 t, 2.16×**, to **226.1 t, 2.26×**.
<!-- mass-budget:floor:end -->

The cycle is infeasible; this energy-based allowance does not establish endurance. The cryogenic plant stays: see the retraction in `air-ballast.md`.

**The cryogenic line is now the second-largest item in the vehicle and the worst-supported.**
Published skid-mounted liquefiers run about 65 t/MW (Stirling StirLIN-2: 34 kW in 2,200 kg),
and Hauser, Johnson and Sutherlin's [NASA Mars-surface oxygen liquefaction estimate](https://ntrs.nasa.gov/api/citations/20160004210/downloads/20160004210.pdf),
Table 1, printed p. 3, totals 136.5 kg including cryocooler and radiator at 1,990 W input:
68.6 t/MW. This is a surface-system estimate, not a flight design or an airborne mass bound.
The floor of 2.0 t/MW in this table is **34× lighter than that estimate** and has no published
source; it is retained so a reader can see what the budget is given for free. At the
65 t/MW industrial comparison, the plant alone is 390 t on a 100 t allowance.

<!-- solar:budget-note:start -->
The [generated publication comparison](#solar-input-sensitivity-of-the-existing-budget-diagnostic)
records the preceding power-input publication beside the current integrated diagnostic.
It does not isolate each model correction or validate the enlarged-hull closure condition.
<!-- solar:budget-note:end -->

## But the allowance is not a law, and this is the correction that matters

**Displacement is a design variable and the payload is the requirement.** Shell mass
per enclosed volume is held constant in this conditional study. Area-scaled equipment grows
more slowly than volume. The complete bill can therefore close by growing the hull only when:

> Net lift after shell sundries = ρ_air − shell_kg/m³ × (1 + f) > 0.
> Sundries are a fraction of everything, including the shell; payload is separate.

Air density at 2,500 m is **0.957 kg/m³**. At or above this lift wall the shell has no
net lift at any size. Closing the equipment budget needs a lower shell density:
**ρ/(1 + f), or 0.870 kg/m³ in the floor case (f = 0.10)**.

The cases differ with their own sundries fractions: floor: f = 0.10, wall 0.870 kg/m³; credible: f = 0.15, wall 0.832 kg/m³; demonstrated: f = 0.20, wall 0.797 kg/m³.

Against the floor closure wall, the literature separates:

| source | shell | verdict against the floor closure wall |
|---|---|---|
| Jenett et al. 2019, discrete lattice | 0.508 kg/m³ | below by 41.6% |
| Jenett + 50% for joints and skin | 0.75 kg/m³ | below by 13.8% |
| Metlen 2013, frame with a real membrane | ≈0.94 kg/m³ equivalent | passes the lift wall; fails the closure wall by 8.1% |
| Akhmeteli & Gavrilin 2021, sandwich sphere | 1.16 kg/m³ | fails both; 33.4% above the closure wall |

And the hull that closes, in the floor case:

| shell | volume that closes | × baseline | hull |
|---|---|---|---|
| 0.264 kg/m³ | 306,093 m³ | 1.39× | 123 × 61 m |
| 0.350 kg/m³ | 357,508 m³ | 1.63× | 129 × 65 m |
| 0.508 kg/m³ (Jenett, published) | 516,771 m³ | 2.35× | 146 × 73 m |
| 0.600 kg/m³ | 697,253 m³ | 3.17× | 162 × 81 m |
| 0.750 kg/m³ | 1,609,811 m³ | 7.32× | 214 × 107 m |
| 0.900 kg/m³ | **never** | — | — |

**At the best published shell density the reference ship conditionally closes at 146 × 73 m —
still shorter than the Hindenburg.** Its volume is **2.35× the reference**.
This is a complete equipment-bill balance under constant shell density, not a checked structure.

The conditional volume grows from 516,771 m³ at 0.508 kg/m³ to
1,609,811 m³ at 0.75 kg/m³ (214 × 107 m). At 0.90 kg/m³
it **never closes**: shell plus its 10% sundries costs 0.990 kg/m³, above the air density.

## The sealed-cell architecture is the answer to the shape problem — and it has a price

**2026-10-05:** This budget prices the first-generation hull of many permanently sealed vacuum cells; it has not been re-priced for the current one film on hoop rings over a two-walled truss.

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
| effective closure wall | 0.644 kg/m³ | 0.739 kg/m³ | 0.870 kg/m³ |
| hull at shell 0.264 | 492,055 m³, 144 × 72 m | 391,499 m³, 133 × 67 m | 306,093 m³, 123 × 61 m |
| hull at shell 0.508 | 1,415,173 m³, 205 × 102 m | 816,286 m³, 170 × 85 m | 516,771 m³, 146 × 73 m |
| hull at shell 0.750 | **never** | **never** | 1,609,811 m³, 214 × 107 m |

The packing wall is ρφ/(1 + f); the table uses the floor f = 0.10. Credible (f = 0.15) and demonstrated (f = 0.20) lower each wall further.

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
- **Thermal management** — largely a false alarm, and worth recording as one. The current drawing puts machinery
  on an ambient-pressure raft outside the vacuum, so convection works. This is an aircraft
  cooling problem with a modest altitude derate (air at
  the working altitude is 78% of sea-level density). A hypothetical alternative with machinery inside a vacuum
  would require a spacecraft thermal design: ~1.8 MW of waste heat needing 1,750 to
  7,000 m² of radiator, **5 to 56 t**. There is still no line for the ducting, coolant loops and
  bay ventilation. Their installed mass remains open; ambient convection alone does not price it.

Also missing: a mass line for `genMW` (8 MW of generation that `plan.js` uses in the thrust
budget), load diffusion for a 1.2 MN anchor point into a shell designed for uniform pressure,
and a realistic mass growth allowance — `sundries_frac` is 10% at the floor where conceptual
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
| **What cooling does the configured machinery need on its ambient-pressure raft outside the vacuum?** | aircraft thermal engineering | a duty-cycle heat balance and installed mass for ducting, coolant loops and bay ventilation |
| What does a 6 MW airborne liquefier weigh? | cryogenic plant | a vendor or first-principles estimate — there is no published one |

## The honest summary

The budget as specified fails by 2.16× at its most favourable,
and 2.26× with the battery sized to the prescribed cycle. At the best published
shell density the conditional complete bill closes at **2.35× the reference volume,
a 146 m hull**. The lift wall is **0.957 kg/m³**; the floor equipment-budget closure
wall is **0.870 kg/m³**, reduced further by packing losses and larger sundries fractions.

What decides this sealed-cell budget is the density of one complete cell and its packing
fraction. Neither is measured here, and these conditional sizes do not validate a hull.

<!-- solar:budget-comparison:start -->
## Solar-input sensitivity of the existing budget diagnostic

This comparison preserves the pre-correction publication on the left and refreshes the
existing diagnostic on the right from `mass-budget.json`. The reason is the projected
solar-area correction; gross material area stays a separate assumption. Neither column
establishes a buildable hull or validates the enlarged-hull closure condition. If this
record is regenerated on an integrated tree, other model corrections can also contribute
to the differences; this comparison does not isolate their individual effects.

| Class | Nominal floor t | Three-cycle floor t | Three-cycle floor / dry | Existing 0.508 kg/m³ diagnostic volume m³ | Existing volume / baseline |
|---|---|---|---|---|---|
| P100 | 216.1 → 216.1 | 226.2 → 226.1 | 2.26 → 2.26 | 457,324 → 516,771 | 2.08 → 2.35 |
| P1000 | 1803.6 → 1803.6 | 1950.9 → 1950.5 | 1.95 → 1.95 | 3,855,851 → 4,353,131 | 1.75 → 1.98 |
| P10000 | 19524.2 → 19524.2 | 19707.1 → 19705.8 | 1.97 → 1.97 | 38,938,209 → 43,946,913 | 1.77 → 2.00 |

P-100 density sweep of the same existing diagnostic; current values precede the preserved publication:

| Shell kg/m³ | Current volume m³ | Current / baseline | Current length × diameter | Earlier volume m³ | Earlier / baseline | Earlier length × diameter |
|---|---|---|---|---|---|---|
| 0.264 | 306,093 | 1.39 | 123 × 61 m | 294,309 | 1.34 | 121 × 61 m |
| 0.350 | 357,508 | 1.63 | 129 × 65 m | 336,631 | 1.53 | 127 × 63 m |
| 0.508 | 516,771 | 2.35 | 146 × 73 m | 457,324 | 2.08 | 140 × 70 m |
| 0.600 | 697,253 | 3.17 | 162 × 81 m | 577,748 | 2.63 | 152 × 76 m |
| 0.750 | 1,609,811 | 7.32 | 214 × 107 m | 1,010,309 | 4.59 | 183 × 91 m |
| 0.900 | not closed | | | 3,908,881 | 17.77 | 287 × 144 m |

Current P-100 packing diagnostics (their earlier dimensions remain in the numeric reference):

| Existing diagnostic | phi=0.74 | phi=0.85 | phi=1.0 |
|---|---|---|---|
| hull at shell 0.264 | 492,055 m³; 144 × 72 m | 391,499 m³; 133 × 67 m | 306,093 m³; 123 × 61 m |
| hull at shell 0.508 | 1,415,173 m³; 205 × 102 m | 816,286 m³; 170 × 85 m | 516,771 m³; 146 × 73 m |
| hull at shell 0.750 | not closed | not closed | 1,609,811 m³; 214 × 107 m |
<!-- solar:budget-comparison:end -->
