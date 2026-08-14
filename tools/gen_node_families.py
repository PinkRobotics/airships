#!/usr/bin/env python3
"""Group the 51 printed joints into their five families and emit them as an ES module.

    python3 tools/gen_node_families.py            # write ship/nodes.generated.js
    python3 tools/gen_node_families.py --check    # exit 1 if the module has gone stale

WHY THIS EXISTS. ship/model.js carries exactly ONE number out of the whole node manifest —
NODE_MASS_MEASURED_KG — hand-copied, with a comment explaining that a browser cannot read a
file off disk. (check_cell_parity holds it to the manifest; this docstring used to quote its
value, 0.444, and was wrong within a day of the per-arm SKU fix moving it to 0.465. A
number typed into a comment about not typing numbers is worth deleting rather than
correcting.) The connectors level of the explorer wants five families times
a dozen fields, and five hand-copies of a dozen fields is not a hand-copy, it is a second
copy of the manifest that no gate reads. So the manifest gets a generated ES module beside
it, the page imports it like any other module, and check_explorer.py holds the DOM to the
manifest through the page's own wiring.

THE CUT SCHEDULE IS HERE FOR THE SAME REASON, and it is the same two authorities meeting:
what a member is cut to is its centre-to-centre length minus the depth each of its ends
disappears into a socket, and that depth is the node's own slot base — a manifest field
that no browser can read. So the grouping is done here and the DEDUCTIONS are emitted;
the lengths are not. See cut_groups().

TWO SOURCES, BOTH AUTHORITIES, NEITHER RE-DERIVED HERE:
  research/geometry/nodes/manifest.json   what was actually printed — mass, volume, slot
                                          base, overhang, arm count, per node
  tools/gen_nodes.py::article_graph()     what each node is CONNECTED to, by member kind;
                                          imported, never reimplemented, because a second
                                          copy of the incidence is the same bug class as a
                                          second copy of a calculation

WHAT IS DELIBERATELY NOT EXPORTED: jointCheck.shoulderBearingMPa. It divides the strut
demand by the pipe's full 28.27 mm2 wall annulus, which is true at the 60-degree centre
node and at no other: at the four 45-degree families the slot base is pushed out to
13.96 mm while the printed collar only reaches core_r + lip = 10.5 mm, so the pipe lands on
the blend fillet instead of the shoulder. Publishing 119.3 MPa as the joint's bearing
stress would be quoting a figure that holds for 12 of 432 member-ends.
"""
from __future__ import annotations

import heapq
import json
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from gen_nodes import (HALF, article_graph, boundary_frame,  # noqa: E402  (path set above)
                       face_planes, spanning_tree)

MANIFEST = ROOT / "research" / "geometry" / "nodes" / "manifest.json"
OUT = ROOT / "ship" / "nodes.generated.js"

# The families, in the order the tour walks them: the cell centre first, then outward to
# the boundary. Names are the page's, the keys are the manifest's own (role, arms).
ORDER = ["lattice-12", "lattice-11", "lattice-8", "rimVertex-7", "hexHub-9"]
NAMES = {
    "lattice-12": "the cell centre",
    "lattice-11": "the workhorse",
    "lattice-8": "the square-face centre",
    "rimVertex-7": "the corner",
    "hexHub-9": "the hexagon hub",
}


def cut_groups(nodes: list, members: list, prm: dict, cut_list: list) -> list:
    """Every member of the article, grouped by what it is actually cut to.

    A member's length is centre to centre between two joints — SUNKEN centres, since the
    boundary frame: each boundary node sits displaced from its lattice point and every
    member touching one is genuinely shorter. A CUT is shorter again by the depth its ends
    disappear into their sockets. Group the 216 members by (SKU, length class, deduction,
    true cut) and the whole build collapses to nine saw settings — the same nine rows
    manifest.cutList carries, and that agreement is PROVEN below, not assumed.

    THE TRUE CUT IS BAKED IN NOW, and that is a reversal this docstring owes an account of.
    It used to emit deductions only, because the model's half-pitch is 0.115 mm off this
    generator's and a length derived here would be wrong in the fourth digit. The sunken
    frame changed the arithmetic's OWNER: a true cut depends on each end's sink, which the
    model does not know and cannot derive — the model keeps nominal lattice lengths as its
    conservative physics — so the cut is the manifest's fact, derived here exactly as
    gen_nodes.main() derives it and held to manifest.cutList row by row. The page still
    takes centre-to-centre lengths from the model; what it may no longer do is subtract its
    way to a cut, because the difference between those two numbers is the sink itself.
    """
    base = {tuple(n["u"]): n["slotBaseMm"] for n in nodes}
    # The sunken positions, exactly as gen_nodes.main() derives them: sinks judged on
    # NOMINAL directions, then real positions. sinkMm is already in the manifest per node,
    # but the frame is re-derived from the same rule instead of read back, so a manifest
    # written by a different boundary_frame drifts loudly at the cutList proof below.
    incident: dict[tuple, list] = {tuple(n["u"]): [] for n in nodes}
    for a, b, kind in members:
        d = np.array(b, float) - np.array(a, float)
        d /= np.linalg.norm(d)
        incident[a].append((d, kind))
        incident[b].append((-d, kind))
    pos = {}
    for n in nodes:
        u = tuple(n["u"])
        sink_vec, _pairs = boundary_frame(u, [d for d, _ in incident[u]],
                                          [k for _, k in incident[u]], prm)
        pos[u] = np.array(u, float) * HALF + sink_vec
    groups: dict[tuple, dict] = {}
    for a, b, kind in members:
        step2 = sum((a[i] - b[i]) ** 2 for i in range(3))    # in half-pitch units
        if step2 not in (1, 2):
            raise SystemExit(f"gen_node_families: member {a}-{b} steps {step2}, which is "
                             "neither a <100> tie nor a <110> octet step")
        length_key = "short" if step2 == 1 else "long"
        # The rim is the article's second SKU: the 36 cell edges carry the film's dihedral
        # pull and the model puts them on 14 x 12. Everything else is the 10 x 8.
        sku = "rim" if kind == "rim" else "main"
        deduct = round(base[a] + base[b], 2)
        true_len = float(np.linalg.norm(pos[b] - pos[a]))
        cut = round(true_len - base[a] - base[b], 3)
        g = groups.setdefault((sku, length_key, deduct, cut),
                              {"sku": sku, "lengthKey": length_key, "deductMm": deduct,
                               "cutMm": cut, "trueMemberMm": round(true_len, 3),
                               "count": 0, "kinds": {}})
        g["count"] += 1
        g["kinds"][kind] = g["kinds"].get(kind, 0) + 1

    # THE PROOF, AND THE HANDOVER: these groups ARE manifest.cutList, family by family,
    # count by count — and once each group is identified with its row, the row's own cutMm
    # replaces the derivation. The derived value groups and matches only: it is built on
    # the manifest's ROUNDED slot bases (two decimals), so it sits up to ~7 microns off the
    # generator's full-precision saw length, and publishing it would be publishing the
    # rounding. The match window is 0.02 mm — twice the worst that rounding can do and 50x
    # smaller than the closest two distinct cuts in the article — and a frame rule or a
    # manifest from a different run misses it loudly, by name.
    rows_left = [dict(r) for r in cut_list]
    for g in groups.values():
        if len(g["kinds"]) != 1:
            raise SystemExit(f"gen_node_families: cut group {g} mixes member families — "
                             "cutList rows are per family and this group matches none")
        fam = next(iter(g["kinds"]))
        near = [r for r in rows_left if r["family"] == fam
                and abs(r["cutMm"] - g["cutMm"]) <= 0.02]
        if len(near) != 1 or near[0]["count"] != g["count"]:
            raise SystemExit(f"gen_node_families: derived cut {fam} {g['cutMm']} x"
                             f"{g['count']} matches {len(near)} manifest.cutList rows "
                             f"{[(r['cutMm'], r['count']) for r in near]} — the frame rule "
                             "and the shipped manifest disagree; run `make nodes`.")
        g["cutMm"] = near[0]["cutMm"]
        g["closingCutMm"] = near[0]["closingCutMm"]
        g["swingReliefMm"] = near[0]["swingReliefMm"]
        rows_left.remove(near[0])
    if rows_left:
        raise SystemExit(f"gen_node_families: manifest.cutList rows unmatched by any drawn "
                         f"group: {[(r['family'], r['cutMm']) for r in rows_left]}")

    # A key must survive being written into a data-n path, a data-stop attribute and a
    # ?stop= link, so it carries no dot and no length. RANK the distinct (deduction, cut)
    # pairs inside each (SKU, length class) — deduction first, descending, then the longer
    # cut, so rank 0 is suffix-free and the ranks below it take Deep/Deep2/... The sink is
    # what made the second sort key exist: the 36 rim edges share one deduction and still
    # saw to two lengths, because hexagon-hexagon and square-hexagon corners sink along
    # different bisectors.
    ranks: dict[tuple, list] = {}
    for (sku, lk, ded, cut) in groups:
        ranks.setdefault((sku, lk), []).append((ded, cut))
    for k in ranks:
        ranks[k] = sorted(set(ranks[k]), key=lambda dc: (-dc[0], -dc[1]))
    out = []
    for (sku, lk, ded, cut), g in groups.items():
        r = ranks[(sku, lk)].index((ded, cut))
        g["key"] = sku + lk.capitalize() + ("" if r == 0 else "Deep" if r == 1 else f"Deep{r}")
        # The name is the composition, not a label someone chose: what kinds of member are
        # cut to this length, heaviest count first. (The old ", into the centre" tag hung
        # off the Deep suffix, which stopped meaning that the day the sink split classes.)
        kinds = sorted(g["kinds"], key=lambda k: (-g["kinds"][k], k))
        g["name"] = " + ".join(kinds)
        g["kindsText"] = " + ".join(f"{g['kinds'][k]} {k}" for k in kinds)
        out.append(g)
    keys = [g["key"] for g in out]
    if len(set(keys)) != len(keys):
        raise SystemExit(f"gen_node_families: cut group keys collide: {sorted(keys)}")
    # Interior first, boundary last, longest run first: the order the tour walks them.
    out.sort(key=lambda g: (g["sku"] == "rim", g["lengthKey"] == "short", -g["count"]))
    return out


def assembly_order(gnodes: list, members: list) -> list:
    """The build sequence, for the page to play: every member in the order the assembly
    proof walks them, with each one's engagement kind, its arriving joint, and its proven
    approach line.

    THE ORDER IS A3's OWN RULE, transcribed exactly — inside-out and TREE-CONSTRAINED:
    ascending lattice |midpoint| with (family, u, v) ties, taken only among members whose
    end joints' discovery members are already placed — not a new opinion about how to
    build the cell. check_assembly.build_order_access() derives the same order from the
    same graph every run and PROVES it: members blocked at their own turn counted,
    straight-line escapes swept against everything placed before each one, emitted as
    buildOrder in the report. This transcription exists because the page reads generated
    modules, not prover reports, and the rule is a dozen deterministic lines; if the two
    ever diverge, the dir-attach guard below compares this list's ids against the
    report's memberIds and refuses the mismatch by name.

    `closing` is the spanning tree's verdict, the same one that sizes the spigots: a tree
    member slides on axially over its full stub, a closing member swings in on pilots at
    its own entry tilt — which is exactly how the page animates each kind. `arriving` is
    the tree's own answer to which joint a tree member CARRIES: A4's proven free motion is
    the arriving node retracting along the parent axis WITH its member, so the page slides
    joint and pipe in together and neither can pass through the other. `dir` is the escape
    line A3 verified for this member at its own turn, read back from the committed report
    when the report matches this graph — the animation flies members in along the reversed
    escape, the one straight line proven clear of everything placed before it. A stale or
    absent report degrades softly: rows just lack `dir`, the page falls back to its
    outward-radial approach, and the mismatch is printed rather than hidden.
    """
    tree, tree_order = spanning_tree(gnodes, members)
    arriving_of = {k: arriving for k, _parent, arriving in tree_order}

    def mid(k):
        a, b, _f = members[k]
        return math.sqrt(sum(((ai + bi) / 2.0) ** 2 for ai, bi in zip(a, b)))

    # Inside-out AND tree-constrained, exactly as A3 emits it since the designer caught
    # the seam: the spanning tree is rooted at a square-centre joint while |midpoint|
    # walks out from the cell centre, so an unconstrained order had 27 tree members
    # arriving after their joint was already pinned — and a 20 mm stub cannot engage
    # sideways. Kahn's construction with the same key among the ready set: every joint
    # arrives carried by its own discovery member, deterministically.
    tree_of = {tuple(arr): k for k, _p, arr in tree_order}
    prereq: dict[int, set] = {}
    dependents: dict[int, list] = {}
    for k, (a, b, _f) in enumerate(members):
        for u in (a, b):
            d = tree_of.get(tuple(u))
            if d is not None and d != k:
                prereq.setdefault(k, set()).add(d)
                dependents.setdefault(d, []).append(k)
    key_of = {k: (mid(k), members[k][2], members[k][0], members[k][1])
              for k in range(len(members))}
    indeg = {k: len(prereq.get(k, ())) for k in range(len(members))}
    ready = sorted((key_of[k], k) for k in range(len(members)) if indeg[k] == 0)
    heapq.heapify(ready)
    order = []
    while ready:
        _, k = heapq.heappop(ready)
        order.append(k)
        for k2 in dependents.get(k, ()):
            indeg[k2] -= 1
            if indeg[k2] == 0:
                heapq.heappush(ready, (key_of[k2], k2))
    if len(order) != len(members):
        raise SystemExit("gen_node_families: tree-dependency order is cyclic — the "
                         "constraint wiring no longer matches spanning_tree")
    rows = []
    for k in order:
        row = {"a": list(members[k][0]), "b": list(members[k][1]),
               "fam": members[k][2], "closing": k not in tree}
        if k in arriving_of:
            row["arriving"] = list(arriving_of[k])
        rows.append(row)
    report = ROOT / "research" / "geometry" / "nodes" / "assembly.json"
    ids = [f"{members[k][0]}-{members[k][1]}-{members[k][2]}" for k in order]
    bo = None
    if report.exists():
        try:
            bo = json.loads(report.read_text()).get("buildOrder")
        except json.JSONDecodeError:
            bo = None
    if bo and bo.get("memberIds") == ids and len(bo.get("escapeDirs") or []) == len(rows):
        for row, d in zip(rows, bo["escapeDirs"]):
            if d:
                row["dir"] = d
    else:
        print("gen_node_families: assembly.json's buildOrder is absent or predates this "
              "graph — ASSEMBLY rows carry no proven approach lines; the page falls back "
              "to radial approaches. Run `make assemblycheck` and regenerate.")
    return rows


def payload() -> dict:
    m = json.loads(MANIFEST.read_text())
    nodes = m["nodes"]
    gnodes, members, tally = article_graph()

    # Arm composition per node, by member kind, from the graph that generated the meshes.
    inc: dict[tuple, dict[str, int]] = {}
    for a, b, kind in members:
        for u in (a, b):
            inc.setdefault(u, {})
            inc[u][kind] = inc[u].get(kind, 0) + 1

    total_mass = sum(n["massG"] for n in nodes)
    total_ends = sum(n["arms"] for n in nodes)

    groups: dict[str, list] = {}
    for n in nodes:
        groups.setdefault(f"{n['role']}-{n['arms']}", []).append(n)
    if sorted(groups) != sorted(ORDER):
        raise SystemExit(f"gen_node_families: families {sorted(groups)} != {sorted(ORDER)}"
                         " — the manifest's arm histogram moved; retune ORDER/NAMES.")

    fams = {}
    for key in ORDER:
        g = sorted(groups[key], key=lambda n: (n["massG"], n["u"]))
        # The representative is the MEDIAN-mass node of its family, tie-broken by u, so it
        # is deterministic and so no family is advertised by its lightest or heaviest
        # outlier. Values differ in the last digit inside a family — the page quotes the
        # min-max range, never one node's row as the family's.
        rep = g[len(g) // 2]
        comps = {tuple(sorted(inc[tuple(n["u"])].items())) for n in g}
        if len(comps) != 1:
            raise SystemExit(f"gen_node_families: {key} has mixed arm composition {comps}")
        comp = dict(next(iter(comps)))
        if sum(comp.values()) != g[0]["arms"]:
            raise SystemExit(f"gen_node_families: {key} composition {comp} does not sum "
                             f"to {g[0]['arms']} arms")

        # The angle the out-of-plane arms stand off this node's mating land, where it has
        # exactly one. At a hexagon hub that is the tripod prop against the hexagon normal
        # — the cube diagonal, 54.74 degrees — which is the whole reason three props on
        # <100> reach the octet at all. Computed from the graph and face_planes, so the
        # page can bind it instead of typing it.
        land_deg = None
        if g[0]["lands"] == 1:
            u = tuple(rep["u"])
            nrm = face_planes(u)[0]
            offs = set()
            for a, b, _kind in members:
                if u not in (a, b):
                    continue
                v = b if a == u else a
                d = [v[i] - u[i] for i in range(3)]
                dl = math.sqrt(sum(x * x for x in d))
                cos = abs(sum(d[i] * nrm[i] for i in range(3))) / dl
                if cos > 1e-9:                      # in-plane arms have nothing to report
                    offs.add(round(math.degrees(math.acos(cos)), 2))
            if len(offs) == 1:
                land_deg = offs.pop()

        def rng(field, nd=None):
            vals = [n[field] for n in g]
            lo, hi = min(vals), max(vals)
            return (round(lo, nd), round(hi, nd)) if nd is not None else (lo, hi)

        mass_lo, mass_hi = rng("massG", 2)
        vol_lo, vol_hi = rng("volumeMm3")
        ov_lo, ov_hi = rng("overhangAreaFrac", 4)
        tri_lo, tri_hi = rng("triangles")
        nme_lo, nme_hi = rng("nonManifoldEdges")
        ang = {n["minArmAngleDeg"] for n in g}
        slot = {n["slotBaseMm"] for n in g}
        lands = {n["lands"] for n in g}
        for name, s in (("minArmAngleDeg", ang), ("slotBaseMm", slot), ("lands", lands)):
            if len(s) != 1:
                raise SystemExit(f"gen_node_families: {key} has mixed {name} {sorted(s)}")
        mass_sum = round(sum(n["massG"] for n in g), 2)
        fams[key] = {
            "key": key, "name": NAMES[key], "role": g[0]["role"], "arms": g[0]["arms"],
            "count": len(g),
            "memberEnds": len(g) * g[0]["arms"],
            "memberEndPct": round(100 * len(g) * g[0]["arms"] / total_ends, 1),
            "composition": comp,
            "lands": lands.pop(),
            "armToLandDeg": land_deg,
            "minArmAngleDeg": ang.pop(),
            "slotBaseMm": slot.pop(),
            "massGMin": mass_lo, "massGMax": mass_hi,
            "massGSum": mass_sum,
            "massPct": round(100 * mass_sum / total_mass, 1),
            "volumeMm3Min": vol_lo, "volumeMm3Max": vol_hi,
            "overhangFracMin": ov_lo, "overhangFracMax": ov_hi,
            "trianglesMin": tri_lo, "trianglesMax": tri_hi,
            "nonManifoldEdgesMin": nme_lo, "nonManifoldEdgesMax": nme_hi,
            "repFile": rep["file"], "repU": list(rep["u"]),
            "repUText": "(" + ", ".join(str(x) for x in rep["u"]) + ")",
            "repMassG": rep["massG"],
        }

    p = m["paramsMm"]
    jc = m["jointCheck"]
    slot_bases = sorted({n["slotBaseMm"] for n in nodes})
    joint = {
        # The capture, as the SDF grows it: pipe over a hollow spigot, butted on a shoulder.
        "pipeOdMm": p["pipe_od"], "pipeIdMm": p["pipe_id"],
        "clearanceMm": p["clearance"], "stubMm": p["stub"],
        # The TWO engagements — the display meshes made the bare spigots visible for the
        # first time and their deliberate inequality needs its numbers on the page: a tree
        # member-end slides on axially over the full stub, a closing member-end swings
        # into a short pilot bounded by the swing-in geometry.
        "treeEndsMm": jc["treeEndsMm"], "closingEndsMm": jc["closingEndsMm"],
        "coreRMm": p["core_r"], "lipMm": p["lip"], "shoulderMm": p["shoulder"],
        "padRMm": p["pad_r"], "ribHMm": p["rib_h"], "ribs": p["ribs"],
        "perStrutDemandN": jc["perStrutDemandN"],
        "glueAreaMm2": jc["glueAreaMm2"], "glueShearMPa": jc["glueShearMPa"],
        "glueMarginAt10MPa": jc["glueMarginAt10MPa"],
        "spigotSectionMm2": jc["spigotSectionMm2"], "spigotStressMPa": jc["spigotStressMPa"],
        # An annular slot is a tube of this outer radius about each arm; two of them at
        # angle theta intersect until the slot starts beyond slotOuterRMm/sin(theta/2).
        # That one line is why four families seat 3.16 mm shallower than the fifth.
        "slotOuterRMm": round(p["pipe_od"] / 2 + p["clearance"], 2),
        "slotBaseMinMm": slot_bases[0], "slotBaseMaxMm": slot_bases[-1],
        "slotBaseSpreadMm": round(slot_bases[-1] - slot_bases[0], 2),
        # WHERE THE COLLAR ENDS, against where the slot starts. node_sdf's lip term reaches
        # core_r + lip from the node centre; the slot-clearance rule pushes every family's
        # base past that, so the pipe seats on the blend fillet and not on the nominal 2 mm
        # shoulder. That is geometry the manifest supports. How much bearing annulus is
        # left is NOT — it takes sampling the SDF — which is why jointCheck's
        # shoulderBearingMPa is not exported and the page does not quote it.
        "collarReachMm": round(p["core_r"] + p["lip"], 2),
        # The 36 cell edges are a 14 x 12 SKU in the structural model and a 10 mm socket in
        # every one of these meshes. This is how many member-ends that is.
        "rimMemberEnds": tally["rim"] * 2,
        "halfPitchMm": HALF,
        # rib_h and clearance against the voxel the meshes were extracted at: both under
        # half a cell, so the shipped STLs are geometry of record for FORM, not for FIT.
        "voxelMm": m["cellMm"],
        "ribHVoxels": round(p["rib_h"] / m["cellMm"], 2),
        "clearanceVoxels": round(p["clearance"] / m["cellMm"], 2),
    }
    cuts = cut_groups(nodes, members, m["paramsMm"], m["cutList"])
    return {
        "families": fams,
        "order": ORDER,
        "assembly": assembly_order(gnodes, members),
        "cuts": {
            "order": [g["key"] for g in cuts],
            "groups": {g["key"]: g for g in cuts},
            "members": len(members),
        },
        "totals": {
            "nodes": len(nodes), "families": len(fams),
            "members": sum(tally.values()), "memberEnds": total_ends,
            # The flat mating faces the skin is meant to bond to, and how many joints carry
            # one. Three at a corner, one on a square centre, one on a hub — nothing else
            # in the article is flat on purpose.
            "landedNodes": sum(1 for n in nodes if n["lands"]),
            "lands": sum(n["lands"] for n in nodes),
            "massG": round(total_mass, 2),
            "manifestMassKg": m["totalNodeMassKg"],
            "graph": tally, "res": m["res"],
        },
        "joint": joint,
    }


HEADER = """/* GENERATED — do not edit. `python3 tools/gen_node_families.py` rewrites this file.
 *
 * The 51 printed joints of the article, grouped into the five families the manifest's own
 * (role, arms) histogram produces, with every field taken from
 * research/geometry/nodes/manifest.json — the meshes that were actually written — and the
 * arm composition taken from tools/gen_nodes.py::article_graph().
 *
 * The browser cannot read the manifest off disk, and five families times a dozen fields is
 * not a number you hand-copy. tools/check_explorer.py regroups the manifest and fails if
 * this file has drifted from it, which is the same freshness gate check_figures_fresh runs
 * for figures, applied to geometry.
 */
"""


def render(data: dict) -> str:
    body = json.dumps(data, indent=2, sort_keys=False)
    return (HEADER + "\nexport const NODES = " + body + ";\n\n"
            "export const FAMILIES = NODES.families;\n"
            "export const FAMILY_ORDER = NODES.order;\n"
            "export const NODE_TOTALS = NODES.totals;\n"
            "export const JOINT = NODES.joint;\n"
            "export const CUT_GROUPS = NODES.cuts;\n"
            "export const ASSEMBLY = NODES.assembly;\n")


def main() -> None:
    if not MANIFEST.exists():
        sys.exit("gen_node_families: no manifest — run `make nodes` first.")
    text = render(payload())
    if "--check" in sys.argv:
        if not OUT.exists():
            sys.exit("gen_node_families: ship/nodes.generated.js is missing — run "
                     "`python3 tools/gen_node_families.py`.")
        if OUT.read_text() != text:
            sys.exit("gen_node_families: ship/nodes.generated.js has drifted from "
                     "research/geometry/nodes/manifest.json — run "
                     "`python3 tools/gen_node_families.py` (then `make stamp`).")
        print(f"node families: ship/nodes.generated.js is current with the manifest "
              f"({len(payload()['families'])} families, 51 joints).")
        return
    OUT.write_text(text)
    d = payload()
    fams = ", ".join(f"{k} x{v['count']}" for k, v in d["families"].items())
    print(f"wrote {OUT.relative_to(ROOT)}: {fams} — {d['totals']['memberEnds']} member-ends, "
          f"{d['totals']['massG']} g.")


if __name__ == "__main__":
    main()
