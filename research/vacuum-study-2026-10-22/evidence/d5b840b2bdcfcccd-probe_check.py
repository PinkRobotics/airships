from liquid_check import *
from scipy.optimize import least_squares
beta=np.deg2rad(np.arange(2.5,180,5))[:,None]
phi=np.deg2rad(np.arange(0,360,15))[None,:]
for rho in [1.16726833074618,1.2,1.225]:
    r,t,_,_=flux(10,'paint_040','night_050_reference',beta,phi,rho_air=rho)
    print('rho',rho,'rate',r[0,0],r[-1,0],'T',t[0,0],t[-1,0])
for typ in ['rain','dew']:
    failures=[r for r in json.loads((ROOT/'LIQUID-COMPARISONS.json').read_text()) if not r['passed'] and r['path'].startswith('RETAIN/'+typ)]
    print(typ,'failed',len(failures),'first',failures[:3])
print('mode keys',list(dict.fromkeys(k.split('|')[1] for k in DRY['results'])))
for n in [12,24,36,48,72]:
    for phase in [0.,.5]:
        pp=((np.arange(n)+phase)*2*np.pi/n)[None,:]
        rate,t,*_=flux(10,'paint_040','morning_fair',beta,pp)
        print('azimuth',n,phase,'max',rate.max(),'mean',np.average(rate.mean(axis=1),weights=np.sin(beta[:,0])))
print('RETAIN one',RET['dew']['MLCCAg|R10|night_050_reference']['retained_mean_kg_m2'])
