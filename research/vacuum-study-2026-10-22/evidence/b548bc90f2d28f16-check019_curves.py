#!/usr/bin/env python3
"""MAINLINE-019 check, sensitivity: both families under MAINLINE-018's two continuous knockdown curves.

018 (rpt-ref-089ed1faaaf72118b83f): optimistic curve, PROJECTION, gamma = 0.20 + 0.40*min(Vc, 2);
conservative curve, gamma = 0.20 at every Vc (the crimp mode knocked down with it, as 018 re-scored). 019 keeps the
CR-1457 step rule (gamma = kd for Vc <= 2, 1 above). Also tries regular core-fraction grids against 014b's filed value.
Checker's own arithmetic (check019.py); QUESTIONABLE, not a certification.
"""
import json

import numpy as np

import check019 as c


def modes_curve(core, tf, tc, curve):
    md, Vc, Kc, gam = c.modes(core, tf, tc)
    md = dict(md)
    if curve == "optimistic":
        g = np.where(Vc > 2, 1.0, 0.2 + 0.4 * np.minimum(Vc, 2))
    else:
        g = np.full(np.shape(Vc), 0.2)
    md["global"] = md["global"] / gam * g
    if curve == "conservative":
        md["crimp"] = md["crimp"] * 0.2
    return md, Vc, g


def main():
    out = {"curves": {}, "grid_014b": {}}
    for line, M in (("0%", 0.0), ("5%", 0.05 * c.L0), ("optimistic_10.96%", 535.9459071525378),
                    ("conservative_86.49%", 4229.074656)):
        S = (c.L0 - c.SYS_ALLOW - M) / (1 + c.JF)
        f = np.linspace(1e-6, 1 - 1e-6, 400001)
        for core in c.CORES:
            tf, tc = c.geometry(S, f, core)
            for curve in ("optimistic", "conservative"):
                md, Vc, g = modes_curve(core, tf, tc, curve)
                sf = c.least(md)
                i = int(np.argmax(sf))
                vals = {k: float(np.ravel(np.broadcast_to(v, np.shape(sf)))[i]) for k, v in md.items()}
                out["curves"][f"{line}|{core}|{curve}"] = {
                    "SF": float(sf[i]), "governs": min(vals, key=vals.get), "Vc": float(Vc[i]), "gamma": float(g[i]),
                    "tf_mm": float(tf[i]) * 1e3, "tc_mm": float(tc[i]) * 1e3, "modes": vals}
    S0 = (c.L0 - c.SYS_ALLOW) / (1 + c.JF)
    for step in (0.001, 0.0005, 0.00025, 0.0002, 0.0001, 0.00005, 0.00001):
        f = np.arange(step, 1.0, step)
        tf, tc = c.geometry(S0, f, "aluminium")
        sf = c.least(c.modes("aluminium", tf, tc)[0])
        i = int(np.argmax(sf))
        out["grid_014b"][str(step)] = {"max_SF": float(sf[i]), "f": float(f[i]),
                                       "rel_to_014b_0.668649769508548": abs(float(sf[i]) - 0.668649769508548) / 0.668649769508548}
    (c.OUT / "SENS-018-CURVES.json").write_text(json.dumps(out, indent=1))
    for k, v in out["curves"].items():
        print(k, round(v["SF"], 6), v["governs"], "Vc", round(v["Vc"], 4), "gamma", round(v["gamma"], 4))


if __name__ == "__main__":
    main()
