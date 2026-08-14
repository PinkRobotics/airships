#!/usr/bin/env python3
"""The blueprint page must boot clean, draw every figure, and keep its text on the canvas.

    python3 tools/check_levels.py

The fast gate for cell/levels.html — and the page's ONLY gate, so it checks the failure
modes that have actually shipped:

  * a module error at boot. The figures are drawn by top-level put() calls, so one throw
    blanks every figure after it — this page went out exactly that way once (a figure
    function deleted for rewrite and still called). The page collects window.__errs; any
    entry fails the run.
  * an empty figure. Every <figure class="lvl-fig"> must contain an SVG with enough
    children to be a drawing rather than a stub, and the catalog pane must have mounted.
  * an unresolved number. Every [data-cat] binding must have found its value — a dash is
    the binder's own "path resolves to nothing" mark, and prose carries no digits of its
    own on this page.
  * TEXT OFF THE CANVAS. Every caption burn this arc was a too-long monospace string
    silently clipped by its viewBox — twice on the same day this gate was written. Every
    <text> in every figure (the catalog pane included) must sit inside its SVG's viewBox,
    measured by getBBox in the real renderer, with 2 px of slack.

Deliberately NOT here: model-figure parity (check_explorer and check_cell_parity own the
model; this page reads catalog.js, whose cell figures come from the same model.js) and
anything needing WebGL. This gate is the ~10 s iteration loop for page edits; the full
chain still runs before publish.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = "8911"          # explorer's in-check server uses 8909, the Makefile's 8899

# Figures each page promises today. The probe also sweeps every .lvl-fig it finds, so a
# NEW figure is covered automatically; these lists only pin the known sets against silent
# removal (an id typo'd in HTML simply vanishes — querySelector finds nothing to fill).
# The public engineering page rides the same gate: same binder contract, same failure
# modes, no catalog pane.
PAGES = [
    {"url": "cell/levels.html", "pane": True,
     "figs": ["fig-cell", "fig-cellmass", "fig-band", "fig-ring", "fig-support",
              "fig-webs", "fig-closure", "fig-ledger", "fig-equip"]},
    {"url": "engineering/index.html", "pane": False,
     "figs": ["fig-wall", "fig-walls", "fig-gear"]},
]

PROBE = r"""(() => {
  const out = { errors: window.__errs || [], figs: [], miss: [], overflow: [], paneSvg: false };
  const sweep = (svg, where) => {
    const vb = svg.viewBox.baseVal;
    for (const t of svg.querySelectorAll('text')) {
      const b = t.getBBox();
      if (b.x < vb.x - 2 || b.x + b.width > vb.x + vb.width + 2 ||
          b.y < vb.y - 2 || b.y + b.height > vb.y + vb.height + 2)
        out.overflow.push({ where, text: (t.textContent || '').slice(0, 44),
                            x: +b.x.toFixed(1), right: +(b.x + b.width).toFixed(1),
                            y: +b.y.toFixed(1), bottom: +(b.y + b.height).toFixed(1),
                            vbw: vb.width, vbh: vb.height });
    }
  };
  for (const f of document.querySelectorAll('figure.lvl-fig')) {
    const svg = f.querySelector('svg');
    out.figs.push({ id: f.id, kids: svg ? svg.children.length : 0 });
    if (svg) sweep(svg, f.id);
  }
  const pane = document.querySelector('#pane-a svg');
  if (pane) { out.paneSvg = true; sweep(pane, 'catalog pane'); }
  out.fignos = [...document.querySelectorAll('figure.lvl-fig .figno')].map(e => e.textContent);
  for (const el of document.querySelectorAll('[data-cat]'))
    if (el.classList.contains('miss') || el.textContent.trim() === '—')
      out.miss.push(el.dataset.cat);
  return out;
})()"""


def check_page(page, td) -> tuple[list[str], int]:
    probe = pathlib.Path(td) / "probe.js"
    probe.write_text(PROBE)
    out = pathlib.Path(td) / f"out-{page['url'].replace('/', '-')}.json"
    subprocess.run([sys.executable, str(ROOT / "tools" / "js_eval.py"),
                    f"http://127.0.0.1:{PORT}/{page['url']}",
                    str(probe), str(out), "8"], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
    res = json.loads(out.read_text())

    bad = []
    for e in res.get("errors", []):
        bad.append(f"page error at boot: {e}")
    seen = {f["id"]: f["kids"] for f in res.get("figs", [])}
    for fid in page["figs"]:
        if fid not in seen:
            bad.append(f"#{fid} is missing from the page")
    for fid, kids in seen.items():
        if kids < 3:
            bad.append(f"#{fid} drew {kids} SVG children — an empty or stub figure")
    if page["pane"] and not res.get("paneSvg"):
        bad.append("the catalog pane mounted no part drawing")
    want_nos = [f"fig {i + 1}" for i in range(len(seen))]
    if res.get("fignos") != want_nos:
        bad.append(f"figure numbers read {res.get('fignos')} — every figure carries "
                   "'fig N' in document order, or the operator cannot name what he sees")
    for path in res.get("miss", []):
        bad.append(f"data-cat=\"{path}\" resolved to nothing — the binder shows a dash")
    for o in res.get("overflow", []):
        bad.append(f"text clipped by its viewBox in {o['where']}: \"{o['text']}\" spans "
                   f"x {o['x']}..{o['right']} of {o['vbw']}, "
                   f"y {o['y']}..{o['bottom']} of {o['vbh']}")
    return [f"{page['url']}: {b}" for b in bad], len(seen)


def main() -> int:
    bad, figs = [], []
    with tempfile.TemporaryDirectory(dir=str(pathlib.Path.home() / "tmp")) as td:
        srv = subprocess.Popen([sys.executable, str(ROOT / "tools" / "serve.py"),
                                "--port", PORT, "--quiet"], cwd=ROOT)
        try:
            for page in PAGES:
                page_bad, n = check_page(page, td)
                bad += page_bad
                figs.append(f"{page['url']} {n}")
        finally:
            srv.terminate()
            srv.wait()

    if bad:
        print("LEVELS CHECK FAILED:\n")
        for b in bad:
            print(f"  {b}")
        return 1
    print(f"levels: {len(PAGES)} pages booted with no page errors ({', '.join(figs)} "
          "figures drawn), the catalog pane mounted, all number bindings resolved, "
          "every caption inside its viewBox.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
