/* The two things that draw the descent anchor must agree about when it moves.
 *
 * `3d/anim/mission.js` → `anchorAt()` drives the WebGL model. `app/anchorview.js` → `anchorView()`
 * draws the schematic avatar beside it. They are separate implementations because the 3D library
 * imports nothing outside itself — a boundary the linter enforces — so neither can call the other
 * and the rule exists twice.
 *
 * That is exactly the arrangement that let the vehicle specification drift between its two copies
 * once already, and it drifted here within a day: the model was moved onto an altitude-derived
 * rule and the avatar was left on a hand-authored curve against phase progress, so the bucket
 * went down in one picture seconds before the other. This file is the same answer
 * `spec-parity.cases.js` gives — compare them, over the whole envelope, rather than trusting a
 * comment that says they match.
 */
import { close, describe, eq, it, ok } from '../harness.js';
import { CLASSES, CLASS_ORDER } from '../../sim/index.js?v=32eb46d5';
import { anchorView } from '../../app/anchorview.js?v=32eb46d5';
import { anchorAt } from '../../3d/anim/mission.js';
import { resolveClass } from '../../3d/model/config.js';

describe('the anchor reads the same in the model and in the avatar', () => {
  for (const id of CLASS_ORDER) {
    it(`${id}: cable and bag agree at every altitude`, () => {
      const host = CLASSES[id];              // the monitor's class record
      const viz = resolveClass(id);          // the 3D library's own copy
      // Both rules read the PUBLISHED diameter, and spec-parity.cases.js pins the two copies of
      // it to each other. They used to read different fields — a diameter here, a derived max
      // radius there — which put the bag's fill a percent apart and is what this file caught.
      eq(viz.nominalDiameterM, host.diaM, 'the diameter the two files publish');
      for (let alt = 1200; alt >= 0; alt -= 10) {
        const a = anchorAt(viz, alt, 1);
        const b = anchorView(host, alt, 'SOURCE_APPROACH', 0.5, 1);
        eq(b.cableP, a.anchorProgress, `${id} @${alt} m: cable out`);
        close(b.fillF, a.anchorFill, 1e-9, `${id} @${alt} m: bag fill`);
      }
    });
  }

  it('the cable is stowed everywhere the ship is not over water', () => {
    // The avatar has phases the model's own eleven-phase cycle does not, so this half of the
    // rule has no counterpart to compare against and is asserted directly.
    for (const id of CLASS_ORDER) {
      const host = CLASSES[id];
      for (const phase of ['OUTBOUND_TRANSIT', 'WATER_RELEASE', 'BUOYANCY_ESCAPE']) {
        const v = anchorView(host, 300, phase, 0.5, 1);
        eq(v.cableP, phase === 'OUTBOUND_TRANSIT' ? 0 : 0, `${id} ${phase}: cable out`);
        eq(v.fillF, 0, `${id} ${phase}: bag holding water`);
      }
      // The return leg only counts as over-water in its last few per cent, where the ship is a
      // few hundred metres out and braking.
      eq(anchorView(host, 800, 'RETURN_TRANSIT', 0.5, 1).cableP, 0, `${id}: mid-leg`);
    }
  });

  it('the bag empties and the cable comes in during the fill, on schedule not on altitude', () => {
    // The ship is stationary at this point; the trigger is the tanks passing what the descent
    // needed, which is a time, not a height. Both files therefore special-case WATER_FILL, and
    // they have to special-case it the same way.
    const host = CLASSES.P10000;
    const early = anchorView(host, 300, 'WATER_FILL', 0.02, 1);
    const late = anchorView(host, 300, 'WATER_FILL', 0.70, 1);
    ok(early.fillF > 0.9, `the bag should still be full at the start of the fill: ${early.fillF}`);
    eq(late.fillF, 0, 'and empty well before the end');
    eq(late.cableP, 0, 'with the cable stowed');
  });
});
