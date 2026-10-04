/* State data only: the Python checker reconstructs the equations independently. */
import {CLASSES,MODES,planCycle,drawAt} from '../../sim/index.js?v=182fd413';
const rows=[];
for(const c of Object.values(CLASSES))for(const km of [15,60])for(const basis of ['record','favourable']){
 const p=planCycle(c,MODES.balanced,km,null,{basis}),s=drawAt(c,MODES.balanced,p,p.worst.phase,p.worst.progress);
 rows.push({class:c.id,km,basis,phase:p.worst.phase,progress:p.worst.progress,...s});
}
console.log(JSON.stringify(rows));
