import fs from 'node:fs';
import {profileKey} from './energy-printed-profiles.mjs';
import {STORAGE_PROFILE_NOTE} from '../../sim/energy-label.js?v=01e992e3';
const record=JSON.parse(fs.readFileSync('research/analysis/energy-necessary.json'));
const results=new Map(record.routes.map(r=>[profileKey(r),r]));
export function storageNote(input){
 const r=results.get(profileKey(input));
 if(!r)throw new Error('Printed profile has no necessary-energy result: '+profileKey(input));
 if(r.accounting.shortageMWh<=1e-6)return '';
 return r.quasiStaticFeasible?STORAGE_PROFILE_NOTE.replace('one ideal cycle','an ideal cycle'):'unsupported profile; exceeds nominal storage in an ideal cycle';
}
export function storageSummary(input){
 const r=results.get(profileKey(input));storageNote(input);
 return r.accounting;
}
