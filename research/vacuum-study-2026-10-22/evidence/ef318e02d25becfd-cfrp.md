# MAINLINE-049 CFRP faces, thin plies, supply, joints (121 rows in cfrp.json; each quote machine-checked verbatim against the opened file)

## 1. K13D2U (Mitsubishi DIALEAD pitch fibre)
- Fibre [Mitsubishi tow table, 2022]: 935 GPa, 3.70 GPa (3700 MPa), 2.20 g/cm3, 2K tow 365 mg/m, 800 W/mK.
- Fibre CTE about -1.5 ppm/K and strain <0.4% [Shin, NASA GRC 2007; value grouped with K1100].
- Lamina K13D2U/epoxy [Tuttle, Univ. Washington; 1 specimen each, Vf not stated]: E1 410 GPa, E2 5.56 GPa, G12 4.10 GPa, nu12 0.39, ply 0.061 mm.
- Prepreg: EX1515/K13D2U 69 gsm, 33% resin [Fermilab/DOE 2023]; 6-ply K13D2U/EX1522 face sheet about 1 mm [NASA NETS 2011].
- NOT FOUND: Xt, Xc, Yt, Yc, lamina CTE, any QI data, any laminate compression strength.
- Other pitch fibres [NGF GRANOC, Nippon Steel TR134, 2025]: YSH-70A 720 GPa/3630 MPa; YS-80A 785/3630; XN-80 780/3430; CTE -1.4 to -1.5e-6/K. Composite compression is printed only for low-modulus XN-15 (1150 MPa).

## 2. M55J (Toray PAN high-modulus fibre)
- Fibre [Toray datasheet Rev 04/2025]: 4020 MPa, 540 GPa, 0.8%, 1.91 g/cm3, 5 um, CTE -1.1e-6/C.
- UD composite at 60% Vf, #2500 epoxy [same]: Xt 2020 MPa, E1 338 GPa, Xc 890 MPa, Yt 37 MPa, shear 68 MPa, ILSS 73.2 MPa.
- RS-3C/M55J [Toray Adv. Composites PDS 12/2025], 0 deg compression (backed out, 60% Vf): 903 MPa RTD, 703 at 150 C, 393 at 232 C, 883 at -130 C; ILSS 69.9 MPa RTD, 46.9 at 150 C.
- QI laminate: CALCULATED only [Rock West M55J/PMT-F33, 1.12 mm plate]: E 108.9 GPa, Fc 313 MPa, Ft 710 MPa, CTE -0.365 ppm/K. No measured QI data found.

## 3. Thin plies
- NTPT 15 gsm UD tape (intermediate-modulus fibre; thickness not printed) [CompositesWorld 2015]; OnlyTop 15-50 gsm FAW [CW 2026].
- Hexcel IM7/8552 30 gsm FAW = 0.0305 mm cured ply, special order; 64-ply QI tension 951 MPa, compression 814 MPa [NASA 2020].
- Oxeon: spread tapes from 38 gsm; research tape 21 gsm = 20 um (HS40 PAN); pitch K13916 spread only to 105 gsm [Alves 2020].
- High-modulus/space: ESA GSTP YSH-60A-60S 6K at 35 g/m2 (vs 105), Vf 55%, QI CTE 74% lower, tension 15-20% lower, compression +11%, porosity problems; space skins commonly 0.3 mm. ESA text: about 30 gsm with M55J 6k (intent).
- 4-ply QI of 0.0305 mm plies = 0.12 mm is arithmetic only, not sourced.

## 4. Supply
- Continuous pitch fibre about 1,400 t/yr (3 producers); all carbon fibre 250,000-300,000 t/yr [Nippon Steel TR134, 2025].
- Demand 117,500 t (2023), 126,500 t (2024) [Composites United]; 156,100 t (2024), 224,510 t (2025), capacity 326,080 t [ATA CFT via CompositesWorld]; aerospace/defense average roughly $80/kg. No pitch or M55J price or tonnage found.

## 5. Joints and bonding
- Scarf angle <= tau/(eps_u E): 4 deg (about 1:14) for 20 MPa hot-wet adhesive, 4000 microstrain, 70 GPa [Li, ICAS 2008]; 5 deg test joint with FM73 0.38 mm.
- Scarf repair recovery 79.1% (1/20), 83.6% (1/30) static; 39.7%/52.1% at 1e6 cycles [Yoo 2016, abstract only]. Hart-Smith NASA CR-112237: scarf strength rises with overlap; stepped-lap approximates scarf.
- FM 300 177 C (lightest 0.03 psf = 146 gsm); FM 300-2 121 C, made for co-cure; on CFRP: lap shear 23.7 MPa, co-cured wide-area lap shear 17.3 MPa with ALL LAMINATE failure.
- AF 163-2 0.015-0.100 lb/ft2, 250 F/60 min; EA 9696 225-265 F, .060NW = 293 g/m2, flatwise 9.0 MPa. Their other numbers are on aluminium adherends.

## GAPS
- No K13D2U compression/Xt/Yt/QI; no measured M55J QI; no cured-ply datasheet for 15-30 gsm high-modulus plies; no Mitsubishi pitch capacity, M55J tonnage or fibre price.
- LBNL TenCate CE-3 sheets 404; Cal Poly allowables thesis PDF blocked (numbers proprietary); FM 73, HexBond, self-adhesive prepreg sheets not opened; Yoo 2016 abstract only. Full list in cfrp.json "gaps".
