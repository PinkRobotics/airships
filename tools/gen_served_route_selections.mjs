/* Captured route inputs remain fixed; current controls replay the served selector. */
import fs from 'node:fs';
import {CLASSES,selectServedPlan} from '../sim/index.js';
const file='tests/energy/served-route-distances.json';
const original=fs.readFileSync(file,'utf8'),data=JSON.parse(original);
data.source='Local captured route inputs from the shipped exercise and dated replay; current controls replayed through the served selector. No emergency feed fetched.';
let changed=0;
for(const m of data.missions){
 const s=selectServedPlan(CLASSES[m.class],m.km,null,m.mode);
 if(s.state!=='ready'||!s.plan?.feasible)throw Error(`Captured route no longer accepted: ${m.capture}/${m.mission}`);
 const {basis,...options}=s.options;
 if(s.mode!==m.mode||JSON.stringify(options)!==JSON.stringify(m.options))changed++;
 m.mode=s.mode;m.options=options;
}
const body=JSON.stringify(data,null,2)+'\n';
if(process.argv.includes('--check')){
 if(body!==original){console.error(`Served route controls RED: ${changed} changed selections or stale provenance`);process.exit(1);}
}else fs.writeFileSync(file,body);
console.log(`Served route controls: ${data.missions.length} exact-input accepted selections; ${changed} refreshed controls`);
