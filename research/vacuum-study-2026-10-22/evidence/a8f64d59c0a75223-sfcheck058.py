#!/usr/bin/env python3
"""MAINLINE-058 check: every relieved and finish P2 hull (masks 11, 15) keeps minimum SF >= 1 at its design load from its
clear-night cold threshold up to 315 K air (1 K steps, own thermal state at each ambient). Writes runs/sfcheck058.json."""
import json
from pathlib import Path

import numpy as np

import p2m058 as m

RUNS = Path("unpublished-local-ref:3c8f53a40b5020e4"
            "vacuum-mainline058-flyable-band-1020/runs")


def main():
    lev = json.loads((RUNS / "levers058.json").read_text())
    rows = []
    for h in lev["hulls"]:
        if h["mask"] not in (11, 15) or not (h["id"] in ("full", "trim-30") or h["id"].startswith("finish_")):
            continue
        hull = m.P2(h["R_m"])
        t0 = h["cold_threshold_K"]["clear_night"]
        worst = (9.0, None, None)
        for ta in np.r_[h["design_T_K"], np.arange(np.ceil(t0) + 1, 316, 1.0)]:
            th = m.thermal(h["R_m"], [h["tc_m"]], ta, alpha=h["alpha"], eps_day=h["eps_day"], eps_night=h["eps_night"])
            e = hull.evaluate(h["tf_m"], h["tc_m"], h["design_load_Pa"], th, h["mask"], 1.0)
            sf = float(np.asarray(e["minimum_SF"]).ravel()[0])
            if sf < worst[0]:
                worst = (sf, float(ta), min(e["modes"], key=lambda k: float(np.asarray(e["modes"][k]).ravel()[0])))
        rows.append({"R_m": h["R_m"], "mask": h["mask"], "hull": h["id"], "min_SF": worst[0], "at_air_K": worst[1],
                     "mode": worst[2], "design_T_K": h["design_T_K"]})
    res = {"rows": rows, "all_at_or_above_one": all(r["min_SF"] >= 1 - 1e-9 for r in rows),
           "lowest": min(r["min_SF"] for r in rows)}
    (RUNS / "sfcheck058.json").write_text(json.dumps(res, indent=1))
    print(res["all_at_or_above_one"], res["lowest"], sorted({(r["at_air_K"] == r["design_T_K"]) for r in rows}))


if __name__ == "__main__":
    main()
