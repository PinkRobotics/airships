"""Independent CHECK-051 formulas. Inputs are data, never owner programs."""
import sys, json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), "unpublished-local-ref:e2218733e161c504"]
import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp
P = 95460.8379139
LIFT = 4889.44215019
UP = ROOT / "intake/upstream/intake"
OWNER = ROOT / "intake/owner"
BASE = json.loads((UP/"041/RESULTS.json").read_text())["best_closure_by_reserve"]

def read(name):
    return json.loads((OWNER/name).read_text())

def dump(path, data):
    path = ROOT/path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False,
        default=lambda x: x.tolist() if isinstance(x,np.ndarray) else x.item())+"\n")

class Audit:
    def __init__(self): self.rows=[]
    def check(self,row,field,owner,independent,rtol=2e-8,atol=1e-9):
        if owner is None or independent is None:
            ok = owner is None and independent is None
        elif isinstance(owner,(bool,str)):
            ok = owner == independent
        else:
            ok = bool(np.isclose(owner,independent,rtol=rtol,atol=atol))
        self.rows.append(dict(row=row,field=field,owner=owner,independent=independent,
                              rtol=rtol,atol=atol,passed=bool(ok)))
    def fields(self,row,owner,independent,rtol=2e-8,atol=1e-9,prefix=""):
        for k,v in independent.items():
            if k not in owner: continue
            if isinstance(v,dict):
                self.fields(row,owner[k],v,rtol,atol,prefix+k+".")
            elif isinstance(v,(list,np.ndarray)):
                for j,(o,x) in enumerate(zip(owner[k],v)):
                    if isinstance(x,(dict,list,np.ndarray)): continue
                    self.check(row,prefix+k+f"[{j}]",o,x,rtol,atol)
            else: self.check(row,prefix+k,owner[k],v,rtol,atol)
    def save(self,name):
        bad=[r for r in self.rows if not r["passed"]]
        dump(name,dict(comparisons=len(self.rows),mismatches=len(bad),rows=self.rows))
        print(json.dumps(dict(artifact=name,comparisons=len(self.rows),mismatches=len(bad))),flush=True)

def strain_transform(deg):
    c,s=math.cos(math.radians(deg)),math.sin(math.radians(deg))
    return np.array([[c*c,s*s,c*s],[s*s,c*c,-c*s],
                     [-2*c*s,2*c*s,c*c-s*s]])

def local_coefficient(Q):
    a=np.linalg.inv(Q)
    # Rational quadratic in y=z². Derivative numerator is a quadratic.
    n=np.array([Q[0,0],2*(Q[0,1]+2*Q[2,2]),Q[1,1]])
    d=np.array([a[1,1],2*a[0,1]+a[2,2],a[0,0]])
    poly=np.polynomial.polynomial.polysub(
        np.polynomial.polynomial.polymul([n[1],2*n[2]],d),
        np.polynomial.polynomial.polymul(n,[d[1],2*d[2]]))
    candidates=[n[0]/d[0],n[2]/d[2]]
    for y in np.polynomial.polynomial.polyroots(poly):
        if abs(y.imag)<1e-8 and y.real>=0:
            candidates.append(np.polynomial.polynomial.polyval(y.real,n)/
                              np.polynomial.polynomial.polyval(y.real,d))
    return math.sqrt(min(candidates)/3)

def materials():
    # E1,E2,G12 in GPa; nu, density, longitudinal compression, transverse tension, shear.
    iso={"041-reference":(410,.14,3100,3.9),"Hexoloy-SA":(430,.14,3100,3.9),
         "CVD-PureSiC-HR":(462,.21,3210,None),"UltraSiC-sintered":(410,.21,3150,3.5),
         "Al6061T6":(68.3,.33,2700,.276)}
    comp={
        "SCS6-epoxy":(.6*380+.4*3,6,4.2,.30,.6*3080+.4*1200,None,None,None),
        "SCSUltra-epoxy":(.6*415+.4*3,6,4.2,.30,.6*2890+.4*1200,None,None,None),
        "HNS-MI-CMC-scenario":(230,230,70,.2,2700,1.,None,None),
        "Tyranno-SA-CVI-scenario":(230,230,70,.2,2750,None,None,None),
        "M55J":(338,6,4.2,.35,.6*1910+.4*1200,.89,.037,.068),
        "K13D2U":(.6*935+.4*3,8,4.5,.30,.6*2200+.4*1200,None,None,None),
        "T700S":(134,8,4.5,.30,.6*1800+.4*1200,1.45,.081,.136)}
    out={}
    for ref in read("MATERIAL-MODELS.json"):
        name=ref["id"]
        if name in iso:
            E,nu,rho,X=iso[name]; E1=E2=E;G=E/(2*(1+nu));Y=S=None
        else:
            key=next(k for k in comp if name==k or name.startswith(k+"-"))
            E1,E2,G,nu,rho,X,Y,S=comp[key]
        denom=1-nu*nu*E2/E1
        lam=np.array([[E1,nu*E2,0],[nu*E2,E2,0],[0,0,G*denom]])*1e9/denom
        Q=sum(f*(strain_transform(t).T@lam@strain_transform(t)) for t,f in ref["layup"])
        a=np.linalg.inv(Q)
        ratios=[lam@strain_transform(t)@[address]([-1.,0,0]) for t,f in ref["layup"]]
        caps=[]
        for ss in ratios:
            if X is not None and ss[0]<0:caps.append(X*1e9/-ss[0])
            if Y is not None and ss[1]>0:caps.append(Y*1e9/ss[1])
            if S is not None and abs(ss[2])>1e-15:caps.append(S*1e9/abs(ss[2]))
        out[name]=dict(id=name,Eax_Pa=1/a[0,0],Ehoop_Pa=1/a[1,1],Gaxhoop_Pa=1/a[2,2],
          nu_axhoop=-a[0,1]/a[0,0],density_kgm3=rho,Q_Pa=Q,lamina_Q_Pa=lam,
          local_classical_coefficient_Pa=local_coefficient(Q),
          screen_compression_Pa=min(caps) if caps else None,
          ply_Xc_GPa=X,ply_transverse_tension_GPa=Y,ply_shear_GPa=S,layup=ref["layup"],
          ply_ratios=ratios)
    return out

def section(ro,t):
    A=math.pi*t*(2*ro-t)
    I=A*(ro*ro+(ro-t)**2)/4
    return A,I

def base_data(res):
    d=np.load(UP/f"check041/runs/f5-{res}-m24/STATIC.npz",allow_pickle=False)
    rr=json.loads((UP/f"check041/runs/f5-{res}-m24/RESULTS.json").read_text())
    arrays={k:d[k].copy() for k in d.files}
    arrays["L"]=np.asarray(rr["geometry"]["member_arc_lengths_m"])
    return BASE[res],arrays,rr

def demands(arr,mat,ro,t):
    A,I=section(ro,t)
    N=arr["subelement_N"]; M=arr["subelement_M"]
    L=arr["L"][arr["subelement_member"]]
    a=N/A
    beta=(M+abs(N)*L/1000)*ro/I
    e=np.full(len(N),np.inf)
    mask=N>0
    e[mask]=math.pi**2*mat["Eax_Pa"]*I/(L[mask]**2*N[mask])
    return a,beta,e

def peak(arr,mat,ro,t,q):
    a,b,e=demands(arr,mat,ro,t)
    if np.min(e)<=q: return None,None
    bend=q*b/(1-q/e)
    c=np.maximum(0,q*a+bend)
    ten=np.maximum(0,-q*a+bend)
    peaks=np.zeros(len(arr["L"]))
    np.maximum.at(peaks,arr["subelement_member"],c)
    return peaks,float(ten.max())

def load_roots(a,b,e,S):
    # Direct quadratic for compressed segments, linear for tensile segments.
    d=a+b+S/e
    roots=np.full(len(a),np.inf)
    mask=a>0
    roots[mask]=2*S/(d[mask]+np.sqrt(np.maximum(0,d[mask]**2-4*a[mask]*S/e[mask])))
    mask2=(~mask)&(a+b>0)
    roots[mask2]=S/(a[mask2]+b[mask2])
    return roots

def scale(stress,m,pf,weights=1.):
    ss=np.asarray(stress); good=ss>0
    ww=np.broadcast_to(weights,ss.shape)[good]
    return float(np.exp((logsumexp(m*np.log(ss[good])+np.log(ww))-math.log(-math.log1p(-pf)))/m))

def probability(stress,m,s0,weights=1.):
    ss=np.asarray(stress);good=ss>0
    if not good.any():return 0.
    hlog=logsumexp(m*np.log(ss[good]/s0)+np.log(np.broadcast_to(weights,ss.shape)[good]))
    return 1. if hlog>7 else float(-np.expm1(-np.exp(hlog)))

def shape_needed(stress,s0,pf,weights=1.):
    ss=np.asarray(stress)
    if ss.max()>=s0:return None
    logs=np.log(ss[ss>0]/s0); target=math.log(-math.log1p(-pf))
    logw=np.log(np.broadcast_to(weights,ss.shape)[ss>0])
    hi=2.
    while logsumexp(hi*logs+logw)>target: hi*=2
    return brentq(lambda m:logsumexp(m*logs+logw)-target,1e-8,hi,xtol=1e-12)

def target_row(stress,L,A,m,pf):
    return dict(equal_complete_member_scale_GPa=scale(stress,m,pf)/1e9,
      common_3m_reference_scale_GPa=scale(stress,m,pf,L/3)/1e9,
      coupon_1cm3_scale_GPa=scale(stress,m,pf,A*L/1e-6)/1e9,
      hypothetical_all_750_lengths_3m_coupon_scale_GPa=scale(stress,m,pf,A*3/1e-6)/1e9,
      three_m_member_volume_cm3=A*3/1e-6,
      coupon_to_3m_strength_retention=(A*3/1e-6)**(-1/m))

def fixed_score(res,mat,ro,t,arr=None):
    base,aa,rr=base_data(res)
    if arr is None:arr=aa
    A,I=section(ro,t);a,b,e=demands(arr,mat,ro,t)
    gamma=.099+.901*math.exp(-math.sqrt(ro/t)/16)
    loc=gamma*mat["local_classical_coefficient_Pa"]*t/ro
    modes=dict(euler=float(e.min()),local_axial=float((loc/a).min()),
      local_peak=float(load_roots(a,b,e,loc).min()),
      global_k0p2=.2*rr["linear_multipliers"][0]*mat["Eax_Pa"]*I/(410e9*base["section"]["inertia_m4"]),
      film=base["modes"]["film"],joint=base["least_screened_SF"],
      compression=None if mat["screen_compression_Pa"] is None else float(load_roots(a,b,e,mat["screen_compression_Pa"]).min()))
    sf=min(x for x in modes.values() if x is not None)
    mass=mat["density_kgm3"]*A*sum(arr["L"])
    total=mass+sum(v for k,v in base["mass_kg"].items() if k not in ["tube","headroom","total_with_reserve_and_sag"])
    ss,_=peak(arr,mat,ro,t,1.)
    s0=mat["screen_compression_Pa"] if mat["id"]!="Al6061T6" else None
    oldlim=gamma*.6*mat["Eax_Pa"]*t/ro
    result=dict(ro_m=ro,wall_m=t,area_m2=A,inertia_m4=I,frame_tubes_kg=mass,
      frame_plus_joints_nodes_kg=mass+base["mass_kg"]["joint"]+base["mass_kg"]["nodes"],
      total_mass_including_reserve_sag_kg=total,lift_headroom_kg=LIFT-total,modes=modes,
      conditional_SF_or_ceiling=sf,legacy_isotropic_local_axial=float((oldlim/a).min()),
      legacy_isotropic_local_peak=float(load_roots(a,b,e,oldlim).min()),
      q1_peak_compression_Pa=None if ss is None else float(ss.max()),
      q1_whole_member_scale_needed_m10_Pf1e3_Pa=None if ss is None else scale(ss,10,.001),
      hypothetical_m10_strength_multiplier_over_typical=None if ss is None or s0 is None else scale(ss,10,.001)/s0,
      hypothetical_m_needed_if_typical_is_whole_member_scale=None if ss is None or s0 is None else shape_needed(ss,s0,.001),
      hypothetical_m10_Pf_if_typical_is_whole_member_scale=None if ss is None or s0 is None else probability(ss,10,s0))
    return result
