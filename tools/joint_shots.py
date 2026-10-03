#!/usr/bin/env python3
"""Multi-view captures of every printed joint, for the vision review.

    python3 tools/joint_shots.py [--joints 2,9,22] [--size 640]
                                 [--out research/geometry/nodes/vision/shots]

The joints are expected to keep changing, and each change has to be verifiably correct —
the designer's brief, verbatim: "each one is fully correct... the pipe fits where it
needs to, there isn't overlap between pipes... multi-views from each joint, render them
in various ways." So this drives the EXPLORER PAGE ITSELF — the real renderer, the real
depth buffer, the article exactly as shipped — through one headless Chromium, and
captures six views per joint:

    orbit0 / orbit1 / orbit2   the seated article from three azimuths, pipes on
    top                        from overhead
    joinery                    pipes hidden: bare sockets, spigots, ghost centrelines
    cutaway                    the page's own cut plane pushed through this joint

Every view also records ALIGNMENT MARKERS projected by the page's own camera math — the
joint centre and each arm's seat point, in image pixels — and the marked copies drawn
from them are what the vision model reviews: it can be told exactly where a pipe end
OUGHT to be, not asked to guess. Output: per-joint PNGs (raw + .marked) and index.json
with markers and camera state per view.

NOT in `make check` — this needs a browser and minutes, and its consumer
(tools/review_joints.py) needs the local vision fleet. `make jointreview` runs both.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import os
import pathlib
import subprocess
import sys
import time
import tempfile
from serve import serve_tree
from devtools import page_target

ROOT = pathlib.Path(__file__).resolve().parent.parent

VIEW_JS = """
(async () => {
  const cfg = __CFG__;
  const E = window.EXPLORER;
  if (!E) return { error: 'no EXPLORER', errs: window.__errs };
  if (!window.__vinit) {
    window.__vinit = true;
    E.setLevel(3, true);
    E.setGroup('all');
    E.state.skinMode = 'off';
    E.state.turntable = false;
    window.__cam = await import('/3d/render/camera.js');
    // The review sees geometry, not the page: hide every DOM layer except the canvas.
    const st = document.createElement('style');
    st.textContent = 'body > *:not(#stage){visibility:hidden !important}' +
                     '#stage{visibility:visible !important}';
    document.head.appendChild(st);
  }
  const p = E.parts.find((q) => q.key === cfg.key);
  if (!p) return { error: 'no part ' + cfg.key };
  E.state.partsMode = cfg.mode;
  // The cutaway plane lives on the stage's own x: world x = cx + cut * radius * 0.9.
  // Solve for the value that puts the section a hair past this joint's centre, and
  // never exactly 0, which the page reads as "off".
  let cut = 0;
  if (cfg.cutaway) {
    const st = E.levels[3];
    cut = (p.pos[0] - (st.target ? st.target[0] : 0)) / (st.radius * 0.9) + 0.03;
    cut = Math.max(-1, Math.min(1, Math.abs(cut) < 0.05 ? 0.05 : cut));
  }
  E.setCut(cut);
  E.cam.minDistance = 0.005;
  E.cam.maxDistance = 10;
  E.cam.target = p.pos.slice();
  E.cam.azimuth = cfg.az;
  E.cam.elevation = cfg.el;
  E.cam.distance = cfg.dist;
  E.tick(0.016);
  const vm = window.__cam.viewMatrix(E.cam);
  const pm = window.__cam.projMatrix(E.cam, cfg.w / cfg.h);
  const proj = (pt) => {
    const [x, y, z] = pt;
    const vx = vm[0]*x + vm[4]*y + vm[8]*z + vm[12];
    const vy = vm[1]*x + vm[5]*y + vm[9]*z + vm[13];
    const vz = vm[2]*x + vm[6]*y + vm[10]*z + vm[14];
    const cx = pm[0]*vx + pm[4]*vy + pm[8]*vz + pm[12];
    const cy = pm[1]*vx + pm[5]*vy + pm[9]*vz + pm[13];
    const cw = pm[3]*vx + pm[7]*vy + pm[11]*vz + pm[15];
    if (cw <= 1e-6) return null;
    const sx = (cx / cw * 0.5 + 0.5) * cfg.w;
    const sy = (1 - (cy / cw * 0.5 + 0.5)) * cfg.h;
    if (sx < -40 || sy < -40 || sx > cfg.w + 40 || sy > cfg.h + 40) return null;
    return [Math.round(sx), Math.round(sy)];
  };
  const cg = E.cellFrame;
  const xf = (v) => [cg[0]*v[0] + cg[4]*v[1] + cg[8]*v[2] + cg[12],
                     cg[1]*v[0] + cg[5]*v[1] + cg[9]*v[2] + cg[13],
                     cg[2]*v[0] + cg[6]*v[1] + cg[10]*v[2] + cg[14]];
  // A seat behind the joint's own body draws as a marker floating ON the body — the
  // reviewer then fails an arm that is fine. Split near-side from far-side by camera
  // distance against the joint centre; far-side seats are drawn hollow and the brief
  // says to verify them in the other tiles.
  const c = E.cam;
  const eye = [c.target[0] + c.distance * Math.cos(c.elevation) * Math.cos(c.azimuth),
               c.target[1] + c.distance * Math.cos(c.elevation) * Math.sin(c.azimuth),
               c.target[2] + c.distance * Math.sin(c.elevation)];
  const dEye = (pt) => Math.hypot(pt[0]-eye[0], pt[1]-eye[1], pt[2]-eye[2]);
  const dC = dEye(p.pos);
  const seats = [];
  let ai = 0;
  for (const m of E.members) {
    const ki = m.keys.indexOf(cfg.key);
    if (ki < 0 || !m.seats) continue;
    const [A, B] = m.ends;
    const d = [B[0]-A[0], B[1]-A[1], B[2]-A[2]];
    const L = Math.hypot(d[0], d[1], d[2]);
    const n = [d[0]/L, d[1]/L, d[2]/L];
    const s = m.seats[ki];
    const local = ki === 0
      ? [A[0] + n[0]*s, A[1] + n[1]*s, A[2] + n[2]*s]
      : [B[0] - n[0]*s, B[1] - n[1]*s, B[2] - n[2]*s];
    const world = xf(local);
    seats.push({ i: ai++, kind: m.kind, group: m.group || null,
                 px: proj(world), far: dEye(world) > dC + 0.004 });
  }
  return { centre: proj(p.pos), seats, cut,
           tris: E.renderer.stats.triangles, errs: window.__errs };
})()
"""


def annotate(png_path: pathlib.Path, rec: dict) -> None:
    """Markers onto a copy: cyan circle at the joint centre; solid green crosshair for a
    NEAR-side seat (its pipe end must be visible here); hollow orange square for a
    FAR-side seat (occluded by the body in this view — verify in the other tiles).
    The vision model is briefed on exactly this legend."""
    from PIL import Image, ImageDraw
    im = Image.open(png_path).convert("RGB")
    dr = ImageDraw.Draw(im)
    c = rec.get("centre")
    if c:
        dr.ellipse([c[0]-9, c[1]-9, c[0]+9, c[1]+9], outline=(0, 220, 255), width=2)
    for s in rec["seats"]:
        if not s["px"]:
            continue
        x, y = s["px"]
        if s.get("far"):
            o = (255, 160, 40)
            dr.rectangle([x-6, y-6, x+6, y+6], outline=o, width=2)
            dr.text((x+8, y+4), str(s["i"]), fill=o)
        else:
            g = (60, 255, 60)
            dr.line([x-7, y, x+7, y], fill=g, width=2)
            dr.line([x, y-7, x, y+7], fill=g, width=2)
            dr.text((x+8, y+4), str(s["i"]), fill=g)
    im.save(png_path.with_suffix(".marked.png"))


async def run(args) -> None:
    flags = ["--disable-gpu", "--hide-scrollbars", "--use-angle=swiftshader",
             "--enable-unsafe-swiftshader", f"--window-size={args.size},{args.size}"]
    if os.environ.get('CI'):
        flags += ['--no-sandbox', '--disable-dev-shm-usage']
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    with serve_tree(ROOT) as base, tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp, \
            page_target('chromium', flags, pathlib.Path(tmp) / 'profile') as (_proc, ws_url):
        import websockets
        async with websockets.connect(ws_url, max_size=300_000_000) as ws:
            mid = 0

            async def call(method, params=None):
                nonlocal mid
                mid += 1
                await ws.send(json.dumps({"id": mid, "method": method,
                                          "params": params or {}}))
                while True:
                    msg = json.loads(await ws.recv())
                    if msg.get("id") == mid:
                        return msg.get("result", {})

            await call("Page.enable")
            await call("Runtime.enable")
            await call("Emulation.setDeviceMetricsOverride",
                       {"width": args.size, "height": args.size,
                        "deviceScaleFactor": 1, "mobile": False})
            await call("Page.navigate",
                       {"url": f"{base}ship/index.html?still=1"})
            await asyncio.sleep(args.boot)

            manifest = json.loads(
                (ROOT / "research/geometry/nodes/manifest.json").read_text())
            picks = ([int(x) for x in args.joints.split(",") if x != ""]
                     if args.joints else range(len(manifest["nodes"])))
            # The page keys parts by integer u; recover each manifest row's page key the
            # same way the page builds them (lattice by u; rim/hub keys resolved below).
            first = await call("Runtime.evaluate", {
                "expression": "window.EXPLORER ? JSON.stringify(window.EXPLORER.parts"
                              ".map(p => ({key: p.key, role: p.role, u: p.u}))) : 'no'",
                "returnByValue": True})
            pages_parts = json.loads(first["result"]["value"])
            by_ru = {f"{p['role']}|{','.join(map(str, p['u']))}": p["key"]
                     for p in pages_parts}

            index = {"sizePx": args.size, "views": {}, "generated": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            n_shot = 0
            for i in picks:
                row = manifest["nodes"][i]
                key = by_ru.get(f"{row['role']}|{','.join(map(str, row['u']))}")
                if key is None:
                    print(f"  node {i:02d}: NO PAGE PART — skipped", file=sys.stderr)
                    continue
                jdir = out / f"node_{i:02d}"
                jdir.mkdir(exist_ok=True)
                a0 = 0.5 + i * 0.37          # varied per joint, deterministic
                views = [
                    ("orbit0", dict(mode="all", az=a0, el=0.32, cutaway=False)),
                    ("orbit1", dict(mode="all", az=a0 + 2.094, el=0.32, cutaway=False)),
                    ("orbit2", dict(mode="all", az=a0 + 4.189, el=0.32, cutaway=False)),
                    ("top", dict(mode="all", az=a0 + 0.7, el=1.25, cutaway=False)),
                    ("joinery", dict(mode="joinery", az=a0, el=0.32, cutaway=False)),
                    ("cutaway", dict(mode="all", az=0.0, el=0.25, cutaway=True)),
                ]
                index["views"][f"node_{i:02d}"] = {"key": key, "file": row["file"],
                                                   "role": row["role"],
                                                   "arms": row["arms"], "shots": {}}
                for vname, v in views:
                    cfg = dict(key=key, dist=args.dist, w=args.size, h=args.size, **v)
                    r = await call("Runtime.evaluate", {
                        "expression": VIEW_JS.replace("__CFG__", json.dumps(cfg)),
                        "returnByValue": True, "awaitPromise": True})
                    val = r.get("result", {}).get("value")
                    if not isinstance(val, dict) or val.get("error"):
                        sys.exit(f"joint_shots: probe failed on node {i} {vname}: "
                                 f"{json.dumps(r)[:300]}")
                    shot = await call("Page.captureScreenshot", {"format": "png"})
                    png = jdir / f"{vname}.png"
                    png.write_bytes(base64.b64decode(shot["data"]))
                    annotate(png, val)
                    val.pop("errs", None)
                    index["views"][f"node_{i:02d}"]["shots"][vname] = val
                    n_shot += 1
                print(f"  node_{i:02d} ({row['role']}, {row['arms']} arms): 6 views")
            (out / "index.json").write_text(json.dumps(index, indent=1))
            print(f"joint_shots: {n_shot} captures -> {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "research/geometry/nodes/vision/shots"))
    ap.add_argument("--joints", default="", help="comma list of node indices; empty = all")
    ap.add_argument("--size", type=int, default=640)
    ap.add_argument("--dist", type=float, default=0.16, help="camera distance, m")
    ap.add_argument("--boot", type=float, default=9.0, help="page boot wait, s")
    args = ap.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
