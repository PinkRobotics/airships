#!/usr/bin/env python3
"""MAINLINE-039: the stiffened sandwich sphere. Does a rib grid or a frame buy back gamma?

Own arithmetic, seat ref-55cff924be25afe6f9dd. Baseline: 028b's nominal AF/scarf point (SR-200 Be faces, nu 0.0752,
on Hexcel CR-III 5056 3/8-1.0, 019's fixed reserve, 028's joining), reproduced first. Concepts on the same mass line:
  C1   SR-200 Be tee ribs (isogrid) bonded to the inner face, a = 0.5, 1.0, 2.04 m
  C2   SiC (Hexoloy-SA, 026's E 410 GPa) tubes on 026's s = 2.04 m layout, bonded under the skin seams
  C2b  the same frame in SR-200 Be tubes (CTE-matched to the faces)
Modes: smeared global (two-group shear-flexible core, k-minimised), panel (SP-8032 cap / SS triangle plate), rib crippling,
tube local, rib yield, face compression, wrinkling, crimp, dimpling, crush (uniform and rib-line), core shear at rib
lines, scarf screen, SiC compression, thermal mismatch (C2). Every value is QUESTIONABLE; nothing is a certification.
"""
import datetime
import itertools
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

T_START = datetime.datetime.now().astimezone().isoformat()
T0C = time.monotonic()
OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline039-stiffened-sandwich-1020"

# ---- the case (COMMON.md, 019, 028b) ----
R, P, L0 = 10.0, 95460.83791390515, 4889.442150186961
SYS, RES019, JF = 100.0, 411.2989440716474, 0.05
A = 4 * math.pi * R ** 2
N = P * R / 2                                    # membrane resultant each way, N/m
BIAX = brentq(lambda x: x ** 3 + x - 1, 0, 1, xtol=1e-15)
S3 = math.sqrt(3.0)

FACE = {"E": 290e9, "nu": 0.0752, "rho": 1850.0, "sig_today": 345e6, "sig_full": 379.2e6, "cte": 11.3e-6,
        "src": "Materion SR-200 sheet datasheet (028b sources/sr200.pdf: 290 GPa, 1.85 g/cm3, 11.3 ppm/C); nu21 0.0752 "
               "from the NASA CR-194164 lot; 345 MPa tensile yield used for compression (QUESTIONABLE); 379.2 MPa one lot"}
CORE = {"rho": 16.018463373960138, "Ec": 103421359.3975254, "Gc": 46884349.59354485, "crush": 241316.50526089262,
        "tauW": 241316.50526089262, "cell": 0.009525,
        "src": "Hexcel HexWeb CR-III 5056 3/8-1.0 typical, W direction (028b INPUTS.json; QUESTIONABLE)"}
J028 = {"scarf_ratio": 30.0, "scarf_film": 0.07, "splice_gap": 0.0005, "splice_rho": 500.0, "seal": 0.002,
        "bond": 0.07323641454574575, "panel_a": 0.6096, "panel_b": 1.8288, "scarf_tau": 10e6,
        "src": "028/028b constants (028b INPUTS.json constants, route af015_scarf); formula as 028b calculate.py:31-46"}
SCARF_CAP = J028["scarf_tau"] * (1 + J028["scarf_ratio"] ** 2) / J028["scarf_ratio"]       # 300.333 MPa face stress
SIC = {"E": 410e9, "rho": 3100.0, "sig_c": 3.9e9, "flex4": 380e6, "cte": 4.02e-6,
       "src": "026 INPUTS (E 410 GPa inherited, 3100 kg/m3, 3.9 GPa typical compression); Hexoloy-SA datasheet archived "
              "in 026 sources (4-pt flexural 380 MPa, CTE 4.02 ppm/K); typical values, not allowables (QUESTIONABLE)"}
DT_CLIMATE = 25.1                                # 019's larger climate swing, K
LOCAL_COEFF = 0.6                                # 026/011b inherited tube local coefficient, times SP-8007 gamma (FIX-B)
SLEEVE_023 = (157.7, 562.2e3)                    # 023 (030 register R064): Ti sleeves 157.7 kg at 562.2 kN
NODES_026 = (362, 0.02)                          # 026: 362 joints, 0.02 kg node allowance each

# knockdown record (LIT-STIFF.json; load-bearing values verified at source by this seat)
GAMMA_SANDWICH_TODAY = 0.20                      # CR-1457 step for Vc < 2 (the line's today)
GAMMA_IDH_HEAVY = 0.425                          # Isogrid Design Handbook CR-124075A p.4.1.012, heavily stiffened domes
GAMMA_GEODESIC_BEST = 0.377 / 0.6125             # CR-62257 plastic geodesic cap 2-G: C 0.377 against classical 0.6125
GAMMA_FRAME_026 = 0.702                          # 026 nonlinear, 10 mm first-mode imperfection (computed, PROJECTION)
PANEL_TODAY_CAP = 1 / 1.2380                     # Pineda 2014 fairing panels: eigenvalue 2.85-23.80% above test (035, CHECK-035 E13)
PANEL_FULL = 1 / 1.0285                          # the 2.85% end (CHECK-035 E13)
Q_TODAY, Q_FULL = 0.33, 0.82
TF_MIN = 0.25e-3                                 # sheet floor for the search (QUESTIONABLE)
GAMMA_S_MIN = 10.0                               # adequacy: stiffener rigidity EI_e/(a D_skin) for nodal lines (assumed)
LAMBDA_REGIME1 = 1.165                           # lambda_p at which the skin's natural wavelength equals 2a (rigid core)
V028 = {"gamma_g": 0.564164, "Q": 0.434628, "panel_cap_sphere": 0.564164}   # 028b's two needed values, same claims
FACTORS = ("gamma_g", "gamma_p", "Q", "sigma")
HARD = ("crimp", "dimple", "crush_uniform", "crush_rib_line", "scarf_screen", "core_shear_rib_line", "rib_crippling",
        "tube_local", "sic_compression")


def sp8007(r_over_t):
    return 1 - 0.901 * (1 - np.exp(-np.sqrt(r_over_t) / 16))


def sp8032_cap(lam):
    """SP-8032 Eq. 4 (and Eq. 19 for stiffened domes): lower bound for clamped caps, stated for lambda > 2."""
    return 0.14 + 3.2 / lam ** 2


def skin_joining(tf, tc):
    """028b's physical joining bill for the AF/scarf route, own implementation of the same formula."""
    k = J028
    overlap = k["scarf_ratio"] * tf
    length = A * (1 / (k["panel_a"] - overlap) + 1 / (k["panel_b"] - overlap))
    scarf_mu = 2 * tf * math.hypot(1, k["scarf_ratio"]) * k["scarf_film"]
    core_mu = k["splice_gap"] * tc * k["splice_rho"]
    bond = 2 * A * k["bond"]
    return {"bond": bond + 0 * tf, "scarf_film": length * scarf_mu, "core_splice": length * core_mu,
            "seal": length * k["seal"], "seam_m": length, "total": bond + length * (scarf_mu + core_mu + k["seal"])}


# ---- lattice sections; joining(tf, tc) needs the skin to find the member force ----
def tee_section(m_rib, a, aspect, w_foot=0.025, t_foot=0.0005):
    """SR-200 tee: blade b x d on a foot w_foot x t_foot bonded with one AF line; member length per area 2*sqrt3/a."""
    mat = FACE
    L = A * 2 * S3 / a
    A_tot = m_rib / (mat["rho"] * L)
    Af = w_foot * t_foot
    A_bl = np.maximum(A_tot - Af, 1e-12)
    b = np.sqrt(A_bl / aspect)
    d = aspect * b
    zc = (Af * t_foot / 2 + b * d * (t_foot + d / 2)) / (Af + b * d)
    I = w_foot * t_foot ** 3 / 12 + Af * (zc - t_foot / 2) ** 2 + b * d ** 3 / 12 + b * d * (t_foot + d / 2 - zc) ** 2
    bond = L * w_foot * J028["bond"]
    return {"kind": "tee", "A": Af + b * d, "I": I, "zc": zc, "E": mat["E"], "nu_m": mat["nu"], "b": b, "d": d, "L": L,
            "ok": A_tot > 1.05 * Af, "w_bond": w_foot,
            "parts": {"rib_bond_film": bond + 0 * m_rib, "rib_splices_nodes_5pct": 0.05 * m_rib},
            "joining": bond + 0.05 * m_rib}


def tube_section(m_fr, a, r_over_t, mat, tf):
    """Thin round tube tangent to the inner face; 30 mm AF land plus two 5 mm paste fillets (QUESTIONABLE);
    023's sleeves scaled by this frame's member force; 026's node allowance."""
    L = A * 2 * S3 / a
    A_t = m_fr / (mat["rho"] * L)
    t = np.sqrt(A_t / (math.pi * (2 * r_over_t - 1)))
    ro = r_over_t * t
    ri = ro - t
    I = math.pi / 4 * (ro ** 4 - ri ** 4)
    eps = N / (2 * FACE["E"] * tf / (1 - FACE["nu"]) + S3 * mat["E"] * A_t / a)
    F = mat["E"] * A_t * eps
    sleeves = SLEEVE_023[0] * F / SLEEVE_023[1]
    bond = L * (0.03 * J028["bond"] + 2 * 0.5 * 0.005 ** 2 * 1250.0)
    nodes = NODES_026[0] * NODES_026[1]
    return {"kind": "tube", "A": A_t, "I": I, "zc": ro, "E": mat["E"], "ro": ro, "t": t, "L": L, "ok": A_t > 0,
            "w_bond": 0.03, "F": F, "parts": {"frame_bond": bond + 0 * m_fr, "sleeves_023_scaled": sleeves,
                                               "nodes_026": nodes + 0 * m_fr},
            "joining": bond + sleeves + nodes}


def make_section(concept, a, shape, m_lat, tf):
    if concept == "C1":
        return tee_section(m_lat, a, shape)
    if concept == "C2":
        return tube_section(m_lat, a, shape, SIC, tf)
    if concept == "C2b":
        return tube_section(m_lat, a, shape, FACE, tf)
    return None


def close_mass(concept, a, shape, f_lat, f_core, lift):
    """Bisection on structural mass S = faces + core + lattice so S + max(5% S, joining) + 100 + 411.299 = lift."""
    lo = np.zeros_like(f_lat)
    hi = np.full_like(f_lat, lift)
    for _ in range(64):
        S = (lo + hi) / 2
        m_lat = f_lat * S
        skin = S - m_lat
        tc = f_core * skin / (A * CORE["rho"])
        tf = (1 - f_core) * skin / (2 * A * FACE["rho"])
        sec = make_section(concept, a, shape, m_lat, tf)
        J = skin_joining(tf, tc)["total"] + (sec["joining"] if sec is not None else 0.0)
        over = S + np.maximum(JF * S, J) + SYS + RES019 > lift
        hi = np.where(over, S, hi)
        lo = np.where(over, lo, S)
    S = lo
    m_lat = f_lat * S
    skin = S - m_lat
    tc = f_core * skin / (A * CORE["rho"])
    tf = (1 - f_core) * skin / (2 * A * FACE["rho"])
    return S, m_lat, tf, tc, make_section(concept, a, shape, m_lat, tf)


# ---- the structural model ----
def kmin(D0, Ds, S, Y, kmax=None, n=400):
    """min over k of N(k) = (D0 + Ds/(1 + Ds k^2/S)) k^2 + Y/(R^2 k^2): log grid, then golden refinement."""
    kn = (Y / (np.maximum(D0 + Ds, 1e-30) * R ** 2)) ** 0.25
    lo = np.log(kn) - 5.0
    hi = np.log(kn) + 5.0
    if kmax is not None:
        hi = np.minimum(hi, math.log(kmax))
        lo = np.minimum(lo, hi - 1e-6)

    def fn(x):
        kk = np.exp(2 * x)
        return (D0 + Ds / (1 + Ds * kk / S)) * kk + Y / (R ** 2 * kk)
    g = np.linspace(0, 1, n)[:, None]
    f = fn(lo + (hi - lo) * g)
    i = np.argmin(f, axis=0)
    step = (hi - lo) / (n - 1)
    a_ = lo + step * np.maximum(i - 1, 0)
    b_ = lo + step * np.minimum(i + 1, n - 1)
    gr = (math.sqrt(5) - 1) / 2
    for _ in range(50):
        c = b_ - gr * (b_ - a_)
        d = a_ + gr * (b_ - a_)
        sel = fn(c) < fn(d)
        b_ = np.where(sel, d, b_)
        a_ = np.where(sel, a_, c)
    x = (a_ + b_) / 2
    return fn(x), np.exp(x)


def evaluate(tf, tc, sec, a, concept):
    E, nu = FACE["E"], FACE["nu"]
    h = tc + tf
    C11f = E * tf / (1 - nu ** 2)
    Bf = E * tf / (1 - nu)                                          # one face, equal biaxial
    if sec is None:
        C11r = Br = D11r = zr = 0.0 * tf
        Er = 0.0
    else:
        Er = sec["E"]
        C11r = (3 * S3 / 4) * Er * sec["A"] / a                      # triangulated lattice, nu 1/3
        Br = S3 * Er * sec["A"] / a
        D11r = (3 * S3 / 4) * Er * sec["I"] / a
        zr = -(h / 2 + tf / 2 + sec["zc"])
    Bt = 2 * Bf + Br
    eps = N / Bt
    fr = Br / Bt
    sig_f = E * eps / (1 - nu)
    sig_r = Er * eps
    th_face = 0 * tf
    th_rib = 0 * tf
    if concept == "C2":                                             # Be on SiC, adverse direction of the climate swing
        de = (FACE["cte"] - SIC["cte"]) * DT_CLIMATE
        th_face = E / (1 - nu) * de * fr
        th_rib = SIC["E"] * de * (1 - fr)
    # two-group global model: G1 outer face; G2 inner face + lattice; shear-flexible core between them
    C2 = C11f + C11r
    z2 = (C11f * (-h / 2) + C11r * zr) / C2
    D0 = D11r + C11f * (-h / 2 - z2) ** 2 + C11r * (zr - z2) ** 2
    d12 = h / 2 - z2
    Ds = C11f * C2 / (C11f + C2) * d12 ** 2
    Sg = CORE["Gc"] * d12 ** 2 / tc
    C11t = 2 * C11f + C11r
    C12t = 2 * nu * C11f + C11r / 3
    Y = (C11t ** 2 - C12t ** 2) / C11t
    Ng, kg = kmin(D0, Ds, Sg, Y)
    Ngr, kgr = (Ng, kg) if sec is None else kmin(D0, Ds, Sg, Y, kmax=math.pi / a)
    s0 = E * h / (R * math.sqrt(1 - nu ** 2))
    scr = h * h * CORE["Gc"] / (2 * tf * tc)
    Vc = s0 / scr
    Kc = np.where(Vc <= 2, 1 - Vc / 4, 1 / Vc)
    Ds_skin = E * tf * h * h / (2 * (1 - nu ** 2))
    Nsph = Kc * 2 * np.sqrt(Ds_skin * 2 * E * tf) / R
    Drig = D0 + Ds
    ev = {"h": h, "eps": eps, "fr": fr, "sig_f": sig_f, "sig_r": sig_r + th_rib, "th_face": th_face, "Vc": Vc, "Kc": Kc,
          "Ng": Ng, "Ngr": Ngr, "lam_g": 2 * math.pi / kg, "lam_gr": 2 * math.pi / kgr, "psi": Drig / Ds_skin,
          "teq": np.sqrt(12 * Drig / Y), "Nsph_skin": Nsph, "Ns": 2 * Bf * eps, "Y": Y, "D_rigid": Drig,
          "crush_uniform": P * (Bf + Br) / Bt}
    if sec is not None:
        re = math.sqrt(S3 / (4 * math.pi)) * a                       # equal-area circle of the triangle
        lam = (12 * (1 - nu ** 2)) ** 0.25 * re / np.sqrt(R * S3 * h)
        kt = 16 * math.pi ** 2 / (3 * a * a)                         # SS equilateral triangle, equal biaxial load
        Sk = CORE["Gc"] * h * h / tc
        Npl = kt * Ds_skin / (1 + kt * Ds_skin / Sk)
        at = S3 / 2 * a                                              # altitude; SS triangle centre moment (1+nu) q at^2/54
        sig_b = (1 + nu) * fr * P * at ** 2 / 54 / (tf * h)
        q_line = sec["E"] * sec["A"] * eps / R                       # = fr P a/(2 sqrt3), skin onto lattice line
        w_eff = sec["w_bond"] + 2 * h
        ev.update({"lam_panel": lam, "N_plate": Npl, "N_panel_cl": np.maximum(Nsph, Npl), "sig_b": sig_b,
                   "q_line": q_line, "crush_line": P * (Bf / Bt) + q_line / w_eff, "tau_line": (q_line / 2) / h})
    else:
        ev.update({"sig_b": 0 * tf, "crush_line": P * Bf / Bt, "tau_line": 0 * tf})
    return ev


def modes(tf, tc, sec, ev):
    """Base SF per mode: SF = factor x base for factor-linked modes, SF = base for hard modes."""
    E, nu = FACE["E"], FACE["nu"]
    sig_face = ev["sig_f"] + ev["sig_b"] + ev["th_face"]
    m = {"global": ev["Ngr"] / N, "global_unrestricted": ev["Ng"] / N,
         "face_per_Pa": 1 / sig_face,
         "wrinkle_per_Q": BIAX * np.sqrt(E * CORE["Ec"] * tf / tc) / sig_face,
         "crimp": (ev["h"] ** 2 * CORE["Gc"] / (2 * tf * tc)) / sig_face,
         "dimple": E / (1 - nu ** 2) * (tf / CORE["cell"]) ** 2 / sig_face,
         "crush_uniform": CORE["crush"] / ev["crush_uniform"],
         "crush_rib_line": CORE["crush"] / ev["crush_line"],
         "scarf_screen": SCARF_CAP / sig_face}
    if sec is not None:
        # bay/skin mode: an adequate lattice (gamma_s >= GAMMA_S_MIN) gives rigid nodal lines (cap or SS-triangle plate);
        # an inadequate one gives no bay: if the skin's own dimple fits between lines (lambda_p > LAMBDA_REGIME1) the skin
        # buckles alone, else the ribs must bend with it and the smeared general mode covers it
        adequate = (ev["psi"] - 1) / (3 * S3 / 4) >= GAMMA_S_MIN
        regime1 = ev["lam_panel"] <= LAMBDA_REGIME1
        nb = np.where(adequate, ev["N_panel_cl"], np.where(regime1, 1e9 * ev["Ns"], ev["Nsph_skin"]))
        m["panel"] = nb / ev["Ns"]
        m["core_shear_rib_line"] = CORE["tauW"] / np.maximum(ev["tau_line"], 1e-9)
        if sec["kind"] == "tee":
            m["rib_crippling"] = (0.43 * math.pi ** 2 * sec["E"] / (12 * (1 - sec["nu_m"] ** 2)) * (sec["b"] / sec["d"]) ** 2
                                  / ev["sig_r"])
            m["rib_per_Pa"] = 1 / ev["sig_r"]
        else:
            m["tube_local"] = sp8007(sec["ro"] / sec["t"]) * LOCAL_COEFF * sec["E"] * sec["t"] / sec["ro"] / ev["sig_r"]
            if sec["E"] == SIC["E"]:
                m["sic_compression"] = SIC["sig_c"] / ev["sig_r"]
            else:
                m["rib_per_Pa"] = 1 / ev["sig_r"]
    return m, sig_face


def today_full(ev, sec, concept, psi_heavy):
    """Today and full endpoints of each named factor, per design.
    Global: 0.20 (sandwich record) unless heavily stiffened (psi at least the IDH test dome's) -> 0.425 (IDH).
    Panel: bays with lambda_p <= 2 are plate-like (sandwich panel record 0.806 / 0.971); larger bays hold the skin's own
    dimple, so they take the sphere record (0.20 / 018 curve) unless O5 (adequate frame, gamma_s >= GAMMA_S_MIN): then
    the SP-8032 clamped-cap curve capped by the panel record (today) and 0.971 (full)."""
    if sec is None:
        heavy = np.zeros_like(ev["psi"], dtype=bool)
        g_today = np.where(ev["Vc"] < 2, GAMMA_SANDWICH_TODAY, 1.0)
    else:
        heavy = ev["psi"] >= psi_heavy
        g_today = np.full_like(ev["psi"], GAMMA_SANDWICH_TODAY)
    g_018 = 0.2 + 0.4 * np.minimum(ev["Vc"], 2)
    stiff_full = GAMMA_FRAME_026 if concept in ("C2", "C2b") else GAMMA_GEODESIC_BEST
    g_today = np.where(heavy, GAMMA_IDH_HEAVY, g_today)
    g_full = np.where(heavy, stiff_full, g_018)
    one = np.ones_like(ev["psi"])
    if sec is not None:
        lam = ev["lam_panel"]
        cap = lam > 2
        adequate = (ev["psi"] - 1) / (3 * S3 / 4) >= GAMMA_S_MIN
        plate = adequate & ~cap
        o5cap = adequate & cap
        p_today = np.where(plate, PANEL_TODAY_CAP, GAMMA_SANDWICH_TODAY)
        p_full = np.where(plate, PANEL_FULL, g_018)
        p5_today = np.where(o5cap, np.minimum(sp8032_cap(np.maximum(lam, 2)), PANEL_TODAY_CAP), p_today)
        p5_full = np.where(o5cap, PANEL_FULL, p_full)
        gamma_s = (ev["psi"] - 1) / (3 * S3 / 4)
    else:
        cap = plate = o5cap = adequate = np.zeros_like(ev["psi"], dtype=bool)
        p_today, p_full = PANEL_TODAY_CAP * one, PANEL_FULL * one
        p5_today, p5_full = p_today, p_full
        gamma_s = np.zeros_like(ev["psi"])
    return {"gamma_g": (g_today, g_full), "gamma_p": (p_today, p_full), "gamma_p_O5": (p5_today, p5_full),
            "Q": (Q_TODAY * one, Q_FULL * one), "sigma": (FACE["sig_today"] * one, FACE["sig_full"] * one),
            "heavy": heavy, "cap_regime": cap, "gamma_s": gamma_s, "adequate": adequate, "panel_sphere": ~plate,
            "o5cap": o5cap}


def endpoints(tfv, fct, o5):
    """Endpoints of a factor; with O5 the panel takes the clamped-cap endpoints where the frame is adequate."""
    if fct == "gamma_p" and o5:
        return tfv["gamma_p_O5"]
    return tfv[fct]


def needs(m):
    g = m["global"]
    out = {"gamma_g": 1 / g, "Q": 1 / m["wrinkle_per_Q"], "sigma": 1 / m["face_per_Pa"]}
    if "rib_per_Pa" in m:
        out["sigma"] = np.maximum(out["sigma"], 1 / m["rib_per_Pa"])
    out["gamma_p"] = 1 / m["panel"] if "panel" in m else 0 * g
    return out


def log_usage(need, today, full):
    with np.errstate(divide="ignore", invalid="ignore"):
        raw = np.log(need / today) / np.log(full / today)
    return np.where(need <= today * (1 + 1e-12), 0.0, np.where(full > today * (1 + 1e-12), raw, np.inf))


def hard_min(m, seam=True):
    return np.minimum.reduce([m[k] for k in HARD if k in m and (seam or k != "scarf_screen")])


def design_space(concept):
    fc = np.concatenate([np.linspace(0.003, 0.06, 24), np.linspace(0.065, 0.6, 60)])
    if concept == "baseline":
        return np.array([0.0]), np.linspace(0.003, 0.6, 3000), [None]
    if concept == "C1":
        return np.linspace(0.005, 0.55, 56), fc, [3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0]
    return np.linspace(0.005, 0.55, 56), fc, [30.0, 40.0, 60.0, 80.0, 100.0, 150.0, 200.0, 300.0]


def run_concept(concept, a, psi_heavy, lift=L0):
    fl, fc, shapes = design_space(concept)
    rows = []
    for shape in shapes:
        FL, FC = np.meshgrid(fl, fc, indexing="ij")
        FL, FC = FL.ravel(), FC.ravel()
        S, m_lat, tf, tc, sec = close_mass(concept, a, shape, FL, FC, lift)
        ev = evaluate(tf, tc, sec, a, concept)
        m, sig_face = modes(tf, tc, sec, ev)
        valid = (tf >= TF_MIN) & (tc > 0)
        if sec is not None:
            valid &= sec["ok"]
        rows.append({"concept": concept, "a": a, "shape": shape, "FL": FL, "FC": FC, "S": S, "m_lat": m_lat, "tf": tf,
                     "tc": tc, "sec": sec, "ev": ev, "m": m, "tfv": today_full(ev, sec, concept, psi_heavy),
                     "valid": valid, "sig_face": sig_face})
    return rows


def sf_table(row, o5=False, seam=True, over=None):
    """Mode SFs at today's endpoints (or with `over` values) for every design in a row."""
    m, tfv = row["m"], row["tfv"]
    val = {f: endpoints(tfv, f, o5)[0] for f in FACTORS}
    for f, v in (over or {}).items():
        if f == "panel_cap_sphere":
            use = tfv["panel_sphere"] & ~(tfv["o5cap"] & o5)
            val["gamma_p"] = np.where(use, v, val["gamma_p"])
        else:
            val[f] = v * np.ones_like(row["tf"])
    sfs = {"global": val["gamma_g"] * m["global"], "face": val["sigma"] * m["face_per_Pa"],
           "wrinkle": val["Q"] * m["wrinkle_per_Q"]}
    if "panel" in m:
        sfs["panel"] = val["gamma_p"] * m["panel"]
    if "rib_per_Pa" in m:
        sfs["rib_yield"] = val["sigma"] * m["rib_per_Pa"]
    for k in HARD:
        if k in m and (seam or k != "scarf_screen"):
            sfs[k] = m[k]
    names = list(sfs)
    arr = np.vstack([sfs[k] for k in names])
    least = np.where(row["valid"], np.min(arr, axis=0), -np.inf)
    return least, np.array(names)[np.argmin(arr, axis=0)], sfs


def pick(row, i):
    ev, m, sec = row["ev"], row["m"], row["sec"]
    f = lambda v: float(np.asarray(v)[i]) if np.ndim(v) else float(v)
    rec = {"concept": row["concept"], "a_m": row["a"], "shape": row["shape"], "f_lattice": f(row["FL"]),
           "f_core": f(row["FC"]), "tf_mm": f(row["tf"]) * 1e3, "tc_mm": f(row["tc"]) * 1e3, "S_kg": f(row["S"]),
           "lattice_kg": f(row["m_lat"]), "sig_face_MPa": f(row["sig_face"]) / 1e6, "heavy": bool(row["tfv"]["heavy"][i])}
    for k in ("Vc", "Kc", "psi", "teq", "lam_g", "lam_gr", "fr", "sig_f", "sig_r", "th_face", "eps", "Ng", "Ngr",
              "Nsph_skin", "Ns", "sig_b", "lam_panel", "N_plate", "N_panel_cl", "q_line", "crush_line", "tau_line"):
        if k in ev:
            rec[k] = f(ev[k])
    rec["base"] = {k: f(v) for k, v in m.items()}
    rec["today_full"] = {k: [f(v[0]), f(v[1])] for k, v in row["tfv"].items() if isinstance(v, tuple)}
    rec["cap_regime"] = bool(row["tfv"]["cap_regime"][i])
    rec["adequate"] = bool(row["tfv"]["adequate"][i])
    rec["gamma_s"] = f(row["tfv"]["gamma_s"])
    sj = skin_joining(row["tf"][i], row["tc"][i])
    lj = 0.0
    if sec is not None:
        rec["section"] = {k: f(sec[k]) for k in ("A", "I", "zc", "b", "d", "ro", "t", "F") if k in sec}
        rec["section"]["kind"] = sec["kind"]
        rec["section"]["shape_param"] = row["shape"]
        rec["lattice_joining_parts"] = {k: f(v) for k, v in sec["parts"].items()}
        lj = f(sec["joining"])
    S = f(row["S"])
    J = float(sj["total"]) + lj
    rec["masses"] = {"faces": 2 * A * FACE["rho"] * f(row["tf"]), "core": A * CORE["rho"] * f(row["tc"]),
                     "lattice": f(row["m_lat"]), "skin_joining": float(sj["total"]),
                     "skin_joining_parts": {k: float(v) for k, v in sj.items() if k != "total"},
                     "lattice_joining": lj, "joining_physical": J, "joint_allowance_5pct": JF * S,
                     "joint_charged": max(JF * S, J), "joint_excess": max(0.0, J - JF * S), "systems": SYS,
                     "reserve_019_fixed": RES019, "total": S + max(JF * S, J) + SYS + RES019}
    return rec


def best(rows, o5=False, seam=True, over=None):
    top = None
    for row in rows:
        least, gov, sfs = sf_table(row, o5, seam, over)
        i = int(np.argmax(least))
        if top is None or least[i] > top[0]:
            top = (float(least[i]), str(gov[i]), row, i, {k: float(v[i]) for k, v in sfs.items()})
    v, g, row, i, sfs = top
    rec = pick(row, i)
    rec.update({"least_SF": v, "governs": g, "SF": sfs, "O5_frame_bay": o5, "seam_screen": seam, "over": over})
    return rec


def least_sets(rows, o5_allowed, seam=True):
    """028b's rule: per factor subset, min over designs of the max log-usage; unselected factors at today; hard >= 1."""
    concept = rows[0]["concept"]
    facs = [f for f in FACTORS if not (f == "gamma_p" and concept == "baseline")]
    opts = facs + (["O5_frame_bay"] if o5_allowed else [])
    cands = []
    for r in range(0, len(opts) + 1):
        for sub in itertools.combinations(opts, r):
            o5 = "O5_frame_bay" in sub
            top = None
            for row in rows:
                m, tfv = row["m"], row["tfv"]
                nd = needs(m)
                ok = row["valid"] & (hard_min(m, seam) >= 1 - 1e-12)
                obj = np.zeros_like(row["tf"])
                for fct in facs:
                    today, full = endpoints(tfv, fct, o5)
                    if fct in sub:
                        obj = np.maximum(obj, log_usage(nd[fct], today, full))
                    else:
                        ok &= nd[fct] <= today * (1 + 1e-12)
                obj = np.where(ok & (obj <= 1 + 1e-12), obj, np.inf)
                i = int(np.argmin(obj))
                if np.isfinite(obj[i]) and (top is None or obj[i] < top[0]):
                    top = (float(obj[i]), row, i, {fct: float(nd[fct][i]) for fct in facs})
            if top is not None:
                u, row, i, need = top
                rec = pick(row, i)
                today_i = {fct: float(endpoints(row["tfv"], fct, o5)[0][i]) for fct in facs}
                rec.update({"subset": list(sub), "max_usage": u, "needed": need, "today_at_point": today_i,
                            "needed_over_today": {fct: need[fct] / today_i[fct] for fct in facs}, "seam_screen": seam})
                cands.append(rec)
    if not cands:
        return None, []
    least = sorted(cands, key=lambda c: (len(c["subset"]), c["max_usage"]))[0]
    return least, sorted(cands, key=lambda c: (len(c["subset"]), c["max_usage"]))


def lift_shift_to_sf1(concept, a, psi_heavy, o5=False, seam=True, over=None, lo=-3000.0, hi=25000.0, it=20):
    """Lift change (kg) at which the best least SF is exactly 1 (negative = mass to spare), with the design found there."""
    def top(shift):
        return max(float(np.max(sf_table(r, o5, seam, over)[0])) for r in run_concept(concept, a, psi_heavy, L0 + shift))
    if top(hi) < 1:
        return {"shift_kg": float("inf"), "design": None}
    if top(lo) < 1:
        for _ in range(it):
            mid = (lo + hi) / 2
            if top(mid) >= 1:
                hi = mid
            else:
                lo = mid
        shift = hi
    else:
        shift = lo
    d = best(run_concept(concept, a, psi_heavy, L0 + shift), o5, seam, over)
    keep = ("least_SF", "governs", "tf_mm", "tc_mm", "lattice_kg", "psi", "gamma_s", "heavy", "adequate", "lam_panel",
            "sig_face_MPa", "section", "masses", "SF")
    return {"shift_kg": shift, "design": {k: d.get(k) for k in keep}}


def record_psi():
    """psi = composite bending / own skin bending for the record domes (CR-62257 design values, inches)."""
    out = {}
    for name, (a_, d_, b_, t_, nu) in {"aluminium_dome_IDH_ref_1-1": (1.65, 0.166, 0.10, 0.0375, 0.33),
                                       "plastic_1-G": (1.57, 0.23, 0.0191, 0.0474, 0.35),
                                       "plastic_2-G": (1.6, 0.226, 0.0239, 0.0479, 0.35),
                                       "plastic_3-G": (1.25, 0.205, 0.0153, 0.0296, 0.35)}.items():
        C11s = t_ / (1 - nu ** 2)
        Ds = t_ ** 3 / (12 * (1 - nu ** 2))
        C11r = (3 * S3 / 4) * b_ * d_ / a_
        D11r = (3 * S3 / 4) * b_ * d_ ** 3 / 12 / a_
        zr = -(t_ / 2 + d_ / 2)
        zbar = C11r * zr / (C11s + C11r)
        out[name] = (Ds + C11s * zbar ** 2 + D11r + C11r * (zr - zbar) ** 2) / Ds
    return out


def main():
    quick = "--quick" in sys.argv
    global GAMMA_S_MIN
    if "--gs" in sys.argv:
        GAMMA_S_MIN = float(sys.argv[sys.argv.index("--gs") + 1])
    res = {"schema": 1, "card": "MAINLINE-039", "unit": "vacuum-mainline039-stiffened-sandwich-1020",
           "tag": "QUESTIONABLE", "certification": False, "started_local": T_START,
           "constants": {"FACE": FACE, "CORE": CORE, "J028": J028, "SCARF_CAP_Pa": SCARF_CAP, "SIC": SIC,
                         "DT_CLIMATE_K": DT_CLIMATE, "LOCAL_COEFF": LOCAL_COEFF, "SLEEVE_023": SLEEVE_023,
                         "NODES_026": NODES_026, "GAMMA_SANDWICH_TODAY": GAMMA_SANDWICH_TODAY,
                         "GAMMA_IDH_HEAVY": GAMMA_IDH_HEAVY, "GAMMA_GEODESIC_BEST": GAMMA_GEODESIC_BEST,
                         "GAMMA_FRAME_026": GAMMA_FRAME_026, "PANEL_TODAY_CAP": PANEL_TODAY_CAP, "PANEL_FULL": PANEL_FULL,
                         "Q": [Q_TODAY, Q_FULL], "TF_MIN_m": TF_MIN, "BIAX": BIAX}}
    # 1. reproduce 028b's nominal AF/scarf point (nu 0.0752 headline)
    tf0, tc0 = np.array([0.0007946240669858892]), np.array([0.02323721790601576])
    ev0 = evaluate(tf0, tc0, None, None, "baseline")
    m0, _ = modes(tf0, tc0, None, ev0)
    sj0 = skin_joining(tf0[0], tc0[0])
    rep = {"Vc": float(ev0["Vc"][0]), "gamma_needed": float(1 / m0["global"][0]), "Q_needed": float(1 / m0["wrinkle_per_Q"][0]),
           "crimp": float(m0["crimp"][0]), "dimple": float(m0["dimple"][0]), "crush": float(m0["crush_uniform"][0]),
           "scarf": float(m0["scarf_screen"][0]), "face_SF_345": float(345e6 * m0["face_per_Pa"][0]),
           "teq_mm": float(ev0["teq"][0] * 1e3), "global_wavelength_m": float(ev0["lam_g"][0]),
           "joining": {k: float(v) for k, v in sj0.items()},
           "target_028b_card": {"gamma": 0.564164, "Q": 0.434628, "Vc": 0.953214, "joining": 215.742, "crimp": 2.441308,
                                "dimple": 6.758508, "crush": 5.055822, "face": 1.148724, "scarf": 1.0}}
    res["reproduce_028b"] = rep
    print("028b reproduced:", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in rep.items() if k != "joining"},
          "joining", round(sj0["total"], 3))
    psi = record_psi()
    res["psi_record_domes"] = psi
    psi_heavy = psi["aluminium_dome_IDH_ref_1-1"]
    print("psi of the record domes:", {k: round(v, 2) for k, v in psi.items()})
    concepts = [("baseline", None), ("C1", 0.5), ("C1", 1.0), ("C1", 2.04), ("C2", 2.04), ("C2b", 2.04)]
    res["concepts"] = []
    keep = ("subset", "max_usage", "needed", "today_at_point", "needed_over_today", "lattice_kg", "tf_mm", "tc_mm",
            "psi", "gamma_s", "heavy", "cap_regime", "governs")
    for concept, a in concepts:
        t1 = time.monotonic()
        lat = concept != "baseline"
        rows = run_concept(concept, a, psi_heavy)
        e = {"concept": concept, "a_m": a,
             "best_today": best(rows), "best_today_six_modes": best(rows, seam=False),
             "best_at_028b_values": best(rows, over=V028)}
        if lat:
            e["best_today_O5"] = best(rows, o5=True)
        for tag, seam in (("seam", True), ("six_modes", False)):
            ls, allsets = least_sets(rows, o5_allowed=lat, seam=seam)
            e["least_set_" + tag] = ls
            e["sets_" + tag] = [{k: c.get(k) for k in keep} for c in allsets]
        if not quick:
            e["lift_shift_kg"] = {"today": lift_shift_to_sf1(concept, a, psi_heavy),
                                  "at_028b_values": lift_shift_to_sf1(concept, a, psi_heavy, over=V028),
                                  "today_six_modes": lift_shift_to_sf1(concept, a, psi_heavy, seam=False)}
            if lat:
                e["lift_shift_kg"]["today_O5"] = lift_shift_to_sf1(concept, a, psi_heavy, o5=True)
        e["elapsed_s"] = time.monotonic() - t1
        res["concepts"].append(e)
        print(f"\n== {concept} a={a}")
        for key in ("best_today", "best_today_six_modes", "best_at_028b_values", "best_today_O5"):
            if key in e:
                b = e[key]
                print(f"   {key:22s} least {b['least_SF']:.4f} ({b['governs']}) tf {b['tf_mm']:.3f} tc {b['tc_mm']:.2f} "
                      f"lattice {b['lattice_kg']:.1f} psi {b['psi']:.2f} g_s {b['gamma_s']:.2f} cap {b.get('cap_regime')} "
                      f"lam_p {b.get('lam_panel', float('nan')):.2f} lam_g {b['lam_gr']:.2f}")
        for tag in ("seam", "six_modes"):
            ls = e["least_set_" + tag]
            if ls:
                print(f"   least set [{tag}] {ls['subset']} usage {ls['max_usage']:.4f} need/today "
                      f"{ {k: round(v, 3) for k, v in ls['needed_over_today'].items()} } lattice {ls['lattice_kg']:.1f} "
                      f"tf {ls['tf_mm']:.3f} tc {ls['tc_mm']:.2f}")
            else:
                print(f"   least set [{tag}] none within the full endpoints")
            for c in e["sets_" + tag][:5]:
                print(f"      {str(c['subset']):50s} {c['max_usage']:.4f} lattice {c['lattice_kg']:.1f} psi {c['psi']:.2f}")
        if "lift_shift_kg" in e:
            print("   lift shift for SF 1 (kg):", {k: round(v["shift_kg"], 1) for k, v in e["lift_shift_kg"].items()})
            for k, v in e["lift_shift_kg"].items():
                d = v["design"]
                if d:
                    print(f"      {k:16s} lattice {d['lattice_kg']:.0f} tf {d['tf_mm']:.3f} tc {d['tc_mm']:.2f} psi {d['psi']:.2f} "
                          f"g_s {d['gamma_s']:.2f} governs {d['governs']}")
        print(f"   ({e['elapsed_s']:.1f} s)")
    res["ended_local"] = datetime.datetime.now().astimezone().isoformat()
    res["elapsed_s"] = time.monotonic() - T0C
    OUT.mkdir(parents=True, exist_ok=True)
    name = ("RUNS-quick" if quick else "RUNS") + ("" if GAMMA_S_MIN == 10.0 else f"-gs{GAMMA_S_MIN:g}") + ".json"
    res["GAMMA_S_MIN"] = GAMMA_S_MIN
    (OUT / name).write_text(json.dumps(res, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))


if __name__ == "__main__":
    main()
