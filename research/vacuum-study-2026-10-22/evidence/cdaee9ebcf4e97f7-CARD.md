# REVIEW-E, the 069 half

Unit vacuum-review-e-069-1020. QUESTIONABLE inputs. PROJECTION payloads. No qualified hull safety factor. No finite-element run. One round.

The admitted record was rebuilt in this seat's directory. Nothing was written into the owner's record directory.

## Custody

Version 7 is the pinned CLAIM-RECORD.json from rpt-ref-5cd187fda051a1f967ef, sha256 5234234ce0219906d39c9fcc2f3f8ff5ce14f28618441a4f3d6603ef6910552a, 21697950 bytes. DELTA-D-1020.json is sha256 7472abe12cdfb637e1034b5dc99823b1eb45b363aa50271ea61e2c1f51cbc900. The record's apply_delta.py, run on a copy, produces version 8 at sha256 dede05e82b02973f6d4b2d79170dd9930563bc0500ce63717897c62da70040c7, 21796723 bytes. That is the admitted digest.

The live file in ref-08887151c61d86c0cd02 is sha256 c2fdd2327f93a78cc989bcb6cdaa15e32a836122f49da335985496cb6bac308d, 21806940 bytes. Applying DELTA-069-GRAPHITE-071.json to the rebuilt version 8 reproduces those bytes exactly. The delta is the only difference. It is not in version 8. It appends finding PD069-GRAPHITE-071, register row R122 and one NFI row. On CR-III the graphite variant is thermally infeasible. Face density does not release it. The condition is a core expansion at or below 12.2e-6 per K. The filed 069 page is left unchanged. DELTA-E should re-append this delta. Dropping it would put the contradiction back.

## Load-bearing numbers

Lift 132014.938 kg reproduces from the COMMON 10 m lift times 27. Face mass 73751.362 kg and core mass 32375.509 kg reproduce from the outer sphere, the filed thicknesses and the filed densities. Film mass 1656.569 kg reproduces from both faces at the favorable areal density. Optimistic payload +5.031 kg, ISA +1499.236 kg, and the same-geometry TRL 7 payloads +11607.266 kg and +13101.470 kg reproduce as lift minus the filed bill minus growth. The density factor 1.82477 is 1850 divided by 1013.825.

Vc differs. The card has 1.322817. Equation (4.2-6), with the middle-surface distance equal to core plus face, the outer radius, nu 0.0768 and the W-direction core modulus, gives 1.320862. The gap does not move the payload.

Global buckling differs in a named way. With gamma_d 0.20 and Kc from (4.2-4), and no cure stress, the margin is 1.027. The card's 1.000 puts cure in the denominator. That cure term was not found in the opened sources.

Face wrinkling on membrane stress, equation (2.2-14) with eta 1, is 1.0491. That is the card's own membrane-only figure. The card's 1.000 is that margin after gradient, bending and cure. Those three additions were not found in the opened sources.

Equibiaxial compression is a fix. Equation (2.2-15) is R_x cubed plus R_y cubed equals 1. For equal stresses the factor is 0.7937. Applied to the card's wrinkling margin of 1.000, the margin is 0.794. A sphere's membrane is equibiaxial. To clear, face stress must fall by 1.260, or this shell must be shown to be outside that interaction. The model's root 0.682 is not this factor, and BETA = 1 is not this factor. The frozen margin at the root, 0.6823, reproduces as that root times 1. The resized payload of -17249 kg was not re-optimized.

The thermal interface, 1.071, cannot be checked. The admitted record does not state kb or the cure-temperature increment as a computable law.

Scarf, splice, mooring and the weather headroom were not re-derived. Their mass is thousands of kilograms. The +5 kg residual sits inside that unchecked mass. The arithmetic of the filed bill is exact. The physical float is not independently closed.

## The four terms

CR-1457 equation (4.2-4): when Vc is at most 2, Kc = 1 minus Vc/4. Equation (4.2-5): above that, Kc = 1/Vc. Equation (6.2-1) uses that Kc on an externally pressurized sandwich dome, and (6.2-13) sets gamma_d = 0.20 for hemispheres except where shear crimping governs. The kc term stands, with those limits. It is a cylinder coefficient carried onto domes, and the hemisphere factor rests on scarce S-II tests. The factor without it, 1.459, stays a sensitivity beside a sourced term.

The cure term, the gradient and bending stresses at 11.3e-6, and the pressure adder P0 times max(1.01, QWEATHER) plus QWIND are absent from CR-1457. They are absent from DOI 10.2514/3.5568, which is axial buckling of imperfect monocoque cylinders. They are absent from DOI 10.2514/3.1932, which is a general numerical shell solver and does not state these stresses. They stay QUESTIONABLE. The DELTA-D factors without them, for this concept R 30 optimistic point, are 1.769, 1.809 and 1.740.

## The join

The +5 kg point is a hypothetical face at 1013.825 kg/m3 that keeps the 293.6 GPa and 379.2 MPa tuple. It is not the graphite film at 2250 kg/m3. The graphite route's filed conclusion is that no case floats, and that on an aluminum core the shell is thermally infeasible. The 069 page still quotes a graphite factor of 1.659 and a thermal margin near 1.071. Those sentences do not stand with 071. The design point stands only as that hypothetical face, tagged PROJECTION. It does not stand as a graphite hull.

## Fixes, unreviewed

The equibiaxial wrinkling margin is the fix. Vc is a 0.15 percent definition gap and does not move a payload. The absent cure, gradient, bending and pressure adder are NFI, not demonstrated arithmetic errors. Nobody reviews these fixes.
