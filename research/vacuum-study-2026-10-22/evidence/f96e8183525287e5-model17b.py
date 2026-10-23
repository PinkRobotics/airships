#!/usr/bin/env python3
"""MAINLINE-017b models: P2 (Be sandwich on CR-III 5056) and P3 (SiC arc frame), own arithmetic.

P2 follows 021 rev1's modes (CR-1457 as 009d/014b state them, biaxial dimpling) with 028's joining
(film per bond line, 30:1-or-steeper adhesive scarf, core splice, sealing) replacing the 5% joint
allowance, on 019's optimistic reserve scaled with radius by 027's laws.
P3 follows 022c's equilateral frame: 022b equilibrium force pRs/(2*sqrt(3)), SP-8007 local gamma,
Perry with L/1000, k 0.2 global, 023 sized end joints C*N^2/r, 024 inradius-cap sag charged as lift.
Every material value is QUESTIONABLE; projections are named PROJECTION where they are used.
"""
import math
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

P0 = 95460.83791390515            # Pa, 500 m ISA (COMMON; 014b, 028 carry this value)
L10 = 4889.442150186961           # kg, lift at R 10 m (COMMON)
SYS = 100.0                       # kg systems allowance (COMMON; 019 sealed service sits inside it)
SQRT3 = math.sqrt(3.0)
# 019 optimistic fixed reserve items at R 10 m (022's budget report quotes them), and 027's radius laws
RES019 = {"water_0p1mm": (125.663706144, 2), "contamination": (5.0, 2), "temperature_pressure": (213.036426544, 3),
          "humidity": (18.7043898824, 3), "internal_air": (48.8944215019, 3)}


def biax():
    """Positive real root of q^3 + q = 1 (CR-1457 equibiaxial wrinkling interaction), by Cardano."""
    s = math.sqrt(0.25 + 1.0 / 27.0)
    return (0.5 + s) ** (1.0 / 3.0) - (s - 0.5) ** (1.0 / 3.0)


Q_BIAX = biax()


def reserve_019(R):
    return sum(v * (R / 10.0) ** n for v, n in RES019.values())


def lift(R):
    return L10 * (R / 10.0) ** 3


# ============================================================================ P2
LB_FT2 = 0.45359237 / 0.3048 ** 2
P2_TODAY = {
    # face: Materion SR-200 sheet (DS-HPP-613, 2024): typical E, minimum tensile yield used as compressive
    "E": 290e9, "sigma": 345e6, "rho_f": 1850.0,
    "nu": 0.08,          # S-200F VHP Poisson ratios 0.058-0.108, mean 0.083 (IAEA compilation, Table 7); transferred
    # core: Hexcel CR-III 5056 3/8-1.0 (datasheet Table II, typical)
    "rho_c": 16.018463373960138, "Gc": 46884349.59354485, "Ec": 103421359.3975254,
    "crush": 241316.50526089262, "cell": 0.009525, "Fc_flatwise": 60 * 6894.757293168,
    # analysis: CR-1457 handbook gamma (0.20 below Vc 2, 1 at and above) and wrinkle coefficient 0.33
    "gamma": 0.20, "Q": 0.33,
    # 028 joining, today: stock SR-200 envelope, AF 163-2U at 0.015 lb/ft2 per bond line, 70 g/m2 scarf film
    "panel_a": 0.6096, "panel_b": 1.8288, "film": 0.015 * LB_FT2, "seam_film": 0.070,
    "scarf_tau": 10e6, "scarf_min": 30.0, "splice_gap": 0.0005, "splice_rho": 500.0, "sealing": 0.002,
}


KDELTA_TODAY = (0.82 / 0.33 - 1.0) / 0.64      # waviness parameter that eq 2.2-12 needs to give 0.33


def p2_apply(base, fac):
    """Property factors: >1 is always an improvement."""
    q = dict(base)
    f = lambda k: fac.get(k, 1.0)  # noqa: E731
    q["sigma"] *= f("face_strength")
    q["E"] *= f("face_modulus")
    q["rho_f"] /= f("face_density")
    q["Gc"] *= f("core_shear_modulus")
    q["Ec"] *= f("core_tt_modulus")
    q["rho_c"] /= f("core_density")
    q["crush"] *= f("core_crush")
    q["cell"] /= f("cell_size")
    q["gamma_fac"] = f("gamma")
    # wrinkling: CR-1457 eq 2.2-12/13, Q = 0.82/(1 + 0.64 K_delta), K_delta = delta Ec/(tc Fc); today's 0.33 is
    # K_delta = KDELTA_TODAY. 'face_flatness' divides K_delta (the waviness amplitude, held as that ratio).
    q["Q"] = 0.82 / (1.0 + 0.64 * KDELTA_TODAY / f("face_flatness")) * f("wrinkle_Q")
    q["panel_a"] *= f("sheet_size")
    q["panel_b"] *= f("sheet_size")
    q["film"] /= f("film_mass")
    q["seam_scale"] = 1.0 / f("seam_mass")
    return q


def scarf_ratio(sm, q, fixed30=False):
    """Smallest scarf run/thickness r >= 30 whose average shear sm*r/(1+r^2) meets 028's 10 MPa screen."""
    if fixed30:
        return np.full_like(sm, q["scarf_min"])
    x = sm / q["scarf_tau"]
    root = 0.5 * (x + np.sqrt(np.maximum(x * x - 4.0, 0.0)))
    return np.maximum(q["scarf_min"], root)


def p2_joining(R, tf, tc, q, fixed30=False):
    A = 4.0 * math.pi * R * R
    sm = P0 * R / (4.0 * tf)
    r = scarf_ratio(sm, q, fixed30)
    ov = r * tf
    a, b = q["panel_a"] - ov, q["panel_b"] - ov
    ok = (a > 0) & (b > 0)
    length = np.where(ok, A * (1.0 / np.where(ok, a, 1.0) + 1.0 / np.where(ok, b, 1.0)), np.inf)
    per_m = q.get("seam_scale", 1.0) * (2.0 * tf * np.sqrt(1.0 + r * r) * q["seam_film"]
                                         + q["splice_gap"] * tc * q["splice_rho"] + q["sealing"])
    films = 2.0 * A * q["film"]
    return films + length * per_m, {"films": films, "seam_length": length, "per_m": per_m, "ratio": r}


def p2_geometry(R, F, q, line="019", fixed30=False, iters=60):
    """Mass line for core-mass fractions F; explicit joining replaces the 5% allowance (as 028).
    line '019': S + J + 100 + 019 reserve(R) = lift(R).  line '5pct': S + J = 0.95 lift - 100 (028's)."""
    A = 4.0 * math.pi * R * R
    L = lift(R)
    cap = (L - SYS - reserve_019(R)) if line == "019" else (0.95 * L - SYS)
    F = np.asarray(F, dtype=float)
    lo = np.zeros_like(F)
    hi = np.full_like(F, cap)
    for _ in range(iters):
        S = 0.5 * (lo + hi)
        tf = (1.0 - F) * S / (2.0 * A * q["rho_f"])
        tc = F * S / (A * q["rho_c"])
        J, _ = p2_joining(R, tf, tc, q, fixed30)
        over = S + J > cap
        hi = np.where(over, S, hi)
        lo = np.where(over, lo, S)
    S = lo
    tf = (1.0 - F) * S / (2.0 * A * q["rho_f"])
    tc = F * S / (A * q["rho_c"])
    J, parts = p2_joining(R, tf, tc, q, fixed30)
    return {"S": S, "tf": tf, "tc": tc, "J": J, "parts": parts, "cap": cap}


P2_MODES = ("global_buckling", "face_compression", "core_shear_crimping", "core_crush", "face_wrinkling",
            "intracell_dimpling")


def p2_modes(R, tf, tc, q, gamma_override=None):
    root = math.sqrt(1.0 - q["nu"] ** 2)
    h = tc + tf
    sigma0 = q["E"] * h / (R * root)
    scrimp = h * h * q["Gc"] / (2.0 * tf * tc)
    vc = sigma0 / scrimp
    stiff = vc < 2.0
    kc = np.where(stiff, 1.0 - vc / 4.0, 1.0 / vc)
    if gamma_override is not None:
        gam = np.full_like(vc, gamma_override)
    elif q.get("gamma_rule") == "conservative":
        # 018's conservative reading: 0.20 at every Vc (no step to 1 on the crimp branch)
        gam = np.full_like(vc, min(1.0, q["gamma"] * q.get("gamma_fac", 1.0)))
    else:
        # CR-1457 eq 6.2-13 / p. 6-12: 0.20 below Vc 2, 1 at and above
        gam = np.where(stiff, np.minimum(1.0, q["gamma"] * q.get("gamma_fac", 1.0)), 1.0)
    sm = P0 * R / (4.0 * tf)
    out = {
        "global_buckling": gam * kc * sigma0 / sm,
        "face_compression": q["sigma"] / sm,
        "core_shear_crimping": scrimp / sm,
        "core_crush": np.full_like(vc, q["crush"] / (P0 / 2.0)),
        "face_wrinkling": Q_BIAX * q["Q"] * np.sqrt(q["E"] * q["Ec"] * tf / tc) / sm,
        "intracell_dimpling": 0.5 * 2.0 * q["E"] / (1.0 - q["nu"] ** 2) * (tf / q["cell"]) ** 2 / sm,
    }
    return out, {"Vc": vc, "Kc": kc, "gamma": gam, "sigma_m": sm}


def p2_least(ev):
    return np.min(np.vstack([ev[k] for k in P2_MODES]), axis=0)


def p2_optimise(R, q, line="019", fixed30=False, extra_scarf_mode=False, n=6001):
    """Best least SF over the core-mass fraction: dense grid, then golden refinement."""
    def score(F):
        g = p2_geometry(R, F, q, line, fixed30)
        ev, aux = p2_modes(R, g["tf"], g["tc"], q)
        lst = p2_least(ev)
        if extra_scarf_mode:
            r = g["parts"]["ratio"]
            ev["scarf_screen"] = q["scarf_tau"] * (1.0 + r * r) / (aux["sigma_m"] * r)
            lst = np.minimum(lst, ev["scarf_screen"])
        return lst, g, ev, aux
    # log-spaced in the core-mass fraction, so very light cores (fractions far below 1e-4) are reached
    X = np.linspace(math.log(1e-9), math.log(0.99999), n)
    lst, _, _, _ = score(np.exp(X))
    k = int(np.argmax(lst))
    lo, hi = X[max(0, k - 1)], X[min(n - 1, k + 1)]
    for _ in range(90):
        u, v = lo + (hi - lo) * 0.381966, hi - (hi - lo) * 0.381966
        su = score(np.array([math.exp(u)]))[0][0]
        sv = score(np.array([math.exp(v)]))[0][0]
        if su < sv:
            lo = u
        else:
            hi = v
    F = np.exp(X)
    Fb = np.array([math.exp(0.5 * (lo + hi))])
    lst, g, ev, aux = score(Fb)
    if lst[0] < score(np.array([F[k]]))[0][0]:
        Fb = np.array([F[k]])
        lst, g, ev, aux = score(Fb)
    row = {"least": float(lst[0]), "F": float(Fb[0]), "tf": float(g["tf"][0]), "tc": float(g["tc"][0]),
           "S": float(g["S"][0]), "J": float(g["J"][0]), "films": float(g["parts"]["films"]),
           "seam_length": float(g["parts"]["seam_length"][0]), "seam_per_m": float(g["parts"]["per_m"][0]),
           "scarf_ratio": float(g["parts"]["ratio"][0]),
           "Vc": float(aux["Vc"][0]), "Kc": float(aux["Kc"][0]), "gamma": float(aux["gamma"][0]),
           "sigma_m": float(aux["sigma_m"][0]),
           "modes": {k2: float(v[0]) for k2, v in ev.items()}}
    row["governing"] = min(row["modes"], key=row["modes"].get)
    return row


# ============================================================================ P3
P3_TODAY = {
    # SiC: Saint-Gobain Hexoloy SA (011b/022 values): 3100 kg/m3, 410 GPa, 3900 MPa typical compressive
    # strength carried as the tube allowable (022c 'crush'); 380 MPa four-point flexure is the other sourced value
    "rho": 3100.0, "E": 410e9, "sigma": 3900e6,
    "k": 0.2, "c_local": 0.6, "perry_a": 1.0 / 1000.0, "m_node": 0.02, "local_gamma_fac": 1.0,
}
FILMS = {
    "kapton": {"name": "Kapton HN", "rho": 1420.0, "sigma": 115.5e6, "t_cat": 25.0e-6},     # 024: half of 231 MPa
    "zylon": {"name": "Zylon HM 0/90", "rho": 1560.0, "sigma": 3.48e9, "t_cat": 12.0e-6},   # 024: PROJECTION
}
JOINTS = {"ti": 2.950e-14, "cfrp": 5.807e-15}   # 023 (load fix), kg m / N^2 per member end


def p3_apply(base, film, joint, fac):
    q = dict(base)
    f = lambda k: fac.get(k, 1.0)  # noqa: E731
    q["sigma"] *= f("sic_strength")
    q["E"] *= f("sic_modulus")
    q["rho"] /= f("sic_density")
    q["k"] *= f("lattice_knockdown")
    q["local_gamma_fac"] *= f("local_knockdown")
    q["perry_a"] /= f("straightness")
    q["m_node"] /= f("node_mass")
    q["film_rho"] = film["rho"]
    q["film_sigma"] = film["sigma"] * f("film_specific_strength")
    q["t_cat"] = film["t_cat"]
    q["C"] = JOINTS[joint] / f("joint_mass")
    return q


def cap_sag_lift(s, R=10.0):
    """024 inradius cap (pillow radius s over a triangle of inradius s/(2 sqrt3)); lift lost = L*3*mean/R."""
    base = s / (2.0 * SQRT3)
    h = s - np.sqrt(s * s - base * base)
    mean = h * (3.0 * s - h) / (3.0 * (2.0 * s - h))
    return lift(R) * 3.0 * mean / R


def p3_eval(s, tfilm, ro, q, reserve, R=10.0):
    """Arrays broadcast together. Returns dict of SFs (nan where infeasible) and masses."""
    s = np.asarray(s, dtype=float)
    L = lift(R)
    nodes = 8.0 * math.pi * R * R / (SQRT3 * s * s) + 2.0
    members = 3.0 * nodes - 6.0
    ncoef = R * s / (2.0 * SQRT3)
    N = P0 * ncoef
    coeff = 4.0 * math.sqrt(1.5)
    m_nodes = q["m_node"] * nodes
    m_film = 4.0 * math.pi * R * R * tfilm * q["film_rho"]
    sag = cap_sag_lift(s, R)
    vehicle = L - (reserve + sag)
    m_joint = 2.0 * members * q["C"] * N * N / ro
    m_tube = vehicle - SYS - m_film - m_nodes - m_joint
    length = 2.0 * R * np.arcsin(np.minimum(1.0, 0.5 * s / R))
    area = m_tube / (members * length * q["rho"])
    rmax = np.minimum(0.25, s / 3.0)
    ok = (m_tube > 0) & (area > 0) & (ro * ro > area / math.pi) & (ro <= rmax + 1e-12)
    area_s = np.where(ok, area, 1.0)
    ri = np.sqrt(np.where(ok, ro * ro - area_s / math.pi, 0.0))
    tw = np.where(ok, ro - ri, 1.0)
    inertia = 0.25 * math.pi * (ro ** 4 - ri ** 4)
    inertia = np.where(ok, inertia, 1.0)
    E, sig = q["E"], q["sigma"]
    sf_y = sig * area_s / N
    sf_e = math.pi ** 2 * E * inertia / length ** 2 / N
    rt = np.where(ok, ro / tw, 1.0)
    # SP-8007 local knockdown; a better tube wall can lift it at most to 1 (classical 0.6 E t / r)
    gam = np.minimum(1.0, (1.0 - 0.901 * (1.0 - np.exp(-np.sqrt(rt) / 16.0))) * q["local_gamma_fac"])
    sf_l = q["c_local"] * E * tw / ro * area_s / N * gam
    sf_f = 2.0 * q["film_sigma"] * tfilm / s / P0 * np.ones_like(sf_y)
    rg2 = inertia / area_s
    eta = (length * q["perry_a"]) * ro / rg2
    sig_e = math.pi ** 2 * E * rg2 / length ** 2
    phi = 0.5 * (sig + (eta + 1.0) * sig_e)
    disc = phi * phi - sig * sig_e
    ok = ok & (disc >= 0)
    sig_cr = phi - np.sqrt(np.maximum(disc, 0.0))
    sf_p = sig_cr / (N / area_s)
    sf_g = q["k"] * coeff * E * np.sqrt(inertia * area_s) / (s * R * R) / P0
    sfs = {"yield": sf_y, "euler": sf_e, "local": sf_l, "film": sf_f, "perry": sf_p, "global": sf_g}
    least = np.min(np.stack(np.broadcast_arrays(*sfs.values())), axis=0)
    least = np.where(ok, least, np.nan)
    return {"least": least, "sfs": sfs, "ok": ok, "rt": rt, "gamma_local": gam, "tw": tw,
            "m_tube": m_tube, "m_joint": m_joint, "m_film": m_film, "m_nodes": m_nodes, "sag": sag,
            "area": area, "N": N}


P3_MODES = ("yield", "euler", "local", "film", "perry", "global")


def p3_t_grid(q, reserve, n=12):
    L = L10
    assembly = (L - SYS - reserve) / 1.05
    t_hi = 0.75 * assembly / (4.0 * math.pi * 100.0 * q["film_rho"])
    t_lo = q["t_cat"]
    if t_hi <= t_lo:
        return np.array([t_lo])
    return t_lo * (t_hi / t_lo) ** (np.arange(n) / (n - 1.0))


def p3_grid_search(q, reserve, s_values, n_t=12, n_ro=480):
    """022c's search: s band, film log grid, r_o from r_min to min(0.25, s/3), equilateral, sized joints."""
    best = None
    ts = p3_t_grid(q, reserve, n_t)
    for s in s_values:
        if s >= 20.0:
            continue
        nodes = 8.0 * math.pi * 100.0 / (SQRT3 * s * s) + 2.0
        members = 3.0 * nodes - 6.0
        N = P0 * 10.0 * s / (2.0 * SQRT3)
        rmax = min(0.25, s / 3.0)
        m_nodes = q["m_node"] * nodes
        sag = float(cap_sag_lift(np.array(s)))
        length = 20.0 * math.asin(min(1.0, 0.05 * s))
        structural = L10 - (reserve + sag) - SYS - 4.0 * math.pi * 100.0 * ts * q["film_rho"] - m_nodes
        m_joint_light = 2.0 * members * q["C"] * N * N / rmax
        m_hi = structural - m_joint_light
        area_hi = m_hi / (members * length * q["rho"])
        rmin = np.sqrt(np.maximum(area_hi, 0.0) / math.pi) * 1.0001
        good = (structural > 0) & (m_hi > 0) & (rmax > rmin)
        if not good.any():
            continue
        frac = np.arange(n_ro) / (n_ro - 1.0)
        T = ts[good][:, None] * np.ones((1, n_ro))
        RO = rmin[good][:, None] + (rmax - rmin[good])[:, None] * frac[None, :]
        ev = p3_eval(np.full_like(T, s), T, RO, q, reserve)
        lst = np.where(np.isnan(ev["least"]), -1.0, ev["least"])
        i = np.unravel_index(int(np.argmax(lst)), lst.shape)
        val = lst[i]
        if best is None or val > best["least"]:
            best = {"least": float(val), "s": float(s), "tfilm": float(T[i]), "ro": float(RO[i])}
    return best


def p3_row(q, reserve, s, tfilm, ro):
    ev = p3_eval(np.array([s]), np.array([tfilm]), np.array([ro]), q, reserve)
    sfs = {k: float(np.broadcast_to(v, (1,))[0]) for k, v in ev["sfs"].items()}
    out = {"least": float(ev["least"][0]), "s": s, "tfilm": tfilm, "ro": ro, "tw": float(ev["tw"][0]),
           "rt": float(ev["rt"][0]), "gamma_local": float(ev["gamma_local"][0]), "modes": sfs,
           "m_tube": float(ev["m_tube"][0]), "m_joint": float(ev["m_joint"][0]),
           "m_film": float(np.broadcast_to(ev["m_film"], (1,))[0]), "m_nodes": float(ev["m_nodes"][0]),
           "sag": float(ev["sag"][0])}
    out["governing"] = min(sfs, key=sfs.get)
    return out
