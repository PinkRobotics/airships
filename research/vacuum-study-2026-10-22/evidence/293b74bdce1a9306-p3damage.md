# MAINLINE-045 P3 damage sources: SiC and film (107 rows in p3damage.json; quotes string-matched against the opened text, except 3 Sterling Table 2 rows read from a page image)
All rows tagged QUESTIONABLE, state "exists today". Bracketed keys name the source; full citations, quotes and page locations are in the JSON.
## SiC strength statistics
- Hexoloy SA datasheet [Saint-Gobain B-1045, 2012]: flexure 380 MPa (4-pt) / 550 MPa (3-pt) on 3x4x45 mm bars, Weibull modulus 10 (test not stated), compression 3900 MPa, E 430 GPa, K_IC 4.60 MPa m^1/2; sheet says compression is 10x tension.
- NIST SRD 150 sintered alpha-SiC (Munro 1997) [NIST]: flexure 359 MPa, tensile 250 MPa, Weibull modulus 11 (27% unc.), K_IC 3.1, E 415 GPa. Direct tension on sintered alpha-SiC: 160 MPa, Weibull modulus 4.3 [NIST SCD Z00009, Seshadri and Chia].
- Hexoloy SA in NIST SCD [Z00042, Hecht 1988]: flexure 331 and 402 MPa, Weibull modulus 9 (51x6.4x3.2 mm bars). GE sintered beta-SiC [Z00021]: 346+-34 MPa, m 11.0. Reaction-bonded SCRB210 [Z00046]: 370 MPa, m 7.7.
- CVD SiC: 370 MPa at 20 C, K_IC 2.94 [Morgan]; 595 MPa, K_IC 2.7-3.3 [Goela 1991]; "389 MPa, Weibull 5" only as a secondary citation [Horvath, ORNL].
- Hexoloy TUBES [INL/ORNL TM-2013/114]: axial tension 320 MPa m=10; internal pressure (OD 14, wall 1.5 mm) 132-137 MPa m=5.3-5.8, surface-flaw failures 108 MPa; diametral compression 253 m=31.7; C-ring 299 m=4.6; sectored flexure 192 m=5.5. Triplex SiC/SiC tube hoop 282 MPa, m=11.05; first load drop 227 MPa [KAERI].
## SiC impact and contact damage
- Only low-velocity SiC plate data found [GE/NASA CR-134990, 1976]: 4.49 mm, 0.37 g steel ball; visible Hertzian damage at 0.29 J (39 m/s); catastrophic damage of a 5x5x0.9 cm plate at 0.67 J (60 m/s); porous-layer variants survived 1.16 to 5.94 J.
- ORNL hot-pressed SiC ring-crack stress estimates ~1400 MPa (fine grain) and ~1151 MPa (coarse); steel balls yield (2-3x yield) before ring cracking [ORNL/TM-2009/234]. Spherical indentation of SiC-N: yield at 12-13 GPa contact stress, ring/radial cracking near 19 GPa [OSTI 931248].
- Korean sphere-impact papers on SiC [Oh 2001, 2005, 2010]: ring cracks grow with velocity, steel larger than SiC particles, 2 mm steel ball at 113-180 m/s on 3 mm RS-SiC, ring to cone crack transition; abstracts only, no thresholds in m/s. Si3N4 2 mm disks (proxy): back-side cracking from 160-220 m/s, Vc 300-440 m/s [NASA TM-2003-212224].
## Film puncture and tear
- Kapton HN [DuPont 2016]: Elmendorf 0.07/0.21/0.38/0.58 N and Graves 7.2/16.3/26.3/46.9 N for 25/50/75/125 um; pneumatic impact 78 N cm (same for every gauge); tensile 231 MPa. UBE Upilex-S 25 um: Elmendorf 3.2 N, Graves 600 N/mm (not reconciled with DuPont).
- Kapton 0.1-1 mil tongue tear 0.5-6 gf, 11-29x higher after a perforation hole; "Kapton films exhibit extremely low resistance to tear propagation"; ripstop requirement 8 m [ILC Dover/JPL CR-155616, 1977].
- 11-12 um films, Elmendorf 0.1 N (PET, PEN, polyimide) vs 3.7 N MD (LLDPE); ASTM D3420 impact 0.6 N (PET, polyimide) vs 8.8 N (LLDPE); 12 um PET balloons destroyed in deployment tests [Sterling and Fairbrother 2004]. Mylar 52 um essential work of fracture ~40 kJ/m2 (63.7 at 1 m/s) [Pegoretti, ICF11].
- Balloon film: StratoFilm 420 (38 um) Jc 500-2000 J/m2 at 253 K, 2 mm slit [Hegyi, Li, Pellegrino 2013]; undamaged 0.8 mil PE cylinder hoop failure 2086 psi, pin hole stopped inflation, burned seam -19% [Portanova CR-181872].
- Zylon fibre [Toyobo 2005]: 5.8 GPa, knot strength 26-32% of tensile, compressive 0.47-0.56 GPa, 35% strength left after 6 months daylight. No PBO film data found.
## GAPS (details in JSON "gaps")
- No Dow/Rohm and Haas/CoorsTek CVD datasheet; DTIC CVD reports blocked (403); SiC/SiC composite tensile tables not retrieved; Munro paper itself not opened.
- No SiC Auerbach critical loads, no SiC-tube impact/drop test, no post-damage strength of SiC, no effective volume/area for any datasheet value.
- No Zylon/PBO film, no tear-under-tension data for Kapton/Zylon, no aerostat hail or puncture report; Montana EWF thesis (Mylar/Kapton) unreachable.
