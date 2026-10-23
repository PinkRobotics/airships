# MAINLINE-037b: the bond's stress-free temperature and a CTE-matched core (rpt-ref-d6eac96dde8db1968e86)

Order: ord-admiral-rr2-mainline037b-dispatch-1019, from admiral-robotics-review-v2. Brief: CARD-037b-BOND-TEMPERATURE.md with COMMON.md.

Files: `.ship/work/outputs/vacuum-mainline037b-bond-temperature-1020/`.

Sourcing files: `.ship/work/sources/037b/{adhesive,core,interlayer}.{json,md}`. Three sourcing sub-workers of this seat wrote them: 81, 116 and 51 rows, each with a URL, a location and a quote.

## Re-run (in the outputs directory, with TMPDIR=unpublished-local-ref:1ffe4110219d37c0 and OPENBLAS_NUM_THREADS=1)

1. `python3 run37b.py` writes COMPUTE.json in about 2 minutes. It needs 017b's `model17b.py`, imported by path. It asserts its pins, 10 reproduction checks and every sourced value.
2. `python3 card37b.py` writes CARD.md, RESULTS.json, NFI.json and INPUTS.json.

## Basis

These choices are deliberate:
- **Both readings are reported.** One is 037's rigid shear-lag screen, reproduced exactly. The other is this seat's free-edge model.
- **Strength:** typical and minimum-average, W and L, from CR-III Table II.
- **028b replica:** usage, gamma and Q from 017b's model17b P2 modes, reproducing 028b's least set to 2e-6.
- **Cure compression:** K_biax d_eps tc/(2 tf) on each face, added to the face-local modes: yield, wrinkling, dimpling and the scarf. It is not added to global buckling or crimping, because it is balanced inside the wall. That is this seat's argument (NFI).
- **Projections:**
  - Room-temperature and mid-swing cures are priced at AF's areal weight.
  - Non-metallic in-plane expansion is a proxy.
  - Metal cores are mass bounds, with every other core property perfect.

## Results

**The 037 screen cannot hold.** At the 250 F cure it reads 1063 kPa, factor 0.227. But it would need the core to carry 47 times its wall-yield force; even 037's swing needs 12 times.

**The bond:**
- In the field it carries no mismatch shear.
- The walls carry 102 MPa on a uniform cell (factor 2.24) and 122 MPa in the doubled cell's single walls (factor 1.87).
- A free core edge reads 1.17 typical and 0.83 minimum. W governs; L reads 1.23 / 1.01.

**The faces carry the larger cost.** Cure compression is 4.4 MPa at 028b's lead. Through 028b's fixed 30:1 scarf it takes usage from 0.972 to 1.052. At 037's point the scarf falls from 1.0064 to 0.9925; any bond stress-free above 54 C does this.

**Lightest sourced fix, +0.12 kg:**
- the 200 F datasheet cure, which gives a free edge 1.51 / 1.08;
- a 30.34:1 scarf, which brings usage back to 0.972.

**Other cures and fixes:**
- Room-temperature and mid-swing cures read 0.990 and 0.982, on projections.
- Matched cores and RTV interlayers cannot float.

## Deferred and open

There are 13 NFI rows. The weightiest are:
- the screen premise;
- the free-edge model;
- the balanced-compression argument;
- the projected 10 MPa scarf screen;
- 028b's fixed 30:1 scarf as an untaken lever (30.44:1 alone reads 0.894);
- splice fill.

Carbon UCF-145 (12.8 kg/m3) is not priced: it has no in-plane expansion and its W strength is 97 kPa.

## Next

The brief says stop and file. The robotics seat sends the next job.
