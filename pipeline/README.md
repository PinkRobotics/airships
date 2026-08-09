# pipeline/ — the data generators

Four standalone Python 3 scripts. None of them is needed to run the page: everything they
produce is committed under `data/`. They exist so that the committed data can be rebuilt
from its sources by anyone, rather than taken on trust.

| Script | Produces | Run it when |
|---|---|---|
| `live.py` | `data/live/*.json` (gitignored) | continuously, from a timer, if you host the page |
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
`data/live/`, and the page reads that. `app/net.js` falls back to the upstream feeds only if
the mirror is missing or stale, and to the committed `data/snapshot.json` if that also fails
— and says on the page which of the three it is showing.

Run it from a timer every ten minutes. The freshness rules are inside the script, not in the
timer, so running it more often costs upstream nothing.

## Configuration

Both settings are environment variables and both are optional. Neither has a default that
does anything to anybody else's machine.

### `AIRSHIPS_CONTACT`

A contact address or URL, sent in the `User-Agent` header of every request `live.py` makes.

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

None of these scripts is deterministic — they fetch live data from services that change.
That is exactly why the page ships `data/snapshot.json` and `data/snapshot-heat.json`, and
why `?data=snapshot` exists: the tests compare model output against pinned inputs, never
against whatever the wildfire feeds happen to say today.
