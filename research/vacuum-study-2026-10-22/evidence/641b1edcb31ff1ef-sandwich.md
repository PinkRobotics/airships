# MAINLINE-045 sandwich impact and detection: sourced record (sandwich.json, 136 rows, tag QUESTIONABLE)
Conventions: negative values mean a strength or depth reduction; "model" = finite-element result; secondary = number quoted inside another document. Row count is above the 50-110 aim because the hail topic was added and Table rows are kept as separate rows.
## 1. Impact and indentation of thin-faced Al honeycomb
- Pach 2026 (test): 0.508 mm 2024-T3 faces, 6.35 mm cell 5052 core; 25.4 mm hemispherical steel, 1053 g from 152 mm (1.57 J) gave a dent about 1.1-1.2 mm deep, about 30 mm across, no face cracking [pach].
- Wang 2017 (test): 5052 faces 0.5/1.0/1.5/2.0 mm over 3003 core, 50 mm ball dropped 2 m (mass not stated): dents 3.93/2.79/2.48/2.00 mm, no perforation; its tables contradict its own text [wang].
- Clarke 2017 (FE): 0.301 mm 7075-T6 faces, 0.61-4.31 J: dents 0.51-2.42 mm deep, 14.3-43.6 mm wide; face ruptured at 1.62-1.66 mJ/mm2 (1.07 J, 6.35 mm radius sphere); 1.3 mJ/mm2 did not rupture; core crush depth 5.1-7.0 mm (mean 6.0), constant with dent depth; core damage width = dent width; thicker face 0.102->1.219 mm cut dent depth 70% [clarke].
- Clarke: least-dense core tried (3/8 in cell, 16 kg/m3) had the largest displacement, 2.37 mm vs 1.04 mm for the densest [clarke]. Foo/Boctor/Wowk energy-and-dent ranges are secondary via Pach [pach].
- Gilioli 2014 (test, Nomex core, 1 and 1.5 mm Al2024 skins, 15-242 J): dent 2.2-10.1 mm; 1 mm skin fails above 200 J [gilioli]. Azouaoui 2013: 0.6 mm Al skins cracked after 18,000-20,000 impacts of 2 J [azouaoui].
- Hexcel CR III 5056, 3/8 in, 1.0 pcf: crush 35 psi (0.241 MPa) typ; bare compressive 55 psi typ / 25 psi min; crush values scatter up to +/-20% below 3 pcf [hexcel].
## 2. Compression after impact
- Pach: singly-dented panel peak 66.9 kN (215 mm wide); a second dent cuts it up to 9% more; no undamaged baseline printed [pach].
- Gilioli: CAI 18.3-44.6 kN after 15-242 J against intact 29.4-76.8 kN (1 mm) and 47.9-84.1 kN (1.5 mm); flat above about 50 J; no skin-thickness gain once damaged [gilioli].
- Castanie 2012 (0.5 mm brass skins): 0.5 mm indentation left a 0.1 mm print and cost 2% strength; the dent grows abruptly at peak load [castanie]. McGowan 1998: composite-faced panels preloaded in compression fail on impact above a threshold strain [mcgowan].
- Secondary: up to 60% (Raju), up to 25% with no visible damage and 50% deeper (McQuigg), 0.5 mm Al face with a hole 32.9 -> 31.1 kN (Tariq), two dents -13% (Boctor FE) [clarke, boctor].
## 3. Beryllium
- SR-200 sheet minimums: UTS 483 MPa, yield 345 MPa, elongation 10.0% (in 1 in); E 290 GPa, 1.85 g/cm3; sheet is "hot rolled", 0.5-6.25 mm; S-200-F block minimum elongation 2.0% [sr200, s200f].
- NASA 1971: beryllium "considered a brittle material", impact resistance "extremely low"; crack toughness about 10 ksi-in^1/2 (11.0 MPa m^1/2) pressed, 11 (12.1) forged, S-200 23 (25.3, not fatigue-cracked) [jones]. Hypervelocity: brittle crater plus cracking [diedrich]. No through-thickness elongation, Charpy value or thin-sheet point-impact test found.
## 4. Detection
- BVID dent depth: 0.05 in (1.27 mm) NASA Langley criterion [mcgowan]; Boeing 0.25-0.5 mm, NPL 0.5 mm, NASA 1.27-2.54 mm (secondary) [boctor, pach]; Griffon repair manual: negligible below 12.7 mm wide, allowable to 101.6 mm and 20% of panel thickness deep [clarke].
- Relaxation: CFRP face under 30 um in a week [prior]; foam-core 0.95 mm in 5 min (cited); a disbond can erase the dent [prior]; metal faces keep a dent [clarke].
- Tap test on 0.5 mm Al skins (disbonds, no dent): a90/95 41.8 mm manual, 29 mm automated, best inspector 25.4 / 22.5 mm [genest]; tap sensitivity falls with face thickness (no number) [prior]; no limit found for ultrasound, thermography or shearography on metal faces.
## 5. Hail (added)
- Al 5083-H116 plate, 50.8 mm lab ice, 35-80 m/s: 3 mm plate 0.480 mm dent at 46.9 m/s (64.8 J), 0.664 mm at 54.5 m/s (89.0 J); 4 mm plate 0.283 mm at 64.3 m/s (122 J) to 0.525 mm at 79.1 m/s (188 J) [shi]. Al-faced polymer-core panel: 40 and 50 mm ice dented, 30 mm did not [stac].
- Carbon/epoxy laminates, lab ice: 16-ply failure threshold 332-384 J (38.1 mm), 453-458 J (50.8 mm), 484-505 J (61 mm) (cell assignment inferred) [kim]. Natural-hail terminal energy: 3.8 cm 10.85 J, 5.1 cm 29.8 J [marshall]. No ice density printed in any source.
## GAPS (full list in sandwich.json "gaps")
FAA AR-00/44, 02/80, 02/121 blocked (DTIC "request is blocked"); Foo/Crupi/Akatay/Hazizan papers paywalled; no Be sheet through-thickness ductility, Charpy or point-impact data; no NDI limit on metal faces beyond tap; no quantified metal-face dent relaxation; no SHM data; no hail test on Al honeycomb sandwich found open.
