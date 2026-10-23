"""Small independent optimizer cross-check before the full exhaustive batches."""
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import independent_search as s

r=Path(__file__).resolve().parent
data=json.loads((r/"intake/owner/RESULTS.json").read_text())
ids=[
    "MLCCAg-R10-ISA-floor-bake70-retained_water",
    "MLCCAg-R12-optimistic-floor-bake70-retained_water",
    "MLCCAg-R15-both-floor-desiccant-retained_water",
    "AgFEP05-R10-optimistic-actual-dry_gas-dry_exterior",
]
rows=[]
start=time.monotonic()
for key in ids:
    row=next(x for x in data["rows"] if x["id"]==key)
    p=row["two_factor_endpoint"]
    own=s.optimize(row["R_m"],11,1.,p["settings"])
    rows.append(dict(id=key,kind="endpoint",owner=p["signed_payload_kg"],own=own,
                     difference=own["payload_kg"]-p["signed_payload_kg"]))
    least=row["least"]["least"]
    if least is not None:
        own=s.optimize(row["R_m"],least["mask"],least["usage"],p["settings"])
        rows.append(dict(id=key,kind="least_at_supplied_usage",owner=least["signed_payload_kg"],
                         own=own,difference=own["payload_kg"]-least["signed_payload_kg"]))
out=dict(rows=rows,elapsed_seconds=time.monotonic()-start)
(r/"SEARCH-SMOKE.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
