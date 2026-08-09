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
  hoseMul: 1,      // scales every class's hose; the LENGTH is per class, see CLASSES[*].hoseM
  pumpEta: 0.75,   // pump + hose + electrical efficiency, all-in
  propEta: 0.70,   // propulsive efficiency applied to drag and disk power
  Cd: 0.05,        // hull drag coefficient (streamlined body of revolution)
  // Drag and every rotor calculation still use one fixed density. 1.10 kg/m3 is ISA at
  // about 990 m MSL, and the working altitude is 2,500 m (below), where the air is
  // 0.957 kg/m3. So drag is overstated by 15% and induced power understated by 7%. Both
  // are the power model's to fix, not the ledger's: see docs/PHYSICS.md Defect 2.
  rhoAir: 1.10,    // kg/m3, a fixed working-band density for drag and disk power
  // The sea-level ANCHOR of the density profile, not the density anything is weighed in.
  // sim/atmosphere.js scales the ISA column from it, so moving this dial moves the air at
  // every altitude — a hotter or colder day — rather than lying about where the ship flies.
  rhoSL: 1.225,    // kg/m3, ISA sea level
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

/* Working altitudes, metres above ground.
 *
 * There is no `source` here any more. The altitude a ship fills from is set by the HOSE it
 * carries, the hose length is a property of the class, and `sourceAltM()` below is the one
 * place that answers the question. See CLASSES[*].hoseM for why the lengths are what they are.
 *
 * `drop` used to be lower than the pickup, which had the ship flying its most dangerous
 * minutes closer to the ground than its calmest ones. It is a fire: the column is turbulent,
 * the terrain is not flat, and an 876 m hull cannot manoeuvre out of a surprise. 450 m puts
 * the P-10000's keel ~350 m over the canopy, above the worst of the fire's own air, and gives
 * the drop the fall it needs to arrive as rain instead of a column.
 */
export const ALT = { cruise: 1500, drop: 450 };

/* How high a class hovers while it fills, in metres above the water.
 *
 * The hose length IS the fill altitude and IS the pumping head — one number, because they are
 * one distance, and keeping them as two invited them to disagree (they did: a 250 m head under
 * a ship hovering at 300 m).
 */
export function sourceAltM(cls) {
  return cls.hoseM * CFG.hoseMul;
}

/* THE GROUND UNDER ALL OF THAT, and the altitude the buoyancy ledger is evaluated at.
 *
 * Every other altitude in this file is above ground. Buoyancy is not: it answers to the air
 * the hull is sitting in, and a kilometre of British Columbia is underneath. These two
 * constants are the bridge between the two, and they are the reason the hulls below are the
 * size they are.
 *
 * TERRAIN_MSL — one reference elevation for the ground the fleet works over. An assumption,
 * and a deliberately coarse one: the southern interior plateau runs about 900–1,400 m, and
 * the model carries a single figure for the lake and the fire alike rather than pretending
 * to know the ground under each. A ship recovering onto a valley floor is lower and needs
 * more ballast to reach it; that limit is stated with the nitrogen tankage below.
 *
 * WORK_ALT_MSL — the ceiling of ALT.cruise over that plateau. It is the WORST case in the
 * cycle: every other point a ship reaches is lower, in denser air, with more lift. Sizing
 * here therefore sizes for everywhere.
 *
 * THE TERRAIN ENVELOPE, because "1,500 m above ground" is a profile, not a clearance claim.
 * The fires that matter in the interior burn between the valley floors — Okanagan and
 * Thompson, 300–500 m — and treeline, about 2,100 m in the southern interior. Local summits
 * inside that fuel belt reach roughly 2,320 m at Big White. A 2,500 m MSL ceiling clears the
 * fuel everywhere in the belt and the highest ground in it by about 180 m. Flying lower was
 * permitted as relief from the hull growth below and is not taken: it buys a smaller
 * envelope by putting the largest aircraft ever proposed under the ridgelines it is working.
 */
export const TERRAIN_MSL = 1000;                       // m, interior plateau reference
export const WORK_ALT_MSL = TERRAIN_MSL + ALT.cruise;  // m, 2,500 — where the hulls are sized

/* The release ends 130 m higher than it began — the hull is already rising off the line as the
 * last of the water goes. The escape has to START there, or the ship teleports at the seam. */
export const ALT_DROP_TOP = ALT.drop + 130;

/* Comfortable climb/descent rate, m/s. Buoyancy could do better; a hull this size choosing to
 * is another matter, and it is what keeps short legs from flying impossible vertical profiles. */
export const VZ_MAX = 6;

/* The three vehicles.
 *
 * FAIL-SAFE FLOAT-UP SETS THE DISPLACEMENT. A hull must be positively buoyant at
 * WORK_ALT_MSL while fully loaded with water AND UNABLE TO DROP IT. A ship whose outlets
 * jam must rise, not sink. That is a safety property, so it sets the size of the envelope
 * and nothing else is allowed to trade it away.
 *
 * The arithmetic, per tonne of payload, is the same for all three because dry mass is set
 * equal to payload: loaded mass is 2 t, air at 2,500 m is 0.95686 kg/m3 (sim/atmosphere.js),
 * and a 5% margin wants 2.1 t of displaced air, which is 2,194.7 m3. Published: 2,200 m3 per
 * tonne, giving a margin of 5.25% — 210.5 t of lift against 200 t of loaded ship on a P-100.
 * That is +22.2% on the displacement these hulls used to carry, when the ledger bought its
 * lift at sea level and spent it at altitude.
 *
 * Nitrogen is NOT in that mass, and the omission is the doctrine: LN2 ballast vents to
 * atmosphere in seconds, so it is never the load a ship is stuck with. Water is.
 *
 * WHAT GREW AND WHAT DID NOT. Displacement, length and diameter grew; the dry allowance did
 * not, because it is still one tonne of vehicle per tonne of water. So the vacuum shell now
 * has 14% more area to cover with the same mass, and the implied areal density falls from
 * 5.07 / 10.94 / 23.50 to 4.43 / 9.58 / 20.59 kg/m2. Frontal area grew with it, so cruise
 * drag is up 14% on every class. Fail-safe float-up is bought by making the hardest unsolved
 * problem in the project harder and paying more to fly, and that price is the honest one.
 *
 * `ln2CapT` IS SIZED BY UNPOWERED RECOVERY, not by the cycle. A dead ship floats up; it must
 * be able to make itself heavy enough to come back down and land with no rotor authority at
 * all. The binding case is the BOTTOM of that descent, not the top: at TERRAIN_MSL the air
 * is 16% denser than at the ceiling, and an empty hull's surplus buoyancy there is 144.6 t
 * per 100 t of payload against 110.5 t at 2,500 m. Ballast sized for the ceiling stalls the
 * ship at about 2,065 m and never lands it. The tanks hold 1.55 payloads, 7.2% over the
 * ground figure. A recovery onto a valley floor at 350 m would need 160.6 t per 100 t and is
 * outside what the tanks hold: a dead ship must be brought down over high ground.
 *
 * `hoseM` — the hose that fetches the water, and the altitude the ship fills from. One number,
 * because it is one distance: the pump lifts water exactly as far as the ship is hanging above
 * it. 300 m on every class. It was briefly 1,100 and 1,350 m on the larger two, as a way of
 * keeping them out of the dense air near the water — that worked and cost 29 MWh a cycle in
 * pump work against a 2 m bore and 140 bar at the pod. The anchor below does the same job for
 * 0.04 MWh, so the hoses went back to being hoses.
 *
 * `anchorM`, `anchorBagT` — THE DESCENT ANCHOR, which is how a buoyant ship gets down.
 *
 * The problem: a hull sized to float up while fully loaded is very hard to push down when
 * empty, and hardest of all at the bottom, where the air is densest. At 300 m over the water a
 * P-10000 has 13,744 t of surplus lift and its rotors can hold down 12,666 t. It is 1,056 t
 * short of being able to arrive.
 *
 * The answer is not to carry ballast, make ballast, or keep water back. It is to borrow the
 * lake. The ship lowers a cable with a bag on it, fills the bag, and winches it just clear of
 * the surface: 1,056 m3 of water hanging on a line is 1,056 t of downward force that costs
 * only the few metres of lift needed to break the surface. When the tanks have taken on more
 * than the shortfall, the bag is dumped back where it came from. Nothing is carried away, and
 * nothing is manufactured.
 *
 * It is a Bambi bucket — the collapsible helicopter bucket the industry has used since 1983 —
 * at a scale nobody has built. Commercial ones top out near 10 tonnes. This is 1,200. The
 * principle is unchanged and the engineering is not, which is the honest way to describe it.
 *
 * `anchorM` is the cable, and it is shorter than it looks like it should be: the rotors can
 * hold the hull down unaided until the air thickens, which is 760 m above the water for a
 * P-10000 and 510 m for a P-1000, so the cable only has to reach the surface from there. 850
 * and 600 m with margin. The P-100 carries none — its descent closes with x1.94 headroom.
 *
 * `anchorBagT` is sized GENEROUSLY, and deliberately. The bare shortfall is 1,056 t on a
 * P-10000, and a bag that size leaves the rotors at 100% of their authority for the whole
 * letdown — which is not a margin, and costs power besides. Rotor thrust is expensive and the
 * lake is free, so the bag covers enough that the rotors work at no more than 90%: 2,400 t on
 * the P-10000, 200 t on the P-1000. The extra cable that buys is 195 mm and 25 t.
 *
 * A cable is a far better thing to hang than a pipe. 1,056 t is 10.4 MN; in steel wire that is
 * a 163 mm rope massing 216 t, and in UHMWPE (Dyneema and kin) it is 128 mm and about 11 t.
 * Synthetic rope is what makes this idea cheap, exactly as it did for deep-tow oceanography.
 *
 * NOT MODELLED, and material: 1,056 t swinging on one cable under an 876 m hull is a pendulum
 * nobody here has analysed, the bag has to survive being filled and dumped every cycle, and
 * the winch is assumed to run at 5 m/s in both directions. See docs/OPEN-QUESTIONS.md.
 */
export const CLASSES = {  P100: {
    id: "P100", name: "P-100", payloadT: 100, dispM3: 220000, lenM: 190, diaM: 47,
    cruiseKph: 90, fillM3s: 0.5, hoseDeployMin: 4, hoseRetractMin: 3, hoseM: 300,
    anchorM: 0, anchorBagT: 0,
    genMW: 8, battMWh: 20, battMW: 30, cryoMW: 6, solarM2: 6000, diskM2: 2500, rotors: 4, ln2CapT: 155,
    minSourceHa: 10, searchKm: 25, dropKm: 1.2, use: "Initial attack and small incidents close to water",
  },
  P1000: {
    id: "P1000", name: "P-1000", payloadT: 1000, dispM3: 2.2e6, lenM: 404, diaM: 102,
    cruiseKph: 110, fillM3s: 3, hoseDeployMin: 6, hoseRetractMin: 5, hoseM: 300,
    anchorM: 600, anchorBagT: 200,
    genMW: 40, battMWh: 120, battMW: 150, cryoMW: 30, solarM2: 28000, diskM2: 12000, rotors: 6, ln2CapT: 1550,
    minSourceHa: 100, searchKm: 100, dropKm: 2.5, use: "Sustained delivery on project fires and fires of note",
  },
  P10000: {
    id: "P10000", name: "P-10000", payloadT: 10000, dispM3: 2.2e7, lenM: 876, diaM: 219,
    cruiseKph: 130, fillM3s: 15, hoseDeployMin: 10, hoseRetractMin: 8, hoseM: 300,
    anchorM: 850, anchorBagT: 2400,
    // diskM2 and battMW are sized so the force balance closes with NOTHING held back:
    // after a full 10,000 t dump the hull is 11,051 t buoyant at its working altitude, and
    // 14 big discs on a battery-surge bus must push all of it back down to the water. Brute
    // force, chosen deliberately over retaining water as descent ballast — every drop empties
    // the tanks. Honest density made this EASIER, not harder: the surplus to be pushed down
    // fell from the 12,050 t the sea-level ledger claimed, so the headroom over rotorMaxT/0.6
    // widened from 5% to 15%. The descent check is still made at the ceiling; see
    // docs/OPEN-QUESTIONS.md #4 for why the bottom of the letdown is the harder case.
    genMW: 150, battMWh: 2000, battMW: 1400, cryoMW: 100, solarM2: 120000, diskM2: 160000, rotors: 14, ln2CapT: 15500,
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
