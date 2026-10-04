/* Observe inputs and model results; the Python check supplies the independent equations. */
import fs from 'node:fs';
import {CLASSES,MODES,CFG,planCycle,drawAt,rotorMaxTonnes,ledger} from '../../sim/index.js?v=182fd413';
const modes=[],profiles=[];
for(const c of Object.values(CLASSES))for(const m of Object.values(MODES)) {
 const p=planCycle(c,m,15,null,{basis:'record'}),s=drawAt(c,m,p,'WATER_FILL',.3);
 modes.push({class:c.id,mode:m.id,batteryMW:c.battMW,generatorRatingMW:c.genMW,diskM2:c.diskM2,
   eta:p.rotorEfficiency,rho:s.led.rho,fullBusModelT:rotorMaxTonnes(c,c.battMW+c.genMW,s.led.rho,p.rotorEfficiency),
   modeBusMW:s.busMW,solarMW:s.gen.solar,regenMW:s.gen.regen||0,nonRotorMW:s.nonRotorMW,
   modeModelT:rotorMaxTonnes(c,Math.max(0,s.busMW-s.nonRotorMW),s.led.rho,p.rotorEfficiency),
   emptySurplusT:ledger(c,1300).surplusT});
}
for(const name of ['energy-profiles','energy-feasible'])for(const row of JSON.parse(fs.readFileSync(`research/analysis/${name}.json`)).rows)for(const [kind,b] of [['cheapest',row.best],['full delivery',row.fullDeliveryBest]])if(b) {
 const c=CLASSES[b.class],m=MODES[b.mode],p=planCycle(c,m,b.km,null,b.options),s=drawAt(c,m,p,'WATER_FILL',.3);
 profiles.push({table:name,kind,class:b.class,km:b.km,basis:b.basis,mode:b.mode,retainedT:p.retainedT,
   diskM2:c.diskM2,eta:p.rotorEfficiency,rho:s.led.rho,volumeM3:c.dispM3,dryT:c.payloadT,
   busMW:s.busMW,nonRotorMW:s.nonRotorMW,installedMW:c.battMW+c.genMW,
   newWaterT:s.water-p.retainedT,nitrogenT:s.ln2,bagT:s.owners.bagT,
   verticalDragT:s.owners.verticalDragT,aeroT:s.owners.aeroT,airV:s.airV,vz:s.vz,
   modelUnheldT:s.unheldT,modelRotorT:s.owners.rotorT});
}
console.log(JSON.stringify({modes,profiles}));
