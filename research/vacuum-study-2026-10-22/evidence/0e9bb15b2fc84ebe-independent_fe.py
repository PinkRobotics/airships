"""Independent axisymmetric total-Lagrangian Q8 solver for CHECK055.

Units N, mm, MPa. Independently derived weak form of 1/2 E:C:E,
with live exterior pressure. No owner/predecessor executable is read.
"""
import math
import numpy as np
from numba import njit
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu


def shape(x,y):
    N=np.zeros(8);D=np.zeros((8,2))
    for i,(sx,sy) in enumerate(((-1,-1),(1,-1),(1,1),(-1,1))):
        N[i]=.25*(1+sx*x)*(1+sy*y)*(sx*x+sy*y-1)
        D[i,0]=.25*sx*(1+sy*y)*(2*sx*x+sy*y)
        D[i,1]=.25*sy*(1+sx*x)*(sx*x+2*sy*y)
    N[4]=.5*(1-x*x)*(1-y);D[4]=[-x*(1-y),-.5*(1-x*x)]
    N[5]=.5*(1+x)*(1-y*y);D[5]=[.5*(1-y*y),-(1+x)*y]
    N[6]=.5*(1-x*x)*(1+y);D[6]=[-x*(1+y),.5*(1-x*x)]
    N[7]=.5*(1-x)*(1-y*y);D[7]=[-.5*(1-y*y),-(1-x)*y]
    return N,D


def iso(E,nu):
    mu=E/(2*(1+nu));la=E*nu/((1+nu)*(1-2*nu))
    C=np.zeros((4,4));C[:3,:3]=la
    C[np.arange(3),np.arange(3)]+=2*mu;C[3,3]=mu
    return C


@njit(cache=True)
def element_eval(ue, Ns, grads, weights, Cs, radii):
    # Engineering strain vector [E_rr,E_zz,E_tt,2 E_rz].
    ne=ue.shape[0];forces=np.zeros((ne,16));tangents=np.zeros((ne,16,16))
    stresses=np.zeros((ne,9,4));deformations=np.zeros((ne,9,5))
    energies=np.zeros(ne)
    for e in range(ne):
        for q in range(9):
            F00=1.;F01=0.;F10=0.;F11=1.;F22=1.
            for i in range(8):
                nr=grads[e,q,i,0];nz=grads[e,q,i,1]
                F00+=ue[e,2*i]*nr;F01+=ue[e,2*i]*nz
                F10+=ue[e,2*i+1]*nr;F11+=ue[e,2*i+1]*nz
                F22+=ue[e,2*i]*Ns[q,i]/radii[e,q]
            strain=np.array([.5*(F00*F00+F10*F10-1),
                             .5*(F01*F01+F11*F11-1),
                             .5*(F22*F22-1),F00*F01+F10*F11])
            S=Cs[e,q]@strain
            w=weights[e,q];energies[e]+=.5*w*np.dot(S,strain)
            B=np.zeros((4,16))
            for i in range(8):
                nr=grads[e,q,i,0];nz=grads[e,q,i,1]
                B[0,2*i]=F00*nr;B[0,2*i+1]=F10*nr
                B[1,2*i]=F01*nz;B[1,2*i+1]=F11*nz
                B[2,2*i]=F22*Ns[q,i]/radii[e,q]
                B[3,2*i]=F00*nz+F01*nr
                B[3,2*i+1]=F10*nz+F11*nr
            matB=Cs[e,q]@B
            for i in range(16):
                for a in range(4):forces[e,i]+=w*B[a,i]*S[a]
                for j in range(16):
                    for a in range(4):tangents[e,i,j]+=w*B[a,i]*matB[a,j]
            for i in range(8):
                nr=grads[e,q,i,0];nz=grads[e,q,i,1]
                for j in range(8):
                    mr=grads[e,q,j,0];mz=grads[e,q,j,1]
                    geo=w*(S[0]*nr*mr+S[1]*nz*mz+S[3]*(nr*mz+nz*mr))
                    tangents[e,2*i,2*j]+=geo+w*S[2]*Ns[q,i]*Ns[q,j]/radii[e,q]**2
                    tangents[e,2*i+1,2*j+1]+=geo
            det=(F00*F11-F01*F10)*F22
            stresses[e,q,0]=(F00*F00*S[0]+2*F00*F01*S[3]+F01*F01*S[1])/det
            stresses[e,q,1]=(F10*F10*S[0]+2*F10*F11*S[3]+F11*F11*S[1])/det
            stresses[e,q,2]=F22*F22*S[2]/det
            stresses[e,q,3]=(F00*F10*S[0]+(F00*F11+F01*F10)*S[3]+F01*F11*S[1])/det
            deformations[e,q]=np.array([F00,F01,F10,F11,F22])
    return forces,tangents,stresses,deformations,energies


@njit(cache=True)
def pressure_eval(coords, lineN, lineD, lineW):
    ne=coords.shape[0];f=np.zeros((ne,6));K=np.zeros((ne,6,6))
    for e in range(ne):
        for q in range(3):
            r=0.;dr=0.;dz=0.
            for i in range(3):
                r+=lineN[q,i]*coords[e,i,0]
                dr+=lineD[q,i]*coords[e,i,0]
                dz+=lineD[q,i]*coords[e,i,1]
            w=2*math.pi*lineW[q]
            for i in range(3):
                ni=lineN[q,i]
                f[e,2*i]+=w*ni*r*dz
                f[e,2*i+1]-=w*ni*r*dr
                for j in range(3):
                    nj=lineN[q,j];dj=lineD[q,j]
                    K[e,2*i,2*j]+=w*ni*nj*dz
                    K[e,2*i,2*j+1]+=w*ni*r*dj
                    K[e,2*i+1,2*j]-=w*ni*(nj*dr+r*dj)
    return f,K


class Model:
    def __init__(self,R,tf,tc,Ef,nuf,amp=0,width=356.777,nth=512,
                 a=None,nface=1,ncore=4,grading=1.5,Ein=.01,Gin=.005,
                 homogeneous=False,**unused):
        self.inputs=dict(R=R,tf=tf,tc=tc,Ef=Ef,nuf=nuf,amp=amp,width=width,
                         nth=nth,a=a,nface=nface,ncore=ncore,grading=grading,Ein=Ein)
        self.R=R;self.a=a
        self.theta_max=math.pi if a is None else math.asin(a/R)
        self.theta=self.theta_max*np.linspace(0,1,2*nth+1)**grading
        rb=R-2*tf-tc
        radii=np.concatenate([np.linspace(rb,rb+tf,2*nface+1)[:-1],
                              np.linspace(rb+tf,rb+tf+tc,2*ncore+1)[:-1],
                              np.linspace(rb+tf+tc,R,2*nface+1)])
        nr=(len(radii)-1)//2;ids={};points=[]
        for j,th in enumerate(self.theta):
            for k,rr in enumerate(radii):
                if j%2==1 and k%2==1:continue
                ids[j,k]=len(points)
                rdef=rr-amp*math.exp(-(R*th/width)**2)
                points.append([rdef*math.sin(th),rdef*math.cos(th)])
        self.X=np.array(points)
        self.X[np.abs(self.X[:,0])<1e-9,0]=0
        elements=[];materials=[]
        for j in range(nth):
            for k in range(nr):
                ij=[(2*j,2*k),(2*j+2,2*k),(2*j+2,2*k+2),(2*j,2*k+2),
                    (2*j+1,2*k),(2*j+2,2*k+1),(2*j+1,2*k+2),(2*j,2*k+1)]
                elements.append([ids[p] for p in ij])
                materials.append(0 if k<nface else (2 if k>=nface+ncore else 1))
        self.elements=np.array(elements);self.material=np.array(materials)
        self.dofs=(2*self.elements[:,:,None]+np.arange(2)).reshape(-1,16)
        self.edges=np.array([[ids[2*j,2*nr],ids[2*j+1,2*nr],ids[2*j+2,2*nr]] for j in range(nth)])
        self.edofs=(2*self.edges[:,:,None]+np.arange(2)).reshape(-1,6)
        self.ndof=2*len(points)
        constrained=[2*i for (j,k),i in ids.items() if j==0 or (a is None and j==2*nth)]
        if a is None:constrained.append(2*ids[2*nth,0]+1)
        else:constrained.extend(v for (j,k),i in ids.items() if j==2*nth for v in (2*i,2*i+1))
        self.free=np.setdiff1d(np.arange(self.ndof),np.array(constrained))
        self.control=2*ids[0,2*nr]+1;self.control_local=int(np.where(self.free==self.control)[0][0])
        self.krows=np.broadcast_to(self.dofs[:,:,None],(len(elements),16,16)).ravel()
        self.kcols=np.broadcast_to(self.dofs[:,None,:],(len(elements),16,16)).ravel()
        self.prows=np.broadcast_to(self.edofs[:,:,None],(nth,6,6)).ravel()
        self.pcols=np.broadcast_to(self.edofs[:,None,:],(nth,6,6)).ravel()
        q,w=np.polynomial.legendre.leggauss(3)
        Ns=[];Ds=[];ws=[]
        for i,x in enumerate(q):
            for j,y in enumerate(q):
                n,d=shape(x,y);Ns.append(n);Ds.append(d);ws.append(w[i]*w[j])
        self.Ns=np.array(Ns);Ds=np.array(Ds)
        Xe=self.X[self.elements]
        # J[physical component, reference coordinate].
        J=np.einsum("eia,qib->eqab",Xe,Ds)
        self.grads=np.einsum("qia,eqab->eqib",Ds,np.linalg.inv(J))
        self.qcoords=np.einsum("qi,eia->eqa",self.Ns,Xe)
        self.radii=self.qcoords[:,:,0]
        det=np.linalg.det(J)
        assert np.all(det>0)
        self.weights=2*np.pi*self.radii*det*np.array(ws)[None,:]
        tangent=J[:,:,:,0];tangent=tangent/np.linalg.norm(tangent,axis=2)[:,:,None]
        self.tangent=tangent
        self.Cs=np.broadcast_to(iso(Ef,nuf),(len(elements),9,4,4)).copy()
        if not homogeneous:
            tr=tangent[:,:,0];tz=tangent[:,:,1];nr0=-tz;nz0=tr
            L=np.zeros_like(self.Cs)
            L[:,:,0,0]=tr*tr;L[:,:,0,1]=tz*tz;L[:,:,0,3]=tr*tz
            L[:,:,1,0]=nr0*nr0;L[:,:,1,1]=nz0*nz0;L[:,:,1,3]=nr0*nz0
            L[:,:,2,2]=1
            L[:,:,3,0]=2*tr*nr0;L[:,:,3,1]=2*tz*nz0;L[:,:,3,3]=tr*nz0+tz*nr0
            Ccore=np.diag([Ein,15000*.006894757293168361,Ein,6800*.006894757293168361])
            Crot=np.einsum("eqai,ab,eqbj->eqij",L,Ccore,L)
            self.Cs[self.material==1]=Crot[self.material==1]
        self.lineN=np.column_stack([.5*q*(q-1),1-q*q,.5*q*(q+1)])
        self.lineD=np.column_stack([q-.5,-2*q,q+.5])
        self.lineW=w

    def evaluate(self,u,diagnostics=False):
        ue=u[self.dofs]
        f,k,stress,F,energy=element_eval(ue,self.Ns,self.grads,self.weights,self.Cs,self.radii)
        force=np.bincount(self.dofs.ravel(),weights=f.ravel(),minlength=self.ndof)
        K=coo_matrix((k.ravel(),(self.krows,self.kcols)),shape=(self.ndof,self.ndof)).tocsc()
        fp,kp=pressure_eval((self.X+u.reshape(-1,2))[self.edges],self.lineN,self.lineD,self.lineW)
        load=np.bincount(self.edofs.ravel(),weights=fp.ravel(),minlength=self.ndof)
        KP=coo_matrix((kp.ravel(),(self.prows,self.pcols)),shape=(self.ndof,self.ndof)).tocsc()
        if not diagnostics:return force,K,load,KP
        vm=np.sqrt(.5*((stress[:,:,0]-stress[:,:,1])**2+(stress[:,:,1]-stress[:,:,2])**2+
                       (stress[:,:,2]-stress[:,:,0])**2)+3*stress[:,:,3]**2)
        # Current tangent is F times reference tangent.
        tr=F[:,:,0]*self.tangent[:,:,0]+F[:,:,1]*self.tangent[:,:,1]
        tz=F[:,:,2]*self.tangent[:,:,0]+F[:,:,3]*self.tangent[:,:,1]
        length=np.sqrt(tr*tr+tz*tz);tr/=length;tz/=length;nr=-tz;nz=tr
        shear=tr*(stress[:,:,0]*nr+stress[:,:,3]*nz)+tz*(stress[:,:,3]*nr+stress[:,:,1]*nz)
        snn=nr*nr*stress[:,:,0]+2*nr*nz*stress[:,:,3]+nz*nz*stress[:,:,1]
        core=(self.material==1)
        locations=np.einsum("qi,eia->eqa",self.Ns,(self.X+u.reshape(-1,2))[self.elements])
        ix=np.unravel_index(np.argmax(np.abs(shear[core])),shear[core].shape)
        diag=dict(outer_vm=float(vm[self.material==2].max()),
                  inner_vm=float(vm[self.material==0].max()),
                  core_tau=float(np.abs(shear[core]).max()),
                  core_tau_r_mm=float(locations[core][ix][0]),
                  core_min_snn=float(snn[core].min()),
                  min_jacobian=float(np.min((F[:,:,0]*F[:,:,3]-F[:,:,1]*F[:,:,2])*F[:,:,4])),
                  strain_energy=float(energy.sum()))
        return force,K,load,KP,diag

    def solve_control(self,target,u=None,p=0,maxiter=25):
        u=np.zeros(self.ndof) if u is None else u.copy()
        for it in range(maxiter):
            force,K,load,KP=self.evaluate(u)
            residual=force-p*load
            err=float(np.max(np.abs(residual[self.free])))
            scale=max(1.,float(np.max(np.abs((p*load)[self.free]))))
            if err<1e-7*scale and abs(target-u[self.control])<1e-8:
                return u,p,dict(iterations=it,residual_N=err,scaled_residual=err/scale)
            tangent=(K-p*KP)[self.free,:][:,self.free]
            lu=splu(tangent)
            solutions=lu.solve(np.column_stack([-residual[self.free],load[self.free]]))
            v,w=solutions[:,0],solutions[:,1]
            dp=(target-u[self.control]-v[self.control_local])/w[self.control_local]
            du=v+w*dp
            if not np.all(np.isfinite(du)):raise RuntimeError("Nonfinite Newton step")
            # Control increments are externally cut back on failure.
            u[self.free]+=du;p+=dp
        raise RuntimeError(f"Newton did not converge: target={target} p={p}, residual={err/scale}")

    def solve_load(self,p,u=None,maxiter=25):
        u=np.zeros(self.ndof) if u is None else u.copy()
        for it in range(maxiter):
            force,K,load,KP=self.evaluate(u)
            residual=force-p*load
            scale=max(1.,float(np.max(np.abs((p*load)[self.free]))))
            err=float(np.max(np.abs(residual[self.free])))/scale
            if err<1e-7:return u,dict(iterations=it,scaled_residual=err)
            lu=splu((K-p*KP)[self.free,:][:,self.free])
            u[self.free]+=lu.solve(-residual[self.free])
        raise RuntimeError(f"Load-control failure p={p}, residual={err}")
