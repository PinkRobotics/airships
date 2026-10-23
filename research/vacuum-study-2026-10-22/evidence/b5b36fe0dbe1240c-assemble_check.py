"""Verify and package the independent 022b/022c check; never files a queue item."""

import ast
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIFT = 4889.44215019


def read(name):
    return json.loads((ROOT / name).read_text())


def write(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def main():
    arithmetic, studies, source = read("ARITHMETIC.json"), read("STUDIES.json"), read("SOURCE-CHECKS.json")
    pins, pdfs = read("INPUT-PINS.json"), read("EXTERNAL-PDF-PINS.json")
    checks = []

    def check(name, passed, **evidence):
        checks.append({"name": name, "passed": bool(passed), **evidence})
        if not passed:
            raise ValueError(checks[-1])

    for expected in pins + pdfs:
        actual = pin(expected["path"])
        check("source pin " + expected["path"],
              actual["sha256"] == expected["sha256"] and actual["bytes"] == expected["bytes"])
    check("all published-coordinate and independent-grid field comparisons",
          not arithmetic["mismatches"], count=len(arithmetic["comparisons"]))
    check("all ancillary arithmetic and printed row comparisons",
          source["all_passed"], count=len(source["checks"]))
    rows = arithmetic["at_published_geometry"]
    check("all 70 published rows close the mass balance",
          len(rows) == 70 and all(abs(r["mass_closure_kg"] - LIFT) < 1e-7 for r in rows.values()))
    max_perry_residual = 0.
    for label, row in rows.items():
        stress = row["SF_perry"] * row["sigma_axial_Pa"]
        extreme = stress * (1 + row["eta"] / (1 - stress / row["Euler_stress_Pa"]))
        strength = 380e6 if "mylar" in label else 3900e6
        max_perry_residual = max(max_perry_residual, abs(extreme / strength - 1))
    check("compression roots independently satisfy the amplified stress equation",
          max_perry_residual < 1e-8, maximum_relative_residual=max_perry_residual)
    missing = []
    for stage in ("EQUILIBRIUM", "GAMMA", "FOLD"):
        doc = read("inputs/" + stage + ".json")
        for name, block in doc["cases"].items():
            for grid, expected in block.items():
                label = "/".join((stage, name, grid))
                missing += [(label, k) for k in expected if k not in rows[label]]
    sagdoc = read("inputs/022c/SAG.json")
    for kind in ("cap", "membrane"):
        for name, block in sagdoc[kind].items():
            for grid, expected in block.items():
                label = "/".join(("022c_" + kind, name, grid))
                missing += [(label, k) for k in expected if k not in rows[label]]
    check("no published row fields silently omitted", not missing, missing=missing)
    refined = studies["continuous_refinement"]
    check("all continuous witnesses improve or match published feasible candidates",
          all(v["SF_increase"] >= -1e-8 for v in refined.values()), count=len(refined))
    cap = studies["radius_and_spacing_relaxation"]
    check("four broadened searches remain inside original bounds",
          all(v["within_original_limits"] for v in cap.values()), count=len(cap))
    check("four broadened searches reproduce continuous maximum to1e-8 SF",
          all(abs(v["SF_change_from_cap025"]) < 1e-8 for v in cap.values()))
    for filename in ("check_model.py", "check_studies.py", "check_sources.py", "assemble_check.py"):
        tree = ast.parse((ROOT / filename).read_text())
        imported = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
        imported |= {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        forbidden = {"floatpoint", "equilibrium", "gamma_local", "fold_pair", "sag_scan", "arcs", "nodes"}
        check(filename + " parses and imports no owner script", not imported.intersection(forbidden))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
