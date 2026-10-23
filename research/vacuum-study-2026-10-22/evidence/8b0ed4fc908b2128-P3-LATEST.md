**MAINLINE-038 — latest P3 test targets from filed 022d. QUESTIONABLE / PROJECTION.**

These supersede 022c procurement dimensions. The frozen 022c sensitivities remain in CARD/METHOD/OUTCOMES solely to audit the named 1.5 GPa material premise. Both Zylon plies are included here. No row establishes a full-size allowable or qualified hull SF.

| Family / reserve / band | Modeled SF | s / arc m | OD / wall mm | Film total / each ply μm | Operating / sized-joint load MN | Film mass kg | Half-wave/member |
|---|---:|---:|---:|---:|---:|---:|---:|
| cfrp_zylon / 5 / overall | 1.397733 | 6.085747 / 6.183804 | 336.155 / 1.626170 | 233.337 / 116.669 | 1.677060 / 2.344081 | 457.423 | 0.569022 |
| cfrp_zylon / 5 / in_band | 1.258252 | 3.170759 / 3.184194 | 275.083 / 1.137365 | 109.440 / 54.720 | 0.873771 / 1.099425 | 214.542 | 1.000000 |
| projection / 019 / overall | 1.311145 | 6.026689 / 6.121837 | 329.665 / 1.570459 | 251.440 / — | 1.660785 / unknown | 306.489 | 0.569228 |
| projection / 019 / in_band | 1.151626 | 3.128683 / 3.141586 | 267.747 / 1.084036 | 114.651 / — | 0.862176 / unknown | 139.752 | 1.000000 |
| cfrp_zylon / 019 / overall | 1.328131 | 6.038536 / 6.134263 | 330.962 / 1.581516 | 219.998 / 109.999 | 1.664050 / 2.210075 | 431.274 | 0.569186 |
| cfrp_zylon / 019 / in_band | 1.194121 | 3.145837 / 3.158955 | 270.726 / 1.105548 | 103.046 / 51.523 | 0.866904 / 1.035188 | 202.006 | 1.000000 |

**Use the 019 screened Zylon point as the procurement reference for this plan, while retaining the overall branch as a separate sensitivity.** This choice carries the larger inherited reserve; it is not a claim of demonstrated conservatism. The one-member half-wave constraint is a requested screen, not a demonstrated homogenization boundary. Its three modes (local/global/film) bind at 1.194121. It still assumes SiC Fc=3.9 GPa and an unqualified complete membrane.

T4: total structural gauge is 103.046 μm, half in each direction. Nominal directional stress is 2.914276 GPa, not the total-gauge effective 1.457138 GPa. A 0.30 m same-gauge cap-equivalent bulge needs about 1.001014 MPa to reproduce service stress; a same-pressure geometrically scaled laminate would be only 9.827 μm total and is not the production microstructure.

| Measured effective strength using total two-ply gauge, GPa | Corresponding directional-ply strength, GPa | Film SF, fixed gauge |
|---:|---:|---:|
| 0.500 | 1.000 | 0.343138 |
| 1.000 | 2.000 | 0.686277 |
| 1.500 | 3.000 | 1.029415 |
| 1.740 | 3.480 | 1.194121 |

An improvement above the baseline film capacity leaves other modeled modes binding. Barrier, adhesive, UV/moisture protection and seams must be weighed separately; the structural fiber gauge is not the finished laminate gauge. 034's 57.546 kg illustrative barrier/attachment bill demonstrates the kind of missing mass; it is not a measured bill for this geometry.

T5: mean and maximum compression at operating load are 0.925745 and 0.983923 GPa. At the claimed multiplier the maximum is 1.179764 GPa. These include the inherited bow model, not contact/fracture qualification. Make representative approximately 270.726 mm OD, 1.105548 mm wall stubs; the eventual arc is 3.158955 m long.

| Assumed Fc, GPa | Mean-compression SF | Inherited Perry SF |
|---:|---:|---:|
| 0.38 | 0.410480 | 0.390127 |
| 1.00 | 1.080211 | 1.016015 |
| 1.20 | 1.296254 | 1.214052 |
| 3.90 | 4.212824 | 3.301678 |

These ratios do not replace the maximum-compression, local wall, global, contact and brittle-failure checks. A coupon that passes mean stress alone is insufficient.

T6: operating/sized joint forces are 0.866904/1.035188 MN, or 34.676/41.408 kN at 1:5 with the same material and geometric similarity. The modeled wrap overlap is 42.116 mm and the charged mass is 0.045970 kg/end. The actual adhesive and all restraint hardware must be included. An extra 10 g/end costs 8.797 kg before replacing the fractional member count.

At fixed joint section/bond geometry, an observed axial or bond capacity of 0.7 / 1.0 / 1.2 times the claimed target gives the corresponding joint-mode SF 0.835885 / 1.194121 / 1.432946. Whole-frame SF remains unknown without rotational/roll data. Here EI/L=1.104439 MN m/rad; report beta=Ktheta/(EI/L).

T8: the screened branch has a fractional node count near 149. A 162-node frequency-4 mesh is a possible integer candidate for a fresh model, while a 42-node frequency-2 mesh addresses the coarse overall branch. No existing model factor is assigned to either merely by proximity of node count. At R=0.5 m, the screened reference scales to about 13.536 mm OD and 55.277 μm wall; reject or redesign the test if the available tube/joint/skin cannot preserve the intended dimensionless response.

**No stiffness threshold or allowable was supplied by these arithmetic updates.** First measure real joints and full laminate, then compute the selected integer model. The two-way numerical maxima are excluded from this procurement preference because their in-plane shear stiffness remains unresolved. R20 transfer still requires topology, gauge/process and size-dependent material qualification.
