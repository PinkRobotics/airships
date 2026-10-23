# CHECK-047: MAINLINE-047 behind its owner (rpt-ref-a18ff970381ef39185d1)

Order: ord-admiral-rr2-check047-opus-65d1-1020, from admiral-robotics-review-v2. Brief: CHECK.md (03b357cb) with COMMON.md (6a6a596f).

Checked report: rpt-ref-e23aa05d834f8e89bb2c. Owner: codex ref-4bc9297546b34b47e7f1. CARD.md: ad003407.

The owner's code was neither read nor run. Its filed JSON/CSV/MD were read as data.

Files: `.ship/work/outputs/vacuum-mainline047-check-1020/`.

## Re-run

Work in the outputs folder.
1. `python3 chk047a.py` writes A-ARITH.json: the arithmetic, sources and simple-shear ellipticity. It takes about 2 min on one core.
2. FE solves go through simjob.
   - `python3 runall.py` runs 25 solves; `runall2.py` (core law) and `runall3.py` (face E) run 2 each.
   - Each solve is ccx on 4 cores via `./simretry.sh`, and takes 0.4-5.2 min.
   - Runs sit in `fe/<name>/` with result.json and a gzipped .dat.
3. `python3 chk047b.py` writes B-FE.json.
4. B-ACOUSTIC.json holds the exact acoustic minima. It was computed inline, from chk047a's functions on the runs' worst-shear strains.
5. `python3 card047.py` writes CHECK.md, RESULTS.json, NFI.json, INPUTS.json and FE-RUNS.json.

## Own model (fe047.py)

- **Mesh:** full-sphere CAX8. Own graded mesh: 4 mm out to 1.3 m, growth 1.06, 60 mm beyond. That is 857 angular elements, 2+6+2 layers, 8570 elements.
- **Core:** a cylindrical orientation about the global z axis gives the sphere's radial, meridian and hoop axes; core engineering constants with NLGEOM are StVK.
- **Faces:** *PLASTIC with NLGEOM. A 10,000 MPa yield traces the pre-yield branch, as the owner does.
- **Gotcha:** CalculiX reads at most 20 characters a field. A 21-character pressure became 100-1000 times the load. Keep numbers to 12 significant digits.
- **Endpoint:** the last converged increment, from .sta. Skip U attempts and use column 6, the step time.

## Result

- **Arithmetic:** 72/72 rows agree.
- **FE:** 43/44 rows agree.
  - Governing SF 1: own 344.646/345.358 MPa at 1.208988/1.226988 mm (card 344.597/345.309); estimate 1.2179 mm (card 1.2192).
  - SF 1.05: estimate 0.7469 mm (card 0.7478).
  - Perfect sphere: within 0.004 kPa.
  - 1.10 endpoints: within 0.004 kPa.
- **Core law:** inherited law ellipticity loss at 0.0877 MPa; regularized at 2.65 MPa. At the governing state, the exact minimum is +0.498 (regularized) and -0.005444 (inherited).
- **Regularization:** at most 0.004 mm.
- **Mismatch:** the 11.8 mm larger-dimple face-yield estimate is 61.910 on the card and 63.596 kPa on the check. The cause is the owner's coarse sweep mesh; it is a diagnostic only.
- **NFI:** C047-01 is the sweep mesh, which is unstated. C047-02 is E = 290 GPa, which is unsourced; 298.7 GPa adds 0.015 mm.

## Next

The brief says stop and file. The robotics seat sends the next job.
