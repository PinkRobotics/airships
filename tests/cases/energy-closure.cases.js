/* Force closure: independent identities, limits, bus allocation and adversarial control points. */
import {describe,it,ok,close,eq} from '../harness.js';
import {CLASSES,MODES,PHASES,CFG,planCycle,drawAt,integrateCycle,resetConfig} from '../../sim/index.js?v=ae2bcece';
const sum = o => Object.values(o).reduce((a,b)=>a+b,0);
const winds=[null,{spd:40,dir:270,bearing:90},{spd:25,dir:90,bearing:90}];

export function assertInstant(c,p,s,tag) {
  const tol=1e-6*Math.max(1,Math.abs(s.surplusT));
  close(sum(s.owners)+s.unheldT,s.led.liftT-s.massT,tol,tag+' complete force accounting');
  ok(s.owners.bagT>=0 && s.owners.bagT<=c.anchorBagT+tol,tag+' bag capacity');
  ok(s.owners.rotorT>=0 && s.owners.rotorT<=s.thrustLimitT+tol,tag+' rotor thrust');
  ok(s.owners.aeroT>=0 && s.owners.aeroT<=s.aeroLimitT+tol,tag+' aero limit');
  if(s.airV===0)eq(s.owners.aeroT,0,tag+' stopped aero');
  if(p.basis==='record')eq(s.owners.aeroT,0,tag+' record aero');
  ok(s.draw.rotors <= Math.max(0,s.busMW-(sum(s.draw)-s.draw.rotors))+1e-6,tag+' whole bus rotor limit');
  const drag=(.5*s.led.rho*CFG.Cd*Math.PI*(c.diaM/2)**2*s.airV**2+s.inducedDragN)*s.airV/CFG.propEta/1e6;
  close(s.draw.prop,drag,1e-9*Math.max(1,drag),tag+' instantaneous propulsion law');
  if(Math.abs(s.unheldT)>tol || sum(s.draw)>s.busMW+1e-6) {
    eq(s.feasible,false,tag+' unsupported instant refused');
    ok(s.limits.length>0,tag+' instant reason');
    eq(p.feasible,false,tag+' unsupported plan refused');
    ok(p.bindingLimits.length>0 && p.worst.phase,tag+' plan reason/location');
  }
}

describe('energy closure — both bases',()=>{
  it('135 golden combinations x both bases x 1000 instants per phase: owners and limits',()=>{
    resetConfig();let n=0;
    for(const c of Object.values(CLASSES))for(const m of Object.values(MODES))for(const km of [5,15,30,60,120])for(const wind of winds)for(const basis of ['record','favourable']) {
      const p=planCycle(c,m,km,wind,{basis});
      for(const [id]of PHASES)for(let i=0;i<1000;i++) {
        const s=drawAt(c,m,p,id,i/999);assertInstant(c,p,s,`${c.id}/${m.id}/${km}/${basis}/${id}/${i}`);n++;
      }
    }
    eq(n,1620000,'sample count');
  });
  it('zero airspeed and both transit plateaus obey the same force and drag laws',()=>{
    for(const c of Object.values(CLASSES))for(const basis of ['record','favourable']){
      const p=planCycle(c,MODES.balanced,15,null,{basis});
      for(const id of ['WATER_FILL','OUTBOUND_TRANSIT','RETURN_TRANSIT'])assertInstant(c,p,drawAt(c,MODES.balanced,p,id,.5),c.id+id+basis);
    }
  });
  it('seam peaks and clipping are independent of energy quadrature resolution',()=>{
    for(const c of Object.values(CLASSES)) {
      const p=planCycle(c,MODES.balanced,15),a=integrateCycle(c,MODES.balanced,p,96),b=integrateCycle(c,MODES.balanced,p,384);
      eq(a.downMW,b.downMW);eq(a.rotorClipMin,b.rotorClipMin);eq(a.letdownClipMin,b.letdownClipMin);
      for(const [id]of PHASES)for(let i=0;i<=6144;i++)ok(drawAt(c,MODES.balanced,p,id,i/6144).draw.rotors<=p.downMW+1e-6,c.id+id+' dense peak');
    }
  });
  it('the fill inherits only water whose hoist completed before the seam',()=>{
    for(const [id,hoseM]of [['P100',300],['P100',323],['P1000',600]]) {
      const c={...CLASSES[id],hoseM},p=planCycle(c,MODES.balanced,15);
      const a=drawAt(c,MODES.balanced,p,'SOURCE_APPROACH',1),b=drawAt(c,MODES.balanced,p,'WATER_FILL',0);
      close(a.anchor.tonnes,b.anchor.tonnes,1e-9,'no unlifted mass');
      let work=0;for(let i=0;i<8192;i++)work+=drawAt(c,MODES.balanced,p,'SOURCE_APPROACH',(i+.5)/8192).hoistMW*p.dur.SOURCE_APPROACH/60/8192;
      close(work,a.anchor.tonnes*9810*15/.85/3.6e9,Math.max(1e-8,work*1e-4),'every hanging tonne hoisted');
    }
  });
});
