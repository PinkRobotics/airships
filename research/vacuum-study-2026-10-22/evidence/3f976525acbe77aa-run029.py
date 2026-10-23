#!/usr/bin/env python3
"""Driver for CHECK MAINLINE-029 runs on the own axisymmetric model (axi029). One case per call; writes a JSON record.

usage: run029.py OUT.json CASE [key=value ...]
CASE: eucass-flat, eucass-dimple, lead021, lead021b, transfer40, eucass-sens
keys: dir=W|L amp=<mm> width=<mm> nth=<n> grading=<g> nface=<n> ncore=<n> nu=<face nu> mode=linear|arc pref=<MPa>
      dl=<arc length> steps=<n> follower=1|0 widthnu=0.3|0.33
"""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from axi029 import Model  # noqa: E402

STEEL = ("iso", 210000.0, 0.33)
FOAM = ("iso", 40.0, 0.0)
CORE_EN, CORE_GW, CORE_GL = 103.42135939752539, 46.88434959354485, 103.4213593975254
LEAD = {"lead021": (0.8434480441930918, 20.21337638749162), "lead021b": (0.691748, 30.118231)}


def build(case, kv):
    nth = int(kv.get("nth", 192))
    g = float(kv.get("grading", 1.0))
    nf = int(kv.get("nface", 2)); nc = int(kv.get("ncore", 6))
    amp = float(kv.get("amp", 0.0))
    if case.startswith("eucass"):
        ti = 0.42 if case == "eucass-flat" else 0.40
        Ro = float(kv.get("Ro", 42.8))                      # the paper's 42.80 mm read as the outer radius unless overridden
        steel = ("iso", float(kv.get("Esteel", 210000.0)), 0.33)
        foam = ("iso", float(kv.get("Efoam", 40.0)), float(kv.get("nufoam", 0.0)))
        width = float(kv.get("width", 4.28))
        m = Model(Ro, [{"t": ti, "n": nf, "mat": steel}, {"t": 3.1, "n": nc, "mat": foam}, {"t": 0.42, "n": nf, "mat": steel}],
                  math.pi / 2, nth, grading=g, dimple=(amp, width) if amp > 0 else None, clamp_equator=True)
        return m, {"R_outer": Ro, "ti": ti, "width": width}
    if case == "transfer40":
        Rmid = 124.0; tc = 3.1; tf = 0.42
        Ro = Rmid + (tc + 2 * tf) / 2
        width = float(kv.get("width", 0.1 * Ro))
        m = Model(Ro, [{"t": tf, "n": nf, "mat": STEEL}, {"t": tc, "n": nc, "mat": FOAM}, {"t": tf, "n": nf, "mat": STEEL}],
                  math.pi / 2, nth, grading=g, dimple=(amp, width) if amp > 0 else None, clamp_equator=True)
        return m, {"R_outer": Ro, "width": width}
    tf, tc = LEAD[case]
    Ro = 10000.0
    nu = float(kv.get("nu", 0.33))
    G = CORE_GW if kv.get("dir", "W") == "W" else CORE_GL
    teq = math.sqrt(3) * (tc + tf)
    wnu = float(kv.get("widthnu", 0.3))
    width = float(kv.get("width", math.sqrt(Ro * teq) / (12 * (1 - wnu ** 2)) ** 0.25))
    face = ("iso", 290000.0, nu)
    core = ("core", CORE_EN, G, float(kv.get("ein", 0.01)), float(kv.get("gin", 0.005)))
    m = Model(Ro, [{"t": tf, "n": nf, "mat": face}, {"t": tc, "n": nc, "mat": core}, {"t": tf, "n": nf, "mat": face}],
              math.pi, nth, grading=g, dimple=(amp, width) if amp > 0 else None, fix_south_inner_z=True)
    return m, {"R_outer": Ro, "tf": tf, "tc": tc, "width": width, "teq": teq, "G": G, "nu": nu}


def main():
    out = sys.argv[1]; case = sys.argv[2]
    kv = dict(a.split("=", 1) for a in sys.argv[3:])
    t0 = time.time()
    m, info = build(case, kv)
    rec = {"case": case, "args": kv, "info": info, "dof": int(m.ndof), "elements": int(m.ne)}
    if kv.get("mode", "arc") == "linear":
        vd, _, _ = m.linear_buckling(nev=4)
        vf, _, _ = m.linear_buckling(nev=4, load_stiffness=True)
        rec.update({"dead_MPa": vd[:4].tolist(), "follower_MPa": vf[:4].tolist()})
    else:
        pref = float(kv.get("pref", 1.0))
        m.grow = float(kv.get("grow", 1.2))
        m.probe = 2 * m.nid[0, 2 * m.nt] + 1              # outer north-pole axial displacement recorded on the path
        dl0 = float(kv.get("dl", 1.0))
        res = m.arc_length(pref, dl0, int(kv.get("steps", 400)), tol=float(kv.get("tol", 1e-8)),
                           dl_max=float(kv.get("dlmax", 3 * dl0)), dl_min=dl0 / 1e4,
                           follower=kv.get("follower", "1") == "1", verbose=kv.get("verbose", "0") == "1",
                           stop_after_limit_drop=float(kv.get("drop", 0.15)))
        rec.update({"p_peak_MPa": res["p_peak"], "lam_end": res["lam_end"],
                    "path": [(float(a), float(b) if b == b else None, int(c) if c == c else None) for a, b, c in res["hist"]]})
        # pole inward displacement at the peak (outer surface, north pole) and face stress diagnostic
        npole = m.nid[0, 2 * m.nt]
        rec["pole_outer_dz_at_peak_mm"] = float(res["u_peak"][2 * npole + 1])
        vm, where = m.face_von_mises(res["u_peak"], [m.nt - k - 1 for k in range(int(kv.get("nface", 2)))])
        rec["outer_face_max_vonmises_MPa"] = vm; rec["where"] = where
    rec["elapsed_s"] = time.time() - t0
    json.dump(rec, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k != "path"}))


if __name__ == "__main__":
    main()
