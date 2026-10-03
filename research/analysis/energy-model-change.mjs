import {writeGenerated} from './energy-output.mjs';
/* Preserve the recorded earlier attribution; append the live, replayable comparison. */
import fs from 'node:fs';
const history=JSON.parse(fs.readFileSync('research/analysis/energy-attribution-history.json'));
const current=JSON.parse(fs.readFileSync('research/analysis/energy-closure.json'));
writeGenerated('research/analysis/energy-model-change.json',JSON.stringify({...history,currentComparison:{date:current.date,rows:current.rows.map(r=>({class:r.class,km:r.km,basis:r.basis,earlierMWh:r.first.cycleMWh,currentMWh:r.current.cycleMWh,changeMWh:r.current.cycleMWh-r.first.cycleMWh,feasible:r.current.feasible,reason:'Local density, named force owners, bus reservation and paid bag inventory.'}))}},null,2)+'\n');
console.log('Preserved historical attribution and regenerated the current twelve-row comparison.');
