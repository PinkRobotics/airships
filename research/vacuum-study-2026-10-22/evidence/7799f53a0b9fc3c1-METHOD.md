# Independent CHECK-026b method

All physical values are QUESTIONABLE. Fabrication, rigid/ball joints and film transfer are PROJECTION assumptions. No owner source program or archive was read, imported, extracted or executed. The equations in the pinned METHODS documents are the specification being checked.

The independent topology begins with Cartesian icosahedron vertices, obtains its outward triangular hull, subdivides each face barycentrically, and projects the deduplicated joints onto R=10 m. Edges are independently extracted from triangular connectivity. Joint, member and cell counts are 10f²+2, 30f² and 20f². A circular-arc construction through the endpoints generates the stress-free reference subelements. True circular arc lengths determine tube mass; straight subelement chords determine element stiffness.

Each element has two three-dimensional translations and rotations. Axial and torsional energies use EA/L and GJ/L. Cubic Hermite displacement derivatives are integrated with three-point Gauss quadrature: elastic bending integrates EI times curvature products, and compression stiffness integrates N times slope products. Both bending planes are transformed to global coordinates. This provides the specified Euler–Bernoulli matrix without importing a peer operator or transcribing the owner's matrix implementation. The compressive geometric bilinear form is consistent with the primary [Bleyer beam-buckling example](https://comet-fenics.readthedocs.io/en/latest/demo/beam_buckling/beam_buckling.html); that example uses a Timoshenko discretization, so its code is not the discretization used here.

For a cell boundary b_j, define c=mean(b), S=Σ(b_j×b_(j+1)) and d_j=b_(j+1)−b_(j−1). The signed volume is c·S/6. Its analytic gradient is

`g_j = [S/n + d_j × c]/6`.

For a displacement q, dc=mean(q), dS=Σ(q_j×d_j), and

`(Hq)_j = [dS/n + (q_(j+1)−q_(j−1))×c + d_j×dc]/6`.

Assembly sums shared boundary nodes. The static load is −p grad(V). Hessian products remain matrix-free; no dense face-boundary matrix or owner pressure operator is used.

Six rigid translation/rotation vectors are orthonormalized. Six coordinate eliminations permit sparse factorization of K, but both forces and solutions are projected orthogonally to the rigid space. Thus these eliminations are a computational gauge, not physical support pins. A positive extension on the otherwise null rigid space supplies a generalized eigensolver metric.

The unit-pressure state supplies element compressions. The projected eigenproblem is K v = λ(G_N−pH)v. The largest algebraic eigenvalues of the destabilizing operator relative to the positive elastic metric give the smallest positive λ by reciprocation. Twelve representative modes are retained per run; this is not a complete multiplicity census. Static and eigen residuals are independently computed. Initial-moment coupling and the other physical exclusions of the specified model remain excluded.

The independent checks precede the comparison. A 12-element simply supported Euler beam is within 6.51×10⁻⁶ relative error of π²EI/L². Pressure gradient and Hessian directional errors are below 8×10⁻¹⁰ and 3×10⁻¹⁰; the symmetry error is below 10⁻¹⁷. On the validation mesh, closed-surface resultant force and moment are below 10⁻⁸ in their respective SI units. Endpoint-distance rigidity matrices have full row rank at f2/f4/f6. A rigid finite member roll preserves the geometry, verifying the independent internal mechanism by objectivity. The owner's exact roundoff-level finite-roll energy numbers are not claimed reproduced.

Mass uses rho*A*Σtrue_arc_length, with exact annular A and I. Node mass is 0.02 kg per original joint. Source film, systems, sag and joint rules are carried explicitly. Continuum and half-wave expressions are independently evaluated from the recovered section. Source-row transcription is checked in SOURCE-INPUT-CHECK.json.

The first comparison exposed an endpoint-definition difference. Our original static output averaged the chord-projected forces at both member ends. A separate standard-library postprocessor recovered end forces from the already-completed independent displacement solutions. In global coordinates, with t the element direction, Δu=u_i−u_j and θ=θ_i+θ_j,

`F_i = EA/L (t·Δu)t + 12EI/L³[Δu−(t·Δu)t] + 6EI/L²(θ×t)`.

Owner coordinate/chain data supply only labels for matching endpoints, not displacements or operators. Sampling the first endpoint in the owner's orientation reproduces its entire reported chord-thrust population. The two-end alternative is retained and labeled. This postprocessing launches no FE solve.

All eight simulation jobs used simjob with one core and a 6 GiB cap, with numerical-library threads fixed to one and no GPU. The default host watchdog is a technical resource limit, not a task time budget; it never triggered. A subsequent rise8 request was refused by the memory-pressure gate. No later solver or simulation was launched. The two audit scripts use the standard library to read completed results and perform scalar arithmetic.

The raised-frame forces remain independently unverified. Applying ro*M/I to the owner's moment or multiplying its raised arc length by rho*A checks only those formulas. Nonlinear bracket midpoints likewise do not verify equilibrium or the earliest tangent loss. [SciPy's selection definitions](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html) support keeping the new first-loss fields null.
