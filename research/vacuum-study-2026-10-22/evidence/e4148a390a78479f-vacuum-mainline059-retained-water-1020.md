# MAINLINE-059: the water on the hull (rpt-ref-4fb99766fa9a4406a85a)

Order: ord-admiral-rr2-mainline059-dispatch-1019, from admiral-robotics-review-v2. Brief: CARD-059-RETAINED-WATER.md (68b3e5bd) with COMMON.md (6a6a596f).

Files: `.ship/work/outputs/vacuum-mainline059-retained-water-1020/`.

Sources: `.ship/work/sources/059/{retention,dew,drying,shedding}.{json,md}`, with 30, 29, 17 and 36 rows. Four sourcing sub-workers of this seat wrote them, each row quote-verified.

## Re-run

Work in the outputs folder. The heavy step goes through simjob with `./simretry.sh`.
1. `python3 ponds59.py` writes PONDS.json in about 15 s. It holds P3's bay ponds: 024's sag and 052's bay size, with 200 placements of the top point.
2. `python3 dry59.py` writes DRY.json in about 3 s. It holds the evaporation and dew energy balance, with two convection bounds.
3. `python3 retain59.py` writes RETAIN.json. It holds the films and drops by finish and position, calibrated on the acrylic plate.
4. `./simretry.sh LOG 8 4G env OPENBLAS_NUM_THREADS=1 python3 cap59.py` writes CAP.json in about 30 s. It holds P2's capacity from 049's model49 on 048's cure-included account.
5. `python3 water59.py` writes WATER.json. It asserts every sourced value.
6. `python3 card59.py` writes CARD.md, RESULTS.json, NFI.json and INPUTS.json.

## Basis

These choices are deliberate:
- **Drop retention:** Furmidge with each finish's angles. kappa is calibrated so the measured acrylic plate (78/48 deg) gives its 54 g/m2. Rain carries a x1.48 upper reading from the PVC rain-gauge estimate.
- **Hydrophilic finishes:** a Jeffreys draining film after rain and a Nusselt condensate film under dew.
- **Cap:** 0.8 kg/m2, the horizontal-leaf dew limit.
- **Lower hemisphere:** no rain credited below 135 deg.
- **P3 dish shape:** quadratic, with 024's crown 0.0426 s and mean 0.5036 crown. The bay side comes from 052's sag debit (R cubed).
- **P3 film:** paint-like (base) and FEP-like (upper).
- **Drying convection:** bracketed between 040's sphere correlation and a flat-plate h = 5.7 + 3.8 U.
- **Shedding costs:** topcoat mass from a 13-25 um film at 1.0-1.5 g/cm3 (PROJECTION); shelter cost from one inflatable-hangar price per floor area.

## Result

**P2: keep 0.1 kg/m2.**
- After rain it holds 0.014-0.051 kg/m2 (upper reading 0.021-0.076).
- After dew it holds 0.011-0.056 kg/m2.
- Its capacity is 0.1945 kg/m2 at R10 ISA and 1.127 at R30.
- At 1 mm of water it floats only at R30 ISA (G+Q+film 0.917).
- The cheapest way to hold the allowance is waiting: drained in 10 min, dry in 0.2-1.0 h at a fair midday.

**P3: ponds.**
- At R10 they hold 37 kg on average, ranging 5-171 kg (node on top 55, bay on top 171). They scale as R cubed.
- With a bay on top, R10 sinks: 210 kg of water against a 157 kg capacity.
- The cheapest way is to orient the frame with a node or the best placement on top, and tilt it past 14 deg after rain. A night shelter (about 4.9M RUB, floor-scaled) is the fallback.
- Waiting takes 65-465 h.

**Grounding:** weigh a full-scale panel and a sagged bay on a tilting load-cell rig after rain and dew.

## Deferred and open

There are 12 NFI rows. The weightiest are:
- the retention calibration (one plate each for condensation and rain);
- the paint's and P3 finish's wettability;
- the pond geometry and orientation;
- the drying convection bracket;
- topcoat optics;
- the shelter's height and cost;
- rain met in flight;
- wet optics.

## Next

The brief says stop and file. The robotics seat sends the next job.
