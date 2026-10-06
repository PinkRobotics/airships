/* Logistics uses the same bounded selector as the served pages, at the exact leg.
 * Released water is a tank quantity, not a ground deposition or suppression result. */
import {selectServedPlan} from '../../sim/index.js?v=b2f068b7';
export function acceptedLogistics(cls, km) {
  const s = selectServedPlan(cls, km, null, 'balanced');
  const p = s.state === 'ready' && s.plan?.feasible ? s.plan : null;
  return {km, state: s.state, reason: s.reason || null, mode: s.mode || null,
    options: s.options || null, feasible: p ? true : false,
    releasedT: p?.deliveredT ?? null, retainedT: p?.retainedT ?? null,
    cycleMin: p?.cycleMin ?? null, suppliedMWh: p?.eCycleMWh ?? null,
    tph: p?.tph ?? null};
}
