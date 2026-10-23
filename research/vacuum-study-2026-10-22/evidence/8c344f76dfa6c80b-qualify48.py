#!/usr/bin/env python3
"""Resolve the eight selected E-axis points and price emittance-statistic uncertainty."""
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
import model48 as m

B=Path(__file__).resolve().parent
tables=json.loads((B/"THERMAL-TABLES.json").read_text())
audit=[]
for name in ["MLCCAg","CCAg","AgFEP05","AgFEP1"]:
    m.THERMAL=tables[name]
    rows=json.loads((B/f"RESULTS-{name}.json").read_text())["rows"]
    for row in rows:
        p=row["least"]["least"]
        if p is None or not p["mask"]&4:
            continue
        ceiling=p["usage"];s=m.Settings(**p["settings"]);r=row["R_m"]
        def value(uE):
            q=m.optimize(r,p["mask"],[ceiling,ceiling,uE,ceiling],s,n=800,detail=False)
            return -1e20 if q is None else q
        samples=[dict(E_usage=float(u),payload_kg=value(u)) for u in np.linspace(0,ceiling,9)]
        opt=minimize_scalar(lambda u:-value(u),bounds=(0,ceiling),method="bounded",
                            options={"xatol":1e-7})
        samples.append(dict(E_usage=float(opt.x),payload_kg=float(-opt.fun)))
        best=max(samples,key=lambda x:x["payload_kg"])
        delta=best["payload_kg"]-p["signed_payload_kg"]
        audit.append(dict(id=row["id"],usage_ceiling=ceiling,
                          best_independent_E=best,samples=samples,
                          improvement_kg=delta,
                          endpoint_retains_minimax_to_mass_tolerance=delta<.002))
        print(row["id"],delta,flush=True)
assert all(x["endpoint_retains_minimax_to_mass_tolerance"] for x in audit)

# .40 is a deliberately low emittance sensitivity for the classical coating.
# Reuse the exact AgFEP05 thermal pair, keeping CCAg mass and no tape adhesive.
rows=json.loads((B/"RESULTS-CCAg.json").read_text())["rows"]
source=next(x for x in rows if x["R_m"]==10 and x["weather"]=="ISA" and x["floor"]
            and x["drying"]=="bake70" and x["external_water_kg_m2"]==.1)
s=m.Settings(**source["two_factor_endpoint"]["settings"])
m.THERMAL=tables["AgFEP05"]
low=m.least(10,s)
point=next(x["solution"] for x in low["endpoint_trials"] if x["mask"]==11)
m.dump(B/"ADDITIONAL-AUDIT.json",dict(
    passed=True,E_axis_checks=audit,
    classical_low_emittance_sensitivity=dict(
        tag="PROJECTION",alpha=.09,assumed_hemispherical_epsilon=.40,
        endpoint=point,least=low,
        note="This tests robustness to optical-statistic uncertainty; .40 is not a measured CCAg value."),
    scope="Independent E usage at the selected minimax ceiling, nine samples plus bounded refinement; numerical tolerance 0.002 kg."))
print("Additional audit passed; classical .40-emittance payload",point["signed_payload_kg"],flush=True)
