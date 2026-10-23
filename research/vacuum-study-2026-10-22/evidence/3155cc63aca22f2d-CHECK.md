# CHECK-007 — MAINLINE-007 core density trade — PASS

Unit vacuum-check007-1019. Order ord-admiral-rr2-check006-007-007b-after-011-1019. Owner ref-1a533823b6613bf7ff73 (grok); checker ref-3dada7412231c2ce03cc (glm) — different provider. Own script .ship/work/scripts/check007_core_trade.py; owner files read read-only; owner code never imported.

## What was re-derived

429 fields from the COMMON.md pins (R=10 m, p=95460.83791390515 Pa, L=4889.442150186961 kg, E=68.9 GPa, ν=0.33, σ=276 MPa QUESTIONABLE, ρ_f=2700, kd=0.2, joints 5%, systems 100) at 1e-9 relative:

- Mass line M = (L−100)/1.05 = 4561.3735 kg is the faces+core budget (joints 228.0687 on top; totals close to L). Buckling-optimal closed form tf = M/(2S(2ρ_f−ρ_c)) — verified by my own 200k-point tf grid at ρ=16 and ρ=8: the closed form dominates the grid and the gap is <1e-4, reproducing the card's grid claim. Algebraic identity confirmed: the buckling-peak separation equals M/(2Sρ_c) (the equal-mass core thickness) at every density.
- Equal-factor line d = σR√(1−ν²)/(kdE) = 0.189070201186 m — independent of density ✓. Coincide/diverge threshold follows: separation below the line ⟺ ρ_c ≳ 9.6 kg/m³, matching the card (32 and 16 coincide; 8, 6, 4, 3, 2, 1 move to the equal line).
- Both splits at all eight densities: tf, core, separation, masses, p_b, p_y, both SFs, least, governing, membrane = pR/(4tf), E_factor = p/p_b, strength_factor = membrane/σ, Gc crimp target pR/(2d), Ec·Gc target (2·membrane)³/E, crush p/2.
- The SF_b=1 crossing: my bisection reproduces ρ_c* = 3.73369568197 with tf 0.00033632751569, core 0.485753861595, SF_y 0.38896115458, strength factor 2.57095082176.
- Peak claims: named-set high at 1 kg/m³ (0.737028554512); 0.25→64 ratio-1.05 sample is 114 points, monotone (no next-higher sample), low end 0.767296865535 — all reproduced.
- The 6061 gap: all-faces tf 0.000672189940789, membrane 355036694.695 Pa, SF_y 0.777384434128, closing factor 1.28636483585; at the named peak 1.35679953494 ✓.
- Sealed-card checks re-derived independently: P2-A baseline p_b 11701.5583953 (tf 0.0002, core 0.1), P2-A ceiling SF 0.23078902511, P2-E ceiling SF 0.233885578993 — all match 003/006, which my CHECK-006 just re-derived from scratch.
- Catalog rows: all psi→Pa conversions exact (187, 52, 20000, 7000, 34000, 10000 psi × 6894.757293168361); Ec·Gc products (2.21e14, 4.8e14, 1.064e15, 3.69e14); every crush/crimp/wrinkle margin per material at the correct row; density offsets; the "40 to 180×" wrinkling miss (38.4–184.7), the "7 to 27×" crush clear (7.51–27.01) and the crimp clear (min 1.069) all hold.

## Result

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## Notes (no objection, no NFI opened)

1. My first run reported 26 "mismatches" that were two bugs in my own checker (strength_factor inverted; bisection branch backwards) — fixed in my script, and the owner's values then matched everywhere. The owner's numbers were never wrong.
2. The datasheet values (ROHACELL/DIAB/Plascore/Hexcel/Schaedler) are carried as sourced QUESTIONABLE pins; my check verifies the arithmetic and the named sources, not the datasheets' own prints — the owner's NFI-DATASHEET already carries the one known inconsistency between two Plascore prints.
3. Card phrase "modulus factor 1" at the crossing is exact by construction (SF_b=1), consistent.
