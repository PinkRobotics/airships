#!/usr/bin/env python3
"""Point concept/index.html at sim/ as well, deleting the second copy of the model.

The how-it-works page carried its own byte-copy of the simulation, kept in step by a
copy-paste ritual that had already failed: at the time of the split the two differed by
sixteen lines. Both pages import the same modules now, so they cannot disagree.

The concept page needs a smaller slice of the model than the monitor does — it renders
worked examples and class cards, it does not fly anything — so it imports what it uses.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slice import read_region                                          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGE = ROOT / 'concept' / 'index.html'

IMPORT_BLOCK = '''/* ── the simulation ──────────────────────────────────────────────────────────────────
 *
 * This page used to carry its own copy of the model, kept in step with the monitor's copy
 * by hand. They had already drifted. Both pages import `sim/` now, so every figure below
 * is computed by the same code that flies the fleet on the monitor — if one is wrong,
 * both are wrong, which is the only honest arrangement.
 */
import {
  CFG, DEFAULTS, setConfig, resetConfig, CLASSES, CLASS_ORDER, MODES,
  ledger, planCycle, fmt, fmtHa, fmtMin, fmtT,
} from '../sim/index.js';
import * as SIM from '../sim/index.js';'''

CONSOLE_SURFACE = '''
/* Published so a reader can check any figure on this page in their own console:
 * `AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P1000, AIRSHIPS.sim.MODES.balanced, 15)`
 * recomputes the worked example from the same code that rendered it. */
window.AIRSHIPS = { sim: SIM };
'''


def main():
    lines, a, b = read_region(str(PAGE), '/*SIM*/', '/*/SIM*/')
    removed = b - a + 1
    lines = lines[:a] + IMPORT_BLOCK.split('\n') + lines[b + 1:]
    s = '\n'.join(lines)

    for opener in ('<script>\n"use strict";\n/* ── the simulation',
                   '<script>\n/* ── the simulation'):
        if s.count(opener) == 1:
            s = s.replace(opener, '<script type="module">\n/* ── the simulation')
            break
    else:
        sys.exit('rewire_concept: could not find the page script tag')

    # the page's sliders reassigned CFG wholesale; the model owns that now
    s = s.replace('CFG = Object.assign({}, DEFAULTS);', 'resetConfig();')
    s = s.replace('CFG[dd.k] = parseFloat(e.target.value);',
                  'setConfig({ [dd.k]: parseFloat(e.target.value) });')

    s = s.rstrip('\n')
    assert s.endswith('</script>\n</body>\n</html>') or '</script>' in s
    i = s.rindex('</script>')
    s = s[:i] + CONSOLE_SURFACE + s[i:] + '\n'

    PAGE.write_text(s)
    print(f"  concept/index.html: removed {removed} duplicated model lines, imports ../sim/")


if __name__ == '__main__':
    main()
