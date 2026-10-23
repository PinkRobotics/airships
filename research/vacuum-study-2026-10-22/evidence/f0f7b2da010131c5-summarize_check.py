"""Scientific result aggregation and comparison tables; run only through simjob."""
import csv,json,math,sys
from pathlib import Path
R=Path(__file__).resolve().parent
profiles=['MLCCAg','CCAg','AgFEP05','AgFEP1']
searches=[json.loads((R/f'SEARCH-{x}.json').read_text()) for x in profiles]
allrows=[x for s in searches for x in s['rows']];byid={x['id']:x for x in allrows}
main=json.loads((R/'intake/owner/RESULTS.json').read_text());add=json.loads((R/'intake/addendum048/2-RESULTS.json').read_text())
sourcebyid={x['id']:x for src in [main,add] for x in src['rows']}
comparisons=[x for s in searches for x in s['comparisons']]
bad=[x for s in searches for x in s['mismatches']]
for c in comparisons:
    if not c['agrees'] and c not in bad:bad.append(c)
primary=[]
for radius in [10,12,15]:
 for weather in ['ISA','optimistic','both']:
  for drying in ['dry_gas','bake70','desiccant']:
   for cure in [False,True]:
    identifier=f'MLCCAg-R{radius}-{weather}-floor-{drying}-retained_water'+('-cure_included' if cure else '')
    own=byid[identifier];p=own['endpoints']['11'];sel=own['selected']
    primary.append(dict(id=identifier,R_m=radius,weather=weather,drying=drying,cure_in_global=cure,payload_kg=p['payload_kg'],all_four_payload_kg=own['endpoints']['15']['payload_kg'],least_mask=None if sel is None else sel['mask'],least_usage=None if sel is None else sel['usage']))
one_mm=[]
for own in allrows:
    src=sourcebyid[own['id']]
    if src['two_factor_endpoint']['settings']['external_water_kg_m2']==1:
        one_mm.append(dict(id=own['id'],all_four_payload_kg=own['endpoints']['15']['payload_kg'],float=own['selected'] is not None))
bounds=[x for s in searches for x in s['bounds']]
one_bounds=[x for x in bounds if sourcebyid[x['id']]['two_factor_endpoint']['settings']['external_water_kg_m2']==1]
water_offsets=[]
for rad in [10,12,15]:water_offsets.append(dict(R_m=rad,added_kg=.9*4*math.pi*rad**2))
lost=[];changed=[]
for owner in add['paired_cure_rows']:
    identifier=owner['id'];before=byid[identifier];after=byid[identifier+'-cure_included']
    if before['selected'] is not None and after['selected'] is None:lost.append(identifier)
    if before['minimum_axis_count']!=after['minimum_axis_count']:changed.append(dict(id=identifier,old=before['minimum_axis_count'],new=after['minimum_axis_count']))
extra=json.loads((R/'EXTRA-AUDITS.json').read_text());detail=json.loads((R/'DETAIL-VALIDATION.json').read_text());account=json.loads((R/'ACCOUNT-RESULTS.json').read_text());sup=json.loads((R/'SUPPLEMENTAL-RESULTS.json').read_text())
energy=[]
for row in sup['drying']:
    if row['id'].startswith('MLCCAg-') and '-ISA-floor-' in row['id']:energy.append(row)
max_delta={}
for c in comparisons:
    if c['delta'] is None:continue
    group='payload' if 'payload' in c['field'] else 'usage' if 'usage' in c['field'] else 'discrete'
    if group not in max_delta or abs(c['delta'])>abs(max_delta[group]['delta']):max_delta[group]=c
all_e=[x for s in searches for x in s['E_usage']]
summary=dict(tag='QUESTIONABLE / PROJECTION',checker_complete=True,installed_hull_SF=None,
 original_configurations=sum(x['source']=='original' for x in allrows),addendum_configurations=sum(x['source']=='addendum' for x in allrows),
 total_configurations=len(allrows),subset_optimizations=16*len(allrows),search_comparisons=len(comparisons),search_mismatches=bad,largest_search_differences=max_delta,
 favorable_E_bounds=len(bounds),bound_exclusion_failures=[x for x in bounds if not x['excludes_float']],E_usage_cases=len(all_e),max_E_usage_improvement_kg=max(x['improvement_over_common_kg'] for x in all_e),
 primary=primary,one_mm_configurations=len(one_mm),one_mm_float_count=sum(x['float'] for x in one_mm),best_one_mm=max(one_mm,key=lambda x:x['all_four_payload_kg']),
 best_one_mm_bound=max(one_bounds,key=lambda x:x['independent']['payload_kg']),water_offsets=water_offsets,lost_float_configurations=lost,changed_axis_counts=changed,
 account=dict(points=account['distinct_points'],comparisons=account['comparison_count'],mismatches=account['mismatch_count'],tighter_comparisons=detail['tight_witness_comparisons'],tighter_mismatches=len(detail['tight_mismatches'])),
 supplemental_comparisons=sup['comparisons'],supplemental_mismatches=len(sup['mismatches']),extra_comparisons=len(extra['comparisons']),extra_mismatches=extra['mismatches'],
 detail_comparisons=len(detail['comparisons']),detail_mismatches=detail['mismatches'],optical_screens=detail['optical_screens'],thermal_convergence_points=len(extra['convergence']),thermal_guard_failures=sum(not x['guard_covers'] for x in extra['convergence']),
 old040_R10=extra['original040_R10'],reconciliation=sup['reconciliation'],drying_primary=energy,SolarWhite=extra['SolarWhite'],null_field_witnesses=json.loads((R/'NULL-SENSITIVITY-WITNESSES.json').read_text())['rows'])
(R/'SUMMARY.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
with (R/'PRIMARY-COMPARISON.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(primary[0]));w.writeheader();w.writerows(primary)
with (R/'SEARCH-COMPARISONS.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(comparisons[0]));w.writeheader();w.writerows(comparisons)
(R/'SEARCH-MISMATCHES.json').write_text(json.dumps(bad,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if isinstance(v,(int,float,bool)) or v is None}))
print(json.dumps(dict(largest_differences=max_delta,best_one_mm=summary['best_one_mm'],best_one_mm_bound=summary['best_one_mm_bound'],lost=lost,changed=changed)))
