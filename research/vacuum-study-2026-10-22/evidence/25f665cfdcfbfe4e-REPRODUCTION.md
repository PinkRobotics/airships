# REVIEW-A2 reproduction

Only this review's scripts execute. They read pinned JSON, NPZ and CSV
inputs and do not import any predecessor code.

From this directory, route each command through the host's simjob tool
with one CPU and 1 GiB memory:

```text
python3 independent_review.py
python3 independent_review.py canonical
python3 independent_thermal.py
```

The first command generates the 061 arithmetic and 058 pressure/edge
checks. Its height-zero weather file is explicitly diagnostic.
The second command generates the authoritative weather recount with
station height 25.29+2 m and a local station-pressure humidity correction.
The third generates the authoritative mixed-convection thermal roots.
Use a fresh copy of the package when reproducing it so sealed evidence
files are not overwritten.

Expected selected checks:

- All eight final weather cases exactly match the owner's original hour
  and day counts before the added-hardware sensitivity.
- Complete weather denominator: 87,354 hours and 3,559 full UTC days.
- Largest density-factor disagreement: less than 2.72e-8.
- R12 ISA P2 TRL7 payload: +4.615730 kg.
- Four cold-edge temperature disagreements: less than 0.00345 K.
- R30 ISA P3 irreducible payload upper bound: −3,681.927506 kg;
  even with the entire stated tube-relief fraction free: −329.452553 kg.

`VERIFICATION.json` records the package and arithmetic checks actually
performed. It does not certify the inherited mechanical, material or
weather-operation models.
