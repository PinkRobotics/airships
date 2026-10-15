"""One fixed raised-crown construction, using saved data and the standard library.

The arithmetic is a conditional construction/route screen. It neither solves
the indeterminate frame nor qualifies the inherited gas, connections or lift.
No ancestor code is imported or executed. JSON is emitted on stdout once.
"""
from pathlib import Path
import copy
import hashlib
import itertools
import json
import math
import sys


def add(a, b): return [x+y for x, y in zip(a, b)]
def sub(a, b): return [x-y for x, y in zip(a, b)]
def scale(a, s): return [x*s for x in a]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def norm(a): return math.sqrt(dot(a, a))
def unit(a):
    size = norm(a)
    if size < 1e-12: raise ValueError('Degenerate selected axis; no geometry substitution')
    return scale(a, 1/size)
def mid(a, b): return scale(add(a, b), 0.5)
def total(values):
    out = [0., 0., 0.]
    for v in values: out = add(out, v)
    return out
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def product(values): return math.prod(values)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def gravity(m): return [0., 0., -D['gravity_m_s2']*m]
def frame(axis):
    e = unit(axis)
    seed = [0., 0., 1.]
    v = sub(seed, scale(e, dot(e, seed)))
    if norm(v) < 1e-10:
        seed = [1., 0., 0.]
        v = sub(seed, scale(e, dot(e, seed)))
    v = unit(v)
    return e, v, cross(e, v)
def at(origin, axes, coords):
    return add(origin, total(scale(a, x) for a, x in zip(axes, coords)))


def point_segment(point, a, b):
    ab = sub(b, a)
    den = dot(ab, ab)
    t = clamp(dot(sub(point, a), ab)/den) if den else 0.
    witness = add(a, scale(ab, t))
    return norm(sub(point, witness)), witness, t


def segment_segment(a, b, c, d):
    """Exact closest points on two finite straight segments, including points."""
    u, v, w = sub(b, a), sub(d, c), sub(a, c)
    aa, bb, cc, dd, ee = dot(u,u), dot(u,v), dot(v,v), dot(u,w), dot(v,w)
    if aa < 1e-24:
        dist, q, _ = point_segment(a, c, d)
        return dist, a, q
    if cc < 1e-24:
        dist, p, _ = point_segment(c, a, b)
        return dist, p, c
    den = aa*cc-bb*bb
    s = clamp((bb*ee-cc*dd)/den) if den > 1e-20*aa*cc else 0.
    t = (bb*s+ee)/cc
    if t < 0.: t, s = 0., clamp(-dd/aa)
    elif t > 1.: t, s = 1., clamp((bb-dd)/aa)
    p, q = add(a,scale(u,s)), add(c,scale(v,t))
    return norm(sub(p,q)), p, q


def bend(a, intersection, b):
    incoming, outgoing = unit(sub(intersection,a)), unit(sub(b,intersection))
    theta = math.acos(clamp(dot(incoming,outgoing), -1., 1.))
    axis = unit(cross(incoming,outgoing))
    radius = D['guide_radius_m']
    tangent = radius*math.tan(theta/2)
    entry = sub(intersection,scale(incoming,tangent))
    exit_point = add(intersection,scale(outgoing,tangent))
    centre = add(entry,scale(unit(cross(axis,incoming)),radius))
    r0 = unit(sub(entry,centre)); r1 = cross(axis,r0)
    count = D['guide_arc_chords']
    points = [add(centre,scale(add(scale(r0,math.cos(theta*k/count)),
                                  scale(r1,math.sin(theta*k/count))),radius))
              for k in range(count+1)]
    # The analytic endpoint is retained to avoid accumulated endpoint drift.
    points[0], points[-1] = entry, exit_point
    cg = add(centre,scale(add(scale(r0,math.sin(theta)/theta),
                              scale(r1,(1-math.cos(theta))/theta)),radius))
    return dict(intersection=intersection,centre=centre,entry=entry,exit=exit_point,
                u_in=incoming,u_out=outgoing,axis=axis,angle_rad=theta,radius_m=radius,
                tangent_length_m=tangent,arc_length_m=radius*theta,cg=cg,points=points,
                chord_error_m=radius*(1-math.cos(theta/(2*count))))


class Construction:
    def __init__(self):
        self.original = copy.deepcopy(B['predecessor']['parts'])
        remove_groups = {'receiver_members','receiver_plates_gussets_pins_bolts',
                         'guide_arms','eight_replacement_ropes'}
        self.removed = [p for p in self.original if p['group'] in remove_groups]
        self.parts = [copy.deepcopy(p) for p in self.original if p['group'] not in remove_groups]
        self.new = []
        # Only explicitly replaced objects are rebuilt. All old rack/root/pad/
        # curtain/lower-contact objects and every fixed obstacle are retained.
        replace_roles = {'hoop_sector','receiver_members','receiver_joint','splice',
                         'guard','rope','tail','socket','actuator','guide_arms'}
        self.objects = [dict(o, origin='retained', cluster='retained:'+o['id'])
                        for o in B['predecessor']['objects'] if o['role'] not in replace_roles]
        self.interfaces = []; self.seams = []; self.sectors = []; self.supports = []
        self.guides = []; self.routes = []; self.boxes = []; self.splices = []
        self.relocations = []

    def find(self, name):
        return next(p for p in self.parts if p['id']==name)

    def relocate(self, name, cg, boundary):
        part = self.find(name)
        self.relocations.append(dict(id=name,old_cg=part['cg'],new_cg=cg,
                                     mass_kg=part['mass_kg'],solid_volume_m3=part['solid_volume_m3']))
        part['cg'] = cg; part['boundary'] = boundary
        part['reuse'] = 'Existing whole named part retained and relocated, paid once.'
        return part

    def part(self, name, volume, density, cg, group, boundary, **details):
        p = dict(id=name,mass_kg=volume*density,solid_volume_m3=volume,cg=cg,
                 group=group,boundary=boundary,**details)
        self.parts.append(p); self.new.append(p)
        return p

    def allowance(self, name, kg, density, cg, group, boundary):
        return self.part(name,kg/density,density,cg,group,boundary,
                         qualification='Paid material allowance; no assembly or load-path qualification.')

    def obj(self, name, a, b, radius, role, cluster, *, error=0., host=None, **details):
        item = dict(id=name,a=a,b=b,radius_m=radius+error,role=role,cluster=cluster,
                    curve_error_m=error,host=host,origin='I034',**details)
        self.objects.append(item)
        return item

    def plate(self, name, centre, axes, dimensions, boundary, group, cluster, density=None):
        density = D['aluminium_density_kg_m3'] if density is None else density
        p = self.part(name,product(dimensions),density,centre,group,boundary,
                      dimensions_m=dimensions,axes=axes,hole_credit_m3=0.)
        vertices = [at(centre,axes,[sign[k]*dimensions[k]/2 for k in range(3)])
                    for sign in itertools.product((-1,1), repeat=3)]
        self.obj(name,centre,centre,norm(dimensions)/2,'plate',cluster,
                 represented_shape='Oriented full blank; sphere is a conservative collision enclosure.',
                 vertices=vertices,axes=axes,dimensions_m=dimensions)
        return p

    def seam(self, name, a, b, boundary, cluster):
        length = norm(sub(b,a)); leg = D['fillet_leg_m']
        # Full triangular nominal bead, with no overlap or penetration credit.
        p = self.part(name,0.5*leg*leg*length,D['aluminium_density_kg_m3'],mid(a,b),
                      'nominal_fillet_welds',boundary,path=[a,b],leg_m=leg,
                      qualification='Paid nominal weld bead; strength, HAZ, access and fit UNKNOWN.')
        self.seams.append(dict(id=name,path=[a,b],length_m=length,nominal_leg_m=leg,
                               mass_kg=p['mass_kg'],boundary=boundary))
        self.obj(name,a,b,leg,'weld',cluster)

    def perimeter(self, name, centre, v, w, width, height, boundary, cluster):
        corners = [add(centre,add(scale(v,x*width/2),scale(w,y*height/2)))
                   for x,y in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for k in range(4): self.seam(name+str(k),corners[k],corners[(k+1)%4],boundary,cluster)

    def tube(self, name, a, b, dimensions, group, boundary):
        width, wall = dimensions; length = norm(sub(b,a)); e,v,w = frame(sub(b,a))
        area = width**2-(width-2*wall)**2
        p = self.part(name,area*length,D['aluminium_density_kg_m3'],mid(a,b),group,boundary,
                      endpoints=[a,b],length_m=length,outer_width_m=width,wall_m=wall,
                      axes=[e,v,w],section_and_capacity='UNKNOWN; no inherited stress proxy.')
        self.obj(name,a,b,width/math.sqrt(2),'tube',name,
                 outer_width_m=width,wall_m=wall,axes=[e,v,w])
        return p

    def bolt(self, name, face, e, v, w, xy, family, length, grip_known, boundary, cluster):
        diameter = 0.024 if family=='M24' else 0.020
        backer = D[family+'_backer_m']; washer = D[family+'_washer_m']
        head = D[family+'_head_m']; nut = D[family+'_nut_m']
        centre = add(face,add(scale(v,xy[0]),scale(w,xy[1])))
        # Positions are a nominal axial stack measured from the head bearing face.
        # Unknown mating/grip stock is not filled in with invented receiver walls.
        definitions = [
            ('shank',math.pi*diameter**2/4*length,length/2),
            ('head',math.sqrt(3)/2*head[0]**2*head[1],-head[1]/2),
            ('near-washer',math.pi*(washer[0]**2-washer[1]**2)/4*washer[2],washer[2]/2),
            ('backer',product(backer),washer[2]+backer[2]/2),
            ('far-washer',math.pi*(washer[0]**2-washer[1]**2)/4*washer[2],grip_known+washer[2]*1.5),
            ('nut',math.sqrt(3)/2*nut[0]**2*nut[1],grip_known+2*washer[2]+nut[1]/2)]
        components = [dict(id=label,solid_volume_m3=vol,mass_kg=vol*D['steel_density_kg_m3'],
                           cg=add(centre,scale(e,z))) for label,vol,z in definitions]
        volume = sum(c['solid_volume_m3'] for c in components)
        cg = scale(total(scale(c['cg'],c['solid_volume_m3']) for c in components),1/volume)
        self.part(name,volume,D['steel_density_kg_m3'],cg,'bolts_backers_washers_heads_nuts',boundary,
                  components=components,diameter_m=diameter,shank_length_m=length,
                  grip_known_m=grip_known,full_shank_paid=True)
        a=add(centre,scale(e,-head[1])); b=add(centre,scale(e,length+D['thread_runout_m']))
        self.obj(name,a,b,max(norm(backer[:2])/2,head[0]/math.sqrt(3),washer[0]/2),
                 'bolt_assembly',cluster,shank=[centre,add(centre,scale(e,length))],
                 shank_diameter_m=diameter,hole_diameter_m=D['support_hole_m'] if family=='M24' else D['arm_hole_m'])
        required=grip_known+2*washer[2]+nut[1]+D['thread_runout_m']
        return dict(id=name,centre=centre,axis=e,nominal_known_grip_m=grip_known,
                    minimum_required_shank_m=required,selected_shank_m=length,
                    known_stack_fits=required<=length,
                    extra_mating_wall_and_oblique_stack='UNKNOWN; arithmetic fit does not certify grip.')

    def box(self, label, centre):
        boundary=label; cluster=label; axes=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]
        extent=0.4; thickness=0.02; faces=[]
        for normal in range(3):
            others=[i for i in range(3) if i!=normal]
            for sign in (-1,1):
                cg=add(centre,scale(axes[normal],sign*(extent-thickness/2)))
                self.plate(label+f'-face{normal}-{sign}',cg,
                           [axes[others[0]],axes[others[1]],axes[normal]],D['node_plate_m'],
                           boundary,'node_box_full_blanks',cluster)
                faces.append(dict(normal=scale(axes[normal],sign),outer_centre=add(centre,scale(axes[normal],sign*extent))))
        # Two full central orthogonal diaphragm blanks; their intersections are
        # retained as assembly conflicts, never volume-subtracted.
        for k,normal in enumerate((0,1)):
            others=[i for i in range(3) if i!=normal]
            self.plate(label+f'-diaphragm{k}',centre,[axes[others[0]],axes[others[1]],axes[normal]],
                       D['node_plate_m'],boundary,'node_box_full_blanks',cluster)
            self.perimeter(label+f'-diaphragm{k}-seam',centre,axes[others[0]],axes[others[1]],0.8,0.8,boundary,cluster)
        # Twelve external cube-edge seams.
        for direction in range(3):
            others=[i for i in range(3) if i!=direction]
            for signs in itertools.product((-1,1),repeat=2):
                c=add(centre,total(scale(axes[j],sign*extent) for j,sign in zip(others,signs)))
                self.seam(label+f'-edge{direction}-{signs[0]}-{signs[1]}',
                          sub(c,scale(axes[direction],extent)),add(c,scale(axes[direction],extent)),boundary,cluster)
        self.boxes.append(dict(id=label,centre=centre,dimensions_m=D['node_box_m'],faces=faces,
                               full_blanks=8,capacity='UNKNOWN',
                               assembly='Full-blank corner/diaphragm intersections retained; no unpriced notches or node fixity.'))

    def connection(self, name, point, outward, width, arm, boundary, box_face_normal=None):
        e,v,w=frame(outward); axes=[v,w,e]; cluster=name
        prefix='arm' if arm else 'support'; family='M20' if arm else 'M24'
        plate=D[prefix+'_endplate_m']; backer=D[prefix+'_backer_m']; gusset=D[prefix+'_gusset_m']
        self.plate(name+'-endplate',point,axes,plate,boundary,'connection_plates',cluster)
        for k in range(2):
            c=add(point,scale(e,-plate[2]/2-(k+0.5)*backer[2]))
            self.plate(name+f'-backer{k}',c,axes,backer,boundary,'connection_backers',cluster)
        # Four whole gusset blanks oriented in the two longitudinal member planes.
        for k,(radial,transverse) in enumerate([(v,w),(scale(v,-1),w),(w,v),(scale(w,-1),v)]):
            c=add(point,add(scale(e,gusset[0]/2),scale(radial,width/2+gusset[1]/2)))
            self.plate(name+f'-gusset{k}',c,[e,radial,transverse],gusset,boundary,'connection_gussets',cluster)
            self.seam(name+f'-gusset{k}-tube',add(point,scale(radial,width/2)),
                      add(point,add(scale(e,gusset[0]),scale(radial,width/2))),boundary,cluster)
            self.seam(name+f'-gusset{k}-plate',add(point,scale(radial,width/2)),
                      add(point,scale(radial,width/2+gusset[1])),boundary,cluster)
        self.perimeter(name+'-tube-seam',point,v,w,width,width,boundary,cluster)
        grip=plate[2]+2*backer[2]+D[family+'_backer_m'][2]
        rows=[self.bolt(name+f'-bolt{k}',point,e,v,w,xy,family,D[prefix+'_bolt_m'][1],grip,boundary,cluster)
              for k,xy in enumerate(D[prefix+'_bolt_xy_m'])]
        hole=D[prefix+'_hole_m']; wall=D['arm_rhs_m' if arm else 'support_rhs_m'][1]
        edge=min(min(plate[0]/2-abs(x),plate[1]/2-abs(y))-hole/2 for x,y in D[prefix+'_bolt_xy_m'])
        # A hole intersects the tube end if its disc reaches the square wall band.
        conflicts=[]
        for k,(x,y) in enumerate(D[prefix+'_bolt_xy_m']):
            nearest=max(abs(x),abs(y)); r=hole/2
            if nearest+r>=width/2-wall and nearest-r<=width/2:
                conflicts.append(k)
        aligned=None if box_face_normal is None else abs(dot(e,box_face_normal))>=1-1e-10
        row=dict(id=name,point=point,axes=[e,v,w],endplate_m=plate,bolts=rows,
                 minimum_hole_edge_ligament_m=edge,tube_wall_hole_conflicts=conflicts,
                 box_face_normal=box_face_normal,plate_parallel_to_box_face=aligned,
                 completion='UNKNOWN: oblique intersecting box/fork face, wall grip, access and gusset attachment are not a resolved adapter.',
                 couple_capacity='UNKNOWN',bolt_capacity='UNKNOWN',weld_capacity='UNKNOWN')
        self.interfaces.append(row)
        return row

    def build(self):
        self.Q=[[*r['old_ring_point'][:2],D['z_m']] for r in B['saved_receivers']]
        self.R=[r['existing_receiver_xyz_m'] for r in B['saved_receivers']]
        for j,saved in enumerate(B['saved_sectors']):
            a,b=saved['angles_rad']; count=D['sector_chords']
            # Exact saved x/y coordinates and angular discretisation are retained.
            points=[[p[0],p[1],D['z_m']] for p in saved['points']]
            cg=[saved['cg'][0],saved['cg'][1],D['z_m']]
            sector=self.relocate(f'hoop-sector{j}',cg,f'sector{j}')
            error=D['radius_m']*(1-math.cos(abs(b-a)/(2*count)))
            for k,(p,q) in enumerate(zip(points,points[1:])):
                self.obj(f'crown-sector{j}-chord{k}',p,q,0.5/math.sqrt(2),'sector',f'sector{j}',error=error)
            self.sectors.append(dict(id=j,endpoints=[self.Q[j],self.Q[(j+1)%8]],points=points,
                                     angles_rad=[a,b],length_m=saved['length_m'],cg=cg,
                                     mass_kg=sector['mass_kg'],chord_error_m=error))
            self.relocate(f'splice{j}',self.Q[j],f'Q{j}')
            self.relocate(f'isolation{j}',self.Q[j],f'Q{j}')
            self.relocate(f'earthing{j}',self.R[j],f'R{j}')
            self.relocate(f'access{j}',cg,f'sector{j}')
            self.box(f'Q{j}',self.Q[j]); self.box(f'R{j}',self.R[j])
            self.allowance(f'R{j}-isolation',4,1400,self.R[j],'node_isolation',f'R{j}')
            self.allowance(f'R{j}-temporary-brace-stock',10,2700,self.R[j],'temporary_assembly_stock',f'R{j}')
            # Physical reuse of the complete four-cover/sixteen-shank splice.
            angle=a; tangent=[math.sin(angle),-math.cos(angle),0.]; radial=[math.cos(angle),math.sin(angle),0.]; z=[0.,0.,1.]
            for k,(n,side) in enumerate([(z,1),(z,-1),(radial,1),(radial,-1)]):
                transverse=radial if k<2 else z; c=add(self.Q[j],scale(n,side*0.26))
                vertices=[at(c,[tangent,transverse,n],[u*0.4,v*0.175,w*0.01]) for u,v,w in itertools.product((-1,1),repeat=3)]
                self.obj(f'splice{j}-cover{k}',c,c,norm([.8,.35,.02])/2,'splice_cover',f'Q{j}',vertices=vertices,
                         mass_source=f'splice{j}; already retained, no second charge')
            bolts=[]
            for axis_index,(axis,transverse) in enumerate([(radial,z),(z,radial)]):
                for k,(u,v) in enumerate(itertools.product((-.3,-.1,.1,.3),(-.1,.1))):
                    c=add(self.Q[j],add(scale(tangent,u),scale(transverse,v)))
                    ends=[sub(c,scale(axis,.28)),add(c,scale(axis,.28))]
                    self.obj(f'splice{j}-shank{axis_index}-{k}',*ends,.012,'splice_shank',f'Q{j}',
                             hole_diameter_m=.026,head_nut_washer_allowance_kg=.5)
                    bolts.append(dict(axis=axis,endpoints=ends,diameter_m=.024,length_m=.56,hole_m=.026))
            self.splices.append(dict(id=j,covers=4,bolts=bolts,known_outer_grip_m=.54,shank_m=.56,
                                      remaining_for_head_nut_threads_m=.02,edge_ligament_m=.087,
                                      fit='UNKNOWN: paid 0.5kg head/nut/washer allowance has no complete axial dimensions; node intersection retained.',
                                      force_couple_capacity='UNKNOWN'))
            for kind in ('main','brace'):
                target=j if kind=='main' else (j+1)%8
                a=add(self.Q[j],[0,0,-.4 if kind=='main' else .4])
                b=add(self.R[target],[-.4 if kind=='main' else .4,0,0])
                name=f'{kind}{j}'; e=unit(sub(b,a))
                member=self.tube(name,a,b,D['support_rhs_m'],'main_legs' if kind=='main' else 'braces',name)
                ca=self.connection(name+'-Q',a,e,.3,False,name,[0,0,-1 if kind=='main' else 1])
                cb=self.connection(name+'-R',b,scale(e,-1),.3,False,name,[-1 if kind=='main' else 1,0,0])
                self.supports.append(dict(id=name,Q=j,R=target,endpoints=[a,b],axis=e,
                                          mass_kg=member['mass_kg'],connections=[ca['id'],cb['id']],
                                          end_force_and_couple='UNKNOWN: compatible frame/receiver reactions not solved.'))
            # Two added doubler blanks at the stated receiver, normal +/-x.
            for sign in (-1,1):
                c=self.R[j]
                self.plate(f'R{j}-saddle{sign}',c,[[0,1,0],[0,0,1],[sign,0,0]],D['receiver_doubler_m'],f'R{j}','receiver_saddles',f'R{j}')
                self.perimeter(f'R{j}-saddle{sign}-seam',c,[0,1,0],[0,0,1],.8,.6,f'R{j}',f'R{j}')
            receiver_bolts=[self.bolt(f'R{j}-through{k}',self.R[j],[1,0,0],[0,1,0],[0,0,1],xy,
                                      'M24',.5,.04+.012,f'R{j}',f'R{j}') for k,xy in enumerate(D['receiver_bolt_yz_m'])]
            self.interfaces.append(dict(id=f'R{j}-rack-saddle',point=self.R[j],bolts=receiver_bolts,
                                         old_receiver_wall_grip='UNKNOWN',selected_shank_m=.5,
                                         actual_rack_interface='UNKNOWN: full saddle blanks are located at the specified receiver datum with +/-x normals; their separate mating-face offsets and bolt axial datum remain unresolved, never invented from the new node size.',
                                         couple_capacity='UNKNOWN',completion='UNKNOWN'))
        self.build_routes()
        assert len({p['id'] for p in self.parts})==len(self.parts)
        assert len(self.supports)==16 and len(self.boxes)==16 and len(self.guides)==16

    def build_routes(self):
        for i,old in enumerate(B['saved_route_datums']):
            h=old['host']; low=old['low_xyz_m']; H=old['fixed_upper_anchor_xyz_m']
            G0=[*old['old_lower_intersection_xyz_m'][:2],18.]; G1=old['retained_upper_intersection_xyz_m']
            last=unit(sub(H,G1)); endpoint=sub(H,scale(last,D['nominal_actuator_m']))
            bends=[bend(low,G0,G1),bend(G0,G1,H)]
            spans=[[low,bends[0]['entry']],[bends[0]['exit'],bends[1]['entry']],[bends[1]['exit'],endpoint]]
            lengths=[norm(sub(q,p)) for p,q in spans]
            geometric=sum(lengths)+sum(be['arc_length_m'] for be in bends)
            free=math.ceil(geometric/D['free_stock_increment_m'])*D['free_stock_increment_m']
            tails=[[low,add(low,scale(bends[0]['u_in'],1.))],[endpoint,sub(endpoint,scale(last,1.))]]
            pieces=[dict(id=f'rope{h}-straight{k}',length_m=length,cg=mid(*span),shape=span)
                    for k,(span,length) in enumerate(zip(spans,lengths))]
            pieces += [dict(id=f'rope{h}-bend{k}',length_m=be['arc_length_m'],cg=be['cg']) for k,be in enumerate(bends)]
            pieces += [dict(id=f'rope{h}-tail{k}',length_m=1.,cg=mid(*tail),shape=tail) for k,tail in enumerate(tails)]
            surplus=free-geometric
            # The small rounded surplus is explicitly an unresolved laid-out
            # shape. The nominal endpoint allocation is disclosed, not a fit.
            pieces += [dict(id=f'rope{h}-rounding-stock',length_m=surplus,cg=mid(low,endpoint),
                            actual_distribution='UNKNOWN; nominal half at each termination for the conditional gravity calculation.')]
            paid=free+2.; cg=scale(total(scale(p['cg'],p['length_m']) for p in pieces),1/paid)
            self.part(f'crown-rope{h}',paid*ROPE_VOLUME_PER_M,ROPE_MASS_PER_M/ROPE_VOLUME_PER_M,cg,
                      'replacement_rope_and_two_tails',f'route{h}',pieces=pieces,free_length_m=free,
                      paid_length_m=paid,actual_loaded_cg='UNKNOWN; nominal geometry and rounding allocation only.')
            for k,(p,q) in enumerate(spans):self.obj(f'rope{h}-straight{k}',p,q,D['rope_enclosure_radius_m'],'rope',f'route{h}',host=h)
            for k,be in enumerate(bends):
                for j,(p,q) in enumerate(zip(be['points'],be['points'][1:])):
                    self.obj(f'rope{h}-bend{k}-{j}',p,q,D['rope_enclosure_radius_m'],'rope',f'route{h}',host=h,error=be['chord_error_m'])
                self.relocate(f'guide{h}-{k}',be['centre'],f'guide{h}-{k}')
                self.obj(f'guide{h}-{k}-guard',be['centre'],be['centre'],.6,'guard',f'guide{h}-{k}',host=h,
                         paid_composite='Saved body/axle/bearings/guard/saddle row retained whole; internal contact geometry UNKNOWN.')
                bearing_points=[sub(be['centre'],scale(be['axis'],.06)),add(be['centre'],scale(be['axis'],.06))]
                self.obj(f'guide{h}-{k}-axle',*bearing_points,.03,'axle',f'guide{h}-{k}',host=h)
                a,b=be['centre'],be['intersection']; name=f'arm{h}-{k}'
                self.tube(name,a,b,D['arm_rhs_m'],'new_guide_arms',f'guide{h}-{k}')
                axis=unit(sub(b,a))
                self.connection(name+'-guide',a,axis,.15,True,f'guide{h}-{k}')
                self.connection(name+'-support',b,scale(axis,-1),.15,True,f'guide{h}-{k}')
                access_a=add(be['centre'],scale(be['axis'],.06)); access_b=add(access_a,scale(be['axis'],.8))
                self.obj(f'guide{h}-{k}-access',access_a,access_b,.3,'access',f'guide{h}-{k}',host=h,
                         exact_cylinder_diameter_m=.6,exact_cylinder_length_m=.8,
                         qualification='Capsule conservatively encloses cylinder; no clearance inferred from stock payment.')
                self.obj(f'guide{h}-{k}-axle-removal',access_a,access_b,.03,'axle_removal',f'guide{h}-{k}',host=h)
                self.guides.append(dict(host=h,guide=k,bend=be,bearing_points=bearing_points,arm_endpoints=[a,b],
                                        guard_radius_m=.6,groove_width_m=.026,groove_root_radius_m=.01,
                                        rope_radial_fit_in_groove=(.018/2<=.01),
                                        composite_fork_interface='UNKNOWN; no guide body components or moment discarded.'))
            self.relocate(f'rope{h}-lower-termination',low,f'lower{h}')
            self.relocate(f'rope{h}-upper-termination',endpoint,f'upper{h}')
            self.relocate(f'actuator{h}',mid(endpoint,H),f'upper{h}')
            self.find(f'lower-contact{h}')['boundary']=f'lower{h}'
            self.obj(f'rope{h}-lower-socket',low,low,.12,'socket',f'lower{h}',host=h)
            self.obj(f'rope{h}-upper-socket',endpoint,endpoint,.12,'socket',f'upper{h}',host=h)
            self.obj(f'actuator{h}',endpoint,H,B['inherited']['bag_adjuster']['od_m']/2,'actuator',f'upper{h}',host=h)
            for k,tail in enumerate(tails):self.obj(f'rope{h}-tail{k}',*tail,D['rope_enclosure_radius_m'],'tail',f'route{h}',host=h)
            fits=(bends[0]['tangent_length_m']<norm(sub(G0,low)) and
                  bends[0]['tangent_length_m']+bends[1]['tangent_length_m']<norm(sub(G1,G0)) and
                  bends[1]['tangent_length_m']+1.<norm(sub(H,G1)))
            self.routes.append(dict(host=h,bag=old['bag'],low=low,top=H,endpoint=endpoint,
                                    G0=G0,G1=G1,bends=bends,segments=spans,segment_lengths_m=lengths,
                                    geometric_length_m=geometric,free_length_m=free,paid_length_m=paid,
                                    pre_load_rounding_surplus_m=surplus,tails=tails,rope_pieces=pieces,
                                    finite_tangencies_fit=fits,nominal_actuator_m=1.,
                                    loaded_geometry='UNKNOWN; current geometry is unloaded construction, never a loaded clearance claim.'))


def wrench(origin, forces=(), parts=()):
    """Full vector wrench; forces are (point, force, free couple) triples."""
    f=[0.,0.,0.]; m=[0.,0.,0.]
    for point,force,couple in forces:
        f=add(f,force); m=add(m,add(cross(sub(point,origin),force),couple))
    for part in parts:
        force=gravity(part['mass_kg'])
        f=add(f,force);m=add(m,cross(sub(part['cg'],origin),force))
    return dict(origin_m=origin,force_n=f,moment_nm=m)


def negative_wrench(value):
    return dict(origin_m=value['origin_m'],force_n=scale(value['force_n'],-1),moment_nm=scale(value['moment_nm'],-1))


def nominal_rope_gravity(route):
    """A disclosed simply-supported gravity allocation, with exact nominal sum.

    Straight-span half weights act at their two endpoints; arc and tail weights
    retain their own CG moments. This is not a solved unequal-tension catenary.
    """
    out={'lower':[],'guide0':[],'guide1':[],'upper':[]}
    names=[('lower','guide0'),('guide0','guide1'),('guide1','upper')]
    for k,(span,length,ends) in enumerate(zip(route['segments'],route['segment_lengths_m'],names)):
        for j,key in enumerate(ends):
            out[key].append(dict(id=f'straight{k}-endpoint{j}',mass_kg=ROPE_MASS_PER_M*length/2,cg=span[j],
                                 meaning='Equivalent nominal gravity reaction at endpoint; not a second rope mass.'))
    for k,be in enumerate(route['bends']):
        out[f'guide{k}'].append(dict(id=f'bend{k}',mass_kg=ROPE_MASS_PER_M*be['arc_length_m'],cg=be['cg']))
    for k,key in enumerate(('lower','upper')):
        out[key].append(dict(id=f'tail{k}',mass_kg=ROPE_MASS_PER_M,cg=mid(*route['tails'][k])))
        out[key].append(dict(id=f'rounding-stock-half{k}',mass_kg=ROPE_MASS_PER_M*route['pre_load_rounding_surplus_m']/2,
                             cg=route['low'] if k==0 else route['endpoint'],
                             qualification='Conditional endpoint allocation; actual excess-stock shape UNKNOWN.'))
    return out


def mass_ledger(c):
    old=B['predecessor']['mass']; removed=sum(p['mass_kg'] for p in c.removed)
    added=sum(p['mass_kg'] for p in c.new)
    construction=old['construction_known_kg']-removed+added
    groups={}; removed_groups={}
    for p in c.new: groups[p['group']]=groups.get(p['group'],0.)+p['mass_kg']
    for p in c.removed: removed_groups[p['group']]=removed_groups.get(p['group'],0.)+p['mass_kg']
    new_ids={p['id'] for p in c.new}
    retained_by_id={p['id']:p for p in c.parts if p['id'] not in new_ids}
    removed_by_id={p['id']:p for p in c.removed}
    reconciliation=[]
    for p in c.original:
        new=retained_by_id.get(p['id'])
        reconciliation.append(dict(old_id=p['id'],old_group=p['group'],old_mass_kg=p['mass_kg'],
                                   old_volume_m3=p['solid_volume_m3'],old_cg=p['cg'],
                                   disposition='retained' if new else 'conditionally_replaced',
                                   retained_mass_kg=new['mass_kg'] if new else 0.,
                                   removed_mass_kg=p['mass_kg'] if p['id'] in removed_by_id else 0.,
                                   retained_cg=new['cg'] if new else None,
                                   qualification='No qualified retirement; whole composite guide/receiver-root rows stay charged unless the entire explicitly identified replaceable part is removed.'))
    total_paid=sum(p['mass_kg'] for p in c.parts)
    first_moment=total(scale(p['cg'],p['mass_kg']) for p in c.parts)
    old_paid=sum(p['mass_kg'] for p in c.original)
    material=B['predecessor']['volume']['material_inside_represented_reserve_m3']-sum(p['solid_volume_m3'] for p in c.removed)+sum(p['solid_volume_m3'] for p in c.new)
    return dict(predecessor_known_construction_kg=old['construction_known_kg'],
                conditional_removed_kg=removed,added_kg=added,new_groups_kg=groups,removed_groups_kg=removed_groups,
                construction_known_kg=construction,delta_from_I030_kg=construction-old['construction_known_kg'],
                no_retirement_construction_kg=old['construction_known_kg']+added,
                no_retirement_delta_from_I030_kg=added,qualified_retirement_count=0,
                retained_liners_cuffs_kg=old['retained_penetration_liners_kg'],
                old_I026_to_I030_credit_not_subtracted_again_kg=old['conditional_replacement_removed_kg'],
                equipment_kg=old['equipment_kg'],pressure_hardware_kg=old['pressure_hardware_kg'],
                original_pressure_allowance_counted_once_kg=old['original_pressure_allowance_kg_once'],
                energy_allowance_kg=old['energy_allowance_kg'],propulsion_allowance_kg=old['propulsion_allowance_kg'],
                enumerated_paid_mass_kg=total_paid,enumerated_first_moment_kg_m=first_moment,
                enumerated_nominal_CG_m=scale(first_moment,1/total_paid),
                other_construction_mass_kg=old['construction_known_kg']-old_paid,
                other_construction_CG='UNKNOWN; unchanged saved whole-vehicle inventory is not assigned an invented CG.',
                reconciliation=reconciliation,new_part_ids=[p['id'] for p in c.new],
                ledger_identity_residual_kg=(total_paid-old_paid)-(added-removed),
                material_inside_reserve_m3=material,material_reserve_m3=50.,datum_debit_m3=100.,
                material_amount_within_reserve=material<=50.,physical_volume_closure='UNKNOWN',
                omitted_mass='U: unresolved receiver/rack/hull strengthening. C: unresolved interfaces, grip, notches, weld access and erection. Subtract U+C from every known margin.',
                capacity='UNKNOWN; stock payment is not a stress or connection-capacity bound.')


def load_case(c, index, mass):
    saved=B['states'][index]; rows=[]; route_by_host={}; load_entries=[]
    guide_support_loads={}
    actuator=B['inherited']['bag_adjuster']; zero=[0.,0.,0.]
    for r,dutyrow in zip(c.routes,saved['duties']):
        h=r['host']; assert dutyrow['host']==h
        rope_dead=nominal_rope_gravity(r)
        lower_parts=[p for p in c.parts if p.get('boundary')==f'lower{h}']
        lower_lumps=lower_parts+rope_dead['lower']
        deadmass=sum(p['mass_kg'] for p in lower_lumps)
        u=r['bends'][0]['u_in']; vertical=dutyrow['unchanged_bag_duty_n']+D['gravity_m_s2']*deadmass
        tension=vertical/u[2] if u[2]>0. else None
        if tension is None:
            rows.append(dict(host=h,unchanged_bag_duty_n=dutyrow['unchanged_bag_duty_n'],
                             upward_direction_cosine=u[2],tension_n=None,result='FAIL: selected departure cannot support upward duty.'))
            continue
        lower_traction=scale(u,tension)
        upper_traction=scale(r['bends'][1]['u_out'],-tension)
        ideal=[(r['low'],lower_traction,zero),(r['top'],upper_traction,zero)]
        low_w=wrench(r['low'],[(r['low'],lower_traction,zero)],lower_lumps)
        upper_parts=[p for p in c.parts if p.get('boundary')==f'upper{h}']
        upper_w=wrench(r['top'],[(r['endpoint'],upper_traction,zero)],upper_parts+rope_dead['upper'])
        guide_rows=[]
        for k,be in enumerate(r['bends']):
            traction=scale(sub(be['u_out'],be['u_in']),tension)
            ideal.append((be['centre'],traction,zero))
            paid=[p for p in c.parts if p.get('boundary')==f'guide{h}-{k}']
            body=c.find(f'guide{h}-{k}')
            body_w=wrench(be['centre'],[(be['centre'],traction,zero)],[body]+rope_dead[f'guide{k}'])
            support=wrench(be['intersection'],[(be['centre'],traction,zero)],paid+rope_dead[f'guide{k}'])
            guide_support_loads[(h,k)]=support
            axis=be['axis']; F=body_w['force_n']; M=body_w['moment_nm']
            axial=dot(F,axis); radial=sub(F,scale(axis,axial)); spin=dot(M,axis)
            transverse=sub(M,scale(axis,spin))
            delta=scale(cross(axis,transverse),1/D['bearing_span_m'])
            # These are reactions ON the axle. Axial reaction sharing and spin
            # torque support are deliberately not assigned equal numeric values.
            radial_reactions=[sub(scale(radial,-.5),delta),add(scale(radial,-.5),delta)]
            bearing_points=[sub(be['centre'],scale(axis,.06)),add(be['centre'],scale(axis,.06))]
            guide_rows.append(dict(guide=k,traction_from_rope_n=traction,
                                   body_and_nominal_rope_wrench=body_w,complete_support_wrench=support,
                                   paid_part_ids=[p['id'] for p in paid],rope_gravity_allocation=rope_dead[f'guide{k}'],
                                   bearing_points_m=bearing_points,conditional_radial_reactions_n=radial_reactions,
                                   required_axial_reaction_sum_n=-axial,individual_axial_reactions='UNKNOWN',
                                   unbalanced_spin_torque_nm=spin,contact_rating_friction_fatigue='UNKNOWN',
                                   arm_section_bolts_welds_capacity='UNKNOWN',
                                   bearing_scope='Ideal two supports at the stated span; radial equilibrium only. No contact/fork/axial load-sharing qualification.'))
        sag=[]
        for span,length in zip(r['segments'],r['segment_lengths_m']):
            direction=unit(sub(span[1],span[0])); transverse=math.sqrt(max(0.,1-direction[2]**2))
            q=ROPE_MASS_PER_M*D['gravity_m_s2']*transverse
            displacement=q*length**2/(8*tension); slope=q*length/(2*tension)
            excess=q*q*length**3/(24*tension*tension)
            gaps=[]
            for bag,centre in enumerate(B['inherited']['geometry']['bag_centres']):
                distance,witness,_=point_segment(centre,*span)
                gaps.append(dict(bag=bag,witness=witness,
                                 conditional_sag_enclosure_gap_m=distance-B['inherited']['geometry']['bag_radius_m']-D['rope_enclosure_radius_m']-displacement))
            sag.append(dict(span_m=length,transverse_weight_n_m=q,sag_m=displacement,
                            maximum_slope=slope,small_slope_domain=slope<=D['small_slope_limit'],
                            positive_geometric_excess_m=excess,four_bag_fixed_endpoint_sag_bounds=gaps))
        excess=sum(s['positive_geometric_excess_m'] for s in sag)
        extension=tension*r['free_length_m']/EA
        stretch=tension/actuator['axial_stiffness_n_m']
        command=1+r['geometric_length_m']+excess-r['free_length_m']-extension-stretch
        residual=(r['free_length_m']+extension+command+stretch)-(r['geometric_length_m']+1+excess)
        balance=wrench(zero,ideal)
        load_entries.extend(ideal)
        rw=dict(host=h,bag=r['bag'],unchanged_bag_duty_n=dutyrow['unchanged_bag_duty_n'],
                upward_direction_cosine=u[2],local_lower_dead_mass_kg=deadmass,tension_n=tension,
                lower_wrench=low_w,lower_wrench_about_bag_centre=wrench(B['inherited']['geometry']['bag_centres'][r['bag']],
                    [(r['low'],lower_traction,zero)],lower_lumps),
                lower_gravity_allocation=lower_lumps,upper_anchor_wrench=upper_w,
                upper_gravity_allocation=upper_parts+rope_dead['upper'],guide_loads=guide_rows,
                endpoint_force_on_socket_n=upper_traction,actuator_force_n=tension,
                nominal_rope_action_reaction_force_residual_n=balance['force_n'],
                nominal_rope_action_reaction_moment_residual_nm=balance['moment_nm'],
                sag=sag,axial_extension_m=extension,actuator_stretch_m=stretch,command_m=command,
                positive_sag_identity_residual_m=residual,stroke_pass=D['command_m'][0]<=command<=D['command_m'][1],
                factored_rope_demand_n=D['load_factor']*tension,rope_working_force_n=ROPE_AREA*D['rope_working_pa'],
                rope_strength_pass=D['load_factor']*tension<=ROPE_AREA*D['rope_working_pa'],
                factored_actuator_demand_n=D['load_factor']*tension,
                actuator_saved_conditional_rating_n=actuator['tensile_force_rating_n'],
                actuator_strength_pass=D['load_factor']*tension<=actuator['tensile_force_rating_n'],
                factor_scope='Inherited 1.5 applied to the conditional service traction only; not a dynamic/connection certification.',
                local_domain=all(s['small_slope_domain'] for s in sag),
                loaded_clearance='UNKNOWN; failed stroke/force and unsolved structure/contact invalidate physical fit.',
                model='Nominal equal frictionless traction plus statically balanced distributed-gravity allocation. No loaded catenary/frame compatibility or unequal tension solution.')
        rows.append(rw);route_by_host[h]=rw
    sectors=[]
    for sector in c.sectors:
        j=sector['id']; h=c.routes[j]['host']; gl=guide_support_loads.get((h,0))
        parts=[p for p in c.parts if p.get('boundary')==f'sector{j}']
        forces=[] if gl is None else [(gl['origin_m'],gl['force_n'],gl['moment_nm'])]
        applied=wrench(c.Q[j],forces,parts)
        sectors.append(dict(id=j,endpoints_m=sector['endpoints'],applied_wrench_about_Qj=applied,
                            required_end_wrench_sum=negative_wrench(applied),
                            left_end_force_n=None,left_end_couple_nm=None,right_end_force_n=None,right_end_couple_nm=None,
                            end_requirement='Fleft+Fright=-Fapplied; Mleft+Mright+(Qnext-Qj)xFright=-Mapplied. Each end UNKNOWN without compatible support sharing.',
                            capacity_stiffness='UNKNOWN; no square-RHS vector-magnitude proxy.'))
    supports=[]
    for member in c.supports:
        parts=[p for p in c.parts if p.get('boundary')==member['id']]
        dead=wrench(member['endpoints'][0],parts=parts)
        supports.append(dict(id=member['id'],endpoints_m=member['endpoints'],paid_gravity_wrench=dead,
                             required_end_wrench_sum=negative_wrench(dead),
                             Q_end_force_n=None,Q_end_couple_nm=None,R_end_force_n=None,R_end_couple_nm=None,
                             requirement='End forces sum to opposite paid gravity; end couples plus lever arm complete the moment balance. Node forces and elastic sharing UNKNOWN.',
                             capacity='UNKNOWN'))
    # Receiver labels and paid part IDs are different namespaces (notably
    # rack1 versus rack+1). Map each saved receiver explicitly; do not infer
    # membership from a prefix or add these already-paid parts to c.parts.
    retained_receiver_parts={
        'rack-1-root0': ('rack-1-root-strut0','rack-1-plate-pin0','rack-1-curtain0'),
        'rack-1-root1': ('rack-1-root-strut1','rack-1-plate-pin1','rack-1-curtain1'),
        'rack-1-root2': ('rack-1-root-strut2','rack-1-plate-pin2','rack-1-curtain2'),
        'rack-1-root3': ('rack-1-root-strut3','rack-1-plate-pin3','rack-1-curtain3'),
        'rack1-root0': ('rack+1-root-strut0','rack+1-plate-pin0','rack+1-curtain0'),
        'rack1-root1': ('rack+1-root-strut1','rack+1-plate-pin1','rack+1-curtain1'),
        'rack1-root2': ('rack+1-root-strut2','rack+1-plate-pin2','rack+1-curtain2'),
        'rack1-root3': ('rack+1-root-strut3','rack+1-plate-pin3','rack+1-curtain3'),
    }
    paid_by_id={p['id']:p for p in c.parts}
    receivers=[]
    for j,saved_r in enumerate(B['saved_receivers']):
        retained=[paid_by_id[pid] for pid in retained_receiver_parts[saved_r['existing_receiver_name']]]
        receiver_stock=[p for p in c.parts if p.get('boundary')==f'R{j}']
        local=receiver_stock+retained
        local_gravity=wrench(c.R[j],parts=local)
        retained_members=[]
        for part in retained:
            dead=wrench(c.R[j],parts=[part])
            retained_members.append(dict(id=part['id'],mass_kg=part['mass_kg'],cg_m=part['cg'],
                                         gravity_wrench_about_receiver=dead,
                                         required_external_wrench_sum=negative_wrench(dead),
                                         reactions='UNKNOWN: sum all forces and couples on this retained part about R to the exported requirement; this does not assign its gravity wholly to R or solve attachment sharing.'))
        receivers.append(dict(id=saved_r['existing_receiver_name'],R_m=c.R[j],pad_m=saved_r['retained_pad_xyz_m'],
                              curtain_end_m=saved_r['retained_curtain_end_xyz_m'],
                              local_known_gravity_wrench=local_gravity,
                              retained_path_part_ids=[p['id'] for p in retained],
                              receiver_stock_part_ids=[p['id'] for p in receiver_stock],
                              retained_members=retained_members,
                              required_external_wrench_sum=negative_wrench(local_gravity),
                              retained_part_ids=[p['id'] for p in local],incoming_supports=[f'main{j}',f'brace{(j-1)%8}'],
                              force_n=None,couple_nm=None,pad_force_n=None,pad_couple_nm=None,curtain_demand_n=None,
                              full_boundary='UNKNOWN: both support end wrenches, upper-guide/rack frame loads and external receiver/pad/curtain reactions, transported about R, must sum to required_external_wrench_sum. Known gravity includes the retained root-strut, plate-pin and curtain CGs plus receiver stock; their internal exchanges cancel only for the whole local assembly. No free fixity, equal split, or zero-couple pin.',
                              inventory_scope='Existing paid parts referenced only; no addition to the global inventory or second gravity charge in total_nominal_boundary_wrench.',
                              receiver_wall_grip_and_strengthening='UNKNOWN U+C'))
    nodes=[]
    for j in range(8):
        local=[p for p in c.parts if p.get('boundary')==f'Q{j}']
        nodes.append(dict(id=f'Q{j}',point_m=c.Q[j],local_gravity_wrench=wrench(c.Q[j],parts=local),
                          incident=[f'sector{(j-1)%8}',f'sector{j}',f'main{j}',f'brace{j}'],
                          compatible_force_and_couple='UNKNOWN'))
    budgets={}
    for name,prior in saved['complete_known_budgets'].items():
        p=copy.deepcopy(prior);p['construction_known_kg']=mass['construction_known_kg']
        p['all_up_before_fixed_water_kg']=sum(p[k] for k in ('payload_kg','construction_known_kg','equipment_kg','helium_kg','impurity_air_kg','other_air_kg'))
        p['all_up_with_fixed_water_kg']=p['all_up_before_fixed_water_kg']+B['predecessor']['fixed_water_kg']
        p['raw_margin_kg']=p['gross_displacement_kg']-p['all_up_before_fixed_water_kg']
        p['after_fixed_water_margin_kg']=p['gross_displacement_kg']-p['all_up_with_fixed_water_kg']
        p['no_retirement_raw_margin_kg']=p['raw_margin_kg']-mass['conditional_removed_kg']
        p['no_retirement_fixed_water_margin_kg']=p['after_fixed_water_margin_kg']-mass['conditional_removed_kg']
        p['delta_from_I030_margin_kg']=p['raw_margin_kg']-prior['raw_margin_kg']
        p['inherited_delta_identity_error_kg']=p['delta_from_I030_margin_kg']+mass['delta_from_I030_kg']
        p['physical_margin']='UNKNOWN; matching saved gross displacement/air state is a conditional ledger, not closed volume/shape.'
        budgets[name]=p
    ideal=wrench(zero,load_entries)
    dead=wrench(zero,parts=c.parts)
    combined=wrench(zero,load_entries,c.parts)
    return dict(altitude_m=saved['altitude_m'],superheat_k=saved['superheat_k'],rows=rows,
                sectors=sectors,supports=supports,Q_nodes=nodes,receivers=receivers,
                upper_guide_rack_wrenches=[dict(host=h,**value) for (h,k),value in guide_support_loads.items() if k==1],
                total_paid_nominal_gravity_wrench=dead,total_nominal_boundary_wrench=combined,
                total_ideal_route_internal_force_residual_n=ideal['force_n'],
                total_ideal_route_internal_moment_residual_nm=ideal['moment_nm'],
                boundary_identity='Sum of all ideal rope interface forces/couples is zero; adding each enumerated paid part gravity once gives the exported total. This accounting identity is not a compatible global equilibrium, and excludes unlocated whole-vehicle CG and U+C.',
                complete_known_budgets=budgets,inventory=saved['inventory'],physical_float='NOT SHOWN')


def geometry(c):
    geo=B['inherited']['geometry']; bag_rows=[]; hull_rows=[]
    for obj in c.objects:
        error=obj.get('curve_error_m',0.)
        for bag,centre in enumerate(geo['bag_centres']):
            distance,witness,_=point_segment(centre,obj['a'],obj['b'])
            gap=distance-geo['bag_radius_m']-obj['radius_m']
            axis_upper=distance+error-geo['bag_radius_m']
            # Plate spheres/assembly capsules are enclosing bounds, not solid
            # shape penetration proofs. A declared segment/curve-axis witness
            # is stronger but remains in the unloaded, selected construction.
            actual_axis=obj['role'] in ('tube','sector','rope','tail','axle','actuator')
            bag_rows.append(dict(object=obj['id'],role=obj['role'],origin=obj.get('origin'),bag=bag,
                                 enclosure_gap_m=gap,represented_axis_gap_upper_m=axis_upper,
                                 represented_axis_intrusion=actual_axis and axis_upper<0.,
                                 witness=witness,curve_error_m=error,
                                 qualification='Negative enclosing gap is unqualified fit; only a negative declared-axis upper bound is an axis intrusion witness.'))
        endpoints=[obj['a'],obj['b']]
        max_axis=max(norm(p) for p in endpoints)
        vertices=obj.get('vertices',[])
        hull_rows.append(dict(object=obj['id'],role=obj['role'],
                              conservative_inside_gap_m=geo['radius_m']-max_axis-obj['radius_m'],
                              axis_outside_hull=max_axis>geo['radius_m'],
                              full_blank_vertex_outside=any(norm(p)>geo['radius_m'] for p in vertices),
                              maximum_vertex_radius_m=max((norm(p) for p in vertices),default=None)))
    fixed_witnesses={}; fixed_tests=0
    for obj in c.objects:
        if obj.get('origin')!='I034': continue
        for fixed in B['fixed_objects']:
            distance,p,q=segment_segment(obj['a'],obj['b'],fixed['a'],fixed['b'])
            gap=distance-obj['radius_m']-fixed['radius_m']; fixed_tests+=1
            key=obj['role']+' / '+fixed['category']
            if key not in fixed_witnesses or gap<fixed_witnesses[key]['gap_m']:
                fixed_witnesses[key]=dict(object=obj['id'],fixed=fixed['id'],gap_m=gap,witnesses=[p,q],
                                           qualification='Conservative enclosing shapes; positive does not establish loaded fit.')
    rope={h:[o for o in c.objects if o['role']=='rope' and o.get('host')==h] for h in D['hosts']}
    rope_pairs=[]
    for a,b in itertools.combinations(D['hosts'],2):
        best=None; tests=0
        for first in rope[a]:
            for second in rope[b]:
                distance,p,q=segment_segment(first['a'],first['b'],second['a'],second['b'])
                gap=distance-first['radius_m']-second['radius_m'];tests+=1
                if best is None or gap<best['gap_m']:
                    best=dict(hosts=[a,b],objects=[first['id'],second['id']],gap_m=gap,witnesses=[p,q])
        best['segment_pairs_checked']=tests;rope_pairs.append(best)
    # Sweep the exact capsule AABBs. Disjoint AABBs are safely excluded from
    # overlap tests; every intersecting pair remains visible, including intended
    # mating parts and same-route neighbours. No blanket contact exemption.
    bounded=[]
    for obj in c.objects:
        r=obj['radius_m']; lo=[min(obj['a'][k],obj['b'][k])-r for k in range(3)]
        hi=[max(obj['a'][k],obj['b'][k])+r for k in range(3)]
        bounded.append((lo,hi,obj))
    bounded.sort(key=lambda t:t[0][0]); active=[]; tested=0; overlaps=0
    classes={}; examples=[]
    for lo,hi,obj in bounded:
        active=[entry for entry in active if entry[1][0]>=lo[0]]
        for otherlo,otherhi,other in active:
            if any(otherhi[k]<lo[k] or hi[k]<otherlo[k] for k in (1,2)):continue
            tested+=1
            distance,p,q=segment_segment(obj['a'],obj['b'],other['a'],other['b'])
            gap=distance-obj['radius_m']-other['radius_m']
            if gap>=0.:continue
            overlaps+=1
            local=obj.get('cluster')==other.get('cluster')
            classification='nominal local interface overlap; unresolved fit' if local else 'distinct construction envelopes overlap'
            key=' / '.join(sorted([obj['role'],other['role']]))+' / '+classification
            row=dict(objects=[obj['id'],other['id']],roles=[obj['role'],other['role']],gap_m=gap,
                     witnesses=[p,q],classification=classification)
            if key not in classes:classes[key]={'count':0,'worst':row}
            classes[key]['count']+=1
            if gap<classes[key]['worst']['gap_m']:classes[key]['worst']=row
            if len(examples)<80:examples.append(row)
        active.append((lo,hi,obj))
    new_bag=[r for r in bag_rows if r['origin']=='I034']
    return dict(object_count=len(c.objects),bag_count=4,bag_witnesses=bag_rows,hull_witnesses=hull_rows,
                minimum_new_bag_witness=min(new_bag,key=lambda r:r['enclosure_gap_m']),
                new_axis_intrusion_count=sum(r['represented_axis_intrusion'] for r in new_bag),
                fixed_object_count=len(B['fixed_objects']),fixed_pairs_checked=fixed_tests,
                fixed_class_minima=fixed_witnesses,rope_pairs=rope_pairs,
                rope_pair_count=len(rope_pairs),minimum_rope_pair=min(rope_pairs,key=lambda r:r['gap_m']),
                structure_and_assembly=dict(method='Capsule AABB sweep then exact segment distance; no local-interface exemptions.',
                    narrow_pairs_checked=tested,envelope_overlap_count=overlaps,classes=classes,
                    first_examples=examples,example_limit=80,all_overlap_counts_preserved=True,
                    omitted_positive_separations='AABB-disjoint pairs cannot overlap their enclosing capsules; positive distance minima are not claimed.'),
                loaded_clearance='UNKNOWN; nominal straight/arc witnesses are not a loaded shape. Full bags and all inherited duties unchanged.',
                physical_fit='FAIL/UNKNOWN')


def main():
    global B,D,ROPE_AREA,ROPE_MASS_PER_M,ROPE_VOLUME_PER_M,EA
    here=Path(__file__).resolve().parent
    source=json.loads((here/'sources.json').read_text())
    raw=(here/'baseline.json').read_bytes(); pin=source['inputs'][0]
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
    B=json.loads(raw);D=source['design']
    assert [r['host'] for r in B['saved_route_datums']]==D['hosts']
    assert len(B['states'])==4 and len(B['saved_receivers'])==8
    ROPE_AREA=math.pi*D['rope_diameter_m']**2/4
    ROPE_MASS_PER_M=ROPE_AREA*D['rope_density_kg_m3']+D['coating_kg_m']
    ROPE_VOLUME_PER_M=ROPE_AREA+D['coating_kg_m']/D['coating_density_kg_m3']
    EA=ROPE_AREA*D['rope_E_pa']
    c=Construction();c.build();mass=mass_ledger(c)
    geometry_result=geometry(c)
    states=[load_case(c,k,mass) for k in range(4)]
    for state in states:
        rows={r['host']:r for r in state['rows']}
        state['conditional_sag_rope_pairs']=[]
        for pair in geometry_result['rope_pairs']:
            hosts=pair['hosts']
            if any('sag' not in rows[h] for h in hosts):
                state['conditional_sag_rope_pairs'].append(dict(hosts=hosts,status='FAIL: upward departure unavailable'))
                continue
            allowances=[max(s['sag_m'] for s in rows[h]['sag']) for h in hosts]
            state['conditional_sag_rope_pairs'].append(dict(hosts=hosts,
                enclosure_gap_lower_m=pair['gap_m']-sum(allowances),max_sag_each_m=allowances,
                qualification='Fixed-end parabolic sag envelope only; axial extension, failed commands and structural motion leave actual loaded clearance UNKNOWN.'))
        state['summary']={
            'route_rows':len(state['rows']),
            'rope_strength_failures':sum(not r.get('rope_strength_pass',False) for r in state['rows']),
            'actuator_strength_failures':sum(not r.get('actuator_strength_pass',False) for r in state['rows']),
            'stroke_failures':sum(not r.get('stroke_pass',False) for r in state['rows']),
            'sag_domain_failures':sum(not r.get('local_domain',False) for r in state['rows']),
            'support_load_sharing':'UNKNOWN','physical_float':'NOT SHOWN'}
    # In-run bookkeeping invariants are part of this sole calculator execution.
    assert abs(mass['ledger_identity_residual_kg'])<1e-6
    assert all(len(s['rows'])==8 and len(s['supports'])==16 and len(s['receivers'])==8 for s in states)
    summary=dict(route_count=8,state_count=4,route_state_rows=32,sectors=8,legs_and_braces=16,
                 node_boxes=16,guide_arms=16,parts=len(c.parts),new_parts=len(c.new),
                 interfaces=len(c.interfaces),weld_seams=len(c.seams),
                 any_finite_tangency_failure=any(not r['finite_tangencies_fit'] for r in c.routes),
                 conditional_rope_failures=sum(s['summary']['rope_strength_failures'] for s in states),
                 conditional_actuator_failures=sum(s['summary']['actuator_strength_failures'] for s in states),
                 conditional_stroke_failures=sum(s['summary']['stroke_failures'] for s in states),
                 conditional_sag_domain_failures=sum(s['summary']['sag_domain_failures'] for s in states),
                 original_I030_findings='Two MEDIUM findings remain OPEN; accepted README correction UNREVIEWED.',
                 new_section_bolt_weld_capacity='UNKNOWN',qualified_retirement_count=0,
                 overall='FAIL/UNKNOWN',physical_float='NOT SHOWN')
    result=dict(calculator_sha256=digest(Path(__file__)),baseline_sha256=hashlib.sha256(raw).hexdigest(),
                sources_sha256=digest(here/'sources.json'),base=source['base'],base_tree=source['base_tree'],
                frozen_design=D,routes=c.routes,sectors=c.sectors,supports=c.supports,node_boxes=c.boxes,
                guides=c.guides,splices=c.splices,interfaces=c.interfaces,weld_seams=c.seams,
                parts=c.parts,new_parts=c.new,removed_parts=c.removed,relocations=c.relocations,
                objects=c.objects,geometry=geometry_result,states=states,mass=mass,
                inventory=B['predecessor']['inventory'],fixed_water_kg=B['predecessor']['fixed_water_kg'],
                inherited_qualifications=B['predecessor']['inherited_limits'],summary=summary,
                unpriced_stock=['U: complete support/rack/root/pad/curtain/hull strengthening after compatible load sharing.',
                    'C: resolved oblique box/endplate adapters, saddle face/grip stack, guide fork interfaces, hole/notch packing, weld access, erection and loaded slack/clearance.'],
                result='FAIL/UNKNOWN; no physical float shown',
                weakest_assumption='Whether the paid sixteen-support crown can deliver its couples into the existing racks without unsupported fixity or dominant extra U+C.',
                next_change='UNISSUED hypothesis only: one wider paid receiver saddle joining each crown support into both existing same-rack upper/lower receiver levels, with full stock and compatible load sharing.')
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
