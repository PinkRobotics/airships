/* planCycle: the function that produces every number the site publishes.
 *
 * Given a vehicle class, an operating mode, a distance and a wind, it returns the
 * duration of each phase of a delivery cycle, the energy that cycle costs, how much
 * water arrives, and which constraint is binding. Pure: same inputs, same outputs.
 */
import { CFG } from './config.js';
import { diskMW, dragMW, ledger, pumpMW } from './physics.js';

export function planCycle(cls, mode, oneWayKm, wind) {
  // Airspeed is the vehicle's; ground speed belongs to the day. When a live 850 hPa wind is
  // known for the route, each leg gets its along-track component — one leg's tailwind is the
  // other's headwind. Clamped so a storm cannot produce absurd legs in a first-order model.
  const kph = cls.cruiseKph * mode.speed * CFG.speedMul;
  let gsOut = kph, gsRet = kph, tailOut = 0;
  if (wind && wind.spd != null && wind.bearing != null) {
    const toDir = (wind.dir + 180) % 360;
    const comp = b => wind.spd * Math.cos((toDir - b) * Math.PI / 180);
    tailOut = comp(wind.bearing);
    gsOut = Math.min(kph * 1.8, Math.max(kph * 0.35, kph + tailOut));
    gsRet = Math.min(kph * 1.8, Math.max(kph * 0.35, kph + comp((wind.bearing + 180) % 360)));
  }
  const fill = Math.max(0.01, cls.fillM3s * CFG.fillMul);
  const led = ledger(cls);
  const dur = {};                                   // minutes per phase
  // Overlap doctrine: the pod is already dropping during the approach, so HOSE_DEPLOY is
  // only the tail of that work; the hose winds up during the climb-out; climb and descent
  // ride the transit legs; and the drop is a run at working speed, not a hover.
  dur.SOURCE_APPROACH = Math.max(1.5 * mode.fixed, cls.hoseDeployMin * 0.5 * mode.hose);
  dur.WATER_FILL = cls.payloadT / fill / 60;
  // A leg is a trapezoid, not a step: the ship accelerates over the first 15% and brakes over
  // the last 15%, so covering the distance at a CRUISE of gsOut takes 1/0.85 as long as the
  // naive quotient. Without this the map flew 18% faster than the ground-speed dial read.
  const rampF = 1 / (1 - 0.15);
  dur.OUTBOUND_TRANSIT = Math.max(oneWayKm / gsOut * 60 * rampF,
    cls.hoseRetractMin * 0.4 * mode.hose + 0.8);
  dur.WATER_RELEASE = Math.max(0.8, cls.dropKm / (kph * 0.45) * 60);
  dur.BUOYANCY_ESCAPE = 2 * mode.fixed;
  dur.RETURN_TRANSIT = Math.max(1.2, oneWayKm / gsRet * 60 * rampF);

  // Nitrogen: the return leg's cryo output, bounded by the tanks and by what descent needs.
  const cryoCapMW = cls.cryoMW * CFG.cryoMul * mode.cryoShare;
  const ln2NeedT = Math.min(led.surplusT * 0.8, cls.ln2CapT);
  const ln2MakeT = Math.min(ln2NeedT, cryoCapMW * (dur.RETURN_TRANSIT / 60) * 1000 / CFG.eLN2 / 1000);
  const cryoLimited = ln2MakeT < ln2NeedT - 0.5;
  // The force balance must CLOSE. Rotors can only push down so hard on this bus:
  const rotorMaxT = Math.pow((cls.battMW + cls.genMW) * 1e6 * CFG.propEta *
    Math.sqrt(2 * CFG.rhoAir * cls.diskM2), 2 / 3) / 9.81 / 1000;
  // Whatever ballast and rotors (with aero assist) cannot cover, the Mind never drops in
  // the first place: retained water is descent ballast, and only the rest is delivered.
  const retainedT = Math.max(0, led.surplusT - ln2MakeT - rotorMaxT / 0.6);
  const deliveredT = cls.payloadT - retainedT;
  dur.WATER_FILL = deliveredT / fill / 60;          // only the delivered water needs replacing
  // The dump is metered like the fill: sprayers lay water on a line, they do not blow the
  // tanks. A payload bigger than one line's worth re-treats the line — whole passes, and an
  // odd count so the run still ends at the far end, where the escape climb begins.
  const lineMin = dur.WATER_RELEASE;
  let passes = Math.max(1, Math.ceil(deliveredT / fill / 60 / lineMin));
  if (passes % 2 === 0) passes += 1;
  dur.WATER_RELEASE = lineMin * passes;
  const resid = Math.max(0, led.surplusT - ln2MakeT - retainedT);
  const downMW = diskMW(cls, resid * 1000 * 9.81 * 0.6);   // ≤ bus by construction now
  const battLimited = downMW > (cls.battMW + cls.genMW) * 0.92;
  if (battLimited) dur.RETURN_TRANSIT *= 1.12;      // authority-limited: a longer, shallower letdown

  const cycleMin = Object.values(dur).reduce((a, b) => a + b, 0);

  // Energy, phase by phase (MWh). Hotel load rides on everything.
  const hotelMW = cls.genMW * 0.02;
  const eCryo = ln2MakeT * 1000 * CFG.eLN2 / 1000;  // MWh spent liquefying
  const eBack = eCryo * CFG.rtLN2;                  // partially recovered on discharge
  const E = {};
  // Recovery lands where the mass leaves: nitrogen expands back to electricity while the
  // fill replaces it with water, so it offsets pump work, not descent work.
  E.WATER_FILL = Math.max(0, pumpMW(cls) * dur.WATER_FILL / 60 - eBack);
  E.OUTBOUND_TRANSIT = dragMW(cls, mode) * dur.OUTBOUND_TRANSIT / 60;
  E.RETURN_TRANSIT = dragMW(cls, mode) * 0.55 * dur.RETURN_TRANSIT / 60 + eCryo; // lighter ship, cheaper leg
  E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60;
  E.other = hotelMW * cycleMin / 60 +
    dragMW(cls, mode) * 0.4 * (dur.SOURCE_APPROACH + dur.BUOYANCY_ESCAPE + dur.WATER_RELEASE) / 60;
  const eCycle = Object.values(E).reduce((a, b) => a + b, 0);

  const tph = deliveredT * 60 / cycleMin;
  const handling = dur.SOURCE_APPROACH + dur.WATER_FILL;
  const transit = dur.OUTBOUND_TRANSIT + dur.RETURN_TRANSIT;
  let bottleneck = "transit distance";
  if (handling > transit) bottleneck = "water handling at the source";
  if (cryoLimited && mode.id === "endurance") bottleneck = "cryogenic production rate";
  if (battLimited) bottleneck = "descent authority";
  if (retainedT > cls.payloadT * 0.25) bottleneck = "descent ballast — cryogenic capacity";

  return {
    dur, cycleMin, tph, eCycleMWh: eCycle, kwhPerTonne: eCycle * 1000 / Math.max(1, deliveredT),
    eBack,
    retainedT, deliveredT, rotorMaxT, passes,
    gsOut, gsRet, tailOut, windUsed: !!(wind && wind.spd != null),
    ln2MakeT, cryoLimited, battLimited, downMW, bottleneck,
    pumpMW: pumpMW(cls), dragMW: dragMW(cls, mode), led,
    dropsPerHour: 60 / cycleMin,
  };
}

/* ---------- water sources --------------------------------------------------------------- */
/* WATER rows: [lon, lat, areaHa, kind(0 lake|1 reservoir), name, ring|null]                  */
