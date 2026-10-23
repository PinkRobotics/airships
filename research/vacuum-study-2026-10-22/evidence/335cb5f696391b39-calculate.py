#!/usr/bin/env python3
"""MAINLINE-020: own arithmetic, no imported peer operator or third-party packages.

Run through simjob. INPUTS.json supplies the pinned evidence and explicit assumptions.
These screening calculations are estimates, not a qualified design or material basis.
"""
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def main():
    started, mono = utc(), time.monotonic()
    data = json.loads((ROOT / "INPUTS.json").read_text())
    checks = []
    for pin in data["input_pins"]:
        path = Path(pin["copy_path"])
        blob = path.read_bytes()
        assert len(blob) == pin["bytes"], path
        assert hashlib.sha256(blob).hexdigest() == pin["sha256"], path
    checks.append("All pinned input copies matched SHA-256 and size before arithmetic.")
    c = data["case"]
    radius, pressure, lift = c["radius_m"], c["pressure_Pa"], c["lift_kg"]
    area = 4 * math.pi * radius**2
    point = data["lead_point"]
    t, d = point["tf_m"], point["core_m"]
    be = data["faces"][0]
    core = data["lead_core"]
    nu = c["inherited_nu"]
    # Unique positive root of x^3+x=1: inherited equibiaxial interaction model.
    lo, hi = 0.0, 1.0
    for _ in range(64):
        mid = (lo + hi) / 2
        if mid**3 + mid < 1:
            lo = mid
        else:
            hi = mid
    biax = (lo + hi) / 2

    def modes(face, core_, tf=t, tc=d, nu_=nu, eta=1.0):
        """Reimplementation of the pinned screening equations, not peer code."""
        E, sig = face["E_Pa"], face["sigma_Pa"]
        h = tc + tf
        sigma0 = E * h / (radius * math.sqrt(1 - nu_**2))
        crimp = h**2 * core_["Gc_Pa"] / (2 * tf * tc)
        vc = sigma0 / crimp
        if vc <= 2:
            kc, gamma, branch = 1 - vc / 4, c["kd"], "stiff_or_moderate_core"
        else:
            kc, gamma, branch = 1 / vc, 1.0, "shear_crimping"
        demand = pressure * radius / (4 * tf)
        sfs = {
            "global_buckling": gamma * kc * sigma0 / demand,
            "core_shear_crimping": crimp / demand,
            "face_compression_or_joint_net_section": eta * sig / demand,
            "face_wrinkling": biax * 0.33 * E
            * math.sqrt(core_["Ec_Pa"] * tf / (E * tc)) / demand,
            "core_crush": core_["crush_Pa"] / (pressure / 2),
            "intracell_dimpling": 2 * E / (1 - nu_**2)
            * (tf / core_["s_cell_m"]) ** 2 / demand,
        }
        sf = min(sfs.values())
        governing = [k for k, v in sfs.items() if abs(v - sf) < 1e-10]
        return {"least_SF": sf, "sfs": sfs, "governing": governing,
                "Vc": vc, "Kc": kc, "gamma": gamma, "branch": branch,
                "membrane_compression_Pa": demand, "tf_m": tf, "core_m": tc,
                "tag": "QUESTIONABLE", "certification": "none"}

    mface = 2 * area * t * be["rho_kg_m3"]
    mcore = area * d * core["rho_kg_m3"]
    mstruct = mface + mcore
    joints = mstruct * c["joint_fraction"]
    total = mstruct + joints + c["systems_kg"]
    baseline = modes(be, core)
    assert abs(mface - point["expected_face_kg"]) < 1e-7
    assert abs(baseline["least_SF"] - point["expected_SF"]) < 1e-10
    assert abs((lift - total) / lift - 0.05) < 1e-10
    checks.append("Independently reproduced 009c5 face mass, least SF and 5% payload margin.")

    supply = []
    costs = []
    for scenario in data["procurement_scenarios"]:
        for name, mass in [("brief_reference_2100kg", 2100.0), ("pinned_lead_faces", mface)]:
            supply.append({
                "scenario": scenario["name"], "mass_basis": name,
                "finished_face_mass_kg": mass,
                "mine_output_year": scenario["output_year"],
                "world_mine_Be_content_kg": scenario["mine_output_kg"],
                "finished_share_percent": 100 * mass / scenario["mine_output_kg"],
                "assumed_fabrication_yield": scenario["yield"],
                "purchased_stock_kg": mass / scenario["yield"],
                "purchased_share_percent": 100 * mass / scenario["yield"] / scenario["mine_output_kg"],
                "tag": "QUESTIONABLE",
                "note": "Mine-content comparison, not measured finished-sheet capacity; no supply reservation.",
            })
            for grade in ["S200F", "SR200"]:
                unit = scenario[grade + "_USD_per_kg"]
                costs.append({
                    "scenario": scenario["name"], "mass_basis": name, "grade": grade,
                    "assumed_USD_per_kg": unit, "finished_mass_times_unit_price_USD": mass * unit,
                    "purchased_stock_cost_USD": mass / scenario["yield"] * unit,
                    "tag": "QUESTIONABLE", "basis": "Owner budget sensitivity, NOT a supplier price or market interval.",
                    "exclusions": "Forming, tooling, assembly, quality assurance, exposure controls, freight, tax; no scrap credit.",
                })

    panels = []
    for q in data["panel_scenarios"]:
        a, b = q["width_m"], q["length_m"]
        count = math.ceil(area / (a * b))
        # Mean-field shared-edge geometry, not a designed tessellation.
        seam = area * (1 / a + 1 / b)
        chord_radius = math.hypot(a, b) / 2
        sag = radius - math.sqrt(radius**2 - chord_radius**2)
        panels.append({
            **q, "panels_per_skin_area_lower_bound": count,
            "panel_pieces_both_skins_lower_bound": 2 * count,
            "mean_field_edge_joints_per_skin": 2 * count,
            "mean_field_edge_joints_both_skins": 4 * count,
            "coincident_hull_seam_m": seam, "skin_seam_m_both_skins": 2 * seam,
            "corner_sag_from_tangent_plane_m": sag,
            "through_thickness_bending_strain": t / (2 * radius),
            "double_curvature_metric_strain_scale": chord_radius**2 / (6 * radius**2),
            "note": "Flat rectangular area approximation, zero trim/lap allowance; sphere topology and final layout unresolved.",
        })
    # Nominal film masses are taken from 3M; carrier compatibility/coverage are assumptions.
    lbft2_to_kgm2 = 0.45359237 / 0.3048**2
    joins = []
    for panel in panels:
        for q in data["joint_scenarios"]:
            film = q["film_lb_ft2"] * lbft2_to_kgm2
            width = q["doubler_width_m"]
            # A hull seam means corresponding seams in both skins.
            # One Be strap per skin, one bond layer per strap, width across the whole seam.
            parts = {
                "Be_doublers": 2 * be["rho_kg_m3"] * t * width,
                "doubler_adhesive": 2 * film * width,
                "core_gap_paste": q["core_gap_m"] * d * q["paste_rho_kg_m3"],
                "sealant": q["sealant_cross_section_total_m2"] * q["paste_rho_kg_m3"],
            }
            per_m = sum(parts.values())
            full_film = 2 * area * film
            seam_mass = panel["coincident_hull_seam_m"] * per_m
            joining_mass = full_film + seam_mass
            # Replaces the existing 5% joints allowance, never adds it twice.
            new_total = mstruct + c["systems_kg"] + joining_mass
            eta_point = modes(be, core, eta=q["joint_efficiency"])
            joins.append({
                "panel": panel["name"], "joint": q["name"],
                "tag": "PROJECTION", "input_material_tag": "QUESTIONABLE",
                "film_kg_m2_per_interface": film,
                "full_area_face_core_film_kg": full_film,
                "per_hull_seam_m_kg_breakdown": parts, "kg_per_hull_seam_m": per_m,
                "seam_mass_kg": seam_mass, "total_joining_mass_kg": joining_mass,
                "replaces_joint_allowance_kg": joints,
                "additional_mass_over_allowance_kg": joining_mass - joints,
                "total_with_replacement_joining_kg": new_total,
                "remaining_payload_kg": lift - new_total,
                "payload_fraction": (lift - new_total) / lift,
                "assumed_joint_efficiency": q["joint_efficiency"],
                "joint_efficiency_only_SF": eta_point["least_SF"],
                "note": "No seam stiffness/buckling, peel, flaws, core node or leak qualification. No reoptimization after mass added.",
            })
    film_only = []
    for nominal in [0.015, 0.030, 0.045, 0.060]:
        mass = 2 * area * nominal * lbft2_to_kgm2
        film_only.append({
            "nominal_lb_ft2": nominal, "both_interfaces_kg": mass,
            "film_weight_tolerance_lb_ft2": 0.005,
            "mass_plus_minus_kg": 2 * area * 0.005 * lbft2_to_kgm2,
            "remaining_payload_if_only_film_replaces_5pct_joints_kg":
                lift - (mstruct + c["systems_kg"] + mass),
            "tag": "QUESTIONABLE",
        })
    braze = []
    for q in data["braze_scenarios"]:
        # Two skins; one assumed added bead cross-section per skin.
        per_m = 2 * q["added_area_per_skin_m2"] * q["filler_rho_kg_m3"]
        braze.append({**q, "kg_per_hull_seam_m_filler_only": per_m,
                      "filler_mass_large_panel_kg": per_m * panels[0]["coincident_hull_seam_m"],
                      "joint_efficiency_only_SF": modes(be, core, eta=q["joint_efficiency"])["least_SF"],
                      "note": "Filler-only floor: no straps, lands, repairs or fixtures; no proven thin-shell butt joint. Braze before adding organic core/adhesive."})
    tolerance = []
    for offset in [-data["gauge_tolerance_m"], 0, data["gauge_tolerance_m"]]:
        tf = t + offset
        fmass = 2 * area * tf * be["rho_kg_m3"]
        tol_total = (fmass + mcore) * (1 + c["joint_fraction"]) + c["systems_kg"]
        tolerance.append({
            "uniform_offset_m": offset, "face_mass_kg": fmass,
            "face_mass_change_kg": fmass - mface,
            "remaining_payload_if_uniform_kg": lift - tol_total,
            "modes_at_local_gauge": modes(be, core, tf=tf),
            "tag": "QUESTIONABLE",
            "note": "Uniform gauge mass sensitivity; a local low spot does not imply whole-shell mass savings.",
        })
    mechanical = []
    for q in data["mechanical_scenarios"]:
        f = {**be, "E_Pa": q["E_Pa"], "sigma_Pa": q["compression_proxy_Pa"]}
        mechanical.append({**q, "modes": modes(f, core, nu_=q["nu"]),
                           "note": "Sensitivity only; compression proxies and scalar anisotropy are not SR200 allowables."})
    thermal = []
    for q in data["thermal_scenarios"]:
        E = data["current_sheet_E_Pa"]
        lam = math.sqrt(core["Gc_Pa"] / (E * t * d))
        mismatch = q["delta_alpha_per_K"] * q["delta_T_K"]
        thermal.append({
            **q, "shear_lag_lambda_per_m": lam, "transfer_length_m": 1 / lam,
            "long_joint_peak_shear_Pa": abs(mismatch) * E * t * lam,
            "fully_restrained_uniaxial_thermal_stress_Pa": E * abs(mismatch),
            "fully_restrained_biaxial_proxy_Pa": E * abs(mismatch) / (1 - 0.08),
            "qualified_daily_thermal_life_cycles": None,
            "note": "016 scalar long-joint screen rederived for Be/HRH10; actual effective core CTE, restraint and shear strength are unknown.",
        })
    # Fixed-geometry substitution uses the same core, tf, tc and pressure.
    alternatives = []
    for face in data["faces"]:
        evaluated = modes(face, core)
        fm = 2 * area * t * face["rho_kg_m3"]
        tot = (fm + mcore) * (1 + c["joint_fraction"]) + c["systems_kg"]
        alternatives.append({
            "face": face["name"], "tag": face["tag"], "Be_free": face["Be_free"],
            "geometry": "Exact 009c5 tf and core; same 5%-of-structure joint formula",
            "modes": evaluated, "face_mass_kg": fm, "remaining_payload_kg": lift - tot,
            "SF_lost_absolute_vs_lead": baseline["least_SF"] - evaluated["least_SF"],
            "SF_lost_percent_vs_lead": 100 * (1 - evaluated["least_SF"] / baseline["least_SF"]),
        })
    # Independent arithmetic at each published 014b geometry, without reoptimizing.
    published = []
    reference = data["published_014b"][0]["expected_SF"]
    for q in data["published_014b"]:
        face = next(f for f in data["faces"] if f["name"] == q["face"])
        evaluated = modes(face, q["core"], tf=q["tf_m"], tc=q["core_m"])
        assert abs(evaluated["least_SF"] - q["expected_SF"]) < 1e-10
        published.append({
            "face": q["face"], "core": q["core"]["name"], "tag": "QUESTIONABLE",
            "Be_free": face["Be_free"], "reported_SF": q["expected_SF"],
            "recomputed_SF": evaluated["least_SF"],
            "loss_absolute_vs_014b_Be": reference - evaluated["least_SF"],
            "loss_percent_vs_014b_Be": 100 * (1 - evaluated["least_SF"] / reference),
            "tf_m": q["tf_m"], "core_m": q["core_m"],
            "basis": "Same P2 zero-payload float ceiling; each has its own geometry and possibly core.",
        })
    checks.append("Reproduced all four selected 014b mode minima at their published geometries.")
    # The +5%-payload-line comparison retains each published core and mass split.
    # This is uniform resizing, not a fresh optimization.
    resized = []
    scale = mstruct / data["published_014b_structural_mass_kg"]
    for q in data["published_014b"]:
        face = next(f for f in data["faces"] if f["name"] == q["face"])
        ev = modes(face, q["core"], tf=q["tf_m"] * scale, tc=q["core_m"] * scale)
        resized.append({"face": face["name"], "core": q["core"]["name"],
                        "tag": "QUESTIONABLE", "Be_free": face["Be_free"],
                        "modes": ev, "scale": scale,
                        "basis": "Uniformly resized published geometry onto 009c5 structural budget; no reoptimization."})
    checks.append("Joining totals replace the 5% allowance; both skins and both core interfaces are counted.")
    assert all(x["mean_field_edge_joints_both_skins"] == 2 * x["mean_field_edge_joints_per_skin"] for x in panels)
    assert abs(joins[0]["total_joining_mass_kg"] - joins[0]["seam_mass_kg"] - joins[0]["full_area_face_core_film_kg"]) < 1e-8
    assert be["Be_free"] is False and data["faces"][-1]["Be_free"] is False
    checks.append("Panel/skin counting and joining mass closure assertions passed.")
    results = {
        "schema": 1, "card": "MAINLINE-020",
        "unit": "vacuum-mainline020-beryllium-reality-1019",
        "status": "ESTIMATE", "tag": "QUESTIONABLE", "certification": "none",
        "scope": "Materials/manufacturing reality and own sensitivity calculations; no physical validation.",
        "baseline": {
            "radius_m": radius, "area_one_skin_m2": area, "pressure_Pa": pressure,
            "lift_kg": lift, "face_mass_kg": mface, "core_mass_kg": mcore,
            "structural_mass_kg": mstruct, "joint_allowance_kg": joints,
            "total_kg": total, "payload_kg": lift - total, "modes": baseline,
            "capacity_gap_to_SF1_fraction": 1 - baseline["least_SF"],
            "capacity_factor_needed_for_SF1": 1 / baseline["least_SF"],
            "brief_face_mass_kg": 2100.0, "brief_mass_error_kg": mface - 2100,
            "brief_mass_understatement_percent_of_reference": 100 * (mface / 2100 - 1),
        },
        "annual_supply": supply, "cost_scenarios": costs,
        "panel_scenarios": panels, "joining_scenarios": joins,
        "film_only_scenarios": film_only, "braze_scenarios": braze,
        "thickness_tolerance": tolerance, "mechanical_sensitivities": mechanical,
        "thermal_sensitivities": thermal,
        "daily_cycles_assumed_30_years": math.ceil(30 * 365.25),
        "fatigue_benchmark": {
            "S200F_smooth_R_minus_1_stress_amplitude_MPa": [262, 266],
            "cycles": 10000000, "source": "S07",
            "tag": "QUESTIONABLE",
            "transfer": "Not an SR200 bonded-joint thermal-cycle allowable. Life at the hull's compressive mean stress is unknown.",
        },
        "fixed_geometry_alternatives": alternatives,
        "published_equal_ceiling_alternatives": published,
        "resized_5pct_margin_alternatives": resized,
        "ranking_by_effect_on_lead": [
            "1: Installed face-core bonds plus seams: mass and actual joint capacity.",
            "2: Purchasable gauge, panel size and formed geometry: local strength and mass.",
            "3: Grade/orientation/post-form compression and elastic basis.",
            "4: Thermal mismatch and joint fatigue at nonzero mean load.",
            "5: Beryllium-free K13D2U laminate feasibility and honest SF trade.",
            "6: Procurement price, finished-sheet capacity and controlled-process cost.",
        ],
        "first_two_to_ground": [
            "A weighed, sealed, representative two-skin joint/core panel with measured load transfer, flaws and curvature.",
            "A supplier-confirmed 0.75-0.79 mm SR200 panel specification with gauge map and post-form biaxial/compression coupon basis.",
        ],
        "limitations": [
            "All sourced, inherited and assumed real-material values remain QUESTIONABLE.",
            "Unverified panel availability and engineered joining configurations are PROJECTION.",
            "No change to the inherited crimp-branch gamma=1 or wrinkling core-modulus assumption.",
            "No material/joint qualification, supplier quotation, fabrication or flight-readiness claim.",
            "Published alternatives are QI laminate estimates, not single-fiber properties or manufactured-shell allowables.",
        ],
        "checks": checks,
        "measurement": {
            "started_utc": started, "ended_utc": utc(),
            "elapsed_seconds": time.monotonic() - mono,
            "pid": os.getpid(), "cgroup": Path("/proc/self/cgroup").read_text(),
            "budget": None, "phase_cap": None,
            "note": "Measurement only. simjob timeout is a technical watchdog, not a task budget.",
        },
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "status": "ESTIMATE", "baseline_face_kg": mface,
        "baseline_least_SF": baseline["least_SF"], "checks": len(checks),
        "elapsed_seconds": results["measurement"]["elapsed_seconds"],
        "results": str(ROOT / "RESULTS.json"),
    }))


if __name__ == "__main__":
    main()
