# CHECK-039 — stiffened sandwich

**REVISE. The filed design-point arithmetic reproduces. The claimed best mass and safety-factor values need a grid qualification, and several source interpretations need correction.**

Order: `ord-admiral-rr2-check039-codex-8497-1020`.
Checked report: `rpt-mainline039-opus-stiffened-sandwich-1020`.
Seat: `ref-4bc9297546b34b47e7f1`.
All material transfers and hull predictions remain QUESTIONABLE/PROJECTION.

I rebuilt the declared mechanics from dimensions and equations. No owner code was opened, imported or executed. Its script bytes were hashed only to verify the filed artifact pins. All 31 assignment/report/upstream pin checks pass.

## Arithmetic and coverage

There are **13,176 matching numerical field comparisons**: 5,392 across 60 full design records, 7,768 across mass-shift designs, compact sets and RESULTS presentations, and 16 nominal-028b checks. These include duplicated presentations and input dimensions; they are not 13,176 independent measurements. Tolerances are recorded in the checker. Four compact gs5 rows omit shape: their shape was recovered from the supplied psi, so those four psi values are inputs, not independent checks. This limitation is explicit in EXTENDED-ARITHMETIC.json.

The full endpoints, every filed set's needed values and usage, frame sections, joining masses, safety-factor vectors, nominal baseline and gs5 sensitivity reproduce. The exact negative statement that no seam-held stiffened solution exists is a **finite-search result**, not an independently established impossibility theorem.

| Concept | Filed least SF today, independently reproduced | With O5 | Filed extra mass today / O5, kg |
| --- | ---: | ---: | ---: |
| Plain | 0.528213 | — | 2797.195 / — |
| C1, a=0.5 m | 0.585608 | 0.585608 | 3029.831 / 3029.831 |
| C1, a=1.0 m | 0.538864 | 0.538864 | 2422.981 / 2422.981 |
| C1, a=2.04 m | 0.517394 | 0.517394 | 3002.033 / 3002.033 |
| C2, SiC | 0.511934 | 0.619356 | 2957.333 / 1810.310 |
| C2b, Be | 0.512146 | 0.689108 | 2691.292 / 1329.819 |

The nominal 028b geometry can be recovered without using its rounded thicknesses: impose the 300.333333 MPa scarf ceiling and mass equality. This gives gamma_needed=0.564163566603 and Q_needed=0.434627854375. SUPPLEMENTARY.json carries all intermediate values.

## A better point under the same assumptions

Independent continuous optimization of the same adequate, cap-like C2b branch converged from two different starting designs. Slightly perturbing into gamma_s>10 and re-evaluating the original thresholded model gives:

| Quantity | Original O5 point | New fixed-mass point | New SF≥1 point |
| --- | ---: | ---: | ---: |
| Total mass, kg | 4889.442150 | 4889.442150 | 6016.513503 |
| Extra mass, kg | 0 | 0 | **1127.071353** |
| Face thickness, mm | 0.673761 | 0.678208 | 0.879808 |
| Core thickness, mm | 15.806839 | 15.640425 | 17.128372 |
| Be frame, kg | 626.420370 | 609.562072 | 766.010583 |
| r/t | 300 | 300 | 300 |
| gamma_s | 10.400178 | 10.000025 | 10.000010 |
| Least SF | 0.689108 | **0.699691806** | **1.000001080** |

The third point reduces the filed 1329.818726 kg deficit by **202.747373 kg**. Its panel SF is 1.000002512; scarf 1.074625; tube local 1.015467; global 1.527433. Every scored factor is above one. These are constructive points, not a proof of a global optimum. They remain especially sensitive to the unvalidated adequacy threshold. Exact coordinates and all factors are in CONSTRUCTIVE-POINTS.json.

**No tested or certified floating hull follows.** The fixed-mass point remains below unity; the unity point still exceeds lift by 1127 kg.

## What changes in the conclusions

1. Keep 0.689108 and +1329.818726 kg as attained grid-point results. Replace a claim of best achievable performance with the better constructive points above and a stated search domain.
2. The source's 0.425 heavy-dome recommendation is real; **psi≥28 is the owner's extrapolated gate**, not a handbook threshold. gamma_s≥10 likewise has no demonstrated clamping calibration in the cited material. See SOURCE-CHECK.md and NFI C039-02.
3. The O5 cap factor at the filed lambda is **0.601013192**, not the card's approximate 0.603. Equal-area circular mapping, triangular boundary restraint and coupled modes still need evidence.
4. At fixed mass, the O5 point fails wrinkle, face, scarf, panel and tube-local screens. At the owner's **mass-added** +1329.819 kg point, Q=.33, the 10 MPa scarf and today's tube-local rule already pass: SF 1.059449, 1.109144 and 1.055118. The sentence requiring these to “move” conflates two operating points.
5. Correct the source-table plain-Ti ratio to 317/917=0.345692, retaining the paper's printed 33% as a source inconsistency. In the STA8.1 record, 759,000 lb is an intermediate model; 754,000 lb includes load nonuniformity. They are not conflicting estimates of the same model.

## Adequacy and load-path diagnostics

At the filed C2b O5 point, gamma_s=10.400178 is equivalent to psi=1+(3sqrt(3)/4)gamma_s=14.510227. The isolated tube's EI/(a D_skin) is only **3.196840**; the larger value includes composite participation. Neither number alone proves rotational clamping.

Mapping the same triangle to its circumscribed circle instead of its equal-area circle changes lambda from 2.634622 to 4.097154, the cap factor from 0.601013 to 0.330627, and panel SF from 0.710384 to 0.390794. This is a sensitivity example, not a replacement design rule.

The unrestricted smeared minimum has wavelength 3.427772 m; the global calculation excludes wavelengths below 4.08 m. Restoring that minimum changes the global factor from 1.118206 to 1.055069. A coupled discrete frame/bay analysis must cover the omitted wavelengths and eccentric coupling.

For SiC O5, tube compression includes the thermal envelope but the force used in line loading and sleeve scaling is mechanical: 55.521 kN versus 63.974 kN in the tube compression envelope. Resolve signed hot/cold compatibility before propagating this 8.454 kN difference. It does not affect the CTE-matched Be comparison.

## Deliverables and disposition

METHOD.md gives the independent equations. SOURCE-CHECK.md and SUPPLEMENTARY.json give source readings and source arithmetic. NFI.json contains actionable revisions; none stopped the check. ARITHMETIC.json, EXTENDED-ARITHMETIC.json and RECALCULATED.json retain the field-level audit. CONTINUOUS-CHECK.json and CONSTRUCTIVE-POINTS.json contain the numerical counterexamples. VALIDATION.json records checks and limits.

One completion report to sciences, cc co, xo and admiral-robotics-review-v2. No successor assignment or out-of-band seat contact.
