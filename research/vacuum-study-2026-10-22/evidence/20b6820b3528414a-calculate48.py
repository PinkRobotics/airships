#!/usr/bin/env python3
"""Finish-specific 040 reruns; each worker owns its own output files."""
import itertools
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import model48 as m

B = Path(__file__).resolve().parent
profiles = {x["id"]: x for x in json.loads((B/"COATINGS.json").read_text())}
tables = json.loads((B/"THERMAL-TABLES.json").read_text())
name = sys.argv[1]
profile = profiles[name]
m.THERMAL = tables[name]
is_fep = "FEP" in name
installed = profile["areal_mass_kg_m2"]*(1.05 if is_fep else 1.10)
# Film/metal mass and adhesive are both in the 88/115 g/m2 tape entry.
fep_mass = .028 if name == "AgFEP05" else .054
finish_water = ((fep_mass*.0001 + (profile["areal_mass_kg_m2"]-fep_mass)*.01)*1.05
                if is_fep else installed*.01)
started = datetime.now(timezone.utc).isoformat()
t0 = time.monotonic()
rows = []
out = B/("RESULTS-"+name+".json")
for r, weather, floor, route, water in itertools.product(
        [10,12,15], ["ISA","optimistic","both"], [False,True],
        ["dry_gas","bake70","desiccant"], [.1,0.]):
    s = m.Settings(
        weather=weather, floor=floor, coating=installed,
        finish_id=name, external_water_kg_m2=water,
        structural_primer_kg_m2=.01,
        moisture_scale=.1 if route == "bake70" else 1.,
        finish_water_kg_m2=finish_water, desiccant=route=="desiccant")
    result = m.least(r, s)
    endpoint = next(t["solution"] for t in result["endpoint_trials"] if t["mask"]==11)
    row = dict(id=f"{name}-R{r}-{weather}-{'floor' if floor else 'actual'}-{route}-"
                  f"{'retained_water' if water else 'dry_exterior'}",
               profile=name, R_m=r, weather=weather, floor=floor,
               drying=route, external_water_kg_m2=water,
               least=result, two_factor_endpoint=endpoint)
    rows.append(row)
    m.dump(out, dict(complete=False, rows=rows, started_at=started))
    least = result["least"]
    print(row["id"], "payload", None if endpoint is None else round(endpoint["signed_payload_kg"],4),
          "least", None if least is None else (least["selected_axes"],round(least["usage"],6)), flush=True)
m.dump(out, dict(
    tag="QUESTIONABLE / PROJECTION", complete=True, rows=rows,
    started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
    elapsed_s=time.monotonic()-t0, profile=profile,
    coating_installed_kg_m2=installed,
    structural_primer_additional_kg_m2=.01,
    model_notes=[
        "All external liquid remains in the retained-water rows for every drying route.",
        "Zero exterior water is a separate operating condition, not a bake-out result.",
        "Ground conditioning equipment is not carried; 100 kg onboard systems stays reserved.",
        "Nominal film mass is unchanged by TML. Added water stays aboard if adsorbed.",
        "Mass includes an extra 10 g/m2 structural-primer allowance; its process is unqualified.",
        "Film overlap 5%, deposited-coating installation allowance 10% are assumptions.",
        "Thermal table includes maximum day/night gradient and curvature at each core thickness.",
        "All assembly pass flags are conditional scalar model results, never installed qualification."
    ]))
