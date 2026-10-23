"""Positive-payload witnesses for null sensitivity least-set fields."""
import json,math,sys
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
import independent_search as search
m=search.m
m.THERMAL=json.loads((R/'INDEPENDENT-THERMAL-TABLES.json').read_text())
supp=json.loads((R/'SUPPLEMENTAL-THERMAL-TABLES.json').read_text())
data=json.loads((R/'intake/owner/SENSITIVITIES.json').read_text())['rows']
extra=json.loads((R/'EXTRA-AUDITS.json').read_text())
results=[]
for comparison in extra['mismatches']:
    if comparison['field']!='least_mask':continue
    index=int(comparison['row'].split('[')[1].split(']')[0]);row=data[index]
    calc=extra['sensitivities'][index]
    candidate=min(calc['least_candidates'],key=lambda x:(x['usage'],x['mask']))
    usage=min(1.,candidate['usage']+1e-5)
    settings=dict(row['endpoint']['settings'],finish_id='_null_optics')
    m.THERMAL['_null_optics']=supp[row['type']]
    point=search.optimize(row['R_m'],candidate['mask'],usage,settings,n=1801)
    full=m.evaluate(row['R_m'],point['tf_m'],point['tc_m'],candidate['mask'],usage,settings)
    assert point['payload_kg']>0 and point['least_SF']>=1-2e-9 and point['pressure_SF']>1
    full['properties']['gamma']=float(full['properties']['gamma'])
    results.append(dict(source_row_index=index,type=row['type'],R_m=row['R_m'],weather=row['weather'],owner_least=None,independent_least_mask=candidate['mask'],independent_common_usage=candidate['usage'],positive_witness_usage=usage,positive_witness=full,settings=settings,grid_points=1801))
def native(x):
    if hasattr(x,'tolist'):return x.tolist()
    if hasattr(x,'item'):return x.item()
    raise TypeError(type(x).__name__)
(R/'NULL-SENSITIVITY-WITNESSES.json').write_text(json.dumps(dict(rows=results,scope='Scalar assembly/pressure constraints only. These are not qualified wet/aged optics or installed-hull floats. The filed null fields should be populated or labeled not searched; a null field does not establish infeasibility.'),indent=2,allow_nan=False,default=native)+'\n')
print(json.dumps(dict(witnesses=len(results),minimum_positive_payload_kg=min(x['positive_witness']['signed_payload_kg'] for x in results))))
