/* How the descent anchor READS, for the two things that draw it.
 *
 * The 3D model and the schematic avatar have to show the same cable at the same moment. They are
 * drawn by different code in different languages of geometry — one is a catenary in a WebGL scene,
 * the other is a line on a 2D canvas — and the one thing they must not disagree about is WHEN.
 * They did: the model was moved to derive the anchor from altitude and the avatar was left on a
 * hand-authored curve against phase progress, so the bucket went down in one of them several
 * seconds before the other. An avatar that disagrees with the model is worse than no avatar.
 *
 * This is the app's copy of the rule in `3d/anim/mission.js` → `anchorAt()`. It is a copy because
 * the 3D library imports nothing outside itself, by design and by lint rule, so it cannot read the
 * monitor's model and the monitor cannot make it. `tests/cases/anchor-parity.cases.js` compares
 * the two across the whole altitude envelope, which is the same treatment the two copies of the
 * vehicle specification get in `spec-parity.cases.js`.
 */

const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);

/**
 * @param {object} cls   the monitor's class record (CLASSES[id])
 * @param {number} altM  height above the water, metres
 * @param {string} phase the monitor's phase id
 * @param {number} prog  0..1 within that phase
 * @param {number} fullF what a full bag means for this mission — plan.anchorT over the bag
 * @returns {{cableP: number, fillF: number}} cable payout and bag fill, both 0..1
 */
export function anchorView(cls, altM, phase, prog, fullF, gsKph = 0) {
  const cable = cls.anchorM || 0;
  if (cable <= 0) return { cableP: 0, fillF: 0 };

  // The fill dumps and the cable comes back in on a schedule, not on an altitude: the ship is
  // sitting still at this point and the trigger is the tanks passing what the descent needed.
  if (phase === "WATER_FILL") {
    return {
      cableP: 1 - clamp01((prog - 0.25) / 0.35),
      fillF: fullF * (1 - clamp01(prog / 0.30)),
    };
  }

  /* Everywhere else it is the water's distance that decides, exactly as in anchorAt(): the hull
   * radius appears because the winch is on the keel, one radius below the point `alt` refers to.
   *
   * OUTBOUND_TRANSIT is deliberately NOT in this list even though its first 18% is still over the
   * lake — the hose is winding up there and the water line is drawn, but the anchor was stowed
   * before the fill ended. Deriving it from altitude there put a full bucket back on the cable as
   * the ship climbed away with its load, which is the flash that was reported "showing down when
   * transitioning to outbound". Being over water is not the same question as needing the anchor.
   */
  const overLake = phase === "SOURCE_APPROACH"
    || (phase === "RETURN_TRANSIT" && prog > 0.94);
  if (!overLake) return { cableP: 0, fillF: 0 };
  // NOT WHILE MOVING — the same 2 m/s gate the model applies. A bag dipped at speed is the
  // objection that put the stop into the flight profile in the first place.
  if (gsKph / 3.6 > 2) return { cableP: 0, fillF: 0 };
  const reachAlt = Math.max(0, cable - cls.diaM / 2);
  if (altM > reachAlt + cable * 0.25) return { cableP: 0, fillF: 0 };
  return {
    cableP: 1,
    fillF: fullF * clamp01((reachAlt - altM) / Math.max(1, cable * 0.14)),
  };
}
