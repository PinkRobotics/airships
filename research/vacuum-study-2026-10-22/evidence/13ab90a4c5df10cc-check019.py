#!/usr/bin/env python3
"""MAINLINE-019 check: own arithmetic from the pinned inputs and the formulas the card states.

Checker seat ref-55cff924be25afe6f9dd. The owner's scripts (compute.py and the rest) are neither imported nor run.
The owner's RESULTS.json is read only by compare019.py, after these numbers exist.
Every value is QUESTIONABLE; nothing here is a certification.
"""
import datetime
import json
import math
import time
from pathlib import Path

import numpy as np

T0_LOCAL = datetime.datetime.now().astimezone().isoformat()
T0C = time.monotonic()
OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline019-check-1020"

# ---- pinned case (COMMON.md; 019 INPUTS case) --------------------------------------------------------
R = 10.0
P0 = 95460.83791390515
L0 = 4889.442150186961
T0 = 284.9
NU = 0.33
KD = 0.2
JF = 0.05
SYS_ALLOW = 100.0
A = 4 * math.pi * R ** 2
VOL = 4 / 3 * math.pi * R ** 3
# Be S-200F (009c / 014b pin; Materion sheet), Hexcel cores
FACE = {"rho": 1850.0, "E": 303e9, "sig": 283e6}
PSI = 6894.757293168361        # Pa
PCF = 16.018463373960138       # kg/m3
LBFT2 = 0.45359237 / 0.09290304  # kg/m2 per lb/ft2
CORES = {
    "aramid": {"name": "Hexcel HRH-10-4.8-32", "rho": 32.0, "Ec": 76e6, "Gc": 14e6, "crush": 1e6, "cell": 0.0048},
    "aluminium": {"name": "Hexcel CR-III 5056 1/4-1.6", "rho": 1.6 * PCF, "Ec": 30000 * PSI, "Gc": 10500 * PSI,
                  "crush": 50 * PSI, "cell": 0.25 * 0.0254},
}
# b^3 + b = 1, solved here
B = 0.5
for _ in range(200):
    B -= (B ** 3 + B - 1) / (3 * B ** 2 + 1)

SCEN = {
    "optimistic": {"hours": 24.0, "payload": 0.0, "p_int_frac": 0.01, "rho_w": 1000.0, "rho_adh": 1250.0,
                   "rho_spl": 1100.0, "systems": {"vacuum_hardware": 15.0, "power_package": 10.0, "controls": 5.0},
                   "pump_W": 0.0, "mon_W": 5.0, "battery": None, "w": 4.0, "strip": 0.06, "adh": 0.0002,
                   "splice": 0.0015, "film_lbft2": 0.015, "water": 0.0001, "contam": 5.0, "dT": 10.0, "dp": 0.01,
                   "e": 1000.0},
    "conservative": {"hours": 24.0, "payload": 0.0, "p_int_frac": 0.01, "rho_w": 1000.0, "rho_adh": 1250.0,
                     "rho_spl": 1100.0, "systems": {"vacuum_hardware": 223.0, "controls": 20.0},
                     "pump_W": 5500.0, "mon_W": 5.0, "battery": (150.0, 0.8, 0.9), "w": 0.6, "strip": 0.12,
                     "adh": 0.0003, "splice": 0.003, "film_lbft2": 0.030, "water": 0.001, "contam": 25.0,
                     "dT": 25.1, "dp": 0.02, "e": 6000.0},
}


# ---- the P2 sandwich model as the card states it ------------------------------------------------------
def geometry(S, f, core):
    tf = (1 - f) * S / (2 * A * FACE["rho"])
    tc = f * S / (A * CORES[core]["rho"])
    return tf, tc


def modes(core, tf, tc, kd=KD, E=None):
    E = FACE["E"] if E is None else E
    c = CORES[core]
    h = tc + tf
    s0 = E * h / (R * math.sqrt(1 - NU ** 2))
    scr = h * h * c["Gc"] / (2 * tf * tc)
    Vc = s0 / scr
    crimp_branch = Vc > 2
    Kc = np.where(crimp_branch, 1 / Vc, 1 - Vc / 4)
    gam = np.where(crimp_branch, 1.0, kd)
    fs = P0 * R / (4 * tf)
    md = {
        "global": 4 * gam * Kc * s0 * tf / (R * P0),
        "compression": 4 * FACE["sig"] * tf / (R * P0),
        "crush": np.broadcast_to(c["crush"] / (P0 / 2), np.shape(tf)),
        "crimp": 4 * scr * tf / (R * P0),
        "wrinkle": B * 0.33 * np.sqrt(E * c["Ec"] * tf / tc) / fs,
        "dimple": (2 * E / (1 - NU ** 2) * (tf / c["cell"]) ** 2) / fs,
    }
    return md, Vc, Kc, gam


def least(md):
    return np.minimum.reduce([np.asarray(v, float) for v in md.values()])


def optimise(core, M, kd=KD, E=None, n=400001):
    S = (L0 - SYS_ALLOW - M) / (1 + JF)
    f = np.linspace(1e-6, 1 - 1e-6, n)
    tf, tc = geometry(S, f, core)
    sf = least(modes(core, tf, tc, kd, E)[0])
    i = int(np.argmax(sf))
    a, b = f[max(i - 1, 0)], f[min(i + 1, n - 1)]
    g = (math.sqrt(5) - 1) / 2

    def F(x):
        t1, t2 = geometry(S, np.array([x]), core)
        return float(least(modes(core, t1, t2, kd, E)[0])[0])

    c_, d_ = b - g * (b - a), a + g * (b - a)
    fc, fd = F(c_), F(d_)
    for _ in range(100):
        if fc < fd:
            a, c_, fc = c_, d_, fd
            d_ = a + g * (b - a)
            fd = F(d_)
        else:
            b, d_, fd = d_, c_, fc
            c_ = b - g * (b - a)
            fc = F(c_)
    x = (a + b) / 2
    fbest = x if F(x) >= sf[i] else float(f[i])
    tf, tc = geometry(S, np.array([fbest]), core)
    md, Vc, Kc, gam = modes(core, tf, tc, kd, E)
    vals = {k: float(np.ravel(v)[0]) for k, v in md.items()}
    order = sorted(vals, key=vals.get)
    return {"core": core, "M_kg": M, "S_kg": S, "f": fbest, "tf_m": float(tf[0]), "tc_m": float(tc[0]),
            "Vc": float(np.ravel(Vc)[0]), "Kc": float(np.ravel(Kc)[0]), "gamma": float(np.ravel(gam)[0]),
            "SF": vals, "least_SF": vals[order[0]], "governs": order[0], "second": order[1],
            "faces_kg": (1 - fbest) * S, "core_kg": fbest * S, "joint_allow_kg": JF * S}


# ---- the budget ---------------------------------------------------------------------------------------
def climate(sc):
    ratio_T = T0 / (T0 + sc["dT"])
    dry = L0 * (1 - (1 - sc["dp"]) * ratio_T)
    hum = L0 * 0.378 * sc["e"] / P0 * ratio_T
    return dry, hum


def systems_total(sc, hours=None):
    hours = sc["hours"] if hours is None else hours
    tot = sum(sc["systems"].values())
    batt = 0.0
    if sc["battery"]:
        whkg, usable, eff = sc["battery"]
        batt = (sc["pump_W"] + sc["mon_W"]) * hours / (whkg * usable * eff)
    return tot + batt, batt


def joints(sc, tf, tc):
    per_len = 2 * sc["strip"] * tf * FACE["rho"] + 2 * sc["strip"] * sc["adh"] * sc["rho_adh"] + \
        tc * sc["splice"] * sc["rho_spl"]
    seams = 2 * A / sc["w"] * per_len
    films = 2 * A * sc["film_lbft2"] * LBFT2
    return seams, films


def items(sc, core, M, hours=None, sealed=False, extra_payload=0.0, E=None):
    o = optimise(core, M, E=E, n=100001)
    st, batt = (30.0, 0.0) if sealed else systems_total(sc, hours)
    seams, films = joints(sc, o["tf_m"], o["tc_m"])
    dry, hum = climate(sc)
    it = {"systems_excess": max(0.0, st - SYS_ALLOW), "joints_excess": max(0.0, seams + films - JF * o["S_kg"]),
          "water": sc["rho_w"] * A * sc["water"], "contamination": sc["contam"], "climate_dry": dry,
          "humidity": hum, "internal_air": sc["p_int_frac"] * L0, "payload": sc["payload"] + extra_payload}
    return sum(it.values()), it, o, {"systems_total": st, "battery": batt, "seams": seams, "films": films}


def solve_budget(sc, core, **kw):
    lo, hi = 0.0, L0 - SYS_ALLOW - 50.0
    for _ in range(80):
        mid = (lo + hi) / 2
        tot = items(sc, core, mid, **kw)[0]
        if tot > mid:
            lo = mid
        else:
            hi = mid
    return hi


def main():
    res = {"schema": 1, "card": "MAINLINE-019 CHECK", "unit": "vacuum-mainline019-check-1020",
           "seat": "ref-55cff924be25afe6f9dd", "questionable": True, "certification": False,
           "started_local": T0_LOCAL, "b_biaxial": B, "area_m2": A, "volume_m3": VOL,
           "aluminium_core_SI_from_datasheet_units": CORES["aluminium"]}
    # climate formula and its stated numbers
    res["climate"] = {}
    for name, sc in SCEN.items():
        dry, hum = climate(sc)
        res["climate"][name] = {"dry_loss_kg": dry, "humidity_loss_kg": hum,
                                "L_day_kg": L0 - dry - hum}
    res["climate"]["dT_25.1_alone_exact"] = L0 * (1 - T0 / (T0 + 25.1))
    res["climate"]["dT_25.1_alone_first_order"] = L0 * 25.1 / T0
    res["climate"]["old_5pct_short_by"] = res["climate"]["dT_25.1_alone_exact"] - 0.05 * L0
    # 009c-5 direct evaluation
    tf, tc = 0.000752430055433027, 0.020642305866854553
    md, Vc, Kc, gam = modes("aramid", np.array([tf]), np.array([tc]))
    res["direct_009c5"] = {"least": float(least(md)[0]), "Vc": float(Vc[0]), "SF": {k: float(np.ravel(v)[0]) for k, v in md.items()}}
    # budgets
    res["budgets"] = {}
    for name, sc in SCEN.items():
        Ms = {core: solve_budget(sc, core) for core in CORES}
        Mc = max(Ms.values())
        per = {}
        for core in CORES:
            tot, it, o, extra = items(sc, core, Mc)
            per[core] = {"own_fixed_point_kg": Ms[core], "items_on_common_line": it, "total_on_common_line": tot,
                         "left_over_kg": Mc - tot, "extra": extra, "opt": o}
        res["budgets"][name] = {"common_kg": Mc, "common_pct": 100 * Mc / L0, "setter": max(Ms, key=Ms.get),
                                "per_core": per}
    # the margin lines
    lines = {"0%": 0.0, "5%": 0.05 * L0, "optimistic": res["budgets"]["optimistic"]["common_kg"],
             "conservative": res["budgets"]["conservative"]["common_kg"]}
    res["lines"] = {k: {core: optimise(core, M) for core in CORES} for k, M in lines.items()}
    # maximum-pressure corner, fixed geometry
    res["max_pressure"] = {k: {core: res["lines"][k][core]["least_SF"] / (1 + SCEN[k]["dp"]) for core in CORES}
                           for k in ("optimistic", "conservative")}
    # slope 0 -> 5 % per 100 kg
    res["slope_0_5_per100kg"] = {core: (res["lines"]["0%"][core]["least_SF"] - res["lines"]["5%"][core]["least_SF"])
                                 / (0.05 * L0) * 100 for core in CORES}
    # panel widths at the common 5 % line: seams alone, and with films
    res["panel_limits_5pct"] = {}
    S5 = (L0 - SYS_ALLOW - 0.05 * L0) / (1 + JF)
    allow = JF * S5
    for name, sc in SCEN.items():
        for core in CORES:
            o = res["lines"]["5%"][core]
            per_len = 2 * sc["strip"] * o["tf_m"] * FACE["rho"] + 2 * sc["strip"] * sc["adh"] * sc["rho_adh"] + \
                o["tc_m"] * sc["splice"] * sc["rho_spl"]
            films = 2 * A * sc["film_lbft2"] * LBFT2
            w_seam = 2 * A * per_len / allow
            w_all = 2 * A * per_len / (allow - films) if allow > films else None
            res["panel_limits_5pct"][f"{name}|{core}"] = {"allowance_kg": allow, "w_seams_only_m": w_seam,
                                                          "w_with_films_m": w_all, "films_kg": films}
    # systems and vacuum route
    sc = SCEN["conservative"]
    st, batt = systems_total(sc)
    res["systems"] = {"conservative_total": st, "battery": batt, "optimistic_total": systems_total(SCEN["optimistic"])[0],
                      "battery_8h": systems_total(sc, 8.0)[1]}
    ceiling = 0.01 * P0
    res["vacuum"] = {
        "ceiling_Pa": ceiling,
        "allowed_gas_load_ref_Pa_m3_s": VOL * (ceiling * T0 / 320.0 - 10.0) / 86400.0,
        "ingress_1pct_day_Pa_m3_s": 0.01 * P0 * VOL / 86400.0,
        "speed_ref_m3_h": 0.01 * P0 * VOL / 86400.0 / ceiling * 3600,
        "speed_320K_m3_h": 0.01 * P0 * VOL / 86400.0 * 320.0 / T0 / ceiling * 3600,
        "pumpdown_min_kWh": VOL * P0 * (1 - 0.01 + 0.01 * math.log(0.01)) / 3.6e6,
    }
    # sensitivities as the card names them
    res["sensitivities"] = {}
    for tag, sc_name, kw in (("conservative_sealed", "conservative", {"sealed": True}),
                             ("conservative_8h", "conservative", {"hours": 8.0}),
                             ("optimistic_payload100", "optimistic", {"extra_payload": 100.0})):
        sc = SCEN[sc_name]
        Ms = {core: solve_budget(sc, core, **kw) for core in CORES}
        Mc = max(Ms.values())
        res["sensitivities"][tag] = {"common_kg": Mc, "common_pct": 100 * Mc / L0,
                                     "SF": {core: optimise(core, Mc)["least_SF"] for core in CORES}}
    # 290 GPa at the optimistic common line, re-optimised and at fixed geometry
    Mo = res["budgets"]["optimistic"]["common_kg"]
    res["E290"] = {"reoptimised": {core: optimise(core, Mo, E=290e9)["least_SF"] for core in CORES}}
    fixed = {}
    for core in CORES:
        o = res["lines"]["optimistic"][core]
        md = modes(core, np.array([o["tf_m"]]), np.array([o["tc_m"]]), E=290e9)[0]
        fixed[core] = float(least(md)[0])
    res["E290"]["fixed_geometry"] = fixed
    res["ended_local"] = datetime.datetime.now().astimezone().isoformat()
    res["elapsed_s"] = time.monotonic() - T0C
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "RESULTS.json").write_text(json.dumps(res, indent=1, default=float))
    print("wrote", OUT / "RESULTS.json", round(res["elapsed_s"], 1), "s")


if __name__ == "__main__":
    main()
