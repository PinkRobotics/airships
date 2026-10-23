"""Independent MAINLINE-009e calculation; no owner code imported or executed."""
import json
import math
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = json.loads((HERE / "INPUTS.json").read_text())
CASE, FACE = INPUT["case"], INPUT["face"]
R, P, NU, LIFT = (CASE[k] for k in ("R_m", "p_Pa", "nu", "lift_kg"))
E, RF, SY = (FACE[k] for k in ("E_Pa", "rho_kg_m3", "sigma_Pa"))
AREA = 4 * math.pi * R**2
JOINTS = INPUT["mass_model"]["joint_fraction_of_structure"]
SYSTEMS = INPUT["mass_model"]["systems_kg"]
MARGIN = INPUT["mass_model"]["payload_fraction"]
STRUCTURE = ((1 - MARGIN) * LIFT - SYSTEMS) / (1 + JOINTS)
lo, hi = 0.0, 1.0
for _ in range(100):
    mid = (lo + hi) / 2
    if mid**3 + mid < 1:
        lo = mid
    else:
        hi = mid
BIAXIAL = (lo + hi) / 2
COMPARISONS, LABEL_CHECKS = [], []


def compare(row, field, filed, own):
    COMPARISONS.append({
        "row": row, "field": field, "filed": filed, "checker": own,
        "difference": own - filed,
        "matches": math.isclose(filed, own, rel_tol=2e-12, abs_tol=2e-12),
    })


def geometry(fraction, core, margin=MARGIN):
    structure = ((1 - margin) * LIFT - SYSTEMS) / (1 + JOINTS)
    return ((1 - fraction) * structure / (2 * AREA * RF),
            fraction * structure / (AREA * core["rho_kg_m3"]))


def score(fraction, core, k, margin=MARGIN, curve="optimistic"):
    t, c = geometry(fraction, core, margin)
    h = t + c
    demand = P * R / (4 * t)
    sigma0 = E * h / (R * math.sqrt(1 - NU**2))
    sigma_crimp = h**2 * core["Gc_Pa"] / (2 * t * c)
    vc = sigma0 / sigma_crimp
    kc = 1 - vc / 4 if vc <= 2 else 1 / vc
    gamma = (0.2 + 0.4 * min(vc, 2) if curve == "optimistic"
             else (0.2 if vc < 2 else 1.0))
    modes = {
        "global_buckling": gamma * kc * sigma0 / demand,
        "face_yield": SY / demand,
        "core_shear_crimping": sigma_crimp / demand,
        "core_crush": core["crush_Pa"] / (P / 2),
        "face_wrinkling": BIAXIAL * k * math.sqrt(E * core["Ec_Pa"] * t / c) / demand,
        "intracell_dimpling": 2 * E / (1 - NU**2) * (t / core["s_cell_m"])**2 / demand,
    }
    ranked = sorted(modes.items(), key=lambda x: x[1])
    structural = AREA * (2 * t * RF + c * core["rho_kg_m3"])
    total = (1 + JOINTS) * structural + SYSTEMS
    return {
        "tf_m": t, "core_m": c, "h_m": h, "core_mass_fraction": fraction,
        "Vc": vc, "Kc": kc, "gamma": gamma,
        "branch": "shear_crimping" if vc >= 2 else "stiff_or_moderate_core",
        "k_wrinkle": k, "sfs": modes, "least_SF": ranked[0][1],
        "governing": ranked[0][0], "second_SF": ranked[1][1], "second_mode": ranked[1][0],
        "core_name": core["name"], "structural_kg": structural,
        "total_kg": total, "payload_kg": LIFT - total, "margin": 1 - total / LIFT,
        "sigma0_Pa": sigma0, "sigma_crimp_Pa": sigma_crimp, "demand_Pa": demand,
        "intracell_dimpling_equal_biaxial": modes["intracell_dimpling"] / 2,
        "least_SF_with_biaxial_dimpling": min(ranked[0][1], modes["intracell_dimpling"] / 2),
        "global_only_gamma_for_SF_1": demand / (kc * sigma0),
        "held_geometry_least_SF_ceiling_if_only_gamma_changes":
            min(v for mode, v in modes.items() if mode != "global_buckling"),
        "face_strength_for_face_SF_1_Pa": demand,
    }


def optimize(core, k, margin=MARGIN, curve="optimistic"):
    # Sweep the entire physical interval before refining the best region.
    def objective(f):
        return score(f, core, k, margin, curve)["least_SF"]
    best_value, best_fraction = max((objective(i / 8000), i / 8000)
                                    for i in range(1, 8000))
    a, b = max(1e-12, best_fraction - 0.0005), min(1 - 1e-12, best_fraction + 0.0005)
    ratio = (math.sqrt(5) - 1) / 2
    x, y = b - ratio * (b - a), a + ratio * (b - a)
    fx, fy = objective(x), objective(y)
    for _ in range(100):
        if fx < fy:
            a, x, fx = x, y, fy
            y = a + ratio * (b - a)
            fy = objective(y)
        else:
            b, y, fy = y, x, fx
            x = b - ratio * (b - a)
            fx = objective(x)
    refined = (a + b) / 2
    return {
        "grid_step": 1 / 8000, "grid_evaluations": 7999,
        "grid_best": score(best_fraction, core, k, margin, curve),
        "refined": score(refined, core, k, margin, curve),
        "scope": "Fixed face/core pair, mass limit, and assigned curve; not a search over materials.",
    }


owner = INPUT["owner_point"]
points = []
for raw in owner["optima"]:
    core = next(c for c in INPUT["cores"] if c["name"] == raw["core_name"])
    k = raw["k_wrinkle"]
    label = f'{core["name"]}, k={k}'
    optimization = optimize(core, k)
    grid = optimization["grid_best"]
    # Compare every numeric output field, using independently found geometry.
    for field, value in raw.items():
        if isinstance(value, (int, float)):
            compare(label, field, value, grid[field])
        elif field == "sfs":
            for mode, sf in value.items():
                compare(label, "sfs." + mode, sf, grid["sfs"][mode])
        else:
            LABEL_CHECKS.append({"row": label, "field": field, "filed": value,
                                 "checker": grid[field], "matches": value == grid[field]})
    # A second method solves the governing mode crossing directly.
    left, right = 1e-10, grid["core_mass_fraction"] + 0.001
    for _ in range(100):
        middle = (left + right) / 2
        sfs = score(middle, core, k)["sfs"]
        if sfs["global_buckling"] < sfs["face_yield"]:
            left = middle
        else:
            right = middle
    crossing = score((left + right) / 2, core, k)
    assert math.isclose(crossing["least_SF"], optimization["refined"]["least_SF"], rel_tol=2e-12)
    # The exact maximum Vc on this mass line follows from t=A(1-f), c=Bf.
    a = STRUCTURE / (2 * AREA * RF)
    b = STRUCTURE / (AREA * core["rho_kg_m3"])
    f_vmax = math.sqrt(a) / (math.sqrt(a) + math.sqrt(b))
    vcmax = score(f_vmax, core, k)["Vc"]
    assert vcmax < 2
    points.append({
        "name": label, "core": core, "optimization": optimization,
        "global_face_crossing": crossing,
        "analytic_Vc_maximum": {"fraction": f_vmax, "Vc": vcmax,
            "derivation": "Vc=C*A*B*f*(1-f)/(A+(B-A)*f); maximum at f=sqrt(A)/(sqrt(A)+sqrt(B))."},
        "refinement_gain_SF": crossing["least_SF"] - grid["least_SF"],
        "refinement_gain_relative": crossing["least_SF"] / grid["least_SF"] - 1,
    })

held = points[0]["optimization"]["grid_best"]
for field in ["margin", "structural_kg", "payload_kg", "total_kg"]:
    compare("mass", field, owner[field], held[field])
compare("material", "density_kg_m3", owner["density_kg_m3"], INPUT["cores"][0]["rho_kg_m3"])
ceiling = optimize(INPUT["cores"][0], 0.33, margin=0, curve="handbook")
compare("handbook zero-payload control", "ceiling_check_least_SF",
        owner["ceiling_check_least_SF"], ceiling["grid_best"]["least_SF"])
psi, pcf = 0.45359237 * 9.80665 / 0.0254**2, 0.45359237 / 0.3048**3
for core in INPUT["cores"]:
    for field, own in {
        "rho_kg_m3": 1.6 * pcf, "Ec_Pa": 30000 * psi, "Gc_Pa": 10500 * psi,
        "Gl_Pa": 20000 * psi, "crush_Pa": 50 * psi,
        "s_cell_m": (1 / 4 if core["cell"] == "1/4" else 3 / 8) * 0.0254,
        "shear_strength_L_Pa": 90 * psi, "shear_strength_W_Pa": 60 * psi,
    }.items():
        compare(core["name"], "material." + field, core[field], own)

result = {
    "schema": 1, "unit": INPUT["unit"], "card": "MAINLINE-009e independent check",
    "status": "CHECKED_WITH_NFI", "tag": "QUESTIONABLE", "curve_tag": "PROJECTION",
    "certification": "none", "started_at": INPUT["started_at"],
    "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "independence": INPUT["independence"],
    "comparison_tolerance": {"relative": 2e-12, "absolute": 2e-12},
    "comparison_count": len(COMPARISONS), "comparisons": COMPARISONS,
    "mismatches_under_stated_formulas": [c for c in COMPARISONS if not c["matches"]],
    "label_checks": LABEL_CHECKS,
    "label_mismatches": [c for c in LABEL_CHECKS if not c["matches"]],
    "points": points, "handbook_zero_payload_control": ceiling,
    "biaxial_wrinkling_factor": BIAXIAL,
    "unit_conversions": {"psi_to_Pa": psi, "pcf_to_kg_m3": pcf},
    "dimpling_source_note": {
        "source": "NASA CR-1457 pp 2-5 and 2-7, equations 2.1-4 and 2.1-6",
        "finding": "The stated uniaxial estimate reproduces. Equal biaxial compression halves this mode, without changing any optimum or governing mode.",
        "classification": "Known inherited modelling discrepancy, not a numeric mismatch against the stated formula.",
    },
}
(HERE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({
    "comparison_count": result["comparison_count"],
    "mismatches": result["mismatches_under_stated_formulas"],
    "label_mismatches": result["label_mismatches"],
    "points": [{
        "name": p["name"], "grid_least": p["optimization"]["grid_best"]["least_SF"],
        "refined_fraction": p["global_face_crossing"]["core_mass_fraction"],
        "refined_least": p["global_face_crossing"]["least_SF"],
        "refined_tf_m": p["global_face_crossing"]["tf_m"],
        "refined_core_m": p["global_face_crossing"]["core_m"],
        "Vc_max": p["analytic_Vc_maximum"]["Vc"],
        "dimpling_biaxial": p["optimization"]["grid_best"]["intracell_dimpling_equal_biaxial"],
        "refinement_relative": p["refinement_gain_relative"],
    } for p in points],
    "held_gamma_global_1": held["global_only_gamma_for_SF_1"],
    "held_face_strength_for_1_Pa": held["face_strength_for_face_SF_1_Pa"],
    "handbook_ceiling": ceiling["grid_best"]["least_SF"],
}, indent=2))
