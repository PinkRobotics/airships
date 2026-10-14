#!/usr/bin/env python3
"""One finite cap-to-cap construction attempt. Scalar statics, not a pressure rating.

Frozen I014 data are read, never executed. All added geometry is priced even
when its nominal strength or local fit fails. No inherited cap/flight saving
is selected on the strength of these incomplete load paths.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R = 40.0
P = 101325.0
SF = 1.2
Q = P * SF
NC = 37
NF = 666
ALPHA = 2 * math.pi / NC
E = 135e9
RC = 1600.0
RS = 7850.0
RA = 1200.0
FY = 355e6
CARBON_PROXY = 1450e6
PHI_LAST = math.radians(72)
PHI_HUB = math.acos(3 / R)
WEB_SETBACK = .55


def close(a, b, rel=1e-9, atol=1e-7):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=atol), (a, b)


def compare(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a:
            compare(a[k], b[k])
    elif isinstance(a, list):
        assert len(a) == len(b)
        for x, y in zip(a, b):
            compare(x, y)
    elif isinstance(a, float):
        close(a, b, rel=1e-8, atol=1e-6)
    else:
        assert a == b, (a, b)


def annulus(od, bore, length, rho):
    return math.pi * (od**2 - bore**2) / 4 * length * rho


def tube(od, wall, rho):
    a = math.pi * (od**2 - (od - 2 * wall)**2) / 4
    i = math.pi * (od**4 - (od - 2 * wall)**4) / 64
    return dict(odM=od, wallM=wall, areaM2=a, inertiaM4=i,
                sectionModulusM3=2 * i / od, kgPerM=rho * a)


def fastener(d, length, af, head, nut, wod, wid, wt):
    h = math.sqrt(3) / 2 * af**2
    return RS * (math.pi * d*d / 4 * length + h * head
                 + (h - math.pi * d*d / 4) * nut) + 2 * annulus(wod, wid, wt, RS)


def screen(force, sec, length, modulus=E, ceiling=CARBON_PROXY):
    euler = math.pi**2 * modulus * sec['inertiaM4'] / length**2
    direct = abs(force) / sec['areaM2']
    return dict(forceN=force, directStressPa=direct, pinLengthM=length,
                pinEulerN=euler, axialCeilingPa=ceiling,
                directProxyPass=direct <= ceiling,
                pinEulerPass=force <= 0 or force < euler,
                qualification='UNKNOWN: actual laminate, local shell, connection and restraint not established')


def geometry(prior):
    ro0 = prior['geometry']['outerRingRadiusM']
    ri0 = prior['geometry']['innerRingRadiusM']
    ratio = ri0 / ro0
    rows = []
    for degree in range(0, 73, 4):
        phi = math.radians(degree)
        x, surface = 40 + R * math.sin(phi), R * math.cos(phi)
        # A declared bounding box for the cap frame's two web planes: +/-360
        # mm in x, +170 mm radially. Fine wall/support fittings are separate.
        ro = ro0 if not degree else math.sqrt((R - .010)**2 - (R*math.sin(phi) + .360)**2) - .170
        ri = ro * ratio
        n = 111 if not degree else NC
        chord = lambda radius: 2 * radius * math.sin(math.pi/n)
        rows.append(dict(degrees=degree, phiRad=phi, xM=x,
                         surfaceRadiusM=surface, outerRadiusM=ro, innerRadiusM=ri,
                         columns=n, outerChordM=chord(ro), innerChordM=chord(ri),
                         axialSpacingFromPreviousM=x-rows[-1]['xM'] if rows else 2.,
                         surfaceArcSpacingM=R*math.radians(4) if rows else 2.,
                         capFrameEnvelopeRadiusM=math.hypot(x-40+.360, ro+.170) if degree else None))
    hub_x = 40 + R * math.sin(PHI_HUB) - .500
    hub = dict(phiRad=PHI_HUB, degrees=math.degrees(PHI_HUB), xM=hub_x,
               surfaceXAt3mM=hub_x+.500, surfaceRadiusM=3.,
               outerRadiusM=3.25, innerRadiusM=2.75, columns=NC,
               boxMeanRadiusM=3., boxRadialWidthM=.600, boxAxialWidthM=.500,
               boxWallM=.012, domeThicknessM=.012, poleXM=80.)
    assert min(row['innerChordM'] for row in rows) > 1.604
    assert all(row['capFrameEnvelopeRadiusM'] <= R-.009 for row in rows[1:])
    return rows, hub


def new_hardware(hw):
    end = dict(hw['webEndPartsKg'])
    end['oneOutboardLug'] += .150 * .120 * .016 * RS
    meridian = dict(
        steelInsert=annulus(.225, .213, .200, RS),
        endPlate=math.pi*.270**2/4*.008*RS,
        twoClevisLugs=2*(.302*.180-math.pi*.080**2/4)*.020*RS,
        pin=math.pi*.080**2/4*.150*RS,
        twoWashers=2*annulus(.110,.082,.008,RS), retainers=.040,
        insertBond=annulus(.226,.225,.194,RA),
        insertWeld=.5*.004**2*math.pi*.225*RS,
        fourLugWelds=.5*.008**2*.720*RS)
    bolt16 = fastener(.016,.090,.024,.010,.013,.030,.017,.003)
    saddle = dict(
        splitCuff=annulus(.330,.314,.400,RS),
        liner=annulus(.314,.310,.400,1100),
        fourFlanges=4*(.100*.070-2*math.pi*.017**2/4)*.012*RS,
        eightM16Sets=8*bolt16,
        oneTwoPinPlate=(.500*.650-2*math.pi*.096**2/4)*.040*RS,
        twoBushes=2*annulus(.096,.080,.040,RS),
        plateAndFlangeWelds=.5*.008**2*2.0*RS)
    hub_root = dict(onePinPlate=(.500*.400-math.pi*.096**2/4)*.040*RS,
                    bush=annulus(.096,.080,.040,RS),
                    rootWeld=.5*.008**2*1.0*RS)
    fine_splice = dict(steelCuff=annulus(.178,.168,.404,RS),
                       twoBonds=annulus(.168,.166,.400,RA))
    bar_splice = dict(carbonSleeve=annulus(.047,.044,.204,RC),
                     twoBonds=annulus(.044,.043,.200,RA))
    m6 = fastener(.006,.030,.010,.004,.005,.012,.0064,.0016)
    clip = dict(twoAngles=2*(.020+.020-.002)*.030*.002*RS,
                twoM6Sets=2*m6, twoBonds=2*.020*.030*.0005*RA)
    # The large sleeve deliberately prices a maximum-node cuff at every foot.
    # A failed fit is reported rather than shortening a post or deleting hardware.
    post_end = dict(lowerSplitCuff=annulus(.330,.314,.080,RS),
                    lining=annulus(.314,.310,.080,1100),
                    twoPlates=2*.080*.080*.005*RS,
                    fourM8Sets=4*fastener(.008,.045,.013,.0055,.0065,.016,.0084,.0016),
                    twoBondWraps=2*.200*.080*.001*RA,
                    twoWelds=.5*.004**2*.320*RS)
    return dict(capWebEndPartsKg=end, capWebEndKg=sum(end.values()),
                meridianEndPartsKg=meridian, meridianEndKg=sum(meridian.values()),
                meridianChamferRemovedKg=math.pi*.006/12*(.234**2+.234*.226-2*.226**2)*RC,
                saddlePartsKg=saddle, saddleKg=sum(saddle.values()),
                hubRootPartsKg=hub_root, hubRootKg=sum(hub_root.values()),
                fineSplicePartsKg=fine_splice, fineSpliceKg=sum(fine_splice.values()),
                barSplicePartsKg=bar_splice, barSpliceKg=sum(bar_splice.values()),
                filmClipPartsKg=clip, filmClipKg=sum(clip.values()),
                standOffHardwarePartsKg=post_end, standOffHardwareKg=sum(post_end.values()),
                m16SetKg=bolt16)


def cap_frames(rows, hw, new):
    web = tube(.300,.0025,RC)
    masses = dict(baseTubesT=0., bridgesT=0., integralNodesT=0.,
                  webCarbonT=0., bothWebEndsT=0.)
    details = []
    for row in rows[1:]:
        ro,ri = row['outerRadiusM'],row['innerRadiusM']
        dx,dy = ri*math.cos(ALPHA)-ro,ri*math.sin(ALPHA)
        length = math.hypot(dx,dy)
        cut = length-2*WEB_SETBACK
        assert cut > .600
        er_o = abs(dx/length)
        er_i = abs((dx*math.cos(ALPHA)+dy*math.sin(ALPHA))/length)
        clear_o=math.hypot(.200,WEB_SETBACK*er_o)-.305
        clear_i=math.hypot(.200,WEB_SETBACK*er_i)-.305
        masses['baseTubesT'] += 2*NC*(row['outerChordM']+row['innerChordM']-.008)*hw['ring']['kgPerM']/1000
        masses['bridgesT'] += 4*NC*hw['spliceKg']/1000
        masses['integralNodesT'] += 4*NC*hw['nodeKg']/1000
        masses['webCarbonT'] += 4*NC*(cut*web['kgPerM']-2*hw['carbonChamferRemovedKgEach'])/1000
        masses['bothWebEndsT'] += 8*NC*new['capWebEndKg']/1000
        details.append(dict(degrees=row['degrees'], pinLengthM=length, carbonCutM=cut,
                            outerRadialDirection=er_o,innerRadialDirection=er_i,
                            outerTangentialDirection=abs(dy/length),
                            innerTangentialDirection=abs((-dx*math.sin(ALPHA)+dy*math.cos(ALPHA))/length),
                            outerCarbonClearanceM=clear_o,innerCarbonClearanceM=clear_i,
                            outerPlateClearanceM=math.hypot(.200,.542*er_o)-.315,
                            innerPlateClearanceM=math.hypot(.200,.542*er_i)-.315,
                            lugNeckAxialGapM=.214-.188,
                            lugTongueGapM=.214-.212,
                            pinPadGapM=.170-.168,
                            washerNeckVoidGapM=min(.058,.068)-.030,
                            endPlateNeckQGapM=.542-(.070*max(er_o,er_i)+.080),
                            symmetry='Both ends and +/- families use the corrected single outboard lug; absolute-x interval proof applies to all 144 end classes across both caps.'))
    return dict(massT=masses, oneEndStations=details,
                counts=dict(capFrames=36,ringNodes=36*2*NC,splices=36*2*NC,
                            webs=36*2*NC,webEnds=36*4*NC), webSection=web)


def meridians(rows, hub, new):
    sec=tube(.250,.012,RC)
    paths={}
    masses=dict(carbonT=0., bothEndsT=0., saddlesT=0., hubRootsT=0.)
    for layer in ('outer','inner'):
        field=layer+'RadiusM'
        points=[]
        for row in rows:
            points.append((row['xM'],row[field]-.445))
        points.append((hub['xM'],hub[field]))
        segments=[]
        for a,b in zip(points,points[1:]):
            delta=(b[0]-a[0],b[1]-a[1]); length=math.hypot(*delta)
            pin_length=length-.300
            carbon=pin_length-.500
            assert carbon > .400
            segments.append(dict(fromM=list(a),toM=list(b),nodeLengthM=length,
                                 direction=[v/length for v in delta],pinLengthM=pin_length,
                                 carbonCutM=carbon))
        # Forty 2 m barrel bays plus both nineteen-segment caps, for each layer.
        total_carbon=NC*(40*1.200+2*sum(s['carbonCutM'] for s in segments))
        count=NC*(40+2*len(segments))
        masses['carbonT']+=(total_carbon*sec['kgPerM']-2*count*new['meridianChamferRemovedKg'])/1000
        masses['bothEndsT']+=2*count*new['meridianEndKg']/1000
        masses['saddlesT']+=NC*(41+36)*new['saddleKg']/1000
        masses['hubRootsT']+=2*NC*new['hubRootKg']/1000
        paths[layer]=dict(oneEndSegments=segments,totalMembers=count,
                          totalCarbonLengthM=total_carbon,
                          barrelNodePitchM=2.,barrelPinLengthM=1.700,barrelCarbonCutM=1.200)
    return dict(section=sec,paths=paths,massT=masses,
                noCapacityCredit='Two layers priced. All pressure-thrust demand is applied to the outer layer; the inner layer has no assumed load-sharing or free stiffness credit.')


def primitive(phi):
    return phi/2+math.sin(2*phi)/4


def pressure_path(rows,hub,mer,frames,hw,new):
    phis=[row['phiRad'] for row in rows]+[PHI_HUB]
    boundaries=[0.]+[(a+b)/2 for a,b in zip(phis,phis[1:])]+[math.pi/2]
    segments=mer['paths']['outer']['oneEndSegments']
    cut_forces=[]
    for k,s in enumerate(segments):
        axial=Q*math.pi*(R*math.cos(boundaries[k+1]))**2/NC
        force=axial/s['direction'][0]
        cut_forces.append(force)
    barrel_force=Q*math.pi*R**2/NC
    node_rows=[]
    for k,phi in enumerate(phis):
        lo,hi=boundaries[k],boundaries[k+1]
        px=Q*ALPHA*R**2/2*(math.sin(hi)**2-math.sin(lo)**2)
        pr=Q*2*math.sin(ALPHA/2)*R**2*(primitive(hi)-primitive(lo))
        # One half of the adjacent barrel bay belongs to the shoulder node.
        if k==0:
            pr+=Q*2*R*math.sin(ALPHA/2)*1.0
        cprev=barrel_force if k==0 else cut_forces[k-1]
        uprev=[1.,0.] if k==0 else segments[k-1]['direction']
        cnext=0. if k==len(phis)-1 else cut_forces[k]
        unext=[0.,0.] if k==len(phis)-1 else segments[k]['direction']
        axial_residual=cprev*uprev[0]-cnext*unext[0]-px
        close(axial_residual,0.,atol=3e-7)
        radial_required=pr-cprev*uprev[1]+cnext*unext[1]
        hoop=radial_required/(2*math.sin(ALPHA/2))
        hoop_residual=2*hoop*math.sin(ALPHA/2)-radial_required
        close(hoop_residual,0.,atol=1e-7)
        # Offset from ring centre to meridian root, plus two collinear pin arms.
        # The shared ring must accept the resulting moment; no fixity is assigned.
        node_moment=.445*abs(px)
        row=dict(degrees=math.degrees(phi),pressureDualLoDeg=math.degrees(lo),
                 pressureDualHiDeg=math.degrees(hi),axialPressurePerNodeN=px,
                 radialPressurePerNodeN=pr,lowerMeridianCompressionN=cprev,
                 upperMeridianCompressionN=cnext,hoopCompressionN=hoop,
                 residualXN=axial_residual,residualRN=hoop_residual,
                 offsetMomentToRingNm=node_moment,
                 collectorRadialReactionN=radial_required)
        if 0<k<len(phis)-1:
            chord=rows[k]['outerChordM']
            row['outerRingScreen']=screen(hoop,hw['ring'],chord)
            row['bridgeMeanLapShearPa']=abs(hoop)/(math.pi*.250*.500)
            row['bridgeAxialPlusHalfOffsetMomentPa']=abs(hoop)/hw['bridge']['areaM2']+node_moment/2/hw['bridge']['sectionModulusM3']
            f=frames['oneEndStations'][k-1]
            # Alternate radial-transfer ENVELOPE, not an extra applied force or
            # an asserted sharing ratio. Both web ends and the inner hoop are priced.
            web=abs(radial_required)/(2*f['outerRadialDirection'])
            inner_hoop=web*f['innerRadialDirection']/math.sin(ALPHA/2)
            row['webTransferEnvelope']=dict(webCompressionN=web,innerHoopCompressionN=inner_hoop,
                outerArmCornerStressPa=.222*web*(f['outerRadialDirection']/(hw['boxItM4']/.070)+f['outerTangentialDirection']/(hw['boxIrM4']/.080)),
                innerArmCornerStressPa=.222*web*(f['innerRadialDirection']/(hw['boxItM4']/.070)+f['innerTangentialDirection']/(hw['boxIrM4']/.080)),
                webBody=screen(web,frames['webSection'],f['pinLengthM']),
                webEccentricBodyMomentNm=web*.022,
                webDirectPlusEccentricStressPa=web/frames['webSection']['areaM2']+web*.022/frames['webSection']['sectionModulusM3'],
                tongueBearingPa=web/(.048*.024), pinSingleShearPa=web/(math.pi*.040**2/4),
                pinCantileverBendingPa=web*.022/(math.pi*.040**3/32),
                singleLugBearingPa=web/(.016*.040),
                endPlateStripBendingPa=6*web*.022/(.120*.008**2),
                bothEndMeanBondShearPa=web/(math.pi*.294*.296),
                insertWeldMeanShearPa=web/(.003/math.sqrt(2)*math.pi*.294),
                twoLugWeldMeanShearPa=web/(.006/math.sqrt(2)*.240),
                innerRingScreen=screen(inner_hoop,hw['ring'],rows[k]['innerChordM']),
                status='Alternate full radial transfer demand only; actual outer/inner load sharing and out-of-plane cap coupling UNKNOWN')
        node_rows.append(row)
    close(NC*sum(n['axialPressurePerNodeN'] for n in node_rows),Q*math.pi*R**2,rel=1e-12)
    worst=max([barrel_force]+cut_forces)
    meridian_screens=[dict(degreesFrom=math.degrees(phis[k]),
                          **screen(force,mer['section'],s['pinLengthM']))
                      for k,(force,s) in enumerate(zip(cut_forces,segments))]
    end_demand=dict(maximumMeridianCompressionN=worst,
        insertBondMeanShearPa=worst/(math.pi*.225*.194),
        pinDoubleShearPa=worst/(2*math.pi*.080**2/4),
        rootBushBearingPa=worst/(.096*.040),
        steelClevisBearingPa=worst/(2*.020*.080),
        steelInsertStressPa=worst/tube(.225,.006,RS)['areaM2'],
        twoPinRootNetSectionPa=worst/(.040*(.650-2*.096)),
        fourLugWeldMeanShearPa=worst/(.008/math.sqrt(2)*.720),
        insertWeldMeanShearPa=worst/(.004/math.sqrt(2)*math.pi*.225),
        qualifiedCapacityN=None)
    # A single serial-compliance illustration at the most highly loaded end.
    # G variation is a named input sensitivity; neither is a certified bound.
    length=mer['paths']['outer']['barrelCarbonCutM']
    sensitivities=[]
    for g in (1e9,.1e9):
        compliance=length/(E*mer['section']['areaM2'])+2*.0005/(g*math.pi*.225*.194)
        sensitivities.append(dict(adhesiveShearPa=g,complianceMPerN=compliance,
                                  compressionAtMaximumN_M=worst*compliance,
                                  positiveAxialMaterialEnergyJ=.5*worst**2*compliance))
    return dict(factoredPressurePa=Q,oneCapAxialResultantN=Q*math.pi*R**2,
                barrelMeridianForceN=barrel_force,
                barrelMeridianScreen=screen(barrel_force,mer['section'],1.7),
                oneEndNodes=node_rows,oneEndMeridianScreens=meridian_screens,
                bothMeridianEndDemands=end_demand,materialEnergyIllustrations=sensitivities,
                matrixOrder=0,globalPressureCapacityPa=None,
                status='Scalar, statically assigned outer-layer force path; forces balance, but material/joint/film screens fail. No prestress, geometric/follower tangent, ring/axial redistribution or cap-coupled stability solution.')


def packing_mass(chord, centre):
    """Profiled 80 mm-long filler, OD310 to actual node/bridge/base OD.

    Developed chord distance; the same profile repeats at the neighbouring
    vertex. This is a priced shape, not a laminate/contact qualification.
    """
    intervals=[(0.,.300,.310),(.300,chord/2-.502,.250),
               (chord/2-.502,chord/2+.502,.292),
               (chord/2+.502,chord-.300,.250),(chord-.300,chord,.310)]
    total=0.
    for shift in (-chord,0.,chord):
        for lo,hi,diameter in intervals:
            length=max(0.,min(centre+.040,hi+shift)-max(centre-.040,lo+shift))
            total+=annulus(.310,diameter,length,RC)
    return total


def clip_screens(force):
    """Existing two-angle screen, applied to the known load-vector magnitude."""
    return dict(meanBondShearPa=force/(2*.020*.030),
                angleRootBendingPa=6*(force/2)*.010/(.030*.002**2),
                twoM6RootMeanShearPa=force/(2*math.pi*.0048**2/4))


def film_clip_demands(dphi,span,width):
    """Assemble both real bar ends at each shared clip; terminals have one.

    Retain the simply-supported, all-on-bars rectangular-strip approximation:
    a span's width and inward normal are evaluated at its angular midpoint.
    Each end receives half that span's load. Forces below are bar-on-clip
    demands, not the opposite support-on-bar reactions. No film solution or
    unknown shoulder/polar collector contribution is supplied by this screen.
    """
    spans=[]
    for j in range(90):
        phi=(j+.5)*dphi
        tributary=width*math.cos(phi)
        end_force=Q*tributary*span/2
        inward=[-math.sin(phi),-math.cos(phi)]
        spans.append(dict(index=j,fromRow=j,toRow=j+1,
                          midpointDegrees=(j+.5)*.8,surfacePitchM=span,
                          midpointTributaryWidthM=tributary,
                          inwardUnitXR=inward,eachEndResultantN=end_force,
                          eachEndForceXRN=[end_force*c for c in inward]))
    joints=[]
    for j in range(91):
        phi=j*dphi
        adjacent=[k for k in (j-1,j) if 0<=k<90]
        fx=sum(spans[k]['eachEndForceXRN'][0] for k in adjacent)
        fr=sum(spans[k]['eachEndForceXRN'][1] for k in adjacent)
        fn=fx*math.sin(phi)+fr*math.cos(phi)
        ft=fx*math.cos(phi)-fr*math.sin(phi)
        force=math.hypot(fx,fr)
        close(force,math.hypot(fn,ft))
        joints.append(dict(row=j,degrees=j*.8,
                           classification='shoulder terminal' if j==0 else 'polar terminal' if j==90 else 'interior',
                           adjacentSpanIndices=adjacent,knownCapForceXRN=[fx,fr],
                           localOutwardNormalForceN=fn,localIncreasingPhiForceN=ft,
                           knownCapResultantN=force,totalWithUnestablishedLoadsN=None))
    # Every actual span has exactly two represented ends; none is invented at
    # either terminal, and neither end is lost at a shared interior clip.
    assert sum(len(j['adjacentSpanIndices']) for j in joints)==180
    for component in range(2):
        close(sum(j['knownCapForceXRN'][component] for j in joints),
              2*sum(s['eachEndForceXRN'][component] for s in spans))
    control_end=Q*width*span/2
    controlling=max(joints,key=lambda j:j['knownCapResultantN'])
    assert controlling['row']==1
    assert controlling['knownCapResultantN']<=2*control_end
    terminals=[dict(j,capOnlyScreens=clip_screens(j['knownCapResultantN']),
                    additionalInterfaceContributionN=None,
                    interface='UNKNOWN: legacy barrel/shoulder collector' if j['row']==0 else 'UNKNOWN: polar-closure/root collector')
               for j in (joints[0],joints[-1])]
    return dict(
        model='Midpoint rectangular tributaries and simply-supported half-span loads; signed vector assembly, not a compatible film/collector solution.',
        frame='Right cap X is global +x; R is local cylindrical outward radial. At joint phi, outward normal n=(sin(phi),cos(phi)), increasing-phi tangent t=(cos(phi),-sin(phi)). Negative normal demand is inward. Azimuthal component is zero in this symmetric strip approximation.',
        otherCap='Reflect global X force and the X components of n/t; R and local normal/tangent components are unchanged. Rotate the R basis for each of the 666 meridians.',
        tributary='Each span uses L=40*dphi and w=2*40*sin(pi/666)*cos(phi_mid), with uniform inward normal at phi_mid. Full pressure pitch crosses the 4mm stock gaps; the gap removes no pressure area. Bar radial offset is not used to shrink the loaded surface.',
        rightCapSpans=spans,rightCapRows=joints,
        controllingKnownCapRow=controlling,
        controllingCapOnlyScreens=clip_screens(controlling['knownCapResultantN']),
        terminalRows=terminals,
        uniformWidthControl=dict(singleBarEndN=control_end,
                                 sharedInteriorClipN=2*control_end,
                                 terminalKnownCapEndN=control_end,
                                 sharedInteriorScreens=clip_screens(2*control_end),
                                 missingReactionWithOldSingleEndN=control_end,
                                 oldSingleEndSatisfiesInteriorEquilibrium=False),
        status='Known cap-bar demand only. Shoulder/barrel and polar collectors, film in-plane tension, bond peel, actual restraint and load sharing remain UNKNOWN. No fictitious neighbouring bar or zero interface load is asserted. Two bonds/angles/bolts share the known resultant equally for the inherited nominal screen; the full resultant acts at the existing10mm angle lever. This does not qualify the failed fit or transfer.')


def film_support(rows,hub,hw,new,base):
    fine=tube(.166,.006,RC); bar=tube(.043,.001,RC); post=tube(.060,.003,RC)
    dphi=math.radians(.8)
    cap_area=4*math.pi*R**2*math.sin(PHI_LAST)
    fine_rows=[]
    fine_length=0.
    for index in range(1,91):
        phi=index*dphi
        if index%5==0:
            continue  # Shared with the ONE charged outer main frame at that station.
        radius=R*math.cos(phi)-.089
        length=2*math.pi*radius
        fine_length+=2*(length-NC*.004)
        fine_rows.append(dict(degrees=index*.8,radiusM=radius,
                              segmentArcM=length/NC,segmentsBothCaps=2*NC))
    n_fine=2*len(fine_rows)*NC
    # Fine ring -> meridian connections use radial posts at all 37 columns.
    # Main-frame film support uses 666 radial positions, including chord sag.
    post_lengths=[]; conflicts=[]; main_packing=0.
    for row in rows[1:]:
        ro=row['outerRadiusM']
        for j in range(NF):
            theta=2*math.pi*j/NF
            local=theta%ALPHA-math.pi/NC
            support_radius=ro*math.cos(math.pi/NC)/math.cos(local)
            along=support_radius*math.sin(local)+row['outerChordM']/2
            main_packing+=packing_mass(row['outerChordM'],along)
            clear=row['surfaceRadiusM']-.0215-(support_radius+.165)-.020
            if clear<.080:
                conflicts.append(dict(degrees=row['degrees'],column=j,availableLengthM=clear))
            post_lengths.append(max(.080,clear))
    # The cap meridian is a straight segment between main stations, not the
    # surface circle. Interpolate its actual radius at each fine-hoop x.
    path=[(r['xM'],r['outerRadiusM']-.445) for r in rows]
    fine_post_rows=[]
    for row in fine_rows:
        x=40+R*math.sin(math.radians(row['degrees']))
        for a,b in zip(path,path[1:]):
            if a[0]<=x<=b[0]:
                radius=a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]);break
        clear=row['radiusM']-.089-(radius+.125)-.020
        fine_post_rows.append(dict(degrees=row['degrees'],lengthM=max(.080,clear),availableLengthM=clear))
        if clear<.080:
            conflicts.append(dict(degrees=row['degrees'],column='fine-meridian',availableLengthM=clear))
    all_post_length=2*sum(post_lengths)+2*NC*sum(r['lengthM'] for r in fine_post_rows)
    n_posts=2*len(post_lengths)+2*NC*len(fine_post_rows)
    # 90 cap bays, 666 bars, both ends; 91 attachment/splice rows per cap.
    bar_length=2*NF*(R*PHI_LAST-90*.004)
    n_bar_joints=2*91*NF
    mass=dict(fineHoopCarbonT=fine_length*fine['kgPerM']/1000,
              fineHoopSplicesT=n_fine*new['fineSpliceKg']/1000,
              meridionalFilmBarsT=bar_length*bar['kgPerM']/1000,
              filmBarSplicesT=n_bar_joints*new['barSpliceKg']/1000,
              filmBarClipsT=n_bar_joints*new['filmClipKg']/1000,
              radialPostCarbonT=all_post_length*post['kgPerM']/1000,
              radialPostHardwareT=n_posts*new['standOffHardwareKg']/1000,
              profiledFootPackingT=(2*main_packing+2*NC*len(fine_post_rows)*annulus(.310,.250,.080,RC))/1000,
              filmThicknessSupplementT=cap_area*base['model']['wall']['filmKgM2']*(R*dphi/.5-1)/1000)
    span=R*dphi; width=2*R*math.sin(math.pi/NF)
    moment=Q*width*span**2/8
    max_radius=fine_rows[0]['radiusM']
    hoop_n=Q*span*max_radius
    hoop_span=2*math.pi*max_radius/NC
    # One shared clip receives both adjoining bar-end vectors. Its two real
    # terminal cases have only one cap span, with other interface loads unknown.
    clips=film_clip_demands(dphi,span,width)
    clip_force=clips['controllingKnownCapRow']['knownCapResultantN']
    clip_stress=clips['controllingCapOnlyScreens']
    # One-way trough: h=a/4, rho=(a²+h²)/(2h), T=p*rho. No two-way credit.
    a=max(span,width)/2; h=a/4; rho=(a*a+h*h)/(2*h)
    tension=Q*rho
    critical_post=max([r['lengthM'] for r in fine_post_rows]+post_lengths)
    post_force=Q*span*(2*math.pi*R/NC)
    return dict(massT=mass, capAreaTo72M2=cap_area,
                fineHoopsPerCap=72,fineHoopRows=fine_rows,
                fineMeridianPostRows=fine_post_rows,
                barCountAround=NF,capSurfacePitchM=span,maxAzimuthalFilmSpanM=width,
                capBarSegments=2*90*NF,capBarSplicesAndClips=n_bar_joints,
                posts=n_posts,postCarbonLengthM=all_post_length,
                mainFramePostMinimumAvailableM=min(p['availableLengthM'] for p in conflicts) if conflicts else min(post_lengths),
                insufficientPostLengthCount=len(conflicts)*2,
                representativeFitFailures=conflicts[:3],
                fineBarToOrdinaryHoopNormalGapM=(.089-.0215)-(.083+.0215),
                fineBarToSpliceCuffNormalGapM=(.089-.0215)-(.089+.0215),
                filmSupportFit='FAIL: the selected bar radial datum overlaps ordinary fine hoops by37mm and their splice cuffs by43mm; 888 main support locations also cannot fit the selected minimum80mm post. All chosen stock/hardware/packing remains charged; no buildability or old-mass deletion is claimed.',
                barBendingMomentNm=moment,barBendingStressPa=moment/bar['sectionModulusM3'],
                barNominalPass=moment/bar['sectionModulusM3']<=CARBON_PROXY,
                fineHoopScreen=screen(hoop_n,fine,hoop_span),
                fineHoopSteelSpliceStressPa=hoop_n/tube(.178,.005,RS)['areaM2'],
                fineHoopBondMeanShearPa=hoop_n/(math.pi*.166*.200),
                filmOneWayFactoredTensionNPerM=tension,
                clipReactionAssembly=clips,
                clipControllingDegrees=clips['controllingKnownCapRow']['degrees'],
                clipCapResultantN=clip_force,
                clipMeanBondShearPa=clip_stress['meanBondShearPa'],
                clipAngleRootBendingPa=clip_stress['angleRootBendingPa'],
                twoM6RootMeanShearPa=clip_stress['twoM6RootMeanShearPa'],
                maximumRadialPost=screen(post_force,post,critical_post),
                status='FAIL/UNKNOWN: nominal fine-hoop, clips, post and local fit do not qualify the new wall. Legacy capGrid/wall/flight mass remains charged and supplies no claimed bracing credit.')


def polar(rows,hub,new,pressure):
    area_one=2*math.pi*R**2*(1-math.sin(PHI_LAST))
    t=.012
    box_area=.600*.500-(.600-.024)*(.500-.024)
    box_i=(.500*.600**3-(.500-.024)*(.600-.024)**3)/12
    seam_len=NC*R*(PHI_HUB-PHI_LAST)
    root=rows[-1]['surfaceRadiusM']
    ring_circ=2*math.pi*root
    standoff=tube(.040,.004,RS)
    mass=dict(twoDomePlatesT=2*area_one*t*RS/1000,
              twoHubBoxesT=2*2*math.pi*3*box_area*RS/1000,
              goreAndButtonCoverStrapsT=2*(seam_len*.060*.006+2*math.pi*3*.080*.006)*RS/1000,
              allCoverWeldsT=2*.5*.006**2*(2*seam_len+4*math.pi*3)*RS/1000,
              twoRootFlangesT=2*ring_circ*.200*.012*RS/1000,
              rootFlangeWeldT=2*.5*.008**2*2*ring_circ*RS/1000,
              rootBoltsT=2*NC*8*new['m16SetKg']/1000,
              domeHubPostsT=2*NC*.500*standoff['kgPerM']/1000,
              domePostFeetT=2*NC*(2*.100*.100*.008*RS+4*fastener(.012,.060,.018,.0075,.010,.024,.013,.0025))/1000,
              domePostWeldsT=2*NC*.5*.006**2*(2*math.pi*.040+2*.400)*RS/1000,
              rootGasketsT=2*ring_circ*.200*.002*1100/1000)
    last=pressure['oneEndNodes'][-1]
    dome_axial=Q*math.pi*root**2
    hub_post_force=last['axialPressurePerNodeN']
    strip=2*math.pi*root/NC
    bending=6*(Q*strip**2/8)/t**2
    membrane=Q*R/(2*t)
    hub_h=last['hoopCompressionN']
    return dict(massT=mass,eachDomeAreaM2=area_one,polarButtonSurfaceRadiusM=3.,
                eachButtonAreaM2=2*math.pi*R**2*(1-math.sin(PHI_HUB)),
                eachDomeAxialResultantN=dome_axial,
                membraneCompressionPa=membrane,unsupportedStripWidthAtRootM=strip,
                oneWayPlateBendingPa=bending,plateNominalPass=membrane+bending<=FY,
                rootLineLoadNPerM=dome_axial/ring_circ,
                rootFlangeToFrameCuffRadialGapM=root-.200-(rows[-1]['outerRadiusM']+.165),
                rootFlangeFit='FAIL: selected 200mm flange cannot span the inset frame-to-skin gap; no unpriced transition plate or load path is credited.',
                rootEightBoltGroupN=dome_axial/NC,
                eachM16RootShearPa=(dome_axial/NC/8)/(math.pi*.013**2/4),
                hubHoopSignedCompressionN=hub_h,hubAxialStressPa=abs(hub_h)/box_area,
                hubOffsetMomentTrialNm=.500*hub_post_force,
                hubAxialPlusMomentPa=abs(hub_h)/box_area+.500*hub_post_force/(box_i/.300),
                domeHubPostScreen=screen(hub_post_force,standoff,.500,modulus=200e9,ceiling=FY),
                status='Finite 12 mm spherical closure and nonzero steel hub are fully charged; plate bending, hub posts/root transfer FAIL or UNKNOWN. No zero-radius frame, pole point support, dome buckling or weld qualification.')


def attachment(prior,new):
    original=prior['erectionAttachment']
    # Added cap fine-hoop clamps: four per 37-column sector. Existing 40,393
    # I014 attachments remain in the carried bill; their removal is not justified.
    count=2*72*148
    return dict(additionalCount=count,eachKg=original['eachKg'],
                addedAzimuthRule='theta=2*pi*(j+0.5)/148: offset from each37-column hoop splice',
                additionalMassT=count*original['eachKg']/1000,
                inheritedCount=original['totalCount'],inheritedMassT=original['totalT'],
                demandN=original['demandN'],requiredNominalN=original['requiredNominalN'],
                jawStressPa=original['jawBendingPa'],flangeStressPa=original['flangeBendingPa'],
                flangeNominalPass=False,qualifiedCapacityN=None,
                status='Same I014 8 mm jaw / 6 mm flange and full original 7.018733 kN erection demand, without dilution by extra clamps. Flange FAIL, grip/patch/welds and wind/cradle/load redistribution UNKNOWN.')


def ledger(base,prior,frames,mer,film,dome,attachments):
    old=base['model']['ledgerT']; frac=41/104
    retained_rows={k:dict(originalT=v,retainedT=v,reason='Retained: replacement of this flight, wall or contingency duty is not established') for k,v in old.items()}
    for key in ('innerRings','thetaWebs'):
        retained_rows[key]['retainedT']=old[key]*(1-frac)
        retained_rows[key]['reason']='I014 already replaced only 41/104; residual 63/104 cap/equivalent family stays charged'
    joint_removed=(old['innerRings']+old['thetaWebs'])*frac*.15/.85
    retained_rows['tiJoints']['retainedT']=old['tiJoints']-joint_removed
    retained_rows['tiJoints']['reason']='Only I014 attributed 41/104 inner/theta joint share already removed; all residual joints remain'
    retained_rows['clamps']['retainedT']=0.
    retained_rows['clamps']['reason']='Already replaced by the explicit I014 attachment bill; not subtracted again'
    retained=sum(row['retainedT'] for row in retained_rows.values())
    close(retained,prior['mass']['retainedOtherHullT'])
    additions={}
    for label,group in [('capFrames',frames['massT']),('meridians',mer['massT']),
                        ('filmSupport',film['massT']),('polarClosure',dome['massT'])]:
        for key,val in group.items():
            additions[label+'.'+key]=val
    additions['addedCapAttachmentsT']=attachments['additionalMassT']
    carried=dict(prior['mass']['newBillT'])
    new_bill=sum(carried.values())+sum(additions.values())
    hull=retained+new_bill
    close(hull,prior['mass']['hullT']+sum(additions.values()))
    close(hull,prior['mass']['hullT']-sum(carried.values())+new_bill)
    # Maintain the original loss; do not credit either a steel dome's smaller
    # drape or any local protrusion. Add a one-sided span and facet debit.
    cap_area=film['capAreaTo72M2']
    span_debit=cap_area*(film['capSurfacePitchM']-.5)/16
    facet_sag=R*(1-math.cos(math.radians(.4)))+R*(1-math.cos(math.pi/NF))
    facet_debit=cap_area*facet_sag
    volume=base['effectiveVolumeM3']-span_debit-facet_debit
    gas=base['gas']['pressurePa']*volume/(base['gas']['gasConstant']*base['gas']['temperatureK'])/1000
    new_frame=sum(carried.values())-carried['erectionAttachmentsT']+sum(frames['massT'].values())+sum(mer['massT'].values())+sum(dome['massT'].values())
    nonframe=retained+sum(film['massT'].values())+attachments['inheritedMassT']+attachments['additionalMassT']
    close(hull,new_frame+nonframe)
    at=[]
    for a in base['at']:
        lift=a['rhoAirKgM3']*volume/1000
        at.append(dict(altitudeM=a['altitudeM'],rhoAirKgM3=a['rhoAirKgM3'],liftT=lift,
                       knownMarginT=lift-hull-gas,
                       matchedOriginalVolumeMarginT=a['liftT']-hull-base['gas']['massT'],
                       i014MarginT=next(v['knownMarginT'] for v in prior['mass']['at'] if v['altitudeM']==a['altitudeM'])))
    allowance=at[0]['liftT']-gas-nonframe
    assert allowance < prior['mass']['maximumNewFrameT'] < 0
    assert all(a['knownMarginT']<0 for a in at)
    return dict(legacyRows=retained_rows,retainedOtherHullT=retained,
                carriedI014NewBillT=carried,addedBillT=additions,addedTotalT=sum(additions.values()),
                removedLegacyMassBeyondI014T=0.,newCompleteBillT=new_bill,hullT=hull,
                baselineEffectiveVolumeM3=base['effectiveVolumeM3'],extraSpanDebitM3=span_debit,
                additionalFacetDebitM3=facet_debit,selectedVolumeProxyM3=volume,
                residualGasOnceT=gas,knownSubtotalT=hull+gas,
                frameAndPolarAndMeridianT=new_frame,nonframeHullT=nonframe,
                maximumNewFrameT=allowance,i014MaximumNewFrameT=prior['mass']['maximumNewFrameT'],
                i014FrameT=prior['mass']['frameAndNodeT'],i014HullT=prior['mass']['hullT'],
                at=at,allUpMassT=None,allUpMarginT=None,
                replacementPolicy='No new legacy deletion. New outer cap main rings are shared with their pressure-hoop duty and are counted once; fine hoop count excludes them. Unresolved old wall/cap/flight rows remain mass contingencies, not active stiffness. This failed layout is not an installable full-hull design.',
                volumeQualification='Bookkeeping proxy only: retained I008 loss plus conservative added span/facet debit. Actual film shape, local support protrusions, pressure collapse and displacement volume UNKNOWN.')


def calculate():
    frozen=json.loads((HERE/'baseline.json').read_text())
    for p,d in frozen['referenceFiles'].items():
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
    base=frozen['case80']; prior=frozen['i014']; hw=prior['hardware']
    close(sum(base['model']['ledgerT'].values()),base['model']['totalT'])
    rows,hub=geometry(prior); new=new_hardware(hw)
    frames=cap_frames(rows,hw,new); mer=meridians(rows,hub,new)
    pressure=pressure_path(rows,hub,mer,frames,hw,new)
    film=film_support(rows,hub,hw,new,base)
    dome=polar(rows,hub,new,pressure); attach=attachment(prior,new)
    mass=ledger(base,prior,frames,mer,film,dome,attach)
    # The selected unnotched cuff is an explicit failed solid arrangement:
    # at r=t=0, pad occupies x155..168mm and steel occupies x157..165mm.
    witness=.160
    assert .314/2 < witness < .330/2
    assert .310/2 < witness < .168
    cuff_fit=dict(witnessLocalXRTM=[witness,0.,0.],
        padAxialIntervalAtR0M=[.155,.168],steelCuffIntervalAtR0M=[.157,.165],
        overlapAlongXAtR0M=.008,
        symmetry='Both signs of x, both ring layers, all selected meridian cuffs; node-centred film foot cuffs have the same clash.',
        status='FAIL: unnotched330/314 cuffs intersect integral pads. No unpriced notch, replacement root or transferred clamp capacity is credited.')
    return dict(unit='R3-I016',baselineSha256=hashlib.sha256((HERE/'baseline.json').read_bytes()).hexdigest(),
                geometry=dict(diameterM=80.,totalLengthM=160.,barrelStationCount=41,
                              barrelXRule='x=-40+2k, k=0..40; 111 ring nodes',
                              capNodeRule='37 nodes, theta=2*pi*j/37, aligned to barrel node 3j',
                              oneCapMainStations=rows,otherCap='Reflection x -> -x',polarHub=hub,
                              capInnerOuterRatio=prior['geometry']['innerRingRadiusM']/prior['geometry']['outerRingRadiusM'],
                              capWebIndexOffsets=[-1,1],capWebFamilyPlanesM=[-.2,.2],
                              capWebSetbackEachM=WEB_SETBACK,capWebInsertM=.300,
                              capWebEffectiveBondM=.296,capWebWeldReliefM=.004,
                              meridianRootRadialOffsetM=.445,meridianPinOffsetEachM=.150,
                              meridianCarbonSetbackEachM=.250,meridianInsertM=.200,
                              meridianEffectiveBondM=.194,meridianWeldReliefM=.006),
                newHardware=new,nominalCuffInterference=cuff_fit,capFrames=frames,meridians=mer,
                pressure=pressure,filmSupport=film,polarClosure=dome,
                erectionAttachment=attach,mass=mass,
                qualification='FAIL: nominal thrust members/end fittings, fine pressure hoops, polar plate/supports and inherited erection flange; local film support fit also fails. Bond/laminate/assembly/global pressure and U+C UNKNOWN. No float demonstrated.',
                weakestAssumption='A closed, noninterfering pressure-wall-to-ring/meridian/polar connection path; scalar force balance does not establish this or global stability.',
                nextGeometry='Replace the single outer meridian pressure path by one explicitly triangulated two-layer cap truss with normal-oriented film-support nodes and a finite polar compression ring; price the new axial end blocks and force split before selecting any legacy cap deletion.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    m=p.add_mutually_exclusive_group();m.add_argument('--write',action='store_true');m.add_argument('--check',action='store_true')
    args=p.parse_args();result=calculate()
    if args.write:
        (HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    elif args.check:
        compare(result,json.loads((HERE/'result.json').read_text()))
        print('I016 reproduction PASS: pins, finite station/joint counts, signed adjacent-bar clip assembly, sector equilibrium, conservative complete ledger and gas-once identities. Construction/strength FAIL; global and physical UNKNOWN.')
    else:
        print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
