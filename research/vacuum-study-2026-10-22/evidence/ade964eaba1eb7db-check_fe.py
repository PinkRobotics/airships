"""Fresh beam re-solves from pinned topology using this seat's earlier own 041 solver."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
import beam as b
import frame_tools as ft
from score import end_design
from scipy.sparse import coo_matrix
import argparse, time, types

def pressure_groups(self,q=None,tangent=True):
    x=self.x if q is None else self.x+q[:3*self.nn].reshape(-1,3)
    grad=np.zeros(self.ndof);volume=0.;Hs=[]
    for nb in sorted(set(map(len,self.loops))):
        boundary=np.array([a for a in self.loops if len(a)==nb])
        pts=x[boundary];center=pts.mean(axis=1)
        nxt,prev=np.roll(pts,-1,axis=1),np.roll(pts,1,axis=1)
        cross=np.cross(pts,nxt).sum(axis=1)
        volume+=np.einsum("fi,fi->",center,cross)/6
        diff=nxt-prev
        local=cross[:,None,:]/(6*nb)+np.cross(diff,center[:,None,:])/6
        dofs=(3*boundary[...,None]+np.arange(3)).reshape(len(boundary),-1)
        grad+=np.bincount(dofs.ravel(),weights=local.ravel(),minlength=self.ndof)
        if tangent:
            sd,sc=b.skew(diff),b.skew(center)
            h=(sd[:,:,None]-sd[:,None,:])/(6*nb)
            for i in range(nb):
                h[:,i,(i+1)%nb]-=sc/6;h[:,i,(i-1)%nb]+=sc/6
            h=h.transpose(0,1,3,2,4).reshape(len(boundary),3*nb,3*nb)
            Hs.append(coo_matrix((h.ravel(),(np.repeat(dofs,3*nb,axis=1).ravel(),
                np.tile(dofs,(1,3*nb)).ravel())),shape=(self.ndof,self.ndof)).tocsc())
    return volume,grad,sum(Hs) if tangent else None

def remove_member(f,edge):
    a,c=f.edges[edge]
    incident=[j for j,face in enumerate(f.faces) if a in face and c in face]
    def merge(loops):
        links=set()
        for loop in loops:
            for u,v in zip(loop,np.roll(loop,-1)):
                if (v,u) in links:links.remove((v,u))
                else:links.add((u,v))
        nxt=dict(links);start=min(nxt);out=[start]
        while nxt[out[-1]]!=start:out.append(nxt[out[-1]])
        assert len(out)==len(nxt)
        return out
    boundary=merge([f.boundary[j] for j in incident])
    corners=merge([f.faces[j] for j in incident])
    def effective(ids):
        x=f.x[ids];center=x.mean(axis=0)
        ar=np.linalg.norm(np.cross(x,np.roll(x,-1,axis=0)).sum(axis=0))/2
        per=np.linalg.norm(np.roll(x,-1,axis=0)-x,axis=1).sum()
        return 2*ar/per
    radii=[effective(f.faces[j]) for j in incident];newr=effective(corners)
    info=dict(incident_faces=incident,corner_nodes=corners,old_effective_inradii_m=radii,
      new_effective_inradius_m=newr,tension_multiplier_same_rise_to_span=newr/max(radii))
    loops=[list(loop) for j,loop in enumerate(f.boundary) if j not in incident]+[boundary]
    keep=np.arange(750)!=edge
    chains=f.chains[keep]; nodes=np.unique(chains)
    remap=np.full(f.nn,-1,int);remap[nodes]=np.arange(len(nodes))
    f.x=f.x[nodes];f.nn=len(nodes);f.ndof=6*f.nn
    f.chains=remap[chains];f.edges=remap[f.edges[keep]]
    f.true_member_lengths=np.asarray(f.true_member_lengths)[keep]
    f.beams=np.concatenate([f.chains[:,k:k+2] for k in range(f.segments)])
    f.member_of_beam=np.tile(np.arange(749),f.segments)
    f.rotation_nodes=f.beams.copy()
    f.loops=[remap[v].tolist() for v in loops]
    f.pressure=types.MethodType(pressure_groups,f)
    f.dofs=np.concatenate([3*f.beams[:,0,None]+np.arange(3),
       3*f.nn+3*f.beams[:,0,None]+np.arange(3),
       3*f.beams[:,1,None]+np.arange(3),
       3*f.nn+3*f.beams[:,1,None]+np.arange(3)],axis=1)
    f.krows=np.repeat(f.dofs,12,axis=1).ravel();f.kcols=np.tile(f.dofs,(1,12)).ravel()
    f.xpair=f.x[f.beams];chord=f.xpair[:,1]-f.xpair[:,0]
    f.length=np.linalg.norm(chord,axis=1);ex=chord/f.length[:,None]
    helper=np.tile([0.,0.,1.],(len(ex),1));helper[abs(ex[:,2])>.8]=[0.,1.,0.]
    ey=np.cross(helper,ex);ey/=np.linalg.norm(ey,axis=1)[:,None]
    f.q0=np.stack([ex,ey,np.cross(ex,ey)],axis=2)
    return info,np.flatnonzero(keep)

def solve(row,mats,eigen_number=4):
    res=row["reserve"];mat=mats[row["material"]];ro=row["radius_m"];t=row["wall_m"]
    base,original,rr=base_data(res)
    # Given topology is a data input. This preserves the owner's member identifiers.
    points=original["points"][:252];cells=original["cells"];edges=original["edges"]
    b.geodesic=lambda freq:(points.copy(),cells.copy(),edges.copy())
    b.E=mat["Eax_Pa"];b.NU=b.E/(2*mat["Gaxhoop_Pa"])-1
    b.RHO=mat["density_kgm3"]
    ft.configure(ro=ro,wall=t)
    f=b.Frame(5,row["segments"])
    merged=None;ids=np.arange(750)
    if row["removed_member"] is not None:
        merged,ids=remove_member(f,row["removed_member"])
    K=f.linear_stiffness();Q=f.rigid_basis();volume,g,H=f.pressure()
    inverse=b.GaugeInverse(K,Q);u=inverse.projected(-P*g)
    arr=ft.force_arrays(f,u);arr["L"]=np.asarray(f.true_member_lengths)
    G=ft.geometric_stiffness(f,arr["subelement_N"])
    eigen,_,resids=b.eigen_buckling(K,G-P*H,Q,number=eigen_number)
    a,beta,e=demands(arr,mat,ro,t);A,I=section(ro,t)
    gamma=.099+.901*math.exp(-math.sqrt(ro/t)/16)
    local=gamma*mat["local_classical_coefficient_Pa"]*t/ro
    locroots=load_roots(a,beta,e,local)
    comproots=None if mat["screen_compression_Pa"] is None else load_roots(a,beta,e,mat["screen_compression_Pa"])
    jd=end_design(original["joint_N"],original["joint_M"],original["joint_T"],ro,base["least_screened_SF"])
    Aj=jd["area"][ids];rj=jd["outer"][ids];over=jd["overlap"][ids]
    Ij=Aj*(rj*rj+ro*ro)/4
    JN,JM,JT=arr["joint_N"],arr["joint_M"],arr["joint_T"]
    sleeve=1470e6/(JN/Aj+JM*rj/Ij)
    bond=28.9e6*2*math.pi*ro*over/np.sqrt((JN+2*JM/ro)**2+(JT/ro)**2)
    modes=dict(euler=float(e.min()),global_k0p2=float(.2*eigen[0]),
        local_peak=float(locroots.min()),compression=None if comproots is None else float(comproots.min()),
        joint_sleeve=float(sleeve.min()),joint_bond=float(bond.min()),
        film=base["modes"]["film"]/(1. if merged is None else merged["tension_multiplier_same_rise_to_span"]))
    sf=min(x for x in modes.values() if x is not None)
    ss,ten=peak(arr,mat,ro,t,1.)
    # Retain the installed tube mass: rupture does not imply discarded mass.
    tube=mat["density_kgm3"]*A*sum(original["L"])
    overhead=sum(v for k,v in base["mass_kg"].items() if k not in ["tube","headroom","total_with_reserve_and_sag"])
    fail={}
    for name,roots in [("local_shell",locroots),("compression",comproots)]:
        fail[name]=None if roots is None else ids[np.unique(arr["subelement_member"][roots<1])].tolist()
    result=dict(label=row["label"],ndof=f.ndof,frame_tubes_kg=tube,
       total_mass_including_reserve_sag_kg=tube+overhead,
       modes=modes,conditional_SF_or_ceiling=sf,linear_multipliers=eigen.tolist(),
       eigen_relative_residuals=resids,equilibrium_relative_residual=float(np.linalg.norm(K@u+P*g)/np.linalg.norm(P*g)),
       load_rigid_projection_ratio=float(np.linalg.norm(Q.T@g)/np.linalg.norm(g)),
       q1_peak_compression_Pa=None if ss is None else float(ss.max()),
       q1_peak_tension_Pa=ten,
       q1_whole_member_scale_needed_m10_Pf1e3_Pa=None if ss is None else scale(ss,10,.001),
       max_axial_N=float(arr["subelement_N"].max()),max_bending_Nm=float(arr["subelement_M"].max()),
       local_shell_limit_Pa=local,secondary_failure_trigger_at_q1=sf<1,
       individual_secondary_failure_members_at_q1=fail,merged_bay=merged,
       pressure_fan_volume_m3=float(volume))
    return result,arr

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--start",type=int,default=0)
    parser.add_argument("--stop",type=int,default=182);parser.add_argument("--name",default="all")
    args=parser.parse_args();mats=materials();audit=Audit();rows=read("FE-ALL.json")["rows"]
    for index in range(args.start,min(args.stop,len(rows))):
        row=rows[index];start=time.monotonic()
        calc,arr=solve(row,mats);label=row["label"]
        dump("fe/"+label+".json",calc)
        np.savez_compressed(ROOT/"fe"/(label+".npz"),**arr)
        # Numerical residuals are independent quality checks, not matching random roundoff.
        compare={k:v for k,v in calc.items() if k not in ["eigen_relative_residuals",
            "equilibrium_relative_residual","load_rigid_projection_ratio","individual_secondary_failure_members_at_q1",
            "merged_bay"]}
        audit.fields(label,row,compare,rtol=3e-6,atol=1e-7)
        audit.check(label,"equilibrium_valid",True,calc["equilibrium_relative_residual"]<1e-7)
        audit.check(label,"eigen_residuals_valid",True,max(calc["eigen_relative_residuals"])<1e-6)
        if row["merged_bay"] is not None:audit.fields(label,row["merged_bay"],calc["merged_bay"])
        for key,ids in row["individual_secondary_failure_members_at_q1"].items():
            alt=calc["individual_secondary_failure_members_at_q1"].get(key)
            if alt is not None:audit.check(label,"failed_ids/"+key,ids==alt,True)
        print(json.dumps(dict(index=index,label=label,seconds=time.monotonic()-start,
                             SF=calc["conditional_SF_or_ceiling"])),flush=True)
    audit.save("FE-CHECK-"+args.name+".json")
