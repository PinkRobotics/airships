import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
from check_fe import solve
import time
mats=materials();audit=Audit()
old=json.loads((ROOT/"FE-CHECK-all.json").read_text())
selected=set(r["row"] for r in old["rows"] if not r["passed"] and r["field"].startswith("linear_multipliers"))
dump("history/FE-CHECK-all-initial.json",old)
for row in read("FE-ALL.json")["rows"]:
    label=row["label"]
    calc=json.loads((ROOT/"fe"/(label+".json")).read_text())
    if mats[row["material"]]["screen_compression_Pa"] is None:
        calc["individual_secondary_failure_members_at_q1"]["compression"]=None
        dump("fe/"+label+".json",calc)
    for key,ids in row["individual_secondary_failure_members_at_q1"].items():
        alt=calc["individual_secondary_failure_members_at_q1"][key]
        audit.check(label,"failed_ids/"+key,True,ids==alt)
    if label in selected:
        start=time.monotonic()
        expanded,_=solve(row,mats,eigen_number=12)
        dump("eigen-expanded/"+label+".json",expanded)
        for j,x in enumerate(row["linear_multipliers"]):
            nearest=min(expanded["linear_multipliers"],key=lambda v:abs(v-x))
            audit.check(label,f"owner_returned_mode[{j}]_found_in_independent_12",x,nearest,rtol=3e-6,atol=1e-7)
        audit.check(label,"lowest_unchanged",calc["linear_multipliers"][0],expanded["linear_multipliers"][0],rtol=3e-6)
        audit.check(label,"expanded_eigen_residuals_valid",True,max(expanded["eigen_relative_residuals"])<1e-6)
        print(json.dumps(dict(label=label,seconds=time.monotonic()-start)),flush=True)
audit.save("FE-RECONCILIATION.json")
