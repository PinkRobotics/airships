# CR III 5056 transfer: sourced limits and the remaining calibration

The isotropic PVC foam model is not transferable as the CR III honeycomb constitutive law. A candidate honeycomb law must retain separate L, W and T directions, irreversible normal crushing and directional shear failure.

For the inherited CR III 5056, 3/8-inch cell, 1.0 pcf product, Hexcel Table II gives the following. Values are QUESTIONABLE for an installed curved hull; “minimum” means the datasheet's minimum average for a product type.

| Quantity | Typical | Minimum average |
|---|---:|---:|
| T compression modulus | 15 ksi | — |
| Stabilized initial compression strength | 60 psi | 35 psi |
| Bare initial compression strength | 55 psi | 25 psi |
| Crush strength | 35 psi | — |
| L–T shear modulus | 15.0 ksi | — |
| W–T shear modulus | 6.8 ksi | — |
| L–T shear strength | 55 psi | 45 psi |
| W–T shear strength | 35 psi | 25 psi |

The source tested 0.625-inch-thick material. The 35 psi crush plateau is distinct from the stabilized 60 psi compression peak. [Hexcel CR III datasheet, Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).

An implementable **candidate form**, not a fully identified product law, is an orthotropic compressible honeycomb model with separate stress/strain curves in each material direction, elastic unloading, and compaction-dependent moduli. This type of directional model is documented by [LS-DYNA's MAT026 interface](https://2023.help.altair.com/2023/hwsolvers/rad/topics/solvers/rad/mat_026_honeycomb_lsdyna_r.htm). For the T direction, the sourced initial elastic slope, peak and crush stress anchor a curve with an initial compression peak, postpeak crushing and eventual densification. The strains and energies needed to join those anchors are not supplied by the datasheet.

For onset screening, use

\[
I=\max\!\left(
\frac{|\tau_{LT}|}{S_{LT}},\
\frac{|\tau_{WT}|}{S_{WT}},\
\frac{\langle-\sigma_{TT}\rangle}{X_{Tc}},\
\frac{\langle\sigma_{TT}\rangle}{X_{Tt}}
\right).
\]

I=1 flags the first source-strength crossing. The orthotropic maximum-stress form is documented in [Ansys ACP's core-failure criterion](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/acp_ug/Core_Failure.html). The T tension strength is unresolved; that term cannot be evaluated from Table II. Separate typical and minimum-average screens must be retained. For an initial supported-core comparison, XTc is the stabilized compression strength, not the crush plateau. Mixed shear/compression interactions remain uncalibrated.

The simplest post-yield directional plastic law caps each stress component at its own current tabulated strength. That is only a **PROJECTION** until full coupon curves are supplied. A plateau does not define shear rupture, unloading, permanent set or fracture energy. Replacing rupture by unlimited plastic shear would overstate surviving load paths.

Before the method can return evidence for the P2 lead's gamma it needs:

1. The benchmark's full foam yield/flow calibration, consistent densification data, steel compression/plasticity curve and indentation-generated stress-free geometry; then agreement with a physical test under the relevant loading.
2. CR III curves for T compression through peak/plateau/densification, both shear directions, unloading and tension; enough combined-load tests to select an interaction law.
3. A finite-strain law that remains admissible over the operating strain range. The prior 0.01 MPa in-plane StVK regularization cannot silently remain the physical material law.
4. The actual thin beryllium sheet's directional compression, yield/fracture and Poisson data, plus core/face bond and debond behavior.
5. A realizable ribbon layout, curved-core manufacturing effects, measured imperfections, joints and seams, and a three-dimensional stability calculation that includes nonaxisymmetric modes.
6. Mesh/step/objectivity checks and a documented gamma denominator. A foam/steel hemisphere's normalized collapse ratio is not the lead's honeycomb/beryllium knockdown.

Until those conditions are met, the inherited CHECK029 strength crossings are warning evidence against the elastic endpoints. They are not repaired by matching one foam-shell pressure numerically.
