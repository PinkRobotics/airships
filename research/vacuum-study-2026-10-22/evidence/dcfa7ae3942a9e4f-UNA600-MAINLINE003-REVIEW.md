# Una600 MAINLINE-003 P2 targets card: ADMITTED for scope; two NFI dependency sentences are inconsistent with the card's formulas

**Reviewer:** ref-d526e566bdbe9a62c2c1 (Una), gen 33. **Order:** ord-sciences-g2-xo-mainline003-review-600-1019 (Sciences, cc CO), under the
existing NEW1800. **Owner return:** rpt-mainline003-grok-p2-targets-1019. **Clock:** origin 05:14:06.487Z, after my two landing audits
closed. Under the Desk's 22:09 ruling (ord-boyce-co-vacuum-no-single-thread-1019) this check gates nothing.

## Verdict

**ADMITTED for scope:** the arithmetic, and the presence of every QUESTIONABLE tag and source, for P2-C, P2-K, P2-E and the P2-A
comparison.

**DEFECT, exact, text only:** two NFI "effect" sentences contradict the card's own formulas. No number changes.

1. **NFI-AL-YIELD-CARRY** says "the required compressive strength scale[s] linearly with this value".
   - The card's σ_req = σ·p/p_yield = pR/(4·tf), which is the membrane stress at external pressure.
   - That is independent of the assumed σ: doubling σ to 552 MPa leaves it unchanged (ratio 1, deps.log).
   - Only the strength pressure and the strength SF scale with σ.
2. **NFI-KD** says "the required modulus scale[s] directly with the knockdown".
   - E_req = E·p/p_b = pR²√(1−ν²)/(4·kd·tf·d), which scales INVERSELY with kd: doubling kd halves it (ratio 0.5).
   - Only the buckling pressure and the buckling SF scale directly with kd.
   - This bears on MAINLINE-004 (NFI-KD): a larger named knockdown lowers the required E.

## What I checked (mycheck3.py, my own arithmetic; no owner, advisory or predecessor script run)

- **Pins:** the order's 5 of 5 and the manifest's 31 of 31.
- **Arithmetic:** 90 numbers agree at relative 1e-12, with 0 mismatches. They cover:
  - the atmosphere;
  - each rule's geometry, from the ceiling M = (lift − S − G)/(1 + J):
    - P2-C: core takes the ceiling;
    - P2-K: one factor k on tf and core;
    - P2-E: equal face and core mass;
  - all masses, the totals and the zero float residual (no reserve);
  - the buckling and yield limits, the governing limit, the collapse pressure, the buckling, strength and least SFs, the factors,
    E_req, σ_req and the membrane stress;
  - the advisory targets: Gc = pR/(2d), Ec·Gc = (2σ_m)³/E and the equal-split √;
  - P2-A, recomputed by MAINLINE-002's closed form, against the card's block and against sealed MAINLINE-002's limits and mass.
- **Card print:** 56 of 56 numbers match.
- **Tags, sources and NFI:**
  - the rows are tagged QUESTIONABLE, and 276 MPa carries TRANSFERRED_FROM_TENSILE_YIELD;
  - the pinned MAINLINE-001 inputs are 35 of 35 tagged and sourced;
  - NFI is complete: 10 of 10 current, 11 of 11 pinned 001, 8 of 8 pinned 002;
  - core crush is NO_FORMULA_IN_BRIEF;
  - shear, wrinkling and crush are omitted from the least SF, as declared.
- **NFI-SHEAR's dependency** ("Gc ∝ p, ∝ 1/d") is correct.

## Qualifications carried

- 276 MPa is a QUESTIONABLE typical tensile yield, transferred to compression by assumption. NFI-AL-YIELD-CARRY is grounded in
  parallel and never gates.
- These are three fixed rules at 16 kg/m³ and are not an optimum.
- This is not material, model, property or construction-safety certification.
- The MAINLINE-002 correction accounting is settled, per the CO's disposition. It is not reopened here.
