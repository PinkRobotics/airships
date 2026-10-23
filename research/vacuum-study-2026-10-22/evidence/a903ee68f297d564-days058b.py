#!/usr/bin/env python3
"""MAINLINE-058 days, full set: Heathrow 2014-2023 hours against every optimism subset and lever set.

P2: for each radius and each of the 16 endpoint subsets (usage 1), the full-range build (103953.2 Pa) and the build
sized at -30 hPa (98019.4 Pa), both MLCCAg at the cold design temperature; finish variants (AlAOC, switchable low-e)
for masks 11 and 15 from levers058. Sets: none, trim (air for relief and cold-day lift dump), climb (rise to the
design load; ballast or air for the dump), best (per hour, climb if its colder air passes the cold test, else trim),
free (no dump: floats at its equilibrium altitude, relieved by air there if still overloaded). Cold thresholds against
sky depression are tabulated once per radius and finish on the mask-11 trim hull's core (core differences between
subsets move them by < 0.05 K). P3: every 052 subset and the baseline at design loads -30/-20/-10/0/+10 hPa and
full range, sets none/trim/climb/best (best = climb, P3 has no cold screen).
Also: excess lift over in-band hours (ballast or dump need), daily trim-air peak pressure and re-evacuation time,
climb heights. Writes runs/days058b.json."""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import days058 as D  # noqa: E402
import lev058 as L  # noqa: E402
import p2m058 as m  # noqa: E402
import p3m058 as p3  # noqa: E402

RUNS = D.RUNS
P_FULL = 103953.19780784745
GROUND_SPEED_PER_M3 = 1574.9 / 4188.790204786391     # 052: effective m3/h per m3 of hull for a 24 h first evacuation


def column_state(s, z):
    return m.column(z, s["offset"], s["dp"], s["x"])


def modes(vol, s, p_d, z=100.0):
    """Per hour: lift (kg) for none/trim/climb, hull-altitude T for each, climb height, relief pressure for trim."""
    w = column_state(s, z)
    cap = p_d - m.QWIND
    out = {"w": w}
    out["none_ok"] = w["load_Pa"] <= p_d * (1 + 1e-12)
    out["L_none"] = w["rho"] * vol
    pe = np.minimum(w["p_Pa"], cap)
    out["L_trim"] = vol * pe * (1 - 0.378 * s["x"]) / (m.RD * w["T_K"])
    out["p_relief"] = np.maximum(0.0, w["p_Pa"] - cap)
    lo = np.full(w["p_Pa"].shape, z)
    hi = lo + 3000.0
    for _ in range(40):
        mid = (lo + hi) / 2
        pm = m.column(mid, s["offset"], s["dp"], s["x"])["p_Pa"]
        lo = np.where(pm > cap, mid, lo)
        hi = np.where(pm > cap, hi, mid)
    zs = np.where(w["p_Pa"] > cap, (lo + hi) / 2, z)
    c = m.column(zs, s["offset"], s["dp"], s["x"])
    out["L_climb"], out["T_climb"], out["z_climb"] = c["rho"] * vol, c["T_K"], zs
    out["T_floor"] = w["T_K"]
    return out


def free_float(vol, s, mass, p_d, z=100.0):
    """Equilibrium altitude above the floor where rho V = mass; relief by air there if still overloaded."""
    w = column_state(s, z)
    ok = w["rho"] * vol >= mass
    lo = np.full(w["p_Pa"].shape, z)
    hi = lo + 6000.0
    for _ in range(44):
        mid = (lo + hi) / 2
        r = m.column(mid, s["offset"], s["dp"], s["x"])["rho"] * vol
        lo = np.where(r >= mass, mid, lo)
        hi = np.where(r >= mass, hi, mid)
    ze = np.where(ok, (lo + hi) / 2, z)
    c = m.column(ze, s["offset"], s["dp"], s["x"])
    return ok, c["T_K"], ze, np.maximum(0.0, c["p_Pa"] - (p_d - m.QWIND))


def cold_masks(s, tab, T_at):
    night = s["sun"] <= 0
    t_prim = np.where(night, np.interp(24.9, D.DGRID, tab["night"]), np.interp(9.9, D.DGRID, tab["day"]))
    dn = D.sky_depression(s, 24.9)
    dd = D.sky_depression(s, 9.9)
    t_cl = np.where(night, np.interp(dn, D.DGRID, tab["night"]), np.interp(dd, D.DGRID, tab["day"]))
    return T_at >= t_prim, T_at >= t_cl


def pct(a, qs=(50, 90, 99, 100)):
    a = np.asarray(a)
    if a.size == 0:
        return None
    return {str(q): float(np.percentile(a, q)) for q in qs}


def stats_trim(s, inband, mo, mass, vol, use_air_dump, chosen_trim):
    """Daily peak internal pressure (relief, plus dump by air if use_air_dump) over in-band hours where trim is used."""
    lift_after = np.where(chosen_trim, mo["L_trim"], mo["L_climb"])
    excess = np.maximum(0.0, lift_after - mass)
    Tz = np.where(chosen_trim, mo["T_floor"], mo["T_climb"])
    p_dump = excess * m.RD * Tz / vol
    p_int = np.where(chosen_trim, mo["p_relief"], 0.0) + (p_dump if use_air_dump else 0.0)
    p_int = np.where(inband, p_int, 0.0)
    days = len(inband) // 24
    peak = p_int.reshape(days, 24).max(axis=1)
    used = peak > 1.0
    t10 = np.where(used, (1 / GROUND_SPEED_PER_M3) * np.log(np.maximum(peak, 10.0) / 10.0), 0.0)
    t100 = np.where(used, (1 / GROUND_SPEED_PER_M3) * np.log(np.maximum(peak, 100.0) / 100.0), 0.0)
    ideal_kWh = np.where(used, vol * peak * (1 + np.log(101325.0 / np.maximum(peak, 1.0))) / 3.6e6, 0.0)
    return {"days_with_trim_air_fraction": float(used.mean()), "daily_peak_internal_Pa": pct(peak[used]),
            "reevac_to_10Pa_h": pct(t10[used]), "reevac_to_100Pa_h": pct(t100[used]),
            "ideal_isothermal_kWh_per_trim_day": pct(ideal_kWh[used]),
            "excess_lift_kg_inband_hours": pct(excess[inband])}


def main():
    t0 = time.time()
    s = D.hour_state()
    lev = json.loads((RUNS / "levers058.json").read_text())
    p_trim = L.design_load(100, -30)
    loads = {dp: L.design_load(100, dp) for dp in (-30, -20, -10, 0, 10)}
    hulls3 = p3.load_hulls()
    res = {"unit": "vacuum-mainline058-flyable-band-1020", "site": "London Heathrow, NOAA ISD 03772099999, 2014-2023",
           "tag": "QUESTIONABLE / PROJECTION", "ground_speed_m3h_per_m3": GROUND_SPEED_PER_M3, "P2": [], "P3": []}
    for R in (10, 12, 15, 20, 30):
        vol = 4 * math.pi * R ** 3 / 3
        t_d = next(h for h in lev["hulls"] if h["R_m"] == R and h["id"] == "full" and h["mask"] == 11)["design_T_K"]
        tabs = {}
        for fin in ("MLCCAg", "AlAOC", "lowe_night_0.05"):
            hid = "trim-30" if fin == "MLCCAg" else f"finish_{fin}"
            h = next(x for x in lev["hulls"] if x["R_m"] == R and x["mask"] == 11 and x["id"] == hid)
            tabs[fin] = D.threshold_table(R, h["tc_m"], h["alpha"], h["eps_day"], h["eps_night"])
        builds = []
        for mask in range(16):
            for hid, p_d in (("full", P_FULL), ("trim-30", p_trim)):
                _, o = L.build(R, p_d, t_d, mask)
                builds.append((mask, hid, "MLCCAg", p_d, o["mass_kg"], o["tc_m"]))
        for mask in (11, 15):
            for fin in ("AlAOC", "lowe_night_0.05"):
                h = next(x for x in lev["hulls"] if x["R_m"] == R and x["mask"] == mask and x["id"] == f"finish_{fin}")
                builds.append((mask, "trim-30", fin, h["design_load_Pa"], h["mass_kg"], h["tc_m"]))
        for mask, hid, fin, p_d, mass, tc in builds:
            mo = modes(vol, s, p_d)
            tab = tabs[fin]
            c_floor = cold_masks(s, tab, mo["T_floor"])
            c_climb = cold_masks(s, tab, mo["T_climb"])
            ok = s["ok"]
            sets = {}
            lift_none = (mo["L_none"] >= mass) & mo["none_ok"]
            lift_trim = mo["L_trim"] >= mass
            lift_climb = mo["L_climb"] >= mass
            fo, Tfree, zfree, prel_free = free_float(vol, s, mass, p_d)
            c_free = cold_masks(s, tab, Tfree)
            for v, idx in (("primary", 0), ("cloud_aware", 1)):
                sets[("none", v)] = lift_none & c_floor[idx] & ok
                if hid != "full":
                    tr = lift_trim & c_floor[idx]
                    cl = lift_climb & c_climb[idx]
                    sets[("trim", v)] = tr & ok
                    sets[("climb", v)] = cl & ok
                    sets[("best", v)] = (tr | cl) & ok
                    # floating free it rises to rho V = M; that is feasible only where its load there is within design
                    # (equivalently where the climb test passes), and it meets the colder air of that altitude
                    sets[("free", v)] = fo & (prel_free <= 1e-6) & c_free[idx] & ok
            for (st, v), ib in sets.items():
                row = {"R_m": R, "mask": mask, "hull": hid, "finish": fin, "design_load_Pa": p_d, "mass_kg": mass,
                       "set": st, "variant": v, **D.metrics(ib, s)}
                row.pop("by_month") if not (mask in (11, 15) and v == "primary") else None
                if v == "primary" and mask in (11, 15) and st in ("trim", "climb", "best"):
                    chosen = (lift_trim & c_floor[0]) if st != "climb" else np.zeros_like(ib)
                    if st == "best":
                        chosen = (lift_trim & c_floor[0]) & ~(lift_climb & c_climb[0])
                    row["air_dump"] = stats_trim(s, ib, mo, mass, vol, True, chosen if st != "trim" else np.ones_like(ib))
                    row["ballast_dump"] = stats_trim(s, ib, mo, mass, vol, False, chosen if st != "trim" else np.ones_like(ib))
                    zc = mo["z_climb"][ib & (lift_climb & c_climb[0]) & (mo["z_climb"] > 100.5)]
                    row["climb_height_m"] = pct(zc - 100.0) if zc.size else None
                    row["climb_hours_fraction"] = float(zc.size / max(1, ib.sum()))
                if v == "primary" and mask in (11, 15) and st == "free":
                    row["free_altitude_m"] = pct(zfree[ib])
                    row["free_vs_climb_lift_test_mismatch_hours"] = int(np.sum((fo & (prel_free <= 1e-6) & ok) != (lift_climb & ok)))
                res["P2"].append(row)
            print(R, mask, hid, fin, round(mass, 1), {f"{k[0]}:{k[1][:3]}": round(float(D.metrics(v_, s)["full_day_fraction"]), 3)
                                                      for k, v_ in sets.items() if k[1] == "primary"}, round(time.time() - t0, 1), flush=True)
        for sel in ["baseline"] + [f"mask{k}" for k in range(16)]:
            hh = hulls3[(R, sel)]["hull"]
            v3 = vol - hh.v_sag
            for hid, p_d in [("full", P_FULL)] + [(f"design{dp:+d}", loads[dp]) for dp in (-30, -20, -10, 0, 10)]:
                mass = hh.mass(p_d)
                mo = modes(v3, s, p_d)
                ok = s["ok"]
                sets = {"none": ((mo["L_none"] >= mass) & mo["none_ok"]) & ok}
                if hid != "full":
                    sets["trim"] = (mo["L_trim"] >= mass) & ok
                    sets["climb"] = (mo["L_climb"] >= mass) & ok
                for st, ib in sets.items():
                    row = {"R_m": R, "selection": sel, "hull": hid, "design_load_Pa": p_d, "mass_kg": mass, "set": st,
                           "variant": "primary", **D.metrics(ib, s)}
                    if not (sel in ("mask15", "mask11") and hid == "design-30"):
                        row.pop("by_month")
                    if sel in ("mask15", "mask11") and hid in ("design-30", "design+0") and st in ("trim", "climb"):
                        chosen = np.ones_like(ib) if st == "trim" else np.zeros_like(ib)
                        row["air_dump"] = stats_trim(s, ib, mo, mass, v3, True, chosen)
                        row["ballast_dump"] = stats_trim(s, ib, mo, mass, v3, False, chosen)
                        zc = mo["z_climb"][ib & (mo["z_climb"] > 100.5)]
                        row["climb_height_m"] = pct(zc - 100.0) if (st == "climb" and zc.size) else None
                    res["P3"].append(row)
        print(R, "P3 done", round(time.time() - t0, 1), flush=True)
    (RUNS / "days058b.json").write_text(json.dumps(res, indent=1))
    print("DONE", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
