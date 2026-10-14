#!/usr/bin/env python3
"""One fixed polar module: scalar force, fit and stock-accounting evidence.

Read the corrected I016 result, never execute an ancestor model. The selected
pin-truss force path does not supply the unresolved connection moments or
repair its demonstrated solid intersections. No pressure rating is inferred.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R = 40.0
O = (40.0, 0.0)
Q = 121590.0
NC = 37
NF = 666
ALPHA = 2 * math.pi / NC
BETA = 2 * math.pi / NF
PHI0 = math.radians(72)
PHI1 = math.acos(3 / R)
NB = 18
EC, ES = 135e9, 200e9
RC, RS, RA = 1600.0, 7850.0, 1200.0
FY, FC = 355e6, 1450e6
PIN_OFFSET = .300
END_SETBACK = .250


def add(a, b): return [a[0] + b[0], a[1] + b[1]]
def sub(a, b): return [a[0] - b[0], a[1] - b[1]]
def mul(k, a): return [k * a[0], k * a[1]]
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def cross(a, b): return a[0] * b[1] - a[1] * b[0]
def norm(a): return math.hypot(*a)
def direction(a, b): return mul(1 / norm(sub(b, a)), sub(b, a))
def normal(phi): return [math.sin(phi), math.cos(phi)]
def surface(phi, offset=0): return add(O, mul(R - offset, normal(phi)))


def close(a, b, atol=1e-6, rel=1e-9):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=atol), (a, b)


def compare(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a: compare(a[k], b[k])
    elif isinstance(a, list):
        assert len(a) == len(b)
        for x, y in zip(a, b): compare(x, y)
    elif isinstance(a, float): close(a, b, atol=1e-5, rel=1e-8)
    else: assert a == b, (a, b)


def tube(od, wall, rho=RC):
    bore = od - 2 * wall
    area = math.pi * (od**2 - bore**2) / 4
    inertia = math.pi * (od**4 - bore**4) / 64
    return dict(odM=od, wallM=wall, areaM2=area, inertiaM4=inertia,
                sectionModulusM3=2*inertia/od, kgPerM=area*rho)


def annulus(od, bore, length, rho):
    return math.pi*(od**2-bore**2)/4*length*rho


def bolt(d, length, af, head, nut, washer_od, washer_id, washer_t):
    hex_area=math.sqrt(3)/2*af**2
    return RS*(math.pi*d*d/4*length + hex_area*head
               + (hex_area-math.pi*d*d/4)*nut) + 2*annulus(washer_od,washer_id,washer_t,RS)


def force_pair(u, v, applied):
    determinant=cross(u,v)
    assert abs(determinant)>1e-8
    a=-cross(applied,v)/determinant
    b=-cross(u,applied)/determinant
    residual=add(applied,add(mul(a,u),mul(b,v)))
    close(norm(residual),0,atol=1e-5)
    return a,b,determinant


def section_screen(force, sec, length, modulus=EC, ceiling=FC, moment=0):
    direct=abs(force)/sec['areaM2']
    bending=abs(moment)/sec['sectionModulusM3']
    euler=math.pi**2*modulus*sec['inertiaM4']/length**2
    return dict(signedTensionN=force, directStressPa=direct,
                bendingStressPa=bending, additiveStressPa=direct+bending,
                pinLengthM=length,pinEulerN=euler,nominalCeilingPa=ceiling,
                nominalStressPass=direct+bending<=ceiling,
                pinEulerPass=force>=0 or -force<euler,
                qualification='Unqualified material/laminate, local shell, restraint and connection; pin Euler is not global pressure stability.')


def series_foot_screens(force, moment_o, source, receiver, source_name, receiver_name):
    """Carry one force/couple system through two separately stocked plate feet.

    The existing plate kit has eight M12 sets and 0.640 m of 8 mm weld in
    total. Allocate four sets and two 160 mm weld runs to EACH series foot.
    Attachment centres are the existing load-transfer datums. Bolt/weld-group
    centroids and moment distribution are unqualified, so mean force-only
    shear is not a combined connection PASS.
    """
    source_couple = moment_o - cross(sub(source, O), force)
    force_lever = cross(sub(source, receiver), force)
    receiver_couple = source_couple + force_lever
    source_identity = cross(sub(source, O), force) + source_couple - moment_o
    receiver_identity = cross(sub(receiver, O), force) + receiver_couple - moment_o
    close(source_identity, 0)
    close(receiver_identity, 0)
    feet = []
    for name, point, sense, couple in [
            (source_name, source, 1, source_couple),
            (receiver_name, receiver, -1, receiver_couple)]:
        reaction = mul(sense, force)
        reaction_couple = sense * couple
        feet.append(dict(
            name=name, datumXR=point,
            forceAppliedToSupportXRN=reaction,
            coupleAppliedToSupportAboutDatumNm=reaction_couple,
            oppositeForceToAttachmentXRN=mul(-1, reaction),
            oppositeCoupleToAttachmentNm=-reaction_couple,
            resultantN=norm(reaction), knownCoupleMagnitudeNm=abs(couple),
            plateDimensionsM=[.160, .160, .012],
            m12Count=4, threadedRootDiameterM=.0098,
            weldRunLengthsM=[.160, .160], weldLengthM=.320,
            weldLegM=.008, nominalThroatFactor=.707,
            forceOnlyFourM12MeanShearPa=norm(reaction)/(4*math.pi*.0098**2/4),
            forceOnlyWeldMeanShearPa=norm(reaction)/(.707*.008*.320),
            actualBoltAndWeldGroupCentroidsXR=None,
            additionalBoltStressFromKnownMomentPa=None,
            additionalWeldStressFromKnownMomentPa=None,
            combinedConnectionPass=None,
            qualification='Known force and couple retained at the declared attachment datum. Actual bolt pattern, weld-group distribution, local plate eccentricity, preload and material capacity are UNKNOWN; force-only mean shear is not a combined connection screen.'))
    reaction_force = add(*(f['forceAppliedToSupportXRN'] for f in feet))
    reaction_moment = sum(cross(sub(f['datumXR'], O), f['forceAppliedToSupportXRN'])
                          + f['coupleAppliedToSupportAboutDatumNm'] for f in feet)
    close(norm(reaction_force), 0)
    close(reaction_moment, 0)
    assert sum(f['m12Count'] for f in feet) == 8
    close(sum(f['weldLengthM'] for f in feet), .640)
    return dict(
        throughForceFromSourceToReceiverXRN=force,
        sourceMomentAboutCapCentreNm=moment_o,
        sourceDatumXR=source, receiverDatumXR=receiver,
        sourceCoupleNm=source_couple, forceLeverToReceiverNm=force_lever,
        receiverCoupleNm=receiver_couple,
        sourceMomentIdentityResidualNm=source_identity,
        receiverMomentIdentityResidualNm=receiver_identity,
        supportReactionForceResidualN=norm(reaction_force),
        supportReactionMomentResidualNm=reaction_moment,
        allocation=dict(totalPlateCount=2, totalM12Count=8,
                        totalWeldLengthM=.640, weldLegM=.008,
                        assumption='Equal allocation of existing stock: four M12 and two 160 mm weld runs per foot. Opposite feet transmit in series; neither hardware set is pooled with the other.'),
        feet=feet,
        maximumForceOnlyBoltMeanShearPa=max(f['forceOnlyFourM12MeanShearPa'] for f in feet),
        maximumForceOnlyWeldMeanShearPa=max(f['forceOnlyWeldMeanShearPa'] for f in feet),
        maximumKnownFootCoupleNm=max(f['knownCoupleMagnitudeNm'] for f in feet),
        rejectedPooledHardwareControl=dict(
            eightBoltsAcrossBothFeetMeanShearPa=norm(force)/(8*math.pi*.0098**2/4),
            wholeKitWeldMeanShearPa=norm(force)/(.707*.008*.640),
            perFootToPooledDemandRatio=2.,
            status='REJECTED: hardware at the opposite series foot does not provide parallel resisting area.'),
        combinedConnectionPass=None)


def geometry(prior):
    last=prior['geometry']['oneCapMainStations'][-1]
    shift=-BETA/2
    radii={name:last[key]*math.cos(ALPHA/2)/math.cos(shift)
           for name,key in [('A','outerRadiusM'),('B','innerRadiusM')]}
    nodes={'A':[last['xM']-.250,radii['A']],
           'B':[last['xM']-.450,radii['B']],
           'D':surface(PHI0,.500),
           'C':[prior['geometry']['polarHub']['xM'],3.]}
    members=[]
    for first,last_name in [('A','D'),('B','D'),('D','C'),('B','C')]:
        a,b=nodes[first],nodes[last_name]
        e=direction(a,b);length=norm(sub(b,a))
        pins=[add(a,mul(PIN_OFFSET,e)),sub(b,mul(PIN_OFFSET,e))]
        pin_length=length-2*PIN_OFFSET
        cut=pin_length-2*END_SETBACK
        assert cut>0
        members.append(dict(name=first+last_name,firstNode=first,lastNode=last_name,
                            directionXR=e,nodeLengthM=length,pinCentresXR=pins,
                            pinLengthM=pin_length,carbonCutM=cut,
                            insertLengthEachM=.300,insertGapM=cut-.600,
                            insertFit=cut>=.600))
    return dict(nodesXR=nodes,members=members,
                repeatCount=2*NC,sectorAngleRad=ALPHA,
                supportAzimuthRule='theta_j=(18*j+8.5)*2*pi/666; 18 inherited bar columns j*18..j*18+17 are centred on each support meridian.',
                cuffChordMidpointAngularShiftRad=shift,
                cuffDevelopedOffsetsM={k:radii[k]*math.sin(shift) for k in radii},
                lastFrame=last,rootNormalOffsetM=.500,
                polarRingDatum='Inherited x79.38734135035827,r3; new200x200x20 box replaces its active hub duty only as an unqualified attempt.',
                finiteButtonSurfaceXR=surface(PHI1),finiteButtonPhiRad=PHI1,
                otherCap='Reflect X about zero; reverse axial forces, preserve radial/local demands.')


def hardware():
    b24=bolt(.024,.120,.036,.015,.019,.044,.026,.004)
    b12=bolt(.012,.070,.019,.008,.010,.024,.013,.0025)
    b8=bolt(.008,.050,.013,.0055,.0065,.016,.0084,.0016)
    end=dict(insert=annulus(.309,.285,.300,RS),
             bond=annulus(.310,.309,.290,RA),
             endPlate=math.pi*.400**2/4*.020*RS,
             centredEye=(.300*.220-math.pi*.100**2/4)*.080*RS,
             eyeWeld=.5*.012**2*2*.220*RS,
             insertWeld=.5*.010**2*math.pi*.309*RS)
    root=dict(twoForkCheeks=2*(.300*.220-math.pi*.100**2/4)*.030*RS,
              pin=math.pi*.100**2/4*.220*RS,
              washers=2*annulus(.140,.102,.008,RS),retainers=.600,
              twoGussets=2*.400*.250*.020*RS,
              basePlate=.400*.300*.030*RS,
              fourM24=4*b24,welds=.5*.012**2*1.2*RS)
    cuff=dict(splitBand=annulus(.328,.296,.400,RS),
              liner=annulus(.296,.292,.400,1100),
              fourFlanges=4*(.150*.100-2*math.pi*.026**2/4)*.020*RS,
              eightM24=8*b24,flangeWelds=.5*.010**2*1.2*RS,
              twoStemEndPlates=2*.200*.200*.020*RS)
    film_end=dict(sleeve=annulus(.055,.044,.100,RS),
                  lug=(.080*.040-.040*.010)*.008*RS,
                  weld=.5*.004**2*.160*RS)
    clip=dict(basePlate=.120*.100*.012*RS,
              fourForkCheeks=4*(.080*.035-math.pi*.008**2/4)*.008*RS,
              commonPin=math.pi*.008**2/4*.080*RS,
              twoM12=2*b12,retainers=.010,
              twoBondPads=2*.030*.050*.0005*RA,
              welds=.5*.004**2*.320*RS)
    clip_post=dict(twoPlates=2*.080*.080*.008*RS,
                   fourM8=4*b8,welds=.5*.004**2*.320*RS)
    hoop_foot=dict(splitCuff=annulus(.132,.110,.080,RS),
                   liner=annulus(.110,.108,.080,1100),
                   twoFlanges=2*.080*.040*.008*RS,fourM8=4*b8,
                   welds=.5*.004**2*.160*RS)
    beam_foot=dict(splitCuff=annulus(.386,.354,.200,RS),
                   liner=annulus(.354,.350,.200,1100),
                   fourFlanges=4*.120*.080*.016*RS,
                   eightM12=8*b12,welds=.5*.008**2*.600*RS)
    stanchion_end=dict(twoPlates=2*.160*.160*.012*RS,
                       eightM12=8*b12,welds=.5*.008**2*.640*RS)
    groups=dict(mainEnd=end,mainRoot=root,receivingCuff=cuff,
                filmBarEnd=film_end,filmClip=clip,clipPostEnd=clip_post,
                hoopFoot=hoop_foot,beamFoot=beam_foot,stanchionEnd=stanchion_end)
    return dict(partsKg=groups,eachKg={k:sum(v.values()) for k,v in groups.items()},
                m24SetKg=b24,m12SetKg=b12,m8SetKg=b8)


def projected_pressure(lo, hi, angular_width):
    fx=-Q*angular_width*R**2/2*(math.sin(hi)**2-math.sin(lo)**2)
    integral=(hi-lo)/2+(math.sin(2*hi)-math.sin(2*lo))/4
    fr=-Q*2*math.sin(angular_width/2)*R**2*integral
    return [fx,fr]


def box_ray_outer(phi, centre, half_width):
    s=surface(phi);n=normal(phi)
    lower=[(s[k]-centre[k]-half_width)/n[k] for k in range(2)]
    upper=[(s[k]-centre[k]+half_width)/n[k] for k in range(2)]
    entry=max(lower);exit_at=min(upper)
    assert 0<entry<exit_at
    return entry,sub(s,mul(entry,n))


def film_grid(g,prior,hw):
    dphi=(PHI1-PHI0)/NB
    spans=[]
    for j in range(NB):
        a=PHI0+j*dphi;b=a+dphi
        pa,pb=surface(a,.060),surface(b,.060)
        length=norm(sub(pb,pa));e=direction(pa,pb);n=[-e[1],e[0]]
        load=projected_pressure(a,b,BETA)
        upper_normal=-cross(sub(pa,O),load)/length
        fb=mul(upper_normal,n);fa=sub(load,fb)
        close(cross(sub(pa,O),fa)+cross(sub(pb,O),fb),0)
        close(dot(fb,e),0)
        mid=mul(.5,add(pa,pb));half_load=projected_pressure(a,(a+b)/2,BETA)
        mid_moment=.5*length*cross(e,fa)-cross(sub(mid,O),half_load)
        spans.append(dict(index=j,lowerPhiRad=a,upperPhiRad=b,
                          pinCentresXR=[pa,pb],pinLengthM=length,
                          surfacePitchM=R*dphi,carbonCutM=length-.120,
                          fixedBondLengthM=.080,guideLengthM=.080,
                          endInsertGapM=length-.120-.160,
                          pressureForceXRN=load,lowerPinForceXRN=fa,
                          upperGuideForceXRN=fb,midspanBendingMomentNm=mid_moment))
    inherited=prior['filmSupport']['clipReactionAssembly']['terminalRows'][-1]
    incoming=inherited['knownCapForceXRN']
    old_point=[g['lastFrame']['xM'],g['lastFrame']['surfaceRadiusM']-.0215]
    radial_factor=math.sin(ALPHA/2)/math.sin(BETA/2)
    rows=[];beam=sub(g['nodesXR']['C'],g['nodesXR']['D']);beam_e=mul(1/norm(beam),beam)
    for j in range(NB+1):
        phi=PHI0+j*dphi;n=normal(phi);p=surface(phi,.060)
        contributions=[];extra_moment=0.
        if j>0:contributions.append(dict(source='new poleward guide',span=j-1,forceXRN=spans[j-1]['upperGuideForceXRN']))
        if j<NB:contributions.append(dict(source='new lower pin',span=j,forceXRN=spans[j]['lowerPinForceXRN']))
        if j==0:
            contributions.append(dict(source='frozen I016 incoming terminal',span=None,forceXRN=incoming))
            extra_moment=cross(sub(old_point,p),incoming)
        force=[sum(v['forceXRN'][k] for v in contributions) for k in range(2)]
        sector_force=[18*force[0],radial_factor*force[1]]
        moment_o=radial_factor*(cross(sub(p,O),force)+extra_moment)
        if j==0:
            collector=g['nodesXR']['D'];depth,foot=box_ray_outer(phi,collector,.225)
            support='root box ring, including cover envelope'
        elif j==NB:
            collector=g['nodesXR']['C'];depth,foot=box_ray_outer(phi,collector,.125)
            support='finite polar box ring, including cover envelope'
        else:
            collector=surface(phi,.300);depth=.300-.066;foot=surface(phi,depth)
            support='100mm hoop,108mm sleeve,132mm clip-foot cuff'
        available=depth-(.060+.0275)-.016
        post_length=max(.080,available)
        full_post_moment=cross(sub(p,foot),force)+extra_moment
        stanchion=None
        if 0<j<NB:
            rhs=sub(surface(phi),g['nodesXR']['D']);det=cross(beam,n)
            lam=cross(rhs,n)/det;axis_depth=cross(beam,rhs)/det
            axis=add(g['nodesXR']['D'],mul(lam,beam))
            close(norm(sub(axis,surface(phi,axis_depth))),0)
            sine=abs(cross(n,beam_e))
            clear=axis_depth-.300-.066-.193/sine-.024
            stanchion=dict(beamFraction=lam,beamAxisPointXR=axis,axisNormalDepthM=axis_depth,
                            availableTubeLengthM=clear,selectedTubeLengthM=max(.080,clear),
                            minimumLengthPass=clear>=.080,
                            betweenActualPins=PIN_OFFSET/norm(beam)<=lam<=1-PIN_OFFSET/norm(beam))
        rows.append(dict(row=j,phiRad=phi,degrees=math.degrees(phi),barPinXR=p,
                         incidentBars=contributions,capForcePerClipXRN=force,
                         normalPerClipN=dot(force,n),tangentPerClipN=dot(force,[n[1],-n[0]]),
                         resultantPerClipN=norm(force),rootStepMomentPerClipNm=extra_moment,
                         collectorCentreXR=collector,clipPostFootXR=foot,
                         clipPostAvailableM=available,clipPostSelectedM=post_length,
                         clipPostMinimumPass=available>=.080,
                         clipPostMomentNm=full_post_moment,
                         sectorForceXRN=sector_force,sectorMomentAboutCapCentreNm=moment_o,
                         support=support,stanchion=stanchion))
    button=projected_pressure(PHI1,math.pi/2,ALPHA)
    new_axial=NF*sum(s['pressureForceXRN'][0] for s in spans)+NC*button[0]
    expected=-Q*math.pi*(R*math.cos(PHI0))**2
    close(new_axial,expected)
    new_radial=radial_factor*sum(s['pressureForceXRN'][1] for s in spans)+button[1]
    close(new_radial,projected_pressure(PHI0,math.pi/2,ALPHA)[1])
    new_moment=0.
    for s in spans:
        new_moment+=radial_factor*sum(cross(sub(p,O),f) for p,f in zip(s['pinCentresXR'],[s['lowerPinForceXRN'],s['upperGuideForceXRN']]))
    close(new_moment,0)
    return dict(spans=spans,rows=rows,polarButtonSectorForceXRN=button,
                sourcePolarAxialForceOneCapN=-new_axial,
                sourcePolarRadialPerSectorN=-new_radial,
                wholeEndAxialForceN=prior['pressure']['oneCapAxialResultantN'],
                incomingOldBoundaryAxialAndLocalRadialSumOneCapN=mul(NF,incoming),
                incomingBoundaryFrame='First component is global axial. Second is the sum of local radial components around the cap, not a global radial vector; the full-ring global transverse resultant cancels by symmetry.',
                newPressureMomentAboutCapCentreNm=new_moment,
                sectorRadialFactor=radial_factor,
                clipCount=2*(NB+1)*NF,barCount=2*NB*NF,
                fineHoopCount=2*(NB-1),fineHoopSpliceCount=2*(NB-1)*NC,
                incomingRootAdapterCount=2*NF,
                scope='New72degree-to-button pressure plus finite button equals the polar projection once. The inherited incoming half-span reaction is a separately labelled boundary transfer. No611MN whole-end load is added. Both incident bars are assembled; the polar film terminal has one bar and a separately priced button flange.')


def box_section(size,wall):
    area=size**2-(size-2*wall)**2
    inertia=(size**4-(size-2*wall)**4)/12
    return dict(sizeM=size,wallM=wall,areaM2=area,inertiaM4=inertia,
                sectionModulusM3=2*inertia/size,kgPerM=area*RS)


def routed_row(row, radial_fraction):
    full=row['sectorForceXRN']
    hoop_reaction=[0.,-(1-radial_fraction)*full[1]]
    applied=add(full,hoop_reaction)
    moment_o=row['sectorMomentAboutCapCentreNm']+cross(sub(row['collectorCentreXR'],O),hoop_reaction)
    return dict(forceXRN=applied,momentAboutCapCentreNm=moment_o,
                collectorCoupleNm=moment_o-cross(sub(row['collectorCentreXR'],O),applied),
                circumferentialCompressionN=abs(hoop_reaction[1])/(2*math.sin(ALPHA/2)))


def main_end_screen(force,axis):
    axial=dot(force,axis);shear=cross(axis,force)
    insert=tube(.309,.012,RS)
    moment=abs(shear)*END_SETBACK
    return dict(resultantN=norm(force),signedAxialN=axial,transverseN=shear,
                pinDoubleShearPa=norm(force)/(2*math.pi*.100**2/4),
                eyeBearingPa=norm(force)/(.100*.080),
                twoForkBearingPa=norm(force)/(2*.100*.030),
                forkNetSectionPa=norm(force)/(2*.030*(.220-.100)),
                insertAxialStressPa=abs(axial)/insert['areaM2'],
                meanBondShearPa=abs(axial)/(math.pi*.309*.290),
                endPlateTransverseMomentNm=moment,
                endPlateStripBendingPa=6*moment/(.400*.020**2),
                fourM24RootMeanShearPa=norm(force)/(4*math.pi*.020**2/4),
                forkWeldMeanShearPa=norm(force)/(.707*.012*1.2),
                capacityN=None,
                status='Centred double-shear geometry; nominal demands only. Bond peel, laminate, plate distribution, bolt preload, access and failed solid arrangement are not qualified.')


def load_case(g,film,radial_fraction):
    nodes=g['nodesXR'];D,C,A,B=(nodes[k] for k in ('D','C','A','B'))
    dc=next(m for m in g['members'] if m['name']=='DC')
    e=dc['directionXR'];n=[-e[1],e[0]];pd,pc=dc['pinCentresXR'];length=dc['pinLengthM']
    routed=[routed_row(row,radial_fraction) for row in film['rows']]
    button_full=film['polarButtonSectorForceXRN']
    button_hoop=[0.,-(1-radial_fraction)*button_full[1]]
    button_force=add(button_full,button_hoop)
    button_moment_o=cross(sub(C,O),button_hoop)
    root_force=routed[0]['forceXRN']
    hub_force=add(routed[-1]['forceXRN'],button_force)
    root_couple=routed[0]['collectorCoupleNm']
    hub_couple=(routed[-1]['momentAboutCapCentreNm']+button_moment_o
                -cross(sub(C,O),hub_force))
    beam_loads=[]
    for row,load in zip(film['rows'][1:-1],routed[1:-1]):
        point=row['stanchion']['beamAxisPointXR'];force=load['forceXRN']
        couple=load['momentAboutCapCentreNm']-cross(sub(point,O),force)
        station=dot(sub(point,pd),e)
        beam_loads.append(dict(row=row['row'],pointXR=point,stationM=station,
                               forceXRN=force,forceAlongBeamN=dot(force,e),
                               forceNormalBeamN=dot(force,n),coupleNm=couple,
                               momentAboutLowerPinNm=cross(sub(point,pd),force)+couple,
                               withinCarbonAndCuffEnvelope=END_SETBACK+.100<=station<=length-END_SETBACK-.100))
    total=[sum(v['forceXRN'][k] for v in beam_loads) for k in range(2)]
    moment=sum(v['momentAboutLowerPinNm'] for v in beam_loads)
    fixed_c=mul(moment/length,n);fixed_d=sub(total,fixed_c)
    # The axial reference puts the distributed axial force at D. Solving the
    # unknown DC axial force then determines both actual ends; it is not an
    # assumed division of thrust between the two receiving layers.
    dc_tension,bc_tension,det_c=force_pair(mul(-1,e),direction(C,B),add(hub_force,fixed_c))
    ad_tension,bd_tension,det_d=force_pair(direction(D,A),direction(D,B),
                                         add(root_force,add(fixed_d,mul(dc_tension,e))))
    force_d=add(fixed_d,mul(dc_tension,e));force_c=sub(fixed_c,mul(dc_tension,e))
    to_a=mul(ad_tension,direction(A,D))
    to_b=add(mul(bd_tension,direction(B,D)),mul(bc_tension,direction(B,C)))
    source_total=add(root_force,add(hub_force,total))
    close(norm(sub(add(to_a,to_b),source_total)),0,atol=1e-5)
    source_moment=(sum(v['momentAboutCapCentreNm'] for v in routed)+button_moment_o)
    receiving_moment=cross(sub(A,O),to_a)+cross(sub(B,O),to_b)
    close(source_moment-receiving_moment,
          root_couple+cross(sub(pd,D),force_d)+hub_couple+cross(sub(pc,C),force_c))
    dc_samples=[]
    for station in sorted({0.,length,*[p['stationM'] for p in beam_loads]}):
        for side in ('before','after'):
            left=[p for p in beam_loads if p['stationM']<station or (side=='after' and p['stationM']==station)]
            axial=dc_tension+dot(total,e)-sum(p['forceAlongBeamN'] for p in left)
            shear=dot(fixed_d,n)-sum(p['forceNormalBeamN'] for p in left)
            bending=dot(fixed_d,n)*station+sum(p['momentAboutLowerPinNm']-station*p['forceNormalBeamN'] for p in left)
            dc_samples.append(dict(stationM=station,side=side,signedTensionN=axial,
                                   shearN=shear,bendingMomentNm=bending))
    carbon=tube(.350,.020)
    max_axial=max(abs(v['signedTensionN']) for v in dc_samples)
    max_compression=max(0.,-min(v['signedTensionN'] for v in dc_samples))
    peak_bending=max(dc_samples,key=lambda v:abs(v['bendingMomentNm']))
    dc_screen=section_screen(max_axial,carbon,length,moment=peak_bending['bendingMomentNm'])
    dc_screen.update(maximumAbsoluteAxialN=max_axial,maximumCompressionN=max_compression,
                     pinEulerPass=max_compression<dc_screen['pinEulerN'],
                     axialSignConvention='Positive stress-envelope magnitude is the maximum absolute axial force. Actual signed section forces are tabulated; Euler uses only actual maximum compression.',
                     maximumBendingSample=peak_bending)
    forces={'AD':ad_tension,'BD':bd_tension,'BC':bc_tension}
    screens={m['name']:section_screen(forces[m['name']],carbon,m['pinLengthM'])
             for m in g['members'] if m['name']!='DC'}
    screens['DC']=dc_screen
    ends=[]
    for member in g['members']:
        axis=member['directionXR'];name=member['name']
        endpoint_forces=[force_d,force_c] if name=='DC' else [mul(forces[name],axis),mul(-forces[name],axis)]
        for j,force in enumerate(endpoint_forces):
            local_axis=axis if j==0 else mul(-1,axis)
            ends.append(dict(member=name,node=member['firstNode'] if j==0 else member['lastNode'],
                             forceOnNodeXRN=force,screen=main_end_screen(force,local_axis)))
    ring_rows=[]
    stanchion_screens=[]
    for row,load in zip(film['rows'],routed):
        j=row['row'];radius=row['collectorCentreXR'][1]
        sec=box_section(.400,.025) if j==0 else box_section(.200,.020) if j==NB else tube(.100,.008)
        hoop=load['circumferentialCompressionN']
        force=load['forceXRN'];couple=load['collectorCoupleNm']
        if j==NB:
            hoop+=abs(button_hoop[1])/(2*math.sin(ALPHA/2))
            force=hub_force;couple=hub_couple
        chord=2*radius*math.sin(ALPHA/2)
        bending_bound=norm(force)*chord/4+abs(couple)
        nominal=hoop/sec['areaM2']+bending_bound/sec['sectionModulusM3']
        ring_rows.append(dict(row=j,radiusM=radius,chordM=chord,
                               hoopCompressionN=hoop,section=sec,
                               localPinSpanBendingEnvelopeNm=bending_bound,
                               axialPlusBendingEnvelopePa=nominal,
                               nominalCeilingPa=FY if j in (0,NB) else FC,
                               nominalPass=nominal<=(FY if j in (0,NB) else FC),
                               spliceMeanBondShearPa=None if j in (0,NB) else hoop/(math.pi*.100*.150),
                               boxSplice16M24ShearPa=hoop/(16*math.pi*.020**2/4) if j in (0,NB) else None,
                               qualification='Two load-route limits only; actual circumferential redistribution, curved-member stability and support stiffness UNKNOWN. Bending bound includes all one-sector force at the worst pin-span lever plus the known collector couple.'))
        if row['stanchion']:
            st=row['stanchion'];nphi=normal(row['phiRad']);force=load['forceXRN']
            axial=dot(force,nphi)
            moment_at_foot=load['momentAboutCapCentreNm']-cross(sub(st['beamAxisPointXR'],O),force)
            screen=section_screen(axial,tube(.100,.008),st['selectedTubeLengthM'],moment=moment_at_foot)
            feet=series_foot_screens(force,load['momentAboutCapCentreNm'],
                                     row['collectorCentreXR'],st['beamAxisPointXR'],
                                     'hoop-side plate foot','DC-side plate foot')
            close(feet['sourceCoupleNm'],load['collectorCoupleNm'])
            close(feet['receiverCoupleNm'],moment_at_foot)
            stanchion_screens.append(dict(row=j,screen=screen,
                                           footMomentNm=moment_at_foot,
                                           sectionScreenDatum='Existing DC beam-axis datum; not a combined foot-connection qualification.',
                                           seriesPlateFeet=feet,
                                           separateCuffKits=dict(
                                               beamFoot='Existing eight M12 split-cuff set and 0.600 m of 8 mm fabrication weld remain a distinct interface; not part of the eight-total plate kit.',
                                               hoopFoot='Existing four M8 split-cuff set and 0.160 m of 4 mm fabrication weld remain distinct; not pooled with plate bolts/welds.',
                                               actualGripAndMomentTransfer=None)))
    stanchion_foot_summary=dict(
        interfaceCount=2*len(stanchion_screens),
        maximumForceOnlyBoltMeanShearPa=max(s['seriesPlateFeet']['maximumForceOnlyBoltMeanShearPa'] for s in stanchion_screens),
        maximumForceOnlyWeldMeanShearPa=max(s['seriesPlateFeet']['maximumForceOnlyWeldMeanShearPa'] for s in stanchion_screens),
        maximumKnownFootCoupleNm=max(s['seriesPlateFeet']['maximumKnownFootCoupleNm'] for s in stanchion_screens),
        combinedConnectionPass=None,
        qualification='Per-interface demand maxima for the two-foot plate kits only. Separate cuff hardware and unknown moment distribution do not create parallel capacity.')
    cuffs=[]
    for name,force in [('A',to_a),('B',to_b)]:
        offset=nodes[name][0]-g['lastFrame']['xM']
        moment=offset*force[1]
        cuffs.append(dict(node=name,forceToInheritedFrameXRN=force,
                           oppositeFrameOnModuleXRN=mul(-1,force),
                           stemMomentNm=moment,
                           phaseShiftCircumferentialForceN=force[1]*math.sin(-BETA/2),
                           nominalContactPressurePa=abs(force[1])/(.292*.400),
                           axialInterfaceMeanShearPa=abs(force[0])/(math.pi*.292*.400),
                           eightM24MeanShearPa=norm(force)/(8*math.pi*.020**2/4),
                           fourBoltTensionFromMomentPa=abs(moment)/(4*.250*math.pi*.020**2/4),
                           qualification='Actual clamp preload/friction, old bridge/node, receiving-ring bending and frame stiffness UNKNOWN; nominal contact is not a qualified attachment.'))
    return dict(radialFractionToTruss=radial_fraction,
                interpretation='All radial load goes to post/truss flexure; no radial hoop credit.' if radial_fraction else 'Radial collectors carry all radial load as hoop compression; axial load still transfers. This is a limiting assignment, not demonstrated sharing.',
                determinants={'C':det_c,'D':det_d},
                memberSignedTensionN=dict(forces,DC_reference=dc_tension),
                mainMemberScreens=screens,allEightEndScreens=ends,
                dcBeamPointLoads=beam_loads,dcBeamSections=dc_samples,
                dcActualEndForcesToNodesXRN=[force_d,force_c],
                rootEndBlockMomentNm=root_couple+cross(sub(pd,D),force_d),
                polarEndBlockMomentNm=hub_couple+cross(sub(pc,C),force_c),
                totalAppliedForcePerSectorXRN=source_total,
                receivingForcesPerSectorXRN={'A':to_a,'B':to_b},
                sourceMomentAboutCapCentreNm=source_moment,
                unresolvedModuleMomentNm=source_moment-receiving_moment,
                receivingCuffScreens=cuffs,ringScreens=ring_rows,stanchionScreens=stanchion_screens,
                stanchionPlateFootSummary=stanchion_foot_summary,
                forceBalanceResidualN=norm(sub(add(to_a,to_b),source_total)),
                pressureCapacityPa=None,
                status='Force equilibrium only. Known root/polar/receiver moments require bending transfer that the ideal pin triangles do not establish. Solid pin/insert conflicts invalidate assembly; no rigid receiving-frame or global stability credit.')


def clearance(g,film):
    clearances=[]
    for name,key in [('A','outerChordM'),('B','innerChordM')]:
        half=g['lastFrame'][key]/2
        developed=abs(g['cuffDevelopedOffsetsM'][name])
        gap=half-.300-(developed+.200)
        clearances.append(dict(node=name,nearestNodePadDevelopedGapM=gap,
                                cuffBoreM=.296,bridgeOdM=.292,linerEachM=.002,
                                noPadCuffOverlap=gap>0,
                                scope='400mm cuff lies wholly away from600mm developed node pads. This addresses the named nominal pad/cuff intersection only.'))
    pin_collisions=[]
    for node in g['nodesXR']:
        attached=[]
        for m in g['members']:
            for end,n in enumerate((m['firstNode'],m['lastNode'])):
                if node==n:attached.append((m['name'],m['pinCentresXR'][end]))
        for (ma,pa),(mb,pb) in itertools.combinations(attached,2):
            separation=norm(sub(pa,pb));witness=mul(.5,add(pa,pb))
            pin_collisions.append(dict(node=node,members=[ma,mb],centreSeparationM=separation,
                                       requiredFor100mmPinsM=.100,clearanceM=separation-.100,
                                       intersection=separation<.100,
                                       witnessXR=witness,witnessTangentialM=0.,
                                       explanation='All selected pins are parallel to the sector tangential axis with the same220mm axial extent. A midpoint within both50mm disks is a solid intersection, not a centreline-only warning.'))
    root_old=[g['lastFrame']['xM'],g['lastFrame']['surfaceRadiusM']-.0215]
    step=sub(root_old,film['rows'][0]['barPinXR'])
    normal_step=abs(dot(step,normal(PHI0)))
    boxes=[]
    for name,half in [('D',.225),('C',.125)]:
        centre=g['nodesXR'][name]
        maximum=max(norm(sub(add(centre,[sx*half,sr*half]),O)) for sx,sr in itertools.product((-1,1),repeat=2))
        boxes.append(dict(node=name,maximumCoverCornerRadiusM=maximum,
                          nominalPressureSurfaceClearanceM=R-maximum,
                          scope='Box and cover envelope only; attached roots and surrounding inherited parts are not globally cleared.'))
    return dict(receivingCuffs=clearances,centredPinPairs=pin_collisions,
                insertFit=[dict(member=m['name'],carbonCutM=m['carbonCutM'],twoInsertsM=.600,
                                gapM=m['insertGapM'],passFit=m['insertFit']) for m in g['members']],
                normalFilmBarToFineHoopM=.300-.060-.0215-.050,
                normalFilmSleeveToLargestFootCuffM=.300-.060-.0275-.066,
                filmClipPostMinimumAvailableM=min(row['clipPostAvailableM'] for row in film['rows']),
                filmClipPostMinimumRequiredM=.080,
                fineStanchionMinimumAvailableM=min(row['stanchion']['availableTubeLengthM'] for row in film['rows'] if row['stanchion']),
                fineStanchionShortCount=2*NC*sum(row['stanchion']['availableTubeLengthM']<.080 for row in film['rows'] if row['stanchion']),
                fineStanchionOutsideActualPins=[row['row'] for row in film['rows'] if row['stanchion'] and not row['stanchion']['betweenActualPins']],
                rootDatumAdapter=dict(oldToNewPinVectorXR=step,
                                      requiredNormalStepM=normal_step,
                                      selectedFlatPlateNormalThicknessM=.016,
                                      unbridgedNormalStepM=normal_step-.016,
                                      status='FAIL:160x120x16 flat plate in the new normal/tangent frame does not bridge this normal step. No unpriced spacer, bend or wedge is supplied; the force/couple ledger is conditional on that unresolved transfer.'),
                ringBoxEnvelope=boxes,
                inheritedFailures='I016 barrel/mid-cap37/43mm grid clashes,888short posts, original nonreplaced pad/cuff collisions and other failed joints remain. New nominal clearances do not repair those.',
                status='FAIL: the selected compact coplanar centred end blocks have explicit pin/insert conflicts. No cutout, moved ring, shortened insert or unpriced shared fitting is substituted.')


def local_screens(g,film,prior):
    clips=[];bar=tube(.043,.001);post=tube(.060,.003)
    for row in film['rows']:
        f=row['resultantPerClipN'];m=abs(row['rootStepMomentPerClipNm'])+.010*f
        incident=max(norm(x['forceXRN']) for x in row['incidentBars'])
        clips.append(dict(row=row['row'],incidentBarCount=len(row['incidentBars']),
                          resultantN=f,common8mmPinDoubleShearPa=f/(2*math.pi*.008**2/4),
                          worstEyeOrGuideBearingPa=incident/(.008*.008),
                          twoM12MeanRootShearPa=f/(2*math.pi*.0098**2/4),
                          twoBondPadMeanShearPa=f/(2*.030*.050),
                          basePlateStripBendingPa=6*m/(.100*.012**2),
                          rootAdapterStepMomentNm=row['rootStepMomentPerClipNm'],
                          normalPost=section_screen(row['normalPerClipN'],post,row['clipPostSelectedM'],
                                                    moment=row['clipPostMomentNm']),
                          totalWithFilmTensionAndUnknownInterfacesN=None))
    bar_screens=[]
    for span in film['spans']:
        fixed=span['lowerPinForceXRN'];guide=span['upperGuideForceXRN']
        axis=direction(*span['pinCentresXR'])
        moment=span['midspanBendingMomentNm']
        bar_screens.append(dict(span=span['index'],fixedEndResultantN=norm(fixed),
                                guideEndResultantN=norm(guide),
                                fixedEndAxialN=dot(fixed,axis),guideAxialN=dot(guide,axis),
                                fixedBondMeanShearPa=norm(fixed)/(math.pi*.043*.080),
                                guideBearingPa=norm(guide)/(.008*.008),
                                midspanBendingPa=abs(moment)/bar['sectionModulusM3'],
                                midspanNominalPass=abs(moment)/bar['sectionModulusM3']<=FC,
                                actualMaximumBendingPa=None,
                                qualification='Exact declared midspan sample, not a claim of the peak along the bar; guide friction/axial stroke, laminate and all other sections unqualified.'))
    panel_pitch=film['spans'][0]['surfacePitchM']
    max_width=2*R*math.cos(PHI0)*math.sin(BETA/2)
    a=max(panel_pitch,max_width)/2;h=a/4
    tension=Q*(a*a+h*h)/(2*h)
    film_stress=tension/.001
    button_bending=6*(Q*6**2/8)/.012**2
    button_force=film['polarButtonSectorForceXRN']
    button_point=surface(PHI1,.006);button_axis=direction(g['nodesXR']['C'],button_point)
    button_length=max(.080,norm(sub(button_point,g['nodesXR']['C']))-.100)
    button_feet=series_foot_screens(button_force,0.,button_point,g['nodesXR']['C'],
                                   'button-side plate foot','C-ring-side plate foot')
    button_sections=[]
    for name,point,moment in [('button-side datum',button_point,button_feet['sourceCoupleNm']),
                              ('C-ring datum',g['nodesXR']['C'],button_feet['receiverCoupleNm'])]:
        button_sections.append(dict(name=name,datumXR=point,signedTransferredMomentNm=moment,
                                    screen=section_screen(dot(button_force,button_axis),tube(.100,.008,RS),
                                                          button_length,modulus=ES,ceiling=FY,moment=moment)))
    governing=max(button_sections,key=lambda s:s['screen']['additiveStressPa'])
    button_support=dict(governing['screen'],controllingDatum=governing['name'],
                        scope='Conditional complete force/couple transfer along the existing support; no distributed support load. Endpoint moment envelope is linear. Actual foot restraint and capacity remain UNKNOWN.')
    old_button_screen=section_screen(dot(button_force,button_axis),tube(.100,.008,RS),button_length,
                                     modulus=ES,ceiling=FY,moment=button_feet['forceLeverToReceiverNm'])
    old_source_residual=cross(sub(g['nodesXR']['C'],O),button_force)+button_feet['forceLeverToReceiverNm']
    close(old_source_residual,-button_feet['sourceCoupleNm'])
    erection=prior['erectionAttachment']['requiredNominalN']
    return dict(clips=clips,bars=bar_screens,
                film=dict(surfaceMeridionalPitchM=panel_pitch,maximumAzimuthalChordM=max_width,
                          thicknessM=.001,densityKgM3=1400,oneWayTroughTensionNPerM=tension,
                          tensileDemandPa=film_stress,unqualifiedProxyPa=50e6,
                          nominalPass=film_stress<=50e6,
                          qualification='Generic polymer assumption, not qualified material or drape. Pads close the declared normal gap but creep/adhesion/seams are UNKNOWN.'),
                button=dict(surfaceRadiusM=3.,plateThicknessM=.012,
                            membraneCompressionPa=Q*R/(2*.012),
                            diameterStripBendingPa=button_bending,nominalSteelPa=FY,
                            diameterStripPass=button_bending<=FY,
                            oneOf37SupportForceXRN=button_force,
                            support=button_support,
                            supportEndSections=button_sections,
                            seriesPlateFeet=button_feet,
                            rejectedOmittedCoupleControl=dict(
                                oldForceLeverMomentNm=button_feet['forceLeverToReceiverNm'],
                                omittedSourceCoupleNm=button_feet['sourceCoupleNm'],
                                oldAdditiveStressPa=old_button_screen['additiveStressPa'],
                                oldImpliedSourceMomentAboutCapCentreNm=old_source_residual,
                                requiredSourceMomentAboutCapCentreNm=0.,
                                sourceMomentIdentityPass=False,
                                status='REJECTED: the former short-offset screen omitted the known source couple and its apparent nominal PASS was invalid.'),
                            radialRouteScope='The support carries the full button force/couple to C in both existing radial limits. The declared radial hoop reaction acts downstream at C. The global cases already carry this source moment; these local screens add no new global force or couple.',
                            edge666M12MeanShearPa=NC*norm(button_force)/(NF*math.pi*.0098**2/4),
                            qualification='Retained shallow spherical button; the unsupported6m one-way strip is a failed nominal screen. Two-way plate/shell buckling and actual edge restraint UNKNOWN.'),
                erection=dict(nominalRequiredPerPointN=erection,
                              fineHoopKitCount=2*(NB-1)*148,boxRingKitCount=2*2*148,
                              lugNetSectionPa=erection/(.012*(.080-.024)),
                              lugBearingPa=erection/(.020*.012),
                              pinSingleShearPa=erection/(math.pi*.020**2/4),
                              lugRootBendingPa=6*erection*.050/(.080*.012**2),
                              fourM12RootMeanShearPa=erection/(4*math.pi*.0098**2/4),
                              qualification='Full inherited demand, no wind-load dilution. Grip, bolt preload, carbon packing, ring transfer and other wind cases UNKNOWN. Original nonreplaced erection-flange FAIL remains.'),
                status='Midspan bar and nominal connection screens do not qualify film, guide friction, pressure wall or physical assembly.')


def replacement_ledger(g,film,hw,prior):
    bill=[]
    def item(name,count,each_kg,dimensions,duty):
        assert count>=0 and each_kg>=0
        bill.append(dict(item=name,count=count,eachKg=each_kg,massT=count*each_kg/1000,
                         dimensions=dimensions,duty=duty))
    sec=tube(.350,.020)
    for m in g['members']:
        item('main carbon '+m['name'],2*NC,m['carbonCutM']*sec['kgPerM'],
             '350x20; actual pin length minus2x250mm carbon setback','Both ends; selected short AD stock is retained despite insert overlap.')
    item('main member end assemblies',2*NC*4*2,hw['eachKg']['mainEnd'],
         '309/285x300 insert;290bond+10relief;400x20plate;centred80mmeye','Every end of all four members, both caps')
    item('centred double-fork node roots',2*NC*4*2,hw['eachKg']['mainRoot'],
         'two30mmcheeks;100x220pin;washers;gussets;base;4M24;welds','Distinct selected roots; no free shared pin replaces colliding stock')
    item('receiving bridge cuffs',2*NC*2,hw['eachKg']['receivingCuff'],
         '328/296x400 steel,2mmliner on292bridge,eightM24','No300mm developed node-pad overlap')
    stem=box_section(.200,.020)
    item('outer receiver stem',2*NC,.250*stem['kgPerM'],'200x200x20,length250','Axial root stand-off, not a zero-moment connection')
    item('inner receiver stem',2*NC,.450*stem['kgPerM'],'200x200x20,length450','Axial root stand-off, not a zero-moment connection')
    for name,size,wall in [('D',.400,.025),('C',.200,.020)]:
        radius=g['nodesXR'][name][1];section=box_section(size,wall)
        item('box ring '+name,2,(2*math.pi*radius-NC*.004)*section['kgPerM'],
             f'{size*1000:g}square x{wall*1000:g};37curvedsegments,4mmgaps','New root/polar compression collector')
        cover=(.304*size-4*math.pi*.026**2/4)*wall*RS
        item('four face splice covers '+name,2*NC*4,cover,
             '304developed;four26mmholes per face;150mm overlap each side','Load-bearing covers over every4mm ring gap')
        item('ring splice bolts '+name,2*NC*16,hw['m24SetKg'],'M24x120 full set','Four per face, every splice')
        item('ring box fabrication weld '+name,2,.5*.010**2*4*(2*math.pi*radius-NC*.004)*RS,
             'four10mmfillet equivalent seams,full ring length','Fabrication allowance, no weld qualification')
        item('root bolt access/nut backing plates '+name,2*NC*(3 if name=='D' else 2)*4,
             (.080*.080-math.pi*.026**2/4)*.012*RS,
             '80x80x12 backers;M24 pattern120axial x200tangential','Install nuts before closing box wall; no unpriced access cutout')
    fine=tube(.100,.008)
    for row in film['rows'][1:-1]:
        r=row['collectorCentreXR'][1]
        item('fine hoop row '+str(row['row']),2,(2*math.pi*r-NC*.004)*fine['kgPerM'],
             '100x8carbon,normaloffset300;37arcs with4mmgaps','Only17interior hoops per cap')
    fine_splice=annulus(.108,.102,.304,RS)+annulus(.102,.100,.300,RA)
    item('fine hoop splices',2*(NB-1)*NC,fine_splice,
         '108/102x304 steel,two150mmannular bonds','No assumed weld or splice capacity')
    film_bar=tube(.043,.001)
    for span in film['spans']:
        item('film bar span '+str(span['index']),2*NF,span['carbonCutM']*film_bar['kgPerM'],
             '43x1carbon;actual chord minus2x60 setback','18 spans,666meridians,both caps once')
    item('film bar steel end fittings',film['barCount']*2,hw['eachKg']['filmBarEnd'],
         '55/44x100 sleeve,80x40x8 eye/guide lug,4mmweld','One fixed and one poleward guided end per bar')
    item('fixed bar-end bonds',film['barCount'],annulus(.044,.043,.080,RA),
         '80mm bond,0.5mm radial','One fixed end per new bar')
    item('poleward guide liners',film['barCount'],annulus(.044,.043,.080,1100),
         '80mm sleeve liner,40x10 axial slot and8mmpin','No assumed friction load; guide stroke/assembly UNKNOWN')
    item('shared film clips including terminal stock',film['clipCount'],hw['eachKg']['filmClip'],
         '120x100x12base,four8mmcheeks,8mmpin,twoM12,two30x50bondpads','One common clip per row; both incident loads assembled')
    item('root old-to-new datum adapters',2*NF,.160*.120*.016*RS+4*hw['m8SetKg'],
         '160x120x16 plate,fourM8','Selected flat adapter fails to bridge the normal datum step; stock and conditional transfer couple retained')
    post=tube(.060,.003)
    for row in film['rows']:
        item('film clip normal post row '+str(row['row']),2*NF,
             row['clipPostSelectedM']*post['kgPerM'],
             '60x3carbon,selected length at least80mm','Actual normal box/cuff intersection and two8mmplates')
    item('film post end hardware',film['clipCount'],hw['eachKg']['clipPostEnd'],
         'two80x80x8plates,fourM8,welds','Every film clip,including both terminals')
    item('fine hoop clip-foot cuffs',2*(NB-1)*NF,hw['eachKg']['hoopFoot'],
         '132/110x80cuff,2mmliner to108,flanges,fourM8','Bare100mmhoop locations receive separately priced carbon packing')
    # Every fine clip cuff is priced for108mm OD; identify the part of its
    # 80mm developed footprint not already over a304mm splice sleeve.
    packing=0.
    for row in film['rows'][1:-1]:
        r=row['collectorCentreXR'][1];segment=2*math.pi*r/NC
        for k in range(18):
            centre=(k-8.5)*BETA*r
            covered=0.
            for shift in (-segment,0.,segment):
                covered+=max(0.,min(centre+.040,shift+.152)-max(centre-.040,shift-.152))
            uncovered=max(0.,.080-covered)
            packing+=2*NC*annulus(.108,.100,uncovered,RC)
    item('profiled fine-clip foot packing',1,packing,
         '108/100 carbon profile outside exact304mm sleeve intervals','No empty annulus under the max-OD cuffs')
    stanchion=tube(.100,.008)
    for row in film['rows'][1:-1]:
        item('normal hoop-to-DC stanchion row '+str(row['row']),2*NC,
             row['stanchion']['selectedTubeLengthM']*stanchion['kgPerM'],
             '100x8carbon,min80mm;actual normal intersection withDC','Unfit short locations remain charged at chosen stock length')
    item('stanchion beam feet',2*(NB-1)*NC,hw['eachKg']['beamFoot'],
         '386/354x200splitcuff,2mmliner,eightM12,flanges,welds','Actual350OD DC beam; no free point support')
    item('stanchion hoop feet',2*(NB-1)*NC,hw['eachKg']['hoopFoot'],
         '132/110x80cuff and fullflanges/bolts','At108OD splice sites,not an assumed bare-hoop grip')
    item('stanchion end hardware',2*(NB-1)*NC,hw['eachKg']['stanchionEnd'],
         'two160x160x12plates,eightM12,welds','Both ends of every normal stanchion')
    # Conservative full-length pad stock is selected. Its active normal
    # stock is38.5mm over43OD and32.5mm over55OD. Trim1mm for the
    # inward film thickness; the discarded material stays in the bill.
    pad_length=2*NF*sum(s['pinLengthM'] for s in film['spans'])
    item('profiled pressure-film pads,full stock',1,pad_length*.030*.0385*1100,
         '30mmwide;38.5mmstock;active37.5mm bare/31.5mm over sleeves','Trim allowance retained; reaches inner face of1mm film whose outer face isR40;creep/adhesion UNKNOWN')
    annular_area=4*math.pi*R**2*(math.sin(PHI1)-math.sin(PHI0))
    item('new annular polymer film',1,annular_area*.001*1400,
         '1mm generic polymer,1400kg/m3','No additional film beyond the finite3m button; material is unqualified')
    edge_length=2*(2*math.pi*(R*math.cos(PHI0))+2*math.pi*3)
    item('root and button edge straps',1,edge_length*.120*.012*RS,
         '120x12 continuous steel straps','Finite supported film edges; full circumference at both ends')
    item('edge strap backing plates',1,edge_length*.120*.008*RS,
         '120x8 backing strip','Paired pressure-edge clamp,not an unsupported membrane edge')
    item('edge seal gaskets',1,edge_length*.100*.002*1100,
         '100x2 continuous gasket','Seal compression/leakage not qualified')
    item('edge bolts',2*2*NF,hw['m12SetKg'],'M12 perbarcolumn at root andbutton','Bothcaps; terminal overlap stock charged')
    item('edge and button weld allowances',1,.5*.008**2*2*edge_length*RS,
         'two8mmfillets per edge','Explicit seam stock; actual polymer sealing remains UNKNOWN')
    # Button is reused from the old12mm dome and is not bought again. New
    # finite supports and feet transmit its pressure to the new polar ring.
    button_support_length=norm(sub(surface(PHI1,.006),g['nodesXR']['C']))-.100
    item('button normal/offset support stock',2*NC,max(.080,button_support_length)*tube(.100,.008,RS)['kgPerM'],
         '100x8steel,finite surface-to-ring offset','Actual oblique offset and end moments retained;no pole point')
    item('button support feet and bolts',2*NC,
         2*.160*.160*.012*RS+8*hw['m12SetKg']+.5*.008**2*.640*RS,
         'two160x160x12feet,eightM12,8mmwelds','One complete kit per support')
    # Four erection lugs per sector per support ring; fine hoops use a
    # fitted108OD base, and box rings use full welded/bolted base plates.
    lug=(.100*.080-math.pi*.024**2/4)*.012*RS
    pin=math.pi*.020**2/4*.080*RS+2*annulus(.038,.022,.003,RS)+.020
    common=lug+pin+4*hw['m12SetKg']+.5*.006**2*.240*RS
    fine_attach=annulus(.140,.112,.080,RS)+annulus(.112,.108,.080,1100)+2*.100*.050*.010*RS+common
    box_attach=.120*.100*.016*RS+common
    item('fine-hoop erection kits',2*(NB-1)*148,fine_attach,
         '140/112x80cuff,liner,flanges,12mmlug,20mmpin,fourM12','Full inherited wind demand per location;no load dilution')
    item('box-ring erection kits',2*2*148,box_attach,
         '120x100x16base,12mmlug,20mmpin,fourM12','148 locations oneachroot/polarring,eachcap')
    attachment_packing=0.
    for row in film['rows'][1:-1]:
        r=row['collectorCentreXR'][1];segment=2*math.pi*r/NC
        for k in range(4):
            centre=(k+.5)*segment/4
            covered=sum(max(0.,min(centre+.040,s+.152)-max(centre-.040,s-.152)) for s in (0.,segment))
            attachment_packing+=2*NC*annulus(.108,.100,max(0.,.080-covered),RC)
    item('profiled erection cuff packing',1,attachment_packing,
         '108/100 carbon outside actual sleeve footprint','Avoids applying max-OD cuff to an empty annulus')
    old_rows=[]
    button_area=2*math.pi*R**2*(1-math.sin(PHI1))
    button_mass=2*button_area*.012*RS/1000
    for name,value in prior['polarClosure']['massT'].items():
        reused=button_mass if name=='twoDomePlatesT' else 0.
        old_rows.append(dict(item='polarClosure.'+name,priorT=value,reusedActiveT=reused,
                             inactiveContingencyT=value-reused,selectedRetirementT=0.,
                             disposition='Finite button reused once; annular plate stock retained as unqualified-replacement contingency.' if reused else 'Old active hardware replaced locally in the attempted layout; its mass saving is not selected because replacement fit/transfer is unqualified.'))
    old_carbon=0.
    for name,path in prior['meridians']['paths'].items():
        terminal=path['oneEndSegments'][-1]
        # The frozen takeoff supplies exact cut lengths, not an ancestor run.
        cut=terminal['carbonCutM']
        old_carbon+=2*NC*cut*prior['meridians']['section']['kgPerM']/1000
    old_rows.extend([
        dict(item='terminal meridian carbon',priorT=old_carbon,reusedActiveT=0.,inactiveContingencyT=old_carbon,selectedRetirementT=0.,disposition='Both outer/inner last spans physically superseded; no unqualified saving selected.'),
        dict(item='terminal meridian end fittings',priorT=2*NC*2*2*prior['newHardware']['meridianEndKg']/1000,reusedActiveT=0.,inactiveContingencyT=2*NC*2*2*prior['newHardware']['meridianEndKg']/1000,selectedRetirementT=0.,disposition='Both ends, two layers, both caps; retained contingency.'),
        dict(item='old hub roots',priorT=prior['meridians']['massT']['hubRootsT'],reusedActiveT=0.,inactiveContingencyT=prior['meridians']['massT']['hubRootsT'],selectedRetirementT=0.,disposition='All148 hub roots superseded; retained contingency.'),
        dict(item='old terminal film clips and splices',priorT=2*NF*(prior['newHardware']['filmClipKg']+prior['newHardware']['barSpliceKg'])/1000,reusedActiveT=0.,inactiveContingencyT=2*NF*(prior['newHardware']['filmClipKg']+prior['newHardware']['barSpliceKg'])/1000,selectedRetirementT=0.,disposition='Root shared collector hardware is newly priced;oldterminal stock remains contingency.'),
        dict(item='last-frame meridian saddles,remaining cap/barrel and attachments',priorT=None,reusedActiveT=None,inactiveContingencyT=None,selectedRetirementT=0.,disposition='Unchanged outside this local replacement,including still-needed incoming-span roots. Full old hull remains carried; do not add these attributed rows a second time.')])
    added=sum(v['massT'] for v in bill)
    hull=prior['mass']['hullT']+added
    gas=prior['mass']['residualGasOnceT']
    subtotal=hull+gas
    at=[dict(altitudeM=a['altitudeM'],liftT=a['liftT'],knownMarginT=a['liftT']-subtotal,
             priorKnownMarginT=a['knownMarginT'],deltaT=-added) for a in prior['mass']['at']]
    for a,b in zip(at,prior['mass']['at']):close(a['knownMarginT'],b['knownMarginT']-added)
    return dict(newItems=bill,newModuleAddedT=added,oldModuleAttribution=old_rows,
                priorHullT=prior['mass']['hullT'],selectedRetirementT=0.,
                hullT=hull,residualGasOnceT=gas,knownSubtotalT=subtotal,
                reusedFiniteButtonT=button_mass,selectedVolumeM3=prior['mass']['selectedVolumeProxyM3'],
                selectedDisplacementChangeM3=0.,at=at,
                priorAllowanceBeforeFramePolarMeridianT=prior['mass']['maximumNewFrameT'],
                allUpMassT=None,allUpMarginT=None,
                accounting='Corrected I016 hull minus0 selected retirement plus every new module item. Attribution rows are already inside the prior hull and are not added again. Reused button appears once. Inactive contingencies are stock-accounting reserves, not a claim that old and new intersecting hardware are simultaneously installed. No unsupported mass/displacement saving or extra residual gas is selected.',
                qualification='Failed-construction stock budget,not an installable aircraft or all-up mass. Loaded surface/displacement and U+C remain UNKNOWN.')


def calculate():
    frozen=json.loads((HERE/'baseline.json').read_text())
    for path,digest in frozen['referenceFiles'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    prior=frozen['i016'];g=geometry(prior);hw=hardware()
    film=film_grid(g,prior,hw)
    cases=[load_case(g,film,f) for f in (0,1)]
    fit=clearance(g,film);screens=local_screens(g,film,prior)
    ledger=replacement_ledger(g,film,hw,prior)
    return dict(unit='R3-I020',baselineSha256=hashlib.sha256((HERE/'baseline.json').read_bytes()).hexdigest(),
                hypothesis='A repeated two-triangle polar module and normal-offset film supports might bridge the oldroot gap without node-pad cuffs or fine-grid interference. The chosen centred coplanar ends must fit and transfer both force and residual moment.',
                geometry=g,hardware=hw,filmLoadPath=film,loadCases=cases,
                clearance=fit,localScreens=screens,mass=ledger,
                computation=dict(matrixOrder=0,parameterSweeps=0,ancestorModelCalls=0,
                                 loadSharingLimits=2,selectedGeometries=1),
                pressureCapacityPa=None,physicalFloat=None,
                qualification='FAIL: selected centred pins/inserts, short stanchions and root datum adapter are not realizable; force equilibrium does not close known ring/end-block/receiving moments. Local nominal strength/film/button limits and all inherited failures remain. Assembly,full pressure stability,U+C and physical float UNKNOWN.',
                weakestAssumption='A physically separable root/polar end-block arrangement that can carry the known moments into the two existing receiving rings; ideal pin force balance supplies neither.',
                nextConstruction='Test one spaced three-dimensional root node with separate tangential pin planes and a shorter dedicated AD end cartridge, while explicitly pricing its torsion collector. Do not change the remaining hull or claim a saving before that local fit and moment path exist.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group()
    action.add_argument('--write',action='store_true');action.add_argument('--check',action='store_true')
    args=parser.parse_args();result=calculate()
    if args.write:(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    elif args.check:
        compare(result,json.loads((HERE/'result.json').read_text()))
        print('I020 reproduction PASS: frozen inputs, exact polar projection, signed incident bars, two scalar force routes, solid-fit witnesses and complete retained-stock/gas-once ledger. Construction FAIL; physical/global capacity UNKNOWN.')
    else:print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':main()
