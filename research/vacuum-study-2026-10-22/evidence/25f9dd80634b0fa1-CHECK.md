# MAINLINE-005b check

Unit vacuum-mainline005b-check-1019. Checker ref-cca93dbfd236dcaa3a8b. Owner card rpt-ref-9dd3721f6f2e5595ab9a. Arithmetic is check005b.py. The owner's script was not run.

## What was re-derived

sigma_core = p/2. p is the pinned MAINLINE-001 pressure 95460.83791390515 Pa. Required strength is 47730.41895695257 Pa on P2, P2-A, P2-C, P2-K and P2-E. The model has no thickness, so the five rows match. Margin is stated strength divided by that requirement. Catalog strengths are sourced inputs. This check recomputes the margins and the p/2 line. It does not re-measure the datasheets.

## Result

7 comparisons against RESULTS.json, worst relative difference 1.524e-16. Displayed margins match: 1.05, 11.6, 22, 13, 23, 2.1, and 47730.4 Pa. 25 kPa is below the requirement and 70 kPa is above it. Honeycomb and PMI entries at or above 20.8 kg/m3 all exceed a margin of 10. The smallest of those is 11.565. Pins in COMMON.md: 12 of 12. The four owner files match the hashes on the owner report. The header tags sourced values QUESTIONABLE. The microlattice is PROJECTION and has no strength. 007 filed 2026-10-19T22:54:28-07:00. This card filed 2026-10-19T22:37:56-07:00. NFI-005B-007 matches the brief.

## Mismatches

Row: lowest density on the 1% definition. Field: about 18-22 kg/m3. Card value: 18-22. The only 1% point in the table is 25 kPa at 14.4 kg/m3. Scaling that point linearly in density reaches 47730 Pa at 27.49 kg/m3. Scaling with the square of density reaches it at 19.90 kg/m3. The card states no exponent. NFI-CHECK-005B-1PCT.

Row: PMI foam, Rohacell range. Field: RESULTS.json. Card value: 52-110 kg/m3, 0.8-3.6 MPa, margin 17-75, source Evonik Rohacell RIST-HT via Knowde. My value: no RESULTS entry and no URL. The margin arithmetic on 0.8 MPa and 3.6 MPa is 16.76 and 75.42, which display as 17 and 75. NFI-CHECK-005B-RANGE.

Row: owner report body. Field: "from 20 kg/m3 up by ten times or more". Report value: sourced real cores clear by ten times. My value: Pyrogel XTF at 200 kg/m3 has margin 2.137. The card sentence that limits the claim to honeycomb and PMI does hold.

These do not stop the card. Crush on this model is still not what binds the P2 rows.

## Not taken

Datasheet pages were not re-fetched. MAINLINE-007 rows were not computed. The brief told the owner to take them once 007 had filed, and 007 filed later.
