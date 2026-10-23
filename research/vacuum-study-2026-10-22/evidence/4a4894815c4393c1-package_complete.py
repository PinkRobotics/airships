"""Administrative file custody, execution closeout and final manifest; no scientific imports."""
import datetime as dt,hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parents[3]
checks=[]
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def pin(p,relative=False):
    h=hashlib.sha256();size=0
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk);size+=len(chunk)
    return dict(path=str(p.relative_to(R)) if relative else str(p),sha256=h.hexdigest(),bytes=size)
def dump(name,x):(R/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def check(name,ok,**kw):checks.append(dict(check=name,passed=bool(ok),**kw))
inputs=json.loads((R/'INPUTS.json').read_text());drift=[]
for x in inputs['pins']:
    src=Path(x['source']);copy=R/x['copy']
    if src.suffix.lower() in ['.py','.sh','.js','.ts','.ipynb']:raise RuntimeError('Owner executable input is forbidden')
    for kind,p in [('copy',copy),('source',src)]:
        got=pin(p);okay=got['sha256']==x['sha256'] and got['bytes']==x['bytes']
        check('input_'+kind,okay,path=str(p),required=kind=='copy')
        if kind=='source' and not okay:drift.append(dict(source=str(src),expected_sha256=x['sha256'],current=got,governing_copy=x['copy']))
dump('SOURCE-DRIFT.json',dict(at=stamp(),rows=drift,disposition='Pinned copies govern; live-source differences are recorded, not substituted.'))
check('no_owner_executables',inputs['owner_code_read'] is False and inputs['owner_code_executed'] is False)
executions=[];events=[];byseries={}
starts=sorted((R/'execution').glob('*/START.json'))
for start in starts:
    end=start.parent/'END.json';check('attempt_has_end',end.exists(),label=start.parent.name)
    if not end.exists():continue
    rec=json.loads(end.read_text());err=(end.parent/'stderr.log').read_text();label=end.parent.name
    admitted='simjob: ADMITTED' in err;released='reservation released' in err;refused='simjob: REFUSED' in err
    check('execution_released_or_not_started',(admitted and released) or (rec['returncode']==75 and refused and 'nothing was started' in err),label=label)
    failure=None
    if rec['returncode'] not in [0,75]:
        failure='missing_optional_ties' if "KeyError: 'ties'" in err else 'numpy_boolean_serialization' if 'not JSON serializable' in err else 'UNCLASSIFIED'
        check('failed_checker_attempt_explained',failure!='UNCLASSIFIED',label=label,failure=failure)
    command=rec['command']
    check('fixed_resources',command[command.index('--cores')+1]=='1' and command[command.index('--mem')+1]=='3G' and command[command.index('--timeout')+1]=='900',label=label)
    check('cpu_only_single_threads','CUDA_VISIBLE_DEVICES=' in command and all(x+'=1' in command for x in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS']),label=label)
    for sp in rec['source_pins']:
        snap=end.parent/'source'/Path(sp['path']).name;got=pin(snap)
        check('execution_source_snapshot',got['sha256']==sp['sha256'] and got['bytes']==sp['bytes'],label=label,path=str(snap))
    own_unit=re.search(r'simjob: ADMITTED (\S+\.scope)',err)
    entry=dict(label=label,returncode=rec['returncode'],admitted=admitted,released=released,refused=refused,failure=failure,unit=own_unit.group(1) if own_unit else None,receipt=rec,receipt_pin=pin(end),stderr_pin=pin(end.parent/'stderr.log'))
    executions.append(entry)
    if admitted:events.extend([(rec['started_utc'],1),(rec['ended_utc'],-1)])
    match=re.fullmatch(r'(.+)-retry(\d+)',label)
    if match:byseries.setdefault(match.group(1),[]).append(entry)
retry_checks=[]
for prefix,entries in byseries.items():
    entries.sort(key=lambda x:x['receipt']['started_utc'])
    for prev,nxt in zip(entries,entries[1:]):
        elapsed=(dt.datetime.fromisoformat(nxt['receipt']['started_utc'])-dt.datetime.fromisoformat(prev['receipt']['ended_utc'])).total_seconds()
        def normalized(cmd):return [v.split('=')[0]+'=PER_ATTEMPT_SCRATCH' if v.startswith(('TMPDIR=','MPLCONFIGDIR=','XDG_CACHE_HOME=')) else v for v in cmd]
        same=normalized(prev['receipt']['command'])==normalized(nxt['receipt']['command'])
        check('authorized_retry',prev['returncode']==75 and elapsed>=60 and same,series=prefix,elapsed_after_refusal_seconds=elapsed,payload_resources_same=same)
        retry_checks.append(dict(series=prefix,from_label=prev['label'],to_label=nxt['label'],elapsed_after_refusal_seconds=elapsed,payload_resources_same=same))
active=peak=0
for at,delta in sorted(events,key=lambda x:(x[0],x[1])):active+=delta;peak=max(peak,active)
check('own_cpu_cap',peak<=8 and active==0,peak_reserved_cores=peak,remaining=active)
status=subprocess.run(['ref-81e2f24e4e80426e80f0','unpublished-local-ref:6b66f99ebd630954','status'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=False)
(R/'FINAL-SIMJOB-STATUS.txt').write_text(status.stdout)
check('final_status_read',status.returncode==0)
for x in executions:
    if x['unit']:check('own_unit_not_live',x['unit'] not in status.stdout,unit=x['unit'])
dump('EXECUTION.json',dict(time_budget=None,timeout_is_technical_watchdog=True,retry_authority='ord-admiral-rr2-check048-resume-retry-1020',retry_interval_seconds=61,peak_reserved_own_cores=peak,live_own_jobs=0,admitted=sum(x['admitted'] for x in executions),refused=sum(x['refused'] for x in executions),failed_checker_attempts=sum(x['failure'] is not None for x in executions),successful_attempts=sum(x['returncode']==0 for x in executions),retries=retry_checks,attempts=executions))
for required in ['account-final','supplemental-corrected','thermal-resolved','extra-audits-v2','detail-validation','null-witness','summarize']+['full-v3-'+x for x in ['MLCCAg','CCAg','AgFEP05','AgFEP1']]:
    check('final_required_attempt_succeeded',any(x['label'].startswith(required+'-retry') and x['returncode']==0 and x['released'] for x in executions),prefix=required)
freezes=[]
for name in ['rpt-ref-29ebe6d900e7cbd982ea','rpt-ref-a53ddf165139979127c4']:
    report=W/'.ship/outbox'/(name+'.json');old=json.loads(report.read_text());records=[]
    for x in old['artifacts']:
        got=pin(Path(x['path']));okay=got['sha256']==x['sha256'] and got['bytes']==x['bytes'];check('prior_report_pin_unchanged',okay,path=x['path']);records.append(dict(path=x['path'],unchanged=okay))
    freezes.append(dict(report_pin=pin(report),checks=records))
partial=R.parent/'mainline048-independent-check-1020';manifest=json.loads((partial/'MANIFEST.json').read_text())
for x in manifest['files']:
    got=pin(partial/x['path']);check('partial_manifest_file_unchanged',got['sha256']==x['sha256'] and got['bytes']==x['bytes'],path=x['path'])
dump('PREVIOUS-FREEZE-CHECK.json',dict(reports=freezes,partial_manifest_files_checked=len(manifest['files']),all_unchanged=True))
dump('CODE.json',dict(owner_code_accessed=False,files=[dict(**pin(p),status='Own checker source; immutable per-attempt snapshots and execution outcomes establish used versions.') for p in sorted(R.glob('*.py'))]))
summary=json.loads((R/'SUMMARY.json').read_text());scope=json.loads((R/'SCOPE.json').read_text());detail=json.loads((R/'DETAIL-VALIDATION.json').read_text())
check('scientific_scope_complete',summary['checker_complete'] and scope['full_check_complete'])
check('main_search_agrees',not summary['search_mismatches'])
check('tight_witness_agrees',not detail['tight_mismatches'])
check('E_exclusions_agree',not summary['bound_exclusion_failures'])
check('exact_null_differences_retained',len(summary['extra_mismatches'])==24 and len(summary['null_field_witnesses'])==12)
check('report_body_limit',len((R/'REPORT-BODY.txt').read_text().split())<=250)
check('qualified_hull_value_null',scope['installed_hull_SF'] is None and summary['installed_hull_SF'] is None)
dump('WORK-END.json',dict(start=json.loads((R/'RESUME-START.json').read_text()),end_utc=stamp(),full_check_complete=True,time_budget=None,live_own_jobs=0,next='none',out_of_band_contact=False,owner_executable_access=False))
for p in sorted(R.glob('*.json')):
    if p.name in ['PACKAGE-CHECK.json','MANIFEST.json']:continue
    json.loads(p.read_text());check('final_json_parse',True,path=p.name)
files=[pin(p,relative=True) for p in sorted(R.rglob('*')) if p.is_file() and p not in [R/'MANIFEST.json',R/'PACKAGE-CHECK.json']]
dump('MANIFEST.json',dict(schema=1,root=str(R),files=files,excludes=['MANIFEST.json','PACKAGE-CHECK.json'],interpretation='Complete checker package; diagnostic and failed attempts remain identified. File custody does not establish physical qualification.'))
for x in files:
    check('final_manifest_pin',pin(R/x['path'],relative=True)==x,path=x['path'])
passed=all(x['passed'] for x in checks if x.get('required',True))
dump('PACKAGE-CHECK.json',dict(administrative_only=True,required_checks_passed=passed,all_checks_passed=all(x['passed'] for x in checks),live_source_drift_count=len(drift),checks=checks,manifest_pin=pin(R/'MANIFEST.json')))
if not passed:raise RuntimeError('Required package checks failed: '+str([x for x in checks if not x['passed'] and x.get('required',True)]))
print(json.dumps(dict(required_checks_passed=passed,checks=len(checks),input_pins=len(inputs['pins']),manifest_files=len(files),live_source_drift_count=len(drift),peak_own_cores=peak,attempts=len(executions),admitted=sum(x['admitted'] for x in executions),refused=sum(x['refused'] for x in executions),successful=sum(x['returncode']==0 for x in executions),failed=sum(x['failure'] is not None for x in executions),manifest_sha256=pin(R/'MANIFEST.json')['sha256'])))
