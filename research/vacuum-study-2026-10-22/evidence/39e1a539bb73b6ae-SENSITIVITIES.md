# MAINLINE-022d — assumption sensitivities

**QUESTIONABLE. All alternatives are PROJECTION.**

Square-cell alternatives use square inradius for the cap or the exact linear square membrane mean, and the scalar two-way D/Y=I/A half-wave. They remain unvalidated for the shear-free lattice.

| Branch | Reserve | Family | Overall SF | Screened SF | Screened s, m |
|---|---|---|---:|---:|---:|
| cap | 5 | Projected film | 1.795705372 | 1.728882831 | 3.180830 |
| cap | 5 | Mylar / Fc 380 MPa | 0.411601980 | 0.411601980 | 0.517428 |
| cap | 5 | Kapton / Ti | 0.974642535 | 0.974642535 | 1.186234 |
| cap | 5 | Zylon 0/90 / CFRP | 1.760011640 | 1.720244372 | 3.178447 |
| cap | 019 | Projected film | 1.698927970 | 1.636555516 | 3.154808 |
| cap | 019 | Mylar / Fc 380 MPa | 0.395906067 | 0.395906067 | 0.522081 |
| cap | 019 | Kapton / Ti | 0.931878102 | 0.931878102 | 1.189521 |
| cap | 019 | Zylon 0/90 / CFRP | 1.670149904 | 1.632822988 | 3.153729 |
| membrane | 5 | Projected film | 1.788384221 | 1.724469116 | 3.179614 |
| membrane | 5 | Mylar / Fc 380 MPa | 0.411480828 | 0.411480828 | 0.516322 |
| membrane | 5 | Kapton / Ti | 0.973885032 | 0.973885032 | 1.183603 |
| membrane | 5 | Zylon 0/90 / CFRP | 1.753868276 | 1.716077673 | 3.177293 |
| membrane | 019 | Projected film | 1.691796461 | 1.632242278 | 3.153561 |
| membrane | 019 | Mylar / Fc 380 MPa | 0.395783873 | 0.395783873 | 0.520936 |
| membrane | 019 | Kapton / Ti | 0.931120490 | 0.931120490 | 1.186782 |
| membrane | 019 | Zylon 0/90 / CFRP | 1.664129907 | 1.628730039 | 3.152544 |

Tensile ceiling alternatives below show cap/5% equilateral results. All 48 optimized tensile alternatives, including membrane and 019, are in SENSITIVITIES.json.

| Family | Search | Ft, MPa | Least SF | s, m |
|---|---|---:|---:|---:|
| Projected film | overall | 0.000 | 1.381848171 | 6.072204 |
| Projected film | overall | 7.192 | 1.381886087 | 6.073600 |
| Projected film | overall | 380.000 | 1.383400125 | 6.130252 |
| Projected film | in_band | 0.000 | 1.214863410 | 3.154020 |
| Projected film | in_band | 7.192 | 1.214863410 | 3.154020 |
| Projected film | in_band | 380.000 | 1.214863410 | 3.154020 |
| Zylon 0/90 / CFRP | overall | 0.000 | 1.397681534 | 6.082771 |
| Zylon 0/90 / CFRP | overall | 7.192 | 1.397705249 | 6.084153 |
| Zylon 0/90 / CFRP | overall | 380.000 | 1.398644329 | 6.140263 |
| Zylon 0/90 / CFRP | in_band | 0.000 | 1.258252477 | 3.170759 |
| Zylon 0/90 / CFRP | in_band | 7.192 | 1.258252477 | 3.170759 |
| Zylon 0/90 / CFRP | in_band | 380.000 | 1.258252477 | 3.170759 |

Expanded spacing/radius bounds leave all 16 cap/5% optima unchanged within 4.07e-14 SF. Using chord spacing instead of the longer arc in the 16 active screens raises SF by at most 0.002183537.

The separate magnified-local diagnostic applies the axial shell threshold to the amplified maximum compression face at fixed primary geometry. It is **not a validated interaction rule** and is not substituted into the main results.

| Primary key | Primary SF | Unvalidated diagnostic multiplier |
|---|---:|---:|
| cap/equilateral/5/projection/overall | 1.381929805 | 1.085380579 |
| cap/equilateral/5/projection/in_band | 1.214863410 | 1.140361381 |
| cap/equilateral/5/cfrp_zylon/overall | 1.397732582 | 1.097987958 |
| cap/equilateral/5/cfrp_zylon/in_band | 1.258252477 | 1.181463888 |
| cap/two_way/5/projection/overall | 2.010980577 | 1.613483441 |
| cap/two_way/5/projection/in_band | 1.867825477 | 1.739702732 |
| cap/two_way/5/cfrp_zylon/overall | 1.952879351 | 1.565409423 |
| cap/two_way/5/cfrp_zylon/in_band | 1.849171174 | 1.722158346 |
