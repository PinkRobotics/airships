# CHECK MAINLINE-006 — checker behind rpt-mainline006-grok-float-margin-1019

Checker: ref-9af2822b3fe57c40be31. Order: ord-admiral-rr2-check006-007-007b-muse-1019. Brief CHECK.md with COMMON.md, pinned and verified. Owner script was not used; numbers are from my arithmetic.py in this directory, solving each family's thickness from its mass budget.

## Verdict

Numeric PASS on every material number. Two numerical-zero residuals and one text provenance mismatch are listed exactly below. They do not change any safety factor.

Formulas: A = 4*pi*R^2, R 10 m, E 68.9 GPa, nu 0.33, sigma 276 MPa QUESTIONABLE, kd 0.2, p_ext 95460.83791390515 Pa, lift 4889.442150186961 kg. P1: shell = A*t*2700, joints 10%, systems 200 kg, p_b = kd*2*(t/R)^2*E/sqrt(3*(1-nu^2)), p_y = 2*sigma*t/R. P2: faces = 2*A*tf*2700, core = A*core*16, joints 5% of sandwich, systems 100 kg, p_b = kd*4*tf*(core+tf)*E/(R^2*sqrt(1-nu^2)), p_y = 4*sigma*tf/R. P3: frame from 002 n_edges and tube area, film/nodes/systems fixed, Euler and member yield as in 002. Least SF = min(buckling, yield); P3 film SF = 240000/p_ext = 2.51411998098 and never governs. Segments are sorted by payload; loss per 100 kg is the finite difference over that step.

## P1

Thickness solved from (counted mass - 200)/1.1. At margins 0, 5, 10, 20, 30% and baseline I get least SF 0.0027876603671443925, 0.0025045815207599066, 0.0022366552382636594, 0.0017462603649358705, 0.0013164757471610241, 0.0008652193070060096. Secant 0-30% = 0.00010029669198745669 per 100 kg. Knee 0 to 5% = 0.00011579187878259695 per 100 kg. All match the card.

## P2-A

Core held at 0.1 m, face solved from the sandwich budget. Least SF: 0.23078902511015878, 0.20965111861478725, 0.18852761414332897, 0.1463238112721516, 0.10417761649662667, baseline 0.12257967404267693. Secant 0-30% = 0.008631619226656272 per 100 kg. Knee 0 to 5% = 0.00864634690260653 per 100 kg. All match.

## P2-E

Equal face-mass and core-mass split at 16 kg/m3. Least SF: 0.23388557899250978, 0.21061807098729998, 0.18856933425573794, 0.1481281746135562, 0.11256210006596452, baseline 0.12749744890822584. Secant 0-30% = 0.008271119362898151 per 100 kg. Knee 0 to 5% = 0.009517448940190472 per 100 kg. All match.

## P3

Tube wall solved from frame mass with outer radius 0.02 m. Least SF: 0.09602613905451597, 0.09194147542814259, 0.08775871067785629, 0.07909887780554474, 0.07004664043758142, baseline 0.03320954045817858. Secant 0-30% = 0.0017711290176488515 per 100 kg. Knee 30% to baseline = 0.002039729307497046 per 100 kg. All match.

## Mismatch list (exact)

Numeric mismatches at relative 1e-9: none in geometry, masses, pressures, safety factors, segments, secants or knees. RESULTS.json compares every row field.

Zero residuals, listed for exactness:
- Row P3/0, field payload_kg: card 1.8189894035458565e-12 kg, checker 0.0 kg. Absolute difference 1.8e-12 kg.
- Row P3/0, field float_margin: card 3.7202391350029625e-16, checker 0.0. Absolute difference 3.7e-16.
These are the owner's solver residue at zero margin. No other row differs.

Text mismatch M1 (no number changes):
- Row P2-E/baseline, field provenance in the owner report body ("plus each family's sealed 002 baseline").
- Card value: the baseline is presented as a sealed 002 baseline for each family.
- Checker value: P1, P2-A and P3 baselines do reproduce sealed 002 geometries. P2-E has no sealed 002 row; its baseline face 0.000248148148148 m, core 0.08375 m is the equal-mass split constructed at the 002 P2 counted mass 3636.17669088 kg. Its numbers are right; its provenance label is not sealed.
- Proposed fix is CHECK-NFI-1 in NFI.json: call it the equal-split row at the 002 P2 mass.

## Sources and tags

Every row is QUESTIONABLE. Yield is 276 MPa transferred from tensile data, QUESTIONABLE, and scales linearly with that allowable. Buckling uses kd 0.2 from 002 and scales linearly with kd; yield does not move with kd. Sandwich buckling omits core shear, as stated. Owner NFI-KD-020, NFI-KNEE, NFI-YIELD and NFI-SHEAR stand. Pins: 10 of 10 match, pin_bad 0; owner report artifacts verified against the filing. Elapsed 28.72730285488069 s in the owner report recomputes from its stamps and is a measurement only.

Files: RESULTS.json (row comparisons), INPUTS.json (pins), NFI.json (checker rows), arithmetic.py (my script; its stamps measure that script run only).
