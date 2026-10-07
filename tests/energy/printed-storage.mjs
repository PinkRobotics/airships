/* Refuse missing results or a mismatched shortage note in any current producer. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {profileKey,printedProfiles} from '../../research/analysis/energy-printed-profiles.mjs';
import {storageNote} from '../../research/analysis/energy-storage-notes.mjs';
const record=JSON.parse(fs.readFileSync('research/analysis/energy-necessary.json'));
const results=new Map(record.routes.map(r=>[profileKey(r),r]));
assert.equal(results.size,record.routes.length,'deduplicated storage results');
for(const r of printedProfiles()){
 const n=results.get(profileKey(r));assert.ok(n,'every printed current input has storage accounting');
 assert.equal(storageNote(r).includes('exceeds nominal storage'),n.accounting.shortageMWh>1e-6,'shortage note matches accounting');
}
// The freshly emitted force table is independently bound to the storage record.
const forceRows=JSON.parse(fs.readFileSync('research/analysis/energy-served-inertia.json')).rows;
for(const r of forceRows)assert.ok(results.has(profileKey({class:r.class,km:r.km,mode:r.controls.mode,options:{...r.controls.options,basis:r.basis}})),
 'every emitted current candidate-force row has exact-input storage accounting');
let count=0,shortages=0;
for(const row of JSON.parse(fs.readFileSync('research/analysis/energy-feasible.json')).rows)
 for(const b of [row.best,row.fullDeliveryBest].filter(Boolean)){
  count++;const n=results.get(profileKey(b));assert.ok(n,'golden-distance profile is covered');
  if(n.accounting.shortageMWh>1e-6){shortages++;assert.ok(storageNote(b));}
 }
const study=fs.readFileSync('research/analysis/payload-exchange.md','utf8');
for(const header of ['| class, km | hover bound','| class | push down, empty at the lake','| pair | closes | delivered']){
 const start=study.indexOf(header),block=study.slice(start,study.indexOf('\n\n',start));
 assert.ok(start>=0,'excluded study population is named');
 for(const row of block.split('\n').slice(2))assert.ok(row.includes('outside: separate study sketch'),'excluded study row states scope');
}
// These comparisons independently rerender all printed notes from exact input identities.
for(const producer of ['energy-tables','energy-unheld','energy-motion','energy-descent']){
 const run=spawnSync(process.execPath,[`research/analysis/${producer}.mjs`,'--check'],{encoding:'utf8'});
 assert.equal(run.status,0,run.stdout+run.stderr);
}
console.log(`PASS printed storage coverage: ${results.size} unique current profiles; golden ${count}/${count}, ${shortages} shortages; every generated table note matches`);
