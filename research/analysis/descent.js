/* Read both energy bases from the current instantaneous ledger.
 * Bag removal and disabled bag credit are supplied-effort comparisons.
 * Neither comparison establishes a feasible flight or a delivery saving. */
(async () => {
  const S = window.AIRSHIPS.sim;
  const { CLASSES, CLASS_ORDER, MODES, CFG, PHASES, TERRAIN_MSL, BUS_CEILING, LETDOWN_FROM,
    PLAN_STEPS, planCycle, ledger, drawAt, integrateCycle, cycleGeometry, anchorGeometry } = S;
  const r = (x, n = 3) => (Number.isFinite(x) ? Number(x.toFixed(n)) : null);
  const G = 9.81;

  const out = { generated: { by: 'research/analysis/descent.js', worked: { oneWayKm: CFG.exampleKm, mode: 'balanced' } }, classes: {}, favourableClasses: {} };

  for (const basis of ['record','favourable'])for (const id of CLASS_ORDER) {
    const cls = CLASSES[id];
    const mode = MODES.balanced;
    const plan = planCycle(cls, mode, CFG.exampleKm,null,{basis});
    const g = cycleGeometry(cls, plan);
    const cableM = cls.anchorM || 0;
    const reachAglM = anchorGeometry(cableM, cls.diaM).contactAltitudeM; // hull-centre contact altitude

    /* THE PROFILE. The letdown is the last (1 - LETDOWN_FROM) of the return leg — the descent
       from the ceiling to the hold altitude — and the approach: close the track, stop, then sink
       onto the lake with the bag going in on the way. Sampled at every tenth of each. */
    const sample = (phase, prog) => {
      const d = drawAt(cls, mode, plan, phase, prog);
      return {
        phase, prog: r(prog, 2), aglM: r(d.alt, 0), gsKph: r(d.gs, 1), vzMps: r(d.vz, 2),
        surplusT: r(d.led.liftT - d.massT, 1), bagT: r(d.anchor.tonnes, 1),
        netAfterBagT: r(Math.max(0, d.led.liftT - d.massT - d.anchor.tonnes), 1),
        owners: d.owners, unheldT: d.unheldT, feasible: d.feasible, thrustT: r(d.thrustN / G / 1000, 1),
        askedMW: r(d.rotorAskMW, 1), rotorsMW: r(d.draw.rotors, 1), busMW: r(d.busMW, 1),
        clipped: d.rotorAskMW > d.draw.rotors * (1 + 1e-9),
      };
    };
    const profile = [];
    for (let i = 0; i <= 10; i++) profile.push(sample('RETURN_TRANSIT', LETDOWN_FROM + (1 - LETDOWN_FROM) * (i / 10) * 0.9999));
    for (let i = 0; i <= 10; i++) profile.push(sample('SOURCE_APPROACH', Math.min(0.9999, i / 10)));

    /* WHERE THE ROTORS STOP MANAGING ALONE. Scanned upward from the fill altitude, as plan.js
       does, with the honest bus: the surplus the empty hull has to be held down by, less the
       nitrogen aboard, against what the rotors hold at full share. */
    const rotorCapT = plan.rotorMaxT;
    let crossingAglM = null;                                   // null: the rotors manage all the way up
    for (let a = g.srcAlt; a <= 3000; a += 10) {
      if (ledger(cls, TERRAIN_MSL + a).surplusT - plan.ln2MakeT > rotorCapT) crossingAglM = a;
    }
    // A static crossing is only a diagnostic; the signed ledger decides feasibility.
    const bandNeitherM = crossingAglM === null ? 0 : Math.max(0, crossingAglM - reachAglM);

    // The same flown cycle with the rotors blind to the bag (#14, as it was), and the bare hull.
    const blind = integrateCycle(cls, mode, plan, PLAN_STEPS, { anchorCredit: false });
    const bare = planCycle({ ...cls, anchorBagT: 0 }, mode, CFG.exampleKm,null,{basis});
    const bareHoist = r(bare.anchorHoistMWh, 3);

    out[basis==='record'?'classes':'favourableClasses'][id] = {
      cableM, bagT: cls.anchorBagT || 0, reachAglM,
      bus: { battMW: cls.battMW, genMW: cls.genMW, descentBusMW: r(plan.busMW, 2), rotorShareOfBus: BUS_CEILING,
        rotorMaxT: r(plan.rotorMaxT, 1), rotorCapT: r(rotorCapT, 1), basis: plan.basis, feasible: plan.feasible },
      hold: { surplusAtSourceT: r(plan.ledLow.surplusT, 1), ln2MakeT: r(plan.ln2MakeT, 2),
        holdAtSourceT: r(plan.ledLow.surplusT - plan.ln2MakeT, 1), anchorT: r(plan.anchorT, 1),
        leftToRotorsT: r(plan.ledLow.surplusT - plan.ln2MakeT - plan.anchorT, 1),
        rotorsLeftDoingPctOfCapability: r(100 * (plan.ledLow.surplusT - plan.ln2MakeT - plan.anchorT) / rotorCapT, 1) },
      basis: plan.basis, feasible: plan.feasible, cycleMin:plan.cycleMin,worst:plan.worst,bindingLimits: plan.bindingLimits,
      geometry: { ceilingAglM: r(g.altTop, 0), holdAglM: r(g.holdAgl, 0), fillAglM: r(g.srcAlt, 0),
        anchorFromAglM: plan.anchorFromAglM, rotorsAloneFailBelowAglM: crossingAglM,
        bagInTheWaterBelowAglM: reachAglM, bandNeitherRotorsNorBagM: bandNeitherM,
        letdownMinutes: r(plan.dur.RETURN_TRANSIT * (1 - LETDOWN_FROM) + plan.dur.SOURCE_APPROACH, 2) },
      letdown: {
        mwh: r(plan.letdownMWh, 3), pctOfCycle: r(100 * plan.letdownMWh / plan.eCycleMWh, 1),
        peakRotorMW: r(plan.downMW, 1), peakPhase: plan.downMWPhase,
        battLimited: plan.battLimited, clippedMinutes: r(plan.letdownClipMin, 2), clippedMWh: r(plan.rotorClipMWh, 3),
        rotorsWholeCycleMWh: r(plan.Echan.rotors, 3), rotorsPctOfCycle: r(100 * plan.Echan.rotors / plan.eCycleMWh, 1),
      },
      cycle: { eCycleMWh: r(plan.eCycleMWh, 3), kwhPerTonne: r(plan.kwhPerTonne, 2), deliveredT: r(plan.deliveredT, 1), bottleneck: plan.bottleneck },
      // Supplied-effort comparisons on unsupported requested cycles.
      rotorsBlindToTheBag: { letdownMWh: r(blind.letdownMWh, 3), eCycleMWh: r(blind.eCycleMWh, 3), peakRotorMW: r(blind.downMW, 1),
        creditSavesMWh: r(blind.eCycleMWh - plan.eCycleMWh, 3), creditSavesPctOfCycle: r(100 * (blind.eCycleMWh - plan.eCycleMWh) / blind.eCycleMWh, 1) },
      withoutTheBag: { feasible:bare.feasible,cycleMin:bare.cycleMin,worst:bare.worst,retainedT: r(bare.retainedT, 1), deliveredT: r(bare.deliveredT, 1), eCycleMWh: r(bare.eCycleMWh, 3),
        kwhPerTonne: r(bare.kwhPerTonne, 2), letdownMWh: r(bare.letdownMWh, 3), bottleneck: bare.bottleneck, battLimited: bare.battLimited,
        anchorHoistMWh: bareHoist,
        bagBuysDeliveredT: r(plan.deliveredT - bare.deliveredT, 1),
        bagCostsCyclePct: r(100 * (plan.eCycleMWh - bare.eCycleMWh) / bare.eCycleMWh, 1),
        bagCostsPerTonnePct: r(100 * (plan.kwhPerTonne - bare.kwhPerTonne) / bare.kwhPerTonne, 1) },
      hoist: { mwh: r(plan.anchorHoistMWh, 3), formulaMgh: r(plan.anchorT * 1000 * G * 15 / 0.85 / 3.6e9, 3) },
      profile,
    };
  }
  return out;
})()
