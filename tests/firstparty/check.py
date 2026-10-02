#!/usr/bin/env python3
"""Record CDP network events for every served HTML page in three mirror modes.

External attempts fail the test and are intercepted BEFORE transmission. This is crucial:
putting a removed agency fallback back must make a test red without loading that agency.
The server supplies dated local captures with fresh fixture envelopes; no live feed runs.
"""
import argparse
import asyncio
import contextlib
import http.server
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from static import ROOT, served_files
sys.path.insert(0, str(ROOT))
from pipeline.live import WIND_LATS, WIND_LONS, wind_grid


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    mode = 'fixture'
    wind_mode = 'fresh'
    note_variant = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *args): pass

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/index.html' and self.note_variant:
            inserted = {
                'module': '<script type="module" src="https://edge-module.invalid/beacon.js"></script>',
                'fetch': '<script>fetch("https://edge-fetch.invalid/ping").catch(() => {});</script>',
                # The browser's resource log is closed to new entries, then a foreign request is made
                # after the note has rendered once. Only the observer's own entries can show it.
                # The log is filled to its default size before the page's modules run: entries after that
                # were dropped where the note cannot see them, so it must not say the log is clean.
                'full': '<script>for(let i=0;i<260;i++){const x=new XMLHttpRequest();'
                        'x.open("GET","/sim/version.json?fill="+i,false);x.send();}</script>',
                'late': '<script>performance.setResourceTimingBufferSize(0);(function wait(){'
                        'const n=document.getElementById("firstPartyNote");'
                        'if(n&&n.textContent.indexOf("the site that served it")<0)'
                        'fetch("https://edge-late.invalid/ping").catch(()=>{});'
                        'else setTimeout(wait,50);})();</script>',
            }[self.note_variant]
            body = (ROOT / 'index.html').read_text().replace('</body>', inserted + '</body>').encode()
            self.send_response(200); self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        if path == '/__external_probe.html':
            body = b'<img src="https://firstparty-test.invalid/probe.png">'
            self.send_response(200); self.send_header('Content-Type', 'text/html'); self.end_headers(); self.wfile.write(body); return
        if path.startswith('/data/live/'):
            if self.mode == 'absent' or (path.endswith('/wind.json') and self.wind_mode == 'missing'):
                self.send_error(404); return
            now = datetime.now(timezone.utc).isoformat()
            snap = json.loads((ROOT / 'data/snapshot.json').read_text())
            if path.endswith('/fires.json'): data = snap['fires']
            elif path.endswith('/perims.json'): data = snap['perimeters']
            elif path.endswith('/heat.json'): data = json.loads((ROOT / 'data/snapshot-heat.json').read_text())
            elif path.endswith('/wind.json'):
                fixture = json.loads((Path(__file__).parent / 'fixtures/wind-response.json').read_text())
                data = wind_grid([fixture[i % 4] for i in range(25)])
                data['forecastAt'] = now
                if self.wind_mode == 'stale': now = '2000-01-01T00:00:00Z'
            else:
                self.send_error(404); return
            body = json.dumps({'fetchedAt': now, 'data': data}).encode()
            self.send_response(200); self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(body); return
        super().do_GET()


class Page:
    def __init__(self, ws, origin):
        self.ws, self.origin = ws, origin
        self.mid, self.pending, self.requests = 0, {}, []
        self.loaded = asyncio.Event()
        self.reader = asyncio.create_task(self.receive())

    def external(self, url):
        parts = urlsplit(url)
        return parts.scheme not in {'data', 'blob', 'about'} and (
            parts.scheme, parts.netloc) != ('http', self.origin)

    async def send(self, method, params=None, wait=True):
        self.mid += 1
        mid = self.mid
        future = asyncio.get_running_loop().create_future() if wait else None
        if future: self.pending[mid] = future
        await self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params or {}}))
        if future: return await asyncio.wait_for(future, 100)

    async def receive(self):
        async for raw in self.ws:
            msg = json.loads(raw)
            if 'id' in msg:
                future = self.pending.pop(msg['id'], None)
                if future and not future.done():
                    if 'error' in msg: future.set_exception(RuntimeError(str(msg['error'])))
                    else: future.set_result(msg.get('result', {}))
                continue
            method, params = msg.get('method'), msg.get('params', {})
            if method in {'Network.requestWillBeSent', 'Network.webSocketCreated'}:
                url = params.get('request', {}).get('url', params.get('url'))
                self.requests.append({'url': url, 'type': params.get('type', 'WebSocket'),
                                      'external': self.external(url)})
            elif method == 'Fetch.requestPaused':
                external = self.external(params['request']['url'])
                await self.send('Fetch.failRequest' if external else 'Fetch.continueRequest',
                                {'requestId': params['requestId'], **({'errorReason': 'BlockedByClient'} if external else {})},
                                wait=False)
            elif method == 'Page.loadEventFired': self.loaded.set()

    async def evaluate(self, expression):
        result = await self.send('Runtime.evaluate', {'expression': expression,
                                'awaitPromise': True, 'returnByValue': True})
        if result.get('exceptionDetails'): raise AssertionError(result['exceptionDetails'])
        return result.get('result', {}).get('value')

    async def navigate(self, url):
        self.requests = []; self.loaded.clear()
        await self.send('Page.navigate', {'url': url})
        await asyncio.wait_for(self.loaded.wait(), 90)


TRAP = """window.__firstpartyErrors=[];
addEventListener('error', e => { if(e.message) window.__firstpartyErrors.push(e.message); });
addEventListener('unhandledrejection', e => window.__firstpartyErrors.push(String(e.reason)));
"""
BOOT = """(async () => {
  const start = Date.now();
  while(Date.now()-start < 80000) {
    const s = window.AIRSHIPS?.app;
    if(s?.ready && s.windOk !== null) return true;
    await new Promise(r => setTimeout(r,100));
  }
  return false;
})()"""


async def note_cases(page, origin, shot_dir):
    async def note():
        return await page.evaluate("document.getElementById('firstPartyNote').textContent")

    async def wait_note(needle):
        for _ in range(100):
            value = await note()
            if needle in value: return value
            await asyncio.sleep(.1)
        raise AssertionError(f'first-party note did not say {needle!r}: {value!r}')

    async def screenshots(state):
        if not shot_dir: return
        import base64
        shot_dir.mkdir(parents=True, exist_ok=True)
        for width, height in ((1440, 900), (390, 844)):
            await page.send('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height,
                            'deviceScaleFactor': 1, 'mobile': width == 390})
            await page.evaluate("""(() => {
              document.getElementById('introOv')?.click();
              document.getElementById('layersPanel').style.display = 'flex';
              document.getElementById('firstPartyNote').scrollIntoView({block:'center'});
            })()""")
            await asyncio.sleep(.2)
            visible = await page.evaluate("""(() => {
              const r = document.getElementById('firstPartyNote').getBoundingClientRect();
              return r.width > 0 && r.height > 0 && r.top >= 0 && r.bottom <= innerHeight;
            })()""")
            assert visible, f'{state} note is outside {width}px screenshot'
            result = await page.send('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': False})
            (shot_dir / f'note-{state}-{width}.png').write_bytes(base64.b64decode(result['data']))
        await page.send('Emulation.clearDeviceMetricsOverride')

    Handler.mode, Handler.wind_mode, Handler.note_variant = 'fixture', 'fresh', None
    await page.navigate(f'http://{origin}/index.html?seed=7&data=snapshot')
    own = f"This page's own code talks only to {origin}."
    clean = await wait_note('shows no other host.')
    assert clean == f"{own} The browser's resource log for this page shows no other host.", clean
    print(f'note clean: {clean}')
    await screenshots('clean')

    await page.evaluate("performance.dispatchEvent(new Event('resourcetimingbufferfull'))")
    overflowed = await wait_note('is full')
    assert overflowed == (f"{own} The browser's resource log for this page is full; "
                          'other requests cannot be confirmed.'), overflowed
    await page.evaluate('performance.clearResourceTimings()')
    assert await note() == overflowed, 'clearing the log must not erase an observed overflow'
    print(f'note after buffer-full event: {overflowed}')

    before_mount = await page.evaluate("""(async () => {
      const {auditFirstPartyNote} = await import('./app/first-party-note.js?before-mount-test');
      performance.dispatchEvent(new Event('resourcetimingbufferfull'));
      performance.clearResourceTimings();
      const probe = document.createElement('p');
      auditFirstPartyNote(probe);
      return probe.textContent;
    })()""")
    assert before_mount == overflowed, before_mount
    print(f'note with event before mounting: {before_mount}')

    Handler.note_variant = 'module'
    await page.navigate(f'http://{origin}/index.html?seed=7&data=snapshot')
    module = await wait_note('edge-module.invalid')
    assert module == f'{own} Also requested in this browser: edge-module.invalid.', module
    assert any(r['url'].startswith('https://edge-module.invalid/') for r in page.requests), page.requests
    print(f'note injected module: {module}')
    await screenshots('edge')

    Handler.note_variant = 'fetch'
    await page.navigate(f'http://{origin}/index.html?seed=7&data=snapshot')
    fetched = await wait_note('edge-fetch.invalid')
    assert fetched == f'{own} Also requested in this browser: edge-fetch.invalid.', fetched
    assert any(r['url'].startswith('https://edge-fetch.invalid/') for r in page.requests), page.requests
    print(f'note injected fetch: {fetched}')

    Handler.note_variant = 'late'
    await page.navigate(f'http://{origin}/index.html?seed=7&data=snapshot')
    late = await wait_note('edge-late.invalid')
    assert late == (f'{own} Also requested in this browser: edge-late.invalid. '
                    "The browser's resource log for this page is full; other requests cannot be confirmed."), late
    assert any(r['url'].startswith('https://edge-late.invalid/') for r in page.requests), page.requests
    full = await page.evaluate(
        "performance.getEntriesByType('resource').some(e => e.name.includes('edge-late.invalid'))")
    assert full is False, 'the fixture did not close the resource log: the case proves nothing'
    print(f'note late request, resource log closed: {late}')

    Handler.note_variant = 'full'
    await page.navigate(f'http://{origin}/index.html?seed=7&data=snapshot')
    filled = await wait_note('is full')
    assert filled == (f"{own} The browser's resource log for this page is full; "
                      'other requests cannot be confirmed.'), filled
    print(f'note with the resource log full at start: {filled}')

    Handler.note_variant = None
    await page.send('Emulation.setScriptExecutionDisabled', {'value': True})
    try:
        await page.navigate(f'http://{origin}/index.html?seed=7&data=snapshot')
        static = await note()
        assert static == "This page's own code talks only to the site that served it.", static
        print(f'note scripts off: {static}')
    finally:
        await page.send('Emulation.setScriptExecutionDisabled', {'value': False})


async def session(ws_url, origin, records, evidence, note_evidence, note_only=False):
    import websockets
    async with websockets.connect(ws_url, max_size=64_000_000) as ws:
        page = Page(ws, origin)
        try:
            for domain in ('Page', 'Runtime', 'Network'): await page.send(domain + '.enable')
            await page.send('Network.setCacheDisabled', {'cacheDisabled': True})
            await page.send('Network.setBypassServiceWorker', {'bypass': True})
            await page.send('Fetch.enable', {'patterns': [{'urlPattern': '*'}]})
            await page.send('Page.addScriptToEvaluateOnNewDocument', {'source': TRAP})
            # Positive control: an external image must be recorded and blocked.
            await page.navigate(f'http://{origin}/__external_probe.html')
            await asyncio.sleep(.2)
            assert any(r['external'] for r in page.requests), f'network detector missed its external probe: {page.requests}'
            print('CDP detector control: external image recorded and blocked before transmission')
            if note_only:
                await note_cases(page, origin, note_evidence)
                return
            pages = [str(rel) for _, rel in served_files() if rel.suffix == '.html']
            for mode in ('fixture', 'snapshot', 'absent'):
                Handler.mode, Handler.wind_mode = mode, 'fresh'
                for path in pages:
                    query = '?seed=7' + ('&data=snapshot' if mode == 'snapshot' else '')
                    await page.navigate(f'http://{origin}/{path}{query}')
                    if path == 'index.html':
                        assert await page.evaluate(BOOT), f'{mode}: monitor failed to boot'
                        # Wait for the wind promise and lazy imports, then exercise refresh.
                        await page.evaluate("new Promise(r => setTimeout(r, 1000))")
                        state = await page.evaluate("({tier:AIRSHIPS.app.tier, wind:AIRSHIPS.app.windOk, still:document.getElementById('windNote').textContent})")
                        expected = {'fixture': 'mirror', 'snapshot': 'replay', 'absent': 'snapshot'}[mode]
                        assert state['tier'] == expected, state
                        assert state['wind'] == (mode == 'fixture'), state
                        if mode != 'fixture': assert 'Still air' in state['still'], state
                        # Stale and missing wind must erase previously applied wind.
                        if mode == 'fixture':
                            for wind_mode in ('stale', 'fresh', 'missing'):
                                Handler.wind_mode = wind_mode
                                state = await page.evaluate("""(async () => {
                                  const main = await import(document.querySelector('script[src*="app/main.js"]').src);
                                  await main.refresh();
                                  await new Promise(r=>setTimeout(r,600));
                                  const s=AIRSHIPS.app;
                                  return {ok:s.windOk, winds:s.missions.filter(m=>!m.idle&&m.wind).length,
                                          note:document.getElementById('windNote').textContent};
                                })()""")
                                assert state['ok'] == (wind_mode == 'fresh'), state
                                if wind_mode != 'fresh':
                                    assert state['winds'] == 0 and 'Still air' in state['note'], state
                            Handler.wind_mode = 'fresh'
                    # Trigger lazy images throughout the document, then settle imports/rendering.
                    await page.evaluate("""(async()=>{
                      for(let y=0;y<document.body.scrollHeight;y+=600) {
                        scrollTo(0,y); await new Promise(r=>setTimeout(r,30));
                      }
                      scrollTo(0,0); await new Promise(r=>setTimeout(r,1000));
                    })()""")
                    errors = await page.evaluate('window.__firstpartyErrors')
                    bad = [r for r in page.requests if r['external']]
                    records.append({'mode': mode, 'page': path, 'requests': list(page.requests), 'errors': errors})
                    print(f'{mode:8} {path:26} {len(page.requests):3} requests; {len(bad)} external; {len(errors)} script errors', flush=True)
                    assert not bad, bad
                    assert not errors, errors
                    if evidence and mode == 'snapshot' and path == 'index.html':
                        await page.evaluate("document.getElementById('introOv')?.click(); AIRSHIPS.app.follow=false; document.getElementById('btnFitFires').click()")
                        await asyncio.sleep(.2)
                        import base64
                        shot = await page.send('Page.captureScreenshot', {'format': 'png'})
                        evidence.with_suffix('.png').write_bytes(base64.b64decode(shot['data']))
            print(f'first-party browser: {len(records)} page/mode visits; zero third-party requests')
            await note_cases(page, origin, note_evidence)
        finally:
            page.reader.cancel()
            with contextlib.suppress(asyncio.CancelledError): await page.reader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, help='write the recorded request log and monitor screenshot')
    parser.add_argument('--note-evidence', type=Path, help='write clean and injected note screenshots at 1440 and 390 px')
    parser.add_argument('--note-only', action='store_true', help='run only the note cases')
    args = parser.parse_args()
    records = []
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'127.0.0.1:{server.server_port}'
    try:
        with tempfile.TemporaryDirectory(dir=os.environ.get('AIRSHIPS_TMPDIR'), ignore_cleanup_errors=True) as tmp:
            port = free_port()
            flags = ['--no-sandbox', '--disable-dev-shm-usage'] if os.environ.get('CI') else []
            proc = subprocess.Popen([os.environ.get('CHROME', 'chromium'), '--headless=new', '--disable-gpu',
                '--disable-background-networking', '--disable-component-update', '--no-first-run',
                '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--window-size=1600,1000',
                # Prevent accidental external transmission including workers or browser speculation.
                '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1',
                f'--remote-debugging-port={port}', f'--user-data-dir={tmp}/profile', *flags, 'about:blank'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                for _ in range(100):
                    try:
                        tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json', timeout=1))
                        ws_url = next(t['webSocketDebuggerUrl'] for t in tabs if t['type'] == 'page')
                        break
                    except Exception: time.sleep(.2)
                else: raise RuntimeError('Chromium did not expose a page')
                asyncio.run(session(ws_url, origin, records, args.evidence, args.note_evidence, args.note_only))
            finally:
                proc.terminate()
                try: proc.wait(timeout=8)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
    finally:
        server.shutdown(); server.server_close()
        if args.evidence: args.evidence.write_text(json.dumps(records, indent=2) + '\n')


if __name__ == '__main__': main()
