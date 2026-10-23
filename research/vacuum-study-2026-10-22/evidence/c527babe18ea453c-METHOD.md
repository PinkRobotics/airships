**Independent method and reproducibility — CHECK MAINLINE-043**

`verify043.py` reads the pinned input copies listed in INPUTS.json; it does not import owner code. `rise_check.py` independently completes the inherited section, mass and ratio conversions. The runtime receipts and executed-source snapshots are under `execution/`. Scientific calculations used the mandatory simjob launcher, one CPU core per job, one numerical-library thread and no GPU. The job timeouts were technical watchdogs, not task budgets. See [EXECUTION.json](8e8ca1231a6c6413-EXECUTION.json) and [CODE.json](22f1cfe16506d7b9-CODE.json).

The final main calculation has 95,634 field comparisons and 481 consistency checks; the rise conversion adds ten and five. Numerical mismatch means outside `rel_tol=2e-8`, `abs_tol=2e-10` for the main scalar fields. The clipped tensile-field quadrature comparisons instead use 2e-6 relative and 2e-12 absolute tolerance. Allocation comparisons use zero relative and 1e-15 absolute tolerance. The rise conversion uses 2e-8 relative and 1e-8 absolute tolerance. The CSV records every main signed difference, including harmless roundoff; exact binary identity is not claimed.

Inputs include 94 pinned order/report/document/data entries and 12 retained primary-source files. Six owner scripts and two unnecessary upstream explanatory scripts are explicitly excluded. The manifest excludes itself and its validation result to avoid recursive hashes. Owner manifests may be read as documents; their executable entries were neither opened nor verified. Primary-source browser readings without retained full text are identified in SOURCE-AUDIT.

**Section and beam recovery**

For an annulus, `A=π(ro²−ri²)` and `I=π(ro⁴−ri⁴)/4`. Stable factored forms avoid subtracting nearly equal powers. Given A and I, `ro²=2I/A+A/(2π)` and `ri²=2I/A−A/(2π)`. Member material volume is `A L`; inner-plus-outer cylindrical area is `2π(ro+ri)L`. End faces are excluded, consistently with the owner's population assumption. The 022d continuum count rounds to 433 only for bookkeeping; 433 edges cannot satisfy the closed triangular sphere relation E=3V−6. The f5 arrays instead contain 750 actual members, 252 nodes and 500 faces.

For the older f4/f6/f2 cases, global translations and rotations are transformed into independent local orthonormal beam frames. Axial compression follows EA/l times the relative local axial displacement. Euler–Bernoulli shear and end moments use the standard 12EI/l³, 6EI/l² and 4EI/l–2EI/l coefficients; torsion uses GJ/l. Circular isotropic sections make the arbitrary transverse basis irrelevant. The resultant end-moment magnitude is converted to outer-fiber bending stress by Mro/I.

Axial and bending contributions are combined on each segment before taking parent-member extrema. The shear estimate is `τ=2|V|/A+|T|ro/(2I)` on that same segment. For minimum longitudinal compression c−b, the positive principal-stress estimate is `τ²/[hypot((c−b)/2,τ)+(c−b)/2]`. This is an ideal beam estimate rather than a resolved three-dimensional joint bound. A separate sensitivity combines independently maximized member shear, torque and least compression; it is more conservative because those extrema need not coincide.

The selected 022d section uses inherited E=410 GPa, ν=.14 and density 3100 kg/m³. With `NE=π²EI/L²`, its axial compression is qN/A and bow moment is `qNe/(1−qN/NE)`, with e=L/1000 unless varied. The additional joint proxy scales the recovered f4 end moment by force and length ratios and assumes aligned bending. It is a transfer hypothesis, not a new equilibrium solution.

For the f5 designs, the frozen 041 subelement N/M arrays and parent-member arc lengths are inputs. At each q, segment compression plus bending is

`qN/A + q(M+NL/1000)ro/[I(1−qNL²/(π²EI))]`.

N and M retain their segment pairing before grouping. Final-section area and inertia are obtained from 041's resized section; the inherited force-invariance convention is explicit. No extra 043 joint proxy is added, since FE moments are already present. All six design/load states and all 4,500 member rows are compared. Inherited joint-mass and screen values are traced to the earlier independent 041 package; this check does not re-solve their optimization.

**Probability, reference size and inverse requirements**

For a specified flaw population, `Hi=ri(σi/s0)^m`, with `ri=Qeff_i/Qref`. Member Pf is `−expm1(−Hi)` and independent series Pf is `−expm1(−ΣHi)`. The common complete-member scale hypothesis sets every ri to one. The 1 cm³ and 100 cm³ hypotheses set ri to actual volume divided by 1e-6 or 1e-4 m³. They are alternate calibrations, not cumulative corrections. No matched compression calibration is established.

For target frame P, the common reference scale is
`s0=[Σ ri σi^m/(−log1p(−P))]^(1/m)`.
To avoid unnecessary large powers, stresses are temporarily normalized by 1 GPa. Substitution into the hazard equation checks each inverse result. Required m at fixed 3.9 GPa is solved by an independently written scalar root equation. The current stresses all lie below that assumed scale, so the relevant hazard is monotone in m.

If a two-parameter Weibull mean μ is assumed, `s0=μ/Γ(1+1/m)`. This derived value does not supersede an independently reported fitted scale. For rectangular bend bars of b=4 mm, h=3 mm, outer span Lo and inner span Li, `Leff=Li+(Lo−Li)/(m+1)`, tensile `Vref=bh Leff/[2(m+1)]` and alternative surface `Sref=(b+h/(m+1))Leff`. SA spans 40/20 mm are assumptions; the RBSC three-point span is 30 mm. Their m-dependent reference sizes differ from gross or geometric dimensions.

The selected member field combines uniform axial compression with sinusoidal bow bending and constant aligned joint bending. Compression moments for integer m=8,10,20 are independently integrated by a finite binomial expansion. Their results agree with axial/radial/angular Gauss quadrature. Tensile integration clips analytically at the zero-stress angle; a 192×16×48 rule is checked against a 384×24×64 rule for the localized 50 mm target-bow case. Surface and volume fits are alternative population assumptions. Hypothetical stressed fractions are not measured contact areas.

An independent equal allocation uses `pi=−expm1(log1p(−P)/n)`; `P/n` is a sufficient union-bound allocation without independence. The latter still needs valid marginal probabilities and a budget for other failure modes. The zero-failure 95% sample count is `ceil(log(.05)/(log1p(−P)/n))`, an illustration of tail-estimation burden rather than a proposed campaign.

**Proof and inherited rise conversions**

For unchanged scalar strength and perfect proof stress sp, immediate conditional failure is zero at s≤sp. At s>sp it is `1−exp(−[(s/s0)^m−(sp/s0)^m])`. Reject fraction is `1−exp(−(sp/s0)^m)`. This construction alone says nothing about damage, environment, altered loading or lifetime. The 1.25 force example is independently re-evaluated through beam-column amplification, rather than treated as a 1.25 stress multiplier.

The rise8 addendum derives area and inertia from radii/wall, tube mass from total arc length and density, charges the 5% joint allowance, 20 g/node, inherited film and systems mass, and converts the attributed moments into bending stresses. Four refinement/baseline ratios are rederived from attributed force summaries. This does not reconstruct rise geometry or verify its equilibrium solution.

**Diagnostic history**

The first main run exposed a missing factor of two in this checker's annulus inversion. The second exposed this checker's use of separately maximized shear/torque rather than the owner's same-segment correlation. Both were corrected; their source snapshots, receipts and diagnostic outputs remain. The conservative alternate extrema calculation is retained as a sensitivity. These were checker defects, not owner mismatches. The final main run passes, and the later rise-label run passes its additional conversions. No refusal or fallback execution occurred.
