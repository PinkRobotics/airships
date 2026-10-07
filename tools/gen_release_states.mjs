/* Replay accepted release states; ideal-disc arithmetic does not measure a wake. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {CLASSES,MODES,planCycle,drawAt} from '../sim/index.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const file='research/analysis/release-states.json';
export function replayRelease(cid,row){
 const c=CLASSES[cid];
 if(!row||row.state!=='ready')return {state:row?.state||'unavailable',plan:row,reason:'No accepted plan; no release illustration.'};
 const p=planCycle(c,MODES[row.mode],row.km,null,row.options);
 if(!p.feasible||row.options?.basis!=='record'||Math.abs(p.deliveredT-row.releasedT)>1e-9||Math.abs(p.retainedT-row.retainedT)>1e-9)
   throw Error(cid+': accepted release row does not replay');
 const states={};
 for(const [label,progress] of [['start of release',0],['end of release',1]]){
   const at=drawAt(c,MODES[row.mode],p,'WATER_RELEASE',progress);
   const held=at.owners.rotorT,rho=at.led.rho;
   if(!(held>=0&&rho>0))throw Error(cid+': unsupported release force or density');
   const vi=Math.sqrt(held*9810/(2*rho*c.diskM2));
   states[label]={progress,altitudeAglM:at.alt,densityKgM3:rho,waterAboardT:at.water,nitrogenAboardT:at.ln2,
     heldT:held,inducedUpwashAtDiscMs:vi,wakeMs:2*vi,airMassFlowKgS:rho*c.diskM2*vi};
 }
 const end=states['end of release'];
 const inflow=Object.fromEntries([25,50,100,200,300,400].map(z=>[z+' m below',c.diskM2*end.inducedUpwashAtDiscMs/(2*Math.PI*z*z)]));
 const benchmark=c.fillM3s*1000;
 return {state:'ready',basis:'Accepted worked-example plan replay, local density and water aboard; ideal-disc estimate, not wake or deposition evidence.',
  plan:row,diskM2:c.diskM2,states,inflowBelowHullMs:inflow,waterBenchmarkKgS:benchmark,
  benchmarkBasis:'Nominal water-rate benchmark from configured intake capacity, not measured outlet flow.',
  acceptedMeanWaterReleaseKgS:p.deliveredT*1000/(p.dur.WATER_RELEASE*60),airToWaterBenchmarkRatio:end.airMassFlowKgS/benchmark};
}
export function record({releaseOnly=false}={}){
 const water=JSON.parse(fs.readFileSync(path.join(root,'research/analysis/water-availability.json')));
 if(releaseOnly){
 return {producer:'tools/gen_release_states.mjs',classes:Object.fromEntries(Object.keys(CLASSES).map(cid=>[cid,replayRelease(cid,water.classes[cid].acceptedPlans.workedExample)]))};
 }
 const delivery=JSON.parse(fs.readFileSync(path.join(root,'research/analysis/delivery.json')));
 const heights=Object.keys(delivery.fall).filter(h=>h.includes('ALT.drop'));
 if(heights.length!==1)throw Error('delivery needs one corrected ALT.drop fall row');
 const largest=Math.max(...Object.values(delivery.fall[heights[0]]).map(r=>r.terminalAtReleaseMs));
 if(!(largest>0&&Number.isFinite(largest)))throw Error('corrected drop speed unavailable');
 return {producer:'tools/gen_release_states.mjs',dropComparison:{largestTabulatedReleaseSpeedMs:largest,
  basis:'Density-corrected fixed-diameter drop speeds at ALT.drop in delivery.json; no updraft or deposition model.'},
  classes:Object.fromEntries(Object.keys(CLASSES).map(cid=>[cid,replayRelease(cid,water.classes[cid].acceptedPlans.workedExample)]))};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const j=record({releaseOnly:process.argv.includes('--release-only')}),body=JSON.stringify(j,null,2)+'\n';
 if(process.argv.includes('--record'))console.log(JSON.stringify(j));
 else if(process.argv.includes('--emit'))console.log(JSON.stringify({[file]:body}));
 else if(process.argv.includes('--check')){
   if(!fs.existsSync(path.join(root,file))||fs.readFileSync(path.join(root,file),'utf8')!==body){console.error('release states RED: accepted replay differs');process.exit(1);}
   console.log('release states: all accepted plans replay at their own local release states');
 }else{fs.writeFileSync(path.join(root,file),body);console.log('release states: generated accepted release replays');}
}
