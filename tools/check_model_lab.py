#!/usr/bin/env python3
"""Measure model-lab phone overflow and motion controls in an owned local browser.

Called by the existing 3D browser gate. --record saves measurements for review.
No real feed, display browser or fixed listening port is used.
"""
import argparse
import asyncio
import contextlib
import json
import os
from pathlib import Path
import tempfile
import time
from urllib.parse import urlsplit

import websockets
from devtools import page_target
from serve import serve_tree

ROOT = Path(__file__).resolve().parents[1]


async def measure(endpoint, base):
    async with websockets.connect(endpoint, max_size=30_000_000) as ws:
        ident = 0
        async def call(method, params=None):
            nonlocal ident
            ident += 1
            await ws.send(json.dumps(dict(id=ident, method=method, params=params or {})))
            deadline = time.monotonic()+240
            while True:
                message = json.loads(await asyncio.wait_for(ws.recv(), max(0, deadline-time.monotonic())))
                if message.get('id') == ident:
                    if 'error' in message:
                        raise RuntimeError(message['error'])
                    return message.get('result', {})
        async def evaluate(expression):
            result = await call('Runtime.evaluate', dict(expression=expression,
                                returnByValue=True, awaitPromise=True))
            if result.get('exceptionDetails'):
                raise RuntimeError('model-lab evaluation threw')
            return result['result'].get('value')
        await call('Page.enable')
        await call('Runtime.enable')
        results, failures = [], []
        cases = [(390, 'no-preference', ''), (320, 'no-preference', '?paused=1'),
                 (390, 'reduce', ''), (390, 'no-preference', '?reduced=1'),
                 (390, 'no-preference', '?paused=1'), (390, 'reduce', '?reduced=0')]
        for case_index, (width, preference, query) in enumerate(cases):
            await call('Emulation.setDeviceMetricsOverride', dict(width=width,
                       height=844, deviceScaleFactor=1, mobile=True))
            await call('Emulation.setTouchEmulationEnabled', dict(enabled=True, maxTouchPoints=5))
            await call('Emulation.setEmulatedMedia', dict(features=[
                dict(name='prefers-reduced-motion', value=preference)]))
            target = base+'model-lab/'+query+('&' if query else '?')+f'probe={case_index}'
            await call('Page.navigate', dict(url=target))
            deadline = time.monotonic()+180
            ready = f"location.href === {json.dumps(target)} && document.readyState === 'complete' && !!window.LAB && !!document.querySelector('#scaleScene .a3d-table')"
            while not await evaluate(ready):
                if time.monotonic() > deadline:
                    raise RuntimeError('model-lab did not boot within 180 s')
                await asyncio.sleep(0.5)
            before = await evaluate("""(() => {
                const table = document.querySelector('#scaleScene table');
                const svg = document.querySelector('#scaleScene svg');
                const region = table.closest('[role=region]');
                return {scrollWidth:document.documentElement.scrollWidth,
                    clientWidth:document.documentElement.clientWidth,
                    scrub:Number(document.getElementById('scrub').value),
                    reduced:document.getElementById('reduced').checked,
                    tableWidth:table.getBoundingClientRect().width,
                    svgWidth:svg.getBoundingClientRect().width,
                    labelledScroll:!!region && !!region.getAttribute('aria-label') && region.tabIndex===0};
            })()""")
            await asyncio.sleep(3)
            after = await evaluate("Number(document.getElementById('scrub').value)")
            reduced = query == '?reduced=1' or (preference == 'reduce' and query != '?reduced=0')
            advances = query != '?paused=1' and not reduced
            row = dict(width=width, preference=preference, query=query,
                       before=before, scrubAfter3s=after)
            results.append(row)
            print(json.dumps(row), flush=True)
            label = f'{width}px/{preference}/{query or "default"}'
            if before['clientWidth'] != width or before['scrollWidth'] != width:
                failures.append(label+': document overflows the mobile viewport')
                print('Overflow elements: '+json.dumps(await evaluate("[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1 && !e.closest('[role=region]')).map(e=>({tag:e.tagName,id:e.id,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,60)})).slice(0,10)")),flush=True)
            if before['svgWidth'] > width or not before['labelledScroll']:
                failures.append(label+': scale figure or labelled keyboard scroll region fails')
            if before['reduced'] != reduced:
                failures.append(label+': motion control does not show its initial state')
            if (after > before['scrub']) != advances:
                failures.append(label+': timeline does not follow the preference/query controls')
        return results, failures


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base', help='existing complete loopback base URL')
    ap.add_argument('--record', type=Path)
    args = ap.parse_args()
    if args.base:
        url = urlsplit(args.base)
        if url.scheme != 'http' or url.hostname != '127.0.0.1' or not url.port:
            ap.error('--base must name a local owned server')
    scratch = Path(os.environ.get('TMPDIR', str(ROOT/'.browser-scratch')))
    scratch.mkdir(parents=True, exist_ok=True)
    server = contextlib.nullcontext(args.base.rstrip('/')+'/') if args.base else serve_tree(ROOT)
    with tempfile.TemporaryDirectory(dir=scratch, prefix='model-lab-', ignore_cleanup_errors=True) as td:
        with server as base, (Path(td)/'browser.log').open('w') as log:
            flags = ['--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
            if os.environ.get('CI'):
                flags += ['--no-sandbox', '--disable-dev-shm-usage']
            with page_target(os.environ.get('CHROME','chromium'), flags,
                             Path(td)/'profile', stderr=log) as (_, endpoint):
                results, failures = asyncio.run(measure(endpoint, base))
    if args.record:
        args.record.write_text(json.dumps(dict(measurements=results, failures=failures), indent=2)+'\n')
    for failure in failures:
        print('FAIL '+failure)
    print(f'model-lab: {len(results)} mobile/motion cases; {len(failures)} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
