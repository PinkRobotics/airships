"""Current energy publication: accepted plans, complete unavailable states, dated history.

The earlier global interim notice is retired. Feasibility and rendered quantities belong
with servedenergycheck; this gate checks the publication boundary and its negative controls.
"""
from pathlib import Path
import json,os,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from serve import serve_tree
OLD='earlier model · under review'
CURRENT=('index.html','concept/index.html','model-lab/index.html','notices.html')
PROBE=r'''
(async()=>{
 for(let i=0;i<200;i++){
  if(location.pathname.includes('notices')&&document.querySelector('tbody tr'))break;
  if(location.pathname.includes('concept')&&window.AIRSHIPS?.concept?.workedSelection)break;
  if(location.pathname.includes('model-lab')&&document.querySelector('[data-energy-unavailable]'))break;
  if(window.AIRSHIPS?.app?.ready)break;
  await new Promise(r=>setTimeout(r,100));
 }
 document.getElementById('introOv')?.click();
 const unavailable=()=>{
  const errors=[];
  for(const el of document.querySelectorAll('[data-energy-unavailable]')){
   const text=el.textContent;
   if(!/mission energy (?:supply and demand|bus balance)/i.test(text)||!/unavailable/i.test(text)||!/no mission energy record/i.test(text))errors.push('incomplete unavailable quantity: '+text);
  }
  return errors;
 };
 const errors=unavailable();
 if(document.body.innerText.includes('earlier model · under review'))errors.push('superseded interim label is rendered');
 const A=window.AIRSHIPS;
 if(A?.app){
  for(const m of A.app.missions)A.sim.auditServedPlan(m.cls,m.legKm,m.wind,m.selection,m.mode.id);
 }else if(A?.concept){const w=A.concept.workedSelection;A.sim.auditServedPlan(A.sim.CLASSES[w.cls],w.km,null,w.selection,w.selection.mode);}
 else if(location.pathname.includes('notices')&&!document.body.innerText.includes('not accepted mission results'))errors.push('source records lack their publication class');
 let controls=[];
 const fixture=document.createElement('p');fixture.dataset.energyUnavailable='true';document.body.append(fixture);
 for(const text of ['123 MW','Mission energy bus balance unavailable','Bus balance: no mission energy record']){
  fixture.textContent=text;const red=unavailable();controls.push({text,caught:red.length>0});
 }
 fixture.textContent='Mission energy bus balance unavailable: no mission energy record';
 if(unavailable().length)errors.push('complete unavailable fixture refused');
 fixture.remove();
 return {errors,controls,unavailable:document.querySelectorAll('[data-energy-unavailable]').length};
})()
'''
def report_boundary():
 failures=[]
 for p in sorted((ROOT/'research/reports').glob('0[123]-*.md')):
  text=p.read_text();preface=text.split('<!--tex:skip-->')[0]
  if 'Energy reading, 2026-10-02' not in preface or 'superseded' not in preface or 'do not establish delivery' not in preface:
   failures.append(str(p.relative_to(ROOT))+': historical report lacks its superseded energy boundary')
 for name in ('ledger','ledger-limit','deficit','sensitivity'):
  p=ROOT/'research/pdf/charts'/f'{name}.pdf'
  text=subprocess.check_output(['pdftotext',str(p),'-'],text=True)
  if 'Diagnostic analysis' not in text or OLD in text:failures.append(str(p.relative_to(ROOT))+': energy chart lacks its diagnostic class')
 return failures

def check_energy_labels():
 failures=report_boundary()
 for f in CURRENT:
  if OLD in (ROOT/f).read_text():failures.append(f+': superseded interim label remains')
 with serve_tree(ROOT) as base:
  with tempfile.TemporaryDirectory(prefix='energy-labels-',dir=os.environ.get('TMPDIR'),ignore_cleanup_errors=True) as scratch:
   js=Path(scratch)/'probe.js';js.write_text(PROBE)
   for route in ('index.html?view=exercise','index.html?day=2026-09-22','concept/index.html','model-lab/index.html','notices.html'):
    out=Path(scratch)/'view.json';out.unlink(missing_ok=True)
    r=subprocess.run([sys.executable,'tools/js_eval.py',base+route,str(js),str(out),'5'],cwd=ROOT,capture_output=True,text=True,timeout=300)
    if r.returncode or not out.exists():failures.append(route+': browser probe failed: '+(r.stdout+r.stderr)[-1000:]);continue
    result=json.loads(out.read_text());failures.extend(route+': '+e for e in result['errors'])
    for control in result['controls']:
     if not control['caught']:failures.append(route+': unavailable negative control missed: '+control['text'])
    print('energy boundary:',route,':',len(result['errors']),'errors;',len(result['controls']),'unavailable controls RED;',result['unavailable'],'labelled unavailable states')
 if failures:raise ValueError('\n'.join(failures).replace(str(ROOT),'<repo>').replace(str(Path.home()),'<user>'))
 print('energy boundary: PASS; accepted-plan provenance, complete unavailable labels, source comparisons and dated diagnostic history')
if __name__=='__main__':
 try:check_energy_labels()
 except (ValueError,OSError,subprocess.SubprocessError) as exc:print('energy boundary: FAIL\n'+str(exc),file=sys.stderr);sys.exit(1)
