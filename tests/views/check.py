#!/usr/bin/env python3
"""The views gate: what every view of the page owes the reader, proved on the page.

Born when the guard was removed (2026-10) and its gate retired with it: the coverage here
is the page's own, not the guard's — the honest-labels refusal over every string the page
holds, the labels a view wears before the map, the stand-down in words for a view that
could not be read, the layout holds, and the live-words rule for views that are not the
live feed.

    tests/views/check.py            everything (this is what `make viewscheck` runs)
    tests/views/check.py <word>     only the tests whose name has the word

Exit status is non-zero on any failure. Requires python3, chromium on PATH and the
`websockets` package (tools/js_eval.py uses it). No node, no network beyond 127.0.0.1.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import page  # noqa: E402

# The days this gate loads: one from the peak August week and the latest captured day,
# which is also the sample route's day. Every captured day's fleet is ranked and held by
# the activity gate (tests/activity); this gate holds what a view says, not how many fly.
DAYS = ["2026-08-08", "2026-10-01"]
SAMPLE_DAY = "2026-10-01"                                          # the newest captured day
UNKNOWN_DAYS = ["2026-07-01", "2026-08-27"]                         # no day file exists

TIME = page.TIME


def fleet_sentence(day):
    return re.compile(
        rf"^(Replay|Live) of {re.escape(day)}: the fires as British Columbia published them "
        rf"at {TIME}\. The fleet is simulated and never flew\. Its drops are water released, "
        r"not water arrived, and nothing here says any fire would have burned differently\.$")


TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def same(got, want, what):
    assert got == want, f"{what}: got {got!r}, expected {want!r}"


VIEWS = {}          # filled by the page pass, read by the tests
PAGE_LOADED = []


def load_views(base: str):
    """Every view this gate reads, once. Blocking on purpose: one browser at a time."""
    plan = [(d, f"?day={d}&seed=7", 9) for d in DAYS]
    plan += [("sample", "?seed=7", 9)]
    plan += [(f"unknown-{d}", f"?day={d}", 9) for d in UNKNOWN_DAYS]
    plan += [("exercise", "?view=exercise&seed=7", 9)]
    for name, query, wait in plan:
        VIEWS[name] = page.probe_once(base, query, page.PROBE, wait)
    # 1440: the side-by-side split, all five call-outs up. 1100: the stacked split, still
    # wide enough for the call-outs. 834 and 390: under the phone breakpoint the call-outs
    # are hidden and only the tap prompt shows — the layout test measures what is visible.
    for w, h in ((1440, 900), (1100, 900), (834, 1000), (390, 844)):
        VIEWS[f"layout-{w}"] = page.probe_once(base, "?seed=7", page.LAYOUT, 0, f"{w}x{h}")


def page_pass(fn):
    """A test that needs the browser. The first one to run loads every view."""
    @test
    def wrapped(*a, **kw):
        if not PAGE_LOADED:
            with page.serve() as base:
                load_views(base)
                PAGE_LOADED.append(True)
        return fn(*a, **kw)
    wrapped.__name__ = fn.__name__
    wrapped.__doc__ = fn.__doc__
    return wrapped


@test
def all_served_scripts_and_meta_tags_refuse_effect_claims():
    from html.parser import HTMLParser
    class Sources(HTMLParser):
        def __init__(self):
            super().__init__(); self.src = []; self.meta = []; self.inline = []; self.script = False
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if tag == "script":
                self.script = True
                if a.get("src"): self.src.append(a["src"])
            if tag == "meta": self.meta.append(a.get("content", ""))
        def handle_endtag(self, tag):
            if tag == "script": self.script = False
        def handle_data(self, data):
            if self.script: self.inline.append(data)
    src_page = Sources(); src_page.feed((ROOT/"index.html").read_text())
    page.refuse_words("meta tags", src_page.meta)
    pending = [(ROOT/rel.split("?")[0]).resolve() for rel in src_page.src]
    visited = set()
    # Scan literals, including template strings, not variable names or comments.
    tokens = re.compile(r"//[^\n]*|/\*.*?\*/|(?:'(?:(?:\\.)|[^'\\])*'|\"(?:(?:\\.)|[^\"\\])*\"|`(?:(?:\\.)|[^`\\])*`)", re.S)
    def scan(name, code):
        strings = [m.group(0)[1:-1] for m in tokens.finditer(code) if m.group(0)[0] in "'\"`"]
        page.refuse_words(name, strings)
    for code in src_page.inline: scan("inline script", code)
    while pending:
        path = pending.pop()
        if path in visited: continue
        assert path.is_relative_to(ROOT), "served script escapes the repository"
        visited.add(path); code = path.read_text()
        scan(str(path.relative_to(ROOT)), code)
        specs = re.findall(r"(?:from\s*|import\s*\(?\s*)['\"]([^'\"]+)['\"]", code)
        # The 3D bridge stamps a URL before dynamic import; its literal path is served too.
        specs += re.findall(r"new URL\(\s*['\"]([^'\"]+\.js(?:\?[^'\"]*)?)['\"]", code)
        for spec in specs:
            if spec.startswith("."):
                pending.append((path.parent/spec.split("?")[0]).resolve())
            else:
                assert not re.match(r"https?://", spec), "foreign served script"
    return f"{len(visited)} served scripts, inline scripts and {len(src_page.meta)} meta tags scanned"


@test
def effect_scan_refuses_claims_but_accepts_specific_denials():
    for text in ["protecting a town", "shields a town", "would have to do"]:
        try: page.refuse_words("fixture", [text])
        except AssertionError: pass
        else: raise AssertionError("missed " + text)
    page.refuse_words("denials", page.DENIALS)
    return "three claims refused; only the complete denial sentences accepted"


@test
def the_static_head_names_no_one_view():
    """index.html's own <head>, before any script runs. A link preview fetched without
    scripts and a reader without scripts get it on every address, so it may claim none of
    them: not live, not a date, not the exercise."""
    html = (ROOT / "index.html").read_text()
    head = html[:html.index("</head>")]
    title = re.search(r"<title>(.*?)</title>", head, re.S).group(1)
    tags = {k: re.search(pat, head).group(1) for k, pat in (
        ("description", r'<meta name="description" content="([^"]*)">'),
        ("og:title", r'<meta property="og:title" content="([^"]*)">'),
        ("og:description", r'<meta property="og:description" content="([^"]*)">'))}
    for where, text in [("title", title)] + sorted(tags.items()):
        m = page.LIVE_WORDS.search(text)
        assert not m, f"the static {where} says {m.group(0)!r}: {text!r}"
        assert not re.search(r"\d{4}-\d{2}-\d{2}", text), f"the static {where} names a date: {text!r}"
    for word in ("exercise", "invented"):
        for where in ("title", "og:title"):
            text = title if where == "title" else tags[where]
            assert word not in text.lower(), f"the static {where} claims the exercise: {text!r}"
    assert "No aircraft has flown" in tags["description"], "the static description lost its denial"
    return "title and three tags: no live claim, no date, no single view"


@page_pass
def fleet_days_fly_and_say_so():
    """Every dated day this gate loads is a fleet day and its sentence is the ruled one."""
    for day in DAYS:
        v = VIEWS[day]
        same(v["recordOnly"], False, f"{day}: a fleet day")
        same(v["daySource"], "day", f"{day}: a named day")
        assert v["missions"] >= 1, f"{day}: no fleet was simulated on a fleet day"
        m = fleet_sentence(day).match(v["panels"]["mode"] or "")
        assert m, f"{day}: the mode sentence is not the ruled one: {v['panels']['mode']!r}"
        page.refuse_words(day, v["visible"])
    return (f"{len(DAYS)} fleet days, {sum(VIEWS[d]['flying'] for d in DAYS)} hulls flying, "
            "the ruled sentence on each")


@page_pass
def the_sample_routes_land_on_the_newest_day():
    """The mirror failing, or ?data=snapshot, is the newest captured day — and is called
    a replay, never live."""
    v = VIEWS["sample"]
    same(v["daySource"], "sample", "the mirror did not answer, so this is the sample")
    same(v["day"], SAMPLE_DAY, "the newest day in the repository")
    same(v["recordOnly"], False, "the sample is a fleet day")
    assert v["dataNote"] and "mirror unavailable" in v["dataNote"], (
        f"the sample's note should name the mirror: {v['dataNote']!r}")
    assert (v["panels"]["mode"] or "").startswith("Replay of "), (
        "the sample must never wear the live label")
    page.refuse_words("sample", v["visible"])
    return f"mirror failure → {SAMPLE_DAY}, flown, called a replay"


@page_pass
def a_date_with_no_day_file_stands_the_fleet_down_in_words():
    """A date the season never captured is not a blank map and not a fleet over nothing:
    a sentence."""
    for day in UNKNOWN_DAYS:
        v = VIEWS[f"unknown-{day}"]
        same(v["unknownDay"], day, f"{day}: the unknown day is named")
        same(v["recordOnly"], True, f"{day}: no fleet for it")
        same(v["missions"], 0, f"{day}: nothing simulated")
        mode = v["panels"]["mode"] or ""
        assert "has no dated copy in this repository" in mode and "no fleet is simulated" in mode, (
            f"{day}: the stand-down sentence moved: {mode!r}")
        page.refuse_words(f"unknown-{day}", v["visible"])
    return f"{', '.join(UNKNOWN_DAYS)}: stood down, in words"


@page_pass
def the_orientation_cards_and_roster_rows_fit_at_four_widths():
    """No two orientation cards overlap and none leaves the viewport; no roster class row
    is clipped. 1440 is the side-by-side split, 1100 the stacked one — the two
    arrangements move the centre call-outs — and 834/390 check the rows alone, the
    call-outs being hidden under the phone breakpoint."""
    for w in (1440, 1100, 834, 390):
        v = VIEWS[f"layout-{w}"]
        same(v["vw"], w, f"the {w} px viewport")
        same(v["overlay"], True, f"{w} px: the orientation screen must be up for this to test it")
        same(v["overlaps"], [], f"{w} px: orientation cards overlap")
        same(v["outside"], [], f"{w} px: an orientation card is off-screen")
        assert v["clsRows"] >= 3, f"{w} px: the roster has no class rows to clip"
        same(v["clipped"], [], f"{w} px: a roster class row is clipped")
        n = v["note"]
        assert n["text"] > 80 and n["w"] > 100 and n["h"] > 10, f"{w} px: the mode sentence is not on screen: {n}"
        same(n["chipsOver"], [], f"{w} px: a chip covers the mode sentence")
        same(n["outsideMap"], False, f"{w} px: the mode sentence leaves the map's box")
    return "1440/1100/834/390: cards apart, rows whole, the mode sentence under no chip"


HEAD_KEYS = ("title", "description", "ogTitle", "ogDescription")


@page_pass
def every_view_names_itself_in_its_title_tags_strip_and_day_control():
    """The labels a reader meets before the map: the tab title, the three description tags
    (a link preview made with scripts on), the header strip and the day control. A dated
    view names its day; a view with nothing on it names itself as empty; none of them is
    live, so none may say live."""
    dated = [(d, d) for d in DAYS] + [("sample", SAMPLE_DAY)]
    empty = [(f"unknown-{d}", d) for d in UNKNOWN_DAYS]
    for name, day in dated + empty:
        v = VIEWS[name]; lab = v["labels"]
        for k in HEAD_KEYS + ("fires", "fleet", "day", "map", "mapHelp"):
            assert lab[k], f"{name}: the probe read nothing for {k}"
        for k in HEAD_KEYS + ("fires", "map"):
            m = page.LIVE_WORDS.search(lab[k])
            assert not m, f"{name}: {k} says {m.group(0)!r} on a view that is not live: {lab[k]!r}"
        # the fleet, promised only where one is simulated
        if v["recordOnly"]:
            same(lab["fleet"], "no fleet simulated", f"{name}: the header strip's fleet label")
            for k in ("title", "ogTitle", "fires"):
                assert "simulated fleet" not in lab[k].lower(), (
                    f"{name}: {k} promises a simulated fleet on a view with none: {lab[k]!r}")
        else:
            same(lab["fleet"], "simulated fleet", f"{name}: the header strip's fleet label")
        # "The fleet is simulated" stands under the roster only where there is a fleet
        same(lab["fleetNote"], not v["recordOnly"], f"{name}: the fleet note is laid out")
        # the description tags are the mode sentence itself, so they cannot drift from it
        same(lab["description"], v["panels"]["mode"], f"{name}: the description tag")
        same(lab["ogDescription"], v["panels"]["mode"], f"{name}: the og:description tag")
    for name, day in dated:
        lab = VIEWS[name]["labels"]
        same(lab["fires"], f"BC fires of {day}", f"{name}: the header strip's fires label")
        for k in ("title", "ogTitle", "map"):
            assert day in lab[k], f"{name}: {k} does not name its day: {lab[k]!r}"
        same(lab["day"], day, f"{name}: the day control shows {lab['day']!r} while the view shows {day}")
        # the first-visit screen opens only over a fleet, and each of its four phrases
        # that name the view names this day
        if not VIEWS[name]["recordOnly"]:
            same(lab["intro"].count(day), 4, f"{name}: first-visit phrases that name the day ({lab['intro']!r})")
    for name, day in empty:
        v = VIEWS[name]; lab = v["labels"]; p = v["panels"]
        same(v["fires"], 0, f"{name}: fires on the map")
        same(lab["fires"], f"no dated copy of {day}", f"{name}: the header strip's fires label")
        assert lab["title"].startswith(f"No dated copy of {day}"), f"{name}: title {lab['title']!r}"
        same(lab["day"], f"{day} · no dated copy", f"{name}: the day control")
        same(p["firesTop"], "", f"{name}: the fires table")
        # nothing was published for this view, so nothing on it may describe a record
        for where, text in (("map label", lab["map"]), ("map help", lab["mapHelp"]),
                            ("roster", p["roster"]), ("headings", p["heads"]),
                            ("operation panel", p["ops"]), ("mode sentence", p["mode"])):
            assert text, f"{name}: the probe read nothing for the {where}"
            assert "published" not in text and "the record" not in text, (
                f"{name}: the {where} describes a published record over an empty map: {text[:140]!r}")
        assert "Click a ship" not in p["ops"], f"{name}: the operation panel offers a cockpit"
    return (f"{len(dated)} dated views named by day, {len(empty)} empty views named as empty; "
            "no view says live, none without a fleet promises one")


@page_pass
def no_string_on_a_view_that_is_not_live_says_live():
    """Every string the page holds, on every view that is not the live feed: none says
    "live", "current" or "today" outside the named uses in tests/page.py."""
    names = DAYS + ["sample"] + [f"unknown-{d}" for d in UNKNOWN_DAYS] + ["exercise"]
    used, strings = set(), 0
    for name in names:
        v = VIEWS[name]
        assert v["daySource"] != "live", f"{name}: the probe loaded the live feed"
        assert len(v["visible"]) > 100, f"{name}: the probe read only {len(v['visible'])} strings"
        for s in v["visible"]:
            strings += 1
            t = s
            for ok in page.NOT_A_LIVE_CLAIM:
                if ok.lower() in t.lower():
                    used.add(ok)
                    t = re.sub(re.escape(ok), "", t, flags=re.I)
            m = page.LIVE_WORDS.search(t)
            assert not m, (f"{name}: says {m.group(0)!r} on a view that is not live: "
                           f"…{t[max(0, m.start() - 70):m.end() + 50]}…")
    stale = [ok for ok in page.NOT_A_LIVE_CLAIM if ok not in used]
    assert not stale, f"named uses that no view shows any more (remove them): {stale}"
    return f"{len(names)} views, {strings:,} strings, {len(page.NOT_A_LIVE_CLAIM)} named uses, each one met"


# A deployment with a file gone, four ways: (name, address, what answers 404, how the title
# opens, the reason every panel must give).
BROKEN = [
    ("nothing readable", "?seed=7",
     ("data/live/", "data/season/2026.days.json", "data/snapshot.json"),
     "No fire data", "nothing could be read"),
    ("the season index gone, a day asked", f"?day={DAYS[1]}&seed=7",
     ("data/season/2026.days.json",), "No fire data", "the season index did not load"),
    ("a day's fire file gone", f"?day={DAYS[1]}&seed=7",
     (f"data/season/days/{DAYS[1]}/fires.json",),
     "No fire data", "the day's own files failed their checks"),
    ("the exercise file gone", "?view=exercise&seed=7", ("data/exercise/exercise.json",),
     "Exercise unavailable", "the exercise could not be read"),
]
# What the view it failed to be would have said.
LEFTOVERS = ("published", "the record", "Click a ship", "Click a fire", "simulated hulls",
             "simulated fleet", "invented")


@test
def a_view_that_could_not_be_read_says_nothing_is_shown_and_why():
    """Each broken deployment ends in a view with no fire and no fleet that names itself
    as empty, gives the reason in every panel, and keeps no sentence of the view it failed
    to be."""
    for name, query, missing, title, why in BROKEN:
        with page.serve(missing) as base:
            v = page.probe_once(base, query, page.PROBE, 9)
        lab, p = v["labels"], v["panels"]
        same(v["fires"], 0, f"{name}: fires on the map")
        same(v["missions"], 0, f"{name}: hulls")
        assert lab["title"].startswith(title + " · "), f"{name}: the title is {lab['title']!r}"
        same(lab["fleet"], "no fleet simulated", f"{name}: the header strip's fleet label")
        same(lab["fleetNote"], False, f"{name}: the fleet note is laid out")
        assert lab["day"].endswith(" · nothing shown"), f"{name}: the day control shows {lab['day']!r}"
        same(p["firesTop"], "", f"{name}: the fires table")
        says_why = [("mode sentence", p["mode"]), ("description tag", lab["description"]),
                    ("map label", lab["map"]), ("map help", lab["mapHelp"]), ("roster", p["roster"]),
                    ("headings", p["heads"]), ("operation panel", p["ops"])]
        for where, text in says_why:
            assert text and why in text, f"{name}: the {where} does not say why: {str(text)[:160]!r}"
        for where, text in says_why + [("chip", p["hud"]), ("title", lab["title"]),
                                       ("og:title", lab["ogTitle"]), ("day control", lab["day"]),
                                       ("header strip", lab["fires"])]:
            for word in LEFTOVERS:
                assert word not in text, f"{name}: the {where} still says {word!r}: {text[:160]!r}"
        if "view=exercise" in query:
            # The exercise has no calendar day, read or unread.
            for text in v["visible"]:
                assert "this day" not in text, f"{name}: an exercise has no day, yet: {text[:160]!r}"
    return f"{len(BROKEN)} broken deployments: no fire, no fleet, the reason in seven places, nothing left over"


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
    print(f"views: {len(chosen) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
