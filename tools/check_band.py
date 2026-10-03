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
from browser_scratch import browser_scratch
from serve import serve_tree

ROOT = pathlib.Path(__file__).resolve().parent.parent
REL_TOL = 1e-9

PROBE = """(async () => {
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
  out.altitudes = [];
  for (const world of ['harsh', 'frame']) {
    for (const moves of [false, true]) {
      for (const altitude of [0, 2500]) {
        for (const [id, value] of Object.entries({dia: 52, alt: altitude,
             world, sigma: 's1450', sf: 1.2}))
          document.getElementById(id).value = value;
        for (const id of ['chordal', 'membrane'])
          document.getElementById(id).checked = moves;
        document.getElementById('alt').dispatchEvent(new Event('input'));
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        const text = id => document.getElementById(id).textContent;
        out.altitudes.push({world, moves, altitude, band: text('bandV'),
          label: text('bandK'), sf: text('sfFloat'), sfLabel: text('sfFloatK'),
          chartLabel: text('chartNote'),
          shaded: [...document.querySelectorAll('#chart path')].filter(
            p => p.getAttribute('fill') === 'rgba(80,200,120,0.16)').length});
      }
    }
  }
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

    with browser_scratch() as td:
        probe = pathlib.Path(td) / "probe.js"
        probe.write_text(PROBE)
        out = pathlib.Path(td) / "out.json"
        with serve_tree(ROOT) as base:
            subprocess.run([sys.executable, str(ROOT / "tools" / "js_eval.py"),
                            f"{base}cell/band.html", str(probe),
                            str(out), "10"], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL)
            js = json.loads(out.read_text())

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

    for reading in js["altitudes"]:
        altitude = reading["altitude"]
        where = f"{reading['world']}, moves={reading['moves']}, altitude={altitude}"
        gi = vc.SHIP0["giKnockdownFrame"] if reading["world"] == "frame" else None
        result = vc.ship0("s1450", 1.0, 52.0, gi, reading["moves"], reading["moves"])
        lift = result["liftSLT"] if altitude == 0 else result["lift2500T"]
        band = lift - result["totalT"]
        want = f"{'+' if band >= 0 else '−'}{abs(band):,.1f} t"
        checked += 1
        if reading["band"] != want:
            bad.append(f"{where}: selected-altitude band {reading['band']!r}, expected {want!r}")
        label = "sea level" if altitude == 0 else "2,500 m"
        for field in ("label", "sfLabel", "chartLabel"):
            checked += 1
            if label not in reading[field]:
                bad.append(f"{where}: {field} missing altitude label {label!r}: {reading[field]!r}")
        checked += 1
        if "a design exists" in reading["label"].lower():
            bad.append(f"{where}: a mass band does not establish that a design exists")
        checked += 1
        if band <= 0 and ("closed" not in reading["label"] or reading["sf"] != "closed"):
            bad.append(f"{where}: closed band was labelled open or given a float factor")
        if band > 0 and ("open" not in reading["label"] or reading["sf"] == "closed"):
            bad.append(f"{where}: positive band did not exercise the open branch")
        checked += 1
        if altitude == 2500 and reading["shaded"]:
            bad.append(f"{where}: chart shades a sea-level band under the 2,500 m selection")
        if altitude == 0 and reading["world"] == "frame" and not reading["shaded"]:
            bad.append(f"{where}: positive sea-level chart band was not shaded")

    if bad:
        print("check_band: MISMATCH — the calculator is not the model:")
        for b in bad:
            print(f"  {b}")
        sys.exit(1)
    print(f"band calculator: page boots, {checked} values solved live in the "
          "browser match the Python mirror at off-record hulls, SF 1.0, and "
          "the bound view; eight altitude selections keep band values, labels, verdicts and shading consistent.")


if __name__ == "__main__":
    main()
