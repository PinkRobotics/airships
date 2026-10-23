"""Diagnose stated thermal boundary conventions using published result data."""
import json
import math
from pathlib import Path

R = Path(__file__).resolve().parent
d = json.loads((R/"intake/base040/inputs/037/RESULTS.json").read_text())["p2_thermal"]["coated_outer"]
sigma, ta, eps = 5.670374419e-8, 284.9, .9
rows = []
for location, mu, outer_key, inner_key in [
    ("sunward", 36/37, "T_outer_subsolar_K", "T_inner_subsolar_K"),
    ("antisolar", -36/37, "T_outer_antisolar_K", "T_inner_antisolar_K"),
]:
    to, ti = d[outer_key], d[inner_key]
    sky4 = .5*(1+mu)*275**4 + .5*(1-mu)*ta**4
    flux = .2*970*max(mu,0) + eps*sigma*(sky4-to**4) - d["U_conduction_W_per_m2K"]*(to-ti)
    rows.append(dict(location=location, implied_h_W_m2K=flux/(to-ta),
                     implied_cavity_fourth_moment_K4=ti**4-d["U_conduction_W_per_m2K"]*(to-ti)/(.2*sigma)))
out = dict(inferences_from_reported_temperatures=rows, warning="Boundary-convention diagnostic, not a fitted material property.")
(R/"THERMAL-DIAGNOSTIC.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
