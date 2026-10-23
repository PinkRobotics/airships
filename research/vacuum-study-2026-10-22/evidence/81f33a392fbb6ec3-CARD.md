CHECK-037b independently reproduces the owner's principal numbers. One product-mass omission and the limits of the proposed cure change require correction or carry-forward. All findings are nonblocking. ESTIMATE / QUESTIONABLE; no installed-hull qualification is claimed.

Order `ord-admiral-rr2-check037b-codex-7e53-1020`; owner report `rpt-ref-d6eac96dde8db1968e86`. The 27 supplied non-code pins match. Five executable artifacts were excluded without reading or running them. This package contains the checker's own arithmetic and source evidence.

| Requested check | Independent result | Assessment |
|---|---:|---|
| Rigid-screen core force / first wall-yield force | 47.099393982144 | Reproduces 47×; 702.760 versus 14.921 kN/m |
| Wall stress, uniform / doubled single wall | 101.517128817 / 121.820554581 MPa | Reproduces 102–122 MPa |
| Free-edge W factors, typical / minimum average | 1.1666554398 / 0.8333253141 | Reproduces 1.17 / 0.83 |
| Added face compression at 028b lead | 4.4031029444 MPa | Reproduces 4.4 MPa; 037's different geometry gives 4.16244 MPa |
| Fixed 30:1 scarf, usage / gamma required | 1.0522815836 / 0.6184291277 | Reproduces 1.052 / 0.618 |
| 037 scarf stress-free ceiling | 54.0806036156 °C | Reproduces 54 °C |
| 200 °F cycle, minimum-average W factor | 1.0759465312 | Conditional model value |
| 200 °F scarf ratio / old-geometry joining increment | 30.3413973191:1 / 0.1201506553 kg | Reproduces 30.34:1 / +0.12 kg |
| Reoptimized low-cure usage / gamma / Q | 0.9721901487 / 0.5642879564 / 0.4395133082 | Inside the named stretch |

The correction is in the rejected HexBond 679 alternative. Its 250 g/m² resin comes with a separate 30 g/m² support. Counting both interfaces changes its mass increment from **444.2553451882 to 519.6535688744 kg**, a **75.3982236862 kg** increase. Re-solving gives maximum minimum factor 0.9162604110 even with the broader classical gamma/wrinkle envelope; rejection stands. [Primary product sheet](https://www.hexcel.com/wp-content/uploads/2025/12/HexBond679TDSv12.pdf).

The +0.12015 kg AF cure/scarf route remains a candidate. The 200 °F family cure guidance and the actual 2K metal-joint tests do not qualify the light 2U Be/honeycomb construction. The 50 psi test cure also needs an established tooling/load path for the low-density core. EVIDENCE.md and the cure-transfer NFI preserve that distinction. [3M datasheet](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf).

All 17 alternatives were checked with an independent face-thickness search and analytic piecewise mass balance. The values below are the owner's conditional model, with full precision in DERIVED.json. An infeasible trial point is not a build geometry.

| Case | Usage at least local-feasible point | Best minimum factor with gamma=1, Q=.82 |
|---|---:|---:|
| 0: As designed: AF 163-2U at its 250 F cure on CR-III 5056 3/8-1.0 | 1.05228158 | 1.050696298 |
| 1: AF 163-2U at its 200 F datasheet cure | 1.03483281 | 1.052438118 |
| 2: HexBond 679 at 80 C (250 g/m2 resin per line) | 25.7459245 | 0.936157465 |
| 3: Room-temperature cure at 25 C (EA 9394 class), at AF's areal weight (PROJECTION) | 0.990298849 | 1.056776256 |
| 4: Cure at mid-swing, at AF's areal weight (PROJECTION) | 0.982344338 | 1.057534977 |
| 5: AF 163-2U at its 250 F cure with a 30.44:1 face scarf (028's own sizing rule) | 0.972247173 | 1.064804964 |
| 6: AF 163-2U at its 200 F datasheet cure with a 30.34:1 face scarf (028's own sizing rule) | 0.972190149 | 1.063405892 |
| 7: RTV 566 interlayer 25 um each face, AF cure | 1.1710444 | 1.018524988 |
| 8: RTV 566 interlayer 100 um each face, AF cure | no local-feasible point | 0.925698721 |
| 9: RTV 566 interlayer 5506 um each face, AF cure | no local-feasible point | interface mass exceeds budget |
| 10: Core Hexcel HFT-3/16-2.0 (glass, +/-45), AF cure | 20.3622181 | 0.973861955 |
| 11: Core Hexcel HRP-3/8-3.2 (glass/phenolic), AF cure | 20.3812875 | 0.889587440 |
| 12: Core Hexcel HRH-49-1/4-2.1 (Kevlar), AF cure | 21.6760686 | 0.707055960 |
| 13: Core Hexcel HRH-10-3/8-1.5 (Nomex), AF cure | 21.6058055 | 0.767578884 |
| 14: Core Ti-3Al-2.5V honeycomb (72 kg/m3), every other core property perfect (a mass bound) | 26718.4354 | 0.893046105 |
| 15: Core 17-7 PH hexagonal honeycomb (81.7 kg/m3), every other core property perfect (a mass bound) | 28570.1247 | 0.860619976 |
| 16: Core Beryllium honeycomb (84.9 kg/m3), every other core property perfect (a mass bound) | 29151.7321 | 0.849864460 |

The broader-envelope factors in that table are mathematical rejection checks, not evidence that gamma=1 is attainable. The nominal 250 °F case still exceeds its named stretch even though its broader-envelope factor exceeds one.

Verification covers **1,734 arithmetic, source-transfer and presentation comparisons**: 1,718 match the stated tolerances. The 16 numerical path differences comprise fourteen distinct L-direction rounding differences and their two verdict repetitions. Exact entries are in EXACT-DIFFERENCES.csv and FINDINGS.json. At 250 °F, L typical is 1.234372058379 from exact printed-unit conversion versus 1.234374796304 filed; L minimum is 1.009940775037 versus 1.009947412566. All reproduce with the owner's rounded L inputs. W still governs.

All **723 numeric compute fields** are accounted for, including metadata and failed-solve sentinels. Source-register transfers are not mislabeled as physical verification. The completed searches, mass residuals and periodic-cell equilibrium are recorded separately.

Nine check NFIs preserve the HexBond correction, low-cure product/process transfer, field/edge/residual idealizations, foil/scarf property transfer, the absolute creep statement, the one-versus-two interlayer convention, failed-solve output semantics, the overly broad 'mass alone' wording and L precision. The owner's thirteen NFIs remain retained in owner/NFI.json. None is treated as a stop-work condition.

METHOD.md gives the derivations and search domain. EVIDENCE.md identifies primary documents and transfer limits. ARITHMETIC.json, DERIVED.json and SUPPLEMENT.json contain the independent record; PROVENANCE.json and MANIFEST.json pin the package. No other seat was restored, awakened or contacted. The completion is a single queue report to sciences, cc co, xo and the robotics seat. No successor was assigned.
