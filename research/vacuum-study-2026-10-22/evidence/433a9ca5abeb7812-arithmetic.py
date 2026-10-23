#!/usr/bin/python3
"""MAINLINE-003 three P2 allocations. Reads sealed JSON. Does not execute predecessor or advisory scripts."""
from __future__ import annotations

import json
import math
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SEALED = Path("unpublished-local-ref:827c7db7d9847d66")
PRIOR = Path("unpublished-local-ref:53da98db762d6c66")
ORIGIN = 2085091.743109635
SIGMA = 276_000_000.0


def now():
    return datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="microseconds"), time.monotonic()


def get(rows, iid, point):
    for row in rows:
        if row["input_id"] == iid and row["point_id_or_common"] == point:
            return row["value"]
    raise SystemExit(f"missing {iid} {point}")


def g(x):
    return format(x, ".12g")


def main():
    origin = json.loads((ROOT / "ORIGIN.json").read_text())
    if origin["origin_monotonic_s"] != ORIGIN:
        raise SystemExit("origin moved")
    phase1 = json.loads((ROOT / "PHASE1.json").read_text())
    if phase1["status"] != "INSIDE":
        raise SystemExit("phase1 not inside")
    p1_elapsed = phase1["elapsed_s"]
    inputs = json.loads((SEALED / "INPUTS.json").read_text())
    prior = json.loads((PRIOR / "RESULTS.json").read_text())
    sealed_a = next(r for r in prior["rows"] if r["point_id"] == "P2-A")

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
    kd = get(inputs, "I-KD", "P2")
    tf0 = get(inputs, "I-TF", "P2")
    core0 = get(inputs, "I-CORE-T", "P2")
    rho_c = get(inputs, "I-RHO-CORE", "P2")
    j2 = get(inputs, "I-J2", "P2")
    sys2 = get(inputs, "I-SYS2", "P2")
    gas2 = get(inputs, "I-GAS2", "P2")
    denom = R**2 * math.sqrt(1.0 - nu**2)
    budget = (lift - sys2 - gas2) / (1.0 + j2)

    def pressures(tf, core):
        d = core + tf
        p_s = kd * 4.0 * E * tf * d / denom
        p_y = 4.0 * SIGMA * tf / R
        return d, p_s, p_y

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    tf_a = (budget - rho_c * area * core0) / (2.0 * rho_al * area)
    d_a, p_s_a, p_y_a = pressures(tf_a, core0)
    if abs(tf_a - sealed_a["extra"]["tf_m"]) / tf_a > 1e-9:
        raise SystemExit(f"P2-A thickness drift {tf_a} {sealed_a['extra']['tf_m']}")
    if abs((p_s_a / p_ext) - sealed_a["crush_safety_factor"]) / sealed_a["crush_safety_factor"] > 1e-9:
        raise SystemExit("P2-A stiffness SF drift")
    if abs((p_ext / p_y_a) - sealed_a["factors"]["aluminum_yield"]["factor"]) / sealed_a["factors"]["aluminum_yield"]["factor"] > 1e-9:
        raise SystemExit("P2-A strength factor drift")

    faces0 = rho_al * area * 2.0 * tf0
    if budget <= faces0:
        raise SystemExit("no core budget")
    core_c = (budget - faces0) / (rho_c * area)
    sand0 = faces0 + rho_c * area * core0
    k = budget / sand0
    tf_k = k * tf0
    core_k = k * core0
    tf_e = (budget / 2.0) / (2.0 * rho_al * area)
    core_e = (budget / 2.0) / (rho_c * area)
    if min(core_c, tf_k, core_k, tf_e, core_e) <= 0.0:
        raise SystemExit("nonpositive geometry")
    specs = [
        ("P2-C", "core_thickness_takes_the_ceiling_faces_fixed", tf0, core_c),
        ("P2-K", "one_factor_scales_baseline_face_and_core", tf_k, core_k),
        ("P2-E", "equal_face_mass_and_core_mass", tf_e, core_e),
    ]
    rows = [row(*spec) for spec in specs]
    for item in rows:
        if abs(item["float_margin"]) > 1e-9:
            raise SystemExit(f"margin {item['point_id']} {item['float_margin']}")
        if item["all_mass_kg"] - lift > 1e-6:
            raise SystemExit(f"above ceiling {item['point_id']}")
        if abs(item["membrane_stress_at_external_Pa"] - item["sigma_required_Pa"]) / item["sigma_required_Pa"] > 1e-12:
            raise SystemExit("stress identity")

    nfis = [
        {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "276 MPa remains the inherited AA typical tensile yield, transferred to compression. Strength safety factors are QUESTIONABLE. The carry is parallel and is not a gate.", "direction": "A compression yield or design allowable can replace the transfer.", "effect": "Strength pressure and the required compressive strength scale linearly with this value."},
        {"NFI_id": "NFI-DENSITY", "gap": "All three points keep the inherited core density of 16 kg/m3. The advisory lower-density leads were not given a point.", "direction": "A later card can spend one of three points on a named lower density.", "effect": "A lighter core leaves more of the ceiling for faces or for a thicker core."},
        {"NFI_id": "NFI-SAND", "gap": "Buckling still uses the inherited sandwich extrapolation and omits core shear from the stated safety factor.", "direction": "Replace with a published sandwich formula that includes shear.", "effect": "The stated buckling pressure can fall once shear is inside the model."},
        {"NFI_id": "NFI-SHEAR", "gap": "The shear target uses the advisory crimping formula p=2*Gc*d/R. It is not a measured core modulus.", "direction": "Pin a core datasheet and a sourced sandwich shear formula.", "effect": "The required Gc scales with external pressure and inversely with d."},
        {"NFI_id": "NFI-WRINKLE", "gap": "The wrinkling target uses the advisory one-half cube-root formula and an equal Ec and Gc split.", "direction": "Separate Ec and Gc from a datasheet.", "effect": "The reported product is the quantity fixed by the formula. The square root is only the equal-split assumption."},
        {"NFI_id": "NFI-CRUSH", "gap": "Core crush has no formula in the pinned brief, so no crush target was produced.", "direction": "Name a crush pressure formula before treating crush as a stated limit.", "effect": "Crush is absent from the least stated safety factor."},
        {"NFI_id": "NFI-KD", "gap": "Knockdown remains 0.2, the inherited severe typical value.", "direction": "Evaluate a knockdown curve at these R/t and sandwich proportions.", "effect": "Buckling pressure and the required modulus scale directly with the knockdown."},
        {"NFI_id": "NFI-MASS", "gap": "Joint fraction, payload allowance and zero gas are unchanged inherited numbers.", "direction": "Replace them with a parts list.", "effect": "They set the structural mass on the ceiling."},
        {"NFI_id": "NFI-GEOM", "gap": "External volume still ignores wall and core intrusion.", "direction": "Inner and outer mould lines.", "effect": "A smaller displaced volume lowers the ceiling."},
        {"NFI_id": "NFI-RULE", "gap": "Equal mass, core-only and proportional scale are stated rules. They are not an optimum and not the advisory search.", "direction": "Do not read the equal-mass point as a proved best split.", "effect": "Another rule would move both safety factors."},
    ]

    utc, mono = now()
    elapsed = mono - ORIGIN
    dur2 = elapsed - p1_elapsed
    phase2 = {
        "schema": 1,
        "phase": 2,
        "name": "three_p2_rows_and_property_targets",
        "end_utc": utc,
        "end_monotonic_s": mono,
        "end_elapsed_s": elapsed,
        "duration_s": dur2,
        "actual_max_s": 450,
        "cumulative_max_s": 600,
        "status": "INSIDE" if dur2 <= 450 and elapsed <= 600 else "OVER",
    }
    out = {
        "schema": 1,
        "status": "ESTIMATE_PENDING_UNA",
        "card": "MAINLINE-003",
        "atmosphere": {"T_K": T, "p_ext_Pa": p_ext, "rho_kg_m3": rho, "volume_m3": V, "lift_kg": lift},
        "sigma_Pa": SIGMA,
        "sigma_tag": "QUESTIONABLE",
        "sigma_transfer": "TRANSFERRED_FROM_TENSILE_YIELD",
        "core_density_kg_m3": rho_c,
        "comparison_P2A": {
            "source": "sealed MAINLINE-002 RESULTS P2-A, recomputed here and not by executing its script",
            "tf_m": tf_a,
            "core_m": core0,
            "buckling_SF": p_s_a / p_ext,
            "strength_SF_QUESTIONABLE": p_y_a / p_ext,
            "E_factor": p_ext / p_s_a,
            "strength_factor": p_ext / p_y_a,
            "match": "PASS",
        },
        "rows": rows,
        "checks": {"P2A_recompute": "PASS", "ceiling_residual": "PASS", "point_count": 3},
    }
    if phase2["status"] != "INSIDE":
        (ROOT / "PHASE2.json").write_text(json.dumps(phase2, indent=1) + "\n")
        raise SystemExit(phase2)
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n")
    (ROOT / "PHASE2.json").write_text(json.dumps(phase2, indent=1) + "\n")
    (ROOT / "NFI.json").write_text(json.dumps(nfis, indent=1) + "\n")
    (ROOT / "INPUTS.json").write_text(json.dumps({
        "schema": 1,
        "card": "MAINLINE-003",
        "status": "ESTIMATE_PENDING_UNA",
        "choice": phase1["choice"],
        "points": phase1["points"],
        "density_kg_m3": rho_c,
        "sigma_Pa": SIGMA,
        "sigma_tag": "QUESTIONABLE",
        "sigma_transfer": "TRANSFERRED_FROM_TENSILE_YIELD",
        "mass_ceiling": "counted mass equals lift; numerical-zero margin is no reserve",
        "comparison": "P2-A recomputed from sealed MAINLINE-001 inputs and matched to sealed MAINLINE-002 RESULTS",
        "omitted_from_stated_SF": ["core_shear", "face_wrinkling", "core_crush"],
    }, indent=1) + "\n")

    lines = [
        "# MAINLINE-003 P2 targets — ESTIMATE_PENDING_UNA",
        "",
        "Unit vacuum-mainline003-p2-targets-owner1200-1019. Three sandwich redistributions at the inherited core density. This estimate is pending its own Una admission and adds no map point.",
        "",
        f"Case: evacuated sphere, external radius {g(R)} m, 500 m ISA air. Pressure {g(p_ext)} Pa. Lift mass {g(lift)} kg. Internal pressure 0. Core density {g(rho_c)} kg/m3.",
        "",
        "Aluminum strength uses 276 MPa as a QUESTIONABLE tensile yield transferred to compression. Modeled strength safety factors are QUESTIONABLE. The transfer is not a certification.",
        "",
        "Each new point sits on the float-mass ceiling. Numerical-zero margin is no reserve and no payload. Face-only P2-A is the sealed comparison, recomputed and matched. These rules are not an optimum.",
        "",
        f"P2-A comparison: face {g(tf_a)} m, core {g(core0)} m, buckling SF {g(p_s_a / p_ext)}, QUESTIONABLE strength SF {g(p_y_a / p_ext)}, modulus factor {g(p_ext / p_s_a)}, strength factor {g(p_ext / p_y_a)}.",
        "",
    ]
    for item in rows:
        lines.append(f"## {item['point_id']} — {item['rule']}")
        lines.append("")
        geo = item["geometry"]
        lines.append(f"Face {g(geo['tf_m'])} m, core {g(geo['core_m'])} m, separation {g(geo['d_m'])} m.")
        lines.append("")
        lines.append("Masses in kilograms: " + ", ".join(f"{k} {g(v)}" for k, v in item["masses_kg"].items()) + f". Total {g(item['all_mass_kg'])}. Float margin {g(item['float_margin'])}.")
        lines.append("")
        lines.append(
            f"Buckling pressure {g(item['limits_Pa']['knocked_down_buckling'])} Pa, safety factor {g(item['buckling_SF'])}. "
            f"QUESTIONABLE yield pressure {g(item['limits_Pa']['aluminum_yield'])} Pa, safety factor {g(item['strength_SF_QUESTIONABLE'])}. "
            f"Governing {item['governing_limit']}. Least stated safety factor {g(item['least_stated_modeled_SF'])}."
        )
        lines.append("")
        lines.append(
            f"Required face modulus {g(item['E_required_Pa'])} Pa. Required compressive strength {g(item['sigma_required_Pa'])} Pa. "
            f"That strength is also the face membrane stress at the external pressure."
        )
        lines.append("")
        om = item["omitted_targets_QUESTIONABLE"]
        lines.append(
            f"QUESTIONABLE targets beside the row: shear modulus {g(om['Gc_for_crimp_at_external_Pa'])} Pa for advisory crimping at the external pressure; "
            f"Ec times Gc {g(om['Ec_times_Gc_Pa2'])} Pa^2 for advisory wrinkling at the membrane stress. "
            f"An equal Ec and Gc split would be {g(om['equal_Ec_Gc_assumption_Pa'])} Pa. Core crush has no formula here."
        )
        lines.append("")
    lines.append("Lower core density is not one of the three points. Needs-further-investigation rows are in NFI.json.")
    (ROOT / "CARD.md").write_text("\n".join(lines) + "\n")
    utc3, mono3 = now()
    elapsed3 = mono3 - ORIGIN
    dur3 = elapsed3 - elapsed
    phase3 = {
        "schema": 1,
        "phase": 3,
        "name": "card_inputs_nfi_comparison",
        "end_utc": utc3,
        "end_monotonic_s": mono3,
        "end_elapsed_s": elapsed3,
        "duration_s": dur3,
        "actual_max_s": 200,
        "cumulative_max_s": 800,
        "status": "INSIDE" if dur3 <= 200 and elapsed3 <= 800 else "OVER",
    }
    (ROOT / "PHASE3.json").write_text(json.dumps(phase3, indent=1) + "\n")
    if phase3["status"] != "INSIDE":
        raise SystemExit(phase3)
    summary = []
    for item in rows:
        summary.append({
            "id": item["point_id"],
            "tf": item["geometry"]["tf_m"],
            "core": item["geometry"]["core_m"],
            "buck_sf": item["buckling_SF"],
            "str_sf": item["strength_SF_QUESTIONABLE"],
            "least": item["least_stated_modeled_SF"],
            "E_req": item["E_required_Pa"],
            "sig_req": item["sigma_required_Pa"],
            "Gc": item["omitted_targets_QUESTIONABLE"]["Gc_for_crimp_at_external_Pa"],
            "EcGc": item["omitted_targets_QUESTIONABLE"]["Ec_times_Gc_Pa2"],
            "governing": item["governing_limit"],
        })
    print(json.dumps({"elapsed2": elapsed, "elapsed3": elapsed3, "p2a_sf": p_s_a / p_ext, "rows": summary}, indent=1))


if __name__ == "__main__":
    main()
