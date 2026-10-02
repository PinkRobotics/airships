# pipeline/ — the data generators

Standalone Python 3 scripts. None is needed to run the page: static inputs are committed
under `data/`, and an absent live mirror falls back to the dated snapshot. They exist so that the committed data can be rebuilt
from its sources by anyone, rather than taken on trust.

| Script | Produces | Run it when |
|---|---|---|
| `live.py` | fire, perimeter, heat and hourly wind mirrors (gitignored) | continuously, from a timer, if you host the page |
| `vectors.py` | pinned Natural Earth roads, outline and provenance sidecars | to reproduce the map vectors |
| `capture.py` | dated raw captures under a root you name | once a day during the season, from a timer |
| `water.py` | `data/water-bc.json` | the BC freshwater atlas is updated — rarely |
| `terrain.py` | `data/terrain-bc.jpg` | never, in practice; the hillshade is static |
| `figures.py` | the SVG diagrams inlined into `concept/index.html` | after editing a diagram |

`live.py` and `water.py` need only the standard library. `terrain.py` needs `numpy` and
`Pillow`. `figures.py` needs nothing beyond `argparse` and `pathlib`, and writes only
between marker comments (`<!--CYCLE-->…<!--/CYCLE-->`) on the concept page, so running it on
an unmodified checkout is a no-op you can verify with `git diff`.

`figures.py` builds four figures — `CYCLE`, `SCALE3`, `CUTAWAY`, `LADDER` — and the concept
page carries markers for only three of them. `SCALE3` has no marker, so a run prints
`SCALE3: no marker on the page — skipped` and inlines three. That is either a figure that
was dropped from the page and not from the generator, or a marker that was never added;
nobody has decided which. `python3 pipeline/figures.py --print` lists all four with their
sizes and touches nothing.

## The live mirror, and why it exists

The monitor's fire data comes from the BC Wildfire Service and from CWFIS. Both are public,
unauthenticated and free, and both sit in front of systems that matter during a fire season.

A page that fetches them directly turns every visitor into upstream load, and a page that
gets linked somewhere busy turns into a small denial-of-service attempt on an emergency
service. So `live.py` fetches once per interval on the server, writes the result under
`data/live/`, and the page reads that. The browser falls back only to the dated `data/snapshot.json` if the fire mirror is missing
or stale, and says which tier answered. Heat snapshots accompany snapshot fires; an absent
heat mirror beside live fires means no heat overlay. Wind uses a fixed 5×5 grid, with one
server request an hour (failed attempts included). Missing or stale wind means labelled
still air. Run a single mirror timer; the script locks concurrent invocations.

Run it from a timer every ten minutes. The freshness rules are inside the script, not in the
timer, so running it more often costs upstream nothing.

## The daily season capture, and why it is daily

`capture.py` saves one dated, complete copy of BC Wildfire Service's two public
current-season layers — fire incidents and fire perimeters — raw, as the service returns
them. It captures the *whole* layer, out fires included, which is exactly what `live.py`
deliberately does not do: the mirror keeps only what a visitor wants to see on the map
right now, while the capture keeps what the season actually looked like that day.

The reason it must run every day is that the province's public layer carries only each
fire's CURRENT status, and a season moves into the historical layer only on April 1. The
day-by-day history of a season — when each fire went Out, how long each was held — exists
nowhere unless someone captures the whole layer each day and keeps the copies. A capture
of 2026-10-01 answers questions no later fetch can.

Each run writes `<out>/<America-Vancouver date>/` — the date is the day a replay of that
folder would show, not UTC — holding every raw response plus a `MANIFEST.json` with each
request's URL, byte count, duration and sha256, each layer's own count, the number
fetched, and `complete`. A folder that already holds anything is never written into; the
run takes a timestamped sibling name instead. If what was fetched does not match the
layer's own count, the run says `INCOMPLETE`, keeps the raw responses, records
`complete: false`, and exits 1 — an honest capture that knows it is short, not a green
exit on a gap.

**The request budget of one run, plainly: nine requests** on 2026-10-01 (five for
incidents, four for perimeters) — three fixed requests per layer (description, count,
status tally) plus one per page at the layer's own page size of 1000 features. It grows
by one for each additional page a busy season adds, and by nothing else.

Politeness to the service is in the tool, not left to the caller: a 1.5 s pause between
requests (`--pause` to change it), one retry after a pause when a request fails, and a
full stop — exit 1, nothing further asked — when it fails twice. The User-Agent carries
`AIRSHIPS_CONTACT` exactly as `live.py` does (see below); unset, the header says how to
set it and carries no address.

```sh
python3 pipeline/capture.py --out /srv/airships-captures/bcws
#   --base URL     another ArcGIS REST services base (default: BCWS's public one)
#   --pause SECS   pause between requests (default 1.5)
```

`--out` has no default on purpose: this repository must not decide where on a stranger's
machine a season archive grows. Schedule it once a day — the exact minute does not matter,
only that each Vancouver day gets exactly one folder. As text only (nothing here is
installed by this repository):

```ini
# /etc/systemd/system/airships-season-capture.service
[Service]
Type=oneshot
Environment=AIRSHIPS_CONTACT=https://your-operators-page.example/contacts
ExecStart=/usr/bin/python3 /srv/airships/checkout/pipeline/capture.py --out /srv/airships-captures/bcws
```

```ini
# /etc/systemd/system/airships-season-capture.timer
[Timer]
OnCalendar=*-*-* 19:30:00 America/Vancouver
Persistent=true

[Install]
WantedBy=timers.target
```

`make capturecheck` runs the tool's tests against trimmed copies of the 2026-10-01
capture served from a fixture server on 127.0.0.1 — the tests never touch the service
the tool is polite about.

## Configuration

Both settings are environment variables and both are optional. Neither has a default that
does anything to anybody else's machine.

### `AIRSHIPS_CONTACT`

A contact address or URL, sent in the `User-Agent` header of every request `live.py` and
`capture.py` make.

Sending a contact when you scrape a public feed is a courtesy with a practical point: if
your fetcher misbehaves — a stuck loop, a timer that fires every second, a bug that requests
the whole province at full resolution — the people running the service can tell you, instead
of having to block an anonymous client and find out later that they broke something. It also
distinguishes a single deliberate mirror from an unidentified crawler when someone reads
their access logs.

It is not authentication. No feed used here requires it, and the script works without it.
Unset, the header says so:

```
airships-fleet-monitor mirror (single server-side fetcher; set AIRSHIPS_CONTACT to add a contact address)
```

There is deliberately no default address, because any default shipped in a public repository
is some real person's inbox receiving mail about servers they do not run.

### `AIRSHIPS_PUBLISH_DEST`

Where `live.py --push` copies `data/live/` after a successful fetch. **Unset by default,
which means nothing is pushed anywhere** — `--push` prints that it is not configured and
exits with whatever the fetch returned.

The value is a comma-separated list of `rsync` destinations. A destination is anything rsync
accepts:

```sh
# a local directory served by nginx
AIRSHIPS_PUBLISH_DEST=/var/www/airships/data/live/

# a remote host over ssh
AIRSHIPS_PUBLISH_DEST=deploy@example.org:/var/www/airships/data/live/

# two servers behind a load balancer
AIRSHIPS_PUBLISH_DEST=/srv/a/live/,deploy@b.example.org:/srv/b/live/
```

The push is `rsync -rltz --mkpath --chmod=D755,F644` of that one directory. It never touches
anything else on the target, and the script has no other write path off the machine it runs
on. Host names, credentials and directory layout are entirely the operator's business and
are not recorded anywhere in this repository.

## Determinism

`vectors.py` is deterministic for its checksum-pinned archive and recorded retrieval time.
The live feed scripts read services that change.
That is exactly why the page ships `data/snapshot.json` and `data/snapshot-heat.json`, and
why `?data=snapshot` exists: the tests compare model output against pinned inputs, never
against whatever the wildfire feeds happen to say today.
