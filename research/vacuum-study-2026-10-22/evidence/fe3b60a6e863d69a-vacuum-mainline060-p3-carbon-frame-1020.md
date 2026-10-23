# MAINLINE-060: the carbon-framed P3 (rpt-ref-93808d41af02a0580060)

Order: ord-admiral-rr2-060-untimed-1020, from admiral-robotics-review-v2. It replaced ord-admiral-rr2-mainline060-dispatch-1019 only to drop the 07:00 deadline; the board's 07:00 stall casualty was acknowledged and closed by ack-ref-9432c207fefd50edf0d4. Brief: CARD-060-P3-CARBON-FRAME.md (6429c526) with COMMON.md (6a6a596f).

Files: `.ship/work/outputs/vacuum-mainline060-p3-carbon-frame-1020/`.

Sources: `.ship/work/sources/060/{compression,joints,impact}.{json,md}`, with 45, 14 and 42 rows. Three sourcing sub-workers of this seat wrote them, each row quote-verified.

## Re-run

Work in the outputs folder. Each step is light: under a tenth of a second on one core, so simjob was not needed.
1. `python3 carbon60.py` writes CARBON.json. It holds the nine constructions, the whole bill and the compression needed to float.
2. `python3 extra60.py` writes EXTRA.json. It holds joints, Pf at every sizing, and hail.
3. `python3 card60.py` writes CARD.md, RESULTS.json, NFI.json and INPUTS.json. It asserts the checks.

## Basis

These choices are deliberate:
- **Witnesses:** 051's 019-reserve witnesses, because 052 resizes that family. The 5%-reserve witness is 1.3% heavier.
- **Tubes:** 052's stiffness-sized SiC tubes x (051 carbon witness / 041 reference witness) x the wall factor. The tubes replace SiC on 052's endpoint and baseline rows.
- **Compression:**
  - The laminate value is the data-sheet UD strength / 051's 0 deg ply ratio (first-ply failure).
  - m = 1.2/CV, with CV 5.2% and 6%.
  - 051's k(m) is interpolated in log m.
  - Size scaling runs from a 0.32 cm3 gauge to one tube. Its wall factor is f = x^(m/(m-1)), because the volume grows with the wall.
- **Cavity:** 054's increment over ground. One day is MET; seven days are SiOx plus 3A. R 20-30 are extrapolated.
- **Joints:** 052's SiC bill is kept. Boeing 44K (16.9%) and space-strut (70%) fitting shares are sensitivities.
- **Hail:** the design strike is 051's (50.8 mm, 32.0 m/s). It is compared with the sourced ice thresholds on flat panels. 051's quasi-static stress is extended as a power of the wall.

## Result

**No carbon frame floats on sourced compression.**
- K13D2U 50/20/20/10 gives 0.19 GPa, 11.4 times below 2.16 GPa.
- At mean strength the best is M55J 50/20/20/10: -470 kg at R10 and -4,624 kg at R30.
- At Pf 1e-3 the best is M55J 70/10/10/10: -2,044 kg at R10 and -47,116 kg at R30.

**The light pitch layup floats only if its compression is ignored.** It gives +619 kg at R10 and +24,765 kg at R30.
- It needs a 0.59 GPa laminate mean, or UD 1.06 GPa.
- For Pf 1e-3 it needs UD 1.94 GPa, or 3.07 GPa size-scaled.
- With Boeing-share fittings it floats only from R12.

**Hail:** about 32 J, 7.3-7.9 times below flat-panel ice delamination.

**Not a better lead than SiC.**

**Grounding test:** about 30 full-length tubes with fittings, compressed to failure.

## Checks that are not circular

- Lift is exactly 4.88944 R^3 and matches 054's lift column within 0.5 g.
- 054's increments equal its barrier change plus its capture hardware within 0.5 g.
- All Pf-sized walls recompute to 1e-3.

## Deferred and open

There are 12 NFI rows:
- tube compression;
- scatter;
- size scaling;
- wall scaling;
- first-ply failure;
- joints (775 kN per tube, 1.43 times the largest sourced strut test);
- film;
- moisture in the cavity;
- cavity extrapolation;
- hail;
- T700S;
- unexplored layups.

## Next

The brief says stop and file. The robotics seat sends the next job.
