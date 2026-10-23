#!/usr/bin/env python3
"""MAINLINE-023. P3 node and member-end mass at the 011b SiC point.

Own arithmetic. arcs.py is not executed. The 5 percent joint row is recomputed
here only as a regression against the filed 011b SiC point.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
T0 = datetime.now(ZONE).isoformat(timespec="seconds")

# 011b case, same printed constants.
R = 10.0
P_EXT = 95460.8379139
L_MASS = 4889.44215019
M_FILM = 97.515
M_NODE = 0.02
M_SYS = 50.0
SIGMA_FILM = 1.5e9
T_FILM = 8e-5
C_LOCAL = 0.6
JOINT_FRAC = 0.05
C_TRI = 4.0 * math.sqrt(1.5)
N_RO = 4000
SLENDER = 3.0
RHO = 3100.0
E_SIC = 410e9
SIG = 3900e6
SIG_FLEX = 380e6
SIG_COMP = 3900e6

# Sourced allowables. QUESTIONABLE where the adherend is not SiC.
TAU_ADH = 28.9e6          # EA 9394 lap shear, 25 C, aluminium adherend
TAU_BRAZE = 25.0e6        # Cusil-ABA SiC/metal compressive shear, lab
RHO_TI = 4430.0
SIG_TI = 827e6            # AMS 4911 annealed minimum yield
RHO_INVAR = 8050.0
SIG_INVAR = 276e6         # Carpenter annealed yield
RHO_CFRP = 1550.0
# T700S / Toray 250 F epoxy, normalized 60% Vf, ASTM D695. The member is
# in compression, so the wrap is sized on 1470 MPa, not the 2550 MPa tensile.
SIG_CFRP = 1470e6
SIG_CFRP_TENSILE = 2550e6
TAU_TI_SHEAR = 0.6 * SIG_TI
RHO_OF = {"ti_sleeve": RHO_TI, "invar_sleeve": RHO_INVAR, "cfrp_wrap": RHO_CFRP}

# MAINLINE-022 filed rpt-mainline022-grok-p3-optimistic-floating-point-1020.
# Carried equilateral rows. N is their n_at_ext, not p*R*s/2.
POINT_022 = (
    {
        "name": "carried_equilateral_k0.2",
        "s_m": 3.0,
        "r_o_m": 0.13670908289556455,
        "A_m2": 0.0009170752328248388,
        "t_w_m": 0.0010718489471981119,
        "nodes": 163.2266101541527,
        "members": 483.6798304624581,
        "N_N": 1423812.236919077,
        "allowance_kg": 216.4271448895479,
        "sigma_axial_Pa": 1552557724.7717745,
    },
    {
        "name": "carried_equilateral_k0.4",
        "s_m": 2.5,
        "r_o_m": 0.10245509760694975,
        "A_m2": 0.0007648558401364123,
        "t_w_m": 0.0011951062469423707,
        "nodes": 234.16631862197994,
        "members": 696.4989558659398,
        "N_N": 1188580.948835369,
        "allowance_kg": 216.4271448895479,
        "sigma_axial_Pa": 1553993427.8639817,
    },
)

S_ALL = [round(0.4 + 0.02 * i, 3) for i in range(131)]  # 0.40 to 3.00


def half_up(value: float, places: int) -> str:
    quant = Decimal("1").scaleb(-places)
    return str(Decimal(format(value, ".20f")).quantize(quant, rounding=ROUND_HALF_UP))


def grid(s: float):
    nodes = 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s) + 2.0
    members = 3.0 * nodes - 6.0
    budget = L_MASS - M_FILM - M_NODE * nodes - M_SYS
    return nodes, members, budget


def force(s: float) -> float:
    """Equilateral member force, p*R*s/(2*sqrt(3)). p*R*s/2 is the two-way value."""
    return P_EXT * R * s / (2.0 * math.sqrt(3.0))


def force_twoway(s: float) -> float:
    return P_EXT * R * s / 2.0


def bond_length(n_force: float, r_o: float, tau: float) -> float:
    return n_force / (2.0 * math.pi * r_o * tau)


def section(area: float, r_o: float):
    disc = r_o * r_o - area / math.pi
    if disc <= 0.0:
        return None
    r_i = math.sqrt(disc)
    t_w = r_o - r_i
    inertia = 0.25 * math.pi * (r_o ** 4 - r_i ** 4)
    return r_i, t_w, inertia


def scores(s: float, r_o: float, area: float, k: float, equilateral: bool = True):
    sec = section(area, r_o)
    if sec is None:
        return None
    r_i, t_w, inertia = sec
    n_force = force(s) if equilateral else force_twoway(s)
    sig_app = n_force / area
    sf_y = SIG / sig_app
    sf_e = (math.pi ** 2 * E_SIC * inertia / (s * s)) / n_force
    sig_loc = C_LOCAL * E_SIC * t_w / r_o
    sf_l = sig_loc / sig_app
    sf_f = (2.0 * SIGMA_FILM * T_FILM / s) / P_EXT
    rg2 = inertia / area
    eta = (s / 1000.0) * r_o / rg2
    sig_e = math.pi ** 2 * E_SIC * rg2 / (s * s)
    phi = 0.5 * (SIG + (eta + 1.0) * sig_e)
    disc = phi * phi - SIG * sig_e
    if disc < 0.0:
        return None
    sig_cr = phi - math.sqrt(disc)
    sf_p = sig_cr / sig_app
    g_unit = E_SIC * math.sqrt(inertia * area) / (s * R * R)
    sf_g = k * C_TRI * g_unit / P_EXT
    pairs = (("yield", sf_y), ("euler", sf_e), ("local", sf_l), ("film", sf_f), ("perry", sf_p), ("global", sf_g))
    gov, least = pairs[0]
    for name, val in pairs[1:]:
        if val < least:
            gov, least = name, val
    return {
        "r_i_m": r_i,
        "t_w_m": t_w,
        "I_m4": inertia,
        "sigma_axial_Pa": sig_app,
        "SF_yield": sf_y,
        "SF_euler": sf_e,
        "SF_local": sf_l,
        "SF_film": sf_f,
        "SF_perry": sf_p,
        "SF_global": sf_g,
        "governing": gov,
        "SF_least": least,
        "sigma_contact_compression_Pa": sig_app,
        "SF_contact_on_3900": SIG_COMP / sig_app,
        "SF_contact_on_flexure_380": SIG_FLEX / sig_app,
    }


def sleeve_t(kind: str, m_end, length, r_o: float):
    rho = RHO_OF.get(kind)
    if rho is None or m_end is None or not length:
        return None
    return m_end / (length * 2.0 * math.pi * r_o * rho)


def end_at_force(kind: str, n_force: float, r_o: float, area: float | None):
    """One member end. area is the ceramic section, used by the braze socket."""
    if kind == "ti_sleeve":
        length = bond_length(n_force, r_o, TAU_ADH)
        area_m = n_force / SIG_TI
        return area_m * length * RHO_TI, length, area_m / (2.0 * math.pi * r_o)
    if kind == "invar_sleeve":
        length = bond_length(n_force, r_o, TAU_ADH)
        area_m = n_force / SIG_INVAR
        return area_m * length * RHO_INVAR, length, area_m / (2.0 * math.pi * r_o)
    if kind == "cfrp_wrap":
        length = bond_length(n_force, r_o, TAU_ADH)
        area_m = n_force / SIG_CFRP
        return area_m * length * RHO_CFRP, length, area_m / (2.0 * math.pi * r_o)
    if kind == "sic_braze":
        if area is None:
            raise ValueError("braze mass needs the tube area")
        length = bond_length(n_force, r_o, TAU_BRAZE)
        return area * length * RHO, length, None
    raise ValueError(kind)


def tube_budget(kind: str, s: float, r_o: float):
    nodes, members, budget = grid(s)
    if kind == "percent5":
        m_tube = budget / (1.0 + JOINT_FRAC)
        m_joint = budget - m_tube
        area = m_tube / (members * s * RHO)
        return nodes, members, budget, m_tube, m_joint, area, None, None
    if kind == "sic_braze":
        # m_joint = 2*L/s * m_tube, L from the braze shear on the outside radius.
        length = bond_length(force(s), r_o, TAU_BRAZE)
        m_tube = budget / (1.0 + 2.0 * length / s)
        m_joint = budget - m_tube
        area = m_tube / (members * s * RHO)
        return nodes, members, budget, m_tube, m_joint, area, length, m_joint / (2.0 * members)
    n_force = force(s)
    if kind in ("ti_sleeve", "invar_sleeve", "cfrp_wrap"):
        m_end, length, _thick = end_at_force(kind, n_force, r_o, None)
    else:
        raise ValueError(kind)
    m_joint = 2.0 * members * m_end
    m_tube = budget - m_joint
    area = m_tube / (members * s * RHO) if m_tube > 0.0 else -1.0
    return nodes, members, budget, m_tube, m_joint, area, length, m_end


def optimise(kind: str, k: float, equilateral: bool = True):
    best = None
    for s in S_ALL:
        nodes, members, budget = grid(s)
        if budget <= 0.0 or members <= 0.0:
            continue
        r_max = min(0.25, s / SLENDER)
        # Radius grid. Joint mass depends on radius, so the legal window is checked inside.
        for i in range(N_RO):
            r_o = r_max * (i + 1) / N_RO
            nodes, members, budget, m_tube, m_joint, area, length, m_end = tube_budget(kind, s, r_o)
            if m_tube <= 0.0 or area <= 0.0:
                continue
            if r_o <= math.sqrt(area / math.pi) * 1.0001:
                continue
            pack = scores(s, r_o, area, k, equilateral)
            if pack is None:
                continue
            row = {
                "s_m": s,
                "r_o_m": r_o,
                "A_m2": area,
                "nodes": nodes,
                "members": members,
                "m_tube_kg": m_tube,
                "m_joint_kg": m_joint,
                "m_end_kg": m_end,
                "bond_or_insert_m": length,
                "sleeve_t_m": sleeve_t(kind, m_end, length, r_o),
                "ends_per_node": 2.0 * members / nodes,
                "m_joint_per_node_kg": m_joint / nodes,
                **pack,
            }
            if best is None or row["SF_least"] > best["SF_least"]:
                best = row
    return best


def frozen(kind: str, k: float, s: float, r_o: float):
    nodes, members, budget, m_tube, m_joint, area, length, m_end = tube_budget(kind, s, r_o)
    pack = None
    legal = area > 0.0 and r_o > math.sqrt(max(area, 0.0) / math.pi) * 1.0001
    if legal:
        pack = scores(s, r_o, area, k)
    return {
        "s_m": s,
        "r_o_m": r_o,
        "legal_at_frozen_radius": legal and pack is not None,
        "nodes": nodes,
        "members": members,
        "budget_kg": budget,
        "m_tube_kg": m_tube,
        "m_joint_kg": m_joint,
        "m_end_kg": m_end,
        "bond_or_insert_m": length,
        "sleeve_t_m": sleeve_t(kind, m_end, length, r_o),
        "A_m2": area,
        "m_joint_per_node_kg": m_joint / nodes,
        "versus_225_kg": m_joint / 225.47208004250842,
        "scores": pack,
    }


def pin_clevis(n_force: float):
    # Double-shear pin, length 3 diameters. The rough 0.5 kg figure.
    diameter = math.sqrt(n_force / (0.5 * math.pi * TAU_TI_SHEAR))
    length = 3.0 * diameter
    mass = (math.pi / 4.0) * diameter ** 2 * length * RHO_TI
    return {"d_m": diameter, "length_m": length, "mass_kg": mass, "tau_Pa": TAU_TI_SHEAR}


def size_stated(kind: str, point: dict):
    """Joint hardware at a filed force and geometry. Does not rescore that card."""
    m_end, length, thick = end_at_force(kind, point["N_N"], point["r_o_m"], point["A_m2"])
    m_joint = 2.0 * point["members"] * m_end
    pin = pin_clevis(point["N_N"])
    bearing = point["N_N"] / (2.0 * pin["d_m"] * point["t_w_m"])
    return {
        "m_end_kg": m_end,
        "bond_or_insert_m": length,
        "sleeve_t_m": thick,
        "m_joint_kg": m_joint,
        "m_joint_per_node_kg": m_joint / point["nodes"],
        "ends_per_node": 2.0 * point["members"] / point["nodes"],
        "versus_allowance": m_joint / point["allowance_kg"],
        "sigma_contact_Pa": point["sigma_axial_Pa"],
        "SF_contact_on_3900": SIG_COMP / point["sigma_axial_Pa"],
        "SF_contact_on_flexure_380": SIG_FLEX / point["sigma_axial_Pa"],
        "pin_kg": pin["mass_kg"],
        "pin_d_m": pin["d_m"],
        "pin_bearing_Pa": bearing,
    }


def main():
    filed = {
        "s_m": 2.04,
        "r_o_m": 0.12368836237368608,
        "A_m2": 0.0006816960123390095,
        "SF_least": 1.2255279468805444,
        "governing": "global",
        "m_joint_kg": 225.47208004250842,
        "m_tube_kg": 4509.441600850166,
        "nodes": 350.67346486624723,
        "members": 1046.0203945987416,
        "k": 0.2,
    }
    n562 = force(2.04)
    n_two = force_twoway(2.04)
    reg = optimise("percent5", 0.2)
    reg04 = optimise("percent5", 0.4)
    reg_two = optimise("percent5", 0.2, equilateral=False)
    frozen_reg = frozen("percent5", 0.2, 2.04, filed["r_o_m"])
    kinds = ("ti_sleeve", "invar_sleeve", "sic_braze", "cfrp_wrap")
    out_kinds = {}
    for kind in kinds:
        out_kinds[kind] = {
            "frozen_k0.2": frozen(kind, 0.2, 2.04, filed["r_o_m"]),
            "reopt_k0.2": optimise(kind, 0.2),
            "reopt_k0.4": optimise(kind, 0.4),
        }
    # Mass coefficients. m_end = C * N^2 / r_o for a sleeve or wrap.
    # Braze: m_end = C_A * A * N / r_o. Nodes and members are functions of s.
    coeff = {}
    for kind, rho, sig, tau in (
        ("ti_sleeve", RHO_TI, SIG_TI, TAU_ADH),
        ("invar_sleeve", RHO_INVAR, SIG_INVAR, TAU_ADH),
        ("cfrp_wrap", RHO_CFRP, SIG_CFRP, TAU_ADH),
    ):
        coeff[kind] = {"C_end_kg_m_per_N2": rho / (sig * 2.0 * math.pi * tau)}
    coeff["sic_braze"] = {"C_end_per_area_1_per_N": RHO / (2.0 * math.pi * TAU_BRAZE)}
    scale_rows = []
    for s_tab in (1.44, 2.04, 3.0, 4.0):
        n_tab = force(s_tab)
        nodes_t, members_t, _budget = grid(s_tab)
        row = {
            "s_m": s_tab,
            "N_N": n_tab,
            "nodes": nodes_t,
            "members": members_t,
            "ends_per_node": 2.0 * members_t / nodes_t,
            "r_o_held_m": filed["r_o_m"],
            "A_held_m2": filed["A_m2"],
            "kinds": {},
        }
        point = {
            "N_N": n_tab,
            "r_o_m": filed["r_o_m"],
            "A_m2": filed["A_m2"],
            "t_w_m": 0.0008802990936851718,
            "nodes": nodes_t,
            "members": members_t,
            "allowance_kg": 225.47208004250842,
            "sigma_axial_Pa": n_tab / filed["A_m2"],
        }
        for kind in kinds:
            row["kinds"][kind] = size_stated(kind, point)
        scale_rows.append(row)
    # Ceramic bearing if a pin were driven through the filed wall.
    pin = pin_clevis(n562)
    t_w = 0.0008802990936851718
    bearing = n562 / (2.0 * pin["d_m"] * t_w)
    checks = []
    checks.append({
        "name": "equilateral N at s 2.04 is 562 kN within 0.1 percent",
        "pass": abs(n562 - 562e3) / 562e3 < 0.001,
        "got": n562,
    })
    checks.append({
        "name": "two-way force is sqrt(3) times the equilateral force",
        "pass": abs(n_two / n562 - math.sqrt(3.0)) < 1e-12,
        "got": n_two / n562,
    })
    checks.append({
        "name": "two-way 5 percent regression finds s 2.04 and SF within 0.5 percent of 1.22553",
        "pass": reg_two is not None and abs(reg_two["s_m"] - 2.04) < 0.021 and abs(reg_two["SF_least"] - filed["SF_least"]) / filed["SF_least"] < 0.005,
        "got_s": None if reg_two is None else reg_two["s_m"],
        "got_sf": None if reg_two is None else reg_two["SF_least"],
    })
    checks.append({
        "name": "frozen 5 percent radius still legal and near the filed SF",
        "pass": frozen_reg["scores"] is not None and abs(frozen_reg["scores"]["SF_least"] - filed["SF_least"]) / filed["SF_least"] < 0.01,
        "got": None if frozen_reg["scores"] is None else frozen_reg["scores"]["SF_least"],
    })
    doc = {
        "schema": 1,
        "card": "MAINLINE-023",
        "unit": "vacuum-mainline023-p3-nodes-1020",
        "started_at": T0,
        "ended_at": datetime.now(ZONE).isoformat(timespec="seconds"),
        "certification": False,
        "tag": "QUESTIONABLE",
        "member_force_N": {
            "s_2.04_equilateral": n562,
            "s_2.04_twoway": n_two,
            "note": "Equilateral N = p*R*s/(2*sqrt(3)). p*R*s/2 is the two-way value. Yield, Euler, local and Perry use the equilateral force. Global and film do not.",
        },
        "mass_coefficients": coeff,
        "filed_011b_point": filed,
        "regression_percent5": {
            "equilateral_k0.2": reg,
            "equilateral_k0.4": reg04,
            "twoway_k0.2": reg_two,
            "frozen_equilateral": frozen_reg,
        },
        "pin_clevis_reference": pin,
        "pin_through_wall_bearing_Pa": bearing,
        "joints": out_kinds,
        "scale_at_held_section": scale_rows,
        "cfrp_allowable_Pa": {"compression": SIG_CFRP, "tensile_not_used": SIG_CFRP_TENSILE},
        "checks": checks,
    }
    # Display block for the card.
    display = {
        "N_kN": half_up(n562 / 1000.0, 1),
        "N_twoway_kN": half_up(n_two / 1000.0, 1),
        "pin_kg": half_up(pin["mass_kg"], 3),
        "pin_d_mm": half_up(pin["d_m"] * 1000.0, 1),
        "bearing_GPa": half_up(bearing / 1e9, 1),
        "wall_MPa": half_up((n562 / filed["A_m2"]) / 1e6, 1),
    }
    for kind in kinds:
        fr = out_kinds[kind]["frozen_k0.2"]
        display[kind] = {
            "end_kg": None if fr["m_end_kg"] is None else half_up(fr["m_end_kg"], 3),
            "joint_kg": half_up(fr["m_joint_kg"], 1),
            "per_node_kg": half_up(fr["m_joint_per_node_kg"], 3),
            "insert_mm": None if fr["bond_or_insert_m"] is None else half_up(fr["bond_or_insert_m"] * 1000.0, 1),
            "sleeve_mm": None if fr["sleeve_t_m"] is None else half_up(fr["sleeve_t_m"] * 1000.0, 2),
            "times_225": half_up(fr["versus_225_kg"], 2),
            "frozen_tw_mm": None if not fr["scores"] else half_up(fr["scores"]["t_w_m"] * 1000.0, 3),
        }
        for label in ("reopt_k0.2", "reopt_k0.4"):
            row = out_kinds[kind][label]
            if row is None:
                display[kind][label] = None
                continue
            sc = row
            display[kind][label] = {
                "s_m": half_up(sc["s_m"], 2),
                "SF": half_up(sc["SF_least"], 3),
                "gov": sc["governing"],
                "joint_kg": half_up(sc["m_joint_kg"], 1),
                "tube_kg": half_up(sc["m_tube_kg"], 1),
                "r_o_mm": half_up(sc["r_o_m"] * 1000.0, 1),
                "t_w_mm": half_up(sc["t_w_m"] * 1000.0, 3),
            }
        if fr["scores"]:
            display[kind]["frozen_SF"] = half_up(fr["scores"]["SF_least"], 3)
            display[kind]["frozen_gov"] = fr["scores"]["governing"]
            display[kind]["contact_MPa"] = half_up(fr["scores"]["sigma_contact_compression_Pa"] / 1e6, 1)
            display[kind]["SF_on_3900"] = half_up(fr["scores"]["SF_contact_on_3900"], 2)
            display[kind]["SF_on_380"] = half_up(fr["scores"]["SF_contact_on_flexure_380"], 3)
    display["scale_held_section"] = []
    for block in scale_rows:
        shown = {"s_m": half_up(block["s_m"], 2), "N_kN": half_up(block["N_N"] / 1000.0, 1)}
        for kind, row in block["kinds"].items():
            shown[kind] = {
                "end_kg": half_up(row["m_end_kg"], 3),
                "joint_kg": half_up(row["m_joint_kg"], 1),
                "per_node_kg": half_up(row["m_joint_per_node_kg"], 3),
            }
        display["scale_held_section"].append(shown)
    doc["display_half_up"] = display
    (ROOT / "RESULTS.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print("checks")
    for c in checks:
        print(("PASS " if c["pass"] else "FAIL ") + c["name"], {k: c[k] for k in c if k not in ("name", "pass")})
    print(json.dumps(display, indent=1))


if __name__ == "__main__":
    main()
