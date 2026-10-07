// Invented incidents, water and exclusion only; the real allocator and route guard run.
import assert from 'node:assert/strict';
import test from 'node:test';
import {S,SIM,rebuildMissions} from '../../tests/node/operations-fleet-harness.mjs';
const fire=(id,ll,sizeHa)=>({id,name:id,ll,sizeHa,status:'Out of Control',exercise:true,note:false,ring:null});
const inputs=[fire('EX900',[-4,50],100000),...Array.from({length:20},(_,i)=>fire('EX'+String(i+1).padStart(3,'0'),[i*.001,50],10000-i))];
function reset(regions){
  SIM.setSeed(7);S.fires=structuredClone(inputs);S.exerciseRegions=regions;
  S.water=[[-4.02,50,2000,0,'Invented blocked lake',null],[-.02,50,2000,0,'Invented clear lake',null]];
}
test('refusal-first dispatch retains the same hull slot for an eligible route', async () => {
  reset([{kind:'place',who:'Invented exclusion',ll:[-4,50],rKm:10}]);
  await rebuildMissions();
  assert.equal(S.fires.filter(f=>f.heldOut).length,1);
  assert.equal(S.fires[0].mission,null);
  assert.match(S.fires[0].heldOut,/Invented exclusion/);
  assert.equal(S.missions.length,16);
  assert.equal(S.missions.filter(m=>!m.idle).length,16);
  assert.equal(S.uncovered,5);
  assert.equal(S.missions[0].hullNo,1);
  assert.equal(new Set(S.missions.map(m=>m.name)).size,16);
  assert.ok(S.missions.every(m=>!SIM.missionBlocked(S.regions,m)));
});
test('dispatch without an exclusion still fills the same fixed pool', async () => {
  reset([]);await rebuildMissions();
  assert.equal(S.missions.length,16);assert.equal(S.uncovered,5);
  assert.equal(S.fires.filter(f=>f.heldOut).length,0);
});
