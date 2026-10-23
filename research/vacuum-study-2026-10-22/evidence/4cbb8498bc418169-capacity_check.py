"""Use this seat's previously independent CHECK-053 mechanics, never owner code."""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'intake/own053'))
import account_check as a
import thermal_check as thermal
from scipy.optimize import brentq
def dump(name,x):
    (ROOT/name).write_text(json.dumps(x,indent=2,default=lambda z:z.tolist() if isinstance(z,np.ndarray) else z.item())+'\n')
def case(R,w,global_cure=True,floor=False):
    return dict(model='owner_table',R_m=R,weather=w,cure_in_global=global_cure,floor=floor,drying='bake')
def main():
    extra={}
    for R in [20,30]:
        answer=thermal.solve(R,np.geomspace(.001*R/10,1.5*R/10,241),'mixed_gap',
                 .09,.8,n=128,scheme='gauss',poles=False,curv='grid')
        a.OLD[str(R)]=answer;extra[str(R)]=answer
    dump('EXTENDED-THERMAL-INDEPENDENT.json',extra)
    owner=json.loads((ROOT/'owner/CAP.json').read_text())['rows']
    modes=[]
    for g in [False,True]:
        for floor in [False,True]:
            fit=a.optimize(case(12,'ISA',g,floor),11,n=801)
            modes.append(dict(global_cure=g,floor=floor,payload_kg=float(fit['payload_kg'])))
    print('conventions',modes,flush=True)
    rows=[];endpoints={}
    for R in [10,12,15,20,30]:
        for w in ['ISA','optimistic']:
            c=case(R,w)
            ends={m:a.optimize(c,m,n=1001) for m in range(16)}
            endpoints[(R,w)]=ends
            row=dict(R=R,weather=w,endpoints={str(m):x for m,x in ends.items()})
            rows.append(row)
            print('capacity',R,w,{m:float(ends[m]['payload_kg']) for m in [0,11,15]},flush=True)
    dump('CAPACITY-ENDPOINTS-INDEPENDENT.json',rows)
    comparisons=[];least=[]
    for j,row in enumerate(owner):
        R,w,water=row['R_m'],row['weather'],row['external_water']
        ends=endpoints[(R,w)];area=4*np.pi*R*R
        for mask,key in [(11,'endpoint_named_kg'),(15,'endpoint_all_kg'),(0,'endpoint_today_kg')]:
            val=float(ends[mask]['payload_kg'])-(water-.1)*area
            comparisons.append(dict(row=j,key=key,own=val,owner=row[key],delta=val-row[key],
                                    passed=abs(val-row[key])<.003))
        for mask,key in [(11,'water_capacity_named_kg_m2'),(15,'water_capacity_all_kg_m2')]:
            val=.1+float(ends[mask]['payload_kg'])/area
            comparisons.append(dict(row=j,key=key,own=val,owner=row[key],delta=val-row[key],
                                    passed=abs(val-row[key])<3e-6))
        feasible=[m for m,e in ends.items() if float(e['payload_kg'])-(water-.1)*area>=-1e-7]
        if not feasible:
            least.append(dict(row=j,least_mask=None,least_usage=None,owner_axes=row['least_axes'],
                              owner_usage=row['least_usage']))
            continue
        fewest=min(m.bit_count() for m in feasible)
        ties=[m for m in feasible if m.bit_count()==fewest]
        roots=[]
        for m in ties:
            def objective(u):
                x=a.optimize(case(R,w),m,u,n=401)
                return -1e30 if x is None else float(x['payload_kg'])-(water-.1)*area
            u=0. if objective(0)>=0 else brentq(objective,0,1,xtol=5e-8)
            roots.append((u,m))
        u,m=min(roots)
        least.append(dict(row=j,least_mask=m,least_usage=u,ties=ties,
            owner_axes=row['least_axes'],owner_usage=row['least_usage'],
            usage_difference=u-row['least_usage'] if row['least_usage'] is not None else None))
    dump('CAPACITY-COMPARISONS.json',comparisons);dump('LEAST-INDEPENDENT.json',least)
    dump('CAPACITY-SUMMARY.json',dict(conventions=modes,comparisons=len(comparisons),
        failed=[x for x in comparisons if not x['passed']],least_rows=len(least)))
    print('finished',len(comparisons),'failed',sum(not x['passed'] for x in comparisons),flush=True)
if __name__=='__main__':main()
