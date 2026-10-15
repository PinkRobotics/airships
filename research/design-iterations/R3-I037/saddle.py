#!/usr/bin/env python3
"""One frozen saddle: paid stock, finite material witnesses and unresolved wrenches.

Only saved JSON is input. No ancestor imports, stiffness allocation, optimizer,
capacity solver or alternate geometry. Null means UNKNOWN, never zero demand.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = U.parents[2]
XYZ = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
ZERO = [0., 0., 0.]
O = [40., 0., 0.]

def add(a, b): return [a[i] + b[i] for i in range(3)]
def sub(a, b): return [a[i] - b[i] for i in range(3)]
def mul(a, s): return [v * s for v in a]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def norm(a): return math.sqrt(dot(a, a))
def total(vs): return [sum(v[i] for v in vs) for i in range(3)]
def mid(a, b): return mul(add(a, b), .5)
def transport(f, m, p, q): return add(m, cross(sub(p, q), f))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rotated(p, sector):
    angle = 2*math.pi*sector/37; c = math.cos(angle); s = math.sin(angle)
    return [p[0], c*p[1]-s*p[2], s*p[1]+c*p[2]]
def reflected_point(p, sector): return rotated([-p[0], p[1], p[2]], sector)
def reflected_couple(v, sector): return rotated([v[0], -v[1], -v[2]], sector)
def box(ident, c, d, axes=None, **extra):
    return dict(id=ident, kind='box', centre=c, dimensions=d, axes=axes or XYZ, holes=[], **extra)
def annulus(ident, c, length, outer, inner, axis=0, **extra):
    axes = [XYZ[axis]] + [XYZ[i] for i in range(3) if i != axis]
    return dict(id=ident, kind='annulus', centre=c, dimensions=[length, 2*outer, 2*outer],
                axes=axes, outerRadiusM=outer, innerRadiusM=inner, holes=[], **extra)
def aabb(s):
    ext = [sum(abs(a[i])*d/2 for a, d in zip(s['axes'], s['dimensions'])) for i in range(3)]
    return [sub(s['centre'], ext), add(s['centre'], ext)]
def hole(point, diameter, axis=0): return dict(point=point, axis=XYZ[axis], radius=diameter/2)
def material(p, s):
    """A strict material witness, not a full intersection/clearance solver."""
    e = 1e-8; q = sub(p, s['centre']); v = [dot(q, a) for a in s['axes']]; d = s['dimensions']
    if s['kind'] == 'ringbox':
        rr = math.hypot(v[1], v[2])-s['radiusM']; half=s['sizeM']/2; w=s['wallM']
        inside = abs(v[0]) < half-e and abs(rr) < half-e and (abs(v[0]) > half-w+e or abs(rr) > half-w+e)
    elif s['kind'] == 'annulus':
        rr = math.hypot(v[1], v[2]); inside=abs(v[0]) < d[0]/2-e and s['innerRadiusM']+e < rr < s['outerRadiusM']-e
        if s['innerRadiusM'] == 0: inside=abs(v[0]) < d[0]/2-e and rr < s['outerRadiusM']-e
    else:
        inside = all(abs(v[i]) < d[i]/2-e for i in range(3))
        if s['kind'] == 'cubeShell': inside = inside and max(abs(x) for x in v) > d[0]/2-s['wallM']+e
        if s['kind'] == 'boxTube':
            w=s.get('wallM'); inside=inside and w is not None and (abs(v[1])>d[1]/2-w+e or abs(v[2])>d[2]/2-w+e)
    if not inside: return False
    if 'splitSign' in s and q[0]*s['splitSign'] <= e: return False
    if 'boreCentre' in s:
        v0=sub(p,s['boreCentre'])
        if math.hypot(v0[0],v0[1]) <= s['boreRadiusM']+e: return False
    for h in s.get('holes', []):
        hp=sub(p,h['point']); perp=sub(hp,mul(h['axis'],dot(hp,h['axis'])))
        if norm(perp) <= h['radius']+e: return False
    return True

def intersection(a,b):
    aa=a['_aabb'];bb=b['_aabb'];lo=[max(aa[0][i],bb[0][i]) for i in range(3)];hi=[min(aa[1][i],bb[1][i]) for i in range(3)]
    if any(hi[i]-lo[i] <= 2e-8 for i in range(3)): return None,False
    # Fixed, deterministic witnesses in the common enclosing box. A miss is UNKNOWN.
    fractions=(.1,.3,.5,.7,.9)
    for fx in fractions:
        for fy in fractions:
            for fz in fractions:
                p=[lo[i]+f*(hi[i]-lo[i]) for i,f in enumerate((fx,fy,fz))]
                if material(p,a) and material(p,b): return p,True
    return None,True

def main():
    assert sys.argv[1:] == ['--write']
    B=json.loads((U/'baseline.json').read_text());S=json.loads((U/'sources.json').read_text())
    assert sha(U/'baseline.json') == S['baselineSha256']
    for name,h in S['inputFiles'].items(): assert sha(R/name)==h, name
    P=B['savedI033'];PB=B['savedI033Baseline'];D=B['design'];rho=D['steelDensityKgM3'];repeat=D['repeatCount']
    assert repeat==74 and len(P['geometry']['members'])==31 and len(P['geometry']['feet'])==62 and len(P['states'])==74
    assert P['mass']['knownHullT']==6478.234514991365 and P['mass']['qualifiedRetirementT']==0
    print('SCIENCE_STARTED: R3-I037 one frozen saddle; saved predecessors as data only',flush=True)
    datums=P['geometry']['datumsXRTm'];stock=[];solids=[];welds=[];unplaced_welds=[];stacks=[];boundaries=[];contacts=[];retained_backers=[]
    def paid(name,kg,centre,dimensions,receiver,geometry=None,qualification='Full stock paid; capacity UNKNOWN.'):
        ident='saddle-'+str(len(stock));stock.append(dict(id=ident,item=name,countPerModule=1,massPerModuleKg=kg,massT=kg*repeat/1000,totalCount=repeat,centreXRTm=centre,dimensions=dimensions,receiver=receiver,qualification=qualification))
        if geometry is not None:
            geometry.update(id=ident,label=name,stockID=ident,receiver=receiver);solids.append(geometry)
        return ident
    def blank(name,centre,dims,receiver,**kw):
        return paid(name,rho*math.prod(dims),centre,dims,receiver,box('',centre,dims,**kw))
    def washer(name,x0,x1,r,t,base,od,id_,receiver):
        c=add(base,[(x0+x1)/2,r,t]);return paid(name,rho*math.pi*(od*od-id_*id_)*(x1-x0)/4,c,dict(outerDiameterM=od,innerDiameterM=id_,lengthM=x1-x0),receiver,annulus('',c,x1-x0,od/2,id_/2))
    def hexpart(name,x0,x1,r,t,base,af,bore,receiver):
        c=add(base,[(x0+x1)/2,r,t]);g=annulus('',c,x1-x0,af/2,bore/2);g['hexMaterialQualification']='Only the orientation-independent inscribed circular core is tested. Hex corners/clocking unresolved; no clearance PASS.'
        return paid(name,rho*math.sqrt(3)/2*af*af*(x1-x0),c,dict(AF=af,length=x1-x0,bore=bore),receiver,g,'Full hex blank paid without bore credit; guaranteed material core used for positive witnesses only.')
    def shaft(name,x0,x1,r,t,base,diam,receiver):
        c=add(base,[(x0+x1)/2,r,t]);return paid(name,rho*math.pi*diam*diam*(x1-x0)/4,c,dict(diameterM=diam,underHeadLengthM=x1-x0),receiver,annulus('',c,x1-x0,diam/2,0),'Full-length threaded stock assumed; nominal outer cylinder only. Thread-root capacity/engagement UNKNOWN.')
    def boundary(ident,point,kind,owner,sourceids=None,**extra):
        boundaries.append(dict(id=ident,pointXRTm=point,kind=kind,receiver=owner,stockIDs=sourceids or [],forceXRTn=None,coupleAtBoundaryXRTnm=None,completeCapacity=None,**extra))
    def weld_line(name,length,c,receiver,line,supported):
        ident=paid(name,rho*.5*D['weldLegM']**2*length,c,dict(legM=D['weldLegM'],lengthM=length),receiver,qualification='Geometric fillet stock paid once. Unsupported requested edge is paid uninstalled stock, not an actual weld/load path.')
        row=dict(id=ident,line=line,lengthM=length,legM=D['weldLegM'],centroidXRTm=c,receiver=receiver,actualMeetingSteel=supported,capacity=None)
        (welds if supported else unplaced_welds).append(row)
        boundary(ident+'-joint',c,'actual weld line' if supported else 'requested weld without finite fillet backing',receiver,[ident],activeLoadPath=supported)
        return ident
    for receiver in ['A','B']:
        base=datums[receiver];tieholes=[hole(add(base,[0,r,t]),D['tieHoleDiameterM']) for r,t in D['tieRTm']]
        for sign in [-1,1]:
            c=add(base,[sign*.09,0,0]);ident=blank(receiver+' saddle half '+str(sign),c,D['halfBlankXRTm'],receiver,boreCentre=base,boreRadiusM=D['boreRadiusM']);solids[-1]['holes']=tieholes
            boundary(ident+'-split',base,'saddle split plane/contact; unilateral and preload unknown',receiver,[ident])
            ri=D['cuffOuterRadiusM'];ro=D['boreRadiusM'];length=D['cuffLengthM'];kg=D['polymerDensityKgM3']*math.pi*(ro*ro-ri*ri)*length/2
            cx=sign*4*(ro**3-ri**3)/(3*math.pi*(ro*ro-ri*ri));c=add(base,[cx,0,0]);shape=annulus('',base,length,ro,ri,axis=2,splitSign=sign)
            lid=paid(receiver+' liner half '+str(sign),kg,c,dict(innerRadiusM=ri,outerRadiusM=ro,lengthM=length),receiver,shape,'Nominal half-shell, density1200kg/m3 assumed; no friction/adhesion/preload/compression credit.')
            for interface,radius in [('cuff',ri),('saddle',ro)]:
                boundary(lid+'-'+interface,base,'finite half cylindrical liner contact',receiver,[lid],radiusM=radius,finiteTM=[-.2,.2],normalPressurePa=None,slipCapacity=None)
            contacts.append(dict(id=lid,innerRadiusM=ri,outerRadiusM=ro,finiteLengthM=length,contactAreaM2=math.pi*ri*length,installationTolerance=None,preload=None,friction=None,capacity=None))
            c=add(base,[sign*.25,0,0]);bid=blank(receiver+' bridge '+str(sign),c,D['bridgeXRTm'],receiver);solids[-1]['holes']=tieholes.copy()
            if sign==-1:solids[-1]['holes'] += [hole(add(base,[0,r,t]),D['M24HoleDiameterM']) for r,t in D['M24RTm']]
            boundary(bid+'-cut',c,'bridge section; unsupported overhang has no cuff contact',receiver,[bid],supportedCuffTM=[-.2,.2],plateTM=[-.6,.6])
        for index,(r,t) in enumerate(D['tieRTm']):
            name=f'{receiver} tie{index}';ids=[];under=-.265-.012-.005;tip=under+D['tieUnderHeadLengthM'];nutend=.265+.012+.005+D['tieNutHeightM']
            ids.append(shaft(name+' M30 shank',under,tip,r,t,base,.03,receiver));ids.append(hexpart(name+' head',under-.020,under,r,t,base,.045,0,receiver));ids.append(hexpart(name+' nut',.282,nutend,r,t,base,.045,.03,receiver))
            for sign in [-1,1]:
                backerx=sign*(.265+.006);c=add(base,[backerx,r,t]);bid=blank(name+' backer '+str(sign),c,D['tieBackerXRTm'],receiver);solids[-1]['holes']=[hole(c,.034)];ids.append(bid)
                x0,x1=sorted([sign*.277,sign*.282]);ids.append(washer(name+' washer '+str(sign),x0,x1,r,t,base,.06,.034,receiver))
                x0,x1=sorted([sign*.180,sign*.235]);c=add(base,[(x0+x1)/2,r,t]);spid=paid(name+' spacer '+str(sign),rho*math.pi*(.06**2-.034**2)*.055/4,c,dict(OD=.06,ID=.034,lengthM=.055),receiver,annulus('',c,.055,.03,.017));ids.append(spid)
                for x in [x0,x1]:
                    cp=add(base,[x,r,t]);boundary(spid+f'-end{x}',cp,'spacer compression-only end contact',receiver,[spid],tensionCredit=False,compressionForceN=None)
                    weld_line(name+f' spacer{sign} circle{x}',2*math.pi*.03,cp,receiver,dict(kind='circle',centreXRTm=cp,axisXRT=XYZ[0],radiusM=.03),True)
            stacks.append(dict(id=name,kind='M30 cross tie',axisXRT=XYZ[0],localRTm=[r,t],stockIDs=ids,underHeadLocalXM=under,tipLocalXM=tip,segmentsLocalXM={'head':[under-.020,under],'negativeWasher':[-.282,-.277],'negativeBacker':[-.277,-.265],'negativeBridge':[-.265,-.235],'negativeSpacer':[-.235,-.180],'negativeHalf':[-.180,0],'positiveHalf':[0,.180],'positiveSpacer':[.180,.235],'positiveBridge':[.235,.265],'positiveBacker':[.265,.277],'positiveWasher':[.277,.282],'nut':[.282,nutend]},threadProjectionBeyondNutM=tip-nutend,lengthOnlyStatus='PASS LENGTH ONLY' if tip>=nutend else 'FAIL',threadEngagementCapacity=None,access=None))
            boundary(name+'-tie-cut',add(base,[0,r,t]),'M30 axial/shear/couple cut',receiver,ids,boltGrade=None,threadRootAreaM2=None)
        for sx in [-1,1]:
            for sr in [-1,1]:
                c=add(base,[sx*.2075,sr*.390,0]);wid=blank(receiver+f' web {sx}/{sr}',c,D['webXRTm'],receiver)
                for x in [sx*.180,sx*.235]:
                    # Four requested edge lines at each actual connecting face.
                    # A fillet also needs receiving steel outside the web edge.
                    for rr in [sr*.390-.010,sr*.390+.010]:
                        p=add(base,[x,rr,-.200]);q=add(base,[x,rr,.200]);supported=abs(rr)+D['weldLegM'] <= .400+1e-10
                        weld_line(wid+f' face{x} R{rr}',norm(sub(q,p)),mid(p,q),receiver,dict(kind='segment',endpointsXRTm=[p,q]),supported)
                    for tt in [-.200,.200]:
                        p=add(base,[x,sr*.390-.010,tt]);q=add(base,[x,sr*.390+.010,tt]);supported=abs(x)>.200
                        weld_line(wid+f' face{x} T{tt}',norm(sub(q,p)),mid(p,q),receiver,dict(kind='segment',endpointsXRTm=[p,q]),supported)
                boundary(wid+'-cut',c,'web cut/plate bending',receiver,[wid])
        oldbacker='new-390' if receiver=='A' else 'new-399'
        for index,(r,t) in enumerate(D['M24RTm']):
            name=f'{receiver} end1 bolt{index}';under=-.290-.004;tip=under+D['M24UnderHeadLengthM'];back0=-.235;back1=back0+.012;washend=back1+.004;nutend=washend+.032;ids=[]
            ids.append(shaft(name+' M24x120 shank',under,tip,r,t,base,.024,receiver));ids.append(hexpart(name+' head',under-.020,under,r,t,base,.036,0,receiver));ids.append(hexpart(name+' nut',washend,nutend,r,t,base,.036,.024,receiver));ids.append(washer(name+' incoming washer',under,-.290,r,t,base,.048,.026,receiver));ids.append(washer(name+' back washer',back1,washend,r,t,base,.048,.026,receiver))
            c=add(base,[(back0+back1)/2,r,t]);back=box(name+' retained backer',c,[.012,.080,.080],label=name+' retained backer',stockID=oldbacker,receiver=receiver);back['holes']=[hole(c,.026)];solids.append(back)
            retained_backers.append(dict(id=oldbacker+f'-bolt{index}',sourceStockID=oldbacker,pointXRTm=c,massKg=None,receiver=receiver))
            stacks.append(dict(id=name,kind='replacement M24 end1',axisXRT=XYZ[0],localRTm=[r,t],stockIDs=ids,retainedBackerSource=oldbacker,underHeadLocalXM=under,tipLocalXM=tip,segmentsLocalXM={'head':[under-.020,under],'incomingWasher':[under,-.290],'retainedPlate':[-.290,-.265],'newBridge':[-.265,-.235],'retainedBacker':[back0,back1],'backWasher':[back1,washend],'nut':[washend,nutend]},threadProjectionBeyondNutM=tip-nutend,lengthOnlyStatus='PASS LENGTH ONLY' if tip>=nutend else 'FAIL',installedGripAndClearanceStatus='UNKNOWN; see positive interference witnesses',threadRootCapacity=None))
            boundary(name+'-cut',add(base,[-.265,r,t]),'M24 end1 bolt independent cut',receiver,ids,retainedBackerSource=oldbacker)
        for i,p in enumerate(D['toolCentresLocalXRTm']):blank(receiver+f' detachable tool{i}',add(base,p),D['toolEnvelopeXRTm'],receiver)
        boundary(receiver+'-incoming-end1',add(base,[-.265,0,0]),'retained incoming plate/new bridge interface',receiver,[],contactAreaM2=.350*.350,pressureDistribution=None,prying=None)
        boundary(receiver+'-cuff-to-ring',base,'finite inherited cuff/ring attachment',receiver,[],forceXRTnUnknown=True,rotationStiffness=None,bearingPeelOvalisationCapacity=None)

    # Every before-state paid row is carried independently. Only issued rows subtract.
    remove33=set(D['conditionallyRemovedI033IDs']);remove29=set(D['conditionallyRemovedI029IDs']);park29=set(D['displacedButChargedI029IDs']);before=[];removed=[];accounting=[]
    for row in P['stock']['newItems']:
        entry=dict(source='I033',sourceID=row['id'],sourceRow=row,conditionalRemovedT=row['massT'] if row['id'] in remove33 else 0.,retainedT=0. if row['id'] in remove33 else row['massT'],qualifiedRetirementT=0.)
        entry['disposition']='Displaced; conditional subtraction only' if row['id'] in remove33 else 'Retained once; original fit/placement qualifications carry'
        before.append(entry)
        if row['id'] in remove33:removed.append(entry)
    old29={x['id']:x for x in PB['massBasis']['newItems']}
    for row in P['stock']['matchedI029Rows']:
        ident=row['sourceID'];activepaid=row['retainedT'];entry=dict(source='I029',sourceID=ident,sourceRow=old29[ident],inheritedDisposition=row,conditionalRemovedT=activepaid if ident in remove29 else 0.,retainedT=0. if ident in remove29 else activepaid,qualifiedRetirementT=0.)
        if ident in remove29:entry['disposition']='Displaced clamp blank; sole eligible old I029 subtraction';removed.append(entry)
        elif ident in park29:entry['disposition']='Displaced function, still paid; storage and gravity placement UNKNOWN';accounting.append(entry)
        elif ident==111:entry['disposition']='Pooled old weld row retained in full; active versus displaced fraction/placement UNKNOWN';accounting.append(entry)
        elif not activepaid:entry['disposition']='Historical already conditionally replaced; not newly removed or active'
        else:entry['disposition']='Retained once with original placement/fit limits'
        before.append(entry)
    assert len(removed)==20
    removed_t=sum(x['conditionalRemovedT'] for x in removed);new_t=sum(x['massT'] for x in stock);parked_t=sum(x['retainedT'] for x in accounting)
    mass=P['mass'];hull=mass['knownHullT']-removed_t+new_t;gas=mass['residualGasOnceT'];subtotal=hull+gas
    newmass=dict(previousI033=mass,newStockT=new_t,conditionalRemovedStockT=removed_t,deltaKnownHullT=new_t-removed_t,knownHullT=hull,residualGasOnceT=gas,knownSubtotalT=subtotal,qualifiedRetirementT=0.,noNewRetirementHullT=mass['knownHullT']+new_t,noNewRetirementSubtotalT=mass['knownSubtotalT']+new_t,carriedI033NoRetirementHullT=mass['noNewRetirementHullT']+new_t,carriedI033NoRetirementSubtotalT=mass['noNewRetirementSubtotalT']+new_t,fullyUnretiredHistoricalHullT=mass['fullyUnretiredHistoricalHullT']+new_t,fullyUnretiredHistoricalSubtotalT=mass['fullyUnretiredHistoricalSubtotalT']+new_t,displacedStillChargedT=parked_t,selectedVolumeM3=mass['selectedVolumeM3'],displacementChangeM3=0.,additionalUCt=None,missionHardwareMassT=None,equipmentPayloadMassT=None,physicalFloat=None,at=[])
    for a in mass['at']:
        lift=a['fixedVolumeLiftT'];newmass['at'].append(dict(altitudeM=a['altitudeM'],fixedVolumeLiftT=lift,selectedKnownMarginT=lift-subtotal,noNewRetirementKnownMarginT=lift-newmass['noNewRetirementSubtotalT'],carriedI033NoRetirementKnownMarginT=lift-newmass['carriedI033NoRetirementSubtotalT'],fullyUnretiredHistoricalKnownMarginT=lift-newmass['fullyUnretiredHistoricalSubtotalT']))
    newmass['qualification']='Alternative bookkeeping bounds, never added together. Displaced retained mass is not simultaneously installed. All include full paid stock and gas once; U+C/mission/equipment/payload remain UNKNOWN.'

    # Placed bookkeeping gravity and unplaced charged mass are not conflated.
    removedids=remove33|{'I029-'+str(i) for i in remove29};parkids={'I029-'+str(i) for i in park29|{111}}
    gravity=[];gravity_disposition=[];retained_byid={x['id']:x for x in P['stock']['newItems']}
    for row in P['localStockGravitySources']:
        ident=row['id']
        if ident in removedids:action='inactive conditionally displaced; omitted from new installed/placed subset'
        elif ident in parkids:action='still charged, placement UNKNOWN; omitted from known placed subset, never assigned zero true wrench'
        elif ident in D['M24RetainedBackerRows']:action='same paid row expanded at eight issued backer positions below; not added twice'
        else:gravity.append(dict(row,qualification='Inherited paid-stock bookkeeping centroid, not renewed installation proof.'));action='carried once in placed bookkeeping subset'
        gravity_disposition.append(dict(id=ident,source=row,action=action))
    for x in retained_backers:
        x['massKg']=retained_byid[x['sourceStockID']]['massPerModuleKg']/8
        gravity.append(dict(x,item='retained M24 end1 backer',qualification='Same paid row; now explicit issued behind-bridge location.'))
    for x in stock:
        gravity.append(dict(id=x['id'],item=x['item'],massKg=x['massPerModuleKg'],pointXRTm=x['centreXRTm'],qualification='Full paid component/blank stock assigned once at stated bookkeeping centre. Cut scrap, unsupported weld stock and detachable tooling placement are assumptions, not extra contact.'))
    newmass['knownPlacedLocalStockKgPerModule']=sum(x['massKg'] for x in gravity)
    newmass['accountingOnlyDisplacedKgPerModule']=parked_t*1000/repeat
    newmass['selectedLocalChargedKgPerModule']=mass['selectedLocalStockKgPerModule']+(new_t-removed_t)*1000/repeat
    newmass['placedPlusUnplacedMassResidualKg']=newmass['selectedLocalChargedKgPerModule']-newmass['knownPlacedLocalStockKgPerModule']-newmass['accountingOnlyDisplacedKgPerModule']
    assert abs(newmass['placedPlusUnplacedMassResidualKg'])<1e-7

    # Retain every saved finite active body; missing installation geometry stays UNKNOWN.
    retained=[]
    for f in P['geometry']['feet']:
        q=dict(f['plateSolid']);q.update(kind='box',holes=[dict(point=h['centreAtFootXRTm'],axis=h['axisXRT'],radius=.013) for h in f['boltPattern']],label=f['id'],source='saved I033 foot plate; nominal holes, not registration proof');retained.append(q)
    for s in P['geometry']['finiteTubeWallPrisms']:retained.append(dict(s,kind='box',holes=[],label=s['id'],source='saved I033 finite tube wall'))
    for s in P['geometry']['nodeBoxes']:retained.append(dict(s,kind='cubeShell',wallM=.020,holes=[],label=s['id'],source='saved I033 node shell; unspecified apertures not opened'))
    for c in P['geometry']['covers']:retained.append(dict(c['solid'],kind='box',holes=[],label=c['solid']['id'],source='saved I033 full cover; unspecified holes'))
    for a in P['geometry']['saddles']:
        for s in a['plateSolids']:retained.append(dict(s,kind='box',holes=[],label=s['id'],source='saved I033 saddle plate'))
    for s in P['geometry']['sourceAdaptors']:
        normal=s['normalXRT'];seed=XYZ[2] if abs(dot(normal,XYZ[2]))<.99 else XYZ[1];v=cross(seed,normal);v=mul(v,1/norm(v));axes=[normal,v,cross(normal,v)]
        retained.append(box(s['id'],s['centreXRTm'],[.020,.350,.350],axes,label=s['id'],source='saved I033 adaptor full blank, no unissued hole credit'))
    for disp,s in zip(PB['legacySolidDisposition'],PB['inheritedGeometry']['solids']):
        assert disp['name']==s['name']
        if not disp['active']:continue
        kind=s['kind'];q=dict(s,id='legacy-'+str(disp['sourceIndex']),label=s['name'],centre=s['centreXRT'],dimensions=s['dimensionsM'],holes=[],source='saved retained active finite body')
        if kind in ['tube','cylinder']:
            q.update(kind='annulus',outerRadiusM=s['dimensionsM'][1]/2,innerRadiusM=s.get('innerDiameterM',0)/2)
        retained.append(q)
    # The retained continuous I029 AD plate is an explicitly saved primitive.
    ad=PB['retainedI029Geometry']['ad'];ae=ad['axisXRT'];ap=ad['pinAxisXRT'];aw=cross(ap,ae);aw=mul(aw,1/norm(aw));ac=mid(*ad['pinCentresXRTm'])
    aq=box('I029-continuous-AD',ac,[ad['blankLengthM'],ad['blankWidthM'],ad['blankThicknessM']],[ae,aw,ap],label='I029 continuous AD plate',source='saved finite AD blank');aq['holes']=[dict(point=p,axis=ap,radius=ad['boreM']/2) for p in ad['pinCentresXRTm']];retained.append(aq)
    for s in solids+retained:s['_aabb']=aabb(s)
    collisions=[];uncertain=[];paircount=0
    # All new/retained backer pairs, plus every new body against every known retained body.
    for i,a in enumerate(solids):
        for b in solids[i+1:]+retained:
            paircount+=1;p,broad=intersection(a,b)
            if p is not None:
                collisions.append(dict(a=a['id'],b=b['id'],aLabel=a.get('label',a['id']),bLabel=b.get('label',b['id']),witnessXRTm=p,status='FAIL: strict interior material witness',oppositeCapWitnessXRTm=reflected_point(p,0),mirrorStatement='Q=diag(-1,1,1) is a material-preserving isometry; this witness holds on both cap placements and under all sector rotations.'))
            elif broad:uncertain.append([a['id'],b['id']])
    for s in solids+retained:del s['_aabb']
    fit=dict(status='FAIL' if collisions or unplaced_welds else 'UNKNOWN',materialWitnesses=collisions,broadBoxCandidatesWithoutWitness=uncertain,checkedPairs=paircount,knownNewAndRepositionedBodyCount=len(solids),retainedKnownBodyCount=len(retained),unsupportedRequestedWeldEdges=unplaced_welds,nominalStacks=stacks,cuffFiniteTM=[-.2,.2],bothCaps='Every positive witness explicitly mirrored; geometry identity under37 rotations. No opposite-cap or neighbor-sector clearance PASS.',wholeConstructionClearance=None,boltInsertionAndSocketSweeps=None,unknownRetainedGeometry=['Unspecified I033 webs/gussets/cover apertures/bolt head poses','Other retained pooled contact/backer/weld/access stock without full individual installed solids','Hex corners, real threads, fillet volumes, installation trajectories and all neighbor-sector sweeps'],qualification='Strict witnesses establish local interference only. Fixed125-point sampling cannot prove separation inside overlapping enclosing boxes. Unknown/missing geometry never becomes clearance. Holes and bores are subtracted in witness tests; no stock mass credit. No geometry repaired.')

    # The complete six-component receiver/connection solution remains unresolved.
    # Compute known placed-subset source+gravity wrenches and every boundary's
    # own-stock gravity contribution; these are NOT an assigned reaction split.
    gm={x['id']:x for x in gravity};states=[]
    for saved in P['states']:
        assignment=next(x for x in P['pressureAssignments'] if x['id']==saved['assignment']);g=saved['gravityLocalMps2'];sector=saved['sector']
        fg=total([mul(g,x['massKg']) for x in gravity]);mg=total([cross(sub(x['pointXRTm'],O),mul(g,x['massKg'])) for x in gravity])
        fp=total([x['forceXRTn'] for x in assignment['sourceWrenches']]);mp=total([transport(x['forceXRTn'],x['coupleXRTnm'],x['pointXRTm'],O) for x in assignment['sourceWrenches']]);f=add(fp,fg);m=add(mp,mg)
        own=[]
        for b in boundaries:
            parts=[gm[k] for k in b['stockIDs'] if k in gm];bf=total([mul(g,x['massKg']) for x in parts]);bm=total([cross(sub(x['pointXRTm'],b['pointXRTm']),mul(g,x['massKg'])) for x in parts])
            own.append(dict(boundary=b['id'],componentStockSelfWeightForceXRTn=bf,componentStockSelfWeightMomentAboutBoundaryXRTnm=bm,completeForceXRTn=None,completeCoupleXRTnm=None,qualification='Only listed stock self-weight about this point, not the contact/cut reaction; source-sharing and other connected parts unresolved.'))
        receiverrefs={n:dict(pointXRTm=datums[n],forceXRTn=None,coupleAtReceiverXRTnm=None,knownPairMomentExpressedAtThisPointXRTnm=transport(mul(f,-1),mul(m,-1),O,datums[n]),qualification='Last vector is the entire known pair expressed at this origin; NOT the individual receiver moment.') for n in ['A','B']}
        states.append(dict(id=saved['id'],assignment=saved['assignment'],sector=sector,angleRad=saved['angleRad'],gravityLocalMps2=g,knownPlacedGravityForceXRTn=fg,knownPlacedGravityMomentAboutOXRTnm=mg,pressureForceXRTn=fp,pressureMomentAboutOXRTnm=mp,knownPlacedExternalForceXRTn=f,knownPlacedExternalMomentAboutOXRTnm=m,requiredKnownSubsetReceiverPairForceXRTn=mul(f,-1),requiredKnownSubsetReceiverPairMomentAboutOXRTnm=mul(m,-1),completeExternalForceXRTn=None,completeExternalMomentAboutOXRTnm=None,completeReceiverPairForceXRTn=None,completeReceiverPairMomentAboutOXRTnm=None,unknownContribution='Displaced charged stock placement and older hull/global gravity; unresolved active assembly. Known subset is a necessary bookkeeping demand, not full equilibrium.',receiverReactions=receiverrefs,boundarySelfWeight=own,retainedMemberDemandSet='all31Unresolved',retainedFootDemandSet='all62Unresolved',retainedNodeDemandSet='all12Unresolved',rightCapGlobal=dict(origin=rotated(O,sector),force=rotated(f,sector),momentAboutOrigin=rotated(m,sector)),oppositeCapGlobal=dict(origin=reflected_point(O,sector),force=reflected_point(f,sector),momentAboutOrigin=reflected_couple(m,sector),requiredKnownSubsetPairForce=reflected_point(mul(f,-1),sector),requiredKnownSubsetPairMoment=reflected_couple(mul(m,-1),sector))))
    assert len(states)==74 and len({s['id'] for s in states})==74
    summary=dict(status='FAIL / UNKNOWN; physical float NOT SHOWN',retainedTubeCount=31,retainedFootLocations=62,pressureAssignments=2,gravityOrientations=37,states=74,physicalModules=74,newStockRows=len(stock),newStockT=new_t,conditionalRemovedT=removed_t,deltaHullT=new_t-removed_t,knownHullT=hull,knownSubtotalT=subtotal,qualifiedRetirementT=0.,materialWitnesses=len(collisions),unsupportedRequestedWeldEdges=len(unplaced_welds),actualWeldLines=len(welds),boundaries=len(boundaries),completeReceiverReaction=None,fullCapacity=None,physicalFloat=None)
    output=dict(unit='R3-I037',baselineSha256=sha(U/'baseline.json'),sourcesSha256=sha(U/'sources.json'),calculatorSha256=sha(Path(__file__)),selectedHypothesis=D['id'],geometry=dict(datumsXRTm=datums,newFiniteSolids=solids,retainedKnownFiniteSolids=retained,retained31Members=P['geometry']['members'],retained62Feet=P['geometry']['feet'],finiteCuffs=[x for x in PB['inheritedGeometry']['solids'] if x['name'] in ['A receiving cuff','B receiving cuff']],linerContacts=contacts,actualWeldLines=welds,requestedUnsupportedWeldStock=unplaced_welds,stacks=stacks),stock=dict(newItems=stock,beforeRows=before,conditionalDisplacedRows=removed,displacedStillChargedRows=accounting,retainedI024Rows=PB['massBasis']['priorRows'],gravityDisposition=gravity_disposition,retainedBackers=retained_backers),mass=newmass,fixedPressureAndFilm=P['fixedPressureAndFilm'],pressureAssignments=P['pressureAssignments'],localStockGravitySources=gravity,demandBoundaries=boundaries,retainedDemandSets=P['demandSets'],states=states,fit=fit,inheritedFit=P['fit'],inheritedFailures=P['inheritedFailures'],inheritedUnresolved=P['unresolved'],conventions=dict(originXRTm=O,rightHanded='X cross R = T',momentTransport='M_Q=M_P+(P-Q) cross F',oppositeForce='Q=diag(-1,1,1), followed by sector rotation',oppositeAxialMoment='det(Q)Q=diag(1,-1,-1), followed by sector rotation',states='2 pressure alternatives x37 gravity orientations; physical stock repeated74 once, not148',sign='External source loads on module; reaction on module is minus their known sum. Opposite force/couple acts on support. No source-applied wrench is called bolt tension.',unknown='null is UNKNOWN, never a zero load, equal A/B split or free stiffness'),summary=summary,weakestAssumption='The actual finite0.400m cuffs and their ring attachments can accept the complete3D saddle reactions without unproved slip, rotation, ovalisation or peel. That capacity and the A/B split remain UNKNOWN.',nextUntestedHypothesis='A separately paid local ring doubler/diaphragm tied to the actual saved receiving frame at unchanged A/B datums; geometry requires a separate future issue.',computation=dict(designs=1,sweeps=0,solvers=0,ancestorImports=0,drawings=0),qualification='One fixed failed/unqualified construction. No qualified retirement, full contact/fastener/frame capacity, global stiffness, complete all-up mass, loaded shape or physical float established. All inherited failures survive.')
    (U/'saddle.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2),flush=True);print('SCIENCE_COMPLETED',flush=True)

if __name__=='__main__': main()
