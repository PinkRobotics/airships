#!/usr/bin/env python3
"""EUCASS 2023-367 clamped sandwich hemisphere (029's stated geometry): linear buckling, dead and follower pressure."""
import json, math, sys, time
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from axi029 import Model
STEEL = ("iso", 210000.0, 0.33)
FOAM = ("iso", 40.0, 0.0)
out = []
for case, ti in (("flat", 0.42), ("dimple", 0.40)):
    for nth, nf, nc in ((96, 2, 6), (192, 2, 6), (384, 2, 6), (384, 3, 10)):
        t0 = time.time()
        m = Model(42.8, [{"t": ti, "n": nf, "mat": STEEL}, {"t": 3.1, "n": nc, "mat": FOAM}, {"t": 0.42, "n": nf, "mat": STEEL}],
                  math.pi / 2, nth, clamp_equator=True)
        vd, _, _ = m.linear_buckling(nev=4)
        vf, _, _ = m.linear_buckling(nev=4, load_stiffness=True)
        rec = {"case": case, "ntheta": nth, "nface": nf, "ncore": nc, "dof": m.ndof, "dead_MPa": vd[:3].tolist(),
               "follower_MPa": vf[:3].tolist(), "s": time.time() - t0}
        out.append(rec)
        print(json.dumps(rec), flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=1)
