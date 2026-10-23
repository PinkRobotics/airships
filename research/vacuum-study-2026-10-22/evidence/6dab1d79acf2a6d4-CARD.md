# MAINLINE-035 — measured knockdowns of sandwich shells at moderate Vc

Unit vacuum-mainline035-sandwich-knockdown-tests-1020. Order ord-admiral-rr2-mainline035-dispatch-1019. Seat
ref-55cff924be25afe6f9dd (claude-opus-5-5, max). Every value is QUESTIONABLE, and PROJECTION where named. Nothing
here is a certification.

## The answer

- **Cylinders.** The only modern, fully documented sandwich-shell buckling tests at moderate Vc are NASA SBKF's 8 ft
  honeycomb-core composite cylinders. Measured over the linear eigenvalue, they give 0.721 to 0.87, at Vc 0.32 to 0.53
  (my lamination arithmetic; 0.21 to 0.83 across conventions) and R/rho 335 to 413. That is 1.29 to 1.56 times SP-8007.
  The pre-1969 sandwich cylinders in CR-1457 Fig. 4.2-3 sit near SP-8007, at 0.42 to 0.76 over R/rho 105 to 1300. Their
  Vc is unknown, below 2. FPL 1830's two cylinders, at R/rho 1050 and 1300, read 0.42 and 0.44.
- **Spheres.** The only measured sandwich-dome knockdowns are the Saturn S-II set summarised in NASA CR-1457, Fig. 6.2-3.
  There are two hemispheres at gamma 0.22 to 0.24 (R/rho about 240, Vc not recoverable) and six ellipsoids at 0.39 to
  0.99. Nothing else was found.
- **Vc 0.9 to 2.** No measured point exists in any shell form.
- **Verdict.**
  - As a cylinder, 021b's 0.468 is at the edge of the record. The pre-1969 cylinders interpolate to about 0.46 at its
    R/rho, and SBKF scaled to that R/rho gives 0.62 to 0.75.
  - As a cylinder, 021's 0.595 is beyond the pre-1969 record at its R/rho (about 0.43, so 1.39 times) and at the edge of
    the SBKF-scaled one (0.54 to 0.65).
  - As a sphere, both are beyond. They are 2.0 to 2.7 times the only measured sandwich hemispheres, and 2.1 to 3.3 times
    the SBKF record carried to a sphere.
  - Only a direct transfer, with no sphere penalty, puts them inside. No source supports that transfer.

## 1. The test record

Four research sub-workers covered the source families, and I verified the load-bearing numbers at source: the SBKF ratios
in the NASA texts, and CR-1457 Fig. 6.2-3 read from the page image. LIT-A to LIT-D.json hold every record, with the page,
table or figure and a quote of 15 words or fewer. "Linear" means the perfect-shell linear eigenvalue, which includes
transverse shear in these shell models.

| record | shell, load | Vc (this seat) | R/rho | measured / predicted | basis | source |
|---|---|---:|---:|---:|---|---|
| SBKF CTA8.1 | 8 ft cylinder, axial | 0.53 (0.41-0.83) | 335 | 0.87 | linear eigenvalue | Schultz et al. 2018, NTRS 20180002092 |
| SBKF CTA8.2B | 8 ft cylinder, 90% axial + 10% bending | 0.40 (0.26-0.60) | 397 | 0.721 | linear, combined load | NASA/TM-20210024081 |
| SBKF CTA8.3 | 8 ft cylinder, 90% axial + 10% bending | 0.32 (0.21-0.48) | 413 | 0.864 | linear, combined load | NASA/TM-20210024768 |
| SBKF CTA8.2 | 8 ft cylinder, axial | 0.40 | 397 | 0.775, core crush at a ring | not a buckling datum | NASA/TM-20210024095 |
| S-II hemispheres (2) | sandwich hemisphere, external pressure | n/a | about 240 | 0.22-0.24 | classical sandwich sphere with core shear | CR-1457 Fig. 6.2-3, NTRS 19700004831 |
| S-II ellipsoids (6) | sandwich near-ellipsoid domes | n/a | 240-480 | 0.39-0.99 | as above | CR-1457 Fig. 6.2-3 |
| CR-1457 axial set | pre-1969 sandwich cylinders, axial, non weak-core (Vc below 2); eye-read by the researcher and by this seat from the page image | n/a | 105-1300 | FPL PE-227: 0.61, 0.63, 0.76 (R/rho about 105); Baker 1968: 0.545 (180), 0.57, 0.58, 0.69 (270), 0.49 (410); FPL 1830: 0.42 (1050), 0.44 (1300); Baker cones: 0.51-0.58 (195). All are on or above the design curve, which is 75% of SP-8007 in R/rho | classical with core shear | CR-1457 Fig. 4.2-3 (PDF p. 188) |
| CR-1457 lateral pressure | 7 cylinders | n/a | n/a | 0.56, 0.88 (Kazimi); 1.00-1.16 (FPL) | classical, MIL-HDBK-23 | CR-1457 Sec. 4.4.1.2 |
| TN D-2926 | 3 honeycomb cylinders, about 77 in, bending | n/a | n/a | about 0.87-0.92 (CR-1457 reads 0.62-0.80) | small deflection, by eye | NTRS 19650020360 |
| TN D-7935 | 3 honeycomb 120-degree cones, external pressure | n/a | n/a | 19-29% below FE | SALORS, BOSOR 2 | Anderson and Davis 1975 |
| NASA fairing panels | curved 3 x 5 ft panels from a 10 m barrel | n/a | n/a | eigenvalue 3-24% above test | linear FE | Pineda et al. 2014, NTRS 20140006743 |
| Muc et al. 2018 | deep cylindrical panels, R 92 mm | n/a | n/a | linear FE 8.49% above test | linear FE | doi 10.1007/s10443-017-9614-8 |
| Sim 2024 / EUCASS 2023-367 | foam-core hemispheres | about 200 | about 26 | 1.44-1.54 against crimp (018b) | crimp pressure | doi 10.1155/2024/8765733; doi 10.13009/EUCASS2023-367 |

**Not usable or not found.**
- Cunningham and Jacobson (1962) tested in the plastic range.
- The primary sources behind CR-1457's sandwich data were not retrievable from here: FPL 1830 (March and Kuenzi 1957),
  Baker 1968, the 1963 Hexcel summary, FPL PE-227 and Kazimi 1960.
- The DESICOS sandwich-shell results (Bisagni 2016) are in a restricted paper.
- Gonzalez and Patton's SDL 468, which holds the S-II per-specimen data, was not found.
- Brix 1968 (GFP sandwich domes) and Anderson 1966 (spherical sandwich shell) are unread leads.
- No foam-core cylinder test and no marine sandwich sphere test was found.

## 2. The map (gamma-map.png)

**How the points are placed.**
- **Vc.** Every point uses the line's definition: Vc = sigma0/sigma_crimp = 2*E_f*t_f*t_c/(R*sqrt(1-nu^2)*(t_c+t_f)*G_c).
- **Face moduli.** The SBKF faces were computed by classical lamination theory from the stated lamina values and layups,
  with a generic G12 of 0.77 Msi, the value the CTA8.1 paper assumed. The results are 7.88 Msi quasi-isotropic, and 8.31
  by 5.96 Msi for CTA8.1.
- **Vc conventions.** The plotted Vc uses isotropic-equivalent face and core values (geometric means). The bars span
  "axial face with axial G13" to "the softer core direction".
- **Basis.** The SBKF ratio is against a shear-inclusive eigenvalue, so it is directly a gamma on the line's basis.
- **Cross-check.** SP-8007 at each article's R/t_eq (t_eq = sqrt3*h) reproduces the stated value: 0.560 against the
  stated 0.562 (CTA8.2B), and 0.586 against 0.61 (CTA8.1, orthotropic form).

**Panel (a), gamma against Vc.**
- The three SBKF buckling points sit at 0.72 to 0.87 at Vc 0.3 to 0.5. That is well above 018's optimistic curve there,
  which reads 0.33 to 0.41.
- The two leads sit at Vc 0.89 and 1.06, where nothing has been measured. 021's 0.595 is 0.95 of the optimistic curve's
  0.624.

**Panel (b), gamma against R/rho.**
- The leads sit at R/rho 649 and 950. The only measured sandwich shells at that slenderness are FPL 1830's two
  cylinders, at 0.42 and 0.44 (R/rho 1050 and 1300).
- The pre-1969 cylinders follow SP-8007 at R/t_eq roughly. The SBKF cylinders sit above it. The S-II hemispheres sit at
  the 0.20 line.
- The handbook monocoque lines show how sphere and cylinder diverge at the same t_eq.

## 3. Cylinder to sphere

**What is the same.** The classical baseline is identical. A pressurised sphere and an axially compressed cylinder buckle
at the same membrane resultant, 2*sqrt(D*Y)/R. So sigma0 and the core-shear factor Kc are the same, and a cylinder's gamma
is comparable on the baseline.

**What differs.** Imperfection sensitivity differs. At the leads' R/t_eq of 274 and 187:
- SP-8007 gives 0.419 and 0.482 for a cylinder.
- SP-8032 gives 0.142 and 0.143 for a sphere, a ratio of 0.30 to 0.34.
- CR-1457 makes the same split for sandwich: 0.20 for hemispheres, against its cylinder curve's 0.32 and 0.36 at these
  R/rho.
- The one measured sandwich hemisphere pair, at 0.22 to 0.24, agrees with that split.

**Three readings.** Carrying the SBKF record to the lead points gives:

| transfer | 021 rev1 (needs 0.595) | 021b (needs 0.468) |
|---|---:|---:|
| direct, no sphere penalty (no source supports it) | 0.72-0.87 | 0.72-0.87 |
| pre-1969 sandwich cylinders, interpolated at the lead's R/rho (Baker 410 to FPL 1830's 1050) | about 0.43 | about 0.46 |
| SBKF's beat on SP-8007, as a cylinder at the lead's R/t_eq | 0.54-0.65 | 0.62-0.75 |
| SBKF's beat on SP-8032, as a sphere at the lead's R/t_eq | 0.18-0.22 | 0.18-0.22 |
| measured sandwich hemispheres (S-II) | 0.22-0.24 | 0.22-0.24 |

## 4. The verdict

- **021 rev1, gamma 0.595 at Vc 1.06 and R/rho 950.** On the sphere record it is beyond, at 2.5 to 3.3 times. As a
  cylinder it is beyond the pre-1969 record at its slenderness (about 0.43, so 1.39 times) and at the edge of the
  SBKF-scaled one (0.54 to 0.65).
- **021b, gamma 0.468 at Vc 0.89 and R/rho 649.** On the sphere record it is beyond, at 2.0 to 2.6 times. As a cylinder it
  is at the edge: the pre-1969 record gives about 0.46 there, it sits on SP-8007's own line, and SBKF scaled gives 0.62 to
  0.75.
- **What the best results needed.** SBKF's 0.86 and 0.87 came from these conditions:
  - Autoclave or AFP carbon faces on stiff aluminium or Korex honeycomb, at Vc 0.3 to 0.5 and R/rho 335 to 413.
  - Potted, ring-supported ends.
  - Shape measured and modelled. CTA8.3's prediction came within 0.1% only with the as-installed radial imperfection.
  - CTA8.2 failed at its ring by core crush before buckling. Load introduction is a failure mode in its own right.
- **What the S-II hemispheres achieved.** They reached 0.22 to 0.24 at R/rho 240 with production-quality aerospace
  construction.
- **Reading.** No measured shell of either kind supports gamma near 0.5 to 0.6 for a sphere at Vc about 1 and R/rho 650 to
  950. The record cannot settle it either way, because it holds no sphere at moderate Vc and no shell at Vc 0.9 to 2.
  MAINLINE-029's FE at the lead's own geometry is the instrument that can. A test sphere would need imperfection control
  beyond anything recorded for sandwich domes.

## 5. Open rows (NFI.json)

| row | open issue |
|---|---|
| NFI-035-SPHERE-VC | the S-II hemispheres have no recoverable Vc (SDL 468 not found), so the only sphere data cannot be placed on the Vc axis |
| NFI-035-VC-GAP | there is no measured point at Vc 0.9 to 2 in any form; 018's rise across that range is untested |
| NFI-035-TRANSFER | the cylinder-to-sphere transfer has no sandwich test behind it; the handbook ratio is 0.30 to 0.34 |
| NFI-035-SBKF-VC | the SBKF Vc rests on this seat's lamination arithmetic with a generic G12 and geometric-mean conventions |
| ref-5e993e8eb72d4845aa62 | FPL 1830, Baker 1968, the Hexcel 1963 summary, FPL PE-227 and Kazimi 1960 are unread |
| NFI-035-DESICOS | the measured Ariane sandwich shells are in a restricted paper |
| NFI-035-DOME-LEADS | Brix 1968 and Anderson 1966 are unread, and may hold the only sandwich-dome series |
| NFI-035-SP8007-P | SP-8007's lateral-pressure factor is 0.90 in the 1965 edition as CR-1457 cites it, and 0.56 in 1968 |
| NFI-035-PALETTE | the chart palette is the skill's documented passing set; its validator could not run here (no JavaScript runtime) |

## Method

- **Sources.**
  - LIT-A.json: SBKF.
  - LIT-B.json: the older NASA, NACA and FPL record.
  - LIT-C.json: spheres and domes.
  - LIT-D.json: launch vehicles and fuselages.
  - These were written by four worker-sonnet-high research sub-agents. Each cites only what it opened, with a location and
    a quote of 15 words or fewer; paywalled items are marked abstract-only.
- **Verification at source by this seat.**
  - SBKF ratios: 0.87, 72.1%, 86.4% and 77.5%, together with the ply and core tables, checked in the NASA texts.
  - CR-1457 Fig. 6.2-3, read from the page image.
- **Analysis.** analyze035.py: lamination theory, Vc, R/rho, handbook curves, transfers and the chart. The results are in
  RESULTS-ANALYSIS.json, and RESULTS.json collects everything.
- **Citations.** The 1963 and 1969 sources are cited by identifier only. No text is copied beyond the quoted fragments in
  LIT-*.json.

Times are measurements only: work started at 2026-10-20 01:33:51 PDT and ended at the filing.
