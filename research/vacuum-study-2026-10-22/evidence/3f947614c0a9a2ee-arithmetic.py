#!/usr/bin/python3
"""MAINLINE-002 strength rows. Reads sealed MAINLINE-001 JSON. Does not execute or edit it."""
from __future__ import annotations

import json
import math
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SEALED = Path("unpublished-local-ref:827c7db7d9847d66")
ORIGIN = 2081065.254948193
PHASE1_ELAPSED = 177.37589207896963
SIGMA = 276_000_000.0


def now():
    return datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="microseconds"), time.monotonic()


def get(rows, iid, point):
    for row in rows:
        if row["input_id"] == iid and row["point_id_or_common"] == point:
            return row["value"]
    raise SystemExit(f"missing {iid} {point}")


def zoelly(E, t, R, nu):
    return 2.0 * E * (t / R) ** 2 / math.sqrt(3.0 * (1.0 - nu**2))


def sandwich(E, tf, d, R, nu):
    return 4.0 * E * tf * d / (R**2 * math.sqrt(1.0 - nu**2))


def main():
    inputs = json.loads((SEALED / "INPUTS.json").read_text())
    points = json.loads((SEALED / "POINTS.json").read_text())
    sealed = {p["point_id"]: p for p in points}
    E = get(inputs, "I-E", "common")
    rho_al = get(inputs, "I-RHO-AL", "common")
    nu = get(inputs, "I-NU", "common")
    R = get(inputs, "I-R", "common")
    h = get(inputs, "I-H", "common")
    T0 = get(inputs, "I-T0", "common")
    p0 = get(inputs, "I-P0", "common")
    lapse = get(inputs, "I-LAPSE", "common")
    g0 = get(inputs, "I-G", "common")
    Rspec = get(inputs, "I-RSPEC", "common")
    T = T0 - lapse * h
    p_ext = p0 * (T / T0) ** (g0 / (lapse * Rspec))
    rho = p_ext / (Rspec * T)
    V = (4.0 / 3.0) * math.pi * R**3
    area = 4.0 * math.pi * R**2
    lift = rho * V
    if abs(p_ext - sealed["P1"]["external_pressure_at_500m_Pa"]) / p_ext > 1e-12:
        raise SystemExit("pressure drift")

    kd1 = get(inputs, "I-KD", "P1")
    kd2 = get(inputs, "I-KD", "P2")
    t1 = get(inputs, "I-T1", "P1")
    j1 = get(inputs, "I-J1", "P1")
    sys1 = get(inputs, "I-SYS1", "P1")
    gas1 = get(inputs, "I-GAS1", "P1")
    tf = get(inputs, "I-TF", "P2")
    core = get(inputs, "I-CORE-T", "P2")
    rho_c = get(inputs, "I-RHO-CORE", "P2")
    j2 = get(inputs, "I-J2", "P2")
    sys2 = get(inputs, "I-SYS2", "P2")
    gas2 = get(inputs, "I-GAS2", "P2")
    s = get(inputs, "I-S", "P3")
    ro = get(inputs, "I-RO", "P3")
    tw = get(inputs, "I-TW", "P3")
    sig_f = get(inputs, "I-SIG", "P3")
    t_film = get(inputs, "I-TFILM", "P3")
    rho_f = get(inputs, "I-RHO-FILM", "P3")
    node = get(inputs, "I-NODE", "P3")
    sys3 = get(inputs, "I-SYS3", "P3")
    gas3 = get(inputs, "I-GAS3", "P3")

    def factors(limits):
        out = {}
        for name, pressure, prop, scaling, holds in limits:
            factor = p_ext / pressure
            out[name] = {
                "pressure_Pa": pressure,
                "property": prop,
                "factor": factor,
                "factor_above_one": factor > 1.0,
                "scaling": scaling,
                "held_fixed": holds,
                "baseline_value": E if "Young" in prop or prop.startswith("E") else (SIGMA if "aluminum" in prop else sig_f),
            }
        return out

    def pack(pid, family, kind, geom, masses, limits, extra):
        total = sum(masses.values())
        margin = (lift - total) / lift
        pressures = {name: p for name, p, *_ in limits}
        governing = min(pressures, key=pressures.get)
        p_col = pressures[governing]
        sf = p_col / p_ext
        fac = factors(limits)
        stiff = [n for n, *_ in limits if n in ("knocked_down_buckling", "pinned_euler")][0]
        ceiling = p_ext
        for name, pressure in pressures.items():
            if name != stiff:
                ceiling = min(ceiling, pressure)
        return {
            "point_id": pid,
            "construction_family": family,
            "row_kind": kind,
            "geometry": geom,
            "masses_kg": masses,
            "all_mass_kg": total,
            "lift_equivalent_mass_kg": lift,
            "float_margin": margin,
            "limits_Pa": pressures,
            "governing_limit": governing,
            "collapse_pressure_Pa": p_col,
            "external_pressure_Pa": p_ext,
            "crush_safety_factor": sf,
            "factors": fac,
            "stiffness_only_ceiling_SF": ceiling / p_ext,
            "extra": extra,
        }

    def shell_masses(t):
        shell = rho_al * area * t
        joints = j1 * shell
        return {"shell": shell, "joints": joints, "systems_payload": sys1, "residual_gas": gas1}

    def sand_masses(face):
        faces = rho_al * area * 2.0 * face
        core_m = rho_c * area * core
        sand = faces + core_m
        return {"faces": faces, "core": core_m, "joints": j2 * sand, "systems_payload": sys2, "residual_gas": gas2}

    tri = math.sqrt(3.0) / 4.0 * s * s
    n_tri = area / tri
    n_edge = 1.5 * n_tri
    n_node = n_edge - n_tri + 2.0
    if abs(n_node - n_edge + n_tri - 2.0) > 1e-9:
        raise SystemExit("mesh")
    m_film = rho_f * area * t_film
    m_nodes = n_node * node

    def tube(wall):
        ri = ro - wall
        A = math.pi * (ro**2 - ri**2)
        I = math.pi / 4.0 * (ro**4 - ri**4)
        return A, I

    def frame_masses(wall):
        A, _I = tube(wall)
        return {
            "frame": n_edge * rho_al * A * s,
            "film": m_film,
            "nodes": m_nodes,
            "systems_payload": sys3,
            "residual_gas": gas3,
        }

    def row_shell(pid, kind, t):
        p_s = kd1 * zoelly(E, t, R, nu)
        p_y = 2.0 * SIGMA * t / R
        limits = [
            ("knocked_down_buckling", p_s, "Young_modulus_of_6061-T6", "p_stiff = kd*2*(t/R)^2/sqrt(3*(1-nu^2))*E", "t, R, nu, kd, sigma, masses"),
            ("aluminum_yield", p_y, "transferred_aluminum_tensile_yield", "p_yield = 2*sigma*t/R", "t, R, E, kd"),
        ]
        return pack(pid, "simple_shell", kind, f"sphere R={R} m, t={t} m, p_int=0", shell_masses(t), limits, {"t_m": t})

    def row_sand(pid, kind, face):
        d = core + face
        p_s = kd2 * sandwich(E, face, d, R, nu)
        p_y = 4.0 * SIGMA * face / R
        limits = [
            ("knocked_down_buckling", p_s, "Young_modulus_of_6061-T6_faces", "p_stiff = kd*4*tf*d/(R^2*sqrt(1-nu^2))*E", "tf, d, R, nu, kd, sigma; shear omitted"),
            ("aluminum_yield", p_y, "transferred_aluminum_tensile_yield", "p_yield = 4*sigma*tf/R", "tf, R, E, kd, core"),
        ]
        return pack(pid, "sandwich", kind, f"sphere R={R} m, tf={face} m, core={core} m, p_int=0", sand_masses(face), limits, {"tf_m": face, "d_m": d})

    def row_frame(pid, kind, wall):
        A, I = tube(wall)
        p_e = 2.0 * math.pi**2 * E * I / (R * s**3)
        p_y = 2.0 * SIGMA * A / (R * s)
        p_film = 2.0 * sig_f * t_film / s
        limits = [
            ("pinned_euler", p_e, "Young_modulus_of_6061-T6_frame", "p_euler = 2*pi^2*E*I/(R*s^3)", "I, R, s, A, film, sigma"),
            ("aluminum_yield", p_y, "transferred_aluminum_tensile_yield", "p_yield = 2*sigma*A/(R*s)", "A, R, s, E, I"),
            ("film_membrane", p_film, "film_tensile_allowable", "p_film = 2*sigma_film*t_film/s", "t_film, s; not an aluminum yield"),
        ]
        return pack(
            pid, "frame_membrane", kind,
            f"sphere R={R} m, s={s} m, ro={ro} m, tw={wall} m, film={t_film} m, p_int=0",
            frame_masses(wall), limits,
            {"tw_m": wall, "area_m2": A, "I_m4": I, "n_edges": n_edge},
        )

    rows = [row_shell("P1", "baseline", t1), row_sand("P2", "baseline", tf), row_frame("P3", "baseline", tw)]
    for row, pid in zip(rows, ("P1", "P2", "P3")):
        if abs(row["limits_Pa"]["knocked_down_buckling" if pid != "P3" else "pinned_euler"] - sealed[pid]["collapse_pressure_estimate_Pa"]) / p_ext > 1e-9:
            raise SystemExit(f"stiffness drift {pid}")
        if abs(row["crush_safety_factor"] - min(row["limits_Pa"].values()) / p_ext) > 1e-15:
            raise SystemExit("sf")
        # Baseline stiffness-only SF must match the admitted card, before the new yield minimum.
        stiff_sf = row["limits_Pa"]["pinned_euler" if pid == "P3" else "knocked_down_buckling"] / p_ext
        if abs(stiff_sf - sealed[pid]["crush_safety_factor"]) / max(stiff_sf, 1e-30) > 1e-9:
            raise SystemExit(f"admitted SF drift {pid} {stiff_sf} {sealed[pid]['crush_safety_factor']}")

    # One allocation each. Solve the named thickness so mass equals lift.
    t_alt = (lift - sys1 - gas1) / ((1.0 + j1) * rho_al * area)
    face_budget = (lift - sys2 - gas2) / (1.0 + j2) - rho_c * area * core
    tf_alt = face_budget / (2.0 * rho_al * area)
    A_target = (lift - m_film - m_nodes - sys3 - gas3) / (n_edge * rho_al * s)
    disc = ro**2 - A_target / math.pi
    if t_alt <= t1 or tf_alt <= tf or disc <= 0.0:
        raise SystemExit(f"allocation not inside the wall {t_alt} {tf_alt} {disc}")
    tw_alt = ro - math.sqrt(disc)
    alts = [row_shell("P1-A", "float_margin_allocation", t_alt), row_sand("P2-A", "float_margin_allocation", tf_alt), row_frame("P3-A", "float_margin_allocation", tw_alt)]
    for row in alts:
        if abs(row["float_margin"]) > 1e-9:
            raise SystemExit(f"residual margin {row['point_id']} {row['float_margin']}")
    rows.extend(alts)

    nfis = [
        {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "276 MPa is the retrieved AA typical tensile yield. It is transferred to compression by owner assumption. The sheet says AA typical values are not for design. No compressive yield was in the retrieved snippet.", "direction": "Obtain a compression yield or design allowable and drop the transfer.", "effect": "Aluminum-strength pressure and its factor scale linearly with this value."},
        {"NFI_id": "NFI-FLOAT-ALLOCATION-CARRY", "gap": "Each alternative spends the baseline margin on one thickness. Residual margin is numerical zero by that rule. It is not an optimum and not a search over families.", "direction": "A later card can compare other single changes, including core thickness and tube radius.", "effect": "The allocation changes both stiffness and strength pressures through the named thickness."},
        {"NFI_id": "NFI-SAND", "gap": "Sandwich buckling still extrapolates the monocoque identity and omits core shear, wrinkling and core crush.", "direction": "Replace with a published sandwich formula that includes shear.", "effect": "Shear would lower the stiffness pressure. The omission is optimistic for that limit."},
        {"NFI_id": "NFI-KD", "gap": "Knockdown remains 0.2, the cited severe typical value, not a curve at this R/t.", "direction": "Evaluate NASA SP-8032 for these complete spheres.", "effect": "Stiffness pressure of P1 and P2 scales directly with the knockdown."},
        {"NFI_id": "NFI-FRAME", "gap": "Pinned Euler, tributary width equal to spacing, and no local crippling.", "direction": "Integer mesh, end fixity and crippling.", "effect": "Euler pressure scales with I. Section yield scales with area. Crippling could govern first."},
        {"NFI_id": "NFI-FILM", "gap": "Film allowable stays the owner value from MAINLINE-001 and is not aluminum yield.", "direction": "Pin one film datasheet.", "effect": "Film pressure is reported separately and can govern if it is the least."},
        {"NFI_id": "NFI-GEOM", "gap": "External volume still ignores wall intrusion.", "direction": "Inner and outer mould lines.", "effect": "Volume error moves lift and the allocation thicknesses."},
        {"NFI_id": "NFI-MASS", "gap": "Joint fractions, node mass and payload allowances are unchanged owner numbers.", "direction": "Replace with a parts list.", "effect": "They set how much margin the allocation can spend."},
    ]

    utc, mono = now()
    elapsed = mono - ORIGIN
    dur2 = elapsed - PHASE1_ELAPSED
    phase2 = {
        "schema": 1, "phase": 2,
        "name": "current_geometry_strength_rows_and_one_float_allocation_alternative_per_family",
        "end_utc": utc, "end_monotonic_s": mono, "end_elapsed_s": elapsed,
        "duration_s": dur2, "actual_max_s": 500, "cumulative_max_s": 800,
        "status": "INSIDE" if dur2 <= 500 and elapsed <= 800 else "OVER",
    }
    if phase2["status"] != "INSIDE":
        raise SystemExit(phase2)
    out = {
        "schema": 1,
        "status": "ESTIMATE_PENDING_UNA",
        "card": "MAINLINE-002",
        "atmosphere": {"T_K": T, "p_ext_Pa": p_ext, "rho_kg_m3": rho, "volume_m3": V, "lift_kg": lift},
        "sigma_Pa": SIGMA,
        "sigma_transfer": "TRANSFERRED_FROM_TENSILE_YIELD",
        "rows": rows,
        "NFI": nfis,
        "checks": {"admitted_stiffness_match": "PASS", "allocation_residual_near_zero": "PASS"},
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n")
    (ROOT / "PHASE2.json").write_text(json.dumps(phase2, indent=1) + "\n")
    (ROOT / "NFI.json").write_text(json.dumps(nfis, indent=1) + "\n")

    def g(x):
        return format(x, ".12g")

    lines = [
        "# MAINLINE-002 strength card — ESTIMATE_PENDING_UNA",
        "",
        "Unit vacuum-mainline002-strength-owner1200-1019. This estimate is pending its own Una admission. It does not add a map point. MAINLINE-001 stays the admitted map point at 2026-10-19T19:47:15.465741-07:00. Its artifacts were read and not edited.",
        "",
        f"Case: evacuated spheres, external radius 10 m, 500 m ISA air. Pressure {g(p_ext)} Pa. Density {g(rho)} kg/m3. Lift mass {g(lift)} kg. Internal pressure 0.",
        "",
        "Aluminum strength uses 276 MPa, the AA typical tensile yield on the ASM MatWeb 6061-T6 sheet. That sheet says AA typical values are not for design. No compressive yield was retrieved, so the value is transferred to compression by owner assumption. Film allowable is a separate limit.",
        "",
        "Collapse pressure for a row is the least of the stated limits. Stiffness and strength factors are separate multipliers on their own properties. A factor above one is the multiplier that brings that limit up to the external pressure with the other limits held fixed. It is not an all-mode promise.",
        "",
    ]
    for row in rows:
        lines.append(f"## {row['point_id']} — {row['construction_family']} — {row['row_kind']}")
        lines.append("")
        lines.append(row["geometry"])
        lines.append("")
        lines.append("Masses in kilograms: " + ", ".join(f"{k} {g(v)}" for k, v in row["masses_kg"].items()) + f". Total {g(row['all_mass_kg'])}. Float margin {g(row['float_margin'])}.")
        lines.append("")
        bits = ", ".join(f"{k} {g(v)} Pa" for k, v in row["limits_Pa"].items())
        lines.append(f"Limits: {bits}. Governing {row['governing_limit']}. Collapse {g(row['collapse_pressure_Pa'])} Pa. Crush safety factor {g(row['crush_safety_factor'])}.")
        lines.append("")
        for name, fac in row["factors"].items():
            lines.append(f"{name}: property {fac['property']}, factor {g(fac['factor'])}. Held fixed: {fac['held_fixed']}. Scaling: {fac['scaling']}.")
        lines.append("")
        lines.append(f"If only stiffness is raised to the external pressure, the remaining modeled safety factor is {g(row['stiffness_only_ceiling_SF'])}.")
        lines.append("")
    lines.append("Alternatives P1-A, P2-A and P3-A each spend the baseline float margin on one thickness. Residual margin is numerical zero by that rule. They are not an optimum.")
    lines.append("")
    lines.append("Safety factors below one, and factors above one, are directions. Needs-further-investigation rows are in NFI.json. Core shear, knockdown curve, crippling and compression-yield measurement remain open.")
    (ROOT / "CARD.md").write_text("\n".join(lines) + "\n")
    utc3, mono3 = now()
    elapsed3 = mono3 - ORIGIN
    dur3 = elapsed3 - elapsed
    phase3 = {
        "schema": 1, "phase": 3,
        "name": "stiffness_strength_factors_limits_and_NFI",
        "end_utc": utc3, "end_monotonic_s": mono3, "end_elapsed_s": elapsed3,
        "duration_s": dur3, "actual_max_s": 200, "cumulative_max_s": 1000,
        "status": "INSIDE" if dur3 <= 200 and elapsed3 <= 1000 else "OVER",
    }
    if phase3["status"] != "INSIDE":
        raise SystemExit(phase3)
    (ROOT / "PHASE3.json").write_text(json.dumps(phase3, indent=1) + "\n")
    summary = []
    for row in rows:
        summary.append({
            "id": row["point_id"],
            "margin": row["float_margin"],
            "sf": row["crush_safety_factor"],
            "governing": row["governing_limit"],
            "factors": {k: v["factor"] for k, v in row["factors"].items()},
            "ceiling": row["stiffness_only_ceiling_SF"],
        })
    print(json.dumps({"elapsed2": elapsed, "elapsed3": elapsed3, "rows": summary}, indent=1))


if __name__ == "__main__":
    main()
