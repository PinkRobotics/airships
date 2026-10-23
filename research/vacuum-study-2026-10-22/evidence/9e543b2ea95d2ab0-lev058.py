#!/usr/bin/env python3
"""MAINLINE-058 P2 levers on one fixed hull per radius (own p2m058 model).

Hulls (all sized at the cold-interface design temperature, as 050's fixed builds):
  full    050's full-range build: design load = max over 050's z100-1500/T+-20/dp+-30/RH0-1 grid (103953.2 Pa).
  trimNN  sized for the load at the floor on a sea-pressure anomaly of NN hPa (max over T+-20 K, RH 0-1); on higher
          pressure it admits air (or climbs) so the load never exceeds the design value.
  floorZ  trim hull with a floor of Z m (design at -30 hPa there), flown at Z.
  finish  trim-30 hull with another outer finish (alpha, eps); designed at that finish's own cold threshold.
Bands: zero-payload hot edge (ISA offset at the floor) by sea-pressure anomaly and RH; cold edges by sky case.
Writes runs/levers058.json."""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2m058 as m  # noqa: E402

F050 = Path("unpublished-local-ref:1a1d51aea95bb074"
            "vacuum-mainline050-flyable-weather-1020/FIXED-HULLS.json")
OUT = Path("unpublished-local-ref:3c8f53a40b5020e4"
           "vacuum-mainline058-flyable-band-1020/runs/levers058.json")
RADII = (10, 12, 15, 20, 30)
DP = np.array([-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40], dtype=float)
RH = (0.0, 0.5, 1.0)
# outer finishes: (id, alpha, eps_day, eps_night, source tag)
FINISHES = [
    ("MLCCAg", 0.09, 0.80, 0.80, "048 selected multilayer CCAg/ITO (patent recipe, NASA class optics): QUESTIONABLE/PROJECTION"),
    ("CCAg", 0.09, 0.65, 0.65, "048 classical CCAg/ITO: QUESTIONABLE"),
    ("AgFEP05", 0.09, 0.40, 0.40, "048 / Sheldahl Red Book 0.5 mil Ag/FEP second-surface mirror: QUESTIONABLE"),
    ("SiOxAl", 0.13, 0.26, 0.26, "048 / Sheldahl Red Book p.89 SiOx over Al/polyimide (eps ~0.25): QUESTIONABLE"),
    ("TARC_cold", 0.25, 0.20, 0.20, "Tang et al. Science 374:1504 (2021) TARC below ~22 C: A ~0.25, sky-window eps 0.20; "
                                     "grey transfer PROJECTION"),
    ("AlAOC", 0.14, 0.05, 0.05, "Sheldahl Red Book Rev E: Al first surface + acrylic overcoat, A 0.14, eps_H 0.05: QUESTIONABLE"),
    ("lowe_night_0.05", 0.09, 0.80, 0.05, "050's projected switchable low-emittance night state, day MLCCAg: PROJECTION"),
]
SKY = {"clear_night": dict(night_depr=24.9), "overcast_night": dict(night_depr=2.0, wind=0.5)}


def cold_threshold(radius, tc, alpha, eps_day, eps_night, case, lo=200.0, hi=300.0):
    """Ambient air temperature at which the governing outer-skin minimum equals REQ_COLD."""
    for _ in range(44):
        ta = (lo + hi) / 2
        if case == "day":
            th = m.thermal(radius, [tc], ta, alpha=alpha, eps_day=eps_day, eps_night=eps_night)
            ok = th["min_outer_day_K"][0] >= m.REQ_COLD
        else:
            kw = dict(SKY[case])
            th = m.thermal(radius, [tc], ta, alpha=alpha, eps_day=eps_day, eps_night=eps_night, **kw)
            ok = th["min_outer_K"][0] >= m.REQ_COLD
        if ok:
            hi = ta
        else:
            lo = ta
    return (lo + hi) / 2


def design_load(z_floor, dp):
    t = np.arange(-20, 21, 1.0)
    rh = np.linspace(0, 1, 11)
    w = m.atmosphere(z_floor, t[:, None], dp, rh[None, :])
    return float(w["load_Pa"].max())


def build(radius, p_design, t_design, mask, alpha=0.09, eps_day=0.80, eps_night=0.80, grid=1600):
    tcg = np.geomspace(0.001 * radius / 10, 1.5 * radius / 10, 241)
    table = m.thermal(radius, tcg, t_design, alpha=alpha, eps_day=eps_day, eps_night=eps_night)
    hull = m.P2(radius)
    o = hull.optimum(p_design, table, mask, 1.0, grid=grid)
    return hull, o


def lift_trim(volume, z, offset, dp, rh, p_design, mode):
    """Lift (kg) of an evacuated hull at the floor z. mode: 'none' (no relief: infeasible above design load),
    'trim' (admit air to cap the load), 'climb' (rise to the altitude where the load equals the design value)."""
    w = m.atmosphere(z, offset, dp, rh)
    cap = p_design - m.QWIND
    if mode == "none":
        return np.where(w["load_Pa"] <= p_design * (1 + 1e-12), w["rho"] * volume, -np.inf), w
    if mode == "trim":
        pe = np.minimum(w["p_Pa"], cap)
        return volume * pe * (1 - 0.378 * w["x"]) / (m.RD * w["T_K"]), w
    # climb: find z* in the same column (same mole fraction) with p(z*) = cap when p(z) > cap
    lo = np.full(np.shape(w["p_Pa"]), float(z))
    hi = np.full(np.shape(w["p_Pa"]), float(z) + 3000.0)
    for _ in range(50):
        mid = (lo + hi) / 2
        pm = m.column(mid, offset, dp, w["x"])["p_Pa"]
        lo = np.where(pm > cap, mid, lo)
        hi = np.where(pm > cap, hi, mid)
    zs = np.where(w["p_Pa"] > cap, (lo + hi) / 2, float(z))
    c = m.column(zs, offset, dp, w["x"])
    return c["rho"] * volume, dict(w, z_star=zs, T_star=c["T_K"])


def hot_edge(volume, mass, z, dp, rh, p_design, mode):
    lo, hi = -80.0, 80.0
    if lift_trim(volume, z, lo, dp, rh, p_design, mode)[0] < mass:
        return None
    for _ in range(46):
        mid = (lo + hi) / 2
        if lift_trim(volume, z, mid, dp, rh, p_design, mode)[0] >= mass:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def structural_upper_dp(z, offset, rh, p_design):
    """Highest sea-pressure anomaly the unrelieved hull survives at this temperature (load = design)."""
    lo, hi = -200.0, 200.0
    for _ in range(46):
        mid = (lo + hi) / 2
        if m.atmosphere(z, offset, mid, rh)["load_Pa"] <= p_design:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def lowest_dp(volume, mass, z, offset, rh):
    """Lowest sea-pressure anomaly at which it still floats at this temperature (lift = mass), unrelieved lift."""
    lo, hi = -300.0, 200.0
    for _ in range(46):
        mid = (lo + hi) / 2
        if m.atmosphere(z, offset, mid, rh)["rho"] * volume >= mass:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def heating_power(radius, tc, ta, alpha, eps, setpoint):
    """Outer-skin heater flux (>=0, per zone) holding every zone at or above setpoint on the clear night; W total."""
    heater = np.zeros((1, len(m.MU)))
    for _ in range(400):
        out, _ = m.skin(radius, [tc], ta, ta - 24.9, 0.0, 2.0, alpha, eps, heater=heater)
        new = np.maximum(0.0, heater + 6.0 * (setpoint - out))
        if np.max(np.abs(new - heater)) < 1e-4:
            heater = new
            break
        heater = new
    area = 4 * math.pi * radius ** 2
    return float(area * (heater @ m.WG / 2)[0]), float(np.min(out))


def main():
    t0 = time.time()
    ref = {b["R_m"]: b for b in json.loads(F050.read_text())["reference_builds"]}
    p_full = 103953.19780784745
    loads = {f"z{z}_dp{dp}": design_load(z, dp) for z in (50, 100, 200, 300) for dp in (-30, -20, -10, 0, 10, 20, 30)}
    hulls, bands, costs = [], [], []
    for r in RADII:
        t_d = ref[r]["design_temperature_K"]
        for mask in (11, 15):
            specs = [("full", p_full, 100, "MLCCAg")]
            specs += [(f"trim{dp:+d}", loads[f"z100_dp{dp}"], 100, "MLCCAg") for dp in (-30, -20, -10, 0, 10, 20)]
            specs += [(f"floor{z}", loads[f"z{z}_dp-30"], z, "MLCCAg") for z in (50, 200, 300)]
            specs += [(f"finish_{f[0]}", loads["z100_dp-30"], 100, f[0]) for f in FINISHES[1:]]
            for hid, p_d, z_floor, fin in specs:
                f = next(x for x in FINISHES if x[0] == fin)
                alpha, ed, en = f[1], f[2], f[3]
                if fin == "MLCCAg":
                    tdes = t_d
                else:
                    # design at this finish's own clear-night threshold for the trim-30 MLCCAg core (+0.035 K)
                    base = next(h for h in hulls if h["R_m"] == r and h["mask"] == mask and h["id"] == "trim-30")
                    tdes = cold_threshold(r, base["tc_m"], alpha, ed, en, "clear_night") + 0.035
                hull, o = build(r, p_d, tdes, mask, alpha, ed, en)
                th = m.thermal(r, [o["tc_m"]], tdes, alpha=alpha, eps_day=ed, eps_night=en)
                rec = {"R_m": r, "mask": mask, "id": hid, "finish": fin, "alpha": alpha, "eps_day": ed, "eps_night": en,
                       "design_load_Pa": p_d, "design_T_K": tdes, "floor_m": z_floor, "tf_m": o["tf_m"], "tc_m": o["tc_m"],
                       "mass_kg": o["mass_kg"], "minimum_SF": o["minimum_SF"], "modes": o["modes"], "bill_kg": o["bill_kg"],
                       "thermal_at_design": {k: float(v[0]) for k, v in th.items() if k != "tc_m"}}
                rec["cold_threshold_K"] = {c: cold_threshold(r, o["tc_m"], alpha, ed, en, c)
                                           for c in ("clear_night", "overcast_night", "day")}
                # day skin extremes at the ISA 100 m temperature for the finish comparison
                tday = m.thermal(r, [o["tc_m"]], 287.5, alpha=alpha, eps_day=ed, eps_night=en)
                rec["at_ISA100"] = {k: float(v[0]) for k, v in tday.items() if k != "tc_m"}
                hulls.append(rec)
                modes = ("none", "trim", "climb") if hid != "full" else ("none",)
                for mode in modes:
                    for dp in DP:
                        for rh in RH:
                            he = hot_edge(hull.volume, o["mass_kg"], z_floor, dp, rh, p_d, mode)
                            row = {"R_m": r, "mask": mask, "hull": hid, "mode": mode, "floor_m": z_floor, "dp_hPa": float(dp),
                                   "RH": rh, "hot_edge_offset_K": he}
                            if he is not None:
                                L, w = lift_trim(hull.volume, z_floor, he, dp, rh, p_d, mode)
                                row["T_hot_K"] = float(w["T_K"])
                                if mode == "climb":
                                    row["z_star_m"] = float(w["z_star"])
                                if mode == "trim":
                                    row["p_internal_Pa"] = float(max(0.0, w["p_Pa"] - (p_d - m.QWIND)))
                            bands.append(row)
                print(r, mask, hid, round(o["mass_kg"], 2), round(tdes, 3), {k: round(v, 2) for k, v in rec["cold_threshold_K"].items()},
                      round(time.time() - t0, 1), flush=True)
        # night heating power (mask 11 trim-30 hull, MLCCAg) on the clear night below its threshold
        base = next(h for h in hulls if h["R_m"] == r and h["mask"] == 11 and h["id"] == "trim-30")
        tcl = base["cold_threshold_K"]["clear_night"]
        for dt in (1, 2, 5, 10, 15, 20):
            pw, mn = heating_power(r, base["tc_m"], tcl - dt, 0.09, 0.80, m.REQ_COLD + 0.05)
            costs.append({"R_m": r, "lever": "night_heating", "ambient_K": tcl - dt, "below_clear_threshold_K": dt,
                          "power_W": pw, "energy_12h_kWh": pw * 12 / 1000, "battery_12h_kg_at_108Whkg": pw * 12 / 108,
                          "min_outer_K": mn})
    res = {"unit": "vacuum-mainline058-flyable-band-1020", "tag": "QUESTIONABLE / PROJECTION", "REQ_COLD_K": m.REQ_COLD,
           "QWIND_Pa": m.QWIND, "design_loads_Pa": loads, "full_range_load_Pa": p_full, "finishes": FINISHES,
           "hulls": hulls, "bands": bands, "costs": costs, "seconds": time.time() - t0}
    OUT.write_text(json.dumps(res, indent=1))
    print("DONE", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
