"""Freeze numerical inputs from already pin-verified predecessor JSON."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def read(path):
    return json.loads((ROOT / path).read_text())

a = read("intake/028b/INPUTS.json")
b = read("intake/028b/PROPERTY-CHECKS.json")
c = read("intake/027/INPUTS.json")
d = read("intake/027/RESULTS.json")
held = []
for x in b["searches"]:
    if x["material"] == "SR200" and x["joint_screen_enforced"]:
        p = x["floating_point"]
        held.append({"route": x["route"], "point": p,
                     "E_Pa": 290e9, "nu": .0752,
                     "gamma_constant": p["needed"]["gamma"],
                     "wrinkle": p["needed"]["wrinkle"]})
r20 = next(x for x in d["P2"] if x["radius_m"] == 20 and
           x["scenario"] == "optimistic" and x["family"] == "aluminium" and
           x["mechanical"] == "full_021" and x["mass_model"] == "coupled")
out = {
    "unit": "vacuum-mainline036-be-sheet-compression-1020",
    "tag": "PROJECTION", "overall_installed_SF": None,
    "pin_record": "intake/PINS.json",
    "R10": {"case": a["case"], "routes": a["routes"], "panel": a["panel"],
            "constants": a["constants"], "cores": a["cores"], "held": held,
            "upstream_full": [x for x in b["full_named_maxima"] if x["material"] == "SR200"]},
    "R20": {"case": c["case"], "scenario": c["scenarios"]["optimistic"],
            "cores": c["aluminium_candidates"], "selected_core": c["cores"]["aluminium"],
            "reference": r20},
    "Fcy_sensitivities_MPa": [255, 283, 42*6.894757293168361, 300.3333333333333,
                             48*6.894757293168361, 50*6.894757293168361, 345, 379.2,
                             57.5*6.894757293168361],
    "strength_scope": "Values are uniaxial-to-equibiaxial PROJECTION sensitivities, not thin-sheet allowables.",
    "yield_definition": "Required effective equibiaxial membrane compression limit at scalar model SF=1.",
    "thickness_basis": "Finished face thickness; all extra removal/tolerance sensitivities are separately identified."
}
(ROOT / "INPUTS.json").write_text(json.dumps(out, indent=2) + "\n")
print({"R10_cores": len(a["cores"]), "R20_aluminium_cores": len(c["aluminium_candidates"]),
       "held_routes": [x["route"] for x in held]})
