# MAINLINE-009b

QUESTIONABLE. Not a certification. The geometry is the filed MAINLINE-009 point. This card restates the global column. It does not search a new thickness and it does not score the P3 frame.

## The fix

MAINLINE-009 stated classical global buckling at knockdown 0.90 and at 0.1407. K_c was applied only at 0.20. The factor at 0.1407 then read 0.324151379344, above the handbook factor at 0.20, which is 0.23515931325. That ordering cannot occur when the safety factor is linear in the knockdown.

Re-derived on the stored thicknesses. Face 0.000272153646316 m, core 0.0462419048864 m, separation 0.0465140585328 m, R = 10 m, nu = 0.33. SiC E = 410 GPa. Divinycell H35 Gc = 12 MPa. sigma_0 = E*h/(R*sqrt(1-nu^2)). sigma_crimp = h^2*Gc/(2*tf*tc). Vc = sigma_0/sigma_crimp = 1.95855162232. The moderate branch gives Kc = 1 - Vc/4 = 0.510362094419 and gamma_d = 0.20. Neither stress contains the knockdown, so one Kc applies at every level.

Stated global safety factor at knockdown kd is Kc times the classical safety factor at that same kd.

| knockdown | classical, Kc omitted | stated, Kc applied |
| --- | --- | --- |
| 0.20 | 0.460769551307 | 0.23515931325 |
| 0.90 | 2.07346298088 | 1.05821690962 |
| 0.1407 | 0.324151379344 | 0.165434576871 |

1.05821690962 rounds to 1.058. 0.165434576871 rounds to 0.165. After the fix, 0.165 < 0.235 < 1.058.

The omitted pair is in the ratio 0.1407/0.90. Dividing the 0.90 classical factor by the 0.20 handbook factor gave 8.81726924709, which is 4.5/Kc. That reading is withdrawn. The knockdown gap 0.90/0.20 remains 4.5. MAINLINE-004b's ratio of about 6.4, from 0.90 against its own sealed SP-8032 value, stays beside this gap and is not overwritten.

gamma_d stays 0.20. Knockdown 0.90 is not a handbook gamma.

## Five modes

Face compression 4.44747498063, core crush 10.4754999207 and core shear crimping 1.17630177845 do not use the knockdown.

At 0.20, design wrinkling Q = 0.50 is 0.235167984044. The lesser factor is handbook buckling, 0.23515931325.

At 0.90 the restated global factor is 1.05821690962. Design wrinkling stays 0.235167984044, so wrinkling governs. 1.058 does not clear the point.

At 0.1407 the restated global factor is 0.165434576871, below design wrinkling, so buckling governs.

The point does not reach 1 in every mode.

## Wrinkling, two levels

Foam design Q is 0.50, NASA CR-1457 equation 2.2-5. The theoretical band stated for a perfect face is 0.78 to 0.91. The comparison value is 0.82. Hoff and Mautner 1945, Allen 1969 and Plantema 1966 were not opened. QUESTIONABLE.

At knockdown 0.20 the lesser factor stays 0.23515931325 at Q 0.50, 0.78, 0.82 and 0.91, because handbook buckling does not use Q. At 0.90 and Q 0.82, wrinkling is 0.385675493833 and still governs. At 0.1407 the lesser factor stays 0.165434576871 at both Q values.

The wrinkling-precision gap is (0.82/0.50)^3 = 4.410944 on Ec times Gc. The product factor 76.8892122204 at Q 0.50 becomes 17.4314641538 at Q 0.82. Still short of 1.

Honeycomb is not the point. On the Hexcel HRH-10-4.8-32 row of the same mass line, design coefficient 0.33 gives wrinkling 0.145667432154. Using 0.8 from equation 2.2-12 inside equation 2.2-14 gives wrinkling 0.353133168858, and the lesser of buckling and wrinkling becomes handbook buckling 0.26626666436. QUESTIONABLE.

## P3

P3 stays an alternative marked PENDING-011b. The SiC frame is not scored. Two modes are still absent from MAINLINE-011. Global lattice buckling is the robotics seat's equivalent-continuum estimate, about 0.70 perfect at the 6061 optimum and about 0.14 to 0.35 under a knockdown of 0.2 to 0.5. Member bending from the film line load has no number, unless every member is an arc of the sphere. Both are QUESTIONABLE and were not recomputed.

011b has not filed. 013 has not filed. 014 has filed as rpt-mainline014-grok-balanced-sandwich-1019. MAINLINE-009c is the re-run. This card does not absorb 014.

Float margin remains 0.05. Payload 244.472107509 kg. Total mass 4644.97004268 kg.
