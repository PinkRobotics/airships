# CHECK MAINLINE-022b and MAINLINE-022c

Unit `vacuum-mainline022b-check-1020`; order `ord-admiral-rr2-check022b-codex-d1c0-1020`. Every engineering result is **QUESTIONABLE**; unvalidated materials, geometry transfers and additional screens are **PROJECTION**. No qualified system safety factor is established.

**Finding.** The reported arithmetic reproduces. The Zylon 0/90 film transfer omits a factor of two from its source contract. The long-span projection rows also omit a tensile-bending limit, and the six scored frame/film modes do not include joint strength or coupled shell/column instability. These are separate findings: matching arithmetic does not resolve them.

The check covers the filed 022b EQUILIBRIUM, GAMMA and FOLD artifacts, plus both cap and membrane branches of 022c, which filed during this work. **All 70 published rows and their independently rebuilt search-grid maxima match**, with **4,894 field comparisons**, **33 ancillary arithmetic checks**, and **894 printed-number comparisons**. No owner script was run or imported. All **63 artifact pins and 12 supporting PDF pins** match. `ARITHMETIC.json` and `SOURCE-CHECKS.json` retain every comparison; `MISMATCHES.json` lists 24 exact source-contract or omitted-mode differences.

**Equilibrium and the rise correction.** The three equilateral families each have member-line density \(2/(\sqrt3s)\), and their squared direction cosines sum to \(3/2\). Thus \(N_x=\sqrt3N/s=pR/2\), giving

\[
N_\triangle=\frac{pRs}{2\sqrt3},\qquad N_\square=\frac{pRs}{2}.
\]

At s=2.04 m, these are **562,166.272760 N** and **973,700.546722 N**, ratio √3. Counts follow the stated continuum areas: triangular members \(8\pi\sqrt3R^2/s^2\), vertices=members/3+2; two-way members \(8\pi R^2/s^2=2V-4\). The global formula does not contain N. Using arc length \(2R\arcsin[s/(2R)]\) for mass and Euler/Perry, while retaining chord spacing in the stated global/film formulas, reproduces the cards.

The rise-8 example also reproduces: N=303,128.872567 N, crown moment=32,090.296856 N·m, mean compression=1.102196386 GPa and bending=1.280394108 GPa. The 380 MPa stress ratios are 0.344766145791 before bending and 0.159490269506 after it. Arbitrary rise cannot reduce the equilibrium force. The quoted fixed-mass local/global rebalance is **1.486447192932**.

**Local gamma.** The implemented curve
\(\gamma=1-0.901[1-\exp(-\sqrt{r/t}/16)]\)
gives **0.528523265244 at r/t=140.5**. It is used on the local mode, independently of global k. At the 022b 6.15 m projection point, outer-radius gamma is **0.576583973171**. The small difference from 025's mid-surface-radius convention is documented in `SOURCE-CHECKS.json`; it is not an arithmetic error.

The long-member application remains unresolved: the cap projection points have L/r of about **37.47 and 37.94**. NASA cautions above L/r=5 and requires shell/column interaction evaluation. The selected gamma is therefore a model sensitivity for these curved ceramic struts. [NASA SP-8007 Rev.2, pp.23–25](https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf).

**Reported and refined principal results.** These are the inherited six-mode calculations, including the uncorrected Zylon directional formula where named. “Refined” means an independently found continuous candidate with the same formulas; it is not a certified global optimum or a corrected complete system.

| Equilateral case | 022b least factor | 022c cap least factor | 022c published s, m | Refined 022c factor |
|---|---:|---:|---:|---:|
| Projection film, Fc=3.9 GPa, 5% reserve | 1.375249030041 | 1.373321385784 | 6.15 | 1.385057003046 |
| Same, 019 reserve | 1.298637598856 | 1.294540344663 | 6.15 | 1.314271502475 |
| Mylar, Fc=380 MPa proxy, 5% | 0.411837535103 | 0.411790451893 | 0.55 | 0.412605410971 |
| Same, 019 reserve | 0.395898698999 | 0.395851626757 | 0.55 | 0.396986471968 |
| Ti joint / Kapton, 5% | 0.739113638303 | 0.739113638303 | 1.85 | 0.746899090517 |
| Same, 019 reserve | 0.702127028825 | 0.701745910728 | 1.85 | 0.709771640707 |
| CFRP joint / Zylon, inherited direction formula, 5% | 1.486917096861 | 1.485116372062 | 5.50 | 1.520374657013 |
| Same, 019 reserve | 1.418299174126 | 1.417046571748 | 5.70 | 1.441177129177 |

The stated search uses **0.05 m spacing steps, 12 logarithmic film gauges and 480 radius candidates**. Its finite-grid maxima reproduce, but the film sampling affects the chosen spacing: the 022c Zylon 5% continuous witness is at **6.274813 m**, rather than the published 5.50 m. The projection-film witness is at **6.194427 m**.

**Radius-cap check.** Opening the search from s≤8 m/rₒ≤0.25 m to **s≤19.9 m/rₒ≤1 m**, while retaining rₒ<s/3, returns the same continuous maximum within \(9\times10^{-12}\) for the tested projection-film and CFRP/Zylon branches of both 022b and 022c. All four remain inside the original bounds, with radii about **0.168–0.173 m**. The 0.25 m cap is not driving these tested results. This is numerical evidence, not a proof over every possible architecture.

**Demonstrated Zylon source mismatch.** Pinned 024 states
\(t_\mathrm{total}=2ps/(2\sigma_\mathrm{fiber})\)
for a 0/90 membrane. Half of the total fiber thickness carries each principal direction. The scan charges mass for one total thickness but uses the isotropic-film formula \(2\sigma_\mathrm{fiber}t_\mathrm{total}/(ps)\), giving both directions all of it. Using 024's contract halves that film factor:

| Published equilateral point | Owner film factor | Correct film factor and least six-mode factor at the same geometry |
|---|---:|---:|
| 022b Zylon, 5% | 1.493752313215 | **0.746876156607** |
| 022b Zylon, 019 | 1.429586806896 | **0.714793403448** |
| 022c cap Zylon, 5% | 1.493752313215 | **0.746876156607** |
| 022c cap Zylon, 019 | 1.417046571748 | **0.708523285874** |

The two-way rows have the same factor error; their exact differences are in `MISMATCHES.json`. The correction may be implemented by using \(\sigma_\mathrm{effective}=1.74\) GPa with total thickness, or by charging both directional ply masses.

Correcting only this factor and continuously reoptimizing the cap cases gives **1.409015864574 / 1.337619522959** for 5%/019 reserves. These remain incomplete model results: their limiting loads develop about **1.14/1.18 GPa tensile bending**, and joint strength is still omitted. They are not repaired system safety factors.

**Tensile bending omitted from the long-span projection rows.** Independently solving the elastic imperfect-column stress field gives
\(\sigma_b=\sigma\eta/(1-\sigma/\sigma_E)\).
The owner’s Perry root checks \(\sigma+\sigma_b\) against the assumed compressive input; it does not check positive \(\sigma_b-\sigma\).

| Projection-film point | Owner least factor | Tensile stress at that multiplier | Least factor at same geometry with an assumed Ft=15.586 MPa |
|---|---:|---:|---:|
| 022b, 5% | 1.375249030041 | **664.636 MPa** | 1.340839305928 |
| 022b, 019 | 1.298637598856 | **1,080.415 MPa** | 1.253842631884 |
| 022c cap, 5% | 1.373321385784 | **665.740 MPa** | 1.338919689892 |
| 022c cap, 019 | 1.294540344663 | **990.543 MPa** | 1.251969951123 |

These four rows have no positive midspan tensile stress at the actual design pressure. The omitted tension appears as the pressure is increased toward the reported limiting multiplier. The 15.586 MPa screen is a **PROJECTION** from 025's illustrative uniform-tension assumptions, not a qualified allowable. Actual effective stressed volume, surface populations and contact fields must be resolved. With that explicit constant screen and continuous reoptimization, the cap projection cases give **1.381929805095 / 1.311145459764**; full-size compressive qualification remains unknown.

**Combined local-buckling diagnostic.** Checking local shell stress against mean compression alone while independently amplifying bending near Euler does not establish interaction. As a clearly labeled diagnostic, applying the same local stress threshold to the amplified compressive face gives **1.069350946066 / 1.001382933469** at the two published cap projection geometries. These are **PROJECTION diagnostics**, not validated replacement capacities; curvature, shell bending, ovalization and boundary conditions require a coupled treatment.

**Joint capacity and the meaning of “least.”** The imported 023 sleeve/wrap law is \(m_\mathrm{end}=CN^2/r\), with sleeve area \(N/\sigma\) and overlap \(N/(2\pi r\tau)\). It spends the assumed axial and bond allowables at design N, so its **frozen joint pressure multiplier is 1** in that sizing model. The quoted six-mode minimum omits this mode. For the 022c Zylon 5% point, sizing those same formulas at the claimed λ=1.485116372062 would multiply joint mass by **2.205570638565**, from **23.111041 to 50.973034 kg**. That extra **27.861993 kg** must be charged before reoptimization. Real ceramic joint strength and rotational stiffness remain unqualified.

**Sag, provenance and scale.** The selected 024 cap gives losses **62.9000389203 kg at 2 m**, **125.800077841 kg at 4 m**, and **64.1580396987 kg at 2.04 m**. The earlier linear charge is **61.1180268774 kg at 2 m**. The s/40 sensitivity is **1.16600297093** times the cap mean. Both complete 022c branches reproduce. The circular cap is an explicit approximation, and its transfer to two-way cells still needs its own geometry.

The source and assumption chain is recorded in `SOURCE-LEDGER.md`. It includes Kapton's assumed knockdown, the unsourced Zylon membrane, rounded sleeve coefficients, and 025's unknown compression allowable. The quoted prior-check values 1.205/1.130, braze mass, pin bearing and fixed Kapton/Teonex masses independently reproduce. Measured origin/end times are preserved as records, not independently recreated clock observations.

The cap projection point now requires an arc **6.251292 m long**, **335.280239 mm OD**, and **1.623088 mm wall**. That length is **4.465×** the documented 1.4 m one-piece SA catalogue length used in 025. A combined curved-tube production capability has not been established; this is an evidence gap, not a proof of impossibility.

**Handoff.** Nine explicit followups are in `NFI.json`; they do not stop this check or another card. `RESULTS.json` records the numerical witnesses, diagnostics and 87 packaging/verification checks. Reproduce with `check_model.py`, `check_studies.py`, `check_sources.py`, then `assemble_check.py`. The completed check is filed once to sciences, cc co/xo/robotics. CHECK.md assigns no successor; await the next queue order.
