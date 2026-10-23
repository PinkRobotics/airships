#!/usr/bin/env python3
"""Conditional hydrostatic weather profiles anchored at 500 geopotential metres."""
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
IN = json.loads((ROOT / "INPUTS.json").read_text())
R = IN["case"]["radius_m"]
P0 = IN["case"]["p0_Pa"]
L0 = IN["case"]["lift0_kg"]
T0 = IN["case"]["T0_K"]
V0 = 4 * math.pi * R**3 / 3
A0 = 4 * math.pi * R**2
RD, G, LAPSE = 287.053, 9.80665, .0065


def make_days():
    days = [dict(id="ISA", group="baseline", dT_K=0., dp_fraction=0., e500_Pa=0.)]
    for group, inp in IN["weather"].items():
        dt, dp, vap = inp["temperature_rise_K"], inp["pressure_swing_fraction"], inp["water_vapour_Pa"]
        days.append(dict(id=f"{group}_heat_only", group=group, dT_K=dt,
                         dp_fraction=0., e500_Pa=0.))
        for sign in [-1, 1]:
            for e in [0., vap]:
                days.append(dict(id=f"{group}_hot_{'low' if sign<0 else 'high'}_{'wet' if e else 'dry'}",
                                 group=group, dT_K=dt, dp_fraction=sign*dp, e500_Pa=e))
            days.append(dict(id=f"{group}_pressure_only_{'low' if sign<0 else 'high'}",
                             group=group, dT_K=0., dp_fraction=sign*dp, e500_Pa=0.))
    for day in days:
        day["T500_K"] = T0 + day["dT_K"]
        day["p500_Pa"] = P0 * (1 + day["dp_fraction"])
        day["k"] = 1 - .378 * day["e500_Pa"] / day["p500_Pa"]
        day["rho500_kg_m3"] = day["k"] * day["p500_Pa"] / (RD * day["T500_K"])
        day["n"] = G * day["k"] / (RD * LAPSE)
    return days


DAYS = make_days()


def selected(envelope):
    return [d for d in DAYS if d["group"] == "baseline"
            or envelope == "all_019" or d["group"] == envelope]


def saturation_e(T):
    c = np.asarray(T) - 273.15
    return 611. * 10**(7.5*c/(237.3+c))


def profile(z, day, model="lapse_mixing"):
    """p,rho,T,e. Extension below sea level is mathematical, not flight space."""
    t = day["T500_K"] - LAPSE * (np.asarray(z)-500)
    if model == "isothermal":
        t = np.ones_like(np.asarray(z, dtype=float)) * day["T500_K"]
        p = day["p500_Pa"] * np.exp(-G*day["k"]*(np.asarray(z)-500)/(RD*t))
        e = p * day["e500_Pa"] / day["p500_Pa"]
    elif model == "constant_e":
        e = np.ones_like(t) * day["e500_Pa"]
        p = .378*e + (day["p500_Pa"]-.378*e) * (t/day["T500_K"])**(G/(RD*LAPSE))
    else:
        p = day["p500_Pa"] * (t/day["T500_K"])**day["n"]
        e = p * day["e500_Pa"] / day["p500_Pa"]
    rho = (p-.378*e)/(RD*t)
    return p, rho, t, e


def equilibrium_density(rho, day, model="lapse_mixing"):
    rho = np.asarray(rho)
    if model == "isothermal":
        t = np.ones_like(rho) * day["T500_K"]
        z = 500 - RD*t/(G*day["k"]) * np.log(rho/day["rho500_kg_m3"])
    else:
        n = G/(RD*LAPSE) if model == "constant_e" else day["n"]
        t = day["T500_K"] * (rho/day["rho500_kg_m3"])**(1/(n-1))
        z = 500 + (day["T500_K"]-t)/LAPSE
    p, rr, tt, e = profile(z, day, model)
    return z, p, t, e


def row(mass, volume, day, sfs=None, model="lapse_mixing"):
    z, p, t, e = map(float, equilibrium_density(mass/volume, day, model))
    r = dict(day=day["id"], model=model, z_m=z, p_Pa=p, p_over_p0=p/P0,
             T_K=t, vapour_Pa=e, relative_humidity=e/float(saturation_e(t)),
             mass_kg=mass, volume_m3=volume,
             ground_clearance_m_at_sea_level=z-R,
             below_sea_level=z < 0, touches_or_below_ground=z < R,
             supersaturated=e > float(saturation_e(t))*(1+1e-10))
    if sfs:
        r["sfs"] = {k: v*P0/p for k,v in sfs.items()}
        r["least_SF"] = min(r["sfs"].values())
        r["governing"] = min(r["sfs"], key=r["sfs"].get)
    return r


def demand(C, envelope="all_019", volume=V0, model="lapse_mixing"):
    """C is headroom relative to nominal lift of this effective volume."""
    lift = L0*volume/V0
    rho = (lift-np.asarray(C))/volume
    rows = [equilibrium_density(rho, d, model) for d in selected(envelope)]
    p = np.stack([r[1] for r in rows])
    z = np.stack([r[0] for r in rows])
    return np.max(p, axis=0)/P0, np.min(z, axis=0)


def floor_C(z_floor, envelope="all_019", volume=V0, model="lapse_mixing"):
    if z_floor is None:
        return 0.
    rho = min(float(profile(z_floor,d,model)[1]) for d in selected(envelope))
    return max(0., L0*volume/V0 - volume*rho)


def main():
    floors = []
    for env in ["optimistic","conservative","all_019"]:
        for model in ["lapse_mixing","constant_e","isothermal"]:
            for z in [None,0.,10.,100.,500.]:
                c = floor_C(z,env,model=model)
                q,zmin = demand(c,env,model=model)
                floors.append(dict(envelope=env,profile=model,altitude_floor_m=z,
                                   C_kg=c, C_fraction=c/L0,
                                   nominal_required_SF=float(q),
                                   minimum_float_m=float(zmin),
                                   ISA_float_m=row(L0-c,V0,DAYS[0],model=model)["z_m"]))
    frontier = []
    for env in ["optimistic","conservative","all_019"]:
        for c in np.linspace(0.,650.,131):
            q,zmin=demand(c,env)
            frontier.append(dict(envelope=env,C_kg=float(c),
                                 nominal_required_SF=float(q),minimum_float_m=float(zmin)))
    out = dict(days=DAYS, floors=floors, frontier=frontier,
               full_gross_mass_days=[row(L0,V0,d) for d in DAYS])
    (ROOT/"ATMOSPHERE.json").write_text(json.dumps(out,indent=2)+"\n")
    for r in floors:
        if r["profile"]=="lapse_mixing" and r["envelope"]!="conservative":
            print(r)


if __name__=="__main__":
    main()
