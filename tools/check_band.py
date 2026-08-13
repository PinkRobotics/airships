#!/usr/bin/env python3
"""cell/band.html — the band calculator — must solve the SAME physics the Python
mirror solves, at OFF-record configurations too.

    python3 tools/check_band.py

The calculator is the first page that runs the gated ship model at arbitrary
(hull, SF, world, moves) tuples, so the 345-value record parity alone cannot
vouch for it. This gate boots the page in a real browser, has its probe surface
(window.BAND.sample) solve a spread of tuples — the record hull at the crush
boundary, the friendliest world, an off-record 80 m hull, and a BOUND view with
both SHIP-3 moves on — and diffs every number against the Python mirror solving
the identical tuples. It also asserts the page actually rendered: the wall
readouts must carry numbers, not placeholders.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
REL_TOL = 1e-9

PROBE = """(() => {
  const B = window.BAND;
  if (!B || !B.ready) return { err: 'window.BAND missing — page did not boot' };
  const out = { dom: {}, samples: {} };
  out.samples.record52crush = B.sample('s1050', 1.0, null, 'harsh', false, false);
  out.samples.frame1450crush = B.sample('s1450', 1.0, null, 'frame', false, false);
  out.samples.frame1450at80 = B.sample('s1450', 1.0, 80.0, 'frame', false, false);
  out.samples.declared52 = B.sample('s1050', 1.2, null, 'harsh', false, false);
  out.samples.bound52 = B.sample('s1050', 1.2, null, 'frame', true, true);
  for (const id of ['crushT', 'sinkSL', 'sinkAlt', 'bandV', 'structT',
                    'ceilEmpty', 'ceilLoaded', 'payAlt'])
    out.dom[id] = document.getElementById(id).textContent;
  return out;
})()"""

SAMPLES = {
    # name: (sigma_key, sf, dia_m, world, chordal, membrane)
    "record52crush": ("s1050", 1.0, None, "harsh", False, False),
    "frame1450crush": ("s1450", 1.0, None, "frame", False, False),
    "frame1450at80": ("s1450", 1.0, 80.0, "frame", False, False),
    "declared52": ("s1050", 1.2, None, "harsh", False, False),
    "bound52": ("s1050", 1.2, None, "frame", True, True),
}


def main() -> None:
    spec = importlib.util.spec_from_file_location(
        "vc", ROOT / "research" / "analysis" / "vacuum-cell.py")
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)

    with tempfile.TemporaryDirectory(dir=str(pathlib.Path.home() / "tmp")) as td:
        probe = pathlib.Path(td) / "probe.js"
        probe.write_text(PROBE)
        out = pathlib.Path(td) / "out.json"
        srv = subprocess.Popen([sys.executable, str(ROOT / "tools" / "serve.py"),
                                "--port", "8911", "--quiet"], cwd=ROOT)
        try:
            subprocess.run([sys.executable, str(ROOT / "tools" / "js_eval.py"),
                            "http://127.0.0.1:8911/cell/band.html", str(probe),
                            str(out), "10"], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL)
            js = json.loads(out.read_text())
        finally:
            srv.terminate()
            srv.wait()

    if "err" in js:
        sys.exit(f"check_band: {js['err']}")

    bad = []
    checked = 0

    def cmp(name: str, want: float, got: float) -> None:
        nonlocal checked
        checked += 1
        scale = max(abs(want), abs(got), 1e-12)
        if abs(want - got) / scale > REL_TOL:
            bad.append(f"{name}: python {want!r}, js {got!r}")

    for name, (key, sf, dia, world, ch, mem) in SAMPLES.items():
        gi = vc.SHIP0["giKnockdownFrame"] if world == "frame" else None
        r = vc.ship0(key, sf, dia, gi, ch, mem)
        want = dict(totalT=r["totalT"], liftSLT=r["liftSLT"],
                    ceilM=vc.ship_neutral_ceiling_m(r["totalT"], r["liftSLT"]))
        got = js["samples"].get(name)
        if got is None:
            bad.append(f"{name}: missing from the JS probe")
            continue
        for k in ("totalT", "liftSLT", "ceilM"):
            cmp(f"{name}.{k}", want[k], got[k])

    for el, text in js["dom"].items():
        checked += 1
        if text.strip() in ("", "—", "-"):
            bad.append(f"page: #{el} rendered '{text}' — the calculator did "
                       "not solve on boot")

    if bad:
        print("check_band: MISMATCH — the calculator is not the model:")
        for b in bad:
            print(f"  {b}")
        sys.exit(1)
    print(f"band calculator: page boots, {checked} values solved live in the "
          "browser match the Python mirror at off-record hulls, SF 1.0, and "
          "the bound view.")


if __name__ == "__main__":
    main()
