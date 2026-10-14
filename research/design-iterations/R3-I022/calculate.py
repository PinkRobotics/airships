#!/usr/bin/env python3
"""One fixed paired-rack proposal. Necessary loads, not an equilibrium solution.

Only the standard library is used. Predecessor numerical outputs are read from
the pinned extract; no predecessor calculator or suspension suite is executed.
"""
import hashlib
import json
from math import acos, ceil, cos, exp, pi, sin, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_SHA = "94e002ca1e976434509d5850ca557773120cd35553cdc38ace849e22b46580d2"
assert hashlib.sha256((HERE / "baseline.json").read_bytes()).hexdigest() == BASE_SHA
B = json.loads((HERE / "baseline.json").read_text())
GEO = B["geometry"]
R, RB = GEO["radius_m"], GEO["bag_radius_m"]
G = 9.80665
HOSTS = (9, 10, 11, 12, 16, 21, 22, 23)
LANES = {9: -1.8, 10: -.6, 11: .6, 12: 1.8,
         16: -1.8, 21: -.6, 22: .6, 23: 1.8}
ROPE_D, ROPE_R = .018, .035  # rope and finite clamp/chafe envelope
ROPE_A = pi * ROPE_D**2 / 4
EA, MU = 50e9 * ROPE_A, 1440 * ROPE_A + .2
BEND_R, GUARD_R = .45, .60
TRAVEL = .20  # declared hardware and separate bag displacement envelopes, each
RHO_AL = 2700.


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def mul(a, s): return tuple(x*s for x in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def norm(a): return sqrt(dot(a, a))
def unit(a): return mul(a, 1/norm(a))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def mean(a, b): return mul(add(a, b), .5)
def clamp(x, a=0., b=1.): return min(b, max(a, x))


def point_segment(c, a, b):
    d = sub(b, a)
    t = clamp(dot(sub(c, a), d)/dot(d, d)) if dot(d, d) else 0.
    p = add(a, mul(d, t))
    return norm(sub(p, c)), p, t


def segment_segment(a, b, c, d):
    """Exact closest points of two finite straight segments, including ends."""
    u, v, w = sub(b, a), sub(d, c), sub(a, c)
    aa, bb, cc, dd, ee = dot(u, u), dot(u, v), dot(v, v), dot(u, w), dot(v, w)
    candidates = []
    for p, s in ((a, 0.), (b, 1.)):
        dist, q, t = point_segment(p, c, d); candidates.append((dist, p, q, s, t))
    for q, t in ((c, 0.), (d, 1.)):
        dist, p, s = point_segment(q, a, b); candidates.append((dist, p, q, s, t))
    den = aa*cc-bb*bb
    if den > 1e-14*aa*cc:
        s, t = (bb*ee-cc*dd)/den, (aa*ee-bb*dd)/den
        if 0 <= s <= 1 and 0 <= t <= 1:
            p, q = add(a, mul(u, s)), add(c, mul(v, t))
            candidates.append((norm(sub(p, q)), p, q, s, t))
    return min(candidates, key=lambda x: x[0])


def bend(a, p, b):
    u, v = unit(sub(p, a)), unit(sub(b, p))
    theta = acos(clamp(dot(u, v), -1., 1.))
    tangent = BEND_R*sin(theta/2)/cos(theta/2)
    n = unit(sub(v, mul(u, cos(theta))))
    entry, leave = sub(p, mul(u, tangent)), add(p, mul(v, tangent))
    centre = add(entry, mul(n, BEND_R))
    points = [add(centre, mul(add(mul(n, -cos(theta*k/16)), mul(u, sin(theta*k/16))), BEND_R)) for k in range(17)]
    assert norm(sub(points[0], entry)) < 1e-10 and norm(sub(points[-1], leave)) < 1e-10
    return {"intersection": p, "centre": centre, "entry": entry, "exit": leave,
            "u_in": u, "u_out": v, "axis": unit(cross(u, v)), "angle_rad": theta,
            "radius_m": BEND_R, "arc_length_m": BEND_R*theta, "points": points,
            "chord_error_m": BEND_R*(1-cos(theta/32)), "tangent_m": tangent}


def routes():
    result = []
    for i in HOSTS:
        h = GEO["hangers"][i]; bag = h["bag"]; s = -1 if bag == 1 else 1
        normal = unit(sub(h["low"], GEO["bag_centres"][bag]))
        eye = add(h["low"], mul(normal, .15))
        p, q = (LANES[i], s*29., 4.), (LANES[i], s*29., 22.5)
        top = h["top"]
        direction = unit(sub(top, q))
        # Original nominal one-metre actuator, now swivelled into this direction.
        rope_top = sub(top, direction)
        bends = [bend(eye, p, q), bend(p, q, rope_top)]
        straight = [(eye, bends[0]["entry"]), (bends[0]["exit"], bends[1]["entry"]), (bends[1]["exit"], rope_top)]
        lengths = [norm(sub(b, a)) for a, b in straight]
        assert all(x > 0 for x in lengths)
        length = sum(lengths)+sum(x["arc_length_m"] for x in bends)
        # A stock cut rule fixed from unloaded geometry, never adjusted by load.
        free = ceil(length/.5)*.5
        result.append({"host": i, "bag": bag, "rack": s, "original_low": h["low"],
                       "original_top": top, "eye": eye, "normal": normal,
                       "bends": bends, "segments": straight, "segment_lengths_m": lengths,
                       "geometric_rope_length_m": length, "new_free_length_m": free,
                       "paid_length_with_two_tails_m": free+2.,
                       "old_free_length_m": B["bag_free_lengths_m"][i],
                       "total_path_including_nominal_actuator_m": length+1.})
    return result


ROUTES = routes()


def construction():
    parts, objects = [], []

    def capsule(name, a, b, radius, role, rack=0, host=None):
        objects.append({"id": name, "a": a, "b": b, "radius_m": radius, "role": role, "rack": rack, "host": host})

    def part(name, mass, volume, location, group, rack=0, role="rack"):
        parts.append({"id": name, "mass_kg": mass, "solid_volume_m3": volume,
                      "cg": location, "group": group, "rack": rack, "role": role})

    def member(name, a, b, width, wall, group, rack):
        area = width**2-(width-2*wall)**2; length = norm(sub(b, a))
        part(name, area*length*RHO_AL, area*length, mean(a, b), group, rack)
        capsule(name, a, b, width/sqrt(2), "frame", rack)

    roots = {}
    for s in (-1, 1):
        tag = f"rack{s:+d}"
        # A 4.8 x 0.9 x 23 m space frame: four posts and five tied levels.
        levels = (0., 5.75, 11.5, 17.25, 23.)
        corners = [(x, s*29.+dy) for x in (-2.4, 2.4) for dy in (-.45, .45)]
        for k, (x, y) in enumerate(corners):
            member(f"{tag}-post{k}", (x,y,0.), (x,y,23.), .2,.006,"rack_RHS_200x200x6",s)
        for j,z in enumerate(levels):
            for k,(a,b) in enumerate(((0,1),(1,3),(3,2),(2,0))):
                member(f"{tag}-tie{j}-{k}", (*corners[a],z), (*corners[b],z), .2,.006,"rack_RHS_200x200x6",s)
        for j,(z0,z1) in enumerate(zip(levels,levels[1:])):
            for k,(a,b) in enumerate(((0,1),(1,3),(3,2),(2,0))):
                # Both diagonals are paid and geometrically represented.
                for n,(c,d) in enumerate(((a,b),(b,a))):
                    member(f"{tag}-brace{j}-{k}-{n}", (*corners[c],z0),(*corners[d],z1),.1,.004,"rack_RHS_100x100x4",s)
        for z in (4.,22.5):
            member(f"{tag}-guide-beam{z}",(-2.4,s*29.,z),(2.4,s*29.,z),.2,.006,"guide_crossbeams",s)
            for x in (-2.4,2.4):
                for dy in (-.45,.45):
                    member(f"{tag}-beam-end{z}-{x}-{dy}",(x,s*29.,z),(x,s*29.+dy,z),.2,.006,"guide_crossbeam_post_links",s)
        roots[s] = []
        for k,(x,z) in enumerate(((-2.4,0.),(2.4,0.),(-2.4,23.),(2.4,23.))):
            root=(x,s*29.,z)
            # Eight new pads, inboard of the hull; no inherited free reaction.
            anchor=(5.*(1 if x>0 else -1),s*sqrt((R-.10)**2-25-z*z),z)
            length=norm(sub(anchor,root)); width=.15; wall=.006
            member(f"{tag}-root-strut{k}",root,anchor,width,wall,"root_RHS_150x150x6",s)
            # Root plate + two clevis plates, pins and bonded pad are separate.
            plate_volume=.5*.5*.02+2*.25*.25*.02
            part(f"{tag}-plate-pin{k}",plate_volume*2700+12.,plate_volume+12/7850.,anchor,"root_plates_pins",s,"anchor")
            capsule(f"{tag}-pad{k}",anchor,anchor,.37,"hull_attachment",s)
            target=GEO["hangers"][[9,10,11,12][k] if s<0 else [16,21,22,23][k]]["top"]
            # 1 m wide, 8 mm laminate curtain along the actual inner skin arc.
            u,v=unit(anchor),unit(target); ang=acos(clamp(dot(u,v),-1,1)); rad=R-.1
            pts=[mul(add(mul(u,sin((1-t/32)*ang)),mul(v,sin(t/32*ang))),rad/sin(ang)) for t in range(33)]
            length_c=rad*ang; vol=length_c*1.*.008*1.2
            arc_cg=mul(add(u,v),rad*sin(ang)/(ang*(1+cos(ang))))
            part(f"{tag}-curtain{k}",vol*1400.,vol,arc_cg,"curtain_and_bond_20pct",s,"shell")
            chord_error=rad*(1-cos(ang/64))
            for n,(a,b) in enumerate(zip(pts,pts[1:])):
                capsule(f"{tag}-curtain{k}-{n}",a,b,.5+chord_error,"hull_attachment",s)
            # K values are unqualified construction assumptions, used as limits.
            inertia=(width**4-(width-2*wall)**4)/12
            beam_k=3*70e9*inertia/length**3
            effective_k=1/(1/beam_k+1/5e5+1/2e5)
            roots[s].append({"root":root,"pad":anchor,"curtain_end":target,"length_m":length,
                             "beam_lateral_k_n_m":beam_k,"curtain_k_n_m":5e5,
                             "joint_k_n_m":2e5,"effective_k_n_m":effective_k,
                             "assumed_rotational_k_nm_rad":2e5,"second_moment_m4":inertia})
        # Explicit finite stocks for joints, access and erection: no massless rack.
        for k,z in enumerate(levels):
            part(f"{tag}-joints{k}",40.,40/2700.,(0.,s*29.,z),"frame_joints",s)
            capsule(f"{tag}-jointbox{k}",(0.,s*29.,z),(0.,s*29.,z),.25,"frame",s)
        part(f"{tag}-erection-access",80.,80/2700.,(0.,s*29.,11.5),"erection_access",s)
        capsule(f"{tag}-access",(0.,s*29.,0.),(0.,s*29.,23.),.15,"frame",s)

    for row in ROUTES:
        i,s=row["host"],row["rack"]
        for j,(a,b) in enumerate(row["segments"]): capsule(f"rope{i}-straight{j}",a,b,ROPE_R,"rope",s,i)
        for j,be in enumerate(row["bends"]):
            for k,(a,b) in enumerate(zip(be["points"],be["points"][1:])):
                capsule(f"rope{i}-arc{j}-{k}",a,b,ROPE_R+be["chord_error_m"],"rope",s,i)
            centre=be["centre"]
            capsule(f"guide{i}-{j}-guard",centre,centre,GUARD_R,"guard",s,i)
            # 900 mm pitch diameter, two flanges, hub, 60 mm steel axle,
            # two separately priced bearings and 20 mm saddle plates.
            rim_volume=pi*(.49**2-.41**2)*.06+2*pi*(.51**2-.41**2)*.008
            axle_volume=pi*.06**2/4*.22
            plate_volume=2*.24*.30*.02
            mass=rim_volume*2700+axle_volume*7850+plate_volume*2700+2*4.+6.+8.
            vol=rim_volume+axle_volume+plate_volume+22/2700.
            part(f"guide{i}-{j}",mass,vol,centre,"sheaves_axles_bearings_guards_saddles",s)
            member(f"guide{i}-{j}-arm",be["intersection"],centre,.1,.004,"guide_support_arms",s)
        # Complete rope is paid as new stock. Existing penetrations cannot yet
        # be retired; their ropes are not credited or counted as this stock.
        first_moment=(0.,0.,0.)
        for (a,b),length in zip(row["segments"],row["segment_lengths_m"]):
            first_moment=add(first_moment,mul(mean(a,b),length))
        for be in row["bends"]:
            theta=be["angle_rad"]
            n=unit(sub(be["centre"],be["entry"]))
            arc_cg=add(be["centre"],mul(add(mul(n,-sin(theta)/theta),mul(be["u_in"],(1-cos(theta))/theta)),BEND_R))
            first_moment=add(first_moment,mul(arc_cg,be["arc_length_m"]))
        extra=row["paid_length_with_two_tails_m"]-row["geometric_rope_length_m"]
        first_moment=add(first_moment,mul(mean(row["eye"],row["segments"][-1][1]),extra))
        part(f"rope{i}",MU*row["paid_length_with_two_tails_m"],(ROPE_A+.2/1000)*row["paid_length_with_two_tails_m"],mul(first_moment,1/row["paid_length_with_two_tails_m"]),"new_eight_ropes",s,"rope")
        for end,pt in (("lower",row["eye"]),("upper",row["original_top"])):
            part(f"rope{i}-{end}-termination",12.,12/2700.,pt,"rope_sockets_swivels",s,"bag" if end=="lower" else "anchor")
            capsule(f"rope{i}-{end}-socket",pt,pt,.12,"bag_attachment" if end=="lower" else "hull_attachment",s,i)
        # The two-leg lower bridle uses original cradle-band points +/- .25 m
        # along the latitude circle. It does not create a new free bag anchor.
        low=row["original_low"]; centre=GEO["bag_centres"][row["bag"]]
        tangent=unit((-(low[1]-centre[1]),low[0]-centre[0],0.))
        for j,sign in enumerate((-1,1)):
            trial=add(low,mul(tangent,sign*.25)); lug=add(centre,mul(unit(sub(trial,centre)),RB))
            capsule(f"bridle{i}-{j}",lug,row["eye"],.055,"bag_attachment",s,i)
        part(f"bridle{i}",20.,20/2700.,low,"bridle_pins_bands_doublers",s,"bag")
        # Retention ledger pays a second identical actuator: no double-use of
        # the actuator still required by the unretired old penetration.
        act=B["bag_adjuster"]
        oil=act["parts_kg"]["contained_oil"]
        part(f"actuator{i}",act["mass_kg"],(act["mass_kg"]-oil)/7850.+oil/850.,mean(row["segments"][-1][1],row["original_top"]),"new_eight_same_selected_actuators",s,"anchor")
        capsule(f"actuator{i}",row["segments"][-1][1],row["original_top"],.06,"actuator",s,i)
    return parts,objects,roots


PARTS, OBJECTS, ROOTS = construction()


def fixed_objects():
    result=[]
    def put(name,a,b,r,category): result.append({"id":name,"a":a,"b":b,"radius_m":r,"category":category})
    for i,h in enumerate(GEO["hangers"]):
        put(f"old-hanger{i}",h["low"],h["top"],.12 if i in HOSTS else .035,"retained_hangers_and_liners")
    for d in B["ducts"]:
        for j,(a,b) in enumerate(zip(d["points"],d["points"][1:])):
            put(f"duct{d['bag']}-{j}",a,b,.5*1.0300645387285057+.001,"pressure_branches")
    for name,h in B["headers"].items():
        u=(1/sqrt(2),-1/sqrt(2),0.) if name=="L12" else (1.,0.,0.)
        put(f"header-{name}",sub(h["centre"],mul(u,h["length_m"]/2)),add(h["centre"],mul(u,h["length_m"]/2)),h["diameter_m"]/2+.002,"headers")
        # Old stub azimuths unspecified: circumscribed finite volume covers
        # the two-metre stubs, valve bodies and nearby mount frame.
        put(f"header-{name}-stub-bound",h["centre"],h["centre"],h["length_m"]/2+3.,"header_stub_bounds")
    for line in B["main_layout"]:
        bound=B["main_saved_curve_enclosures"][line["id"]]["radius_m"]
        put(f"main{line['id']}",line["low"],line["anchor"],bound,"main_saved_curve_enclosures")
    for k,pt in enumerate(GEO["modules"]):
        put(f"service-frame{k}",add(pt,(0,0,-1.9)),add(pt,(0,0,1.9)),sqrt(2)*1.6,"service_frame_bounds")
    return result


FIXED = fixed_objects()


def geometry_screen():
    bags=[]; hull=[]; fixed=[]
    for obj in OBJECTS:
        for b,c in enumerate(GEO["bag_centres"]):
            dist,p,t=point_segment(c,obj["a"],obj["b"])
            gap=dist-RB-obj["radius_m"]
            bags.append({"object":obj["id"],"role":obj["role"],"host":obj["host"],"bag":b,
                         "gap_m":gap,"gap_with_declared_motion_m":gap-2*TRAVEL,
                         "closest_axis_point":p,"bag_centre":c,"segment_fraction":t,
                         "axis_radius_m":obj["radius_m"],"object_a":obj["a"],"object_b":obj["b"],
                         "intended_own_attachment":obj["role"]=="bag_attachment" and obj["host"] is not None and GEO["hangers"][obj["host"]]["bag"]==b})
        p=max((obj["a"],obj["b"]),key=norm)
        hull.append({"object":obj["id"],"gap_m":R-norm(p)-obj["radius_m"],
                     "closest_axis_point":p,"radius_m":obj["radius_m"],
                     "hull_attachment":obj["role"]=="hull_attachment"})
        # Save the governing finite closest points in every fixed-object class.
        by_category={}
        for other in FIXED:
            dist,p,q,t,u=segment_segment(obj["a"],obj["b"],other["a"],other["b"])
            gap=dist-obj["radius_m"]-other["radius_m"]
            result={"object":obj["id"],"fixed_object":other["id"],"category":other["category"],"gap_m":gap,
                    "gap_with_hardware_motion_m":gap-TRAVEL,"new_point":p,"fixed_point":q,
                    "new_radius_m":obj["radius_m"],"fixed_radius_m":other["radius_m"],
                    "new_fraction":t,"fixed_fraction":u}
            if other["category"] not in by_category or gap<by_category[other["category"]]["gap_m"]:
                by_category[other["category"]]=result
        fixed.extend(by_category.values())
    ropes=[o for o in OBJECTS if o["role"]=="rope"]
    pairs=[]
    for k,i in enumerate(HOSTS):
        for j in HOSTS[k+1:]:
            closest=None
            for a in (o for o in ropes if o["host"]==i):
                for b in (o for o in ropes if o["host"]==j):
                    dist,p,q,_,_=segment_segment(a["a"],a["b"],b["a"],b["b"])
                    gap=dist-a["radius_m"]-b["radius_m"]
                    r={"hosts":[i,j],"gap_m":gap,"gap_with_declared_motion_m":gap-2*TRAVEL,"objects":[a["id"],b["id"]],"points":[p,q]}
                    if closest is None or gap<closest["gap_m"]: closest=r
            pairs.append(closest)
    guards=[o for o in OBJECTS if o["role"]=="guard"]
    guard_pairs=[]
    for i,a in enumerate(guards):
        for b in guards[:i]:
            guard_pairs.append({"objects":[a["id"],b["id"]],"gap_m":norm(sub(a["a"],b["a"]))-a["radius_m"]-b["radius_m"],"points":[a["a"],b["a"]]})
    rope_hardware=[]
    for i in HOSTS:
        by_role={}
        for a in (o for o in ropes if o["host"]==i):
            for b in (o for o in OBJECTS if o["role"]!="rope" and o["host"]!=i):
                dist,p,q,_,_=segment_segment(a["a"],a["b"],b["a"],b["b"])
                gap=dist-a["radius_m"]-b["radius_m"]
                row={"host":i,"objects":[a["id"],b["id"]],"role":b["role"],"gap_m":gap,"points":[p,q],"radii_m":[a["radius_m"],b["radius_m"]]}
                if b["role"] not in by_role or gap<by_role[b["role"]]["gap_m"]: by_role[b["role"]]=row
        rope_hardware.extend(by_role.values())
    actual_lower=[r for r in bags if r["role"]=="rope" and r["object"].endswith("straight0") and GEO["hangers"][r["host"]]["bag"]==r["bag"]]
    foreign=[r for r in bags if r["role"] in ("rope","guard","actuator") and r["bag"] in (0,3)]
    return {"bags":bags,"hull":hull,"fixed":fixed,"rope_pairs":pairs,"guard_pairs":guard_pairs,"rope_to_new_hardware":rope_hardware,
            "lower_legs_to_own_full_bags":actual_lower,"foreign_upper_min":min(foreign,key=lambda r:r["gap_m"]),
            "minimum_new_rope_pair":min(pairs,key=lambda r:r["gap_m"]),
            "minimum_guard_pair":min(guard_pairs,key=lambda r:r["gap_m"]),
            "motion_each_m":TRAVEL,"full_bag_retirement_gate":False,
            "reason":"Lower ropes intersect their own full envelopes. Force/travel compliance cannot establish the declared motion envelope. No penetration retirement is authorized by this calculation."}


def load_case(state, new_construction):
    bag_loads=list(state["supported_bag_masses_kg"])
    rows=[]; rackloads={-1:[],1:[]}; bagforce=[(0.,0.,0.) for _ in range(4)]; bagmoment=[(0.,0.,0.) for _ in range(4)]
    for row in ROUTES:
        i,b,s=row["host"],row["bag"],row["rack"]
        directions=[unit(sub(q,p)) for p,q in row["segments"]]
        # Necessary full-load demand, had the old eight load paths been removed.
        # All new rope gravity is explicitly allocated to adjacent endpoints.
        extra=row["paid_length_with_two_tails_m"]-row["geometric_rope_length_m"]
        rope_end_mass=MU*(row["segment_lengths_m"][0]+extra)/2
        lower_fitting_mass=20.+12.
        vertical=bag_loads[b]*G/8+(rope_end_mass+lower_fitting_mass)*G
        tension=vertical/directions[0][2]
        lower=mul(directions[0],tension)
        bagforce[b]=add(bagforce[b],lower)
        bagmoment[b]=add(bagmoment[b],cross(sub(row["eye"],GEO["bag_centres"][b]),lower))
        guides=[]
        for j,be in enumerate(row["bends"]):
            traction=mul(sub(be["u_out"],be["u_in"]),tension)
            guide_mass=next(p["mass_kg"] for p in PARTS if p["id"]==f"guide{i}-{j}")
            gravity_mass=MU*(row["segment_lengths_m"][j]/2+row["segment_lengths_m"][j+1]/2+be["arc_length_m"])+guide_mass
            # Guide deadweight is included here, so excluded from PARTS below.
            force=add(traction,(0,0,-gravity_mass*G))
            moment=cross(sub(be["centre"],be["intersection"]),force)
            # A 0.02 bearing friction coefficient is only a rating requirement.
            bearing_torque=.02*norm(traction)*.03
            guides.append({"guide":j,"force_on_guide_n":force,"rope_traction_n":traction,
                           "axle_bending_limit_nm":1.5*norm(force)*.12/4,
                           "two_bearings_limit_each_n":1.5*norm(force)/2,
                           "60mm_axle_bending_mpa":1.5*norm(force)*.12/4/(pi*.06**3/32)/1e6,
                           "saddle_moment_nm":moment,"bearing_torque_requirement_nm":bearing_torque,
                           "friction_tension_difference_bound_n":bearing_torque/BEND_R})
            rackloads[s].append((be["centre"],force))
        topforce=mul(directions[-1],-tension)
        top_dead=MU*(row["segment_lengths_m"][-1]+extra)/2+12.+B["bag_adjuster"]["mass_kg"]
        top_total=add(topforce,(0.,0.,-top_dead*G))
        top_rope_gravity=MU*(row["segment_lengths_m"][-1]+extra)/2*G
        top_moment=add(cross(sub(row["segments"][-1][1],row["original_top"]),add(topforce,(0.,0.,-top_rope_gravity))),
                       cross(sub(mean(row["segments"][-1][1],row["original_top"]),row["original_top"]),(0.,0.,-B["bag_adjuster"]["mass_kg"]*G)))
        # Two pin-linked bridle legs: solve only their local two-vector
        # projection. Any third-direction residual remains an unmet force.
        legs=[o for o in OBJECTS if o["id"].startswith(f"bridle{i}-")]
        d1,d2=[unit(sub(o["a"],row["eye"])) for o in legs]
        c=dot(d1,d2); den=1-c*c
        t1=(-dot(lower,d1)+c*dot(lower,d2))/den
        t2=(-dot(lower,d2)+c*dot(lower,d1))/den
        bridle_residual=add(lower,add(mul(d1,t1),mul(d2,t2)))
        extension=tension*row["new_free_length_m"]/EA
        sag=[]
        for length,direction in zip(row["segment_lengths_m"],directions):
            qperp=MU*G*sqrt(max(0.,1-direction[2]**2))
            slope=qperp*length/(2*tension)
            sag.append({"span_m":length,"maximum_transverse_slope":slope,
                        "small_slope_domain":slope<=.2,"sag_bound_m":qperp*length*length/(8*tension),
                        "geometric_excess_bound_m":qperp*qperp*length**3/(24*tension*tension)})
        band_offset=norm(lower)/B["bag_band_stiffness_n_m"]
        top_offset=norm(topforce)/2e6
        actuator_stretch=tension/B["bag_adjuster"]["axial_stiffness_n_m"]
        # Fixed-node compatibility: command + free length + rope/actuator
        # stretch = nominal path + positive sag excess, for either stock length.
        sag_excess=sum(x["geometric_excess_bound_m"] for x in sag)
        command=row["total_path_including_nominal_actuator_m"]-row["new_free_length_m"]-extension+sag_excess-actuator_stretch
        old_command=row["total_path_including_nominal_actuator_m"]-row["old_free_length_m"]-tension*row["old_free_length_m"]/EA+sag_excess-actuator_stretch
        rows.append({"host":i,"bag":b,"vertical_share_n":vertical,"tension_n":tension,"lower_force_n":lower,
                     "top_force_n":topforce,"guide_loads":guides,"axial_extension_m":extension,
                     "top_force_including_lumped_deadweight_n":top_total,
                     "top_anchor_swivel_moment_nm":top_moment,
                     "bridle_leg_axial_requirements_n":[t1,t2],"bridle_unclosed_force_n":bridle_residual,
                     "bridle_tension_positive":min(t1,t2)>0,
                     "rope_lumped_mass_kg":MU*row["paid_length_with_two_tails_m"],
                     "new_stock_command_fixed_nodes_m":command,"old_free_length_command_fixed_nodes_m":old_command,
                     "new_stock_stroke_ok_fixed_nodes":.8<=command<=1.2,
                     "force_limit_n":1.5*tension,"rope_working_n":150e6*ROPE_A,
                     "rope_strength_screen":1.5*tension<=150e6*ROPE_A,
                     "actuator_strength_screen":1.5*tension<=B["bag_adjuster"]["tensile_force_rating_n"],
                     "lower_band_offset_required_m":band_offset,"old_top_foundation_offset_required_m":top_offset,
                     "within_declared_lower_motion":band_offset<=TRAVEL,
                     "sag_diagnostics":sag,"loaded_positions":"UNKNOWN: collisions and unresolved bag/rack equilibrium"})
    racks=[]
    for s in (-1,1):
        origin=(0.,s*29.,11.5)
        loads=list(rackloads[s])
        for p in PARTS:
            if p["rack"]==s and p["role"]=="rack" and p["group"]!="sheaves_axles_bearings_guards_saddles":
                loads.append((p["cg"],(0.,0.,-p["mass_kg"]*G)))
        force=(0.,0.,0.); moment=(0.,0.,0.)
        for pos,f in loads:
            force=add(force,f);moment=add(moment,cross(sub(pos,origin),f))
        # One statically admissible, explicit four-root reaction allocation.
        # It is NOT an elastic frame solution. Each reaction's finite strain
        # requirement is reported; no matrix or global trim is solved.
        J=(4*11.5**2,4*(2.4**2+11.5**2),4*2.4**2)
        omega=tuple(-m/j for m,j in zip(moment,J))
        roots=[]; closure=force; momentclosure=moment
        for root in ROOTS[s]:
            arm=sub(root["root"],origin)
            reaction=add(mul(force,-.25),cross(omega,arm))
            padmoment=cross(sub(root["root"],root["pad"]),mul(reaction,-1.))
            displacement=mul(reaction,-1/root["effective_k_n_m"])
            rotation=norm(padmoment)/root["assumed_rotational_k_nm_rad"]
            sigma=1.5*norm(padmoment)*.075/root["second_moment_m4"]
            closure=add(closure,reaction);momentclosure=add(momentclosure,cross(arm,reaction))
            roots.append({**root,"required_reaction_on_rack_n":reaction,"equal_opposite_at_pad_n":mul(reaction,-1.),
                          "pad_moment_nm":padmoment,"root_displacement_requirement_m":displacement,
                          "pad_rotation_requirement_rad":rotation,"RHS_bending_limit_mpa":sigma/1e6,
                          "150MPa_working_screen":sigma<=150e6,
                          "declared_motion_screen":norm(displacement)<=TRAVEL,
                          "curtain_limit_line_force_n_m":1.5*norm(reaction),
                          "curtain_bond_mean_shear_pa":1.5*norm(reaction)/(.5*.5),
                          "curtain_shape_and_peel_qualified":False})
        crossbeams=[]
        for guide_index in (0,1):
            applied=[]
            for route,loadrow in zip(ROUTES,rows):
                if route["rack"]==s:
                    applied.append((route["bends"][guide_index]["intersection"][0],loadrow["guide_loads"][guide_index]["force_on_guide_n"]))
            span=4.8
            left=(0.,0.,0.)
            for x,f in applied: left=add(left,mul(f,-(2.4-x)/span))
            peak=0.
            for x,_ in applied:
                moment_beam=mul(left,x+2.4)
                for a,f in applied:
                    if a<=x: moment_beam=add(moment_beam,mul(f,x-a))
                peak=max(peak,sqrt(moment_beam[1]**2+moment_beam[2]**2))
            inertia=(.2**4-.188**4)/12
            deflection=sum(sqrt(f[1]**2+f[2]**2) for _,f in applied)*span**3/(48*70e9*inertia)
            crossbeams.append({"guide_index":guide_index,"force_only_bending_moment_nm":peak,
                               "bending_limit_mpa":1.5*peak*.1/inertia/1e6,
                               "point_load_deflection_screen_m":deflection,
                               "working_150MPa_screen":1.5*peak*.1/inertia<=150e6,
                               "scope":"Simply supported beam force loads only; eccentric moments, member deadweight, torsion and joints may change the result. This isolated screen is not a full member qualification or a rigorous lower bound."})
        racks.append({"rack":s,"force_on_rack_n":force,"moment_about_midheight_nm":moment,"guide_crossbeam_screens":crossbeams,
                      "root_requirements":roots,"statics_force_residual_n":norm(closure),
                      "statics_moment_residual_nm":norm(momentclosure),
                          "elastic_compatibility_solved":False})
    residuals=[]
    for b in (1,2):
        # Four unchanged vertical hangers provide their old quarter-pair shares.
        # Their first moments are added, so the complete lower-bag wrench is
        # visible even when equal vertical sharing happens to balance weight.
        f=add(bagforce[b],(0.,0.,-bag_loads[b]*G))
        m=bagmoment[b]
        for i in range(b*8,(b+1)*8):
            if i not in HOSTS:
                v=(0.,0.,bag_loads[b]*G/8)
                f=add(f,v);m=add(m,cross(sub(GEO["hangers"][i]["low"],GEO["bag_centres"][b]),v))
        for row in ROUTES:
            if row["bag"]==b:
                extra=row["paid_length_with_two_tails_m"]-row["geometric_rope_length_m"]
                dead=(32.+MU*(row["segment_lengths_m"][0]+extra)/2)*G
                f=add(f,(0.,0.,-dead))
                m=add(m,cross(sub(row["original_low"],GEO["bag_centres"][b]),(0.,0.,-20.*G)))
                m=add(m,cross(sub(row["eye"],GEO["bag_centres"][b]),(0.,0.,-(dead-20.*G))))
        # Actual air centroid is vertically below the bag centre: no gravity
        # torque about x/y at the declared unshifted centre. No water repair.
        residuals.append({"bag":b,"unclosed_force_n":f,"unclosed_moment_nm":m,
                          "air_centroid_z_m":state["bags"][b]["air_centroid_z_m"],
                          "old_cuff_forces_also_remain_in_retained_system":True,
                          "simultaneous_retained_and_new_load_sharing_solved":False})
    delta=new_construction-B["hardware"]["construction_kg"]
    return {"altitude_m":state["altitude_m"],"superheat_k":state["superheat_k"],"rows":rows,"racks":racks,
            "lower_bag_wrenches":residuals,"conditional_full_load_trial_only":True,
            "M20_raw_kg":state["M20"]["raw_margin_kg"]-delta,"P100_raw_kg":state["P100"]["raw_margin_kg"]-delta,
            "M20_after_old_74669kg_water_kg":state["M20"]["raw_margin_kg"]-delta-state["M20_fixed_water_kg"],
            "M20_after_older_82851kg_water_kg":state["M20_residual_with_inherited_water_kg"]-delta,
            "all_air_mass_kg_unchanged":state["all_air_mass_kg"],
            "retained_cuff_comparison":state["old_cuff_screen"]}


def main():
    import resource
    resource.setrlimit(resource.RLIMIT_CPU,(180,180))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    groups={}
    for p in PARTS: groups[p["group"]]=groups.get(p["group"],0.)+p["mass_kg"]
    added=sum(p["mass_kg"] for p in PARTS)
    new=B["hardware"]["construction_kg"]+added
    geometry=geometry_screen()
    states=[load_case(s,new) for s in B["states"]]
    for s in states:
        assert max(r["statics_force_residual_n"] for r in s["racks"]) < 1e-7
        assert max(r["statics_moment_residual_nm"] for r in s["racks"]) < 1e-6
    out={"calculator_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"baseline_sha256":BASE_SHA,
         "routes":ROUTES,"parts":PARTS,"objects":OBJECTS,"fixed_objects":FIXED,"geometry":geometry,"states":states,
         "mass":{"old_construction_kg":B["hardware"]["construction_kg"],"retired_kg":0.,"new_items_kg":added,
                 "construction_kg":new,"groups_kg":groups,"equipment_kg":17000.,"pressure_hardware_kg_unchanged":B["hardware"]["pressure_hardware_kg"],
                 "retained_eight_liners_kg":sum(x["mass_kg"] for x in B["guides"]),
                 "retained_old_hangers_and_actuators":"counted once in baseline; no replacement credit; new stock is separately identified",
                 "conversion_gate":"FAIL; this is a priced retained-hardware proposal, not a completed eight-hanger conversion"},
         "volume":{"new_solid_material_m3":sum(x["solid_volume_m3"] for x in PARTS),
                   "inherited_total_debit_m3":100.,"routing_reserve_within_debit_m3":50.,
                   "freed_liner_exclusion_m3":0.,"restored_bag_capacity_m3":0.,"new_sealed_air_m3":0.,
                   "rule":"Hollow sections vent to common gas. Old cap/liner geometry and 100 m3 datum debit retained. New material fits inside existing 50 m3 routing reserve; no displaced-volume credit.",
                   "hydrostatic_placement":"Actual new solid positions supplied; their reserve stays represented at z=0 as inherited. Exact redistribution correction is not claimed."},
         "bounds":{"cpu_s":180,"wall_s":240,"memory_mib":512,"arc_subdivisions":16,"curtain_subdivisions":32},
         "result":"FAIL: one routing intersects lower full bags; stiffness, travel, strength and rotational closure do not establish conversion. Pressure protection FAIL, vehicle UNKNOWN."}
    print(json.dumps(out,indent=2))


if __name__=="__main__": main()
