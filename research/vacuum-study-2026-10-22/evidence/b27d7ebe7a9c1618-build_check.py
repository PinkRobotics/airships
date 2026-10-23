#!/usr/bin/env python3
"""Assemble the check from independently produced results; never reads owner code."""
from check_model import *
from datetime import datetime
from zoneinfo import ZoneInfo
import csv,hashlib

def run():
    radii=(10,12,15,20,30)
    tables=[read(f"TABLE-CHECK-R{R}.json") for R in radii]
    coupled=[read(f"COUPLED-GRID-CHECK-R{R}.json") for R in radii]
    frozen=[read(f"FROZEN-GRID-CHECK-R{R}.json") for R in radii]
    fixed=read("FIXED-CHECK.json");dew=read("DEW-CHECK.json");accounts=read("ACCOUNTS-CHECK.json")
    days=read("DESIGN-DAY-CHECK.json");extras=read("EXTRAS-CHECK.json");gas=read("GAS-CHECK.json")
    original=read("owner-data/RESULTS.json")
    reference={x["R_m"]:x for x in read("owner-data/MASS-CURVES.json")["reference"]}
    nums=[]
    def number(row,field,owner,checker,decimals):
        nums.append(dict(row=row,field=field,card_value=owner,checker_value=checker,
            difference=checker-owner,display_decimals=decimals,
            agrees_at_display_precision=abs(checker-owner)<=.5*10**(-decimals)+1e-9))
    family100=[5.8,9.5,12.2,14.3,15.8];family500=[-2.7,1.5,4.5,6.9,8.6]
    fixed100=[-6.5,-3.,-.3,1.8,3.3];isapay=[124.3,337.,832.3,2290.,8525.5]
    fixedmass=[5024,8568,16560,38937,130621]
    usage=[.8331,.8847,.7208,.5984,.5666]
    dew_display=[[.090,.004,.243,.084,.199],[.090,.004,.242,.084,.286],
                 [.089,.004,.241,.083,.394],[.088,.004,.239,.082,.556],[.085,.003,.236,.081,.854]]
    cases=["clear_calm_reference","overcast_humid","clear_saturated","clear_cold_frost"]
    for i,R in enumerate(radii):
        for height,values in ((100,family100),(500,family500)):
            row=next(x for x in accounts["direct_family_boundaries"] if x["R_m"]==R and x["z_m"]==height)
            number(f"headline/R{R}/z{height}","family_upper_K",values[i],row["checker_direct_offset_K"],1)
        row=next(x for x in fixed["boundaries"] if x["R_m"]==R and x["z_m"]==100)
        number(f"headline/R{R}/z100","fixed_upper_K",fixed100[i],row["worst_P_RH_upper_offset_K"],1)
        number(f"headline/R{R}","ISA_payload_kg",isapay[i],LIFT_REF*(R/10)**3-reference[R]["mass_kg"],1)
        number(f"headline/R{R}","fixed_mass_kg",fixedmass[i],fixed["builds"][i]["mass_kg"],0)
        number(f"headline/R{R}","least_usage",usage[i],accounts["ISA_usage"][i]["common_log_usage"],4)
        for j,case in enumerate(cases):
            row=next(x for x in dew["base"] if x["R_m"]==R and x["case"]==case)
            number(f"night/R{R}/{case}","deposit_kg_m2",dew_display[i][j],row["mean_deposit_kg_m2"],3)
        allowance=next(x["checker"]["ISA_water_capacity_kg_m2"] for x in accounts["dew_accounts"] if x["checker"]["R_m"]==R)
        number(f"night/R{R}","ISA_total_water_kg_m2",dew_display[i][4],allowance,3)
    for z,reported in ((100,-10.5),(500,-7.9)):
        row=next(x for x in fixed["boundaries"] if x["R_m"]==10 and x["z_m"]==z)
        number(f"cold/z{z}","conservative_lower_K",reported,row["conservative_cold_offset_K"],1)
    number("fixed/R30/z500","upper_K",-6.8,next(x for x in fixed["boundaries"] if x["R_m"]==30 and x["z_m"]==500)["worst_P_RH_upper_offset_K"],1)
    number("fixed","design_pressure_kPa",103.953,fixed["grid_maximum_pressure_Pa"]/1000,3)
    number("night/R10/dry","minimum_skin_K",271.54,dew["dry_reference"]["minimum_outer_K"],2)
    number("night/R10/clear","minimum_skin_K",273.66,dew["base"][0]["minimum_outer_K"],2)
    for R,case,capacity,payload in ((10,"clear_calm_reference",.184,117),(10,"clear_saturated",.178,-82),(12,"clear_saturated",None,33)):
        row=next(x["checker"] for x in accounts["dew_accounts"] if x["checker"]["R_m"]==R and x["checker"]["case"]==case)
        if capacity is not None:number(f"water/R{R}/{case}","capacity_kg_m2",capacity,row["total_water_capacity_kg_m2"],3)
        number(f"water/R{R}/{case}","dry_start_payload_kg",payload,row["dry_start_payload_kg"],0)
    h=accounts["heater_exact"][0]["exact"]
    for key,value,digits in (("mean_power_W_m2",21.1,1),("total_power_kW",26.6,1),("energy_kWh_12h",319,0),("battery_mass_kg",2952,0)):
        number("heater/R10/clear",key,value,h[key],digits)
    h=accounts["heater_exact"][1]["exact"]
    number("heater/R10/overcast","mean_power_W_m2",1.16,h["mean_power_W_m2"],2)
    number("heater/R10/overcast","battery_mass_kg",162,h["battery_mass_kg"],0)
    for R,low,high,digits in ((10,12.6,62.8,1),(30,113,565,0)):
        number(f"cover/R{R}","10_g_m2_mass_kg",low,4*np.pi*R**2*.01,digits)
        number(f"cover/R{R}","50_g_m2_mass_kg",high,4*np.pi*R**2*.05,digits)
    for case,value in (("clear_calm_reference",2.8),("clear_saturated",7.6)):
        row=next(x for x in dew["mitigations"] if x["R_m"]==10 and x["case"]==case)
        number(f"solar/R10/{case}","energy_equivalent_hours",value,row["solar_only_ideal_hours_at_970_W_m2"],1)
    low=next(x for x in dew["mitigations"] if x["R_m"]==10 and x["case"]=="clear_saturated")
    number("low_e/R10/saturated","deposit_kg_m2",.027,low["low_e_0p05_night"]["mean_deposit_kg_m2"],3)
    hot=next(x for x in days["cases"] if x["name"]=="hot_10pct_z100")
    for i,row in enumerate(hot["sizes"]):
        number(f"hot10/z100/R{row['R_m']}","mask11_deficit_kg",[295,397,602,1114,2993][i],-row["payload_by_mask_kg"][11],0)
    number("hot10/z100/R30","mask15_deficit_kg",2771,-hot["sizes"][-1]["payload_by_mask_kg"][15],0)
    zero=np.load(B/"CHECKED-COUPLED-GRID-R10.npz")["upper_zero_T_offset_K"]
    for mask,value in ((3,-4.87),(11,5.71),(15,6.19)):
        number(f"transition/R10/z500/RH100/mask{mask}","upper_K",value,float(zero[mask,8,15,10]),2)
    number("grid","weather_point_count",2027245,sum(x["summary"]["points"] for x in coupled),0)
    with (B/"CARD-NUMBERS.csv").open("w") as f:
        writer=csv.DictWriter(f,fieldnames=list(nums[0]));writer.writeheader();writer.writerows(nums)

    exact=[]
    for name,data in (("design_day",days),("dew",dew),("accounts",accounts),("fixed",fixed)):
        for item in data.get("comparisons",[]):
            if "difference" in item:
                exact.append(dict(category=name,**item))
    for item in accounts["direct_family_boundaries"]:
        exact.append(dict(category="direct_family_root",row=f"R{item['R_m']}/z{item['z_m']}",field="offset_K",
            owner=item["owner_interpolated_offset_K"],checker=item["checker_direct_offset_K"],difference=item["difference_K"]))
    for item in extras["comparisons"]+extras["slices"]:
        exact.append(dict(category="supplemental",**item))
    for pair in accounts["dew_accounts"]:
        o=pair["owner"];n=pair["checker"]
        for oldkey,newkey in (("deposit_kg_m2","deposit_kg_m2"),("threshold_at_night_density_kg_m2","total_water_capacity_kg_m2"),
                ("fresh_dry_payload_after_night_kg","dry_start_payload_kg"),("preexisting_0p1_plus_night_payload_kg","preexisting_0p1_payload_kg")):
            exact.append(dict(category="water_account",row=f"R{n['R_m']}/{n['case']}",field=oldkey,
                owner=o[oldkey],checker=n[newkey],difference=n[newkey]-o[oldkey]))
    save("EXACT-COMPARISONS.json",dict(rows=exact,table_knot_comparisons="TABLE-COMPARISONS-R*.csv",
        frozen_knot_comparisons="FROZEN-KNOT-CHECK.json",dense_grid_values="CHECKED-*-GRID-R*.npz",
        note="All signed arithmetic differences, including harmless floating-point noise; not all are errors."))
    daydiffs=[x for x in days["comparisons"] if x["field"]=="payload_kg"]
    significant=[dict(category="direct_vs_interpolated_design_day",**x) for x in daydiffs if abs(x["difference"])>.05]
    significant += [dict(category="analytic_heater_vs_128_point_quadrature",**x) for x in accounts["comparisons"] if x["row"].startswith("heater_exact") and abs(x["difference"])>1e-7]
    marginal=[]
    for table in tables:
        for x in table["mismatches"]:
            if x.get("owner_feasible") and x.get("checker_feasible"):
                significant.append(dict(category="strict_coupled_knot_difference",**x))
                continue
            marginal.append(dict(category="exploratory_marginal_cold_domain",R_m=x["R_m"],T_K=x["T_K"],
                mask=x["mask"],p_Pa=x["p_Pa"],owner_mass_kg=x["owner_mass_kg"],checker_mass_kg=x["checker_mass_kg"],
                disposition="Exact marginal knot; broader checker core domain and tolerance. Excluded from conservative operating maps."))
    save("MISMATCHES.json",dict(headline_mismatches=[x for x in nums if not x["agrees_at_display_precision"]],
        numerical_resolution_differences=significant,marginal_domain_differences=marginal,
        gas_scope_differences=gas["records"],
        exact_ledger="EXACT-COMPARISONS.json; TABLE-COMPARISONS-R*.csv; FROZEN-KNOT-CHECK.json",
        thresholds=dict(display="Card's stated decimals",direct_vs_interpolated_kg=.05,
            discrete_mask="Exact integer equality",coupled_knot_kg=.05,fixed_geometry_SF=1e-7),
        interpretation="Interpolation and quadrature differences retain the headline verdict. Exploratory domain and gas-scope comparisons are not same-input owner errors."))
    ownfindings=[
      ("CHK50-01","Independence scope","Checker authored 040/048. No 050 code was accessed, but upstream personnel independence is limited.","A checker with no upstream authorship for independent physical review."),
      ("CHK50-02","Material and installed-system qualification","Numeric agreement does not validate Be/core/bond strengths, curvature restraint, defects, cure stress distribution, coatings, moisture or installed loads.","Matched materials, panels, joints and shell tests; inherited NFIs remain open."),
      ("CHK50-03","Weather meaning","The maps are conditional profiles and rectangular parameter samples; family designs change geometry. Percentiles and grid fractions are not operational probabilities.","A selected build, site and mission joint weather/thermal history."),
      ("CHK50-04","Cold boundary and numerical domain","The exact marginal knot depends on the scanned core domain and tolerances. The first fully feasible table point is .05 K warmer. Broader exploratory root solutions are not credited as new feasible operating designs.","Restrict the exclusion claim to its scanned domain and establish cold interface strength experimentally."),
      ("CHK50-05","Interpolation precision","All design-day float/least-set conclusions agree, but a full direct recomputation finds endpoint table differences above .05 kg, up to approximately .23814 kg. Selected decision-critical checkpoints remain much closer.","Say 'selected checkpoints within .05 kg' and retain the exact direct/interpolated ledger."),
      ("CHK50-06","Heater quadrature","The 128-zone result reproduces. An analytic positive-deficit integral differs slightly; R10 reference is 21.144629726 W/m² and 2952.347263 kg battery. Displayed card figures are unchanged.","Use the analytic integral or report the quadrature error; heater installation mass stays unknown."),
      ("CHK50-07","Gas calculation scope","The independently defined all-geometry service bound differs from the owner's scalar sampling and inventory/volume conventions, while both retain ample reserve. No sealed-life qualification follows.","Equation-only gas clarification or explicitly distinguish the conservative checker sweep; measured leaks, venting and desorption remain needed."),
      ("CHK50-08","Thermal mechanics version","050 reproduces the original 048 treatment: cure enters face/scarf demand but not global buckling or crimping. The separately filed 048 cure-inclusive sensitivity is not silently substituted into 050.","Retain both model versions and their scope; qualify prestress/restraint before an operational claim.")
    ]
    oldnfi=read("owner-data/NFI.json")
    findings=[dict(id=i,title=t,finding=f,missing_evidence=e,tag="QUESTIONABLE / PROJECTION",blocks_filing=False)
              for i,t,f,e in ownfindings]
    save("NFI.json",dict(unit="vacuum-mainline050-check-1020",findings=findings,
        inherited_owner_register=oldnfi,qualified_installed_hull_SF=None,qualified_operational_availability=None,
        qualification_closed=False,duplicate_provenance_note="Inherited findings are namespaced evidence, not extra independent confirmations."))
    summary=dict(card_numbers_checked=len(nums),card_display_mismatches=sum(not x["agrees_at_display_precision"] for x in nums),
        strict_interface_rechecked_knots=read("INTERFACE-TOLERANCE-CHECK.json")["corrected_knots"],
        coupled_knots=sum(x["knots"] for x in tables),finite_filed_geometry_checks=sum(x["fixed_geometry_checks"] for x in tables),
        coupled_max_finite_knot_difference_kg=max(x["max_finite_mass_difference_kg"] for x in tables),
        exploratory_marginal_knot_differences=len(marginal),frozen_pressure_knots=len(read("FROZEN-KNOT-CHECK.json")["comparisons"]),
        coupled_weather_points=sum(x["summary"]["points"] for x in coupled),
        frozen_weather_points=sum(x["summary"]["points"] for x in frozen),fixed_weather_points=2027245,
        coupled_zero_entries=sum(x["summary"]["zero_surface_points"] for x in coupled),
        frozen_zero_entries=sum(x["summary"]["zero_surface_points"] for x in frozen),
        grid_classification_mismatches=sum(x["summary"]["feasible_mask_disagreements"]+x["summary"]["least_mask_disagreements"] for x in coupled+frozen),
        fixed_grid_classification_mismatches=extras["fixed_grid_classification_disagreements"],
        zero_finite_disagreements=sum(x["summary"]["zero_finite_disagreements"] for x in coupled+frozen),
        coupled_max_payload_difference_kg=max(x["summary"]["payload_max_abs_difference_kg"] for x in coupled),
        max_zero_offset_difference_K=max(x["summary"]["zero_max_abs_difference_K"] for x in coupled+frozen),
        design_days=len(days["cases"]),design_day_endpoint_cases=len(daydiffs),
        max_design_day_interpolation_difference_kg=max(abs(x["difference"]) for x in daydiffs),
        design_day_least_set_mismatches=sum(s["least_cardinality_masks"]!=s["owner_least_masks"] for c in days["cases"] for s in c["sizes"]),
        dew_numeric_comparisons=len(dew["comparisons"]),
        maximum_deposit_difference_kg_m2=max(abs(x["difference"]) for x in dew["comparisons"] if x["field"]=="mean_deposit_kg_m2"),
        maximum_midpoint_refinement_change_kg_m2=max(abs(x["mean_deposit_kg_m2"]-y["mean_deposit_kg_m2"]) for x,y in zip(dew["base"],dew["refined"])),
        transition_intervals=extras["transition_count"],transition_mismatches=extras["transition_mask_mismatches"],
        boundary_slice_values=extras["slice_count"],slice_finite_mismatches=extras["slice_finite_mismatches"],
        gas_all_geometry_reserve_pass=all(x["all_geometry_mass_pass"] and x["all_geometry_pressure_pass_even_without_pores"] for x in gas["records"]))
    save("RESULTS.json",dict(unit="vacuum-mainline050-check-1020",status="COMPLETE",
        verdict="CONDITIONAL_HEADLINES_REPRODUCED_WITH_NUMERICAL_AND_SCOPE_QUALIFICATIONS",
        completed_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat(),summary=summary,
        primary_artifact="CHECK.md",exact_mismatches="MISMATCHES.json",headline_rows=nums,
        owner_code_read=False,owner_code_run=False,independence=read("START.json")["independence_disclosure"],
        qualified_installed_hull_SF=None,qualified_operational_availability=None,next_job=None))
    save("INPUTS.json",dict(unit="vacuum-mainline050-check-1020",tag="QUESTIONABLE inputs / PROJECTION calculations",
        authority=read("ORDER.json"),brief_pins=read("BRIEF-PINS.json"),owner_data_pins=read("OWNER-DATA-PINS.json"),
        upstream_pins=read("UPSTREAM-PINS.json"),source_fetches=read("sources/FETCH-PINS.json"),
        refinement_targets_pin=dict(path=str(B/"REFINEMENT-TARGETS.json"),
            sha256=hashlib.sha256((B/"REFINEMENT-TARGETS.json").read_bytes()).hexdigest(),
            bytes=(B/"REFINEMENT-TARGETS.json").stat().st_size),
        clarification_pins=read("clarifications/PINS.json"),independence=read("START.json")["independence_disclosure"],
        equations="METHOD.md and independently authored check_*.py",
        atmosphere=CASE["atmosphere"],thermal=CASE["thermal"],night_constants=CASE["night_constants"],
        night_cases=CASE["night_cases"],radii_m=radii,mask_definition=CASE["masks"],
        material_source="inputs/040/INPUTS.json",gas_source="inputs/034/INPUTS.json",coating_source="inputs/048/COATINGS.json",
        work_budget=None,resource_request="simjob --cores 1 --mem 2G",qualified_installed_hull_SF=None))
    print(json.dumps(summary,indent=2),flush=True)

if __name__=="__main__":run()
