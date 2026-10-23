"""MAINLINE-028: independent mass accounting and one-core mass-line optimization.

Run with Python 3 from any directory. Reads the frozen INPUTS.json beside this
file. No inherited executable is imported. All SF results are continuum screens:
the installed core bond has UNKNOWN strength and is not certified by this model.
"""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "INPUTS.json").read_text())
C = I["case"]
P, R, LIFT = C["p_Pa"], C["R_m"], C["lift_kg"]
A = 4 * math.pi * R**2
N = P * R / 4  # force per unit width in EACH of the two equally loaded faces
E, NU, RHO, SIGMA = C["E_Pa"], C["nu"], C["rho_face"], C["sigma_face_Pa"]
EC, GC, RHOC = C["Ec_Pa"], C["Gc_Pa"], C["rho_core"]
B = C["joint_allowance_kg"]
STRUCTURE_PLUS_JOINING = (1 - C["margin_fraction"]) * LIFT - C["systems_kg"]
PSF = 0.45359237 / 0.3048**2


def modes(tf, tc, gamma, wrinkle, weld_retention=1.0):
    """Re-derived six-mode equations, retaining the pinned 021 conventions."""
    h = tf + tc
    sigma0 = E * h / (R * math.sqrt(1 - NU**2))
    crimp = h*h * GC / (2*tf*tc)
    vc = sigma0 / crimp
    kc = 1-vc/4 if vc <= 2 else 1/vc
    demand = N/tf
    sf = {
        "global_buckling": gamma * kc * sigma0 / demand,
        "face_compression": SIGMA / demand,
        "core_shear_crimping": crimp / demand,
        "core_crush_inherited": C["crush_Pa"]/(P/2),
        "face_wrinkling": C["biaxial_factor"]*wrinkle*math.sqrt(E*EC*tf/tc)/demand,
        "intracell_dimpling": E/(1-NU**2)*(tf/C["cell_m"])**2/demand,
    }
    if weld_retention < 1:
        sf["projected_weld_compression"] = weld_retention * SIGMA / demand
    return {"sfs": sf, "least_known_mode_SF": min(sf.values()),
            "governing": min(sf, key=sf.get), "Vc": vc, "Kc": kc}


def geometry(m, f):
    return (1-f)*m/(2*A*RHO), f*m/(A*RHOC)


def joining(tf, tc, panel, route):
    a, b = panel["a_m"], panel["b_m"]
    seam = route["seam"]
    overlap = 30*tf if seam == "scarf" else 3*tf if seam == "braze_scarf" else 0
    # Treat named panel dimensions as raw blanks; account for scarf overlap.
    length = A*(1/(a-overlap) + 1/(b-overlap))
    mu = {"face_joint_metal": 0.0, "face_joint_adhesive": 0.0,
          "face_joint_braze": 0.0, "core_splice": 0.0005*tc*500,
          "sealing": 0.002}
    if seam == "scarf":
        mu["face_joint_adhesive"] = 2*tf*math.sqrt(1+30**2)*0.070
    elif seam == "strap":
        width = 2*N/10e6
        mu["face_joint_metal"] = 2*RHO*tf*width
        mu["face_joint_adhesive"] = 2*width*0.070
    elif seam == "braze_scarf":
        mu["face_joint_braze"] = 2*tf*math.sqrt(1+3**2)*50e-6*2700
    elif seam == "legacy_020":
        mu = {"face_joint_metal": 2*RHO*tf*0.06,
              "face_joint_adhesive": 2*0.06*0.030*PSF,
              "face_joint_braze": 0.0,
              "core_splice": 0.001*tc*1100, "sealing": 0.011}
    elif seam != "eb":
        raise ValueError(seam)
    bond = 2*A*route["bond_kg_m2"]
    primer = 2*A*route.get("primer_kg_m2", 0)
    total = bond + primer + length*sum(mu.values())
    return {"bond_kg": bond, "primer_kg": primer,
            "seam_length_m": length, "skin_seam_length_m": 2*length,
            "scarf_overlap_m": overlap, "mu_kg_m": mu,
            "mu_total_kg_m": sum(mu.values()),
            "seams_kg": length*sum(mu.values()), "total_kg": total,
            "budget_fraction": total/B, "remaining_budget_kg": B-total,
            "margin_at_this_geometry_kg":
                LIFT-(2*A*RHO*tf+A*RHOC*tc+C["systems_kg"]+total)}


def point(f, panel, route):
    # Bisection solves structural mass + geometry-dependent joining = mass line.
    lo, hi = 0.0, STRUCTURE_PLUS_JOINING
    for _ in range(43):
        m = (lo+hi)/2
        tf, tc = geometry(m, f)
        j = joining(tf, tc, panel, route)
        if m+j["total_kg"] > STRUCTURE_PLUS_JOINING:
            hi = m
        else:
            lo = m
    m = (lo+hi)/2
    tf, tc = geometry(m, f)
    ev = modes(tf, tc, C["gamma_needed"], C["wrinkle_needed"],
               route.get("weld_retention", 1.0))
    demand = N/tf
    # Additional seam screens remain PROJECTION, not measured allowables.
    if route["seam"] == "scarf":
        ev["sfs"]["projected_scarf_average_shear"] = 10e6/(demand*30/(1+30**2))
    elif route["seam"] == "braze_scarf":
        ev["sfs"]["projected_braze_average_shear"] = 103.4e6/(demand*3/10)
    elif route["seam"] == "legacy_020":
        ev["sfs"]["projected_joint_retention"] = 0.9*SIGMA/demand
    ev["least_known_mode_SF"] = min(ev["sfs"].values())
    ev["governing"] = min(ev["sfs"], key=ev["sfs"].get)
    return {"core_mass_fraction": f, "tf_m": tf, "tc_m": tc,
            "structural_mass_kg": m, "joining": joining(tf, tc, panel, route),
            "evaluation": ev,
            "mass_residual_kg": m+joining(tf, tc, panel, route)["total_kg"]
                               - STRUCTURE_PLUS_JOINING}


def optimize(panel, route, grid=500):
    # Search all fractions, then refine the best cell; no one-sided start.
    fs = [0.001 + i*0.998/grid for i in range(grid+1)]
    scores = [point(f, panel, route)["evaluation"]["least_known_mode_SF"] for f in fs]
    k = max(range(len(fs)), key=scores.__getitem__)
    lo, hi = fs[max(0,k-1)], fs[min(grid,k+1)]
    for _ in range(60):
        u, v = lo+(hi-lo)/3, hi-(hi-lo)/3
        su = point(u,panel,route)["evaluation"]["least_known_mode_SF"]
        sv = point(v,panel,route)["evaluation"]["least_known_mode_SF"]
        if su < sv:
            lo = u
        else:
            hi = v
    return point((lo+hi)/2, panel, route)


def main():
    started = datetime.now(timezone.utc).isoformat()
    baseline = modes(C["tf_m"], C["tc_m"], C["gamma_needed"], C["wrinkle_needed"])
    cases = []
    for panel in I["panels"]:
        for route in I["routes"]:
            cases.append({"panel": panel["id"], "route": route["id"],
                          "tag": "PROJECTION", "bond_strength_qualified": False,
                          "fixed_geometry": joining(C["tf_m"], C["tc_m"], panel, route),
                          "reoptimized_5pct_margin": optimize(panel, route)})
    films = [{"id": x["id"], "kg_m2_per_line": x["kg_m2"],
              "two_bond_lines_kg": 2*A*x["kg_m2"],
              "fraction_of_joining_allowance": 2*A*x["kg_m2"]/B}
             for x in I["bond_routes"] if x.get("kg_m2") is not None]
    demands = {
        "hull_membrane_N_m": 2*N, "per_face_membrane_N_m": N,
        "face_compression_Pa": N/C["tf_m"],
        "ideal_radial_compression_Pa": P/2,
        "ideal_interface_shear_Pa": 0,
        "ideal_flatwise_tension_Pa": 0,
        "note": "The zero base-state stresses do not bound imperfection, thermal, seam or wrinkle stresses.",
        "relative_displacement_screens": [
            {"delta_m": d, "normal_Pa": EC*d/C["tc_m"],
             "shear_W_Pa": GC*d/C["tc_m"]} for d in (1e-5, 5e-5, 1e-4)],
        "core_shear_target_W_typical_Pa": 35*6894.757293168,
        "core_shear_target_W_min_average_Pa": 25*6894.757293168,
        "core_shear_target_L_typical_Pa": 55*6894.757293168,
        "core_shear_target_L_min_average_Pa": 45*6894.757293168,
        "scarf30_shear_Pa": N/C["tf_m"]*30/901,
        "scarf30_normal_compression_Pa": N/C["tf_m"]/901,
        "braze_scarf3_shear_Pa": N/C["tf_m"]*3/10,
        "bare_weld_required_retention": N/(C["tf_m"]*SIGMA),
    }
    budgets = []
    for panel in I["panels"]:
        length=A*(1/panel["a_m"]+1/panel["b_m"])
        budgets.append({"panel":panel["id"],"zero_trim_seam_m":length,
                        "max_total_seam_kg_m_after_AF015": (B-2*A*0.015*PSF)/length,
                        "max_total_seam_kg_m_after_8gsm": (B-2*A*.008)/length})
    validations = {
        "baseline_least_SF_equals_one": abs(baseline["least_known_mode_SF"]-1)<1e-10,
        "baseline_all_six_modes_reproduced": all(
            abs(baseline["sfs"][k]-v) < 1e-9
            for k,v in C["baseline_mode_SFs"].items()),
        "film_conversion_matches_020": abs(2*A*.015*PSF-184.0631855297372)<1e-8,
        "baseline_mass_balances": abs(C["structural_mass_kg"]+B-
                                      STRUCTURE_PLUS_JOINING)<1e-8,
        "all_optimized_mass_residuals_under_microgram":
            max(abs(x["reoptimized_5pct_margin"]["mass_residual_kg"]) for x in cases)<1e-9,
        "all_reoptimized_points_retain_five_percent_margin": all(
            abs(x["reoptimized_5pct_margin"]["joining"]["margin_at_this_geometry_kg"]
                - C["margin_fraction"]*LIFT)<1e-8 for x in cases),
        "same_panel_more_film_never_improves_SF": True,
    }
    # A denser independent scan must reproduce the optimum on the critical nominal
    # stock-size case. Refinement is bounded to the winning grid interval.
    p=I["panels"][1]; r=next(x for x in I["routes"] if x["id"]=="af015_scarf")
    fine=optimize(p,r,grid=2000)
    coarse=next(x for x in cases if x["panel"]==p["id"] and x["route"]==r["id"])
    err=abs(fine["evaluation"]["least_known_mode_SF"]-
            coarse["reoptimized_5pct_margin"]["evaluation"]["least_known_mode_SF"])
    validations["denser_grid_agrees_within_1e_7_SF"]=err<1e-7
    for p in I["panels"]:
        rows={x["route"]:x for x in cases if x["panel"]==p["id"]}
        vals=[rows[r]["reoptimized_5pct_margin"]["evaluation"]["least_known_mode_SF"]
              for r in ["lab8_scarf","lab20_scarf","hex70_scarf","af015_scarf",
                        "hex100_scarf","af030_scarf"]]
        if any(b>a+1e-8 for a,b in zip(vals,vals[1:])):
            validations["same_panel_more_film_never_improves_SF"]=False
    output={"schema":1,"card":"MAINLINE-028","unit":I["unit"],
            "status":"ESTIMATE","tag":"QUESTIONABLE / PROJECTION",
            "certification":False,"overall_installed_hull_SF":None,
            "overall_SF_reason":"Core-bond, seam, thermal and defect allowables are unmeasured.",
            "job_started_at":I["job_started_at"],"calculation_started_at":started,
            "calculation_ended_at":datetime.now(timezone.utc).isoformat(),
            "case":C,"area_m2":A,"mass_budget_bonds_only_kg_m2_per_line":B/(2*A),
            "demands":demands,"bond_masses":films,"seam_budget":budgets,
            "baseline_reproduction":baseline,
            "baseline_at_kd_0p2":modes(C["tf_m"],C["tc_m"],.2,C["wrinkle_needed"]),
            "cases":cases,"validation":validations,
            "scope":"Reoptimization holds the 021-rev1 material, core and the two needed optimism constants fixed. It does not reoptimize material grades or transfer the 006 aluminium-shell slope."}
    (ROOT/"RESULTS.json").write_text(json.dumps(output,indent=2)+"\n")
    (ROOT/"VALIDATION.json").write_text(json.dumps({
        "all_passed":all(validations.values()),"checks":validations,
        "denser_grid_absolute_SF_error":err,
        "calculation_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    },indent=2)+"\n")
    assert all(validations.values()), validations
    print(json.dumps({"checks":validations,"cases":len(cases)}))
    for x in cases:
        if x["panel"] in ["stock_envelope","4m_projection"]:
            print(x["panel"],x["route"],
                  round(x["fixed_geometry"]["total_kg"],3),
                  round(x["reoptimized_5pct_margin"]["evaluation"]["least_known_mode_SF"],6))


if __name__ == "__main__":
    main()
