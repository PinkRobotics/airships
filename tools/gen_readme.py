#!/usr/bin/env python3
"""Regenerate the README's published model figures from generated records.

The records are checked by energydoccheck, figfresh and cellparity. This
tool checks the README projection, including prose values, without a browser.
tools/gen_readme.py also emits the current README for exact-region verification.
"""

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def record(path):
    return json.loads((ROOT / path).read_text())


def sections():
    figures = record("research/figures.json")
    sources = record("research/sources.json")
    energy = record("research/analysis/energy-documents.json")
    names = ("P100", "P1000", "P10000")
    classes = {r["class"]: r for r in energy["classes"]}
    km = figures["assumptions"]["exampleKm"]
    cycles = {(r["class"], r["basis"]): r["asDrawn"]
              for r in energy["records"] if r["km"] == km}

    def row(label, get):
        return "| " + label + " | " + " | ".join(get(name) for name in names) + " |"

    def paired(name, field, digits=3):
        return " / ".join(f"{cycles[name, basis][field]:.{digits}f}"
                          for basis in ("record", "favourable"))

    headline = [
        f"| Prescribed balanced profile at {km} km | P100 | P1000 | P10000 |",
        "|---|---:|---:|---:|",
        row("Force verdict", lambda n: " / ".join(
            "closes" if cycles[n, b]["feasible"] else "does not close"
            for b in ("record", "favourable"))),
        row("Hull length, m", lambda n: str(classes[n]["lengthM"])),
        row("Minutes", lambda n: f"{cycles[n, 'record']['cycleMin']:.1f}"),
        row("Requested payload, t", lambda n: f"{cycles[n, 'record']['deliveredT']:g}"),
        row("Water kept, t", lambda n: f"{cycles[n, 'record']['ballastT']:g}"),
        row("Supplied MWh: record / favourable", lambda n: paired(n, "cycleMWh")),
        row("kWh per planned tonne: record / favourable", lambda n: paired(n, "kwhPerTonne")),
        row("Worst unheld t: record / favourable", lambda n: " / ".join(
            f"{cycles[n, b]['worst']['unheldT']:.3f}" for b in ("record", "favourable"))),
    ]
    first_screen = []
    examples = energy["readmeExamples"]
    distances = list(dict.fromkeys(r["km"] for r in examples))
    for distance in distances:
        rec, fav = (next(r for r in examples if r["km"] == distance and r["basis"] == b)
                    for b in ("record", "favourable"))
        verdict = "closes" if rec["feasible"] else "does not close on the drawn hardware"
        first_screen.extend([
            f"At {distance} km, the prescribed P-10000 cycle takes **{rec['cycleMin']:.1f} minutes** and {verdict}.",
            f"Its supplied effort is **{rec['cycleMWh']:.2f} MWh/cycle** on record and **{fav['cycleMWh']:.2f} MWh/cycle** on favourable.",
            f"The corresponding **{rec['kwhPerTonne']:.2f} / {fav['kwhPerTonne']:.2f} kWh per planned tonne** do not establish delivered water.",
        ])
    example_input = [
        "2. **Reproduce and move a number (about one minute; Node only).**",
        "   This example uses balanced mode and a one-way distance in kilometres.",
        "   It prints both energy bases and the force verdict, without a feed request.",
        "",
        "   ```sh",
        "   node --input-type=module -e \"import {planCycle,CLASSES,MODES} from './sim/index.js'; "
        f"for(const km of {json.dumps(distances)}) for(const basis of ['record','favourable']) "
        "{ const p=planCycle(CLASSES.P10000,MODES.balanced,km,null,{basis}); "
        "console.log(km,basis,p.feasible,p.cycleMin,p.eCycleMWh,p.kwhPerTonne,p.worst); }\"",
        "   ```",
        "",
        "   The columns are distance, basis, force verdict, minutes, supplied MWh, kWh per planned tonne, and the worst unheld force.",
        "   An infeasible row establishes no delivery or endurance.",
        "   The example and table use `energy-documents.json`; `make energydoccheck` compares that record with the model.",
    ]
    energy_intro = [
        "This table describes prescribed cycles under the model defaults. The force ledger and energy integrals now share one calculation.",
        "All rows below are unsupported prescribed profiles; their requested mass and supplied effort are not achieved delivery.",
        "The P-100 is the reference class. Nobody is proposing to build a P-10000.",
    ]
    energy_reading = [
        "The prescribed profiles leave force unheld in several phases, including stationary fill on the larger classes.",
        "The [generated tables](docs/ENERGY-CLOSURE-2026-10.md) show the cheapest feasible profiles found in the stated space, their retained water and their minutes.",
        "The independent [payload-exchange study](research/analysis/payload-exchange.md) is analysis, not design.",
    ]
    energy_method = [
        "`sim/config.js` names the assumptions. `sim/plan.js` times the cycle; `sim/power.js` owns force limits and integrated power.",
        "`sim/requirements.js` searches the stated profiles. Run `make energycheck energydoccheck figfresh` to check the energy records and documents.",
        "Run `make readmecheck` to compare this page with those records; regenerate it with `python3 tools/gen_readme.py`.",
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
    spec = importlib.util.spec_from_file_location('cell', ROOT / 'research/analysis/vacuum-cell.py')
    cell = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cell)
    float_example = ['```text']
    for sf in (1.2, 1.5):
        result = cell.ship0('s1050', sf=sf, basis='record')
        float_example.append(
            f"SF {sf:.1f}: mass {result['totalT']:.3f} t; lift {result['liftSLT']:.3f} t; "
            f"lift/mass {result['ratioSL']:.3f} sea level, {result['ratio2500']:.3f} at 2500 m; "
            f"sizing checks {result['checksPass']}")
    float_example.append('```')
    return {
        "float-example": "\n".join(float_example),
        "energy-input": "\n".join(example_input),
        "energy-intro": "\n".join(energy_intro),
        "energy-reading": "\n".join(energy_reading),
        "energy-method": "\n".join(energy_method),
        "energy-budget-context": "The mass budget's cycle-energy context follows the figure cache. Its battery sizing does not establish feasible endurance.",
        "float": "\n".join("   " + line for line in float_lines),
        "example": "\n".join("   " + line for line in first_screen),
        "headline": "\n".join(headline),
        "sources": f"The [source catalogue](research/sources.json) contains **{len(sources['sources'])} entries**.",
    }


def regenerate(readme):
    current = readme
    current = current.replace('The cycle-energy context still comes from the earlier flight model.', '<!-- readme:energy-budget-context:start -->\n<!-- readme:energy-budget-context:end -->')
    # Introduce generator boundaries around the earlier energy prose once.
    spans = {
        "energy-input": ("2. **Reproduce and move a number", "   <!-- readme:example:start -->"),
        "energy-intro": ("This table describes the simulated cycle", "<!-- readme:headline:start -->"),
        "energy-reading": ("The table names the limit on cycle time", "## Where to inspect the calculation"),
        "energy-method": ("[`sim/config.js`](sim/config.js) names", "For a pinned browser run"),
    }
    for name, (first, last) in spans.items():
        if f"<!-- readme:{name}:start -->" not in current:
            a, b = current.index(first), current.index(last)
            current = current[:a] + f"<!-- readme:{name}:start -->\n<!-- readme:{name}:end -->\n\n" + current[b:]
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
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    args = parser.parse_args()
    try:
        original = args.readme.read_text()
        generated = regenerate(original)
    except (OSError, KeyError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"readmecheck: {exc}", file=sys.stderr)
        return 1
    if args.emit:
        print(json.dumps({'README.md': generated}))
    elif args.check:
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
