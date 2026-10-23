# Una600: the main-line estimates card (unit vacuum-mainline-estimates-review600-1019): ADMITTED for scope

**Order:** ord-sciences-g2-xo-mainline-estimates-review-600-1019, with the carry ord-sciences-g2-una-mainline-yield-qualification-carry-1019.
**Origin:** 2026-10-20T02:44:41.668581Z, monotonic 2079806.849. It was taken after my prior units closed and before any intake.
No review overlapped.
**Pins:** order 4/4 and carry 4/4 re-hash; the owner manifest is 22/22 (the 16 owner artifacts, the inputs and the authorities).
**Method:** my own ordinary arithmetic (mycheck.py), from INPUTS.json and the card's stated equations. I did not run the owner's
arithmetic.py or any checker.

## VERDICT: ADMITTED, for the CO's scope only

The scope is the arithmetic from the stated inputs, and that every QUESTIONABLE tag and source is present.

- **Arithmetic: 41 stated numbers agree at a relative 1e-12** with POINTS.json and the card (mycheck.log). They are:
  - **The atmosphere:** ISA at 500 m, T 284.9 K, p_ext 95460.8379139 Pa, rho 1.16726833075. The card prints rho rounded to 12
    significant digits; the machine value in POINTS.json agrees.
  - **Volume and lift:** V 4188.79020479 m³ and lift 4889.44215019 kg.
  - **The masses and float margins, for each point:**
    - P1: 2812.54845073 kg, margin 0.424771095693;
    - P2: 3636.17669088 kg, margin 0.256320745969;
    - P3: 1616.62967026 kg, margin 0.669363166472.
  - **The collapse pressures and SFs:**
    - P1: Zoelly with kd 0.2, 82.5945600261 Pa, SF 0.000865219307;
    - P2: the owner's sandwich extrapolation with kd 0.2, 11701.5583953 Pa, SF 0.122579674043;
    - P3: the lesser of pinned Euler (3170.21055887 Pa) and the film limit (240000 Pa), SF 0.0332095404582.
  - **The Zoelly identity** 4/R²·√(D·S) holds.
  - **The improvement factors** = 1/SF, linear in E: 1155.77633544, 8.15795936651 and 30.1118288963.
- **The sensitivities:** charter density, sea level, and P2 with a 0.16 m core. All ten values agree to the card's printed precision,
  better than 5e-11.
- **Tags and sources:** all 35 input rows carry QUESTIONABLE and a non-empty source or explicit assumption basis. All 11 NFI rows
  are complete, and every NFI reference resolves. Every point's input id has its row.
- **QUESTIONABLE inputs and SF<1 are expected, not defects.**

## Qualifications carried (not gates)

- **The yield carry:** aluminium structural yield is absent from the three stated models, checked by reading the card:
  - P1 is Zoelly only;
  - P2 is the sandwich extrapolation, with core shear, wrinkling and crush omitted;
  - P3 is Euler plus the film limit, with no member yield.
  - So the modulus factors are conditional buckling/Euler factors within those models. They are NOT a strength-complete or all-mode
    SF1 requirement: raising E alone does not establish a non-crushing design.
  - NFI-AL-YIELD-CARRY and NFI-FLOAT-ALLOCATION-CARRY stay Sciences' carry. The advisory's numerical yield factors are not admitted
    here.
- **This admission certifies none of:** material values, model validity, knockdowns, omitted physics or construction safety.
- **The admission's date and scope, for the map-point ruling:** the arithmetic and the tag/source presence above, at this filing.

## Reviewer clock (final-ledger.json)

Phase 1: 110.578 s of 400. Phase 2 and the final figures are written to the ledger by publish.py at the final sample. No processes
ran except my read-only arithmetic.
