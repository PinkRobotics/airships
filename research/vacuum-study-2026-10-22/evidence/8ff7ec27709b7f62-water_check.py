from liquid_check import *
W=json.loads((ROOT/'owner/WATER.json').read_text())
P=json.loads((ROOT/'owner/PONDS.json').read_text())
def main():
    wet=json.loads((ROOT/'RETAIN-INDEPENDENT.json').read_text())
    dry=json.loads((ROOT/'DRY-INDEPENDENT.json').read_text())
    p3=json.loads((ROOT/'intake/own052/RESULTS.json').read_text())
    print('P3 row schema',p3['rows'][0].keys(),flush=True)
    beta=np.deg2rad(np.arange(.25,180,.5));wt=np.sin(beta)*np.deg2rad(.5)/2
    p3dew=[]
    for row in W['account']:
        R=row['R_m'];A=4*np.pi*R*R;f=row['finish'];path=f"WATER/account/{row['lead']}|R{R}|{row['weather']}|{f}"
        rain=wet['rain'][f'{f}|R{R}|wait600s']['total_kg']
        compare(path+'/allowance_kg',.1*A,row['allowance_kg'])
        compare(path+'/capacity_kg',.1*A+row['endpoint_payload_kg'],row['capacity_kg'])
        compare(path+'/capacity_kg_m2',.1+row['endpoint_payload_kg']/A,row['capacity_kg_m2'])
        if row['lead']=='P3':
            endpoint=next(x for x in p3['rows'] if x['R_m']==R and x['weather']==row['weather'] and x['service']=='ground')['all_axes_endpoint']['payload_kg']
            compare(path+'/endpoint_payload_kg',endpoint,row['endpoint_payload_kg'],rtol=0,atol=.0005)
        compare(path+'/rain_10min_kg',rain,row['rain_10min_kg'])
        compare(path+'/rain_10min_upper_kg',rain*.08/.054,row['rain_10min_upper_kg'])
        compare(path+'/rain_1h_kg',wet['rain'][f'{f}|R{R}|wait3600s']['total_kg'],row['rain_1h_kg'])
        for night,field in [('night_050_reference','dew_reference_kg'),('night_050_saturated','dew_saturated_kg')]:
            if row['lead']=='P2':
                value=wet['dew'][f'{f}|R{R}|{night}']['retained_kg']
                compare(path+'/'+field,value,row[field])
            else:
                val,dep=retained(f,R,beta,night=night)
                trials={str(angle):float(np.where(beta<np.deg2rad(angle),dep,val)@wt*A) for angle in [9,10,12,14,15,16]}
                p3dew.append(dict(path=path+'/'+field,owner=row[field],top_cap_trials=trials))
                compare(path+'/'+field,trials['14'],row[field])
    for i,row in enumerate(W['waits']):
        R,f,c=row['R_m'],row['finish'],row['condition']
        rates=sorted([dry[f'R{R}|{m}|{f}|{c}']['hull_rate_kg_h'] for m in ['sphere040','flatplate']])
        for j,v in enumerate(rates):compare(f'WATER/waits/{i}/rate/{j}',v,row['hull_rate_kg_h'][j])
        # Use each account's inventory, including the owner's geometric dew increment.
        acc=next(x for x in W['account'] if x['lead']==row['lead'] and x['finish']==f and x['R_m']==R and x['weather']=='ISA')
        for fkey in ['rain_10min_kg','dew_saturated_kg']:
            for j,val in enumerate([acc[fkey]/rates[1],acc[fkey]/rates[0]]):
                compare(f'WATER/waits/{i}/{fkey}/{j}',val,row['dry_fully_h_'+fkey][j])
    methods=[]
    for row in W['methods']:
        R=row['R_m'];A=4*np.pi*R*R;m=row['method'];own={}
        if m.startswith('superhydrophobic'):
            own=dict(flying_mass_kg=[A*13e-6*1000,A*25e-6*1500],
                cost_usd_per_application=2*A/23*3.8*(7685.9/(50*3.785411784)),
                corrected_two_coat_mass_kg=[2*A*13e-6*1000,2*A*25e-6*1500])
        elif m.startswith('onboard'):
            own=dict(flying_mass_kg=A*.04*.001/1e-4)
        elif m.startswith('shelter'):
            own=dict(floor_m2=(2*R+4)**2,cost_rub=(2*R+4)**2*3848256/450)
        elif m.startswith('ground-supported'):
            own=dict(fabric_kg=[1.1*A*.042,1.1*A*.09])
        elif m.startswith('air knives'):
            own=dict(power_kW=[4,180*.7457],energy_kWh_per_pass=[2,180*.7457*.5])
        elif m=='ground heating':
            rain=wet['rain'][f'MLCCAg|R{R}|wait600s']['total_kg']
            own=dict(dew_prevention_kWh_per_night=319*(R/10)**2,dew_prevention_kW=26.6*(R/10)**2,
                evaporate_P2_rain_kWh_ideal=rain*2.45/3.6,
                evaporate_P3_ponds_kWh_ideal=[P['radii'][str(R)]['pond_random_top']['random_mean']*2.45/3.6,P['radii'][str(R)]['pond_face_up_kg']*2.45/3.6])
        for k,v in own.items():
            if k not in row:continue
            if isinstance(v,list):
                for i,x in enumerate(v):compare(f'WATER/methods/R{R}/{m}/{k}/{i}',x,row[k][i])
            else:compare(f'WATER/methods/R{R}/{m}/{k}',v,row[k])
        methods.append(dict(R=R,method=m,own=own))
    dump('WATER-COMPARISONS.json',COMP)
    dump('WATER-INDEPENDENT.json',dict(methods=methods,p3_dew_cap_diagnostics=p3dew,
        comparisons=len(COMP),failed=[r for r in COMP if not r['passed']]))
    print('comparisons',len(COMP),'failed',sum(not r['passed'] for r in COMP))
    print('P3 dew',p3dew[:4])
if __name__=='__main__':main()
