"""Historical conventions, radiation-path diagnostics, finishes and convergence."""
import json
import numpy as np
from thermal_check import *
from account_check import E0, GC, CRUSH, SW, KB, CURE, DA

comp = Compare("SUPPLEMENT-COMPARISONS")
probes = {}
for model, target in json.loads((ROOT/"owner/THERMAL-PROBE.json").read_text()).items():
    ans = solve(10,TC_REF,model,.2,.9,n=128,scheme="gauss",poles=False,density=2640,curv="grid")
    probes[model] = ans
    comp.table("historical_R10_grid_convention",model,ans,target)
dump("FOUR-R10-GRID-INDEPENDENT.json",probes)

for source,model,curv_mode in (
        ("040/THERMAL-TABLE.json","mixed_gap","grid"),
        ("040check/THERMAL-INDEPENDENT.json","forced_conduction","roots")):
    data = json.loads((ROOT/"intake/inputs"/source).read_text())
    for radius,target in data.items():
        ans = solve(float(radius),target["tc_m"],model,.2,.9,n=128,scheme="gauss",poles=False,curv=curv_mode)
        ans["gradient_K"] = ans["day_gradient_K"]
        ans["curvature_temperature_K"] = ans["day_curvature_temperature_K"]
        comp.table("historical_"+source, radius, ans, target)

screen_results = []
geometry = json.loads((ROOT/"intake/inputs/028b/PROPERTY-CHECKS.json").read_text())["full_named_maxima"][0]["point"]
tf_ref = geometry["tf_m"]
rigid_coefficient = DA*np.sqrt(E0*tf_ref*GC/TC_REF)
for row in json.loads((ROOT/"owner/SETTLED-FINISH-SCREEN.json").read_text()):
    c = COATS[row["id"]]
    ans = solve(10,TC_REF,row["model"],c["alpha"],c["epsilon"])
    rise = float(ans["rise_K"][0])
    swing = float(ans["swing_K"][0])
    cold = float(ans["min_outer_K"][0])
    hot = float(ans["max_outer_K"][0])
    factors = {
        "day_factor":CRUSH/(rigid_coefficient*rise),
        "cycle_factor":CRUSH/(rigid_coefficient*swing),
        "cure_edge_minimum_factor":SW/(DA*max(abs(CURE-cold),abs(CURE-hot))*np.sqrt(2*KB*GC))}
    for key,val in factors.items():
        # 037's source geometry/properties and the later display convention
        # differ at ~4e-8 relative. Preserve each exact difference.
        comp.add("finish_factors",row["model"]+"/"+row["id"]+"/"+key,
                 val,row[key],atol=1e-6,rtol=1e-8)
    factors.update(day_pass=factors["day_factor"]>=row["day_threshold"],
                   cycle_pass=factors["cycle_factor"]>=1)
    screen_results.append({"model":row["model"],"id":row["id"],
                           "tf_source_m":tf_ref,"own":factors})
dump("FINISH-SCREENS-INDEPENDENT.json",screen_results)

legacy = []
for row in json.loads((ROOT/"owner/SCREEN-REPRODUCTION.json").read_text()):
    c = COATS[row["id"]]
    item = {"id":row["id"]}
    for boundary,model in (("owner_boundary","mixed_gap"),("checker_boundary","forced_conduction")):
        results = {}
        for convention in ("legacy","common"):
            old = convention=="legacy"
            ans = solve(10,TC_REF,model,c["alpha"],c["epsilon"],
                n=37 if old else 128,scheme="midpoint" if old else "gauss",
                poles=False,density=2640 if old else 2700,
                raw_day=old,raw_night=old and boundary=="checker_boundary",curv="grid")
            comp.table("screen_reproductions",f'{row["id"]}/{boundary}/{convention}',
                       ans,row[boundary][convention])
            results[convention]=ans
        item[boundary]=results
    legacy.append(item)
dump("LEGACY-SCREENS-INDEPENDENT.json",legacy)

invariants=[]
diagnostics=[]
for model in MODELS:
    uniform=solve(10,[.001,TC_REF,1.5],model,uniform=True)
    error=max(float(np.max(abs(uniform[key]-TA))) for key in ("max_outer_K","min_outer_K"))
    invariants.append({"model":model,"check":"uniform environment","maximum_error_K":error,"passed":error<1e-9})
    isolated=solve(10,TC_REF,model,inner_epsilon=0.)
    invariants.append({"model":model,"check":"no enclosure exchange yields zero core gradient",
        "gradient_K":float(isolated["gradient_K"][0]),"passed":float(isolated["gradient_K"][0])<1e-9})
    for r in (10,15,30):
        low=solve(r,[.001*r/10,TC_REF*r/10,1.5*r/10],model)
        high=solve(r,[.001*r/10,TC_REF*r/10,1.5*r/10],model,n=1024)
        diagnostics.append({"model":model,"R_m":r,"n_low":256,"n_high":1024,
            "differences_K":{k:(np.array(high[k])-low[k]).tolist() for k in
                ("gradient_K","swing_K","rise_K","curvature_temperature_K","max_outer_K","min_outer_K")}})
dump("INVARIANTS-INDEPENDENT.json",invariants)
dump("CONVERGENCE-INDEPENDENT.json",diagnostics)

gap_sensitivity=[]
for model in ("forced_gap","mixed_gap"):
    for emissivity in (0,1/9,.2):
        ans=solve(10,TC_REF,model,.2,.9,n=128,scheme="gauss",poles=False,density=2640,
                  curv="grid",gap_override=emissivity)
        gap_sensitivity.append({"model":model,"effective_gap_emissivity":emissivity,
             "gradient_K":float(ans["gradient_K"][0]),"swing_K":float(ans["swing_K"][0]),
             "rise_K":float(ans["rise_K"][0])})
dump("GAP-SENSITIVITY.json",{
    "two_gray_plate_effective_emissivity":1/(1/.2+1/.2-1),
    "assumed_coefficient_to_two_plate_ratio":.2/(1/(1/.2+1/.2-1)),
    "two_plate_is_a_sensitivity_not_honeycomb_validation":True,
    "rows":gap_sensitivity})
comp.close("SUPPLEMENT")
print(json.dumps(comp.stats,indent=2))
