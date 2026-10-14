#!/usr/bin/env python3
"""One fixed X-web design: analytic four-coordinate modes, not qualification."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
N = 111
ALPHA = 2 * math.pi / N
PRESSURE = 101325.0
SF = 1.2
SURFACE_R = 40.0
DEPTH = 60 / 13
# The 262 mm ring coupler, not just the 250 mm tube, fits inside R=40 m.
OUTER_R = SURFACE_R - 0.262 / 2
INNER_R = OUTER_R - DEPTH
BAY = 2.0
STATIONS = 41  # x=-40,-38,...,40; end stations have half tributary width.
E_CARBON = 135e9  # I008 comparison proxy, not a selected laminate allowable.
RHO_CARBON = 1600.0
E_STEEL = 200e9
RHO_STEEL = 7850.0
FY_STEEL = 355e6
RHO_ADHESIVE = 1200.0  # mass allowance; no adhesive strength is assumed.
WEB_SETBACK = 0.3  # pin to carbon tube end, at EACH end.
AXIAL_LAYER = 0.2  # +2 and -2 web families in separate axial planes.


def close(a, b, rel=1e-9, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol), (a, b)


def tube(diameter, wall, density):
    area = math.pi * (diameter**2 - (diameter - 2*wall)**2) / 4
    inertia = math.pi * (diameter**4 - (diameter - 2*wall)**4) / 64
    return dict(odM=diameter, wallM=wall, areaM2=area, inertiaM4=inertia,
                sectionModulusM3=2*inertia/diameter, kgPerM=density*area)


def lattice():
    """Physical endpoints repeated by rotation; only 4x4 matrices are formed."""
    sections = dict(ring=tube(.250, .012, RHO_CARBON),
                    web=tube(.300, .0025, RHO_CARBON))
    xy = np.array([[rad*math.cos(j*ALPHA), rad*math.sin(j*ALPHA)]
                   for rad in (OUTER_R, INNER_R) for j in range(N)])
    members = []
    for family in ('outer', 'inner', 'plus', 'minus'):
        for j in range(N):
            if family == 'outer':
                a, b = j, (j+1) % N
            elif family == 'inner':
                a, b = N+j, N+(j+1) % N
            else:
                a, b = j, N+(j+(2 if family == 'plus' else -2)) % N
            delta = xy[b] - xy[a]
            length = float(np.linalg.norm(delta))
            is_web = family in ('plus', 'minus')
            section = sections['web' if is_web else 'ring']
            carbon_length = length - 2*WEB_SETBACK if is_web else length
            # Two end springs; numerical hypotheses, NOT measured bond stiffness.
            end_k = 1e8 if is_web else 1e9
            axial_k = 1 / (carbon_length/(E_CARBON*section['areaM2']) + 2/end_k)
            members.append(dict(family=family, a=a, b=b, length=length,
                                carbonLength=carbon_length, direction=delta/length,
                                stiffness=axial_k, endStiffness=end_k,
                                section=section))
    return xy, members, sections


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
        amplified = weight_moment/(1-compression/euler) if compression < euler else None
        interaction = (compression/(section['areaM2']*local) +
                       amplified/(section['sectionModulusM3']*local)) if amplified else None
        forces[family] = force
        screens[family] = dict(pinLengthM=length, carbonCutLengthM=member['carbonLength'],
            compressionN=compression, eulerN=euler, localProxyPa=local,
            directStressPa=compression/section['areaM2'], gravityMomentNm=weight_moment,
            amplifiedGravityMomentNm=amplified, interaction=interaction,
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


def hardware():
    """Dimensioned custom hardware mass; both ends counted, no catalogue rating."""
    ring_cuff = tube(.262, .005, RHO_STEEL)
    web_insert = tube(.294, .003, RHO_STEEL)
    cross_area = .120**2-.104**2
    cross_i = (.120**4-.104**4)/12
    pin_volume = math.pi*.040**2/4*.120
    washer_volume = 2*math.pi*(.060**2-.042**2)/4*.005
    # Two clevis lugs; two 40 mm holes are subtracted from the finished mass.
    lug_volume = 2*(.320*.120*.016 - math.pi*.040**2/4*.016)
    end = dict(insert=web_insert['kgPerM']*.300,
               endPlate=math.pi*.320**2/4*.008*RHO_STEEL,
               clevisLugs=lug_volume*RHO_STEEL,
               pin=pin_volume*RHO_STEEL, washers=washer_volume*RHO_STEEL,
               retainers=.020,
               bond=math.pi*.294*.300*.0005*RHO_ADHESIVE)
    node = dict(twoMiteredHalfCuffs=ring_cuff['kgPerM']*.300,
                cuffBond=math.pi*.250*.300*.001*RHO_ADHESIVE,
                crossarm=cross_area*.600*RHO_STEEL,
                weld=.5*.006**2*.480*RHO_STEEL)
    return dict(webEndKg=end, webEndTotalKg=sum(end.values()),
                nodeKg=node, nodeTotalKg=sum(node.values()), ringCuff=ring_cuff,
                crossarmAreaM2=cross_area, crossarmIM4=cross_i,
                crossarmZM3=cross_i/.060,
                ringEndBondAreaM2=math.pi*.250*.150,
                webEndBondAreaM2=math.pi*.294*.300,
                pinDoubleShearAreaM2=2*math.pi*.040**2/4,
                lugBearingAreaM2=2*.016*.040)


def attachment(baseline):
    """A complete priced custom saddle; keep unproved grip/interface capacity open."""
    # Two 3 mm semicircular bands around a 166 mm hoop plus 2 mm lining.
    parts = dict(band=math.pi*.173*.100*.003*RHO_STEEL,
        flanges=2*(.060*.050*.006-math.pi*.013**2/4*.006)*RHO_STEEL,
        twoM12Shanks=2*math.pi*.012**2/4*.060*RHO_STEEL,
        nutsHeadsWashers=.120, twoJaws=2*.080*.040*.003*RHO_STEEL,
        lining=math.pi*.168*.100*.002*1100,
        twoPatchPlies=2*.200*.200*baseline['model']['wall']['filmKgM2'])
    # Discrete barrel schedule; caps retain an explicit equivalent-area count.
    barrel_count = 161*math.ceil(2*math.pi*SURFACE_R/2)
    cap_equivalent = math.ceil(4*math.pi*SURFACE_R**2)
    count = barrel_count+cap_equivalent
    demand = baseline['model']['unpressurised']['erectionClampN']
    nominal = 1.5*demand
    return dict(partsKg=parts, eachKg=sum(parts.values()), barrelCount=barrel_count,
        capEquivalentCount=cap_equivalent, totalCount=count,
        totalT=count*sum(parts.values())/1000, sameConventionDemandN=demand,
        requiredNominalN=nominal, strapTensionAreaM2=2*.100*.003,
        strapYieldScreenN=2*.100*.003*FY_STEEL,
        twoBoltShearScreenN=2*math.pi*.012**2/4*FY_STEEL/math.sqrt(3),
        twoJawCantileverStressPa=6*(nominal/2*.020)/(.080*.003**2),
        bandBearingThresholdPa=nominal/(.100*.166),
        twoLapMeanShearThresholdPa=nominal/(2*.080*.040),
        qualifiedNominalCapacityN=None,
        status='FAIL retained: 3 mm jaw bending fails the nominal steel screen; film grip, bolt grade, hoop bearing and patch/bond transfer are also unqualified.')


def calculate():
    base = json.loads((HERE/'baseline.json').read_text())['case80']
    close(sum(base['model']['ledgerT'].values()), base['model']['totalT'])
    close(base['gas']['massT'], 1000*base['effectiveVolumeM3']/(287.05*288.15)/1000)
    xy, members, sections = lattice()
    mechanics = arithmetic(members, xy)
    hw = hardware()
    clamp = attachment(base)
    lengths = {family: next(m['length'] for m in members if m['family']==family)
               for family in ('outer', 'inner', 'plus', 'minus')}
    close(lengths['outer'], 2*OUTER_R*math.sin(ALPHA/2))
    close(lengths['inner'], 2*INNER_R*math.sin(ALPHA/2))
    close(lengths['plus'], math.sqrt(OUTER_R**2+INNER_R**2-2*OUTER_R*INNER_R*math.cos(2*ALPHA)))
    counts = dict(stations=STATIONS, outerSegments=N*STATIONS, innerSegments=N*STATIONS,
                  webs=2*N*STATIONS, webEnds=4*N*STATIONS, ringNodes=2*N*STATIONS)
    new = dict(outerRingT=counts['outerSegments']*lengths['outer']*sections['ring']['kgPerM']/1000,
        innerRingT=counts['innerSegments']*lengths['inner']*sections['ring']['kgPerM']/1000,
        webTubeT=counts['webs']*(lengths['plus']-2*WEB_SETBACK)*sections['web']['kgPerM']/1000,
        webEndHardwareT=counts['webEnds']*hw['webEndTotalKg']/1000,
        ringNodeHardwareT=counts['ringNodes']*hw['nodeTotalKg']/1000,
        newAttachmentsT=clamp['totalT'])
    # Only 41 of the 104 provisional maximum-circumference inner/theta stations
    # are replaced. Existing outer wall hoops, caps and other components remain.
    frac = STATIONS/base['model']['skeleton']['nInnerRings']
    old_family = base['model']['ledgerT']['innerRings']+base['model']['ledgerT']['thetaWebs']
    removed_members = frac*old_family  # already includes the old 5% addition
    removed_joints = removed_members*(1/.85-1)
    removed_clamps = base['model']['ledgerT']['clamps']
    retained = base['model']['totalT']-removed_members-removed_joints-removed_clamps
    hull = retained+sum(new.values())
    subtotal = hull+base['gas']['massT']
    at = [dict(altitudeM=a['altitudeM'], liftT=a['liftT'],
               knownMarginT=a['liftT']-subtotal, baselineMarginT=a['knownSubtotalMarginT'])
          for a in base['at']]
    forces = mechanics['axialForcesAtFactoredPressureN']
    ring_force = max(abs(forces['outer']), abs(forces['inner']))
    web_force = max(abs(forces['plus']), abs(forces['minus']))
    connection = dict(ringForceN=ring_force, ringCuffYieldScreenN=hw['ringCuff']['areaM2']*FY_STEEL,
        ringCuffRequiredYieldPa=ring_force/hw['ringCuff']['areaM2'],
        ringBondRequiredMeanShearPa=ring_force/hw['ringEndBondAreaM2'],
        webForceN=web_force, webBondRequiredMeanShearPa=web_force/hw['webEndBondAreaM2'],
        pinDoubleShearScreenN=hw['pinDoubleShearAreaM2']*FY_STEEL/math.sqrt(3),
        lugBearingScreenN=hw['lugBearingAreaM2']*FY_STEEL,
        oneCrossarmMomentNm=web_force*AXIAL_LAYER,
        crossarmYieldMomentNm=hw['crossarmZM3']*FY_STEEL,
        status='FAIL: ring cuff axial yield screen. Other checks are conditional, and actual bond/end stiffness is UNKNOWN.')
    assert connection['ringCuffYieldScreenN'] < ring_force
    assert clamp['twoJawCantileverStressPa'] > FY_STEEL
    assert all(a['knownMarginT'] < 0 for a in at)
    return dict(unit='R3-I011', baselineSha256=hashlib.sha256((HERE/'baseline.json').read_bytes()).hexdigest(),
        geometry=dict(pressureSurfaceDiameterM=80, totalLengthM=160, barrelLengthM=80,
            centrelineDepthM=DEPTH, outerFrameRadiusM=OUTER_R, innerFrameRadiusM=INNER_R,
            columnCount=N, indexOffset=2, angleRad=2*ALPHA, webPinLengthM=lengths['plus'],
            webCarbonCutM=lengths['plus']-2*WEB_SETBACK, axialFamilyPlanesM=[-.2,.2],
            familyClearanceM=2*AXIAL_LAYER-sections['web']['odM'],
            oldNominalEndpointLengthM=math.sqrt(40**2+(40-DEPTH)**2-2*40*(40-DEPTH)*math.cos(2*ALPHA))),
        sections=sections, counts=counts, mechanics=mechanics, hardware=hw,
        connectionScreens=connection, erectionAttachment=clamp,
        mass=dict(baselineHullT=base['model']['totalT'], replacedStationFraction=frac,
            removedInnerThetaMembersT=removed_members, removedAttributedJointsT=removed_joints,
            removedOldClampsT=removed_clamps, retainedOtherHullT=retained,
            newBillT=new, hullT=hull, retainedGasT=base['gas']['massT'], knownSubtotalT=subtotal,
            at=at, fullOldFamilyIncludingJointsT=old_family/.85,
            baselineWholeFamilyBalanceLimitT=old_family/.85+base['at'][0]['knownSubtotalMarginT'],
            newFrameAndNodeT=sum(new.values())-new['newAttachmentsT'],
            maximumNewFrameAndNodeT=base['at'][0]['liftT']-base['gas']['massT']-retained-new['newAttachmentsT'],
            allUpMassT=None, allUpMarginT=None),
        qualification='FAIL for represented mass, ring-cuff load transfer and erection jaw; global stability and all-up physical confidence UNKNOWN.',
        nextGeometry='Retain the 80 m envelope for one continuous-ring/locally thickened node concept to remove the failed sleeve splice; replace the jaw with an 8 mm plate only as a new untested sizing trial. Re-derive stiffness, mass and interface load transfer before credit.')


def compare(a, b):
    if isinstance(a, dict):
        assert a.keys()==b.keys()
        for key in a: compare(a[key], b[key])
    elif isinstance(a, list):
        assert len(a)==len(b)
        for x, y in zip(a,b): compare(x,y)
    elif isinstance(a, float): close(a,b,rel=1e-8,abs_tol=1e-7)
    else: assert a==b, (a,b)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    args=parser.parse_args(); result=calculate()
    if args.write:
        (HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    elif args.check:
        compare(result,json.loads((HERE/'result.json').read_text()))
        print('I011 reproduction PASS: exact endpoints/counts, four-coordinate energy, rigid motions, mass replacement and failure screens. Physical qualification UNKNOWN.')
    else: print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__': main()
