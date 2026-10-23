"""Plastic extension of CHECK029's explicitly authorized Q8 FE reuse."""
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, str(Path(__file__).resolve().parent / "reuse"))
from axi029 import Model
from material56 import evaluate, baseline_tables


class PlasticModel(Model):
    def __init__(self, ntheta=96, ncore=4, nface=1, radius="outer", amplitude=.75,
                 alpha=3/math.sqrt(2), foam_scale=1., steel_scale=1., inner=.42,
                 width=None, grading=1.0):
        thickness = inner + 3.1 + .42
        ro = 42.8 + (thickness/2 if radius == "mid" else 0.)
        width = .1*ro if width is None else width
        layers = [{"t":inner,"n":nface,"mat":("iso",210000.,.33)},
                  {"t":3.1,"n":ncore,"mat":("iso",40.,0.)},
                  {"t":.42,"n":nface,"mat":("iso",210000.,.33)}]
        super().__init__(ro,layers,math.pi/2,ntheta,grading=grading,
                         dimple=(amplitude*thickness,width) if amplitude else None,
                         clamp_equator=True)
        self.parameters = dict(ntheta=ntheta,ncore=ncore,nface=nface,radius=radius,
                               radius_outer_mm=ro,amplitude_mu=amplitude,
                               amplitude_mm=amplitude*thickness,alpha=alpha,
                               foam_scale=foam_scale,steel_scale=steel_scale,
                               inner_face_mm=inner,width_mm=width,grading=grading)
        self.foam, self.steel, _, _ = baseline_tables(foam_scale, steel_scale)
        self.props = np.array([[40.,0.,alpha],[210000.,.33,0.]])
        self.kinds = np.array([0 if m[1] == 40. else 1 for m in self.emat])
        self.ep = np.zeros((9,self.ne,4))
        self.kap = np.zeros((9,self.ne))
        self.probe = 2*self.nid[0,2*self.nt]+1
        self.inner_probe = 2*self.nid[0,0]+1
        self.where_core = self.kinds == 0
        self.where_face = self.kinds == 1
        self.core_first_shear = self.foam[0,1]*math.sqrt((1+alpha**2/9)/3)

    def internal(self,u,tangent=True,linear=False,stress_from=None):
        if linear or stress_from is not None:
            return super().internal(u,tangent,linear,stress_from)
        ue = u[self.edofs].reshape(self.ne,8,2)
        f = np.zeros(self.ndof)
        Kv = np.zeros((self.ne,16,16)) if tangent else None
        for k,g in enumerate(self.gp):
            E,B = self._kin(g,ue)
            S,D,_,_,_,_ = evaluate(E,self.ep[k],self.kap[k],self.kinds,self.props,
                                  self.foam,self.steel,tangent)
            fe = np.einsum("eki,ek->ei",B,S)*g["w"][:,None]
            np.add.at(f,self.edofs,fe)
            if tangent:
                Km = B.transpose(0,2,1) @ (D @ B)
                Kv += (Km+self._geo(g,S))*g["w"][:,None,None]
        K = sp.coo_matrix((Kv.ravel(),(self.rows,self.cols)),
                          shape=(self.ndof,self.ndof)).tocsr() if tangent else None
        return f,K

    def collect(self,u,commit=False):
        ue = u[self.edofs].reshape(self.ne,8,2)
        maxima = {"core_equivalent_plastic_strain":0.,"face_equivalent_plastic_strain":0.,
                  "core_shear_MPa":0.,"core_compression_MPa":0.,"face_von_mises_MPa":0.,
                  "core_initial_yield_index":0.,"face_initial_yield_index":0.,
                  "maximum_core_plastic_increment":0.,"maximum_face_plastic_increment":0.,
                  "minimum_J":1e99,"maximum_J":0.,"core_extrapolated_points":0,
                  "core_shear_location":None,"face_yield_location":None}
        for k,g in enumerate(self.gp):
            E,_ = self._kin(g,ue)
            S,_,ep,kap,sig,extra = evaluate(E,self.ep[k],self.kap[k],self.kinds,
                                           self.props,self.foam,self.steel,False)
            dk=kap-self.kap[k]
            maxima["maximum_core_plastic_increment"]=max(maxima["maximum_core_plastic_increment"],float(dk[self.where_core].max()))
            maxima["maximum_face_plastic_increment"]=max(maxima["maximum_face_plastic_increment"],float(dk[self.where_face].max()))
            if commit:
                self.ep[k] = ep
                self.kap[k] = kap
            tr = np.sum(sig[:,:3],axis=1)/3
            q = np.sqrt(1.5*(np.sum((sig[:,:3]-tr[:,None])**2,axis=1)+2*sig[:,3]**2))
            alpha = self.props[0,2]
            eq = np.sqrt((q*q+alpha*alpha*tr*tr)/(1+alpha*alpha/9))
            maxima["core_equivalent_plastic_strain"] = max(maxima["core_equivalent_plastic_strain"],float(kap[self.where_core].max()))
            maxima["face_equivalent_plastic_strain"] = max(maxima["face_equivalent_plastic_strain"],float(kap[self.where_face].max()))
            maxima["core_initial_yield_index"] = max(maxima["core_initial_yield_index"],float(eq[self.where_core].max()/self.foam[0,1]))
            maxima["face_initial_yield_index"] = max(maxima["face_initial_yield_index"],float(q[self.where_face].max()/self.steel[0,1]))
            maxima["minimum_J"] = min(maxima["minimum_J"],float(extra[:,2].min()))
            maxima["maximum_J"] = max(maxima["maximum_J"],float(extra[:,2].max()))
            maxima["core_extrapolated_points"] += int(np.count_nonzero(kap[self.where_core]>self.foam[-1,0]+1e-10))
            # Reconstruct Cauchy tensor in current global axes and resolve the
            # shear on the deformed reference tangent, not a fixed global axis.
            F = np.zeros((self.ne,2,2))
            F[:,0,0]=1+np.einsum("ea,ea->e",g["dNr"],ue[:,:,0])
            F[:,0,1]=np.einsum("ea,ea->e",g["dNz"],ue[:,:,0])
            F[:,1,0]=np.einsum("ea,ea->e",g["dNr"],ue[:,:,1])
            F[:,1,1]=1+np.einsum("ea,ea->e",g["dNz"],ue[:,:,1])
            pk = np.zeros_like(F)
            pk[:,0,0]=S[:,0];pk[:,1,1]=S[:,1]
            pk[:,0,1]=S[:,3];pk[:,1,0]=S[:,3]
            cauchy = (F @ pk @ F.transpose(0,2,1))/extra[:,2,None,None]
            # Tangent follows the xi mapping at this integration point.
            # q8 derivatives are inherited, reconstructed from point station.
            from axi029 import q8,GP3
            xi,eta=GP3[k//3],GP3[k%3]
            _,dx,_=q8(xi,eta)
            tangent0=(self.X[self.conn].transpose(0,2,1)@dx)
            tc=np.einsum("eij,ej->ei",F,tangent0)
            tc/=np.linalg.norm(tc,axis=1)[:,None]
            nc=np.stack([-tc[:,1],tc[:,0]],axis=1)
            shear=np.abs(np.einsum("ei,eij,ej->e",tc,cauchy,nc))
            comp=-np.einsum("ei,eij,ej->e",nc,cauchy,nc)
            loc=int(np.argmax(np.where(self.where_core,shear,-np.inf)))
            if shear[loc]>maxima["core_shear_MPa"]:
                maxima["core_shear_MPa"]=float(shear[loc])
                maxima["core_shear_location"]={"element":loc,"gp":k,"reference_r_mm":float(g["r"][loc])}
            maxima["core_compression_MPa"]=max(maxima["core_compression_MPa"],float(comp[self.where_core].max()))
            loc=int(np.argmax(np.where(self.where_face,q,-np.inf)))
            if q[loc]>maxima["face_von_mises_MPa"]:
                maxima["face_von_mises_MPa"]=float(q[loc])
                maxima["face_yield_location"]={"element":loc,"gp":k,"reference_r_mm":float(g["r"][loc])}
        maxima["core_shear_initial_strength_MPa"]=self.core_first_shear
        maxima["core_shear_initial_strength_index"]=maxima["core_shear_MPa"]/self.core_first_shear
        return maxima


def trace(model, directory, step=.02, max_step=.05, end_displacement=10.,
          tolerance=2e-8, drop_fraction=.12, plastic_step_cap=None):
    """Committed-state bordered Newton with line search and adaptive cutback."""
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=False)
    (directory/"MODEL.json").write_text(json.dumps(model.parameters,indent=2)+"\n")
    np.savez_compressed(directory/"MESH.npz",X=model.X,conn=model.conn,
                        kinds=model.kinds,fixed=model.fixed,edges=model.edges)
    fr=model.free; n=len(fr);pos=int(np.where(fr==model.probe)[0][0])
    row=sp.csr_matrix(([1.],([0],[pos])),shape=(1,n))
    u=np.zeros(model.ndof);p=0.; target=0.; inc=step
    history=[];peak=-1.;peak_state=None;postpeak=0;start=time.monotonic()
    reason="not started"; retries=0;attempts=0
    first={}
    with (directory/"PATH.jsonl").open("w") as out:
        while -target<end_displacement-1e-10:
            goal=max(target-inc,-end_displacement)
            trial_u=u.copy();trial_p=p;ok=False
            for it in range(35):
                try:
                    fi,K=model.internal(trial_u)
                    fp,Kp=model.pressure(trial_u)
                    res=fi[fr]-trial_p*fp[fr]
                    g=trial_u[model.probe]-goal
                    scale=max(np.linalg.norm(trial_p*fp[fr]),100.)
                    merit=np.linalg.norm(res)/scale+abs(g)/max(inc,1e-6)
                    if np.linalg.norm(res)/scale<tolerance and abs(g)<1e-10 and it>0:
                        ok=True;break
                    KT=(K-trial_p*Kp)[fr][:,fr]
                    col=sp.csr_matrix(-fp[fr,None])
                    A=sp.bmat([[KT,col],[row,None]],format="csc")
                    d=spla.spsolve(A,np.r_[-res,-g])
                    if not np.all(np.isfinite(d)):break
                    accepted=False
                    for ls in range(12):
                        weight=.5**ls
                        cand=trial_u.copy();cand[fr]+=weight*d[:n]
                        cp=trial_p+weight*d[n]
                        try:
                            ff,_=model.internal(cand,tangent=False)
                            pf,_=model.pressure(cand,stiffness=False)
                            rr=ff[fr]-cp*pf[fr]
                            cg=cand[model.probe]-goal
                            cm=np.linalg.norm(rr)/scale+abs(cg)/max(inc,1e-6)
                            if cm<merit*(1-1e-4*weight) or cm<tolerance:
                                trial_u,trial_p=cand,cp;accepted=True;break
                        except (ValueError,FloatingPointError):
                            pass
                    if not accepted:break
                except (ValueError,RuntimeError,FloatingPointError):
                    break
            attempts+=1
            if not ok:
                retries+=1;inc*=.5
                print(json.dumps({"cutback":retries,"accepted_steps":len(history),
                                  "pressure_MPa":p,"next_step_mm":inc,"iteration":it}),flush=True)
                if inc<1e-5:
                    reason="Newton cutback exhausted; not a proven limit";break
                continue
            if plastic_step_cap is not None:
                preview=model.collect(trial_u,commit=False)
                dk=preview["maximum_core_plastic_increment"]
                if dk>plastic_step_cap:
                    retries+=1
                    inc*=min(.5,.8*plastic_step_cap/dk)
                    print(json.dumps({"plastic_cutback":retries,"dk":dk,
                                      "next_step_mm":inc,"pressure_MPa":p}),flush=True)
                    if inc<1e-7:
                        reason="plastic-increment continuity unresolved; not a proven limit";break
                    continue
            u,p,target=trial_u,trial_p,goal
            metrics=model.collect(u,commit=True)
            rec={"step":len(history)+1,"outer_pole_mm":target,
                 "inner_pole_mm":float(u[model.inner_probe]),"pressure_MPa":float(p),
                 "iterations":it,"increment_mm":inc,"relative_residual":float(np.linalg.norm(res)/scale),
                 "elapsed_s":time.monotonic()-start,**metrics}
            history.append(rec);out.write(json.dumps(rec)+"\n");out.flush()
            for key,hit in [("core_yield",metrics["core_equivalent_plastic_strain"]>1e-9),
                            ("face_yield",metrics["face_equivalent_plastic_strain"]>1e-9),
                            ("core_shear_screen",metrics["core_shear_initial_strength_index"]>=1),
                            ("foam_extrapolation",metrics["core_extrapolated_points"]>0)]:
                if hit and key not in first:
                    first[key]={"first_above":rec,"last_below":history[-2] if len(history)>1 else
                                {"pressure_MPa":0.,"outer_pole_mm":0.}}
            print(json.dumps({k:rec[k] for k in ["step","outer_pole_mm","pressure_MPa","iterations",
                                                "core_equivalent_plastic_strain","face_equivalent_plastic_strain",
                                                "core_shear_initial_strength_index"]}),flush=True)
            if p>peak:
                peak=p;peak_state=rec
                np.savez_compressed(directory/"PEAK.npz",u=u,ep=model.ep,kap=model.kap,pressure=p)
                postpeak=0
            else:
                postpeak+=1
            if postpeak>=3 and p<peak*(1-drop_fraction):
                reason="pressure peak passed and postpeak fall resolved";break
            if it<=6:inc=min(max_step,inc*1.25)
            elif it>=14:inc=max(1e-5,inc*.7)
        else:
            reason="displacement endpoint reached"
    np.savez_compressed(directory/"END.npz",u=u,ep=model.ep,kap=model.kap,pressure=p)
    result={"parameters":model.parameters,"elements":model.ne,"nodes":model.nn,
            "free_dofs":len(fr),"peak":peak_state,"first_events":first,
            "reason":reason,"steps":len(history),"attempts":attempts,"cutbacks":retries,
            "elapsed_s":time.monotonic()-start,"tag":"QUESTIONABLE / PROJECTION",
            "capacity_validated":False,
            "limit_point_bracketed":postpeak>=3 and peak_state is not None,
            "requested_step_mm":step,"maximum_step_mm":max_step,
            "end_displacement_mm":end_displacement,"tolerance":tolerance}
    result["plastic_step_cap"]=plastic_step_cap
    (directory/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    return result


if __name__=="__main__":
    import argparse
    a=argparse.ArgumentParser()
    a.add_argument("name")
    a.add_argument("--ntheta",type=int,default=96)
    a.add_argument("--ncore",type=int,default=4)
    a.add_argument("--nface",type=int,default=1)
    a.add_argument("--radius",choices=["outer","mid"],default="outer")
    a.add_argument("--alpha",type=float,default=3/math.sqrt(2))
    a.add_argument("--foam-scale",type=float,default=1.)
    a.add_argument("--steel-scale",type=float,default=1.)
    a.add_argument("--amplitude",type=float,default=.75)
    a.add_argument("--inner",type=float,default=.42)
    a.add_argument("--width",type=float)
    a.add_argument("--grading",type=float,default=1.)
    a.add_argument("--step",type=float,default=.02)
    a.add_argument("--max-step",type=float,default=.05)
    a.add_argument("--end",type=float,default=10.)
    a.add_argument("--plastic-step-cap",type=float)
    args=a.parse_args()
    m=PlasticModel(**{k:v for k,v in vars(args).items() if k not in ["name","step","max_step","end","plastic_step_cap"]})
    r=trace(m,Path(__file__).resolve().parent/"runs"/args.name,step=args.step,
            max_step=args.max_step,end_displacement=args.end,plastic_step_cap=args.plastic_step_cap)
    print(json.dumps({"complete":args.name,"peak_MPa":r["peak"]["pressure_MPa"] if r["peak"] else None,
                      "reason":r["reason"]}),flush=True)
