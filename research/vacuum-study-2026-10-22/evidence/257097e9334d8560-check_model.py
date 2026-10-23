#!/usr/bin/env python3
"""CHECK050 equations written from noncode inputs; no upstream module imports."""
from pathlib import Path
from functools import lru_cache
import json
import math
import numpy as np
from numpy.polynomial.legendre import leggauss, Legendre
from scipy.optimize import minimize_scalar, brentq

B = Path(__file__).resolve().parent
MATERIAL = json.loads((B/"inputs/040/INPUTS.json").read_text())
CASE = json.loads((B/"owner-data/INPUTS.json").read_text())
SIGMA = 5.670374419e-8
TA_REF = 284.9
RHO_REF = 1.1672683307461802
P_REF = 95460.83791390515
LIFT_REF = 4889.442150186961
RD, RV, GRAV, LAPSE = 287.053, 461.5, 9.80665, .0065
NU = .0768
RHO_FACE = 1850.
RHO_CORE = 16.018463373960138
GC = 46884349.59354485
EC = 103421359.3975254
CRUSH = 241316.50526089262
CELL = .009525
ALPHA_BE, ALPHA_AL = 11.3e-6, 23.6e-6
E_FOIL = 67e9
K_BIAX = .5*E_FOIL*RHO_CORE/2700
SCARF = 30.34139731914874
W_MIN = 25*6894.757293168
WALL_YIELD = 227.53e6
T_CURE = (200-32)*5/9+273.15
GUARD = 1.002
BETA = float(np.cbrt(.5+np.sqrt(.25+1/27))+np.cbrt(.5-np.sqrt(.25+1/27)))
WIND70 = .5*RHO_REF*(70*.514444)**2
WIND35_GUST = .5*RHO_REF*(35*.514444+35*.3048)**2


def read(name):
    return json.loads((B/name).read_text())


def finite(value):
    if isinstance(value, dict):
        return {k:finite(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)):
        return [finite(x) for x in value]
    if isinstance(value, np.ndarray):
        return finite(value.tolist())
    if isinstance(value, (np.floating,float)):
        return float(value) if math.isfinite(value) else None
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def save(name, value):
    (B/name).write_text(json.dumps(finite(value),indent=2,allow_nan=False)+"\n")


def es_water(T):
    c=np.asarray(T)-273.15
    return 611.21*np.exp((18.678-c/234.5)*c/(257.14+c))


def es_ice(T):
    c=np.asarray(T)-273.15
    return 611.15*np.exp((23.036-c/333.7)*c/(279.82+c))


def atmosphere(z, offset, anomaly, rh):
    """Solve log(p/ps)=A(1-.378e/p) by Newton, not fixed iteration."""
    z,offset,anomaly,rh=np.broadcast_arrays(z,offset,anomaly,rh)
    temp=288.15-LAPSE*z+offset
    surface_temp=288.15+offset
    surface_p=101325+100*anomaly
    vapor=rh*es_water(temp)
    a=GRAV/(RD*LAPSE)*np.log(temp/surface_temp)
    logratio=a.copy()
    for _ in range(30):
        p=surface_p*np.exp(logratio)
        residual=logratio-a*(1-.378*vapor/p)
        change=residual/(1-a*.378*vapor/p)
        logratio-=change
        if np.max(abs(change))<2e-15:
            break
    p=surface_p*np.exp(logratio)
    rho=(p-.378*vapor)/(RD*temp)
    return temp,p,vapor,rho


def load_pressure(p):
    return np.maximum(1.01*P_REF,p)+max(WIND70,WIND35_GUST)


def convection(R, temperature, air=TA_REF, wind=2., multiplier=1.):
    re=RHO_REF*wind*(2*R)/1.79e-5
    forced=(2+(.4*re**.5+.06*re**(2/3))*.71**.4)*.0257/(2*R)
    delta=np.asarray(temperature)-air
    natural=1.32*np.maximum(abs(delta),.05)**.25
    h=np.maximum(forced,natural)*multiplier
    derivative=h+np.where((natural>forced)&(abs(delta)>.05),.25*h,0)
    return h,derivative


@lru_cache(maxsize=8)
def quadrature(n):
    mu,weights=leggauss(n)
    weights=weights/2
    angles=np.linspace(0,np.pi,1441)
    x=np.cos(angles)
    basis=np.stack([Legendre.basis(j)(mu)*(2*j+1) for j in range(2,7)])
    curvature=np.stack([(1-x*x)*Legendre.basis(j).deriv(2)(x)-
                        x*Legendre.basis(j).deriv()(x) for j in range(2,7)])
    return mu,weights,basis,curvature


def thermal_zones(R, cores, air, solar, sky, n=128, eps=.8, alpha=.09):
    """Simultaneous Newton with exact rank-two enclosure Jacobian."""
    cores=np.atleast_1d(cores).astype(float)
    mu,w,_,_=quadrature(n)
    ti=np.full((len(cores),n),air)
    env4=(1+mu)*.5*sky**4+(1-mu)*.5*air**4
    absorbed=alpha*solar*np.maximum(mu,0)
    gap=4*.2*SIGMA
    for iteration in range(60):
        mean=np.sum(ti*w,axis=1,keepdims=True)
        mean4=np.sum(ti**4*w,axis=1,keepdims=True)
        u=130*RHO_CORE/2700/cores[:,None]+gap*mean**3
        q=.2*SIGMA*(ti**4-mean4)
        c=4*.2*SIGMA*ti**3
        to=ti+q/u
        h,h_derivative=convection(R,to,air)
        residual=eps*SIGMA*(to**4-env4)+h*(to-air)+q-absorbed
        aa=4*eps*SIGMA*to**3+h_derivative
        diagonal=aa*(1+c/u)+c
        first=aa/u+1
        second=aa*q/u**2*(3*gap*mean**2)
        vv=c*w
        x0=first/diagonal
        x1=second/diagonal
        rhs=residual/diagonal
        a00=1-np.sum(vv*x0,axis=1)
        a01=-np.sum(vv*x1,axis=1)
        a10=-np.sum(w*x0,axis=1)
        a11=1-np.sum(w*x1,axis=1)
        r0=np.sum(vv*rhs,axis=1)
        r1=np.sum(w*rhs,axis=1)
        det=a00*a11-a01*a10
        z0=(r0*a11-a01*r1)/det
        z1=(a00*r1-r0*a10)/det
        change=rhs+x0*z0[:,None]+x1*z1[:,None]
        # Damping is a solver safeguard, not a material/model parameter.
        step=np.minimum(1,20/np.maximum(np.max(abs(change),axis=1),1e-30))
        ti-=change*step[:,None]
        if np.max(abs(change))<2e-11:
            break
    else:
        raise ArithmeticError(("thermal Newton convergence",R,air,np.max(abs(change))))
    mean=np.sum(ti*w,axis=1,keepdims=True)
    mean4=np.sum(ti**4*w,axis=1,keepdims=True)
    u=130*RHO_CORE/2700/cores[:,None]+gap*mean**3
    q=.2*SIGMA*(ti**4-mean4)
    to=ti+q/u
    h,_=convection(R,to,air)
    residual=eps*SIGMA*(to**4-env4)+h*(to-air)+q-absorbed
    return to,ti,dict(iterations=iteration+1,max_residual_W_m2=float(np.max(abs(residual))))


def thermal(R, cores, air=TA_REF, n=128):
    cores=np.atleast_1d(cores).astype(float)
    _,w,basis,curvature=quadrature(n)
    day,di,dd=thermal_zones(R,cores,air,970,air-9.9,n)
    night,ni,nd=thermal_zones(R,cores,air,0,air-24.9,n)
    amplitudes=[]
    for outer,inner in ((day,di),(night,ni)):
        pattern=(outer+inner)/2
        pattern-=np.sum(pattern*w,axis=1,keepdims=True)
        coeff=(pattern*w)@basis.T
        amplitudes.append(np.max(abs(coeff@curvature),axis=1))
    return dict(tc_m=cores,gradient_K=np.maximum(np.max(abs(day-di),axis=1),
                    np.max(abs(night-ni),axis=1)),
        curvature_temperature_K=np.maximum(*amplitudes),
        max_outer_K=np.max(day,axis=1),min_outer_K=np.min(night,axis=1),
        swing_K=np.max(day,axis=1)-np.min(night,axis=1),
        day_diagnostics=dd,night_diagnostics=nd)


@lru_cache(maxsize=256)
def thermal_table(R, air=TA_REF, n=128):
    return thermal(R,np.geomspace(.001*R/10,1.5*R/10,241),air,n)


def interpolated_thermal(R, cores, air=TA_REF):
    table=thermal_table(float(R),float(air))
    return {k:np.interp(np.log(cores),np.log(table["tc_m"]),table[k])
            for k in ("gradient_K","curvature_temperature_K","max_outer_K","min_outer_K")}


def material(mask, usage=1.):
    e=290e9*(293.6/290)**(usage if mask&4 else 0)
    f=345e6*(379.2/345)**(usage if mask&4 else 0)
    q=.33*(.82/.33)**(usage if mask&2 else 0)
    film=.1464728290914915*(.5)**(usage if mask&8 else 0)
    return e,f,q,film


def modes(R, tf, tc, pressure, mask=11, usage=1., air=TA_REF, temperature=None):
    tf,tc,pressure=np.broadcast_arrays(tf,tc,pressure)
    t=temperature if temperature is not None else interpolated_thermal(R,tc,air)
    e,f,q,film=material(mask,usage)
    separation=tf+tc
    pressure_stress=pressure*R/(4*tf)
    sigma0=e*separation/(R*np.sqrt(1-NU**2))
    crimp=GC*separation**2/(2*tf*tc)
    vc=sigma0/crimp
    baseline=np.where(vc<2,.2,1.)
    full=.2+.4*np.minimum(vc,2)
    gamma=baseline*(full/baseline)**(usage if mask&1 else 0)
    kc=np.where(vc<=2,1-vc/4,1/vc)
    grad=e*ALPHA_BE*GUARD*t["gradient_K"]/(2*(1-NU))
    bend=e*separation/(2*(1-NU**2))*ALPHA_BE*GUARD*t["curvature_temperature_K"]/R
    excursion=np.maximum(abs(T_CURE-t["min_outer_K"]),abs(T_CURE-t["max_outer_K"]))
    mismatch=GUARD*abs(ALPHA_AL-ALPHA_BE)*excursion
    cure=K_BIAX*(ALPHA_AL-ALPHA_BE)*GUARD*np.maximum(T_CURE-t["min_outer_K"],0)*tc/(2*tf)
    total=pressure_stress+grad+bend
    demand=total+cure
    edge=mismatch*np.sqrt(2*K_BIAX*GC)
    wall=1.2*E_FOIL*mismatch
    return dict(global_buckling=gamma*kc*sigma0/pressure_stress,
        face_compression=f/demand,core_shear_crimping=crimp/total,
        core_crush=np.broadcast_to(2*CRUSH/pressure,tf.shape),
        face_wrinkling=BETA*q*np.sqrt(e*EC*tf/tc)/demand,
        intracell_dimpling=e*(tf/CELL)**2/((1-NU**2)*demand),
        scarf_average_shear_screen=1e7/(demand*SCARF/(1+SCARF**2)),
        core_cell_wall_yield_screen=WALL_YIELD/wall,
        thermal_core_interface_screen=W_MIN/edge)


def pad(R):
    force=.47*WIND70*np.pi*R**2
    area=force/CRUSH
    radius=np.sqrt(area/np.pi)
    thick=np.sqrt(3*(1+.33)*force*np.log(radius/.025)/(2*np.pi*276e6))
    return dict(force_N=force,area_m2=area,radius_m=radius,thickness_m=thick,
                mass_kg=area*thick*2700)


def bill(R, tf, tc, mask=11, usage=1.):
    area=4*np.pi*R**2
    e,f,q,film=material(mask,usage)
    seam=area*(1/(.6096-SCARF*tf)+1/(1.8288-SCARF*tf))
    faces=2*area*RHO_FACE*tf
    core=area*RHO_CORE*tc
    adhesive=2*area*film
    scarf=seam*2*tf*np.sqrt(1+SCARF**2)*.07
    splice=seam*.0005*tc*500
    seal=seam*.002
    finish=area*.00833272
    primer=area*.01
    addedwater=.1*(.002*adhesive+.001*core+.01*primer+.01*finish+.01*(scarf+splice+seal))
    return dict(faces=faces,core=core,charged_joining=np.maximum(adhesive+scarf+splice+seal,.05*(faces+core)),
        coating=finish,mooring_pad=pad(R)["mass_kg"],gas=.01*LIFT_REF*(R/10)**3,systems=100.,
        water=.1*area,contamination=5*(R/10)**2,absorbed_water=addedwater,structural_primer=primer)


def evaluate(R, tf, tc, pressure, mask=11, usage=1., air=TA_REF):
    mm=modes(R,tf,tc,pressure,mask,usage,air)
    bb=bill(R,tf,tc,mask,usage)
    return dict(R_m=R,tf_m=float(tf),tc_m=float(tc),pressure_Pa=pressure,
        mask=mask,usage=usage,air_K=air,modes=mm,minimum_SF=min(float(x) for x in mm.values()),
        bill_kg=bb,mass_kg=sum(float(x) for x in bb.values()),pad=pad(R),
        qualified_installed_hull_SF=None,tag="QUESTIONABLE / PROJECTION")


def face_for_core(R, cores, pressure, mask=11, usage=1., air=TA_REF):
    cores=np.atleast_1d(cores)
    tt=interpolated_thermal(R,cores,air)
    low=np.full_like(cores,1e-8);high=np.full_like(cores,min(.0195,.008*R/10))
    excursion=np.maximum(abs(T_CURE-tt["min_outer_K"]),abs(T_CURE-tt["max_outer_K"]))
    strain=GUARD*abs(ALPHA_AL-ALPHA_BE)*excursion
    interface_ok=(strain*np.sqrt(2*K_BIAX*GC)<=W_MIN*(1+1e-9))&(
        1.2*E_FOIL*strain<=WALL_YIELD*(1+1e-9))
    if not np.any(interface_ok):
        return high,np.full_like(cores,np.inf)
    for _ in range(46):
        mid=(low+high)/2
        mm=modes(R,mid,cores,pressure,mask,usage,air,tt)
        # The edge and ribbon criteria are independent of the face thickness.
        keys=("global_buckling","face_compression","core_shear_crimping","core_crush",
              "face_wrinkling","intracell_dimpling","scarf_average_shear_screen")
        ok=np.minimum.reduce([mm[k] for k in keys])>=1
        high=np.where(ok,mid,high);low=np.where(ok,low,mid)
    mm=modes(R,high,cores,pressure,mask,usage,air,tt)
    feasible=np.minimum.reduce([np.broadcast_to(v,cores.shape) for v in mm.values()])>=1-1e-9
    mass=sum(bill(R,high,cores,mask,usage).values())
    mass=np.where(feasible,mass,np.inf)
    return high,mass


def optimize(R, pressure, mask=11, usage=1., air=TA_REF, points=800):
    grid=np.geomspace(.0005*R/10,2*R/10,points)
    faces,masses=face_for_core(R,grid,pressure,mask,usage,air)
    if not np.any(np.isfinite(masses)):
        return None
    best=int(np.argmin(masses));candidates=[(masses[best],grid[best])]
    local=np.flatnonzero((masses[1:-1]<=masses[:-2])&(masses[1:-1]<=masses[2:])&
                        np.isfinite(masses[1:-1]))+1
    for i in local:
        def objective(logcore):
            return float(face_for_core(R,[np.exp(logcore)],pressure,mask,usage,air)[1][0])
        result=minimize_scalar(objective,bounds=(np.log(grid[i-1]),np.log(grid[i+1])),
                               method="bounded",options={"xatol":2e-11})
        if math.isfinite(result.fun):candidates.append((result.fun,np.exp(result.x)))
    _,core=min(candidates)
    face=float(face_for_core(R,[core],pressure,mask,usage,air)[0][0])
    return evaluate(R,face,core,pressure,mask,usage,air)
