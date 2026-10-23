# MAINLINE-022d — corrected P3 scan

**QUESTIONABLE throughout.** Completed all 32 branch/grid/reserve/family combinations, with 64 primary numerical
witnesses. Both Zylon plies, each sleeve/wrap's own load multiplier and joint mass, projected tensile bending,
continuous film gauge and the requested half-wave screen are included. These are conditional calculations;
qualified full-structure SF, compression allowable and assembly failure probability remain unknown.

The **best equilateral overall** witness is Zylon 0/90/CFRP, cap, 5% reserve:
SF **1.397732582**, s=6.085747 m, half-wave/member=0.569022.
It fails the half-wave screen. The **best equilateral screened** witness is the same family at
SF **1.258252477**, s=3.170759 m and arc length=3.184194 m;
half-wave equals one member at numerical precision. Local shell, smeared global and film capacities bind;
the assumed sleeve/wrap axial and bond capacities equal the target by sizing. The tensile demand is zero.
This single-member boundary is the requested minimum screen, not a validated continuum limit.

Across the full inherited surrogate matrix, the largest numerical values occur in the **two-way projected-film**
cap/5% family: overall **2.010980577** at s=5.255982 m,
and screened **1.867825477** at s=3.327589 m.
These cannot establish a real frame capacity: NFI-030-TWO-WAY identifies absent in-plane shear stiffness
behind the inherited C=4 coefficient. The 5% joint allowance also has no capacity model.
Both grids' full rows are retained, with this qualification attached.

**Each equilateral family's least modeled SF**

| Family | Reserve | Cap overall | Cap screened | Membrane overall | Membrane screened |
|---|---|---:|---:|---:|---:|
| Projected film | 5 | 1.381930 | 1.214863 | 1.368422 | 1.208585 |
| Projected film | 019 | 1.311145 | 1.151626 | 1.297919 | 1.145490 |
| Mylar / Fc 380 MPa | 5 | 0.412605 | 0.412605 | 0.412326 | 0.412326 |
| Mylar / Fc 380 MPa | 019 | 0.396986 | 0.396986 | 0.396704 | 0.396704 |
| Kapton / Ti | 5 | 0.764865 | 0.764865 | 0.763100 | 0.763100 |
| Kapton / Ti | 019 | 0.730007 | 0.730007 | 0.728242 | 0.728242 |
| Zylon 0/90 / CFRP | 5 | 1.397733 | 1.258252 | 1.384440 | 1.251857 |
| Zylon 0/90 / CFRP | 019 | 1.328131 | 1.194121 | 1.315081 | 1.187858 |

Reserve 5 is 244.472108 kg; reserve 019 is 411.298944 kg. Both also carry 100 kg systems.
Mylar uses the inherited Fc=380 MPa proxy; all other families use Fc=3900 MPa, each unqualified for the full arc.
The two lower-strength film families' overall optima already pass the screen.
Sixteen of the 32 overall optima fail it. Film is a binding mode at every continuous optimum.

[TABLES.md](52276872c0a4b508-TABLES.md) gives **all 64 least factors, binding modes, spacings and complete mass rows**;
[TABLES.csv](131601ad1913788a-TABLES.csv) adds full-precision dimensions, stresses and individual modes.
The best equilateral screened cap/5% point closes as:
tubes 4183.590023, film 214.541558, joints 44.191468, nodes 2.926575,
systems 100, reserve 244.472108, sag lift loss 99.720419 kg,
summing to 4,889.44215019 kg. Its OD is 275.082856 mm,
wall 1.137365 mm and total 0/90 gauge 109.440222 µm.
Each directional ply gets half that gauge. Membrane sag reduces this family's screened SF to
1.251857092 at 5% reserve and 1.187857743 at 019 reserve.

**What changed and what remains assumed**

Zylon now uses 024's two-direction contract, equivalent to 1.74 GPa acting on total gauge.
For every sleeve/wrap trial, end area=λN/σ and overlap=λN/(2πrτ);
the resulting mass is charged before closing tube area. Thus joint mass scales as λ² at fixed geometry.
The two percentage-joint families retain 022c's 5% of tube+film+nodes rule and UNKNOWN joint capacity.
Sub-unity Kapton/Ti rows size joints below operating load, as the order's candidate-multiplier rule requires;
their improved numerical result remains a failure at pressure multiplier one.

The added ceiling Ft=15.586 MPa is the prior check's fixed **PROJECTION** screen, not a measured allowable
or a size-corrected assembly reliability claim. Initial bow is L/1000, with Euler-amplified bending and an
explicit opposite-face tensile check. All eight screened equilateral projected-film/Zylon witnesses
remain unchanged across 24 alternatives with ceilings of 0, 7.192 or 380 MPa: their limit has no tensile stress.
Separate local/column/bending interaction remains open.

The equilateral membrane mean is exactly s²/(40ρ) **within the linear constant-tension membrane model**,
with ρ=s, giving 1.166002970933 times 024's circular-cap mean.
Primary two-way rows preserve 022c's triangular sag surrogate and evaluate the common 030 wave expression.
The separately filed square-cell/D-over-Y sensitivity lowers the two-way cap/5% projected-film screened
value to **1.728882831**. It does not supply the missing shear stiffness.
Using arc length rather than chord spacing for the screen is slightly stricter; the largest difference
in the 16 active comparisons is 0.002183537 SF.

**Verification and evidence**

All 64 final four-variable differential-evolution searches terminated successfully and were refined
with constrained multiple starts. Opening spacing/radius bounds in 16 cap/5% cases improved nothing beyond
4.07e-14 SF. They are best numerical witnesses, not certified mathematical global optima.
Independent reconstruction passed **2,800 checks**, including 112 optimized sensitivity
witnesses, direct force/moment capacities, both membrane integrations, all seven 030 source half-waves
and source pins. Maximum primary mass-closure error is 9.09e-13 kg.
No owner script was executed.

[METHOD.md](2edecc3c851d8306-METHOD.md) contains the equations, inputs and source ledger;
[SENSITIVITIES.md](39e1a539bb73b6ae-SENSITIVITIES.md) separates the altered assumptions;
[NFI.json](23377b822a4303a6-NFI.json) keeps eleven open qualification issues linked to the prior records.
No sourced complete high-strength membrane, full-size ceramic arc allowable, discrete frame stability,
complete joint qualification or manufacturing specification is established.
Work is complete under ord-admiral-rr2-mainline022d-in-band-corrected-1020; no successor job is named. Times are measurements only.
