# `data/live/` — the server-side feed mirror

This directory is written on the server by `pipeline/live.py` every ten minutes. Its
contents are **not committed**, and this README is the only file in it that git tracks.

```
data/live/fires.json     BC Wildfire Service active fires
data/live/perims.json    BC Wildfire Service fire perimeters
data/live/heat.json      NRCan CWFIS 24-hour satellite hotspots
```

Each is `{"fetchedAt": "<iso8601 utc>", "source": "<upstream url>", "data": <upstream json>}`.

## Why it exists

Visitors read the fire data from our server, not from the agencies'. One fetch per interval
serves every viewer, instead of one fetch per viewer. Traffic to this page must never become
load on emergency infrastructure — if the front page of Hacker News points at a map that
proxies fifty thousand browsers straight into the BC Wildfire Service, that is our fault and
nobody else's. `pipeline/live.py` refreshes fires and perimeters only when the mirror is
older than eight minutes and hotspots only when older than 25, so upstream sees roughly six
fire requests an hour regardless of how many people are watching.

The page checks `fetchedAt`. If the mirror is stale it falls back to the upstream feed
directly, and if that fails too it falls back to the committed `data/snapshot.json`. A dead
timer degrades to the old behaviour, never to a silent lie about how old the data is.

## Why it is not committed

Because committing it would ship stale fire data over a fresh mirror on every deploy.

The failure is not hypothetical. A deploy copies the repository to the server. If
`fires.json` were tracked, the copy would overwrite a mirror that is two minutes old with
one that is however many hours or days old the last commit is — and it would do so
silently, because the file is present and parses fine. A map showing a fire that has been
out for a week, on a page whose whole argument is that the wildfire data is real, is worse
than a map showing nothing. `.gitignore` therefore excludes `data/live/*` and re-admits only
this README.

The same reasoning says this is deployment state, not source. It has a timestamp, a
lifetime measured in minutes, and no meaning outside the machine it was written on. There
is nothing here to review, diff or roll back.

## Populating it

On the server, from a timer every ten minutes:

```
python3 pipeline/live.py           # fetch into data/live/
python3 pipeline/live.py --push    # ...and rsync only that directory to the edge docroot
```

Locally, for development, the same command works and the page will pick the files up. You
do not need them: with no mirror present the page falls through to the live feeds, and with
`?data=snapshot` it ignores both and uses the committed snapshot. Deterministic runs
(`?seed=N&data=snapshot`) never touch this directory at all, which is why the golden tests
do not depend on it.

The script exits non-zero if any feed failed, so a timer that reports failures will tell
you when the mirror has gone stale. It keeps the previous copy on failure rather than
writing a partial file, and each write is an atomic rename, so a reader never sees a
half-written mirror.

## Two things to fix in `pipeline/live.py` before release

Both are stale references to the private website repository this project was extracted
from, and both are open:

1. `LIVE` is computed as `ROOT / "pinkrobotics" / "airships" / "data" / "live"`, which was
   the path inside the old repository. In this repository the mirror belongs at
   `ROOT / "data" / "live"`, i.e. this directory. As written, the script creates a
   `pinkrobotics/airships/data/live/` tree at the repository root and the page never sees
   it.
2. The docstring's usage lines still say `tools/airships_live.py`, which is the old name of
   the file.

`PUSH_DESTS` points at a specific deployment host and is expected to be edited by anyone
running their own copy.
