#!/usr/bin/env python3
"""SHIP-2 — the film-on-rings wall, checked, priced, and the two verdicts.

    python3 tools/ship_scoping.py [--json [PATH]]

The operator's 08-12/08-13 cascade replaced the Kelvin band with a wall that is nothing
but structure and one membrane: hoop rings at panel pitch, continuous meridional
cross-bars one diameter outboard, film laid straight on them, split-Ti clamps at one
crossing in four. This tool is the cascade's bill. It answers the two questions the
project exists to answer, at ship 0's plan of record (52 m x 104 m, sea level):

    DOES IT STAND?  — every named check, margin by margin, at the declared SF 1.2
                      with SF 1.5 always beside it (house display rule), including
                      the operator's new requirement that the wall stand as a
                      structure BEFORE it is ever pumped down.
    DOES IT FLOAT?  — the full component ledger against displaced air, across the
                      three chord-allowable worlds (742 verified-class / 1050 mid /
                      1450 sourced-ceiling), plus the CLOSURE DIAMETER per world —
                      the size at which this architecture first floats.

Nothing here is a new physics model. Every capacity law is the repo's own:

  * local wall buckling: K_CLASSICAL * K_LOCAL * ORTHO_PENALTY * E * (t/r) — the
    0.605-corrected coefficient, exactly tools/subdivision_study.py's capacity set;
  * Euler: pi^2 * E * I / L^2 at K = 1 pinned (K < 1 is unlicensed, audit U3);
  * the film: barrier_kg_per_m2, the model's own membrane law (spherical cap at
    bulge h/a = 0.25, T = pR/2, Zylon-class at sf 4 x seam eff 0.5) — the doubly-
    curved square panel is exactly the case that law prices;
  * general instability: Bryant's finite-length stiffened form (membrane term from
    the smeared longerons, ring term from the two walls as flanges), minimised
    over circumferential wave number, series-combined with the ring-plane web
    crimp, knocked down whole at gamma 0.3 with the K_SHELL 0.2 world beside it.

TWO FINDINGS THIS TOOL SURFACED, recorded where they were found:
  1. RING-PLANE WEBS ARE A MISSING MEMBER CLASS. The drawn 2:1 fan lives in
     meridional planes and cannot carry ring-plane shear, so the sandwich
     ovalization stiffness everyone assumed does not exist in the drawn ship.
     Diagonals in the ring plane (one per column per bay) restore it for
     single-digit tonnes. The drawings owe them a member.
  2. AT 0.5-M PITCH WITH FAN-PITCH BRACING THE RING IS STABILITY-GOVERNED, not
     strength-governed — the coupon campaign buys nothing on the barrel until
     the brace pitch tightens. Brace pitch is therefore a design variable here,
     coupled to its own web cost, and the optimiser sweeps it.

SELF-CHECKS RUN FIRST — the tool refuses to print a new number until it reproduces
the ISA anchors, the criterion ladder, P*R = 2,634 kPa*m, the film law's own
article figure, and the v2 SS7 plan-of-record closure (221.7 / 257.7 t, ratios
1.017 / 0.875 / 1.043) on the OLD architecture, so the closure arithmetic is
proven before the new wall replaces the band line inside it. Mutation guards then
prove the guards can fire. A failed self-check means the model moved: stop.

Objects, stated (house rule): SHIP 0 = 2:1 stubby cigar, hemispherical ends,
sea-level survive AND sea-level float, declared SF 1.2 with SF 1.5 beside.
Sources: ~/data/airships-reviews/analysis/26-08-12-ship-scale-analysis-v2.md
(framework), docs/working/26-08-12-seven-levels-handoff.md SS6a (the cascade).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "vc", ROOT / "research" / "analysis" / "vacuum-cell.py")
vc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vc)

# ---------------------------------------------------------------------------------
# Constants — the repo's own wherever one exists, cited; scoping constants flagged.
# ---------------------------------------------------------------------------------
P = vc.P_ATM                            # 101,325 Pa [vacuum-cell.py:47]
SF_DECL = 1.2                           # ship-0 declared SF (operator ruling, v2 SS0)
SF_15 = vc.LATTICE_SF                   # 1.5 — always shown beside [vacuum-cell.py:88]
MAT = vc.MATERIALS["T700_LAM"]          # E 135 GPa, rho 1600 [vacuum-cell.py:91]
E = MAT["E"]
RHO = MAT["rho"]
RHO_TI = vc.MATERIALS["TI64"]["rho"]
K_LOCAL_EFF = vc.K_CLASSICAL * vc.K_LOCAL * vc.ORTHO_PENALTY   # 0.605*0.3*0.5699
# Chord axial-compressive allowables — the coupon axis (v2 SS2). [TO VERIFY]:
# 742 = co-critical verified-class; 1050 = [0/90] working estimate; 1450 = sourced
# Toray 0-deg ceiling (SACMA SRM 1R-94, 60% Vf). The campaign decides the world.
SIGMA_WORLDS = {"s742": 742e6, "s1050": 1050e6, "s1450": 1450e6}
SIGMA_MID = "s1050"

BAY_M = 2.0                             # inner-ring bay pitch (GRID.bayM)
RING_PITCH = 0.5                        # s_r baseline; swept
BAR_PITCH = 0.5                         # s_b baseline; swept
CLAMP_EVERY = 4                         # 1 crossing in 4, brick-staggered (ruled)
CLAMP_KG_AT_130 = 0.11                  # Ti split clamshell class [TO VERIFY]
ETA_MASS = 0.85                         # joints+overhead (v2 SS6) [TO VERIFY]
VOID_SKIN_KGM2 = 0.010
JACKET_KGM2 = 0.050
JUNCTION_ADDER = 0.05                   # dome-barrel junction bays (v2 SS4) [SCOPING]
CLAMP_CAP_N = 2000.0                    # working shear per crossing [TO VERIFY]

OUT_JSON = ROOT / "research" / "analysis" / "ship-scoping.json"

# The live geometry — set by configure(); every solver reads these.
DIA_M = LEN_M = R = CYL_L = V_M3 = AREA_M2 = MERIDIAN_M = 0.0
DEPTH_M = R_IN = BRACE_M = 0.0
N_LONG = 0
K_FAN = 1


def configure(dia_m: float = 52.0, fineness: float = 2.0, n_long: int = 72,
              k_fan: int = 1, depth: float = 3.0) -> None:
    """Set the ship's geometry. brace pitch = the fan's own circumferential
    landing pitch (2*pi*R / (n_long * k_fan)) — derived, never typed, so the
    web bill and the ring bracing cannot disagree about the same fan."""
    global DIA_M, LEN_M, R, CYL_L, V_M3, AREA_M2, MERIDIAN_M
    global DEPTH_M, R_IN, BRACE_M, N_LONG, K_FAN
    DIA_M = dia_m
    LEN_M = fineness * dia_m
    R = dia_m / 2
    CYL_L = LEN_M - dia_m
    V_M3 = math.pi * R * R * CYL_L + 4 / 3 * math.pi * R ** 3
    AREA_M2 = 2 * math.pi * R * CYL_L + 4 * math.pi * R * R
    MERIDIAN_M = math.pi * R + CYL_L
    DEPTH_M = depth
    R_IN = R - depth
    N_LONG = n_long
    K_FAN = k_fan
    BRACE_M = 2 * math.pi * R / (n_long * k_fan)


configure()


# ---------------------------------------------------------------------------------
# Section machinery — one honest solver used by every compression member.
# ---------------------------------------------------------------------------------
def section(od_mm: float, wall_mm: float) -> dict:
    ro = od_mm / 2000
    ri = ro - wall_mm / 1000
    a = math.pi * (ro * ro - ri * ri)
    i = math.pi / 4 * (ro ** 4 - ri ** 4)
    return {"odMm": od_mm, "wallMm": wall_mm, "ro": ro, "rm": (ro + ri) / 2,
            "A": a, "I": i, "Z": i / ro, "kgPerM": a * RHO}


def sigma_local(s: dict) -> float:
    return K_LOCAL_EFF * E * (s["wallMm"] / 1000) / s["rm"]


def sigma_euler(s: dict, braced_l: float) -> float:
    return math.pi ** 2 * E * s["I"] / (s["A"] * braced_l * braced_l)


def size_compression(n_demand: float, braced_l: float, sigma_mat: float,
                     sf: float) -> dict:
    """The lightest tube that carries n_demand [N] in compression at margin >= sf
    against all three INDEPENDENT checks (Euler / local wall / material) — no
    combined interaction is claimed anywhere in this repo (audit U4)."""
    best = None
    for od in [x * 2.0 for x in range(10, 141)]:
        for w in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
                  6.0, 7.0, 8.0, 10.0, 12.0):
            if w * 2 >= od * 0.45:
                continue
            s = section(od, w)
            cap = min(sigma_euler(s, braced_l), sigma_local(s), sigma_mat)
            if cap * s["A"] < n_demand * sf:
                continue
            if best is None or s["A"] < best["A"]:
                best = dict(s)
                best["sigmaCap"] = cap
                best["sigmaDemand"] = n_demand / s["A"]
                best["marginAtSF"] = cap * s["A"] / (n_demand * sf)
                best["governs"] = ("euler" if cap == sigma_euler(s, braced_l)
                                   else "local" if cap == sigma_local(s)
                                   else "material")
    if best is None:
        raise RuntimeError(f"no section carries {n_demand:.0f} N over "
                           f"{braced_l:.2f} m at sigma {sigma_mat / 1e6:.0f}")
    best["demandN"] = n_demand
    best["bracedL"] = braced_l
    return best


def size_bending(m_demand: float, sigma_mat: float, sf: float) -> dict:
    """The lightest stocky tube (R/t <= 25 — inside tested territory; the axial
    local-buckling formula must NOT be reused as a bending limit, FLOAT open q.3)
    whose section modulus carries m_demand [N*m] at margin >= sf."""
    best = None
    for od in [float(x) for x in range(20, 121)]:
        for w in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0):
            if od / 2 / w > 25 or w * 2 >= od * 0.45:
                continue
            s = section(od, w)
            if sigma_mat * s["Z"] < m_demand * sf:
                continue
            if best is None or s["A"] < best["A"]:
                best = dict(s)
                best["marginAtSF"] = sigma_mat * s["Z"] / (m_demand * sf)
    if best is None:
        raise RuntimeError(f"no bending section for {m_demand:.0f} N*m")
    best["demandNm"] = m_demand
    return best


# ---------------------------------------------------------------------------------
# THE WALL — rings + bars + film + clamps, checks attached.
# ---------------------------------------------------------------------------------
def wall_stack(sigma_mat: float, sf: float, s_r: float = RING_PITCH,
               s_b: float = BAR_PITCH) -> dict:
    """The film-on-rings wall at ring pitch s_r, bar pitch s_b.

    Load path, as ruled: the sky presses the film onto the grid; each ring
    carries its tributary as hoop compression N = P*s_r*R — the funicular case,
    exact and pitch-independent in total. Rings brace radially at the fan's own
    landing pitch (BRACE_M — configure() derives it). The bars are CONSERVATIVELY
    sized as if every panel handed its whole load to its bar first (end-span
    w*L^2/8); the drape's true ring-share can only lighten them. [SCOPING]
    """
    n_ring = P * s_r * R
    ring = size_compression(n_ring, BRACE_M, sigma_mat, sf)
    ring_kgm2 = ring["kgPerM"] / s_r

    w_bar = P * s_b
    m_bar = w_bar * s_r * s_r / 8
    bar = size_bending(m_bar, sigma_mat, sf)
    bar_kgm2 = bar["kgPerM"] / s_b

    film_kgm2 = vc.barrier_kg_per_m2(max(s_r, s_b))

    crossings_m2 = 1 / (s_r * s_b)
    clamp_kg = CLAMP_KG_AT_130 * (ring["odMm"] / 130.0)
    clamp_kgm2 = crossings_m2 / CLAMP_EVERY * clamp_kg

    # THE CAPS: on a hemisphere both families carry pR/2 as membrane compression
    # (T = pR/2 each way), crossing every panel pitch — so cap members are braced
    # at the PANEL pitch, reach the material cap, and the cap grid prices at the
    # demand-fixed line rho*SF*P*R/sigma_mat. Its own dome buckling is checked in
    # skeleton() (the sandwich continues under the caps — drawn).
    cap_grid_kgm2 = RHO * sf * P * R / sigma_mat

    barrel_a = 2 * math.pi * R * CYL_L
    caps_a = 4 * math.pi * R * R
    members_t = ((ring_kgm2 + bar_kgm2) * barrel_a + cap_grid_kgm2 * caps_a) / 1000
    film_t = film_kgm2 * AREA_M2 / 1000
    clamp_t = clamp_kgm2 * AREA_M2 / 1000

    return {
        "sigmaMatMPa": sigma_mat / 1e6, "sf": sf,
        "ringPitchM": s_r, "barPitchM": s_b, "braceM": BRACE_M,
        "ring": ring, "bar": bar,
        "ringKgM2": ring_kgm2, "barKgM2": bar_kgm2,
        "filmKgM2": film_kgm2, "clampKgM2": clamp_kgm2,
        "capGridKgM2": cap_grid_kgm2,
        "ringsT": ring_kgm2 * barrel_a / 1000,
        "barsT": bar_kgm2 * barrel_a / 1000,
        "capGridT": cap_grid_kgm2 * caps_a / 1000,
        "membersT": members_t, "filmT": film_t, "clampsT": clamp_t,
        "wallT": members_t + film_t + clamp_t,
        "counts": {
            "rings": round(MERIDIAN_M / s_r) + 1,
            "bars": round(2 * math.pi * R / s_b),
            "panels": round(AREA_M2 / (s_r * s_b)),
            "clamps": round(AREA_M2 / (s_r * s_b) / CLAMP_EVERY),
        },
    }


# ---------------------------------------------------------------------------------
# THE SKELETON — longerons, inner rings, both web families; the global checks.
# ---------------------------------------------------------------------------------
def skeleton(sigma_mat: float, sf: float, wall: dict) -> dict:
    depth = DEPTH_M
    r_in = R_IN
    # Longerons: the caps' whole axial thrust (outer longerons deleted — ruled),
    # P*pi*R^2 over N_LONG columns braced at bay pitch by the inner rings.
    n_axial_total = P * math.pi * R * R
    lng = size_compression(n_axial_total / N_LONG, BAY_M, sigma_mat, sf)
    # Longerons run the BARREL plus a junction overlap only: under the caps the
    # meridional pR/2 is the cap grid's own family (priced in capGridKgM2), and
    # the axial resultant migrates to the longerons across ~sqrt(R*T) of
    # junction (v2 SS4) — running them to the poles would price that family
    # twice. The 5% junction adder carries the transition detail.
    long_len = CYL_L + 2 * min(math.sqrt(R * depth), math.pi / 2 * r_in)
    long_t = lng["kgPerM"] * N_LONG * long_len / 1000

    # The meridional fan (drawn, 2:1): k_fan diagonal pairs per column per bay.
    # Duties: ring radial bracing (the classical 2% rule on the braced ring's
    # hoop force), axial-plane shear for beam bending, erection. [SCOPING]
    web_len = math.hypot(depth, BAY_M / 2)
    n_web_brace = 0.02 * wall["ring"]["demandN"]
    web = size_compression(max(n_web_brace, 2000.0), web_len, sigma_mat, sf)
    webs_per_col = MERIDIAN_M / BAY_M * 2 * K_FAN
    web_t = web["kgPerM"] * web_len * webs_per_col * N_LONG / 1000

    # Inner rings: the web-landing minimum — general instability asks for SHEAR
    # (below), not ring area, so these stay light unless the solver proves otherwise.
    inner0 = size_compression(0.10 * wall["ring"]["demandN"], BAY_M, sigma_mat, sf)
    n_inner = round(MERIDIAN_M / BAY_M) + 1

    # GENERAL INSTABILITY — finite-length stiffened form (see module docstring;
    # the free-tube n=2 floor is reported beside it so the end-dome credit is
    # visible). Ring-plane sandwich stiffness exists ONLY through the theta-webs
    # (finding #1) and is series-combined with their crimp.
    a_o = wall["ring"]["A"] / wall["ringPitchM"]
    a_x = lng["A"] * N_LONG / (2 * math.pi * r_in)
    lam = math.pi * R / CYL_L
    circ_col = 2 * math.pi * R / N_LONG
    theta_len = math.hypot(depth, circ_col / 2)
    n_theta = n_inner * N_LONG

    def crimp_of(a_theta: float) -> float:
        if a_theta <= 0:
            return 0.0
        ang = math.atan2(depth, circ_col / 2)
        g_eff_t = E * (a_theta / (BAY_M * circ_col)) \
            * math.sin(ang) ** 2 * math.cos(ang) * depth
        return 2 * g_eff_t / R

    def general_instability(a_i_smeared: float, a_theta: float,
                            knockdown: float) -> dict:
        abar = a_o * a_i_smeared / (a_o + a_i_smeared)
        i_eff = abar * depth * depth
        q_crimp = crimp_of(a_theta)
        best_n, best_q = 2, None
        for n in range(2, 13):
            q_mem = E * a_x * lam ** 4 / (R * (n * n + lam * lam) ** 2)
            q_ring = (n * n - 1) * E * i_eff / R ** 3
            q_ring = (1 / (1 / q_ring + 1 / q_crimp)
                      if q_ring > 0 and q_crimp > 0 else 0.0)
            q = q_mem + q_ring
            if best_q is None or q < best_q:
                best_q, best_n = q, n
        return {"qCrPa": best_q * knockdown, "critN": best_n,
                "qCrimpPa": q_crimp,
                "qFreeTubeN2Pa": 3 * E * i_eff / R ** 3 * knockdown,
                "iEffM4PerM": i_eff,
                "marginAtSF": best_q * knockdown / (P * sf)}

    def solve(knockdown: float, a_i0: float, a_th0: float):
        """Grow the CHEAPEST capacity first: theta-web area vs inner-ring area,
        each step taking whichever buys more margin per kilogram."""
        a_i, a_th = a_i0, a_th0
        gi = general_instability(a_i / BAY_M, a_th, knockdown)
        guard, d_ai, d_th = 0, 2e-4, 2e-5
        kg_ai = d_ai / BAY_M * RHO * n_inner * 2 * math.pi * r_in * BAY_M
        kg_th = d_th * theta_len * n_theta * RHO
        while gi["marginAtSF"] < 1.0 and guard < 6000:
            gi_r = general_instability((a_i + d_ai) / BAY_M, a_th, knockdown)
            gi_t = general_instability(a_i / BAY_M, a_th + d_th, knockdown)
            gain_r = (gi_r["marginAtSF"] - gi["marginAtSF"]) / kg_ai
            gain_t = (gi_t["marginAtSF"] - gi["marginAtSF"]) / kg_th
            if gain_t >= gain_r:
                a_th, gi = a_th + d_th, gi_t
            else:
                a_i, gi = a_i + d_ai, gi_r
            guard += 1
        return a_i, a_th, gi

    a_th_min = section(30, 1.5)["A"]                 # handling min-gauge floor
    a_i_03, a_th_03, ov = solve(0.3, inner0["A"], a_th_min)
    inner_kgpm = a_i_03 * RHO
    inner_t = inner_kgpm * n_inner * 2 * math.pi * r_in / 1000
    theta_t = a_th_03 * theta_len * n_theta * RHO / 1000
    ov_02 = general_instability(a_i_03 / BAY_M, a_th_03, vc.K_SHELL)
    reserve_kgm2 = 0.0
    if ov_02["marginAtSF"] < 1.0:
        a_i_02, a_th_02, ov_02b = solve(vc.K_SHELL, a_i_03, a_th_03)
        if ov_02b["marginAtSF"] >= 1.0:
            reserve_kgm2 = ((a_i_02 - a_i_03) * RHO * n_inner * 2 * math.pi
                            * r_in + (a_th_02 - a_th_03) * theta_len
                            * n_theta * RHO) / AREA_M2

    # THE CAPS' OWN BUCKLING — orthotropic sphere q_cr = gamma*4*sqrt(B*D)/R^2,
    # B from the cap grid's membrane area, D from the two-wall sandwich (the
    # inner wall continues under the caps — drawn), at gamma 0.3.
    a_cap = wall["capGridKgM2"] / RHO / 2            # per direction, smeared
    b_cap = E * a_cap
    a_i_cap = a_i_03 / BAY_M
    d_cap = E * (a_cap * a_i_cap / (a_cap + a_i_cap)) * depth * depth
    q_cap = 0.3 * 4 * math.sqrt(b_cap * d_cap) / R ** 2
    cap_buckle = {"qCrPa": q_cap, "marginAtSF": q_cap / (P * sf)}

    # Hull beam bending, single inner flange (the check the outer-longeron
    # deletion owes): near-neutral buoyancy leaves gravity bending small, so the
    # named case is a 20 m/s gust at delta-Cp 0.3 over the beam. [SCOPING]
    q_gust = 0.5 * 1.225 * 20 ** 2
    w_gust = 0.3 * q_gust * DIA_M
    m_gust = w_gust * LEN_M ** 2 / 8
    z_hull = lng["A"] * N_LONG * r_in / 2
    sigma_bend = m_gust / z_hull
    # Torsion on one closed wall: Bredt shear flow from a differential-gust
    # couple; one clamp collects the flow over its along-ring spacing. [SCOPING]
    t_demand = w_gust * LEN_M / 2 * LEN_M / 4
    shear_flow = t_demand / (2 * math.pi * R * R)
    clamp_shear_n = shear_flow * wall["barPitchM"] * CLAMP_EVERY

    return {
        "depthM": depth, "rInM": r_in, "braceM": BRACE_M,
        "longeron": lng, "nLong": N_LONG, "longeronsT": long_t,
        "web": web, "websT": web_t,
        "innerRingAM2": a_i_03, "nInnerRings": n_inner, "innerRingsT": inner_t,
        "thetaWebAM2": a_th_03, "thetaWebLenM": theta_len,
        "nThetaWebs": n_theta, "thetaWebsT": theta_t,
        "ovalization": ov, "ovalizationAtK02": ov_02,
        "capBuckle": cap_buckle,
        "reserveKgM2": reserve_kgm2,
        "beamBending": {"mGustNm": m_gust, "sigmaMPa": sigma_bend / 1e6,
                        "marginAtSF": sigma_mat / (sigma_bend * sf)},
        "torsion": {"shearFlowNPerM": shear_flow, "clampShearN": clamp_shear_n,
                    "marginAtSF": CLAMP_CAP_N / (clamp_shear_n * sf)},
    }


# ---------------------------------------------------------------------------------
# THE UNPRESSURISED STATE — "buildable and structured without pressure" (ruled).
# ---------------------------------------------------------------------------------
def unpressurised(wall: dict, skel: dict, total_t: float) -> dict:
    """Three named checks on the wall as a STRUCTURE before the sky is let in:
    (a) one bare ring under self-weight on k jig points (the erection question);
    (b) the assembled, unpumped ship on two cradle lines — gravity ovalization
        carried by the two walls as flanges through the theta-webs;
    (c) the sparse clamp net as the erection shear path in a ground wind.
    All [SCOPING]; the erection SEQUENCE itself is a design input SHIP-2 owes."""
    ring = wall["ring"]
    w_self = ring["kgPerM"] * 9.80665
    out_a = []
    for k in (4, 8, 12, 24):
        span = 2 * math.pi * R / k
        m = w_self * span * span / 12
        sig = m / ring["Z"]
        out_a.append({"jigPoints": k, "spanM": span, "sigmaMPa": sig / 1e6,
                      "ok": sig < 50e6})
    w_dead = total_t * 1000 * 9.80665 / LEN_M / (2 * math.pi * R)
    m_oval = 0.15 * w_dead * R * R                  # ring-on-cradle class moment
    flange_f = m_oval / skel["depthM"]
    a_flange = wall["ring"]["A"] / wall["ringPitchM"]
    sig_cradle = flange_f / a_flange
    q_wind = 0.5 * 1.225 * 15 ** 2
    v_wind = q_wind * DIA_M * LEN_M * 0.5
    flow = v_wind / (2 * math.pi * R)
    clamp_n = flow * wall["barPitchM"] * CLAMP_EVERY
    return {
        "bareRing": out_a,
        "cradle": {"wDeadNPerM2": w_dead, "flangeStressMPa": sig_cradle / 1e6,
                   "ok": sig_cradle < 100e6},
        "erectionWind": {"clampShearN": clamp_n, "capN": CLAMP_CAP_N,
                         "ok": clamp_n < CLAMP_CAP_N / 1.5},
        "verdict": ("stands [SCOPING]" if sig_cradle < 100e6
                    else "DOES NOT STAND"),
    }


# ---------------------------------------------------------------------------------
# THE LEDGER AND THE VERDICTS.
# ---------------------------------------------------------------------------------
def ship_ledger(sigma_key: str, sf: float, s_r: float = RING_PITCH,
                s_b: float = BAR_PITCH) -> dict:
    sig = SIGMA_WORLDS[sigma_key]
    wall = wall_stack(sig, sf, s_r, s_b)
    skel = skeleton(sig, sf, wall)
    eta = 1 / ETA_MASS
    member_t = (wall["membersT"]
                + (skel["longeronsT"] + skel["innerRingsT"] + skel["websT"]
                   + skel["thetaWebsT"]) * (1 + JUNCTION_ADDER))
    joints_t = member_t * (eta - 1)
    skins_t = (VOID_SKIN_KGM2 + JACKET_KGM2) * AREA_M2 / 1000
    reserve_t = skel["reserveKgM2"] * AREA_M2 / 1000
    total_t = (member_t + joints_t + wall["filmT"] + wall["clampsT"]
               + skins_t + reserve_t)
    lift_sl = vc.rho_air(0) * V_M3 / 1000
    lift_25 = vc.rho_air(2500) * V_M3 / 1000
    unp = unpressurised(wall, skel, total_t)
    return {
        "sigmaKey": sigma_key, "sf": sf, "ringPitchM": s_r, "barPitchM": s_b,
        "depthM": DEPTH_M, "nLong": N_LONG, "kFan": K_FAN, "braceM": BRACE_M,
        "diaM": DIA_M, "lenM": LEN_M,
        "wall": wall, "skeleton": skel, "unpressurised": unp,
        "ledgerT": {
            "rings": round(wall["ringsT"], 1),
            "capGrid": round(wall["capGridT"], 1),
            "bars": round(wall["barsT"], 1),
            "film": round(wall["filmT"], 1),
            "clamps": round(wall["clampsT"], 1),
            "longerons": round(skel["longeronsT"] * (1 + JUNCTION_ADDER), 1),
            "innerRings": round(skel["innerRingsT"] * (1 + JUNCTION_ADDER), 1),
            "fanWebs": round(skel["websT"] * (1 + JUNCTION_ADDER), 1),
            "thetaWebs": round(skel["thetaWebsT"] * (1 + JUNCTION_ADDER), 1),
            "tiJoints": round(joints_t, 1),
            "skins": round(skins_t, 1),
            "stabilityReserve": round(reserve_t, 1),
        },
        "totalT": total_t,
        "liftSLT": lift_sl, "lift2500T": lift_25,
        "ratioSL": lift_sl / total_t, "residualSLT": lift_sl - total_t,
        "ratio2500": lift_25 / total_t, "residual2500T": lift_25 - total_t,
        "arealKgM2": total_t * 1000 / AREA_M2,
        "floats": total_t < lift_sl,
        "unmodelled": ["pumps/valves/avionics/ground gear (payload axis, named "
                       "not weighed — operator declaration)",
                       "combined axial+bending interaction (audit U4)",
                       "erection sequence loads beyond the three scoping checks",
                       "aero loads beyond the named gust cases"],
    }


# ---------------------------------------------------------------------------------
# SELF-CHECKS — published figures reproduced before anything new is printed.
# ---------------------------------------------------------------------------------
def v2_closure_reproduction() -> dict:
    """The OLD architecture's closure (v2 SS7 plan-of-record row), reproduced
    from its own stated model, so the arithmetic frame is proven before the new
    wall replaces the band line inside it."""
    barrel_a = 2 * math.pi * R * CYL_L
    caps_a = 4 * math.pi * R * R

    def row(sf: float, band_kgm2: float, sigma: float) -> dict:
        mu_barrel = 1.5 * sf * P * R * RHO / (sigma * ETA_MASS)
        chord_t = (mu_barrel * barrel_a + mu_barrel * 2 / 3 * caps_a) / 1000
        band_t = band_kgm2 * AREA_M2 / 1000
        total = chord_t + band_t + (0.5 + 0.4 + 0.05) * AREA_M2 / 1000
        lift = vc.rho_air(0) * V_M3 / 1000
        return {"chordT": chord_t, "bandT": band_t, "totalT": total,
                "liftT": lift, "ratio": lift / total}
    return {"sf12": row(1.2, 5.01, 1050e6), "sf15": row(1.5, 5.36, 1050e6),
            "sf15s1450": row(1.5, 5.36, 1450e6)}


def self_check() -> list:
    configure()                                       # the plan-of-record geometry
    cks = []

    def add(name, got, want, tol):
        cks.append((name, got, want, tol, abs(got - want) <= tol))

    add("rhoAir(0)", vc.rho_air(0), 1.22501, 2e-5)
    add("rhoAir(2500)", vc.rho_air(2500), 0.9568654, 2e-6)
    add("V m3", V_M3, 184100, 120)
    add("hull m2", AREA_M2, 16990, 12)
    add("lift SL t", vc.rho_air(0) * V_M3 / 1000, 225.5, 0.3)
    add("P*R kPa*m", P * R / 1000, 2634, 1)
    fill = P / vc.rho_air(0) / 1000
    add("ladder fill SL kJ/kg", fill, 82.71, 0.05)
    add("ladder shell SL", 1.5 * fill, 124.07, 0.07)
    add("ladder shell SF1.5 SL", SF_15 * 1.5 * fill, 186.11, 0.11)
    add("cell film kg", vc.film_kg(2 * vc.DEMO_PITCH_PINNED_M), 0.028, 0.0005)
    add("step law anchor kPa", 2.84 * 101.325 / 1.5, 191.8, 0.15)
    rep = v2_closure_reproduction()
    add("v2 total @SF1.2 t", rep["sf12"]["totalT"], 221.7, 2.5)
    add("v2 ratio @SF1.2", rep["sf12"]["ratio"], 1.017, 0.012)
    add("v2 total @SF1.5 t", rep["sf15"]["totalT"], 257.7, 3.0)
    add("v2 ratio @SF1.5", rep["sf15"]["ratio"], 0.875, 0.011)
    add("v2 ratio @SF1.5 s1450", rep["sf15s1450"]["ratio"], 1.043, 0.013)
    # Mutation guards — each must FIRE.
    no_band = rep["sf12"]["totalT"] - rep["sf12"]["bandT"]
    cks.append(("MUT: dropping the band moves the total", no_band, 221.7, 2.5,
                abs(no_band - 221.7) > 2.5))
    twice = 1.2 * rep["sf12"]["totalT"]
    cks.append(("MUT: SF applied twice breaks the ratio",
                rep["sf12"]["liftT"] / twice, 1.017, 0.012,
                abs(rep["sf12"]["liftT"] / twice - 1.017) > 0.012))
    w = wall_stack(1050e6, 1.2)
    cks.append(("MUT: film line is not zero", w["filmT"], 0, 0.1,
                w["filmT"] > 0.1))
    cks.append(("MUT: eta<=1 enforced", ETA_MASS, 0.85, 0.2, ETA_MASS <= 1.0))
    return cks


# ---------------------------------------------------------------------------------
# The design-space sweep, the closure probe, and the sensitivity table.
# ---------------------------------------------------------------------------------
def config_sweep(sigma_key: str, sf: float) -> dict:
    """#74's optimisation, honestly coupled: ring/bar pitch, longeron count and
    fan density (which SET the ring brace pitch and the web bill together), and
    sandwich depth. One geometry must serve every world — the pick is made on
    the mid basis at the declared SF and then evaluated everywhere."""
    rows = []
    best = None
    for n_long, k_fan in ((72, 1), (72, 2), (96, 1), (96, 2), (144, 1)):
        for depth in (3.0, 4.0):
            for s_r in (0.4, 0.5, 0.6, 0.8):
                for s_b in (0.5, 0.7, 1.0):
                    configure(n_long=n_long, k_fan=k_fan, depth=depth)
                    try:
                        led = ship_ledger(sigma_key, sf, s_r, s_b)
                    except RuntimeError:
                        continue
                    row = {"nLong": n_long, "kFan": k_fan, "depth": depth,
                           "sR": s_r, "sB": s_b,
                           "totalT": round(led["totalT"], 1),
                           "ratioSL": round(led["ratioSL"], 3)}
                    rows.append(row)
                    if best is None or led["totalT"] < best["totalT"]:
                        best = row
    configure()
    return {"rows": rows, "best": best}


def at_diameter(dia: float, cfg: dict, sigma_key: str, sf: float) -> dict:
    """The chosen configuration scaled GEOMETRICALLY to another hull: depth and
    longeron count grow with R (so the sandwich stays similar and the ring brace
    pitch stays what the config chose), pitches stay absolute (panel physics is
    absolute). Fixed-depth scaling makes the stability tax explode with R and is
    exactly the trap the first cut of this probe fell into."""
    scale = dia / 52.0
    configure(dia_m=dia, n_long=max(24, round(cfg["nLong"] * scale)),
              k_fan=cfg["kFan"], depth=cfg["depth"] * scale)
    return ship_ledger(sigma_key, sf, cfg["sR"], cfg["sB"])


def float_window(sigma_key: str, sf: float, cfg: dict) -> dict:
    """Where this architecture floats, by diameter. The OLD closure map assumed
    ratio rises with size (the band's fixed per-area mass diluting); with the
    band gone almost every line scales with lift and the curve is gently
    FALLING — so the answer is a window, not a minimum size. Reported as the
    ratio at a spread of hulls plus the window edges where one exists."""
    dias = [40.0, 44.0, 48.0, 52.0, 56.0, 60.0, 68.0, 80.0]
    curve = []
    for d in dias:
        try:
            led = at_diameter(d, cfg, sigma_key, sf)
            curve.append({"diaM": d, "ratioSL": round(led["ratioSL"], 3),
                          "totalT": round(led["totalT"], 1),
                          "residualT": round(led["residualSLT"], 1)})
        except RuntimeError:
            curve.append({"diaM": d, "ratioSL": None, "totalT": None,
                          "residualT": None})
    configure()
    floats = [c["diaM"] for c in curve if c["ratioSL"] and c["ratioSL"] >= 1.0]
    return {"curve": curve,
            "window": [min(floats), max(floats)] if floats else None}


def sensitivity(cfg: dict, sigma_key: str, sf: float) -> list:
    global ETA_MASS
    out = []

    def run(label, dia=52.0, **kw):
        c = {**cfg, **kw}
        d = at_diameter(dia, c, sigma_key, sf)
        out.append({"case": label, "totalT": round(d["totalT"], 1),
                    "ratioSL": round(d["ratioSL"], 3)})
        configure()
    run("baseline (chosen config)")
    run("depth +1 m", depth=cfg["depth"] + 1.0)
    run("rings +0.1 m", sR=cfg["sR"] + 0.1)
    keep = ETA_MASS
    ETA_MASS = 0.80
    run("eta 0.80")
    ETA_MASS = 0.90
    run("eta 0.90")
    ETA_MASS = keep
    run("dia 56 m", dia=56.0)
    run("dia 60 m", dia=60.0)
    return out


# ---------------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", nargs="?", const=str(OUT_JSON), default=None)
    args = ap.parse_args()

    cks = self_check()
    width = max(len(c[0]) for c in cks)
    print("SELF-CHECKS — published figures first, mutation guards after:\n")
    ok = True
    for name, got, want, tol, passed in cks:
        print(f"  {'PASS' if passed else 'FAIL'}  {name:<{width}}  "
              f"got {got:.6g}  want {want:.6g} +/- {tol:.2g}")
        ok = ok and passed
    if not ok:
        sys.exit("\nship_scoping: SELF-CHECK FAILED — the model moved; every "
                 "figure below would be stale. Stop; do not widen.")

    # The configuration pick: the sweep finds the optimum, and the PLAN OF
    # RECORD keeps the operator's ruled 0.5-m square panels — the sweep's own
    # result is that the ruling costs ~2%, which is the right way for a ruling
    # to survive its optimisation check. One geometry serves every world.
    print("\nDESIGN-SPACE SWEEP (mid basis, declared SF 1.2) ...")
    sweep = config_sweep(SIGMA_MID, SF_DECL)
    b = sweep["best"]
    print(f"  sweep optimum: rings {b['sR']} x bars {b['sB']} m, "
          f"{b['nLong']} longerons x fan {b['kFan']}, depth {b['depth']:.0f} m "
          f"-> {b['totalT']} t")
    cfg = {"sR": 0.5, "sB": 0.5, "nLong": 72, "kFan": 2, "depth": 3.0}
    print(f"  PLAN OF RECORD keeps the ruled 0.5 m squares: rings {cfg['sR']} x "
          f"bars {cfg['sB']} m, {cfg['nLong']} longerons x fan {cfg['kFan']} "
          f"(brace {2 * math.pi * 26 / (cfg['nLong'] * cfg['kFan']):.2f} m), "
          f"depth {cfg['depth']:.0f} m — within ~2% of the optimum")

    configure(n_long=cfg["nLong"], k_fan=cfg["kFan"], depth=cfg["depth"])
    print(f"\nSHIP 0 — {DIA_M:.0f} m x {LEN_M:.0f} m, V = {V_M3:,.0f} m3, "
          f"hull {AREA_M2:,.0f} m2, sea level.\n")

    results = {}
    for sf, sf_name in ((SF_DECL, "declared SF 1.2"), (SF_15, "SF 1.5")):
        for key in ("s742", "s1050", "s1450"):
            configure(n_long=cfg["nLong"], k_fan=cfg["kFan"], depth=cfg["depth"])
            r = ship_ledger(key, sf, cfg["sR"], cfg["sB"])
            results[f"{key}_sf{sf}"] = r
            tag = "FLOATS" if r["floats"] else "sinks"
            print(f"  {sf_name:>16} @ {key[1:]:>4} MPa: total {r['totalT']:6.1f} t"
                  f" vs {r['liftSLT']:.1f} t -> ratio {r['ratioSL']:.3f} "
                  f"({r['residualSLT']:+.1f} t)  {tag}")

    print("\nTHE FLOAT WINDOW (chosen config, geometric scaling; the old "
          "closure map inverts — the band's diluting mass is gone):")
    closures = {}
    for sf in (SF_DECL, SF_15):
        for key in ("s742", "s1050", "s1450"):
            fw = float_window(key, sf, cfg)
            closures[f"{key}_sf{sf}"] = fw
            if fw["window"]:
                print(f"    SF {sf} @ {key[1:]:>4} MPa: floats "
                      f"{fw['window'][0]:.0f}-{fw['window'][1]:.0f} m "
                      f"(52 m: {next(c['ratioSL'] for c in fw['curve'] if c['diaM'] == 52.0)})")
            else:
                print(f"    SF {sf} @ {key[1:]:>4} MPa: floats nowhere "
                      f"40-80 m (52 m: "
                      f"{next(c['ratioSL'] for c in fw['curve'] if c['diaM'] == 52.0)})")

    configure(n_long=cfg["nLong"], k_fan=cfg["kFan"], depth=cfg["depth"])
    mid = results[f"{SIGMA_MID}_sf{SF_DECL}"]
    print(f"\nLEDGER (mid basis, declared SF {SF_DECL}), tonnes:")
    for k, v in mid["ledgerT"].items():
        print(f"    {k:<18} {v:>7.1f}")
    print(f"    {'TOTAL':<18} {mid['totalT']:>7.1f}   "
          f"lift {mid['liftSLT']:.1f}  ratio {mid['ratioSL']:.3f}")

    w, s = mid["wall"], mid["skeleton"]
    print(f"\nTHE CHECKS (mid basis, declared SF; the SF 1.5 columns are above):")
    print(f"    ring   {w['ring']['odMm']:.0f} x {w['ring']['wallMm']:.1f} mm  "
          f"margin {w['ring']['marginAtSF']:.2f} ({w['ring']['governs']}; "
          f"runs at {w['ring']['sigmaDemand'] / 1e6:.0f} MPa)")
    print(f"    bar    {w['bar']['odMm']:.0f} x {w['bar']['wallMm']:.1f} mm  "
          f"margin {w['bar']['marginAtSF']:.2f} (bending, all-on-bars worst case)")
    print(f"    film   {w['filmKgM2'] * 1000:.0f} g/m2 at the "
          f"{max(w['ringPitchM'], w['barPitchM']):.2f} m panel (house law)")
    print(f"    longeron {s['longeron']['odMm']:.0f} x "
          f"{s['longeron']['wallMm']:.1f} mm  margin "
          f"{s['longeron']['marginAtSF']:.2f} ({s['longeron']['governs']})")
    print(f"    general instability margin {s['ovalization']['marginAtSF']:.2f} "
          f"at gamma 0.3 (crit n={s['ovalization']['critN']}; free-tube n=2 "
          f"floor {s['ovalization']['qFreeTubeN2Pa'] / (P * mid['sf']):.2f}); "
          f"{s['ovalizationAtK02']['marginAtSF']:.2f} at K_SHELL 0.2 -> "
          f"reserve {s['reserveKgM2']:.2f} kg/m2")
    print(f"    cap (sandwich dome) buckling margin "
          f"{s['capBuckle']['marginAtSF']:.1f} at gamma 0.3")
    print(f"    beam bending margin {s['beamBending']['marginAtSF']:.0f}; "
          f"torsion clamp margin {s['torsion']['marginAtSF']:.1f} [SCOPING]")
    unp = mid["unpressurised"]
    print(f"    unpressurised: cradle flange "
          f"{unp['cradle']['flangeStressMPa']:.1f} MPa -> {unp['verdict']}; "
          f"bare ring wants >="
          f"{next(a['jigPoints'] for a in unp['bareRing'] if a['ok'])} jig points")

    sens = sensitivity(cfg, SIGMA_MID, SF_DECL)
    print("\nSENSITIVITY (mid basis, declared SF):")
    for row in sens:
        print(f"    {row['case']:<24} total {row['totalT']:6.1f} t  "
              f"ratio {row['ratioSL']:.3f}")

    if args.json:
        payload = {
            "selfChecks": [{"name": n, "got": g, "want": wt, "pass": p}
                           for n, g, wt, _t, p in cks],
            "chosenConfig": cfg,
            "geometry": {"diaM": 52.0, "lenM": 104.0, "vM3": V_M3,
                         "areaM2": AREA_M2, "meridianM": MERIDIAN_M,
                         "bayM": BAY_M},
            "results": {k: {kk: vv for kk, vv in v.items()
                            if kk not in ("wall", "skeleton", "unpressurised")}
                        for k, v in results.items()},
            "midBasis": results[f"{SIGMA_MID}_sf{SF_DECL}"],
            "closureDiametersM": closures,
            "sweep": sweep,
            "sensitivity": sens,
        }
        pathlib.Path(args.json).write_text(json.dumps(payload, indent=1,
                                                      default=float))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
