# Verification plan

`docs/OPEN-QUESTIONS.md` says what is wrong. This says **what would settle it**, and who has to
do it.

Every question is in exactly one of four states:

| | meaning |
|---|---|
| **SETTLED** | analysis has answered it. The answer is stated and the working is in the repository. |
| **EXPERIMENT** | no amount of modelling will do. A physical test is specified. |
| **EXPERT** | a person with a discipline has to look at it. The question is written out. |
| **DATA** | a dataset we do not have would answer it. The dataset is named. |

Regenerate everything this rests on with `make analysis`; `make check` now gates the prose
against it.

---

## The critical path: one number decides whether this can exist

**2026-10-05:** This budget prices the first-generation hull of many permanently sealed vacuum cells; it has not been re-priced for the current one film on hoop rings over a two-walled truss.

> **Air density is 0.957 kg/m³ at 2,500 m:** a shell at or above it has no net lift
> at any size. The complete budget can be grown until it closes only below
> **ρ/(1 + f) = 0.870 kg/m³ in the floor case**, because sundries include the shell.

The cases differ with their own sundries fractions: floor: f = 0.10, wall 0.870 kg/m³; credible: f = 0.15, wall 0.832 kg/m³; demonstrated: f = 0.20, wall 0.797 kg/m³.

Displacement is a design variable; payload is the requirement. These constant-density
closure sizes balance the conditional equipment bill and do not validate a drawn hull.

| source | shell | verdict against the floor closure wall |
|---|---|---|
| Jenett et al. 2019, discrete lattice | 0.508 kg/m³ | below by 41.6% |
| Jenett + 50% for joints and skin | 0.75 kg/m³ | below by 13.8% |
| Metlen 2013, frame with a real membrane | ≈0.94 kg/m³ equivalent | passes the lift wall; fails the closure wall by 8.1% |
| Akhmeteli & Gavrilin 2021, sandwich sphere | 1.16 kg/m³ | fails both; 33.4% above the closure wall |

The 0.508 kg/m³ floor closes at 516,771 m³, a 146 m ship, shorter than
the Hindenburg; 0.75 needs 7.32× the baseline volume. At 0.90 it never closes.

Two things also matter:

- **Shape.** A monocoque fineness-4 hull's estimated ~2.45× buckling penalty would take
  Jenett's 0.508 to 1.25 kg/m³, over both walls.
- **Packing.** This budget prices **many permanently sealed vacuum cells**. Their buckling
  radius is the cell's; ambient space between cells lifts nothing. At φ = 0.74 the floor
  closure wall is **0.644 kg/m³**, from ρφ/(1 + f).

The sealed-cell density and packing fraction have neither been chosen nor measured.


---

## The register

### Settled by analysis

| # | question | answer | where |
|---|---|---|---|
| 13 | Do the fires have water? | The mapped shoreline screen is a geometric result, not proof of usable water. The [station study](../research/analysis/water-availability.md) records selected-source refusals, detours and invented exercise legs. Depth, permissions, replenishment, intake access and hull clearance remain unresolved. | `water-availability.json`, `water-availability.md` |
| — | Is the published throughput representative? | **Conservative by 1.9×** — but see the vertical-profile caveat below. | `water-availability.md` |
| 0, 4 | Can we delete the cryogenic plant? | **Open for the current architecture.** The first-generation sealed-cell hull could not admit air as ballast; its retraction is retained. The current raft-and-membrane layout has no record settling the emergency-ballast choice. | `air-ballast.md` |
<!-- editorial:nitrogen-register:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:nitrogen-register:end -->
<!-- editorial:descent-register:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:descent-register:end -->
<!-- editorial:disc-register:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:disc-register:end -->
<!-- editorial:release-register:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:release-register:end -->
| # | question | answer | where |
|---|---|---|---|
| 11 | Does the mass budget close? | **Not as specified** (2.16× at its most favourable). But the hull is free to grow, so it becomes the shell-density question above. | `mass-budget.md` |

### Needs an experiment

| question | experiment |
|---|---|
| **What does one real sealed vacuum cell mass — lattice, skin, seal, and its joint to its neighbours?** | **E1**, below. This is the project. |
| Can sealing be separated from load-bearing? | **E2** — a membrane coupon holding 1 atm across a lattice cell, in creep, to failure. |
| What pattern does a sprayer lead make? | **E3** — a USFS cup-grid test under a slow release at 50–150 m. |
| What happens when a cell is breached? | **E4** — the failure mode, and whether cellularity really makes it benign. |

### Needs an expert

| question | discipline |
|---|---|
| **What packing fraction is achievable, and what does a space-filling cell cost against a spherical one?** | geometry / pressure vessels — *no hardware needed, and it moves the wall directly* |
| **What cooling does the configured machinery need on its ambient-pressure raft outside the vacuum?** | aircraft thermal engineering — ducting, coolant loops and bay ventilation remain unpriced |
| What does a 6 MW airborne nitrogen liquefier weigh? | cryogenic plant — ground practice is ~65 t/MW; our floor assumes 2 |
| Can a 300–400 m sprayer lead, and a 1,500 m anchor cable with a 125 t bag, be flown stably? | flight dynamics / deep-tow marine |
| Is the 0.6 rotor thrust share defensible? Is `rhoAir` = 1.10 defensible at 2,500 m? | rotor aerodynamics — removing the 0.6 alone multiplies the descent bill by 2.15× |
| **Does pre-treatment work, and what is it worth?** | fire behaviour / operations research — *the primary mission, and the least analysed thing here* |

### Needs data

| question | dataset |
|---|---|
| **How many of the 13,646 lakes are deep enough for the bag?** It needs 8.1 / 17.5 / 37.6 m and the Freshwater Atlas carries area, not depth. | BC lake bathymetry |
| Which lakes are legally and practically draftable? | water licensing, First Nations consultation, fisheries |
| Can we serve a basemap we are entitled to? | an openly-licensed satellite layer, or none |

---

## The experiments, specified

### E1 — what a sealed vacuum cell actually weighs

**Question.** Can one closed, skinned, sealed cell — with its joints and its share of the
inter-cell structure — hold vacuum at a mass per enclosed cubic metre that clears the wall with
margin, at a size that tiles into a hull?

**Why it cannot be modelled.** Three published analyses disagree by 2.3×, all are spheres, all
exclude different things, and the lightest excludes the most. Jenett's own paper says full 3D
buckling is "later work" and never masses the 125,600 skin panels it counts.

**Stage A — a gram-level breakdown.** Not a test: a design, itemised to the node and the
fastener, by someone who builds architected structures. Cheapest possible next step in the
project; it either kills the concept in a fortnight or gives it a number to aim at.

**Stage B — build one and evacuate it.** Success is not "it did not implode". Success is a
measured kg/m³ and a measured leak rate. Answers E2 and E4 on the same article.

**Stage B is now a concrete article: the printed demonstrator.** From the printer chain in
`research/analysis/vacuum-cell.md` — every dimension is forced by the 0.6 mm hardened nozzle,
none is a choice:

- **216 cuts of purchased pultruded carbon tube** — 144 long
  and 72 short, cut to the joint's own seats rather than to the
  centre-to-centre span (`make nodes` writes the cut list; nine lengths, not two). The
  sunken boundary frame shortens every boundary-adjacent member by its own ends'
  displacements, which is where the extra saw settings come from — with
  <!-- editorial:joint-bill:start -->
  **modelled printed joints** (computed geometry bill)
  <!-- editorial:joint-bill:end -->
  . Assembles into a **709 mm Kelvin
  cell, 178 litres**. Of the 216 members, 166 are CLOSING members that drop between two
  nodes already fixed in space: their 332 ends carry a 2 mm pilot inside a 2 mm cup, which is
  what `tools/check_assembly.py` proves against the swing-in bound end by end.

- **THE BOUNDARY IS SIZED BY THE FILM, NOT BY CRUSH, and that is new.** Writing the
  film-edge load model for the first time showed the rim failing at
  **0.26 atmospheres** with the hexagon faces unbraced — the
  article could not have survived Stage B. Six spokes per hexagon plus the heavier rim
  section take it to 1.65 atm. **E5 must therefore load a rim
  member in BENDING as well as a strut in compression**; the bending case is the one that
  governs, and it had never been tested because it had never been computed.
- **It will not float and is not supposed to** — a printed-nylon lattice is ~20× the wall at
  any size. What it measures: print yield and tolerance at 251 mm; joint behaviour at the
  12-tube nodes (nodes *carry load* in every measured discrete-lattice assembly, whatever
  the model's 15% dead-mass line assumes); strut strain under a full atmosphere against the
  model's 3p/φ; creep; months of pressure log; breach of an instrumented sub-volume.

- **Build sequence, which is itself under test.** Print → dry/anneal (PAHT-CF is
  hygroscopic and its numbers are dry-state; absorbed water alone can exceed a naive
  vacuum budget, so **bake-out under vacuum is a hard gate, not a nicety**) → assemble →
  apply the barrier: films pre-formed to their loaded dome shape, bonded at temperature
  **while the cell sits in a vacuum chamber** — the chamber does the evacuating, the heat
  drives off volatiles and closes printed micro-voids, and the last operation before
  cool-down is the seal. The printed wall is structure, not barrier: as-printed FDM walls
  are porous, and pretending otherwise fails the first pressure log.
- **Pass/fail needs a number the project has not chosen: the vacuum-degradation allowance.**
  Adopt one (proposed: ≤10% lift-margin erosion in 10 years, prorated for the test) before
  the first pressure log, or the log proves nothing. Month-one pressure rise will be
  outgassing-dominated, not leak-dominated; the protocol must separate them.

**What would falsify the concept.** A Stage A breakdown above ~0.7 kg/m³ per cell with no path
below it — because packing then takes the effective figure over the wall.

### E2 — the sealing membrane

Can a film that only has to *seal*, with load-carrying left to the lattice, hold one atmosphere
across a cell in permanent creep for a service life? The derived floor is 43 g/m²; Metlen's real
membrane is eighty times that, because his membrane was *also* structural. That gap is the whole
question, and it is a coupon test.

### E3 — what the drop does

The standard USFS cup-grid method, under a slow metered release from a sprayer lead at 50, 100
and 150 m in measured wind. Settles `ALT.drop`, `dropKm` and the swath together — all three of
which are currently one number applied to three very different aircraft.

### E4 — breach

What happens when a cell fails. Cellularity is supposed to make this benign — one cell's lift,
not the ship's — and that is the claim the architecture is bought with, so it should be the
claim that gets tested. Cycle the Stage B article to failure and watch how it goes. The open
part nobody has modelled is the **transient**: the shock of one atmosphere arriving suddenly
on partitions rated for zero differential, not the steady state after it.

### E5 — the level-2 coefficient, A/B

**What would test the level-2 prediction?** The M60J formula gives 1.1243 kg/m³ with outer-envelope film and a node allowance.
Its structural safety factor is 1.5 against full sea-level pressure, with assumed local-wall knockdown 0.30.
This is a formula without a drawn hierarchical strut, as the [float ledger](FLOAT-LEDGER.md) records.
Lakes’ 1993 exponent argument does not supply a measurement of this structure.
Which measured knockdowns apply to this geometry?
Could equal-mass, equal-length compression tests of a plain tube and a tube whose wall contains smaller tubes establish the model’s failure-load ratio?

### E6 — the barrier stack

The demonstrator's sealing film, tested as a component before it is trusted on the article:
permeation rate of the candidate stack (pre-formed dome, bonded at temperature under vacuum)
on a printed coupon, through thermal cycling and against the crazing strain limit — inorganic
barriers craze near 1% strain, which is why the dome must be pre-formed rather than blown
into shape on first pump-down.

---

## What we would ask external evaluators

1. **An architected-materials structures group** (the Jenett/Cheung lineage, or a university
   lattice group). *"Here is the floor closure wall: ρφ/(1 + f), or 0.870φ kg/m³ of enclosed volume. Here is your published 0.508 for a bare sphere. What does one complete, sealed,
   jointed cell weigh?"*
2. **A pressure-vessel geometer.** *"Spheres pack at 0.74 and are the ideal pressure shape;
   space-filling polyhedra pack at 1.0 and are not. Where is the optimum?"* No hardware, and it
   moves the go/no-go number directly.
3. **An aircraft thermal engineer.** *"The configured drives and plant sit on an ambient-pressure
   raft outside the vacuum. What ducting, coolant loops and ventilation do their duty cycles need,
   and what does that cooling system weigh at the working altitude?"*
4. **A BC Wildfire Service operations chief.** *"One aircraft, 5,500 tonnes of water a day,
   113 km of geometric line in retardant coverage-level units, under suitable conditions — and its best use may be soaking
   ground **before** a fire arrives rather than fighting one. Is that useful, and would it
   compete with the skimmers for the same lakes?"* **This decides what the vehicle is for.**
5. **A fire-behaviour scientist.** *"What is pre-treatment worth, how long does a water line
   persist, and what is the right effectiveness metric for a machine with unlimited water and
   no crews under it?"*
6. **A battery pack engineer**, and **a cryogenic plant engineer** — for the two mass lines with
   the widest unsupported spreads.

---

## What is still missing entirely

Named here because an honest plan says what it does not cover. Ranked by how likely each is to
be fatal:

1. **Ground handling, mooring and the parked state.** An evacuated moored P-100 pulls ~1.4 MN
   upward permanently; 10 cm of wet snow is 268 t downward; a broadside 30 m/s wind is ~2.5 MN
   on the side area. **There is no demonstrated state in which this aircraft sits still**, and
   BC's off-season is eight months.
2. **Stored energy at breach.** ~22 GJ on a P-100. The cellular architecture is the mitigation
   and it is untested (E4).
<!-- solar:daily:start -->
3. **The energy supply chain.** 222.9 MWh of supplied effort per P-100 per day at the accepted median-leg rate,
   against 4.96 MWh/day of assumed solar. The tender fleet is named in the README and deliberately never
   modelled. **Every 24-hour figure in this folder is a claim about the aircraft, not about a
   system shown to supply it.**
<!-- solar:daily:end -->
<!-- editorial:certification:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:certification:end -->
5. **Competing with the existing fleet for the same lakes.** CL-415s scoop the water this
   vehicle drafts from, and a hull holding station takes a lake out of their rotation.
6. **Icing, lightning, hail, gust loading, noise, and the cost of anything.** All named nowhere,
   or in a single word inside a catch-all.
7. **The vertical flight profile.** The served model checks its bounded vertical controls and
   reserve; the earlier shore-distance throughput and unchecked-climb headline are withdrawn.
   These accepted-plan quotients remain conditional calculations, not demonstrated flight.

---

## What the analysis changed

**Better than we thought.** Water is not a constraint anywhere in BC, and the reference ship is
the class the geography suits. The floor budget's closure wall includes shell sundries; Jenett's published shell clears it with a margin before packing losses.

<!-- editorial:nitrogen-conclusion:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:nitrogen-conclusion:end -->
The first-generation sealed-cell study addressed the shape penalty by separating cell
geometry from the hull's outer shape. The current film-and-truss drawing needs its own structural case.

<!-- logistics:line-comparison:start -->
At the accepted median-leg rate, the conditional CL 4 line-length quotient is 112.8 km per day, longer than 85.5% of the stored simplified final perimeters; this is a geometric comparison, with no fire-outcome inference.
<!-- logistics:line-comparison:end -->

<!-- editorial:descent-conclusion:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:descent-conclusion:end -->


<!-- editorial:release-conclusion:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:release-conclusion:end -->
The first-generation sealed-cell budget retains the cryogenic plant. Ducting, coolant loops and bay ventilation for the current ambient-pressure machinery
layout remain unpriced. The thermal analysis exists; the cooling installation's mass is still open.

**Retracted.** Air-admission ballast. It is impossible in a sealed-cell hull, it was not novel
(Akhmeteli & Gavrilin propose it by name in the very paper this project cites for shell mass,
and US 9,016,622 patents air ballast for airships), and it would not have worked as a fail-open
valve even given an envelope to open. The retraction is kept in place at
`research/analysis/air-ballast.md` rather than deleted.

**A process fix that matters more than any single number.** The analysis notes were quoting
hand-transcribed figures while asserting they were generated. A review caught nine of them
stale — the exact failure `tools/check_figures_fresh.py` was written to kill, reproduced one
directory over. `tools/check_analysis.py` now gates them and runs in `make check`.

<!-- solar:budget-reference:start -->
The generated comparison preserves the preceding power-input publication beside the current integrated diagnostic. The existing P-100 0.508 kg/m³ sizing routine now returns 516,771 m³, against the earlier 457,324 m³, on the current model after the projected solar-area correction. Other integrated model corrections can also contribute. This is a diagnostic comparison, not validation of the closure condition. See the [generated before/after budget comparison](../research/analysis/mass-budget.md#solar-input-sensitivity-of-the-existing-budget-diagnostic).
<!-- solar:budget-reference:end -->
