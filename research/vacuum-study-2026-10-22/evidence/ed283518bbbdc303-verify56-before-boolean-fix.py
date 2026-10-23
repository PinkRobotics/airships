"""Analytic material limits, irreversible unloading, FE tangent and linear anchors."""
import json
import math
from pathlib import Path
import time

import numpy as np
from material56 import return_log, point, evaluate, baseline_tables
from fem56 import PlasticModel

ROOT=Path(__file__).resolve().parent
rows=[]

def check(name,observed,expected,tol):
    error=float(np.max(np.abs(np.asarray(observed)-np.asarray(expected))))
    rows.append(dict(name=name,observed=np.asarray(observed).tolist(),
                     expected=np.asarray(expected).tolist(),absolute_tolerance=tol,
                     maximum_absolute_error=error,passed=bool(error<=tol)))

t0=time.monotonic()
ep=np.zeros(4)
perfect=np.array([[0.,1.4],[10.,1.4]])
a=3/math.sqrt(2)
sig,pe,k,*_=return_log(np.array([-.1,0.,0.,0.]),ep,0.,40.,0.,a,perfect)
check("foam uniaxial plateau",sig,[-1.4,0,0,0],1e-10)
check("foam residual compression",pe,[-.065,0,0,0],1e-10)
check("foam accumulated strain",k,.065,1e-10)
sig,pe2,k2,*_=return_log(pe,pe,k,40.,0.,a,perfect)
check("unloading to permanent strain gives zero stress",sig,np.zeros(4),1e-10)
check("unloading preserves plastic strain",k2,k,1e-10)
sig,*_=return_log(np.array([-.1,-.1,-.1,0.]),ep,0.,40.,0.,a,perfect)
check("hydrostatic initial yield is uniaxial divided sqrt3",sig[:3],np.full(3,-1.4/math.sqrt(3)),1e-10)
sig,*_=return_log(np.array([0.,0.,0.,.2]),ep,0.,40.,0.,a,perfect)
check("pure shear plateau is uniaxial divided sqrt2",sig,[0,0,0,1.4/math.sqrt(2)],1e-10)
steelpp=np.array([[0.,750.],[10.,750.]])
sig,pe,k,*_=return_log(np.array([-.02,0.,0.,.015]),ep,0.,210000.,.33,0.,steelpp)
mean=np.mean(sig[:3]);q=math.sqrt(1.5*(np.sum((sig[:3]-mean)**2)+2*sig[3]**2))
check("J2 von Mises perfect plasticity",q,750.,1e-8)
check("J2 plastic incompressibility",pe[:3].sum(),0.,1e-12)
check("J2 hydrostatic elastic stress",mean,-.02*210000/(3*(1-2*.33)),1e-8)
foam,steel,totalf,totals=baseline_tables()
check("positive foam plastic-strain knots",float(np.diff(foam[:,0]).min())>0,True,0)
# Homogeneous uniaxial strain with zero lateral strains for nu=nu_p=0.
for e,s in totalf:
    sig,pe,k,*_=return_log(np.array([-e,0.,0.,0.]),np.zeros(4),0.,40.,0.,a,foam)
    check(f"digitized compression knot e={e}",-sig[0],s,1e-9)
# General alpha branch has a genuinely different analytic hydrostatic result.
for alpha in [1.,1.5,3.]:
    sig,pe,k,*_=return_log(np.array([-.2,-.2,-.2,0.]),np.zeros(4),0.,40.,0.,alpha,perfect)
    expect=-1.4*math.sqrt(1+alpha**2/9)/alpha
    check(f"general DF hydrostatic alpha={alpha}",sig[:3],np.full(3,expect),1e-9)
# Finite compression reconstructs Cauchy independently from PK2.
F=np.diag([math.exp(-.2),1.,1.])
green=np.array([(F[0,0]**2-1)/2,0.,0.,0.])
pk,_,_,sig,_,_,jac=point(green,np.zeros(4),0.,40.,0.,a,perfect)
S=np.diag(pk[:3])
check("finite strain PK2 pushforward",np.diag(F@[address]/np.linalg.det(F)),sig[:3],1e-10)
# Superposed rotation objectivity, including a sheared finite state.
F=np.array([[.83,.12,0.],[-.03,1.04,0.],[0.,0.,.98]])
C=F.T@F
green=np.array([(C[0,0]-1)/2,(C[1,1]-1)/2,(C[2,2]-1)/2,C[0,1]])
pk,*_=point(green,np.zeros(4),0.,40.,0.,a,perfect)
S=np.array([[pk[0],pk[3],0.],[pk[3],pk[1],0.],[0.,0.,pk[2]]])
angle=.71;Q=np.array([[math.cos(angle),-math.sin(angle),0.],
                     [math.sin(angle),math.cos(angle),0.],[0.,0.,1.]])
stress=F@[address]/np.linalg.det(F)
stress_rot=(Q@F)@S@(Q@F).T/np.linalg.det(Q@F)
check("superposed rigid rotation objectivity",stress_rot,Q@[address],1e-10)
# Full assembled residual derivative: perturbed nodal field, plastic state,
# independent difference size and random direction.
m=PlasticModel(ntheta=12,ncore=2,nface=1)
u=np.zeros(m.ndof)
u[1::2]=-.07*np.exp(-(m.X[:,0]/8)**2)
u[m.fixed]=0
fi,K=m.internal(u)
fp,Kp=m.pressure(u)
rng=np.random.default_rng(5661)
direction=rng.normal(size=m.ndof);direction[m.fixed]=0
direction/=np.linalg.norm(direction)
dh=2e-6;press=1.7
fi1,_=m.internal(u+dh*direction,False);fp1,_=m.pressure(u+dh*direction,False)
fi2,_=m.internal(u-dh*direction,False);fp2,_=m.pressure(u-dh*direction,False)
fd=(fi1-fi2-press*(fp1-fp2))/(2*dh)
an=(K-press*Kp)@direction
relative=np.linalg.norm(fd-an)/np.linalg.norm(fd)
check("assembled plastic follower residual tangent",relative,0.,2e-5)
lin=[]
for radius in ["outer","mid"]:
    m=PlasticModel(ntheta=96,ncore=4,nface=1,radius=radius,amplitude=0.)
    values,_,_=m.linear_buckling(nev=4)
    lin.append({"radius":radius,"ntheta":96,"ncore":4,"nface":1,
                "dead_pressure_MPa":values.tolist()})
    if radius=="outer":
        check("029 exact coarse linear anchor",float(values[0]),30.23653,.0001)
result={"checks":rows,"all_passed":all(x["passed"] for x in rows),
        "linear_anchors":lin,"elapsed_s":time.monotonic()-t0,
        "scope":"Numerical constitutive and FE checks; not experimental validation."}
(ROOT/"VERIFICATION.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2),flush=True)
raise SystemExit(0 if result["all_passed"] else 1)
