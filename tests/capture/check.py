#!/usr/bin/env python3
"""The season-capture gate: pipeline/capture.py against the trimmed capture fixtures.

The capture tool's whole point is politeness to an emergency-information service, so the
tests never leave this machine: every run points --base at a fixture server this file
starts on 127.0.0.1, which serves the trimmed copies in fixtures/ of the raw responses
the stop-gap captured (the fire layers on 2026-10-01, the evacuation layer on
2026-10-02). The one thing that cannot be faked locally — that the tool really would hit
the agency — is exactly the thing these tests must not do.

Covered, one test per behaviour the tool promises:

    pause between requests (default 1.5 s, asserted on an injected sleep — no real sleep)
    the folder is named for the America/Vancouver date, and never overwrites a capture
    exit 1, said plainly, when the fetched count misses the layer's own count
    one transient failure is retried once after a pause; a second failure stops the run
    the User-Agent carries AIRSHIPS_CONTACT, read as pipeline/live.py reads it
    the file set and manifest keys match the stop-gap's capture folders
    the evacuation layer: three requests (no status field, so no by-status request),
    its manifest entry carrying no byStatus, and a capture that is complete only when
    all three layers are

Run from anywhere: make capturecheck, or python3 tests/capture/check.py directly.
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
FIXTURES = HERE / "fixtures"
sys.path.insert(0, str(REPO / "pipeline"))
import capture  # noqa: E402  (path set up just above)
sys.path.insert(0, str(REPO / "tools"))
from serve import serve_tree

# The stop-gap's folders held exactly these files (fire layers 2026-10-01, evacuation
# layer 2026-10-02); the fixture set mirrors them, so a passing "file set" assertion here
# is the comparison against the real captures.
STOPGAP_FILE_SET = {
    "MANIFEST.json",
    "incidents.layer.json", "incidents.count.json", "incidents.by-status.json",
    "incidents.page-000.geojson", "incidents.page-001.geojson",
    "perimeters.layer.json", "perimeters.count.json", "perimeters.by-status.json",
    "perimeters.page-000.geojson",
    "evacuations.layer.json", "evacuations.count.json", "evacuations.page-000.geojson",
}
MANIFEST_KEYS = {"capturedAt", "localDate", "layers", "requests"}
LAYER_KEYS = {"url", "where", "countOnly", "byStatus", "featuresFetched",
              "pages", "pageSize", "complete"}
# the evacuation layer has no status field, so its manifest entry names no tally
EVAC_LAYER_KEYS = LAYER_KEYS - {"byStatus"}
REQUEST_KEYS = {"file", "url", "bytes", "seconds", "sha256"}
DATE_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_DIR_RETRY = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{6}(-\d+)?$")
CAPTURED_AT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

# incidents pages at the fixture's page size of 3: offsets 0 and 3; anything else is past
# the end of the layer and gets an empty page, as the real service returns one.
EMPTY_PAGE = b'{"type":"FeatureCollection","features":[]}'
INCIDENT_PAGES = {"0": "incidents.page-000.geojson", "3": "incidents.page-001.geojson"}
PERIMETER_PAGES = {"0": "perimeters.page-000.geojson"}
# the evacuation layer's real maxRecordCount is 1000 and the day held 16 features: one page
EVAC_PAGES = {"0": "evacuations.page-000.geojson"}


class Fixtures:
    """What the local stand-in for the ArcGIS service serves, plus what it saw.

    `fail` maps a route (see route()) to a number of 500s to return first, so a test can
    inject exactly one transient failure, or a permanent one. `count_override` rewrites a
    layer's count response — how the incomplete-capture case is staged without a second
    copy of every fixture.
    """

    def __init__(self, fail=None, count_override=None):
        self.fail = dict(fail or {})
        self.count_override = dict(count_override or {})
        self.hits = []          # one {path, query, ua} per request received

    def route(self, path, query):
        """Name a request the way `fail` keys them: '<layer>/<kind>'."""
        layer = ("incidents" if "BCWS_ActiveFires" in path else
                 "perimeters" if "BCWS_FirePerimeters" in path else
                 "evacuations" if "Evacuation_Orders_and_Alerts" in path else path)
        if not path.endswith("/query"):
            return f"{layer}/layer"
        if "returnCountOnly" in query:
            return f"{layer}/count"
        if "groupByFieldsForStatistics" in query:
            return f"{layer}/stats"
        return f"{layer}/page-{query.get('resultOffset', ['?'])[0]}"

    def body(self, route, query):
        layer, _, kind = route.partition("/")
        if kind == "layer":
            return (FIXTURES / f"{layer}.layer.json").read_bytes()
        if kind == "count":
            count = self.count_override.get(layer)
            return json.dumps({"count": count}).encode() if count is not None \
                else (FIXTURES / f"{layer}.count.json").read_bytes()
        if kind == "stats":
            return (FIXTURES / f"{layer}.by-status.json").read_bytes()
        pages = {"incidents": INCIDENT_PAGES, "perimeters": PERIMETER_PAGES,
                 "evacuations": EVAC_PAGES}[layer]
        name = pages.get(kind.removeprefix("page-"))
        return (FIXTURES / name).read_bytes() if name else EMPTY_PAGE

    def hits_on(self, route):
        return sum(1 for h in self.hits if h["route"] == route)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        f = self.fixtures      # set by start_server, shared with the test
        url = urlparse(self.path)
        query = parse_qs(url.query)
        route = f.route(url.path, query)
        f.hits.append({"path": url.path, "query": url.query,
                       "ua": self.headers.get("User-Agent", ""), "route": route})
        if f.fail.get(route, 0) > 0:
            f.fail[route] -= 1
            self.send_error(500, "injected transient failure")
            return
        body = f.body(route, query)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):      # keep unittest's output readable
        pass


def start_server(fixtures):
    class FixtureHandler(Handler):
        pass
    FixtureHandler.fixtures = fixtures
    return serve_tree(handler=FixtureHandler)


class Recorder:
    """The injected sleep: remembers every pause instead of taking it."""

    def __init__(self):
        self.calls = []

    def __call__(self, seconds):
        self.calls.append(seconds)


class CaptureToolTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = Fixtures()
        serving = start_server(self.fixtures)
        self.base = serving.__enter__().rstrip('/')
        self.addCleanup(serving.__exit__, None, None, None)
        self.root = Path(tempfile.mkdtemp(prefix="capture-check-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self._contact = os.environ.get("AIRSHIPS_CONTACT")
        self.addCleanup(self._restore_contact)

    def _restore_contact(self):
        if self._contact is None:
            os.environ.pop("AIRSHIPS_CONTACT", None)
        else:
            os.environ["AIRSHIPS_CONTACT"] = self._contact

    def run_tool(self, pause="0", sleep=time.sleep, args=()):
        """Run the tool in-process against the fixture server. Returns (code, stdout,
        stderr, sleep recorder). `pause="default"` leaves --pause off so the CLI default
        applies; an injected Recorder never really sleeps."""
        recorder = sleep if isinstance(sleep, Recorder) else None
        argv = ["--base", self.base, "--out", str(self.root)]
        if pause != "default":
            argv += ["--pause", pause]
        argv += list(args)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = capture.main(argv, sleep=sleep)
        return code, out.getvalue(), err.getvalue(), recorder

    def dated_dirs(self):
        return sorted(d for d in self.root.iterdir() if d.is_dir())

    @staticmethod
    def snapshot(directory):
        return {p.name: p.read_bytes() for p in sorted(directory.iterdir())}

    # -- the five behaviours, plus the format ---------------------------------------

    def test_01_complete_two_page_capture(self):
        """A complete run: 12 requests (three fixed per fire layer plus one per page, and
        three for the evacuation layer — definition, count, its one page, and no
        by-status request, because that layer has no status field to tally), the
        stop-gap's file set, the stop-gap's manifest keys, every URL on the fixture
        base, hashes that match the files on disk."""
        code, out, _, recorder = self.run_tool(sleep=Recorder())
        self.assertEqual(code, 0, out)
        self.assertIn("COMPLETE", out)

        dirs = self.dated_dirs()
        self.assertEqual(len(dirs), 1, "one dated folder under the root")
        day = dirs[0]
        self.assertRegex(day.name, DATE_DIR)
        self.assertEqual(sorted(self.snapshot(day)), sorted(STOPGAP_FILE_SET))

        manifest = json.loads((day / "MANIFEST.json").read_text())
        self.assertEqual(set(manifest), MANIFEST_KEYS)
        self.assertRegex(manifest["capturedAt"], CAPTURED_AT)
        self.assertEqual(manifest["localDate"], day.name,
                         "the folder is named for the Vancouver date, and only for it")
        self.assertEqual(set(manifest["layers"]), {"incidents", "perimeters", "evacuations"})
        self.assertEqual(len(manifest["requests"]), 12)
        for request in manifest["requests"]:
            self.assertEqual(set(request), REQUEST_KEYS)
            self.assertTrue(request["url"].startswith(self.base),
                            f"every request went to the fixture server: {request['url']}")
            raw = (day / request["file"]).read_bytes()
            self.assertEqual(request["bytes"], len(raw))
            self.assertEqual(request["sha256"], hashlib.sha256(raw).hexdigest())
        inc, per = manifest["layers"]["incidents"], manifest["layers"]["perimeters"]
        self.assertEqual(set(inc), LAYER_KEYS)
        self.assertEqual((inc["countOnly"], inc["featuresFetched"], inc["pages"],
                          inc["pageSize"], inc["complete"]), (5, 5, 2, 3, True))
        self.assertEqual(inc["byStatus"], {"Being Held": 1, "Out": 2,
                                           "Out of Control": 1, "Under Control": 1})
        self.assertEqual((per["countOnly"], per["featuresFetched"], per["pages"],
                          per["pageSize"], per["complete"]), (3, 3, 1, 1000, True))
        self.assertEqual(per["byStatus"], {"Being Held": 1, "Out": 1, "Under Control": 1})
        eva = manifest["layers"]["evacuations"]
        self.assertEqual(set(eva), EVAC_LAYER_KEYS, "no byStatus: nothing to tally")
        self.assertEqual((eva["countOnly"], eva["featuresFetched"], eva["pages"],
                          eva["pageSize"], eva["complete"]), (16, 16, 1, 1000, True))
        self.assertEqual(self.fixtures.hits_on("incidents/page-0"), 1)
        self.assertEqual(self.fixtures.hits_on("incidents/page-3"), 1)
        self.assertEqual(self.fixtures.hits_on("evacuations/page-0"), 1)
        self.assertEqual(self.fixtures.hits_on("evacuations/stats"), 0,
                         "the evacuation layer was never asked for a by-status tally")
        self.assertEqual(len(self.fixtures.hits), 12,
                         "the whole run was twelve requests, as the budget says")
        self.assertEqual(len(recorder.calls), 11,
                         "eleven pauses between twelve requests, none before the first")
        self.assertEqual(set(recorder.calls), {0},
                         "--pause 0 was honoured, so the test really did not sleep")

    def test_02_incomplete_capture_exits_1_and_says_so(self):
        """The layer's own count says 6, the pages hold 5: exit 1, the mismatch said in
        plain words, the manifest honest, and the other layers still captured."""
        self.fixtures.count_override = {"incidents": 6}
        code, out, _, _ = self.run_tool()
        self.assertEqual(code, 1)
        self.assertIn("INCOMPLETE", out)
        self.assertIn("fetched 5", out)
        self.assertIn("count 6", out)
        manifest = json.loads((self.dated_dirs()[0] / "MANIFEST.json").read_text())
        self.assertFalse(manifest["layers"]["incidents"]["complete"])
        self.assertTrue(manifest["layers"]["perimeters"]["complete"])
        self.assertTrue(manifest["layers"]["evacuations"]["complete"])

    def test_02b_a_capture_is_complete_only_with_the_evacuation_layer(self):
        """Both fire layers fetched all they counted and the evacuation layer did not:
        exit 1 anyway, the evacuation layer named in the mismatch, fire layers complete,
        and the raw evacuation responses still kept. A capture is complete only when
        every layer is."""
        self.fixtures.count_override = {"evacuations": 17}
        code, out, _, _ = self.run_tool()
        self.assertEqual(code, 1)
        self.assertIn("INCOMPLETE", out)
        self.assertIn("evacuations: fetched 16", out)
        self.assertIn("count 17", out)
        manifest = json.loads((self.dated_dirs()[0] / "MANIFEST.json").read_text())
        eva = manifest["layers"]["evacuations"]
        self.assertEqual((eva["countOnly"], eva["featuresFetched"], eva["complete"]),
                         (17, 16, False))
        self.assertTrue(manifest["layers"]["incidents"]["complete"])
        self.assertTrue(manifest["layers"]["perimeters"]["complete"])
        kept = self.snapshot(self.dated_dirs()[0])
        self.assertIn("evacuations.page-000.geojson", kept,
                      "the incomplete layer's raw responses are still kept")

    def test_03_never_overwrites_an_existing_capture(self):
        """Two runs, one root: the second takes a timestamped sibling name, and every
        byte of the first capture is unchanged after it."""
        first, out, _, _ = self.run_tool()
        self.assertEqual(first, 0, out)
        day_one = self.dated_dirs()[0]
        before = self.snapshot(day_one)

        second, out, _, _ = self.run_tool()
        self.assertEqual(second, 0, out)
        dirs = self.dated_dirs()
        self.assertEqual(len(dirs), 2)
        day_one, day_two = dirs
        self.assertRegex(day_one.name, DATE_DIR)
        self.assertRegex(day_two.name, DATE_DIR_RETRY)
        self.assertTrue(day_two.name.startswith(day_one.name))
        self.assertEqual(self.snapshot(day_one), before, "the first capture is untouched")
        self.assertEqual(sorted(self.snapshot(day_two)), sorted(STOPGAP_FILE_SET))

    def test_04_one_transient_failure_retried_once_after_a_pause(self):
        """The layer description 500s once: one retry after a full pause, the run then
        completes, and that URL was hit exactly twice — never a tight loop."""
        self.fixtures.fail = {"incidents/layer": 1}
        code, out, _, recorder = self.run_tool(pause="default", sleep=Recorder())
        self.assertEqual(code, 0, out)
        self.assertEqual(self.fixtures.hits_on("incidents/layer"), 2,
                         "one attempt, one retry, and no more")
        self.assertEqual(len(self.fixtures.hits), 13,
                         "the failed attempt plus the twelve of a clean run, and no more")
        self.assertEqual(len(recorder.calls), 12,
                         "11 between-request pauses + 1 before the retry")
        self.assertEqual(set(recorder.calls), {1.5}, "every pause is the full default")

    def test_05_second_failure_stops_the_run_exit_1(self):
        """The layer description always 500s: two attempts, then the run stops — no
        third try, no other layer asked, nothing written, exit 1."""
        self.fixtures.fail = {"incidents/layer": 99}
        code, _, err, _ = self.run_tool()
        self.assertEqual(code, 1)
        self.assertIn("failed twice", err)
        self.assertEqual(self.fixtures.hits_on("incidents/layer"), 2,
                         "two attempts only: no hammering")
        self.assertEqual(len(self.fixtures.hits), 2, "the run stopped, not just the layer")
        self.assertEqual(list(self.dated_dirs()[0].iterdir()), [],
                         "a stopped run writes nothing")

    def test_06_pause_default_honoured_between_every_request(self):
        """The default pause is 1.5 s and sits between every request but the first; the
        injected sleep proves it without the test ever really sleeping."""
        code, out, _, recorder = self.run_tool(pause="default", sleep=Recorder())
        self.assertEqual(code, 0, out)
        self.assertEqual(len(recorder.calls), 11)
        self.assertEqual(set(recorder.calls), {1.5})

    def test_07_user_agent_carries_the_contact_from_the_environment(self):
        """AIRSHIPS_CONTACT set: every request's User-Agent ends with it. Unset: the
        header says how to set it and carries no address at all."""
        os.environ["AIRSHIPS_CONTACT"] = "https://example.invalid/airships"
        code, out, _, _ = self.run_tool()
        self.assertEqual(code, 0, out)
        expected = ("airships-fleet-monitor season capture (single server-side fetcher; "
                    "contact https://example.invalid/airships)")
        self.assertTrue(self.fixtures.hits)
        for hit in self.fixtures.hits:
            self.assertEqual(hit["ua"], expected)

        os.environ.pop("AIRSHIPS_CONTACT")
        self.fixtures.hits.clear()
        code, out, _, _ = self.run_tool()
        self.assertEqual(code, 0, out)
        for hit in self.fixtures.hits:
            self.assertIn("set AIRSHIPS_CONTACT", hit["ua"])
            self.assertNotIn("@", hit["ua"])
            self.assertNotIn("example.invalid", hit["ua"])

    def test_08_vancouver_date_uses_the_real_day_from_the_capture(self):
        """The date is the BC calendar day, not UTC — pinned with the actual pair from
        the 2026-10-01 capture: 02:01 UTC on the 2nd was 19:01 on the 1st in BC."""
        from datetime import datetime, timezone
        utc = timezone.utc
        self.assertEqual(capture.vancouver_date(datetime(2026, 10, 2, 2, 1, tzinfo=utc)),
                         "2026-10-01")
        self.assertEqual(capture.vancouver_date(datetime(2026, 10, 1, 6, 59, tzinfo=utc)),
                         "2026-09-30")   # 23:59 the previous evening, Pacific Daylight Time

    def test_09_cli_subprocess_exit_codes(self):
        """The shebang path end to end: python3 pipeline/capture.py, real process, real
        argv — exit 0 complete, exit 1 when the count cannot be met."""
        run = subprocess.run(
            [sys.executable, "pipeline/capture.py",
             "--base", self.base, "--out", str(self.root), "--pause", "0"],
            capture_output=True, text=True, cwd=REPO)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("COMPLETE", run.stdout)

        fresh = Path(tempfile.mkdtemp(prefix="capture-check-"))
        self.addCleanup(shutil.rmtree, fresh, ignore_errors=True)
        self.fixtures.count_override = {"perimeters": 4}
        run = subprocess.run(
            [sys.executable, "pipeline/capture.py",
             "--base", self.base, "--out", str(fresh), "--pause", "0"],
            capture_output=True, text=True, cwd=REPO)
        self.assertEqual(run.returncode, 1)
        self.assertIn("INCOMPLETE", run.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
