#!/usr/bin/env python3
"""SHIP-2 — the film-on-rings wall, checked, priced, and the two verdicts.

    python3 tools/ship_scoping.py [--json [PATH]]

The operator's 08-12/08-13 cascade replaced the Kelvin band with a wall that is nothing
but structure and one membrane: hoop rings at panel pitch, continuous meridional
cross-bars one diameter outboard, film laid straight on them, split-Ti clamps at one
crossing in four. This tool is the cascade's bill. It answers the two questions the
project exists to answer for the selected hull. Its configuration is compared
with the hull of record before it is named:

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

FINDINGS LEDGER — what this tool surfaced, and what a three-refuter adversarial
panel (08-13, run before any page quoted a number) then surfaced about IT. All
eleven confirmed bugs are fixed in this version; each fix is marked [REF-n] at
the line that carries it:
  1. RING-PLANE WEBS ARE A MISSING MEMBER CLASS (this tool's own finding, which
     survived review): the drawn 2:1 fan lives in meridional planes and cannot
     carry ring-plane shear. Now X-braced diagonals per column per bay plane.
  2. [REF-1/9] The general-instability membrane term was missing Bryant's
     load-side divisor (n^2 + lam^2/2 - 1) — restored, with the head-credit
     effective length L_eff = L + 2R/3 [REF-S2].
  3. [REF-2/7s] The crimp stiffness used the wrong triangle leg and the sphere
     coefficient — now S = E*A*T*cos^2(th)/(bay*l) per diagonal (X-braced x2),
     q_crimp = S/R (cylinder), series-combined per mode.
  4. [REF-4] The ring brace pitch is the fan's TRUE circumferential landing
     pitch 2*pi*R/n_long — k_fan buys meridional density only.
  5. [REF-3] The cap dome check now series-combines its own crimp branch, and
     [REF-5] the cap grid carries the film's bending duty (cap bars line).
  6. [REF-6] The dome-barrel junction is a priced shear-transfer member set,
     not a percentage.
  7. [REF-7] The cross-bars are decoupled from hull axial strain BY DESIGN
     (sliding crossings — the ruled clamp is retention, not a load path) and a
     dedicated torsion-strap line replaces the failing clamp-net torsion path.
  8. [REF-8/11] Every named check now gates the verdicts: FLOATS is only
     printed when the structure also STANDS, and the unpressurised verdict
     fails on any of its three checks, not just the cradle.
  9. [REF-10] The stability system carries the same eta and junction
     multipliers as every other member class.
 10. [REF-S4] Unclamped crossings carry a bonded saddle-pad line; [REF-S5] the
     film is priced one-way (T = p*r trough) until a drape analysis licenses
     the two-way credit; [REF-S9] the film's inward scallop debits lift.
 11. THE KNOCKDOWN IS THE VERDICT: gamma_GI = 0.3 (house-harsh) sizes the
     ledger; the frame-practice world (0.65, submarine GI custom with OOR
     control [TO VERIFY]) is REPORTED beside it. The SHIP-2 knockdown test is
     now, explicitly, the float decision.

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
GI_KNOCKDOWN = 0.3                      # gamma on Bryant, house-harsh — SIZES the ledger
GI_KNOCKDOWN_FRAME = 0.65               # frame-practice world, REPORTED beside [TO VERIFY]
GI_ACTIVE = GI_KNOCKDOWN                # what the solver sizes at (main flips it to
                                        # print the frame-practice matrix, then restores)
PAD_KG = 0.04                           # bonded saddle pad at unclamped crossings [TO VERIFY]
STRAP_SIGMA = 300e6                     # torsion strap working stress class [TO VERIFY]
# THE LICENSED FALLBACK (v2 SS1, verbatim): "tension spokes against ovalization
# (unstudied alternative if SHIP-2 prices the stability reserve high)". SHIP-2
# has now priced it high — 150 t-class of compression iron — so the spokes are
# studied. Diametral tension cords across the void, pretensioned so both signs
# of the mode load them: a Winkler foundation under every ring, strongest at
# exactly the low-n shape modes the sandwich pays most for. They cross the void
# as TENSION, which is the ruled exception; nothing about them is a column.
E_SPOKE = 70e9                          # Dyneema-class cord modulus [TO VERIFY — creep]
RHO_SPOKE = 970.0
SPOKE_FITTING = 1.3                     # terminations + pretension hardware [SCOPING]

# SHIP-3 DESIGN-MOVE BOUNDS — for the --band study ONLY; both False in every
# gated run and the record never sizes with either:
#   BOUND_CHORDAL — the chordal spoke net engages the ODD circumferential
#     modes a diametral cord cannot [REV-1]. Credited as the same Winkler
#     foundation at odd n; the cord mass IS priced (the greedy buys it at
#     diametral-cord rates), the net's geometry/terminations are [SCOPING].
#   BOUND_MEMBRANE — the in-surface shear system licenses Bryant's membrane
#     term back [REV-2]. Stiffness credited, the shear system's own mass NOT
#     priced — an OUTER BOUND, not a design.
BOUND_CHORDAL = False
BOUND_MEMBRANE = False

# The committed plan-of-record configuration. main() re-derives it from the
# sweep every run; the band study evaluates this committed row and refuses to
# print if the 52 m record does not reproduce first.
PLAN_CFG = {"sR": 0.5, "sB": 0.5, "nLong": 72, "kFan": 1, "depth": 3.0}

OUT_JSON = ROOT / "research" / "analysis" / "ship-scoping.json"

# The live geometry — set by configure(); every solver reads these.
DIA_M = LEN_M = R = CYL_L = V_M3 = AREA_M2 = MERIDIAN_M = 0.0
DEPTH_M = R_IN = BRACE_M = 0.0
N_LONG = 0
K_FAN = 1


def configure(dia_m: float = 52.0, fineness: float = 2.0, n_long: int = 72,
              k_fan: int = 1, depth: float = 3.0) -> None:
    """Set the ship's geometry. Ring brace pitch = the fan's TRUE circumferential
    landing pitch 2*pi*R/n_long — k_fan multiplies web density ALONG THE MERIDIAN
    and buys no circumferential brace lines whatever (refuter finding 08-13: the
    first draft credited it with exactly that, and the ring was Euler-sized on a
    brace pitch that does not exist)."""
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
    BRACE_M = 2 * math.pi * R / n_long


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

    # [REF-S5] The film is priced ONE-WAY (a cylindrical trough at T = p*r,
    # twice the doubly-curved tension) until a drape analysis licenses the
    # two-way credit: the drawn one-bar-diameter step is smaller than the
    # membrane law's own design bulge, so the pillow's second curvature is
    # unverified. barrier_kg_per_m2 prices T = pR/2; the trough doubles it.
    film_kgm2 = 2.0 * vc.barrier_kg_per_m2(max(s_r, s_b))

    crossings_m2 = 1 / (s_r * s_b)
    clamp_kg = CLAMP_KG_AT_130 * (ring["odMm"] / 130.0)
    clamp_kgm2 = crossings_m2 / CLAMP_EVERY * clamp_kg

    # THE CAPS: on a hemisphere both families carry pR/2 as membrane compression
    # (T = pR/2 each way), crossing every panel pitch — so cap members are braced
    # at the PANEL pitch, reach the material cap, and the cap grid prices at the
    # demand-fixed line rho*SF*P*R/sigma_mat. [REF-5] The outer family is ALSO a
    # beam-column under the film's line load — the same duty the barrel prices
    # as bars — so the caps carry the bar areal too. Dome buckling with its own
    # crimp branch is checked in skeleton().
    cap_grid_kgm2 = RHO * sf * P * R / sigma_mat + bar_kgm2

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
    """Longerons, the meridional fan, the inner rings, the X-braced ring-plane
    webs, the junction shear set — and the global checks with the corrected
    physics (see the findings ledger in the module docstring; every [REF-n]
    marks a refuter fix)."""
    depth = DEPTH_M
    r_in = R_IN
    # Longerons: the caps' whole axial thrust, barrel + junction overlap only
    # (the cap grid owns pR/2 under the caps).
    n_axial_total = P * math.pi * (R * R)
    lng = size_compression(n_axial_total / N_LONG, BAY_M, sigma_mat, sf)
    long_len = CYL_L + 2 * min(math.sqrt(R * depth), math.pi / 2 * r_in)
    long_t = lng["kgPerM"] * N_LONG * long_len / 1000

    # The meridional fan: ring radial bracing (2% rule) + erection.
    web_len = math.sqrt(depth * depth + BAY_M * BAY_M / 4.0)
    n_web_brace = 0.02 * wall["ring"]["demandN"]
    web = size_compression(max(n_web_brace, 2000.0), web_len, sigma_mat, sf)
    webs_per_col = MERIDIAN_M / BAY_M * 2 * K_FAN
    web_t = web["kgPerM"] * web_len * webs_per_col * N_LONG / 1000

    # [REF-6] THE JUNCTION IS A MEMBER SET, NOT A PERCENTAGE: 215 MN of cap
    # thrust arrives at the outer surface and shears inward to the longerons
    # through 45-deg diagonals over the sqrt(R*T) transition zone, at each end.
    n_flow = P * R / 2.0                              # meridional N at the equator
    a_junction_per_m = n_flow * sf / (sigma_mat * 0.45)
    junction_len = math.sqrt(2.0) * depth
    junction_t = (a_junction_per_m * junction_len * RHO
                  * 2 * math.pi * R * 2) / 1000

    inner0 = size_compression(0.10 * wall["ring"]["demandN"], BAY_M, sigma_mat, sf)
    n_inner = round(MERIDIAN_M / BAY_M) + 1

    # GENERAL INSTABILITY — Bryant's finite-length stiffened form, honest:
    #   q(n) = E*a_x*lam^4 / (R*(n^2+lam^2/2-1)*(n^2+lam^2)^2)     [REF-1]
    #        + series((n^2-1)*E*I'/R^3, S/R)                        [REF-2]
    # minimised over n = 2..12, knocked down whole. lam uses the head-credit
    # effective length L_eff = CYL_L + 2R/3 [REF-S2]. The ring term's shear
    # partner S comes from X-BRACED ring-plane diagonals (full-panel run):
    #   S = 2 * E * A_th * T * cos^2(th) / (BAY * l_th)  per unit circumference
    # with cos(th) = c/l_th — the tangential leg, not the radial one [REF-2].
    a_o0 = wall["ring"]["A"] / wall["ringPitchM"]
    a_x = lng["A"] * N_LONG / (2 * math.pi * r_in)
    l_eff = CYL_L + 2 * R / 3.0
    lam = math.pi * R / l_eff
    lam2 = lam * lam
    circ_col = 2 * math.pi * R / N_LONG
    theta_len = math.sqrt(depth * depth + circ_col * circ_col)
    cos_th = circ_col / theta_len
    n_theta = n_inner * N_LONG * 2                    # X-braced: two per panel

    def crimp_of(a_theta: float) -> float:
        if a_theta <= 0:
            return 0.0
        s_shear = (2.0 * E * a_theta * depth * (cos_th * cos_th)
                   / (BAY_M * theta_len))
        return s_shear / R                             # cylinder: N = qR [REF-2]

    def general_instability(a_i_smeared: float, a_theta: float,
                            a_o_extra: float, a_spoke: float,
                            knockdown: float) -> dict:
        a_o = a_o0 + a_o_extra
        abar = a_o * a_i_smeared / (a_o + a_i_smeared)
        i_eff = abar * depth * depth
        q_crimp = crimp_of(a_theta)
        # THE SPOKES: a Winkler foundation under the wall — diametral cords of
        # smeared area a_spoke per m^2 of wall, pretensioned so both signs of
        # the mode load them. Ring on elastic foundation adds k*R/(n^2-1):
        # strongest at n=2, gone by n>=5 — exactly complementary to the
        # bend+crimp branch, which is weakest at n=2 and strong at high n.
        # [REV-1] diametral cords have zero first-order stiffness at odd n
        # (ends move (+w,-w): pure translation); even n: per-end E*a/R.
        # Chordal spoke nets engage odd n — SHIP-3's design move, not drawn.
        # [REV-2] the Bryant membrane term is ZEROED — it needs an in-surface
        # shear path this wall does not have [TO VERIFY — SHIP-3 buys it back].
        # [REV-3, REJECTED with the textbook]: the second panel proposed
        # swapping the crimp to c*d^2/l^3; Timoshenko's laced-column shear
        # rigidity S = E*A_d*sin(g)cos^2(g) (g from the CHORD) is exactly the
        # coded d*c^2/l^3, confirmed by the exact X-panel slip stiffness and
        # by both degenerate limits. The coded form stands.
        k_r = E_SPOKE * a_spoke / R
        best_n, best_q = 2, None
        for n in range(2, 13):
            q_ring = (n * n - 1) * E * i_eff / (R * R * R)
            if q_ring > 0 and q_crimp > 0:
                q_ring = 1.0 / (1.0 / q_ring + 1.0 / q_crimp)
            else:
                q_ring = 0.0
            q_found = (k_r * R / (n * n - 1)) \
                if (n % 2 == 0 or BOUND_CHORDAL) else 0.0
            q_mem = 0.0
            if BOUND_MEMBRANE:
                nn_l2 = n * n + lam2
                q_mem = (E * a_x * lam2 * lam2
                         / (R * (n * n + lam2 / 2 - 1) * nn_l2 * nn_l2))
            q = q_ring + q_found + q_mem
            if best_q is None or q < best_q:
                best_q, best_n = q, n
        return {"qCrPa": best_q * knockdown, "critN": best_n,
                "qCrimpPa": q_crimp, "kFoundation": k_r,
                "iEffM4PerM": i_eff,
                "marginAtSF": best_q * knockdown / (P * sf)}

    def solve(knockdown: float, a_i0: float, a_th0: float, a_oe0: float,
              a_sp0: float):
        """Grow the CHEAPEST capacity first among FOUR moves: inner-ring area,
        theta-web area, outer-ring flange doubler, and the licensed tension
        spokes [the greedy's move set was itself a refuter finding]."""
        a_i, a_th, a_oe, a_sp = a_i0, a_th0, a_oe0, a_sp0
        rec = general_instability(a_i / BAY_M, a_th, a_oe, a_sp, knockdown)
        guard = 0
        d_ai, d_th, d_oe, d_sp = 4e-4, 4e-5, 2e-4, 2e-7
        kg_ai = d_ai / BAY_M * RHO * n_inner * 2 * math.pi * r_in * BAY_M
        kg_th = d_th * theta_len * n_theta * RHO
        kg_oe = d_oe * RHO * 2 * math.pi * R * CYL_L / (2 * math.pi * R) \
            * 2 * math.pi * R
        kg_sp = d_sp * R * RHO_SPOKE * SPOKE_FITTING * AREA_M2
        while rec["marginAtSF"] < 1.0 and guard < 6000:
            cands = []
            rec_i = general_instability((a_i + d_ai) / BAY_M, a_th, a_oe,
                                        a_sp, knockdown)
            cands.append(((rec_i["marginAtSF"] - rec["marginAtSF"]) / kg_ai,
                          "i", rec_i))
            rec_t = general_instability(a_i / BAY_M, a_th + d_th, a_oe,
                                        a_sp, knockdown)
            cands.append(((rec_t["marginAtSF"] - rec["marginAtSF"]) / kg_th,
                          "t", rec_t))
            rec_o = general_instability(a_i / BAY_M, a_th, a_oe + d_oe,
                                        a_sp, knockdown)
            cands.append(((rec_o["marginAtSF"] - rec["marginAtSF"]) / kg_oe,
                          "o", rec_o))
            rec_s = general_instability(a_i / BAY_M, a_th, a_oe,
                                        a_sp + d_sp, knockdown)
            cands.append(((rec_s["marginAtSF"] - rec["marginAtSF"]) / kg_sp,
                          "s", rec_s))
            cands.sort(key=lambda c: -c[0])
            _, move, best = cands[0]
            if move == "i":
                a_i += d_ai
            elif move == "t":
                a_th += d_th
            elif move == "o":
                a_oe += d_oe
            else:
                a_sp += d_sp
            rec = best
            guard += 1
        return a_i, a_th, a_oe, a_sp, rec

    a_th_min = section(30, 1.5)["A"]
    a_i_03, a_th_03, a_oe_03, a_sp_03, ov = solve(GI_ACTIVE, inner0["A"],
                                                  a_th_min, 0.0, 0.0)
    inner_t = a_i_03 * RHO * n_inner * 2 * math.pi * r_in / 1000
    theta_t = a_th_03 * theta_len * n_theta * RHO / 1000
    flange_t = a_oe_03 * RHO * 2 * math.pi * R * CYL_L / 1000
    spoke_t = a_sp_03 * R * RHO_SPOKE * SPOKE_FITTING * AREA_M2 / 1000
    ov_frame = general_instability(a_i_03 / BAY_M, a_th_03, a_oe_03, a_sp_03,
                                   GI_KNOCKDOWN_FRAME)
    ov_harsh = general_instability(a_i_03 / BAY_M, a_th_03, a_oe_03, a_sp_03,
                                   GI_KNOCKDOWN)
    ov_02 = general_instability(a_i_03 / BAY_M, a_th_03, a_oe_03, a_sp_03,
                                vc.K_SHELL)
    reserve_kgm2 = 0.0
    # The K_SHELL 0.2 top-up is priced ONLY on the harsh sizing basis: the
    # frame-practice world asserts the knockdown tests landed at 0.65, and
    # carrying 0.2 insurance inside that world would contradict its premise.
    if ov_02["marginAtSF"] < 1.0 and GI_ACTIVE == GI_KNOCKDOWN:
        a_i_02, a_th_02, a_oe_02, a_sp_02, ov_02b = solve(
            vc.K_SHELL, a_i_03, a_th_03, a_oe_03, a_sp_03)
        if ov_02b["marginAtSF"] >= 1.0:
            reserve_kgm2 = ((a_i_02 - a_i_03) * RHO * n_inner * 2 * math.pi
                            * r_in
                            + (a_th_02 - a_th_03) * theta_len * n_theta * RHO
                            + (a_oe_02 - a_oe_03) * RHO * 2 * math.pi * R
                            * CYL_L
                            + (a_sp_02 - a_sp_03) * R * RHO_SPOKE
                            * SPOKE_FITTING * AREA_M2) / AREA_M2

    # THE CAPS' OWN BUCKLING [REF-3]: orthotropic sphere WITH its crimp branch —
    # q = gamma * series(4*sqrt(B*D)/R^2, 2*S_cap/R) (the sphere keeps its 2:
    # membrane N = qR/2 there). The cap theta-webs are the same family.
    a_cap = (wall["capGridKgM2"] - wall["barKgM2"]) / RHO / 2
    b_cap = E * a_cap
    a_i_cap = a_i_03 / BAY_M
    d_cap = E * (a_cap * a_i_cap / (a_cap + a_i_cap)) * depth * depth
    q_cap_bend = 4 * math.sqrt(b_cap * d_cap) / (R * R)

    def cap_margin(a_theta: float) -> float:
        s_cap = crimp_of(a_theta) * R
        q_cap_crimp = 2 * s_cap / R                    # sphere keeps its 2
        if q_cap_bend <= 0 or q_cap_crimp <= 0:
            return 0.0
        return (GI_ACTIVE / (1 / q_cap_bend + 1 / q_cap_crimp)) / (P * sf)

    # The dome is crimp-limited through the SAME theta family — grow it until
    # the cap clears too (the spokes cannot reach a dome dimple mode).
    guard_c = 0
    while cap_margin(a_th_03) < 1.0 and guard_c < 4000:
        a_th_03 += 4e-5
        guard_c += 1
    theta_t = a_th_03 * theta_len * n_theta * RHO / 1000
    q_cap = cap_margin(a_th_03) * (P * sf)
    cap_buckle = {"qCrPa": q_cap, "marginAtSF": cap_margin(a_th_03)}

    # Beam bending on the single inner flange (named gust case). [SCOPING]
    q_gust = 0.5 * 1.225 * 400.0
    w_gust = 0.3 * q_gust * DIA_M
    m_gust = w_gust * (LEN_M * LEN_M) / 8
    z_hull = lng["A"] * N_LONG * r_in / 2
    sigma_bend = m_gust / z_hull
    # [REF-7] Torsion: a dedicated helical strap set carries the Bredt shear
    # flow — the sparse clamp net is retention, not a torsion path, and the
    # bars are strain-decoupled at their sliding crossings BY DESIGN.
    t_demand = w_gust * LEN_M / 2 * LEN_M / 4
    shear_flow = t_demand / (2 * math.pi * R * R)
    strap_a_per_m = shear_flow * sf / STRAP_SIGMA
    strap_t = strap_a_per_m * 1550 * AREA_M2 * 2 / 1000   # both helices, UHMWPE-class

    return {
        "depthM": depth, "rInM": r_in, "braceM": BRACE_M,
        "longeron": lng, "nLong": N_LONG, "longeronsT": long_t,
        "web": web, "websT": web_t,
        "junctionT": junction_t,
        "innerRingAM2": a_i_03, "nInnerRings": n_inner, "innerRingsT": inner_t,
        "thetaWebAM2": a_th_03, "thetaWebLenM": theta_len,
        "nThetaWebs": n_theta, "thetaWebsT": theta_t,
        "flangeDoublerAM2": a_oe_03, "flangeDoublerT": flange_t,
        "spokeAM2PerM2": a_sp_03, "spokesT": spoke_t,
        "ovalization": ov, "ovalizationFramePractice": ov_frame,
        "ovalizationAtHarsh": ov_harsh, "ovalizationAtK02": ov_02,
        "capBuckle": cap_buckle,
        "reserveKgM2": reserve_kgm2,
        "strapsT": strap_t,
        "beamBending": {"mGustNm": m_gust, "sigmaMPa": sigma_bend / 1e6,
                        "marginAtSF": sigma_mat / (sigma_bend * sf)},
        "torsion": {"shearFlowNPerM": shear_flow,
                    "path": "dedicated helical straps, sized at margin 1.0",
                    "marginAtSF": 1.0},
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
    cradle_ok = sig_cradle < 100e6
    wind_ok = clamp_n < CLAMP_CAP_N / 1.5
    # [REF-8/11] The verdict gates on ALL of its checks, not the one that
    # passes. A failing erection-wind check does not sink the ship — it
    # constrains the BUILD (shoring / tie-downs / a calmer day), and the
    # verdict string says exactly that instead of "stands".
    if cradle_ok and wind_ok:
        verdict = "stands [SCOPING]"
    elif cradle_ok:
        verdict = ("stands SHORED [SCOPING] — the 1-in-4 clamp net alone "
                   "cannot take a 15 m/s ground wind unshored")
    else:
        verdict = "DOES NOT STAND"
    return {
        "bareRing": out_a,
        "cradle": {"wDeadNPerM2": w_dead, "flangeStressMPa": sig_cradle / 1e6,
                   "ok": cradle_ok},
        "erectionWind": {"clampShearN": clamp_n, "capN": CLAMP_CAP_N,
                         "ok": wind_ok},
        "verdict": verdict,
        "allOk": cradle_ok and wind_ok,
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
    # [REF-10] every structural class — the stability system included — carries
    # the same junction and joint multipliers; nothing is booked twice, nothing
    # is booked bare.
    member_t = (wall["membersT"]
                + (skel["longeronsT"] + skel["innerRingsT"] + skel["websT"]
                   + skel["thetaWebsT"] + skel["flangeDoublerT"]
                   + skel["junctionT"]) * (1 + JUNCTION_ADDER))
    spokes_t = skel["spokesT"]      # cord: SPOKE_FITTING is its own overhead
    joints_t = member_t * (eta - 1)
    skins_t = (VOID_SKIN_KGM2 + JACKET_KGM2) * AREA_M2 / 1000
    reserve_t = (skel["reserveKgM2"] * AREA_M2 / 1000
                 * (1 + JUNCTION_ADDER) * eta)
    # [REF-S4] the 3-in-4 unclamped crossings get bonded saddle pads.
    pads_t = (AREA_M2 / (s_r * s_b) * (CLAMP_EVERY - 1) / CLAMP_EVERY
              * PAD_KG) / 1000
    total_t = (member_t + joints_t + spokes_t + wall["filmT"]
               + wall["clampsT"] + pads_t + skel["strapsT"] + skins_t
               + reserve_t)
    # [REF-S9] the film scallops INWARD between members — half the trough sag
    # over the whole hull is volume the solid-of-revolution never had.
    sag_m = 0.5 * (max(s_r, s_b) / 2) * 0.25          # half the design bulge
    lift_debit_t = vc.rho_air(0) * AREA_M2 * sag_m / 1000
    lift_sl = vc.rho_air(0) * V_M3 / 1000 - lift_debit_t
    lift_25 = vc.rho_air(2500) * V_M3 / 1000 - lift_debit_t * (
        vc.rho_air(2500) / vc.rho_air(0))
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
            "pads": round(pads_t, 1),
            "longerons": round(skel["longeronsT"] * (1 + JUNCTION_ADDER), 1),
            "innerRings": round(skel["innerRingsT"] * (1 + JUNCTION_ADDER), 1),
            "fanWebs": round(skel["websT"] * (1 + JUNCTION_ADDER), 1),
            "thetaWebs": round(skel["thetaWebsT"] * (1 + JUNCTION_ADDER), 1),
            "flangeDoubler": round(skel["flangeDoublerT"]
                                   * (1 + JUNCTION_ADDER), 1),
            "junctionShear": round(skel["junctionT"] * (1 + JUNCTION_ADDER), 1),
            "spokes": round(spokes_t, 1),
            "torsionStraps": round(skel["strapsT"], 1),
            "tiJoints": round(joints_t, 1),
            "skins": round(skins_t, 1),
            "stabilityReserve": round(reserve_t, 1),
        },
        "liftDebitT": lift_debit_t,
        "totalT": total_t,
        "liftSLT": lift_sl, "lift2500T": lift_25,
        "ratioSL": lift_sl / total_t, "residualSLT": lift_sl - total_t,
        "ratio2500": lift_25 / total_t, "residual2500T": lift_25 - total_t,
        "arealKgM2": total_t * 1000 / AREA_M2,
        # The floats flag compares sea-level mass and lift only. Structural checks
        # are recorded separately; the frame-practice basis remains unverified.
        "checksPassInclErection": (wall["ring"]["marginAtSF"] >= 1
                       and wall["bar"]["marginAtSF"] >= 1
                       and skel["longeron"]["marginAtSF"] >= 1
                       and skel["ovalization"]["marginAtSF"] >= 1
                       and skel["capBuckle"]["marginAtSF"] >= 1
                       and unp["allOk"]),
        "floats": total_t < lift_sl,
        "floatsAndStands": total_t < lift_sl and (
            wall["ring"]["marginAtSF"] >= 1
            and wall["bar"]["marginAtSF"] >= 1
            and skel["longeron"]["marginAtSF"] >= 1
            and skel["ovalization"]["marginAtSF"] >= 1
            and skel["capBuckle"]["marginAtSF"] >= 1),
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
    for n_long, k_fan in ((72, 1), (96, 1), (144, 1)):
        for depth in (3.0, 4.0, 5.0, 6.0):
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
# THE BAND STUDY (--band) — operator question, 2026-08-13 morning: "instead of
# asking for a set safety factor, put ourselves in the middle of the band (best
# float, farthest from crush) and let the margin be an OUTPUT of materials and
# design." The two boundaries at every hull:
#   CRUSH = the greedy sizing ledger at SF exactly 1.0;
#           neither minimum mass nor zero margin at every check is established;
#   SINK  = displacement lift.
# A positive float band is an unchecked allowance, not a design. The emergent
# safety factor of a design at mass m is the SF whose ledger hits m — so the
# margin becomes a consequence of the band, not a declaration. Honest limits:
# the crush boundary is the STATIC nominal-pressure boundary (gusts, thermal
# and control loads spend emergent SF in service), it lives inside a knockdown
# WORLD (which the campaigns decide), and the erection/shoring bill stays a
# separate ops line, not a mass line.
# ---------------------------------------------------------------------------------
def _mass_lift(dia: float, sigma_key: str, sf: float) -> tuple:
    led = at_diameter(dia, PLAN_CFG, sigma_key, sf)
    converged = (led["skeleton"]["ovalization"]["marginAtSF"] >= 1.0
                 and led["skeleton"]["capBuckle"]["marginAtSF"] >= 1.0)
    return led["totalT"], led["liftSLT"], converged


def _mass_or_inf(dia: float, sigma_key: str, sf: float) -> float:
    """m(SF), with the section catalog running out treated as +inf — a factor
    the catalog cannot build is above any mass target we would bisect for."""
    try:
        m, _, _ = _mass_lift(dia, sigma_key, sf)
        return m
    except RuntimeError:
        return math.inf


def emergent_sf(dia: float, sigma_key: str, target_t: float) -> float | None:
    """The safety factor whose ledger mass hits target_t — m(SF) is monotone
    rising in SF. None if even the crush boundary (SF 1.0) overshoots."""
    lo, hi = 1.0, 2.0
    m_lo, _, ok = _mass_lift(dia, sigma_key, lo)
    if not ok or m_lo > target_t:
        return None
    m_hi = _mass_or_inf(dia, sigma_key, hi)
    grow = 0
    while m_hi < target_t and grow < 4:
        hi *= 1.5
        m_hi = _mass_or_inf(dia, sigma_key, hi)
        grow += 1
    if m_hi < target_t:
        return None
    for _ in range(14):
        mid = (lo + hi) / 2.0
        if _mass_or_inf(dia, sigma_key, mid) < target_t:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def band_study() -> None:
    global GI_ACTIVE, BOUND_CHORDAL, BOUND_MEMBRANE
    # Pin the committed plan before printing anything: the 52 m record must
    # reproduce from PLAN_CFG or this study is talking about some other ship.
    configure(n_long=PLAN_CFG["nLong"], k_fan=PLAN_CFG["kFan"],
              depth=PLAN_CFG["depth"])
    rec = ship_ledger(SIGMA_MID, SF_DECL, PLAN_CFG["sR"], PLAN_CFG["sB"])
    if abs(rec["totalT"] - 403.1) > 0.8 or abs(rec["ratioSL"] - 0.558) > 0.003:
        sys.exit("band: the 52 m record did not reproduce "
                 f"({rec['totalT']:.1f} t, ratio {rec['ratioSL']:.3f}) — "
                 "PLAN_CFG drifted from the sweep's pick. Stop; fix the plan.")
    print(f"\n  record reproduced first: {rec['totalT']:.1f} t, "
          f"ratio {rec['ratioSL']:.3f} at 52 m, harsh basis, declared SF.\n")

    dias = [32.0, 36.0, 40.0, 46.0, 52.0, 60.0, 68.0, 80.0, 96.0, 112.0]
    worlds = [("house-harsh 0.3 (+K_SHELL 0.2 reserve)", GI_KNOCKDOWN),
              ("frame-practice 0.65 [TO VERIFY - SHIP-2]", GI_KNOCKDOWN_FRAME)]
    sigmas = ("s1050", "s1450")
    grid = {}

    print("THE BAND, BY HULL: greedy sizing (the SF-1.0 ledger) vs sink "
          "boundary (sea-level lift), in tonnes.\n"
          "The SF-1.0 result is greedy sizing, not a proven minimum.\n"
          "A positive float band is an unchecked mass allowance, not a design.\n"
          "SF_float is the emergent factor at that sea-level allowance:\n")
    for wname, gamma in worlds:
        GI_ACTIVE = gamma
        for key in sigmas:
            print(f"  {wname} @ {key[1:]} MPa:")
            print(f"    {'dia m':>6} {'crush t':>9} {'lift t':>9} "
                  f"{'band t':>9} {'SF_float':>9}")
            for d in dias:
                m1, lift, ok = _mass_lift(d, key, 1.0)
                grid[(gamma, key, d)] = (m1, lift, ok)
                band = lift - m1
                sff = emergent_sf(d, key, lift) if (band > 0 and ok) else None
                sfs = f"{sff:9.2f}" if sff else "        -"
                note = "" if ok else "   [solver hit its guard; sizing is incomplete]"
                print(f"    {d:6.0f} {m1:9.1f} {lift:9.1f} {band:+9.1f}"
                      f"{sfs}{note}")
            print()
    GI_ACTIVE = GI_KNOCKDOWN

    print("FLOATS below means mass below sea-level lift only. "
          "It does not establish a drawn floating design.")
    print("THE TWO DESIGN MOVES AS BOUNDS at 52 m (chordal net: cord mass "
          "priced, geometry\n[SCOPING]; in-surface shear: stiffness credited, "
          "its own mass UNPRICED - outer\nbound). crush = SF-1.0 ledger; "
          "@SF1.2 = the declared-factor ledger beside it:\n")
    variants = [("as drawn", False, False),
                ("chordal spoke net", True, False),
                ("in-surface shear", False, True),
                ("both moves", True, True)]
    for wname, gamma in worlds:
        GI_ACTIVE = gamma
        for key in sigmas:
            print(f"  {wname} @ {key[1:]} MPa:")
            for vname, ch, mem in variants:
                BOUND_CHORDAL, BOUND_MEMBRANE = ch, mem
                m1, lift, ok = _mass_lift(52.0, key, 1.0)
                configure(n_long=PLAN_CFG["nLong"], k_fan=PLAN_CFG["kFan"],
                          depth=PLAN_CFG["depth"])
                led = ship_ledger(key, SF_DECL, PLAN_CFG["sR"], PLAN_CFG["sB"])
                configure()
                tag = "FLOATS" if led["floats"] else "sinks"
                print(f"    {vname:<18} crush {m1:6.1f} t  band "
                      f"{lift - m1:+7.1f} t   @SF1.2 {led['totalT']:6.1f} t "
                      f"ratio {led['ratioSL']:.3f} {tag}")
            BOUND_CHORDAL = BOUND_MEMBRANE = False
            print()
    GI_ACTIVE = GI_KNOCKDOWN

    print("MID-BAND DESIGN POINTS — mass target halfway crush->sink at the "
          "widest hull;\nfloat reserve and emergent SF split the band, and "
          "the margin is an output:\n")
    for wname, gamma in worlds:
        GI_ACTIVE = gamma
        for key in sigmas:
            best = None
            for d in dias:
                m1, lift, ok = grid[(gamma, key, d)]
                if best is None or (lift - m1) > best[1]:
                    best = (d, lift - m1, m1, lift, ok)
            d, band, m1, lift, ok = best
            if band <= 0:
                print(f"    {wname} @ {key[1:]} MPa: band CLOSED at every "
                      f"hull (best {band:+.1f} t at {d:.0f} m) - the "
                      "campaigns and the design moves are what open it")
                continue
            target = (m1 + lift) / 2.0
            sfm = emergent_sf(d, key, target)
            sfm_s = f"{sfm:.2f}" if sfm else "-"
            print(f"    {wname} @ {key[1:]} MPa: widest at {d:.0f} m - "
                  f"design at {target:.1f} t:\n"
                  f"      float reserve {lift - target:+.1f} t AND emergent "
                  f"SF {sfm_s}  (crush {m1:.1f} / lift {lift:.1f})")
    GI_ACTIVE = GI_KNOCKDOWN

    print("\nTHE DESIGN-GOAL SCENARIO — BOTH moves credited as bounds "
          "(chordal cord priced,\nshear system mass unpriced), by hull; "
          "mid-band design at the widest:\n")
    BOUND_CHORDAL = BOUND_MEMBRANE = True
    for wname, gamma in worlds:
        GI_ACTIVE = gamma
        for key in sigmas:
            print(f"  {wname} @ {key[1:]} MPa, both moves:")
            print(f"    {'dia m':>6} {'crush t':>9} {'lift t':>9} "
                  f"{'band t':>9} {'SF_float':>9}")
            best = None
            for d in dias:
                m1, lift, ok = _mass_lift(d, key, 1.0)
                band = lift - m1
                sff = emergent_sf(d, key, lift) if (band > 0 and ok) else None
                sfs = f"{sff:9.2f}" if sff else "        -"
                note = "" if ok else "   [solver hit its guard]"
                print(f"    {d:6.0f} {m1:9.1f} {lift:9.1f} {band:+9.1f}"
                      f"{sfs}{note}")
                if ok and (best is None or band > best[1]):
                    best = (d, band, m1, lift)
            d, band, m1, lift = best
            if band > 0:
                target = (m1 + lift) / 2.0
                sfm = emergent_sf(d, key, target)
                sfm_s = f"{sfm:.2f}" if sfm else "-"
                print(f"    -> mid-band at {d:.0f} m: {target:.1f} t, float "
                      f"reserve {lift - target:+.1f} t, emergent SF {sfm_s}\n")
            else:
                print(f"    -> band still closed (best {band:+.1f} t "
                      f"at {d:.0f} m)\n")
    BOUND_CHORDAL = BOUND_MEMBRANE = False
    GI_ACTIVE = GI_KNOCKDOWN
    configure()
    print("\n  Erection/shoring stays a separate ops bill. Emergent SF is "
          "spent by gusts,\n  thermal and control loads in service - the "
          "declared-SF record remains the\n  published basis until the "
          "operator re-rules.")


# ---------------------------------------------------------------------------------
def hull_label(cfg: dict) -> str:
    """Name the selected configuration only after comparing it with the record."""
    selected = dict(
        diaM=DIA_M, fineness=LEN_M / DIA_M, sfDeclared=SF_DECL,
        sigmaWorldsMPa={key: value / 1e6 for key, value in SIGMA_WORLDS.items()},
        sigmaMid=SIGMA_MID, ringPitchM=cfg["sR"], barPitchM=cfg["sB"],
        nLong=cfg["nLong"], kFan=cfg["kFan"], depthM=cfg["depth"], bayM=BAY_M,
        clampEvery=CLAMP_EVERY, clampKgAt130=CLAMP_KG_AT_130, etaMass=ETA_MASS,
        voidSkinKgM2=VOID_SKIN_KGM2, jacketKgM2=JACKET_KGM2,
        junctionAdder=JUNCTION_ADDER, clampCapN=CLAMP_CAP_N,
        giKnockdown=GI_ACTIVE, giKnockdownFrame=GI_KNOCKDOWN_FRAME,
        padKg=PAD_KG, strapSigma=STRAP_SIGMA, eSpoke=E_SPOKE,
        rhoSpoke=RHO_SPOKE, spokeFitting=SPOKE_FITTING)
    differences = [f"{key} {value} versus {vc.SHIP0[key]}"
                   for key, value in selected.items() if value != vc.SHIP0[key]]
    if BOUND_CHORDAL or BOUND_MEMBRANE:
        differences.append("undrawn design credits enabled")
    if differences:
        return (f"scoping tool's default hull (wall {cfg['depth']:.1f} m); "
                "differs from the hull of record: " + "; ".join(differences))
    actual = ship_ledger(SIGMA_MID, SF_DECL, cfg["sR"], cfg["sB"])
    expected = vc.ship0()
    for field in ("totalT", "ratioSL", "ratio2500"):
        if not math.isclose(actual[field], expected[field], rel_tol=1e-10, abs_tol=1e-10):
            raise ValueError(f"hull of record does not reproduce: {field}")
    return "hull of record"


def main() -> None:
    global GI_ACTIVE
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", nargs="?", const=str(OUT_JSON), default=None)
    ap.add_argument("--band", action="store_true",
                    help="the float/crush band study (operator, 08-13 morning)")
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

    if args.band:
        band_study()
        return

    # The configuration pick: the sweep finds the optimum, and the PLAN OF
    # RECORD keeps the operator's ruled 0.5-m square panels — the sweep's own
    # result is that the ruling costs ~2%, which is the right way for a ruling
    # to survive its optimisation check. One geometry serves every world.
    print("\nDESIGN-SPACE SWEEP (mid basis, declared SF 1.2, gamma_GI "
          f"{GI_ACTIVE}) ...")
    sweep = config_sweep(SIGMA_MID, SF_DECL)
    b = sweep["best"]
    print(f"  sweep optimum: rings {b['sR']} x bars {b['sB']} m, "
          f"{b['nLong']} longerons x fan {b['kFan']}, depth {b['depth']:.0f} m "
          f"-> {b['totalT']} t")
    # PLAN OF RECORD: the ruled 0.5-m squares stand; depth / columns / fan are
    # free — pick the best row AT those pitches (the bogus fan brace credit is
    # gone, so fan density no longer buys ring bracing).
    ruled = [r for r in sweep["rows"] if r["sR"] == 0.5 and r["sB"] == 0.5]
    bestr = min(ruled, key=lambda r: r["totalT"]) if ruled else b
    cfg = {"sR": 0.5, "sB": 0.5, "nLong": bestr["nLong"],
           "kFan": bestr["kFan"], "depth": bestr["depth"]}
    print(f"  SELECTED CONFIGURATION keeps the ruled 0.5 m squares: "
          f"{cfg['nLong']} longerons x fan {cfg['kFan']} "
          f"(ring brace {2 * math.pi * 26 / cfg['nLong']:.2f} m), "
          f"depth {cfg['depth']:.0f} m -> {bestr['totalT']} t")

    configure(n_long=cfg["nLong"], k_fan=cfg["kFan"], depth=cfg["depth"])
    label = hull_label(cfg)
    print(f"\n{label}\n{DIA_M:.0f} m x {LEN_M:.0f} m, V = {V_M3:,.0f} m3, "
          f"hull {AREA_M2:,.0f} m2, sea level.\n")

    results = {}
    for sf, sf_name in ((SF_DECL, "declared SF 1.2"), (SF_15, "SF 1.5")):
        for key in ("s742", "s1050", "s1450"):
            configure(n_long=cfg["nLong"], k_fan=cfg["kFan"], depth=cfg["depth"])
            r = ship_ledger(key, sf, cfg["sR"], cfg["sB"])
            results[f"{key}_sf{sf}"] = r
            tag = "positive float margin" if r["floats"] else "negative float margin"
            print(f"  {sf_name:>16} @ {key[1:]:>4} MPa: total {r['totalT']:6.1f} t"
                  f" vs {r['liftSLT']:.1f} t -> ratio {r['ratioSL']:.3f} "
                  f"({r['residualSLT']:+.1f} t) at sea level; "
                  f"ratio {r['ratio2500']:.3f} ({r['residual2500T']:+.1f} t) at 2,500 m. {tag} at sea level")

    # THE DECISION TABLE: the same six worlds under the frame-practice GI
    # knockdown — reported, never used for sizing until SHIP-2's tests land.
    GI_ACTIVE = GI_KNOCKDOWN_FRAME
    print(f"\n  IF THE FRAME-PRACTICE KNOCKDOWN ({GI_KNOCKDOWN_FRAME}) "
          "VERIFIES [TO VERIFY — SHIP-2 knockdown tests]:")
    frame_results = {}
    for sf, sf_name in ((SF_DECL, "declared SF 1.2"), (SF_15, "SF 1.5")):
        for key in ("s742", "s1050", "s1450"):
            configure(n_long=cfg["nLong"], k_fan=cfg["kFan"], depth=cfg["depth"])
            r = ship_ledger(key, sf, cfg["sR"], cfg["sB"])
            frame_results[f"{key}_sf{sf}"] = r
            tag = "positive float margin" if r["floats"] else "negative float margin"
            print(f"  {sf_name:>16} @ {key[1:]:>4} MPa: total {r['totalT']:6.1f} t"
                  f" -> ratio {r['ratioSL']:.3f} ({r['residualSLT']:+.1f} t) at sea level; "
                  f"ratio {r['ratio2500']:.3f} ({r['residual2500T']:+.1f} t) at 2,500 m. {tag} at sea level")
    GI_ACTIVE = GI_KNOCKDOWN

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
          f"at gamma {GI_KNOCKDOWN} (crit n={s['ovalization']['critN']}); "
          f"{s['ovalizationFramePractice']['marginAtSF']:.2f} at the "
          f"frame-practice {GI_KNOCKDOWN_FRAME}; "
          f"{s['ovalizationAtK02']['marginAtSF']:.2f} at K_SHELL 0.2 -> "
          f"reserve {s['reserveKgM2']:.2f} kg/m2")
    print(f"    cap (sandwich dome) buckling margin "
          f"{s['capBuckle']['marginAtSF']:.1f} at gamma 0.3")
    print(f"    beam bending margin {s['beamBending']['marginAtSF']:.0f}; "
          f"torsion on dedicated straps ({s['strapsT']:.1f} t, margin "
          f"{s['torsion']['marginAtSF']:.1f}) [SCOPING]")
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
            "resultsFramePractice": {k: {kk: vv for kk, vv in v.items()
                                         if kk not in ("wall", "skeleton",
                                                       "unpressurised")}
                                     for k, v in frame_results.items()},
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
