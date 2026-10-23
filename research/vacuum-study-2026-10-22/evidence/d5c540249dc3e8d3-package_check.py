"""Custody/schema checks and atomic-outbox draft; no scientific calculations."""
from pathlib import Path
import json,hashlib,datetime

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

def read(name):
    return json.loads((ROOT/name).read_text())
def write(name,value):
    (ROOT/name).write_text(json.dumps(value,indent=2)+"\n")
def pin(path):
    b=path.read_bytes()
    return {"path":str(path.resolve()),"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}

checks=[]
def check(name,ok,**details):
    checks.append({"check":name,"passed":bool(ok),**details})

input_pins=read("INPUT-PINS.json")
for p in input_pins:
    for kind,path in (("snapshot",ROOT/p["copy"]),("live original",Path(p["source"]))):
        b=path.read_bytes()
        check("input "+kind,len(b)==p["bytes"] and hashlib.sha256(b).hexdigest()==p["sha256"],
            path=str(path),expected_sha256=p["sha256"])

excluded=read("EXCLUDED-EXECUTABLES.json")["paths_only_no_read_copy_hash_import_run"]
for p in read("owner/MANIFEST.json")["files"]:
    if Path(p["relative"]).parts[0] in {"inputs","sources"} and Path(p["relative"]).suffix in {".py",".sh",".js",".pyc"}:
        excluded.append(p["path"])
write("EXCLUDED-EXECUTABLES.json",{"paths_only_no_read_copy_hash_import_run":sorted(set(excluded))})
check("no executable in foreign-data snapshots",
      not any(p.suffix in {".py",".sh",".js",".pyc"} for d in ("owner","intake") for p in (ROOT/d).rglob("*") if p.is_file()))

write("INPUTS.json",{
    "unit":"vacuum-mainline053-check-1020","order":ORDER,"owner_report":"rpt-ref-3fb9907ba4e1c52825f0",
    "classification":"QUESTIONABLE / PROJECTION","owner_or_predecessor_executable_access":False,
    "input_pins":input_pins,"pinned_inputs":len(input_pins),
    "native_session":"ref-7477216a93e0bebe13b3",
    "equation_specification":["METHOD.md","owner/SPECIFICATION.md","owner/METHOD.md",
        "intake/inputs/048/METHOD.md","intake/inputs/048reply/BOUNDARY-REPLY.md"],
    "thermal_inputs":"owner/INPUTS.json; intake/inputs/048/COATINGS.json",
    "mechanical_inputs":"owner/INPUTS.json; intake/inputs/040/ATMOSPHERE.json",
    "primary_source_audit":"SOURCE-AUDIT.md",
    "independent_thermal_tables_used_for_accounts":["THERMAL-INDEPENDENT.json","HISTORICAL-INDEPENDENT.json"],
    "excluded_executables":len(set(excluded)),
    "next":"none"})
write("VISUAL-REVIEW.json",{"at":now,"file":"CHECK-053.png","review":"Viewed after footer-spacing correction; labels and units legible, footer clear of axes, all four models and numerical values shown.",
    "correction":"render01 moved the footer only; scientific values unchanged."})

result=read("RESULTS.json")
for name in ("RESULTS.json","INPUTS.json","NFI.json","MISMATCHES.json","SEARCH-SUMMARY.json",
             "FINAL-CHECKS.json","CROSSINGS-INDEPENDENT.json","FOUR-R10-GRID-INDEPENDENT.json",
             "OPTIMA-INDEPENDENT.json","LEAST-INDEPENDENT.json","DIRECT-GUARD-INDEPENDENT.json"):
    json.loads((ROOT/name).read_text(),parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    check("strict JSON",True,file=name)
check("final numerical comparisons passed",result["scalar_comparisons"]==result["scalar_passed"])
check("search passed",result["search"]["failures"]==[])
check("final scientific checks passed",result["final_failures"]==[])
check("no unresolved arithmetic mismatch",read("MISMATCHES.json")["unresolved_numerical_mismatches"]==[])
check("physical qualification remains open",result["installed_hull_SF"] is None and result["classification"]=="QUESTIONABLE / PROJECTION")
check("four nonblocking checker NFIs",len(read("NFI.json")["checker_open"])==4 and read("NFI.json")["all_nonblocking"])
executions=[read(p.name) for p in sorted(ROOT.glob("*.execution.json"))]
check("all executions admitted at same resource request",all(x["cores"]==1 and x["memory"]=="1G" for x in executions))
check("all executions ended",all("ended_at" in x for x in executions))
check("only disclosed execution failure",[(x["tag"],x["exit_code"]) for x in executions if x["exit_code"]!=0]==[("search01",1)])
write("TIMING.json",{"started_at":read("START.json")["at"],"packaged_at":now,"no_time_budget":True,
    "executions":[{k:r[k] for k in ("tag","started_at","ended_at","exit_code","cores","memory")} for r in executions],
    "note":"One search schema exception corrected; no admission refusal. Final render changed footer spacing only."})
for name in ("CARD.md","METHOD.md","SOURCE-AUDIT.md","CHECK-053.pdf","CHECK-053.png","CHECK-053.svg"):
    check("required artifact present",(ROOT/name).is_file() and (ROOT/name).stat().st_size>0,file=name)
write("DELIVERY-CHECKS.json",{"at":now,"checks":checks,"passed":sum(c["passed"] for c in checks),
    "failed":sum(not c["passed"] for c in checks),"input_pins":len(input_pins)})
assert all(c["passed"] for c in checks),[c for c in checks if not c["passed"]]

note=WORKSPACE/".ship/notes/vacuum-mainline053-check-1020.md"
note.write_text(f"""# CHECK-053 handoff

Completed {now}; authority {ORDER}.
Output: {ROOT}/CARD.md.
Report to file: .ship/outbox/{REPORT}.json.

Numerical PASS: 653001 scalar comparisons, 7310 search checks and 6342 final checks.
Reproduced four R10 gradients/swings, 4.3889250393713155 kg maximum loss,
288 frozen scarf crossings and 85 global crossings.
All 5760 endpoint grids, 360 mask-11 reoptimizations and 60 primary least rows checked.
Maximum independent endpoint payload difference 0.00010391194336989429 kg.
Core-gap and inner-enclosure radiation are distinct paths; effective .20 remains unqualified.
Four checker NFI clarifications, nine owner groups and six inherited registers carried.
Exact initial checker discrepancies, corrections and one schema failure preserved.
No owner executables read/copied/hashed/imported/run; no other-seat contact.
All scientific executions admitted/released at one core, 1 GiB; no exit75.
No named successor. After filing read own queue once, set SLEEPING and end; no waiter.
""")

files=[]
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and p!=ROOT/"MANIFEST.json":
        row=pin(p);row["relative"]=str(p.relative_to(ROOT));files.append(row)
write("MANIFEST.json",{"schema":1,"unit":"vacuum-mainline053-check-1020","generated_at":now,
    "file_count":len(files),"excludes":["MANIFEST.json (self)"],"files":files})
body="""CHECK-053 complete: numerical PASS; QUESTIONABLE/PROJECTION.

Own equations reproduce 653,001 scalar comparisons, including all 9,640 settled thermal rows. All 7,310 search checks and 6,342 final cross-checks pass. No owner executable was accessed.

R10 gradients 0.464608894/0.426155555/0.451215439/0.413901181 K and swings 33.640781944/31.120115857/33.638308050/31.118178070 K reproduce the four boundaries. Core-gap and inner-enclosure radiation are distinct paths, so simultaneous inclusion is not inherently double counting. Effective gap emissivity .20 remains unqualified; two .20 gray plates give 1/9.

Maximum resized loss is 4.388925039 kg. Independent reoptimization gives 4.388889843 kg; largest individual endpoint discrepancy is 0.000103912 kg. All 5,760 endpoint grids, 360 reoptimized endpoints and 60 primary least-set rows pass. No endpoint float sign or minimum-set choice changes.

All 288 frozen scarf crossings and 85 global crossings reproduce. Largest scarf deficit is 0.0366%; resizing restores the declared scalar constraints. This is not installed qualification.

Exact differences and corrected checker conventions are retained. Four checker NFI clarifications extend nine owner groups and six inherited registers. All 206 input pins verify. Ten one-core/1-GiB admitted runs ended; one disclosed schema failure was corrected.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]