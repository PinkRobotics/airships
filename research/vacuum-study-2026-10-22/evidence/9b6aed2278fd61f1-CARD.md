# MAINLINE-023 — P3 nodes and member-end fittings — ESTIMATE

Unit vacuum-mainline023-p3-nodes-1020. Orders ord-admiral-rr2-mainline023-dispatch-1019 and ord-admiral-rr2-mainline023-load-562kn-1020. Every row is QUESTIONABLE or PROJECTION. Nothing here is a certification. The arithmetic is nodes.py. arcs.py and floatpoint.py were not run. Display figures are half-up. Full values are in RESULTS.json.

The first filing, rpt-ref-59bfd43c34a09e9f120a, sized the equilateral grid at p R s / 2, which is 973.7 kN. That is the two-way force. The equilateral force is p R s / (2 √3). At s 2.04 m it is 562.2 kN. Yield, Euler, local buckling and Perry use that force, so those four factors rise by √3. Global and the film do not use N. At the filed radius the global factor is still 1.2255279468805444. Checks 4/4. The two-way 5 percent search still recovers s 2.04 m.

## The mass as a function of N and s

A sleeve or a wrap has one end at m = C N² / r. The constants, in kg·m/N², are 2.950e-14 for Ti-6Al-4V, 1.606e-13 for Invar 36, and 5.807e-15 for the CFRP wrap. A brazed socket needs the tube area: m = 1.974e-5 A N / r, with that constant in 1/N. Nodes are 8 π R² / (√3 s²) + 2. Members are 3 times the nodes, minus 6, which cancels to 24 π R² / (√3 s²). The joint total is two ends times the member count.

When N is the equilateral force, it is proportional to s. At a held radius the sleeve total is then independent of s. At the 011b radius, 123.7 mm, that total is 157.7 kg of titanium, 858.6 kg of Invar, and 31.0 kg of CFRP, at s 1.44 m, 2.04 m, 3 m and 4 m. The mass per node scales as s². The braze total, at the filed tube area, falls as 1/s: 127.9 kg at s 2.04 m, 87.0 kg at 3 m, 65.2 kg at 4 m. 022b can rescale with those expressions. The radius is an input. It is not determined by N and s alone.

## At 562.2 kN, the 011b section re-closed

The pin, double shear at 0.6 times the 827 MPa yield, is 0.202 kg and 26.9 mm. Bearing on two walls of the 0.880 mm tube is 11.9 GPa. It does not fit.

Ti-6Al-4V sleeve, same yield, EA 9394 at 28.9 MPa. 0.075 kg per end, bond 25.0 mm, sleeve 0.87 mm, total 157.7 kg, 0.70 times the 225.5 kg allowance. Frozen least SF is 1.232 by the film. Re-optimised least SF is 1.431 at k 0.2, global, s 1.74 m, and 1.995 at k 0.4, film, s 1.26 m.

Invar 36 at 276 MPa. 0.410 kg per end, total 858.6 kg, 3.81 times the allowance. Frozen least SF is 1.054, global. It closes. Re-optimised least SF is 1.245 at k 0.2, film, and 1.616 at k 0.4, global.

Brazed socket at Cusil-ABA 25 MPa. The wall continues for 28.9 mm. 0.062 kg per end, total 130.6 kg, 0.58 times the allowance. Frozen least SF is 1.232, film. Re-optimised least SF is 1.441 at k 0.2, global, and 2.011 at k 0.4, global. The socket is not a solid node. The shear pair is in the lab.

CFRP wrap, T700S compression 1470 MPa, not the tensile 2550 MPa. 0.015 kg per end, wrap 0.49 mm, bond 25.0 mm, total 31.0 kg, 0.089 kg per node, 0.14 times the allowance. Frozen least SF is 1.232, film. Re-optimised least SF is 1.466 at k 0.2, local, s 1.70 m, and 2.061 at k 0.4, film, s 1.22 m. The fiber and the coupon exist today. The wound joint is a PROJECTION.

## Contact, and the 5 percent search

At the filed wall the compression is 824.7 MPa. That is SF 4.73 on 3900 MPa and SF 0.461 on the flexural 380 MPa. The flexural coupon still cannot carry the member. This card does not replace the 011b allowable.

With the member modes corrected, the 5 percent search leaves s 2.04 m. It finds s 1.78 m, least SF 1.406, global. The joint allowance there is still 5 percent of the tube.

## Lightest

The lightest joint is the CFRP wrap, 31.0 kg at 562.2 kN. It relies on the 1470 MPa coupon and on transferring the 28.9 MPa aluminum lap shear onto SiC. NFI-023-EQUILIBRIUM-FORCE, NFI-023-CFRP-WRAP, NFI-023-ADHESIVE-TRANSFER.

Sources are unchanged from the first filing: EA 9394, AMS 4911, Carpenter Invar 36, Cusil-ABA doi 10.1007/s11665-020-04934-3, and the Torayca T700S sheet. Density stays 3100 kg/m3 so the two-way regression matches 011b.

Compute ran from 2026-10-20T00:55:05-07:00 to 2026-10-20T00:55:14-07:00. Measurements only. No budget and no cap. Stop. The robotics seat sends the next job.
