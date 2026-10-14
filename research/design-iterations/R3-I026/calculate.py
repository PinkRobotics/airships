#!/usr/bin/env python3
"""One frozen finite radial-yoke hypothesis; fixed-root screens, not vehicle equilibrium.

Read pinned saved predecessor data only. No ancestor calculator is imported or run.
Vector/finite-segment/circular-bend algebra is carried from the cited predecessor.
"""
import hashlib
import json
import resource
from math import acos, ceil, cos, pi, sin, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_SHA = "b0907fa2f2589d3d087b099b38e730f45eaaa06351a5bb85efee55367bf59127"
SPEC_SHA = "16c924ba0aad76a19ff303e0fadd5854a2eded07f659daa7ef086d0d66e23615"
for name, sha in [("baseline.json", BASE_SHA), ("geometry.json", SPEC_SHA)]:
    assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == sha
B = json.loads((HERE / "baseline.json").read_text())
S = json.loads((HERE / "geometry.json").read_text())
OLD, I = B["predecessor"], B["inherited"]
GEO = I["geometry"]
R, RB = GEO["radius_m"], GEO["bag_radius_m"]
HOSTS = tuple(S["hosts"])
G = 9.80665
ROPE_D, ROPE_R = S["rope_diameter_m"], S["rope_clamp_enclosure_radius_m"]
ROPE_A = pi * ROPE_D**2 / 4
EA = S["rope_E_pa"] * ROPE_A
MU = S["rope_density_kg_m3"] * ROPE_A + S["rope_coating_mass_kg_m"]
BEND_R, GUARD_R = S["rack_bend_radius_m"], S["guard_radius_m"]
TRAVEL, RHO_AL = S["module_movement_allowance_m"], S["aluminium_density_kg_m3"]


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


def solve3(matrix, rhs):
    """Three scalar equations for one local fixed-root truss, with pivoting."""
    a = [list(row) + [v] for row, v in zip(matrix, rhs)]
    for k in range(3):
        pivot = max(range(k, 3), key=lambda j: abs(a[j][k]))
        a[k], a[pivot] = a[pivot], a[k]
        assert abs(a[k][k]) > 1e-12
        divisor = a[k][k]
        a[k] = [v / divisor for v in a[k]]
        for j in range(3):
            if j != k:
                factor = a[j][k]
                a[j] = [v - factor * w for v, w in zip(a[j], a[k])]
    return tuple(row[3] for row in a)


def sphere_arc(c, a, b, rad, count=24):
    u, v = unit(sub(a, c)), unit(sub(b, c))
    theta = acos(clamp(dot(u, v), -1, 1))
    points = [add(c, mul(add(mul(u, sin((1-k/count)*theta)),
                              mul(v, sin(k/count*theta))), rad/sin(theta)))
              for k in range(count+1)]
    cg = add(c, mul(add(u, v), rad*sin(theta)/(theta*(1+cos(theta)))))
    return points, rad*theta, cg, rad*(1-cos(theta/(2*count)))


def build():
    routes, modules = [], []
    for old in OLD["routes"]:
        host, bag = old["host"], old["bag"]
        c, low = GEO["bag_centres"][bag], old["original_low"]
        n = unit(sub(low, c))
        t1 = unit((-(low[1]-c[1]), low[0]-c[0], 0.))
        t2 = unit(cross(n, t1))
        tip = add(low, mul(n, S["outreach_from_original_low_m"]))
        roots = []
        for j, (sx, sy) in enumerate(((-1,-1), (-1,1), (1,-1), (1,1))):
            surface = add(c, mul(unit(add(mul(n, RB), add(mul(t1, sx*.75), mul(t2, sy*.75)))), RB))
            normal = unit(sub(surface, c))
            root = add(surface, mul(normal, S["root_radial_standoff_m"]))
            lug = add(c, mul(unit(add(mul(n,RB),mul(t1,sx*S["existing_cradle_lug_tangent_offset_m"]))), RB))
            roots.append(dict(id=f"host{host}-root{j}", surface=surface, normal=normal, root=root,
                              existing_cradle_lug=lug, cradle_point=f"original-band-{host}-latitude-{'minus' if sx<0 else 'plus'}"))
        p, q = [be["intersection"] for be in old["bends"]]
        rope_top = old["segments"][-1][1]
        bends = [bend(tip, p, q), old["bends"][1]]
        spans = [(tip,bends[0]["entry"]), (bends[0]["exit"],bends[1]["entry"]), (bends[1]["exit"],rope_top)]
        lengths = [norm(sub(b,a)) for a,b in spans]
        assert min(lengths)>0
        length = sum(lengths)+sum(be["arc_length_m"] for be in bends)
        free = ceil(length/.5)*.5
        routes.append({**old, "eye":tip, "normal":n, "bends":bends, "segments":spans,
                       "segment_lengths_m":lengths, "geometric_rope_length_m":length,
                       "new_free_length_m":free,"paid_length_with_two_tails_m":free+2,
                       "total_path_including_nominal_actuator_m":length+1})
        modules.append(dict(host=host,bag=bag,low=low,centre=c,normal=n,tangent1=t1,tangent2=t2,tip=tip,roots=roots))

    # Only physically superseded I022 stock is removed. The I018 penetrations,
    # their old ropes/actuators and the complete upper/rack system remain paid.
    retire = {f"rope{i}" for i in HOSTS} | {f"bridle{i}" for i in HOSTS} | {f"guide{i}-0-arm" for i in HOSTS}
    retired = [p for p in OLD["parts"] if p["id"] in retire]
    parts = [dict(p) for p in OLD["parts"] if p["id"] not in retire]
    removed_objects = {f"guide{i}-0-guard" for i in HOSTS} | {f"guide{i}-0-arm" for i in HOSTS} | {f"rope{i}-lower-socket" for i in HOSTS}
    objects = [dict(o) for o in OLD["objects"] if o["role"]!="rope" and not o["id"].startswith("bridle") and o["id"] not in removed_objects]
    new_parts = []

    def capsule(name,a,b,r,role,rack=0,host=None,**extra):
        objects.append(dict(id=name,a=a,b=b,radius_m=r,role=role,rack=rack,host=host,**extra))
    def part(name,mass,volume,cg,group,host=None,rack=0,role="module"):
        p=dict(id=name,mass_kg=mass,solid_volume_m3=volume,cg=cg,group=group,host=host,rack=rack,role=role)
        parts.append(p);new_parts.append(p)
    def member(name,a,b,w,t,group,host,rack=0,role="module"):
        volume=(w*w-(w-2*t)**2)*norm(sub(b,a))
        part(name,volume*RHO_AL,volume,mean(a,b),group,host,rack,role)
        capsule(name,a,b,w/sqrt(2),role,rack,host)

    for row,mod in zip(routes,modules):
        i,s,tip=row["host"],row["rack"],row["eye"]
        lower=row["bends"][0]
        # Reuse the same paid sheave/guard and socket, moved and swivelled.
        for p in parts:
            if p["id"]==f"guide{i}-0":p["cg"]=lower["centre"]
            if p["id"]==f"rope{i}-lower-termination":p["cg"]=tip
        capsule(f"guide{i}-0-guard",lower["centre"],lower["centre"],GUARD_R,"guard",s,i)
        member(f"guide{i}-0-arm",lower["intersection"],lower["centre"],.1,.004,"replacement_lower_guide_arms",i,s,"rack")
        capsule(f"rope{i}-lower-socket",tip,tip,.12,"socket",s,i)
        first_moment=(0.,0.,0.)
        for k,((a,b),length) in enumerate(zip(row["segments"],row["segment_lengths_m"])):
            capsule(f"rope{i}-straight{k}",a,b,ROPE_R,"rope",s,i)
            first_moment=add(first_moment,mul(mean(a,b),length))
        for j,be in enumerate(row["bends"]):
            for k,(a,b) in enumerate(zip(be["points"],be["points"][1:])):
                capsule(f"rope{i}-arc{j}-{k}",a,b,ROPE_R+be["chord_error_m"],"rope",s,i)
            theta=be["angle_rad"];normal=unit(sub(be["centre"],be["entry"]))
            arc_cg=add(be["centre"],mul(add(mul(normal,-sin(theta)/theta),mul(be["u_in"],(1-cos(theta))/theta)),BEND_R))
            first_moment=add(first_moment,mul(arc_cg,be["arc_length_m"]))
        extra=row["paid_length_with_two_tails_m"]-row["geometric_rope_length_m"]
        first_moment=add(first_moment,mul(mean(tip,row["segments"][-1][1]),extra))
        paid=row["paid_length_with_two_tails_m"]
        part(f"rope{i}",MU*paid,(ROPE_A+.2/1000)*paid,mul(first_moment,1/paid),"replacement_eight_ropes",i,s,"rope")
        w,t=S["leg_and_base_width_m"],S["leg_and_base_wall_m"]
        for j,root in enumerate(mod["roots"]):
            a,p,n=root["root"],root["surface"],root["normal"]
            member(f"yoke{i}-leg{j}",a,tip,w,t,"yoke_legs_RHS_100x100x6",i)
            member(f"yoke{i}-post{j}",add(p,mul(n,.10)),a,.12,.006,"root_posts_RHS_120x120x6",i)
            platevol=2*.18*.24*.018
            pinvol=pi*.05**2/4*.18
            # Aluminium clevis/base plates and terminal doubler; steel pin.
            vol=platevol+pinvol+.30*.30*.020+5/RHO_AL
            mass=(platevol+.30*.30*.020)*RHO_AL+pinvol*7850+5
            part(f"yoke{i}-root-joint{j}",mass,vol,a,"root_plates_clevis_pins_terminals",i)
            capsule(f"yoke{i}-root-joint{j}",a,a,.24,"module",host=i)
            padvol=pi*.25**2*.010*1.2
            part(f"yoke{i}-pad{j}",padvol*1400,padvol,add(p,mul(n,.005)),"conformal_pads_and_bond",i)
            capsule(f"yoke{i}-pad{j}",p,p,.25+.010,"footprint",host=i,own_bag=mod["bag"],actual_shape="defined spherical cap: geodesic radius0.25m, outward thickness0.010m")
            points,length,cg,error=sphere_arc(mod["centre"],p,root["existing_cradle_lug"],RB+.003)
            vol=length*.25*.006*1.2
            part(f"yoke{i}-strap{j}",vol*1400,vol,cg,"four_curved_straps_and_bond",i)
            root["strap_points"]=points;root["strap_length_m"]=length
            for k,(a,b) in enumerate(zip(points,points[1:])):
                capsule(f"yoke{i}-strap{j}-{k}",a,b,.125+.006+error,"footprint",host=i,own_bag=mod["bag"],actual_shape="defined geodesic ribbon width0.25m, radial thickness0..0.006m; capsule is only its enclosure")
        for j,(a,b) in enumerate(((0,1),(1,3),(3,2),(2,0))):
            member(f"yoke{i}-base{j}",mod["roots"][a]["root"],mod["roots"][b]["root"],w,t,"base_ties_and_diagonals",i)
        # Each of the two diagonals is split into two mitred halves at a
        # 0.20 m centre hub; no two intact tubes occupy the same centre volume.
        mid=mean(mod["roots"][0]["root"],mod["roots"][3]["root"])
        for j,root in enumerate(mod["roots"]):
            end=add(mid,mul(unit(sub(root["root"],mid)),.10))
            member(f"yoke{i}-diagonal-half{j}",root["root"],end,w,t,"base_ties_and_diagonals",i)
        for j,root in enumerate(mod["roots"]):
            part(f"yoke{i}-base-gusset{j}",3.,3/RHO_AL,root["root"],"base_gussets",i)
        part(f"yoke{i}-centre-gusset",6.,6/RHO_AL,mid,"base_gussets",i)
        capsule(f"yoke{i}-centre-gusset",mid,mid,.15,"module",host=i)
        tipvol=.30*.30*.02+4*pi*.05**2/4*.18
        tipmass=.30*.30*.02*RHO_AL+4*pi*.05**2/4*.18*7850+8
        part(f"yoke{i}-tip-joint",tipmass,tipvol+8/RHO_AL,tip,"tip_plate_four_pins_and_saddle",i)
        capsule(f"yoke{i}-tip-joint",tip,tip,max(.16,sqrt(2*.15**2+.01**2)),"module",host=i)
        access=add(mod["low"],mul(mod["normal"],.5))
        part(f"yoke{i}-erection-access",8.,8/RHO_AL,access,"erection_access",i)
        capsule(f"yoke{i}-erection-access",access,access,.15,"module",host=i)
    assert len(retired)==24 and len({p["id"] for p in parts})==len(parts)
    return routes,modules,parts,objects,retired,new_parts


def local_module(mod,row,tension,lower_dead):
    tip,host=mod["tip"],mod["host"]
    direction=unit(sub(row["segments"][0][1],tip))
    rope_force=mul(direction,tension)
    applied=add(rope_force,(0.,0.,-lower_dead*G))
    w,t=.10,.006;area=w*w-(w-2*t)**2;inertia=(w**4-(w-2*t)**4)/12
    legs=[];matrix=[[0.]*3 for _ in range(3)]
    for root in mod["roots"]:
        d=unit(sub(root["root"],tip));length=norm(sub(root["root"],tip));k=70e9*area/length
        legs.append((root,d,length,k))
        for j in range(3):
            for l in range(3):matrix[j][l]+=k*d[j]*d[l]
    displacement=solve3(matrix,applied)
    rootrows=[];force_closure=applied;moment=(0.,0.,0.)
    # Tip-load allocation includes all module weight. Exact part CG moments
    # below expose the missing couple, rather than treating the roots as free.
    for root,d,length,k in legs:
        axial=-k*dot(d,displacement);reaction=mul(d,axial)
        force_closure=add(force_closure,reaction)
        moment=add(moment,cross(sub(root["root"],mod["low"]),reaction))
        euler=pi*pi*70e9*inertia/length**2
        gravity_moment=area*2700*G*length**2/8
        stress=1.5*(abs(axial)/area+gravity_moment*.05/inertia)
        rootrows.append({**root,"leg_axial_n":axial,"leg_tension_positive":axial>0,
                         "leg_length_m":length,"leg_euler_pinned_n":euler,
                         "compression_buckling_screen":axial>=0 or 1.5*(-axial)<=euler,
                         "leg_axial_plus_selfweight_limit_mpa":stress/1e6,
                         "leg_150MPa_screen":stress<=150e6,"reaction_on_module_n":reaction,
                         "equal_opposite_on_bag_n":mul(reaction,-1.)})
    moment=add(moment,cross(sub(tip,mod["low"]),rope_force))
    module_parts=[p for p in NEW_PARTS if p["host"]==host and p["role"]=="module"]
    for p in module_parts:moment=add(moment,cross(sub(p["cg"],mod["low"]),(0,0,-p["mass_kg"]*G)))
    extra_dead=lower_dead-sum(p["mass_kg"] for p in module_parts)
    moment=add(moment,cross(sub(tip,mod["low"]),(0,0,-extra_dead*G)))
    # The exact CG correction is a demanded, unqualified root couple.
    couple=mul(moment,-.25)
    closed_f=add(rope_force,(0,0,-lower_dead*G));closed_m=moment
    bag_f=(0.,0.,0.);bag_m=(0.,0.,0.)
    post_I=(.12**4-.108**4)/12
    for rr in rootrows:
        react=rr["reaction_on_module_n"]
        foot_couple=add(cross(sub(rr["root"],rr["surface"]),react),couple)
        post_sigma=1.5*norm(foot_couple)*.06/post_I
        post_delta=norm(react)*.30**3/(3*70e9*post_I)
        joint_delta=norm(react)/S["assumed_joint_translational_k_n_m"]
        # Same host-level band stiffness, conservative summed reaction norm.
        band_delta=sum(norm(x["reaction_on_module_n"]) for x in rootrows)/I["bag_band_stiffness_n_m"]
        pin_shear=1.5*norm(react)/(2*pi*.05**2/4)
        pin_bending=1.5*norm(react)*.08/4/(pi*.05**3/32)
        plate_bearing=1.5*norm(react)/(2*.018*.05)
        rr.update(required_foot_couple_on_module_nm=foot_couple,
                  equal_opposite_foot_couple_on_bag_nm=mul(foot_couple,-1),
                  additional_exact_cg_couple_nm=couple,
                  root_post_bending_limit_mpa=post_sigma/1e6,
                  root_post_150MPa_screen=post_sigma<=150e6,
                  root_post_deflection_requirement_m=post_delta,
                  assumed_joint_deflection_requirement_m=joint_delta,
                  assumed_band_deflection_requirement_m=band_delta,
                  pin_double_shear_limit_mpa=pin_shear/1e6,pin_bending_limit_mpa=pin_bending/1e6,
                  clevis_bearing_limit_mpa=plate_bearing/1e6,
                  pad_mean_limit_traction_pa=1.5*norm(react)/(pi*.25**2),
                  strap_limit_line_force_n_m=1.5*norm(react)/.25,
                  root_capacity_qualified=False,
                  movement_budget_screen=norm(displacement)<=.05 and post_delta<=.05 and joint_delta<=.05 and band_delta<=.05)
        bag_f=add(bag_f,mul(react,-1))
        bag_m=add(bag_m,add(cross(sub(rr["surface"],mod["centre"]),mul(react,-1)),mul(foot_couple,-1)))
        closed_f=add(closed_f,react)
        # Relative to the root-node result, only the added CG correction
        # changes the moment; moving reaction to its foot + couple is exact.
        closed_m=add(closed_m,couple)
    return dict(host=host,rope_force_on_tip_n=rope_force,opposite_on_rope_n=mul(rope_force,-1),
                exact_module_mass_kg=lower_dead-extra_dead,tip_lumped_dead_mass_kg=lower_dead,
                roots=rootrows,local_truss_displacement_requirement_m=displacement,
                force_residual_n=norm(force_closure),unclosed_exact_cg_moment_nm=moment,
                force_residual_with_required_foot_reactions_n=norm(closed_f),
                moment_residual_with_required_unqualified_couples_nm=norm(closed_m),
                additional_couples_physical_status="UNKNOWN/unclosed: required, not supplied by proven membrane/root stiffness",
                bag_force_if_demands_supported_n=bag_f,bag_moment_if_demands_supported_nm=bag_m,
                loaded_position="UNKNOWN; reject displacement beyond declared movement and small-deflection domain",
                all_motion_budgets_pass=all(rr["movement_budget_screen"] for rr in rootrows),
                all_legs_tension_positive=all(rr["leg_tension_positive"] for rr in rootrows))


def load_case(oldstate,construction):
    rows=[];modules=[]
    inherited=next(s for s in I["states"] if (s["altitude_m"],s["superheat_k"])==(oldstate["altitude_m"],oldstate["superheat_k"]))
    for route,mod in zip(ROUTES,MODULES):
        i=route["host"];b=route["bag"]
        directions=[unit(sub(q,p)) for p,q in route["segments"]]
        extra=route["paid_length_with_two_tails_m"]-route["geometric_rope_length_m"]
        module_mass=sum(p["mass_kg"] for p in NEW_PARTS if p["host"]==i and p["role"]=="module")
        lower_dead=module_mass+12+MU*(route["segment_lengths_m"][0]+extra)/2
        vertical=inherited["supported_bag_masses_kg"][b]*G/8+lower_dead*G
        assert directions[0][2]>0, "Frozen topology cannot supply upward share with a tension rope"
        tension=vertical/directions[0][2]
        modules.append(local_module(mod,route,tension,lower_dead))
        guides=[]
        for j,be in enumerate(route["bends"]):
            traction=mul(sub(be["u_out"],be["u_in"]),tension)
            mass=next(p["mass_kg"] for p in PARTS if p["id"]==f"guide{i}-{j}")
            gravity=MU*(sum(route["segment_lengths_m"][j:j+2])/2+be["arc_length_m"])+mass
            force=add(traction,(0,0,-gravity*G));torque=.02*norm(traction)*.03
            guides.append(dict(guide=j,incoming_tension_vector_n=mul(be["u_in"],tension),
                               outgoing_tension_vector_n=mul(be["u_out"],tension),rope_traction_n=traction,
                               force_on_guide_n=force,opposite_guide_force_on_rope_n=mul(traction,-1),
                               saddle_moment_nm=cross(sub(be["centre"],be["intersection"]),force),
                               axle_bending_limit_nm=1.5*norm(force)*.12/4,
                               axle_60mm_bending_limit_mpa=1.5*norm(force)*.12/4/(pi*.06**3/32)/1e6,
                               two_bearings_limit_each_n=1.5*norm(force)/2,
                               bearing_friction_torque_requirement_nm=torque,
                               friction_tension_difference_bound_n=torque/BEND_R,
                               bearing_fatigue_and_contact_rating="UNKNOWN; retained metal mass is not a rating"))
        sag=[]
        for length,d in zip(route["segment_lengths_m"],directions):
            q=MU*G*sqrt(max(0.,1-d[2]**2));slope=q*length/(2*tension)
            sag.append(dict(span_m=length,maximum_transverse_slope=slope,small_slope_domain=slope<=.2,
                            sag_bound_m=q*length**2/(8*tension),geometric_excess_bound_m=q*q*length**3/(24*tension*tension)))
        sag_excess=sum(x["geometric_excess_bound_m"] for x in sag)
        extension=tension*route["new_free_length_m"]/EA
        act=tension/I["bag_adjuster"]["axial_stiffness_n_m"]
        command=route["total_path_including_nominal_actuator_m"]+sag_excess-route["new_free_length_m"]-extension-act
        oldcommand=route["total_path_including_nominal_actuator_m"]+sag_excess-route["old_free_length_m"]-tension*route["old_free_length_m"]/EA-act
        top_force=mul(directions[-1],-tension)
        anchor,endpoint=route["original_top"],route["segments"][-1][1]
        upper_socket=next(p for p in PARTS if p["id"]==f"rope{i}-upper-termination")
        upper_actuator=next(p for p in PARTS if p["id"]==f"actuator{i}")
        endpoint_rope_mass=MU*(route["segment_lengths_m"][-1]+extra)/2
        top_dead=endpoint_rope_mass+upper_socket["mass_kg"]+upper_actuator["mass_kg"]
        top_total=add(top_force,(0,0,-top_dead*G))
        # Force/couple transmitted to the support at its actual anchor. The
        # opposite pair is required from the support on this upper assembly.
        # Keep the existing endpoint gravity lumping, including half of the
        # current paid-minus-geometric length (rounding allowance + two tails).
        tension_moment=cross(sub(endpoint,anchor),top_force)
        top_moment=tension_moment;gravity_lumps=[]
        for name,mass,cg in [("upper_rope_endpoint",endpoint_rope_mass,endpoint),
                             (upper_socket["id"],upper_socket["mass_kg"],upper_socket["cg"]),
                             (upper_actuator["id"],upper_actuator["mass_kg"],upper_actuator["cg"])]:
            gravity=(0.,0.,-mass*G)
            moment=cross(sub(cg,anchor),gravity)
            gravity_lumps.append(dict(id=name,mass_kg=mass,cg_m=cg,force_n=gravity,moment_about_anchor_nm=moment))
            top_moment=add(top_moment,moment)
        upper_wrench=dict(origin_m=anchor,rope_endpoint_m=endpoint,
                          tension_force_on_assembly_n=top_force,tension_moment_about_anchor_nm=tension_moment,
                          gravity_lumps=gravity_lumps,force_on_support_n=top_total,moment_on_support_nm=top_moment,
                          opposite_support_reaction_force_n=mul(top_total,-1),
                          opposite_support_reaction_moment_nm=mul(top_moment,-1),
                          endpoint_rope_allocation="Half of the final straight span and half of current paid-minus-geometric rope length, lumped at the rope endpoint; arc gravity stays at its guide. Socket and actuator use their paid part CGs. This is not a distributed-rope moment solution.",
                          capacity_status="UNKNOWN: required anchor force/couple only; retained support and connection capacity and global compatibility are unqualified")
        rows.append(dict(host=i,bag=b,tension_n=tension,vertical_share_n=vertical,
                         counterfactual_replaced_old_share_n=inherited["supported_bag_masses_kg"][b]*G/8,
                         lower_force_n=mul(directions[0],tension),top_force_n=top_force,
                         top_force_including_deadweight_n=top_total,upper_anchor_wrench=upper_wrench,
                         old_top_foundation_offset_required_m=norm(top_force)/2e6,
                         guide_loads=guides,sag_diagnostics=sag,axial_extension_m=extension,
                         actuator_stretch_m=act,new_stock_command_fixed_nodes_m=command,
                         old_free_length_command_fixed_nodes_m=oldcommand,
                         new_stock_stroke_ok_fixed_nodes=.8<=command<=1.2,
                         old_stock_stroke_ok_fixed_nodes=.8<=oldcommand<=1.2,
                         force_limit_n=1.5*tension,rope_working_n=150e6*ROPE_A,
                         rope_strength_screen=1.5*tension<=150e6*ROPE_A,
                         actuator_strength_screen=1.5*tension<=I["bag_adjuster"]["tensile_force_rating_n"],
                         sag_clearance_allowance_m=max(x["sag_bound_m"] for x in sag),
                         path_status="fixed-node necessary screen only; roots, joints and vehicle compatibility unclosed"))
    residuals=[]
    for b in (1,2):
        force=(0.,0.,-inherited["supported_bag_masses_kg"][b]*G);moment=(0.,0.,0.)
        for host in range(b*8,(b+1)*8):
            if host not in HOSTS:
                f=(0.,0.,inherited["supported_bag_masses_kg"][b]*G/8)
                force=add(force,f);moment=add(moment,cross(sub(GEO["hangers"][host]["low"],GEO["bag_centres"][b]),f))
        for module,route in zip(modules,ROUTES):
            if route["bag"]==b:
                force=add(force,module["bag_force_if_demands_supported_n"])
                moment=add(moment,module["bag_moment_if_demands_supported_nm"])
        residuals.append(dict(bag=b,unclosed_force_n=force,unclosed_moment_nm=moment,
                              interpretation="Counterfactual replacement, requiring unqualified foot couples; no simultaneous old/new load sharing solved"))
    delta=construction-OLD["mass"]["construction_kg"]
    return dict(altitude_m=oldstate["altitude_m"],superheat_k=oldstate["superheat_k"],rows=rows,modules=modules,
                racks=rack_balance(rows),lower_bag_wrenches=residuals,
                conditional_full_load_trial_only=True,M20_raw_kg=oldstate["M20_raw_kg"]-delta,
                P100_raw_kg=oldstate["P100_raw_kg"]-delta,
                M20_after_fixed_water_kg=oldstate["M20_after_old_74669kg_water_kg"]-delta,
                all_air_mass_kg_unchanged=oldstate["all_air_mass_kg_unchanged"],
                retained_cuff_comparison=oldstate["retained_cuff_comparison"],
                inventories_unchanged={k:inherited[k] for k in ["helium_space_m3","inside_duct_air_m3","lobe_air_total_m3","all_air_mass_kg"]},
                unknown_additional_mass="U+C remains unpriced beside every known subtotal and reduces each margin")


def rack_balance(rows):
    rackloads={-1:[],1:[]}
    for route,row in zip(ROUTES,rows):
        for be,guide in zip(route["bends"],row["guide_loads"]):
            rackloads[route["rack"]].append((be["centre"],guide["force_on_guide_n"]))
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
    return racks


def geometry_screen():
    bags=[]; hull=[]; fixed=[]
    for obj in OBJECTS:
        for b,c in enumerate(GEO["bag_centres"]):
            dist,p,t=point_segment(c,obj["a"],obj["b"])
            axis_enclosure_gap=dist-RB-obj["radius_m"]
            exact_own_footprint=obj["role"]=="footprint" and obj.get("own_bag")==b
            gap=0. if exact_own_footprint else axis_enclosure_gap
            bags.append({"object":obj["id"],"role":obj["role"],"host":obj["host"],"bag":b,
                         "gap_m":gap,"axis_enclosure_gap_m":axis_enclosure_gap,"defined_own_footprint_contact":exact_own_footprint,
                         "gap_with_declared_motion_m":None if exact_own_footprint else gap-2*TRAVEL,
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
            "reason":"Full route and finite-module clearance plus force/travel/root-couple qualification are required. Defined own surface patches are contact only; other module or rope penetrations receive no exemption. No penetration retirement is authorized."}


def main():
    resource.setrlimit(resource.RLIMIT_CPU,(180,180))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    global ROUTES,MODULES,PARTS,OBJECTS,RETIRED,NEW_PARTS,ROOTS,FIXED
    ROUTES,MODULES,PARTS,OBJECTS,RETIRED,NEW_PARTS=build()
    FIXED=OLD['fixed_objects']
    keys=('root','pad','curtain_end','length_m','beam_lateral_k_n_m','curtain_k_n_m','joint_k_n_m','effective_k_n_m','assumed_rotational_k_nm_rad','second_moment_m4')
    ROOTS={r['rack']:[{k:row[k] for k in keys} for row in r['root_requirements']] for r in OLD['states'][0]['racks']}
    retired_mass=sum(p['mass_kg'] for p in RETIRED)
    new_mass=sum(p['mass_kg'] for p in NEW_PARTS)
    construction=OLD['mass']['construction_kg']-retired_mass+new_mass
    assert abs(construction-(OLD['mass']['old_construction_kg']+sum(p['mass_kg'] for p in PARTS)))<1e-7
    volume=OLD['volume']['new_solid_material_m3']-sum(p['solid_volume_m3'] for p in RETIRED)+sum(p['solid_volume_m3'] for p in NEW_PARTS)
    assert abs(volume-sum(p['solid_volume_m3'] for p in PARTS))<1e-8
    geometry=geometry_screen()
    states=[load_case(s,construction) for s in OLD['states']]
    # The only positive allowance is a requirement, not a clearance credit.
    for state in states:
        for row in state['rows']:
            gaps=[r for r in geometry['bags'] if r['host']==row['host'] and r['role']=='rope']
            nominal=min(gaps,key=lambda x:x['gap_m'])
            row['worst_bag_nominal_gap_m']=nominal['gap_m']
            row['required_gap_including_motion_sag_m']=S['nominal_clearance_allowance_m']+2*TRAVEL+row['sag_clearance_allowance_m']
            row['remaining_bag_allowance_m']=nominal['gap_m']-row['required_gap_including_motion_sag_m']
            assert max(m['force_residual_n'] for m in state['modules'])<1e-6
    groups={}
    for p in NEW_PARTS:groups[p['group']]=groups.get(p['group'],0)+p['mass_kg']
    geometry['own_noncontact_module_min']=min((x for x in geometry['bags'] if x['role'] in ('module','socket') and x['host'] is not None and x['bag']==GEO['hangers'][x['host']]['bag']),key=lambda x:x['gap_m'])
    geometry['foreign_module_min']=min((x for x in geometry['bags'] if x['role'] in ('module','socket','footprint') and x['host'] is not None and x['bag']!=GEO['hangers'][x['host']]['bag']),key=lambda x:x['gap_m'])
    geometry['nominal_clearance_allowance_m']=S['nominal_clearance_allowance_m']
    geometry['interpretation']='Straight finite capsule distances are exact; circular paths use inflated chords, guards/pads/service bounds are conservative enclosures. A negative enclosure gap alone means unqualified clearance. An actual rope centreline inside a full bag demonstrates intrusion. Defined own spherical pads/ribbons have exact radial contact only in their stated footprint.'
    footprint_contacts=[x for x in geometry['bags'] if x['defined_own_footprint_contact']]
    geometry['defined_contact_count']=len(footprint_contacts)
    own_rope_checks=[];module_hardware=[]
    for route in ROUTES:
        host=route['host'];tip=route['eye']
        own=[o for o in OBJECTS if o['host']==host and o['role'] in ('module','socket','footprint')]
        best=None
        for rope in (o for o in OBJECTS if o['role']=='rope' and o['host']==host):
            a,b=rope['a'],rope['b']
            # Only the first 0.30 m at the declared socket/tip connection is
            # a shared joint. It cannot excuse intersection farther away.
            if rope['id']==f'rope{host}-straight0':
                a=add(a,mul(unit(sub(b,a)),.30))
            for obj in own:
                dist,p,q,t,u=segment_segment(a,b,obj['a'],obj['b'])
                gap=dist-rope['radius_m']-obj['radius_m']
                row=dict(host=host,objects=[rope['id'],obj['id']],gap_m=gap,points=[p,q],radii_m=[rope['radius_m'],obj['radius_m']],excluded_joint_length_m=.30)
                if best is None or gap<best['gap_m']:best=row
        own_rope_checks.append(best)
        best=None
        for obj in own:
            for other in (o for o in OBJECTS if o['host']!=host and o['role']!='rope'):
                dist,p,q,t,u=segment_segment(obj['a'],obj['b'],other['a'],other['b'])
                gap=dist-obj['radius_m']-other['radius_m']
                row=dict(host=host,objects=[obj['id'],other['id']],gap_m=gap,points=[p,q],radii_m=[obj['radius_m'],other['radius_m']])
                if best is None or gap<best['gap_m']:best=row
        module_hardware.append(best)
    geometry['rope_to_own_module_outside_defined_joint']=own_rope_checks
    geometry['module_to_other_hardware']=module_hardware
    out=dict(calculator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),baseline_sha256=BASE_SHA,geometry_spec_sha256=SPEC_SHA,
             routes=ROUTES,modules=MODULES,parts=PARTS,objects=OBJECTS,fixed_objects=FIXED,geometry=geometry,states=states,
             mass=dict(comparison_I022_kg=OLD['mass']['construction_kg'],comparison_I018_kg=OLD['mass']['old_construction_kg'],
                       retired_I022_parts=RETIRED,retired_I022_kg=retired_mass,new_parts=NEW_PARTS,new_parts_kg=new_mass,
                       new_groups_kg=groups,construction_known_kg=construction,unknown_strengthening_and_contact='U+C unpriced, additional to every known construction/payload subtotal',
                       equipment_kg=17000,pressure_hardware_kg_unchanged=OLD['mass']['pressure_hardware_kg_unchanged'],original_pressure_allowance_kg_once=2000,
                       energy_allowance_kg=5000,propulsion_allowance_kg=3000,retained_eight_liners_kg=OLD['mass']['retained_eight_liners_kg'],retired_old_penetrations=0,
                       retained_I022_parts_count=len(PARTS)-len(NEW_PARTS),retained_old_load_paths='I018 hangers/actuators/liners counted once; no dual load-sharing credit',
                       same_I022_hardware_reused='16 guide bodies/guards, 16 sockets, eight actuators, upper guide arms, racks, curtain/root/access stock; reuse capacity is unqualified'),
             volume=dict(I022_material_inside_reserve_m3=OLD['volume']['new_solid_material_m3'],retired_material_m3=sum(p['solid_volume_m3'] for p in RETIRED),new_material_m3=sum(p['solid_volume_m3'] for p in NEW_PARTS),current_material_inside_reserve_m3=volume,
                         inherited_non_gas_debit_m3=100,routing_reserve_within_debit_m3=50,remaining_routing_reserve_m3=50-volume,new_sealed_air_m3=0,restored_bag_capacity_m3=0,
                         approximation='All hollow members vent to common gas. Actual material locations/CGs supplied; controlling represented volumes and old liner-cap quadrature unchanged. Reserve remains represented at z=0; no displacement or capacity credit and no exact hydrostatic redistribution claimed.'),
             common_inventory_unchanged=I['inventory'],fixed_water_kg=I['states'][0]['M20_fixed_water_kg'],
             inherited_failures=B['original_failures'],inherited_15k=I['same_inventory_15k'],bounds=S['limits'],
             result='FAIL: one frozen radial yoke/retained-rack construction. Complete route, reactions, travel, strength and physical root-couple compatibility do not qualify conversion; pressure/header FAIL and vehicle/global/mission UNKNOWN persist.')
    assert volume<50
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
