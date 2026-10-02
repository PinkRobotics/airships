#!/usr/bin/env python3
"""The 2026 wildfire season as data: one hindsight record per fire, and the days with a dated one.

    python3 pipeline/season.py <capture folder>           regenerate data/season/ from raw inputs
    python3 pipeline/season.py <capture folder> --check   the same, in memory; exit 1 on any drift
    python3 pipeline/season.py --check                    the gate that needs no raw inputs
    python3 pipeline/season.py --table                    print the impossible-date table

NO NETWORK. Nothing here opens a socket. Every input is a file somebody already has: a capture
folder (a complete copy of the BC Wildfire Service's two public layers, with a MANIFEST.json
naming each file's sha256), the recovered history of this site's own live mirror, and
data/snapshot.json. The raw inputs are megabytes and stay out of the repository; their sha256s
are written into the provenance.

WHY TWO KINDS OF FILE. A replay that shows a fire at its final size on the day it started has
looked ahead. So this writes two things that must never be mixed:

  data/season/<year>.json     ONE RECORD PER FIRE, AS THE RECORD STOOD AT CAPTURE. Hindsight in
                              every field: the size (named hindsightSizeHa so that it cannot be
                              mistaken for anything else), the final status, the out date, and
                              the ignition date, which the publisher revises after the fact.
  data/season/days/<date>/    STATUS DAYS: what the public record said on a day, for the days
                              that have a dated first-party copy. fires.json and perims.json in
                              exactly the shape pipeline/live.py serves, so the page can feed
                              them through the code path it uses for live data. For each
                              America/Vancouver date, the LAST copy of that local day.

Three kinds of copy become a status day. A copy of the live mirror recovered from the site's
deploy history is kept byte for byte. The repository's own snapshot is reduced to the mirror's
property names. A complete capture is filtered the way the mirror filters (status not Out) and
its perimeters generalised the way the mirror's request generalises them.

IMPOSSIBLE DATES ARE KEPT, COUNTED AND FLAGGED: NEVER REPAIRED, NEVER DROPPED. The layer carries
ignitions in 1429 and 2044, fires out before they started, and one fire a dated record lists two
days before its own ignition. Each such fire stays in the file and in every total, with the
recorded values untouched and the reason in its `dates` field. It is left off the day-by-day
timeline (ignited and out are null) unless one of two stated rules places it; see RULES below.
The printed table is the evidence, one row per fire.

DATES. The source stores epoch milliseconds in UTC. A day is the America/Vancouver calendar
date of an instant, for the season file and for the status days alike. The conversion uses the
system time-zone database.

--check WITHOUT A CAPTURE FOLDER rebuilds everything that can be rebuilt from committed files
(every derived field of every fire, the summary, the day index, the provenance record, and the
snapshot day from data/snapshot.json) and compares bytes. It cannot prove that the season file
matches a capture nobody on that machine has; `--check` WITH the folder does that.

ADDING A DAY. Captures are taken daily into sibling folders named by local date. One command:

    python3 pipeline/season.py <the season's capture folder> --through 2026-10-02

keeps the season record pinned to its capture and adds every complete sibling capture up to
that date as a status day. Pointing the command at a newer capture folder instead re-pins the
season record to it; the totals then move, and the pins in tests/season/check.py with them.
"""
from __future__ import annotations

import argparse
import bisect
import datetime
import hashlib
import json
import math
import pathlib
import re
import statistics
import sys
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEASON_DIR = ROOT / "data" / "season"
SNAPSHOT = ROOT / "data" / "snapshot.json"

ZONE_NAME = "America/Vancouver"
ZONE = ZoneInfo(ZONE_NAME)
UTC = datetime.timezone.utc
EPOCH = datetime.datetime(1970, 1, 1, tzinfo=UTC)
DAY_MS = 86_400_000

# What the live mirror serves, in its order. tests/season/check.py holds these two tuples
# against the outFields in pipeline/live.py, so the status days cannot drift from the mirror.
FIRE_PROPS = ("FIRE_NUMBER", "FIRE_STATUS", "FIRE_CAUSE", "INCIDENT_NAME",
              "GEOGRAPHIC_DESCRIPTION", "CURRENT_SIZE", "IGNITION_DATE", "FIRE_URL",
              "FIRE_OF_NOTE_IND", "RESPONSE_TYPE_DESC")
PERIM_PROPS = ("FIRE_NUMBER", "FIRE_STATUS", "FIRE_SIZE_HECTARES", "TRACK_DATE")
SERVICE = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/"
FIRES_SOURCE = SERVICE + "BCWS_ActiveFires_PublicView/FeatureServer/0/query"
PERIMS_SOURCE = SERVICE + "BCWS_FirePerimeters_PublicView/FeatureServer/0/query"
CRS = {"type": "name", "properties": {"name": "EPSG:4326"}}
# What a capture's own status day and the season file both say about a fire that is not out.
SHARED = ("FIRE_STATUS", "CURRENT_SIZE", "FIRE_CAUSE", "INCIDENT_NAME", "GEOGRAPHIC_DESCRIPTION",
          "IGNITION_DATE", "FIRE_OF_NOTE_IND")

# The mirror asks the server for perimeters at maxAllowableOffset=0.002 degrees. A capture is
# full resolution, so a capture day is generalised here, to the same tolerance and precision.
GENERALISE_DEG = 0.002
COORD_DECIMALS = 4
# The mirror fetches fires and perimeters in one run, a second or two apart.
PAIR_SECONDS = 120

# The layer publishes the fire centre as a bare integer. The names are this project's
# labelling, by the letter that begins every fire number; the pairing of code and letter is
# checked on every record.
CENTRES = {2: ("V", "Coastal"), 3: ("R", "Northwest"), 4: ("G", "Prince George"),
           5: ("K", "Kamloops"), 6: ("N", "Southeast"), 7: ("C", "Cariboo")}
LETTER_CENTRE = {letter: name for letter, name in CENTRES.values()}
CENTRE_CODE = {name: code for code, (_, name) in CENTRES.items()}
FIRE_NUMBER = re.compile(r"[A-Z][0-9A-Z][0-9]{4}")

LICENCE = "Open Government Licence - British Columbia, version 2.0"
LICENCE_URL = "https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc"
ATTRIBUTION = "Contains information licensed under the Open Government Licence - British Columbia."
PUBLISHER = "Province of British Columbia, BC Wildfire Service (Ministry of Forests)"
CATALOGUE = ["https://catalogue.data.gov.bc.ca/dataset/bc-wildfire-fire-locations-current",
             "https://catalogue.data.gov.bc.ca/dataset/bc-wildfire-fire-perimeters-current"]
NO_ENDORSEMENT = ("The Province of British Columbia does not endorse this project and nothing "
                  "here has official status.")
NOT_FOR_EMERGENCY = ("Not for emergency use. This is a dated copy of a public record, kept for a "
                     "labelled replay. For a real fire, use the BC Wildfire Service.")

# ---- RULES: the impossible-date policy, in one place ---------------------------------------
DATE_FLAGS = {
    "ignition-missing": "The record has no ignition date.",
    "ignition-outside-fire-year":
        "The America/Vancouver calendar year of the ignition date is not the fire year the "
        "record itself gives.",
    "ignition-after-capture": "The ignition date is later than the time this copy was taken.",
    "out-missing": "The status is Out and there is no out date.",
    "out-date-but-not-out": "There is an out date and the status is not Out.",
    "out-after-capture": "The out date is later than the time this copy was taken.",
    "out-before-ignition": "The fire is recorded as out before it ignited.",
    "listed-before-ignition":
        "A status-day record lists the fire at a time earlier than the ignition date this "
        "copy gives it.",
}
OUT_FAULTS = {"out-missing", "out-date-but-not-out", "out-after-capture"}
TIMELINE_RULES = {
    "dated-record":
        "The ignition date in this copy is impossible, the out date is not in question, and "
        "every status-day record that lists the fire carries one and the same ignition date, "
        "which is possible: in the fire year, not later than the record that carries it, not "
        "later than the out date. The fire is placed from that date. The value this copy "
        "gives stays in ignitionMs and in dates.recorded.",
    "same-local-day":
        "The only fault is an out time earlier than the ignition time, and both fall on the "
        "same America/Vancouver date. The timeline is kept by date, so the fire is placed on "
        "that date: it starts and is out the same day and is active on no day. Which of the "
        "two times is wrong is not decided.",
}


class SeasonError(Exception):
    """An input is missing, incomplete or not what its manifest says. Never papered over."""


# ---- time ----------------------------------------------------------------------------------
def instant(ms):
    return EPOCH + datetime.timedelta(milliseconds=ms)


def local(ms):
    return instant(ms).astimezone(ZONE)


def iso_utc(ms):
    if ms is None:
        return None
    d = instant(ms)
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (d.year, d.month, d.day, d.hour, d.minute, d.second)


def local_date(ms):
    if ms is None:
        return None
    d = local(ms)
    return "%04d-%02d-%02d" % (d.year, d.month, d.day)


def utc_offset(ms):
    seconds = int(local(ms).utcoffset().total_seconds())
    sign, seconds = ("-", -seconds) if seconds < 0 else ("+", seconds)
    return "%s%02d:%02d" % (sign, seconds // 3600, seconds % 3600 // 60)


def parse_utc(text):
    d = datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise SeasonError(f"a time with no zone cannot be placed on a day: {text!r}")
    return (d - EPOCH) // datetime.timedelta(milliseconds=1)


def date_range(first, last):
    d, end = datetime.date.fromisoformat(first), datetime.date.fromisoformat(last)
    while d <= end:
        yield d.isoformat()
        d += datetime.timedelta(days=1)


# ---- bytes ---------------------------------------------------------------------------------
def digest(data):
    return hashlib.sha256(data).hexdigest()


def compact(obj):
    """Exactly what pipeline/live.py writes: every recovered mirror copy re-serialises to its
    own bytes through this, so a status day made here is the same kind of file."""
    return json.dumps(obj, separators=(",", ":")).encode("ascii")


def render(obj, width=96, row=1400):
    """JSON a person can read and git can diff: one key per line, and one line per record.

    A value is written flat if it fits in `width`; a dictionary inside a list is a record and
    gets `row`, so each fire, each timeline day and each flagged fire is one line."""
    def enc(o, depth, limit):
        flat = json.dumps(o, separators=(",", ":"))
        if not isinstance(o, (dict, list)) or not o or len(flat) <= limit:
            return flat
        pad, inner = " " * (depth + 1), max(limit, width)
        if isinstance(o, dict):
            body = [pad + json.dumps(k) + ":" + enc(v, depth + 1, inner) for k, v in o.items()]
            return "{\n" + ",\n".join(body) + "\n" + " " * depth + "}"
        body = [pad + enc(v, depth + 1, row if isinstance(v, dict) else inner) for v in o]
        return "[\n" + ",\n".join(body) + "\n" + " " * depth + "]"
    return enc(obj, 0, 0).encode("ascii")


def read_checked(path, size, sha, what):
    try:
        data = path.read_bytes()
    except OSError as e:
        raise SeasonError(f"{what}: cannot read {path.name} ({e.strerror})") from None
    if len(data) != size or digest(data) != sha:
        raise SeasonError(f"{what}: {path.name} is not the file its manifest describes "
                          f"({len(data)} bytes, sha256 {digest(data)[:12]}; "
                          f"expected {size} bytes, {sha[:12]})")
    return data


def tally(values):
    out = {}
    for v in values:
        key = "null" if v is None else v
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items()))


# ---- perimeter generalisation --------------------------------------------------------------
# Douglas-Peucker in plain degrees, the way the server answers maxAllowableOffset: anchor the
# ring at its first vertex and at the vertex farthest from it, never return less than a closed
# triangle, round to four places. This is not a guess at the server's method: on every
# perimeter that a mirror copy and a capture hold at the same vintage it gives the server's
# vertices exactly (tests/season/check.py re-proves it whenever the raw inputs are present).
def _offset(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    span = math.hypot(dx, dy)
    if not span:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    return abs(dy * (p[0] - a[0]) - dx * (p[1] - a[1])) / span


def _keep(ring, first, last, tol, keep):
    stack = [(first, last)]
    while stack:
        i, j = stack.pop()
        best, at = -1.0, -1
        for k in range(i + 1, j):
            d = _offset(ring[k], ring[i], ring[j])
            if d > best:
                best, at = d, k
        if best > tol:
            keep[at] = True
            stack += [(i, at), (at, j)]


def generalise_ring(ring, tol=GENERALISE_DEG):
    n = len(ring)
    if n < 5:
        return [list(p) for p in ring]
    keep = [False] * n
    keep[0] = keep[-1] = True
    x0, y0 = ring[0][0], ring[0][1]
    far = max(range(1, n - 1), key=lambda i: (ring[i][0] - x0) ** 2 + (ring[i][1] - y0) ** 2)
    keep[far] = True
    _keep(ring, 0, far, tol, keep)
    _keep(ring, far, n - 1, tol, keep)
    if sum(keep) < 4:
        rest = (i for i in range(1, n - 1) if i != far)
        keep[max(rest, key=lambda i: _offset(ring[i], ring[0], ring[far]))] = True
    return [list(p) for p, k in zip(ring, keep) if k]


def generalise(geometry, tol=GENERALISE_DEG, places=COORD_DECIMALS):
    def ring(r):
        return [[round(x, places), round(y, places)] for x, y in generalise_ring(r, tol)]
    if geometry["type"] == "Polygon":
        return {"type": "Polygon", "coordinates": [ring(r) for r in geometry["coordinates"]]}
    if geometry["type"] == "MultiPolygon":
        return {"type": "MultiPolygon",
                "coordinates": [[ring(r) for r in poly] for poly in geometry["coordinates"]]}
    raise SeasonError(f"a perimeter is a {geometry['type']}, not a polygon")


# ---- reading the raw inputs ----------------------------------------------------------------
def read_capture(folder):
    """One capture folder, checked against its own manifest before a byte of it is believed."""
    folder = pathlib.Path(folder)
    name = folder.name
    manifest = folder / "MANIFEST.json"
    if not manifest.is_file():
        raise SeasonError(f"capture '{name}': no MANIFEST.json; is this a capture folder?")
    raw = manifest.read_bytes()
    man = json.loads(raw)
    listed = {r["file"]: r for r in man["requests"]}
    used = []

    def load(file):
        r = listed.get(file)
        if r is None:
            raise SeasonError(f"capture '{name}': MANIFEST.json lists no {file}")
        data = read_checked(folder / file, r["bytes"], r["sha256"], f"capture '{name}'")
        used.append({"name": file, "url": r["url"], "bytes": r["bytes"], "sha256": r["sha256"]})
        return json.loads(data)

    capture = {"name": name, "capturedMs": parse_utc(man["capturedAt"]),
               "manifest": {"bytes": len(raw), "sha256": digest(raw)}, "files": used}
    if local_date(capture["capturedMs"]) != man.get("localDate"):
        raise SeasonError(f"capture '{name}': taken {man['capturedAt']}, which is "
                          f"{local_date(capture['capturedMs'])} in {ZONE_NAME}, but its manifest "
                          f"says {man.get('localDate')}")
    for layer in ("incidents", "perimeters"):
        info = man["layers"][layer]
        if info.get("complete") is not True:
            raise SeasonError(f"capture '{name}': the {layer} layer is not marked complete")
        meta = load(f"{layer}.layer.json")
        zone = (meta.get("dateFieldsTimeReference") or {}).get("timeZone")
        if zone != "UTC":
            raise SeasonError(f"capture '{name}': the {layer} layer stores dates in {zone!r}; "
                              "this reads them as UTC and will not guess")
        features = []
        for file in sorted(f for f in listed if re.fullmatch(layer + r"\.page-\d+\.geojson", f)):
            features += load(file)["features"]
        counted = tally(f["properties"]["FIRE_STATUS"] for f in features)
        if len(features) != info["countOnly"] or counted != dict(sorted(info["byStatus"].items())):
            raise SeasonError(f"capture '{name}': {len(features)} {layer} {counted} do not match "
                              f"the layer's own count {info['countOnly']} {info['byStatus']}")
        edited = (meta.get("editingInfo") or {}).get("dataLastEditDate")
        capture[layer] = {"features": features, "url": info["url"], "where": info["where"],
                          "lastEdited": iso_utc(edited)}
    return capture


def yes_no(value, what):
    if value in ("Y", "Yes"):
        return True
    if value in ("N", "No"):
        return False
    raise SeasonError(f"{what}: {value!r} is neither yes nor no")


def records_from(capture):
    """The incidents layer reduced to the fields the season file keeps, values untouched."""
    years = {f["properties"]["FIRE_YEAR"] for f in capture["incidents"]["features"]}
    if len(years) != 1:
        raise SeasonError(f"capture '{capture['name']}': fire years {sorted(years)}; a season "
                          "file is one fire year")
    records = []
    for f in capture["incidents"]["features"]:
        p = f["properties"]
        n = p["FIRE_NUMBER"]
        records.append({
            "fire": n, "name": p["INCIDENT_NAME"], "place": p["GEOGRAPHIC_DESCRIPTION"],
            "lat": p["LATITUDE"], "lon": p["LONGITUDE"], "centreCode": p["FIRE_CENTRE"],
            "cause": p["FIRE_CAUSE"], "ignitionMs": p["IGNITION_DATE"],
            "outMs": p["FIRE_OUT_DATE"], "status": p["FIRE_STATUS"],
            "fireOfNote": yes_no(p["FIRE_OF_NOTE_IND"], f"{n} FIRE_OF_NOTE_IND"),
            "wasFireOfNote": yes_no(p["WAS_FIRE_OF_NOTE_IND"], f"{n} WAS_FIRE_OF_NOTE_IND"),
            "sizeHa": p["CURRENT_SIZE"]})
    return years.pop(), records


def feature(source, props, geometry=None):
    p = source["properties"]
    missing = [k for k in props if k not in p]
    if missing:
        raise SeasonError(f"a feature has no {', '.join(missing)}")
    return {"type": "Feature", "geometry": source["geometry"] if geometry is None else geometry,
            "properties": {k: p[k] for k in props}}


def mirror_document(ms, source, features):
    return compact({"fetchedAt": iso_utc(ms), "source": source,
                    "data": {"type": "FeatureCollection", "crs": CRS, "features": features}})


def not_out(feat):
    """The mirror asks for FIRE_STATUS <> 'Out'. In SQL that also drops a null status."""
    return feat["properties"]["FIRE_STATUS"] not in (None, "Out")


def day_from_capture(capture):
    ms = capture["capturedMs"]
    fires = [feature(f, FIRE_PROPS) for f in capture["incidents"]["features"] if not_out(f)]
    perims = [feature(f, PERIM_PROPS, generalise(f["geometry"]))
              for f in capture["perimeters"]["features"] if not_out(f)]
    return {"date": local_date(ms), "kind": "capture", "ms": ms,
            "fires": mirror_document(ms, capture["incidents"]["url"] + "/query", fires),
            "perims": mirror_document(ms, capture["perimeters"]["url"] + "/query", perims),
            "source": {"capturedAt": iso_utc(ms), "manifest": capture["manifest"],
                       "files": [{k: f[k] for k in ("name", "bytes", "sha256")}
                                 for f in capture["files"]]}}


def day_from_snapshot(path):
    """data/snapshot.json is the mirror's two answers under one roof, with one extra property
    on each feature. Dropping those two properties is the whole conversion."""
    try:
        raw = pathlib.Path(path).read_bytes()
    except OSError as e:
        raise SeasonError(f"the repository snapshot: cannot read it ({e.strerror})") from None
    snap = json.loads(raw)
    ms = parse_utc(snap["retrievedAt"])
    fires = [feature(f, FIRE_PROPS) for f in snap["fires"]["features"]]
    perims = [feature(f, PERIM_PROPS) for f in snap["perimeters"]["features"]]
    return {"date": local_date(ms), "kind": "repository-snapshot", "ms": ms,
            "fires": mirror_document(ms, FIRES_SOURCE, fires),
            "perims": mirror_document(ms, PERIMS_SOURCE, perims),
            "source": {"file": "data/snapshot.json", "retrievedAt": iso_utc(ms),
                       "bytes": len(raw), "sha256": digest(raw)}}


def days_from_mirror(folder):
    """The last fires copy and the last perimeters copy of each local day, byte for byte."""
    folder = pathlib.Path(folder)
    index = folder / "INDEX.json"
    if not index.is_file():
        raise SeasonError(f"mirror history '{folder.name}': no INDEX.json")
    raw = index.read_bytes()
    by_day = {"fires": {}, "perims": {}}
    times = []
    for copy in json.loads(raw)["copies"]:
        if copy["name"] in by_day:
            ms = parse_utc(copy["fetchedAt"])
            times.append(ms)
            by_day[copy["name"]].setdefault(local_date(ms), []).append((ms, copy))
    if set(by_day["fires"]) != set(by_day["perims"]):
        odd = sorted(set(by_day["fires"]) ^ set(by_day["perims"]))
        raise SeasonError(f"mirror history: {odd} have fires or perimeters but not both")
    days = []
    for date in sorted(by_day["fires"]):
        picked = {}
        for name in ("fires", "perims"):
            ms, copy = max(by_day[name][date], key=lambda c: c[0])
            data = read_checked(folder / copy["folder"] / copy["file"], copy["bytes"],
                                copy["sha256"], "mirror history")
            picked[name] = (ms, data, {"fetchedAt": iso_utc(ms), "bytes": copy["bytes"],
                                       "sha256": copy["sha256"]})
        if abs(picked["fires"][0] - picked["perims"][0]) > PAIR_SECONDS * 1000:
            raise SeasonError(f"mirror history {date}: the last fires copy and the last "
                              f"perimeters copy are more than {PAIR_SECONDS} s apart")
        days.append({"date": date, "kind": "mirror-history", "ms": picked["fires"][0],
                     "fires": picked["fires"][1], "perims": picked["perims"][1],
                     "source": {"copiesThatDay": len(by_day["fires"][date]),
                                "fires": picked["fires"][2], "perims": picked["perims"][2]}})
    history = {"index": {"bytes": len(raw), "sha256": digest(raw)},
               "fireCopies": sum(len(v) for v in by_day["fires"].values()),
               "perimeterCopies": sum(len(v) for v in by_day["perims"].values()),
               "firstFetchedAt": iso_utc(min(times)), "lastFetchedAt": iso_utc(max(times))}
    return days, history


def capture_fingerprint(folder):
    """Hash sorted relative filenames and SHA-256s of every file, including the manifest."""
    folder = pathlib.Path(folder)
    if not folder.is_dir():
        raise SeasonError(f"capture '{folder.name}': missing named folder")
    try:
        files = [{"file": p.relative_to(folder).as_posix(), "sha256": digest(p.read_bytes())}
                 for p in sorted(folder.rglob("*")) if p.is_file()]
    except OSError as e:
        raise SeasonError(f"capture '{folder.name}': cannot read contents ({e.strerror})") from None
    return {"folder": folder.name, "sha256": digest(render(files))}


def recorded_captures(root, record):
    """Verify every named input before reading; additional captures are information only."""
    if not isinstance(record, list) or not record:
        raise SeasonError("captureFolders: missing or empty capture record")
    names = set()
    for entry in record:
        name = entry.get("folder")
        if (not isinstance(name, str) or not name or pathlib.Path(name).name != name
                or name in {".", ".."} or name in names):
            raise SeasonError("captureFolders: invalid or repeated folder name")
        names.add(name)
        if capture_fingerprint(root / name) != entry:
            raise SeasonError(f"capture '{name}': contents changed from the provenance record")
    for p in sorted(root.iterdir()):
        if p.name not in names and (p / "MANIFEST.json").is_file():
            print(f"season: capture '{p.name}': not in the record; ignored (information)")
    return [root / entry["folder"] for entry in record]


def read_raw(capture_dir, mirror_dir=None, snapshot=SNAPSHOT, through=None, capture_folders=None):
    """Everything that cannot be rebuilt without the raw inputs, and nothing else."""
    capture_dir = pathlib.Path(capture_dir)
    siblings = (recorded_captures(capture_dir.parent, capture_folders)
                if capture_folders is not None else sorted(capture_dir.parent.iterdir()))
    if capture_folders is not None and capture_dir not in siblings:
        raise SeasonError(f"capture '{capture_dir.name}': not in the provenance record")
    capture = read_capture(capture_dir)
    year, records = records_from(capture)
    season_date = local_date(capture["capturedMs"])
    through = through or season_date
    if through < season_date:
        raise SeasonError(f"--through {through} is before the season capture's own day "
                          f"({season_date})")
    candidates = [day_from_snapshot(snapshot)]
    if mirror_dir is None:
        mirror_dir = capture_dir.parent.parent / "mirror-history"
    mirror_days, history = days_from_mirror(mirror_dir)
    candidates += mirror_days
    # The capture series: this capture and its dated siblings. A sibling later than --through
    # is not read at all, so a capture taken tomorrow cannot move today's files.
    used = []
    for sibling in siblings:
        if sibling.resolve() == capture_dir.resolve():
            candidates.append(day_from_capture(capture))
            used.append(capture_fingerprint(sibling))
        elif (sibling / "MANIFEST.json").is_file():
            said = json.loads((sibling / "MANIFEST.json").read_bytes()).get("localDate")
            if said is not None and said <= through:
                candidates.append(day_from_capture(read_capture(sibling)))
                used.append(capture_fingerprint(sibling))
    days = {}
    for day in sorted(candidates, key=lambda d: d["ms"]):
        if day["date"] > through:
            continue
        older = days.get(day["date"])
        if older is not None:          # the LAST copy of the local day wins, and says so
            day["source"]["supersedes"] = older["source"].get("supersedes", []) + [
                {"kind": older["kind"], "at": iso_utc(older["ms"])}]
        days[day["date"]] = day
    layer = capture["incidents"]
    return {
        "year": year,
        "capture": {"capturedAt": iso_utc(capture["capturedMs"]),
                    "layer": {"name": layer["url"].split("/services/")[-1].split("/")[0],
                              "url": layer["url"], "where": layer["where"],
                              "lastEdited": layer["lastEdited"]},
                    "manifest": capture["manifest"], "files": capture["files"]},
        "records": records,
        "captureFolders": used,
        "days": [days[d] for d in sorted(days)],
        "mirrorHistory": history,
    }


# ---- reading the committed files back ------------------------------------------------------
def read_committed(year, season_dir=SEASON_DIR, snapshot=SNAPSHOT):
    """The same state, recovered from what is committed.

    Raw values come back out of the season file, the day files and the index's source blocks.
    Nothing derived is read: build() makes all of that again, which is the point. The snapshot
    day is not read back either. data/snapshot.json is in the repository, so it is rebuilt."""
    season_dir = pathlib.Path(season_dir)

    def committed(name):
        try:
            return (season_dir / name).read_bytes()
        except OSError as e:
            raise SeasonError(f"{name}: cannot read it ({e.strerror})") from None

    try:
        season = json.loads(committed(f"{year}.json"))
        index = json.loads(committed(f"{year}.days.json"))
        records = []
        for f in season["fires"]:
            if f["centre"] not in CENTRE_CODE:
                raise SeasonError(f"{f['fire']}: unknown fire centre {f['centre']!r}")
            records.append({
                "fire": f["fire"], "name": f["name"], "place": f["place"], "lat": f["lat"],
                "lon": f["lon"], "centreCode": CENTRE_CODE[f["centre"]], "cause": f["cause"],
                "ignitionMs": f["ignitionMs"], "outMs": f["outMs"],
                "status": f["statusAtCapture"], "fireOfNote": f["fireOfNote"],
                "wasFireOfNote": f["wasFireOfNote"], "sizeHa": f["hindsightSizeHa"]})
        days = []
        for entry in index["days"]:
            if entry["kind"] == "repository-snapshot":
                day = day_from_snapshot(snapshot)
                made_from = entry["source"]["sha256"]
                if day["source"]["sha256"] != made_from:
                    raise SeasonError(
                        f"status day {entry['date']} was made from a {entry['source']['file']} "
                        f"with sha256 {made_from[:12]}; the one here is "
                        f"{day['source']['sha256'][:12]}. If the snapshot was replaced on "
                        "purpose, regenerate the season from the raw inputs")
                if "supersedes" in entry["source"]:
                    day["source"]["supersedes"] = entry["source"]["supersedes"]
            else:
                day = {"date": entry["date"], "kind": entry["kind"],
                       "ms": parse_utc(entry["fetchedAt"]), "source": entry["source"],
                       "fires": committed(entry["fires"]["file"]),
                       "perims": committed(entry["perims"]["file"])}
            days.append(day)
        capture = season["capture"]
        return {"year": season["season"],
                "capture": {"capturedAt": capture["capturedAt"], "layer": capture["layer"],
                            "manifest": capture["manifest"], "files": capture["files"]},
                "records": records, "days": days, "mirrorHistory": index.get("mirrorHistory"),
                "captureFolders": json.loads(committed(f"{year}.prov.json"))["captureFolders"]}
    except (KeyError, TypeError, ValueError) as e:
        raise SeasonError(f"the {year} season files are not in the shape the generator "
                          f"writes ({type(e).__name__}: {e})") from None


# ---- building ------------------------------------------------------------------------------
def sequence(number):
    """A fire number is a centre letter, a zone character and a province-wide sequence number."""
    return int(number[2:])


def open_day(day):
    """Parse one status day and hold it to the mirror's shape, feature by feature."""
    opened = dict(day)
    for name, props in (("fires", FIRE_PROPS), ("perims", PERIM_PROPS)):
        what = f"status day {day['date']} {name}"
        doc = json.loads(day[name])
        if list(doc) != ["fetchedAt", "source", "data"]:
            raise SeasonError(f"{what}: keys {list(doc)} are not the mirror's")
        if local_date(parse_utc(doc["fetchedAt"])) != day["date"]:
            raise SeasonError(f"{what}: fetched {doc['fetchedAt']}, which is not that local day")
        for f in doc["data"]["features"]:
            if list(f) != ["type", "geometry", "properties"] or tuple(f["properties"]) != props:
                raise SeasonError(f"{what}: a feature is not in the mirror's shape "
                                  f"({list(f)}, {list(f['properties'])})")
            if not not_out(f):
                raise SeasonError(f"{what}: {f['properties']['FIRE_NUMBER']} has status "
                                  f"{f['properties']['FIRE_STATUS']!r}; the mirror drops those")
        opened[name + "Features"] = doc["data"]["features"]
        opened[name + "FetchedAt"] = doc["fetchedAt"]
    numbers = [f["properties"]["FIRE_NUMBER"] for f in opened["firesFeatures"]]
    if len(set(numbers)) != len(numbers):
        raise SeasonError(f"status day {day['date']}: a fire number appears twice")
    if parse_utc(opened["firesFetchedAt"]) != day["ms"]:
        raise SeasonError(f"status day {day['date']}: the file and its index disagree on the time")
    return opened


def assess(rec, year, cap_ms, seen):
    """One fire's dates: possible or not, why not, and whether a rule places it anyway.

    `seen` is every status-day record that lists the fire: (date, time of the record, the
    ignition date that record gave it). Returns (ignited, out, dates) for the season file."""
    ig, out = rec["ignitionMs"], rec["outMs"]
    times = [t for _, t, _ in seen]
    flags = []
    if ig is None:
        flags.append("ignition-missing")
    else:
        if local(ig).year != year:
            flags.append("ignition-outside-fire-year")
        if ig > cap_ms:
            flags.append("ignition-after-capture")
    if out is None:
        if rec["status"] == "Out":
            flags.append("out-missing")
    else:
        if rec["status"] != "Out":
            flags.append("out-date-but-not-out")
        if out > cap_ms:
            flags.append("out-after-capture")
        if ig is not None and out < ig:
            flags.append("out-before-ignition")
    if ig is not None and any(t < ig for t in times):
        flags.append("listed-before-ignition")
    if not flags:
        return local_date(ig), local_date(out), {"ok": True}

    def possible(v):
        return (local(v).year == year and v <= cap_ms and (out is None or v <= out)
                and all(v <= t for t in times))

    known = sorted({v for _, _, v in seen if v is not None})
    rule = ignited = None
    if flags == ["out-before-ignition"] and local_date(ig) == local_date(out):
        rule, ignited = "same-local-day", local_date(ig)
    elif not OUT_FAULTS & set(flags) and known and all(possible(v) for v in known):
        if len({local_date(v) for v in known}) == 1:
            rule, ignited = "dated-record", local_date(known[0])
    dates = {
        "ok": False, "flags": flags, "onTimeline": rule is not None, "rule": rule,
        "recorded": {"ignition": iso_utc(ig), "ignitionLocalDate": local_date(ig),
                     "out": iso_utc(out), "outLocalDate": local_date(out)},
        "statusDays": {"listedOn": [d for d, _, _ in seen],
                       "ignitionAsKnown": [iso_utc(v) for v in known]} if seen else None,
        "bracket": None}
    return ignited, (local_date(out) if rule else None), dates


def as_known(props, day_ms, year):
    """The same year and order tests, applied to a status day's own ignition date."""
    ig = props["IGNITION_DATE"]
    flags = []
    if ig is None:
        flags.append("ignition-missing")
    else:
        if local(ig).year != year:
            flags.append("ignition-outside-fire-year")
        if ig > day_ms:
            flags.append("listed-before-ignition")
    return flags


def centre_of(number):
    if not FIRE_NUMBER.fullmatch(number) or number[0] not in LETTER_CENTRE:
        raise SeasonError(f"{number!r} is not a fire number this knows how to read")
    return LETTER_CENTRE[number[0]]


def under_1ha(size):
    return size is not None and size < 1


def build(state):
    """Every file under data/season/ for one season, as {relative path: bytes}. A pure function
    of the state: read_raw() and read_committed() must give the same bytes or the gate is red."""
    year, cap = state["year"], state["capture"]
    cap_ms = parse_utc(cap["capturedAt"])
    cap_date = local_date(cap_ms)
    days = [open_day(d) for d in state["days"]]

    seen = {}
    for d in days:
        for f in d["firesFeatures"]:
            p = f["properties"]
            seen.setdefault(p["FIRE_NUMBER"], []).append((d["date"], d["ms"], p["IGNITION_DATE"]))

    # -- the season record -------------------------------------------------------------------
    fires = []
    numbers = set()
    for r in sorted(state["records"], key=lambda r: (sequence(r["fire"]), r["fire"])):
        n = r["fire"]
        if n in numbers:
            raise SeasonError(f"{n} appears twice in the incidents layer")
        numbers.add(n)
        if r["centreCode"] not in CENTRES or CENTRES[r["centreCode"]][1] != centre_of(n):
            raise SeasonError(f"{n}: fire centre code {r['centreCode']!r} does not go with "
                              "the letter that begins its number")
        ignited, out, dates = assess(r, year, cap_ms, seen.get(n, []))
        fires.append({
            "fire": n, "name": r["name"], "place": r["place"], "lat": r["lat"], "lon": r["lon"],
            "centre": centre_of(n), "cause": r["cause"], "ignited": ignited, "out": out,
            "statusAtCapture": r["status"], "fireOfNote": r["fireOfNote"],
            "wasFireOfNote": r["wasFireOfNote"], "hindsightSizeHa": r["sizeHa"],
            "ignitionMs": r["ignitionMs"], "outMs": r["outMs"], "dates": dates})
    by_number = {f["fire"]: f for f in fires}
    for d in days:
        if d["kind"] == "mirror-history":       # the file IS the recovered copy, or it is not
            for name in ("fires", "perims"):
                src = d["source"][name]
                if (len(d[name]), digest(d[name])) != (src["bytes"], src["sha256"]):
                    raise SeasonError(f"status day {d['date']} {name}: the file is not the "
                                      "recovered copy its index entry names")
        elif d["kind"] == "capture" and d["source"]["manifest"] == cap["manifest"]:
            # One capture made this day and the season file. They must tell one story.
            day = {f["properties"]["FIRE_NUMBER"]: tuple(f["properties"][k] for k in SHARED)
                   for f in d["firesFeatures"]}
            file = {f["fire"]: (f["statusAtCapture"], f["hindsightSizeHa"], f["cause"],
                                f["name"], f["place"], f["ignitionMs"], f["fireOfNote"])
                    for f in fires if f["statusAtCapture"] not in (None, "Out")}
            day = {n: v[:-1] + (yes_no(v[-1], n),) for n, v in day.items()}
            if day != file:
                odd = sorted(n for n in set(day) | set(file) if day.get(n) != file.get(n))
                raise SeasonError(f"status day {d['date']} and the season file come from one "
                                  f"capture and disagree on {', '.join(odd[:8])}")
    # Evidence for a flagged fire, never a placement: the possible-dated fires numbered just
    # before and just after it. Numbers are issued as fires enter the record.
    good = [(sequence(f["fire"]), f) for f in fires if f["dates"]["ok"]]
    order = [s for s, _ in good]
    for f in fires:
        if not f["dates"]["ok"]:
            at = bisect.bisect_left(order, sequence(f["fire"]))
            near = {"before": good[at - 1][1] if at else None,
                    "after": good[at][1] if at < len(good) else None}
            f["dates"]["bracket"] = {
                k: v and {"fire": v["fire"], "ignited": v["ignited"]} for k, v in near.items()}

    flagged = [f for f in fires if not f["dates"]["ok"]]
    placed = [f for f in fires if f["ignited"] is not None]
    flag_counts = {k: sum(k in f["dates"]["flags"] for f in flagged) for k in DATE_FLAGS}
    impossible = {
        "fires": len(flagged),
        "onTimeline": sum(f["dates"]["onTimeline"] for f in flagged),
        "notOnTimeline": sum(not f["dates"]["onTimeline"] for f in flagged),
        "byFlag": {k: v for k, v in flag_counts.items() if v},
        "byRule": {k: sum(f["dates"]["rule"] == k for f in flagged) for k in TIMELINE_RULES}}
    status_tally = tally(f["statusAtCapture"] for f in fires)

    season = {
        "season": year,
        "what": f"One record per fire of British Columbia's {year} wildfire season, as the BC "
                "Wildfire Service's public incidents layer stood when this copy was taken. "
                "Hindsight throughout: read the notes before using a value.",
        "capture": {"capturedAt": cap["capturedAt"], "localDate": cap_date,
                    "utcOffset": utc_offset(cap_ms), "layer": cap["layer"],
                    "manifest": cap["manifest"], "files": cap["files"]},
        "timeZone": ZONE_NAME,
        "total": len(fires),
        "statusTally": status_tally,
        "impossibleDates": impossible,
        "notes": [
            "HINDSIGHT. Every value here is the public record as it stood at the capture time, "
            "after the fact: the size, the final status, the date a fire was declared out, and "
            "an ignition date the publisher goes on revising after a fire is first reported. "
            "None of it was knowable on the day. Nothing in this file may be fed to the "
            "dispatch model, or to anything else that plays out a decision made on a past day. "
            "The status-day files under days/ are the only files here that say what was known "
            "on a date.",
            "hindsightSizeHa is the layer's estimated size in hectares at capture. It carries "
            "that name so that it cannot be mistaken for a size known on any earlier day.",
            "Dates. The source stores epoch milliseconds in UTC; ignitionMs and outMs are those "
            "values, untouched. ignited and out are the calendar dates of those instants in the "
            f"{ZONE_NAME} time zone, the same local date that keys a status day.",
            f"Impossible dates. {len(flagged)} fires carry a date that cannot be true. They are "
            "kept and counted, never repaired and never dropped: the recorded values stay in "
            "ignitionMs, outMs and dates.recorded, and dates.flags gives the reason. Such a fire "
            "is on the day-by-day timeline only where a rule in timelineRules places it "
            f"({impossible['onTimeline']} are, {impossible['notOnTimeline']} are not). A fire "
            "that is not on the timeline has ignited and out set to null and is still in every "
            "count that is not a count of days.",
            "A fire with an out date of null and a status other than Out was not out when the "
            "copy was taken.",
            "name and place are the layer's INCIDENT_NAME and GEOGRAPHIC_DESCRIPTION exactly as "
            "published, trailing spaces included. name is often only the fire number, and is "
            "null for some fires.",
            "lat and lon are the layer's own LATITUDE and LONGITUDE attributes, four decimal "
            "places. The status-day files carry the point geometry instead; the two differ by "
            "a few metres.",
            "centre is this project's label for the layer's integer fire-centre code; the layer "
            "publishes no names. See centres.",
            "The Information was modified: reduced to the fields below, dates converted to "
            "local calendar dates, sorted by fire number sequence, and checked for impossible "
            "dates. " + NO_ENDORSEMENT,
        ],
        "fields": {
            "fire": "FIRE_NUMBER: a centre letter, a zone character and a province-wide "
                    "sequence number. The fires are sorted by that sequence.",
            "name": "INCIDENT_NAME.",
            "place": "GEOGRAPHIC_DESCRIPTION ('Approximate Location').",
            "lat": "LATITUDE, degrees north.",
            "lon": "LONGITUDE, degrees east (negative here).",
            "centre": "Fire centre, by name. See centres.",
            "cause": "FIRE_CAUSE ('Suspected Cause').",
            "ignited": "TIMELINE DATE. The local date of IGNITION_DATE ('Ignition Date'), or "
                       "null if the fire is not on the timeline. Hindsight.",
            "out": "TIMELINE DATE. The local date of FIRE_OUT_DATE; null if the fire was not "
                   "out at capture or is not on the timeline. Hindsight.",
            "statusAtCapture": "FIRE_STATUS ('Stage of Control') when the copy was taken.",
            "fireOfNote": "FIRE_OF_NOTE_IND at capture.",
            "wasFireOfNote": "WAS_FIRE_OF_NOTE_IND at capture.",
            "hindsightSizeHa": "The layer's estimated size in hectares AT CAPTURE. Hindsight; "
                               "never an input to anything that decides on a past day.",
            "ignitionMs": "IGNITION_DATE exactly as published: epoch milliseconds, UTC.",
            "outMs": "FIRE_OUT_DATE exactly as published, or null.",
            "dates": "{ok: true}, or the flags, the recorded values, what the status days say, "
                     "and whether a rule places the fire on the timeline. dates.bracket names "
                     "the fires with possible dates numbered just before and just after; "
                     "numbers are issued as fires enter the record, so it is evidence of when "
                     "this one did, and nothing is ever placed by it.",
        },
        "dateFlags": DATE_FLAGS,
        "timelineRules": TIMELINE_RULES,
        "centres": {str(code): {"letter": letter, "name": name}
                    for code, (letter, name) in CENTRES.items()},
        "licence": LICENCE,
        "licenceUrl": LICENCE_URL,
        "attribution": ATTRIBUTION,
        "publisher": PUBLISHER,
        "noEndorsement": NO_ENDORSEMENT,
        "notForEmergencyUse": NOT_FOR_EMERGENCY,
        "fires": fires,
    }

    # -- the day-by-day timeline, from the season record (hindsight) ---------------------------
    first = min(f["ignited"] for f in placed)
    timeline = []
    active = 0
    started, went_out = tally(f["ignited"] for f in placed), tally(
        f["out"] for f in placed if f["out"] is not None)
    for date in date_range(first, cap_date):
        active += started.get(date, 0) - went_out.get(date, 0)
        timeline.append({"date": date, "started": started.get(date, 0),
                         "out": went_out.get(date, 0), "active": active})
    peak = max(t["active"] for t in timeline)
    spans = sorted((f["outMs"] - f["ignitionMs"]) / DAY_MS
                   for f in fires if f["dates"]["ok"] and f["outMs"] is not None)
    out_fires = [f for f in fires if f["statusAtCapture"] == "Out"]
    small = [f for f in fires if under_1ha(f["hindsightSizeHa"])]
    # How closely the numbering follows the calendar: what dates.bracket is worth as evidence.
    dated = [datetime.date.fromisoformat(f["ignited"]) for f in fires if f["dates"]["ok"]]
    gaps = [abs((b - a).days) for a, b in zip(dated, dated[1:])]

    # -- the status days, each as known that day -----------------------------------------------
    index_days, summary_days = [], []
    listed_ever = {}
    for d in days:
        props = [f["properties"] for f in d["firesFeatures"]]
        listed = {p["FIRE_NUMBER"] for p in props}
        for n in listed:
            centre_of(n)                # a number this cannot read stops the run here
        for n in sorted(listed):
            listed_ever.setdefault(n, []).append(d["date"])
        burning = {f["fire"] for f in fires if f["dates"]["ok"] and f["ignitionMs"] <= d["ms"]
                   and (f["outMs"] is None or f["outMs"] > d["ms"])}
        strangers = []
        for n in sorted(listed - numbers):
            same = [f["fire"] for f in fires if sequence(f["fire"]) == sequence(n)]
            strangers.append({"fire": n, "sameSequenceNumberAs": same[0] if same else None})
        odd = [{"fire": p["FIRE_NUMBER"], "flags": as_known(p, d["ms"], year),
                "ignition": iso_utc(p["IGNITION_DATE"])}
               for p in props if as_known(p, d["ms"], year)]
        index_days.append({
            "date": d["date"], "kind": d["kind"], "fetchedAt": d["firesFetchedAt"],
            "fires": {"file": f"days/{d['date']}/fires.json", "count": len(props),
                      "byStatus": tally(p["FIRE_STATUS"] for p in props),
                      "bytes": len(d["fires"]), "sha256": digest(d["fires"])},
            "perims": {"file": f"days/{d['date']}/perims.json",
                       "count": len(d["perimsFeatures"]), "fetchedAt": d["perimsFetchedAt"],
                       "bytes": len(d["perims"]), "sha256": digest(d["perims"])},
            "source": d["source"],
            "notInSeasonFile": strangers,
            "impossibleAsKnown": sorted(odd, key=lambda o: (sequence(o["fire"]), o["fire"]))})
        summary_days.append({
            "date": d["date"], "fetchedAt": d["firesFetchedAt"], "fires": len(props),
            "byStatus": tally(p["FIRE_STATUS"] for p in props),
            "byCause": tally(p["FIRE_CAUSE"] for p in props),
            "byCentre": tally(centre_of(p["FIRE_NUMBER"]) for p in props),
            "under1ha": sum(under_1ha(p["CURRENT_SIZE"]) for p in props),
            "fireOfNote": sum(p["FIRE_STATUS"] == "Fire of Note"
                              or p["FIRE_OF_NOTE_IND"] in ("Y", "Yes") for p in props),
            "perimeters": len(d["perimsFeatures"]),
            "hindsightAtThatMoment": {"burning": len(burning), "alsoListed": len(burning & listed),
                                      "notListed": len(burning - listed),
                                      "listedNotBurning": len(listed - burning)}})

    # How far the ignition date moves between a fire's first dated record and the capture.
    shifts = []
    for n, when in sorted(seen.items()):
        then, now = when[0][2], by_number[n]["ignitionMs"] if n in by_number else None
        if then is not None and now is not None:
            shifts.append((now - then, local_date(now) != local_date(then)))
    moved = sorted(s for s, _ in shifts if s)

    summary = {
        "season": year,
        "what": f"Facts about the {year} season derived from {year}.json and the status-day "
                "files by pipeline/season.py. Generated, never typed: python3 "
                "pipeline/season.py --check recomputes every number here from committed files.",
        "capturedAt": cap["capturedAt"],
        "capturedLocalDate": cap_date,
        "timeZone": ZONE_NAME,
        "notes": [
            "Everything outside statusDays is HINDSIGHT: computed from the record as it stood "
            "at capture. Only statusDays says what was known on a day.",
            "under1ha counts fires whose size at capture is strictly less than 1 hectare. For "
            "a fire that is out that is how it ended; for one that is not out it is only the "
            "size at capture.",
            "ignitionToOut is the median of (out instant - ignition instant) over the fires "
            "that are out and whose dates are possible. Fires with an impossible date are left "
            "out of it, placed on the timeline or not.",
            "timeline: a fire is active on a day when ignited <= day < out, by local date: it "
            "was burning at the end of that day. A fire that starts and is out on one date is "
            "active on no day; it is in started and in out for that date. active on any day is "
            "the fires started up to and including it minus the fires out up to and including "
            "it. Fires not on the timeline are in neither. The last day is the capture date and "
            "ends when the copy was taken, not at midnight.",
            "statusDays: counts of the fires listed in that day's record (not out, as known "
            "then). byCentre goes by the letter that begins the fire number. "
            "hindsightAtThatMoment asks the season file the same question at the same instant: "
            "burning is the fires with possible dates that had ignited and were not yet out; "
            "notListed is how many of those the day's record did not show; listedNotBurning is "
            "how many it showed that hindsight does not count.",
            "ignitionRevised compares, for every fire in both the season file and a status "
            "day, the ignition instant at capture with the one in the first status day that "
            "listed the fire.",
            "numbering takes the fires with possible dates in the order of their sequence "
            "numbers and asks how many local dates separate each one's ignition from that of "
            "the fire numbered just before it. It is the measure of what dates.bracket in the "
            "season file is worth: evidence of when a fire entered the record, never proof.",
        ],
        "total": len(fires),
        "statusAtCapture": status_tally,
        "notOutAtCapture": len(fires) - len(out_fires),
        "under1ha": {"fires": len(small),
                     "out": sum(f["statusAtCapture"] == "Out" for f in small),
                     "notOut": sum(f["statusAtCapture"] != "Out" for f in small),
                     "sizeZero": sum(f["hindsightSizeHa"] == 0 for f in fires),
                     "sizeUnknown": sum(f["hindsightSizeHa"] is None for f in fires)},
        "ignitionToOut": {"medianDays": round(statistics.median(spans), 2) if spans else None,
                          "medianHours": round(statistics.median(spans) * 24, 1) if spans else None,
                          "fires": len(spans), "outFiresLeftOut": len(out_fires) - len(spans)},
        "byCause": tally(f["cause"] for f in fires),
        "byCentre": tally(f["centre"] for f in fires),
        "fireOfNote": {"atCapture": sum(f["fireOfNote"] for f in fires),
                       "atCaptureOrEarlier": sum(f["fireOfNote"] or f["wasFireOfNote"]
                                                 for f in fires)},
        "impossibleDates": dict(impossible, list=[
            {"fire": f["fire"], "flags": f["dates"]["flags"],
             "onTimeline": f["dates"]["onTimeline"], "rule": f["dates"]["rule"]}
            for f in flagged]),
        "numbering": {"firesWithPossibleDates": len(dated), "pairs": len(gaps),
                      "ignitedTheSameDay": sum(g == 0 for g in gaps),
                      "ignitedWithinOneDay": sum(g <= 1 for g in gaps),
                      "ignitedWithinSevenDays": sum(g <= 7 for g in gaps),
                      "largestGapDays": max(gaps) if gaps else None},
        "timeline": {"from": first, "to": cap_date, "firesOnTimeline": len(placed),
                     "firesNotOnTimeline": len(fires) - len(placed),
                     "peak": {"active": peak,
                              "dates": [t["date"] for t in timeline if t["active"] == peak]},
                     "days": timeline},
        "statusDays": {"count": len(days), "dates": [d["date"] for d in days],
                       "days": summary_days},
        "coverage": {"firesListedOnAStatusDay": len(listed_ever),
                     "ofThemInSeasonFile": len(set(listed_ever) & numbers),
                     "ofThemNotInSeasonFile": sorted(set(listed_ever) - numbers),
                     "seasonFiresNeverListed": len(numbers - set(listed_ever))},
        "ignitionRevised": {
            "firesCompared": len(shifts), "sameInstant": sum(s == 0 for s, _ in shifts),
            "earlierAtCapture": sum(s < 0 for s, _ in shifts),
            "laterAtCapture": sum(s > 0 for s, _ in shifts),
            "differentLocalDate": sum(changed for _, changed in shifts),
            "medianShiftHoursWhereMoved": (round(statistics.median(moved) / 3_600_000, 1)
                                           if moved else None)},
    }

    index = {
        "season": year,
        "what": "The status days: each America/Vancouver date that has a dated first-party "
                "copy of the public record, and where that copy came from. A status day is what "
                "was KNOWN that day, and is the only thing a replay may show its fleet.",
        "timeZone": ZONE_NAME,
        "notes": [
            "Each day is the LAST copy of that local date: fires.json and perims.json, in the "
            "document shape and with the property names pipeline/live.py serves, so the page "
            "can read a day through the code path it uses for live data.",
            "A day holds the fires that were not out, with status, size and ignition date as "
            "the record gave them then. Nothing in a day file comes from a later record.",
            "fetchedAt is the time of the fires copy. byStatus counts FIRE_STATUS as published "
            "that day; in August 'Fire of Note' was a status of its own.",
            "notInSeasonFile lists fire numbers a day carries that the season file does not, "
            "with the season fire that has the same sequence number where there is one: a fire "
            "renumbered after that day.",
            "impossibleAsKnown lists fires whose ignition date in that day's own record cannot "
            "be true: outside the fire year, or later than the record itself. The day files "
            "keep those values untouched.",
            "sha256 and bytes under fires and perims are of the committed file. For a "
            "mirror-history day the file IS the recovered copy, so they equal the source's.",
            "The Information was modified: a capture day is filtered and its perimeters "
            "generalised, a snapshot day is reduced to the mirror's property names. "
            + NO_ENDORSEMENT + " " + NOT_FOR_EMERGENCY,
        ],
        "shape": {"document": ["fetchedAt", "source", "data"],
                  "feature": ["type", "geometry", "properties"],
                  "fires": list(FIRE_PROPS), "perims": list(PERIM_PROPS)},
        "kinds": {
            "repository-snapshot": "data/snapshot.json, the snapshot bundled with this "
                                   "repository, reduced to the mirror's property names.",
            "mirror-history": "A copy of this site's own live mirror, recovered from the site's "
                              "deploy history and kept byte for byte.",
            "capture": "A complete copy of both public layers, filtered the way the mirror "
                       "filters (status not Out, which also drops a null status), with "
                       f"perimeters generalised to {GENERALISE_DEG} degrees and "
                       f"{COORD_DECIMALS} decimal places as the mirror's request does.",
        },
        "mirrorHistory": state.get("mirrorHistory"),
        "licence": LICENCE,
        "licenceUrl": LICENCE_URL,
        "attribution": ATTRIBUTION,
        "publisher": PUBLISHER,
        "count": len(days),
        "dates": [d["date"] for d in days],
        "days": index_days,
    }

    files = {f"{year}.json": render(season), f"{year}.summary.json": render(summary),
             f"{year}.days.json": render(index)}
    for d in days:
        files[f"days/{d['date']}/fires.json"] = d["fires"]
        files[f"days/{d['date']}/perims.json"] = d["perims"]
    files[f"{year}.prov.json"] = provenance(year, cap, state, days, summary, files)
    return files


def provenance(year, cap, state, days, summary, files):
    """The sidecar, in the convention of data/*.prov.json, plus the sha256 of every raw input."""
    inputs = [{"what": "the capture's manifest: every request, its sha256 and the layers' own "
                       "counts", "retrievedAt": cap["capturedAt"], **cap["manifest"]}]
    inputs += [{"what": f"capture file {f['name']}", "retrievedAt": cap["capturedAt"],
                "bytes": f["bytes"], "sha256": f["sha256"]} for f in cap["files"]]
    history = state.get("mirrorHistory")
    if history:
        inputs.append({"what": "the index of the live-mirror copies recovered from the site's "
                               "deploy history", "retrievedAt": None, **history["index"]})
    for d in days:
        src = d["source"]
        if d["kind"] == "mirror-history":
            for name, label in (("fires", "fires"), ("perims", "perimeters")):
                inputs.append({"what": f"status day {d['date']}: the live mirror's {label} "
                                       "copy, from the site's deploy history",
                               "retrievedAt": src[name]["fetchedAt"],
                               "bytes": src[name]["bytes"], "sha256": src[name]["sha256"]})
        elif d["kind"] == "repository-snapshot":
            inputs.append({"what": f"status day {d['date']}: {src['file']}, in this repository",
                           "retrievedAt": src["retrievedAt"], "bytes": src["bytes"],
                           "sha256": src["sha256"]})
        elif src["manifest"] != cap["manifest"]:
            inputs.append({"what": f"status day {d['date']}: a later capture's manifest",
                           "retrievedAt": src["capturedAt"], **src["manifest"]})
            inputs += [{"what": f"status day {d['date']}: capture file {f['name']}",
                        "retrievedAt": src["capturedAt"], "bytes": f["bytes"],
                        "sha256": f["sha256"]} for f in src["files"]]
    flagged = summary["impossibleDates"]
    doc = {
        "file": f"{year}.json",
        "description":
            f"British Columbia's {year} wildfire season as data. {year}.json: one record per "
            f"fire ({summary['total']:,} fires) as the BC Wildfire Service's public incidents "
            f"layer stood at {cap['capturedAt']}; hindsight in every field. {year}.summary.json: "
            f"the facts derived from it. {year}.days.json and days/: {len(days)} status days, "
            "each the last dated copy of the public record for one America/Vancouver date, in "
            "the shape the live mirror serves. This sidecar covers all of them.",
        "source": [f["url"] for f in cap["files"]] + [
            "data/snapshot.json (this repository)",
            "copies of this site's live mirror (pipeline/live.py output) recovered from the "
            "site's deploy history; raw copies are not in the repository, see inputs"],
        "catalogue": CATALOGUE,
        "publisher": PUBLISHER,
        "licence": LICENCE,
        "licenceUrl": LICENCE_URL,
        "attribution": ATTRIBUTION,
        "retrievedAt": cap["capturedAt"],
        "generator": "pipeline/season.py",
        "notes":
            "Regenerate with: python3 pipeline/season.py <capture folder> (no network; under "
            "ten seconds). The raw inputs are not in the repository: a capture folder holding "
            "complete copies of the two public layers with a MANIFEST.json, and a folder of "
            "recovered live-mirror copies with an INDEX.json. Every raw input is named under "
            "inputs by sha256 and size, so anyone holding the same bytes can prove it. "
            "captureFolders pins every folder used, including superseded copies: its sha256 "
            "hashes the compact JSON list of sorted relative file names and file sha256s. "
            "Raw checks use exactly that record; extra captures are reported and ignored, "
            "while missing or changed named captures fail. Regeneration without --check "
            "deliberately adopts all eligible captures. "
            "python3 pipeline/season.py --check rebuilds everything that can be rebuilt from "
            "committed files and compares bytes. Modifications: the incidents layer is reduced "
            "to sixteen fields per fire and sorted by fire-number sequence; epoch-millisecond "
            f"dates are converted to {ZONE_NAME} calendar dates; {flagged['fires']} fires "
            "carrying an impossible date are flagged, kept and counted, and left off the "
            f"day-by-day timeline unless a stated rule places them ({flagged['onTimeline']} "
            f"placed, {flagged['notOnTimeline']} not); a capture day is filtered to status not "
            f"Out and its perimeters generalised to {GENERALISE_DEG} degrees and "
            f"{COORD_DECIMALS} decimal places; a snapshot day is reduced to the mirror's "
            "property names; a mirror-history day is unmodified. The season file is hindsight "
            "and must never be an input to the dispatch model; the status days are what was "
            "known on each day. The Information was modified. " + NO_ENDORSEMENT + " "
            + NOT_FOR_EMERGENCY,
        "captureFolders": state["captureFolders"],
        "inputs": inputs,
        "outputs": [{"file": name, "bytes": len(data), "sha256": digest(data)}
                    for name, data in sorted(files.items())],
    }
    house = json.loads(SNAPSHOT.with_suffix(".prov.json").read_text())
    doc.update(decision="redistributed", licenceStatement=house["licenceStatement"],
               licenceEvidence=house["licenceEvidence"] + " Raw capture inputs are named below by digest.",
               licenceReason="Dated BC Wildfire Service records retained under the snapshot's recorded terms.",
               sha256=digest(files[f"{year}.json"]),
               measurements={"bytes": len(files[f"{year}.json"])})
    doc = {**{key: doc[key] for key in house},
           "captureFolders": doc["captureFolders"], "inputs": doc["inputs"], "outputs": doc["outputs"],
           "documentation": json.loads((pathlib.Path(__file__).with_name("season-notes.json")).read_text())}
    return (json.dumps(doc, indent=2) + "\n").encode("ascii")


# ---- the table -----------------------------------------------------------------------------
def table(season):
    """The impossible-date table: every flagged fire, raw values first."""
    flagged = [f for f in season["fires"] if not f["dates"]["ok"]]
    info = season["impossibleDates"]
    lines = [f"Impossible dates in the {season['season']} season file: {info['fires']} fires "
             f"of {season['total']:,} ({info['onTimeline']} placed on the timeline by a rule, "
             f"{info['notOnTimeline']} not). Raw values are epoch milliseconds, UTC.", ""]
    head = ("fire", "IGNITION_DATE", "as UTC", "FIRE_OUT_DATE", "as UTC", "status", "ha")
    rows = [(f["fire"], str(f["ignitionMs"]), f["dates"]["recorded"]["ignition"] or "-",
             str(f["outMs"]), f["dates"]["recorded"]["out"] or "-", f["statusAtCapture"],
             str(f["hindsightSizeHa"])) for f in flagged]
    widths = [max(len(r[i]) for r in [head] + rows) for i in range(len(head))]
    for r in [head] + rows:
        lines.append("  ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip())
    lines.append("")
    for f in flagged:
        d = f["dates"]
        where = (f"ON the timeline from {f['ignited']} by rule {d['rule']}" if d["onTimeline"]
                 else "NOT on the timeline")
        lines.append(f"{f['fire']}  {', '.join(d['flags'])}  ->  {where}")
        rec = d["recorded"]
        lines.append(f"        recorded local dates: ignition {rec['ignitionLocalDate']}, "
                     f"out {rec['outLocalDate']}")
        if d["statusDays"]:
            days = d["statusDays"]["listedOn"]
            lines.append(f"        status days listing it: {days[0]} to {days[-1]} "
                         f"({len(days)}); ignition as known then: "
                         f"{', '.join(d['statusDays']['ignitionAsKnown']) or 'none'}")
        else:
            lines.append("        on no status day")
        near = d["bracket"]
        lines.append("        numbered between: " + " and ".join(
            f"{v['fire']} (ignited {v['ignited']})" if v else "nothing"
            for v in (near["before"], near["after"])))
    return "\n".join(lines)


# ---- writing and checking ------------------------------------------------------------------
def on_disk(year, out_dir):
    """This season's files under out_dir, so that a stray one is seen and named."""
    out_dir = pathlib.Path(out_dir)
    found = {p.name for p in out_dir.glob(f"{year}.*") if p.is_file()}
    found |= {p.relative_to(out_dir).as_posix()
              for p in out_dir.glob(f"days/{year}-*/*") if p.is_file()}
    return found


def drift(files, year, out_dir):
    out_dir = pathlib.Path(out_dir)
    problems = []
    for name, data in sorted(files.items()):
        path = out_dir / name
        if not path.is_file():
            problems.append(f"{name}: missing")
        elif path.read_bytes() != data:
            problems.append(f"{name}: differs from a fresh regeneration")
    problems += [f"{name}: not produced by the generator"
                 for name in sorted(on_disk(year, out_dir) - set(files))]
    return problems


def write(files, year, out_dir):
    out_dir = pathlib.Path(out_dir)
    changed = 0
    for name, data in sorted(files.items()):
        path = out_dir / name
        if not path.is_file() or path.read_bytes() != data:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            changed += 1
    return changed, sorted(on_disk(year, out_dir) - set(files))


def committed_years(season_dir=SEASON_DIR):
    return sorted(int(p.stem) for p in pathlib.Path(season_dir).glob("[0-9][0-9][0-9][0-9].json"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capture", nargs="?", help="the season's capture folder (raw input)")
    ap.add_argument("--mirror-history", metavar="DIR",
                    help="recovered live-mirror copies (default: ../../mirror-history from "
                         "the capture folder)")
    ap.add_argument("--through", metavar="YYYY-MM-DD",
                    help="last status day to produce (default: the capture's own local date)")
    ap.add_argument("--check", action="store_true",
                    help="write nothing; exit 1 if the committed files differ")
    ap.add_argument("--table", action="store_true", help="print the impossible-date table")
    ap.add_argument("--out", metavar="DIR", default=str(SEASON_DIR),
                    help="where the season files live (default: data/season)")
    ap.add_argument("--snapshot", metavar="FILE", default=str(SNAPSHOT),
                    help="the repository snapshot (default: data/snapshot.json)")
    args = ap.parse_args(argv)
    try:
        if args.capture:
            folders = None
            through = args.through
            if args.check:
                year, _ = records_from(read_capture(pathlib.Path(args.capture)))
                record = read_committed(year, args.out, args.snapshot)
                folders = record["captureFolders"]
                through = through or record["days"][-1]["date"]
            states = [read_raw(args.capture, args.mirror_history, args.snapshot, through, folders)]
        else:
            if not (args.check or args.table):
                ap.error("give a capture folder to regenerate from, or --check, or --table")
            years = committed_years(args.out)
            if not years:
                raise SeasonError(f"no season file under {pathlib.Path(args.out).name}/")
            states = [read_committed(y, args.out, args.snapshot) for y in years]
        status = 0
        for state in states:
            year = state["year"]
            files = build(state)
            season = json.loads(files[f"{year}.json"])
            if args.table or not args.check:
                print(table(season))
                print()
            if args.check:
                problems = drift(files, year, args.out)
                for p in problems:
                    print(f"season: {p}", file=sys.stderr)
                basis = "the raw inputs" if args.capture else "committed files alone"
                if problems:
                    status = 1
                    print(f"season: {len(problems)} file(s) of {year} are not what "
                          f"{basis} produce", file=sys.stderr)
                else:
                    print(f"season: {year}: {len(files)} files match a regeneration from "
                          f"{basis} ({season['total']:,} fires, "
                          f"{len(state['days'])} status days)")
            elif args.capture:
                changed, strays = write(files, year, args.out)
                print(f"season: {year}: {len(files)} files, {changed} written "
                      f"({season['total']:,} fires, {len(state['days'])} status days: "
                      f"{', '.join(d['date'] for d in state['days'])})")
                for name in strays:
                    print(f"season: {name} is in the way: the generator does not produce it "
                          "and has not touched it", file=sys.stderr)
                status = 1 if strays else status
        return status
    except SeasonError as e:
        print(f"season: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
