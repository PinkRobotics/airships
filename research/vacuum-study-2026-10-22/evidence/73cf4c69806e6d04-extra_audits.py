"""Independent legacy convention, convergence, supplemental searches, old040 and source corrections."""
import csv,json,math,time,sys
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
import numpy as np
from numpy.polynomial import legendre as lg,polynomial as poly
from scipy.optimize import brentq
import thermal_resolved as thermal
import independent_search as search
m=search.m
m.THERMAL=json.loads((R/'INDEPENDENT-THERMAL-TABLES.json').read_text())
supp=json.loads((R/'SUPPLEMENTAL-THERMAL-TABLES.json').read_text())
coatings=json.loads((R/'intake/owner/COATINGS.json').read_text())
byfinish={x['id']:x for x in coatings}
rows=json.loads((R/'intake/owner/RESULTS.json').read_text())['rows']
sens=json.loads((R/'intake/owner/SENSITIVITIES.json').read_text())
old040=json.loads((R/'intake/base040/03/RESULTS.json').read_text())
t0=time.monotonic(); comparisons=[]

def cmp(row,field,old,new,atol=.002,rtol=0):
    okay=(old==new) if old is None or new is None else math.isclose(old,new,rel_tol=rtol,abs_tol=atol)
    comparisons.append(dict(row=row,field=field,owner=old,independent=new,delta=None if old is None or new is None else new-old,agrees=okay,atol=atol,rtol=rtol))

screens=json.loads((R/'intake/owner/THERMAL-SCREEN.json').read_text())
legacy=[]
for old in screens:
    f=byfinish[old['id']]
    if f['alpha'] is None:continue
    tc=old['legacy']['tc_m'][0]
    night=thermal.state(10,[tc],f['alpha'],f['epsilon'],False,legacy=True)
    mu=-1+(np.arange(37)+.5)*2/37
    pattern=(night['outer'][0]+night['inner'][0])/2
    centered=pattern-pattern.mean()
    coeff=np.array([(2*j+1)*np.mean(centered*lg.legval(mu,[0]*j+[1])) for j in range(7)])
    coeff[:2]=0
    p=lg.leg2poly(coeff);d1=poly.polyder(p);d2=poly.polyder(p,2)
    curvature=poly.polysub(poly.polymul([1,0,-1],d2),poly.polymul([0,1],d1))
    curv=float(abs(poly.polyval(np.cos(np.linspace(0,math.pi,1441)),curvature)).max())
    own=thermal.thermal(10,[tc],f['alpha'],f['epsilon'],legacy=True)
    amp=max(own['day_curvature_temperature_K'][0],curv)
    cmp(f['id'],'legacy.centered_night_curvature',old['legacy']['night_curvature_temperature_K'][0],curv,atol=1e-7,rtol=2e-6)
    cmp(f['id'],'legacy.mixed_day_night_curvature',old['legacy']['curvature_temperature_K'][0],amp,atol=1e-7,rtol=2e-6)
    legacy.append(dict(finish=f['id'],night_centered_curvature_K=curv,combined_curvature_K=amp,convention='Legacy day uses raw 37-midpoint projection; legacy night removes the mean. This convention is inferred from non-code tables, not owner code.'))
print(json.dumps(dict(stage='legacy',rows=len(legacy))),flush=True)

optical=[]
geometry=json.loads((R/'intake/base040/inputs/028b/PROPERTY-CHECKS.json').read_text())['full_named_maxima']
geometry=next(x for x in geometry if x['route']=='af015_scarf' and x['material']=='SR200')['point']
lag=(23.6e-6-11.3e-6)*math.sqrt(290e9*geometry['tf_m']*46884349.59354485/geometry['tc_m'])
for old in sens['optical_limits_at_037_geometry']:
    e=old['epsilon']
    def margin(a):
        t=thermal.thermal(10,[geometry['tc_m']],a,e,legacy=True)
        return min(241316.50526089262/(lag*t['rise_K'][0])/1.678,241316.50526089262/(lag*t['swing_K'][0]))-1
    root=brentq(margin,.06,.35,xtol=1e-11)
    cmp('optical_limit',f'alpha_at_epsilon_{e}',old['maximum_alpha_for_day_and_cycle'],root,atol=2e-7)
    optical.append(dict(epsilon=e,maximum_alpha=root))

convergence=[]
for f in ['MLCCAg','CCAg','AgFEP05','AgFEP1']:
    c=byfinish[f]
    for rad in (10,12,15):
        points=[x['two_factor_endpoint'] for x in rows if x['profile']==f and x['R_m']==rad]
        tcs=sorted(set(x['geometry']['tc_m'] for x in points))
        direct=thermal.thermal(rad,tcs,c['alpha'],c['epsilon'],nodes=256)
        tab=m.THERMAL[f][str(rad)]
        for j,tc in enumerate(tcs):
            interp=m.thermal_values(rad,tc,{'finish_id':f})
            ratios={key:direct[key][j]/interp[key] for key in ['gradient_K','curvature_temperature_K']}
            convergence.append(dict(finish=f,R_m=rad,tc_m=tc,ratios=ratios,stress_guard=1.002,guard_covers=bool(max(ratios.values())<=1.002)))
print(json.dumps(dict(stage='thermal_convergence',points=len(convergence))),flush=True)

# Reoptimize each sensitivity endpoint and the complete optical least-set search.
sensitivity=[]
extra=json.loads((R/'intake/owner/ADDITIONAL-AUDIT.json').read_text())['classical_low_emittance_sensitivity']
for i,row in enumerate(sens['rows']+[dict(extra,type='classical_low_emittance',R_m=10)]):
    identifier=f"sensitivity[{i}]-{row['type']}"
    endpoint=row.get('endpoint');radius=row['R_m']
    settings=dict(endpoint['settings'] if endpoint else row['settings'])
    if row['type'] in supp:
        m.THERMAL['_sensitivity']=supp[row['type']]
        settings['finish_id']='_sensitivity'
    end=search.optimize(radius,11,1.,settings)
    cmp(identifier,'endpoint_payload_kg',None if endpoint is None else endpoint['signed_payload_kg'],None if end is None else end['payload_kg'])
    allfour=search.optimize(radius,15,1.,settings)
    if 'all_four_endpoint' in row:
        old=row['all_four_endpoint']
        cmp(identifier,'all_four_payload_kg',None if old is None else old['signed_payload_kg'],None if allfour is None else allfour['payload_kg'])
    candidates=[]
    if 'least' in row:
        endpoints={j:search.optimize(radius,j,1.,settings) for j in range(16)}
        floating=[j for j,v in endpoints.items() if v and v['payload_kg']>=0]
        cardinality=min(map(int.bit_count,floating)) if floating else None
        for mask in floating:
            if mask.bit_count()!=cardinality:continue
            def pay(u):
                p=search.optimize(radius,mask,u,settings)
                return p['payload_kg'] if p else -1e12
            u=0. if pay(0)>=0 else brentq(pay,0,1,xtol=1e-10)
            candidates.append(dict(mask=mask,usage=u))
        best=min(candidates,key=lambda x:(x['usage'],x['mask'])) if candidates else None
        old=row['least']['least'] if row['least'] else None
        cmp(identifier,'least_mask',None if old is None else old['mask'],None if best is None else best['mask'],atol=0)
        cmp(identifier,'least_usage',None if old is None else old['usage'],None if best is None else best['usage'],atol=2e-6)
    sensitivity.append(dict(id=identifier,endpoint=end,all_four=allfour,least_candidates=candidates))
    if i%8==0:print(json.dumps(dict(stage='supplemental_search',done=i+1,elapsed_s=time.monotonic()-t0)),flush=True)

# Independently reproduce the historical 040 table and target calculations.
tab040=json.loads((R/'intake/base040/04/THERMAL-TABLE.json').read_text());ind040={}
for rad,tab in tab040.items():
    if not isinstance(tab,dict) or 'tc_m' not in tab:continue
    own=thermal.thermal(float(rad),tab['tc_m'],.2,.9)
    own['gradient_K']=own['day_gradient_K']; own['curvature_temperature_K']=own['day_curvature_temperature_K']
    ind040[rad]=own
    for field in ['gradient_K','curvature_temperature_K','max_outer_K','min_outer_K','swing_K','rise_K']:
        for j,(a,b) in enumerate(zip(tab[field],own[field])):cmp('040-R'+rad,f'{field}[{j}]',a,b,atol=3e-8,rtol=2e-6)
m.THERMAL['reference040']=ind040
by040={x['id']:x for x in old040['rows']}
oldchecks=[]
targets=json.loads((R/'intake/addendum048/11-CHECK040-REPRODUCTION.json').read_text())
for target in targets:
    row=by040[target['id']]
    settings=dict(row['two_factor_endpoint']['settings'],finish_id='reference040',structural_primer_kg_m2=0,moisture_scale=0,finish_water_kg_m2=0,desiccant=False,cure_in_global=True)
    point=search.optimize(row['R_m'],11 if target['track']=='two_factor' else 15,1.,settings)
    cmp('040-cure-'+target['id'],target['track'],target['reproduced_kg'],point['payload_kg'],atol=.002)
    oldchecks.append(dict(id=target['id'],track=target['track'],owner_kg=target['reproduced_kg'],independent=point))
row=by040['R10-ISA-floor-heavy70-vented'];settings=dict(row['two_factor_endpoint']['settings'],finish_id='reference040',structural_primer_kg_m2=0,moisture_scale=0,finish_water_kg_m2=0,desiccant=False)
base=search.optimize(10,11,1.,settings)
cmp('040-R10-original','payload_kg',-109.64920782047648,base['payload_kg'])

# The newly located primary SolarWhite sheet supplies mass previously marked missing.
solar=[]
for rad in (10,12,15):
    template=next(x for x in rows if x['profile']=='MLCCAg' and x['R_m']==rad and x['weather']=='ISA' and x['floor'] and x['drying']=='bake70' and x['two_factor_endpoint']['settings']['external_water_kg_m2']==.1)
    settings=dict(template['two_factor_endpoint']['settings'],finish_id='SolarWhite',coating=.285,finish_water_kg_m2=.00285)
    solar.append(dict(R_m=rad,coating_mass_kg=.285*4*math.pi*rad**2,point=search.optimize(rad,11,1.,settings),scope='Typical 150um Al2024-T3 product mass; no allowance for extra Be preparation. Water fraction is retained 1% scenario.'))
bad=[x for x in comparisons if not x['agrees']]
result=dict(comparisons=comparisons,mismatches=bad,legacy=legacy,optical_limits=optical,convergence=convergence,sensitivities=sensitivity,old040_checks=oldchecks,original040_R10=base,SolarWhite=solar,elapsed_s=time.monotonic()-t0)
(R/'EXTRA-AUDITS.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(comparisons=len(comparisons),mismatches=len(bad),first=bad[:8],convergence_failures=sum(not x['guard_covers'] for x in convergence),elapsed_s=time.monotonic()-t0)),flush=True)
