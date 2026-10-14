#!/usr/bin/env python3
"""One frozen split cassette: saved-boundary wrench transfer, stock and lift.

No ancestor code is loaded. All nominal section/connection demands are
conditional on the explicitly unqualified contact and stiffness assumptions.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = U.parents[2]
O = [40.0, 0.0, 0.0]
Z = [0.0, 0.0, 0.0]
T = [0.0, 0.0, 1.0]

def add(a, b): return [x+y for x, y in zip(a, b)]
def sub(a, b): return [x-y for x, y in zip(a, b)]
def mul(a, s): return [x*s for x in a]
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def norm(a): return math.sqrt(dot(a, a))
def unit(a): return mul(a, 1/norm(a))
def mid(a, b): return mul(add(a, b), .5)
def total(vs): return [sum(v[i] for v in vs) for i in range(3)]
def moment_at(F, M, p, q): return add(M, cross(sub(p, q), F))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def box_area(size, wall): return size**2-(size-2*wall)**2
def box_inertia(size, wall): return (size**4-(size-2*wall)**4)/12

def frame(axis):
    e=unit(axis); seed=T if abs(dot(e,T))<.9 else [1.,0.,0.]
    v=unit(cross(seed,e));w=cross(e,v)
    return e,v,w

def bolt_stock(d, length):
    # Paid cylindrical shank, hex-prism head/nut blanks, two annular washers.
    head=1.5*d; nut=.8*d; ht=.65*d; wt=d/6
    return 7850*(math.pi*d*d*length/4+math.sqrt(3)*head*head*(ht+nut)/2
                 +2*math.pi*((1.85*d)**2-(1.1*d)**2)*wt/4)

def bolt_group(F, M, p, axis, offsets, d, core, length, grip):
    e,v,w=frame(axis);n=len(offsets)
    # e,v,w right handed; F_e and both bending moments remain signed.
    fe,fv,fw=[dot(F,a) for a in (e,v,w)];me,mv,mw=[dot(M,a) for a in (e,v,w)]
    sv=sum(x*x for x,y in offsets);sw=sum(y*y for x,y in offsets);polar=sv+sw
    rows=[]
    for x,y in offsets:
        axial=fe/n+mv*y/sw-mw*x/sv
        shear_v=fv/n-me*y/polar;shear_w=fw/n+me*x/polar
        f=add(mul(e,axial),add(mul(v,shear_v),mul(w,shear_w)))
        loc=add(p,add(mul(v,x),mul(w,y)))
        rows.append(dict(offsetVWm=[x,y],centreXRTm=loc,forceXRTn=f,signedAxialN=axial,
                         tensionPa=max(0,axial)/(math.pi*core**2/4),shearPa=math.hypot(shear_v,shear_w)/(math.pi*core**2/4)))
    force_res=norm(sub(total([x['forceXRTn'] for x in rows]),F))
    mom_res=norm(sub(total([cross(sub(x['centreXRTm'],p),x['forceXRTn']) for x in rows]),M))
    projection=2*(d/6)+.8*d+.4*d
    tension=max(x['tensionPa'] for x in rows);shear=max(x['shearPa'] for x in rows)
    return dict(datumXRTm=p,axisXRT=e,basisVW=[v,w],forceXRTn=F,coupleXRTnm=M,
                boltCount=n,diameterM=d,threadRootProxyM=core,underHeadLengthM=length,
                gripM=grip,nutWashersProjectionM=projection,lengthAllowanceM=length-grip-projection,
                lengthPass=length>=grip+projection,bolts=rows,forceResidualN=force_res,
                momentResidualNm=mom_res,maximumTensionPa=tension,maximumShearPa=shear,
                nominal355MPaComparisonPass=max(tension,shear)<=355e6,
                contactPryingSlipPreloadAndCombinedCapacity=None,
                qualification='Bilateral elastic demand distribution, including negative axial forces; compression requires actual contact. 355MPa is an inherited nominal comparison, not bolt certification.')

def beam_screen(F, M, axis, length, size, wall, plate=False):
    e,v,w=frame(axis); N=-dot(F,e); internalM=mul(M,-1)
    if plate:
        width=size;thickness=wall;area=width*thickness
        # Demand envelope uses weak modulus regardless of direction: conservative
        # scalar screen, not a biaxial/local-buckling or open-section torsion rating.
        inertia=width*thickness**3/12;modulus=width*thickness**2/6
        torsion=None
    else:
        area=box_area(size,wall);inertia=box_inertia(size,wall);modulus=inertia/(size/2)
        torsion=abs(dot(internalM,e))/(2*(size-wall)**2*wall)
    bending=norm(sub(internalM,mul(e,dot(internalM,e))))
    normal=abs(N)/area+bending/modulus
    euler=math.pi**2*200e9*inertia/max(length,.001)**2
    return dict(internalForceXRTn=mul(F,-1),internalCoupleXRTnm=internalM,
                axialTensionPositiveN=N,areaM2=area,weakInertiaM4=inertia,weakModulusM3=modulus,
                normalEnvelopePa=normal,torsionShearPa=torsion,conditionalEulerN=euler,
                normalComparisonPass=normal<=355e6,eulerComparisonPass=N>=0 or -N<=euler,
                combinedBucklingWeldAndConnectionCapacity=None)

def main():
    assert sys.argv[1:]==['--write'], 'Use --write for one recorded numerical execution.'
    B=json.loads((U/'baseline.json').read_text()); S=json.loads((U/'sources.json').read_text())
    for path,digest in S['inputFiles'].items():
        assert sha(R/path)==digest, 'Frozen input differs: '+path
    # First numerical operations occur after this explicit marker.
    print('SCIENCE_STARTED: one fixed geometry; two assignments; 74 gravity orientations',flush=True)
    D=B['design']; G=B['geometry']; rho=D['steelDensityKgM3'];repeat=74
    nodes=G['nodesXRT']; dnode=nodes['D'];cnode=nodes['C']; e=unit(sub(cnode,dnode));n=unit(cross(T,e))
    length=norm(sub(cnode,dnode))+2*D['cheekEndExtensionM']; centre=mid(dnode,cnode)
    halfgap=D['cheekNormalOffsetM']-D['cheekThicknessM']/2
    def project(p,sign=-1): return add(p,mul(n,sign*halfgap-dot(sub(p,dnode),n)))
    A=G['receivingFrameXRT']['A'];BB=G['receivingFrameXRT']['B']
    members=[];bill=[]
    def item(name,count,eachkg,point,duty,route='A',dimensions=None):
        row=dict(id=len(bill),item=name,countPerModule=count,eachKg=eachkg,massPerModuleKg=count*eachkg,
                 totalCount=count*repeat,massT=count*eachkg*repeat/1000,centreXRTm=point,
                 gravityReceiver=route,duty=duty,dimensions=dimensions)
        bill.append(row);return row
    def plate(name,count,dims,p,duty,route='A'):
        return item(name,count,rho*math.prod(dims),p,duty,route,dims)
    def arm(name,p,q,size,wall,receiver='A',duty='Full wrench path'):
        L=norm(sub(q,p));obj=dict(name=name,firstXRTm=p,lastXRTm=q,axisXRT=unit(sub(q,p)),lengthM=L,
                sizeM=size,wallM=wall,receiver=receiver,duty=duty)
        members.append(obj);item(name+' box stock',1,rho*box_area(size,wall)*L,mid(p,q),duty,receiver,[L,size,wall])
        return obj
    cheeks=[]
    for sign in (-1,1):
        p=add(centre,mul(n,sign*D['cheekNormalOffsetM']))
        cheeks.append(dict(name='inner' if sign<0 else 'outer',centreXRTm=p,axes=[e,T,n],dimensionsM=[length,D['cheekWidthM'],D['cheekThicknessM']],installationWithdrawalXRTm=mul(n,sign)))
        plate('cassette '+cheeks[-1]['name']+' cheek',1,[length,D['cheekWidthM'],D['cheekThicknessM']],p,'One removable half; full rectangular stock including all cutouts/trim')
    stations=[sub(dnode,mul(e,.50)),add(A,[0,.35,0]),add(BB,[0,-.35,0]),add(cnode,mul(e,.40))]
    spacers=[]
    for i,p in enumerate(stations):
        for t in D['spacerTOffsetsM']:
            p=add(p,[0,0,t-p[2]])
            x=arm(f'cross spacer {i} {t:+.2f}',project(p,1),project(p,-1),D['spacerSizeM'],D['spacerWallM'],duty='Split-half connection outside named ring; full outer-cheek weight conservatively routed through spacer0/-0.42')
            spacers.append(x)
            plate(x['name']+' two end plates',2,[.16,.16,.016],mid(x['firstXRTm'],x['lastXRTm']),'Finite split flange; holes/trim charged')
            item(x['name']+' M30 sets',8,bolt_stock(.03,.12),mid(x['firstXRTm'],x['lastXRTm']),'Four bolts per independent end',dimensions=[.03,.12])
    rootarms=[]
    for root in G['roots']:
        name=root['member']+'-'+root['node'];route='B' if root['node']=='B' else 'A'
        x=arm('root '+name,root['forkBaseXRT'],project(root['forkBaseXRT']),D['rootArmSizeM'],D['rootArmWallM'],route)
        x['pinXRTm']=root['pinXRT'];x['pinAxisXRT']=root['pinAxisXRT'];x['key']=name;rootarms.append(x)
        plate(name+' mating plates',2,D['rootArmEndPlateM'],mid(x['firstXRTm'],x['lastXRTm']),'Fork root bolts retained once; second end has four new M24 sets',route)
        plate(name+' nut backers',8,[.08,.08,.012],mid(x['firstXRTm'],x['lastXRTm']),'Four per series end',route)
        item(name+' added M24 sets',4,bolt_stock(.024,.12),x['lastXRTm'],'Second end only; first-end sets are in retained fork kit',route,[.024,.12])
    receiverarms=[];clamps=[]
    for name,P in [('A',A),('B',BB)]:
        dims=D['clampHalfBlankXRTm'];clamps.append(dict(name=name,centreXRTm=P,outerBlankXRTm=[2*dims[0],dims[1],dims[2]],splitPlane='X = receiver centre X',boreRadiusM=.166,cuffOuterRadiusM=.164,cuffInnerRadiusM=.148,cuffFiniteT=[-.2,.2],linerThicknessM=.002,installation='Two open semi-cylindrical halves approach along +/-X; no closed sleeve slides through the ring.'))
        for sign in (-1,1):
            plate(name+f' clamp half {sign}',1,dims,add(P,[sign*dims[0]/2,0,0]),'Full machined half blank including bore trim; retained trim assigned at clamp for gravity',name)
            plate(name+f' external ring reinforcement {sign}',1,D['reinforcementPlateM'],add(P,[sign*(dims[0]+.01),0,0]),'Paid external doubler; curved ring-wall transfer and rotational capacity UNKNOWN',name)
            end=add(P,[sign*(dims[0]+.02),0,0]);start=project(P,sign)
            x=arm(name+f' receiver bridge {sign}',start,end,D['clampBridgeSizeM'],D['clampBridgeWallM'],name)
            receiverarms.append(x)
            plate(x['name']+' two end plates',2,[.36,.36,.02],mid(start,end),'Independent end connections',name)
            item(x['name']+' M24 sets',8,bolt_stock(.024,.12),mid(start,end),'Four per independent foot',name,[.024,.12])
        item(name+' lining stock',1,1100*math.pi*(.166**2-.164**2)*.36,P,'Full two-half liner; no free friction capacity',name,[.332,.328,.36])
        item(name+' root M30 ties',4,bolt_stock(.03,.52),P,'Outside existing cuff wall at R+/-220,T+/-120mm; do not drill carbon',name,[.03,.52])
        plate(name+' root tie backers',8,[.08,.08,.012],P,'Two backers per tie counted in actual grip',name)
    nodearms=[]
    for name,P,size in [('D',dnode,.4),('C',cnode,.2)]:
        nd=D['nodeRingClamp'];rt=nd[name+'plateRTm']
        for sign in (-1,1):
            pos=add(P,[sign*(size/2+.003+.01),0,0])
            plate(name+f' ring contact plate {sign}',1,[.02,*rt],pos,'Finite external ring side plate; full rectangular blank including curvature/trim')
            item(name+f' ring liner {sign}',1,1100*.003*math.prod(rt),pos,'Nominal isolation/contact liner; compression/slip strength UNKNOWN',dimensions=[.003,*rt])
        item(name+' ring M30 ties',4,bolt_stock(.03,.60),P,'External to box wall; four finite ties at declared R/T offsets',dimensions=[.03,.60])
        plate(name+' ring tie backers',8,[.08,.08,.012],P,'Both sides of each tie')
        source=add(P,[-size/2-.003-.02,0,0])
        x=arm(name+' ring boundary bridge',source,project(P),.20,.02,duty='Saved ring-boundary remainder only, separate from main-root and button inputs')
        x['node']=name;nodearms.append(x)
        plate(name+' bridge feet',2,[.30,.30,.02],mid(source,x['lastXRTm']),'Independent plate feet')
        item(name+' bridge M24 sets',8,bolt_stock(.024,.12),mid(source,x['lastXRTm']),'Four per series foot',dimensions=[.024,.12])
    ad=G['members'][0];adp,adq=ad['pinCentresXRT'];adlength=ad['pinLengthM']+.28
    plate('continuous AD plate blank',1,[adlength,.28,.08],mid(adp,adq),'Same pin centres; two102mm bores, constant280x80 section; all bore/corner trim charged')
    button_source=G['buttonSupport']['sourceXRT']
    buttonarm=arm('button continuous arm',button_source,project(cnode),.30,.016,duty='Entire separate finite button source force and couple, once')
    plate('button feet and pads',4,[.4,.4,.02],mid(button_source,buttonarm['lastXRTm']),'Two plates and two profiled pads; full stock')
    plate('button source packing',1,[.4,.4,.008],button_source,'Selected source packing unchanged in thickness')
    plate('button bolt backers',16,[.08,.08,.02],mid(button_source,buttonarm['lastXRTm']),'Eight per independent end')
    item('button M24 sets',16,bolt_stock(.024,.14),mid(button_source,buttonarm['lastXRTm']),'Eight per independent end',dimensions=[.024,.14])
    plate('removable access covers',4,[.30,.20,.012],centre,'Open covers during bolt/pin installation; section screens use gross plate, cut weakening UNKNOWN')
    item('access M12 sets',16,bolt_stock(.012,.07),centre,'Four per cover',dimensions=[.012,.07])
    item('access gasket stock',4,1100*.30*.20*.002,centre,'Paid 2mm gasket',dimensions=[.30,.20,.002])
    seams=sum(4*m['lengthM']+8*m['sizeM'] for m in members)
    item('new fabrication weld stock',1,rho*.5*.012**2*seams,centre,'All box longitudinal seams and two perimeter feet per member; full deposited triangular fillet stock',dimensions=dict(legM=.012,totalLengthM=seams))
    item('installation tool allocation',1,D['toolsAllowanceKgPerModule'],A,'15kg charged per module and carried for comparison; torque tools/access/scaffolding completeness UNKNOWN')
    item('erection kit stock allocation',1,D['erectionAllowanceKgPerModule'],A,'12kg per module for four inherited-size lug/pin/base/bolt kits; full10528.0994855N each, no load dilution; attachment capacity UNKNOWN')

    replacement=set(D['retirementRows']);reconciliation=[];kept=[]
    for i,row in enumerate(B['mass']['newItems']):
        removed=i in replacement
        reconciliation.append(dict(sourceIndex=i,sourceRow=row,selectedDisposition='removed for failing selected replacement' if removed else 'kept or reassigned unchanged',selectedRemovedT=row['massT'] if removed else 0.0,qualifiedRetirementT=0.0,replacementDuty=('New direct split cassette, AD plate, ring/clamp bridges, continuous button support and fully charged attachment stock' if removed else row['duty'])))
        if not removed:
            # Conservative explicit centroid allocation, not a measured mass centre.
            p=centre;route='A'
            if row['item'].startswith('main carbon '):
                member=next(m for m in G['members'] if m['name']==row['item'].split()[-1]);p=mid(*member['pinCentresXRT'])
            elif row['item'].startswith('canted stanchion row '):
                k=int(row['item'].split()[-1])-1;st=G['stanchions'][k]
                p=st.get('sourceXRT',centre)
            elif 'root adapter' in row['item'] or 'root datum' in row['item']:p=dnode
            kept.append(dict(sourceIndex=i,sourceRow=row,massPerModuleKg=row['massT']*1000/repeat,centreXRTm=p,gravityReceiver=route,duty='Retained charged I024 stock; centroid/route is an explicit conservative local allocation, not installed mass validation.'))
    newkg=sum(x['massPerModuleKg'] for x in bill);keptkg=sum(x['massPerModuleKg'] for x in kept)
    removedT=sum(x['selectedRemovedT'] for x in reconciliation);newT=newkg*repeat/1000
    hull=B['mass']['hullT']-removedT+newT;gas=B['mass']['residualGasOnceT'];subtotal=hull+gas
    retentionHull=B['mass']['hullT']+newT
    margins=[dict(altitudeM=x['altitudeM'],fixedVolumeLiftT=x['liftT'],selectedKnownMarginT=x['liftT']-subtotal,
                  predecessorKnownMarginT=x['knownMarginT'],deltaT=x['liftT']-subtotal-x['knownMarginT'],
                  noRetirementKnownMarginT=x['liftT']-(retentionHull+gas)) for x in B['mass']['at']]
    mass=dict(previousHullT=B['mass']['hullT'],previousStockT=B['mass']['newAddedT'],newCassetteStockT=newT,
              retainedI024StockT=keptkg*repeat/1000,selectedRemovedI024StockT=removedT,qualifiedRetirementT=0,
              knownHullT=hull,residualGasOnceT=gas,knownSubtotalT=subtotal,additionalUCt=None,
              marginExpression='selectedKnownMarginT - additional U+C; equipment/payload/mission obligations remain unpriced UNKNOWN, not zero or removed',
              noRetirementHullT=retentionHull,noRetirementSubtotalT=retentionHull+gas,at=margins,
              selectedVolumeM3=B['mass']['selectedVolumeM3'],displacementChangeM3=0,
              newItems=bill,priorRows=reconciliation,keptStockGravity=kept,
              olderHullAndContingencies='Entire pre-I0245313.920567044793t remains in the mass basis. No earlier active or inactive row retired. Their global gravity/stability allocation is outside this local interface model and remains UNKNOWN.',
              selectedStockGravityKgPerModule=newkg+keptkg,
              qualification='Selected failing alternative bill and separate no-retirement accounting bound; never sum them. Neither is an installed saving or all-up vehicle budget.')

    # Analytic normal-projection bounds isolate the long cheeks from actual
    # curved ring walls over the full plate tangential interval, not a point.
    ringchecks=[]
    for name,P,size in [('D',dnode,.4),('C',cnode,.2)]:
        radius=P[1];tmax=.6
        rlow=math.sqrt(max(0,(radius-size/2)**2-tmax*tmax));rhigh=radius+size/2
        signed=[dot(sub([P[0]+xx,rr,0],dnode),n) for xx in (-size/2,size/2) for rr in (rlow,rhigh)]
        gap=halfgap-max(abs(x) for x in signed)
        ringchecks.append(dict(ring=name,actualSizeM=size,wallM=.025 if name=='D' else .02,
                   tangentialCoveredIntervalM=[-.6,.6],wallNormalProjectionBoundsM=[min(signed),max(signed)],
                   cheekInnerFaceAbsNormalM=halfgap,minimumProvedNormalClearanceM=gap,status='PASS' if gap>0 else 'UNKNOWN',
                   scope='Both whole cheeks against this wall within their full tangential interval only; clamps deliberately contact the wall. Other bodies and loaded shape not certified.'))
    adfit=dict(blankLengthM=adlength,blankWidthM=.28,blankThicknessM=.08,pinCentresXRTm=[adp,adq],
               axisXRT=ad['axisXRT'],pinAxisXRT=ad['pinAxisXRT'],boreM=.102,
               endLigamentM=.14-.051,minimumNetWidthAtBoreM=.28-.102,netAreaAtBoreM2=(.28-.102)*.08,
               continuousSection=True,blankContainsPlate=True,oldZeroAreaShoulderRetiredOnlyInSelectedBill=True,
               qualification='Full constant-section rectangular plate around two bores; no disconnected tangent shoulder. Existing AD-A pin/BD-carbon collision is unchanged.')
    # A previously witnessed overlap remains a valid counterexample because
    # both the occupied AD-A pin and BD carbon stay byte-identical in geometry.
    retained_witness=dict(pointXRTm=[77.720772,11.291868,-.175395],bodies=['AD A pin','BD carbon'],status='FAIL',
                         provenance='I024 saved finite witness retained for unchanged pin and carbon; no claim that sampled rounded coordinates are a new independent witness computation.')
    access=[]
    for root in G['roots']:
        p=root['pinXRT'];axis=root['pinAxisXRT'];travel=.3;pinhalf=.11
        access.append(dict(pin=root['member']+'-'+root['node'],axisXRT=axis,occupiedEndsXRTm=[add(p,mul(axis,-pinhalf)),add(p,mul(axis,pinhalf))],
                    insertionSweptEndpointsXRTm=[add(p,mul(axis,-pinhalf)),add(p,mul(axis,pinhalf+travel))],
                    sweptRadiusM=.05,toolCylinderRadiusM=.075,toolAxialExtraM=.15,
                    status='FAIL' if root['member']=='AD' and root['node']=='A' else 'UNKNOWN',
                    reason='Retained AD-A/BD carbon obstruction' if root['member']=='AD' and root['node']=='A' else 'Finite envelope declared; complete swept material/neighbor/tool proof not established'))
    # C cheek tangential extent overlaps adjacent-sector bounds; do not call
    # this a solid collision without a material point witness.
    pitch=2*nodes['C'][1]*math.sin(math.pi/37)
    clearance=dict(ringWallIsolation=ringchecks,ad=adfit,retainedAssemblyFailure=retained_witness,pinAccess=access,
              receiverClampBoreM=.332,actualCuffODm=.328,paidLinerRadialM=.002,cuffFiniteLengthM=.4,clampLengthM=.36,
              clampAxialEndAllowanceEachM=.02,clampRemoval='Withdraw inner/outer half along -X/+X after unloading and removing all pins/ties; no sleeve axial-through-ring insertion.',
              assemblySequence=['Preserve source geometry; remove only enumerated replaced active stock after independent unloading/support (capacity UNKNOWN).',
                'Offer open A/B half clamps along +/-X around328mm cuff with2mm liners; fit external doublers and outside-wall root ties.',
                'Offer inner cheek along -normal and outer cheek along +normal; ring-wall bounds below cover only the long plates.',
                'Fit the eight cross spacers outside the ring sections, D/C contact plates/liners/ties, and their short bridges.',
                'Attach retained forks to new arms; offer continuous AD plate and insert each pin through its recorded sweep before retainers.',
                'Connect the full-length button box, retaining all film/post hardware and failures; torque exposed fasteners before closing covers.',
                'Attempt is FAIL at AD-A access; other sequences, curved fits, neighboring sectors and installed clearance remain UNKNOWN.'],
              neighborCChordPitchM=pitch,cheekTangentialWidthM=1.2,neighborCheekBoundsOverlap=1.2>pitch,
              neighborMaterialClearance=None,combinedAssembly='FAIL',allSweepsCertified=False)

    # Carry pressure wrenches from saved data. Every old endpoint and demand
    # is unchanged; the changed receiver route shifts moments at actual points.
    cases=[];allmodules=[];maxnormal=0.;maxbolttension=0.;maxboltshear=0.;max_force_res=0.;max_moment_res=0.
    gravityrows=[dict(item=x['item'],massKg=x['massPerModuleKg'],point=x['centreXRTm'],receiver=x['gravityReceiver']) for x in bill]
    gravityrows += [dict(item=x['sourceRow']['item'],massKg=x['massPerModuleKg'],point=x['centreXRTm'],receiver=x['gravityReceiver']) for x in kept]
    for src in B['loadCases']:
        f=src['radialFraction'];loads=[];ports=[];rootrecords=[]
        # Individual main roots; old aggregate ring demand minus these roots
        # becomes an explicitly separately assigned wall input.
        node_wrenches={name:dict(F=Z[:],MO=Z[:]) for name in ('D','C')}
        for k,root in enumerate(src['rootScreens']):
            a=rootarms[k];P=a['pinXRTm'];F=root['forceOnRootXRTn'];M=root['coupleAtPinXRTnm'];Q=a['lastXRTm']
            mo=moment_at(F,M,P,O);mq=moment_at(F,M,P,Q)
            if root['node'] in node_wrenches:
                nw=node_wrenches[root['node']];nw['F']=add(nw['F'],F);nw['MO']=add(nw['MO'],mo)
            loads.append(dict(name=a['name'],point=Q,F=F,M=mq,receiver=a['receiver']))
            screen=beam_screen(F,moment_at(F,M,P,a['firstXRTm']),a['axisXRT'],a['lengthM'],.20,.02)
            connection=bolt_group(F,mq,Q,a['axisXRT'],[[-.06,-.06],[-.06,.06],[.06,-.06],[.06,.06]],.024,.020,.12,.062)
            rootrecords.append(dict(member=a['name'],sourcePinXRTm=P,sourceForceXRTn=F,sourceCoupleXRTnm=M,
                 deliveredPointXRTm=Q,deliveredCoupleXRTnm=mq,pressureSection=screen,secondFoot=connection,
                 oppositeFirstFootForceXRTn=mul(F,-1),oppositeFirstFootCoupleXRTnm=mul(moment_at(F,M,P,a['firstXRTm']),-1)))
        for a in nodearms:
            name=a['node'];source=src['nodeDCollectorInput' if name=='D' else 'nodeCCollectorInputWithoutButton']
            F=sub(source['forceXRTn'],node_wrenches[name]['F']);MO=sub(source['momentAboutOXRTnm'],node_wrenches[name]['MO'])
            P=a['firstXRTm'];Q=a['lastXRTm'];MP=sub(MO,cross(sub(P,O),F));MQ=moment_at(F,MP,P,Q)
            loads.append(dict(name=name+' boundary remainder',point=Q,F=F,M=MQ,receiver='A'))
            nd=D['nodeRingClamp'];pattern=nd[name+'patternRTm'];size=.4 if name=='D' else .2
            ports.append(dict(node=name,forceXRTn=F,momentAboutOXRTnm=MO,sourceWallPointXRTm=P,coupleAtWallXRTnm=MP,
                deliveredPointXRTm=Q,deliveredCoupleXRTnm=MQ,section=beam_screen(F,MP,a['axisXRT'],a['lengthM'],.2,.02),
                tieGroup=bolt_group(F,MP,P,[1,0,0],pattern,.03,.025,.60,size+.04+.006+.024),
                wallRotationContactAndSlipCapacity=None))
        bs=src['button'];a=buttonarm;F=bs['forceXRTn'];M=bs['coupleXRTnm'];P=bs['datumXRT'];Q=a['lastXRTm'];mq=moment_at(F,M,P,Q)
        loads.append(dict(name='separate button',point=Q,F=F,M=mq,receiver='A'))
        button=dict(sourceXRTm=P,forceXRTn=F,sourceCoupleXRTnm=M,receiverXRTm=Q,receiverCoupleXRTnm=mq,
                    cutLengthM=a['lengthM']-.020,chargedLengthM=a['lengthM'],plateFaceGapEachM=0,
                    sectionEnds=[beam_screen(F,m,a['axisXRT'],a['lengthM'],.30,.016) for m in (M,mq)],
                    feet=[bolt_group(F,m,p,a['axisXRT'],[[-.16,-.16],[-.16,0],[-.16,.16],[0,-.16],[0,.16],[.16,-.16],[.16,0],[.16,.16]],.024,.020,.14,.08) for p,m in ((P,M),(Q,mq))],
                    curvedShellConnectionAndInheritedButtonStripCapacity=None)
        pressureF=total([x['F'] for x in loads]);pressureMO=total([moment_at(x['F'],x['M'],x['point'],O) for x in loads])
        pressureResidual=dict(forceN=norm(sub(pressureF,src['totalAppliedForceXRTn'])),momentNm=norm(sub(pressureMO,src['totalAppliedMomentAboutOXRTnm'])))
        # Unit loads have inherited upstream hoop reactions already allocated.
        # Aggregate input includes the separate incoming boundary. No whole-end load.
        case=dict(radialFraction=f,pressureBoundaryResidual=pressureResidual,rootMembers=rootrecords,ringPorts=ports,
             button=button,pressureLoadsOnCheek=loads,sourceTotalForceXRTn=src['totalAppliedForceXRTn'],
             sourceTotalMomentAboutOXRTnm=src['totalAppliedMomentAboutOXRTnm'],
             adAxialTensionN=src['memberSignedTensionN']['AD'],adNetStressPa=abs(src['memberSignedTensionN']['AD'])/adfit['netAreaAtBoreM2'],
             qualification='Prescribed static source wrenches from unchanged pin topology; not stiffness-derived repartition or global sufficiency.')
        cases.append(case)
        for sector in range(37):
            angle=2*math.pi*sector/37;g=[0,-D['gMps2']*math.cos(angle),D['gMps2']*math.sin(angle)]
            gl=[]
            for x in gravityrows:
                F=mul(g,x['massKg']);P=x['point'];Q=P
                if x['item']=='cassette outer cheek':Q=spacers[0]['lastXRTm']
                gl.append(dict(name=x['item'],point=Q,F=F,M=cross(sub(P,Q),F),receiver=x['receiver']))
            # All stock gravity is a finite wrench at its declared centroid.
            # Transfer to the receiver is recorded without cancelling its lever.
            receivers=[]
            for name,Q in [('A',A),('B',BB)]:
                relevant=[x for x in loads+gl if x['receiver']==name]
                force=total([x['F'] for x in relevant]);couple=total([moment_at(x['F'],x['M'],x['point'],Q) for x in relevant])
                rootbolts=bolt_group(force,couple,Q,[1,0,0],D['clampTiePatternRTm'],.03,.025,.52,.44+.04+.024)
                bridge=next(x for x in receiverarms if x['name']==name+' receiver bridge -1')
                mc=moment_at(force,couple,Q,bridge['firstXRTm'])
                screen=beam_screen(force,mc,bridge['axisXRT'],bridge['lengthM'],.30,.02)
                maxnormal=max(maxnormal,screen['normalEnvelopePa']);maxbolttension=max(maxbolttension,rootbolts['maximumTensionPa']);maxboltshear=max(maxboltshear,rootbolts['maximumShearPa'])
                receivers.append(dict(name=name,datumXRTm=Q,forceXRTn=force,coupleXRTnm=couple,
                    requiredOppositeReactionForceXRTn=mul(force,-1),requiredOppositeReactionCoupleXRTnm=mul(couple,-1),
                    rootTies=rootbolts,innerBridgeSection=screen,
                    forceOnlyProjectedContactPa=norm(force)/(.36*.328),
                    requiredFrictionCoefficient=None,rotationStiffness=None,completeRingAndClampCapacity=None))
            allF=total([x['F'] for x in loads+gl]);allMO=total([moment_at(x['F'],x['M'],x['point'],O) for x in loads+gl])
            rf=total([x['forceXRTn'] for x in receivers]);rm=total([moment_at(x['forceXRTn'],x['coupleXRTnm'],x['datumXRTm'],O) for x in receivers])
            fres=norm(sub(allF,rf));mres=norm(sub(allMO,rm));max_force_res=max(max_force_res,fres);max_moment_res=max(max_moment_res,mres)
            # All pressure and selected local gravity are conservatively routed
            # through the inner cheek to their named receiver station. This is
            # a wrench envelope, not a spring-derived parallel sharing rule.
            cuts=[]
            stations_s=sorted(set([dot(sub(x['point'],dnode),e) for x in loads+gl]+[dot(sub(A,dnode),e),dot(sub(BB,dnode),e),-.6,norm(sub(cnode,dnode))+.6]))
            reactions=[dict(point=x['datumXRTm'],F=mul(x['forceXRTn'],-1),M=mul(x['coupleXRTnm'],-1)) for x in receivers]
            for st in stations_s:
                P=add(add(dnode,mul(e,st)),mul(n,-halfgap))
                for side in ('before','after'):
                    selected=[x for x in loads+gl+reactions if dot(sub(x['point'],dnode),e)<st-1e-10 or (side=='after' and dot(sub(x['point'],dnode),e)<=st+1e-10)]
                    F=total([x['F'] for x in selected]);M=total([moment_at(x['F'],x['M'],x['point'],P) for x in selected])
                    sc=beam_screen(F,M,e,length,1.2,.020,plate=True);maxnormal=max(maxnormal,sc['normalEnvelopePa'])
                    cuts.append(dict(stationM=st,side=side,datumXRTm=P,**sc))
            # Every actual local box gets its own full source force/couple plus
            # self-weight endpoint envelope. Loads on connections are conditional.
            memberGravity=[]
            for m in members:
                Fp=Z[:];Mp=Z[:]
                match=next((x for x in rootrecords if x['member']==m['name']),None)
                if match:Fp=match['sourceForceXRTn'];Mp=moment_at(Fp,match['sourceCoupleXRTnm'],match['sourcePinXRTm'],m['firstXRTm'])
                if m is buttonarm:Fp=bs['forceXRTn'];Mp=bs['coupleXRTnm']
                port=next((x for x in ports if m.get('node')==x['node']),None)
                if port:Fp=port['forceXRTn'];Mp=port['coupleAtWallXRTnm']
                # Receiver bridges already have the complete receiver load above.
                if m in receiverarms:
                    rr=next(x for x in receivers if x['name']==m['receiver'])
                    if m['name'].endswith('-1'):Fp=rr['forceXRTn'];Mp=moment_at(Fp,rr['coupleXRTnm'],rr['datumXRTm'],m['firstXRTm'])
                selfkg=rho*box_area(m['sizeM'],m['wallM'])*m['lengthM']
                already_in_receiver=m in receiverarms and m['name'].endswith('-1')
                FG=Z[:] if already_in_receiver else mul(g,selfkg)
                FGcentre=mid(m['firstXRTm'],m['lastXRTm'])
                if m is spacers[0]:
                    outer=next(x for x in bill if x['item']=='cassette outer cheek');fo=mul(g,outer['massPerModuleKg'])
                    Fp=add(Fp,fo);Mp=add(Mp,cross(sub(outer['centreXRTm'],m['firstXRTm']),fo))
                FF=add(Fp,FG)
                Ml=add(moment_at(Fp,Mp,m['firstXRTm'],m['lastXRTm']),cross(sub(FGcentre,m['lastXRTm']),FG))
                ends=[];feet=[]
                for end_index,(P,F,M) in enumerate(((m['firstXRTm'],Fp,Mp),(m['lastXRTm'],FF,Ml))):
                    sc=beam_screen(F,M,m['axisXRT'],m['lengthM'],m['sizeM'],m['wallM'])
                    maxnormal=max(maxnormal,sc['normalEnvelopePa']);ends.append(sc)
                    diameter=.03 if m in spacers else .024;core=.025 if m in spacers else .020
                    offsets=[[-.05,-.05],[-.05,.05],[.05,-.05],[.05,.05]] if m in spacers else [[-.06,-.06],[-.06,.06],[.06,-.06],[.06,.06]]
                    if m is buttonarm:offsets=[[-.16,-.16],[-.16,0],[-.16,.16],[0,-.16],[0,.16],[.16,-.16],[.16,0],[.16,.16]]
                    if m in spacers:
                        grip=.016+.020;stack='16mm spacer end plate +20mm cheek; bolt washers charged separately'
                    elif m in rootarms:
                        grip=.072 if end_index==0 else .062;stack='30mm mating plate +30mm retained fork base +12mm backer' if end_index==0 else '30mm mating plate +20mm cheek +12mm backer'
                    elif m in receiverarms:
                        grip=.040 if end_index==0 else .260;stack='20mm bridge plate +20mm cheek' if end_index==0 else '20mm bridge plate +20mm reinforcement +220mm clamp half blank; full through-grip lower bound, no free blind thread'
                    elif m is buttonarm:
                        grip=.080;stack='First:20plate+20pad+12shell+20backer+8packing; last:20plate+20pad+20cheek+20backer, all mm'
                    else:
                        grip=.040;stack='20mm node bridge foot +20mm ring contact plate or cheek; first-side nut clearance to ring remains UNKNOWN'
                    bg=bolt_group(F,M,P,m['axisXRT'],offsets,diameter,core,.14 if m is buttonarm else .12,grip)
                    foot={k:bg[k] for k in ('datumXRTm','boltCount','gripM','underHeadLengthM','nutWashersProjectionM','lengthAllowanceM','lengthPass','maximumTensionPa','maximumShearPa','forceResidualN','momentResidualNm','contactPryingSlipPreloadAndCombinedCapacity')}
                    foot.update(stack=stack,ringPenetrationNutToolClearance=None)
                    feet.append(foot)
                memberGravity.append(dict(member=m['name'],selfWeightKg=selfkg,ownWeightAlreadyInReceiverDemand=already_in_receiver,firstAppliedForceXRTn=Fp,firstAppliedCoupleXRTnm=Mp,lastDeliveredForceXRTn=FF,lastDeliveredCoupleXRTnm=Ml,endpoints=ends,independentFeet=feet,
                    qualification='Local own-stock gravity screen; complete receiver and inner-cheek envelopes separately include all paid retained/new local stock. No connection load distribution inferred from this member screen.'))
            outer=next(x for x in bill if x['item']=='cassette outer cheek');of=mul(g,outer['massPerModuleKg'])
            outerM=cross(sub(outer['centreXRTm'],spacers[0]['firstXRTm']),of)
            outerScreen=beam_screen(of,outerM,e,length,1.2,.02,plate=True)
            maxnormal=max(maxnormal,outerScreen['normalEnvelopePa'])
            local=dict(radialFraction=f,sector=sector,angleRad=angle,gravityLocalMps2=g,knownLocalStockKg=newkg+keptkg,
                       gravityForceXRTn=total([x['F'] for x in gl]),gravityMomentAboutOXRTnm=total([moment_at(x['F'],x['M'],x['point'],O) for x in gl]),
                       receivers=receivers,cheekMaximumNormalPa=max(x['normalEnvelopePa'] for x in cuts),cheekControllingCut=max(cuts,key=lambda x:x['normalEnvelopePa']),cheekCutCount=len(cuts),outerCheekOwnWeightAtSpacerD=outerScreen,
                       memberOwnWeightScreens=memberGravity,forceResidualN=fres,momentResidualNm=mres)
            allmodules.append(local)
    # Both caps use these37 local orientations. Reflection in X acts as an
    # ordinary vector on forces and as det(Q)Q on couples; no second load is added.
    reflection=dict(moduleCount=74,rightCapSectorRecords=37,radialAssignments=2,
                    rightMap='(X,R,T) -> (X,R cos(theta)-T sin(theta),R sin(theta)+T cos(theta))',
                    leftPositionAndForce='Reflect X, then rotate R/T',leftCouple='(Mx,Mr,Mt)->(Mx,-Mr,-Mt), then rotate R/T',
                    pressureAndGravityUseSameTransform=True,oppositeCapInstalledQualification=None)
    remaining=B['mass']['hullT']-hull
    result=dict(unit='R3-I029',baselineSha256=sha(U/'baseline.json'),sourcesSha256=sha(U/'sources.json'),
                selectedHypothesis='Two removable cheeks, finite spacers and direct split receiver clamps replace the stacked collector/yokes; one continuous AD plate replaces disconnected cartridge stock.',
                geometry=dict(cheeks=cheeks,cheekAxisXRT=e,cheekNormalXRT=n,cheekLengthM=length,members=members,receiverClamps=clamps,ringNodes=nodes,ad=adfit,repeat=reflection),
                fixedPressureAndFilm=B['unchangedPressureAndFilm'],mass=mass,clearance=clearance,pressureCases=cases,
                gravityCases=allmodules,localStockGravitySources=gravityrows,
                summary=dict(selectedNewStockT=newT,selectedRemovedT=removedT,hullDeltaT=hull-B['mass']['hullT'],knownSubtotalT=subtotal,
                    selectedMarginsT=[x['selectedKnownMarginT'] for x in margins],marginDeltaT=remaining,
                    maximumConditionalSectionNormalPa=maxnormal,maximumReceiverBoltTensionPa=maxbolttension,maximumReceiverBoltShearPa=maxboltshear,
                    maximumForceClosureResidualN=max_force_res,maximumMomentClosureResidualNm=max_moment_res,
                    receiverTieGripM=.504,receiverTieRequiredUnderHeadM=.504+2*(.03/6)+.8*.03+.4*.03,receiverTieSelectedLengthM=.52,
                    geometryStatus='FAIL',nominalStrengthStatus='FAIL' if maxnormal>355e6 else 'UNKNOWN',physicalFloat=None),
                weakestAssumption='The direct split receiver clamp can transmit the complete vector couple into the existing ring wall without dominating reinforcement; contact, rotation and stiffness are UNKNOWN.',
                sensitivity=dict(marginChangeTPerAdditionalT=-1,marginChangeTPerAdditionalKgPerModule=-.074,
                    remainingSelectedSavingT=remaining,additionalStockKgPerModuleToEraseSaving=max(0,remaining)*1000/74,ringRotationSensitivity=None,
                    qualification='Algebraic mass allowance only, not a second geometry/material case or a lower bound on required reinforcement.'),
                nextDesignChange='Replace the long plate-cheek moment route with a triangulated receiver-bypass load path to two separated existing frame stations, retaining the same paid full pressure and gravity duties; this is untested.',
                inheritedFailures=['Film tensile68.639MPa versus50MPa proxy','Finite button strip22798.125MPa nominal failure','AD-A pin/BD-carbon interference','Post socket rows1-3, finite cuff rows1-8 and carbon cuff footprint rows1/17','Barrel/mid-cap construction and non-replaced erection failures','Global pressure capacity, loaded shape, installed equilibrium, all-up U+C and physical float UNKNOWN'],
                unresolved=['Ring contact/preload/friction/rotation/compliance and global transfer','Neighbor-sector cassette overlap bounds and complete pin/tool sweeps','Root-arm plate angle/miter contact and weld interaction','Gross-cheek cutout/local-buckling/open-section torsion capacity','Retained stock centroid/gravity-routing assumption and earlier hull/global gravity allocation','Equipment, payload, mission hardware and complete installation U+C'],
                computation=dict(newGeometryCount=1,radialAssignments=[0,1],scalarVectorOnly=True,matrixOrder=0,parameterSweeps=0,ancestorImports=0,ancestorExecutions=0,numericalInvocation='This --write call; governed tip binding uses exact source/output hashes, not a claimed tip rerun.'),
                qualification='Failing selected stock alternative with a separate no-retirement bound. Wrench bookkeeping and individual nominal comparisons establish no installed structure, qualified retirement, float confidence or global pressure resistance.')
    # Post-calculation invariant failures are scientific attempts, not controls.
    assert all(x['pressureBoundaryResidual']['forceN']<1e-5 and x['pressureBoundaryResidual']['momentNm']<1e-3 for x in cases), 'Saved pressure boundary not closed'
    assert max_force_res<1e-4 and max_moment_res<1e-2, 'Receiver wrench transfer not closed'
    assert abs(removedT+keptkg*74/1000-B['mass']['newAddedT'])<1e-8, 'Old rows partition'
    path=U/'cassette.json'
    # Compact data serialization avoids duplicating presentation whitespace;
    # all physical values and records are retained, with tables in the README.
    with path.open('w') as out:json.dump(result,out,separators=(',',':'),allow_nan=False);out.write('\n')
    print(json.dumps(result['summary'],indent=2),flush=True)
    print('SCIENCE_COMPLETED',flush=True)

if __name__=='__main__': main()
