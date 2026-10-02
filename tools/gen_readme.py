#!/usr/bin/env python3
"""Regenerate the README's published model figures from generated records.

The records are checked against the live model by figfresh and cellparity. This
tool checks the README projection, including prose values, without a browser.
"""

import argparse
import json
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def record(path):
    return json.loads((ROOT / path).read_text())


def sections():
    figures = record("research/figures.json")
    sources = record("research/sources.json")
    classes = figures["classes"]
    names = ("P100", "P1000", "P10000")

    def row(label, get, unit=""):
        return "| " + label + " | " + " | ".join(
            f"{get(classes[name])}{unit}" for name in names
        ) + " |"

    def decimal(key, digits):
        return lambda cls: f"{cls['cycle'][key]:,.{digits}f}"

    headline = [
        f"| Model output, balanced mode, {figures['assumptions']['exampleKm']} km one way | P-100 | P-1000 | P-10000 |",
        "|---|---:|---:|---:|",
        row("Payload", lambda c: f"{c['spec']['payloadT']:,}", " t"),
        row("Hull length", lambda c: c["spec"]["lenM"], " m"),
        row("Cycle", decimal("cycleMin", 1), " min"),
        row("Water delivered", lambda c: f"{c['cycle']['tph']:,}", " t/h"),
        row("Descent anchor", lambda c: f"{c['descent']['anchorT']:,}", " t"),
        row("Retained ballast", lambda c: c["descent"]["retainedT"], " t"),
        row("Energy per cycle", decimal("eCycleMWh", 2), " MWh"),
        row("Energy per delivered tonne", decimal("kwhPerTonne", 2), " kWh/t"),
        "| What sets the cycle time | " + " | ".join(
            classes[name]["cycle"]["bottleneck"] for name in names
        ) + " |",
    ]
    example = classes["P10000"]["cycle"]
    changed_distance = json.loads(subprocess.check_output(
        ["node", "--input-type=module", "-e",
         "import {planCycle} from './sim/plan.js'; "
         "import {CLASSES, MODES} from './sim/config.js'; "
         "const c=planCycle(CLASSES.P10000, MODES.balanced, 45); "
         "console.log(JSON.stringify({tph:c.tph,cycleMin:c.cycleMin,eCycleMWh:c.eCycleMWh,kwhPerTonne:c.kwhPerTonne}));"],
        cwd=ROOT, text=True,
    ))
    first_screen = [
        f"Expected from the shipped defaults: **{example['tph']:,} t/h**, "
        f"**{example['cycleMin']:.1f} min/cycle**, "
        f"**{example['eCycleMWh']:.2f} MWh/cycle**, and "
        f"**{example['kwhPerTonne']:.2f} kWh/t**. These are model outputs, "
        "not observed aircraft performance.",
        f"Expected at 45 km from the shipped defaults: **{changed_distance['tph']:,.0f} t/h**, "
        f"**{changed_distance['cycleMin']:.1f} min/cycle**, "
        f"**{changed_distance['eCycleMWh']:.2f} MWh/cycle**, and "
        f"**{changed_distance['kwhPerTonne']:.2f} kWh/t**. This row is also a model output."
    ]
    return {
        "example": "\n".join("   " + line for line in first_screen),
        "headline": "\n".join(headline),
        "sources": f"The [source catalogue](research/sources.json) contains **{len(sources['sources'])} entries**.",
    }


def regenerate(readme):
    current = readme
    for name, body in sections().items():
        start = f"<!-- readme:{name}:start -->"
        end = f"<!-- readme:{name}:end -->"
        if current.count(start) != 1 or current.count(end) != 1:
            raise ValueError(f"Expected one pair of markers for {name}")
        before, rest = current.split(start, 1)
        _, after = rest.split(end, 1)
        indent = "   " if name == "example" else ""
        current = before + start + "\n" + body + "\n" + indent + end + after
    return current


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    args = parser.parse_args()
    try:
        original = args.readme.read_text()
        generated = regenerate(original)
    except (OSError, KeyError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"readmecheck: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if original != generated:
            print("readmecheck: README.md differs from generated model records", file=sys.stderr)
            return 1
        print("readmecheck: generated figures match README.md")
    else:
        args.readme.write_text(generated)
        print(f"readme: regenerated {args.readme.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
