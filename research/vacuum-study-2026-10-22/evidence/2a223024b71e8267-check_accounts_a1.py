"""Independent ratio, geometry, stock, cost and mass-account spot checks."""
import csv
import json
import math
from source_a1 import ROOT, read, dependency

owner=read("062--RESULTS.json")
assumptions=read("062--ASSUMPTIONS.json")
source047=read("047--INPUTS.json")
check047=read("CHECK047--RESULTS.json")
source057=json.loads(dependency("057","mga057.json").read_text())
classes=source057["classification"]["P2"]
rho=assumptions["Be_density_kg_m3"]
rhoc=assumptions["core_density_kg_m3"]
p=source047["pressure_kPa"]*1000
F=assumptions["assumed_face_compressive_yield_MPa"]*1e6
tf0=source047["model"]["tf_each_mm"]/1000
tc0=source047["model"]["tc_mm"]/1000
d0=tf0+tc0
res0=source047["thermal_sensitivity"]["face_residual_compression_MPa"]*1e6

def bill(r,weather):
    candidates=[x for x in source057["P2_records"] if x["R_m"]==r and x["weather"]==weather
                and x["floor"] is False and x["source"]==("048" if r==10 else "040 with 048 finish transfer")]
    assert len(candidates)==1,(r,weather)
    row=next(x for x in candidates[0]["masks"] if x["mask"]==15)
    return row["bill"],row["lift_kg"],candidates[0]["id"]

shapes=[]; costs=[]; masses=[]; fixes=[]
csvrows=list(csv.DictReader((ROOT/"sources/062--COST-BILL.csv").open()))
for radius in (10,20,30):
    b,lift,source_id=bill(radius,"ISA")
    area=4*math.pi*radius**2
    tf=b["faces"]/(2*area*rho)
    tc=b["core"]/(area*rhoc)
    sep=tf+tc
    res=res0*(tc/tf)/(tc0/tf0)
    row={"R_m":radius,"tf_m":tf,"tc_m":tc,"cure_debit_MPa":res/1e6,"tolerances":[]}
    for sf in (1.,1.05):
        key="SF1" if sf==1 else "SF1.05"
        a0=round(check047["verdict"]["governing_estimates_mm"][key],4)/1000
        base_excess=4*tf0*F/(sf*p*10)-1
        for with_cure in (False,True):
            capacity=F-res if with_cure else F
            target_excess=4*tf*capacity/(sf*p*radius)-1
            amp=a0*(sep/d0)*(target_excess/base_excess)
            # Independent rearrangement: calibrate the eccentricity slope in
            # stress units and solve one linear stress equation.
            slope0=(F-sf*p*10/(4*tf0))/a0
            slopeR=slope0*(sf*p*radius/(4*tf))/(sf*p*10/(4*tf0))*d0/sep
            alternate=(capacity-sf*p*radius/(4*tf))/slopeR
            assert abs(amp-alternate)<1e-14
            row["tolerances"].append({"SF":sf,"with_cure":with_cure,"amplitude_mm":amp*1000,
                                     "reference_rounded_mm":a0*1000,
                                     "formula":"reference-amplitude ratio after eliminating C"})
    row["homothetic_SF105_mm"]=.7469*radius/10
    row["gaussian_width_m"]=.332216*math.sqrt(radius*sep/(10*d0))
    row["shop_cap_mm"]=assumptions["conditional_shop_caps_mm"][str(radius)]
    row["small_patch_RMS_mm"]=row["shop_cap_mm"]*row["gaussian_width_m"]/(math.sqrt(8)*radius)
    shapes.append(row)
    overlap=assumptions["scarf_ratio"]*tf
    W,L=assumptions["blank_width_m"],assumptions["blank_length_m"]
    panels=math.ceil(area/((W-overlap)*(L-overlap)))
    blanks=2*panels
    blankmass=blanks*W*L*tf*rho
    seam=2*area*(1/(W-overlap)+1/(L-overlap))
    for scenario,rates in assumptions["cost_rates"].items():
        declared={x["item"]:float(x["USD_2026_planning"]) for x in csvrows
                  if int(x["R_m"])==radius and x["scenario"]==scenario}
        purchase=blankmass/rates["purchased_stock_yield"]
        # The rates declare R10 hall/handling costs but no scaling exponent.
        # Treat the larger-radius allowance lines as supplied assumptions;
        # infer/report the exponent rather than inventing their source.
        hall=declared["assembly_hall_provision"]
        handling=declared["handling_transport_and_setup"]
        lines={
            "flat_Be_stock_including_purchase_loss":purchase*rates["Be_USD_kg"],
            "face_forming_and_supplier_preparation":blanks*rates["forming_hours_per_face"]*rates["labor_USD_hour"],
            "core_material_and_profile_machining":area*tc*rates["core_USD_m3"],
            "joining_materials":b["charged_joining"]*rates["joining_USD_kg"],
            "panel_bond_cure_labor":panels*rates["bond_hours_per_panel"]*rates["labor_USD_hour"],
            "two_face_scarf_assembly_labor":seam*rates["seam_hours_per_m"]*rates["labor_USD_hour"],
            "retained_shape_hardware_materials":area*.02*rates["shape_hardware_USD_kg"],
            "temporary_jig_fabrication":area*rates["temporary_jig_kg_m2"]*rates["jig_USD_kg"],
            "metrology_and_NDE":rates["metrology_fixed_USD"]+area*rates["metrology_USD_m2"],
            "finish_and_primer":area*rates["finish_USD_m2"],
            "mooring_pad_fabrication":b["mooring_pad"]*rates["pad_USD_kg"],
            "systems_ground_vacuum_and_consumables":rates["systems_and_service_USD"],
            "assembly_hall_provision":hall,
            "handling_transport_and_setup":handling,
            "coupon_process_and_subscale_qualification_allowance":rates["qualification_USD"],
        }
        total=sum(lines.values())*(1+rates["cost_contingency_fraction"])
        costs.append({"R_m":radius,"scenario":scenario,"blank_count":blanks,
                      "blank_stock_before_process_loss_kg":blankmass,"purchased_Be_kg":purchase,
                      "two_face_seam_m":seam,"independent_items_USD":lines,
                      "independent_total_USD":total,"owner_total_USD":declared["total_USD"],
                      "difference_USD":total-declared["total_USD"],
                      "max_line_difference_USD":max(abs(v-declared[k]) for k,v in lines.items()),
                      "hall_exponent_inferred_not_declared":None if radius==10 else math.log(hall/rates["hall_R10_USD"])/math.log(radius/10),
                      "handling_exponent_inferred_not_declared":None if radius==10 else math.log(handling/rates["handling_R10_USD"])/math.log(radius/10),
                      "tag":"PROJECTION; conditional arithmetic, not supplier pricing"})
    for weather in ("ISA","optimistic"):
        b,lift,source_id=bill(radius,weather)
        o=next(x for x in owner["whole_mass_bills"] if x["R_m"]==radius and x["weather"]==weather)
        assert all(abs(v-o["baseline_bill_kg"][k])<1e-9 for k,v in b.items())
        growth={}
        inherited_growth={}
        for k,mass in b.items():
            item=classes[k]
            rate=0 if item["type"] is None else {"structure":.15,"hardware":.30,"thermal":.20}[item["type"]]
            own=item["own_margin"]
            # Additional growth to reach the declared total allowance should
            # act on mass before its embedded margin, rather than the margined mass.
            growth[k]=(mass/(1+own))*max(0,rate-own)
            inherited_growth[k]=mass*max(0,rate-own)
        addition=area*assumptions["retained_shape_hardware_kg_m2"]
        additional_growth=addition*assumptions["shape_hardware_MGA_fraction"]
        corrected=lift-sum(b.values())-sum(growth.values())-addition-additional_growth
        inherited=lift-sum(b.values())-sum(inherited_growth.values())-addition-additional_growth
        diff=corrected-o["payload_with_concept_MGA_kg"]
        assert abs(inherited-o["payload_with_concept_MGA_kg"])<1e-8
        masses.append({"R_m":radius,"weather":weather,"source_case":source_id,
                       "owner_payload_kg":o["payload_with_concept_MGA_kg"],
                       "independent_inherited_arithmetic_kg":inherited,
                       "corrected_embedded_margin_payload_kg":corrected,
                       "corrected_minus_owner_kg":diff,"growth_detail_kg":growth,
                       "shape_mass_kg":addition,"shape_growth_kg":additional_growth,
                       "owner_coating_increment_kg":inherited_growth["coating"],
                       "correct_coating_increment_kg":growth["coating"],
                       "no_float_sign_preserved":corrected<0,
                       "tag":"PROJECTION"})
        if abs(diff)>1e-8:
            fixes.append({"id":f"FIX-A1-062-COATING-R{radius}-{weather}",
                          "card":"062","row":{"R_m":radius,"weather":weather},
                          "field":"payload_with_concept_MGA_kg",
                          "card_value":o["payload_with_concept_MGA_kg"],"reviewer_value":corrected,
                          "difference_kg":diff,
                          "cause":"Inherited 057 coating growth applies the extra 10% to mass already carrying 10%, giving 21% total instead of the stated 20%. Divide by 1.1 before adding the excess.",
                          "decision_effect":"All six signs remain negative; no float/no-float decision changes.",
                          "review_status":"unreviewed correction; one review round"})

field=json.loads((ROOT/"FIELD-CHECK.json").read_text())
peaks={x["case"]:x["peak"]["pressure_MPa"] for x in field["pressure_path_checks"]}
refined=field["best_reconstruction"]["pressure_from_equilibrium_MPa"]
ratios={"refined_gap_to_paper_percent":100*(refined/6.03-1),
        "contact_mesh_refinement_percent":100*(peaks["indent-mid192p30k-pressure"]/peaks["indent-mid96p30k-pressure"]-1),
        "penalty_doubling_percent":100*(peaks["indent-mid96p60k-pressure"]/peaks["indent-mid96p30k-pressure"]-1),
        "indentation_range_MPa":[min(peaks.values()),max(peaks.values())],
        "paper_normalization":6.03/27.53,
        "foam_initial_pure_shear_screen_MPa":1.4*math.sqrt((1+4.5/9)/3)}
results={"tag":"QUESTIONABLE / PROJECTION","shape":shapes,"cost":costs,"mass":masses,
         "056_ratios":ratios,"owner_code_read_or_executed":False,
         "method":"Independent arithmetic from pinned 047/CHECK047/057 inputs and declared planning rates; two hall/handling allowance lines retained as supplied assumptions."}
(ROOT/"ACCOUNT-CHECK.json").write_text(json.dumps(results,indent=2,allow_nan=False)+"\n")
(ROOT/"FIXES.json").write_text(json.dumps({"unit":"vacuum-review-a-056-062-1020","status":"unreviewed corrections","items":fixes},indent=2)+"\n")
for x in shapes:
    print("SHAPE",x["R_m"],next(z["amplitude_mm"] for z in x["tolerances"] if z["SF"]==1.05 and z["with_cure"]),flush=True)
for x in costs:
    print("COST",x["R_m"],x["scenario"],x["independent_total_USD"],"difference",x["difference_USD"],flush=True)
for x in masses:
    print("MASS",x["R_m"],x["weather"],x["owner_payload_kg"],"corrected",x["corrected_embedded_margin_payload_kg"],flush=True)
print("RATIOS",json.dumps(ratios),flush=True)
