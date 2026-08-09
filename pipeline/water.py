#!/usr/bin/env python3
"""Build a compact water-source extract for the airships fleet monitor.

Downloads FWA lakes >= 10 ha (definite, GB15300000) and manmade reservoirs
(definite, GB24300000) from BC's openmaps WFS, then writes a compact JSON:

  { "generated": iso8601, "sources": [...counts...],
    "water": [[lon, lat, area_ha, kind, name, ring|null], ...] }

kind: 0 = lake, 1 = reservoir. ring: simplified outer ring [[lon,lat],...]
included only for area >= 200 ha (for map drawing); smaller bodies are drawn
as area-scaled circles. Coordinates rounded to 4 dp (~11 m).
"""
import json, math, sys, time, urllib.request, urllib.parse, datetime

BASE = "https://openmaps.gov.bc.ca/geo/pub/{layer}/ows"

def wfs(layer, cql, start, count=5000):
    q = {
        "service": "WFS", "version": "2.0.0", "request": "GetFeature",
        "typeName": f"pub:{layer}", "outputFormat": "application/json",
        "srsName": "EPSG:4326", "count": str(count), "startIndex": str(start),
        "CQL_FILTER": cql, "sortBy": "AREA_HA",
    }
    url = BASE.format(layer=layer) + "?" + urllib.parse.urlencode(q)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.load(r)
        except Exception as e:
            print(f"  retry {attempt+1} after {e}", file=sys.stderr)
            time.sleep(5)
    raise SystemExit("WFS fetch failed")

def fetch_all(layer, cql):
    feats, start = [], 0
    while True:
        d = wfs(layer, cql, start)
        got = d.get("features", [])
        feats.extend(got)
        print(f"  {layer}: +{len(got)} (total {len(feats)})", file=sys.stderr)
        if len(got) < 5000:
            return feats
        start += 5000

def outer_ring(geom):
    if geom is None: return None
    if geom["type"] == "Polygon":
        return geom["coordinates"][0]
    if geom["type"] == "MultiPolygon":
        # largest polygon's outer ring by vertex-shoelace area
        best, besta = None, -1
        for poly in geom["coordinates"]:
            r = poly[0]
            a = abs(sum(r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1] for i in range(len(r)-1)))
            if a > besta: best, besta = r, a
        return best
    return None

def centroid(ring):
    a = cx = cy = 0.0
    for i in range(len(ring)-1):
        x0,y0 = ring[i][0], ring[i][1]; x1,y1 = ring[i+1][0], ring[i+1][1]
        f = x0*y1 - x1*y0
        a += f; cx += (x0+x1)*f; cy += (y0+y1)*f
    if abs(a) < 1e-12:
        xs=[p[0] for p in ring]; ys=[p[1] for p in ring]
        return sum(xs)/len(xs), sum(ys)/len(ys)
    a *= 0.5
    return cx/(6*a), cy/(6*a)

def dp(points, tol):
    """Douglas-Peucker on lon/lat with tolerance in degrees."""
    if len(points) < 5: return points
    keep = [False]*len(points); keep[0] = keep[-1] = True
    # closed ring: endpoints coincide, so the baseline is degenerate and every
    # perpendicular distance is zero. Anchor the farthest vertex first.
    x0, y0 = points[0][:2]
    ifar = max(range(1, len(points)-1),
               key=lambda i: (points[i][0]-x0)**2 + (points[i][1]-y0)**2)
    keep[ifar] = True
    stack = [(0, ifar), (ifar, len(points)-1)]
    while stack:
        i0, i1 = stack.pop()
        x0,y0 = points[i0][:2]; x1,y1 = points[i1][:2]
        dx,dy = x1-x0, y1-y0
        norm = math.hypot(dx,dy) or 1e-12
        dmax, imax = -1.0, -1
        for i in range(i0+1, i1):
            px,py = points[i][:2]
            d = abs(dy*(px-x0)-dx*(py-y0))/norm
            if d > dmax: dmax, imax = d, i
        if dmax > tol:
            keep[imax] = True
            stack.append((i0,imax)); stack.append((imax,i1))
    return [p for p,k in zip(points,keep) if k]

def compact(feats, kind, ring_min_ha=80.0):
    rows = []
    for f in feats:
        p = f["properties"]
        area = p.get("AREA_HA")
        if area is None: continue
        ring = outer_ring(f.get("geometry"))
        if not ring: continue
        cx, cy = centroid(ring)
        name = p.get("GNIS_NAME_1") or None
        out_ring = None
        if area >= ring_min_ha:
            simp = dp(ring, 0.0025 if area < 2000 else 0.006)
            if len(simp) >= 4:
                out_ring = [[round(x,4), round(y,4)] for x,y in
                            ((pt[0],pt[1]) for pt in simp)]
        rows.append([round(cx,4), round(cy,4), round(area,1), kind, name, out_ring])
    return rows

lakes = fetch_all("WHSE_BASEMAPPING.FWA_LAKES_POLY",
                  "AREA_HA>=10 AND FEATURE_CODE='GB15300000'")
resv  = fetch_all("WHSE_BASEMAPPING.FWA_MANMADE_WATERBODIES_POLY",
                  "AREA_HA>=10 AND FEATURE_CODE='GB24300000'")

water = compact(lakes, 0) + compact(resv, 1)
water.sort(key=lambda r: -r[2])
doc = {
    "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "note": "FWA definite lakes >=10 ha and definite reservoirs >=10 ha; centroids, areas, names; simplified outer rings for bodies >=80 ha. Surface area is a proxy only.",
    "counts": {"lakes": sum(1 for w in water if w[3]==0),
               "reservoirs": sum(1 for w in water if w[3]==1)},
    "water": water,
}
out = sys.argv[1] if len(sys.argv) > 1 else "water-bc.json"
with open(out, "w") as fh:
    json.dump(doc, fh, separators=(",",":"))
print(f"wrote {out}: {len(water)} bodies, "
      f"{sum(1 for w in water if w[5])} with rings", file=sys.stderr)
