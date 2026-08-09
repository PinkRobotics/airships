/* The simulation, as one import.
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
