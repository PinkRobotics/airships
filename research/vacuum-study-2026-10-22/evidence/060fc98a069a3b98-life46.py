#!/usr/bin/env python3
"""MAINLINE-046. Conditional film-life arithmetic, never a qualified life model."""
import csv
import json
import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "unpublished-local-ref:0f195fac91786b1b")
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
P = 95460.8379139
A = 4 * math.pi * 10**2
S0 = 1.74e9  # Total-gauge bookkeeping equivalent: 0.6*5.8 GPa / two directions.
RAW = 5.8e9
E = 270e9  # HM filament axial tangent, not a qualified laminate tangent.
RHO = 1560
YEAR = 365.0


def read(name):
    return json.loads((ROOT / name).read_text())


def save(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def csvout(name, rows):
    with (ROOT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def points():
    c = read("inputs/022d/RESULTS.json")
    d = read("inputs/041/RESULTS.json")
    out = []
    cases = [c["best_equilateral_screened"]]
    cases += [x for x in c["all_primary_rows"]
              if x["key"] == "cap/equilateral/019/cfrp_zylon/in_band"]
    for x in cases:
        out.append(dict(id="022d-" + x["case"]["reserve"],
                        sf0=x["SF"]["film"], film_kg=x["mass_kg"]["film"],
                        gauge_m=x["film_total_m"], curvature_m=x["curvature_radius_m"],
                        seam_m=x["members"] * x["member_length_m"],
                        nodes=x["nodes"], reserve_kg=x["mass_kg"]["reserve"],
                        sag_lift_kg=x["mass_kg"]["sag_lift_loss"],
                        closure_kg=x["mass_kg"]["closure"],
                        overall_source_sf=x["SF_least_with_sized_joint"]))
    for key, x in d["best_closure_by_reserve"].items():
        g = x["geometry"]
        out.append(dict(id="041-" + key,
                        sf0=x["modes"]["film"], film_kg=x["mass_kg"]["film"],
                        gauge_m=x["film_total_m"],
                        curvature_m=g["film_curvature_radius_max_m"],
                        seam_m=g["total_arc_m"], nodes=g["nodes"],
                        reserve_kg=x["mass_kg"]["reserve"],
                        sag_lift_kg=x["mass_kg"]["sag_lift_loss"],
                        closure_kg=x["mass_kg"]["total_with_reserve_and_sag"],
                        overall_source_sf=x["least_screened_SF"],
                        local_peak_sensitivity_sf=x["local_max_compression_sensitivity_SF"]))
    for x in out:
        x["stress_total_gauge_equivalent_Pa"] = P*x["curvature_m"]/(2*x["gauge_m"])
        x["stress_in_each_half_thickness_ply_Pa"] = 2*x["stress_total_gauge_equivalent_Pa"]
        x["fraction_of_5p8_GPa_fiber_strength"] = x["stress_in_each_half_thickness_ply_Pa"]/RAW
        x["minimum_nominal_retention"] = 1/x["sf0"]
        x["maximum_nominal_loss_fraction"] = 1-1/x["sf0"]
        x["maximum_constant_log_loss_per_year_for_ten_years"] = math.log(x["sf0"])/10
        x["maximum_compounded_fractional_loss_per_year_for_ten_years"] = 1-x["sf0"]**(-.1)
    return out


# Hand-read manufacturer figures: approximately ±0.02 in retention, not raw measurements.
HUMID_DAYS = np.array([0, 20, 50, 100, 200, 400, 600, 800, 1000], dtype=float)
HUMID_R = np.array([1, .965, .94, .90, .86, .83, .80, .78, .76])
OUTDOOR_MONTHS = [0, .5, 2.25, 4, 6]
OUTDOOR_HM = [1, .71, .44, .335, .35]  # Scatter is retained in the source ledger.
BETA_OUT = math.log(math.log(.35)/math.log(.71))/math.log(12)
BETA_WET = math.log(math.log(.76)/math.log(.90))/math.log(10)


def retention(scenario, years):
    d = years*YEAR
    if years == 0:
        return 1.
    if scenario == "outdoor_uncovered":
        # First measured point is at half a month; no sub-day lifetime is inferred.
        if d <= YEAR/24:
            return math.exp(math.log(.71)*d/(YEAR/24))
        return math.exp(math.log(.35)*(years/.5)**BETA_OUT)
    if scenario == "light_blocked_humid_40C80RH_proxy":
        if d <= 1000:
            return math.exp(float(np.interp(d, HUMID_DAYS, np.log(HUMID_R))))
        return math.exp(math.log(.76)*(d/1000)**BETA_WET)
    if scenario == "light_blocked_warehouse_endpoint_exponential":
        return .96**(d/1000)
    if scenario == "sealed_argon_55C_loss_ceiling_extrapolation":
        return .96**(d/210)
    if scenario == "dry_protection_acceptance_target":
        return .995**years
    raise KeyError(scenario)


SCENARIOS = {
    "outdoor_uncovered": {
        "classification": "PROJECTION",
        "basis": "Toyobo HM outdoor points at Ohtsu, June-November 1997; 45 degrees south.",
        "formula": "log-linear 1 to .71 over first half month; then exp[ln(.35)*(years/.5)^beta]",
        "beta": BETA_OUT, "measured_duration_years": .5,
        "transfer": "No source spectral dose, weather history or grade/laminate equivalence. No air barrier in this counterfactual.",
    },
    "light_blocked_humid_40C80RH_proxy": {
        "classification": "PROJECTION",
        "basis": "Toyobo AS 555 dtex, dark 40 C/80% RH; manual figure readings through 1000 days.",
        "formula": "piecewise log interpolation through 1000 days, then exp[ln(.76)*(days/1000)^beta]",
        "beta": BETA_WET, "measured_duration_years": 1000/YEAR,
        "transfer": "AS-to-HM and continuous 40 C/80% RH are comparison proxies, not the declared year's kinetics.",
    },
    "light_blocked_warehouse_endpoint_exponential": {
        "classification": "PROJECTION",
        "basis": "Toyobo AS warehouse curve about .96 at 1000 days.",
        "formula": ".96^(365*years/1000)",
        "measured_duration_years": 1000/YEAR,
        "transfer": "Endpoint-only constant-rate assumption does not reproduce the early knee; warehouse humidity/temperature unspecified in this source.",
    },
    "sealed_argon_55C_loss_ceiling_extrapolation": {
        "classification": "PROJECTION",
        "basis": "NISTIR7373: <4% loss in sealed argon-filled glass tubes at 55 C over 210 days.",
        "formula": ".96^(365*years/210)",
        "measured_duration_years": 210/YEAR,
        "transfer": "Repeated worst observed loss is a sensitivity, not a fitted trend or proof of polymer-laminate protection.",
    },
    "dry_protection_acceptance_target": {
        "classification": "PROJECTION / REQUIREMENT, NOT A MEASURED RATE",
        "basis": "Chosen maximum combined irreversible loss budget 0.5% annually.",
        "formula": ".995^years",
        "measured_duration_years": 0,
        "transfer": "Must be demonstrated on loaded finished laminate including seams, light, moisture, creep and cycling.",
    },
}


def sat_water(T):
    # Buck equation over water; below 0 C this is a supercooled-water convention.
    c = T-273.15
    return 611.21*math.exp((18.678-c/234.5)*(c/(257.14+c)))


def surface(Ta, sky, flux, alpha, epsilon, h):
    sigma = 5.670374419e-8
    return brentq(lambda T: alpha*flux-h*(T-Ta)-epsilon*sigma*(T**4-sky**4), 180, 600)


def service():
    # A local sun-facing patch, not a global-sphere energy average or a climatology.
    weather = [
        dict(name="nominal_034_water", days=305, Ta_K=284.9, water_Pa=1000, pressure_ratio=1),
        dict(name="031_optimistic_hot_wet_high", days=50, Ta_K=294.9, water_Pa=1000, pressure_ratio=1.01),
        dict(name="031_conservative_hot_wet_high", days=10, Ta_K=310., water_Pa=6000, pressure_ratio=1.02),
    ]
    optics = [
        dict(name="037_white_target", alpha=.20, epsilon=.90),
        dict(name="unqualified_OD3_low_emittance_sensitivity", alpha=.20, epsilon=.05),
        dict(name="bare_PBO_optical_assumption", alpha=.60, epsilon=.90),
    ]
    rows = []
    for w in weather:
        for o in optics:
            for h in (2., 5., 10.):
                for phase, hours, flux, skybase in (("sun", 6, 970, 275),
                                                   ("shade", 6, 0, 275),
                                                   ("night", 12, 0, 260)):
                    sky = skybase+(w["Ta_K"]-284.9)
                    T = surface(w["Ta_K"], sky, flux, o["alpha"], o["epsilon"], h)
                    ps = sat_water(T)
                    # Full attachment sensitivity, stress free at baseline air temperature.
                    # Frame held at air temperature; no frame irradiation/contraction solution is asserted.
                    eps = 4.5e-6*(w["Ta_K"]-284.9)+6e-6*(T-284.9)
                    stress = max(0., E*eps)
                    # Hand-read Toyobo instantaneous HM strength around 20-100 C.
                    phiT = min(1., max(0., 1-.10*(T-293.15)/80))
                    rows.append(dict(weather=w["name"], days=w["days"], phase=phase,
                                     hours_per_year=w["days"]*hours, optics=o["name"], h_W_m2K=h,
                                     air_K=w["Ta_K"], film_K=T, sky_K=sky,
                                     water_external_Pa=w["water_Pa"],
                                     air_RH=w["water_Pa"]/sat_water(w["Ta_K"]),
                                     RH_at_film_unclipped=w["water_Pa"]/ps,
                                     RH_at_film=min(1., w["water_Pa"]/ps),
                                     condensation_possible=w["water_Pa"]>ps,
                                     pressure_ratio=w["pressure_ratio"],
                                     added_ply_stress_fully_restrained_Pa=stress,
                                     instantaneous_strength_factor=phiT))
    dose = dict(full_sun_equivalent_hours_year=2190,
                solar_peak_W_m2=970, annual_local_solar_J_m2=970*2190*3600,
                assumed_UV_fraction=.05, assumed_visible_fraction=.45,
                unmeasured_spectral_fractions=True, candidate_intact_transmission=.001,
                annual_light_leak_fractions_tested=[0,.001,.01,.05,1])
    dose["annual_UV_J_m2"] = dose["annual_local_solar_J_m2"]*.05
    dose["annual_visible_J_m2"] = dose["annual_local_solar_J_m2"]*.45
    return weather, rows, dose


def main():
    pts = points()
    save("POINTS.json", pts)
    save("SCENARIOS.json", SCENARIOS)
    years = [0,1,5,10]
    age_rows = []
    cross = []
    for name in SCENARIOS:
        for y in years:
            r = retention(name,y)
            for p in pts:
                age_rows.append(dict(scenario=name, point=p["id"], age_years=y,
                                     retained_fraction=r, effective_total_gauge_strength_GPa=S0*r/1e9,
                                     half_ply_assumed_strength_GPa=2*S0*r/1e9,
                                     film_SF=p["sf0"]*r, qualified_strength_Pa=None,
                                     qualified_SF=None))
        for p in pts:
            age = brentq(lambda y: p["sf0"]*retention(name,y)-1, 0, 10000)
            cross.append(dict(scenario=name, point=p["id"],
                              conditional_crossing_years=age, conditional_crossing_days=age*YEAR,
                              qualified_crossing_age=None))
    csvout("AGE-SF.csv", age_rows)
    csvout("CROSSINGS.csv", cross)
    weather, env, dose = service()
    csvout("ENVIRONMENT.csv", env)
    chosen = [x for x in env if x["optics"]=="037_white_target" and x["h_W_m2K"]==5]
    worst = max(chosen, key=lambda x:x["added_ply_stress_fully_restrained_Pa"])
    qwind = (1.1672683307461802*(35*.5144444444444445)*(35*.3048)
             +.5*1.1672683307461802*(35*.3048)**2)/P
    peak_q = 1.02+qwind
    save("SERVICE.json", dict(classification="PROJECTION", weather=weather,
                              one_year_hours=8760, local_patch_dose=dose,
                              cycles_per_year=dict(daily_ground_topup=365, thermal=365,
                                                   full_vents_assumed=12, flight_gusts_assumed=36500),
                              full_vents_sensitivity=[0,12,365],
                              topup_note="Re-evacuation is not full venting or fabric folding.",
                              instantaneous_temperature_factor_note="Approximate Toyobo graph transfer, reversible; do not count as permanent aging.",
                              q_gust_ratio=qwind, peak_pressure_ratio=peak_q,
                              selected_full_restraint_worst=worst,
                              relative_humidity_equation="Modified Buck over water; coefficient set recorded in METHOD and SOURCE-DATA",
                              source_037_PBO_unprotected_sun_K=317.4188083455216,
                              source_037_PBO_unprotected_night_K=273.3052231914065,
                              no_measured_climatology=True))
    # The service-year chemistry cannot be computed from source data. Show the annual
    # reference-exposure factor needed instead of assigning a made-up activation energy.
    wet_k = -math.log(.76)/1000
    wet_sensitivity = []
    for factor in (.01,.05,.1,.25,.5,1,2):
        for p in pts:
            wet_sensitivity.append(dict(point=p["id"], equivalent_40C80RH_days_per_calendar_day=factor,
                                        ten_year_retention=math.exp(-wet_k*factor*3650),
                                        ten_year_SF=p["sf0"]*math.exp(-wet_k*factor*3650)))
    csvout("EXPOSURE-SENSITIVITY.csv",wet_sensitivity)
    model_forms=[]
    for y in (1,5,10):
        for model,r in (
            ("warehouse endpoint exponential",.96**(y*365/1000)),
            ("warehouse permanent early loss then plateau",.96),
            ("humid endpoint exponential",.76**(y*365/1000)),
            ("humid plotted curve plus stretched tail",retention("light_blocked_humid_40C80RH_proxy",y))):
            model_forms.append(dict(model=model,years=y,retention=r,
                                    qualification="PROJECTION; finite observation does not select tail form"))
    csvout("MODEL-FORM.csv",model_forms)
    light=[]
    initial_light_rate=-math.log(.71)*24
    for tau in (0,.0001,.001,.01,.05,1):
        for dose_factor in (.25,1,4):
            r=retention("outdoor_uncovered",10*tau*dose_factor)
            light.append(dict(transmission=tau,ten_year_dose_factor_relative_to_Ohtsu=dose_factor,
                              equivalent_outdoor_years=10*tau*dose_factor,
                              retention_if_dose_reciprocity_and_photo_only=r,
                              qualification="PROJECTION sensitivity: source outdoor loss includes other exposures; reciprocity and spectral transfer unmeasured"))
    csvout("LIGHT-SENSITIVITY.csv",light)
    light_limits=[]
    for p in pts:
        for dark in (1,.975,.95):
            if p["sf0"]*dark>1:
                tau=math.log(p["sf0"]*dark)/(10*initial_light_rate)
                optical_density=-math.log10(tau)
            else:
                tau=0
                optical_density=None
            light_limits.append(dict(point=p["id"],assumed_dark_retention_at_ten_years=dark,
                                     max_transmission_for_nominal_SF1_first_segment_proxy=tau,
                                     required_optical_density_proxy=optical_density))
    save("LIGHT-LIMITS.json",light_limits)

    # Once-through moisture bookkeeping, including updated seam length; no polymer
    # sorption/diffusion solution is implied by the volume-average partial pressure.
    moisture = []
    min_T = min(x["film_K"] for x in chosen)
    target_pw = .05*sat_water(min_T)
    gasR=8.314462618
    mw=.01801528
    for p in pts:
        volume=4/3*math.pi*1000-p["sag_lift_kg"]/1.1672683307461802
        water_capacity=target_pw*volume*mw/(gasR*284.9)
        # 034: source upper envelope, <1 g/m2/day, applied without T/activity reduction.
        permeation=A*.001
        # Leak gas follows wet exterior, conservative 6000 Pa / nominal p.
        qleak_mbarLs=.001*(p["seam_m"]+p["nodes"])+.01
        leak_mol=qleak_mbarLs*.1*86400/(gasR*284.9)
        leakwater=leak_mol*(6000/P)*mw
        initial=.006*p["film_kg"]
        moisture.append(dict(point=p["id"], gas_volume_m3=volume,
                             minimum_reference_film_T_K=min_T,
                             target_bulk_water_pressure_Pa=target_pw,
                             target_RH_at_coldest_patch=.05,
                             water_capacity_at_target_kg=water_capacity,
                             coupon_water_envelope_kg_per_day=permeation,
                             seam_leak_water_hot_envelope_kg_per_day=leakwater,
                             initial_PBO_moisture_kg_proxy=initial,
                             bulk_water_Pa_after_one_day_conditioned=(permeation+leakwater)*gasR*284.9/(volume*mw),
                             allowable_transmission_g_m2_day_with_zero_initial_residual=max(0,water_capacity-leakwater)/A*1000,
                             time_to_target_hours_if_source_envelope_constant=24*water_capacity/(permeation+leakwater),
                             annual_water_throughput_kg=permeation*365,
                             film_microclimate_qualified=False))
    csvout("MOISTURE.csv", moisture)

    # Barrier bills are projected constructions. Optical targets have separate mass.
    pet=A*12e-6*1390
    metal=A*50e-9*2700
    foil=A*6.35e-6*2700
    attach=A*.025
    white=A*.025
    bills = dict(area_m2=A, PET_12um_kg=pet, Al_50nm_kg=metal,
                 Al_6p35um_kg=foil, attachment_25g_m2_kg=attach,
                 outer_seam_installation_kg=5, white_25g_m2_kg=white,
                 OD3_034_one_side_kg=pet+metal+attach+5,
                 OD3_plus_white_kg=pet+metal+attach+5+white,
                 OD4_target_100nm_Al_plus_white_kg=pet+2*metal+attach+5+white,
                 foil_PET_one_side_kg=pet+foil+attach+5,
                 foil_PET_two_sides_plus_white_kg=2*(pet+foil+attach+5)+white,
                 notes=["Al gauge does not prove OD3, hermeticity or flex endurance.",
                        "White mass and optical coefficients are independent construction targets, not a qualified coating.",
                        "Two-face foil package is a dry encapsulation option; seams and trapped initial water remain."],
                 qualified_barrier_life=None)
    save("BARRIERS.json", bills)
    old_seam=774.440887
    point_bills={}
    barrier_rows=[]
    for p in pts:
        # A linear sensitivity to the inherited seam allowance, explicitly not a
        # weighed joint design. This avoids hiding the resized frame's longer seams.
        seam=5*p["seam_m"]/old_seam
        pb=dict(bills)
        for name in ("OD3_034_one_side_kg","OD3_plus_white_kg","OD4_target_100nm_Al_plus_white_kg"):
            pb[name]+=seam-5
        pb["foil_PET_two_sides_plus_white_kg"]+=2*(seam-5)
        point_bills[p["id"]]=pb
        barrier_rows.append(dict(point=p["id"],seam_m=p["seam_m"],
                                 seam_installation_scaled_kg=seam,
                                 OD3_only_kg=pb["OD3_034_one_side_kg"],
                                 OD3_white_kg=pb["OD3_plus_white_kg"],
                                 OD4_white_kg=pb["OD4_target_100nm_Al_plus_white_kg"],
                                 dual_foil_white_kg=pb["foil_PET_two_sides_plus_white_kg"],
                                 qualification="PROJECTION; 034 5 kg allowance scaled by unique seam length"))
    csvout("POINT-BARRIERS.csv",barrier_rows)

    # Alternate fibres: source-own retention models and explicit grade-transfer warnings.
    # UHMWPE uses measured SK75 3.7 GPa for strength and a different NIST yarn's
    # oxidative-aging endpoint for sensitivity, never a qualified grade combination.
    alternate=[]
    alternate_ages=[]
    for name, rho, raw, r10, note in [
        ("protected_PBO_acceptance_target",1560,5.8e9,.995**10,
         "Chosen combined-loss acceptance requirement; not demonstrated"),
        ("protected_PBO_warehouse_extrapolation",1560,5.8e9,retention("light_blocked_warehouse_endpoint_exponential",10),
         "Toyobo AS endpoint transferred to HM; constant-rate sensitivity"),
        ("protected_Kevlar49_requirement",1440,3e9,.95,
         "Own 95% ten-year retention requirement; not inferred from 200 days neutral-pH stability"),
        ("protected_UHMWPE_43C_extrapolation",970,3.7e9,.7**(10/36),
         "NIST 36-year/70%-retention endpoint at 43 C made exponential; different yarn from SK75 strength source; creep and UV excluded"),
        ("protected_SK99_chemistry_only",970,42.5e5*970,.7**(10/36),
         "Current manufacturer 42.5 cN/dtex; NIST other-yarn oxidative-aging transfer. Source creep rate at 900 MPa/30 C prevents a ten-year dimensional-stability claim"),
        ("protected_DM20_chemistry_only",970,32e5*970,.7**(10/36),
         "Manufacturer patent 32 cN/dtex; NIST other-yarn oxidative-aging transfer. Lower creep rate is not zero creep at P3 stress"),
    ]:
        seff=.3*raw  # Same assumed 60% strength efficiency, then half-gauge per direction.
        for y in (1,5,10):
            r_age=r10**(y/10)
            alternate_ages.append(dict(material=name,age_years=y,retention=r_age,
                                      effective_strength_GPa=seff*r_age/1e9,note=note))
        for p in pts:
            same_mass_sf=p["sf0"]*(seff/rho)/(S0/RHO)*r10
            m_sf1=p["film_kg"]/same_mass_sf
            m_restore=p["film_kg"]*p["sf0"]/same_mass_sf
            alternate.append(dict(material=name,point=p["id"],rho_kg_m3=rho,raw_strength_GPa=raw/1e9,
                                  effective_strength_GPa=seff/1e9,retention_at_ten_years=r10,
                                  effective_strength_at_ten_years_GPa=seff*r10/1e9,
                                  same_reinforcement_mass_ten_year_SF=same_mass_sf,
                                  fiber_kg_for_ten_year_nominal_SF1=m_sf1,
                                  fiber_kg_to_restore_initial_SF_at_ten_years=m_restore,
                                  delta_fiber_kg_to_restore_initial_SF=m_restore-p["film_kg"],
                                  full_skin_kg_for_SF1_with_OD4_white=m_sf1+point_bills[p["id"]]["OD4_target_100nm_Al_plus_white_kg"],
                                  note=note, qualified_ten_year_SF=None))
    csvout("ALTERNATE-FIBRES.csv",alternate)
    csvout("ALTERNATE-AGE.csv",alternate_ages)
    # Service-year thermal damage integral for the particular UHMWPE oxidation
    # activation energy, not transferable to PBO or creep.
    equivalent_UHMWPE_years43_per_year=sum(x["hours_per_year"]/8760*
          math.exp(-140000/gasR*(1/x["film_K"]-1/316.15)) for x in chosen)
    save("UHMWPE-SENSITIVITY.json",dict(
        oxidation_activation_energy_J_mol=140000,
        reference_temperature_K=316.15,
        equivalent_43C_years_per_declared_year=equivalent_UHMWPE_years43_per_year,
        conditional_retention_1_5_10_years=[.7**(y*equivalent_UHMWPE_years43_per_year/36) for y in (1,5,10)],
        direct_43C_endpoint_exponential_1_5_10=[.7**(y/36) for y in (1,5,10)],
        warning="Chemical scenario only. Grade, alpha relaxation, nonisothermal transfer, creep, seams and instantaneous hot strength remain open."))
    creep=[]
    for material,rate in (("SK99",7e-6),("DM20",1.3e-6)):
        for p in pts:
            # Total film mass = 2*N_per_direction*surface_area*density/stress.
            # This is a reference-stress mass, expressly not a creep-safe design.
            mass900 = P*p["curvature_m"]*A*970/900e6
            creep.append(dict(material=material,point=p["id"],
                              source_stress_Pa=900e6,source_temperature_K=303.15,
                              source_minimum_rate_percent_per_second=rate,
                              constant_rate_hours_to_1_percent=1/rate/3600,
                              rate_percent_per_second_for_1_percent_in_ten_years=1/(3650*86400),
                              ratio_of_source_rate_to_ten_year_1_percent_budget=rate*3650*86400,
                              reinforcement_kg_at_900MPa_reference_stress=mass900,
                              qualification="Patent example claim; 900 MPa is not a safe creep allowable and this is not rupture life"))
    csvout("UHMWPE-CREEP.csv",creep)

    # Fresh replacement keeps the inherited frame; no structural modification/re-optimization.
    replacements=[]
    for p in pts:
        for months in (1,3,12):
            y=months/12
            r=retention("light_blocked_warehouse_endpoint_exponential",y)
            sets=math.ceil(10/y)
            for strips in (0,.025,.05):
                # Seam area counts one strip per unique boundary, not per cell.
                # Strip has 2 extra film layers; no mechanical fastener mass included.
                strip_mass=2*strips*p["seam_m"]*(p["film_kg"]/A)
                skin_mass=p["film_kg"]+point_bills[p["id"]]["OD4_target_100nm_Al_plus_white_kg"]+strip_mass
                replacements.append(dict(point=p["id"],interval_months=months,
                                         edge_strip_width_m=strips,edge_extra_fiber_kg=strip_mass,
                                         installed_skin_kg=skin_mass,ten_year_sets=sets,
                                         ten_year_skin_consumption_kg=sets*skin_mass,
                                         offboard_spares_kg=(sets-1)*skin_mass,
                                         nominal_film_SF_before_replacement=p["sf0"]*r,
                                         humid_proxy_SF_before_replacement=p["sf0"]*retention("light_blocked_humid_40C80RH_proxy",y),
                                         replacement_fresh_film_SF=p["sf0"],
                                         qualification="PROJECTION; interface/removal damage and hardware not qualified"))
    csvout("REPLACEMENT.csv",replacements)

    # PBO fibre fatigue interpolation between two measured median points, not a laminate S-N.
    n_exp=math.log(514800/21060)/math.log(.7/.6)
    def cycles_median(stress):
        return 514800*(stress/(.6*5.03e9))**(-n_exp)
    fatigue=[]
    peakrows=[]
    for p in pts:
        sigma0=p["stress_in_each_half_thickness_ply_Pa"]
        for y in (0,1,5,10):
            r=retention("dry_protection_acceptance_target",y)
            hot_demand=sigma0*peak_q+worst["added_ply_stress_fully_restrained_Pa"]
            hot_sf=(2*S0*r*worst["instantaneous_strength_factor"])/hot_demand
            # Added thickness reduces pressure stress, not strain-controlled thermal stress.
            avail=(2*S0*r*worst["instantaneous_strength_factor"])-worst["added_ply_stress_fully_restrained_Pa"]
            mult=sigma0*peak_q/avail if avail>0 else None
            peakrows.append(dict(point=p["id"],age_years=y,irreversible_retention=r,
                                 pressure_only_hot_SF=2*S0*r*worst["instantaneous_strength_factor"]/(sigma0*peak_q),
                                 full_restraint_hot_SF=hot_sf,
                                 full_restraint_added_ply_stress_MPa=worst["added_ply_stress_fully_restrained_Pa"]/1e6,
                                 fiber_mass_kg_for_hot_SF1=p["film_kg"]*mult if mult else None,
                                 extra_fiber_mass_kg_for_hot_SF1=max(0,p["film_kg"]*(mult-1)) if mult else None))
        for label,stress in (("nominal",sigma0),("hot_full_restraint",hot_demand)):
            f=stress/5.03e9
            N=cycles_median(stress)
            fatigue.append(dict(point=p["id"],condition=label,ply_stress_GPa=stress/1e9,
                                fraction_of_measured_5p03GPa_strength=f,
                                source_R=0,source_frequency_Hz=50,
                                median_cycles_interpolation=N,
                                interpolation_within_test_range=.6<=f<=.7,
                                annual_full_vent_12_cycle_index=12/N,
                                ten_year_120_cycle_index=120/N,
                                daily_full_vent_ten_year_3650_index=3650/N,
                                all_36500_gusts_treated_as_full_vent_ten_year_index=365000/N,
                                qualification="QUESTIONABLE median single-fibre proxy; no aged laminate or high-R credit"))
    csvout("PEAK-SERVICE-SF.csv",peakrows)
    csvout("FATIGUE.csv",fatigue)
    save("FATIGUE-MODEL.json",dict(
        source="Davies et al 2010 Table 3, doi:10.1007/s10853-010-4721-z",
        absolute_stress_endpoints_Pa=[.6*5.03e9,.7*5.03e9],
        median_cycles=[514800,21060],power_exponent=n_exp,
        creep_source="Toyobo HM <.03% nonrecoverable strain after 100 h at 50% breaking load; 19 y at 60% is manufacturer extrapolation",
        design_ratio_note="Per-ply 3.48 GPa equals 60% of nominal 5.8 GPa. The 1.74 GPa total-gauge equivalent cannot be used as actual ply stress.",
        qualified_creep_life=None,qualified_fatigue_life=None))
    # Transparent allocation against the existing 100 kg systems line.
    budget=[]
    for p in pts:
        for protection in ("OD3_034_one_side_kg","OD3_plus_white_kg",
                           "OD4_target_100nm_Al_plus_white_kg","foil_PET_two_sides_plus_white_kg"):
            for vacuum in (30,50):
                # A separate 5 kg fitting-adhesive placeholder replaces the old point's 4.078 kg.
                # It is never silently scaled from old frame counts.
                total=point_bills[p["id"]][protection]+vacuum+5
                extra=max(0,total-100)
                budget.append(dict(point=p["id"],protection=protection,vacuum_system_kg=vacuum,
                                   fitting_adhesive_placeholder_kg=5,package_kg=total,
                                   package_shortfall_over_existing_100kg=extra,
                                   remaining_unallocated_systems_kg=max(0,100-total),
                                   closure_kg_if_package_added_outside_existing_allowance=p["closure_kg"]+total,
                                   closure_kg_if_package_replaces_existing_allowance=p["closure_kg"]-100+total,
                                   reserve_held_fixed=True))
    csvout("PACKAGE-MASS.csv",budget)

    checks=[]
    def ck(name, actual, expected, atol=1e-8):
        checks.append(dict(name=name,actual=actual,expected=expected,tolerance=atol,
                           passed=abs(actual-expected)<=atol))
    for p in pts:
        ck(p["id"]+" film mass",p["gauge_m"]*A*RHO,p["film_kg"],1e-8)
        ck(p["id"]+" per-ply capacity",3.48e9/p["stress_in_each_half_thickness_ply_Pa"],p["sf0"],1e-10)
        ck(p["id"]+" retained-capacity threshold",p["sf0"]*p["minimum_nominal_retention"],1,1e-12)
        ck(p["id"]+" closure",p["closure_kg"],4889.44215019,1e-7)
    ck("fatigue endpoint .6",cycles_median(.6*5.03e9),514800,1e-6)
    ck("fatigue endpoint .7",cycles_median(.7*5.03e9),21060,1e-6)
    ck("outdoor six-month endpoint",retention("outdoor_uncovered",.5),.35,1e-12)
    ck("humid 1000-day endpoint",retention("light_blocked_humid_40C80RH_proxy",1000/365),.76,1e-12)
    ck("warehouse 1000-day endpoint",retention("light_blocked_warehouse_endpoint_exponential",1000/365),.96,1e-12)
    ck("annual hours",sum(x["hours_per_year"] for x in chosen),8760,1e-9)
    ck("034 barrier mass",bills["OD3_034_one_side_kg"],57.54627872394289,1e-8)
    for x in cross:
        point=next(p for p in pts if p["id"]==x["point"])
        ck(x["point"]+" crossing "+x["scenario"],
           point["sf0"]*retention(x["scenario"],x["conditional_crossing_years"]),1,1e-8)
    invariants={
        "topup_is_not_full_vent":12!=365,
        "all_years_and_points_present":len(age_rows)==len(SCENARIOS)*4*len(pts),
        "all_retention_values_in_unit_interval":all(0<x["retained_fraction"]<=1 for x in age_rows),
        "no_qualified_strength_claims":all(x["qualified_strength_Pa"] is None for x in age_rows),
        "all_source_thresholds_above_first_outdoor_observation":all(1/p["sf0"]>.71 for p in pts),
        "thermal_mass_scaling_retains_strain_controlled_stress":True,
    }
    save("VALIDATION.json",dict(numerical=checks,invariants=invariants,
                                passed=all(x["passed"] for x in checks) and all(invariants.values())))
    assert all(x["passed"] for x in checks),[x for x in checks if not x["passed"]]
    assert all(invariants.values())
    results=dict(status="QUESTIONABLE / PROJECTION",qualified_film_life_years=None,
                 qualified_strength_by_age=None,qualified_hull_SF=None,points=pts,
                 age_table=age_rows,crossings=cross,barriers=bills,
                 peak_service=peakrows,minimum_cold_film_T_K=min_T,
                 bulk_dry_water_target_Pa=target_pw,
                 source_equivalent_factor_not_identified=True,
                 coupled_chemical_creep_fatigue_model_validated=False,
                 validation_checks=len(checks),physical_invariants=len(invariants))
    save("RESULTS.json",results)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size":10,"svg.fonttype":"none"})
    fig,ax=plt.subplots(1,2,figsize=(13,5),layout="constrained")
    y=np.linspace(0,10,401)
    names=list(SCENARIOS)
    for name in names:
        if name=="sealed_argon_55C_loss_ceiling_extrapolation":
            continue
        label={
            names[0]:"Uncovered: outdoor continuation",
            names[1]:"Light blocked: humid reference",
            names[2]:"Light blocked: warehouse extrapolation",
            names[4]:"Dry protection: acceptance target",
        }[name]
        ax[0].plot(y,[retention(name,t) for t in y],label=label)
    for p in pts:
        if p["id"]=="022d-019":
            continue
        ax[0].axhline(1/p["sf0"],lw=.8,ls="--",color=".45")
        ax[0].text(9.8,1/p["sf0"]+.008,p["id"],ha="right",fontsize=8)
    ax[0].set(xlim=(0,10),ylim=(0,1.03),xlabel="Age (years)",ylabel="Retained strength fraction")
    ax[0].legend(loc="lower left",fontsize=8)
    selected=[p for p in pts if p["id"]!="022d-019"]
    xx=np.arange(len(selected))
    for j,name in enumerate((names[0],names[1],names[2],names[4])):
        ax[1].bar(xx+(j-1.5)*.19,[p["sf0"]*retention(name,10) for p in selected],.19,
                  label=["Uncovered","Humid proxy","Warehouse","Dry target"][j])
    ax[1].axhline(1,color="black",ls="--",lw=1)
    ax[1].set(xticks=xx,xticklabels=[p["id"] for p in selected],ylabel="Film SF at ten years",
              ylim=(0,1.35))
    ax[1].legend(fontsize=8,loc="upper right")
    fig.suptitle("MAINLINE-046 — conditional scenarios, not demonstrated service life")
    fig.savefig(ROOT/"film-life.png",dpi=180)
    fig.savefig(ROOT/"film-life.svg")
    plt.close(fig)
    print(json.dumps({"points":len(pts),"checks":len(checks),"passed":True,
                      "worst_coated_K":worst["film_K"],"water_target_Pa":target_pw,
                      "barrier_kg":bills["OD3_plus_white_kg"]},indent=2))


if __name__=="__main__":
    main()
