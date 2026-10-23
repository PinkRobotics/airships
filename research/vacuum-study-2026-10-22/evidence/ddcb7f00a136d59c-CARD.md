**MAINLINE-051 COMPLETE — P3 tube targets, candidate constructions, and damage**

QUESTIONABLE / PROJECTION

The requested calculations are complete. No candidate is established by the retrieved evidence to meet a measured whole-frame Pf of 1e-3. The obstacle is a missing complete-member compression distribution, in addition to unqualified structural and damage models. The conditional calculations below identify useful numerical targets without converting fibre tension, coupon averages, or flexural statistics into tube compression allowables.

At the 5% reserve, the same-mass Hexoloy-SA model comes closest among candidates with a sourced compression number: it already meets the **operating** q=1 target under the invented whole-member scale 3.9 GPa/m=10. At 041's higher original screened loads, that hypothesis needs roughly 10% more scale or 7% more m. These are different load cases. The high-modulus K13D2U wrapped laminate also passes the mechanical screen as a **ceiling**, but its compression strength and distribution are unknown. Neither is a qualified winner.

For Hexoloy-SA, fresh same-mass mechanical SFs are **1.053993/0.997807** (5%/019 reserve). The required whole-member m10 scales at q=1 are **3.727343/3.873840 GPa**. Its hypothetical m10 Pf is 0.0006359548/0.0009349415. At 5%, the combined mechanical/reliability load multiplier is 1.045469. At 019 reserve, the local wall screen is 0.220% short in load factor; raising compression strength alone cannot repair that buckling shortfall.

For K13D2U 50/20/20/10, the same-mass ceilings are **1.135743/1.075982**. Demonstrating whole-member compression scales of **2.161413/2.245731 GPa at m10** would close the modeled reliability gap. There is no sourced compression denominator from which to claim an improvement multiplier. This is a test target, not evidence that a current K13D2U tube achieves it.

**Target surface.** There are 750 members, with actual arc lengths 1.984730–2.623498 m (mean 2.399569 m, total 1799.676624 m). A “3 m member” is a reference size for strength transfer; the calculation does not lengthen the existing frame. 019 is the named fixed reserve case, not a 19% reserve.

For independent Weibull compression events, H=Σ wᵢ(σᵢ/σ₀)^m and Pf=1−exp(−H). Thus σ₀,required=[Σwᵢσᵢ^m/(−ln(1−Pf))]^(1/m). Every member is assigned its own beam peak, including L/1000 bow and Euler amplification. Equal complete-member fits use w=1; a common 3 m fit uses w=L/3; a 1 cm³ volume fit uses w=AL/10⁻⁶. These are alternative size conventions, not interchangeable strength data.

The table gives equal complete-member scales at the **original 041 own-screen loads**, in GPa. All integer m=5–40, both probability targets, both reserve cases, operating/own-screen loads, and all size conventions are in TARGET-SURFACE.csv.

| m | Pf 1e-3, 5% | Pf 1e-3, 019 | Pf 1e-6, 5% | Pf 1e-6, 019 |
|---:|---:|---:|---:|---:|
| 5 | 16.425501 | 16.158441 | 65.397634 | 64.334342 |
| 8 | 5.984313 | 5.886999 | 14.191930 | 13.961147 |
| 10 | 4.278678 | 4.209090 | 8.537512 | 8.398658 |
| 15 | 2.740392 | 2.695806 | 4.343373 | 4.272706 |
| 20 | 2.196242 | 2.160498 | 3.102351 | 3.051861 |
| 30 | 1.763754 | 1.735041 | 2.220471 | 2.184324 |
| 40 | 1.583058 | 1.557289 | 1.881492 | 1.850864 |

At m10 the original own-screen target requires 4.278678/4.209090 GPa for Pf 1e-3: **1.09710×/1.07925×** the hypothetical whole-member 3.9 GPa scale. Alternatively m must rise from 10 to **10.74315/10.60365** (1.07432×/1.06037×), holding that scale fixed. Pf 1e-6 instead needs 8.537512/8.398658 GPa (2.18911×/2.15350×), or m=16.30240/16.08945.

At 5% reserve, a complete 3 m reference member has 2292.464 cm³ of material. Under the volume-flaw model, coupon-to-member retention is 0.21278, 0.46128, 0.67918 and 0.82412 at m=5,10,20,40. At m10 and the original screened loads, the required **1 cm³ coupon** scales are 9.088382/8.907641 GPa for Pf 1e-3, and 18.134612/17.773969 GPa for Pf 1e-6. Treating 3.9 GPa as that coupon scale gives Pf=0.99113/0.97905. At operating q=1, the original 041 whole-member hypothesis instead gives Pf=0.0006439/0.0009473; its coupon interpretation gives 0.7000/0.8187. The brief's near-unity coupon result is therefore a higher-load result, not a universal P3 probability.

**Candidate masses and SFs.** The fixed envelope retains 041's f5 geometry, outside diameters, film, nodes, systems, reserves and joints. At the common tube-mass budgets (4263.218/4108.765 kg), the lift-budget total is 4889.442 kg in both reserve cases. This total includes reserve and the sag lift debit; it is not simply vehicle dry mass.

The table's first two columns give the **5% reserve fresh-FE q≥1 witness**, with unchanged OD and increased wall where necessary. “Frame” includes tubes, joints and nodes. The total also charges film, systems, reserve and sag. These are explicit witness sections, not minimum-mass designs. The last pair are SFs/ceilings at the **original tube-mass budgets**; the witness section has its own SF in the preceding column. A ceiling means compression or other failure modes remain unmeasured. Full sections, mode values, same-section alternatives and both reserve witnesses are in FRAME-COMPARE.json, WITNESSES.json and GAPS.csv.

| Tube construction | q≥1 witness frame kg, 5% | Witness lift-budget kg | Witness SF/ceiling | Same-budget SF/ceiling 5% / 019 |
|---|---:|---:|---:|---:|
| 041-reference | 4302.0 | 4880.4 | 1.0001 | 1.0050 / 0.9514 |
| Hexoloy-SA | 4213.4 | 4791.8 | 1.0001 | 1.0540 / 0.9978 |
| CVD-PureSiC-HR | 4247.0 | 4825.4 | 1.0232 | 1.0590 / 1.0025 |
| UltraSiC-sintered | 4391.4 | 4969.8 | 1.0231 | 0.9808 / 0.9285 |
| SCS6-epoxy | 13284.6 | 13863.0 | 1.0314 | 0.0851 / 0.0806 |
| SCSUltra-epoxy | 12512.3 | 13090.7 | 1.0314 | 0.0973 / 0.0922 |
| HNS-MI-CMC-scenario | 6149.1 | 6727.5 | 1.0092 | 0.6653 / 0.6299 |
| Tyranno-SA-CVI-scenario | 6262.0 | 6840.5 | 1.0092 | 0.6384 / 0.6045 |
| M55J-UD | 8882.2 | 9460.6 | 1.0316 | 0.2093 / 0.1984 |
| M55J-70-10-10-10 | 4882.6 | 5461.0 | 1.0310 | 0.7820 / 0.7411 |
| M55J-50-20-20-10 | 4670.1 | 5248.5 | 1.0096 | 0.9321 / 0.8830 |
| K13D2U-UD | 8846.3 | 9424.7 | 1.0319 | 0.2097 / 0.1988 |
| K13D2U-70-10-10-10 | 4369.2 | 4947.6 | 1.0314 | 1.0009 / 0.9485 |
| K13D2U-50-20-20-10 | 3703.5 | 4282.0 | 1.0285 | 1.1357 / 1.0760 |
| T700S-UD | 9005.0 | 9583.4 | 1.0311 | 0.2048 / 0.1941 |
| T700S-70-10-10-10 | 8764.2 | 9342.6 | 1.0057 | 0.4091 / 0.3877 |
| T700S-50-20-20-10 | 10870.7 | 11449.1 | 1.0065 | 0.4036 / 0.3824 |
| Al6061T6 | 20600.2 | 21178.6 | 1.0090 | 0.2147 / 0.2034 |

The reference row uses 041's E=410 GPa/rho=3100/nu=.14 assumptions. The Hexoloy sheet instead reports E=430 GPa; the CVD and UltraSiC rows use their separate manufacturer property sets. The updated local wall screen uses the orthotropic Donnell coefficient and peak axial-plus-bending demand. In the isotropic limit its classical coefficient is E/√[3(1−nu²)], rather than 041's rounded 0.6E, and it retains the same unvalidated knockdown γ. This explains why the reference's revised SF is lower than 041's 1.143/1.083. The old .6E/axial-demand values remain reproduced as regression checks; this is a sensitivity, not a validated replacement safety factor.

For composites, “UD” is axial fibre. 70/10/10/10 and 50/20/20/10 are 0/+45/−45/90 degree fractions in an ideal, finely interleaved, symmetric balanced wall. These wrapped virtual tubes are not measured pultruded products. Transverse/shear constants and densities use stated assumptions; D=Q̄t³/12, B=0. Fibre tensile strength is never used as compressive strength. All composite SFs omit at least transverse compression/interlaminar failure, even when a longitudinal compression screen exists.

**Compression gaps at operating q=1, same tube-mass budget.** Whole-member m10 targets and ratios below use the fresh FE stress fields. A ratio below one means the assumed scale is sufficient for this model. A quoted average used as a whole-member Weibull scale is an explicit hypothetical assumption. “Unknown” supplies no empirical strength multiplier; the absolute target remains useful. No finite m can repair a proposed scale below a member's peak stress.

| Construction | Required whole scale GPa, 5% / 019 | × assumed compression scale, 5% | Required m, 5% |
|---|---:|---:|---:|
| 041-reference | 3.731 / 3.878 | 0.95657 | 9.6794 |
| Hexoloy-SA | 3.727 / 3.874 | 0.95573 | 9.6733 |
| CVD-PureSiC-HR | 3.858 / 4.009 | unknown | unknown |
| UltraSiC-sintered | 3.792 / 3.942 | 1.0836 | 10.637 |
| SCS6-epoxy | 2.834 / 2.948 | unknown | unknown |
| SCSUltra-epoxy | 2.685 / 2.792 | unknown | unknown |
| HNS-MI-CMC-scenario | 3.291 / 3.426 | 3.2915 | 110.04 |
| Tyranno-SA-CVI-scenario | 3.355 / 3.492 | unknown | unknown |
| M55J-UD | 1.953 / 2.029 | 2.194 | 24.376 |
| M55J-70-10-10-10 | 1.959 / 2.036 | 2.9752 | 57.177 |
| M55J-50-20-20-10 | 1.967 / 2.045 | 3.9206 | no finite m |
| K13D2U-UD | 2.154 / 2.237 | unknown | unknown |
| K13D2U-70-10-10-10 | 2.157 / 2.241 | unknown | unknown |
| K13D2U-50-20-20-10 | 2.161 / 2.246 | unknown | unknown |
| T700S-UD | 1.909 / 1.987 | 1.3163 | 12.587 |
| T700S-70-10-10-10 | 1.935 / 2.018 | 1.7734 | 17.542 |
| T700S-50-20-20-10 | 1.975 / 2.068 | 2.3166 | 27.44 |
| Al6061T6 | unknown / unknown | unknown | unknown |

The same calculation at each candidate's screened load and at its q≥1 witness is in GAPS.json, including m=5,8,10,11,15,20,30,40, Pf 1e-3/1e-6, coupon and 3 m references. Dividing a listed required m by the assumed 10 gives the m multiplier. This mathematical shape parameter improvement is not a measured processing trend.

For a monolithic 5% frame, the single missing reliability result is a complete-tube compression population meeting the target: at operating pressure the assumed Hexoloy scale already suffices, while preserving the original higher screen requires the roughly 10% scale improvement above. No one strength improvement closes all structural, reliability and hail gaps. For the fibre constructions, load sharing and matrix/interface failure prevent inference of a tube distribution from a filament or tow distribution.

The public M55J and T700S composite compression numbers are 890 and 1450 MPa, respectively, not tube allowables. M55J's current composite modulus is 338 GPa, not its fibre modulus 540 GPa. K13D2U's 935 GPa and 3.7 GPa are fibre modulus and tensile strength; no tube compression denominator was retrieved. [Toray M55J](https://www.toraycma.com/wp-content/uploads/M55J-Data-Sheet.pdf), [Toray T700S](https://www.toraycma.com/wp-content/uploads/T700S-Data-Sheet.pdf), [Mitsubishi DIALEAD](https://www.m-chemical.co.jp/carbon-fiber/pdf/dialead/composites.pdf).

The HNS research population illustrates the statistical distinction: filament m=8.42 and scale 3062 MPa versus 25 mm bundle m=9 and scale 1730 MPa; neither measures tube compression. Tyranno-SA/CVI m=10.2 describes flexure of 25×4×2 mm bars, not 3 m axial crushing. [HNS primary data](https://pmc.ncbi.nlm.nih.gov/articles/PMC7452681/), [Tyranno primary experiment](https://www.jstage.jst.go.jp/article/matertrans/44/9/44_9_1797/_pdf). SOURCES.md retains the source, test mode, size and missing properties for every construction.

**Hail, conditional on a direct tube strike.** Use 50.8 mm ice at 32.004 m/s, a 12 mm contact radius, the inherited flow contact pressure 0.942725 MPa and the inherited Shi multiplier. 045's plate-on-membrane-foundation method is reproduced; an orthotropic plate with foundation k=Ehoop t/r² extends it to the virtual laminates. This approximation omits dynamic contact, axial preload, interface damage and residual strength.

The two probability columns below deliberately impose the **same hypothetical matching-contact distributions on every construction**: (scale=299 MPa,m=4.6) and (scale=192 MPa,m=5.5). They answer what 045's formula returns under those assumptions. They are **not measured break probabilities**, and are not a basis for ranking unlike materials. For the ceramic rows they are still uncalibrated transfers of C-ring/sectored flexural tests. For composites and ductile aluminium there is no basis to equate these events with member severance. Actual identified break-probability bounds remain [0,1].

The table uses the same-budget 5% sections; both reserves, all witness sections, seven hail sizes and pressure models are in HAIL.json. HAIL-DESIGN.csv is the compact design-strike table.

| Construction | Shi surface demand MPa | Hypothetical P, 299/m4.6 | Hypothetical P, 192/m5.5 |
|---|---:|---:|---:|
| 041-reference | 113.47 | 0.0115326 | 0.0539264 |
| Hexoloy-SA | 113.47 | 0.0115326 | 0.0539264 |
| CVD-PureSiC-HR | 125.74 | 0.0184284 | 0.0928933 |
| UltraSiC-sintered | 123.87 | 0.0172086 | 0.0858528 |
| SCS6-epoxy | 535.36 | 1 | 1 |
| SCSUltra-epoxy | 517.02 | 0.999996 | 1 |
| HNS-MI-CMC-scenario | 110.13 | 0.0100567 | 0.0459322 |
| Tyranno-SA-CVI-scenario | 111.93 | 0.0108302 | 0.0501017 |
| M55J-UD | 372.03 | 0.934952 | 1 |
| M55J-70-10-10-10 | 137.78 | 0.0279281 | 0.148882 |
| M55J-50-20-20-10 | 115.27 | 0.012389 | 0.0586338 |
| K13D2U-UD | 472.15 | 0.999719 | 1 |
| K13D2U-70-10-10-10 | 159.22 | 0.0536002 | 0.300302 |
| K13D2U-50-20-20-10 | 132.67 | 0.0235244 | 0.122739 |
| T700S-UD | 219.54 | 0.214517 | 0.8763 |
| T700S-70-10-10-10 | 119.13 | 0.0144052 | 0.069886 |
| T700S-50-20-20-10 | 102.03 | 0.00708927 | 0.0304267 |
| Al6061T6 | 123.94 | 0.0172527 | 0.0861067 |

For the resized sintered-SiC frame, the two transferred Shi probabilities are 1.153–5.393% (5%) and 1.182–5.548% (019). Flow-pressure values are separately reported, not used as the ends of that interval. The source's old 55.549976 MPa/MPa coefficient is reproduced with its assumed nu=.16; the new 041 reference uses nu=.14.

A different, still uncalibrated choice—PremaTech's CVD flexure scale424 MPa/m11—gives 1.56047e-06 at the CVD same-budget section. The Tyranno flexural fit gives 2.32772e-08. Those small numbers do not demonstrate superior tube survival: effective size, stress mode, grade, rate and failure event differ. Matching-contact targets are provided for m5/10/20/40 and conditional strike probabilities 1e-3/1e-6, so missing probability evidence becomes a numerical test target. CFRP first-ply stress screens and aluminium's hail-only yield margin are also reported separately from severance.

**One member lost.** Each material/reserve pair was solved intact and with two independently selected member removals (median and maximum original compression). All beam pieces of the member and their unused internal nodes are removed; the adjacent triangular pressure bays become a quadrilateral. Pressure remains a balanced derivative of the closed fan volume, rather than loading unsupported deleted nodes. Joints retain their original, individually sized sleeves and bond overlaps.

Every one of the 72 same-budget deletion cases has a modeled secondary-failure trigger. The table reports the worst post-loss SF/ceiling and largest compression amplification among the two samples, at operating pressure. It is a static/tangent warning, not a computed dynamic cascade history. No statement that every possible lost edge produces the identical sequence is implied.

| Construction | Post-loss SF/ceiling, 5% / 019 | Max compression ratio, 5% / 019 |
|---|---:|---:|
| 041-reference | 0.4345 / 0.4100 | 2.503 / 2.533 |
| Hexoloy-SA | 0.4557 / 0.4300 | 2.488 / 2.517 |
| CVD-PureSiC-HR | 0.4585 / 0.4326 | 2.476 / 2.503 |
| UltraSiC-sintered | 0.4243 / 0.4004 | 2.508 / 2.538 |
| SCS6-epoxy | 0.0381 / 0.0360 | 2.597 / 2.640 |
| SCSUltra-epoxy | 0.0436 / 0.0412 | 2.533 / 2.568 |
| HNS-MI-CMC-scenario | 0.2879 / 0.2718 | 2.711 / 2.771 |
| Tyranno-SA-CVI-scenario | 0.2765 / 0.2610 | 2.725 / 2.788 |
| M55J-UD | 0.0938 / 0.0886 | 2.370 / 2.389 |
| M55J-70-10-10-10 | 0.3429 / 0.3240 | 2.449 / 2.473 |
| M55J-50-20-20-10 | 0.4047 / 0.3881 | 2.545 / 2.579 |
| K13D2U-UD | 0.0944 / 0.0892 | 2.309 / 2.323 |
| K13D2U-70-10-10-10 | 0.4405 / 0.4161 | 2.366 / 2.383 |
| K13D2U-50-20-20-10 | 0.4865 / 0.4591 | 2.424 / 2.446 |
| T700S-UD | 0.0910 / 0.0860 | 2.694 / 2.753 |
| T700S-70-10-10-10 | 0.1784 / 0.1686 | 3.014 / 3.126 |
| T700S-50-20-20-10 | 0.2281 / 0.2155 | 3.627 / 4.105 |
| Al6061T6 | 0.1027 / 0.0969 | unknown / unknown |

In the 5% reference, peak compression rises to 2.461–2.539 GPa, about 2.426–2.503× intact. This is not just axial force multiplication: bending and beam-column amplification dominate. The local wall screen falls below 0.45; the retained joint screen falls to about 0.49–0.51, and the merged-bay film screen to about 0.773. At 019 reserve the analogous film screen is about 0.733. The actual geometry gives a tension multiplier near 1.478, close to but distinct from 045's equilateral 1.5 assumption.

A better compression material alone does not resolve these joint and film failures. A damage-tolerant proposal needs a changed load path, joints and film-bay support with their masses charged. Existing perfect-joint/global-knockdown assumptions remain unvalidated; two static removals cannot identify a lifetime loss rate or a dynamic cascade probability.

**Is a non-brittle tube better?** CFRP is not generally ductile; delamination, matrix cracking, microbuckling and compression-after-impact can govern. The present M55J and T700S reference constructions need higher mass than the buoyancy budget to reach the mechanical screen, and still lack member statistics. Ductile 6061-T6 needs much greater mass at this fixed OD and geometry. K13D2U with hoop and ±45 reinforcement is the promising conditional stiffness/mass construction, but no sourced compression population or impact-survival evidence supports calling it the better frame today. These comparisons are confined to the stated geometry and constitutive assumptions; they are not a global optimum or a proof that all composite designs fail. [NASA compression-after-impact research](https://ntrs.nasa.gov/api/citations/20160010546/downloads/20160010546.pdf).

017b's flat SiC trend concerns the cited stiffness/density history. It does not establish that strength scatter, processing defects, interfaces, proof testing or damage tolerance are frozen. Those are the relevant directions exposed here, alongside a load path that survives a missing member.

**Evidence and completion.** 592 target checks, six original scalar regressions, 145 hail/integral/angular checks and 560 FE/mesh checks pass. The independent m6 calculation is checked against the prior m24 reference and against focused m12 intact/deleted-member cases. Every admitted job recorded its release; all runs retained one core and 1 GiB. Exit-75 refusals were retried under the resume order. One manual retry was inadvertently 29 seconds after the preceding refusal; the subsequent retry wrapper enforced at least 60 seconds. The initial comparison's fixed m=5000 root bracket was corrected to an analytic bracket. The hail anchor's nu mismatch was traced to the pinned source, not hidden by loosening its tolerance.

The earlier partial report and all its pinned files are preserved. Its unfinished computations are resolved by this package; physical qualification issues remain in NFI.json. INPUTS.json pins source copies; per-attempt START/END records pin executed code; CODE.tar.gz and MANIFEST-051-COMPLETE.json capture the completed package. Start/end times are measurements, with no task or phase cap. Stop and file; robotics owns any next job.
