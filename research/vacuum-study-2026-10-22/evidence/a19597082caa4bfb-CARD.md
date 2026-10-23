# MAINLINE-009c

QUESTIONABLE. Not a certification. The P2 point is MAINLINE-014's beryllium S-200F row on Hexcel HRH-10-4.8-32. Thicknesses are not searched again. The P3 frame is not scored.

## The row

Face beryllium S-200F, QUESTIONABLE, rho 1850 kg/m3, E 303 GPa, compressive yield 283 MPa. Core Hexcel HRH-10-4.8-32, QUESTIONABLE, 32 kg/m3, Gc 14 MPa (W shear), Ec 76 MPa stabilised, crush 1.00 MPa. Each face is 0.000792920704344 m (0.793 mm). The core is 0.0217505960684 m (21.8 mm). R is 10 m. nu is 0.33.

014 built the row on the float ceiling, structural mass (lift − 100) / 1.05. Re-derived faces, core and joints close on the lift of 4889.44215019 kg. Payload is 0. Float margin is 0. MAINLINE-009's 5 percent margin is a different point.

CNT-yarn reaches 0.750340630448 on 014 and is tagged PROJECTION. It is not this point.

## Branch

Vc is 3.50800837286, above 2. The handbook then sets Kc = 1/Vc = 0.285062033413 and gamma_d = 1. Stated global buckling is gamma_d times Kc times the classical pressure. That product equals core shear crimping. It does not depend on the knockdown.

| knockdown | stated global | crimp | wrinkling at 0.33 |
| --- | --- | --- | --- |
| 0.20 | 0.685338231171 | 0.685338231171 | 0.685454960252 |
| 0.90 | 0.685338231171 | 0.685338231171 | 0.685454960252 |
| 0.1407 | 0.685338231171 | 0.685338231171 | 0.685454960252 |

0.685338231171 rounds to 0.685. Scaling it by kd/0.20 would put a knockdown on a branch whose gamma_d is already 1. That is the error MAINLINE-009b removed, run the other way. Kc is already in the factor at every level.

Face compression is 0.940266455786. Core crush is 20.9509998415. The lesser factor is the crimp pair, 0.685338231171. Wrinkling sits 0.00011672908 above it. The point does not reach 1. The factor on the crimp allowable is 1.45913354095.

## Wrinkling, two levels

Design coefficient 0.33 is NASA CR-1457 equation 2.2-14. Wrinkling safety factor 0.685454960252. The theoretical coefficient 0.82 is the value 014 names from Hemp, as quoted for anti-plane cores in NASA/CR-1999-208994. Those works were not opened. QUESTIONABLE. At 0.82 the wrinkling factor is 1.70325171941, and the lesser factor stays the crimp pair. Ec would scale by (0.82/0.33)^2 = 6.17447199265 to move the design wrinkling stress onto the theoretical coefficient. That move does not clear the point.

## P3

P3 stays PENDING-011b. Lattice buckling and member bending are still absent from MAINLINE-011. The SiC frame is not scored. 014b has not filed. MAINLINE-009d waits for it.

The NFI ledger is in POINT.json: crimp branch, Poisson ratio, face strength, stabilised modulus, wrinkling coefficient, crush, mass, CNT, 013, and the aluminium honeycombs that have no Ec.
