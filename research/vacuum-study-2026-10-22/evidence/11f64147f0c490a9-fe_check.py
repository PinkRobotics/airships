from pathlib import Path
import argparse
import json
import time
import math
import numpy as np
from independent_fe import Model,shape

ROOT=Path(__file__).resolve().parent


def reference(a):
    R,tf,tc,nu,E=(a[k] for k in ("R","tf","tc","nuf","Ef"))
    h=tf+tc
    pcl=4*E*tf*h/(R*R*np.sqrt(1-nu*nu))*1000
    crimp=2*h*h*(6800*.006894757293168361)/(R*tc)*1000
    V=pcl/crimp
    K=1-V/4 if V<=2 else 1/V
    return dict(p_classical_kPa=pcl,p_crimp_kPa=crimp,Vc=V,Kc=K,p_H_kPa=pcl*K)


def validate():
    out={}
    errors=[]
    for x in np.linspace(-.9,.9,7):
        for y in np.linspace(-.9,.9,7):
            n,d=shape(x,y)
            errors.append(abs(sum(n)-1));errors.extend(abs(d.sum(axis=0)))
    out["shape_partition_error"]=max(errors)
    m=Model(R=100,tf=.2,tc=.6,Ef=70000,nuf=.3,nth=16,a=30,grading=1)
    u=.0001*np.random.default_rng(1970).normal(size=m.ndof);u[np.setdiff1d(np.arange(m.ndof),m.free)]=0
    f,K,l,Kp=m.evaluate(u)
    v=np.random.default_rng(2000).normal(size=m.ndof);v[np.setdiff1d(np.arange(m.ndof),m.free)]=0
    eps=1e-6
    fp,_,lp,_=m.evaluate(u+eps*v)
    fm,_,lm,_=m.evaluate(u-eps*v)
    diff=(fp-fm)/(2*eps);pred=K@v
    out["internal_tangent_relative_error"]=float(np.linalg.norm(diff-pred)/np.linalg.norm(pred))
    diff=(lp-lm)/(2*eps);pred=Kp@v
    out["pressure_tangent_relative_error"]=float(np.linalg.norm(diff-pred)/np.linalg.norm(pred))
    out["internal_symmetry_error"]=float(np.linalg.norm((K-K.T).data)/np.linalg.norm(K.data))
    Kpf=Kp[m.free,:][:,m.free]
    out["pressure_symmetry_on_free_error"]=float(np.linalg.norm((Kpf-Kpf.T).data)/np.linalg.norm(Kpf.data))
    homogeneous=[]
    for R in (100,1000):
        m=Model(R=R,tf=.2,tc=.6,Ef=70000,nuf=.3,nth=128,grading=1,homogeneous=True)
        p=.00001
        u,info=m.solve_load(p)
        node=int(np.argmin((m.X[:,0]-R)**2+m.X[:,1]**2))
        ri=R-1
        exact=-p*R/(70000*(R**3-ri**3))*((1-2*.3)*R**3+(1+.3)/2*ri**3)
        homogeneous.append(dict(R=R,t=1,outer_radial_mm=float(u[2*node]),exact_small_strain_mm=exact,
                                relative_error=float(u[2*node]/exact-1),solver=info))
    out["homogeneous_spheres"]=homogeneous
    out["passed"]=bool(out["shape_partition_error"]<1e-13 and
                       out["internal_tangent_relative_error"]<1e-5 and
                       out["pressure_tangent_relative_error"]<1e-6 and
                       all(abs(r["relative_error"])<.001 for r in homogeneous))
    (ROOT/"FE-VALIDATION.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2),flush=True)
    if not out["passed"]:raise RuntimeError("Independent FE validation failed")


def path_run(label,outlabel=None,nth=None,grading=1.5,nface=1,ncore=4,Ein=.01,
             amplitude=None,targets=None,peak_refine=False):
    start=time.monotonic()
    original=json.loads((ROOT/"intake/owner-runs"/(label+".json")).read_text())
    a={k:float(v) for k,v in original["args"].items() if k!="label"}
    a["nth"]=int(a["nth"] if nth is None else nth)
    if amplitude is not None:a["amp"]=amplitude
    m=Model(**a,grading=grading,nface=nface,ncore=ncore,Ein=Ein)
    ref=reference(a)
    name=outlabel or label
    folder=ROOT/"fe-runs";folder.mkdir(exist_ok=True)
    out=dict(label=name,owner_comparison_label=label,inputs=m.inputs,reference=ref,
             nodes=len(m.X),elements=len(m.elements),free_equations=len(m.free),
             control="outer north pole axial displacement; inner south pole axial anchor for sphere",
             path=[],status="running")
    target_values=targets if targets is not None else [r["pole_dz_mm"] for r in original["path"]]
    u=np.zeros(m.ndof);p=0.
    def advance(target,u,p,depth=0):
        try:
            return m.solve_control(target,u,p)
        except (RuntimeError,ValueError):
            if depth>=6:raise
            mid=.5*(u[m.control]+target)
            um,pm,_=advance(mid,u,p,depth+1)
            return advance(target,um,pm,depth+1)
    peak_states=[]
    for target in target_values:
        u,p,info=advance(target,u,p)
        *_,diag=m.evaluate(u,True)
        row=dict(pole_dz_mm=float(u[m.control]),p_kPa=float(p*1000),**diag,**info)
        out["path"].append(row)
        if peak_refine:peak_states.append((target,u.copy(),p))
        (folder/(name+".json")).write_text(json.dumps(out,indent=2)+"\n")
        print(name,round(target,5),round(p*1000,8),round(diag["core_tau"],8),flush=True)
    if peak_refine:
        j=int(np.argmax([r["p_kPa"] for r in out["path"]]))
        if 0<j<len(peak_states)-1:
            # Fine sampling of a bracket, retaining the pressure decline on both sides.
            t0,u0,p0=peak_states[j-1]
            t1=peak_states[j+1][0]
            fine=[]
            for target in np.linspace(t0,t1,13)[1:-1]:
                un,pn,info=advance(float(target),u0,p0)
                *_,diag=m.evaluate(un,True)
                fine.append(dict(pole_dz_mm=float(target),p_kPa=float(pn*1000),**diag,**info))
            out["peak_refinement"]=fine
    allpoints=out["path"]+out.get("peak_refinement",[])
    peak=max(allpoints,key=lambda row:row["p_kPa"])
    out["limit_kPa"]=peak["p_kPa"];out["pole_dz_at_limit_mm"]=peak["pole_dz_mm"]
    out["gamma_H_elastic"]=peak["p_kPa"]/ref["p_H_kPa"]
    out["owner_limit_kPa"]=original["limit_kPa"]
    out["relative_limit_difference"]=out["limit_kPa"]/original["limit_kPa"]-1
    thresholds={"face_yield_outer":("outer_vm",a["sy"],1),
                "face_yield_inner":("inner_vm",a["sy"],1),
                "core_W_shear_typ":("core_tau",35*.006894757293168361,1),
                "core_W_shear_min":("core_tau",25*.006894757293168361,1),
                "core_crush_typ":("core_min_snn",35*.006894757293168361,-1)}
    crosses={}
    for key,(field,threshold,sign) in thresholds.items():
        previous={field:0,"p_kPa":0};cross=None
        for row in out["path"]:
            if sign*row[field]>=threshold:
                cross=previous["p_kPa"]+(row["p_kPa"]-previous["p_kPa"])*(threshold-sign*previous[field])/(sign*(row[field]-previous[field]))
                break
            previous=row
        crosses[key]=cross
    out["crossings_kPa"]=crosses
    out["elapsed_seconds"]=time.monotonic()-start;out["status"]="complete"
    (folder/(name+".json")).write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps({k:out[k] for k in ("label","limit_kPa","gamma_H_elastic","relative_limit_difference","crossings_kPa","elapsed_seconds")}),flush=True)
    return out


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["validate","path"])
    p.add_argument("--label",default="S1-be-sphere-d16")
    p.add_argument("--outlabel")
    p.add_argument("--nth",type=int)
    p.add_argument("--grading",type=float,default=1.5)
    p.add_argument("--nface",type=int,default=1)
    p.add_argument("--ncore",type=int,default=4)
    p.add_argument("--Ein",type=float,default=.01)
    p.add_argument("--amplitude",type=float)
    p.add_argument("--smoke",action="store_true")
    p.add_argument("--peak-refine",action="store_true")
    args=p.parse_args()
    if args.action=="validate":validate()
    else:path_run(args.label,args.outlabel,args.nth,args.grading,args.nface,args.ncore,args.Ein,
                  args.amplitude,[-.5,-1,-2] if args.smoke else None,args.peak_refine)
