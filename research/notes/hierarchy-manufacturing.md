# Level-2 hierarchy — what is actually manufactured, and what the coefficient really costs

A topic note, not a single-source note: the level-2 claim touches ten sources and the useful
statement only emerges from reading them together. Written 2026-08-10 against the papers in
`research/papers/` (Gregg 2024 + supplement, Zheng 2016, Smith 2025, Ochalek 2018, Sajjadi 2018)
and against reads of Lakes 1993 (author posting), Meza 2015 (PMC), Cheung 2013 and Jenett 2020
(author/CC copies, catalogued not stored). Confidence tags: **MEASURED** (a number someone
tested), **DATASHEET** (a vendor or estimated constituent value), **OOM** (order-of-magnitude
extrapolation).

## The headline first

**The level-2 coefficient is carried at zero degradation, and no published source supports
0.428 kg/m³.** The cell model steps the shell from 1.086 to 0.428 against the 0.957 buoyancy
wall by adding a second level of hierarchy — and it applies the exponent gain while leaving the
strength coefficient untouched, even though the page itself admits the coefficient "degrades
even as the exponent improves." Every measured hierarchical specimen in the literature pays a
coefficient penalty; none of them is a tube-of-tubes strut; none is at structural scale and
airship-usable density. 0.428 is a **prediction of this project's own scaling arithmetic**, and
must be labelled as such wherever it appears. The measured knockdown bands straddle exactly what
the margin tolerates (arithmetic below), so the number is not safe and not dead — it is
undecided, and the A/B crush benchmark on the project's own printer is the retirement path.

## What the sources actually establish

**The exponent gain is real, measured three times at three scales.**

- Lakes (1993, Nature) built second-order paper honeycomb and crushed it: **3.2–3.8× stronger
  in compression than first-order honeycomb at the same 0.01 g/cm³ density** (MEASURED). Two
  more things the project's page does not yet carry: his own plastic-buckling theory predicted
  4.6×, so even the founding measurement landed at 0.7–0.83 of its predicted gain — a
  coefficient shortfall of 1.2–1.4× in the friendliest possible experiment; and he bounds the
  ladder — cell-wall relative thickness grows with order, so at relative density 0.01 "values
  of n above 4 are unrealistic." Both support stopping at level 2 with 3 as reserve.
- Zheng et al. (2016, **Nature Materials** 15:1100 — the project page has been citing this as
  Science; Science 344 is the separate 2014 single-scale paper) measured 2nd–3rd-order Ni-P
  hollow-tube lattices: strength–density scaling exponent as low as **1.3** at relative density
  below 10⁻³, tensile strain ~20%, specific strength to 40.8 MPa/(g/cm³) (MEASURED, from the
  OSTI accepted manuscript in `papers/`).
- Meza et al. (2015, PNAS) measured 2nd-order hollow-tube alumina octahedron-of-octets:
  stiffness E = 0.015·E_s·ρ̄^1.04 — nearly linear where a single-level bend-dominated
  architecture would be quadratic or worse (MEASURED, read at PMC).

**And every measured coefficient lands below the ideal.** Meza's 0.015 sits ≈7× under the
A = 0.1 that Jenett 2019 assumes for an ideal lattice and ≈20× under the octet ideal. Their own
finite-element predictions overshot the hollow-tube measurements by 68.5% — a **1.69× defect
knockdown, attributed to sinusoidal wall waviness from the two-photon writing process**
(MEASURED) — while their monolithically printed polymer specimens came in ~11% *above*
prediction (MEASURED): monolithic printing at ~micron scale was coefficient-clean, the
hollow-tube coating process was not. ARMADAS (Gregg 2024, in `papers/` with supplement) measured
injection-molding knit lines at **3.5× on coupon strength** (108.52 → 31.101 MPa, tables S5/S6,
MEASURED). Assembled single-level lattices land at A ≈ 0.06 (Cheung 2013, Science, catalogued
only) and A ≈ 0.019 (ARMADAS) — but both of those coefficients divide by constituent properties
this note had to assume (quasi-iso laminate values for Cheung; ρ_s ≈ 1,340 kg/m³ for StatTech
NN-40CF, a DATASHEET-class value not stated in the paper), so treat them as estimates, and note
the audit's finding that they are our arithmetic, not the papers'.

**Nodes carry load — the model has this wrong in both directions.** The cell model's
correction 3 prices nodes at ×1.15 as dead mass that "carries no load." Measured reality:

- ARMADAS' 3×3×3 assemblies **failed at the fastener**, before strut buckling — the joints were
  carrying and *limiting* the load (MEASURED). Fasteners plus bolts are **27.8% of assembled
  mass** (80.91 g of 291.24 g/voxel, computed from Table S8; MEASURED) — the worst case on
  record, and it is the price of *reversible, robot-actuated* connection, not of joints per se.
- Jenett 2020 (Sci Adv, CC BY-NC, catalogued only) states the discipline that avoids this:
  intervoxel nodes ~2× and fasteners ~4× the voxel yield strength, so their lattices failed in
  the beams, with assembled modulus scaling b = 1.01 (MEASURED). Cheung 2013 shows connection
  mass scaling *falls* relative to strut mass in the slender limit (MEASURED at one design
  point). Ochalek 2018 (poster, in `papers/`) is the candidate joint design lineage — geometry
  and captive-fastener trade space, but **no published numbers**, so the "real 12-tube node"
  the cell page says would settle ±0.14 kg/m³ still does not exist in the literature we hold.
- So the 10–30% band is confirmed at its top (27.8% MEASURED) but the modelling class is wrong:
  a node is a strength-governing element that must be designed 2–4× over strut strength, not a
  mass tax. And continuous processes put the fraction near zero at the level below assembly.

**Hierarchical *assembly* works at metre scale.** Smith 2025 (SCF '25, CC BY, in `papers/`):
CF-nylon voxels handled as blocks by mobile robots; 81.85 kg/m³ average, a 2×2×2 block held
3,445 N ≈ 2,220× its own weight, and the assembled lattice is stretch-dominated (MEASURED).
Note carefully: the hierarchy there is in the *handling*, not in the strut cross-section — it
is evidence for construction logistics, not for the level-2 coefficient.

## What this project takes

The literature lets the coefficient risk be split into three parts with different owners:

1. **Geometry choice, 4–20×, avoidable.** Meza's 0.015 is mostly the price of a compliant,
   node-rotating octahedron-of-octets chosen for printability and recovery, not stiffness. The
   design rule this forces: **the second level must be stretch-dominated too**, or the exponent
   win is spent on the coefficient. A tube wall built as a triangulated shell-like lattice is on
   the right side of this; nothing about hierarchy grants it automatically.
2. **Process defects, ~1.1–3.5×, process-selectable.** Measured points: ~1.1× monolithic
   micro-printing (Meza polymer), 1.69× ALD wall waviness (Meza hollow), 3.5× injection-molding
   knit lines (ARMADAS), 1.2–1.4× even in Lakes' glued paper honeycomb. The favourable end of
   the band belongs to continuous, monolithic processes — which is the argument for winding,
   drawing or pultruding the level-2 wall rather than molding or FFF-printing it.
3. **Joints, 0–28% of mass and possibly strength-governing, route-dependent.** Spend discrete
   joints only at the highest level (cell-to-cell, where assembly and replacement need them);
   make everything below continuous, where the node count is zero by construction.

**The margin arithmetic.** With strength ∝ B·φ^(4/3), required shell mass scales as B^(−3/4),
so the level-2 margin of 2.24× survives a total coefficient knockdown of 2.24^(4/3) = **2.9×**
and no more. The defect-class band fits inside that with room (1.7× costs 1.7^0.75 ≈ 1.5× mass);
the geometry-class band (≥4×) kills it outright.

**⚠ Label carried forward from the audit:** the "defect-class band 1.3–1.7×" doing the work in
that sentence is **effectively two data points from one lab line** (Meza's waviness 1.69× and
polymer ~1.1×), and **neither is from a process this project would use at flight scale**. It is
the thinnest load-bearing band in the whole cell argument. The audit also flags that no
published source supports 0.428 itself. Both labels stay until the benchmark reports.

**Manufacturing routes.** Three candidate routes make a tube-whose-wall-is-a-lattice without
level-2 joints — wound anisogrid scaled down (flight-proven at interstage scale per Vasiliev
2012; strut-scale ribs are OOM extrapolation), thermally drawn structured cross-sections (the
photonic-crystal-fibre industry produces exactly this geometry by the kilometre, per Russell
2003, in silica or thermoplastic only — no continuous carbon), and bundled sub-mm pultrusions
under a hoop wrap (constituents DATASHEET-real, the bonded wall unproven, bond-line creep
data-free). **Caveat on all three: Vasiliev and Russell were catalogued from verified Crossref
metadata plus secondary confirmation in the read papers — neither was read for this note**, so
the routes are leads with cited existence proofs, not reviewed engineering. The conservative
fallback — honeycomb-sandwich wall per SP-8007-2020 Rev 2 (already in `papers/`) — will not
reach 0.428, but its codified failure taxonomy (face wrinkling, shear crimping, intracell
dimpling) is the checklist any level-2 wall analysis has to answer.

**Inspection.** A billion sub-struts is the wrong count if the lower level is continuous: you
inspect process-kilometres (in-line laser micrometry is standard draw-tower and pultrusion
practice), qualify against *systematic* defects (the measured big hits — knit lines, waviness —
are systematic, exactly what small-sample qualification plus µCT spot checks catch), and
proof-load at the strut level, thousands of parts per cell, seconds each — the per-part Instron
discipline the NASA Ames line already practises (Sajjadi 2018, in `papers/`). Sealed cells then
contain whatever survives proof load and fails anyway.

## Where the sources do NOT support what we would like

1. **Nobody has ever built or crushed a tube-of-tubes strut.** Not at 100 µm, not at 1 mm, not
   at any scale. The three measured hierarchy demonstrations are paper honeycomb, nanolattices
   at ρ̄ < 10⁻³, and micron-scale alumina — none within reach of an airship design point. The
   right citation posture is: *exponent mechanism confirmed at three scales; coefficient never
   demonstrated at structural scale.*
2. **Zheng's measured exponent is 1.3, not the ladder's 1.333 read as achieved** — supportive
   of the mechanism, and simultaneously a warning against printing the ladder as fact; and its
   coefficient at those densities is far below any airship-usable value.
3. **The node correction is the wrong kind of model.** "Carry no load, 15%" fails against
   measured joint-governed failure and a 27.8% measured mass fraction. The ×1.15 number itself
   remains what the cell page already admits: the largest unsourced number left.
4. **The joint that would settle it is undesigned.** Ochalek 2018 proves the design lineage
   exists and publishes no numbers; no source in this collection prices a 12-tube vacuum-cell
   node.
5. **The manufacturing routes are existence proofs, not designs.** Anisogrid rib modulus at
   100–300 µm tow scale: no data. Drawn-silica structural walls: index-inferior to M60J and
   never used structurally. Bonded bundle creep under multi-year load: no source found at this
   scale. And the two anchor papers for routes A and B were not read for this note.
6. **Hierarchy-of-assembly results (Smith 2025, ARMADAS) do not transfer to the strut wall.**
   They demonstrate logistics and assembled-lattice scaling at 10–80 kg/m³ — an order of
   magnitude above the design point, with the hierarchy in the robots' hands, not in the
   material.

## The retirement path

The A/B crush benchmark, on the project's stated gear (0.6 mm nozzle, PAHT-CF): specimen A, the
251 mm demonstrator strut with solid 1.2 mm wall; specimen B, same length and mass ±3%, wall
printed as two 0.6 mm skins joined by a triangulated corrugation; n ≥ 10 per arm, axial
compression to failure, potted ends. Readout: k = (P_B/P_A)_measured / (P_B/P_A)_theory from the
project's own cell model — one dimensionless number, which is the entire level-2 coefficient
question. **Prediction registered before testing: the model's 1.086 → 0.428 step implies an
equal-mass strength ratio ≈ 2.5×. k > 2.9 retires the level-2 claim; k ≤ 1.7 funds it.** A
second tier at 1/10 scale on a DLP printer (~100 µm features, where Meza's polymer result says
monolithic printing can be nearly coefficient-clean) checks whether k is a geometry/process
property or a scale property — which is precisely what the hierarchy ladder assumes and nobody
has checked for this geometry.

## Corrections this note forces on the page

- Label 0.428 kg/m³ a **prediction of this project**, unsupported by any published measurement,
  wherever it appears; the "floats" column inherits the label.
- Fix the Zheng citation: Nature Materials 15 (2016), not Science.
- Reclassify nodes from dead mass to potentially strength-governing elements; keep 10–30% as
  the measured band for discretely assembled levels (top measured: 27.8%).
- State the design rule as a requirement, not a preference: the level-2 wall must be
  stretch-dominated and continuously manufactured, because only that combination keeps the
  measured knockdown bands inside the 2.9× the margin can absorb.

## Clarification — 2026-10-05: the compression cap and the margin arithmetic

The original note above is retained as the 2026-08-10 research record. Its “margin
arithmetic” uses a superseded tensile-derived material cap. The current cell model
uses the M60J datasheet's composite compressive strength, 790 MPa (p. 1, SACMA SRM
1R-94, 60% fibre volume, #2500 epoxy), while leaving modulus and density unchanged.
Levels 2–4 now each cost 1.1243 kg/m³ with nodes and outer-envelope film; lift/mass
is 1.090 at sea level and 0.851 at 2,500 m. None reaches unity at working altitude.
Additional hierarchy cannot bypass the constituent compression floor, so the
original note's strength-reserve argument is no longer a current model result.
The [cell analysis](../analysis/vacuum-cell.md) records the old and new rows.

## Clarification — 2026-10-05: Meza's comparison is stiffness

The original research record above is retained. Meza et al., PNAS 112(37),
11502–11507 (2015), [doi:10.1073/pnas.1509120112](https://doi.org/10.1073/pnas.1509120112),
compare computed and measured **stiffness** in both passages behind this note's
68.5% and polymer 10.7% figures:

Printed p. 11503:

> The absolute computed stiffnesses were, on average, 10.7% lower for polymer, 30.2% higher for composite, and 68.5% higher for hollow samples compared with experimental data (Fig. 5), which hints that geometric and/or material imperfections contribute significantly to a reduction in the effective stiffness.

Printed p. 11506:

> The simulations overpredicted the stiffnesses of composite and hollow ceramic hierarchical lattices by 30.2% and 68.5%, respectively, which suggests that waviness-induced defects significantly contribute to this reduction.

Thus 1.685 (rounded here to 1.69) is a simulated-to-measured stiffness ratio
for those hollow specimens, not a measured strength knockdown. The polymer comparison
is also stiffness: the simulation underpredicts it. The original process band and margin
arithmetic must not treat these figures as measured strength coefficients.

Stiffness affects elastic buckling, but transferring this deficit to a failure-load
coefficient requires a failure-mode argument: the member's stiffness components, geometry,
load path, defect form and amplitude, and the governing instability or material failure
must correspond to the proposed specimen. A failure-load comparison or a validated
mechanistic model would then have to establish the transfer. This paper's stated
stiffness discrepancy alone does not do so, and it does not remove the separate
compression-strength floor in the current model.
