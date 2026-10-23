"""Compile independent arithmetic, exact differences, qualifications and figures."""
from liquid_check import *
import datetime,csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read(name):return json.loads((ROOT/name).read_text())
def check(rows,name,ok,**detail):rows.append(dict(name=name,passed=bool(ok),**detail))
def main():
    liquid=read('LIQUID-COMPARISONS.json');water=read('WATER-COMPARISONS.json')
    capacity=read('CAPACITY-COMPARISONS.json');least=read('LEAST-INDEPENDENT.json')
    pond=read('PONDS-INDEPENDENT.json');pv=read('POND-VALIDATION.json')
    ret=read('RETAIN-INDEPENDENT.json');dry=read('DRY-INDEPENDENT.json')
    local=read('LOCAL-DRYING.json');methods=read('WATER-INDEPENDENT.json')['methods']
    ow=read('owner/WATER.json');op=read('owner/PONDS.json')
    prior=read('intake/own052/RESULTS.json')
    caps=read('CAPACITY-ENDPOINTS-INDEPENDENT.json')
    tests=[]
    check(tests,'drop, rain, dew and energy-balance fields',all(x['passed'] for x in liquid),count=len(liquid))
    check(tests,'capacity endpoints and zero-payload water',all(x['passed'] for x in capacity),count=len(capacity),
          max_payload_difference_kg=max(abs(x['delta']) for x in capacity if x['key'].startswith('endpoint')))
    failures=[x for x in water if not x['passed']]
    check(tests,'water account: only the two identified coating-cost discrepancies',len(failures)==2 and all('cost_usd' in x['path'] for x in failures),count=len(water))
    axes=['gamma','Q','face_compression_and_E','film']
    for x in least:
        m=None if x['owner_axes'] is None else sum(1<<axes.index(y) for y in x['owner_axes'])
        check(tests,f"least choice row {x['row']}",m==x['least_mask'] and
              (m is None or abs(x['usage_difference'])<5e-6),**x)
    for x in pv['cartesian_checks']:
        check(tests,f"independent triangle integral {x['beta_deg']}/{x['azimuth_deg']}",x['passed'],delta_kg=x['delta_kg'])
    check(tests,'pond quadrature refinement',pond['max_quadrature_difference_s3']<1e-8,
          max_difference_s3=pond['max_quadrature_difference_s3'])
    for fine in local['convergence']:
        coarse=next(x for x in local['rows'] if all(x[k]==fine[k] for k in ['R','finish','condition','mode','initial']))
        check(tests,'local drying convergence '+fine['mode'],
            abs(fine['residual_at_bulk_hours_kg']-coarse['residual_at_bulk_hours_kg'])<.001 and
            abs(fine['local_99pct_removal_hours']-coarse['local_99pct_removal_hours'])<.005)
    check(tests,'energy residual',max(x['max_energy_residual_W_m2'] for x in local['rows'])<1e-8)

    mismatches=[]
    def mismatch(ident,kind,claim,own,owner,unit,explanation):
        mismatches.append(dict(id=ident,kind=kind,claim=claim,independent=own,filed=owner,
                               delta=own-owner if isinstance(own,(int,float)) and isinstance(owner,(int,float)) else None,
                               units=unit,explanation=explanation))
    for R in [10,30]:
        m=next(x for x in methods if x['R']==R and x['method'].startswith('superhydrophobic'))['own']
        om=next(x for x in ow['methods'] if x['R_m']==R and x['method'].startswith('superhydrophobic'))
        for i,edge in enumerate(['minimum','maximum']):
            mismatch(f'COAT-MASS-R{R}-{edge}','source application','two-coat dry mass',
                m['corrected_two_coat_mass_kg'][i],om['flying_mass_kg'][i],'kg',
                'Supplier step 1 specifies 13–25 micrometres; step 2 follows the same application guidelines. Retain the assumed 1000–1500 kg/m³ density, count both layers.')
        mismatch(f'COAT-COST-R{R}','arithmetic/source application','bottom-coat unit price applied to both layers',
            m['cost_usd_per_application'],om['cost_usd_per_application'],'USD',
            '2*A/23*3.8/(50*3.785411784)*7685.90. Conditional equal top/bottom price, not a supplier quote for a full installed system.')
    mismatch('POND-K','continuum versus quadrature','shape normalization',
        pond['exact_shape_normalization'],op['k_shape'],'dimensionless',
        'For uniform triangle area, t=3 min(lambda) has density 2(1-t), so mean[t(2-t)]=1/2. Filed k is reproduced by an equal-weight boundary-inclusive barycentric grid with 301 divisions; this is a resolved numerical convention with a finite-grid bias.')
    for field,own,owner in [
        ('orientation_integral',pond['orientation_integral_kg'],op['radii']['10']['pond_capacity_kg']),
        ('node_up',pv['positions']['node']['volume_kg'],op['radii']['10']['pond_vertex_up_kg']),
        ('bay_up',pv['positions']['bay']['volume_kg'],op['radii']['10']['pond_face_up_kg']),
        ('random_mean',pond['sample_1024']['mean'],op['radii']['10']['pond_random_top']['random_mean']),
        ('random_min',pond['sample_1024']['min'],op['radii']['10']['pond_random_top']['random_min']),
        ('random_p05',pond['sample_1024']['p05'],op['radii']['10']['pond_random_top']['random_p05']),
        ('random_p95',pond['sample_1024']['p95'],op['radii']['10']['pond_random_top']['random_p95'])]:
        mismatch('POND-'+field,'independent surrogate / non-reproduction',field,own,owner,'kg',
            'Independently tiled equilateral bays retain their azimuth and are counted once. 1024 deterministic placements replace an undisclosed 200-placement sample. These are explicit model/sampling differences, not asserted corrections to the real 500-bay frame.')
    mismatch('POND-TILT','model/claim','largest directional spill angle',
        pv['continuous_spill_angle_max_deg'],14.,'degrees',
        'The declared dish still contains water at 14 degrees for some azimuths; the owner numeric profile also remains positive above 14. Rotating the hull also moves other bays toward its top.')
    for r in local['convergence']:
        mismatch('DRY-MIDDAY-'+r['mode'],'interpretation','water remaining at mass/fullwet-rate time',
            r['residual_at_bulk_hours_kg'],0.,'kg',
            'Local inventory is max(m0-E*t,0); already dry patches cease evaporating. Model at 0.5 degree resolution, held weather, no redistribution or runoff.')
    morning=next(r for r in local['rows'] if r['R']==10 and r['finish']=='MLCCAg' and
                 r['initial']=='rain' and r['condition']=='morning_fair' and r['mode']=='sphere040')
    mismatch('DRY-MORNING','interpretation','condensing area under held fair morning',
        morning['condensing_area_fraction'],0.,'fraction',
        'Positive hull-average potential evaporation does not imply all locations dry. No finite complete-drying time in this held-weather model.')
    mismatch('DRY-POND-AREA','interpretation','pond evaporation time method',
        'integral of dV / (E*A(V))','V_initial / (E*A_initial)','method',
        'Shrinking free surface invalidates constant-area complete-drying time. Constant uniform flux implies maximum vertical depth divided by evaporation depth rate.')
    r30=next(x for x in caps if x['R']==30 and x['weather']=='ISA')
    mismatch('HEATER-R30','scope/claim','R30 P2 payload after film heater alone',
        float(r30['endpoints']['11']['payload_kg'])-4*np.pi*30**2*.4,
        'excluded: heavier than either lead margin','kg',
        'Film alone is 4523.893 kg versus 11612.999 kg P2 and 8895.646 kg P3 margins. Power supply, wiring, controls and optics remain unaccounted, so this is not an endorsement of onboard heating.')
    dump('MISMATCHES.json',mismatches)

    nfis=[]
    def nfi(code,topic,evidence,fix):
        nfis.append(dict(id='NFI-CHECK059-'+code,status='OPEN',tag='QUESTIONABLE / PROJECTION',
                         topic=topic,evidence=evidence,needed_to_ground=fix))
    nfi('01','Complete drying and float readiness',
        'Midday bulk times leave 11.7071–13.5622 kg. 99% removal takes 0.31031–5.34571 h under held weather; these are not guaranteed operating times.',
        'Replace complete-drying labels with potential-rate equivalents, integrate local inventories and the water threshold required for takeoff; measure full curved-panel drying.')
    nfi('02','Morning condensation',
        'Sphere-correlation morning model condenses on 36.545% of the hull while the full-wet hull integral is positive.',
        'Resolve wet/dry areas, runoff and time-varying sun/weather before using a morning waiting time.')
    nfi('03','Pond orientation and missing placement inputs',
        'Named 55.1496/171.4239 kg node/bay totals are not reproduced. Explicit independent triangular geometry gives 110.7660/117.0939 kg.',
        'Publish vertices, oriented bays, placement coordinates/seed and quadrature; evaluate the actual 500-face frame, including fivefold vertices. Confirm by a full-size bay test. Do not promote either surrogate to a hull prediction.')
    nfi('04','Pond discretization and tilt',
        '301-division equal-point quadrature reproduces k=1.017367; continuous area gives 1.007250. Directional dry angle reaches 16.5463 degrees, and the filed profile is positive above 14.',
        'Converge area-weighted integration and trace the complete tilt/drain/re-capture path rather than claiming all ponds empty after a single 14-degree hull tilt.')
    nfi('05','Pond drying',
        '65–465 h reproduces a mass/initial-area/flux calculation. Area shrinks as water level falls.',
        'Integrate changing pond area and use liquid-water optical properties. Retain the operational finding that passive pond drying is slow.')
    nfi('06','Two-layer coating bill',
        'At R10 the same thickness/density assumptions give 32.6726–94.2478 kg and USD 16861.9274, versus 16.3363–47.1239 kg and USD 8430.9637.',
        'Count bottom and top coats; measure cured areal mass. Obtain a top-coat quote. Resolve the retailer heading 50 gallons versus descriptive 55-gallon drum, and include application cost.')
    nfi('07','Retention transfer',
        'Measured acrylic 0.35±0.08 g over 80×80 mm equals 54.6875±12.5 g/m². The 54 g/m² calibration is a rounded mean. Rain factor 0.08/0.054 is a cross-material scenario, not a statistical upper bound.',
        'Measure advancing/receding angles, population/coverage, water uptake and retained load on actual finishes; include underside rain and drainage across the equator.')
    nfi('08','Wet thermal and phase assumptions',
        'All RETAIN finishes inherit mirror emittance .8 for dew. The dry-optics reference night reaches 272.9766 K locally. Sphere convection is extrapolated to large Reynolds numbers.',
        'Measure wet optics and transfer; model liquid/ice phase and both hull faces. Keep the whole calculation provisional.')
    nfi('09','P3 dew top cap',
        'P3 dew totals reproduce only when all deposited water is retained over the top 14-degree cap, independently of bay orientation.',
        'Document that inferred cap convention and replace it with each bay’s remaining capacity and drainage connection.')
    nfi('10','Capacity scope',
        'P2 capacities are for the mirror, actual joining, bake, cure in global/crimp, no 5% joining floor. They are reused for other finishes without changing their thermal/coating bill.',
        'Recompute capacity after any actual coating, heater, weather or joining change. Add pond hydrostatic loading and installed failure qualifications when resolving the structural model.')
    nfi('11','Heater and shelter comparison',
        'Film-mass rejection applies at R10, not at R30 ISA. Floor-scaled shelter cost has no adequate height or system quote; air-knife costs and residual water are absent.',
        'Compare complete energy, wiring, ground equipment, availability and shelter bills before claiming a least-cost operating system.')
    nfi('12','FAO comparison scope',
        'FAO example 19 is grass reference evapotranspiration with surface resistance and ground heat storage. A sun-facing wet hull element is a different boundary-value problem.',
        'Keep 0.63 versus about 0.72 kg/m²/h as a plausibility comparison, not validation of hull drying.')
    dump('NFI.json',dict(unit='vacuum-mainline059-check-1020',status='OPEN',new=nfis,
        inherited_owner=read('owner/NFI.json')['items'],
        inherited_other_registers=['intake/own052/NFI.json','intake/own053/NFI.json','intake/050/NFI.json']))

    # Re-derive sag, bay dimensions and all radius scalings, independently of the placement claims.
    scale=[]
    c=1-np.sqrt(11/12);mean=.5+2*c*c
    s10=73.1007331152853/(1.16726833074618*4*np.pi*10**2*c*mean)
    for r,opoint in op['radii'].items():
        R=int(r);s=s10*R/10;area=np.sqrt(3)/4*s*s;A=4*np.pi*R*R
        own=dict(s_m=s,crown_m=c*s,bay_area_m2=area,bays=A/area,
            level_bay_capacity_kg=1000*area*c*s*mean)
        for k,v in own.items():
            scale.append(dict(R=R,field=k,own=v,owner=opoint[k],delta=v-opoint[k]))
            check(tests,f'pond geometry R{R} {k}',abs(v-opoint[k])<1e-7)
        for k in ['pond_face_up_kg','pond_vertex_up_kg','pond_capacity_kg','level_bay_capacity_kg']:
            val=op['radii']['10'][k]*(R/10)**3
            check(tests,f'conditional cubic scaling {R} {k}',abs(val-opoint[k])<1e-8)
    dump('POND-SCALING.json',scale)
    results=dict(unit='vacuum-mainline059-check-1020',status='COMPLETE WITH NFI',
        classification='QUESTIONABLE / PROJECTION',qualified_installed_hull_SF=None,
        liquid_comparisons=len(liquid),liquid_failures=sum(not x['passed'] for x in liquid),
        capacity_comparisons=len(capacity),water_comparisons=len(water),water_discrepancies=failures,
        least_rows=len(least),independent_pond=pond,pond_validation=pv,
        local_midday=local['convergence'],new_nfi_count=len(nfis),inherited_owner_nfi_count=12,
        tests=len(tests),failed_tests=[x for x in tests if not x['passed']],
        code_access='Owner and predecessor executables excluded; only this seat’s prior independent mechanics reused.',
        completed_at=datetime.datetime.now().astimezone().isoformat())
    dump('RESULTS.json',results);dump('VALIDATION.json',tests)
    lines=['# CHECK-059: retained-water audit','',
        'Complete with corrections and open qualifications. QUESTIONABLE / PROJECTION. No installed-hull qualification is asserted.',
        '',
        'The drop/film and energy-balance arithmetic reproduces (7,094 fields). The 185 capacity comparisons reproduce within 3 g in payload and 3×10⁻⁶ kg/m² in capacity; all 37 least-set choices agree. Water-account arithmetic reproduces except the two coating-cost rows. Complete-drying claims, the coating bill and named pond placements need the changes below.',
        '',
        '## Exact differences and consequence','',
        '| Item | Filed | Independent | Meaning |','|---|---:|---:|---|',
        f'| R10 coating dry mass, kg | 16.3363–47.1239 | 32.6726–94.2478 | Both supplier-required layers, same assumed density |',
        f'| R10 equal-price coating cost, USD | 8430.963714 | 16861.927429 | Both layers; not an installed quote |',
        f'| R30 equal-price coating cost, USD | 75878.673429 | 151757.346858 | Same correction |',
        f'| R10 pond angular-integral mean, kg | {op["radii"]["10"]["pond_capacity_kg"]:.9f} | {pond["orientation_integral_kg"]:.9f} | Continuum area integration of declared dish |',
        f'| R10 node-up ponds, kg | 55.149608596 | {pv["positions"]["node"]["volume_kg"]:.9f} | Explicit alternative tiling; filed placement not reproduced |',
        f'| R10 bay-up ponds, kg | 171.423902496 | {pv["positions"]["bay"]["volume_kg"]:.9f} | Explicit alternative tiling; not a corrected real-hull result |',
        f'| Largest directional spill angle, deg | about 14 | {pv["continuous_spill_angle_max_deg"]:.9f} | Some declared bays retain water above 14 |',
        '| R10 midday water left at the bulk time, kg | 0 (“fully dry”) | 11.707123–13.562237 | Dry parts stop evaporating |',
        '',
        'MISMATCHES.json records exact numbers, signs, units and classifications; the comparison JSONs retain every scalar difference. POND-GRID-INDEPENDENT.json is a diagnostic of unreported quadrature, not a selected physical model.',
        '',
        '## Drop calibration and retained loads','',
        'For cap base radius a and q=tan(theta/2), V=πa³q(3+q²)/6. Balancing rho*g*V*sin(beta) against 2*a*gamma*(cos(theta_R)-cos(theta_A)) gives a_c. Projected radius is a below 90° contact angle and a/sin(theta) above it. The plate fixes kappa=0.06264893813335032 and a_c=2.500176546338056 mm. This is a coverage/population calibration, not a measured critical radius for the hull.',
        '',
        '| Finish, R10 | Rain after 10 min, kg/m² | Upper rain scenario | Reference dew | Saturated dew |',
        '|---|---:|---:|---:|---:|']
    for f in RET['finishes']:
        rain=ret['rain'][f'{f}|R10|wait600s']['mean_kg_m2']
        ref=ret['dew'][f'{f}|R10|night_050_reference']['retained_mean_kg_m2']
        sat=ret['dew'][f'{f}|R10|night_050_saturated']['retained_mean_kg_m2']
        lines.append(f'| {f} | {rain:.9f} | {rain*.08/.054:.9f} | {ref:.9f} | {sat:.9f} |')
    lines += ['', 'Rain 0.014219621–0.051481564 and dew 0.010875146–0.056001172 kg/m² reproduce. The ×1.481481 upper-rain scenario reaches 0.076268984 kg/m². Every retained profile and all radii are in RETAIN-INDEPENDENT.json. These values fit 0.1 kg/m² within this model, without waiting. They do not establish a measured upper bound.',
        '',
        '## Capacity, with the named bill','',
        '| R, m | P2 ISA, kg/m² | P2 optimistic | P3 ISA | P3 optimistic |',
        '|---|---:|---:|---:|---:|']
    for R in [10,12,15,20,30]:
        vals=[]
        for w in ['ISA','optimistic']:
            ep=next(x for x in caps if x['R']==R and x['weather']==w)['endpoints']['11']['payload_kg']
            vals.append(.1+ep/(4*np.pi*R*R))
        for w in ['ISA','optimistic']:
            ep=next(x for x in prior['rows'] if x['R_m']==R and x['weather']==w and x['service']=='ground')['all_axes_endpoint']['payload_kg']
            vals.append(.1+ep/(4*np.pi*R*R))
        lines.append('| '+str(R)+' | '+' | '.join(f'{x:.9f}' for x in vals)+' |')
    lines += ['', 'Capacity is 0.1 + endpoint payload/(4πR²). P2 includes cure compression in global/crimp, bake, mirror coating and actual joining without the 5% floor. This explains why its R12 value differs from the retained-floor primary case in CHECK-053. P3 uses this seat’s independently derived MAINLINE-052 ground-service bill; the owner rounded endpoint payloads to 0.001 kg. One kg/m² exterior water floats only at R30 ISA among the sampled cases, on gamma/Q/film, usage about 0.917466 and about +1434.239 kg. Full endpoints, least choices and signed residuals are supplied.',
        '',
        '## Pond geometry and operating claim','',
        f'The charged spherical-cap crown ratio is {c:.15g}, and circular mean/crown is {mean:.15g}; these give s={s10:.12f} m at R10, crown 0.098954140165 m and 116.585202 kg for a level bay. The area-based equivalent bay count is 537.164867, while the actual f5 frame has 500 faces. This is already an effective surrogate.',
        '',
        'For the stated triangular dish, d=k*c*t*(2-t), t=3 min(lambda). Uniform triangle area makes mean[t(2-t)]=1/2, hence k=1.007249804616. The reported 1.0173672190414051 is independently reproduced with 301 barycentric divisions and equal weights including the rim; it does not represent the continuum area average. Exact strip integration agrees with independent two-dimensional quadrature in nine checks. The angle-averaged profile is tabulated against every filed ordinate.',
        '',
        f'The independent explicit tiling gives a 1024-placement mean {pond["sample_1024"]["mean"]:.6f} kg, sampled range {pond["sample_1024"]["min"]:.6f}–{pond["sample_1024"]["max"]:.6f} kg, and node/bay witnesses above. The owner used 200 placements without their coordinates or random seed in the packet. Its 5–171 kg placement envelope is not independently established. Both accounts scale cubically with radius, but this scaling does not validate their R10 coefficient. Use the full frame and a sagged-bay experiment to settle the load; neither surrogate licenses an R10 float.',
        '',
        'The owner’s R10 bay-up arithmetic is 39.020593+171.423902=210.444496 kg versus 156.526706 kg total water capacity. That arithmetic is correct conditional on its pond input. Merely replacing it by the independent surrogate would leave a margin of only about 0.41 kg in that example; such a tiny unqualified difference must not be treated as flight clearance. Under the upper rain scenario both the independent node and bay witnesses exceed the capacity.',
        '',
        '## Drying','',
        'The 76 heat/mass-transfer cases reproduce with air density 1.2 kg/m³, cp=1005 J/kg/K, vapor gas constant 461.5, Le=0.845, Magnus saturation, and 36×72 midpoint angular samples. The printed mean is normalized; the hull integral retains the midpoint sine weights. RETAIN interpolates clipped positive condensation on the coarse polar grid, uses mirror optics for all finishes, and adds all deposition over the top 14° for P3. Those conventions explain the final numerical agreement.',
        '',
        'At R10 the mirror’s fair-midday potential is about 34.46–216.93 kg/h. M/E gives 0.16262–1.02381 h, but local integration leaves 11.7071–13.5622 kg at those respective times. A 0.5° calculation gives 99% removal after 0.31031–5.34571 h. The last trace of polar water is grid-sensitive, so no universal complete-drying time is claimed. Under held fair-morning sphere convection, about 36.545% of area condenses; a positive mean does not ensure complete drying. Weather variation and runoff are still omitted.',
        '',
        'The pond time range reproduces as approximately 64.52–216.11 h (node) and 138.60–464.25 h (bay), using filed volumes and initial wetted areas with top-point paint flux. It is an initial-area equivalent, not full drying. As an illustrative alternative, the independent geometry with constant top-point flux would require 127–426 h for node-up and 427–1430 h for bay-up from maximum vertical depth. Actual liquid-water optics, weather and changing exposure remain unresolved.',
        '',
        '## Disposition','',
        'Retain 0.1 kg/m² as a provisional design assumption, with the owner’s retention qualification carried forward. Correct the coating bill and drying labels. Keep P3’s pond orientation and tilt-drain claims open until the actual bay geometry and handling path are evaluated. The full-size weighing and logged drying experiments remain the right grounding measurements.',
        '',
        f'{len(nfis)} new NFI rows plus all 12 owner rows are in NFI.json; the pinned 052/053/050 registers are inherited. No objection stops the completed check. One report is filed to sciences, cc co, xo and admiral-robotics-review-v2; no out-of-band seat contact.',
        '',
        '## Evidence and reproducibility','',
        'SOURCE-AUDIT.md provides primary-source checks. METHOD.md records the independent numerical choices. INPUT-PINS.json, SOURCE-PINS.json, execution receipts and MANIFEST.json carry hashes. Owner/predecessor executable paths are listed only as exclusions; none was read, copied, hashed, imported or run. Scientific work used admitted one-core, 1 GiB jobs. An early missing R20 thermal table and a diagnostic JSON-print type error were corrected; their receipts remain. Early arithmetic differences were resolved as documented density, angular-grid, clipping, cure and joining conventions.',
        '',
        f'Validation: {len(tests)} checks, {sum(not x["passed"] for x in tests)} unexplained validation failures. Physical/model discrepancies are explicit, not suppressed.']
    (ROOT/'CARD.md').write_text('\n'.join(lines)+'\n')
    with (ROOT/'MISMATCHES.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(mismatches[0]));w.writeheader();w.writerows(mismatches)
    render(ret,pond,pv,local,methods)
    print(json.dumps(dict(checks=len(tests),failed=[x for x in tests if not x['passed']],
                         discrepancies=len(mismatches),new_nfi=len(nfis)),indent=2))

def render(ret,pond,pv,local,methods):
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axs=plt.subplots(2,2,figsize=(12,8.6))
    fig.suptitle('CHECK-059 · Retained water: arithmetic and limits',fontsize=18,x=.06,ha='left',weight='bold')
    fs=['MLCCAg','paint_040','hydrophobic_FEP','slippery_silicone','superhydrophobic'];x=np.arange(5)
    ax=axs[0,0]
    rain=[ret['rain'][f'{f}|R10|wait600s']['mean_kg_m2'] for f in fs]
    dew=[ret['dew'][f'{f}|R10|night_050_saturated']['retained_mean_kg_m2'] for f in fs]
    ax.bar(x-.18,rain,.36,label='Rain, 10 min',color='#206e91')
    ax.bar(x+.18,dew,.36,label='Saturated dew',color='#85b4c3')
    ax.axhline(.1,color='#ad4432',ls='--',label='Design allowance')
    ax.set_xticks(x,['Mirror','Paint','FEP','Silicone','Superhyd.'])
    ax.set_ylabel('Retained water / hull area (kg/m²)')
    ax.set_title('R10 smooth hull: numerical retention reproduces',loc='left',fontsize=11)
    ax.legend(fontsize=8,frameon=False)
    ax=axs[0,1]
    for mode,color,label in [('sphere040','#206e91','Sphere correlation'),('flatplate','#b65b39','Wind flat-plate bracket')]:
        row=next(x for x in local['convergence'] if x['mode']==mode)
        ts=[float(t) for t in row['inventory_kg'] if float(t)<=8]
        vals=[row['inventory_kg'][str(int(t)) if t.is_integer() else str(t)] for t in ts]
        ax.plot(ts,vals,marker='o',ms=3,color=color,label=label)
        ax.scatter([row['bulk_hours']],[row['residual_at_bulk_hours_kg']],marker='X',s=65,color=color)
    ax.set(xlabel='Held fair-midday weather (hours)',ylabel='Water remaining (kg)',ylim=(-1,38))
    ax.set_title('“Fully dry” bulk times leave 12–14 kg',loc='left',fontsize=11)
    ax.legend(fontsize=8,frameon=False);ax.text(.98,.49,'× = mass / full-wet rate',ha='right',transform=ax.transAxes,fontsize=8)
    ax=axs[1,0];x=np.arange(3)
    owner=[36.62985885071348,55.14960859574659,171.42390249596139]
    own=[pond['orientation_integral_kg'],pv['positions']['node']['volume_kg'],pv['positions']['bay']['volume_kg']]
    ax.bar(x-.18,owner,.36,label='Filed surrogate',color='#96a0a5')
    ax.bar(x+.18,own,.36,label='Independent surrogate',color='#206e91')
    ax.axhline(156.52670614359172-39.0205933864096,color='#ad4432',ls='--')
    ax.set_xticks(x,['Angular mean','Node up','Bay up']);ax.set_ylabel('R10 ponds (kg)')
    ax.set_title('Pond placement needs actual frame geometry',loc='left',fontsize=11)
    ax.legend(fontsize=8,frameon=False,loc='upper left')
    ax.text(.02,.51,'Dashed: pond budget after base rain residue',transform=ax.transAxes,fontsize=8,color='#ad4432')
    ax=axs[1,1]
    low=[16.336281798666924,32.67256359733385];high=[47.1238898038469,94.2477796076938]
    for i in range(2):
        ax.plot([low[i],high[i]],[i,i],lw=11,color=['#96a0a5','#206e91'][i],solid_capstyle='butt')
        ax.text(high[i]+2,i,f'{low[i]:.1f}–{high[i]:.1f}',va='center',fontsize=9)
    ax.axvline(17.40749809715305,color='#ad4432',ls='--')
    ax.set_yticks([0,1],['Filed: one layer','Supplier: two layers'])
    ax.set(xlim=(0,117),ylim=(-.6,1.7),xlabel='R10 dry coating mass (kg)')
    ax.set_title('Count both coats; same density assumptions',loc='left',fontsize=11)
    ax.text(.03,.95,'Dashed: modelled rain water saved, 17.4 kg',transform=ax.transAxes,fontsize=8,va='top',color='#ad4432')
    fig.text(.06,.025,'QUESTIONABLE / PROJECTION · Held-weather and ideal-bay models · No installed-hull or operating qualification',fontsize=9,color='#555555')
    fig.tight_layout(rect=[.02,.05,.99,.94],h_pad=3,w_pad=3)
    for ext in ['pdf','png','svg']:fig.savefig(ROOT/f'CHECK-059.{ext}',dpi=160)
    plt.close(fig)
if __name__=='__main__':main()
