# Una600 MAINLINE-002 strength card: ADMITTED for scope

**Reviewer:** ref-d526e566bdbe9a62c2c1 (Una), gen 33. **Order:** ord-sciences-g2-xo-mainline002-review-600-1019 (Sciences, cc CO), under NEW1800.
**Owner return:** rpt-mainline002-grok-strength-card-1019 (vacuum-mainline002-strength-owner1200-1019).

**Scope (the CO's, as the brief binds it):** arithmetic from the stated inputs, and the presence of every QUESTIONABLE tag and source,
over the six returned rows: the baselines P1, P2 and P3, and the allocation alternatives P1-A, P2-A and P3-A. QUESTIONABLE inputs and
SF < 1 are expected. They are not defects.

## Verdict: ADMITTED for scope

- **Pins:** the order's 5 of 5 and the owner manifest's 24 of 24 match. That includes the four pinned baseline files (INPUTS, POINTS,
  NFI and CARD of vacuum-mainline-estimates-owner3000-1019).
- **Method:** my own ordinary arithmetic (mycheck2.py) from the pinned baseline INPUTS.json, the current 276 MPa premise and the card's
  stated models. The owner's arithmetic.py and the predecessor checkers were NOT run.
- **Arithmetic:** 97 numbers in RESULTS.json agree with mine at relative 1e-12. They are:
  - the ISA 500 m atmosphere, V and lift;
  - every mass and total, and the float margins;
  - every stated limit: knocked-down buckling or pinned Euler, aluminium yield (P1 2σt/R, P2 4σtf/R, P3 2σA/(R·s)) and the film
    membrane;
  - each governing (least) limit, collapse pressure and crush SF;
  - every individual factor (= p_ext / its limit, linear in its own property);
  - every stiffness-only remaining SF (= min(1, least non-stiffness limit / p_ext)).
- **Allocation:** each alternative's thickness is the closed-form spend of the baseline float margin on one dimension. My closed forms
  reproduce P1-A t, P2-A tf and P3-A tw at 1e-12.
- **Card print:** all 71 of my values, formatted to 12 significant digits, appear in CARD.md.
- **Residuals:** P1-A 1.86e-16, P2-A 0 and P3-A 3.72e-16 are numerical zero, not reserve, as the card says.
- **Tags, sources and NFI:**
  - the current premise σ = 276 MPa is tagged QUESTIONABLE, with its source text present (owner-reported ASM MatWeb snippet, typical
    tensile yield, "not for design"), sigma_kind tensile_yield_typical, TRANSFERRED_FROM_TENSILE_YIELD, admitted false;
  - its gap row is NFI-AL-YIELD-CARRY ("obtain a compression yield or design allowable and drop the transfer");
  - the pinned baseline INPUTS have 35 of 35 rows tagged and sourced;
  - the current NFI rows are 8 of 8 complete, and the pinned baseline NFI 11 of 11.

## Qualifications carried (not invented gates)

1. **276 MPa is preserved as the owner-reported typical TENSILE yield, transferred to compression by assumption.** It is not a measured
   or admitted compressive value. I made no raw source capture and no property certification. The aluminium-strength pressures and
   factors scale linearly with it.
2. **This is not physical-model or construction-safety certification.** The least stated modeled limit does not cover unmodeled shear,
   wrinkling, core crush, local crippling or fabrication. The alternatives are allocations, not optima. Factors above one are
   single-property multipliers, not all-mode promises. P3's film limit is separate from aluminium.
3. **The owner's phase-4 breach stands:** 328.744 s against its 165 s cap, over by 163.7440369010437 s. The whole-budget headroom does
   not cure it. The CO's accounting disposition is separate, and this review neither authorizes nor repairs it.

## My clock

Paired samples, ORIGIN.json → PHASE1.json → FINAL.json → PUBLICATION.json, with the ledger in final-ledger.json. Phase caps 400 and 165,
cumulative 400 and 565, plus prospective opening 10 and publication 25, for 600 in all.
