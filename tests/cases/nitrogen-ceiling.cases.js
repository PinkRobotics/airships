import {describe,it,ok,close,eq} from '../harness.js';
import * as S from '../../sim/index.js';

describe('declared nitrogen recovery ceiling',()=>{
  it('holds recovered work across all nitrogen-control pairs, including both extremes',()=>{
    const prior={eLN2:S.CFG.eLN2,rtLN2:S.CFG.rtLN2};
    const ceiling=173.4; // Arnaiz-del-Pozo et al. (2020), printed p. 8; declared model limit.
    const plan={ln2MakeT:1,dur:{SOURCE_APPROACH:60,WATER_FILL:60}};
    let pairs=0,maximum=0;
    try {
      S.setConfig({eLN2:.8,rtLN2:.38}); // Planted exposed upper pair before the range sweep.
      const planted=S.regenMW({...S.CLASSES.P100,genMW:1e6},plan,'WATER_FILL')/S.ventTph(plan,'WATER_FILL')*1000;
      ok(planted<=ceiling+1e-10,`planted upper pair: ${planted} kWh/t exceeds ${ceiling}`);
      for(let e=30;e<=80;e+=5)for(let rt=10;rt<=38;rt+=2){
        S.setConfig({eLN2:e/100,rtLN2:rt/100});pairs++;
        for(const cls of Object.values(S.CLASSES))for(const phase of ['SOURCE_APPROACH','WATER_FILL']){
          // Make the generator nonbinding: its rating must not hide a per-tonne violation.
          const c={...cls,genMW:1e6},flow=S.ventTph(plan,phase);
          const recovered=S.regenMW(c,plan,phase)/flow*1000;
          maximum=Math.max(maximum,recovered);
          ok(recovered<=ceiling+1e-10,`${cls.id}: eLN2=${e/100}, rtLN2=${rt/100}: ${recovered} kWh/t exceeds ${ceiling}`);
          close(recovered,Math.min(e*rt/10,ceiling),1e-10,'recovery is the smaller of requested work and declared ceiling');
          const limited={...c,genMW:.01};
          ok(S.regenMW(limited,plan,phase)<=limited.genMW,'generator rating also holds');
        }
      }
      eq(pairs,165,'all selectable pairs, including endpoints');
      close(maximum,ceiling,1e-10,'upper pair reaches declared ceiling');
      S.setConfig({eLN2:S.DEFAULTS.eLN2,rtLN2:S.DEFAULTS.rtLN2});
      close(S.regenMW({...S.CLASSES.P100,genMW:1e6},plan,'WATER_FILL')/S.ventTph(plan,'WATER_FILL')*1000,90,1e-10,'default recovery unchanged');
    } finally { S.setConfig(prior); }
  });
});
