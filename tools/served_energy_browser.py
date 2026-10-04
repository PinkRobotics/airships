import asyncio,base64,json,os,sys,tempfile,time
from pathlib import Path
import websockets
sys.path.insert(0,str(Path.cwd()/'tools'))
from serve import serve_tree
from devtools import page_target
ROOT=Path(__file__).resolve().parent.parent;
OUT=Path(sys.argv[sys.argv.index('--output')+1]) if '--output' in sys.argv else Path(tempfile.mkdtemp(prefix='served-energy-',dir=os.environ.get('TMPDIR')))
OUT.mkdir(parents=True,exist_ok=True)
async def probe(wsurl,base,page,width,stem):
 async with websockets.connect(wsurl,max_size=30_000_000) as ws:
  serial=0;errors=[]
  async def call(method,params=None):
   nonlocal serial
   serial+=1;want=serial;await ws.send(json.dumps(dict(id=want,method=method,params=params or {})))
   while True:
    msg=json.loads(await ws.recv())
    if msg.get('method')=='Runtime.exceptionThrown':errors.append(msg['params'])
    if msg.get('method')=='Fetch.requestPaused':
     p=msg['params'];url=p['request']['url'];allowed=url.startswith(base) or url.startswith(('data:','blob:'))
     serial+=1;await ws.send(json.dumps(dict(id=serial,method='Fetch.continueRequest' if allowed else 'Fetch.failRequest',params=dict(requestId=p['requestId'],**({} if allowed else dict(errorReason='BlockedByClient'))))))
    if msg.get('id')==want:
     if 'error' in msg:raise RuntimeError(str(msg['error']))
     return msg.get('result',{})
  await call('Page.enable');await call('Runtime.enable');await call('Fetch.enable',dict(patterns=[dict(urlPattern='*')]))
  await call('Emulation.setDeviceMetricsOverride',dict(width=width,height=1000,deviceScaleFactor=1,mobile=width<500))
  await call('Emulation.setEmulatedMedia',dict(features=[dict(name='prefers-reduced-motion',value='reduce')]))
  await call('Page.navigate',dict(url=base+page));await asyncio.sleep(2)
  result=await call('Runtime.evaluate',dict(expression=(ROOT/'tests/served-energy/page.js').read_text(),returnByValue=True,awaitPromise=True))
  (OUT/(stem+'.json')).write_text(json.dumps(dict(result=result,errors=errors),indent=2)+'\n')
  if 'exceptionDetails' in result:raise RuntimeError(str(result['exceptionDetails'])[:1200])
  await call('Runtime.evaluate',dict(expression="document.getElementById('introOv')?.click();document.getElementById('worked')?.scrollIntoView({block:'center'});",returnByValue=True))
  await asyncio.sleep(.3)
  if '--pictures' in sys.argv:
   shot=await call('Page.captureScreenshot',dict(format='png'));(OUT/(stem+'.png')).write_bytes(base64.b64decode(shot['data']))
  value=result['result']['value'];print(stem,'feasible rows',len(value['rows']),'first/total/slowest ms',*[round(value['timing'][k],1) if value['timing'][k] is not None else None for k in ['firstPlanMs','totalMs','slowestMissionMs']],flush=True)
  return value
with serve_tree(ROOT) as base:
 results=[]
 for page,width,stem in [('index.html?view=exercise',1440,'exercise-1440'),('index.html?day=2026-09-22',1440,'replay-1440'),('index.html?view=exercise',390,'exercise-390'),('index.html?day=2026-09-22',390,'replay-390'),('concept/index.html',1440,'concept-1440')]:
  if '--view' in sys.argv and stem!=sys.argv[sys.argv.index('--view')+1]:continue
  with tempfile.TemporaryDirectory(prefix='served-probe-',dir=os.environ['TMPDIR'],ignore_cleanup_errors=True) as temp:
   with page_target('/snap/bin/chromium',['--no-sandbox','--disable-dev-shm-usage','--use-angle=swiftshader','--enable-unsafe-swiftshader'],Path(temp)/'profile') as (proc,url):
    print('owned browser PID',proc.pid,stem,flush=True);results.append(asyncio.run(probe(url,base,page,width,stem)))
 (OUT/'inventory.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS browser audit; owned browser groups and server closed',flush=True)
