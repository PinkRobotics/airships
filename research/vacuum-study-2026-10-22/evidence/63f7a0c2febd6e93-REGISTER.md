# Complete design register

QUESTIONABLE / PROJECTION. Record version 5; snapshot 2026-10-20T10:48:05.827454-07:00. Qualified installed-hull SF, life, failure probability and availability remain unknown.

All 104 original rows and their original fields are preserved. New rows have stable finding IDs. See CLAIMS.md for the full finding index and CLAIM-RECORD.json for exact original fields and source selectors.

## R001 — Case and atmosphere

**Gap:** hull radius and volume convention (mould line vs mid-surface, wall intrusion)

**Unknown:** Handbook radius is the middle surface; ratios use external 10 m and are unaffected since both pressures scale as 1/R^2; absolute pressure on thick rows needs an inner mould line.

**Physical qualification:** open.

**Today:**

- buckling-peak core 1.81457668 m at 1 kg/m3 [MAINLINE-007]
- external radius 10 m [MAINLINE-07B]
- R = 10 m external [CHECK-MAINLINE-07B]

**Needed:**

- Inner and outer mould lines [MAINLINE-007]
- Inner mould line for absolute pressure [MAINLINE-07B]
- Define inner and outer mould lines. [rpt-mainline-grok-estimates-card-1019]
- Inner and outer mould lines. [MAINLINE-002]

**Finding IDs:** N036, N045, N249, N259, N269, N303

## R002 — Case and atmosphere

**Gap:** ISA case is a standard dry column, not a site or day

**Unknown:** Dry constant-g geopotential formula used with geometric height substituted; no humidity case; density and pressure drive float margin and every safety factor.

**Physical qualification:** open.

**Today:**

- N2 0.78084; O2 0.20946 (not in case) [MAINLINE-024]
- 500 m ISA point matches pinned case within 0.1 Pa [MAINLINE-010]

**Needed:**

- Include composition in the case [MAINLINE-024]
- a measured column once a site is named [MAINLINE-010]
- Pin an ISO 2533 or ICAO Doc 7488 table at 500 m plus a humidity case. [rpt-mainline-grok-estimates-card-1019]
- Keep the 500 m case as the basis. [rpt-mainline-grok-estimates-card-1019]

**Finding IDs:** N099, N146, N242, N252

## R003 — Shell knockdown kd

**Gap:** buckling SF is linear in kd only at fixed geometry

**Unknown:** The claim that local needs are independent of kd holds only at fixed geometry; re-optimising for a new kd changes thicknesses and local needs.

**Physical qualification:** open.

**Today:**

- kd = 0.2 [MAINLINE-005]
- 0.2 (0.90 optimistic carry) [MAINLINE-006]

**Needed:**

- Qualify the statement as fixed-geometry; rebuild the design if kd changes [CHECK-MAINLINE-013]
- kd from the 004 named knockdown curve; multiply each E by 0.2/kd [MAINLINE-005]
- MAINLINE-004 filed values [MAINLINE-008]
- Multiply buckling SF by kd/0.2 when another knockdown is adopted. [CHECK-MAINLINE-006]

**Finding IDs:** N009, N122, N137, N285, N289, N297, N318

## R004 — Shell knockdown kd

**Gap:** knockdown transfer from monocoque to sandwich sphere at R 10 m

**Unknown:** The curve is monolithic clamped-cap evidence; phi equal pi and the equivalent thickness are transfers onto a complete sandwich sphere, so the buckling SF is not a validated sandwich knockdown.

**Physical qualification:** open.

**Today:**

- conservative SP-8032 cap factor, central 0.20, optimistic 0.90 [MAINLINE-08B]
- transfer t_eq = sqrt(3)(d+tf) [MAINLINE-015]
- dimple 0.20, flat 0.22 (numerical, small hemispheres) [MAINLINE-04B]

**Needed:**

- a sandwich-specific knockdown for this geometry [MAINLINE-08B]
- a sandwich imperfection study at this geometry [MAINLINE-015]
- A sandwich knockdown test or formula at these proportions. [MAINLINE-004]
- A sandwich source at these proportions. [MAINLINE-04B]

**Finding IDs:** N143, N177, N272, N279, N280

## R005 — Shell knockdown kd

**Gap:** monocoque sphere knockdown kd: value and range (SP-8032 curve, 0.14 to 0.9)

**Unknown:** gamma_d is 0.20 on the moderate branch; 0.90 is not a handbook value but the precision direction; 0.1407 conservative. Separation of face-modulus knockdown from core-shear flexibility is untested.

**Physical qualification:** open.

**Today:**

- kd = 0.2 [MAINLINE-007]
- kd 0.2 main; 0.1407 conservative; 0.9 optimistic [MAINLINE-009]
- gamma_d 0.2 main; 0.1407 conservative; 0.9 optimistic [MAINLINE-009]
- 0.14 + 3.2/lambda^2 form (text reproduction) [MAINLINE-004]

**Needed:**

- Knockdown curve from the owning card [MAINLINE-007]
- Knockdown tests on sandwich spheres at lambda near 66 [MAINLINE-009]
- Tests separating face-modulus knockdown from core-shear flexibility on a complete sphere [MAINLINE-009]
- Evaluate NASA SP-8032 at the complete-sphere geometry. [rpt-mainline-grok-estimates-card-1019]

**Finding IDs:** N034, N048, N054, N244, N256, N267, N271, N277, N278, N281, N282, N322, N331

## R006 — Crimp-branch gamma

**Gap:** core shear (crimp) in sandwich buckling: formula and Gc basis

**Unknown:** Advisory crimp replaced by sourced equations; sourced cores stay on the moderate branch, buckling SF trimmed. A core G below about 2.45 MPa would enter crimping; none do.

**Physical qualification:** open.

**Today:**

- advisory crimp target cleared by catalog G at 16-38 kg/m3 [MAINLINE-007]
- Kc trims buckling SF to 0.864-0.991 of the MAINLINE-007 value; crimp entry below G about 2.45 MPa [MAINLINE-07B]

**Needed:**

- Published sandwich-shell formula including transverse shear [MAINLINE-007]
- Sourced crimp formula [MAINLINE-007]
- A published sandwich-sphere formula that includes core shear. [rpt-mainline-grok-estimates-card-1019]
- A published sandwich formula that includes shear. [MAINLINE-002]

**Finding IDs:** N030, N031, N041, N245, N255, N263, N264, N275, N288, N292

## R007 — Crimp-branch gamma

**Gap:** gamma(Vc) for a sandwich sphere: CR-1457 step (0.20 below Vc 2, 1 above) vs 018 curves; P2 lead needs 0.468-0.595 (O1)

**Unknown:** A high shear modulus leaves the crimp branch and gamma becomes the knockdown 0.20; best aluminium stiff-branch rows reach SF 0.669 and 0.642, below the HRH-10 crimp balance 0.685.

**Physical qualification:** open.

**Today:**

- gamma 0.2 at Vc=2 [CHECK-MAINLINE-09C5]
- With same curve for both: Al 0.847 vs aramid 0.609 (optimistic line) [CHECK-019]
- gamma_d 0.20 on moderate branch [MAINLINE-07B]
- step 0.2 to 1 at Vc=2 vs 0.2+0.4*min(Vc,2) [MAINLINE-027]

**Needed:**

- gamma = 1 for Vc>=2 per cited convention [CHECK-MAINLINE-09C5]
- State the equality convention when carrying the branch wording [CHECK-MAINLINE-14B]
- Re-solve budgets under the same gamma curve for both families [CHECK-019]
- gamma_d 1 on crimping branch (handbook) [MAINLINE-07B]

**Finding IDs:** N004, N016, N025, N044, N075, N103, N192, N193, N197, N202, N203, N211, N241, N299, N302, N327, N344, N347, N349

## R008 — Wrinkling and core Ec

**Gap:** core Ec (stabilised datasheet value) transferred into the wrinkling formula

**Unknown:** Plascore PAMG-XR1 5052 prints no stabilised compressive modulus and no crush column; Ec is transferred from Hexcel CR-III 5052; crush is Plascore bare, not the Hexcel crush-column test.

**Physical qualification:** open.

**Today:**

- catalog cores miss product by about 40-180x [MAINLINE-007]
- Hexcel wrinkling SF 0.0565 and 0.0415 [MAINLINE-07B]
- coefficient 0.5 on cube root of E_f*Ec*Gc [MAINLINE-08B]
- catalog cores 16-38 kg/m3 clear advisory crush and crimp [CHECK-MAINLINE-007]

**Needed:**

- Sourced wrinkling formula keeping Ec and Gc separate; aluminium honeycomb Ec [MAINLINE-007]
- Sourced honeycomb Ec [MAINLINE-07B]
- 007b sourced sandwich-shell shear and wrinkling formulas [MAINLINE-08B]
- Separate Ec and Gc from a datasheet. [MAINLINE-003]

**Finding IDs:** N032, N042, N139, N265, N296, N325, N336, N339

## R009 — Wrinkling and core Ec

**Gap:** equibiaxial wrinkling interaction factor (0.682) on a curved face

**Unknown:** The flat-plate interaction is applied to equibiaxial membrane stress of a sphere; a sphere-specific interaction could replace it.

**Physical qualification:** open.

**Today:**

- equibiaxial factor 0.6823 (from R^3+R=1) [MAINLINE-07B]
- equibiaxial factor 0.6823, already inside the stated SF [MAINLINE-009]
- 0.6823278038280193 [CHECK-MAINLINE-07B]

**Needed:**

- Sphere-specific wrinkling interaction [MAINLINE-07B]
- Sphere-face wrinkling test [MAINLINE-009]
- A sphere-specific wrinkling interaction. [CHECK-MAINLINE-07B]

**Finding IDs:** N047, N055, N305

## R010 — Wrinkling and core Ec

**Gap:** honeycomb wrinkling coefficient 0.33 (design) vs 0.82 (theoretical) (O2)

**Unknown:** Foam wrinkling gives 0.709 of advisory uniaxial SF; Hexcel honeycomb wrinkling (0.0565, 0.0415) falls below general instability and would govern if admitted; Plascore Ec open, Hexcel stabilised Ec questionable.

**Physical qualification:** open.

**Today:**

- design coefficients 0.50 and 0.33; classical 0.76 and 0.82 [MAINLINE-013]
- coefficient 0.33 (design lower bound) [MAINLINE-021]
- coefficient 0.33 (classical 0.82) [MAINLINE-21B]
- foam factor 0.6823278 (Q 0.50) [CHECK-MAINLINE-07B]

**Needed:**

- Correct the sentence [CHECK-MAINLINE-14B]
- a representative wrinkling test fixing the coefficient for the chosen face and core [MAINLINE-013]
- coefficient 0.3707; a wrinkling test on a representative sandwich [MAINLINE-021]
- coefficient 0.6092 [MAINLINE-21B]

**Finding IDs:** N014, N167, N194, N204, N300, N329, N343, N351

## R011 — Wrinkling and core Ec

**Gap:** intracell dimpling: biaxial vs uniaxial rule and coefficient

**Unknown:** Intracell dimpling uses the brief stress 2*E_f/(1-nu^2)*(tf/s_cell)^2 with nominal cell size, no equibiaxial factor; foam is not dimpled; the coefficient 2 is the brief expression.

**Physical qualification:** open.

**Today:**

- dimpling margin 9.019 biaxial vs 18.04 uniaxial [MAINLINE-021]
- coefficient 2 (brief expression) [MAINLINE-14B]

**Needed:**

- none [MAINLINE-021]

**Finding IDs:** N200, N342

## R012 — Wrinkling and core Ec

**Gap:** laminate bending stiffness in wrinkling

**Unknown:** Composite faces use an inherited scalar quasi-isotropic modulus in the wrinkling formula; laminate bending stiffness (layup) is not supplied.

**Physical qualification:** open.

**Today:**

- Scalar quasi-isotropic face modulus (value not stated) [CHECK-MAINLINE-14B]

**Needed:**

- Layup / bending-stiffness sensitivity in a later fix card [CHECK-MAINLINE-14B]

**Finding IDs:** N015

## R013 — Face properties

**Gap:** Be face compressive allowable by grade, form and source: 241 / 255 / 283 / 345 / 379 MPa (O3)

**Unknown:** Face compression is exactly 1 on the SR-200 minimum tensile yield used as compressive; no compressive minimum is published, and gauge tolerance or post-form properties can take it below 1.

**Physical qualification:** open.

**Today:**

- 283 MPa (frozen); current guide about 255 MPa [CHECK-MAINLINE-09C5]
- S-200F E 290 GPa, 283 MPa; SR-200 lot 379.2 MPa, E 293.6 GPa; SR-200 tensile minimum 345 MPa [MAINLINE-027]
- 283 MPa starting value; current guide about 255 MPa; SR-200 tensile minimum 345 MPa; main route needs about 283 MPa [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- 379.2 MPa sheet; tube values 450 and 544 MPa [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Needed:**

- Pin the exact older edition supporting 283 MPa and reconcile with the newer guide [CHECK-MAINLINE-09C5]
- Lot-, gauge-, direction- and post-form compression, stiffness and Poisson data [MAINLINE-027]
- Matched product, lot and thickness compression value [CHECK-rpt-ref-e92af61311c9bf4a89cd]
- Narrow wording to the strongest applicable sheet value; any tube-to-sheet transfer is a separate PROJECTION [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Finding IDs:** N002, N013, N104, N120, N121, N187, N195, N207, N240

## R014 — Face properties

**Gap:** CFRP quasi-isotropic face properties (Be-free fallback)

**Unknown:** QI laminate modulus and compressive strength for T700, M55J, K13D2U and boron/epoxy are estimated from UD data with assumed reduction factors, not measured.

**Physical qualification:** open.

**Today:**

- least SF 0.5415 (exact geometry) to 0.6519 (published); relative loss 4.9 to 16.7 percent [MAINLINE-020]

**Needed:**

- measured QI laminate modulus and compressive strength at intended fibre volume fraction [MAINLINE-008]
- I014b QI laminate compression, stiffness, density and manufacturing route [MAINLINE-020]

**Finding IDs:** N132, N189

## R015 — Face properties

**Gap:** face Poisson ratio (0.33 carried; Be sheet about 0.08)

**Unknown:** Poisson ratio in buckling and foam-wrinkling formulas is carried from the 6061 case; no SiC value was given. Buckling pressure scales as 1/sqrt(1-nu^2).

**Physical qualification:** open.

**Today:**

- nu 0.33 (carried from 6061) [MAINLINE-009]
- nu 0.33 (card); nu12 0.0768, nu21 0.0752 (orthotropic lot) [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Needed:**

- Face sheet's own Poisson ratio [MAINLINE-009]
- Coherent measured in-plane elastic tuple and an orthotropic model, or a tagged isotropic approximation [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Finding IDs:** N051, N119, N321, N330

## R016 — Face properties

**Gap:** S-200F modulus is 290 GPa, not the 303 GPa of S-200FH

**Unknown:** Comparisons retain 303 GPa, 283 MPa compression and nu 0.33 although the current forms sheet gives 290 GPa for S200F and 303 for S200FH; compression basis to reconcile.

**Physical qualification:** open.

**Today:**

- E = 303 GPa as reported (source says 290 GPa) [CHECK-MAINLINE-09C5]
- E = 303 GPa (card); 290 GPa (checker) [CHECK-MAINLINE-013]
- E 303 GPa; compression 283 MPa; nu 0.33 (290 GPa sensitivity supplied) [MAINLINE-019]
- E 303 GPa (card); 290 GPa (datasheet); sheet full-gamma SF 0.942 at same geometry [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Needed:**

- Grade-specific 290 GPa, or an explicitly sourced 303 GPa scenario [CHECK-MAINLINE-09C5]
- Use 290 GPa for the named grade and update the projection, or source and label S200FH [CHECK-MAINLINE-013]
- Reconcile exact grade, compression basis and Poisson ratio; no tensile substitution [MAINLINE-019]
- Keep E, strength and product form together; reissue claims under the grade correction [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Finding IDs:** N001, N007, N012, N074, N118, N198

## R017 — Face properties

**Gap:** SiC face properties (009b)

**Unknown:** SiC face compressive strength is taken as 3900 MPa (compression mode) vs 380 MPa flexural; a compressive allowable for the sintered face and a membrane-compression-only check are open.

**Physical qualification:** open.

**Today:**

- 3900 MPa compressive (optimistic); 380 MPa flexural (conservative); SF 0.433 if flexural used [MAINLINE-009]
- E 410 GPa, density 3100 kg/m3 [MAINLINE-009]

**Needed:**

- Compressive allowable for the sintered face; check stress stays membrane compression [MAINLINE-009]
- Batch modulus and density for the actual face sheet [MAINLINE-009]

**Finding IDs:** N049, N050

## R018 — Face sheet and panels

**Gap:** Be thin-sheet panel size and gauge: 0.914 m square-equivalent stock today, 3.13 to 4 m assumed (O4)

**Unknown:** Severe-budget faces are far below supplier stock gauge; stock for the large panel begins at 0.059 in and the enhanced aluminium face at R=20 is thinner. Small panel size assumed.

**Physical qualification:** open.

**Today:**

- 18 m equivalent widths required [MAINLINE-019]
- Be faces about 0.056-0.057 mm; core 6.8-8.3 mm [MAINLINE-019]
- stock begins 0.059 in (1.4986 mm); enhanced Al face 1.423 mm at R=20; panel 0.6096 x 1.8288 m [MAINLINE-027]
- assumed panels 0.61x1.83 m (optimistic) to 0.30x0.61 m; source gauge tolerance 0.1016 mm [MAINLINE-020]

**Needed:**

- Manufacturer grade, size, forming route, gauge tolerance and yield quote; spherical seam-layout takeoff [MAINLINE-019]
- Local geometry, imperfections, seam load transfer and nonlinear validation [MAINLINE-019]
- Supplier confirmation of dimensions at each minimum gauge, shaping yield, thickness distribution [MAINLINE-027]
- supplier-confirmed grade, gauge, size, flatness; formed-panel gauge map and curvature survey [MAINLINE-020]

**Finding IDs:** N071, N077, N100, N186, N199, N205, N235, N236

## R019 — Cores

**Gap:** core crush criterion (crush strength against p/2)

**Unknown:** Hexcel CR-III crush column is used; HFT and HRH-49 have no crush column so stabilised compressive strength is used; thickness does not enter; target is p/2.

**Physical qualification:** open.

**Today:**

- catalog compressive strengths at 16-38 kg/m3 clear p/2 by about 7 to 27 times [MAINLINE-007]
- core stress p/2 [MAINLINE-009]
- core stress factor 1/2 of p (brief example, no pinned reference) [MAINLINE-05B]
- required core strength 47730.4 Pa on every row [MAINLINE-013]

**Needed:**

- A sourced crush model [MAINLINE-007]
- Core stress from face-to-face load path including local bending [MAINLINE-009]
- pinned sandwich core-crush reference and re-derived factor [MAINLINE-05B]
- apply p/2 at 007's external pressure when it lands [MAINLINE-05B]

**Finding IDs:** N033, N053, N128, N130, N168, N266, N276, N326, N340

## R020 — Cores

**Gap:** core shear strength is not a scored mode

**Unknown:** L and W plate-shear strengths are stored, but the crimp mode scores shear modulus and shear strength is not a separate mode.

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** N341

## R021 — Cores

**Gap:** foam core allowables (crush strain, creep, design values)

**Unknown:** H35 properties are typical or nominal, not allowables; rev9 prints a minimum compressive strength of 0.3 MPa vs 0.5 MPa nominal used (factor 1.67).

**Physical qualification:** open.

**Today:**

- density 38 kg/m3; Ec 40 MPa; Gc 12 MPa; compressive 0.5 MPa nominal (0.3 MPa minimum) [MAINLINE-009]
- incumbent 16 kg/m3 passes on one strain definition, fails on the other; lowest passing density between about 11 and 22 kg/m3 [MAINLINE-05B]
- 11 kg/m3 lowest passing density, no creep derate [MAINLINE-05B]
- EPS12 at 11.2 kg/m3: 15 kPa at 1 percent, 40 kPa at 10 percent [MAINLINE-013]

**Needed:**

- Design allowables for Ec, Gc and compressive strength at the used thickness [MAINLINE-009]
- checker names the governing strain definition [MAINLINE-05B]
- sustained-load derate of foam allowables before relying on densities near 11 kg/m3 [MAINLINE-05B]
- one strain definition and a measured value [MAINLINE-013]

**Finding IDs:** N052, N129, N131, N169

## R022 — Cores

**Gap:** honeycomb datasheet values and conversions (W vs L shear, typical vs minimum, density)

**Unknown:** Datasheets print conflicting values: Plascore 5052 gives 100 psi and 0.55 MPa in one cell; Divinycell H35 0.45 MPa (rev7) vs 0.50 MPa (rev9). Crush margins still clear.

**Physical qualification:** open.

**Today:**

- 100 psi vs 0.55 MPa; H35 0.45 vs 0.50 MPa [MAINLINE-007]
- Hexcel test thickness 0.625 inch vs 20 mm core [MAINLINE-021]
- 16 kg/m3 [rpt-mainline-grok-estimates-card-1019]
- 14.3 ksi used (brochure 13.3 ksi) [MAINLINE-14B]

**Needed:**

- Keep both readings; resolve revision [MAINLINE-007]
- Pin a honeycomb or foam sheet at the thickness used. [rpt-mainline-grok-estimates-card-1019]
- Stabilised Ec and L/W shear moduli in the band. [MAINLINE-14B]

**Finding IDs:** N039, N201, N246, N334, N335, N337, N338

## R023 — Cores

**Gap:** thick curved honeycomb core validation

**Unknown:** Core data are catalogue typical rows tested at 15.875 mm depth, while optimised cores reach about 120-144 mm; Ec transferred from another maker and bare compression substituted for crush.

**Physical qualification:** open.

**Today:**

- test depth 15.875 mm vs 120-144 mm needed at R=50 [MAINLINE-027]

**Needed:**

- Validation of thick curved honeycomb: skin restraint, orthotropy, depth effects, crush definition [MAINLINE-027]

**Finding IDs:** N105

## R024 — Cores

**Gap:** ultralight cores below about 16 kg/m3: no sourced material; scaled moduli are PROJECTION

**Unknown:** No measured shear modulus at or below 10 kg/m3; G=E/2 is an assumption; figure reads, bulk-scale transfer and continuum validity unproved; 190 kg/m3 row passes locally only.

**Physical qualification:** open.

**Today:**

- Basotect crush above 9000 Pa, no upper bound; EPS12 minimum 15000 Pa at 1% strain, density minimum 11.2 kg/m3 [CHECK-MAINLINE-013]
- named-set high SF 0.737 at 1 kg/m3; buckling SF reaches 1 at 3.73 kg/m3 [MAINLINE-007]
- density at or above 0.9 kg/m3 [MAINLINE-007]
- lightest sourced catalog core 16 kg/m3 (ROHACELL 31, HexWeb 24); microlattice at 0.9 kg/m3 has no modulus or strength [MAINLINE-08B]

**Needed:**

- Measured crush, Ec and G of the actual material; keep comparison operators and property basis [CHECK-MAINLINE-013]
- Measured properties at the claimed density before any new material claim; keep PROJECTION tag on ideal-lattice uses [CHECK-MAINLINE-013]
- A sourced structural core at low density [MAINLINE-007]
- Sourced Gc, Ec and crush strength at those densities [MAINLINE-007]

**Finding IDs:** N008, N011, N029, N038, N040, N046, N138, N155, N156, N157, N158, N159, N162, N163, N166, N170, N262, N273, N295, N304, N323, N324, N332, N333

## R025 — P2 joints, seams and film

**Gap:** 30:1 adhesive scarf seam

**Unknown:** Thin Be/Be scarf performance is untested; the 10 MPa shear screen is selected, not qualified.

**Physical qualification:** open.

**Today:**

- 25.303 mm run; 9.421 MPa average shear; 0.01060 kg/m seam [MAINLINE-028]

**Needed:**

- thin Be/Be scarf compression, biaxial transfer, peel and cyclic data at actual film weight [MAINLINE-028]

**Finding IDs:** N228

## R026 — P2 joints, seams and film

**Gap:** adhesive-free diffusion interface

**Unknown:** Zero added filler is an ideal limit; the replacement core density and strength are unknown.

**Physical qualification:** open.

**Today:**

- 0 added filler (ideal limit) [MAINLINE-028]

**Needed:**

- complete installed bill and measured structure: core density, stiffness, strength, process pressure [MAINLINE-028]

**Finding IDs:** N227

## R027 — P2 joints, seams and film

**Gap:** bond film areal weight and coverage (0.015 to 0.060 lb/ft2)

**Unknown:** Matching Be/core strength and stiffness at the lowest-weight reticulated film weight are unmeasured; hull adoption is a projection.

**Physical qualification:** open.

**Today:**

- 0.03 lb/ft2 (full optimism 0.015 lb/ft2) [MAINLINE-21B]
- AF163-2U 73.236 g/m2 exists; budget maximum 74.107 g/m2 [MAINLINE-028]
- manufacturer tolerance +/-0.005 lb/ft2; upper-weight joining 275.6 kg vs 216.4 kg allowance [MAINLINE-028]
- HexBond312 70 g/m2 lap shear 37 MPa on Al; 100 g/m2 5.4 MPa on a different sandwich [MAINLINE-028]

**Needed:**

- 0.03 lb/ft2 at the floating point [MAINLINE-21B]
- weigh installed cured film; Be/core strength, stiffness and defects at that weight [MAINLINE-028]
- lot areal-mass distribution and cured retained mass [MAINLINE-028]
- test of the actual assembly [MAINLINE-028]

**Finding IDs:** N206, N222, N223, N224

## R028 — P2 joints, seams and film

**Gap:** brazed scarf seam

**Unknown:** Al-Si braze shear is a typical value, not an allowable; thin-sheet joint distribution, fatigue and distortion unknown.

**Physical qualification:** open.

**Today:**

- Al-Si typical shear 103.4 MPa vs 84.884 MPa needed; 50 um filler gap [MAINLINE-028]

**Needed:**

- thin-sheet joint distribution, compressive/peel fatigue, distortion, closure sequence [MAINLINE-028]

**Finding IDs:** N230

## R029 — P2 joints, seams and film

**Gap:** butt-strap seam route

**Unknown:** Butt-strap bending, peel and strip buckling are unmeasured; this route is 2.88x over the joining allowance.

**Physical qualification:** open.

**Today:**

- 47.730 mm strap width per face; 0.162691 kg/m; 623.1 kg [MAINLINE-028]

**Needed:**

- measured local bending and peel, strip buckling, or a symmetric alternative [MAINLINE-028]

**Finding IDs:** N229

## R030 — P2 joints, seams and film

**Gap:** core splice allowance

**Unknown:** Installed core splice mass and its ability to transmit core shear are unknown.

**Physical qualification:** open.

**Today:**

- selected 0.5 mm gap and 500 kg/m3 cured filling; 0.00505 kg/m [MAINLINE-028]

**Needed:**

- weighed edge splice transmitting core shear with real gaps and nodes [MAINLINE-028]

**Finding IDs:** N232

## R031 — P2 joints, seams and film

**Gap:** core-to-face brazing route

**Unknown:** No structural data for brazing a Be face to the selected 16 kg/m3 Al core exist; coated CRIII properties may not carry over.

**Physical qualification:** open.

**Today:**

- generic Be brazing exists; filler 5.67-22.68 g/m2 geometric [MAINLINE-028]

**Needed:**

- wetting, residual stress and bare-core condition after joining qualified [MAINLINE-028]

**Finding IDs:** N226

## R032 — P2 joints, seams and film

**Gap:** electron-beam seam retention

**Unknown:** Thin-sheet Be EB seam compression retention is unknown; 100 percent retention is a projection and 80 percent a sensitivity.

**Physical qualification:** open.

**Today:**

- Be EB process exists; SF 0.853 at assumed 80 percent retention [MAINLINE-028]

**Needed:**

- retention 0.9998 at original gauge; weld/HAZ compression, ductility, penetration, leak integrity [MAINLINE-028]

**Finding IDs:** N231

## R033 — P2 joints, seams and film

**Gap:** P2 seam and bond mass and capacity on the hull (016, 019, 020, 021b, 027, 028)

**Unknown:** Net-section efficiencies are assumed screens applied only to compression; the enhanced aluminium optimum is joint-limited and no joint buckling, shear or peel allowables exist.

**Physical qualification:** open.

**Today:**

- today's 0.5 m Hexoloy plate gives 330-694% of the 216.427 kg allowance [MAINLINE-016]
- film use .015/.030 lb/ft2 (.015 mass-lower choice) [MAINLINE-019]
- efficiencies 0.9 / 0.6 (assumed) [MAINLINE-027]
- joining 968.2 kg optimistic (eta 0.9) to 3722.0 kg conservative (eta 0.6); payload -507 to -3261 kg [MAINLINE-020]

**Needed:**

- Real maximum plate size and a seam parts list for a named panel size, or a face family with 2-4 m sheets [MAINLINE-016]
- Test a complete seam and bond architecture for installed mass, leak rate and stiffness [MAINLINE-019]
- Weigh and load-test a curved two-skin splice; seam parameters versus thickness [MAINLINE-027]
- Measured seam biaxial compression, eccentricity and failure envelope [MAINLINE-027]

**Finding IDs:** N057, N072, N101, N102, N185, N209, N238

## R034 — P2 joints, seams and film

**Gap:** primer and surface prep mass

**Unknown:** Be-compatible primer and surface preparation mass is not counted; zero is only a bookkeeping limit.

**Physical qualification:** open.

**Today:**

- zero primer; 5 g/m2 per line as sensitivity (12.57 kg) [MAINLINE-028]

**Needed:**

- qualified Be-compatible preparation weighed including core-side coverage [MAINLINE-028]

**Finding IDs:** N234

## R035 — P2 joints, seams and film

**Gap:** seam step effect on kd

**Unknown:** A seam step is counted only as delta/t_eq; a real seam also breaks face continuity, and no joint failure model exists.

**Physical qualification:** open.

**Today:**

- kd 0.950, 0.931, 0.869 at steps of 1, 3, 10 mm on P2-E [MAINLINE-015]

**Needed:**

- a joint model with the sandwich failure cards [MAINLINE-015]

**Finding IDs:** N182

## R036 — P2 joints, seams and film

**Gap:** selective cell-edge adhesive deposition

**Unknown:** Selective cell-edge deposition is lab-only on CFRP/Nomex and not shown on Be/Al.

**Physical qualification:** open.

**Today:**

- 8-80 g/m2 deposited in CFRP/Nomex experiments [MAINLINE-028]

**Needed:**

- coverage, fillets, cured mass and mechanical performance after transfer to Be/Al [MAINLINE-028]

**Finding IDs:** N225

## R037 — P2 joints, seams and film

**Gap:** spherical layout and scarf edges

**Unknown:** No polar-cap or intersection design; the mean-field rectangular layout ignores tessellation, tolerances and rejects.

**Physical qualification:** open.

**Today:**

- mean-field layout with scarf overlap deducted; spare 2.19 kg [MAINLINE-028]

**Needed:**

- finished spherical tessellation with fit tolerances, waviness and installation rejects [MAINLINE-028]

**Finding IDs:** N237

## R038 — Margin items

**Gap:** 019's optimistic reserve embeds 4 m panels and 0.015 lb/ft2 film

**Unknown:** The 019 reserve of 535.95 kg embeds 4 m panels and 0.015 lb/ft2 film; at today panel and film the reserve is larger.

**Physical qualification:** open.

**Today:**

- reserve 1229.4 kg at today panel and film [MAINLINE-21B]

**Needed:**

- See source fields.

**Finding IDs:** N208

## R039 — Margin items

**Gap:** design-day climate envelope for lift (site, temperature, pressure, humidity)

**Unknown:** Lift depends on site temperature and pressure; no site is named so the 5% margin has no climate envelope. Hot afternoon and retained water each consume the margin.

**Physical qualification:** open.

**Today:**

- +25.1 K gives margin -186.3 kg; 0.1 mm retained water 125.6 kg [MAINLINE-016]
- optimistic +10 K, +/-1%, 1000 Pa vapour; conservative +25.1 K, +/-2%, 6000 Pa [MAINLINE-027]
- optimistic day: 0.1 mm water, +10 K, 1 percent, 1 kPa; conservative needs 4229 kg [MAINLINE-21B]

**Needed:**

- Named site and season windows; ballast or trim sizing; coating and shedding check [MAINLINE-016]
- Station data and operating constraints; recompute mass and max differential-pressure cases [MAINLINE-019]
- Site, gas composition, temperatures, weather exposure, water shedding/icing, duration [MAINLINE-027]
- site and gas-load measurement (019 follow-ups) [MAINLINE-21B]

**Finding IDs:** N058, N068, N108, N210

## R040 — Margin items

**Gap:** float margin and payload: 0%, 5%, 10.96% and 86.49% budgets

**Unknown:** Reserve is the explicit charge above baseline floors, not statistical contingency or free payload; climate plus internal air alone exceeds a 5% margin and larger radius alone cannot fix it.

**Physical qualification:** open.

**Today:**

- payload reserve 5% of lift; total mass 95% of lift [CHECK-MAINLINE-09C5]
- 5% main and conservative; 0% optimistic [MAINLINE-009]
- payload 0 kg; +100 kg case supplied [MAINLINE-019]
- climate plus internal air alone: 5.7396% optimistic, 13.1183% conservative [MAINLINE-027]

**Needed:**

- Reword to state payload 5% and total mass 95% [CHECK-MAINLINE-09C5]
- Newer equal-margin geometry input [MAINLINE-009]
- Set payload and float reserve separately [MAINLINE-019]
- Specified residual reserve added to the budget [MAINLINE-019]

**Finding IDs:** N003, N056, N069, N080, N115, N196, N212

## R041 — Margin items

**Gap:** retained water and contamination

**Unknown:** Water films are equivalent retained thickness, not rainfall; absorbed core moisture, corrosion, thermal gradients and derating are unquantified; 320 K gas temperature is an acceptance condition.

**Physical qualification:** open.

**Today:**

- gas temperature at most 320 K (acceptance condition) [MAINLINE-019]

**Needed:**

- Measured water shedding, conditioning, absorbed moisture and thermal response [MAINLINE-019]
- Exterior humidity case and hull water rate [MAINLINE-024]

**Finding IDs:** N078, N094

## R042 — Margin items

**Gap:** systems and allowance masses are owner allowances (100 kg P2, 50 kg P3, pump, battery)

**Unknown:** Battery estimate assumes packaged energy density, usable fraction and conversion; catalog pump data are not installed duty measurements and the smaller pump misses the hot-gas flow.

**Physical qualification:** open.

**Today:**

- joint fraction 5%; systems 100 kg; residual gas zero [MAINLINE-007]
- 150 Wh/kg packaged, 80% usable, 90% conversion [MAINLINE-019]
- optimistic case retains 70 kg unused system allowance [MAINLINE-019]
- 100 kg system floor (70 kg above passive package); 0.1 kg/m2 sensitivity [MAINLINE-027]

**Needed:**

- A parts list [MAINLINE-007]
- Measured pump curve, power, cooling, conductance and duty cycle; qualified power package [MAINLINE-019]
- Explicit allocation of each needed item [MAINLINE-019]
- Itemised additional vehicle masses [MAINLINE-027]

**Finding IDs:** N035, N073, N079, N109, N145, N250, N260, N268

## R043 — Vacuum holding

**Gap:** getter capacity nitrogen air

**Unknown:** SAES offers room-temperature nitrogen sorption, so the blanket denial and unsourced N2 capacity band cannot support the mass result; all-air getter lifetime incl. noble gases is unsized.

**Physical qualification:** open.

**Today:**

- pump band 150-400 kg (catalog class) [MAINLINE-024]

**Needed:**

- Measured species loads, sorption speeds and capacities with activation conditions [MAINLINE-019]
- Getter capacity against gas load [MAINLINE-024]

**Finding IDs:** N076, N096

## R044 — Vacuum holding

**Gap:** vacuum-holding route mass and power (sealed service vs onboard pump)

**Unknown:** Holding internal pressure at a 1000 Pa ceiling needs a pump whose mass and power are uncertain and can exceed the float margin; the ceiling itself is an owner assumption.

**Physical qualification:** open.

**Today:**

- 46.3 L/s; 527-844 W; 150-400 kg pump set; commissioning pump-down 506 kWh [MAINLINE-016]
- pumps needed 1,3,7,23,103 at R 10,15,20,30,50 m [MAINLINE-027]
- 30 kg fixed [MAINLINE-027]
- perfect vacuum (zero residual) assumed [rpt-mainline-grok-estimates-card-1019]

**Needed:**

- Real Roots or screw pump spec at this duty; operational ceiling set from leak budget [MAINLINE-016]
- Measured leak/outgas and installed speed at pressure; measured gas-load decomposition [MAINLINE-027]
- 24 h hold demonstration at temperature envelope; supporting hardware mass [MAINLINE-027]
- State a hold pressure and the pump mass. [rpt-mainline-grok-estimates-card-1019]

**Finding IDs:** N060, N106, N107, N251

## R045 — Vacuum holding

**Gap:** whole-hull gas load: leaks, permeation, outgassing (needs measurement)

**Unknown:** Face permeation is negligible at the present budget; CFRP figure comes from a helium band divided by 50 for air and no measured air permeance exists.

**Physical qualification:** open.

**Today:**

- 0.5-3% moisture = 11.0-66.2 kg water = 347-2079 Pa vs 954.6 Pa ceiling [MAINLINE-016]
- budget equals 2.48 mm2 choked hole or 4.25 mm2 molecular aperture; 46.28 Pa m3/s [MAINLINE-016]
- CFRP 5.4e-5 percent of the 1%/day budget [MAINLINE-016]
- 30-50 kg passive package (estimate) [MAINLINE-019]

**Needed:**

- Water content of the core lot; bake-out and dry-gas backfill procedure [MAINLINE-016]
- Operational leak spec with margin; per-panel seam leak testing; sensitive pressure sensor [MAINLINE-016]
- Measured air permeance of the chosen face and seam coupon [MAINLINE-016]
- Measure gas load through a representative panel/valve assembly then the hull; Qref at most 40.71949 Pa m3/s for 24 h from 10 Pa [MAINLINE-019]

**Finding IDs:** N061, N062, N067, N070, N233

## R046 — Thermal

**Gap:** ground-side thermal environment

**Unknown:** Thermal balance averages sky and ground radiation; a hot apron, heat island or hangar is not bounded and the core-limit conclusion could invert.

**Physical qualification:** open.

**Today:**

- no-convection bound 313.5 K vs H35 limit 343-353 K [MAINLINE-016]

**Needed:**

- Re-run for named ground conditions; measure emissivity of the face finish [MAINLINE-016]

**Finding IDs:** N065

## R047 — Thermal

**Gap:** thermal mismatch, cycling and fatigue of bonded faces and joints

**Unknown:** Property loss at temperature is datasheet-class only; no derate curves pinned and daily-cycle fatigue of core and adhesive is unquantified.

**Physical qualification:** open.

**Today:**

- SiC 4.5e-6 vs PVC 60e-6 per K; shear 283 kPa per 30 K; SF 1.41-1.94 at 30 K, 0.71-0.97 at 60 K [MAINLINE-016]
- scored modes use room-temperature properties; H35 derates above 50-60 C [MAINLINE-016]

**Needed:**

- Bond-line and core shear coupon under daily thermal cycling; pinned H35 shear strength and modulus [MAINLINE-016]
- Derate curves for core and adhesive against the measured daily band [MAINLINE-016]
- effective CTE, temperature histories, restraint and fatigue under compressive mean load; test 10,958 daily cycles for 30 years [MAINLINE-020]
- CTE residual stress, polymer heat exposure, corrosion, fatigue, final weld/braze access [MAINLINE-028]

**Finding IDs:** N059, N066, N188, N239

## R048 — Handling, cost and supply

**Gap:** Be cost, supply and controlled processing

**Unknown:** Finished-sheet capacity, current S200F/SR200 prices and fabrication yields are unknown; the multipliers are owner stress cases.

**Physical qualification:** open.

**Today:**

- assumed S200F 4800-9600 USD/kg, SR200 9600-24000 USD/kg, yield 0.85-0.5 [MAINLINE-020]
- owner allowance 10 to 30 percent of conversion cost [MAINLINE-020]

**Needed:**

- grade/gauge/size-specific quotes, lead time, rolling capacity, scrap recovery, panel yield [MAINLINE-020]
- contractor quote pricing the conversion and capital separately [MAINLINE-020]

**Finding IDs:** N190, N191

## R049 — Handling, cost and supply

**Gap:** brittle face buildability SiC Be

**Unknown:** SiC and beryllium rank only on compressive membrane modes; flexure, fracture toughness, toxicity, joining and ductility are outside the formulas.

**Physical qualification:** open.

**Today:**

- SiC flexural strength about 380 MPa [MAINLINE-008]

**Needed:**

- fracture and joining assessment before either is carried as a face [MAINLINE-008]

**Finding IDs:** N134

## R050 — Handling, cost and supply

**Gap:** ground handling and dent survey

**Unknown:** Growth of diameter from 20 to 100 m raises ground area and wind force 25-fold and overturning moment 125-fold; point attachments, transport, launch and landing fall outside uniform-pressure modes.

**Physical qualification:** open.

**Today:**

- core-safe pad pressure target 250 kPa or less; hull 4645 kg [MAINLINE-016]
- diameter 20 to 100 m; wind force x25; overturning moment x125 [MAINLINE-027]

**Needed:**

- Cradle geometry, pad pressure and post-move imperfection survey [MAINLINE-016]
- Design and weigh handling and anchoring equipment; verify concentrated and asymmetric loads [MAINLINE-027]

**Finding IDs:** N064, N110

## R051 — P3 member force

**Gap:** P3 member force: pRs/(2*sqrt3) on the equilateral frame (FIX-A), two-way 2V-4 members

**Unknown:** P3 assumes tributary width equals spacing, pinned members, a real-valued equal triangulation, and ignores tube crippling; Euler pressure scales with I, E and 1/s^3.

**Physical qualification:** open.

**Today:**

- N = pRs/2; member-end load 974 kN at s 2.04 m (statics: 562 kN) [CHECK-011b]
- equilateral N = 562166 N at s 2.04 m (two-way 973701 N) [MAINLINE-023]

**Needed:**

- N = pRs/(2*sqrt3) on the equilateral frame, or a true two-way frame, then re-optimise [CHECK-011b]
- none; 022b rescales [MAINLINE-023]
- Integer geodesic, end fixity, imperfection knockdown and local crippling. [rpt-mainline-grok-estimates-card-1019]
- Integer mesh, end fixity and crippling. [MAINLINE-002]

**Finding IDs:** N018, N213, N247, N257

## R052 — P3 member force

**Gap:** P3 member shape: arcs vs straight chords, arc length

**Unknown:** Members are scored as spherical arcs with N=p*R*s/2; straight chords would give sag 0.1125 m and bending stress 2.1-3.2 GPa, reported outside the least-SF minimiser.

**Physical qualification:** open.

**Today:**

- chord sag 0.1125 m; bending 2.1065-3.1598 GPa [MAINLINE-11B]

**Needed:**

- See source fields.

**Finding IDs:** N309, N313

## R053 — P3 local buckling

**Gap:** P3 tube local buckling knockdown: SP-8007 gamma (FIX-B)

**Unknown:** Local buckling keeps gamma = 1 at r/t 140.5, while the cited NASA report's curve gives 0.529; local capacity at the SiC point falls to 0.648.

**Physical qualification:** open.

**Today:**

- gamma 1 at r/t 140.5 [CHECK-011b]
- gamma = 1 (classical 0.6 E tw/ro) [MAINLINE-011]

**Needed:**

- gamma 0.529 from the SP-8007 expression, then re-optimise [CHECK-011b]
- re-optimise ro under a knocked-down local curve; conclusion survives to gamma about 0.29 [MAINLINE-011]

**Finding IDs:** N019, N150

## R054 — P3 global lattice

**Gap:** lattice knockdown k (0.2 floor; Wright 1965's 0.4 and its meaning)

**Unknown:** Wright 1965 modified k 0.4 is applied to this card derived classical pressure, which may not match his Table 2 expression; thickness equation illegible; other sources gave no number.

**Physical qualification:** open.

**Today:**

- k = 0.4 used [CHECK-011b]
- k = 0.2 design; 0.5 band top [MAINLINE-11B]
- scored 0.2; Wright 0.4 (factor 2.0) [MAINLINE-022]

**Needed:**

- Wright 1965 Table 2 expression [CHECK-011b]
- Legible Wright thickness equation and expression. [MAINLINE-11B]

**Finding IDs:** N022, N307, N308, N360

## R055 — P3 global lattice

**Gap:** P3 continuum validity: smeared global mode vs member length (band s <= 3 m; buckle half-wave)

**Unknown:** Optima stay within s<=3 m where 011 judged the equal-triangle continuum defensible; the unconstrained run to s=6.4 m was not repeated.

**Physical qualification:** open.

**Today:**

- optimum cut at s <= 3.0 m (V >= 161 nodes) [MAINLINE-011]
- s <= 3 m [MAINLINE-11B]

**Needed:**

- re-run on real geodesic layouts if a design point is picked [MAINLINE-011]

**Finding IDs:** N149, N315

## R056 — P3 global lattice

**Gap:** P3 global lattice mode added and its coefficient (sqrt(3/2), Buchert 1968)

**Unknown:** Scored global pressure uses the equilateral continuum grid (nu 1/3); the brief two-way coefficient 4 is robotics arithmetic and a geodesic coefficient was not invented.

**Physical qualification:** open.

**Today:**

- coefficient 4*sqrt(3/2) on E*sqrt(I*A)/(s*R^2) [MAINLINE-11B]
- 009 estimate: about 0.70 perfect, 0.14-0.35 knocked down (6061 optimum) [MAINLINE-017]

**Needed:**

- equivalent-stiffened-shell general-instability check (ribbed-sphere analogy) [MAINLINE-011]
- A geodesic grid coefficient. [MAINLINE-11B]
- Score global lattice buckling and member bending (011b) before admitting SiC. [MAINLINE-017]

**Finding IDs:** N148, N306, N348

## R057 — P3 global lattice

**Gap:** two-way grid global coefficient 4 assumes isotropy; an unbraced two-way grid has no in-plane shear stiffness (022b's two-way rows rest on it)

**Unknown:** Whether a two-way grid without diagonals has any smeared global buckling capacity near 4*E*sqrt(I*A)/(s*R^2); the lattice sum gives C1212 = 0. 022b's two-way rows (Ti + Kapton 0.986, SiC 1.98) are governed by it.

**Physical qualification:** open.

**Today:**

- C = 4 (isotropic) [CHECK-011b]

**Needed:**

- a discrete buckling solve of the two-way frame, or diagonals [CHECK-011b]

**Finding IDs:** N023

## R058 — P3 Perry

**Gap:** P3 member imperfection: geometric Perry eta, brittle tube

**Unknown:** The P3 pass relies on SiC compression 3900 MPa and a metal-style Perry interaction; a 380 MPa screen gives only about 0.24-0.25. Compressive strength is not a bending allowable.

**Physical qualification:** open.

**Today:**

- 3900 MPa compression; 380 MPa screen gives SF about 0.24-0.25 over 10-50 m [MAINLINE-027]
- a0 = s/1000 [MAINLINE-11B]

**Needed:**

- Brittle tension/compression interaction, statistical size effect and joint eccentricity [MAINLINE-027]

**Finding IDs:** N112, N310

## R059 — P3 tube material

**Gap:** SiC tube density 3100 vs 3150

**Unknown:** Tube density kept at 3100 kg/m3 though sheet density is 3150; brazed-socket mass about 1.6 percent light.

**Physical qualification:** open.

**Today:**

- 3100 kg/m3 used; sheet 3150 kg/m3 [MAINLINE-023]

**Needed:**

- See source fields.

**Finding IDs:** N221

## R060 — P3 tube material

**Gap:** SiC tube design allowable: 3.9 GPa crush vs 380 MPa flexural vs Weibull; demand 0.82 GPa with FIX-A (025)

**Unknown:** SiC and T700 P3 values are 011 equal-mass swap properties from 008; SiC 3900 MPa is compressive, flexural about 380 MPa governs bending; 011 uses compressive sigma for member yield.

**Physical qualification:** open.

**Today:**

- service compression 1.428 GPa; imperfection adds +/-58.8 MPa; no tension [CHECK-011b]
- 3900 MPa crush allowable; flexural about 380 MPa [MAINLINE-011]
- flexural 380 MPa; compressive 3900 MPa scored; axial stress 824.7 MPa at 562.2 kN [MAINLINE-023]
- 3900 MPa crush primary; 380 MPa flexural [MAINLINE-11B]

**Needed:**

- Compressive design allowable (Weibull treatment) [CHECK-011b]
- a buildable-tube demonstration; row to be read as material-boundary only [MAINLINE-011]
- allowable owned by MAINLINE-025 [MAINLINE-023]
- Score member bending before admitting the SiC direction (011b). [MAINLINE-017]

**Finding IDs:** N021, N151, N220, N312, N352, N355, N356, N362

## R061 — P3 tube material

**Gap:** SiC tube manufacture at hull scale (025)

**Unknown:** P3 needs metre-scale curved thin-walled SiC tubes and a film at 1.5 GPa allowable; the opened supplier example is about 12 in long; not demonstrated products.

**Physical qualification:** open.

**Today:**

- supplier seal tube typically 12 in long [MAINLINE-027]
- design OD 281.9 mm, L 0.62 m, wall 0.216 mm; exists: OD 25-381 mm, single piece to 1.4 m, SiSiC wall about 2-4 mm [MAINLINE-022]

**Needed:**

- Tube and film manufacturing, joints, leaks, defects, proof loads and tolerances [MAINLINE-027]

**Finding IDs:** N111, N357

## R062 — P3 nodes and joints

**Gap:** P3 node and joint mass (5% assumed; 023 bill 31 to 859 kg)

**Unknown:** Joints carried at 5 percent (216.4 kg); a SiC pad bearing the member force gives bounds 1938-11620 kg; a 1 MN ceramic load introduction is not a catalog fitting.

**Physical qualification:** open.

**Today:**

- 20 g/node; joints 5% of tube mass [MAINLINE-027]
- node hardware 0.02 kg each [MAINLINE-011]
- 5 percent of tube mass [MAINLINE-11B]
- 216.4 kg allowance; bounds 1937.7-11619.8 kg; member force 295857 N [MAINLINE-022]

**Needed:**

- Nodes and film attachment sized from load paths [MAINLINE-027]
- real geodesic load paths and joint masses [MAINLINE-011]
- A measured fitting or parts list. [MAINLINE-11B]
- Joint mass owned by MAINLINE-023. [MAINLINE-022]

**Finding IDs:** N113, N153, N311, N358

## R063 — P3 nodes and joints

**Gap:** P3 node moment rigidity required by the smeared global mode

**Unknown:** Smeared bending stiffness assumes members continuous through nodes; pinned or soft nodes lower the global mode. Member torsion omitted (would add 11.8-13.7%).

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- Joints that carry member-end moments as well as axial force; check torsion-rigid case [CHECK-011b]

**Finding IDs:** N020

## R064 — P3 nodes and joints

**Gap:** P3 tube-end joint routes at about 0.5 MN (023: CFRP wrap, Ti, Invar, braze, pin, bond to SiC)

**Unknown:** The rough 0.5 kg fitting was the pin at the two-way force; at the equilateral force the pin is 0.202 kg and the wall still cannot bear it.

**Physical qualification:** open.

**Today:**

- 31.0 kg (0.015 kg per end) at 562.2 kN; 1470 MPa compression allowable [MAINLINE-023]
- 28.9 MPa lap shear at 25 C (anodized aluminium); bond 25.0 mm at 562.2 kN [MAINLINE-023]
- 157.7 kg (0.075 kg per end) at 562.2 kN, 0.70x the 225.5 kg allowance [MAINLINE-023]
- 858.6 kg (0.410 kg per end), 3.81x the allowance [MAINLINE-023]

**Needed:**

- compression coupon of the wrap bonded to SiC at the sized bond length [MAINLINE-023]
- lap shear on the real SiC surface at service temperature [MAINLINE-023]
- a higher allowable or a shorter bonded detail [MAINLINE-023]
- shear measurement on the tube diameter and a socket section [MAINLINE-023]

**Finding IDs:** N214, N215, N216, N217, N218, N219

## R065 — P3 film

**Gap:** fibre cross-ply membranes as film (Zylon, Dyneema): not a sourced film; resin, life, gas-tightness

**Unknown:** A uniaxial filament needs a 0/90 build for both pillow directions, doubling thickness; resin not included so a real laminate is heavier.

**Physical qualification:** open.

**Today:**

- 19 years at 60% of break (filament) [MAINLINE-024]
- total thickness = 2 x one-direction thickness [MAINLINE-024]
- 20% fraction; lives 15 and 250 years at 16 C (rope) [MAINLINE-024]

**Needed:**

- Laminate creep test [MAINLINE-024]
- Resin-inclusive laminate mass [MAINLINE-024]
- Film creep data [MAINLINE-024]
- Printed density [MAINLINE-024]

**Finding IDs:** N085, N086, N087, N088, N098

## R066 — P3 film

**Gap:** film barrier: permeation data and coatings

**Unknown:** Alumina barrier numbers are coupon measurements; coating a 1257 m2 hull was not opened. PROJECTION at hull scale.

**Physical qualification:** open.

**Today:**

- 1 atm oxygen assumed [MAINLINE-024]
- coupon-scale measurements [MAINLINE-024]

**Needed:**

- Stated test pressure [MAINLINE-024]
- N2 permeation for those films [MAINLINE-024]
- Hull-scale coating demonstration [MAINLINE-024]

**Finding IDs:** N092, N093, N095

## R067 — P3 film

**Gap:** film pillow radius assumption

**Unknown:** Pillow radius set to the bay side 2.04 m because that is the earlier film formula, not a measured cap.

**Physical qualification:** open.

**Today:**

- pillow radius 2.04 m [MAINLINE-024]

**Needed:**

- Measured pillow cap [MAINLINE-024]

**Finding IDs:** N083

## R068 — P3 film

**Gap:** P3 film allowable and design stress (1.5 GPa carried, no datasheet; Kapton, Teonex, Mylar today)

**Unknown:** Film allowable is an owner assumption with no datasheet; wrinkling, puncture, sag area and shear transfer are unmodelled, and it binds for SiC and CNT rows.

**Physical qualification:** open.

**Today:**

- film allowable 1.5 GPa (no datasheet) [CHECK-011b]
- 1.5 GPa, 80 um, 970 kg/m3 (pin) [MAINLINE-024]
- design stress = 0.5 x ultimate [MAINLINE-024]
- 210 MPa ultimate (thickest opened gauge, 250 um row) [MAINLINE-024]

**Needed:**

- A datasheet or test for the film allowable [CHECK-011b]
- A sourced film allowable [MAINLINE-024]
- Creep-rupture fraction for each film [MAINLINE-024]
- Data at design thickness [MAINLINE-024]

**Finding IDs:** N024, N082, N084, N089, N090, N091, N126, N152, N248, N258, N314, N359

## R069 — Tolerance maps

**Gap:** 015 tolerance map conventions (lambda, nu) and inversion range; Lee 2016 envelope (015b)

**Unknown:** Amplitudes at kd 0.5, 0.7 and 0.9 are lambda_I = 1 values; worst-width amplitudes are smaller, so the inverted table is optimistic in width.

**Physical qualification:** open.

**Today:**

- kd 0.3 ceiling below 197.052 mm (P2-E), 73.17 mm (014b Be), 39.05 mm (014 Be) [MAINLINE-015]
- least SF 0.6686 at kd 0.20; kd 0.2991 lifts only the global mode [MAINLINE-015]
- P2-E factor 1.82 (0.46 mm RMS allowance looser than 0.25 mm) [MAINLINE-015]
- ratio 293.1 on P2-E [MAINLINE-015]

**Needed:**

- digitised worst-width envelope at delta/t below 1 [MAINLINE-015]
- re-optimised split with kd 0.519 (face yield) for SF 1 [MAINLINE-015]
- none [MAINLINE-015]
- the min-over-width envelope [MAINLINE-015]

**Finding IDs:** N172, N173, N174, N175, N176, N178, N179, N183

## R070 — Tolerance maps

**Gap:** tolerance maps from monocoque shells transferred to sandwich (core shear, waviness, boundaries)

**Unknown:** Core shear cut to classical pressure is derived, but its cut to imperfection sensitivity has no coefficient; kd levels carry no shear correction.

**Physical qualification:** open.

**Today:**

- core shear cuts classical pressure 10.3, 7.0, 0.8 percent on P2-E at 9, 14, 138 MPa [MAINLINE-015]
- a locally 10 percent thin face costs 10.0 percent of P2-E classical pressure [MAINLINE-015]
- hydrostatic column 240 Pa, 0.25 percent of case pressure [MAINLINE-015]

**Needed:**

- a shear-flexible imperfection study [MAINLINE-015]
- autoclave and core-machining tolerances when the build is chosen [MAINLINE-015]
- a separate card for any equator the design keeps [MAINLINE-015]

**Finding IDs:** N180, N181, N184

## R071 — Geometry levers

**Gap:** geometry levers at equal margin (radius, altitude, partial vacuum)

**Unknown:** 11000 m is evaluated on the tropospheric lapse at the tropopause boundary; the isothermal stratosphere is not used; no effect inside this grid.

**Physical qualification:** open.

**Today:**

- 0.1 m core [MAINLINE-012]
- troposphere lapse at 11000 m [MAINLINE-012]

**Needed:**

- re-run levers with thickness re-solved at the float ceiling per radius [MAINLINE-010]
- re-run lever 1 on their best rows when filed [MAINLINE-010]
- A core thickness that scales with radius. [MAINLINE-012]
- Hold T at 216.65 K above 11000 m if climbing further. [MAINLINE-012]

**Finding IDs:** N144, N147, N319, N320

## R072 — Geometry levers

**Gap:** P3 member cap bounded continuation

**Unknown:** P3 re-optimisation holds bay 0.4-3 m and member radius at most 0.25 m, which governs large hulls; similarity rows hold 80 um film so film SF falls as 1/R.

**Physical qualification:** open.

**Today:**

- bay 0.4-3 m; member radius at most 0.25 m; film 80 um [MAINLINE-027]

**Needed:**

- Relaxed member caps or thicker film costed as separate designs [MAINLINE-027]

**Finding IDs:** N114

## R073 — Geometry levers

**Gap:** thin-shell validity at low density

**Unknown:** On the buckling split the core exceeds a tenth of the radius below about 1.8 kg/m3, so margins there are not physical.

**Physical qualification:** open.

**Today:**

- B-split core 1.81 m at 1 kg/m3, 18.1 m at 0.1 kg/m3 [MAINLINE-013]

**Needed:**

- thick-shell sandwich model with inner-surface area [MAINLINE-013]

**Finding IDs:** N165

## R074 — Metal strength transfer

**Gap:** face stress past yield elastic wrinkling

**Unknown:** The 6061 face exceeds its questionable 276 MPa yield on every row, so elastic wrinkling forms flatter it.

**Physical qualification:** open.

**Today:**

- face stress 3.57e8 to 7.09e8 Pa against 276 MPa [MAINLINE-013]

**Needed:**

- a face change (008b) or plasticity factors from CR-1457 section 9 [MAINLINE-013]

**Finding IDs:** N164

## R075 — Metal strength transfer

**Gap:** tensile yield used as the compressive allowable (aluminium and others)

**Unknown:** 276 MPa typical tensile yield is transferred to compression by owner assumption; source says typical values are not for design; no compressive yield was retrieved.

**Physical qualification:** open.

**Today:**

- 276 MPa tensile yield used in compression [MAINLINE-007]
- 276 MPa typical tensile yield used as compression [MAINLINE-005]
- tensile yields transferred to compression for four metals [MAINLINE-008]
- 276 MPa; all-face SF 0.7773844341284152 [CHECK-MAINLINE-007]

**Needed:**

- A compression yield or a design allowable [MAINLINE-007]
- a compressive design allowable [MAINLINE-005]
- measured compressive yield per temper and product form [MAINLINE-008]
- MMPDS allowables at about 285 K. [rpt-mainline-grok-estimates-card-1019]

**Finding IDs:** N028, N123, N133, N243, N253, N261, N274, N283, N287, N291, N294

## R076 — PROJECTION materials

**Gap:** CNT and graphene materials (PROJECTION)

**Unknown:** Cheapest P2 direction on all three leaders is lower face density alone, needing faces near 0.9-1.1 g/cc with CNT, Be and graphene E and sigma; all PROJECTION.

**Physical qualification:** open.

**Today:**

- lightest questionable face T700 at 1550 kg/m3 [MAINLINE-017]

**Needed:**

- Production allowable and thickness [MAINLINE-024]
- a demonstrated QI CNT-yarn or graphene laminate card [MAINLINE-008]
- Structural face at about 0.9-1.1 g/cc (959.5, 1129.7, 906.5 kg/m3) with those E and sigma. [MAINLINE-017]

**Finding IDs:** N097, N136, N350

## R077 — Method and provenance

**Gap:** 013 source quality (figure-read, second-hand, unopened sources)

**Unknown:** A list of paywalled sources was not opened, so none of their values is used; the stiffer ultralight ceramic octet point may be among them.

**Physical qualification:** open.

**Today:**

- 1.1 GPa and 10.2 MPa (secondary Jacobsen) [MAINLINE-013]
- read-off uncertainty about 25 to 50 percent [MAINLINE-013]

**Needed:**

- primary papers opened and values matched [MAINLINE-013]
- tabulated values from journal SI or theses [MAINLINE-013]
- obtain those texts and add values through build_cores.py [MAINLINE-013]

**Finding IDs:** N160, N161, N171

## R078 — Method and provenance

**Gap:** 1/least SF is not property multiple

**Unknown:** 1/least SF is the safety-factor gap and equals the property multiple only when the mode scales proportionally; wrinkling scales as a cube or square root.

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** N328, N345

## R079 — Method and provenance

**Gap:** documentation and provenance defects (no numeric effect)

**Unknown:** Owner caveats stand: volume ignores intrusion; joints 5% and systems 100 kg inherited; no sourced Gc/Ec core at 8-1 kg/m3; datasheet disagreements kept; microlattice 0.9 kg/m3 is density only.

**Physical qualification:** open.

**Today:**

- Notes say 12 um cell, N 20, rel. density 0.000104; table gives 8 um, N 10, 0.00182 [CHECK-MAINLINE-013]
- payload 0 kg both lines; 100 kg sensitivity [CHECK-019]
- 53 verified/measured pins in INPUTS [MAINLINE-027]
- RESULTS.json 59234 bytes filed vs 67862 observed; float021.py 31581 vs 36429 [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Needed:**

- Correct the notes field only [CHECK-MAINLINE-013]
- Correct text, pin 011 inputs, relabel two_way rows [CHECK-011b]
- Correct the id; state payload handling [CHECK-019]
- Normalised throughput, exact p/T climate calculation, variable-pressure integral; measured ground pump-down energy [MAINLINE-019]

**Finding IDs:** N010, N023, N026, N081, N116, N117, N140, N284, N293, N298, N317, N353

## R080 — Method and provenance

**Gap:** equal-mass separation convention

**Unknown:** Whether face separation should follow face thickness when face density changes at equal mass; effect is second order against 0.1-0.16 m cores.

**Physical qualification:** open.

**Today:**

- separation held at the row value [MAINLINE-005]
- at most 0.348 percent of SF_b on P2-E [MAINLINE-08B]

**Needed:**

- recompute E/rho with separation following tf for faces far from 2700 kg/m3 [MAINLINE-005]
- folds into any future exact recompute [MAINLINE-08B]

**Finding IDs:** N124, N141

## R081 — Method and provenance

**Gap:** omitted failure modes scope

**Unknown:** Core shear, wrinkling, crush, laminate anisotropy, bond and thermal stress are omitted; SF_b is a first-order thin-face scaling.

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- 005b for crush; later cards for shear, wrinkling, crippling [MAINLINE-005]
- MAINLINE-004 knockdown for kd rescaling and a sandwich failure check per candidate [MAINLINE-008]

**Finding IDs:** N127, N135

## R082 — Method and provenance

**Gap:** optimiser resolution and scope (grid vs continuous, splits, knees)

**Unknown:** General instability now includes transverse shear; the 007 thickness splits were not re-searched, which matters only for a named core whose Kc moves the equal-factor point.

**Physical qualification:** open.

**Today:**

- least SF 0.65041 (continuous balance 0.65041) [CHECK-MAINLINE-09C5]
- least SF 0.17502 (boundary limit 0.17503) [CHECK-MAINLINE-09C5]
- grid j/8000 [CHECK-MAINLINE-14B]
- grid 0.66865; continuous 0.66871 [CHECK-019]

**Needed:**

- Label as finite search result; refinement optional [CHECK-MAINLINE-09C5]
- Label as grid resolution [CHECK-MAINLINE-09C5]
- Label as grid optima; keep reported precision as computational precision [CHECK-MAINLINE-14B]
- The unstated core-fraction grid [CHECK-019]

**Finding IDs:** N005, N006, N017, N027, N037, N043, N254, N270, N286, N290, N301, N354

## R083 — Method and provenance

**Gap:** optimism factor comparison 021 vs frame

**Unknown:** MAINLINE-021 P2 reaches SF 1 with gamma 2.90x0.20 and wrinkling 1.10x0.33; this frame least equilateral SF 1.354 needs a largest named factor of 8 (arc rise); both questionable.

**Physical qualification:** open.

**Today:**

- P2 largest factor 2.90; frame largest 8; frame least SF 1.35387562843 [MAINLINE-022]

**Needed:**

- See source fields.

**Finding IDs:** N361

## R084 — Method and provenance

**Gap:** regressions recover filed points

**Unknown:** With dimpling off, Be S-200F on HRH-10-4.8-32 at kd 0.20 recovers the filed 014 least SF, thicknesses and modes.

**Physical qualification:** open.

**Today:**

- kd 0.20 [MAINLINE-14B]

**Needed:**

- See source fields.

**Finding IDs:** N316, N346

## R085 — Method and provenance

**Gap:** thin-wall section approximation P3

**Unknown:** Answered here: exact annuli used, and tw/ro at optima is thin; only the fixed ro = 0.02 comparison rows are thick.

**Physical qualification:** open.

**Today:**

- tw/ro = 0.175 on P3-A [MAINLINE-005]
- tw/ro 0.019-0.076 at optima; 0.175 to 0.38 at comparison rows [MAINLINE-011]

**Needed:**

- exact annulus A and I for a named candidate section [MAINLINE-005]
- none unless a family nears P3 feasibility [MAINLINE-08B]
- none for optima [MAINLINE-011]

**Finding IDs:** N125, N142, N154

## R086 — Other

**Gap:** mooring hardpoint load design

**Unknown:** Mooring hardpoint patch stress exceeds the questionable core allowable and snatch loads need dynamic analysis.

**Physical qualification:** open.

**Today:**

- design load 48.3 kN; bare patch 683 kPa vs 500 kPa allowable, SF 0.73 [MAINLINE-016]

**Needed:**

- Spreaders of at least 0.145 m2 per hardpoint; mooring dynamics with added mass [MAINLINE-016]

**Finding IDs:** N063

## R087 — Face sheet and panels

**Gap:** Finished minimum gauge, forming and strength retention

**Unknown:** Finished minimum gauge, forming and strength retention

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R088 — Wrinkling and core Ec

**Gap:** Waviness at the critical wavelength; metric and process transfer

**Unknown:** Waviness at the critical wavelength; metric and process transfer

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R089 — Thermal

**Gap:** Sun, bond reference temperature and additional pressure/load interaction

**Unknown:** Sun, bond reference temperature and additional pressure/load interaction

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R090 — Case and atmosphere

**Gap:** Terrain, weather, altitude floor/ceiling and passive equilibrium requirement

**Unknown:** Terrain, weather, altitude floor/ceiling and passive equilibrium requirement

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R091 — P3 local buckling

**Gap:** Tensile bending and coupled shell/column/curvature limits

**Unknown:** Tensile bending and coupled shell/column/curvature limits

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R092 — P3 nodes and joints

**Gap:** Discrete curved-member rolling mechanisms and restraint

**Unknown:** Discrete curved-member rolling mechanisms and restraint

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R093 — Grounding plan

**Gap:** Ordered evidence route and grounding of the current leads

**Unknown:** Ordered evidence route and grounding of the current leads

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R094 — Method and provenance

**Gap:** Snapshot completeness and pending follow-on filings

**Unknown:** Snapshot completeness and pending follow-on filings

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R095 — Native numerical evidence

**Gap:** Unresolved FE benchmark, load-control endpoints and excluded spectra

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R096 — Stiffened sandwich

**Gap:** Frame/bay adequacy, cap knockdown and coupled modes

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R097 — Build route and inspection

**Gap:** Full-blank forming, in-place seams, closure tooling and inspection

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R098 — Cure residual state

**Gap:** Stress-free temperature, cellular force balance and residual-stress stability

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R099 — Exterior finish

**Gap:** Installed coating mass, optical transfer and wet optical state

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R100 — Water and conditioning

**Gap:** Exterior retention versus absorbed material water and dry-out

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R101 — P2 local damage

**Gap:** Crushed-core dent growth, face damage and operating response

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R102 — P3 local damage

**Gap:** Member loss, brittle impact, merged bays and film tears

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R103 — P3 film life

**Gap:** Protected-film ageing, creep, loss budget and renewal

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R104 — Frame reliability and proof

**Gap:** Finished-member statistical scale, system risk and proof coverage

**Unknown:** 

**Physical qualification:** open.

**Today:**

- See source fields.

**Needed:**

- See source fields.

**Finding IDs:** 

## R105 — Mass growth and maturity

**Gap:** Mass growth and maturity

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Concept growth defeats every evaluated P2/P3 case; corrected direct-048 and coating-denominator values are carried by size.
- Direct 048 puts P2 R12 ISA at +1.256483 kg under the earlier TRL7 table; coating increment is divided by 1.1.
- Density witnesses and fixed-family P3 bound reproduce; all-density best-product ranking remains unresolved after REVIEW-A2.
- Sciences admits attributed targets; the original 061 process release is verified and later source replacement is not an owner fault.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-0d67fad3e120f6df3f39, E-bf13e3125ea0acfc0d25, E-a32cac7d88f77f68e580, E-ac994ee429aa9e303cf4, E-8fd681861aebe120736a, E-0dea2abb78cdfeb5c454, E-fe23e203943d68788328, E-c76166feb5f7c4b4f289, CHANGE-057, E-2be873981e30262329af, E-29d5fc987f188fc75d60, E-e321d720d2e00e9f22fc, E-4d23bda6def036a857c0, E-80f8288ce9949c09b3dc, E-46fe8e72c04503987f2d, E-91d8441ff6dd6a475302, E-ddea005d1701b130495e, E-afe5447bfadca02b0357, E-29ef9228442c3d432e70, E-9b3049e3f1648a8992b5, E-ef73e1f76c0645225953, E-6c94da5534de33d8657a, E-b1af1299c8866204be58, E-523abc46bf1c9f95775a, E-a154369d8046d977b814, CHANGE-check057, E-540c1c7dfc85c8776f6c, E-238b07250efd4113af27, E-ff5afbf0246c8040e453, E-abaa8821fc42d4addff4, E-3d7f7927caac867db538, E-a15fe476285660fecef8, E-9abdf56e5fb898b2e64c, E-ad72d8949b7a8196abdc, E-5788daa762eb9c224e3f, E-a5d017a757acabd2a000, E-a7441ff13cd9b89b6fb9, E-a25d17848813669dd660, E-f59d15060d618f7523d9, E-116218b57ee291bb3b0d, E-7756c2c4ea000d1dcb50, E-6a987933e3002b4afa00, E-0004ff89b71a66556375, E-0b66691ea79a4e57ebe2, E-1f63a9f18a12333593ce, E-c26747aaf03a38854623, E-0b0e07dedf0282106962, CHANGE-061, CHANGE-admit061

## R106 — Weather levers and complete-day coverage

**Gap:** Weather levers and complete-day coverage

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Relief and low-emittance finish widen conditional bands; REVIEW-A2's valve/bladder corrections lower the sampled day fractions.
- Dew uses actual night density; frozen geometry, thermal and gas conventions are explicitly separated.
- Convection and the 32-geometries-per-radius gas supplement are explicit; this is not an all-weather gas maximum.
- Displayed quantities and weather classifications reproduce; 680 marginal-cold knots are excluded and availability remains unknown.
- 160 frozen-thermal endpoints reproduce; R10 gas 102.491169 Pa/3.192390 kg and heater quadrature conventions resolve computational questions.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-c4f9dc424943c318e49a, E-8c12ee4d9b6a1859792e, E-1cc1660dc8e84e60093e, E-921721c1e6b5faa425f0, E-d92c0c89d8a71f7b905e, E-faf6025b057bfd9f952f, E-e5fae1e233fb75ace69f, E-d2d9ba656507cf910ec7, E-46ffb8f1a928a9969735, E-aa0cf8dff6fcb6ce66b3, E-78a2a83ec3cebc0aabaf, E-cb696d745818c07a7401, E-7b9d2b5c47457ca51a12, E-2482be056b9c856c3a07, E-94c30e5b1aa84f9359b8, E-941e935e19ae9dd58c04, E-0ba693aef788144ef23e, CHANGE-058, CHANGE-050notes, CHANGE-050gas, E-2539b8457cc9ed2e572a, E-5ef3649e9c6d31490c66, E-9d172a98ae37990954f2, E-4b3d3da1315f0b855bb7, E-4f2bb6c00c218320bb7f, E-4480458a03d40eb2d4ba, E-70eecb30e7f254c7653e, E-b2228ce04ba9fbba94e6, E-d7c6e78d6fa6ba9eeb99, E-019e559899ca77c5e372, E-0f167d2cefbb1f0a1536, E-1de2a8392a99cab60a70, E-72c84ed3df235e5053c1, E-6a9a13ff8e3d141ac4dd, E-2633f3df8a2d0d5460d2, E-dee3151791d363d77170, E-62bcfba35121a6bc8ac8, E-9fecf7b2b6a87b0902dc, E-ddee9edb1e917020f584, E-595254e0949a3cb2a580, E-b443668667e98016c729, E-bb563f6b245a39d23feb, E-6a45370cd543a14bc040, E-e73062c71360a3655c6e, E-e3eca157f44e9ed1a485, E-3b32addecff5b79673a0, E-f5d6cd77f0c76473560f, E-6a0b050508076e72f5fd, E-8efb3b44d2fc34b4bc25, E-f75279e45b4563aa0ed7, E-8d019a1838b3439129ad, E-50c674e4744c383bd0d0, E-435042f5079924934dfd, E-c84999d341962cedef91, E-eed25902b144eff0ca61, E-f58d3bc1dd6787fe8e82, E-402e1ed96185f83190a4, E-985d6cfe29c1f9228baa, E-d014920c8d56f5a96bfe, E-3e9c8c00c98a32563892, E-7d9bbd70bbbc3c566040, E-d4aa3522335e34ca28e3, E-7905a78dbfb28804e6c8, E-6c3cde18697acd8c2b9c, E-5ddcd4e9313f3cf71679, E-1cb8eebece5ba4e992ce, E-4372a2ef5e390841ba45, E-1d13a504291851ffd3c7, E-711a2181a75f733ed59c, E-24dcb65009093e3c41c6, E-6e4c23a90f6f52e06388, E-c53964d92a3010d7f1c5, E-d2e2a58851bfdae9eb48, E-f6dd227cccf05b1a8326, E-163b8f2b455770558c63, E-59748e101fa9bb6fff71, E-ff3aedf9425fbdbf0756, E-b080d178302b2b0444e2, E-87030cd0fd531e4fb5d6, E-75a9c23766397fd35149, E-ffef70bf718bc1c1c62c, E-1a91125e7a6cee813671, E-d76a198cbc0d5f67f6b1, E-ba81f4fed27c6fa7612e, E-8f1dedcbab1845cc1155, E-25d08d9bbf83c278fe09, E-646129587544607ab707, E-00694210ced8ef65da75, E-e39fde0615000d577b61, E-f5d7aaa47737c971a816, E-8d970f9335bd05893483, E-47f8f4f4875b6ab989ad, E-f76e2f3bbe8df167ff13, E-2059b332886149b43dba, E-a6409f7eca2982b53982, E-d5be09991c357adea357, E-b8c27ec1110deffb694b, E-c10e283b170ac479b3ae, E-77f9c1c5171c2b5ac77b, E-d2aee2f18f45904781c0, E-545618c7b0a8cce25e35, E-d41148ddecb13fe3db9b, E-0f84891e135bd4c266c2, E-b982ac9fbdf0b401179e, E-bbf4247c87a5dd352bf9, E-4986dbbf4938038ea7d2, E-74f2b389b04860c0208e, E-d83ee2f392d3e8ce4a16, E-22a36690d3be28812d7c, E-edd6e2f20abf5b33f900, E-ab9186799acef82c24e3, E-e1b9c722f3043a94c18c, E-42e8fd99628fe9823475, E-7246420ccfd7bff069de, E-8d3d0408288810dd1d9e, E-82bf5e97aac296bae30b, E-dc3b90689ac89cc37b34, E-9384c9ae53824e3748a2, E-a89c1918c429fda8750e, E-fa9fdc661408fb15f187, E-39166156983ac6932b83, E-1853e3e9e7870936a59a, E-2bb90e8f4e70b7d6bd3b, E-53eec33592f58010db02, E-75ba62fdca9db1334ce8, E-aa0afd698333a64be300, E-6d50a5e49911670d828c, E-44e5fa3dd76701205bc7, E-b936f9a7492023a2b313, E-2202c0ad5986a5a34034, E-59f011fb3108b4ae9718, E-73654c57794598b44676, E-519329c0a1a2c3366c09, E-e14689cfa0d0abc51c03, E-699701214ba64b77995e, E-83acf456882a6901db72, E-10075f8f10453d328e7a, E-b21c5d068be5a4c55e23, E-df4fbee28f0b2f311249, E-2a2c08d19dccfa4a0aee, E-816bd7969d6a87868a63, E-a5696cdad12e6f72b72c, E-1c95943dff8b317aaeca, CHANGE-check050, CHANGE-check050add

## R107 — Retained water and local drying

**Gap:** Retained water and local drying

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Carry CHECK-059's 99%-removal times, two-coat Ultra-Ever Dry bill and unreproduced P3 ponding; 0.1 kg/m² stays provisional.
- 99% removal takes .310–5.346 h under held weather; node/bay surrogate ponds differ, and two coats cost/mass twice the one-coat assumption.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-002c8c6414c844e6a07b, E-2a1475b8ab00de93a26e, E-7f737e14ed6ae33a35d9, E-09dd567431667a03f19a, E-0bb3d6e7264cd327542d, E-1c7b3a296f5bfaebed59, E-8751eaf1b318aa2f4c74, E-90072ba7e8ff0b0a8e8d, E-4bdee3d7c19bc7bdfb6a, E-8c828d2a3511d64f5dab, E-18155c04f3641b7e2a50, E-cb37a287b601e7e46852, CHANGE-059, E-c7fa7663bb0f63bca3ad, E-c9d8ce2d9746b9c0b0d5, E-7e91e8ceabc8a83b67c7, E-81403c8d762e90121693, E-b58668fcd65ec33bc8e4, E-781c3ac500971c59ef31, E-d9b2f72cf6cbe790a6af, E-8d132ca2a8803475051c, E-3cf00f2a42a067e7798e, E-e2bc741ecfb1022c276e, E-9fadcee722fa46975900, E-136673b469b23f4b0992, E-969aec92c59423e1e27a, E-b162f140d28a7f62eafc, E-c93ce168d4d939a23f4e, E-95dda7122b3a1a1d0d1a, E-4aba8539a765cff691a1, E-ab32312c7e87889dc39d, E-b0d85d1e9cbf9c8f4ca8, E-9910219e81d1aa15282f, E-1e64f268d8ed71163822, E-942cc3087b84465e1c1a, E-2d05da14fd107b6719db, E-69b2b7fab4c12d3d49bc, CHANGE-check059

## R108 — Dimple criterion, core law and test transfer

**Gap:** Dimple criterion, core law and test transfer

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Regularized-core model gives SF1/SF1.05 pass–fail dimples 1.209–1.227/0.738–0.756 mm; no physical tolerance is qualified.
- Three full-section 5 m cap tests cost an unquoted $0.420–1.558M; use corrected rig reach and direct limits from CHECK-055.
- 6.03 MPa is a published simulation, not a measured collapse; refined 6.159021 MPa releases no P2 gamma.
- Elastic endpoints reproduce but exceed core/face admissibility; inherited core loses ellipticity and the foam-law comparison is not empirical gamma.
- Independent direct estimates are 1.2179/.7469 mm; core regularization and compression allowables remain physical gaps.
- 5052-O rig reach is .575038/.856084; direct elastic/core/face limits are 5.7754/2.2998/1.2220 mm, with tooling and statistics gaps.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-d667b3a2b99e6f5816e6, E-58d12adc4662f4d1efa1, E-76f055c4c4ec0a828fa0, E-50810597f415b6de5f81, E-59977cd4cf8781aff1d6, E-d31dbaad88c980c997ec, E-126aba2389d591572fc2, E-450193a740b49dfd4f0e, E-453d433bf3e88ab6c7e6, E-b3aee6365cab8bffd239, E-a1cbde74bd2614d140fa, E-eaebb06fa64619ee5fa7, E-d5b6d31f59ec16d1ca4a, E-72e98f9b8825fb7cfba3, CHANGE-047, E-329f7b150a0857f282f7, E-02a927ee2db8da8a4d20, E-031b89d5341f8f6d7523, E-7d3eabc4528d59f27a71, E-5a214b75dc769ad5aa3c, E-af1eee80d887c590b1a6, E-03e5509f6bfdae5d33bc, E-bcea0323a80676dd5497, E-4c9caf02e9bba3db07b4, E-5de5a2556da0dd3f2804, E-39b19b1a1b6fa46038fd, E-0bdb297c19bb023a4c7d, CHANGE-055, E-da1e2379d2094f65212b, E-a28efd05a1120f2793ed, E-c14770c63421960e76fa, E-daeae473852466ec75bf, E-fd846ba83b58d4c48622, E-ab5ec5202603b9ecfcc0, E-b4dada3251ef66ac09ae, E-933db7f797ed51560343, E-47ccfb857233d2eb4924, E-7930cd4b9cf4501089cf, E-6e4be337e1ab03aace39, CHANGE-056, E-d321a173056e63ab4ff5, E-1175bc8f7b9af76718f0, E-2f271a9ec77bf4dff691, E-230652272530447d124e, E-bb8e9209d0901cd9d22e, E-e7fc560301f1a3234746, E-004194187aacbbc4a3a8, E-88da5aab6529e34d4a5b, E-724561ce0292000fb612, E-beeec292d62572312f38, E-701eee21e0734330773d, CHANGE-check029, E-e47ceeae86cf0b13975e, E-ea75636f6205cab68ba0, CHANGE-check047, E-de39e6768cf5cdd7827d, E-d6f7aa1a7e6b3f069073, E-5604ad2b0b2d50c54ebb, E-12e659a940f1847e35a9, E-3c42c8abfaace3d15719, E-431ac19e7e3cc6bab960, E-64ca2141ffbbaf787bc1, E-32567aa2be88bf55caaf, E-d4f62644c678a519cd03, E-7274aa7515c6b6286054, E-bf280fb81f73369d7eec, E-a4b290a849702cc46d6b, E-a0dbae5f36bbd11522ac, E-136db3d2533f05ae32c3, CHANGE-check055

## R109 — One-, seven- and thirty-day dry cavity

**Gap:** One-, seven- and thirty-day dry cavity

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- R10 ISA MET one-day payload is +30.710562 kg; SIOX/3A seven/thirty-day payload is +1.115544/−55.428312 kg before concept growth.
- One/seven/thirty-day screens reproduce; R12 ISA FOIL30 is +47.344558 kg, and installed service remains unqualified.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-57808de1e708b46b02d4, E-4cbf78fa82f0e6f7d410, E-00f7c546012814324889, E-741121a245ce88971ad2, E-f02a762faca26fecd4ad, E-0fe504a963441772fda5, E-e73b0234e0576ac68d83, E-105d44a30ab78876d881, E-231d858e9352bc4ce9f6, E-742a3c432c66ebe5b2ee, E-81eee6074c0f4e7bc0c5, E-252c247a93bf0ab34fc5, E-aa55d288d1578d3eb8dc, E-526f12c2a7bb2e6113be, E-00607ddcb4f5adb04d14, E-f2caa3e8504684147479, CHANGE-054, E-02997f6aed623a3d7383, E-a9561bdcf95550c54686, E-3df975058492c4177e88, E-9d216f8b4b9cbf16834b, E-88e1453b1eaf876192db, E-4f52f907a3d2897b9c49, E-237e0fab467d47321e12, E-6e98e121abcc229c4d9b, E-3def74ad1634a0f29fc4, E-1b604dff791bc074ded9, E-f7f1f432a1caa4cfdcf1, E-31604ad00e5e2260b6df, E-b9e9e764caf9bd0cb18b, E-baed4816ada87a4cf01f, E-3cda7898c8eac843c88c, E-743d956c80e743369ff1, E-5a464622cca950341c6c, E-cb8caa0f4e07403b7787, E-d5bed64cbb32c4190f20, E-6f016e6fa64069282660, E-171d1a0d157ecfdbb2eb, E-1f762981caa86e944d3d, E-8d5d68e9d0f328017e41, E-15a2c8df0ee74592c7e6, E-ce8c59ef8cdab2cb6e87, E-2111a9a62a74143ed168, E-3a261d066f390212ec91, E-7216bb39f0757a70cc64, E-56c62b7adeb3f4f7e8b2, E-ec87d8f39998cb20865c, E-4d29ffba1a52227384cd, E-2c97d2aeb8da063cf469, E-3785b21d522f3a3a97a4, E-00de9ca72712d18d4566, CHANGE-check054

## R110 — P3 material, full-member reliability and damage

**Gap:** P3 material, full-member reliability and damage

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Completed member/material, reliability, hail and damage tables replace the partial filing; hypothetical distributions remain unqualified.
- Carbon remains an alternative beside SiC, with no sourced-compression float; corrected axial load is about 701 kN.
- Main frame/reliability numbers reproduce; 336 shear labels and two Weibull inversions remain exact attributed corrections.
- 701 kN axial load and FE-normalized reliability walls correct the carbon table; the no-float screen survives.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-bd9d30e2113a7c8eb322, E-9da76afafeca54786047, E-a0cf1f3c3ceec6ae999b, E-78f5bf6e0ea0cc3de2e0, E-7bb7ba239829455d1a73, E-de078f71c83a952b32a3, E-6eb92f1b85562e18982d, E-ae67fa9c343442b9a7ee, E-cd118be5336020ba1fed, E-5bd5e5f7f2fbebdd6c72, E-044e75dd6b9ee9737f4e, E-370ea945aeba2306b02f, E-619a2e36f613fb979c8d, E-99fe03e0f6d94f4226e0, E-ec0134f4eecc4d1c3bc2, E-700fe9042af7c576b416, CHANGE-051, E-eca213fcb7014457d86b, E-03f4f15c669dd283f6e1, E-67245c7a064db04cb552, E-547427827814cc6113db, E-40130b37753703a52f8f, E-9d91ecea1b65d969cb7a, E-7994e1e64c1471023c67, E-a1c69df0b9f0dfce5833, E-5120de574956d9d9ea85, E-6137c6cfb25e60d9b8e1, E-1b5aa168444f6b705adf, E-38a0be8e6f6f6b121439, CHANGE-060, E-796852ca5d563ca8feb6, E-0eb90749933bbf52601b, E-6824c1d2de420c82a1bd, E-00e215be000575f2e962, E-b13f7ba7a474612bb9dc, E-dc549a2c7a2c0f68e2df, E-0bf9802453f031114592, E-f6e016f058fe40018b4a, E-4b9e7308cf3f185a9dc5, E-aedcfefbfc97bcfd9a73, E-30fcb3bee2d3988a5622, E-8856e58279fb08a8a5de, E-d2853d5c98dbbf9c0ce9, E-67fed28a03a0cecadf85, E-add2b5df142d5652d3e8, E-95dbed206bc0a85737a4, E-00e19a1c2fea6e6bb6bc, E-ef064afeb87e5499406f, E-9d82e15f85a21ee77c47, E-bab6615f9ea8e88214e8, E-51ba7657238bad866792, CHANGE-check051, E-08c4b8dcb40b9bced2ad, E-25c5402bfb2cd7e3e298, E-bd9ce7318493766b017e, E-47648a2e2bc54970c1b5, E-03badd9d8efa274357c1, E-28a45fa5ee8e20e4dee5, E-ba88ab55d50e6376e88a, E-3f579bdf2dc6f2fc71e3, E-59328165d638d217d5db, CHANGE-check060

## R111 — Thermal boundary settlement and common accounts

**Gap:** Thermal boundary settlement and common accounts

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Four thermal alternatives reproduce; maximum resized payload loss 4.388925 kg changes no endpoint float sign or least/tied set.
- Completed CHECK-048 is folded; convection/core-radiation conventions and finish-source corrections remain explicit.
- Complete independent accounts/searches replace partial status; SolarWhite 285 g/m²/.18/.89 and twelve null-field witnesses are carried.
- Owner boundary equations identify the natural-convection floor and core-radiation term; 053 resolves numerical, not physical, selection.
- 88,750 fields and 326 table cells reproduce; 288 f5-5 labels and 52.426 kg family difference are corrected.
- Four boundaries, all 5,760 endpoint grids and frozen scarf/global crossings reproduce; no installed boundary is selected.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-de0523a7be3ae20d8ed8, E-13050635972f9560e1a7, E-65628a908f734d71851c, E-d1a5f64209be540b337b, E-1148ea752d1f88d1f075, E-a5cc8c02c5826af910bf, E-458bad2aaeeef39da6a0, E-ca32d92c5ef4238b68c6, E-eac794c64a2156bc8a9b, E-47821062d7ba743dd6e9, E-1cb34d1c30d219bc2f41, CHANGE-053, E-5884de7a2af7eb46fd94, CHANGE-053fold, E-0c69def4fc6b5d335118, E-16808fd020245439c2f7, E-548318518c304b686679, E-970ce9b1d5440d423a23, E-9e21205be7aa141f3ecf, E-0bd10c0f8ab26a8e93fd, E-b291f501cd18ae32f6f7, E-732b8da8d9c92706879e, E-a73b44bc414669cdf7ad, E-fd978ace0869b6ddd544, E-96820570343bb1756e85, E-300eacef7e78461113fc, E-087c7cd7cd17b1c12670, E-60af0b07ac08195bc5eb, E-e040da0848ddd069241f, E-aea0b40d7707fd8fd2f4, E-0f3342534384a255e6ec, CHANGE-check048, CHANGE-check048boundary, E-74f4493723fd95e8d3ce, E-68d400837bb4e8d64d76, E-e6cdfed4dedaf71ef354, E-8ffd9e97f3b7efd72088, E-1c5cc64e88c6a0e20797, E-71a7665c2bb109721956, E-5d1cdf45733a5dd2484a, E-99d3a16969c9d6e5d845, E-03a3d7106a2e47443730, E-89443104aa2a00222acc, E-8a0621cd638b4acebf42, E-8071c9e6e69adec2c4fa, E-363cd33eb84fb39fe4c7, E-962d8eb5796a205e6347, E-acbb5e5a3728b854d192, E-de8a974152d1b0bb0dd1, E-d16925b01957eb12e54c, E-dfbe62fa7b769c30c32f, E-5b095c1a1452c678d86b, E-20fa6ef05951df0bc6bb, E-86bb850565a4b3d37b70, E-d90b3808148abb18871f, E-d0b9a76e12af30c644b6, E-31c47907bbbb31b74018, E-049c3937fc5953aff12b, E-16bbc0395b5c9df8f38f, E-b39859004aa2da304a22, E-ca4fa6626c2ae0dfc3db, E-d49b0c87256982cc987e, E-2c93d59d25d0cc352814, E-6962d01c17e3899d8c1c, E-77c4564e368023455392, E-cf82ab058c4981e988e4, E-8305e37884a8a71ed324, E-32cd88280d774ff19168, E-5797b25bc37c6b3bfbbf, E-bc0754da95d7db11d291, E-b1c1eb3994ec4931e96e, E-1f15dfa8998cc6a75354, E-f8315068fcd98561777b, E-caf0a5a0272abe43d923, E-31622e1cb4d3be3eab6d, E-6c36750f308029641562, E-a471bb51c6e3daf0ac5f, E-46b3e28b8f2170c616f6, E-205d61b6ac162b5b7228, E-c5ed4e61ba09b0af1ec0, E-c7e1306c2d7b1fa7c876, E-f9f0c6e35e59c4ffa87a, E-7e002c1eb7b9dc18b8d1, E-82f2e4f823c4b77a3af6, E-a17785cdd687a08e5897, E-6f6e8d373fcddcc21852, E-be0b8908206ba3ffabdf, E-09943c0bf5e7c431a397, E-af5d993cb6dd9603dd92, E-4b7914a4d31fc2bebc99, E-888c4ac06212038ae1a4, E-cd8205664b450f1b90ea, E-e7f5c8dba5ca016430b9, E-491ed4fde7effbfc4669, E-43072261af90ccbdd447, E-b66253cce8c55c761a13, E-043a9a41d9e1c9a466d2, E-e43899d22bdc34fac64a, E-77602a0372f6570a5b4a, E-dbee08ef7cb0a268e1a3, E-cec1b8a3d633c2aa4ce7, E-214ed5a592a0ecdaa927, E-bb98a48991a1e09c6cd8, E-f9cee5dbaf283317cc94, E-00954e9e2de3a646f1fe, E-e7f7975fb2a19850ba3b, E-61c1e1b65df785f88b3c, E-3eab7164eaa28a0f8efe, E-b54d292c6cfa6c45c0f9, E-dbee7ff8b776da177d4b, E-856d381ce436a7821ae1, E-c1b93857281bdc7e9985, E-6ca114014ad12b205121, E-8f0d887844a9d19e2a83, E-50b1a0c7605cda00e271, E-3661370629260f7083c2, E-663e5d3ef9f28897d66f, E-ddca892117077eb2c237, E-62f2b34fc9f1f9e9eeda, E-20e5d3bd751e5b23244e, E-fabb803fad12175f0b1c, E-06dd799ac417962075e7, E-e784a8f73d2a5e92097d, E-faf7cc0b5444bf7f38ee, E-d57e2d0a9436217b13cc, E-62f856789421aa60b5de, E-e940c61ad8ef1d1b00fe, E-5aadc20323a1b358fb72, E-8f56e31cac8ab84de194, E-a48636b09f7c5e3d3677, E-8f1dd9943d070c2356ec, E-7dc3815091be96fea5c0, E-a1c4c78838eadea31c73, E-9add56f0896928e3d852, E-e5ff08ab4c2fe1d8c7c7, E-1ae483d685de3d6a7e41, E-cc2548160dddc138b28f, E-32577eda97b88c934a5a, E-0bc17c15168d6d13f187, E-fe472ef4148230e9ea3e, E-7a16fff1f3830d25ca59, E-914e07b29455d218f583, E-6c412b3bbd3ddfa3de20, E-6ea0f9fd3d61b2f54743, E-5804d23012f8782e6695, E-6d408fca0f057a89701b, E-21477dfa0a7685daf114, E-2266daa22b672145c41f, E-7110bbc20dff04963b97, E-cfab341b3f70a95fd7be, E-577c7fd5412c234834e0, E-13945e0cf2955ecfa0c0, E-570aa4619bc4abd83e23, E-caa9e703ecd9e7d0bae1, E-b6a6bbe475b598dc1f3d, E-13f480bb18432165b376, E-7158207c45009835da9d, E-2140aab4b1abb26b78d6, E-e953919c2ae2de883903, E-7a62110ba246b717ca9f, E-8398a5d79e4f95e6a327, E-ed22c97357aafaa4c98e, E-6374ce846f9a3262c52f, E-418c66055097ce59f810, E-cf33741a7c9c153e1422, E-5abab6d717828a986bf5, E-4f757441f0904c25df7a, E-85c386904270728f5b3f, E-51a01eb3964a64746055, E-0e6c162498145cbf24f4, E-2ce04231a96f9e5470cb, E-b35c1a79c67605a3d4b4, E-0e5d22f8a0e94f252cb4, E-cb1aa7ea4289f87ad69f, E-d395b9921624795c7590, E-0bcb65b8bab3f4a5d802, E-3901e6fd0d0f3daf95fb, E-d9f91dcdc7e46c1d4cd4, E-9f27ac3d98fb873db7b0, E-3afa18ced4a9eb0a8377, E-3e025515716e7abb51b7, E-523897569b964481e67e, E-c3f3d1ed83f3b017ab75, E-bf27d1d10a2a0b898f12, E-39cdfc2c73eaf5645789, E-7250479fbcad79ca6386, E-27f87b2e9280870d71b8, E-18a26800ed6edd1c9ed5, E-286992ef8b687998d385, E-402d50adb8c163d50730, E-4e8fec21955de5cdd5a1, E-948193b18bf6d51fe00f, E-1c54dfcb7ceb800c5dcd, E-fa014dc8291b3ada5876, E-b334e76e9b49f74a34e7, E-cf510be7782ae3fce3c8, E-bd0e126bf3301a8b32b3, E-9ad6bbb6ae96ef442326, E-c281be47bcf12b6cd8e9, E-3ca08d24813322146db2, E-e27616c3ffbfba075a66, E-a14540c57972b9941bae, E-cf2db464c591977702c4, E-d7050849b820a9cc4126, E-74d8b14be7d6fb384b9b, E-c4beee700ed24c9a55a4, E-128818cd5a2bda418591, E-6a58e5d51bc59652c0b6, E-636e72ce49fcc0ef75e8, E-41154db4166699f89d57, E-cd75fbd481881b271e74, E-055f612bfbbf6b5940ee, E-d96cda369da25db4228d, E-cbeff196ac6fb7837f3d, E-180fd2959c95e8b75c9b, E-bbf96d3786c30df21d2e, E-0f3723fc6f68a7a43148, E-180ab1176df0f0db7eea, E-c940377adb98809f808d, E-42ac8ef6107602bd47e4, E-b69cc6ca0fb795cee945, E-4516a847876fecabb178, E-d13cbc79bccc7f44d12f, E-105ec18aa42397e961fb, E-188434f7bf109759f737, E-b9eeacfe2585006abf29, E-17d34a1fc02160152c07, E-e6a516e83a88cdf1bd53, E-27c476264cbeae5fd597, E-8d7fcda0ef939995cfd3, E-ab68a23b113ad1e8d5b3, E-6d4b7788af0e7313ec6b, E-5ee5ee256ed20e988865, E-0d10f09b97c365cd9071, E-efe1c3cbe193af1fb470, E-7165a4f86eafe4a78292, E-229822db9ee781297978, E-b1313891aabf5cf2ee0d, E-7b054f61e026b74ede29, E-f85de2827cea5d88d36d, E-21af9686b52b1ee687ea, E-66b5e09fc6c0966fdd7c, E-e8a9a8a77d55381d3016, E-3251751ad1a8f7885fb9, E-4d32217084efb0aa431d, CHANGE-check052, E-76203e1d44a5b9f2c93a, E-1fa3eb7d5d1a921e637a, E-326f5d54d3472e4a4ee7, E-d203d19a04415115f65a, E-2d438c896cca1dcd2772, E-42d008b71fc41a2b29a7, E-e781873619aa901750f1, E-01ab71c3226c70418685, E-5055a94525aa10624a7a, E-581154a18e0f61ba6f3f, E-3a25f5905733225f935a, E-ac7c45ed0723052d9274, E-a007d0995801efe6c786, E-3d9f82001816c6c5bd46, E-4f17d99c849227bd0ee9, E-178e21dfe0d98cb9311c, E-25c666eea1ca652d6c27, CHANGE-check053

## R112 — Beryllium-free P2 screen

**Gap:** Beryllium-free P2 screen

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Sourced Be-free faces do not float; the 60% Vf projection needs CHECK-049's consistent mixture and reoptimization.
- 60% Vf requires 1800 kg/m³ and fibre fraction .733333; R30 ISA reoptimized usage .783530/endpoint +12.444 t remains a projection.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-1e0a8d07cb580b6b121a, E-610df459d6dab4fbc508, E-c82738045af2a41b93d9, E-d7f03217dd50f080aa90, E-1db8807349225f6624ef, E-78a73c09af3deebd6d2e, E-9e101e6048787255ffd7, E-0dae8e49e94ebe63aff7, E-326b9b355a4b6157fe80, E-934f1ea225421e01273f, E-81dd4e368e8d14d24cd7, E-b8f27df86d6a4e7268dd, E-9145dff635e958928f43, E-3344f019e07f9a8bbb51, E-33aebab6584ca5a7a051, E-f40c98c80ee1ac6d702f, E-0774730f4ce7ccb87ce3, CHANGE-049, E-4779059a1cf8c16a29a4, E-643e1e32cdd74961fa8a, E-b8114040cb2020a72285, E-6d82a4cc7f4d4aa89ba0, E-1dff5cd276c8070a839d, E-5079dbb9c53be5d9530e, E-66511a50319ddba54521, E-0496704a5a0daf06096d, CHANGE-check049

## R113 — Buildable shape, stock, costs and whole bills

**Gap:** Buildable shape, stock, costs and whole bills

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- Model-only SF1.05 amplitudes .793/1.628/2.486 mm and unquoted costs reproduce; six coating corrections remain UNREVIEWED.
- Sciences admits the conditional shape/cost account; no buildable floating P2 or qualified cheapest route is established.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-c37a86ac2149571405d4, E-839974c356856359826a, E-8fc8b4c6ceb816e051b3, E-cc219b09effa13dc88b8, E-1ad869c55a584f037f42, E-fa6b1e657d8dc1e025e8, E-1875ebfa6462bdafc0ec, E-636e78acdd2bb3435f01, E-214b20d5efd66182de3e, E-908a7cab973402aebc38, E-cc22d883186653669a4d, E-bda502d6ba1087246531, E-93b1bd14e806a5d53da6, E-2be46f6ae8da09404f8a, E-da287cd4cd142c49352e, E-8bf0899227c6ddaaa337, E-c3594ac148bf9af7f6b1, E-c126d1d213329e33873a, CHANGE-062, CHANGE-admit062

## R114 — Piece A independent review and unreviewed fixes

**Gap:** Piece A independent review and unreviewed fixes

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- 16/17 claims reproduce conditionally; six unreviewed coating field corrections preserve all negative payload signs.
- 13/17 reproduce, two differ, two need evidence; two hardware-fix groups are UNREVIEWED and radius/product rankings remain open.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-16858c52b922d570982d, E-6d7745837e92b9c45b31, E-19f8532ddffdfbd595a8, E-575231e60d1abf25195b, E-f569f05f6bc4442ed8af, E-3ccd41fc1539fd022250, E-09389cb70e547396ab16, E-a00201776943dbaa468e, E-7d8b9d4b65049917f7d9, E-c8f1924a6a455c162ddf, E-e6bd4661d525676bbbe5, CHANGE-reviewA1, A1-01, A1-02, A1-03, A1-04, A1-05, A1-06, A1-07, A1-08, A1-09, A1-10, A1-11, A1-12, A1-13, A1-14, A1-15, A1-16, A1-17, FIX-A1-062-COATING-R10-ISA, FIX-A1-062-COATING-R10-optimistic, FIX-A1-062-COATING-R20-ISA, FIX-A1-062-COATING-R20-optimistic, FIX-A1-062-COATING-R30-ISA, FIX-A1-062-COATING-R30-optimistic, E-6e01cd8bfe7db9ea98ee, E-084abb79dbf55068e7c0, E-be20ad4b8bd0fc864581, E-a1b16dd91eb6faa8e008, E-56389f7851955668e816, E-036ac0a8505c887c4d6a, E-8e820ac8dec3ac1752db, CHANGE-reviewA2, A2-01, A2-02, A2-03, A2-04, A2-05, A2-06, A2-07, A2-08, A2-09, A2-10, A2-11, A2-12, A2-13, A2-14, A2-15, A2-16, A2-17, F-A2-058-P2-HARDWARE, F-A2-058-P3-HARDWARE

## R115 — Stable incremental record and qualification

**Gap:** Stable incremental record and qualification

**Unknown:** See individual claims and separate qualification column

**Physical qualification:** open.

**Today:**

- 550 checked numbers stand; all ten wording items and 22 joined/broken-token occurrences are corrected in the annotated historical card.
- Sciences' six-row confidence table is carried as qualification; numerical reproduction does not establish installed performance.

**Needed:**

- Resolve source/test questions without treating numerical agreement as physical qualification

**Finding IDs:** E-16d6e383001c41a7d6e8, E-6d8a1ba7ec5d8e7d6f39, E-1f93c2092b39bdfc758a, E-41dface83514a86ff15b, CHANGE-check030d, CHANGE-processreview

## R116 — 058 relief sizing: whole hardware bill and band

**Gap:** 058 relief sizing: whole hardware bill and band

**Unknown:** Installed qualification remains open

**Physical qualification:** open.

**Today:**

- R10/R30 P2 hull mass changes −225.219/−6174.518 kg before complete hardware; hot-edge gains 11.9209/12.0257 K reproduce. The whole-bill MLCCAg R10 case adds 11.444985 kg hardware. A2 corrects day fractions; hardware/trajectory qualification stays open.

**Needed:**

- See source fields.

**Finding IDs:** E-CURRENT-RELIEF

## R117 — 058 low-emittance finish: mass and band

**Gap:** 058 low-emittance finish: mass and band

**Unknown:** Installed qualification remains open

**Physical qualification:** open.

**Today:**

- AlAOC epsilon .05 moves the R10 cold edge about 11.1 K. With complete hardware, the cited P2 R10/R30 bands are 25.7277/34.6262 K; see the exact mass/band rows. Source optics do not qualify an installed Be finish.

**Needed:**

- See source fields.

**Finding IDs:** E-CURRENT-FINISH

## R118 — 060 carbon alternative beside the SiC frame

**Gap:** 060 carbon alternative beside the SiC frame

**Unknown:** Installed qualification remains open

**Physical qualification:** open.

**Today:**

- Carbon has no sourced-compression float in the assessed family; CHECK-060 corrects axial load to about 701 kN and the reliability-normalized mass rows. SiC's favorable mechanical/reliability screens remain hypothetical, not qualified material performance.

**Needed:**

- See source fields.

**Finding IDs:** E-CURRENT-CARBON
