"""Fresh rigid-joint beam / pressure-fan validation and one-member-loss screens.

All physical results QUESTIONABLE / PROJECTION. Linear static redistribution
and tangent eigenvalues are not a time-domain progressive collapse analysis.
"""
from pathlib import Path
import argparse
import gc
import json
import math
import time
import numpy as np
from scipy.optimize import brentq
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import LinearOperator, eigsh
import linear_core as core
from material_models import models
from frame_compare import BASE, load_data, score, section, comp_root

ROOT=Path(__file__).resolve().parent

def dump(p,x):
    p.write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")

class MixedFan:
    """Group variable-length faces; exact same cubic volume as core.Fan."""
    def __init__(self,data):
        self.groups=[]
        for n in sorted(set(map(len,data["boundaries"]))):
            small={"points":data["points"],"boundaries":np.array(
                [b for b in data["boundaries"] if len(b)==n])}
            self.groups.append(core.Fan(small))
        self.gradient=sum(f.gradient for f in self.groups)
        self.volume=sum(f.volume for f in self.groups)
    def hessian(self,v):
        return sum(f.hessian(v) for f in self.groups)

def polygon_radius(points):
    center=points.mean(axis=0)
    area=.5*np.linalg.norm(np.cross(points-center,np.roll(points,-1,axis=0)-center).sum(axis=0))
    per=np.linalg.norm(np.roll(points,-1,axis=0)-points,axis=1).sum()
    return float(2*area/per)

def remove_member(original,member):
    data=dict(original)
    edge=original["edges"][member]
    incident=[j for j,c in enumerate(original["cells"]) if set(edge).issubset(set(c))]
    assert len(incident)==2
    halfedges=set()
    for j in incident:
        b=original["boundaries"][j]
        for a,c in zip(b,np.roll(b,-1)):
            a,c=int(a),int(c)
            if (c,a) in halfedges:halfedges.remove((c,a))
            else:halfedges.add((a,c))
    nextnode=dict(halfedges)
    assert len(nextnode)==len(halfedges)
    merged=[min(nextnode)]
    while nextnode[merged[-1]]!=merged[0]:
        merged.append(nextnode[merged[-1]])
        assert len(merged)<=len(halfedges)
    assert len(merged)==4*original["segments"]
    boundaries=[list(b) for j,b in enumerate(original["boundaries"]) if j not in incident]+[merged]
    keep=np.delete(np.arange(750),member)
    chains=original["chains"][keep]
    used=np.unique(chains)
    mapping=np.full(len(original["points"]),-1,int);mapping[used]=np.arange(len(used))
    data.update(points=original["points"][used],chains=mapping[chains],
                edges=original["edges"][keep],arcs=original["arcs"][keep],
                boundaries=[mapping[b] for b in boundaries],member_ids=keep)
    data["elements"]=np.column_stack((data["chains"][:,:-1].ravel(),data["chains"][:,1:].ravel()))
    r_old=[polygon_radius(original["main"][original["cells"][j]]) for j in incident]
    corners=[j for j in merged if j<len(original["main"])]
    r_new=polygon_radius(original["main"][corners])
    data["film_tension_multiplier"]=r_new/max(r_old)
    data["merged_bay"]=dict(incident_faces=incident,corner_nodes=corners,
        old_effective_inradii_m=r_old,new_effective_inradius_m=r_new,
        tension_multiplier_same_rise_to_span=r_new/max(r_old),
        assumption="045 equal rise/span, area/perimeter radius; not a membrane shape solution")
    assert all(np.min(b)>=0 for b in data["boundaries"])
    return data

def baseline_joints(ref,old):
    ro=ref["section"]["r_o_m"];target=ref["least_screened_SF"]
    N=old["joint_N"];M=old["joint_M"];T=old["joint_T"]
    areas=np.empty_like(N)
    for ix in np.ndindex(N.shape):
        n,m=N[ix],M[ix]
        def f(a):
            outer=math.sqrt(ro*ro+a/math.pi);inertia=a*(outer*outer+ro*ro)/4
            return target*(n/a+m*outer/inertia)-1470e6
        lo=target*n/1470e6;hi=target*(n+2*m/ro)/1470e6
        areas[ix]=brentq(f,lo*(1-1e-12),hi*(1+1e-12),xtol=1e-16)
    overlaps=target*np.hypot(N+2*M/ro,T/ro)/(2*math.pi*ro*28.9e6)
    assert abs(np.sum(1550*areas*overlaps)-ref["mass_kg"]["joint"])<1e-5
    return areas,overlaps

def solve(mat,reserve,segments,policy,removed=None):
    ref=BASE[reserve];old,length,geo=load_data(reserve)
    ro=ref["section"]["r_o_m"]
    area_budget=ref["mass_kg"]["tube"]/(mat["density_kgm3"]*length.sum())
    wall=ro-math.sqrt(ro*ro-area_budget/math.pi)
    if policy=="same_section":wall=ref["section"]["wall_m"]
    label=f'{mat["id"]}-{reserve}-{policy}-m{segments}-'+("intact" if removed is None else f"lost{removed}")
    folder=ROOT/"runs"/label
    if (folder/"RESULTS.json").exists():
        return json.loads((folder/"RESULTS.json").read_text())
    folder.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    core.E=mat["Eax_Pa"]
    # core's NU occurs only in torsion GJ=EI/(1+NU). This is an algebraic
    # adapter for independent axial E and G, not an isotropic Poisson ratio.
    core.NU=mat["Eax_Pa"]/(2*mat["Gaxhoop_Pa"])-1
    core.CASES[5]=dict(ro=ro,wall=wall,s=1)
    data=core.mesh(5,segments,1.)
    data["member_ids"]=np.arange(750);data["film_tension_multiplier"]=1.
    if removed is not None:data=remove_member(data,removed)
    ops=core.beam_operators(data);fan=MixedFan(data)
    inverse=core.ConstrainedInverse(ops["K"],data["points"])
    load=-core.P*fan.gradient;u=inverse.solve(load)
    residual=float(np.linalg.norm(ops["K"]@u-inverse.project(load))/np.linalg.norm(load))
    balance=float(np.linalg.norm(inverse.Q.T@load)/np.linalg.norm(load))
    assert residual<2e-6,(label,residual)
    assert balance<1e-12,(label,balance)
    ends=np.einsum("eij,ej->ei",ops["local"],
            np.einsum("eij,ej->ei",ops["transforms"],u[ops["dofs"]]))
    N=(ends[:,0]-ends[:,6])/2
    M=np.maximum(np.linalg.norm(ends[:,[4,5]],axis=1),np.linalg.norm(ends[:,[10,11]],axis=1))
    nmember=len(data["chains"]);shape=ends.reshape(nmember,segments,12)
    jN=np.stack((N.reshape(nmember,segments)[:,0],N.reshape(nmember,segments)[:,-1]),axis=1)
    jM=np.stack((np.linalg.norm(shape[:,0,4:6],axis=1),np.linalg.norm(shape[:,-1,10:12],axis=1)),axis=1)
    jT=np.abs(np.stack((shape[:,0,3],shape[:,-1,9]),axis=1))
    ids=np.repeat(data["member_ids"],segments)
    d=dict(subelement_N=N,subelement_M=M,subelement_member=ids,
           joint_N=jN,joint_M=jM,joint_T=jT)
    vals=ops["geometric_unit"]*N[:,None,None]
    G=coo_matrix((vals.ravel(),(ops["rows"],ops["cols"])),shape=ops["K"].shape).tocsr()
    def destabilize(v):
        v=inverse.project(np.asarray(v).reshape(-1))
        return inverse.project([address]*fan.hessian(v))
    ndof=len(load)
    D=LinearOperator((ndof,ndof),matvec=destabilize,dtype=float)
    metric=LinearOperator((ndof,ndof),matvec=inverse.metric,dtype=float)
    inv=LinearOperator((ndof,ndof),matvec=inverse.solve,dtype=float)
    seed=inverse.project(np.random.default_rng(51020).standard_normal(ndof))
    mu,v=eigsh(D,k=4,M=metric,Minv=inv,which="LA",v0=seed,tol=2e-8,ncv=24,maxiter=4000)
    order=np.argsort(mu)[::-1];lambdas=1/mu[order]
    eigen_res=[]
    for j in order:
        vv=inverse.project(v[:,j]);kv=ops["K"]@vv;dv=destabilize(vv);lam=1/mu[j]
        eigen_res.append(float(np.linalg.norm(kv-lam*dv)/(np.linalg.norm(kv)+abs(lam)*np.linalg.norm(dv))))
    assert max(eigen_res)<2e-6,(label,eigen_res)
    A,I=section(ro,wall)
    # Intact uses the identical scalar model as the fixed-demand comparison.
    # Removed-member loads may include tension; general handling below.
    Nc=np.maximum(N,0)
    euler=np.where(Nc>0,math.pi**2*mat["Eax_Pa"]*I/(length[ids]**2*np.maximum(Nc,1e-30)),1e99)
    aa=N/A;bb=(M+np.abs(N)*length[ids]/1000)*ro/I
    gamma=.099+.901*math.exp(-math.sqrt(ro/wall)/16)
    local=gamma*mat["local_classical_coefficient_Pa"]*wall/ro
    local_sf=float(np.min(comp_root(np.maximum(aa,0),bb,euler,local)))
    comp=mat["screen_compression_Pa"]
    comp_sf=None if comp is None else float(np.min(comp_root(np.maximum(aa,0),bb,euler,comp)))
    areas,overlaps=baseline_joints(ref,old)
    areas=areas[data["member_ids"]];overlaps=overlaps[data["member_ids"]]
    outer=np.sqrt(ro*ro+areas/math.pi);ji=areas*(outer*outer+ro*ro)/4
    jsleeve=float(np.min(1470e6/(np.abs(jN)/areas+jM*outer/ji)))
    bond=np.hypot(np.abs(jN)+2*jM/ro,jT/ro)
    jbond=float(np.min(28.9e6*2*math.pi*ro*overlaps/bond))
    film=ref["modes"]["film"]/data["film_tension_multiplier"]
    modes=dict(euler=float(euler.min()),global_k0p2=float(.2*lambdas[0]),
               local_peak=local_sf,compression=comp_sf,
               joint_sleeve=jsleeve,joint_bond=jbond,film=film)
    upper=min(v for v in modes.values() if v is not None)
    q1_stable=euler.min()>1
    peak=None;tension=None;required=None;first_failures={}
    if q1_stable:
        compression=np.maximum(aa+bb/(1-1/euler),0)
        tensile=np.maximum(-aa+bb/(1-1/euler),0)
        peak=float(compression.max());tension=float(tensile.max())
        member=np.full(750,0.);np.maximum.at(member,ids,compression)
        from scipy.special import logsumexp
        required=float(np.exp((logsumexp(10*np.log(np.maximum(member,1e-20)/1e9))-math.log(-math.log1p(-.001)))/10)*1e9)
        for name,allow in [("local_shell",local),("compression",comp)]:
            first_failures[name]=None if allow is None else np.flatnonzero(member>allow).tolist()
    tube=mat["density_kgm3"]*A*length.sum() # launch mass retained after damage
    result=dict(tag="QUESTIONABLE / PROJECTION",label=label,material=mat["id"],reserve=reserve,
        section_policy=policy,removed_member=removed,segments=segments,ndof=ndof,
        radius_m=ro,wall_m=wall,frame_tubes_kg=float(tube),
        total_mass_including_reserve_sag_kg=float(tube+ref["mass_kg"]["total_with_reserve_and_sag"]-ref["mass_kg"]["tube"]),
        modes=modes,conditional_SF_or_ceiling=upper,
        qualified_structural_SF=None,qualified_frame_Pf=None,qualified_hail_break_probability=None,
        all_composite_modes_complete=False if mat["kind"]=="composite" else None,
        linear_multipliers=lambdas.tolist(),eigen_relative_residuals=eigen_res,
        equilibrium_relative_residual=residual,load_rigid_projection_ratio=balance,
        q1_peak_compression_Pa=peak,q1_peak_tension_Pa=tension,
        q1_whole_member_scale_needed_m10_Pf1e3_Pa=required,
        max_axial_N=float(N.max()),max_bending_Nm=float(M.max()),
        local_shell_limit_Pa=local,
        secondary_failure_trigger_at_q1=any(v<1 for v in modes.values() if v is not None),
        individual_secondary_failure_members_at_q1=first_failures,
        merged_bay=data.get("merged_bay"),pressure_fan_volume_m3=fan.volume,
        tube_loss_includes_pressure_bay_merge=removed is not None,
        dynamic_cascade_probability=None,elapsed_seconds=time.monotonic()-started)
    np.savez_compressed(folder/"STATIC.npz",**d,member_ids=data["member_ids"],
                        member_arcs_m=length,points=data["points"],u=u,
                        ends=ends,chains=data["chains"],edges=data["edges"])
    dump(folder/"RESULTS.json",result)
    print(json.dumps({k:result[k] for k in ["label","conditional_SF_or_ceiling","equilibrium_relative_residual","elapsed_seconds"]}),flush=True)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--material",default="all")
    p.add_argument("--segments",type=int,default=6)
    p.add_argument("--intact-only",action="store_true")
    p.add_argument("--reserve",default="all")
    p.add_argument("--policy",default="same_tube_mass")
    a=p.parse_args()
    mats=[m for m in models() if a.material=="all" or m["id"]==a.material]
    result=[]
    for mat in mats:
        for reserve in (["5","019"] if a.reserve=="all" else [a.reserve]):
            old,_,_=load_data(reserve)
            avg=old["joint_N"].mean(axis=1)
            picks=[None] if a.intact_only else [None,int(np.argsort(avg)[len(avg)//2]),int(np.argmax(avg))]
            for removed in picks:
                result.append(solve(mat,reserve,a.segments,a.policy,removed))
                gc.collect()
    dump(ROOT/f"FE-{a.material}-{a.reserve}-{a.policy}-m{a.segments}.json",dict(rows=result))

if __name__=="__main__":main()
