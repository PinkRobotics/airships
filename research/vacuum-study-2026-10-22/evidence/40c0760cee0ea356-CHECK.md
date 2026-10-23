# MAINLINE-011b CHECK — SiC arcs at 1.226, re-derived

Unit vacuum-mainline011b-check-1019. Order ord-admiral-rr2-check011b-opus-1020. Checker ref-55cff924be25afe6f9dd
(claude-opus-5-5, max) behind the owner, grok ref-2543c559b19ffce7dfdd (rpt-mainline011b-grok-p3-global-arcs-1019).
Every value is QUESTIONABLE. Nothing here is a certification.

Method. My own scripts (check011b.py, check011b_extra.py, compare011b.py) work from the pinned inputs and the formulas the
card states. The owner's arcs.py was not run or imported. I read its radius-grid lines once, after my own scan, to explain
a 2e-5 difference: it starts the radius scan at 1.0001 times the solid rod. My scan uses that grid for the like-for-like
comparison and a continuous optimiser beside it. The owner's RESULTS.json and CARD.md were read only to compare.

## Verdict

The arithmetic reproduces. 951 numeric fields match: the 48 RESULTS rows, the 36-row CARD table and 15 named numbers. The
largest relative difference is 3e-12, the card's 12-digit rounding. All 169 governing and second-mode labels match. There
are no numeric mismatches. A continuous optimum gains at most 0.30% over the card's grid (SiC, equilateral, k 0.4).

The model has one demonstrated conservatism, one optimism measured against the line's own source, and one unstated
condition. SiC arcs on the equilateral grid stay at or above 1 at k 0.2 with all of them applied, including 100 kg systems
and a 5% margin (1.130). On the two-way coefficient, SP-8007's knockdown takes the row below 1 (0.967).

## The order's items

**Smeared stiffness and sqrt(3/2): confirmed.** Summing the three member families (0, 60 and 120 degrees, line spacing
s*sqrt(3)/2) gives nu = 1/3, Et = (2/sqrt(3))*E*A/s and D = (3*sqrt(3)/4)*E*I/s. Then 4*sqrt(D*Et) =
2*sqrt(6)*E*sqrt(I*A)/s = 4.898979*E*sqrt(I*A)/s, which is sqrt(3/2) = 1.224745 times the brief's two-way
4*E*sqrt(I*A)/s. A printed source exists: Buchert, "Space Frame Buckling", AISC Engineering Journal, October 1968. It gives
t_m = 2A/(sqrt(3)*l) and t_B = (9*sqrt(3)*I/l)^(1/3) for the equilateral reticulated dome, and with D = E*t_B^3/12 these
are exactly the card's Et and D. The derivation omits member torsion and presumes moment-rigid joints
(NFI-CHK011B-JOINTS).

**Global pressure: confirmed.** p = k*C*E*sqrt(I*A)/(s*R^2), with C = 2*sqrt(6) on the equilateral grid and 4 on the two-way
grid. At the SiC equilateral point (s 2.04 m, r_o 123.688 mm, t_w 0.8803 mm, r/t 140.5), k 0.2 gives 116,990 Pa and SF
1.22552794688. That matches the card to 2e-15 and the robotics seat's 116,989 Pa.

**Perry term: confirmed.** sigma_cr = 0.5*[(sigma + (1+eta)*sigma_E) - sqrt((sigma + (1+eta)*sigma_E)^2 - 4*sigma*sigma_E)],
with sigma_E = pi^2*E*rg^2/s^2, eta = (s/1000)*r_o/rg^2 and SF = sigma_cr/sigma_axial. It reproduces every Perry SF,
including the filed 011 tube with joints off (0.178765809625) and SiC at 380 MPa (0.26224593556). At the SiC point, eta is
0.0332 and the amplifier is 1.240. The bending is ±58.8 MPa on 1.428 GPa of compression, so both fibres stay in
compression (-1.487 and -1.370 GPa).

**Mass closure: confirmed.** Film 97.515 kg + nodes 0.02*V(s) + joints 0.05*tube + systems 50 kg + tube = L =
4889.44215019 kg exactly, with V(s) = 8*pi*R^2/(sqrt(3)*s^2) + 2 and M = 3V - 6. For SiC on the equilateral grid: V 350.67,
M 1046.0, tube 4509.44 kg, joints 225.47 kg, nodes 7.013 kg. All match to 1e-12 or better.

**Both SiC rows: confirmed.**
- Equilateral, k 0.2: 1.22552794688, global governing and local second, at s 2.04 m.
- Two-way, k 0.2: 1.10810389922, global governing and local second, at s 2.26 m.

The continuous optima are 1.2272 and 1.1094.

**50 kg systems and margin 0: they match the brief.** CARD-011 says "Hold P3 at the float-mass ceiling (margin 0) ...
systems 50 kg", COMMON.md's P3 rule says the same, and I-SYS3 is 50 kg. 011b re-runs 011 and adds nodes and joints at the
new spacing, as its brief directs. This is P3's own accounting, not the common rules that 022 restates. At 100 kg systems
and a 5% margin (244.47 kg), the same model at k 0.2 gives 1.151 on the equilateral grid and 1.041 on the two-way grid.

## Mismatches (text and tagging only)

- **M1.** The report body says "k 0.4 and 0.5 are in the card". The CARD.md table carries k 1, 0.4 and 0.2; the k 0.5
  rows are in RESULTS.json only.
- **M2.** INPUTS.json material rows carry "questionable": true but no source. COMMON.md asks for a URL, DOI or handbook
  name. The sources are in 011's INPUTS.json (I-011-AL, I-011-SWAP via MAINLINE-008, I-011-LOCAL, I-011-FILM-PROPS),
  which 011b does not pin.
- **M3.** The card says no coefficient was taken from Buchert. Buchert 1968 prints the card's Et and D, so the card can
  cite it.
- **M4.** The "two_way" rows are the triangulated frame (the same V(s), M = 3V - 6 and masses) scored with C = 4. They
  are not a two-way frame, which would have M = 2V, V = 4*pi*R^2/s^2, and zero in-plane shear stiffness (the lattice
  sum gives C1212 = 0).

## Objections (NFI.json; FIX-A and FIX-B are proposed fix cards)

**NFI-CHK011B-FORCE (demonstrated; conservative; FIX-A).** The card's member force N = pRs/2 is the two-way arch
resultant. The frame the card counts has 3V - 6 members of length s, and statics alone fix their mean compression at
pRs/(2*sqrt(3)). Three checks agree:
- The virial identity for a closed pin-jointed frame under external pressure, sum(C*l) = 4*pi*R^3*p, is exact.
- The card's own Et and nu = 1/3 give the same member strain.
- Discrete geodesic trusses of 162 and 362 nodes were solved by statics (rank complete, residual 6e-15). Mean C over
  pRl/(2*sqrt(3)) is 1.017 and 1.007. The largest force is 600 kN at a mean length of 2.0 m.

Equivalently, each member carries sqrt(3)*s^2/6 = 0.289*s^2 of film, not s^2/2. The force is inherited from
MAINLINE-002's P3 rule, and the card used the stated formula. As a result, yield, Euler, local and Perry are
sqrt(3)-conservative at a given tube. Re-optimised, SiC on the equilateral grid at k 0.2 rises to 1.408 and 6061 to
0.339. At the card's s of 2.04 m the mean member-end load for 022 and 023 is 562 kN, not 974 kN.
FIX-A: score the P3 members with N = pRs/(2*sqrt(3)) on the equilateral frame, or count a true two-way frame, then
re-optimise.

**NFI-CHK011B-LOCAL-GAMMA (demonstrated from the cited source; optimistic; FIX-B).** Local buckling keeps gamma = 1 at
r/t 140.5. NASA SP-8007, which 011 cites for the 0.6, gives gamma = 1 - 0.901*(1 - exp(-sqrt(r/t)/16)) = 0.529, which
puts local at 0.648 at the card's SiC point. Re-optimised with gamma, SiC on the equilateral grid at k 0.2 is 1.075 (r/t
94), and 1.205 with FIX-A as well. FIX-B: apply SP-8007's gamma to the local mode and re-optimise.

**NFI-CHK011B-JOINTS (asserted).** D presumes the members are continuous in bending through the nodes, which means
moment-rigid joints. With pinned or soft nodes, the smeared bending stiffness and the global mode fall. 023's joints must
therefore carry member-end moments as well as the axial force. Member torsion is omitted; with torsion-rigid joints it
would raise the global SF by 13.7% for SiC (nu 0.14) and 11.8% for 6061 (from the lattice sum).

**NFI-CHK011B-SIC-FIBRE (demonstrated).** The arcs stay fully compressed under the L/1000 imperfection, so the 380 MPa
flexural scan (0.262) is not the allowable for arcs. The open allowable is the compressive strength of a 0.88 mm brittle
wall at 1.43 GPa of service stress (0.82 GPa with FIX-A). That is 022's Weibull item.

**NFI-CHK011B-WRIGHT-K (asserted, unverified).** Wright's "modified k of 0.4" may be the coefficient in p = k*E*(t/R)^2
(classical 2/sqrt(3(1-nu^2)) = 1.2247 at nu 1/3). If so, it is about 0.327 of classical, and the k 0.4 global pressures
would fall by about 18%. The citation itself is confirmed by Buchert 1965's bibliography (J. Struct. Div. ASCE
91(ST1):173-201). The expression needs Wright's Table 2.

## SiC restated (checker estimates, continuous optimum, QUESTIONABLE)

Each cell gives two least SFs: margin 0 with 50 kg systems / 5% margin with 100 kg systems.

| case | equilateral k 0.2 | two-way k 0.2 | equilateral k 0.4 | two-way k 0.4 |
|---|---|---|---|---|
| card model | 1.227 / 1.151 | 1.109 / 1.041 | 1.732 / 1.625 | 1.566 / 1.469 |
| FIX-A, equilibrium force | 1.408 / 1.320 | 1.272 / 1.194 | 1.986 / 1.863 | 1.796 / 1.685 |
| FIX-B, SP-8007 gamma | 1.075 / 1.009 | 0.967 / 0.907 | 1.545 / 1.449 | 1.390 / 1.304 |
| FIX-A and FIX-B | 1.205 / 1.130 | 1.083 / 1.015 | 1.735 / 1.628 | 1.560 / 1.463 |

6061 on the equilateral grid at k 0.2, margin 0: card 0.216, FIX-A 0.339, FIX-B 0.210, both 0.279.

The film co-binds in most rows (its SF is 2.514/s). The 1.5 GPa film allowable, which has no datasheet, is therefore on
the critical path.

Times are measurements only: work started at 2026-10-20 00:25:09 PDT and ended at the filing.
