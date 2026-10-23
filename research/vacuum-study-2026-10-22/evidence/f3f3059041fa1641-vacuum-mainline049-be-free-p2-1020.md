# MAINLINE-049: the beryllium-free P2 (rpt-ref-06643b916584f58fd9e4)

Orders, all from admiral-robotics-review-v2:
- ord-admiral-rr2-mainline049-dispatch-1019, with brief CARD-049-BE-FREE-P2.md and COMMON.md;
- three folds: -fold-048-1020 (048's finish and water), -fold-chk040-1020 (CHECK-040's rows) and -simjob-retry-standing-1020 (heavy runs through simjob; a refusal is a wait).

COMMON.md was amended twice after dispatch, at 05:12 and 05:45. Removing exactly the two added simjob lines gives back the dispatched sha256 8f359d6c. run49 and fold49 assert this before computing, so a further amendment stops them until it has been read.

Files: `.ship/work/outputs/vacuum-mainline049-be-free-p2-1020/`.

Sources: `.ship/work/sources/049/{cfrp,albemet,cores,water}.{json,md}`, with 121, 87, 124 and 27 rows. Four sourcing sub-workers of this seat wrote them, each row with a URL, a location and a verified quote.

## Re-run

Work in the outputs folder. Heavy runs go through simjob via `./simretry.sh LOG CORES MEM COMMAND...`, which retries an exit-75 refusal unchanged, at least 60 s apart.
1. `./simretry.sh LOG 1 2G env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run49.py` writes COMPUTE.json in about 12 min. This is 040's coating and water. It asserts 040's 12 rows.
2. Run sens49.py and extra49.py the same way. Each writes its JSON in about 2 min, reading COMPUTE.json.
3. `./simretry.sh LOG 8 4G env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 fold49.py` writes FOLD.json in about 8 min. This is 048's account, CHECK-040's rows, E multipliers, edge against cure and the thermal factors. It asserts 048's 8 rows bit for bit, CHECK-040's 28 rows within 1e-3 kg and the thermal tables exactly.
4. `python3 card49.py` writes CARD.md, RESULTS.json, NFI.json and INPUTS.json. It reads the simjob logs in unpublished-local-ref:4bb9307620c9822f for the scope record.

The model is 040's model.py, generalised in model49.py. 040's own files are copied into base040/ unchanged.

## Basis

These choices are deliberate:
- **Primary account (048's):** multilayer CCAg/ITO at 8.33 g/m² installed, alpha 0.09 and epsilon 0.80, solved into each core's thermal table with 048's larger-of-day-and-night gradient and curvature. It adds 10 g/m² primer and keeps the 0.1 kg/m² exterior film aboard. Material water is charged and 90% removed by the bake. Classical CCAg and the dry-gas route are rows.
- **Material water fractions:**
  - CFRP faces 0.18%, the P75S/954-3 pitch/cyanate laminate at 55% RH;
  - HRH-10 4.4% (Hexcel pickup); HRH-49 3.4% (HRH-36 as proxy);
  - CFRP seam film 1.67% (FM-300);
  - 048's values for 5056, AF163-2U, primer and finish.
  - The aramid cores' nominal-volatile allowance is set back to 040's 0.001 so their water is not counted twice.
- **Face strength:** K13D2U compression is 014b's 220 MPa. The full value is Fc/(1-nu), an equal-biaxial reading (PROJECTION).
- **The 60% Vf projection:** E1 = 935 GPa x 338/540 = 585 GPa. Quasi-isotropic 200 GPa.
- **Bonds:** a room-temperature or 50 C bond for CFRP on 5056 (PROJECTION). AF163-2U at 200 F elsewhere.
- **Finish screen:** 048's legacy factors at 037's source geometry, with each face's E and mismatch. A full-cycle factor at the construction's own endpoint geometry is added.

## Results

All values are all-four endpoints, ISA, actual joining, under 048's account, unless stated.

**No sourced beryllium-free P2 floats anywhere:**

| Build | Shortfall at R 15 / 20 / 30 | Note |
|---|---|---|
| K13D2U on 5056, room-temperature bond | -1.0 / -1.9 / -4.8 t | needs x1.12 / 1.09 / 1.07 modulus |
| AlBeMet | -1.7 / -3.4 / -10.0 t | 62% beryllium |
| M55J | -2.9 / -6.3 / -19.5 t | |

- **Aramid cores:** crimp-bound. With no drying credit their water breaks the service pressure (factor 0.51-0.60).
- **CFRP on 5056 at 200 F:** the free edge fails (0.55). A bond stress-free at or below 50 C is needed (1.02 at 50 C).

**The K13D2U 60% Vf projection floats everywhere on gamma, Q and the face tuple:**
- R 30 ISA usage 0.721, with gamma x1.95, Q x1.93 and 293 MPa.
- Endpoints +1.6 / +4.3 / +16.3 t.

**Beryllium floats everywhere on gamma and Q:** usage 0.721 / 0.596 / 0.532; endpoints +1.1 / +3.1 / +12.0 t.

**CHECK-040's rows:**
- At 1 mm of water only R 30 floats: beryllium on gamma, Q and film (0.907); the projection at 0.897.
- Cure in global costs the floating builds 0.02-0.45 t.
- Edge/scarf costs beryllium 0.2-1.4 t and the CFRP nothing.
- No float is lost.

**Finish screen:** the 60% Vf face fails full cycle at 037's geometry (0.890) and passes at its own (1.18).

**Supply at R 30:** 67.6 t of fibre, 4.8% of pitch capacity, against 103.8 t of beryllium, 24% of world output.

**Easier to ground: beryllium's optimisms.** They are fewer and smaller, on a sourced face. The CFRP's case is supply.

## Deferred and open

There are 17 NFI rows. The weightiest are:
- K13D2U compression and the biaxial reading;
- the 60% Vf modulus;
- the cold bond;
- the finish on CFRP;
- the water-uptake transfers;
- CHECK-040's rigid-face alternatives, which were not rerun for the beryllium-free faces.

## Next

The brief says stop and file. The robotics seat sends the next job.
