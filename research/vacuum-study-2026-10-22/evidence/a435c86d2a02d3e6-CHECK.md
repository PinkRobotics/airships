# CHECK-007b — MAINLINE-007b sourced shear and wrinkling — PASS

Unit vacuum-check007b-1019. Order ord-admiral-rr2-check006-007-007b-after-011-1019. Owner ref-1a533823b6613bf7ff73 (grok); checker ref-3dada7412231c2ce03cc (glm) — different provider. Own script .ship/work/scripts/check007b_shear_wrinkle.py; owner files read read-only; owner code never imported.

## Source verification (beyond arithmetic)

The owner pinned the actual NASA CR-1457 PDF (10,571,741 B) in their outputs. I hashed it (sha256 6a1a55855cc2c8b0a864289518b868a0528db319739a26eacb6a4b262f110b51 — matches the INPUTS pin) and extracted its text: the title page is "NASA CR-1457 MANUAL FOR STRUCTURAL STABILITY", and every equation form the card uses is present in the document — σ₀ = η·E_f·h/(R√(1−ν²)), Kc = 1 − Vc/4 for Vc ≤ 2 and Kc = 1/Vc for Vc > 2 (both branches print verbatim at 6.2-3/6.2-4), σcrimp with the Gc/(2·tf·tc) factor, the recommendation "γd = 0.20 … except where shear crimping occurs" (the card's meager-tests caveat appears as "insufficient data"), Q = 0.50 for 2.2-5, the biaxial interaction R_x³ + R_y = 1 (2.2-6/2.2-15), and the honeycomb 0.33·E·√(Ec·tf/(E·tc)) form (2.2-14). The equal-elastic-faces premise matches the handbook's own stated equivalence condition.

## What was re-derived

230 fields, 0 mismatches, all from the COMMON.md pins plus the 007 geometries (which CHECK-007 re-derived independently):

- All 14 comparison rows: σ₀, σcrimp, Vc, Kc, γ_d, SF_classical, SF_general = γd·Kc·σ₀·4tf/(Rp) computed through the handbook chain (not as ratio×classical), SF_y, least, and the identity SF_general/SF_classical = Kc on the moderate branch — every sourced core stays below Vc = 2 (max 0.5451), so γd = 0.20 everywhere reported.
- Foam wrinkling: 0.5(E·Ec·Gc/(1−ν²))^(1/3), the advisory-uniaxial counterpart, the biaxial root R³+R=1 = 0.6823278038280194 (my own Newton solve), the conversion ratio 0.709062069568, both stress SFs per material.
- Honeycomb wrinkling (HRH-10 ×2): 0.33·E·√(Ec·tf/(E·tc)) and equibiaxial SFs 0.0565286364026 / 0.0415196459641 — both below their trimmed general-instability factors, so the card's "would govern if admitted" reading holds; the foam rows stay above.
- Crimp boundary table, all 17 geometries: Gc* = E·tf·tc/(R√(1−ν²)·h), including P2-E 2445868.57733 Pa and the 1 kg/m³ equal-line 4635858.19265 Pa; buckling-peak rows all ≈2.453 MPa (2,453,028–2,453,116 Pa) as the card states; every sourced Gc (min 9 MPa) is above the boundary.
- The infinite-shear identity (Gc→10³⁰ restores Kc→1 and exactly the kd-0.2 classical pressure), the P2-E classical 0.233885578993 recomputation, the Vc=2 discontinuity note (Kc continuous at 0.5, γd jumps 0.2→1), the crimp-pressure h/tc ratios (1.00296296…1.00599700), and the trim range 0.863720643326 (HRH-10-6.4-24, largest) to 0.991105457684 (Plascore 3/16 at 32, smallest).
- All 6 INPUTS pins hash-match (the four 007 artifacts + compute.py + the PDF).

## Result

**0 mismatches.** Two early mismatch batches were bugs in my own checker (coincide rule applied to the wrong table; then infeasible equal-line splits at ρ=32 where the splits coincide) — fixed; the owner's values matched everywhere after. Status ESTIMATE, tag QUESTIONABLE, certification none; NFI set carries the γd-jump, biaxial-interaction and core-floor caveats honestly.

## Notes (no objection, no NFI opened)

1. Equation numbers 6.2-25…6.2-29 were not individually located in my extraction; the forms the numbers were cited for (critical-pressure conversion and dome factors) appear in the section's text and figures. The arithmetic uses only the forms I verified.
2. The card's "gamma_d = 0.20 is the same number as kd" is a coincidence of values, not a shared derivation — the card itself says so; no action.
