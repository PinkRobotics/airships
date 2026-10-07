import {writeGenerated} from './energy-output.mjs';
/* Current comparisons use the live ledger; earlier published rows remain dated history. */
import fs from 'node:fs';
import {CLASSES,MODES,planCycle,energySummary} from '../../sim/index.js?v=31a23fa3';
const historical=JSON.parse(fs.readFileSync('research/analysis/energy-closure-history.json'));
const requirements=JSON.parse(fs.readFileSync('research/analysis/energy-requirements.json')).rows;
const rows=historical.flatMap(old=>['record','favourable'].map(basis=>({
 ...old,basis,current:energySummary(CLASSES[old.class],planCycle(CLASSES[old.class],MODES.balanced,old.km,null,{basis})),
 requirements:requirements.find(r=>r.class===old.class&&r.km===old.km&&r.basis===basis)
})));
writeGenerated('research/analysis/energy-closure.json',JSON.stringify({date:'2026-10-02',mode:'balanced',wind:'still air',
 warning:'Infeasible energy is supplied effort along an unsupported profile, not justified delivery or endurance.',rows},null,2)+'\n');
console.log('Generated twelve current closure comparisons beside their published history.');
