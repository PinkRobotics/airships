# MAINLINE-018b narrowed — pressures, face bending, lead, run size

QUESTIONABLE. Not a certification. The checker already compared the collapse pressures with the handbook crimp pressure. This card confirms the source, gives the face-bending share, restates the lead, and sizes a run. The run is not executed.

## Pressures on the paper's figure

EUCASS 2023-367, doi 10.13009/EUCASS2023-367, Figure 15 on page 10 prints four bars. Linear perfect pressure is 27.53 MPa on the flat model and 27.56 MPa on the dimple model. Imperfect collapse is 6.03 MPa flat and 5.63 MPa dimple. The Sim 2024 journal file was not opened.

Section 3.2.1, beside Figure 9, states the flat nonlinear perfect load as 12.45 MPa. Section 3.2.2, beside Figure 12, states the dimple nonlinear perfect load as 12.44 MPa. Those two numbers are not printed on Figure 15. The paper assigns them to foam plasticity.

## Ratio to handbook crimp pressure

p_crimp = 2 h^2 Gc / (R_middle tc) at Gc 20 MPa. Flat 3.9156534174 MPa, Vc 201.532463528, R/tc 13.1709677419. Dimple 3.89248364981 MPa, Vc 197.24625832, R/tc 13.1741935484. Collapse over that pressure is 1.53997286205 flat and 1.44637730213 dimple. The checker's unequal-face factor changes the dimple Vc and does not change these pressures.

## Face-bending share

Own-face bending is 0.00472319506474 of the sandwich flexural rigidity on the flat shell and 0.00453826240047 on the dimple shell. That is the term CR-1457 section 2.3.2 neglects. Restoring a fraction of a percent of the bending stiffness does not multiply the shear-crimp pressure by 1.54. This share is not the source of the excess.

Linear pressure over crimp pressure is 7.03075504019 flat and 7.08031233513 dimple. Nonlinear perfect over crimp pressure is 3.17954595897 and 3.19590295533. The paper does not split face bending out of that mix.

## The lead

The 009c-5 least factor is 0.650411843681. Times the measured ratios it is 1.00161658843 flat and 0.940740927738 dimple. The flat product crosses 1. The dimple product stays below 1. Both are a transfer from a 43 mm numerical foam shell. The lead core on the 10 m sphere is at R/tc 484.442002966.

## The run that fits

One flat shell, thicknesses held, R/tc 40, Vc 66.3594394021, still on the crimp branch. Foam solids at 1.54 mm and continuum-shell faces at 1.04 mm, the sizes in section 2.2. Two linear solves, one with face bending and one without, plus one imperfect collapse at mu 0.50. The count is 265752.062471 elements and 1348507.32351 degrees of freedom. At an allowance of 10 kB per degree of freedom the memory is 12.5589531242 GiB. This host had 44 GiB free and a full swap when that allowance was compared. Use 16 of the 32 threads. Do not use the two GPUs.

The same mesh at R/tc 100 is 1641744.58907 elements and 77.4202492434 GiB. It does not fit. P3 stays PENDING-011b.
