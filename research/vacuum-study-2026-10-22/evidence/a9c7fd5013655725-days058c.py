#!/usr/bin/env python3
"""MAINLINE-058 P2 sweep at Heathrow: design sea-pressure anomaly (-30/-20/-10/0/+10 hPa at the 100 m floor) x finish
(MLCCAg, AlAOC, switchable low-e night) x the subsets that contain gamma (1, 3, 5, 7, 9, 11, 13, 15), each sized at its
finish's own cold design temperature (clear-night threshold of the mask-11 trim hull's core + 0.035 K, as lev058).
Sets trim / climb / best (days058b definitions), primary and cloud-aware cold tests. Also the worst-corner hot edges
(-30/0/+30 hPa, RH 100 %) with the best relief and the lowest sea-pressure anomaly at ISA (offset 0, RH 100 %).
Writes runs/days058c.json."""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import days058 as D  # noqa: E402
import days058b as DB  # noqa: E402
import lev058 as L  # noqa: E402

RUNS = D.RUNS
FIN = {"MLCCAg": (0.09, 0.80, 0.80), "AlAOC": (0.14, 0.05, 0.05), "lowe_night_0.05": (0.09, 0.80, 0.05)}
MASKS = (1, 3, 5, 7, 9, 11, 13, 15)
DPS = (-30, -20, -10, 0, 10)


def main():
    t0 = time.time()
    s = D.hour_state()
    lev = json.loads((RUNS / "levers058.json").read_text())
    loads = {dp: L.design_load(100, dp) for dp in DPS}
    out = {"unit": "vacuum-mainline058-flyable-band-1020", "tag": "QUESTIONABLE / PROJECTION", "design_loads_Pa": loads,
           "rows": []}
    for R in (10, 12, 15, 20, 30):
        vol = 4 * math.pi * R ** 3 / 3
        for fin, (a, ed, en) in FIN.items():
            hid = "trim-30" if fin == "MLCCAg" else f"finish_{fin}"
            ref = next(x for x in lev["hulls"] if x["R_m"] == R and x["mask"] == 11 and x["id"] == hid)
            tdes = ref["design_T_K"]
            tab = D.threshold_table(R, ref["tc_m"], a, ed, en)
            for mask in MASKS:
                for dp in DPS:
                    p_d = loads[dp]
                    hull, o = L.build(R, p_d, tdes, mask, a, ed, en)
                    mass = o["mass_kg"]
                    mo = DB.modes(vol, s, p_d)
                    cf = DB.cold_masks(s, tab, mo["T_floor"])
                    cc = DB.cold_masks(s, tab, mo["T_climb"])
                    lt = mo["L_trim"] >= mass
                    lc = mo["L_climb"] >= mass
                    row = {"R_m": R, "finish": fin, "mask": mask, "design_dp_hPa": dp, "design_load_Pa": p_d, "mass_kg": mass,
                           "tf_m": o["tf_m"], "tc_m": o["tc_m"], "design_T_K": tdes,
                           "clear_night_threshold_K": float(np.interp(24.9, D.DGRID, tab["night"])),
                           "hot_edge_K": {}, "sets": {}}
                    for st in ("trim", "climb", "best"):
                        for v, k in (("primary", 0), ("cloud_aware", 1)):
                            tr = lt & cf[k]
                            cl = lc & cc[k]
                            ib = {"trim": tr, "climb": cl, "best": tr | cl}[st] & s["ok"]
                            mt = D.metrics(ib, s)
                            if not (st == "best" and v == "primary"):
                                mt.pop("by_month")
                            row["sets"][f"{st}:{v}"] = mt
                    for edp in (-30, 0, 30):
                        he_t = L.hot_edge(hull.volume, mass, 100, edp, 1.0, p_d, "trim")
                        he_c = L.hot_edge(hull.volume, mass, 100, edp, 1.0, p_d, "climb")
                        row["hot_edge_K"][str(edp)] = {"trim": he_t, "climb": he_c}
                    row["lowest_dp_at_ISA_RH100_hPa"] = L.lowest_dp(hull.volume, mass, 100, 0.0, 1.0)
                    out["rows"].append(row)
                print(R, fin, mask, round(time.time() - t0, 1), flush=True)
    (RUNS / "days058c.json").write_text(json.dumps(out, indent=1))
    print("DONE", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
