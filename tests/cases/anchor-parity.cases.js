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
import { CLASSES, CLASS_ORDER } from '../../sim/index.js?v=2d8ae1c4';
import { anchorView } from '../../app/anchorview.js?v=2d8ae1c4';
import { fromMonitorState } from '../../3d/adapter/fable.js?v=7439a398';
import { resolveClass } from '../../3d/model/config.js?v=7439a398';

describe('the anchor reads the same in the model and in the avatar', () => {
  /* Compared END TO END: the avatar's rule against what the ADAPTER actually hands the 3D model,
   * over every phase and the whole altitude envelope. An earlier version of this file compared
   * only the approach, and missed that the avatar put a full bucket back on the cable through the
   * first 18% of the outbound leg — the ship climbing away from the lake with a bag it had
   * already dumped. Comparing one phase proves one phase. */
  const PHASES = ['SOURCE_APPROACH', 'WATER_FILL', 'OUTBOUND_TRANSIT', 'RETURN_TRANSIT',
    'WATER_RELEASE', 'BUOYANCY_ESCAPE'];

  for (const id of CLASS_ORDER) {
    it(`${id}: cable and bag agree in every phase, at every altitude`, () => {
      const host = CLASSES[id];              // the monitor's class record
      const viz = resolveClass(id);          // the 3D library's own copy
      // Both rules compute first contact from the PUBLISHED diameter, and spec-parity.cases.js
      // pins the two copies of it. They used to read different fields — a diameter here, a
      // derived max radius there — half a metre apart, which put the bag's fill a percent out.
      eq(viz.nominalDiameterM, host.diaM, 'the diameter the two files publish');
      let checked = 0;
      for (const phase of PHASES) {
        for (const prog of [0.02, 0.1, 0.17, 0.3, 0.5, 0.8, 0.96, 0.99]) {
          for (const gs of [0, 1.5, 8, 40]) for (let alt = 1200; alt >= 0; alt -= 120) {
            const model = fromMonitorState(
              { phase, prog, alt, gs, water: 0, ln2: 0, draw: {} }, host, viz,
              { anchorT: host.anchorBagT });
            const avatar = anchorView(host, alt, phase, prog, 1, gs);
            eq(avatar.cableP, model.anchorProgress,
              `${id} ${phase} @${prog} @${alt} m: cable out`);
            close(avatar.fillF, model.anchorFill, 1e-9,
              `${id} ${phase} @${prog} @${alt} m: bag fill`);
            checked++;
          }
        }
      }
      ok(checked > 500, `only ${checked} points compared`);
    });
  }

  it('the cable is stowed climbing away from the lake, load aboard', () => {
    // The specific flash this file was extended for. The first 18% of the outbound leg is still
    // over the water — the hose is winding up — but the bag went back into the lake during the
    // fill and must not reappear on the cable as the ship leaves.
    for (const id of CLASS_ORDER) {
      const host = CLASSES[id];
      for (const prog of [0.01, 0.05, 0.1, 0.17, 0.2]) {
        const v = anchorView(host, 300, 'OUTBOUND_TRANSIT', prog, 1);
        eq(v.cableP, 0, `${id}: cable out at outbound ${prog}`);
        eq(v.fillF, 0, `${id}: bag holding water at outbound ${prog}`);
      }
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
