/* One model: force-closure regressions plus plan/state and electrical ledger parity. */
import './energy-closure.cases.js';
import './energy-force.cases.js';
import './energy-profile.cases.js';
import './energy-assumptions.cases.js';
import './energy-planner.cases.js';
import {describe,it,ok,close,eq,deepEq} from '../harness.js';
import {CFG,WORK_ALT_MSL,ledger,CLASSES,CLASS_ORDER,MODES,PHASES,drawAt,planCycle,integrateCycle,inducedMW,diskMW,stateAt,buildMission,findSource,resetConfig,setSeed} from '../../sim/index.js?v=b2f068b7';
describe('one energy record',()=>{
  it('plan equals a finer independent phase integral on both bases',()=>{
    for(const c of Object.values(CLASSES))for(const basis of ['record','favourable']){
      const p=planCycle(c,MODES.balanced,15,null,{basis});let energy=0;
      for(const [id]of PHASES)for(let i=0;i<4000;i++){
        const s=drawAt(c,MODES.balanced,p,id,(i+.5)/4000);
        energy+=(Object.values(s.draw).reduce((a,b)=>a+b,0)-(s.gen.regen||0))*p.dur[id]/60/4000;
      }
      close(energy/p.eCycleMWh,1,.005,c.id+basis);
    }
  });
  it('stateAt uses the same draw and generation at 9000 instants',()=>{
    for(const c of Object.values(CLASSES))for(const mode of Object.values(MODES)){
      const plan=planCycle(c,mode,15),m={cls:c,mode,plan,offset:0,legKm:15,oneWayKm:15,fire:{id:'ENERGY',ll:[-120.05,50.05]},intake:[-120.3,50],delivery:[-120.05,50.05],cycleSec:plan.cycleMin*60,phaseEnds:[]};
      let t=0;for(const [id]of PHASES){t+=plan.dur[id]*60;m.phaseEnds.push(t);}
      for(let i=0;i<1000;i++){const s=stateAt(m,m.cycleSec*(i+.5)/1000),d=drawAt(c,mode,plan,s.phase,s.prog);deepEq(s.draw,d.draw);deepEq(s.gen,d.gen);}
    }
  });
  it('Glauert reduces to hover and satisfies the oblique-flow identity',()=>{
    for(const c of Object.values(CLASSES)){
      const T=c.payloadT*9810*.1;eq(inducedMW(c,T),diskMW(c,T));
      for(const [V,vc]of [[36,0],[7.5,2],[0,3]]){
        const P=inducedMW(c,T,V,vc),vi=P*1e6*CFG.propEta/T-vc;
        close(vi*Math.sqrt(V*V+(vc+vi)**2)/(T/(2*ledger(c,WORK_ALT_MSL).rho*c.diskM2)),1,1e-9);
      }
    }
  });
});

const WATER = [[-120.30, 50.00, 40000, 0, 'Big Lake', null]];
const FIRE = () => ({ id: 'NRG-1', ll: [-120.05, 50.05], sizeHa: 4000, status: 'Out of Control', note: false, ring: null });

function mission(clsId, modeId = 'balanced') {
  resetConfig();
  setSeed(7);
  const f = FIRE();
  const src = findSource(f.ll, CLASSES[clsId], WATER);
  return buildMission(f, WATER, modeId, clsId, { src, relaxed: false });
}

/** Riemann sum of every draw channel over one cycle, in MWh. N is large enough that the
    sum has converged to well under a percent; doubling it moves the totals by ~0.1%. */
function integrate(m, N = 4000) {
  let draw = 0, gen = 0;
  const dtH = (m.cycleSec / N) / 3600;
  for (let i = 0; i < N; i++) {
    const st = stateAt(m, (m.cycleSec * (i + 0.5)) / N + m.cycleSec - m.offset * m.cycleSec);
    for (const v of Object.values(st.draw)) draw += v * dtH;
    for (const v of Object.values(st.gen)) gen += v * dtH;
  }
  return { drawMWh: draw, genMWh: gen };
}

describe('energy · each model on its own terms', () => {
  it('the planned cycle energy is positive, finite and dominated by nothing negative', () => {
    resetConfig();
    for (const id of CLASS_ORDER) for (const mid of Object.keys(MODES)) {
      const p = planCycleOf(id, mid);
      ok(isFinite(p.eCycleMWh) && p.eCycleMWh > 0, `${id}/${mid}: eCycleMWh = ${p.eCycleMWh}`);
      ok(p.kwhPerTonne > 0 && p.kwhPerTonne < 1e6, `${id}/${mid}: ${p.kwhPerTonne} kWh/t`);
    }
  });

  it('the integrated draw is positive and finite', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const { drawMWh, genMWh } = integrate(m, 1200);
      ok(isFinite(drawMWh) && drawMWh > 0, `${id}: integrated draw = ${drawMWh}`);
      ok(isFinite(genMWh) && genMWh > 0, `${id}: integrated generation = ${genMWh}`);
      ok(genMWh < drawMWh, `${id}: generation ${genMWh.toFixed(1)} MWh exceeds draw ${drawMWh.toFixed(1)} MWh — the fleet is meant to run a deficit`);
    }
  });

  it('the integration has converged', () => {
    const m = mission('P1000');
    const coarse = integrate(m, 600).drawMWh;
    const fine = integrate(m, 4800).drawMWh;
    close(fine / coarse, 1, 0.02, 'the Riemann sum is still moving at 600 samples');
  });
});


function planCycleOf(id, mid) { return mission(id, mid).plan; }
