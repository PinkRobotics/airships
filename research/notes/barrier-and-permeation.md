# Barrier and permeation — does a pumpless sealed cell hold its vacuum?

*Topic note across five sources rather than one. Read in full: IEA/ECBCS Annex 39 Subtask A
(2005); Li et al., Materials 2025 (CC BY, stored); Santucci et al., Molecules 2020 (CC BY,
stored); Bourim et al., Micromachines 2018 (CC BY, stored); Povilus et al. 2013 arXiv version
(catalogue only). Vendor figures from the Bambu PAHT-CF TDS (V3.0 at the catalogued URL — the
catalogue says V2; same numbers) and VSi Parylene's properties page. Tags: MEASURED /
DATASHEET / OOM.*

## The question, and a budget the project has not chosen

A cell is evacuated once, sealed, and never touched again. What must the skin be, and for how
long does the vacuum last?

Everything below is computed against **an allowed pressure rise of 10% of an atmosphere in 10
years** — and that budget is **a proposal of this note, not a project decision**. Nothing in
`figures.json` sets a degradation allowance; the print-reliability note independently invented
a different one (1%/90 days), and the two notes' headline verdicts ("closes with orders to
spare" vs "over budget") are not a contradiction but two invented budgets applied to two
different mechanisms — permeation through the skin here, outgassing from the plastic there.
Until the project adopts an allowance and puts it in `figures.json`, every margin figure in
this note is margin against an assumption.

For the demonstrator (354 mm cell, **44 L** — not the 45 L an earlier draft used; Rule 1),
a 10%/10 yr budget is 4,458 mbar·L, and the allowed rates work out to [arithmetic, cell
surface taken as the 0.752 m² cube-equivalent, ~12% conservative vs the Kelvin cell]:

| enclosure | volume | area | allowed leak | equivalent air transmission |
|---|---|---|---|---|
| 354 mm demonstrator | 44 L | 0.752 m² | 1.4×10⁻⁵ mbar·L/s | **1.6 cm³/(m²·day)** |
| 2 m flight cell | 8,000 L | 24 m² | 2.6×10⁻³ mbar·L/s | 9.1 cm³/(m²·day) |
| P-100 hull, barrier at the boundary only | 220,000 m³ | 22,592 m² | 71 mbar·L/s | ~270 cm³/(m²·day) |

Allowed flux scales with V/A: bigger cells are strictly easier, the demonstrator is the worst
case the project will ever face, and in the boundary-only architecture the requirement is lax
enough that ordinary packaging film is within an order of it. (An earlier draft put the hull
row at ~1,400 cm³/(m²·day) by using 5.2× the actual hull volume; corrected here against
`figures.json`'s 220,000 m³.) Interior partitions see vacuum on both sides and have no
permeation duty at all until a neighbour floods — their spec is breach containment, which is a
different question (E5).

## What the sources establish

**The vacuum insulation panel industry has already run our experiment.** A VIP is a sealed
evacuated envelope with no pump and a 25–50 year service life, and Annex 39 measured real
envelopes at our driving pressure (Δ ≈ 1 atm of air) by tracking internal pressure for a year.
MEASURED, 23 °C/50% RH: triple-metallised PET laminate faces pass 0.0034 (MF3) and 0.0087
(MF4) cm³ of air per m² per day; whole 1.0×0.6 m panels rise 1.0 and 0.5 mbar/yr. Against the
demonstrator's 1.6 cm³/(m²·day) requirement, the measured MF3 face rate is a factor of ~470.
DATASHEET, same report: an 8 µm aluminium-foil laminate is below OTR 0.0005; a low-priced
dual-metallised film (MF1) is 0.072; MF2 is 0.00062 cm³/(m²·day). In years-to-10%-loss on the
44 L cell [arithmetic on those rates]: MF1 ~220 yr, MF4 ~1,800 yr, MF3 ~4,700 yr, foil
>30,000 yr; a 25 µm parylene-C coat alone fails in under half a year (DATASHEET permeabilities,
VSi). **Permeation through a metallised face is a solved problem, with two orders of margin
even on a 10× stricter budget.**

Two caveats, and they are the load-bearing ones. First, **every VIP number above is
single-sourced** — one 2005 report, flagged as such by this round's audit; no second
measurement campaign of VIP envelope ATR was found. Second, the measured panels did not age by
face permeation: **MF3's 1.0 mbar/yr splits 0.87 perimeter vs 0.12 face** (MEASURED) — seams
dominate — and the accelerated condition (65 °C/75% RH) killed the majority of AF and MF2
panels in about a quarter year by **delamination of the laminate adhesives**, not by gas
transport. Scaled to the demonstrator, ~3 m of seam at MF3's measured 0.0090 cm³/(m·day) eats
only ~2% of the decade budget — at VIP seam quality. Seams and adhesive ageing, not faces, are
what actually retire this technology in the field.

**Inorganic barriers craze near 1% strain.** MEASURED, via the CC BY OLED-encapsulation
review (Li 2025): 20 nm ALD Al₂O₃ cracks at 1.19 ± 0.22% tensile strain, most metal oxides
near 1% — the primary source is Jen et al. 2011, which we did not read directly
(single-sourced, secondhand; flagged). The project's own cell analysis says a flat film
inflating into its bulge takes 4.12% membrane strain: any inorganic barrier applied flat and
then evacuated is destroyed on first pump-down. Pre-formed domes were already a design
requirement; the coating literature re-derives it. The same review carries the constructive
result: ALD/polymer dyad stacks hold WVTR 3.1×10⁻⁵ g/(m²·day) unchanged at 1.09% strain
(MEASURED) — alternating thin inorganic layers with polymer decorrelates the pinholes, which
is what a metallised laminate is as a roll good. The escape this project leans on — coat the
cell *after* evacuation, so the barrier never sees pump-down strain, leaving only thermal
cycling (~0.18% for Al on PA-CF at ±60 K — OOM: the 30 ppm/K CTE mismatch behind it is
unsourced) and **creep**, which no source in this round measured for PA-CF under multi-year
compression. Creep walking a coating through 1% is the one identified mechanism that reopens
a closed permeation budget (E3).

**Getters cannot buy air-tightness.** MEASURED (Santucci 2020): NEG alloys sorb active gases
only — H₂, H₂O, CO, CO₂, N₂, O₂ — and "rare gases are not sorbed at all". Argon is 0.93% of
the atmosphere, so the barrier must close the budget unaided. Capacity settles it anyway: even
at St707's *hydrogen* limit of 20 Torr·L/g, eating the 4,458 mbar·L budget takes ≥167 g — and
N₂/O₂ capacity per gram is far smaller — against a cell whose gross displacement lift is 42 g
at the 0.957 kg/m³ wall. Getters are outgassing janitors at 0.5–2 g, not air pumps. And NEG
activation is a 300–450 °C vacuum heat treatment (MEASURED practice, Bourim 2018) against a
polymer that melts at 225 °C (DATASHEET): if a getter is used at all it is CaO for water
(no activation) or an externally activated, vacuum-transferred pill.

## The part the budget does not cover: the gas the cell brings with it

The binding gate is not permeation, it is water. DATASHEET (Bambu PAHT-CF TDS V3.0):
saturated water absorption 0.88% at 25 °C/55% RH. The demonstrator cell is **0.948 kg of
printed PAHT-CF in the model's in-array convention, and ~1.32 kg as the standalone printed
article** (36 struts + 14 nodes) — an earlier draft used 650 g and understated this gate by
half. At saturation those masses hold 8.3–11.6 g of water = **11,300–15,700 mbar·L of vapour:
2.5–3.5× the entire ten-year budget**, released from the inside [arithmetic]. Vacuum bake-out
before sealing is not an optimisation; it is a gate, and 2–3 g of CaO (0.32 g H₂O/g
stoichiometric) is the cheap backstop for an imperfect bake.

Povilus et al. (MEASURED, but on **SLS PA12** — the extrapolation to FDM PAHT-CF is ours, not
theirs, and the audit flags it) is the only measured outgassing datum for printed polyamide:
3×10⁻⁸–4×10⁻⁷ mbar·L/(cm²·s) *after* cleaning and bake-out, residual gases atmospheric —
trapped air venting from the void network. Held constant on the demonstrator's surface that is
16–213× the decade-budget rate [arithmetic]; the rate decays, but it means month-one pressure
rise in any QA soak measures outgassing, not leaks. The same paper cuts against this note's
own bake prescription: their polyamide could only be baked at 65 °C — at 100 °C the vacuum
degraded and a residue appeared. The TDS's 80 °C/8–12 h drying line and that 65 °C ceiling
bracket the real schedule; E2 exists because no source gives it.

The related correction to the project's own table: "printed parts cannot hold vacuum — 4–7
orders" is right about the *part* and misleading about the *polymer*. Fully dense PA at this
wall thickness computes to centuries on this budget (OOM, handbook-class permeability); the
gap is inter-road porosity and trapped air. That strengthens the existing lever (the barrier
is a separate film) and the bake-under-vacuum step, which empties the voids that would
otherwise sit under the coating as virtual leaks.

## Barrier mass is a scale problem, and the demonstrator cannot represent flight

Computed from Annex 39's own layer specifications and bulk densities [arithmetic]: the
laminates that produced the measured numbers weigh 76–130 g/m² (MF1 76, MF2 79, MF3 105, AF1
130). Wrapped around a standalone 354 mm cell that is **1.3–2.2 kg per m³ of enclosed volume —
three to six times the 0.347 kg/m³ film line in the cell analysis, and 57–98 g against the
cell's 42 g of gross lift.** At 2 m cells the same skins are 0.24–0.39 kg/m³ — bracketing the
film line, not comfortably under it. (An earlier draft carried ~30 g/m² and "~0.42 kg/m³
minimum-gauge"; the as-specified constructions are heavier, and the correction moves the
conclusion from "heavy fraction" to "lift-negative at demonstrator scale".) Only
deposited-on-the-part stacks — 2–3 PVD metal layers with organic interlayers, 2–5 g/m², the
roll-laminate construction without the carrier film — scale to every cell size
(0.03–0.09 kg/m³ at 354 mm). This is also the audit's gap 4 in miniature: sealing at every
scale gets more expensive per m³ as cells shrink, and nobody has costed it below ~0.3 m.

So the demonstrator has two honest configurations: a VIP-transplant skin (buildable now,
measured-class performance, no pretence of flight-representative mass) or the in-situ PVD
stack — for which **no measured number exists on printed PAHT-CF anywhere; the audit is right
that its "MF1–MF2 class" expectation is argued only by construction identity.** That is
experiment E1, and it must be measured, not argued.

## What this project takes

- A sealed, pumpless vacuum cell is permeation-feasible with measured, shipping technology:
  requirement 1.6 cm³/(m²·day) at the worst-case scale, measured VIP faces at 0.0034.
- The failure modes to engineer against, in order: absorbed water (bake-out is a gate), seams
  and adhesive ageing (they aged the measured panels), creep-craze coupling (unmeasured),
  punctures/breach (E5) — and not face permeation.
- Process order matters and the project's is right: bake under vacuum, pre-form or
  coat-in-the-loaded-state, seal, then a month-long pressure-rise soak (0.84 mbar/month is
  the at-budget signal — the cell is its own leak detector; He mass-spec, 2–4 orders more
  sensitive than needed, only for fallout).

## Where the sources do not support what we would like

- Nothing here validates the 10%/10 yr allowance itself; it is this note's invention, awaiting
  a project decision in `figures.json`.
- All VIP performance rests on one 2005 report; Annex 39 is indoor construction data — no UV,
  rain, or outdoor thermal cycling on metallised laminates over decades, anywhere.
- The craze threshold is one 2011 primary read via a review; the CTE mismatch under it is
  unsourced (OOM).
- OLED figures are water-vapour rates on flat display substrates, not air rates on printed
  domes; the NEG paper is written for fusion tritium recovery; Povilus measured SLS PA12, not
  FDM PAHT-CF. Every cross-application is ours.
- No source measures: the in-situ PVD stack on printed PAHT-CF (E1), the bake schedule for
  1.2–1.4 mm CF-filled walls (E2), PA-CF creep under multi-year load (E3), seam ATR for our
  closure (E4), or film survival of a breach transient (E5).
