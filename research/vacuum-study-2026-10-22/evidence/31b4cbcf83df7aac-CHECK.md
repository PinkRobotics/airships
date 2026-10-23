# MAINLINE-008 check — ref-cca93dbfd236dcaa3a8b

Unit vacuum-mainline008-check-1019. Card rpt-ref-45da79edf548b064b228. Order ord-admiral-rr2-check008-dispatch-1019.

Queue view rendered 2026-10-19T22:47:29-07:00. Arithmetic log written 2026-10-19T22:57:53-07:00. Times are measurements, not limits.

Method: check008.py, this directory. Aluminium safety factors from the COMMON.md sandwich formulas and the pinned 002/003 geometry (P2-A from 002; P2-C, P2-K, P2-E from 003). Candidate safety factors from the brief's first-order rules and the card's stated rho, E and sigma_c. Not the owner's compute.py.

## Arithmetic

Aluminium SF_b, SF_y, tf and separation match the card's rows_from at relative difference below 1e-15.

480 derived comparisons against RESULTS.json (figures, equal-mass thickness, tf/d, SF_b, SF_y, least SF, gap, both improvement factors, and the limiting figure) for 15 candidates and 4 rows. Worst relative difference 5.672e-16.

Rank by least SF in P2-E matches the card, 1 through 15. The 6061 candidate reproduces the pinned aluminium rows. CARD.md digits match, including the materials-direction factors. Pins named in the card: 16 of 16. The four filed card files match their stated sha256.

Worst tf/d is 0.007222230. If the core is held and separation follows the new face thickness, SF_b moves by at most 0.348 percent. The card uses the brief's first-order form, which drops that term. Yield has no such term: it follows sigma_c/rho exactly at equal face mass.

P2 buckling safety factors scale with kd. That claim is right for this card. 41 ksi converts to 282.685 MPa and rounds to the card's 283 MPa.

## Tags and sources

All 15 candidates are tagged. Thirteen are QUESTIONABLE and two, CNT-yarn and graphene, are PROJECTION. Each source is a URL, a DOI, or a handbook name. 6061, 7075 and Ti-6Al-4V cite ASM MatWeb by sheet name; the 6061 URL also sits on the pinned 001 inputs.

## Mismatches

These are basis sentences. The table uses the rounded moduli, and those table numbers match.

| row | field | card | stated product |
|---|---|---|---|
| CFRP T700/epoxy | E | 54 GPa | 0.40 × 134 = 53.6 GPa |
| CFRP M55J/epoxy | E | 135 GPa | 0.42 × 325 = 136.5 GPa |
| CFRP K13D2U/epoxy | E | 210 GPa | 0.41 × 515 = 211.15 GPa |
| Boron/epoxy | E | 86 GPa | 0.42 × 204 = 85.68 GPa |
| CNT-yarn PROJECTION | E | 180 GPa | 0.50 × 256 GPa per g/cc × 1.40 g/cc = 179.2 GPa |

Boron compressive strength is 0.34 × 2500 = 850 MPa and matches. T700, M55J and K13D2U compressive strengths give a factor, or none, and no numeric unidirectional strength, so those three cannot be re-derived.

## NFI from this check

NFI-CHECK-008-BASIS. Write each quasi-isotropic modulus as the product, or state the rounding that produced 54, 135, 210, 86 and 180. Name the unidirectional compressive strength behind 520, 350 and 220 MPa. Recomputing with the products does not change the P2-E rank order.

This does not stop the card or MAINLINE-008b.
