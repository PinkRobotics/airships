# MAINLINE-037 — loads beyond uniform pressure

ESTIMATE. QUESTIONABLE throughout. Not a certification. 022d had not filed, so the P3 rows are 022c's cap branch. The arithmetic is loads037.py. RESULTS.json is the record.

The P2 lead is 028b's full-named SR-200 scarf on Hexcel CR-III 5056, sheet Poisson 0.0752. Least factor 1.006358, global and the scarf screen tied. Face thickness 0.7997 mm, core 22.107 mm. Working face stress p*R/(4*tf) is 298.436 MPa. The 345 MPa tensile yield, used in compression, is factor 1.156. The floated face factor 1.271 uses the 379.2 MPa compression endpoint. At today's gamma 0.20 the same geometry is 0.33958 by global. The 1.006 figure spends the projected gamma and the wrinkling coefficient.

## Sun

Gradient stress is E*alpha*dT/(2*(1-nu)). With E 290 GPa, alpha 11.3e-6 and nu 0.0752 that is 1.7717 MPa per kelvin. The honeycomb conductance is aluminum conductivity times the core solidity, and the cells are taken as evacuated. A white coating, absorptance 0.20 and emittance 0.90, puts the subsolar faces at 301.569 K and 301.170 K. The gradient is 0.399 K and the stress is 0.707 MPa. The sphere-average face is 288.377 K, 3.48 K above the 284.9 K air, in the same band as 016's coated average.

A temperature pattern that is uniform through the thickness has no membrane stress on a complete single-material sphere. The part that is not linear in position produces bending. From the n=2 through n=6 reconstruction that bending is 0.818 MPa. The fully constrained upper bound is 20.51 MPa. The table uses the bending value.

Bare beryllium, absorptance 0.40 and emittance 0.05, reaches 356.946 K at the subsolar point. The gradient is 1.907 K and 3.379 MPa. Pattern bending is 0.772 MPa. The constrained bound is 60.75 MPa and is not the stress.

Face-core shear lag uses aluminum 23.6e-6 against beryllium 11.3e-6, the core shear modulus, and tau = dEps*E*tf*lambda. On the coated day rise from the air temperature the shear is 143.8 kPa and the factor on the 241.3 kPa W-direction sheet strength is 1.678. If the bond is instead stress-free at the cold night, the 30.493 K swing gives 263.0 kPa and factor 0.917. Bare beryllium on the day rise gives 621.5 kPa and factor 0.388. The coating is what keeps this mode above 1.

P3 film and tube temperatures are in RESULTS.json. A stiff frame forces the film to take (alpha_frame*dT_frame - alpha_film*dT_film). The added member force is tens to thousands of newtons against member forces of 0.15 to 1.69 MN. It does not move the governing P3 factor by itself. The projection film has no stated modulus or expansion; 10 GPa with 4.5e-6 and with 17e-6 are assumptions. Member bow from a uniform mismatch is not an equilibrium result: the sphere changes radius and the members stay straight.

## Wind

Dynamic pressure uses the 500 m density. A 20 m/s gust is 233.45 Pa, 0.2445 percent of p. Drag at Cd 0.47 is 34.47 kN, and 016's 1.4 factor makes the mooring load 48.259 kN.

FAA-P-8110-2 paragraph 3.9 prescribes a 35 ft/s discrete gust at VB, and paragraph 3.6 says VB is at least 35 knots. The stagnation excess of that pair is 290.634 Pa. Paragraph 3.25 Table 4 lists 70 knots for symmetrical mooring. That dynamic pressure is 756.856 Pa and the drag is 111.75 kN. The change discussion names 78 knots; that drag is larger and is in RESULTS.json.

The windward excess is applied as a uniform pressure. That is the conservative global case. Potential flow on a sphere has Cp = 1 - 2.25 sin²(theta) and an area-mean Cp of -0.5, so the mean crushing pressure falls. No sourced knockdown for a windward patch was found, so the patch is not scored below the uniform excess.

## Hard points

The mooring load governs. A 100 kg systems set is 0.98 kN and the 411.3 kg reserve is 4.03 kN. On this core the 016 bare patch of 0.0707 m² is factor 0.354. One 6061-T6 pad sized to crush factor 1 and to the plate yield is 0.2000 m², 16.02 mm thick and 8.65 kg. The 70-knot drag needs 0.4631 m², 26.50 mm and 33.14 kg. The plate formula is a simply-supported disc with a 25 mm boss. P3 shares 48.259 kN so that no member gains more than 5 percent of its pressure force: 7 members at the Mylar spacing, 2 at the titanium spacing, and 1 member at the out-of-band spacings. Those fittings are not the mass that restores a factor below 1.

## Factors

P2, full-named point. Uniform: global 1.006358, face on 345 MPa 1.156027, face on the 379.2 MPa endpoint 1.270625, crimp 2.331434, crush 5.055822, wrinkling 1.964868, dimpling 6.973752, scarf 1.006358. Coated sun, gradient plus bending: the pressure modes stay, and the 345 MPa face factor becomes 1.15015. Bare sun: that face factor becomes 1.14017. Flight-gust excess: least 1.003303, scarf and global. Combined coated gust: least 1.003303. Combined bare gust: the seven screens stay at 1.003303, while the separate shear-lag factor is 0.388. Seventy-knot uniform excess: least 0.998442. Restoring that hundredth is 0.16 percent of critical pressure, not a weighed mass. Shear-lag is restored by the coating and by the bond temperature, not by face mass.

P3 combined flight gust, cap branch. Projection at 6.15 m is outside the half-wave band, ratio 0.571, and stays about 1.370 by global. CFRP and Zylon at 5.5 m is outside, ratio 0.636, and stays 1.457 by film. Mylar at 0.55 m is in band, ratio 4.562, and is 0.41051 by Perry against 0.41179 uniform. Titanium and Kapton at 1.85 m is in band, ratio 1.490, and is 0.74123 by global against 0.74170 uniform. The 019 rows and the membrane branch sit a few hundredths lower and take the same load fractions. A proportional tube-wall increase to reach 1 is 5863 kg on the Mylar row and 1634 kg on the titanium row. Both exceed what the lift can still accept. The gap is the filed baseline, not the sun or the wind.

## Requirements

The coating, the temperature at which the bond is stress-free, and the mooring wind are decisions for the Admiral. Design airspeed is the other. Each changes a factor that otherwise sits on 1. No next job is named.

Started 2026-10-20T02:07:28-07:00. Ended 2026-10-20T02:07:30-07:00. Elapsed about 2 s, a measurement.
