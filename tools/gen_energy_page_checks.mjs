/* A reproducible force-check record for the generated page sentence. */
import fs from 'node:fs';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {CLASSES,MODES,PHASES,planCycle,drawAt} from '../sim/index.js';
import {MODEL_SOURCE_HASHES} from '../sim/served-candidates.js';
const path='research/analysis/energy-page-checks.json';
const strip=s=>s.replace(/(\.m?js)\?v=[A-Za-z0-9_.-]+(['"])/g,'$1$2');
const sourceHashes=Object.fromEntries(['tests/energy/closure.mjs','tests/energy/model.mjs'].map(file=>[file,crypto.createHash('sha256').update(strip(fs.readFileSync(file,'utf8'))).digest('hex')]));
const report=JSON.parse(execFileSync(process.execPath,['tests/energy/closure.mjs'],{env:{...process.env,N:'1000'},encoding:'utf8',maxBuffer:8*1024*1024}));
if(Object.keys(report.violations).length||report.verdictMismatches.length)throw new Error('force-check record contains violations');
const examples=['record','favourable'].map(basis=>{
 const cls=CLASSES.P100,mode=MODES.balanced,km=60,p=planCycle(cls,mode,km,null,{basis});
 if(!p.feasible)throw new Error('as-drawn 60 km example no longer closes');
 let peak=null;
 for(const [phase] of PHASES)for(let i=0;i<p.planSteps;i++){
  const progress=(i+.5)/p.planSteps,s=drawAt(cls,mode,p,phase,progress);
  if(!peak||s.draw.rotors>peak.rotorMW)peak={phase,progress,rotorMW:s.draw.rotors,supplyMW:s.busMW,grossMW:Object.values(s.draw).reduce((a,b)=>a+b,0)};
 }
 return {class:cls.id,km,basis,mode:mode.id,feasible:p.feasible,planSteps:p.planSteps,peak};
});
const body=JSON.stringify({producer:'tools/gen_energy_page_checks.mjs',model:MODEL_SOURCE_HASHES,checkSources:sourceHashes,report,examples},null,2)+'\n';
if(process.argv.includes('--check')){
 if(!fs.existsSync(path)||fs.readFileSync(path,'utf8')!==body){console.error('FAIL stale generated page force-check record: '+path);process.exitCode=1;}
 else console.log('PASS page force-check record: '+report.instants+' independently checked instants, no violations');
}else{fs.writeFileSync(path,body);console.log('Generated page force-check record: '+report.instants+' instants');}
