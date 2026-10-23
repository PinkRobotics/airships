"""Rigid frictionless spherical indentation, followed by geometry-only import.

This resolves a known difference from the paper without fitting a pressure.
Penalty contact is integrated on the current outer meridian with its full
nodal derivative. Indenter radius=.1*42.8 mm, prescribed penetration=.75*T.
After indentation all stresses and plastic states are reset explicitly.
"""
import argparse
import json
import math
from pathlib import Path
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from fem56 import PlasticModel,trace
from axi029 import edge3,GP3,GW3

ROOT=Path(__file__).resolve().parent


def contact(model,u,depth,penalty=3000.,indenter_radius=4.28,stiffness=True):
    x=model.X+u.reshape(-1,2)
    xe=x[model.edges]
    center=np.array([0.,model.Ro+indenter_radius-depth])
    force=np.zeros(model.ndof)
    kval=np.zeros((len(model.edges),6,6))
    penetration=0.;active=0
    for xi,wq in zip(GP3,GW3):
        N,dN=edge3(xi)
        point=np.einsum("a,eai->ei",N,xe)
        deriv=np.einsum("a,eai->ei",dN,xe)
        length=np.linalg.norm(deriv,axis=1)
        vec=point-center
        dist=np.linalg.norm(vec,axis=1)
        inside=dist<indenter_radius
        penetration=max(penetration,float(np.max(np.maximum(indenter_radius-dist,0.))))
        active+=int(inside.sum())
        fac=np.where(inside,penalty*(indenter_radius/dist-1),0.)
        traction=fac[:,None]*vec
        area=2*math.pi*wq*point[:,0]*length
        fe=(N[None,:,None]*traction[:,None,:]*area[:,None,None]).reshape(-1,6)
        np.add.at(force,model.edge_dofs,fe)
        if stiffness:
            normals=vec/dist[:,None]
            deriv_traction=fac[:,None,None]*np.eye(2)[None]-(
                np.where(inside,penalty*indenter_radius/dist,0.)[:,None,None]*
                normals[:,:,None]*normals[:,None,:])
            darea=np.empty((len(model.edges),3,2))
            darea[:,:,0]=2*math.pi*wq*(length[:,None]*N[None,:]+
                                     (point[:,0]*deriv[:,0]/length)[:,None]*dN[None,:])
            darea[:,:,1]=2*math.pi*wq*(point[:,0]*deriv[:,1]/length)[:,None]*dN[None,:]
            for ia in range(3):
                for ib in range(3):
                    kval[:,2*ia:2*ia+2,2*ib:2*ib+2]+=(
                        N[ia]*N[ib]*area[:,None,None]*deriv_traction+
                        N[ia]*traction[:,:,None]*darea[:,ib,None,:])
    K=None
    if stiffness:
        rows=np.repeat(model.edge_dofs,6,axis=1).ravel()
        cols=np.tile(model.edge_dofs,(1,6)).ravel()
        K=sp.coo_matrix((kval.ravel(),(rows,cols)),shape=(model.ndof,model.ndof)).tocsr()
    return force,K,{"maximum_contact_penetration_mm":penetration,
                    "active_contact_quadrature_points":active,
                    "indenter_reaction_N":float(-force[1::2].sum())}


def indent(model,name,penalty=3000.,amplitude=.75,plastic_cap=.02):
    directory=ROOT/"runs"/name
    directory.mkdir(parents=True,exist_ok=False)
    fr=model.free;u=np.zeros(model.ndof);depth=0.;increment=.001
    target=amplitude*model.T;hist=[];cutbacks=0;start=time.monotonic()
    reason="not started"
    with (directory/"PATH.jsonl").open("w") as f:
        while depth<target-1e-10:
            goal=min(target,depth+increment)
            trial=u.copy();ok=False
            for it in range(40):
                try:
                    fi,K=model.internal(trial)
                    fc,Kc,diag=contact(model,trial,goal,penalty)
                    residual=(fi-fc)[fr]
                    scale=max(np.linalg.norm(fc[fr]),10.)
                    merit=np.linalg.norm(residual)/scale
                    if merit<2e-8 and it>0:
                        ok=True;break
                    du=spla.spsolve((K-Kc)[fr][:,fr].tocsc(),-residual)
                    if not np.all(np.isfinite(du)):break
                    accepted=False
                    for ls in range(13):
                        wt=.5**ls
                        cand=trial.copy();cand[fr]+=wt*du
                        try:
                            ff,_=model.internal(cand,False)
                            cf,_,_=contact(model,cand,goal,penalty,stiffness=False)
                            nm=np.linalg.norm((ff-cf)[fr])/scale
                            if nm<merit*(1-1e-4*wt) or nm<2e-8:
                                trial=cand;accepted=True;break
                        except (ValueError,FloatingPointError):
                            pass
                    if not accepted:break
                except (ValueError,RuntimeError,FloatingPointError):
                    break
            if not ok:
                increment*=.5;cutbacks+=1
                print(json.dumps({"indent_cutback":cutbacks,"depth":depth,"next_increment":increment}),flush=True)
                if increment<1e-7:
                    reason="indentation Newton continuation unresolved";break
                continue
            pre=model.collect(trial,False)
            dk=pre["maximum_core_plastic_increment"]
            if dk>plastic_cap:
                increment*=min(.5,.8*plastic_cap/dk);cutbacks+=1
                if increment<1e-7:
                    reason="indentation plastic continuation unresolved";break
                continue
            u=trial;depth=goal
            metrics=model.collect(u,True)
            rec={"step":len(hist)+1,"indenter_depth_mm":depth,
                 "outer_pole_mm":float(u[model.probe]),
                 "inner_pole_mm":float(u[model.inner_probe]),
                 "increment_mm":increment,"iterations":it,
                 "relative_residual":merit,"elapsed_s":time.monotonic()-start,
                 **diag,**metrics}
            hist.append(rec);f.write(json.dumps(rec)+"\n");f.flush()
            if len(hist)%20==0:
                np.savez_compressed(directory/"CHECKPOINT.npz",u=u,ep=model.ep,
                                    kap=model.kap,depth=depth)
            print(json.dumps({k:rec[k] for k in ["step","indenter_depth_mm",
                  "indenter_reaction_N","outer_pole_mm","inner_pole_mm","iterations"]}),flush=True)
            if it<=7:increment=min(.02,increment*1.2)
            elif it>=15:increment=max(1e-7,increment*.6)
        else:
            reason="prescribed indentation completed"
    np.savez_compressed(directory/"END.npz",u=u,ep=model.ep,kap=model.kap,depth=depth,
                        X=model.X,conn=model.conn)
    result={"parameters":model.parameters,"penalty_MPa_per_mm":penalty,
            "indenter_radius_mm":4.28,"target_depth_mm":target,"depth_mm":depth,
            "reason":reason,"steps":len(hist),"cutbacks":cutbacks,
            "elapsed_s":time.monotonic()-start,"last":hist[-1] if hist else None,
            "tag":"QUESTIONABLE / PROJECTION"}
    (directory/"INDENT-RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    return result,u


def verify_contact(label=None):
    m=PlasticModel(ntheta=12,ncore=2,nface=1,amplitude=0)
    u=np.zeros(m.ndof)
    u[1::2]=-.03*np.exp(-(m.X[:,0]/8)**2);u[m.fixed]=0
    f,K,_=contact(m,u,.12)
    rng=np.random.default_rng(5617);v=rng.normal(size=m.ndof);v[m.fixed]=0
    v/=np.linalg.norm(v);eps=1e-6
    a,_,_=contact(m,u+eps*v,.12,stiffness=False)
    c,_,_=contact(m,u-eps*v,.12,stiffness=False)
    fd=(a-c)/(2*eps)
    error=float(np.linalg.norm(fd-K@v)/np.linalg.norm(fd))
    result={"contact_tangent_relative_error":error,"tolerance":1e-6,"passed":error<1e-6}
    filename="CONTACT-VERIFICATION.json" if label is None else f"CONTACT-VERIFICATION-{label}.json"
    (ROOT/filename).write_text(json.dumps(result,indent=2)+"\n")
    assert result["passed"],result
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("name")
    p.add_argument("--ntheta",type=int,default=96)
    p.add_argument("--ncore",type=int,default=4)
    p.add_argument("--nface",type=int,default=2)
    p.add_argument("--penalty",type=float,default=3000.)
    p.add_argument("--radius",choices=["outer","mid"],default="outer")
    p.add_argument("--verify-only",action="store_true")
    args=p.parse_args()
    print(json.dumps(verify_contact(args.name)),flush=True)
    if args.verify_only:raise SystemExit(0)
    m=PlasticModel(ntheta=args.ntheta,ncore=args.ncore,nface=args.nface,
                   radius=args.radius,amplitude=0)
    r,u=indent(m,args.name+"-indent",penalty=args.penalty)
    if r["reason"]!="prescribed indentation completed":
        raise SystemExit(2)
    original=m.X.copy()
    m.X=m.X+u.reshape(-1,2)
    m.ep[:]=0;m.kap[:]=0
    m._precompute()
    if any(np.any(g["w"]<=0) for g in m.gp):
        raise ValueError("indented imported mesh has a nonpositive integration weight")
    m.parameters.update(imperfection="rigid spherical indentation; imported geometry; all stress/plastic state reset",
                        amplitude_mu=.75,amplitude_mm=r["depth_mm"],width_mm=None,
                        indentation_parent=args.name+"-indent",indenter_radius_mm=4.28,
                        indenter_depth_mm=r["depth_mm"],
                        actual_outer_pole_offset_mm=float(u[m.probe]),
                        actual_inner_pole_offset_mm=float(u[m.inner_probe]),
                        imported_volume_mm3=float(sum(g["w"].sum() for g in m.gp)),
                        material_state_import="reset stresses AND plastic strains AND hardening; conditional")
    r=trace(m,ROOT/"runs"/(args.name+"-pressure"),step=.0005,max_step=.02,
            plastic_step_cap=.02,elastic_step_cap=.0005,end_displacement=10.)
    print(json.dumps({"complete":args.name,"peak_MPa":r["peak"]["pressure_MPa"] if r["peak"] else None,
                      "reason":r["reason"]}),flush=True)
