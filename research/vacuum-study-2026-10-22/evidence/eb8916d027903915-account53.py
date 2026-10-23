"""Independent P2 scalar account using the explicitly selected thermal table.

No upstream Python module is imported. Equations are stated in METHOD.md.
"""
from pathlib import Path
from functools import lru_cache
import json
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
INPUT = json.loads((ROOT/"inputs/040/INPUTS.json").read_text())
CORE = INPUT["core"]
ATMOS = json.loads((ROOT/"inputs/040/ATMOSPHERE.json").read_text())
SPECIES = json.loads((ROOT/"inputs/040/SERVICE-INPUTS.json").read_text())["species"]
P0, L0, T0 = (INPUT["case"][k] for k in ["p0_Pa", "lift0_kg", "T0_K"])
BETA = brentq(lambda b: b+b**3-1, 0., 1.)
RHOAIR = L0/(4*np.pi*10**3/3)
DRYM = sum(s["dry_x"]*s["M_kg_mol"] for s in SPECIES.values())/sum(s["dry_x"] for s in SPECIES.values())
RU = 8.31446261815324
SCARF = 30.34139731914874
NU = .0768
ALPHA = 11.3e-6
DA = 23.6e-6-ALPHA
KB = .5*67e9*CORE["rho"]/2700
COAT = .0075752*1.10
NAMES = ["gamma", "Q", "face_tuple", "film"]


def save(name, obj):
    (ROOT/name).write_text(json.dumps(obj, indent=2, allow_nan=False)+"\n")


def parameters(mask, usage):
    u = [usage if mask & (1 << j) else 0. for j in range(4)]
    return 290e9*(293.6/290)**u[2], 345e6*(379.2/345)**u[2], .33*(.82/.33)**u[1], .1464728290914915*2**(-u[3]), u[0]


class Account:
    def __init__(self, table, radius, weather, cure_global=False):
        self.table, self.r, self.weather, self.cure_global = table, radius, weather, cure_global
        self.area = 4*np.pi*radius**2
        self.volume = 4*np.pi*radius**3/3
        self.lift = L0*(radius/10)**3
        if weather == "ISA":
            self.weather_loss, multiplier = 0., 1.
        else:
            row = next(x for x in ATMOS["floors"] if x["envelope"] == "optimistic"
                       and x["profile"] == "lapse_mixing" and x["altitude_floor_m"] == 100)
            self.weather_loss = self.lift*row["C_fraction"]
            multiplier = row["nominal_required_SF"]
        q70 = .5*RHOAIR*(70*1852/3600)**2
        self.pressure = P0*max(1.01, multiplier)+q70
        self.force_constant = self.pressure*radius/4
        self.gridlog = np.log(table["tc_m"])
        load = .47*q70*np.pi*radius**2
        pad_area = load/CORE["crush_Pa"]
        pad_t = np.sqrt(3*1.33*load*np.log(np.sqrt(pad_area/np.pi)/.025)/(2*np.pi*276e6))
        self.pad_mass = 2700*pad_area*pad_t
        self.scan = np.geomspace(.0012*radius/10, 1.4*radius/10, 560)

    def heat(self, tc):
        x = np.log(tc)
        values = {k: np.interp(x, self.gridlog, self.table[k]) for k in
                  ["gradient_K", "curvature_temperature_K", "max_outer_K", "min_outer_K"]}
        excursion = 1.002*np.maximum(abs(366.4833333333333-values["max_outer_K"]),
                                    abs(366.4833333333333-values["min_outer_K"]))
        cold_drop = 1.002*np.maximum(366.4833333333333-values["min_outer_K"], 0.)
        values["edge_shear_Pa"] = DA*excursion*np.sqrt(2*KB*CORE["Gc_Pa"])
        values["edge_SF"] = 25*6894.757293168361/values["edge_shear_Pa"]
        values["wall_SF"] = 227.53e6/(1.2*67e9*DA*excursion)
        values["cure_numerator"] = KB*DA*cold_drop*tc/2
        return values

    def preparation(self, tc, mask, usage, favorable_e=False):
        E, strength, Q, film, ug = parameters(mask, usage)
        heat = self.heat(tc)
        et = 290e9 if favorable_e else E
        gradient = et*ALPHA*1.002*heat["gradient_K"]/(2*(1-NU))
        bending_per_m = et*ALPHA*1.002*heat["curvature_temperature_K"]/(2*(1-NU**2)*self.r)
        return E, strength, Q, film, ug, heat, gradient, bending_per_m

    def screens(self, tf, tc, prepared, detail=False):
        E, strength, Q, film, ug, heat, gradient, bend_per_m = prepared
        sep = tf+tc
        pressure_stress = self.force_constant/tf
        sigma0 = E*sep/(self.r*np.sqrt(1-NU**2))
        crimp = CORE["Gc_Pa"]*sep**2/(2*tf*tc)
        vc = sigma0/crimp
        kc = np.where(vc <= 2, 1-vc/4, 1/vc)
        base = np.where(vc < 2, .2, 1.)
        gamma = base*((.2+.4*np.minimum(vc, 2))/base)**ug
        bend = bend_per_m*sep
        cure = heat["cure_numerator"]/tf
        demand = pressure_stress+gradient+bend+cure
        global_demand = pressure_stress+(cure if self.cure_global else 0.)
        crimp_demand = pressure_stress+gradient+bend+(cure if self.cure_global else 0.)
        modes = {
            "global": gamma*kc*sigma0/global_demand,
            "compression": strength/demand,
            "crimp": crimp/crimp_demand,
            "crush": np.full_like(tf, 2*CORE["crush_Pa"]/self.pressure),
            "wrinkle": BETA*Q*np.sqrt(E*CORE["Ec_Pa"]*tf/tc)/demand,
            "dimple": E*(tf/CORE["s_cell_m"])**2/((1-NU**2)*demand),
            "scarf": 10e6*(1+SCARF**2)/(SCARF*demand),
            "cell_wall": heat["wall_SF"],
        }
        if not detail:
            return np.minimum.reduce(list(modes.values()))
        return modes, dict(E_Pa=E, strength_Pa=strength, Q=Q, film_kg_m2_interface=film,
                           gamma=gamma, Vc=vc, pressure_stress_Pa=pressure_stress,
                           gradient_stress_Pa=gradient, pattern_stress_Pa=bend,
                           cure_compression_Pa=cure, demand_Pa=demand, **heat)

    def face(self, tc, mask, usage, favorable_e=False):
        tc = np.atleast_1d(tc).astype(float)
        prepared = self.preparation(tc, mask, usage, favorable_e)
        lower = np.full_like(tc, 1e-6)
        upper = np.full_like(tc, min(.0195, .008*self.r/10))
        valid_upper = self.screens(upper, tc, prepared) >= 1
        for _ in range(44):
            mid = (lower+upper)/2
            passes = self.screens(mid, tc, prepared) >= 1
            upper = np.where(passes, mid, upper)
            lower = np.where(passes, lower, mid)
        tf = upper*(1+3e-12)
        valid = valid_upper & (prepared[5]["edge_SF"] >= 1-1e-10)
        return tf, valid

    @lru_cache(maxsize=128)
    def scanned_face(self, mask, usage, favorable_e):
        return self.face(self.scan, mask, usage, favorable_e)

    def bill(self, tf, tc, mask, usage, floor, route, detail=False):
        E, strength, Q, film, ug = parameters(mask, usage)
        A = self.area
        seam = A*(1/(.6096-SCARF*tf)+1/(1.8288-SCARF*tf))
        joint = {"film": 2*A*film,
                 "scarf": seam*2*tf*np.sqrt(1+SCARF**2)*.07,
                 "splice": seam*.0005*tc*500, "seal": seam*.002}
        face_mass, core_mass = 2*A*1850*tf, A*CORE["rho"]*tc
        physical = sum(joint.values())
        charged = np.maximum(physical, .05*(face_mass+core_mass)) if floor else physical
        seam_polymer = joint["scarf"]+joint["splice"]+joint["seal"]
        moisture_scale = .1 if route == "bake" else 1.
        material_water = moisture_scale*(.002*joint["film"]+.001*core_mass+
                                         .01*A*.01+.01*A*COAT+.01*seam_polymer)
        inventory = .1*(.0485*joint["film"]+.001*core_mass+.01*seam_polymer)
        sorbent = (1.1*(material_water+inventory)+.1*(self.r/10)**3)/.1+2 if route == "sorbent" else np.zeros_like(tc)
        initial = 10*self.volume/(RU*T0)*DRYM
        ingress_moles = ((seam*.001+.01)*.1/(RU*T0)*86400
                         +10*3.34645e-16*seam*(.07/1250)/(tf*np.sqrt(1+SCARF**2))*P0*86400)
        water_x = 1000/P0
        incoming = ingress_moles*((1-water_x)*DRYM+water_x*.01801528)
        gas_aboard = initial+incoming
        capture = .95 if route == "sorbent" else 0.
        released = (inventory+material_water)*(1-np.exp(-1))*(1-capture)
        gas_pressure = (initial/DRYM+ingress_moles*(1-water_x*capture)+released/.01801528)*RU*320/self.volume
        bill = dict(faces=face_mass, core=core_mass, joining=charged, coating=A*COAT,
                    structural_primer=A*.01, external_water=A*.1, added_material_water=material_water,
                    sorbent=sorbent, pad=self.pad_mass, systems=100.,
                    gas=np.maximum(.01*self.lift, gas_aboard), contamination=A*5/(400*np.pi),
                    weather=self.weather_loss)
        payload = self.lift-sum(bill.values())
        if not detail:
            return payload, gas_pressure <= .01*P0*(1+1e-10)
        scalar = lambda x: float(np.ravel(x)[0])
        modes, props = self.screens(np.atleast_1d(tf), np.atleast_1d(tc),
                                   self.preparation(np.atleast_1d(tc), mask, usage), True)
        return dict(tf_m=scalar(tf), tc_m=scalar(tc), payload_kg=scalar(payload),
                    mask=mask, usage=float(usage), selected_axes=[NAMES[j] for j in range(4) if mask & 1 << j],
                    bill_kg={k: scalar(v) for k, v in bill.items()},
                    joining_kg={k: scalar(v) for k, v in joint.items()}, seam_length_m=scalar(seam),
                    properties={k: scalar(v) for k, v in props.items()},
                    modes={**{k: scalar(v) for k, v in modes.items()}, "core_edge":scalar(props["edge_SF"])},
                    pressure_Pa=self.pressure, service_pressure_Pa=scalar(gas_pressure),
                    service_pressure_SF=scalar(.01*P0/gas_pressure), lift_kg=self.lift,
                    geometry_domain=dict(tc_min_m=.0012*self.r/10, tc_max_m=1.4*self.r/10),
                    installed_hull_SF=None)

    def optimize(self, mask, usage, floor, route, favorable_e=False, details=True):
        tf, good = self.scanned_face(mask, float(usage), favorable_e)
        values, pressure_ok = self.bill(tf, self.scan, mask, usage, floor, route)
        valid = good & pressure_ok
        values = np.where(valid, values, -np.inf)
        if not np.any(valid):
            return None
        candidates = [(float(np.max(values)), float(self.scan[np.argmax(values)]))]
        def objective(logtc):
            tc = np.array([np.exp(logtc)])
            face, feasible = self.face(tc, mask, usage, favorable_e)
            payload, service = self.bill(face, tc, mask, usage, floor, route)
            return -float(payload[0]) if feasible[0] and service[0] else 1e15
        peaks = np.flatnonzero(valid[1:-1] & (values[1:-1] >= values[:-2])
                               & (values[1:-1] >= values[2:]))+1
        for j in peaks:
            answer = minimize_scalar(objective, bounds=(np.log(self.scan[j-1]), np.log(self.scan[j+1])),
                                     method="bounded", options={"xatol": 2e-10})
            if answer.fun < 1e14:
                candidates.append((-float(answer.fun), float(np.exp(answer.x))))
        for j in np.flatnonzero(valid[:-1] != valid[1:]):
            left, right = np.log(self.scan[j]), np.log(self.scan[j+1])
            left_good = bool(valid[j])
            for _ in range(35):
                mid = (left+right)/2
                if (objective(mid) < 1e14) == left_good:
                    left = mid
                else:
                    right = mid
            t = left if left_good else right
            candidates.append((-objective(t), float(np.exp(t))))
        best, tc = max(candidates)
        if not details:
            return best
        tf, _ = self.face([tc], mask, usage, favorable_e)
        answer = self.bill(tf, np.array([tc]), mask, usage, floor, route, True)
        answer["search"] = dict(grid_count=len(self.scan), refined_peaks=len(peaks),
                                candidates=len(candidates), favorable_E_bound=favorable_e)
        return answer


def least(account, floor, route):
    points = [account.optimize(mask, 1. if mask else 0., floor, route) for mask in range(16)]
    feasible = [mask for mask, point in enumerate(points) if point is not None and point["payload_kg"] >= 0.]
    if not feasible:
        return dict(minimum_axis_count=None, chosen=None, endpoints=points, favorable_bounds=[])
    count = min(m.bit_count() for m in feasible)
    candidates = []
    for mask in feasible:
        if mask.bit_count() != count:
            continue
        if mask == 0:
            candidates.append(points[0])
        else:
            def value(usage):
                out = account.optimize(mask, usage, floor, route, details=False)
                return -1e10 if out is None else out
            usage = brentq(value, 0., 1., xtol=2e-8)
            candidates.append(account.optimize(mask, min(1., usage+2e-9), floor, route))
    bounds = []
    for mask in range(16):
        if mask & 4 and mask.bit_count() < count:
            upper = account.optimize(mask, 1., floor, route, favorable_e=True, details=False)
            bounds.append(dict(mask=mask, favorable_payload_upper_kg=upper))
    return dict(minimum_axis_count=count, chosen=min(candidates, key=lambda p:(p["usage"], p["mask"])),
                ties=candidates, endpoints=points, favorable_bounds=bounds)


if __name__ == "__main__":
    import sys
    model = sys.argv[1]
    if model == "owner_table":
        tables = json.loads((ROOT/"inputs/048/THERMAL-TABLES.json").read_text())["MLCCAg"]
    else:
        tables = json.loads((ROOT/"SETTLED-THERMAL-TABLES.json").read_text())[model]["MLCCAg"]
    if "--probe" in sys.argv:
        import csv
        records = list(csv.DictReader((ROOT/"inputs/048/ROWS.csv").open()))
        records = [r for r in records if r["profile"] == "MLCCAg"
                   and r["external_water_kg_m2"] == "0.1"
                   and r["weather"] in ["ISA", "optimistic"]]
        checks = []
        for row in records:
            radius = int(row["R_m"])
            account = Account(tables[str(radius)], radius, row["weather"])
            point = account.bill(np.array([float(row["endpoint_tf_mm"])/1000]),
                                 np.array([float(row["endpoint_tc_mm"])/1000]), 11, 1.,
                                 row["floor"] == "True",
                                 {"desiccant": "sorbent", "bake70": "bake",
                                  "dry_gas": "dry_gas"}[row["drying"]], True)
            expected = float(row["endpoint_payload_kg"])
            checks.append(dict(id=row["id"], owner_payload_kg=expected,
                               independent_payload_kg=point["payload_kg"],
                               difference_kg=point["payload_kg"]-expected))
        account = Account(tables["10"], 10, "ISA")
        optimum = account.optimize(11, 1., True, "bake")
        account_cure = Account(tables["10"], 10, "ISA", True)
        cure_optimum = account_cure.optimize(11, 1., True, "bake")
        save("ACCOUNT-PROBE.json", dict(filed_geometry_checks=checks,
                                       baseline_optimum=optimum, cure_included_optimum=cure_optimum))
        print(json.dumps(dict(comparisons=len(checks),
                              max_payload_difference_kg=max(abs(c["difference_kg"]) for c in checks),
                              optimized_baseline_payload_kg=optimum["payload_kg"],
                              optimized_cure_payload_kg=cure_optimum["payload_kg"]), indent=2))
        raise SystemExit(0)
    output = []
    for radius in [10, 12, 15]:
        for weather in ["ISA", "optimistic"]:
            for cure_global in [False, True]:
                account = Account(tables[str(radius)], radius, weather, cure_global)
                for floor in [False, True]:
                    for route in ["dry_gas", "bake", "sorbent"]:
                        row = dict(model=model, R_m=radius, weather=weather,
                                   cure_in_global=cure_global, floor=floor, drying=route,
                                   result=least(account, floor, route))
                        output.append(row)
                print(json.dumps(dict(model=model, R_m=radius, weather=weather,
                                      cure_in_global=cure_global, completed_rows=len(output))), flush=True)
    save("ACCOUNT-"+model+".json", output)
    print(json.dumps({"model": model, "rows":len(output),
                      "endpoint_points":sum(p is not None for row in output for p in row["result"]["endpoints"])}))
