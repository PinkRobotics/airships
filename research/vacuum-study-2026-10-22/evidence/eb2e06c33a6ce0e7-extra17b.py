#!/usr/bin/env python3
"""MAINLINE-017b extras: the SiC design compressive strength each P3 single-property route needs, and today's
values across the CR-III 5056 family (Hexcel Table II, typical). Writes EXTRA.json."""
import json
import math
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import model17b as m  # noqa: E402
import scan17b as sc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "COMPUTE.json")))
out = {"p3_strength_needed_MPa": {}, "criii_family": {}}
for prop in ("film_specific_strength", "sic_density", "sic_modulus", "lattice_knockdown"):
    f = C["p3"]["today"]["alone"][prop]["factor"]
    lo, hi = 1e-3, 1.0
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        if sc.p3_best("today", {prop: f, "sic_strength": mid})["least"] >= 0.999:
            hi = mid
        else:
            lo = mid
    out["p3_strength_needed_MPa"][prop] = {"factor": f, "strength_MPa": hi * 3900.0,
                                           "rule": "lowest strength keeping the re-optimised least SF at 0.999"}
KSI, PSI, PCF = 6.894757293168e6, 6894.757293168, 16.018463373960138
ROWS = {"5056 3/8-1.0": (1.0, 15, 6.8, 35, 0.009525, 60), "5056 1/4-1.6": (1.6, 30, 10.5, 50, 0.00635, 110),
        "5056 3/8-1.6": (1.6, 30, 10.5, 50, 0.009525, 110), "5056 1/4-2.3": (2.3, 58, 15.0, 100, 0.00635, 265)}
for name, (pcf, ec, gw, crush, cell, fc) in ROWS.items():
    out["criii_family"][name] = {}
    for R in (10.0, 20.0):
        q = m.p2_apply(m.P2_TODAY, {})
        q.update({"rho_c": pcf * PCF, "Ec": ec * KSI, "Gc": gw * KSI, "crush": crush * PSI, "cell": cell,
                  "Fc_flatwise": fc * PSI})
        r = m.p2_optimise(R, q, "019")
        out["criii_family"][name][f"R{int(R)}"] = {k: r[k] for k in ("least", "governing", "tf", "tc")}
tmp = os.path.join(HERE, "EXTRA.json.tmp")
with open(tmp, "w") as fh:
    json.dump(out, fh, indent=1)
os.replace(tmp, os.path.join(HERE, "EXTRA.json"))
print(json.dumps(out, indent=1)[:1500])
