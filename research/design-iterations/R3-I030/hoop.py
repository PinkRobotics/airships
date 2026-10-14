#!/usr/bin/env python3
"""One frozen circumferential hoop: finite geometry and conditional statics.

Standard-library calculation over pinned saved data. No ancestor execution,
optimization, iterative shape solution or claim of a physically qualified ring.
"""
import hashlib
import json
import os
import resource
from math import acos, ceil, cos, pi, sin, sqrt
from pathlib import Path

for resource_name, ceiling in [(resource.RLIMIT_CPU,180),(resource.RLIMIT_AS,512*1024**2)]:
    soft,hard=resource.getrlimit(resource_name)
    limit=min([ceiling]+[x for x in (soft,hard) if x!=resource.RLIM_INFINITY])
    resource.setrlimit(resource_name,(limit,limit))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})

HERE = Path(__file__).resolve().parent
SOURCES = json.loads((HERE / 'sources.json').read_text())
for entry in SOURCES['inputs']:
    raw = (HERE / entry['path']).read_bytes()
    assert len(raw) == entry['bytes']
    assert hashlib.sha256(raw).hexdigest() == entry['sha256']
B = json.loads((HERE / 'baseline.json').read_text())
S, OLD, I = SOURCES['design'], B['predecessor'], B['inherited']
GEO = I['geometry']
G, R, RB = 9.80665, GEO['radius_m'], GEO['bag_radius_m']
HOSTS = S['hosts']
AREA = pi * S['rope_diameter_m']**2 / 4
MU = AREA*S['rope_density_kg_m3'] + S['rope_coating_mass_kg_m']
EA = AREA*S['rope_E_pa']


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def mul(a, t): return tuple(x*t for x in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def norm(a): return sqrt(dot(a, a))
def unit(a): return mul(a, 1/norm(a))
def mean(a, b): return mul(add(a, b), .5)
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def clamp(x, low=0., high=1.): return min(high, max(low, x))
def gravity(m): return (0., 0., -G*m)
def total(vectors):
    ans = (0., 0., 0.)
    for v in vectors: ans = add(ans, v)
    return ans
def volume(dimensions):
    ans = 1.
    for d in dimensions: ans *= d
    return ans
def radial(angle): return (cos(angle), sin(angle), 0.)
def tangent(angle): return (sin(angle), -cos(angle), 0.)
def ring_point(angle): return mul(radial(angle), S['hoop_radius_m'])
def arc_cg(a, b):
    return mul(radial((a+b)/2), S['hoop_radius_m']*sin((b-a)/2)/((b-a)/2))


def point_segment(c, a, b):
    d = sub(b, a)
    t = clamp(dot(sub(c, a), d)/dot(d, d)) if dot(d, d) else 0.
    p = add(a, mul(d, t))
    return norm(sub(p, c)), p, t


def segment_segment(a, b, c, d):
    u, v, w = sub(b, a), sub(d, c), sub(a, c)
    aa, bb, cc, dd, ee = dot(u, u), dot(u, v), dot(v, v), dot(u, w), dot(v, w)
    candidates = []
    for p in (a, b):
        dist, q, _ = point_segment(p, c, d)
        candidates.append((dist, p, q))
    for q in (c, d):
        dist, p, _ = point_segment(q, a, b)
        candidates.append((dist, p, q))
    den = aa*cc-bb*bb
    if den > 1e-14*aa*cc:
        s, t = (bb*ee-cc*dd)/den, (aa*ee-bb*dd)/den
        if 0 <= s <= 1 and 0 <= t <= 1:
            p, q = add(a, mul(u, s)), add(c, mul(v, t))
            candidates.append((norm(sub(p, q)), p, q))
    return min(candidates, key=lambda x: x[0])


def bend(a, p, b):
    u, v = unit(sub(p, a)), unit(sub(b, p))
    theta = acos(clamp(dot(u, v), -1., 1.))
    radius = S['guide_bend_radius_m']
    n = unit(sub(v, mul(u, cos(theta))))
    distance = radius*sin(theta/2)/cos(theta/2)
    entry, leave = sub(p, mul(u, distance)), add(p, mul(v, distance))
    centre = add(entry, mul(n, radius))
    count = S['bend_subdivisions']
    points = [add(centre, mul(add(mul(n, -cos(theta*k/count)), mul(u, sin(theta*k/count))), radius)) for k in range(count+1)]
    cg = add(centre, mul(add(mul(n, -sin(theta)/theta), mul(u, (1-cos(theta))/theta)), radius))
    return dict(intersection=p, centre=centre, entry=entry, exit=leave, u_in=u, u_out=v,
                axis=unit(cross(u, v)), angle_rad=theta, radius_m=radius,
                tangent_length_m=distance, arc_length_m=radius*theta, cg=cg, points=points,
                chord_error_m=radius*(1-cos(theta/(2*count))))


def rhs(width, wall):
    a = width**2-(width-2*wall)**2
    inertia = (width**4-(width-2*wall)**4)/12
    return dict(area_m2=a, inertia_m4=inertia, section_modulus_m3=2*inertia/width,
                median_area_m2=(width-wall)**2, width_m=width, wall_m=wall)


def member_screen(force, moment, axis, section, length):
    """Fixed cantilever screen, including axial, biaxial bending and torsion.

    Curved sectors use arc length in the straight-beam compliance surrogate.
    This is not a curved-beam proof or a bound on an elastically continuous ring.
    """
    axial = dot(force, axis)
    shear = norm(sub(force, mul(axis, axial)))
    torsion = dot(moment, axis)
    bending = norm(sub(moment, mul(axis, torsion)))
    sigma = S['load_factor']*(abs(axial)/section['area_m2']+bending/section['section_modulus_m3'])
    tau = S['load_factor']*abs(torsion)/(2*section['median_area_m2']*section['wall_m'])
    vm = sqrt(sigma*sigma+3*tau*tau)
    elastic = shear*length**3/(3*S['aluminium_E_pa']*section['inertia_m4']) + bending*length**2/(2*S['aluminium_E_pa']*section['inertia_m4'])
    euler = pi*pi*S['aluminium_E_pa']*section['inertia_m4']/(2*length)**2
    return dict(axial_n=axial, transverse_n=shear, torsion_nm=torsion, bending_nm=bending,
                factored_normal_stress_pa=sigma, factored_torsional_shear_pa=tau,
                factored_von_mises_pa=vm, working_screen=vm<=S['aluminium_working_pa'],
                compression_cantilever_euler_screen=S['load_factor']*max(0., -axial)<=euler,
                compression_euler_n=euler, formal_deflection_surrogate_m=elastic,
                small_displacement_domain=elastic<=S['movement_allowance_each_m'],
                local_buckling_welds_fatigue='UNKNOWN',
                interpretation='Conditional straight-cantilever surrogate; force and full resultant root moment conservatively counted together in compliance; not a loaded shape.')


def bolt_screen(force, moment, count, radius):
    # A conservative scalar demand sum for an assumed equally spaced bolt group.
    # The full moment norm is charged as a tension/shear resultant, not discarded.
    demand = S['load_factor']*(norm(force)/count + norm(moment)/(count*radius))
    stress = demand/(pi*S['splice_bolt_diameter_m']**2/4)
    return dict(bolts=count, group_radius_m=radius, factored_each_resultant_bound_n=demand,
                nominal_shank_stress_pa=stress, nominal160MPa_screen=stress<=S['steel_working_pa'],
                threads_prying_slip_bearing_plate_bending='UNKNOWN; shank-area screen does not certify a joint')


def build():
    removed_ids = {f'rope{h}' for h in HOSTS} | {f'guide{h}-0-arm' for h in HOSTS}
    removed = [p for p in OLD['parts'] if p['id'].startswith('yoke') or p['id'] in removed_ids]
    removed_set = {p['id'] for p in removed}
    parts = [dict(p) for p in OLD['parts'] if p['id'] not in removed_set]
    # Every rerouted rope, guide and socket enclosure is rebuilt; old racks remain.
    objects = [dict(o) for o in OLD['objects'] if not o['id'].startswith(('yoke', 'rope', 'guide', 'actuator'))]
    new_parts, routes, sectors, roots = [], [], [], []
    def obj(name, a, b, radius, role, host=None, error=0., **kw):
        objects.append(dict(id=name, a=a, b=b, radius_m=radius+error, role=role,
                            host=host, curve_error_m=error, **kw))
    def part(name, mass, vol, cg, group, owner=None):
        p = dict(id=name, mass_kg=mass, solid_volume_m3=vol, cg=cg, group=group, owner=owner)
        parts.append(p); new_parts.append(p)
        return p
    def member(name, a, b, width, wall, group, owner=None):
        length = norm(sub(b, a)); vol = rhs(width, wall)['area_m2']*length
        part(name, vol*S['aluminium_density_kg_m3'], vol, mean(a,b), group, owner)
        obj(name, a, b, width/sqrt(2), group)
    def steel_bolts(count, length):
        vol = count*(pi*S['splice_bolt_diameter_m']**2/4*length+S['bolt_head_nut_washer_mass_kg']/S['steel_density_kg_m3'])
        return vol*S['steel_density_kg_m3'], vol

    ring_section = rhs(S['hoop_rhs_width_m'], S['hoop_rhs_wall_m'])
    for i in range(8):
        a, b = -i*pi/4, -(i+1)*pi/4
        length = S['hoop_radius_m']*pi/4
        vol = ring_section['area_m2']*length
        p = part(f'hoop-sector{i}', vol*S['aluminium_density_kg_m3'], vol, arc_cg(a,b), 'hoop_sectors', i)
        count = S['arc_subdivisions_per_sector']
        points = [ring_point(a+(b-a)*k/count) for k in range(count+1)]
        error = S['hoop_radius_m']*(1-cos(pi/(8*count)))
        for k,(p0,p1) in enumerate(zip(points,points[1:])):
            obj(f'hoop-sector{i}-chord{k}',p0,p1,S['hoop_rhs_width_m']/sqrt(2),'hoop_sector',error=error)
        sectors.append(dict(id=i, angles_rad=[a,b], endpoints=[points[0],points[-1]], points=points,
                            guide_intersection=ring_point((a+b)/2), length_m=length,
                            mass_kg=p['mass_kg'], cg=p['cg'], section=ring_section,
                            half_cgs=[arc_cg(a,(a+b)/2),arc_cg((a+b)/2,b)]))
        pos=points[0]
        platevol=S['splice_cover_plate_count']*volume(S['splice_plate_dimensions_m'])
        bm,bv=steel_bolts(S['splice_through_bolt_count'],S['splice_bolt_length_m'])
        part(f'splice{i}',platevol*S['steel_density_kg_m3']+bm,platevol+bv,pos,'splice_plates_bolts',i)
        obj(f'splice{i}',pos,pos,sqrt(.4**2+.28**2+.28**2),'splice')
        rack, index=S['root_receivers'][i]
        saved=next(r for r in B['receiving_racks'] if r['rack']==rack)['root_requirements'][index]
        receive=saved['root']
        member(f'receiver{i}',pos,receive,S['receiver_rhs_width_m'],S['receiver_rhs_wall_m'],'receiver_members',i)
        roots.append(dict(id=i,ring_point=pos,receiver=receive,receiver_name=f'rack{rack}-root{index}',
                          rack=rack,receiver_index=index,pad=saved['pad'],curtain_end=saved['curtain_end'],
                          section=rhs(S['receiver_rhs_width_m'],S['receiver_rhs_wall_m']),length_m=norm(sub(receive,pos))))
        for end, location in enumerate([pos,receive]):
            av=volume(S['root_end_plate_dimensions_m'])+S['root_gussets_per_end']*volume(S['root_gusset_dimensions_m'])+2*volume(S['root_clevis_plate_dimensions_m'])
            pv=pi*S['root_pin_diameter_m']**2/4*S['root_pin_length_m']
            bm,bv=steel_bolts(S['root_bolts_per_end'],S['root_bolt_length_m'])
            part(f'receiver{i}-joint{end}',av*S['aluminium_density_kg_m3']+pv*S['steel_density_kg_m3']+bm,av+pv+bv,location,'receiver_plates_gussets_pins_bolts',i)
            obj(f'receiver{i}-joint{end}',location,location,.30,'receiver_joint')
        part(f'isolation{i}',S['isolation_each_root_kg'],S['isolation_each_root_kg']/S['laminate_density_kg_m3'],pos,'isolation_contact',i)
        part(f'earthing{i}',S['earthing_each_root_kg'],S['earthing_each_root_kg']/S['steel_density_kg_m3'],pos,'bonding',i)
        part(f'access{i}',S['access_erection_each_sector_kg'],S['access_erection_each_sector_kg']/S['aluminium_density_kg_m3'],sectors[-1]['cg'],'access_erection',i)

    for i, old in enumerate(OLD['routes']):
        host=old['host']; assert host==HOSTS[i]
        low=old['original_low']; top=old['original_top']; endpoint=old['segments'][-1][1]
        p=sectors[i]['guide_intersection']; q=old['bends'][1]['intersection']
        bends=[bend(low,p,q),bend(p,q,endpoint)]
        spans=[(low,bends[0]['entry']),(bends[0]['exit'],bends[1]['entry']),(bends[1]['exit'],endpoint)]
        lengths=[norm(sub(y,x)) for x,y in spans]
        geom=sum(lengths)+sum(be['arc_length_m'] for be in bends)
        free=ceil(geom/.5)*.5; paid=free+2
        route=dict(host=host,bag=old['bag'],rack=old['rack'],low=low,top=top,endpoint=endpoint,
                   bends=bends,segments=spans,segment_lengths_m=lengths,geometric_length_m=geom,
                   free_length_m=free,paid_length_m=paid,old_free_length_m=old['old_free_length_m'],
                   finite_tangencies_fit=(bends[0]['tangent_length_m']<norm(sub(p,low)) and
                     bends[1]['tangent_length_m']<norm(sub(endpoint,q)) and
                     bends[0]['tangent_length_m']+bends[1]['tangent_length_m']<norm(sub(q,p))))
        first_moment=total(mul(mean(x,y),length) for (x,y),length in zip(spans,lengths))
        first_moment=add(first_moment,total(mul(be['cg'],be['arc_length_m']) for be in bends))
        extra=paid-geom
        first_moment=add(first_moment,mul(mean(low,endpoint),extra))
        part(f'rope{host}',MU*paid,(AREA+S['rope_coating_mass_kg_m']/S['rope_coating_density_kg_m3'])*paid,mul(first_moment,1/paid),'eight_replacement_ropes',i)
        for j,(x,y) in enumerate(spans): obj(f'rope{host}-straight{j}',x,y,S['rope_enclosure_radius_m'],'rope',host)
        for j,be in enumerate(bends):
            for k,(x,y) in enumerate(zip(be['points'],be['points'][1:])):
                obj(f'rope{host}-bend{j}-{k}',x,y,S['rope_enclosure_radius_m'],'rope',host,be['chord_error_m'])
            obj(f'guide{host}-{j}-guard',be['centre'],be['centre'],S['guard_radius_m'],'guard',host)
            member(f'guide{host}-{j}-arm',be['intersection'],be['centre'],S['guide_arm_width_m'],S['guide_arm_wall_m'],'guide_arms',i)
            # The previous upper arm is replaced because its finite tangent plane changes.
            prior_arm=next((v for v in parts if v['id']==f'guide{host}-{j}-arm' and 'owner' not in v),None)
            if prior_arm is not None:
                parts.remove(prior_arm); removed.append(prior_arm)
            guide=next(v for v in parts if v['id']==f'guide{host}-{j}')
            guide['cg']=be['centre']
        lower=next(v for v in parts if v['id']==f'rope{host}-lower-termination'); lower['cg']=low
        obj(f'rope{host}-lower-socket',low,low,.12,'socket',host)
        obj(f'rope{host}-upper-socket',top,top,.12,'socket',host)
        obj(f'actuator{host}',endpoint,top,I['bag_adjuster']['od_m']/2,'actuator',host)
        # Paid tails are retained in the endpoint mass allocation and drawn folded back.
        route['tails']=[(low,add(low,mul(unit(sub(bends[0]['entry'],low)),1.))),
                        (endpoint,add(endpoint,mul(unit(sub(bends[1]['exit'],endpoint)),1.)))]
        for j,(x,y) in enumerate(route['tails']):obj(f'rope{host}-tail{j}',x,y,S['rope_enclosure_radius_m'],'tail',host)
        av=volume(S['lower_contact_saddle_dimensions_m'])+2*volume(S['root_clevis_plate_dimensions_m'])
        pv=pi*S['root_pin_diameter_m']**2/4*S['root_pin_length_m']
        lv=(volume(S['lower_contact_pad_dimensions_m'])+S['lower_contact_straps']*volume(S['lower_contact_strap_dimensions_m']))*(1+S['bond_fraction'])
        # Two paid one-metre ribbons follow opposite geodesics from the old band point.
        normal=unit(sub(low,GEO['bag_centres'][old['bag']]))
        along=unit((-normal[1],normal[0],0.))
        strap_cgs=[]
        for sign in (-1,1):
            angle=S['lower_contact_strap_dimensions_m'][0]/RB
            pts=[add(GEO['bag_centres'][old['bag']],mul(add(mul(normal,cos(angle*k/8)),mul(along,sign*sin(angle*k/8))),RB+.003)) for k in range(9)]
            for k,(x,y) in enumerate(zip(pts,pts[1:])):
                obj(f'lower-strap{host}-{sign}-{k}',x,y,.125+.006,'lower_contact',host,error=(RB+.003)*(1-cos(angle/16)))
            strap_cgs.append(add(GEO['bag_centres'][old['bag']],mul(add(mul(normal,sin(angle)/angle),mul(along,sign*(1-cos(angle))/angle)),RB+.003)))
        # Actual declared stock CGs, rather than deleting their small local moments.
        am=av*S['aluminium_density_kg_m3'];pm=pv*S['steel_density_kg_m3'];lm=lv*S['laminate_density_kg_m3']
        cg=mul(total([mul(add(low,mul(normal,.06)),am),mul(add(low,mul(normal,.15)),pm),mul(mean(*strap_cgs),lm)]),1/(am+pm+lm))
        part(f'lower-contact{host}',am+pm+lm,av+pv+lv,cg,'eight_direct_cradle_connections',i)
        obj(f'lower-contact{host}',low,low,.36,'lower_contact',host)
        route['lower_connection']='Original named cradle attachment; paid local saddle/pad/straps, contact and load spreading unqualified. No whole-member clearance exemption.'
        routes.append(route)
    assert len({p['id'] for p in parts})==len(parts)
    return routes,sectors,roots,parts,new_parts,removed,objects


def geometry_screen(objects, routes):
    """Finite conservative envelopes; negative enclosure gaps are not all penetrations."""
    bags=[]; hull=[]; fixed_by_class={}; pairs=[]
    for o in objects:
        for b,c in enumerate(GEO['bag_centres']):
            distance,p,fraction=point_segment(c,o['a'],o['b'])
            bags.append(dict(object=o['id'],role=o['role'],host=o.get('host'),bag=b,
                             enclosure_gap_m=distance-RB-o['radius_m'],
                             centreline_contact_upper_bound_m=distance-RB+o.get('curve_error_m',0),
                             closest_point=p,segment_fraction=fraction,
                             clearance_with_motion_m=distance-RB-o['radius_m']-2*S['movement_allowance_each_m']))
        p=max((o['a'],o['b']),key=norm)
        hull.append(dict(object=o['id'],role=o['role'],gap_m=R-norm(p)-o['radius_m']))
        if o['role'] in ('rope','hoop_sector','receiver_members','guard','receiver_joint','splice'):
            for f in OLD['fixed_objects']:
                distance,p,q=segment_segment(o['a'],o['b'],f['a'],f['b'])
                row=dict(object=o['id'],fixed=f['id'],category=f['category'],gap_m=distance-o['radius_m']-f['radius_m'],points=[p,q])
                key=(o['role'],f['category'])
                if key not in fixed_by_class or row['gap_m']<fixed_by_class[key]['gap_m']:fixed_by_class[key]=row
    rope_by_host={h:[o for o in objects if o['role']=='rope' and o.get('host')==h] for h in HOSTS}
    for k,h in enumerate(HOSTS):
        for j in HOSTS[k+1:]:
            closest=None
            for a in rope_by_host[h]:
                for b in rope_by_host[j]:
                    distance,p,q=segment_segment(a['a'],a['b'],b['a'],b['b'])
                    row=dict(hosts=[h,j],objects=[a['id'],b['id']],gap_m=distance-a['radius_m']-b['radius_m'],points=[p,q])
                    if closest is None or row['gap_m']<closest['gap_m']:closest=row
            pairs.append(closest)
    own=[r for r in bags if r['object'].endswith('straight0') and r['bag']==next(t['bag'] for t in routes if t['host']==r['host'])]
    ring=[r for r in bags if r['role']=='hoop_sector']
    receivers=[r for r in bags if r['role']=='receiver_members']
    guards=[o for o in objects if o['role']=='guard']
    guard_pairs=[dict(objects=[a['id'],b['id']],gap_m=norm(sub(a['a'],b['a']))-a['radius_m']-b['radius_m']) for i,a in enumerate(guards) for b in guards[:i]]
    interfaces=[]
    for h in HOSTS:
        by_role={}
        for rope in rope_by_host[h]:
            for hardware in objects:
                if hardware['role'] not in ('hoop_sector','receiver_members','receiver_joint','splice','guard'):continue
                if hardware['role']=='guard' and hardware.get('host')==h:continue
                distance,p,q=segment_segment(rope['a'],rope['b'],hardware['a'],hardware['b'])
                row=dict(host=h,objects=[rope['id'],hardware['id']],role=hardware['role'],gap_m=distance-rope['radius_m']-hardware['radius_m'],points=[p,q])
                if row['role'] not in by_role or row['gap_m']<by_role[row['role']]['gap_m']:by_role[row['role']]=row
        interfaces.extend(by_role.values())
    return dict(bag_witnesses=bags,hull_witnesses=hull,fixed_class_witnesses=list(fixed_by_class.values()),
                rope_to_hardware=interfaces,
                rope_pairs=pairs,guard_pairs=guard_pairs,own_departures=own,
                minimum_ring_bag=min(ring,key=lambda r:r['enclosure_gap_m']),
                minimum_receiver_bag=min(receivers,key=lambda r:r['enclosure_gap_m']),
                minimum_route_bag=min((r for r in bags if r['role']=='rope'),key=lambda r:r['enclosure_gap_m']),
                minimum_rope_pair=min(pairs,key=lambda r:r['gap_m']),
                nominal_route_clearance_screen_pass=all(r['enclosure_gap_m']>=S['nominal_clearance_m'] for r in bags if r['role'] in ('rope','hoop_sector','receiver_members','guard')),
                physical_routing_fit='UNKNOWN; finite unloaded screens do not solve loaded fit',retired_penetrations=0,
                qualification='Capsules enclose paid members. Negative enclosure gap is unqualified clearance; a negative centreline upper bound proves intrusion for a rope axis/curved centreline. Existing bag contacts stay visible; no blanket contact exemption. Unmodelled joint details, other new hardware interfaces and loaded movement remain UNKNOWN.')


def load_case(index,routes,sectors,roots,parts,new_parts,construction):
    old=OLD['states'][index]; inherited=I['states'][index]
    assert (old['altitude_m'],old['superheat_k'])==(inherited['altitude_m'],inherited['superheat_k'])
    rows=[]; endpoint_loads=[[] for _ in range(8)]
    def paid(name):return next(p for p in parts if p['id']==name)
    for i,route in enumerate(routes):
        h=route['host'];directions=[unit(sub(y,x)) for x,y in route['segments']]
        extra=route['paid_length_m']-route['geometric_length_m']
        lower_mass=paid(f'rope{h}-lower-termination')['mass_kg']+paid(f'lower-contact{h}')['mass_kg']+MU*(route['segment_lengths_m'][0]+extra)/2
        duty=inherited['supported_bag_masses_kg'][route['bag']]*G/8
        vertical=duty+lower_mass*G
        uz=directions[0][2]
        if uz<=0:
            rows.append(dict(host=h,vertical_share_n=vertical,tension_n=None,result='FAIL: tension-only route has no upward component'))
            continue
        tension=vertical/uz; guide_loads=[]
        for j,be in enumerate(route['bends']):
            traction=mul(sub(be['u_out'],be['u_in']),tension)
            dead=paid(f'guide{h}-{j}')['mass_kg']+MU*(sum(route['segment_lengths_m'][j:j+2])/2+be['arc_length_m'])
            force=add(traction,gravity(dead))
            arm=paid(f'guide{h}-{j}-arm')
            origin=be['intersection']
            moment=add(cross(sub(be['centre'],origin),force),cross(sub(arm['cg'],origin),gravity(arm['mass_kg'])))
            guide_loads.append(dict(guide=j,force_on_guide_n=force,force_on_support_n=add(force,gravity(arm['mass_kg'])),
                                    moment_at_support_nm=moment,rope_traction_n=traction,opposite_force_on_rope_n=mul(traction,-1),
                                    allocated_rope_and_guide_mass_kg=dead,arm_mass_kg=arm['mass_kg'],
                                    axle_bending_stress_pa=S['load_factor']*norm(force)*S['axle_span_m']/4/(pi*S['axle_diameter_m']**3/32),
                                    two_bearings_each_demand_n=S['load_factor']*norm(force)/2,
                                    assumed_friction_torque_nm=.02*norm(traction)*.03,
                                    bearing_contact_fatigue='UNKNOWN'))
        sag=[]
        for length,d in zip(route['segment_lengths_m'],directions):
            q=MU*G*sqrt(max(0,1-d[2]**2));slope=q*length/(2*tension)
            sag.append(dict(span_m=length,slope=slope,small_slope_domain=slope<=.2,
                            sag_m=q*length**2/(8*tension),positive_geometric_excess_m=q*q*length**3/(24*tension*tension)))
        excess=sum(x['positive_geometric_excess_m'] for x in sag)
        extension=tension*route['free_length_m']/EA; actuator=tension/I['bag_adjuster']['axial_stiffness_n_m']
        command=route['geometric_length_m']+1+excess-route['free_length_m']-extension-actuator
        identity=route['free_length_m']+extension+actuator+command-(route['geometric_length_m']+1+excess)
        upper_force=mul(directions[-1],-tension); anchor=route['top']; endpoint=route['endpoint']
        upper_mass=MU*(route['segment_lengths_m'][-1]+extra)/2
        lumps=[dict(id='upper-rope-allocation',mass_kg=upper_mass,cg=endpoint),paid(f'rope{h}-upper-termination'),paid(f'actuator{h}')]
        top_force=add(upper_force,total(gravity(p['mass_kg']) for p in lumps))
        top_moment=add(cross(sub(endpoint,anchor),upper_force),total(cross(sub(p['cg'],anchor),gravity(p['mass_kg'])) for p in lumps))
        lower_force=mul(directions[0],tension)
        lower_bag_force=sub(lower_force,(0,0,lower_mass*G))
        contact=paid(f'lower-contact{h}')
        lower_couple=cross(sub(contact['cg'],route['low']),gravity(contact['mass_kg']))
        bag_moment=add(cross(sub(route['low'],GEO['bag_centres'][route['bag']]),lower_bag_force),lower_couple)
        route_traction_sum=add(add(lower_force,upper_force),total(x['rope_traction_n'] for x in guide_loads))
        route_traction_moment=total([cross(route['low'],lower_force),cross(route['endpoint'],upper_force),
                                    *[cross(be['centre'],gl['rope_traction_n']) for be,gl in zip(route['bends'],guide_loads)]])
        prior=next(x for x in old['rows'] if x['host']==h)
        row=dict(host=h,bag=route['bag'],upward_direction_cosine=uz,tension_n=tension,vertical_share_n=vertical,
                 unchanged_bag_duty_n=duty,lower_dead_mass_kg=lower_mass,lower_force_n=lower_force,
                 lower_force_on_bag_n=lower_bag_force,lower_moment_about_bag_centre_nm=bag_moment,
                 lower_couple_about_original_attachment_nm=lower_couple,lower_paid_connection_cg=contact['cg'],
                 lower_opposite_on_rope_n=mul(lower_force,-1),upper_anchor_wrench=dict(origin_m=anchor,
                 endpoint_m=endpoint,force_on_support_n=top_force,moment_on_support_nm=top_moment,
                 opposite_force_n=mul(top_force,-1),opposite_moment_nm=mul(top_moment,-1),gravity_lumps=lumps),
                 guide_loads=guide_loads,sag=sag,axial_extension_m=extension,actuator_stretch_m=actuator,
                 command_m=command,positive_sag_identity_residual_m=identity,stroke_pass=.8<=command<=1.2,
                 factored_rope_force_n=S['load_factor']*tension,rope_working_force_n=AREA*S['rope_working_pa'],
                 rope_strength_pass=S['load_factor']*tension<=AREA*S['rope_working_pa'],
                 actuator_strength_pass=S['load_factor']*tension<=I['bag_adjuster']['tensile_force_rating_n'],
                 rope_action_reaction_sum_n=route_traction_sum,rope_action_reaction_moment_nm=route_traction_moment,
                 prior_I026_tension_n=prior['tension_n'],
                 tension_delta_n=tension-prior['tension_n'],lower_contact_peel_and_stiffness='UNKNOWN',
                 old_free_length_command_m=route['geometric_length_m']+1+excess-route['old_free_length_m']-tension*route['old_free_length_m']/EA-actuator)
        rows.append(row)
        sec=sectors[i]; guide=guide_loads[0]; pos=sec['guide_intersection']
        # Split the same actual guide wrench, not eight equal direction-independent tensions.
        for side,rootindex in enumerate([i,(i+1)%8]):
            endpoint=sec['endpoints'][side]; cg=sec['half_cgs'][side]
            half_mass=(sec['mass_kg']+paid(f'access{i}')['mass_kg'])/2
            force=add(mul(guide['force_on_support_n'],.5),gravity(half_mass))
            moment=add(add(cross(sub(pos,endpoint),mul(guide['force_on_support_n'],.5)),mul(guide['moment_at_support_nm'],.5)),cross(sub(cg,endpoint),gravity(half_mass)))
            axis=tangent(sec['angles_rad'][side]); axis=axis if side==0 else mul(axis,-1)
            screen=member_screen(force,moment,axis,sec['section'],sec['length_m']/2)
            endpoint_loads[rootindex].append(dict(sector=i,side=side,force_n=force,moment_nm=moment,screen=screen,
                                                splice_bolts=bolt_screen(force,moment,S['splice_through_bolt_count'],S['splice_bolt_group_radius_m'])))
    if len(rows)!=8 or any(r['tension_n'] is None for r in rows):
        return dict(altitude_m=old['altitude_m'],superheat_k=old['superheat_k'],rows=rows,structural_result='FAIL: unsupported topology; remaining reaction solution UNKNOWN')
    rootrows=[]
    for i,root in enumerate(roots):
        ring=root['ring_point']; recv=root['receiver']; pointloads=endpoint_loads[i]
        # Sector half weight and guide/arm weight already appear in pointloads.
        local=[p for p in new_parts if p.get('owner')==i and p['group'] in ('splice_plates_bolts','receiver_members','receiver_plates_gussets_pins_bolts','isolation_contact','bonding')]
        force=add(total(x['force_n'] for x in pointloads),total(gravity(p['mass_kg']) for p in local))
        moment=add(total(add(x['moment_nm'],cross(sub(ring,recv),x['force_n'])) for x in pointloads),
                   total(cross(sub(p['cg'],recv),gravity(p['mass_kg'])) for p in local))
        screen=member_screen(force,moment,unit(sub(ring,recv)),root['section'],root['length_m'])
        rootrows.append(dict(id=i,receiver_name=root['receiver_name'],origin_m=recv,
                             force_on_existing_frame_n=force,moment_on_existing_frame_nm=moment,
                             opposite_reaction_on_new_assembly_n=mul(force,-1),opposite_moment_nm=mul(moment,-1),
                             sector_end_demands=pointloads,receiver_member_screen=screen,
                             receiver_bolts=bolt_screen(force,moment,S['root_bolts_per_end'],S['root_bolt_group_radius_m']),
                             pin_double_shear_demand_pa=S['load_factor']*norm(force)/(2*pi*S['root_pin_diameter_m']**2/4),
                             force_displacement_requirement_m=norm(force)/S['joint_k_n_m'],
                             rotation_requirement_rad=norm(moment)/S['joint_rotational_k_nm_rad'],
                             receiving_structure='Required wrench; combined existing frame/curtain response below remains conditional.'))
    racks=[]
    for oldrack in B['receiving_racks']:
        s=oldrack['rack']; origin=(0.,s*29.,11.5); loads=[]
        for route,row in zip(routes,rows):
            if route['rack']==s:
                gl=row['guide_loads'][1];loads.append((route['bends'][1]['intersection'],gl['force_on_support_n'],gl['moment_at_support_nm']))
        for root,row in zip(roots,rootrows):
            if root['rack']==s:loads.append((root['receiver'],row['force_on_existing_frame_n'],row['moment_on_existing_frame_nm']))
        # Existing rack structural stock, excluding guides and arms counted above.
        for p in parts:
            if p.get('rack')==s and p.get('role')=='rack' and not p['id'].startswith('guide'):
                loads.append((p['cg'],gravity(p['mass_kg']),(0.,0.,0.)))
        force=total(x[1] for x in loads); moment=total(add(cross(sub(x[0],origin),x[1]),x[2]) for x in loads)
        inertia=(4*11.5**2,4*(2.4**2+11.5**2),4*2.4**2)
        omega=tuple(-m/j for m,j in zip(moment,inertia)); rr=[]
        for k,saved in enumerate(oldrack['root_requirements']):
            arm=sub(saved['root'],origin);reaction=add(mul(force,-.25),cross(omega,arm))
            load=mul(reaction,-1);pm=cross(sub(saved['root'],saved['pad']),load)
            rr.append(dict(name=f'rack{s}-root{k}',root=saved['root'],pad=saved['pad'],curtain_end=saved['curtain_end'],
                           required_reaction_on_frame_n=reaction,equal_opposite_at_pad_n=load,required_pad_moment_nm=pm,
                           formal_displacement_m=norm(reaction)/saved['effective_k_n_m'],formal_rotation_rad=norm(pm)/saved['assumed_rotational_k_nm_rad'],
                           old150mm_RHS_bending_stress_pa=S['load_factor']*norm(pm)*.075/saved['second_moment_m4'],
                           movement_domain=norm(reaction)/saved['effective_k_n_m']<=S['movement_allowance_each_m'],
                           global_curtain_peel_contact='UNKNOWN; existing reaction allocation is not compatible displacement'))
        residual=add(force,total(x['required_reaction_on_frame_n'] for x in rr))
        mr=add(moment,total(cross(sub(x['root'],origin),x['required_reaction_on_frame_n']) for x in rr))
        racks.append(dict(rack=s,applied_force_n=force,applied_moment_nm=moment,roots=rr,
                          statics_residual_n=norm(residual),statics_residual_nm=norm(mr),global_compatibility='UNKNOWN'))
    delta=construction-OLD['mass']['construction_known_kg']; water=OLD['fixed_water_kg']
    budgets={}
    for name,payload in [('M20',3000.),('P100',100000.)]:
        inventory=OLD['common_inventory_unchanged']
        before=construction+17000+payload+inventory['helium_kg']+inventory['impurity_air_kg']+old['all_air_mass_kg_unchanged']
        gross=inherited[name]['gross_displacement_kg']
        budgets[name]=dict(payload_kg=payload,construction_known_kg=construction,equipment_kg=17000,
                           helium_kg=inventory['helium_kg'],impurity_air_kg=inventory['impurity_air_kg'],
                           other_air_kg=old['all_air_mass_kg_unchanged'],gross_displacement_kg=gross,
                           all_up_before_fixed_water_kg=before,all_up_with_fixed_water_kg=before+water,
                           raw_margin_kg=gross-before,after_fixed_water_margin_kg=gross-before-water,
                           inherited_delta_identity_error_kg=(gross-before)-(old[name+'_raw_kg']-delta),
                           omitted_mass='U+C unpriced; subtract once from each known margin')
    return dict(altitude_m=old['altitude_m'],superheat_k=old['superheat_k'],rows=rows,roots=rootrows,racks=racks,
                complete_known_budgets=budgets,
                M20_raw_kg=old['M20_raw_kg']-delta,P100_raw_kg=old['P100_raw_kg']-delta,
                M20_after_fixed_water_kg=old['M20_after_fixed_water_kg']-delta,
                P100_after_same_fixed_water_kg=old['P100_raw_kg']-delta-water,
                margin_delta_kg=-delta,air_mass_kg=old['all_air_mass_kg_unchanged'],
                inventory=old['inventories_unchanged'],
                physical_margin='UNKNOWN; these four matching mass-ledger margins retain the saved gas basis conditionally, despite unresolved fit/volume distribution and U+C.')


def main():
    routes,sectors,roots,parts,new_parts,removed,objects=build()
    removed_mass=sum(p['mass_kg'] for p in removed); added=sum(p['mass_kg'] for p in new_parts)
    construction=OLD['mass']['construction_known_kg']-removed_mass+added
    groups={}; removed_groups={}
    for p in new_parts:groups[p['group']]=groups.get(p['group'],0)+p['mass_kg']
    for p in removed:removed_groups[p['group']]=removed_groups.get(p['group'],0)+p['mass_kg']
    material=OLD['volume']['current_material_inside_reserve_m3']-sum(p['solid_volume_m3'] for p in removed)+sum(p['solid_volume_m3'] for p in new_parts)
    geometry=geometry_screen(objects,routes)
    states=[load_case(k,routes,sectors,roots,parts,new_parts,construction) for k in range(4)]
    result=dict(calculator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                sources_sha256=hashlib.sha256((HERE/'sources.json').read_bytes()).hexdigest(),
                baseline_sha256=SOURCES['inputs'][0]['sha256'],routes=routes,sectors=sectors,roots=roots,
                parts=parts,new_parts=new_parts,removed_parts=removed,objects=objects,geometry=geometry,states=states,
                mass=dict(baseline_construction_kg=OLD['mass']['construction_known_kg'],conditional_replacement_removed_kg=removed_mass,
                          added_kg=added,new_groups_kg=groups,removed_groups_kg=removed_groups,construction_known_kg=construction,
                          change_kg=construction-OLD['mass']['construction_known_kg'],
                          retained_penetration_liners_kg=OLD['mass']['retained_eight_liners_kg'],qualified_retirement_count=0,
                          equipment_kg=17000,pressure_hardware_kg=OLD['mass']['pressure_hardware_kg_unchanged'],
                          original_pressure_allowance_kg_once=2000,energy_allowance_kg=5000,propulsion_allowance_kg=3000,
                          completeness='Known conditional hardware alternative + U+C; includes no credit for retirement of unqualified old penetrations.'))
    result['volume']=dict(material_inside_represented_reserve_m3=material,reserve_m3=50,datum_debit_m3=100,
                         material_amount_within_reserve=material<=50,routing_fit='FAIL/UNKNOWN',
                         hydrostatic_redistribution='UNKNOWN; material amount does not prove that routing fits. Matching inherited lift is conditional only, not a physically closed volume budget.',
                         sealed_new_displacement_m3=0,full_bag_capacity_credit_m3=0)
    result['inventory']=OLD['common_inventory_unchanged'];result['fixed_water_kg']=OLD['fixed_water_kg']
    result['paid_subassembly_deadweight']=dict(mass_kg=sum(p['mass_kg'] for p in parts),
        force_n=total(gravity(p['mass_kg']) for p in parts),
        moment_about_vehicle_origin_nm=total(cross(p['cg'],gravity(p['mass_kg'])) for p in parts),
        scope='Every enumerated paid part at its stated CG. This is not the missing complete vehicle mass distribution or equilibrium. Rope loading uses the inherited endpoint/guide allocation; distributed rope gravity moments and loaded contact remain UNKNOWN.')
    result['inherited_limits']=['Trapped-bag/header/lower-trip pressure FAIL; no pressure-system change supplied.',
        'Contact, membrane/curtain load spreading and complete strengthening mass remain unqualified U+C.',
        'Global loaded shape, trim and mission-energy UNKNOWN. Full bags, inventory, fixed water and equipment conventions unchanged.',
        'No ballast dump, powered lift, helium reset, penetration retirement or shrunk-bag clearance credit.']
    result['summary']=[]
    for st in states:
        valid=[r for r in st['rows'] if r['tension_n'] is not None]
        result['summary'].append(dict(altitude_m=st['altitude_m'],superheat_k=st['superheat_k'],
            tension_range_n=[min(r['tension_n'] for r in valid),max(r['tension_n'] for r in valid)] if valid else None,
            lower_inclination_cosine_range=[min(r['upward_direction_cosine'] for r in valid),max(r['upward_direction_cosine'] for r in valid)] if valid else None,
            all_rope_strength_pass=all(r.get('rope_strength_pass',False) for r in st['rows']),
            all_actuator_strength_pass=all(r.get('actuator_strength_pass',False) for r in st['rows']),
            all_stroke_pass=all(r.get('stroke_pass',False) for r in st['rows']),
            maximum_receiver_stress_pa=max((r['receiver_member_screen']['factored_von_mises_pa'] for r in st.get('roots',[])),default=None),
            maximum_receiver_formal_displacement_m=max((r['receiver_member_screen']['formal_deflection_surrogate_m'] for r in st.get('roots',[])),default=None),
            maximum_ring_half_stress_pa=max((e['screen']['factored_von_mises_pa'] for r in st.get('roots',[]) for e in r['sector_end_demands']),default=None),
            maximum_positive_sag_identity_error_m=max((abs(r['positive_sag_identity_residual_m']) for r in valid),default=None)))
    failed=(not geometry['nominal_route_clearance_screen_pass'] or
            any(not r.get('rope_strength_pass',False) or not r.get('actuator_strength_pass',False) or not r.get('stroke_pass',False) for st in states for r in st['rows']))
    result['result']=('FAIL' if failed else 'UNKNOWN')+': fixed hoop alternative; complete installed mass, physical/global compatibility, trim and mission remain UNKNOWN; U+C remains unpriced. Inspect the individual finite screens; no physical qualification follows.'
    result['weakest_assumption']='Finite sectors and their existing receivers can distribute large 3D reactions without dominant bending/rotation/curtain mass. Independent cantilever compliance is only a conditional screen; coupled stiffness sensitivity UNKNOWN.'
    result['next_construction']='Raise the load-transfer guide plane onto a paid three-dimensional upper crown while retaining the same full bag envelopes; freeze one new crown/receiver construction before testing whether departure inclination improves.'
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
