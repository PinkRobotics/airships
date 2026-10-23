#!/usr/bin/env python3
"""MAINLINE-058 validation: rebuild 050's fixed full-range P2 hulls with my own p2m058 and compare with FIXED-HULLS.json
(read as data): design pressure, geometry, mass, design-temperature thermal state, modes, and the 100/500 m zero-payload
offsets. Also finds my own cold-interface threshold for each hull. Writes runs/validate058.json."""
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2m058 as m  # noqa: E402

F050 = Path("unpublished-local-ref:1a1d51aea95bb074"
            "vacuum-mainline050-flyable-weather-1020/FIXED-HULLS.json")
OUT = Path("unpublished-local-ref:3c8f53a40b5020e4"
           "vacuum-mainline058-flyable-band-1020/runs/validate058.json")


def zero_offset(volume, mass, z, anom, rh, lo=-60.0, hi=60.0):
    for _ in range(42):
        mid = (lo + hi) / 2
        if m.atmosphere(z, mid, anom, rh)["rho"] * volume >= mass:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def cold_threshold(radius, tc, lo=240.0, hi=300.0, **kw):
    """Ambient at which the night outer-skin minimum equals REQ_COLD for this core."""
    for _ in range(40):
        ta = (lo + hi) / 2
        if m.thermal(radius, [tc], ta, **kw)["min_outer_K"][0] >= m.REQ_COLD:
            hi = ta
        else:
            lo = ta
    return (lo + hi) / 2


def main():
    t0 = time.time()
    ref = json.loads(F050.read_text())
    z = np.arange(100, 1501, 50)
    t = np.arange(-20, 21)
    p = np.arange(-30, 31, 2)
    rh = np.linspace(0, 1, 11)
    w = m.atmosphere(z[:, None, None, None], t[None, :, None, None], p[None, None, :, None], rh[None, None, None, :])
    designp = float(w["load_Pa"].max())
    rows = []
    for rb in ref["reference_builds"]:
        r = rb["R_m"]
        designT = rb["design_temperature_K"]
        grid = np.geomspace(0.001 * r / 10, 1.5 * r / 10, 241)
        table = m.thermal(r, grid, designT)
        hull = m.P2(r)
        o = hull.optimum(designp, table, 11, 1.0, grid=1600)
        th = m.thermal(r, [o["tc_m"]], designT)
        bounds = {}
        for alt in (100, 500):
            for anom in (-30, 0, 30):
                for h in (0.0, 1.0):
                    bounds[f"z{alt}_dp{anom}_rh{int(h * 100)}"] = zero_offset(hull.volume, o["mass_kg"], alt, anom, h)
        theirs = {}
        for s in ref["boundary_slices"]:
            if s["R_m"] == r and s["z_m"] in (100, 500):
                theirs[f"z{s['z_m']}_dp{s['sea_pressure_anomaly_hPa']}_rh0"] = s["RH0_upper_offset_K"]
                theirs[f"z{s['z_m']}_dp{s['sea_pressure_anomaly_hPa']}_rh100"] = s["RH100_upper_offset_K"]
        tcold = cold_threshold(r, o["tc_m"])
        rows.append({"R_m": r, "design_temperature_K_050": designT,
                     "mine": {"tf_m": o["tf_m"], "tc_m": o["tc_m"], "mass_kg": o["mass_kg"], "minimum_SF": o["minimum_SF"],
                              "modes": o["modes"], "bill_kg": o["bill_kg"],
                              "thermal_at_designT": {k: float(v[0]) for k, v in th.items() if k != "tc_m"}},
                     "050": {"tf_m": rb["tf_m"], "tc_m": rb["tc_m"], "mass_kg": rb["mass_kg"], "modes": rb["modes"],
                             "thermal": rb["thermal"]},
                     "mass_difference_kg": o["mass_kg"] - rb["mass_kg"],
                     "zero_offsets_mine_K": bounds, "zero_offsets_050_K": theirs,
                     "max_zero_offset_difference_K": max(abs(bounds[k] - theirs[k]) for k in theirs),
                     "my_cold_threshold_air_K": tcold,
                     "my_cold_threshold_ISA_offset_100m_K": tcold - (288.15 - 0.65),
                     "my_cold_threshold_ISA_offset_500m_K": tcold - (288.15 - 3.25)})
        print(r, round(o["mass_kg"], 3), round(rb["mass_kg"], 3), round(o["tf_m"] * 1e3, 5), round(o["tc_m"] * 1e3, 4),
              round(tcold, 3), round(time.time() - t0, 1), flush=True)
    res = {"design_pressure_Pa_mine": designp, "design_pressure_Pa_050": ref["design_pressure_Pa"],
           "REQ_COLD_K": m.REQ_COLD, "rows": rows, "seconds": time.time() - t0}
    OUT.write_text(json.dumps(res, indent=1))
    print("DONE", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
