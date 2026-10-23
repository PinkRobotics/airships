# MAINLINE-008b check — ref-cca93dbfd236dcaa3a8b

Unit vacuum-mainline008b-check-1019. Card rpt-ref-cc9cef5e55adca018a8f. Order ord-admiral-rr2-check008b-dispatch-1019.

Arithmetic log written with check008b.py in this directory. Times are measurements, not limits. Own formulas. The owner's compute.py was not run.

## Arithmetic

Aluminium P2-E safety factors from the COMMON sandwich formulas match 008 and 004b. Knockdown 0.140725695373 is the 004b card print. The fuller 004b RESULTS value 0.14072569537344654 changes a safety factor only past the printed digits.

878 comparisons against RESULTS.json. Worst relative difference 3.730e-5. That difference is P1 and P3 dividing by 005's printed five-significant-figure requirements. Dividing by the full 005 RESULTS requirements reproduces 005. The P3 section that reproduces 005 is the exact annulus, area pi(ro^2-ri^2) and inertia pi/4(ro^4-ri^4), outer radius 0.02 m.

The headline table matches those recomputed digits except two P3 yield cells, which follow the printed 1.4428e6 rather than 1442836:

| row | field | card | recomputed |
|---|---|---|---|
| SiC | P3 SFy | 0.8720 | 0.8719 |
| Graphene QI | P3 SFy | 0.4159 | 0.4158 |

No rank changes. P3 remains below 1 for every candidate. Best catalog product is Hexcel HRH-10-4.8-32, 76 MPa times 14 MPa = 1.064e15 Pa^2, the largest product 007 published. Filed file hashes 5/5. Six input pins and four order pins match.

Tags: thirteen QUESTIONABLE, CNT-yarn and graphene PROJECTION. Each candidate has a source.

## Mismatches

1. Closing paragraph, and the filed report: at kd 0.1407 no candidate passes buckling, best SiC 0.8529. The table's conservative column gives beryllium 1.0562. Yield still limits beryllium at 0.5817. SiC is second, 0.8529.

2. Best three at kd 0.20, the factor called a core-product factor. CNT 1.28, graphene 1.45 and M55J 1.65 equal 1/SF. The product ratio is the cube, 2.08, 3.08 and 4.47. The miss column already prints 2.1x, 3.1x and 4.5x. RESULTS factor_needed is 1/SF for every limit. For yield that is the property factor. For wrinkling the product moves by the cube.

3. On the 1 kg/m3 row at the conservative knockdown, the close names SiC 2.688, CNT 2.613 and beryllium 1.103. Graphene at 2.032 and M55J at 1.539 also clear a face factor of 1. M55J is yield-limited, so the knockdown does not reduce it.

4. NFI-008B-WRINKLE-FORMULA says the two HexWeb sheets carry no compressive modulus and that those products stay open. 007 records stabilised modulus 76 MPa on HRH-10-4.8-32 and 41 MPa on HRH-10-6.4-24, and the table uses 1.064e15 as the best product. 007's own note says a stabilised modulus is not the continuum Ec of the wrinkling formula.

## NFI from this check

NFI-CHECK-008B-BE-KD. State beryllium's conservative buckling factor, 1.0562, when the sentence is next touched. The table already has it.

NFI-CHECK-008B-PRODUCT. When the limit is wrinkling, quote the miss column for the product and 1/SF for the stress.

NFI-CHECK-008B-1KG. Add graphene and M55J to the conservative 1 kg/m3 clearers.

NFI-CHECK-008B-HEXWEB. Keep the continuum-modulus caveat. Do not say the HexWeb modulus was absent.

NFI-CHECK-008B-P3-DIGIT. The two P3 yield cells above. No rank change.

None of these stop the card or the next card.
