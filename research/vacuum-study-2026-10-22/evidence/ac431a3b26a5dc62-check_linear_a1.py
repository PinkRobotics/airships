"""Fresh Q8 small-strain/prestress eigenproblem, from equations and source data."""
import gc
import json
import math
import time

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh, spsolve
from source_a1 import ROOT, read

natural=np.array([[-1,-1],[1,-1],[1,1],[-1,1],[0,-1],[1,0],[0,1],[-1,0]],float)
def mono(s,t):
    return np.array([1,s,t,s*t,s*s,t*t,s*s*t,s*t*t])
inv=np.linalg.inv(np.array([mono(s,t) for s,t in natural]))
def shp(s,t):
    return (mono(s,t)@inv,
            np.array([[0,1,0,t,2*s,0,2*s*t,t*t],
                      [0,0,1,s,0,2*t,s*s,2*s*t]])@inv)

def run(outer_radius, ntheta=384, ncore=8, nface=2):
    started=time.monotonic()
    radial=np.concatenate([np.linspace(outer_radius-3.94,outer_radius-3.52,2*nface+1),
                           np.linspace(outer_radius-3.52,outer_radius-.42,2*ncore+1)[1:],
                           np.linspace(outer_radius-.42,outer_radius,2*nface+1)[1:]])
    nr=(len(radial)-1)//2
    indices=np.full((2*ntheta+1,len(radial)),-1,int)
    coords=[]
    for i in range(2*ntheta+1):
        theta=math.pi*i/(4*ntheta)
        for j,r in enumerate(radial):
            if i%2 and j%2:continue
            indices[i,j]=len(coords)
            coords.append([r*math.sin(theta),r*math.cos(theta)])
    X=np.array(coords)
    connectivity=[]; kinds=[]
    for i in range(0,2*ntheta,2):
        for j in range(0,2*nr,2):
            connectivity.append([indices[i,j],indices[i+2,j],indices[i+2,j+2],indices[i,j+2],
                                 indices[i+1,j],indices[i+2,j+1],indices[i+1,j+2],indices[i,j+1]])
            kinds.append(0 if 2*nface<=j<2*(nface+ncore) else 1)
    conn=np.array(connectivity); kinds=np.array(kinds)
    ne=len(conn); nn=len(X); coords_e=X[conn]
    edofs=np.empty((ne,16),int)
    edofs[:,::2]=2*conn; edofs[:,1::2]=2*conn+1
    fixed=np.concatenate([2*indices[0],2*indices[-1],2*indices[-1]+1])
    free=np.setdiff1d(np.arange(2*nn),fixed)
    g,w=np.polynomial.legendre.leggauss(3)
    E=np.where(kinds==0,40.,210000.)
    nu=np.where(kinds==0,0.,.33)
    mu=E/(2*(1+nu)); la=E*nu/((1+nu)*(1-2*nu))
    D=np.zeros((ne,4,4))
    D[:,:3,:3]=la[:,None,None]
    for j in range(3):D[:,j,j]+=2*mu
    D[:,3,3]=mu
    Ke=np.zeros((ne,16,16)); gauss=[]
    for i,s in enumerate(g):
        for j,t in enumerate(g):
            N,dn=shp(s,t); dn=dn.T
            jac=np.einsum("eai,aj->eij",coords_e,dn)
            grad=np.einsum("ai,eij->eaj",dn,np.linalg.inv(jac))
            radius=coords_e[:,:,0]@N
            weights=2*math.pi*radius*np.linalg.det(jac)*w[i]*w[j]
            B=np.zeros((ne,4,16))
            B[:,0,::2]=grad[:,:,0]
            B[:,1,1::2]=grad[:,:,1]
            B[:,2,::2]=N[None,:]/radius[:,None]
            B[:,3,::2]=grad[:,:,1]
            B[:,3,1::2]=grad[:,:,0]
            Ke+=np.einsum("eai,eab,ebj,e->eij",B,D,B,weights,optimize=True)
            gauss.append((N,grad,radius,weights,B))
    row=np.repeat(edofs,16,axis=1).ravel()
    col=np.tile(edofs,(1,16)).ravel()
    K=coo_matrix((Ke.ravel(),(row,col)),shape=(2*nn,2*nn)).tocsc()
    del Ke
    # Pressure is a reference-direction (dead) unit load for this anchor.
    edges=np.array([[indices[i,-1],indices[i+1,-1],indices[i+2,-1]]
                    for i in range(0,2*ntheta,2)])
    fe=np.zeros((nn,2))
    for s,wt in zip(g,w):
        N=np.array([s*(s-1)/2,1-s*s,s*(s+1)/2])
        dn=np.array([s-.5,-2*s,s+.5])
        r=X[edges]
        rad=r[:,:,0]@N
        tang=np.einsum("eai,a->ei",r,dn)
        area=np.column_stack([tang[:,1],-tang[:,0]])
        val=2*math.pi*wt*rad[:,None,None]*N[None,:,None]*area[:,None,:]
        for a in range(3):np.add.at(fe,edges[:,a],val[:,a])
    Kf=K[free][:,free]
    u=np.zeros(2*nn)
    u[free]=spsolve(Kf,fe.ravel()[free])
    preload_res=float(np.linalg.norm(Kf@u[free]-fe.ravel()[free])/np.linalg.norm(fe.ravel()[free]))
    ue=u[edofs]
    Ge=np.zeros((ne,16,16))
    for N,grad,radius,weights,B in gauss:
        stress=np.einsum("eab,ebj,ej->ea",D,B,ue,optimize=True)
        S=np.zeros((ne,2,2))
        S[:,0,0]=stress[:,0];S[:,1,1]=stress[:,1]
        S[:,0,1]=S[:,1,0]=stress[:,3]
        base=np.einsum("eai,eij,ebj,e->eab",grad,S,grad,weights,optimize=True)
        Ge[:,::2,::2]+=base
        Ge[:,1::2,1::2]+=base
        Ge[:,::2,::2]+=np.einsum("a,b,e->eab",N,N,weights*stress[:,2]/radius**2)
    G=coo_matrix((Ge.ravel(),(row,col)),shape=K.shape).tocsc()[free][:,free]
    # Largest eigenvalues of (-G)v=mu K v give the smallest positive p=1/mu.
    eig,v=eigsh(-G,k=4,M=Kf,which="LA",tol=2e-10)
    pressures=np.sort(1/eig)
    k=int(np.argmax(eig))
    rayleigh=float(-(v[:,k]@(Kf@v[:,k]))/(v[:,k]@(G@v[:,k])))
    residual=float(np.linalg.norm(Kf@v[:,k]+pressures[0]*(G@v[:,k])) /
                   np.linalg.norm(Kf@v[:,k]))
    return {"radius_outer_mm":outer_radius,"ntheta":ntheta,"ncore":ncore,"nface":nface,
            "nodes":nn,"elements":ne,"free_dofs":len(free),
            "dead_pressure_MPa":float(pressures[0]),"first_four_MPa":pressures.tolist(),
            "Rayleigh_pressure_MPa":rayleigh,"unit_preload_relative_residual":preload_res,
            "eigen_relative_residual":residual,"elapsed_seconds":time.monotonic()-started,
            "tag":"QUESTIONABLE; conditional linear anchor"}

out=[]
expected=read("056--RESULTS.json")["linear_results"]
for name,r in [("outer",42.8),("mid",44.77)]:
    answer=run(r)
    ref=next(x for x in expected if x["radius_reading"]==name and x["ntheta"]==384)
    answer["radius_reading"]=name
    reference=min(ref["dead_pressure_MPa"])
    answer["owner_dead_pressure_MPa"]=reference
    answer["difference_MPa"]=answer["dead_pressure_MPa"]-reference
    answer["gap_to_paper_27p53_percent"]=100*(answer["dead_pressure_MPa"]/27.53-1)
    out.append(answer)
    print(json.dumps(answer,indent=2),flush=True)
    gc.collect()
(ROOT/"LINEAR-CHECK.json").write_text(json.dumps({"scope":"Two fresh linear/prestress eigenproblem anchors; no owner code.",
                                                "cases":out},indent=2)+"\n")
