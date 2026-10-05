/* Exact-input logistics acceptance. Reads only local generated analysis records. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {CLASSES,MODES,planCycle} from '../sim/index.js';
import {acceptedLogistics} from '../research/analysis/accepted-logistics.js';
export function checkRecord(cid, row, replayOnly=false) {
  if (!row || !Number.isFinite(row.km)) throw Error(`${cid}: missing exact-input plan row`);
  if (row.tph != null && (row.state !== 'ready' || row.feasible !== true))
    throw Error(`${cid}: infeasible or inactive row supplies a logistics rate`);
  let fresh;
  if (replayOnly && row.state === 'ready') {
    const p = planCycle(CLASSES[cid], MODES[row.mode], row.km, null, row.options);
    if (!p.feasible || !(p.deliveredT > 0) || row.options?.basis !== 'record')
      throw Error(`${cid}: exact-input replay refuses logistics rate`);
    fresh = {km:row.km, state:'ready', reason:null, mode:row.mode, options:row.options,
      feasible:true,releasedT:p.deliveredT,retainedT:p.retainedT,cycleMin:p.cycleMin,
      suppliedMWh:p.eCycleMWh,tph:p.tph};
  } else fresh = acceptedLogistics(CLASSES[cid], row.km);
  for (const key of Object.keys(fresh)) {
    if (typeof fresh[key] === 'number') {
      if (!Number.isFinite(row[key]) || Math.abs(row[key]-fresh[key]) > 1e-9)
        throw Error(`${cid}: ${key} differs from exact-input accepted plan`);
    } else if (JSON.stringify(row[key]) !== JSON.stringify(fresh[key]))
      throw Error(`${cid}: ${key} differs from served selector`);
  }
  return row.state === 'ready';
}
const rounded = (v,n=1) => v == null ? null : Number(v.toFixed(n));
export function checkFiles(directory) {
  const water = JSON.parse(fs.readFileSync(path.join(directory,'water-availability.json')));
  const delivery = JSON.parse(fs.readFileSync(path.join(directory,'delivery.json')));
  let count = 0, accepted = 0, inactive = 0;
  for (const [cid, c] of Object.entries(water.classes)) {
    const plans = c.acceptedPlans;
    if (!plans || !Array.isArray(plans.byFire)) throw Error(`${cid}: missing exact-input accepted-plan rows`);
    if (plans.byFire.length !== c.servedWithinFarKm.fires) throw Error(`${cid}: missing fire legs`);
    for (const [name, rate] of [['workedExample','atWorkedExample15km'],['medianByFire','atMedianByFire'],['medianByHectare','atMedianByHectare']]) {
      checkRecord(cid, plans[name]); count++;
      if (c.throughputTph[rate] !== rounded(plans[name].tph)) throw Error(`${cid}: ${rate} is not its accepted rate`);
    }
    if (plans.workedExample.km !== 15 || plans.medianByFire.km !== c.distanceKm.byFire.p50 ||
        plans.medianByHectare.km !== c.distanceKm.byHectare.p50) throw Error(`${cid}: plan is bound to another leg`);
    const ready = [];
    for (const row of plans.byFire) {
      if (checkRecord(cid,row,true)) {ready.push(row);accepted++;} else inactive++;
      count++;
    }
    const mean = ready.length ? ready.reduce((a,r)=>a+r.tph,0)/ready.length : null;
    const ha = ready.reduce((a,r)=>a+r.ha,0);
    const weighted = ha ? ready.reduce((a,r)=>a+r.tph*r.ha,0)/ha : null;
    if (c.throughputTph.meanOverFires !== rounded(mean) || c.throughputTph.meanOverHectares !== rounded(weighted))
      throw Error(`${cid}: mean includes inactive legs or differs from accepted rates`);
    const counts = c.logisticsService;
    if (counts.acceptedFires !== ready.length || counts.notServedFires !== water.input.fires-ready.length ||
        counts.standDowns !== plans.byFire.filter(r=>r.state==='stand-down').length ||
        counts.unavailable !== plans.byFire.filter(r=>r.state==='unavailable').length)
      throw Error(`${cid}: accepted/stand-down counts disagree`);
    const g = water.geometry[cid], draw = plans.workedExample.tph;
    if (g.drawTonnesPer12h !== rounded(draw == null ? null : draw*12,0) ||
        g.drawdownMetresPer12hOnMinBody !== rounded(draw == null ? null : draw*12/(c.minSourceHa*10000),4))
      throw Error(`${cid}: drawdown is not based on accepted throughput`);
    const d = delivery.classes[cid], median = plans.medianByFire;
    const worked = plans.workedExample;
    if (worked.state === 'ready') {
      const p = planCycle(CLASSES[cid], MODES[worked.mode], worked.km, null, worked.options);
      const seconds = p.dur.WATER_RELEASE*60;
      if (d.releaseSeconds !== Math.round(seconds) || Math.abs(d.releaseRateM3s-worked.releasedT/seconds)>1e-9)
        throw Error(`${cid}: worked release uses another plan's duration or rate`);
    }
    if (worked.state !== 'ready' && (d.payloadT != null || d.releaseSeconds != null || d.releaseRateM3s != null || Object.values(d.coverageLevelBySwath).some(v=>v!=null)))
      throw Error(`${cid}: inactive worked example supplies release or coverage`);
    if (JSON.stringify(d.workedExamplePlan) !== JSON.stringify(plans.workedExample) ||
        JSON.stringify(d.atRealMedianLeg.plan) !== JSON.stringify(median)) throw Error(`${cid}: delivery plan drift`);
    if (d.atRealMedianLeg.tph !== median.tph || d.atRealMedianLeg.tonnesPer24h !== rounded(median.tph == null ? null : median.tph*24,0))
      throw Error(`${cid}: daily delivery uses an unaccepted rate`);
  }
  return `logistics: ${count} exact-input rows checked; ${accepted} accepted fire legs; ${inactive} inactive legs excluded from means`;
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  try {
    if (process.argv[2] === '--row') {
      const {cid,row}=JSON.parse(fs.readFileSync(process.argv[3]));
      checkRecord(cid,row); console.log('logistics: accepted or inactive row has exact-input semantics');
    } else console.log(checkFiles(process.argv[2] || 'research/analysis'));
  } catch (e) {console.error('logistics RED: '+e.message);process.exitCode=1;}
}
