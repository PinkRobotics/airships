/* Dated report readings beside an exact current bag-intervention replay. */
import fs from 'node:fs';
import {CLASSES,MODES,planCycle,LN2_RECOVERY_KWH_PER_T} from '../../sim/index.js?v=01e992e3';
import {writeGenerated} from './energy-output.mjs';
const recordPath='research/analysis/energy-report-percentages.json';
const papers=['research/reports/02-paper.md','research/reports/03-diligence.md'];
const one=(text,pattern)=>{const hits=[...text.matchAll(pattern)];if(hits.length!==1)throw new Error(`Expected one dated report comparator: ${pattern}`);return hits[0];};
function historicalReadings(){
 const texts=papers.map(p=>fs.readFileSync(p,'utf8'));
 const dates=texts.map(t=>one(t,/Pink Robotics · (\d{4}-\d{2}-\d{2}) · v1/g)[1]);
 const letdown=one(texts[1],/from ([\d.]+) MWh to ([\d.]+) →[^\n]+ — (\d+)%/g);
 const rotor=one(texts[0],/model's assumed [^\n]+gave a stated (\d+)% reduction;[\s\S]*?Its comparison was ([\d,]+) MW to ([\d.]+) →[^\n]+/g);
 const bag=one(texts[0],/attributed a ([\d.]+) MWh penalty to removing it, against ([\d.]+) →[^\n]+That earlier (\d+)% saving/g);
 const more=one(texts[1],/does not need, costs (\d+)% more energy per cycle/g);
 return {letdown:{source:papers[1],published:dates[1],withoutMWh:Number(letdown[1]),withMWh:Number(letdown[2]),reportedReductionPct:Number(letdown[3])},
  rotor:{source:papers[0],published:dates[0],withoutMW:Number(rotor[2].replaceAll(',','')),withMW:Number(rotor[3]),reportedReductionPct:Number(rotor[1])},
  bag:{source:papers[0],published:dates[0],reportedPenaltyMWh:Number(bag[1]),withMWh:Number(bag[2]),reportedSavingPct:Number(bag[3]),
   diligenceSource:papers[1],diligencePublished:dates[1],diligenceReportedIncreasePct:Number(more[1]),
   qualification:'These are retained report readings. No historical model replay was reconstructed, and these printed energy comparators do not substantiate either reported bag percentage.'}};
}
export function generateReportPercentages(){
 const input={class:'P100',km:15,basis:'record',mode:'balanced',options:{basis:'record'}};
 const c=CLASSES[input.class],m=MODES[input.mode];
 const withBag=planCycle(c,m,input.km,null,input.options);
 const hardware={anchorM:0,anchorBagT:0};
 const withoutBag=planCycle({...c,...hardware},m,input.km,null,input.options);
 const reading=p=>({suppliedMWh:p.eCycleMWh,feasible:p.feasible,worst:p.worst});
 const bigInput={class:'P10000',km:15,basis:'record',mode:'balanced',options:{basis:'record'}};
 const big=planCycle(CLASSES.P10000,MODES.balanced,bigInput.km,null,bigInput.options);
 return {generator:'research/analysis/energy-report-percentages.mjs',historical:historicalReadings(),
  replay:{input,intervention:{hardware,definition:'Remove the bag and its cable; retain every other class and configuration input. Still air.'},withBag:reading(withBag),withoutBag:reading(withoutBag),
   increasePct:100*(withoutBag.eCycleMWh/withBag.eCycleMWh-1),denominator:'with-bag supplied MWh',
   qualification:'Both force verdicts are reported. An unsupported path supplies no achieved cycle or demonstrated energy saving.'},
  letdown:{input:bigInput,suppliedMWh:big.letdownMWh,feasible:big.feasible},nitrogenRecoveryCeilingKWhPerT:LN2_RECOVERY_KWH_PER_T};
}
export function reportCorrection(r){
 const h=r.historical,b=r.replay,f=(x,n=3)=>Number(x).toFixed(n),v=p=>p.feasible?'closes':'does not close';
 return `### Dated percentages and the current bag replay\n\n`+
  `The following older percentage language is retained as a report reading, with its original comparator. It does not apply to the current values at the right of the arrows.\n\n`+
  `- Report dated ${h.letdown.published}: P-10000 letdown ${f(h.letdown.withoutMWh,2)} → ${f(h.letdown.withMWh)} MWh, reported ${h.letdown.reportedReductionPct}% reduction.\n`+
  `- Report dated ${h.rotor.published}: P-10000 rotor power ${f(h.rotor.withoutMW,0)} → ${f(h.rotor.withMW,1)} MW, reported ${h.rotor.reportedReductionPct}% reduction.\n`+
  `- Reports dated ${h.bag.published}: P-100 reported bag-removal penalty ${f(h.bag.reportedPenaltyMWh)} MWh, against ${f(h.bag.withMWh)} MWh with it; the paper reported ${h.bag.reportedSavingPct}% saving and the diligence report reported ${h.bag.diligenceReportedIncreasePct}% more without the bag. ${h.bag.qualification}\n\n`+
  `Current named replay: ${b.input.class}, ${b.input.mode}, ${b.input.km} km one-way, ${b.input.basis} basis, still air. ${b.intervention.definition} With the bag: ${f(b.withBag.suppliedMWh,6)} MWh, ${v(b.withBag)}; without the bag: ${f(b.withoutBag.suppliedMWh,6)} MWh, ${v(b.withoutBag)}. The supplied-effort increase is ${f(b.increasePct,4)}%, using ${b.denominator}. ${b.qualification}\n\n`+
  `Current P-10000 prescribed ${r.letdown.input.km} km ${r.letdown.input.basis} letdown: ${f(r.letdown.suppliedMWh,6)} MWh; the cycle ${r.letdown.feasible?'closes':'does not close'}. No current letdown saving is inferred from the dated comparator.\n\n`+
  `The model now holds nitrogen recovery to ${f(r.nitrogenRecoveryCeilingKWhPerT,1)} kWh/t, the cited medium-pressure pure-nitrogen feed at 4 bar and feed/product flow-exergy difference, not measured airborne recovery. Averaged sunlight enters instantaneous bus power and force closure; the [zero-sunlight sensitivity](../../docs/ENERGY-CLOSURE-2026-10.md#zero-sunlight-sensitivity-of-the-selected-profiles) replays fixed selected controls. No night search was run.\n\n`+
  `Record and generator: \`research/analysis/energy-report-percentages.json\` and \`research/analysis/energy-report-percentages.mjs\`.\n`;
}
export function reportModelQualification(r){
 return `**Current model qualification of the adjacent dated sections.** Nitrogen recovery is held to ${Number(r.nitrogenRecoveryCeilingKWhPerT).toFixed(1)} kWh/t in the model. Its source is the medium-pressure pure-nitrogen feed at 4 bar and feed/product flow-exergy difference in [Arnaiz-del-Pozo et al.](https://doi.org/10.3390/e22090959), printed pp. 6 and 8. The earlier state description and airborne-expander estimate below are withdrawn: the cited comparator is neither a universal liquid-exergy value nor measured airborne recovery. The shared power model limits requested recovered work per tonne before the generator cap; tests cover every selectable control pair, including both extremes.\n\n`+
  `Averaged sunlight is credited to instantaneous bus power before rotor allocation, so it enters force closure as well as energy accounting. The adjacent older statements that solar cannot affect published ledger results are withdrawn. The [generated zero-sunlight sensitivity](../../docs/ENERGY-CLOSURE-2026-10.md#zero-sunlight-sensitivity-of-the-selected-profiles) holds selected controls and collecting area fixed. No night search was run; it does not show that no profile closes at night.\n`;
}
if(process.argv[1]?.endsWith('energy-report-percentages.mjs')){
 const result=generateReportPercentages();writeGenerated(recordPath,JSON.stringify(result,null,2)+'\n');
 console.log(`${process.argv.includes('--check')?'PASS':'Generated'} dated report percentages: named P100 balanced 15 km record replay; with bag ${result.replay.withBag.suppliedMWh}, without bag ${result.replay.withoutBag.suppliedMWh} MWh; increase ${result.replay.increasePct}%; force verdicts ${result.replay.withBag.feasible}/${result.replay.withoutBag.feasible}`);
}
