/* Prescribed controls are read from the descent record; these are diagnostics. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {CLASSES,MODES,CFG,planCycle} from '../sim/index.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output='research/analysis/editorial-controls.json';
const d=JSON.parse(fs.readFileSync(path.join(root,'research/analysis/descent.json')));
const controls={km:d.generated.worked.oneWayKm,mode:d.generated.worked.mode,basis:'record'};
const classes={};
for(const [id,c] of Object.entries(CLASSES)){
 const p=planCycle(c,MODES[controls.mode],controls.km,null,{basis:controls.basis});
 const doubled=planCycle({...c,diskM2:c.diskM2*2},MODES[controls.mode],controls.km,null,{basis:controls.basis});
 const nitrogen=p.ln2MakeT*CFG.eLN2*(1-CFG.rtLN2);
 classes[id]={name:c.name,prescribedCloses:p.feasible,cycleMWh:p.eCycleMWh,netNitrogenMWh:nitrogen,
   netNitrogenPct:100*nitrogen/p.eCycleMWh,doubledDiscM2:c.diskM2*2,
   doubledDiscCycleMWh:doubled.eCycleMWh,doubledDiscCloses:doubled.feasible,
   doubledDiscChangePct:100*(p.eCycleMWh-doubled.eCycleMWh)/p.eCycleMWh};
}
const body=JSON.stringify({producer:'tools/gen_editorial_controls.mjs',controls,
 basis:'Prescribed record controls; diagnostic effort comparisons, not operational savings.',classes},null,2)+'\n';
if(process.argv.includes('--check')){
 if(!fs.existsSync(path.join(root,output))||fs.readFileSync(path.join(root,output),'utf8')!==body){console.error('editorial controls RED: prescribed replay differs');process.exit(1);}
 console.log('editorial controls: prescribed and doubled-disc diagnostics match the live model');
}else if(process.argv.includes('--emit'))console.log(JSON.stringify({[output]:body}));
else{fs.writeFileSync(path.join(root,output),body);console.log('editorial controls: generated prescribed diagnostics');}
