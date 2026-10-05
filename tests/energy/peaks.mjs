/* Dense independent peak observer by muse-spark-1.3. */
import * as S from './observer-common.mjs';
const result={};
for(const c of Object.values(S.CLASSES)) {
 const m=S.MODES.balanced,p=S.planCycle(c,m,15); let peak,ask,descent;
 for(const [id] of S.PHASES) for(let i=0;i<=10000;i++) {
  const prog=i/10000,q=S.drawAt(c,m,p,id,prog),o={id,prog,...q};
  if(!peak||q.draw.rotors>peak.draw.rotors)peak=o;
  if(!ask||q.rotorAskMW>ask.rotorAskMW)ask=o;
  if(q.vz<0&&(!descent||q.rotorAskMW>descent.rotorAskMW))descent=o;
 }
 const cruise=S.drawAt(c,m,p,'OUTBOUND_TRANSIT',.5),r=S.simpson(S,c,m,p,6144);
 result[c.id]={c,p,peak,ask,descent,cruise,integral:r};
 console.log(`${c.id} publishedPeak=${p.downMW.toFixed(6)} densePeak=${peak.draw.rotors.toFixed(6)} phase=${peak.id} prog=${peak.prog} ask=${ask.rotorAskMW.toFixed(6)} askPhase=${ask.id} vz=${peak.vz.toFixed(6)} hoist=${r.hoist.toFixed(9)} MWh`);
}
for(const r of Object.values(result))if(Math.abs(r.p.downMW-r.peak.draw.rotors)>1e-5)throw new Error('dense peak differs from reported peak');

await import("./signed-authority.mjs");
