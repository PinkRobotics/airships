# MAINLINE-028b method and forward carry

Order `ord-admiral-rr2-mainline028b-joining-into-021b-1020`. Unit
`vacuum-mainline028b-joining-into-021b-1020`. This is a numerical estimate, not a
qualified assembly or an installed-hull safety factor. Times are measurements
only. The order asks for three fixed joining routes on 021b's reserve, fixed
stock-envelope panels, SR-200 properties, a 255 MPa compression sensitivity, and
the least set of remaining optimisms with all mode results.

## Frozen inputs and scope

The named 021b report's seven attached files were verified against their full
SHA-256 and byte counts, then copied under `intake/021b`. Six owned 028 files
were similarly checked against its final manifest and frozen under `intake/028`.
021b's full pins identify the 019 inputs/results and 014b core table; these were
also verified and copied. `intake/PINS.json` records all sixteen frozen pins.
No inherited executable was imported or run.

Use 021b's radius, pressure, lift, systems allowance, fixed reserve and 47-core
honeycomb candidate table. Reimplement all six continuum modes and the minimax
logarithmic definition of optimism usage. The candidate table includes explicitly
projected low-density aramid cores; their presence is retained for replication,
and their properties are not promoted to measured data.

`calculate.py` first retains 021b's Poisson ratio 0.33 to give an exact comparison.
`property_checks.py` repeats the search with 0.0752, the smaller of the historical
SR-200 sheet's in-plane Poisson ratios in NASA CR-194164 Table 2. The other
in-plane ratio is 0.0768. This is a scalar approximation to orthotropic sheet,
not a validated orthotropic shell calculation. Keep this material-model
qualification visible in any downstream use.

SR-200 density is 1850 kg/m³ and modulus 290 GPa, as in the current datasheet.
Its 345 MPa minimum is **tensile** yield; treating it as compressive is the explicit
021b assumption. The permitted face-strength optimism reaches the reported
379.2 MPa compression of a historical 1.96 mm SR-200 lot. The search holds modulus
at 290 GPa; full-endpoint evaluations pair the lot with its lower in-plane
modulus, 293.6 GPa. These are not thin formed-sheet allowables.

The 255 MPa sensitivity changes compression strength only, leaving the sheet
model's other inputs fixed. It is based on Materion's S-200-F prose, and does not
claim that S-200-F block is available as this sheet. No SR-200 lot strength is
transferred to that sensitivity.

## Mass accounting

Let A = 4πR², S = face mass plus core mass, f = core mass / S, and Q be physical
joining mass. Then:

    tf = (1-f) S / (2 A rho_face)
    tc = f S / (A rho_core)
    S + max(0.05 S, Q(tf,tc)) + 100 + 411.2989440716474 = 4889.442150186961 kg

Equivalently, the reserve is 411.2989440716474 kg plus
max(0, Q − 0.05 S). **Q replaces total physical joining; it is not added as an
extra reserve on top of the existing joint allowance.** When Q is below the
allowance, its unused balance remains reserved, following 021b. It is not
silently returned to the faces. There is no additional 5% buoyancy margin: this
is the commissioned 019/021b mass line, not 028's earlier 5% float-margin line.

The fixed reserve contains both mass and mass-equivalent environmental losses:
water 125.663706 kg, contamination 5 kg, temperature/pressure 213.036427 kg,
humidity 18.704390 kg, internal gas 48.894422 kg, and zero payload/system excess.
It is a specific optimistic service scenario, not an independently demonstrated
operational reserve.

Panels remain 0.6096 × 1.8288 m raw blanks. For a 30:1 scarf, overlap is 30 tf and
coincident hull seam length is:

    L = A [1/(0.6096 − 30tf) + 1/(1.8288 − 30tf)]

For the ideal autogenous seam, use zero overlap. L counts the hull pattern once;
both skins are already included in the per-metre joining expression:

    Q = 2 A (bond areal mass + primer areal mass)
        + L [2 tf sqrt(901) × 0.070 + 0.0005 tc × 500 + 0.002]

The first seam term is present only for bonded scarfs. The core splice and
sealing terms remain explicit owner projections inherited from 028. Film weights
are 0.015 × 0.45359237 / 0.09290304 kg/m² for AF 163-2U and 0.008 kg/m² for the
laboratory projection. Primer adds 0.005 kg/m² at both interfaces.

The laboratory primary case uses 028's lightest finite bill: 8 g/m² cell-edge
adhesive and ideal autogenous seams with full parent-strength retention. A
fourth case uses the same laboratory bond with the 30:1 scarf, to separate the
low bond mass from the ideal weld assumption. Neither Be assembly is qualified.

The 214.24 and 226.81 kg values in the order are reproduced at the old 028
geometry. They are not held constant after thicknesses change. Fixed panel size
has zero search usage, but its availability at sub-1.499 mm gauge remains
unverified: the manufacturer's full envelope applies to thicker stock.

## Modes and remaining optimisms

For each face, membrane force per width is N = pR/4 and compression demand N/tf.
Let h = tf + tc:

    sigma0 = E h / [R sqrt(1−nu²)]
    sigma_crimp = h² Gc / (2 tf tc)
    Vc = sigma0 / sigma_crimp
    Kc = 1−Vc/4 for Vc <= 2; otherwise 1/Vc

The six inherited mode SFs are:

1. Global buckling: gamma Kc sigma0 / (N/tf).
2. Face compression: sigma_face / (N/tf).
3. Core shear crimping: sigma_crimp / (N/tf).
4. Core crush: core crush strength / (p/2).
5. Face wrinkling: b k sqrt(E Ec tf/tc) / (N/tf), with b³+b=1.
6. Intracell dimpling: E (tf/cell)² / [(1−nu²)(N/tf)].

The inherited knockdown convention is gamma_today = 0.2 below Vc=2 and 1
at/above it. Its full projected value is 0.2 + 0.4 min(Vc,2).
Wrinkling goes from k=0.33 to 0.82. SR-200 face strength goes from the 345 MPa
proxy to the 379.2 MPa lot result. Usage is
max(0, log(required/today)/log(full/today)); a requirement above an unchanged
endpoint is infeasible. Do not call a usage above one feasible.

Every subset of these three remaining factors is searched. Factors outside a
subset remain at today's values. Minimize the largest usage, first selecting
the fewest factors that admit SF >= 1, then the smallest largest usage. Panel
and film are fixed choices and are not searchable factors. This count therefore
does not erase the qualifications or optimism embedded in those fixed choices.

The comparison search enforces the six inherited modes. The joint-aware search
also enforces 028's projected 10 MPa average scarf-shear screen:

    SF_scarf = 10 MPa / [(N/tf) × 30/901]

Its effective face-compression ceiling is 300.333333 MPa. Thus increasing the
SR-200 face-strength value cannot overcome that fixed seam screen. This assumed
10 MPa limit is not a measured Be scarf allowable. The ideal weld screen equals
parent face-compression SF; full strength retention remains a projection.

Flatwise bond tension, imperfection-driven bond shear, scarf peel, weld/HAZ
fracture, local seam buckling, thermal/cyclic degradation and leak-tightness
lack relevant measured allowables. They remain `null`/unknown. The minimum of
the six or seven numerical screens must never be substituted for overall
installed-hull SF.

## Search, checks and reproduction

Run with Python, NumPy and SciPy:

    python3 calculate.py
    python3 property_checks.py
    python3 make_report.py

Optionally run `python3 plot.py` with Matplotlib to reproduce the figures.
The report renderer combines the twelve numerical checks and verifies all
sixteen frozen input pins before writing the final VALIDATION.json.

The global search samples 6,001 core-mass fractions per candidate core, then
refines sampled local minima and feasible-interval boundaries. Each geometry
solves the nonlinear mass balance by 48 bisection steps. Boundary feasibility is
rooted on actual mode SF, not the zero plateau of the usage function. All 47
cores are searched for each subset. The two critical scarf cases are checked
again over all cores with 24,001 fractions.

Validation reproduces all six modes and the full mass account at 021b's sealed
floating point; reproduces all four 028 joining weights; checks selected mass
residuals and enforced mode bounds; and independently solves the selected mass
balances with a separately expanded scalar expression and Brent root finder.

A separate analytic rejection supports the 255 MPa sensitivity. Even with zero
core, S cannot exceed (lift − systems − fixed reserve)/1.05. Assign all S to the
faces: their compression SF is already below one. More gamma or wrinkling cannot
repair that material-budget bound. Full-endpoint optimized geometries are also
reported, with all six mode values and the seam screen.

## Carry forward

Final numeric answers are in `RESULTS.json` (021b Poisson convention) and
`PROPERTY-CHECKS.json` (sheet-based scalar Poisson value); CARD.md distinguishes
them. NFI.json records unresolved properties, bonds, seams, stock availability,
reserve and model assumptions. Verify the manifest pins before using them.

The actionable grounding step is a weighed curved SR-200/honeycomb panel and
representative joint, with post-form compression, actual gauge map, scarf shear
and peel, bond shear/flatwise strength, geometric imperfections and leak/thermal
performance. No such test or procurement is authorized or claimed here.

File one completion report to sciences, cc co, xo and the robotics seat. The
order names no successor; after filing, record SLEEPING and await queued work.
