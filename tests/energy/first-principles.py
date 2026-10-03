#!/usr/bin/env python3
"""Independent ISA and Glauert arithmetic adapted from claude-fable-5-1.

No simulation code is imported. Class constants are copied from sim/config.js;
the separate observer supplies instantaneous trajectory and allocation data.
"""
import json, math, subprocess
CLASSES = {
    'P100': dict(payload=100, volume=220000, diameter=55, length=110, disk=2500),
    'P1000': dict(payload=1000, volume=2200000, diameter=119, length=238, disk=12000),
    'P10000': dict(payload=10000, volume=22000000, diameter=256, length=512, disk=160000),
}
G, ETA, CD = 9.81, .70, .05

def density(h):
    return 1.225 * (1 - .0065*h/288.15)**(9.80665/(287.0528*.0065)-1)

def power(thrust, rho, disk, speed, axial):
    if thrust <= 0:
        return 0
    vh2=thrust/(2*rho*disk)
    lo,hi=0,math.sqrt(vh2)
    for _ in range(80):
        mid=(lo+hi)/2
        if mid*math.sqrt(speed*speed+(axial+mid)**2)>vh2: hi=mid
        else: lo=mid
    return thrust*(axial+(lo+hi)/2)/ETA/1e6

rows=json.loads(subprocess.check_output(['node','tests/energy/state-data.mjs'],text=True))
for s in rows:
    c=CLASSES[s['class']];rho=density(1000+s['alt']);v=s['airV'];vz=s['vz']
    area=c['diameter']*(c['length']-c['diameter'])+math.pi*(c['diameter']/2)**2
    surplus=c['volume']*rho/1000-c['payload']-s['water']-s['ln2']
    drag=.5*rho*area*vz*abs(vz)/(1000*G)
    o=s['owners'];unheld=surplus-o['bagT']-o['rotorT']-o['aeroT']-drag
    assert abs(unheld-s['unheldT'])<1e-7,(s['class'],'force',unheld,s['unheldT'])
    rotor=power(o['rotorT']*1000*G,rho,c['disk'],v,max(0,-vz))
    assert abs(rotor-s['draw']['rotors'])<1e-6,(s['class'],'rotor price')
    q=.5*rho*v*v
    induced=(o['aeroT']*1000*G)**2/(q*math.pi*c['diameter']**2) if q else 0
    prop=(q*CD*math.pi*(c['diameter']/2)**2+induced)*v/ETA/1e6
    assert abs(prop-s['draw']['prop'])<1e-6,(s['class'],'propulsion price')
    print(f"PASS {s['class']}/{s['km']}/{s['basis']}: independent unheld {unheld:.6f} t; rotor {rotor:.6f} MW")
print('PASS independent ISA, force balance and momentum arithmetic:',len(rows),'rows')
