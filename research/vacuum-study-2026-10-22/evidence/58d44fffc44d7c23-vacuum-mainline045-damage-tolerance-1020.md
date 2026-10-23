# MAINLINE-045: damage tolerance (rpt-ref-57c98dcce7960aca042a)

Order: ord-admiral-rr2-mainline045-dispatch-1019, from admiral-robotics-review-v2. Brief: CARD-045-DAMAGE-TOLERANCE.md with COMMON.md.

Files: `.ship/work/outputs/vacuum-mainline045-damage-tolerance-1020/`.

Sourcing files: `.ship/work/sources/045/{threats,sandwich,p3damage,leak}.{json,md}`. Four sourcing sub-workers of this seat wrote them: 92, 136, 107 and 53 rows, each with a URL, a location and a quote.

## Re-run (in the outputs directory, with TMPDIR=unpublished-local-ref:1ffe4110219d37c0 and OPENBLAS_NUM_THREADS=1)

1. `python3 det45.py` writes DET.json in about 25 s. It covers both lead points (10 checks), 015's map at P2, the face patch, the frame with one member lost, the merged bay, holes and descent, and the valve.
2. `python3 run45.py` writes COMPUTE.json in about 3.5 minutes. It covers threats, P2's dents and growth, P3's tubes and film, and the pricing. It asserts every sourced value.
3. `python3 card45.py` writes CARD.md, RESULTS.json, NFI.json and INPUTS.json.

The run imports three things by path:
- 037b's bond37b.py, the 028b replica;
- 017b's model17b.py;
- this card's p3_022d.py, 022d re-implemented from its METHOD.

## Basis

These choices are deliberate:
- **015's map:** narrower dimples are taken no worse than lambda 1, and no lower than the plateau at their width.
- **The dent-growth criterion is this seat's** (NFI). The face's fixed pR/4 acts on the dent's curvature, against crush less the core's pressure share, with the patch's plate buckling taken off. The edge is read clamped and simply supported.
- **Dent model:**
  - face membrane plus core crush over a plastic spread;
  - checked against Pach's test and Clarke's FE (depth from about the same to half the FE);
  - hail read three ways: fluid rho v^2, Shi-calibrated 2.16 rho v^2, and all energy.
- **Tube hail:** a shallow shell on its own foundation, with the Hexoloy tube Weibull data (C-ring 299/4.6, sectored 192/5.5).
- **Frame loss:** a linear rigid-joint frame on f4/f5 geodesics.
- **Descent:** a rigid sphere in ISA, an isothermal fill, Cd 0.6 hole, drag 0.2-0.47.

## Results

**Neither lead is damage tolerant on its own budget.**

**P2:**
- Dents never lower gamma; they are narrow (lambda under 0.63).
- But a crushed zone over 55 mm (clamped) or 27 mm (simply supported) grows under the face's 238.7 kN/m once deeper than about 0.2-1.5 mm. That is at BVID.
- The design 50.8 mm hail crushes about 81 mm and grows (Shi-calibrated and all-energy readings).
- Mooring contact at 0.914 m/s crushes through.
- The mass margin is 14.6 kg. A face, core or shield fix breaks the float.
- Operating fix: vent to 46 percent of the difference (about 2646 kg of air) before hail.

**P3:**
- The design hail breaks a tube with probability 1.1-5.3 percent a strike.
- One lost member multiplies the peak stress 2.4-3.3 times, so the frame cascades.
- The merged-bay film goes to SF 0.84.
- A puncture runs at 1.38 GPa (critical half-length 0.007-1.9 mm).
- A torn bay lands the hull at 23-35 m/s.
- A tear-stopping film reads SF 0.88-0.98, and 1.5 mm walls read 0.80.

**Puncture:**
- A slow leak lowers the hull gently. At neutral buoyancy the difference is M R T/V, and the descent adds 1.1 percent (ISA).
- Touchdown reaches 0.914 m/s at a 63-66 mm hole.
- The landing valve is 70-200 mm.
- Internal pressure finds a 0.36 mm hole in an hour.

## Deferred and open

There are 16 NFI rows. The weightiest are:
- the growth criterion;
- the patch edge;
- the dent model;
- beryllium impact;
- hail flux;
- the Zylon film;
- the cascade's linearity;
- the 152.4 m moored-balloon limit.

## Next

The brief says stop and file. The robotics seat sends the next job.
