#!/usr/bin/env python3
"""MAINLINE-017 check. Own arithmetic. Does not call the owner's script.

P2 modes are the NASA CR-1457 relations stated on the MAINLINE-007b card
and used by MAINLINE-014: sigma_0, Vc, Kc, gamma_d, handbook crimp pressure,
honeycomb wrinkling 2.2-14 times the equibiaxial root of x^3 + x = 1.
Face yield is 4*sigma*tf/R. Crush is strength over p/2.
The mass line is the 002 sandwich ceiling: joints 5 percent, systems 100 kg.
P3 is the 011 axial-column scan. Geometry is re-optimised at every factor.
"""

import json
import math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import numpy as np

OWN = Path(
    "unpublished-local-ref:6769073de134f0f3"
    "/.ship/work/outputs/vacuum-mainline017-improvement-directions-1019/RESULTS.json"
)
P14 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline014-balanced-sandwich-1019/RESULTS.json"
)
P08 = Path(
    "unpublished-local-ref:b5eced3bc27be18f"
    "/.ship/work/outputs/vacuum-mainline008-material-gap-1019/RESULTS.json"
)

R = 10.0
P = 95460.83791390515
LIFT = 4889.442150186961
NU = 0.33
S1 = math.sqrt(1.0 - NU * NU)
A = 4.0 * math.pi * R * R
SANDWICH = (LIFT - 100.0) / 1.05
# Root of x^3 + x - 1 = 0. Equation 2.2-6 with equal stresses.
BIAX = 0.6823278038280193
KD = 0.20
WR = 0.33

FILM_KG = 97.515
SYS_P3 = 50.0
NODE_KG = 0.02
SIG_F = 1.5e9
T_F = 8.0e-5


def half_up(value, nd):
    q = Decimal(1).scaleb(-nd)
    return Decimal(format(value, ".20f")).quantize(q, rounding=ROUND_HALF_UP)


def tf_of(tc, rho_f, rho_c):
    return (SANDWICH / A - tc * rho_c) / (2.0 * rho_f)


def modes(tf, tc, E, sigma, Ec, Gc, crush, kd, wr):
    h = tc + tf
    sigma_0 = E * h / (R * S1)
    crimp_stress = h * h * Gc / (2.0 * tf * tc)
    vc = sigma_0 / crimp_stress
    if vc <= 2.0:
        kc = 1.0 - vc / 4.0
        gamma = kd
    else:
        kc = 1.0 / vc
        gamma = 1.0
    p_global = 4.0 * gamma * kc * sigma_0 * tf / R
    p_crimp = 4.0 * crimp_stress * tf / R
    p_yield = 4.0 * sigma * tf / R
    p_crush = 2.0 * crush
    uni = wr * E * math.sqrt(Ec * tf / (E * tc))
    p_wr = 4.0 * BIAX * uni * tf / R
    sfs = {
        "global_buckling": p_global / P,
        "core_shear_crimping": p_crimp / P,
        "face_yield": p_yield / P,
        "core_crush": p_crush / P,
        "face_wrinkling": p_wr / P,
    }
    governing = min(sfs, key=sfs.get)
    return sfs, sfs[governing], governing, vc


def best_p2(E, sigma, rho_f, Ec, Gc, crush, rho_c, kd, wr, n=4000):
    tc_max = min(SANDWICH / (A * rho_c) * 0.995, 0.45)
    tc = np.linspace(0.004, tc_max, n)
    tf = (SANDWICH / A - tc * rho_c) / (2.0 * rho_f)
    ok = tf > 1e-6
    h = tc + tf
    sigma_0 = E * h / (R * S1)
    crimp_stress = h * h * Gc / (2.0 * tf * tc)
    vc = sigma_0 / crimp_stress
    kc = np.where(vc <= 2.0, 1.0 - vc / 4.0, 1.0 / vc)
    gamma = np.where(vc <= 2.0, kd, 1.0)
    p_global = 4.0 * gamma * kc * sigma_0 * tf / R
    p_crimp = 4.0 * crimp_stress * tf / R
    p_yield = 4.0 * sigma * tf / R
    p_crush = 2.0 * crush
    uni = wr * E * np.sqrt(Ec * tf / (E * tc))
    p_wr = 4.0 * BIAX * uni * tf / R
    stack = np.vstack((p_global, p_crimp, p_yield, np.full_like(tc, p_crush), p_wr)) / P
    least = np.min(stack, axis=0)
    least = np.where(ok, least, -1.0)
    k = int(np.argmax(least))
    sfs, least_v, gov, vc_v = modes(
        float(tf[k]), float(tc[k]), E, sigma, Ec, Gc, crush, kd, wr
    )
    return {
        "tf": float(tf[k]),
        "tc": float(tc[k]),
        "least": least_v,
        "governing": gov,
        "sfs": sfs,
        "Vc": vc_v,
    }


def refine_p2(E, sigma, rho_f, Ec, Gc, crush, rho_c, kd, wr):
    coarse = best_p2(E, sigma, rho_f, Ec, Gc, crush, rho_c, kd, wr, n=2500)
    lo = max(0.003, coarse["tc"] * 0.85)
    hi = coarse["tc"] * 1.15
    best = coarse
    for _ in range(40):
        span = hi - lo
        grid = np.linspace(lo, hi, 400)
        local = None
        for tc in grid:
            tf = tf_of(float(tc), rho_f, rho_c)
            if tf <= 1e-6:
                continue
            sfs, least, gov, vc = modes(tf, float(tc), E, sigma, Ec, Gc, crush, kd, wr)
            if local is None or least > local["least"]:
                local = {
                    "tf": tf, "tc": float(tc), "least": least,
                    "governing": gov, "sfs": sfs, "Vc": vc,
                }
        best = local
        lo = max(0.003, best["tc"] - span / 8.0)
        hi = best["tc"] + span / 8.0
    return best


def reach(base_props, key, cap=1.0e4):
    """Multiply `key` by the factor, or divide a density. Bisect to least SF 1."""

    def apply(factor):
        props = dict(base_props)
        if key in ("rho_f", "rho_c"):
            props[key] = base_props[key] / factor
        else:
            props[key] = base_props[key] * factor
        return refine_p2(
            props["E"], props["sigma"], props["rho_f"], props["Ec"], props["Gc"],
            props["crush"], props["rho_c"], props["kd"], props["wr"],
        )

    top = apply(cap)
    if top["least"] < 1.0 - 1e-9:
        return {"status": "not_alone", "cap": top["least"], "governing": top["governing"], "at": top}
    lo, hi = 1.0, cap
    best = top
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        row = apply(mid)
        if row["least"] >= 1.0:
            hi = mid
            best = row
        else:
            lo = mid
    return {"status": "reaches", "factor": hi, "at": best, "cap": top["least"]}


def nodes(s):
    return 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s) + 2.0


def evaluate_p3(s, ro, rho, E, sigma, film_sig=SIG_F):
    v = nodes(s)
    m = 3.0 * v - 6.0
    mass = LIFT - FILM_KG - NODE_KG * v - SYS_P3
    area = mass / (m * s * rho)
    if ro * ro <= area / math.pi:
        return None
    ri2 = ro * ro - area / math.pi
    tw = ro - math.sqrt(ri2)
    inertia = math.pi / 4.0 * (ro ** 4 - ri2 * ri2)
    sfs = {
        "euler": (2.0 * math.pi ** 2 * E * inertia / (R * s ** 3)) / P,
        "yield": (2.0 * sigma * area / (R * s)) / P,
        "local": (2.0 * (0.6 * E * tw / ro) * area / (R * s)) / P,
        "film": (2.0 * film_sig * T_F / s) / P,
    }
    gov = min(sfs, key=sfs.get)
    return {"s": s, "ro": ro, "tw": tw, "A": area, "sfs": sfs, "least": sfs[gov], "governing": gov}


def best_p3_at_s(s, rho, E, sigma, film_sig=SIG_F, n=3000):
    v = nodes(s)
    m = 3.0 * v - 6.0
    mass = LIFT - FILM_KG - NODE_KG * v - SYS_P3
    if mass <= 0 or m <= 0:
        return None
    area = mass / (m * s * rho)
    ro_min = math.sqrt(area / math.pi) * 1.0000001
    ro_max = min(0.25, s / 3.0)
    if ro_max <= ro_min:
        return None
    ros = np.linspace(ro_min, ro_max, n)
    ri2 = ros * ros - area / math.pi
    tw = ros - np.sqrt(ri2)
    inertia = 0.5 * area * ros * ros - area * area / (4.0 * math.pi)
    euler = 2.0 * math.pi ** 2 * E * inertia / (R * s ** 3)
    yield_p = 2.0 * sigma * area / (R * s)
    local = 2.0 * (0.6 * E * tw / ros) * area / (R * s)
    film = 2.0 * film_sig * T_F / s
    least = np.minimum(np.minimum(euler, yield_p), np.minimum(local, np.full_like(ros, film)))
    k = int(np.argmax(least))
    return evaluate_p3(s, float(ros[k]), rho, E, sigma, film_sig)


def optimise_p3(rho, E, sigma, film_sig=SIG_F):
    best = None
    s = 0.40
    while s <= 3.0 + 1e-12:
        row = best_p3_at_s(s, rho, E, sigma, film_sig)
        if row is not None and (best is None or row["least"] > best["least"]):
            best = row
        s = round(s + 0.02, 10)
    return best


def reach_p3(rho, E, sigma, key):
    def apply(factor):
        rr, ee, ss, ff = rho, E, sigma, SIG_F
        if key == "rho":
            rr = rho / factor
        elif key == "E":
            ee = E * factor
        elif key == "sigma":
            ss = sigma * factor
        elif key == "film":
            ff = SIG_F * factor
        return optimise_p3(rr, ee, ss, ff)

    base = apply(1.0)
    if base is None:
        return {"status": "not_alone", "cap": 0.0, "governing": "no geometry"}
    if base["least"] >= 1.0:
        return {"status": "already", "factor": 1.0, "at": base}
    # A 1e4 density cut makes the tube thicker than the spacing cap. Probe a
    # moderate factor first; film and modulus still use the high cap.
    hi_probe = 4.0 if key == "rho" else 1.0e4
    top = apply(hi_probe)
    if top is None or top["least"] < 1.0:
        cap_row = top if top is not None else base
        return {"status": "not_alone", "cap": cap_row["least"], "governing": cap_row["governing"]}
    lo, hi = 1.0, hi_probe
    best = top
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        row = apply(mid)
        if row["least"] >= 1.0:
            hi = mid
            best = row
        else:
            lo = mid
    return {"status": "reaches", "factor": hi, "at": best}


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-30)


def main():
    theirs = json.loads(OWN.read_text())
    print("biaxial", BIAX, "sandwich", SANDWICH)
    # Classical identity: infinite G, kd 0.20, aluminium P2-E thicknesses.
    tf_e, tc_e = 0.0003360949703945902, 0.1134320525081742
    sfs, least, gov, vc = modes(tf_e, tc_e, 68.9e9, 276e6, 1e12, 1e15, 1e6, 0.20, 0.33)
    print("classical infinite-G least", least, "global", sfs["global_buckling"], "Vc", vc, "gov", gov)

    faces = {
        "CNT-yarn": dict(E=180e9, sigma=1200e6, rho_f=1400.0),
        "Be S-200F": dict(E=303e9, sigma=283e6, rho_f=1850.0),
        "graphene": dict(E=150e9, sigma=900e6, rho_f=1500.0),
    }
    core = dict(Ec=76e6, Gc=14e6, crush=1.0e6, rho_c=32.0, kd=KD, wr=WR)
    print("\nBASE")
    bases = {}
    for name, face in faces.items():
        props = {**face, **core}
        row = refine_p2(**{
            "E": props["E"], "sigma": props["sigma"], "rho_f": props["rho_f"],
            "Ec": props["Ec"], "Gc": props["Gc"], "crush": props["crush"],
            "rho_c": props["rho_c"], "kd": props["kd"], "wr": props["wr"],
        })
        bases[name] = (props, row)
        t = theirs["P2_points"][name]["base"]
        print(name, "least", row["least"], "theirs", t["least_SF"], "rel", rel(row["least"], t["least_SF"]))
        print("  gov", row["governing"], "Vc", row["Vc"], "tf", row["tf"], "tc", row["tc"])
        print("  theirs tf", t["tf_m"], "tc", t["core_m"], "gov", t["governing"])
        for key, value in t["sfs"].items():
            print(f"  {key} mine {row['sfs'][key]} theirs {value} rel {rel(row['sfs'][key], value)}")

    keys = ("E", "sigma", "rho_f", "Ec", "Gc", "crush", "rho_c", "kd", "wr")
    their_keys = {
        "E": "E_f", "sigma": "sigma_f", "rho_f": "rho_f", "Ec": "E_c", "Gc": "G_c",
        "crush": "core_crush", "rho_c": "rho_c", "kd": "kd", "wr": "wrinkling_coefficient",
    }
    print("\nFACTORS")
    for name, (props, _) in bases.items():
        print("==", name)
        block = theirs["P2_points"][name]["single_property"]
        for key in keys:
            got = reach(props, key)
            field = their_keys[key]
            spec = block[field]
            if got["status"] == "reaches":
                factor = got["factor"]
                print(
                    f"  {field} REACH {factor} theirs {spec.get('factor')} "
                    f"rel {rel(factor, spec.get('factor', 1))} gov {got['at']['governing']} "
                    f"least {got['at']['least']}"
                )
            else:
                print(
                    f"  {field} CAP {got['cap']} theirs {spec.get('cap_least_SF_at_1e4')} "
                    f"rel {rel(got['cap'], spec.get('cap_least_SF_at_1e4', 0))} "
                    f"gov {got['governing']} theirs {spec.get('cap_governing')}"
                )

    print("\nCOMBOS at stated geometry")
    for name, point in theirs["P2_points"].items():
        combo = point["cheapest_combination_found"]
        split = combo["split"]
        props = {**bases[name][0]}
        for key, factor in split.items():
            mapped = {"rho_f": "rho_f", "wrinkling_coefficient": "wr"}.get(key, key)
            if mapped in ("rho_f", "rho_c"):
                props[mapped] = bases[name][0][mapped] / factor
            else:
                props[mapped] = bases[name][0][mapped] * factor
        sfs, least, gov, vc = modes(
            combo["tf_m"], combo["core_m"], props["E"], props["sigma"], props["Ec"],
            props["Gc"], props["crush"], props["kd"], props["wr"],
        )
        product = 1.0
        for factor in split.values():
            product *= factor
        print(name, "stated product", combo["product_of_factors"], "split product", product)
        print("  least at stated tf/core", least, "theirs", combo["least_SF_on_grid"], "gov", gov)

    print("\nP3")
    p3 = {
        "SiC": (3100.0, 410e9, 3900e6),
        "CFRP T700": (1550.0, 54e9, 520e6),
    }
    for name, (rho, E, sigma) in p3.items():
        row = optimise_p3(rho, E, sigma)
        t = theirs["P3_points"][name]["base"]
        print(name, "least", row["least"], "theirs", t["least_SF"], "rel", rel(row["least"], t["least_SF"]))
        print("  s", row["s"], "ro", row["ro"], "tw", row["tw"], "gov", row["governing"])
        print("  theirs s", t["s_m"], "ro", t["r_o_m"], "tw", t["t_w_m"], "gov", t["governing"])
        for key in ("euler", "yield", "local", "film"):
            print(f"  {key} mine {row['sfs'][key]} theirs {t['sfs'][key]} rel {rel(row['sfs'][key], t['sfs'][key])}")
        for key, field in (("E", "E"), ("sigma", "sigma"), ("rho", "rho"), ("film", "film_allowable")):
            got = reach_p3(rho, E, sigma, key)
            spec = theirs["P3_points"][name]["single_property"][field]
            if got["status"] == "reaches":
                print(f"  {field} REACH {got['factor']} theirs {spec.get('factor')} rel {rel(got['factor'], spec.get('factor', 1))}")
            elif got["status"] == "already":
                print(f"  {field} ALREADY {got['at']['least']} theirs factor {spec.get('factor')} status {spec.get('status')}")
            else:
                print(f"  {field} CAP {got['cap']} theirs {spec.get('cap_least_SF_at_1e4')} gov {got['governing']}")

    data = json.loads(P14.read_text())
    ranked = sorted(
        (row["least_SF"], row["face"], row["core_density_kg_m3"], row["kd"])
        for row in data["optima"]
        if row["kd"] == 0.2 and row["core_density_kg_m3"] == 32.0
    )
    print("\n014 leaders at 32 kg/m3 kd 0.20, highest last")
    for row in ranked[-8:]:
        print(" ", row)

    # Densities the card states.
    print("\nDENSITY TARGETS")
    print("CNT", 1400 / 1.4591232219167407, "card 959.5")
    print("Be", 1850 / 1.637322535667118, "card 1129.7")
    print("graphene", 1500 / 1.6547089494882732, "card 906.5")
    print("T700 rho", 1550 / 1.3073708918971367, "card 1185.6")
    print("T700 sig", 520 * 1.3080514668285677, "card 680.2")
    print("CNT E GPa", 180 * 3.3068950443382388)
    print("CNT Ec MPa", 76 * 3.3068950443382388)
    print("graphene E", 150 * 4.92416299489463)
    print("wrinkle 0.33*1.818487020668071", 0.33 * 1.818487020668071)


if __name__ == "__main__":
    main()
