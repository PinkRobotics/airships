# MAINLINE-060: the carbon-framed P3. ESTIMATE

Unit vacuum-mainline060-p3-carbon-frame-1020. Order ord-admiral-rr2-060-untimed-1020, which replaced ord-admiral-rr2-mainline060-dispatch-1019 to drop its deadline. Status ESTIMATE. Values are QUESTIONABLE, and PROJECTION where named. Nothing here is a certification. Started 06:58:23 PDT when the order was read; the end time is in RESULTS.json. Times are measurements, not limits.

## The answer

- **Does a carbon-framed P3 float? No, at no radius from 10 to 30 m, on sourced compression.** That holds even at mean strength, with all of 052's endpoint optimisms and ground vacuum service. The best case at mean strength is M55J 50/20/20/10: -470 kg at R 10 ISA and -4,624 kg at R 30. A frame sized to mean strength fails with Pf near 1, so it is not a design. The best-supported frame is the lightest that meets 051's Pf 1e-3 with carbon's own scatter: M55J 70/10/10/10, walls x1.32. It gives -2,044 kg at R 10 ISA and -47,116 kg at R 30.
- **On which optimisms it would float.** Only the light pitch layups can float, and only if their compression is ignored: K13D2U 50/20/20/10 from R 10, and K13D2U 70/10/10/10 from R 12. At its stiffness wall K13D2U 50/20/20/10 gives +619 kg at R 10 ISA and +24,765 kg at R 30. At R 10 it still floats with 052's optimistic weather, its baseline film and joint axes and seven days of dry cavity together (+258 kg). So the one optimism that matters is compression. Its tubes must carry at least 0.59 GPa of laminate compression at mean, 3.1 times the sourced 0.19 GPa. That needs a UD 0 deg strength of 1.06 GPa at mean. For Pf 1e-3 it needs 1.94 GPa, or 3.07 GPa with coupon-to-tube size scaling. The sourced value is 340 MPa. The second optimism is 052's lean SiC joint bill: with titanium end fittings at the sourced Boeing strut share, it floats only from R 12.
- **Is it a better lead than SiC? No.** SiC floats on paper (+31 kg at R 10 ISA), with one unknown: its whole-tube strength. The light carbon layup misses by a factor of three in compression on sourced data. The PAN layups that are strong enough are stiffness-heavy: M55J 50/20/20/10's tubes weigh 1.120 times SiC's, and P3 floats only below 1.007 (R 10) to 1.079 (R 30). Carbon's real advantage is damage (below) and tight scatter (m about 20 against SiC's assumed 10). Neither closes the strength gap.
- **The single test that would ground it.** Compress about 30 full-length wrapped K13D2U 50/20/20/10 tubes (2.4 m, 247 mm outer diameter, 1.45-1.70 mm wall) with their end fittings, to failure. At R 10 the frame floats only if the tubes carry a laminate mean of at least 0.59 GPa. For Pf 1e-3 it also needs a whole-tube Weibull scale of at least 1.12 GPa at m 20. Sourced data predict 0.19 GPa, so the test is more likely to close the option than to open it. A flat-laminate compression coupon of the same layup is the cheap first gate.

## 1. What the tubes carry

**Sourced 0 deg compressive strength of unidirectional laminates (data sheets, 60% fibre volume, epoxy; all QUESTIONABLE):**

| Fibre (class) | UD compression, MPa | UD modulus, GPa | Source |
|---|---|---|---|
| DIALEAD K13C6U | 340 | 550 | Mitsubishi Rayon Co., Ltd. |
| DIALEAD K13D2U | 340 | 560 | Mitsubishi Rayon Co., Ltd. |
| GRANOC YS-95A | 340 | 540 | Nippon Graphite Fiber Corp. |
| DIALEAD K13916 | 360 | 430 | Mitsubishi Rayon Co., Ltd. |
| GRANOC YS-90A | 360 | 520 | Nippon Graphite Fiber Corp. |
| Dialead K63712 | 374 |  | Montagnier and Hochard (measured) |
| DIALEAD K13C2U | 380 | 560 | Mitsubishi Rayon Co., Ltd. |
| DIALEAD K63A12 | 380 | 470 | Mitsubishi Rayon Co., Ltd. |
| GRANOC YS-80A | 380 | 460 | Nippon Graphite Fiber Corp. |
| DIALEAD K1392U | 400 | 420 | Mitsubishi Rayon Co., Ltd. |
| DIALEAD K63712 | 440 | 330 | Mitsubishi Rayon Co., Ltd. |
| DIALEAD K1352U | 450 | 250 | Mitsubishi Rayon Co., Ltd. |
| DIALEAD K13312 | 540 | 160 | Mitsubishi Rayon Co., Ltd. |
| Toray M60J | 785 |  | Toray Carbon Fibers Europe |
| Toray M60J | 790 |  | Toray Composite Materials America |
| Toray M55J | 880 |  | Toray Carbon Fibers Europe |
| Toray M55J | 890 |  | Toray Composite Materials America |
| Toray M46J | 1080 |  | Toray Carbon Fibers Europe |
| GRANOC XN-15 (155 GPa low-modulus pitch) | 1150 |  | Nippon Steel Corp. |
| PAN-CF 230 GPa class | 1400 |  | Nippon Steel Corp. |
| Toray T800S | 1490 |  | Toray Composite Materials America |

- **Pitch fibres:** the ultra-high-modulus pitch fibres carry 340-380 MPa. The best pitch value, 540 MPa, belongs to a 160 GPa fibre. The one independent measurement (K63712, Montagnier and Hochard) found 374 MPa against the maker's 440, 15% lower.
- **High-modulus PAN fibres:** 785-1,080 MPa. A 2025 Nippon Steel report gives a compression-to-tension ratio of 0.5 for a 230 GPa PAN fibre and 0.79 for a 155 GPa pitch fibre.
- **Scatter:** the coefficient of variation of compressive strength is 5.1% (K63712, n=6) and 5.198% (an NCAMP IM fibre). CMH-17 expects at least 6%. These give m = 1.2/CV of about 20-23.5 (PROJECTION).
- **Not found:** tube or strut compression tests, quasi-isotropic or multidirectional laminate compression, and a Weibull modulus, for any pitch or M-series fibre.

**What 50/20/20/10 gives.** The 0 deg ply fails first. Per unit of laminate stress, 051's laminate model puts 1.7875 on that ply. The laminate's mean first-ply compression is therefore 340/1.7875 = 0.190 GPa (PROJECTION). Its Weibull scale is 0.200 GPa at m 10 and 0.195 GPa at m 20. **That is 11.4 times below 051's 2.16 GPa** (10.8 times in scale at m 10). Reaching 2.16 GPa at m 10 would need a 0 deg ply strength of 3.68 GPa, above every sourced carbon laminate (T800S 1490 MPa). At 051's own stiffness-sized wall the tubes carry 0.695 GPa at q 1: a mean safety factor of 0.274.

**Every construction at 051's 019-reserve witness (tube mass scales with wall; peak stress with 1/wall):**

| Construction | UD strength, MPa | 0 deg ply ratio | Laminate mean, GPa | Witness tubes, kg | Peak at q 1, GPa | Mean SF | Wall for mean | Wall for Pf 1e-3 (CV 5.2 / 6%) | With size scaling (CV 6%) | Pf at witness (CV 6%) |
|---|---|---|---|---|---|---|---|---|---|---|
| K13D2U 50/20/20/10 | 340 | 1.787 | 0.190 | 3,610 | 0.695 | 0.274 | x3.65 | x6.21 / x6.69 | x11.90 | 1 |
| K13D2U 70/10/10/10 | 340 | 1.355 | 0.251 | 4,267 | 0.584 | 0.430 | x2.33 | x3.96 / x4.26 | x7.46 | 1 |
| K13D2U UD | 340 | 1.000 | 0.340 | 8,689 | 0.285 | 1.193 | x1.00 | x1.43 / x1.54 | x2.65 | 0.995 |
| M55J 50/20/20/10 | 890 | 1.774 | 0.502 | 4,704 | 0.484 | 1.037 | x1.00 | x1.64 / x1.76 | x2.98 | 1 |
| M55J 70/10/10/10 | 890 | 1.352 | 0.658 | 4,775 | 0.474 | 1.390 | x1.00 | x1.22 / x1.32 | x2.19 | 0.216 |
| M55J UD | 890 | 1.000 | 0.890 | 8,725 | 0.257 | 3.463 | x1.00 | x1.00 / x1.00 | x1.00 | 2.94e-09 |
| T700S 50/20/20/10 | 1450 | 1.700 | 0.853 | 11,024 | 0.199 | 4.292 | x1.00 | x1.00 / x1.00 | x1.00 | 3.9e-11 |
| T700S 70/10/10/10 | 1450 | 1.329 | 1.091 | 8,876 | 0.246 | 4.430 | x1.00 | x1.00 / x1.00 | x1.00 | 2.03e-11 |
| T700S UD | 1450 | 1.000 | 1.450 | 8,849 | 0.245 | 5.906 | x1.00 | x1.00 / x1.00 | x1.00 | 6.51e-14 |

The T700S strength is 051's Toray value, not re-sourced here. T700S frames are stiffness-limited, so it does not decide anything.

## 2. The whole bill

**Method.** 052's account is used line by line, ground service, R 10-30.
- **Tubes:** the SiC tubes are replaced by 052's stiffness-sized SiC tubes x (051's carbon witness / 051's 041 reference witness) x the wall factor.
- **Kept unchanged:** the film (PBO plies, barrier and protection), the joint lines (sleeves, bond, nodes), systems, vacuum service, gas, water, contamination, mooring, sag and weather headroom.
- **Lift:** 052's card endpoint payload plus its endpoint bill (checked below against R^3 and 054's lift).
- **Dry cavity:** 054's increment over ground service. One day is the MET barrier; seven days are the SiOx barrier plus a 3A sieve. These are 054's R 10-15 rows; R 20 and 30 are extrapolated (barrier as R^2, capture as a + bR^2; PROJECTION). 054's ALD and ML3 carriers are not used, as 054 did not verify them.

**Line by line at R 10, ISA, 052's endpoints, kg:**

| Line | SiC (052) | K13D2U 50/20/20/10, stiffness wall | K13D2U 50/20/20/10, mean strength | M55J 50/20/20/10, mean strength | M55J 70/10/10/10, Pf 1e-3 |
|---|---|---|---|---|---|
| tubes | 4,182.2 | 3,594.5 | 13,135.9 | 4,683.0 | 6,256.7 |
| joint sleeves and allowance | 34.3 | 34.3 | 34.3 | 34.3 | 34.3 |
| joint bond and installation | 10.1 | 10.1 | 10.1 | 10.1 | 10.1 |
| nodes | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 |
| PBO two plies | 95.3 | 95.3 | 95.3 | 95.3 | 95.3 |
| barrier and protection | 95.8 | 95.8 | 95.8 | 95.8 | 95.8 |
| systems | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| vacuum service | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 |
| gas | 48.9 | 48.9 | 48.9 | 48.9 | 48.9 |
| exterior water | 125.7 | 125.7 | 125.7 | 125.7 | 125.7 |
| contamination | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 |
| mooring load introduction | 33.1 | 33.1 | 33.1 | 33.1 | 33.1 |
| sag lift debit | 73.1 | 73.1 | 73.1 | 73.1 | 73.1 |
| weather headroom | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **total** | 4,858.6 | 4,270.8 | 13,812.2 | 5,359.3 | 6,933.1 |
| lift | 4,889.4 | 4,889.4 | 4,889.4 | 4,889.4 | 4,889.4 |
| **payload, ground** | +30.9 | +618.6 | -8,922.8 | -469.9 | -2,043.6 |
| dry cavity, 1 day | 0.15 | 0.15 | 0.15 | 0.15 | 0.15 |
| dry cavity, 7 days | 29.7 | 29.7 | 29.7 | 29.7 | 29.7 |

**Payload by radius, ISA, 052's endpoints, kg (ground / 1 day / 7 days of dry cavity):**

| Frame | R 10 | R 12 | R 15 | R 20 | R 30 |
|---|---|---|---|---|---|
| SiC (052) | +31 / +31 / +1 | +232 / +231 / +191 | +727 / +727 / +666 | +2,234 / +2,234 / +2,129 | +8,896 / +8,894 / +8,665 |
| K13D2U 50/20/20/10, stiffness wall (strength ignored) | +619 / +618 / +589 | +1,247 / +1,247 / +1,207 | +2,711 / +2,711 / +2,650 | +6,937 / +6,936 / +6,831 | +24,765 / +24,764 / +24,535 |
| K13D2U 50/20/20/10, mean strength | -8,923 / -8,923 / -8,953 | -15,240 / -15,241 / -15,281 | -29,491 / -29,492 / -29,552 | -69,395 / -69,395 / -69,500 | -232,852 / -232,854 / -233,083 |
| K13D2U 50/20/20/10, Pf 1e-3, CV 6% | -19,840 / -19,840 / -19,870 | -34,106 / -34,106 / -34,146 | -66,338 / -66,338 / -66,399 | -156,735 / -156,736 / -156,840 | -527,627 / -527,628 / -527,857 |
| M55J 50/20/20/10, stiffness wall (strength ignored) | -470 / -470 / -500 | -634 / -634 / -674 | -963 / -963 / -1,024 | -1,771 / -1,772 / -1,877 | -4,624 / -4,625 / -4,855 |
| M55J 70/10/10/10, Pf 1e-3, CV 6% | -2,044 / -2,044 / -2,073 | -3,353 / -3,353 / -3,394 | -6,274 / -6,275 / -6,335 | -14,362 / -14,362 / -14,467 | -47,116 / -47,117 / -47,347 |
| M55J UD, Pf 1e-3, CV 6%, size-scaled | -4,474 / -4,474 / -4,504 | -7,553 / -7,553 / -7,594 | -14,477 / -14,477 / -14,538 | -33,805 / -33,805 / -33,910 | -112,736 / -112,738 / -112,967 |
| T700S 70/10/10/10, stiffness wall (strength ignored) | -4,624 / -4,624 / -4,654 | -7,812 / -7,813 / -7,853 | -14,984 / -14,984 / -15,045 | -35,006 / -35,007 / -35,111 | -116,791 / -116,792 / -117,022 |

052's optimistic-weather case and its baseline axes (PBO ply 3.48 GPa, retention 0.8616, sleeves at 5% of the tubes) lower every row. For example, M55J 70/10/10/10 at Pf 1e-3 gives -2,175 kg (optimistic weather) and -2,405 kg (baseline axes) at R 10. All rows are in CARBON.json.

**The cubic penalty.** Carbon tubes scale as R^3, like lift. P3 floats only while the tube bill stays below 1.0074 times SiC's at R 10, 1.0515 at R 15 and 1.0788 at R 30 (ISA endpoints). So a construction heavier than that never floats at any size. At its stiffness wall, M55J 50/20/20/10 is 1.1197 and M55J 70/10/10/10 is 1.1368. The light pitch layup is 0.8595, so it floats only below a wall factor of 1.172 (R 10) to 1.255 (R 30).

**Joints (QUESTIONABLE).** 052's SiC joint bill is kept: 34.3 kg of sleeves at R 10. Carbon tubes need bonded end fittings, so the sourced strut fitting shares are used as a sensitivity:
- **Boeing 44K strut:** titanium insert and ball are 16.9% of the strut, or 0.203 times the tube. Even the strength-ignored K13D2U 50/20/20/10 frame then gives -76 kg at R 10, and floats only from R 12 (+6,005 kg at R 30).
- **Typical space strut:** fittings are 70% of the strut, or 2.33 times the tube. No frame floats.
- **Load:** each tube carries up to 775 kN (174 klb) at q 1. That is 1.43 times the largest sourced composite strut failure (121.7 klb, Northrop Grumman NG-2). Bonded-fitting struts failed at about 70% of their compressive design ultimate.

## 3. Reliability and damage

**Pf with carbon's own scatter.** This uses 051's frame sum, H = 0.0010005 (k(m) peak / scale)^m, and 051's k(m) for each construction (Pf 1e-3, operating). The scale is the sourced mean / Gamma(1 + 1/m), with m from the coefficient of variation.
- **Size scaling:** the size-scaled reading moves the coupon scale (a 0.32 cm3 compression gauge; PROJECTION) to one tube's volume as (V coupon / V tube)^(1/m).
- **At the stiffness walls:** Pf is near 1 for both multidirectional K13D2U layups, K13D2U UD (0.995) and M55J 50/20/20/10. M55J 70/10/10/10 is 0.22.
- **To meet 1e-3:** at CV 6% the walls must be x1.32 (M55J 70/10/10/10) to x6.69 (K13D2U 50/20/20/10). With size scaling they must be x2.19 to x11.90.
- **Already below 1e-3:** M55J UD and every T700S frame, at their stiffness walls, at 6.6e-05 and below with size scaling. They are the heavy ones.
- **Scatter:** carbon's scatter is tight (m about 20 against SiC's assumed 10), so its size penalty is mild (x0.56-0.64). Its mean strength is the problem.

**Design hail on a carbon tube.** 051's design strike is 50.8 mm ice at 32.0 m/s: 28.5-32.3 J over the sourced natural-hail density range of 810-920 kg/m3.
- **Ice on flat carbon panels.** Ice first delaminates a 1.59 mm quasi-isotropic T800 panel at 254 J with 50.8 mm ice; the source prints "254 J to 263 J (93 to 94 m/s)" (FAA JAMS, Kim et al. 2010, an interim table). That is 7.9 times the design energy. The threshold is linear in thickness: 39 + 134 J/mm, so 233 J at the pitch layup's 1.45 mm wall (x7.3). AS4/8552 at 4 mm needs 667 J with 50 mm ice. On these data a design strike most likely leaves the laminate intact, unlike SiC's 1-5% fracture per strike (045, 051).
- **Hard impactors.** 20 J punctured 76-102 mm CFRP tubes, and barely visible damage needs 10.8-20 J on 4 mm laminates. These are not ice, but they show what a thin carbon wall gives up. If a strike does delaminate, the one paired compression-after-impact row keeps 52% (202/385 MPa at 50 J, 5 mm).
- **Quasi-static stress (051's method, extended as a power of the wall; PROJECTION).** The strike adds 159 MPa of surface stress at the pitch layup's stiffness wall, and 100 MPa at M55J 50/20/20/10's. At M55J 50/20/20/10's wall the mean strength left after the operating load is only 18 MPa, so a strike exceeds it 5.6 times over. At M55J 70/10/10/10's Pf 1e-3 wall it takes 28% of the 299 MPa left.
- **Not sourced:** ice on pitch-fibre laminates, ice on tubes, walls below 1.5 mm, and members under compressive preload.

## 4. What the light frame must carry to float

K13D2U 50/20/20/10, ISA, 052's endpoints. The largest wall factor that still floats, and the compression it then needs:

| R, m | Service | Payload at stiffness wall, kg | Max wall factor | Laminate mean, GPa | UD 0 deg at mean, GPa | UD for Pf 1e-3, CV 5.2 / 6%, GPa | Same, size-scaled, GPa | Whole-tube scale at m 20, GPa |
|---|---|---|---|---|---|---|---|---|
| 10 | ground | +619 | 1.172 | 0.593 | 1.060 | 1.80 / 1.94 | 2.68 / 3.07 | 1.116 |
| 10 | one day | +618 | 1.172 | 0.593 | 1.060 | 1.80 / 1.94 | 2.68 / 3.07 | 1.116 |
| 10 | seven day | +589 | 1.164 | 0.597 | 1.068 | 1.82 / 1.95 | 2.70 / 3.09 | 1.123 |
| 12 | ground | +1,247 | 1.201 | 0.579 | 1.035 | 1.76 / 1.89 | 2.62 / 3.00 | 1.089 |
| 12 | one day | +1,247 | 1.201 | 0.579 | 1.035 | 1.76 / 1.89 | 2.62 / 3.00 | 1.089 |
| 12 | seven day | +1,207 | 1.194 | 0.582 | 1.040 | 1.77 / 1.91 | 2.64 / 3.02 | 1.095 |
| 15 | ground | +2,711 | 1.223 | 0.568 | 1.016 | 1.73 / 1.86 | 2.58 / 2.95 | 1.069 |
| 15 | one day | +2,711 | 1.223 | 0.568 | 1.016 | 1.73 / 1.86 | 2.58 / 2.95 | 1.069 |
| 15 | seven day | +2,650 | 1.218 | 0.571 | 1.020 | 1.73 / 1.87 | 2.59 / 2.96 | 1.073 |
| 20 | ground | +6,937 | 1.241 | 0.560 | 1.001 | 1.70 / 1.83 | 2.54 / 2.91 | 1.053 |
| 20 | one day | +6,936 | 1.241 | 0.560 | 1.001 | 1.70 / 1.83 | 2.54 / 2.91 | 1.053 |
| 20 | seven day | +6,831 | 1.238 | 0.562 | 1.004 | 1.71 / 1.84 | 2.55 / 2.92 | 1.057 |
| 30 | ground | +24,765 | 1.255 | 0.554 | 0.990 | 1.68 / 1.81 | 2.51 / 2.88 | 1.042 |
| 30 | one day | +24,764 | 1.255 | 0.554 | 0.990 | 1.68 / 1.81 | 2.51 / 2.88 | 1.042 |
| 30 | seven day | +24,535 | 1.253 | 0.555 | 0.992 | 1.69 / 1.82 | 2.52 / 2.88 | 1.044 |

Sourced K13D2U is 340 MPa. So the requirement is about three times the data at mean, and five to nine times for the reliability target.

## Method and limits

- **Witnesses:** 051's 019-reserve witnesses, because 052 resizes that family. The 5%-reserve K13D2U 50/20/20/10 witness has 1.3% more tube mass (3,655.7 against 3,610.3 kg).
- **Wall scaling (PROJECTION):** walls thicken uniformly at fixed radius. Peak stress goes as 1/wall and mass as wall. Thicker walls also cut Euler amplification, so this is conservative. 051's FE was not re-run.
- **First-ply failure:** the 0 deg ply's failure is taken as the laminate's (PROJECTION). No laminate data test it.
- **Not explored:** film and joint redesign, hybrid layups (PAN 0 deg plies over pitch), and other tube radii.

## Checks

- **Lift:** taken as 052's card payload plus its bill, it scales exactly as R^3 (4.88944 R^3 kg in both weathers). It matches 054's own lift column at R 10-15 within 0.5 g.
- **Cavity:** 054's one- and seven-day increments equal its barrier change plus its capture hardware within 0.5 g at R 10-15, and no other line moves. The capture fit reproduces R 12 within 0.5%.
- Every sourced value is asserted against its row (sources_used in CARBON.json and EXTRA.json).
- The Pf-sized walls give Pf = 1.000e-3 when recomputed, with and without size scaling.
- No sized carbon row floats; the script asserts it.

## Reproduce

In the outputs folder, run `python3 carbon60.py`, then `python3 extra60.py`, then `python3 card60.py`. Each runs in under two seconds on one core.

## Then

Stop and file. The robotics seat sends the next job. NFI.json carries the open rows.
