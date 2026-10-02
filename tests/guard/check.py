#!/usr/bin/env python3
"""The guard gate: the ruling pinned in its file, and proved on the page.

The guard is the project's rule that a tragedy is never replayed with a better ending,
carried as data (data/season/2026.guard.json) and enforced in code (sim/guard.js). This
gate holds both halves to the ruling, R by R:

    the file     R8 — the canonical digest is pinned, so widening a window or softening a
                 distance is a deliberate two-place edit; the window and the distances are
                 the file's to say, and sim/guard.js carries no date of its own.
    the block    R1/R7 — the static fallback names its day, carries the exact fleet
                 sentence, and names no guarded fire.
    the page     R1 — a record-only day has no missions, no regions and no fleet figures
                 anywhere in its rendered text;
                 R2 — the sample routes (the mirror failing, ?data=snapshot) land on the
                 newest fleet day, never on a day inside the window;
                 R3 — no mission's fire is guarded, and no guarded fire's name reaches the
                 roster, the fires panel or the operation text on a fleet day;
                 R4 — the ships themselves stay out: every mission's fixed points and a
                 dense sweep of stateAt positions across three cycles are checked against
                 the day's keep-out regions, in the page, on every fleet day;
                 R6 — a date with no day file stands the fleet down and says so in words;
                 R7 — the mode sentence and the guard note match the ruled sentences
                 exactly (only the braces filled), and no other visible string on any view
                 says a fire would have burned differently.
    the layout   the orientation cards and the roster at three widths — the two defects
                 the guard work found at 1440 px (cards overlapping, class rows clipping),
                 held so they stay fixed.

    tests/guard/check.py            everything (this is what `make guardcheck` runs)
    tests/guard/check.py <word>     only the tests whose name has the word

Exit status is non-zero on any failure. Requires python3, chromium on PATH and the
`websockets` package (tools/js_eval.py uses it). No node, no network beyond 127.0.0.1.
"""
import asyncio
import http.server
import json
import os
import pathlib
import re
import shutil
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TOOLS = ROOT / "tools"
GUARD = ROOT / "data" / "season" / "2026.guard.json"

YEAR = 2026

# ---- the pins -------------------------------------------------------------------------------
# R8. The digest is of the file's CANONICAL form (parsed, then sort_keys + compact
# separators), not its bytes: a formatting change is not a policy change. Anyone editing
# the guard file on purpose changes this pin in the same commit, by hand, and says why.
PIN = {
    "canonicalSha256": "d8fa369ffa1dbb724cc76cbaa9cc306187fa89b2e47bd6e32d6a49aab38f3c15",
    "window": {"from": "2026-08-08", "to": "2026-08-27"},        # the provincial emergency
    "defaultKeepOutKm": 25,
    "fires": 22,
    "tiers": {1: 8, 2: 7, 3: 7},
    "places": 2,
    "noteKm": 25,                                                 # the widest kept distance
}

# The window's captured days, first to last captured. The captures end at 08-15: the
# window itself runs to 08-27, and that final week was never captured — so its last day
# is held by the R6 test below (a date inside the window, with no day file, still stands
# the fleet down) rather than by the record-day test, which needs a record to show.
RECORD_DAYS = ["2026-08-08", "2026-08-11", "2026-08-15"]
FLEET_DAYS = ["2026-09-20", "2026-09-22", "2026-10-01"]
SAMPLE_DAY = "2026-10-01"                                          # the newest fleet day
UNKNOWN_DAY = "2026-07-01"                                         # no day file exists
NO_DAY_IN_WINDOW = "2026-08-27"                                    # the window's last day, no capture

# R7. The sentences the ruling fixed, as patterns: only the braced parts vary. {time} is
# filled by vancouverClock() as "19:01 on October 1, 2026" — clock and spelled-out date.
TIME = r"\d{1,2}:\d{2} on [A-Za-z]+ \d{1,2}, \d{4}"


def record_sentence(day):
    return re.compile(
        rf"^{re.escape(day)}: the fires as British Columbia published them at {TIME}\. "
        r"No fleet is simulated for 8 to 27 August 2026\. The province was under a state of "
        r"emergency, and this page does not replay those days with a different ending\.$")


def fleet_sentence(day):
    return re.compile(
        rf"^(Replay|Live) of {re.escape(day)}: the fires as British Columbia published them "
        rf"at {TIME}\. The fleet is simulated and never flew\. Its drops are water released, "
        r"not water arrived, and nothing here says any fire would have burned differently\.$")


GUARD_NOTE = re.compile(
    r"^The simulated fleet never works a fire that was a wildfire of note or led to an "
    rf"evacuation order or alert, and it keeps {PIN['noteKm']} km from those that forced "
    r"people out\. The list and its sources are in data/season/2026\.guard\.json\.$")
# The one place "would have" is allowed is inside the mandated fleet sentence itself, whose
# whole point is to refuse the claim. The sentence is stripped before the scan.
MANDATED_FLEET = re.compile(
    rf"(Replay|Live) of \d{{4}}-\d{{2}}-\d{{2}}: the fires as British Columbia published them "
    rf"at {TIME}\. The fleet is simulated and never flew\. Its drops are water released, not "
    r"water arrived, and nothing here says any fire would have burned differently\.")
REFUSED = [("would have", re.compile(r"\bwould have\b")),
           ("could have", re.compile(r"\bcould have\b")),
           ("saved", re.compile(r"\bsaved\b")),
           ("prevented", re.compile(r"\bprevented\b")),
           ("stopped the fire", re.compile(r"stopped the fire"))]

# What may not appear in the rendered panels of a record-only day (R1: nothing of the
# fleet — no ship, no rate, no queue, no energy figure). Calibrated against the shipped
# page: anything here that turns up on a fleet day's same panels is a fleet artefact.
BANNED_ON_RECORD_DAYS = ["kL/h", "queued", "not flown", "hull", "Kingfisher", "battery",
                         "MW", "t of water", "priority"]

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def same(got, want, what):
    assert got == want, f"{what}: got {got!r}, expected {want!r}"


def load_guard():
    return json.loads(GUARD.read_bytes())


# ============================================================================================
# 1. THE FILE (R8) — pure arithmetic, no browser
# ============================================================================================
@test
def the_guard_file_is_pinned_by_its_canonical_digest():
    doc = load_guard()
    canon = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()
    import hashlib
    same(hashlib.sha256(canon).hexdigest(), PIN["canonicalSha256"],
         "the canonical digest of data/season/2026.guard.json (R8: edit the file on purpose, "
         "then change this pin in the same commit and say why)")
    return "digest d8fa369f…38f3c15 holds"


@test
def the_window_and_the_distances_are_the_file_s_to_say():
    """R8 the other way round: the code carries no date and no distance of its own. If a
    window ever moves out of the file and into sim/guard.js, this is what notices."""
    doc = load_guard()
    same([(w["from"], w["to"]) for w in doc["noFleet"]],
         [(PIN["window"]["from"], PIN["window"]["to"])], "the no-fleet window")
    same(doc["defaultKeepOutKm"], PIN["defaultKeepOutKm"], "the default distance")
    same(len(doc["fires"]), PIN["fires"], "listed fires")
    same(len(doc["places"]), PIN["places"], "places")
    tiers = {}
    for e in doc["fires"]:
        tiers[e["tier"]] = tiers.get(e["tier"], 0) + 1
    same(tiers, PIN["tiers"], "fires by tier")
    src = (ROOT / "sim" / "guard.js").read_text()
    assert not re.search(r"\d{4}-\d{2}-\d{2}", src), (
        "sim/guard.js carries a date literal: the window belongs in the guard file, not the code")
    # Distances are not regex-checked the same way: the module's arithmetic and its comments
    # legitimately speak of kilometres. What pins a number to a policy is the digest above
    # plus the unit tests (tests/cases/guard.cases.js), which feed the module invented
    # files and assert it obeys THEIR numbers, not any of its own.
    # every entry rests on exactly one public link, and the file names nobody: it quotes
    # nothing longer than a fire's own published name
    for e in doc["fires"] + doc["places"]:
        same(len(re.findall(r"https?://", e["source"])), 1, f"{e['name']}: one source link")
    for e in doc["fires"]:
        assert len(e["name"]) <= 40, f"{e['name']}: a name field long enough to be a quotation"
    return (f"window {PIN['window']['from']} to {PIN['window']['to']}, {PIN['fires']} fires "
            f"({PIN['tiers'][1]}+{PIN['tiers'][2]}+{PIN['tiers'][3]}), {PIN['places']} places, "
            "and no date or distance literal in sim/guard.js")


# ============================================================================================
# 2. THE STATIC FALLBACK (R1/R7) — pure text, no browser
# ============================================================================================
def fallback_regions():
    """The four regions tools/gen_fallback.py writes, as (name, text)."""
    html = (ROOT / "index.html").read_text()
    out = []
    for name in ("FALLBACK-HUD", "FALLBACK-ROSTER", "FALLBACK-FIRES", "FALLBACK"):
        m = re.search(r"<!--" + name + r"-->(.*?)<!--/" + name + r"-->", html, re.S)
        assert m, f"index.html has no {name} region"
        out.append((name, m.group(1)))
    return out


@test
def the_static_fallback_names_its_day_and_no_guarded_fire():
    doc = load_guard()
    plain = " ".join(text for _, text in fallback_regions())
    squeezed = " ".join(plain.split())
    assert SAMPLE_DAY in squeezed, "the fallback does not name the day it is a record of"
    for e in doc["fires"]:
        assert e["fire"] not in plain, f"the fallback names the guarded fire {e['fire']}"
        # a name match is only a hit where it is the fire being named, not a shared word:
        # match on the entry's full name, case-insensitively, as a whole phrase
        assert not re.search(re.escape(e["name"]), plain, re.I), (
            f"the fallback names the guarded fire {e['name']} ({e['fire']})")
    for p in doc["places"]:
        assert p["name"] not in plain, f"the fallback names the guarded place {p['name']}"
    return f"{len(fallback_regions())} regions checked against {PIN['fires']} guarded fires"


@test
def the_static_fallback_carries_the_ruled_sentences():
    texts = [t for _, t in fallback_regions()]
    joined = " ".join(" ".join(t.split()) for t in texts)
    stripped = MANDATED_FLEET.sub("", joined)
    for what, pat in REFUSED:
        m = pat.search(stripped)
        assert not m, f"the static fallback says {what!r}: …{stripped[max(0, m.start()-60):m.end()+40]}…"
    same(len(MANDATED_FLEET.findall(joined)), 1, "the exact fleet sentence, once")
    assert "never flew" in joined, "the fallback does not say the fleet never flew"
    assert re.search(r"The simulated fleet never works a fire that was a wildfire of note", joined), (
        "the fallback does not carry the guard note")
    return "fleet sentence once, guard note present, no refused words"


# ============================================================================================
# 3. THE PAGE — served locally, driven headless, one probe per view
# ============================================================================================
def answers(port: int) -> bool:
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/sim/index.js", timeout=1).read(1)
        return True
    except (urllib.error.URLError, OSError):
        return False


def existing_server():
    for var in ("AIRSHIPS_PORT", "PORT"):
        raw = os.environ.get(var)
        if not raw:
            continue
        try:
            port = int(raw)
        except ValueError:
            continue
        if answers(port):
            return port
    return None


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def serve(port: int) -> Server:
    httpd = Server(("127.0.0.1", port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    for _ in range(100):
        if answers(port):
            return httpd
        time.sleep(0.05)
    raise SystemExit("the local server never came up")


# What one view is asked, in the page, after it has booted. Everything the tests assert on
# comes back in one record; nothing is asserted inside the browser.
PROBE = r"""
(async () => {
  // js_eval's wait is a wall-clock sleep from navigation: on a loaded machine the page's
  // own boot can outrun it. Wait for the read handle here (up to 40 s), not in the shell.
  for (let i = 0; i < 160 && !(window.AIRSHIPS && window.AIRSHIPS.app); i++)
    await new Promise(r => setTimeout(r, 250));
  const S = window.AIRSHIPS.app, sim = window.AIRSHIPS.sim, stateAt = window.AIRSHIPS.stateAt;
  const ov = document.getElementById('introOv'); if (ov && !ov.hidden) ov.click();
  for (let i = 0; i < 120 && !S.ready; i++) await new Promise(r => setTimeout(r, 250));
  await new Promise(r => setTimeout(r, 1200));
  S.paused = true;
  const txt = id => { const e = document.getElementById(id); return e ? e.textContent.replace(/\s+/g,' ').trim() : null; };
  const guardedInView = S.fires.filter(f => f.guarded).map(f => ({ id: f.id, name: f.name || null, why: f.guarded.why }));
  const out = {
    url: location.search, day: S.day, daySource: S.daySource,
    recordOnly: !!S.recordOnly, recordWindow: !!S.recordWindow, unknownDay: S.unknownDay,
    standDown: S.standDown, guardOk: !!(S.guard && S.guard.ok), seasonNote: S.seasonNote || null,
    dataNote: S.dataNote || null,
    fires: S.fires.length, guardedInView,
    missions: S.missions.length,
    flying: S.missions.filter(m => !m.idle).length,
    missionsOnGuardedFires: S.missions.filter(m => !m.idle && m.fire && m.fire.guarded)
      .map(m => m.fire.id),
    guardedWithShips: S.fires.filter(f => f.guarded && f.mission).map(f => f.id),
    uncovered: S.uncovered,
    regions: (S.regions || []).map(r => ({ kind: r.kind, who: r.who, rKm: +r.rKm.toFixed(1) })),
    sweep: null,
    panels: { roster: txt('roster'), firesTop: txt('firesTop'), stats: txt('stats'),
              ops: txt('ops'), mode: txt('modeNote'), guardNote: txt('guardNote'),
              heat: txt('heatNote'), hud: txt('hudLive') },
    visible: [],
  };
  // R4 in the page: the mission's fixed points, and the ships' own positions sampled
  // across three full cycles at 30 s of sim time — the drop line moves each cycle, so
  // three cycles see every line the plan will fly.
  if (!S.recordOnly && S.missions.length) {
    let samples = 0; const bad = [];
    const hitAt = (ll) => (ll ? sim.pointBlocked(S.regions, ll) : null);
    for (const m of S.missions) {
      if (m.idle) continue;
      const cyc = Math.max(1, m.cycleSec || 3600);
      for (let t = 0; t <= cyc * 3; t += 30) {
        const st = stateAt(m, t); samples++;
        const hit = hitAt(st && st.ll);
        if (hit) bad.push({ hull: m.shipId || m.name, t, who: hit.who });
        if (bad.length >= 25) break;
      }
      for (const [where, pt] of [['intake', m.intake], ['delivery', m.delivery],
                                 ['ctlOut', m.ctlOut], ['ctlRet', m.ctlRet]]) {
        if (!pt) continue; samples++;
        const hit = hitAt(pt);
        if (hit) bad.push({ hull: m.shipId || m.name, where, who: hit.who });
      }
      for (const [i, p] of (m.stations || []).entries()) {
        samples++; const hit = hitAt(p);
        if (hit) bad.push({ hull: m.shipId || m.name, where: 'station ' + i, who: hit.who });
      }
      for (const [i, p] of (m.targets || []).entries()) {
        samples++; const hit = hitAt(p);
        if (hit) bad.push({ hull: m.shipId || m.name, where: 'target ' + i, who: hit.who });
      }
    }
    out.sweep = { samples, violations: bad };
  }
  // R7's raw material: every string the page shows, own text nodes plus the attributes a
  // reader meets without a pointer — title, aria-label, alt.
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
  out.visible = seen;
  return JSON.stringify(out);
})()
"""

# The two layout defects the guard work found at 1440 px, held at three widths. The
# orientation overlay only exists on a fleet view with a fresh profile, so this runs on
# the sample route and asserts the overlay is actually on screen.
LAYOUT = r"""
(async () => {
  // Bounded at 6 s — the orientation screen dismisses itself 12 s after boot, and this
  // has to see it up. If the cards never appear, the measurement below says so.
  for (let i = 0; i < 24 && !document.querySelector('#introOv .io'); i++)
    await new Promise(r => setTimeout(r, 250));
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
  return JSON.stringify({
    vw: innerWidth, vh: innerHeight, overlay: visible, cards: cards.length,
    overlaps, outside,
    clsRows: rows.length,
    clipped: rows.filter(r => r.over > 1),
  });
})()
"""

VIEWS = {}          # filled by the page pass, read by the tests


def probe_once(port: int, query: str, script: str, wait: float, viewport=None):
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
             f"http://127.0.0.1:{port}/index.html{query}", str(js), str(out), str(wait)],
            cwd=str(ROOT), capture_output=True, text=True, env=env, timeout=300)
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"the probe of {query!r} did not run:\n{r.stdout}\n{r.stderr}")
        return json.loads(out.read_text())


def load_views(port: int):
    """Every view this gate reads, once. Blocking on purpose: one browser at a time."""
    plan = [(d, f"?day={d}&seed=7", 9) for d in RECORD_DAYS]
    plan += [(d, f"?day={d}&seed=7", 9) for d in FLEET_DAYS]
    plan += [("sample", "?seed=7", 9), ("unknown", f"?day={UNKNOWN_DAY}", 9),
             ("no-day-in-window", f"?day={NO_DAY_IN_WINDOW}", 9)]
    for name, query, wait in plan:
        VIEWS[name] = probe_once(port, query, PROBE, wait)
    # 1440: the side-by-side split, all five call-outs up. 1100: the stacked split, still
    # wide enough for the call-outs. 834 and 390: under the phone breakpoint the call-outs
    # are hidden and only the tap prompt shows — the layout test measures what is visible.
    for w, h in ((1440, 900), (1100, 900), (834, 1000), (390, 844)):
        VIEWS[f"layout-{w}"] = probe_once(port, "?seed=7", LAYOUT, 9, f"{w}x{h}")


PAGE_LOADED = []


def page_pass(fn):
    """A test that needs the browser. The first one to run loads every view."""
    @test
    def wrapped(*a, **kw):
        if not PAGE_LOADED:
            port = existing_server()
            httpd = None
            if port is None:
                port = free_port()
                httpd = serve(port)
            try:
                load_views(port)
                PAGE_LOADED.append(True)
            finally:
                if httpd is not None:
                    httpd.shutdown()
        return fn(*a, **kw)
    wrapped.__name__ = fn.__name__
    wrapped.__doc__ = fn.__doc__
    return wrapped


def refuse_words(name, strings):
    """R7's scan: strip the mandated sentence (the refusal itself), then refuse the rest."""
    hits = []
    for s in strings:
        t = MANDATED_FLEET.sub("", s)
        for what, pat in REFUSED:
            m = pat.search(t)
            if m:
                hits.append(f"{name} says {what!r}: …{t[max(0, m.start()-50):m.end()+30]}…")
    assert not hits, "\n          ".join(hits[:6])


# --------------------------------------------------------------------------------------------
@page_pass
def record_only_days_carry_the_record_and_nothing_of_the_fleet():
    """R1 on the page: every day of the window, first to last."""
    for day in RECORD_DAYS:
        v = VIEWS[day]
        same(v["day"], day, f"{day}: the view's day")
        same(v["recordOnly"], True, f"{day}: record only")
        same(v["recordWindow"], True, f"{day}: the window is the reason")
        same(v["missions"], 0, f"{day}: no missions")
        same(v["regions"], [], f"{day}: no keep-out regions are drawn from")
        same(v["missionsOnGuardedFires"], [], f"{day}: nothing to fly")
        assert v["fires"] > 0, f"{day}: the record itself must be on the page"
        # no fleet figure may survive in the rendered text
        assert "No fleet is simulated for this day" in (v["panels"]["roster"] or ""), (
            f"{day}: the roster does not say why it is empty")
        for panel in ("roster", "stats", "ops", "firesTop"):
            t = v["panels"][panel] or ""
            for gone in BANNED_ON_RECORD_DAYS:
                assert gone not in t, f"{day}: the {panel} panel still says {gone!r}"
        m = record_sentence(day).match(v["panels"]["mode"] or "")
        assert m, f"{day}: the mode sentence is not the ruled one: {v['panels']['mode']!r}"
        assert GUARD_NOTE.match(v["panels"]["guardNote"] or ""), (
            f"{day}: the guard note is not the ruled one: {v['panels']['guardNote']!r}")
        refuse_words(day, v["visible"])
        assert not re.search(r"\bqueued\b", " ".join(v["visible"])), (
            f"{day}: an allocator word is on a record-only page")
    return f"{len(RECORD_DAYS)} window days: record only, zero fleet, ruled sentences"


@page_pass
def fleet_days_fly_and_keep_every_rule():
    """R2/R3/R4 on the page: the fleet works only unguarded fires, out of every ring."""
    for day in FLEET_DAYS:
        v = VIEWS[day]
        same(v["recordOnly"], False, f"{day}: a fleet day")
        same(v["daySource"], "day", f"{day}: a named day")
        assert v["missions"] >= 1, f"{day}: no fleet was simulated on a fleet day"
        same(v["missionsOnGuardedFires"], [], f"{day}: R3 — a guarded fire was worked")
        same(v["guardedWithShips"], [], f"{day}: R3 — a guarded fire was given a ship")
        assert v["sweep"], f"{day}: the frame sweep did not run"
        same(v["sweep"]["violations"], [], f"{day}: R4 — a simulated position entered a keep-out")
        m = fleet_sentence(day).match(v["panels"]["mode"] or "")
        assert m, f"{day}: the mode sentence is not the ruled one: {v['panels']['mode']!r}"
        assert GUARD_NOTE.match(v["panels"]["guardNote"] or ""), f"{day}: the guard note moved"
        # R3 in the rendered text: no guarded fire's name reaches the fleet's panels
        names = [g["name"] for g in v["guardedInView"] if g["name"]]
        panels = " ".join(v["panels"][k] or "" for k in ("roster", "firesTop", "ops"))
        leaked = [n for n in names if n in panels]
        assert not leaked, f"{day}: guarded fires named in the fleet panels: {leaked}"
        refuse_words(day, v["visible"])
    return (f"{len(FLEET_DAYS)} fleet days, {sum(VIEWS[d]['flying'] for d in FLEET_DAYS)} "
            f"hull-days flown, {sum(VIEWS[d]['sweep']['samples'] for d in FLEET_DAYS):,} "
            "sampled positions, no violation")


@page_pass
def the_sample_routes_land_on_a_fleet_day_never_a_window_day():
    """R2: the mirror failing, or ?data=snapshot, is the newest fleet day — and is called
    a replay, never live."""
    v = VIEWS["sample"]
    same(v["daySource"], "sample", "the mirror did not answer, so this is the sample")
    same(v["day"], SAMPLE_DAY, "the newest day the guard allows a fleet on")
    same(v["recordOnly"], False, "the sample is a fleet day")
    assert v["dataNote"] and "mirror unavailable" in v["dataNote"], (
        f"the sample's note should name the mirror: {v['dataNote']!r}")
    assert (v["panels"]["mode"] or "").startswith("Replay of "), (
        "the sample must never wear the live label")
    same(v["missionsOnGuardedFires"], [], "R3 on the sample")
    same(v["sweep"]["violations"], [], "R4 on the sample")
    refuse_words("sample", v["visible"])
    return f"mirror failure → {SAMPLE_DAY}, flown, called a replay"


@page_pass
def a_date_with_no_day_file_stands_the_fleet_down_in_words():
    """R6, twice over: a date the season never captured, and the window's own last day —
    which was never captured either. Not a blank map and not a fleet over nothing: a
    sentence. The second case is R1's edge: a missing day inside the window cannot fall
    back to a fleet any more than a present one can."""
    for name, day in (("unknown", UNKNOWN_DAY), ("no-day-in-window", NO_DAY_IN_WINDOW)):
        v = VIEWS[name]
        same(v["unknownDay"], day, f"{day}: the unknown day is named")
        same(v["recordOnly"], True, f"{day}: no fleet for it")
        same(v["missions"], 0, f"{day}: nothing simulated")
        mode = v["panels"]["mode"] or ""
        assert "has no dated copy in this repository" in mode and "no fleet is simulated" in mode, (
            f"{day}: the stand-down sentence moved: {mode!r}")
        refuse_words(name, v["visible"])
    return f"{UNKNOWN_DAY} and {NO_DAY_IN_WINDOW} (the window's last day, uncaptured): stood down, in words"


@page_pass
def the_orientation_cards_and_roster_rows_fit_at_four_widths():
    """The layout half of item 9: no two orientation cards overlap and none leaves the
    viewport; no roster class row is clipped. Red on the old 1440 px layout (the 3D
    call-out reached into the right column's), green now. 1440 is the side-by-side split,
    1100 the stacked one — the two arrangements move the centre call-outs — and 834/390
    check the rows alone, the call-outs being hidden under the phone breakpoint."""
    for w in (1440, 1100, 834, 390):
        v = VIEWS[f"layout-{w}"]
        same(v["vw"], w, f"the {w} px viewport")
        same(v["overlay"], True, f"{w} px: the orientation screen must be up for this to test it")
        same(v["overlaps"], [], f"{w} px: orientation cards overlap")
        same(v["outside"], [], f"{w} px: an orientation card is off-screen")
        assert v["clsRows"] >= 3, f"{w} px: the roster has no class rows to clip"
        same(v["clipped"], [], f"{w} px: a roster class row is clipped")
    return "1440/1100/834/390: cards apart, rows whole"


@page_pass
def the_guard_s_own_counts_for_the_record():
    """The published guard counts, read off the same views: per day, what the
    fleet did and what it refused. Printed, not asserted — the assertions are above."""
    rows = []
    views = [(d, VIEWS[d]) for d in sorted(set(RECORD_DAYS + FLEET_DAYS))]
    views.append((NO_DAY_IN_WINDOW, VIEWS["no-day-in-window"]))
    for day, v in views:
        rows.append(f"{day}  {'record only' if v['recordOnly'] else 'fleet':11s}  "
                    f"{v['fires']:3d} fires  {len(v['guardedInView']):2d} held in view  "
                    f"{v['missions']:2d} hulls  "
                    + (f"{v['sweep']['samples']:5d} positions swept" if v["sweep"] else "no fleet"))
    return "; ".join(rows)


def main():
    only = sys.argv[1:]
    chosen = [fn for fn in TESTS if not only or any(o in fn.__name__ for o in only)]
    failed = 0
    for fn in chosen:
        try:
            note = fn()
            print(f"  ok    {fn.__name__}" + (f": {note}" if note else ""))
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}\n        {e}")
        except Exception as e:  # noqa: BLE001  (a crash is a failure with a name)
            failed += 1
            print(f"  FAIL  {fn.__name__}\n        {type(e).__name__}: {e}")
    print(f"guard: {len(chosen) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
