#!/usr/bin/env python3
"""CHECK-060 extras: exact Weibull m for the card's CVs and the walls they give; Pernas-Sanchez's delamination scaling at the
pitch wall; the axial-force reading of the strut comparison. Appends 'extras' to RESULTS-CHECK.json."""
import json
import math
from pathlib import Path

import check060 as C

OUT = C.OUT


def cv_of_m(m):
    g1, g2 = math.gamma(1 + 1 / m), math.gamma(1 + 2 / m)
    return math.sqrt(g2 / g1 ** 2 - 1)


def m_of_cv(cv):
    lo, hi = 2.0, 200.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if cv_of_m(mid) > cv:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    res = json.loads(OUT.read_text())
    s1 = res["sec1"]
    ex = {"m_exact": {}, "walls_exact_m": {}}
    for cv in (0.051, 0.052, 0.06):
        ex["m_exact"][str(cv)] = {"exact": m_of_cv(cv), "card_1p2_over_cv": 1.2 / cv, "cv_at_card_m": cv_of_m(1.2 / cv)}
    for cid in ("K13D2U-50-20-20-10", "M55J-70-10-10-10", "M55J-50-20-20-10", "K13D2U-UD"):
        r = s1[cid]
        ks = {int(k): v for k, v in r["k"].items()}
        row = {}
        for cv in (0.052, 0.06):
            m = m_of_cv(cv)
            k = C.interp_k(ks, m)
            scale = r["lam_mean_GPa"] / C.gam(m)
            row[str(cv)] = {"m": m, "wall_cg": max(1.0, k * r["peak_cg_GPa"] / scale), "wall_fe": max(1.0, k * r["peak_fe_GPa"] / scale)}
        ex["walls_exact_m"][cid] = row
    af = math.pi * 0.0254 ** 2
    ex["pernas_scaling"] = {"C1_J_m3": 85e6, "Af_m2_50p8mm": af, "KEc_1p45mm_J": 85e6 * af * 0.00145,
                            "KEc_1p45mm_over_32p3J": 85e6 * af * 0.00145 / 32.333}
    res["extras"] = ex
    OUT.write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(ex, indent=1, default=float))


if __name__ == "__main__":
    main()
