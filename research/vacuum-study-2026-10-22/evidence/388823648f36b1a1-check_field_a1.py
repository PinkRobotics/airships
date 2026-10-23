"""Own virtual-work pressure reconstruction from pinned data, no owner code."""
import json
import math
from pathlib import Path

import numpy as np
from source_a1 import ROOT, read, runfile

CASE = "indent-mid192p30k-pressure"
mesh = np.load(runfile(CASE, "MESH.npz"), allow_pickle=False)
state = np.load(runfile(CASE, "PEAK.npz"), allow_pickle=False)
X, conn, kinds, fixed, edges = [mesh[k] for k in ("X", "conn", "kinds", "fixed", "edges")]
u = state["u"].reshape((-1, 2))
x = X + u
Xe, xe = X[conn], x[conn]
ne, nn = len(conn), len(X)
free = np.ones(2*nn, dtype=bool)
free[fixed] = False

# Derive Q8 interpolation by polynomial nodal interpolation, without importing
# a finite-element implementation or copying a tabulated shape-function routine.
natural = np.array([[-1,-1],[1,-1],[1,1],[-1,1],[0,-1],[1,0],[0,1],[-1,0]], float)
def monom(s, t):
    return np.array([1,s,t,s*t,s*s,t*t,s*s*t,s*t*t])
Vinv = np.linalg.inv(np.array([monom(s,t) for s,t in natural]))
def shape(s,t):
    N = monom(s,t) @ Vinv
    ds = np.array([0,1,0,t,2*s,0,2*s*t,t*t]) @ Vinv
    dt = np.array([0,0,1,s,0,2*t,s*s,2*s*t]) @ Vinv
    return N, np.array([ds,dt]).T
assert np.max(abs(np.array([shape(s,t)[0] for s,t in natural])-np.eye(8))) < 1e-14
g, w = np.polynomial.legendre.leggauss(3)

pre = []
for i,s in enumerate(g):
    for j,t in enumerate(g):
        N, dn = shape(s,t)
        jac = np.einsum("eai,aj->eij", Xe, dn)
        det = np.linalg.det(jac)
        assert min(det) > 0
        grad = np.einsum("ai,eij->eaj", dn, np.linalg.inv(jac))
        F2 = np.einsum("eai,eaj->eij", xe, grad)
        ref_r = Xe[:,:,0] @ N
        cur_r = xe[:,:,0] @ N
        hoop = cur_r/ref_r
        J = np.linalg.det(F2)*hoop
        C2 = np.einsum("eki,ekj->eij", F2, F2)
        eig, vec = np.linalg.eigh(C2)
        assert min(eig.ravel()) > 0
        H2 = np.einsum("eik,ek,ejk->eij",vec,.5*np.log(eig),vec)
        Ui = np.einsum("eik,ek,ejk->eij",vec,1/np.sqrt(eig),vec)
        H3 = np.log(hoop)
        volume = 2*math.pi*ref_r*det*w[i]*w[j]
        pre.append((i,j,N,grad,F2,hoop,J,H2,Ui,H3,volume,ref_r))

# Independent outward-surface integration. Edge nodes are end, middle, end.
unitload = np.zeros((nn,2))
for s, wt in zip(g,w):
    N = np.array([s*(s-1)/2,1-s*s,s*(s+1)/2])
    dn = np.array([s-.5,-2*s,s+.5])
    surf = x[edges]
    rad = surf[:,:,0] @ N
    tangent = np.einsum("eai,a->ei",surf,dn)
    inward_area = np.column_stack((tangent[:,1],-tangent[:,0]))
    local = 2*math.pi*wt*rad[:,None,None]*N[None,:,None]*inward_area[:,None,:]
    for a in range(3):
        np.add.at(unitload,edges[:,a],local[:,a])
f = unitload.ravel()[free]
material = read("056--INPUTS.json")
young = np.where(kinds==0,40.,210000.)
poisson = np.where(kinds==0,0.,.33)
mu = young/(2*(1+poisson))
lam = young*poisson/((1+poisson)*(1-2*poisson))

def reconstruction(transpose_gp, hoop_component, shear_tensor_factor):
    force = np.zeros((nn,2))
    Jmin = 1e30
    worst_yield = 0.
    extrapolated = 0
    max_kappa = 0.
    volume = 0.
    shear_component = 3 if hoop_component==2 else 2
    for i,j,N,grad,F2,hoop,J,H2,Ui,H3,dvol,ref_r in pre:
        k = j*3+i if transpose_gp else i*3+j
        ep = state["ep"][k]
        kap = state["kap"][k]
        elastic2 = H2.copy()
        elastic2[:,0,0] -= ep[:,0]
        elastic2[:,1,1] -= ep[:,1]
        elastic2[:,0,1] -= ep[:,shear_component]*shear_tensor_factor
        elastic2[:,1,0] -= ep[:,shear_component]*shear_tensor_factor
        elastic3 = H3-ep[:,hoop_component]
        trace = np.trace(elastic2,axis1=1,axis2=2)+elastic3
        stress2 = 2*mu[:,None,None]*elastic2+lam[:,None,None]*trace[:,None,None]*np.eye(2)
        stress3 = 2*mu*elastic3+lam*trace
        # P = J F U^-1 sigma_hat U^-1 and hoop analogue.
        P2 = J[:,None,None] * (F2 @ Ui @ stress2 @ Ui)
        P3 = J*stress3/hoop
        local = np.einsum("eij,eaj->eai",P2,grad)
        local[:,:,0] += P3[:,None]*N[None,:]/ref_r[:,None]
        local *= dvol[:,None,None]
        for a in range(8):
            np.add.at(force,conn[:,a],local[:,a])
        Jmin = min(Jmin,float(J.min()))
        volume += float(dvol.sum())
        core = kinds==0
        mean = (np.trace(stress2,axis1=1,axis2=2)+stress3)/3
        s2 = stress2-mean[:,None,None]*np.eye(2)
        s3 = stress3-mean
        qsq = 1.5*(np.sum(s2*s2,axis=(1,2))+s3*s3)
        eq = np.sqrt((qsq+4.5*mean*mean)/1.5)
        curve=np.array(material["foam_plastic_strain_strength_MPa"])
        kk=kap[core]
        strength=np.interp(kk,curve[:,0],curve[:,1])
        slope=(curve[-1,1]-curve[-2,1])/(curve[-1,0]-curve[-2,0])
        strength += np.maximum(kk-curve[-1,0],0)*slope
        worst_yield=max(worst_yield,float(np.max(eq[core]/strength)))
        extrapolated+=int(np.count_nonzero(kk>curve[-1,0]))
        max_kappa=max(max_kappa,float(kk.max()))
    internal=force.ravel()[free]
    pressure=float(np.dot(internal,f)/np.dot(f,f))
    relative=float(np.linalg.norm(internal-pressure*f)/np.linalg.norm(pressure*f))
    return {"gauss_order":"eta_outer" if transpose_gp else "xi_outer",
            "hoop_plastic_component":hoop_component,"plastic_shear_tensor_factor":shear_tensor_factor,
            "pressure_from_equilibrium_MPa":pressure,"relative_free_force_residual":relative,
            "minimum_J":Jmin,"reference_volume_mm3":volume,
            "max_foam_yield_surface_ratio":worst_yield,"core_extrapolated_points":extrapolated,
            "max_core_equivalent_plastic_strain":max_kappa}

# State metadata omit the component/quadrature layout. Check both standard
# axisymmetric Voigt arrangements and tensor/engineering shear conventions.
# Nothing in this search changes material constants, geometry or pressure.
trials=[reconstruction(gp,h,sh) for gp in (False,True) for h in (2,3) for sh in (.5,1.)]
best=min(trials,key=lambda z:z["relative_free_force_residual"])
best["file_pressure_MPa"]=float(state["pressure"])
best["pressure_difference_MPa"]=best["pressure_from_equilibrium_MPa"]-best["file_pressure_MPa"]
assert best["relative_free_force_residual"] < 1e-7, best
assert abs(best["pressure_difference_MPa"]) < 1e-7, best

paths=[]
for case in (CASE,"indent-mid96p30k-pressure","indent-mid96p60k-pressure","indent-outer96p30k-pressure"):
    rows=[json.loads(line) for line in runfile(case,"PATH.jsonl").read_text().splitlines() if line]
    top=max(rows,key=lambda z:z["pressure_MPa"])
    index=rows.index(top)
    paths.append({"case":case,"samples":len(rows),"peak":top,
                  "adjacent_pressures_MPa":[z["pressure_MPa"] for z in rows[max(0,index-1):index+2]],
                  "three_following_lower":all(z["pressure_MPa"]<top["pressure_MPa"] for z in rows[index+1:index+4])})
result={"tag":"QUESTIONABLE / PROJECTION","scope":"Independent frozen-state virtual work, not a rerun of plastic/contact history or stability proof.",
        "best_reconstruction":best,"layout_checks":trials,"pressure_path_checks":paths,
        "owner_code_read_or_executed":False}
(ROOT/"FIELD-CHECK.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
print(json.dumps(best,indent=2),flush=True)
print("Independent frozen-state equilibrium and pressure-path checks passed.",flush=True)
