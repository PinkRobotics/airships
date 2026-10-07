/* The stricter completed-hoist rule is a sensitivity, not the default force owner. */
import {producerCheckMode,writeOutputs} from './energy-output.mjs';
import {CLASSES,MODES,ballastRequirement} from '../../sim/index.js?v=01e992e3';
const check=producerCheckMode('node research/analysis/energy-bag-comparison.mjs');
const rows=[];
for(const c of Object.values(CLASSES))for(const km of [15,60])for(const basis of ['record','favourable']){
 const carried=ballastRequirement(c,MODES.balanced,km,{basis});
 const completed=ballastRequirement(c,MODES.balanced,km,{basis,bagCreditRule:'completed-hoist'});
 const row={class:c.id,km,basis,carried,completed,extraRetainedT:carried.feasible&&completed.feasible?completed.ballastT-carried.ballastT:null};
 rows.push(row);console.log(c.id,km,basis,'stricter-rule extra ballast',row.extraRetainedT);
}
writeOutputs({'research/analysis/energy-bag-comparison.json':JSON.stringify({rule:'The cable carries water from pickup while its hoist remains priced. The comparison delays force credit until that hoist finishes.',rows},null,2)+'\n'},check);
