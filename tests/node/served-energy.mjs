/* Adversarial checks of the page selector's acceptance, distinct from model equations. */
import assert from 'node:assert/strict';
import {CLASSES,MODES,CFG,PHASES,planCycle,selectServedPlan,auditServedPlan,stateAt,missionReady,workedFigures} from '../../sim/index.js?v=fc85766f';
const cls=CLASSES.P100,km=15,selection=selectServedPlan(cls,km,null,'balanced');
assert.equal(selection.state,'ready');
const inactive=selectServedPlan(CLASSES.P10000,3,null,'balanced',[]);
assert.equal(inactive.state,'stand-down');
function validate(m){
 auditServedPlan(m.cls,m.legKm,m.wind,m.selection,m.mode.id);
 if(m.selection.state!=='ready'){
  if(!m.idle||!stateAt(m,0).inactive)throw new Error('stand-down is shown flying');
  assert.equal(missionReady(m),false);assert.deepEqual(workedFigures(m.cls,m.legKm,m.selection).rows,[]);
 }else if(m.plan!==m.selection.plan||m.idle)throw new Error('mission differs from selected plan');
}
const fixture={cls,legKm:km,wind:null,selection,plan:selection.plan,mode:MODES[selection.mode],served:true,planState:'ready',idle:false,fire:{ll:[0,0]}};
const stand={...fixture,cls:CLASSES.P10000,legKm:3,selection:inactive,plan:null,planState:'stand-down',idle:true};
const mutation=process.argv.includes('--mutation')?process.argv[process.argv.indexOf('--mutation')+1]:null;
try{
 if(process.argv.includes('--mutation')){
  if(mutation==='infeasible'){const bad=planCycle(cls,MODES.balanced,km);fixture.selection={...selection,plan:bad};fixture.plan=bad;}
  else if(mutation==='neighbor')fixture.legKm=km+.01;
  else if(mutation==='mode')fixture.mode=MODES[selection.mode==='rapid'?'balanced':'rapid'];
  else if(mutation==='stand-down')stand.idle=false;
  else throw new Error('unknown mutation');
  validate(mutation==='stand-down'?stand:fixture);
  console.log('UNEXPECTED GREEN '+mutation);process.exitCode=2;
 }else{
  validate(fixture);validate(stand);
  assert.equal(selectServedPlan(CLASSES.P1000,400,null,'endurance').state,'ready','battery-hours quotient is not an endurance rule');
  assert.equal(selectServedPlan(CLASSES.P100,15,{spd:40,dir:270,bearing:90},'rapid').state,'stand-down','model wind refusal uses the bounded candidate set');
  assert.equal(selectServedPlan(cls,km,null,'balanced'),selection,'identical exact inputs are cached');
  assert.notEqual(selectServedPlan(cls,km+.01,null,'balanced').key,selection.key,'neighboring distance changes cache key');
  const wind={spd:0,dir:210,bearing:38,capture:'dated fixture'},w=selectServedPlan(cls,km,wind,'balanced');
  assert.equal(w.state,'ready');auditServedPlan(cls,km,wind,w,w.mode);
  assert.notEqual(w.key,selection.key,'missing wind is distinct from a measured value');
  assert.equal(selectServedPlan(cls,km,{spd:0},'balanced').state,'unavailable');
  const old=CFG.fillMul;CFG.fillMul=old+.1;assert.notEqual(selectServedPlan(cls,km,null,'balanced').key,selection.key);CFG.fillMul=old;
  assert.ok(selection.plan.retainedT>0);assert.equal(selection.plan.deliveredT+selection.plan.retainedT,cls.payloadT);
  console.log('PASS served selector: exact input and mode replay, wind distinction, all-input cache, retained/delivered water, labelled stand-down, malformed wind unavailable');
 }
}catch(error){console.error('FAIL '+(mutation||'served selector')+': '+error.message);process.exitCode=1;}
