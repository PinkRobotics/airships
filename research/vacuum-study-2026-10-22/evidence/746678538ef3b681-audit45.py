"""Evidence, witness feasibility and independent cross-form checks."""
from pathlib import Path
import json,math,hashlib,csv,re
import numpy as np
from scipy.optimize import brentq
from check45 import ROOT,save,check,compare,CHECKS,p3point,P,R,AREA,B,RGAS,G,VOLUME,PI,TF,TC,N,DF,CRUSH,LAM_C
from leak45 import simulate,atmosphere,flux,MASS

c=json.loads((ROOT/"inputs/owner/COMPUTE.json").read_text())
a=json.loads((ROOT/"ARITHMETIC.json").read_text())
evidence=[]
for filename in ["threats.json","sandwich.json","p3damage.json","leak.json"]:
    library=json.loads((ROOT/"inputs/owner"/filename).read_text())
    for i,row in enumerate(library["rows"]):
        source=row["source"]
        evidence.append(dict(file=filename,index=i,property=row["property"],value=row["value"],
          units=row["units"],tag=row["tag"],basis=row["basis"],url=source["url"],
          location=source["location"],has_title=bool(source.get("title")),
          has_source_quote=bool(source.get("quote")),tag_valid=row["tag"] in ["QUESTIONABLE","PROJECTION"]))
used=[]
for key,row in c["sources_used"].items():
    source=json.loads((ROOT/"inputs/owner"/row["file"]).read_text())["rows"][row["index"]]
    used.append(dict(key=key,file=row["file"],index=row["index"],
      value=row["value"],underlying_value=source["value"],units=row.get("units"),
      tag=source["tag"],url=row["url"],source_url_matches=row["url"]==source["source"]["url"],
      scalar_matches=row["value"]==source["value"] if row["value"] is not None else None,
      text_selection=row["value"] is None))
save("EVIDENCE-ROWS.json",evidence)
save("USED-SOURCE-CHECKS.json",used)
pins=[]
for row in json.loads((ROOT/"INPUT-PINS.json").read_text()):
    original=Path(row["path"]);copy=ROOT/row["snapshot"]
    for kind,p in [("original",original),("snapshot",copy)]:
        b=p.read_bytes();pins.append(dict(path=str(p),kind=kind,sha256=hashlib.sha256(b).hexdigest(),
          bytes=len(b),match=hashlib.sha256(b).hexdigest()==row["sha256"] and len(b)==row["bytes"]))
retrieval=[]
for name in ["SOURCE-INTAKE.json","SOURCE-ADDITIONAL.json","SOURCE-REGULATORY-2025.json","SOURCE-SUPPLEMENT.json"]:
    path=ROOT/name
    if not path.exists():continue
    for row in json.loads(path.read_text()):
        if row.get("status")=="retrieved":
            p=ROOT/row["path"];b=p.read_bytes()
            valid=(hashlib.sha256(b).hexdigest()==row["sha256"] and len(b)==row["bytes"])
            substantive=not(b"Federal Register :: Request Access" in b[:2000])
            retrieval.append(dict(path=row["path"],url=row["url"],pin_match=valid,substantive_document=substantive))
save("PIN-CHECKS.json",pins)
save("SOURCE-DOCUMENT-CHECKS.json",retrieval)

# A separate forward calculation at each of the OWNER's supplied witnesses
# distinguishes numerical reproduction from improvements made by a new search.
witnesses=[]
for family,rows in c["p3"]["pricing"].items():
    for i,row in enumerate(rows):
        if row.get("SF") is None or "s" not in row:continue
        p=p3point(row["s"],row["OD"]/2,row["SF"],row.get("film_allowable_Pa",1.74e9),
                  row.get("extra_kg",0),row.get("wall_min_m",0))
        out=dict(wall=p["t"],film_kg=p["m_film"],tube_kg=p["m_tube"])
        compare(f"filed_witness/p3/{family}/{i}",out,row,rtol=5e-6)
        physical_min=min(p["modes"][k] for k in ["compression","euler","local","film","global","perry"])
        witnesses.append(dict(family=family,index=i,declared_SF=row["SF"],minimum_SF=physical_min,
              half_wave_ratio=p["half_over_L"],wall_m=p["t"],wall_min_m=row.get("wall_min_m",0),
              feasible_at_declared_multiplier=physical_min>=row["SF"]-2e-6 and p["half_over_L"]>=1-2e-6 and p["t"]>=row.get("wall_min_m",0)-1e-8))
save("FILED-WITNESS-CHECKS.json",witnesses)

# Expand each independent optimized witness directly from annulus area and
# section integrals, without using the p3point evaluator's section values.
new_witness=[]
p3sets=[("nominal",a["p3"],1.74e9,0.)]
for family,rows in a["p3_pricing"].items():
    for i,row in enumerate(rows):
        if row.get("SF") is None:continue
        orig=c["p3"]["pricing"][family][i]
        val=p3point(row["s"],row["OD"]/2,row["SF"],orig.get("film_allowable_Pa",1.74e9),orig.get("extra_kg",0))
        p3sets.append((family+"/"+str(i),val,orig.get("film_allowable_Pa",1.74e9),orig.get("extra_kg",0)))
for label,p,allowable,extra in p3sets:
    annulus=PI*(2*p["ro"]*p["t"]-p["t"]**2)
    inertia=PI/4*(p["ro"]**4-(p["ro"]-p["t"])**4)
    mode_comp=3.9e9*annulus/p["N"]
    mode_euler=PI**2*410e9*inertia/(p["L"]**2*p["N"])
    eta=(p["L"]/1000)*p["ro"]*annulus/inertia
    z=mode_comp+mode_euler*(1+eta)
    perry=2*mode_comp*mode_euler/(z+math.sqrt(z*z-4*mode_comp*mode_euler))
    q=p["lam"]
    magnified_moment=q*p["N"]*(p["L"]/1000)/(1-q/mode_euler)
    tensile=max(0.,magnified_moment*p["ro"]/inertia-q*p["N"]/annulus)
    structural_mass=3100*annulus*p["members"]*p["L"]+p["m_film"]+p["m_nodes"]+p["m_joint"]
    mass_residual=structural_mass+100+.05*B+p["sag"]+extra-B
    check("invariant/"+label+"/annulus_area",annulus,p["A"],rtol=2e-10)
    check("invariant/"+label+"/inertia",inertia,p["I"],rtol=2e-10)
    check("invariant/"+label+"/perry_closed_root",perry,p["modes"]["perry"],rtol=2e-9)
    check("invariant/"+label+"/mass_residual",mass_residual,0.,atol=1e-6)
    check("invariant/"+label+"/tensile_15p586_screen",tensile<=15.586e6,True)
    new_witness.append(dict(label=label,SF=q,mass_residual_kg=mass_residual,perry_SF=perry,
      tension_at_load_Pa=tensile,tension_screen_Pa=15.586e6,half_wave_ratio=p["half_over_L"]))
save("NEW-WITNESS-INVARIANTS.json",new_witness)

with (ROOT/"inputs/upstream/022d_tables_csv/TABLES.csv").open() as f:
    upstream=next(row for row in csv.DictReader(f) if row["branch"]=="cap" and row["grid"]=="equilateral" and row["reserve"]=="5" and row["family"]=="cfrp_zylon" and row["band"]=="in_band")
check("upstream_022d/Perry",a["p3"]["modes"]["perry"],float(upstream["SF_perry"]),rtol=1e-9)

# Important prose quantities that are not exposed as calculation fields.
growth55=(CRUSH-P/2)*(.055/2)**2/(4*(N-LAM_C**2*DF/(.055/2)**2))
hail=c["p2"]["pricing"]["design_hail_needs"]
needratio={k:(row["crush_needed_Pa"]/CRUSH)**.6 for k,row in hail.items()}
width=a["p2"]["width_lambda1_m"]
contact_v=math.sqrt(2*PI*width**2*CRUSH*a["p2"]["depth_allow_lee_envelope_m"]/(1.5*MASS))
float_margin=a["p2_margin"]
face81=((N*(.08086510609617895/2)**2*12*(1-.0752**2))/(LAM_C**2*290e9))**(1/3)
maxfaces=(B-100-411.2989440716474)/1.05
leak=json.loads((ROOT/"LEAK-RESULTS.json").read_text())
rho0=atmosphere(0)[2]
bay_heaviness=[MASS+row["m_in_end_kg"]-rho0*VOLUME for row in leak["big"][:2]]
sea_level_vent_mass=(101325-P*hail["Shi-calibrated k rho v2"]["vent_fraction_dp"])*VOLUME/(RGAS*288.15)
display=dict(growth_at_55mm_m=growth55,core_depth_m=TC,
             patch_55mm_is_deeper_than_core=bool(growth55>TC),
             density_multiplier_to_required_crush=needratio,
             lambda1_contact_speed_for_Lee_depth_m_s=contact_v,
             mass_margin_kg=float_margin,margin_g_per_m2=float_margin/AREA*1000,
             face_gauge_to_bridge_design_hail_m=face81,face_mass_alone_kg=2*AREA*1850*face81,
             maximum_structural_budget_kg=maxfaces,
             bay_net_heaviness_at_zero_centre_height_kg=bay_heaviness,
             sea_level_vent_to_same_absolute_differential_air_kg=sea_level_vent_mass,
             air_volume_convention_m3=VOLUME)
save("PROSE-CROSS-CHECKS.json",display)

# An actual sphere first touches level ground when its centre is R above it.
ground_sensitivity=[]
for dia in [.0631009341,.0656067703,.1,.3,1.]:
    for drag in [.47,.2]:
        value=simulate(PI*dia**2/4,drag,ground_altitude=R)
        ground_sensitivity.append(dict(diameter_m=dia,drag=drag,centre_height_at_contact_m=R,
          time_s=value["t_end_s"],speed_m_s=-value["v_end_m_s"],net_heaviness_kg=value["net_heaviness_kg"]))
for drag in [.47,.2]:
    value=simulate(a["p3"]["bay_area_m2"],drag,ground_altitude=R)
    ground_sensitivity.append(dict(case="torn P3 bay",drag=drag,centre_height_at_contact_m=R,
      time_s=value["t_end_s"],speed_m_s=-value["v_end_m_s"],net_heaviness_kg=value["net_heaviness_kg"]))
save("GROUND-CONTACT-SENSITIVITY.json",ground_sensitivity)

# Filing consistency is separate from independent physics.
owner_results=json.loads((ROOT/"inputs/owner/RESULTS.json").read_text())
check("filing/RESULTS_compute_equals_COMPUTE",owner_results["compute"]==c,True)
check("evidence/all_388_rows_have_valid_tag",all(v["tag_valid"] for v in evidence),True)
check("evidence/all_388_rows_have_title_and_url",all(v["has_title"] and v["url"] for v in evidence),True)
check("evidence/all_87_selected_source_urls_match",all(v["source_url_matches"] for v in used),True)
check("evidence/all_nonnull_selected_values_match",all(v["scalar_matches"] is not False for v in used),True)
check("pins/all_originals_and_snapshots_match",all(v["match"] for v in pins),True)
check("pins/all_downloads_match",all(v["pin_match"] for v in retrieval),True)
save("AUDIT-CHECKS.json",CHECKS)
save("AUDIT-DIFFERENCES.json",[v for v in CHECKS if not v["pass_"]])
print(json.dumps(dict(checks=len(CHECKS),differences=sum(not v["pass_"] for v in CHECKS),
  evidence_rows=len(evidence),selected_sources=len(used),original_and_copy_pins=len(pins),
  downloaded_documents=len(retrieval),substantive_documents=sum(v["substantive_document"] for v in retrieval),
  display=display),indent=2))
