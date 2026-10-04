/* Fast four-invariant probe adapted from gpt-6-sol's independent force test. */
import {CLASSES,MODES,PHASES,planCycle,drawAt} from '../../sim/index.js?v=1ead4525';
import {auditForce} from '../cases/energy-force.cases.js';
let checked=0;
for(const c of Object.values(CLASSES))for(const basis of ['record','favourable']){
  const p=planCycle(c,MODES.balanced,15,null,{basis});
  for(const [phase] of PHASES)for(let i=0;i<=20;i++){
    auditForce(c,p,drawAt(c,MODES.balanced,p,phase,i/20));checked++;
  }
}
console.log('GREEN force mutations audit:',checked,'samples');
