**Independent method and scope.** The owner code, including predecessor code, was neither opened nor executed. `UNREAD-CODE.json` records the exclusions. The check uses the pinned reports, equations, input JSON and primary-source documents. `independent_check.py` is newly written checker code. The model validation concerns the filed scalar model, not its physical qualification.

**Force and mass reconstruction.** For a sphere of area A=4πR², balancing a hemispherical pressure resultant against both identical skins gives pπR²=(2πR)(2tf)d and therefore d=pR/(4tf). For structural mass S and core mass fraction f, tf=(1−f)S/(2Aρf), tc=fS/(Aρc), with ρf=1850 kg/m³. The complete closure is

    lift = S + max(0.05 S, physical joining) + fixed reserve + 100 + payload.

The R10 environment is independently rebuilt from the inherited climatic scenario and equals 411.298944071647 kg. At R20 the corresponding environmental reserve is 2767.736727998812 kg. Dry lift uses (1−Δp)T0/(T0+ΔT); humidity loss uses 0.378 e/p0 times the same temperature ratio. Retained water scales with area and internal gas with volume. R20 demand uses 1.01 p0; the held R10 demand uses p0. No radius-only equivalence between their joining models is inferred.

For R10 scarf seams, overlap=30tf and coincident seam length is A[1/(a−30tf)+1/(b−30tf)], with a=.6096 m, b=1.8288 m. Joint mass is the two face/core films and any primer, plus seam length times [.25tc+.002+2tf√901(.070)]. The last term is omitted for welds and their seam length omits overlap. The check solves the mass closure using a differentiable joint-mass expression and Newton updates capped by the 5% allowance solution. Maximum final mass residuals are checked directly.

For R20, joining mass is Aλ[2ρf tf w+2μw+1100 g tc+1100 Ab]+2Aμ, using λ=1/a+1/b, w=.06 m, μ=.1464728290914915 kg/m² per interface, g=.001 m and Ab=1e−5 m². This becomes u(f)S+v. The smaller of the allowance-limited mass H/1.05 and the physical-joining solution (H−v)/(1+u) satisfies the budget.

**Seven-mode reconstruction.** Let h=tf+tc, σ0=Eh/[R√(1−ν²)], σcr=h²Gc/(2tf tc), Vc=σ0/σcr and Kc=1−Vc/4 for Vc≤2, otherwise 1/Vc. Safety factors are:

- Global: γKcσ0/d.
- Face: Fcy/d.
- Core shear crimping: σcr/d.
- Core crush: crush/(p/2).
- Wrinkling: b kw√(E Ec tf/tc)/d, where the positive root of b³+b=1 is solved independently.
- Dimpling: E(tf/cell)²/[(1−ν²)d].
- Joint: 10 MPa ×901/30 divided by d for R10 scarf seams; ηFcy/d for welds and R20, with η=1 and .9 respectively.

The held R10 coefficients are the predecessor's declared constants. Full cases use γ=.2+.4 min(Vc,2), kw=.82, with the stated elastic-property variants. Today's convention uses γ=.2 below Vc=2 and γ=1 above, kw=.33. This discontinuous inherited convention is explicitly searched on both sides of Vc=2; it is not a new physical validation.

**Independent optimization.** Core fractions span 10⁻⁷ to 1−10⁻⁷, with 2,049 linear interior samples and logarithmic end sampling. Every listed core is searched. Local maxima of the seven-mode minimum are refined using bounded scalar optimization; competing active-mode intersections are then solved with Brent roots. Today's branch switches receive explicit one-sided evaluations. Strength thresholds are found differently: solve every strength-independent mode's SF=1 boundary, retain feasible boundaries, and choose the smallest required Fcy among them. This captures isolated feasible held points without mistaking a finite grid miss for infeasibility.

All 15 reported model families and nine strengths per family are independently optimized. Their 15 thresholds and 135 sensitivity points are also re-evaluated at the filed geometry to separate arithmetic from optimization. Five held geometries, 15 thickness deductions, two unlimited-strength cases, environmental accounting and the zero-core bound are checked separately.

The R20 payload endpoint receives a second certificate: impose tf=pR/(4×.9Fcy), solve the global SF=1 condition for tc, then subtract the resulting structural and joining masses from available lift. This gives 209.838651699805 kg and explains the 20.898 mg difference from the filed optimizer endpoint.

**Source arithmetic.** Unit conversions use exact 0.45359237 kg/lb, 9.80665 m/s² and .0254 m/in. For equal in-plane compression, a pressure-insensitive isotropic von Mises model gives sqrt[((−s+s)²+(−s−0)²+(0+s)²)/2]=s; that identity does not validate its use for textured beryllium. NASA-TM-4397 Table 8 uses the cross-term convention as printed in its equations, so no additional factor two is inserted. The compression extrapolation solves

    (3.521 + 2.889 − 2.726) ×10⁻⁴ s²
      + (2.394 + 0.780) ×10⁻³ s − 1 = 0,  s in ksi.

The positive root is 47.970266896899 ksi. It is a fit extrapolation, not an allowable.

**Tolerances and records.** Fixed-point arithmetic comparisons use relative tolerance 10⁻⁸ plus 10⁻⁹ absolute, with 10⁻⁵ kg absolute for mass residuals. Reoptimized thresholds and safety factors use 2×10⁻⁷ relative tolerance. Payload has an additional 10⁻⁵ kg absolute tolerance. Every expected value, independent value, difference and tolerance is written to JSON and CSV; none is suppressed because it passes. Threshold differences are below 0.000072 Pa; the largest optimized-SF difference is below 4.7×10⁻⁹.

`NUMERICAL-RUN.log`, `RECOMPUTED.json`, `NUMERICAL-CHECKS.json`, `PAYLOAD-CERTIFICATE.json` and `UNIT-CONVERSIONS.json` are calculation evidence. The source evidence ledger distinguishes directly checked tables, newly found context, failed retrievals and unqualified transfers. Hash manifests identify the data and primary sources; none substitutes for a controlled current material specification.
