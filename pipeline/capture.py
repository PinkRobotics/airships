#!/usr/bin/env python3
"""The daily season capture: one dated, complete copy of BC Wildfire Service's public
current-season layers, saved raw for the day it was asked for.

Why daily: the province's public layer carries only each fire's CURRENT status, and moves
a season into its historical layer only on April 1. The live mirror (pipeline/live.py)
asks only for fires that are not out. So the day-by-day history of a season exists nowhere
unless somebody captures the whole layer every day — that is this tool's one job.

Load discipline, enforced here and not left to the caller: one run a day, nine requests on
a 2026-10-01-shaped day (see pipeline/README.md for the budget), a pause between requests,
one retry after a pause when a request fails and a full stop when it fails twice, and an
honest User-Agent.

Usage:
    python3 pipeline/capture.py --out DIR [--base URL] [--pause SECONDS]

--out is the capture root; the run writes DIR/<America/Vancouver date>/. A folder that
already holds anything is never written into — the run takes a timestamped sibling name
instead. Exit 0 when every layer's fetched count matches the layer's own count; exit 1
when it does not (the raw responses are still kept, and the manifest says complete: false),
or when a request fails twice and the run stops.

Configuration: AIRSHIPS_CONTACT, read exactly as pipeline/live.py reads it — see
pipeline/README.md.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ARC_BASE = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services"
LAYERS = {
    "incidents": "/BCWS_ActiveFires_PublicView/FeatureServer/0",
    "perimeters": "/BCWS_FirePerimeters_PublicView/FeatureServer/0",
}
PAUSE_S = 1.5          # between requests, and again before the single retry
TIMEOUT_S = 120
MAX_PAGES = 60         # a season is a few thousand fires; more pages than this is a bug
VANCOUVER = ZoneInfo("America/Vancouver")


class CaptureError(Exception):
    """A failure that stops the run: a request failed twice, a body was unusable."""


def user_agent():
    """Same construction as pipeline/live.py: the contact comes from the environment,
    and there is deliberately no default address in this file."""
    contact = os.environ.get("AIRSHIPS_CONTACT", "").strip()
    return ("airships-fleet-monitor season capture (single server-side fetcher; "
            + (f"contact {contact})" if contact
               else "set AIRSHIPS_CONTACT to add a contact address)"))


def vancouver_date(now):
    """The date a replay of this capture would show: the calendar day in BC, not UTC."""
    return now.astimezone(VANCOUVER).strftime("%Y-%m-%d")


def q(base, **params):
    return base + "/query?" + urllib.parse.urlencode(params)


def parse_body(raw, name):
    try:
        return json.loads(raw)
    except ValueError as e:
        raise CaptureError(f"{name}: the response is not JSON ({e})") from e


class Capture:
    """One run: the request sequence of the stop-gap, with the politeness rules testable.

    `sleep` is injected so the tests can assert the pauses without really sleeping.
    """

    def __init__(self, base, out_root, pause=PAUSE_S, sleep=time.sleep):
        self.base = base.rstrip("/")
        self.out_root = out_root
        self.pause = pause
        self.sleep = sleep
        self.ua = user_agent()
        self.out = None
        self.manifest = None
        self._first_request = True

    # -- politeness ---------------------------------------------------------------

    def _http_get(self, url):
        """One GET. Returns (raw body, seconds on the wire). Raises on any failure."""
        request = urllib.request.Request(url, headers={
            "User-Agent": self.ua, "Accept": "application/json"})
        t0 = time.time()
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
            raw = response.read()
        return raw, time.time() - t0

    def get(self, url):
        """Fetch one URL: pause first unless this is the run's first request, then one
        attempt, then — only if that raised — one more attempt after another pause.
        A second failure raises CaptureError; nothing here ever hammers."""
        if self._first_request:
            self._first_request = False
        else:
            self.sleep(self.pause)
        try:
            return self._http_get(url)
        except Exception as first:
            self.sleep(self.pause)
            try:
                return self._http_get(url)
            except Exception as second:
                raise CaptureError(
                    f"{url} failed twice ({first}; {second}) — stopping rather than retrying further"
                ) from second

    def save(self, name, url, raw, seconds):
        (self.out / name).write_bytes(raw)
        self.manifest["requests"].append({
            "file": name, "url": url, "bytes": len(raw),
            "seconds": round(seconds, 2), "sha256": hashlib.sha256(raw).hexdigest()})

    # -- the run ------------------------------------------------------------------

    def reserve_dir(self, local_date, now):
        """The dated folder, or a timestamped sibling if that name is taken. A folder is
        taken when it holds anything — including a run that stopped part-way and wrote
        no manifest — so no existing capture is ever written into."""
        root = self.out_root
        candidate = root / local_date
        if not (candidate.exists() and any(candidate.iterdir())):
            return candidate
        stem = now.astimezone(VANCOUVER).strftime("%Y-%m-%dT%H%M%S")
        for n in range(100):
            candidate = root / (stem if n == 0 else f"{stem}-{n}")
            if not (candidate.exists() and any(candidate.iterdir())):
                return candidate
        raise CaptureError(f"no free capture folder under {root}")

    def capture_layer(self, key, service_path):
        base = self.base + service_path

        url = base + "?f=json"
        raw, seconds = self.get(url)
        self.save(f"{key}.layer.json", url, raw, seconds)
        page_size = int(parse_body(raw, f"{key}.layer.json").get("maxRecordCount") or 1000)

        url = q(base, where="1=1", returnCountOnly="true", f="json")
        raw, seconds = self.get(url)
        self.save(f"{key}.count.json", url, raw, seconds)
        total = parse_body(raw, f"{key}.count.json").get("count")
        if not isinstance(total, int):
            raise CaptureError(f"{key}.count.json: no count in the response")

        stats = json.dumps([{"statisticType": "count", "onStatisticField": "OBJECTID",
                             "outStatisticFieldName": "n"}])
        url = q(base, where="1=1", groupByFieldsForStatistics="FIRE_STATUS",
                outStatistics=stats, f="json")
        raw, seconds = self.get(url)
        self.save(f"{key}.by-status.json", url, raw, seconds)
        body = parse_body(raw, f"{key}.by-status.json")
        by_status = {f["attributes"]["FIRE_STATUS"]: f["attributes"]["n"]
                     for f in body.get("features", [])}

        fetched, offset, pages = 0, 0, 0
        while True:
            url = q(base, where="1=1", outFields="*", returnGeometry="true", outSR="4326",
                    orderByFields="OBJECTID", resultOffset=offset,
                    resultRecordCount=page_size, f="geojson")
            raw, seconds = self.get(url)
            name = f"{key}.page-{pages:03d}.geojson"
            self.save(name, url, raw, seconds)
            body = parse_body(raw, name)
            n = len(body.get("features", []))
            fetched += n
            pages += 1
            offset += n
            more = body.get("exceededTransferLimit") \
                or (body.get("properties") or {}).get("exceededTransferLimit")
            if n == 0 or (not more and n < page_size) or fetched >= total:
                break
            if pages > MAX_PAGES:
                raise CaptureError(f"{key}: paging did not terminate within {MAX_PAGES} pages")

        self.manifest["layers"][key] = {
            "url": base, "where": "1=1", "countOnly": total, "byStatus": by_status,
            "featuresFetched": fetched, "pages": pages, "pageSize": page_size,
            "complete": fetched == total,
        }
        print(f"{key}: countOnly={total} fetched={fetched} pages={pages} byStatus={by_status}")

    def run(self):
        """Returns the process exit code: 0 complete, 1 not."""
        now = datetime.now(timezone.utc)
        local_date = vancouver_date(now)
        self.out = self.reserve_dir(local_date, now)
        self.out.mkdir(parents=True, exist_ok=True)
        self.manifest = {
            "capturedAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "localDate": local_date,
            "layers": {},
            "requests": [],
        }
        for key, service_path in LAYERS.items():
            self.capture_layer(key, service_path)
        (self.out / "MANIFEST.json").write_text(json.dumps(self.manifest, indent=1))
        incomplete = {key: layer for key, layer in self.manifest["layers"].items()
                      if not layer["complete"]}
        if not incomplete:
            print(f"COMPLETE {self.out}")
            return 0
        detail = "; ".join(f"{key}: fetched {layer['featuresFetched']} of the layer's own "
                           f"count {layer['countOnly']}" for key, layer in incomplete.items())
        print(f"INCOMPLETE {detail} — raw responses kept in {self.out}")
        return 1


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="capture.py",
        description="Capture today's whole BC Wildfire Service current-season layers, "
                    "raw, into a dated folder. One run is nine requests on a day when "
                    "incidents fit in two pages and perimeters in one.")
    parser.add_argument("--base", metavar="URL", default=ARC_BASE,
                        help="the ArcGIS REST services base URL "
                             f"(default: {ARC_BASE})")
    parser.add_argument("--out", required=True, metavar="DIR",
                        help="capture root; the run writes DIR/<Vancouver date>/ "
                             "and never overwrites a folder that holds anything")
    parser.add_argument("--pause", metavar="SECONDS", type=float, default=PAUSE_S,
                        help="pause between requests, and before the single retry "
                             f"(default: {PAUSE_S})")
    args = parser.parse_args(argv)
    if args.pause < 0:
        parser.error("--pause must be zero or more")
    return args


def main(argv=None, sleep=time.sleep):
    args = parse_args(argv)
    try:
        capture = Capture(base=args.base, out_root=Path(args.out),
                          pause=args.pause, sleep=sleep)
        return capture.run()
    except CaptureError as e:
        print(f"capture: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
