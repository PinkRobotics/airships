#!/usr/bin/env python3
"""030d additive synthesis using 030c's preserved register and source workflow."""
import copy
import math
from pathlib import Path
from intake import B, Q, load, save, pin

BASE=B/"baseline030c"
UNIT="vacuum-mainline030d-design-register-1020"
REPORT="rpt-ref-e999413f5ed23130ebf6"
TAG="QUESTIONABLE / PROJECTION"
intake=load(B/"INTAKE.json")
reports={r["id"]:r for r in intake["reports"]}
baseindex=load(BASE/"SOURCE-INDEX.json")
allreports={}
for group in ("baseline","additions","additions_030c"):
    allreports.update({r["id"]:r for r in baseindex[group]})
allreports.update(reports)
ALIASES={
    "040fold":"rpt-ref-378f34abc5a6eea5b053",
    "043fold":"rpt-ref-14993e3c2e5e64177c8f",
    "CHECK042":"rpt-ref-049190971618f3ca1e72",
    "045":"rpt-ref-57c98dcce7960aca042a",
    "046":"rpt-ref-b6da4592385c83f4db2a",
    "CHECK040":"rpt-ref-593068c3ed82fd458128",
    "048":"rpt-ref-2092a3e39c7141afde61",
    "CHECK044":"rpt-1228-mainline044-independent-check-1020",
    "CHECK043":"rpt-ref-a53ddf165139979127c4",
    "CHECK041":"rpt-ref-52963d63a80d69bb90bd",
    "CHECK046":"rpt-ref-982a0ff761f72abce96c",
    "048fold":"rpt-ref-9a9a131b4ca724b68cc2",
    "050exception":"rpt-1228-mainline050-simjob-refusal-retry-request-1020",
    "CHECK048partial":"rpt-ref-29ebe6d900e7cbd982ea",
    "051partial":"rpt-ref-8d5027d15bbe034522e3",
    "CHECK045":"rpt-ref-e0fc07c506c86dae19c1",
    "052":"rpt-ref-d7b2450119f373b2d1db",
    "050":"rpt-1228-mainline050-flyable-weather-1020",
    "020":"rpt-ref-3e02218a03708a878faa",
    "040":"rpt-ref-b10363665c6202d8ef75",
    "044":"rpt-ref-29830021a6e140ff7411",
}
def artifact(alias,name):
    r=allreports[ALIASES[alias]]
    a=next(a for a in r["artifacts"] if Path(a["path"]).name==name)
    # Prefer this register's immutable local snapshots.
    candidate=B/"snapshots"/r["id"]/name
    if not candidate.exists():
        candidate=Path(a.get("snapshot",a["path"]))
        original=Path(load(B/"BASELINE-PINS.json")["original_root"])
        if candidate.is_relative_to(original):
            candidate=BASE/candidate.relative_to(original)
    return a,candidate
def source(alias,name):
    return load(artifact(alias,name)[1])
def ref(alias,name,pointer="/"):
    a,p=artifact(alias,name)
    return dict(report=ALIASES[alias],file=str(p),original_file=a["path"],
                sha256=a["sha256"],selector=pointer)

change_text={
 "040fold":("040/037b fold confirmed",
   "All as-designed 250°F rows fail the minimum-strength free-edge screen. Geometry-specific 200°F/scarf repair is distinct from the original +0.120151 kg allowance; positive conditional payload is not an assembly qualification."),
 "043fold":("043 uses the direct 041 f5 frames",
   "At their own screens, m=10 and assumed 3.9 GPa complete-member scale give Pf .002524/.002143; interpreting 3.9 GPa at 1 cm³ instead gives .991133/.979046. These are different uncalibrated populations."),
 "CHECK042":("Build-route values corrected by CHECK-042",
   "S-II .254 mm is a core-face matching gap, not spherical error. Simply supported critical disbond is 27.127598 mm. Two-skin seams total 5683.037–5685.225 m with at least 1190 panels per skin at 30.34:1. The 200°F data do not qualify the specified bond."),
 "045":("Damage requirement added for both leads",
   "028b/022d damage models find no priced damage-tolerant float on their original budgets. Local crushed-core growth and member-loss/film-tear screens consume the intact margins. Transfer to 048/041 geometry requires reclosure; no operating protocol is qualified."),
 "046":("P3 film life and protection charged",
   "No installed film life is demonstrated. At 041, OD4/white protection is 95.751 kg; hot-film corrections plus equipment leave 31.465–51.465 / 39.916–59.916 kg closure deficits. Ten-year SF depends on the unselected ageing law."),
 "CHECK040":("Common-account sensitivities and thermal limit retained",
   "Arithmetic matches conditional on the owner temperature table; independent thermal reproduction remains open. One millimetre of water removes every original primary float. Cure in global/crimp demand gives R15 optimistic actual −1.821 kg; edge/scarf coincidence removes four of thirteen primary floats."),
 "048":("Light coating recovers conditional R10 ISA float",
   "Multilayer CCAg/ITO at 7.5752 g/m² plus 10%, separate 10 g/m² structural primer, .1 kg/m² exterior water and a distinct material-water inventory give +124.262 kg at the original R10 ISA bake endpoint. Optics and process transfer remain unqualified."),
 "CHECK044":("Film label and pad credit corrected",
   "The .060 fatigue-test film is AF163-2K. The +36.661200 kg strict-pad/60:1-scarf scenario requires 3.414034 kg old-plate credit; without documented credit the addition is +40.075234 kg. Installed life stays null."),
 "CHECK043":("Proof and mass labels corrected",
   "At 1.25× target force the member Euler ratio is .375, not buckling. Exceeding the combined screen does not establish Euler failure; fixtures and stress coverage remain open. Required Pf10⁻⁶ member scales are 8.53751/8.39866 GPa. Rise8 is 5446.291 kg total, 5039.558 kg tubes."),
 "CHECK041":("Direct-frame computation corroborated with exact limits",
   "Fixed f5 screens 1.143285/1.083205 and local sensitivities 1.033223/.978132 reproduce. Independent nonlinear continuation corroborates the m24 bracket. Nine printed cells differ, including film-direction and midpoint values; prior postprocessor exposure is disclosed."),
 "CHECK046":("Film-life audit adds quantitative limits",
   "Required retention and ten-year scenarios reproduce. Coupon-only 458.672527 kg/year becomes 459.261468 with weighted leakage. Warehouse reading uncertainty crosses SF1 at both f5 points; hot 041-5 annual loss ceiling is .457%, below the .5% requirement."),
 "048fold":("CHECK-040 folded into 048",
   "648 new rows include cure compression and both water scenarios. All 432 1 mm R10–15 cases fail to float; best all-four is −998.333 kg. Cure-included R10 ISA bake is +118.695 kg, least G+Q+film usage .842794; two marginal floats are lost. Exact 2U .015 bond qualification stays open."),
 "050exception":("050 operational exception retained as history",
   "A canonical exception report records refusal before execution and a request for retry authority. The subsequently filed050 card reports authorized unchanged retries and completion. The exception itself supplies no numerical result."),
 "CHECK048partial":("Partial CHECK-048: supplied bill matches; full check remains open",
   "At7149 stored points, compared bills/modes/payloads match conditional on owner thermal tables. The+124.261910kg R10 bill reproduces. Three vacuum bookkeeping fields differ; proposed corrections are unverified. Thermal297/325 comparisons differ and independent searches are unfinished. The classical optical citation gives alpha.08/normal epsilon.72 on Kapton, not the model's.09/.65."),
 "051partial":("Partial 051: load-specific member targets complete, candidate frames pending",
   "All288 reliability target rows are filed. Under assumed member-scale3.9GPa/m10, q1 Pf=.000643916/.000947308 meets1e-3, while own-screen Pf does not. Own-screen Pf1e-3 scales are4.278678/4.209090GPa; candidate masses/SFs and041damage remain null. Old f5 stress amplification2.427/2.480 differs from f4's3.27."),
 "CHECK045":("CHECK-045 corrects damage arithmetic and limits categorical claims",
   "Main danger screens reproduce;1358 comparisons include71 differences and88 exact findings. The55mm growth threshold is19.176311mm within the core; Pach calibration does not agree. PerrySF is3.454499, not4.095818. Better wall/tear witnesses remain below1. All-edge stress ratios1.959485–3.270739 and trajectory/inspection corrections do not establish universal cascade or a safe vent protocol."),
 "052":("052 closes a conditional P3 whole bill with additional strength assumptions",
   "Resized f5-019 first closes at tested R10 ISA/R12 optimistic with ground service; full endpoints +30.863/+46.259kg. R10 least S+F+J usage.839340 requires5.343GPa effective ply strength and planned15.552h ground service. No combined-weather or24h onboard-dry case closes throughR30. Its original048 comparison is supplemented with the cure-included account and the same extra50kg service debit."),
 "050":("050 separates weather design families from one fixed hull",
   "The2,027,245-point map extends the original048 finish account throughR30. No sampled radius closes the declared MIL10% hot profile, even at all four endpoints. At100m the full-range fixed R10/R30 upper ISA offsets are−6.5/+3.3K, versus family+5.8/+15.8K; cold limit about−10.5K. R10 saturated-clear dew gives−82.280kg. The cure-included alternate and operational probabilities remain unqualified."),
}
assert set(reports)=={ALIASES[k] for k in change_text},"New report requires semantic disposition"
changes=[dict(report=ALIASES[a],alias=a,title=t,text=s,tag=TAG)
         for a,(t,s) in change_text.items()]
save(B/"CHANGES.json",changes)

# Extract source values without importing or running any numerical model.
new48=source("048fold","RESULTS.json")
old48=source("048","RESULTS.json")
ix48={x["id"]:x for x in new48["rows"]}
ixold={x["id"]:x for x in old48["rows"]}
selected=[]
for r in (10,12,15):
    for weather in ("ISA","optimistic","both"):
        for floor in (False,True):
            stem=f"MLCCAg-R{r}-{weather}-{'floor' if floor else 'actual'}-bake70-retained_water"
            new=ix48[stem+"-cure_included"]
            old=ixold[stem]
            selected.append(dict(
                id=new["id"],R_m=r,weather=weather,floor=floor,tag=TAG,
                source=ref("048fold","RESULTS.json",f"/rows/{new48['rows'].index(new)}"),
                original_endpoint=old["two_factor_endpoint"],
                cure_included_endpoint=new["two_factor_endpoint"],
                least=new["least"]["least"],
                all_four_endpoint=next(t["solution"] for t in new["least"]["endpoint_trials"] if t["mask"]==15),
                dependencies=["MLCCAg dry optical properties transferred to Be",
                  "7.5752 g/m² recipe plus 10% allowance","separate 10 g/m² structural primer",
                  "0.1 kg/m² optimistic exterior retained-water scenario",
                  "90% removal target for added absorbed material water, no exterior-service credit",
                  "200°F stress-free state and unqualified 2U adhesive/Be/honeycomb process",
                  "selected gamma/Q/film axes; scalar mechanical and thermal model",
                  "vented cells, resized 70 kn pad, full gas and contamination charges",
                  "30–50 kg sealed daily service nested in the 100 kg systems inventory",
                  "weather-specific lift and load envelope; chosen joining convention"],
                qualified_installed_hull_SF=None))
primary=next(x for x in selected if x["R_m"]==10 and x["weather"]=="ISA" and x["floor"])
save(B/"P2-048-ACCOUNT.json",dict(
    tag=TAG,rows=selected,primary=primary,
    water_one_mm=dict(source=ref("048fold","RESULTS.json"),
        configurations=432,best_all_four=new48["best_one_mm_all_four"],
        favorable_upper=new48["best_one_mm_favorable_upper"]),
    lost_floats=new48["lost_float_configurations"],changed_axis_count=new48["changed_axis_count"],
    scope="This cure-included finish account covers R10/12/15. Original040 R30 and050's original048-account extension are separate; no common cure-inclusive R10–30 optimum is claimed.",
    bond_NFI="AF163-2K .060 metal-joint 200°F tests do not qualify 2U .015 Be/5056 honeycomb.",
    overall_installed_hull_SF=None))

raw52=source("052","RESULTS.json")
rows52=[]
for i,row in enumerate(raw52["rows"]):
    keep={k:copy.deepcopy(row[k]) for k in (
        "R_m","weather","service","baseline","all_axes_endpoint","least","least_axis_count")}
    keep.update(tag=TAG,source=ref("052","RESULTS.json",f"/rows/{i}"))
    rows52.append(keep)
primary52=next(x for x in rows52 if (x["R_m"],x["weather"],x["service"])==(10,"ISA","ground"))
comparison52=[]
for row in selected:
    point=row["all_four_endpoint"]
    comparison52.append(dict(R_m=row["R_m"],weather=row["weather"],floor=row["floor"],
        source=row["source"],endpoint_mask=point["mask"],
        cure_included_all_four_payload_kg=point["signed_payload_kg"],
        additional_service_kg=50.0,
        same_extra_vacuum50_payload_kg=point["signed_payload_kg"]-50.0,
        interpretation="Arithmetic at the filed all-four point; same additional 50 kg service allocation as052, no P2 reoptimization or common qualification."))
account52=dict(tag=TAG,source=ref("052","RESULTS.json"),rows=rows52,primary=primary52,
    axes=raw52["axes"],sensitivities=source("052","SENSITIVITIES.json"),
    original_P2_comparison=source("052","P2-COMPARISON.json"),
    original_P2_comparison_source=ref("052","P2-COMPARISON.json"),
    cure_included_P2_comparison=comparison52,
    original_comparison_limit="052 used original048 without the filed cure-demand alternative; retain its values as source history and use the separately labelled cure-inclusive allocation view for that correction.",
    family="Checked f5-019 force/eigen family, constant gyration/radius, resized area with peak local buckling enforced; not the original041 geometry or a topology optimum.",
    dependencies=["Unqualified complete-member compression strength/distribution",
        "Unqualified effective PBO ply strength and installed ten-year retention",
        "Rigid joint response and sized sleeves, installation and node allowances",
        "OD4/white protection includes the034 barrier once",
        "100 kg systems plus additional50 kg ground-service inventory",
        "Dry initial fill, assumed90% material conditioning, transferred leakage and humidity target",
        "Ground interval follows humidity, not merely total-pressure limit",
        "0.1 kg/m² exterior water, vented bores, explicit gas/weather/contamination replace bulk reserve",
        "P2-derived mooring allowance is not a qualified P3 hardpoint",
        "Damage resistance, thermal/local/global interaction and manufactured scaling remain open"],
    qualified_installed_hull_SF=None,qualified_hull_life=None,qualified_failure_probability=None)
save(B/"P3-052-ACCOUNT.json",account52)
weather50=dict(tag=TAG,source=ref("050","RESULTS.json"),results=source("050","RESULTS.json"),
    inputs=source("050","INPUTS.json"),fixed_hulls=source("050","FIXED-HULLS.json"),
    dew_frost=source("050","DEW-FROST.json"),design_days=source("050","DESIGN-DAYS.json"),
    validation=source("050","VERIFICATION.json"),
    account_scope="050 extends the original048 account and reproduces its R10 +124.262kg endpoint. It does not claim a rerun of the separately filed048 cure-included alternative. Thus no cure-inclusive R20/R30 weather ranking is inferred.",
    interpretation="Design-family boundaries allow different geometries. Fixed-hull boundaries retain one full-range build mass and stress screen. Marginal design-day percentiles are not annual flight probabilities; wet optics, drainage, installed water-control cost and physical cold/thermal validation remain open.",
    qualified_installed_hull_SF=None,qualified_operational_availability=None)
save(B/"P2-WEATHER-050.json",weather50)

base_results=load(BASE/"RESULTS.json")
old40=source("040","RESULTS.json")
r30=next(x for x in old40["rows"] if x["id"]=="R30-ISA-actual-heavy70-vented")
be=r30["two_factor_endpoint"]["bill_kg"]["faces"]
supply=dict(tag=TAG,source=ref("040","RESULTS.json",f"/rows/{old40['rows'].index(r30)}/two_factor_endpoint/bill_kg/faces"),
            output_source=ref("020","CARD.md","Supply and price"),
            R_m=30,point="original 040 ISA actual named endpoint",Be_faces_kg=be,
            world_output_2024_revised_t=433,world_output_2025_estimate_t=430,
            share_2024=be/433000,share_2025=be/430000,
            least_usage_point_faces_kg=next(x["point"]["bill_kg"]["faces"]
                for x in base_results["P2_common_account_040"]["necessary_points"]
                if x["id"]=="R30-ISA-actual-heavy70-vented"),
            interpretation="Historical mine-output Be content, not current output, available stock, finished-sheet capacity or purchase commitment.")
save(B/"BERYLLIUM-SUPPLY.json",supply)

c43=source("CHECK043","RESULTS.json")
f43=source("043fold","RESULTS.json")
probabilities=[x for x in f43["comparison"] if x["load"]=="own_screen"]
requirements=[]
for p in c43["derived"]["fold"]:
    own=next(x for x in p["loads"] if x["label"]=="own_screen")
    hazard=own["member_scale_m10"]["frame_hazard"]
    requirements.append(dict(point=p["reserve"],peak_compression_Pa=own["max_compression_Pa"],
         assumed_m=10,assumed_member_scale_Pa=3.9e9,
         required_member_scale_for_Pf1e6_Pa=3.9e9*(hazard/(-math.log1p(-1e-6)))**.1,
         hypothesis="Independent complete members with common m/scale; no qualified distribution."))
reliability=dict(tag=TAG,source=ref("CHECK043","RESULTS.json","/derived/fold"),
    probabilities=probabilities,requirements=requirements,
    proof=c43["derived"]["model_sensitivities"],
    rise8_total_kg=5446.29062569268,rise8_tubes_kg=5039.557738754902,
    proof_correction="The original member Euler ratio at 1.25× target force is .375. A combined-screen exceedance is not proof of Euler buckling.",
    qualified_frame_failure_probability=None,qualified_lifetime_failure_probability=None)
save(B/"P3-RELIABILITY.json",reliability)
partial048=dict(
    tag=TAG,status="PARTIAL; final check PENDING",source=ref("CHECK048partial","CHECK.md"),
    scope=source("CHECK048partial","SCOPE.json"),
    account=source("CHECK048partial","ACCOUNT-RESULTS.json"),
    NFI=source("CHECK048partial","NFI.json"),
    classical_optical_correction=dict(
        source_alpha=.08,source_normal_emittance=.72,source_substrate="Kapton",
        modeled_alpha=.09,modeled_emittance=.65,
        source="NASA2015 printed slide19, as audited in partialCHECK048",
        URL="https://ntrs.nasa.gov/api/citations/20150018109/downloads/20150018109.pdf",
        disposition="Correct source attribution/statistic; retain the model tuple only as an unqualified projection. No corrected-optics optimization is claimed."),
    independent_least_sets_verified=False,independent_thermal_equivalence=False)
partial051=source("051partial","RESULTS.json")
save(B/"PARTIAL-FILINGS.json",dict(
    tag=TAG,CHECK048=partial048,MAINLINE051=partial051,
    target_surface_source=ref("051partial","TARGET-SURFACE.csv"),
    material_evidence_source=ref("051partial","MATERIAL-EVIDENCE.json"),
    rule="Completed portions are attributed evidence; neither filing closes its assignment. No proposed or unexecuted correction is promoted to a result."))

d45=source("045","RESULTS.json")
d46=source("046","RESULTS.json")
c44=source("CHECK044","RESULTS.json")
c45=source("CHECK045","RESULTS.json")
life_rows=[]
for pid in ("022d-5","041-5","041-019"):
    point=next(x for x in d46["points"] if x["id"]==pid)
    laws={x["scenario"]:x for x in d46["age_table"] if x["point"]==pid and x["age_years"]==10}
    hot=next(x for x in d46["peak_service"] if x["point"]==pid and x["age_years"]==10)
    life_rows.append(dict(point=pid,initial=point,ten_year_laws=laws,ten_year_hot=hot,
        minimum_including_unchanged_local_sensitivity={
            k:min(v["film_SF"],point.get("local_peak_sensitivity_sf",point["sf0"]))
            for k,v in laws.items()},
        hot_minimum_including_unchanged_local_sensitivity=min(
            hot["full_restraint_hot_SF"],point.get("local_peak_sensitivity_sf",point["sf0"]))))
damage_life=[
 dict(card="044 / CHECK044",lead="P2",source=ref("CHECK044","RESULTS.json","/headlines"),
      mass_delta_kg=c44["headlines"]["relative_strict_pad_and_scarf_added_kg"],
      mass_without_old_plate_credit_kg=c44["headlines"]["conditional_no_old_plate_credit_added_kg"],
      credit_required_kg=3.414033639,
      least_SF_effect="Original six-pad core SF .714286; combined R10 scarf sensitivity .9891. Conditional resized pad/scarf candidate does not qualify life.",
      updated_048_least_SF=None,
      transfer_scope="044's old R10 six-pad spectrum is not 048's resized single heavy pad or R30; reprice on the selected geometry."),
 dict(card="044 / CHECK044",lead="P3",mass_delta_kg=None,least_SF_effect="Not calculated for P3 by 044; no film/frame life closure follows.",
      qualified_least_SF=None,transfer_scope="No transfer of Be/honeycomb pad or scarf result to the SiC/PBO frame."),
 dict(card="045",lead="P2",source=ref("045","RESULTS.json","/answer"),
      mass_delta_kg=None,example_shield_kg=25,
      original_028b_margin_kg=d45["answer"]["p2_mass_margin_kg"],
      vent_air_kg=d45["answer"]["p2_air_admitted_kg"],
      least_SF_effect="Crushed-core growth is a local loss of load capacity; a 25 kg shield needs usage1.021 on the old bill. Venting admits2645.660kg and ends the evacuated float condition.",
      updated_048_least_SF=None,transfer_scope="028b damage geometry and 14.581kg margin; not the new 048 coated account. Barrier protection and vent hardware are unpriced/unqualified."),
 dict(card="045",lead="P3",source=ref("045","RESULTS.json","/answer"),
      mass_delta_kg=None,example_protection_kg=100,
      lost_member_film_SF=d45["answer"]["p3_merged_bay_film_SF"],
      least_SF_effect="Lost member: filmSF.838835. CHECK045 all-edge linear stress range1.959485–3.270739; selected cases2.427–3.271. Improved old022d witnesses: 1.5mm wallsSF.805476, 2mmSF.483053, tear filmSF.975445 at848.604kg. None reaches1; not a global optimum proof.",
      checked_tear_film_kg=848.604,checked_wall_1p5_SF=.805476,checked_wall_2_SF=.483053,
      updated_041_least_SF=None,transfer_scope="Old022d section and f4/f5 member-loss surrogates; no directly qualified damaged041 capacity."),
 dict(card="046 / CHECK046",lead="P2",mass_delta_kg=None,least_SF_effect="PBO film ageing is not a Be/honeycomb life calculation.",
      qualified_least_SF=None,transfer_scope="No change to P2 SF established; 044 and bond/cure/finish life questions remain."),
 dict(card="046 / CHECK046",lead="P3",source=ref("046","RESULTS.json","/peak_service"),
      OD4_white_package_kg=95.751050702,hot_fiber_additions_kg=[.713771403,9.165385273],
      closure_delta_ranges_kg=[[31.464822105,51.464822105],[39.916435975,59.916435975]],
      least_SF_effect="At041-5/019, warehouse ten-year filmSF=.985018/.933256; hot/full-restraint target=.995706/.944784. These fall below the unchanged intact screens. A film-only SF1 fix does not restore the019 local-shell sensitivity .978132.",
      qualified_least_SF=None,transfer_scope="Direct041 film geometry, with frame held fixed and reserve retained; whole-vehicle reclosure still open.")
]
for row in damage_life:row.update(tag=TAG,qualified_installed_life=None)
save(B/"DAMAGE-AND-LIFE.json",dict(
    tag=TAG,rows=damage_life,damage_answer_045=d45["answer"],film_life_rows=life_rows,
    pad_life_044=c44["headlines"],
    CHECK046_water=dict(coupon_water_kg_year=458.672527,with_weighted_leakage_kg_year=459.261468),
    CHECK045=dict(
        results=c45,source=ref("CHECK045","CARD.md"),
        exact_findings=ref("CHECK045","MISMATCHES.json"),
        findings=source("CHECK045","MISMATCHES.json"),
        corrections=dict(clamped_55mm_growth_depth_mm=19.176311,
          source_core_depth_mm=23.237218,pach_measured_m=.0011,
          modeled_Pach_depth_mm=[1.489,1.541],measured_Pach_depth_mm=[1.1,1.2],
          IEC_printed_35_55_65mm_masses_g=[20.7,80.2,132.0],
          corrected_Perry_SF=c45["p3_perry_SF"],
          exact_independent_half_failure_counts=[60.877292,12.784859],
          all_edge_class_stress_range=[1.959485,3.270739],
          all_edge_class_tension_range_MPa=c45["p3_all_orbits_tension_range_MPa"],
          improved_wall_SF={"1.5mm":.805476,"2mm":.483053,"3mm":.223304},
          improved_tear_SF=.975445,improved_tear_film_kg=848.604,
          half_kg_event_100mm_hole_s=.464206,torn_bay_half_kg_event_s=.000837478,
          ground_first_contact_centre_m=10,
          ground_contact_torn_bay_speed_m_s=[23.099647,34.541863],
          sea_level_vent_air_kg=2912.791114),
        no_universal_dynamic_cascade_or_puncture_claim=True,
        no_installed_damage_tolerance=True),
    all_costs_are_scenario_costs=True,qualified_hull_SF=None,qualified_lifetime=None))

# Preserve every old field. Current annotations and findings are added.
register=copy.deepcopy(load(BASE/"REGISTER.json"))
topics=[
 ("R099","Exterior finish","Installed coating mass, optical transfer and wet optical state"),
 ("R100","Water and conditioning","Exterior retention versus absorbed material water and dry-out"),
 ("R101","P2 local damage","Crushed-core dent growth, face damage and operating response"),
 ("R102","P3 local damage","Member loss, brittle impact, merged bays and film tears"),
 ("R103","P3 film life","Protected-film ageing, creep, loss budget and renewal"),
 ("R104","Frame reliability and proof","Finished-member statistical scale, system risk and proof coverage"),
]
for rid,title,gap in topics:
    register["rows"].append(dict(rid=rid,topic="T030D",topic_name=title,gap=gap,
        sources=[],updates_030b=[],updates_030c=[],states=["QUESTIONABLE","PROJECTION"]))
byrid={r["rid"]:r for r in register["rows"]}
for r in register["rows"]:r["updates_030d"]=[]
new=load(B/"NEW-NFI.json")
defaults={"040fold":"R098","043fold":"R104","CHECK042":"R097","045":"R101",
          "046":"R103","CHECK040":"R083","048":"R099","CHECK044":"R047",
          "CHECK043":"R104","CHECK041":"R055","CHECK046":"R103","048fold":"R100",
          "CHECK048partial":"R099","051partial":"R104","CHECK045":"R101","052":"R040","050":"R039"}
rules=[
 ("R079",("precision","labeling","rounding","nonfinite")),
 ("R104",("weibull","probability","proof","statistical","reference size","reference population","compression m")),
 ("R102",("cascade","merged-bay","member loss","tube impact","tube-impact","tube fracture")),
 ("R101",("dent","impact","bvid","puncture","damage tolerance","hole-edge")),
 ("R103",("ageing","aging","kinetics","tail shape","loss-budget","renewal","replacement","uhmwpe","creep","filament","film life")),
 ("R100",("retained-water","retained water","exterior water","material water","conditioning","drying","moisture","sorbent","desiccant")),
 ("R099",("coating","optical","finish mass","optics")),
 ("R098",("cure","residual","stress-free","cellular force","free-edge","free edge","compliant-core")),
 ("R025",("scarf","seam process","rt-seam")),
 ("R037",("seam length","spherical layout","panel count")),
 ("R027",("bond strength","adhesive","bond film")),
 ("R018",("stock","gauge","supply envelope")),
 ("R048",("beryllium supply","world output","cost","process-safety")),
 ("R088",("waviness","spectrum","metrology","roughness")),
 ("R070",("dimple map","matching gap","heritage","monocoque")),
 ("R010",("wrinkling","wrinkle","q=")),
 ("R007",("gamma","knockdown")),
 ("R086",("mooring","pad","hardpoint")),
 ("R045",("leak","permeation","vacuum-water","wvtr","gas load","descent")),
 ("R044",("service","hardware","systems","equipment")),
 ("R039",("weather","climate","terrain","altitude")),
 ("R089",("thermal","temperature","sun","heat-balance")),
 ("R063",("joint","end moment","end interface")),
 ("R091",("local-wall","local wall","local shell","tensile bending")),
 ("R055",("nonlinear","eigen","integer geometry","direct frame","frequency")),
 ("R013",("compression strength","face compression","face-tuple","elasticity")),
 ("R097",("forming","inspection","nde","jig","disbond","tap-test","tap ")),
 ("R082",("search","optimum","optimization","ranking")),
 ("R040",("mass closure","mass budget","mass credit","mass floor","mass-closure","joining floor")),
]
reverse={v:k for k,v in ALIASES.items()}
assignments={};reasons={}
overrides={
 "048F-no-fixed-surcharge":"R033","NFI-C042-MAP":"R070","NFI-C042-CORE-AIR":"R045",
 "NFI-045-HAIL-FLUX":"R102","NFI-045-REGULATION":"R090",
 "040-14-aerodynamic_pressure":"R089","040-15-unvented_cells":"R045",
 "NFI-037b-NONMETAL-CTE":"R098","NFI-037b-FOIL":"R022",
 "NFI-CHECK037b-HEX679-SUPPORT":"R027","NFI-CHECK037b-INTERLAYER-COUNT":"R098",
 "NFI-CHECK037b-DIAGNOSTIC-SCHEMA":"R079",
 "048-02-classical_emittance":"R099","048-03-Be_deposition_process":"R099",
 "048-05-white_paint_mass":"R099","048-06-film_availability":"R099",
 "048-07-film_attachment":"R099","048-18-dry_gas_process":"R100",
 "048-27-least_set_definition":"R082","NFI-CHECK044-005":"R079",
 "NFI-044-CORE-DENSITY":"R022","NFI-028b-SR200-compression":"R013",
 "NFI-028b-sheet-anisotropy":"R015","NFI-028b-primer":"R034",
 "NFI-028b-lab-bond":"R036","NFI-028b-lab-weld":"R032",
 "NFI-028b-splice-and-seal":"R030","NFI-028b-255-sensitivity":"R013",
 "NFI-CHECK037-SHELL-EQUILIBRIUM":"R089","NFI-CHECK037-P3-ARC-MASS":"R052",
 "NFI-CHECK037-STEADY-FLIGHT-LOAD":"R089","NFI-CHECK037-RESTORATION":"R078",
 "NFI-CHECK037-CORE-CTE-LAG":"R098","NFI-CHECK037-FILM-CONSTITUTIVE":"R065",
 "NFI-CHECK037-CURRENT-GEOMETRY":"R082","NFI-043-CHECK-02":"R060",
 "CHECK041-NFI-02":"R065","CHECK041-NFI-07":"R060","CHECK041-NFI-12":"R067",
 "NFI-048-C01":"R089","NFI-048-C02":"R082","NFI-048-C03":"R045",
 "NFI-048-C04":"R099","NFI-048-C12":"R094","NFI-048-C13":"R094",
 "051-01-admission":"R094","051-05-cvd-manufacture":"R061",
 "051-08-cfrp-allowable":"R060","051-09-orthotropy":"R053",
 "051-10-frame-instability":"R091","051-11-hail-transfer":"R102",
 "051-12-cascade":"R102","051-14-nonbrittle-ranking":"R102","051-15-common-source-drift":"R079",
 "NFI-CHECK045-PERRY":"R058","NFI-CHECK045-STRIKES":"R104",
 "NFI-CHECK045-SEARCH":"R082","NFI-CHECK045-FEASIBILITY":"R079",
 "NFI-CHECK045-LEAK-EVENT":"R045","NFI-CHECK045-NDI":"R097",
 "NFI-CHECK045-FRAME":"R102","NFI-CHECK045-FILM":"R102",
 "NFI-CHECK045-TRAJECTORY":"R090","NFI-CHECK045-VENT":"R090",
 "NFI052-01":"R104","NFI052-02":"R091","NFI052-03":"R063",
 "NFI052-04":"R068","NFI052-05":"R103","NFI052-06":"R044",
 "NFI052-07":"R100","NFI052-08":"R044","NFI052-09":"R086",
 "NFI052-10":"R102","NFI052-11":"R082","NFI052-12":"R042",
 "NFI052-13":"R041","NFI052-14":"R083","NFI052-15":"R104",
 "NFI50-01":"R083","NFI50-02":"R039","NFI50-03":"R082","NFI50-04":"R089",
 "NFI50-05":"R098","NFI50-06":"R100","NFI50-07":"R100","NFI50-08":"R044",
 "NFI50-09":"R045","NFI50-10":"R086","NFI50-11":"R079","NFI50-12":"R079",
 "NFI50-13":"R039",
}
for n in new:
    f=n["fields"]
    text=" ".join(str(f.get(k,"")) for k in ("id","topic","title","finding","claim","open_issue","issue")).lower()
    rid=defaults[reverse[n["report"]]];reason="source-specific default"
    for dest,words in rules:
        match=next((w for w in words if w in text),None)
        if match:
            rid=dest;reason=f"semantic topic: {match}";break
    if n["row_id"] in overrides:
        rid=overrides[n["row_id"]];reason="reviewed source-finding override, stable across inherited copies"
    assignments[n["uid"]]=rid;reasons[n["uid"]]=reason
    byrid[rid]["updates_030d"].append(copy.deepcopy(n))
save(B/"ROUTING.json",dict(
    method="One primary topic per complete attributed finding; source-specific defaults and reviewed semantic rules. Historical duplicate findings remain attributed.",
    assignments=assignments,reasons=reasons,reviewed_overrides=overrides))

notes={
 "R007":"CHECK-040 verifies scalar gamma arithmetic conditional on temperature inputs. CHECK-029/047 status is in PENDING. New light finishes do not qualify a physical global knockdown.",
 "R025":"200°F/30.3414:1 is a modelled repair, not a process qualification. CHECK-044's 60:1 scenario requires a geometry-specific joining and pad account; no fixed .120151kg surcharge transfers to a new hull.",
 "R027":"CHECK-040/042/044: detailed 200°F and .060 fatigue evidence concerns AF163-2K metal joints, not 2U .015 Be/honeycomb. Film-weight arithmetic does not establish bond strength or life.",
 "R034":"048 charges 10g/m² structural primer separately from the optical finish and joining floor; actual product, process and environmental uptake remain unqualified.",
 "R037":"CHECK-042: two-skin seams are5683.037m at30:1 and5685.225m at30.34:1; at least1190 panels per skin in the coverage approximation. No completed spherical layout is established.",
 "R040":"048 recovers conditional R10 ISA float with a lighter finish: original endpoint+124.262kg, cure-included+118.695kg. Least G+Q+film usage.842794 is near zero payload. R12/15 ISA use G+Q only. R30 remains a different original040 account; new-finish global size ranking is uncomputed.",
 "R041":"Exterior .1mm is the optimistic retained-water assumption, not material uptake. One millimetre removes all original040 primary floats and all432 new048 R10–15 heavy-water cases. Neither scenario is a measured finish/process upper limit.",
 "R047":"044/CHECK044: pad coreSF.714286, plate-only index949.846days and conditional thermal index18816days do not give hull life. Strict-pad/scarf cost+36.661200kg needs3.414034kg old-plate credit; otherwise+40.075234kg. Reprice on048/041 geometries.",
 "R048":"Original040 R30 ISA named endpoint has102.231t Be faces:23.61% of020's revised2024 world mine-output433t, or23.77% of2025estimate430t. These are Be-content totals, not finished-sheet capacity. Least-usage point has103.146t instead. Be-free049 status is explicit.",
 "R050":"045's narrow dents can preserve transferred global gamma yet trigger local crushed-core growth. Do not equate a gamma-only pass with damage tolerance; current coated construction needs matched impact testing.",
 "R055":"CHECK-041 corroborates fixed f5 screens1.143285/1.083205, local sensitivities1.033223/.978132 and independentm24 nonlinear bracket. Nine displayed cells differ; film direction and midpoint reproduction remain qualified. Prior owner postprocessor exposure was disclosed.",
 "R060":"043fold/CHECK043: source3.9GPa is not a calibrated member or1cm³ scale. At own-screen demands the two population hypotheses give Pf.002524/.002143 versus.991133/.979046. Pf10⁻⁶ needs8.53751/8.39866GPa under the complete-member m10 hypothesis.",
 "R065":"046/CHECK046: protectedPBO remains a development candidate. No installed one-year or ten-year film life is demonstrated; chemistry-onlySK99 mass ranking omits unacceptable/unqualified creep at the stated stress.",
 "R068":"041 required nominal retention is.874673/.923186. Warehouse ten-year filmSF.985018/.933256; hot/full-restraint targetSF.995706/.944784. These reduce the intact least screens. The019 local-shell sensitivity.978132 is not repaired by film sizing.",
 "R070":"CHECK-042 separates the .254mm S-II core-face matching gap from spherical shape error. Historical test gamma and current tolerance-map transfer do not establish Be-sandwich knockdown.",
 "R086":"044 six-pad life spectrum differs from040/048 resized one-pad account. Plate removal credit must be documented. A scalar pad/crush calculation is not the installed load path or life.",
 "R089":"CHECK-040's independent temperatures differ; 048fold supplies exact existing boundary equations without declaring independent or physical thermal closure. Wet finish optics, whole mission weather and constraints remain open.",
 "R093":"Keep firstT1 finished-sheet compression/specification,T2 weighed curved sealed scarf includingF1 extension,T3 same-batch wrinkling. Add finish/retention, damage, film-ageing and full-member proof evidence to the existing routes; no purchases authorized.",
 "R094":"Current filing snapshot and pending jobs govern. Every new canonical report is given an explicit change disposition and every NFI collection retains original fields and source pointers. Running seats provide no evidence.",
 "R097":"CHECK-042 critical disbond is27.127598mm simply supported/54.779991mm clamped. Full-cohort tapa90/95 is41.8/29mm; neither establishes Be inspection. Build and seam processes remain unqualified.",
 "R098":"048fold explicitly includes cure compression in alternate global/crimp demand without doubling local cure. R10MLCCAg ISA bake remains+118.695kg, but two marginal original048 configurations lose every allowed float. Actual residual field and eigenmode effect remain open.",
 "R099":"048 light finish mass7.5752g/m²×1.10 and alpha.09/epsilon.80 are recipe/class transfers, not matched installed Be coating. 10g/m² structural primer is separate. Classical CCAg and Ag/FEP alternatives remain in the full source matrix.",
 "R100":"Dry gas retains the added inventory; bake uses an assumed90% material-water removal; onboard sorbent retains captured water and adds bed/cartridge mass. None reduces future exterior-service retention. Measured before/after exterior fields are unknown.",
 "R101":"045 uses028b's14.581kg margin. Design hail gives80.865mm crushed zone with growth in two of three clamped readings and all simply supported readings. Conditional vent to.458904pressure admits2645.660kg air; no damage-tolerant048 float or qualified operating route follows.",
 "R102":"045 old022d/member-loss surrogates give filmSF.838835 and stress amplification2.427–3.271; tube hail probabilities use transferred specimens. Linear overload is adverse evidence, not a dynamically solved cascade probability on041.",
 "R103":"046/CHECK046 at041:95.751kg OD4/white package plus equipment and hot-film correction exceeds the100kg allocation by31.465–51.465/39.916–59.916kg. Annual replacement resets onlyfilm; source ageing laws and.5% annual-loss requirement are not established life.",
 "R104":"CHECK-043 corrects the brief: proof force1.25× gives memberEuler ratio.375 and peakstress1.259379×; it does not establish Euler buckling. Fixture, local/assembly stability, stress coverage and proof damage remain open. Rise8 total5446.291kg includes5039.558kg tubes.",
}
notes["R099"]+=" PartialCHECK048 corrects classicalCCAg's cited source toalpha.08/normal epsilon.72 onKapton; the modeled.09/.65 pair remains an unqualified projection and is not automatically rerun here."
notes["R089"]+=" PartialCHECK048 independently differs in297/325thermal comparisons; this does not identify an owner error or close boundary equivalence."
notes["R082"]="PartialCHECK048 evaluates stored points but does not complete independent least-set, geometry orE-axis bound searches. Original source minima remain conditional reported results, not independently verified optima."
notes["R104"]+=" Partial051 completes288 target rows: atq1 the hypothetical member3.9GPa/m10 model meetsPf1e-3; at own screens it needs4.278678/4.209090GPa. Candidate construction comparison remains unfinished."
notes["R102"]+=" Partial051 separates045f5stress factors2.427/2.480 fromf4's3.27; no resized041hail or dynamic cascade result is filed."
notes["R101"]+=" CHECK045 corrects55mm growth threshold to19.176311mm within the23.237218mm core. Pach peak model1.489–1.541mm does not agree with measured residual1.1–1.2mm; the stored test unit must be.0011m."
notes["R102"]+=" CHECK045 checks every edge class: stress ratio1.959485–3.270739 and tension0–1019.372MPa. Improved wall1.5/2mm witnessesSF.805476/.483053 and tearSF.975445 at848.604kg remain below1; every-loss cascade and every-puncture opening are unproved."
notes["R058"]="CHECK045 corrects the historical045 non-governing PerrySF to3.454499160 from4.095817936; nominal022dSF1.258252477 is unchanged."
notes["R090"]="CHECK045 corrects trajectory ground contact to10m sphere-centre height, distinguishes gross-neutral reference from built inventory, and requires an explicit valve/control/support objective. Sea-level vent air for the same absolute differential is2912.791kg; no safe operating protocol or current regulatory route is established."
notes["R040"]+=" 052 adds a resized P3 f5-019 account: first tested ground-service closure R10ISA/R12optimistic, endpoints+30.863/+46.259kg. This new strength/section/account scenario does not repair the original041 witness by implication."
notes["R041"]+=" 052 also assumes.1kg/m² external water; an extra.9kg/m² costs1130.973kg atR10. Its explicit gas/water/weather/contamination replace the old bulk reserve."
notes["R044"]="052 charges100kg systems plus50kg ground hardware. The R10ISA least point reaches the chosen humidity limit in17.280h and plans15.552h service, despite450.241h total-pressure headroom. Coldh2 reduces humidity time to11.475h. No tested24h onboard-dry case closes throughR30; this is a selected hardware scenario, not a universal pumping impossibility."
notes["R068"]+=" 052's new R10ISA least root requires5.343008GPa effective ply strength,92.12% of5.8GPa raw yarn; the inherited60% efficiency cannot closeR10. This is an additional unqualified axis. The resized peak-local screen is enforced at1."
notes["R083"]="052's source P2 comparison used original048 without the cure-demand alternative. The register adds a clearly labelled cure-included all-four point minus50kg extra service, with no reoptimization or equivalence of qualification. R10ISA is+77.253kg andR12optimistic floor+28.576kg."
notes["R086"]+=" 052 carries33.138kg of P2-derived mooring allowance atR10; it does not establish the P3 hardpoint load path."
notes["R102"]+=" 052 does not price or qualify a damage-tolerance repair; its intact mass closure does not retire045/CHECK045."
notes["R103"]+=" 052 includes the95.751kg protection package explicitly and resizesfilm/structure. Its mass closure does not validate the retained-strength law or erase the earlier fixed041 deficits."
notes["R104"]+=" At the different052R10ISA resized root, m10/3.9GPa yields hypothetical member-Pf.000947798 or1cm³-coupon-Pf.824296. Neither is a measured whole-hull or lifetime probability."
notes["R039"]="050 is filed:2,027,245 weather points overR10/12/15/20/30, all16subsets. None closes the declared MIL10% hot profile. At100m across RH0–100% and sea-pressure±30hPa, family R10/R30 upper offsets+5.8/+15.8K become−6.5/+3.3K for fixed full-range builds; cold interface limit about−10.5K. Joint weather distributions and annual availability remain unknown."
notes["R040"]+=" 050 now supplies an original048-account weather/size extension throughR30; the corrected cure-included account remains limited toR10–15. Do not transfer050's original+124.262kg basis to the+118.695kg corrected headline."
notes["R082"]+=" 050 distinguishes weather-dependent design families from immutable103.953kPa full-range builds; their masses stay aboard in favorable weather. Its16subset surfaces retain ties rather than claim a unique full-grid winner."
notes["R100"]+=" 050's projected12h clear saturated R10 deposits.243108kg/m² and leaves−82.280kg dry-start payload; the clear reference deposits.090198kg/m² and leaves+117.381kg. Added preexisting film is arithmetic, not a wet-start transient. No drainage or switched-optics performance is measured."
notes["R089"]+=" 050 extends the dry thermal field with shifted air/sky and gives a cold-interface boundary; this is not independent validation of the inherited model, the new cure alternative or wet weather."
notes["R048"]+=" 050's new fixed full-range hull is a different geometry/account from the historical040 supply example; its existence does not change which point the102.231t headline describes."
for rid,text in notes.items():byrid[rid]["current_030d"]=dict(tag=TAG,text=text)
own_specs=[
 ("R040","030D-ACCOUNT-TRANSFER","The cure-included light-finish R10–15 rows, old040 R30 account and050 original048-account weather extension are different accounts; no common cure-inclusive R10–30 optimum is claimed."),
 ("R041","030D-RETENTION-MEASUREMENT","Neither .1mm nor1mm is a measured finish/process bound; no dry-out route earns an in-service exterior-liquid credit."),
 ("R047","030D-LIFE-MASS-TRANSFER","Damage/life surcharges must be reclosed on the selected hull, with explicit old-hardware credits and no independent double counting of systems."),
 ("R048","030D-BE-SUPPLY","R30 endpoint and least-usage face masses differ; historical world mine output is not finished-sheet availability."),
 ("R089","030D-THERMAL-INDEPENDENCE","Written boundary clarification and internal numerical convergence do not close CHECK-040's independent thermal mismatch."),
 ("R101","030D-DAMAGE-TRANSFER","Narrow-dent gamma survival does not establish local damage tolerance or transfer 028b impact thresholds to the coated048 design."),
 ("R103","030D-FILM-LIFE","A film-only restoration toSF1 neither re-closes equipment/protection mass nor fixes the019 local shell sensitivity or qualifies an annual renewal interval."),
 ("R104","030D-PROOF-CORRECTION","The combined-screen exceedance does not establish member Euler buckling; proof fixtures, stress coverage and life remain unqualified."),
 ("R094","030D-CUTOFF","The register is a filing snapshot of canonical reports; pending work contributes no guessed numerical result."),
]
authored=dict(schema=1,unit=UNIT,tag=TAG,rows=[
    dict(id=id,finding=text,tag=TAG,status="OPEN",blocks_progress=False) for _,id,text in own_specs])
save(B/"AUTHORED-NFI.json",authored)
ap=pin(B/"AUTHORED-NFI.json");own=[]
for i,((rid,id,_),fields) in enumerate(zip(own_specs,authored["rows"])):
    n=dict(uid=f"DS{i+1:03d}",report=REPORT,card="MAINLINE-030d",
        file=str(B/"AUTHORED-NFI.json"),snapshot=str(B/"AUTHORED-NFI.json"),
        row_id=id,fields=fields,source_sha256=ap["sha256"],
        source_json_pointer=f"/rows/{i}",register_classification=TAG)
    own.append(n);byrid[rid]["updates_030d"].append(copy.deepcopy(n))
nfi=copy.deepcopy(load(BASE/"NFI.json"))
nfi.update(schema=4,unit=UNIT,tag=TAG,
    auxiliary_source_documents="NEW-NFI-SOURCES.json",
    note="Prior961 findings and all source fields are preserved. Attributed duplicates are not independent physical gaps. Current030d annotations and corrected source values govern.")
nfi["rows"]+=new+own
coverage=dict(baseline_register_rows_preserved=98,baseline_findings_preserved=961,
    new_register_rows=len(topics),new_source_findings=len(new),new_authored_findings=len(own),
    total_register_rows=len(register["rows"]),total_attributed_findings=len(nfi["rows"]),
    new_canonical_reports=len(reports),new_report_artifact_pins=sum(len(r["artifacts"]) for r in reports.values()))
register["previous_030c_coverage"]=copy.deepcopy(register["coverage"])
register.update(schema=4,tag=TAG,coverage=coverage)
save(B/"REGISTER.json",register);save(B/"NFI.json",nfi);save(B/"REGISTER-COVERAGE.json",coverage)

ledger=copy.deepcopy(load(BASE/"LEDGER.json"))
for c in changes:
    ledger["rows"].append(dict(correction=c["title"],by=c["report"],effect_on_lead=c["text"],
        lead_relevant=True,register_version="030d",tag=TAG,ids_in_store=[]))
ledger["rows"].append(dict(correction="R30 beryllium supply scale",by=ALIASES["020"],
    effect_on_lead=f"{be/1000:.6f}t faces at original040 named endpoint; {100*be/433000:.6f}% of revised2024 output433t; distinct from103.146t least-usage point.",
    lead_relevant=True,register_version="030d",tag=TAG,ids_in_store=[]))
ledger.update(schema=4,previous_030c_rows=len(load(BASE/"LEDGER.json")["rows"]))
save(B/"LEDGER.json",ledger)
optimism=copy.deepcopy(load(BASE/"OPTIMISM-LEDGER.json"))
optimism["previous_030c_rows"]=len(optimism["rows"])
for p in selected:
    if p["least"] is None:continue
    point=p["least"]
    optimism["rows"].append(dict(lead="P2",id=p["id"],name="048 cure-included least set",
        factor=dict(gamma_over_point2=point["properties"]["gamma"]/.2,Q_over_point33=point["properties"]["Q"]/.33,
                    film_mass_reduction=.1464728290914915/point["properties"]["film_kg_m2_interface"]),
        tag=TAG,evidence_category="conditional source model",evidence_state="Unqualified",
        source=p["source"],mask=point["mask"],usage=point["usage"],
        dependencies=p["dependencies"],grounding_route="T1/T2/T3 plus finish, retention, residual and installed-account evidence"))
optimism["rows"]+= [
 dict(lead="P2",id="048-finish",name="MLCCAg optical/areal-mass transfer",factor=None,tag=TAG,
      evidence_category="recipe and class transfer",evidence_state="Unqualified",grounding_route="Matched coated Be mass/optics/adhesion/wet-weather test"),
 dict(lead="P2",id="048-water",name="Optimistic exterior retention",factor=10,tag=TAG,
      evidence_category=".1 versus1mm planning scenarios",evidence_state="Unmeasured",grounding_route="Measure retention and drainage, independently of material dry-out"),
 dict(lead="P3",id="043-reference-scale",name="Finished-member failure distribution",factor=None,tag=TAG,
      evidence_category="alternative calibration hypotheses",evidence_state="Unqualified",grounding_route="Matched finished-member compression, size/scatter, proof fixture and lifetime evidence"),
 dict(lead="P3",id="046-ageing",name="Ten-year retained strength",factor=None,tag=TAG,
      evidence_category="alternative laws and acceptance target",evidence_state="Unqualified",grounding_route="Protected loaded laminate, edges, high-R cycling, creep and measured combined loss")]
for row in rows52:
    if row["service"]!="ground" or row["least"] is None:continue
    point=row["least"]
    optimism["rows"].append(dict(lead="P3",id=f"052-R{row['R_m']}-{row['weather']}-ground",
        name="052 resized ground-service least set",tag=TAG,source=row["source"],
        mask=point["mask"],usage=point["usage"],axes=point["axes"],
        factor=dict(assumed_member_compression_over_1GPa=point["assumed_SiC_strength_Pa"]/1e9,
            effective_ply_strength_over_3p48GPa=point["film_effective_strength_Pa"]/3.48e9,
            retention_over_baseline=point["ten_year_retention"]/.8615688736605606),
        required_member_compression_Pa=point["required_SiC_strength_Pa"],
        evidence_category="conditional resized source family",evidence_state="Unqualified",
        dependencies=account52["dependencies"],
        grounding_route="Finished-member and crossply distributions, loaded joints, life, whole-hull humidity/service, installed inventory and damage tests"))
save(B/"OPTIMISM-LEDGER.json",optimism)
ground=copy.deepcopy(load(BASE/"GROUND-FIRST.json"))
ground["first_three_030d"]=["T1","T2","T3"]
ground["extensions_030d"]=[
 dict(id="D-G1",route="Matched finish and retained-water demonstration",ties=["T2","T3"],
      target="Weigh coating/primer and material uptake separately; measure optics, adhesion and rain/dew/frost retention before/after actual conditioning."),
 dict(id="D-G2",route="Loaded damaged curved sandwich and member/bay tests",ties=["T2","T7"],
      target="Impact/crushed-core growth and detection on selected048geometry;041member loss, film tears, joint restraint and safe loading."),
 dict(id="D-G3",route="Protected film life and renewal interface",ties=["G6","G7","G9"],
      target="Measure combined loss, thermal restraint, creep, high-R fatigue, seam/edge protection and installed package mass."),
 dict(id="D-G4",route="Finished-member statistics and proof coverage",ties=["G2","G9"],
      target="Calibrate compression population/reference size and joint/common-cause risk; qualify fixtures and damage-sensitive proof coverage."),
 dict(id="D-G5",route="052 complete dry-service and crossply demonstration",ties=["G6","G7","G9"],
      target="Measure installed PBO ply efficiency, loaded wet barrier/humidity and cold-point service interval; replace100+50kg equipment allowances and verify the P3 hardpoint and damaged state.")]
save(B/"GROUND-FIRST.json",ground)
checks=copy.deepcopy(load(BASE/"CHECK-VERDICTS.json"))
for a in change_text:
    if not a.startswith("CHECK"):continue
    r=reports[ALIASES[a]]
    names={Path(x["path"]).name for x in r["artifacts"]}
    name="CHECK.md" if "CHECK.md" in names else "CARD.md"
    checks.append(dict(check_id=r["id"],at=r["at"],register_version="030d",
        verdict=r["body"],source=ref(a,name),qualified_installed_hull_SF=None,tag=TAG))
save(B/"CHECK-VERDICTS.json",checks)

# Pending means no filed canonical report, never an observation of a live seat.
pending_specs=[
 ("029 check",("check029","mainline029-independent","mainline029-check")),
 ("041 check",("check041",)),("042 check",("mainline042-independent-check",)),
 ("043 check",("mainline043-independent-check",)),("044 check",("mainline044-independent-check",)),
 ("045 check",("mainline045-independent-check","check045")),
 ("046 check",("check046",)),("047 dimple tolerance",("mainline047-",)),
 ("047 check",("check047","mainline047-independent-check")),
 ("048 check",("check048","mainline048-independent-check")),
 ("049 Be-free P2",("mainline049-",)),("049 check",("check049","mainline049-independent-check")),
 ("050 flyable weather",("mainline050-",)),("051 P3 frame targets",("mainline051-",)),
 ("052 P3 common account",("mainline052-",)),
]
pending=[]
partial_ids={ALIASES["CHECK048partial"],ALIASES["051partial"]}
for name,patterns in pending_specs:
    ids=[id for id in allreports if any(p in id for p in patterns)
         and id!=ALIASES["050exception"] and id not in partial_ids]
    partial=[id for id in partial_ids if any(p in id for p in patterns)]
    pending.append(dict(item=name,status="FILED" if ids else "PENDING",reports=ids,
        partial_reports=partial,
        snapshot_at=intake["sampled_at"],meaning="Canonical report availability only; not live seat status."))
save(B/"PENDING.json",pending)
index=copy.deepcopy(baseindex)
index.update(additions_030d=intake["reports"],baseline_030c_report=pin(BASE/"report.json"),
             snapshot_at_030d=intake["sampled_at"],
             supplemental_orders_030d=load(B/"SUPPLEMENTAL-ORDERS.json"),
             source_drift_030d=load(B/"SOURCE-DRIFT.json"))
save(B/"SOURCE-INDEX.json",index)
results=copy.deepcopy(base_results)
results["previous_030c_metadata"]={k:base_results.get(k) for k in ("schema","card","unit","snapshot_at","coverage","pending")}
results.update(schema=4,card="MAINLINE-030d",unit=UNIT,tag=TAG,snapshot_at=intake["sampled_at"],
    source_aliases_030d=ALIASES,coverage=coverage,pending=pending,next="Stop and file; robotics seat sends next job.",
    P2_current_hull_account="048 light-finish R10–15 account including separate primer/material/exterior water and explicit cure-demand alternative; original040 R30 retained separately.",
    P2_048_account=load(B/"P2-048-ACCOUNT.json"),P2_beryllium_supply=supply,
    P3_052_common_account=account52,
    P2_050_weather=weather50,
    P3_043_checked_reliability=reliability,damage_and_life_030d=load(B/"DAMAGE-AND-LIFE.json"),
    check041=source("CHECK041","RESULTS.json"),changes_030d=changes,
    partial_filings_030d=load(B/"PARTIAL-FILINGS.json"),
    overall_installed_hull_SF=None,qualified_hull_life=None,qualified_failure_probability=None)
save(B/"RESULTS.json",results)
save(B/"INPUTS.json",dict(schema=1,unit=UNIT,tag=TAG,
    brief_pins=load(B/"BRIEF-PINS.json"),baseline_pins_file=pin(B/"BASELINE-PINS.json"),
    intake=pin(B/"INTAKE.json"),source_index=pin(B/"SOURCE-INDEX.json"),
    code_ancestry="030c intake/normalize/build/render/validation code and every manifest file preserved under baseline030c. Additive source-identity, topic routing and ledger workflow extended.",
    source_scope="Filed canonical reports and their pinned artifacts; no new literature, supplier claim or current price assertion.",
    arithmetic_scope="Selected-point ledger sums, minima, ratios, same-allocation extra50kg service debit, 433t/430t supply comparisons and Weibull hazard inversion only. No upstream numerical model is imported or executed.",
    overall_installed_hull_SF=None))
print("BUILT",coverage)
