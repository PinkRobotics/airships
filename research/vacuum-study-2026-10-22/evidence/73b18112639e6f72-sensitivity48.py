#!/usr/bin/env python3
"""Additional material, optical and operating assumptions; no fitted properties."""
import json
import itertools
import time
from dataclasses import replace
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
import model48 as m
from thermal48 import evaluate

B = Path(__file__).resolve().parent
tables = json.loads((B/"THERMAL-TABLES.json").read_text())
profiles = {x["id"]: x for x in json.loads((B/"COATINGS.json").read_text())}
rows = []
start = time.monotonic()

def setting(profile, **kw):
    c = profiles[profile]
    coating = c["areal_mass_kg_m2"]*(1.05 if "FEP" in profile else 1.1)
    film = .028 if profile == "AgFEP05" else .054
    water = (((film*.0001+(c["areal_mass_kg_m2"]-film)*.01)*1.05)
             if "FEP" in profile else coating*.01)
    return replace(m.Settings(finish_id=profile, coating=coating,
                   structural_primer_kg_m2=.01, moisture_scale=.1,
                   finish_water_kg_m2=water), **kw)

def save():
    m.dump(B/"SENSITIVITIES.json", dict(complete=False, rows=rows))

# These are explicitly assumed wet/aged optical pairs, not water-film data.
for label, alpha, epsilon in [
        ("wet_optics_assumed", .20, .95),
        ("aged_alpha015_assumed", .15, .80),
        ("aged_alpha020_assumed", .20, .80)]:
    optical = {}
    for r in [10,12,15]:
        optical[str(r)] = evaluate(r,np.geomspace(.001*r/10,1.5*r/10,241),
                                   n=128,alpha_out=alpha,epsilon_out=epsilon)
    tables[label] = optical
    m.THERMAL = optical
    for r, weather in itertools.product([10,12,15],["ISA","optimistic","both"]):
        s = setting("MLCCAg", weather=weather)
        # Full least search is warranted at R10; larger rows price endpoints.
        result = m.least(r,s) if r == 10 else None
        endpoint = (next(x["solution"] for x in result["endpoint_trials"] if x["mask"]==11)
                    if result else m.optimize(r,11,1,s))
        rows.append(dict(type=label, alpha=alpha, epsilon=epsilon, R_m=r,
                         weather=weather, endpoint=endpoint, least=result))
        save()
        print(label,r,weather,endpoint["signed_payload_kg"],flush=True)

for profile in ["MLCCAg","CCAg","AgFEP05","AgFEP1"]:
    m.THERMAL = tables[profile]
    s0 = setting(profile)
    cases = {
        "no_extra_structural_primer": replace(s0,structural_primer_kg_m2=0),
        "structural_primer_50g_m2": replace(s0,structural_primer_kg_m2=.05),
        "AF_severe_9p16pct_after_90pct_removal":
            replace(s0,adhesive_water_fraction=.0916),
        "AF_severe_9p16pct_no_extra_drying":
            replace(s0,adhesive_water_fraction=.0916,moisture_scale=1),
        "99pct_material_water_removal": replace(s0,moisture_scale=.01),
        "edge_scarf_scalar_interaction": replace(s0,edge_scarf_interaction=True),
        "250F_cure_original_scarf": replace(s0,cure_temperature_K=394.2611111111111,
                                           scarf_ratio=30),
        "desiccant_zero_capture": replace(s0,moisture_scale=1,desiccant=True,
                                          desiccant_capture_fraction=0),
    }
    if profile == "CCAg":
        upper = profiles[profile]["mass_band_kg_m2"][1]*1.10
        cases["classical_maximum_layer_recipe"] = replace(
            s0,coating=upper,finish_water_kg_m2=upper*.01)
    for label,s in cases.items():
        p = m.optimize(10,11,1,s,n=900)
        full = m.optimize(10,15,1,s,n=900)
        rows.append(dict(type=label,profile=profile,R_m=10,weather="ISA",
                         endpoint=p,all_four_endpoint=full,settings=s.__dict__))
        save()
        print(profile,label,None if p is None else p["signed_payload_kg"],flush=True)

# A day SF is based on |rise|. Search only its physically relevant warm branch
# and report the largest alpha that satisfies BOTH the legacy day criterion
# and the explicit day-to-night swing criterion at the source geometry.
limits=[]
tf=.000799676281908861
tc=.022106790073532958
factor=12.3e-6*np.sqrt(290e9*tf*46884349.59354485/tc)
for epsilon in [.4,.48,.65,.8,.89,.9]:
    def score(alpha):
        t=evaluate(10,[tc],n=37,midpoint=True,fixed_iterations=25,
                   legacy_project=True,solid_density=2640,
                   alpha_out=alpha,epsilon_out=epsilon)
        day=241316.50526089262/(factor*abs(t["rise_K"][0]))
        cycle=241316.50526089262/(factor*abs(t["swing_K"][0]))
        return min(day/1.678,cycle)-1
    bound=brentq(score,.05,.4,xtol=1e-10)
    limits.append(dict(epsilon=epsilon,maximum_alpha_for_day_and_cycle=bound))

m.dump(B/"SENSITIVITY-THERMAL.json",{k:v for k,v in tables.items()
                                  if k not in profiles})
m.dump(B/"SENSITIVITIES.json",dict(
    tag="QUESTIONABLE / PROJECTION",complete=True,rows=rows,
    optical_limits_at_037_geometry=limits,elapsed_s=time.monotonic()-start,
    notes=[
        "Wet and aged optical pairs are assumed; no wet-surface qualification is claimed.",
        "All primary rows retain 0.1 kg/m2 external water and 10 g/m2 structural primer.",
        "Severe adhesive fraction is 2M/70 C immersion evidence transferred to 2U only as a sensitivity.",
        "A null optimum means no geometry meets the retained scalar constraints in the stated search domain."
    ]))
print("complete",len(rows),flush=True)
