"""Pin filed evidence and select frozen reference points; never execute foreign code."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import math
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
OWN = HERE.parents[3]
QUEUE = Path("unpublished-local-ref:ab52dba26d6cc3a7")
REPORTS = [
    "rpt-mainline030-opus-register-1020",
    "rpt-ref-d907de1e97319ecc3f9a",
    "rpt-mainline022c-grok-sag-in-scan-1020",
    "rpt-ref-58c781cbea9c220eb5b4",
    "rpt-ref-4f09fd6b4c4dd848ebb0",
    "rpt-ref-2bb3c2b520a8e5f8c750",
    "rpt-ref-a4768f77870336c8cdbb",
    "rpt-ref-3e02218a03708a878faa",
    "rpt-ref-7ce5b278fa083d87105b",
    "rpt-ref-5f14d083ceae03234596",
    "rpt-ref-244f32e2449e729d312f",
    "rpt-ref-6c81b0b188ad134a3ea2",
]
pins = []
reports = {}

def pin(path, expected=None, role="source"):
    path = Path(path).resolve()
    data = path.read_bytes()
    item = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                bytes=len(data), role=role)
    if expected:
        item["filed_sha256"] = expected["sha256"]
        item["filed_bytes"] = expected["bytes"]
        item["matches_filed"] = (item["sha256"] == expected["sha256"]
                                 and item["bytes"] == expected["bytes"])
    pins.append(item)
    return data

def clean(x):
    if isinstance(x, float) and not math.isfinite(x):
        return {"inherited_nonfinite": str(x), "not_a_finite_measurement": True}
    if isinstance(x, list):
        return [clean(v) for v in x]
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    return x

def artifact(report, basename):
    found = [p for p in reports[report]["artifacts"] if Path(p["path"]).name == basename]
    assert len(found) == 1, (report, basename, found)
    return Path(found[0]["path"])

for rid in REPORTS:
    report = json.loads(pin(QUEUE / (rid + ".json"), role="filed_report"))
    reports[rid] = report
    for a in report["artifacts"]:
        pin(a["path"], a)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

prior31_path = HERE.parent / "vacuum-mainline031-altitude-margin-1020/INPUTS.json"
prior27_path = HERE.parent / "vacuum-mainline027-size-as-lever-1020/RESULTS.json"
prior31 = json.loads(pin(prior31_path, role="own_frozen_reference"))
prior27 = json.loads(pin(prior27_path, role="own_frozen_reference"))
p2_raw = json.loads(artifact(REPORTS[1], "PROPERTY-CHECKS.json").read_text())
p2_routes = {
    x["route"]: x["floating_point"]
    for x in p2_raw["searches"]
    if x["material"] == "SR200" and x["joint_screen_enforced"]
}
p3_raw = json.loads(artifact(REPORTS[2], "SAG.json").read_text())
p3_new = json.loads(artifact(REPORTS[-1], "RESULTS.json").read_text())
vacuum34 = json.loads(artifact(REPORTS[-2], "RESULTS.json").read_text())
r20 = [x for x in prior27["P2"] if x["radius_m"] == 20
       and x["family"] == "aluminium" and x["scenario"] == "optimistic"]

result = {
    "schema": 1, "card": "MAINLINE-038", "status": "QUESTIONABLE/PROJECTION",
    "captured_at": dt.datetime.now(ZoneInfo("America/Vancouver")).isoformat(),
    "pins": pins,
    "reports": {k: {"at": v.get("at"), "body": v["body"]} for k, v in reports.items()},
    "case": prior31["case"],
    "P2_021b": prior31["reference_021b"]["floating_point"],
    "P2_028b_routes": p2_routes,
    "P2_028b_full_named_maxima": p2_raw["full_named_maxima"],
    "P2_255_upper_bound": p2_raw["S200F255_all_subsets_infeasible_proof"],
    "P3_022c": p3_raw["cap"],
    "P3_022c_sag_pins": p3_raw["pins"],
    "P2_R20_027": r20,
    "P2_036_report": reports["rpt-ref-5f14d083ceae03234596"]["body"],
    "P3_022d_selected": [
        {k: v for k, v in x.items() if k != "search"} for x in p3_new["all_primary_rows"]
        if x["case"]["grid"] == "equilateral" and x["case"]["branch"] == "cap"
        and (x["case"]["family"] == "cfrp_zylon"
             or x["case"]["family"] == "projection" and x["case"]["reserve"] == "019")
    ],
    "vacuum_034_geometry": vacuum34["geometry"],
    "vacuum_034_ledger": vacuum34["systems_ledger"],
    "vacuum_034_report": reports[REPORTS[-2]]["body"],
    "source_state_note": (
        "022d supersedes 022c optimization; 022c is retained as the frozen projected-material sensitivity. "
        "034 applies to its own older 021b/022c geometry, not current 028b/022d inventories. "
        "028b property check supersedes old nu=0.33 "
        "for its current routes. 026 applies to frequency 6 near s=2.04 m, not the "
        "s=6.15 m 022c optimum. Material allowables remain unqualified. "
        "Pin mismatches, if any, are disclosed and not treated as valid filed evidence."
    ),
    "normalization": "Inherited nonfinite JSON numbers become labelled objects; raw byte pins retained.",
}
(HERE / "INPUTS.json").write_text(json.dumps(clean(result), indent=2, allow_nan=False) + "\n")
bad = [p for p in pins if p.get("matches_filed") is False]
print(json.dumps({"pins": len(pins), "mismatches": bad,
                  "R20_candidates": [(x["mechanical"], x["mass_model"], x["least_SF"])
                                     for x in r20]}, indent=2))
