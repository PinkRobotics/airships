import {CLASSES,MODES,planCycle,drawAt} from '../../sim/index.js?v=93744380';
import {assertInstant} from '../cases/energy-closure.cases.js';
for(const c of Object.values(CLASSES))for(const basis of ['record','favourable']){
 const p=planCycle(c,MODES.balanced,15,null,{basis});
 for(const id of ['WATER_FILL','SOURCE_APPROACH','RETURN_TRANSIT','OUTBOUND_TRANSIT'])for(const x of [0,.25,.5,.75,1])assertInstant(c,p,drawAt(c,MODES.balanced,p,id,x),`${c.id}/${basis}/${id}/${x}`);
}
console.log('PASS independent force, stopped aero, instantaneous drag and whole-bus assertions');
