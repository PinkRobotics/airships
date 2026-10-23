#!/usr/bin/env python3
import json
import time
from pathlib import Path
import numpy as np
from thermal48 import evaluate

B = Path(__file__).resolve().parent
coatings = json.loads((B/"COATINGS.json").read_text())
tc0 = .022106790073532958
tf0 = .000799676281908861
E = 290e9
Gc = 46884349.59354485
Wtyp = 241316.50526089262
dalpha = 12.3e-6
factor_per_K = dalpha*np.sqrt(E*tf0*Gc/tc0)
tables, screen = {}, []
start = time.monotonic()
for c in coatings:
    if c["alpha"] is None:
        screen.append(dict(id=c["id"], status="No sourced optical pair; not scored."))
        continue
    kw = dict(alpha_out=c["alpha"], epsilon_out=c["epsilon"])
    legacy = evaluate(10, [tc0], n=37, midpoint=True, fixed_iterations=25,
                      legacy_project=True, solid_density=2640, **kw)
    common = evaluate(10, [tc0], n=128, **kw)
    rise = legacy["rise_K"][0]
    swing = legacy["swing_K"][0]
    day_sf = Wtyp/(factor_per_K*abs(rise))
    cycle_sf = Wtyp/(factor_per_K*abs(swing))
    edge_sf = (25*6894.757293168361 /
               (dalpha*1.002*(366.4833333333333-common["min_outer_K"][0]) *
                np.sqrt(2*(.5*67e9*16.018463373960138/2700)*Gc)))
    screen.append(dict(
        id=c["id"], legacy_037_day_SF=day_sf,
        legacy_037_full_swing_SF=cycle_sf,
        legacy_037_day_at_least_reference=bool(day_sf >= 1.6775),
        legacy_037_cycle_at_least_one=bool(cycle_sf >= 1),
        current_200F_minimum_edge_SF=edge_sf,
        legacy=legacy, common=common))
    tables[c["id"]] = {}
    for r in [10,12,15]:
        tables[c["id"]][str(r)] = evaluate(r, np.geomspace(.001*r/10, 1.5*r/10, 241),
                                          n=128, **kw)
    print(c["id"], round(day_sf,6), round(cycle_sf,6), round(edge_sf,6), flush=True)
    (B/"THERMAL-SCREEN.json").write_text(json.dumps(screen,indent=2,allow_nan=False)+"\n")
    (B/"THERMAL-TABLES.json").write_text(json.dumps(tables,indent=2,allow_nan=False)+"\n")
(B/"THERMAL-SCREEN.json").write_text(json.dumps(screen,indent=2,allow_nan=False)+"\n")
(B/"THERMAL-RUN.json").write_text(json.dumps(dict(complete=True,elapsed_s=time.monotonic()-start),indent=2)+"\n")
