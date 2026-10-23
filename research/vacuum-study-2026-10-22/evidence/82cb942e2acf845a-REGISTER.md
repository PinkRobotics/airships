# MAINLINE-030 NFI register — every filed card's and check's NFI rows, merged

QUESTIONABLE throughout; PROJECTION where a row says so. Nothing here is a certification. Built by build030.py from TOPICS-JOINED.json (each verbatim row normalised by a sub-worker, completeness-checked), the checker's CANON.json merge map, and CHECK-VERDICTS.json. Where two cards name the same gap, every id is kept. Report ids and NFI file paths are in the source table at the end; REGISTER.json carries the same data per row.

86 register rows from 362 filed rows in 41 reports.


## T01 Case and atmosphere

**R001. hull radius and volume convention (mould line vs mid-surface, wall intrusion)**
- Unknown: Handbook radius is the middle surface; ratios use external 10 m and are unaffected since both pressures scale as 1/R^2; absolute pressure on thick rows needs an inner mould line.
- Today: buckling-peak core 1.81457668 m at 1 kg/m3 [MAINLINE-007] | external radius 10 m [MAINLINE-07B] | R = 10 m external [CHECK-MAINLINE-07B]
- Needed or settling test: Inner and outer mould lines [MAINLINE-007] | Inner mould line for absolute pressure [MAINLINE-07B] | Define inner and outer mould lines. [rpt-mainline-grok-estimates-card-1019] | Inner and outer mould lines. [MAINLINE-002]
- Owner: CHECK-MAINLINE-07B, MAINLINE-002, MAINLINE-003, MAINLINE-007, MAINLINE-007B, rpt-mainline-grok-estimates-card-1019. State: assumption.
- Check: raised by CHECK-MAINLINE-07B.
- Ids: MAINLINE-007 NFI-GEOM; MAINLINE-07B NFI-GEOM; rpt-mainline-grok-estimates-card-1019 NFI-GEOM; MAINLINE-002 NFI-GEOM; MAINLINE-003 NFI-GEOM; CHECK-MAINLINE-07B NFI-GEOM

**R002. ISA case is a standard dry column, not a site or day**
- Unknown: Dry constant-g geopotential formula used with geometric height substituted; no humidity case; density and pressure drive float margin and every safety factor.
- Today: N2 0.78084; O2 0.20946 (not in case) [MAINLINE-024] | 500 m ISA point matches pinned case within 0.1 Pa [MAINLINE-010]
- Needed or settling test: Include composition in the case [MAINLINE-024] | a measured column once a site is named [MAINLINE-010] | Pin an ISO 2533 or ICAO Doc 7488 table at 500 m plus a humidity case. [rpt-mainline-grok-estimates-card-1019] | Keep the 500 m case as the basis. [rpt-mainline-grok-estimates-card-1019]
- Owner: MAINLINE-010, MAINLINE-024, rpt-mainline-grok-estimates-card-1019. State: assumption.
- Check: source cards checked by rpt-ref-7d4d494ebf14f37f5ea0 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-024 NFI-AIR-FRACTIONS; MAINLINE-010 NFI-010-ISA; rpt-mainline-grok-estimates-card-1019 NFI-ISA; rpt-mainline-grok-estimates-card-1019 NFI-CHARTER


## T02 Shell knockdown kd

**R003. buckling SF is linear in kd only at fixed geometry**
- Unknown: The claim that local needs are independent of kd holds only at fixed geometry; re-optimising for a new kd changes thicknesses and local needs.
- Today: kd = 0.2 [MAINLINE-005] | 0.2 (0.90 optimistic carry) [MAINLINE-006]
- Needed or settling test: Qualify the statement as fixed-geometry; rebuild the design if kd changes [CHECK-MAINLINE-013] | kd from the 004 named knockdown curve; multiply each E by 0.2/kd [MAINLINE-005] | MAINLINE-004 filed values [MAINLINE-008] | Multiply buckling SF by kd/0.2 when another knockdown is adopted. [CHECK-MAINLINE-006]
- Owner: CHECK-MAINLINE-006, CHECK-MAINLINE-007, CHECK-MAINLINE-013, MAINLINE-004, MAINLINE-006, MAINLINE-012. State: assumption, exists_today.
- Check: raised by CHECK-MAINLINE-006, CHECK-MAINLINE-007, CHECK-MAINLINE-013.
- Ids: CHECK-MAINLINE-013 NFI-CHECK013-KD-CONDITION; MAINLINE-005 NFI-005-KD; MAINLINE-008 NFI-008-KD; CHECK-MAINLINE-006 NFI-KD-020; MAINLINE-006 NFI-KD-020; CHECK-MAINLINE-007 NFI-KD; MAINLINE-012 NFI-KD-020

**R004. knockdown transfer from monocoque to sandwich sphere at R 10 m**
- Unknown: The curve is monolithic clamped-cap evidence; phi equal pi and the equivalent thickness are transfers onto a complete sandwich sphere, so the buckling SF is not a validated sandwich knockdown.
- Today: conservative SP-8032 cap factor, central 0.20, optimistic 0.90 [MAINLINE-08B] | transfer t_eq = sqrt(3)(d+tf) [MAINLINE-015] | dimple 0.20, flat 0.22 (numerical, small hemispheres) [MAINLINE-04B]
- Needed or settling test: a sandwich-specific knockdown for this geometry [MAINLINE-08B] | a sandwich imperfection study at this geometry [MAINLINE-015] | A sandwich knockdown test or formula at these proportions. [MAINLINE-004] | A sandwich source at these proportions. [MAINLINE-04B]
- Owner: MAINLINE-004, MAINLINE-008B, MAINLINE-015, MAINLINE-04B. State: assumption, unknown.
- Check: source cards checked by rpt-ref-c49d322288a0b11e4381 (admitted_with_defects), rpt-ref-88e650e7f8b713866e0b (partial), rpt-mainline004-check-glm-1019 (reproduced); no objection on this row.
- Ids: MAINLINE-08B NFI-008B-KD-TRANSFER; MAINLINE-015 NFI-015-SANDWICH-TRANSFER; MAINLINE-004 NFI-TRANSFER; MAINLINE-04B NFI-TRANSFER; MAINLINE-04B NFI-SANDWICH

**R005. monocoque sphere knockdown kd: value and range (SP-8032 curve, 0.14 to 0.9)**
- Unknown: gamma_d is 0.20 on the moderate branch; 0.90 is not a handbook value but the precision direction; 0.1407 conservative. Separation of face-modulus knockdown from core-shear flexibility is untested.
- Today: kd = 0.2 [MAINLINE-007] | kd 0.2 main; 0.1407 conservative; 0.9 optimistic [MAINLINE-009] | gamma_d 0.2 main; 0.1407 conservative; 0.9 optimistic [MAINLINE-009] | 0.14 + 3.2/lambda^2 form (text reproduction) [MAINLINE-004]
- Needed or settling test: Knockdown curve from the owning card [MAINLINE-007] | Knockdown tests on sandwich spheres at lambda near 66 [MAINLINE-009] | Tests separating face-modulus knockdown from core-shear flexibility on a complete sphere [MAINLINE-009] | Evaluate NASA SP-8032 at the complete-sphere geometry. [rpt-mainline-grok-estimates-card-1019]
- Owner: MAINLINE-002, MAINLINE-003, MAINLINE-004, MAINLINE-009, MAINLINE-014, MAINLINE-04B, MAINLINE-14B, rpt-mainline-grok-estimates-card-1019. State: assumption, resolved, unknown.
- Check: source cards checked by rpt-1228-mainline013-independent-check-1020 (admitted_with_defects), rpt-ref-650cc5448a49ba2d595f (reproduced), rpt-mainline007-check-lead4f19-1019 (reproduced); no objection on this row.
- Ids: MAINLINE-007 NFI-KD; MAINLINE-009 NFI-KD-PRECISION; MAINLINE-009 NFI-HANDBOOK-GAMMA; rpt-mainline-grok-estimates-card-1019 NFI-KD; MAINLINE-002 NFI-KD; MAINLINE-003 NFI-KD; MAINLINE-004 NFI-KD; MAINLINE-04B NFI-OPT-GAP; MAINLINE-04B NFI-LAMBDA; MAINLINE-04B NFI-LRSM; MAINLINE-04B NFI-CLASSICAL; MAINLINE-014 NFI-KD-01407; MAINLINE-14B NFI-KD-01407


## T03 Crimp-branch gamma

**R006. core shear (crimp) in sandwich buckling: formula and Gc basis**
- Unknown: Advisory crimp replaced by sourced equations; sourced cores stay on the moderate branch, buckling SF trimmed. A core G below about 2.45 MPa would enter crimping; none do.
- Today: advisory crimp target cleared by catalog G at 16-38 kg/m3 [MAINLINE-007] | Kc trims buckling SF to 0.864-0.991 of the MAINLINE-007 value; crimp entry below G about 2.45 MPa [MAINLINE-07B]
- Needed or settling test: Published sandwich-shell formula including transverse shear [MAINLINE-007] | Sourced crimp formula [MAINLINE-007] | A published sandwich-sphere formula that includes core shear. [rpt-mainline-grok-estimates-card-1019] | A published sandwich formula that includes shear. [MAINLINE-002]
- Owner: CHECK-MAINLINE-006, MAINLINE-002, MAINLINE-003, MAINLINE-004, MAINLINE-006, MAINLINE-007B, rpt-mainline-grok-estimates-card-1019. State: assumption, resolved.
- Check: raised by CHECK-MAINLINE-006.
- Ids: MAINLINE-007 NFI-SAND; MAINLINE-007 NFI-SHEAR; MAINLINE-07B NFI-SHEAR; rpt-mainline-grok-estimates-card-1019 NFI-SAND; MAINLINE-002 NFI-SAND; MAINLINE-003 NFI-SAND; MAINLINE-003 NFI-SHEAR; MAINLINE-004 NFI-SAND; CHECK-MAINLINE-006 NFI-SHEAR; MAINLINE-006 NFI-SHEAR

**R007. gamma(Vc) for a sandwich sphere: CR-1457 step (0.20 below Vc 2, 1 above) vs 018 curves; P2 lead needs 0.468-0.595 (O1)**
- Unknown: A high shear modulus leaves the crimp branch and gamma becomes the knockdown 0.20; best aluminium stiff-branch rows reach SF 0.669 and 0.642, below the HRH-10 crimp balance 0.685.
- Today: gamma 0.2 at Vc=2 [CHECK-MAINLINE-09C5] | With same curve for both: Al 0.847 vs aramid 0.609 (optimistic line) [CHECK-019] | gamma_d 0.20 on moderate branch [MAINLINE-07B] | step 0.2 to 1 at Vc=2 vs 0.2+0.4*min(Vc,2) [MAINLINE-027]
- Needed or settling test: gamma = 1 for Vc>=2 per cited convention [CHECK-MAINLINE-09C5] | State the equality convention when carrying the branch wording [CHECK-MAINLINE-14B] | Re-solve budgets under the same gamma curve for both families [CHECK-019] | gamma_d 1 on crimping branch (handbook) [MAINLINE-07B]
- Owner: CHECK-019, CHECK-MAINLINE-07B, CHECK-MAINLINE-09C5, CHECK-MAINLINE-14B, MAINLINE-007B, MAINLINE-014, MAINLINE-017, MAINLINE-018, MAINLINE-018B, MAINLINE-021, MAINLINE-021B, MAINLINE-027, MAINLINE-028, MAINLINE-14B. State: PROJECTION, assumption, unknown.
- Check: OPEN, the lead's whole margin. 018 (checked: rpt-ref-62323cf6831eb964377f) sources the step to CR-1457; 018b measures 1.44-1.54 above Vc 2 on R/tc 13 shells (checked: rpt-ref-d458cd5a32d90025482b), transfer QUESTIONABLE. OBJECTION rpt-check019-opus-1020: the step gives aramid the optimistic and aluminium the conservative reading; with one curve for both, aluminium leads.
- Ids: CHECK-MAINLINE-09C5 NFI-BRANCH-EQUALITY; CHECK-MAINLINE-14B NFI-BRANCH-EQUALITY; CHECK-019 NFI-CHK019-GAMMA-PAIRING; MAINLINE-07B NFI-KD; MAINLINE-019 NFI-019-BRANCH; MAINLINE-027 NFI-027-GAMMA; MAINLINE-020 NFI-020-INHERITED-MODEL; MAINLINE-021 NFI-021-GAMMA; MAINLINE-021 NFI-021-CRIMP-BRANCH-GAMMA; MAINLINE-021 NFI-021-CONSERVATIVE-READING; MAINLINE-21B NFI-021b-GAMMA; MAINLINE-21B NFI-021b-ARAMID-BLOCKED; MAINLINE-028 NFI-028-20; CHECK-MAINLINE-07B NFI-SHEAR; CHECK-MAINLINE-07B NFI-KD; MAINLINE-014 NFI-HEMISPHERE; MAINLINE-14B NFI-HEMISPHERE; MAINLINE-14B NFI-STIFF-BRANCH; MAINLINE-017 NFI-017-GC-BRANCH


## T04 Wrinkling and core Ec

**R008. core Ec (stabilised datasheet value) transferred into the wrinkling formula**
- Unknown: Plascore PAMG-XR1 5052 prints no stabilised compressive modulus and no crush column; Ec is transferred from Hexcel CR-III 5052; crush is Plascore bare, not the Hexcel crush-column test.
- Today: catalog cores miss product by about 40-180x [MAINLINE-007] | Hexcel wrinkling SF 0.0565 and 0.0415 [MAINLINE-07B] | coefficient 0.5 on cube root of E_f*Ec*Gc [MAINLINE-08B] | catalog cores 16-38 kg/m3 clear advisory crush and crimp [CHECK-MAINLINE-007]
- Needed or settling test: Sourced wrinkling formula keeping Ec and Gc separate; aluminium honeycomb Ec [MAINLINE-007] | Sourced honeycomb Ec [MAINLINE-07B] | 007b sourced sandwich-shell shear and wrinkling formulas [MAINLINE-08B] | Separate Ec and Gc from a datasheet. [MAINLINE-003]
- Owner: CHECK-MAINLINE-007, MAINLINE-003, MAINLINE-007B, MAINLINE-014, MAINLINE-14B. State: assumption, unknown.
- Check: raised by CHECK-MAINLINE-007.
- Ids: MAINLINE-007 NFI-WRINKLE; MAINLINE-07B NFI-WRINKLE; MAINLINE-08B NFI-008B-WRINKLE-FORMULA; MAINLINE-003 NFI-WRINKLE; CHECK-MAINLINE-007 NFI-SAND/SHEAR/WRINKLE/CRUSH; MAINLINE-014 NFI-ALHC; MAINLINE-14B NFI-PLASCORE-EC; MAINLINE-14B NFI-HRH36

**R009. equibiaxial wrinkling interaction factor (0.682) on a curved face**
- Unknown: The flat-plate interaction is applied to equibiaxial membrane stress of a sphere; a sphere-specific interaction could replace it.
- Today: equibiaxial factor 0.6823 (from R^3+R=1) [MAINLINE-07B] | equibiaxial factor 0.6823, already inside the stated SF [MAINLINE-009] | 0.6823278038280193 [CHECK-MAINLINE-07B]
- Needed or settling test: Sphere-specific wrinkling interaction [MAINLINE-07B] | Sphere-face wrinkling test [MAINLINE-009] | A sphere-specific wrinkling interaction. [CHECK-MAINLINE-07B]
- Owner: CHECK-MAINLINE-07B, MAINLINE-007B, MAINLINE-009. State: assumption.
- Check: raised by CHECK-MAINLINE-07B.
- Ids: MAINLINE-07B NFI-BIAX; MAINLINE-009 NFI-WRINKLE-BIAX; CHECK-MAINLINE-07B NFI-BIAX

**R010. honeycomb wrinkling coefficient 0.33 (design) vs 0.82 (theoretical) (O2)**
- Unknown: Foam wrinkling gives 0.709 of advisory uniaxial SF; Hexcel honeycomb wrinkling (0.0565, 0.0415) falls below general instability and would govern if admitted; Plascore Ec open, Hexcel stabilised Ec questionable.
- Today: design coefficients 0.50 and 0.33; classical 0.76 and 0.82 [MAINLINE-013] | coefficient 0.33 (design lower bound) [MAINLINE-021] | coefficient 0.33 (classical 0.82) [MAINLINE-21B] | foam factor 0.6823278 (Q 0.50) [CHECK-MAINLINE-07B]
- Needed or settling test: Correct the sentence [CHECK-MAINLINE-14B] | a representative wrinkling test fixing the coefficient for the chosen face and core [MAINLINE-013] | coefficient 0.3707; a wrinkling test on a representative sandwich [MAINLINE-021] | coefficient 0.6092 [MAINLINE-21B]
- Owner: CHECK-MAINLINE-07B, CHECK-MAINLINE-14B, MAINLINE-013, MAINLINE-014, MAINLINE-017, MAINLINE-021, MAINLINE-021B, MAINLINE-14B. State: assumption, resolved.
- Check: OPEN (O2): no pending card; a wrinkling test on a representative sandwich grounds it.
- Ids: CHECK-MAINLINE-14B NFI-WRINKLE-GC-TEXT; MAINLINE-013 NFI-013-WRINKLE-LEVEL; MAINLINE-021 NFI-021-WRINKLE; MAINLINE-21B NFI-021b-WRINKLE; CHECK-MAINLINE-07B NFI-WRINKLE; MAINLINE-014 NFI-WRINKLE-Q; MAINLINE-14B NFI-WRINKLE-Q; MAINLINE-017 NFI-017-WRINKLE-COEFF

**R011. intracell dimpling: biaxial vs uniaxial rule and coefficient**
- Unknown: Intracell dimpling uses the brief stress 2*E_f/(1-nu^2)*(tf/s_cell)^2 with nominal cell size, no equibiaxial factor; foam is not dimpled; the coefficient 2 is the brief expression.
- Today: dimpling margin 9.019 biaxial vs 18.04 uniaxial [MAINLINE-021] | coefficient 2 (brief expression) [MAINLINE-14B]
- Needed or settling test: none [MAINLINE-021]
- Owner: MAINLINE-021, MAINLINE-14B. State: assumption.
- Check: CORRECTED: rpt-ref-444cea756201354c34c3 and rpt-ref-0d85ae067b41baf8d095 halve dimpling SF for equal-biaxial load; 021 uses the biaxial rule. Never binding.
- Ids: MAINLINE-021 NFI-021-DIMPLING-FORM; MAINLINE-14B NFI-DIMPLE

**R012. laminate bending stiffness in wrinkling**
- Unknown: Composite faces use an inherited scalar quasi-isotropic modulus in the wrinkling formula; laminate bending stiffness (layup) is not supplied.
- Today: Scalar quasi-isotropic face modulus (value not stated) [CHECK-MAINLINE-14B]
- Needed or settling test: Layup / bending-stiffness sensitivity in a later fix card [CHECK-MAINLINE-14B]
- Owner: CHECK-MAINLINE-14B. State: assumption.
- Check: raised by CHECK-MAINLINE-14B.
- Ids: CHECK-MAINLINE-14B NFI-LAMINATE-BENDING


## T05 Face properties

**R013. Be face compressive allowable by grade, form and source: 241 / 255 / 283 / 345 / 379 MPa (O3)**
- Unknown: Face compression is exactly 1 on the SR-200 minimum tensile yield used as compressive; no compressive minimum is published, and gauge tolerance or post-form properties can take it below 1.
- Today: 283 MPa (frozen); current guide about 255 MPa [CHECK-MAINLINE-09C5] | S-200F E 290 GPa, 283 MPa; SR-200 lot 379.2 MPa, E 293.6 GPa; SR-200 tensile minimum 345 MPa [MAINLINE-027] | 283 MPa starting value; current guide about 255 MPa; SR-200 tensile minimum 345 MPa; main route needs about 283 MPa [CHECK-rpt-ref-e92af61311c9bf4a89cd] | 379.2 MPa sheet; tube values 450 and 544 MPa [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Needed or settling test: Pin the exact older edition supporting 283 MPa and reconcile with the newer guide [CHECK-MAINLINE-09C5] | Lot-, gauge-, direction- and post-form compression, stiffness and Poisson data [MAINLINE-027] | Matched product, lot and thickness compression value [CHECK-rpt-ref-e92af61311c9bf4a89cd] | Narrow wording to the strongest applicable sheet value; any tube-to-sheet transfer is a separate PROJECTION [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Owner: CHECK-MAINLINE-09C5, CHECK-MAINLINE-14B, CHECK-rpt-ref-e92af61311c9bf4a89cd, MAINLINE-020, MAINLINE-027, MAINLINE-028. State: assumption, exists_today.
- Check: OBJECTION rpt-ref-e92af61311c9bf4a89cd: the Materion guide gives about 255 MPa; at 255 MPa 021's least set moves to wrinkling plus strength on aramid (crimp-branch gamma 1). 028b runs it.
- Ids: CHECK-MAINLINE-09C5 NFI-STRENGTH-EDITION; CHECK-MAINLINE-14B NFI-STRENGTH-EDITION; MAINLINE-027 NFI-027-BE-GRADE; CHECK-rpt-ref-e92af61311c9bf4a89cd NFI-CHECK021-STRENGTH-FORM; CHECK-rpt-ref-e92af61311c9bf4a89cd NFI-CHECK021-STRONGEST-SCOPE; MAINLINE-020 NFI-020-GRADE-ORIENTATION-COMPRESSION; MAINLINE-021 NFI-021-BE-STRENGTH; MAINLINE-21B NFI-021b-FACE-AT-ONE; MAINLINE-028 NFI-028-19

**R014. CFRP quasi-isotropic face properties (Be-free fallback)**
- Unknown: QI laminate modulus and compressive strength for T700, M55J, K13D2U and boron/epoxy are estimated from UD data with assumed reduction factors, not measured.
- Today: least SF 0.5415 (exact geometry) to 0.6519 (published); relative loss 4.9 to 16.7 percent [MAINLINE-020]
- Needed or settling test: measured QI laminate modulus and compressive strength at intended fibre volume fraction [MAINLINE-008] | I014b QI laminate compression, stiffness, density and manufacturing route [MAINLINE-020]
- Owner: MAINLINE-008, MAINLINE-020. State: assumption.
- Check: source cards checked by rpt-ref-f08b92e3e640a19fb4ea (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-008 NFI-008-QI-LAMINATE; MAINLINE-020 NFI-020-BERYLLIUM-FREE-FALLBACK

**R015. face Poisson ratio (0.33 carried; Be sheet about 0.08)**
- Unknown: Poisson ratio in buckling and foam-wrinkling formulas is carried from the 6061 case; no SiC value was given. Buckling pressure scales as 1/sqrt(1-nu^2).
- Today: nu 0.33 (carried from 6061) [MAINLINE-009] | nu 0.33 (card); nu12 0.0768, nu21 0.0752 (orthotropic lot) [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Needed or settling test: Face sheet's own Poisson ratio [MAINLINE-009] | Coherent measured in-plane elastic tuple and an orthotropic model, or a tagged isotropic approximation [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Owner: CHECK-rpt-ref-e92af61311c9bf4a89cd, MAINLINE-009, MAINLINE-014, MAINLINE-14B. State: assumption.
- Check: OBJECTION rpt-ref-e92af61311c9bf4a89cd: Be sheet in-plane nu about 0.076, not 0.33.
- Ids: MAINLINE-009 NFI-NU; CHECK-rpt-ref-e92af61311c9bf4a89cd NFI-CHECK021-POISSON; MAINLINE-014 NFI-NU; MAINLINE-14B NFI-NU

**R016. S-200F modulus is 290 GPa, not the 303 GPa of S-200FH**
- Unknown: Comparisons retain 303 GPa, 283 MPa compression and nu 0.33 although the current forms sheet gives 290 GPa for S200F and 303 for S200FH; compression basis to reconcile.
- Today: E = 303 GPa as reported (source says 290 GPa) [CHECK-MAINLINE-09C5] | E = 303 GPa (card); 290 GPa (checker) [CHECK-MAINLINE-013] | E 303 GPa; compression 283 MPa; nu 0.33 (290 GPa sensitivity supplied) [MAINLINE-019] | E 303 GPa (card); 290 GPa (datasheet); sheet full-gamma SF 0.942 at same geometry [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Needed or settling test: Grade-specific 290 GPa, or an explicitly sourced 303 GPa scenario [CHECK-MAINLINE-09C5] | Use 290 GPa for the named grade and update the projection, or source and label S200FH [CHECK-MAINLINE-013] | Reconcile exact grade, compression basis and Poisson ratio; no tensile substitution [MAINLINE-019] | Keep E, strength and product form together; reissue claims under the grade correction [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Owner: CHECK-MAINLINE-013, CHECK-MAINLINE-09C5, CHECK-MAINLINE-14B, CHECK-rpt-ref-e92af61311c9bf4a89cd, MAINLINE-019, MAINLINE-021. State: assumption, resolved.
- Check: RESOLVED: corrected by rpt-1228-mainline009c5-independent-check-1019, rpt-1228-mainline014b-independent-check-1019 and rpt-ref-e92af61311c9bf4a89cd; 021 rev1 carries 290 GPa.
- Ids: CHECK-MAINLINE-09C5 NFI-S200F-MODULUS; CHECK-MAINLINE-013 NFI-CHECK013-S200F-GRADE; CHECK-MAINLINE-14B NFI-S200F-MODULUS; MAINLINE-019 NFI-019-MATERIAL-GRADE; CHECK-rpt-ref-e92af61311c9bf4a89cd NFI-CHECK021-MODULUS; MAINLINE-021 NFI-021-FACE-MODULUS

**R017. SiC face properties (009b)**
- Unknown: SiC face compressive strength is taken as 3900 MPa (compression mode) vs 380 MPa flexural; a compressive allowable for the sintered face and a membrane-compression-only check are open.
- Today: 3900 MPa compressive (optimistic); 380 MPa flexural (conservative); SF 0.433 if flexural used [MAINLINE-009] | E 410 GPa, density 3100 kg/m3 [MAINLINE-009]
- Needed or settling test: Compressive allowable for the sintered face; check stress stays membrane compression [MAINLINE-009] | Batch modulus and density for the actual face sheet [MAINLINE-009]
- Owner: MAINLINE-009. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-009 NFI-FACE-STRENGTH; MAINLINE-009 NFI-FACE-MODULUS


## T06 Face sheet and panels

**R018. Be thin-sheet panel size and gauge: 0.914 m square-equivalent stock today, 3.13 to 4 m assumed (O4)**
- Unknown: Severe-budget faces are far below supplier stock gauge; stock for the large panel begins at 0.059 in and the enhanced aluminium face at R=20 is thinner. Small panel size assumed.
- Today: 18 m equivalent widths required [MAINLINE-019] | Be faces about 0.056-0.057 mm; core 6.8-8.3 mm [MAINLINE-019] | stock begins 0.059 in (1.4986 mm); enhanced Al face 1.423 mm at R=20; panel 0.6096 x 1.8288 m [MAINLINE-027] | assumed panels 0.61x1.83 m (optimistic) to 0.30x0.61 m; source gauge tolerance 0.1016 mm [MAINLINE-020]
- Needed or settling test: Manufacturer grade, size, forming route, gauge tolerance and yield quote; spherical seam-layout takeoff [MAINLINE-019] | Local geometry, imperfections, seam load transfer and nonlinear validation [MAINLINE-019] | Supplier confirmation of dimensions at each minimum gauge, shaping yield, thickness distribution [MAINLINE-027] | supplier-confirmed grade, gauge, size, flatness; formed-panel gauge map and curvature survey [MAINLINE-020]
- Owner: MAINLINE-019, MAINLINE-020, MAINLINE-027, MAINLINE-028. State: PROJECTION, assumption, unknown.
- Check: OPEN (O4): 020 finds 0.61 x 1.83 m the largest stock (>= 0.059 in), thin unknown.
- Ids: MAINLINE-019 NFI-019-PANELS; MAINLINE-019 NFI-019-GEOMETRY-MODES; MAINLINE-027 NFI-027-PANEL-GAUGE; MAINLINE-020 NFI-020-THIN-SHEET-GEOMETRY; MAINLINE-021 NFI-021-SHEET-SIZE; MAINLINE-21B NFI-021b-PANEL; MAINLINE-028 NFI-028-14; MAINLINE-028 NFI-028-15


## T07 Cores

**R019. core crush criterion (crush strength against p/2)**
- Unknown: Hexcel CR-III crush column is used; HFT and HRH-49 have no crush column so stabilised compressive strength is used; thickness does not enter; target is p/2.
- Today: catalog compressive strengths at 16-38 kg/m3 clear p/2 by about 7 to 27 times [MAINLINE-007] | core stress p/2 [MAINLINE-009] | core stress factor 1/2 of p (brief example, no pinned reference) [MAINLINE-05B] | required core strength 47730.4 Pa on every row [MAINLINE-013]
- Needed or settling test: A sourced crush model [MAINLINE-007] | Core stress from face-to-face load path including local bending [MAINLINE-009] | pinned sandwich core-crush reference and re-derived factor [MAINLINE-05B] | apply p/2 at 007's external pressure when it lands [MAINLINE-05B]
- Owner: MAINLINE-003, MAINLINE-004, MAINLINE-005B, MAINLINE-007, MAINLINE-009, MAINLINE-013, MAINLINE-014, MAINLINE-14B. State: assumption, unknown.
- Check: source cards checked by rpt-1228-mainline013-independent-check-1020 (admitted_with_defects), rpt-ref-650cc5448a49ba2d595f (reproduced), rpt-mainline007-check-lead4f19-1019 (reproduced); no objection on this row.
- Ids: MAINLINE-007 NFI-CRUSH; MAINLINE-009 NFI-CRUSH-MODEL; MAINLINE-05B NFI-005B-MODEL; MAINLINE-05B NFI-005B-007; MAINLINE-013 NFI-013-CRUSH-MODEL; MAINLINE-003 NFI-CRUSH; MAINLINE-004 NFI-CRUSH; MAINLINE-014 NFI-CRUSH; MAINLINE-14B NFI-CRUSH-COLUMN

**R020. core shear strength is not a scored mode**
- Unknown: L and W plate-shear strengths are stored, but the crimp mode scores shear modulus and shear strength is not a separate mode.
- Owner: MAINLINE-14B. State: assumption.
- Check: source cards checked by rpt-1228-mainline014b-independent-check-1019 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-14B NFI-SHEAR-STRENGTH

**R021. foam core allowables (crush strain, creep, design values)**
- Unknown: H35 properties are typical or nominal, not allowables; rev9 prints a minimum compressive strength of 0.3 MPa vs 0.5 MPa nominal used (factor 1.67).
- Today: density 38 kg/m3; Ec 40 MPa; Gc 12 MPa; compressive 0.5 MPa nominal (0.3 MPa minimum) [MAINLINE-009] | incumbent 16 kg/m3 passes on one strain definition, fails on the other; lowest passing density between about 11 and 22 kg/m3 [MAINLINE-05B] | 11 kg/m3 lowest passing density, no creep derate [MAINLINE-05B] | EPS12 at 11.2 kg/m3: 15 kPa at 1 percent, 40 kPa at 10 percent [MAINLINE-013]
- Needed or settling test: Design allowables for Ec, Gc and compressive strength at the used thickness [MAINLINE-009] | checker names the governing strain definition [MAINLINE-05B] | sustained-load derate of foam allowables before relying on densities near 11 kg/m3 [MAINLINE-05B] | one strain definition and a measured value [MAINLINE-013]
- Owner: MAINLINE-005B, MAINLINE-009, MAINLINE-013. State: assumption, unknown.
- Check: source cards checked by rpt-ref-40cc094053ddae09d5ac (admitted_with_defects), rpt-1228-mainline013-independent-check-1020 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-009 NFI-CORE; MAINLINE-05B NFI-005B-STRAIN; MAINLINE-05B NFI-005B-CREEP; MAINLINE-013 NFI-013-EPS-DEFINITIONS

**R022. honeycomb datasheet values and conversions (W vs L shear, typical vs minimum, density)**
- Unknown: Datasheets print conflicting values: Plascore 5052 gives 100 psi and 0.55 MPa in one cell; Divinycell H35 0.45 MPa (rev7) vs 0.50 MPa (rev9). Crush margins still clear.
- Today: 100 psi vs 0.55 MPa; H35 0.45 vs 0.50 MPa [MAINLINE-007] | Hexcel test thickness 0.625 inch vs 20 mm core [MAINLINE-021] | 16 kg/m3 [rpt-mainline-grok-estimates-card-1019] | 14.3 ksi used (brochure 13.3 ksi) [MAINLINE-14B]
- Needed or settling test: Keep both readings; resolve revision [MAINLINE-007] | Pin a honeycomb or foam sheet at the thickness used. [rpt-mainline-grok-estimates-card-1019] | Stabilised Ec and L/W shear moduli in the band. [MAINLINE-14B]
- Owner: MAINLINE-007, MAINLINE-021, MAINLINE-14B, rpt-mainline-grok-estimates-card-1019. State: assumption, exists_today, unknown.
- Check: source cards checked by rpt-1228-mainline013-independent-check-1020 (admitted_with_defects), rpt-ref-650cc5448a49ba2d595f (reproduced), rpt-mainline007-check-lead4f19-1019 (reproduced); no objection on this row.
- Ids: MAINLINE-007 NFI-DATASHEET; MAINLINE-021 NFI-021-CORE-TABLE; rpt-mainline-grok-estimates-card-1019 NFI-CORE; MAINLINE-14B NFI-W-SHEAR; MAINLINE-14B NFI-W-13-3; MAINLINE-14B NFI-DENSITY; MAINLINE-14B NFI-CARBON

**R023. thick curved honeycomb core validation**
- Unknown: Core data are catalogue typical rows tested at 15.875 mm depth, while optimised cores reach about 120-144 mm; Ec transferred from another maker and bare compression substituted for crush.
- Today: test depth 15.875 mm vs 120-144 mm needed at R=50 [MAINLINE-027]
- Needed or settling test: Validation of thick curved honeycomb: skin restraint, orthotropy, depth effects, crush definition [MAINLINE-027]
- Owner: MAINLINE-027. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-027 NFI-027-CORE-TRANSFER

**R024. ultralight cores below about 16 kg/m3: no sourced material; scaled moduli are PROJECTION**
- Unknown: No measured shear modulus at or below 10 kg/m3; G=E/2 is an assumption; figure reads, bulk-scale transfer and continuum validity unproved; 190 kg/m3 row passes locally only.
- Today: Basotect crush above 9000 Pa, no upper bound; EPS12 minimum 15000 Pa at 1% strain, density minimum 11.2 kg/m3 [CHECK-MAINLINE-013] | named-set high SF 0.737 at 1 kg/m3; buckling SF reaches 1 at 3.73 kg/m3 [MAINLINE-007] | density at or above 0.9 kg/m3 [MAINLINE-007] | lightest sourced catalog core 16 kg/m3 (ROHACELL 31, HexWeb 24); microlattice at 0.9 kg/m3 has no modulus or strength [MAINLINE-08B]
- Needed or settling test: Measured crush, Ec and G of the actual material; keep comparison operators and property basis [CHECK-MAINLINE-013] | Measured properties at the claimed density before any new material claim; keep PROJECTION tag on ideal-lattice uses [CHECK-MAINLINE-013] | A sourced structural core at low density [MAINLINE-007] | Sourced Gc, Ec and crush strength at those densities [MAINLINE-007]
- Owner: CHECK-MAINLINE-007, CHECK-MAINLINE-013, CHECK-MAINLINE-07B, MAINLINE-003, MAINLINE-004, MAINLINE-007, MAINLINE-007B, MAINLINE-008B, MAINLINE-013, MAINLINE-014, MAINLINE-14B. State: PROJECTION, assumption, unknown.
- Check: raised by CHECK-MAINLINE-007, CHECK-MAINLINE-013, CHECK-MAINLINE-07B.
- Ids: CHECK-MAINLINE-013 NFI-CHECK013-LOWER-BOUNDS; CHECK-MAINLINE-013 NFI-CHECK013-INHERITED-LIMITS; MAINLINE-007 NFI-DENSITY; MAINLINE-007 NFI-CORE-FLOOR; MAINLINE-007 NFI-MICROLATTICE; MAINLINE-07B NFI-CORE-FLOOR; MAINLINE-08B NFI-008B-CORE-NONE-LIGHT; MAINLINE-013 NFI-013-WRINKLE-PRODUCT; MAINLINE-013 NFI-013-SHEAR-UNMEASURED; MAINLINE-013 NFI-013-CRIMP; MAINLINE-013 NFI-013-STRENGTH-BASIS; MAINLINE-013 NFI-013-MID-DENSITY; MAINLINE-013 NFI-013-CONTINUUM-AND-DIMPLING; MAINLINE-013 NFI-013-HONEYCOMB-FORM; MAINLINE-013 NFI-013-IDEAL-LATTICE; MAINLINE-013 NFI-013-SCALE-AND-ENVIRONMENT; MAINLINE-003 NFI-DENSITY; MAINLINE-004 NFI-DENSITY; CHECK-MAINLINE-007 NFI-DENSITY; CHECK-MAINLINE-07B NFI-CORE-FLOOR; MAINLINE-014 NFI-SCALE; MAINLINE-014 NFI-013; MAINLINE-14B NFI-SCALE; MAINLINE-14B NFI-013


## T08 P2 joints, seams and film

**R025. 30:1 adhesive scarf seam**
- Unknown: Thin Be/Be scarf performance is untested; the 10 MPa shear screen is selected, not qualified.
- Today: 25.303 mm run; 9.421 MPa average shear; 0.01060 kg/m seam [MAINLINE-028]
- Needed or settling test: thin Be/Be scarf compression, biaxial transfer, peel and cyclic data at actual film weight [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-07

**R026. adhesive-free diffusion interface**
- Unknown: Zero added filler is an ideal limit; the replacement core density and strength are unknown.
- Today: 0 added filler (ideal limit) [MAINLINE-028]
- Needed or settling test: complete installed bill and measured structure: core density, stiffness, strength, process pressure [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-06

**R027. bond film areal weight and coverage (0.015 to 0.060 lb/ft2)**
- Unknown: Matching Be/core strength and stiffness at the lowest-weight reticulated film weight are unmeasured; hull adoption is a projection.
- Today: 0.03 lb/ft2 (full optimism 0.015 lb/ft2) [MAINLINE-21B] | AF163-2U 73.236 g/m2 exists; budget maximum 74.107 g/m2 [MAINLINE-028] | manufacturer tolerance +/-0.005 lb/ft2; upper-weight joining 275.6 kg vs 216.4 kg allowance [MAINLINE-028] | HexBond312 70 g/m2 lap shear 37 MPa on Al; 100 g/m2 5.4 MPa on a different sandwich [MAINLINE-028]
- Needed or settling test: 0.03 lb/ft2 at the floating point [MAINLINE-21B] | weigh installed cured film; Be/core strength, stiffness and defects at that weight [MAINLINE-028] | lot areal-mass distribution and cured retained mass [MAINLINE-028] | test of the actual assembly [MAINLINE-028]
- Owner: MAINLINE-021B, MAINLINE-028. State: assumption, exists_today.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-21B NFI-021b-FILM; MAINLINE-028 NFI-028-01; MAINLINE-028 NFI-028-02; MAINLINE-028 NFI-028-03

**R028. brazed scarf seam**
- Unknown: Al-Si braze shear is a typical value, not an allowable; thin-sheet joint distribution, fatigue and distortion unknown.
- Today: Al-Si typical shear 103.4 MPa vs 84.884 MPa needed; 50 um filler gap [MAINLINE-028]
- Needed or settling test: thin-sheet joint distribution, compressive/peel fatigue, distortion, closure sequence [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-09

**R029. butt-strap seam route**
- Unknown: Butt-strap bending, peel and strip buckling are unmeasured; this route is 2.88x over the joining allowance.
- Today: 47.730 mm strap width per face; 0.162691 kg/m; 623.1 kg [MAINLINE-028]
- Needed or settling test: measured local bending and peel, strip buckling, or a symmetric alternative [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-08

**R030. core splice allowance**
- Unknown: Installed core splice mass and its ability to transmit core shear are unknown.
- Today: selected 0.5 mm gap and 500 kg/m3 cured filling; 0.00505 kg/m [MAINLINE-028]
- Needed or settling test: weighed edge splice transmitting core shear with real gaps and nodes [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-11

**R031. core-to-face brazing route**
- Unknown: No structural data for brazing a Be face to the selected 16 kg/m3 Al core exist; coated CRIII properties may not carry over.
- Today: generic Be brazing exists; filler 5.67-22.68 g/m2 geometric [MAINLINE-028]
- Needed or settling test: wetting, residual stress and bare-core condition after joining qualified [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-05

**R032. electron-beam seam retention**
- Unknown: Thin-sheet Be EB seam compression retention is unknown; 100 percent retention is a projection and 80 percent a sensitivity.
- Today: Be EB process exists; SF 0.853 at assumed 80 percent retention [MAINLINE-028]
- Needed or settling test: retention 0.9998 at original gauge; weld/HAZ compression, ductility, penetration, leak integrity [MAINLINE-028]
- Owner: MAINLINE-028. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-10

**R033. P2 seam and bond mass and capacity on the hull (016, 019, 020, 021b, 027, 028)**
- Unknown: Net-section efficiencies are assumed screens applied only to compression; the enhanced aluminium optimum is joint-limited and no joint buckling, shear or peel allowables exist.
- Today: today's 0.5 m Hexoloy plate gives 330-694% of the 216.427 kg allowance [MAINLINE-016] | film use .015/.030 lb/ft2 (.015 mass-lower choice) [MAINLINE-019] | efficiencies 0.9 / 0.6 (assumed) [MAINLINE-027] | joining 968.2 kg optimistic (eta 0.9) to 3722.0 kg conservative (eta 0.6); payload -507 to -3261 kg [MAINLINE-020]
- Needed or settling test: Real maximum plate size and a seam parts list for a named panel size, or a face family with 2-4 m sheets [MAINLINE-016] | Test a complete seam and bond architecture for installed mass, leak rate and stiffness [MAINLINE-019] | Weigh and load-test a curved two-skin splice; seam parameters versus thickness [MAINLINE-027] | Measured seam biaxial compression, eccentricity and failure envelope [MAINLINE-027]
- Owner: MAINLINE-016, MAINLINE-019, MAINLINE-020, MAINLINE-021B, MAINLINE-027, MAINLINE-028. State: PROJECTION, assumption, unknown.
- Check: OPEN: 028 prices a stock-envelope bill at 214.24 kg against the 216.43 kg allowance (scarfs, nominal film); 020's optimistic 968 kg used heavier film and doublers; 028b runs it into 021b.
- Ids: MAINLINE-016 NFI-016-SEAM; MAINLINE-019 NFI-019-JOINTS; MAINLINE-027 NFI-027-SEAM-SCALING; MAINLINE-027 NFI-027-JOINT-STRENGTH; MAINLINE-020 NFI-020-JOINT-MASS-CAPACITY; MAINLINE-21B NFI-021b-JOINT-PARAMETERS; MAINLINE-028 NFI-028-17

**R034. primer and surface prep mass**
- Unknown: Be-compatible primer and surface preparation mass is not counted; zero is only a bookkeeping limit.
- Today: zero primer; 5 g/m2 per line as sensitivity (12.57 kg) [MAINLINE-028]
- Needed or settling test: qualified Be-compatible preparation weighed including core-side coverage [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-13

**R035. seam step effect on kd**
- Unknown: A seam step is counted only as delta/t_eq; a real seam also breaks face continuity, and no joint failure model exists.
- Today: kd 0.950, 0.931, 0.869 at steps of 1, 3, 10 mm on P2-E [MAINLINE-015]
- Needed or settling test: a joint model with the sandwich failure cards [MAINLINE-015]
- Owner: MAINLINE-015. State: assumption.
- Check: source cards checked by rpt-ref-88e650e7f8b713866e0b (partial); no objection on this row.
- Ids: MAINLINE-015 NFI-015-SEAM-DISCONTINUITY

**R036. selective cell-edge adhesive deposition**
- Unknown: Selective cell-edge deposition is lab-only on CFRP/Nomex and not shown on Be/Al.
- Today: 8-80 g/m2 deposited in CFRP/Nomex experiments [MAINLINE-028]
- Needed or settling test: coverage, fillets, cured mass and mechanical performance after transfer to Be/Al [MAINLINE-028]
- Owner: MAINLINE-028. State: in_lab.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-04

**R037. spherical layout and scarf edges**
- Unknown: No polar-cap or intersection design; the mean-field rectangular layout ignores tessellation, tolerances and rejects.
- Today: mean-field layout with scarf overlap deducted; spare 2.19 kg [MAINLINE-028]
- Needed or settling test: finished spherical tessellation with fit tolerances, waviness and installation rejects [MAINLINE-028]
- Owner: MAINLINE-028. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-028 NFI-028-16


## T09 Margin items

**R038. 019's optimistic reserve embeds 4 m panels and 0.015 lb/ft2 film**
- Unknown: The 019 reserve of 535.95 kg embeds 4 m panels and 0.015 lb/ft2 film; at today panel and film the reserve is larger.
- Today: reserve 1229.4 kg at today panel and film [MAINLINE-21B]
- Owner: MAINLINE-021B. State: assumption.
- Check: CONFIRMED by arithmetic: 021b states it (1229 kg at its point); this checker's unfiled 020 check re-solved 019's own families at 1154.23 kg, matching 021b's 1154 kg aluminium row.
- Ids: MAINLINE-21B NFI-021b-RESERVE-HIDES-OPTIMISMS

**R039. design-day climate envelope for lift (site, temperature, pressure, humidity)**
- Unknown: Lift depends on site temperature and pressure; no site is named so the 5% margin has no climate envelope. Hot afternoon and retained water each consume the margin.
- Today: +25.1 K gives margin -186.3 kg; 0.1 mm retained water 125.6 kg [MAINLINE-016] | optimistic +10 K, +/-1%, 1000 Pa vapour; conservative +25.1 K, +/-2%, 6000 Pa [MAINLINE-027] | optimistic day: 0.1 mm water, +10 K, 1 percent, 1 kPa; conservative needs 4229 kg [MAINLINE-21B]
- Needed or settling test: Named site and season windows; ballast or trim sizing; coating and shedding check [MAINLINE-016] | Station data and operating constraints; recompute mass and max differential-pressure cases [MAINLINE-019] | Site, gas composition, temperatures, weather exposure, water shedding/icing, duration [MAINLINE-027] | site and gas-load measurement (019 follow-ups) [MAINLINE-21B]
- Owner: MAINLINE-016, MAINLINE-019, MAINLINE-027. State: assumption, unknown.
- Check: source cards checked by rpt-ref-e5b19d75c664308465ef (admitted_with_defects), rpt-check019-opus-1020 (objection); no objection on this row.
- Ids: MAINLINE-016 NFI-016-CLIMATE; MAINLINE-019 NFI-019-SITE; MAINLINE-027 NFI-027-ENVIRONMENT; MAINLINE-21B NFI-021b-CLIMATE-SERVICE

**R040. float margin and payload: 0%, 5%, 10.96% and 86.49% budgets**
- Unknown: Reserve is the explicit charge above baseline floors, not statistical contingency or free payload; climate plus internal air alone exceeds a 5% margin and larger radius alone cannot fix it.
- Today: payload reserve 5% of lift; total mass 95% of lift [CHECK-MAINLINE-09C5] | 5% main and conservative; 0% optimistic [MAINLINE-009] | payload 0 kg; +100 kg case supplied [MAINLINE-019] | climate plus internal air alone: 5.7396% optimistic, 13.1183% conservative [MAINLINE-027]
- Needed or settling test: Reword to state payload 5% and total mass 95% [CHECK-MAINLINE-09C5] | Newer equal-margin geometry input [MAINLINE-009] | Set payload and float reserve separately [MAINLINE-019] | Specified residual reserve added to the budget [MAINLINE-019]
- Owner: CHECK-MAINLINE-09C5, MAINLINE-009, MAINLINE-019, MAINLINE-021B, MAINLINE-027. State: assumption, exists_today, unknown.
- Check: raised by CHECK-MAINLINE-09C5.
- Ids: CHECK-MAINLINE-09C5 NFI-PAYLOAD-SENTENCE; MAINLINE-009 NFI-MASS; MAINLINE-019 NFI-019-PAYLOAD; MAINLINE-019 NFI-019-RESERVE; MAINLINE-027 NFI-027-RESERVE-MEANING; MAINLINE-021 NFI-021-MARGIN; MAINLINE-21B NFI-021b-MARGIN

**R041. retained water and contamination**
- Unknown: Water films are equivalent retained thickness, not rainfall; absorbed core moisture, corrosion, thermal gradients and derating are unquantified; 320 K gas temperature is an acceptance condition.
- Today: gas temperature at most 320 K (acceptance condition) [MAINLINE-019]
- Needed or settling test: Measured water shedding, conditioning, absorbed moisture and thermal response [MAINLINE-019] | Exterior humidity case and hull water rate [MAINLINE-024]
- Owner: MAINLINE-019, MAINLINE-024. State: unknown.
- Check: source cards checked by rpt-check019-opus-1020 (objection); no objection on this row.
- Ids: MAINLINE-019 NFI-019-ENVIRONMENT; MAINLINE-024 NFI-HULL-HUMIDITY

**R042. systems and allowance masses are owner allowances (100 kg P2, 50 kg P3, pump, battery)**
- Unknown: Battery estimate assumes packaged energy density, usable fraction and conversion; catalog pump data are not installed duty measurements and the smaller pump misses the hot-gas flow.
- Today: joint fraction 5%; systems 100 kg; residual gas zero [MAINLINE-007] | 150 Wh/kg packaged, 80% usable, 90% conversion [MAINLINE-019] | optimistic case retains 70 kg unused system allowance [MAINLINE-019] | 100 kg system floor (70 kg above passive package); 0.1 kg/m2 sensitivity [MAINLINE-027]
- Needed or settling test: A parts list [MAINLINE-007] | Measured pump curve, power, cooling, conductance and duty cycle; qualified power package [MAINLINE-019] | Explicit allocation of each needed item [MAINLINE-019] | Itemised additional vehicle masses [MAINLINE-027]
- Owner: MAINLINE-002, MAINLINE-003, MAINLINE-007, MAINLINE-010, MAINLINE-019, MAINLINE-027, rpt-mainline-grok-estimates-card-1019. State: assumption, unknown.
- Check: source cards checked by rpt-1228-mainline013-independent-check-1020 (admitted_with_defects), rpt-ref-650cc5448a49ba2d595f (reproduced), rpt-mainline007-check-lead4f19-1019 (reproduced); no objection on this row.
- Ids: MAINLINE-007 NFI-MASS; MAINLINE-019 NFI-019-SYSTEMS; MAINLINE-019 NFI-019-OTHER-MASS; MAINLINE-027 NFI-027-OTHER-MASS; MAINLINE-010 NFI-010-SYSTEMS; rpt-mainline-grok-estimates-card-1019 NFI-MASS; MAINLINE-002 NFI-MASS; MAINLINE-003 NFI-MASS


## T10 Vacuum holding

**R043. getter capacity nitrogen air**
- Unknown: SAES offers room-temperature nitrogen sorption, so the blanket denial and unsourced N2 capacity band cannot support the mass result; all-air getter lifetime incl. noble gases is unsized.
- Today: pump band 150-400 kg (catalog class) [MAINLINE-024]
- Needed or settling test: Measured species loads, sorption speeds and capacities with activation conditions [MAINLINE-019] | Getter capacity against gas load [MAINLINE-024]
- Owner: MAINLINE-019, MAINLINE-024. State: unknown.
- Check: source cards checked by rpt-check019-opus-1020 (objection); no objection on this row.
- Ids: MAINLINE-019 NFI-019-GETTERS; MAINLINE-024 NFI-GETTER

**R044. vacuum-holding route mass and power (sealed service vs onboard pump)**
- Unknown: Holding internal pressure at a 1000 Pa ceiling needs a pump whose mass and power are uncertain and can exceed the float margin; the ceiling itself is an owner assumption.
- Today: 46.3 L/s; 527-844 W; 150-400 kg pump set; commissioning pump-down 506 kWh [MAINLINE-016] | pumps needed 1,3,7,23,103 at R 10,15,20,30,50 m [MAINLINE-027] | 30 kg fixed [MAINLINE-027] | perfect vacuum (zero residual) assumed [rpt-mainline-grok-estimates-card-1019]
- Needed or settling test: Real Roots or screw pump spec at this duty; operational ceiling set from leak budget [MAINLINE-016] | Measured leak/outgas and installed speed at pressure; measured gas-load decomposition [MAINLINE-027] | 24 h hold demonstration at temperature envelope; supporting hardware mass [MAINLINE-027] | State a hold pressure and the pump mass. [rpt-mainline-grok-estimates-card-1019]
- Owner: MAINLINE-016, MAINLINE-027, rpt-mainline-grok-estimates-card-1019. State: PROJECTION, assumption.
- Check: source cards checked by rpt-ref-e5b19d75c664308465ef (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-016 NFI-016-PUMP; MAINLINE-027 NFI-027-PUMP-SCALE; MAINLINE-027 NFI-027-PASSIVE-SERVICE; rpt-mainline-grok-estimates-card-1019 NFI-GAS

**R045. whole-hull gas load: leaks, permeation, outgassing (needs measurement)**
- Unknown: Face permeation is negligible at the present budget; CFRP figure comes from a helium band divided by 50 for air and no measured air permeance exists.
- Today: 0.5-3% moisture = 11.0-66.2 kg water = 347-2079 Pa vs 954.6 Pa ceiling [MAINLINE-016] | budget equals 2.48 mm2 choked hole or 4.25 mm2 molecular aperture; 46.28 Pa m3/s [MAINLINE-016] | CFRP 5.4e-5 percent of the 1%/day budget [MAINLINE-016] | 30-50 kg passive package (estimate) [MAINLINE-019]
- Needed or settling test: Water content of the core lot; bake-out and dry-gas backfill procedure [MAINLINE-016] | Operational leak spec with margin; per-panel seam leak testing; sensitive pressure sensor [MAINLINE-016] | Measured air permeance of the chosen face and seam coupon [MAINLINE-016] | Measure gas load through a representative panel/valve assembly then the hull; Qref at most 40.71949 Pa m3/s for 24 h from 10 Pa [MAINLINE-019]
- Owner: MAINLINE-016, MAINLINE-019, MAINLINE-028. State: PROJECTION, assumption, unknown.
- Check: source cards checked by rpt-ref-e5b19d75c664308465ef (admitted_with_defects), rpt-check019-opus-1020 (objection); no objection on this row.
- Ids: MAINLINE-016 NFI-016-BAKEOUT; MAINLINE-016 NFI-016-LEAKSPEC; MAINLINE-016 NFI-016-PERM; MAINLINE-019 NFI-019-LEAK; MAINLINE-028 NFI-028-12


## T11 Thermal

**R046. ground-side thermal environment**
- Unknown: Thermal balance averages sky and ground radiation; a hot apron, heat island or hangar is not bounded and the core-limit conclusion could invert.
- Today: no-convection bound 313.5 K vs H35 limit 343-353 K [MAINLINE-016]
- Needed or settling test: Re-run for named ground conditions; measure emissivity of the face finish [MAINLINE-016]
- Owner: MAINLINE-016. State: assumption.
- Check: source cards checked by rpt-ref-e5b19d75c664308465ef (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-016 NFI-016-THERMENV

**R047. thermal mismatch, cycling and fatigue of bonded faces and joints**
- Unknown: Property loss at temperature is datasheet-class only; no derate curves pinned and daily-cycle fatigue of core and adhesive is unquantified.
- Today: SiC 4.5e-6 vs PVC 60e-6 per K; shear 283 kPa per 30 K; SF 1.41-1.94 at 30 K, 0.71-0.97 at 60 K [MAINLINE-016] | scored modes use room-temperature properties; H35 derates above 50-60 C [MAINLINE-016]
- Needed or settling test: Bond-line and core shear coupon under daily thermal cycling; pinned H35 shear strength and modulus [MAINLINE-016] | Derate curves for core and adhesive against the measured daily band [MAINLINE-016] | effective CTE, temperature histories, restraint and fatigue under compressive mean load; test 10,958 daily cycles for 30 years [MAINLINE-020] | CTE residual stress, polymer heat exposure, corrosion, fatigue, final weld/braze access [MAINLINE-028]
- Owner: MAINLINE-016, MAINLINE-020, MAINLINE-028. State: assumption, unknown.
- Check: source cards checked by rpt-ref-e5b19d75c664308465ef (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-016 NFI-016-CTE; MAINLINE-016 NFI-016-PROPTEMP; MAINLINE-020 NFI-020-THERMAL-FATIGUE; MAINLINE-028 NFI-028-18


## T12 Handling, cost and supply

**R048. Be cost, supply and controlled processing**
- Unknown: Finished-sheet capacity, current S200F/SR200 prices and fabrication yields are unknown; the multipliers are owner stress cases.
- Today: assumed S200F 4800-9600 USD/kg, SR200 9600-24000 USD/kg, yield 0.85-0.5 [MAINLINE-020] | owner allowance 10 to 30 percent of conversion cost [MAINLINE-020]
- Needed or settling test: grade/gauge/size-specific quotes, lead time, rolling capacity, scrap recovery, panel yield [MAINLINE-020] | contractor quote pricing the conversion and capital separately [MAINLINE-020]
- Owner: MAINLINE-020. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-020 NFI-020-SUPPLY-QUOTE-YIELD; MAINLINE-020 NFI-020-CONTROLLED-PROCESS-COST

**R049. brittle face buildability SiC Be**
- Unknown: SiC and beryllium rank only on compressive membrane modes; flexure, fracture toughness, toxicity, joining and ductility are outside the formulas.
- Today: SiC flexural strength about 380 MPa [MAINLINE-008]
- Needed or settling test: fracture and joining assessment before either is carried as a face [MAINLINE-008]
- Owner: MAINLINE-008. State: unknown.
- Check: source cards checked by rpt-ref-f08b92e3e640a19fb4ea (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-008 NFI-008-BRITTLE-FACES

**R050. ground handling and dent survey**
- Unknown: Growth of diameter from 20 to 100 m raises ground area and wind force 25-fold and overturning moment 125-fold; point attachments, transport, launch and landing fall outside uniform-pressure modes.
- Today: core-safe pad pressure target 250 kPa or less; hull 4645 kg [MAINLINE-016] | diameter 20 to 100 m; wind force x25; overturning moment x125 [MAINLINE-027]
- Needed or settling test: Cradle geometry, pad pressure and post-move imperfection survey [MAINLINE-016] | Design and weigh handling and anchoring equipment; verify concentrated and asymmetric loads [MAINLINE-027]
- Owner: MAINLINE-016, MAINLINE-027. State: PROJECTION, unknown.
- Check: source cards checked by rpt-ref-e5b19d75c664308465ef (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-016 NFI-016-HANDLE; MAINLINE-027 NFI-027-HANDLING


## T13 P3 member force

**R051. P3 member force: pRs/(2*sqrt3) on the equilateral frame (FIX-A), two-way 2V-4 members**
- Unknown: P3 assumes tributary width equals spacing, pinned members, a real-valued equal triangulation, and ignores tube crippling; Euler pressure scales with I, E and 1/s^3.
- Today: N = pRs/2; member-end load 974 kN at s 2.04 m (statics: 562 kN) [CHECK-011b] | equilateral N = 562166 N at s 2.04 m (two-way 973701 N) [MAINLINE-023]
- Needed or settling test: N = pRs/(2*sqrt3) on the equilateral frame, or a true two-way frame, then re-optimise [CHECK-011b] | none; 022b rescales [MAINLINE-023] | Integer geodesic, end fixity, imperfection knockdown and local crippling. [rpt-mainline-grok-estimates-card-1019] | Integer mesh, end fixity and crippling. [MAINLINE-002]
- Owner: CHECK-011b, MAINLINE-002, MAINLINE-023, rpt-mainline-grok-estimates-card-1019. State: assumption, resolved.
- Check: RESOLVED, demonstrated: rpt-check011b-opus-1020 (FIX-A; virial identity, geodesic truss solves); adopted by 022b, 023 (562 kN) and 025 (0.82 GPa demand).
- Ids: CHECK-011b NFI-CHK011B-FORCE; MAINLINE-023 NFI-023-EQUILIBRIUM-FORCE; rpt-mainline-grok-estimates-card-1019 NFI-FRAME; MAINLINE-002 NFI-FRAME

**R052. P3 member shape: arcs vs straight chords, arc length**
- Unknown: Members are scored as spherical arcs with N=p*R*s/2; straight chords would give sag 0.1125 m and bending stress 2.1-3.2 GPa, reported outside the least-SF minimiser.
- Today: chord sag 0.1125 m; bending 2.1065-3.1598 GPa [MAINLINE-11B]
- Owner: MAINLINE-11B. State: assumption.
- Check: source cards checked by rpt-check011b-opus-1020 (objection); no objection on this row.
- Ids: MAINLINE-11B NFI-011B-ARC; MAINLINE-11B NFI-011B-LENGTH


## T14 P3 local buckling

**R053. P3 tube local buckling knockdown: SP-8007 gamma (FIX-B)**
- Unknown: Local buckling keeps gamma = 1 at r/t 140.5, while the cited NASA report's curve gives 0.529; local capacity at the SiC point falls to 0.648.
- Today: gamma 1 at r/t 140.5 [CHECK-011b] | gamma = 1 (classical 0.6 E tw/ro) [MAINLINE-011]
- Needed or settling test: gamma 0.529 from the SP-8007 expression, then re-optimise [CHECK-011b] | re-optimise ro under a knocked-down local curve; conclusion survives to gamma about 0.29 [MAINLINE-011]
- Owner: CHECK-011b, MAINLINE-011. State: assumption.
- Check: RESOLVED, demonstrated: rpt-check011b-opus-1020 (FIX-B, gamma 0.529 at r/t 140); adopted by 022b.
- Ids: CHECK-011b NFI-CHK011B-LOCAL-GAMMA; MAINLINE-011 NFI-011-LOCAL-KD


## T15 P3 global lattice

**R054. lattice knockdown k (0.2 floor; Wright 1965's 0.4 and its meaning)**
- Unknown: Wright 1965 modified k 0.4 is applied to this card derived classical pressure, which may not match his Table 2 expression; thickness equation illegible; other sources gave no number.
- Today: k = 0.4 used [CHECK-011b] | k = 0.2 design; 0.5 band top [MAINLINE-11B] | scored 0.2; Wright 0.4 (factor 2.0) [MAINLINE-022]
- Needed or settling test: Wright 1965 Table 2 expression [CHECK-011b] | Legible Wright thickness equation and expression. [MAINLINE-11B]
- Owner: CHECK-011b, MAINLINE-022, MAINLINE-11B. State: assumption, unknown.
- Check: OPEN: 022 judges k 0.2 for ceramic arcs (Wright's 0.4 an optimism of 2); rpt-check011b-opus-1020 notes 0.4 may be a coefficient of E(t/R)^2 (asserted, unverified).
- Ids: CHECK-011b NFI-CHK011B-WRIGHT-K; MAINLINE-11B NFI-011B-WRIGHT; MAINLINE-11B NFI-011B-KNOCKDOWN; MAINLINE-022 NFI-022-KNOCKDOWN

**R055. P3 continuum validity: smeared global mode vs member length (band s <= 3 m; buckle half-wave)**
- Unknown: Optima stay within s<=3 m where 011 judged the equal-triangle continuum defensible; the unconstrained run to s=6.4 m was not repeated.
- Today: optimum cut at s <= 3.0 m (V >= 161 nodes) [MAINLINE-011] | s <= 3 m [MAINLINE-11B]
- Needed or settling test: re-run on real geodesic layouts if a design point is picked [MAINLINE-011]
- Owner: MAINLINE-011, MAINLINE-11B. State: assumption.
- Check: OBJECTION, demonstrated by this card: the smeared buckle half-wave pi*sqrt(1.06*rg*R) is 0.57 of the member at 022b's s 6.15 m and 1.48 at 011b's s 2.04 m (CONTINUUM.json). The global mode does not describe a 40-node frame; a discrete FE decides it.
- Ids: MAINLINE-011 NFI-011-BAND; MAINLINE-11B NFI-011B-BAND

**R056. P3 global lattice mode added and its coefficient (sqrt(3/2), Buchert 1968)**
- Unknown: Scored global pressure uses the equilateral continuum grid (nu 1/3); the brief two-way coefficient 4 is robotics arithmetic and a geodesic coefficient was not invented.
- Today: coefficient 4*sqrt(3/2) on E*sqrt(I*A)/(s*R^2) [MAINLINE-11B] | 009 estimate: about 0.70 perfect, 0.14-0.35 knocked down (6061 optimum) [MAINLINE-017]
- Needed or settling test: equivalent-stiffened-shell general-instability check (ribbed-sphere analogy) [MAINLINE-011] | A geodesic grid coefficient. [MAINLINE-11B] | Score global lattice buckling and member bending (011b) before admitting SiC. [MAINLINE-017]
- Owner: MAINLINE-011, MAINLINE-11B. State: assumption, unknown.
- Check: CONFIRMED: rpt-check011b-opus-1020 re-derived sqrt(3/2) from the lattice sums; Buchert 1968 prints the same thicknesses.
- Ids: MAINLINE-011 NFI-011-GLOBAL; MAINLINE-11B NFI-011B-GRID; MAINLINE-017 NFI-017-P3-MODES

**R057. two-way grid global coefficient 4 assumes isotropy; an unbraced two-way grid has no in-plane shear stiffness (022b's two-way rows rest on it)**
- Unknown: Whether a two-way grid without diagonals has any smeared global buckling capacity near 4*E*sqrt(I*A)/(s*R^2); the lattice sum gives C1212 = 0. 022b's two-way rows (Ti + Kapton 0.986, SiC 1.98) are governed by it.
- Today: C = 4 (isotropic) [CHECK-011b]
- Needed or settling test: a discrete buckling solve of the two-way frame, or diagonals [CHECK-011b]
- Owner: CHECK-011b. State: unknown.
- Check: OBJECTION, demonstrated (lattice sum, C1212 = 0) by rpt-check011b-opus-1020 M4; 022b adopted the 2V-4 count but kept C = 4.
- Ids: CHECK-011b NFI-CHK011B-TEXT


## T16 P3 Perry

**R058. P3 member imperfection: geometric Perry eta, brittle tube**
- Unknown: The P3 pass relies on SiC compression 3900 MPa and a metal-style Perry interaction; a 380 MPa screen gives only about 0.24-0.25. Compressive strength is not a bending allowable.
- Today: 3900 MPa compression; 380 MPa screen gives SF about 0.24-0.25 over 10-50 m [MAINLINE-027] | a0 = s/1000 [MAINLINE-11B]
- Needed or settling test: Brittle tension/compression interaction, statistical size effect and joint eccentricity [MAINLINE-027]
- Owner: MAINLINE-027, MAINLINE-11B. State: PROJECTION, assumption.
- Check: source cards checked by rpt-check011b-opus-1020 (objection); no objection on this row.
- Ids: MAINLINE-027 NFI-027-FRAME-BRITTLE; MAINLINE-11B NFI-011B-PERRY


## T17 P3 tube material

**R059. SiC tube density 3100 vs 3150**
- Unknown: Tube density kept at 3100 kg/m3 though sheet density is 3150; brazed-socket mass about 1.6 percent light.
- Today: 3100 kg/m3 used; sheet 3150 kg/m3 [MAINLINE-023]
- Owner: MAINLINE-023. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-023 NFI-023-DENSITY-3100

**R060. SiC tube design allowable: 3.9 GPa crush vs 380 MPa flexural vs Weibull; demand 0.82 GPa with FIX-A (025)**
- Unknown: SiC and T700 P3 values are 011 equal-mass swap properties from 008; SiC 3900 MPa is compressive, flexural about 380 MPa governs bending; 011 uses compressive sigma for member yield.
- Today: service compression 1.428 GPa; imperfection adds +/-58.8 MPa; no tension [CHECK-011b] | 3900 MPa crush allowable; flexural about 380 MPa [MAINLINE-011] | flexural 380 MPa; compressive 3900 MPa scored; axial stress 824.7 MPa at 562.2 kN [MAINLINE-023] | 3900 MPa crush primary; 380 MPa flexural [MAINLINE-11B]
- Needed or settling test: Compressive design allowable (Weibull treatment) [CHECK-011b] | a buildable-tube demonstration; row to be read as material-boundary only [MAINLINE-011] | allowable owned by MAINLINE-025 [MAINLINE-023] | Score member bending before admitting the SiC direction (011b). [MAINLINE-017]
- Owner: MAINLINE-011, MAINLINE-022, MAINLINE-025, MAINLINE-11B. State: assumption, exists_today, unknown.
- Check: OPEN (025 running): rpt-check011b-opus-1020 shows the arcs stay fully compressed, so the 380 MPa flexural scan is not the arcs' allowable; demand is 0.82 GPa with FIX-A.
- Ids: CHECK-011b NFI-CHK011B-SIC-FIBRE; MAINLINE-011 NFI-011-SIC; MAINLINE-023 NFI-023-FLEXURE-380; MAINLINE-11B NFI-011B-SIC; MAINLINE-017 NFI-017-SIC-SIGMA; MAINLINE-022 NFI-022-SIC-ALLOWABLE; MAINLINE-022 NFI-022-BENDING-CONTACT; MAINLINE-022 NFI-022-DATASHEET-SPREAD

**R061. SiC tube manufacture at hull scale (025)**
- Unknown: P3 needs metre-scale curved thin-walled SiC tubes and a film at 1.5 GPa allowable; the opened supplier example is about 12 in long; not demonstrated products.
- Today: supplier seal tube typically 12 in long [MAINLINE-027] | design OD 281.9 mm, L 0.62 m, wall 0.216 mm; exists: OD 25-381 mm, single piece to 1.4 m, SiSiC wall about 2-4 mm [MAINLINE-022]
- Needed or settling test: Tube and film manufacturing, joints, leaks, defects, proof loads and tolerances [MAINLINE-027]
- Owner: MAINLINE-025, MAINLINE-027. State: PROJECTION.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-027 NFI-027-FRAME-PRODUCT; MAINLINE-022 NFI-022-TUBE


## T18 P3 nodes and joints

**R062. P3 node and joint mass (5% assumed; 023 bill 31 to 859 kg)**
- Unknown: Joints carried at 5 percent (216.4 kg); a SiC pad bearing the member force gives bounds 1938-11620 kg; a 1 MN ceramic load introduction is not a catalog fitting.
- Today: 20 g/node; joints 5% of tube mass [MAINLINE-027] | node hardware 0.02 kg each [MAINLINE-011] | 5 percent of tube mass [MAINLINE-11B] | 216.4 kg allowance; bounds 1937.7-11619.8 kg; member force 295857 N [MAINLINE-022]
- Needed or settling test: Nodes and film attachment sized from load paths [MAINLINE-027] | real geodesic load paths and joint masses [MAINLINE-011] | A measured fitting or parts list. [MAINLINE-11B] | Joint mass owned by MAINLINE-023. [MAINLINE-022]
- Owner: MAINLINE-011, MAINLINE-023, MAINLINE-027, MAINLINE-11B. State: PROJECTION, assumption.
- Check: source cards checked by rpt-ref-3484d24f707ffbfe30ee (admitted_with_defects), rpt-check011b-opus-1020 (objection); no objection on this row.
- Ids: MAINLINE-027 NFI-027-FRAME-NODES; MAINLINE-011 NFI-011-NODES; MAINLINE-11B NFI-011B-JOINT; MAINLINE-022 NFI-022-JOINTS

**R063. P3 node moment rigidity required by the smeared global mode**
- Unknown: Smeared bending stiffness assumes members continuous through nodes; pinned or soft nodes lower the global mode. Member torsion omitted (would add 11.8-13.7%).
- Needed or settling test: Joints that carry member-end moments as well as axial force; check torsion-rigid case [CHECK-011b]
- Owner: CHECK-011b. State: assumption.
- Check: OPEN, asserted by rpt-check011b-opus-1020: the smeared D needs moment-rigid nodes; 023's joints must carry member-end moments.
- Ids: CHECK-011b NFI-CHK011B-JOINTS

**R064. P3 tube-end joint routes at about 0.5 MN (023: CFRP wrap, Ti, Invar, braze, pin, bond to SiC)**
- Unknown: The rough 0.5 kg fitting was the pin at the two-way force; at the equilateral force the pin is 0.202 kg and the wall still cannot bear it.
- Today: 31.0 kg (0.015 kg per end) at 562.2 kN; 1470 MPa compression allowable [MAINLINE-023] | 28.9 MPa lap shear at 25 C (anodized aluminium); bond 25.0 mm at 562.2 kN [MAINLINE-023] | 157.7 kg (0.075 kg per end) at 562.2 kN, 0.70x the 225.5 kg allowance [MAINLINE-023] | 858.6 kg (0.410 kg per end), 3.81x the allowance [MAINLINE-023]
- Needed or settling test: compression coupon of the wrap bonded to SiC at the sized bond length [MAINLINE-023] | lap shear on the real SiC surface at service temperature [MAINLINE-023] | a higher allowable or a shorter bonded detail [MAINLINE-023] | shear measurement on the tube diameter and a socket section [MAINLINE-023]
- Owner: MAINLINE-023. State: PROJECTION, assumption, exists_today, in_lab, resolved.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-023 NFI-023-CFRP-WRAP; MAINLINE-023 NFI-023-ADHESIVE-TRANSFER; MAINLINE-023 NFI-023-TI-SLEEVE; MAINLINE-023 NFI-023-INVAR; MAINLINE-023 NFI-023-BRAZE; MAINLINE-023 NFI-023-PIN-BEARING


## T19 P3 film

**R065. fibre cross-ply membranes as film (Zylon, Dyneema): not a sourced film; resin, life, gas-tightness**
- Unknown: A uniaxial filament needs a 0/90 build for both pillow directions, doubling thickness; resin not included so a real laminate is heavier.
- Today: 19 years at 60% of break (filament) [MAINLINE-024] | total thickness = 2 x one-direction thickness [MAINLINE-024] | 20% fraction; lives 15 and 250 years at 16 C (rope) [MAINLINE-024]
- Needed or settling test: Laminate creep test [MAINLINE-024] | Resin-inclusive laminate mass [MAINLINE-024] | Film creep data [MAINLINE-024] | Printed density [MAINLINE-024]
- Owner: MAINLINE-024. State: assumption, exists_today, in_lab.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-024 NFI-ZYLON-EXTRAPOLATION; MAINLINE-024 NFI-CROSSPLY; MAINLINE-024 NFI-DYNEEMA-ROPE; MAINLINE-024 NFI-DYNEEMA-DENSITY; MAINLINE-024 NFI-FABRIC-POROUS

**R066. film barrier: permeation data and coatings**
- Unknown: Alumina barrier numbers are coupon measurements; coating a 1257 m2 hull was not opened. PROJECTION at hull scale.
- Today: 1 atm oxygen assumed [MAINLINE-024] | coupon-scale measurements [MAINLINE-024]
- Needed or settling test: Stated test pressure [MAINLINE-024] | N2 permeation for those films [MAINLINE-024] | Hull-scale coating demonstration [MAINLINE-024]
- Owner: MAINLINE-024. State: assumption, in_lab, unknown.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-024 NFI-MYLAR-PRESSURE; MAINLINE-024 NFI-N2-MISSING; MAINLINE-024 NFI-ALD-SCALE

**R067. film pillow radius assumption**
- Unknown: Pillow radius set to the bay side 2.04 m because that is the earlier film formula, not a measured cap.
- Today: pillow radius 2.04 m [MAINLINE-024]
- Needed or settling test: Measured pillow cap [MAINLINE-024]
- Owner: MAINLINE-024. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-024 NFI-CURVATURE

**R068. P3 film allowable and design stress (1.5 GPa carried, no datasheet; Kapton, Teonex, Mylar today)**
- Unknown: Film allowable is an owner assumption with no datasheet; wrinkling, puncture, sag area and shear transfer are unmodelled, and it binds for SiC and CNT rows.
- Today: film allowable 1.5 GPa (no datasheet) [CHECK-011b] | 1.5 GPa, 80 um, 970 kg/m3 (pin) [MAINLINE-024] | design stress = 0.5 x ultimate [MAINLINE-024] | 210 MPa ultimate (thickest opened gauge, 250 um row) [MAINLINE-024]
- Needed or settling test: A datasheet or test for the film allowable [CHECK-011b] | A sourced film allowable [MAINLINE-024] | Creep-rupture fraction for each film [MAINLINE-024] | Data at design thickness [MAINLINE-024]
- Owner: CHECK-011b, MAINLINE-002, MAINLINE-005, MAINLINE-011, MAINLINE-024, MAINLINE-11B, rpt-mainline-grok-estimates-card-1019. State: PROJECTION, assumption, exists_today, unknown.
- Check: raised by CHECK-011b.
- Ids: CHECK-011b NFI-CHK011B-FILM; MAINLINE-024 NFI-FILM-ALLOWABLE-011B; MAINLINE-024 NFI-KNOCK-HALF; MAINLINE-024 NFI-PEN-THICKNESS; MAINLINE-024 NFI-PEN-NOT-DESIGN-DATA; MAINLINE-024 NFI-MYLAR-STRENGTH; MAINLINE-005 NFI-005-FILM; MAINLINE-011 NFI-011-FILM; rpt-mainline-grok-estimates-card-1019 NFI-FILM; MAINLINE-002 NFI-FILM; MAINLINE-11B NFI-011B-LOCAL-FILM; MAINLINE-022 NFI-022-FILM


## T20 Tolerance maps

**R069. 015 tolerance map conventions (lambda, nu) and inversion range; Lee 2016 envelope (015b)**
- Unknown: Amplitudes at kd 0.5, 0.7 and 0.9 are lambda_I = 1 values; worst-width amplitudes are smaller, so the inverted table is optimistic in width.
- Today: kd 0.3 ceiling below 197.052 mm (P2-E), 73.17 mm (014b Be), 39.05 mm (014 Be) [MAINLINE-015] | least SF 0.6686 at kd 0.20; kd 0.2991 lifts only the global mode [MAINLINE-015] | P2-E factor 1.82 (0.46 mm RMS allowance looser than 0.25 mm) [MAINLINE-015] | ratio 293.1 on P2-E [MAINLINE-015]
- Needed or settling test: digitised worst-width envelope at delta/t below 1 [MAINLINE-015] | re-optimised split with kd 0.519 (face yield) for SF 1 [MAINLINE-015] | none [MAINLINE-015] | the min-over-width envelope [MAINLINE-015]
- Owner: MAINLINE-015. State: assumption, resolved, unknown.
- Check: OBJECTION rpt-ref-88e650e7f8b713866e0b: lambda and nu conventions mixed; 015b corrects.
- Ids: MAINLINE-015 NFI-015-KD03-AMPLITUDE; MAINLINE-015 NFI-015-BE-WRINKLING; MAINLINE-015 NFI-015-GAP-DIRECTION; MAINLINE-015 NFI-015-PRESSURE-RATIO; MAINLINE-015 NFI-015-WORST-WIDTH-RISING-BRANCH; MAINLINE-015 NFI-015-FIT-RANGE-FLOOR; MAINLINE-015 NFI-015-HT-EQ32-UNRESOLVED; MAINLINE-015 NFI-015-PNAS-EXTRAPOLATION

**R070. tolerance maps from monocoque shells transferred to sandwich (core shear, waviness, boundaries)**
- Unknown: Core shear cut to classical pressure is derived, but its cut to imperfection sensitivity has no coefficient; kd levels carry no shear correction.
- Today: core shear cuts classical pressure 10.3, 7.0, 0.8 percent on P2-E at 9, 14, 138 MPa [MAINLINE-015] | a locally 10 percent thin face costs 10.0 percent of P2-E classical pressure [MAINLINE-015] | hydrostatic column 240 Pa, 0.25 percent of case pressure [MAINLINE-015]
- Needed or settling test: a shear-flexible imperfection study [MAINLINE-015] | autoclave and core-machining tolerances when the build is chosen [MAINLINE-015] | a separate card for any equator the design keeps [MAINLINE-015]
- Owner: MAINLINE-015. State: assumption, unknown.
- Check: source cards checked by rpt-ref-88e650e7f8b713866e0b (partial); no objection on this row.
- Ids: MAINLINE-015 NFI-015-CORE-SHEAR-SENSITIVITY; MAINLINE-015 NFI-015-THICKNESS-WAVINESS-VALUES; MAINLINE-015 NFI-015-BOUNDARY-AND-TRANSIENT


## T21 Geometry levers

**R071. geometry levers at equal margin (radius, altitude, partial vacuum)**
- Unknown: 11000 m is evaluated on the tropospheric lapse at the tropopause boundary; the isothermal stratosphere is not used; no effect inside this grid.
- Today: 0.1 m core [MAINLINE-012] | troposphere lapse at 11000 m [MAINLINE-012]
- Needed or settling test: re-run levers with thickness re-solved at the float ceiling per radius [MAINLINE-010] | re-run lever 1 on their best rows when filed [MAINLINE-010] | A core thickness that scales with radius. [MAINLINE-012] | Hold T at 216.65 K above 11000 m if climbing further. [MAINLINE-012]
- Owner: MAINLINE-010, MAINLINE-012. State: assumption, unknown.
- Check: source cards checked by rpt-ref-7d4d494ebf14f37f5ea0 (admitted_with_defects), rpt-mainline012-check-glm-1019 (reproduced); no objection on this row.
- Ids: MAINLINE-010 NFI-010-FIXEDTHICK; MAINLINE-010 NFI-010-007008; MAINLINE-012 NFI-CORE-FIXED; MAINLINE-012 NFI-TROPOPAUSE

**R072. P3 member cap bounded continuation**
- Unknown: P3 re-optimisation holds bay 0.4-3 m and member radius at most 0.25 m, which governs large hulls; similarity rows hold 80 um film so film SF falls as 1/R.
- Today: bay 0.4-3 m; member radius at most 0.25 m; film 80 um [MAINLINE-027]
- Needed or settling test: Relaxed member caps or thicker film costed as separate designs [MAINLINE-027]
- Owner: MAINLINE-027. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-027 NFI-027-FRAME-BOUNDARY

**R073. thin-shell validity at low density**
- Unknown: On the buckling split the core exceeds a tenth of the radius below about 1.8 kg/m3, so margins there are not physical.
- Today: B-split core 1.81 m at 1 kg/m3, 18.1 m at 0.1 kg/m3 [MAINLINE-013]
- Needed or settling test: thick-shell sandwich model with inner-surface area [MAINLINE-013]
- Owner: MAINLINE-013. State: unknown.
- Check: source cards checked by rpt-1228-mainline013-independent-check-1020 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-013 NFI-013-GEOMETRY-B


## T22 Metal strength transfer

**R074. face stress past yield elastic wrinkling**
- Unknown: The 6061 face exceeds its questionable 276 MPa yield on every row, so elastic wrinkling forms flatter it.
- Today: face stress 3.57e8 to 7.09e8 Pa against 276 MPa [MAINLINE-013]
- Needed or settling test: a face change (008b) or plasticity factors from CR-1457 section 9 [MAINLINE-013]
- Owner: MAINLINE-013. State: assumption.
- Check: source cards checked by rpt-1228-mainline013-independent-check-1020 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-013 NFI-013-FACE-YIELD

**R075. tensile yield used as the compressive allowable (aluminium and others)**
- Unknown: 276 MPa typical tensile yield is transferred to compression by owner assumption; source says typical values are not for design; no compressive yield was retrieved.
- Today: 276 MPa tensile yield used in compression [MAINLINE-007] | 276 MPa typical tensile yield used as compression [MAINLINE-005] | tensile yields transferred to compression for four metals [MAINLINE-008] | 276 MPa; all-face SF 0.7773844341284152 [CHECK-MAINLINE-007]
- Needed or settling test: A compression yield or a design allowable [MAINLINE-007] | a compressive design allowable [MAINLINE-005] | measured compressive yield per temper and product form [MAINLINE-008] | MMPDS allowables at about 285 K. [rpt-mainline-grok-estimates-card-1019]
- Owner: CHECK-MAINLINE-006, CHECK-MAINLINE-007, MAINLINE-002, MAINLINE-003, MAINLINE-004, MAINLINE-005, MAINLINE-006, MAINLINE-007, MAINLINE-008, MAINLINE-04B, rpt-mainline-grok-estimates-card-1019. State: assumption.
- Check: QUALIFICATION: Una's source objection (rpt-xo-h1-mainline002-review-600-source-objection-correction-sci-1019), carried as a qualification by rpt-admiral-rr2-co-mainline002-strength-questionable-not-objection-1019.
- Ids: MAINLINE-007 NFI-AL-YIELD-CARRY; MAINLINE-005 NFI-005-SIGMA; MAINLINE-008 NFI-008-SIGMA-TRANSFER; rpt-mainline-grok-estimates-card-1019 NFI-AL; MAINLINE-002 NFI-AL-YIELD-CARRY; MAINLINE-003 NFI-AL-YIELD-CARRY; MAINLINE-004 NFI-AL-YIELD-CARRY; MAINLINE-04B NFI-STRENGTH; CHECK-MAINLINE-006 NFI-YIELD; MAINLINE-006 NFI-YIELD; CHECK-MAINLINE-007 NFI-AL-YIELD-CARRY


## T23 PROJECTION materials

**R076. CNT and graphene materials (PROJECTION)**
- Unknown: Cheapest P2 direction on all three leaders is lower face density alone, needing faces near 0.9-1.1 g/cc with CNT, Be and graphene E and sigma; all PROJECTION.
- Today: lightest questionable face T700 at 1550 kg/m3 [MAINLINE-017]
- Needed or settling test: Production allowable and thickness [MAINLINE-024] | a demonstrated QI CNT-yarn or graphene laminate card [MAINLINE-008] | Structural face at about 0.9-1.1 g/cc (959.5, 1129.7, 906.5 kg/m3) with those E and sigma. [MAINLINE-017]
- Owner: MAINLINE-008, MAINLINE-017, MAINLINE-024. State: PROJECTION.
- Check: source cards checked by rpt-ref-f08b92e3e640a19fb4ea (admitted_with_defects), rpt-ref-6936f2b720197d97b0f2 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-024 NFI-CNT-GRAPHENE; MAINLINE-008 NFI-008-PROJECTIONS; MAINLINE-017 NFI-017-FACE-DENSITY


## T24 Method and provenance

**R077. 013 source quality (figure-read, second-hand, unopened sources)**
- Unknown: A list of paywalled sources was not opened, so none of their values is used; the stiffer ultralight ceramic octet point may be among them.
- Today: 1.1 GPa and 10.2 MPa (secondary Jacobsen) [MAINLINE-013] | read-off uncertainty about 25 to 50 percent [MAINLINE-013]
- Needed or settling test: primary papers opened and values matched [MAINLINE-013] | tabulated values from journal SI or theses [MAINLINE-013] | obtain those texts and add values through build_cores.py [MAINLINE-013]
- Owner: MAINLINE-013. State: unknown.
- Check: source cards checked by rpt-1228-mainline013-independent-check-1020 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-013 ref-ce7077da95749d9c1df0; MAINLINE-013 NFI-013-FIGURE-READS; MAINLINE-013 NFI-013-NOT-OPENED

**R078. 1/least SF is not property multiple**
- Unknown: 1/least SF is the safety-factor gap and equals the property multiple only when the mode scales proportionally; wrinkling scales as a cube or square root.
- Owner: MAINLINE-014, MAINLINE-14B. State: assumption.
- Check: source cards checked by rpt-1228-mainline014b-independent-check-1019 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-014 NFI-FACTOR; MAINLINE-14B NFI-FACTOR

**R079. documentation and provenance defects (no numeric effect)**
- Unknown: Owner caveats stand: volume ignores intrusion; joints 5% and systems 100 kg inherited; no sourced Gc/Ec core at 8-1 kg/m3; datasheet disagreements kept; microlattice 0.9 kg/m3 is density only.
- Today: Notes say 12 um cell, N 20, rel. density 0.000104; table gives 8 um, N 10, 0.00182 [CHECK-MAINLINE-013] | payload 0 kg both lines; 100 kg sensitivity [CHECK-019] | 53 verified/measured pins in INPUTS [MAINLINE-027] | RESULTS.json 59234 bytes filed vs 67862 observed; float021.py 31581 vs 36429 [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Needed or settling test: Correct the notes field only [CHECK-MAINLINE-013] | Correct text, pin 011 inputs, relabel two_way rows [CHECK-011b] | Correct the id; state payload handling [CHECK-019] | Normalised throughput, exact p/T climate calculation, variable-pressure integral; measured ground pump-down energy [MAINLINE-019]
- Owner: CHECK-011b, CHECK-019, CHECK-MAINLINE-006, CHECK-MAINLINE-007, CHECK-MAINLINE-013, CHECK-rpt-ref-e92af61311c9bf4a89cd, MAINLINE-008B, MAINLINE-017, MAINLINE-019, MAINLINE-027, MAINLINE-11B. State: assumption, exists_today, resolved, unknown.
- Check: raised by CHECK-011b, CHECK-019, CHECK-MAINLINE-006, CHECK-MAINLINE-007, CHECK-MAINLINE-013, CHECK-rpt-ref-e92af61311c9bf4a89cd.
- Ids: CHECK-MAINLINE-013 NFI-CHECK013-MEZA-SPECIMEN-NOTE; CHECK-011b NFI-CHK011B-TEXT; CHECK-019 NFI-CHK019-TEXT; MAINLINE-019 NFI-019-PREDECESSOR-ARITHMETIC; MAINLINE-027 NFI-027-PROVENANCE; CHECK-rpt-ref-e92af61311c9bf4a89cd NFI-CHECK021-PINS; MAINLINE-08B NFI-008B-BASIS; CHECK-MAINLINE-006 CHECK-NFI-1; CHECK-MAINLINE-007 CHECK-NFI-1; CHECK-MAINLINE-007 NFI-GEOM/MASS/RULE/CORE-FLOOR/DATASHEET/MICROLATTICE; MAINLINE-11B NFI-011B-SKIP; MAINLINE-017 NFI-017-UNFILED

**R080. equal-mass separation convention**
- Unknown: Whether face separation should follow face thickness when face density changes at equal mass; effect is second order against 0.1-0.16 m cores.
- Today: separation held at the row value [MAINLINE-005] | at most 0.348 percent of SF_b on P2-E [MAINLINE-08B]
- Needed or settling test: recompute E/rho with separation following tf for faces far from 2700 kg/m3 [MAINLINE-005] | folds into any future exact recompute [MAINLINE-08B]
- Owner: MAINLINE-005, MAINLINE-008B. State: assumption.
- Check: source cards checked by rpt-ref-78794352b6bc0d9b9309 (admitted_with_defects), rpt-ref-c49d322288a0b11e4381 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-005 NFI-005-SEP; MAINLINE-08B NFI-008B-SEP

**R081. omitted failure modes scope**
- Unknown: Core shear, wrinkling, crush, laminate anisotropy, bond and thermal stress are omitted; SF_b is a first-order thin-face scaling.
- Needed or settling test: 005b for crush; later cards for shear, wrinkling, crippling [MAINLINE-005] | MAINLINE-004 knockdown for kd rescaling and a sandwich failure check per candidate [MAINLINE-008]
- Owner: MAINLINE-004, MAINLINE-005. State: unknown.
- Check: source cards checked by rpt-ref-78794352b6bc0d9b9309 (admitted_with_defects), rpt-ref-f08b92e3e640a19fb4ea (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-005 NFI-005-OMITTED; MAINLINE-008 NFI-008-OMITTED-MODES

**R082. optimiser resolution and scope (grid vs continuous, splits, knees)**
- Unknown: General instability now includes transverse shear; the 007 thickness splits were not re-searched, which matters only for a named core whose Kc moves the equal-factor point.
- Today: least SF 0.65041 (continuous balance 0.65041) [CHECK-MAINLINE-09C5] | least SF 0.17502 (boundary limit 0.17503) [CHECK-MAINLINE-09C5] | grid j/8000 [CHECK-MAINLINE-14B] | grid 0.66865; continuous 0.66871 [CHECK-019]
- Needed or settling test: Label as finite search result; refinement optional [CHECK-MAINLINE-09C5] | Label as grid resolution [CHECK-MAINLINE-09C5] | Label as grid optima; keep reported precision as computational precision [CHECK-MAINLINE-14B] | The unstated core-fraction grid [CHECK-019]
- Owner: CHECK-019, CHECK-MAINLINE-006, CHECK-MAINLINE-07B, CHECK-MAINLINE-09C5, CHECK-MAINLINE-14B, MAINLINE-002, MAINLINE-003, MAINLINE-006, MAINLINE-007, MAINLINE-007B, MAINLINE-017. State: assumption, exists_today, unknown.
- Check: raised by CHECK-019, CHECK-MAINLINE-006, CHECK-MAINLINE-07B, CHECK-MAINLINE-09C5, CHECK-MAINLINE-14B.
- Ids: CHECK-MAINLINE-09C5 NFI-OPTIMUM-RESOLUTION; CHECK-MAINLINE-09C5 NFI-OTHER-BRANCH-RESOLUTION; CHECK-MAINLINE-14B NFI-GRID-RESOLUTION; CHECK-019 NFI-CHK019-014B-GRID; MAINLINE-007 NFI-RULE; MAINLINE-07B NFI-SAND; MAINLINE-002 NFI-FLOAT-ALLOCATION-CARRY; MAINLINE-003 NFI-RULE; CHECK-MAINLINE-006 NFI-KNEE; MAINLINE-006 NFI-KNEE; CHECK-MAINLINE-07B NFI-SAND; MAINLINE-017 NFI-017-COMBO

**R083. optimism factor comparison 021 vs frame**
- Unknown: MAINLINE-021 P2 reaches SF 1 with gamma 2.90x0.20 and wrinkling 1.10x0.33; this frame least equilateral SF 1.354 needs a largest named factor of 8 (arc rise); both questionable.
- Today: P2 largest factor 2.90; frame largest 8; frame least SF 1.35387562843 [MAINLINE-022]
- Owner: MAINLINE-022. State: assumption.
- Check: no check filed on the source cards yet.
- Ids: MAINLINE-022 NFI-022-021

**R084. regressions recover filed points**
- Unknown: With dimpling off, Be S-200F on HRH-10-4.8-32 at kd 0.20 recovers the filed 014 least SF, thicknesses and modes.
- Today: kd 0.20 [MAINLINE-14B]
- Owner: MAINLINE-11B, MAINLINE-14B. State: resolved.
- Check: source cards checked by rpt-check011b-opus-1020 (objection), rpt-1228-mainline014b-independent-check-1019 (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-11B NFI-011B-REGRESSION; MAINLINE-14B NFI-014-REGRESSION

**R085. thin-wall section approximation P3**
- Unknown: Answered here: exact annuli used, and tw/ro at optima is thin; only the fixed ro = 0.02 comparison rows are thick.
- Today: tw/ro = 0.175 on P3-A [MAINLINE-005] | tw/ro 0.019-0.076 at optima; 0.175 to 0.38 at comparison rows [MAINLINE-011]
- Needed or settling test: exact annulus A and I for a named candidate section [MAINLINE-005] | none unless a family nears P3 feasibility [MAINLINE-08B] | none for optima [MAINLINE-011]
- Owner: MAINLINE-005, MAINLINE-008B, MAINLINE-011. State: assumption, resolved.
- Check: source cards checked by rpt-ref-78794352b6bc0d9b9309 (admitted_with_defects), rpt-ref-c49d322288a0b11e4381 (admitted_with_defects), rpt-ref-3484d24f707ffbfe30ee (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-005 NFI-005-THINWALL; MAINLINE-08B NFI-008B-THINWALL; MAINLINE-011 NFI-011-TW-EXACT


## T25 Other

**R086. mooring hardpoint load design**
- Unknown: Mooring hardpoint patch stress exceeds the questionable core allowable and snatch loads need dynamic analysis.
- Today: design load 48.3 kN; bare patch 683 kPa vs 500 kPa allowable, SF 0.73 [MAINLINE-016]
- Needed or settling test: Spreaders of at least 0.145 m2 per hardpoint; mooring dynamics with added mass [MAINLINE-016]
- Owner: MAINLINE-016. State: assumption.
- Check: source cards checked by rpt-ref-e5b19d75c664308465ef (admitted_with_defects); no objection on this row.
- Ids: MAINLINE-016 NFI-016-MOOR


## Sources: report id and NFI file

| report | file |
|---|---|
| rpt-ref-05310d05f1fb52d6522e | evidence/d0ddbdac23ccf0df-NFI.json |
| rpt-ref-3dd5ab5528276031581d | evidence/07d0f8e52a240650-NFI.json |
| rpt-mainline-grok-estimates-card-1019 | evidence/2d0dc7b9973fdc16-NFI.json |
| rpt-mainline002-grok-strength-card-1019 | evidence/b155c07e690eaa66-NFI.json |
| rpt-mainline003-grok-p2-targets-1019 | evidence/2090c6e1f4ca8afb-NFI.json |
| rpt-mainline007b-check-lead4f19-1019 | evidence/ef98a0f4f10c64ba-NFI.json |
| rpt-ref-4f09fd6b4c4dd848ebb0 | evidence/9c93ce0d2b5d8d46-NFI.json |
| rpt-ref-58b2bed18db2449100f2 | evidence/21991360c704a696-NFI.json |
| rpt-1228-mainline013-independent-check-1020 | evidence/ef406b56c4cff82e-NFI.json |
| rpt-ref-eb07faa637b7487d6dc5 | evidence/c108cdbb9f3bcf68-NFI.json |
| rpt-ref-45da79edf548b064b228 | evidence/6284193a78be0578-NFI.json |
| rpt-mainline006-check-lead4f19-1019 | evidence/8060138631058409-NFI.json |
| rpt-mainline006-grok-float-margin-1019 | evidence/c433e7ad1bc469c3-NFI.json |
| rpt-mainline007-check-lead4f19-1019 | evidence/a27128f0dc1713bc-NFI.json |
| rpt-mainline012-grok-equal-margin-1019 | evidence/811b275dbd0d54b1-NFI.json |
| rpt-ref-cc9cef5e55adca018a8f | evidence/cbad32790fc5fde1-NFI.json |
| rpt-ref-06668dbf12580ed0ffc3 | evidence/32fd0bf058dd6218-NFI.json |
| rpt-mainline004-grok-knockdown-card-1019 | evidence/e0152663a63bcf24-NFI.json |
| rpt-mainline004b-grok-kd-range-1019 | evidence/f528292663aa7701-NFI.json |
| rpt-ref-d5b4aaa267b71d82fe25 | evidence/b9cd9c3b294887e6-NFI.json |
| rpt-mainline014-grok-balanced-sandwich-1019 | evidence/e0fba238a74bd426-NFI.json |
| rpt-mainline014b-grok-metal-honeycomb-1019 | evidence/e56941cee236de62-NFI.json |
| rpt-1228-mainline009c5-independent-check-1019 | evidence/4662757b4d50b2d1-NFI.json |
| rpt-1228-mainline014b-independent-check-1019 | evidence/5d2a8afe8b483d72-NFI.json |
| rpt-check019-opus-1020 | evidence/9cc8bdcb82e9b2d1-NFI.json |
| rpt-ref-d7f99cd71e977826da48 | evidence/fec518f4f7e18a36-NFI.json |
| rpt-ref-2898e43e4928e833af6d | evidence/fecbe3eb74d15e6e-NFI.json |
| rpt-ref-3e02218a03708a878faa | evidence/72e91c4df6df4236-NFI.json |
| rpt-ref-769a7442efd5a04681e9 | evidence/fae865c7f039491f-NFI.json |
| rpt-ref-1080d4f6a1af4cfa8c67 | evidence/b056cc13a604abed-NFI.json |
| rpt-ref-2519e14e5d71b9eb18f3 | evidence/4a6f636dbfa17be3-NFI.json |
| rpt-mainline017-improvement-directions-lead4f19-1019 | evidence/9f3c760a855408f0-NFI.json |
| rpt-ref-44f9940325e236cb80b3 | evidence/fe5e5ec3daad9605-NFI.json |
| rpt-ref-e92af61311c9bf4a89cd | evidence/0b74ca6f4252ee9e-NFI.json |
| rpt-ref-9dd3721f6f2e5595ab9a | evidence/fa0b32e084a42fda-NFI.json |
| ref-0c9ab80606a173c6adb6 | evidence/e000d61baed6b1db-NFI.json |
| rpt-check011b-opus-1020 | evidence/610aec93220adcc1-NFI.json |
| rpt-ref-a4768f77870336c8cdbb | evidence/30c19a9c27a07c4b-NFI.json |
| rpt-mainline011b-grok-p3-global-arcs-1019 | evidence/da2eeba2a608cb9e-NFI.json |
| rpt-ref-f21d4bd21d2026511818 | evidence/0f1373271ca0676e-NFI.json |
| rpt-mainline022-grok-p3-optimistic-floating-point-1020 | evidence/307ab133da904ca4-NFI.json |
