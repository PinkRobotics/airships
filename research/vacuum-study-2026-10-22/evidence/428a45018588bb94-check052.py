"""Independent CHECK052 arithmetic. No foreign executable is accessed.

Inputs are the pinned numerical force/eigen witnesses and declared assumptions.
Owner output is loaded only by the comparison driver, not by the model.
"""
from pathlib import Path
from functools import lru_cache
import csv
import json
import math
import time
import numpy as np
from scipy.optimize import brentq

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


def write(name, value):
    (B / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


I34 = read("inputs/034/INPUTS.json")
I40 = read("inputs/own040/owner/INPUTS.json")
S46 = read("inputs/046/SERVICE.json")["selected_full_restraint_worst"]
P0 = I34["environment"]["p_external_Pa"]
T0 = I34["environment"]["T_K"]
LIFT = I34["environment"]["lift_reference_kg"]
RG = I34["constants"]["R_universal_J_mol_K"]
RHO = LIFT / (4 * math.pi * 10**3 / 3)
E = 410e9
RHOSIC = 3100.
RHOJ = 1550.
TAU = 28.9e6
FJ = 1470e6
F_TENSION = 15.586e6
MW = I34["species"]["H2O"]["M_kg_mol"]
RET0 = .96**3.65
RET1 = .995**10
PHI = S46["instantaneous_strength_factor"]
THERM = S46["added_ply_stress_fully_restrained_Pa"]
AXES = ["SiC_full_member_compression", "film_effective_strength",
        "ten_year_retention", "joint_allowance"]
WEATHER = {
    "ISA": {"headroom10_kg": 0., "pressure_factor": 1., "T_K": 284.9, "pw_Pa": 1000.},
    "optimistic": {"headroom10_kg": 55.340908917960405,
                   "pressure_factor": 1.0365529619839071, "T_K": 294.9, "pw_Pa": 1000.},
    "both": {"headroom10_kg": 441.77010544583936,
             "pressure_factor": 1.0228888077609428, "T_K": 310., "pw_Pa": 6000.},
}
ENV46 = list(csv.DictReader((B / "inputs/046/ENVIRONMENT.csv").open()))


def saturation(T):
    c = T - 273.15
    return 611.21 * math.exp((18.678 - c / 234.5) * c / (257.14 + c))


def cold(h):
    return float(next(r["film_K"] for r in ENV46
                      if r["weather"] == "nominal_034_water"
                      and r["phase"] == "night"
                      and r["optics"] == "037_white_target"
                      and float(r["h_W_m2K"]) == h))


PW_TARGET = .05 * saturation(cold(5))
PW_COLD = .05 * saturation(cold(2))


def mooring(radius):
    dynamic = .5 * RHO * (70 * 1852 / 3600)**2
    force = .47 * dynamic * math.pi * radius**2
    area = force / I40["core"]["crush_Pa"]
    a = math.sqrt(area / math.pi)
    t = math.sqrt(3 * (1 + .33) * force * math.log(a / .025)
                  / (2 * math.pi * 276e6))
    return {"force_N": force, "area_m2": area, "thickness_m": t,
            "mass_kg": area * t * 2700.}


class Family:
    def __init__(self, label):
        self.label = label
        folder = f"inputs/check041/runs/{label}-m24/"
        self.ref = read(folder + "RESULTS.json")
        with np.load(B / folder / "STATIC.npz", allow_pickle=False) as z:
            self.points = z["points"]
            self.edges = z["edges"]
            self.cells = z["cells"]
            self.N = z["subelement_N"]
            self.M = z["subelement_M"]
            self.member = z["subelement_member"]
            self.JN = z["joint_N"].ravel()
            self.JM = z["joint_M"].ravel()
            self.JT = z["joint_T"].ravel()
        chord = np.linalg.norm(self.points[self.edges[:, 1]]
                               - self.points[self.edges[:, 0]], axis=1)
        self.lengths = 20 * np.arcsin(chord / 20)
        self.total_length = float(sum(self.lengths))
        self.max_chord = float(max(chord))
        self.a0 = self.ref["section"]["area_m2"]
        self.g = self.ref["section"]["gyration_m"]
        self.eigen = self.ref["linear_multipliers"][0]
        self.sag = self.geometry_sag()
        self.L = self.lengths[self.member]

    def geometry_sag(self):
        pts = self.points[self.cells]
        a = np.linalg.norm(pts[:, 1] - pts[:, 2], axis=1)
        b = np.linalg.norm(pts[:, 0] - pts[:, 2], axis=1)
        c = np.linalg.norm(pts[:, 0] - pts[:, 1], axis=1)
        s = (a+b+c)/2
        ap = np.sqrt(s*(s-a)*(s-b)*(s-c))
        ri = ap / s
        rc = np.maximum.reduce([a, b, c])
        h = rc - np.sqrt(rc*rc - ri*ri)
        mean_sag = h * h * (rc-h/3) / (ri*ri)
        unit = pts / 10
        numerator = np.abs(np.einsum("ij,ij->i", unit[:, 0],
                                    np.cross(unit[:, 1], unit[:, 2])))
        denominator = (1 + np.einsum("ij,ij->i", unit[:, 0], unit[:, 1])
                       + np.einsum("ij,ij->i", unit[:, 1], unit[:, 2])
                       + np.einsum("ij,ij->i", unit[:, 2], unit[:, 0]))
        spherical = 200 * np.arctan2(numerator, denominator)
        return float(np.dot(mean_sag, spherical) / sum(spherical))

    def section_at(self, a, q, want_joint=False):
        ro = math.sqrt(2*self.g**2 + a/(2*math.pi))
        ri = math.sqrt(2*self.g**2 - a/(2*math.pi))
        inertia = a * self.g**2
        lam = math.pi**2 * E * inertia / (self.L**2 * self.N)
        axial = q * self.N / a
        if np.min(lam) <= q:
            return {"failure": True, "compression": math.inf}
        bending = q*(self.M + self.N*self.L/1000)*ro/inertia/(1-q/lam)
        comp = axial+bending
        tensile = float(max(0., max(bending-axial)))
        gamma = .099 + .901*math.exp(-math.sqrt(ro/(ro-ri))/16)
        local = gamma*.6*E*(ro-ri)/ro
        result = {"failure": False, "a": a, "ro": ro, "ri": ri,
                  "I": inertia, "compression": float(max(comp)),
                  "tension": tensile, "local_peak_SF": local/max(comp),
                  "local_axial_SF": local/max(axial),
                  "global_SF": .2*self.eigen*a/self.a0/q,
                  "euler_SF": float(min(lam)/q)}
        if want_joint:
            peak = np.zeros(750)
            np.maximum.at(peak, self.member, comp)
            result["member_compression"] = peak
            # Independent simultaneous bisection of all 1500 scalar sleeve roots.
            jn, jm, jt = q*self.JN, q*self.JM, q*self.JT
            low = np.full(jn.shape, 1e-12)
            high = np.full(jn.shape, .01)
            for _ in range(65):
                aj = (low+high)/2
                rj = np.sqrt(ro**2 + aj/math.pi)
                ij = aj*(rj*rj+ro*ro)/4
                demand = jn/aj + jm*rj/ij
                bad = demand > FJ
                low = np.where(bad, aj, low)
                high = np.where(bad, high, aj)
            aj = (low+high)/2
            overlap = np.sqrt((jn+2*jm/ro)**2+(jt/ro)**2)/(2*math.pi*ro*TAU)
            result["sleeves10_kg"] = float(sum(aj*overlap)*RHOJ)
            result["bond10_kg"] = float(sum(2*math.pi*ro*overlap)*.0002*1400)
            result["joint_capacity_SF"] = float(np.min(FJ/(jn/aj + jm*np.sqrt(ro*ro+aj/math.pi)
                                                             /(aj*(2*ro*ro+aj/math.pi)/4))))
        return result

    @lru_cache(maxsize=20000)
    def size(self, weather, strength, peak):
        p = P0*max(1.01, WEATHER[weather]["pressure_factor"]) + .5*RHO*(70*1852/3600)**2
        q = p/P0

        def margin(a):
            s = self.section_at(a, q)
            if s["failure"]:
                return -1.
            return min(s["global_SF"], s["euler_SF"],
                       strength/s["compression"],
                       F_TENSION/max(s["tension"], 1e-20),
                       s["local_peak_SF" if peak else "local_axial_SF"]) - 1

        lo = 1e-5
        hi = .002
        while margin(hi) < 0:
            hi *= 1.3
        a = brentq(margin, lo, hi, xtol=5e-17, rtol=2e-14)
        return self.section_at(a, q, True)

    def vacuum(self, radius, weather, service, s, film_t, pbo, actual_sleeves,
               bond, protection):
        k = radius/10
        a = s["a"]*k*k
        ro, ri = s["ro"]*k, s["ri"]*k
        length = self.total_length*k
        area = 4*math.pi*radius**2
        vol = 4*math.pi*radius**3/3 - 4*math.pi*radius**2*self.sag*k - a*length - film_t*area
        surface = 2*math.pi*(ro+ri)*length
        Bwater = .1*(.006*pbo + .0057*actual_sleeves + .0026*protection["PET"]
                     + .0263*bond + .0001*surface
                     + .01*(protection["attachment"]+protection["white"]+protection["seams"]))
        ext = P0*WEATHER[weather]["pressure_factor"]
        pw = WEATHER[weather]["pw_Pa"]
        species = I34["species"]
        drysum = sum(v["dry_x"] for v in species.values())
        xs = {name:v["dry_x"]/drysum for name,v in species.items() if name != "H2O"}
        leak_moles = .1*(.001*length + .001*252 + .01)*86400/(RG*T0)
        dry_rates = {name: .5*area/22414 * I34["mylar"]["permeance_ratios_to_O2_assumed"][name]
                     * (ext-pw)*x/101325 + leak_moles*(1-pw/ext)*x
                     for name,x in xs.items()}
        water_rate = .001*area + leak_moles*(pw/ext)*MW
        dry_rate = sum(dry_rates[n]*species[n]["M_kg_mol"] for n in xs)
        initial_n = 10*vol/(RG*T0)
        dry_mean_molar = sum(xs[n]*species[n]["M_kg_mol"] for n in xs)
        initial_mass = initial_n*dry_mean_molar
        pressure_limit = P0*.01
        capacity = PW_TARGET*vol*MW/(RG*T0)
        cold_capacity = PW_COLD*vol*MW/(RG*T0)

        def humtime(cap):
            return 24*brentq(lambda d: water_rate*d+Bwater*(-math.expm1(-d))-cap,
                             0, max(1, 2*cap/water_rate))

        first_h = humtime(capacity)
        cold_h = humtime(cold_capacity)
        all_external_moles = sum(dry_rates.values()) + water_rate/MW

        def pressure(d):
            return (initial_n + all_external_moles*d+Bwater/MW*(-math.expm1(-d)))*RG*320/vol

        pressure_h = 24*brentq(lambda d: pressure(d)-pressure_limit, 0, 10000)
        speed_p = (all_external_moles+Bwater/MW)*RG*320/(24*(pressure_limit-3))
        speed_w = (water_rate+Bwater)/MW*RG*320/(24*(PW_TARGET-3))
        pumps_p = math.ceil(max(speed_p/(27.5*.75), (water_rate+Bwater)/24/.7))
        pumps_d = math.ceil(max(speed_p/(27.5*.75), speed_w/(27.5*.75),
                               (water_rate+Bwater)/24/.7))
        pumps = 0 if service == "ground" else pumps_p if service == "onboard_pressure" else pumps_d
        energy_kwh = (1000*pumps+5)*24/1000
        battery = energy_kwh*1000/(150*.8*.9)
        mass = 50. if service == "ground" else 15+5+5+20+44*pumps+battery
        return {"service": service, "service_mass_kg": mass,
                "installed_high_allowance_kg": 20., "pumps": pumps,
                "pressure_only_pumps": pumps_p, "dry_cavity_pumps": pumps_d,
                "pump_speed_required_pressure_m3_h": speed_p,
                "pump_speed_required_dry_m3_h": speed_w,
                "electrical_24h_kWh": energy_kwh, "battery_24h_kg": battery,
                "total_pressure_24h_sealed_Pa": pressure(1),
                "pressure_limit_Pa": pressure_limit, "free_volume_m3": vol,
                "water_external_upper_kg_day": water_rate, "dry_external_kg_day": dry_rate,
                "initial_material_release_water_proxy_kg": Bwater,
                "SiC_internal_and_external_surface_m2": surface, "initial_gas_kg": initial_mass,
                "gas_charge_kg": max(.01*LIFT*k**3, initial_mass+water_rate+dry_rate),
                "humidity_pressure_target_Pa": PW_TARGET, "water_capacity_kg": capacity,
                "first_cycle_humidity_limit_h": first_h, "cold_h2_humidity_limit_h": cold_h,
                "steady_cycle_humidity_limit_h": 24*capacity/water_rate,
                "total_pressure_limit_h": pressure_h,
                "planned_ground_service_interval_h": (min(24., .9*first_h, .9*pressure_h)
                                                      if service == "ground" else None),
                "life_dryness_supported_by_sizing": service != "onboard_pressure",
                "initial_evacuation_24h_effective_speed_m3_h": vol*math.log(ext/10)/24,
                "unvented_bore_air_debit_kg": math.pi*ri*ri*length*RHO}

    @lru_cache(maxsize=30000)
    def point(self, radius, weather, service, mask, u, peak=True):
        k = radius/10
        area = 4*math.pi*radius**2
        strength = 1e9 * 3.9**u if mask&1 else 1e9
        film_strength = 3.48e9*(5.8/3.48)**u if mask&2 else 3.48e9
        retention = RET0*(RET1/RET0)**u if mask&4 else RET0
        s = self.size(weather, strength, peak)
        applied = P0*max(1.01, WEATHER[weather]["pressure_factor"]) + .5*RHO*(70*1852/3600)**2
        film_t = applied*self.max_chord*k/(film_strength*retention*PHI-THERM)
        pbo = film_t*area*1560
        tube = RHOSIC*s["a"]*self.total_length*k**3
        sleeve = s["sleeves10_kg"]*k**3
        lower_joint = max(sleeve, .05*tube)
        joint = lower_joint*(sleeve/lower_joint)**u if mask&8 else lower_joint
        bond = max(5*k*k, s["bond10_kg"]*k*k)
        protection = {"PET": area*12e-6*1390, "Al": area*100e-9*2700,
                      "attachment": area*.025, "white": area*.025,
                      "seams": 5*self.total_length*k/774.4408874322422}
        vacuum = self.vacuum(radius, weather, service, s, film_t, pbo, sleeve, bond, protection)
        headroom = WEATHER[weather]["headroom10_kg"]*k**3
        sag = 3*(LIFT*k**3-headroom)*self.sag*k/radius
        bill = {"SiC_tubes": tube, "joint_sleeves_and_allowance": joint,
                "joint_bond_and_installation": bond, "nodes": .02*252*k**3,
                "PBO_two_plies": pbo, "barrier_and_protection": sum(protection.values()),
                "systems": 100., "vacuum_service": vacuum["service_mass_kg"],
                "gas": vacuum["gas_charge_kg"], "exterior_water": .1*area,
                "contamination": 5*k*k, "mooring_load_introduction": mooring(radius)["mass_kg"],
                "sag_lift_debit": sag, "weather_headroom": headroom}
        hazard = (s["member_compression"]/3.9e9)**10
        hwhole = float(sum(hazard))
        hcoupon = float(np.dot(hazard, s["a"]*self.lengths*k**3/1e-6))
        reliability = {"m": 10., "scale_Pa": 3.9e9, "H_whole_member": hwhole,
                       "Pf_whole_member": -math.expm1(-hwhole), "H_coupon_1cm3": hcoupon,
                       "Pf_coupon_1cm3": -math.expm1(-hcoupon),
                       "whole_scale_for_Pf1e_3_Pa": 3.9e9*(hwhole/-math.log1p(-.001))**.1,
                       "coupon_scale_for_Pf1e_3_Pa": 3.9e9*(hcoupon/-math.log1p(-.001))**.1,
                       "population": "750 members; each member peak applied uniformly to its complete SiC volume",
                       "qualified_probability": None}
        return {"R_m": radius, "weather": weather, "service": service, "mask": mask, "usage": u,
                "axes": [axis for i,axis in enumerate(AXES) if mask&(1<<i)],
                "section_area_m2": s["a"]*k*k, "gyration_m": self.g*k, "ro_m": s["ro"]*k,
                "wall_m": (s["ro"]-s["ri"])*k, "film_total_m": film_t,
                "required_SiC_strength_Pa": s["compression"], "assumed_SiC_strength_Pa": strength,
                "film_effective_strength_Pa": film_strength, "ten_year_retention": retention,
                "joint_allowance_kg": joint, "joint_actual_sleeves_kg": sleeve,
                "applied_pressure_Pa": applied,
                "all_screened_SF": min(strength/s["compression"], s["global_SF"], s["euler_SF"],
                                       s["local_peak_SF" if peak else "local_axial_SF"],
                                       F_TENSION/max(s["tension"], 1e-20), 1.),
                "global_SF": s["global_SF"], "local_peak_SF": s["local_peak_SF"],
                "local_axial_SF": s["local_axial_SF"], "required_tension_Pa": s["tension"],
                "film_SF_at_ten_years": 1., "joint_capacity_SF": s["joint_capacity_SF"],
                "bill_kg": bill, "protection_kg": protection, "vacuum": vacuum,
                "lift_kg": LIFT*k**3, "payload_kg": LIFT*k**3-sum(bill.values()),
                "local_peak_enforced": peak,
                "family": f"{self.label} CHECK041; constant g/R; rescaled area and all associated debits",
                "qualified_SF": None, "actual_frame_Pf": None, "reliability": reliability}


class Audit:
    def __init__(self):
        self.rows = []
        self.mismatches = []
        self.numeric = 0

    def compare(self, path, owner, checker):
        if isinstance(owner, dict):
            for key, value in owner.items():
                if key not in checker:
                    self.mismatches.append({"path": path+"."+key, "owner": value,
                                            "checker": "NOT_RECONSTRUCTED", "kind": "coverage"})
                else:
                    self.compare(path+"."+key, value, checker[key])
        elif isinstance(owner, list):
            if len(owner) != len(checker):
                self.mismatches.append({"path": path, "owner_length": len(owner),
                                        "checker_length": len(checker), "kind": "length"})
            for i,(a,b) in enumerate(zip(owner, checker)):
                self.compare(f"{path}[{i}]", a, b)
        else:
            row = {"path": path, "owner": owner, "checker": checker}
            if isinstance(owner, (int,float)) and not isinstance(owner, bool):
                self.numeric += 1
                absolute = 2e-6 if ("payload_kg" in path or path.endswith(".usage")) else 1e-8
                tolerance = absolute + 3e-8*abs(owner)
                row.update(delta=checker-owner, tolerance=tolerance,
                           match=bool(abs(checker-owner) <= tolerance))
            else:
                row["match"] = bool(owner == checker)
            self.rows.append(row)
            if not row["match"]:
                self.mismatches.append(dict(row, kind="numeric" if "delta" in row else "metadata"))


def reconstruct_row(family, row, audit, path):
    r,w,service = row["R_m"],row["weather"],row["service"]
    result = {"R_m":r,"weather":w,"service":service}
    for field in ["baseline", "all_axes_endpoint"]:
        old = row[field]
        new = family.point(r,w,service,old["mask"],old["usage"])
        audit.compare(path+"."+field,old,new)
        result[field] = new
    # At a subset endpoint u=1 also for the empty subset (no axis moves).
    ends = [family.point(r,w,service,mask,1.) for mask in range(16)]
    audit.compare(path+".endpoints", row["endpoints"], ends)
    feasible = [x for x in ends if x["payload_kg"] >= -1e-7]
    count = min((x["mask"].bit_count() for x in feasible), default=None)
    roots = []
    if count is not None:
        for end in feasible:
            if end["mask"].bit_count() != count:
                continue
            mask = end["mask"]
            u = (0. if family.point(r,w,service,mask,0.)["payload_kg"] >= 0 else
                 brentq(lambda t:family.point(r,w,service,mask,t)["payload_kg"],
                        0,1,xtol=2e-12,rtol=2e-12))
            roots.append(family.point(r,w,service,mask,u))
    roots.sort(key=lambda x:x["usage"])
    least = roots[0] if roots else None
    # Filed roots are ordered by mask, while selection is by common log usage.
    roots.sort(key=lambda x:x["mask"])
    audit.compare(path+".least_axis_count",row["least_axis_count"],count)
    audit.compare(path+".roots",row["roots"],roots)
    audit.compare(path+".least",row["least"],least)
    result.update(endpoints=ends, roots=roots,least=least,least_axis_count=count)
    return result


def main():
    started = time.monotonic()
    family = Family("f5-019")
    audit = Audit()
    owner = read("owner/RESULTS.json")
    print("Geometry",family.total_length, family.max_chord, family.sag,flush=True)
    reconstructed = []
    for i,row in enumerate(owner["rows"]):
        reconstructed.append(reconstruct_row(family,row,audit,f"RESULTS.rows[{i}]"))
        if (i+1)%9 == 0:
            print("primary rows",i+1,"mismatches",len(audit.mismatches),flush=True)
    sensitivity = read("owner/SENSITIVITIES.json")
    alt = Family("f5-5")
    alt_rows = []
    for i,row in enumerate(sensitivity["alternative_checked_f5_5"]):
        alt_rows.append(reconstruct_row(alt,row,audit,f"SENSITIVITIES.alternative_checked_f5_5[{i}]"))
    local = []
    for i,row in enumerate(sensitivity["local_axial_only"]):
        new=family.point(row["R_m"],row["weather"],row["service"],row["mask"],row["usage"],False)
        audit.compare(f"SENSITIVITIES.local_axial_only[{i}]",row,new)
        local.append(new)
    crossing = []
    for old in sensitivity["primary_family_crossings"]:
        w = old["weather"]
        ep = family.point(10,w,"ground",15,1.)
        bill=ep["bill_kg"]
        # Only the immutable cubic terms are needed for a lower bound on mass.
        cubic = sum(bill[x] for x in ["SiC_tubes","joint_sleeves_and_allowance",
                                      "nodes","PBO_two_plies","gas","sag_lift_debit","weather_headroom"])
        surplus=LIFT-cubic
        root=(10. if ep["payload_kg"]>=0 else
              brentq(lambda rr:family.point(rr,w,"ground",15,1.)["payload_kg"],10,30)
              if family.point(30,w,"ground",15,1.)["payload_kg"]>=0 else None)
        new={"weather":w, "endpoint_continuous_crossing_radius_m":root,
             "cubic_surplus_10m_kg":surplus,
             "negative_cubic_surplus_precludes_any_radius_in_this_family":surplus<0}
        audit.compare("SENSITIVITIES.primary_family_crossings."+w,old,new)
        crossing.append(new)
    write("RECONSTRUCTED.json",{"rows":reconstructed,"alternative_checked_f5_5":alt_rows,
                              "local_axial_only":local,"primary_family_crossings":crossing})
    write("ARITHMETIC-AUDIT.json",audit.rows)
    write("MISMATCHES.json",audit.mismatches)
    summary={"comparisons":len(audit.rows),"numeric":audit.numeric,
             "mismatches":len(audit.mismatches),"elapsed_s":time.monotonic()-started,
             "geometry":{"arc_length_m":family.total_length,"max_chord_m":family.max_chord,
                         "mean_cap_sag_m":family.sag},
             "no_owner_executable_access":True}
    write("ARITHMETIC-SUMMARY.json",summary)
    print(json.dumps(summary,indent=2),flush=True)


if __name__ == "__main__":
    main()
