#!/usr/bin/env python3
"""Independent MAINLINE-015b arithmetic; never imports or runs owner code."""
import csv
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import dawsn

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / "vacuum-mainline015-check-1019"
R, NU, RETIRED_NU, RETIRED_WIDTH = 10.0, 0.33, 0.30, 2.625
LEVELS = [0.9, 0.7, 0.5, 0.595, 0.468]
COMPARISONS = []


def read(name):
    return json.loads((ROOT / "inputs" / name).read_text())


def write(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def half_up(value, places):
    quantum = Decimal(1).scaleb(-places)
    return format(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP), "f")


def compare(path, reported, checked, category="numeric", atol=2e-12):
    if isinstance(reported, bool) or reported is None:
        okay = reported is checked
        delta = None
    elif isinstance(reported, str):
        okay = reported == checked
        delta = None
    else:
        delta = reported - checked
        okay = math.isclose(reported, checked, rel_tol=5e-12, abs_tol=atol)
    COMPARISONS.append(dict(path=path, reported=reported, checked=checked,
                            reported_minus_checked=delta, category=category, match=okay))


def eq3_alpha(kd):
    return -math.log((kd - 0.45) / 0.51) / 3.88 if kd > 0.45 else None


def lee_alpha(kd):
    return 0.25 / (kd - 0.068) - 0.28


def beta(t, nu=NU, width=1):
    return width * math.sqrt(t / R) / (12 * (1 - nu * nu)) ** 0.25


def level(kd, t):
    b = beta(t)
    a = eq3_alpha(kd)
    if a is None:
        eq = dict(delta_bar=None, amplitude_mm=None, single_dimple_rms_mm=None)
    else:
        amplitude = 1000 * t * a
        rms = amplitude * b / math.sqrt(8)
        legacy = amplitude * beta(t, RETIRED_NU, RETIRED_WIDTH) / math.sqrt(8)
        eq = dict(delta_bar=a, amplitude_mm=amplitude, width_m=R*b,
                  single_dimple_rms_mm=rms,
                  inside_source_small_amplitude_exclusion=a < 0.07,
                  inside_source_R_over_t=100 <= R/t <= 1550,
                  retired_mixed_rms_mm=legacy, retired_over_matched=legacy/rms)
    la = lee_alpha(kd)
    amp = 1000*t*la
    lrms = amp*b/math.sqrt(8)
    return dict(kd=kd, nu=NU, lambda_matched=1.0, eq3=eq,
                lee=dict(delta_bar=la, amplitude_mm=amp,
                         single_dimple_rms_mm_at_k_1=lrms,
                         single_dimple_rms_mm_at_k_5=5*lrms,
                         width_m_at_k_1=R*b, width_m_at_k_5=5*R*b,
                         range=dict(fem_amplitude_at_or_above_0_15=la >= 0.15,
                                    ode_amplitude_at_or_above_0_20=la >= 0.20,
                                    r_over_t_is_100_or_200=R/t in (100, 200),
                                    width_sweep_k=[1.0, 5.0], unique_rms=False)))


def threshold():
    # Reconstruct the former 015 mass/yield/global crossing, independently.
    pressure, lift = 95460.83791390515, 4889.442150186961
    mass = (lift - 100) / 1.05
    area = 4*math.pi*R*R
    density_f, density_c = 1850, 1.6*16.018463373960138
    ef, yield_stress = 303e9, 283e6
    gc, ec, crush = (v*6894.757293168361 for v in (10500, 30000, 50))
    biax = brentq(lambda x: x**3 + x - 1, 0, 1, xtol=1e-15)
    q = math.sqrt(1-NU**2)

    def modes(x, kd):
        tf = mass*(1-x)/(2*area*density_f)
        core = mass*x/(area*density_c)
        h = core+tf
        stress = pressure*R/(4*tf)
        s0 = ef*h/(R*q)
        crimp = gc*h*h/(2*tf*core)
        vc = s0/crimp
        kc = 1-vc/4 if vc <= 2 else 1/vc
        sfs = dict(global_buckling=(kd if vc < 2 else 1)*kc*s0/stress,
                   face_yield=yield_stress/stress, core_shear_crimping=crimp/stress,
                   core_crush=crush/(pressure/2),
                   face_wrinkling=biax*0.33*math.sqrt(ef*ec*tf/core)/stress,
                   intracell_dimpling=2*ef/(1-NU**2)*(tf/0.00635)**2/stress)
        return dict(core_mass_fraction=x, tf_m=tf, core_m=core, Vc=vc,
                    Kc=kc, sfs=sfs, least_SF=min(sfs.values()))

    tf_y = pressure*R/(4*yield_stress)
    x_y = 1-2*area*density_f*tf_y/mass
    kd = 1/modes(x_y, 1)["sfs"]["global_buckling"]
    crossing = modes(x_y, kd)
    a, b = mass/(2*area*density_f), mass/(area*density_c)
    c = ef/(2*gc*R*q)
    c1, c2, c3 = a*(b-2*a)-c*a*a*b, -a*(b-a)+2*c*a*a*b, -c*a*a*b
    derivatives = [c1, c1+2*c2*x_y+3*c3*x_y*x_y]
    grids = {str(k): max((modes(i/8000, k) for i in range(1, 8000)),
                        key=lambda x: x["least_SF"]) for k in (0.518, 0.519)}
    assert min(derivatives) > 0
    assert min(crossing["sfs"].values()) >= 1-1e-12
    assert grids["0.518"]["least_SF"] < 1 <= grids["0.519"]["least_SF"]
    return dict(value=kd, crossing=crossing, grid=grids,
                global_capacity_derivative_endpoints=derivatives,
                inputs=dict(pressure_Pa=pressure, lift_kg=lift, structural_mass_kg=mass,
                            face_density=density_f, core_density=density_c,
                            face_E_Pa=ef, face_yield_Pa=yield_stress,
                            core_Gc_Pa=gc, core_Ec_Pa=ec, core_crush_Pa=crush, nu=NU))


def scalar_paths(value, path=""):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from scalar_paths(item, path+"/"+key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from scalar_paths(item, path+"/"+str(index))
    elif isinstance(value, (int, float)) or value is None:
        yield path, value
    elif isinstance(value, str) and re.fullmatch(r"-?\d+(?:\.\d+)?", value):
        yield path, value


def main():
    owner = read("owner-RESULTS.json")
    old, up21, up21b = (read(n) for n in ("015.json", "021.json", "021b.json"))
    fp21, fp21b = up21["main"]["floating_point"], up21b["floating_point"]
    g21, g21b = fp21["needed_values"]["gamma"], fp21b["needed_values"]["gamma"]
    level_values = dict(zip(map(str, LEVELS), LEVELS))
    level_values.update({"0.5953179642995181": g21, "0.4682285666772076": g21b,
                         "0.3": 0.3, "0.2": 0.2})
    geometries = {"Al-P2-E": old["shells"]["P2-E"],
                  "Be-015": old["shells"]["014b-Be-CRIII-1.6"],
                  "Be-021": fp21, "Be-021b": fp21b}
    thresholds = threshold()
    ratio = RETIRED_WIDTH*((1-NU*NU)/(1-RETIRED_NU**2))**0.25
    expected = dict(schema=1, certification=False, nu_live=NU, nu_retired_audit_only=RETIRED_NU,
                    kd_for_SF_1=dict(value=thresholds["value"], rescored_here=False),
                    range_limits=dict(
                        eq3=dict(lambda_I=1, source_nu=0.5, carried_nu=NU,
                                 R_over_t=[100.0, 1550.0], excluded_delta_over_t_below=0.07,
                                 floor_kd=0.45),
                        lee_23=dict(k=[1.0, 5.0], R_over_t_computed=[100.0, 200.0],
                                    no_FEM_below_delta_over_t=0.15,
                                    no_ODE_below_delta_over_t=0.2, unique_rms=False)),
                    shells={}, gaps_matched_rms_over_GBT_0_25_mm={},
                    display_half_up={}, checks=[])
    supplemental = {}
    for name, geom in geometries.items():
        f, d = geom["tf_m"], geom["core_m"]
        h = f+d
        t = math.sqrt(3)*h
        w = beta(t)*R
        shell = dict(tf_m=f, core_m=d, h_m=h, t_eq_m=t,
                     t_eq_exact_ad_m=math.sqrt(3*h*h+f*f),
                     R_over_t_eq=R/t, nu=NU,
                     length_scale_sqrt_R_t_m=math.sqrt(R*t),
                     classical_wavelength_m=2*math.pi*w,
                     width_lambda_1_m=w, beta0_lambda_1_rad=w/R,
                     levels={key:level(k, t) for key,k in level_values.items()})
        if name in ("Be-021", "Be-021b"):
            shell["filed_gamma"] = g21 if name == "Be-021" else g21b
        expected["shells"][name] = shell
        expected["gaps_matched_rms_over_GBT_0_25_mm"][name] = {
            str(k): dict(matched_rms_over_GBT_0_25mm=shell["levels"][str(k)]["eq3"]["single_dimple_rms_mm"]/0.25,
                         allowance_looser_than_0_25mm=shell["levels"][str(k)]["eq3"]["single_dimple_rms_mm"]>0.25)
            for k in LEVELS}
        display = dict(t_eq_mm=half_up(t*1000, 2), R_over_t=half_up(R/t, 2),
                       width_lambda_1_m=half_up(w, 4),
                       classical_wavelength_m=half_up(2*math.pi*w, 4),
                       sqrt_R_t_m=half_up(math.sqrt(R*t), 4))

        def displays(prefix, values, actual=False):
            eq, lee = values["eq3"], values["lee"]
            fields = dict(eq3_amp_mm=half_up(eq["amplitude_mm"], 3),
                          eq3_rms_mm=half_up(eq["single_dimple_rms_mm"], 4),
                          lee_amp_mm=half_up(lee["amplitude_mm"], 3),
                          lee_rms_k1_mm=half_up(lee["single_dimple_rms_mm_at_k_1"], 4),
                          lee_rms_k5_mm=half_up(lee["single_dimple_rms_mm_at_k_5"], 4),
                          lee_fem=lee["range"]["fem_amplitude_at_or_above_0_15"],
                          lee_ode=lee["range"]["ode_amplitude_at_or_above_0_20"])
            if actual:
                fields["eq3_rms_over_0_25mm"] = half_up(eq["single_dimple_rms_mm"]/0.25, 3)
            else:
                fields["eq3_small"] = eq["inside_source_small_amplitude_exclusion"]
                fields["eq3_in_Rt"] = eq["inside_source_R_over_t"]
            display.update({prefix+"_"+key:value for key,value in fields.items()})

        for k in LEVELS:
            displays("kd_"+str(k), shell["levels"][str(k)])
        if "filed_gamma" in shell:
            displays("filed_gamma", level(shell["filed_gamma"], t), True)
        expected["display_half_up"][name] = display
        # Integrate the spherical area element instead of replacing sin(theta) by theta.
        finite_area = {}
        for width in (1, 5):
            b0 = beta(t, width=width)
            integral, error = quad(lambda u: math.exp(-2*u*u)*math.sin(b0*u)*b0,
                                   0, math.pi/b0, epsabs=1e-14, epsrel=1e-13)
            exact_factor = math.sqrt(integral/2)
            small_factor = b0/math.sqrt(8)
            x = b0/(2*math.sqrt(2))
            dawson_factor = math.sqrt(x*dawsn(x))
            assert abs(exact_factor-dawson_factor) < 1e-13
            finite_area[str(width)] = dict(beta0_rad=b0, exact_RMS_over_amplitude=exact_factor,
                                          small_angle_RMS_over_amplitude=small_factor,
                                          exact_over_approx=exact_factor/small_factor,
                                          approx_overstatement_percent=100*(small_factor/exact_factor-1),
                                          quadrature_absolute_error=error)
        changes = {}
        for short, full in (("0.595", g21), ("0.468", g21b)):
            rounded, actual = level(float(short), t), level(full, t)
            changes[short] = {}
            for model in ("eq3", "lee"):
                av, rv = actual[model]["amplitude_mm"], rounded[model]["amplitude_mm"]
                changes[short][model] = dict(actual_gamma=full, rounded_amplitude_mm=rv,
                                             actual_amplitude_mm=av,
                                             rounded_minus_actual_mm=rv-av,
                                             excess_relative_to_actual_percent=100*(rv/av-1))
        supplemental[name] = dict(
            finite_spherical_area=finite_area,
            exact_RMS_k5_over_k1=finite_area["5"]["exact_RMS_over_amplitude"]/finite_area["1"]["exact_RMS_over_amplitude"],
            rounding_changes=changes, effective_modulus_over_face_E=2*f/t,
            finite_face_thickness_over_thin_face=shell["t_eq_exact_ad_m"]/t,
            Lee_radius_position="outside_computed_interval" if R/t<100 or R/t>200 else "between_computed_radii")

    for item in owner["checks"]:
        name = item["name"]
        value = None
        if name == "live map uses one nu":
            okay = all(s["nu"] == NU for s in expected["shells"].values())
        elif name.startswith("retired mix over live"):
            value, okay = ratio, True
        elif name == "Eq 3 does not invert 0.2 or 0.3":
            okay = all(eq3_alpha(k) is None for k in (0.2, 0.3))
        elif name == "Lee inverse round-trips":
            okay = all(abs(0.068+0.25/(0.28+lee_alpha(k))-k)<1e-14 for k in level_values.values())
        elif name.startswith("check Lee delta/t"):
            value, okay = lee_alpha(float(name.split()[-1])), True
        elif name.startswith("check "):
            m = re.fullmatch(r"check (amplitude|matched RMS|Lee amplitude) (Al-P2-E|Be-015) kd (.*)", name)
            assert m, name
            kind, shellname, key = m.groups()
            lev = expected["shells"][shellname]["levels"][key]
            value = lev["lee" if kind=="Lee amplitude" else "eq3"][
                "single_dimple_rms_mm" if kind=="matched RMS" else "amplitude_mm"]
            okay = True
        elif name.startswith("015 card"):
            m = re.search(r"(Al-P2-E|Be-015) (0\.\d+)$", name)
            shellname, key = m.groups()
            val = expected["shells"][shellname]["levels"][key]["eq3"][
                "retired_mixed_rms_mm" if "RMS" in name else "amplitude_mm"]
            places = len(item["got"].split(".")[1]) if "." in item["got"] else 0
            value, okay = half_up(val, places), True
        elif name.startswith(("021 ", "021b ")):
            shellname = "Be-021b" if name.startswith("021b") else "Be-021"
            shell = expected["shells"][shellname]
            lev = level(shell["filed_gamma"], shell["t_eq_m"])["eq3"]
            value = lev["retired_mixed_rms_mm" if "RMS" in name else "amplitude_mm"]
            okay = True
        else:
            raise ValueError(name)
        row = {"pass":okay}
        if "got" in item:
            row["got"] = value
        expected["checks"].append(row)

    target_paths, expected_paths = dict(scalar_paths(owner)), dict(scalar_paths(expected))
    missing = sorted(set(target_paths)-set(expected_paths))
    extra = sorted(set(expected_paths)-set(target_paths))
    assert not missing, missing
    assert not extra, extra
    for path, value in target_paths.items():
        category = ("display" if path.startswith("/display_half_up/") else
                    "owner_check" if path.startswith("/checks/") else
                    "boolean" if isinstance(value, bool) else
                    "null" if value is None else "numeric")
        compare(path, value, expected_paths[path], category,
                atol=5e-11 if path=="/kd_for_SF_1/value" else 2e-12)

    # Read displayed CARD tables directly, rather than only checking its JSON.
    card = (ROOT/"inputs"/"owner-CARD.md").read_text()
    report = read("rpt-ref-74e882831c201b1a953c.json")["body"]
    prose_audit = []

    def excerpt_claim(container, excerpt, values, label):
        # Values: (literal printed token, independently computed quantity).
        for literal, value in values:
            places = len(literal.split(".")[1]) if "." in literal else 0
            compare(label+"/"+literal, literal, half_up(value, places), "prose")
        assert excerpt in container, (label, excerpt)
        prose_audit.append(dict(label=label, verbatim_excerpt=excerpt, values_recomputed=len(values)))

    segments = card.split("## ")
    for name, heading in (("Al-P2-E","Al point, P2-E"), ("Be-015","Be point, frozen 014b")):
        segment = next(s for s in segments if s.startswith(heading))
        table = [line for line in segment.splitlines() if re.match(r"\| 0\.", line)]
        assert len(table)==5
        for line in table:
            cells = [s.strip() for s in line.split("|")[1:-1]]
            kd, *printed = cells
            lev = expected["shells"][name]["levels"][kd]
            values = [lev["eq3"]["amplitude_mm"], lev["eq3"]["single_dimple_rms_mm"],
                      lev["lee"]["amplitude_mm"], lev["lee"]["single_dimple_rms_mm_at_k_1"]]
            for j,(literal,value) in enumerate(zip(printed,values)):
                compare("CARD/table/"+name+"/"+kd+"/"+str(j), literal,
                        half_up(value, (3,4,3,4)[j]), "card_table")
            prose_audit.append(dict(label="CARD table "+name+" "+kd, verbatim_excerpt=line,
                                    values_recomputed=4))
    for name in geometries:
        sh = expected["shells"][name]
        tf, co, te, rt = half_up(sh["tf_m"]*1000,6), half_up(sh["core_m"]*1000,3), half_up(sh["t_eq_m"]*1000,2), half_up(sh["R_over_t_eq"],2)
        phrase = f"tf {tf} mm, core {co} mm, t_eq {te} mm, R/t {rt}"
        excerpt_claim(card, phrase, [(tf,sh["tf_m"]*1000),(co,sh["core_m"]*1000),
                                     (te,sh["t_eq_m"]*1000),(rt,sh["R_over_t_eq"])], "CARD geometry "+name)
        if name in ("Al-P2-E","Be-015"):
            for k in (0.3,0.2):
                amp = sh["levels"][str(k)]["lee"]["amplitude_mm"]
                literal = half_up(amp,3)
                excerpt_claim(card, literal+" mm", [(literal,amp)], "CARD Lee "+name+" "+str(k))
            for field,label in (("width_lambda_1_m","Lambda-1 width"),("classical_wavelength_m","Classical wavelength")):
                val=sh[field]
                literal=half_up(val,4)
                excerpt_claim(card, label+" "+literal+" m",[(literal,val)],"CARD "+name+" "+field)
            if name=="Al-P2-E":
                val=sh["length_scale_sqrt_R_t_m"]
                excerpt_claim(card, "Length scale "+half_up(val,4)+" m",
                              [(half_up(val,4),val)],"CARD length scale")
        else:
            lev = level(sh["filed_gamma"],sh["t_eq_m"])
            eq,le = lev["eq3"],lev["lee"]
            for val,places in ((sh["filed_gamma"],None), (eq["amplitude_mm"],3),
                               (eq["single_dimple_rms_mm"],4), (le["amplitude_mm"],3),
                               (le["single_dimple_rms_mm_at_k_1"],4),
                               (le["single_dimple_rms_mm_at_k_5"],4)):
                literal = str(val) if places is None else half_up(val,places)
                excerpt_claim(card, literal, [(literal,val)],"CARD floating "+name)
            old_places = 4 if name=="Be-021" else 3
            literal=half_up(eq["retired_mixed_rms_mm"],old_places)
            excerpt_claim(card, "RMS "+literal+" mm", [(literal,eq["retired_mixed_rms_mm"])],
                          "CARD retired "+name)
            actualratio=eq["single_dimple_rms_mm"]/0.25
            excerpt_claim(card, half_up(actualratio,3)+" times",[(half_up(actualratio,3),actualratio)],
                          "CARD comparison "+name)
            # Report prints gamma to 5 decimals and the other fields as the CARD.
            for val,places in ((sh["filed_gamma"],5),(sh["t_eq_m"]*1000,2),
                               (eq["amplitude_mm"],3),(eq["single_dimple_rms_mm"],4),
                               (eq["retired_mixed_rms_mm"],old_places),
                               (le["amplitude_mm"],3),
                               (le["single_dimple_rms_mm_at_k_1"],4),
                               (le["single_dimple_rms_mm_at_k_5"],4)):
                literal=half_up(val,places)
                excerpt_claim(report,literal,[(literal,val)],"REPORT floating "+name)
    for name in ("Al-P2-E","Be-015"):
        sh=expected["shells"][name]
        for k in LEVELS:
            e=sh["levels"][str(k)]["eq3"]
            phrase=f"{k}: {half_up(e['amplitude_mm'],3)}, {half_up(e['single_dimple_rms_mm'],4)}."
            excerpt_claim(report,phrase,[(half_up(e["amplitude_mm"],3),e["amplitude_mm"]),
                                        (half_up(e["single_dimple_rms_mm"],4),e["single_dimple_rms_mm"])],
                          "REPORT table "+name+" "+str(k))
        le=sh["levels"]["0.5"]["lee"]
        for value,places in ((sh["t_eq_m"]*1000,2),(le["amplitude_mm"],3),
                             (le["single_dimple_rms_mm_at_k_1"],4)):
            literal=half_up(value,places)
            excerpt_claim(report,literal,[(literal,value)],"REPORT Lee/geometry "+name)
        comparison=sh["levels"]["0.9"]["eq3"]["single_dimple_rms_mm"]/0.25
        literal=half_up(comparison,3)
        excerpt_claim(card,literal+" times",[(literal,comparison)],"CARD GBT "+name)
    legacy_ratio=expected["shells"]["Al-P2-E"]["levels"]["0.9"]["eq3"]["retired_mixed_rms_mm"]/0.25
    excerpt_claim(card,"1.82 times looser",[("1.82",legacy_ratio)],"CARD old ratio")
    for label,text in (("CARD",card),("REPORT",report)):
        excerpt_claim(text,"0.5183040769",[("0.5183040769",thresholds["value"])],label+" continuous threshold")
        excerpt_claim(text,"2.611 times",[("2.611",ratio)],label+" retired ratio")

    pins=[]
    for manifest in (read("pin-audit.json"),read("upstream-pins.json"),
                     json.loads((OLD/"sources"/"manifest.json").read_text())):
        for item in manifest:
            p=Path(item["path"])
            raw=p.read_bytes()
            digest=hashlib.sha256(raw).hexdigest()
            match=digest==item["sha256"] and len(raw)==item["bytes"]
            pins.append(dict(path=str(p),sha256=digest,bytes=len(raw),match=match))
            assert match,p
    write("SOURCE-PINS.json",pins)
    write("PROSE-CHECK.json",prose_audit)
    counts=Counter(row["category"] for row in COMPARISONS)
    mismatches=[r for r in COMPARISONS if not r["match"]]
    results=dict(schema=1,unit="vacuum-mainline015b-check-1020",
                 tag="QUESTIONABLE",certification=False,
                 started_at=read_work()["started_at"],
                 calculated_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds"),
                 independent_method="Equations derived from primary papers and spherical Gaussian integration; geometry and gamma read as inputs from pinned upstream data. No owner code read or run.",
                 declared_tolerances=dict(raw_relative=5e-12,raw_absolute=2e-12,
                                          truncated_threshold_absolute=5e-11,decimal_displays="exact ROUND_HALF_UP"),
                 numeric_leaf_coverage=dict(owner_scalar_leaves=len(target_paths),covered=len(expected_paths),
                                            missing=missing,extra=extra),
                 comparison_counts=dict(counts),comparison_total=len(COMPARISONS),
                 mismatches=mismatches,threshold=thresholds,retired_over_live_ratio=ratio,
                 independently_derived=expected,supplemental=supplemental,
                 scope="Every numeric/boolean/null leaf of owner RESULTS and engineering displays checked. IDs, paper/equation labels and timestamps are metadata. Upstream optimisations 021/021b are inputs, not rescored.",
                 foreign_scripts_read_or_executed=False,all_pins_match=all(p["match"] for p in pins))
    write("RESULTS.json",results)
    with (ROOT/"NUMERIC-CHECK.csv").open("w",newline="") as stream:
        out=csv.DictWriter(stream,fieldnames=list(COMPARISONS[0]))
        out.writeheader()
        out.writerows(COMPARISONS)
    print(json.dumps(dict(counts=dict(counts),total=len(COMPARISONS),mismatches=mismatches,
                          threshold=thresholds["value"],supplemental=supplemental),indent=2))
    assert not mismatches


def read_work():
    return json.loads((ROOT/"WORK.json").read_text())


if __name__ == "__main__":
    main()
