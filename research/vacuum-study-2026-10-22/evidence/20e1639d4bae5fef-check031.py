#!/usr/bin/env python3
"""MAINLINE-031 independent check. Owner scripts are not executed.

Atmosphere, sandwich closure and the equilateral frame are recomputed
from the method text. Published geometry is rescored. The core search
is not repeated.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
OWNER = Path(
    "unpublished-local-ref:9cae3d24fd5d4f59"
    "/.ship/work/outputs/vacuum-mainline031-altitude-margin-1020"
)
CONTINUUM = Path(
    "unpublished-local-ref:3810915cf17e47f1"
    "/.ship/work/outputs/vacuum-mainline030-design-register-1020/CONTINUUM.json"
)
BRIEFS = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019"
)

R = 10.0
V0 = 4.0 / 3.0 * math.pi * R**3
A = 4.0 * math.pi * R**2
P0 = 95460.83791390515
T0 = 284.9
L0 = 4889.442150186961
RD = 287.053
G = 9.80665
LAPSE = 0.0065
ZREF = 500.0
RHO_F = 1850.0
NU = 0.33
E_FACE = 290e9
B_SEAM = 0.06
T_ADH = 0.0002
RHO_ADH = 1250.0
W_SPLICE = 0.0015
RHO_SPLICE = 1100.0
NONCLIM = 125.66370614359174 + 5.0 + 48.89442150186961
SYSTEMS = 100.0
PANEL_TODAY = 0.9144
PANEL_FULL = 4.0
FILM_TODAY = 0.03
FILM_FULL = 0.015
SIGMA_TODAY = 345e6
SIGMA_FULL = 379.2e6
K_TODAY = 0.33
K_FULL = 0.82
LB_FT2 = 0.45359237 / 0.09290304
SIC_E = 410e9
SIC_RHO = 3100.0
SIC_SIGMA = 3900e6
FILM_SIGMA = 1.5e9
FILM_RHO = 970.0
KAPTON_SIGMA = 115.5e6
KAPTON_RHO = 1420.0
C_END_TI = 2.950e-14
NODE_MASS = 0.02


def now() -> str:
    return datetime.now(ZONE).isoformat(timespec="seconds")


def bx_root() -> float:
    x = 0.7
    for _ in range(40):
        x = x - (x**3 + x - 1.0) / (3.0 * x**2 + 1.0)
    return x


BX = bx_root()


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "path": str(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def near(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def mismatch(bag: list, row: str, field: str, card, mine) -> None:
    bag.append({
        "row": row,
        "field": field,
        "card": card,
        "mine": mine,
    })


def day_record(name: str, group: str, dT: float, dp: float, e: float) -> dict:
    Td = T0 + dT
    pd = P0 * (1.0 + dp)
    k = 1.0 - 0.378 * e / pd
    return {
        "id": name,
        "group": group,
        "dT_K": dT,
        "dp_fraction": dp,
        "e500_Pa": e,
        "T500_K": Td,
        "p500_Pa": pd,
        "k": k,
    }


def build_days() -> list[dict]:
    rows = [
        ("ISA", "baseline", 0.0, 0.0, 0.0),
        ("optimistic_heat_only", "optimistic", 10.0, 0.0, 0.0),
        ("optimistic_hot_low_dry", "optimistic", 10.0, -0.01, 0.0),
        ("optimistic_hot_low_wet", "optimistic", 10.0, -0.01, 1000.0),
        ("optimistic_pressure_only_low", "optimistic", 0.0, -0.01, 0.0),
        ("optimistic_hot_high_dry", "optimistic", 10.0, 0.01, 0.0),
        ("optimistic_hot_high_wet", "optimistic", 10.0, 0.01, 1000.0),
        ("optimistic_pressure_only_high", "optimistic", 0.0, 0.01, 0.0),
        ("conservative_heat_only", "conservative", 25.1, 0.0, 0.0),
        ("conservative_hot_low_dry", "conservative", 25.1, -0.02, 0.0),
        ("conservative_hot_low_wet", "conservative", 25.1, -0.02, 6000.0),
        ("conservative_pressure_only_low", "conservative", 0.0, -0.02, 0.0),
        ("conservative_hot_high_dry", "conservative", 25.1, 0.02, 0.0),
        ("conservative_hot_high_wet", "conservative", 25.1, 0.02, 6000.0),
        ("conservative_pressure_only_high", "conservative", 0.0, 0.02, 0.0),
    ]
    return [day_record(*row) for row in rows]


def envelope_days(days: list[dict], envelope: str) -> list[dict]:
    if envelope == "optimistic":
        return [d for d in days if d["group"] == "optimistic"]
    if envelope == "conservative":
        return [d for d in days if d["group"] == "conservative"]
    if envelope == "all_019":
        return list(days)
    raise KeyError(envelope)


def profile_state(day: dict, z: float, profile: str) -> tuple[float, float, float]:
    Td = day["T500_K"]
    pd = day["p500_Pa"]
    e = day["e500_Pa"]
    k = day["k"]
    if profile == "lapse_mixing":
        T = Td - LAPSE * (z - ZREF)
        n = G * k / (RD * LAPSE)
        p = pd * (T / Td) ** n
        rho = k * p / (RD * T)
        return T, p, rho
    if profile == "constant_e":
        T = Td - LAPSE * (z - ZREF)
        n_dry = G / (RD * LAPSE)
        p = 0.378 * e + (pd - 0.378 * e) * (T / Td) ** n_dry
        rho = (p - 0.378 * e) / (RD * T)
        return T, p, rho
    if profile == "isothermal":
        T = Td
        p = pd * math.exp(-k * G * (z - ZREF) / (RD * T))
        rho = k * p / (RD * T)
        return T, p, rho
    raise KeyError(profile)


def float_z(day: dict, mass: float, volume: float, profile: str) -> float:
    target = mass / volume
    if profile == "lapse_mixing":
        Td = day["T500_K"]
        k = day["k"]
        n = G * k / (RD * LAPSE)
        rho_d = k * day["p500_Pa"] / (RD * Td)
        t_float = Td * (target / rho_d) ** (1.0 / (n - 1.0))
        return ZREF + (Td - t_float) / LAPSE
    z_lo = -20000.0
    z_hi = 30000.0
    if profile != "isothermal":
        z_hi = min(z_hi, ZREF + day["T500_K"] / LAPSE - 1.0)
    rho_lo = profile_state(day, z_lo, profile)[2]
    rho_hi = profile_state(day, z_hi, profile)[2]
    if not (rho_lo >= target >= rho_hi):
        raise RuntimeError(f"float bracket {day['id']} {profile} {target} {rho_lo} {rho_hi}")
    for _ in range(80):
        mid = 0.5 * (z_lo + z_hi)
        if profile_state(day, mid, profile)[2] > target:
            z_lo = mid
        else:
            z_hi = mid
    return 0.5 * (z_lo + z_hi)


def ledger(days: list[dict], envelope: str, floor_m, profile: str,
           volume: float = V0) -> dict:
    chosen = envelope_days(days, envelope)
    lift = L0 * volume / V0
    if floor_m is None:
        absent = 0.0
    else:
        rho_min = min(profile_state(day, floor_m, profile)[2] for day in chosen)
        absent = max(0.0, lift - volume * rho_min)
    mass = lift - absent
    floats = []
    for day in chosen:
        z = float_z(day, mass, volume, profile)
        _t, p, _rho = profile_state(day, z, profile)
        floats.append((day["id"], z, p / P0))
    isa = next(day for day in build_days() if day["id"] == "ISA")
    z_isa = float_z(isa, mass, volume, profile)
    q = max(item[2] for item in floats)
    return {
        "C_kg": absent,
        "nominal_required_SF": max(1.0, q),
        "minimum_float_m": min(item[1] for item in floats),
        "ISA_float_m": z_isa,
        "peak_ratio": q,
        "governing_day": max(floats, key=lambda item: item[2])[0],
    }


def close_sandwich(fraction: float, panel_m: float, film_lb: float,
                   absent: float, rho_c: float) -> dict:
    mu = film_lb * LB_FT2
    m_film = 2.0 * A * mu
    alpha = (2.0 * B_SEAM * (1.0 - fraction) / panel_m
             + 2.0 * fraction * W_SPLICE * RHO_SPLICE / (panel_m * rho_c))
    beta = (2.0 * A / panel_m) * (2.0 * B_SEAM * T_ADH * RHO_ADH)
    room = L0 - absent - SYSTEMS - NONCLIM
    s_floor = room / 1.05
    seam_floor = alpha * s_floor + beta
    if seam_floor + m_film <= 0.05 * s_floor + 1e-9:
        structure = s_floor
        m_seam = seam_floor
        m_joint = 0.05 * structure
    else:
        structure = (room - beta - m_film) / (1.0 + alpha)
        m_seam = alpha * structure + beta
        m_joint = m_seam + m_film
    tf = (1.0 - fraction) * structure / (2.0 * A * RHO_F)
    tc = fraction * structure / (A * rho_c)
    excess = max(0.0, m_joint - 0.05 * structure)
    return {
        "S_kg": structure,
        "tf_m": tf,
        "tc_m": tc,
        "m_seam_kg": m_seam,
        "m_film_kg": m_film,
        "m_joint_kg": m_joint,
        "joint_excess_kg": excess,
        "reserve_kg": absent + NONCLIM + excess,
        "carried_kg": L0 - absent,
    }


def sandwich_modes(tf: float, tc: float, pressure: float, core: dict,
                   gamma: float, k_wrinkle: float, sigma: float,
                   modulus: float = E_FACE) -> dict:
    h = tf + tc
    stress = pressure * R / (4.0 * tf)
    sigma0 = modulus * h / (R * math.sqrt(1.0 - NU**2))
    sigma_crimp = h**2 * core["Gc_Pa"] / (2.0 * tf * tc)
    vc = sigma0 / sigma_crimp
    kc = (1.0 - vc / 4.0) if vc <= 2.0 else (1.0 / vc)
    return {
        "Vc": vc,
        "Kc": kc,
        "global": gamma * kc * sigma0 / stress,
        "face": sigma / stress,
        "crimp": sigma_crimp / stress,
        "crush": 2.0 * core["crush_Pa"] / pressure,
        "wrinkle": BX * k_wrinkle * math.sqrt(modulus * core["Ec_Pa"] * tf / tc) / stress,
        "dimple": (modulus / (1.0 - NU**2)) * (tf / core["s_cell_m"]) ** 2 / stress,
    }


def gamma_ends(vc: float) -> tuple[float, float]:
    today = 0.2 if vc < 2.0 else 1.0
    full = 0.2 + 0.4 * min(vc, 2.0)
    return today, full


def axis_value(today: float, full: float, usage: float) -> float:
    return today * (full / today) ** usage


def tube_rg(ro: float, wall: float) -> float:
    ri = ro - wall
    return math.sqrt((ro * ro + ri * ri) / 2.0)


def half_wave(ro: float, wall: float) -> float:
    return math.pi * math.sqrt(0.75 * tube_rg(ro, wall) * R)


def annulus(ro: float, wall: float) -> tuple[float, float]:
    ri = ro - wall
    area = math.pi * (ro**2 - ri**2)
    inertia = math.pi / 4.0 * (ro**4 - ri**4)
    return area, inertia


def frame_counts(side: float) -> tuple[float, float, float]:
    nodes = 8.0 * math.pi * R**2 / (math.sqrt(3.0) * side**2) + 2.0
    members = 3.0 * nodes - 6.0
    arc = 2.0 * R * math.asin(side / (2.0 * R))
    return nodes, members, arc


def frame_modes(side: float, ro: float, wall: float, t_film: float, pressure: float,
                sigma_film: float, modulus: float = SIC_E,
                sigma_tube: float = SIC_SIGMA) -> dict:
    area, inertia = annulus(ro, wall)
    _nodes, _members, arc = frame_counts(side)
    force = pressure * R * side / (2.0 * math.sqrt(3.0))
    gamma_local = 1.0 - 0.901 * (1.0 - math.exp(-math.sqrt(ro / wall) / 16.0))
    euler_stress = math.pi**2 * modulus * (inertia / area) / arc**2
    eta = (arc / 1000.0) * ro * area / inertia
    phi = (sigma_tube + (1.0 + eta) * euler_stress) / 2.0
    perry = phi - math.sqrt(max(0.0, phi**2 - sigma_tube * euler_stress))
    return {
        "yield": sigma_tube * area / force,
        "euler": math.pi**2 * modulus * inertia / (arc**2 * force),
        "local": 0.6 * modulus * (wall / ro) * gamma_local * area / force,
        "film": 2.0 * sigma_film * t_film / (side * pressure),
        "perry": perry * area / force,
        "global": 0.2 * 4.0 * math.sqrt(1.5) * modulus * math.sqrt(inertia * area)
        / (side * R**2 * pressure),
        "gamma_local": gamma_local,
        "area_m2": area,
        "I_m4": inertia,
        "arc_m": arc,
        "force_N": force,
    }


def check_printed(bag: list, row: str, field: str, mine: float, card: float, digits: int) -> None:
    if abs(mine - card) > 0.5 * 10.0 ** (-digits) + 1e-12:
        mismatch(bag, row, field, card, mine)


def main() -> None:
    started = now()
    bag: list[dict] = []
    days = build_days()
    atmosphere = json.loads((OWNER / "ATMOSPHERE.json").read_text())
    p2 = json.loads((OWNER / "P2.json").read_text())
    p3 = json.loads((OWNER / "P3.json").read_text())
    inputs = json.loads((OWNER / "INPUTS.json").read_text())
    cores = {row["name"]: row for row in inputs["cores"]}
    published_days = {row["id"]: row for row in atmosphere["days"]}
    for day in days:
        stored = published_days[day["id"]]
        for field, tol in (("T500_K", 1e-9), ("p500_Pa", 1e-6), ("k", 1e-12), ("e500_Pa", 1e-9)):
            if not near(day[field], stored[field], tol):
                mismatch(bag, day["id"], field, stored[field], day[field])

    for floor in atmosphere["floors"]:
        mine = ledger(days, floor["envelope"], floor["altitude_floor_m"], floor["profile"])
        label = f"{floor['envelope']}:{floor['profile']}:{floor['altitude_floor_m']}"
        # The floor file stores the raw peak pressure ratio. The card's nominal
        # factor is max(1, that ratio), which is the inherited p0 floor.
        if not near(mine["peak_ratio"], floor["nominal_required_SF"], 1e-9):
            mismatch(bag, label, "peak_pressure_ratio", floor["nominal_required_SF"], mine["peak_ratio"])
        for field, tol in (
            ("C_kg", 1e-6),
            ("minimum_float_m", 1e-6),
            ("ISA_float_m", 1e-6),
        ):
            if not near(mine[field], floor[field], tol):
                mismatch(bag, label, field, floor[field], mine[field])

    for row in atmosphere["full_gross_mass_days"]:
        if row["model"] != "lapse_mixing":
            continue
        day = next(item for item in days if item["id"] == row["day"])
        z = float_z(day, L0, V0, "lapse_mixing")
        _t, p, _rho = profile_state(day, z, "lapse_mixing")
        if not near(z, row["z_m"], 1e-6):
            mismatch(bag, "gross:" + row["day"], "z_m", row["z_m"], z)
        if not near(p / P0, row["p_over_p0"], 1e-12):
            mismatch(bag, "gross:" + row["day"], "p_over_p0", row["p_over_p0"], p / P0)

    heat = next(day for day in days if day["id"] == "optimistic_heat_only")
    z_heat = float_z(heat, L0, V0, "lapse_mixing")
    p_heat = profile_state(heat, z_heat, "lapse_mixing")[1] / P0
    descent = ZREF - z_heat
    check_printed(bag, "heat-only C=0", "float_m", z_heat, 130.743, 3)
    check_printed(bag, "heat-only C=0", "descent_m", descent, 369.257, 3)
    check_printed(bag, "heat-only C=0", "pressure_percent", (p_heat - 1.0) * 100.0, 4.352464, 6)

    opt100 = ledger(days, "optimistic", 100.0, "lapse_mixing")
    check_printed(bag, "optimistic 100 m", "C_kg", opt100["C_kg"], 55.341, 3)
    check_printed(bag, "optimistic 100 m", "nominal_SF", opt100["nominal_required_SF"], 1.036553, 6)
    check_printed(bag, "optimistic 100 m", "ISA_float_m", opt100["ISA_float_m"], 617.075, 3)
    opt500 = ledger(days, "optimistic", 500.0, "lapse_mixing")
    check_printed(bag, "optimistic 500 m", "nominal_SF", max(1.0, opt500["peak_ratio"]), 1.000000, 6)
    check_printed(bag, "optimistic 500 m", "anchor_ratio", opt500["peak_ratio"], 0.990000, 6)

    bound_diffs = []
    for search in p2["least_optimism_searches"]:
        label = f"{search['envelope']}:{search['altitude_floor_m']}"
        point = search["winner"]["point"]
        core = cores[point["core"]]
        closed = close_sandwich(
            point["core_mass_fraction"], point["parameters"]["panel"],
            point["parameters"]["film"], point["C_kg"], core["rho"],
        )
        comparisons = (
            ("tf_m", point["tf_m"], 1e-9),
            ("tc_m", point["tc_m"], 1e-9),
            ("m_joint_kg", point["masses_kg"]["joint"], 1e-4),
            ("reserve_kg", point["reserve_kg"], 1e-4),
        )
        for field, card, tol in comparisons:
            if not near(closed[field], card, tol):
                mismatch(bag, "least " + label, field, card, closed[field])
        modes = sandwich_modes(
            point["tf_m"], point["tc_m"], P0, core, point["metadata"]["gamma"],
            point["parameters"]["wrinkle"], point["parameters"]["sigma"],
        )
        for name in ("global", "face", "crimp", "crush", "wrinkle", "dimple"):
            if not near(modes[name], point["sfs_at_p0"][name], 1e-8):
                mismatch(bag, "least " + label, name, point["sfs_at_p0"][name], modes[name])
        q = point["required_nominal_SF"]
        needed_wrinkle = point["parameters"]["wrinkle"] * q / modes["wrinkle"]
        needed_gamma = point["metadata"]["gamma"] * q / modes["global"]
        if label == "optimistic:100.0":
            check_printed(bag, "optimistic 100 m", "needed_gamma", needed_gamma, 0.448157, 6)
            check_printed(bag, "optimistic 100 m", "needed_wrinkle", needed_wrinkle, 0.614995, 6)
            check_printed(bag, "optimistic 100 m", "reserve_kg", closed["reserve_kg"], 616.43, 2)
            check_printed(bag, "optimistic 100 m", "face_mm", point["tf_m"] * 1000.0, 0.717031, 6)
            check_printed(bag, "optimistic 100 m", "core_mm", point["tc_m"] * 1000.0, 31.815413, 6)
            check_printed(bag, "optimistic 100 m", "max_log_use", search["winner"]["min_max_log_usage"], 0.773511, 6)
            if search["winner"]["subset"] != ["gamma", "wrinkle", "panel"]:
                mismatch(bag, "optimistic 100 m", "subset", ["gamma", "wrinkle", "panel"], search["winner"]["subset"])
        if label == "all_019:100.0":
            check_printed(bag, "all_019 100 m", "C_kg", point["C_kg"], 441.770, 3)
            check_printed(bag, "all_019 100 m", "nominal_SF", q, 1.022889, 6)
            check_printed(bag, "all_019 100 m", "reserve_kg", closed["reserve_kg"], 967.96, 2)
            check_printed(bag, "all_019 100 m", "face_mm", point["tf_m"] * 1000.0, 0.649000, 6)
            check_printed(bag, "all_019 100 m", "core_mm", point["tc_m"] * 1000.0, 30.897147, 6)
        if label == "optimistic:500.0":
            check_printed(bag, "optimistic 500 m", "reserve_kg", closed["reserve_kg"], 775.56, 2)
        usage = search["winner"]["min_max_log_usage"]
        g_today, g_full = gamma_ends(modes["Vc"])
        g_used = axis_value(g_today, g_full, usage if "gamma" in search["winner"]["subset"] else 0.0)
        if not near(g_used, point["metadata"]["gamma"], 1e-8):
            mismatch(bag, "least " + label, "gamma", point["metadata"]["gamma"], g_used)
        for subset_row in search["tested_subsets"]:
            subset = set(subset_row["subset"])
            best = subset_row["full_bound_best"]
            if best is None:
                continue
            bound_core = cores[best["core"]]
            closed_bound = close_sandwich(
                best["fraction"],
                PANEL_FULL if "panel" in subset else PANEL_TODAY,
                FILM_FULL if "film" in subset else FILM_TODAY,
                search["C_kg"],
                bound_core["rho"],
            )
            probe = sandwich_modes(
                closed_bound["tf_m"], closed_bound["tc_m"], P0, bound_core,
                0.2, K_FULL if "wrinkle" in subset else K_TODAY,
                SIGMA_FULL if "strength" in subset else SIGMA_TODAY,
            )
            g_today_b, g_full_b = gamma_ends(probe["Vc"])
            gamma_b = g_full_b if "gamma" in subset else g_today_b
            scored = sandwich_modes(
                closed_bound["tf_m"], closed_bound["tc_m"], P0, bound_core,
                gamma_b, K_FULL if "wrinkle" in subset else K_TODAY,
                SIGMA_FULL if "strength" in subset else SIGMA_TODAY,
            )
            least = min(scored[name] for name in ("global", "face", "crimp", "crush", "wrinkle", "dimple"))
            q_req = ledger(days, search["envelope"], search["altitude_floor_m"], "lapse_mixing")[
                "nominal_required_SF"
            ]
            score = least / q_req
            diff = score - subset_row["full_bound_score"]
            bound_diffs.append(diff)
            if abs(diff) > 1e-6:
                mismatch(
                    bag, "bound " + label + ":" + "+".join(subset_row["subset"]),
                    "full_bound_score", subset_row["full_bound_score"], score,
                )

    filed_reserve = inputs["reference_021b"]["floating_point"]["masses_kg"]["reserve_total"]
    check_printed(bag, "filed 021b", "reserve_kg", filed_reserve, 775.73, 2)

    for row in p2["source_fixed"]:
        for day_row in row["days"]:
            if day_row["model"] != "lapse_mixing":
                continue
            if day_row["day"] not in (
                "ISA", "optimistic_heat_only", "optimistic_hot_low_wet", "conservative_hot_low_wet",
            ):
                continue
            day = next(item for item in days if item["id"] == day_row["day"])
            z = float_z(day, row["carried_mass_kg"], V0, "lapse_mixing")
            ratio = profile_state(day, z, "lapse_mixing")[1] / P0
            least = min(value / ratio for value in row["sfs_at_p0"].values())
            label = row["label"] + ":" + day_row["day"]
            if not near(z, day_row["z_m"], 1e-6):
                mismatch(bag, label, "z_m", day_row["z_m"], z)
            if not near(ratio, day_row["p_over_p0"], 1e-9):
                mismatch(bag, label, "p_over_p0", day_row["p_over_p0"], ratio)
            if not near(least, day_row["least_SF"], 1e-8):
                mismatch(bag, label, "least_SF", day_row["least_SF"], least)

    def score_p3(row: dict, film_sigma: float, film_rho: float, ti: bool,
                 absent: float, q_req: float) -> dict:
        side = row["spacing_m"]
        volume = V0 * (1.0 - side / (16.0 * R))
        lift = L0 * volume / V0
        sag = L0 - lift
        nodes, members, arc = frame_counts(side)
        m_nodes = nodes * NODE_MASS
        m_film = A * film_rho * row["film_m"]
        if ti:
            force = q_req * P0 * R * side / (2.0 * math.sqrt(3.0))
            m_joint = 2.0 * members * C_END_TI * force**2 / row["outer_radius_m"]
            carried_budget = lift - absent
            m_tube = carried_budget - SYSTEMS - NONCLIM - m_film - m_nodes - m_joint
        else:
            carried_budget = lift - absent
            m_tube = (carried_budget - SYSTEMS - NONCLIM) / 1.05 - m_film - m_nodes
            m_joint = 0.05 * (m_film + m_nodes + m_tube)
        modes = frame_modes(
            side, row["outer_radius_m"], row["wall_m"], row["film_m"], P0, film_sigma,
        )
        area_mass = m_tube / (members * arc * SIC_RHO)
        reserve = absent + NONCLIM + sag
        return {
            "C_kg": absent,
            "nominal_required_SF": q_req,
            "sag_kg": sag,
            "volume_m3": volume,
            "lift_kg": lift,
            "nodes": nodes,
            "members": members,
            "arc_m": arc,
            "m_film_kg": m_film,
            "m_nodes_kg": m_nodes,
            "m_joint_kg": m_joint,
            "m_tube_kg": m_tube,
            "area_from_mass_m2": area_mass,
            "reserve_kg": reserve,
            "modes": modes,
        }

    p3_rows = [("reopt", row, False, FILM_SIGMA, FILM_RHO) for row in p3["reoptimised"]]
    p3_rows.append(("source", p3["source_reproduction"], False, FILM_SIGMA, FILM_RHO))
    for row in p3["sensitivities"]:
        p3_rows.append(("ti", row, True, KAPTON_SIGMA, KAPTON_RHO))

    half_rows = []
    for kind, row, ti, film_sigma, film_rho in p3_rows:
        side = row["spacing_m"]
        volume = V0 * (1.0 - side / (16.0 * R))
        if "altitude_floor_m" in row:
            weather = ledger(days, row["envelope"], row["altitude_floor_m"], "lapse_mixing", volume)
            absent = weather["C_kg"]
            q_req = weather["nominal_required_SF"]
        else:
            absent = row["C_kg"]
            q_req = row["nominal_required_SF"]
        mine = score_p3(row, film_sigma, film_rho, ti, absent, q_req)
        floor_name = row["altitude_floor_m"] if "altitude_floor_m" in row else "held-022b"
        label = f"P3 {kind} {row['envelope']}:{floor_name}"
        for field, tol in (
            ("C_kg", 1e-6),
            ("nominal_required_SF", 1e-9),
            ("sag_kg", 1e-6),
            ("volume_m3", 1e-6),
            ("nodes", 1e-8),
            ("m_film_kg", 1e-4),
            ("m_nodes_kg", 1e-6),
            ("m_joint_kg", 1e-4),
            ("m_tube_kg", 1e-4),
            ("reserve_kg", 1e-4),
        ):
            card = {
                "C_kg": row["C_kg"],
                "nominal_required_SF": row["nominal_required_SF"],
                "sag_kg": row["sag_lost_lift_at_ISA_kg"],
                "volume_m3": row["effective_volume_m3"],
                "nodes": row["nodes"],
                "m_film_kg": row["masses_kg"]["m_film"],
                "m_nodes_kg": row["masses_kg"]["m_nodes"],
                "m_joint_kg": row["masses_kg"]["m_joint"],
                "m_tube_kg": row["masses_kg"]["m_tube"],
                "reserve_kg": row["reserve_kg"],
            }[field]
            if not near(mine[field], card, tol):
                mismatch(bag, label, field, card, mine[field])
        if not near(mine["area_from_mass_m2"], mine["modes"]["area_m2"], 1e-8):
            mismatch(bag, label, "section_area_m2", row["section_area_m2"], mine["area_from_mass_m2"])
        if not near(mine["modes"]["area_m2"], row["section_area_m2"], 1e-10):
            mismatch(bag, label, "annulus_area_m2", row["section_area_m2"], mine["modes"]["area_m2"])
        for name in ("yield", "euler", "local", "film", "perry", "global"):
            if not near(mine["modes"][name], row["sfs_at_p0"][name], 1e-8):
                mismatch(bag, label, name, row["sfs_at_p0"][name], mine["modes"][name])
        ratio = half_wave(row["outer_radius_m"], row["wall_m"]) / row["spacing_m"]
        half_rows.append({
            "row": label,
            "s_m": row["spacing_m"],
            "r_o_m": row["outer_radius_m"],
            "wall_m": row["wall_m"],
            "half_wave_m": half_wave(row["outer_radius_m"], row["wall_m"]),
            "half_wave_over_s": ratio,
            "outside_band": ratio < 1.0 or row["spacing_m"] > 3.0,
            "least_SF": row["least_SF"],
        })

    opt_p3 = next(
        row for row in p3["reoptimised"]
        if row["envelope"] == "optimistic" and row["altitude_floor_m"] == 100.0
    )
    both_p3 = next(
        row for row in p3["reoptimised"]
        if row["envelope"] == "all_019" and row["altitude_floor_m"] == 100.0
    )
    check_printed(bag, "P3 optimistic 100 m", "C_kg", opt_p3["C_kg"], 53.197, 3)
    check_printed(bag, "P3 optimistic 100 m", "least_SF", opt_p3["least_SF"], 1.343321, 6)
    check_printed(bag, "P3 optimistic 100 m", "s_m", opt_p3["spacing_m"], 6.19898, 5)
    check_printed(bag, "P3 optimistic 100 m", "ro_mm", opt_p3["outer_radius_m"] * 1000.0, 168.729, 3)
    check_printed(bag, "P3 optimistic 100 m", "wall_mm", opt_p3["wall_m"] * 1000.0, 1.63746, 5)
    check_printed(bag, "P3 optimistic 100 m", "film_mm", opt_p3["film_m"] * 1000.0, 0.27466, 5)
    check_printed(bag, "P3 optimistic 100 m", "reserve_kg", opt_p3["reserve_kg"], 422.190, 3)
    check_printed(bag, "P3 all_019 100 m", "C_kg", both_p3["C_kg"], 424.936, 3)
    check_printed(bag, "P3 all_019 100 m", "least_SF", both_p3["least_SF"], 1.208051, 6)
    check_printed(bag, "P3 all_019 100 m", "reserve_kg", both_p3["reserve_kg"], 790.812, 3)
    check_printed(
        bag, "022b source sag", "sag_kg",
        p3["source_reproduction"]["sag_lost_lift_at_ISA_kg"], 187.937933, 6,
    )

    continuum = json.loads(CONTINUUM.read_text())
    continuum_checks = []
    for point_name in ("022b carried, 5%, gamma", "022b carried, 019 reserve, gamma"):
        stored = next(row for row in continuum if row["point"] == point_name)
        wave = half_wave(stored["r_o_m"], stored["wall_m"])
        ratio = wave / stored["s_m"]
        continuum_checks.append({
            "point": point_name,
            "stored_ratio": stored["half_wave_over_s"],
            "mine_ratio": ratio,
            "stored_wave_m": stored["buckle_half_wave_m"],
            "mine_wave_m": wave,
        })
        if not near(ratio, stored["half_wave_over_s"], 1e-9):
            mismatch(bag, point_name, "half_wave_over_s", stored["half_wave_over_s"], ratio)

    opt_ratio = next(row["half_wave_over_s"] for row in half_rows if row["row"].endswith("optimistic:100.0") and row["row"].startswith("P3 reopt"))
    source_ratio = next(row["half_wave_over_s"] for row in half_rows if row["row"].startswith("P3 source"))
    ti_ratios = [row["half_wave_over_s"] for row in half_rows if row["row"].startswith("P3 ti")]
    reopt_outside = all(row["outside_band"] for row in half_rows if row["row"].startswith("P3 reopt"))

    nfi = [
        {
            "id": "NFI-CHECK-031-HALF-WAVE",
            "status": "open",
            "issue": (
                "030's half-wave is pi*sqrt((3/4)*rg*R), rg=sqrt((ro^2+ri^2)/2), "
                "divided by bay side. Below 1, or a bay longer than 3 m, is outside "
                "the smeared band. The 019-reserve 022b point is s 6.15 m at ratio "
                f"{source_ratio:.6f}. Every reoptimised SiC row is outside that band. "
                "The optimistic 100 m row is ratio "
                f"{opt_ratio:.6f}. The least factor on those rows is global."
            ),
            "effect": (
                "The passing P3 factors use a global formula the register says does "
                "not describe these bays. The Ti/Kapton rows are inside the band and "
                "remain below 1. This objection does not change the printed arithmetic."
            ),
        },
        {
            "id": "NFI-CHECK-031-PASS-CONDITIONS",
            "status": "open",
            "issue": (
                "The P3 pass uses 3900 MPa, a typical property, and a 1.5 GPa film. "
                "The lapse with constant vapour fraction is a projection. The C=0 "
                "roots at -23.190 m and -1015.877 m are below sea-level ground."
            ),
            "effect": "The card already tags these. They stay open.",
        },
    ]

    headline = {
        "heat_only_float_m": z_heat,
        "heat_only_descent_m": descent,
        "heat_only_pressure_ratio": p_heat,
        "optimistic_100_C_kg": opt100["C_kg"],
        "optimistic_100_SF": opt100["nominal_required_SF"],
        "optimistic_100_reserve_kg": next(
            search["winner"]["point"]["reserve_kg"]
            for search in p2["least_optimism_searches"]
            if search["envelope"] == "optimistic" and search["altitude_floor_m"] == 100.0
        ),
        "filed_021b_reserve_kg": filed_reserve,
        "optimistic_500_reserve_kg": next(
            search["winner"]["point"]["reserve_kg"]
            for search in p2["least_optimism_searches"]
            if search["envelope"] == "optimistic" and search["altitude_floor_m"] == 500.0
        ),
        "p3_optimistic_100_half_wave_over_s": opt_ratio,
        "p3_source_half_wave_over_s": source_ratio,
        "p3_ti_half_wave_over_s": ti_ratios,
        "p3_reopt_all_outside_band": reopt_outside,
        "bound_max_abs_diff": max(abs(item) for item in bound_diffs) if bound_diffs else None,
        "bound_count": len(bound_diffs),
        "bx": BX,
        "mismatches": len(bag),
    }

    card = "\n".join([
        "# CHECK MAINLINE-031",
        "",
        "QUESTIONABLE. Not a certification. The owner's card is not rewritten.",
        "Owner scripts were not executed.",
        "",
        (
            f"Heat-only descent {descent:.12g} m, pressure ratio {p_heat:.12g}. "
            f"Optimistic 100 m headroom {opt100['C_kg']:.12g} kg, "
            f"nominal factor {opt100['nominal_required_SF']:.12g}, "
            f"reserve {headline['optimistic_100_reserve_kg']:.12g} kg "
            f"against filed 021b {filed_reserve:.12g} kg."
        ),
        (
            f"P3 optimistic 100 m half-wave over s is {opt_ratio:.12g}. "
            f"The 022b 019-reserve source ratio is {source_ratio:.12g}. "
            "Both are outside 030's smeared band. Mismatches: "
            f"{len(bag)}."
        ),
        "",
    ])
    ended = now()
    results = {
        "unit": "vacuum-mainline031-check-1020",
        "status": "QUESTIONABLE",
        "certification": "none",
        "mismatches": bag,
        "headline": headline,
        "half_wave_rows": half_rows,
        "continuum_reference": continuum_checks,
        "started_at": started,
        "ended_at": ended,
    }
    read_only = [
        pin(BRIEFS / "CHECK.md"),
        pin(BRIEFS / "COMMON.md"),
        pin(OWNER / "CARD.md"),
        pin(OWNER / "METHOD.md"),
        pin(OWNER / "ATMOSPHERE.json"),
        pin(OWNER / "P2.json"),
        pin(OWNER / "P3.json"),
        pin(CONTINUUM),
    ]
    (ROOT / "CHECK-CARD.md").write_text(card, encoding="utf-8")
    (ROOT / "CHECK-RESULTS.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    (ROOT / "CHECK-NFI.json").write_text(json.dumps({"rows": nfi}, indent=1) + "\n", encoding="utf-8")
    (ROOT / "CHECK-INPUTS.json").write_text(json.dumps({
        "read_only": read_only,
        "started_at": started,
        "ended_at": ended,
        "owner_scripts_executed": False,
    }, indent=1) + "\n", encoding="utf-8")
    print("MISMATCHES", len(bag))
    for item in bag[:30]:
        print(item["row"], item["field"], "card", item["card"], "mine", item["mine"])
    print("HEAT", f"{z_heat:.12g}", f"{descent:.12g}", f"{p_heat:.12g}")
    print("OPT100", f"{opt100['C_kg']:.12g}", f"{opt100['nominal_required_SF']:.12g}",
          f"{headline['optimistic_100_reserve_kg']:.12g}")
    print("RES500", f"{headline['optimistic_500_reserve_kg']:.12g}", "FILED", f"{filed_reserve:.12g}")
    print("HALF", f"{opt_ratio:.12g}", "SOURCE", f"{source_ratio:.12g}", "TI", ti_ratios)
    print("BOUND", headline["bound_count"], headline["bound_max_abs_diff"])
    print("OUTSIDE", reopt_outside)
    print("DONE", ended)


if __name__ == "__main__":
    main()
