#!/usr/bin/env python3
"""Rebuild map-only BC vectors from a verified Natural Earth v5.1.2 tagged archive.

    python3 pipeline/vectors.py
    python3 pipeline/vectors.py --archive path/to/natural-earth-v5.1.2.tar.gz

The full upstream archive is large (~1.5 GB). Only the two GeoJSON members are read;
no archive member is extracted to the filesystem. A cached archive is verified too.
"""
import argparse
import hashlib
import json
import math
import tarfile
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = 'v5.1.2'
URL = 'https://codeload.github.com/nvkelso/natural-earth-vector/tar.gz/refs/tags/' + RELEASE
SHA256 = '62b2ecf311e54b76e433c680c4e47a29ecffc87b0cadd014716cbff7c6daa54b'
BOUNDS = [-137.5, 47.3, -112, 60.6]
MEMBERS = {'roads': 'geojson/ne_10m_roads.geojson',
           'outline': 'geojson/ne_50m_admin_1_states_provinces.geojson'}


def simplify(points, tolerance):
    if len(points) < 3:
        return points
    keep, stack = {0, len(points) - 1}, [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        x, y = points[a]; dx, dy = points[b][0] - x, points[b][1] - y
        denom = dx * dx + dy * dy
        far, index = tolerance * tolerance, None
        for i in range(a + 1, b):
            px, py = points[i]
            t = max(0, min(1, ((px - x) * dx + (py - y) * dy) / denom)) if denom else 0
            distance = (px - x - t * dx) ** 2 + (py - y - t * dy) ** 2
            if distance > far: far, index = distance, i
        if index is not None:
            keep.add(index); stack.extend([(a, index), (index, b)])
    return [points[i] for i in sorted(keep)]


def clip_segment(a, b, bounds=BOUNDS):
    dx, dy = b[0] - a[0], b[1] - a[1]
    lo, hi = 0, 1
    for p, q in [(-dx, a[0] - bounds[0]), (dx, bounds[2] - a[0]),
                 (-dy, a[1] - bounds[1]), (dy, bounds[3] - a[1])]:
        if p == 0:
            if q < 0: return None
        elif p < 0: lo = max(lo, q / p)
        else: hi = min(hi, q / p)
        if lo > hi: return None
    return [[a[0] + lo * dx, a[1] + lo * dy], [a[0] + hi * dx, a[1] + hi * dy]]


def clip_line(line):
    result, current = [], []
    for a, b in zip(line, line[1:]):
        segment = clip_segment(a, b)
        if segment is None:
            if len(current) > 1: result.append(current)
            current = []
        elif current and all(math.isclose(x, y, abs_tol=1e-10) for x, y in zip(current[-1], segment[0])):
            current.append(segment[1])
        else:
            if len(current) > 1: result.append(current)
            current = segment
    if len(current) > 1: result.append(current)
    return result


def rounded(points):
    out = []
    for p in points:
        q = [round(x, 3) for x in p]
        if not out or q != out[-1]: out.append(q)
    return out


def build(sources):
    roads, outline = [], []
    for feature in sources['roads']['features']:
        if feature['properties'].get('featurecla') == 'Ferry': continue
        geom = feature['geometry']
        lines = geom['coordinates'] if geom['type'] == 'MultiLineString' else [geom['coordinates']]
        for line in lines:
            for part in clip_line(line):
                points = rounded(simplify(part, 0.003))
                if len(points) >= 2: roads.append(points)
    for feature in sources['outline']['features']:
        if feature['properties'].get('name') != 'British Columbia': continue
        geom = feature['geometry']
        polygons = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
        for polygon in polygons:
            ring = rounded(simplify(polygon[0], 0.005))
            if len(ring) >= 4: outline.append(ring)
    if not roads or not outline: raise ValueError('archive did not produce BC vectors')
    return {'roads-bc': roads, 'bc-outline': outline}


def read_archive(path):
    with path.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    if digest != SHA256: raise ValueError(f'archive SHA-256 mismatch: {digest}')
    sources = {}
    with tarfile.open(path, 'r|gz') as archive:
        for member in archive:
            for key, suffix in MEMBERS.items():
                if member.name == 'natural-earth-vector-5.1.2/' + suffix:
                    sources[key] = json.load(archive.extractfile(member))
            if len(sources) == len(MEMBERS): break
    if len(sources) != len(MEMBERS): raise ValueError('required GeoJSON members missing')
    return sources


def regenerate(archive, output, retrieved):
    built = build(read_archive(archive))
    for name, geometry in built.items():
        path = output / (name + '.json')
        old = json.loads(path.read_text()) if path.exists() else []
        vertices = lambda data: sum(len(part) for part in data)
        print(f'{name}: {len(old)} -> {len(geometry)} parts; {vertices(old)} -> {vertices(geometry)} vertices; '
              f'geometry {"identical" if old == geometry else "changed"}')
        path.write_text(json.dumps(geometry, separators=(',', ':')) + '\n')
        key = 'roads' if name == 'roads-bc' else 'outline'
        prov = {
            'file': path.name, 'source': URL, 'release': RELEASE, 'archiveSha256': SHA256,
            'member': MEMBERS[key], 'publisher': 'Natural Earth',
            'licence': 'Public domain', 'licenceUrl': 'https://www.naturalearthdata.com/about/terms-of-use/',
            'attribution': 'Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.',
            'retrievedAt': retrieved, 'generator': 'pipeline/vectors.py',
            'parts': len(geometry), 'vertices': vertices(geometry),
            'notes': ('Non-ferry roads clipped to ' + str(BOUNDS) + '; Douglas-Peucker tolerance 0.003 degrees.'
                      if key == 'roads' else 'British Columbia outer rings only; holes discarded; Douglas-Peucker tolerance 0.005 degrees.')
                     + ' Coordinates rounded to 3 decimal places. Map orientation only; not a survey boundary. Model does not read these vectors.',
        }
        path.with_suffix('.prov.json').write_text(json.dumps(prov, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'data')
    parser.add_argument('--retrieved-at', help='recorded archive retrieval time; defaults to archive mtime')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        archive = args.archive or Path(tmp) / 'natural-earth-v5.1.2.tar.gz'
        if not args.archive:
            urllib.request.urlretrieve(URL, archive)
        retrieved = args.retrieved_at or datetime.fromtimestamp(archive.stat().st_mtime, timezone.utc).isoformat()
        args.output.mkdir(parents=True, exist_ok=True)
        regenerate(archive, args.output, retrieved)


if __name__ == '__main__': main()
