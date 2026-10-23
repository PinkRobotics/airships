# MAINLINE-055: the gamma test

Unit vacuum-mainline055-gamma-test-1020. Order ord-admiral-rr2-mainline055-dispatch-1019. Author: ref-55cff924be25afe6f9dd (claude-opus-5-5, max).

Every value here is QUESTIONABLE or a PROJECTION; nothing is a certification. No supplier or lab was contacted; they are named only.

Gamma is p_collapse / (Kc · p_classical) of the article's own section, the line's convention (028b, 038).

## The answer

**The test.** The cheapest test that would move gamma from optimism to evidence is three full-cross-section spherical caps on the true R 10 m curvature.
- **Size:** 5 m in diameter.
- **Section:** 5052-O faces 3.10 mm thick on the real Hexcel CR III 5056 3/8-1.0 core, 20.9 mm thick. The faces are matched to beryllium's classical buckling stiffness, and the face separation is held.
- **Construction:** built with the route's panels and seams, with a reinforced edge.
- **Defects:** each cap is seeded with one pole dimple at 2, 6 or 16 mm over a 0.357 m width.
- **Loading:** evacuation under the cap plus a water head above it.

**The cost** is about USD 0.4–1.6 million for the three. That is a PROJECTION: once-only costs of 0.21–0.69M plus 0.07–0.29M per article.

**Before buying:**
- Settle the dimple tolerance, which is now the deciding unknown (N055-01).
- Measure SR-200 compression (038 T1), because the stand-in is matched to the 345 MPa proxy.
- Witness-test the CR III core's shear and crush strengths (ASTM C273, C365). Per CHECK-029 the core shear governs.
- Fix the rig concept. No commercial 5 m chamber was found.

**What the cheaper option misses.** 038's T7 model shells (R 0.5 m, aluminium foil on foam, USD 30–90k) are cheaper but cannot measure P2's gamma. CHECK-029 shows that at the specified dimples, the lead's capacity is set by core shear strength, face yield and the honeycomb core law, and a foil/foam model has none of them. T7 remains a useful elastic-FE calibration.

**The pre-test prediction is adverse.** My elastic FE of the R10 lead section (028b) gives gamma 0.469–0.511 at 042's tolerance dimples (9.3–16.1 mm), not 0.564. The core reaches its typical shear strength there at 25–38 kPa, which is 0.26–0.40 of operating. The test would most likely confirm the record unless the build holds much tighter shape.

## 1. Scaling

### The groups a subscale article must keep

The R10 lead is 028b's nominal section: faces 0.7946 mm, core 23.237 mm. The R30 point is 040's ISA least set: faces 2.465 mm, core 102.6 mm, gamma 0.3865 (0.373–0.418 across 040's ISA rows).

**R/h (face-centroid separation h).** R10 416, R30 286. Controls imperfection sensitivity; Reis 2017 shows that above R/t ≈ 200 the knockdown converges to the thin-shell limit.

**Vc = p_classical / p_crimp.** R10 0.953, R30 0.996. Shear flexibility, Kc = 1 − Vc/4. The record has no shell at Vc 0.9–2 (035).

**Dimple δ/t_eq and width.** The 015b width is λ = 1, which is 357 mm at R10 and 1292 mm at R30. Reis 2017 shows the knockdown depends on δ/t and λ = [12(1−ν²)]^¼ · √(R/t) · β0. Here t_eq = √3·h is used, so this transfer is unproven (N055-11).

**Face stress at collapse / face yield.** R10 0.871, R30 0.857. The design puts the face just under the 345 MPa proxy at operating, and classical buckling would need 2.03 / 2.95 times yield. CHECK-029: faces yield first, at 43–59 kPa on the 021 paths.

**Core shear / core shear strength.** CHECK-029 C029-11: the CR III W typical strength is passed far below operating at the specified dimples. Recomputed for 028b: 24.9 kPa at 16 mm and 37.8 kPa at 9.3 mm. Any test core must have the same strength and modulus, so it must be the same product.

**Core law and cell scale.**
- R10 has 4.0 cells per 38 mm wrinkle wavelength (cell/h 0.40). R30 has 13.6 cells per 129 mm (cell/h 0.09).
- CHECK-029 C029-10: the homogenized core (in-plane E 0.01 MPa) loses ellipticity at 0.088 MPa shear, so the dimple-flank response is cell-scale. Only the real honeycomb reproduces it.

**Wrinkling margin.** Binding in the line (wrinkle coefficient 0.4346, SF 1). The 0.82-form margin is 2.77 at R10. It needs coupons (038 T3) if the article suppresses it.

**Seams.** The 0.61 × 1.83 m blanks span 0.94–2.83 √(R·t_eq) at R10, so seams fall inside the buckle. The article must carry the route's seams.

**Boundary.** Reis's clamped hemispheres buckle like spheres. A cap is valid only if its edge is far enough from the dimple; see the FE below.

### The smallest scale that preserves them

**Same-material homothety** (038's rule: R, faces, core, cells, bonds and defects scaled together) preserves every group and the collapse pressure. Two stock limits break it:
- SR-200 sheet comes only from 0.508 mm (Materion), so a beryllium article needs a scale of at least 0.64, R 6.4 m.
- The 3/8 in. 1.0 pcf cell cannot shrink. Hexcel's lightest hex cores are 1/4 in. 1.6, 3/16 in. 2.0 and 1/8 in. 3.1 pcf. A smaller cell is a denser, stiffer, stronger core, which would hide the core-shear failure that governs.

**So the core groups survive only at full core thickness.** The smallest article that keeps them is a full-cross-section cap on the true R 10 m curvature.

**Cap size, from my FE** (028b section, 16 mm dimple):

| cap diameter | limit vs full sphere | core-shear onset vs sphere |
|---|---:|---:|
| 3 m | −10.0% | −2.7% |
| 4 m | −3.6% | −2.2% |
| 5 m | +1.4% | −0.4% |
| 6 m | +0.8% | +0.2% |

- **Choose 5 m:** about 20 m² and 18 panels per face, with cap parameter Λ = 7.1.
- **The clamped edge needs reinforcement.** It yields the inner face and crushes the core at about 60 kPa (N055-05).

**Stand-in faces.** Each candidate is matched to beryllium's E·t/√(1−ν²) with h held. Ratio = operating face stress / yield, relative to beryllium's 0.871.

| material | thickness (mm) | ratio | verdict |
|---|---:|---:|---|
| 5052-O | 3.10 | 0.99 | the only metal tried that keeps the yield interaction |
| 5052-H32 | 3.10 | 0.46 | does not keep it |
| 6061-T6 | 3.17 | 0.31 | does not keep it |
| 2024-T3 | 2.98 | 0.27 | does not keep it |
| 7075-T6 | 3.04 | 0.18 | does not keep it |
| CP-Ti grade 2 | 2.05 | 0.49 | does not keep it |
| Ti-6Al-4V | 1.91 | 0.16 | does not keep it |
| CFRP quasi-isotropic | 4.01 | 0.14 | elastic knockdown only; linear to brittle failure |

**How faithful 5052-O is, in my FE.**
- The elastic gamma is reproduced within +2.8% at 16 mm and +3.7% at 9.3 mm, and the core-shear onset within +2.6%. The face yields at 0.88 of beryllium's pressure, which is conservative.
- **Not reproduced:** biaxial membrane stiffness is 31% higher (ν 0.33 against 0.0752); wrinkling is suppressed (margin × 4.0); beryllium's low-ductility fracture is absent (N055-03).

**R30.** Its true section needs a cap about 15 m across, which is impractical. A 1/3-scale section on the same R 10 m mould (0.82 mm Be faces on a 34.2 mm core, or 3.21 mm 5052-O on 31.8 mm) keeps R/h, Vc, δ/t_eq and the stresses. The cell stays at 9.5 mm (4.5 cells per wavelength), and it needs a 6 m cap: 2.5 m radius reads −2.2%, 3 m reads +1.2% (N055-06).

## 2. Articles and rigs

**A. Model shells (038 T7).**
- *Article:* R 0.5 m, 1 m in diameter. Aluminium foil faces about 40 µm; foam core 1.16 mm, chosen for G about 11.8 MPa.
- *Rig:* sea-level evacuation. The design-equivalent pressure is 24 kPa, and gamma 1 is 42.5 kPa.
- *Instrumentation:* DIC, a laser scan and pressure-volume.
- *Cost:* USD 30–90k for three (038).
- *Limits:* it keeps the geometry groups only. It has no face-yield match, no core strength or law, and no seams. Use it to calibrate the elastic FE.

**B. Full-section stand-in caps (recommended).**
- *Article:* 5 m in diameter on R 10 m. Faces 3.10 mm 5052-O, from panels on the mould or spun gores (spinning shops reach 2.5–3.5 m; the MJC SPC-270.500 takes a 6.8 m blank).
- *Core:* CR III 3/8-1.0, 20.9 mm, fitted to each face's measured contour (042's method).
- *Bond:* cured at 200 F under heat blankets and a vacuum bag. Scarf seams follow the route.
- *Edge:* reinforced with face doublers and a potted core ring.
- *Shape target:* as-built waviness at most 0.075–0.129 mm (042). One stress-free seeded Gaussian dimple per article: 2, 6 and 16 mm over 0.357 m.
- *Rig:* a steel ring base sealing a vacuum cavity under the cap, with a water tank above it. Sea-level evacuation reaches gamma 0.593; adding 2 m of water reaches 0.709, 5 m reaches 0.883 and 10 m reaches 1.17 (rig reach in RESULTS.json).
- *Instrumentation:*
  - stereo DIC on the inner face from cameras in the cavity, rented or through a partner;
  - photogrammetry or a laser tracker scan before and after (0.1–0.3 mm);
  - back-to-back face gauges on the dimple flank at r 250–450 mm;
  - acoustic emission for core shear and disbond;
  - pole LVDT, water level and pressure.
- *Cost:* USD 0.42–1.56M for three. Once-only items are 0.21–0.69M (mould 40–150k, rig 80–250k, instruments 60–185k, pre-test FE 30–100k). Each article is 0.07–0.29M (materials 5–46k, 300–700 h labor 45–175k, metrology 5–20k, test 15–50k).

**C. SR-200 confirmation cap, one article after B.**
- About 59 kg of beryllium, at 038's USD 10–50k/kg planning range.
- About USD 1–4.6M with beryllium forming and handling.

**D. R30-similar caps, two articles on B's mould and rig.** About USD 0.15–0.61M.

## 3. Outcome table

Measured gamma is reported against the seeded amplitude, together with the first failure mode.

| measured gamma | R10 (needs 0.564) | R30 (needs 0.37–0.42 ISA) | meaning |
|---|---|---|---|
| below 0.21 | fails | fails | worse than the S-II record; reject the route or the section |
| 0.21–0.25 | fails | fails | confirms the record (035, CHECK-035); P2 rests on optimism at both radii |
| 0.25–0.37 | fails | fails | better than the record, still short of 040's least R30 set |
| 0.37–0.42 | fails | some ISA rows (0.373–0.418 by pad and floor) | R30 becomes the P2 path |
| 0.42–0.53 | fails | ISA clears; optimistic-weather rows need 0.459–0.530 | R30 with margin |
| 0.53–0.564 | just fails | every 040 row | R10 needs a little more |
| 0.564–0.593 | clears at SF 1 | clears | the most sea-level evacuation alone can show is 0.593 |
| 0.593 and above | clears with margin | clears | needs the water head |

**Two qualifiers attach to every row.**
- **Failure mode.** If the first failure is core shear on the dimple flank, face yield or fracture, wrinkling, or a seam, the value is a capacity of that mode, not a global gamma. Per N055-02 that is the expected first mode at 042's amplitudes.
- **Amplitude.** P2 is cleared only by gamma at the amplitude the full-scale route can hold.

**How many articles.**
- Three per configuration (seeded at 2, 6 and 16 mm) discriminate between the models. That is 038's view too.
- A statistical lower bound needs far more. Using 90/95 normal tolerance factors (k = 6.16 at n = 3, 3.41 at n = 5, 2.36 at n = 10): three articles at 5% scatter need a mean of 0.815 to bound 0.564, and at 10% scatter no mean will do. Ten articles at 10% scatter need 0.738.
- **So a result counts under a validated-analysis rule:**
  - at least three articles per configuration;
  - measured as-built shapes;
  - the failure mode identified;
  - an elastic-plastic, cell-aware FE that predicts each article within 10%.
- NASA's SBKF used 8 subscale and 2 full-scale cylinders this way (N055-08).

## 4. The answer, restated

**Cheapest test that moves gamma to evidence:** option B, three 5 m stand-in caps.

**Cost:** about USD 0.4–1.6M. Add 0.15–0.61M for the R30-similar pair, and 1–4.6M for a beryllium confirmation cap afterwards.

**To decide or buy first:**
1. The section(s) to test: 028b for R10, and the R30-similar section.
2. The dimple specification. 047 is not filed, and my FE needs much tighter shape than 042's map tolerance of 9.3–16.1 mm: the elastic gamma 0.564 needs ≤ 5.8 mm, the core strength ≤ 2.4 mm and the faces ≤ 1.3 mm.
3. 038 T1 SR-200 compression.
4. CR III 3/8-1.0 shear and crush witnesses, about USD 5–15k.
5. A pre-test FE with a sourced in-plane core law and face plasticity.
6. The vacuum-plus-water rig and its safety case.

**Evidence base:**
- My FE is the CHECK-029 axisymmetric StVK model. It is elastic, so plasticity and core failure would lower these gammas (N055-12).
- All 16 + 7 runs are in runs/. The arithmetic is in scale055.py, and the run definitions are in batch055a.sh and batch055b.sh.
- Under the COMMON brief, simjob refusals are retried unchanged; none occurred in this card's runs.

**Files:**
- RESULTS.json
- NFI.json (N055-01 to N055-12)
- INPUTS.json, with the pinned inputs and the web sources
