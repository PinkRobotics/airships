/* Observer helpers from muse-spark-1.3. */
import fs from 'node:fs';
export * from '../../sim/index.js?v=b3bc1c96';
export const sum = o => Object.values(o).reduce((a,b)=>a+b,0);

export const winds = [null,{spd:40,dir:270,bearing:90},{spd:25,dir:90,bearing:90}];
export function* grid(S) { for(const c of Object.values(S.CLASSES)) for(const m of Object.values(S.MODES)) for(const km of [5,15,30,60,120]) for(const wind of winds) yield {c,m,km,wind,tag:`${c.id}/${m.id}/${km}/wind${wind?.spd||0}`,p:S.planCycle(c,m,km,wind)}; }
export function simpson(S,c,m,p,n=768) {
 const E={},chan={}; let back=0,hoist=0,peak=0;
 for(const [id] of S.PHASES) { E[id]=0; for(let i=0;i<=n;i++) {
  const q=S.drawAt(c,m,p,id,i/n), dt=p.dur[id]/60/n/3*(i===0||i===n?1:i%2?4:2);
  for(const [k,v] of Object.entries(q.draw)){E[id]+=v*dt;chan[k]=(chan[k]||0)+v*dt;}
  back+=(q.gen.regen||0)*dt; hoist+=q.hoistMW*dt;peak=Math.max(peak,q.draw.rotors);
 }}
 return {net:sum(E)-back,E,chan,back,hoist,peak};
}
