# MAINLINE-028b — joining on the 021b reserve

ESTIMATE · QUESTIONABLE / PROJECTION · no certified installed-hull SF.
Order `ord-admiral-rr2-mainline028b-joining-into-021b-1020`; unit
`vacuum-mainline028b-joining-into-021b-1020`.

**The least remaining adjustable set is {global-buckling gamma, wrinkling
coefficient} in all three commissioned joining cases. No singleton works.**
Keep the stock panel envelope fixed. The nominal and primer scarfs meet the
seven numerical screens only conditionally: their largest remaining usages are
0.97198 and 0.99608 after using the SR-200 sheet Poisson value. The laboratory
8 g/m² bond plus ideal weld needs 0.65147, but its Be bond and weld are unqualified.
The 255 MPa compression sensitivity has **no floating set**, even before core
mass is charged.

These are **two adjustable** factors. The AF cases already fix the original
O5 thin-film optimism at its full 0.015 lb/ft² value. In the original five-factor
bookkeeping the used set is therefore {O1 gamma, O2 wrinkling, fixed O5 film};
O3 face strength and O4 panel enlargement are unused. Do not count the fixed
thin-film choice as newly proven. The laboratory bond is a different process
outside that original film interval.

## SR-200 properties and the comparison with 021b

Use density 1850 kg/m³ and E=290 GPa. The 345 MPa datasheet minimum is **tensile**
yield; using it for compression is an explicit assumption, not a compressive
minimum. The full O3 endpoint is the historical SR-200 lot's 379.2 MPa compression,
with 293.6 GPa at full-endpoint evaluation. All selected least-set points leave
O3 unused. [Materion SR-200 datasheet](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6),
[NASA CR-194164 Tables 2–3](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf).

021b retained nu=0.33. For a sheet-based scalar approximation this card uses
nu=0.0752, the smaller historical in-plane value (the other is 0.0768).
This does not validate an orthotropic sphere. RESULTS.json preserves the exact
021b convention; PROPERTY-CHECKS.json supplies the sheet-property results used
below. All remaining assumptions and equations are in METHOD.md.

| Route | Max usage, six modes, nu=.0752 | Max usage, seam enforced, nu=.33 | Max usage, seam enforced, nu=.0752 |
| --- | --- | --- | --- |
| Nominal AF/scarf | 0.657494 | 0.906439 | 0.971978 |
| AF/scarf + primer | 0.662439 | 0.929701 | 0.996076 |
| Lab 8 g/m² + ideal weld | 0.651469 | 0.619431 | 0.651469 |
| Lab 8 g/m² + scarf | 0.651469 | 0.892819 | 0.957868 |

The fourth row separates a laboratory-light bond from the ideal-weld
assumption. It is an additional sensitivity, not a fourth commissioned material.
The first two six-mode optima have scarf SF only 0.93006 and 0.92691.
Enforcing 028's assumed 10 MPa mean-shear limit requires thicker faces. That
assumption is a numerical screen; peel and actual Be-joint strength remain unknown.

## The least-set points, including the seam screen

All four select Hexcel CR-III 5056 3/8-1.0: density 16.0185 kg/m³, Ec=103.421 MPa,
W shear modulus=46.884 MPa, crush=241.317 kPa, cell=9.525 mm. These inherited
typical values are QUESTIONABLE. [Hexcel CR-III data sheet](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).
R=10 m, pressure=95,460.8379 Pa, lift=4,889.44215 kg. Raw panel blanks stay
0.6096 × 1.8288 m; scarf overlap is deducted from both dimensions.

| Route | Face mm | Core mm | Vc | Physical joining kg | 5% allowance kg | Joint excess kg | Unused allowance kg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nominal AF/scarf | 0.794624 | 23.2372 | 0.953214 | 215.742 | 208.120 | 7.622 | 0.000 |
| AF/scarf + primer | 0.794624 | 22.6342 | 0.952375 | 227.880 | 207.513 | 20.367 | 0.000 |
| Lab 8 g/m² + ideal weld | 0.742123 | 35.7248 | 0.901941 | 50.151 | 208.483 | 0.000 | 158.332 |
| Lab 8 g/m² + scarf | 0.794624 | 23.5978 | 0.953696 | 52.041 | 208.483 | 0.000 | 156.442 |

The order's 214.24/226.81 kg values are reproduced at the old 028
geometry. At these resized points they become **215.742/227.880 kg**.
Joining is recomputed from the actual face/core thicknesses. The laboratory
route becomes 50.151 kg; its unused allowance stays reserved.

The fixed 019 reserve stays 411.298944 kg and systems stay 100 kg. The mass line is:

    faces + core + max(0.05 × (faces + core), actual joining)
        + 100 + 411.298944 = 4889.442150 kg

Only the excess above the joint allowance enters the reserve. Adding the whole
joining bill as excess would double-count it. There is no extra 5% float-margin
charge on this commissioned 019/021b budget.

| Route | Faces kg | Core kg | Base joint allowance kg | Fixed reserve kg | Excess reserve kg | Systems kg | Charged total kg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nominal AF/scarf | 3694.650 | 467.751 | 208.120 | 411.299 | 7.622 | 100.000 | 4889.442 |
| AF/scarf + primer | 3694.650 | 455.613 | 207.513 | 411.299 | 20.367 | 100.000 | 4889.442 |
| Lab 8 g/m² + ideal weld | 3450.542 | 719.118 | 208.483 | 411.299 | 0.000 | 100.000 | 4889.442 |
| Lab 8 g/m² + scarf | 3694.650 | 475.010 | 208.483 | 411.299 | 0.000 | 100.000 | 4889.442 |

The six component columns sum to the charged total before rounding. The fixed reserve includes environmental mass-equivalent losses as well as mass.

| Route | Core bond kg | Primer kg | Scarf film kg | Core splice kg | Seal kg | Hull seam m |
| --- | --- | --- | --- | --- | --- | --- |
| Nominal AF/scarf | 184.063 | 0.000 | 9.489 | 16.507 | 5.683 | 2841.519 |
| AF/scarf + primer | 184.063 | 12.566 | 9.489 | 16.079 | 5.683 | 2841.519 |
| Lab 8 g/m² + ideal weld | 20.106 | 0.000 | 0.000 | 24.548 | 5.497 | 2748.550 |
| Lab 8 g/m² + scarf | 20.106 | 0.000 | 9.489 | 16.763 | 5.683 | 2841.519 |

AF film is 0.015 lb/ft² per bond; primer adds 5 g/m² at both bonds.
The lab's 8 g/m² cell-edge deposition is demonstrated on other adherends and
core, not on this Be/aluminium assembly. Core splice and seal quantities remain
028 projections. [3M AF 163 film weights](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf),
[Rion et al. 2008 laboratory process](https://infoscience.epfl.ch/server/api/core/bitstreams/28b8cc7a-f046-4da3-9fcc-5d5ad3c52a9d/content).

## Each factor

| Route | Gamma needed / full | Gamma × today | Gamma usage | Wrinkle k needed | k × .33 | k usage | Face MPa / usage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nominal AF/scarf | 0.564164 / 0.581286 | 2.820818 | 0.971978 | 0.434628 | 1.317054 | 0.302564 | 345 / 0 |
| AF/scarf + primer | 0.578524 / 0.580950 | 2.892622 | 0.996076 | 0.428952 | 1.299853 | 0.288121 | 345 / 0 |
| Lab 8 g/m² + ideal weld | 0.391500 / 0.560776 | 1.957498 | 0.651469 | 0.597089 | 1.809362 | 0.651469 | 345 / 0 |
| Lab 8 g/m² + scarf | 0.555911 / 0.581478 | 2.779554 | 0.957868 | 0.437987 | 1.327234 | 0.311024 | 345 / 0 |

Gamma today is 0.20 at these Vc<2 points; full is the projected
018 curve, 0.20+0.40Vc. Wrinkling today/full is 0.33/0.82. Usage is the log-share
of that interval required to meet SF=1. Panel enlargement factor is 1 and O4
usage is 0 in every case. AF film mass is half the old 0.030 lb/ft² baseline,
so its **fixed O5 usage is 1**. The lab's 8 g/m² is 18.309 times lighter than
that baseline by areal mass, but is not an AF-film interpolation.

The primer point requires gamma=0.578524 against full=0.580950 at E=290 GPa:
only about 0.4% remains in the allowed log stretch. Larger gamma is not a
measured capability. The scarf points demand 300.333 MPa face compression,
not the full 345 MPa proxy. The ideal weld point requires at least 93.212%
parent compression retention; 80% retention would give seam SF=0.85826
at that selected geometry.

## Every computed mode at the needed values

| Route | Global | Face | Crimp | Crush | Wrinkle | Dimpling | Scarf / ideal weld |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nominal AF/scarf | 1.000000 | 1.148724 | 2.441308 | 5.055822 | 1.000000 | 6.758508 | 1.000000 |
| AF/scarf + primer | 1.000000 | 1.148724 | 2.382148 | 5.055822 | 1.000000 | 6.758508 | 1.000000 |
| Lab 8 g/m² + ideal weld | 1.000000 | 1.072827 | 3.656462 | 5.055822 | 1.000000 | 5.505449 | 1.072827 |
| Lab 8 g/m² + scarf | 1.000000 | 1.148724 | 2.476690 | 5.055822 | 1.000000 | 6.758508 | 1.000000 |

The seam entry is mean scarf shear for scarf cases and parent-strength
compression retention for the ideal weld. All are conditional screens.
Face/core flatwise tension, imperfection-driven shear, seam peel/HAZ failure,
local seam buckling, thermal/cyclic debonding and leak-tightness are **unknown**.
Overall installed-hull SF therefore remains **unknown**, not 1.

At each selected point, returning gamma to 0.20 while holding the other full
endpoints gives the following least screen. Separately reoptimizing with every
remaining named endpoint at full gives the right column; these are different
geometries and do not constitute proven margin.

| Route | At selected point, full except gamma=.20 | Reoptimized, all endpoints full |
| --- | --- | --- |
| Nominal AF/scarf | 0.357514 | 1.006358 |
| AF/scarf + primer | 0.348641 | 1.002803 |
| Lab 8 g/m² + ideal weld | 0.515329 | 1.229648 |
| Lab 8 g/m² + scarf | 0.362820 | 1.008206 |

## Every subset of the remaining adjustable factors

| Subset | Nominal AF/scarf | AF/scarf + primer | Lab 8 g/m² + ideal weld | Lab 8 g/m² + scarf |
| --- | --- | --- | --- | --- |
| {} | infeasible | infeasible | infeasible | infeasible |
| {gamma} | 1.293662 >1 | 1.304482 >1 | 1.291871 >1 | 1.291871 >1 |
| {k} | infeasible | infeasible | infeasible | infeasible |
| {face} | infeasible | infeasible | infeasible | infeasible |
| {gamma, k} | 0.971978 ✓ | 0.996076 ✓ | 0.651469 ✓ | 0.957868 ✓ |
| {gamma, face} | 1.293662 >1 | 1.304482 >1 | 1.291871 >1 | 1.291871 >1 |
| {k, face} | infeasible | infeasible | 1.285124 >1 | infeasible |
| {gamma, k, face} | 0.971978 ✓ | 0.996076 ✓ | 0.651469 ✓ | 0.957868 ✓ |

A value above one needs more than the named full improvement.
“Infeasible” means the unchanged modes reject all sampled/refined points.
The denser all-core search confirms the critical two-factor results. In the
commissioned fixed-route problem the minimum cardinality is two; the face
endpoint does not reduce it.

## S-200-F's 255 MPa compression as a sensitivity

Materion describes roughly 255 MPa compression for S-200-F.
This run changes only the strength to 255 MPa; it does not mix the SR-200 lot's
379.2 MPa into that sensitivity. [Materion design guide, p.4](https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74).

No subset floats. With the full structural budget placed into faces and **zero
core**, the compression SF upper bound is only **0.958217**. Any real core or
joint excess makes that worse. This independently rules out success regardless
of the gamma/wrinkling search.

Reoptimizing at the permitted full gamma and k=0.82 gives these maxima and all
their mode values (nu=.0752, E=290 GPa):

| Route | Best SF | Face mm | Core mm | Global | Face | Crimp | Crush | Wrinkle | Dimpling | Seam |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nominal AF/scarf | 0.869846 | 0.814081 | 18.8840 | 0.869846 | 0.869846 | 2.018302 | 5.055822 | 2.170201 | 7.267212 | 1.024485 |
| AF/scarf + primer | 0.866848 | 0.811275 | 18.9086 | 0.866848 | 0.866848 | 2.020144 | 5.055822 | 2.157586 | 7.192345 | 1.020955 |
| Lab 8 g/m² + ideal weld | 0.870902 | 0.815069 | 18.8753 | 0.870902 | 0.870902 | 2.017656 | 5.055822 | 2.174654 | 7.293723 | 0.870902 |
| Lab 8 g/m² + scarf | 0.870902 | 0.815069 | 18.8753 | 0.870902 | 0.870902 | 2.017656 | 5.055822 | 2.174654 | 7.293723 | 1.025729 |

## Verification and carry forward

All 47 inherited honeycomb candidates were searched. Twelve aggregate numerical
checks passed: exact reproduction of 021b's six modes and mass line, all four
028 joining masses, feasibility and mass residuals, the analytic 255 MPa bound,
the 24,001-point all-core refinement of both critical scarf subsets, and
independent scalar mass roots. Maximum selected mass discrepancy is below
1e-8 kg. All 16 upstream file pins match.

No repository source was changed, no inherited executable ran, and no other
seat was contacted outside the queue. The calculation, source pins, full subset
results, mode results and unknowns are supplied in the JSON files and scripts.
`NFI.json` identifies what still needs evidence. `METHOD.md` records exact
formulas and reproduction steps. Timing is measured only; no work limit applied.

The next useful evidence is a weighed curved panel and representative joint
with post-form sheet compression, actual gauge, bond shear/flatwise strength,
scarf shear/peel or weld retention, geometric imperfections, and leak/thermal
performance. Thin-stock availability remains open even though panel size is
fixed in this search. No successor is named by this order: file this report
and await the robotics seat's next queued assignment.
