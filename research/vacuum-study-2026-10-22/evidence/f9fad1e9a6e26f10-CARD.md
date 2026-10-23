# MAINLINE-008 material gap table - ESTIMATE_PENDING_CHECKER

Unit vacuum-mainline008-material-gap-1019. Order ord-admiral-rr2-mainline008-dispatch-1019. Nothing here is a certification.

Case: evacuated sphere, external radius 10 m, 500 m ISA, external pressure 95460.8379139 Pa, lift mass 4889.44215019 kg. Rows P2-A (MAINLINE-002) and P2-C, P2-K, P2-E (MAINLINE-003), all at kd 0.2 with 6061-T6 faces. Every buckling safety factor scales linearly with kd, so MAINLINE-004's knockdown rescales each buckling column by one multiplication (required E scales as 1/kd).

Method: each candidate replaces 6061-T6 at equal face mass, so its face thickness is the row's aluminium thickness times 2700 divided by its density; core, separation, joints and systems stay at the pinned row. Face thickness is much smaller than the separation in every row (worst tf/d in the table is 0.00722), so to first order SF_b = SF_b,Al x (E/rho)/(E/rho)_Al and SF_y = SF_y,Al x (sigma_c/rho)/(sigma_c/rho)_Al. Gap is 1/min(SF_b, SF_y). Composites use quasi-isotropic laminate properties, never fibre properties. Every sourced value is QUESTIONABLE; CNT-yarn and graphene rows are PROJECTION.

Aluminium row safety factors used: P2-A: SF_b 0.230789, SF_y 0.434719, tf 0.37589 mm; P2-C: SF_b 0.195203, SF_y 0.231299, tf 0.2 mm; P2-K: SF_b 0.224864, SF_y 0.313274, tf 0.27088 mm; P2-E: SF_b 0.233886, SF_y 0.388692, tf 0.33609 mm.

## Rank 1 - SiC (monolithic alpha SiC, Hexoloy SA type) [QUESTIONABLE]

Density 3100 kg/m3, E 410 GPa, compressive strength 3900 MPa. Basis: measured compressive strength of sintered SiC; flexural strength is only ~380 MPa and governs any bending/tension path (NFI). Source: Saint-Gobain Hexoloy SA data https://www.ceramicsrefractories.saint-gobain.com/pt/files/4731/view (compressive 3900 MPa, flexural 380 MPa); MatWeb alpha SiC https://www.matweb.com/search/datasheet_print.aspx?matguid=dd2598e783ba4457845586b58c8ea9fb (density 3.10 g/cc, E 410 GPa).
Figures: E/rho 132.26 GPa per g/cc, sigma_c/rho 1258.1 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 1.196, SF_y 5.35, least 1.196, gap 0.836; P2-C: SF_b 1.012, SF_y 2.847, least 1.012, gap 0.9884; P2-K: SF_b 1.165, SF_y 3.856, least 1.165, gap 0.8581; P2-E: SF_b 1.212, SF_y 4.784, least 1.212, gap 0.825.
In P2-E the limiting figure is E/rho; gap 0.825. Face thickness in P2-E at equal mass: 0.2927 mm.

## Rank 2 - CNT-yarn composite quasi-isotropic [PROJECTION]

Density 1400 kg/m3, E 180 GPa, compressive strength 1200 MPa. Basis: PROJECTION scenario: QI laminate retaining ~50% of reported UD CNT-laminate specific modulus and a compressive strength below its reported UD tensile specific strength; no such QI structural laminate is available today. Source: PROJECTION from UD CNT-yarn laminate report https://chemrxiv.org/engage/chemrxiv/article-details/639c91d7e8047a61d0eb2d2f (specific modulus 256 GPa per g/cc, specific tensile strength 1.71 GPa per g/cc, unidirectional).
Figures: E/rho 128.57 GPa per g/cc, sigma_c/rho 857.14 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 1.163, SF_y 3.645, least 1.163, gap 0.86; P2-C: SF_b 0.9835, SF_y 1.939, least 0.9835, gap 1.017; P2-K: SF_b 1.133, SF_y 2.627, least 1.133, gap 0.8827; P2-E: SF_b 1.178, SF_y 3.259, least 1.178, gap 0.8486.
In P2-E the limiting figure is E/rho; gap 0.8486. Face thickness in P2-E at equal mass: 0.6482 mm.

## Rank 3 - Graphene composite quasi-isotropic [PROJECTION]

Density 1500 kg/m3, E 150 GPa, compressive strength 900 MPa. Basis: PROJECTION scenario: graphene-reinforced laminate at a small fraction of monolayer graphene properties (E ~1 TPa); no structural graphene QI laminate is available today. Source: PROJECTION; monolayer basis in Lee et al., Science 2008 (graphene E ~1.0 TPa, DOI 10.1126/science.1157996) and graphene-reinforced carbon fibre https://www.science.org/doi/10.1126/sciadv.aaz4191.
Figures: E/rho 100 GPa per g/cc, sigma_c/rho 600 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.9044, SF_y 2.552, least 0.9044, gap 1.106; P2-C: SF_b 0.7649, SF_y 1.358, least 0.7649, gap 1.307; P2-K: SF_b 0.8812, SF_y 1.839, least 0.8812, gap 1.135; P2-E: SF_b 0.9165, SF_y 2.281, least 0.9165, gap 1.091.
In P2-E the limiting figure is E/rho; gap 1.091. Face thickness in P2-E at equal mass: 0.605 mm.

## Rank 4 - CFRP quasi-isotropic M55J/epoxy [QUESTIONABLE]

Density 1640 kg/m3, E 135 GPa, compressive strength 350 MPa. Basis: QI laminate estimate: UD E ~ 325 GPa (Vf 0.6 rule of mixtures on 540 GPa fibre), E_QI ~ 0.42 x UD; sigma_c_QI ~ 0.35 x estimated UD compressive strength; not fibre properties. Source: Toray M55J data sheet https://www.toraycma.com/wp-content/uploads/M55J-Technical-Data-Sheet-1.pdf.pdf (fibre 540 GPa, 1.93 g/cc in Toray carbon-fibre card); QI reduction stated in sigma_c_basis.
Figures: E/rho 82.317 GPa per g/cc, sigma_c/rho 213.41 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.7445, SF_y 0.9076, least 0.7445, gap 1.343; P2-C: SF_b 0.6297, SF_y 0.4829, least 0.4829, gap 2.071; P2-K: SF_b 0.7254, SF_y 0.654, least 0.654, gap 1.529; P2-E: SF_b 0.7545, SF_y 0.8115, least 0.7545, gap 1.325.
In P2-E the limiting figure is E/rho; gap 1.325. Face thickness in P2-E at equal mass: 0.5533 mm.

## Rank 5 - Beryllium S-200F [QUESTIONABLE]

Density 1850 kg/m3, E 303 GPa, compressive strength 283 MPa. Basis: compressive yield 41 ksi = 283 MPa (tensile yield 37 ksi on the same page). Source: Materion beryllium data sheet https://hkvxni.files.cmp.optimizely.com/download/c3141b9ea04211ee9a7b2a5d2cb825d4 (S-200F density 1.85 g/cc, E 303 GPa); Brush/Materion Beryllium Guide MB-001 compressive-yield note.
Figures: E/rho 163.78 GPa per g/cc, sigma_c/rho 152.97 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 1.481, SF_y 0.6505, least 0.6505, gap 1.537; P2-C: SF_b 1.253, SF_y 0.3461, least 0.3461, gap 2.889; P2-K: SF_b 1.443, SF_y 0.4688, least 0.4688, gap 2.133; P2-E: SF_b 1.501, SF_y 0.5817, least 0.5817, gap 1.719.
In P2-E the limiting figure is sigma_c/rho; gap 1.719. Face thickness in P2-E at equal mass: 0.4905 mm.

## Rank 6 - CFRP quasi-isotropic K13D2U pitch/epoxy [QUESTIONABLE]

Density 1750 kg/m3, E 210 GPa, compressive strength 220 MPa. Basis: QI laminate estimate: UD E ~ 515 GPa (Vf 0.55 rule of mixtures on 935 GPa fibre), E_QI ~ 0.41 x UD; sigma_c_QI low, pitch high-modulus laminates are compression-weak; not fibre properties. Source: Mitsubishi Chemical K13D2U tow data https://www.m-chemical.co.jp/carbon-fiber/en/product/tow/ (935 GPa, 3.70 GPa, 2.20 g/cc); QI reduction stated in sigma_c_basis.
Figures: E/rho 120 GPa per g/cc, sigma_c/rho 125.71 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 1.085, SF_y 0.5346, least 0.5346, gap 1.87; P2-C: SF_b 0.9179, SF_y 0.2845, least 0.2845, gap 3.515; P2-K: SF_b 1.057, SF_y 0.3853, least 0.3853, gap 2.596; P2-E: SF_b 1.1, SF_y 0.478, least 0.478, gap 2.092.
In P2-E the limiting figure is sigma_c/rho; gap 2.092. Face thickness in P2-E at equal mass: 0.5185 mm.

## Rank 7 - Boron/epoxy quasi-isotropic [QUESTIONABLE]

Density 2000 kg/m3, E 86 GPa, compressive strength 850 MPa. Basis: QI laminate estimate: E_QI ~ 0.42 x UD E1 (204 GPa); sigma_c_QI ~ 0.34 x UD longitudinal compressive strength (2500 MPa); not fibre properties. Source: Boron fibre review https://www.compositesworld.com/articles/boron-fiber-the-original-high-performance-fiber ; unidirectional boron/epoxy property table (E1 204 GPa, compressive 2500 MPa) in composites textbook extract https://structures.dhu.edu.cn/_upload/article/files/79/64/d90aa6424b14824d25a678e990c0/4ff4b286-e563-4c01-a7f0-ac45163b28a4.pdf.
Figures: E/rho 43 GPa per g/cc, sigma_c/rho 425 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.3889, SF_y 1.807, least 0.3889, gap 2.571; P2-C: SF_b 0.3289, SF_y 0.9617, least 0.3289, gap 3.04; P2-K: SF_b 0.3789, SF_y 1.302, least 0.3789, gap 2.639; P2-E: SF_b 0.3941, SF_y 1.616, least 0.3941, gap 2.537.
In P2-E the limiting figure is E/rho; gap 2.537. Face thickness in P2-E at equal mass: 0.4537 mm.

## Rank 8 - AlBeMet 162 (AM162, HIP) [QUESTIONABLE]

Density 2071 kg/m3, E 193 GPa, compressive strength 193 MPa. Basis: HIP tensile yield transferred to compression. Source: Materion AlBeMet technical data sheet https://web.archive.org/web/20171024043552/https://materion.com/[private path] (density 2.071 g/cc, E 193 GPa, HIP yield 193 MPa).
Figures: E/rho 93.192 GPa per g/cc, sigma_c/rho 93.192 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.8428, SF_y 0.3963, least 0.3963, gap 2.523; P2-C: SF_b 0.7129, SF_y 0.2109, least 0.2109, gap 4.742; P2-K: SF_b 0.8212, SF_y 0.2856, least 0.2856, gap 3.501; P2-E: SF_b 0.8541, SF_y 0.3544, least 0.3544, gap 2.822.
In P2-E the limiting figure is sigma_c/rho; gap 2.822. Face thickness in P2-E at equal mass: 0.4382 mm.

## Rank 9 - CFRP quasi-isotropic T700/epoxy [QUESTIONABLE]

Density 1550 kg/m3, E 54 GPa, compressive strength 520 MPa. Basis: QI laminate estimate: E_QI ~ 0.40 x UD composite E (134 GPa, Toray T700S composite), sigma_c_QI ~ 0.33 x UD compressive strength; not fibre properties. Source: Toray T700S data sheet https://www.rockwestcomposites.com/downloads/T700SDataSheet.pdf (fibre 230 GPa, 1.80 g/cc; composite tensile modulus 134 GPa); QI reduction stated in sigma_c_basis.
Figures: E/rho 34.839 GPa per g/cc, sigma_c/rho 335.48 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.3151, SF_y 1.427, least 0.3151, gap 3.174; P2-C: SF_b 0.2665, SF_y 0.7591, least 0.2665, gap 3.752; P2-K: SF_b 0.307, SF_y 1.028, least 0.307, gap 3.257; P2-E: SF_b 0.3193, SF_y 1.276, least 0.3193, gap 3.132.
In P2-E the limiting figure is E/rho; gap 3.132. Face thickness in P2-E at equal mass: 0.5855 mm.

## Rank 10 - Al-Li 2195-T8 [QUESTIONABLE]

Density 2710 kg/m3, E 76 GPa, compressive strength 560 MPa. Basis: tensile yield (L direction) transferred to compression. Source: MatWeb 2195 composition/density sheet https://www.matweb.com/search/datasheet_print.aspx?matguid=4363dafc7f5545688506d8b4af1e9468 ; MakeItFrom 2195-T8 https://www.makeitfrom.com/compare/2195-2195-T8-Aluminum/B390.0-B390.0-F-SC174B-A23900-Cast-Aluminum (E 76 GPa, yield 560 MPa).
Figures: E/rho 28.044 GPa per g/cc, sigma_c/rho 206.64 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.2536, SF_y 0.8788, least 0.2536, gap 3.943; P2-C: SF_b 0.2145, SF_y 0.4676, least 0.2145, gap 4.661; P2-K: SF_b 0.2471, SF_y 0.6333, least 0.2471, gap 4.047; P2-E: SF_b 0.257, SF_y 0.7857, least 0.257, gap 3.891.
In P2-E the limiting figure is E/rho; gap 3.891. Face thickness in P2-E at equal mass: 0.3349 mm.

## Rank 11 - Ti-6Al-4V (annealed) [QUESTIONABLE]

Density 4430 kg/m3, E 113.8 GPa, compressive strength 970 MPa. Basis: compressive yield, typical annealed value. Source: ASM MatWeb Ti-6Al-4V annealed data sheet (density 4.43 g/cc, E 113.8 GPa, compressive yield 970 MPa).
Figures: E/rho 25.688 GPa per g/cc, sigma_c/rho 218.96 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.2323, SF_y 0.9312, least 0.2323, gap 4.304; P2-C: SF_b 0.1965, SF_y 0.4954, least 0.1965, gap 5.089; P2-K: SF_b 0.2264, SF_y 0.671, least 0.2264, gap 4.418; P2-E: SF_b 0.2354, SF_y 0.8326, least 0.2354, gap 4.247.
In P2-E the limiting figure is E/rho; gap 4.247. Face thickness in P2-E at equal mass: 0.2048 mm.

## Rank 12 - 6061-T6 (baseline) [QUESTIONABLE]

Density 2700 kg/m3, E 68.9 GPa, compressive strength 276 MPa. Basis: typical tensile yield transferred to compression, per pinned COMMON.md. Source: Pinned COMMON.md (MAINLINE-001/002); ASM MatWeb 6061-T6 data sheet (AA typical values).
Figures: E/rho 25.519 GPa per g/cc, sigma_c/rho 102.22 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.2308, SF_y 0.4347, least 0.2308, gap 4.333; P2-C: SF_b 0.1952, SF_y 0.2313, least 0.1952, gap 5.123; P2-K: SF_b 0.2249, SF_y 0.3133, least 0.2249, gap 4.447; P2-E: SF_b 0.2339, SF_y 0.3887, least 0.2339, gap 4.276.
In P2-E the limiting figure is E/rho; gap 4.276. Face thickness in P2-E at equal mass: 0.3361 mm.

## Rank 13 - 7075-T6 [QUESTIONABLE]

Density 2810 kg/m3, E 71.7 GPa, compressive strength 503 MPa. Basis: tensile yield transferred to compression; no compressive yield retrieved. Source: ASM MatWeb 7075-T6 data sheet; density 2.81 g/cc, E 71.7 GPa, tensile yield 503 MPa.
Figures: E/rho 25.516 GPa per g/cc, sigma_c/rho 179 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.2308, SF_y 0.7612, least 0.2308, gap 4.333; P2-C: SF_b 0.1952, SF_y 0.405, least 0.1952, gap 5.123; P2-K: SF_b 0.2248, SF_y 0.5486, least 0.2248, gap 4.448; P2-E: SF_b 0.2339, SF_y 0.6806, least 0.2339, gap 4.276.
In P2-E the limiting figure is E/rho; gap 4.276. Face thickness in P2-E at equal mass: 0.3229 mm.

## Rank 14 - Mg AZ31B [QUESTIONABLE]

Density 1770 kg/m3, E 45 GPa, compressive strength 97 MPa. Basis: compressive yield 97 MPa (rolled/extruded AZ31; tension-compression asymmetry retained, tensile yield not used). Source: AZ31 property table in https://zenodo.org/records/5519242/files/E27900610521.pdf (compressive yield 97 MPa); density 1.77 g/cc, E 45 GPa (ASM MatWeb AZ31B).
Figures: E/rho 25.424 GPa per g/cc, sigma_c/rho 54.802 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.2299, SF_y 0.2331, least 0.2299, gap 4.349; P2-C: SF_b 0.1945, SF_y 0.124, least 0.124, gap 8.064; P2-K: SF_b 0.224, SF_y 0.1679, least 0.1679, gap 5.954; P2-E: SF_b 0.233, SF_y 0.2084, least 0.2084, gap 4.799.
In P2-E the limiting figure is sigma_c/rho; gap 4.799. Face thickness in P2-E at equal mass: 0.5127 mm.

## Rank 15 - Metallic glass Vitreloy 1 (Zr41.2Ti13.8Cu12.5Ni10Be22.5) [QUESTIONABLE]

Density 6120 kg/m3, E 96 GPa, compressive strength 1900 MPa. Basis: compressive ultimate strength (bulk metallic glass has no distinct compressive yield; failure is shear-band fracture). Source: Review of Zr-based bulk metallic glasses https://www.mdpi.com/2075-4701/5/3/1262 (E 70-96 GPa, compressive ultimate 1400-1900 MPa for Vitreloy 1); density 6.12 g/cc typical for Vitreloy 1.
Figures: E/rho 15.686 GPa per g/cc, sigma_c/rho 310.46 MPa per g/cc (6061-T6: 25.519 and 102.22 in the same units, from 68.9 GPa, 276 MPa, 2700 kg/m3).
At equal face mass: P2-A: SF_b 0.1419, SF_y 1.32, least 0.1419, gap 7.049; P2-C: SF_b 0.12, SF_y 0.7025, least 0.12, gap 8.334; P2-K: SF_b 0.1382, SF_y 0.9514, least 0.1382, gap 7.235; P2-E: SF_b 0.1438, SF_y 1.18, least 0.1438, gap 6.956.
In P2-E the limiting figure is E/rho; gap 6.956. Face thickness in P2-E at equal mass: 0.1483 mm.

## Materials-direction list (best three in P2-E)

- SiC (monolithic alpha SiC, Hexoloy SA type) [QUESTIONABLE], rank 1: SF_b 1.212, SF_y 4.784, least 1.212. Limiting figure E/rho; it must improve by factor 0.825 for its own mode to reach SF 1 (E/rho factor 0.825, sigma_c/rho factor 0.209; both are needed if both modes are below 1).
- CNT-yarn composite quasi-isotropic [PROJECTION], rank 2: SF_b 1.178, SF_y 3.259, least 1.178. Limiting figure E/rho; it must improve by factor 0.8486 for its own mode to reach SF 1 (E/rho factor 0.8486, sigma_c/rho factor 0.3068; both are needed if both modes are below 1).
- Graphene composite quasi-isotropic [PROJECTION], rank 3: SF_b 0.9165, SF_y 2.281, least 0.9165. Limiting figure E/rho; it must improve by factor 1.091 for its own mode to reach SF 1 (E/rho factor 1.091, sigma_c/rho factor 0.4383; both are needed if both modes are below 1).

Best three available today (projections excluded):
- SiC (monolithic alpha SiC, Hexoloy SA type) [QUESTIONABLE], rank 1: SF_b 1.212, SF_y 4.784, least 1.212. Limiting figure E/rho; factor 0.825 for its own mode to reach SF 1 (E/rho factor 0.825, sigma_c/rho factor 0.209).
- CFRP quasi-isotropic M55J/epoxy [QUESTIONABLE], rank 4: SF_b 0.7545, SF_y 0.8115, least 0.7545. Limiting figure E/rho; factor 1.325 for its own mode to reach SF 1 (E/rho factor 1.325, sigma_c/rho factor 1.232).
- Beryllium S-200F [QUESTIONABLE], rank 5: SF_b 1.501, SF_y 0.5817, least 0.5817. Limiting figure sigma_c/rho; factor 1.719 for its own mode to reach SF 1 (E/rho factor 0.6662, sigma_c/rho factor 1.719).

Reading: a gap below 1 means that mode already passes on these two formulas alone; it is not a buildability claim. SiC and beryllium carry fracture, joining and handling objections in NFI.json. Next jobs: 008b adds P1 and P3 columns when MAINLINE-005 is filed, 008c rescales buckling by MAINLINE-004's knockdown, and a later update re-ranks on MAINLINE-007's best rows.
