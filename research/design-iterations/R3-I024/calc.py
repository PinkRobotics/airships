#!/usr/bin/env python3
"""One selected 3D polar-node construction; frozen pressure loads, no ancestor run.

All statics are conditional demands. Explicit receiver force/couple requirements
do not establish their installed stiffness or capacity. No matrix solver is used.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
O = [40., 0., 0.]
RS, RC, RA, RL = 7850., 1600., 1200., 1100.
ES, EC, FY, FC = 200e9, 135e9, 355e6, 1450e6
REPEAT = 74
ALPHA = 2*math.pi/37
EX, ER, ET = [1.,0.,0.], [0.,1.,0.], [0.,0.,1.]


def add(a,b): return [x+y for x,y in zip(a,b)]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def mul(k,a): return [k*x for x in a]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a): return math.sqrt(dot(a,a))
def unit(a): return mul(1/norm(a),a)
def embed(a): return [a[0],a[1],0.]
def sumv(rows):
    rows=list(rows)
    return [sum(v[k] for v in rows) for k in range(3)]
def close(a,b=0.,tol=1e-5):
    assert math.isclose(a,b,abs_tol=tol,rel_tol=1e-9),(a,b)
def cross2(a,b): return a[0]*b[1]-a[1]*b[0]
def frame(axis):
    e=unit(axis);p=unit(sub(ET,mul(dot(ET,e),e)));n=cross(p,e)
    return [e,n,p]
def at(p,e,s): return add(p,mul(s,e))
def relocate(force,couple,source,target): return add(couple,cross(sub(source,target),force))
def moment_at(force,moment_o,point): return sub(moment_o,cross(sub(point,O),force))
def pair_xr(u,v,force):
    d=cross2(u,v);assert abs(d)>1e-7
    a=-cross2(force,v)/d;b=-cross2(u,force)/d
    r=add(force,add(mul(a,u),mul(b,v)))
    close(r[0]);close(r[1])
    return a,b
def tube(od,t,rho=RC):
    bore=od-2*t;a=math.pi*(od**2-bore**2)/4;i=math.pi*(od**4-bore**4)/64
    return dict(odM=od,wallM=t,areaM2=a,inertiaM4=i,sectionModulusM3=2*i/od,polarMomentM4=2*i,kgPerM=a*rho)
def box(size,t):
    a=size**2-(size-2*t)**2;i=(size**4-(size-2*t)**4)/12
    return dict(sizeM=size,wallM=t,areaM2=a,inertiaM4=i,sectionModulusM3=2*i/size,medianEnclosedAreaM2=(size-t)**2,kgPerM=a*RS)
def annulus(od,bore,length,rho=RS): return math.pi*(od**2-bore**2)*length*rho/4
def bolt(d,length):
    af,head,nut,wo,wi,wt={.024:(.036,.015,.019,.044,.026,.004),.012:(.019,.008,.010,.024,.013,.0025),.008:(.013,.0055,.0065,.016,.0084,.0016)}[d]
    ha=math.sqrt(3)*af*af/2
    return RS*(math.pi*d*d*length/4+ha*head+(ha-math.pi*d*d/4)*nut)+2*annulus(wo,wi,wt)


def section(force,moment,axis,sec,length,steel=False):
    axial=dot(force,axis);torque=dot(moment,axis);bending=norm(sub(moment,mul(torque,axis)))
    normal=abs(axial)/sec['areaM2']+bending/sec['sectionModulusM3']
    if 'medianEnclosedAreaM2' in sec:
        shear=abs(torque)/(2*sec['medianEnclosedAreaM2']*sec['wallM'])
    else:shear=abs(torque)*(sec['odM']/2)/sec['polarMomentM4']
    e=ES if steel else EC;ceiling=FY if steel else FC
    buckling=math.pi**2*e*sec['inertiaM4']/length**2
    return dict(signedAxialN=axial,transverseForceN=norm(sub(force,mul(axial,axis))),bendingMomentNm=bending,torqueNm=torque,additiveNormalStressPa=normal,torsionShearPa=shear,nominalNormalCeilingPa=ceiling,normalProxyPass=normal<=ceiling,pinEulerN=buckling,pinEulerPass=axial>=0 or -axial<=buckling,combinedCapacity=None,scope='Conditional section demand; unqualified material, restraint, local buckling, shear interaction and connection. Pin Euler is not global pressure stability.')


def transfer_section(source_force,source_moment,axis,sec,length,steel=False):
    # Positive axis runs from the loaded source to the receiver. Equilibrium
    # of the source-side cut gives the opposite internal wrench. Thus a source
    # force pointing toward the receiver gives NEGATIVE axial compression.
    return dict(section(mul(-1,source_force),mul(-1,source_moment),axis,sec,length,steel),forceConvention='Tensile-positive internal cut wrench = minus the applied source-side wrench; axis source to receiver. External transfer/connection wrenches retain their physical signs.')


def pattern(count,r):
    return [[-r,-r],[-r,r],[r,-r],[r,r]] if count==4 else [[-r,-r],[-r,0],[-r,r],[0,-r],[0,r],[r,-r],[r,0],[r,r]]


def connection(force,couple,point,normal,count=4,d=.012,spacing=.050,weld=.320,leg=.008,grip=.030,length=.070,pattern_xy=None,backer_thickness=None):
    # An explicit elastic, bilateral bolt-group DEMAND idealization. Compression
    # contact, preload and prying are not established; no combined pass is given.
    u=unit(normal);v=unit(sub(ER,mul(dot(ER,u),u))) if abs(dot(u,ER))<.95 else unit(sub(EX,mul(dot(EX,u),u)))
    w=cross(u,v);xy=pattern_xy or pattern(count,spacing);assert len(xy)==count
    core={.008:.0065,.012:.0098,.024:.020}[d]
    area=math.pi*core*core/4;fx,fy,fn=dot(force,v),dot(force,w),dot(force,u)
    mx,my,mn=dot(couple,v),dot(couple,w),dot(couple,u)
    xx=sum(x*x for x,y in xy);yy=sum(y*y for x,y in xy);j=xx+yy
    bolts=[]
    for x,y in xy:
        axial=fn/count+mx*y/yy-my*x/xx
        shear=[fx/count-mn*y/j,fy/count+mn*x/j]
        centre=add(point,add(mul(x,v),mul(y,w)))
        af,ht,nt,wo,wi,wt,bw,bt={.008:(.013,.0055,.0065,.016,.0084,.0016,.030,.004),.012:(.019,.008,.010,.024,.013,.0025,.030,.006),.024:(.036,.015,.019,.044,.026,.004,.080,.012)}[d]
        bt=backer_thickness if backer_thickness is not None else bt
        bolts.append(dict(offsetVWm=[x,y],centreXRT=centre,axisXRT=u,shankCentreXRT=at(centre,u,(length-grip)/2-wt),shankLengthM=length,shankDiameterM=d,headCentreXRT=at(centre,u,-grip/2-wt-ht/2),headAcrossFlatsM=af,headThicknessM=ht,nutCentreXRT=at(centre,u,grip/2+wt+nt/2),nutAcrossFlatsM=af,nutThicknessM=nt,washerCentresXRT=[at(centre,u,s*(grip/2+wt/2)) for s in [-1,1]],washerODIDThicknessM=[wo,wi,wt],backerCentreXRT=at(centre,u,grip/2-bt/2),backerWidthHeightThicknessM=[bw,bw,bt],backerBoreM=wi,signedAxialN=axial,shearVWn=shear,tensileStressPa=max(0.,axial)/area,shearStressPa=norm(shear)/area))
    nut,washer,projection={.008:(.0065,.0032,.0024),.012:(.010,.005,.0036),.024:(.019,.008,.006)}[d]
    return dict(datumXRT=point,forceXRTn=force,coupleXRTnm=couple,planeNormalXRT=u,patternBasisVW=[v,w],boltCount=count,boltDiameterM=d,threadRootProxyM=core,boltLengthM=length,actualSelectedGripM=grip,nutPlusWashersProjectionM=nut+washer+projection,lengthAllowanceM=length-grip-nut-washer-projection,boltGripPass=length>=grip+nut+washer+projection,boltGroup=bolts,maximumConditionalBoltTensionPa=max(b['tensileStressPa'] for b in bolts),maximumConditionalBoltShearPa=max(b['shearStressPa'] for b in bolts),forceOnlyMeanBoltShearPa=norm(force)/(count*area),actualFootWeldLengthM=weld,weldLegM=leg,forceOnlyMeanWeldShearPa=norm(force)/(.707*leg*weld),knownMomentMagnitudeNm=norm(couple),additionalWeldMomentStressPa=None,combinedConnectionPass=None,qualification='Explicit pattern gives conditional bilateral elastic bolt demands only. Plate contact, compression bearing, prying, preload, weld moment distribution and certified material/capacity are UNKNOWN. Opposite series end is never parallel resisting area.')


def series(force,moment_o,first,last,axis,**kw):
    m1=moment_at(force,moment_o,first);m2=moment_at(force,moment_o,last)
    residual=sub(add(cross(sub(first,O),force),m1),add(cross(sub(last,O),force),m2))
    close(norm(residual))
    return dict(forceFromSourceToReceiverXRTn=force,sourceMomentAboutONm=moment_o,first=connection(force,m1,first,axis,**kw),last=connection(mul(-1,force),mul(-1,m2),last,axis,**kw),deliveredReceiverCoupleXRTnm=m2,momentIdentityResidualNm=norm(residual),forceResidualN=0.,stockAtEachEndSeparate=True,combinedConnectionPass=None)


def make_geometry(old):
    nodes={k:embed(v) for k,v in old['geometry']['nodesXR'].items()}
    shifts_t={'AD':[-.25,-.50],'BD':[-.25,0.],'DC':[.50,.25],'BC':[.25,-.25]}
    shifts_x={'AD':[0.,0.],'BD':[0.,0.],'DC':[0.,-.35],'BC':[0.,.35]}
    members=[];roots=[];solids=[]
    def solid(name,kind,c,axes,dims,group,**kw):
        row=dict(name=name,kind=kind,centreXRT=c,axes=axes,dimensionsM=dims,group=group,**kw);solids.append(row);return row
    receiver={k:[old['geometry']['lastFrame']['xM']-.179,nodes[k][1],0.] for k in ['A','B']}
    receiver_frame={k:[old['geometry']['lastFrame']['xM'],nodes[k][1],0.] for k in ['A','B']}
    for prev in old['geometry']['members']:
        name=prev['name'];pins=[add(embed(p),[shifts_x[name][i],0.,shifts_t[name][i]]) for i,p in enumerate(prev['pinCentresXR'])]
        axis=unit(sub(pins[1],pins[0]));length=norm(sub(pins[1],pins[0]));axes=frame(axis);e,n,p=axes
        carbon=length-.500 if name!='AD' else None
        member=dict(name=name,pinCentresXRT=pins,axisXRT=axis,pinAxisXRT=p,pinLengthM=length,oldPinLengthM=prev['pinLengthM'],carbonCutM=carbon,carbonIntervalM=[.250,length-.250] if carbon else None,insertIntervalsM=[[.250,.550],[length-.550,length-.250]] if carbon else [],insertFit=carbon>=.600 if carbon else True,oldInsertGapM=prev['insertGapM'],dedicatedCartridge=name=='AD')
        if name=='AD':
            member.update(neckDiameterM=.180,attachmentDepthEachM=.160,freeNeckLengthM=length-.320,fullBilletDiameterM=.220,fullBilletLengthM=length+.220,axialComplianceMPerN=(length-.320)/(ES*math.pi*.180**2/4),bearingAndShoulderCompliance=None,eyeToShoulderBoundaryFromPinM=.110,eyeChordAtShoulderM=0.,finiteEyeShoulderLoadPathPass=False,attachment='Attempted machined billet:180mm neck,two80mm-thick220OD eyes with102mm bores,50mm-long180OD shoulders starting110mm from pins. The represented eye ends exactly at that110mm tangent:zero-area eye/shoulder contact FAIL. No fillet or enlarged transition is silently added. Full billet/trim remains charged; neck-only stiffness is conditional, not a continuous installed cartridge.')
            solid('AD neck','cylinder',mul(.5,add(*pins)),axes,[length-.320,.180,.180],'member-AD')
        else:
            solid(name+' carbon','tube',mul(.5,add(*pins)),axes,[carbon,.350,.350],'member-'+name,innerDiameterM=.310)
        for i,pin in enumerate(pins):
            toward=axis if i==0 else mul(-1,axis);ax=frame(toward);ee,nn,pp=ax
            node=name[i];rootgroup='root-'+name+'-'+node;membergroup='member-'+name
            if name=='AD':
                solid(name+' eye '+node,'cylinder',pin,[pp,ee,nn],[.080,.220,.220],membergroup,innerDiameterM=.102)
                solid(name+' shoulder '+node,'cylinder',at(pin,toward,.135),ax,[.050,.180,.180],membergroup)
            else:
                solid(name+' eye '+node,'box',at(pin,toward,.075),ax,[.350,.220,.080],membergroup,holes=[dict(axis=2,centreLocal=[-.075,0.,0.],radiusM=.051)])
                solid(name+' end plate '+node,'cylinder',at(pin,toward,.240),ax,[.020,.400,.400],membergroup)
                solid(name+' insert '+node,'tube',at(pin,toward,.400),ax,[.300,.309,.309],membergroup,innerDiameterM=.285)
            solid(name+' pin '+node,'cylinder',pin,[pp,ee,nn],[.220,.100,.100],rootgroup,pin=True)
            for side in [-1,1]:
                solid(name+' cheek '+node+str(side),'box',add(at(pin,toward,-.050),mul(side*.058,pp)),ax,[.300,.220,.030],rootgroup,holes=[dict(axis=2,centreLocal=[.050,0.,0.],radiusM=.051)])
                solid(name+' washer '+node+str(side),'tube',at(pin,pp,side*.077),[pp,ee,nn],[.008,.140,.140],rootgroup,innerDiameterM=.102)
                solid(name+' retainer '+node+str(side),'tube',at(pin,pp,side*.099),[pp,ee,nn],[.012,.130,.130],rootgroup,innerDiameterM=.090)
                solid(name+' root gusset '+node+str(side),'box',add(at(pin,toward,-.250),mul(side*.110,pp)),ax,[.400,.250,.020],rootgroup)
            base=at(pin,toward,-.200)
            solid(name+' fork base '+node,'box',base,ax,[.030,.400,.300],rootgroup)
            if node in receiver:
                anchor=add(receiver[node],[0.,0.,pin[2]])
            else:
                size=.400 if node=='D' else .200
                side=1 if base[0]>=nodes[node][0] else -1
                anchor=add(nodes[node],[side*(size/2+.015),0.,pin[2]])
            arm_axis=unit(sub(base,anchor));arm_length=norm(sub(base,anchor))
            solid(name+' root stem '+node,'boxTube',mul(.5,add(base,anchor)),frame(arm_axis),[arm_length,.200,.200],rootgroup,innerSizeM=.160)
            solid(name+' root interface '+node,'box',anchor,[EX,ER,ET],[.030,.400,.300],rootgroup)
            roots.append(dict(member=name,node=node,pinXRT=pin,pinAxisXRT=pp,towardMemberXRT=toward,forkBaseXRT=base,anchorXRT=anchor,stemLengthM=arm_length,stemAxisXRT=arm_axis,eyeGapPerFaceM=.003,forkBearingCentreSpacingM=.116,pinOccupiedLengthM=.220,insertionDirectionXRT=pp,insertionTravelM=.300,rootBoltPatternRToffsetsM=pattern(4,.060),rootM24Count=4,rootM24LengthM=.120,rootGripM=.030+(.025 if node=='D' else .020 if node=='C' else .030)+.012,access='Pin inserted along positive local pin axis before both retainers; nuts/backers installed before box closure. Neighbour solids/access swept volume still require checking.'))
        if name=='AD':
            billet=dict(kind='cylinder',centreXRT=mul(.5,add(*pins)),axes=axes,dimensionsM=[member['fullBilletLengthM'],.220,.220])
            witnesses=[]
            for i,pin in enumerate(pins):
                local=[0.,.108,.030];ax=frame(axis if i==0 else mul(-1,axis))
                point=add(pin,sumv(mul(v,a) for v,a in zip(local,ax)))
                eye=next(s for s in solids if s['name']=='AD eye '+name[i])
                witnesses.append(dict(eye=eye['name'],eyeLocalENPm=local,pointXRT=point,insideSelectedEyeMaterial=solid_contains(eye,point),insideSelectedBillet=solid_contains(billet,point),billetRadialSquaredM2=local[1]**2+local[2]**2,billetRadiusSquaredM2=.110**2))
            assert all(w['insideSelectedEyeMaterial'] and not w['insideSelectedBillet'] for w in witnesses)
            member['billetContainment']=dict(status='FAIL',selectedEyeContainedInPaidBlank=False,witnesses=witnesses,qualification='The longitudinal 220mm billet cannot contain the represented 220OD x80mm transverse eyes: n^2+p^2 exceeds its radius squared. Paid blank and trim are a stock allowance, not a fabricatable one-piece cartridge. The separate zero-area eye/shoulder contact FAIL remains; no bigger blank, bridge or free material is added.')
        members.append(member)
    sd=add(nodes['D'],[-.600,-.200,0.]);sc=add(nodes['C'],[-.600,-.200,0.]);spine=unit(sub(sc,sd));spine_length=norm(sub(sc,sd));mid=mul(.5,add(sd,sc))
    attachments={k:add(nodes[k],[-(.215 if k=='D' else .115),0.,0.]) for k in ['D','C']}
    collector=dict(D=sd,C=sc,nodeAttachmentsXRT=attachments,axisXRT=spine,lengthM=spine_length,box=box(.500,.020),spliceCentreXRT=mid,spliceGapM=.020,coverLengthM=.750,coverThicknessM=.020,boltsEachSeriesSpliceSide=16,totalSpliceM24=32,spliceBoltLengthM=.120,loadRoute='All C collector input passes through the spine to D, combines with D input, then goes through one finite arm to the A yoke. No equal division between A/B and no installed fixed support is inferred. B carries its own two main-member end forces/couples through its separate yoke/cuff.',receiverA=receiver['A'])
    for first,last,label,size,wall in [(sd,at(mid,spine,-.010),'collector D half',.500,.020),(at(mid,spine,.010),sc,'collector C half',.500,.020),(sd,receiver['A'],'collector A arm',.500,.020),(attachments['D'],sd,'collector D node arm',.300,.016),(attachments['C'],sc,'collector C node arm',.300,.016)]:
        solid(label,'boxTube',mul(.5,add(first,last)),frame(sub(last,first)),[norm(sub(last,first)),size,size],'collector',innerSizeM=size-2*wall)
    aa=frame(spine)
    for side_axis in [1,2]:
        for sign in [-1,1]:
            dims=[.750,.500,.500];dims[side_axis]=.020
            solid('collector splice cover '+str(side_axis)+str(sign),'box',at(mid,aa[side_axis],sign*.260),aa,dims,'collector')
    for node in ['A','B']:
        p=receiver[node];cf=receiver_frame[node]
        solid(node+' receiving cuff','tube',cf,[ET,EX,ER],[.400,.328,.328],'receiver-'+node,innerDiameterM=.296)
        solid(node+' receiver yoke','box',p,[EX,ER,ET],[.030,.300,1.000],'receiver-'+node)
        for sign in [-1,1]:
            solid(node+' yoke web '+str(sign),'box',add(p,[-.090,sign*.120,0.]),[EX,ER,ET],[.150,.020,1.000],'receiver-'+node)
        solid(node+' profiled receiver pad','box',add(cf,[-.114,0.,0.]),[EX,ER,ET],[.100,.300,.400],'receiver-'+node,removedCylinder=dict(centreXRT=cf,axisXRT=ET,radiusM=.164))
    for node,size,wall in [('D',.400,.025),('C',.200,.020)]:
        solid(node+' curved box ring','ringbox',[nodes[node][0],0.,0.],[EX,ER,ET],[size,2*(nodes[node][1]+size/2),2*(nodes[node][1]+size/2)],'ring-'+node,radiusM=nodes[node][1],sizeM=size,wallM=wall,ringIdentity=node)
        theta=ALPHA/2;radial=[0.,math.cos(theta),math.sin(theta)];tangent=[0.,-math.sin(theta),math.cos(theta)];centre=[nodes[node][0],nodes[node][1]*math.cos(theta),nodes[node][1]*math.sin(theta)]
        for axis,normal in [('axial',EX),('radial',radial)]:
            for sign in [-1,1]:
                face=at(centre,normal,sign*(size+wall)/2)
                aa=[tangent,radial,EX] if axis=='axial' else [tangent,EX,radial]
                solid(node+' ring splice '+axis+str(sign),'box',face,aa,[.304,size,wall],'ring-splice-'+node,attachmentRole='ringSpliceCover',attachedRingIdentity=node)
    dc=next(m for m in members if m['name']=='DC');pd,pc=dc['pinCentresXRT'];e=dc['axisXRT']
    stanchions=[]
    for row in old['filmLoadPath']['rows'][1:-1]:
        h=embed(row['collectorCentreXR']);n=[math.sin(row['phiRad']),math.cos(row['phiRad']),0.]
        # Intersect the inward normal with the actual DC projection; lift that
        # station onto its actual tangential coordinate, giving a canted post.
        t=cross2(sub(h,pd),n)/cross2(e,n);q=at(pd,e,t);a=unit(sub(q,h));length=norm(sub(q,h))
        hdepth=.066/math.sqrt(1-dot(a,ET)**2);bdepth=.193/math.sqrt(1-dot(a,e)**2)
        source=at(h,a,hdepth);target=at(q,a,-bdepth)
        available=length-hdepth-bdepth-.124
        selected=max(.080,available);start=at(source,a,.062);end=at(start,a,selected)
        group='stanchion-'+str(row['row'])
        solid(group+' carbon','tube',mul(.5,add(start,end)),frame(a),[selected,.100,.100],group,innerDiameterM=.084)
        solid(group+' beam cuff','tube',q,frame(e),[.200,.386,.386],group,innerDiameterM=.354)
        solid(group+' hoop cuff','tube',h,[ET,EX,ER],[.080,.132,.132],group,innerDiameterM=.110)
        for label,point,sense in [('hoop',source,1),('beam',target,-1)]:
            aa=frame(mul(sense,a))
            solid(group+' base '+label,'box',at(point,a,sense*.012),aa,[.024,.160,.160],group)
            solid(group+' socket '+label,'tube',at(point,a,sense*.112),aa,[.100,.083,.083],group,innerDiameterM=.069)
        stanchions.append(dict(row=row['row'],hoopCentreXRT=h,beamAxisPointXRT=q,axisXRT=a,axisLengthM=length,normalProjectionStationM=t,normalVectorXRT=n,sourceCuffSurfaceXRT=source,receiverCuffSurfaceXRT=target,shoeDepthEachM=.062,availableTubeLengthM=available,selectedTubeLengthM=selected,minimumCutM=.080,minimumCutPass=available>=.080,selectedClosureErrorM=selected-available,carbonStartXRT=start,carbonEndXRT=end,insertLengthEachM=.100,insertGapM=selected-.200,insertFit=selected>=.200,beamCuffIntervalM=[t-.100,t+.100],beamCarbonIntervalM=dc['carbonIntervalM'],beamInsertIntervalsM=dc['insertIntervalsM'],cuffWithinCarbon=t-.100>=.250 and t+.100<=dc['pinLengthM']-.250,betweenPins=0<=t<=dc['pinLengthM'],plateBoltsEach=4,plateWeldEachM=.320,beamCuffBoltsSeparate=8,hoopCuffBoltsSeparate=4,attachment='Each foot has mating 160x160x12 cuff pad/base, two160x30x8 webs,120x120x8 head and83/69x100 steel insert with90mm bond. Four M12 per end; two160mm 8mm base welds per end. Separate head/insert welds and cuff hardware are charged.'))
        foot=next(s for s in solids if s['name']==group+' base hoop')
        half_t=sum(abs(dot(ET,u))*d/2 for u,d in zip(foot['axes'],foot['dimensionsM']))
        centre_t=dot(sub(foot['centreXRT'],h),ET);foot_bounds=[centre_t-half_t,centre_t+half_t]
        source_t=dot(sub(source,h),ET);gap=max(foot_bounds[0]-.040,-.040-foot_bounds[1],0.)
        source_in_domain=abs(source_t)<=.040
        stanchions[-1]['finiteHoopCuffAttachment']=dict(sourceDatumConvention='Intersection with infinite 132OD cylinder, not necessarily the selected finite 80mm cuff material.',sourceAxialCoordinateM=source_t,finiteCuffAxialIntervalM=[-.040,.040],sourcePointInFiniteAxialDomain=source_in_domain,footName=foot['name'],completePadBaseAxialBoundsM=foot_bounds,provedAxialMaterialGapM=gap,finiteMaterialGapPass=gap==0.,connectionFitStatus='FAIL' if gap>0. or not source_in_domain else 'UNKNOWN',qualification='A positive axial gap proves the complete 160x160x24 pad/base cannot touch the finite cuff. An overlapping bound alone does not prove a joined interface. Source outside the finite domain also fails the stated cuff-surface datum. Existing stock/datums retained; no bridge or longer cuff. Socket and beam-carbon footprint failures are separate.')
    root=old['filmLoadPath']['rows'][0];new=embed(root['barPinXR'])
    last=old['geometry']['lastFrame'];previous=[last['xM'],last['surfaceRadiusM']-.0215,0.]
    delta=sub(new,previous);n=[-math.sin(root['phiRad']),-math.cos(root['phiRad']),0.]
    web_first=at(previous,n,.008);web_last=at(new,n,-.008);web_axis=unit(sub(web_last,web_first));web_length=norm(sub(web_last,web_first))
    adapter=dict(oldInterfaceXRT=previous,newInterfaceXRT=new,normalXRT=n,normalStepM=dot(delta,n),tangentStepM=dot(delta,cross(ET,n)),platesM=[.160,.120,.008],webWidthThicknessM=[.100,.012],webLengthM=web_length,webAxisXRT=web_axis,webCentresXRT=[add(mul(.5,add(web_first,web_last)),[0.,0.,s*.035]) for s in [-1,1]],boltsEachFoot=4,boltDiameterM=.008,boltLengthM=.050,gripM=.024,weldEachFootM=.400,weldLegM=.004,source='Incoming old bar reaction only. Other new root bar remains separately attached; full row has both actual incident vectors.',closureVectorM=sub(add(previous,delta),new))
    for i,p in enumerate([at(previous,n,.004),at(new,n,-.004)]):solid('root adapter plate'+str(i),'box',p,frame(n),[.008,.160,.120],'root-adapter')
    for i,p in enumerate(adapter['webCentresXRT']):solid('root adapter web'+str(i),'box',p,frame(web_axis),[web_length,.100,.012],'root-adapter')
    adapter_templates=[s for s in solids if s['group']=='root-adapter']
    solids[:]=[s for s in solids if s['group']!='root-adapter']
    for column in range(18):
        theta=(column-8.5)*2*math.pi/666
        for s in adapter_templates:
            solids.append(dict(s,name=s['name']+' column'+str(column),centreXRT=rotate(s['centreXRT'],theta),axes=[rotate(v,theta) for v in s['axes']],group='root-adapter-'+str(column)))
    adapter['columnAnglesWithinSectorRad']=[(column-8.5)*2*math.pi/666 for column in range(18)]
    adapter['representativeFrame']='Typical bar meridian; actual18 columns at(k-8.5)*2pi/666 relative to support meridian. Rotate both force and couple vectors together.'
    button_source=embed(old['localScreens']['button']['seriesPlateFeet']['sourceDatumXR']);button_axis=unit(sub(sc,button_source));bl=norm(sub(sc,button_source))
    button=dict(sourceXRT=button_source,receiverXRT=sc,axisXRT=button_axis,axisLengthM=bl,boxCutM=max(.080,bl-.140),availableBoxCutM=bl-.140,section=box(.300,.016),feetEachM=[.400,.400,.020],boltsEachFoot=8,boltDiameterM=.024,boltLengthM=.140,boltPatternRadiusM=.160,weldEachFootM=1.200,weldLegM=.010,gripM=.080,sourceKnownStackM=.072,sourceSelectedPackingM=.008,unbridgedPlatePadToBoxGapEachM=.040,attachment='Each foot:400x400x20 plate,eightM24 on320mm square perimeter,20mm profiled pad/backers. The box starts70mm from each foot datum; plate plus forward pad reaches30mm, leaving40mm unsupported at each end:FAIL, no free stub. Source72mm known grip plus8mm selected full packing equals80mm; receiver80mm. Stated weld demand is conditional because the selected gap prevents its installation. Curved shell/collector-wall support remain unqualified.')
    solid('button support','boxTube',mul(.5,add(button_source,sc)),frame(button_axis),[button['boxCutM'],.300,.300],'button-support',innerSizeM=.268)
    for i,p in enumerate([button_source,sc]):
        solid('button plate'+str(i),'box',p,frame(button_axis),[.020,.400,.400],'button-support')
        solid('button profile pad'+str(i),'box',at(p,button_axis,.020 if i==0 else -.020),frame(button_axis),[.020,.400,.400],'button-support')
    return dict(coordinates='Right-handed local (X,R,T), X axial, R radial, T tangential; cross(X,R)=T. Embed old XR moments as +T. Rotate R/T for each of37 sectors; reflect X for opposite cap and transform couples as axial vectors.',nodesXRT=nodes,receiverYokesXRT=receiver,receivingFrameXRT=receiver_frame,members=members,roots=roots,collector=collector,stanchions=stanchions,rootAdapter=adapter,buttonSupport=button,solids=solids,repeatCount=REPEAT,sectorAngleRad=ALPHA,selectedGeometries=1,dimensionChoice='D pin planes -500/0/+500mm; C DC/BC planes+250/-250mm with -350/+350mm axial offsets. Same selection retained even if a solid/access or strength witness fails.',solidScope='Explicit pins/cheeks/washers/retainers/eyes/inserts/carbon, root and collector stock, yokes, post cuffs and adapter solids. Bolts/nuts/backers/weld paths and ring splices are separately dimensioned connection/stock records. Bounded collision witnesses do not certify all manufacturing/assembly tolerances.')


def load_case(g,old,fraction):
    members={m['name']:m for m in g['members']};nodes=g['nodesXRT']
    routes=[]
    for row in old['filmLoadPath']['rows']:
        full=embed(row['sectorForceXRN']);hoop=[0.,-(1-fraction)*full[1],0.]
        force=add(full,hoop);h=embed(row['collectorCentreXR'])
        mo=add([0.,0.,row['sectorMomentAboutCapCentreNm']],cross(sub(h,O),hoop))
        routes.append(dict(row=row['row'],forceXRTn=force,momentAboutOXRTnm=mo,hoopReactionXRTn=hoop,collectorCentreXRT=h))
    dc=members['DC'];pd,pc=dc['pinCentresXRT'];e=dc['axisXRT'];length=dc['pinLengthM']
    points=[];posts=[]
    for st in g['stanchions']:
        load=routes[st['row']];force=load['forceXRTn'];mo=load['momentAboutOXRTnm'];q=st['beamAxisPointXRT']
        couple=moment_at(force,mo,q);points.append(dict(row=st['row'],stationM=st['normalProjectionStationM'],pointXRT=q,forceXRTn=force,coupleXRTnm=couple))
        feet=series(force,mo,st['sourceCuffSurfaceXRT'],st['receiverCuffSurfaceXRT'],st['axisXRT'])
        tube_moments=[moment_at(force,mo,st['carbonStartXRT']),moment_at(force,mo,st['carbonEndXRT'])]
        screens=[transfer_section(force,m,st['axisXRT'],tube(.100,.008),st['selectedTubeLengthM']) for m in tube_moments]
        axial=abs(dot(force,st['axisXRT']))
        posts.append(dict(row=st['row'],plateFeet=feet,sectionEndpoints=screens,hoopCuffSourceCoupleXRTnm=moment_at(force,mo,st['hoopCentreXRT']),deliveredDCCoupleXRTnm=couple,steelInsertAxialStressPa=axial/(math.pi*(.083**2-.069**2)/4),meanInsertBondShearPa=axial/(math.pi*.083*.090),separateCuffSets=dict(beamM12=8,hoopM8=4,combinedCapacity=None),finiteHoopCuffAttachment=st['finiteHoopCuffAttachment'],fit=st['minimumCutPass'] and st['insertFit'] and st['cuffWithinCarbon'] and st['finiteHoopCuffAttachment']['connectionFitStatus']!='FAIL',fitQualification='False is a known necessary-geometry failure; true would not qualify the connection or prove finite material contact.'))
    total=sumv(p['forceXRTn'] for p in points)
    moment_d=sumv(add(cross(sub(p['pointXRT'],pd),p['forceXRTn']),p['coupleXRTnm']) for p in points)
    # Exact vector decomposition of the changed DC beam's applied wrench.
    # Its perpendicular moment is a force couple between actual pins; the
    # remaining axial torsion must pass through the D clevis bearing couple.
    fixed_c=mul(1/length,cross(moment_d,e));fixed_d=sub(total,fixed_c)
    torsion_d=mul(dot(e,moment_d),e)
    close(norm(sub(add(cross(sub(pc,pd),fixed_c),torsion_d),moment_d)))
    button_full=embed(old['filmLoadPath']['polarButtonSectorForceXRN'])
    button_hoop=[0.,-(1-fraction)*button_full[1],0.]
    hub=add(routes[-1]['forceXRTn'],add(button_full,button_hoop))
    bcaxis=members['BC']['axisXRT']
    ndc,nbc=pair_xr(mul(-1,e),mul(-1,bcaxis),add(hub,fixed_c))
    force_d=add(fixed_d,mul(ndc,e));force_c=sub(fixed_c,mul(ndc,e))
    nad,nbd=pair_xr(mul(-1,members['AD']['axisXRT']),mul(-1,members['BD']['axisXRT']),add(routes[0]['forceXRTn'],force_d))
    tensions=dict(AD=nad,BD=nbd,BC=nbc,DC_reference=ndc)
    end_forces={};end_couples={}
    for name,m in members.items():
        fs=[force_d,force_c] if name=='DC' else [mul(tensions[name],m['axisXRT']),mul(-tensions[name],m['axisXRT'])]
        for i,force in enumerate(fs):
            key=name+'-'+name[i];end_forces[key]=force;end_couples[key]=torsion_d if key=='DC-D' else [0.,0.,0.]
    root_screens=[]
    for root in g['roots']:
        key=root['member']+'-'+root['node'];force=end_forces[key];couple=end_couples[key]
        free_pin_component=dot(couple,root['pinAxisXRT']);close(free_pin_component)
        mc=relocate(force,couple,root['pinXRT'],root['anchorXRT'])
        eq_bearing=norm(force)/2+norm(couple)/root['forkBearingCentreSpacingM']
        root_screens.append(dict(member=root['member'],node=root['node'],forceOnRootXRTn=force,coupleAtPinXRTnm=couple,untransmittedPinAxisMomentNm=free_pin_component,requiredCoupleAtAnchorXRTnm=mc,conditionalForkBearingPa=eq_bearing/(.100*.030),forceOnlyPinDoubleShearPa=norm(force)/(2*math.pi*.100**2/4),conditionalPinBendingStressPa=(norm(force)*.116/4+norm(couple))/(math.pi*.100**3/32),eyeBearingPa=norm(force)/(.100*.080),forkNetSectionPa=norm(force)/(2*.030*(.220-.102)),rootStem=section(force,mc,root['stemAxisXRT'],box(.200,.020),max(.001,root['stemLengthM']),steel=True),rootBolts=connection(force,mc,root['anchorXRT'],EX,d=.024,spacing=.060,weld=.800,leg=.012,grip=root['rootGripM'],length=.120),combinedCapacity=None))
    samples=[]
    for station in sorted({0.,length,*[p['stationM'] for p in points]}):
        for side in ['before','after']:
            selected=[p for p in points if p['stationM']<station or (p['stationM']==station and side=='after')]
            location=at(pd,e,station)
            force=sub(force_d,sumv(p['forceXRTn'] for p in selected))
            external=add(mul(-1,torsion_d),cross(sub(pd,location),mul(-1,force_d)))
            external=add(external,sumv(add(cross(sub(p['pointXRT'],location),p['forceXRTn']),p['coupleXRTnm']) for p in selected))
            internal=mul(-1,external)
            samples.append(dict(stationM=station,side=side,internalForceXRTn=force,internalMomentXRTnm=internal,screen=section(force,internal,e,tube(.350,.020),length)))
    member_screens={}
    for name,m in members.items():
        if name=='DC':
            member_screens[name]=dict(maximumNormalStressPa=max(s['screen']['additiveNormalStressPa'] for s in samples),maximumTorsionShearPa=max(s['screen']['torsionShearPa'] for s in samples),maximumCompressionN=max(0.,-min(s['screen']['signedAxialN'] for s in samples)),normalProxyPass=all(s['screen']['normalProxyPass'] for s in samples),pinEulerPass=all(s['screen']['pinEulerPass'] for s in samples),combinedCapacity=None)
        else:
            sec=tube(.180,.090,RS) if name=='AD' else tube(.350,.020)
            member_screens[name]=section(mul(tensions[name],m['axisXRT']),[0.,0.,0.],m['axisXRT'],sec,m['pinLengthM'],steel=name=='AD')
    def node_wrench(node,load_force,load_mo):
        keys=[k for k in end_forces if k.endswith('-'+node)]
        force=add(load_force,sumv(end_forces[k] for k in keys))
        mo=add(load_mo,sumv(add(cross(sub(next(r['pinXRT'] for r in g['roots'] if r['member']+'-'+r['node']==k),O),end_forces[k]),end_couples[k]) for k in keys))
        return force,mo
    fd,md=node_wrench('D',routes[0]['forceXRTn'],routes[0]['momentAboutOXRTnm'])
    # The button physically enters at S_C. Excluding it here makes the C arm's
    # back-transfer explicit rather than applying the button twice.
    fc,mc=node_wrench('C',add(routes[-1]['forceXRTn'],button_hoop),add(routes[-1]['momentAboutOXRTnm'],cross(sub(nodes['C'],O),button_hoop)))
    sd,sc=g['collector']['D'],g['collector']['C'];a=g['receiverYokesXRT']['A']
    button=g['buttonSupport'];button_feet=series(button_full,[0.,0.,0.],button['sourceXRT'],sc,button['axisXRT'],count=8,d=.024,spacing=.160,weld=1.200,leg=.010,grip=.080,length=.140,backer_thickness=.020)
    button_screens=[transfer_section(button_full,moment_at(button_full,[0.,0.,0.],p),button['axisXRT'],button['section'],button['axisLengthM'],steel=True) for p in [button['sourceXRT'],sc]]
    collector_c_force=add(fc,button_full);collector_c_mo=mc
    combined_force=add(fd,collector_c_force);combined_mo=add(md,collector_c_mo)
    def transfer(label,force,mo,first,last,size,wall):
        axis=unit(sub(last,first));length=norm(sub(last,first));mom=[moment_at(force,mo,p) for p in [first,last]]
        close(norm(sub(relocate(force,mom[0],first,last),mom[1])))
        return dict(name=label,sourceXRT=first,receiverXRT=last,forceXRTn=force,momentAboutOXRTnm=mo,sourceCoupleXRTnm=mom[0],receiverCoupleXRTnm=mom[1],sectionEndpoints=[transfer_section(force,m,axis,box(size,wall),length,steel=True) for m in mom],feet=series(force,mo,first,last,axis,count=4,d=.024,spacing=.060,weld=4*size,leg=.010,grip=.060,length=.120),combinedCapacity=None)
    legs=[transfer('C ring to spine',fc,mc,g['collector']['nodeAttachmentsXRT']['C'],sc,.300,.016),transfer('C spine to D',collector_c_force,collector_c_mo,sc,sd,.500,.020),transfer('D ring to spine',fd,md,g['collector']['nodeAttachmentsXRT']['D'],sd,.300,.016),transfer('D spine to A yoke',combined_force,combined_mo,sd,a,.500,.020)]
    # Each side of the splice is in series: sixteen M24 on that side. The
    # covers provide a four-wall thin-section demand, not a qualified joint.
    splice_m=moment_at(collector_c_force,collector_c_mo,g['collector']['spliceCentreXRT']);sp=g['collector']['box'];axis=g['collector']['axisXRT']
    torque=dot(splice_m,axis);bending=norm(sub(splice_m,mul(torque,axis)))
    splice=dict(forceXRTn=collector_c_force,coupleXRTnm=splice_m,boltsEachSide=16,totalM24=32,forceOnlyMeanBoltShearEachSidePa=norm(collector_c_force)/(16*math.pi*.020**2/4),wallBendingCoupleForceN=bending/.480,wallTorsionShearFlowNPerM=abs(torque)/(2*.480**2),coverStressEnvelopePa=(abs(dot(collector_c_force,axis))/sp['areaM2']+bending/sp['sectionModulusM3']),additionalBoltMomentDistributionPa=None,combinedCapacity=None,qualification='Four 750x500x20 face covers; four M24 each side on each face, at longitudinal100/250mm and transverse+/-150mm. 20mm gap,365mm cover overlap each side. No opposite-side pooling; preload, local slip, wall bearing and cover interaction remain UNKNOWN.')
    receiving=[]
    for node in ['A','B']:
        keys=[k for k in end_forces if k.endswith('-'+node)]
        force=sumv(end_forces[k] for k in keys)
        mo=sumv(cross(sub(next(r['pinXRT'] for r in g['roots'] if r['member']+'-'+r['node']==k),O),end_forces[k]) for k in keys)
        if node=='A':force=add(force,combined_force);mo=add(mo,combined_mo)
        yf=g['receiverYokesXRT'][node];fr=g['receivingFrameXRT'][node];my=moment_at(force,mo,yf);mf=moment_at(force,mo,fr)
        receiving.append(dict(node=node,forceToFrameXRTn=force,coupleAtYokeXRTnm=my,coupleToInheritedFrameXRTnm=mf,frameDatumXRT=fr,oppositeFrameReactionXRTn=mul(-1,force),oppositeFrameReactionCoupleXRTnm=mul(-1,mf),yokePlateStripEnvelopePa=6*norm(my)/(.300*.030**2),cuffForceOnlyMeanContactPa=norm(force)/(.292*.400),eightM24=connection(force,my,yf,EX,count=8,d=.024,spacing=.060,weld=1.2,leg=.010,grip=.030+.012+.016+.012,length=.120,pattern_xy=[[r,t] for r in [-.060,.060] for t in [-.150,-.050,.050,.150]]),combinedReceiverCapacity=None,qualification='Known required wrench reaches the actual inherited receiver datum. Cuff grip, profiled pad, old frame/node and bending stiffness are unqualified; this is not a proved installed reaction.'))
    source_force=add(sumv(x['forceXRTn'] for x in routes),add(button_full,button_hoop))
    source_mo=add(sumv(x['momentAboutOXRTnm'] for x in routes),cross(sub(nodes['C'],O),button_hoop))
    delivered_force=sumv(r['forceToFrameXRTn'] for r in receiving)
    delivered_mo=sumv(add(cross(sub(r['frameDatumXRT'],O),r['forceToFrameXRTn']),r['coupleToInheritedFrameXRTnm']) for r in receiving)
    fr=norm(sub(source_force,delivered_force));mr=norm(sub(source_mo,delivered_mo));close(fr);close(mr)
    close(source_force[0],old['loadCases'][fraction]['totalAppliedForcePerSectorXRN'][0])
    close(source_force[1],old['loadCases'][fraction]['totalAppliedForcePerSectorXRN'][1])
    close(source_mo[2],old['loadCases'][fraction]['sourceMomentAboutCapCentreNm'])
    ad=g['rootAdapter'];incoming=embed(old['filmLoadPath']['rows'][0]['incidentBars'][1]['forceXRN']);adapter_mo=cross(sub(ad['oldInterfaceXRT'],O),incoming)
    adapter=series(incoming,adapter_mo,ad['oldInterfaceXRT'],ad['newInterfaceXRT'],ad['normalXRT'],count=4,d=.008,spacing=.035,weld=.400,leg=.004,grip=.024,length=.050)
    close(adapter['deliveredReceiverCoupleXRTnm'][2],old['filmLoadPath']['rows'][0]['rootStepMomentPerClipNm'])
    return dict(radialFraction=fraction,route='Existing radial assignment only; three-dimensional demand routing recalculated on actual displaced axes.',memberSignedTensionN=tensions,memberScreens=member_screens,dcPointLoads=points,dcEndForcesToNodesXRTn=[force_d,force_c],dcTorsionDeliveredAtDXRTnm=torsion_d,dcSections=samples,rootScreens=root_screens,nodeDCollectorInput=dict(forceXRTn=fd,momentAboutOXRTnm=md),nodeCCollectorInputWithoutButton=dict(forceXRTn=fc,momentAboutOXRTnm=mc),buttonSeparatePressureForceXRTn=button_full,buttonDownstreamHoopReactionXRTn=button_hoop,buttonFeet=button_feet,buttonSectionEndpoints=button_screens,collectorLegs=legs,collectorSplice=splice,stanchions=posts,rootAdapter=adapter,receiverDemands=receiving,totalAppliedForceXRTn=source_force,totalAppliedMomentAboutOXRTnm=source_mo,forceIdentityResidualN=fr,momentIdentityResidualNm=mr,requiredReceiverMomentsAreNotQualifiedReactions=True,physicalGlobalEquilibrium=None,pressureCapacityPa=None,fixedComparison=dict(rootEndBlockMomentNm=old['loadCases'][fraction]['rootEndBlockMomentNm'],polarEndBlockMomentNm=old['loadCases'][fraction]['polarEndBlockMomentNm'],unresolvedModuleMomentNm=old['loadCases'][fraction]['unresolvedModuleMomentNm'],buttonSourceCoupleNm=old['localScreens']['button']['seriesPlateFeet']['sourceCoupleNm'],buttonReceiverCoupleNm=old['localScreens']['button']['seriesPlateFeet']['receiverCoupleNm'],buttonSupportStressPa=old['localScreens']['button']['support']['additiveStressPa']),qualification='Conditional full wrench accounting only. New tangential forces and all couples are explicit; the old 2D member solution is not reused as proof. Material, connections, global stiffness and installed support reactions remain UNKNOWN.')


def rotate(v,theta):
    c,s=math.cos(theta),math.sin(theta)
    return [v[0],c*v[1]-s*v[2],s*v[1]+c*v[2]]


def solid_contains(s,point,margin=1e-7):
    delta=sub(point,s['centreXRT']);local=[dot(delta,a) for a in s['axes']];dims=s['dimensionsM']
    if s['kind']=='ringbox':
        x=abs(delta[0]);r=abs(math.hypot(point[1],point[2])-s['radiusM']);half=s['sizeM']/2
        return x<half-margin and r<half-margin and (x>half-s['wallM']+margin or r>half-s['wallM']+margin)
    if abs(local[0])>=dims[0]/2-margin:return False
    if s['kind'] in ['cylinder','tube']:
        r=math.hypot(local[1],local[2])
        if r>=dims[1]/2-margin or r<=s.get('innerDiameterM',0.)/2+margin:return False
    else:
        if any(abs(local[k])>=dims[k]/2-margin for k in [1,2]):return False
        if s['kind']=='boxTube' and all(abs(local[k])<s['innerSizeM']/2+margin for k in [1,2]):return False
    for hole in s.get('holes',[]):
        d=sub(local,hole['centreLocal'])
        if math.sqrt(sum(v*v for k,v in enumerate(d) if k!=hole['axis']))<=hole['radiusM']+margin:return False
    if 'removedCylinder' in s:
        c=s['removedCylinder'];d=sub(point,c['centreXRT']);radial=sub(d,mul(dot(d,c['axisXRT']),c['axisXRT']))
        if norm(radial)<=c['radiusM']+margin:return False
    return True


def solid_points(s):
    if s['kind']=='ringbox':return []
    dims=s['dimensionsM'];points=[]
    if s['kind'] in ['tube','cylinder']:
        r=(dims[1]+s.get('innerDiameterM',0.))/4
        for x in [-.4*dims[0],0.,.4*dims[0]]:
            for j in range(16):points.append([x,r*math.cos(j*math.pi/8),r*math.sin(j*math.pi/8)])
    else:
        for j in range(3):
            for sign in [-1,1]:
                for side in [-.35,0.,.35]:
                    p=[0.,0.,0.];p[j]=sign*dims[j]*.48;p[(j+1)%3]=side*dims[(j+1)%3];points.append(p)
    output=[add(s['centreXRT'],sumv(mul(q,a) for q,a in zip(p,s['axes']))) for p in points]
    return [p for p in output if solid_contains(s,p)]


def box_separated(a,b):
    d=sub(b['centreXRT'],a['centreXRT'])
    axes=a['axes']+b['axes']+[cross(u,v) for u in a['axes'] for v in b['axes']]
    for axis in axes:
        if norm(axis)<1e-9:continue
        extent=sum(abs(dot(axis,u))*v/2 for u,v in zip(a['axes'],a['dimensionsM']))+sum(abs(dot(axis,u))*v/2 for u,v in zip(b['axes'],b['dimensionsM']))
        if abs(dot(d,axis))>=extent+1e-7:return True
    return False


def segment_distance(p,q,a,b):
    # Closed finite-segment closest points; scalar dot products, no solve.
    u=sub(q,p);v=sub(b,a);w=sub(p,a);aa=dot(u,u);bb=dot(u,v);cc=dot(v,v);dd=dot(u,w);ee=dot(v,w);den=aa*cc-bb*bb
    candidates=[]
    if den>1e-14:
        s=(bb*ee-cc*dd)/den;t=(aa*ee-bb*dd)/den
        if 0<=s<=1 and 0<=t<=1:candidates.append((s,t))
    clamp=lambda x:max(0.,min(1.,x))
    candidates.extend([(0.,clamp(ee/cc)),(1.,clamp((ee+bb)/cc)),(clamp(-dd/aa),0.),(clamp((bb-dd)/aa),1.)])
    rows=[dict(distanceM=norm(sub(at(p,u,s),at(a,v,t))),firstFraction=s,secondFraction=t,firstPoint=at(p,u,s),secondPoint=at(a,v,t)) for s,t in candidates]
    return min(rows,key=lambda x:x['distanceM'])


def fit_witnesses(g,old):
    originals=g['solids'];next_sector=[]
    for s in originals:
        if s['kind']=='ringbox':continue
        copy=dict(s,centreXRT=rotate(s['centreXRT'],ALPHA),axes=[rotate(v,ALPHA) for v in s['axes']],name=s['name']+' [next sector]',group=s['group']+'-next')
        if 'removedCylinder' in s:
            c=s['removedCylinder'];copy['removedCylinder']=dict(c,centreXRT=rotate(c['centreXRT'],ALPHA),axisXRT=rotate(c['axisXRT'],ALPHA))
        next_sector.append(copy)
    collisions=[];overlap_bounds=[];separated=0;pairs=0;excluded=[]
    point_cache={s['name']:solid_points(s) for s in originals+next_sector}
    for i,a in enumerate(originals):
        for b in originals[i+1:]+next_sector:
            if a['group']==b['group']:continue
            # Ring covers intentionally overlap their own ring attachment;
            # their covers/bolts are not an unrelated collision claim.
            ring,cover=(a,b) if a['kind']=='ringbox' else (b,a)
            if ring['kind']=='ringbox' and cover.get('attachmentRole')=='ringSpliceCover' and ring['ringIdentity']==cover.get('attachedRingIdentity'):
                excluded.append(dict(first=a['name'],second=b['name'],ringIdentity=ring['ringIdentity'],reason='This specific splice cover attaches to this same continuous ring, including its periodic copy; connection capacity remains UNKNOWN.'))
                continue
            pairs+=1
            if box_separated(a,b):separated+=1;continue
            witness=next((p for p in point_cache[a['name']] if solid_contains(b,p)),None)
            if witness is None:witness=next((p for p in point_cache[b['name']] if solid_contains(a,p)),None)
            row=dict(first=a['name'],second=b['name'])
            if witness is not None:collisions.append(dict(row,pointXRT=witness,status='FAIL: the same interior point lies in both represented material solids.'))
            else:overlap_bounds.append(dict(row,status='UNKNOWN: occupied bounds overlap but finite point sampling proves no penetration; absence of a sampled witness is not clearance.'))
    pins=[s for s in originals if s.get('pin')];otherpins=[s for s in next_sector if s.get('pin')];pin_pairs=[]
    for i,a in enumerate(pins):
        for b in pins[i+1:]+otherpins:
            aa,bb=a['axes'][0],b['axes'][0]
            witness=segment_distance(at(a['centreXRT'],aa,-.110),at(a['centreXRT'],aa,.110),at(b['centreXRT'],bb,-.110),at(b['centreXRT'],bb,.110))
            pin_pairs.append(dict(first=a['name'],second=b['name'],**witness,sweptCylinderEnvelopeGapM=witness['distanceM']-.100,clearanceProved=witness['distanceM']>.100))
    access=[]
    for p in pins:
        axis=p['axes'][0];swept=dict(p,name=p['name']+' insertion sweep',centreXRT=at(p['centreXRT'],axis,.150),dimensionsM=[.520,.100,.100])
        blocking=[];bounds=[]
        samples=solid_points(swept)
        for s in originals+next_sector:
            if s['group']==p['group'] or box_separated(swept,s):continue
            witness=next((q for q in samples if solid_contains(s,q)),None)
            if witness:blocking.append(dict(solid=s['name'],pointXRT=witness))
            else:bounds.append(s['name'])
        access.append(dict(pin=p['name'],travelM=.300,provedObstructions=blocking,unresolvedBounds=bounds,status='FAIL' if blocking else 'UNKNOWN' if bounds else 'PASS for represented solids only'))
    all_reflect=[]
    # Polar/axial vectors transform differently under the opposite-cap mirror.
    for force,moment in [([1.,2.,3.],[4.,5.,6.])]:
        p=[7.,8.,9.];mirror=lambda v:[-v[0],v[1],v[2]];axial=lambda v:[v[0],-v[1],-v[2]]
        close(norm(sub(cross(mirror(p),mirror(force)),axial(cross(p,force)))))
        all_reflect.append(dict(forceRule='(-Fx,Fr,Ft)',coupleRule='(Mx,-Mr,-Mt)',crossProductIdentityPass=True))
    return dict(selectedSolidCount=len(originals),comparisonPairs=pairs,separatedByFiniteBounds=separated,excludedIntendedRingCoverPairs=excluded,materialIntersectionWitnesses=collisions,unresolvedOverlapBounds=overlap_bounds,collisionProofScope='Each FAIL has an explicit point strictly inside both declared material shapes, including hollow sections/holes. SAT separation proves only represented bound separation. Connected groups and enumerated same-ring covers omitted; no broad assembly/pressure qualification.',pinPairs=pin_pairs,minimumPinEnvelopeGapM=min(p['sweptCylinderEnvelopeGapM'] for p in pin_pairs),pinInsertionAccess=access,shortStanchions=[s['row'] for s in g['stanchions'] if not s['minimumCutPass']],insertOverlapStanchions=[s['row'] for s in g['stanchions'] if not s['insertFit']],cuffsOutsideCarbon=[s['row'] for s in g['stanchions'] if not s['cuffWithinCarbon']],finiteHoopCuffSourceDomainFailures=[s['row'] for s in g['stanchions'] if not s['finiteHoopCuffAttachment']['sourcePointInFiniteAxialDomain']],finiteHoopCuffMaterialGapFailures=[s['row'] for s in g['stanchions'] if not s['finiteHoopCuffAttachment']['finiteMaterialGapPass']],adBilletContainment=next(m for m in g['members'] if m['name']=='AD')['billetContainment'],rootAdapterClosureNormM=norm(g['rootAdapter']['closureVectorM']),oppositeCapReflection=all_reflect,originalPinIntersectionWitnesses=old['clearance']['centredPinPairs'],originalADInsertGapM=old['geometry']['members'][0]['insertGapM'],originalRootAdapter=old['clearance']['rootDatumAdapter'],qualification='Any remaining material penetration, finite attachment gap, stock-containment failure or access obstruction invalidates the selected assembly. Unresolved overlap bounds remain UNKNOWN, not a clearance PASS.')


def changed_hardware(g,old):
    """Price the selected plate blanks and annular collars, once per kit.

    Plate bores remove material from full rectangular stock: charge that trim.
    Collar stock is the declared 130/90 annulus, not a free solid-cylinder bore.
    Unchanged components retain their explicit predecessor allocations; this
    correction does not rewrite accepted predecessor rows or all fabrication.
    """
    hw=old['hardware'];solids=g['solids']
    eyes=[s for s in solids if any(s['name'].startswith(n+' eye ') for n in ['BD','DC','BC'])]
    cheeks=[s for s in solids if ' cheek ' in s['name']]
    retainers=[s for s in solids if ' retainer ' in s['name']]
    assert len(eyes)==6 and len(cheeks)==16 and len(retainers)==16
    def component(selected,per_kit,kit_count,prior):
        parts=[]
        for s in selected:
            if s['kind']=='box':
                stock=math.prod(s['dimensionsM'])*RS
                trim=sum(math.pi*h['radiusM']**2*s['dimensionsM'][h['axis']]*RS for h in s.get('holes',[]))
                convention='Full selected rectangular plate blank charged; actual bore removal retained as charged trim.'
            else:
                assert s['kind']=='tube'
                stock=annulus(s['dimensionsM'][1],s['innerDiameterM'],s['dimensionsM'][0]);trim=0.
                convention='Selected annular 130/90 tube stock at 12mm length; no unselected solid-billet or extra cutting allowance claimed.'
            parts.append(dict(solid=s['name'],dimensionsM=s['dimensionsM'],holes=s.get('holes',[]),innerDiameterM=s.get('innerDiameterM'),selectedNetEachKg=stock-trim,chargedStockEachKg=stock,chargedTrimEachKg=trim,convention=convention))
        first=parts[0]
        for part in parts[1:]:
            close(part['selectedNetEachKg'],first['selectedNetEachKg']);close(part['chargedStockEachKg'],first['chargedStockEachKg'])
        return dict(parts=parts,countPerKit=per_kit,kitCount=kit_count,totalPartCount=per_kit*kit_count,priorAllocationPerKitKg=prior,selectedNetPerKitKg=per_kit*first['selectedNetEachKg'],chargedStockPerKitKg=per_kit*first['chargedStockEachKg'],chargedTrimPerKitKg=per_kit*first['chargedTrimEachKg'],deltaChargedPerKitKg=per_kit*first['chargedStockEachKg']-prior)
    old_end=hw['partsKg']['mainEnd'];old_root=hw['partsKg']['mainRoot']
    changed=dict(centredEye=component(eyes,1,444,old_end['centredEye']),twoForkCheeks=component(cheeks,2,592,old_root['twoForkCheeks']),retainers=component(retainers,2,592,old_root['retainers']))
    kits={}
    for name,prior,keys,count in [('mainEnd',old_end,['centredEye'],444),('mainRoot',old_root,['twoForkCheeks','retainers'],592)]:
        parts=dict(prior)
        for key in keys:parts[key]=changed[key]['chargedStockPerKitKg']
        close(sum(prior.values()),hw['eachKg'][name])
        each=sum(parts.values())
        kits[name]=dict(count=count,priorPartsKg=prior,correctedChargedPartsKg=parts,changedComponents=keys,unchangedComponents=[k for k in prior if k not in keys],priorEachKg=hw['eachKg'][name],correctedEachKg=each,deltaEachKg=each-hw['eachKg'][name],priorTotalT=count*hw['eachKg'][name]/1000,correctedTotalT=count*each/1000,deltaTotalT=count*(each-hw['eachKg'][name])/1000)
    return dict(components=changed,kits=kits,totalAddedStockCorrectionT=sum(k['deltaTotalT'] for k in kits.values()),qualification='Actual selected solids determine changed components. Charged plate stock = net material + retained bore trim; annular collars use selected net tube stock. All other kit allocations remain identified, counted once, and unqualified as fabrication estimates. No predecessor mass, retirement, selected solid or pressure load is changed.',gravityLoads='No gravity or mass-derived demand is used in this pressure-only calculation; no dependent gravity screen is silently left stale.')


def ledger(g,old):
    rows=[]
    def item(name,count,each,dimensions,duty):
        assert count>=0 and each>=0
        rows.append(dict(item=name,count=count,eachKg=each,massT=count*each/1000,dimensions=dimensions,duty=duty))
    hw=old['hardware'];members={m['name']:m for m in g['members']};hardware=changed_hardware(g,old)
    ad=members['AD']
    item('AD one-piece machined cartridge billet',74,math.pi*.220**2/4*ad['fullBilletLengthM']*RS,'220mm full round billet, pin spacing+220mm stock; intended180mm neck,80mm eyes,102mm bores','Priced blank only: FAIL to contain the selected transverse eyes; also zero-area eye/shoulder contact. All blank stock retained, no free added material or fabricated-cartridge claim.')
    for name in ['BD','DC','BC']:item('main carbon '+name,74,members[name]['carbonCutM']*tube(.350,.020)['kgPerM'],'350x20, actual displaced pin length minus500mm','Changed member cut; both caps')
    item('BD DC BC end assemblies',444,hardware['kits']['mainEnd']['correctedEachKg'],'309/285x300 inserts,290mm bond,400x20 plates;350x220x80 eyes with102mm bore','Six ends per module; selected eye full plate blank includes charged bore trim, other explicit kit allocations unchanged; no AD end overlap')
    item('eight spaced fork root kits',592,hardware['kits']['mainRoot']['correctedEachKg'],'two300x220x30 cheeks with102mm bores,100x220 pin,two140/102x8 washers,two130/90x12 retainers,400x300x30 base,two400x250x20 gussets,fourM24 and welds','Eight separate roots per module; actual cheeks full plate blanks with charged bore trim and actual annular collars; other explicit allocations unchanged, no shared free pin')
    for r in g['roots']:
        item('root stem '+r['member']+'-'+r['node'],74,r['stemLengthM']*box(.200,.020)['kgPerM'],'200x200x20; full centre-to-centre stock incl end trim','Actual pin-base to ring/yoke anchor')
    backer=(.080*.080-math.pi*.026**2/4)*.012*RS
    item('root mating plates and nut backers',592,.400*.300*.030*RS+4*backer,'400x300x30 mating plate;four80x80x12 backers','M24 grip includes mating wall/pad; fork base already separately counted')
    item('root stem fabrication weld',592,.5*.012**2*1.600*RS,'two800mm 12mm perimeter seams','Each end of each stem')
    c=g['collector'];spine_length=c['lengthM'];a_length=norm(sub(c['D'],c['receiverA']))
    item('collector spine stock',74,spine_length*box(.500,.020)['kgPerM'],'500x500x20; two halves with20mm gap','Full pretrim length charged, gap waste not credited')
    item('collector A receiver arm',74,a_length*box(.500,.020)['kgPerM'],'500x500x20, actual centre distance','Whole collector wrench to A as an explicit unqualified routing')
    for node in ['D','C']:
        length=norm(sub(c[node],c['nodeAttachmentsXRT'][node]))
        item('collector node arm '+node,74,length*box(.300,.016)['kgPerM'],'300x300x16, actual ring-face to spine datum','Finite wrench transfer at each node')
    item('collector four-face splice covers',296,.750*.500*.020*RS,'750x500x20;365mm each-side overlap,20mm gap','Full stock incl bolt holes; four covers per module')
    item('collector splice M24 sets',74*32,bolt(.024,.120),'M24x120;16 bolts per series side,32 total','Two longitudinal stations100/250mm,transverse +/-150mm on each face')
    item('collector arm end plates',74*8,.500*.500*.020*RS,'500x500x20 full stock, including smaller-arm trim','Two ends of four represented connections')
    item('collector attachment M24 sets',74*8*4,bolt(.024,.120),'fourM24x120 per independent face;60mm selected grip','No opposite-end pooling')
    item('collector attachment nut backers',74*8*4,backer,'80x80x12','Install before closure; no free inaccessible nut')
    item('collector four-seam fabrication weld',74,.5*.010**2*4*(spine_length+a_length+sum(norm(sub(c[n],c['nodeAttachmentsXRT'][n])) for n in ['D','C']))*RS,'four10mm longitudinal equivalent seams','Full new box length')
    item('collector attachment perimeter weld',74,.5*.010**2*(8*2.000)*RS,'eight2000mm 10mm perimeter weld allowances','Section end plates, stock incl trim; unqualified group moments')
    item('receiver yokes',148,(1*.300*.030+2*1*.150*.020)*RS,'1000x300x30 plate,two1000x150x20 webs','Separate A/B finite overhang, old cuff body active once')
    item('receiver profiled pad full stock',148,1*.300*.100*RS,'1000x300x100 steel billet; active central400mm bearing region machined to328OD cuff','All trim charged; grip/bearing/stiffness unqualified')
    item('receiver new M24 and backers',148,8*(bolt(.024,.120)+backer),'eightM24x120 plus80x80x12 backers per yoke','Old bolts/flanges kept as contingency; new explicit pattern +/-60R, fourT stations +/-150/50')
    item('receiver welds',148,.5*.010**2*4*RS,'4m of10mm weld per yoke','Web/plate fabrication; no qualified old carbon grip')
    adapter=g['rootAdapter'];adapter_steel=(2*.160*.120*.008+2*.100*.012*adapter['webLengthM'])*RS
    item('profiled root datum adapters',1332,adapter_steel,'two160x120x8 plates,two100x12 webs at actual inclined length','Exact old/new normal and tangent datum displacement;no flat-plate gap credit')
    item('root adapter M8 and backers',1332,8*bolt(.008,.050)+8*(.030*.030-math.pi*.0084**2/4)*.004*RS,'fourM8x50 per end,30x30x4 backers;24mm grip','Two series feet,8 bolts total')
    item('root adapter welds',1332,.5*.004**2*.800*RS,'400mm of4mm weld each end','Two sides of each100mm web at each plate')
    for st in g['stanchions']:item('canted stanchion row '+str(st['row']),74,st['selectedTubeLengthM']*tube(.100,.008)['kgPerM'],'100x8 carbon, actual available cut or selected80mm minimum','No shortening to hide foot/socket space or insert overlap')
    count=74*17
    item('new stanchion beam cuffs',count,hw['eachKg']['beamFoot'],'386/354x200 cuff,354/350 liner,eightM12 and600mm8mm fabrication weld','Separate from the four-M12 plate feet')
    item('new stanchion hoop cuffs',count,hw['eachKg']['hoopFoot'],'132/110x80 cuff,110/108 liner,fourM8 and160mm4mm weld','At existing108OD splice datum; no pooled foot area')
    shoe_steel=(4*.160*.160*.012+4*.160*.030*.008+2*.120*.120*.008)*RS
    item('stanchion mating plates and socket shoes',count,shoe_steel,'four160x160x12 plates,four160x30x8 webs,two120x120x8 heads','62mm each-end occupied depth:12pad+12base+30web+8head')
    item('stanchion inserts and bonds',count,2*(annulus(.083,.069,.100)+annulus(.084,.083,.090,RA)),'two83/69x100 steel sockets;90mm bonds','Insert overlap explicitly checked against actual carbon cut')
    item('stanchion plate-foot M12 sets and backers',count,8*(bolt(.012,.070)+(.030*.030-math.pi*.013**2/4)*.006*RS),'fourM12x70 per foot,30mm grip,30x30x6 backers','Eight total per two-foot kit; each grip12base+12pad+6backer')
    item('stanchion shoe welds',count,(.5*.008**2*.640+.5*.004**2*(.480+2*math.pi*.083))*RS,'two160mm8mm base welds per end;two120mm4mm head welds and83mm circumference4mm insert weld per end','All interfaces separately charged; moment distribution remains unqualified')
    button=g['buttonSupport']
    item('button support box',74,button['boxCutM']*box(.300,.016)['kgPerM'],'300x300x16 steel, actual source-to-spine span minus140mm end stack','Full button source couple retained')
    item('button feet profile pads and backers',74,(2*.400*.400*.020+2*.400*.400*.020+16*.080*.080*.020)*RS,'two400x400x20 feet,two full400x400x20 profile pads,16 backers80x80x20','Full pad/trim stock, existing finite button reused once')
    item('button source packing',74,.400*.400*.008*RS,'400x400x8 full steel packing stock','Source grip:20plate+20pad+12shell+20backer+8packing=80mm; no end-gap closure credit')
    item('button foot M24 sets',74,16*bolt(.024,.140),'eightM24x140 per end,80mm selected grip','Separate series ends')
    item('button support seams and foot weld',74,.5*.010**2*(2.400+4*button['boxCutM'])*RS,'1200mm10mm perimeter weld each foot plus four longitudinal seams','Known moments do not create a welded-assembly rating')
    access_mass=(.300*.200*.012*RS+4*bolt(.012,.070)+.300*.200*.002*RL)
    item('collector nut access closure kits',74*4,access_mass,'300x200x12 cover,fourM12,2mm gasket;full removed wall stock retained','Four finite hatches per collector; access/section weakening unqualified')
    erection=(.100*.080-math.pi*.024**2/4)*.012*RS+math.pi*.020**2/4*.080*RS+2*annulus(.038,.022,.003)+4*bolt(.012,.070)+.120*.100*.016*RS+.5*.006**2*.240*RS+.020
    item('new collector erection kits',74*4,erection,'12mm lug,24mm hole,20x80pin,120x100x16base,fourM12,welds','Four per collector,full inherited demand each; no dilution among more locations')
    replaced={'main carbon AD','main carbon BD','main carbon DC','main carbon BC','main member end assemblies','centred double-fork node roots','outer receiver stem','inner receiver stem','root old-to-new datum adapters','stanchion beam feet','stanchion hoop feet','stanchion end hardware','button normal/offset support stock','button support feet and bolts'}
    old_rows=[]
    for row in old['mass']['newItems']:
        changed=row['item'] in replaced or row['item'].startswith('normal hoop-to-DC stanchion row ')
        reused=row['massT'] if not changed else 0.
        if row['item']=='receiving bridge cuffs':reused=row['count']*(hw['partsKg']['receivingCuff']['splitBand']+hw['partsKg']['receivingCuff']['liner'])/1000
        old_rows.append(dict(item=row['item'],priorT=row['massT'],activeReuseT=reused,inactiveContingencyT=row['massT']-reused,selectedRetirementT=0.,duty='Replaced by explicit new stock; old mass remains inactive contingency, not simultaneous installable geometry.' if changed else 'Active reuse remains counted once; receiver cuff bodies/liners only, with old extra fittings retained as contingency.' if row['item']=='receiving bridge cuffs' else 'Unchanged active I020 duty, already counted once in prior hull.'))
    close(sum(x['priorT'] for x in old_rows),old['mass']['newModuleAddedT'])
    added=sum(row['massT'] for row in rows);prior=old['mass'];hull=prior['hullT']+added;gas=prior['residualGasOnceT'];subtotal=hull+gas
    heights=[dict(altitudeM=a['altitudeM'],liftT=a['liftT'],knownMarginT=a['liftT']-subtotal,priorKnownMarginT=a['knownMarginT'],deltaT=-added) for a in prior['at']]
    for x,y in zip(heights,prior['at']):close(x['knownMarginT'],y['knownMarginT']-added)
    return dict(newItems=rows,newAddedT=added,changedHardwareReconciliation=hardware,acceptedI020HullT=prior['hullT'],oldI020Rows=old_rows,olderInactiveContingencies=prior['oldModuleAttribution'],selectedRetirementT=0.,retirementGate='No credit: assembly, access and complete replacement load-transfer duties remain unqualified. Retained old contingency is accounting stock, not co-installed geometry.',hullT=hull,residualGasOnceT=gas,knownSubtotalT=subtotal,at=heights,reusedFiniteButtonT=prior['reusedFiniteButtonT'],selectedVolumeM3=prior['selectedVolumeM3'],selectedDisplacementChangeM3=0.,completeAllUpMassT=None,physicalFloat=None,newErectionDemand=dict(requiredEachN=old['localScreens']['erection']['nominalRequiredPerPointN'],kitCount=296,unchangedLocalLugAndPinScreens=old['localScreens']['erection'],collectorAttachmentCapacity=None,noDemandDilution=True),qualification='Selected-stock budget with inactive contingency and trim, not an installable hull or all-up U+C mass; the charged AD blank cannot contain its selected eye solids.')


def calculate():
    baseline=json.loads((HERE/'baseline.json').read_text())
    for path,digest in baseline['referenceFiles'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    old=baseline['i020'];g=make_geometry(old)
    for row in old['filmLoadPath']['rows']:
        expected=1 if row['row']==18 else 2
        assert len(row['incidentBars'])==expected
        close(norm(sub(sumv(embed(b['forceXRN']) for b in row['incidentBars']),embed(row['capForcePerClipXRN']))))
    cases=[load_case(g,old,f) for f in [0,1]];fit=fit_witnesses(g,old);mass=ledger(g,old)
    return dict(unit='R3-I024',baselineSha256=hashlib.sha256((HERE/'baseline.json').read_bytes()).hexdigest(),hypothesis='Tangentially spaced pins, an axially staggered polar pair, one-piece AD cartridge and fully priced torsion collector might connect the known polar loads without coplanar pin/insert conflicts or a free moment path.',geometry=g,loadCases=cases,clearance=fit,mass=mass,unchangedPressureAndFilm=dict(sourceResultSha256=baseline['referenceFiles']['research/design-iterations/R3-I020/result.json'],pressurePa=121590.,caps=2,sectorsPerCap=37,filmBays=18,filmColumns=666,polarAxialOneCapN=old['filmLoadPath']['sourcePolarAxialForceOneCapN'],incomingOldBoundaryOneCap=old['filmLoadPath']['incomingOldBoundaryAxialAndLocalRadialSumOneCapN'],wholeEnd611MNReapplied=False,incidentBarCounts=[len(r['incidentBars']) for r in old['filmLoadPath']['rows']],buttonPressureSeparate=True),fixedComparison=dict(geometry=old['geometry'],clearance=old['clearance'],localScreens=old['localScreens'],mainMemberScreens=[c['mainMemberScreens'] for c in old['loadCases']],mass=old['mass']),computation=dict(cpuSeconds=30,wallSeconds=60,addressSpaceBytes=1073741824,matrixOrder=0,parameterSweeps=0,ancestorCalls=0,selectedGeometries=1,radialLoadAssignments=2),pressureCapacityPa=None,physicalFloat=None,globalStiffness=None,qualification='Selected construction has explicit finite fit/access witnesses and conditional demand screens only. Any material/access conflict is FAIL. Full receiver/connection capacity, global pressure/loaded shape, physical float and complete U+C are UNKNOWN. Inherited barrel/mid-cap, film, button-strip and receiving-frame failures remain.',weakestAssumption='A finite collector and its A yoke/cuff could transmit the required full vector moment into the already unqualified receiving frame; arithmetic closure alone supplies no stiffness or capacity.',nextConstruction='One receiver-integrated split polar cassette with a proven insertion order and isolated ring-wall clearance could replace the observed interfering branches. Its actual frame attachment must be specified before any retirement credit; this alternative is not calculated here.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=calculate();text=json.dumps(result,indent=2,allow_nan=False)+'\n';path=HERE/'result.json'
    if args.write:path.write_text(text)
    elif args.check:assert json.loads(path.read_text())==result,'Saved output differs';print('I024 fixed geometry, vector identities, input pins and stock ledger PASS; construction/physical qualification not established.')
    else:print(text)


if __name__=='__main__':main()
