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
readouts must match the Python mirror at their published precision. Like
shipcheck, this compares exact displayed strings rather than accepting a
numeric tolerance that could hide a changed decimal place.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from functools import lru_cache
import importlib.util
import json
import pathlib
import subprocess
import sys
from browser_scratch import browser_scratch
from serve import serve_tree
from browser_probe import run_probe

ROOT = pathlib.Path(__file__).resolve().parent.parent
REL_TOL = 1e-9

PROBE = """(async () => {
  const READOUTS = __READOUTS__;
  const B = window.BAND;
  if (!B || !B.ready) return { err: 'window.BAND missing — page did not boot' };
  const out = { samples: {} };
  out.samples.record52crush = B.sample('s1050', 1.0, null, 'harsh', false, false);
  out.samples.frame1450crush = B.sample('s1450', 1.0, null, 'frame', false, false);
  out.samples.frame1450at80 = B.sample('s1450', 1.0, 80.0, 'frame', false, false);
  out.samples.declared52 = B.sample('s1050', 1.2, null, 'harsh', false, false);
  out.samples.bound52 = B.sample('s1050', 1.2, null, 'frame', true, true);
  out.altitudes = []; out.displays = [];
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
        const text = id => document.getElementById(id)?.textContent ?? null;
        out.altitudes.push({world, moves, altitude, band: text('bandV'),
          label: text('bandK'), sf: text('sfFloat'), sfLabel: text('sfFloatK'),
          chartLabel: text('chartNote'),
          cfg: {sigma: 's1450', sf: 1.2, dia: 52, altitude, world, ch: moves, mem: moves, payload: 0},
          readouts: Object.fromEntries(READOUTS.map(id => [id, text(id)])),
          shaded: [...document.querySelectorAll('#chart path')].filter(
            p => p.getAttribute('fill') === 'rgba(80,200,120,0.16)').length});
      }
    }
  }
  for (const cfg of [
    {sigma: 's1050', sf: 1.2, dia: 52, altitude: 0, world: 'harsh', ch: false, mem: false, payload: 0},
    {sigma: 's1450', sf: 1.0, dia: 80, altitude: 1000, world: 'frame', ch: true, mem: false, payload: 10},
    {sigma: 's1450', sf: 1.05, dia: 80, altitude: 0, world: 'frame', ch: false, mem: true, payload: 20},
    {sigma: 's1450', sf: 1.0, dia: 80, altitude: 0, world: 'frame', ch: true, mem: true, payload: 10},
  ]) {
    for (const [id, value] of Object.entries({dia: cfg.dia, alt: cfg.altitude,
         world: cfg.world, sigma: cfg.sigma, sf: cfg.sf, payload: cfg.payload}))
      document.getElementById(id).value = value;
    document.getElementById('chordal').checked = cfg.ch;
    document.getElementById('membrane').checked = cfg.mem;
    document.getElementById('dia').dispatchEvent(new Event('input'));
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    out.displays.push({cfg, readouts: Object.fromEntries(READOUTS.map(id =>
      [id, document.getElementById(id)?.textContent ?? null]))});
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


# Model results only: diaOut, altOut, sfOut and payloadOut echo input controls.
READOUTS = ('crushT', 'sinkSL', 'sinkAlt', 'sfFloat', 'bandV', 'designV',
            'structT', 'payAlt', 'ceilEmpty', 'ceilLoaded')


def displayed(vc, c):
    """Independent physics, formatted to the page's fixed display contract."""
    gi = vc.SHIP0['giKnockdownFrame'] if c['world'] == 'frame' else None

    @lru_cache(maxsize=None)
    def mass(sf):
        try:
            return vc.ship0(c['sigma'], sf, c['dia'], gi, c['ch'], c['mem'])
        except RuntimeError:
            return None  # the section catalog has no such design

    def fixed(value, digits):
        # toLocaleString uses half-up; compare text, as shipcheck does.
        return str(Decimal(repr(float(value))).quantize(
            Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP))

    def tonnes(value):
        return fixed(value, 1)

    def signed(value):
        return ('+' if value >= 0 else '−') + tonnes(abs(value)) + ' t'

    base = mass(1.0)
    if base is None:
        raise ValueError('readout probe configuration is beyond the section catalog')
    crush, lift = base['totalT'], base['liftSLT']
    sink = lift * vc.rho_air(c['altitude']) / vc.rho_air(0)
    band = sink - crush
    altitude = 'sea level' if c['altitude'] == 0 else f"{c['altitude']:,} m"
    sf_float = 'closed'
    if band > 0:
        lo, hi = 1.0, 2.0
        for _ in range(4):
            m = mass(hi)
            if m is None or m['totalT'] >= sink:
                break
            hi *= 1.5
        for _ in range(20):
            mid = (lo + hi) / 2
            m = mass(mid)
            if m is not None and m['totalT'] < sink:
                lo = mid
            else:
                hi = mid
        sf_float = fixed((lo + hi) / 2, 2)
    want = dict(crushT=tonnes(crush) + ' t', sinkSL=tonnes(lift) + ' t',
                sinkAlt=tonnes(sink) + ' t at ' + altitude,
                sfFloat=sf_float, bandV=signed(band))
    design = mass(c['sf'])
    if design is None:
        want.update(designV='beyond the catalog', structT='—', payAlt='—',
                    ceilEmpty='—', ceilLoaded='—')
    else:
        total = design['totalT']
        pay = sink - total
        want.update(structT=tonnes(total) + ' t at SF ' + fixed(c['sf'], 2),
                    payAlt=signed(pay),
                    ceilEmpty=fixed(vc.ship_neutral_ceiling_m(total, lift), 0) + ' m',
                    ceilLoaded=fixed(vc.ship_neutral_ceiling_m(total + c['payload'], lift), 0)
                    + f" m with {c['payload']} t aboard",
                    designV=(f'carries {tonnes(pay)} t at {altitude}' if pay >= 0
                             else f'{tonnes(abs(pay))} t too heavy at {altitude}'))
    return want


def main() -> None:
    spec = importlib.util.spec_from_file_location(
        "vc", ROOT / "research" / "analysis" / "vacuum-cell.py")
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)

    with browser_scratch() as td:
        probe = pathlib.Path(td) / "probe.js"
        probe.write_text(PROBE.replace("__READOUTS__", json.dumps(READOUTS)))
        out = pathlib.Path(td) / "out.json"
        with serve_tree(ROOT) as base:
            js = run_probe(ROOT, f"{base}cell/band.html", probe, out, 10)

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

    for reading in js['displays'] + js['altitudes']:
        for el, want in displayed(vc, reading['cfg']).items():
            checked += 1
            got = reading['readouts'].get(el)
            if got is None or got.replace(',', '') != want.replace(',', ''):
                bad.append(f"cell/band.html #{el} at {reading['cfg']}: "
                           f"page shows {got!r}, Python mirror computes {want!r}")

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
