#!/usr/bin/env python3
"""Check preservation, attribution, current arithmetic and filing coverage."""
import hashlib
import csv
import json
import math
import re
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from intake import B,load,save,pin

BASE=B/"baseline030c"
checks=[];failures=[]
def check(name,good,detail=None):
    row=dict(check=name,passed=bool(good))
    if detail is not None:row["detail"]=detail
    checks.append(row)
    if not good:failures.append(row)
def near(name,a,b,tol=1e-7):
    check(name,abs(a-b)<=tol,dict(actual=a,expected=b,difference=a-b,tolerance=tol))
def ptr(obj,pointer):
    if pointer in ("","/"):return obj
    for token in pointer.lstrip("/").split("/"):
        [credential]
        obj=obj[int(token)] if isinstance(obj,list) else obj[token]
    return obj
def verify(a,p=None,label="pin"):
    path=Path(p or a["path"]);actual=pin(path)
    check(label,actual["sha256"]==a["sha256"] and actual["bytes"]==a["bytes"],str(path))

baseline=load(B/"BASELINE-PINS.json")
for a in baseline["pins"]:
    verify(a,label="original030c and inherited files unchanged")
    if a.get("snapshot"):verify(a,a["snapshot"],"030c immutable snapshot")
drift_history=load(B/"SOURCE-DRIFT.json")
for d in drift_history:
    verify(dict(path=d["observed_snapshot"],sha256=d["observed_sha256"],bytes=d["observed_bytes"]),
           label="every observed brief revision retained")
drifts={d["file"]:d for d in drift_history}
for a in load(B/"BRIEF-PINS.json"):
    if a["path"] in drifts:
        d=drifts[a["path"]]
        current=dict(path=a["path"],sha256=d["observed_sha256"],bytes=d["observed_bytes"])
        verify(current,label="documented current brief revision")
        verify(current,d["observed_snapshot"],"current brief revision snapshot")
        check("pinned brief drift documented",d["pinned_sha256"]==a["sha256"] and d["pinned_bytes"]==a["bytes"])
    else:verify(a,label="brief original")
    verify(a,a["snapshot"],"brief snapshot")
for a in load(B/"SUPPLEMENTAL-ORDERS.json"):
    verify(a,label="supplemental order");verify(a,a["snapshot"],"supplemental order snapshot")
intake=load(B/"INTAKE.json")
for r in intake["reports"]:
    a=dict(path=r["report_path"],sha256=r["report_sha256"],bytes=r["report_bytes"])
    verify(a,label="canonical report");verify(a,r["report_snapshot"],"canonical report snapshot")
    for a in r["artifacts"]:
        verify(a,label="new source artifact")
        if a.get("snapshot"):verify(a,a["snapshot"],"new source snapshot")

oldreg=load(BASE/"REGISTER.json");reg=load(B/"REGISTER.json")
check("all98 prior issue rows remain",len(oldreg["rows"])==98 and len(reg["rows"])>=98)
for old,new in zip(oldreg["rows"],reg["rows"]):
    for k,v in old.items():check("old register field preserved",new.get(k)==v,[old["rid"],k])
oldnfi=load(BASE/"NFI.json");nfi=load(B/"NFI.json")
check("all961 prior findings remain exactly",len(oldnfi["rows"])==961 and nfi["rows"][:961]==oldnfi["rows"])
for name in ("LEDGER","OPTIMISM-LEDGER"):
    old=load(BASE/(name+".json"));new=load(B/(name+".json"))
    check(name+" entries preserved",new["rows"][:len(old["rows"])]==old["rows"])
ground=load(B/"GROUND-FIRST.json");oldground=load(BASE/"GROUND-FIRST.json")
for k,v in oldground.items():check("ground-first field preserved",ground.get(k)==v,k)
check("first three tests preserved",ground["first_three_030d"]==["T1","T2","T3"])
for k,v in load(BASE/"SOURCE-INDEX.json").items():
    check("prior source-index field preserved",load(B/"SOURCE-INDEX.json").get(k)==v,k)

newnfi=load(B/"NEW-NFI.json")
docs=load(B/"NEW-NFI-SOURCES.json")
docix={(d["report"],d["file"]):d for d in docs}
routing=load(B/"ROUTING.json")["assignments"]
check("every new finding routed",set(routing)=={n["uid"] for n in newnfi})
identities=set()
byrid={r["rid"]:r for r in reg["rows"]}
counts=Counter(n["uid"] for r in reg["rows"] for n in r["updates_030d"])
for n in newnfi:
    identity=(n["report"],n["file"],n["source_json_pointer"])
    check("unique attributed finding identity",identity not in identities,identity)
    identities.add(identity)
    d=docix[n["report"],n["file"]]
    check("source finding fields preserved",ptr(d["document"],n["source_json_pointer"])==n["fields"],n["uid"])
    check("finding document matches snapshot",load(Path(d["snapshot"]))==d["document"],n["uid"])
    check("finding assigned exactly once",counts[n["uid"]]==1,n["uid"])
    check("finding stored under assigned topic",n in byrid[routing[n["uid"]]]["updates_030d"],n["uid"])
    check("finding retained in global NFI",n in nfi["rows"][961:],n["uid"])
check("source and authored total",len(nfi["rows"])==961+len(newnfi)+len(load(B/"AUTHORED-NFI.json")["rows"]))
coverage=load(B/"REGISTER-COVERAGE.json")
check("coverage agrees",coverage["total_register_rows"]==len(reg["rows"])
      and coverage["total_attributed_findings"]==len(nfi["rows"])
      and coverage["new_canonical_reports"]==len(intake["reports"]))
changes=load(B/"CHANGES.json")
check("every new report explicitly dispositioned",{c["report"] for c in changes}=={r["id"] for r in intake["reports"]})
check("040037b fold explicitly carried","rpt-ref-378f34abc5a6eea5b053" in {c["report"] for c in changes})
check("no report pin failures",intake["pin_failures"]==0)

account=load(B/"P2-048-ACCOUNT.json")
check("all18 radius/weather/joining rows retained",len(account["rows"])==18 and
      {(x["R_m"],x["weather"],x["floor"]) for x in account["rows"]}==
      {(r,w,f) for r in (10,12,15) for w in ("ISA","optimistic","both") for f in (False,True)})
cache={}
for row in account["rows"]:
    source=row["source"]
    if source["file"] not in cache:cache[source["file"]]=load(Path(source["file"]))
    original=ptr(cache[source["file"]],source["selector"])
    check("selected endpoint exact source copy",row["cure_included_endpoint"]==original["two_factor_endpoint"],row["id"])
    check("selected least exact source copy",row["least"]==original["least"]["least"],row["id"])
    for key in ("cure_included_endpoint","all_four_endpoint","least"):
        p=row[key]
        if p is None:continue
        a=4*math.pi*p["R_m"]**2;b=p["bill_kg"]
        near("whole bill closes",sum(b.values())+p["signed_payload_kg"],p["lift_kg"],1e-6)
        near("exterior water separate",b["water"],.1*a,1e-6)
        near("structural primer separate",b["structural_primer"],.01*a,1e-6)
        near("finish separate",b["coating"],.0075752*1.1*a,1e-6)
        check("cure alternative remains active",p["settings"]["cure_in_global"] is True)
        check("conditional structural screens",min(p["modes"].values())>=1-1e-6)
        check("unknown installedSF retained",p["overall_installed_hull_SF"] is None)
        check("full dependencies retained",len(row["dependencies"])==10)
near("R10 primary endpoint",account["primary"]["cure_included_endpoint"]["signed_payload_kg"],118.69482555678769)
check("R10 least mask",account["primary"]["least"]["mask"]==11)
check("heavy-water result negative",account["water_one_mm"]["configurations"]==432
      and account["water_one_mm"]["best_all_four"]["payload_kg"]<0
      and account["water_one_mm"]["favorable_upper"]["payload_upper_kg"]<0)
check("two marginal floats lost",len(account["lost_floats"])==2)
p3=load(B/"P3-052-ACCOUNT.json")
check("052 all45 scenarios preserved",len(p3["rows"])==45 and
      {(x["R_m"],x["weather"],x["service"]) for x in p3["rows"]}==
      {(r,w,s) for r in (10,12,15,20,30) for w in ("ISA","optimistic","both")
       for s in ("ground","onboard_pressure","onboard_dry")})
for row in p3["rows"]:
    s=row["source"]
    if s["file"] not in cache:cache[s["file"]]=load(Path(s["file"]))
    original=ptr(cache[s["file"]],s["selector"])
    for key in ("baseline","all_axes_endpoint","least","least_axis_count"):
        check("052 exact source point",row[key]==original[key],[row["R_m"],row["weather"],row["service"],key])
    for key in ("baseline","all_axes_endpoint","least"):
        point=row[key]
        if point is None:continue
        bill=point["bill_kg"]
        near("052 whole bill closes",sum(bill.values())+point["payload_kg"],point["lift_kg"],1e-6)
        near("052 systems distinct",bill["systems"],100)
        near("052 service matches separate charge",bill["vacuum_service"],point["vacuum"]["service_mass_kg"])
        check("052 local peak enforced",point["local_peak_enforced"] and point["local_peak_SF"]>=1-1e-6)
        check("052 installedSF andPf remain unknown",point["qualified_SF"] is None and point["actual_frame_Pf"] is None)
    if row["weather"]=="both" or row["service"]=="onboard_dry":
        check("052 combined weather and dry packages do not close",row["least"] is None and row["all_axes_endpoint"]["payload_kg"]<0)
root=p3["primary"]["least"]
check("052 least axis mask",root["mask"]==11)
near("052 least usage",root["usage"],.8393402109303141)
near("052 ply strength",root["film_effective_strength_Pa"],5343007948.312043,1e-3)
near("052 added service",root["bill_kg"]["vacuum_service"],50)
near("052 ground interval humidity basis",root["vacuum"]["planned_ground_service_interval_h"],
     .9*root["vacuum"]["first_cycle_humidity_limit_h"])
check("052 humidity governs before pressure",root["vacuum"]["first_cycle_humidity_limit_h"]<root["vacuum"]["total_pressure_limit_h"])
for row in p3["cure_included_P2_comparison"]:
    old=next(x for x in account["rows"] if (x["R_m"],x["weather"],x["floor"])==
             (row["R_m"],row["weather"],row["floor"]))
    near("052 P2 comparison uses cure corrected point",row["cure_included_all_four_payload_kg"],
         old["all_four_endpoint"]["signed_payload_kg"])
    near("052 P2 comparison same extra service",row["same_extra_vacuum50_payload_kg"],
         row["cure_included_all_four_payload_kg"]-50)
check("052 original comparison preserved",p3["original_P2_comparison"]==
      load(Path(p3["original_P2_comparison_source"]["file"])))
supply=load(B/"BERYLLIUM-SUPPLY.json")
near("R30 supply share433t",supply["share_2024"],supply["Be_faces_kg"]/433000)
near("R30 supply share430t",supply["share_2025"],supply["Be_faces_kg"]/430000)
check("R30 headline about23.6percent",abs(100*supply["share_2024"]-23.6)<.05)
check("R30 endpoint versus least preserved",supply["Be_faces_kg"]!=supply["least_usage_point_faces_kg"])

rel=load(B/"P3-RELIABILITY.json")
near("proof Euler ratio",rel["proof"]["original_proof_Euler_ratio"],.375,1e-10)
near("proof peak stress ratio",rel["proof"]["original_proof_peak_stress_ratio"],1.259378651,1e-8)
near("rise8 allowance",rel["rise8_total_kg"]-rel["rise8_tubes_kg"],406.732886937778,1e-7)
for row in rel["requirements"]:
    p=next(p for p in rel["probabilities"] if p["point"]=="041-f5-"+row["point"] and p["calibration"]=="whole_member")
    recovered=-math.expm1(-p["frame_hazard"]*(3.9e9/row["required_member_scale_for_Pf1e6_Pa"])**10)
    near("required member scale inverts to Pf1e-6",recovered,1e-6,1e-14)
check("reliability remains unqualified",rel["qualified_frame_failure_probability"] is None and rel["qualified_lifetime_failure_probability"] is None)
life=load(B/"DAMAGE-AND-LIFE.json")
check("044045046 rows cover both leads",len(life["rows"])==6 and
      {(x["card"].split(" /")[0],x["lead"]) for x in life["rows"]}=={(c,p) for c in ("044","045","046") for p in ("P2","P3")})
h=life["pad_life_044"]
near("old plate credit explicitly required",h["conditional_no_old_plate_credit_added_kg"]-h["relative_strict_pad_and_scarf_added_kg"],3.414033639,1e-8)
for row in life["film_life_rows"]:
    near("retention inverse initialSF",row["initial"]["minimum_nominal_retention"],1/row["initial"]["sf0"])
    for law in row["ten_year_laws"].values():
        near("film aging multiplies initialSF",law["film_SF"],law["retained_fraction"]*row["initial"]["sf0"])
    check("life scenarios unqualified",all(law["qualified_SF"] is None for law in row["ten_year_laws"].values()))
check("film losses reduce both041 screens",all(
    x["ten_year_laws"]["light_blocked_warehouse_endpoint_exponential"]["film_SF"]<1
    for x in life["film_life_rows"] if x["point"].startswith("041")))
check("life and global qualification null",life["qualified_hull_SF"] is None and life["qualified_lifetime"] is None)
c45=life["CHECK045"]
check("CHECK045 is complete with corrections",c45["results"]["status"]=="COMPLETE_WITH_CORRECTIONS")
near("CHECK045 non-governing Perry correction",c45["corrections"]["corrected_Perry_SF"],3.454499160200503,1e-10)
check("CHECK04555mm growth within core",c45["corrections"]["clamped_55mm_growth_depth_mm"]<c45["corrections"]["source_core_depth_mm"])
check("CHECK045 improved repairs remain below1",max(c45["corrections"]["improved_wall_SF"].values())<1 and c45["corrections"]["improved_tear_SF"]<1)
check("CHECK045 exact source findings preserved",load(Path(c45["exact_findings"]["file"]))==c45["findings"])
results=load(B/"RESULTS.json")
for k in ("overall_installed_hull_SF","qualified_hull_life","qualified_failure_probability"):
    check("global qualification remains unknown",results[k] is None,k)
pending=load(B/"PENDING.json")
check("050 completed report supersedes exception",next(x for x in pending if x["item"]=="050 flyable weather")["status"]=="FILED"
      and "rpt-1228-mainline050-simjob-refusal-retry-request-1020" not in
      next(x for x in pending if x["item"]=="050 flyable weather")["reports"])
weather50=load(B/"P2-WEATHER-050.json");w50=weather50["results"]
check("050 exact source result",w50==load(Path(weather50["source"]["file"])))
check("050 weather coverage",w50["requested_grid_points"]==2027245 and w50["subsets_computed"]==16
      and w50["radii_m"]==[10,12,15,20,30])
check("050 hot-day scoped failure",w50["ten_percent_hot_smallest_sampled_radius_m"] is None)
for point in w50["fixed_builds"]:
    near("050 fixed bill charged",sum(point["bill_kg"].values()),point["mass_kg"],1e-6)
    near("050 fixed pressure capacity",point["pressure_Pa"],103953.19780784745,1e-5)
    check("050 unknown installedSF retained",point["qualified_installed_hull_SF"] is None)
for row in w50["dew_account"]:
    near("050 preexisting water extra debit",row["fresh_dry_payload_after_night_kg"]-
         row["preexisting_0p1_plus_night_payload_kg"],.1*4*math.pi*row["R_m"]**2,1e-6)
check("CHECK045 no longer pending",next(x for x in pending if x["item"]=="045 check")["status"]=="FILED")
check("052 filed",next(x for x in pending if x["item"]=="052 P3 common account")["status"]=="FILED")
partial=load(B/"PARTIAL-FILINGS.json")
check("partial048 remains incomplete",not partial["CHECK048"]["scope"]["full_check_complete"]
      and not partial["CHECK048"]["independent_least_sets_verified"])
check("partial051 remains incomplete",not partial["MAINLINE051"]["work_complete"])
for item in ("048 check","051 P3 frame targets"):
    p=next(x for x in pending if x["item"]==item)
    check("partial report remains pending",p["status"]=="PENDING" and len(p["partial_reports"])==1,item)
with Path(partial["target_surface_source"]["file"]).open() as f:
    check("051 completed target surface288rows",len(list(csv.DictReader(f)))==288)
for p in partial["MAINLINE051"]["target_summary"]:
    if p["load"]=="own_screen":
        old=next(x for x in rel["probabilities"] if x["point"]=="041-f5-"+p["reserve"] and x["calibration"]=="whole_member")
        near("051 own-screen hypothesis matches043",p["hypothetical_whole_3p9_m10_Pf"],old["frame_Pf"],1e-12)
    else:
        check("051 operating hypothetical Pf below1e-3",p["hypothetical_whole_3p9_m10_Pf"]<.001)
check("048 partial raw differences remain attributed",partial["CHECK048"]["account"]["mismatch_count"]==16679
      and set(partial["CHECK048"]["account"]["mismatch_counts_by_field"])==
      {"vacuum.initial_gas_kg","vacuum.gas_aboard_counted_kg","vacuum.desorbed_24h_kg"})
optical=partial["CHECK048"]["classical_optical_correction"]
check("classical optical citation correction retained",optical["source_alpha"]==.08
      and optical["source_normal_emittance"]==.72 and optical["modeled_emittance"]==.65)

card=(B/"CARD.md").read_text()
for token in ("3.414034","40.075234","AF163-2K","27.127598","5685.225425",
              "1190","5039.557739","5446.290626",".375","8.53751","8.39866",
              "459.261468","118.695","102.231","23.6","1.033223","0.978132"):
    check("required corrected value rendered",token in card,token)
check("proof corrected explicitly","statement is corrected" in card and "does not establish individual Euler buckling" in card)
check("thermal independence remains open","does not close independent or physical thermal reproduction" in card)
check("one change per new report",all(c["title"] in card for c in changes))
for name in ("CARD.md","REPORTS.md"):
    for target in re.findall(r"\[[^\]]*\]\(([^)]*)\)",(B/name).read_text()):
        if target.startswith(("https://","http://","#")):continue
        path=(B/target.split("#")[0]).resolve()
        check("rendered local link exists",path.exists(),[name,target])
for p in B.glob("*.json"):
    if p.name in ("VALIDATION.json","MANIFEST.json"):continue
    try:
        json.loads(p.read_text(),parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
        check("current JSON strict finite",True,p.name)
    except ValueError as e:check("current JSON strict finite",False,[p.name,str(e)])
out=dict(passed=not failures,checks=len(checks),failed=len(failures),
         at=datetime.now(timezone.utc).isoformat(),coverage=coverage,
         summary=dict(Counter(x["check"] for x in checks)),failures=failures,records=checks)
save(B/"VALIDATION.json",out)
print(json.dumps({k:v for k,v in out.items() if k not in ("records","summary")},indent=2))
if failures:raise SystemExit(1)
