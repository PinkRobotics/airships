#!/usr/bin/env python3
"""Render the scientific report and evidence ledger from the frozen calculation."""
import csv
import json
from pathlib import Path

R = Path(__file__).resolve().parent
D = json.loads((R/"RESULTS.json").read_text())
PTS = {p["id"]:p for p in D["points"]}


def rows(name):
    return list(csv.DictReader((R/name).open()))


def write(name,text):
    (R/name).write_text(text.strip()+"\n")


def save(name,obj):
    (R/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+"\n")


TOYOBO="https://www.toyobo-global.com/seihin/kc/pbo/zylon-p/bussei-p/technical.pdf"
NIST="https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=860679"
FATIGUE="https://doi.org/10.1007/s10853-010-4721-z"
COATING="https://doi.org/10.1038/s41598-019-45199-8"
NIJ="https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7627.pdf"
UHMWPE="https://doi.org/10.1016/j.polymdegradstab.2015.01.028"
KEVLAR="https://www.r-g.de/wiki/images/e/ec/Td_en_Kevlar_guide.pdf"
DYNEEMA="https://www.dyneema.com/design-with-dyneema/dyneema-product-portfolio"
PATENT="https://patentimages.storage.googleapis.com/6e/89/bd/f4165a0c295be7/US20180112336A1.pdf"

evidence=[
 dict(id="PBO-light-outdoor",source=TOYOBO,file="sources/toyobo2005.pdf",page=12,
      specimen="HM yarn; AS plotted separately",conditions="45 degrees south, Ohtsu Japan, June-November 1997",
      duration_days=182.5,retention_approx=.35,
      points_months=[0,.5,2.25,4,6],HM_retention_readings=[1,.71,.44,.335,.35],
      limits="Manual ±0.02 readings. Solar spectrum/dose, load and detailed humidity absent. Half-month is first nonzero observation."),
 dict(id="PBO-visible",source=TOYOBO,file="sources/toyobo2005.pdf",page=12,
      conditions="Two 35 W fluorescent lamps; 150 cm distance; irradiance not stated",
      duration_hours=720,retention_approx_HM=.73,retention_approx_AS=.65,
      limits="Visible light also matters; lamp power cannot be converted to fibre irradiance without geometry/spectrum."),
 dict(id="PBO-hot-humid",source=TOYOBO,file="sources/toyobo2005.pdf",page=9,
      specimen="AS 555 dtex for long series",conditions="40 C, 80% RH; dark environmental exposure",
      days=[0,20,50,100,200,400,600,800,1000],
      retention_approx=[1,.965,.94,.90,.86,.83,.80,.78,.76],
      limits="Manual ±0.02 readings; transfer to HM, loaded 0/90 membrane and variable service climate unvalidated."),
 dict(id="PBO-warehouse",source=TOYOBO,file="sources/toyobo2005.pdf",page=9,
      specimen="AS 555 dtex",conditions="Room temperature and humidity at warehouse; numeric climate not specified on plot",
      duration_days=1000,retention_approx=.96,
      limits="Curve has early loss then a flatter tail; an endpoint exponential is not a fit to its entire shape."),
 dict(id="PBO-steam",source=TOYOBO,file="sources/toyobo2005.pdf",page=9,
      conditions="Saturated steam, 180 C",duration_hours=50,retention_range=[.4,.5],
      limits="Not an activation-energy calibration for service near ambient."),
 dict(id="PBO-temperature-at-test",source=TOYOBO,file="sources/toyobo2005.pdf",page=10,
      conditions="Tensile test at temperature; instantaneous reversible contribution",
      interpolation_used="1 at 20 C; approximately .9 at 100 C, graph read; linear screening interpolation",
      limits="About ±0.02 graph uncertainty; does not describe permanent aging."),
 dict(id="NIST-PBO-humidity",source=NIST,file="sources/chin2007.pdf",
      identity="NISTIR 7373 (April 2006), not the subsequent 2007 journal PDF",page=26,
      specimen="20-layer woven armor in water-vapor-permeable liner and cotton carrier; extracted yarn",
      conditions="50 C/60% RH for 84 days, then 60 C/37% RH for 73 days; constant absolute humidity intent",
      days=[0,15,29,44,56,71,85,98,109,118,132,146,152,157],
      strengths_GPa=[4.82,4.45,4.18,4.02,3.88,3.80,3.64,3.50,3.57,3.51,3.30,3.23,3.30,3.08],
      relative_standard_uncertainty_strength=.03,
      limits="Table reports .639 retention at day 157; round prose/abstract percentages differ. No single-temperature PBO Arrhenius constant is inferred."),
 dict(id="NIST-PBO-protected",source=NIST,file="sources/chin2007.pdf",pages=[10,11,23],
      specimen="Yarn in evacuated, argon-backfilled, heat-fused glass tubes",conditions="55 C oven",
      duration_days=210,retention_greater_than=.96,
      additional_result="Previously humid-aged vest yarn showed no further measured loss during 332 days at 25 C/5% RH.",
      limits="Glass/argon protection is not a 12 um polymer laminate; remaining moisture and uncertainty matter."),
 dict(id="PBO-coating",source=COATING,file="sources/pbo-coating-published.pdf",
      conditions="QUV/spray 340 nm, 50 C, 400 h; irradiance not specified in retrieved experimental description",
      uncoated_retention=.214,coated_retention=.53,optimized_three_coat_retention=.59,
      coating="KH-560-functionalized PBO with fluorosilane HFTES, UV-328 and silicone-modified epoxy/polyamide system",
      limits="Improvement is partial; no transferable 10-year result or installed g/m2 bill."),
 dict(id="PBO-creep",source=TOYOBO,file="sources/toyobo2005.pdf",page=5,
      specimen="HM yarn",conditions="50% breaking load, 100 hours; test climate unspecified on this page",
      nonrecoverable_strain_less_than=.0003,
      prediction="Manufacturer extrapolates 10^7 minutes (about 19 years) at 60% breaking load",
      limits="Nineteen years is extrapolated, not an observed runout; no aged crossply attachment qualification."),
 dict(id="PBO-fatigue",source=FATIGUE,file="sources/pbo-fatigue.pdf",
      specimen="HM single filaments, 50 mm gauge; measured mean strength 5.030 ± .750 GPa",
      conditions="50 Hz, R=0 tensile cycling",
      stress_fraction_of_measured_strength=[.60,.70],median_cycles=[514800,21060],sample_count=[7,30],
      limits="Median, not allowable or low-tail reliability. Test stresses 3.018/3.521 GPa. No high-R aged laminate curve."),
 dict(id="PBO-folding",source="https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=902527",
      file="sources/nist-folding.pdf",
      conditions="Modified single-fibre tests following folding",
      results="One fold reduced ultimate strength and strain to failure about 10%; repeated-folding comparisons reported 15%/40% changes in strain to failure.",
      limits="Strain-to-failure reductions are not silently relabelled retained tensile strength; body-armor use-time equivalence is not P3 life."),
 dict(id="PBO-PPTA-combined",source=NIJ,file="sources/nij-conditioning.pdf",
      conditions="Phase II: 35-65 C twice daily, 75% RH reduced to 65% on cooling; 40 rpm tumbling 2 h twice weekly, six weeks",
      PBO_all_conditions_retention=.58,PBO_humidity_temperature_only_retention=.80,
      PPTA_result="No measured reduction in this phase; other phases differed",
      limits="Synergy prevents assuming independent damage products are validated. NIJ protocol is not a known number of field-service years."),
 dict(id="Kevlar49",source=KEVLAR,file="sources/kevlar-guide-mirror.pdf",
      authorship="DuPont primary technical guide, retrieved via distributor mirror after official URLs failed",
      density_kg_m3=1440,conditioned_yarn_strength_GPa=3.0,
      neutral_pH_result="Near-unchanged filament tenacity after more than 200 days at 65 C and pH 7",
      light_result="Protection needed against roughly 300-450 nm; yarn/fabric size affects self-shielding",
      limits="95% retention at ten years is an imposed option requirement, not a sourced forecast; moisture regain and finished laminate not in dry-fibre mass."),
 dict(id="UHMWPE-aging",source=UHMWPE,file="sources/uhmwpe-aging.pdf",
      conditions="43,65,90,115 C; dark oxidative aging of ballistic yarn",
      activation_energy_J_mol=140000,predicted_years_to_70pct_at_43C=36,
      limits="Authors' time-temperature-superposition projection; higher-temperature physical changes complicate interpretation. Grade not established as SK75/SK99/DM20."),
 dict(id="UHMWPE-strength",source=DYNEEMA,file="sources/dyneema-portfolio.html",
      SK99_tenacity_cN_dtex=42.5,SK99_modulus_cN_dtex=1590,
      assumptions="970 kg/m3 generic UHMWPE density; same unqualified 60% efficiency and two directions as inherited PBO screen",
      limits="Current supplier property is not a sustained-load allowable."),
 dict(id="UHMWPE-creep",source=PATENT,file="sources/uhmwpe-creep-patent.pdf",pdf_page=12,
      paragraphs=["0099","0106","0107"],conditions="900 MPa, 30 C, minimum creep rate",
      SK99_rate_percent_per_second=7e-6,DM20_rate_percent_per_second=1.3e-6,
      DM20_tenacity_cN_dtex=32,
      limits="Manufacturer patent example claims, graph/page verified. Not a rupture-life calibration or a permissible service stress."),
 dict(id="034-barrier",source="sources/barrier-flex-pack-films-2001.pdf",
      authorship="DuPont Teijin Films primary packaging comparison sheet, frozen via CHECK034",
      specimen="12 um OD3 metallized Mylar",
      water_g_m2_day_less_than=1,water_conditions="38 C, 90% RH",
      oxygen_cc_m2_day=.5,oxygen_conditions="25 C,45% RH,100% oxygen",
      limits="Unflexed coupon transmission, not installed RH or aged seam durability. OD3 is not a measured broadband spectrum."),
]
save("SOURCE-DATA.json",{"classification":"QUESTIONABLE evidence transfer; measured source results distinguished from PROJECTION",
                         "entries":evidence})

nfi_text=[
 ("Finished material","PBO filament/yarn evidence does not qualify 0/90 laminate, areal weight, transverse/shear response, load sharing, seam peel, attachment or large-area flaws.",
  "Test both directions and finished seams under biaxial sustained pressure; establish lot-specific lower-tail allowables."),
 ("Grade transfer","40 C and warehouse long curves are AS; the density/modulus point is HM. NIST yarn and local sourcing are not identified as the actual product.",
  "Identify grade, finish, resin, supplier lot and manufacture process; repeat matched retention tests."),
 ("PBO kinetics","No validated combined humidity-temperature-light-load aging law or low-temperature activation energy is available in the retrieved evidence.",
  "Use multiple controlled temperatures, activities, doses and service exposures; validate accelerated-to-service transfer."),
 ("Tail shape","Exponential, stretched and plateau tails are not distinguished by limited observations. The requested 5/10-year outputs are scenarios.",
  "Extend natural exposure and check model selection against held-out time points; keep qualified ages null."),
 ("Annual climate","031 specifies weather states, not an annual probability distribution. Counts, sunlight hours and spectral fractions here are declared assumptions.",
  "Specify location, season, mission duty, altitude control, terrain and measured weather/light dose."),
 ("Light barrier","OD3 visible designation and assumed metal gauge do not establish broadband UV/visible transmission or protection of edges, cracks and repairs.",
  "Demonstrate local worst-spot OD4 or better across the damaging spectrum after cycling; cover and inspect every seam."),
 ("Dose reciprocity","Transferring outdoor calendar time to attenuated photons assumes unknown spectral/dose reciprocity. Outdoor source includes other aging agents.",
  "Measure low-flux kinetics and humidity synergy; do not count the light table as a life prediction."),
 ("Water microclimate","A low bulk vacuum-water pressure does not prove low activity inside resin, fibres, edges or a laminate sandwich.",
  "Measure moisture sorption, diffusion and water activity in the actual laminate; provide dry conditioning and residual-water acceptance."),
 ("Daily drying","034 water upper envelope exceeds the 5% RH budget on the chosen cold patch; initial fibre moisture can consume that budget alone.",
  "Verify <=0.805 g/m2/day at the chosen 041 conditions or shorten/regulate drying; include all water sources and cold-patch sensitivity."),
 ("Barrier aging","Pinholes, flex cracking, rain, erosion, UV embrittlement, foil corrosion and seal peel can remove protection before fibre strength changes.",
  "Age complete curved bays, with wet exterior and vacuum interior; leak and optical tests before/after cycling."),
 ("Coating performance","25 g/m2 white coating is a mass target, not proof of 037 alpha=.2/epsilon=.9 or ten-year adhesion.",
  "Identify and weigh a qualified construction; measure aged optical properties and outgassing."),
 ("Thermal restraint","No installed membrane stress-free temperature, interply constraint or frame-film temperature solution is measured.",
  "Solve/test coupled pressure-membrane thermal equilibrium; distinguish full restraint from free sliding and wrinkling."),
 ("Instantaneous temperature","Approximate HM hot-strength graph interpolation has reading/grade uncertainty comparable with the small SF margin.",
  "Measure finished-laminate hot allowable at the peak temperature and moisture condition."),
 ("Creep and shape","Toyobo's 19-year/60% value is an extrapolation. Creep changes sag volume, membrane curvature, buoyancy and seam forces.",
  "Measure long-duration biaxial creep/rupture and geometry on protected aged bays; set a permissible sag/strain limit."),
 ("Fatigue","Two single-filament median R=0 points do not establish high-R gust endurance, folded-seam life, low-tail reliability or aged interaction.",
  "Obtain matched laminate/termination S-N and creep-fatigue data under the declared service spectrum."),
 ("Loss-budget proof","0.5% annual total loss is a requirement; source uncertainty around 2-3 percentage points cannot verify that rate.",
  "Define sufficient sample size, confidence/tolerance bounds, controls and a service witness/replacement trigger."),
 ("Alternative fibres","Kevlar ten-year .95 is a requirement; UHMWPE uses another yarn's oxidative-aging law. Neither includes installed creep/hot/UV performance.",
  "Test actual alternate grade/laminate; do not combine SK99 specific strength with an unrelated zero-creep claim."),
 ("UHMWPE creep","SK99/DM20 patent rates at 900 MPa/30 C show why a chemically retained high strength is not ten-year dimensional stability.",
  "Obtain grade-specific stress/temperature/strain-limit maps and a permissible membrane stress; 900 MPa is not approved."),
 ("Mass closure","Both P3 points have zero unallocated closure mass. Barrier, coating and systems allocation exceed 100 kg in the worked white-coated bill.",
  "Reclose the entire vehicle with measured masses; preserve required reserve and rerun frame/joint modes."),
 ("Seam/repair bill","034's 5 kg seam allowance is scaled by length, not weighed. Extra sag area, trim, fasteners, joints, patches, inspection fittings and redundancy remain.",
  "Produce a complete bay BOM and scalable seam/removal design; account for overlap and repair overhead."),
 ("Replacement interface","Annual renewal does not reset frame fatigue, bonds, pads or joints; peeling and reattachment can damage the pressure boundary.",
  "Demonstrate repeated bay replacement, reproof, drying and leak tests with the actual supporting frame."),
 ("Qualified lifetime","No retrieved evidence establishes even a one-year installed film allowable or a qualified ten-year architecture.",
  "Keep qualified life/SF null; treat one-year protected replacement only as a planning candidate until accepted evidence exists."),
]
save("NFI.json",dict(status="OPEN / QUESTIONABLE",
                     new=[dict(id=f"046-{i:02d}",topic=t,finding=f,needed=n) for i,(t,f,n) in enumerate(nfi_text,1)],
                     inherited_pinned_registers=["inputs/022d/NFI.json","inputs/022d-check/NFI.json",
                                                "inputs/041/NFI.json","inputs/031/NFI.json",
                                                "inputs/034/NFI.json","inputs/037/NFI.json"],
                     inherited_effect="No upstream ceramic, frame, joint, atmosphere or gas qualification is closed by this film study.",
                     blocking_of_this_research_card=False))

labels={
 "outdoor_uncovered":"Uncovered, outdoor continuation",
 "light_blocked_humid_40C80RH_proxy":"Light blocked, humid reference",
 "light_blocked_warehouse_endpoint_exponential":"Light blocked, warehouse exponential",
 "sealed_argon_55C_loss_ceiling_extrapolation":"Glass/argon loss-ceiling sensitivity",
 "dry_protection_acceptance_target":"Dry protection acceptance target",
}
primary=["022d-5","041-5","041-019"]
point_table="\n".join(
 f"| {p} | {PTS[p]['gauge_m']*1e6:.3f} | {PTS[p]['film_kg']:.3f} | {PTS[p]['sf0']:.6f} | {PTS[p]['minimum_nominal_retention']:.4%} | {PTS[p]['stress_in_each_half_thickness_ply_Pa']/1e9:.3f} |"
 for p in primary)
age_table=[]
for sc,label in labels.items():
    if sc=="sealed_argon_55C_loss_ceiling_extrapolation":
        continue
    for y in (1,5,10):
        vals=[next(x for x in D["age_table"] if x["point"]==p and x["scenario"]==sc and x["age_years"]==y) for p in primary]
        age_table.append(f"| {label} | {y} | {vals[0]['retained_fraction']:.4f} | {vals[0]['effective_total_gauge_strength_GPa']:.4f} | "+
                         " | ".join(f"{x['film_SF']:.4f}" for x in vals)+" |")
cross_table=[]
for sc,label in labels.items():
    if sc=="dry_protection_acceptance_target":
        continue
    vals=[next(x for x in D["crossings"] if x["point"]==p and x["scenario"]==sc) for p in primary]
    cross_table.append("| "+label+" | "+" | ".join(f"{x['conditional_crossing_years']:.3f}" for x in vals)+" |")
alt_table=[]
for x in rows("ALTERNATE-FIBRES.csv"):
    if x["point"]=="041-5":
        alt_table.append("| "+x["material"].replace("protected_","").replace("_"," ")+" | "+
                         " | ".join(f"{float(x[k]):.3f}" for k in
                          ("retention_at_ten_years","same_reinforcement_mass_ten_year_SF",
                           "fiber_kg_for_ten_year_nominal_SF1","fiber_kg_to_restore_initial_SF_at_ten_years"))+" |")
barrier_table=[]
for x in rows("POINT-BARRIERS.csv"):
    if x["point"] in primary:
        barrier_table.append("| "+x["point"]+" | "+" | ".join(f"{float(x[k]):.3f}" for k in
                             ("OD3_only_kg","OD3_white_kg","OD4_white_kg","dual_foil_white_kg"))+" |")

write("CARD.md",f"""
# MAINLINE-046 — P3 film life under moisture, light, heat and load

**QUESTIONABLE / PROJECTION throughout. Neither a one-year nor a ten-year installed film life is demonstrated.**
Uncovered Zylon is unsuitable for a one-year outdoor planning interval. A protected, conditioned,
inspectable film with renewal at at most one year is the defensible **planning candidate**, conditional on
qualification; that interval is not an approved service life.

For a single ten-year skin, retain PBO as the leading development route: verified broadband light exclusion,
dry fibre microclimate, thermal control and a measured combined retained-strength floor.
The arithmetic does **not** establish a globally lightest qualified solution. SK99 is lighter on static
chemistry-only assumptions, but the sustained-load evidence does not support that ten-year claim.
No barrier restores strength already lost; replacement restores the assumed initial film strength.

The dispatch requires both 022d and 041. These are the actual selected continuum point and the two
resized frequency-5 witnesses, not the obsolete 1.417 film factor from 034.

| Point | Both plies, µm | Reinforcement kg | Initial film SF | Retention required for nominal SF 1 | Actual stress per ply, GPa |
|---|---:|---:|---:|---:|---:|
{point_table}

022d's 019-reserve comparison is also calculated: initial film SF 1.194121, required retention
83.7436%, 202.006 kg reinforcement. All four witnesses are in POINTS and every CSV.
The scalar **1.74 GPa is a total-gauge equivalent**: each t/2 ply uses 3.48 GPa, which is
60% of the nominal 5.8 GPa filament strength. This distinction is essential for creep and fatigue.
Both plies are charged. These are inherited screening factors, not qualified allowables.

**Measured record and its limits**

The following are source observations or the source author's explicitly labelled extrapolation.
SOURCE-DATA.json records specimen, condition, duration, readings, uncertainty and URL; source copies are pinned.

| Exposure / form | Result used | Meaning for P3 |
|---|---|---|
| Outdoor HM/AS yarn, Ohtsu, 45° south, June–November 1997 | About 35% strength after six months; HM first half-month point about 71% | First observation already below all four P3 retention thresholds |
| Visible light, two 35 W fluorescent lamps, 1.5 m, 720 h | About 73% HM / 65% AS retained | UV-only protection is insufficient |
| Dark AS yarn, 40°C/80% RH, 1000 days | About 76%; warehouse curve about 96% | Grade and service-climate transfer remain projections |
| HM creep | <0.03% irreversible strain after 100 h at half breaking load; 19 years at 60% is extrapolated | No observed nineteen-year runout |

These observations come from [Toyobo's 2005 technical information]({TOYOBO}), pp.5,9,12.
Its p.10 hot-strength graph also motivates the separate instantaneous temperature sensitivity.

[NISTIR 7373]({NIST}) tested woven PBO armor inside a vapor-permeable liner and cotton carrier.
The table gives 4.82→3.64 GPa over approximately 84 days at 50°C/60% RH, then 3.08 GPa at
157 days after switching to 60°C/37% RH. That is 63.9% of the starting yarn value.
Previously aged yarn showed no further measured loss during 332 days at 25°C/5% RH.
Fresh yarn in heat-fused, argon-filled glass tubes at 55°C lost less than 4% over 210 days.
Glass protection is evidence that environment control matters, not a qualified polymer-laminate design.

A [fluorosilane/UV-absorber coating study]({COATING}) used 340 nm exposure at 50°C for 400 h.
Uncoated retention was 21.4%, one coated construction 53%, and an optimized three-coat construction 59%.
No usable installed coating mass or ten-year conversion follows from that result.
The [NIST conditioning study]({NIJ}) found approximately 58% PBO retention after six weeks combining
35–65°C cycling, humidity and tumbling, compared with about 80% for humidity/temperature alone.
It explicitly does not equate conditioning duration to a known field lifetime.

**A declared service year**

031 provides weather states, not annual frequencies. This calculation assigns 305 nominal days
(284.9 K, 1 kPa water), 50 optimistic hot/wet days (294.9 K, 1 kPa), and 10 conservative hot/wet days
(310 K, 6 kPa). Their ambient RH is 72.5%, 38.4% and 96.3%. The wet baseline uses 034's
water assumption; the two warm states come from 031. These frequencies are a PROJECTION.

A sun-facing patch gets six equivalent full-sun hours daily, six shaded daylight hours, and twelve
night hours: 2,190 full-sun-equivalent hours/year at 037's 970 W/m², or **7.647 GJ/m²/year**.
Assuming 5% UV and 45% visible gives 0.382 and 3.441 GJ/m²; those spectral fractions are
unmeasured. Sphere-average intercepted energy is different. No source Ohtsu dose exists to equate
these joules to that outdoor test.

The thin-film heat balance uses 037's white optical target α=0.20, ε=0.90 and its sky-temperature
offsets, with assumed exterior h=5 W/(m² K). Film temperatures are 274.0–299.7 K on the nominal
day and peak at **321.94 K (48.79°C)** on the hot day. An h=2–10 sensitivity spans 268.6–325.9 K.
This is a new thin-membrane calculation; 037's P2 sandwich temperatures are not substituted.
Its earlier bare-P3 Zylon subsolar/night values, 317.42/273.31 K, are retained as context.
An unqualified low-emittance metal-facing case can reach 386.8 K in the low-h sensitivity.
Thus opacity alone does not prove acceptable temperature. The white-coating mass is charged below.

Radiative cooling makes condensation possible on the exposed nominal night and hot/wet shaded/night
surfaces. The PBO must be on the dry side of the exterior light/moisture barrier with protected edges.
An interior gas barrier leaving PBO exposed would not implement this protection.

For 041, the chosen cold-patch **5% bulk-RH target is 32.52 Pa water**, about 1.020 kg vapor
in the sag-adjusted volume. The source coupon upper envelope is 1.257 kg water/day plus
approximately 0.0085 kg/day wet seam leakage. A conditioned day reaches about 40.32 Pa.
Consequently the source's “below 1 g/(m² day)” alone does not prove this target: the worked bound
is **0.805 g/(m² day)** with no initial residual water, or roughly 19.36 h between drying at the
source envelope. The initial HM moisture proxy is already 0.965 kg at the 041 5% point.
Resin, PET and assembly residual water tighten the limit. The 458.7 kg/year water throughput
is removed at service; it is not carried as accumulated airborne mass. Local fibre activity remains unknown.
The [DuPont Teijin coupon sheet](sources/barrier-flex-pack-films-2001.pdf) measured water at
38°C/90% RH; transfer to this year is conditional.

Loads are continuous 95.461 kPa external pressure, a declared 365 thermal/top-up cycles,
12 full maintenance vents and 36,500 gusts/year. A vacuum top-up is **not** a full vent.
031's +2% pressure state plus 037's flight gust gives a peak pressure ratio 1.023045.
The cycle counts are assumptions; 0/12/365 full vents and severe gust-as-full-unload sensitivities are retained.
The frame is held fixed: 031's redesigned altitude-reserve point is not silently adopted.

**Strength and film SF at age**

No unique retained strength with the proposed barrier is known. The table gives reproducible,
distinct scenarios. Strength means the 1.74 GPa total-gauge equivalent; the assumed per-ply
strength is twice this. Qualified strengths and SFs are null in RESULTS.
The humid reference is continuous 40°C/80% RH, not a fitted forecast of the year above.
Warehouse exponential is an endpoint extrapolation, not a match to the early part of its source curve.
The dry target is a **combined loss requirement of 0.5% per year**, not an observed aging rate.

| Scenario — all PROJECTION | Years | Retained fraction | Effective strength GPa | 022d 5% film SF | 041 5% film SF | 041 019 film SF |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(age_table)}

The uncovered 5/10-year numbers extrapolate far beyond six months; their precision is arithmetic,
not evidence. Even holding the six-month value constant thereafter would fail every point.
Numbers after a scenario crosses SF 1 describe hypothetical residual material strength, not
continued operation of a surviving vehicle.
Nominal age at SF=1 under each law:

| Scenario | 022d 5%, years | 041 5%, years | 041 019, years |
|---|---:|---:|---:|
{chr(10).join(cross_table)}

The uncovered crossings are **10.2 / 5.95 / 3.55 days by log interpolation**.
The supported observation is only that the first half-month sample has already crossed;
these are not validated field failure dates. Glass/argon extrapolation repeats a measurement
loss ceiling every 210 days and is deliberately a sensitivity, not a fitted degradation law.

MODEL-FORM.csv shows the uncertainty: the warehouse endpoint permits a plateau assumption of
96% versus exponential 86.2% at ten years; the humid endpoint gives 36.7% exponential versus
62.5% for the plotted-curve continuation. No data here selects a ten-year tail.
Nominal annual loss ceilings for ten-year SF≥1 are 2.271%, 1.330% and 0.796% for the three main points.

A separate light-dose reciprocity **sensitivity**, not a validated photochemical model, maps ten years
behind ideal OD3 to 0.01 outdoor-equivalent years and about 92.1% retention. That already approaches
the 041 019 threshold before other loss. With 95% dark retention, that point requires transmission
below about 3.48×10⁻⁴ (OD3.46) under this proxy. A **measured broadband OD4 target**
provides room in that particular calculation; assumed 100 nm Al is merely its mass allowance.
A pinhole is a local unprotected region, not an area-averaged harmless loss.

**Heat, creep and fatigue consume additional margin**

At the declared hot condition, the approximate instantaneous strength factor is 0.9640.
A fully attached sensitivity, stress-free at 284.9 K with the frame at ambient temperature,
adds 90.50 MPa per ply. This is a restraint bound, not a coupled membrane solution.
With the dry ten-year target, film SF becomes **1.0927 / 0.9957 / 0.9448** at
022d 5% / 041 5% / 041 019. Restoring film SF=1 needs 0 / **0.714 / 9.165 kg**
additional PBO at the fixed geometry. Both resized 041 cases then use 161.545 kg reinforcement.
Pressure-only hot factors without that restraint are 1.1277 / 1.0246 / 0.9708.
The 041 019 full-restraint screen is already 0.99335 when new.
These sensitivities do not override 041's separate local-shell result of 0.978132 for its 019 witness.

[Davies et al.]({FATIGUE}) measured median lives of 514,800 and 21,060 cycles for HM single fibres
at 3.018 and 3.521 GPa, R=0, 50 Hz. Log-log interpolation gives the 041 5% nominal/hot-stress
proxies 431,320/148,471 cycles. Twelve full vents per year produce ten-year cycle indices
0.000278/0.000808; interpreting all 36,500 annual gusts as full unloading gives 0.846/2.458.
The real gust has a high minimum tensile load, so those extremes are not interchangeable.
No matched high-R, aged, folded-seam curve exists here. Median filament indices are not safe-life values.
The source's 60%-load PBO creep extrapolation must also retain humidity, light and geometry qualifications.

**Mass and restoration options**

034's historic 57.546 kg barrier comprises 12 µm PET 20.961 kg, assumed 50 nm Al 0.170 kg,
25 g/m² attachment 31.416 kg and 5 kg seam allowance. Its seam length was only 774.44 m.
This card scales that last allowance by current unique seam length: 1,378.71 m for 022d and
1,799.68 m for 041. The 25 g/m² white-coating target adds 31.416 kg. All are projected BOMs.

| Added protection | 022d 5%, kg | 041 5%, kg | 041 019, kg |
|---|---:|---:|---:|
| OD3 exterior layer, attachment and scaled seams | 61.448 | 64.165 | 64.165 |
| Above plus white optical target | 92.864 | 95.581 | 95.581 |
| OD4 mass target (100 nm Al) plus white | 93.033 | 95.751 | 95.751 |
| Two 6.35 µm foil/PET envelopes, attachment/seams, white | 197.062 | 202.498 | 202.498 |

The heavier foil option is a protected dry-package candidate, not a demonstrated hermetic life.
None earns a retention improvement without evidence. If the combined dry target is met,
unchanged films have the nominal ten-year SFs 1.1967/1.0874/1.0302 above. Restoring their
**initial** nominal factors requires 225.570/169.098/160.212 kg reinforcement respectively,
in addition to protection. This is different from restoring only SF=1.

For the 041 5% geometry, alternate-fibre comparisons use each stated retained-strength assumption,
the same projected 60% efficiency, and both directions. The table reports reinforcement only;
add **95.751 kg** for the common OD4/white package, before vacuum equipment and additional hardware.
The chemistry-only alternatives do not inherit PBO's creep resistance.

| Fibre / assumption | Ten-year retention | SF at existing 160.831 kg | Fibre kg for nominal SF=1 | Fibre kg to restore original SF=1.143285 |
|---|---:|---:|---:|---:|
{chr(10).join(alt_table)}

[DuPont's Kevlar guide]({KEVLAR}) supports the 1,440 kg/m³ and 3.0 GPa yarn values and
good neutral-pH hydrolytic stability; **95% at ten years remains a requirement**, with light exclusion.
[Forster et al.]({UHMWPE}) project 70% UHMWPE strength after 36 years at 43°C using an approximately
140 kJ/mol activation energy. Exponential interpolation gives 90.57% at ten years.
The declared cool year would yield 99.60% in an additional oxidation-only time-temperature sensitivity,
but neither result qualifies a specific SK75/SK99/DM20 membrane or its creep.

[Dyneema's current portfolio]({DYNEEMA}) gives SK99 42.5 cN/dtex.
It is the **lightest static chemistry-only option**, 135.881 kg reinforcement at nominal ten-year SF=1.
However [the manufacturer's patent]({PATENT}), paragraphs 0099/0106–0107, reports minimum creep
rates at 900 MPa/30°C of 7×10⁻⁶ %/s for SK99 and 1.3×10⁻⁶ %/s for DM20.
Constant-rate arithmetic reaches 1% strain in 39.7/213.7 h, not a rupture prediction.
Merely reducing a 041 UHMWPE skin to that 900 MPa reference stress requires 338.220 kg;
900 MPa is itself not a demonstrated ten-year allowable. A zero-creep label cannot be transferred
to the roughly 2 GPa stress of the thin chemistry-only candidates.

A **replaceable PBO skin** resets only the film. At 041 5%, the OD4/white skin is 256.582 kg;
two extra ply layers in a 25 mm strip along each unique boundary add 11.517 kg, giving
**268.099 kg per skin set**. Ten annual sets consume 2,680.985 kg over ten years, with
2,412.887 kg of replacements stored offboard. Under the warehouse scenario, pre-renewal
nominal SF is 1.1264 and fresh SF 1.1433. Under the humid reference, annual pre-renewal
SF is only 0.9548: a calendar replacement promise is not enough. Faster 1/3-month options
are tabulated, but require a qualified removable interface and appropriate thermal gauge.

**Decision carried forward**

Develop protected PBO with a measured total loss budget and replaceable bays; do not label the present
film a ten-year part. The lightest worked **PBO ten-year hot-film candidate** is the OD4/white
protection plus reinforcement resized to 161.545 kg at either 041 geometry/reserve case.
It requires the unproved 0.9511 retention target and meets only the stated film SF=1 screen.
The cheaper static SK99 alternative remains open for grade-specific creep qualification.
There is no established lightest qualified ten-year route.

With 30–50 kg vacuum hardware and a separate 5 kg fitting-adhesive placeholder, the 041
OD4/white package totals **130.751–150.751 kg**, exceeding the existing 100 kg line by
30.751–50.751 kg. Including the hot-film correction makes the added closure burden
31.465–51.465 kg for 041 5%, or 39.916–59.916 kg for 041 019, while holding reserve fixed.
No spare mass or payload credit is awarded. Reclosing and checking the complete vehicle is still required.

Forty-three calculator checks, forty-two independent audit comparisons, six physical/allocation
invariants and 113 original/copy/source pin checks pass. Twenty-two new NFI entries and all
relevant pinned upstream registers remain open.
METHOD.md, SOURCE-DATA, all CSVs, source snapshots, code and the figure are retained.
The brief says stop and file; no successor is named. No out-of-band contact, manual wake or restore occurred.
""")

write("METHOD.md",f"""
# MAINLINE-046 methods and scope

**All service transfers, strengths, masses, lives and SFs are QUESTIONABLE / PROJECTION.**
The work answers the requested ages with explicit scenarios while leaving qualified installed values null.
No upstream code is needed to execute life46.py; it reads the pinned data files.

The selected points are 022d cap/equilateral/in-band Zylon/CFRP at both reserves and 041's
frequency-5 m=24 closure witnesses at both reserves. R=10 m, p=95,460.8379139 Pa,
surface area 4πR²=1,256.637061 m² and reinforcement density 1,560 kg/m³.
Both total gauges and masses come from the unrounded upstream JSON.
041's unchanged frequency-4 frame is not a closure witness and receives no substituted margin.
Its selected film factor is 1.227877, but the actual-frame closure deficit is 174.444 kg.

For curvature radius r_c and total gauge t, the inherited pressure demand in each direction is
N=p r_c/2. Each ply is t/2, so actual axial ply stress is p r_c/t.
The assumed ply strength is 0.6×5.8 GPa=3.48 GPa; therefore
SF=3.48e9 t/(p r_c)=2×1.74e9 t/(p r_c).
The 1.74 GPa scalar already accounts for the two directions. Do not halve it again or
compare the half-sized equivalent stress to single-fibre creep data.
Age multiplies the same assumed material strength: SF(age)=SF0×R(age).
It does not validate the original 60% efficiency, a complete laminate, or a system SF.
Gauge scaling leaves the fixed pressure-curvature law unchanged; creep-induced shape change is not solved.

**Aging functions**

Source graph readings are stored explicitly. Toyobo's small figures were visually inspected
in rendered PDF pages; an approximate ±0.02 retention uncertainty is appropriate.
These are not statistically independent laboratory raw data.

For outdoor exposure, the first HM point is about .71 at half a month and the source text gives
about .35 after six months. From 0 to half a month, interpolate log(retention) linearly.
After that use R=exp[ln(.35)(y/.5)^β], with
β=ln[ln(.35)/ln(.71)]/ln(12). This joins the two anchors and provides an explicit tail.
Intermediate source readings (.44 at 2.25 months, about .335 at 4 months) show scatter;
the tail is not claimed to fit all points. No outdoor temperature/light-dose record permits
mapping the source months to the constructed service year. Threshold crossings occur before
the first nonzero observation, so their empirical bracket is 0–half a month.

For the humid reference, use log-linear interpolation through the manual 40°C/80% RH
AS readings through 1000 days. Continue past 1000 with
R=exp[ln(.76)(d/1000)^β], β=ln[ln(.76)/ln(.90)]/ln(10).
This tail uses approximate 100-day/.90 and 1000-day/.76 points.
For warehouse sensitivity use R=.96^(d/1000), solely an endpoint exponential.
For sealed-argon loss-ceiling sensitivity use R=.96^(d/210); <4% over 210 days is an
observation ceiling, not evidence of a repeating exponential rate.
For the combined protection acceptance requirement use R=.995^y.
That final function must include moisture, light, mechanical and chemical losses together;
do not multiply it by separate loss factors and call that the same acceptance target.

The first four functions are exposure proxies, and the fifth is a requirement.
None is a validated annual P3 life model. MODEL-FORM compares alternative tails.
EXPOSURE-SENSITIVITY instead parameterizes the unidentified equivalent exposure rate to a
40°C/80% RH reference. No PBO activation energy or humidity exponent is invented.
Do not add or multiply outdoor and dark humidity losses as if their independence were established.
NIST's combined conditioning evidence demonstrates that synergy is possible.

SF crossing solves SF0 R(y)=1. The maximum constant annual fractional loss that preserves
ten-year nominal SF≥1 is 1−SF0^(−1/10).
Apparent long target-function crossing ages beyond ten years are mathematical results only,
not proposed inspection or replacement intervals.

**One-year environment and instantaneous mechanical sensitivity**

SERVICE.json records 305/50/10 days in nominal/optimistic/conservative weather states.
Six sun, six shade and twelve night hours per day total 8760 hours.
The local-patch spectrum is 970 W/m² during sun and zero otherwise; source 037's day/night
effective sky values 275/260 K are shifted by the air-temperature offset.
This assumes an appropriate radiative boundary and view factor; it is not a full spherical
view-factor or internal radiation solution. Fixed h=5, with h=2 and 10 sensitivities,
is a declared exterior-convection approximation.

Solve α I − h(T_f−T_air) − ε σ_SB(T_f⁴−T_sky⁴)=0.
Primary protected optics are α=.2, ε=.9 from 037's white target.
Low-emittance α=.2/ε=.05 and bare-fibre α=.6/ε=.9 are explicit sensitivities,
not measured spectra. No metal-facing package is automatically assigned the white optics.
The membrane is isothermal through its thickness; transient heat capacity, backing/frame
conduction, ground radiation, condensation latent heat and directional transport are omitted.

Water saturation uses the declared modified Buck over-water expression,
611.21 exp[(18.678−C/234.5) C/(257.14+C)] Pa. Below zero, this means supercooled-water
saturation; an ice convention would change the cold sensitivity. RH=min(1,p_w/p_sat).
Condensation is flagged where the unclipped ratio exceeds one. The measured service climate
and local laminate activity remain NFI.

At the selected h=5 hot condition, use a graph interpolation φ_T=min[1,1−.1(T_f−293.15)/80]
for instantaneous HM strength. This approximate reversible effect is separate from permanent R.
For the fully attached sensitivity, assume a stress-free 284.9 K:
ε_mismatch=4.5e−6(T_air−284.9)+6e−6(T_f−284.9).
PBO axial modulus 270 GPa turns positive strain into an added ply stress.
The SiC support is assumed at air temperature; actual support irradiation, adhesive relaxation,
geometric strain and temperature of installation must replace this bound in a coupled calculation.

The peak pressure ratio is 1.02 + [ρVB U + ρU²/2]/p, with
ρ=1.16726833074618 kg/m³, VB=35 knots and U=35 ft/s.
Hot film SF is 3.48e9 R φ_T/[σ_ply,0 q + σ_thermal].
To resize to a target film SF g at that condition:
m/m0=σ_ply,0 q/[3.48e9 R φ_T/g − σ_thermal].
Thermal stress is strain-controlled and does not fall inversely with added thickness.
The code uses g=1 for the reported hot correction. No frame or joint SF is restored by this calculation.

**Water and optical protection**

Sag-corrected gas volume is 4πR³/3−(sag lift debit)/ρ_air.
At the primary cold film temperature, choose p_w,target=.05 p_sat(T_min).
Water capacity is p_w,target V M_w/(R_g T_gas), at 284.9 K.
Transmission is the source upper envelope 1 g/(m² day), uncorrected for temperature/activity.
Seam leakage follows 034's .001 mbar L/s per metre and per extra node plus .01 for ports,
using each new frame's unique boundary length and node count, and hot water mole fraction 6000/p.
This does not qualify assembly leakage. Both conditioned zero-inventory and the separate
HM 0.6%-by-mass initial water proxy are reported. PET, resin and other water must be added.
Moisture in a fibre/polymer microenvironment need not equal bulk gas water pressure.
Daily ground drying removes water, rather than storing a year's throughflow onboard.

Optical transmission τ=10^(−OD) is a wavelength-dependent definition.
The hypothetical dose-reciprocity calculation evaluates outdoor R(10 τ f) for dose ratio f=.25,1,4.
The outdoor data include heat/moisture, so it is only a sensitivity, not an identified photon-only law.
Within the first segment, the allowable τ for ten-year nominal SF 1 with assumed dark retention R_d is
ln(SF0 R_d)/[10×(−24 ln(.71))], if SF0 R_d>1.
An OD4 requirement applies to the damaging spectrum and local worst spot after aging,
not to average metal thickness or average area with pinholes.

Mass uses outer area, 12 µm PET at 1390 kg/m³, assumed 50 nm Al at 2700 kg/m³,
25 g/m² attachment and 25 g/m² white coating. The OD4 mass target allows 100 nm Al.
The 034 seam allowance scales as 5 kg × L_new/774.440887 m.
Foil alternatives use 6.35 µm Al, one PET layer and attachment per side, and doubled scaled seams.
These assumed gauges are not manufacturability or optical certifications.
Extra sagged area, trim, actual seam hardware and redundancy remain uncharged NFI.

**Other fibres, replacement and sustained load**

Alternate masses use directional equivalent strength .3×raw fibre strength, preserving the
original 60% efficiency and two-direction bookkeeping. This efficiency transfer is unqualified.
At the same reinforcement mass,
SF_new=SF_PBO×[(S_new/ρ_new)/(S_PBO/ρ_PBO)]×R_new.
Mass for SF=1 is old mass/SF_new; mass to restore the original SF is old mass×SF0/SF_new.
Kevlar49 uses 1440 kg/m³ and 3.0 GPa conditioned yarn, not the 3.6 GPa resin-impregnated strand.
Its .95 ten-year retention is a requirement, not a prediction from neutral-pH short tests.
UHMWPE includes a 3.7 GPa measured SK75 comparison and current SK99/DM20 tenacity cases.
1 cN/dtex=100000 N m/kg; density 970 kg/m³ converts 42.5/32 cN/dtex to 4.1225/3.104 GPa.

Forster's other-yarn oxidative prediction is represented by R=.7^(y/36) at 43°C.
It is not presented as a measured curve or the same grade. A separate nonisothermal oxidation
sensitivity integrates exp[−Ea/R_g(1/T−1/316.15)] over the declared year, with Ea=140 kJ/mol.
The thermal law, grade transfer, physical relaxation, ultraviolet exposure, hot strength and
creep are all independent qualifications. Source author caution about high-temperature physical
changes is retained.

Patent minimum creep rates at 900 MPa/30°C are recorded in percent per second, with
the exponent visually verified from PDF p.12. Dividing 1% by rate gives a constant-rate
strain time, not rupture life. Ten-year/1%-strain requires mean rate below
3.171e−9 %/s. Film mass at the source's 900 MPa reference stress is
p r_c A ρ_UHMWPE/(900e6); that stress is not certified safe.

Replacement tables retain one installed film and place all later sets offboard.
The 0/25/50 mm boundary-strip sensitivity has two extra film layers:
Δm=2 w L (m_film/A). This is reinforcement only, not a proven demountable joint.
Intervals 1,3,12 months are counted over ten years with ceil(10/interval_years).
The film SF immediately resets only if a new qualified film and interface are installed;
the frame, fittings, pressure-boundary joints and prior damage do not reset.

PBO fatigue uses only Davies' two measured median R=0 endpoints.
N=514800[σ/(.6×5.03e9)]^(−n), n=ln(514800/21060)/ln(.7/.6).
Values outside the 60–70% test-stress range are flagged as extrapolation.
Cycle ratios are bookkeeping comparisons, not a calibrated Miner rule for the real high-R spectrum.
The dry acceptance target already includes total irreversible loss, so these cycle indices are not
multiplied into it as a second independent retained-strength model.

**Reproduction and checks**

Run `TMPDIR=unpublished-local-ref:1ffe4110219d37c0 MPLCONFIGDIR=unpublished-local-ref:0f195fac91786b1b python3 life46.py`,
then `python3 assemble46.py` from this directory. Numeric inputs are the frozen JSON and explicit
source anchors. Files use finite JSON numbers; qualified unknowns are null.
Forty-three numeric checks cover independent source-point mass/ply-stress reconstruction,
closure, retention anchors, crossings and fatigue endpoints. Six invariants check coverage,
bounds, qualified-value nulls and bookkeeping. An independent audit and pin validation are
separate artifacts. Static analytical work runs locally; no persistent calculation process remains.
No statistical reliability, certified fatigue/creep life, approved operational limit or complete vehicle
mass closure is inferred. The next scientific evidence is specified in NFI; the brief names no next job.
""")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]