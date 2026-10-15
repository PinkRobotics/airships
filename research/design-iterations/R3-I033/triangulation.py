#!/usr/bin/env python3
"""One frozen, bending-capable two-side-frame construction; no stiffness solver.

Read only saved predecessor data. All geometry, mass and wrench arithmetic is
inside this one program. UNKNOWN is null, never zero or a hidden equal split.
The output records finite failures without tuning the issued construction.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

U=Path(__file__).resolve().parent
R=U.parents[2]
Z=[0.,0.,0.]
X=[1.,0.,0.]
T=[0.,0.,1.]
XYZ=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]
O=[40.,0.,0.]

def add(a,b):return [a[i]+b[i] for i in range(3)]
def sub(a,b):return [a[i]-b[i] for i in range(3)]
def mul(a,s):return [v*s for v in a]
def dot(a,b):return sum(a[i]*b[i] for i in range(3))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
def mid(a,b):return mul(add(a,b),.5)
def total(vs):return [sum(v[i] for v in vs) for i in range(3)]
def transport(F,M,p,q):return add(M,cross(sub(p,q),F))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frame(e):
    e=unit(e);seed=X if norm(cross(T,e))<1e-12 else T
    v=unit(cross(seed,e));return [e,v,cross(e,v)]
def global_point(p,sector,opposite=False):
    a=2*math.pi*sector/37;c=math.cos(a);s=math.sin(a)
    return [-p[0] if opposite else p[0],c*p[1]-s*p[2],s*p[1]+c*p[2]]
def global_force(v,sector,opposite=False):return global_point(v,sector,opposite)
def global_couple(v,sector,opposite=False):
    return global_point([v[0],-v[1],-v[2]] if opposite else v,sector,False)
def obb(name,centre,axes,dims,role):return dict(id=name,centre=centre,axes=axes,dimensions=dims,role=role)
def corners(box):
    return [add(box['centre'],total([mul(box['axes'][i],sg[i]*box['dimensions'][i]/2) for i in range(3)])) for sg in [(a,b,c) for a in [-1,1] for b in [-1,1] for c in [-1,1]]]
def overlap(a,b):
    """Strict positive intersection of two solid rectangular prisms by SAT."""
    delta=sub(b['centre'],a['centre']);axes=a['axes']+b['axes']+[cross(x,y) for x in a['axes'] for y in b['axes']]
    least=None
    for ax in axes:
        if norm(ax)<1e-10:continue
        ax=unit(ax)
        ra=sum(abs(dot(ax,a['axes'][i]))*a['dimensions'][i]/2 for i in range(3))
        rb=sum(abs(dot(ax,b['axes'][i]))*b['dimensions'][i]/2 for i in range(3))
        d=ra+rb-abs(dot(delta,ax))
        if d<=1e-9:return None
        least=d if least is None else min(least,d)
    return least

def line_box(point,direction,box):
    lo=-float('inf');hi=float('inf');q=sub(point,box['centre'])
    for axis,size in zip(box['axes'],box['dimensions']):
        u=dot(q,axis);v=dot(direction,axis)
        if abs(v)<1e-12:
            if abs(u)>size/2:return None
        else:
            a=(-size/2-u)/v;b=(size/2-u)/v
            lo=max(lo,min(a,b));hi=min(hi,max(a,b))
    return [lo,hi] if lo<=hi else None

def inside_saved(point,s):
    """Strict interior of saved box, annular tube/cylinder or curved box wall."""
    q=sub(point,s['centreXRT']);v=[dot(q,a) for a in s['axes']];d=s['dimensionsM'];k=s['kind'];eps=1e-7
    if k=='box':return all(abs(v[i])<d[i]/2-eps for i in range(3))
    if k in ['cylinder','tube']:
        rr=v[1]**2+v[2]**2;inner=s.get('innerDiameterM',0)/2
        return abs(v[0])<d[0]/2-eps and rr<(d[1]/2-eps)**2 and (inner==0 or rr>(inner+eps)**2)
    if k=='boxTube':
        # A missing wall dimension does not become filled solid.
        wall=s.get('wallM')
        if wall is None:return False
        return all(abs(v[i])<d[i]/2-eps for i in range(3)) and (abs(v[1])>d[1]/2-wall+eps or abs(v[2])>d[2]/2-wall+eps)
    if k=='ringbox':
        radial=math.hypot(v[1],v[2])-s['radiusM'];half=s['sizeM']/2;wall=s['wallM']
        return abs(v[0])<half-eps and abs(radial)<half-eps and (abs(v[0])>half-wall+eps or abs(radial)>half-wall+eps)
    return False

def main():
    assert sys.argv[1:]==['--write'],'Only the single frozen output is supported'
    B=json.loads((U/'baseline.json').read_text());S=json.loads((U/'sources.json').read_text());D=B['design'];G=B['inheritedGeometry'];rho=D['steelDensityKgM3'];repeat=D['repeatCount']
    assert repeat==74 and D['radialAssignments']==[0,1] and D['sectorsPerCap']==37
    for name,h in S['inputFiles'].items():assert sha(R/name)==h,'Saved input changed: '+name
    print('SCIENCE_STARTED: R3-I033; one issued construction; 2x37 keyed states; no solver',flush=True)
    datums={n:list(G['receivingFrameXRT'][n]) for n in ['A','B']}
    datums.update({n:list(G['nodesXRT'][n]) for n in ['C','D']})
    nodes={n+side:add(p,[D['nodeShiftXM'],0,t]) for n,p in datums.items() for side,t in zip(['-','+'],D['sideTM'])}
    saddles={n+'0':add(p,[D['nodeShiftXM'],0,0]) for n,p in datums.items()}
    roots={x['member']+'-'+x['node']:x for x in G['roots']}
    saved={x['name']:x for x in G['solids']}
    bill=[];welds=[];members=[];feet=[];nodeboxes=[];nodeplates=[];covers=[];saddle_records=[];receiver_records=[];adaptors=[];tube_walls=[]
    def stock(name,count,eachkg,p,duty,dimensions=None,body=None):
        key='new-'+str(len(bill));bill.append(dict(id=key,item=name,countPerModule=count,eachKg=eachkg,massPerModuleKg=count*eachkg,totalCount=count*repeat,massT=count*eachkg*repeat/1000,centreXRTm=p,dimensions=dimensions,body=body,duty=duty));return key
    def plate(name,count,dims,p,duty,body=None):return stock(name,count,rho*math.prod(dims),p,duty,dims,body)
    def weld(name,length,p,body,duty):
        key=stock(name,1,rho*.5*D['weldLegM']**2*length,p,duty,{'legM':D['weldLegM'],'lengthM':length},body)
        welds.append(dict(id=key,body=body,lengthM=length,legM=D['weldLegM'],centroidXRTm=p,duty=duty,installedJointStrength=None));return key
    M24=D['M24']
    m24kg=rho*(math.pi*M24['diameterM']**2*M24['lengthM']/4+math.sqrt(3)/2*(M24['headAFm']**2*M24['headHeightM']+M24['nutAFm']**2*M24['nutHeightM'])+M24['washers']*math.pi/4*(M24['washerODm']**2-M24['washerIDm']**2)*M24['washerThicknessM'])
    def old_bolt(d,length):
        return rho*(math.pi*d*d*length/4+math.sqrt(3)/2*(1.5*d)**2*(.65*d+.8*d)+2*math.pi/4*((1.85*d)**2-(1.1*d)**2)*(d/6))
    def m24sets(name,count,p,body):
        return [stock(name+' M24 complete sets',count,m24kg,p,'180mm shank, full hex head/nut blanks and two annular washers; thread root is an unqualified20mm demand proxy.',M24,body),plate(name+' independent backers',count,M24['backerM'],p,'One paid80x80x12 backer per new bolt; no pooling of opposed feet.',body)]
    for name,p in nodes.items():
        nodeboxes.append(obb(name,p,XYZ,[.5,.5,.5],'hollow cubical side node,20mm walls; mitred corners, full blanks paid'))
        for ax in range(3):
            for sign in [-1,1]:
                c=add(p,mul(XYZ[ax],sign*.24));dims=[.5,.5,.5];dims[ax]=.02
                key=plate(name+f' wall {ax}/{sign}',1,[.5,.5,.02],c,'Full500x500x20 blank; corners mitred without trim credit.',name)
                nodeplates.append(dict(id=key,node=name,axis=ax,sign=sign,centreXRTm=c,fullBlankM=[.5,.5,.02],material='Cube shell: max(abs(local X/R/T)) in[.23,.25]; mitred partition, no double corner material.'))
        cp=add(p,[-.256,0,0]);cover=plate(name+' removable cover',1,D['coverM'],cp,'Negative-X removable300x300x12 cover. Aperture and four-hole spacing unspecified: access and local cutout section UNKNOWN.',name)
        bolts=stock(name+' cover M12 sets',4,old_bolt(.012,.080),cp,'80mm M12 shank; inherited head1.5d AF,0.65d high/nut0.8d; two washers1.85d OD/1.1d ID,d/6 thick. No certified fastener capacity.',D['coverBolts'],name)
        covers.append(dict(node=name,cover=cover,bolts=bolts,solid=obb(cover,cp,XYZ,[.012,.30,.30],'removable cover'),apertureM=None,boltCentres=None,toolPath=None,status='UNKNOWN'))
        weld(name+' twelve box seams',12*.5,p,name,'Twelve finite500mm cube edges; mitred full blanks. Penetration, distortion and fatigue UNKNOWN.')
    for name,p in saddles.items():
        ids=[];plate_solids=[]
        for sign in [-1,1]:
            cp=add(p,[sign*.1125,0,0]);ids.append(plate(name+f' saddle plate {sign}',1,[.4,.4,.025],cp,'Plate normal follows X source/standoff axis around continuous T crosshead.',name));plate_solids.append(obb(name+f'-plate{sign}',cp,XYZ,[.025,.4,.4],'saddle plate'))
        # Only issued blank dimensions are instantiated. An unissued placement
        # cannot silently become a fabricated load introduction detail.
        ids.append(plate(name+' saddle webs',2,[.4,.2,.020],p,'Two full web blanks paid; exact mating cut/placement and torsional load path UNKNOWN.',name))
        ids.append(plate(name+' saddle gussets',4,[.2,.2,.020],p,'Four full gusset blanks paid; installed placement/cut/attachment UNKNOWN.',name));ids+=m24sets(name+' saddle',8,p,name)
        weld(name+' saddle plate edge allowance',2*2*(.4+.4),p,name,'Full finite plate perimeters charged; installed contact/weld path remains UNKNOWN.')
        weld(name+' saddle web edge allowance',2*2*(.4+.2),p,name,'Two400x200 full web perimeters; no assumed hidden web transfer.')
        weld(name+' saddle gusset edge allowance',4*2*(.2+.2),p,name,'Four200x200 full gusset perimeters; installed junctions unspecified.')
        saddle_records.append(dict(id=name,pointXRTm=p,normalXRT=X,plateSolids=plate_solids,stockIDs=ids,continuousCrosshead=True,hinge=False,webAndGussetPlacement=None,boltCentres=None,distortionContactRotation=None,status='UNKNOWN'))
    for name in ['A','B']:
        p=datums[name];ids=[];doubles=[]
        for sign in [-1,1]:
            cp=add(p,[sign*.2525,0,0]);ids.append(plate(name+f' added receiver doubler {sign}',1,D['receiverDoublerM'],cp,'Outside retained220mm half blank and20mm reinforcement; no cuff-wall strength claim.',name));doubles.append(obb(name+f'-doubler{sign}',cp,XYZ,[.025,.600,.400],'receiver doubler'))
            weld(name+f' doubler perimeter {sign}',2*(.6+.4),cp,name,'Full600x400 perimeter,12mm fillet stock; ring/curved contact capacity UNKNOWN.')
        ids.append(plate(name+' receiver gussets',4,D['receiverGussetM'],p,'Four250x250x20 full blanks paid between standoff flange and clamp; exact installed cuts/placement and rotation restraint UNKNOWN.',name))
        weld(name+' receiver gusset edge allowance',4*2*(.25+.25),p,name,'Four250mm square blank perimeters; no unenumerated weld capacity assumed.')
        ties=stock(name+' replacement M30x700 sets',4,old_bolt(.030,.700),p,'Replace exactly four old520mm sets; identical inherited head/nut/two-washer stock, changed shanks. Old eight tie backers remain charged.',{'diameterM':.030,'underHeadLengthM':.700,'headAFm':.045,'headHeightM':.0195,'nutAFm':.045,'nutHeightM':.024,'washerODm':.0555,'washerIDm':.033,'washerThicknessM':.005,'washers':2},name);ids.append(ties)
        grip=.44+.04+.05+.024;projection=.010+.024+.012
        receiver_records.append(dict(id=name,pointXRTm=p,cuffGeometry='baseline.inheritedGeometry.solids: '+name+' receiving cuff',oldContactKit='baseline.retainedI029Geometry.receiverClamps',doublerSolids=doubles,stockIDs=ids,tiePatternRTm=[[-.22,-.12],[-.22,.12],[.22,-.12],[.22,.12]],tieGripM=grip,nutWashersThreadProjectionM=projection,tieLengthM=.700,tieLengthAllowanceM=.700-grip-projection,lengthOnlyStatus='PASS' if .700>=grip+projection else 'FAIL',installedLengthAndAccessStatus='UNKNOWN',sourceBody='Frame/clamp reaction acting on this module',forceXRTn=None,coupleXRTnm=None,ringBearingPeelSlipPryingRotationCapacity=None,additionalReinforcementMassT=None))
    specs=[]
    for side in ['-','+']:
        for a,b in D['sideEdges']:specs.append((a+side+'--'+b+side,a+side,b+side,'main',.20,.012,None))
    for n in D['crossheads']:specs.append(('crosshead-'+n,n+'-',n+'+','crosshead',.20,.012,None))
    for a,b in D['diagonals']:specs.append(('diagonal-'+a+'--'+b,a,b,'diagonal',.20,.012,None))
    for root,target in D['rootTargets'].items():specs.append(('root-'+root,'fork-'+root,target,'root',.20,.012,root))
    for n in ['D','C']:specs.append(('boundary-'+n,'source-'+n,n+'0','boundary',.20,.012,n))
    specs.append(('button','source-button','C0','button',.30,.016,'button'))
    for n in ['A','B']:specs.append(('receiver-'+n,n+'0','receiver-'+n,'receiver',.30,.016,n))
    assert len(specs)==31
    def point(label):
        if label in nodes:return nodes[label]
        if label in saddles:return saddles[label]
        if label.startswith('fork-'):return roots[label[5:]]['forkBaseXRT']
        if label=='source-button':return G['buttonSupport']['sourceXRT']
        return datums[label.split('-')[-1]]
    def attachment(label,p,e):
        if label in nodes:
            ax=max(range(3),key=lambda i:abs(e[i]));offset=.25/abs(e[ax]);normal=mul(XYZ[ax],1 if e[ax]>0 else -1)
            return dict(kind='node',offsetM=offset,normal=normal,substrateM=.020,material=label,fullFaceContact=abs(dot(e,normal))>1-1e-10)
        if label in saddles:
            offset=.125/max(abs(e[0]),1e-12)
            return dict(kind='saddle',offsetM=offset,normal=mul(X,1 if e[0]>0 else -1),substrateM=.025,material=label,fullFaceContact=abs(e[0])>1-1e-10)
        if label.startswith('fork-'):
            root=roots[label[5:]];name=root['member']+' fork base '+root['node'];s=saved[name];normal=s['axes'][0]
            # Actual outward support plane of the old finite base along e.
            offset=sum(abs(dot(e,a))*d/2 for a,d in zip(s['axes'],s['dimensionsM']))
            return dict(kind='fork',offsetM=offset,normal=normal,substrateM=.030,material=name,fullFaceContact=abs(dot(e,normal))>1-1e-10)
        if label.startswith('receiver-'):
            return dict(kind='receiver',offsetM=.265,normal=mul(e,-1),substrateM=.025,material=label,fullFaceContact=True)
        if label in ['source-D','source-C']:
            n=label[-1];size=.4 if n=='D' else .2
            return dict(kind='boundary',offsetM=size/2+.003+.020+.020,normal=e,substrateM=.020,material=n+' retained ring contact plate +new20mm adaptor',fullFaceContact=True)
        return dict(kind='button',offsetM=.020,normal=None,substrateM=None,material='Retained finite button source contact, packing and new20mm adaptor',fullFaceContact=None)
    for ident,a,b,kind,size,wall,key in specs:
        p=point(a);q=point(b);e=unit(sub(q,p));length=norm(sub(q,p));mass=rho*(size**2-(size-2*wall)**2)*length
        sid=stock(ident+' centre-to-centre RHS stock',1,mass,mid(p,q),'Full centre-to-centre steel stock paid; physical cut faces exclude feet/node bodies; all trim stays charged at this bookkeeping centroid.',[length,size,wall],ident)
        endrecords=[]
        for j,label,pp,ee in [(0,a,p,e),(1,b,q,mul(e,-1))]:
            at=attachment(label,pp,ee);basis=frame(ee);fpoint=add(pp,mul(ee,at['offsetM']));cp=add(fpoint,mul(ee,.0125));fid=ident+':end'+str(j)
            plateid=plate(fid+' end plate',1,D['endPlateM'],cp,'Independent350x350x25 full blank; no contact area shared with opposite series foot.',ident)
            offsets=D['forkPatternVWm'] if at['kind']=='fork' else D['genericPatternVWm'];hardware=m24sets(fid,len(offsets),cp,ident)
            holes=[]
            for h,(v,w) in enumerate(offsets):
                hp=add(fpoint,add(mul(basis[1],v),mul(basis[2],w)));material_status='UNKNOWN';witness=None
                if at['kind']=='node':
                    box=next(z for z in nodeboxes if z['id']==label);interval=line_box(hp,mul(ee,-1),box)
                    if interval is None or interval[1]<0:material_status='FAIL'
                    else:
                        witness=add(hp,mul(ee,-max(0,interval[0])));material_status='GEOMETRIC INTERSECTION ONLY'
                elif at['kind']=='fork':
                    old=saved[at['material']];bb=obb(at['material'],old['centreXRT'],old['axes'],old['dimensionsM'],'retained finite fork base');interval=line_box(hp,mul(ee,-1),bb)
                    if interval is None or interval[1]<0:material_status='FAIL'
                    else:witness=add(hp,mul(ee,-max(0,interval[0])));material_status='GEOMETRIC INTERSECTION ONLY'
                elif at['kind']=='receiver':
                    local=sub(hp,pp);material_status='GEOMETRIC INTERSECTION ONLY' if abs(local[1])+.012<=.3 and abs(local[2])+.012<=.2 else 'FAIL'
                elif at['kind']=='boundary':
                    local=sub(hp,pp);half=.3 if key=='D' else .2;material_status='GEOMETRIC INTERSECTION ONLY' if abs(local[1])+.012<=half and abs(local[2])+.012<=.3 else 'FAIL'
                holes.append(dict(index=h,centreAtFootXRTm=hp,offsetVWm=[v,w],axisXRT=ee,paidMaterialRayStatus=material_status,intersectionXRTm=witness,finiteHoleEdgeLigament=None,matingHoleRegistration=None,boltReactionForceXRTn=None,boltReactionCoupleXRTnm=None,tensionAndShearPa=None,completeContactCapacity=None))
            grip=None if at['substrateM'] is None else .025+at['substrateM']+.012
            projection=.008+.032+.008
            foot=dict(id=fid,member=ident,end=j,attachment=label,contactDatumXRTm=fpoint,plateCentreXRTm=cp,basisEVW=basis,plateStockID=plateid,hardwareStockIDs=hardware,substrate=at,plateSolid=obb(fid,cp,basis,[.025,.350,.350],'end plate'),boltPattern=holes,gripLowerBoundM=grip,nutWashersThreadProjectionM=projection,lengthAllowanceUpperBoundM=None if grip is None else .180-grip-projection,installedGripStatus='UNKNOWN',faceContactStatus='PASS GEOMETRY ONLY' if at['fullFaceContact'] else 'FAIL' if at['fullFaceContact'] is False else 'UNKNOWN',forceXRTn=None,coupleXRTnm=None,boltLoadConvention='Force/couple exerted by substrate on the isolated tube-end plate. Its reaction is the opposite on substrate. No source-applied sign is called bolt tension.',completeCapacity=None)
            feet.append(foot);endrecords.append(foot)
            weld(fid+' tube perimeter weld',4*size,add(fpoint,mul(ee,.025)),ident,'Full square tube perimeter at this independent foot; 12mm equal-leg fillet stock. Oblique mate/plate bending and weld capacity UNKNOWN.')
        start=add(endrecords[0]['contactDatumXRTm'],mul(e,.025));end=add(endrecords[1]['contactDatumXRTm'],mul(e,-.025));cut=dot(sub(end,start),e)
        m=dict(id=ident,kind=kind,sourceKey=key,fromNode=a,toNode=b,datumEndsXRTm=[p,q],axisXRT=e,basisEVW=frame(e),centreToCentreLengthM=length,stockID=sid,stockMassKg=mass,sizeM=size,wallM=wall,physicalCutEndsXRTm=[start,end],availableCutM=cut,cutStatus='PASS LENGTH ONLY' if cut>0 else 'FAIL',footIDs=[x['id'] for x in endrecords],sectionAreaM2=size**2-(size-2*wall)**2,secondMomentM4=(size**4-(size-2*wall)**4)/12,endForceXRTn=None,endCoupleXRTnm=None,axialBiaxialBendingTorsionCombinedCapacity=None)
        members.append(m)
        if cut>0:
            basis=m['basisEVW'];c=mid(start,end)
            for ax in [1,2]:
                for sign in [-1,1]:
                    cc=add(c,mul(basis[ax],sign*(size-wall)/2));dims=[cut,size-2*wall if ax==2 else size,size-2*wall if ax==1 else size];dims[ax]=wall
                    # Four nonoverlapping wall prisms cover the square annulus.
                    if ax==1:dims=[cut,wall,size]
                    else:dims=[cut,size-2*wall,wall]
                    tube_walls.append(obb(ident+f':wall{ax}/{sign}',cc,basis,dims,ident))
    for n in ['D','C','button']:
        pp=G['buttonSupport']['sourceXRT'] if n=='button' else datums[n];m=next(x for x in members if x['id']==('button' if n=='button' else 'boundary-'+n));f=next(x for x in feet if x['id']==m['footIDs'][0]);e=m['axisXRT'];cp=add(f['contactDatumXRTm'],mul(e,-.010))
        sid=plate(n+' source adaptor full blank',1,D['sourceAdaptorM'],cp,'350x350x20 new source adaptor; exact retained contact/packing duties remain. Mating-hole registration and blind-anchor access UNKNOWN.',m['id']);adaptors.append(dict(id=sid,source=n,centreXRTm=cp,dimensionsM=D['sourceAdaptorM'],normalXRT=e,holeAndContactQualification=None))
    temp=stock('temporary erection bracing allowance',1,D['temporaryBracingKgPerModule'],datums['A'],'Additional10kg/module; old15kg tool and12kg erection stock retained once. No erection capacity, wind dilution or complete temporary works claim.',None,'erection')

    # Matched accounting. Pooled or ambiguous prior rows remain fully charged.
    oldrows=B['massBasis']['newItems'];remove=set(D['conditionallyRemovedI029RowIDs']);reconciliation=[];gravity=[]
    for x in oldrows:
        removed=x['id'] in remove
        reason='Explicit replacement by31 tubes, independent new feet, node/saddle/receiver stock; conditional bill only.' if removed else 'Retained once, including pooled weld, button feet/pads/backers/sets and old access stock without an honest split; physical reuse/placement boundary UNKNOWN where applicable.'
        reconciliation.append(dict(sourceID=x['id'],sourceItem=x['item'],oldMassT=x['massT'],conditionalRemovedT=x['massT'] if removed else 0.,retainedT=0. if removed else x['massT'],qualifiedRetirementT=0.,disposition=reason))
        if not removed:gravity.append(dict(id='I029-'+str(x['id']),item=x['item'],massKg=x['massPerModuleKg'],pointXRTm=x['centreXRTm'],allocation='Inherited bookkeeping centroid; no accepted A/B reaction allocation.',stockSource='baseline.massBasis.newItems'))
    for x in B['massBasis']['keptStockGravity']:
        gravity.append(dict(id='I024-'+str(x['sourceIndex']),item=x['sourceRow']['item'],massKg=x['massPerModuleKg'],pointXRTm=x['centreXRTm'],allocation='Saved I024 bookkeeping centroid retained without old receiver assignment.',stockSource='baseline.massBasis.keptStockGravity'))
    for x in bill:gravity.append(dict(id=x['id'],item=x['item'],massKg=x['massPerModuleKg'],pointXRTm=x['centreXRTm'],allocation='Declared finite stock/bookkeeping centroid; uninstalled trim/blank stock remains charged.',stockSource='stock.newItems'))
    newkg=sum(x['massPerModuleKg'] for x in bill);newT=newkg*repeat/1000;removedT=sum(x['conditionalRemovedT'] for x in reconciliation);old=B['massBasis'];hull=old['knownHullT']-removedT+newT;gas=old['residualGasOnceT'];subtotal=hull+gas;boundHull=old['knownHullT']+newT;localKg=sum(x['massKg'] for x in gravity)
    mass=dict(previousHullT=old['knownHullT'],previousCassetteStockT=old['newCassetteStockT'],selectedRemovedI029StockT=removedT,retainedI029StockT=sum(x['retainedT'] for x in reconciliation),retainedI024StockT=old['retainedI024StockT'],newTriangulationStockT=newT,knownHullT=hull,residualGasOnceT=gas,knownSubtotalT=subtotal,deltaKnownHullT=hull-old['knownHullT'],qualifiedRetirementT=0.,noNewRetirementHullT=boundHull,noNewRetirementSubtotalT=boundHull+gas,fullyUnretiredHistoricalHullT=boundHull+old['selectedRemovedI024StockT'],fullyUnretiredHistoricalSubtotalT=boundHull+old['selectedRemovedI024StockT']+gas,selectedVolumeM3=old['selectedVolumeM3'],displacementChangeM3=0.,additionalUCt=None,missionHardwareMassT=None,equipmentPayloadMassT=None,physicalFloat=None,selectedLocalStockKgPerModule=localKg,selectedLocalStockAllModulesT=localKg*repeat/1000,olderHullMassT=hull-localKg*repeat/1000,olderHullGravityAndGlobalStability=None,at=[dict(altitudeM=x['altitudeM'],fixedVolumeLiftT=x['fixedVolumeLiftT'],selectedKnownMarginT=x['fixedVolumeLiftT']-subtotal,predecessorKnownMarginT=x['selectedKnownMarginT'],deltaMarginT=old['knownSubtotalT']-subtotal,noNewRetirementKnownMarginT=x['fixedVolumeLiftT']-(boundHull+gas),fullyUnretiredHistoricalKnownMarginT=x['fixedVolumeLiftT']-(boundHull+old['selectedRemovedI024StockT']+gas)) for x in old['at']],marginExpression='known margin - additional U+C - mission/equipment/payload obligations; unknown additions are not zero.',qualification='Same vacuum-structural branch and fixed displacement. Conditional replaced-stock comparison is not a qualified saving. No-new-retirement and fully-unretired historical bounds are alternatives, never added to selected mass or each other.')

    # Finite checks. No node-wide exemption and no free crossing joint.
    conflicts=[]
    for i,m in enumerate(members):
        wa=[x for x in tube_walls if x['role']==m['id']]
        for n in members[i+1:]:
            wb=[x for x in tube_walls if x['role']==n['id']];hit=None
            for a in wa:
                for b in wb:
                    ov=overlap(a,b)
                    if ov is not None:hit=dict(firstWall=a['id'],secondWall=b['id'],minimumSATOverlapM=ov);break
                if hit:break
            if hit:conflicts.append(dict(first=m['id'],second=n['id'],status='FAIL',reason='Positive intersection of paid RHS wall prisms; no joint at crossing and no shared-node exclusion.',witness=hit))
    plate_conflicts=[]
    for i,a in enumerate(feet):
        for b in feet[i+1:]:
            ov=overlap(a['plateSolid'],b['plateSolid'])
            if ov is not None:plate_conflicts.append(dict(first=a['id'],second=b['id'],status='FAIL',minimumSATOverlapM=ov,reason='Independent finite end plates overlap; no trim, relocation or shared area credited.'))
    cover_conflicts=[]
    for c in covers:
        for f in feet:
            ov=overlap(c['solid'],f['plateSolid'])
            if ov is not None:cover_conflicts.append(dict(node=c['node'],cover=c['cover'],foot=f['id'],status='FAIL',minimumSATOverlapM=ov))
    active=[G['solids'][x['sourceIndex']] for x in B['legacySolidDisposition'] if x['active']]
    retained_witnesses=[]
    # These are finite interior witnesses, not exhaustive collision clearance.
    for box in tube_walls+[x['plateSolid'] for x in feet]:
        pts=[box['centre']]+[add(box['centre'],mul(sub(v,box['centre']),.999)) for v in corners(box)]
        for oldsolid in active:
            hit=next((v for v in pts if inside_saved(v,oldsolid)),None)
            if hit is not None:retained_witnesses.append(dict(newSolid=box['id'],retainedSolid=oldsolid['name'],pointXRTm=hit,status='FAIL',scope='Point strictly inside this new solid and saved retained material; valid occupied-material witness, not absence proof.'))
    pin_access=[]
    for key,root in roots.items():
        p=root['pinXRT'];axis=root['pinAxisXRT'];half=root['pinOccupiedLengthM']/2
        pin_access.append(dict(root=key,pinAxisXRT=axis,occupiedEndpointsXRTm=[add(p,mul(axis,-half)),add(p,mul(axis,half))],insertionSweptEndpointsXRTm=[add(p,mul(axis,-half)),add(p,mul(axis,half+root['insertionTravelM']))],sweepDiameterM=.100,status='FAIL' if key=='AD-A' else 'UNKNOWN',reason='Inherited occupied AD-A pin/BD-carbon interference remains.' if key=='AD-A' else 'Finite axis/travel retained; continuous swept material and tool/retainer access not proved.'))
    fit=dict(memberCutFailures=[x['id'] for x in members if x['cutStatus']=='FAIL'],noncoplanarFootFailures=[x['id'] for x in feet if x['faceContactStatus']=='FAIL'],boltMaterialMisses=[dict(foot=f['id'],bolt=x['index'],pointXRTm=x['centreAtFootXRTm']) for f in feet for x in f['boltPattern'] if x['paidMaterialRayStatus']=='FAIL'],tubeWallIntersections=conflicts,independentPlateIntersections=plate_conflicts,coverIntersections=cover_conflicts,retainedMaterialWitnesses=retained_witnesses,pinInsertion=pin_access,receiverLengthOnly=[{k:x[k] for k in ['id','tieGripM','tieLengthM','tieLengthAllowanceM','lengthOnlyStatus','installedLengthAndAccessStatus']} for x in receiver_records],neighborSectorClearance=None,toolAndNutSweeps=None,allFiniteBodyClearance=None,qualification='Each positive solid witness or missing cut/contact is FAIL. A missing witness is UNKNOWN, not clearance. Cube inner volumes, cover aperture/access, all gusset/web and saddle bolt placements, curved source contact and receiver reinforcement are not silently solved.')

    # Full pressure wrenches at each original pin/wall/button; transport only.
    pressures=[]
    for src in B['pressureAssignments']:
        sources=[]
        for x in src['roots']:sources.append(dict(id=x['member'].replace('root ','root-'),pointXRTm=x['sourcePinXRTm'],forceXRTn=x['sourceForceXRTn'],coupleXRTnm=x['sourceCoupleXRTnm']))
        for x in src['ringPorts']:sources.append(dict(id='boundary-'+x['node'],pointXRTm=x['sourceWallPointXRTm'],forceXRTn=x['forceXRTn'],coupleXRTnm=x['coupleAtWallXRTnm']))
        x=src['button'];sources.append(dict(id='button',pointXRTm=x['sourceXRTm'],forceXRTn=x['forceXRTn'],coupleXRTnm=x['sourceCoupleXRTnm']))
        totalF=total([x['forceXRTn'] for x in sources]);totalM=total([transport(x['forceXRTn'],x['coupleXRTnm'],x['pointXRTm'],O) for x in sources]);arms=[]
        for x in sources:
            m=next(z for z in members if z['id']==x['id']);fp=[next(z for z in feet if z['id']==fid)['contactDatumXRTm'] for fid in m['footIDs']]
            arms.append(dict(id=m['id'],originalSource=x,firstFootAppliedForceXRTn=x['forceXRTn'],firstFootAppliedCoupleXRTnm=transport(x['forceXRTn'],x['coupleXRTnm'],x['pointXRTm'],fp[0]),lastFootDeliveredForceXRTn=x['forceXRTn'],lastFootDeliveredCoupleXRTnm=transport(x['forceXRTn'],x['coupleXRTnm'],x['pointXRTm'],fp[1]),firstSourceReactionOnSourceForceXRTn=mul(x['forceXRTn'],-1),firstSourceReactionOnSourceCoupleAtOriginalPointXRTnm=mul(x['coupleXRTnm'],-1),qualification='Pressure-only wrench transport; full source couple retained. This is not a bolt reaction distribution or closed-frame member solution; gravity is added in keyed states.'))
        pressures.append(dict(id='f'+str(src['radialFraction']),radialFraction=src['radialFraction'],sourceWrenches=sources,sourceArms=arms,totalForceXRTn=totalF,totalMomentAboutOXRTnm=totalM,sourceForceResidualN=norm(sub(totalF,src['savedTotalForceXRTn'])),sourceMomentResidualNm=norm(sub(totalM,src['savedTotalMomentAboutOXRTnm'])),adAxialTensionN=src['adAxialTensionN'],qualification='Two inherited load assignments only; no new load sharing, whole-end611MN, pressure retuning or ancestor execution.'))
    unknown_members=[dict(member=m['id'],firstFoot=m['footIDs'][0],lastFoot=m['footIDs'][1],forceAtFirstXRTn=None,coupleAtFirstXRTnm=None,forceAtLastXRTn=None,coupleAtLastXRTnm=None,axialN=None,bendingVWnm=None,torsionNm=None,normalCornerPa=None,combinedCapacity=None,reason='Bending-capable closed frame; no stiffness/contact model or approved allocation. Known pressure/source-tube-own-weight subset is separately named, never full demand.') for m in members]
    unknown_feet=[dict(foot=f['id'],forceExertedBySubstrateOnFootXRTn=None,coupleExertedBySubstrateOnFootXRTnm=None,boltReactionSet=None,tensionShearBearingPryingWeld=None,status='UNKNOWN') for f in feet]
    unknown_nodes=[dict(node=n,incidentMembers=[m['id'] for m in members if n in [m['fromNode'],m['toNode']] or (n.endswith('0') and m['id']=='crosshead-'+n[0])],forceXRTn=None,coupleXRTnm=None,wallDistortionAndLocalCapacity=None,status='UNKNOWN') for n in list(nodes)+list(saddles)]
    states=[]
    for pressure in pressures:
        for k in range(37):
            angle=2*math.pi*k/37;g=[0,-D['gMps2']*math.cos(angle),D['gMps2']*math.sin(angle)]
            gf=total([mul(g,x['massKg']) for x in gravity]);gm=total([cross(sub(x['pointXRTm'],O),mul(g,x['massKg'])) for x in gravity]);ef=add(pressure['totalForceXRTn'],gf);em=add(pressure['totalMomentAboutOXRTnm'],gm);partials=[]
            for arm in pressure['sourceArms']:
                m=next(z for z in members if z['id']==arm['id']);x=arm['originalSource'];mp=mid(*m['datumEndsXRTm']);last=next(z for z in feet if z['id']==m['footIDs'][1])['contactDatumXRTm'];ownF=mul(g,m['stockMassKg']);F=add(x['forceXRTn'],ownF);M=add(transport(x['forceXRTn'],x['coupleXRTnm'],x['pointXRTm'],last),cross(sub(mp,last),ownF))
                partials.append(dict(member=m['id'],pressureAndTubeStockOnlyForceDeliveredXRTn=F,pressureAndTubeStockOnlyCoupleDeliveredXRTnm=M,completeMemberAndFootDemand=None))
            states.append(dict(id=pressure['id']+'-s'+str(k).zfill(2),assignment=pressure['id'],sector=k,angleRad=angle,gravityLocalMps2=g,gravityStockSet='allSelectedLocalStock',gravityForceXRTn=gf,gravityMomentAboutOXRTnm=gm,totalKnownExternalForceXRTn=ef,totalKnownExternalMomentAboutOXRTnm=em,requiredReceiverPairReactionForceXRTn=mul(ef,-1),requiredReceiverPairReactionMomentAboutOXRTnm=mul(em,-1),receiverReactions={'A':{'forceXRTn':None,'coupleAtReceiverXRTnm':None},'B':{'forceXRTn':None,'coupleAtReceiverXRTnm':None}},memberDemandSet='all31Unresolved',footDemandSet='all62Unresolved',nodeDemandSet='all12Unresolved',sourceArmPartialDemand=partials,oppositeCap={'originGlobalXRTm':global_point(O,k,True),'knownExternalForceGlobalXRTn':global_force(ef,k,True),'knownExternalMomentAboutReflectedOriginGlobalXRTnm':global_couple(em,k,True),'receiverPairReactionGlobalXRTn':global_force(mul(ef,-1),k,True),'receiverPairReactionMomentGlobalXRTnm':global_couple(mul(em,-1),k,True)},qualification='All retained/new local stock gravity is in aggregate, once. Per-source-arm subset adds only its paid tube stock; excluded connections and other retained mass remain in aggregate and full unresolved demands. Older hull gravity is UNKNOWN, mass remains charged.'))
    assert len(states)==74 and len({x['id'] for x in states})==74 and len(feet)==62 and len(unknown_nodes)==12
    fixed=B['pressureBasis'];summary=dict(status='FAIL / UNKNOWN',newTubeCount=len(members),newFootCount=len(feet),sideNodeCount=len(nodes),saddleCount=len(saddles),stateCount=len(states),assignments=2,orientationsPerAssignment=37,physicalModules=74,stockRows=len(bill),gravityRows=len(gravity),newStockT=newT,removedStockT=removedT,knownHullT=hull,knownSubtotalT=subtotal,deltaHullT=mass['deltaKnownHullT'],massReductionOnly=hull<old['knownHullT'],qualifiedRetirementT=0.,memberCutFailures=len(fit['memberCutFailures']),noncoplanarFootFailures=len(fit['noncoplanarFootFailures']),boltMaterialMisses=len(fit['boltMaterialMisses']),tubeWallConflicts=len(conflicts),plateConflicts=len(plate_conflicts),coverConflicts=len(cover_conflicts),retainedMaterialWitnesses=len(retained_witnesses),maximumSourceForceResidualN=max(x['sourceForceResidualN'] for x in pressures),maximumSourceMomentResidualNm=max(x['sourceMomentResidualNm'] for x in pressures),receiverCapacity=None,completeMemberStress=None,completeAllUpMassT=None,physicalFloat=None)
    result=dict(unit='R3-I033',baselineSha256=sha(U/'baseline.json'),sourcesSha256=sha(U/'sources.json'),calculatorSha256=sha(Path(__file__)),selectedHypothesis='Two triangulated RHS side frames with paid transverse bracing, source arms and standoffs to actual A/B receiving cuffs. One failed/unqualified construction, not an axial-only truss.',geometry=dict(datumsXRTm=datums,sideNodesXRTm=nodes,saddleCentresXRTm=saddles,members=members,nodeBoxes=nodeboxes,nodeWallStock=nodeplates,covers=covers,saddles=saddle_records,feet=feet,receivers=receiver_records,sourceAdaptors=adaptors,retainedGeometryReference='baseline.inheritedGeometry with legacySolidDisposition; baseline.retainedI029Geometry; no ancestor model import',material=dict(steelDensityKgM3=rho,elasticModulusPa=D['steelEpa'],nominalComparisonPa=D['steelNominalPa'],certification=None),boltM24SetKg=m24kg,finiteTubeWallPrisms=tube_walls),fixedPressureAndFilm=fixed,stock=dict(newItems=bill,newWeldRuns=welds,matchedI029Rows=reconciliation,matchedI024RowsReference='baseline.massBasis.priorRows; unchanged retained and already conditionally removed historical rows; never newly retired'),mass=mass,fit=fit,pressureAssignments=pressures,localStockGravitySources=gravity,demandSets=dict(all31Unresolved=unknown_members,all62Unresolved=unknown_feet,all12Unresolved=unknown_nodes),states=states,conventions=dict(originXRTm=O,rightHanded=True,gravity='For sector theta: local g=(0,-g cos(theta),g sin(theta)).',rightMap='Rotate R/T by theta: (X,R cos(theta)-T sin(theta),R sin(theta)+T cos(theta)).',oppositePositionForce='Reflect global X through vehicle midplane, then rotate R/T: Q=diag(-1,1,1). Positions and polar force vectors use Q.',oppositeCouple='Axial pseudovector transforms by det(Q)Q=diag(1,-1,-1), then R/T rotation. Moment origin also reflected. No second pressure load is added.',stateInterpretation='74 keyed assignment/orientation records = 2x37. Each has the opposite-cap mapping; physical bill repeats37 sectors x2 caps, never74x2.',receiverEquilibrium='RA+RB=-Fexternal; cross(A-O,RA)+MA+cross(B-O,RB)+MB=-Mexternal. Six constraints cannot determine12 reaction components. Individual A/B and every closed-frame member/foot/node demand remain UNKNOWN.',sectionRule='If full signed internal resultants were available, square-corner normal demand is |N|/A+|Mv|/Zv+|Mw|/Zw. No transverse-norm/one-Z surrogate is used. Full member stress and buckling remain UNKNOWN.',sourceReactionRule='A source wrench applied to this module has its negative acting on the source body at the same point. Unknown bolt/contact allocation is null, not zero tension.',stockGravityRule='All charged selected local rows are applied at declared bookkeeping centres once, including retained pooled stock and trim. Exact installed CG and older hull/global gravity allocation remain UNKNOWN.'),summary=summary,weakestAssumption='The existing A/B cuffs and surrounding frame can accept the complete three-dimensional reaction pair without dominant additional reinforcement, peel/rotation or contact conflict. Individual reactions and that capacity are UNKNOWN.',sensitivity=dict(geometrySweeps=0,additionalReceiverReinforcementMassT=None,receiverStiffness=None,loadSharing=None,knownMassMarginalEffect='One additional tonne of U+C decreases each fixed-lift margin by one tonne; no structural sensitivity is inferred.'),nextUntestedHypothesis='A separately paid wider frame saddle replacing cuff load introduction at the same named frame region; one future freeze required, not a second geometry or execution here.',inheritedFailures=B['inheritedFailures'],historicalQualification=B['historicalQualification'],unresolved=['All closed-frame stiffness/load sharing and full31 member/62 foot/12 node demands','Receiver cuff/ring bearing, peel, slip, prying, preload, rotation and any additional reinforcement C','Unissued saddle web/gusset/bolt layout, receiver gusset layout, cover apertures and tool access','Continuous swept/neighbor-sector interference, curved source contacts and mating-hole registration','Finite pin/fork/carbon and retained historical failures','All older hull gravity/global shape, pressure resistance, erection, full U+C/mission/payload and physical float'],computation=dict(newGeometries=1,states=74,solverInvocations=0,sweeps=0,drawings=0,ancestorImports=0,engineeringScope='Finite fixed construction bookkeeping, analytic wrench transport, finite material witnesses and explicit unresolved duties only.'),qualification='Failed finite construction and conditional stock comparison. No installed structure, qualified retirement, resolved review finding, full ring/receiver capacity, global pressure resistance, mission completion or float confidence is established.')
    (U/'triangulation.json').write_text(json.dumps(result,separators=(',',':'),allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    print('SCIENCE_COMPLETED',flush=True)

if __name__=='__main__':main()
