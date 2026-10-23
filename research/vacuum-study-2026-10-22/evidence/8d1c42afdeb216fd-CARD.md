# MAINLINE-011b — P3 global lattice buckling and arc members

Unit vacuum-mainline011b-p3-global-arcs-1019. Seat ref-2543c559b19ffce7dfdd.
Every row is QUESTIONABLE. Nothing here is a certification.
The 011 author's files were read and not rewritten. Checks 006, 007 and 007b were not run on this order.

## What was re-derived

At the brief's rounded 6061 point (s 3 m, r_o 86.6 mm, t_w 2.25 mm) the two-way continuum reproduces the robotics arithmetic. Perfect SF is 0.702903874926. Knockdowns 0.2, 0.4 and 0.5 give 0.140580774985, 0.281161549970 and 0.351451937463. Line load w is 143191.256871 N/m. Arch axial stress is 1.18499087263 GPa. Chord sag s^2/(8R) is 0.1125 m, greater than the tube radius. Simply-supported bending is 3.1598 GPa and fixed-end bending is 2.1065 GPa.

The correction is the grid. MAINLINE-011's frame is the equilateral triangulation V=8*pi*R^2/(sqrt(3)*s^2)+2, not a two-way net and not a geodesic. Smeared membrane stiffness is Et=(2/sqrt(3))*E*A/s with nu=1/3. Smeared bending stiffness is D=(3*sqrt(3)/4)*E*I/s. The classical sphere pressure 4*sqrt(D*Et)/R^2 is then 4*sqrt(3/2)*E*sqrt(I*A)/(s*R^2), which is sqrt(3/2) times the brief's two-way pressure. That factor is scored. The two-way pressure is re-optimised beside it. No geodesic coefficient was invented.

Scored members are spherical arcs, because N=p*R*s/2 is the arch resultant of the 011 load path. Straight-chord bending is reported at each optimum and is outside the minimiser. Arc shape error is a geometric Perry-Robertson imperfection a0=s/1000, eta=a0*r_o/rg^2. The safety factor is sigma_cr/sigma_axial at p_ext. The amplifier 1/(1-N/Ne) is not the score.

Joint mass is 5 percent of tube mass, so the float ceiling still closes. Node mass stays 0.02 kg times V(s). The 5 percent is the P2 joint fraction applied to the tubes. A 6061 scan with that term removed is in RESULTS.json.

Design knockdown is k=0.2, the floor of the brief's 0.2–0.5 lattice-dome band. Perfect is k=1. k=0.4 is Wright's modified factor, applied here to the classical pressure derived above. k=0.5 is the top of that band. All four are re-optimised.

## Least safety factor

Joints on. Perry scored. Band s<=3 m. Governing mode is the least of yield, Euler, local, film, Perry and global.

| material | grid | k | least SF | governs | second | s m | r_o mm | t_w mm | nodes kg | joints kg |
|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| 6061-T6 | equilateral_triangular | 1 | 0.215905443307 | perry | local | 0.98 | 95.6315283133 | 0.624722663181 | 30.2573988211 | 224.365226256 |
| 6061-T6 | two_way | 1 | 0.215905443307 | perry | local | 0.98 | 95.6315283133 | 0.624722663181 | 30.2573988211 | 224.365226256 |
| 6061-T6 | equilateral_triangular | 0.4 | 0.215905443307 | perry | local | 0.98 | 95.6315283133 | 0.624722663181 | 30.2573988211 | 224.365226256 |
| 6061-T6 | two_way | 0.4 | 0.215905443307 | perry | local | 0.98 | 95.6315283133 | 0.624722663181 | 30.2573988211 | 224.365226256 |
| 6061-T6 | equilateral_triangular | 0.2 | 0.215551582204 | perry | local | 1.36 | 113.086560578 | 0.735395039388 | 15.730305919 | 225.056992584 |
| 6061-T6 | two_way | 0.2 | 0.214330305457 | perry | local | 2 | 137.767146599 | 0.889285247664 | 7.29519745694 | 225.458664416 |
| CFRP-QI-M55J-epoxy | equilateral_triangular | 1 | 0.455203976657 | perry | local | 1.26 | 172.434701397 | 0.734398855386 | 18.3196610152 | 224.933689961 |
| CFRP-QI-M55J-epoxy | two_way | 1 | 0.455203976657 | perry | local | 1.26 | 172.434701397 | 0.734398855386 | 18.3196610152 | 224.933689961 |
| CFRP-QI-M55J-epoxy | equilateral_triangular | 0.4 | 0.455203976657 | perry | local | 1.26 | 172.434701397 | 0.734398855386 | 18.3196610152 | 224.933689961 |
| CFRP-QI-M55J-epoxy | two_way | 0.4 | 0.455203976657 | perry | local | 1.26 | 172.434701397 | 0.734398855386 | 18.3196610152 | 224.933689961 |
| CFRP-QI-M55J-epoxy | equilateral_triangular | 0.2 | 0.455203976657 | perry | local | 1.26 | 172.434701397 | 0.734398855386 | 18.3196610152 | 224.933689961 |
| CFRP-QI-M55J-epoxy | two_way | 0.2 | 0.455203976657 | perry | local | 1.26 | 172.434701397 | 0.734398855386 | 18.3196610152 | 224.933689961 |
| CFRP-QI-T700-epoxy | equilateral_triangular | 1 | 0.702239779207 | perry | local | 0.78 | 72.8469978028 | 1.13801388729 | 47.740180519 | 223.532712841 |
| CFRP-QI-T700-epoxy | two_way | 1 | 0.702239779207 | perry | local | 0.78 | 72.8469978028 | 1.13801388729 | 47.740180519 | 223.532712841 |
| CFRP-QI-T700-epoxy | equilateral_triangular | 0.4 | 0.670799403436 | perry | local | 2.3 | 129.139407224 | 1.90914235021 | 5.52597161205 | 225.542913266 |
| CFRP-QI-T700-epoxy | two_way | 0.4 | 0.641279271625 | global | local | 3 | 150.871623964 | 2.13180408102 | 3.26453220308 | 225.650600857 |
| CFRP-QI-T700-epoxy | equilateral_triangular | 0.2 | 0.462797231124 | global | local | 3 | 177.451965157 | 1.8088980027 | 3.26453220308 | 225.650600857 |
| CFRP-QI-T700-epoxy | two_way | 0.2 | 0.404338497731 | global | local | 3 | 189.758719325 | 1.69049058566 | 3.26453220308 | 225.650600857 |
| CFRP-QI-K13D2U-epoxy | equilateral_triangular | 1 | 0.269484735855 | perry | local | 1.16 | 250 | 0.436174968733 | 21.6071743666 | 224.777141706 |
| CFRP-QI-K13D2U-epoxy | two_way | 1 | 0.269484735855 | perry | local | 1.16 | 250 | 0.436174968733 | 21.6071743666 | 224.777141706 |
| CFRP-QI-K13D2U-epoxy | equilateral_triangular | 0.4 | 0.269484735855 | perry | local | 1.16 | 250 | 0.436174968733 | 21.6071743666 | 224.777141706 |
| CFRP-QI-K13D2U-epoxy | two_way | 0.4 | 0.269484735855 | perry | local | 1.16 | 250 | 0.436174968733 | 21.6071743666 | 224.777141706 |
| CFRP-QI-K13D2U-epoxy | equilateral_triangular | 0.2 | 0.269484735855 | perry | local | 1.16 | 250 | 0.436174968733 | 21.6071743666 | 224.777141706 |
| CFRP-QI-K13D2U-epoxy | two_way | 0.2 | 0.269484735855 | perry | local | 1.16 | 250 | 0.436174968733 | 21.6071743666 | 224.777141706 |
| SiC-alpha-Hexoloy-SA | equilateral_triangular | 1 | 2.57212492542 | perry | local | 0.8 | 53.0870633037 | 0.801008321598 | 45.3849841059 | 223.644865052 |
| SiC-alpha-Hexoloy-SA | two_way | 1 | 2.46482351076 | film | global | 1.02 | 61.4429269143 | 0.885372920878 | 27.9338771893 | 224.475870143 |
| SiC-alpha-Hexoloy-SA | equilateral_triangular | 0.4 | 1.72722296275 | global | local | 1.44 | 87.4192281783 | 0.879186662778 | 14.0353654648 | 225.137704035 |
| SiC-alpha-Hexoloy-SA | two_way | 0.4 | 1.5646239301 | global | local | 1.6 | 96.8861630699 | 0.881492782605 | 11.3762460265 | 225.26432877 |
| SiC-alpha-Hexoloy-SA | equilateral_triangular | 0.2 | 1.22552794688 | global | local | 2.04 | 123.688362374 | 0.880299093685 | 7.01346929732 | 225.472080043 |
| SiC-alpha-Hexoloy-SA | two_way | 0.2 | 1.10810389922 | global | local | 2.26 | 136.888065854 | 0.881134139272 | 5.72188382562 | 225.533584113 |
| CNT-yarn-QI-PROJECTION | equilateral_triangular | 1 | 1.81151567296 | perry | local | 0.98 | 103.010175158 | 1.12096633737 | 30.2573988211 | 224.365226256 |
| CNT-yarn-QI-PROJECTION | two_way | 1 | 1.81151567296 | perry | local | 0.98 | 103.010175158 | 1.12096633737 | 30.2573988211 | 224.365226256 |
| CNT-yarn-QI-PROJECTION | equilateral_triangular | 0.4 | 1.81151567296 | perry | local | 0.98 | 103.010175158 | 1.12096633737 | 30.2573988211 | 224.365226256 |
| CNT-yarn-QI-PROJECTION | two_way | 0.4 | 1.80959391809 | perry | local | 1.24 | 116.206419544 | 1.26030155602 | 18.9140828744 | 224.905384158 |
| CNT-yarn-QI-PROJECTION | equilateral_triangular | 0.2 | 1.46169766336 | film | global | 1.72 | 151.990564681 | 1.33777000641 | 9.84962338688 | 225.337025086 |
| CNT-yarn-QI-PROJECTION | two_way | 0.2 | 1.32322104262 | film | global | 1.9 | 168.396018096 | 1.33371075867 | 8.07899995228 | 225.421340488 |

P2-E pinned comparison, not recomputed: 0.233885578993 at kd 0.2, and 0.164568553708 at kd 0.140725695373. The brief rounds these to 0.234 and 0.165 at 0.1407.

SiC is also scanned at 380 MPa, the flexural figure carried by 011 from 008. The primary SiC row keeps 011's 3900 MPa crush. CNT remains a projection. Local buckling stays gamma=1. The film allowable stays 1.5 GPa.

## Sources

Wright, D. T., Membrane Forces and Buckling in Reticulated Shells, ASCE Journal of the Structural Division, Vol. 91, ST1, February 1965, pp. 173–201. An ASCE extract of that paper contains the sentence that the author uses a modified k factor of 0.4 for Table 2. The equivalent-thickness line in that extract is not legible and was not used. Buchert, Gioncu 1995 and Makowski are the brief's named works. No coefficient was taken from them. Gioncu 1995 is the state-of-the-art article in the International Journal of Space Structures.

Regression, joints off and the four 011 modes only, recovers the filed 011 6061 optimum at s=3 m. Elapsed time is a measurement and is in ORIGIN.json and RESULTS.json.

