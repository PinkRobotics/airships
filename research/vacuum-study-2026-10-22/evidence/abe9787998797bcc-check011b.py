#!/usr/bin/env python3
"""MAINLINE-011b check: own arithmetic from the pinned inputs (CHECK.md + COMMON.md).

Checker seat ref-55cff924be25afe6f9dd. The owner's arcs.py is neither imported nor run.
The owner's RESULTS.json is read ONLY to compare numbers after they are computed here.
Every value is QUESTIONABLE; nothing here is a certification.
"""
import datetime
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

T0_LOCAL = datetime.datetime.now().astimezone().isoformat()
T0 = time.monotonic()

OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline011b-check-1019"
OWNER = Path("unpublished-local-ref:6d6611b67d773afa"
             "vacuum-mainline011b-p3-global-arcs-1019")

# ---- pinned inputs ------------------------------------------------------------------------------
# COMMON.md (case, P3 rule), the estimates owner's INPUTS.json (I-SIG, I-TFILM, I-NODE, I-SYS3),
# 011's INPUTS.json (I-011-SWAP materials from MAINLINE-008; I-011-LOCAL coefficient 0.6).
R = 10.0
P = 95460.8379139
L = 4889.44215019
FILM = 97.515
SYS = 50.0
NODE = 0.02
SIG_F = 1.5e9
T_F = 8e-5
C_LOC = 0.6
JF = 0.05
MATS = {  # rho kg/m3, E Pa, sigma Pa
    "6061-T6": (2700.0, 68.9e9, 276e6),
    "CFRP-QI-M55J-epoxy": (1640.0, 135e9, 350e6),
    "CFRP-QI-T700-epoxy": (1550.0, 54e9, 520e6),
    "CFRP-QI-K13D2U-epoxy": (1750.0, 210e9, 220e6),
    "SiC-alpha-Hexoloy-SA": (3100.0, 410e9, 3900e6),
    "CNT-yarn-QI-PROJECTION": (1400.0, 180e9, 1200e6),
}
KS = (1.0, 0.5, 0.4, 0.2)
MODES = ("yield", "euler", "local", "film", "perry", "global")


# ---- 1. smeared lattice stiffness, from the member families themselves ----------------------------
def lattice(angles_deg, h):
    """Plane stiffness of a pin-jointed grid: one family per angle, line spacing h, members E*A, E*I.
    Returns the 2D coefficients per unit E*A (membrane) and per unit E*I (bending, torsion ignored)."""
    e = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in angles_deg]
    c1111 = sum(x ** 4 for x, _ in e) / h
    c1122 = sum((x * y) ** 2 for x, y in e) / h
    c1212 = c1122
    return c1111, c1122, c1212


def smeared(s):
    tri = lattice((0.0, 60.0, 120.0), s * math.sqrt(3) / 2)   # member length s, line spacing s*sqrt3/2
    two = lattice((0.0, 90.0), s)                             # spacing s
    out = {}
    for name, (c11, c12, c66) in (("equilateral_triangular", tri), ("two_way", two)):
        nu = c12 / c11
        Y = c11 * (1 - nu ** 2)        # 2D Young's modulus per unit E*A
        D = c11                        # plate D (coefficient of del^4 w) per unit E*I
        C = 4 * math.sqrt(D * Y) * s   # p_cr = C * E*sqrt(I*A)/(s*R^2)
        out[name] = {"nu": nu, "Y_over_EA_per_s": Y * s, "D_over_EI_per_s": D * s,
                     "shear_C1212_over_EA_per_s": c66 * s, "C": C}
    out["ratio_C_tri_over_two_way"] = out["equilateral_triangular"]["C"] / out["two_way"]["C"]
    return out


SM = smeared(1.0)
C_GRID = {"equilateral_triangular": SM["equilateral_triangular"]["C"], "two_way": SM["two_way"]["C"]}


# ---- geometry and mass closure ------------------------------------------------------------------
def nodes(s):
    return 8 * math.pi * R ** 2 / (math.sqrt(3) * s ** 2) + 2


def members(s):
    return 3 * nodes(s) - 6


def m_tube(s, jf, sys_kg=SYS, margin_kg=0.0):
    return (L - FILM - NODE * nodes(s) - sys_kg - margin_kg) / (1 + jf)


def section(ro, A):
    ri = np.sqrt(np.maximum(ro ** 2 - A / np.pi, 0.0))
    I = np.pi / 4 * (ro ** 2 - ri ** 2) * (ro ** 2 + ri ** 2)
    return ri, ro - ri, I


def all_modes(mat, s, ro, A, k, grid, force=1.0, sig_override=None):
    rho, E, sig = MATS[mat]
    if sig_override is not None:
        sig = sig_override
    ri, tw, I = section(ro, A)
    N = P * R * s / 2 * force            # card: w = p*s/2, N = w*R; force=1/sqrt3 is the equilibrium value
    sax = N / A
    rg2 = I / A
    sE = np.pi ** 2 * E * rg2 / s ** 2
    eta = (s / 1000.0) * ro / rg2
    b = sig + (1 + eta) * sE
    scr = 0.5 * (b - np.sqrt(np.maximum(b * b - 4 * sig * sE, 0.0)))
    out = {
        "yield": np.broadcast_to(sig / sax, np.shape(ro)),
        "euler": (np.pi ** 2 * E * I / s ** 2) / N,
        "local": (C_LOC * E * tw / ro) / sax,
        "film": np.broadcast_to((2 * SIG_F * T_F / s) / P, np.shape(ro)),
        "perry": scr / sax,
        "global": k * C_GRID[grid] * E * np.sqrt(I * A) / (s * R ** 2) / P,
    }
    return out, (ri, tw, I, N, sax)


def least(md):
    return np.minimum.reduce([md[m] for m in MODES])


S_GRID = [round(0.40 + 0.02 * i, 10) for i in range(131)]


R_LO = 1.0001   # the owner's lower radius bound is 1.0001 x the solid rod (read from its grid lines only)


def optimise(mat, grid, k, jf=JF, modes=MODES, force=1.0, sig_override=None, sys_kg=SYS, margin_kg=0.0,
             n_ro=4000, s_list=None, r_lo=R_LO):
    """The card's stated scan: s on S_GRID, r_o in n_ro steps from r_lo x the solid rod to min(0.25, s/3)."""
    rho = MATS[mat][0]
    best = None
    for s in (s_list or S_GRID):
        mt = m_tube(s, jf, sys_kg, margin_kg)
        A = mt / (rho * members(s) * s)
        r_solid = math.sqrt(A / math.pi) * r_lo
        r_max = min(0.25, s / 3)
        if r_max <= r_solid:
            continue
        ro = np.linspace(r_solid, r_max, n_ro)
        md, _ = all_modes(mat, s, ro, A, k, grid, force, sig_override)
        sf = np.minimum.reduce([md[m] for m in modes])
        i = int(np.argmax(sf))
        if best is None or sf[i] > best[0]:
            best = (float(sf[i]), s, float(ro[i]), A, mt)
    return best


def refine(mat, grid, k, jf=JF, force=1.0, sig_override=None, sys_kg=SYS, margin_kg=0.0):
    """Continuous optimum inside the same band: s every 1 mm, r_o by a 2000-point grid then golden section."""
    rho = MATS[mat][0]
    best = None
    per_s = {}
    for s in np.round(np.arange(0.400, 3.0000001, 0.001), 6):
        s = float(s)
        mt = m_tube(s, jf, sys_kg, margin_kg)
        A = mt / (rho * members(s) * s)
        lo, hi = math.sqrt(A / math.pi), min(0.25, s / 3)
        if hi <= lo:
            continue
        ro = np.linspace(lo, hi, 2000)
        sf = least(all_modes(mat, s, ro, A, k, grid, force, sig_override)[0])
        i = int(np.argmax(sf))
        a, b = ro[max(i - 1, 0)], ro[min(i + 1, len(ro) - 1)]
        f = lambda x: float(least(all_modes(mat, s, np.array([x]), A, k, grid, force, sig_override)[0])[0])
        g = (math.sqrt(5) - 1) / 2
        c, d = b - g * (b - a), a + g * (b - a)
        fc, fd = f(c), f(d)
        for _ in range(60):
            if fc < fd:
                a, c, fc = c, d, fd
                d = a + g * (b - a)
                fd = f(d)
            else:
                b, d, fd = d, c, fc
                c = b - g * (b - a)
                fc = f(c)
        x = (a + b) / 2
        val = max(f(x), float(sf[i]))
        xr = x if f(x) >= float(sf[i]) else float(ro[i])
        if abs(s * 50 - round(s * 50)) < 1e-9:
            per_s[f"{s:.2f}"] = (val, xr)
        if best is None or val > best[0]:
            best = (val, s, xr, A, mt)
    REFINE_PER_S[(mat, grid, k, jf, force, sig_override, sys_kg, margin_kg)] = per_s
    return best


REFINE_PER_S = {}


def row(mat, grid, k, best, jf=JF, force=1.0, sig_override=None, sys_kg=SYS, margin_kg=0.0):
    sf, s, ro, A, mt = best
    md, (ri, tw, I, N, sax) = all_modes(mat, s, np.array([ro]), A, k, grid, force, sig_override)
    vals = {m: float(md[m][0]) for m in MODES}
    order = sorted(MODES, key=lambda m: vals[m])
    return {
        "material": mat, "grid": grid, "k": k, "joints_frac": jf, "force_factor": force,
        "sigma_override_Pa": sig_override, "systems_kg": sys_kg, "margin_kg": margin_kg,
        "s_m": s, "r_o_m": ro, "t_w_m": float(tw[0]), "A_m2": A, "I_m4": float(I[0]),
        "nodes": nodes(s), "members": members(s), "m_nodes_kg": NODE * nodes(s), "m_tube_kg": mt,
        "m_joint_kg": jf * mt, "total_kg": mt * (1 + jf) + FILM + NODE * nodes(s) + sys_kg + margin_kg,
        "N_member_N": float(N), "sigma_axial_Pa": float(sax[0]) if np.ndim(sax) else float(sax),
        "SF": vals, "SF_least": min(vals.values()), "governs": order[0], "second": order[1],
        "r_over_t": ro / float(tw[0]),
    }


# ---- 2. member force by static equilibrium (virial / Maxwell load-path identity) ----------------------
def equilibrium_force(s):
    """For a closed pin-jointed frame under external pressure p: sum(C_m * l_m) = 3*p*Vol = 4*pi*R^3*p.
    With the card's M = 3V-6 members of length s, the mean compression is fixed by statics alone."""
    M = members(s)
    mean_C = 4 * math.pi * R ** 3 * P / (M * s)
    card = P * R * s / 2
    return {"s_m": s, "members": M, "mean_C_equilibrium_N": mean_C, "card_N_pRs_over_2": card,
            "card_over_equilibrium": card / mean_C, "pRs_over_2sqrt3": P * R * s / (2 * math.sqrt(3)),
            "film_area_per_member_m2": 4 * math.pi * R ** 2 / M,
            "film_area_per_member_over_s2": 4 * math.pi * R ** 2 / M / s ** 2}


# ---- 3. a discrete geodesic truss under the same pressure --------------------------------------------
def icosphere(n):
    t = (1 + math.sqrt(5)) / 2
    v = np.array([[-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0], [0, -1, t], [0, 1, t], [0, -1, -t],
                  [0, 1, -t], [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]], float)
    f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2),
         (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5),
         (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    pts, key, tris = [], {}, []

    def idx(p):
        p = p / np.linalg.norm(p) * R
        kk = tuple(np.round(p, 6))
        if kk not in key:
            key[kk] = len(pts)
            pts.append(p)
        return key[kk]

    for a, b, c in f:
        A, B, C = v[a], v[b], v[c]
        g = {}
        for i in range(n + 1):
            for j in range(n + 1 - i):
                g[(i, j)] = idx(A + (B - A) * i / n + (C - A) * j / n)
        for i in range(n):
            for j in range(n - i):
                tris.append((g[(i, j)], g[(i + 1, j)], g[(i, j + 1)]))
                if i + j + 1 < n:
                    tris.append((g[(i + 1, j)], g[(i + 1, j + 1)], g[(i, j + 1)]))
    X = np.array(pts)
    edges = sorted({tuple(sorted(e)) for t3 in tris for e in ((t3[0], t3[1]), (t3[1], t3[2]), (t3[0], t3[2]))})
    return X, edges, tris


def geodesic_demo(n):
    X, edges, tris = icosphere(n)
    V, M = len(X), len(edges)
    area = np.zeros(V)
    for a, b, c in tris:
        ar = 0.5 * np.linalg.norm(np.cross(X[b] - X[a], X[c] - X[a]))
        area[[a, b, c]] += ar / 3
    area *= 4 * math.pi * R ** 2 / area.sum()          # the sphere's pressure, shared by tributary area
    f = -P * area[:, None] * X / R                      # inward radial nodal loads
    B = np.zeros((3 * V, M))
    lengths = np.zeros(M)
    for m, (a, b) in enumerate(edges):
        d = X[b] - X[a]
        l = np.linalg.norm(d)
        u = d / l
        lengths[m] = l
        B[3 * a:3 * a + 3, m] = u
        B[3 * b:3 * b + 3, m] = -u
    F, *_ = np.linalg.lstsq(B, -f.ravel(), rcond=None)  # tension positive
    resid = float(np.linalg.norm(B @ F + f.ravel()) / np.linalg.norm(f))
    C = -F
    lbar = float(lengths.mean())
    return {"frequency": n, "nodes": V, "members": M, "euler_check_M_eq_3V_minus_6": M == 3 * V - 6,
            "rank_B": int(np.linalg.matrix_rank(B)), "relative_residual": resid,
            "l_mean_m": lbar, "l_min_m": float(lengths.min()), "l_max_m": float(lengths.max()),
            "C_mean_N": float(C.mean()), "C_min_N": float(C.min()), "C_max_N": float(C.max()),
            "all_compression": bool((C > 0).all()),
            "virial_sum_Cl_over_4piR3p": float((C * lengths).sum() / (4 * math.pi * R ** 3 * P)),
            "C_mean_over_card_pRl_2": float(C.mean() / (P * R * lbar / 2)),
            "C_mean_over_pRl_2sqrt3": float(C.mean() / (P * R * lbar / (2 * math.sqrt(3)))),
            "C_over_l_mean_over_pR_2sqrt3": float((C / lengths).mean() / (P * R / (2 * math.sqrt(3))))}


# ---- named points ---------------------------------------------------------------------------------
def point(mat, s, ro, tw, k, grid, joints_on):
    rho, E, sig = MATS[mat]
    ri = ro - tw
    A = math.pi * (ro ** 2 - ri ** 2)
    md, (ri_, tw_, I, N, sax) = all_modes(mat, s, np.array([ro]), A, k, grid)
    return {m: float(md[m][0]) for m in MODES}, A, float(I[0]), float(N), float(np.ravel(sax)[0])


def main():
    res = {"schema": 1, "card": "MAINLINE-011b CHECK", "unit": "vacuum-mainline011b-check-1019",
           "seat": "ref-55cff924be25afe6f9dd", "questionable": True, "certification": False,
           "started_local": T0_LOCAL}
    # 1. stiffness
    res["smeared_stiffness"] = SM
    res["sqrt_3_over_2"] = math.sqrt(1.5)
    # brief's rounded 6061 point
    s, ro, tw = 3.0, 0.0866, 0.00225
    sfs, A, I, N, sax = point("6061-T6", s, ro, tw, 1.0, "two_way", False)
    w = P * s / 2
    res["rounded_point"] = {
        "s": s, "r_o": ro, "t_w": tw, "A": A, "I": I, "SF_two_way_perfect": sfs["global"],
        "SF_two_way_k": {str(k): k * sfs["global"] for k in (0.2, 0.4, 0.5)},
        "SF_tri_perfect": sfs["global"] * SM["ratio_C_tri_over_two_way"],
        "w_N_per_m": w, "sigma_arch_Pa": w * R / A, "sag_m": s ** 2 / (8 * R),
        "sigma_bend_simple_Pa": (w * s ** 2 / 8) * ro / I, "sigma_bend_fixed_Pa": (w * s ** 2 / 12) * ro / I}
    # 011's filed 6061 tube, joints off
    s, ro, tw = 3.0, 0.0866221663456903, 0.002251568619368413
    sfs, A, I, N, sax = point("6061-T6", s, ro, tw, 0.2, "equilateral_triangular", False)
    res["filed_011_tube"] = {"s": s, "r_o": ro, "t_w": tw, "A": A, "I": I, "SF": sfs,
                             "tube_mass_kg_at_A": A * members(s) * s * 2700.0, "m_tube_joints_off": m_tube(s, 0.0)}
    # 2-3. member force
    res["equilibrium"] = [equilibrium_force(x) for x in (1.0, 1.36, 2.04, 3.0)]
    res["geodesic_truss"] = [geodesic_demo(n) for n in (4, 6)]
    # 4. the card's 48 rows, on the card's grid and continuously
    rows, refined = [], []
    for mat in MATS:
        for grid in C_GRID:
            for k in KS:
                rows.append(row(mat, grid, k, optimise(mat, grid, k)))
                refined.append(row(mat, grid, k, refine(mat, grid, k)))
    res["primary_joints_on_grid"] = rows
    res["primary_joints_on_refined"] = refined
    res["refined_best_ro_per_grid_s"] = {f"{m}|{g}|{k}": REFINE_PER_S[(m, g, k, JF, 1.0, None, SYS, 0.0)]
                                         for m in MATS for g in C_GRID for k in KS}
    res["primary_joints_on_grid_solid_start"] = [row(m, g, k, optimise(m, g, k, r_lo=1.0))
                                                 for m in MATS for g in C_GRID for k in KS]
    # sensitivities as the card states them
    res["sens_6061_joints_off"] = [row("6061-T6", g, k, optimise("6061-T6", g, k, jf=0.0), jf=0.0)
                                   for g in C_GRID for k in KS]
    res["sens_SiC_380MPa"] = [row("SiC-alpha-Hexoloy-SA", g, k,
                                  optimise("SiC-alpha-Hexoloy-SA", g, k, sig_override=380e6), sig_override=380e6)
                              for g in C_GRID for k in KS]
    res["regression_011"] = {}
    for tag, rl in (("owner_grid", R_LO), ("solid_start", 1.0)):
        reg = optimise("6061-T6", "two_way", 1.0, jf=0.0, modes=("yield", "euler", "local", "film"), r_lo=rl)
        res["regression_011"][tag] = {"SF": reg[0], "s": reg[1], "r_o": reg[2], "A": reg[3], "m_tube": reg[4]}
    # 5. proposed-fix estimates: equilibrium member force, and the 022 accounting
    fx = 1 / math.sqrt(3)
    res["fix_equilibrium_force"] = [row(m, g, k, refine(m, g, k, force=fx), force=fx)
                                    for m in ("6061-T6", "SiC-alpha-Hexoloy-SA")
                                    for g in C_GRID for k in (0.2, 0.4)]
    acc = dict(sys_kg=100.0, margin_kg=0.05 * L)
    res["sens_SiC_100kg_5pct"] = [row("SiC-alpha-Hexoloy-SA", g, k, refine("SiC-alpha-Hexoloy-SA", g, k, **acc), **acc)
                                  for g in C_GRID for k in (0.2, 0.4)]
    res["sens_SiC_100kg_5pct_eqforce"] = [
        row("SiC-alpha-Hexoloy-SA", g, k, refine("SiC-alpha-Hexoloy-SA", g, k, force=fx, **acc), force=fx, **acc)
        for g in C_GRID for k in (0.2, 0.4)]
    res["ended_local"] = datetime.datetime.now().astimezone().isoformat()
    res["elapsed_s"] = time.monotonic() - T0
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "RESULTS.json").write_text(json.dumps(res, indent=1, default=float))
    print("wrote", OUT / "RESULTS.json", "elapsed", round(res["elapsed_s"], 1), "s")


if __name__ == "__main__":
    main()
