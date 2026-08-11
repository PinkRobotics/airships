/* OPEN-QUESTIONS #3, #14 and #15: what does the descent actually cost?
 *
 * Three entries, one fact. `E.letdown = downMW * min(6, RETURN_TRANSIT * 0.2) / 60` prices the
 * whole descent at the ANCHOR-ASSISTED residual power, over a window set by two constants
 * (`6` and `0.2`) that are justified nowhere. But the bag is in the water only for the last
 * few hundred metres — the cable is 350 / 600 / 850 m — and above that the rotors are alone
 * against a surplus that grows as the air thickens. Meanwhile `stateAt` computes rotor power
 * with no anchor term at all and over-reads by ~33x at the moment the mechanism is working.
 * Neither model prices the descent, and they disagree by 20-30x in the phase the anchor was
 * invented for.
 *
 * This integrates it, in 10 m steps, from cruise to the fill altitude, using the model's own
 * `ledger` for the surplus at each altitude and its own `diskMW` for the power to hold it.
 * No new physics and no new constants: the only inputs are the model's.
 *
 *   make descent
 */
(async () => {
  const S = window.AIRSHIPS.sim;
  const { CLASSES, CLASS_ORDER, MODES, CFG, planCycle, ledger, diskMW,
    TERRAIN_MSL, ALT, VZ_MAX, sourceAltM } = S;

  const r = (x, n = 3) => (Number.isFinite(x) ? Number(x.toFixed(n)) : null);
  const STEP = 10;                          // m, the same step planCycle scans anchorFromAglM at

  // plan.js charges the rotors 0.6 of the force they are holding. The factor is undocumented
  // and it is carried here unchanged so that this integral and the ledger differ ONLY in how
  // they treat altitude and the anchor — one variable at a time.
  const THRUST_SHARE = 0.6;

  const out = { generated: { by: 'research/analysis/descent.js' }, classes: {} };

  for (const id of CLASS_ORDER) {
    const cls = CLASSES[id];
    const plan = planCycle(cls, MODES.balanced, CFG.exampleKm);
    const srcAgl = sourceAltM(cls);
    const cableM = cls.anchorM || 0;
    const bagT = cls.anchorBagT || 0;

    // The descent the ship actually flies: from cruise down to the fill altitude, at the
    // model's own climb/descent rate.
    const fromAgl = ALT.cruise, toAgl = srcAgl;
    const vz = VZ_MAX * MODES.balanced.climb;
    const profile = [];
    let eRotorOnly = 0, eWithAnchor = 0, peakAlone = 0, peakWith = 0;
    // Scanning DOWNWARD, so the first altitude at which the bus cannot supply the rotors is
    // the top of the band in which they fail — the ship cannot hold itself down BELOW it.
    let rotorsFailBelowAgl = null, anchorReachAgl = null;

    for (let a = fromAgl; a > toAgl; a -= STEP) {
      const led = ledger(cls, TERRAIN_MSL + a);
      const surplusT = led.surplusT;                       // empty hull, the letdown case
      // The bag can only help when the cable reaches the water.
      const reaches = a <= cableM;
      if (reaches && anchorReachAgl === null) anchorReachAgl = a;
      const heldByBag = reaches ? Math.min(bagT, surplusT) : 0;
      const residT = Math.max(0, surplusT - heldByBag);

      const mwAlone = diskMW(cls, surplusT * 1000 * 9.81 * THRUST_SHARE);
      const mwWith = diskMW(cls, residT * 1000 * 9.81 * THRUST_SHARE);
      const busMW = (cls.battMW + cls.genMW);
      if (mwAlone > busMW && rotorsFailBelowAgl === null) rotorsFailBelowAgl = a;

      const dt = STEP / vz / 3600;                          // hours
      eRotorOnly += mwAlone * dt;
      eWithAnchor += mwWith * dt;
      if (mwAlone > peakAlone) peakAlone = mwAlone;
      if (mwWith > peakWith) peakWith = mwWith;

      if (a % 250 === 0 || a === fromAgl)
        profile.push({ aglM: a, surplusT: r(surplusT, 1), bagT: r(heldByBag, 1),
                       residT: r(residT, 1), rotorAloneMW: r(mwAlone, 1),
                       withAnchorMW: r(mwWith, 2) });
    }

    const descentMin = (fromAgl - toAgl) / vz / 60;
    const ledgerWindowMin = Math.min(6, plan.dur.RETURN_TRANSIT * 0.2);

    out.classes[id] = {
      cableM, bagT, busMW: cls.battMW + cls.genMW,
      descentFromAglM: fromAgl, toAglM: toAgl, descentMinutes: r(descentMin, 2),
      anchorAvailableBelowAglM: anchorReachAgl,
      anchorAvailableForPctOfDescent:
        r(100 * (anchorReachAgl === null ? 0 : (anchorReachAgl - toAgl)) /
          (fromAgl - toAgl), 1),
      rotorsAloneFailBelowAglM: rotorsFailBelowAgl,
      anchorReachesBeforeRotorsFail:
        rotorsFailBelowAgl === null ? true : (anchorReachAgl >= rotorsFailBelowAgl),
      peakRotorAloneMW: r(peakAlone, 1),
      peakWithAnchorMW: r(peakWith, 2),
      integratedMWh: {
        rotorsAlone: r(eRotorOnly, 3),
        withAnchorWhereItReaches: r(eWithAnchor, 3),
        anchorSavingPct: r(100 * (1 - eWithAnchor / eRotorOnly), 1),
      },
      ledgerSays: {
        letdownMWh: r(plan.E.letdown, 3),
        downMW: r(plan.downMW, 2),
        windowMinutes: r(ledgerWindowMin, 2),
        // The two things #3 and #15 assert, now measured.
        understatementVsIntegral: r(eWithAnchor / Math.max(1e-9, plan.E.letdown), 1),
        windowVsActualDescent: r(ledgerWindowMin / descentMin, 2),
      },
      cycleContext: {
        eCycleMWh: r(plan.eCycleMWh, 3),
        honestLetdownPctOfCycle:
          r(100 * eWithAnchor / (plan.eCycleMWh - plan.E.letdown + eWithAnchor), 1),
      },
      profile,
    };
  }
  return out;
})()
