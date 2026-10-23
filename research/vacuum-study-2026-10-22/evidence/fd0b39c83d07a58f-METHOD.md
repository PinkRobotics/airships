# Independent calculation method

QUESTIONABLE throughout; no certification. The owner's `analyze035.py` was copied and hash-checked as an input artifact, but its contents were not read, imported, or executed.

Run `python3 rederive.py` in this directory. It requires Python and NumPy, uses no network, and opens owner result JSON only after calculating the comparable values. `NUMERIC-COMPARISON.json` exposes every one of the 112 derived-field comparisons, including values and signed differences. Source-input verification, graph readings and interpretation corrections are recorded separately.

The face calculation starts with orthotropic plane-stress stiffness. For each ply, three unit engineering strains are rotated as tensors into the material frame, multiplied by material stiffness, then the stresses are rotated back. Through-thickness integration gives A, B and D. Inverting A gives Ex, Ey, nu_xy, nu_yx and Gxy. Checks enforce positive stiffness, reciprocity, vanishing B for the symmetric layups, and the quasi-isotropic identity G=E/[2(1+nu)] for the six-ply faces. This independently reproduces the card's lamination results.

For equal face thickness tf and core thickness tc, h=tc+tf is the face-centroid separation. The card's thin-face approximations are rho=h/2 and t_eq=sqrt(12)*rho=sqrt(3)*h. They are geometrical approximations, not laminate principal radii derived from full A/D matrices. Finite homogeneous face thickness would give rho²=h²/4+tf²/12. Directional CLT corrections use rho_x²=h²/4+Dface_11/Aface_11, with the analogous y expression. Their small size does not repair the larger constitutive transfer problem.

The nominated scalar map uses Ef=sqrt(Ex*Ey), nu=sqrt(nu_xy*nu_yx), and Gc=sqrt(G13*G23), followed by:

`Vc = 2 Ef tf tc / [R sqrt(1-nu²) (tc+tf) Gc]`.

Its “axial” endpoint instead substitutes Ex, nu_xy and G13; its “soft” endpoint uses the scalar face with G23. These are three conventions, not statistical confidence bounds. For orthotropic CTA8.1, replacing nu_xy with the reciprocal denominator sqrt(1-nu_xy*nu_yx) changes the axial proxy from 0.412724 to 0.400216. The card's specified scalar convention is reproduced, not promoted to an exact anisotropic buckling parameter.

CTA8.1 uses the paper's initially assumed generic lamina and nominal ply thickness. Replacing only ply thickness by the measured 0.005679 in changes Vc_iso from 0.531659 to 0.573914 and R/rho from 335.196 to 331.317. A zero-strain posttest-modulus calculation gives Vc_iso=0.590001 and a soft-direction proxy of 0.925067. This is a sensitivity calculation: strain-dependent properties cannot be collapsed to a unique measured Vc by selecting one modulus.

The handbook calculations are:

- SP-8007, 1968: `gamma_c = 1 - 0.901[1-exp(-sqrt(R/t_eq)/16)]`.
- CR-1457 cylinder recommendation: `gamma_CR = 0.75 gamma_c`, in the relevant stiff/moderate branch.
- SP-8032: `lambda² = sqrt[12(1-nu²)] (R/t_eq) [2 sin(phi/2)]²`; `gamma_cap=0.14+3.2/lambda²`, lambda>2. The card's numbers imply nu=0.3 and phi=90 degrees. Nu=0.33 changes them by under 0.00003. Substituting phi=180 degrees is recorded only as a formula extrapolation, not a validated closed-sphere boundary condition.

The card's cylinder fit is separately reproduced using straight segments in log10(R/rho) through (10,0.68), (100,0.55), (1000,0.31). The primary source provides an analytic relationship, so corrected handbook values use that relationship. Interpolating observed Baker/FPL points in log(R/rho) is also reproduced, but it has no population-level significance or established uncertainty beyond the underlying graph reads.

For the sphere projection, divide each of the three accepted SBKF ratios by its SP-8007 value, retain the minimum and maximum factors, and multiply them by the lead's SP-8032 value. All of those operations reproduce. The operation is an invented extrapolation across geometry, loading, material anisotropy and Vc. A common isotropic ideal-shell membrane resultant does not prove equality of the actual FE denominators, imperfection sensitivities or shear corrections.

Source lead points are independently recalculated from the pinned 021/021b geometry, E=290 GPa, nu=0.33, Gc=46.8843496 MPa and p=95.4608379 kPa. With Kc=1−Vc/4, the perfect pressure is `4 Ef tf h/[R² sqrt(1-nu²)]` and required gamma is p/(Kc*perfect_pressure). Both source Vc and required gamma reproduce. Rounding in 035's copied inputs accounts for its very small differences in derived slenderness.

Graph readings use the retained 1849×2400 pixel renders. A projective transform maps four plot corners to the axis coordinates, correcting the skew of the S-II scan. Three unused interior grid crossings validate the transformation. Marker centers are independently selected from the image. Report gamma to about 0.01 and R/rho to about 5; stored extra digits support audit of the transformation only. The cylinder figure uses the same approach with a logarithmic horizontal coordinate, conservatively allowing 5% in R/rho. Scanner/marker uncertainty is not specimen-to-specimen variability.

The source CTA8.3 inconsistency is retained explicitly: its printed ratio is 0.864, while its stated loads give 0.86530488. The principal reproduction uses the printed ratio because that is what the card cited. The alternative raises its SP-8007 multiplier from 1.558660 to approximately 1.561014; it does not change the qualitative conclusion.

No source scripts or downloaded executables were run. No repository source was changed. Failed PDF/archive requests are distinguished from successful primary HTML inspection; `sources/muc2018.html` is an archived challenge response, not the article.
