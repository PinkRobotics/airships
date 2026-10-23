# MAINLINE-053 — settled thermal specification and consequences

**The arithmetic discrepancy is resolved. Physical boundary qualification remains open.**
An independently written simultaneous energy solver reproduces all 118,499
selected owner/CHECK-040/CHECK-048 comparisons after their actual boundary terms
are specified. Four explicit thermal alternatives are filed for R10–30.
At R10/12/15, no endpoint float decision, minimum-axis choice or tied minimum-axis
set changes. Resizing costs at most 4.388925 kg.
Previously sized geometries do cross the scarf screen; the resized witnesses
pass the declared scalar constraints.

Every inherited material property is **QUESTIONABLE** and every installed
geometry, optical transfer, process and performance prediction is **PROJECTION**.
Installed hull safety factor and flight qualification remain unknown.
The brief is complete and names no immediate successor; stop and file.

The complete equations, units and omitted physics are in
[SPECIFICATION.md](c32791ae36578213-SPECIFICATION.md) and [METHOD.md](31dcdce0873b7959-METHOD.md).
[INPUTS.json](e3a9091fe9ab8b5b-INPUTS.json), [INPUT-PINS.json](696bfd8c4d00c3ba-INPUT-PINS.json) and
[EVIDENCE.json](da566fd9bcd1243c-EVIDENCE.json) make their provenance explicit.

**Why owner and checkers differed.** The owner uses a temperature-dependent
convection floor, h=max(hforced,1.32 max(|To−Ta|,.05)^.25), and adds
4×.20×σ×average(Ti)³ to solid-core conductance. Both checkers use forced
convection alone and omit that gap term. At the historical R10 white-finish
geometry, tc=.02210679007353296 m and foil density 2640 kg/m³, the independent
128-node reproduction gives:

| Convection / core transport | Face gradient K | Day rise K | Day–night swing K |
| --- | --- | --- | --- |
| Forced / conduction | 0.464608894 | 18.476891625 | 33.640781944 |
| Mixed / conduction | 0.426155555 | 17.125220272 | 31.120115857 |
| Forced / gap .20 | 0.451215439 | 18.475049422 | 33.638308050 |
| Mixed / gap .20 | 0.413901181 | 17.123766274 | 31.118178070 |

For example, the gradient difference .464608894→.413901181 K and swing
33.640781944→31.118178070 K follow from changing those terms.
The extra core-gap exchange and the hull's internal enclosure radiation are
distinct heat paths; their joint inclusion is not automatically double counting.
The gap coefficient nevertheless remains unqualified.

A separate legacy projection issue is also resolved. Raw 37-midpoint
projection leaks a constant temperature into degrees 2–6. CHECK-048 retained
this for night, giving 226.884841 K of apparent curvature temperature in its
reference legacy row; the owner-derived 048 night row removed the mean
(2.585175 K under its different boundary). Those legacy rows differ in both
boundary and projection. Neither raw-field curvature is carried forward.
All settled tables remove the mean before projection.

The later in-band order
`ord-admiral-rr2-mainline053-fold-boundary-reply-1020` supplies the owner's
[BOUNDARY-REPLY.md](2a3c8f34e94934a1-BOUNDARY-REPLY.md). Its convection,
conductance, normalized averages and outer balance agree with this
reconstruction. All 46 supplied temperature and screen entries
match the already completed independent results within declared tolerance;
[BOUNDARY-REPLY-COMPARISONS.json](3d7ed1becf49fd34-BOUNDARY-REPLY-COMPARISONS.json) records
each comparison. Current and legacy densities and iteration conventions are
kept distinct. The reply's legacy projection prose is read with its numerical
attachment: the later 048 night diagnostic removes the mean, while the day
diagnostic retains the raw projection. Different solver iteration counts
do not signify different physical solutions.

| Compared product | Comparisons | Pass | Largest absolute difference |
| --- | --- | --- | --- |
| owner048_screen | 325 | 325 | 1.75e-07 |
| checker048_screen | 325 | 325 | 6.31e-12 |
| owner048_full_table | 103389 | 103389 | 3.93e-09 |
| owner040_full_table | 7230 | 7230 | 3.01e-09 |
| checker040_full_table | 7230 | 7230 | 5.54e-13 |

These are field-by-field arithmetic comparisons, not independent material
observations. The compressed comparison ledger records values and tolerances;
[THERMAL-REPRODUCTION-DIFFERENCES.json](37517e5f3dc66819-MISMATCHES.json)
is empty. Upstream source was inspected to settle specification omissions,
but no upstream executable was imported or run.

**The selected specification is a disclosed family.** Air is 284.9 K at
2 m/s, solar flux 970 W/m², day/night sky 275/260 K, ground 284.9 K, inner
emissivity .20, and solar zenith aligned with the sphere's axis. Sky/ground
view factors are (1±μ)/2. The selected multilayer CCAg/ITO pair is .09/.80.
Solid-core transport is 130ρcore/(2700tc), with zero or .20 gap augmentation.
The two convection readings crossed with these two gap readings give the
four labels below. None is a certified bound on real operation.

Whitaker's primary sphere fit reports Re 3.5–76,000; the inherited hull use
at 2.61–7.83 million is extrapolation. No supplied evidence validates the
inherited natural-convection floor for this sphere.
[Whitaker, 1972](https://www.researchgate.net/profile/Stephen-Whitaker-3/publication/229709417_Forced_convection_heat_transfer_correlations_for_flow_in_pipes_past_flat_plates_single_cylinders_single_spheres_and_for_flow_in_packed_beds_and_tube_bundles/links/59d73bda0f7e9b42a6b0694a/Forced-convection-heat-transfer-correlations-for-flow-in-pipes-past-flat-plates-single-cylinders-single-spheres-and-for-flow-in-packed-beds-and-tube-bundles.pdf).
NASA's bonded honeycomb work distinguishes conduction, radiation and interface
resistance; it does not supply the missing installed CR-III/AF163/Be
conductance. [NASA honeycomb study](https://ntrs.nasa.gov/api/citations/19680009019/downloads/19680009019.pdf).
The transparent conduction-only rows and inherited gap rows therefore remain
side by side.

Settled tables use 256 split-Gauss nodes, explicit poles, mean-removed
degrees 2–6 and polynomial curvature extrema. Each finish/model/radius has
241 core thicknesses. [THERMAL-TABLES.csv](f6544e2741e75386-THERMAL-TABLES.csv) contains all
9,640 thickness rows; the JSON retains solver diagnostics.
The following multilayer-finish reference rows use tc=.02210679007353296R/10 m.
Gradient means the largest absolute day/night face difference; swing means
maximum daytime minus minimum nighttime outer temperature. Curvature is a
temperature-derived screen, not a temperature rise.

| Boundary | R m | tc mm | Gradient K | Rise K | Swing K | Cold K | Curvature K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Forced / conduction | 10 | 22.1068 | 0.186432 | 6.522550 | 21.008173 | 270.414377 | 27.717837 |
| Forced / conduction | 12 | 26.5281 | 0.226836 | 6.650544 | 21.486630 | 270.063914 | 28.212171 |
| Forced / conduction | 15 | 33.1602 | 0.287581 | 6.802726 | 22.057552 | 269.645173 | 28.773932 |
| Forced / conduction | 20 | 44.2136 | 0.388564 | 6.992444 | 22.770310 | 269.122134 | 29.421305 |
| Forced / conduction | 30 | 66.3204 | 0.587450 | 7.250150 | 23.733666 | 268.416485 | 30.168066 |
| Mixed / conduction | 10 | 22.1068 | 0.183825 | 6.435357 | 19.793887 | 271.541470 | 27.640212 |
| Mixed / conduction | 12 | 26.5281 | 0.219613 | 6.439352 | 19.803895 | 271.535456 | 28.293043 |
| Mixed / conduction | 15 | 33.1602 | 0.272919 | 6.444573 | 19.815975 | 271.528598 | 29.045022 |
| Mixed / conduction | 20 | 44.2136 | 0.359838 | 6.454509 | 19.835615 | 271.518894 | 29.083870 |
| Mixed / conduction | 30 | 66.3204 | 0.526541 | 6.476097 | 19.874962 | 271.501135 | 28.823843 |
| Forced / gap .20 | 10 | 22.1068 | 0.181113 | 6.521775 | 21.006722 | 270.415052 | 27.726112 |
| Forced / gap .20 | 12 | 26.5281 | 0.219151 | 6.649403 | 21.484492 | 270.064911 | 28.224042 |
| Forced / gap .20 | 15 | 33.1602 | 0.275593 | 6.800908 | 22.054137 | 269.646771 | 28.792304 |
| Forced / gap .20 | 20 | 44.2136 | 0.367515 | 6.989175 | 22.764136 | 269.125038 | 29.453261 |
| Forced / gap .20 | 30 | 66.3204 | 0.542021 | 7.242877 | 23.719815 | 268.423062 | 30.236260 |
| Mixed / gap .20 | 10 | 22.1068 | 0.178582 | 6.434652 | 19.792669 | 271.541983 | 27.648475 |
| Mixed / gap .20 | 12 | 26.5281 | 0.212177 | 6.438353 | 19.802171 | 271.536182 | 28.304815 |
| Mixed / gap .20 | 15 | 33.1602 | 0.261553 | 6.443048 | 19.813341 | 271.529706 | 29.063479 |
| Mixed / gap .20 | 20 | 44.2136 | 0.340374 | 6.451899 | 19.831103 | 271.520796 | 29.116569 |
| Mixed / gap .20 | 30 | 66.3204 | 0.485916 | 6.470656 | 19.865517 | 271.505139 | 28.891846 |

The reference white finish is also retained in
[THERMAL-REFERENCE.csv](4215b8659f775575-THERMAL-REFERENCE.csv), with full angular face
profiles in [REFERENCE-THERMAL-ROWS.json](5a9d19912fc74fd1-REFERENCE-THERMAL-ROWS.json).
These are separate equilibria; thermal inertia, lateral conduction, actual
sun angle, adhesive/contact resistance, inner obstructions, wet optics and a
joint weather/thermal mission remain open.

**Finish screening is unchanged in outcome.** At the original R10 geometry,
the inherited rigid shear-lag day threshold is 1.678282710 and the cycle
threshold is 1. The separate compliant-core 200°F free-edge screen uses
minimum W shear rather than the typical value used by the historical screen.

| Boundary | Day factor | Cycle factor | 200°F free-edge factor | Day / cycle |
| --- | --- | --- | --- | --- |
| Forced / conduction | 4.289012 | 1.331639 | 1.066408 | pass / pass |
| Mixed / conduction | 4.347124 | 1.413330 | 1.079067 | pass / pass |
| Forced / gap .20 | 4.289522 | 1.331731 | 1.066415 | pass / pass |
| Mixed / gap .20 | 4.347601 | 1.413417 | 1.079073 | pass / pass |

All four multilayer rows pass these stated screens. NASA's multilayer CCAg
class supports the optical-pair transfer, but does not qualify this exact
coating on Be after outdoor moisture and aging.
[NASA Goddard, slide 39](https://ntrs.nasa.gov/api/citations/20180002012/downloads/20180002012.pdf).
The 13 candidate finishes under all four boundaries are in
[SETTLED-FINISH-SCREEN.json](54895baecd674087-SETTLED-FINISH-SCREEN.json).

**Payload consequences preserve the full mass account.** The following
numbers use the 028b gamma/Q endpoint, today's face tuple and its already
favorable .015 lb/ft² interface film. This is mask 11: gamma+Q+film in the
four-axis accounting. Each geometry is resized with the 30.341397319:1 scarf,
200°F cure, retained 5% joining floor and projected ground-bake drying route.
The bill retains 0.1 kg/m² exterior water, material moisture, coating,
structural primer, pad, systems, gas, contamination and weather headroom.
The optimistic weather label is inherited from the atmospheric account;
it changes pressure and buoyancy, not the thermal boundary.

| Cure in global/crimp | R / weather | Filed kg | Forced/conduction kg | Mixed/conduction kg | Forced/gap kg | Mixed/gap kg |
| --- | --- | --- | --- | --- | --- | --- |
| no | R10 / ISA | 124.261888 | 123.726891 | 124.163690 | 123.824750 | 124.260142 |
| no | R10 / optimistic | -23.921160 | -24.458591 | -24.020957 | -24.359129 | -23.922934 |
| no | R12 / ISA | 336.966617 | 335.562157 | 336.714220 | 335.819400 | 336.963143 |
| no | R12 / optimistic | 73.104546 | 71.691509 | 72.848079 | 71.953017 | 73.100997 |
| no | R15 / ISA | 832.294647 | 828.337651 | 831.544480 | 829.121083 | 832.287076 |
| no | R15 / optimistic | 316.854323 | 312.865769 | 316.091790 | 313.661957 | 316.846524 |
| yes | R10 / ISA | 118.694825 | 118.088578 | 118.594926 | 118.188125 | 118.692997 |
| yes | R10 / optimistic | -29.257217 | -29.863021 | -29.358656 | -29.761952 | -29.259078 |
| yes | R12 / ISA | 327.176036 | 325.606508 | 326.919327 | 325.868218 | 327.172431 |
| yes | R12 / optimistic | 63.720186 | 62.148681 | 63.459553 | 62.414379 | 63.716507 |
| yes | R15 / ISA | 813.155245 | 808.781562 | 812.392615 | 809.578126 | 813.147416 |
| yes | R15 / optimistic | 298.508108 | 294.119183 | 297.733541 | 294.928213 | 298.499990 |

The first six rows retain the original exclusion of balanced cure compression
from global/crimp demand. The final six include it, as the later CHECK-040/048
fold requires for the conservative scalar comparison. These mechanical
branches are separate from the four thermal readings. Ground bake is a
conditional process credit, not an installed qualification.

[PAYLOAD-AND-BOND.csv](d6280f3e1fc3d960-PAYLOAD-AND-BOND.csv) gives all 360 configurations,
including actual joining and retained-floor accounts and dry-gas/bake/sorbent
routes. The five ACCOUNT files retain every geometry, material property,
mass item, limit and least-set witness. [SUBSET-ENDPOINTS.csv](4b8f0ebf6a12321a-SUBSET-ENDPOINTS.csv)
contains all 5,760 endpoint witnesses. Across four alternatives and 72
configurations, none of the 4,608 endpoint comparisons changes float sign.

**Least optimism sets persist, with slightly larger usage.** Usage is the
common logarithmic interpolation fraction on the selected axes, not a
fractional payload or safety factor. This table shows the reference
forced/conduction alternative against the filed thermal table; all other
alternatives and tied minimum sets are retained in the machine-readable data.

| Cure included | R / weather | Minimum axes | Filed usage | Forced/conduction usage | Change |
| --- | --- | --- | --- | --- | --- |
| no | R10 / ISA | gamma+Q+film | 0.833075518 | 0.833875933 | +0.000800415 |
| no | R10 / optimistic | none floats | — | — | — |
| no | R12 / ISA | gamma+Q | 0.884705366 | 0.886099070 | +0.001393704 |
| no | R12 / optimistic | gamma+Q+film | 0.928594829 | 0.930035335 | +0.001440506 |
| no | R15 / ISA | gamma+Q | 0.720756663 | 0.722785202 | +0.002028539 |
| no | R15 / optimistic | gamma+Q | 0.941832568 | 0.943836790 | +0.002004222 |
| yes | R10 / ISA | gamma+Q+film | 0.842794206 | 0.843699146 | +0.000904939 |
| yes | R10 / optimistic | none floats | — | — | — |
| yes | R12 / ISA | gamma+Q | 0.895849721 | 0.897392900 | +0.001543179 |
| yes | R12 / optimistic | gamma+Q+film | 0.938736760 | 0.940312881 | +0.001576121 |
| yes | R15 / ISA | gamma+Q | 0.733994276 | 0.736243583 | +0.002249307 |
| yes | R15 / optimistic | gamma+Q | 0.951827307 | 0.953999981 | +0.002172674 |

At retained-floor/bake R10 optimistic weather, no allowed subset floats,
including the full four-axis endpoint. That failure is not repaired by
thermal reconciliation.

**A frozen-geometry bond pass does change.** Every filed endpoint is almost
exactly scarf-limited, so the updated thermal demand takes all 288 frozen
scarf checks below one under the declared 2e−7 comparison tolerance.
There are also 85 new frozen global-screen crossings.
Free-edge and cell-wall screens remain above one. Results by alternative:

| Boundary | Frozen scarf SF range | New global failures / 72 | Worst edge usage after resize | Worst wall usage after resize | Payload change range kg |
| --- | --- | --- | --- | --- | --- |
| Forced / conduction | 0.999634186–0.999831090 | 36 | 0.945244 | 0.421736 | -4.388925 to -0.533371 |
| Mixed / conduction | 0.999930093–0.999968634 | 13 | 0.926858 | 0.413532 | -0.774566 to -0.097897 |
| Forced / gap .20 | 0.999707199–0.999862353 | 36 | 0.945228 | 0.421729 | -3.579894 to -0.435803 |
| Mixed / gap .20 | 0.999999296–0.999999440 | 0 | 0.926847 | 0.413527 | -0.008132 to -0.001747 |

The mixed/gap deficit is only about six parts in ten million, a numerical
convention effect whose physical significance is far below the open material
uncertainty. The largest scarf deficit is about 0.0366%. It would be
incorrect either to claim unchanged frozen pass status or to turn that
numerically small branch difference into a demonstrated physical failure.
Resizing restores scarf and global screens; added face thickness across all
alternatives ranges from sub-nanometre numerical adjustments to 0.441010 μm.
The new core/edge usages stay below one.

For the cure-inclusive, retained-floor/bake reference alternative, balanced
cure compression and geometry are:

| R / weather | Filed cure compression MPa | Forced/conduction MPa | Change MPa | New tf mm | New tc mm |
| --- | --- | --- | --- | --- | --- |
| R10 / ISA | 3.246622 | 3.284272 | +0.037649 | 0.809733 | 22.602197 |
| R10 / optimistic | 3.135818 | 3.172206 | +0.036388 | 0.830534 | 22.391828 |
| R12 / ISA | 3.245211 | 3.294142 | +0.048930 | 0.971955 | 27.112913 |
| R12 / optimistic | 3.134468 | 3.181762 | +0.047294 | 0.996920 | 26.860676 |
| R15 / ISA | 3.243091 | 3.305338 | +0.062247 | 1.215444 | 33.873150 |
| R15 / optimistic | 3.132439 | 3.192608 | +0.060169 | 1.246657 | 33.558230 |

This is a conditional stress calculation. The continuous compliant-core
field, free-edge transfer, scarf-average shear and foil yield proxy do not
establish adhesive peel, coincident loads, a finished assembly allowable or
full-hull stability. The pinned 037b qualifications remain open.

**Verification and custody.** All 31,460 accounting checks pass,
including exact mass conservation, resized limits, cure-force balance,
an independent closed scarf root, lower-cardinality favorable-E bounds,
288 direct thermal guard checks and 60 denser geometry searches.
The maximum difference from the 72 original payload endpoints is
0.000090740 kg; the 36
fixed-geometry bill reproductions agree within 1.819e−12 kg. Doubling the
core grid changes primary payloads by at most
0.000103434 kg.

There are eight energy/quadrature invariants. Increasing thermal quadrature
from 256 to 1024 changes the sampled extrema/swing by less than
9.48597801e-07 K
and curvature temperature by at most
0.000149089168 K.
Across complete settled tables, maximum local energy residual is
4.35e-11 W/m². The retained 1.002 guard
covers numerical interpolation in all directly checked resized points;
it does not bound physical model error.

All heavy runs used one-core, 1 GiB simjob admission. Four refusals were
retried unchanged; a serialization failure was corrected and retained in
the execution record. Later thermal runs completed the R20/30 reproduction
coverage. [TIMING.json](903074057a233f3b-TIMING.json) measures elapsed time without imposing
a work budget. [VALIDATION.json](035d20a3e472156a-VALIDATION.json), MANIFEST.json [source link unavailable in this public projection]
and the report pins provide delivery custody.

All 142 frozen inputs retain their intake hashes. One live original,
COMMON.md, gained an explicit heavy-run simjob requirement after intake.
The runs already comply. Its pinned version, later copy, exact difference
and disposition are preserved in [SOURCE-DRIFT.json](98f16677a4e1c399-SOURCE-DRIFT.json);
the other 141 live originals remain unchanged at delivery validation.

Nine new open, nonblocking NFI groups and six inherited registers preserve
the unresolved physics and assembly evidence. Only the local arithmetic and
legacy-projection discrepancies are resolved. No installed hull safety
factor is asserted. No supplier or other seat was contacted out of band.

Thermal choices and payload consequences [source link unavailable in this public projection]

The figure is also supplied as [SVG](9cb06b480587a946-THERMAL-SETTLEMENT.svg) and
PDF [source link unavailable in this public projection].
