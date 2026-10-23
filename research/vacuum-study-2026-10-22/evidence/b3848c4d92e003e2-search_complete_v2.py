"""Independent full subset/least-usage search and favorable-E exclusion checks."""
import json,math,time,sys
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
import numpy as np
from scipy.optimize import brentq,minimize_scalar
import independent_search as search
m=search.m
m.THERMAL=json.loads((R/'INDEPENDENT-THERMAL-TABLES.json').read_text())
profile=sys.argv[1]
t0=time.monotonic()
original=json.loads((R/'intake/owner/RESULTS.json').read_text())
addendum=json.loads((R/'intake/addendum048/2-RESULTS.json').read_text())
bounds=json.loads((R/'intake/owner/SUBSET-BOUNDS.json').read_text())+addendum['exclusion_bounds']
checks=[]
comparisons=[]
cache={}

def optimized(radius,mask,usage,settings,n=901):
    key=json.dumps([radius,mask,usage,settings,n],sort_keys=True)
    if key not in cache:cache[key]=search.optimize(radius,mask,usage,settings,n=n)
    return cache[key]

def cmp(row,field,old,new,tol):
    okay=(old==new) if old is None or new is None else abs(new-old)<=tol
    comparisons.append(dict(row=row,field=field,owner=old,independent=new,delta=None if old is None or new is None else new-old,agrees=okay,absolute_tolerance=tol))

rows=[dict(x,source=source) for source,data in [('original',original),('addendum',addendum)] for x in data['rows'] if x['profile']==profile]
byid={x['id']:x for x in rows}
for i,row in enumerate(rows):
    radius=row['R_m']; settings=row['two_factor_endpoint']['settings']; identifier=row['id']
    endpoints={mask:optimized(radius,mask,1.,settings) for mask in range(16)}
    for trial in row['least']['endpoint_trials']:
        got=endpoints[trial['mask']]
        cmp(identifier,f"subset[{trial['mask']}].payload_kg",trial['payload_kg'],None if got is None else got['payload_kg'],.002)
    e11=endpoints[11]
    cmp(identifier,'named_endpoint_payload_kg',row['two_factor_endpoint']['signed_payload_kg'],None if e11 is None else e11['payload_kg'],.002)
    floating=[mask for mask,v in endpoints.items() if v is not None and v['payload_kg']>=0]
    cardinality=min(map(int.bit_count,floating)) if floating else None
    cmp(identifier,'minimum_axis_count',row['least']['minimum_axis_count'],cardinality,0)
    candidates=[]
    if cardinality is not None:
        for mask in floating:
            if mask.bit_count()!=cardinality:continue
            def fun(u):
                pt=optimized(radius,mask,float(u),settings)
                return pt['payload_kg'] if pt else -1e12
            u=0. if fun(0)>=0 else brentq(fun,0,1,xtol=1e-10)
            candidates.append(dict(mask=mask,usage=u,point=optimized(radius,mask,float(u),settings)))
    chosen=min(candidates,key=lambda x:(x['usage'],x['mask'])) if candidates else None
    old=row['least']['least']
    cmp(identifier,'least_mask',None if old is None else old['mask'],None if chosen is None else chosen['mask'],0)
    cmp(identifier,'least_usage',None if old is None else old['usage'],None if chosen is None else chosen['usage'],2e-6)
    for tie in row['least'].get('ties',[]):
        got=next((x for x in candidates if x['mask']==tie['mask']),None)
        cmp(identifier,f"tie[{tie['mask']}].usage",tie['usage'],None if got is None else got['usage'],2e-6)
    checks.append(dict(id=identifier,source=row['source'],endpoints=endpoints,minimum_axis_count=cardinality,candidates=candidates,selected=chosen))
    if i%12==0:print(json.dumps(dict(profile=profile,stage='subsets',done=i+1,total=len(rows),elapsed_s=time.monotonic()-t0)),flush=True)
    if i%24==0:(R/f'SEARCH-{profile}-PROGRESS.json').write_text(json.dumps(dict(done=i+1,total=len(rows),elapsed_s=time.monotonic()-t0)))

bound_checks=[]
for bound in bounds:
    if bound['id'] not in byid:continue
    row=byid[bound['id']]; settings=dict(row['two_factor_endpoint']['settings'],thermal_modulus_Pa=290e9)
    point=optimized(row['R_m'],bound['mask'],1.,settings)
    value=None if point is None else point['payload_kg']
    cmp(row['id'],f"favorable_E[{bound['mask']}].payload_upper_kg",bound['payload_upper_kg'],value,.002)
    bound_checks.append(dict(id=row['id'],mask=bound['mask'],owner_kg=bound['payload_upper_kg'],independent=point,excludes_float=value is None or value<0))

# Independent E variation at every original selected E-containing least point.
e_checks=[]
for check in checks:
    chosen=check['selected']
    if not chosen or not chosen['mask']&4:continue
    row=byid[check['id']]; ceiling=chosen['usage']; mask=chosen['mask'];settings=row['two_factor_endpoint']['settings']
    def epay(u):
        p=optimized(row['R_m'],mask,[ceiling,ceiling,float(u),ceiling],settings)
        return p['payload_kg'] if p else -1e12
    samples=[dict(E_usage=float(u),payload_kg=epay(u)) for u in np.linspace(0,ceiling,17)]
    opt=minimize_scalar(lambda u:-epay(u),bounds=(0,ceiling),method='bounded',options={'xatol':1e-9})
    samples.append(dict(E_usage=float(opt.x),payload_kg=float(-opt.fun)))
    best=max(samples,key=lambda x:x['payload_kg'])
    e_checks.append(dict(id=check['id'],usage_ceiling=ceiling,samples=samples,best=best,improvement_over_common_kg=best['payload_kg']-chosen['point']['payload_kg']))

bad=[x for x in comparisons if not x['agrees']]
out=dict(profile=profile,scope='Independent thermal tables; 901-point log-core brackets and independently refined extrema; every subset and every smallest-cardinality root. Favorable full-elastic/reduced-thermal E bounds.',rows=checks,bounds=bound_checks,E_usage=e_checks,comparisons=comparisons,mismatches=bad,elapsed_s=time.monotonic()-t0,owner_code_accessed=False)
(R/f'SEARCH-{profile}.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(profile=profile,rows=len(checks),bounds=len(bound_checks),comparisons=len(comparisons),mismatches=len(bad),E_usage_cases=len(e_checks),elapsed_s=time.monotonic()-t0,first_mismatches=bad[:5])),flush=True)
