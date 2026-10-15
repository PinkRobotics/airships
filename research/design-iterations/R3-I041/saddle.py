"""One fixed paid receiver saddle; saved predecessor JSON is data only.

This enumerates nominal stock and finite geometric enclosures. It does not
solve contact, compatible frame reactions, loaded shape or connection strength.
Only --write is supported. No ancestor source is imported or executed.
"""
from pathlib import Path
import copy
import hashlib
import itertools
import json
import math
import sys

STEEL = 7850.0
POLYMER = 1200.0
G = 9.80665
AXES = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]


def add(a, b): return [x+y for x, y in zip(a, b)]
def sub(a, b): return [x-y for x, y in zip(a, b)]
def mul(a, k): return [x*k for x in a]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def norm(a): return math.sqrt(dot(a, a))
def unit(a): return mul(a, 1/norm(a))
def mid(a, b): return mul(add(a, b), .5)
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def total(vectors):
    out = [0., 0., 0.]
    for v in vectors: out = add(out, v)
    return out
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def at(c, axes, q): return add(c, total(mul(a, x) for a, x in zip(axes, q)))
def box_vertices(c, dims, axes=AXES):
    return [at(c, axes, [s[i]*dims[i]/2 for i in range(3)])
            for s in itertools.product((-1, 1), repeat=3)]
def frame(a, b):
    e = unit(sub(b, a))
    v = [1., 0., 0.] if abs(e[0]) < .9 else [0., 1., 0.]
    v = unit(sub(v, mul(e, dot(v, e))))
    return e, v, cross(e, v)
def closest(p, a, b):
    d = sub(b, a); den = dot(d, d)
    t = max(0., min(1., dot(sub(p, a), d)/den)) if den else 0.
    q = add(a, mul(d, t))
    return norm(sub(p, q)), q
def wrench(parts, origin):
    forces = [[0., 0., -p['mass_kg']*G] for p in parts]
    return dict(origin_m=origin, force_n=total(forces),
                moment_nm=total(cross(sub(p['cg'], origin), f) for p, f in zip(parts, forces)))
def transport(w, origin):
    return dict(origin_m=origin, force_n=w['force_n'],
                moment_nm=add(w['moment_nm'], cross(sub(w['origin_m'], origin), w['force_n'])))
def sum_wrenches(rows, origin):
    rows = [transport(w, origin) for w in rows]
    return dict(origin_m=origin, force_n=total(w['force_n'] for w in rows),
                moment_nm=total(w['moment_nm'] for w in rows))
def opposite(w):
    return dict(origin_m=w['origin_m'], force_n=mul(w['force_n'], -1), moment_nm=mul(w['moment_nm'], -1))


class Stock:
    def __init__(self):
        self.parts = []; self.objects = []; self.seams = []; self.joints = []
        self.bolts = []; self.modules = []
        self.module = None

    def part(self, name, volume, cg, group, density=STEEL, **details):
        p = dict(id=name, module=self.module, mass_kg=volume*density,
                 paid_volume_m3=volume, density_kg_m3=density, cg=cg,
                 group=group, **details)
        self.parts.append(p)
        return p

    def obj(self, name, a, b, radius, role, vertices=None, **details):
        o = dict(id=name, module=self.module, a=a, b=b, radius_m=radius,
                 role=role, vertices=vertices or [], **details)
        self.objects.append(o)
        return o

    def plate(self, name, c, dims, group, axes=AXES, density=STEEL, opening=None):
        vertices = box_vertices(c, dims, axes)
        p = self.part(name, math.prod(dims), c, group, density,
                      dimensions_m=dims, axes=axes, hole_or_offcut_credit_m3=0.)
        self.obj(name, c, c, norm(dims)/2, 'plate', vertices,
                 central_opening_m=opening,
                 representation='Full-blank enclosure; openings are explicit voids but no clearance credit is inferred from the enclosure.')
        return p

    def seam(self, name, a, b, mating):
        length = norm(sub(b, a))
        self.part(name, .5*.010**2*length, mid(a, b), 'fillet_welds',
                  leg_m=.010, endpoints_m=[a, b], length_m=length,
                  mating=mating, capacity='UNKNOWN; nominal bead only, access/fit unresolved.')
        self.seams.append(dict(id=name, endpoints_m=[a, b], length_m=length,
                               leg_m=.010, mating=mating))
        self.obj(name, a, b, .010, 'weld')

    def perimeter(self, name, c, v, w, width, height, mating):
        corners = [add(c, add(mul(v, i*width/2), mul(w, j*height/2)))
                   for i, j in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
        for k in range(4): self.seam(name+str(k), corners[k], corners[(k+1)%4], mating)

    def triangle(self, name, corners, thickness, normal, mating):
        area = norm(cross(sub(corners[1], corners[0]), sub(corners[2], corners[0])))/2
        c = mul(total(corners), 1/3)
        self.part(name, area*thickness, c, 'triangular_gussets',
                  corners_m=corners, thickness_m=thickness, full_blank_paid=True)
        vertices = [add(p, mul(normal, s*thickness/2)) for p in corners for s in (-1, 1)]
        self.obj(name, c, c, max(norm(sub(v, c)) for v in vertices), 'gusset', vertices)
        for k in range(3): self.seam(name+'-edge'+str(k), corners[k], corners[(k+1)%3], mating)

    def tube(self, name, a, b, width, wall, stock_endpoints=None, clip_y=False):
        e, v, w = frame(a, b); length = norm(sub(b, a))
        stock = stock_endpoints or [a, b]
        stock_length = norm(sub(stock[1], stock[0]))
        # Full selected stock is paid, including any clipped offcuts. Its nominal
        # mass CG is the full stock midpoint; actual offcut disposition is unknown.
        self.part(name, (width**2-(width-2*wall)**2)*stock_length,
                  mid(*stock), 'steel_RHS', width_m=width, wall_m=wall,
                  stock_endpoints_m=stock, stock_length_m=stock_length,
                  body_endpoints_m=[a, b], body_length_m=length,
                  offcut_credit_kg=0., offcut_actual_location='UNKNOWN; paid full-stock nominal CG retained.')
        def cut_vertices(p, inset=0.):
            points=[]
            for i,j in itertools.product((-1,1),repeat=2):
                offset=add(mul(v,i*width/2),mul(w,j*width/2))
                # Intersection of each longitudinal stock edge with the actual
                # rail-wall y plane; not a square cut normal to the diagonal.
                shift=-offset[1]/e[1] if clip_y else 0.
                points.append(add(add(p,offset),mul(e,shift+inset)))
            return points
        vertices=cut_vertices(a)+cut_vertices(b)
        self.obj(name, a, b, width/math.sqrt(2), 'RHS', vertices,
                 hollow_width_m=width-2*wall, axis_is_material=False)
        for k, p in enumerate((a, b)):
            # Full square caps lie just inside the selected body end planes.
            # Full blank/wall overlap is retained and paid, never credited.
            c = add(p, mul(e, .006 if k == 0 else -.006))
            if clip_y:
                corners=cut_vertices(p)
                # 12mm plate thickness normal to the mating rail y face.
                direction=1 if k==0 and e[1]>0 or k==1 and e[1]<0 else -1
                capvertices=corners+[add(q,[0.,direction*.012,0.]) for q in corners]
                capcg=mul(total(capvertices),1/8)
                self.part(name+'-cap'+str(k),width*width/abs(e[1])*.012,capcg,'RHS_endcaps',
                          thickness_m=.012,cut_plane_y_m=p[1],full_oblique_blank_paid=True)
                self.obj(name+'-cap'+str(k),capcg,capcg,max(norm(sub(q,capcg)) for q in capvertices),'plate',capvertices)
                perimeter=[corners[i] for i in (0,1,3,2)]
                for j in range(4):self.seam(name+f'-cap-weld{k}-{j}',perimeter[j],perimeter[(j+1)%4],[name,name+'-cap'+str(k)])
            else:
                self.plate(name+'-cap'+str(k), c, [.012, width, width], 'RHS_endcaps', [e, v, w])
                self.perimeter(name+'-cap-weld'+str(k)+'-', p, v, w, width, width,
                               [name, name+'-cap'+str(k)])
        return e, v, w

    def bolt(self, name, a, y, z):
        # Head is always on the -x side. All dimensions below are actual axial
        # stations relative to a, including both full outer backers.
        head_bearing = a-.445
        intervals = dict(head=[a-.470, a-.445], near_washer=[a-.445, a-.440],
                         near_backer=[a-.440, a-.428], near_plate=[a-.428, a-.403],
                         box_and_pads=[a-.403, a+.403], far_plate=[a+.403, a+.428],
                         far_backer=[a+.428, a+.440], far_washer=[a+.440, a+.445],
                         nut=[a+.445, a+.493], runout=[a+.493, a+.513],
                         shank=[head_bearing, head_bearing+1.050])
        specs = [('shank', math.pi*.030**2/4*1.050, .015),
                 ('head', math.sqrt(3)/2*.046**2*.025, .046/math.sqrt(3)),
                 ('nut', math.sqrt(3)/2*.046**2*.048, .046/math.sqrt(3)),
                 ('near_washer', math.pi*(.060**2-.032**2)/4*.005, .030),
                 ('far_washer', math.pi*(.060**2-.032**2)/4*.005, .030),
                 ('near_backer', .100*.100*.012, math.sqrt(2)*.050),
                 ('far_backer', .100*.100*.012, math.sqrt(2)*.050)]
        for label, volume, radius in specs:
            lo, hi = intervals[label]; c = [(lo+hi)/2, y, z]
            self.part(name+'-'+label, volume, c, 'M30_bolt_stack',
                      interval_x_m=[lo, hi], hole_credit_m3=0.)
            self.obj(name+'-'+label, [lo, y, z], [hi, y, z], radius, 'bolt_stack')
        self.obj(name+'-socket', [a-.670, y, z], [a-.470, y, z], .060, 'access')
        self.obj(name+'-insertion', [a-.440-1.200, y, z], [a-.440, y, z], .060, 'access')
        row = dict(id=name, module=self.module, y_m=y, z_m=z,
                   intervals_x_m=intervals, shank_diameter_m=.030, plate_hole_m=.032,
                   head_AF_m=.046, nut_AF_m=.046, backers_m=[.100, .100, .012],
                   washers_OD_ID_t_m=[.060, .032, .005],
                   outer_backer_grip_m=.880, bearing_to_nut_m=.890,
                   nominal_thread_engagement_m=.048, required_runout_m=.020,
                   required_underhead_length_m=.958, selected_underhead_length_m=1.050,
                   nominal_axial_surplus_m=(head_bearing+1.050)-(a+.513),
                   actual_thread_length='UNKNOWN; full shank payment does not specify thread start or certify engagement.',
                   capacity='UNKNOWN; no preload, friction, adhesive or rigid clamp credit.',
                   socket=dict(diameter_m=.120, length_m=.200),
                   insertion=dict(length_m=1.200, from_headside_outer_backer_m=[a-.440, y, z]))
        self.bolts.append(row)

    def build(self, receivers):
        for m, (a, b, lo, hi) in enumerate([(2.4,-29.,0,1),(-2.4,-29.,2,3),
                                            (-2.4,29.,4,5),(2.4,29.,6,7)]):
            self.module = m; s = 1 if a > 0 else -1; x = a+s*.900; pre = f'M{m}'
            rails = []
            for side in (-1, 1):
                rid = pre+f'-rail{side}'; rails.append(rid)
                self.tube(rid, [x,b+side*.9,-.6], [x,b+side*.9,23.6], .2, .01)
            junctions = []
            for j, z in enumerate((0.,11.5,23.)):
                rid = pre+f'-cross{j}'
                self.tube(rid, [x,b-.8,z], [x,b+.8,z], .2, .01,
                          [[x,b-.9,z],[x,b+.9,z]])
                for side in (-1, 1):
                    c = [x,b+side*.8,z]
                    self.perimeter(rid+f'-rail{side}-',c,AXES[0],AXES[2],.2,.2,[rid,pre+f'-rail{side}'])
                    junctions.append((rid+f'-j{side}',[x,b+side*.9,z],side,[rid,pre+f'-rail{side}']))
            for j, (aa, bb) in enumerate([([x,b-.9,0.],[x,b+.9,11.5]),
                                           ([x,b+.9,11.5],[x,b-.9,23.])]):
                e,v,w = frame(aa,bb); ratio=.1/abs(bb[1]-aa[1])
                start=add(aa,mul(sub(bb,aa),ratio));end=add(bb,mul(sub(aa,bb),ratio))
                name=pre+f'-diagonal{j}';self.tube(name,start,end,.1,.008,[aa,bb],clip_y=True)
                for k,(joint,p) in enumerate(((aa,start),(bb,end))):
                    side=-1 if joint[1]<b else 1
                    corners=[]
                    for u,t in [(-1,-1),(1,-1),(1,1),(-1,1)]:
                        offset=add(mul(v,u*.05),mul(w,t*.05))
                        corners.append(add(add(p,offset),mul(e,-offset[1]/e[1])))
                    for edge in range(4):self.seam(name+f'-join{k}-{edge}',corners[edge],corners[(edge+1)%4],[name,pre+f'-rail{side}'])
                    junctions.append((name+f'-j{k}',joint,side,[name,pre+f'-rail{side}']))
                self.joints.append(dict(id=name, selected_joint_centres=[aa,bb],
                    body_axis_clipped_at_rail_inner_y_faces=[start,end],
                    end_face='Oblique end vertices and seams clipped to the explicit rail inner y planes.',
                    unresolved='Welding access, wall overlap and crossbar intersections UNKNOWN; no penetration credit.'))
            for name,c,side,mating in junctions:
                for face in (-1,1):
                    anchor=add(c,[face*.106,0.,0.])
                    corners=[anchor,add(anchor,[0.,-side*.300,0.]),add(anchor,[0.,0.,.300])]
                    self.triangle(name+f'-gusset{face}',corners,.012,AXES[0],mating)
            for level,index in enumerate((lo,hi)):
                R=receivers[index]['existing_receiver_xyz_m'];z=R[2];q=pre+f'-cage{level}'
                assert R == [a,b,z]
                for side in (-1,1):
                    self.plate(q+f'-plate{side}',[a+side*.4155,b,z],[.025,1.,1.],
                               'cage_full_plates',opening=dict(axes=['y','z'],size_m=[.6,.6],centre_m=[a+side*.4155,b,z]))
                    self.plate(q+f'-pad{side}',[a+side*.4015,b,z],[.003,.8,.8],
                               'polymer_isolation',density=POLYMER,
                               opening=dict(axes=['y','z'],size_m=[.6,.6],centre_m=[a+side*.4015,b,z]))
                for axis in (1,2):
                    for side in (-1,1):
                        c=[a,b,z];c[axis]+=side*.4155
                        dims=[.806,.025,.100] if axis==1 else [.806,.100,.025]
                        name=q+f'-bar{axis}-{side}';self.plate(name,c,dims,'cage_bearing_bars')
                        pad=[a,b,z];pad[axis]+=side*.4015
                        pd=[.800,.003,.100] if axis==1 else [.800,.100,.003]
                        self.plate(name+'-isolation',pad,pd,'polymer_isolation',density=POLYMER)
                        for end in (-1,1):
                            cp=c.copy();cp[0]=a+end*.403
                            self.perimeter(name+f'-end{end}-',cp,AXES[1],AXES[2],dims[1],dims[2],
                                           [name,q+f'-plate{end}'])
                for k,(dy,dz) in enumerate(itertools.product((-.450,.450),repeat=2)):
                    self.bolt(q+f'-bolt{k}',a,b+dy,z+dz)
                for side in (-1,1):
                    y=b+side*.400;name=q+f'-stub{side}'
                    self.tube(name,[a+s*.448,y,z],[a+s*.780,y,z],.100,.008)
                    for end,offset in enumerate((.428,.800)):
                        c=[a+s*offset,y,z];plate=name+f'-endplate{end}'
                        self.plate(plate,c,[.020,.160,.200],'stub_endplates')
                        face=[a+s*(.448 if end==0 else .780),y,z]
                        self.perimeter(name+f'-tube-seam{end}-',face,AXES[1],AXES[2],.1,.1,[name,plate])
                        self.perimeter(plate+'-mating-',c,AXES[1],AXES[2],.16,.2,
                                       [plate,q+f'-plate{s}' if end==0 else pre+f'-cross{level*2}'])
                        for k in range(4):
                            # Four full 200x150 triangular blanks around each
                            # stub end. Keep intersections; no notch credit.
                            dy,dz=[(1,0),(0,1),(-1,0),(0,-1)][k]
                            anchor=add(c,[0.,dy*.055,dz*.055])
                            corners=[anchor,add(anchor,[s*(.200 if end==0 else -.200),0.,0.]),
                                     add(anchor,[0.,dy*.150,dz*.150])]
                            normal=[0.,-dz,dy]
                            self.triangle(plate+f'-gusset{k}',corners,.010,normal,[name,plate])
                    self.joints.append(dict(id=name, body_offsets_x_m=[.448,.780],
                        endplate_offsets_x_m=[.428,.800], endplate_thickness_m=.020,
                        nominal_body_to_endplate_face_gaps_m=[.010,.010],
                        status='UNRESOLVED: frozen stock leaves 10mm axial gaps; nominal paid seams do not establish bridging strength or physical connection.'))
                self.joints.append(dict(id=q,receiver=receivers[index],normal_contact='unilateral',
                    plate_inner_faces_x_m=[a-.403,a+.403],box_faces_x_m=[a-.400,a+.400],
                    pads_thickness_m=.003,bearing_bar_x_span_m=[a-.403,a+.403],
                    unknowns=['normal contact distribution','old box-wall strength','local diaphragm path',
                              'support passage through 600mm openings','weld/tool access','rigid-couple transfer'],
                    friction_credit=0.,preload_credit=0.,adhesive_credit=0.))
            self.part(pre+'-handling',20./STEEL,[x,b,11.5],'temporary_handling_access',
                      qualification='Paid allowance; actual disposition and erection adequacy UNKNOWN.')
            self.part(pre+'-bonding',4./STEEL,[x,b,11.5],'bonding_earthing',
                      qualification='Paid allowance; detailed routing and adequacy UNKNOWN.')
            self.modules.append(dict(id=m,a_m=a,b_m=b,ladder_x_m=x,
                                     receiver_indices=[lo,hi],receiver_ids=[receivers[i]['existing_receiver_name'] for i in (lo,hi)],
                                     transport_erection='UNKNOWN; continuous full-length rails have no hidden splices.'))


def aabb(o):
    v=o.get('vertices')
    if v:
        return tuple(min(p[k] for p in v) for k in range(3))+tuple(max(p[k] for p in v) for k in range(3))
    r=o['radius_m'];a=o['a'];b=o['b']
    return tuple(min(a[k],b[k])-r for k in range(3))+tuple(max(a[k],b[k])+r for k in range(3))


def geometry(stock, baseline):
    geo=baseline['inherited_geometry'];old=baseline['predecessor']['objects']+baseline['fixed_objects']
    rows=[];hull=[]
    for o in stock.objects:
        for k,c in enumerate(geo['bag_centres']):
            distance,p=closest(c,o['a'],o['b']);gap=distance-geo['bag_radius_m']-o['radius_m']
            rows.append(dict(object=o['id'],bag=k,enclosure_gap_m=gap,
                axis_gap_m=distance-geo['bag_radius_m'],axis_witness_m=p,
                axis_inside=distance<geo['bag_radius_m'],
                solid_intrusion_proved=False,
                meaning='Conservative overlap is not a solid collision proof; RHS axes are hollow and plate openings remain voids.'))
        verts=o.get('vertices') or [o['a'],o['b']]
        hull.append(dict(object=o['id'],conservative_inside_gap_m=geo['radius_m']-max(norm(o[k]) for k in ('a','b'))-o['radius_m'],
                         vertex_max_radius_m=max(norm(v) for v in verts),
                         represented_vertex_outside=any(norm(v)>geo['radius_m'] for v in verts)))
    newboxes=[aabb(o) for o in stock.objects];oldboxes=[aabb(o) for o in old]
    minima={};counts=dict(new_old=0,new_new=0,old_old=0,overlap_enclosures=0);witnesses=[]
    def scan(i,ob,bounds,kind):
        a=newboxes[i];o=stock.objects[i];best=None;negative=0
        for j,b in enumerate(bounds):
            # Largest coordinate separation is a conservative signed separation
            # for axis-aligned enclosing boxes. A negative result means overlap
            # of enclosures, never proof of occupied solid overlap.
            gap=max(b[0]-a[3],a[0]-b[3],b[1]-a[4],a[1]-b[4],b[2]-a[5],a[2]-b[5])
            counts[kind]+=1
            if best is None or gap<best['signed_gap_m']:
                best=dict(first=o['id'],second=ob[j]['id'],signed_gap_m=gap,
                          enclosure_bounds_m=[a,b],meaning='AABB enclosure separation; no mating exclusions.')
            if gap<0:
                negative+=1;counts['overlap_enclosures']+=1
                if len(witnesses)<2048:witnesses.append(dict(first=o['id'],second=ob[j]['id'],signed_gap_m=gap,kind=kind))
        return dict(minimum=best,overlap_enclosure_count=negative)
    for i,o in enumerate(stock.objects):
        minima[o['id']]=dict(new_old=scan(i,old,oldboxes,'new_old'),
                             new_new=scan(i,stock.objects[i+1:],newboxes[i+1:],'new_new'))
    return dict(method='Complete new/old and triangular new/new AABB enclosure screen, no old/old rerun; all new objects against saved full bags and spherical hull.',
                counts=counts,per_object_pair_minima=minima,first_overlap_witnesses=witnesses,
                overlap_witness_limit=2048,all_overlap_count_preserved=True,
                bag_rows=rows,hull_rows=hull,access_objects=[o for o in stock.objects if o['role']=='access'],
                old_access_retained=[o for o in old if 'access' in o.get('role','')],
                intended_contacts=stock.joints,
                qualification='All nominal mating intersections remain screened. Access is a reserved volume, not material. No loaded clearance, friction, contact capacity or assembly PASS.')


def states(stock, baseline):
    previous=baseline['predecessor'];out=[];added=sum(p['mass_kg'] for p in stock.parts)
    for old in previous['states']:
        modules=[]
        for module in stock.modules:
            ids=module['receiver_indices'];stations=[old['receivers'][i] for i in ids]
            origin=stations[0]['R_m'];new=[p for p in stock.parts if p['module']==module['id']]
            weight=wrench(new,origin)
            known=sum_wrenches([weight]+[r['local_known_gravity_wrench'] for r in stations],origin)
            retained=[p for r in stations for p in r['retained_members']]
            incoming=[dict(receiver=r['id'],support=s,force_n=None,couple_nm=None)
                      for r in stations for s in r['incoming_supports']]
            rack=[w for w in old['upper_guide_rack_wrenches'] if w['origin_m'][1]==module['b_m']]
            modules.append(dict(module=module['id'],origin_m=origin,receiver_records=stations,
                retained_members=retained,retained_path_part_ids=[p['id'] for p in retained],
                new_parts=[dict(id=p['id'],mass_kg=p['mass_kg'],cg_m=p['cg'],gravity_wrench=wrench([p],origin)) for p in new],
                new_gravity_wrench=weight,known_gravity_wrench=known,required_external_wrench_sum=opposite(known),
                incident_support_terms=incoming,
                pad_curtain_terms=[dict(receiver=r['id'],pad_m=r['pad_m'],curtain_end_m=r['curtain_end_m'],
                    pad_force_n=None,pad_couple_nm=None,curtain_force_n=None,curtain_couple_nm=None) for r in stations],
                shared_rack_upper_guide_wrenches=rack,
                rack_ownership='Saved rack-wide upper guide loads are shown for context, not numerically allocated to either same-rack module. Allocation and intervening rack forces/couples remain UNKNOWN; do not add these rows twice.',
                equations=['sum(F_support + F_pad + F_curtain + F_rack_exchange) = required_external_wrench_sum.force_n',
                           'sum(M_support + M_pad + M_curtain + M_rack_exchange + (application-origin) cross F) = required_external_wrench_sum.moment_nm',
                           'same-rack allocations plus remaining rack boundary must recover each saved upper-guide wrench once'],
                reactions=None,couple_transfer=None,
                accounting='Old receiver stock/local retained gravity used once per pair; retained-member detail is not added again. New parts occur in one module. These local equations do not add another global mass charge.'))
        budgets=copy.deepcopy(old['complete_known_budgets'])
        for budget in budgets.values():
            for k in ('construction_known_kg','all_up_before_fixed_water_kg','all_up_with_fixed_water_kg'):budget[k]+=added
            for k in ('raw_margin_kg','after_fixed_water_margin_kg','no_retirement_raw_margin_kg','no_retirement_fixed_water_margin_kg'):budget[k]-=added
            budget['I041_increment_kg']=added
            budget['physical_margin']='UNKNOWN; deduct U+C once from each displayed conditional known margin.'
            budget.pop('delta_from_I030_margin_kg',None)
        out.append(dict(altitude_m=old['altitude_m'],superheat_k=old['superheat_k'],
            rows=old['rows'],inventory=old['inventory'],modules=modules,complete_known_budgets=budgets,
            saved_total_paid_nominal_gravity_wrench=old['total_paid_nominal_gravity_wrench'],
            new_global_gravity_wrench=wrench(stock.parts,[0.,0.,0.]),
            combined_enumerated_nominal_gravity_wrench=sum_wrenches([old['total_paid_nominal_gravity_wrench'],wrench(stock.parts,[0.,0.,0.])],[0.,0.,0.]),
            other_construction_CG='UNKNOWN; no invented whole-vehicle CG.',physical_float='NOT SHOWN'))
    return out


def main():
    assert sys.argv[1:]==['--write'], 'Only the fixed --write payload is supported'
    here=Path(__file__).resolve().parent
    source=json.loads((here/'sources.json').read_text())
    for row in source['inputs']:
        path=(here/row['path']).resolve();raw=path.read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'], row['path']
    baseline=json.loads((here/'baseline.json').read_text());previous=baseline['predecessor']
    assert [(s['altitude_m'],s['superheat_k']) for s in previous['states']]==[(0,0),(0,10),(2500,0),(2500,10)]
    assert len(previous['states'])==4 and all(len(s['rows'])==8 for s in previous['states'])
    c=Stock();c.build(baseline['saved_receivers'])
    assert len({p['id'] for p in c.parts})==len(c.parts)
    added=sum(p['mass_kg'] for p in c.parts)
    groups={}
    for p in c.parts:groups[p['group']]=groups.get(p['group'],0.)+p['mass_kg']
    reconciliation=[dict(id=p['id'],before_kg=p['mass_kg'],retained_kg=p['mass_kg'],removed_kg=0.,new_kg=0.,after_kg=p['mass_kg'],cg=p['cg']) for p in previous['parts']]
    reconciliation += [dict(id=p['id'],before_kg=0.,retained_kg=0.,removed_kg=0.,new_kg=p['mass_kg'],after_kg=p['mass_kg'],cg=p['cg']) for p in c.parts]
    result=dict(calculator_sha256=digest(Path(__file__)),baseline_sha256=digest(here/'baseline.json'),
        sources_sha256=digest(here/'sources.json'),base=source['base'],base_tree=source['base_tree'],
        design=source['design'],modules=c.modules,new_parts=c.parts,new_objects=c.objects,
        weld_seams=c.seams,bolt_stacks=c.bolts,interfaces=c.joints,
        retained_parts=previous['parts'],retained_geometry_reference='baseline.json:predecessor',
        mass=dict(before_conditional_kg=previous['mass']['construction_known_kg'],
            before_no_retirement_kg=previous['mass']['no_retirement_construction_kg'],
            added_kg=added,removed_kg=0.,qualified_retirement_count=0,
            construction_known_kg=previous['mass']['construction_known_kg']+added,
            no_retirement_construction_kg=previous['mass']['no_retirement_construction_kg']+added,
            new_groups_kg=groups,new_nominal_CG_m=mul(total(mul(p['cg'],p['mass_kg']) for p in c.parts),1/added),
            reconciliation=reconciliation,old_credit_subtracted_again_kg=0.,
            other_construction_CG='UNKNOWN',unpriced='U+C; subtract once from each margin'),
        geometry=geometry(c,baseline),states=states(c,baseline),
        inventory=previous['inventory'],fixed_water_kg=previous['fixed_water_kg'],
        inherited_qualifications=previous['inherited_qualifications'],inherited_summary=previous['summary'],
        route_rows='All 32 saved rows preserved without numerical reevaluation.',
        physical_float='NOT SHOWN',capacity='UNKNOWN',pressure='FAIL carried',
        weakest_assumption='Unilateral cage/old-node contact and the two-level rack path can transfer couples without dominant unsized completion or unproved stiffness.',
        next_change='UNISSUED hypothesis only: paid local box-wall/diaphragm reinforcement at the same eight R datums. Not implemented or credited.')
    text=json.dumps(result,indent=2,allow_nan=False)+'\n'
    (here/'saddle.json').write_text(text)
    print(text,end='')


if __name__=='__main__':main()
