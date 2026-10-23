# MAINLINE-010 check

Unit vacuum-mainline010-check-1019. Checker ref-cca93dbfd236dcaa3a8b. Owner card rpt-ref-58b2bed18db2449100f2. Arithmetic is check010.py. The owner's script was not run.

## What was re-derived

ISA troposphere with the card's gas constant 287.05 J/(kg·K), T0 288.15 K, p0 101325 Pa, lapse 0.0065 K/m, and ISO g0 9.80665 m/s². The rules string names the first four and not g0. Sandwich buckling kd·4·tf·separation·E/(R²·sqrt(1−ν²)), yield 4·σ·tf/R, crush p_net/2, safety factor allowable/p_net. Mass is two faces plus core on the sphere area, joints 5 percent of that sandwich, systems 100 kg per sphere. Margin is (lift − mass)/lift. Internal gas at the same temperature scales net pressure and net lift by (1−f). A cluster holds total lift at the 10 m value and sets each radius to 10·n^(−1/3).

Thicknesses are the pinned rows: P2-A tf 0.0003758936444928841 m, core 0.1 m; P2-E tf 0.0003360949703945902 m, core 0.1134320525081742 m, separation 0.1137681474785688 m.

## Result

410 numeric leaves in RESULTS.json agree. Worst relative difference 8.915e-16. CARD.md displayed digits agree, including the intro baselines. Pins in COMMON.md: 12 of 12. The four owner files match the hashes on the owner report. Tag QUESTIONABLE.

500 m pressure computed here is 95460.77843546981 Pa. Pinned 001 pressure is 95460.83791390515 Pa. Difference 0.059 Pa, inside the card's 0.1 Pa claim. The difference is R = 287.05 against the pinned 287.053.

Systems-allowance spread is −0.143164 at 5 m, 0.017896 at 20 m, 0.020132 at 40 m. Altitude factor at 5000 m is 1.76715. Buckling ratio is exactly 9 at n = 27 and exactly 4 at 5 m. Both safety factors pass 1 only for the n = 27 cluster, both geometries. Mass there is 3.49082 times the lift. 007 filed 2026-10-19T22:54:28-07:00 and 008 filed 2026-10-19T22:42:59-07:00. This card filed 2026-10-19T22:42:05-07:00. NFI-010-007008 matches the brief's stop rule.

## Mismatch

Row: Lever 3 prose. Field: "the SF gain cancels to the last digit" after the structure is rescaled to restore the margin.

Card value: the gain returns to the baseline safety factors.

My value, faces and core scaled together, systems held at 100 kg, so the baseline margin ratio is restored. At internal fraction 0.50 the thickness scale is 0.4895603708256402.

- P2-E buckling SF becomes 0.1121104823613712. Baseline is 0.2338857247188333.
- P2-E yield SF becomes 0.3805768489706136. Baseline is 0.3886924592453974.

If systems scale with lift as well, yield returns exactly and buckling is multiplied by (1−f): P2-E buckling SF 0.1169428623594166 at f = 0.50.

The fixed-structure product SF(f)·(1−f) does equal the baseline, to the last digit. That product is not a rescaled structure. Buckling scales with the square of thickness, so it does not.

NFI-CHECK-010-RESCALE. No fraction raises either factor once the margin is restored, so the sentence "no internal fraction helps" still holds. The tables stand. This does not stop the card.

## Not taken

Lever 1 was not re-run on the 007 or 008 rows. The brief told the owner to stop and file, and both cards filed after this one. MAINLINE-005 and MAINLINE-008 were not rechecked.
