#!/usr/bin/env python3
"""MAINLINE-058 extras: (a) dynamic lift by thrust (momentum theory) and by a tethered kite sail, with the Heathrow
hours a relieved hull fails on the hot side; (b) 050's MIL-HDBK-310 design-day markers against the relieved hulls,
and P3 designed for each marker's own load; (c) re-evacuation times with 034's onboard pumps for the median trim day.
All parameters below the sourced ones are PROJECTION. Writes runs/extra058.json."""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import days058 as D  # noqa: E402
import days058b as DB  # noqa: E402
import lev058 as L  # noqa: E402
import p2m058 as m  # noqa: E402
import p3m058 as p3  # noqa: E402

RUNS = D.RUNS
F050 = Path("unpublished-local-ref:1a1d51aea95bb074"
            "vacuum-mainline050-flyable-weather-1020/DESIGN-DAYS.json")
FM, ETA, BATT, MOTOR = 0.70, 0.85, 108.0, 0.5      # figure of merit; motor+drive; usable Wh/kg (050); kg/kW (PROJECTION)
SAIL_KG_M2, CL = 0.2, 1.0                           # sail + spar areal mass; lift coefficient (PROJECTION)
SHEAR = (100 / 10) ** (1 / 7)                       # 10 m to 100 m wind, 1/7 power law (PROJECTION)


def rotor_power(thrust_n, disk_m2, rho):
    return thrust_n ** 1.5 / math.sqrt(2 * rho * disk_m2) / (FM * ETA)


def thrust_table(R, dLdT):
    rows = []
    rho = 1.18
    for frac in (0.01, 0.04):
        disk = frac * math.pi * R ** 2
        for dk in (0.5, 1.0, 2.0):
            lift = dLdT * dk
            p = rotor_power(lift * m.GRAV, disk, rho)
            motor = MOTOR * p / 1000
            net = {f"{h}h": lift - motor - p * h / BATT for h in (0.5, 1, 2, 4)}
            breakeven_h = (lift - motor) * BATT / p if lift > motor else 0.0
            rows.append({"R_m": R, "disk_fraction_of_frontal": frac, "disk_m2": disk, "deficit_K": dk, "lift_kg": lift,
                         "power_kW": p / 1000, "motor_kg": motor, "net_lift_kg": net,
                         "net_K": {k: v / dLdT for k, v in net.items()}, "breakeven_h": breakeven_h})
    return rows


def main():
    s = D.hour_state()
    lev = json.loads((RUNS / "levers058.json").read_text())
    wind = np.load(RUNS / "heathrow_hourly058.npz")["wind_m_s"]
    out = {"unit": "vacuum-mainline058-flyable-band-1020", "tag": "PROJECTION", "parameters": {
        "figure_of_merit": FM, "motor_drive_efficiency": ETA, "battery_usable_Wh_kg": BATT, "motor_kg_per_kW": MOTOR,
        "sail_kg_m2": SAIL_KG_M2, "kite_CL": CL, "wind_shear_10_to_100m": SHEAR}, "thrust": [], "kite": [], "mil": [],
        "onboard_pump_back": []}
    # (a) dynamic lift on the P2 mask-11 relieved AlAOC hull and the P3 mask-15 design-0 climb hull
    hulls3 = p3.load_hulls()
    p3d0 = L.design_load(100, 0)
    for R in (10, 12, 15, 20, 30):
        vol = 4 * math.pi * R ** 3 / 3
        h = next(x for x in lev["hulls"] if x["R_m"] == R and x["mask"] == 11 and x["id"] == "finish_AlAOC")
        he = L.hot_edge(vol, h["mass_kg"], 100, -30, 1.0, h["design_load_Pa"], "climb")
        lo = L.lift_trim(vol, 100, he - 0.5, -30, 1.0, h["design_load_Pa"], "climb")[0]
        hi = L.lift_trim(vol, 100, he + 0.5, -30, 1.0, h["design_load_Pa"], "climb")[0]
        dLdT = float(lo - hi)
        out["thrust"] += thrust_table(R, dLdT)
        for lead, vol_l, mass, p_d, tab in (
                ("P2", vol, h["mass_kg"], h["design_load_Pa"], D.threshold_table(R, h["tc_m"], h["alpha"], h["eps_day"], h["eps_night"])),
                ("P3", vol - hulls3[(R, "mask15")]["hull"].v_sag, hulls3[(R, "mask15")]["hull"].mass(p3d0), p3d0, None)):
            mo = DB.modes(vol_l, s, p_d)
            lift = np.maximum(mo["L_trim"], mo["L_climb"])
            if tab is not None:
                cf = DB.cold_masks(s, tab, mo["T_floor"])[0]
                cc = DB.cold_masks(s, tab, mo["T_climb"])[0]
                cold_ok = cf | cc
            else:
                cold_ok = np.ones_like(lift, dtype=bool)
            hotfail = (lift < mass) & cold_ok & s["ok"]
            deficit = (mass - lift)[hotfail]
            w100 = (wind * SHEAR)[hotfail]
            q = 0.5 * 1.15 * w100 ** 2
            per_m2 = np.nan_to_num(q * CL / m.GRAV - SAIL_KG_M2, nan=-1)
            rec = {"lead": lead, "R_m": R, "hot_fail_hours_fraction": float(hotfail.sum() / s["ok"].sum()),
                   "deficit_kg": DB.pct(deficit) if deficit.size else None,
                   "wind100_m_s_in_hot_fail_hours": DB.pct(w100[np.isfinite(w100)]) if deficit.size else None, "kite_rescue": {}}
            for area in (0.25, 0.5, 1.0):   # sail area as a fraction of frontal area pi R^2
                sa = area * math.pi * R ** 2
                rec["kite_rescue"][f"{area}xfrontal"] = float(np.mean(per_m2 * sa >= deficit)) if deficit.size else None
            if deficit.size:
                p_med = rotor_power(float(np.median(deficit)) * m.GRAV, 0.04 * math.pi * R ** 2, 1.15)
                rec["thrust_power_for_median_deficit_kW_disk4pct"] = p_med / 1000
            out["kite"].append(rec)
    # (b) MIL markers from 050 DESIGN-DAYS (z = 100 m cases)
    cases = [c for c in json.loads(F050.read_text())["cases"] if c["z_m"] == 100]
    for c in cases:
        offset = c["T_K"] + m.LAPSE * c["z_m"] - 288.15
        dp = c["surface_pressure_anomaly_hPa"]
        x = c["e_Pa"] / c["p_Pa"]
        for R in (10, 12, 15, 20, 30):
            vol = 4 * math.pi * R ** 3 / 3
            row = {"case": c["name"], "R_m": R, "T_K": c["T_K"], "rho_050": c["rho_kg_m3"],
                   "p2_050_design_family_best_kg": max(next(z for z in c["sizes"] if z["R_m"] == R)["payload_by_mask_kg"])}
            w = m.column(c["z_m"], offset, dp, x)
            row["rho_mine"] = float(w["rho"])
            for mask in (11, 15):
                for hid in ("trim-30", "finish_AlAOC"):
                    h = next(y for y in lev["hulls"] if y["R_m"] == R and y["mask"] == mask and y["id"] == hid)
                    # lift_trim takes RH at z; convert the case's mole fraction to RH at 100 m for the call
                    rh = float(x * w["p_Pa"] / m.es_water(w["T_K"]))
                    Lc, _ = L.lift_trim(vol, 100, offset, dp, rh, h["design_load_Pa"], "climb")
                    row[f"P2_{hid}_mask{mask}_payload_kg"] = float(Lc - h["mass_kg"])
            for sel in ("mask15", "mask11"):
                hh = hulls3[(R, sel)]["hull"]
                v3 = vol - hh.v_sag
                rh = float(x * w["p_Pa"] / m.es_water(w["T_K"]))
                for hid, p_d in (("design-30", L.design_load(100, -30)), ("design+0", p3d0)):
                    Lc, _ = L.lift_trim(v3, 100, offset, dp, rh, p_d, "climb")
                    row[f"P3_{hid}_{sel}_payload_kg"] = float(Lc - hh.mass(p_d))
                row[f"P3_designed_for_case_{sel}_payload_kg"] = float(w["rho"] * v3 - hh.mass(float(w["load_Pa"])))
            out["mil"].append(row)
    # (c) pump back the median trim day with 034's onboard benchmarks (75 % installed speed), to 954.6 Pa
    for R in (10, 30):
        vol = 4 * math.pi * R ** 3 / 3
        for name, speed in (("KNF N920 (034, 0.675 m3/h)", 0.675), ("Edwards E2M28 (034, 20.625 m3/h)", 20.625)):
            for p_i in (3500.0, 7400.0):
                out["onboard_pump_back"].append({"R_m": R, "pump": name, "p_internal_Pa": p_i,
                                                 "hours_to_954Pa": vol / speed * math.log(p_i / 954.6)})
    (RUNS / "extra058.json").write_text(json.dumps(out, indent=1, default=float))
    for k in out["kite"]:
        print(k["lead"], k["R_m"], round(k["hot_fail_hours_fraction"], 4), k["deficit_kg"] and {a: round(b) for a, b in k["deficit_kg"].items()},
              k["wind100_m_s_in_hot_fail_hours"] and {a: round(b, 1) for a, b in k["wind100_m_s_in_hot_fail_hours"].items()},
              k["kite_rescue"], round(k.get("thrust_power_for_median_deficit_kW_disk4pct", 0), 1))
    for t in out["thrust"]:
        if t["deficit_K"] == 1.0:
            print("thrust", t["R_m"], t["disk_fraction_of_frontal"], round(t["power_kW"], 2), {a: round(b, 2) for a, b in t["net_K"].items()},
                  round(t["breakeven_h"], 2))
    for r in out["mil"]:
        if r["case"] in ("hot_10pct_z100", "hot_1pct_z100", "joint_hot_humid_10pct_z100"):
            print(r["case"], r["R_m"], round(r["rho_mine"], 4), round(r["rho_050"], 4),
                  {k: round(v) for k, v in r.items() if k.endswith("_kg")})
    for p in out["onboard_pump_back"]:
        print(p)


if __name__ == "__main__":
    main()
