"""Tighter witness comparison audit and exact supplied E/optical supplemental points."""
import csv,gzip,json,math,sys,collections
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
import independent_search as search
import thermal_resolved as thermal
from scipy.optimize import minimize_scalar
m=search.m;m.THERMAL=json.loads((R/'INDEPENDENT-THERMAL-TABLES.json').read_text())
strict_bad=[];largest={};groups=collections.Counter();count=0
with gzip.open(R/'ACCOUNT-COMPARISONS.csv.gz','rt') as f:
    for row in csv.DictReader(f):
        count+=1;field=row['field'];old=float(row['owner']);new=float(row['independent']);delta=new-old
        group=field.split('.')[0];groups[group]+=1
        if group not in largest or abs(delta)>abs(largest[group]['delta']):largest[group]=dict(point=row['point'],field=field,owner=old,independent=new,delta=delta)
        if not math.isclose(old,new,rel_tol=2e-8,abs_tol=2e-8):strict_bad.append(dict(point=row['point'],field=field,owner=old,independent=new,delta=delta))
print(json.dumps(dict(stage='tight_witness_check',comparisons=count,mismatches=len(strict_bad))),flush=True)
main=json.loads((R/'intake/owner/RESULTS.json').read_text());byid={x['id']:x for x in main['rows']}
old=json.loads((R/'intake/owner/ADDITIONAL-AUDIT.json').read_text());checks=[];comparisons=[]
def cmp(row,field,a,b,atol=.002):
    comparisons.append(dict(row=row,field=field,owner=a,independent=b,delta=b-a,agrees=math.isclose(a,b,rel_tol=2e-8,abs_tol=atol),absolute_tolerance=atol))
for check in old['E_axis_checks']:
    row=byid[check['id']];point=row['least']['least'];settings=point['settings'];u=check['usage_ceiling'];mask=point['mask'];rad=row['R_m']
    samples=[]
    for sample in check['samples']:
        p=search.optimize(rad,mask,[u,u,sample['E_usage'],u],settings)
        cmp(check['id'],f"E_usage={sample['E_usage']}",sample['payload_kg'],p['payload_kg'])
        samples.append(dict(E_usage=sample['E_usage'],payload_kg=p['payload_kg']))
    best=max(samples,key=lambda x:x['payload_kg'])
    cmp(check['id'],'best_E_payload_kg',check['best_independent_E']['payload_kg'],best['payload_kg'])
    cmp(check['id'],'improvement_kg',check['improvement_kg'],best['payload_kg']-point['signed_payload_kg'])
    checks.append(dict(id=check['id'],usage_ceiling=u,samples=samples,best=best))
fold=json.loads((R/'intake/addendum048/2-RESULTS.json').read_text());byfold={x['id']:x for x in fold['rows']}
fold_E=[]
for oldE in json.loads((R/'intake/addendum048/13-E-USAGE-VALIDATION.json').read_text()):
    row=byfold[oldE['id']];point=row['least']['least'];u=point['usage'];mask=point['mask'];settings=point['settings'];rad=row['R_m']
    def pay(eu):return search.optimize(rad,mask,[u,u,float(eu),u],settings)['payload_kg']
    opt=minimize_scalar(lambda x:-pay(x),bounds=(0,u),method='bounded',options={'xatol':1e-9})
    best=max(pay(0),pay(u),-opt.fun)
    cmp(oldE['id'],'addendum_E_improvement_kg',oldE['improvement_kg'],best-point['signed_payload_kg'])
    fold_E.append(dict(id=oldE['id'],improvement_kg=best-point['signed_payload_kg']))
geo=next(x for x in json.loads((R/'intake/base040/inputs/028b/PROPERTY-CHECKS.json').read_text())['full_named_maxima'] if x['route']=='af015_scarf' and x['material']=='SR200')['point']
lag=(23.6e-6-11.3e-6)*math.sqrt(290e9*geo['tf_m']*46884349.59354485/geo['tc_m'])
optical=[]
for x in json.loads((R/'intake/owner/OPTICAL-SENSITIVITY-SCREEN.json').read_text()):
    t=thermal.thermal(10,[geo['tc_m']],x['alpha'],x['epsilon'],legacy=True)
    day=241316.50526089262/(lag*t['rise_K'][0]);cycle=241316.50526089262/(lag*t['swing_K'][0])
    cmp(x['id'],'legacy_day_SF',x['legacy_day_SF'],day,atol=1e-7)
    cmp(x['id'],'legacy_cycle_SF',x['legacy_cycle_SF'],cycle,atol=1e-7)
    optical.append(dict(id=x['id'],day_SF=day,cycle_SF=cycle,meets_finish_screen=day>=1.678 and cycle>=1))
out=dict(tight_witness_comparisons=count,tight_rtol=2e-8,tight_atol=2e-8,tight_mismatches=strict_bad,groups=dict(groups),largest_by_group=largest,comparisons=comparisons,mismatches=[x for x in comparisons if not x['agrees']],E_usage=checks,addendum_E=fold_E,optical_screens=optical)
(R/'DETAIL-VALIDATION.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(witness_comparisons=count,tight_mismatches=len(strict_bad),additional_comparisons=len(comparisons),additional_mismatches=len(out['mismatches']))))
