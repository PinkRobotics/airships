#!/usr/bin/env python3
"""MAINLINE-009d. The 5 percent point under the MAINLINE-018 curves.

Geometry is the filed 009c-5 row. It is not searched again.
The curves are the two functions filed in 018. Nothing here is a certification.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
STARTED = sys.argv[1]
POINT = Path(
    "unpublished-local-ref:7f7c51a246885c2d"
    "/.ship/work/outputs/vacuum-mainline009c5-margin-five-percent-1019/POINT.json"
)
R018 = Path(
    "unpublished-local-ref:7f7c51a246885c2d"
    "/.ship/work/outputs/vacuum-mainline018-crimp-branch-kd-1019/RESULTS.json"
)


def g(x: float) -> str:
    return format(x, ".12g")


def gamma_optimistic(vc: float) -> float:
    return 0.20 + 0.40 * min(vc, 2.0)


def gamma_conservative(vc: float) -> float:
    return 0.20


def main() -> None:
    point = json.loads(POINT.read_text())
    prior = json.loads(R018.read_text())
    if prior["curves"]["optimistic"]["gamma"] != "0.20 + 0.40 * min(Vc, 2)":
        raise SystemExit("018 optimistic formula moved")
    if prior["curves"]["conservative"]["gamma"] != "0.20":
        raise SystemExit("018 conservative formula moved")
    opt = point["optimum"]
    vc = opt["Vc"]
    if opt["branch"] != "shear_crimping" or opt["gamma_d"] != 1.0:
        raise SystemExit("009c-5 point is no longer the crimp branch at gamma 1")
    modes0 = opt["modes_at_0.20_design_wrinkle"]
    bare = modes0["core_shear_crimping"]
    if abs(modes0["global_buckling"] - bare) > 1e-12:
        raise SystemExit("filed global and crimp differ")
    curves = {}
    for name, fn, tag in (
        ("optimistic", gamma_optimistic, "PROJECTION"),
        ("conservative", gamma_conservative, "QUESTIONABLE"),
    ):
        gamma = fn(vc)
        design_global = bare * (gamma / opt["gamma_d"])
        modes = dict(modes0)
        modes["global_buckling"] = design_global
        design = dict(modes)
        design.pop("global_buckling")
        design["core_shear_crimping"] = design_global
        ordered = sorted(design.items(), key=lambda item: (item[1], item[0]))
        curves[name] = {
            "gamma": gamma,
            "tag": tag,
            "modes": modes,
            "bare_crimp_SF": bare,
            "design_global_SF": design_global,
            "least_SF": ordered[0][1],
            "governing": ordered[0][0],
            "second_mode": ordered[1][0],
            "second_SF": ordered[1][1],
            "factor_to_SF_1": 1.0 / ordered[0][1],
        }
    if curves["optimistic"]["gamma"] != 1.0:
        raise SystemExit("optimistic gamma on this Vc is not 1")
    if abs(curves["optimistic"]["least_SF"] - opt["least_SF"]) > 1e-12:
        raise SystemExit("optimistic curve moved the filed least factor")
    ended = datetime.now(ZONE).isoformat(timespec="seconds")
    out = {
        "schema": 1,
        "card": "MAINLINE-009d",
        "unit": "vacuum-mainline009-combined-point-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": ended,
        "held_from": "rpt-ref-656730310661fdf86af6",
        "curves_from": "rpt-ref-089ed1faaaf72118b83f",
        "geometry_held": {
            "tf_m": opt["tf_m"],
            "core_m": opt["core_m"],
            "Vc": vc,
            "Kc": opt["Kc"],
            "branch": opt["branch"],
            "float_margin": opt["masses_kg"]["float_margin"],
            "payload_kg": opt["masses_kg"]["payload"],
            "total_kg": opt["masses_kg"]["total"],
        },
        "carried_point": "optimistic",
        "why_carried": "On this branch the optimistic curve is gamma 1, the handbook step. The filed 009c-5 factor stands. The conservative curve is the alternative if the crimp exception is withheld. It is not a replacement geometry.",
        "curves": curves,
        "p3": "PENDING-011b. Not scored.",
        "not_folded": "rpt-mainline014b-grok-metal-honeycomb-1019 has filed. This re-run does not take that core.",
        "kd_columns": "None. The 018 curves replace kd. They are not stacked on 0.20, 0.90 or 0.1407.",
    }
    (ROOT / "POINT.json").write_text(json.dumps(out, indent=1) + "\n")
    print(ended)
    for name, curve in curves.items():
        print(name, "gamma", g(curve["gamma"]), "least", g(curve["least_SF"]), curve["governing"], "second", curve["second_mode"], g(curve["second_SF"]), "factor", g(curve["factor_to_SF_1"]))


if __name__ == "__main__":
    main()
