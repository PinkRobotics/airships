#!/usr/bin/env python3
"""Shared machinery for the gates that drive the served page headless.

One local server, one probe script, one browser at a time — and the scans every page
gate runs: the effect-claims refusal over every string the page holds, and the live-words
rule for views that are not the live feed. Extracted from the retired guard gate when the
guard was removed (2026-10); the honesty scans survive it because the honest labels are
the page's own rule, not the guard's.
"""
import http.server
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from serve import serve_tree  # noqa: E402
TOOLS = ROOT / "tools"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):
        pass


def serve(missing=()):
    """A local server for the repository. `missing`: path fragments it answers 404 for —
    a deployment with a file gone."""
    class Broken(Handler):
        def do_GET(self):
            if any(m in self.path for m in missing):
                self.send_error(404)
                return
            super().do_GET()
    return serve_tree(ROOT, handler=Broken if missing else Handler)


def probe_once(base: str, query: str, script: str, wait: float, viewport=None):
    """One headless load of one view. Returns the parsed record."""
    with tempfile.TemporaryDirectory(dir=os.environ.get("AIRSHIPS_TMPDIR") or None) as tmp:
        js = pathlib.Path(tmp) / "probe.js"
        js.write_text(script)
        out = pathlib.Path(tmp) / "out.json"
        env = dict(os.environ)
        if viewport:
            env["A3D_VIEWPORT"] = viewport
        r = subprocess.run(
            [sys.executable, str(TOOLS / "js_eval.py"),
             f"{base}index.html{query}", str(js), str(out), str(wait)],
            cwd=str(ROOT), capture_output=True, text=True, env=env, timeout=420)
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"the probe of {query!r} did not run:\n{r.stdout}\n{r.stderr}")
        return json.loads(out.read_text())


# What one view is asked, in the page, after it has booted. Everything the tests assert on
# comes back in one record; nothing is asserted inside the browser.
PROBE = r"""
(async () => {
  // The page publishes readiness after boot; route planning yields between missions.
  // Navigation time is not proof of completion on a loaded hosted runner.
  const deadline = performance.now() + 300000;
  while (!(window.AIRSHIPS?.app?.ready && (window.AIRSHIPS.app.recordOnly || window.AIRSHIPS.app.planning?.state === 'settled'))) {
    if (performance.now() >= deadline) throw new Error('probe: readiness deadline exceeded (300 s)');
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  const S = window.AIRSHIPS.app;
  const ov = document.getElementById('introOv'); if (ov && !ov.hidden) ov.click();
  await new Promise(r => setTimeout(r, 1200));
  S.paused = true;
  const txt = id => { const e = document.getElementById(id); return e ? e.textContent.replace(/\s+/g,' ').trim() : null; };
  const meta = sel => { const e = document.querySelector(sel); return e ? e.content : null; };
  const out = {
    url: location.search, day: S.day, daySource: S.daySource,
    recordOnly: !!S.recordOnly, unknownDay: S.unknownDay,
    standDown: S.standDown, seasonNote: S.seasonNote || null,
    dataNote: S.dataNote || null,
    fires: S.fires.length,
    missions: S.missions.length,
    flying: S.missions.filter(m => !m.idle).length,
    uncovered: S.uncovered,
    // `ops` is the operation panel (#cpOps) and `heads` the two panel headings with the
    // fires panel's note. An earlier probe read #ops and #stats, ids the page no longer
    // has, so every assertion on those two keys held on an empty string.
    panels: { roster: txt('roster'), firesTop: txt('firesTop'),
              heads: [txt('fleetH'), txt('firesH'), txt('firesNote')].join(' | '),
              ops: txt('cpOps'), mode: txt('modeNote'), sceneNote: txt('sceneNote'),
              heat: txt('heatNote'), hud: txt('hudLive') },
    labels: {
      title: document.title,
      description: meta('meta[name="description"]'),
      ogTitle: meta('meta[property="og:title"]'),
      ogDescription: meta('meta[property="og:description"]'),
      fires: txt('fireModeLabel'), fleet: txt('fleetModeLabel'),
      day: (() => { const a = document.querySelector('#dayRow a[aria-current]');
                    return a ? a.textContent.replace(/\s+/g, ' ').trim() : null; })(),
      map: document.getElementById('map').getAttribute('aria-label'),
      mapHelp: txt('mapHelp'),
      // The first-visit screen's four phrases that name the view, and whether the fleet
      // note under the roster ("The fleet is simulated…") is laid out.
      intro: ['introTapH', 'introMapH', 'introMapP', 'introFires'].map(txt).join(' | '),
      fleetNote: (() => { const e = document.getElementById('fleetNote');
                          return e ? getComputedStyle(e).display !== 'none' : null; })(),
    },
    visible: [],
  };
  // The raw material for the honesty scans: every string the page shows, own text nodes
  // plus the attributes a reader meets without a pointer — title, aria-label, alt.
  const seen = [];
  for (const el of document.body.querySelectorAll('*')) {
    const own = [...el.childNodes].filter(n => n.nodeType === 3)
      .map(n => n.textContent.replace(/\s+/g, ' ').trim()).filter(Boolean);
    if (own.length) seen.push(own.join(' '));
    for (const a of ['title', 'aria-label', 'alt']) {
      const v = el.getAttribute && el.getAttribute(a);
      if (v) seen.push(v);
    }
  }
  seen.push(document.title);
  for (const meta of document.querySelectorAll("meta[content]")) seen.push(meta.content);
  out.visible = seen;
  return JSON.stringify(out);
})()
"""

# The layout probe: the orientation cards and the roster at four widths, plus the mode
# sentence's place among the chips. Runs on the sample route, where the first-visit
# screen is up.
LAYOUT = r"""
(async () => {
  // Wait for the real first-visit screen after asynchronous data and plan acceptance.
  // Static cards exist while hidden; they do not establish that boot completed.
  // The page publishes readiness after boot; route planning yields between missions.
  // Navigation time is not proof of completion on a loaded hosted runner.
  const deadline = performance.now() + 300000;
  while (!(document.getElementById('introOv') && !document.getElementById('introOv').hidden && document.querySelector('#introOv .io'))) {
    if (performance.now() >= deadline) throw new Error('layout: readiness deadline exceeded (300 s)');
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  const ov = document.getElementById('introOv');
  const visible = !!(ov && !ov.hidden);
  const cards = visible ? [...document.querySelectorAll('#introOv .io')].map(e => {
    const r = e.getBoundingClientRect();
    return { cls: (e.className.match(/io-\w+/) || [''])[0], x: r.x, y: r.y, w: r.width, h: r.height };
  }).filter(c => c.w > 0 && c.h > 0) : [];   // under the phone breakpoint the call-outs hide
  const overlaps = [];
  for (let i = 0; i < cards.length; i++)
    for (let j = i + 1; j < cards.length; j++) {
      const a = cards[i], b = cards[j];
      const x = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
      const y = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
      if (x > 1 && y > 1) overlaps.push([a.cls, b.cls]);
    }
  const outside = cards.filter(c => c.x < 0 || c.y < 0
    || c.x + c.w > innerWidth || c.y + c.h > innerHeight).map(c => c.cls);
  const rows = [...document.querySelectorAll('#roster .r-cls')].map(e => ({
    text: e.textContent.slice(0, 34), over: e.scrollWidth - e.clientWidth }));
  // The mode sentence against the chips it sits with: it must be on screen, inside the
  // map's box, and under no chip, however many rows the chips wrap to.
  const note = document.getElementById('modeNote'), nr = note.getBoundingClientRect();
  const box = document.getElementById('map').getBoundingClientRect();
  const chipsOver = [...document.querySelectorAll('.hud .chip')].filter(e => {
    const r = e.getBoundingClientRect();
    return r.width > 0 && Math.min(r.right, nr.right) > Math.max(r.left, nr.left) + 1
      && Math.min(r.bottom, nr.bottom) > Math.max(r.top, nr.top) + 1;
  }).map(e => e.id || e.textContent.slice(0, 20));
  return JSON.stringify({
    vw: innerWidth, vh: innerHeight, overlay: visible, cards: cards.length,
    overlaps, outside,
    note: { text: note.textContent.length, w: Math.round(nr.width), h: Math.round(nr.height),
            chipsOver, outsideMap: nr.left < box.left - 1 || nr.right > box.right + 1 || nr.top < box.top - 1 },
    clsRows: rows.length,
    clipped: rows.filter(r => r.over > 1),
  });
})()
"""


# The effect-claims refusal. The one place "would have" is allowed is inside the mandated
# fleet sentence itself, whose whole point is to refuse the claim; the sentence is stripped
# before the scan, and so are the complete denial sentences.
TIME = r"\d{1,2}:\d{2} on [A-Za-z]+ \d{1,2}, \d{4}"
MANDATED_FLEET = re.compile(
    rf"(Replay|Live) of \d{{4}}-\d{{2}}-\d{{2}}: the fires as British Columbia published them "
    rf"at {TIME}\. The fleet is simulated and never flew\. Its drops are water released, not "
    r"water arrived, and nothing here says any fire would have burned differently\.")
DENIALS = [
    "water released is not fire extinguished",
    "none of it says whether this fire grows or is contained",
    "nothing here says any fire would have burned differently",
]
REFUSED = [("protecting", re.compile(r"\bprotecting\b", re.I)),
           ("shields", re.compile(r"\bshields\b", re.I)),
           ("fire extinguished", re.compile(r"fire extinguished", re.I)),
           ("is contained", re.compile(r"is contained", re.I)),
           ("would have", re.compile(r"\bwould have\b")),
           ("could have", re.compile(r"\bcould have\b")),
           ("saved", re.compile(r"\bsaved\b", re.I)),
           ("prevented", re.compile(r"\bprevented\b", re.I)),
           ("stopped the fire", re.compile(r"stopped the fire"))]


def refuse_words(name, strings):
    """The honesty scan: strip the mandated sentence (the refusal itself) and the complete
    denials, then refuse the rest."""
    hits = []
    for s in strings:
        t = MANDATED_FLEET.sub("", s)
        for denial in DENIALS:
            t = re.sub(re.escape(denial), "", t, flags=re.I)
        for what, pat in REFUSED:
            m = pat.search(t)
            if m:
                hits.append(f"{name} says {what!r}: …{t[max(0, m.start()-50):m.end()+30]}…")
    assert not hits, "\n          ".join(hits[:6])


# Uses of "live", "current" and "today" that claim nothing about the fire data on screen.
# Whole phrases, so that a new label with one of these words fails here until someone has
# read it and ruled on it.
LIVE_WORDS = re.compile(r"\b(live|current|currently|today|today's)\b", re.I)
NOT_A_LIVE_CLAIM = (
    "with live force vectors",                          # the schematic follows the simulation
    "Nothing floats today as drawn",                    # the float ledger's verdict
    "Currently in frame:",                              # what the map frame holds
    "Current constraint:",                              # the simulated cycle's binding limit
    "its current phase",                                # the roster's third column
)


def fallback_regions():
    """The regions tools/gen_fallback.py writes, as (name, text)."""
    html = (ROOT / "index.html").read_text()
    out = []
    for name in ("FALLBACK-FLEET-HEADING", "FALLBACK-HUD", "FALLBACK-ROSTER",
                 "FALLBACK-FIRES", "FALLBACK-DAYROW", "FALLBACK"):
        m = re.search(r"<!--" + name + r"-->(.*?)<!--/" + name + r"-->", html, re.S)
        assert m, f"index.html has no {name} region"
        out.append((name, m.group(1)))
    return out
