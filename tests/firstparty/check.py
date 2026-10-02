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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *args): pass

    def do_GET(self):
        path = urlsplit(self.path).path
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


async def session(ws_url, origin, records, evidence):
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
        finally:
            page.reader.cancel()
            with contextlib.suppress(asyncio.CancelledError): await page.reader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, help='write the recorded request log and monitor screenshot')
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
                asyncio.run(session(ws_url, origin, records, args.evidence))
            finally:
                proc.terminate()
                try: proc.wait(timeout=8)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
    finally:
        server.shutdown(); server.server_close()
        if args.evidence: args.evidence.write_text(json.dumps(records, indent=2) + '\n')


if __name__ == '__main__': main()
