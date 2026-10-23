CHECK MAINLINE-046 — independent film-life audit

QUESTIONABLE / PROJECTION. The highlighted arithmetic reproduces. No installed one-year or ten-year life, qualified film strength, or qualified whole-hull SF is established. Protected replaceable PBO remains a development candidate; no demonstrated lightest ten-year route can be selected.

The check uses frozen data and primary sources. No owner or predecessor executable was read, hashed, imported, copied or run. The two excluded owner scripts are identified only by supplied metadata. The independent scripts are audit.py and supplement.py.

Arithmetic: 3,796 field checks across all 389 CSV rows and associated JSON: 3,780 strict matches and 16 differences. All 16 resolve using the owner's explicitly declared 774.440887 m seam reference instead of the pinned 774.4408874322422 m value. Maximum strict difference is 6.4851e-9 kg (6.4851 micrograms). ARITHMETIC-DIFFERENCES.json gives every path, both values and signed delta; ROUNDING-RESOLUTION.json gives the reconciliation. No conclusion changes.

All 135 calculated table cells in CARD.md match their displayed precision. Fourteen NIST source-table pairs match. All 115 non-code manifest entries verify; the two executable entries remain excluded. Forty report artifacts and 62 input/source pin records also verify (overlapping sets, not added as independent evidence). The figure was visually checked against the independently computed curves and ten-year bars.

| Point | Total gauge μm | Film kg | SF0 | Retention for nominal SF1 | Per-ply stress GPa |
|---|---:|---:|---:|---:|---:|
| 022d-5 | 109.440222 | 214.541558 | 1.258252477 | 0.794753055 | 2.765740632 |
| 022d-019 | 103.045891 | 202.006405 | 1.194121426 | 0.837435773 | 2.914276492 |
| 041-5 | 82.041755 | 160.830867 | 1.143284619 | 0.874672836 | 3.043861470 |
| 041-019 | 77.730485 | 152.379253 | 1.083205354 | 0.923185983 | 3.212687221 |

For membrane resultant p rc/2 and two t/2 plies, ply stress is p rc/t. Compare it with .6×5.8=3.48 GPa; 1.74 GPa is the equivalent strength for total gauge and is not halved again. A separately generated frequency-5 icosahedral mesh reproduces 252 nodes, 750 arcs, 500 cells, 1799.676623909 m seam length, 2.615980975 m maximum chord and 73.100733115 kg sag debit. Upstream frame/joint eigensolutions are pinned input evidence; this check does not rerun 041's structural analysis or qualify its local-shell screen.

| Ten-year scenario | 022d-5 film SF | 041-5 film SF | 041-019 film SF |
|---|---:|---:|---:|
| Warehouse endpoint exponential | 1.084071169 | 0.985018441 | 0.933256017 |
| Combined .5% annual-loss requirement | 1.196736677 | 1.087389583 | 1.030247586 |
| Combined requirement, hot/full restraint | 1.092730519 | 0.995706369 | 0.944784460 |

The five scenario laws, 1/5/10-year strengths, all twenty nominal crossing ages, and the alternative tail/dose tables reproduce. The humidity and warehouse records are AS yarn proxies. Outdoor continuation residuals reach .082089, exceeding the graph-reading band; the owner already discloses that the curve is not an all-point fit. Its early crossing times are interpolations before the first nonzero measurement. An endpoint reading sensitivity alone moves both 041 warehouse ten-year SF ranges across 1. EVIDENCE.md and AGE-MODEL-SENSITIVITY.json record the source and model limits; no probabilistic confidence is inferred.

At 041 the reconstructed OD4/white mass is 20.960706185 kg PET + .339292007 kg aluminium + 31.415926536 kg attachment + 31.415926536 kg white coat + 11.619199432 kg scaled seams = 95.751050695 kg. The owner's rounded-reference result is 95.751050702 kg. The two-face foil option is 202.497675678 kg. Optical performance is not inferred from mass.

The primary service solve reproduces 321.940239586 K peak film temperature, .964012201 instantaneous strength factor, 90.501688 MPa added full-restraint ply stress and pressure ratio 1.023044536. The hot corrections add .713771403/9.165385273 kg PBO at 041-5/019. With the protected package, 30–50 kg vacuum hardware and 5 kg adhesive placeholder, reserve-preserving closure deficits are 31.464822–51.464822 kg and 39.916436–59.916436 kg. These corrections do not restore an unqualified frame or joint mode; the inherited 041-019 local peak sensitivity remains .978132.

The primary 041 moisture result is 1.020387 kg capacity at 32.516516 Pa, max WVTR .805222 g/m²/day and 19.3568-hour drying. The h=2 cold-patch case reduces these to .686336 kg, .539393 g/m²/day and 13.0198 hours. The 458.672527 kg/year field includes only coupon water: adding weighted seam/port leakage gives 459.261468 kg/year under the same pressure convention. This small labeling omission is CHECK046-01; initial residual water and actual laminate activity remain unmeasured.

SK99's chemistry-only 135.881 kg nominal-SF1 mass reproduces. Its patent creep rate is 2207.52 times the ten-year/1%-strain constant-rate budget; DM20 is 409.968 times that budget. At 900 MPa a 041 UHMWPE film would weigh 338.220 kg, without demonstrating that stress safe. Thus the static mass ranking cannot select a ten-year installed material. Fatigue endpoints, exponent 20.735575 and all cycle indices reproduce but remain median R=0 single-filament sensitivities.

Annual replacement at 041-5 with 25 mm two-layer edge reinforcement uses 268.098510 kg per set, 2680.985104 kg over ten years, with 2412.886594 kg offboard. No annual interval is qualified; the humid-proxy pre-renewal SF is .9548. Eight checker NFI entries add quantified implications or a labeling correction; all 22 owner NFI entries and the six inherited registers remain open.

Reproduction: run audit.py, then supplement.py, then package.py from this frozen directory using Python 3 and the standard library. PDF extraction used pdftotext; page inspection used pdftoppm. An initial checker draft used a truncated knot conversion; the final audit uses exact 1852/3600 m/s per knot. No failure from that draft is attributed to the owner. All reported comparisons use the final source state.

Report to sciences, cc co/xo/admiral-robotics-review-v2. Brief says stop and file; no successor. No out-of-band contact, wake or restore. No time budget.
