#!/usr/bin/env python3
"""ALGORITHMIC NODE GEOMETRY — the designer's ask, verbatim: "maybe computed smoothing
between the shapes would be the best path to take." Not spliced primitives.

    python3 tools/gen_nodes.py [--res 96] [--out research/geometry/nodes] ...

Every joint in the article is grown from one rule. A signed distance field smooth-min-blends
a spigot along each incident member into a solid core; the bores and the pipe's seating slot
are cut afterwards; and the mating faces are truncated flat LAST, so no blend can round a
land back off. Surface nets extract it, the vertices the truncation produced are snapped
exactly onto their planes, and each joint is written as a watertight binary STL — printable
directly. Change a diameter and all 51 joints regrow.

WHAT V2 ADDED, all of it from questions the designer asked while looking at the render:
  - FLAT MATING LANDS. Every boundary node sits exactly ON its faces, so the land is just
    the half-space truncation: the cell's own face plane, cutting the node flush. Square
    centres get one land, hexagon hubs one, rim vertices three — the corner of the cell.
  - A FILM PAD on each hexagon hub, coplanar with the face, so the membrane bears on an
    area instead of a point. It is local protection, NOT a load path: a pad can only
    collect 2*pi*r*T*sin(theta) from the film, a few hundred newtons at any sane size,
    while the hub's real share arrives through the spokes.
  - HEXAGON SPOKES. Six per face, because the squares were already braced in plane and the
    hexagons were not — see kelvin_lattice_counts in the analysis.
  - PRINT FRAMES. Each node is emitted in the orientation it should print in: land face
    down. For a hexagon hub that also lays all six spokes flat, in the strong in-plane
    direction. (V2 also claimed the 13 landless lattice nodes "keep the article frame ...
    and print support-free". They kept it because nothing had chosen, and they did not
    print support-free — see the V3 print datum below.)
  - CRUSH RIBS on the spigots: three shallow axial ridges that deform on assembly, so the
    fit is set by three ribs rather than by FDM's roundness — and a dry press fit becomes
    credible, which matters because a uniformly evacuated shell is all compression and may
    need no adhesive at all.
  - EXACT VOLUMES by the divergence theorem over the mesh actually written. Voxel counting
    was wrong by -7% to +3% depending only on where the grid happened to fall, and node
    mass is now a published figure the gates hold.

WHAT V3 ADDED, all of it from what the connection prover measured on V2's own field. Five
defects, one rule each, and every one of them changes all 51 joints at once:

  - A PILOT ON EVERY CLOSING MEMBER-END. The article has 51 nodes and 216 members, so its
    cycle rank is 216 - 51 + 1 = 166: only 50 members ever have a free end, and the other
    166 must drop between two nodes already fixed in space. Each needed 20 mm of axial
    travel and had 0.00, because the cut length IS the shoulder-to-shoulder gap. Nothing
    springs it in (116-227 kN for 20 mm) and nothing tilts it in (24.5 deg wanted, 0.86
    permitted). So engagement is now PER MEMBER-END: the 100 ends of the 50 spanning-tree
    members keep the full stub and are slid on axially; the 332 closing ends get a pilot
    short enough to swing in, 0.75*(2D)^(2/3)*P^(1/3) with D the diametral fit being the
    bound they are checked against. The cut length, the butt and the compression path are
    untouched.
  - A SEAT THAT EXISTS. The pipe was landing on a blend fillet: shoulder-forming material
    stopped at core_r + lip while the slot rule had pushed the seat 3.5 mm further out, so
    420 of 432 ends bore on 1.2-11.1 mm2 of fillet instead of the 28.27 mm2 annulus the
    manifest published, and the article's built dimensions were set by how hard each pipe
    was pushed. A COLLAR now carries the seat out to wherever the slot rule puts it: a
    cone-backed cylinder of radius pipe_od/2 + lip_wall, from base - shoulder to base + cup.
    The slot cuts the pipe's own annulus out of its top, which leaves a flat full-width land
    at t = base and a cup wall around it.
  - THE CUP IS THE LIP, AND IT REACHES. The old outer lip terminated at core_r + lip = 10.5
    mm while every seat sat at 10.8 mm or beyond, so the anti-brooming feature was absent at
    420 of 432 ends. Driving it off `base` instead of off `core_r` puts it where the pipe
    is. It also gives back some of what the pilot gives up: a closing end is now captured on
    BOTH surfaces over its short engagement rather than on one.
  - LIVE CRUSH RIBS. The seating slot subtracted the whole annulus from spig_r outward, and
    the rib crest lives inside that band, so rib_h was dead at every one of 432 member-ends
    and the "press fit" was a 0.15 mm slip. The slot's inner boundary is now the ribbed
    spigot's own profile, so the ribs survive exactly where the pipe grips them.
  - A BORE THAT DOES NOT OPEN ONTO A MATING FACE. Starting every bore at core_r*0.3 put its
    mouth through the land at 120 (arm, land) pairs. It now starts at whatever that arm's
    own steepest land needs, r_bore*tan(beta) plus a margin.
  - A PRINT DATUM FOR THE JOINTS THAT HAVE NO LAND. 13 of the 51 nodes are interior lattice
    nodes: they lie on no cell face, so face_planes() returns nothing and print_frame()
    returned the identity — the article frame, chosen by nothing. The bill for that, once
    something measured it: 11447 mm3 of material across the article that could not be built
    up from the bed, 9 arm ends starting in mid-air, one joint standing on 2.3 mm2 of plate.
    print_frame() now MEASURES all six lattice bed normals on the joint's own field and takes
    the one with the least material that cannot be built up from the bed: 5678 mm3, 0 ends in
    air, least contact 6.2 mm2. The objective is stated in full in that function; the short
    version is that "fewest downward arms" is the wrong objective and picking it makes the
    part worse, because an arm aimed down whose tip reaches the plate is a tower and four of
    them are a stand.
  - A PRINTABILITY MEASURE THAT CAN SEE AN ISLAND. overhangAreaFrac is an area fraction over
    the whole mesh: the joint with 716 mm3 hanging scores 0.143 and a joint with none scores
    0.128, inside a 0.11-0.20 spread — no signal at all. The manifest now carries
    bedContactMm2, supportAreaMm2 and islandVolumeMm3 per node, measured on the extraction
    grid by bed_support(), plus armsIntoAir — the count of ends that start with nothing
    beneath them, which is what "downward arm" was reaching for — and frameSearch, every
    orientation that was rejected and what it would have cost.

THE SLOT RULE, generalised. V2 computed one clearance — two seating slots must not bore
through each other — from an expression that was only about slots. The collar and the seated
pipe are features too, and the pipe's approach path is a feature. `slot_base` now takes the
worst of all four over the node's own arm pairs, which is why base moved outward.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
import pathlib
import struct as _struct
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
HALF = 177.25            # p/2 in mm — every article coordinate is an integer multiple


# ---------------------------------------------------------------- the article graph --
def article_graph():
    """51 nodes and 216 members, from the same parity rule the analysis counts with.

    60 octet + 36 rim + 48 hexagon spokes at 251 mm, 72 ties at 177 mm. One purchased SKU
    (10 x 8 pultruded tube), two cut lengths — including the ties, which sizing against
    the film's inward pull showed to be the MOST loaded members in the article, not the
    lightest.
    """
    def inside(u):
        a, b, c = abs(u[0]), abs(u[1]), abs(u[2])
        return max(a, b, c) <= 2 and a + b + c <= 3 and sum(u) % 2 == 0

    lattice = [u for u in itertools.product(range(-2, 3), repeat=3) if inside(u)]
    verts = [u for u in {tuple(s * v for s, v in zip(sg, pm))
                         for pm in itertools.permutations((0, 1, 2))
                         for sg in itertools.product((-1, 1), repeat=3)}
             if sorted(map(abs, u)) == [0, 1, 2]]
    hubs = list(itertools.product((-1, 1), repeat=3))

    members, lat = [], set(lattice)
    steps = [s for ab in ((1, 1), (1, -1)) for s in
             ((ab[0], ab[1], 0), (ab[0], 0, ab[1]), (0, ab[0], ab[1]))]
    for u in lattice:                                        # 60 octet
        for s in steps:
            v = (u[0] + s[0], u[1] + s[1], u[2] + s[2])
            if v in lat:
                members.append((u, v, "octet"))
    seen = set()
    for u in verts:                                          # 36 rim: the cell's edges
        for v in verts:
            if sum((x - y) ** 2 for x, y in zip(u, v)) == 2:
                k = tuple(sorted((u, v)))
                if k not in seen:
                    seen.add(k)
                    members.append((u, v, "rim"))
    for u in hubs:                                           # 48 hexagon spokes
        for w in itertools.permutations((0, 1, 2)):
            q = tuple(s * x for s, x in zip(u, w))
            if all(abs(x - y) <= 2 for x, y in zip(q, u)):
                members.append((u, q, "spoke"))
    for u in verts:                                          # 48 vertex ties
        members.append((u, tuple(0 if abs(x) == 1 else x for x in u), "tie"))
        members.append((u, tuple(x - (1 if x > 0 else -1) if abs(x) == 2 else x
                                 for x in u), "tie"))
    for u in hubs:                                           # 24 hexagon tripod props
        for q in range(3):
            t = list(u)
            t[q] = 0
            members.append((u, tuple(t), "tie"))

    nodes = ([(u, "lattice") for u in lattice] + [(u, "rimVertex") for u in verts]
             + [(u, "hexHub") for u in hubs])
    tally = {}
    for _, _, k in members:
        tally[k] = tally.get(k, 0) + 1
    assert len(nodes) == 51 and len(members) == 216, (len(nodes), len(members))
    assert tally == {"octet": 60, "rim": 36, "spoke": 48, "tie": 72}, tally
    return nodes, members, tally


def spanning_tree(nodes, members):
    """The 50 members that arrive at a node nothing has reached yet — and, by omission, the
    166 that do not.

    THE FAILURE THIS PREVENTS, and it is the one that only appears with glue on your hands.
    A member with a spigot at BOTH ends can only be seated if one of its two nodes is still
    free to move: slide the node on, and the member's own length is the travel. Every other
    member has to drop into a gap that equals its cut length exactly, and 20 mm of spigot at
    each end has nowhere to go. Which members those are is a property of the GRAPH, not of a
    guess: breadth-first from the first node, every member that discovers a new node is a
    tree member and every member that does not is a closing member. E - V + C = 216 - 51 + 1
    = 166 of them, and no build order can beat that, because exactly V - 1 = 50 insertions
    in any sequence bring a new node.

    Returns (tree, order): the member indices in the tree, and the discovery order as
    (member, parent node, arriving node) — which is also the order the tree assembles in.
    """
    adj = collections.defaultdict(list)
    for k, (a, b, _) in enumerate(members):
        adj[a].append((b, k))
        adj[b].append((a, k))
    root = nodes[0][0]
    seen, queue, tree, order = {root}, collections.deque([root]), set(), []
    while queue:
        u = queue.popleft()
        for v, k in adj[u]:
            if v not in seen:
                seen.add(v)
                tree.add(k)
                order.append((k, u, v))
                queue.append(v)
    assert len(seen) == len(nodes), "the article graph is not connected"
    assert len(tree) == len(nodes) - 1, (len(tree), len(nodes))
    return tree, order


def pilot_bound(cut_mm, diametral_mm):
    """s_max = 0.75 (2D)^(2/3) P^(1/3): the deepest pilot a closing member can swing in on.

    Two constraints bound the path of a member dropped between two fixed nodes. The kinematic
    identity e_A + e_B = s_A + s_B - P(1 - cos phi) says how much engagement a tilt buys back,
    and the peg-in-hole limit e <= D/phi says how deep a tilted spigot can be before it jams.
    Feasibility at every phi needs 2s <= 2D/phi + P phi^2/2, and minimising the right-hand side
    over phi gives phi* = (2D/P)^(1/3) and the closed form above. On this article it is 3.23 mm
    at the 219 mm cut and 2.83 at the 146 mm tie, so --pilot 2.0 is the design point with
    margin. main() asserts against it rather than trusting the default.
    """
    return 0.75 * (2.0 * diametral_mm) ** (2.0 / 3.0) * cut_mm ** (1.0 / 3.0)


def swing_relief(cut_mm, prm, kind):
    """How much SHORTER each end of a closing member must be cut than its seat-to-seat gap.

    THE PITFALL THIS CLOSES, and neither the pilot bound nor any parameter in this file sees
    it. A member dropped between two fixed nodes is tilted by phi, so each end face pulls back
    from its seat by P(1 - cos phi)/2 — but the end face is a disc, and its low corner swings
    Ro sin phi the other way. The corner is therefore below the seat plane whenever

        Ro sin phi > P (1 - cos phi) / 2,

    and for small phi that is EVERY angle under about 4 Ro / P — 5.3 degrees on the long cut.
    So a square-cut tube whose length equals the seat gap cannot be rotated down through the
    last few degrees AT ALL, at any pilot depth and at any axial position, because the two
    corners' projections have to fit in a gap the tilt itself is what opens. Shortening the
    pilot does not help; this is about the pipe, not the spigot.

    The relief is the deepest that corner ever reaches, max over phi at tan phi* = 2 Ro / P:
    0.115 mm on the long cuts, 0.173 on the ties. Cut that much off each end and the whole
    rotation is clear — which is why it is derived here and published on every cut row rather
    than left to a note about chamfering.

    Ro IS THE MEMBER'S OWN TUBE, which is why `kind` has no default. Ro appears twice above and
    the relief grows with it: on the 212.70 mm rim cut a 14 mm tube's corner reaches 0.2301 mm
    below the seat plane where a 10 mm one reaches 0.1175. Reading the global pipe_od published
    0.150 mm on all 36 rim members — 0.080 mm short of their own geometric minimum — and their
    corners then fouled the seat through the 2.1-5.4 degree part of the rotation, 0.052 mm of
    solid at four of the thirteen poses check_assembly's sweep samples. Defaulting the argument
    would let the next call site reintroduce exactly that silently, so every caller states the
    family it holds.

    WHAT IT COSTS, said plainly: a closing member no longer butts dry on its seat. It stops
    2 x relief short of the shoulder-to-shoulder gap, and that space is a bondline. E5's crush
    coupon therefore has to load a GLUE-FILLED butt at a closing end, not only a dry one.
    """
    r_o = arm_pipe(kind, prm)[0] / 2.0
    phi = math.atan(2.0 * r_o / cut_mm)
    need = r_o * math.sin(phi) - cut_mm * (1.0 - math.cos(phi)) / 2.0
    # A quarter over the geometric minimum, then rounded UP to 0.05 mm. The bare minimum leaves
    # 0.003 mm at the tightest pose on the tie, which is a hundredth of what any of the probes
    # here resolve and is not a clearance anyone can cut to. Rounding DOWN would publish a
    # relief that does not clear at all.
    return round(math.ceil(need * 1.25 / 0.05 - 1e-12) * 0.05, 3)


def face_planes(u):
    """Outward unit normals of the cell faces this node lies ON — its mating lands.

    Square faces are u_q = +-2; hexagon faces are sum(s*u) = 3 per sign octant. Every
    boundary node sits exactly ON its faces, so in the node's own frame the land plane
    passes through the origin and the land is a plain half-space truncation. No inset is
    needed any more: v1 pushed boundary nodes inward by a core radius to keep the faces
    flat, which is exactly what truncation does properly.
    """
    out = []
    for q in range(3):
        if abs(u[q]) == 2:
            n = [0.0, 0.0, 0.0]
            n[q] = float(np.sign(u[q]))
            out.append(np.array(n))
    for s in itertools.product((-1, 1), repeat=3):
        if sum(si * ui for si, ui in zip(s, u)) == 3:
            out.append(np.array(s, float) / math.sqrt(3.0))
    return out


# -------------------------------------------------------------------- the slot rule --
def arm_pipe(kind, prm):
    """The SKU this member is actually cut from — (od, id) in mm.

    stock_build() specifies TWO tubes, not one: 10 x 8 for the 180 octet/spoke/tie members and
    14 x 12 for the 36 rim members, which the film's dihedral edge sized when the bending check
    found the unbraced rim failing at 0.44 atm. V2 drew every socket at the single global
    pipe_od, so all 72 rim ends got a socket four millimetres too small for the tube the
    analysis buys: 2.15 mm of radial slop, the pipe never touching the crush ribs, and the lip
    cup at 6.60 mm sitting INSIDE the pipe's own 6.00 mm bore. The designer found it by eye in
    the render before any gate did, and the prover then put it as plainly as it can be put —
    that connection does not exist.

    Everything the socket is made of keys off these two numbers, so passing the member's own
    kind through is the whole fix; nothing else special-cases the rim.
    """
    if kind == "rim":
        return prm["rim_pipe_od"], prm["rim_pipe_id"]
    return prm["pipe_od"], prm["pipe_id"]


def pair_reach(r1, r2, theta_deg):
    """How far along BOTH axes two features of outer radius r1 and r2 can share a point.

    Both are surfaces of revolution about axes crossing at theta, so a point inside both is
    fixed by its two axial coordinates and its out-of-plane offset; maximising the smaller
    axial coordinate over that region gives min(r2 + r1 cos, r1 + r2 cos) / sin. For equal
    radii it collapses to the familiar R cot(theta/2), and for r2 = 0 to r1 cot(theta) — the
    distance out to which a bare axis stays inside a cylinder. A feature that starts beyond
    this value cannot reach a feature on the neighbouring arm that starts beyond it either.

    Collinear arms return -inf: two opposed arms are the same line, and their features are
    separated by their own axial ranges rather than by any angle. The tolerance is 1e-6 on the
    sine and not 1e-9, because acos of a dot product that should be exactly -1 comes back a
    couple of 1e-8 short of pi, and dividing by that sine returns 7.6e7 mm of "reach" — which
    silently became the slot base on the 21 nodes that have an opposed pair.
    """
    th = math.radians(theta_deg)
    ct, st = math.cos(th), math.sin(th)
    if abs(st) < 1e-6:
        return -math.inf
    return min(r2 + r1 * ct, r1 + r2 * ct) / st


def one_way_reach(r_self, r_other, theta_deg):
    """How far along THIS arm's axis a feature of radius r_other on the neighbour reaches.

    The asymmetric half of the same geometry: max t_self = (r_other + r_self cos)/sin. Used
    where the neighbour's feature has no axial start worth crediting — a spigot runs from the
    node centre, so only this arm's own coordinate bounds the overlap.
    """
    th = math.radians(theta_deg)
    if abs(math.sin(th)) < 1e-6:
        return -math.inf
    return (r_other + r_self * math.cos(th)) / math.sin(th)


def slot_base(dirs, prm, kinds=None):
    """Where this node's seating slots may start, from the node's own worst pair of arms.

    THE FAILURE THE DESIGNER REASONED OUT before any render could show it: the annular slot a
    pipe seats in is a tube of outer radius Ro around each arm, and two arms at angle theta
    have their SLOTS intersect until the slot starts far enough out. Cut both anyway — the SDF
    subtracts last and wins — and the print comes out with each slot bored through its
    neighbour: the pipe fouls on the remains and never reaches its shoulder. Nothing in a
    render shows it.

    V2 checked that one pair type and used Ro/sin(theta/2), which is a radial distance where
    an axial one is wanted. Three more features have to clear each other, and the collar is
    the one that governs now:

      slot x slot      two seating slots, the original rule, exactly: Ro cot(theta/2)
      slot x collar    a neighbour's slot must not eat the seat or the cup this arm bears on,
                       and the collar starts a shoulder EARLIER than the slot does
      slot x spigot    a neighbour's ribbed spigot must not stand inside this slot
      pipe x collar    the seated pipe is 5 mm of solid tube: the collar must be clear of it

    Returns (base, min_ang, need). `need` is the envelope plus the declared slot_margin, and
    base is that or core_r + shoulder, whichever is further out.

    PER-ARM RADII. `kinds` gives each direction its member kind, and every radius below is
    that arm's OWN SKU. This matters far more than it looks: with one global pipe_od the rim
    and the vertex ties at a shared corner were both drawn 10 mm, needed 10.0 mm of separation
    and had 10.68, and passed. At the 14 mm tube the analysis actually specifies they need
    12.0 and the pair overlaps by 1.32 mm — so giving the rim its real tube does not create
    that interference, it REVEALS it. The cure falls out of this function on its own: a bigger
    tube demands a longer reach, the base moves out until the pipes clear, and the corner nodes
    grow by however much the geometry says. No special case, no patch, one rule still growing
    all 51 joints. `kinds` defaults to the main SKU throughout so an old caller is unchanged.
    """
    dirs = list(dirs)
    kinds = ["octet"] * len(dirs) if kinds is None else list(kinds)
    rad = []
    for k in kinds:
        od, idm = arm_pipe(k, prm)
        rad.append((od / 2.0 + prm["clearance"],                    # ro_slot
                    od / 2.0 + prm["lip_wall"],                     # r_collar
                    idm / 2.0 - prm["clearance"]
                    + (prm["rib_h"] if prm["ribs"] else 0.0),       # r_crest
                    od / 2.0))                                      # r_pipe
    min_ang, need = 180.0, 0.0
    for i, j in itertools.combinations(range(len(dirs)), 2):
        th = math.degrees(math.acos(max(-1.0, min(1.0, float(dirs[i] @ dirs[j])))))
        min_ang = min(min_ang, th)
        (ro_i, col_i, cr_i, pipe_i), (ro_j, col_j, cr_j, pipe_j) = rad[i], rad[j]
        need = max(need,
                   pair_reach(ro_i, ro_j, th),
                   pair_reach(ro_i, col_j, th) + prm["shoulder"],
                   pair_reach(ro_j, col_i, th) + prm["shoulder"],
                   one_way_reach(ro_i, cr_j, th),
                   one_way_reach(ro_j, cr_i, th),
                   one_way_reach(pipe_i, col_j, th),
                   one_way_reach(pipe_j, col_i, th))
    need += prm["slot_margin"]
    return max(prm["core_r"] + prm["shoulder"], need), min_ang, need


def bore_start(d, lands, prm, kind="octet"):
    """Where this arm's bore may open, from the mating faces this arm's node carries.

    A bore of radius R whose axis meets a land plane at beta = acos(-d.n) breaks that plane
    unless it starts beyond R*tan(beta). Starting every bore at core_r*0.3 opened 120 (arm,
    land) mouths onto a face two cells are meant to seat on — 0.216 mm short at the worst of
    them, which is exactly the kind of miss no render shows and no triangle count moves.
    """
    r_bore = arm_pipe(kind, prm)[1] / 2.0 - prm["clearance"] - prm["spigot_wall"]
    t0 = prm["core_r"] * 0.3
    for n in lands:
        c = float(d @ n)
        if c >= 0.0:                 # the arm points out of the half-space: no mouth to cut
            continue
        beta = math.acos(max(-1.0, min(1.0, -c)))
        if beta < math.pi / 2.0 - 1e-9:
            t0 = max(t0, r_bore * math.tan(beta) + prm["bore_margin"])
    return t0


# ------------------------------------------------------------------------- the SDF --
def smin(a, b, k):
    """Polynomial smooth min — the computed smoothing itself."""
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + (a - b) * h - k * h * (1.0 - h)


def node_sdf(P, arms, lands, prm, is_hub, base=None, stubs=None, bores=None, kinds=None):
    """One field, every joint. Spigots and collars blended into a core, then the slots and
    bores subtracted, then the mating lands truncated last.

    `stubs` is the engagement PER ARM and is the whole of the closing-member fix: a tree
    member-end gets prm["stub"], a closing one gets prm["pilot"], and everything downstream —
    the spigot's reach, the slot's length, the cup's depth, the bore's end — follows from that
    one number rather than from a global. `bores` is each arm's own bore start. Both default
    to the uniform V2 values so a caller that does not know the graph still gets a field.
    """
    if base is None:
        base = prm["core_r"] + prm["shoulder"]
    stubs = [prm["stub"]] * len(arms) if stubs is None else list(stubs)
    bores = [prm["core_r"] * 0.3] * len(arms) if bores is None else list(bores)
    # PER-ARM SKU. `kinds` is what lets one node carry both tubes: a rim vertex has three 14 mm
    # rim arms and four 10 mm spoke/tie arms, and every radius below is the arm's own. Defaults
    # to the main SKU on every arm, which is exactly the V2 field, so old callers are unchanged.
    kinds = ["octet"] * len(arms) if kinds is None else list(kinds)
    spig_rs, ro_slots, r_collars = [], [], []
    for k in kinds:
        od, idm = arm_pipe(k, prm)
        spig_rs.append(idm / 2.0 - prm["clearance"])
        ro_slots.append(od / 2.0 + prm["clearance"])
        r_collars.append(od / 2.0 + prm["lip_wall"])
    root2 = math.sqrt(2.0)

    d = None
    for dirv, stub, spig_r, r_collar in zip(arms, stubs, spig_rs, r_collars):
        ta = P @ dirv                                   # signed distance along the arm
        t = np.clip(ta, 0.0, base + stub)
        rad = np.linalg.norm(P - t[:, None] * dirv[None, :], axis=1)
        if prm["ribs"]:
            # three shallow axial ridges around the spigot: the fit lands on the ribs, not
            # on FDM's idea of a circle. Phase is arbitrary but must be per-arm, so it is
            # taken about the arm's own axis. The seating slot below is cut to THIS profile,
            # not to the bare cylinder, or the ribs are removed by the slot that needs them.
            ref = np.array([0.0, 0.0, 1.0]) if abs(dirv[2]) < 0.9 else np.array([1.0, 0, 0])
            e1 = np.cross(dirv, ref)
            e1 /= np.linalg.norm(e1)
            e2 = np.cross(dirv, e1)
            ang = np.arctan2(P @ e2, P @ e1)
            crest = spig_r + prm["rib_h"] * np.clip(np.cos(prm["ribs"] * ang), 0, 1)
        else:
            crest = spig_r
        arm = rad - crest
        # THE COLLAR: the seat the pipe butts on and the cup that closes around it. A
        # cylinder of radius pipe_od/2 + lip_wall from base - shoulder to base + cup, backed
        # by a 45 degree cone so the flange is not an unsupported ledge on the bed. The seat
        # face itself is cut by the slot below, which is a hard subtraction, so no blend can
        # round the land the pipe lands on. Driving both off `base` is what makes them exist:
        # V2 drove the cup off core_r and it stopped 3.5 mm short of every seat in the
        # article.
        cup = min(prm["lip"], stub)
        rad_ax = np.linalg.norm(P - ta[:, None] * dirv[None, :], axis=1)
        collar = np.maximum(
            rad_ax - r_collar,
            np.maximum((rad_ax - ta + base - prm["shoulder"] - r_collar) / root2,
                       ta - (base + cup)))
        arm = np.minimum(arm, collar)
        d = arm if d is None else smin(d, arm, prm["blend"])
    d = smin(d, np.linalg.norm(P, axis=1) - prm["core_r"], prm["blend"])
    if is_hub and prm["pad_r"] > 0.0:      # optional film pad; the spokes replaced it
        n = lands[0]
        h = P @ n
        disc = np.maximum(np.linalg.norm(P - h[:, None] * n[None, :], axis=1) - prm["pad_r"],
                          np.maximum(h, -prm["pad_t"] - h))
        d = smin(d, disc, prm["pad_blend"])
    for dirv, stub, t_bore, spig_r, ro_slot in zip(arms, stubs, bores, spig_rs, ro_slots):
        # bores and slots, AFTER the blend
        t = P @ dirv
        rad = np.linalg.norm(P - t[:, None] * dirv[None, :], axis=1)
        if prm["ribs"]:
            ref = np.array([0.0, 0.0, 1.0]) if abs(dirv[2]) < 0.9 else np.array([1.0, 0, 0])
            e1 = np.cross(dirv, ref)
            e1 /= np.linalg.norm(e1)
            e2 = np.cross(dirv, e1)
            ang = np.arctan2(P @ e2, P @ e1)
            crest = spig_r + prm["rib_h"] * np.clip(np.cos(prm["ribs"] * ang), 0, 1)
        else:
            crest = spig_r
        t_end = base + stub + prm["blend"]
        slot = np.maximum(
            np.maximum(crest - rad, rad - ro_slot),
            np.maximum(base - t, t - t_end))
        d = np.maximum(d, -slot)
        hollow_r = spig_r - prm["spigot_wall"]
        if hollow_r > 0.8:
            # rad - hollow_r, NOT hollow_r - rad: a solid cylinder is negative INSIDE, and
            # the inverted sign had every arm subtracting its own exterior instead.
            bore = np.maximum(rad - hollow_r,
                              np.maximum(t_bore - t, t - t_end))
            d = np.maximum(d, -bore)
    for n in lands:                  # THE LANDS, hard and last
        d = np.maximum(d, P @ n)
    return d


# ------------------------------------------------------- surface nets + STL writing --
def surface_nets(sdf_grid, origin, h):
    """Naive surface nets: one vertex per sign-change cell, one quad per sign-change edge."""
    s = sdf_grid
    n = s.shape[0]
    cell_sum = np.zeros((n - 1, n - 1, n - 1, 3))
    cell_cnt = np.zeros((n - 1, n - 1, n - 1))
    quads = []
    # (ax, o1, o2) MUST be a cyclic permutation — (1, (0, 2)) is left-handed and winds
    # every y-crossing quad backwards, which cost this file its first watertight run.
    axes = ((0, (1, 2)), (1, (2, 0)), (2, (0, 1)))
    for ax, _ in axes:
        sl0, sl1 = [slice(None)] * 3, [slice(None)] * 3
        sl0[ax], sl1[ax] = slice(0, n - 1), slice(1, n)
        a, b = s[tuple(sl0)], s[tuple(sl1)]
        cross = (a < 0) != (b < 0)
        idx = np.argwhere(cross)
        if idx.size == 0:
            continue
        t = a[cross] / (a[cross] - b[cross])
        pt = idx.astype(float)
        pt[:, ax] += t
        pts = origin + pt * h
        o1, o2 = dict(axes)[ax]
        for d1 in (0, -1):
            for d2 in (0, -1):
                ci = idx.copy()
                ci[:, o1] += d1
                ci[:, o2] += d2
                ok = ((ci >= 0) & (ci <= n - 2)).all(axis=1)
                np.add.at(cell_sum, tuple(ci[ok].T), pts[ok])
                np.add.at(cell_cnt, tuple(ci[ok].T), 1.0)
        flip = a[cross] > 0
        for k in range(idx.shape[0]):
            base = list(idx[k])
            cells = []
            for d1, d2 in ((-1, -1), (0, -1), (0, 0), (-1, 0)):
                c = base.copy()
                c[o1] += d1
                c[o2] += d2
                cells.append(tuple(c))
            if flip[k]:
                cells.reverse()
            quads.append(cells)

    vert_of, verts, tris = {}, [], []
    for q in quads:
        ids, skip = [], False
        for c in q:
            if not all(0 <= c[i] <= n - 2 for i in range(3)) or cell_cnt[c] == 0:
                skip = True
                break
            if c not in vert_of:
                vert_of[c] = len(verts)
                verts.append(cell_sum[c] / cell_cnt[c])
            ids.append(vert_of[c])
        if skip:
            continue
        tris.append((ids[0], ids[1], ids[2]))
        tris.append((ids[0], ids[2], ids[3]))
    return np.array(verts), np.array(tris, dtype=np.int64)


def mesh_health(tris):
    """CLOSED means printable: every directed edge has its reverse, so there are no holes.
    Saddle cells leave a few NON-MANIFOLD pinch edges; the surface stays closed and slicers
    take it, and the count is reported rather than hidden."""
    edges = {}
    for a, b, c in tris:
        for e in ((a, b), (b, c), (c, a)):
            edges[e] = edges.get(e, 0) + 1
    closed = bool(edges) and all((e[1], e[0]) in edges for e in edges)
    return closed, sum(1 for v in edges.values() if v != 1) // 2


def mesh_volume(v, t):
    """Exact volume of the mesh actually written — divergence theorem, mm^3."""
    a, b, c = v[t[:, 0]], v[t[:, 1]], v[t[:, 2]]
    return float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)


def overhang_fraction(v, t):
    """Area fraction facing downward steeper than 45 degrees.

    KEPT, BUT IT IS NOT THE PRINTABILITY FIGURE and must never be read as one: it is an area
    fraction over the WHOLE mesh, so it is diluted by every square millimetre of the part
    that is fine, and it cannot see an island at all. The joints that came out with hundreds
    of cubic millimetres of material hanging in air scored no worse on it than the joints
    with none — the whole spread over 51 joints is 0.11 to 0.20. bed_support() below measures
    what actually decides the print.
    """
    a, b, c = v[t[:, 0]], v[t[:, 1]], v[t[:, 2]]
    n = np.cross(b - a, c - a)
    mag = np.linalg.norm(n, axis=1)
    area = mag / 2.0
    nz = n[:, 2] / (mag + 1e-12)
    return float(area[nz < -0.7071].sum() / max(area.sum(), 1e-12))


# ------------------------------------------------------------------- printability --
def _fill_runs(mask, seed, axis):
    """One run-fill pass: every maximal run of `mask` along `axis` that a seed touches fills.

    Cell-by-cell dilation needs one pass per cell of travel — 112 passes to cross one layer
    of the extraction grid, times 112 layers, times six candidate orientations, times 13
    joints. Filling whole runs at a time crosses a shape in as many passes as the shape has
    turns, which is a handful. Same construction as check_assembly's flood, and for the same
    reason: scipy is not a declared dependency of this repository.
    """
    m = np.moveaxis(mask, axis, -1)
    s = np.moveaxis(seed, axis, -1)
    pad = np.zeros_like(m[..., :1])
    starts = m & ~np.concatenate([pad, m[..., :-1]], axis=-1)
    rid = np.cumsum(starts, axis=-1)
    lines = int(np.prod(m.shape[:-1])) if m.ndim > 1 else 1
    stride = int(rid.max()) + 1
    key = rid + np.arange(lines).reshape(m.shape[:-1] + (1,)) * stride
    key = np.where(m, key, -1)
    flat = key.ravel()
    sel = flat >= 0
    hits = np.bincount(flat[sel], weights=s.ravel()[sel].astype(np.float64),
                       minlength=lines * stride) > 0
    out = np.zeros(m.shape, bool)
    out.ravel()[sel] = hits[flat[sel]]
    return np.moveaxis(out, -1, axis)


def _flood_layer(mask, seed):
    """Everything in one layer's `mask` laterally connected to `seed`."""
    while True:
        new = seed | _fill_runs(mask, seed, 0) | _fill_runs(mask, seed, 1)
        if np.array_equal(new, seed):
            return seed
        seed = new


def _spread45(layer):
    """A layer dilated by one cell in the four lateral directions and the four diagonals.

    This is the 45 degree rule at the grid's own spacing: material one layer up may hang out
    by one cell and still be carried. Using only the four-neighbour cross would put the
    threshold exactly ON 45 degrees, and 160 of this article's 432 member-ends sit at exactly
    45 degrees — whether each one came out supported would then be decided by where the grid
    happened to fall, not by the part.
    """
    o = layer.copy()
    o[1:, :] |= layer[:-1, :]
    o[:-1, :] |= layer[1:, :]
    o[:, 1:] |= layer[:, :-1]
    o[:, :-1] |= layer[:, 1:]
    o[1:, 1:] |= layer[:-1, :-1]
    o[1:, :-1] |= layer[:-1, 1:]
    o[:-1, 1:] |= layer[1:, :-1]
    o[:-1, :-1] |= layer[1:, 1:]
    return o


def bed_support(F3, h):
    """What the printer has to hold up, measured on the field the mesh came out of.

    THE FAILURE THIS EXISTS TO CATCH, in the prover's own words: "40 of 432 arms point
    downward, each a 7.7 mm OD, 2.0 mm wall tube printed into air — and overhangAreaFrac
    cannot see any of it." It cannot, because it is a fraction of the whole mesh's area and
    an island is small. Three quantities decide whether a part comes off the bed, and not
    one of them is a fraction:

      bedContactMm2    what touches the plate on layer one. A joint standing on one 30 mm2
                       arm tip is a joint that comes loose.
      supportAreaMm2   cross-section with no material within 45 degrees below it: the
                       support bill. It matters beyond print time because every support
                       that lands inside a seating slot is a 0.15 mm fit destroyed.
      islandVolumeMm3  material that cannot be built up from the bed AT ALL — the arm that
                       starts in mid-air. This is the one that decides whether the part
                       exists, and it is zero or it is not.

    The reachability rule is the slicer's own, layer by layer from the bed: a cell is
    buildable if a buildable cell sits within one lateral step on the layer below, or if it
    is laterally connected inside its own layer to a cell that is. The lateral flood is what
    makes a horizontal arm buildable — its underside is a bridge off the core, not an
    island — and leaving it out would have condemned every arm the article has.

    WHAT THIS MEASURE CONCEDES, said out loud because a measure whose blind spot is unstated
    is the thing it replaced. In-layer connection is treated as buildable, so a long
    cantilever printed sideways off a supported root counts as reached even though it will
    droop; that is what supportAreaMm2 is beside it for, and it is why the two are reported
    together rather than one being called the answer. On the centre joint in the article
    frame it was the difference between a spigot 16 mm clear of the plate reading as an
    island and reading as reached — the blend at the core joins it to a foot inside its own
    layer, and it does.

    Returns the three figures plus the island mask, which arms_into_air() reads to say WHICH
    arm is hanging rather than only how much material is.
    """
    solid = F3 < 0.0
    occ = solid.any(axis=(0, 1))
    if not occ.any():
        return {"bedContactMm2": 0.0, "supportAreaMm2": 0.0, "islandVolumeMm3": 0.0,
                "bedLayer": 0, "island": solid}
    k0 = int(np.argmax(occ))
    reach = np.zeros_like(solid)
    reach[:, :, k0] = solid[:, :, k0]          # layer one is held by the plate
    unsup = np.zeros_like(solid)
    for k in range(k0 + 1, solid.shape[2]):
        here = solid[:, :, k]
        unsup[:, :, k] = here & ~_spread45(solid[:, :, k - 1])
        reach[:, :, k] = _flood_layer(here, here & _spread45(reach[:, :, k - 1]))
    island = solid & ~reach
    return {"bedContactMm2": float(solid[:, :, k0].sum()) * h * h,
            "supportAreaMm2": float(unsup.sum()) * h * h,
            "islandVolumeMm3": float(island.sum()) * h ** 3,
            "bedLayer": k0, "island": island}


def arms_into_air(island, ext, h, arms, prm, base, stubs, kinds):
    """Which arms have their far end starting in mid-air — the honest form of "downward arm".

    "Points downward" is not the question and never was. An arm aimed straight down whose tip
    lands ON the bed is a tower: it prints from its own end face upward and needs nothing.
    Four arms of equal length aimed down are a four-legged stand, which is why the frame
    search below prefers them to one arm down and everything else hanging. What cannot print
    is an end face that starts with nothing beneath it, and that is what this counts — by
    reading the island mask bed_support() already produced, at the ring of material the tip
    actually has (between the bore and the spigot crest), not at a point on the axis where
    the bore has removed the material.
    """
    n = island.shape[0]
    out = []
    for d, s, kd in zip(arms, stubs, kinds):
        spig_r = arm_pipe(kd, prm)[1] / 2.0 - prm["clearance"]
        r = 0.5 * (spig_r + max(spig_r - prm["spigot_wall"], 0.0))
        ref = np.array([0.0, 0.0, 1.0]) if abs(d[2]) < 0.9 else np.array([1.0, 0, 0])
        e1 = np.cross(d, ref)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(d, e1)
        hit = 0
        for j in range(8):
            a = 2.0 * math.pi * j / 8.0
            p = (base + s - h) * d + r * (math.cos(a) * e1 + math.sin(a) * e2)
            idx = np.clip(np.round((p + ext) / h).astype(int), 0, n - 1)
            hit += bool(island[idx[0], idx[1], idx[2]])
        out.append(hit >= 4)
    return out


# ------------------------------------------------------------------- the print frame --
# The six candidates a landless joint may print in. THE ARTICLE FRAME IS FIRST so that a tie
# keeps the orientation this generator has always used: the search may only move a part when
# it can show the move is worth something.
BED_NORMALS = ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0))
# Cell size of the grid the frame search measures on, mm. The extraction grid is 0.88 mm and
# six orientations of 13 joints at that spacing is minutes inside a gate that has to stay
# runnable. Checked against a 0.98 mm grid over all 13: the coarse search picks the same bed
# normal on 11 and a normal within 0.6% of the best island volume on the other two, which are
# genuine ties. The number the manifest PUBLISHES is measured on the extraction grid, not
# this one — the search ranks, the manifest measures.
PRINT_SEARCH_CELL_MM = 1.6


def _bed_frame(up):
    """Rotation taking the article frame to a print frame in which `up` becomes +z.

    Built from signed unit axes rather than from a normalised cross product, so every arm
    direction stays an exact lattice direction and the elevation census stays exactly
    0, 35.2644, 45 and 90 degrees — the article symmetry P13 checks. A cross product leaves
    1e-16 on those and turns a symmetry check into a tolerance question.
    """
    q = int(np.argmax(np.abs(up)))
    e = np.eye(3)
    z = float(np.sign(up[q])) * e[q]
    x = e[(q + 1) % 3]
    return np.vstack([x, np.cross(z, x), z])


def print_frame(lands, dirs=None, prm=None, base=None, stubs=None, bores=None, kinds=None,
                search_out=None):
    """The orientation the part prints in — a datum chosen, not one inherited by accident.

    A node that HAS a mating land prints on it: the land is a plane through the node's own
    centre, so the whole part lies above it, it is the largest flat the part will ever have,
    and every arm comes out at or above the bed. Nothing here changes for those 38 joints.

    THE DEFECT THIS FIXES is the other 13. An interior lattice node lies on no cell face, so
    it has no land, and this function used to return the identity — the part was emitted in
    the article frame not because that frame was good but because nothing had chosen. What
    that cost, measured on the extraction grid: 11447 mm3 of material across the article that
    could not be built up from the bed, 9 arm ends starting in mid-air, and the centre joint
    standing on 13.2 mm2 of plate with 441 mm3 hanging. Choosing gives 5678, 0, and a centre
    joint on 74.8 mm2 with 8 mm3 hanging.

    THE OBJECTIVE, chosen deliberately and stated so it can be argued with: MINIMISE THE
    MATERIAL THAT CANNOT BE BUILT UP FROM THE BED. Not "minimise downward arms" — that is
    the wrong quantity and choosing it makes the part worse. An arm aimed down whose tip
    reaches the plate is a tower and prints support-free; four equal arms aimed down are a
    four-legged stand. The frames with the FEWEST downward arms are the ones that put a
    single long tree arm straight down, which drops the bed 36 mm below the node and leaves
    every other downward feature hanging in the gap: over the 13 joints, minimising the
    downward count costs 2.5x the island volume for a third fewer arms pointing down, and
    P11 prints both columns off the search this function records. Ties are broken on bed
    contact (adhesion), then on sum cos^2(elevation) — PAHT-CF is 92 MPa in plane and 47 in
    Z, and that cosine is the same weight the allowable is interpolated on, so the last
    tie-break lays the arms into the strong direction.

    The candidates are the six signed axes, and that restriction is not laziness: they are
    the bed normals of the article's own symmetry group, the only ones that leave every arm
    at an elevation the lattice produces. A <111> bed would buy the centre joint one fewer
    downward arm and put 24 arm ends at 54.7 degrees, an elevation this article has never
    had and every direction-dependent allowable would have to be re-argued for.

    `dirs`, `prm`, `base`, `stubs`, `bores` and `kinds` have NO DEFAULTS on purpose. A
    default here is how the next call site quietly gets the identity back and 13 joints go
    out unchosen again — which is exactly how this defect survived two revisions.

    Pass a list as `search_out` and every candidate it measured is appended to it, ranked.
    That is what puts the whole search in the manifest: a chosen orientation whose rejected
    alternatives are not recorded is an assertion, and the counterfactual — what minimising
    downward arms instead would have cost — is then a figure someone has to type.
    """
    if lands:
        n, target = lands[0], np.array([0.0, 0.0, -1.0])
        v = np.cross(n, target)
        s, c = np.linalg.norm(v), float(n @ target)
        if s < 1e-12:
            return np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
        V = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.eye(3) + V + V @ V * ((1 - c) / (s * s))
    if dirs is None or prm is None or base is None or stubs is None or kinds is None:
        raise ValueError(
            "print_frame: this node has no mating land, so there is no datum to inherit. "
            "Pass dirs/prm/base/stubs/bores/kinds and the frame is measured and chosen. "
            "The identity that used to be returned here is what emitted 13 of 51 joints in "
            "the article frame with nothing flat on the bed.")
    ext = max(base + max(stubs) + prm["blend"] + 6.0, 22.0 + prm["stub"])
    res = int(2.0 * ext / PRINT_SEARCH_CELL_MM) | 1
    axis = np.linspace(-ext, ext, res)
    hh = axis[1] - axis[0]
    gx, gy, gz = np.meshgrid(axis, axis, axis, indexing="ij")
    P = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1)
    ranked = []
    for up in BED_NORMALS:
        R = _bed_frame(np.array(up, float))
        arms = [R @ d for d in dirs]
        F3 = node_sdf(P, arms, [], prm, False, base, stubs, bores, kinds).reshape([res] * 3)
        sup = bed_support(F3, hh)
        air = arms_into_air(sup["island"], ext, hh, arms, prm, base, stubs, kinds)
        flat = sum(1.0 - float(a[2]) ** 2 for a in arms)      # sum cos^2(elevation)
        ranked.append(((round(sup["islandVolumeMm3"], 6), -round(sup["bedContactMm2"], 6),
                        -flat),
                       R,
                       {"bedNormalArticle": [int(-x) for x in up],
                        "islandVolumeMm3": round(sup["islandVolumeMm3"], 1),
                        "bedContactMm2": round(sup["bedContactMm2"], 1),
                        "armsIntoAir": int(sum(air)),
                        "downwardArms": sum(1 for a in arms if a[2] < -1e-9)}))
    ranked.sort(key=lambda r: r[0])
    if search_out is not None:
        # Every figure in here is measured on the SEARCH grid, which is coarser than the one
        # the STL comes off; it ranks, it does not publish. The per-node islandVolumeMm3
        # beside it in the manifest is the extraction-grid measurement.
        search_out.extend(r[2] for r in ranked)
    return ranked[0][1]


def write_stl(path, verts, tris, header=b"pink-robotics computed node"):
    with open(path, "wb") as f:
        f.write(header.ljust(80, b" "))
        f.write(_struct.pack("<I", len(tris)))
        for a, b, c in tris:
            va, vb, vc = verts[a], verts[b], verts[c]
            nrm = np.cross(vb - va, vc - va)
            l = np.linalg.norm(nrm)
            f.write(_struct.pack("<12fH", *(nrm / l if l > 0 else nrm), *va, *vb, *vc, 0))


# --------------------------------------------------------------------------- main --
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "research" / "geometry" / "nodes"))
    ap.add_argument("--res", type=int, default=96)
    ap.add_argument("--pipe-od", type=float, default=10.0, help="mm, the main SKU")
    ap.add_argument("--pipe-id", type=float, default=8.0, help="mm, the tube's bore")
    ap.add_argument("--rim-pipe-od", type=float, default=14.0,
                    help="mm, the rim SKU — stock_build's rimOdM, sized by the film's "
                         "dihedral edge, not by crush")
    ap.add_argument("--rim-pipe-id", type=float, default=12.0, help="mm, the rim tube's bore")
    ap.add_argument("--clearance", type=float, default=0.15, help="radial fit gap, mm")
    ap.add_argument("--stub", type=float, default=20.0,
                    help="engagement at a TREE member-end, mm — the ends slid on axially")
    ap.add_argument("--pilot", type=float, default=2.0,
                    help="engagement at a CLOSING member-end, mm — held to the swing-in bound")
    ap.add_argument("--core-r", type=float, default=8.0)
    ap.add_argument("--shoulder", type=float, default=2.0,
                    help="thickness of the seat collar under the pipe's butt, mm")
    ap.add_argument("--lip", type=float, default=2.5,
                    help="depth of the cup over the pipe's cut end, mm (capped by engagement)")
    ap.add_argument("--lip-wall", type=float, default=1.6)
    ap.add_argument("--spigot-wall", type=float, default=2.0)
    ap.add_argument("--blend", type=float, default=4.0, help="smooth-min k, mm")
    ap.add_argument("--ribs", type=int, default=3, help="crush ribs per spigot (0 = none)")
    ap.add_argument("--rib-h", type=float, default=0.25)
    ap.add_argument("--bore-margin", type=float, default=0.4,
                    help="mm a bore mouth must clear a mating land by")
    ap.add_argument("--pad-r", type=float, default=0.0,
                    help="hexagon film pad radius; 0 = none, which is the design "
                         "since the six spokes carry the film on lines instead")
    ap.add_argument("--pad-t", type=float, default=3.0)
    ap.add_argument("--pad-blend", type=float, default=2.5)
    ap.add_argument("--demand-n", type=float, default=3372.0)
    ap.add_argument("--slot-margin", type=float, default=0.5,
                    help="mm of clearance beyond the slot-intersection limit")
    ap.add_argument("--rho", type=float, default=1060.0, help="print density, kg/m3")
    ap.add_argument("--only", type=int, default=None)
    ap.add_argument("--assembly", action="store_true",
                    help="also write the whole article as one STL, in article coordinates")
    args = ap.parse_args()
    prm = vars(args)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    nodes, members, tally = article_graph()
    tree, tree_order = spanning_tree(nodes, members)
    incident = {u: [] for u, _ in nodes}
    for k, (a, b, _fam) in enumerate(members):
        d = np.array(b, float) - np.array(a, float)
        d /= np.linalg.norm(d)
        incident[a].append((d, k))
        incident[b].append((-d, k))

    # THE PILOT IS HELD TO ITS OWN BOUND, not to the default in argparse. Every closing
    # member's cut length is its own, so the shortest one governs; a --pilot that clears 20 mm
    # of travel on the long members and jams on the ties is exactly the fix-that-is-not-a-fix
    # this bound exists to catch.
    def kinds_of(u):
        """Each incident arm's member family — incident[] carries the member INDEX, and the
        family is members[idx][2]. This is what tells a rim vertex that three of its seven
        arms are 14 mm rim tube and four are 10 mm."""
        return [members[k][2] for _, k in incident[u]]

    base_of = {u: slot_base([d for d, _ in incident[u]], prm, kinds_of(u))[0]
               for u, _ in nodes}

    # THE EXTRACTION WINDOW IS DERIVED, NOT ASSUMED. It used to be a formula in core_r,
    # shoulder and stub that happened to exceed the reach every node needed. Giving the rim its
    # real 14 mm tube pushed the worst slot base from 16.38 mm to 18.98, the part then reached
    # 42.98 mm against a 42 mm window, and surface nets returned a mesh clipped at the boundary
    # — reported honestly as OPEN, which is how this was caught. The window now follows the
    # largest base the node rule actually produces, so any future change to a tube, an angle or
    # the graph carries its own grid with it.
    ext = max(max(base_of.values()) + args.stub + args.blend + 6.0,
              args.pad_r + 4.0, 22.0 + args.stub)
    axis = np.linspace(-ext, ext, args.res)
    h = axis[1] - axis[0]
    gx, gy, gz = np.meshgrid(axis, axis, axis, indexing="ij")
    P = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1)
    cuts = {}
    for k, (a, b, _fam) in enumerate(members):
        L = float(np.linalg.norm((np.array(b, float) - np.array(a, float)) * HALF))
        cuts[k] = L - base_of[a] - base_of[b]
    worst_cut = min(cuts[k] for k in range(len(members)) if k not in tree)
    s_max = pilot_bound(worst_cut, 2.0 * args.clearance)
    if args.pilot > s_max:
        sys.exit(f"gen_nodes: --pilot {args.pilot:.2f} mm exceeds the swing-in bound "
                 f"{s_max:.3f} mm on the shortest closing cut ({worst_cut:.2f} mm). A closing "
                 f"member cannot be tilted into a socket deeper than that.")

    # THE JOINT, CHECKED — "will we have sufficient holdage?" answered with arithmetic, and
    # now answered twice, because the two engagements are two different joints.
    F = args.demand_n
    spig_r = args.pipe_id / 2 - args.clearance
    sect = math.pi * (spig_r ** 2 - max(spig_r - args.spigot_wall, 0.0) ** 2)
    seat = math.pi * ((args.pipe_od / 2) ** 2 - (args.pipe_id / 2) ** 2)

    def glue_of(s):
        # both surfaces bond: the pipe's bore over the spigot and its outside inside the cup
        return (math.pi * args.pipe_id * s
                + math.pi * args.pipe_od * min(args.lip, s))

    joint = {"capture": "internal pilot plus an external cup (the pipe is captured on both "
                        "faces and butts on a full-width seat)",
             "perStrutDemandN": F,
             "treeEndsMm": args.stub, "closingEndsMm": args.pilot,
             "closingPilotBoundMm": round(s_max, 3),
             "glueAreaTreeMm2": round(glue_of(args.stub)),
             "glueAreaClosingMm2": round(glue_of(args.pilot)),
             "glueShearTreeMPa": round(F / glue_of(args.stub), 2),
             "glueShearClosingMPa": round(F / glue_of(args.pilot), 2),
             "glueMarginAt10MPa": round(10.0 * glue_of(args.pilot) / F, 1),
             "glueAreaMm2": round(glue_of(args.pilot)),
             "glueShearMPa": round(F / glue_of(args.pilot), 2),
             "spigotSectionMm2": round(sect, 1),
             "spigotStressMPa": round(F / sect, 1),
             "shoulderBearingMPa": round(F / seat, 1),
             "note": "axial load rides the seat and the glue line, not the spigot's own "
                     "section; the seat is now the full pipe annulus rather than a blend "
                     "fillet, which is what makes that sentence true. A uniformly evacuated "
                     "shell is all compression, so E5 crushes one joint DRY and one GLUED "
                     "and the dry result decides whether adhesive is needed at all — and it "
                     "must crush one of each ENGAGEMENT, because a closing end is a "
                     f"{args.pilot:.0f} mm pilot in a {min(args.lip, args.pilot):.0f} mm cup "
                     "and a tree end is not"}
    manifest = {"paramsMm": {k: prm[k] for k in
                             ("pipe_od", "pipe_id", "rim_pipe_od", "rim_pipe_id",
                              "clearance", "stub", "pilot", "core_r",
                              "shoulder", "lip", "lip_wall", "spigot_wall", "blend",
                              "ribs", "rib_h", "bore_margin", "pad_r", "pad_t")},
                "graph": tally, "jointCheck": joint, "res": args.res,
                "cellMm": round(h, 3),
                "assembly": {"closingMembers": len(members) - len(tree),
                             "treeMembers": len(tree),
                             "closingEnds": 2 * (len(members) - len(tree)),
                             "shortestClosingCutMm": round(worst_cut, 3),
                             "pilotBoundMm": round(s_max, 3),
                             "rule": "spanning_tree(): BFS from the first node in graph order; "
                                     "a member that discovers a new node keeps the full stub, "
                                     "every other member gets the pilot at both ends"},
                "nodes": []}
    print(f"graph: {tally}, {len(nodes)} nodes; {len(tree)} tree / "
          f"{len(members) - len(tree)} closing members, pilot {args.pilot:.1f} mm against a "
          f"{s_max:.2f} mm bound; joint: glue {joint['glueShearClosingMPa']} MPa at a closing "
          f"end, seat bearing {joint['shoulderBearingMPa']} MPa")

    cut_rows = collections.Counter()
    for k, (a, b, fam) in enumerate(members):
        cut_rows[(fam, round(cuts[k], 3))] += 1

    total, asm_v, asm_t = 0.0, [], []
    todo = list(enumerate(nodes)) if args.only is None else [
        list(enumerate(nodes))[args.only]]
    for i, (u, role) in todo:
        dirs = [d for d, _ in incident[u]]
        kinds = kinds_of(u)
        base, min_ang, need = slot_base(dirs, prm, kinds)
        lands = face_planes(u)
        # stubs and bores are needed BEFORE the frame now: a landless node has no land to
        # print on, so its datum is chosen by measuring the part, and the part is not defined
        # until the per-arm engagement and bore starts are.
        stubs = [args.stub if k in tree else args.pilot for _, k in incident[u]]
        bores = [bore_start(d, lands, prm, kd) for d, kd in zip(dirs, kinds)]
        search = []
        R = print_frame(lands, dirs, prm, base, stubs, bores, kinds, search)
        arms = [R @ d for d in dirs]
        lands_p = [R @ n for n in lands]
        F3 = node_sdf(P, arms, lands_p, prm, role == "hexHub",
                      base, stubs, bores, kinds).reshape([args.res] * 3)
        v, t = surface_nets(F3, np.array([-ext] * 3), h)
        for n in lands_p:                       # snap: the plane is known exactly
            dist = v @ n
            near = np.abs(dist) < h * 0.75
            v[near] -= np.outer(dist[near], n)
        closed, nonman = mesh_health(t)
        vol = mesh_volume(v, t)
        g = vol * 1e-9 * args.rho * 1000.0
        total += g
        # PRINTABILITY, MEASURED ON THE FIELD THIS MESH CAME OUT OF — not on the coarse grid
        # print_frame ranked orientations with, and not as a fraction of anything.
        sup = bed_support(F3, h)
        air = arms_into_air(sup["island"], ext, h, arms, prm, base, stubs, kinds)
        name = f"node_{i:02d}_{role}.stl"
        write_stl(out / name, v, t)
        if args.assembly:
            # `off`, not `base`: this used to rebind the slot start to the running vertex
            # count, and every manifest row written by an --assembly run recorded that
            # instead. The STLs were fine and nothing downstream could tell.
            off = len(asm_v)
            world = v @ R + np.array(u, float) * HALF     # R is orthonormal: R^T = R^-1
            asm_v.append(world)
            asm_t.append(t + off)
        manifest["nodes"].append({
            "file": name, "u": list(u), "role": role, "arms": len(arms),
            "lands": len(lands), "triangles": int(len(t)), "closed": closed,
            "nonManifoldEdges": nonman, "overhangAreaFrac": round(overhang_fraction(v, t), 3),
            "minArmAngleDeg": round(min_ang, 1), "slotBaseMm": round(base, 2),
            "slotsClear": bool(base >= need - 1e-9),
            "armEngagementMm": [round(s, 3) for s in stubs],
            "armIsClosing": [bool(k not in tree) for _, k in incident[u]],
            "armBoreStartMm": [round(b, 3) for b in bores],
            # THE PRINT DATUM AND WHAT IT BOUGHT. bedNormalArticle is which way is down, in
            # article coordinates — a land normal on the 38 joints that have one, a measured
            # choice on the 13 that do not. The three figures beside it are the ones that
            # decide the print; armsIntoAir is the honest form of "downward arm", counting
            # only the ends that start with nothing under them.
            "bedNormalArticle": [round(float(x), 6) for x in -R[2]],
            "bedContactMm2": round(sup["bedContactMm2"], 1),
            "supportAreaMm2": round(sup["supportAreaMm2"], 1),
            "islandVolumeMm3": round(sup["islandVolumeMm3"], 1),
            "armsIntoAir": int(sum(air)),
            # THE ORIENTATIONS THAT WERE REJECTED, with what each would have cost. Empty on
            # the 38 joints that print on a mating land, where there is nothing to choose.
            "frameSearch": search,
            "armIntoAir": [bool(x) for x in air],
            "armElevationDeg": [round(math.degrees(math.asin(
                max(-1.0, min(1.0, float(a[2]))))), 4) for a in arms],
            "volumeMm3": round(vol), "massG": round(g, 2)})
        print(f"  {name}: {len(arms):2d} arms, {len(lands)} lands, {len(t):6d} tris, "
              f"{'closed' if closed else 'OPEN':6s} ({nonman:3d} saddle), "
              f"bed {sup['bedContactMm2']:5.1f} mm2, island "
              f"{sup['islandVolumeMm3']:6.1f} mm3 ({sum(air)} arms in air), {g:5.1f} g")

    manifest["totalNodeMassKg"] = round(total / 1000.0, 3)
    # The cut list is geometry, so it belongs to the generator: cut = L - base_A - base_B, and
    # the bases are per node. stock_build used to publish the centre-to-centre member lengths
    # as cuts and bill tube against them; it reads this instead.
    manifest["cutList"] = [
        {"family": f, "cutMm": c, "count": n,
         "swingReliefMm": swing_relief(c, prm, f),
         "closingCutMm": round(c - 2.0 * swing_relief(c, prm, f), 3),
         "basis": "cutMm is the seat-to-seat gap and is what a TREE member is cut to. A "
                  "CLOSING member is cut closingCutMm, shorter by swing_relief() at each end, "
                  "because its own end-face corner has to clear the seat while it is rotated "
                  "in; the space that leaves is a bondline, not a butt. The relief is derived "
                  "from THIS row's own tube — the rim's 14 mm corner swings deeper than the "
                  "10 mm one on the same length — so it is a per-family figure, not a global "
                  "one."}
        for (f, c), n in sorted(cut_rows.items())]
    manifest["cutTotalM"] = round(sum(c * n for (_, c), n in cut_rows.items()) / 1000.0, 3)
    # THE PRINTABILITY ROLL-UP, so a regression is one number away rather than 51. It is a
    # sum and not an average: averaging island volume over 51 joints is how a fraction hid
    # this defect in the first place.
    rows = manifest["nodes"]
    manifest["printability"] = {
        "islandVolumeMm3": round(sum(r["islandVolumeMm3"] for r in rows), 1),
        "nodesWithIslandOver10Mm3": sum(1 for r in rows if r["islandVolumeMm3"] > 10.0),
        "armsIntoAir": sum(r["armsIntoAir"] for r in rows),
        "minBedContactMm2": round(min(r["bedContactMm2"] for r in rows), 1),
        "supportAreaMm2": round(sum(r["supportAreaMm2"] for r in rows), 1),
        "searchCellMm": round(PRINT_SEARCH_CELL_MM, 3),
        "rule": "a node with a mating land prints on it; a node without one is oriented by "
                "measuring all six lattice bed normals and taking the least island volume, "
                "then the most bed contact, then the most sum cos^2(elevation). Island "
                "volume is material that cannot be built up from the bed at 45 degrees per "
                "layer — measured here on the extraction grid, not on the coarser grid the "
                "search ranks with."}
    manifest["note"] = ("measured by integrating each joint's own SDF over the mesh that "
                        "was written — this retires NODE_MASS_FRAC at article scale")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    if args.assembly and asm_v:
        write_stl(out / "article.stl", np.vstack(asm_v), np.vstack(asm_t),
                  b"pink-robotics article: 51 computed joints in place")
        print(f"wrote article.stl ({sum(len(t) for t in asm_t)} triangles)")
    bad = [r["file"] for r in manifest["nodes"] if not r["closed"]]
    pr = manifest["printability"]
    print(f"wrote {len(manifest['nodes'])} nodes, {total:.0f} g total at rho={args.rho:.0f}"
          f"; {'ALL CLOSED' if not bad else 'OPEN: ' + str(bad)}")
    print(f"printability: {pr['islandVolumeMm3']:.0f} mm3 of island on "
          f"{pr['nodesWithIslandOver10Mm3']} joints, {pr['armsIntoAir']} arm ends starting in "
          f"air, least bed contact {pr['minBedContactMm2']:.1f} mm2")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
