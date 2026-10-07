/* An empirical isolated-rotor screen on the unchanged force/velocity trace. */
import {pathToFileURL} from 'node:url';
import {S,geometry,profiles,replay,read,format,table,label} from './energy-rotor-common.mjs';
import {writeGenerated} from './energy-output.mjs';
export const SCREEN_INPUTS={scope:'Stipulated sensitivity inputs from the reviewer’s isolated-rotor screen; not measured hull or coaxial-array properties.',
 source:'johnson-2005-vortex-ring',locator:'Tables 3–4, printed pages 23–24',edgewiseLimit:0.95,axialUpper:-0.45,axialLower:-1.5,upperExponent:0.2,lowerExponent:1.5};
export const SAMPLES_PER_PHASE=2000;
export function vrsScreen(s,c){
 if(!(s.thrustN>0))return null;
 const vh=Math.sqrt(s.thrustN/(2*s.led.rho*c.diskM2)),x=s.airV/vh,z=-s.vz/vh;
 const k=SCREEN_INPUTS;
 if(!(x<k.edgewiseLimit&&z<0))return {vh,x,z,inside:false};
 const f=1-(x/k.edgewiseLimit)**2,mid=(k.axialUpper+k.axialLower)/2,half=(k.axialUpper-k.axialLower)/2;
 const upper=mid+half*f**k.upperExponent,lower=mid-half*f**k.lowerExponent;
 return {vh,x,z,upper,lower,inside:z>lower&&z<upper};
}
export function computeRegimeSensitivity(cases=profiles()){
 const geometries=geometry();
 return {scope:'Empirical screen on isolated-rotor data at selected profiles’ fixed controls, with no re-search. It marks an unresolved state, not measured instability of an unbuilt hull; it does not make quasi-static closure false. Power while rising is priced as level flight with no bound. No replacement power, thrust or efficiency penalty is assigned.',
  inputs:SCREEN_INPUTS,samplesPerPhase:SAMPLES_PER_PHASE,
  method:'Equal midpoint progress samples per phase, matching the pre-review probe. Hover induced velocity uses actual rotor thrust and local density; normalized axial speed is signed hull velocity relative to downward thrust, and normalized edgewise speed is the model’s airV. Footprint changes normalization on the same original trace only.',
  profiles:cases.map(q=>{
   const {c,m,p}=replay(q),g=geometries.find(g=>g.class===q.class);
   const phases=S.PHASES.map(([phase])=>{
    let count=0,footCount=0,risingRotorMWh=0,totalRotorMWh=0,firstInside=null,peakRising=null;
    const dtHours=p.dur[phase]/60/SAMPLES_PER_PHASE;
    for(let i=0;i<SAMPLES_PER_PHASE;i++){
     const progress=(i+.5)/SAMPLES_PER_PHASE,s=S.drawAt(c,m,p,phase,progress),v=vrsScreen(s,c);
     if(v&&(!peakRising||-v.z>-peakRising.z))peakRising={phase,progress,altM:s.alt,vz:s.vz,airV:s.airV,thrustN:s.thrustN,rho:s.led.rho,...v};
     if(v?.inside){count++;firstInside??={phase,progress,altM:s.alt,vz:s.vz,airV:s.airV,thrustN:s.thrustN,rho:s.led.rho,...v};}
     if(vrsScreen(s,{...c,diskM2:g.footprintM2})?.inside)footCount++;
     totalRotorMWh+=s.draw.rotors*dtHours;
     if(s.vz>0)risingRotorMWh+=s.draw.rotors*dtHours;
    }
    return {phase,durationMinutes:p.dur[phase],screenMinutes:count/SAMPLES_PER_PHASE*p.dur[phase],footprintScreenMinutes:footCount/SAMPLES_PER_PHASE*p.dur[phase],risingRotorMWh,totalRotorMWh,firstInside,peakRising};
   });
   const totalScreenMinutes=phases.reduce((a,p)=>a+p.screenMinutes,0),risingRotorMWh=phases.reduce((a,p)=>a+p.risingRotorMWh,0);
   return {...q,totalScreenMinutes,footprintScreenMinutes:phases.reduce((a,p)=>a+p.footprintScreenMinutes,0),risingRotorMWh,
    risingFractionOfRotorMWh:risingRotorMWh/S.integrateCycle(c,m,p).chan.rotors,phases};
  })};
}
export function regimeSentence(){
 const data=read('energy-rotor-regime'),selected=data.profiles.filter(q=>q.dataset==='energy-profiles');
 const hit=selected.filter(q=>q.totalScreenMinutes>0);
 const detail=hit.map(q=>`${label(q)}: ${format(q.totalScreenMinutes,6)} sampled minutes (${q.phases.filter(p=>p.screenMinutes>0).map(p=>p.phase.toLowerCase().replaceAll('_',' ')+' '+format(p.screenMinutes,6)).join('; ')})`).join(', ');
 return `${hit.length} of ${selected.length} selected profiles cross the empirical isolated-rotor vortex-ring screen${hit.length?', including '+detail:''}. The generated phase table in [the selected-profile analysis](../research/analysis/energy-profiles.md#isolated-rotor-regime-screen) identifies the crossings. ${data.scope}`;
}
export function regimeTable(dataset){
 const data=read('energy-rotor-regime'),rows=data.profiles.filter(q=>q.dataset===dataset),f=v=>format(v,6);
 const phases=S.PHASES.map(([id])=>id);
 let out='\n<!-- rotor:regime:start -->\n\n## Isolated-rotor regime screen\n\n'+data.scope+'\n\n';
 out+=`Stipulated sensitivity inputs: edgewise limit ${data.inputs.edgewiseLimit}, axial endpoints ${data.inputs.axialUpper} and ${data.inputs.axialLower}, boundary exponents ${data.inputs.upperExponent} and ${data.inputs.lowerExponent}; [Johnson’s vortex-ring model](https://rotorcraft.arc.nasa.gov/Publications/files/Johnson_TP-2005-213477.pdf), ${data.inputs.locator}. These are not measured properties of these rotors. Sampling is ${data.samplesPerPhase} midpoint intervals per phase. ${data.method}\n\n`;
 out+=table(['Fixed profile',...phases.map(id=>id+' min'),'Total min','Footprint: same-trace total min','Rising rotor MWh','Rising fraction of rotor MWh'],rows.map(q=>[label(q),...phases.map(id=>f(q.phases.find(p=>p.phase===id).screenMinutes)),f(q.totalScreenMinutes),f(q.footprintScreenMinutes),f(q.risingRotorMWh),f(q.risingFractionOfRotorMWh)]));
 return out+'\nScreen minutes are sampled occupancy, not a solved unstable trajectory. Zero occupancy does not validate a profile’s dynamics or rotor control. The rising rotor energy is the existing level-flight substitute, not a replacement vortex-ring power prediction.\n\n<!-- rotor:regime:end -->\n';
}
if(process.argv[1]&&pathToFileURL(process.argv[1]).href===import.meta.url){
 const data=computeRegimeSensitivity();
 writeGenerated('research/analysis/energy-rotor-regime.json',JSON.stringify(data,null,2)+'\n');
 console.log(`PASS rotor regime screen: ${data.profiles.length} fixed selected profiles; ${data.samplesPerPhase} midpoint samples per phase; ${process.argv.includes('--check')?'record fresh':'record written'}`);
}
