#!/usr/bin/env python3
"""MAINLINE-021b: the least-set search of MAINLINE-021 re-run on MAINLINE-019's optimistic reserve, with the thin face
taken as SR-200 rolled sheet at its own sourced properties (MAINLINE-020; Materion SR-200 datasheet), and with the
panel-size and bond-film optimisms inside 019's reserve named and searched like the others.

Own arithmetic, vectorised. Pinned inputs are hashed before use (INPUTS.json lists them).

THE MASS LINE (019's, re-implemented): reserve M; S = (L0 - 100 - M)/1.05 is faces plus core; joints keep their 0.05*S
allowance and only joint mass above it is charged into M. 019's optimistic scenario fixes every other item (sealed
service, 0.1 mm water, contamination, +10 K / 1 percent / 1 kPa climate, internal air): their sum is read from 019's
RESULTS. M is made self-consistent at every geometry: M = fixed items + max(0, joints - 0.05*S), with
joints = (2A/w)*[2*b*tf*rho_f + 2*b*t_adh*rho_adh + tc*w_splice*rho_splice] + 2A*film (019's formula, its optimistic b,
t_adh, w_splice and densities).

THE FIVE OPTIMISMS (today -> full; usage u = log-share of that stretch a point needs, 0 = not needed, 1 = full):
  O1 gamma: CR-1457 0.20 below Vc 2 and 1 above -> 018 optimistic curve 0.20 + 0.40*min(Vc, 2) (PROJECTION)
  O2 honeycomb wrinkling coefficient: 0.33 (CR-1457 eq 2.2-14) -> 0.82 (eq 2.2-12, K_delta 0)
  O3 face strength: SR-200 datasheet minimum tensile yield 345 MPa, taken as compressive (the one sourced lot shows a
     compressive/tensile ratio of 0.99) -> 379.2 MPa, that lot's lower in-plane compressive yield (NASA CR-194164)
  O4 panel size (square-equivalent width w): today the largest published SR-200 stock, 609.6 x 1828.8 mm (listed for
     gauges of 0.059 inch and up; thinner stock is unspecified), w = 2ab/(a+b) -> 019's optimistic 4 m (PROJECTION)
  O5 face/core bond film per bond: today 0.030 lb/ft2 (019's conservative weight) -> 0.015 lb/ft2 (019's optimistic,
     the lightest published 3M AF 163 weight; Be bonding unqualified)
For every subset S: minimise max_{i in S} u_i over core (014b's honeycomb table), core-mass fraction, and the O4/O5
grid, with every optimism outside S at today's value and crimp, crush and dimpling at SF >= 1 untouched.
Run: python3 -I float021b.py
"""
import datetime
import hashlib
import itertools
import json
import math
import os
import sys

import numpy as np

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pins():
    out = {}
    for key, (path, want) in PINS.items():
        got = sha256(path)
        if not got.startswith(want):
            sys.exit(f"PIN MISMATCH {key}: {got}")
        out[key] = {"path": path, "sha256": got, "bytes": os.path.getsize(path)}
    return out


PIN_RECORDS = verify_pins()
I019 = json.load(open(PINS["019_inputs"][0]))
R019 = json.load(open(PINS["019_results"][0]))
I014B = json.load(open(PINS["014b_inputs"][0]))
BE = json.load(open(PINS["be_sources"][0]))
R021 = json.load(open(PINS["021_rev1_results"][0]))

# ---------------------------------------------------------------- case and 019's optimistic scenario (read, not retyped)
CASE = I019["case"]
R, NU, P0, L0 = CASE["radius_m"], CASE["nu"], CASE["p0_Pa"], CASE["lift0_kg"]
SYS, J = CASE["system_allowance_kg"], CASE["joint_fraction"]
A = 4.0 * math.pi * R * R
OPT = I019["scenarios"]["optimistic"]
CONS = I019["scenarios"]["conservative"]
LINES = R019["scenarios"]["optimistic"]["budgets"]["aluminium"]["lines"]
M_FIXED = sum(v for k, v in LINES.items() if k != "joints_and_bondfilm_excess_kg")   # every optimistic item but joints
M_019 = R019["scenarios"]["optimistic"]["margin_kg"]                                 # 535.9459, the common reserve
LB_FT2 = 0.45359237 / 0.09290304                                                       # kg/m2 per lb/ft2
ROOT = math.sqrt(1.0 - NU * NU)

# the face: SR-200 rolled sheet at its own sourced properties
SR200 = next(g for g in BE["grades"] if g.get("grade") == "SR-200")
LOT = [g for g in BE["grades"] if (g.get("grade") or "").startswith("SR-200 (cross-rolled sheet, 1.96 mm")]
FACE = {"name": "SR-200 rolled beryllium sheet", "rho": SR200["density_kg_m3"], "E_Pa": SR200["E_Pa"],
        "sigma_today_Pa": SR200["tensile_yield_Pa"],
        "sigma_full_Pa": min(g["compressive_yield_Pa"] for g in LOT), "E_full_Pa": min(g["E_Pa"] for g in LOT)}
# O4 and O5 today/full
STOCK_A, STOCK_B = 0.6096, 1.8288                                  # Materion SR-200 datasheet maximum stock (020, 019)
W_TODAY = 2.0 * STOCK_A * STOCK_B / (STOCK_A + STOCK_B)             # square-equivalent: equal seam length per area
W_FULL = OPT["panel_width_m"]
F_TODAY, F_FULL = CONS["bondfilm_lb_ft2"], OPT["bondfilm_lb_ft2"]
K_TODAY, K_FULL = 0.33, 0.82


def biax():
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid ** 3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


BIAX = biax()


# ---------------------------------------------------------------- vectorised geometry and modes
def geometry(core, F, w, film, face_rho, fixed_M=None, iters=8):
    """Self-consistent mass line for an array of core-mass fractions F."""
    M = np.full_like(F, M_019 if fixed_M is None else fixed_M, dtype=float)
    for _ in range(1 if fixed_M is not None else iters):
        S = (L0 - SYS - M) / (1.0 + J)
        tc = F * S / (A * core["rho"])
        tf = (1.0 - F) * S / (2.0 * A * face_rho)
        seam = (2.0 * A / w) * (2.0 * OPT["strip_width_m"] * tf * face_rho
                                + 2.0 * OPT["strip_width_m"] * OPT["seam_adhesive_m"] * OPT["rho_adhesive_kg_m3"]
                                + tc * OPT["core_splice_width_m"] * OPT["rho_splice_kg_m3"])
        filmkg = 2.0 * A * film * LB_FT2
        excess = np.maximum(0.0, seam + filmkg - J * S)
        if fixed_M is None:
            M = M_FIXED + excess
    return {"S": S, "tc": tc, "tf": tf, "M": M, "seam": seam, "film": filmkg, "excess": excess, "allowance": J * S}


def modes(core, tf, tc, E, sigma, gamma_kind, k):
    h = tc + tf
    sigma0 = E * h / (R * ROOT)
    scrimp = h * h * core["Gc_Pa"] / (2.0 * tf * tc)
    vc = sigma0 / scrimp
    stiff = vc <= 2.0
    kc = np.where(stiff, 1.0 - vc / 4.0, 1.0 / vc)
    if gamma_kind == "handbook":
        gam = np.where(vc < 2.0, 0.20, 1.0)
    elif gamma_kind == "optimistic":
        gam = 0.20 + 0.40 * np.minimum(vc, 2.0)
    elif gamma_kind == "conservative":
        gam = np.full_like(vc, 0.20)
    else:
        gam = np.full_like(vc, float(gamma_kind))
    membrane = P0 * R / (4.0 * tf)
    wr = BIAX * k * np.sqrt(E * core["Ec_Pa"] * tf / tc) / membrane
    out = {"Vc": vc, "Kc": kc, "gamma": gam, "h": h,
           "global_buckling": 4.0 * gam * kc * sigma0 * tf / R / P0,
           "face_compression": 4.0 * sigma * tf / R / P0,
           "core_shear_crimping": 4.0 * scrimp * tf / R / P0,
           "core_crush": np.full_like(vc, core["crush_Pa"] / (P0 / 2.0)),
           "face_wrinkling": wr}
    if core.get("s_cell_m"):
        out["intracell_dimpling"] = 0.5 * 2.0 * E / (1.0 - NU * NU) * (tf / core["s_cell_m"]) ** 2 / membrane
    return out


MODE_KEYS = ("global_buckling", "face_compression", "core_shear_crimping", "core_crush", "face_wrinkling",
             "intracell_dimpling")


def least(ev):
    arr = np.vstack([ev[k] for k in MODE_KEYS if k in ev])
    return arr.min(axis=0)


def usage(needed, today, full):
    needed = np.asarray(needed, dtype=float)
    today = np.asarray(today, dtype=float) * np.ones_like(needed)
    full = np.asarray(full, dtype=float) * np.ones_like(needed)
    u = np.zeros_like(needed)
    need = needed > today * (1.0 + 1e-12)
    room = full > today * (1.0 + 1e-12)
    with np.errstate(divide="ignore", invalid="ignore"):
        val = np.log(needed / today) / np.log(full / today)
    u = np.where(need & room, val, np.where(need & ~room, np.inf, 0.0))
    return u


# ---------------------------------------------------------------- reproduction checks
def optimise_family(core, E, sigma, gamma_kind, k, fixed_M, n=100001):
    """019's way: the least SF over the fraction with 019's UNIAXIAL dimpling (twice this card's biaxial value),
    a 100001-point grid, then a golden refinement around the best grid point."""
    def least_of(F):
        g = geometry(core, F, OPT["panel_width_m"], OPT["bondfilm_lb_ft2"], 1850.0, fixed_M=fixed_M)
        ev = modes(core, g["tf"], g["tc"], E, sigma, gamma_kind, k)
        if "intracell_dimpling" in ev:
            ev["intracell_dimpling"] = 2.0 * ev["intracell_dimpling"]
        return least(ev), g
    F = np.linspace(1e-6, 1 - 1e-6, n)
    lst, _ = least_of(F)
    i = int(np.argmax(lst))
    lo, hi = F[max(i - 1, 0)], F[min(i + 1, n - 1)]
    gr = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        a, b = hi - gr * (hi - lo), lo + gr * (hi - lo)
        if least_of(np.array([a]))[0][0] < least_of(np.array([b]))[0][0]:
            lo = a
        else:
            hi = b
    f = 0.5 * (lo + hi)
    val, g = least_of(np.array([f]))
    if val[0] < lst[i]:
        f, val, g = F[i], lst[i:i + 1], least_of(F[i:i + 1])[1]
    return {"least": float(val[0]), "tf_m": float(g["tf"][0]), "core_m": float(g["tc"][0]), "fraction": float(f)}


def checks():
    out = {}
    cores019 = I019["cores"]
    face019 = I019["face"]
    # 019's two family optima on its fixed common reserve, S-200F 303 GPa / 283 MPa, handbook gamma, 0.33, 019's
    # uniaxial dimpling (the 2x factor above undoes this card's biaxial halving, for the reproduction only)
    for fam, want in (("aluminium", 0.556669198), ("aramid", 0.608701338)):
        r = optimise_family(cores019[fam], face019["E_Pa"], face019["sigma_Pa"], "handbook", 0.33, M_019)
        out[f"019_{fam}_least"] = {"mine": r["least"], "sealed": want, "tf_m": r["tf_m"], "core_m": r["core_m"],
                                   "result": "PASS" if abs(r["least"] - want) < 2e-6 else "FAIL"}
    # 019's joint excess at its aluminium point, from that point's own tf and tc
    pt = R019["scenarios"]["optimistic"]["points"]["aluminium"]
    S = (L0 - SYS - M_019) / (1.0 + J)
    seam = (2.0 * A / OPT["panel_width_m"]) * (2.0 * OPT["strip_width_m"] * pt["tf_m"] * 1850.0
                                               + 2.0 * OPT["strip_width_m"] * OPT["seam_adhesive_m"] * OPT["rho_adhesive_kg_m3"]
                                               + pt["core_m"] * OPT["core_splice_width_m"] * OPT["rho_splice_kg_m3"])
    excess = seam + 2.0 * A * OPT["bondfilm_lb_ft2"] * LB_FT2 - J * S
    out["019_joint_excess_aluminium"] = {"mine": excess, "sealed": LINES["joints_and_bondfilm_excess_kg"],
                                         "result": "PASS" if abs(excess - LINES["joints_and_bondfilm_excess_kg"]) < 1e-6 else "FAIL"}
    out["019_reserve_rebuilt"] = {"mine": M_FIXED + excess, "sealed": M_019,
                                  "result": "PASS" if abs(M_FIXED + excess - M_019) < 1e-6 else "FAIL"}
    # 021-rev1's least set at the 5 percent line with S-200F 290 GPa / 283 MPa: largest usage 0.958099...
    sealed = R021["main"]["least_set"]["min_max_usage"]
    core = next(c for c in I014B["cores_eligible"] if c["name"] == "Hexcel CR-III 5056 3/8-1.0")
    F = np.array([R021["main"]["least_set"]["fraction"]])
    g = geometry(core, F, 4.0, 0.015, 1850.0, fixed_M=0.05 * L0)
    ev = modes(core, g["tf"], g["tc"], 290e9, 283e6, "handbook", 0.33)
    g_need = 0.20 / ev["global_buckling"]
    u1 = usage(g_need, 0.20, 0.20 + 0.40 * np.minimum(ev["Vc"], 2.0))[0]
    out["021_rev1_least_set_usage"] = {"mine": float(u1), "sealed": sealed,
                                       "result": "PASS" if abs(u1 - sealed) < 1e-9 else "FAIL"}
    return out


# ---------------------------------------------------------------- MAINLINE-015's tolerance map (kd.py), as in 021
def tolerance(h, kd):
    t_eq = math.sqrt(3.0) * h
    root = (12.0 * (1.0 - 0.3 ** 2)) ** 0.25 * math.sqrt(R / t_eq)
    out = {"kd": kd, "t_eq_mm": t_eq * 1000.0, "R_over_t_eq": R / t_eq, "in_fit_range": 100.0 <= R / t_eq <= 1550.0}
    ratio = (kd - 0.45) / 0.51
    if ratio <= 0.0 or ratio >= 1.0:
        out.update({"status": "outside the Eq 3 inversion (floor 0.45)", "amplitude_mm": None, "rms_worst_mm": None})
        return out
    dbar = -math.log(ratio) / 3.88
    out.update({"status": "lambda_I_1 inversion", "delta_over_t_eq": dbar, "amplitude_mm": dbar * t_eq * 1000.0,
                "rms_worst_mm": dbar * t_eq * (2.625 / root) / math.sqrt(8.0) * 1000.0})
    return out


def search_fixed_M(cores, M, nfrac=4000):
    """019's optimistic reserve taken as given (535.95 kg, its 4 m panels and 0.015 lb/ft2 films already inside it):
    the subsets of O1-O3 only, with the SR-200 face."""
    F = np.linspace(1.0 / nfrac, 1.0 - 1.0 / nfrac, nfrac - 1)
    names = ("O1_gamma", "O2_wrinkle", "O3_face_strength")
    subsets = [s for n in range(0, 4) for s in itertools.combinations(names, n)]
    best = {s: (math.inf, None) for s in subsets}
    for core in cores:
        g = geometry(core, F, W_FULL, F_FULL, FACE["rho"], fixed_M=M)
        ev = modes(core, g["tf"], g["tc"], FACE["E_Pa"], FACE["sigma_today_Pa"], "handbook", K_TODAY)
        vc = ev["Vc"]
        g_today = np.where(vc < 2.0, 0.20, 1.0)
        u = {"O1_gamma": usage(g_today / ev["global_buckling"], g_today, 0.20 + 0.40 * np.minimum(vc, 2.0)),
             "O2_wrinkle": usage(K_TODAY / ev["face_wrinkling"], K_TODAY, K_FULL),
             "O3_face_strength": usage(FACE["sigma_today_Pa"] / ev["face_compression"], FACE["sigma_today_Pa"], FACE["sigma_full_Pa"])}
        ok = np.vstack([ev[k] for k in ("core_shear_crimping", "core_crush", "intracell_dimpling") if k in ev]).min(axis=0) >= 1.0
        for s in subsets:
            mask = ok.copy()
            for nm in names:
                if nm not in s:
                    mask &= u[nm] == 0.0
            parts = [u[nm] for nm in s]
            score = np.vstack(parts).max(axis=0) if parts else np.zeros_like(F)
            score = np.where(mask, score, np.inf)
            k = int(np.argmin(score))
            if score[k] < best[s][0]:
                best[s] = (float(score[k]), {"core": core["name"], "fraction": float(F[k]), "tf_m": float(g["tf"][k]),
                                             "core_m": float(g["tc"][k]), "Vc": float(vc[k]),
                                             "needed_gamma": float(max(g_today[k], g_today[k] / ev["global_buckling"][k])),
                                             "needed_wrinkle": float(max(K_TODAY, K_TODAY / ev["face_wrinkling"][k]))})
    return [{"subset": list(s), "min_max_usage": None if math.isinf(best[s][0]) else best[s][0],
             "feasible_within_named": best[s][0] <= 1.0, "point": best[s][1]} for s in subsets]


# ---------------------------------------------------------------- the search
NAMES = ("O1_gamma", "O2_wrinkle", "O3_face_strength", "O4_panel_size", "O5_bond_film")


def point_arrays(core, F, w, film):
    g = geometry(core, F, w, film, FACE["rho"])
    ev = modes(core, g["tf"], g["tc"], FACE["E_Pa"], FACE["sigma_today_Pa"], "handbook", K_TODAY)
    vc = ev["Vc"]
    g_today = np.where(vc < 2.0, 0.20, 1.0)
    g_full = 0.20 + 0.40 * np.minimum(vc, 2.0)
    u = {"O1_gamma": usage(g_today / ev["global_buckling"], g_today, g_full),
         "O2_wrinkle": usage(K_TODAY / ev["face_wrinkling"], K_TODAY, K_FULL),
         "O3_face_strength": usage(FACE["sigma_today_Pa"] / ev["face_compression"], FACE["sigma_today_Pa"],
                                   FACE["sigma_full_Pa"])}
    hard = np.vstack([ev[k] for k in ("core_shear_crimping", "core_crush", "intracell_dimpling") if k in ev]).min(axis=0)
    return g, ev, u, hard >= 1.0


def search(cores, nw=24, nf=24, nfrac=2000):
    F = np.linspace(1.0 / nfrac, 1.0 - 1.0 / nfrac, nfrac - 1)
    subsets = [s for n in range(0, 6) for s in itertools.combinations(NAMES, n)]
    best = {s: (math.inf, None) for s in subsets}
    for i in range(nw + 1):
        w = W_TODAY * (W_FULL / W_TODAY) ** (i / nw)
        for j in range(nf + 1):
            film = F_TODAY * (F_FULL / F_TODAY) ** (j / nf)
            for core in cores:
                g, ev, u, ok = point_arrays(core, F, w, film)
                for s in subsets:
                    if "O4_panel_size" not in s and i != 0:
                        continue
                    if "O5_bond_film" not in s and j != 0:
                        continue
                    mask = ok.copy()
                    for nm in ("O1_gamma", "O2_wrinkle", "O3_face_strength"):
                        if nm not in s:
                            mask &= u[nm] == 0.0
                    if not mask.any():
                        continue
                    parts = [u[nm] for nm in ("O1_gamma", "O2_wrinkle", "O3_face_strength") if nm in s]
                    if "O4_panel_size" in s:
                        parts.append(np.full_like(F, i / nw))
                    if "O5_bond_film" in s:
                        parts.append(np.full_like(F, j / nf))
                    score = np.vstack(parts).max(axis=0) if parts else np.zeros_like(F)
                    score = np.where(mask, score, np.inf)
                    k = int(np.argmin(score))
                    if score[k] < best[s][0]:
                        best[s] = (float(score[k]), {"core": core["name"], "fraction": float(F[k]), "w": w, "film": film,
                                                     "i": i, "j": j})
    return subsets, best


def describe(core, fraction, w, film):
    F = np.array([fraction])
    g, ev, u, ok = point_arrays(core, F, w, film)
    vc = float(ev["Vc"][0])
    g_today = 0.20 if vc < 2.0 else 1.0
    g_full = 0.20 + 0.40 * min(vc, 2.0)
    need = {"gamma": max(g_today, g_today / float(ev["global_buckling"][0])),
            "wrinkle": max(K_TODAY, K_TODAY / float(ev["face_wrinkling"][0])),
            "face_strength_Pa": max(FACE["sigma_today_Pa"], FACE["sigma_today_Pa"] / float(ev["face_compression"][0]))}
    def at(gamma_kind, k, sigma, E):
        e = modes(core, g["tf"], g["tc"], E, sigma, gamma_kind, k)
        sfs = {kk: float(e[kk][0]) for kk in MODE_KEYS if kk in e}
        lm = min(sfs, key=sfs.get)
        return {"gamma": float(e["gamma"][0]), "sfs": sfs, "least_SF": sfs[lm], "governing": lm}
    tf, tc, S, M = float(g["tf"][0]), float(g["tc"][0]), float(g["S"][0]), float(g["M"][0])
    faces = 2.0 * A * tf * FACE["rho"]
    return {
        "core": core["name"], "core_tag": core["tag"], "core_rho_kg_m3": core["rho"], "core_Ec_Pa": core["Ec_Pa"],
        "core_Gc_Pa": core["Gc_Pa"], "core_crush_Pa": core["crush_Pa"], "core_cell_m": core.get("s_cell_m"),
        "core_mass_fraction": fraction, "panel_width_m": w, "bond_film_lb_ft2": film,
        "R_m": R, "tf_m": tf, "core_m": tc, "h_m": tf + tc,
        "masses_kg": {"faces": faces, "core": A * tc * core["rho"], "joint_allowance_0.05S": J * S,
                      "joint_seams": float(g["seam"][0]), "joint_bond_films": float(g["film"]),
                      "joint_excess_in_reserve": float(g["excess"][0]), "systems_allowance": SYS,
                      "reserve_total": M, "reserve_fixed_items": M_FIXED,
                      "total": faces + A * tc * core["rho"] + J * S + SYS + M, "lift": L0},
        "Vc": vc, "branch": "stiff_or_moderate_core" if vc <= 2.0 else "shear_crimping",
        "needed_values": need, "today_values": {"gamma": g_today, "wrinkle": K_TODAY, "face_strength_Pa": FACE["sigma_today_Pa"],
                                                "panel_width_m": W_TODAY, "bond_film_lb_ft2": F_TODAY},
        "full_values": {"gamma": g_full, "wrinkle": K_FULL, "face_strength_Pa": FACE["sigma_full_Pa"],
                        "panel_width_m": W_FULL, "bond_film_lb_ft2": F_FULL},
        "usage": {"O1_gamma": float(u["O1_gamma"][0]), "O2_wrinkle": float(u["O2_wrinkle"][0]),
                  "O3_face_strength": float(u["O3_face_strength"][0]),
                  "O4_panel_size": max(0.0, math.log(w / W_TODAY) / math.log(W_FULL / W_TODAY)),
                  "O5_bond_film": max(0.0, math.log(F_TODAY / film) / math.log(F_TODAY / F_FULL))},
        "today": at("handbook", K_TODAY, FACE["sigma_today_Pa"], FACE["E_Pa"]),
        "at_needed_values": at(need["gamma"] if vc < 2.0 else "handbook", need["wrinkle"], need["face_strength_Pa"], FACE["E_Pa"]),
        "at_full_named_set": at("optimistic", K_FULL, FACE["sigma_full_Pa"], FACE["E_full_Pa"]),
        "at_full_set_conservative_gamma": at("conservative", K_FULL, FACE["sigma_full_Pa"], FACE["E_full_Pa"]),
        "hard_modes_ok": bool(ok[0]),
        "tolerance_015_at_needed_gamma": tolerance(float(g["tf"][0] + g["tc"][0]), need["gamma"]) if vc <= 2.0 else None,
        "tolerance_015_at_018_curve": tolerance(float(g["tf"][0] + g["tc"][0]), g_full) if vc <= 2.0 else None,
        "reserve_at_today_panel_and_film_same_geometry_kg": float(M_FIXED + max(0.0,
            (2.0 * A / W_TODAY) * (2.0 * OPT["strip_width_m"] * float(g["tf"][0]) * FACE["rho"]
                                   + 2.0 * OPT["strip_width_m"] * OPT["seam_adhesive_m"] * OPT["rho_adhesive_kg_m3"]
                                   + float(g["tc"][0]) * OPT["core_splice_width_m"] * OPT["rho_splice_kg_m3"])
            + 2.0 * A * F_TODAY * LB_FT2 - J * float(g["S"][0]))),
    }


def refine(core, best_point, nw=24, nf=24, s=None, steps=16):
    """Finer grid around a coarse optimum: w and film within one coarse step, fraction to 1e-5."""
    i0, j0 = best_point["i"], best_point["j"]
    best = (math.inf, None)
    for a in range(-steps, steps + 1):
        ii = (i0 + a / steps)
        if ii < 0 or ii > nw:
            continue
        if "O4_panel_size" not in s and ii != 0:
            continue
        w = W_TODAY * (W_FULL / W_TODAY) ** (ii / nw)
        for b in range(-steps, steps + 1):
            jj = (j0 + b / steps)
            if jj < 0 or jj > nf:
                continue
            if "O5_bond_film" not in s and jj != 0:
                continue
            film = F_TODAY * (F_FULL / F_TODAY) ** (jj / nf)
            F = np.linspace(max(1e-6, best_point["fraction"] - 2e-3), min(1 - 1e-6, best_point["fraction"] + 2e-3), 401)
            g, ev, u, ok = point_arrays(core, F, w, film)
            mask = ok.copy()
            for nm in ("O1_gamma", "O2_wrinkle", "O3_face_strength"):
                if nm not in s:
                    mask &= u[nm] == 0.0
            parts = [u[nm] for nm in ("O1_gamma", "O2_wrinkle", "O3_face_strength") if nm in s]
            if "O4_panel_size" in s:
                parts.append(np.full_like(F, ii / nw))
            if "O5_bond_film" in s:
                parts.append(np.full_like(F, jj / nf))
            score = np.vstack(parts).max(axis=0) if parts else np.zeros_like(F)
            score = np.where(mask, score, np.inf)
            k = int(np.argmin(score))
            if score[k] < best[0]:
                best = (float(score[k]), {"fraction": float(F[k]), "w": w, "film": film})
    return best

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
