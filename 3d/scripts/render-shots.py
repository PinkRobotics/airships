#!/usr/bin/env python3
"""Render the vehicle scenes used on the site and in the reports, on the GPU.

    python3 3d/scripts/render-shots.py            # every shot
    python3 3d/scripts/render-shots.py anchor     # one of them

Each shot is a query string against 3d/scripts/render-scene.html, which mounts the viewer at a
fixed pixel size with no page chrome around it. That matters: the alternative is screenshotting
the model lab, and then the figure's dimensions depend on the lab's panel widths and change
whenever someone adjusts the CSS.

HARDWARE, DELIBERATELY. `A3D_GPU=1` puts js_eval on the ANGLE/Vulkan path. swiftshader can
produce these — it did, while this was being written — but in software, slowly, and without
the multisampling that stops an 876 m hull looking like a staircase.

Output is written to 3d/assets/renders/, which is committed: these are the pictures on a public
page, and regenerating them needs a GPU that CI does not have.
"""
from __future__ import annotations

import base64
import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = ROOT / '3d' / 'assets' / 'renders'
sys.path.insert(0, str(ROOT / 'tools'))
from serve import serve_tree

# name -> query string. `t` is a position in the mission clip: source approach runs to 0.110,
# the fill to 0.354, outbound to 0.533, the release to 0.777, escape to 0.821.
SHOTS = {
    # The descent anchor deployed, mid-fill, with the lake under it. The picture the site has
    # been describing in words and not showing.
    'anchor': 'class=P10000&clip=mission_cycle&t=0.12&preset=mission&el=0.07&dist=1.55&w=2400&h=1350&quality=high',
    'anchor-close': 'class=P10000&clip=mission_cycle&t=0.12&preset=pumpbay&dist=1.6&w=2000&h=1400&quality=high',
    # The release, which is the other half of the cycle and the one people picture.
    'release': 'class=P10000&clip=mission_cycle&t=0.64&preset=mission&w=2400&h=1350&quality=high',
    # A clean three-quarter exterior for the class table and the paper's specification section.
    'exterior': 'class=P10000&clip=mission_cycle&t=0.45&preset=three-quarter&w=2400&h=1200&quality=high',
    # The lattice, which is the structural claim, and the cutaway that shows what is inside.
    'cutaway': 'class=P100&clip=mission_cycle&t=0.45&preset=side&mode=cutaway&w=2400&h=1100&quality=high',
    'lattice': 'class=P1000&clip=mission_cycle&t=0.45&preset=side&mode=lattice&w=2400&h=1000&quality=high',
}

GRAB = """(async () => {
  for (let i = 0; i < 200 && !window.__ready; i++) await new Promise(r => setTimeout(r, 100));
  if (!window.__ready) return { error: 'harness never became ready' };
  const url = window.viewer.snapshot();
  if (!url) return { error: 'snapshot() returned null — no WebGL 2 context' };
  return { png: url };
})()
"""


def trim_letterbox(path: pathlib.Path) -> tuple[int, int]:
    """Cut the dead band off the top of a capture.

    The canvas is sized from its container but the GL viewport does not always fill it, so a
    capture can carry a strip of clear colour along one edge. Rather than chase the mismatch
    through the renderer, crop rows that are uniformly the clear colour — it is unambiguous
    (the scene has a gradient sky, never a flat one) and it costs nothing.
    """
    from PIL import Image
    im = Image.open(path).convert('RGB')
    w, h = im.size
    px = im.load()

    def dead(y):
        return all(sum(px[x, y]) < 24 for x in range(0, w, max(1, w // 64)))

    top = 0
    while top < h - 1 and dead(top):
        top += 1
    bot = h
    while bot > top + 1 and dead(bot - 1):
        bot -= 1
    if top or bot != h:
        im.crop((0, top, w, bot)).save(path, optimize=True)
        return w, bot - top
    return w, h


def main() -> int:
    want = sys.argv[1:] or list(SHOTS)
    unknown = [w for w in want if w not in SHOTS]
    if unknown:
        print(f'render-shots: no such shot: {", ".join(unknown)}', file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)

    env = {**os.environ, 'A3D_GPU': '1'}
    with tempfile.TemporaryDirectory(prefix='shots-') as tmp, serve_tree(ROOT) as base:
        for name in want:
            q = SHOTS[name]
            w = dict(p.split('=', 1) for p in q.split('&'))
            env['A3D_WINDOW'] = f"{int(w.get('w', 1800)) + 80},{int(w.get('h', 1000)) + 80}"
            js = pathlib.Path(tmp) / 'grab.mjs'
            js.write_text(GRAB)
            res = pathlib.Path(tmp) / 'grab.json'
            r = subprocess.run(
                [sys.executable, str(ROOT / 'tools' / 'js_eval.py'),
                 f'{base}3d/scripts/render-scene.html?{q}',
                 str(js), str(res), '45'],
                capture_output=True, text=True, errors='replace', env=env, cwd=ROOT)
            if r.returncode or not res.exists():
                print(f'  {name}: FAILED\n{r.stdout[-800:]}{r.stderr[-800:]}', file=sys.stderr)
                return 1
            data = json.loads(res.read_text())
            if 'png' not in data:
                print(f'  {name}: {data.get("error", data)}', file=sys.stderr)
                return 1
            raw = base64.b64decode(data['png'].split(',', 1)[1])
            path = OUT / f'{name}.png'
            path.write_bytes(raw)
            trimmed = trim_letterbox(path)
            print(f'  {name}.png — {trimmed[0]}x{trimmed[1]}, {path.stat().st_size // 1024} KB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
