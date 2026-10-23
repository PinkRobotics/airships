"""Independent MAINLINE-009d check, including mass-constrained searches."""
import json
import math
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "INPUTS.json").read_text())
case = data["case"]
P, R, LIFT, NU = case["p_Pa"], case["R_m"], case["lift_kg"], case["nu"]
AREA = 4 * math.pi * R**2
FACE = data["face"]
E, RHO, SIGMA = FACE["E_Pa"], FACE["rho_kg_m3"], FACE["sigma_Pa"]
lo, hi = 0.0, 1.0
for _ in range(100):
    mid = (lo + hi) / 2
    if mid**3 + mid < 1:
        lo = mid
    else:
        hi = mid
B = (lo + hi) / 2
COMPARISONS = []


def compare(row, field, filed, own):
    COMPARISONS.append({
        "row": row, "field": field, "filed": filed, "checker": own,
        "difference": own - filed,
        "matches": math.isclose(filed, own, rel_tol=2e-12, abs_tol=2e-12),
    })


def score(t, c, core, curve="handbook"):
    h = t + c
    sigma0 = E * h / (R * math.sqrt(1 - NU**2))
    crimp = h * h * core["Gc_Pa"] / (2 * t * c)
    vc = sigma0 / crimp
    kc = 1 - vc / 4 if vc <= 2 else 1 / vc
    gamma = {"handbook": (0.2 if vc < 2 else 1.0),
             "optimistic": 0.2 + 0.4 * min(vc, 2),
             "conservative": 0.2}[curve]
    demand = P * R / (4 * t)
    wrinkle = B * 0.33 * math.sqrt(E * core["Ec_Pa"] * t / c) / demand
    dimpling = 2 * E / (1 - NU**2) * (t / core["s_cell_m"])**2 / demand
    modes = {
        "global_buckling": gamma * kc * sigma0 / demand,
        "face_compression": SIGMA / demand,
        "core_shear_crimping": crimp / demand,
        "core_crush": core["crush_Pa"] / (P / 2),
        "face_wrinkling": wrinkle,
        "intracell_dimpling": dimpling,
    }
    effective = {
        ("core_shear_crimping" if vc >= 2 else "global_buckling"): modes["global_buckling"],
        "face_compression": modes["face_compression"],
        "face_wrinkling": wrinkle,
        "core_crush": modes["core_crush"],
        "intracell_dimpling": dimpling,
    }
    if vc < 2:
        effective["core_shear_crimping"] = crimp / demand
    ranking = sorted(effective.items(), key=lambda kv: kv[1])
    structural = AREA * (2 * t * RHO + c * core["rho_kg_m3"])
    mass = 1.05 * structural + 100
    return {
        "tf_m": t, "core_m": c, "h_m": h, "Vc": vc, "Kc": kc,
        "gamma": gamma, "modes": modes, "effective_modes": effective,
        "least_SF": ranking[0][1], "governing": ranking[0][0],
        "second_SF": ranking[1][1], "second_mode": ranking[1][0],
        "factor_to_SF_1": 1 / ranking[0][1],
        "wrinkle_SF_coefficient_0.82": wrinkle * 0.82 / 0.33,
        "intracell_dimpling_equal_biaxial": dimpling / 2,
        "least_SF_with_biaxial_dimpling": min(ranking[0][1], dimpling / 2),
        "structural_kg": structural, "total_kg": mass,
        "payload_kg": LIFT - mass, "margin": 1 - mass / LIFT,
        "core_mass_fraction": AREA * c * core["rho_kg_m3"] / structural,
        "kd_that_brings_global_to_1": demand / (kc * sigma0),
        "maximum_least_SF_if_only_global_gamma_changes":
            min(v for k, v in modes.items() if k != "global_buckling"),
    }


def geometry(fraction, core, margin):
    structural = ((1 - margin) * LIFT - 100) / 1.05
    return ((1 - fraction) * structural / (2 * AREA * RHO),
            fraction * structural / (AREA * core["rho_kg_m3"]))


def objective(fraction, core, margin):
    t, c = geometry(fraction, core, margin)
    return score(t, c, core)["least_SF"]


def optimize(core, margin):
    # A separate full mass-fraction sweep, followed by local interval refinement.
    grid = [(objective(i / 8000, core, margin), i / 8000)
            for i in range(1, 8000)]
    best_value, fraction = max(grid)
    a, b = max(1e-9, fraction - 0.0005), min(1 - 1e-9, fraction + 0.0005)
    ratio = (math.sqrt(5) - 1) / 2
    x, y = b - ratio * (b - a), a + ratio * (b - a)
    fx, fy = objective(x, core, margin), objective(y, core, margin)
    for _ in range(100):
        if fx < fy:
            a, x, fx = x, y, fy
            y = a + ratio * (b - a)
            fy = objective(y, core, margin)
        else:
            b, y, fy = y, x, fx
            x = b - ratio * (b - a)
            fx = objective(x, core, margin)
    refined = (a + b) / 2
    t, c = geometry(refined, core, margin)
    return {
        "grid_fraction_step": 1 / 8000,
        "grid_best_fraction": fraction, "grid_best_least_SF": best_value,
        "refined_fraction": refined, "refined": score(t, c, core),
        "scope": "Fixed sourced material pair, fixed mass, inherited handbook model; numerical refinement of the grid, not a new material search.",
    }


owner = data["owner_point"]
aramid_owner = owner["aramid_crimp_branch"]
points = []
for name, raw, core in [
    ("aramid", aramid_owner, data["cores"][0]),
    *[(core["name"], row, core)
      for core, row in zip(data["cores"][1:], owner["aluminium_stiff_branch"]["cores"])],
]:
    curves = {curve: score(raw["tf_m"], raw["core_m"], core, curve)
              for curve in ["handbook", "optimistic", "conservative"]}
    own = curves["handbook"]
    for key in ["tf_m", "core_m", "h_m", "Vc", "Kc", "gamma", "least_SF",
                "second_SF", "wrinkle_SF_coefficient_0.82", "core_mass_fraction"]:
        if key in raw:
            compare(name, key, raw[key], own[key])
    for key, value in raw.get("modes", raw.get("sfs")).items():
        mapped = "face_compression" if key == "face_yield" else key
        compare(name, "modes." + key, value, own["modes"][mapped])
    for key, value in owner["mass"].items():
        compare(name, "mass." + key, value, own[key])
    assert raw["governing"] == own["governing"]
    if "second_mode" in raw:
        assert raw["second_mode"] == own["second_mode"]
    if name != "aramid":
        compare(name, "kd_that_brings_global_to_1",
                owner["aluminium_stiff_branch"]["kd_statement"]["kd_that_brings_global_to_1"],
                own["kd_that_brings_global_to_1"])
    points.append({"name": name, "core": core, "curves": curves,
                   "optimization_margin_0_05": optimize(core, 0.05)})

# Verify the earlier, distinct aramid curve carry as part of interpreting 009d.
for curve, old in data["owner_aramid_curve_carry"]["curves"].items():
    own = points[0]["curves"][curve]
    for key in ["gamma", "least_SF", "second_SF", "factor_to_SF_1"]:
        compare("earlier aramid curve carry", curve + "." + key, old[key], own[key])
    for key, value in old["modes"].items():
        compare("earlier aramid curve carry", curve + ".modes." + key, value, own["modes"][key])

ceiling = optimize(data["cores"][1], 0)
compare("aluminium zero-payload ceiling", "grid_least_SF",
        0.668649769509, ceiling["grid_best_least_SF"])
psi = 0.45359237 * 9.80665 / 0.0254**2
pcf = 0.45359237 / 0.3048**3
conversion_checks = {"psi_to_Pa": psi, "pcf_to_kg_m3": pcf}
for core in data["cores"][1:]:
    for key, own in {"rho_kg_m3": 1.6 * pcf, "Ec_Pa": 30000 * psi,
                     "Gc_Pa": 10500 * psi, "crush_Pa": 50 * psi}.items():
        compare(core["name"], "material." + key, core[key], own)

result = {
    "schema": 1, "card": "MAINLINE-009d both points independent check",
    "status": "CHECKED_WITH_NFI", "tag": "QUESTIONABLE", "certification": False,
    "started_at": data["started_at"],
    "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "independence": "Own formula implementation and independent mass-fraction search; no owner script read or executed.",
    "biaxial_wrinkle_factor": B, "unit_conversions": conversion_checks,
    "points": points, "aluminium_ceiling_check": ceiling,
    "comparisons": COMPARISONS, "comparison_count": len(COMPARISONS),
    "mismatches_under_stated_formula": [x for x in COMPARISONS if not x["matches"]],
    "dimpling_source_difference": {
        "status": "Known upstream modelling NFI, not an arithmetic mismatch against its explicitly stated uniaxial formula.",
        "source": "NASA CR-1457 pp 2-5 and 2-7, eqs 2.1-4 and 2.1-6.",
        "rule": "Rx+Ry=1; for equal biaxial compression divide the uniaxial allowable by two.",
        "aramid_mode": "Missing from the filed aramid row; independently evaluated from the nominal 4.8 mm cell.",
    },
}
(HERE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({
    "comparison_count": len(COMPARISONS),
    "mismatches": result["mismatches_under_stated_formula"],
    "summary": [{"name": p["name"],
                 "least_by_curve": {k: v["least_SF"] for k, v in p["curves"].items()},
                 "biaxial_dimpling": p["curves"]["handbook"]["intracell_dimpling_equal_biaxial"],
                 "optimistic_gamma": p["curves"]["optimistic"]["gamma"],
                 "optimistic_global_SF": p["curves"]["optimistic"]["modes"]["global_buckling"],
                 "refined_best": p["optimization_margin_0_05"]["refined"]["least_SF"],
                 "refined_fraction": p["optimization_margin_0_05"]["refined_fraction"]}
                for p in points],
    "ceiling_grid_best": ceiling["grid_best_least_SF"],
    "ceiling_refined": ceiling["refined"]["least_SF"],
}, indent=2))
