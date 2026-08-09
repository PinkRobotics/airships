#!/usr/bin/env python3
"""Point index.html at sim/ instead of carrying the model inline.

Four edits, each asserted so the script fails loudly rather than half-applying:

  1. the /*SIM*/ … /*/SIM*/ region becomes an import of `sim/index.js`;
  2. the page's script becomes `type="module"` so it can import at all;
  3. the community list, now a model input, stops being declared here too;
  4. `window.APP` gains `window.AIRSHIPS`, so that a reader can run the model in
     their own devtools console on the page they are reading.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slice import read_region                                          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGE = ROOT / 'index.html'

IMPORT_BLOCK = '''/* ── the simulation ──────────────────────────────────────────────────────────────────
 *
 * The model used to live here, inline, which meant the how-it-works page carried a
 * byte-identical copy of it and the two drifted apart. It is `sim/` now, imported by
 * both pages, and `sim/index.js` says what is in each file.
 */
import {
  DEFAULTS, CFG, resetConfig, CLASSES, CLASS_ORDER, HULL_NAMES, MODES, PHASES, PHASE_TINT,
  setSeed, bez, havKm, ledger, pumpMW, planCycle, findSource, insideFire, dropSeg,
  planTargets, segAt, legKmFor, deliveryPoint, buildMission, stateAt, narrate, srcName,
  fmt, fmtHa, fmtMin, fmtT, selftest, CITIES,
} from './sim/index.js';
import * as SIM from './sim/index.js';

/* Deterministic replay: `?seed=N` pins every choice the model makes. The URL is read
 * here, in the page, so that nothing in sim/ needs to know a browser exists. */
{
  const seed = new URLSearchParams(location.search).get('seed');
  if (seed) setSeed(seed);
}'''

CONSOLE_SURFACE = '''
/* The page is an ES module, so nothing it declares is global. These two are published
 * deliberately. `APP` because the markup binds to it. `AIRSHIPS` so that anyone reading
 * the page can run the model themselves without cloning anything: `AIRSHIPS.sim
 * .selftest()` re-runs every assertion in the browser they are already using, and
 * `AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P100, AIRSHIPS.sim.MODES.balanced, 15)`
 * recomputes a published figure from scratch. Publishing arithmetic that cannot be
 * re-run is just a claim. */
window.AIRSHIPS = { sim: SIM, app: S, stateAt };
'''


def main():
    lines, a, b = read_region(str(PAGE), '/*SIM*/', '/*/SIM*/')
    lines = lines[:a] + IMPORT_BLOCK.split('\n') + lines[b + 1:]
    s = '\n'.join(lines)

    old_script = '<script>\n/* ── the simulation'
    if s.count(old_script) != 1:
        # the model region is preceded by a "use strict" line in the original
        old_script = '<script>\n"use strict";\n/* ── the simulation'
        assert s.count(old_script) == 1, 'could not find the application script tag'
        s = s.replace(old_script, '<script type="module">\n/* ── the simulation')
    else:
        s = s.replace(old_script, '<script type="module">\n/* ── the simulation')

    # the community list moved into the model; the page must not declare it as well
    lines = s.split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith('const CITIES = ['))
    j = next(k for k in range(i, len(lines)) if lines[k].rstrip().endswith('];'))
    start = i
    while start - 1 >= 0 and lines[start - 1].lstrip().startswith(('/*', '*', '//')):
        start -= 1
    del lines[start:j + 1]
    s = '\n'.join(lines)

    boot = 'document.addEventListener("visibilitychange", () => { S.lastFrame = null; });\nboot();'
    assert s.count(boot) == 1, 'could not find the boot call'
    s = s.replace(boot, boot.replace('\nboot();', '\n' + CONSOLE_SURFACE + '\nboot();'))

    PAGE.write_text(s)
    print(f"  index.html: model region ({b - a + 1} lines) -> import, script -> module, "
          f"CITIES de-duplicated, console surface published")


if __name__ == '__main__':
    main()
