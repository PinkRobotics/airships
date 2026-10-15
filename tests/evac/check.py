#!/usr/bin/env python3
"""The evacuation gate: the derived record is data, proved three ways.

    tests/evac/check.py                    everything that needs no raw inputs
    tests/evac/check.py <word>             only the tests whose name has the word

1. REGENERATION. The committed pair data/season/2026.evac.json + .prov.json is generated
   output, so it is rebuilt here from a committed trimmed capture (tests/evac/fixtures/)
   and compared against pinned bytes (tests/evac/fixtures/expected/), twice for
   determinism. The fixture is the real capture's shape — the same facts must come out —
   so the fixture-built fires and counts are also held against the committed file itself.
   With the raw capture present (inputs/evac-capture/, untracked), the committed pair is
   regenerated from IT, byte for byte. Without it that one test SKIPs, loudly, and names
   the folder.

2. THE MINIMAL FIELDS. What the ruling refuses to publish — the layer's counts of homes
   and population, the issuing agency, free-text names — is refused everywhere: the
   derived file's own shape is pinned key by key, and the tracked tree is scanned for the
   layer's dropped field names and for any homes/population/agency key in any tracked
   JSON. The banned names are built from pieces here, so this file does not carry them
   either.

3. THE SEASON JOIN. Every fire number in the derived record must resolve in the season
   record, and the exercise generator's exclusion basis — the evacuation record union the
   season record's fires of note — must be wired to both records it claims to read, with
   the page re-deriving its own half of that basis at runtime.

Exit status is non-zero on any failure. A skip is not a failure and is never silent.
Python 3 and its standard library; no browser, no node, no network.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
import season  # noqa: E402  (the generator under test)

YEAR = 2026
SEASON = ROOT / "data" / "season"
FIXTURE = HERE / "fixtures" / "hand-capture"
EXPECTED = HERE / "fixtures" / "expected"
RAW_CAPTURE = ROOT / "inputs" / "evac-capture"

# The published fire record, key for key, in the file's own order.
FIRE_KEYS = ["fire", "everOrder", "everAlert", "firstSeen", "lastSeen", "orderOutlines"]
DOC_KEYS = ["season", "what", "timeZone", "toleranceDeg", "toleranceNote", "days", "fires",
            "counts", "fields", "notes", "publisher", "licence", "notForEmergencyUse"]

TESTS = []


class Skip(Exception):
    pass


def test(fn):
    TESTS.append(fn)
    return fn


def same(got, want, what):
    assert got == want, f"{what}: got {got!r}, expected {want!r}"


def load(path):
    return json.loads(pathlib.Path(path).read_bytes())


def build_from(folder):
    """The pair the generator builds from one evacuation capture folder."""
    return season.build_evac_files(YEAR, season.evac_facts([season.read_evac_capture(folder)]))


# ============================================================================================
# 1. REGENERATION
# ============================================================================================
@test
def the_fixture_regenerates_the_pinned_pair_byte_for_byte():
    files = build_from(FIXTURE)
    same(files, build_from(FIXTURE), "two runs from the fixture, same bytes")
    for name, data in files.items():
        same(data, (EXPECTED / name).read_bytes(), f"the pinned {name}, byte for byte")
    # the fixture is the real capture's shape: its fires and counts are the committed
    # file's own — the same facts from the same captured day, only the day's manifest
    # hashes differ (they name the fixture's files, not the raw ones).
    committed, built = load(SEASON / f"{YEAR}.evac.json"), json.loads(files[f"{YEAR}.evac.json"])
    same(built["fires"], committed["fires"], "the fixture-built fires against the committed file")
    same(built["counts"], committed["counts"], "the fixture-built counts against the committed file")
    day, real = built["days"][0], committed["days"][0]
    for key in ("date", "capturedAt", "features", "url"):
        same(day[key], real[key], f"the captured day's {key}")
    # the pinned pair names the fixture's own files, truthfully
    for row in day["files"]:
        same(hashlib.sha256((FIXTURE / row["name"]).read_bytes()).hexdigest(), row["sha256"],
             f"the day entry's sha256 for {row['name']}")
    return (f"{len(files)} files, byte for byte, twice; fires and counts equal the committed "
            f"record's ({len(built['fires'])} fires)")


@test
def the_raw_capture_regenerates_the_committed_pair():
    """inputs/evac-capture/ (untracked captured inputs) -> the committed pair, exactly."""
    if not (RAW_CAPTURE / "MANIFEST.json").is_file():
        raise Skip(
            "inputs/evac-capture/ is not here. This test regenerates the committed pair from "
            "the one real capture of the evacuation layer, which is deliberately untracked. "
            "Run it on the machine that holds the capture: make evaccheck")
    files = build_from(RAW_CAPTURE)
    for name, data in files.items():
        same(data, (SEASON / name).read_bytes(), f"the committed {name}, byte for byte")
    return f"both committed files regenerated from the raw capture, byte for byte"


# ============================================================================================
# 2. THE MINIMAL FIELDS
# ============================================================================================
@test
def the_derived_record_publishes_the_six_fields_and_nothing_else():
    doc, prov = load(SEASON / f"{YEAR}.evac.json"), load(SEASON / f"{YEAR}.evac.prov.json")
    same(list(doc), DOC_KEYS, "the document's keys")
    same(doc["toleranceDeg"], season.GENERALISE_DEG, "the stated tolerance is the generator's")
    same(doc["timeZone"], season.ZONE_NAME, "the stated time zone")
    dates = [d["date"] for d in doc["days"]]
    for f in doc["fires"]:
        same(list(f), FIRE_KEYS, f"{f['fire']}: the published fields")
        assert re.fullmatch(r"[A-Z][0-9A-Z][0-9]{4}", f["fire"]), f"{f['fire']} is no fire number"
        same(type(f["everOrder"]), bool, f"{f['fire']} everOrder is boolean")
        same(type(f["everAlert"]), bool, f"{f['fire']} everAlert is boolean")
        assert f["everOrder"] or f["everAlert"], f"{f['fire']}: under neither an order nor an alert"
        same(f["firstSeen"] <= f["lastSeen"], True, f"{f['fire']}: seen dates in order")
        assert f["firstSeen"] in dates and f["lastSeen"] in dates, (
            f"{f['fire']}: a seen date no capture carries")
        for ring in f["orderOutlines"]:
            assert len(ring) >= 4 and ring[0] == ring[-1], f"{f['fire']}: an unclosed outline"
            for lon, lat in ring:
                same(round(lon, 4) == lon and round(lat, 4) == lat, True,
                     f"{f['fire']}: an outline coordinate beyond four decimals")
                assert -140 <= lon <= -113 and 48 <= lat <= 61, (
                    f"{f['fire']}: an outline coordinate outside British Columbia")
        if not f["everOrder"]:
            same(f["orderOutlines"], [], f"{f['fire']}: outlines without ever an order")
    # the counts are the file's own rows, recounted here — the fire counts from the fires
    # themselves, the capture counts from the trimmed capture the fixture carries
    fires = doc["fires"]
    c = doc["counts"]
    same(c["fireNumbers"], len(fires), "fire numbers recounted")
    same(c["everOrderFires"], sum(f["everOrder"] for f in fires), "ever-order recounted")
    same(c["everAlertFires"], sum(f["everAlert"] for f in fires), "ever-alert recounted")
    same(c["orderOutlines"], sum(len(f["orderOutlines"]) for f in fires), "outlines recounted")
    same(c["features"], sum(d["features"] for d in doc["days"]), "features recounted")
    feats = load(FIXTURE / "evac.page-000.geojson")["features"]
    is_fire = [f["properties"] for f in feats if f["properties"]["EVENT_TYPE"] == "Fire"]
    others = {}
    for f in feats:
        if f["properties"]["EVENT_TYPE"] != "Fire":
            others[f["properties"]["EVENT_TYPE"]] = others.get(f["properties"]["EVENT_TYPE"], 0) + 1
    same(c["features"], len(feats), "the capture's feature count recounted")
    same(c["fireFeatures"], len(is_fire), "fire features recounted")
    same(c["orderFeatures"], sum(p["ORDER_ALERT_STATUS"] == "Order" for p in is_fire),
         "order features recounted")
    same(c["alertFeatures"], sum(p["ORDER_ALERT_STATUS"] == "Alert" for p in is_fire),
         "alert features recounted")
    same(c["ordersWithoutGeometry"],
         sum(p["ORDER_ALERT_STATUS"] == "Order" and not (f.get("geometry") or {}).get("type", "").endswith("olygon")
             for f in feats for p in [f["properties"]] if p["EVENT_TYPE"] == "Fire"),
         "orders the layer drew no area for recounted")
    same(c["otherEventTypes"], others, "the other event types, counted and left out")
    # the sidecar: the recorded catalogue terms and the incomplete current-layer coverage are explicit
    blob = json.dumps(prov) + json.dumps(doc)
    for phrase in ("Open Government Licence - British Columbia", "incomplete by construction", "Not for emergency use",
                   "does not endorse", "The Information was modified", "dropped"):
        assert phrase in blob, f"the pair must say {phrase!r}"
    same(prov["publisher"], "GeoBC Branch", "catalogue publisher")
    same(prov["licenceUrl"], season.EVAC_TERMS["licenceUrl"], "catalogue licence URL")
    same(prov["decision"], "redistributed", "recorded redistribution decision")
    assert season.EVAC_TERMS["catalogueSha256"] in prov["licenceEvidence"]
    data = (SEASON / f"{YEAR}.evac.json").read_bytes()
    out = prov["outputs"][0]
    same((out["bytes"], out["sha256"]), (len(data), hashlib.sha256(data).hexdigest()),
         "the sidecar's output row against the file")
    assert all(re.fullmatch(r"[0-9a-f]{64}", i["sha256"]) for i in prov["inputs"]), (
        "an input is not named by sha256")
    return (f"{len(fires)} fires, {doc['counts']['orderOutlines']} outlines, six fields each, "
            f"{len(prov['inputs'])} inputs named by sha256")


@test
def no_homes_population_or_agency_field_anywhere_in_the_tracked_tree():
    """The layer's dropped fields are published in no tracked file — this one included: the
    names are built from pieces so the scan's own source does not carry them either."""
    listed = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
    same(listed.returncode, 0, "git ls-files")
    files = [ROOT / p for p in listed.stdout.splitlines() if p.strip()]
    assert files, "git ls-files listed nothing"
    # this order's own output is untracked until it lands: name it here too, so the scan
    # covers the derived pair and its fixtures whatever git knows about today
    files += [SEASON / f"{YEAR}.evac.json", SEASON / f"{YEAR}.evac.prov.json"]
    files += sorted(HERE.rglob("*"))
    files = sorted({p for p in files if p.is_file()})
    # the layer's own names for what the ruling refuses to publish, plus its free-text names
    join, pieces = "_".join, [
        ("MULTI" + "_SOURCED", "_HOMES"), ("MULTI" + "_SOURCED", "_POPULATION"),
        ("ISSUING", "_AGENCY"), ("ORDER" + "_ALERT", "_NAME"), ("EVENT", "_NAME"),
        ("EMRG" + "_OAA", "_SYSID"), ("PREOC", "_CODE"),
        ("FEATURE" + "_AREA", "_SQM"), ("FEATURE" + "_LENGTH", "_M"),
        ("Shape" + "__", "Area"), ("Shape" + "__", "Length")]
    banned = [join(a + b) for a, b in pieces]
    key = re.compile(rb'"[^"]*(homes|population|agency)[^"]*"\s*:', re.I)
    hits = []
    for path in files:
        raw = path.read_bytes()
        for name in banned:
            if name.encode() in raw:
                hits.append(f"{path.relative_to(ROOT)}: the layer field {name!r}")
        if path.suffix == ".json" and key.search(raw):
            hits.append(f"{path.relative_to(ROOT)}: a homes/population/agency key "
                        f"({key.search(raw).group(0)[:40].decode()!r})")
    assert not hits, "; ".join(hits)
    return f"{len(files)} tracked files, {len(banned)} banned names, no key, nothing found"


# ============================================================================================
# 3. THE SEASON JOIN
# ============================================================================================
@test
def every_fire_number_resolves_in_the_season_record():
    season_doc, evac = load(SEASON / f"{YEAR}.json"), load(SEASON / f"{YEAR}.evac.json")
    numbers = {f["fire"] for f in season_doc["fires"]}
    strangers = [f["fire"] for f in evac["fires"] if f["fire"] not in numbers]
    same(strangers, [], "fires in the evacuation record that no season record carries")
    return f"{len(evac['fires'])} fire numbers, all {len(numbers):,} of the season record's"


@test
def the_generator_reads_the_record_and_the_page_rechecks_its_own_half():
    """A static check of the wiring the deeper gates exercise: the exercise generator's
    exclusion basis is the evacuation record joined to the season record's fires of note,
    and the page re-derives the of-note half of that basis at runtime instead of trusting
    the generator's word. The geographic hold is tests/exercise/check.py's."""
    gen = (ROOT / "tools" / "gen_exercise.py").read_text()
    for needle, what in ((f"data/season/{YEAR}.evac.json", "the generator's exclusion basis includes the derived record"),
                         ("fireOfNote", "and the season record's fires of note")):
        assert needle in gen, f"tools/gen_exercise.py: {what} — {needle!r} is gone"
    ex = (ROOT / "app" / "exercise.js").read_text()
    for needle, what in (("EXERCISE_CLEARANCE_KM = 150", "the page re-checks the clearance at runtime"),
                         ("seasonFires", "against the season record it loaded")):
        assert needle in ex, f"app/exercise.js: {what} — {needle!r} is gone"
    return "the wiring is in place; exercisecheck holds what it does on the page"


@test
def the_live_mirror_serves_the_same_minimal_record():
    """pipeline/live.py's hourly feed: fire events only, V2's minimal fields, one request an
    hour — and its reduction of the captured day equals the derived record's own rows."""
    sys.path.insert(0, str(ROOT / "pipeline"))
    import live  # noqa: E402  (the fetcher under test; importing it fetches nothing)

    feed = live.FEEDS["evac"]
    same(feed["maxAgeMin"], 60, "the evacuation feed is fetched at most once an hour")
    same(bool(feed.get("attempt")), True, "an hourly attempt gate, like the wind grid's")
    url = feed["url"]
    same(url.split("?")[0], season.EVAC_SOURCE, "the province's public evacuation layer")
    query = re.findall(r"([^?&=]+)=([^?&]*)", url.split("?", 1)[1])
    q = {urllib.parse.unquote(k): urllib.parse.unquote(v) for k, v in query}
    same(q["where"], "EVENT_TYPE='Fire'", "fire events only")
    same(q["outFields"].split(","), ["EVENT_NUMBER", "ORDER_ALERT_STATUS"],
         "V2's minimal fields, and no others")
    for word in ("HOME", "AGENCY", "NAME"):
        assert word not in q["outFields"].upper(), f"the fetch asks for {word}"

    # the reduction: the captured day's features, reduced the live way, are the derived
    # record's own rows for that day — same numbers, same flags, same outlines
    page = load(FIXTURE / "evac.page-000.geojson")
    day = load(SEASON / f"{YEAR}.evac.json")["days"][0]["capturedAt"]
    reduced = live.evac_record(page, day)
    same(reduced["fires"], load(SEASON / f"{YEAR}.evac.json")["fires"],
         "the live reduction of the captured day against the derived record")
    # a layer that says something the derived record's reader would refuse raises, so the
    # mirror keeps its previous copy instead of publishing an unreadable one
    for broken, words in (
        ({"features": [{"properties": {"EVENT_TYPE": "Fire", "EVENT_NUMBER": "x1234",
                                       "ORDER_ALERT_STATUS": "Order"}}]},
         "not a fire number"),
        ({"features": [{"properties": {"EVENT_TYPE": "Fire", "EVENT_NUMBER": "K51490",
                                       "ORDER_ALERT_STATUS": "Warning"}}]},
         "neither an order nor an alert"),
        ({"features": [{"properties": {"EVENT_TYPE": "Fire", "EVENT_NUMBER": "K51490",
                                       "ORDER_ALERT_STATUS": "Order"},
                        "geometry": {"type": "Point", "coordinates": [0, 0]}}]},
         "not a polygon")):
        try:
            live.evac_record(broken, day)
            raise AssertionError(f"was not refused: {words}")
        except AssertionError:
            raise
        except Exception as e:  # noqa: BLE001  (the fetcher raises its own and season's)
            assert words in str(e), f"refused, but for something else: {e}"
    return ("hourly, minimal outFields; the captured day reduced live equals the derived "
            "record's rows; three broken layers refused")


def main():
    only = sys.argv[1:]
    chosen = [fn for fn in TESTS if not only or any(o in fn.__name__ for o in only)]
    failed = skipped = 0
    for fn in chosen:
        try:
            note = fn()
            print(f"  ok    {fn.__name__}" + (f": {note}" if note else ""))
        except Skip as e:
            skipped += 1
            print(f"  SKIP  {fn.__name__}\n        *** NOT RUN *** " + str(e))
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}\n        {e}")
        except Exception as e:  # noqa: BLE001  (a crash is a failure with a name)
            failed += 1
            print(f"  FAIL  {fn.__name__}\n        {type(e).__name__}: {e}")
    line = f"evac: {len(chosen) - failed - skipped} passed, {failed} failed, {skipped} skipped"
    if skipped:
        line += " (raw capture not here: inputs/evac-capture/ runs that one)"
    print(line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
