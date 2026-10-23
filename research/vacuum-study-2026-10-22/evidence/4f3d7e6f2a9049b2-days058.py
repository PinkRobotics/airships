#!/usr/bin/env python3
"""MAINLINE-058 days: which Heathrow hours (2014-2023) fall inside each hull's band, and on what fraction of days a whole
24-hour flight, a daylight-only flight or a night-only flight stays inside it.

Hour state at the 100 m centre altitude, 050's convention: sea-level surface; T(z) = T_obs - 0.0065 (z - 27.3 m);
sea-pressure anomaly = SLP - 1013.25 hPa; vapour mole fraction from the observed dew point, constant with height.
Lift tests (lev058.lift_trim logic, vectorised): none (load <= design, else out), trim (load capped by admitting air),
climb (rise in the same column to the design load). P2 cold test: governing outer-skin minimum >= REQ_COLD, from a
threshold table against sky depression D; primary = 050's scenario (night D 24.9 K clear; day D 9.9 K, no sun credit);
cloud-aware sensitivity: sky radiance mixed by observed cloud fraction, overcast sky D 2 K. P3 has no cold screen.
Writes runs/days058.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2m058 as m  # noqa: E402
import p3m058 as p3  # noqa: E402

RUNS = Path("unpublished-local-ref:3c8f53a40b5020e4"
            "vacuum-mainline058-flyable-band-1020/runs")
Z_OBS = 25.29 + 2.0
DGRID = np.array([0.0, 1.0, 2.0, 3.0, 5.0, 7.5, 9.9, 12.5, 15.0, 17.5, 20.0, 22.5, 24.9])
P2_SETS = [  # (label, hull id, mode, description)
    ("P2-050", "full", "none", "050 full-range hull, MLCCAg, no relief"),
    ("P2-trim", "trim-30", "trim", "sized at -30 hPa; admits air above it and to dump cold-day lift; MLCCAg"),
    ("P2-climb", "trim-30", "climb", "sized at -30 hPa; climbs to its design load; ballast or air for cold-day lift; MLCCAg"),
    ("P2-trim-AlAOC", "finish_AlAOC", "trim", "trim hull with Al + acrylic overcoat finish (A 0.14, eps 0.05)"),
    ("P2-trim-lowe", "finish_lowe_night_0.05", "trim", "trim hull, MLCCAg by day, switchable eps 0.05 by night (050)"),
    ("P2-trim-TARC", "finish_TARC_cold", "trim", "trim hull, TARC-class finish (cold state A 0.25, eps 0.20)"),
]
P3_SETS = [("P3-050", "full", "none", "full-range P3 (052 bill at 103.95 kPa), no relief"),
           ("P3-trim", "trim-30", "trim", "P3 sized at -30 hPa, admits (dried) air above it"),
           ("P3-climb", "trim-30", "climb", "P3 sized at -30 hPa, climbs to its design load")]


def hour_state():
    d = np.load(RUNS / "heathrow_hourly058.npz")
    T, TD, SLP, CL, SUN = d["T_K"], d["Td_K"], d["SLP_hPa"], d["cloud_oktas"], d["sun_elevation_deg"]
    ok = np.isfinite(T) & np.isfinite(TD) & np.isfinite(SLP)
    offset = np.where(ok, T + m.LAPSE * Z_OBS - 288.15, 0.0)
    dp = np.where(ok, SLP - 1013.25, 0.0)
    x = np.where(ok, m.es_water(np.where(ok, TD, 280.0)) / (100 * np.where(ok, SLP, 1013.25)), 0.0)
    for _ in range(3):  # station pressure in the same column
        x = np.where(ok, m.es_water(np.where(ok, TD, 280.0)) / m.column(Z_OBS, offset, dp, x)["p_Pa"], 0.0)
    return {"ok": ok, "offset": offset, "dp": dp, "x": x, "cloud": CL, "sun": SUN, "T_obs": T}


def lift_hours(vol, s, p_design, mode, z=100.0):
    w = m.column(z, s["offset"], s["dp"], s["x"])
    cap = p_design - m.QWIND
    if mode == "none":
        good = w["load_Pa"] <= p_design * (1 + 1e-12)
        return w["rho"] * vol, good, w["T_K"]
    if mode == "trim":
        pe = np.minimum(w["p_Pa"], cap)
        return vol * pe * (1 - 0.378 * s["x"]) / (m.RD * w["T_K"]), np.ones(w["p_Pa"].shape, dtype=bool), w["T_K"]
    lo = np.full(w["p_Pa"].shape, z)
    hi = lo + 3000.0
    for _ in range(40):
        mid = (lo + hi) / 2
        pm = m.column(mid, s["offset"], s["dp"], s["x"])["p_Pa"]
        lo = np.where(pm > cap, mid, lo)
        hi = np.where(pm > cap, hi, mid)
    zs = np.where(w["p_Pa"] > cap, (lo + hi) / 2, z)
    c = m.column(zs, s["offset"], s["dp"], s["x"])
    return c["rho"] * vol, np.ones(w["p_Pa"].shape, dtype=bool), c["T_K"]


def threshold_table(radius, tc, alpha, eps_day, eps_night):
    """Ambient threshold (K) against sky depression D, night (no sun) and day (no sun credit, day emittance)."""
    out = {}
    for case, eps in (("night", eps_night), ("day", eps_day)):
        th = []
        for D in DGRID:
            lo, hi = 200.0, 300.0
            for _ in range(40):
                ta = (lo + hi) / 2
                o, _ = m.skin(radius, [tc], ta, ta - D, 0.0, 2.0, alpha, eps)
                if np.min(o) >= m.REQ_COLD:
                    hi = ta
                else:
                    lo = ta
            th.append((lo + hi) / 2)
        out[case] = np.array(th)
    return out


def sky_depression(s, base):
    """Cloud-aware sky depression: radiance mix of the clear depression `base` and an overcast 2 K sky."""
    c = np.where(s["cloud"] >= 0, s["cloud"] / 8.0, 0.0)
    ta = s["T_obs"]
    tsky = ((1 - c) * (ta - base) ** 4 + c * (ta - 2.0) ** 4) ** 0.25
    return np.clip(ta - tsky, 0, 24.9)


def metrics(inband, s):
    ok = s["ok"]
    n = len(inband)
    days = n // 24
    ib = inband.reshape(days, 24)
    okd = ok.reshape(days, 24).all(axis=1)
    sun = (s["sun"] > 0).reshape(days, 24)
    full = ib.all(axis=1) & okd
    dayonly = np.where(sun, ib, True).all(axis=1) & okd
    nightonly = np.where(~sun, ib, True).all(axis=1) & okd
    month = np.array([int(str(np.datetime64("2014-01-01") + np.timedelta64(i, "D"))[5:7]) for i in range(days)])
    by_month = {}
    for mo in range(1, 13):
        sel = (month == mo) & okd
        by_month[mo] = {"hours": float(ib[sel].mean()) if sel.any() else None,
                        "full_days": float(full[sel].mean()) if sel.any() else None,
                        "daylight_days": float(dayonly[sel].mean()) if sel.any() else None}
    return {"hours_fraction": float(inband[ok].mean()), "full_day_fraction": float(full[okd].mean()),
            "daylight_only_day_fraction": float(dayonly[okd].mean()), "night_only_day_fraction": float(nightonly[okd].mean()),
            "days_counted": int(okd.sum()), "by_month": by_month}


def main():
    s = hour_state()
    lev = json.loads((RUNS / "levers058.json").read_text())
    hulls3 = p3.load_hulls()
    p_trim3 = json.loads((RUNS / "p3_058.json").read_text())["p_trim_Pa"]
    out = {"unit": "vacuum-mainline058-flyable-band-1020", "site": "London Heathrow, NOAA ISD 03772099999, 2014-2023",
           "tag": "QUESTIONABLE / PROJECTION", "D_grid_K": DGRID.tolist(), "rows": []}
    night = s["sun"] <= 0
    for R in (10, 12, 15, 20, 30):
        vol = 4 * np.pi * R ** 3 / 3
        for mask in (11, 15):
            for label, hid, mode, desc in P2_SETS:
                h = next(x for x in lev["hulls"] if x["R_m"] == R and x["mask"] == mask and x["id"] == hid)
                L, sgood, Tz = lift_hours(vol, s, h["design_load_Pa"], mode)
                lift_ok = (L >= h["mass_kg"]) & sgood
                tab = threshold_table(R, h["tc_m"], h["alpha"], h["eps_day"], h["eps_night"])
                t_prim = np.where(night, np.interp(24.9, DGRID, tab["night"]), np.interp(9.9, DGRID, tab["day"]))
                dn = sky_depression(s, 24.9)
                dd = sky_depression(s, 9.9)
                t_cloud = np.where(night, np.interp(dn, DGRID, tab["night"]), np.interp(dd, DGRID, tab["day"]))
                cold_prim = Tz >= t_prim
                cold_cloud = Tz >= t_cloud
                for variant, cold in (("primary", cold_prim), ("cloud_aware", cold_cloud)):
                    ib = lift_ok & cold & s["ok"]
                    row = {"lead": "P2", "R_m": R, "mask": mask, "set": label, "hull": hid, "mode": mode, "variant": variant,
                           "description": desc, "mass_kg": h["mass_kg"],
                           "fail_hot_fraction": float((~lift_ok & s["ok"]).mean()),
                           "fail_cold_fraction": float((~cold & s["ok"]).mean()), **metrics(ib, s)}
                    if variant == "primary":
                        row["thresholds_K"] = {"night": tab["night"].tolist(), "day_no_sun": tab["day"].tolist()}
                    out["rows"].append(row)
                print(R, mask, label, round(out["rows"][-2]["hours_fraction"], 4), round(out["rows"][-2]["full_day_fraction"], 4),
                      round(out["rows"][-1]["hours_fraction"], 4), round(out["rows"][-1]["full_day_fraction"], 4), flush=True)
        for sel in ("mask15", "mask11", "baseline"):
            hh = hulls3[(R, sel)]["hull"]
            for label, hid, mode, desc in P3_SETS:
                p_d = 103953.19780784745 if hid == "full" else p_trim3
                L, sgood, Tz = lift_hours(vol - hh.v_sag, s, p_d, mode)
                ib = (L >= hh.mass(p_d)) & sgood & s["ok"]
                row = {"lead": "P3", "R_m": R, "mask": sel, "set": label, "hull": hid, "mode": mode, "variant": "primary",
                       "description": desc, "mass_kg": hh.mass(p_d), "fail_hot_fraction": float((~ib & s["ok"]).mean()),
                       "fail_cold_fraction": 0.0, **metrics(ib, s)}
                out["rows"].append(row)
                print(R, sel, label, round(row["hours_fraction"], 4), round(row["full_day_fraction"], 4), flush=True)
    (RUNS / "days058.json").write_text(json.dumps(out, indent=1))
    print("DONE")


if __name__ == "__main__":
    main()
