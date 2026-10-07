// Invented source pairs check the explanation against accepted plans in both directions.
import assert from 'node:assert/strict';
import test from 'node:test';
import {CLASSES,assign,findSource,buildMission,bindServedMission,setSeed} from '../../sim/index.js';
const fire={id:'EX901',exercise:true,ll:[0,50],sizeHa:100,note:false,status:'Out of Control',ring:null};
const lake=(km,ha)=>[0,50+km/111.19492664455873,ha,0,'Invented source',null];
for(const [near,far,label,smallerFaster] of [[3,60,'control',true],[10,41,'counterexample',false]]){
  test(`distance-rule reason remains true for the ${label}`, () => {
    setSeed(7);const water=[lake(near,10),lake(far,100)],a=assign(fire,water);
    assert.equal(a.cls.id,'P100');
    const rates=['P100','P1000'].map(id=>{
      const src=findSource(fire.ll,CLASSES[id],water);
      const m=buildMission(structuredClone(fire),water,'balanced',id,{src,relaxed:false});
      assert.equal(bindServedMission(m,'balanced').state,'ready');return m.plan.tph;
    });
    assert.equal(rates[0]>rates[1],smallerFaster);
    assert.doesNotMatch(a.why,/more water per hour|logistics decide/i);
    assert.match(a.why,/distance rule/i);
    assert.match(a.why,/40 km/);assert.match(a.why,/three times/);
    console.log(`${label}: accepted release rates ${rates.map(n=>n.toFixed(3)).join(' / ')} t/h`);
  });
}
