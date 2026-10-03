#!/usr/bin/env python3
"""Independent stationary momentum and retained-water bounds. No simulation imports.

The full-bus anchors are the payload-exchange analysis at the lake's local density.
Its full generator rating is distinct from the cycle's available nitrogen recovery.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

def thrust(power, rho, area, eta):
    return (power * 1e6 * eta * math.sqrt(2 * rho * area)) ** (2/3) / 9810

data = json.loads(subprocess.check_output(['node', 'tests/energy/hover-data.mjs'], text=True))
anchors = dict(P100=159.3, P1000=785.9, P10000=7551.7)
for row in data['modes']:
    whole = thrust(row['batteryMW'] + row['generatorRatingMW'], row['rho'], row['diskM2'], row['eta'])
    actual = thrust(max(0, row['modeBusMW'] - row['nonRotorMW']), row['rho'], row['diskM2'], row['eta'])
    assert round(whole, 1) == anchors[row['class']], (row['class'], whole)
    assert abs(whole - row['fullBusModelT']) < 1e-8
    assert abs(actual - row['modeModelT']) < 1e-8
    row.update(independentFullBusT=whole, independentModeT=actual,
               wholeBusFloorT=max(0, row['emptySurplusT'] - whole),
               modeEmptyFloorT=max(0, row['emptySurplusT'] - min(whole, actual)))
    print(f"PASS {row['class']}/{row['mode']}: full bus model/independent {row['fullBusModelT']:.3f}/{whole:.3f} t; "
          f"mode supply {row['modeBusMW']:.3f} MW, other draw {row['nonRotorMW']:.3f} MW; mode thrust {actual:.3f} t")
for row in data['profiles']:
    assert abs(row['airV']) < 1e-9 and abs(row['vz']) < 1e-9
    cap = min(thrust(row['installedMW'], row['rho'], row['diskM2'], row['eta']),
              thrust(max(0, row['busMW'] - row['nonRotorMW']), row['rho'], row['diskM2'], row['eta']))
    surplus = row['volumeM3'] * row['rho'] / 1000 - row['dryT']
    credits = {k: row[k] for k in ['newWaterT', 'nitrogenT', 'bagT', 'verticalDragT', 'aeroT'] if abs(row[k]) > 1e-9}
    floor = max(0, surplus - cap - sum(credits.values()))
    tolerance = 1e-6 * max(1, abs(surplus-row['retainedT']-row['newWaterT']-row['nitrogenT']))
    assert row['retainedT'] >= floor - tolerance, (row['class'], 'retained water below first-principles floor', row['retainedT'], floor)
    row.update(independentThrustCapT=cap, independentRetainedFloorT=floor, otherSupport=credits,
               instant='WATER_FILL at progress 0.3, stationary, before any remaining bag credit')
    print(f"PASS {row['table']} {row['class']}/{row['km']}/{row['basis']}: kept {row['retainedT']:.3f} t; "
          f"stationary floor {floor:.3f} t; other support {credits}")
if '--check' in sys.argv:
    expected = json.dumps(data, indent=2)+'\n'
    actual = Path('research/analysis/energy-crosschecks.json').read_text()
    assert actual == expected, 'research/analysis/energy-crosschecks.json:1: stationary cross-check record is stale'
if '--write' in sys.argv:
    Path('research/analysis/energy-crosschecks.json').write_text(json.dumps(data, indent=2)+'\n')
print(f"PASS independent hover and retained-water checks: {len(data['modes'])} mode rows, {len(data['profiles'])} feasible rows")
