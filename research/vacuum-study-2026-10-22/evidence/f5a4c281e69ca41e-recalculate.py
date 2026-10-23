"""Independent MAINLINE-018b equations; no owner code used."""
import json
import math
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "INPUTS.json").read_text())
sim, owner = data["sim"], data["owner_results"]
E, NU = sim["face_E_Pa"], sim["face_nu"]
GC = sim["core_E_Pa"] / (2 * (1 + sim["core_nu"]))
lead = data["lead_point"]
LEAST = lead["least_SF"]
local_limit = min(v for k, v in lead["modes"].items()
                  if k not in ("global_buckling", "core_shear_crimping"))
comparisons = []


def compare(row, field, filed, own):
    comparisons.append({
        "row": row, "field": field, "filed": filed, "checker": own,
        "difference": own - filed,
        "relative_difference": own / filed - 1 if filed != 0 else None,
        "matches": math.isclose(filed, own, rel_tol=2e-12, abs_tol=2e-12),
    })


shells, sensitivities = {}, {}
for name, raw in sim["rows"].items():
    t1, t2, c, rout = (raw[k] for k in
                       ("t_outer_m", "t_inner_m", "t_core_m", "R_outer_m"))
    total_faces = t1 + t2
    h = c + total_faces / 2
    rm = rout - (c + total_faces) / 2
    q = 2 * math.sqrt(t1 * t2) / total_faces
    sigma0_equal = E * h / (rm * math.sqrt(1 - NU**2))
    sigma0 = sigma0_equal * q
    sigma_crimp = h**2 * GC / (total_faces * c)
    p_crimp = 2 * h**2 * GC / (rm * c)
    p_classical = 2 * sigma0 * total_faces / rm
    gamma = raw["imperfect_Pa"] / p_crimp
    down = E / (1 - NU**2) * (t1**3 + t2**3) / 12
    dseparation = E / (1 - NU**2) * t1 * t2 / total_faces * h**2
    pressure_fields = ["linear_perfect_Pa", "nonlinear_perfect_Pa", "imperfect_Pa", "published_kdf"]
    own = {
        "name": name, "t_outer_m": t1, "t_inner_m": t2, "t_core_m": c,
        "h_m": h, "R_outer_m": rout, "R_middle_m": rm, "R_over_tc": rm / c,
        "sigma_0_Pa": sigma0, "sigma_crimp_Pa": sigma_crimp,
        "Vc": sigma0 / sigma_crimp, "branch": "shear_crimping",
        "p_crimp_Pa": p_crimp, "p_classical_Pa": p_classical,
        "linear_over_crimp": raw["linear_perfect_Pa"] / p_crimp,
        "nonlinear_perfect_over_crimp": raw["nonlinear_perfect_Pa"] / p_crimp,
        "gamma_imperfect_over_crimp": gamma,
        "published_kdf_check": raw["imperfect_Pa"] / raw["linear_perfect_Pa"],
        "face_bending_share_of_flexural_rigidity": down / (down + dseparation),
        "lead_least_times_gamma": LEAST * gamma,
        "pressures": {k: raw[k] for k in pressure_fields},
        "unequal_face_factor": q,
        "D_own_faces_Nm": down, "D_face_separation_Nm": dseparation,
        "D_total_facings_Nm": down + dseparation,
        "equal_face_approximation": {
            "sigma_0_Pa": sigma0_equal, "Vc": sigma0_equal / sigma_crimp,
            "p_classical_Pa": 2 * sigma0_equal * total_faces / rm,
        },
        "Gc_for_gamma_equal_one_Pa": GC * gamma,
        "lead_uncapped_all_modes_if_gamma_only_changes_crimp":
            min(LEAST * gamma, local_limit),
    }
    assert own["Vc"] > 2
    for field, value in owner["shells"][name].items():
        if isinstance(value, (int, float)):
            compare(name, field, value, own[field])
        elif field == "pressures":
            for key in pressure_fields:
                compare(name, "pressures." + key, value[key], own["pressures"][key])
    shells[name] = own
    sensitivities[name] = {}
    for label, properties in data["shear_rows"].items():
        g = properties["Gc_Pa"]
        p = 2 * h**2 * g / (rm * c)
        ratio = raw["imperfect_Pa"] / p
        row = {
            "Gc_Pa": g, "p_crimp_Pa": p, "gamma": ratio,
            "lead_least_times_gamma": LEAST * ratio,
            "Vc": own["Vc"] * GC / g,
            "lead_uncapped_all_modes_if_gamma_only_changes_crimp":
                min(LEAST * ratio, local_limit),
            "lead_all_modes_with_gamma_capped_at_one":
                min(LEAST * min(ratio, 1), local_limit),
            "scope": "Denominator-only Gc sensitivity; published collapse pressure held fixed, no new simulation.",
        }
        for field, value in owner["sensitivity"][name][label].items():
            compare(name + "." + label, field, value, row[field])
        sensitivities[name][label] = row

compare("all", "Gc_paper_Pa", owner["Gc_paper_Pa"], GC)
compare("lead", "design_credit_cap", owner["design_credit_cap"], 1.0)
compare("lead", "carried_least_if_capped", owner["carried_least_if_capped"], LEAST)
for grade, shear, compression in [("H80", 27e6, 90e6), ("H35", 12e6, 40e6)]:
    compare(grade, "CARD.shear_modulus_Pa", shear, data["shear_rows"][grade]["Gc_Pa"])
    compare(grade, "CARD.compression_modulus_Pa", compression, data["shear_rows"][grade]["Ec_Pa"])

result = {
    "schema": 1, "card": "MAINLINE-018b independent check", "unit": data["unit"],
    "status": "CHECKED_WITH_CORRECTION_AND_NFI", "tag": "QUESTIONABLE",
    "transfer_tag": "PROJECTION", "certification": "none",
    "started_at": data["started_at"],
    "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "independence": data["independence"],
    "comparison_tolerance": {"relative": 2e-12, "absolute": 2e-12},
    "comparison_count": len(comparisons),
    "comparisons": comparisons,
    "mismatches": [c for c in comparisons if not c["matches"]],
    "shells": shells, "sensitivity": sensitivities,
    "lead_baseline_least_SF": LEAST,
    "lead_other_mode_limit": local_limit,
    "lead_other_mode_governing": "face_wrinkling",
    "face_bending_scope": "Fraction of facings-only conventional flexural rigidity. Does not measure the omitted term's effect on crimp collapse pressure.",
    "curve_scope": "Two numerical high-Vc cases exceed the conditional unity-crimp prediction. This is neither a fit for gamma(Vc) nor validation of a 10 m honeycomb sphere.",
}
(HERE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({
    "comparison_count": result["comparison_count"],
    "mismatch_count": len(result["mismatches"]),
    "mismatches": result["mismatches"],
    "gamma_by_shear_row": {
        name: {k: v["gamma"] for k, v in rows.items()}
        for name, rows in sensitivities.items()
    },
    "own_face_bending_shares": {
        name: row["face_bending_share_of_flexural_rigidity"]
        for name, row in shells.items()
    },
    "uncapped_lead_other_mode_limit": local_limit,
    "lead_carried_with_cap": LEAST,
}, indent=2))
