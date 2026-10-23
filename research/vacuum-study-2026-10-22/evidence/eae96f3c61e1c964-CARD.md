# MAINLINE-069 — the hull that floats on optimistic estimates

Unit vacuum-mainline069-design-point-1020. QUESTIONABLE inputs. PROJECTION payloads. No qualified hull safety factor. No finite-element run.

P2 at R 30. This is the radius that needs the least improvement: 066's concept closure is 1013.8 kg/m3 here and 993.2 kg/m3 at R 20. The face is 066's concept R 30 optimistic density, 1013.825 kg/m3, factor 1.824772 on 1850. That factor floats both concept weathers. simjob-20261020t185846-4e60751d4d81, exit 0. BETA is 1. Q is reverted to 0.33 and gamma to 0.20. Basis is endpoint. E is 293.6 GPa and strength is 379.2 MPa. The film is the favorable sheet. The core is CR-III. Vc is 1.323, inside the CR-1457 hemisphere step.

## The hull

Optimistic concept optimum, which is the design geometry. Face 3.216 mm. Core 178.71 mm. Joints, from the 040 formulas: film 1657 kg, scarf 391 kg, splice 1279 kg, seal 57 kg, together 3384 kg.

Lift is 132015 kg in both weathers. Concept optimistic: mass before growth 114873 kg, growth 17137 kg, payload +5.0 kg. Faces 73751 kg, core 32376 kg, weather headroom 1494 kg. The same geometry in ISA drops the headroom and carries +1499 kg. The same geometry at TRL 7 growth carries +11607 kg optimistic and +13101 kg ISA. An ISA re-optimum at the same density carries +3884 kg, with face 3.147 mm and core 176.21 mm.

Crushing margins at the design geometry, optimistic concept. Each tag is QUESTIONABLE.

| Mode | Value | Law |
| --- | ---: | --- |
| Global buckling | 1.000 | gamma 0.20 times unsourced kc = 1 − Vc/4, over face stress plus cure |
| Face wrinkling | 1.000 | BETA = 1 times Q = 0.33 (CR-1457 eq. 2.2-14) over demand |
| Thermal interface | 1.071 | unsourced interface shear |
| Scarf shear | 1.245 | 10 MPa over the scarf component of demand |
| Face strength | 1.554 | 379.2 MPa over demand |
| Core shear | 5.534 | CR-III Gc over demand |
| Core crush | 4.841 | twice the 040 crush stress over pressure |
| Dimpling | 138.0 | face bending stiffness over the cell |

## Graphite film, beside it

070 has filed. No gamma-0.20 case floats. The R 30 optimistic graphite hull is face 2.534 mm, core 158.3 mm, 969 GPa, 2250 kg/m3, payload −58888 kg. It still needs factor 1.659, to 1357 kg/m3. The factor that clears every concept weather and radius is 1.693, set by R 20 optimistic. The least R 30 factor is ISA at 1.574, and that case does not clear optimistic weather. At R 30, Vc is 3.36 in ISA and 3.45 in optimistic weather, outside the named CR-1457 support for gamma 0.20. Buckling and scarf shear bind together. Wrinkling is near 1.376 and the thermal interface near 1.071.

## TRL 7 on today's faces

Same radius, face density 1850, gamma factor 2.766987, realized gamma 0.553. This is the route T7 tests, and it is optimism of this alternative only. Optimistic optimum: face 2.510 mm, core 71.83 mm, payload +34 kg. Buckling and scarf shear are 1.00, wrinkling 1.12, face strength 1.25, thermal interface 1.07. ISA at that geometry is +1528 kg. At gamma 0.20 the TRL 7 optimistic hull is −52262 kg.

## Optimism ledger

Today's admissible value, the value used, the factor, and what would ground it.

| Item | Today | Used | Factor | Ground |
| --- | --- | --- | --- | --- |
| Face density | 1850 kg/m3 | 1013.825 | 1.825 | 068 graphite-film stack, compressed near 2.1 mm. No published sheet is at 1014. |
| BETA | 0.68233, the model root | 1, as 066 set it | 1.466 | Analysis. At the root this density resizes to −17249 kg and does not float. |
| kc | no opened equation | 1 − Vc/4 = 0.669 | DELTA-D without it, 1.459 | Analysis. Kept. Removing it and resizing frees 19044 kg, so the term is a penalty. |
| Pressure adder | P0 | P0·max(1.01, 1.03655) + wind | DELTA-D without it, 1.740 | Analysis. 040 names pinned 014b, which is not in SOURCE-INDEX. Resizing frees 3991 kg. |
| Cure stress | no opened equation | kept | DELTA-D without it, 1.769 | Analysis. Resizing frees 2587 kg. |
| Bond film | 0.14647 kg/m2 | 0.07324 kg/m2 | 2 | Weigh the installed film. The half-film is 2154 kg, and the hull then does not float. |
| Weather | ISA | optimistic | 1494 kg headroom | Analysis of QWEATHER, QWIND and the mass headroom. ISA still floats. |
| Gradient and bending | no opened equation | 11.3e-6, kept | DELTA-D without them, 1.809 | Analysis. Resizing frees 713 kg. |
| Modulus | 290 GPa | 293.6 GPa | 1.012 | At 290 GPa, buckling on this geometry is 0.994. Payload does not move. |
| Strength | 345 MPa | 379.2 MPa | 1.099 | T1, 038 SR-200 compression. Payload does not move, and the hull still clears. |
| Gamma, this hull | 0.20 | 0.20 | 1 | T7 before any gamma above 0.20. |
| Q, this hull | 0.33 | 0.33 | 1 | T3 before any Q above 0.33. Wrinkling of this SR-200/CR-III coupon. |
| Gamma, TRL 7 alternative | 0.20 | 0.553 | 2.767 | T7. Separate hull. |

COMMON.md, knockdown.md, SOURCE-INDEX and CARD-065 do not state kc, the cure coefficients, 11.3e-6, or the 1.01-and-wind pressure law. CR-1457 is cited there for gamma 0.20 and for Q 0.33 only. No named copy of CR-1457, of pinned 014b, or of 10.2514/3.5568 and 10.2514/3.1932 was opened. The four terms model real effects and stay in the hull as QUESTIONABLE estimates.

## What it must become, in order

1. A face near 1014 kg/m3 that keeps 294 GPa, or this hull is −69947 kg. The mirror-like graphite film is the materials direction and still needs 1.66 at this radius. T3 and T7 stay on SR-200 bonded to CR-III.
2. Earn BETA = 1. The model's own root leaves this density 17 t short.
3. Source kc before anyone spends the 19 t that appears when it is removed. Until then the light face is required.
4. Source the pressure adder, the cure stress, the halved film, the weather headroom, and the gradient and bending stress, in that order. Each is smaller than the face.
5. Run T3 before any Q above 0.33, and T7 before any gamma above 0.20. The TRL 7 alternative is that gamma test on today's faces. It is not a second hull to build on the design-point optimism.

Payload ranks are simjob-20261020t190027-d46b2325e338 and simjob-20261020t190103-258a311c915f, both exit 0. Fixed geometry does not change mass when only a margin term changes, so those ranks resize the shell at the design density.
