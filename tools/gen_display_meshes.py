#!/usr/bin/env python3
"""The 51 printed joints as browser meshes — the real parts, not stand-ins.

    python3 tools/gen_display_meshes.py            # write cell/nodemeshes.generated.js
    python3 tools/gen_display_meshes.py --check    # exit 1 if the module has gone stale
    python3 tools/gen_display_meshes.py --deep     # re-extract and compare (slow, manual)

WHY THIS EXISTS. The explorer drew every joint as a sphere plus twelve socket cones, and
three separate "bugs" the designer found by eye — a hub resized four times, a rim drawn
with no receivers, interference inside the sockets — were all artifacts of the stand-ins,
not of the article. The fix is to draw the joints the SDF actually grows. This module is
those joints, grown by the same rule (`gen_nodes.node_sdf`), grouped exactly the way
`cell/nodes.generated.js` publishes their numbers.

TWO FIELDS, DELIBERATELY, and the difference is measured rather than assumed:

  display field (all 51, DISPLAY_RES)    node_sdf(display=True): the additive half — per-SKU
      spigots, collars, cups, core blend, flat mating lands, tree-stub vs closing-pilot
      engagement per arm. NO seating slots, bores or ribs: those are 0.25-1.3 mm against
      this grid's 2.1 mm cell, and a coarse grid does not show them smaller, it shows
      them ALIASED — extracting the FULL field at res 40 loses a third of every rim
      vertex's volume to grid luck (measured 2026-08-11: median 23% volume error over the
      51 joints, monotone in nothing). The display field at res 48 converges to 3.8%
      median against itself at res 112, and every residual is uniform spigot thinning,
      not a feature.

  print field (the 5 family representatives, res 112)    node_sdf as printed — slots,
      bores, ribs, everything — at the same resolution the shipped STLs are cut at. The
      connector tour frames one joint at a time, and the joint it frames is the family's
      own representative, so the mesh under the camera is the printed part, open sockets
      and all. Fifty-one of these would be ~1.3M triangles; five is the tour's whole
      vocabulary.

WHAT THIS MODULE IS NOT: a fit authority. No mesh at any of these resolutions can show a
0.15 mm clearance — the A6 blocker records that even the print STL cannot certify its own
capture — so fit and interference remain check_assembly's, measured analytically on the
field itself. A figure quoted on the page still comes from the manifest, never from a
display mesh.

FRESHNESS. --check hashes the two source files this geometry is a pure function of
(gen_nodes.py and this file) plus the manifest's own parameters, and compares against the
hash stored in the module. It re-runs no SDF, so it is deterministic across machines and
costs milliseconds; regeneration is ~15 s. Editing either source file without regenerating
goes red, which is the point — this repository has twice shipped a gate that lied by
comparing a stale file. --deep re-extracts everything and compares with tolerances, for a
nightly or a suspicious mind.

ONE COPIED CONSTANT, GUARDED. `slot_margin` is the one generator default the manifest's
paramsMm does not carry. It is copied here and then PROVEN: the slot bases recomputed with
it must equal the manifest's slotBaseMm on all 51 nodes, which fails loudly on any drift
in it or in any other parameter.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from gen_nodes import (article_graph, spanning_tree, face_planes, slot_base,  # noqa: E402
                       bore_start, node_sdf, surface_nets, mesh_health, mesh_volume)
from gen_node_families import ORDER, payload  # noqa: E402

MANIFEST = ROOT / "research" / "geometry" / "nodes" / "manifest.json"
OUT = ROOT / "cell" / "nodemeshes.generated.js"

DISPLAY_RES = 64       # 292k triangles over 51 joints. 48 read as melted up close — the
                       # designer inspects joints at 10-15 px/mm, and the blend's creases
                       # need cells finer than 2 mm to read as made rather than grown.
REP_RES = 112          # the resolution the shipped print STLs are cut at
QUANT_MM = 0.05        # vertex grid; a third of the fit clearance, far under any cell here
SLOT_MARGIN = 0.5      # gen_nodes --slot-margin default; proven against slotBaseMm below

HEADER = """\
/* GENERATED — do not edit. `python3 tools/gen_display_meshes.py` rewrites this file.
 *
 * The article's 51 printed joints as meshes, grown from the same SDF the print STLs come
 * off (`gen_nodes.node_sdf`), in the ARTICLE frame, welded, quantized to 0.05 mm.
 * `nodes` is every joint as a display field (no slots/bores/ribs — see the generator's
 * docstring for the measurement behind that); `reps` is the five family representatives
 * at print resolution with everything in. Vertices decode as q * quantStepMm +
 * quantOriginMm, in millimetres about the joint's own centre; indices are uint16
 * triangles. tools/gen_display_meshes.py --check holds this file to its sources.
 */
"""


def source_hash() -> str:
    h = hashlib.sha256()
    h.update((ROOT / "tools" / "gen_nodes.py").read_bytes())
    h.update(pathlib.Path(__file__).read_bytes())
    man = json.loads(MANIFEST.read_text())
    h.update(json.dumps(man["paramsMm"], sort_keys=True).encode())
    h.update(f"slot_margin={SLOT_MARGIN};res={DISPLAY_RES}/{REP_RES};q={QUANT_MM}".encode())
    return h.hexdigest()[:16]


def article():
    """The graph, the per-node bases, and the per-arm engagements — main()'s own derivation,
    proven against the manifest rather than trusted."""
    man = json.loads(MANIFEST.read_text())
    prm = dict(man["paramsMm"])
    prm["slot_margin"] = SLOT_MARGIN
    nodes, members, _ = article_graph()
    tree, _ = spanning_tree(nodes, members)
    incident = {u: [] for u, _ in nodes}
    for k, (a, b, _fam) in enumerate(members):
        d = np.array(b, float) - np.array(a, float)
        d /= np.linalg.norm(d)
        incident[a].append((d, k))
        incident[b].append((-d, k))
    kinds_of = {u: [members[k][2] for _, k in incident[u]] for u, _ in nodes}
    base_of = {u: slot_base([d for d, _ in incident[u]], prm, kinds_of[u])[0]
               for u, _ in nodes}
    for i, (u, role) in enumerate(nodes):
        want = man["nodes"][i]["slotBaseMm"]
        if abs(round(base_of[u], 2) - want) > 0.005:
            sys.exit(f"gen_display_meshes: recomputed slot base {base_of[u]:.2f} != "
                     f"manifest {want} on {man['nodes'][i]['file']} — a generator "
                     "parameter (slot_margin?) has drifted from the shipped meshes.")
    ext = max(max(base_of.values()) + prm["stub"] + prm["blend"] + 6.0,
              prm["pad_r"] + 4.0, 22.0 + prm["stub"])
    return man, prm, nodes, tree, incident, kinds_of, base_of, ext


def snap_lands(v, lands, h):
    """Vertices near a mating land go exactly onto it; near two lands, onto their edge.

    The single-plane snap alone leaves a visible staircase along the edge where two lands
    meet — vertices alternately caught and missed by each plane's band. The land planes
    all pass through the node's own centre, so the edge is the line orthogonal to both
    normals, and projecting out both components (the second Gram-Schmidt-orthogonalised
    against the first) puts a vertex exactly on it. A rim vertex's three lands meet at the
    cell's corner; a vertex near all three lands is handled by the pairs in sequence and
    ends where it should — at the corner itself.
    """
    if not lands:
        return v
    near = [np.abs(v @ n) < h * 0.85 for n in lands]
    for n, m in zip(lands, near):
        d = v @ n
        v[m] -= np.outer(d[m], n)
    for i in range(len(lands)):
        for j in range(i + 1, len(lands)):
            m = near[i] & near[j]
            if not m.any():
                continue
            n1 = lands[i]
            n2 = lands[j] - float(lands[j] @ n1) * n1
            n2 /= np.linalg.norm(n2)
            v[m] -= np.outer(v[m] @ n1, n1)
            v[m] -= np.outer(v[m] @ n2, n2)
    return v


def project(v, sdf, h):
    """Newton-project every vertex onto the field's own zero surface.

    Surface nets places a vertex at the MEAN of its cell's edge crossings — inside the
    cell, not on the surface — and at display resolution that error is what the eye reads:
    lumps on every cylinder, stair-steps along every crease, a printed part that looks
    grown rather than made. The field is cheap to evaluate at points, so three Newton
    steps along its gradient put each vertex where the surface actually is. Triangle count
    and payload do not move; only the lie about where the vertices sit does. The step is
    clamped to half a cell so a vertex beside a thin feature cannot tunnel through it.
    """
    for _ in range(3):
        f = sdf(v)
        eps = 0.35
        g = np.stack([sdf(v + np.array([[eps, 0, 0]])) - sdf(v - np.array([[eps, 0, 0]])),
                      sdf(v + np.array([[0, eps, 0]])) - sdf(v - np.array([[0, eps, 0]])),
                      sdf(v + np.array([[0, 0, eps]])) - sdf(v - np.array([[0, 0, eps]]))],
                     axis=1) / (2.0 * eps)
        step = f / np.maximum((g * g).sum(axis=1), 1e-9)
        np.clip(step, -h / 2.0, h / 2.0, out=step)
        v = v - g * step[:, None]
    return v


def extract(res, ext, prm, nodes, tree, incident, kinds_of, base_of, which, display):
    """Mesh the given node indices at `res`, article frame. Returns [(v, t, vol), ...]."""
    axis = np.linspace(-ext, ext, res)
    h = axis[1] - axis[0]
    gx, gy, gz = np.meshgrid(axis, axis, axis, indexing="ij")
    P = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1)
    out = []
    for i in which:
        u, role = nodes[i]
        dirs = [d for d, _ in incident[u]]
        kinds = kinds_of[u]
        lands = face_planes(u)
        stubs = [prm["stub"] if k in tree else prm["pilot"] for _, k in incident[u]]
        bores = [bore_start(d, lands, prm, kd) for d, kd in zip(dirs, kinds)]
        sdf = lambda pts: node_sdf(pts, dirs, lands, prm, role == "hexHub",  # noqa: E731
                                   base_of[u], stubs, bores, kinds, display=display)
        F3 = sdf(P).reshape([res] * 3)
        v, t = surface_nets(F3, np.array([-ext] * 3), h)
        # Projection first (onto the true surface), the exact land planes LAST — the same
        # order the field itself is built in, so no smoothing can round a land back off.
        v = project(v, sdf, h)
        v = snap_lands(v, lands, h)
        closed, _ = mesh_health(t)
        if not closed:
            sys.exit(f"gen_display_meshes: node {i} came out OPEN at res {res} — "
                     "the grid clipped it; ext or res has to move.")
        if len(v) > 65535:
            sys.exit(f"gen_display_meshes: node {i} has {len(v)} vertices at res {res} "
                     "— uint16 indices no longer fit.")
        out.append((v, t, mesh_volume(v, t)))
    return out


def encode(v, t, ext):
    q = np.round((v + ext) / QUANT_MM)
    if q.min() < 0 or q.max() > 65535:
        sys.exit("gen_display_meshes: a vertex fell outside the quantisation range.")
    b64 = lambda a: base64.b64encode(a.tobytes()).decode()
    return b64(q.astype("<u2")), b64(t.astype("<u2"))


def build() -> dict:
    man, prm, nodes, tree, incident, kinds_of, base_of, ext = article()
    fams = payload()["families"]
    file_to_idx = {r["file"]: i for i, r in enumerate(man["nodes"])}
    rep_idx = {key: file_to_idx[fams[key]["repFile"]] for key in ORDER}

    disp = extract(DISPLAY_RES, ext, prm, nodes, tree, incident, kinds_of, base_of,
                   range(len(nodes)), display=True)
    reps = extract(REP_RES, ext, prm, nodes, tree, incident, kinds_of, base_of,
                   [rep_idx[k] for k in ORDER], display=False)

    rows = []
    for i, (v, t, vol) in enumerate(disp):
        row = man["nodes"][i]
        pv, pi = encode(v, t, ext)
        rows.append({
            "file": row["file"], "u": row["u"], "role": row["role"], "arms": row["arms"],
            "slotBaseMm": row["slotBaseMm"],
            "verts": len(v), "tris": len(t), "volumeMm3": round(vol),
            "reachMm": round(float(np.linalg.norm(v, axis=1).max()), 2),
            "v": pv, "i": pi,
        })
    rep_rows = {}
    for key, (v, t, vol) in zip(ORDER, reps):
        row = man["nodes"][rep_idx[key]]
        pv, pi = encode(v, t, ext)
        rep_rows[key] = {
            "file": row["file"], "u": row["u"], "role": row["role"],
            "verts": len(v), "tris": len(t), "volumeMm3": round(vol),
            "v": pv, "i": pi,
        }
    return {
        "meta": {
            "displayRes": DISPLAY_RES, "repRes": REP_RES,
            "quantStepMm": QUANT_MM, "quantOriginMm": round(-ext, 6),
            "sourceHash": source_hash(),
            "displayTris": sum(r["tris"] for r in rows),
            "repTris": sum(r["tris"] for r in rep_rows.values()),
        },
        "nodes": rows,
        "reps": rep_rows,
    }


def render(data: dict) -> str:
    return (HEADER + "\nexport const NODEMESHES = "
            + json.dumps(data, indent=1) + ";\n")


def parse_module() -> dict:
    text = OUT.read_text()
    start = text.index("export const NODEMESHES = ") + len("export const NODEMESHES = ")
    return json.loads(text[start:text.rindex(";")])


def check() -> None:
    """Stale, structurally wrong, or out of step with the manifest — without an SDF run."""
    if not OUT.exists():
        sys.exit(f"gen_display_meshes --check: {OUT} does not exist — run the generator.")
    mod = parse_module()
    bad = []
    if mod["meta"]["sourceHash"] != source_hash():
        bad.append("sourceHash differs — gen_nodes.py, this generator or the manifest "
                   "parameters changed after this module was written")
    man = json.loads(MANIFEST.read_text())
    if len(mod["nodes"]) != len(man["nodes"]):
        bad.append(f"{len(mod['nodes'])} meshes against {len(man['nodes'])} manifest rows")
    for got, want in zip(mod["nodes"], man["nodes"]):
        for f in ("file", "u", "role", "arms", "slotBaseMm"):
            if got[f] != want[f]:
                bad.append(f"{want['file']}: {f} {got[f]!r} != manifest {want[f]!r}")
                break
    fams = payload()["families"]
    if list(mod["reps"]) != list(ORDER):
        bad.append(f"rep families {list(mod['reps'])} != {ORDER}")
    else:
        for key in ORDER:
            if mod["reps"][key]["file"] != fams[key]["repFile"]:
                bad.append(f"rep for {key} is {mod['reps'][key]['file']}, families "
                           f"module says {fams[key]['repFile']}")
    for row in mod["nodes"]:
        v, i = base64.b64decode(row["v"]), base64.b64decode(row["i"])
        if len(v) != row["verts"] * 6 or len(i) != row["tris"] * 6:
            bad.append(f"{row['file']}: payload length disagrees with its own counts")
    if bad:
        print("gen_display_meshes --check: STALE —")
        for b in bad[:12]:
            print(f"  {b}")
        sys.exit(1)
    print(f"display meshes: {len(mod['nodes'])} joints ({mod['meta']['displayTris']} tris) "
          f"+ {len(mod['reps'])} print-res representatives ({mod['meta']['repTris']} tris), "
          "sources unchanged")


def deep() -> None:
    """Re-extract everything and compare with tolerances. Slow; not in any gate."""
    mod = parse_module()
    fresh = build()
    bad = []
    for got, want in zip(fresh["nodes"], mod["nodes"]):
        if abs(got["tris"] - want["tris"]) > max(8, 0.01 * want["tris"]):
            bad.append(f"{want['file']}: {got['tris']} tris vs stored {want['tris']}")
        if abs(got["volumeMm3"] - want["volumeMm3"]) > 0.005 * want["volumeMm3"] + 2:
            bad.append(f"{want['file']}: volume {got['volumeMm3']} vs {want['volumeMm3']}")
    if bad:
        print("gen_display_meshes --deep: geometry drifted —")
        for b in bad[:12]:
            print(f"  {b}")
        sys.exit(1)
    print("deep: re-extracted geometry matches the module within tolerance")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--deep", action="store_true")
    args = ap.parse_args()
    if args.check:
        check()
        return
    if args.deep:
        deep()
        return
    data = build()
    OUT.write_text(render(data))
    m = data["meta"]
    print(f"wrote {OUT.name}: 51 display joints at res {m['displayRes']} "
          f"({m['displayTris']} tris), {len(data['reps'])} print-res reps at "
          f"res {m['repRes']} ({m['repTris']} tris), {OUT.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
