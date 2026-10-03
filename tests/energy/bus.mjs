/* Independent bus sampler by muse-spark-1.3. */
import * as S from './observer-common.mjs';
import fs from 'node:fs';
const rows=[];let samples=0;
for(const {c,m,p,tag} of S.grid(S)){
 let worst={excess:-Infinity},overCount=0,unflaggedClip=0,minStore=Infinity,maxStore=0,back=0,cryo=0;
 // Periodic cycle: inventory at approach start is the preceding return's product.
 let store=p.ln2MakeT;
 for(const [id]of S.PHASES)for(let i=0;i<=768;i++){
  const q=S.drawAt(c,m,p,id,i/768),gross=S.sum(q.draw),supply=c.battMW+S.sum(q.gen),excess=gross-supply;
  samples++;if(excess>1e-8)overCount++;
  if(q.rotorAskMW>q.draw.rotors+1e-8&&!p.battLimited)unflaggedClip++;
  if(excess>worst.excess)worst={excess,id,prog:i/768,gross,supply,bus:q.busMW,draw:q.draw,gen:q.gen,ask:q.rotorAskMW};
  minStore=Math.min(minStore,q.ln2);maxStore=Math.max(maxStore,q.ln2);
  if(i<768){const t=S.drawAt(c,m,p,id,(i+.5)/768),dt=p.dur[id]/60/768;back+=(t.gen.regen||0)*dt;cryo+=(t.draw.cryo||0)*dt;}
 }
 rows.push({tag,battLimited:p.battLimited,overCount,unflaggedClip,minStore,maxStore,ln2MakeT:p.ln2MakeT,back,cryo,storeCreditCap:p.ln2MakeT*S.CFG.eLN2*S.CFG.rtLN2,excessReturn:back-cryo*S.CFG.rtLN2,worst});
}
console.log(JSON.stringify({samples,overloadCases:rows.filter(x=>x.overCount).length,unflaggedClippingCases:rows.filter(x=>x.unflaggedClip).length}));
if(rows.some(x=>x.overCount||x.unflaggedClip))throw new Error('bus sampler found an overload or unflagged clipping');
