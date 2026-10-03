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
    TERRAIN_MSL, WORK_ALT_MSL, sourceAltM, ALT, BUS_CEILING, energySummary } = S;
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
    const solarMW = c.solarM2 * CFG.solarWPerM2 / 1e6;
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
        // The bus the closure is struck against is the battery plus what the nitrogen store
        // returns during the approach (plan.busMW), never the generators' nameplate; the
        // rotors get BUS_CEILING of it and hold rotorMaxT at full share, SHARE_MAX.
        busMW: r(p.busMW, 2), rotorMaxT: r(p.rotorMaxT, 1),
        rotorCapT: r(p.rotorMaxT, 1),
        holdAtSourceT: r(ledSrc.surplusT - p.ln2MakeT, 1),
        anchorT: r(p.anchorT, 1), retainedT: r(p.retainedT, 1),
        anchorFromAglM: p.anchorFromAglM,
        anchorPullMN: r(p.anchorT * 1000 * 9.81 / 1e6, 1),
        battLimited: p.battLimited,
        // Where the bus clamp held the rotors below what the choreography asked for: minutes
        // over the cycle, minutes inside the letdown (which is what battLimited reports), MWh.
        rotorClipMin: r(p.rotorClipMin, 2), letdownClipMin: r(p.letdownClipMin, 2),
        rotorClipMWh: r(p.rotorClipMWh, 3),
      },
      bases: Object.fromEntries(["record", "favourable"].map(basis => [basis, energySummary(c, planCycle(c, MODES.balanced, CFG.exampleKm, null, {basis}))])),
      cycle: {
        basis: p.basis, feasible: p.feasible, bindingLimits: p.bindingLimits, worst: p.worst,
        cycleMin: r(p.cycleMin, 2), deliveredT: r(p.deliveredT, 1), tph: r(p.tph, 0),
        dropsPerHour: r(p.dropsPerHour, 2), passes: p.passes,
        eCycleMWh: r(p.eCycleMWh, 3), kwhPerTonne: r(p.kwhPerTonne, 2),
        bottleneck: p.bottleneck,
        durations: Object.fromEntries(Object.entries(p.dur).map(([k, v]) => [k, r(v, 2)])),
      },
      energy: {
        basis: p.basis, feasible: p.feasible, meaning: p.feasible ? "modelled cycle" : "INFEASIBLE: supplied effort only",
        pumpMW: r(p.pumpMW, 2), dragMW: r(p.dragMW, 2),
        // The rotors' peak draw over the cycle and the phase it falls in. Until 2026-10-01 this
        // was the anchor-assisted hold-down power at the fill altitude (0.3 / 5.0 / 52.3 MW);
        // it is now the largest instantaneous rotor draw of the flown cycle, which falls in the
        // approach, where the ship lets itself down onto the lake before the bag is in.
        downMW: r(p.downMW, 1), downMWPhase: p.downMWPhase,
        solarMW: r(solarMW, 2), solarPerCycleMWh: r(solarMW * p.cycleMin / 60, 2),
        deficitPerCycleMWh: r(p.eCycleMWh - solarMW * p.cycleMin / 60, 2),
        ln2MakeT: r(p.ln2MakeT, 2), eBackMWh: r(p.eBack, 3),
        // The per-phase ledger, so a report can cite the budget table line by line instead of
        // transcribing it. docs/PHYSICS.md §9 went 5% stale in its total and 24x adrift from
        // its own §11 precisely because it was transcribed. Since 2026-10-01 the ledger is the
        // integral of the flown cycle: six phases plus the nitrogen recovery (summing to
        // eCycleMWh), and the same energy by channel (summing to eCycleMWh + eBackMWh). The old
        // `letdown`, `anchor` and `other` lines are gone; the letdown and the hoist are read out
        // of the integral below.
        ledgerMWh: Object.fromEntries(Object.entries(p.E).map(([k, v]) => [k, r(v, 3)])),
        ledgerByChannelMWh: Object.fromEntries(Object.entries(p.Echan).map(([k, v]) => [k, r(v, 3)])),
        // Rotor energy over the letdown (the return leg's descent to the hold altitude and the
        // approach onto the lake), and the winch energy of hoisting the bag clear of the water.
        letdownMWh: r(p.letdownMWh, 3), letdownPctOfCycle: r(100 * p.letdownMWh / p.eCycleMWh, 1),
        anchorHoistMWh: r(p.anchorHoistMWh, 3),
        rotorsPctOfCycle: r(100 * p.Echan.rotors / p.eCycleMWh, 1),
        // Endurance, which the deficit implies but nobody was computing in one place.
        cyclesOnBattery: r(c.battMWh / Math.max(1e-9, p.eCycleMWh - solarMW * p.cycleMin / 60), 1),
        hoursOnBattery: r(c.battMWh / Math.max(1e-9, p.eCycleMWh - solarMW * p.cycleMin / 60)
                          * p.cycleMin / 60, 1),
      },
    };
  }
  /* SENSITIVITY, generated rather than transcribed. docs/PHYSICS.md §10 published this table
   * by hand and it went stale twice — once when the descent moved to the source and once when
   * the anchor took the letdown out. Each constant is moved ±20% from its default and the
   * P-10000's cycle energy is re-measured at the worked distance. `resetConfig()` after every
   * probe, or the next one measures the last one's mistake. */
  const base = planCycle(CLASSES.P10000, MODES.balanced, CFG.exampleKm);
  const pct = (a, b) => (b === 0 ? 0 : r(((a - b) / b) * 100, 1));
  const sens = {};
  for (const k of ['propEta', 'Cd', 'rhoAir', 'pumpEta', 'hoseMul', 'rhoSL', 'rtLN2', 'eLN2',
                   'solarWPerM2']) {
    const row = {};
    for (const [side, mul] of [['lo', 0.8], ['hi', 1.2]]) {
      S.resetConfig();
      S.setConfig({ [k]: S.DEFAULTS[k] * mul });
      row[side] = pct(planCycle(CLASSES.P10000, MODES.balanced, CFG.exampleKm).eCycleMWh,
                      base.eCycleMWh);
    }
    S.resetConfig();
    sens[k] = row;
  }
  // Class parameters are not in CFG, so they move on a copy of the class rather than a dial.
  for (const k of ['cruiseKph', 'anchorBagT', 'fillM3s', 'dispM3', 'diskM2', 'battMW', 'solarM2']) {
    const row = {};
    for (const [side, mul] of [['lo', 0.8], ['hi', 1.2]]) {
      const mod = Object.assign({}, CLASSES.P10000);
      mod[k] = CLASSES.P10000[k] * mul;
      row[side] = pct(planCycle(mod, MODES.balanced, CFG.exampleKm).eCycleMWh, base.eCycleMWh);
    }
    sens[k] = row;
  }
  // The one-way TRANSIT distance, which is planCycle's third argument. This was labelled
  // `dropKm` and published in two PDFs under a caption reading "every constant moved ±20%" —
  // but dropKm is the length of the release line (sim/plan.js), a different quantity that this
  // sweep never touched. Nothing checks a label, so a generated chart carried a wrong one.
  {
    const row = {};
    for (const [side, mul] of [['lo', 0.8], ['hi', 1.2]]) {
      row[side] = pct(planCycle(CLASSES.P10000, MODES.balanced, CFG.exampleKm * mul).eCycleMWh,
                      base.eCycleMWh);
    }
    sens.oneWayKm = row;
  }
  // And dropKm itself, which had never been measured.
  {
    const row = {};
    for (const [side, mul] of [['lo', 0.8], ['hi', 1.2]]) {
      const mod = Object.assign({}, CLASSES.P10000);
      mod.dropKm = CLASSES.P10000.dropKm * mul;
      row[side] = pct(planCycle(mod, MODES.balanced, CFG.exampleKm).eCycleMWh, base.eCycleMWh);
    }
    sens.dropKm = row;
  }
  out.sensitivity = sens;

  return JSON.stringify(out, null, 2);
})()
