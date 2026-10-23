# MAINLINE-056 method and predeclared assumptions

Everything is QUESTIONABLE or PROJECTION. No material property, numerical agreement, or capacity here is certified.

The task is a constitutive extension of the MAINLINE-029 benchmark. The implementation reuses CHECK029's Q8 mesh, geometric kinematics, pressure force and load stiffness, boundary conditions, and linear eigenproblem. The new material routine and committed-state nonlinear continuation are owned MAINLINE056 code. The reused file is copied to reuse/axi029.py; original MAINLINE029 code and selected standalone decks are pinned under inputs/owner029. The original packages remain unchanged.

## What is being compared

The 6.03 MPa flat-shell target is a **numerical result**, not a measured pressure-collapse test. EUCASS2023-367 validates its formulation against axial-compression experiments, then predicts pressure buckling. It specifies steel and PVC80 elastic properties, pressure results, and plotted constitutive curves, but does not give a full foam calibration or the indentation-generated mesh. The figure labels and the paper's radius prose are not wholly consistent. [EUCASS2023-367](https://www.eucass.eu/doi/EUCASS2023-367.pdf).

All runs are axisymmetric clamped hemispheres, with a uniform inward follower pressure on the outer boundary and shared interface nodes. Units are mm, N and MPa. Faces are 0.42 mm each; foam is 3.1 mm. The base radius is 42.8 mm at the outer face, preserving MAINLINE029. A separate scenario reads 42.8 mm as the total-thickness midsurface radius, making the outer radius 44.77 mm.

The base initial shape is MAINLINE029's stress-free Gaussian radial offset applied to every layer: depth 0.75 times total thickness, width 0.1 times outer radius. This is a declared approximation to the paper's indenter-generated shape, not that recovered shape. Face/core thickness is preserved in the radial mesh.

Separate reconstructed-contact cases follow the paper's stated two-stage procedure: indent a perfect shell with a frictionless rigid sphere of radius 4.28 mm by 2.955 mm, import the deformed geometry, reset stresses and plastic state, then apply pressure. The contact traction is integrated over the current outer surface; its nodal tangent includes changing normals and area and is independently finite-difference checked. Penetration, reaction force and mesh validity are retained. The coarse 3000 MPa/mm penalty is refined to 30000 MPa/mm and checked further where reported.

Geometry-only import explicitly resets both plastic strain and hardening. The paper does not provide a reproducible import deck establishing that convention; retained hardening would be another constitutive history. These are reconstructed conditional shapes, not the original author's mesh. Unlike the Gaussian offset, indentation compresses the core and moves the inner and outer faces by different amounts.

## Constitutive assumptions

The chosen foam form is the isotropically hardening Deshpande–Fleck ellipse. Let q be von Mises stress and p=−tr(σ)/3. The normalized yield function is

\[
f=\sqrt{\frac{q^2+\alpha^2p^2}{1+\alpha^2/9}}-Y(\kappa).
\]

The base uses associated flow, α=3/√2, hence zero plastic Poisson ratio and uniaxial/hydrostatic strength ratio √3. That ratio is an **assumption**; the paper gives no hydrostatic test. α=1.5 and 3 are separate sensitivities. The published model form, true-stress/logarithmic-strain inputs and calibration requirements are documented in the [Abaqus material manual](https://abaqus.uclouvain.be/English/SIMACAEMATRefMap/simamat-c-crushfoam.htm). A uniaxial curve alone does not identify the yield ellipse.

The steel uses J2 isotropic hardening (the α=0 specialization). Elastic constants are 210000 MPa, ν=0.33 for steel and 40 MPa, ν=0 for foam. The base steel curve reads the plotted stress axis divided by ten: initial yield 750 MPa, rising to about 1018 MPa. **That factor-of-ten reading is PROJECTION, not an established erratum.** A literal-axis scenario uses stresses ten times higher.

The plotted steel curve is from a tensile test. Applying its strength symmetrically in compression is part of the J2 model assumption; a separate compressive curve was not recovered.

The foam curve is a rounded visual digitization, fixed before the first shell run:

| Total compressive logarithmic strain | Cauchy compressive stress, MPa |
|---|---|
| 0.035 | 1.40 |
| 0.10 | 1.40 |
| 0.20 | 1.42 |
| 0.30 | 1.44 |
| 0.40 | 1.46 |
| 0.45 | 1.60 |
| 0.50 | 1.90 |
| 0.55 | 2.40 |
| 0.58 | 2.96 |
| 0.60 | 3.50 |

The initial point uses σ/E=0.035. Plastic strain knots are εtotal−σ/E; the first is zero. ±10% foam-strength scenarios expose digitization/strength sensitivity. They scale hardening stress at the same plastic-strain knots.

**Densification limitation.** The later plotted slope exceeds the declared E=40 MPa. With fixed positive elastic stiffness, an additive elastic-plastic fit would require decreasing plastic strain there: dεp/dε=1−(dσ/dε)/E<0. Thus the full printed curve cannot be represented by this constant-E, monotone-hardening model. The table stops at the last retained monotone segment; later plastic strains use its last slope, explicitly labeled extrapolation. Every step records the number of points beyond the last knot. No extrapolated values are called measured properties.

The steel's plotted total-strain abscissa is converted to plastic strain by subtracting σ/E, with its first flow point at zero plastic strain. The literal-axis sensitivity retains only increasing plastic-strain knots. No curve or scalar was adjusted to produce 6.03 MPa.

## Finite strain and return mapping

Use the material-corotational logarithmic strain H=log U, where F=RU. The old committed plastic strain tensor is held fixed throughout each global Newton solve. The trial corotational Cauchy stress is the isotropic elastic tensor applied to H−Hp,old. Returned Cauchy stress is transformed to PK2:

\[
S=J\,U^{-1}\widehat{\sigma}\,U^{-1},\qquad
\sigma=R\widehat{\sigma}R^\mathsf T.
\]

This follows the documented strain/stress interface convention of [CalculiX's nonlinear Abaqus-style user materials, §6.8.18](https://www.dhondt.de/ccx_2.21.pdf). The extension is its own implementation, not an Abaqus executable or an assertion of exact Abaqus constitutive equivalence.

For associated flow let D=1+α²/9 and dλ=dκ. If the updated strength is Y=Y(κold+dλ), the trial deviator and mean stresses return as

\[
s=s_{\rm tr}/[1+3Gd\lambda/(DY)],\qquad
m=m_{\rm tr}/[1+K\alpha^2d\lambda/(DY)].
\]

The scalar consistency equation enforces f=0. For J2 the scalar reduction is qtr−3Gdλ=Y. For the base foam, ν=0 and α²=4.5, it is σeq,tr−E dλ=Y. Piecewise linear hardening gives an exact segment solution in these two cases. Other α values use a bracketed scalar solve. Plastic state updates only after global equilibrium converges; rejected increments and line searches do not accumulate plastic strain.

The tangent is a centered numerical derivative dS/dEgreen at each integration point, at fixed committed state. It includes the stress transformation. The assembled force derivative is separately checked against nodal finite differences with a different step size. The global matrix is allowed to be unsymmetric.

## Continuation and evidence

A bordered Newton system solves displacement and pressure simultaneously while prescribing monotonically inward outer-pole motion. Three-point Gaussian quadrature is used in each Q8 coordinate. Pressure includes its follower-load stiffness. Line search and increment cutbacks enforce convergence.

Guarded runs additionally bound the maximum accepted local equivalent foam plastic increment (.02, with .01 in the tighter run). An initial .0005 mm cap before first foam yield narrows its load bracket. These are numerical increment controls; no clock or task-phase cap is imposed. Earlier unrestricted runs remain in the evidence rather than being silently replaced.

The run records every accepted step: pressure, both pole displacements, equilibrium residual, plastic strains, material stresses, volume Jacobians, first-threshold brackets and source-extrapolation use. The pressure peak is followed onto the descending branch. A Newton failure is recorded separately and is never renamed a limit point. A resolved axisymmetric equilibrium peak does not establish nonaxisymmetric stability or experimental capacity.

The raw run's `peak` is the largest pressure on the traced path. The collection also reports every sampled local maximum followed by three lower pressure samples, retaining its two adjacent samples. Gaussian-imperfection paths have an earlier maximum and descending branch before their largest pressure; the latter must not be called their first instability. The reconstructed-indentation cases are assessed separately. Load control cannot simply traverse a negative-slope branch; neither pressure-control dynamics nor a full stability eigenanalysis is simulated here.

Admissibility outputs distinguish:

- First foam yield under the full pressure-dependent criterion.
- First resolved transverse shear at the **implied initial pure-shear strength** Y0√(D/3). This is a model screen; no measured PVC80 shear-fracture strength was recovered. Subsequent hardening can raise the current surface.
- First steel yield and its later hardening response.
- The pressure peak, plus any earlier extrapolation.

Material checks cover uniaxial, hydrostatic and pure-shear yield, permanent strain and unloading, J2 plastic incompressibility, all retained uniaxial compression knots, general-α hydrostatic limits, finite-strain stress conversion and rotation objectivity. The small-strain linear anchor uses the exact matched MAINLINE029 mesh. These checks establish internal numerical behavior, not independent material validation.

All simulation and verification runs use simjob with one core and a 4 GiB cap. Each admitted job has a 7200-second host resource limit; this is not a work deadline. Run receipts include admission/release, exit status, measured wall time and peak RSS. Every pressure/indentation job and the final successful verification have full source snapshots and hashes. The first failed verification preceded the snapshot feature; its failed test script, traceback and resource receipt are retained separately. No code or material package is shared into another seat.
