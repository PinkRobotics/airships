// Invented geometry only: a near bank is not a reachable drafting station.
import assert from 'node:assert/strict';
import test from 'node:test';
import {CLASSES, findSource, intakePoint, havKm, buildMission, stationFor} from '../../sim/index.js';
const fireLL = [0, 0], cls = CLASSES.P100;
const wide = [0.45, 0, 2000, 0, 'Invented wide lake',
  [[0.04,-1],[0.86,-1],[0.86,0],[0.86,1],[0.04,1],[0.04,0]]];
wide.spanKm = 112;
test('a near mapped shore cannot qualify stations outside the class radius', () => {
  const stations = [], intake = intakePoint(wide, fireLL, stations);
  assert.ok(Math.min(...wide[5].map(p => havKm(p, fireLL))) < cls.searchKm);
  assert.ok((stations.length ? stations : [intake]).every(p => havKm(p, fireLL) > cls.searchKm));
  assert.equal(findSource(fireLL, cls, [wide]), null);
});
test('a reachable control qualifies and its explanation names station and route distances', () => {
  const lake = [0.05,0,10,0,'Invented reachable lake',null];
  const src = findSource(fireLL, cls, [wide, lake]);
  assert.equal(src.idx, 1);
  assert.ok(src.km <= cls.searchKm);
  const fire = {id:'EX701',ll:fireLL,sizeHa:20,status:'Out of Control',ring:null};
  const m = buildMission(fire, [wide,lake], 'balanced', cls.id, {src,relaxed:false});
  assert.ok(m.stations.every(p => havKm(p, fireLL) <= cls.searchKm));
  assert.ok(havKm(stationFor(m,1),fireLL) <= cls.searchKm);
  assert.ok(Math.abs(src.km - havKm(m.intake,fireLL)) < 1e-9);
  assert.match(m.srcWhy, /station/i);
  assert.match(m.srcWhy, /mean planned leg/i);
});

test('fleet logistics ranks the mean station-to-drop-line leg', async () => {
  const {S,SIM,rebuildMissions}=await import('../../tests/node/operations-fleet-harness.mjs');
  SIM.setSeed(7);S.exerciseRegions=[];S.fires=[];
  S.water=[[0,50,2000,0,'Invented shared lake',null]];
  const make=(id,km)=>({id,name:id,ll:[0,50-km/111.19492664455873],sizeHa:10000,
    status:'Out of Control',exercise:true,note:false,ring:null});
  const edge=make('EX711',10),point=make('EX712',9.5);
  edge.ring=Array.from({length:200},(_,i)=>{
    const a=i/200*2*Math.PI,rad=Math.sqrt(edge.sizeHa*1e4/Math.PI)/1000;
    return [edge.ll[0]+Math.cos(a)*rad/(111.32*Math.cos(edge.ll[1]*Math.PI/180)),
      edge.ll[1]+Math.sin(a)*rad/110.57];
  });
  edge.ring.push(edge.ring[0]);S.fires=[edge,point];
  const c=SIM.CLASSES.P10000;
  const stationDistances=S.fires.map(f=>SIM.findSource(f.ll,c,S.water).km);
  const legs=S.fires.map(f=>SIM.buildMission({...f},S.water,'balanced',c.id,
    {src:SIM.findSource(f.ll,c,S.water),relaxed:false}).legKm);
  assert.ok(stationDistances[0]>stationDistances[1]);
  assert.ok(legs[0]<legs[1]);
  await rebuildMissions();assert.equal(S.missions[0].fire.id,edge.id);
});
