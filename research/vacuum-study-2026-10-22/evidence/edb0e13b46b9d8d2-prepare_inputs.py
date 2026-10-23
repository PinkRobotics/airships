"""Freeze evidence for an independent audit; never load the owner's executable."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def pin(path, expected=None):
    path = Path(path)
    data = path.read_bytes()
    entry = {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
             "bytes": len(data)}
    if expected:
        assert entry["sha256"] == expected["sha256"], path
        assert entry["bytes"] == expected["bytes"], path
        entry["verified_against_filed_pin"] = True
    PINS[str(path)] = entry
    return data


def read_json(path, expected=None):
    assert Path(path).suffix == ".json"
    return json.loads(pin(path, expected))


order = read_json(RUNTIME / "queue/submissions" / (ORDER + ".json"))
report = read_json(RUNTIME / "queue/submissions" / (OWNER_REPORT + ".json"))
for item in report["artifacts"]:
    pin(item["path"], item)  # Hash only; no executable is decoded or executed.
owner_root = Path(next(a["path"] for a in report["artifacts"]
                       if a["path"].endswith("/RESULTS.json"))).parent
owner_inputs = read_json(owner_root / "INPUTS.json")
owner_results = read_json(owner_root / "RESULTS.json")
for item in owner_inputs["pins"]:
    pin(item["path"], item)
for item in order.get("artifacts", []):
    pin(item["path"], item)

p2_root = WORKSPACES / "ref-70f7af6d0a8d64c42272/.ship/work/outputs/vacuum-mainline028b-joining-into-021b-1020"
p2_inputs = read_json(p2_root / "INPUTS.json")
p2_all = read_json(p2_root / "PROPERTY-CHECKS.json")
pin(p2_root / "METHOD.md")
for item in p2_inputs["new_primary_sources"]:
    pin(item["path"], item)
for name in ["sr200.txt", "sr200_lot.txt"]:
    pin(p2_root / "sources" / name)
p2 = next(x for x in p2_all["full_named_maxima"]
          if x["route"] == "af015_scarf" and x["material"] == "SR200")

p3_root = WORKSPACES / "ref-2543c559b19ffce7dfdd/.ship/work/outputs/vacuum-mainline022-p3-optimistic-floating-point-1020"
p3_inputs = read_json(p3_root / "INPUTS.json")
p3_all = read_json(p3_root / "SAG.json")
p3 = {key: value["equilateral"] for key, value in p3_all["cap"].items()}
pin(p3_root / "SAG.md")
pin(WORKSPACES / "ref-baa4584cf36c531365e7/.ship/work/outputs/vacuum-mainline034-holding-the-vacuum-1020/CARD.md")
pin(WS / ".ship/work/outputs/vacuum-mainline038-grounding-test-plan-1020/P3-LATEST.md")
source016 = read_json(WORKSPACES / "ref-8e599f371724624063d9/.ship/work/outputs/ref-81587374594cae9c1e2e-nfi-1019/INPUTS.json")
atmosphere = next(x["value"] for x in source016["inherited_values_used"]
                  if x["name"] == "atmosphere")
pin(ROOT / "sources/faa-airship.pdf")
for page in [24, 27, 35, 139, 140]:
    pin(ROOT / f"sources/faa-{page:03}.jpg")

data = {
    "schema": 1, "unit": "vacuum-mainline037-check-1020", "order": ORDER,
    "captured_at": datetime.now(ZoneInfo("America/Vancouver")).isoformat(),
    "tag": "QUESTIONABLE; alternative models and transferred properties are PROJECTION",
    "owner_code_policy": "loads037.py hashed as evidence only; never inspected, imported, or executed",
    "owner_inputs": owner_inputs, "owner_results": owner_results,
    "P2_028b_selected": p2, "P2_028b_case": p2_inputs["case"],
    "P3_022c_inputs": p3_inputs, "P3_022c_selected": p3,
    "atmosphere_016": atmosphere,
    "explicit_check_assumptions": {
        "Be_E_thermal_Pa": 290e9, "Be_E_full_endpoint_Pa": 293.6e9,
        "Be_alpha_per_K": 11.3e-6, "Al_alpha_per_K": 23.6e-6,
        "Al_k_W_mK": 130.0, "Al_rho_kg_m3": 2640.0,
        "g_m_s2": 9.80665, "knot_m_s_exact": 1852 / 3600,
        "owner_knot_m_s_for_replication": 0.514444,
        "foot_m": 0.3048, "drag_coefficient": 0.47,
        "mooring_multiplier_016": 1.4,
        "film_properties": {
            "projection": {"E_Pa": 10e9, "nu": 0.33, "rho": 970, "strength_Pa": 1.5e9,
                           "tag": "PROJECTION; nu inferred from filed output"},
            "mylar": {"E_Pa": 4.8e9, "nu": 0.38, "rho": 1400,
                      "strength_Pa": 151684660.449916,
                      "tag": "QUESTIONABLE; nu inferred from filed output"},
            "ti_kapton": {"E_Pa": 2.5e9, "nu": 0.34, "rho": 1420,
                          "strength_Pa": 115.5e6,
                          "tag": "QUESTIONABLE; nu inferred; strength reproduces upstream"},
            "cfrp_zylon": {"E_Pa": 180e9, "nu": 0.30, "rho": 1560,
                          "strength_Pa": 3.48e9,
                          "tag": "QUESTIONABLE; nu inferred; fiber-to-film transfer unqualified"}
        },
        "frame": {"E_Pa": 410e9, "rho": 3100, "alpha_per_K": 4.5e-6,
                  "basis": "022c SiC; all eight rows verified by mass and Euler identities"},
        "pad_replication": {
            "yield_Pa": 276e6, "nu": 0.33, "rho": 2700, "boss_radius_m": 0.025,
            "minimum_t_m": 0.001,
            "tag": "PROJECTION; these unstated inputs reproduce the filed logarithmic sizing term"
        },
        "thermal_countermodel": {
            "tag": "PROJECTION; a fully specified comparison, not recovery of missing owner inputs",
            "solar_W_m2": 970, "Tair_K": 284.9, "Tsky_day_K": 275,
            "Tsky_night_K": 260, "sky_view_factor": 0.5,
            "ground_K": 284.9, "interior_emissivity": 0.2,
            "h_cases_W_m2K": [0.5, 2.0, 5.0, 10.0],
            "interior": "closed diffuse-gray spherical cavity, constant inner emissivity, no internal source",
            "neglected": "in-plane face conduction, convection in evacuated cells, contact resistance, radiation across cells",
            "sigma_SB": 5.670374419e-8,
            "quadrature": "Gauss-Legendre surface-area weights in mu=cos(theta)"
        }
    },
    "pins": list(PINS.values())
}
(ROOT / "INPUTS.json").write_text(json.dumps(data, indent=2) + "\n")
print(json.dumps({"pins": len(PINS), "input_bytes": (ROOT / "INPUTS.json").stat().st_size}))
