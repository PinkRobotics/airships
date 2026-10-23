# MAINLINE-026 independent P3 lattice model

All inputs, computations and outputs are **QUESTIONABLE**. No result certifies a
structure, material, joint or vacuum vessel. Hypothetical rigid joints, stress-free
fabrication and prescribed imperfection patterns are **PROJECTION** assumptions.

## Geometry and material

Project the barycentric subdivision of an icosahedron onto the R = 10 m sphere.
Frequency 6 is nearest the requested mean spacing 2.04 m: 362 original joints,
1,080 great-circle members, 720 triangular film cells, mean arc 2.00134356 m.
Arc lengths are not uniform: 1.62747–2.17054 m. Spherical interpolation produces
each member's internal nodes; straight, initially stress-free beam segments join
them. The member cross-section uses the exact selected 011b result, not the
rounded brief: outer radius 0.12368836237368608 m and wall
0.0008802990936851718 m. E = 410 GPa and density 3,100 kg/m³ are inherited.

The archived current Saint-Gobain data sheet gives a typical Poisson ratio 0.14,
used for G = E/[2(1+nu)], and a typical E of 430 GPa. E is deliberately held at
the dispatched 011b value; the difference remains an NFI. Typical vendor values
are not allowables or evidence for manufacturing these thin curved members.
[Saint-Gobain primary data sheet](https://www.ceramicsrefractories.saint-gobain.com/sites/hps-mac3-cma-pcr/files/assetbank_media/hexoloy-sa-sic-en-1013-tds-215398.pdf).
Circular-section A and I are exact annulus expressions, J = 2I.

Rigid joints share all three translations and three rotations. Ball pins share
translations at original joints but give each incident member independent end
rotations. Internal nodes remain rigid beam connections. Six rigid body motions
are removed by orthogonality constraints, without adding physical support pins.

## Film pressure and tributary share

For an equilateral cell, A = sqrt(3)s²/4. Assign one third of its pressure
resultant to each boundary member. Each member has two adjacent cells:

    width = 2 A / (3s) = s/(2 sqrt(3))
    w = p s/(2 sqrt(3)),    N ≈ w R.

At s = 2.04 m this differs from 011b's member loading w = ps/2 by a factor of
sqrt(3). The continuum global expression is compared as inherited; this
observation concerns its local-member loading checks.

For the unequal geodesic cells, use a conservative polygon-fan construction.
For one outward-oriented cell with boundary coordinates b_i and centroid
c = mean(b_i), its signed volume contribution is

    V_cell = c · sum_i [b_i × b_(i+1)] / 6.

The full closed surface has volume V = sum(V_cell). Applied pressure potential
is +lambda p V, so the inward nodal line-load discretization is -lambda p grad V.
The centroid is a dependent coordinate, not a physical support. For a planar
equilateral triangle, partitioning its centroid fan puts pA/3 on each edge; on
refined edges the centroid's load share is also distributed over the boundary.
Internal edge nodal force scales with segment length, converging to a line load.
The same formula treats the actual curved member boundaries and supplies the
consistent follower-load Hessian +lambda p Hessian(V).

There is no film stretching, wrinkling, contact or prestress stiffness. In
particular, the ball-pin result describes a pressure-loaded frame with this
omission; a taut attached film could restrain its mechanisms. The fan is a load
transfer assumption, not a solved membrane equilibrium. Closed-surface force,
moment, rigid-motion invariance, gradient and Hessian checks are recorded.

## Beam energy, geometric stiffness and eigenvalues

`beam.py` independently assembles the standard 12-DOF Euler–Bernoulli elastic
matrix with axial EA, bending EI in both planes, and torsion GJ. No peer operator
or peer calculation program is imported.

`corot.py` defines an objective finite-rotation, small-local-strain beam energy.
For each segment, L0 and Q0 describe its stress-free chord. Current nodal
orientations are Rodrigues exponentials of the nodal rotation vectors.
The corotated x axis follows the deformed chord; the averaged rotated reference
y director, projected perpendicular to that chord, defines the other axes.
Local rotation vectors a and b are the logarithms of nodal orientations relative
to this corotated frame. The segment energy is

    U = EA/(2L0) (L-L0)²
        + GJ/(2L0) (b_x-a_x)²
        + 2EI/L0 (|a_yz|² + |b_yz|² + a_yz·b_yz).

CPU float64 automatic differentiation supplies the force and Hessian of this
specified energy. This is an independently implemented corotational idealization;
the archived [Vetter et al. paper](https://romanvetter.ethz.ch/publications/papers/2/preprint.pdf)
supplies background on the method, not a claim that this implementation
reproduces that paper's complete element formulation.
The zero-state Hessian agrees with the separately assembled elastic matrix.
The finite-rotation pure-moment check verifies the exact end moments and energy
for total rotations of 0.5 and 1.0 rad, with quadratic tip-position convergence
to a circular cantilever. This verifies the elastic beam equations, not SiC
material behavior at those artificial verification loads.

Solve K0 u1 = -p grad(V0), with rigid-motion constraints. The **primary linear
result** in `classical/` uses the segment compression N from that solution and
the usual initial-stress form

    G(v,w) = integral N (v'² + w'²) dx
    [K0 + lambda (p Hessian(V0) - G)] mode = 0.

Cubic Hermite displacement interpolation integrates this form in both bending
planes. In local [v, theta_z, v_end, theta_z_end] coordinates its matrix is

    N/(30L) * [[36, 3L, -36, 3L],
               [3L, 4L², -3L, -L²],
               [-36, -3L, 36, -3L],
               [3L, -L², -3L, 4L²]].

The other plane has the appropriate rotation signs. Initial-moment geometric
couplings, shear and axial/torsional initial-stress corrections are omitted in
this standard slender-beam linear approximation; full finite-rotation equilibrium
is investigated separately. The compression bilinear form and generalized
buckling equation are independently documented in
[Bleyer's beam buckling example](https://comet-fenics.readthedocs.io/en/latest/demo/beam_buckling/beam_buckling.html).

An earlier **diagnostic, not the primary result**, in `linear/rigid-*` instead
differentiated the entire corotational beam Hessian along the unit-load displacement:

    D = d[H_beam(alpha u1)]/d alpha at alpha=0
    B = -(D + p Hessian(V0))
    K0 v = lambda B v.

Central differences at alpha = ±0.001 and ±0.0005 tested D's step sensitivity.
Despite small residuals, that truncated full-tangent eigenproblem did not
converge with the segment mesh. Exact automatic third derivatives reproduced
the drift, excluding finite-difference cancellation as the explanation.
`geometric-audit/` preserves that finding and the independent initial-stress
comparison. A plausible explanation is that dropping higher-order kinematic
terms from the whole corotational tangent is unsuitable here; this is an
inference, not a proven error analysis. The drifting factors and their
imperfection eigenvectors are not used as the final linear answer.

The generalized symmetric eigensolver operates on the constrained subspace
using sparse factorizations. Reported eigenvector residuals accompany the
results. Symmetry produces degenerate eigenvalues, so the stored Lanczos vectors
are representative modes, not a guaranteed complete census of each multiplicity.

Linear factors concern the perfect elastic model. An independent Euler
pin-pin column check verifies convergence to pi²EI/L², including an independent
Gaussian integration of the Hermite initial-stress form. Member Euler comparisons use each arc length and its mean
compression from the discrete unit-pressure solve; they do not assume identical
spacing or the inherited two-way tributary load.

## Ball-pin mechanisms

Rotate one entire curved member about its endpoint chord. Its endpoints stay
fixed while all its segment frames rotate rigidly. Independent pinned end
orientations permit this motion without elastic strain. There is one such
independent roll coordinate per member, beyond the whole-frame rigid motions.
The recorded checks evaluate Kz, a finite 0.05 rad roll, and first/second
derivatives of pressure volume along the roll. An elastic null mode plus
destabilizing pressure work is a mechanism at zero pressure, not a positive
eigenvalue reserve. No artificial anti-roll restraint is inserted.

## Nonlinear continuation and imperfections

For each rigid-joint case solve grad(U + lambda pV) = 0 using sparse Newton
iterations, six rigid-motion gauges and mean inward original-joint displacement
as the continuation parameter. Lambda is an additional unknown. Residual line
search and adaptive displacement steps handle difficult equilibria. Solver
iteration limits and numerical tolerances are convergence diagnostics, not task
time budgets.

For imperfect cases, once the smallest relative tangent stiffness is below 0.12,
the control changes to a fixed translation coordinate aligned with that soft
mode. This avoids the poor sensitivity of mean sphere contraction to a local
dimple. The control vector and actual mean radial contraction are both retained.
Ordinary smallest-algebraic and shift-invert tangent eigensolvers agree at the
six-segment perfect critical state within 4.6e-13.

The refined runs factor an exactly equivalent mixed system with dependent
virtual face centroids and constraint multipliers. This avoids dense low-rank
couplings among every pair of boundary nodes. Eliminating those extra variables
recovers the original pressure Hessian. Independent matrix reconstruction and
solve checks at six and twelve segments are in `MIXED-CHECKS.json`; the physical
model is unchanged. An initial benchmark exceeded its admitted 3 GiB cap,
released, and was repeated through ordinary simjob admission with 8 GiB.
Mean-only diagnostic runs were explicitly stopped when replaced; their partial
paths are not collapse results. Each stop and resource release is archived.

The three prescribed stress-free imperfections are separate cases, not an
ensemble or a worst-case search:

* Nodes: seeded independent radial offsets, normalized to maximum R/1000 =
  0.010 m; endpoint offsets are linearly carried along each member.
* Members: sinusoidal transverse crookedness, zero at endpoints, nominal
  amplitude 2.04/1000 = 0.00204 m, with seeded independent transverse directions.
* Eigenmode: first standard initial-stress eigenvector's translations on the
  six-segment mesh, scaled to maximum point offset 0.010 m, with its dominant
  radial lobe pointing inward. The same field is interpolated to finer meshes
  to preserve the imperfection pattern. Rotations reset with the altered
  stress-free reference geometry. The initial diagnostic run using the drifting
  tangent's eigenvector is retained separately and is not the primary case.

At each converged equilibrium, compute the smallest constrained Hessian
eigenvalues relative to the reference elastic matrix. Refine a sign-changing
stability bracket to 1 micrometre of mean displacement. A zero tangent
eigenvalue is the first elastic instability on the followed branch; a maximum
pressure is a limit point, while an instability on a rising-pressure branch may
be a bifurcation. Newton failure alone is never a collapse load.

These computations exclude ceramic cracking, tube-wall instability, ovalization,
shear flexibility, manufacturing stress, joint compliance, film stiffness and
post-collapse dynamics. Structural self-weight, temperature fields and pressure
gradients are also outside the uniform-pressure calculation. Their conditional elastic instability loads cannot
override earlier material or local-wall limits.

Raw early nonlinear files used the provisional truncated-tangent factor as their
`k_vs_discrete_perfect_linear` denominator. The final top-level `RESULTS.json`
recomputes all reported knockdowns against the primary standard linear factors.
These raw receipts are retained unchanged for audit.

## Execution and audit

All scientific invocations run through simjob, with CPU quotas and memory
reservations. Numerical libraries are set to one thread before import; GPU
visibility is empty. Each invocation has a unique execution directory containing
source byte/hash pins, exact command, stdout, stderr and paired start/end clocks.
Scratch and plotting caches are in that invocation's own directory. No
scientific scratch is placed in `unpublished-local-ref:f2e62936e29c52c7. No time budget or phase budget is set.
Admissions and release messages are retained; elapsed time is a measurement.
