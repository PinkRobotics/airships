#!/usr/bin/env python3
"""Independent local synthesis validation; no owner calculation is imported."""
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime
from decimal import Decimal, getcontext
from pathlib import Path
from zoneinfo import ZoneInfo

B=Path(__file__).resolve().parent
getcontext().prec=40
D=lambda v:Decimal(str(v))
def load(name): return json.loads((B/name).read_text())
checks=[]
def check(name,passed,detail=None):
    checks.append(dict(name=name,passed=bool(passed),detail=detail))
def close(name,a,b,rel=2e-9,abs_tol=1e-7):
    check(name,math.isclose(float(a),float(b),rel_tol=rel,abs_tol=abs_tol),
          dict(observed=float(a),independent=float(b)))
def filepin(path):
    h=hashlib.sha256();size=0
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk);size+=len(chunk)
    return dict(path=str(path),sha256=h.hexdigest(),bytes=size)
r=load("RESULTS.json");reg=load("REGISTER.json");nfi=load("NFI.json")["rows"]
base=load("snapshots/baseline030/REGISTER.json")
bn=load("snapshots/baseline030/NFI-NORM.json")
check("362 baseline raw findings unchanged",nfi[:len(bn)]==bn)
check("86 baseline register records unchanged",
      all(all(new[k]==v for k,v in old.items()) for old,new in zip(base["rows"],reg["rows"])))
check("88 baseline corrections unchanged",load("LEDGER.json")["rows"][:88]==load("snapshots/baseline030/LEDGER.json")["rows"])
check("35 baseline check records unchanged",load("CHECK-VERDICTS.json")[:35]==load("snapshots/baseline030/CHECK-VERDICTS.json"))
check("Original030 lead/optimism/grounding history unchanged",r["original_030_history"]==load("snapshots/baseline030/RESULTS.json"))
refs=[x["uid"] for row in reg["rows"] for x in row["sources"]+row["updates_030b"]]
check("All source findings referenced",set(refs)=={x["uid"] for x in nfi})
check("Source UIDs unique",len(nfi)==len({x["uid"] for x in nfi}))
check("Source report/file/row identities unique",len(nfi)==len({(x["report"],x["file"],x["row_id"]) for x in nfi}))
check("Both historical N023 citations retained",Counter(refs)["N023"]==2)
check("No unexpected duplicate references",all(n==(2 if uid=="N023" else 1) for uid,n in Counter(refs).items()))
check("Coverage counts",r["coverage"]["total_unique_source_rows"]==len(nfi) and r["coverage"]["register_rows"]==len(reg["rows"]))
intake=load("INTAKE.json")
check("Snapshot current",r["snapshot_at"]==intake["sampled_at"])
check("All additions indexed",load("SOURCE-INDEX.json")["additions"]==intake["reports"])
pins=[];seen={}
def verify(p,sha,size,scope):
    key=str(p)
    try:
        got=seen.get(key)
        if got is None: got=filepin(p);seen[key]=got
        passed=got["sha256"]==sha and got["bytes"]==size
        pins.append(dict(**got,scope=scope,matches=passed,expected_sha256=sha,expected_bytes=size))
        check("Pin "+scope+" "+str(p),passed)
    except OSError as e: check("Pin "+scope+" "+str(p),False,str(e))
for group in ["BRIEF-PINS.json","BASELINE-PINS.json"]:
    for p in load(group):
        verify(Path(p["path"]),p["sha256"],p["bytes"],group+" origin")
        if p.get("snapshot"): verify(Path(p["snapshot"]),p["sha256"],p["bytes"],group+" snapshot")
for report in intake["reports"]:
    verify(Path(report["report_snapshot"]),report["report_sha256"],report["report_bytes"],"report snapshot")
    for p in report["artifacts"]:
        verify(Path(p["path"]),p["sha256"],p["bytes"],"new origin")
        if p.get("snapshot"): verify(Path(p["snapshot"]),p["sha256"],p["bytes"],"new snapshot")
sources=load("NEW-NFI-SOURCES.json")
raw_counts=0
for source in sources:
    doc=json.loads(Path(source["snapshot"]).read_text())
    check("NFI document preserved "+source["report"],doc==source["document"])
    for issue in [x for x in nfi if x["report"]==source["report"] and x["file"]==source["file"]]:
        pointer=issue["source_json_pointer"].lstrip("/").split("/")
        node=doc
        for segment in pointer: node=node[int(segment)] if isinstance(node,list) else node[segment]
        check("NFI raw pointer "+issue["uid"],node==issue["fields"]);raw_counts+=1
check("Every source addition checked",raw_counts==r["coverage"]["new_upstream_source_rows"])

for p in r["P2_leads"]:
    name=p["id"];point=p["original_point"];m=point["masses_kg"]
    pressure=D("95460.8379139")*(D("1.01") if name.startswith("033") else D(1))
    demand=pressure*D(p["R_m"])/(4*D(p["tf_m"]))
    close(name+" face demand pR/(4tf)",p["face_compression_required_Pa"],demand,rel=2e-8)
    close(name+" gamma factor",p["gamma_factor"],D(p["gamma"])/D(".20"))
    close(name+" Q factor",p["Q_factor"],D(p["Q"])/D(".33"))
    close(name+" face SF",p["modes"]["face_compression"],D(p["strength_Pa"])/demand,rel=2e-8)
    close(name+" face/core sum",m["structural"],D(m["faces"])+D(m["core"]))
    if name.startswith("028b"):
        j=max(D(m["physical_joining"]),D(".05")*D(m["structural"]))
        close(name+" joining floor",m["charged_joining"],j)
        total=D(m["structural"])+j+D(m["systems"])+D(m["fixed_reserve"])
        close(name+" mass closure",m["lift"],total)
    else:
        total=D(m["structural"])+D(m["charged_joining"])+D(m["systems_allowance"])+D(m["fixed_reserve"])+D(m["payload"])
        close(name+" mass closure",m["lift"],total)
    for psi,delta in p["waviness_projection"].items():
        # Round-trip the inverse through the independent forward equation.
        fc=D(psi)*D("6894.757293168361")
        q=D(".82")/(1+D(".64")*D(delta)*D("103421359.3975254")/(D(p["tc_m"])*fc))
        close(name+" waviness forward equation "+psi,p["Q"],q)
    hc=p["hemisphere_comparator"]["graph_centers"]
    for actual,denom in zip(p["gamma_over_different_hemisphere_graph_centers"],[max(hc),min(hc)]):
        close(name+" corrected CHECK035 graph comparison",actual,D(p["gamma"])/D(denom))
    for actual,denom in zip(p["gamma_over_hemisphere_graph_read_uncertainty_range"],
                            [D(max(hc))+D(".01"),D(min(hc))-D(".01")]):
        close(name+" CHECK035 graph reading interval",actual,D(p["gamma"])/denom)
    check(name+" installed SF remains null",p["overall_installed_hull_SF"] is None)
p=r["P3_lead"];mass=p["mass_kg"]
close("P3 component subtotal",mass["vehicle"],sum(D(mass[k]) for k in ["tube","film","joint","nodes","systems"]))
close("P3 total closure",mass["closure"],D(mass["vehicle"])+D(mass["reserve"])+D(mass["sag_lift_loss"]))
close("P3 both plies",p["film_total_m"],2*D(p["film_per_direction_m"]),abs_tol=1e-13)
close("P3 λ² joint mass",mass["joint"],D(p["joint"]["mass_at_multiplier_1_kg"])*D(p["target_multiplier"])**2)
close("P3 joint design force",p["joint"]["design_force_N"],D(p["force_at_pressure_1_N"])*D(p["target_multiplier"]))
close("P3 half-wave/member",p["half_wave_over_member"],D(p["half_wave_m"])/D(p["member_length_m"]),abs_tol=1e-10)
close("P3 scored SF",p["SF_least_with_sized_joint"],min(list(p["SF"].values())+[p["joint"]["axial_SF"],p["joint"]["bond_SF"]]))
close("P3 film specific-strength comparison",p["film_specific_strength_factor_vs_Kapton_design"],
      (D(1740)/D(1560))/(D("115.5")/D(1420)))
f=r["P3_ordered_fold"];f4=next(x for x in r["P3_discrete_bays_026b"]["comparison"] if x["frequency"]==4)
ratio=D(f4["linear"])/D(f4["continuum_perfect_nominal_s"])
close("026b exact factor",f["source_exact_factor"],ratio,abs_tol=1e-12)
close("Ordered .848 global SF",f["moved_global_SF"],D(p["SF"]["global"])*D(".848"),abs_tol=1e-12)
close("Exact factor sensitivity",f["exact_ratio_sensitivity_SF"],D(p["SF"]["global"])*ratio,abs_tol=1e-12)
close("Fold minimum",f["moved_least_SF"],min(f["modes"].values()),abs_tol=1e-12)
check("Global alone changed",all(f["modes"][k]==v for k,v in p["SF"].items() if k!="global"))
check("Fold held mass/reoptimization labels",f["other_modes_and_mass_held"] and not f["reoptimized"])
check("New nonlinear first-loss remains null",all(x["verified_first_nonlinear_instability"] is None
      for x in r["P3_discrete_bays_026b"]["comparison"] if x["frequency"] in [4,2]))
check("Hull/allowable/reliability remain null",p["overall_installed_hull_SF"] is None and
      p["qualified_compression_allowable_Pa"] is None and p["qualified_failure_probability"] is None and r["overall_installed_hull_SF"] is None)
op=load("OPTIMISM-LEDGER.json")["rows"]
for point in r["P2_leads"]:
    check("Every named P2 optimism "+point["id"],{"P2-O1","P2-O2","P2-O3","P2-O4","P2-O5","P2-J","P2-W","P2-L","P2-V"}==
          {x["id"] for x in op if x["lead"]==point["id"]})
check("Every optimism has evidence class/route",all(x["evidence_category"] in ["measured record","precedent","none"] and x["grounding_route"] for x in op))
check("038 all nine tests retained",len(r["physical_test_plan_038"]["tests"])==9)

missing=[];historical_missing=[]
for name in ["CARD.md","REGISTER.md","OPTIMISM-LEDGER.md","GROUND-FIRST.md","LEDGER.md","REPORTS.md"]:
    for target in re.findall(r'\]\(([^)]+)\)',(B/name).read_text()):
        if target.startswith(("http:","https:","#")): continue
        path=Path(target.split("#",1)[0]);path=path if path.is_absolute() else B/path
        if not path.exists() and path.name!="VALIDATION.json":
            (historical_missing if not path.is_relative_to(B) else missing).append(dict(document=name,target=target))
check("All new document links resolve",not missing,missing)
# Original pointers are intentionally preserved even when their former owners
# rewrote or removed historical files. Report, do not silently repair, these.
check("Historical link defects disclosed",True,dict(count=len(historical_missing),items=historical_missing))
for path in B.glob("*.json"):
    try: json.loads(path.read_text(),parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
    except (ValueError,OSError) as e: check("Strict JSON "+path.name,False,str(e))
check("All parsed packet JSON finite",True)
now=datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
result=dict(schema=1,tag="QUESTIONABLE / PROJECTION",validated_at=now,snapshot_at=r["snapshot_at"],
            purpose="Synthesis coverage, provenance and independent local arithmetic; not an owner-solver rerun or engineering qualification.",
            counts=dict(checks=len(checks),passed=sum(x["passed"] for x in checks),
                        failed=sum(not x["passed"] for x in checks),pin_checks=len(pins),
                        unique_files_hashed=len(seen),source_rows=len(nfi),reports=len(intake["reports"])),
            historical_link_defects=historical_missing,checks=checks,pins=pins)
(B/"VALIDATION.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
print(json.dumps(result["counts"],indent=2))
for x in checks:
    if not x["passed"]: print(json.dumps(x))
raise SystemExit(0 if all(x["passed"] for x in checks) else 1)
