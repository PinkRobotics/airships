"""Independent MAINLINE-015 arithmetic. No owner code is imported or executed.

Run from any directory with Python 3. Only this output directory is written.
The formulas, assumptions, and primary-source corrections are in CHECK.md.
"""
from datetime import datetime
from pathlib import Path
import hashlib
import json
import math
import csv

ROOT = Path(__file__).resolve().parent
R, NU, EF_AL, RHO_AL, RHO_CORE = 10.0, 0.33, 68.9e9, 2700.0, 16.0
AREA = 4 * math.pi * R**2
Q = math.sqrt(1 - NU**2)
WIDTH_COEFF = (12 * (1 - NU**2))**0.25
P = 95460.83791390515
LIFT = 4889.442150186961
MASS = (LIFT - 100) / 1.05
LEVELS = (0.2, 0.3, 0.5, 0.7, 0.9)


def load(path):
    return json.loads(path.read_text())


def bisect(fn, left, right):
    a, b = fn(left), fn(right)
    assert a * b <= 0, (left, right, a, b)
    for _ in range(90):
        mid = (left + right) / 2
        c = fn(mid)
        if a * c <= 0:
            right = mid
        else:
            left, a = mid, c
    return (left + right) / 2


BIAX = bisect(lambda x: x**3 + x - 1, 0, 1)
CORE = {"density": 1.6 * 16.018463373960138,
        "Ec": 30000 * 6894.757293168361,
        "Gc": 10500 * 6894.757293168361,
        "crush": 50 * 6894.757293168361}
FACE = {"density": 1850.0, "E": 303e9, "yield": 283e6}


def geometry(fraction, face=FACE, core=CORE):
    tf = MASS * (1 - fraction) / (2 * AREA * face["density"])
    depth = MASS * fraction / (AREA * core["density"])
    return tf, depth


def modes(fraction, kd, cell=0.00635):
    tf, depth = geometry(fraction)
    h = tf + depth
    stress = P * R / (4 * tf)
    # NASA CR-1457 §§6.2, 2.2.2 and 2.1; equal isotropic faces.
    sigma0 = FACE["E"] * h / (Q * R)
    crimp = CORE["Gc"] * h * h / (2 * tf * depth)
    vc = sigma0 / crimp
    kc = 1 - vc / 4 if vc <= 2 else 1 / vc
    gamma = kd if vc < 2 else 1.0
    sfs = {
        "global_buckling": gamma * kc * sigma0 / stress,
        "face_yield": FACE["yield"] / stress,
        "core_shear_crimping": crimp / stress,
        "core_crush": CORE["crush"] / (P / 2),
        "face_wrinkling": BIAX * 0.33 * math.sqrt(FACE["E"] * CORE["Ec"] * tf / depth) / stress,
        "intracell_dimpling": 2 * FACE["E"] / (1 - NU**2) * (tf / cell)**2 / stress,
    }
    order = sorted(sfs, key=sfs.get)
    return {"tf_m": tf, "core_m": depth, "h_m": h, "core_mass_fraction": fraction,
            "Vc": vc, "Kc": kc, "gamma": gamma,
            "branch": "stiff_or_moderate_core" if vc < 2 else "shear_crimping",
            "sfs": sfs, "governing": order[0], "least_SF": sfs[order[0]],
            "second_mode": order[1], "second_SF": sfs[order[1]]}


def grid_optimum(kd):
    # Reproduce the reported fraction spacing, independently from the mass law.
    return max((modes(i / 8000, kd) for i in range(1, 8000)),
               key=lambda row: row["least_SF"])


def continuous_optimum(kd):
    # Locate the best grid neighbourhood, then refine its mode intersections
    # and local maximum. The threshold below has a separate monotonicity proof.
    # Our independent continuous search is an additional estimate, not a
    # retroactive change to the owner's finite grid.
    from scipy.optimize import minimize_scalar, brentq
    fractions = [i / 10000 for i in range(1, 10000)]
    rows = [modes(x, kd) for x in fractions]
    peak = max(range(len(rows)), key=lambda i: rows[i]["least_SF"])
    lo, hi = fractions[max(0, peak - 2)], fractions[min(len(rows)-1, peak + 2)]
    fit = minimize_scalar(lambda x: -modes(x, kd)["least_SF"], bounds=(lo, hi),
                          method="bounded", options={"xatol": 1e-15})
    candidates = [modes(fit.x, kd)]
    keys = list(rows[peak]["sfs"])
    for i, key in enumerate(keys):
        for other in keys[i+1:]:
            fn = lambda x: modes(x, kd)["sfs"][key] - modes(x, kd)["sfs"][other]
            if fn(lo) * fn(hi) < 0:
                candidates.append(modes(brentq(fn, lo, hi, xtol=1e-15), kd))
    return max(candidates, key=lambda row: row["least_SF"])


def shell(tf, depth, tag="QUESTIONABLE", h=None):
    h = tf + depth if h is None else h
    teq = math.sqrt(3) * h
    exact = math.sqrt(3 * h*h + tf*tf) if tf is not None else None
    scale = math.sqrt(R * teq)
    beta1 = scale / (R * WIDTH_COEFF)
    betaw = 2.625 * beta1
    levels = {}
    for kd in LEVELS:
        alpha = -math.log((kd - 0.45) / 0.51) / 3.88 if kd > 0.45 else None
        lee_alpha = 0.25 / (kd - 0.068) - 0.28
        # Lee eq.23 is used as printed; no silent repair of H&T's 0.68.
        levels[str(kd)] = {
            "delta_bar_lambda1": alpha,
            "amplitude_mm": alpha * teq * 1000 if alpha is not None else None,
            "rms_narrow_single_mm": alpha * teq * beta1 / math.sqrt(8) * 1000 if alpha is not None else None,
            "rms_worst_single_mm": alpha * teq * betaw / math.sqrt(8) * 1000 if alpha is not None else None,
            "mixed_width_rms_has_matched_kd": False,
            "small_amplitude_limit_not_captured": alpha is not None and alpha < 0.07,
            "lee_envelope_delta_bar": lee_alpha,
            "lee_envelope_amplitude_mm": lee_alpha * teq * 1000,
            "lee_envelope_in_computed_amplitude_range": 0.15 <= lee_alpha <= 3,
            "lee_envelope_tag": "QUESTIONABLE",
            "lee_envelope_width_and_rms": None,
        }
        if alpha is None:
            levels[str(kd)].update(
                amplitude_upper_bound_mm=teq*1000,
                rms_at_one_thickness_worst_mm=teq*betaw/math.sqrt(8)*1000,
                bound_is_source_supported=False)
    return {"tf_m": tf, "core_m": depth, "h_m": h, "tag": tag, "t_eq_m": teq,
            "t_eq_finite_faces_m": exact, "R_over_t_eq": R / teq,
            "i2_sandwich_m2": h*h/4, "i2_monocoque_m2": teq*teq/12,
            "widths": {"sqrt_R_t_eq_m": scale, "width_lambda_I_1_m": beta1 * R,
                       "width_worst_m": betaw * R, "beta0_lambda_I_1_rad": beta1,
                       "beta0_worst_rad": betaw, "l_c_m": 2*math.pi*R*beta1},
            "one_thickness_mm": teq*1000, "levels": levels}


def shear(tf, depth, modulus, young):
    h = tf + depth
    vc = 2*young*tf*depth/(Q*R*modulus*h)
    kc = 1-vc/4 if vc <= 2 else 1/vc
    # Reproduction of the isolated 015 'core_shear' formula inferred from
    # its numbers; it is not the primary handbook reduction above.
    isolated_delta = young*tf*Q/(modulus*R)
    return {"Gc_Pa": modulus, "Vc": vc, "CR1457_pressure_ratio": kc,
            "CR1457_reduction": 1-kc, "isolated_delta": isolated_delta,
            "isolated_015_pressure_ratio": 1/math.sqrt(1+isolated_delta)}


def compare(path, expected, actual, rows, rtol=2e-10, atol=2e-11):
    if isinstance(expected, (float, int)) and not isinstance(expected, bool):
        if actual is None:
            return
        ok = math.isclose(expected, actual, rel_tol=rtol, abs_tol=atol)
        rows.append({"field": path, "owner": expected, "check": actual,
                     "difference": actual-expected, "within_rounding": ok})
    elif isinstance(expected, dict) and isinstance(actual, dict):
        for key in sorted(expected.keys() & actual.keys()):
            compare(path+"."+key, expected[key], actual[key], rows, rtol, atol)


def main():
    start = datetime.now().astimezone().isoformat()
    for item in load(ROOT/"inputs/manifest.json"):
        local = ROOT/"inputs"/Path(item["path"]).name
        assert hashlib.sha256(local.read_bytes()).hexdigest() == item["sha256"]
    owner = load(ROOT/"inputs/owner015.json")
    r003 = load(ROOT/"inputs/mainline003.json")
    r014 = load(ROOT/"inputs/mainline014.json")
    atm = r003["atmosphere"]
    assert abs(atm["p_ext_Pa"]-P) < 1e-8 and abs(atm["lift_kg"]-LIFT) < 1e-8
    shells = {"P2": shell(0.0002, 0.1)}
    # Derive all 003 geometries from the defining mass allocations.
    tf_a = (MASS/AREA - 0.1*RHO_CORE)/(2*RHO_AL)
    shells["P2-A"] = shell(tf_a, 0.1)
    shells["P2-C"] = shell(0.0002, (MASS/AREA-2*RHO_AL*0.0002)/RHO_CORE)
    factor = MASS/(AREA*(2*RHO_AL*0.0002+RHO_CORE*0.1))
    shells["P2-K"] = shell(0.0002*factor, 0.1*factor)
    shells["P2-E"] = shell(MASS/(4*AREA*RHO_AL), MASS/(2*AREA*RHO_CORE))
    aliases = {"CNT-yarn composite quasi-isotropic": "014-CNT-HRH10",
               "Graphene composite quasi-isotropic": "014-graphene-HRH10",
               "Beryllium S-200F": "014-Be-HRH10"}
    for row in r014["optima"]:
        if row["kd"] == 0.2 and row["face"] in aliases:
            # Geometry is an inherited, pinned input here; 015 only maps it.
            shells[aliases[row["face"]]] = shell(row["tf_m"], row["core_m"], row["face_tag"])
    frozen = grid_optimum(0.2)
    frozen03 = modes(frozen["core_mass_fraction"], 0.3)
    kd_global = 0.2/frozen["sfs"]["global_buckling"]
    opt03 = grid_optimum(0.3)
    continuous02, continuous03 = continuous_optimum(0.2), continuous_optimum(0.3)
    tf_yield = P*R/(4*FACE["yield"])
    fraction_yield = 1-2*AREA*FACE["density"]*tf_yield/MASS
    capacity = modes(fraction_yield, 1.0)
    kd_min = 1/capacity["sfs"]["global_buckling"]
    crossing = modes(fraction_yield, kd_min)
    # On x <= fraction_yield, monotonic pressure establishes that the
    # yield-boundary split maximises global capacity among yield-feasible ones.
    a, b = MASS/(2*AREA*FACE["density"]), MASS/(AREA*CORE["density"])
    c = FACE["E"]/(2*CORE["Gc"]*R*Q)
    c1 = a*(b-2*a)-c*a*a*b
    c2 = -a*(b-a)+2*c*a*a*b
    c3 = -c*a*a*b
    derivative_endpoints = [c1, c1+2*c2*fraction_yield+3*c3*fraction_yield**2]
    shells["014b-Be-CRIII-1.6"] = shell(frozen["tf_m"], frozen["core_m"])
    regrid = {str(kd): grid_optimum(kd) for kd in (0.518, 0.519)}
    shears = {"P2-E": [shear(shells["P2-E"]["tf_m"], shells["P2-E"]["core_m"], g, EF_AL)
                       for g in (9e6,14e6,20000*6894.757293168361)],
              "014b-Be-CRIII": shear(frozen["tf_m"], frozen["core_m"],CORE["Gc"],FACE["E"])}
    hydrostatic = atm["rho_kg_m3"] * 9.80665 * 2*R
    drivers = {}
    for name in ("P2-E","014b-Be-CRIII-1.6"):
        row = shells[name]
        tf,h,teq = row["tf_m"], row["h_m"], row["t_eq_m"]
        drivers[name] = {
            "thickness_dpc_over_pc_uniform_faces": 1+tf/h,
            "one_face_thinning_10pct_pressure_loss": None,
            "both_faces_thinning_10pct_pressure_loss": 1-0.9*(h-0.1*tf)/h,
            "hydrostatic_Pa": hydrostatic, "hydrostatic_over_p": hydrostatic/P,
            "seam_step_narrow_branch": {f"{mm}mm":{"delta_bar":mm/1000/teq,
                "kappa_eq3":0.45+0.51*math.exp(-3.88*mm/1000/teq)}
                for mm in (1,3,10)}}
        # Unequal-face membrane/bending model, hold core depth and one face.
        t1,t2 = 0.9*tf,tf
        hnew = row["core_m"]+(t1+t2)/2
        drivers[name]["one_face_thinning_10pct_pressure_loss"] = 1-math.sqrt(t1*t2)/tf*hnew/h
    row = shells["P2-E"]
    tf,h,teq = row["tf_m"],row["h_m"],row["t_eq_m"]
    bending = (6*tf*h*h)**(1/3)
    p_sandwich = 4*EF_AL*tf*h/(R*R*Q)
    p_zoelly = 2*EF_AL*(teq/R)**2/(math.sqrt(3)*Q)
    transfer = {"t_eq_bending_only_m":bending,"t_eq_over_bending":teq/bending,
                "bending_core_depth_approximation_m":(6*tf*row["core_m"]**2)**(1/3),
                "lambda_004b_convention":2*WIDTH_COEFF*math.sqrt(R/(6*tf*row["core_m"]**2)**(1/3)),
                "lambda_sealed":2*WIDTH_COEFF*math.sqrt(R/bending),
                "p_sandwich_Pa":p_sandwich,"p_zoelly_at_t_eq_Pa":p_zoelly,
                "p_sandwich_over_zoelly":p_sandwich/p_zoelly,
                "zoelly_over_sandwich":p_zoelly/p_sandwich,
                "E_eq_Pa":EF_AL*2*tf/teq,
                "p_zoelly_with_E_eq_Pa":p_zoelly*2*tf/teq}
    comparisons=[]
    compare("structural_mass_kg",owner["structural_mass_kg"],MASS,comparisons)
    compare("biaxial_factor",owner["biaxial_factor"],BIAX,comparisons)
    compare("plateau",owner["plateau"],{"k_1":.036+.964*2**(-1.23),
            "k_worst_2_625":.036+.964*3.625**(-1.23),"eq3_floor":.45},comparisons)
    compare("be_core",owner["be_aluminium"],{"density_kg_m3":CORE["density"],
            "Gc_Pa":CORE["Gc"],"Ec_Pa":CORE["Ec"],
            "kd_for_global_SF_1":kd_global,
            "cell_3_8_least_SF":modes(frozen["core_mass_fraction"],.2,.009525)["least_SF"]},comparisons)
    for name,row in shells.items():
        compare("shells."+name,owner["shells"][name],row,comparisons)
    compare("transfer",owner["shells"]["P2-E"]["transfer"],transfer,comparisons)
    compare("frozen",owner["be_aluminium"]["frozen_kd_0_20"],frozen,comparisons)
    compare("reoptimised_kd_0.3",owner["be_aluminium"]["reoptimised_at_kd_0_30"],opt03,comparisons)
    for key,row in owner["be_aluminium"]["frozen_at_raised_kd"].items():
        kd = kd_global if key == "0.2991" else float(key)
        compare("raised_frozen."+key,row,modes(frozen["core_mass_fraction"],kd),comparisons)
    for key,kd in [("first_at_or_above_1",0.519),("previous",0.518)]:
        compare("crossing_grid."+key,owner["be_aluminium"]["reoptimised_SF1_crossing"][key],
                regrid[str(kd)],comparisons)
    for name,row in drivers.items():
        owner_name = "014b-Be-CRIII" if name.startswith("014b") else name
        compare("drivers."+name,owner["drivers"][owner_name],row,comparisons)
        compare("drivers."+name+".thickness_dpc_over_pc_per_face",
                owner["drivers"][owner_name]["thickness_dpc_over_pc_per_face"],
                row["thickness_dpc_over_pc_uniform_faces"],comparisons)
    # Check every manufacturing ratio from independent amplitude/width formula.
    manufacture=[]
    for name,levels in owner["gaps_required_over_achieved"].items():
        for kd,entries in levels.items():
            bound="bound" in entries
            entries=entries.get("bound",entries)
            r=shells[name]
            amp=r["t_eq_m"] if bound else r["levels"][kd]["amplitude_mm"]/1000
            rms=amp*r["widths"]["beta0_worst_rad"]/math.sqrt(8)
            for benchmark,vals in entries.items():
                if not isinstance(vals,dict): continue
                compare("gaps."+name+"."+kd+"."+benchmark,vals,
                        {"amplitude_over_achieved":amp/vals["achieved_m"],
                         "rms_over_achieved":rms/vals["achieved_m"]},comparisons)
                manufacture.append({"shell":name,"kd":float(kd),"benchmark":benchmark,
                                    "reference_accuracy_m":vals["achieved_m"],
                                    "amplitude_ratio":amp/vals["achieved_m"],
                                    "rms_ratio_nu_0_33_mixed_width":rms/vals["achieved_m"],
                                    "rms_ratio_matched_lambda1":rms/2.625/vals["achieved_m"] if not bound else None,
                                    "metric_compatible_as_qualification":False})
    cross={}
    for name,row in shells.items():
        rt=row["R_over_t_eq"]
        n_rounded=90*math.sqrt(rt/100)
        n_exact=(20*math.pi/7)*math.sqrt(rt)
        cross[name]={"nasa_kd":1-0.901*(1-math.exp(-math.sqrt(rt)/16)),
                     "R_over_800_mm":R/800*1000,
                     "kappa_eq3_at_R_over_800":0.45+0.51*math.exp(-3.88*(R/800)/row["t_eq_m"]),
                     "pnas_N":n_rounded,"pnas_N_eq6":n_exact,
                     "pnas_mean":0.235*math.sqrt(1+20/n_rounded),
                     "pnas_design_1e-3":0.235+1.24*(1e-3/n_exact)**(1/3.39),
                     "pnas_design_1e-2":0.235+1.24*(1e-2/n_exact)**(1/3.39)}
        cross[name]["pnas_parameters_coherent_as_one_distribution"] = (
            cross[name]["pnas_mean"] >= .999*cross[name]["pnas_design_1e-3"]+.001*.235)
        compare("cross."+name,owner["shells"][name]["cross"],cross[name],comparisons)
    for name,entries in owner["core_shear"].items():
        ours=shears[name]
        pairs=zip(entries.values(),ours) if isinstance(ours,list) else [(entries,ours)]
        for i,(before,after) in enumerate(pairs):
            compare(f"isolated_shear.{name}.{i}",before,
                    {"delta_shear":after["isolated_delta"],
                     "p_cr_over_p_c":after["isolated_015_pressure_ratio"],
                     "reduction":1-after["isolated_015_pressure_ratio"]},comparisons)
    benchmark_values = {"PNAS_100_1e-3":.235+1.24*(1e-3/((20*math.pi/7)*10))**(1/3.39),
                        "PNAS_100_1e-2":.235+1.24*(1e-2/((20*math.pi/7)*10))**(1/3.39)}
    for check in owner["checks"]:
        if "PNAS" in check["name"]:
            key = "PNAS_100_1e-3" if "1e-3" in check["name"] else "PNAS_100_1e-2"
            compare("checks."+key,check["got"],benchmark_values[key],comparisons)
        elif "lambda" in check["name"]:
            compare("checks.lambda",check["got"],transfer["lambda_004b_convention"],comparisons)
        elif "got" in check:
            compare("checks.frozen_least",check["got"],frozen["least_SF"],comparisons)
    # Every width and RMS can also be reproduced using the inferred nu=0.30.
    inferred_width_coeff=(12*(1-0.3**2))**0.25
    reproduction=[]
    for name,row in shells.items():
        ratio=WIDTH_COEFF/inferred_width_coeff
        revised=json.loads(json.dumps(row))
        for key in revised["widths"]:
            if key!="sqrt_R_t_eq_m":
                revised["widths"][key]*=ratio
        for level in revised["levels"].values():
            for key in ["rms_worst_single_mm","rms_narrow_single_mm","rms_at_one_thickness_worst_mm"]:
                if level.get(key) is not None:
                    level[key]*=ratio
        compare("nu_0_30_reproduction."+name,owner["shells"][name],revised,reproduction)
    verifications = {
        "mass_ceiling_kg":1.05*MASS+100,
        "float_mass_residual_kg":1.05*MASS+100-LIFT,
        "bialxial_root_residual":BIAX**3+BIAX-1,
        "frozen_cell_3_8_least_SF":modes(frozen["core_mass_fraction"],0.2,0.009525)["least_SF"],
        "continuous_threshold_least_SF":crossing["least_SF"],
        "threshold_global_SF":crossing["sfs"]["global_buckling"],
        "threshold_yield_SF":crossing["sfs"]["face_yield"],
        "threshold_all_modes_at_least_1":all(v >= 1-1e-12 for v in crossing["sfs"].values()),
        "threshold_global_capacity_derivative_endpoints":derivative_endpoints,
        "threshold_capacity_monotonic_over_yield_feasible_splits":min(derivative_endpoints)>0,
        "equal_A_D_mapping_pressure_residual":transfer["p_zoelly_with_E_eq_Pa"]-p_sandwich,
        "count_numeric_fields_compared":len(comparisons),
        "count_outside_rounding":sum(not x["within_rounding"] for x in comparisons),
        "nu_0_30_reproduction_count":len(reproduction),
        "nu_0_30_reproduction_outside_rounding":sum(not x["within_rounding"] for x in reproduction),
    }
    assert verifications["threshold_all_modes_at_least_1"]
    assert abs(verifications["equal_A_D_mapping_pressure_residual"]) < 1e-7
    result={"schema":1,"unit":"vacuum-mainline015-check-1019","certification":False,
            "tag":"QUESTIONABLE; projected materials individually PROJECTION",
            "started_at":load(ROOT/"WORK.json")["started_at"],"compute_started_at":start,
            "compute_ended_at":datetime.now().astimezone().isoformat(),
            "owner_script_used":False,"case":{"R_m":R,"p_Pa":P,"rho_air":atm["rho_kg_m3"],
                "lift_kg":LIFT,"structural_mass_kg":MASS,"nu":NU},
            "biaxial_factor":BIAX,"plateau":{"k_1":0.036+0.964*2**(-1.23),
                "k_2_625":0.036+0.964*3.625**(-1.23),
                "k_5":0.036+0.964*6**(-1.23),
                "k_2_625_R_over_t_50":0.05+0.95*3.625**(-1.2)},
            "shells":shells,"transfer":transfer,"be_aluminium":{
                "material":FACE,"core":CORE,"frozen_kd_0_20":frozen,"kd_for_global_SF_1":kd_global,
                "frozen_kd_0_30":frozen03,"reoptimised_kd_0_30_grid":opt03,
                "continuous_optimum_0_20":continuous02,"continuous_optimum_0_30":continuous03,
                "grid_crossing":regrid,"continuous_kd_threshold":kd_min,
                "continuous_threshold":crossing},
            "core_shear":shears,"drivers":drivers,"manufacturing_ratios":manufacture,
            "additional_benchmarks":benchmark_values,
            "cross":cross,"numeric_comparisons":comparisons,
            "nu_0_30_reproduction":reproduction,"verification":verifications}
    (ROOT/"RESULTS.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    with (ROOT/"NUMERIC-CHECK.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(comparisons[0]))
        writer.writeheader()
        writer.writerows(comparisons)
    print(json.dumps({"verification":verifications,"continuous_threshold":kd_min,
                      "threshold_geometry":crossing,
                      "continuous_0.3":continuous03,"shears":shears,
                      "hydrostatic_Pa":hydrostatic},indent=2))


if __name__ == "__main__":
    main()
