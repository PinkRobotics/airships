# MAINLINE-005 strength limits, all three families — ESTIMATE_PENDING_CHECKER

Unit vacuum-mainline005-strength-limits-1019. Owner arithmetic from the pinned MAINLINE-002/003 rows; every limit below was recomputed from its formula and matches the pinned RESULTS. Nothing here is a certification.

Case: evacuated sphere, external radius 10 m, internal pressure 0, external pressure 95460.8379139 Pa at 500 m ISA. Knockdown kd = 0.2 throughout. Every buckling requirement scales as 1/kd: E_required(kd) = E_required(0.2) x 0.2/kd, so MAINLINE-004's curve is one multiplication. Every required compressive strength is the membrane stress at external pressure and does not depend on the assumed 276 MPa (Una's 003 correction). That 276 MPa stays QUESTIONABLE, a typical tensile yield transferred to compression.

6061-T6 figures beside every requirement: E/rho^2 = 9451.3 Pa per (kg/m3)^2, E/rho = 2.5519e7 Pa per (kg/m3), sigma/rho = 1.0222e5 Pa per (kg/m3), at rho = 2700 kg/m3.

## Family P1, simple shell. Equal-mass figures: buckling E/rho^2, yield sigma/rho

At fixed shell-plus-joints mass the thickness follows 1/rho, so buckling pressure follows E/rho^2 and yield pressure follows sigma/rho.

| row | t (m) | E required (Pa) | x 68.9 GPa | sigma required (Pa) | x 276 MPa | E/rho^2 required | sigma/rho required |
|---|---|---|---|---|---|---|---|
| P1 | 0.0007 | 7.963e13 | 1156 | 6.819e8 | 2.471 | 1.0924e7 | 2.5254e5 |
| P1-A | 0.00125648 | 2.472e13 | 358.7 | 3.799e8 | 1.376 | 3.3904e6 | 1.4069e5 |

P1: buckling binds first by far. Both modes at once need E = 7.963e13 Pa with sigma = 6.819e8 Pa, or E/rho^2 = 1.0924e7 with sigma/rho = 2.5254e5 at this mass.
P1-A: spending the float margin on thickness helps both modes and changes neither ranking. Both modes at once need E = 2.472e13 Pa with sigma = 3.799e8 Pa, or E/rho^2 = 3.3904e6 with sigma/rho = 1.4069e5.

## Family P2, sandwich. Equal-mass figures, faces: E/rho and sigma/rho, core held

Core thickness, density and face separation stay at each row's value. Face mass fixed means face thickness follows 1/rho, so both pressures follow their property over rho. The small change in separation as face thickness follows mass is neglected; see NFI-005-SEP.

| row | tf (m) | separation (m) | E required (Pa) | x 68.9 GPa | sigma required (Pa) | x 276 MPa | E/rho required | sigma/rho required |
|---|---|---|---|---|---|---|---|---|
| P2 | 0.0002 | 0.1002 | 5.621e11 | 8.158 | 1.193e9 | 4.323 | 2.0818e8 | 4.4195e5 |
| P2-A | 0.000375894 | 0.100376 | 2.985e11 | 4.333 | 6.349e8 | 2.300 | 1.1057e8 | 2.3515e5 |
| P2-C | 0.0002 | 0.159564 | 3.530e11 | 5.123 | 1.193e9 | 4.323 | 1.3073e8 | 4.4195e5 |
| P2-K | 0.000270883 | 0.135712 | 3.064e11 | 4.447 | 8.810e8 | 3.192 | 1.1348e8 | 3.2630e5 |
| P2-E | 0.000336095 | 0.113768 | 2.946e11 | 4.276 | 7.101e8 | 2.573 | 1.0911e8 | 2.6299e5 |

P2: buckling binds. Both modes at once need E = 5.621e11 Pa with sigma = 1.193e9 Pa, or E/rho = 2.0818e8 with sigma/rho = 4.4195e5.
P2-A: thicker faces at fixed core. Both modes at once need E = 2.985e11 Pa with sigma = 6.349e8 Pa, or E/rho = 1.1057e8 with sigma/rho = 2.3515e5.
P2-C: core takes the ceiling, faces fixed, so its required strength equals the P2 baseline's while its required modulus falls. Both modes at once need E = 3.530e11 Pa with sigma = 1.193e9 Pa, or E/rho = 1.3073e8 with sigma/rho = 4.4195e5.
P2-K: one factor on faces and core. Both modes at once need E = 3.064e11 Pa with sigma = 8.810e8 Pa, or E/rho = 1.1348e8 with sigma/rho = 3.2630e5.
P2-E: equal face and core mass gives the lowest pair in this family. Both modes at once need E = 2.946e11 Pa with sigma = 7.101e8 Pa, or E/rho = 1.0911e8 with sigma/rho = 2.6299e5.

## Family P3, frame plus film. Equal-mass figures, members: E/rho and sigma/rho at fixed outer tube radius

Outer tube radius fixed at 0.02 m. Thin-wall section: area about 2 pi ro tw and inertia about pi ro^3 tw, so at fixed member mass the wall follows 1/rho and both pressures follow their property over rho. Spacing s = 1 m.

| row | tw (m) | E required (Pa) | x 68.9 GPa | sigma required (Pa) | x 276 MPa | E/rho required | sigma/rho required |
|---|---|---|---|---|---|---|---|
| P3 | 0.001 | 2.075e12 | 30.11 | 3.896e9 | 14.11 | 7.6841e8 | 1.4428e6 |
| P3-A | 0.00349653 | 7.175e11 | 10.41 | 1.190e9 | 4.313 | 2.6575e8 | 4.4087e5 |

P3: Euler buckling binds, and crush is close behind it in ratio. Both modes at once need E = 2.075e12 Pa with sigma = 3.896e9 Pa, or E/rho = 7.6841e8 with sigma/rho = 1.4428e6. The film needs only 5.966e8 Pa allowable for SF 1 against its inherited 1.5e9 Pa QUESTIONABLE value, so the film passes at SF 2.51 and does not bind.
P3-A: thicker walls at fixed outer radius. Both modes at once need E = 7.175e11 Pa with sigma = 1.190e9 Pa, or E/rho = 2.6575e8 with sigma/rho = 4.4087e5. The film requirement is unchanged at 5.966e8 Pa, SF 2.51. The thin-wall figure is weakest here, where tw/ro = 0.175; see NFI-005-THINWALL.

Every row sits below SF 1 in both modes at 6061-T6. These requirements feed MAINLINE-008, the material gap table. Open issues are in NFI.json. Next job NFI-CRUSH follows as MAINLINE-005b.
