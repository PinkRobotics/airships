#!/usr/bin/env python3
"""MAINLINE-011b: P3 global lattice buckling and arc-member bending.

Unit vacuum-mainline011b-p3-global-arcs-1019.
Seat ref-2543c559b19ffce7dfdd. Own arithmetic. The 011 author's tree is not
written and its script is not executed. RESULTS.json is the measured run.
"""
import datetime
import hashlib
import json
import math
import os
import sys
import time
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(ROOT, "RESULTS.json")
ORIGIN_PATH = os.path.join(ROOT, "ORIGIN.json")
ZONE = ZoneInfo("America/Los_Angeles")

R = 10.0
P_EXT = 95460.8379139
L_MASS = 4889.44215019
RHO_AIR = 1.16726833075
NU_RECORD = 0.33
M_FILM_PIN = 97.515
M_NODE_UNIT = 0.02
M_SYS = 50.0
SIGMA_FILM = 1.5e9
T_FILM = 8e-5
RHO_FILM = 970.0
C_LOCAL = 0.6
JOINT_FRAC = 0.05
BAND_S = 3.0
N_RO = 4000
SLENDER = 3.0
C_TWO = 4.0
C_TRI = 4.0 * math.sqrt(1.5)  # 4*sqrt(D*Et) / (E*sqrt(I*A)/(s*R^2))

MATERIALS = {
    "6061-T6": (2700.0, 68.9e9, 276e6),
    "CFRP-QI-M55J-epoxy": (1640.0, 135e9, 350e6),
    "CFRP-QI-T700-epoxy": (1550.0, 54e9, 520e6),
    "CFRP-QI-K13D2U-epoxy": (1750.0, 210e9, 220e6),
    "SiC-alpha-Hexoloy-SA": (3100.0, 410e9, 3900e6),
    "CNT-yarn-QI-PROJECTION": (1400.0, 180e9, 1200e6),
}
P2E = {
    "SF_b_kd0.2": 0.233885578993,
    "SF_b_curve": 0.164568553708,
    "kd_curve": 0.140725695373,
    "kd_prior": 0.2,
}
KNOCKS = (1.0, 0.5, 0.4, 0.2)
GRIDS = (("equilateral_triangular", C_TRI), ("two_way", C_TWO))
S_ALL = [round(0.4 + 0.02 * i, 3) for i in range(301)]
S_BAND = [s for s in S_ALL if s <= BAND_S + 1e-12]

PINS = (
    (
        "unpublished-local-ref:786479f234a43198",
        "23f16c8770f9f2f26243b67d5fc5329bffb8fbc901664d7be1bf79b2b993695f",
        2180,
    ),
    (
        "withheld-source:b528d6a62c81ce0b",
        "8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5",
        5874,
    ),
    (
        "unpublished-local-ref:b40693bc2fdb6bdf",
        "14983c85c3495169b1bd4ab340f776ad6d4e93737b19623a7b483f440c5ff6ed",
        2021,
    ),
    (
        "unpublished-local-ref:2bf170d37c993460",
        "98c8d5b2988600fcaed430704fba2d16a25e165e5aad1998ef07550437165a3f",
        2063,
    ),
)

# 011 author's filed 6061 banded optimum. Regression target. Not rewritten.
PUBLISHED = {
    "s": 3.0,
    "r_o": 0.0866221663456903,
    "t_w": 0.002251568619368413,
    "A_m2": 0.0012095192717366963,
    "I_m4": 4.421336454767768e-06,
    "m_nodes_kg": 3.264532203083054,
    "m_tube_kg": 4738.662617986916,
    "SF_least": 0.23313387024769294,
    "SF_euler": 0.23329934624064913,
    "SF_yield": 0.23313387024769294,
    "SF_local": 0.9076594005918152,
    "SF_film": 0.8380399936585017,
    "binding": "yield",
}


def g(x):
    return format(x, ".12g")


def atomic_write(path, text):
    tmp = path + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        os.write(fd, text.encode())
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)
    dirfd = os.open(os.path.dirname(path), os.O_RDONLY)
    try:
        os.fsync(dirfd)
    finally:
        os.close(dirfd)


def pin_check():
    rows = []
    ok = True
    for path, sha, nbytes in PINS:
        data = open(path, "rb").read()
        got = hashlib.sha256(data).hexdigest()
        match = got == sha and len(data) == nbytes
        ok = ok and match
        rows.append({"path": path, "sha256": got, "bytes": len(data), "match": match})
        if not match:
            print("PIN DRIFT", path, got, len(data))
    return ok, rows


def mass_pack(s, joints):
    V = 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s) + 2.0
    m_nodes = M_NODE_UNIT * V
    members = 3.0 * V - 6.0
    budget = L_MASS - M_FILM_PIN - m_nodes - M_SYS
    if joints:
        m_tube = budget / (1.0 + JOINT_FRAC)
        m_joint = budget - m_tube
    else:
        m_tube = budget
        m_joint = 0.0
    return V, members, m_nodes, m_tube, m_joint, budget


def section(A, r_o):
    disc = r_o * r_o - A / math.pi
    if disc <= 0.0:
        return None
    r_i = math.sqrt(disc)
    t_w = r_o - r_i
    I = math.pi / 4.0 * (r_o ** 4 - r_i ** 4)
    return r_i, t_w, I


def mode_pack(rho, E, sig, s, r_o, A, use_detail):
    sec = section(A, r_o)
    if sec is None:
        return None
    r_i, t_w, I = sec
    p_yield = 2.0 * sig * A / (R * s)
    p_euler = 2.0 * math.pi ** 2 * E * I / (R * s ** 3)
    sig_loc = C_LOCAL * E * t_w / r_o
    p_local = 2.0 * sig_loc * A / (R * s)
    p_film = 2.0 * SIGMA_FILM * T_FILM / s
    rg2 = I / A
    eta = (s / 1000.0) * r_o / rg2
    sig_E = math.pi ** 2 * E * rg2 / (s * s)
    phi = (sig + (eta + 1.0) * sig_E) * 0.5
    discp = phi * phi - sig * sig_E
    if discp < 0.0:
        return None
    sig_cr = phi - math.sqrt(discp)
    sig_app = P_EXT * R * s / (2.0 * A)
    g_unit = E * math.sqrt(I * A) / (s * R * R)
    out = {
        "r_i": r_i,
        "t_w": t_w,
        "I": I,
        "rg": math.sqrt(rg2),
        "SF_yield": p_yield / P_EXT,
        "SF_euler": p_euler / P_EXT,
        "SF_local": p_local / P_EXT,
        "SF_film": p_film / P_EXT,
        "SF_perry": sig_cr / sig_app,
        "eta": eta,
        "sigma_E_Pa": sig_E,
        "sigma_cr_Pa": sig_cr,
        "sigma_axial_Pa": sig_app,
        "N_over_Ne": sig_app / sig_E,
        "g_unit_Pa": g_unit,
        "sigma_local_Pa": sig_loc,
    }
    if use_detail:
        out["p_yield_Pa"] = p_yield
        out["p_euler_Pa"] = p_euler
        out["p_local_Pa"] = p_local
        out["p_film_Pa"] = p_film
    return out


def base_least(pack, use_perry):
    pairs = (
        ("yield", pack["SF_yield"]),
        ("euler", pack["SF_euler"]),
        ("local", pack["SF_local"]),
        ("film", pack["SF_film"]),
    )
    name, sf = pairs[0]
    for cand, val in pairs[1:]:
        if val < sf:
            name, sf = cand, val
    if use_perry and pack["SF_perry"] < sf:
        name, sf = "perry", pack["SF_perry"]
    return name, sf


def scan(rho, E, sig, joints, use_perry, include_global):
    if include_global:
        variants = [
            {"grid": grid, "k": k, "factor": k * coeff}
            for grid, coeff in GRIDS
            for k in KNOCKS
        ]
    else:
        variants = [{"grid": "none", "k": None, "factor": None}]
    n_var = len(variants)
    per = [[] for _ in range(n_var)]
    for s in S_BAND:
        V, members, m_nodes, m_tube, m_joint, budget = mass_pack(s, joints)
        if m_tube <= 0.0 or members <= 0.0 or budget <= 0.0:
            continue
        A = m_tube / (members * s * rho)
        r_min = math.sqrt(A / math.pi) * 1.0001
        r_max = min(0.25, s / SLENDER)
        if r_max <= r_min:
            continue
        span = r_max - r_min
        denom = N_RO - 1
        best_sf = [-1.0] * n_var
        best = [None] * n_var
        p_film = 2.0 * SIGMA_FILM * T_FILM / s
        sf_f = p_film / P_EXT
        p_yield = 2.0 * sig * A / (R * s)
        sf_y = p_yield / P_EXT
        euler_coef = 2.0 * math.pi ** 2 * E / (R * s ** 3)
        inv = 1.0 / (R * s)
        for i in range(N_RO):
            r_o = r_min + span * i / denom
            disc = r_o * r_o - A / math.pi
            if disc <= 0.0:
                continue
            r_i = math.sqrt(disc)
            t_w = r_o - r_i
            I = math.pi * 0.25 * (r_o ** 4 - r_i ** 4)
            sf_e = euler_coef * I / P_EXT
            sig_loc = C_LOCAL * E * t_w / r_o
            sf_l = 2.0 * sig_loc * A * inv / P_EXT
            rg2 = I / A
            eta = (s * 0.001) * r_o / rg2
            sig_E = math.pi * math.pi * E * rg2 / (s * s)
            phi = (sig + (eta + 1.0) * sig_E) * 0.5
            discp = phi * phi - sig * sig_E
            if discp < 0.0:
                continue
            sig_cr = phi - math.sqrt(discp)
            sig_app = P_EXT * R * s / (2.0 * A)
            sf_p = sig_cr / sig_app
            g_unit = E * math.sqrt(I * A) / (s * R * R)
            name = "yield"
            base = sf_y
            if sf_e < base:
                name, base = "euler", sf_e
            if sf_l < base:
                name, base = "local", sf_l
            if sf_f < base:
                name, base = "film", sf_f
            if use_perry and sf_p < base:
                name, base = "perry", sf_p
            for j, var in enumerate(variants):
                factor = var["factor"]
                if factor is None:
                    gov, least, sf_g = name, base, None
                else:
                    sf_g = factor * g_unit / P_EXT
                    if sf_g < base:
                        gov, least = "global", sf_g
                    else:
                        gov, least = name, base
                if least > best_sf[j]:
                    best_sf[j] = least
                    best[j] = (
                        r_o, t_w, I, r_i, sf_e, sf_l, sf_p, g_unit, eta, sig_E,
                        sig_cr, sig_app, gov, least, sf_g, i, rg2,
                    )
        for j in range(n_var):
            if best[j] is None:
                continue
            per[j].append(
                {
                    "s": s,
                    "A": A,
                    "V": V,
                    "members": members,
                    "m_nodes": m_nodes,
                    "m_tube": m_tube,
                    "m_joint": m_joint,
                    "sf_y": sf_y,
                    "sf_f": sf_f,
                    "r_min": r_min,
                    "r_max": r_max,
                    "pack": best[j],
                }
            )
    picked = []
    for j, var in enumerate(variants):
        rows = per[j]
        if not rows:
            picked.append({"variant": var, "best": None, "next": []})
            continue
        ranked = sorted(rows, key=lambda item: -item["pack"][13])
        best_row = ranked[0]
        nxt = []
        for item in ranked[1:]:
            if all(abs(item["s"] - prev["s"]) > 0.5 for prev in [best_row] + nxt):
                nxt.append(item)
            if len(nxt) == 2:
                break
        picked.append({"variant": var, "best": best_row, "next": nxt})
    return picked


def chord_block(s, r_o, I, sig):
    w = P_EXT * s / 2.0
    sag = s * s / (8.0 * R)
    sag_ex = R - math.sqrt(R * R - (s / 2.0) ** 2)
    def stress(div):
        return (w * s * s / div) * r_o / I
    simple = stress(8.0)
    fixed = stress(12.0)
    mid = stress(24.0)
    return {
        "w_N_per_m": w,
        "sag_approx_m": sag,
        "sag_exact_m": sag_ex,
        "sag_exceeds_tube_radius": sag > r_o,
        "sigma_bend_simple_Pa": simple,
        "sigma_bend_fixed_end_Pa": fixed,
        "sigma_bend_fixed_mid_Pa": mid,
        "SF_bend_simple": sig / simple,
        "SF_bend_fixed_end": sig / fixed,
        "SF_bend_fixed_mid": sig / mid,
    }


def row_from(mat, rho, E, sig, joints, use_perry, item, variant):
    pack = item["pack"]
    (r_o, t_w, I, r_i, sf_e, sf_l, sf_p, g_unit, eta, sig_E,
     sig_cr, sig_app, gov, least, sf_g, i_ro, rg2) = pack
    sf_y = item["sf_y"]
    sf_f = item["sf_f"]
    pairs = [("yield", sf_y), ("euler", sf_e), ("local", sf_l), ("film", sf_f)]
    if use_perry:
        pairs.append(("perry", sf_p))
    if sf_g is not None:
        pairs.append(("global", sf_g))
    rest = sorted((p for p in pairs if p[0] != gov), key=lambda t: (t[1], t[0]))
    second_name, second_sf = rest[0]
    step = (item["r_max"] - item["r_min"]) / (N_RO - 1)
    return {
        "material": mat,
        "questionable": True,
        "grid": variant["grid"],
        "k": variant["k"],
        "joints_on": joints,
        "perry_scored": use_perry,
        "s_m": item["s"],
        "r_o_m": r_o,
        "r_i_m": r_i,
        "t_w_m": t_w,
        "A_m2": item["A"],
        "I_m4": I,
        "rg_m": math.sqrt(rg2),
        "nodes": item["V"],
        "members": item["members"],
        "m_film_kg": M_FILM_PIN,
        "m_nodes_kg": item["m_nodes"],
        "m_joint_kg": item["m_joint"],
        "m_tube_kg": item["m_tube"],
        "m_systems_kg": M_SYS,
        "total_kg": M_FILM_PIN + item["m_nodes"] + item["m_joint"] + item["m_tube"] + M_SYS,
        "SF_yield": sf_y,
        "SF_euler": sf_e,
        "SF_local": sf_l,
        "SF_film": sf_f,
        "SF_perry": sf_p,
        "SF_global": sf_g,
        "SF_global_two_way_perfect": C_TWO * g_unit / P_EXT,
        "SF_global_triangular_perfect": C_TRI * g_unit / P_EXT,
        "SF_least": least,
        "governing": gov,
        "second": second_name,
        "SF_second": second_sf,
        "factor_to_1": 1.0 / least,
        "eta": eta,
        "sigma_E_Pa": sig_E,
        "sigma_cr_Pa": sig_cr,
        "sigma_axial_Pa": sig_app,
        "N_over_Ne": sig_app / sig_E,
        "pole_passed": sig_app > sig_E,
        "on_r_min": i_ro == 0,
        "on_r_max": i_ro == N_RO - 1,
        "r_step_m": step,
        "straight_chord_unscored": chord_block(item["s"], r_o, I, sig),
    }


def family(picked, mat, rho, E, sig, joints, use_perry):
    out = []
    for block in picked:
        if block["best"] is None:
            continue
        out.append(row_from(mat, rho, E, sig, joints, use_perry, block["best"], block["variant"]))
    return out


def check(name, computed, expected, tol, bucket):
    ok = abs(computed - expected) <= tol
    bucket.append({"name": name, "computed": computed, "expected": expected, "tol": tol, "pass": ok})
    if not ok:
        print("FAIL", name, computed, expected, tol)
    return ok

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def build_documents(origin, elapsed, bucket):
    primary = {}
    for mat, (rho, E, sig) in MATERIALS.items():
        picked = scan(rho, E, sig, True, True, True)
        primary[mat] = family(picked, mat, rho, E, sig, True, True)
    rho, E, sig = MATERIALS["6061-T6"]
    no_joint = family(scan(rho, E, sig, False, True, True), "6061-T6", rho, E, sig, False, True)
    sic_rho, sic_E, _ = MATERIALS["SiC-alpha-Hexoloy-SA"]
    sic_flex = family(
        scan(sic_rho, sic_E, 380e6, True, True, True),
        "SiC-alpha-Hexoloy-SA",
        sic_rho,
        sic_E,
        380e6,
        True,
        True,
    )
    # Point evaluation at the published geometry, new modes, both joint settings.
    points = []
    for joints in (False, True):
        V, members, m_nodes, m_tube, m_joint, _ = mass_pack(3.0, joints)
        A = m_tube / (members * 3.0 * rho)
        pack = mode_pack(rho, E, sig, 3.0, PUBLISHED["r_o"], A, False)
        for grid, coeff in GRIDS:
            for k in KNOCKS:
                sf_g = k * coeff * pack["g_unit_Pa"] / P_EXT
                name, base = base_least(pack, True)
                gov, least = ("global", sf_g) if sf_g < base else (name, base)
                points.append({
                    "joints_on": joints,
                    "grid": grid,
                    "k": k,
                    "s_m": 3.0,
                    "r_o_m": PUBLISHED["r_o"],
                    "t_w_m": pack["t_w"],
                    "m_nodes_kg": m_nodes,
                    "m_joint_kg": m_joint,
                    "m_tube_kg": m_tube,
                    "SF_yield": pack["SF_yield"],
                    "SF_euler": pack["SF_euler"],
                    "SF_perry": pack["SF_perry"],
                    "SF_global": sf_g,
                    "SF_least": least,
                    "governing": gov,
                    "N_over_Ne": pack["N_over_Ne"],
                    "questionable": True,
                })
    results = {
        "schema": 1,
        "card": "MAINLINE-011b",
        "unit": "vacuum-mainline011b-p3-global-arcs-1019",
        "seat": "ref-2543c559b19ffce7dfdd",
        "questionable": True,
        "certification": False,
        "origin": origin,
        "elapsed_s": elapsed,
        "case": {
            "R_m": R,
            "p_ext_Pa": P_EXT,
            "lift_mass_kg": L_MASS,
            "rho_air": RHO_AIR,
            "nu_record_only": NU_RECORD,
            "ceiling": "margin 0: film + nodes(s) + joints + systems + tube = L",
        },
        "model": {
            "members": "spherical arcs of the 011 equilateral grid; length used in mass, Euler and Perry is the spacing s",
            "arch": "w = p*s/2, N = w*R, sigma = N/A",
            "straight_chord": "reported at each optimum and at the rounded brief point; not inside the minimiser",
            "perry": "a0 = s/1000, eta = a0*r_o/rg^2, Perry-Robertson sigma_cr, SF = sigma_cr/sigma_axial(at p_ext)",
            "global_two_way": "p = k*4*E*sqrt(I*A)/(s*R^2), from K=E*A/s and D=E*I/s",
            "global_triangular": "Et=(2/sqrt(3))*E*A/s, D=(3*sqrt(3)/4)*E*I/s, nu=1/3, p=k*4*sqrt(D*Et)/R^2 = k*4*sqrt(3/2)*E*sqrt(I*A)/(s*R^2)",
            "design_k": 0.2,
            "wright_k": 0.4,
            "band_ceiling_k": 0.5,
            "perfect_k": 1.0,
            "joints": "m_joint = 0.05*m_tube, m_tube = (L-film-nodes-systems)/1.05",
            "nodes": "V=8*pi*R^2/(sqrt(3)*s^2)+2, 0.02 kg each",
            "band": "s<=3 m, r_o<=s/3, r_o<=0.25 m, 4000 radii, same materials as 011",
            "scored_grid": "equilateral_triangular",
        },
        "cross_checks": bucket,
        "at_011_published_point": points,
        "primary_joints_on": primary,
        "sensitivity_6061_joints_off": no_joint,
        "sensitivity_SiC_flexural_380e6": sic_flex,
        "p2e_pinned": P2E,
    }
    return results


def write_card(results):
    def find(rows, grid, k):
        for row in rows:
            if row["grid"] == grid and row["k"] == k:
                return row
        return None

    lines = []
    lines.append("# MAINLINE-011b — P3 global lattice buckling and arc members")
    lines.append("")
    lines.append("Unit vacuum-mainline011b-p3-global-arcs-1019. Seat ref-2543c559b19ffce7dfdd.")
    lines.append("Every row is QUESTIONABLE. Nothing here is a certification.")
    lines.append("The 011 author's files were read and not rewritten. Checks 006, 007 and 007b were not run on this order.")
    lines.append("")
    lines.append("## What was re-derived")
    lines.append("")
    lines.append("At the brief's rounded 6061 point (s 3 m, r_o 86.6 mm, t_w 2.25 mm) the two-way continuum reproduces the robotics arithmetic. Perfect SF is 0.702903874926. Knockdowns 0.2, 0.4 and 0.5 give 0.140580774985, 0.281161549970 and 0.351451937463. Line load w is 143191.256871 N/m. Arch axial stress is 1.18499087263 GPa. Chord sag s^2/(8R) is 0.1125 m, greater than the tube radius. Simply-supported bending is 3.1598 GPa and fixed-end bending is 2.1065 GPa.")
    lines.append("")
    lines.append("The correction is the grid. MAINLINE-011's frame is the equilateral triangulation V=8*pi*R^2/(sqrt(3)*s^2)+2, not a two-way net and not a geodesic. Smeared membrane stiffness is Et=(2/sqrt(3))*E*A/s with nu=1/3. Smeared bending stiffness is D=(3*sqrt(3)/4)*E*I/s. The classical sphere pressure 4*sqrt(D*Et)/R^2 is then 4*sqrt(3/2)*E*sqrt(I*A)/(s*R^2), which is sqrt(3/2) times the brief's two-way pressure. That factor is scored. The two-way pressure is re-optimised beside it. No geodesic coefficient was invented.")
    lines.append("")
    lines.append("Scored members are spherical arcs, because N=p*R*s/2 is the arch resultant of the 011 load path. Straight-chord bending is reported at each optimum and is outside the minimiser. Arc shape error is a geometric Perry-Robertson imperfection a0=s/1000, eta=a0*r_o/rg^2. The safety factor is sigma_cr/sigma_axial at p_ext. The amplifier 1/(1-N/Ne) is not the score.")
    lines.append("")
    lines.append("Joint mass is 5 percent of tube mass, so the float ceiling still closes. Node mass stays 0.02 kg times V(s). The 5 percent is the P2 joint fraction applied to the tubes. A 6061 scan with that term removed is in RESULTS.json.")
    lines.append("")
    lines.append("Design knockdown is k=0.2, the floor of the brief's 0.2–0.5 lattice-dome band. Perfect is k=1. k=0.4 is Wright's modified factor, applied here to the classical pressure derived above. k=0.5 is the top of that band. All four are re-optimised.")
    lines.append("")
    lines.append("## Least safety factor")
    lines.append("")
    lines.append("Joints on. Perry scored. Band s<=3 m. Governing mode is the least of yield, Euler, local, film, Perry and global.")
    lines.append("")
    lines.append("| material | grid | k | least SF | governs | second | s m | r_o mm | t_w mm | nodes kg | joints kg |")
    lines.append("|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|")
    for mat, rows in results["primary_joints_on"].items():
        for k in (1.0, 0.4, 0.2):
            for grid in ("equilateral_triangular", "two_way"):
                row = find(rows, grid, k)
                lines.append(
                    "| {m} | {g} | {k} | {sf} | {gov} | {sec} | {s} | {ro} | {tw} | {nd} | {jt} |".format(
                        m=mat,
                        g=grid,
                        k=g(k),
                        sf=g(row["SF_least"]),
                        gov=row["governing"],
                        sec=row["second"],
                        s=g(row["s_m"]),
                        ro=g(row["r_o_m"] * 1e3),
                        tw=g(row["t_w_m"] * 1e3),
                        nd=g(row["m_nodes_kg"]),
                        jt=g(row["m_joint_kg"]),
                    )
                )
    lines.append("")
    lines.append("P2-E pinned comparison, not recomputed: 0.233885578993 at kd 0.2, and 0.164568553708 at kd 0.140725695373. The brief rounds these to 0.234 and 0.165 at 0.1407.")
    lines.append("")
    lines.append("SiC is also scanned at 380 MPa, the flexural figure carried by 011 from 008. The primary SiC row keeps 011's 3900 MPa crush. CNT remains a projection. Local buckling stays gamma=1. The film allowable stays 1.5 GPa.")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    lines.append("Wright, D. T., Membrane Forces and Buckling in Reticulated Shells, ASCE Journal of the Structural Division, Vol. 91, ST1, February 1965, pp. 173–201. An ASCE extract of that paper contains the sentence that the author uses a modified k factor of 0.4 for Table 2. The equivalent-thickness line in that extract is not legible and was not used. Buchert, Gioncu 1995 and Makowski are the brief's named works. No coefficient was taken from them. Gioncu 1995 is the state-of-the-art article in the International Journal of Space Structures.")
    lines.append("")
    lines.append("Regression, joints off and the four 011 modes only, recovers the filed 011 6061 optimum at s=3 m. Elapsed time is a measurement and is in ORIGIN.json and RESULTS.json.")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_nfi():
    rows = [
        {
            "id": "NFI-011B-GRID",
            "note": "011 counts nodes with the equilateral continuum. The scored global pressure uses that grid: Et=(2/sqrt(3))*E*A/s, nu=1/3, D=(3*sqrt(3)/4)*E*I/s, and the classical sphere 4*sqrt(D*Et)/R^2. The product is 4*sqrt(3/2)*E*sqrt(I*A)/(s*R^2). The brief's two-way pressure, coefficient 4, is the robotics arithmetic and is re-optimised beside it. A geodesic coefficient was not invented.",
        },
        {
            "id": "NFI-011B-WRIGHT",
            "note": "Wright 1965, ASCE Journal of the Structural Division 91(ST1):173-201, is the cited paper. The extract shows a modified k of 0.4 used for his Table 2. The thickness equation in the extract is not legible. k=0.4 here multiplies the classical pressure derived in this card, which may not be the expression in that table. Buchert, Gioncu 1995 and Makowski contributed no number. A secondary E' and t' pair that cancels back to the two-way pressure was not scored.",
        },
        {
            "id": "NFI-011B-KNOCKDOWN",
            "note": "Perfect is k=1. Design level is k=0.2, the floor of the brief's 0.2 to 0.5 lattice-dome band. k=0.5 is the top of that band. This is not the SP-8032 curve and it does not rescale 004's P2-E knockdown. P2-E stays the pinned pair 0.233885578993 and 0.164568553708.",
        },
        {
            "id": "NFI-011B-ARC",
            "note": "Scored members are spherical arcs. N=p*R*s/2 is the 011 arch resultant. Straight chords are the alternative: at the rounded point the sag is 0.1125 m and the bending stress is 2.1065 to 3.1598 GPa. Those stresses are reported and are outside the least-SF minimiser.",
        },
        {
            "id": "NFI-011B-PERRY",
            "note": "Geometric Perry-Robertson with a0=s/1000 and eta=a0*r_o/rg^2. This is not a code eta table. SF is sigma_cr divided by the arch stress at p_ext. When N exceeds Ne the pole of 1/(1-N/Ne) is passed and that factor is not the score. The formula is a steel-column interaction. On CFRP, CNT and SiC it is a projection. It is scored beside Euler and yield and can bind below both.",
        },
        {
            "id": "NFI-011B-JOINT",
            "note": "011 had no separate joint mass. This card sets joint mass to 5 percent of tube mass and reduces the tube budget so film, nodes, joints, systems and tube still equal the lift mass. The 5 percent is the P2 sandwich fraction applied to tubes, not a measured fitting. RESULTS carries a 6061 scan with the joint term removed. Node mass remains 0.02 kg times V(s).",
        },
        {
            "id": "NFI-011B-SIC",
            "note": "The primary SiC row uses 011's 3900 MPa crush. A second scan uses 380 MPa, the flexural figure 011 carried from 008. Flexural strength, brittle fracture, joining and a sintered tube of this size remain open. Perry and yield at 3900 MPa are not a bending allowable.",
        },
        {
            "id": "NFI-011B-LENGTH",
            "note": "Mass, Euler and Perry use the spacing s, as 011 did. The spherical arc is longer than the chord. That extra length was not substituted.",
        },
        {
            "id": "NFI-011B-LOCAL-FILM",
            "note": "Local buckling remains 0.6*E*t_w/r_o with gamma=1. The film allowable remains 1.5 GPa with no datasheet. Both are open, carried from 011.",
        },
        {
            "id": "NFI-011B-BAND",
            "note": "The reported optima stay inside s<=3 m, where 011 judged the equal-triangle continuum defensible. The unconstrained ride to s=6.4 m was not repeated.",
        },
        {
            "id": "NFI-011B-REGRESSION",
            "note": "With joints off and only yield, Euler, local and film, the 6061 banded optimum recovers the filed 011 point. The 011 tree was not rewritten.",
        },
        {
            "id": "NFI-011B-SKIP",
            "note": "The brief's last line names checks 006, 007 and 007b. The rotating order says those checks are already filed and are skipped here.",
        },
    ]
    return {"schema": 1, "card": "MAINLINE-011b", "unit": "vacuum-mainline011b-p3-global-arcs-1019", "rows": rows}


def write_inputs(pin_rows):
    return {
        "schema": 1,
        "card": "MAINLINE-011b",
        "unit": "vacuum-mainline011b-p3-global-arcs-1019",
        "pins": pin_rows,
        "constants": {
            "R_m": R,
            "p_ext_Pa": P_EXT,
            "lift_mass_kg": L_MASS,
            "film_kg": M_FILM_PIN,
            "node_kg": M_NODE_UNIT,
            "systems_kg": M_SYS,
            "sigma_film_Pa": SIGMA_FILM,
            "t_film_m": T_FILM,
            "rho_film": RHO_FILM,
            "C_local": C_LOCAL,
            "joint_frac": JOINT_FRAC,
            "C_two_way": C_TWO,
            "C_triangular": C_TRI,
            "s_grid": "0.40 to 3.00 step 0.02",
            "n_ro": N_RO,
        },
        "materials": {
            name: {"rho": rho, "E_Pa": E, "sigma_Pa": sig, "questionable": True}
            for name, (rho, E, sig) in MATERIALS.items()
        },
        "p2e_pinned": P2E,
        "published_011_6061": PUBLISHED,
        "decisions": [
            "Scored grid is equilateral triangular. Two-way is reported and re-optimised beside it.",
            "Scored members are arcs. Straight chords are unscored.",
            "Perry a0=s/1000 is an extra scored mode.",
            "Design k=0.2. Also re-optimised: k=1, k=0.4, k=0.5.",
            "Joints are 5 percent of tube mass. 6061 is repeated with joints off.",
            "SiC primary allowable is 3900 MPa. A 380 MPa flexural scan is separate.",
        ],
    }


def main():
    if os.path.exists(RESULTS_PATH):
        raise SystemExit("RESULTS.json is the measured run. Not recomputing.")
    checks_only = "--checks-only" in sys.argv
    passed, bucket = run_checks()
    if not passed:
        raise SystemExit(3)
    if checks_only:
        print("CHECKS_ONLY pass")
        return
    mono0 = time.monotonic()
    wall0 = datetime.datetime.now(ZONE)
    origin = {
        "origin_local": wall0.isoformat(timespec="microseconds"),
        "origin_monotonic_s": mono0,
    }
    if os.path.exists(ORIGIN_PATH):
        origin = json.loads(open(ORIGIN_PATH, encoding="utf-8").read())
        print("ORIGIN exists; not restamping")
    else:
        atomic_write(ORIGIN_PATH, json.dumps(origin, indent=1) + "\n")
        print("ORIGIN", origin["origin_local"])
    results = build_documents(origin, None, bucket)
    wall1 = datetime.datetime.now(ZONE)
    mono1 = time.monotonic()
    elapsed = mono1 - origin["origin_monotonic_s"]
    results["elapsed_s"] = elapsed
    results["ended_local"] = wall1.isoformat(timespec="microseconds")
    pin_rows = next(item["pins"] for item in bucket if "pins" in item)
    atomic_write(RESULTS_PATH, json.dumps(results, indent=1) + "\n")
    atomic_write(os.path.join(ROOT, "NFI.json"), json.dumps(write_nfi(), indent=1) + "\n")
    atomic_write(os.path.join(ROOT, "INPUTS.json"), json.dumps(write_inputs(pin_rows), indent=1) + "\n")
    atomic_write(os.path.join(ROOT, "CARD.md"), write_card(results))
    print("elapsed_s", g(elapsed))
    for mat, rows in results["primary_joints_on"].items():
        for row in rows:
            if row["grid"] == "equilateral_triangular" and row["k"] in (1.0, 0.4, 0.2):
                print(
                    "TRI",
                    mat,
                    "k", g(row["k"]),
                    "SF", g(row["SF_least"]),
                    row["governing"],
                    "second", row["second"], g(row["SF_second"]),
                    "s", g(row["s_m"]),
                    "ro", g(row["r_o_m"]),
                    "tw", g(row["t_w_m"]),
                    "nodes", g(row["m_nodes_kg"]),
                    "joints", g(row["m_joint_kg"]),
                    "perry", g(row["SF_perry"]),
                    "global", g(row["SF_global"]),
                    "yield", g(row["SF_yield"]),
                )
    for row in results["sensitivity_6061_joints_off"]:
        if row["grid"] == "equilateral_triangular" and row["k"] in (1.0, 0.4, 0.2):
            print("NOJOINT", "k", g(row["k"]), "SF", g(row["SF_least"]), row["governing"], "s", g(row["s_m"]))
    for row in results["sensitivity_SiC_flexural_380e6"]:
        if row["grid"] == "equilateral_triangular" and row["k"] in (1.0, 0.2):
            print("SIC380", "k", g(row["k"]), "SF", g(row["SF_least"]), row["governing"], "s", g(row["s_m"]))
    for row in results["primary_joints_on"]["6061-T6"]:
        if row["k"] == 0.2:
            print(
                "TWOCHK",
                row["grid"],
                "SF", g(row["SF_least"]),
                row["governing"],
                "s", g(row["s_m"]),
                "chordSF", g(row["straight_chord_unscored"]["SF_bend_fixed_end"]),
                "sag_gt", row["straight_chord_unscored"]["sag_exceeds_tube_radius"],
            )


if __name__ == "__main__":
    main()
