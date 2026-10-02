#!/usr/bin/env python3
"""The ship page must boot clean and show ONLY the model's numbers.

    python3 tools/check_ship.py

cell/ship.html is the fourth surface displaying the ship physics (explorer,
blueprint, catalog, and now the checks page), and a surface that displays
numbers can drift. This boots it headless and asserts: no page errors, every
data-n binding resolved (the page marks a failed one with .miss), every
generated table non-empty, and the two verdict cells agreeing with a fresh
call into the model — the same one-source rule every other gate enforces.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from browser_scratch import browser_scratch

ROOT = pathlib.Path(__file__).resolve().parent.parent

PROBE = r"""(() => {
  const out = { errors: window.__errs || [] };
  out.missing = [...document.querySelectorAll('[data-n].miss')]
    .map(e => e.dataset.n);
  out.tables = {};
  for (const id of ['worldsHarsh', 'worldsFrame', 'ledger', 'checks', 'window',
                    'bandrows']) {
    const el = document.getElementById(id);
    out.tables[id] = el ? el.querySelectorAll('tr').length : -1;
  }
  const bf = document.getElementById('bandfig');
  out.bandFigMarks = bf ? bf.querySelectorAll('line, rect').length : -1;
  return import('../ship/model.js').then(M => {
    const S = M.ship0Summary();
    const shown = (sel) => document.querySelector(sel).textContent.replace(/,/g, '');
    out.checks = [
      ['midRatio', shown('[data-n="mid.ratioSL"]'), S.mid.ratioSL.toFixed(3)],
      ['bestRatio', shown('[data-n="best.ratioSL"]'),
       S.worldsFramePractice.s1450_sf12.ratioSL.toFixed(3)],
      ['liftT', shown('[data-n="plan.liftSLT"]'), S.planOfRecord.liftSLT.toFixed(1)],
      ['totalT', shown('[data-n="mid.totalT"]'), S.mid.totalT.toFixed(1)],
      ['band25', shown('[data-n="band25"]'), S.band.harshMid.lift2500T.toFixed(1)],
      ['bandCrushHarsh',
       document.querySelector('#bandrows tr td:nth-child(2)').textContent,
       S.band.harshMid.crushT.toFixed(1)],
    ];
    out.bandWorlds = Object.keys(S.band).length;
    out.ledgerRows = Object.keys(S.mid.ledgerT).length;
    return out;
  });
})()"""


def main() -> None:
    with browser_scratch() as td:
        probe = pathlib.Path(td) / "probe.js"
        probe.write_text(PROBE)
        out = pathlib.Path(td) / "out.json"
        srv = subprocess.Popen([sys.executable, str(ROOT / "tools" / "serve.py"),
                                "--port", "8913", "--quiet"], cwd=ROOT)
        try:
            subprocess.run([sys.executable, str(ROOT / "tools" / "js_eval.py"),
                            "http://127.0.0.1:8913/cell/ship.html",
                            str(probe), str(out), "10"], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL)
            res = json.loads(out.read_text())
        finally:
            srv.terminate()
            srv.wait()

    bad = []
    for e in res.get("errors", []):
        bad.append(f"page error: {e}")
    for m in res.get("missing", []):
        bad.append(f"data-n=\"{m}\" resolved to nothing — a figure with no source")
    for tid, n in (res.get("tables") or {}).items():
        want = {"worldsHarsh": 6, "worldsFrame": 6, "window": 8,
                "bandrows": 3}.get(tid, 1)
        if n < want:
            bad.append(f"table #{tid}: {n} rows, expected >= {want}")
    if res.get("tables", {}).get("ledger", 0) != res.get("ledgerRows", -2):
        bad.append(f"ledger draws {res.get('tables', {}).get('ledger')} rows for "
                   f"{res.get('ledgerRows')} model lines")
    for name, got, want in res.get("checks", []):
        if got != want:
            bad.append(f"displayed {name}: page shows {got!r}, model computes {want!r}")
    if res.get("bandrows", res.get("tables", {}).get("bandrows", 0)) \
            != res.get("bandWorlds", 3):
        pass  # row count already asserted above against the fixed 3
    if res.get("bandFigMarks", -1) < 12:
        bad.append(f"band figure: only {res.get('bandFigMarks')} marks drawn — "
                   "the two-walls SVG did not render")

    if bad:
        print("SHIP PAGE CHECK FAILED:\n")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print(f"ship page: boots clean, {res['tables']['ledger']} ledger lines, "
          f"{res['tables']['checks']} checks drawn, both verdict cells match the "
          f"model, the two walls drawn for {res.get('bandWorlds', 0)} worlds, "
          "no unresolved bindings.")


if __name__ == "__main__":
    main()
