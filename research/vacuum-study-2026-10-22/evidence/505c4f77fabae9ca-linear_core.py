"""Independent CHECK-026b frame calculation, from the pinned written equations.

This core was developed before CHECK-041 from the earlier written equations.
CHECK-041's prior exposure to owner postprocessors is disclosed separately in
PRIOR-EXPOSURE.json; this is not a claim of a blind CHECK-041 review.
No owner program is imported or executed by this core. The elastic and
compression matrices are integrated from Hermite shape derivatives. Pressure
derivatives are evaluated from the closed fan's cubic signed-volume polynomial.
Run through tools/simjob.py. All physical inputs are QUESTIONABLE; ideal joints,
fabrication and the pressure-transfer surface are PROJECTION assumptions.
"""
from pathlib import Path
import argparse
import json
import math
import time
import numpy as np
from scipy.spatial import ConvexHull
from scipy.linalg import qr
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu, LinearOperator, eigsh

ROOT = Path(__file__).resolve().parent
P = 95460.8379139
R = 10.0
E = 410e9
NU = .14
RHO = 3100.
LIFT = 4889.44215019
CASES = {
    6: dict(s=2.04, ro=.12368836237368608, wall=.0008802990936851718,
            film=97.515, systems=50., sag=0., payload=0., joint_rule="tubes"),
    4: dict(s=3., ro=.13670908289556455, wall=.0010718489471981119,
            film=184.4416986525136, systems=100., sag=0., payload=244.47210750950035,
            joint_rule="tubes+film+nodes"),
    2: dict(s=6.15, ro=.16764593114772616, wall=.0016252746475689805,
            film=348.8563570154232, systems=100., sag=187.9379326479281,
            payload=244.4721075095, joint_rule="tubes+film+nodes"),
}


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def subdivide(frequency):
    phi = (1+math.sqrt(5))/2
    vertices = []
    for a in [-1, 1]:
        for b in [-phi, phi]:
            vertices += [[0,a,b], [a,b,0], [b,0,a]]
    vertices = np.array(vertices, float)
    faces = ConvexHull(vertices).simplices.copy()
    xyz, ids, cells = [], {}, []
    for face in faces:
        a,b,c = vertices[face]
        if np.dot(np.cross(b-a,c-a), a+b+c) < 0:
            b,c = c,b
        lookup = {}
        for i in range(frequency+1):
            for j in range(frequency+1-i):
                x = (frequency-i-j)*a+i*b+j*c
                x = R*x/np.linalg.norm(x)
                key = tuple(np.round(x, 11))
                if key not in ids:
                    ids[key] = len(xyz)
                    xyz.append(x)
                lookup[i,j] = ids[key]
        for i in range(frequency):
            for j in range(frequency-i):
                cells.append([lookup[i,j],lookup[i+1,j],lookup[i,j+1]])
                if i+j < frequency-1:
                    cells.append([lookup[i+1,j],lookup[i+1,j+1],lookup[i,j+1]])
    xyz, cells = np.array(xyz), np.array(cells, int)
    edges = sorted({tuple(sorted((a,b))) for cell in cells
                    for a,b in zip(cell,np.roll(cell,-1))})
    edges = np.array(edges,int)
    assert len(xyz)==10*frequency**2+2
    assert len(edges)==30*frequency**2 and len(cells)==20*frequency**2
    assert np.all(np.einsum("ij,ij->i", np.cross(xyz[cells[:,1]]-xyz[cells[:,0]],
                                                xyz[cells[:,2]]-xyz[cells[:,0]]),
                           xyz[cells].sum(axis=1)) > 0)
    return xyz, cells, edges


def mesh(frequency, segments, rise):
    main, cells, edges = subdivide(frequency)
    points = list(main.copy())
    chains, arcs, great_arcs, sagittas = [], [], [], []
    for a,b in edges:
        x,y = main[[a,b]]
        chord = np.linalg.norm(y-x)
        radial = (x+y)/np.linalg.norm(x+y)
        tangent = (y-x)/chord
        theta0 = math.acos(np.clip(np.dot(x,y)/R**2,-1,1))
        h0 = R*(1-math.cos(theta0/2))
        h = rise*h0
        radius = chord**2/(8*h)+h/2
        half_angle = 2*math.atan2(2*h,chord)
        center = (x+y)/2+(h-radius)*radial
        angles = np.linspace(-half_angle, half_angle, segments+1)
        internal = [center+radius*(math.cos(t)*radial+math.sin(t)*tangent)
                    for t in angles[1:-1]]
        chain = [int(a),*range(len(points),len(points)+segments-1),int(b)]
        points.extend(internal)
        chains.append(chain)
        arcs.append(2*radius*half_angle)
        great_arcs.append(R*theta0)
        sagittas.append(h)
    points, chains = np.array(points), np.array(chains,int)
    chain_map = {tuple(edge): chain for edge,chain in zip(edges,chains)}
    boundaries = []
    for cell in cells:
        row = []
        for a,b in zip(cell,np.roll(cell,-1)):
            chain = chain_map[tuple(sorted((a,b)))]
            if a>b:
                chain = chain[::-1]
            row.extend(chain[:-1])
        boundaries.append(row)
    elements = np.column_stack((chains[:,:-1].ravel(),chains[:,1:].ravel()))
    return dict(points=points, main=main, cells=cells, edges=edges, chains=chains,
                boundaries=np.array(boundaries,int), elements=elements,
                arcs=np.array(arcs), great_arcs=np.array(great_arcs),
                sagittas=np.array(sagittas), frequency=frequency, segments=segments,
                rise=rise)


def skew(x):
    a,b,c=x
    return np.array([[0,-c,b],[c,0,-a],[-b,a,0]])


def hermite(x, length):
    slope = np.array([(-6*x+6*x*x)/length, 1-4*x+3*x*x,
                      (6*x-6*x*x)/length, -2*x+3*x*x])
    curvature = np.array([(-6+12*x)/length**2,(-4+6*x)/length,
                          (6-12*x)/length**2,(-2+6*x)/length])
    return slope, curvature


def local_matrices(length, area, inertia):
    k = np.zeros((12,12))
    g = np.zeros((12,12))
    for idx, coefficient in [([0,6],E*area/length),([3,9],E*inertia/(1+NU)/length)]:
        k[np.ix_(idx,idx)] += coefficient*np.array([[1,-1],[-1,1]])
    z,w = np.polynomial.legendre.leggauss(3)
    for t,weight in zip((z+1)/2,w/2):
        d,dd = hermite(t,length)
        for idx,sign in [([1,5,7,11],np.ones(4)),
                         ([2,4,8,10],np.array([1,-1,1,-1]))]:
            k[np.ix_(idx,idx)] += E*inertia*length*weight*np.outer(dd*sign,dd*sign)
            g[np.ix_(idx,idx)] += length*weight*np.outer(d*sign,d*sign)
    return k,g


def beam_operators(data):
    case=CASES[data["frequency"]]
    ro,ri=case["ro"],case["ro"]-case["wall"]
    area=math.pi*(ro**2-ri**2)
    inertia=math.pi*(ro**4-ri**4)/4
    x=data["points"]
    el=data["elements"]
    delta=x[el[:,1]]-x[el[:,0]]
    lengths=np.linalg.norm(delta,axis=1)
    ex=delta/lengths[:,None]
    axes=np.eye(3)[np.argmin(np.abs(ex),axis=1)]
    ez=np.cross(ex,axes)
    ez/=np.linalg.norm(ez,axis=1)[:,None]
    ey=np.cross(ez,ex)
    rotation=np.stack((ex,ey,ez),axis=1)
    transforms=np.zeros((len(el),12,12))
    for offset in [0,3,6,9]:
        transforms[:,offset:offset+3,offset:offset+3]=rotation
    # Cache equal lengths only at numerical precision; section remains exact.
    cached={}
    kl,gl=[],[]
    for length in lengths:
        key=round(float(length),13)
        if key not in cached:
            cached[key]=local_matrices(float(length),area,inertia)
        k,g=cached[key]
        kl.append(k);gl.append(g)
    kl,gl=np.array(kl),np.array(gl)
    kg=np.einsum("eai,eab,ebj->eij",transforms,kl,transforms,optimize=True)
    gg=np.einsum("eai,eab,ebj->eij",transforms,gl,transforms,optimize=True)
    dofs=np.column_stack([6*el[:,0,None]+np.arange(6),
                          6*el[:,1,None]+np.arange(6)])
    rows=np.broadcast_to(dofs[:,:,None],kg.shape).ravel()
    cols=np.broadcast_to(dofs[:,None,:],kg.shape).ravel()
    n=6*len(x)
    K=coo_matrix((kg.ravel(),(rows,cols)),shape=(n,n)).tocsc()
    K.eliminate_zeros()
    return dict(K=K, geometric_unit=gg, local=kl, transforms=transforms,
                lengths=lengths,dofs=dofs,rows=rows,cols=cols,area=area,
                inertia=inertia,ro=ro,rotation=rotation)


class Fan:
    def __init__(self,data):
        self.boundaries=data["boundaries"]
        self.points=data["points"]
        self.b=self.points[self.boundaries]
        self.c=self.b.mean(axis=1)
        self.db=np.roll(self.b,-1,axis=1)-np.roll(self.b,1,axis=1)
        self.S=np.cross(self.b,np.roll(self.b,-1,axis=1)).sum(axis=1)
        self.volume=float(np.einsum("ij,ij->",self.c,self.S)/6)
        self.n=len(self.b[0])
        self.ndof=6*len(self.points)
        grad_face=(self.S[:,None,:]/self.n+
                   np.cross(self.db,self.c[:,None,:]))/6
        result=np.zeros((len(self.points),3))
        np.add.at(result,self.boundaries.ravel(),grad_face.reshape(-1,3))
        self.gradient=np.zeros((len(self.points),6))
        self.gradient[:,:3]=result
        self.gradient=self.gradient.ravel()

    def hessian(self,v):
        v=np.asarray(v).reshape(-1,6)[:,:3]
        q=v[self.boundaries]
        dc=q.mean(axis=1)
        dS=np.cross(q,self.db).sum(axis=1)
        dq=np.roll(q,-1,axis=1)-np.roll(q,1,axis=1)
        out=(dS[:,None,:]/self.n+np.cross(dq,self.c[:,None,:])+
             np.cross(self.db,dc[:,None,:]))/6
        ans=np.zeros((len(self.points),6))
        np.add.at(ans[:,:3],self.boundaries.ravel(),out.reshape(-1,3))
        return ans.ravel()


class ConstrainedInverse:
    """Six coordinate eliminations are only a factorization gauge.

    Both loads and solutions are orthogonally projected; no physical support
    conditions are introduced. A low-rank rigid-space extension is used only
    to give ARPACK a strictly positive generalized metric.
    """
    def __init__(self,K,points):
        self.K=K
        n=len(points)
        rigid=np.zeros((n,6,6))
        for j in range(3):
            rigid[:,j,j]=1
            rigid[:,:3,j+3]=np.cross(np.eye(3)[j],points)
            rigid[:,3+j,j+3]=1
        self.Q=np.linalg.qr(rigid.reshape(6*n,6))[0]
        _,_,piv=qr(self.Q.T,pivoting=True,mode="economic")
        self.removed=np.sort(piv[:6])
        self.free=np.setdiff1d(np.arange(6*n),self.removed)
        self.lu=splu(K[self.free][:,self.free],permc_spec="COLAMD")
        self.alpha=float(np.median(K.diagonal()))
        self.rigid_K_relative=float(np.linalg.norm([address])/np.linalg.norm(K.data))
        self.shape=K.shape

    def project(self,v):
        return v-self.Q@(self.Q.T@v)

    def solve(self,v):
        v=np.asarray(v).reshape(-1)
        p=self.project(v)
        ans=np.zeros_like(v)
        ans[self.free]=self.lu.solve(p[self.free])
        return self.project(ans)+(self.Q@(self.Q.T@v))/self.alpha

    def metric(self,v):
        v=np.asarray(v).reshape(-1)
        return self.K@v+self.alpha*self.Q@(self.Q.T@v)


def summary_stats(a):
    return dict(min=float(np.min(a)),mean=float(np.mean(a)),max=float(np.max(a)))


def static_stats(data,ops,u):
    dofs,trans=ops["dofs"],ops["transforms"]
    local_u=np.einsum("eij,ej->ei",trans,u[dofs])
    end=np.einsum("eij,ej->ei",ops["local"],local_u)
    compression=(end[:,0]-end[:,6])/2
    m=data["segments"]
    weighted=(compression*ops["lengths"]).reshape(-1,m).sum(axis=1)/ops["lengths"].reshape(-1,m).sum(axis=1)
    global_end=np.einsum("eji,ej->ei",trans,end)
    chord=data["main"][data["edges"][:,1]]-data["main"][data["edges"][:,0]]
    chord/=np.linalg.norm(chord,axis=1)[:,None]
    left=global_end.reshape(-1,m,12)[:,0,:3]
    right=global_end.reshape(-1,m,12)[:,-1,6:9]
    thrust_left=np.einsum("ij,ij->i",left,chord)
    thrust_right=-np.einsum("ij,ij->i",right,chord)
    thrust=(thrust_left+thrust_right)/2
    moments=np.column_stack((np.linalg.norm(end[:,[4,5]],axis=1),
                              np.linalg.norm(end[:,[10,11]],axis=1)))
    bending=moments*ops["ro"]/ops["inertia"]
    axial=compression/ops["area"]
    valence=np.bincount(data["edges"].ravel(),minlength=len(data["main"]))
    five=[]
    for node in np.where(valence==5)[0]:
        incident=np.where((data["edges"]==node).any(axis=1))[0]
        endpoint=np.where(data["edges"][incident,0]==node,thrust_left[incident],thrust_right[incident])
        # Also retain axial compression in the adjacent segment, separately.
        adjacent=np.where(data["edges"][incident,0]==node,
                          compression.reshape(-1,m)[incident,0],
                          compression.reshape(-1,m)[incident,-1])
        five.append(dict(position=data["main"][node].tolist(),node=int(node),
                         incident_members=incident.tolist(),
                         mean_member_compression_N=float(weighted[incident].mean()),
                         mean_endpoint_axial_compression_N=float(adjacent.mean()),
                         mean_endpoint_chord_thrust_N=float(endpoint.mean()),
                         incident_member_compression_N=weighted[incident].tolist()))
    out=dict(member_mean_compression_N=summary_stats(weighted),
             subelement_compression_N=summary_stats(compression),
             member_endpoint_chord_thrust_N=summary_stats(thrust),
             member_mean_compression_all_N=weighted.tolist(),
             member_endpoint_chord_thrust_all_N=thrust.tolist(),
             five_valent_nodes=five,
             valence_counts={str(v):int(np.sum(valence==v)) for v in np.unique(valence)},
             max_axial_compression_Pa=float(axial.max()),
             max_end_bending_stress_Pa=float(bending.max()),
             max_combined_compressive_fiber_stress_Pa=float((axial[:,None]+bending).max()),
             max_tensile_fiber_stress_Pa=float((bending-axial[:,None]).max()),
             max_end_bending_moment_Nm=float(moments.max()),
             max_displacement_m=float(np.linalg.norm(u.reshape(-1,6)[:,:3],axis=1).max()))
    s=CASES[data["frequency"]]["s"]
    for label,length in [("nominal",s),("actual_mean_arc",data["great_arcs"].mean())]:
        out["equilateral_pRs_over_2sqrt3_N_"+label]=P*R*length/(2*math.sqrt(3))
        out["two_way_pRs_over_2_N_"+label]=P*R*length/2
    out["mean_over_equilateral_at_actual_mean_arc"]=float(weighted.mean()/out["equilateral_pRs_over_2sqrt3_N_actual_mean_arc"])
    return out,compression


def metadata(data,ops):
    f,m=data["frequency"],data["segments"]
    c=CASES[f]
    tube=RHO*ops["area"]*sum(data["arcs"])
    nodes=.02*len(data["main"])
    joints=.05*(tube if f==6 else tube+nodes+c["film"])
    mass=tube+nodes+joints+c["film"]+c["systems"]
    continuum=4*math.sqrt(1.5)*E*math.sqrt(ops["area"]*ops["inertia"])/(c["s"]*R**2*P)
    halfwave=math.pi*math.sqrt(math.sqrt(1.125)*math.sqrt(ops["inertia"]/ops["area"])*R)
    return dict(frequency=f,segments_per_arc=m,rise_factor=data["rise"],
        main_nodes=len(data["main"]),members=len(data["edges"]),film_cells=len(data["cells"]),
        beam_nodes=len(data["points"]),beam_elements=len(data["elements"]),DOF=6*len(data["points"]),
        arc_length_m=summary_stats(data["great_arcs"]),arc_total_length_m=float(sum(data["arcs"])),
        straight_subelement_total_length_m=float(ops["lengths"].sum()),
        sagitta_m=summary_stats(data["sagittas"]),
        A_m2=ops["area"],I_m4=ops["inertia"],GJ_Nm2=E*ops["inertia"]/(1+NU),
        continuum_perfect_lambda_nominal_s=continuum,
        continuum_perfect_lambda_actual_mean_arc=continuum*c["s"]/float(data["great_arcs"].mean()),
        continuum_halfwave_m=halfwave,halfwave_over_nominal_s=halfwave/c["s"],
        halfwave_over_mean_arc=halfwave/float(data["great_arcs"].mean()),
        tube_mass_kg=tube,joints_5pct_kg=joints,node_mass_kg=nodes,
        film_mass_inherited_kg=c["film"],systems_inherited_kg=c["systems"],
        total_mass_with_inherited_allowances_kg=mass,
        gross_inherited_lift_kg=LIFT,payload_before_sag_kg=LIFT-mass,
        payload_after_source_sag_kg=LIFT-mass-c["sag"],
        headroom_after_source_sag_and_source_payload_kg=LIFT-mass-c["sag"]-c["payload"])


def validate():
    """Physical identities and an independent simply supported Euler benchmark."""
    result={}
    n=12
    area,inertia=.003,2e-5
    lengths=np.full(n,2./n)
    size=2*(n+1)
    K,G=np.zeros((size,size)),np.zeros((size,size))
    for i,length in enumerate(lengths):
        k,g=local_matrices(length,area,inertia)
        idx=[2*i,2*i+1,2*i+2,2*i+3]
        K[np.ix_(idx,idx)]+=k[np.ix_([1,5,7,11],[1,5,7,11])]
        G[np.ix_(idx,idx)]+=g[np.ix_([1,5,7,11],[1,5,7,11])]
    free=np.setdiff1d(np.arange(size),[0,2*n])
    from scipy.linalg import eigh
    calculated=eigh(K[np.ix_(free,free)],G[np.ix_(free,free)],eigvals_only=True)[0]
    exact=math.pi**2*E*inertia/4
    result["Euler_simply_supported"]=dict(calculated_N=float(calculated),exact_N=exact,
                                          relative_error=float(calculated/exact-1))
    assert abs(calculated/exact-1)<1e-5
    data=mesh(2,3,1.)
    fan=Fan(data)
    rng=np.random.default_rng(26020)
    a=rng.standard_normal(fan.ndof)
    b=rng.standard_normal(fan.ndof)
    a/=np.linalg.norm(a);b/=np.linalg.norm(b)
    eps=1e-4
    plus=dict(data,points=data["points"]+eps*a.reshape(-1,6)[:,:3])
    minus=dict(data,points=data["points"]-eps*a.reshape(-1,6)[:,:3])
    fd=(Fan(plus).gradient-Fan(minus).gradient)/(2*eps)
    ha=fan.hessian(a)
    gradient_fd=(Fan(plus).volume-Fan(minus).volume)/(2*eps)
    result["pressure_derivatives"]=dict(
        gradient_relative_error=float(abs(gradient_fd-fan.gradient@a)/max(abs(gradient_fd),1)),
        hessian_relative_error=float(np.linalg.norm(fd-ha)/np.linalg.norm(ha)),
        symmetry_error=float(abs(b@[address](b))))
    assert result["pressure_derivatives"]["hessian_relative_error"]<1e-7
    assert result["pressure_derivatives"]["gradient_relative_error"]<1e-6
    assert result["pressure_derivatives"]["symmetry_error"]<1e-10
    force=-P*fan.gradient.reshape(-1,6)[:,:3]
    result["pressure_balance"]=dict(net_force_N=np.linalg.norm(force.sum(axis=0)),
        net_moment_Nm=np.linalg.norm(np.cross(data["points"],force).sum(axis=0)),
        homogeneous_volume_identity_relative=abs(np.sum(fan.gradient.reshape(-1,6)[:,:3]*data["points"])/(3*fan.volume)-1))
    assert result["pressure_balance"]["net_force_N"]<1e-6
    assert result["pressure_balance"]["net_moment_Nm"]<1e-5
    result["pin_counts"]=[]
    for f in [2,4,6]:
        xyz,_,edges=subdivide(f)
        rigidity=np.zeros((len(edges),3*len(xyz)))
        for i,(a,b) in enumerate(edges):
            direction=(xyz[b]-xyz[a])/np.linalg.norm(xyz[b]-xyz[a])
            rigidity[i,3*a:3*a+3]=-direction
            rigidity[i,3*b:3*b+3]=direction
        singular=np.linalg.svd(rigidity,compute_uv=False)
        rank=int(np.sum(singular>singular[0]*1e-10))
        assert rank==3*len(xyz)-6
        result["pin_counts"].append(dict(frequency=f,rank=rank,
            singular_min=float(singular[-1]),singular_max=float(singular[0]),
            endpoint_nullity=3*len(xyz)-rank,
            independent_member_rolls=len(edges),internal_mechanisms=len(edges)))
    # A single curved member rigidly rolled about its endpoint chord:
    # lengths and relative director/chord rotations stay unchanged.
    chain=mesh(2,12,1.)["points"][mesh(2,12,1.)["chains"][0]]
    axis=(chain[-1]-chain[0]);axis/=np.linalg.norm(axis)
    theta=.05
    rotation=np.eye(3)+math.sin(theta)*skew(axis)+(1-math.cos(theta))*skew(axis)@skew(axis)
    rolled=(chain-chain[0])@rotation.T+chain[0]
    before=np.diff(chain,axis=0);after=np.diff(rolled,axis=0)
    result["finite_pin_roll"]=dict(angle_rad=theta,
        endpoint_displacement_m=float(np.linalg.norm(rolled[[0,-1]]-chain[[0,-1]])),
        max_segment_length_change_m=float(np.max(abs(np.linalg.norm(after,axis=1)-np.linalg.norm(before,axis=1)))),
        max_director_chord_error=float(np.max(abs([address]))))
    assert result["finite_pin_roll"]["max_segment_length_change_m"]<1e-12
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--frequency",type=int,choices=[2,4,6],default=2)
    ap.add_argument("--segments",type=int,default=12)
    ap.add_argument("--rise",type=float,default=1.)
    ap.add_argument("--linear",action="store_true")
    ap.add_argument("--validate",action="store_true")
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    start=time.monotonic()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    if args.validate:
        checks=validate()
        save(out/"VALIDATION.json",checks)
        print("Independent formulation checks passed",flush=True)
    data=mesh(args.frequency,args.segments,args.rise)
    ops=beam_operators(data)
    fan=Fan(data)
    inverse=ConstrainedInverse(ops["K"],data["points"])
    force=-P*fan.gradient
    u=inverse.solve(force)
    static,compression=static_stats(data,ops,u)
    residual=np.linalg.norm(ops["K"]@u-inverse.project(force))/np.linalg.norm(force)
    ans=dict(tag="QUESTIONABLE",projection="ideal fabrication, joints and pressure fan",
             model=metadata(data,ops),volume_m3=fan.volume,static=static,
             equilibrium_relative_residual=float(residual),
             rigid_K_relative=inverse.rigid_K_relative,
             code_independent=True)
    assert residual<2e-7,residual
    np.savez_compressed(out/"STATIC.npz",u=u,points=data["points"],
                        chains=data["chains"],edges=data["edges"])
    print(json.dumps(dict(phase="static",frequency=args.frequency,segments=args.segments,
                           rise=args.rise,mean_compression_N=static["member_mean_compression_N"]["mean"],
                           bending_Pa=static["max_end_bending_stress_Pa"],residual=float(residual))),flush=True)
    if args.rise!=1:
        original=mesh(args.frequency,args.segments,1.)
        frozen_force=-P*Fan(original).gradient
        frozen_u=inverse.solve(frozen_force)
        frozen,_=static_stats(data,ops,frozen_u)
        ans["frozen_spherical_load_sensitivity"]=frozen
        ans["frozen_load_residual"]=float(np.linalg.norm(ops["K"]@frozen_u-inverse.project(frozen_force))/np.linalg.norm(frozen_force))
    if args.linear:
        values=ops["geometric_unit"]*compression[:,None,None]
        G=coo_matrix((values.ravel(),(ops["rows"],ops["cols"])),shape=ops["K"].shape).tocsr()
        def destabilize(v):
            q=inverse.project(np.asarray(v).reshape(-1))
            return inverse.project(G@q-P*fan.hessian(q))
        n=len(force)
        D=LinearOperator((n,n),matvec=destabilize,dtype=float)
        M=LinearOperator((n,n),matvec=inverse.metric,dtype=float)
        Minv=LinearOperator((n,n),matvec=inverse.solve,dtype=float)
        seed=inverse.project(np.random.default_rng(26020).standard_normal(n))
        mu,vectors=eigsh(D,k=12,M=M,Minv=Minv,which="LA",
                         v0=seed,tol=2e-9,ncv=48,maxiter=2000)
        positive=np.where(mu>0)[0][::-1]
        modes=[]
        for j in positive:
            v=inverse.project(vectors[:,j])
            lam=1/mu[j]
            kv=ops["K"]@v
            dv=destabilize(v)
            res=np.linalg.norm(inverse.project(kv-lam*dv))/(np.linalg.norm(kv)+abs(lam)*np.linalg.norm(dv))
            modes.append(dict(lambda_factor=float(lam),relative_residual=float(res),
                              rigid_projection_norm=float(np.linalg.norm(inverse.Q.T@v))))
        ans["linear_modes"]=modes
        ans["linear"]=modes[0]["lambda_factor"]
        ans["linear_difference_from_nominal_continuum_pct"]=100*(ans["linear"]/ans["model"]["continuum_perfect_lambda_nominal_s"]-1)
        np.savez_compressed(out/"MODES.npz",modes=vectors[:,positive],reciprocal_eigenvalues=mu[positive])
        print(json.dumps(dict(phase="linear",frequency=args.frequency,segments=args.segments,
                              first=ans["linear"],max_residual=max(m["relative_residual"] for m in modes))),flush=True)
    ans["elapsed_seconds"]=time.monotonic()-start
    save(out/"RESULTS.json",ans)


if __name__=="__main__":
    main()
