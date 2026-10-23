# CHECK-047: MAINLINE-047, the P2 dimple tolerance with face yield and core shear, checked behind its owner. ESTIMATE

Unit vacuum-mainline047-check-1020. Order ord-admiral-rr2-check047-opus-65d1-1020. Checked report rpt-ref-e23aa05d834f8e89bb2c: owner ref-4bc9297546b34b47e7f1, CARD.md sha256 ad003407. Brief CHECK.md (03b357cb) with COMMON.md (6a6a596f). The owner's code was neither read nor run; its filed data files were read as data. Values are QUESTIONABLE, and PROJECTION where named. Started 07:31:39 PDT when the order was read; the end time is in RESULTS.json. Times are measurements, not limits.

## Verdict

Every number the order names re-derives. 72 of 72 arithmetic rows agree. The check's own CalculiX model agrees on 43 of 44 compared FE rows. The one FE mismatch is a diagnostic in the larger-dimple table and is explained by mesh. Two objections become NFI rows: an unsourced face modulus and an unstated sweep mesh. Neither changes the card's conclusions; the modulus would move the SF 1 tolerance by about one bracket width.

**Scope of the check's own FE:**
- the perfect sphere: three first yields and three endpoints;
- the governing W 332 brackets at both SF, on the pre-yield branch and at a real 345 MPa;
- the L 332 and W 401.9 SF 1 brackets, and both cure-debit brackets;
- the 1.10-division pair and one larger dimple (332.2 mm W, 11.8 mm);
- three sensitivities: mesh, core regularization and face modulus.

The other footprints at SF 1.05, the 347.2 and 2181.4 mm widths and the other larger dimples are re-derived from the owner's filed data only.

- **Criterion.** min(endpoint, first face yield, first core shear) >= SF x 95.46083791 kPa.
  - 95.46083791 kPa is ISA at 500 m, to 1.5e-08. The SF 1.05 target 100.23387981 kPa follows.
  - Every tested boundary straddles 345 MPa with the core index below 1 and the converged path past the target.
- **Perfect-sphere first yield, own membrane statics.** The two faces carry the hemisphere load at 300.707 MPa at service. That puts first yield at 80.95, 95.24 and 109.52 kPa for 255, 300 and 345 MPa. All three lie inside the card's brackets.
- **Perfect-sphere first yield, own FE.** 80.977 / 95.283 / 109.594 kPa, against the card's 80.974 / 95.280 / 109.590.
- **Perfect-sphere endpoints, own FE.** 81.042 / 95.364 / 109.684 kPa, against the card's 81.044 / 95.363 / 109.682.
- **345 MPa brackets.** The check's own model, a different and finer mesh, gives the same pass/fail at every tested pair:
  - **SF 1:** 1.208988 / 1.226988 mm carry 344.646 / 345.358 MPa (card 344.597 / 345.309).
  - **SF 1.05:** 0.737936 / 0.755936 mm carry 344.619 / 345.380 MPa (card 344.585 / 345.345).
  - **Estimates:** 1.2179 and 0.7469 mm, against the card's 1.2192 and 0.7478.
  - **At a real 345 MPa:** own runs yield exactly where the card's native confirmations do.
  - **Other pairs:** L 332, W 401.9 and both cure-debit pairs also reproduce (estimates within 0.0017 mm).
  - **Mesh:** own refinement adds +0.11 MPa, about 0.003 mm.
- **Core law and admissibility.** The Hexcel CR III Table II values are verified from the pinned PDF.
  - **Simple shear, own exact minimisation:** the inherited 0.01/0.005 MPa law loses ellipticity at 0.0877 MPa (CHECK-029: 0.088). The regularized 1/0.5 MPa law holds until 2.65 MPa.
  - **Regularized law at the governing passing state:** the exact acoustic minimum is +0.498 MPa. The card's sufficient bound, 0.314 MPa over all passing states, is a valid lower bound.
  - **Inherited law at the same state:** -0.005444 MPa (card's probe -0.005455).
  - **The regularization does not drive the answer:** moving the in-plane law from 0.01 to 10 MPa moves the governing face stress +0.016 to -0.148 MPa, at most 0.004 mm.
- **Endpoint division and transfer.** Own endpoints at the limiting 401.9 mm/W pair are 105.0765 / 104.9167 kPa (card 105.0759 / 104.9204).
  - Dividing by 1.10 gives the same 0.521-0.539 mm bracket.
  - The perfect sphere's endpoint / 1.10 is 99.71 kPa, below 100.23, so SF 1.05 fails even at zero amplitude.
  - 2.3146-2.4589 are CHECK-029's recorded factors. 109.68 / 2.3146 = 47.4 kPa, so no amplitude is admissible.

## Mismatches, exactly

| Where | Field | Card | Check | Note |
|---|---|---:|---:|---|
| Larger dimples, 332.2 mm / W, 11.8 mm | first face yield estimate, kPa | 61.910 | 63.596 | Inside the card's native bracket 61.2-64.8. The card's sweep runs appear to use its coarse family: their native RSS, about 108 MB, matches its 256/1/4 perfect-sphere runs, against 328 MB for the 512/2/6 boundary runs. The check uses a 4 mm mesh. The check's own two-point extrapolation from 60 and 61 kPa gives 63.69, so the estimator is not the cause. It is a diagnostic: that row is governed by core shear at 22.651 kPa (check 22.720), and its endpoint agrees (68.629 / 68.609). |
| Geometry | core thickness, mm | 23.23721790601544 | 23.23721790601548 | 037b's record; 15th digit |
| Service pressure | kPa | 95.46083791390515 | 95.46083934 | ISA 500 m with the US 1976 constants; 8th digit |

Nothing else differs, across 72 arithmetic rows and 44 compared FE rows (A-ARITH.json, B-FE.json).

## Sources, tags and formulas

- **Verified against pinned documents:**
  - Hexcel CR III Table II, 5056 3/8 1.0 pcf: shear W 25/35 psi and L 45/55 psi (minimum average / typical); moduli 6.8 / 15 ksi; compressive modulus 15 ksi; crush 35 psi.
  - NASA CR-194164 Table 2: nu 0.0768.
  - NASA 19660014454 p.25: 0.050 in after trimming, and 0.150-0.200 in after chemical milling.
  - NASA 19730016169 p.86: 0.003 in to the die.
  - 036: the 345 MPa basis is a tensile minimum, with compressive yield blank.
- **Traced to source reports:**
  - 037b: geometry, scarf 30.3414 and residual 3.41022257 MPa.
  - 029: widths and moduli.
  - 042: 9.32-16.06 mm.
  - 015b: 0.1393 / 0.6544 mm, at 015b's own widths.
  - CHECK-029: 0.088 MPa and 2.3146-2.4589.
- **Unsourced:** E = 290 GPa has no source in 047. The cited Table 2 gives 298.7 GPa (L) and 293.6 GPa (LT). At 298.7 GPa the governing face stress falls 0.57 MPa, and the SF 1 tolerance rises to 1.2326 mm (+0.0147 mm), about one bracket width. NFI-C047-02.
- **Tags:** the card carries QUESTIONABLE / PROJECTION, and all 14 NFI rows are tagged.
- **Bookkeeping:** 319 native runs, 1892 checks (all passed), 92 core records, 7913.98 s elapsed, 24053.62 CPU-s and 626.5 MiB peak all re-derive.
- **Formulas confirmed:**
  - the Gaussian offset;
  - the classical lengths: 347.1529189, 347.1845439 with face bending, and 2181.424825 full wave;
  - the exact full-sphere RMS, with the small-patch form 4.6e-5 high;
  - the quadratic interaction: the index exceeds the meridian ratio by an implied 0.0021 MPa hoop shear;
  - the Cholesky current-frame shear: the check's implementation reproduces the card's core shears to 0.0001 MPa;
  - the sufficient acoustic bound: the check derives it as a valid lower bound.

## The check's own model

fe047.py builds it from the card's and METHOD.md's stated definitions alone:
- **Geometry:** full sphere; every layer offset inward by a exp[-(R theta / w)^2], stress-free.
- **Mesh:** CAX8 elements. Own angular mesh: 4 mm out to 1300 mm, growth 1.06, 60 mm beyond. That is 857 angular elements and 2+6+2 layers: 8570 elements and 27445 nodes.
- **Restraints:** the axis radially, and one south-pole node axially.
- **Faces:** E 290 GPa, nu 0.0768, *PLASTIC with NLGEOM. 10,000 MPa traces the pre-yield branch, as the card does.
- **Core:** StVK engineering constants on a cylindrical orientation about the out-of-plane axis, which gives the sphere's radial, meridian and hoop axes. W puts 6.8 ksi on the radial-meridian pair.
- **Load:** a follower pressure in steps that end exactly at the service and SF 1.05 targets. Endpoints are the last converged increment.

- **Runs:** 31 solves ran serially through simjob on 4 cores, 0.4-5.2 min each. Twelve short single-core debug solves (seconds each) ran directly.
- **A setup error of the check's own:** CalculiX reads at most 20 characters a field, so pressures written with 16 digits were truncated, and the first trial ran at 100 times its load.
  - It was found from a 1,000-fold soft all-Be sphere and fixed to 12 digits.
  - The fix was verified against the membrane solution (0.0513 mm at 8 kPa) and a unit axisymmetric column before any compared run.
  - The check's first endpoint parser read the wrong .sta column. It was corrected and every endpoint re-parsed.

## Then

Stop and file. The robotics seat sends the next job. NFI.json carries the check's two rows.
