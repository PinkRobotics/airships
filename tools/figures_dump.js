/* Every figure the reports quote, computed from the model itself.
 *
 * The reports must not carry hand-copied numbers: this project has moved almost every published
 * figure several times in a day, and a report is exactly the artefact that goes stale silently.
 * `make factsheet` regenerates research/figures.json from the live model, the reports cite it by
 * key, and tools/check_figures.py fails if a report quotes a number the model does not produce.
 */
(() => {
  const S = window.AIRSHIPS.sim;
  const { CLASSES, CLASS_ORDER, MODES, CFG, planCycle, ledger, airDensity,
    TERRAIN_MSL, WORK_ALT_MSL, sourceAltM, ALT } = S;
  const r = (x, n = 3) => (Number.isFinite(x) ? Number(x.toFixed(n)) : null);

  const out = {
    generated: { by: 'tools/figures_dump.js via make factsheet', seed: 'model defaults' },
    assumptions: {},
    atmosphere: {
      terrainMslM: TERRAIN_MSL, workAltMslM: WORK_ALT_MSL,
      rhoAtWorkAlt: r(airDensity(WORK_ALT_MSL), 6),
      rhoAtGround: r(airDensity(TERRAIN_MSL), 6),
      rhoSeaLevel: r(airDensity(0), 6),
    },
    classes: {},
    worked: { oneWayKm: CFG.exampleKm, mode: 'balanced' },
  };
  for (const k of Object.keys(CFG)) out.assumptions[k] = CFG[k];

  for (const id of CLASS_ORDER) {
    const c = CLASSES[id];
    const p = planCycle(c, MODES.balanced, CFG.exampleKm);
    const ledWork = ledger(c, WORK_ALT_MSL);
    const ledSrc = ledger(c, TERRAIN_MSL + sourceAltM(c));
    const ledGround = ledger(c, TERRAIN_MSL);
    const solarMW = c.solarM2 * 200 / 1e6;
    out.classes[id] = {
      spec: {
        payloadT: c.payloadT, dispM3: c.dispM3, lenM: c.lenM, diaM: c.diaM,
        cruiseKph: c.cruiseKph, fillM3s: c.fillM3s, hoseM: c.hoseM,
        anchorCableM: c.anchorM, anchorBagT: c.anchorBagT,
        genMW: c.genMW, battMWh: c.battMWh, battMW: c.battMW, cryoMW: c.cryoMW,
        ln2CapT: c.ln2CapT, solarM2: c.solarM2, diskM2: c.diskM2, rotors: c.rotors, dropKm: c.dropKm,
      },
      lift: {
        atWorkAltT: r(ledWork.liftT, 1), atSourceT: r(ledSrc.liftT, 1),
        atGroundT: r(ledGround.liftT, 1),
        loadedMassT: r(ledWork.dryT + c.payloadT, 1),
        floatUpMarginPct: r(100 * (ledWork.liftT / (ledWork.dryT + c.payloadT) - 1), 2),
        surplusAtWorkAltT: r(ledWork.surplusT, 1), surplusAtSourceT: r(ledSrc.surplusT, 1),
        ln2ToSinkEmptyAtGroundT: r(ledGround.surplusT, 1),
      },
      descent: {
        rotorCapT: r(p.rotorMaxT / 0.6, 1),
        holdAtSourceT: r(ledSrc.surplusT - p.ln2MakeT, 1),
        anchorT: r(p.anchorT, 1), retainedT: r(p.retainedT, 1),
        anchorFromAglM: p.anchorFromAglM,
        anchorPullMN: r(p.anchorT * 1000 * 9.81 / 1e6, 1),
        battLimited: p.battLimited,
      },
      cycle: {
        cycleMin: r(p.cycleMin, 2), deliveredT: r(p.deliveredT, 1), tph: r(p.tph, 0),
        dropsPerHour: r(p.dropsPerHour, 2), passes: p.passes,
        eCycleMWh: r(p.eCycleMWh, 3), kwhPerTonne: r(p.kwhPerTonne, 2),
        bottleneck: p.bottleneck,
        durations: Object.fromEntries(Object.entries(p.dur).map(([k, v]) => [k, r(v, 2)])),
      },
      energy: {
        pumpMW: r(p.pumpMW, 2), dragMW: r(p.dragMW, 2), downMW: r(p.downMW, 1),
        solarMW: r(solarMW, 2), solarPerCycleMWh: r(solarMW * p.cycleMin / 60, 2),
        deficitPerCycleMWh: r(p.eCycleMWh - solarMW * p.cycleMin / 60, 2),
        ln2MakeT: r(p.ln2MakeT, 2), eBackMWh: r(p.eBack, 3),
        // The per-phase ledger, so a report can cite the budget table line by line instead of
        // transcribing it. docs/PHYSICS.md §9 went 5% stale in its total and 24x adrift from
        // its own §11 precisely because it was transcribed.
        ledgerMWh: Object.fromEntries(Object.entries(p.E).map(([k, v]) => [k, r(v, 3)])),
        // Endurance, which the deficit implies but nobody was computing in one place.
        cyclesOnBattery: r(c.battMWh / Math.max(1e-9, p.eCycleMWh - solarMW * p.cycleMin / 60), 1),
        hoursOnBattery: r(c.battMWh / Math.max(1e-9, p.eCycleMWh - solarMW * p.cycleMin / 60)
                          * p.cycleMin / 60, 1),
      },
    };
  }
  return JSON.stringify(out, null, 2);
})()
