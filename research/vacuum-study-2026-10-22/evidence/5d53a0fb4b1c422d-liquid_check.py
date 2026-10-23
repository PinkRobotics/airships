"""Independent CHECK-059 equations, written from the declared JSON methods."""
from pathlib import Path
import json, math
import numpy as np

ROOT=Path(__file__).resolve().parent
SIGMA=5.670374419e-8
RHO=1000.; G=9.81; GAMMA=.072; MU=.001
DRY=json.loads((ROOT/'owner/DRY.json').read_text())
RET=json.loads((ROOT/'owner/RETAIN.json').read_text())
COMP=[]
def dump(name,x):
    (ROOT/name).write_text(json.dumps(x,indent=2,default=lambda z:z.tolist() if isinstance(z,np.ndarray) else z.item())+'\n')
def compare(path,own,owner,rtol=1e-6,atol=1e-8,kind='arithmetic'):
    a,b=float(own),float(owner)
    COMP.append(dict(path=path,own=a,owner=b,delta=a-b,relative=(a-b)/b if b else None,
                     tolerance=atol+rtol*abs(b),passed=bool(abs(a-b)<=atol+rtol*abs(b)),kind=kind))
def psat(t):
    c=t-273.15
    return 610.94*np.exp(17.625*c/(243.04+c))
def flux(R,finish,cond,beta,phi,mode='sphere040',rho_air=1.2,cp=1005.,rv=461.5):
    a,e=DRY['finish_optics'][finish]
    c=DRY['conditions'][cond]
    ta,td,sky,u,sun=c['Ta'],c['Td'],c['Tsky'],c['U'],c['G']
    cb,sb=np.cos(beta),np.sin(beta)
    elevation=np.deg2rad(c['sun_el'] or 0)
    cosine=np.maximum(cb*np.sin(elevation)+sb*np.cos(elevation)*np.cos(phi),0)
    absorbed=a*sun*cosine+e*SIGMA*((1+cb)/2*sky**4+(1-cb)/2*ta**4)
    re=rho_air*u*2*R/1.79e-5
    hf=.0257/(2*R)*(2+(.4*np.sqrt(re)+.06*re**(2/3))*.71**.4)
    va=psat(td)/(rv*ta)
    def terms(t):
        h=np.maximum(hf,1.32*np.maximum(abs(t-ta),.05)**.25) if mode=='sphere040' else 5.7+3.8*u
        evap=h/(rho_air*cp*.845**(2/3))*(psat(t)/(rv*t)-va)
        energy=absorbed-e*SIGMA*t**4+h*(ta-t)-2.45e6*evap
        return energy,evap,h
    lo=np.full(np.broadcast_shapes(np.shape(beta),np.shape(phi)),220.)
    hi=np.full_like(lo,360.)
    for _ in range(55):
        t=(lo+hi)/2
        f,_,_=terms(t)
        lo=np.where(f>0,t,lo);hi=np.where(f>0,hi,t)
    t=(lo+hi)/2;err,ev,h=terms(t)
    return ev*3600,t,err,h

def cap_geometry(adv,rec,beta):
    theta=np.deg2rad((adv+rec)/2)
    # V = pi*a^3/6 * tan(theta/2)*(3+tan(theta/2)^2)
    q=math.tan(theta/2)
    vol_factor=math.pi*q*(3+q*q)/6
    force=2*GAMMA*(math.cos(math.radians(rec))-math.cos(math.radians(adv)))
    ac=np.sqrt(force/(RHO*G*vol_factor*np.maximum(np.sin(beta),1e-12)))
    projected_radius=ac if theta<=math.pi/2 else ac/math.sin(theta)
    heff=vol_factor*ac**3/(math.pi*projected_radius**2)
    return ac,heff
AC,HEFF=cap_geometry(78,48,math.pi/2)
KAPPA=.054/(RHO*HEFF)

def retained(finish,R,beta,night=None,wait=600):
    f=RET['finishes'][finish]
    ac,heff=cap_geometry(f['thA'],f['thR'],beta)
    drops=np.minimum(.8,KAPPA*RHO*heff)
    hydrophilic=f['thR']<=15
    if night:
        # All RETAIN profiles share the .8-emittance mirror night, inferred
        # from their identical deposited-water fields, independently solved.
        grid=np.deg2rad(np.arange(2.5,180,5))
        coarse,*_=flux(R,'MLCCAg',night,grid,0,mode='sphere040')
        dep=np.interp(beta,grid,np.maximum(-12*coarse,0))
        film=RHO*np.cbrt(3*MU*(dep/12/3600)*R*beta/(RHO**2*G*np.maximum(np.sin(beta),1e-12)))
        store=np.maximum(drops,np.where((beta<np.pi/2)&hydrophilic,film,0))
        return np.minimum(dep,store),dep
    film=RHO*np.sqrt(MU*R*beta/(RHO*G*np.maximum(np.sin(beta),1e-12)*wait))
    store=np.maximum(drops,np.where((beta<np.pi/2)&hydrophilic,film,0))
    return np.where(beta<3*np.pi/4,np.minimum(store,.8),0)

def main():
    compare('RETAIN/kappa',KAPPA,RET['kappa'])
    compare('RETAIN/acrylic_critical_base_radius_m',AC,RET['acrylic_critical_base_radius_m'])
    out={}
    for key,owner in DRY['results'].items():
        r,mode,finish,cond=key.split('|');R=int(r[1:])
        beta=np.deg2rad(np.arange(2.5,180,5))[:,None]
        phi=np.deg2rad(np.arange(2.5,360,5))[None,:]
        rate,temp,err,_=flux(R,finish,cond,beta,phi,mode)
        weight=np.sin(beta);weight=weight/weight.sum()
        mean=float(np.sum(rate.mean(axis=1,keepdims=True)*weight))
        own=dict(mean_rate_kg_m2_h=mean,hull_rate_kg_h=mean*4*np.pi*R**2*float(np.sin(beta).sum()*np.deg2rad(5)/2),
                 min_rate_kg_m2_h=float(rate.min()),max_rate_kg_m2_h=float(rate.max()),
                 T_min_K=float(temp.min()),T_max_K=float(temp.max()),
                 rate_by_polar_deg={str(float(x)):float(y) for x,y in zip(np.arange(2.5,180,5),rate.mean(axis=1))},
                 max_energy_residual_W_m2=float(np.max(abs(err))))
        for k,v in own.items():
            if k=='rate_by_polar_deg':
                for x,y in v.items():compare(f'DRY/{key}/{k}/{x}',y,owner[k][x])
            elif k in owner:compare(f'DRY/{key}/{k}',v,owner[k])
        out[key]=own
    dump('DRY-INDEPENDENT.json',out)
    beta=np.deg2rad(np.arange(.25,180,.5));weights=np.sin(beta)*np.deg2rad(.5)/2
    rain={};dew={}
    for key,owner in RET['rain'].items():
        finish,r,wait=key.split('|');R=int(r[1:]);sec=int(wait[4:-1])
        values=retained(finish,R,beta,wait=sec)
        mean=float(values@weights)
        own=dict(mean_kg_m2=mean,total_kg=mean*4*np.pi*R**2,
                 profile_deg_kg_m2={str(float(x)):float(v) for x,v in zip(np.arange(.25,180,.5)[::10],values[::10])})
        for k,v in own.items():
            if isinstance(v,dict):
                for x,y in v.items():compare(f'RETAIN/rain/{key}/{k}/{x}',y,owner[k][x])
            else:compare(f'RETAIN/rain/{key}/{k}',v,owner[k])
        rain[key]=own
    for key,owner in RET['dew'].items():
        finish,r,night=key.split('|');R=int(r[1:])
        values,dep=retained(finish,R,beta,night=night)
        mean=float(values@weights);dm=float(dep@weights)
        own=dict(retained_mean_kg_m2=mean,retained_kg=mean*4*np.pi*R**2,
                 deposited_mean_kg_m2=dm,deposited_kg=dm*4*np.pi*R**2,
                 profile_deg_kg_m2={str(float(x)):float(v) for x,v in zip(np.arange(.25,180,.5)[::10],values[::10])})
        for k,v in own.items():
            if isinstance(v,dict):
                for x,y in v.items():compare(f'RETAIN/dew/{key}/{k}/{x}',y,owner[k][x])
            else:compare(f'RETAIN/dew/{key}/{k}',v,owner[k])
        dew[key]=own
    dump('RETAIN-INDEPENDENT.json',dict(kappa=KAPPA,acrylic_base_radius_m=AC,rain=rain,dew=dew))
    dump('LIQUID-COMPARISONS.json',COMP)
    failed=[r for r in COMP if not r['passed']]
    dump('LIQUID-SUMMARY.json',dict(comparisons=len(COMP),failed=len(failed),first_failures=failed[:20]))
    print(json.dumps(dict(comparisons=len(COMP),failed=len(failed),first_failures=failed[:8]),indent=2))
if __name__=='__main__':main()
