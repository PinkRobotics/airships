#!/usr/bin/env python3
"""One dimensioned continuous force-path trial; no physical qualification.

Endpoint energy helpers are adapted from ../R3-I011/calc.py. Neither the
frozen hull model nor I011's calculation is executed by this script.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
N = 111
ALPHA = 2*math.pi/N
PRESSURE = 101325.0
SF = 1.2
SURFACE_R = 40.0
DEPTH = 60/13
OUTER_R = SURFACE_R - .310/2
INNER_R = OUTER_R - DEPTH
BAY = 2.0
STATIONS = 41
E_CARBON = 135e9
RHO_CARBON = 1600.0
E_STEEL = 200e9
RHO_STEEL = 7850.0
FY_STEEL = 355e6
RHO_ADHESIVE = 1200.0
WEB_SETBACK = .400
AXIAL_LAYER = .200
LUG_ECCENTRICITY = .022
LOAD_ARM = AXIAL_LAYER + LUG_ECCENTRICITY
GAP = .004
LAP = .500
NODE_LENGTH = .600
WEB_CHAMFER = .004
WEB_BOND_LENGTH = .300-WEB_CHAMFER

def close(a, b, rel=1e-9, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol), (a, b)

def tube(diameter, wall, density):
    area = math.pi * (diameter**2 - (diameter - 2*wall)**2) / 4
    inertia = math.pi * (diameter**4 - (diameter - 2*wall)**4) / 64
    return dict(odM=diameter, wallM=wall, areaM2=area, inertiaM4=inertia,
                sectionModulusM3=2*inertia/diameter, kgPerM=density*area)

def shapes(mode):
    """u_r=a*cos(n theta), u_t=b*sin(n theta), for each of two rings."""
    result = np.zeros((2*N, 2, 4))
    for ring in range(2):
        for j in range(N):
            theta = j*ALPHA
            er = np.array([math.cos(theta), math.sin(theta)])
            et = np.array([-math.sin(theta), math.cos(theta)])
            result[N*ring+j, :, 2*ring] = er*(math.cos(mode*theta) if mode else 1)
            result[N*ring+j, :, 2*ring+1] = et*(math.sin(mode*theta) if mode else 1)
    return result

def matrices(members, mode):
    basis = shapes(mode)
    parts = {family: np.zeros((4, 4)) for family in ('outer', 'inner', 'plus', 'minus')}
    for member in members:
        extension = member['direction'] @ (basis[member['b']] - basis[member['a']])
        parts[member['family']] += member['stiffness']*np.outer(extension, extension)
    return basis, parts, sum(parts.values())

def arithmetic(members, xy):
    """One geometry: n=2..55 elastic diagnostics, plus n=0/1 checks."""
    basis0, parts0, k0 = matrices(members, 0)
    # Exact resultant of normal pressure over a circular tributary sector.
    node_load_per_pa = 2*SURFACE_R*BAY*math.sin(ALPHA/2)
    load = np.array([-N*node_load_per_pa, 0.0])
    radial = np.linalg.solve(k0[np.ix_([0, 2], [0, 2])], load)
    close(float(np.linalg.norm(k0[np.ix_([0, 2], [0, 2])]@radial-load)), 0, abs_tol=1e-7)
    q0 = np.array([radial[0], 0, radial[1], 0])*PRESSURE*SF
    forces, screens = {}, {}
    for family in parts0:
        member = next(m for m in members if m['family'] == family)
        force = member['stiffness']*float(member['direction'] @ (
            (basis0[member['b']]-basis0[member['a']])@q0))
        section = member['section']
        length = member['length']
        euler = math.pi**2*E_CARBON*section['inertiaM4']/length**2
        # Same unqualified local-shell proxy as I008, now on an actual section.
        local = min(1450e6, .30*.605*.5699*E_CARBON*section['wallM'] /
                    ((section['odM']-section['wallM'])/2))
        compression = max(0, -force)
        weight_moment = SF*section['kgPerM']*9.80665*length**2/8
        eccentric_moment = compression*LUG_ECCENTRICITY if family in ('plus','minus') else 0.
        amplified = (weight_moment+eccentric_moment)/(1-compression/euler) if compression < euler else None
        interaction = (compression/(section['areaM2']*local) +
                       amplified/(section['sectionModulusM3']*local)) if amplified else None
        forces[family] = force
        screens[family] = dict(pinLengthM=length, carbonCutLengthM=member['carbonLength'],
            compressionN=compression, eulerN=euler, localProxyPa=local,
            directStressPa=compression/section['areaM2'], gravityMomentNm=weight_moment,
            singleLugEccentricMomentNm=eccentric_moment,
            amplifiedGravityPlusEccentricMomentNm=amplified, interaction=interaction,
            proxyPass=interaction is not None and interaction <= 1,
            status='Conditional section screen only; laminate, joints and bracing unqualified.')
    # No fictitious foundation: free rigid translation/rotation carry no axial energy.
    rigid_checks = []
    for mode, vector in [(0, np.array([0, OUTER_R, 0, INNER_R])),
                         (1, np.array([1., -1., 1., -1.]))]:
        _, _, k = matrices(members, mode)
        residual = float(np.linalg.norm(k@vector)/(np.linalg.norm(k)*np.linalg.norm(vector)))
        assert residual < 1e-12
        rigid_checks.append(dict(mode=mode, relativeResidual=residual))
    rows = []
    for mode in range(2, N//2+1):
        basis, parts, k = matrices(members, mode)
        eig = np.linalg.eigvalsh(k)
        assert float(eig[0]) > 0
        q = np.r_[1., np.linalg.solve(k[1:, 1:], -k[1:, 0])]
        stiffness = float(q@k@q)
        energies = {family: float(q@part@q) for family, part in parts.items()}
        close(sum(energies.values()), stiffness, rel=1e-8)
        row = dict(mode=mode, normalizedVector=q.tolist(), condensedNPerM=stiffness,
                   twiceEnergyByFamily=energies,
                   negativeGeometricCoefficientThresholdM=stiffness/(SF*PRESSURE),
                   bucklingPressurePa=None)
        if mode in (2, 28, 55):
            row['matrixNPerM'] = k.tolist()
        rows.append(row)
    # Independent finite-extension energy on a nontrivial four-coordinate probe.
    basis, _, k = matrices(members, 3)
    probe = np.array([1., .3, -.4, .2])*1e-4
    displaced = xy + np.einsum('ijk,k->ij', basis, probe)
    exact_energy = sum(.5*m['stiffness']*(float(np.linalg.norm(
        displaced[m['b']]-displaced[m['a']]))-m['length'])**2 for m in members)
    linear_energy = .5*float(probe@k@probe)
    close(exact_energy, linear_energy, rel=2e-5)
    # Outer ring unit tangential displacement with inner ring held: a diagnostic
    # shear stiffness, not a support installed in the aircraft.
    shear_vector = np.array([0., 1., 0., 0.])
    shear_k = float(shear_vector@(parts0['plus']+parts0['minus'])@shear_vector)
    return dict(factoredPressurePa=PRESSURE*SF, nodeLoadPerPaM2=node_load_per_pa,
        uniformDisplacementAtFactoredPressureM=q0.tolist(), axialForcesAtFactoredPressureN=forces,
        sectionScreens=screens, rigidMotionChecks=rigid_checks, modes=rows,
        minimumElasticMode=min(rows, key=lambda row: row['condensedNPerM'])['mode'],
        diagnosticWebShearNPerM=shear_k, finiteExtensionEnergyJ=exact_energy,
        linearEnergyJ=linear_energy, globalStability='UNKNOWN: no prestress/follower-load geometric tangent or out-of-plane connection analysis; elastic stiffness is not a pressure capacity.')

def compare(a, b):
    if isinstance(a, dict):
        assert a.keys()==b.keys()
        for key in a: compare(a[key], b[key])
    elif isinstance(a, list):
        assert len(a)==len(b)
        for x, y in zip(a,b): compare(x,y)
    elif isinstance(a, float): close(a,b,rel=1e-8,abs_tol=1e-7)
    else: assert a==b, (a,b)


def annulus(outer, inner, length, density):
    return math.pi*(outer**2-inner**2)/4*length*density


def hardware():
    ring = tube(.250, .012, RHO_CARBON)
    node = tube(.310, (.310-.226)/2, RHO_CARBON)
    bridge = tube(.292, .020, RHO_CARBON)  # 252 mm bore; 1 mm radial bond.
    insert = tube(.294, .003, RHO_STEEL)
    box_area = .160*.140-.136*.116
    box_it = (.160*.140**3-.136*.116**3)/12
    box_ir = (.140*.160**3-.116*.136**3)/12
    # Fill the curved 310 mm OD surface to x=168 mm over r=+/-70 mm.
    radius, half_width, face = .155, .070, .168
    curved_integral = (half_width*math.sqrt(radius**2-half_width**2)
                       + radius**2*math.asin(half_width/radius))
    pad_area = 2*half_width*face-curved_integral
    assert pad_area > 0
    node_parts = dict(
        localCarbon=annulus(.310,.250,NODE_LENGTH,RHO_CARBON),
        twoCurvedPads=2*pad_area*.160*RHO_CARBON,
        twoBoxNecks=2*box_area*.020*RHO_CARBON,
        twoLandingPlates=2*(.180*.160-math.pi*.049**2/4)*.024*RHO_CARBON,
        twoBushes=2*annulus(.048,.040,.024,RHO_STEEL),
        twoBushBonds=2*annulus(.049,.048,.024,RHO_ADHESIVE))
    splice_parts = dict(
        carbonBridge=bridge['kgPerM']*(2*LAP+GAP),
        twoLapBonds=annulus(.252,.250,2*LAP,RHO_ADHESIVE))
    # Pin at q=0, clevis extends q=-50..392 mm, plate q=392..400 mm,
    # carbon begins q=400 mm, insert continues inside it to q=700 mm.
    web_end = dict(
        insert=insert['kgPerM']*.300,
        endPlate=math.pi*.320**2/4*.008*RHO_STEEL,
        oneOutboardLug=(.442*.120-math.pi*.040**2/4)*.016*RHO_STEEL,
        pin=math.pi*.040**2/4*.120*RHO_STEEL,
        twoWashers=2*annulus(.060,.042,.005,RHO_STEEL),
        retainers=.020,
        insertBond=annulus(.295,.294,WEB_BOND_LENGTH,RHO_ADHESIVE),
        insertWeld=.5*.003**2*math.pi*.294*RHO_STEEL,
        twoLugWelds=.5*.006**2*.240*RHO_STEEL)
    return dict(ring=ring,node=node,bridge=bridge,insert=insert,
        boxAreaM2=box_area,boxItM4=box_it,boxIrM4=box_ir,
        padAreaM2=pad_area,nodePartsKg=node_parts,nodeKg=sum(node_parts.values()),
        splicePartsKg=splice_parts,spliceKg=sum(splice_parts.values()),
        webEndPartsKg=web_end,webEndKg=sum(web_end.values()),
        carbonChamferRemovedKgEach=math.pi*WEB_CHAMFER/12*(.300**2+.300*.295-2*.295**2)*RHO_CARBON,
        lapAreaM2=math.pi*.250*LAP,webBondAreaM2=math.pi*.294*WEB_BOND_LENGTH)


def ring_compliance(length, hw, adhesive_g):
    # Uniform shear transfer in each lap: N_tube=N(1-s/l), N_bridge=Ns/l.
    # Integral N(s)^2/(EA) gives l/(3EA) for each participating member.
    free = length-GAP-2*LAP-NODE_LENGTH
    assert free > 0
    parts = dict(
        freeBase=free/(E_CARBON*hw['ring']['areaM2']),
        integralNode=NODE_LENGTH/(E_CARBON*hw['node']['areaM2']),
        lapCarbons=2*LAP/3/E_CARBON*(1/hw['ring']['areaM2']+1/hw['bridge']['areaM2']),
        bridgeGap=GAP/(E_CARBON*hw['bridge']['areaM2']),
        twoAdhesiveLaps=2*.001/(adhesive_g*hw['lapAreaM2']))
    return parts


def web_end_compliance(radial, tangential, hw, shear_g, adhesive_g, extra):
    # Full 222 mm load-line lever represented as the minimum neck section. This is a
    # homogeneous-section sensitivity hypothesis, not measured root stiffness.
    parts = dict(
        neckBending=LOAD_ARM**3/(3*E_CARBON)*(
            radial**2/hw['boxItM4']+tangential**2/hw['boxIrM4']),
        neckShear=LOAD_ARM/(.8*shear_g*hw['boxAreaM2']),
        webBond=.0005/(adhesive_g*hw['webBondAreaM2']),
        fullInsert=.300/(E_STEEL*hw['insert']['areaM2']),
        oneLugAxial=.400/(E_STEEL*.016*(.120-.040)),
        cantileverPinBending=LUG_ECCENTRICITY**3/(3*E_STEEL*(math.pi*.040**4/64)),
        endPlateStripBending=LUG_ECCENTRICITY**3/(3*E_STEEL*(.120*.008**3/12)),
        additionalUnresolvedContact=extra)
    return parts


def lattice(hw, trial):
    sections=dict(ring=hw['ring'],web=tube(.300,.0025,RHO_CARBON))
    xy=np.array([[r*math.cos(j*ALPHA),r*math.sin(j*ALPHA)]
                 for r in (OUTER_R,INNER_R) for j in range(N)])
    members=[]
    for family in ('outer','inner','plus','minus'):
        for j in range(N):
            if family=='outer': a,b=j,(j+1)%N
            elif family=='inner': a,b=N+j,N+(j+1)%N
            else: a,b=j,N+(j+(2 if family=='plus' else -2))%N
            delta=xy[b]-xy[a]; length=float(np.linalg.norm(delta)); direction=delta/length
            web=family in ('plus','minus'); sec=sections['web' if web else 'ring']
            if web:
                end={}
                for label,index in [('outer',a),('inner',b)]:
                    er=xy[index]/np.linalg.norm(xy[index]); et=np.array([-er[1],er[0]])
                    end[label]=web_end_compliance(float(direction@er),float(direction@et),hw,
                        trial['compositeShearPa'],trial['adhesiveShearPa'],trial['extraEndComplianceMPerN'])
                carbon_length=length-2*WEB_SETBACK
                ends=sum(sum(v.values()) for v in end.values())
                eccentric=LUG_ECCENTRICITY**2*carbon_length/(E_CARBON*sec['inertiaM4'])
                compliance=carbon_length/(E_CARBON*sec['areaM2'])+eccentric+ends
                parts=dict(carbonBody=carbon_length/(E_CARBON*sec['areaM2']),
                    carbonEccentricBending=eccentric,twoEnds=ends)
            else:
                carbon_length=length-GAP; end=None
                parts=ring_compliance(length,hw,trial['adhesiveShearPa']); compliance=sum(parts.values())
            members.append(dict(family=family,a=a,b=b,length=length,carbonLength=carbon_length,
                direction=direction,stiffness=1/compliance,section=sec,
                compliancePartsMPerN=parts,endCompliancePartsMPerN=end))
    return xy,members,sections


def connection_screens(hw, members, mech):
    forces=mech['axialForcesAtFactoredPressureN']
    ring_force=max(abs(forces['outer']),abs(forces['inner']))
    web_force=max(abs(forces['plus']),abs(forces['minus']))
    # Vector offset moments, with +x as the vehicle axis, at outer and inner node.
    resultants={}; arm_screens=[]
    for label,index in [('outer',0),('inner',N)]:
        total_f=np.zeros(3); total_m=np.zeros(3)
        for m in members:
            if m['family'] not in ('plus','minus') or index not in (m['a'],m['b']):continue
            sign=1 if index==m['a'] else -1
            force=np.r_[0.,sign*forces[m['family']]*m['direction']]
            offset=np.array([LOAD_ARM*(1 if m['family']=='plus' else -1),0.,0.])
            arm_m=np.cross(offset,force)
            total_f+=force; total_m+=arm_m
            # At these j=0 nodes global y,z are local radial,tangential.
            biaxial=(abs(float(arm_m[1]))/(hw['boxIrM4']/.080)
                     + abs(float(arm_m[2]))/(hw['boxItM4']/.070))
            arm_screens.append(dict(node=label,family=m['family'],
                forceN=force.tolist(),momentNm=arm_m.tolist(),
                cornerBendingRequiredPa=biaxial))
        resultants[label]=dict(webResultantN=total_f.tolist(),offsetMomentNm=total_m.tolist())
    moment=max(float(np.linalg.norm(v['offsetMomentNm'])) for v in resultants.values())
    # Use half the resultant moment in each outgoing ring leg only as a
    # symmetric split hypothesis; report the full resultant as the required path.
    joint_moment=moment/2
    single_arm_m=web_force*LOAD_ARM
    bridge_stress=ring_force/hw['bridge']['areaM2']+joint_moment/hw['bridge']['sectionModulusM3']
    bridge_local=min(1450e6,.30*.605*.5699*E_CARBON*.020/((.292-.020)/2))
    return dict(ringCompressionN=ring_force,webCompressionN=web_force,
        circumferenceJoint=dict(bridgeAreaM2=hw['bridge']['areaM2'],
            meanLapShearPa=ring_force/hw['lapAreaM2'],
            meanBondSlipMAt1GPa=ring_force*.001/(1e9*hw['lapAreaM2']),
            uniformAxialStressPa=ring_force/hw['bridge']['areaM2'],
            halfNodeMomentTrialNm=joint_moment,
            axialPlusHalfMomentPa=bridge_stress,localProxyPa=bridge_local,
            proxyInteraction=bridge_stress/bridge_local,
            peakShearPeelAndRotationCapacity=None,
            status='Nominal carbon bridge screen only; lap strength, peel, laminate, cure and rotational transfer UNKNOWN.'),
        nodeResultants=resultants,singleArmMomentNm=single_arm_m,
        biaxialArmScreens=arm_screens,
        maximumArmCornerBendingPa=max(a['cornerBendingRequiredPa'] for a in arm_screens),
        armMeanShearPa=web_force/hw['boxAreaM2'],
        nodeAnnulusAxialPlusFullMomentPa=ring_force/hw['node']['areaM2']+moment/hw['node']['sectionModulusM3'],
        tongueBearingRequiredPa=web_force/(.048*.024),
        tongueNetSectionRequiredPa=web_force/((.160-.049)*.024),
        tongueTwoPlaneShearOutRequiredPa=web_force/(2*(.160-.049)/2*.024),
        pinSingleShearPa=web_force/(math.pi*.040**2/4),
        pinCantileverBendingPa=web_force*LUG_ECCENTRICITY/(math.pi*.040**3/32),
        pinVonMisesTrialPa=math.hypot(web_force*LUG_ECCENTRICITY/(math.pi*.040**3/32),
            math.sqrt(3)*web_force/(math.pi*.040**2/4)),
        steelSingleLugBearingPa=web_force/(.016*.040),
        endPlateStripBendingPa=6*web_force*LUG_ECCENTRICITY/(.120*.008**2),
        webBodyEccentricMomentNm=web_force*LUG_ECCENTRICITY,
        webBondMeanShearPa=web_force/hw['webBondAreaM2'],
        webInsertWeldMeanShearPa=web_force/(.003/math.sqrt(2)*math.pi*.294),
        twoLugWeldMeanShearPa=web_force/(.006/math.sqrt(2)*.240),
        status='Single outboard lug clears the neck, but the pin and end-plate nominal eccentric screens FAIL. Composite bearing, shear-out, bond peel, weld, pin and root qualification UNKNOWN.')


def lug_clearance(xy, members):
    """Fixed-geometry interval/separating-axis proof, four symmetry classes.

    Intended pin/bush/lug bearing contacts are not treated as interferences.
    The plate/body/weld q bound is independent of their axial coordinate.
    """
    classes=[]
    for label,index in [('outer',0),('inner',N)]:
        for family in ('plus','minus'):
            m=next(v for v in members if v['family']==family and index in (v['a'],v['b']))
            direction=m['direction']*(1 if index==m['a'] else -1)
            er=xy[index]/np.linalg.norm(xy[index]); et=np.array([-er[1],er[0]])
            radial=float(direction@er); tangential=float(direction@et)
            neck_q_max=.070*abs(radial)+.080*abs(tangential)
            gaps=dict(lugToNeckAxialM=.214-.188,lugToPadAxialM=.214-.168,
                lugToLandingPlateAxialM=.214-.212,pinToPadAxialM=.170-.168,
                pinAndWashersToNeckVoidM=min(.058,.068)-.030,
                endPlateToNeckAlongWebM=.392-neck_q_max,
                weldToNeckAlongWebM=(.392-.006)-neck_q_max,
                carbonToNeckAlongWebM=.400-neck_q_max,
                oppositeFamilyLugAxialGapM=2*.214)
            assert min(gaps.values())>0
            classes.append(dict(node=label,family=family,
                directionRadialTangential=[radial,tangential],
                lugAxialIntervalAbsM=[.214,.230],neckAxialIntervalAbsM=[.168,.188],
                pinAxialIntervalAbsM=[.170,.290],washerIntervalsAbsM=[[.183,.188],[.230,.235]],
                neckProjectionMaximumQM=neck_q_max,positiveSeparations=gaps))
    return dict(method='Analytic interval/projection separation; four endpoint classes, repeated by 111 rotations and 41 planes. No search or mesh.',
        classes=classes,representedWebEnds=4*N*STATIONS,
        removedInboardLugs=4*N*STATIONS,minimumNamedSeparationM=min(min(c['positiveSeparations'].values()) for c in classes),
        status='PASS for the named neck/pad/plate/lug/pin/washer and near-end body/weld solids. Existing swept-circle tube/ring check is separate. No full-hull, deformed-geometry, tolerance or assembly-access qualification.')


def fastener(diameter,length,head_af,head_h,nut_h,washer_od,washer_id,washer_t):
    hex_area=math.sqrt(3)/2*head_af**2
    return dict(shank=math.pi*diameter**2/4*length*RHO_STEEL,
        head=hex_area*head_h*RHO_STEEL,
        nut=(hex_area-math.pi*diameter**2/4)*nut_h*RHO_STEEL,
        twoWashers=2*annulus(washer_od,washer_id,washer_t,RHO_STEEL))


def attachment(base):
    m12=fastener(.012,.060,.018,.0075,.010,.024,.013,.0025)
    m8=fastener(.008,.045,.013,.0055,.0065,.016,.0084,.0016)
    parts=dict(
        twoSplitBands=(math.pi*.173-.004)*.100*.003*RHO_STEEL,
        fourFlanges=4*(.060*.050-math.pi*.013**2/4)*.006*RHO_STEEL,
        twoM12Sets=2*sum(m12.values()),
        two8mmJaws=2*(.080*.040-2*math.pi*.009**2/4)*.008*RHO_STEEL,
        twoM8GripSets=2*sum(m8.values()),
        flangeWeld=.5*.006**2*.400*RHO_STEEL,
        jawWeld=.5*.003**2*.320*RHO_STEEL,
        lining=math.pi*.168*.100*.002*1100,
        twoPatchPlies=2*.200*.200*base['model']['wall']['filmKgM2'],
        twoPatchBonds=2*.200*.200*.0002*RHO_ADHESIVE)
    count_barrel=161*math.ceil(2*math.pi*SURFACE_R/2)
    count_cap=math.ceil(4*math.pi*SURFACE_R**2); count=count_barrel+count_cap
    demand=base['model']['unpressurised']['erectionClampN']; required=1.5*demand
    mu=.3  # Illustration only, for both interfaces; not a friction qualification.
    grip_preload=required/(2*mu)
    each_m8=grip_preload/2
    band_tension=required/(2*math.pi*mu)  # full-wrap uniform belt approximation
    jaw_stress=6*(required/2*.020)/(.080*.008**2)
    flange_stress=6*band_tension*.020/(.050*.006**2)
    weld_area_each=2*.080*.003/math.sqrt(2)
    return dict(partsKg=parts,eachKg=sum(parts.values()),barrelCount=count_barrel,
        capEquivalentCount=count_cap,totalCount=count,totalT=count*sum(parts.values())/1000,
        fastenerGeometryMassKg=dict(M12=m12,M8=m8),
        demandN=demand,requiredNominalN=required,
        jawBendingPa=jaw_stress,jawNominalScreenPass=jaw_stress<FY_STEEL,
        frictionIllustration=mu,gripContactAreaEachM2=.050*.040,
        gripTotalPreloadN=grip_preload,eachM8TensionN=each_m8,
        gripPressureRequiredPa=grip_preload/(.050*.040),
        M8AssumedRootDiameterM=.0065,
        M8DirectTensionPa=each_m8/(math.pi*.0065**2/4),
        M8DoublePryingTrialPa=2*each_m8/(math.pi*.0065**2/4),
        patchRequiredLineLoadNPerM=required/(2*.050),
        gripMeanTransferPa=required/(2*.050*.040),
        fullPatchMeanBondShearPa=required/(2*.200*.200),
        bandTensionN=band_tension,bandDirectStressPa=band_tension/(.100*.003),
        hoopUniformPreloadPressurePa=band_tension/(.100*.083),
        hoopAdditionalProjectedBearingPa=required/(.100*.166),
        eachM12TensionN=band_tension,M12AssumedRootDiameterM=.010,
        M12DoublePryingTrialPa=2*band_tension/(math.pi*.010**2/4),
        flangeBendingPa=flange_stress,flangeNominalScreenPass=flange_stress<FY_STEEL,
        jawWeldDirectShearPa=(required/2)/weld_area_each,
        jawWeldMomentNormalPa=(required/2*.020)/(weld_area_each*.008/2),
        qualifiedNominalCapacityN=None,
        status='8 mm jaw nominal bending PASS; 6 mm band flange nominal bending FAIL in the assumed friction case. Film/patch grip, bolted/welded assembly and hoop bearing UNKNOWN.')


def calculate():
    frozen=json.loads((HERE/'baseline.json').read_text())
    for path,digest in frozen['referenceFiles'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    base=frozen['case80']; prior=frozen['i011']; hw=hardware()
    close(sum(base['model']['ledgerT'].values()),base['model']['totalT'])
    trial_inputs=[dict(name='reference_hypothesis',compositeShearPa=5e9,adhesiveShearPa=1e9,extraEndComplianceMPerN=0.),
                  dict(name='soft_interface_trial',compositeShearPa=.5e9,adhesiveShearPa=.1e9,extraEndComplianceMPerN=1e-8)]
    trials=[]
    for trial in trial_inputs:
        xy,members,sections=lattice(hw,trial)
        mech=arithmetic(members,xy)
        first={f:next(m for m in members if m['family']==f) for f in ('outer','inner','plus','minus')}
        compliance={f:dict(axialNPerM=m['stiffness'],partsMPerN=m['compliancePartsMPerN'],endPartsMPerN=m['endCompliancePartsMPerN']) for f,m in first.items()}
        trials.append(dict(inputs=trial,compliance=compliance,mechanics=mech,connections=connection_screens(hw,members,mech)))
    clearance_proof=lug_clearance(xy,members)
    clamp=attachment(base)
    lengths={f:first[f]['length'] for f in first}
    counts=dict(stations=STATIONS,outerModules=N*STATIONS,innerModules=N*STATIONS,
        ringNodes=2*N*STATIONS,circumferenceSplices=2*N*STATIONS,webs=2*N*STATIONS,
        webEnds=4*N*STATIONS,integralLandings=4*N*STATIONS)
    new=dict(
        outerBaseTubeT=N*STATIONS*(lengths['outer']-GAP)*hw['ring']['kgPerM']/1000,
        innerBaseTubeT=N*STATIONS*(lengths['inner']-GAP)*hw['ring']['kgPerM']/1000,
        circumferentialSplicesT=counts['circumferenceSplices']*hw['spliceKg']/1000,
        integralNodesT=counts['ringNodes']*hw['nodeKg']/1000,
        webCarbonT=counts['webs']*((lengths['plus']-2*WEB_SETBACK)*sections['web']['kgPerM']-2*hw['carbonChamferRemovedKgEach'])/1000,
        bothWebEndsT=counts['webEnds']*hw['webEndKg']/1000,
        erectionAttachmentsT=clamp['totalT'])
    retained=prior['mass']['retainedOtherHullT']; hull=retained+sum(new.values()); gas=base['gas']['massT']
    # Independent two-route replacement identity, never delete retained caps/wall.
    old_new_bill=sum(prior['mass']['newBillT'].values())
    close(hull,prior['mass']['hullT']-old_new_bill+sum(new.values()))
    frac=STATIONS/base['model']['skeleton']['nInnerRings']
    removed=(base['model']['ledgerT']['innerRings']+base['model']['ledgerT']['thetaWebs'])*frac/.85
    close(retained,base['model']['totalT']-removed-base['model']['ledgerT']['clamps'])
    close(gas,1000*base['effectiveVolumeM3']/(287.05*288.15)/1000)
    mass=dict(retainedOtherHullT=retained,removedEntireI011NewBillT=old_new_bill,
        i011HullT=prior['mass']['hullT'],newBillT=new,hullT=hull,retainedGasT=gas,
        knownSubtotalT=hull+gas,changeFromI011T=hull-prior['mass']['hullT'],
        frameAndNodeT=sum(new.values())-clamp['totalT'],
        i011MaximumNewFrameT=prior['mass']['maximumNewFrameAndNodeT'],
        maximumNewFrameT=base['at'][0]['liftT']-gas-retained-clamp['totalT'],
        at=[dict(altitudeM=a['altitudeM'],liftT=a['liftT'],knownMarginT=a['liftT']-hull-gas) for a in base['at']],
        allUpMassT=None,allUpMarginT=None)
    # Geometric envelope checks for the first web at each ring. The swept-circle
    # tube-axis distance is conservative here; no full 3-D collision model.
    clearance=[]
    for label,radius in [('outer',OUTER_R),('inner',INNER_R)]:
        point=xy[0 if label=='outer' else N]
        target=xy[N+2] if label=='outer' else xy[2]
        e=(target-point)/np.linalg.norm(target-point)
        radial=abs(float(e@(point/np.linalg.norm(point))))
        centre_distance=math.hypot(AXIAL_LAYER,WEB_SETBACK*radial)
        clearance.append(dict(node=label,carbonToLocalRingM=centre_distance-(.155+.150),
            endPlateToLocalRingM=math.hypot(AXIAL_LAYER,.392*radial)-(.155+.160)))
    assert all(v['carbonToLocalRingM']>0 and v['endPlateToLocalRingM']>0 for v in clearance)
    assert clamp['jawNominalScreenPass'] and not clamp['flangeNominalScreenPass']
    assert mass['maximumNewFrameT']<prior['mass']['maximumNewFrameAndNodeT']<0
    assert all(a['knownMarginT']<0 for a in mass['at'])
    return dict(unit='R3-I014',baselineSha256=hashlib.sha256((HERE/'baseline.json').read_bytes()).hexdigest(),
        geometry=dict(diameterM=80,totalLengthM=160,barrelLengthM=80,columnCount=N,
            outerRingRadiusM=OUTER_R,innerRingRadiusM=INNER_R,stationPitchM=BAY,
            outerChordM=lengths['outer'],innerChordM=lengths['inner'],webPinLengthM=lengths['plus'],
            webCarbonCutM=lengths['plus']-2*WEB_SETBACK,webSetbackEachM=WEB_SETBACK,
            webInternalChamferEachM=WEB_CHAMFER,effectiveWebBondLengthM=WEB_BOND_LENGTH,
            webFamilyPlanesM=[-.2,.2],familyClearanceM=.100,midChordGapM=GAP,
            bridgeLapEachM=LAP,bridgeLengthM=2*LAP+GAP,localNodeLengthM=NODE_LENGTH,
            nodeRootFaceM=.168,neckLengthM=.020,landingPlateCentreM=.200,
            landingPlateThicknessM=.024,oneOutboardLugCentreM=.222,
            outboardLugThicknessM=.016,lugEccentricityM=LUG_ECCENTRICITY,
            loadLineLeverM=LOAD_ARM,lugToNeckClearanceM=.026,
            pinStartAbsM=.170,pinEndAbsM=.290,lugClearanceProof=clearance_proof,
            localClearanceScreens=clearance),
        counts=counts,hardware=hw,sections=sections,trials=trials,
        rotation='Zero rotational stiffness is credited by the four-coordinate axial-material diagnostic. Actual continuous-joint moment/peel/rotation transfer is UNKNOWN; each arm and the combined offset moment are explicitly demanded.',
        erectionAttachment=clamp,mass=mass,
        qualification='FAIL for represented float mass, selected 6 mm attachment flange and new single-lug eccentric pin/end-plate nominal screens; named neck/lug collision removed. Circumferential joint, integral landing, grip, global pressure stability and all-up confidence UNKNOWN.',
        nextGeometry='One cap-to-cap 80 m capsule schedule with actual variable-radius cap rings, explicit polar closure and a shared outer-frame/pressure-hoop load path. Re-derive film support and cap forces before removing any retained wall or cap mass; a local flange trial alone cannot close the negative whole-hull allowance.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    args=parser.parse_args(); result=calculate()
    if args.write:(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    elif args.check:
        compare(result,json.loads((HERE/'result.json').read_text()))
        print('I014 reproduction PASS: pinned baseline, two fixed-geometry compliance trials, energy/rigid-motion checks, priced interfaces and two-route bill. Physical qualification UNKNOWN.')
    else:print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':main()
