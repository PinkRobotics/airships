# MAINLINE-039: the stiffened sandwich sphere. Does a rib grid or a frame buy back gamma?

- **Seat:** ref-55cff924be25afe6f9dd (Opus), 2026-10-20.
- **Order:** ord-admiral-rr2-mainline039-dispatch-1019. Brief CARD-039-STIFFENED-SANDWICH.md with COMMON.md, both pinned in INPUTS.json.
- **Status:** Every value is QUESTIONABLE and every transfer is a PROJECTION. Nothing here is a certification.
- **Method:** My own arithmetic is in `.ship/work/scripts/check039.py`, and `build039.py` compacts it.

## The answer

1. **On today's record, no.**
   - Stiffening does not buy back gamma at 019's reserve.
   - With 028b's seam screen held, no stiffened version reaches SF 1 under any set of the named optimisms, even at their full endpoints. 028b's own two-factor set does: gamma ×2.82 and Q ×1.32.
2. **At 028b's own two values, every stiffened version falls short.** With gamma 0.564164 and Q 0.434628, each needs 90-258 kg of extra lift, where the plain sandwich needs none (2 kg on the grid). That is 88-257 kg out of 019's reserve or the payload.
3. **The record gives no general credit for stiffening a dome.**
   - The handbook allows 0.425 only for a dome as heavily stiffened as one 1964 aluminium test article.
   - SP-8032 gives stiffened domes the isotropic cap curve: 0.14 at a complete sphere.
   - In the one program that tested both kinds, stiffened domes kept less of their classical load than monocoque caps.
4. **What stiffening can do is move the gamma problem into mass and into a cheaper test.**
   - Take a frame stiff enough to make the 2 m bays act as clamped caps: Be tubes, 0.6-0.8 t, with stiffener ratio γ_s ≥ 10.
   - It raises today's least SF from 0.528 to 0.689.
   - It cuts the mass short of SF 1 at today's record from 2.80 t to 1.33 t.
   - Its claim, a bay knockdown of about 0.6 at λ_p 2.6, can be measured on one bay.
   - It does not float, and every step of it is a PROJECTION.

## Baseline reproduced

- **028b's nominal AF/scarf point reproduces exactly.** Faces 0.794624 mm SR-200 (ν 0.0752, 028b's headline), core 23.2372 mm CR-III 5056 3/8-1.0:
  - Vc 0.953214.
  - Needed gamma 0.564164 and needed Q 0.434628.
  - Crimp 2.441308, dimpling 6.758508, crush 5.055822.
  - Face 1.148724 at 345 MPa.
  - Scarf screen 1.000 at 300.333 MPa.
  - Joining 215.742 kg, from my own implementation of 028b's formula.
- **028b's least sets reproduce on my grid.** {gamma, Q} at usage 0.9726 with the seam screen (028b: 0.971978), and 0.6577 in six modes (028b: 0.657494).
- **The plain sandwich's best least SF today at 019's reserve is 0.528.** That point is faces 0.731 mm and core 37.4 mm, where global and wrinkling balance. 028b's own point scores 0.355 today at ν 0.0752 (0.368 at ν 0.33).

## The stiffened-shell record

Each row is cited. I read the rows marked "read here" at source myself; the others come from the sub-worker's LIT-STIFF.json.

| Source | What was tested or recommended | Knockdown against classical |
| --- | --- | --- |
| [CR-62257](https://ntrs.nasa.gov/api/citations/19650012174/downloads/19650012174.pdf), Meyer and Bellinfante 1964 (read here) | Monocoque PVC caps, clamped, R 20 in | C 0.48-0.50 against 0.6125: **0.78-0.82** |
| same | Geodesic rib-stiffened PVC caps 1-G and 2-G (psi 9.1, 10.1) | C 0.348 and 0.377: **0.57 and 0.62** |
| same | Redesign 3-G (psi 22.2) | 3.96 psi tested against 4.03 psi predicted at C 0.4: about **0.64** |
| same | Aluminium geodesic cap, R 27.3 in, 60 degrees (psi 28.0) | C 0.26 (c_o 0.52 against 1.225): **0.42**, with plasticity suspected |
| [Isogrid Design Handbook, NASA CR-124075 Rev A](https://ntrs.nasa.gov/api/citations/19730011184/downloads/19730011184.pdf), p.4.1.012 (read here) | Design value for heavily stiffened domes, from that one aluminium test. Lightly stiffened domes use Reference 2-8, which is SP-8032 | **gamma 0.425** |
| [NASA SP-8032](https://everyspec.com/NASA/NASA-SP-PUBS/download.php?spec=NASA_SP-8032.046171.pdf), printed p24 (read here) | Stiffened and orthotropic domes "in the absence of more extensive test results" | The isotropic cap curve 0.14 + 3.2/λ², so **0.14** at a complete sphere |
| Ossola et al., J. Spacecraft and Rockets 2021, DOI 10.2514/1.A34823 | AM Ti-6Al-4V isogrid hemispheres, R 100 mm | 0.44 (plain 0.33); the authors say failure was not clearly buckling |
| NASA/SP-8007-2020 | Stiffened cylinders | 0.65 design (0.75 in 1968) |
| SBKF TA01 (NASA/TP-2015-218785), TA02 (NASA/TP-2017-219587), ETTA2 | Orthogrid Al-Li cylinders, axial (TA02 also bending; ETTA2 internal pressure) | 0.948, 0.984 and 0.82 of classical. These are cylinders, not domes |
| 035, as corrected by CHECK-035 | Saturn S-II sandwich hemispheres | about 0.21-0.22 |
| 035 (Pineda 2014, reproduced by CHECK-035 E13) | Curved sandwich fairing panels | eigenvalue 2.85-23.80% above test, so 0.808-0.972 |

psi is the ratio of composite bending stiffness to the skin's own bending stiffness. I computed it from the CR-62257 design values in check039.py.

**Reading.**
- **The stiffened domes gained strength per weight, not knockdown.** They were 1.5-2.27 times the same-weight monocoque, through a larger effective thickness.
- **Handbook credit is narrow.** The only handbook figure above 0.20 for a stiffened dome is 0.425, and it applies only at psi of about 28 or more.
- **No framed sphere was found.** The opened sources hold no test of a discretely framed or ring-stiffened sphere. DTMB 2302 (a stiffened HY-150 hemisphere) was not opened, because DTIC returned 403.

## The concepts (all at 019's reserve with 028's joining, on 021b's Be faces and CR-III 5056 core)

- **C1: isogrid ribs on the inner face**, at a = 0.5, 1.0 and 2.04 m.
  - Ribs are SR-200 tees: a blade b × d on a 25 × 0.5 mm foot, under one AF 0.015 lb/ft² bond line, plus 5% of rib mass for splices and nodes.
  - The search ran the blade aspect from 3 to 20, so crippling (k 0.43) is scored.
- **C2: sandwich panels on 026's frame**, at s = 2.04 m.
  - SiC tubes: Hexoloy-SA, E 410 GPa, 3100 kg/m³, 3.9 GPa typical, with the local coefficient 0.6 × SP-8007 gamma (FIX-B).
  - They sit tangent under the skin seams, on a 30 mm AF land with two 5 mm paste fillets.
  - Fittings are 026's 0.02 kg nodes, plus 023's Ti sleeves (157.7 kg at 562.2 kN) scaled by member force.
- **C2b: the same frame in Be tubes**, CTE-matched to the faces.
- **026's frame as sized will not fit.** Its members alone are 4,567 kg (r_o 123.7 mm, wall 0.880 mm). That leaves no room for any skin under the 4,889 kg lift, so the frame is re-sized here.

## How each mode is scored

- **Global.**
  - Model: smeared triangulated lattice (ν 1/3) in two groups, the outer face and the inner face plus lattice, joined by a shear-flexible core. N(k) is minimised over wavelengths of at least 2a.
  - With no lattice it gives the line's Kc = 1-Vc/4 exactly.
  - Knockdown today is 0.20 (CR-1457), or 0.425 when psi ≥ 28.0 (the IDH test dome).
  - The full endpoint is the 018 curve, or for heavily stiffened designs 0.616 (CR-62257 2-G) for ribs and 0.702 (026) for frames.
- **Bays, with an adequate lattice.** Adequate means γ_s = EI_e/(a·D_skin) ≥ 10, an assumption (NFI N039-01).
  - The bay load is the larger of the skin's own sphere load and the simply supported equilateral-triangle plate, corrected for core shear.
  - Bays with λ_p ≤ 2 take the panel record: 0.808 today, 0.972 full.
  - Larger bays hold the skin's own dimple and take the sphere record, 0.20.
  - Under the named optimism O5, larger bays instead take SP-8032's clamped-cap curve, capped at 0.808.
- **Bays, with an inadequate lattice.** If the skin's dimple fits between the lines (λ_p > 1.165), the skin buckles alone at 0.20. Otherwise the lattice bends with it and only the global mode counts.
- **Faces:** compression at 345 MPa (379.2 MPa full), wrinkling (Q 0.33 or 0.82, biaxial b), crimp, dimpling, and the 028 seam screen at 300.333 MPa. The face stress includes the bay bending that carries the lattice's pressure share to the lines.
- **Core:** crush, both uniform and concentrated at the lattice lines, and W-direction shear at the lines.
- **Lattice:** rib crippling and rib yield; tube local buckling; SiC compression.
- **Thermal:** SiC on Be over 019's 25.1 K swing.
- **Separation:** rib-skin separation is not driven in the membrane state. The bond carries 0.16-0.21 MPa compression. Peel is NFI.

## Results

### Least SF today at 019's reserve (seam screen held)

| Concept | Least SF (mode) | Lattice kg | Faces / core mm | Notes |
| --- | --- | --- | --- | --- |
| Plain sandwich | 0.528 (global) | 0 | 0.731 / 37.4 | |
| C1 ribs, a 0.5 m | 0.586 (bay plate) | 2,229 | 0.363 / 6.7 | psi 29.8 earns IDH's 0.425. Face 0.75 (461 MPa), seam 0.65, rib-line core shear 0.65, crippling 0.68 (blade 2.5 × 50 mm) |
| C1 ribs, a 1.0 m | 0.539 (global) | 1,798 | 0.445 / 10.4 | psi 16.4. Face 0.74, seam 0.64, core shear 0.67, crippling 0.73 |
| C1 ribs, a 2.04 m | 0.517 (wrinkle) | 62 | 0.718 / 37.1 | No better than plain |
| C2 SiC frame | 0.512 (bay) | 20 | 0.713 / 36.8 | Any useful frame scores lower; the bays dimple as the sphere does |
| C2b Be frame | 0.512 (bay) | 20 | 0.713 / 36.8 | Same |
| C2 with O5 (frame-bay caps) | 0.619 (bay) | 828 | 0.634 / 14.9 | r/t 300 tubes: tube local 0.65, face 0.85, seam 0.74 |
| **C2b with O5** | **0.689 (wrinkle)** | **626** | 0.674 / 15.8 | Be tubes r_o 87 mm, wall 0.29 mm, γ_s 10.4. Bays λ_p 2.63 at cap 0.603 give bay 0.71; global 1.12; face 0.93; seam 0.81; tube local 0.78 |

With the adequacy threshold at γ_s ≥ 5, C2b with O5 reaches 0.733 on 465 kg and C2 with O5 reaches 0.664.

### Least named optimism set to SF 1 at 019's reserve

| Concept | Seam screen held (028b's route) | Six modes, seam dropped |
| --- | --- | --- |
| Plain sandwich | {gamma ×2.823, Q ×1.316}, usage 0.973 | {gamma ×1.967, Q ×1.819}, usage 0.658 |
| C1 0.5 / 1.0 m | none within the full endpoints | {gamma ×2.05-2.06, Q ×1.87-1.97}, usage 0.743 / 0.722 |
| C1 2.04 m, C2, C2b | none | {gamma_g ×1.16-1.17, gamma_p ×2.0, Q ×1.85-1.87}, usage 0.680-0.702 |

- **The seam screen is the blocker.** Stiffening takes mass from the faces, and the face stress rises past 300.3 MPa.
- **Without the seam, stiffening still loses.** Every stiffened least set has a higher usage than the plain one, and those designs carry only 20-225 kg of lattice.
- **O5 is never in a least set.** The adequate frames it needs cost too much.

### Mass to SF 1: extra lift needed (negative would be reserve or payload to spare)

| Concept | Today's record | Today with O5 | At 028b's gamma 0.564164 and Q 0.434628 |
| --- | --- | --- | --- |
| Plain sandwich | +2,797 kg | | +2 kg (grid; 0 at 028b's point) |
| C1 ribs 0.5 / 1.0 / 2.04 m | +3,030 / **+2,423** / +3,002 kg | same | +258 / +96 / +90 kg |
| C2 SiC frame | +2,957 kg | +1,810 kg | +134 kg |
| C2b Be frame | +2,691 kg | **+1,330 kg** | +133 kg |

- **Adequacy sensitivity.** With γ_s ≥ 5: C2b needs +2,235 kg today and +1,137 kg with O5, and C1 at 1.0 m needs +2,233 kg.
- **Designs at those points.**
  - C1 at 1.0 m today: 2,212 kg of ribs, faces 0.831 mm, core 19.5 mm.
  - C2b today with O5: 830 kg of Be tubes, faces 0.911 mm, core 16.8 mm.

## Does stiffening trade gamma for mass?

- **Against 028b's two optimistic values, it does not.** Every rib grid or frame is 88-257 kg of reserve or payload worse than the plain sandwich carrying the same gamma and Q claims (ribs 88-257 kg, frames 131-132 kg).
- **Against today's record, it trades gamma for mass in a useful direction.**
  - Ribs at 1 m cut the mass short of SF 1 by 374 kg (2,797 to 2,423 kg).
  - An adequate Be frame cuts it by 106 kg.
  - Read as frame-bay caps (O5), the Be frame cuts it by 1,467 kg (to 1,330 kg). The frame converts the bays' knockdown from the sphere's 0.20 to the clamped-cap curve's 0.57-0.60.
- **None of these floats.**

## Is what it needs cheaper to ground?

- **Yes, for the frame-bay route, but grounding it does not float the hull.**
  - 028b needs gamma 0.564 on a 20 m sandwich sphere at Vc 0.95. Nothing has been measured between Vc 0.9 and 2, and the S-II domes reached about 0.21-0.22 (035 and CHECK-035).
  - The frame-bay route needs two things, both measurable at subscale:
    - frame adequacy (γ_s ≥ 10), by FE of frame plus bays and a frame-bay test;
    - the bay knockdown at λ_p of about 2.6, on one 2.04 m bay or a subscale bay at matched λ_p and γ_s.
  - 026's frame knockdown is not what this needs. The frame's own long-wave mode is not critical (1.12 at 0.20). 026's 0.70-0.79 also comes from t_eq of about 320 mm, and no frame that heavy fits under a skin.
- **Even fully grounded, it would still need more.** The O5 Be frame would still be 1.33 t short at today's record, and it still needs Q, the seam screen and thin-wall tubes (r/t 300) to move.

## Limits

These are in NFI.json, rows N039-01 to N039-16.
- Frame adequacy is assumed.
- The SP-8032 cap-curve transfer to sandwich bays is untested.
- The record's one heavily stiffened metal dome is a single aluminium test, with plasticity suspected.
- Stiffener one-sidedness is not modelled.
- Transfer bending is taken as a simply supported bound; it adds 45 MPa at the C2b O5 point.
- SiC-on-Be thermal mismatch is included only for the climate swing. A hot cure would add about 7.3e-4 strain per 100 K.
- The thin walls at r/t 300 are untested.
- The rib material and the core at the lattice lines are not settled.
- Lattice joining is a projection.
- The seam screen decides feasibility.
- The smeared lattice idealises the geodesic.
- The bays' core-shear correction is untested.

## Files

All files are in this directory. Pins and sha256 are in INPUTS.json and in the report.
- `RESULTS.json`: compact results, including measured times.
- `RUNS.json` and `RUNS-gs5.json`: full runs.
- `NFI.json`, `INPUTS.json`, `LIT-STIFF.json`.
- `run-full.log` and `run-gs5.log`.
- Scripts: `.ship/work/scripts/check039.py` and `build039.py`.
