# R3-I041 — paid receiver ladder-saddles

This fixed construction adds four steel ladder-saddles between the existing
same-rack, same-x lower and upper receiver levels. It preserves the complete
[corrected raised crown](../R3-I034/README.md), including its supports, routes,
guides, receiver stock and retained members. It takes no retirement credit.
The question is whether a fully paid two-level receiver path is a useful next
construction candidate. Compatible reactions and physical float remain **NOT
SHOWN**. Stock payment does not establish connection capacity.

The saved inputs are in [baseline.json](baseline.json), selected dimensions and
provenance in [sources.json](sources.json), and the single fixed calculator in
[saddle.py](saddle.py). Its output is [saddle.json](saddle.json). The baseline is
assembled from the predecessor's saved JSON before calculation; `saddle.py
--write` verifies that input and writes only the saddle result. The generated
path declaration includes both data artifacts.

## Recorded result

The fixed run adds **20242.768226652046 kg**, yielding conditional construction
**144967.1217470858 kg + U + C** and no-retirement construction
**152671.093893035 kg + U + C**. There are 2348 new paid part rows, 1648 named
weld seams and 32 complete bolt stacks. New stock has nominal CG
`(0.0009886574, 0.0, 11.5018437836)` m. The small x offset reflects the consistent
head-side convention; unspecified offcut and allowance disposition remains a
qualification of that nominal CG.

The geometric screen covers 8779408 new/old pairs and 2888406 new/new pairs,
with zero old/old reruns. It records 20055 overlapping enclosure pairs. These
are conservative overlaps, not 20055 proven solid collisions or an assembly
assessment. The result remains **FAIL/UNKNOWN**, with physical float **NOT SHOWN**.

The following kg margins are copied from the saved output and rounded for
display. Every entry still requires one U+C deduction. “No retirement” carries
the predecessor's unqualified retirement stock as well as the whole new bill.

| Altitude / superheat | Mission | Before water | With water | No retirement before water | No retirement with water |
|---|---|---:|---:|---:|---:|
| 0 m / 0 K | M20 | 4591.72 | -70077.75 | -3112.25 | -77781.72 |
| 0 m / 0 K | P100 | -92408.28 | -167077.75 | -100112.25 | -174781.72 |
| 0 m / 10 K | M20 | 11853.83 | -62815.64 | 4149.86 | -70519.62 |
| 0 m / 10 K | P100 | -85146.17 | -159815.64 | -92850.14 | -167519.62 |
| 2500 m / 0 K | M20 | 4650.86 | -70018.61 | -3053.11 | -77722.58 |
| 2500 m / 0 K | P100 | -92349.14 | -167018.61 | -100053.11 | -174722.58 |
| 2500 m / 10 K | M20 | 12369.76 | -62299.71 | 4665.79 | -70003.69 |
| 2500 m / 10 K | P100 | -84630.24 | -159299.71 | -92334.21 | -167003.69 |

## Fixed construction and payment

The module datums are `(2.4,-29)`, `(-2.4,-29)`, `(-2.4,29)` and `(2.4,29)` metres.
Each joins the two saved receiver levels at z=0 and z=23 m. With s=sign(x), the
ladder plane lies 0.900 m outboard. Each ladder has two continuous RHS
200×200×10 mm rails at y offsets ±0.900 m, extending from z=-0.600 to 23.600 m;
three crossbars of the same stock at z=0, 11.500 and 23.000 m; and two RHS
100×100×8 mm diagonals in the frozen alternating pattern. Crossbar and diagonal
body ends meet explicit rail-wall planes. Full selected stock, including
clipped offcuts, stays paid. Its nominal stock CG is reported; actual offcut
placement and transport/erection remain unknown.

Every crossbar/rail and diagonal/rail junction has two full 300×300×12 mm
triangular gusset blanks. All open RHS ends, including the stubs, receive paid
12 mm steel caps. Oblique diagonal caps use their full oblique blank area.
Continuous 10 mm nominal fillets are enumerated separately along member joins,
caps, cage-bar ends, stub plates and gusset edges. The triangular nominal bead
is paid once per named seam. Full-blank intersections are retained, with no
hole, notch, penetration, overlap or offcut credit. Weld strength and access
remain unknown.

Each of the eight split cages retains its original 800 mm receiver box. Two
1000×1000×25 mm steel plates have centres at receiver x±0.4155 m, inner faces
at x±0.403 m and central 600×600 mm openings. The entire square steel blanks
remain charged. The 3 mm polymer face pads have the same opening and an 800 mm
square outer extent; their full blanks remain charged. Four steel bearing bars
close each cage: two 806×25×100 mm and two 806×100×25 mm. Each has a paid
800×100×3 mm inward isolation strip and enumerated end-perimeter welds.
Contact is unilateral, without friction, preload, adhesive or rigid-clamp
capacity credit.

Four M30×1050 mm throughshanks per cage occupy the y/z offsets ±0.450 m.
Every bolt pays its full shank, 46 mm AF ×25 mm head, 46 mm AF ×48 mm nut, two
60 mm OD /32 mm ID ×5 mm washers and two 100×100×12 mm outer backers. Plate
holes are 32 mm. The output records the actual finite axial stack, nominal
engagement and 20 mm runout. Actual threaded length remains unspecified; a
nominal axial surplus does not certify engagement or grip. Every head has a
120 mm diameter ×200 mm socket envelope and a straight 1.200 m removal corridor
from its outer backer, conservatively enclosed at 120 mm diameter. Heads use
the -x side consistently. Old bolts remain paid.

Two RHS100×100×8 mm stubs per fitting sit at y offsets ±0.400 m. Their body
offsets are x=s·0.448 to s·0.780 m relative to the receiver. Each end has a
160×200×20 mm plate at offsets s·0.428 and s·0.800 m, four full 200×150×10 mm
triangular gusset blanks, and separately paid joining seams. These literal
body and plate coordinates leave axial gaps. The output retains the gaps;
nominal weld stock does not prove a complete physical connection. The central
opening likewise does not establish oblique support passage or tool access.

Each module also pays 20 kg temporary handling/access stock and 4 kg
bonding/earthing stock. These are allowances, not evidence of adequate erection
or a substitute for enumerated components. Selected material assumptions are
steel density 7850 kg/m³, E=200 GPa and Poisson ratio 0.30, and polymer density
1200 kg/m³. They are not material certificates. No stress, buckling, fatigue,
old box-wall or connection-capacity PASS is claimed.

## Boundary and inventory discipline

Exactly four states, `(0,0)`, `(0,10)`, `(2500,0)` and `(2500,10)` in metres/K,
and hosts 9, 10, 11, 12, 16, 21, 22 and 23 are retained. All 32 saved route rows
are copied unchanged. Rope tension, sag and guide reactions are not recalculated.

Each of the 16 module/state records contains both complete saved receiver
records, all six retained member records for that pair, every new part's mass,
nominal CG and gravity wrench, and the known and required external six-component
wrenches about the lower receiver. The corrected 24 retained member IDs and
their saved mass/CG appear through all four states. Their detail is not added
again to saved local receiver gravity. Whole-vehicle stock is charged once.

Incoming support, pad and curtain forces and couples remain explicit unknowns.
Saved upper-guide loads belong to the entire rack; they are shown with unknown
allocation, not assigned equally to the two modules or added twice. The sum
of each module's external forces and transported moments must balance its
known gravity. Intervening rack exchanges and the remaining rack boundary must
recover each saved guide wrench once. These identities do not solve compatible
load sharing, torsion, local contact distribution or stiffness. Unlocated old
construction retains an unknown CG, so the enumerated gravity sum is not a
complete vehicle equilibrium solution.

The conditional starting construction is 124724.35352043374 kg + U + C; the
no-retirement column starts at 132428.32566638294 kg + U + C. Both receive the
same entire new bill once. New removed mass and qualified retirement are zero.
The old 7703.972145949183 kg and 2777.8144385218648 kg credits are not subtracted
again. The part-ID reconciliation reports before, retained, removed, new and
after mass. Saved gross displacement, helium/air inventory, 74669.47250300998 kg
fixed water, 17000 kg equipment, 8666.759795158285 kg pressure hardware including
the original 2000 kg once, 5000 kg energy and 3000 kg propulsion are preserved.
Every matching M20/P100 margin before and after fixed water loses the new bill
and remains subject to one further U+C deduction. No gas, bag, payload, pressure,
water or mission relaxation, material-displacement lift or powered lift is used.

## Geometric screen and remaining limits

Only new geometry is screened against saved full bags, the spherical hull,
all saved old objects and the other new objects. Old/old pairs are not rerun.
Straight stock ends, oblique cut faces, triangular/rectangular plate vertices,
explicit openings, finite bolt stacks and reserved access volumes are exported.
Pair screening uses conservative axis-aligned enclosures. The maximum signed
coordinate separation is positive only for separated enclosures; negative
values mean enclosure overlap and are not solid penetration proofs. Per-object
minima, total pair/overlap counts and a bounded first-witness list are retained.
Each unordered new/new pair is visited once globally and updates the minima
and overlap counts of both endpoints. Every object's summary therefore includes
all 2403 other new objects, including earlier indices; its witness is oriented
with that object first. The global counts and the first 2048 witnesses are not
doubled by this per-object accounting.
No blanket mating exclusion hides intersections. Named intended contacts and
their unknowns remain in the interface table. Bag-axis witnesses are labelled
separately; hollow RHS axes and plate openings do not become occupied solids.
For each of the eight oblique diagonal bodies, the bag/hull reporting capsule
uses a radius at least as large as every exported outer vertex's distance to
the finite axis segment. A 1e-12 m outward pad and the next larger floating-point
value cover rounding. Since a capsule is convex, enclosure of all these outer
vertices encloses their convex hull and the represented hollow body within it.
The cut vertices and all constructed geometry stay unchanged; the former
section-only capsule did not enclose the oblique end extensions. The output
records the enclosing radii and vertex distances, separate bag axis and outer
vertex witnesses, and separate hull vertex results. An enclosing overlap is
not an occupied-solid collision proof. Nominal hull or enclosure clearance does
not establish loaded clearance.

All inherited qualifications remain: 15 rope-rating failures, 7 actuator-rating
failures and 22 stroke failures across the 32 saved rows; pressure FAIL;
unresolved bag/crossing/contact geometry, loaded shape and equilibrium;
physical float NOT SHOWN. The predecessor retained-gravity correction has
static acceptance without independent numerical recomputation. The earlier
two mechanics findings remain OPEN and the corresponding withdrawal text is
UNREVIEWED. This construction does not close those matters.

The weakest assumption is that unilateral cage/old-node contact and the
two-level rack path can transfer couples without dominant unsized completion
or unproved stiffness. The sole next **UNISSUED** hypothesis is paid local
box-wall/diaphragm reinforcement at the same eight receiver datums. It is not
implemented or credited here.
