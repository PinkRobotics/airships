#!/usr/bin/env python3
"""Build a fire-history extract for the water-availability question.

    python3 pipeline/firehistory.py data/fire-history-bc.json

OPEN-QUESTIONS #13 asks about operational water availability. This extract preserves dated
points and outlines for geographic distance studies. The water study reports mapped shore
proximity and generated station distances; the monitor qualifies and plans at generated
stations. Neither establishes depth, permission, sustainable draw or water availability for
a real operation.

Downloads BC's historical fire perimeters (PROT_HISTORICAL_FIRE_POLYS_SP) for fires of
10 hectares or more since 2006, and writes a compact JSON:

  { "generated": iso8601, "counts": {...},
    "fires": [[lon, lat, size_ha, year, n_verts, ring|null], ...] }

lon/lat is the SHOELACE CENTROID of the largest ring, not a bounding-box centre: a fire
that burns up a valley has a centroid on the valley floor and a bbox centre on a ridge.
The ring is kept, simplified, for fires of 1,000 ha or more, because a 40,000 ha fire is
not a point and the distance from its far edge to water is a different number from the
distance from its middle. Coordinates rounded to 4 dp (~11 m).

Why 10 ha: BCWS records thousands of quarter-hectare lightning starts a year that are out
before anything flies. The question is about fires that get an aviation response.

Why 2006: the perimeter record is thin before it. 1996-2005 adds 574 fires and a
documented change in how perimeters were captured (GPS track vs. sketch), so the older
decade is fetched separately by anyone who wants it rather than silently blended in.
"""
import datetime
import json
import math
import sys
import time
import urllib.parse
import urllib.request

LAYER = "WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP"
BASE = f"https://openmaps.gov.bc.ca/geo/pub/{LAYER}/ows"
CQL = "FIRE_YEAR>=2006 AND FIRE_SIZE_HECTARES>=10"
PAGE = 1000
RING_MIN_HA = 1000.0


def wfs(start, count=PAGE):
    q = {
        "service": "WFS", "version": "2.0.0", "request": "GetFeature",
        "typeName": f"pub:{LAYER}", "outputFormat": "application/json",
        "srsName": "EPSG:4326", "count": str(count), "startIndex": str(start),
        "CQL_FILTER": CQL, "sortBy": "FIRE_NUMBER",
        # ~110 m at this latitude. The question is "is there a lake within 25 km", and no
        # answer to it turns on 100 m of perimeter detail.
        "maxAllowableOffset": "0.001",
        "propertyName": "FIRE_NUMBER,FIRE_YEAR,FIRE_SIZE_HECTARES,SHAPE",
    }
    url = BASE + "?" + urllib.parse.urlencode(q)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.load(r)
        except Exception as e:                                    # noqa: BLE001
            print(f"  retry {attempt + 1} after {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise SystemExit("WFS fetch failed")


def rings(geom):
    """Every outer ring in the feature, largest first by |shoelace|."""
    if geom is None:
        return []
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon":
        rs = [c[0]]
    elif t == "MultiPolygon":
        rs = [p[0] for p in c if p]
    else:
        return []
    rs = [r for r in rs if r and len(r) >= 4]
    rs.sort(key=lambda r: -abs(shoelace(r)[0]))
    return rs


def shoelace(ring):
    """Signed area (deg^2) and centroid of a ring, in lon/lat."""
    a = cx = cy = 0.0
    for i in range(len(ring) - 1):
        x0, y0 = ring[i][0], ring[i][1]
        x1, y1 = ring[i + 1][0], ring[i + 1][1]
        f = x0 * y1 - x1 * y0
        a += f
        cx += (x0 + x1) * f
        cy += (y0 + y1) * f
    if a == 0:
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        return 0.0, (sum(xs) / len(xs), sum(ys) / len(ys))
    return a / 2.0, (cx / (3.0 * a), cy / (3.0 * a))


def simplify(ring, tol):
    """Douglas-Peucker, iterative, on lon/lat degrees."""
    if len(ring) <= 4:
        return ring
    keep = [False] * len(ring)
    keep[0] = keep[-1] = True
    stack = [(0, len(ring) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        x0, y0 = ring[i]
        x1, y1 = ring[j]
        dx, dy = x1 - x0, y1 - y0
        den = math.hypot(dx, dy)
        best, bi = -1.0, -1
        for k in range(i + 1, j):
            x, y = ring[k]
            d = (abs(dy * x - dx * y + x1 * y0 - y1 * x0) / den if den
                 else math.hypot(x - x0, y - y0))
            if d > best:
                best, bi = d, k
        if best > tol:
            keep[bi] = True
            stack.append((i, bi))
            stack.append((bi, j))
    return [p for p, k in zip(ring, keep) if k]


def main(out):
    feats, start = [], 0
    while True:
        d = wfs(start)
        got = d.get("features", [])
        feats.extend(got)
        print(f"  +{len(got)} (total {len(feats)})", file=sys.stderr)
        if len(got) < PAGE:
            break
        start += PAGE

    fires, skipped, years = [], 0, {}
    for f in feats:
        p = f.get("properties") or {}
        ha = p.get("FIRE_SIZE_HECTARES")
        rs = rings(f.get("geometry"))
        if ha is None or not rs:
            skipped += 1
            continue
        _, (lon, lat) = shoelace(rs[0])
        ring = None
        if float(ha) >= RING_MIN_HA:
            r = simplify([[round(x, 4), round(y, 4)] for x, y in rs[0]], 0.002)
            ring = r if len(r) >= 4 else None
        yr = int(p.get("FIRE_YEAR") or 0)
        years[yr] = years.get(yr, 0) + 1
        fires.append([round(lon, 4), round(lat, 4), round(float(ha), 1), yr,
                      len(rs[0]), ring])

    fires.sort(key=lambda r: (-r[2], r[3]))
    doc = {
        "generated": datetime.datetime.now(datetime.timezone.utc)
                             .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "note": ("BC historical fire perimeters >= 10 ha, 2006 onward. Each entry is "
                 "[lon, lat, size_ha, year, source_vertices, ring|null]; lon/lat is the "
                 "shoelace centroid of the largest ring. Rings kept for >= 1,000 ha."),
        "filter": CQL,
        "counts": {
            "fires": len(fires),
            "withRing": sum(1 for f in fires if f[5]),
            "skippedNoGeometry": skipped,
            "years": dict(sorted(years.items())),
            "totalHa": round(sum(f[2] for f in fires), 1),
        },
        "fires": fires,
    }
    with open(out, "w") as fh:
        json.dump(doc, fh, separators=(",", ":"))
    print(f"{out}: {len(fires)} fires, {doc['counts']['totalHa']:,.0f} ha", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/fire-history-bc.json")
