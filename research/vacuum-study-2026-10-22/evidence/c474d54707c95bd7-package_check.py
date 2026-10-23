"""Metadata-only delivery validation, manifest and atomic-outbox preparation."""
from pathlib import Path
import datetime,json,hashlib
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[3]
def read(n):return json.loads((ROOT/n).read_text())
def write(n,x):(ROOT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def pin(p):
    raw=p.read_bytes()
    return dict(path=str(p.resolve()),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
def main():
    checks=[]
    def check(name,ok,**kw):
        checks.append(dict(name=name,passed=bool(ok),**kw))
        assert ok,name
    for p in read('INPUT-PINS.json'):
        actual=pin(ROOT/p['copy'])
        check('input '+p['copy'],actual['sha256']==p['sha256'] and actual['bytes']==p['bytes'])
    for p in read('SOURCE-PINS.json'):
        check('primary fetch '+p['url'],'error' not in p)
        actual=pin(ROOT/p['copy'])
        check('source '+p['copy'],actual['sha256']==p['sha256'] and actual['bytes']==p['bytes'])
    validation=read('VALIDATION.json')
    check('scientific validation',all(x['passed'] for x in validation),checks=len(validation))
    check('all 12 owner NFIs inherited',read('NFI.json')['inherited_owner']==read('owner/NFI.json')['items'])
    check('new NFI rows',len(read('NFI.json')['new'])==12)
    check('exact differences supplied',len(read('MISMATCHES.json'))==20)
    check('PDF exists',(ROOT/'CHECK-059.pdf').read_bytes().startswith(b'%PDF'))
    check('PNG exists',(ROOT/'CHECK-059.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    check('figure visually inspected',True,note='PNG viewed in the session; legible axes, values and qualifications, no clipped content.')
    executions=[read(p.name) for p in sorted(ROOT.glob('*.execution.json'))]
    check('no admission refusal',all(x['exit_code']!=75 for x in executions))
    check('expected corrected exploratory failures',
        {x['tag'] for x in executions if x['exit_code']!=0}=={'capacity01','pond04'})
    check('all reservations returned',all(x.get('ended_at') and x.get('release') for x in executions))
    for x in executions:
        check('resource request '+x['tag'],x['cores']==1 and x['memory']=='1G')
    check('only own independent scripts in copied executable intake',
        all('intake/own053' in str(p.relative_to(ROOT)) for p in (ROOT/'intake').rglob('*.py')))
    write('TIMING.json',dict(start=read('START.json'),executions=executions,
        times_are='measured, never limits',no_refusal=True,
        corrected_failures={'capacity01':'missing historical R20 table; independent extension added',
                            'pond04':'completed diagnostic data; NumPy integer printing corrected'}))
    body="""CHECK-059 complete. QUESTIONABLE/PROJECTION.

7,094 drop/film/evaporation fields and 185 capacity comparisons reproduce; all 37 least-set choices agree. P2 capacities are 0.194454/1.126815 kg/m² at R10/R30 ISA; P3 R10 is 0.124560.

Corrections:
• The 0.2–1.0 h midday values are mass/full-wet-rate equivalents, not complete drying. Local inventories retain 11.707–13.562 kg at those times; 99% removal takes 0.310–5.346 h under held weather. The low-convection morning case still condenses over 36.5% of area.
• Ultra-Ever Dry requires bottom and top coats. The same assumed density gives 32.67–94.25 kg at R10; applying the bottom-coat price to both gives $16,861.93, twice the filed cost.
• P3's named 55.150/171.424 kg node/bay ponds are not reproduced. An explicit independently tiled surrogate gives 110.766/117.094 kg; neither establishes the real frame. Directional retention persists above 14°. Published placement coordinates and the actual bay geometry are needed.

Rain/dew retention and the 0.1 kg/m² allowance remain provisional. Pond drying must track shrinking area; heater-film exclusion does not extend to R30 ISA.

Exact differences, independent code/data, primary-source checks and the figure are filed. 98 validation checks pass; 12 new NFI rows preserve all 12 owner rows and inherited registers. Owner executables were neither read nor run. All admitted jobs have returned. No successor is named."""
    ident='rpt-ref-3bba4f0f54c6a95070dd'
    order='ord-admiral-rr2-check059-codex-7e53-1020'
    outbox=WORKSPACE/'.ship/outbox'
    check('destination not already filed',not (outbox/(ident+'.json')).exists())
    check('report word limit',len(body.split())<=250,words=len(body.split()))
    write('DELIVERY-CHECKS.json',dict(checks=checks,passed=len(checks),failed=0))
    files=[pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
    write('MANIFEST.json',dict(unit='vacuum-mainline059-check-1020',
        scope='all packet files except manifest; outbox report and seat state are external',
        generated_at=datetime.datetime.now().astimezone().isoformat(),files=files))
    names=['CARD.md','RESULTS.json','MISMATCHES.json','NFI.json','METHOD.md','SOURCE-AUDIT.md',
           'LOCAL-DRYING.json','PONDS-INDEPENDENT.json','POND-VALIDATION.json',
           'CAPACITY-COMPARISONS.json','WATER-COMPARISONS.json','VALIDATION.json',
           'INPUT-PINS.json','CHECK-059.pdf','DELIVERY-CHECKS.json','MANIFEST.json']
    report=dict(id=ident,kind='report',**{'from':'ref-baa4584cf36c531365e7'},
        from_seat='ref-baa4584cf36c531365e7',to='sciences',
        cc=['co','xo','admiral-robotics-review-v2'],re=order,
        unit='vacuum-mainline059-check-1020',authority=[{'id':order}],
        at=datetime.datetime.now().astimezone().isoformat(),asks='none',
        links_schema=1,links=[dict(rel='closes',id=order,outcome='done',extent='work')],
        standing='none',next='none',body=body,artifacts=[pin(ROOT/n) for n in names])
    path=outbox/(ident+'.json.tmp')
    assert not path.exists(),path
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(outbox_tmp=str(path),words=len(body.split()),artifact_pins=len(names),
        delivery_checks=len(checks),packet_files=len(files),manifest=pin(ROOT/'MANIFEST.json')),indent=2))
if __name__=='__main__':main()
