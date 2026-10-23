# MAINLINE-073 — design point under the equibiaxial wrinkling law

Unit `vacuum-mainline073-equibiaxial-wrinkling-1022`. Seat ref-54f4f7dcfd67e7445c6b. Tag QUESTIONABLE / PROJECTION. Every recomputed row is UNREVIEWED. No qualified hull safety factor. No finite-element run.

simjob `simjob-20261022t095337-eb517fa6490c` admitted 2 cores and 4 GiB and exited 0 after 108 s. Runner `run073.py`. Copied model63.py sha256 `2c44efb4bb78a17d61219eb2595a614af86dc7a04c765b4f906a9207c96f95ff` (19294 bytes, the 069 pin) before the edit, and `534cd01fb8f510fdc47b25a0d4aad9b5a203dc424fa9ad787cb514ec9a9aa572` (19438 bytes) after it. The only code change is the face-wrinkling line. BETA is set to 1. Revert is Q and gamma, so Q stays 0.33 and the hemisphere floor stays γ = 0.20. kc, cure, gradient, bending and the pressure adder stay as version 8 carries them.

## 1. The law

CR-1457 section 2.2.2.2. Equation (2.2-14), initial waviness unknown, elastic η = 1, is the uniaxial lower bound for a honeycomb sandwich: σ_wr = 0.33 sqrt(Ef Ec tf/tc). Equation (2.2-15), when both facings are in compression: Rx³ + Ry³ = 1, with Ri the applied compression divided by the critical compression acting alone (2.2-16). Equibiaxial, Rx = Ry, so the allowable is (1/2)^(1/3) = 0.793700525984 times the uniaxial bound. The face stress must fall by 1.259921, or the sphere must be shown exempt.

Admissibility: **admissible with a named limit.** The sweep was allowed to run.

Limits. (2.2-14) and (2.2-15) are flat-panel honeycomb recommendations, not a measured allowable for SR-200 on CR-III. (2.2-15) is not a pressurized-sphere series. It applies here because the membrane field is equibiaxial. It does not cover a wrinkle whose wavelength is long beside R; that wavelength was not checked. The margin still divides by a demand that adds cure, gradient and bending, which are absent from CR-1457 and from DOI 10.2514/3.5568 and DOI 10.2514/3.1932. Those terms stay QUESTIONABLE. They were kept because the card says to carry version 8. The copied buckling stress uses E h / (R sqrt(1−ν²)). Handbook (4.2-3) uses the one-quarter power. That difference was not edited.

Exemption. One principal membrane stress is not compressive, or a test of this sandwich under equibiaxial compression, or under external pressure on a sphere or dome, returns an allowable above (1/2)^(1/3) times the uniaxial lower bound.

## 2. Control, then the new closures

At 069's filed geometry (R 30, optimistic, concept, factor 1.824771768877316, tf 3.216 mm, tc 178.7 mm) the untouched law reproduces payload +5.031483 kg and wrinkling 1.000000022. The equibiaxial law on that same geometry leaves every other mode unchanged and drops wrinkling to 0.793700544. The mass residual is still +5.031 kg. The point does not float.

Least face density is the lightest face with payload at least zero and every mode at least 1. Order is R 20 ISA, R 20 optimistic, R 30 ISA, R 30 optimistic. Factors rose by 1.107 to 1.113, not by 1.260: the re-optimized face is thicker, and density pays the rest. Wrinkling and global buckling co-bind at 1.000 on every closure. Concept and TRL 7 share geometry at a given radius and weather, because those modes do not use maturity. Maturity changes the density that zeros the payload.

| maturity | case | factor | filed | kg/m3 | filed kg/m3 | payload kg |
|---|---|---:|---:|---:|---:|---:|
| concept | R20 ISA | 1.9688 | 1.779 | 939.7 | 1039.9 | +0.002 |
| concept | R20 optimistic | 2.0628 | 1.863 | 896.8 | 993.0 | +0.003 |
| concept | R30 ISA | 1.9320 | 1.743 | 957.6 | 1061.4 | +0.009 |
| concept | R30 optimistic | 2.0235 | 1.825 | 914.3 | 1013.7 | +0.009 |
| TRL 7 | R20 ISA | 1.7158 | 1.544 | 1078.2 | 1198.2 | +0.003 |
| TRL 7 | R20 optimistic | 1.7946 | 1.614 | 1030.8 | 1146.2 | +0.002 |
| TRL 7 | R30 ISA | 1.6891 | 1.519 | 1095.2 | 1217.9 | +0.009 |
| TRL 7 | R30 optimistic | 1.7662 | 1.587 | 1047.5 | 1165.7 | +0.009 |

The 993 and 1146 kg/m3 targets are the two R 20 optimistic cells. They become 896.8 and 1030.8 kg/m3. 069's design density 1013.825 kg/m3, factor 1.824772, is the precise form of the printed 1.825.

R 30 geometry. ISA: tf 3.587 mm, tc 164.4 mm. Optimistic: tf 3.668 mm, tc 167.0 mm. Same figures at TRL 7.

R 30 optimistic concept bill, UNREVIEWED: faces 75858.874 kg, core 30260.544 kg, charged joining 3394.376 kg, mass before growth 114876.227 kg, growth 17138.702 kg, lift 132014.938 kg, payload +0.009 kg. Modes: wrinkling 1.000, buckling 1.000, face compression 1.773, thermal interface 1.071, core crush 4.841. Q 0.33, γ 0.20, Vc 1.503.

R 30 ISA concept: faces 77682.926 kg, core 29777.454 kg, joining 3357.607 kg, mass 114686.130 kg, growth 17328.799 kg, payload +0.009 kg. Thermal 1.071, crush 4.967, Vc 1.470.

R 30 TRL 7 uses those geometries. Optimistic: faces 86910.417 kg, core 30260.543 kg, joining 3394.376 kg, mass 125927.769 kg, growth 6087.160 kg, payload +0.009 kg. ISA: faces 88853.412 kg, core 29777.454 kg, joining 3357.607 kg, mass 125856.617 kg, growth 6158.313 kg, payload +0.009 kg.

## 3. TRL 7 on today's 1850 kg/m3 faces

The γ that floats R 30 is the optimistic root, and it also floats ISA. Factor 3.2035729948565477, realized γ 0.6407145989713096, beside filed factor 2.7669873295303313 and realized 0.5533974659060663. The filed optimum payload at that older factor was +33.823 kg, so the filed factor was not a zero-payload root. The new optimistic root payload is +0.004 kg. Geometry: tf 2.561 mm, tc 60.5 mm. Wrinkling and buckling co-bind; scarf shear is third at 1.023. ISA alone would close at factor 2.9225964350158016, realized γ 0.5845192870031604. At the common factor, ISA payload is +3963.234 kg.

## 4. Tests, in priority order

T3 has to be equibiaxial. CARD-065 defines T3 as a wrinkling coupon, and the review record keeps it on SR-200 bonded to CR-III, to measure elastic wrinkling. A uniaxial coupon admits (2.2-14) only. It does not admit the interaction that now sets the face density. A pressurized sphere or dome of this sandwich would also serve.

1. The equibiaxial allowable of this sandwich, (1/2)^(1/3) times the uniaxial lower bound, including the curvature limit.
2. Face density under that law. Concept R 30 optimistic is 914.3 kg/m3. The R 20 optimistic pair is 896.8 and 1030.8 kg/m3.
3. Cure, gradient, bending and the pressure adder. They stay in the margin and are still unsourced.
4. kb and dtc, so the thermal screen near 1.071 can be checked.

kc = 1 − Vc/4 stands, from (4.2-4) used on domes in (6.2-1), with the hemisphere-data limit already on the record. It is not a new test.

## 5. Custody

This seat still holds the rebuilt admitted version 8, sha256 `dede05e82b02973f6d4b2d79170dd9930563bc0500ce63717897c62da70040c7`. Nothing was written into the owner's record. DELTA-E was not started. The robotics seat sends the record delta next.
