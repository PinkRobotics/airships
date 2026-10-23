"""Explicit independent thermal closure; all boundary choices are recorded."""
from check_model import *
from functools import lru_cache
from numpy.polynomial.legendre import leggauss,Legendre
SIGMA=5.670374419e-8

@lru_cache(None)
def quad(n,legacy=False):
    if legacy:
        x=-1+(np.arange(n)+.5)*2/n;w=np.ones(n)*2/n
    else:x,w=leggauss(n)
    return x,w

def coefficient(R,diameter_factor=2,minimum_h=0):
    D=diameter_factor*R
    Re=AIR*2*D/1.79e-5
    Nu=2+(.4*np.sqrt(Re)+.06*Re**(2/3))*.71**.4
    return max(.0257*Nu/D,minimum_h)

def balance(R,tc,k,finish="MLCCAg",n=128,legacy=False,
            diameter_factor=2,minimum_h=0):
    x,w=quad(n,legacy);tc=np.atleast_1d(tc);U=(k/tc)[:,None]
    h=coefficient(R,diameter_factor,minimum_h)
    opt=FOLD["finishes"][finish];eo=opt["epsilon"];ei=.2
    outputs=[];errors=[]
    for day,sky in [(True,275),(False,260)]:
        irradiation=(.5*(1+x)*sky**4+.5*(1-x)*T0**4)[None,:]
        solar=(opt["alpha"]*970*np.maximum(x,0) if day else np.zeros(n))[None,:]
        outer=np.full((len(tc),n),T0);inner=outer.copy()
        for iteration in range(200):
            avg=(inner**4)@w/2
            f=h*(outer-T0)+eo*SIGMA*(outer**4-irradiation)+U*(outer-inner)-solar
            g=U*(inner-outer)+ei*SIGMA*(inner**4-avg[:,None])
            a=h+4*eo*SIGMA*outer**3+U
            d=U+4*ei*SIGMA*inner**3
            det=a*d-U*U
            # Rank-one correction for the common enclosure irradiation.
            delta_o=(-d*f-U*g)/det
            delta_i=(-U*f-a*g)/det
            b=4*ei*SIGMA*inner**3*w[None,:]/2
            resp_i=a/det
            correction=(b*delta_i).sum(axis=1)/(1-(b*resp_i).sum(axis=1))
            delta_o+=U/det*correction[:,None]
            delta_i+=resp_i*correction[:,None]
            outer+=delta_o;inner+=delta_i
            if max(np.max(abs(delta_o)),np.max(abs(delta_i)))<2e-11:break
        mean=(inner**4)@w/2
        residual=max(np.max(abs(h*(outer-T0)+eo*SIGMA*(outer**4-irradiation)+U*(outer-inner)-solar)),
                     np.max(abs(U*(inner-outer)+ei*SIGMA*(inner**4-mean[:,None]))))
        errors.append(float(residual))
        temperature=(outer+inner)/2
        if not legacy:temperature-=((temperature@w)/2)[:,None]
        # Analytic meridional second derivative, evaluated including both poles.
        axis=np.linspace(-1,1,2001)
        curv=np.zeros((len(tc),len(axis)))
        for degree in range(2,7):
            poly=Legendre.basis(degree)
            coeff=(2*degree+1)/2*(temperature@(w*poly(x)))
            term=(1-axis**2)*poly.deriv(2)(axis)-axis*poly.deriv(1)(axis)
            curv+=coeff[:,None]*term
        outputs.append(dict(gradient=np.max(abs(outer-inner),axis=1),
                            curvature=np.max(abs(curv),axis=1),
                            tmax=np.max(outer,axis=1),tmin=np.min(outer,axis=1)))
    d,ni=outputs
    return dict(tc_m=tc,day_gradient_K=d["gradient"],night_gradient_K=ni["gradient"],
                day_curvature_temperature_K=d["curvature"],night_curvature_temperature_K=ni["curvature"],
                gradient_K=np.maximum(d["gradient"],ni["gradient"]),
                curvature_temperature_K=np.maximum(d["curvature"],ni["curvature"]),
                max_outer_K=np.maximum(d["tmax"],ni["tmax"]),min_outer_K=np.minimum(d["tmin"],ni["tmin"]),
                rise_K=d["tmax"]-T0,swing_K=d["tmax"]-ni["tmin"],
                h_W_m2K=h,max_residual_W_m2=max(errors))

def js(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(str(type(x)))

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--tables",action="store_true");a=p.parse_args()
    if not a.tables:
        trials=[]
        for fac,minimum in [(2,0),(1,0),(2,2),(2,2.5),(2,3)]:
            for legacy in [False,True]:
                t=balance(10,[.02210679007353296],130*16.018463373960138/(2640 if legacy else 2700),
                          finish="reference040",n=37 if legacy else 128,legacy=legacy,
                          diameter_factor=fac,minimum_h=minimum)
                trials.append(dict(diameter_factor=fac,minimum_h=minimum,legacy=legacy,**t))
        (ROOT/"THERMAL-TRIALS.json").write_text(json.dumps(trials,default=js,indent=2)+"\n")
        for t in trials:print(t["diameter_factor"],t["minimum_h"],t["legacy"],t["h_W_m2K"],
              float(t["max_outer_K"][0]),float(t["min_outer_K"][0]),float(t["gradient_K"][0]))
    else:
        tables={}
        for core in COMP["cores"]:
            c=next(props(k) for k,v in CONS.items() if v["core"]==core)
            for finish in ["reference040","MLCCAg","CCAg"]:
                for R in [10,15,20,30]:
                    print(core,finish,R,flush=True)
                    tc=np.geomspace(.001*R/10,1.5*R/10,241)
                    tables[f"{core}|{finish}|{R}"]=balance(R,tc,c["k"],finish)
        (ROOT/"THERMAL-INDEPENDENT-TABLES.json").write_text(json.dumps(tables,default=js)+"\n")
