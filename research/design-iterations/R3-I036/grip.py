"""R3-I036 calculator: six-segment titanium wedge cord grip in a matching aluminium cone.

Implements the frozen construction once from baseline.json (saved accepted data plus the
adopted freeze). Exact solid geometry and closed-form polynomial integrals only; stdlib
only; no ancestor import, solver, search, render or alternate validation invocation.
Contract: python3 -I -B research/design-iterations/R3-I036/grip.py --write
"""
import hashlib
import json
import math
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
RHO_TI = None
RHO_AL = None


def annulus_piece(z0, z1, ro0, ro1, ri0, ri1):
    """Volume and z-moment (mm^4 basis: V in mm^3, Mz in mm^4) of an annulus with linearly
    interpolated outer/inner radii over z in [z0, z1]. Exact closed form."""
    span = z1 - z0
    so = (ro1 - ro0) / span
    si = (ri1 - ri0) / span

    def i0(r0, s):
        return r0 * r0 * span + r0 * s * span * span + s * s * span ** 3 / 3.0

    def i1(r0, s):
        return r0 * r0 * span ** 2 / 2.0 + 2.0 * r0 * s * span ** 3 / 3.0 + s * s * span ** 4 / 4.0

    v = math.pi * (i0(ro0, so) - i0(ri0, si))
    mz = math.pi * (z0 * (i0(ro0, so) - i0(ri0, si)) + (i1(ro0, so) - i1(ri0, si)))
    return v, mz


def hex_area(af):
    return math.sqrt(3.0) / 2.0 * af * af


def prism(z0, z1, area):
    """Constant-section prism: V, Mz."""
    return area * (z1 - z0), area * (z1 * z1 - z0 * z0) / 2.0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def family_calc(fam, geo, saved, rm):
    """One family: geometry, stacks, masses, centres, screens. All mm/kg unless named."""
    D = geo['cordDiaMm']
    L = geo['gripLenMm']
    t0 = geo['wedgeRadialThicknessAtExitMm']
    od = geo['bodyOdMm']
    H = geo['chamberLenMm']
    fl_od = geo['flangeOdMm']
    fl_t = geo['flangeThkMm']
    cap_od = geo['capOdMm']
    cap_t = geo['capThkMm']
    rb = geo['capBoltCircleDiaMm'] / 2.0
    bolt_nom = geo['capBoltNominalMm']
    bolt_clr = geo['capBoltClearanceDiaMm']
    wti = geo['capBoltWasher']
    nut_af = geo['capBoltNutHexAfMm']
    nut_h = geo['capBoltNutHexHMm']
    head_af = geo['capBoltHeadHexAfMm']
    head_h = geo['capBoltHeadHexHMm']
    tip_b = geo['capBoltTipMm']
    stud = geo['studNominalMm']
    stud_bore = geo['studBoreDiaMm']
    N = geo['interiorNutHeightMm']
    sw = geo['studWasher']
    plate_od = geo['receiverPlateOdMm']
    plate_t = geo['receiverPlateThkMm']
    plate_clr = geo['receiverPlateClearanceDiaMm']
    plate_gap = geo['receiverFrontBeyondCapRearMm']
    tip_s = geo['studTipProjectionMm']
    iso = 0.5

    alpha = math.radians(5.0)
    k = math.tan(alpha)
    rc = D / 2.0
    r_out0 = rc + t0
    r_out_l = r_out0 + L * k
    z_fl_front = L + H
    z_fl_rear = z_fl_front + fl_t
    cap_front = z_fl_rear + iso
    cap_rear = cap_front + cap_t
    nut_front = cap_front - iso - sw['thkMm'] - N
    stud_front = nut_front - tip_s
    z_p = cap_rear + plate_gap
    plate = (z_p, z_p + plate_t)
    front_w = (z_p - sw['thkMm'], z_p)
    front_nut = (z_p - sw['thkMm'] - N, z_p - sw['thkMm'])
    rear_w = (plate[1], plate[1] + sw['thkMm'])
    rear_nut = (rear_w[1], rear_w[1] + N)
    stud_rear = rear_nut[1] + tip_s
    stud_len = stud_rear - stud_front
    under_head = 2.0 * wti['thkMm'] + 2.0 * iso + fl_t + iso + cap_t + nut_h + tip_b
    head_seat = z_fl_front - iso - wti['thkMm']
    head = (head_seat - head_h, head_seat)
    hw_ti = (head_seat, head_seat + wti['thkMm'])
    hw_iso = (z_fl_front - iso, z_fl_front)
    nw_iso = (cap_rear, cap_rear + iso)
    nw_ti = (nw_iso[1], nw_iso[1] + wti['thkMm'])
    cb_nut = (nw_ti[1], nw_ti[1] + nut_h)
    cb_tip = (cb_nut[1], cb_nut[1] + tip_b)
    seat_inner = rb - wti['odMm'] / 2.0
    seat_outer = rb + wti['odMm'] / 2.0
    seat_ok = seat_inner > r_out_l and seat_outer < fl_od / 2.0
    if not close(cb_tip[1] - head_seat, under_head):
        raise SystemExit('stack identity mismatch: cap bolt under-head length')

    declared = rm['axialStackDeclaration'][fam]
    derived = {
        'wedges': [0.0, L], 'bodyConstantOd': [0.0, z_fl_front], 'bodyFlange': [z_fl_front, z_fl_rear],
        'flangeCapIsoLayer': [z_fl_rear, cap_front], 'capActual': [cap_front, cap_rear],
        'studWasherInterior': [cap_front - iso - sw['thkMm'], cap_front - iso], 'interiorNut': [nut_front, nut_front + N],
        'studTip': [stud_front, stud_front + tip_s], 'studFront': stud_front, 'capRearActual': cap_rear,
        'receiverPlate': [plate[0], plate[1]], 'frontPlateWasher': [front_w[0], front_w[1]],
        'frontPlateNut': [front_nut[0], front_nut[1]], 'rearPlateWasher': [rear_w[0], rear_w[1]],
        'rearPlateNut': [rear_nut[0], rear_nut[1]], 'studRear': stud_rear, 'studBlankLengthMm': stud_len,
        'capBoltHead': [head[0], head[1]], 'capBoltHeadSideTiWasher': [hw_ti[0], hw_ti[1]],
        'capBoltHeadSideIsoWasher': [hw_iso[0], hw_iso[1]], 'capBoltNutSideIsoWasher': [nw_iso[0], nw_iso[1]],
        'capBoltNutSideTiWasher': [nw_ti[0], nw_ti[1]], 'capBoltNut': [cb_nut[0], cb_nut[1]],
        'capBoltTip': [cb_tip[0], cb_tip[1]], 'capBoltLengthUnderHeadMm': under_head,
    }
    for key, val in derived.items():
        if key in declared:
            dec = declared[key]
            ok = (close(val[0], dec[0]) and close(val[1], dec[1])) if isinstance(val, list) else close(val, dec)
            if not ok:
                raise SystemExit('input identity mismatch at %s/%s: derived %r declared %r' % (fam, key, val, dec))

    # --- solids (mm^3) and centroids (mm) ---
    az = (58.0 / 360.0)
    wed_v_full = math.pi * ((r_out_l ** 3 - r_out0 ** 3) / (3.0 * k) - rc * rc * L)
    a = r_out0
    wed_mz_full = math.pi * (a * a * L * L / 2.0 + 2.0 * a * k * L ** 3 / 3.0 + k * k * L ** 4 / 4.0 - rc * rc * L * L / 2.0)
    wed_v = 6.0 * az * wed_v_full
    wed_mz = 6.0 * az * wed_mz_full
    v_body, mz_body = annulus_piece(0.0, L, od / 2.0, od / 2.0, r_out0, r_out_l)
    vb, mb = annulus_piece(L, z_fl_front, od / 2.0, od / 2.0, r_out_l, r_out_l)
    v_body += vb
    mz_body += mb
    vb, mb = annulus_piece(z_fl_front, z_fl_rear, fl_od / 2.0, fl_od / 2.0, r_out_l, r_out_l)
    v_body += vb
    mz_body += mb
    hole_area = math.pi / 4.0 * bolt_clr * bolt_clr
    vh, mh = prism(z_fl_front, z_fl_rear, 4.0 * hole_area)
    v_body -= vh
    mz_body -= mh
    v_cap, mz_cap = prism(cap_front, cap_rear, math.pi / 4.0 * (cap_od * cap_od - stud_bore * stud_bore) - 4.0 * hole_area)
    shank_v = math.pi / 4.0 * bolt_nom * bolt_nom * under_head
    head_v = hex_area(head_af) * head_h
    bolt_v = 4.0 * (shank_v + head_v)
    bolt_mz = 4.0 * ((head_seat + under_head / 2.0) * shank_v + (head[0] + head_h / 2.0) * head_v)
    nut_v = 4.0 * (hex_area(nut_af) - math.pi / 4.0 * bolt_nom * bolt_nom) * nut_h
    nut_mz = nut_v * (cb_nut[0] + nut_h / 2.0)
    cw_v = 8.0 * math.pi / 4.0 * (wti['odMm'] ** 2 - wti['idMm'] ** 2) * wti['thkMm']
    cw_mz = 8.0 * math.pi / 4.0 * (wti['odMm'] ** 2 - wti['idMm'] ** 2) * wti['thkMm'] * ((hw_ti[0] + hw_ti[1] + nw_ti[0] + nw_ti[1]) / 4.0)
    stud_v = math.pi / 4.0 * stud * stud * stud_len
    stud_mz = stud_v * (stud_front + stud_rear) / 2.0
    stud_af = 1.6 * stud
    snut_v1 = (hex_area(stud_af) - math.pi / 4.0 * stud * stud) * N
    snut_v = 3.0 * snut_v1
    snut_mz = snut_v1 * (nut_front + N / 2.0 + front_nut[0] + N / 2.0 + rear_nut[0] + N / 2.0)
    swash_v1 = math.pi / 4.0 * (sw['odMm'] ** 2 - sw['idMm'] ** 2) * sw['thkMm']
    swash_v = 3.0 * swash_v1
    swash_mz = swash_v1 * (front_w[0] + sw['thkMm'] / 2.0 + rear_w[0] + sw['thkMm'] / 2.0
                           + cap_front - iso - sw['thkMm'] / 2.0)
    plate_v = math.pi / 4.0 * (plate_od * plate_od - plate_clr * plate_clr) * plate_t
    plate_mz = plate_v * (plate[0] + plate_t / 2.0)
    iso_layer_area = math.pi / 4.0 * (fl_od * fl_od - (2.0 * r_out_l) ** 2) - 4.0 * hole_area
    iso_layer_v = iso_layer_area * iso

    kg = lambda v, rho: v * 1e-9 * rho
    rows = [
        ('wedgeSet6', wed_v, RHO_TI, wed_mz, 'six Ti conical-shell sectors, azimuth 58 deg each, z in [0,L]'),
        ('bodyAl', v_body, RHO_AL, mz_body, 'Al constant-OD cylinder + conical bore + chamber bore + integral flange, minus four bolt holes'),
        ('capAl', v_cap, RHO_AL, mz_cap, 'Al cap cylinder minus four bolt holes and central stud bore'),
        ('capBolts4', bolt_v, RHO_TI, bolt_mz, 'four Ti blanks at under-head length plus separate hex head stock'),
        ('capNuts4', nut_v, RHO_TI, nut_mz, 'four Ti hex nuts minus bore'),
        ('capWashers8', cw_v, RHO_TI, cw_mz, 'eight Ti washers, two per bolt'),
        ('studBlank', stud_v, RHO_TI, stud_mz, 'one Ti fully threaded blank spanning declared front/rear endpoints'),
        ('studNuts3', snut_v, RHO_TI, snut_mz, 'interior + two receiver Ti hex nuts at assumed across-flats 1.6x nominal'),
        ('studWashers3', swash_v, RHO_TI, swash_mz, 'three Ti bearing washers (interior + both plate faces)'),
        ('receiverPlate', plate_v, RHO_TI, plate_mz, 'one Ti receiver plate annulus at central clearance'),
    ]
    masses = {}
    centres = {}
    total_kg = 0.0
    for name, v, rho, mz, desc in rows:
        m = kg(v, rho)
        masses[name] = dict(kgPerEnd=m, volumeMm3=v, material='Ti' if rho == RHO_TI else 'Al', role=desc)
        centres[name] = dict(zMm=mz / v, definition='mass centroid of its own priced solid')
        total_kg += m
    machining = 0.03 * (masses['bodyAl']['kgPerEnd'] + masses['capAl']['kgPerEnd'])
    lump = rm['pricedStockAssumptions']['newLumpKgPerEnd'][fam]
    assembly_centre_z = sum(centres[n]['zMm'] * masses[n]['kgPerEnd'] for n in masses) / total_kg

    # --- cord identity ---
    embedded_declared = rm['cordIdentity']['embeddedPerEndM'][fam]
    recorded_implied = (saved['meanCordM'] - saved['lFreeMeanM']) / 2.0
    identity_ok = close(embedded_declared, recorded_implied, rm['cordIdentity']['toleranceM'])

    # --- screens (conditional model outputs, not proofs) ---
    T = saved['TfitkN'] * 1000.0
    N_cone = T / math.sin(alpha)
    a_in = az * math.pi * D * L
    a_out = az * math.pi * (r_out0 + r_out_l) * (L / math.cos(alpha))
    p_in = N_cone * math.cos(alpha) / (6.0 * a_in)
    p_out = N_cone / (6.0 * a_out)
    hoop = p_out * r_out_l / (od / 2.0 - r_out_l)
    r_w = sw['odMm'] / 2.0
    cap_bend = 6.0 * T * (rb - r_w) / (2.0 * math.pi * r_w * cap_t * cap_t)
    stud_ten = T / (math.pi / 4.0 * stud * stud)
    plate_bear = T / (math.pi / 4.0 * (sw['odMm'] ** 2 - sw['idMm'] ** 2))
    iso_comp = T / iso_layer_area
    screens = {
        'loadN': {'fittingDemandN': T, 'setPointT0N': saved['T0kN'] * 1000.0, 'basis': 'carried independently from accepted saved values'},
        'coneNormalTotalN': N_cone, 'perSegmentN': N_cone / 6.0,
        'requiredCordFaceFrictionCoefficient': k,
        'contactPressuresMPa': {'cordFaceMean': p_in, 'coneFaceMean': p_out,
                                'verdict': 'cord crushing/fibre damage UNKNOWN; available friction UNKNOWN'},
        'bodyHoopMPa': {'value': hoop, 'utilisationVs150': hoop / 150.0,
                        'model': 'nominal thin-wall screen at the chamber-entrance plane, mean cone-face pressure at the cone big-end radius'},
        'capBendingMPa': {'value': cap_bend, 'utilisationVs150': cap_bend / 150.0,
                          'model': 'radial-strip upper-bound screen, known-conservative, not a plate solution'},
        'studTensionMPa': {'value': stud_ten, 'utilisationVs880': stud_ten / 880.0, 'threadRootUNKNOWN': True},
        'plateBearingMPa': {'value': plate_bear, 'utilisationVs880': plate_bear / 880.0,
                            'transfer': 'plate/anchor transfer UNSIZED/UNKNOWN'},
        'isoLayerCompressionMPa': {'value': iso_comp, 'occupancyVolumeMm3': iso_layer_v, 'mass': 'covered by the lump'},
        'status': 'CONDITIONAL dimensional elastic metal screens only; no proof; compliance and take-up UNKNOWN',
    }

    stacks = {key: val for key, val in derived.items()}
    stacks['capBoltSeatCheck'] = {'headWasherAnnulusMm': [seat_inner, seat_outer],
                                  'flangeMaterialSpanMm': [r_out_l, fl_od / 2.0], 'within': seat_ok}
    geometry = {'coneRadialK': k, 'rcMm': rc, 'rOut0Mm': r_out0, 'rOutLMm': r_out_l,
                'chamberBoreDiaMm': 2.0 * r_out_l, 'zFlangeFrontMm': z_fl_front, 'zFlangeRearMm': z_fl_rear,
                'capActualFrontMm': cap_front, 'capActualRearMm': cap_rear, 'zReceiverFrontMm': z_p,
                'studSpanMm': [stud_front, stud_rear]}
    return dict(geometry=geometry, stacks=stacks, masses=masses, centres=centres,
                newHardwareKgPerEnd=total_kg, machiningKgPerEnd=machining, lumpKgPerEnd=lump,
                assemblyCentreZMm=assembly_centre_z,
                cordIdentity={'embeddedPerEndM': embedded_declared, 'recordedImpliedPerEndM': recorded_implied,
                              'consistent': identity_ok,
                              'statement': 'recorded datum already carries 2x(L+8mm) embedded cord per cord; no extra run, no unrecorded length increase'
                              if identity_ok else 'DATUM MISMATCH — do not report totals'},
                screens=screens)


def main():
    if sys.argv[1:] != ['--write']:
        print('usage: grip.py --write (frozen contract; no other invocation)', file=sys.stderr)
        raise SystemExit(2)
    print('SCIENCE_STARTED', flush=True)
    base = json.loads((U / 'baseline.json').read_text())
    global RHO_TI, RHO_AL
    RHO_TI = base['materials']['titanium']['rhoKgM3']
    RHO_AL = base['materials']['aluminium']['rhoKgM3']
    out = {'unit': 'R3-I036', 'contract': 'python3 -I -B research/design-iterations/R3-I036/grip.py --write',
           'inputs': {p: hashlib.sha256((U / p).read_bytes()).hexdigest() for p in ('baseline.json', 'sources.json')}}
    fams = {}
    ledger_new_t = 0.0
    ledger_removed_t = 0.0
    removed_ok = True
    for fam in ('d60', 'd180/11'):
        calc = family_calc(fam, base['i036GeometryMm'][fam], base['i028Saved']['families'][fam], base)
        ends = base['i028Saved']['families'][fam]['ends']
        rc = base['ledgerRules']['removalCandidatesConditionalOnly'][fam]
        removed_kg = rc['acceptedBodyKgPerEndAl'] + rc['machiningRowKgPerEnd'] + rc['resinPotKgPerEnd'] + rc['replacedStudKgPerEnd']
        calc['ledger'] = {
            'ends': ends,
            'newHardwareKgPerEnd': calc['newHardwareKgPerEnd'],
            'machiningKgPerEnd': calc['machiningKgPerEnd'],
            'lumpKgPerEnd': calc['lumpKgPerEnd'],
            'removedConditionalKgPerEnd': removed_kg,
            'removedRows': rc,
            'newHardwareT': calc['newHardwareKgPerEnd'] * ends / 1000.0,
            'machiningT': calc['machiningKgPerEnd'] * ends / 1000.0,
            'lumpT': calc['lumpKgPerEnd'] * ends / 1000.0,
            'removedConditionalT': removed_kg * ends / 1000.0,
        }
        ledger_new_t += calc['ledger']['newHardwareT'] + calc['ledger']['machiningT'] + calc['ledger']['lumpT']
        ledger_removed_t += calc['ledger']['removedConditionalT']
        fams[fam] = calc
    mach_check = sum(base['ledgerRules']['removalCandidatesConditionalOnly'][f]['machiningRowKgPerEnd']
                     * base['i028Saved']['families'][f]['ends'] for f in ('d60', 'd180/11')) / 1000.0
    if not close(mach_check, base['i028Saved']['acceptedVehicleT']['machiningStockT'], 1e-9):
        removed_ok = False
    veh = base['i028Saved']['acceptedVehicleT']

    def bill(removed_t):
        delta_hw = ledger_new_t - removed_t
        assembly = 0.05 * delta_hw
        d_total = delta_hw + assembly
        sockets = veh['socketsT'] + delta_hw
        assembly_line = veh['assemblyT'] + assembly
        total = veh['totalT'] + d_total
        spokes = veh['spokesLineT'] + d_total
        msl = veh['marginSLT'] - d_total
        m2500 = veh['margin2500T'] - d_total
        x15_inc = 0.5 * (sockets + veh['anchorBlocksT'] + veh['doublerPadsT'] + veh['attachmentBoltsT']) * 1.05
        return {'deltaHardwareT': delta_hw, 'assemblyShareOnIncrementT': assembly, 'totalDeltaT': d_total,
                'socketsTNew': sockets, 'assemblyTNew': assembly_line, 'totalTNew': total,
                'spokesLineTNew': spokes, 'marginSLTNew': msl, 'margin2500TNew': m2500,
                'x15Scenario': {'candidateX15IncrementT': x15_inc, 'candidateX15SLMarginT': msl - x15_inc,
                                'inheritedX15IncrementT_stored': veh['inheritedX15IncrementT_stored']}}

    bills = {'conditionalSubstitution': bill(ledger_removed_t), 'zeroQualifiedRetirement': bill(0.0)}
    fams['ledgerTotals'] = {'newStockT': ledger_new_t, 'removedConditionalT': ledger_removed_t,
                            'machiningRowReconciliation': {'computedT': mach_check,
                                                           'acceptedT': veh['machiningStockT'], 'equal': removed_ok}}
    out['families'] = fams
    out['bills'] = bills
    cs = bills['conditionalSubstitution']
    zq = bills['zeroQualifiedRetirement']
    out['verdicts'] = {
        'conditionalSubstitution': 'sea-level margin moves %+0.2f t to %+0.2f t (%s); altitude 2500 m margin %+0.2f t (%s)'
        % (cs['marginSLTNew'] - veh['marginSLT'], cs['marginSLTNew'],
           'CONDITIONAL FAIL' if cs['marginSLTNew'] < 0 else 'conditional pass on the assumed record',
           cs['margin2500TNew'], 'FAIL'),
        'zeroQualifiedRetirement': 'sea-level margin %+0.2f t; altitude %+0.2f t' % (zq['marginSLTNew'], zq['margin2500TNew']),
        'sf12': 'substitution into the separate construction UNKNOWN; the nominal mass delta is not its result',
        'compliance': 'chain compliance/take-up UNKNOWN; I028 n=5 packets carried unchanged as labelled comparators',
        'weakestAssumptions': 'direct cord contact/slip/creep and transfer into the retained receiver',
        'physicalFloat': 'none demonstrated; all prior engineering failures/unknowns remain',
    }
    (U / 'grip.json').write_text(json.dumps(out, indent=1) + '\n')
    print('SCIENCE_COMPLETED', flush=True)
    print(json.dumps({'marginSLT_conditional': cs['marginSLTNew'], 'marginSLT_zeroRetirement': zq['marginSLTNew'],
                      'deltaHardwareT_conditional': cs['deltaHardwareT']}), flush=True)


if __name__ == '__main__':
    main()
