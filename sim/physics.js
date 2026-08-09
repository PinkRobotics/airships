/* The four first-order physical relations the whole model is built on.
 *
 * Each is one equation with its units stated. If the project is wrong about how much
 * energy it takes to move water through the sky, it is wrong in one of these four
 * functions, so they are kept together, short, and separately testable.
 */
import { CFG } from './config.js';

export function pumpMW(cls) {
  return 1000 * 9.81 * (cls.fillM3s * CFG.fillMul) * CFG.hoseHead / CFG.pumpEta / 1e6;
}

export function dragMW(cls, mode) {
  const v = cls.cruiseKph * mode.speed * CFG.speedMul / 3.6;
  const A = Math.PI * (cls.diaM / 2) ** 2;
  return 0.5 * CFG.rhoAir * CFG.Cd * A * v ** 3 / CFG.propEta / 1e6;
}

export function diskMW(cls, thrustN) {
  if (thrustN <= 0) return 0;
  return Math.pow(thrustN, 1.5) / Math.sqrt(2 * CFG.rhoAir * cls.diskM2) / CFG.propEta / 1e6;
}

export function ledger(cls) {
  const liftT = cls.dispM3 * CFG.rhoSL / 1000;     // what the evacuated volume displaces
  const dryT = cls.payloadT;                       // structure allowance = payload (the ledger's bet)
  return { liftT, dryT, reserveT: liftT - dryT - cls.payloadT, surplusT: liftT - dryT };
}

/* The whole conceptual cycle for one class, mode and one-way distance. Pure arithmetic. */
