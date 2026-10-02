"""Visitor energy labels: rendered values, downloadable reports and negative controls.

This checks publication labels only. It neither repairs nor certifies the flight model.
Run directly for the energy portion of labelledcheck.
"""
from pathlib import Path
import functools
import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]
NOTE = ('These energy figures come from the earlier flight model, which understates the force '
        'needed to hold an empty hull down. Corrected figures will be higher, and some cycles '
        'may not be flyable as drawn.')
TAG = 'earlier model · under review'
ENERGY = re.compile(r'\b(?:MWh|kWh|MW|kW)\b|<!--f:[^>]*(?:energy\.|eCycleMWh|kwhPerTonne|\.battMWh|\.battMW|\.genMW)|charts/(?:ledger(?:-limit)?|deficit|sensitivity)\.pdf')

PROBE = r'''
(async () => {
  const NOTE=__NOTE__, TAG=__TAG__;
  for(let i=0;i<160;i++) {
    if (location.pathname.includes('notices') && document.querySelector('tbody tr')) break;
    if (location.pathname.includes('concept') && document.querySelector('#worked .stat')) break;
    if (location.pathname.includes('model-lab') && document.querySelector('#statebox b')) break;
    if (window.AIRSHIPS?.app?.ready) break;
    await new Promise(r=>setTimeout(r,250));
  }
  document.getElementById('introOv')?.click();
  for(const d of document.querySelectorAll('details')) d.open=true;
  if (window.AIRSHIPS?.app) { AIRSHIPS.app.paused=true; APP.selRow(0); }
  document.querySelectorAll('#wrenches button')[1]?.click();
  const mag=document.querySelector('#wmag');
  if(mag) { mag.value='30'; mag.dispatchEvent(new Event('input',{bubbles:true})); }
  await new Promise(r=>setTimeout(r,700));
  const norm=s=>s.replace(/\s+/g,' ').trim();
  function inspect() {
    const errors=[], figures=[], used=new Set();
    const body=norm(document.body.innerText);
    if(!body.includes(NOTE)) errors.push('view has no complete energy notice');
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    while(walker.nextNode()) {
      const node=walker.currentNode, el=node.parentElement;
      if(!/\b(?:MWh|kWh|MW|kW)\b/.test(node.textContent) || !el
         || el.closest('script,style,noscript,pre,code') || !el.getClientRects().length) continue;
      const block=el.closest('.stat,.b-row,dd,.a-row,p,[id^="opsN"],#sysDials,#statebox>b,#allocbox>b') || el;
      if(used.has(block)) continue;
      used.add(block); const text=norm(block.textContent);
      figures.push({block,text});
      if(!text.includes(TAG) && !text.includes(NOTE)) errors.push('unlabelled figure: '+text.slice(0,140));
    }
    const canvas=document.querySelector('#shipviz');
    if(canvas && canvas.getClientRects().length) {
      if(document.getElementById('shipvizEnergy')?.textContent.trim()!==TAG)
        errors.push('rotor-power canvas has no adjacent tag');
      if(!norm(canvas.closest('#cpLeft').textContent).includes(NOTE))
        errors.push('rotor-power view has no complete notice');
    }
    if(!figures.length) errors.push('no energy figures rendered; the view was not exercised');
    return {errors,figures};
  }
  const baseline=inspect();
  function removeText(needle,root) {
    const undo=[], w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
    while(w.nextNode()) {
      const n=w.currentNode;
      if(n.textContent.includes(needle)) { undo.push([n,n.textContent]); n.textContent=n.textContent.split(needle).join(''); }
    }
    return ()=>undo.forEach(([n,s])=>n.textContent=s);
  }
  let restore=removeText(NOTE,document.body), missingNotice=inspect().errors;
  restore();
  const compact=baseline.figures.find(f=>f.text.includes(TAG)&&!f.text.includes(NOTE));
  let missingTag=[];
  if(compact) {restore=removeText(TAG,compact.block);missingTag=inspect().errors;restore();}
  return JSON.stringify({errors:baseline.errors,figures:baseline.figures.map(f=>f.text.slice(0,100)),
    missingNoticeCaught:missingNotice.includes('view has no complete energy notice'),
    missingTagCaught:missingTag.some(e=>e.startsWith('unlabelled figure:'))});
})()
'''.replace('__NOTE__', json.dumps(NOTE)).replace('__TAG__', json.dumps(TAG))


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def report_labels():
    failures=[]; count=0
    for path in sorted((ROOT/'research/reports').glob('0[123]-*.md')):
        blocks=re.split(r'\n\s*\n',path.read_text())
        for i,block in enumerate(blocks):
            if not ENERGY.search(block): continue
            count+=1
            if NOTE not in block and (i+1==len(blocks) or blocks[i+1].strip()!=NOTE):
                failures.append(f'{path.relative_to(ROOT)}: energy block lacks its adjacent notice: {block[:60]}')
    for name in ('ledger','ledger-limit','deficit','sensitivity'):
        path=ROOT/'research/pdf/charts'/f'{name}.pdf'
        r=subprocess.run(['pdftotext',str(path),'-'],capture_output=True,text=True,check=True)
        text=' '.join(r.stdout.split())
        if NOTE not in text or TAG not in text:
            failures.append(f'{path.relative_to(ROOT)}: standalone energy chart lacks notice or tag')
    for path in sorted((ROOT/'research/pdf/out').glob('0[123]-*.pdf')):
        r=subprocess.run(['pdftotext',str(path),'-'],capture_output=True,text=True,check=True)
        if NOTE not in ' '.join(r.stdout.split()): failures.append(f'{path.relative_to(ROOT)}: PDF lacks energy notice')
    print(f'energy labels: {count} report energy blocks, four standalone charts and three report PDFs inspected')
    return failures


def check_energy_labels():
    failures=report_labels()
    # A new HTML surface containing energy units must join the rendered checks.
    known={'index.html','concept/index.html','model-lab/index.html','notices.html'}
    ignored={'tests','tools','inputs','series','shots','.git'}
    for path in ROOT.rglob('*.html'):
        rel=path.relative_to(ROOT)
        if any(p in ignored for p in rel.parts): continue
        if re.search(r'\b(?:MWh|kWh|MW|kW)\b',path.read_text()) and rel.as_posix() not in known:
            failures.append(f'{rel}: energy view is not registered for the rendered label check')
    handler=functools.partial(Handler,directory=str(ROOT))
    with socketserver.ThreadingTCPServer(('127.0.0.1',0),handler) as server:
        server.daemon_threads=True
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory(prefix='energy-labels-',dir=os.environ.get('TMPDIR')) as scratch:
                js=Path(scratch)/'probe.js';js.write_text(PROBE)
                for route in ('index.html?view=exercise&seed=7','concept/index.html','model-lab/index.html','notices.html'):
                    out=Path(scratch)/'view.json'
                    out.unlink(missing_ok=True)
                    r=subprocess.run([sys.executable,'tools/js_eval.py',f'http://127.0.0.1:{server.server_address[1]}/{route}',str(js),str(out),'5'],
                                     cwd=ROOT,capture_output=True,text=True,timeout=300)
                    if r.returncode or not out.exists():
                        failures.append(f'{route}: browser probe failed: '+(r.stdout+r.stderr)[-1000:]);continue
                    result=json.loads(out.read_text())
                    failures.extend(f'{route}: {e}' for e in result['errors'])
                    if not result['missingNoticeCaught']: failures.append(f'{route}: removing the notice was not detected')
                    if not result['missingTagCaught']: failures.append(f'{route}: removing one compact label was not detected')
                    print(f"energy labels: {route}: {len(result['figures'])} rendered energy blocks; "
                          f"missing-notice control {'caught' if result['missingNoticeCaught'] else 'MISSED'}, "
                          f"missing-tag control {'caught' if result['missingTagCaught'] else 'MISSED'}")
                    for figure in result['figures']: print('  '+figure)
        finally:
            server.shutdown();thread.join()
    if failures:
        raise ValueError('\n'.join(failures).replace(str(ROOT),'<repo>').replace(str(Path.home()),'<user>'))
    print('energy labels: PASS; notices and their negative controls hold')


if __name__=='__main__':
    try: check_energy_labels()
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        print('energy labels: FAIL\n'+str(exc),file=sys.stderr);sys.exit(1)
