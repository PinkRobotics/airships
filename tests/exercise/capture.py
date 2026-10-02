#!/usr/bin/env python3
"""Capture local exercise evidence with scripts disabled (or enabled), recording requests.

Usage: python3 tests/exercise/capture.py URL OUTDIR [--no-script]
Profiles use TMPDIR; output contains only the screenshots, not browser profiles.
"""
import argparse
import asyncio
import base64
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import tempfile
import urllib.parse
import urllib.request
import websockets


async def capture(url, out, width, height, no_script):
    with socket.socket() as s:
        s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    foreign=[];errors=[]; own=urllib.parse.urlsplit(url).netloc
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        with open(Path(tmp)/'chrome.log','w') as log:
            proc=subprocess.Popen([shutil.which('chromium'),'--headless=new','--disable-gpu',
                '--hide-scrollbars','--disable-background-networking','--no-first-run',
                '--no-default-browser-check',f'--user-data-dir={tmp}/profile',
                f'--remote-debugging-port={port}','about:blank'],stdout=log,stderr=log,start_new_session=True)
            try:
                wsurl=None
                for _ in range(160):
                    try:
                        tabs=json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=1))
                        wsurl=next(t['webSocketDebuggerUrl'] for t in tabs if t['type']=='page');break
                    except Exception: await asyncio.sleep(.25)
                assert wsurl, 'browser did not start'
                async with websockets.connect(wsurl,max_size=None) as ws:
                    seq=0
                    async def call(method,params=None):
                        nonlocal seq
                        seq+=1;mid=seq
                        await ws.send(json.dumps({'id':mid,'method':method,'params':params or {}}))
                        while True:
                            msg=json.loads(await ws.recv())
                            if msg.get('method')=='Network.requestWillBeSent':
                                u=msg['params']['request']['url'];host=urllib.parse.urlsplit(u).netloc
                                if host and host!=own:foreign.append(u)
                            if msg.get('method')=='Runtime.exceptionThrown':errors.append(msg['params']['exceptionDetails']['text'])
                            if msg.get('id')==mid:
                                assert 'error' not in msg,msg.get('error')
                                return msg.get('result',{})
                    await call('Page.enable');await call('Runtime.enable');await call('Network.enable')
                    await call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':False})
                    if no_script:await call('Emulation.setScriptExecutionDisabled',{'value':True})
                    await call('Page.navigate',{'url':url});await asyncio.sleep(5)
                    if not no_script:
                        await call('Runtime.evaluate',{'expression':"document.getElementById('introOv')?.click()"})
                    dims=await call('Page.getLayoutMetrics');size=dims['cssContentSize']
                    shot=await call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True,
                        'clip':{'x':0,'y':0,'width':width,'height':min(16000,size['height']),'scale':1}})
                    out.write_bytes(base64.b64decode(shot['data']))
            finally:
                os.killpg(proc.pid,signal.SIGTERM)
                try:proc.wait(timeout=5)
                except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
    print(f'{out.name}: {width}x{height}; scripts {"off" if no_script else "on"}; foreign requests {len(foreign)}; script errors {len(errors)}')
    assert not foreign and not errors, 'foreign request or script error'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('url');p.add_argument('out',type=Path);p.add_argument('--no-script',action='store_true');a=p.parse_args()
    assert urllib.parse.urlsplit(a.url).hostname=='127.0.0.1','local evidence only'
    a.out.mkdir(parents=True,exist_ok=True)
    for w,h in [(1440,900),(834,1112),(390,844)]:asyncio.run(capture(a.url,a.out/f'{w}.png',w,h,a.no_script))

if __name__=='__main__':main()
