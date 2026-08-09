#!/usr/bin/env python3
"""Move the simulation out of index.html into sim/*.js, byte for byte.

Every function body is copied verbatim from its source lines; the only text this
script writes is the `export` keyword and the import header. That is deliberate:
a reorganisation that retypes code cannot be checked by reading, but one that
only moves it can.
"""
from __future__ import annotations
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slice import read_region, top_level_symbols

ROOT = pathlib.Path(__file__).resolve().parents[2]

# Which symbol lives in which module. Order inside a module follows the source.
MODULES = {
    'config':      ['DEFAULTS', 'CFG', 'CLASSES', 'HULL_NAMES', 'CLASS_ORDER', 'MODES',
                    'ALT', 'ALT_DROP_TOP', 'VZ_MAX', 'PHASES', 'PHASE_TINT'],
    'rng':         ['SEED', 'hashFrac'],
    'geo':         ['R_EARTH', 'havKm', 'moveToward', 'bez', 'bezBearing',
                    'easeTrap', 'easeSm', 'lerpAng', 'trackBearing'],
    'physics':     ['pumpMW', 'dragMW', 'diskMW', 'ledger'],
    'plan':        ['planCycle'],
    'water':       ['findSource', 'intakePoint'],
    'targets':     ['insideFire', 'dropSeg', 'planTargets', 'tIdx', 'segAt', 'legKmFor',
                    'stationFor', 'deliveryPoint', 'arrivalCurve'],
    'assign':      ['sizeTier', 'assign'],
    'format':      ['fmt', 'fmtHa', 'fmtMin', 'fmtT'],
    'mission':     ['buildMission'],
    'state':       ['stateAt'],
    'narrate':     ['narrate', 'srcName'],
    'selftest':    ['selftest'],
}

HEADERS = {
    'config': 'Every tunable number and every vehicle assumption, in one file.\n *\n * Nothing here is measured. These are the assumptions the whole model rests on, which\n * is why they live together where they can be read in one sitting and argued with as a\n * set. `CFG` holds the live values; the page\'s sliders write to it and `resetConfig()`\n * puts it back.',
    'rng': 'Deterministic pseudo-randomness.\n *\n * The plan order and the drop-line placement vary between visits so the demonstration\n * does not replay one identical attack forever. Pinning the seed makes a run\n * reproducible, which is what lets one person hand another an exact scenario and what\n * the golden-output tests compare against. The seed is set by the page, never read from\n * the URL here: this module knows nothing about browsers.',
    'geo': 'Geometry, distance and easing. Pure functions of their arguments.',
    'physics': 'The four first-order physical relations the whole model is built on.\n *\n * Each is one equation with its units stated. If the project is wrong about how much\n * energy it takes to move water through the sky, it is wrong in one of these four\n * functions, so they are kept together, short, and separately testable.',
    'plan': 'planCycle: the function that produces every number the site publishes.\n *\n * Given a vehicle class, an operating mode, a distance and a wind, it returns the\n * duration of each phase of a delivery cycle, the energy that cycle costs, how much\n * water arrives, and which constraint is binding. Pure: same inputs, same outputs.',
    'water': 'Choosing where to draw water, and where over that water to hover.',
    'targets': 'Choosing where the water goes: candidate drop lines across a fire, scored and sequenced.',
    'assign': 'Which class of ship a fire gets, and why.',
    'format': 'Number and unit formatting (en-CA). Presentation, but shared by the model\'s prose.',
    'mission': 'Assembling one mission: a fire, a water source, a plan and a set of drop lines.',
    'state': 'stateAt: where a mission is and what it is doing at a given moment in its cycle.\n *\n * The phase state machine. Everything the map draws, the instruments read and the 3D\n * model animates comes from this one function, so that no two surfaces can disagree\n * about what the ship is doing.',
    'narrate': 'The mission trace in prose: last, now, next, plan.',
    'selftest': 'Assertions the model must satisfy, runnable in a browser console on the live page.\n *\n * These are shipped, not just tested in CI, so that a reader who does not trust the\n * numbers can run the checks themselves in devtools on the page they are reading.',
}


def main():
    src = ROOT / 'index.html'
    lines, a, b = read_region(str(src), '/*SIM*/', '/*/SIM*/')
    syms = {n: (i, s, e) for n, i, s, e in top_level_symbols(lines, a, b)}

    placed = {n: mod for mod, names in MODULES.items() for n in names}
    missing = sorted(set(syms) - set(placed))
    extra = sorted(set(placed) - set(syms))
    if missing or extra:
        print(f"MAPPING ERROR  unplaced={missing}  unknown={extra}"); sys.exit(1)

    bodies, owners = {}, {}
    for mod, names in MODULES.items():
        chunks = []
        for n in names:
            i, s, e = syms[n]
            block = lines[s:e]
            k = i - s                                  # the declaration line inside the block
            block[k] = 'export ' + block[k]
            chunks.append('\n'.join(block).rstrip())
            owners[n] = mod
        bodies[mod] = '\n\n'.join(chunks)

    outdir = ROOT / 'sim'; outdir.mkdir(exist_ok=True)
    strip = re.compile(r'//[^\n]*|/\*.*?\*/', re.S)
    for mod, body in bodies.items():
        # `...spread(x)` puts a dot before an identifier that is NOT a property access,
        # so neutralise the operator before the reference scan or the import is missed.
        scan = strip.sub(' ', body).replace('...', ' ')
        needs = {}
        for name, own in owners.items():
            if own == mod:
                continue
            # not preceded by a dot: `Object.assign` is not a reference to our `assign`
            if re.search(r'(?<![.\w$])' + re.escape(name) + r'\b', scan):
                needs.setdefault(own, []).append(name)
        imports = ''.join(
            f"import {{ {', '.join(sorted(v))} }} from './{k}.js';\n"
            for k, v in sorted(needs.items()))
        head = f"/* {HEADERS[mod]}\n */\n"
        (outdir / f'{mod}.js').write_text(head + (imports + '\n' if imports else '') + body + '\n')
        print(f"  sim/{mod}.js  {len(body.splitlines()):4d} lines  imports: "
              f"{', '.join(sorted(needs)) or 'none'}")


if __name__ == '__main__':
    main()
