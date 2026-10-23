#!/usr/bin/env python3
"""Package source facts and unresolved material/process qualifications."""
import json
from pathlib import Path

B=Path(__file__).resolve().parent
def dump(name,obj):
    (B/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+"\n")

facts=[
 dict(source="https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf",
      access="Web PDF parser; direct download denied 403. This is a selected fact record, not a PDF snapshot.",
      pages=[51,63,65,67,89],
      tape_fact_rows=[
          dict(type="AgFEP",gauge_mil=.5,mass_g_m2=88,alpha_max=.09,epsilon_hemi_min=.40,part="TBD",spec="G400600"),
          dict(type="AgFEP",gauge_mil=1,mass_g_m2=115,alpha_max=.09,epsilon_hemi_min=.48,part="146430"),
          dict(type="AlFEP",gauge_mil=.5,mass_g_m2=88,alpha_max=.14,epsilon_hemi_min=.40,part="TBD"),
          dict(type="AlFEP",gauge_mil=2,mass_g_m2=169,alpha_max=.14,epsilon_hemi_min=.60,part="146372"),
          dict(type="Al_polyimide_silicone",gauge_mil=.5,mass_g_m2=54,alpha_max=.36,epsilon_hemi_min=.52,part="146493")],
      note="Tape mass includes adhesive. 0.5 mil bare Ag/FEP film is 28 g/m2; adhesion specification uses stainless steel, not Be."),
 dict(source="https://patents.justia.com/patent/11391493",
      access="Web text of NASA patent; direct download denied 403. Selected facts, not a full patent snapshot.",
      provenance="US11391493, government-authored invention; description and claims.",
      classical=dict(alpha=.09,IR_emittance_band=[.65,.70],
          layers_um=[["Al2O3",.08],["Ag",.12],["Al2O3",[1.6,1.9]],
                     ["SiO2",[.5,.75]],["ITO",.01]]),
      multilayer_example=dict(layers_um=[["NiCr",.05],["Ag",.12],
                              ["Al2O3_total",1.2],["SiO2_total",.4],["ITO",.01]],
                              oxide_pairs=80),
      limitations="Classical optics depend on substrate roughness. Exact multilayer example is not a measured optical tuple on Be; other reported film constructions differ in thickness and emittance."),
 dict(source="https://enbio.eu/solar-white/",
      access="Web page; direct download denied 406. Selected facts only.",
      coating_thickness_um=[150,220],IR_emittance=[.89,.90],
      ambiguous_optical_header="Solar Reflectance",ambiguous_values=[.15,.18],
      listed_substrate="Beryllium",areal_mass=None,
      limitation="Do not silently certify the ambiguous quantity as solar absorptance."),
 dict(source="https://www.3m.com/3M/en_US/p/dc/v000088346/",
      product="EC-3917",source_claim_scope="Humid-environment bond durability",
      matched_200F_Be_process=None,water_uptake=None),
 dict(source="https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=4",
      model="log10(P_bar)=A-B/(T_K+C)",A=5.40221,B=1838.675,C=-31.737,
      valid_temperature_K=[273,303],
      use="Dew-point indication only; not a retained-water prediction."),
 dict(source="https://de.lesker.com/newweb/deposition_materials/depositionmaterials_sputtertargets_1.cfm?pgid=ag1",
      material="Ag",bulk_density_kg_m3=10500,
      use="Proxy for layer mass; deposited film density unmeasured."),
 dict(source="https://ntrs.nasa.gov/api/citations/20140008875/downloads/20140008875.pdf",
      access="NASA mechanism report read through web tool",
      use="CCAg handling-damage caution; not a matched environmental lifetime."),
 dict(source="https://chemical-catalysts-and-adsorbents.basf.com/dam/jcr%3A0b94531b-3ccc-4be2-af1a-3848a026fb45/basf/chemical-catalysts-and-adsorbents/Adsorbents/BASF_Sorbead_Air_Broschuere_screen_2023-04-13-092728_dcyv.pdf",
      local_snapshot="sources/basf-sorbead-air.pdf",material="4A molecular sieve",
      water_capacity_kg_kg=.21,temperature_C=25,relative_humidity=.80,
      limitation="Main model's .10 capacity at vacuum is assumed; not this catalog condition.")
]
dump("WEB-FACTS.json",facts)

coatings=json.loads((B/"COATINGS.json").read_text())
evidence=[]
for c in coatings:
    cid=c["id"]
    if cid=="reference040":
        uv="No qualified finish specification in original allowance."
        humidity="Unknown.";adhesion="Unknown."
    elif cid=="AZ93":
        uv="Maker documents stability under space UV/radiation conditions."
        humidity="NASA demonstrates retained moisture and controlled-humidity cure; no outdoor life or uptake mass for this hull."
        adhesion="Maker's general adhesion/substrate data do not qualify Be."
    elif cid=="Z93":
        uv="NASA catalog reports 2000 equivalent-sun-hour UV exposure without absorptance change under that test."
        humidity="No matched atmospheric humidity/rain-life measurement established."
        adhesion="Catalog adhesion is not a Be-lot/process qualification."
    elif cid=="SolarWhite":
        uv="Space-flight heritage is documented by maker; atmospheric UV-life endpoint not supplied."
        humidity="Maker describes nonporous inorganic finish; no matched retained-water or wet-aging measurement."
        adhesion="Be is explicitly listed as a compatible substrate; installed mass and this process remain unqualified."
    elif "FEP" in cid:
        uv="Chemours supports long outdoor stability of base FEP; silver/aluminum edges and PSA assembly not thereby qualified."
        humidity="Base FEP water absorption <0.01 wt%; whole tape, overlaps and metal corrosion unqualified."
        adhesion="Catalog peel specification uses stainless steel; Be adhesion and thermal cycling unknown."
    elif "Kapton" in cid:
        uv="Thermal-control film data exist; matched outdoor UV aging for this exact construction not established."
        humidity="Polyimide/PSA moisture cannot be assigned the FEP value; matched assembly uptake unknown."
        adhesion="No matched Be/PSA adhesion result."
    elif cid in ["CCAg","MLCCAg"]:
        uv="NASA space-use evidence; classical material absorbs some UV. No matched terrestrial UV/humidity lifetime."
        humidity="Oxide/metal stack has no sourced water isotherm or edge-corrosion result for this hull."
        adhesion="Direct rigid-metal deposition is described; Be surface preparation, stress, peel and repair mass unqualified."
    else:
        uv="Historical optical values depend on surface state; no stable outdoor-life endpoint."
        humidity="Corrosion changes optical properties; matched native-oxide/water retention unknown."
        adhesion="No adhesive for bare surface; oxide integrity and any protective treatment unknown."
    evidence.append(dict(id=cid,source=c["source"],UV=uv,humidity=humidity,
                         adhesion_on_Be=adhesion,tag="QUESTIONABLE / PROJECTION"))
dump("COATING-EVIDENCE.json",evidence)

items=[
 ("matched_multilayer_optics","The 7.5752 g/m2 recipe and .09/.80 hemispherical optics are linked by a class-level transfer, not a matched Be coupon.","Weigh and measure solar absorptance and hemispherical emittance on the exact stack, Be surface and process."),
 ("classical_emittance","Classical IR emittance .65 is used as hemispherical for the model; the cited 2015 value is normal emittance and not interchangeable.","Measure the hemispherical optical pair over temperature and relevant surface roughness."),
 ("Be_deposition_process","Direct deposition omits carrier and PSA only conditionally. Native oxide, pretreatment, deposition stress and adhesion are unresolved.","Qualify a prepared curved Be panel with thermal cycling and peel/adhesion testing; weigh all treatment layers."),
 ("installed_coating_mass","Layer-density calculations and 10% application allowance are not measured installed weights.","Measure total coating, edge seal, repairs, masking effects and coverage variation per finished area."),
 ("white_paint_mass","AZ93/Z93/SolarWhite minimum useful thickness is sourced but installed dry areal mass is not.","Weigh matched coated Be witnesses, including paint primer; resolve SolarWhite reflectance/absorptance heading."),
 ("film_availability","The lightest 0.5 mil Ag/FEP tape's catalog part number is TBD, despite a specification entry.","Confirm an actual offered construction and as-delivered adhesive weight without treating a catalog row as availability."),
 ("film_attachment","Silver/FEP stainless-steel peel results do not qualify Be, overlaps, edges or repair strips.","Test the complete Be/tape construction and weigh required edge seals and surface preparation."),
 ("UV_humidity_life","Space heritage and base-FEP weathering do not establish atmospheric coating/PSA/metal lifetime.","Measure combined UV, humidity, rain, corrosion, handling and thermal-cycle changes for the selected finish."),
 ("exterior_retention","0.1 kg/m2 is an assumed retained exterior liquid layer, not a measurement or a moisture-uptake property.","Measure dew/rain/frost retention and drainage at hull orientations; specify dry-operating limits if claiming zero."),
 ("wet_optics","Primary dry optical values are used alongside an exterior liquid mass. Assumed wet optics are sensitivities only.","Measure wet/frosted optical properties and solve the coupled condensation/evaporation thermal problem."),
 ("AF_uptake","Historical 2U WVR does not establish equilibrium uptake for the proposed 200 F cure. TML is not a water inventory.","Measure sorption/desorption and mass baseline for the exact 2U lot, cure and humidity cycle."),
 ("AF_2M_transfer","The 9.16% sensitivity derives from 2M immersed at 70 C with dissolution and a different cure.","Use only as a severe sensitivity until exact 2U exposure data exist."),
 ("primer_process","The 10 g/m2 structural-primer charge and 1% water fraction are planning assumptions; cited primer cure differs from 200 F.","Define the actual two-interface primer, dry thickness, density, uptake and matched cure/Be compatibility."),
 ("core_moisture","CRIII durability data are not core moisture-uptake data. Metal nonabsorption does not remove coating/node/cell water.","Measure the actual vented core's coating, contamination and condensed-water inventory."),
 ("finish_moisture","PSA, deposited-stack and seam-polymer water fractions are assumptions.","Measure each complete finish/seam construction's moisture baseline and change after conditioning."),
 ("nominal_water_baseline","Nominal density and film weights may already contain some moisture. The model conservatively adds a separate inventory.","Establish dry-reference versus as-delivered masses to avoid an unknown double allowance."),
 ("bake_endpoint","70 C preconditioning evidence is for exposed coupons; 90% removal and cure compatibility are not proven on a hull.","Demonstrate a measured residual-water endpoint and required access, temperature, time and equipment."),
 ("dry_gas_process","Five well-mixed hull-volume purges are a resource scenario, not a qualified assembly process or material dry-out.","Size the actual enclosure/glovebox and verify mixing, dew point, leak rate, exposure time and final material water."),
 ("sorbent_vacuum","10% usable capacity and 95% capture are unqualified at hull pressure and temperature.","Measure vacuum sorption isotherms, kinetics, dust control, regeneration and cartridge/retention mass."),
 ("nominal_volatiles","040's 90% volatile conditioning and water-equivalent pressure model remain assumptions shared by all routes.","Measure species-resolved release for the chosen cure/process; use the zero-capture and unconditioned sensitivities."),
 ("dew_operating_cycle","Dry-night temperatures can fall below the inherited water partial-pressure dew point; dew mass is unknown.","Resolve latent heat, air humidity transport, shading, sky condition, shedding and frost over the mission cycle."),
 ("coating_thermal_resistance","Optical coating thermal resistance and its own residual stress are omitted.","Measure or bound through-thickness resistance and coating stress for the installed stack."),
 ("joint_interaction","The primary 037b account separates mean scarf and free-edge shear. An added scalar interaction can erase the thin-tape margin.","Validate coincident load paths, peel and free-edge behavior on the matched curved joint."),
 ("200F_cure","The new finish does not repair the original 250 F minimum-strength free-edge failure. The 200 F stress-free state remains conditional.","Measure residual strains and qualify 2U/primer strength, durability and cure against 037b/CHECK-037b findings."),
 ("optical_aging_margin","For fixed emittance .80, the declared legacy day/full-cycle screen limits alpha to about .1665 at the source geometry.","Set optical end-of-life limits and measure aged coupons; this number is a model threshold, not a life prediction."),
 ("combined_mission","031 weather mass/pressure and 037 thermal environments remain separate model inputs.","Choose a joint atmospheric, solar, wind and water exposure before claiming mission-level float."),
 ("least_set_definition","Least sets depend on the four declared optimism axes, minimax interpolation and scalar equations; they are not measured allowable properties.","Ground each retained axis and replace the surrogate with validated coupled structural behavior."),
 ("cost_scope","Ground-gas and ideal heat calculations are resource lower bounds; equipment, labor, pumping, cycle duration and currency cost are unsourced.","Develop a matched process and obtain measured energy/use and equipment quotations."),
]
base=json.loads((B.parent/"vacuum-mainline040-common-account-1020/NFI.json").read_text())
dump("NFI.json",dict(
    unit="vacuum-mainline048-coating-and-water-1020",overall_installed_hull_SF=None,
    findings=[dict(id=f"048-{i:02d}-{name}",tag="QUESTIONABLE / PROJECTION",
                   open_issue=issue,grounding=ground) for i,(name,issue,ground) in enumerate(items,1)],
    inherited_040_findings=base["findings"],
    inheritance_note="040 findings remain open unless explicitly replaced by measured evidence; this card supplies sensitivities, not closure. Source pin is in MODEL-PINS.json."))
print("Prepared web facts, coating evidence and",len(items),"new open findings.")
