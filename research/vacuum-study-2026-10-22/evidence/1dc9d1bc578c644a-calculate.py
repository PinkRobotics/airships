"""MAINLINE-028b: independent joint-aware reconstruction of the 021b search.

Run `python3 calculate.py` beside frozen INPUTS.json. Requires numpy and scipy.
No inherited executable is imported or run. All reported SFs are conditional
screens; an installed-hull SF remains unknown without bond/seam allowables.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "INPUTS.json").read_text())
C, K = I["case"], I["constants"]
R, P, LIFT = C["R_m"], C["p0_Pa"], C["lift0_kg"]
A, NU = 4 * math.pi * R**2, I["nu"]
N = P * R / 4
FIXED, SYS, J = (C["reserve_fixed_items_kg"],
                 C["systems_allowance_kg"], C["joint_fraction"])
BUDGET = LIFT - FIXED - SYS
BIAX = brentq(lambda x: x**3+x-1, 0, 1, xtol=1e-15)
NAMES = ("O1_gamma", "O2_wrinkle", "O3_SR200_face_strength")
MODE_NAMES = ("global_buckling", "face_compression", "core_shear_crimping",
              "core_crush", "face_wrinkling", "intracell_dimpling")


def joining(tf, tc, route):
    overlap = K["scarf_ratio"] * tf if route["seam"] == "scarf" else 0 * tf
    length = A * (1 / (I["panel"]["a_m"]-overlap)
                  + 1 / (I["panel"]["b_m"]-overlap))
    scarf_mu = (2 * tf * math.hypot(1, K["scarf_ratio"])
                * K["scarf_film_kg_m2"] if route["seam"] == "scarf" else 0 * tf)
    core_mu = K["core_splice_gap_m"] * tc * K["core_splice_density_kg_m3"]
    seal_mu = K["seal_both_faces_kg_m"]
    bond = 2*A*route["bond_kg_m2"]
    primer = 2*A*route.get("primer_kg_m2", 0)
    return {"bond_kg": bond, "primer_kg": primer,
            "scarf_film_kg": length*scarf_mu,
            "core_splice_kg": length*core_mu,
            "seal_kg": length*seal_mu, "seam_length_m": length,
            "scarf_overlap_m": overlap,
            "physical_total_kg": bond+primer+length*(scarf_mu+core_mu+seal_mu)}


def geometry(core, f, route, frozen_joining=None):
    f = np.asarray(f, dtype=float)
    lo, hi = np.zeros_like(f), np.full_like(f, BUDGET/(1+J))
    for _ in range(48):
        s = (lo+hi)/2
        tf, tc = (1-f)*s/(2*A*1850), f*s/(A*core["rho"])
        physical = joining(tf, tc, route)["physical_total_kg"]
        charge = np.maximum(J*s, physical if frozen_joining is None else frozen_joining)
        over = s+charge > BUDGET
        hi, lo = np.where(over, s, hi), np.where(over, lo, s)
    s = (lo+hi)/2
    tf, tc = (1-f)*s/(2*A*1850), f*s/(A*core["rho"])
    joint = joining(tf, tc, route)
    physical = joint["physical_total_kg"] if frozen_joining is None else frozen_joining
    charge = np.maximum(J*s, physical)
    return {"S": s, "tf": tf, "tc": tc, "joining": joint,
            "charged_joining": charge, "excess": np.maximum(0, physical-J*s),
            "unused_joint_allowance": np.maximum(0, J*s-physical),
            "residual": s+charge+FIXED+SYS-LIFT}


def modes(core, tf, tc, E, sigma, gamma=None, wrinkle=.33):
    h, demand = tf+tc, N/tf
    sigma0 = E*h/(R*math.sqrt(1-NU*NU))
    crimp = h*h*core["Gc_Pa"]/(2*tf*tc)
    vc = sigma0/crimp
    kc = np.where(vc <= 2, 1-vc/4, 1/vc)
    gamma0 = np.where(vc < 2, .2, 1.)
    if gamma is None:
        gamma = gamma0
    sf = {"global_buckling": gamma*kc*sigma0/demand,
          "face_compression": sigma/demand,
          "core_shear_crimping": crimp/demand,
          "core_crush": np.ones_like(tf)*core["crush_Pa"]/(P/2),
          "face_wrinkling": BIAX*wrinkle*np.sqrt(E*core["Ec_Pa"]*tf/tc)/demand,
          "intracell_dimpling": E/(1-NU*NU)*(tf/core["s_cell_m"])**2/demand}
    return {"sfs": sf, "Vc": vc, "Kc": kc, "demand": demand,
            "gamma_today": gamma0, "gamma_full": .2+.4*np.minimum(vc, 2)}


def log_usage(need, today, full):
    need, today, full = np.broadcast_arrays(need, today, full)
    with np.errstate(divide="ignore", invalid="ignore"):
        raw = np.log(need/today)/np.log(full/today)
    return np.where(need <= today*(1+1e-13), 0.,
                    np.where(full > today*(1+1e-13), raw, np.inf))


def arrays(core, f, route, material, enforce_joint=True, frozen_joining=None):
    g = geometry(core, f, route, frozen_joining)
    ev = modes(core, g["tf"], g["tc"], material["E_Pa"], material["sigma_today_Pa"])
    sfs = ev["sfs"]
    gamma_need = ev["gamma_today"]/sfs["global_buckling"]
    wrinkle_need = .33/sfs["face_wrinkling"]
    u = (log_usage(gamma_need, ev["gamma_today"], ev["gamma_full"]),
         log_usage(wrinkle_need, .33, .82),
         log_usage(ev["demand"], material["sigma_today_Pa"], material["sigma_full_Pa"]))
    hard = [sfs[k] for k in ("core_shear_crimping", "core_crush", "intracell_dimpling")]
    if not material["face_optimism_allowed"]:
        hard.append(sfs["face_compression"])
    if enforce_joint and route["seam"] == "scarf":
        hard.append(K["scarf_mean_shear_screen_Pa"] /
                    (ev["demand"]*K["scarf_ratio"]/(1+K["scarf_ratio"]**2)))
    return g, ev, u, np.minimum.reduce(hard)


def subset_score(data, subset):
    _, ev, u, hard = data
    # Unselected factors remain at today's values, so exact feasibility can be
    # rooted in mode SF rather than in the flat zero part of log_usage.
    constraints = [hard]
    for k, mode in enumerate(("global_buckling", "face_wrinkling", "face_compression")):
        if k not in subset:
            constraints.append(ev["sfs"][mode])
    slack = np.minimum.reduce(constraints)-1
    objective = np.maximum.reduce([u[k] for k in subset]) if subset else 0*slack
    return objective, slack


def best_on_curve(core, route, material, subset, enforce_joint, grid, frozen_joining=None,
                  sampled_curve=None):
    if sampled_curve is None:
        f = np.linspace(1e-6, 1-1e-6, grid+1)
        data = arrays(core, f, route, material, enforce_joint, frozen_joining)
    else:
        f, data = sampled_curve
    score, slack = subset_score(data, subset)
    valid = (slack >= -1e-12) & np.isfinite(score)
    if not np.any(valid):
        return None
    # Find every sampled local minimum and each feasible interval boundary.
    left = np.r_[False, valid[:-1]]
    right = np.r_[valid[1:], False]
    masked = np.where(valid, score, np.inf)
    candidates = np.flatnonzero(valid & ((masked <= np.r_[np.inf, masked[:-1]])
                                         & (masked <= np.r_[masked[1:], np.inf])
                                         | ~left | ~right))
    # A flat score contributes only its boundary plus the global grid optimum.
    if len(candidates) > 80:
        candidates = np.unique(np.r_[np.flatnonzero(valid & (~left | ~right)),
                                     np.argmin(masked)])

    def scalar(x):
        s, t = subset_score(arrays(core, x, route, material, enforce_joint,
                                  frozen_joining), subset)
        return float(s), float(t)

    best = (float(np.min(masked)), float(f[np.argmin(masked)]))
    for idx in candidates:
        lo, hi = f[max(0, idx-1)], f[min(grid, idx+1)]
        for side, x in (("lo", lo), ("hi", hi)):
            if scalar(x)[1] < 0:
                try:
                    boundary = brentq(lambda y: scalar(y)[1], x, f[idx],
                                      xtol=1e-14)
                except ValueError:
                    continue
                if side == "lo":
                    lo = boundary
                else:
                    hi = boundary
        if hi <= lo:
            continue
        opt = minimize_scalar(lambda x: scalar(x)[0] if scalar(x)[1] >= -1e-11
                              else 1e6, bounds=(lo, hi), method="bounded",
                              options={"xatol": 2e-14})
        for x in (lo, hi, float(opt.x)):
            value, constraint = scalar(x)
            if constraint >= -1e-10 and value < best[0]:
                best = value, x
    return {"usage": best[0], "fraction": best[1], "core": core["name"]}


def describe(core, f, route, material, enforce_joint=True, frozen_joining=None):
    g, ev, u, hard = arrays(core, f, route, material, enforce_joint, frozen_joining)
    need = {"gamma": float(max(ev["gamma_today"],
                              ev["gamma_today"]/ev["sfs"]["global_buckling"])),
            "wrinkle": float(max(.33, .33/ev["sfs"]["face_wrinkling"])),
            "face_strength_Pa": float(max(material["sigma_today_Pa"], ev["demand"]))}
    def at(E, sigma, gamma, wrinkle):
        e = modes(core, g["tf"], g["tc"], E, sigma, gamma, wrinkle)
        sf = {k:float(v) for k,v in e["sfs"].items()}
        seam = (K["scarf_mean_shear_screen_Pa"] /
                (float(e["demand"])*K["scarf_ratio"]/(1+K["scarf_ratio"]**2))
                if route["seam"] == "scarf" else
                route.get("weld_retention", 1.)*sigma/float(e["demand"]))
        return {"six_modes":sf, "least_six_mode_SF":min(sf.values()),
                "projected_seam_mode": ("scarf_mean_shear" if route["seam"]=="scarf"
                                        else "ideal_weld_compression"),
                "projected_seam_SF":seam,
                "least_seven_screen_SF":min(min(sf.values()),seam)}
    joint = {k:float(v) for k,v in g["joining"].items()}
    S, tf, tc = float(g["S"]),float(g["tf"]),float(g["tc"])
    masses = {"faces":2*A*1850*tf,"core":A*core["rho"]*tc,
              "structural":S,"physical_joining":joint["physical_total_kg"],
              "base_joint_allowance":J*S,"charged_joining":float(g["charged_joining"]),
              "joint_excess":float(g["excess"]),"unused_joint_allowance":float(g["unused_joint_allowance"]),
              "systems":SYS,"fixed_reserve":FIXED,"total_reserve":FIXED+float(g["excess"]),
              "charged_total":S+float(g["charged_joining"])+SYS+FIXED,
              "physical_total_including_fixed_reserve":S+joint["physical_total_kg"]+SYS+FIXED,
              "lift":LIFT,"residual":float(g["residual"])}
    fullE, fullSigma = material["E_full_Pa"],material["sigma_full_Pa"]
    fullvc = modes(core,tf,tc,fullE,fullSigma)["Vc"]
    return {"core":core,"fraction":f,"tf_m":tf,"tc_m":tc,"nu":NU,"Vc":float(ev["Vc"]),
            "Kc":float(ev["Kc"]),"face_demand_Pa":float(ev["demand"]),
            "masses_kg":masses,"joining":joint,"needed":need,
            "factor_vs_today":{"gamma":need["gamma"]/float(ev["gamma_today"]),
                               "wrinkle":need["wrinkle"]/.33,
                               "face":need["face_strength_Pa"]/material["sigma_today_Pa"],
                               "panel":1.0,"film_mass_reduction_vs_003":.03*(.45359237/.09290304)/route["bond_kg_m2"]},
            "log_usage":dict(zip(NAMES,[float(x) if np.isfinite(x) else None for x in u])),
            "needed_face_within_named":need["face_strength_Pa"] <= material["sigma_full_Pa"]*(1+1e-12),
            "full_gamma_at_search_E":float(ev["gamma_full"]),
            "at_needed":at(material["E_Pa"],need["face_strength_Pa"],need["gamma"],need["wrinkle"]),
            "today":at(material["E_Pa"],material["sigma_today_Pa"],float(ev["gamma_today"]),.33),
            "at_full_named":at(fullE,fullSigma,float(.2+.4*min(fullvc,2)),.82),
            "at_full_but_gamma_02":at(fullE,fullSigma,.2,.82),
            "S200F255_at_same_geometry":at(290e9,255e6,need["gamma"],need["wrinkle"]),
            "weld_retention_required_at_today_strength":float(ev["demand"])/material["sigma_today_Pa"] if route["seam"]=="eb" else None,
            "overall_installed_SF":None,
            "unquantified_modes":["face/core flatwise tension","face/core shear including imperfections",
                                  "scarf peel or weld/HAZ and brittle seam failure",
                                  "seam/local buckling","thermal and cyclic debonding",
                                  "leak-tightness and defects"],
            "joint_screen_enforced":enforce_joint,
            "frozen_joining_charge_sensitivity":frozen_joining}


def search(route, material, enforce_joint=True, grid=6000, frozen_joining=None):
    names = range(3 if material["face_optimism_allowed"] else 2)
    subsets = [s for n in range(len(names)+1) for s in itertools.combinations(names,n)]
    best = {s:None for s in subsets}
    for core in I["cores"]:
        f=np.linspace(1e-6,1-1e-6,grid+1)
        sampled=(f,arrays(core,f,route,material,enforce_joint,frozen_joining))
        for subset in subsets:
            pt = best_on_curve(core,route,material,subset,enforce_joint,grid,frozen_joining,sampled)
            if pt is not None and (best[subset] is None or pt["usage"] < best[subset]["usage"]):
                best[subset] = pt
    rows=[]
    for subset in subsets:
        pt=best[subset]
        rows.append({"subset":[NAMES[k] for k in subset],
                     "min_max_usage":pt["usage"] if pt else None,
                     "feasible_within_named":pt is not None and pt["usage"] <= 1+1e-10,
                     "point":pt})
    feasible=[x for x in rows if x["feasible_within_named"]]
    least=min(feasible,key=lambda x:(len(x["subset"]),x["min_max_usage"])) if feasible else None
    result={"route":route["id"],"material":material["id"],
            "nu":NU,"joint_screen_enforced":enforce_joint,"subsets":rows,"least_set":least}
    if least:
        core=next(c for c in I["cores"] if c["name"]==least["point"]["core"])
        result["floating_point"]=describe(core,least["point"]["fraction"],route,material,
                                          enforce_joint,frozen_joining)
    return result


def maximize_full(route, material, enforce_joint=True, grid=6000):
    best=None
    for core in I["cores"]:
        def score(f):
            g=geometry(core,f,route)
            e=modes(core,g["tf"],g["tc"],material["E_full_Pa"],material["sigma_full_Pa"])
            e=modes(core,g["tf"],g["tc"],material["E_full_Pa"],material["sigma_full_Pa"],
                    e["gamma_full"],.82)
            vals=list(e["sfs"].values())
            if enforce_joint and route["seam"]=="scarf":
                vals.append(K["scarf_mean_shear_screen_Pa"] /
                            (e["demand"]*K["scarf_ratio"]/(1+K["scarf_ratio"]**2)))
            return np.minimum.reduce(vals)
        fs=np.linspace(1e-6,1-1e-6,grid+1); vals=score(fs); k=int(np.argmax(vals))
        opt=minimize_scalar(lambda f:-float(score(f)),bounds=(fs[max(0,k-1)],fs[min(grid,k+1)]),
                            method="bounded",options={"xatol":2e-14})
        candidates=[(float(vals[k]),float(fs[k])),(-float(opt.fun),float(opt.x))]
        value,f=max(candidates)
        if best is None or value>best["least_SF"]:
            best={"least_SF":value,"fraction":f,"core":core["name"]}
    core=next(c for c in I["cores"] if c["name"]==best["core"])
    best["point"]=describe(core,best["fraction"],route,material,enforce_joint)
    return best


def validate(results):
    r21=json.loads((ROOT/"intake/021b/RESULTS.json").read_text())
    r28=json.loads((ROOT/"intake/028/RESULTS.json").read_text())
    fp=r21["floating_point"]
    core=next(c for c in I["cores"] if c["name"]==fp["core"])
    tf,tc=fp["tf_m"],fp["core_m"]
    needs=fp["needed_values"]
    em=modes(core,tf,tc,290e9,needs["face_strength_Pa"],needs["gamma"],needs["wrinkle"])
    mode_error=max(abs(float(em["sfs"][k])-fp["at_needed_values"]["sfs"][k]) for k in MODE_NAMES)
    oldmass=fp["masses_kg"]
    par=C["joint_parameters_019_optimistic"]
    seam=(2*A/fp["panel_width_m"])*(2*par["strip_width_m"]*tf*1850+
          2*par["strip_width_m"]*par["seam_adhesive_m"]*par["rho_adhesive_kg_m3"]+
          tc*par["core_splice_width_m"]*par["rho_splice_kg_m3"])
    film=2*A*fp["bond_film_lb_ft2"]*.45359237/.09290304
    reconstructed=2*A*1850*tf+A*core["rho"]*tc+seam+film+SYS+FIXED
    errors028={}
    for route in I["routes"]:
        old=next(c for c in r28["cases"] if c["panel"]=="stock_envelope" and c["route"]==route["id"])
        actual=joining(r28["case"]["tf_m"],r28["case"]["tc_m"],route)["physical_total_kg"]
        errors028[route["id"]]=abs(actual-old["fixed_geometry"]["total_kg"])
    checks={"021b_six_modes_reproduced":mode_error<1e-10,
            "021b_joint_mass_line_reproduced":abs(reconstructed-LIFT)<1e-6,
            "028_four_joining_masses_reproduced":max(errors028.values())<1e-9,
            "every_floating_point_respects_named_set":True,
            "all_selected_mass_lines_close":True,
            "joint_aware_points_pass_seventh_screen":True,
            "S200F255_no_core_upper_bound_below_one":
                255e6*BUDGET/(1+J)/(2*A*1850)/N<1,
            "stock_envelope_fixed":
                (I["panel"]["a_m"],I["panel"]["b_m"])==(.6096,1.8288)
                and I["panel_is_fixed_not_searched"] is True}
    maxres=0
    for r in results["searches"]:
        if "floating_point" not in r: continue
        p=r["floating_point"]; sf=p["at_needed"]
        maxres=max(maxres,abs(p["masses_kg"]["residual"]))
        checks["every_floating_point_respects_named_set"] &= sf["least_six_mode_SF"]>=1-1e-8
        if r["joint_screen_enforced"]:
            checks["joint_aware_points_pass_seventh_screen"] &= sf["least_seven_screen_SF"]>=1-1e-8
    checks["all_selected_mass_lines_close"]=maxres<1e-8
    return {"all_passed":all(checks.values()),"checks":checks,
            "021b_max_mode_error":mode_error,"021b_mass_residual_kg":reconstructed-LIFT,
            "028_mass_errors_kg":errors028,"max_selected_mass_residual_kg":maxres}


def main():
    started=datetime.now(timezone.utc).isoformat()
    out={"schema":1,"card":"MAINLINE-028b","unit":I["unit"],"status":"ESTIMATE",
         "tag":"QUESTIONABLE / PROJECTION","overall_installed_hull_SF":None,
         "calculation_started_at":started,"searches":[],"full_named_maxima":[],
         "mass_policy":I["mass_policy"],"cores_searched":len(I["cores"]),
         "grid_intervals":6000,
         "S200F255_optimistic_no_core_face_SF_upper_bound":
             255e6*BUDGET/(1+J)/(2*A*1850)/N}
    for material in I["materials"]:
        for route in I["routes"]:
            for enforce in ([False,True] if route["seam"]=="scarf" and material["id"]=="SR200" else [True]):
                result=search(route,material,enforce)
                out["searches"].append(result)
                print(material["id"],route["id"],"joint",enforce,
                      None if result["least_set"] is None else
                      (result["least_set"]["subset"],result["least_set"]["min_max_usage"]),
                      flush=True)
            full=maximize_full(route,material)
            out["full_named_maxima"].append({"route":route["id"],"material":material["id"],**full})
            print("  full-named maximum",full["least_SF"],flush=True)
    out["calculation_ended_at"]=datetime.now(timezone.utc).isoformat()
    val=validate(out)
    out["validation"]=val
    (ROOT/"RESULTS.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    (ROOT/"VALIDATION.json").write_text(json.dumps(val,indent=2)+"\n")
    print(json.dumps(val,indent=2),flush=True)
    assert val["all_passed"],val


if __name__=="__main__":
    main()
