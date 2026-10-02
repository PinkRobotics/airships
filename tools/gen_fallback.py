#!/usr/bin/env python3
"""Generate the static fallback baked into index.html, so no visitor is stuck at "loading…".

    tools/gen_fallback.py            regenerate the FALLBACK regions in index.html
    tools/gen_fallback.py --check    regenerate into scratch and diff; exit 1 on any drift
    tools/gen_fallback.py --poster   also re-capture media/map-snapshot.jpg from the page

WHY THIS EXISTS. The monitor is one big application: with scripts off — a crawler, a
reader-mode fetch, a broken CDN day — the page used to be a labelled empty shell whose only
words about the data were "loading…". The fallback regions give that visitor the real story
from the repository's own bundled snapshot (data/snapshot.json, the dated offline copy that
is also the page's last fallback tier and the golden tests' pinned input): the fires, the
fleet, one worked mission, and two captioned stills. When the page runs, the application
overwrites every one of these regions exactly the way it already overwrote the empty ones.

WHY GENERATED, NEVER TYPED. Every number in the block is read out of the page itself,
running the snapshot replay (`?seed=7&data=snapshot`) headless — the same deterministic run
the golden suite compares — via tools/fallback_dump.js. Hand-typed copies of model output
are the exact class of defect check_figures_fresh.py exists for.

WHY --check RE-RUNS THE BROWSER. This repository has twice shipped a gate that lied by
comparing a committed cache to itself. The check therefore REGENERATES the regions from a
fresh replay and byte-compares them against what index.html carries; a snapshot swap, a
model change, or a hand edit between the markers all go red with the region named.

The regions, each between `<!--NAME-->` and `<!--/NAME-->` markers (the concept page's
marker idiom — see SCALE3/CUTAWAY there):

    FALLBACK-HUD      the #hudLive chip's pre-boot text (was "loading…")
    FALLBACK-ROSTER   the fleet roster table inside #roster (was empty)
    FALLBACK-FIRES    the top-fires table inside #firesTop (was empty)
    FALLBACK          the #fallback section: snapshot summary, posters, worked mission

The poster (media/map-snapshot.jpg) is regenerable evidence, captured from the live map
canvas of the running replay page; it is committed because the page serves it. `--check`
verifies it exists but does not re-shoot it — a canvas capture is not byte-stable, and the
honesty the check owes is about the NUMBERS.
"""
from __future__ import annotations

import base64
import html
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
POSTER = ROOT / 'media' / 'map-snapshot.jpg'
VEHICLE = ROOT / 'media' / 'intake.jpg'
PORT = 8871
REPLAY_URL = f'http://127.0.0.1:{PORT}/index.html?seed=7&data=snapshot'

CHECK = '--check' in sys.argv
SHOOT = '--poster' in sys.argv

# The poster is a CDP screenshot clipped to the map box, including its data-age badge.
POSTER_SETUP_JS = """
(() => {
  const ov = document.getElementById('introOv');
  if (ov && !ov.hidden) ov.click();
  document.getElementById('btnFitFires').click();
  return true;
})()
"""
POSTER_RECT_JS = """
(() => {
  const r = document.querySelector('.mapbox').getBoundingClientRect();
  return { x: Math.ceil(r.x), y: Math.ceil(r.y),
           width: Math.floor(r.width), height: Math.floor(r.height) };
})()
"""


def fmt(n) -> str:
    """Thousands-grouped integers, matching sim/format.js's en-CA fmt()."""
    return f'{round(n):,}'


def fmt1(x) -> str:
    """One decimal at most, none when whole — fmt(x, 1) in the page's locale."""
    s = f'{x:.1f}'
    return s[:-2] if s.endswith('.0') else s


def esc(s) -> str:
    return html.escape(str(s), quote=False)


def run_dump(scratch: pathlib.Path, jsfile: pathlib.Path, out: pathlib.Path, wait: str):
    """One headless replay run, dumped to JSON — the check_figures_fresh idiom."""
    import os
    env = dict(os.environ, AIRSHIPS_TMPDIR=str(scratch), A3D_WINDOW='1600,1600')
    r = subprocess.run(
        [sys.executable, str(ROOT / 'tools' / 'js_eval.py'), REPLAY_URL,
         str(jsfile), str(out), wait],
        capture_output=True, text=True, errors='replace', cwd=ROOT, env=env, timeout=240)
    if r.returncode or not out.exists():
        raise SystemExit('gen_fallback: could not read the replay page\n'
                         + r.stdout[-1500:] + r.stderr[-1500:])
    return json.loads(out.read_text())


def img_size(path: pathlib.Path):
    from PIL import Image
    with Image.open(path) as im:
        return im.size


# ---------- rendering ---------------------------------------------------------------------------


def render(d: dict) -> dict[str, str]:
    date = (d['snapshotAt'] or '')[:10]
    iso = d['snapshotAt'] or ''
    fires, fleet, ex = d['fires'], d['fleet'], d['example']
    top = d['topFires']

    hud = (f'<b>DATA SNAPSHOT</b> · {esc(date)} · {fmt(fires["active"])} fires · '
           'live data replaces this when the page runs')

    rows = []
    for grp in d['roster']:
        # P-1000 and P-10000 wear the truth beside their names (operator, 08-13):
        # the crush envelope closes near 96 m of hull and both live outside it.
        badge = ("" if grp["cls"] == "P-100" else
                 ' <span style="color:#d98b80;font-weight:600">· outside the 96 m envelope</span>')
        rows.append(f'<tr class="r-clsrow"><td colspan="3">'
                    f'<span class="r-cls">{esc(grp["cls"])} ×{grp["count"]}{badge}</span></td></tr>')
        for s in grp['ships']:
            fire = esc(s['fire']) if s['fire'] else '<span style="color:var(--faint)">standing by</span>'
            rate = f'{fmt(s["tph"])} kL/h' if s['tph'] else '—'
            rows.append(f'<tr class="r-ship"><td class="r-name">{esc(s["hull"])}</td>'
                        f'<td>{fire}</td><td class="ph">{rate}</td></tr>')
    roster = ('<table class="fleettab" aria-label="Fleet roster from the bundled snapshot, '
              'grouped by class: hull, the fire it serves, and its simulated delivery rate">'
              '<tbody>' + ''.join(rows) + '</tbody></table>'
              f'<p class="small" style="margin-top:var(--s2);font-size:var(--t-11);color:var(--faint)">'
              f'Live allocation over today’s fires. This printed copy is the bundled {esc(date)} snapshot.</p>')

    frows = []
    for f in top:
        hull = esc(f['hull']) if f['hull'] else '—'
        # "queued", with no reason attached: the allocator leaves a fire without a hull when
        # the sixteen hulls are spent on higher-priority fires (app/fleet.js), and it has no
        # notion of a hull's range, so the cell does not name one.
        rate = f'{fmt(f["tph"])} kL/h' if f['tph'] else 'queued'
        frows.append(f'<tr class="r-ship"><td>{esc(f["name"])}</td>'
                     f'<td style="text-align:right">{fmt(f["sizeHa"])} ha</td>'
                     f'<td style="text-align:right">{hull}</td>'
                     f'<td style="text-align:right">{rate}</td></tr>')
    firestab = ('<table class="fleettab" aria-describedby="firesNote" aria-label="Largest fires '
                'waiting for or receiving a hull, from the bundled snapshot">'
                '<tbody>' + ''.join(frows) + '</tbody></table>'
                f'<p class="small" style="margin-top:var(--s2);font-size:var(--t-11);color:var(--faint)">'
                f'Live sizes over today’s fires. This printed copy is the bundled {esc(date)} snapshot.</p>')

    p100, p1000, p10000 = fleet
    total = sum(g['count'] for g in fleet)
    flying = (f'all {fmt(total)} hulls are flying' if d['flying'] == total
              else f'{fmt(d["flying"])} of {fmt(total)} hulls are flying; the rest stand by')
    pw, ph = img_size(POSTER) if POSTER.exists() else (0, 0)
    vw, vh = img_size(VEHICLE)

    mission = ''
    if ex:
        mission = f'''
  <h3>One mission, worked</h3>
  <p><b style="color:var(--warm)">{esc(ex['hull'])}</b>, a {esc(ex['cls'])}, is assigned to {esc(ex['fire'])} ({esc(ex['fireId'])}: {fmt(ex['fireHa'])} ha, {esc(ex['fireStatus']).lower()}). It fills from {esc(ex['source'])} ({fmt(ex['sourceHa'])} ha of mapped surface), a {fmt1(ex['legKm'])} km leg from the fire. One cycle takes about {fmt(ex['cycleMin'])} minutes: approach the water, pump aboard, transit, and drop along the fire. It escapes on the surplus buoyancy the drop just created and returns while making nitrogen ballast. It delivers {fmt(ex['deliveredT'])} t of water, sustaining {fmt(ex['tph'])} kL/h against this one fire. The cycle is computed end to end from real fire and water data. Simulation, not operations: no such aircraft exists.</p>'''

    main = f'''
<style>
#fallback{{display:none;max-width:880px;margin:0 auto;padding:var(--s5) var(--s5) var(--s8)}}
#fallback h2{{margin:var(--s4) 0 var(--s2)}}
#fallback h3{{margin:var(--s5) 0 var(--s2)}}
#fallback p{{max-width:66ch;color:var(--muted);margin:var(--s2) 0}}
#fallback figure{{margin:var(--s4) 0}}
#fallback img{{max-width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:var(--r)}}
#fallback figcaption{{font-size:var(--t-13);color:var(--faint);max-width:66ch;margin-top:var(--s2)}}
</style>
<noscript><style>
  body{{overflow:auto;display:block;height:auto}}
  .monitor{{display:block}}
  .monbody{{display:block}}
  .cp-leftcol{{overflow:visible}}
  .cp-map,.cp-rightcol,.cp-ops,#introOv{{display:none}}
  #fallback{{display:block}}
</style></noscript>
<section id="fallback" aria-label="Static snapshot of the fleet monitor">
  <p class="kicker">STATIC SNAPSHOT · {esc(date)}</p>
  <h2>The monitor, standing still</h2>
  <p>This page is a live instrument: current BC wildfire data run through a simulated fleet of sixteen conceptual vacuum airships. It ships a complete no-script fallback: the same monitor, computed from the snapshot bundled with this site on <time datetime="{esc(iso)}">{esc(date)}</time>, with the fleet roster, the top fires and one worked mission rendered as text. With scripts on, the identical panels run over the live feed. <b style="color:var(--text)">Live data replaces this when the page runs.</b></p>
  <p>One colour rule governs the whole page: <span style="color:var(--bone)">bone is live public fire data</span>, <span style="color:var(--warm)">pink is the simulated fleet</span>. Nothing on this map mixes the two. The fleet is simulated. The fires are real, and the BC Wildfire Service remains the authority for them. Sources, licences and the arithmetic are on the <a href="concept/">how-it-works page</a>.</p>
  <h3>The fires: real, as of the snapshot</h3>
  <p>The snapshot holds {fmt(fires['active'])} active fires from the BC Wildfire Service feed: {fmt(fires['outOfControl'])} out of control, {fmt(fires['ofNote'])} flagged as fires of note. The top-fires panel above lists the largest out-of-control fires. {esc(top[0]['name']) if top else '—'} is the largest fire at {fmt(top[0]['sizeHa']) if top else 0} ha.</p>
  <h3>The fleet: simulated, sixteen hulls</h3>
  <p>A fixed demonstration fleet is shared across the worst fires. It has {fmt(p100['count'])} {esc(p100['name'])}s at {fmt(p100['payloadT'])} t of water and {fmt(p100['lenM'])} m each, {fmt(p1000['count'])} {esc(p1000['name'])}s at {fmt(p1000['payloadT'])} t and {fmt(p1000['lenM'])} m, and one {esc(p10000['name'])} at {fmt(p10000['payloadT'])} t and {fmt(p10000['lenM'])} m. In this snapshot's allocation {flying}. The full roster, hull by hull, is in the fleet panel above.</p>
  <figure>
    <img src="media/map-snapshot.jpg" width="{pw}" height="{ph}"
      alt="Map of British Columbia with the snapshot's fires drawn as status-coloured circles,
      satellite heat, water bodies, and the simulated airships as pink markers">
    <figcaption>This still shows the monitor's map from the {esc(date)} snapshot. Fires are circles coloured by status, satellite heat is orange, water is blue, and the simulated fleet is pink. When the page runs this is a live, draggable canvas over current data.</figcaption>
  </figure>{mission}
  <figure>
    <img src="media/intake.jpg" width="{vw}" height="{vh}" loading="eager" fetchpriority="high"
      alt="Render: the airship holds station with hoses lowered and pump pods hanging toward the water">
    <figcaption>The reference concept vehicle at a lake intake, hoses down, pumping while it hovers. A still render of the same 3D model the running monitor animates beside the map.</figcaption>
  </figure>
</section>'''

    return {'FALLBACK-HUD': hud, 'FALLBACK-ROSTER': roster,
            'FALLBACK-FIRES': firestab, 'FALLBACK': main}


# ---------- splicing ----------------------------------------------------------------------------


def region_re(name: str) -> re.Pattern:
    return re.compile(f'<!--{re.escape(name)}-->(.*?)<!--/{re.escape(name)}-->', re.S)


def splice(text: str, name: str, body: str) -> str:
    pat = region_re(name)
    hits = pat.findall(text)
    if len(hits) != 1:
        raise SystemExit(f'gen_fallback: expected exactly one <!--{name}--> region '
                         f'in index.html, found {len(hits)}')
    return pat.sub(lambda m: f'<!--{name}-->{body}<!--/{name}-->', text)


def capture_poster(scratch: pathlib.Path):
    """One headless browser: replay the snapshot, dismiss the intro, fit the fires, then a
    CDP screenshot clipped to the map box. The launch flags are js_eval.py's."""
    import asyncio
    import os
    import socket
    import urllib.request
    from PIL import Image

    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        cdp_port = s.getsockname()[1]
    log = (scratch / 'chromium.log').open('w')
    proc = subprocess.Popen([
        'chromium', '--headless=new', '--hide-scrollbars',
        *([ '--no-sandbox', '--disable-dev-shm-usage'] if os.environ.get('CI') else []),
        '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
        f'--remote-debugging-port={cdp_port}', '--remote-allow-origins=*',
        f'--user-data-dir={scratch}/poster-profile', '--window-size=1600,1600', 'about:blank',
    ], stdout=subprocess.DEVNULL, stderr=log, start_new_session=True)

    async def drive():
        ws_url = None
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                break
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{cdp_port}/json'))
                pages = [t for t in tabs if t['type'] == 'page']
                if pages:
                    ws_url = pages[0]['webSocketDebuggerUrl']
                    break
            except Exception:
                pass
            time.sleep(0.2)
        if ws_url is None:
            raise SystemExit('gen_fallback: chromium never opened a debuggable page — see '
                             + str(scratch / 'chromium.log'))
        import websockets
        async with websockets.connect(ws_url, max_size=600_000_000) as ws:
            mid = 0

            async def call(method, params=None):
                nonlocal mid
                mid += 1
                await ws.send(json.dumps({'id': mid, 'method': method,
                                          'params': params or {}}))
                while True:
                    msg = json.loads(await ws.recv())
                    if msg.get('id') == mid:
                        return msg.get('result', {})

            async def evaluate(js):
                r = await call('Runtime.evaluate',
                               {'expression': js, 'returnByValue': True})
                if 'exceptionDetails' in r:
                    raise SystemExit('gen_fallback poster JS failed: '
                                     + json.dumps(r['exceptionDetails'])[:600])
                return r.get('result', {}).get('value')

            await call('Page.enable')
            await call('Runtime.enable')
            await call('Page.navigate', {'url': REPLAY_URL})
            await asyncio.sleep(14)
            await evaluate(POSTER_SETUP_JS)
            await asyncio.sleep(2.5)
            rect = await evaluate(POSTER_RECT_JS)
            shot = await call('Page.captureScreenshot',
                              {'format': 'png', 'clip': {**rect, 'scale': 1}})
            return base64.b64decode(shot['data'])

    try:
        raw = asyncio.run(drive())
    finally:
        try:
            os.killpg(proc.pid, 15)
        except Exception:
            proc.terminate()
        log.close()
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    if im.width > 1100:
        im = im.resize((1100, round(im.height * 1100 / im.width)), Image.LANCZOS)
    im.save(POSTER, quality=82, optimize=True)
    print(f'gen_fallback: poster {im.width}x{im.height} -> {POSTER.relative_to(ROOT)} '
          f'({POSTER.stat().st_size // 1024} KB)')


def main() -> int:
    scratch = pathlib.Path(tempfile.mkdtemp(prefix='fallback-', dir=ROOT))
    server = subprocess.Popen([sys.executable, str(ROOT / 'tools' / 'serve.py'),
                               '--port', str(PORT)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=ROOT)
    try:
        time.sleep(1.5)
        if SHOOT and not CHECK:
            capture_poster(scratch)
        if not POSTER.exists():
            raise SystemExit('gen_fallback: media/map-snapshot.jpg is missing — '
                             'run tools/gen_fallback.py --poster first')
        d = run_dump(scratch, ROOT / 'tools' / 'fallback_dump.js', scratch / 'dump.json', '18')
    finally:
        server.terminate()
        # rmtree, not unlink: a failed browser run leaves its profile DIRECTORY behind, and
        # ignore_errors because chromium's children can outlive it and keep writing briefly.
        import shutil
        shutil.rmtree(scratch, ignore_errors=True)

    if d['tier'] != 'replay':
        raise SystemExit(f'gen_fallback: expected the replay tier, page reports {d["tier"]!r}')

    regions = render(d)
    text = INDEX.read_text()

    if CHECK:
        drift = []
        for name, body in regions.items():
            pat = region_re(name)
            hits = pat.findall(text)
            if len(hits) != 1:
                drift.append(f'{name}: marker pair missing or duplicated ({len(hits)} found)')
            elif hits[0] != body:
                drift.append(f'{name}: committed block differs from a fresh regeneration')
        if drift:
            print('gen_fallback --check: the fallback block has drifted from the snapshot:',
                  file=sys.stderr)
            for line in drift:
                print('  ' + line, file=sys.stderr)
            print('\nRegenerate with: python3 tools/gen_fallback.py  (and commit index.html)',
                  file=sys.stderr)
            return 1
        words = len(re.sub(r'<[^>]+>', ' ', ''.join(regions.values())).split())
        print(f'gen_fallback --check: all {len(regions)} fallback regions match a fresh '
              f'regeneration ({words} words of static content)')
        return 0

    out = text
    for name, body in regions.items():
        out = splice(out, name, body)
    if out != text:
        INDEX.write_text(out)
        print('gen_fallback: index.html fallback regions regenerated '
              f'(snapshot {d["snapshotAt"][:10]}, {d["fires"]["active"]} fires, '
              f'{d["flying"]} hulls flying)')
    else:
        print('gen_fallback: index.html already current')
    return 0


if __name__ == '__main__':
    sys.exit(main())
