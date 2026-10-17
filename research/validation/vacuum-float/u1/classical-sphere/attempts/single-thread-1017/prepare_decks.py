#!/usr/bin/env python3
"""Regenerate frozen decks without invoking a solver; refuse a changed n24 model."""

import argparse
import importlib.util
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("original_sphere", args.runner)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    case_path = Path(__file__).with_name("case.json")
    case = json.loads(case_path.read_text())
    if runner.digest(args.runner) != case["original_runner_sha256"]:
        raise RuntimeError("The original runner source changed")
    if runner.digest(case_path) != "14d878014493c15b5ba16bd3903e35063ffef68f9df819af68208de945ecbf77":
        raise RuntimeError("The frozen follow-up case changed")
    root = runner.home_path(args.run_root)
    for key in ("TMPDIR", "TMP", "TEMP", "XDG_CACHE_HOME"):
        if not runner.home_path(os.environ[key]).is_relative_to(root):
            raise RuntimeError(f"{key} escapes the attempt root")
    controls = case["numerical_settings"]["thread_controls"]
    if any(os.environ.get(key) != value for key, value in controls.items()):
        raise RuntimeError("A supported thread control is not one")
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:8])
    record = {
        "started": runner.now(), "purpose": "mesh/deck generation only; zero solves",
        "case_path": str(case_path.resolve()), "case_sha256": runner.digest(case_path),
        "runner_path": str(args.runner.resolve()), "runner_sha256": runner.digest(args.runner),
        "preparer_path": str(Path(__file__).resolve()), "preparer_sha256": runner.digest(__file__),
        "envelope": runner.envelope(), "thread_environment": {k: os.environ[k] for k in controls},
        "cpu_affinity": sorted(os.sched_getaffinity(0)), "meshes": [], "status": "PREPARING",
    }
    receipt = root / "preparation.json"
    runner.save(receipt, record)
    try:
        for divisions in case["mesh_divisions"]:
            deck = root / "decks" / f"n{divisions}"
            deck.mkdir(parents=True, exist_ok=False)
            os.chdir(deck)
            mesh = runner.sphere_deck(case, divisions)
            runner.save("mesh-definition.json", mesh)
            record["meshes"].append({"divisions": divisions, "path": str(deck), **mesh})
            runner.save(receipt, record)
            if divisions == 24 and mesh["deck_sha256"] != case["required_n24_deck_sha256"]:
                raise RuntimeError("Regenerated n24 differs from the original physical deck; no solve permitted")
        record.update(status="READY", ended=runner.now(), solver_invocations=0,
                      n24_original_deck_match=True)
        runner.save(receipt, record)
    except Exception as error:
        record.update(status="BLOCKED", ended=runner.now(), error=str(error), solver_invocations=0)
        runner.save(receipt, record)
        raise
    print(json.dumps(record), flush=True)


if __name__ == "__main__":
    main()
