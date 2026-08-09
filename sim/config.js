/* Every tunable number and every vehicle assumption, in one file.
 *
 * Nothing here is measured. These are the assumptions the whole model rests on, which
 * is why they live together where they can be read in one sitting and argued with as a
 * set. `CFG` holds the live values; the page's sliders write to it and `resetConfig()`
 * puts it back.
 */
/* ============================================================================================
 * The demonstration model. Everything the monitor shows is computed here, from these numbers.
 * Nothing in this block touches the DOM, so it can be loaded standalone and self-tested
 * (append ?selftest=1 to the page URL; results go to the console).
 *
 * Units: SI internally — kg, m, s, N, W — surfaced as tonnes, km, minutes, MW, MWh.
 * One tonne of water is one cubic metre. All vehicle numbers are DEMONSTRATION ASSUMPTIONS.
 * ============================================================================================ */

export const DEFAULTS = {
  eLN2: 0.45,      // kWh per kg to liquefy nitrogen from air (demonstration assumption)
  rtLN2: 0.50,     // electrical round-trip efficiency of the nitrogen store
  hoseHead: 250,   // m of vertical pumping head at the source
  pumpEta: 0.75,   // pump + hose + electrical efficiency, all-in
  propEta: 0.70,   // propulsive efficiency applied to drag and disk power
  Cd: 0.05,        // hull drag coefficient (streamlined body of revolution)
  rhoAir: 1.10,    // kg/m3 in the working band (~1000 m)
  rhoSL: 1.225,    // kg/m3 sea level — sets the buoyancy ledger
  speedMul: 1.0,   // dial: airspeed multiplier
  fillMul: 1.0,    // dial: fill-rate multiplier
  cryoMul: 1.0,    // dial: cryogenic capacity multiplier
  exampleKm: 15,   // dial: worked-example one-way distance
};

/**
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
}

export const CLASSES = {
  P100: {
    id: "P100", name: "P-100", payloadT: 100, dispM3: 180000, lenM: 177, diaM: 44,
    cruiseKph: 90, fillM3s: 0.5, hoseDeployMin: 4, hoseRetractMin: 3,
    genMW: 8, battMWh: 20, battMW: 30, cryoMW: 6, solarM2: 6000, diskM2: 2500, rotors: 4, ln2CapT: 50,
    minSourceHa: 10, searchKm: 25, dropKm: 1.2, use: "Initial attack and small incidents close to water",
  },
  P1000: {
    id: "P1000", name: "P-1000", payloadT: 1000, dispM3: 1.8e6, lenM: 380, diaM: 95,
    cruiseKph: 110, fillM3s: 3, hoseDeployMin: 6, hoseRetractMin: 5,
    genMW: 40, battMWh: 120, battMW: 150, cryoMW: 30, solarM2: 28000, diskM2: 12000, rotors: 6, ln2CapT: 500,
    minSourceHa: 100, searchKm: 100, dropKm: 2.5, use: "Sustained delivery on project fires and fires of note",
  },
  P10000: {
    id: "P10000", name: "P-10000", payloadT: 10000, dispM3: 1.8e7, lenM: 820, diaM: 205,
    cruiseKph: 130, fillM3s: 15, hoseDeployMin: 10, hoseRetractMin: 8,
    // diskM2 and battMW are sized so the force balance closes with NOTHING held back:
    // after a full 10,000 t dump the hull is ~12,000 t buoyant, and 14 big discs on a
    // battery-surge bus must push all of it back down to the water. Brute force, chosen
    // deliberately over retaining water as descent ballast — every drop empties the tanks.
    genMW: 150, battMWh: 2000, battMW: 1400, cryoMW: 100, solarM2: 120000, diskM2: 160000, rotors: 14, ln2CapT: 5000,
    minSourceHa: 1000, searchKm: 600, dropKm: 5, use: "Campaign fires, long hauls, and moving water between regions",
  },
};

/* Hull names. Water birds, grouped so the name alone gives the class: the P-100s are divers
   that take fish one at a time, the P-1000s are the big scoopers, and the single P-10000 is
   named for the largest wingspan alive. Order is fixed — a hull keeps its name across the
   15-minute live-data rebuilds, which is also what keys its energy ledger. */
export const HULL_NAMES = {
  P100: ["Kingfisher", "Tern", "Merganser", "Dipper", "Grebe",
         "Loon", "Swift", "Petrel", "Kestrel", "Auklet"],
  P1000: ["Osprey", "Pelican", "Heron", "Albatross", "Skimmer"],
  P10000: ["Condor"],
};

export const CLASS_ORDER = ["P100", "P1000", "P10000"];

export const MODES = {
  rapid:     { id: "rapid", label: "Rapid response", speed: 1.15, hose: 0.85, climb: 1.4, cryoShare: 0.4, fixed: 0.8 },
  balanced:  { id: "balanced", label: "Balanced", speed: 1.0, hose: 1.0, climb: 1.0, cryoShare: 0.7, fixed: 1.0 },
  endurance: { id: "endurance", label: "Endurance", speed: 0.8, hose: 1.15, climb: 0.7, cryoShare: 1.0, fixed: 1.2 },
};

/* Working altitudes, metres above ground.
 *
 * `source` is set by the HOSE, not by choice: the pump lifts water CFG.hoseHead (250 m), so the
 * ship hangs just above that over the lake. `drop` used to be lower than the pickup, which had
 * the ship flying its most dangerous minutes closer to the ground than its calmest ones. It is
 * a fire: the column is turbulent, the terrain is not flat, and an 820 m hull cannot manoeuvre
 * out of a surprise. 450 m puts the P-10000's keel ~350 m over the canopy, above the worst of
 * the fire's own air, and gives the drop the fall it needs to arrive as rain instead of a column.
 */
export const ALT = { cruise: 1500, source: 300, drop: 450 };

/* The release ends 130 m higher than it began — the hull is already rising off the line as the
 * last of the water goes. The escape has to START there, or the ship teleports at the seam. */
export const ALT_DROP_TOP = ALT.drop + 130;

/* Comfortable climb/descent rate, m/s. Buoyancy could do better; a hull this size choosing to
 * is another matter, and it is what keeps short legs from flying impossible vertical profiles. */
export const VZ_MAX = 6;

/* Six phases, and the hose work never gets its own stopped time: the pod pays out during
   the flown final approach, the site itself is pure pumping, and the hose winds up inside
   the climb-out that starts the outbound leg. The dial shows the concurrent work as a
   sub-activity under the phase name — two things at once, honestly labelled. */
export const PHASES = [
  ["SOURCE_APPROACH", "final approach — hose paying out"],
  ["WATER_FILL", "pump water aboard"],
  ["OUTBOUND_TRANSIT", "climb out, hose up — transit to the fire"],
  ["WATER_RELEASE", "drop run along the fire"],
  ["BUOYANCY_ESCAPE", "escape climb on surplus buoyancy"],
  ["RETURN_TRANSIT", "return — make ballast, descend to hose range"],
];

export const PHASE_TINT = {
  SOURCE_APPROACH: "#47637d", WATER_FILL: "#7aa2c8",
  OUTBOUND_TRANSIT: "#9a9aa5", WATER_RELEASE: "#ff4fa3",
  BUOYANCY_ESCAPE: "#8c2a58", RETURN_TRANSIT: "#9a9aa5",
};

/* ---------- geometry ------------------------------------------------------------------- */
