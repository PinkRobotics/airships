"""Independent MAINLINE-018 arithmetic; no owner script is read or executed."""
import json
import math
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
inputs = json.loads((HERE / "INPUTS.json").read_text())


def biaxial_factor():
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid**3 + mid < 1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


B = biaxial_factor()
case = inputs["case"]
P, R, NU = case["p_Pa"], case["R_m"], case["nu"]
comparisons = []


def compare(row, field, filed, independently_computed):
    difference = independently_computed - filed
    comparisons.append({
        "row": row, "field": field, "filed": filed,
        "checker": independently_computed, "difference": difference,
        "relative_difference": difference / filed if filed else None,
        "matches": math.isclose(filed, independently_computed,
                               rel_tol=2e-12, abs_tol=2e-12),
    })


def evaluate(geometry, face, core, gamma_function):
    t, c = geometry["tf_m"], geometry["core_m"]
    h = t + c
    e, strength = face["E_Pa"], face["sigma_Pa"]
    ec, gc = core["Ec_Pa"], core["Gc_Pa"]
    sigma0 = e * h / (R * math.sqrt(1 - NU**2))
    crimp = h**2 * gc / (2 * t * c)
    vc = sigma0 / crimp
    kc = 1 - vc / 4 if vc <= 2 else 1 / vc
    gamma = gamma_function(vc)
    demand = P * R / (4 * t)
    if core["form"] == "honeycomb":
        wrinkling_uniaxial = 0.33 * math.sqrt(e * ec * t / c)
    else:
        wrinkling_uniaxial = 0.50 * (e * ec * gc / (1 - NU**2))**(1/3)
    modes = {
        "global_buckling": gamma * kc * sigma0 / demand,
        "face_compression": strength / demand,
        "core_shear_crimping_bare": crimp / demand,
        "core_crush": core["crush_Pa"] / (P / 2),
        "face_wrinkling": B * wrinkling_uniaxial / demand,
    }
    # On the crimp branch, global and crimp are the same physical mechanism.
    # Keep the unmodified bare crimp limit explicit but rank the mechanism once.
    effective = {
        ("core_shear_crimping" if vc >= 2 else "global_buckling"):
            modes["global_buckling"],
        "face_compression": modes["face_compression"],
        "core_crush": modes["core_crush"],
        "face_wrinkling": modes["face_wrinkling"],
    }
    if vc < 2:
        effective["core_shear_crimping"] = modes["core_shear_crimping_bare"]
    ranking = sorted(effective.items(), key=lambda item: item[1])
    mass = 1.05 * 4 * math.pi * R**2 * (
        2 * t * face["rho_kg_m3"] + c * core["rho_kg_m3"]) + 100
    return {
        "tf_m": t, "core_m": c, "h_m": h, "sigma0_Pa": sigma0,
        "sigma_crimp_Pa": crimp, "face_demand_Pa": demand, "Vc": vc,
        "Kc": kc, "gamma": gamma, "modes": modes,
        "effective_modes": effective,
        "governing": ranking[0][0], "least_SF": ranking[0][1],
        "second_mode": ranking[1][0], "second_SF": ranking[1][1],
        "factor_to_SF_1": 1 / ranking[0][1],
        "total_mass_kg": mass, "payload_kg": case["lift_kg"] - mass,
        "float_margin": 1 - mass / case["lift_kg"],
    }


rescores = []
for raw in inputs["rows"]:
    result = {"label": raw["label"], "curves": {}}
    filed_row = raw["owner"]
    for name, gamma in {
        "optimistic": lambda v: 0.2 + 0.4 * min(v, 2),
        "conservative": lambda v: 0.2,
    }.items():
        values = evaluate(raw["geometry"], raw["face"], raw["core"], gamma)
        result["curves"][name] = values
        old = filed_row["curves"][name]
        for field in ["gamma", "least_SF", "second_SF", "factor_to_SF_1"]:
            compare(raw["label"], f"{name}.{field}", old[field], values[field])
        for field, filed in old["modes"].items():
            mapped = {"face_yield": "face_compression",
                      "core_shear_crimping": "core_shear_crimping_bare"}.get(
                          field, field)
            compare(raw["label"], f"{name}.modes.{field}", filed,
                    values["modes"][mapped])
        compare(raw["label"], f"{name}.bare_crimp_SF",
                old["bare_crimp_SF"], values["modes"]["core_shear_crimping_bare"])
        compare(raw["label"], f"{name}.design_global_SF",
                old["design_global_SF"], values["modes"]["global_buckling"])
        for field in ["governing", "second_mode"]:
            if old[field] != values[field]:
                raise AssertionError((raw["label"], name, field,
                                      old[field], values[field]))
    for field in ["tf_m", "core_m", "Vc", "Kc"]:
        compare(raw["label"], field, filed_row[field], values[field])
    handbook = evaluate(raw["geometry"], raw["face"], raw["core"],
                        lambda v: 0.2 if v < 2 else 1.0)
    compare(raw["label"], "filed_least_SF", filed_row["filed_least_SF"],
            handbook["least_SF"])
    compare(raw["label"], "gamma_filed", filed_row["gamma_filed"],
            handbook["gamma"])
    compare(raw["label"], "margin", filed_row["margin"],
            handbook["float_margin"])
    rescores.append(result)

sim = {}
for name, raw in inputs["sim"]["rows"].items():
    t1, t2, c, ro = raw["t_outer_m"], raw["t_inner_m"], raw["t_core_m"], raw["R_outer_m"]
    h = c + (t1 + t2) / 2
    rm = ro - (t1 + t2 + c) / 2
    e, nu = inputs["sim"]["face_E_Pa"], inputs["sim"]["face_nu"]
    gc = inputs["sim"]["core_E_Pa"] / (2 * (1 + inputs["sim"]["core_nu"]))
    # NASA CR-1457 eqs. 6.2-8, 6.2-12, 6.2-19 to 6.2-23.
    unequal_factor = 2 * math.sqrt(t1 * t2) / (t1 + t2)
    sigma0_equal_approximation = e * h / (rm * math.sqrt(1 - nu**2))
    sigma0 = sigma0_equal_approximation * unequal_factor
    crimp = h**2 * gc / ((t1 + t2) * c)
    vc = sigma0 / crimp
    p_handbook_crimp = 2 * (t1 + t2) * crimp / rm
    values = {
        "h_m": h, "R_middle_m": rm, "R_over_tc": rm / c, "Gc_Pa": gc,
        "unequal_face_factor": unequal_factor, "sigma_0_Pa": sigma0,
        "sigma_0_equal_face_approximation_Pa": sigma0_equal_approximation,
        "sigma_crimp_Pa": crimp, "Vc": vc,
        "Vc_equal_face_approximation": sigma0_equal_approximation / crimp,
        "Gc_for_Vc_eq_2_Pa": gc * vc / 2,
        "branch": "shear_crimping" if vc >= 2 else "stiff_or_moderate",
        "published_kdf": raw["published_kdf"],
        "published_imperfect_Pa": raw["imperfect_Pa"],
        "published_linear_perfect_Pa": raw["linear_perfect_Pa"],
        "kdf_from_published_rounded_pressures": raw["imperfect_Pa"] / raw["linear_perfect_Pa"],
        "conditional_CR1457_crimp_pressure_Pa": p_handbook_crimp,
        "imperfect_over_CR1457_crimp": raw["imperfect_Pa"] / p_handbook_crimp,
        "Gc_threshold_over_foam_E": (gc * vc / 2) / inputs["sim"]["core_E_Pa"],
    }
    old = inputs["owner_result"]["tests"]["sim_2024"]["rows"][name]
    for field in ["h_m", "R_middle_m", "R_over_tc", "sigma_0_Pa",
                  "sigma_crimp_Pa", "Vc", "Gc_for_Vc_eq_2_Pa"]:
        compare("Sim " + name, field, old[field], values[field])
    sim[name] = values

summary = {
    "schema": 1, "card": "MAINLINE-018 independent check",
    "status": "CHECKED_WITH_NFI", "tag": "QUESTIONABLE", "certification": False,
    "started_at": inputs["started_at"],
    "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "independence": "Fresh formulas from the handbook and pinned material/geometry data. Owner scripts were neither read nor executed.",
    "biaxial_factor": B, "sim": sim, "rescore": rescores,
    "comparisons": comparisons,
    "comparison_count": len(comparisons),
    "mismatches": [r for r in comparisons if not r["matches"]],
    "source_coverage": inputs["source_coverage"],
}
(HERE / "RESULTS.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({
    "comparison_count": summary["comparison_count"],
    "mismatches": summary["mismatches"],
    "least_factors": {r["label"]: {k: v["least_SF"] for k, v in r["curves"].items()}
                      for r in rescores},
    "sim": sim,
}, indent=2))
