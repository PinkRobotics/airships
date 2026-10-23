"""Triangular-dish integration: exact linear-strip positive part, Gauss in t."""
from liquid_check import ROOT,dump
import json,numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import interp1d

P=json.loads((ROOT/'owner/PONDS.json').read_text())
S=P['radii']['10']['s_m']
V=np.array([[0,1/np.sqrt(3)],[-.5,-1/(2*np.sqrt(3))],[.5,-1/(2*np.sqrt(3))]])
AREA=np.sqrt(3)/4
C=1-np.sqrt(11/12)
K=2*P['mean_per_crown']

def dish(beta,azimuth,n=384,k=K):
    beta,azimuth=np.broadcast_arrays(beta,azimuth)
    b=beta.ravel();phi=azimuth.ravel()
    t,w=leggauss(n);t=(t+1)/2;w=w/2
    x=V[:,0,None]*np.cos(phi)+V[:,1,None]*np.sin(phi)
    low=x.min(axis=0)
    depth=k*C*t*(2-t)
    vol=np.zeros(len(b));wet=vol.copy()
    for i in range(3):
        j,l=[m for m in range(3) if m!=i]
        a=depth[None,:]-np.tan(b[:,None])*((1-t)[None,:]*x[j,:,None]-low[:,None])
        z=depth[None,:]-np.tan(b[:,None])*((1-t)[None,:]*x[l,:,None]-low[:,None])
        delta=z-a
        nz=np.abs(delta)>1e-14
        mean=np.where(nz,(np.maximum(z,0)**2-np.maximum(a,0)**2)/(2*np.where(nz,delta,1)),np.maximum(a,0))
        fraction=np.where(nz,(np.maximum(z,0)-np.maximum(a,0))/np.where(nz,delta,1),(a>0).astype(float))
        vol+=(mean*((2/3)*(1-t)*w)).sum(axis=1)*AREA
        wet+=(fraction*((2/3)*(1-t)*w)).sum(axis=1)*AREA
    return vol.reshape(beta.shape),wet.reshape(beta.shape)

def lattice():
    # One up and one down equilateral triangle per primitive cell; each counted once.
    a=np.array([1.,0]);b=np.array([.5,np.sqrt(3)/2])
    centers=[];angles=[]
    for i in range(-3,4):
        for j in range(-3,4):
            v=i*a+j*b
            centers.extend([v+(a+b)/3,v+2*(a+b)/3])
            angles.extend([0.,np.pi])
    return np.array(centers),np.array(angles)

def placement(top,n=256):
    centers,ang=lattice()
    d=centers-np.array(top)
    bet=np.arctan(np.linalg.norm(d,axis=1)*S/10)
    # Height increases toward the top point, opposite the outward displacement.
    phi=np.arctan2(d[:,1],d[:,0])+np.pi-ang
    vol,wet=dish(bet,phi,n)
    return float(vol.sum()*S**3*1000),float(np.sum(wet*np.cos(bet))*S*S)

def main():
    bet=np.deg2rad(np.array(P['beta_deg']))
    az=np.arange(144)*2*np.pi/144
    own=[];coarse=[]
    for b in bet:
        x,_=dish(np.full_like(az,min(b,np.pi/2-1e-9)),az,n=384)
        own.append(float(x.mean()))
        x,_=dish(np.full_like(az,min(b,np.pi/2-1e-9)),az,n=192)
        coarse.append(float(x.mean()))
    own=np.array(own);owner=np.array(P['pond_volume_per_s3'])
    # Model-independent expected total: bay density times angular integral.
    expected=4*np.pi*100*1000*S/AREA * np.trapezoid(own*np.sin(bet),bet)/2
    pface=placement([.5,np.sqrt(3)/6],384)
    pvertex=placement([0,0],384)
    # Translation sweep is deterministic and reproducible (no unseen random seed).
    samples=[]
    for i in range(32):
        for j in range(32):
            top=(i+.5)/32*np.array([1.,0])+(j+.5)/32*np.array([.5,np.sqrt(3)/2])
            samples.append(placement(top,96)[0])
    sample=np.array(samples)
    out=dict(crown_per_s=C,exact_shape_normalization=K,owner_k=P['k_shape'],
        level_volume_per_s3=AREA*C*P['mean_per_crown'],
        owner_level_volume_per_s3=P['pond_volume_per_s3'][0],
        orientation_integral_kg=expected,owner_integral_kg=P['radii']['10']['pond_capacity_kg'],
        face_up_kg=pface[0],face_up_surface_m2=pface[1],
        node_up_kg=pvertex[0],node_up_surface_m2=pvertex[1],
        sample_1024=dict(mean=float(sample.mean()),min=float(sample.min()),max=float(sample.max()),
                         p05=float(np.quantile(sample,.05)),p95=float(np.quantile(sample,.95))),
        max_quadrature_difference_s3=float(np.max(abs(own-np.array(coarse)))),
        profile=[dict(beta_deg=b,own=v,owner=o,delta=v-o) for b,v,o in zip(P['beta_deg'],own,owner)],
        beta_method='atan(distance/R), lattice directions retained, volume normal to bay plane')
    dump('PONDS-INDEPENDENT.json',out)
    print(json.dumps({k:v for k,v in out.items() if k!='profile'},indent=2))
if __name__=='__main__':main()
