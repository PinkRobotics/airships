# MAINLINE-017b: improvement directions restated with trends (rpt-ref-6ba73ec8a89453b26832)

Order: ord-admiral-rr2-mainline017b-dispatch-1019, from admiral-robotics-review-v2. Brief: CARD-017b-IMPROVEMENT-DIRECTIONS-RESTATED.md with COMMON.md.

Files: `.ship/work/outputs/vacuum-mainline017b-improvement-directions-1020/`.

Sourcing files: `.ship/work/sources/017b/{be-face,core-film,knockdown,p3-materials}.{json,md}`. Four sourcing sub-workers of this seat wrote them; there are 235 rows, each with a URL or DOI, a location and a quote.

## Re-run (in the outputs directory, with TMPDIR=unpublished-local-ref:1ffe4110219d37c0 and OPENBLAS_NUM_THREADS=1)

Run these in order:
1. `python3 val17b.py`: 34 reproduction checks against 028, 021b and 022c.
2. `python3 run17b.py`: COMPUTE.json, about 5 minutes.
3. `python3 extra17b.py`: EXTRA.json.
4. `python3 trend17b.py`: TRENDS.json. It asserts every sourced value.
5. `python3 card17b.py`: CARD.md.
6. `python3 finalize17b.py`: RESULTS.json, NFI.json and INPUTS.json.

## Basis

These choices are made deliberately; each is an NFI row.

**P2:**
- Face: SR-200 at E 290 GPa and 345 MPa (minimum tensile, used as compressive), 1850 kg/m3. Poisson 0.08 (IAEA, VHP), not the inherited 0.33, which reads 2 percent higher.
- Core: CR-III 5056 3/8-1.0. Flatwise strength Fc is 60 psi (Table II typical stabilised strength), used for the flatness map.
- Gamma: the CR-1457 handbook rule, 0.20 below Vc 2 and 1 at and above. 018's conservative 0.20 everywhere is also run.
- Joining: 028's model replaces the 5% allowance, as 028 did. It is AF 163-2U at 0.015 lb/ft2 on both lines, plus a scarf of at least 30:1 sized to 028's 10 MPa screen, plus splice and seal, on stock 609.6 x 1828.8 mm panels.
- Reserve: 019's optimistic fixed items, 411.30 kg at R 10. They scale with R by 027's laws (water and contamination with R^2; the others with R^3). Payload is 0.

**P3:**
- 022c's equilateral rows: Ti + Kapton is "today" and CFRP wrap + Zylon is "projection", on 019's P3 reserve.
- The search is finer than 022c's (a 40-point film grid plus Nelder-Mead). The SP-8007 local gamma is capped at 1.

## Results

**P2 today:** 0.5284 at R 10 and 0.5711 at R 20, with global buckling and wrinkling tied.

Alone to SF 1:

| Property | R 10 | R 20 | Note |
|---|---|---|---|
| Lighter face (Be's E and strength) | x1.871 | x1.734 | |
| Gamma | x4.059 (0.812) | x3.409 (0.682) | 015 map: 2.47 mm dimple at R 10, 13.1 mm at R 20 |
| Face modulus | x2.041 | x1.928 | Only at the Vc 2 step: a knife edge |

Every other property is not alone, and global buckling binds next.

**P2 cheapest combination:**
- The lighter face alone is cheapest.
- Keeping Be: gamma alone.
- Keeping Be with handbook values: product 13.06 at R 10, from core density ÷1.94, Ec x4.54 and K_delta ÷1.485. At R 20 the product is 9.50. The core Ec/rho needed is 57 and 41, beyond aluminium's 24.8.

**P3:**
- Today's row: 0.7097. The projection row: 1.4412.
- Alone on today's row:

  | Property | Factor |
  |---|---|
  | Tube density | x1.406 |
  | Tube modulus | x1.608 |
  | Film specific strength | x3.791 |
  | Lattice knockdown | x1.986 |

- The cheapest combination is tube density alone. Keeping SiC, it is lattice alone. Keeping SiC with no analysis optimism, it is film alone.
- SiC compressive strength: every route to SF 1 needs 0.83-1.20 GPa, qualified. The projection row needs 907 MPa.

**Trends:**
- Be, Al honeycomb, SiC, the knockdown and wrinkling design values are flat. Be sheet has shrunk.
- Film specific strength is 2.2 percent a year since 1975 and 4.1 since 1999. Upilex-S gives x2.17, and the rest takes 14-25 years (PROJECTION).
- Bond film halved from 1954 to 2009, then went flat.

## Deferred and open

There are 15 NFI rows. The crimp-branch combinations do not survive re-optimisation, because they sit at Vc 2 minus epsilon; the card reports the stiff-branch answers only.

## Next

The brief says stop and file. The robotics seat sends the next job.
