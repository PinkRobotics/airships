"""Independent CHECK-040 heat balance; no upstream executable dependencies."""
from pathlib import Path
import json
import numpy as np
from numpy.polynomial import legendre as lg

ROOT = Path(__file__).resolve().parent
SIGMA = 5.670374419e-8
TA = 284.9
RHO_C = 16.018463373960138
RHO_AIR = 4889.442150186961/(4*np.pi*10**3/3)

def temperatures(radius, thickness, n=128, solid_density=2700, midpoint=False, h_floor=0.):
    if midpoint:
        x = (np.arange(n)+.5)*2/n-1
        w = np.full(n, 2/n)
    else:
        x, w = lg.leggauss(n)
    tc = np.atleast_1d(thickness)[:,None]
    U = 130*RHO_C/solid_density/tc
    Re = RHO_AIR*2*(2*radius)/1.79e-5
    h = .0257/(2*radius)*(2+(.4*np.sqrt(Re)+.06*Re**(2/3))*.71**.4)
    h = max(h_floor,h)
    out = []
    diagnostics=[]
    for sky, solar in [(275,970),(260,0)]:
        incoming = .9*SIGMA*((1+x)/2*sky**4+(1-x)/2*TA**4)
        incoming += .2*solar*np.maximum(x,0)
        To = np.full((len(tc),n),TA)
        Ti = To.copy()
        # Newton solve for local faces and the shared interior radiosity.
        for it in range(100):
            mean4 = Ti**4 @ (w/2)
            f = h*(To-TA)+.9*SIGMA*To**4 + U*(To-Ti)-incoming
            g = U*(Ti-To)+.2*SIGMA*(Ti**4-mean4[:,None])
            aa = h+3.6*SIGMA*To**3+U
            bb = -.8*SIGMA*Ti**3*(w/2)
            dd = U+.8*SIGMA*Ti**3-U**2/aa
            rhs = -g-U*f/aa
            # rank-one Schur complement: (diag(dd)+1*bb) dTi=rhs
            dt_i = rhs/dd - (np.sum(bb*rhs/dd,axis=1)/(1+np.sum(bb/dd,axis=1)))[:,None]/dd
            dt_o = (-f+U*dt_i)/aa
            Ti += dt_i
            To += dt_o
            if max(np.max(abs(dt_i)),np.max(abs(dt_o))) < 2e-11: break
        diagnostics.append(dict(iterations=it+1,update_K=float(max(np.max(abs(dt_i)),np.max(abs(dt_o)))),
                                energy_residual_W_m2=float(max(np.max(abs(f)),np.max(abs(g)))),h_W_m2K=h))
        out.append((To,Ti))
    return x,w,out,diagnostics

def solve(radius, thickness, n=128, solid_density=2700, midpoint=False, pattern="mean"):
    x,w,daynight,diagnostics=temperatures(radius,thickness,n,solid_density,midpoint)
    To,Ti=daynight[0]
    Tno,Tni=daynight[1]
    pat=(To+Ti)/2 if pattern=="mean" else To
    pat=pat-np.sum(pat*w/2,axis=1)[:,None]
    coeff=(pat*w) @ lg.legvander(x,6) * ((2*np.arange(7)+1)/2)
    coeff[:,:2]=0
    # Find exact extrema of curvature polynomial, including endpoints.
    curv=[]
    for c in coeff:
        dp=lg.legder(c);ddp=lg.legder(c,2)
        # (1-x*x)*T'' - x*T' ; converted polynomial for roots.
        q=np.polynomial.Polynomial(lg.leg2poly(ddp))*np.polynomial.Polynomial([1,0,-1])
        q-=np.polynomial.Polynomial(lg.leg2poly(dp))*np.polynomial.Polynomial([0,1])
        roots=q.deriv().roots()
        nodes=[-1,1]+[float(z.real) for z in roots if abs(z.imag)<1e-9 and -1<z.real<1]
        curv.append(float(np.max(abs(q(nodes)))))
    return dict(tc_m=np.atleast_1d(thickness).tolist(),
                gradient_K=np.max(abs(To-Ti),axis=1).tolist(),
                swing_K=(np.max(To,axis=1)-np.min(Tno,axis=1)).tolist(),
                rise_K=(np.max(To,axis=1)-TA).tolist(),
                curvature_temperature_K=curv,
                max_outer_K=np.max(To,axis=1).tolist(),
                min_outer_K=np.min(Tno,axis=1).tolist(),
                diagnostics=diagnostics)

if __name__=="__main__":
    import sys
    if "--table" in sys.argv:
        ans={str(r):solve(r,np.geomspace(.001*r/10,1.5*r/10,241)) for r in [10,12,15,20,30]}
        (ROOT/"THERMAL-INDEPENDENT.json").write_text(json.dumps(ans,indent=2)+"\n")
        print("independent thermal tables saved")
    else:
        for density in [2640,2700]:
            for pattern in ["mean","outer"]:
                print(density,pattern,solve(10,.02210679007353296,solid_density=density,pattern=pattern))
