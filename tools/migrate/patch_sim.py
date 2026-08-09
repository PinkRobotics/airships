#!/usr/bin/env python3
"""The hand-written seams of the simulation extraction.

`extract_sim.py` moves code; this file writes the few lines that could not simply be
moved, because they were entangled with the page:

  * the seed was read from the URL inside the model — the page injects it now;
  * the config object was reassigned wholesale — it is one object with a setter now;
  * `planTargets` read live satellite heat off a global — it is an argument now;
  * the community list the drop planner scores against was in the page's map code,
    although it is a physical input, so it moves into the model.

Keeping these edits in a script rather than doing them by hand means the whole
extraction can be re-run from the original file and audited as a single mechanism.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SIM = ROOT / 'sim'


PUBLIC_API = """/* The simulation, as one import.
 *
 * WHAT THIS IS. A first-order model of a fleet of water-carrying airships working real
 * wildfires: how long a delivery cycle takes, how much water arrives, what that costs in
 * energy, and where a ship is at any moment of its cycle. Every number the site
 * publishes comes out of these files and nowhere else.
 *
 * WHAT IT IS NOT. It is not a design, and it is validated against no built vehicle,
 * because no such vehicle exists. It is arithmetic on stated assumptions. The assumptions
 * are all in `config.js`; the four relations everything rests on are in `physics.js`. If
 * a number here is wrong, it is wrong in a file you can read in an afternoon — which is
 * the entire reason the model is separated out like this.
 *
 * RULES THIS DIRECTORY KEEPS. No DOM, no network, no wall clock, no `location`, no
 * globals. Every function is a function of its arguments plus `CFG`. So the model runs
 * unchanged in a browser, in node and in a test, and any part of it can be executed
 * alone.
 *
 * WHERE TO START. `plan.js` for the published figures. `state.js` for what the ships are
 * doing. `config.js` for what we assumed.
 */

export {
  DEFAULTS, CFG, setConfig, resetConfig,
  CLASSES, CLASS_ORDER, HULL_NAMES, MODES, ALT, ALT_DROP_TOP, VZ_MAX, PHASES, PHASE_TINT,
} from './config.js';

export { SEED, setSeed, hashFrac } from './rng.js';

export {
  R_EARTH, havKm, moveToward, bez, bezBearing, easeTrap, easeSm, lerpAng, trackBearing,
} from './geo.js';

export { pumpMW, dragMW, diskMW, ledger } from './physics.js';
export { planCycle } from './plan.js';
export { findSource, intakePoint } from './water.js';
export { CITIES } from './communities.js';

export {
  insideFire, dropSeg, planTargets, tIdx, segAt, legKmFor, stationFor, deliveryPoint,
  arrivalCurve,
} from './targets.js';

export { sizeTier, assign } from './assign.js';
export { fmt, fmtHa, fmtMin, fmtT } from './format.js';
export { buildMission } from './mission.js';
export { stateAt } from './state.js';
export { narrate, srcName } from './narrate.js';
export { selftest } from './selftest.js';
"""

def sub(path, old, new, count=1):
    p = SIM / path if not str(path).startswith('/') else pathlib.Path(path)
    s = p.read_text()
    if s.count(old) != count:
        sys.exit(f"patch_sim: {path}: expected {count} occurrence(s) of {old[:60]!r}, found {s.count(old)}")
    p.write_text(s.replace(old, new))


# ── the seed is injected, not read from a URL ────────────────────────────────────────
s = (SIM / 'rng.js').read_text()
banner_end = s.index(' */\n') + 4
tail = s[s.index('export function hashFrac'):]
(SIM / 'rng.js').write_text(s[:banner_end] + '''
/** The current seed. Pinned by `setSeed`; otherwise a fresh one per page load. */
export let SEED = String(Math.floor(Math.random() * 1e9));

/**
 * Pin the seed, making every downstream choice reproducible.
 *
 * Call this before building any mission — the seed is read when plans are made, not when
 * this module loads. The page passes `?seed=` here; nothing in `sim/` reads a URL itself,
 * so the model stays runnable outside a browser.
 */
export function setSeed(seed) {
  SEED = String(seed);
}

''' + tail)

# ── one config object for its whole life ─────────────────────────────────────────────
sub('config.js', 'export let CFG = Object.assign({}, DEFAULTS);', '''/**
 * The live values, as the sliders on the page have left them.
 *
 * One object for the lifetime of the module — never reassigned — so that everything
 * holding a reference sees the same numbers. Change it through `setConfig` and
 * `resetConfig` rather than by hand, or the page's sliders and the model disagree.
 */
export const CFG = Object.assign({}, DEFAULTS);

/** Overwrite one or more tunables. Unknown keys throw: a typo should not be silent. */
export function setConfig(patch) {
  for (const [k, v] of Object.entries(patch)) {
    if (!(k in DEFAULTS)) throw new Error(`setConfig: unknown key "${k}"`);
    CFG[k] = v;
  }
}

/** Put every tunable back to its documented default. */
export function resetConfig() {
  Object.assign(CFG, DEFAULTS);
}''')

sub('selftest.js', '  CFG = Object.assign({}, DEFAULTS);', '  resetConfig();')
sub('selftest.js', "import { CFG, CLASSES, CLASS_ORDER, DEFAULTS, MODES } from './config.js';",
    "import { CFG, CLASSES, CLASS_ORDER, DEFAULTS, MODES, resetConfig } from './config.js';")

# ── live satellite heat is an argument, not a global ─────────────────────────────────
sub('targets.js', 'export function planTargets(m) {', '''/**
 * Choose and order the drop lines for one mission.
 *
 * @param {object} m     the mission, mutated in place with `targets`, `segs` and `order`
 * @param {Array}  heat  satellite hotspots `{ll, temp}`; empty means fall back to geometry
 *
 * `heat` is passed in rather than read from a global because it is live external data:
 * the model has to be runnable, and testable, with no feed at all.
 */
export function planTargets(m, heat = []) {''')
sub('targets.js', 'm.heat && S.heat.length', 'm.heat && heat.length')
sub('targets.js', 'of S.heat', 'of heat')
sub('targets.js', "import { SEED, hashFrac } from './rng.js';",
    "import { SEED, hashFrac } from './rng.js';\nimport { CITIES } from './communities.js';")

sub('mission.js', 'export function buildMission(fire, water, modeId, forceClsId, forceSrc) {',
    'export function buildMission(fire, water, modeId, forceClsId, forceSrc, heat = []) {')
sub('mission.js', '  planTargets(m);', '  planTargets(m, heat);')

# ── the community list moves out of the page's map code and into the model ───────────
# read from the page as it still stands: rewire_page.py removes this block afterwards
page = (ROOT / 'index.html').read_text().split('\n')
a = next(i for i, l in enumerate(page) if l.startswith('const CITIES = ['))
b = next(i for i in range(a, len(page)) if page[i].rstrip().endswith('];'))
(SIM / 'communities.js').write_text("""/* Populated places, as an input to the model rather than as map decoration.
 *
 * A drop line is scored partly on which way its smoke and water would drift relative to
 * people, so this list is a physical input to `targets.js`, not a label layer — which is
 * why it lives with the model and is versioned alongside the code that reads it.
 *
 * Each entry is [longitude, latitude, name, tier]; tier 1 is a city, 2 a town. The set is
 * hand-picked for the interior fire belt and is not exhaustive: a community that is not
 * in this list is not considered at all, which is a limitation of the model rather than
 * an oversight in the data.
 */
""" + '\n'.join(page[a:b + 1]).replace('const CITIES', 'export const CITIES', 1) + '\n')

# ── the public surface ───────────────────────────────────────────────────────────────
(SIM / 'index.js').write_text(PUBLIC_API)

print("  seams patched: setSeed, config setter, targets(heat), mission(heat); "
      "wrote communities.js and index.js")
