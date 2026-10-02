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
    ledger = record("research/analysis/float-ledger.json")
    caps = record("research/analysis/cap-readings.json")
    census = record("research/analysis/member-census.json")
    cases = {r['id']: r for d in ledger['designs'] for r in d['cases']}
    rec = cases['hull-52m/as-drawn/gamma-0.30/chord-1050/sf-1.2']
    fav = cases['hull-52m/as-drawn/gamma-0.65/chord-1450/sf-1.2']
    rb, fb = census['basis']['record'], census['basis']['favourable']
    altitude = ledger['atmosphere']['targetM']
    ranges = caps['ranges']['favourable']
    float_lines = [
        f"**{ledger['verdict']}**",
        f"Both bases use structural safety factor {rec['safetyFactor']['value']:g} against full sea-level pressure.",
        f"The record basis assumes knockdown {rb['knockdown']:.2f} and {rb['chordAllowableMPa']:,.0f} MPa chords.",
        f"Its {rec['extras']['hullDiameterM']:g} m hull’s lift is {rec['at']['seaLevel']['liftToMass']:.3f} of its mass at sea level and {rec['at']['target']['liftToMass']:.3f} at {altitude:,} m.",
        f"The favourable basis assumes knockdown {fb['knockdown']:.2f} and a {fb['chordAllowableMPa']:,.0f} MPa carbon-laminate ceiling, both unverified.",
        f"Its lift-to-mass ratio is {fav['at']['seaLevel']['liftToMass']:.3f} at sea level and {fav['at']['target']['liftToMass']:.3f} at {altitude:,} m.",
        f"The bill and the drawing disagree in {census['disagreementCount']} places.",
        f"Across {len(caps['readings'])} readings of the end caps, the favourable ratio runs from {ranges['seaLevel']['min']:.3f} to {ranges['seaLevel']['max']:.3f} at sea level and from {ranges['target']['min']:.3f} to {ranges['target']['max']:.3f} at {altitude:,} m.",
        "No reading reaches 1." if caps['noneReachesOne'] else "At least one arithmetic reading reaches 1; that does not establish a checked design.",
        "The [float ledger](docs/FLOAT-LEDGER.md) gives every case and what would have to be true to close it.",
    ]
    return {
        "float": "\n".join("   " + line for line in float_lines),
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
        indent = "   " if name in ("example", "float") else ""
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
