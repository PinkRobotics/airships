/* Projected collection area derived from the current capsule footprint. */
import fs from 'node:fs';
import {CLASSES,DEFAULTS,SOLAR_PROJECTED_FRACTION,aeroGeometry} from '../../sim/index.js?v=816a54f9';
if (!(SOLAR_PROJECTED_FRACTION > 0 && SOLAR_PROJECTED_FRACTION <= 1)) throw new Error('projected coverage must be a fraction in (0, 1]');
for (const c of Object.values(CLASSES)) {
 if (!(Number.isFinite(c.solarM2) && c.solarM2 > 0 && c.solarM2 <= aeroGeometry(c).areaM2)) throw new Error(c.id + ': collector exceeds current footprint or is invalid');
}
const data={generator:'research/analysis/solar-area.mjs',
 coverage:{fraction:SOLAR_PROJECTED_FRACTION,basis:`Unvalidated design assumption: ${100*SOLAR_PROJECTED_FRACTION}% of the current projected capsule footprint carries collecting area. No panel layout or yield validation is claimed.`},
 materialArea:'solarSheetM2 is the independent assumed gross sheet area used by the mass budget. It supplies no extra power credit; curved material area and horizontal projected collection area are different quantities.',
 classes:Object.fromEntries(Object.entries(CLASSES).map(([id,c])=>[id,{name:c.name,lengthM:c.lenM,diameterM:c.diaM,footprintM2:aeroGeometry(c).areaM2,
 projectedSolarM2:c.solarM2,projectedFraction:c.solarM2/aeroGeometry(c).areaM2,grossSheetM2:c.solarSheetM2,
 creditedSolarMW:c.solarM2*DEFAULTS.solarWPerM2/1e6}]))};
const file='research/analysis/solar-area.json',text=JSON.stringify(data,null,2)+'\n';
if(process.argv.includes('--check')){
 if(!fs.existsSync(file)||fs.readFileSync(file,'utf8')!==text){console.error('solar area RED: current geometry differs from '+file);process.exitCode=1;}
 else console.log('solar area: every projected area is the named fraction of its current capsule footprint');
}else if(process.argv.includes('--emit'))console.log(JSON.stringify({[file]:text}));
else{fs.writeFileSync(file,text);for(const [id,r] of Object.entries(data.classes))console.log(`${id}: footprint ${r.footprintM2.toFixed(3)} m2; projected solar ${r.projectedSolarM2.toFixed(3)} m2 (${(r.projectedFraction*100).toFixed(1)}%); credit ${r.creditedSolarMW.toFixed(6)} MW; gross sheet assumption ${r.grossSheetM2} m2`);}
