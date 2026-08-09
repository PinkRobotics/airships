#!/usr/bin/env python3
"""First-party mirror of the live wildfire feeds for pinkrobotics.ca/airships/.

Visitors to the monitor read data/live/*.json from OUR server; this script is the only
thing that talks to the upstream feeds. One fetch per interval total, instead of one per
viewer — traffic to the site must never multiply load on emergency infrastructure.

    python3 tools/airships_live.py           # fetch into pinkrobotics/airships/data/live/
    python3 tools/airships_live.py --push    # ...then rsync ONLY that dir to the edge docroots

Cadence guidance (enforced here, not by the caller): fires/perimeters refresh when older
than 8 minutes (upstream cadence is ~15), hotspots when older than 25 (satellites pass a
handful of times a day). Run it every 10 minutes from a timer and the effective upstream
rate is ~6 fires-requests/hour regardless of visitor count.

File format: {"fetchedAt": iso8601-utc, "source": url, "data": <upstream json>} — the page
checks fetchedAt and falls back to the direct feed only if this mirror goes stale, so a
dead timer degrades to exactly the old behaviour, never to a silent lie about data age.

The URLs mirror the page's own (index.html FIRES_URL/PERIMS_URL/fetchHeat). If one changes,
change both.
"""
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "pinkrobotics" / "airships" / "data" / "live"

ARC = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services"
FEEDS = {
    "fires": {
        "maxAgeMin": 8,
        "url": ARC + "/BCWS_ActiveFires_PublicView/FeatureServer/0/query"
               "?where=FIRE_STATUS%20%3C%3E%20%27Out%27"
               "&outFields=FIRE_NUMBER,FIRE_STATUS,FIRE_CAUSE,INCIDENT_NAME,"
               "GEOGRAPHIC_DESCRIPTION,CURRENT_SIZE,IGNITION_DATE,FIRE_URL,"
               "FIRE_OF_NOTE_IND,RESPONSE_TYPE_DESC"
               "&returnGeometry=true&outSR=4326&f=geojson",
    },
    "perims": {
        "maxAgeMin": 8,
        "url": ARC + "/BCWS_FirePerimeters_PublicView/FeatureServer/0/query"
               "?where=FIRE_STATUS%20%3C%3E%20%27Out%27"
               "&outFields=FIRE_NUMBER,FIRE_STATUS,FIRE_SIZE_HECTARES,TRACK_DATE"
               "&returnGeometry=true&outSR=4326&maxAllowableOffset=0.002&f=geojson",
    },
    "heat": {
        "maxAgeMin": 25,
        "url": "https://cwfis.cfs.nrcan.gc.ca/geoserver/public/wfs"
               "?service=WFS&version=2.0.0&request=GetFeature"
               "&typeNames=public%3Ahotspots_last24hrs"
               "&outputFormat=application%2Fjson&srsName=EPSG:4326"
               "&CQL_FILTER=lat%20BETWEEN%2047.5%20AND%2060.6%20AND%20lon%20BETWEEN%20-140%20AND%20-113.3"
               "&sortBy=temp%20D&count=6000&propertyName=geometry,temp",
    },
}

# Where the served copies live. Production only since 2026-08-08 (the airships page shipped
# to pinkrobotics.ca and guppi.ca went back to its placeholder — pushing there would just
# recreate stray dirs via --mkpath). Re-add the guppi dest if the page is ever staged again:
#   pink-edge:/srv/guppi-website/site/pinkrobotics/airships/data/live/
PUSH_DESTS = [
    "pink-edge:/srv/pinkrobotics-website/site/airships/data/live/",
]


def age_min(path):
    try:
        j = json.loads(path.read_text())
        dt = datetime.fromisoformat(j["fetchedAt"].replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 60
    except Exception:
        return 1e9


def fetch(name, feed):
    out = LIVE / f"{name}.json"
    a = age_min(out)
    if a < feed["maxAgeMin"]:
        print(f"{name}: fresh ({a:.0f} min), skipped")
        return False
    req = urllib.request.Request(feed["url"], headers={
        "User-Agent": "pinkrobotics.ca airships mirror (single server-side fetcher; contact tyler@pinkai.ca)",
        "Accept": "application/json",
    })
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=45) as r:
        body = json.load(r)
    n = len(body.get("features", [])) if isinstance(body, dict) else 0
    wrapped = {
        "fetchedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": feed["url"].split("?")[0],
        "data": body,
    }
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(wrapped, separators=(",", ":")))
    tmp.replace(out)                      # atomic: readers never see a half-written file
    print(f"{name}: {n} features, {time.time() - t0:.1f}s -> {out.relative_to(ROOT)}")
    return True


def main():
    LIVE.mkdir(parents=True, exist_ok=True)
    changed = False
    failures = 0
    for name, feed in FEEDS.items():
        try:
            changed = fetch(name, feed) or changed
        except Exception as e:
            failures += 1
            print(f"{name}: FAILED ({e}) — keeping the previous copy", file=sys.stderr)
    del changed  # push unconditionally: the edge copy must never lag a skipped-fresh run
    if "--push" in sys.argv:
        for dest in PUSH_DESTS:
            r = subprocess.run(
                ["rsync", "-rltz", "--mkpath", "--chmod=D755,F644", f"{LIVE}/", dest],
                capture_output=True, text=True, timeout=120)
            print(f"push {dest}: {'ok' if r.returncode == 0 else 'FAILED — ' + r.stderr.strip()[:200]}")
            if r.returncode != 0:
                failures += 1
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
