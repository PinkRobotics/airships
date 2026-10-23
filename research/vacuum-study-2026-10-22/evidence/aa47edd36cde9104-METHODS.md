# MAINLINE-041: method and limits

All structural results are **QUESTIONABLE / PROJECTION**. They are conditional
calculations for idealized elastic frames, not certified capacities. The work
chooses the brief's **best safety factor at closure mass** option. It does not
claim a minimum-mass design attaining 022d's safety factor.

## Inputs and geometry

`INPUTS.json` pins the dispatch, brief, inherited results, own preceding methods,
and material sources. The selected 022d point is taken from its unrounded JSON:
R = 10 m, p = 95,460.8379139 Pa, SiC E = 410 GPa, density 3,100 kg/m³;
outer radius 0.13754142819010323 m, wall 0.0011373648451580738 m.
Poisson ratio 0.14 is carried from the primary Hexoloy sheet for torsion.
The vendor sheet's E = 430 GPa is a documented difference; 410 GPa is retained
to make the requested comparison.

Class-I icosahedral subdivision at integer frequency f gives 10f²+2 joints,
30f² members and 20f² cells. Projected subdivision vertices lie on the sphere;
each member follows its endpoint great-circle arc. Frequency 4 is the
realization nearest the selected spacing. It has 162 joints, 480 members and
320 cells, rather than the noninteger counts in the continuum sizing.
Unequal actual member lengths and actual total arc length enter the calculations.

Each arc is represented by m initially stress-free, straight Euler–Bernoulli
segments. Mesh studies use m = 6, 12, 24 at the selected point; the frequency
search begins at m = 3. Exact annular A, I and J=2I are used. Rigid joints share
translations and rotations. Ideal ball pins share translations and release
each member's endpoint rotations. Intermediate nodes retain beam continuity.
Six whole-frame rigid motions are removed by a gauge, not by clamping a cell.

The source-based section formulation and distinction between axial, torsional
and bending resultants are described in
[Bleyer's 3D beam notes](https://bleyerj.github.io/comet-fenicsx/tours/beams/beams_3D/beams_3D.html).
The implementation is this seat's frozen 026/026b method, adapted to the new
section and mass model; no peer numerical program is executed.

## Pressure and linear eigenproblem

Each cell boundary includes its intermediate arc nodes. A virtual centroid is
the arithmetic mean of those boundary nodes. Oriented boundary-centroid
triangles form a closed surface. Pressure potential is λpV with derivatives
computed consistently from its volume. The virtual centroid follows its
boundary, so its forces and tangent are condensed onto the structural nodes.
This conservative pressure model differs from independent radial node loads.

First solve K u = −p grad(V). Recover local beam end forces, compression N,
bending magnitude sqrt(My²+Mz²), and torsion. The classical eigenproblem is

    K v = λ [G_N − p Hessian(V)] v.

G_N is the standard cubic-Hermite initial-compression matrix, assembled for
each segment's computed N. The linear eigenproblem does **not** include initial
bending-moment coupling; the geometrically nonlinear calculation supplies a
separate comparison. Linear buckling and its geometric-stiffness construction
follow the standard principle illustrated in
[Bleyer's buckling example](https://comet-fenics.readthedocs.io/en/latest/demo/beam_buckling/beam_buckling.html).

The primary screening convention retains 022d's **0.2 times the perfect linear
multiplier**. This is an inherited assumption, not a knockdown calibrated for
the actual frame, its joints or its imperfections. Raw perfect multipliers are
also reported. No 026b ratio is transferred to this geometry.

## Nonlinear first-loss check

The existing corotational beam energy, gradient and Hessian are combined with
the same pressure potential. The co-rotational formulation is documented by
the archived [Vetter et al. paper](https://romanvetter.ethz.ch/publications/papers/2/preprint.pdf)
and by the prior own verification package. The reference is a perfect,
stress-free frame, with elastic material and rigid joints.

Mean inward joint displacement controls equilibrium. Newton correction uses
an exact sparse mixed representation of the centroid-pressure Hessian; the
virtual variables change factorization cost, not the physical equations.
The solver checks the **six smallest algebraic generalized tangent
eigenvalues at every recorded equilibrium**, with the positive undeformed
stiffness as metric. It does not select the eigenvalues nearest zero during
continuation. A positive/negative sign bracket is refined to a control-width
below 1 micrometre. The six whole-frame motions remain gauged.

`audit_nonlinear.py` independently solves the final snapshot by shift-invert,
using a different random seed. It compares all six values with the preceding
smallest-algebraic solve, checks equilibrium residual, checks the full
beam-plus-pressure tangent by central finite differences, and confirms every
recorded state preceding the first negative value was positive. These tests
address the unverified eigenvalue-family issue carried by the earlier 026b
nonlinear results. They do not retrospectively validate those older results.
`audit_random_sa.py` additionally starts an unshifted eight-eigenvalue
smallest-algebraic solve from a fresh random vector at the final m=24 positive
snapshot. It verifies that no lower negative family was hidden by the path's
warm-start vector or the independent near-zero audit.
Solver-selection meanings follow
[SciPy's eigsh documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html).

The result is a **numerically verified first sampled loss of positive elastic
tangent stiffness on the perfect equilibrium branch**, with the displayed
mesh convergence and residuals. It is not proof of positivity at every real
point between recorded equilibria, imperfection tolerance, material collapse,
contact failure or certified pressure capacity. Material and joint limits can
occur well before the raw elastic instability. A second 0.2 factor is not
silently substituted into the resized ranking.

## Ball pins and film tangent

One initially curved, circular-section member can rotate rigidly about its
fixed endpoint chord. With independent end rotations this is a zero-strain
internal motion: one per arc, in addition to the six whole-frame motions.
Finite rotations of three representative members verify strain energies near
roundoff. Pressure volume decreases along at least one direction; symmetric
members have negative second variation, while an irregular cell can also
produce a first-order pressure torque. The as-prescribed bare pinned frame
therefore has no positive stable pressure margin. This is not a statement
about every possible rearranged geometry.

Toyobo's Zylon HM filament modulus is 270 GPa. A conditional 0/90 material
tangent puts E t_total/2 into each axial direction of each surface triangle.
The first axis follows the projected original cell edge; the second is
orthogonal in the triangle. Virtual centroid displacements are condensed as
above. Shear stiffness, Poisson coupling and membrane prestress are zero,
because they are not established by the selected fiber datum. A rigid-motion
annihilation test checks the assembled tangent.

This is a **taut, perfectly attached axial-material-tangent sensitivity**.
It is not a pressure-equilibrated, tension-only, wrinkling-aware skin model.
The chosen kinematics constrain the interior skin to follow the frame and can
overstate restraint. A filament modulus does not specify a complete laminate:
[Oasys's fabric material documentation](https://docs.oasys-software.com/structural/gsa/references/hidr-data-mat-anal/)
also distinguishes directional moduli, shear and coupling.
Neither stiffness nor weight credit from an unqualified skin is used in the
primary resize. The film's prescribed mass and strength screen are retained.

## Member and joint failure screens

All segment forces are evaluated at operating pressure and scale with λ in
the declared linear-demand screens. Actual parent arc length enters Euler
π²EI/L² and the inherited L/1000 crookedness. Retained material scalars are
3.9 GPa compression and the fixed 15.586 MPa projected tensile screen.

The local-wall convention is 022d's axial-compression screen:

    sigma_local = gamma * 0.6 E t / r_outer
    gamma = 0.099 + 0.901 exp(−sqrt(r_outer/t)/16).

The shell convention and its applicability remain questionable. For Perry
compression, tensile demand and required compression strength, the applied
bending includes computed FE bending plus N L/1000, amplified by
1/(1−λ/λ_Euler). Adding the crookedness moment is a declared conservative
projection, not a measured imperfection or a solved imperfect equilibrium.

An additional sensitivity substitutes peak amplified compression into the
uniform-axial local-wall limit. It is not a validated local bending interaction
law and is not optimized in the matching-022d search. Its lower SF is displayed
beside the main results; it must not be hidden by the favorable axial-only
local convention.

Each member end is scored with its actual axial force N, bending moment M and
torsion T. For an external annular sleeve of area Aj:

    rj = sqrt(ro² + Aj/pi)
    Ij = Aj (rj²+ro²)/4
    sleeve stress = N/Aj + M rj/Ij
    bond equivalent force = sqrt[(N + 2M/ro)² + (T/ro)²]
    bond shear = equivalent force / (2 pi ro overlap).

The as-built result holds 022d's sleeve area and overlap unchanged and charges
the actual 960 ends. Resizing solves each end's sleeve area and overlap for
the candidate target, using 1,470 MPa CFRP compression, 28.9 MPa adhesive shear
and 1,550 kg/m³ joint density. The resulting joint capacities equal the target
by construction; there is no surplus joint reserve. These equations resolve
axial/bending/torsional scalar demands, not adhesive peel, transverse shear,
SiC contact, laminate failure or rotational stiffness.

## Mass closure and resize

Tube mass is density times exact A times the sum of great-circle member
lengths. Both Zylon directions together occupy the quoted total gauge and are
charged over 4 pi R². Film strength uses the largest cell edge chord as its
curvature radius; the uniform gauge must satisfy the worst cell. Node mass is
20 g per actual node; systems mass is 100 kg.

The selected circular-cap sag surrogate is extended to unequal cells by their
actual planar inradius, each cell's largest chord as curvature radius, and
spherical-cell-area weighting. Lift debit is 3 LIFT mean_sag/R. This preserves
the selected cap concept; it does not solve an actual membrane shape or
incorporate seam/gas-barrier/attachment mass. Surface approximation differences
between pressure fans and the cap volume are an explicit NFI.

Closure mass is LIFT = 4,889.44215019 kg. Reserve is either 5% of that quantity
(244.4721075095 kg) or the inherited 019 reserve (411.2989440716474 kg).
Tube, film, individually sized joint ends, nodes, systems, reserve and sag
lift debit must sum to that quantity.

At fixed gyration radius g=sqrt(I/A), scaling A and I together scales the
perfect linear eigenvalues by the same factor and leaves pressure-induced
forces and moments invariant. A fresh-frame scaling test verifies both
identities. This reduces the FE table to one section variable g.

For integer frequencies 1–10, sample g from 0.03 to 0.176 m, interpolate
eigenvalue and full force/moment arrays with shape-preserving cubic splines,
and use multiple local constrained starts to maximize target SF. Bounds are
A in [2e−5,0.006] m², outer radius ≤min(0.25 m, minimum chord/3), a hollow
section, and target in [0.01,3]. The film and every joint end are sized at
each target. New exact FE samples at each proposed optimum drive adaptive
interpolation refinement until its SF error is below 2e−5 and its mass error
below 0.02 kg.

Frequencies 4, 5, 6 are reoptimized at m=6 and m=12. Frequencies 4 and 5 receive
exact m=24 responses at the refined optimum gyrations. Each reported witness
then solves a scalar area root against its **exact** FE response to enforce
closure, resizing film and joints consistently. The 24-element checks are
best-found witnesses, not a proof that their inherited gyration is the exact
24-element optimum. Frequency ranking is limited to the stated uniform-section
geodesic family, not arbitrary topology, nonuniform sections or all integers.
No continuum half-wave homogenization screen is used to override actual
discrete eigenvalues.

## Reproducibility and execution

Every numerical calculation and scientific verification is admitted through
simjob with one CPU core and one thread in each numerical library, CPU-only.
Each invocation archives exact command, source hashes, start/end clocks,
return code, stdout and stderr. The technical watchdog is not a work budget.
An initial invalid 10,800-second watchdog request was rejected as usage
(code 64, never admitted), corrected to the supported 7,200 seconds, and
retained in the execution ledger. It was not a capacity-admission refusal.

The initial pin test incorrectly expected volume to decrease for both roll
signs, overlooking first-order pressure torque in unequal cells. Its failed
receipt and original source remain. The corrected test records signed volume
derivatives and requires a descending isometry, alongside independently
unchanged strain energy; it also reports negative symmetric curvature.
No failed computation is presented as a passing test.

`CODE.tar.gz`, the per-run source pins and `MANIFEST.json` make the work
reviewable. Former 026, 026b and CHECK-022d packages remain frozen. Qualified
structural SF, qualified compression allowable and failure probability remain
null.
