/* Projected coaxial footprint sensitivity only; model and drawing stay unchanged. */
import {pathToFileURL} from 'node:url';
import {S,geometry,profiles,replay,read,format,table,label} from './energy-rotor-common.mjs';
import {writeGenerated} from './energy-output.mjs';
export const COAXIAL_CREDIT={value:0.90,scope:'Favourable stipulated sensitivity input from the reviewer; not a measured property of these rotors.',source:'johnson-2009-ndarc',locator:'section 11-5.1.3, printed page 101'};
export function computeAreaSensitivity(cases=profiles()){
 const geometries=geometry();
 const pick=x=>({feasible:x.feasible,cycleMWh:x.eCycleMWh,rotorMWh:x.chan.rotors,worst:x.worst});
 return {scope:'Sensitivity at selected profiles’ fixed controls; no re-search, design change or aircraft result. Failed-row MWh is clipped supplied effort, not completion energy.',
  convention:'The drawing sums both blade disks at every coaxial station, approximately matching diskM2. A pair shares one stream, so its aerodynamic area is nearer one projected footprint; pricing treats its disks as independent. Footprints sum station areas without assigning additional inter-station overlap.',
  credit:COAXIAL_CREDIT,method:'Plan once with the original class and selected controls, then integrate that plan with footprint area. The stipulated credit is encoded as footprint area divided by credit squared; this is a hover-equivalent extension to the existing inflow law, not a validated coaxial envelope.',geometry:geometries,
  profiles:cases.map(q=>{
   const {c,m,p}=replay(q),g=geometries.find(g=>g.class===q.class);
   return {...q,baseline:pick(S.integrateCycle(c,m,p)),footprint:pick(S.integrateCycle({...c,diskM2:g.footprintM2},m,p)),
    footprintCredit:pick(S.integrateCycle({...c,diskM2:g.footprintM2/COAXIAL_CREDIT.value**2},m,p))};
  })};
}
export function areaText(){
 const data=read('energy-rotor-area'),f=format;
 let out='<!-- rotor:area:start -->\n\n### Rotor area convention\n\n'+data.convention+'\n\n'+data.scope+'\n\n';
 out+=table(['Class','Priced independent area m²','Drawn summed blade area m²','Projected footprint m²','Hover cap: priced / footprint tf','Same-thrust hover power: footprint / priced'],data.geometry.map(g=>[g.class,f(g.pricedM2),f(g.drawnSumM2),f(g.footprintM2),f(g.pricedCapT)+' / '+f(g.footprintCapT),f(g.sameThrustHoverPowerRatio,6)]));
 out+='\nHover caps use local density at the model’s working altitude and the unchanged efficiency and bus rating. The last column changes area only, at the same thrust and efficiency.\n\n';
 out+=`Stipulated sensitivity input: the reviewer’s favourable coaxial credit ${f(data.credit.value,2)}, from [Johnson’s NDARC theory](https://rotorcraft.arc.nasa.gov/ndarc/media/Files/reportsAndPapers/NDARC-NASA-TP-2009-215402.pdf), ${data.credit.locator}. It is not a measured property of these rotors. ${data.method}\n\n`;
 out+=table(['Fixed selected profile','Priced area: closes / MWh','Footprint: closes / supplied MWh / unheld tf','Footprint with stipulated credit: closes / supplied MWh / unheld tf'],data.profiles.filter(q=>q.dataset==='energy-profiles').map(q=>[label(q),`${q.baseline.feasible?'yes':'no'} / ${f(q.baseline.cycleMWh)}`,...[q.footprint,q.footprintCredit].map(v=>`${v.feasible?'yes':'no'} / ${f(v.cycleMWh)} / ${f(v.worst.unheldT)}`)]));
 return out+'\nFailed-row supplied MWh is clipped effort and cannot be used as energy required to complete a mission. A failed fixed-control replay does not exclude a different closing plan. No geometry, diskM2, efficiency or selected controls change.\n\n<!-- rotor:area:end -->\n';
}
if(process.argv[1]&&pathToFileURL(process.argv[1]).href===import.meta.url){
 const result=computeAreaSensitivity();
 writeGenerated('research/analysis/energy-rotor-area.json',JSON.stringify(result,null,2)+'\n');
 console.log(`PASS rotor area sensitivity: ${result.geometry.length} classes; ${result.profiles.length} fixed selected profiles; ${process.argv.includes('--check')?'record fresh':'record written'}`);
}
