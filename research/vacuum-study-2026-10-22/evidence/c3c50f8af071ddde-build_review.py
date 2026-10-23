from check_model import *
from datetime import datetime,timezone
import csv,hashlib
def load(name):return json.loads((ROOT/name).read_text())
def lines(name):return [json.loads(x) for x in (ROOT/name).read_text().splitlines()]
pinned=lines("SEARCH-PINNED.jsonl");independent=lines("SEARCH-INDEPENDENT.jsonl")
ledger=list(csv.DictReader((ROOT/"LEDGER-COMPARISONS.csv").open()))
mode=list(csv.DictReader((ROOT/"MECHANICS-COMPARISONS.csv").open()))
supp=list(csv.DictReader((ROOT/"SUPPLEMENT-COMPARISONS.csv").open()))
validation=load("VALIDATION.json");corrections=load("CORRECTED-SEARCHES.json")
density=load("LEDGER.json")["density_corrections_fixed_geometry"]
finite_ep=[x for x in pinned if x["endpoint"] and x["owner"]["endpoint_all_kg"] is not None]
finite_least=[x for x in pinned if x["least"] and x["owner"]["least_usage"] is not None]
stats=dict(account_configurations=648,fixed_geometry_records=load("LEDGER-SUMMARY.json")["records"],
    ledger_comparisons=len(ledger),
    mass_and_joining_max_abs_kg=max(abs(float(x["delta"])) for x in ledger if ".vacuum" not in x["kind"]),
    pressure_factor_max_abs_difference=max(abs(float(x["delta"])) for x in ledger if x["field"]=="pressure_SF"),
    pinned_thermal_search_configurations=len(pinned),
    pinned_thermal_finite_endpoints=len(finite_ep),pinned_thermal_finite_least=len(finite_least),
    pinned_thermal_endpoint_max_abs_kg=max(abs(x["endpoint"]["payload_kg"]-x["owner"]["endpoint_all_kg"]) for x in finite_ep),
    pinned_thermal_usage_max_abs=max(abs(x["least"]["usage"]-x["owner"]["least_usage"]) for x in finite_least),
    pinned_mechanics_comparisons=sum(x["basis"]=="pinned" for x in mode),
    pinned_mechanics_max_abs=max(abs(float(x["delta"])) for x in mode if x["basis"]=="pinned"),
    independent_thermal_search_configurations=len(independent),supplement_comparisons=len(supp),
    dense_endpoint_max_abs_kg=max(abs(x["endpoint_payload_delta"]) for x in validation["dense_corrected_searches"]),
    independent_thermal_50C_no_geometry=sum(x["endpoint"] is None and "50 C" in x["construction"] for x in independent))
assert len(independent)==648 and len(pinned)==208
assert stats["mass_and_joining_max_abs_kg"]<1e-6
assert stats["pinned_thermal_endpoint_max_abs_kg"]<.001
assert stats["pinned_thermal_usage_max_abs"]<1e-6
assert stats["pinned_mechanics_max_abs"]<1e-8
assert validation["AlBeMet_R15_old_coating_witness"]["point"]["payload_kg"]>10
shortfalls=[]
for face in ["K13D2U QI","M55J QI","AlBeMet AM162"]:
    key=next(k for k,c in CONS.items() if c["face"]==face and c["core"].startswith("CR-III") and (face.startswith("AlBe") or c["cure_K"]==298.15))
    for R in [15,20,30]:
        x=next(x for x in ROWS if x["construction"]==key and x["R_m"]==R and x["weather"]=="ISA" and not x["floor"] and x["finish"]=="MLCCAg" and x["variant"]=="primary")
        g=x["endpoint_all_geometry"];v=bill(props(key),R,g["tf_m"],g["tc_m"])["payload_kg"]
        y=next(y for y in independent if y["construction"]==key and y["R_m"]==R and y["weather"]=="ISA" and not y["floor"] and y["finish"]=="MLCCAg" and y["variant"]=="primary")
        shortfalls.append(dict(face=face,R_m=R,owner_kg=x["endpoint_all_kg"],checker_ledger_kg=v,
                              independent_thermal_reoptimized_kg=y["endpoint"]["payload_kg"] if y["endpoint"] else None))
fix=next(x for x in density if x["R"]==30 and x["weather"]=="ISA" and x["kind"]=="least")
changed=next(x for x in corrections if x["variant"]=="density1800" and x["R_m"]==30 and x["weather"]=="ISA")
baseline=next(x for x in corrections if x["variant"]=="original" and x["R_m"]==30 and x["weather"]=="ISA")
new_supply=changed["least"]["point"]["bill_kg"]["faces"]*(11/15)/1.4e6
owner50=next(x for x in ROWS if "50 C" in x["construction"] and x["R_m"]==30 and
             x["weather"]=="ISA" and not x["floor"] and x["finish"]=="MLCCAg" and x["variant"]=="primary")
findings=[
dict(id="NFI-CHECK049-DENSITY",kind="model-input inconsistency",blocking=False,tag="PROJECTION",
 row="K13D2U QI at 60% Vf; all radii and variants",field="density_kg_m3 / fibre_mass_fraction",
 owner=[1725.4901960784314,.67],checker=[1800.,11/15],
 evidence="The stated 2200/1200 constituent densities give Vf=.525490196 at 67 wt% fibre, not .6.",
 impact=fix,fix="Use one consistent volume/weight mixture and rerun geometry, water, payload and supply. Preserve the separate 33 wt% resin baseline."),
dict(id="NFI-CHECK049-NONMONOTONE-E",kind="numerical search counterexample",blocking=False,tag="PROJECTION",
 row="CARD section 6; AlBeMet/5056/200 F, R15 ISA actual joining, reference040 coating",
 field="E_multiplier_to_float",owner="none up to x8",
 checker=validation["AlBeMet_R15_old_coating_float_interval"],
 witness=validation["AlBeMet_R15_old_coating_witness"],
 fix="Scan/refine interior E intervals; thermal stress makes endpoint-only exclusion invalid. This formal high-E target does not establish available AlBeMet."),
dict(id="NFI-CHECK049-THERMAL-CLOSURE",kind="reproducibility / model dependence",blocking=False,tag="PROJECTION",
 row="folded K13D2U 60% Vf /5056/50 C, R30 ISA endpoint",field="free-edge SF",
 owner=owner50["endpoint_all_modes"]["thermal_core_interface_screen"],checker=.9596642430419865,
 evidence="Independent explicit thermal boundary gives Tmin=268.358318334 K at this geometry. Pinned-table arithmetic agrees where tables exist; the full owner heat boundary remains unspecified.",
 fix="Publish complete non-code convection, sky/ground views, enclosure exchange and all 049 tables; retain both interpretations as sensitivities until closed."),
dict(id="NFI-CHECK049-BE-SCREEN-E",kind="screen reference clarification",blocking=False,tag="PROJECTION",
 row="Be own endpoint thermal screen; R15 ISA",field="full_cycle_SF",
 owner=1.399191044592521,checker=1.3905864399946701,
 evidence="Owner retains 290 GPa in the rigid-face screen at a 293.6 GPa endpoint geometry. The ratio is sqrt(290/293.6); both pass.",
 fix="State that the comparison uses baseline E, or consistently use the endpoint E. No change in float decision."),
dict(id="NFI-CHECK049-SERVICE-TRANSFER",kind="unqualified physical transfer",blocking=False,tag="PROJECTION",
 row="all CFRP constructions",field="whole-area gas permeation and nominal face volatiles",
 owner="inherited metal-shell service construction",checker="not established for CFRP",
 evidence="The exact pressure reconstruction retains the inherited 70 g/m² scarf permeation gap despite the 146 g/m² CFRP seam. A face-specific gap changes SF by <.000057. Whole-area CFRP permeance is a separate unresolved term.",
 fix="Measure the actual face/finish barrier and volatile inventory; document the scarf path consistently. Keep unknowns as NFIs, not zero qualification."),
dict(id="NFI-CHECK049-SOURCE-QUALIFICATION",kind="source limitations carried forward",blocking=False,tag="QUESTIONABLE / PROJECTION",
 row="face/core/bond/finish construction",field="installed allowables",
 owner="calculated, transferred and projected properties as disclosed",checker="sources checked; installed qualification remains absent",
 evidence="K13 Xc=220 MPa is unsourced; M55 QI numbers are calculated; AlBeMet/Be tensile values are transferred. Cold cure and biaxial strength remain projections. 585 GPa E1 is a cross-fibre empirical translation.",
 fix="Ground joint-specific and laminate-specific properties and temperature/drying processes. Keep the 3 GPa resin calculation as a separate hypothetical sensitivity."),
dict(id="NFI-CHECK049-PROVENANCE",kind="metadata correction",blocking=False,tag="QUESTIONABLE",
 row="COMPUTE.faces and COMPUTE.cores",field="nested source/family/nu_basis/strength_basis",
 owner="copied Be and aluminum descriptions",checker="actual CFRP/aramid top-level properties differ",
 fix="Replace stale copied provenance. Use the printed HRH-49 30 psi W minimum, or explicitly retain the conservative 28.571 psi projection."),
dict(id="NFI-CHECK049-SUPPLY",kind="denominator and allocation limits",blocking=False,tag="QUESTIONABLE / PROJECTION",
 row="R30 supply comparison",field="share of supply",
 owner="433 t Be mine production; 1400 t continuous pitch capacity",checker="denominators verified, allocation unverified",
 evidence="Original share arithmetic matches the original 67 wt% assumption. At the original geometry the density-corrected pitch fraction is 5.50926357%; at the independent reoptimized corrected least point it is "+str(new_supply*100)+"%.",
 fix="Separate mine content, fibre capacity and finished-product availability. Obtain grade-specific production, allocation and manufacturing yield. The broader all-carbon market figures were not independently confirmed from a primary market report.")
]
result=dict(schema=1,card="CHECK-049",unit="vacuum-mainline049-check-1020",
 status="CHECK COMPLETE WITH NONBLOCKING CORRECTIONS; not an unconditional numerical/physical pass",
 owner_code_read=False,owner_code_executed=False,task_time_limit=None,phase_time_limit=None,
 coverage=stats,shortfalls=shortfalls,density_fixed_geometry=fix,
 corrected_search_R30_ISA=changed,matching_independent_baseline_R30_ISA=baseline,
 corrected_reoptimized_pitch_capacity_share=new_supply,
 scalar_checks=load("LEDGER.json")["scalar_checks"],property_precision=load("PROPERTY-PRECISION.json"),
 findings=findings,artifacts={
 "literal_ledger":"LEDGER-COMPARISONS.csv","conditional_mechanics":"MECHANICS-COMPARISONS.csv",
 "pinned_searches":"SEARCH-PINNED.jsonl","independent_searches":"SEARCH-INDEPENDENT.jsonl",
 "density_searches":"CORRECTED-SEARCHES.json","thermal_and_service":"SUPPLEMENT.json",
 "modulus_targets":"MODULUS-TARGETS.json","validation":"VALIDATION.json","sources":"SOURCE-AUDIT.md"})
(ROOT/"RESULTS.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
(ROOT/"NFI.json").write_text(json.dumps(dict(schema=1,unit=result["unit"],blocking=False,items=findings),indent=2)+"\n")
print(json.dumps(stats,indent=2));print("reoptimized pitch fraction",new_supply)
