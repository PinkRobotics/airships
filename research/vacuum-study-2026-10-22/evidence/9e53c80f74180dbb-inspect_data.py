import sys,json
from pathlib import Path
r=Path(__file__).resolve().parent
sys.path[:0]=[str(r),"unpublished-local-ref:e2218733e161c504"]
import numpy as np
for res in ["5","019"]:
 p=r/f"intake/upstream/intake/check041/runs/f5-{res}-m24"
 d=np.load(p/"STATIC.npz",allow_pickle=False)
 print(res,{k:d[k].shape for k in d.files})
 x=json.loads((r/"intake/upstream/intake/041/RESULTS.json").read_text())["best_closure_by_reserve"][res]
 print(json.dumps({k:v for k,v in x.items() if not isinstance(v,(dict,list))},indent=1)); print("section",x.get("section"));print("masses",x.get("mass_kg"));print("keys",list(x))
 print("ref",json.loads((p/"RESULTS.json").read_text())["section"])
