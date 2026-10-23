#!/usr/bin/env python3
"""Render the reviewable card, row export, formula notes and evidence needs."""
import csv
import json
import math
import re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parent
I=json.loads((ROOT/"INPUTS.json").read_text())
D=json.loads((ROOT/"RESULTS.json").read_text())
F=json.loads((ROOT/"FRAME.json").read_text())
V=json.loads((ROOT/"VALIDATION.json").read_text())
CAT=json.loads((ROOT/"CATALOGUE.json").read_text())


def format_prose(text):
    """Typeset numerical prose without touching links, identifiers or code."""
    def chunk(s):
        s=s.replace("SR200","SR-200").replace("S200F","S-200F").replace("CR-III5056","CR-III 5056")
        for a,b in [("leastSF","least SF"),("filmSF","film SF"),("absoluteSF","absolute SF"),
                    ("globalk","global k"),("imperfectiona₀","imperfection a₀"),
                    ("andfractional","and fractional"),("andcell","and cell"),
                    ("andA·tc","and A·tc"),("withR","with R"),("byR","by R"),
                    ("armR","arm R"),("asR","as R"),("scaleR","scale R"),
                    ("scalesR","scales R"),("areaπ","area π"),("approachingR","approaching R"),
                    ("Rm |","R (m) |"),("Baym |","Bay (m) |"),("radiusmm |","radius (mm) |")]:
            s=s.replace(a,b)
        s=re.sub(r"(?<=[a-z])(?=(?:R\d|SF\d|P[23]\b))"," ",s)
        s=re.sub(r"(?<=[a-z])(?=\d)"," ",s)
        s=re.sub(r"\bR(?=\d)","R = ",s)
        s=re.sub(r"\bE(?=\d)","E = ",s)
        s=re.sub(r"\bVc(?=\d)","Vc = ",s)
        s=re.sub(r"\bSF(?=\d)","SF ",s)
        s=re.sub(r"(?<=\d)(?=(?:kg|mm|MPa|GPa|kPa|Pa|tonnes|µm|m³|m²|m|g|K|W|h|in)\b)"," ",s)
        s=re.sub(r"(?<=[,;])(?=[A-Za-z])"," ",s)
        s=re.sub(r"(\.\*\*)(?=\S)",r"\1 ",s)
        s=s.replace("revision1","revision 1").replace("reserve%","reserve (%)")
        s=s.replace("009c 5","009c5").replace("ν0.33","ν = 0.33")
        return s
    lines=[]
    for line in text.splitlines():
        if line.startswith("    "):
            lines.append(line)
            continue
        parts=re.split(r"(`[^`]+`|https?://[^\s)]+|unpublished-local-ref:fa794034994ec6d6",line)
        lines.append("".join(part if i%2 else chunk(part) for i,part in enumerate(parts)))
    return "\n".join(lines)+"\n"


def get(r,scenario,family,mechanical="full_021",mass="coupled"):
    return next(p for p in D["P2"] if p["radius_m"]==r and p["scenario"]==scenario and
                p["family"]==family and p["mechanical"]==mechanical and p["mass_model"]==mass)


def pay(p):
    v=p["payload_at_SF1"]["maximum_payload_kg"]
    return "none" if v is None else f"{v:,.2f}"


def n(x, digits=5):
    return f"{x:.{digits}f}"


nfi_data=[
    ("PANEL-GAUGE","PROJECTION","The large 020 panel is 0.6096×1.8288m; its quoted stock maximum begins at 0.059in (1.4986mm). At R20 the enhanced aluminium face is only 1.423mm. The conservative small panel is an assumed 0.3048×0.6096m. Some severe-budget faces are far below the supplier's stated sheet gauge.",
     "Supplier-confirm panel dimensions at each minimum gauge, shaping yield, thickness distribution and installed geometry; re-run with procurement bounds."),
    ("SEAM-SCALING","PROJECTION","Frozen 020 kg/m2 hides Be-doubler and core-gap masses that grow with optimized thickness. The corrected model holds widths/gaps fixed but resizes their depths. Neither seam is mechanically designed.",
     "Weigh and load-test a curved two-skin splice; establish widths, gaps, taper, sealing, peel, fatigue and stiffness as functions of face/core thickness."),
    ("JOINT-STRENGTH","PROJECTION","020's 0.9/0.6 net-section efficiencies are assumed screens, applied only to compression. The enhanced aluminium optimum is global/joint limited. No joint buckling, shear or peel allowables exist.",
     "Measure the seam's biaxial compression, load eccentricity and failure envelope; do not count straps as structural stiffness without a model."),
    ("GAMMA","PROJECTION","Design uses the inherited hemispherical 0.2/1 step at Vc=2. Full021 uses 0.2+0.4min(Vc,2). Neither is validated for this completed sphere. Constant0.2 removes the enhanced P2 pass.",
     "Carry the 018b and 015 evidence into an installed-geometry shell test/model, retaining imperfection maps."),
    ("BE-GRADE","QUESTIONABLE","S200F E290GPa and inherited compression283MPa are the design screen. Full021 transfers a historical SR200 lot's 379.2MPa and lower in-plane E293.6GPa. Current SR200 sheet lists E290GPa and tensile minimum345MPa, not a guaranteed compression allowable. Nu0.33 remains inherited.",
     "Obtain lot-, gauge-, direction- and post-form compression/stiffness/Poisson data. Keep these mechanical optimism choices separate from weather optimism."),
    ("CORE-TRANSFER","QUESTIONABLE","5056 3/8-1.0 uses the published typical Ec/Gc/crush row; stabilized modulus is used in the wrinkle formula. Manufacturer tests were at 15.875mm depth; optimized cores reach roughly120–144mm at R50.",
     "Validate thick curved honeycomb, skin restraint, orthotropy, cell-depth effects, local modes, thermal response and crush definition. Catalogue sensitivity includes Plascore rows with Ec transferred from Hexcel and bare compression substituted for crush."),
    ("PUMP-SCALE","PROJECTION","One SV300B catalog pumping speed is insufficient for 019's volume-proportional 1%/day gas load above R10. Modular counting gives1,3,7,23,103 pumps at10,15,20,30,50m, with full rated power continuously budgeted. Installed conductance/manifolds are not sized.",
     "Measure leak/outgas and installed speed at pressure; replace the assumed gas-load law and duty cycle with a measured area/seam/volume decomposition."),
    ("PASSIVE-SERVICE","PROJECTION","The30kg sealed-service package is held fixed. Its normalized gas-load limit grows with volume; this does not prove its seals, plumbing, monitoring or ground evacuation hardware scale at fixed mass.",
     "Demonstrate24h hold at the temperature envelope, seal transients, pressure monitoring and ground-service capability; add supporting hardware mass."),
    ("ENVIRONMENT","QUESTIONABLE","The optimistic +10K/±1%/1000Pa vapour and conservative +25.1K/±2%/6000Pa cases are owner scenarios, not a site distribution. Water is a full-area equivalent retained film, contamination an area load.",
     "Specify site, gas composition, temperatures, weather exposure, water shedding/icing and mission duration; retain both low-density lift and high-pressure strength envelopes."),
    ("OTHER-MASS","QUESTIONABLE","Extra coatings, lightning protection, mooring, hardpoints, navigation and propulsion are not independently sized. P2 retains a100kg system floor, including70kg above the passive package, but this is not a complete vehicle mass model.",
     "Itemize additional vehicle masses. An extra0.1kg/m2 is included as a P2 sensitivity; 209.84kg payload at R20 is only41.75g/m2 of additional areal mass."),
    ("HANDLING","PROJECTION","Diameters grow20→100m, projected ground area and wind force at fixed speed grow25-fold, characteristic overturning moment125-fold. Point attachments, transport, launch and landing are outside uniform-pressure modes.",
     "Design and weigh handling/anchoring/assembly equipment and verify concentrated and asymmetric loads, gust response and damage tolerance."),
    ("FRAME-PRODUCT","PROJECTION","P3 asks for metre-scale curved, thin-walled SiC tubes and a pressure membrane at1.5GPa allowable. The opened supplier seal-tube example is typically12in long. These components and their formed geometry are not demonstrated products.",
     "Establish tube/film manufacturing, joints, porosity/leaks, defects, proof loads and installation tolerances; then replace bounds with physical ones."),
    ("FRAME-BRITTLE","QUESTIONABLE","011b's SiC compression3900MPa and metal-style Perry interaction produce the P3 pass. A380MPa strength screen gives only about0.24–0.25 over10–50m. Compressive strength is not a ceramic bending/tensile allowable.",
     "Use a brittle tension/compression interaction, statistical size effect and joint eccentricity rather than certifying on the inherited Perry score."),
    ("FRAME-NODES","PROJECTION","P3 retains20g/node and5% tube-mass joints without measured capacity or complete film-attachment masses. A load-linked node-mass sensitivity changes little numerically, but does not validate the20g anchor.",
     "Size nodes and film attachment/seams from load paths. Same topology with truly similar solid nodes would make each node's mass scale asR^3."),
    ("FRAME-BOUNDARY","QUESTIONABLE","P3 reoptimization holds bay0.4–3m and radius≤0.25m. The radius cap governs large hulls. Similarity rows separately scale members but hold80µm film, making film SF fall as1/R.",
     "Treat relaxed member caps or thicker film as separately costed designs; do not infer a universal radius optimum from this bounded continuation."),
    ("RESERVE-MEANING","QUESTIONABLE","Reserve is the explicit charge above retained baseline system/joint floors, not statistical contingency or free payload. Climate plus internal air alone is5.7396% optimistic and13.1183% conservative.",
     "If a sub5% requirement is mandatory, change/justify the climate or gas assumptions or definition. Increasing radius alone cannot meet it."),
    ("PROVENANCE","QUESTIONABLE","The dispatch names a nonmatching019 report ID; actual verified ID uses lead-sci. Original021 hashes are superseded by revision1, which was used. Scientific uncertainty remains despite arithmetic checks.",
     "Use INPUTS.json's53 verified/measured pins and the actual019/revised021 filing IDs; freeze this card after filing."),
]
nfi=dict(schema=1,card="MAINLINE-027",status="OPEN_EVIDENCE_NEEDS",certification=False,
         rows=[dict(id="NFI-027-"+code,tag=tag,issue=format_prose(issue).strip(),next_evidence=format_prose(action).strip())
               for code,tag,issue,action in nfi_data])
(ROOT/"NFI.json").write_text(json.dumps(nfi,indent=2)+"\n")

with (ROOT/"SCALE-ROWS.csv").open("w",newline="") as f:
    fields=["family","scenario","mechanical","mass_model","radius_m","feasible","least_SF",
            "reserve_kg","reserve_fraction","tf_m","tc_m","payload_at_SF1_kg",
            "systems_excess_kg","retained_water_kg","contamination_kg","coating_kg",
            "temperature_pressure_loss_kg","humidity_loss_kg","internal_gas_kg","joining_excess_kg"]
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for p in D["P2"]:
        row={k:p.get(k) for k in fields}
        row.update(p.get("budget_lines_kg",{}))
        row["payload_at_SF1_kg"]=p["payload_at_SF1"]["maximum_payload_kg"]
        w.writerow(row)

lines=[
    "# MAINLINE-027 — size as a lever",
    "",
    "ESTIMATE. **QUESTIONABLE inputs; PROJECTION fabrication, joints and named mechanical optimisms. No certification.** Unit `vacuum-mainline027-size-as-lever-1020`; order `ord-admiral-rr2-mainline027-dispatch-1019`. Radii are10,15,20,30,50m, at the inherited500m atmosphere. Times are measurements, not limits.",
    "",
    "**Size alone does not make either P2 design pass.** With the corrected seam masses and the inherited design properties, optimistic least SF at R50 is0.58971 aramid /0.50005 aluminium. Under MAINLINE-021's full named mechanical optimisms, aluminium first passes at the sampled **R20m: SF1.00749, payload209.84kg**; R30 and50 carry3,543.71 and26,391.28kg at SF1. Aramid remains below1. These payloads include the stated weather/gas/surface budget and joint screen, not a complete vehicle.",
    "",
    "**Neither family's optimistic reserve drops below5% at any radius.** Temperature/pressure, humidity and internal air alone charge **5.7396167%** of reference lift. All other reserve rows are nonnegative. This is an algebraic limit, not an extrapolated fitted crossing. The conservative floor is13.1183154%. Fixed-area masses help, but full-gauge splice doublers do not remain fixed kg/m² as the faces thicken.",
    "",
    "![Size and safety-factor curves](size-as-lever.png)",
    "",
    "## Basis and interpretation",
    "",
    "Aluminium is021 revision1's **Hexcel CR-III5056 3/8-1.0**,16.01846kg/m³, Ec103.421MPa, W shear46.884MPa, crush241.317kPa, cell9.525mm. Aramid is **HRH-10-4.8-32**,32kg/m³, Ec76MPa, W shear14MPa, crush1MPa, cell4.8mm. The old019 aluminium core was1/4-1.6; it is deliberately replaced here by the ordered021 core. Typical core data remain QUESTIONABLE. [Hexcel primary sheet, pp.2,5](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf)",
    "",
    "**Design** means E290GPa, compression283MPa, wrinkle coefficient0.33 and the inherited gamma0.2 below Vc2 /1 above it. **021 full** means the historical SR200 lot at E293.6GPa /379.2MPa, wrinkle coefficient0.82, and gamma=0.2+0.4min(Vc,2). The second set is a separate structural optimism, not another weather forecast. Both use inherited ν0.33. The historical strength is not a current sheet guarantee. [021 revision1](../../../..//../ref-4189c1615990eb515921/.ship/work/outputs/vacuum-mainline021-optimistic-floating-point-1020/CARD.md)",
    "",
    "Every point is re-optimised on **its own** mass line for global buckling, face compression, core crush, crimp, wrinkling, equibiaxial dimpling and joint net-section compression. Joint efficiencies0.9/0.6 come from020's optimistic/conservative screen; they affect only the joint compression mode. Factors use the high-pressure end (+1%/+2%) with no internal-pressure structural relief. Float mass uses the hot, low-pressure, humid end. These are envelope checks, not simultaneous weather states. Reserve excludes payload and retains the original100kg systems /5%-of-structure joint allowances as floors.",
    "",
    "## Each budget row's law",
    "",
    "| Row | Held / scaled quantity | Mass law before allowance credit | Tag |",
    "|---|---|---|---|",
    "| Passive vacuum/power/controls |15+10+5kg,24h sealed-service assumption |R⁰;100kg baseline system floor retained |PROJECTION |",
    "| Active vacuum package, literal fixed-system screen |223kg pump,20kg controls,1223.333kg battery |R⁰; only excess over100kg charged |QUESTIONABLE; capacity fails aboveR10 under inherited gas load |",
    "| Active capacity-corrected variant |240m³/h modules at320K gas,24h at5500W each +5W monitoring |ceil(196.03558(R/10)³/240) modules; power/battery follow count;20kg controls fixed |PROJECTION |",
    "| Retained water |0.1/1mm whole-area equivalent,1000kg/m³ |R² |QUESTIONABLE |",
    "| Contamination |5/25kg atR10 spread over area |R² |QUESTIONABLE |",
    "| Extra coatings |zero independently added in baseline;0.1kg/m² sensitivity |R² for fixed coating thickness |QUESTIONABLE scope choice |",
    "| Two face/core bond films |020:0.146473/0.292946kg/m² per interface |R² |QUESTIONABLE material; PROJECTION installed bond |",
    "| Seam length at020 panel size |a×b=0.6096×1.8288 /0.3048×0.6096m; length=A(1/a+1/b) |R² |PROJECTION |",
    f"| Frozen020 seams, requested screen |{I['scenarios']['optimistic']['seam_kg_m2_frozen_020']:.6f}/{I['scenarios']['conservative']['seam_kg_m2_frozen_020']:.6f}kg per hull m² at009c5 gauges |R², only while seam cross-section stays fixed |PROJECTION |",
    "| Resized020 Be doubler/core gap |two full-gauge straps,60/120mm wide;1/2mm paste gap through actual core |A·tf andA·tc, approachingR³ under structural similarity |PROJECTION |",
    "| Seam adhesive/sealant |020 film, width and bead area fixed |R² |PROJECTION |",
    "| Temperature/pressure loss |sameT andfractionalp envelope |R³ |QUESTIONABLE |",
    "| Humidity loss |samevapour partial pressure |R³ |QUESTIONABLE |",
    "| Internal air |1% of reference lift |R³ |QUESTIONABLE |",
    "| Payload |searched independently until every modelledSF≥1 |solution, not a prescribed% |PROJECTION |",
    "",
    "Joining is charged as `max(0, actual joining −0.05×structural mass)` in reserve. It is not added again on top of the entire existing allowance. See [METHOD.md](METHOD.md) for exact closure and formulas, and [SCALE-ROWS.csv](SCALE-ROWS.csv) for every row at every radius. No phantom negative reserve credit is taken when an allowance exceeds actual mass.",
    "",
    "## P2 with resized020 seams",
    "",
    "Both material settings are separately re-optimised. Reserve shares therefore differ slightly between them. `none` means even the zero-payload point failsSF1; it does not assert a zero-payload safe vehicle.",
]
for scenario in ("optimistic","conservative"):
    lines+=["",f"### {scenario.capitalize()} budget; fixed system package","",
            "| Rm | Family | Design reserve% | Design leastSF |021-full reserve% |021-full leastSF | Payload atSF1,021-full kg |",
            "|---:|---|---:|---:|---:|---:|---:|"]
    for r in I["radii_m"]:
        for fam in ("aluminium","aramid"):
            p=get(r,scenario,fam); b=get(r,scenario,fam,"chain_design")
            lines.append(f"|{r:g}|{fam}|{100*b['reserve_fraction']:.4f}|{b['least_SF']:.6f}|{100*p['reserve_fraction']:.4f}|{p['least_SF']:.6f}|{pay(p)}|")
lines += [
    "",
    "The optimistic aluminium021-full points balance global buckling and joint compression. Aramid balances global/crimp and joint compression; its design-property points instead balance crimp and wrinkling. The conservativeR10 mathematical solutions have extremely thin faces and very low dimpling/global factors; they are not manufacturable configurations established by this study.",
    "",
    "**The fixed conservative systems table is a scaling diagnostic, not a qualified operating package aboveR10.** At the inherited one-percent-volume/day gas load, one pump's240m³/h catalog speed fails already atR15. Keeping its mass fixed would require gas-load limits to tighten with radius. The corrected variant budgets whole parallel modules and batteries:",
    "",
    "| Rm | Modules | Design reserve% Al / Ar | Design leastSF Al / Ar |021-full leastSF Al / Ar |",
    "|---:|---:|---:|---:|---:|",
]
for r in I["radii_m"]:
    a=get(r,"conservative","aluminium","chain_design","coupled_pump_scaled")
    b=get(r,"conservative","aramid","chain_design","coupled_pump_scaled")
    aa=get(r,"conservative","aluminium","full_021","coupled_pump_scaled")
    bb=get(r,"conservative","aramid","full_021","coupled_pump_scaled")
    lines.append(f"|{r:g}|{a['environment']['systems']['modules']}|{100*a['reserve_fraction']:.3f} /{100*b['reserve_fraction']:.3f}|{a['least_SF']:.6f} /{b['least_SF']:.6f}|{aa['least_SF']:.6f} /{bb['least_SF']:.6f}|")
lines+= [
    "",
    "All capacity-corrected conservative points failSF1 and have no nonnegative payload atSF1. Modules are only a transparent bound on hardware/power: pressure-dependent installed speed, manifold losses, cooling and the leak law remain open. A sealed-service hull can instead retain the fixed30kg optimistic package **only conditional on** the stated leak and thermal acceptance test. The allowed normalized total gas load grows40.7195→5089.9363Pa·m³/s fromR10→50 for a10Pa start,320K gas limit and0.01p₀ ceiling; this is an acceptance condition, not a prediction of leakage.",
    "",
    "### What the literal fixed areal020 screen would say",
    "",
    "This holds020's seam cross-sections at the old009c5 gauges even when the new faces become much thicker. It is supplied because the brief asks for the area scaling; the resized-seam tables above are the load-transfer comparison to use.",
    "",
    "| Rm | Optimistic reserve% |021-full SF Al / Ar | Conservative reserve% |021-full SF Al / Ar |",
    "|---:|---:|---:|---:|---:|",
]
for r in I["radii_m"]:
    a=get(r,"optimistic","aluminium",mass="fixed_areal"); b=get(r,"optimistic","aramid",mass="fixed_areal")
    c=get(r,"conservative","aluminium",mass="fixed_areal");e=get(r,"conservative","aramid",mass="fixed_areal")
    cm=f"{100*c['reserve_fraction']:.4f}" if c["feasible"] else "no mass line"
    cf=f"{c['least_SF']:.6f} /{e['least_SF']:.6f}" if c["feasible"] else "infeasible"
    lines.append(f"|{r:g}|{100*a['reserve_fraction']:.4f}|{a['least_SF']:.6f} /{b['least_SF']:.6f}|{cm}|{cf}|")
lines += [
    "",
    "### Aluminium family check",
    "",
    f"A separate{len(CAT['all_scores'])}-search sweep checks{CAT['candidate_count']} inherited aluminium rows, of which{CAT['same_sheet_modulus_count']} have same-sheet modulus data. The remaining Plascore rows transfer Hexcel modulus and use bare compression as the crush proxy; they remain QUESTIONABLE sensitivities. The full021 optimistic winner and its payload stay **5056 3/8-1.0 at every radius**. With design properties, the best core switches back to **5056 1/4-1.6**:",
    "",
    "| Rm | Family-best design leastSF, optimistic budget | Selected021-core leastSF | Family-best reserve% |",
    "|---:|---:|---:|---:|",
]
for r in I["radii_m"]:
    p=next(x for x in CAT["best_points"] if x["radius_m"]==r and x["scenario"]=="optimistic" and x["mechanical"]=="chain_design")
    b=get(r,"optimistic","aluminium","chain_design")
    lines.append(f"|{r:g}|{p['least_SF']:.6f}|{b['least_SF']:.6f}|{100*p['reserve_fraction']:.4f}|")
lines += ["","No design-property aluminium row reachesSF1 in either budget; no conservative row reaches it even with full021. [CATALOGUE.json](CATALOGUE.json) carries all candidates, scores, best geometries and independently reoptimised payload maxima."]
lines += [
    "",
    "## OptionalP3: SiC arc frame",
    "",
    "The011b equilateral continuum is re-optimised, with arc bays0.4–3m, outer tube radius≤min(0.25m,s/3), fixed80µm film, film allowable1.5GPa, SiC E410GPa /compression3900MPa, globalk0.2, Perry imperfectiona₀=s/1000,20g/node, and joints5% of tube mass. Each new sphere recounts `N=8πR²/(√3s²)+2` nodes and `3N−6` members. Tube area comes from the remaining mass after film, nodes, joints,50kg baseline systems and the same019 weather/water/contamination/gas budget. P3 does not receive Be face/core bond films: its frame/film attachment masses are unresolved inside the inherited joint assumption.",
    "",
    "| Rm | Optimistic reserve% | Optimistic leastSF | Payload atSF1kg | Baym | Outer radiusmm | Conservative SF fixed /scaled pumps |",
    "|---:|---:|---:|---:|---:|---:|---:|",
]
for r in I["radii_m"]:
    p=next(x for x in F["P3"] if x["radius_m"]==r and x["scenario"]=="optimistic")
    c=next(x for x in F["P3"] if x["radius_m"]==r and x["scenario"]=="conservative" and not x["pump_scaled"])
    b=next(x for x in F["P3"] if x["radius_m"]==r and x["scenario"]=="conservative" and x["pump_scaled"])
    lines.append(f"|{r:g}|{100*p['reserve_fraction']:.4f}|{p['least_SF']:.6f}|{pay(p)}|{p['s_m']:.4f}|{1000*p['ro_m']:.3f}|{c['least_SF']:.6f} /{b['least_SF']:.6f}|")
lines += [
    "",
    "TheseP3 passes are **PROJECTION**. The380MPa flexural-strength sensitivity gives leastSF0.23692→0.25174 overR10→50. It is a separate strength screen, not a replacement compression allowable.20g/node, the ceramic joints, thin curved tubes and membrane assumptions have not been grounded. The supplier's standard seal-tube example is typically12in long and distinguishes3900MPa compression from380MPa four-point flexure. Its current modulus is430GPa; this continuation retains011b's410GPa for comparison. [Saint-Gobain seal tubes](https://www.ceramicsrefractories.saint-gobain.com/products/shapes/tubes/hexoloy-seal-tubes), [SiC primary technical sheet](https://www.saint-gobain.co.jp/jp/documents/zhipintetashito/hexoloy-sa-sic-en-1013-tds-215398.pdf)",
    "",
    "For a **separate similarity check**, all011b member lengths, radii and walls scale withR; member count stays fixed, tubes/joint fraction scaleR³, but film thickness stays80µm and film mass scalesR². Structural factors stay constant while filmSF falls as1/R: nominal leastSF atR10,15,20,30,50 becomes1.22553,0.82161,0.61621,0.41080,0.24648. Film reachesSF1 atR≈12.324m before weather. Those are shape-scaling diagnostics, not mass-closed payload points. A genuinely similar film would need thickness∝R, losing its area-mass advantage. Similar solid nodes would also need mass per node∝R³; the simple diagnostic holds the inherited20g count and identifies that limit.",
    "",
    "## Limits on going bigger",
    "",
    "- **QUESTIONABLE/PROJECTION: sheet and panel production.**020's large stock dimensions become less speculative at gauges≥1.4986mm, but material grade, compound forming, gauge and installed tolerances remain unverified. Both enhancedP2 families are below this threshold atR20 and above it atR30. Panel count still grows with area: the optimistic lower bound rises1128→28180 pieces per skin, and coincident seam length2.749→68.714km. R50 aluminium carries about435.16tonnes of Be faces, before splice straps. [SR200 supplier sheet, p.3](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6)",
    "- **PROJECTION: assembly and ground handling.**Diameter20→100m requires matching clearance, supports and handling loads. Projected areaπR² grows314.16→7853.98m². At the same wind speed anddrag coefficient, force grows25-fold and a moment with lever armR grows125-fold. This follows dimensional mechanics; no drag coefficient or mooring design is supplied. Local attachment, landing and asymmetric-pressure modes are unscored.",
    "- **QUESTIONABLE: P2 modes.**For tf,tc∝R at fixed material andcell size, global/face/crimp/wrinkle/crush factors are size-invariant; fixed-cell dimpling improves asR². In particular crimp pressure∝h²/(Rtc) is constant, not intrinsically improved or worsened byR. If face/core gauges are held instead, global falls asR⁻² and face/crimp/wrinkle/dimpling asR⁻¹. Any core-depth or gauge cap can therefore reverse the apparent size benefit.",
    "- **PROJECTION: P3 modes and components.**With fixed bay and capped tube radius, global lattice capacity eventually falls roughly as1/R. The0.25m radius cap is active atR30 and50. With similar growing bays and fixed film, film failure worsens as1/R. The20g node law cannot establish load capacity as node/member forces increase.",
    "- **QUESTIONABLE: operational and material limits.**Coatings, hardpoints, thermal gradients, internal heating, icing, leak/outgas and dimensional defects have no radius-independent guarantee. An extra0.1kg/m² consumes125.66→3141.59kg across this radius range. TheR20 aluminium209.84kg payload is only41.75g/m² of extra areal mass; this narrow pass is especially fragile. Full021 with gamma held at0.2 failsSF1 at every sampled radius for both cores.",
    "",
    "## Verification and filing",
    "",
    f"{V['pins_reverified']} input pins verified. Both020 join totals reproduce968.197361 and3721.996275kg; three revised021 geometries reproduce all six modes; the011b SiC point reproduces to{V['source011b_error']:.2g} absoluteSF. {V['P2_dense_grid_checks']} main P2 optima plus{V['catalogue_dense_grid_checks']} catalogue winners were compared with100001 fractions; {V['P3_dense_grid_checks']} P3 optima with801×1001 grids. Independent45-digit scalar checks cover{V['p2_points_including_payload']} P2 and{V['frame_points_including_payload']} P3 geometries including payload points. Maximum pressure-factor discrepancy is below1e-12 and mass discrepancy below3e-10kg. These check arithmetic, not the physical assumptions.",
    "",
    "[RESULTS.json](RESULTS.json), [FRAME.json](FRAME.json), [INPUTS.json](INPUTS.json), [NFI.json](NFI.json), [VALIDATION.json](VALIDATION.json), [METHOD.md](METHOD.md) and [row export](SCALE-ROWS.csv) provide the trace. Seventeen evidence needs remain open. The brief says **stop and file; robotics sends the next job**. No executable successor is named.",
]

# Add spaces at prose word/number boundaries through explicit editorial text,
# without altering technical tokens or numerical tables.
card="\n".join(lines)+"\n"
for a,b in [
    ("are10,15,20,30,50m","are 10, 15, 20, 30, 50 m"),("inherited500m","inherited 500 m"),
    ("below5%","below 5%"),("below1","below 1"),("passSF1","pass SF 1"),
    ("every modelledSF","every modelled SF"),("zero-payload safe","zero-payload qualified"),
    ("sameT","same T"),("samevapour","same vapour"),("fractionalp","fractional p"),
    ("OptionalP3","Optional P3"),("TheseP3","These P3"),("enhancedP2","enhanced P2"),
    ("anddrag","and drag"),
]:
    card=card.replace(a,b)
# Use an absolute file link for the exact pinned external card.
card=card.replace("../../../..//../ref-4189c1615990eb515921/.ship/work/outputs/",
                  "unpublished-local-ref:d49761785f6805ea")
(ROOT/"CARD.md").write_text(format_prose(card))

method=r"""# MAINLINE-027 calculation and scope

All material inputs are QUESTIONABLE. Fabrication, joint efficiency, gamma curve,
full-021 material transfer and P3 components are PROJECTION.

The requested radius series is evaluated at one atmosphere: reference R0=10m,
L0=4889.442150186961kg, p0=95460.83791390515Pa, T0=284.9K.
A=4πR², V=4πR³/3, L=L0(R/10)³. No additional altitude change is inferred.

## Budget laws and exact mass closure

The two climatic scenarios retain019's temperature rises10/25.1K, pressure
fractions±.01/±.02 and vapour pressures1000/6000Pa. Moist lift is

    Lhot = L [(1-dp) - .378 e/p0] T0/(T0+dT).

Dry loss uses e=0; humidity is the difference between dry and moist values.
Internal air mass is .01L, retained conservatively with no load relief.
This is an ideal-mixture planning calculation, not a meteorological bound.
Water is Aρδ, with δ=.0001/.001m. Contamination is A times5/25kg divided
by4π(10m)². Extra coating is zero in the main scope and .1kg/m² in a sensitivity.
No statistical contingency is hidden in the word reserve.

020's panel dimensions are held: (.6096,1.8288)m optimistic,
(.3048,.6096)m conservative. Let λ=1/a+1/b, μ be film mass per interface
(.1464728290914915/.292945658182983kg/m²), w=.06/.12m, g=.001/.002m,
and sealant cross-section Ab=1e-5/3e-5m², paste density1100kg/m³.
Both skins are included. At structural mass S and core mass fraction f:

    tf = (1-f)S/(2Aρf), tc = fS/(Aρc)
    m_join = A λ [2ρf tf w + 2μw + 1100 g tc + 1100 Ab] + 2Aμ
           = u(f)S + v
    u(f) = λ[w(1-f) + 1100 g f/ρc]
    v = A[λ(2μw+1100Ab) + 2μ].

The requested frozen-areal screen replaces this with020's original total
joining/A0. Those constants describe the old009c5 gauge only. In the coupled
model, strap/core-gap parts approachR³ if thicknesses scale withR, whereas the
remaining film/adhesive/sealant parts remainR². Neither recipe is a designed joint.

Let B be weather+gas+water+contamination+coating+systems excess, excluding
joining and payload Y. Systems excess=max(0, actual systems-100).
With retained baseline floors the complete equation is

    L = 100 + 1.05S + B + max(0, m_join-.05S) + Y.

For each f, let H=L-100-B-Y. Candidate S0=H/1.05 is accepted if
m_join(S0)<=.05S0. Otherwise S=(H-v)/(1+u). This closes the resized seam
budget analytically at every optimizer evaluation. Negative S is infeasible.
Reported reserve is B+max(0,m_join-.05S), not the remaining free payload.
This makes the physical carried mass equal the hot moist lift after removing
the separate climate opportunity-loss rows. Unused allowances remain reserved.
There is no common margin constraint across families.

The passive systems estimate15+10+5=30kg is fixed. The literal active screen
uses223kg pump+20kg controls+24h(5500+5)W/(150Wh/kg×.8×.9)
=1466.333333kg. With one-percent-volume/day gas load and gas temperature320K,
required inlet speed is(V/24h)(320/T0), equal196.0355776m³/h atR10.
The capacity-aware variant takes N=ceil(required speed/240m³/h),
hardware223Nkg, power5500N+5W and the same battery formula, with20kg controls.
This is an explicit modular projection, not installed-system qualification.
If leak/outgas follows area rather than the inherited volume allowance,
capacity would instead tend toR²; no such measured decomposition is available.
All 24h pumping cases hold the1% internal-gas mass reserve.

Passive total gas throughput, normalized toT0, must not exceed
V[(.01p0)T0/320-10Pa]/86400s to finish below the pressure ceiling after a10Pa
start atT0. This is conditional capacity, not achieved leak tightness.

## P2 structural calculation and search

With h=tf+tc:

    sigma0 = E h/[R sqrt(1-nu²)]
    sigma_crimp = h² Gc/(2tf tc)
    Vc = sigma0/sigma_crimp
    Kc = 1-Vc/4 for Vc<2; 1/Vc otherwise.

Design gamma=.2 below Vc2 and1 at/above2 (021 convention). Full021
gamma=.2+.4min(Vc,2). Flat-gamma sensitivity is.2 throughout.
The inherited discontinuity is not newly justified. Both sides of every
observed Vc=2 crossing are explicit optimizer candidates.

At maximum external pressure p=p0(1+dp), capacities divided by p are:

    global: 4 gamma Kc sigma0 tf/(Rp)
    face: 4 sigma_allow tf/(Rp)
    core crush: 2 core_crush/p
    crimp: 2 h² Gc/(R tc p)
    wrinkle: 4 BX Cw sqrt(E Ec tf³/tc)/(Rp)
    dimpling: 4 E tf³/[(1-nu²)cell² R p]
    joint net section: eta × face SF.

BX is the positive root of BX³+BX=1. Dimpling uses021's equibiaxial half of
the older uniaxial allowable. η=.9/.6 is020's assumed seam screen; it does
not scale global, wrinkle or every other mode. All modes are retained in JSON.
The solver scans4001 fractions, refines all observed local peaks and both
sides of branch switches, and checks the result against100001 fractions.
There is no gauge, core-depth or procurement feasibility constraint hidden in
the optimizer; unrealistic small gauges are explicitly projected.

Payload is an outer feasibility bisection, reoptimizing at every trial. It is
only returned when the zero-payload envelope has leastSF≥1. The lower feasible
side is retained. This is a model maximum, not an operational payload approval.

## P3 continuation

The held bounds are physical bay.4≤s≤3m and outer radius≤min(.25m,s/3).
Nnodes=8πR²/(√3s²)+2; Nmembers=3Nnodes-6; member length=s as in011b.
Spherical arcs are assumed; extra arc/chord length correction is not applied.
Node mass=.02Nnodes, film=A×970kg/m³×80µm, systems floor50kg,
joints=.05×tube mass. Tube mass is the remaining mass divided by1.05, and
section area is tube mass/(Nmembers s×3100kg/m³).

For an annular section with outer/inner radii ro/ri,
I=π(ro⁴-ri⁴)/4, rg²=I/Abar, axial stress=pRs/(2Abar).
Scores are compressionσc/σax, Eulerπ²E rg²/(s²σax),
local.6E(tw/ro)/σax, film2σfilm tfilm/(sp),
PerryσP/σax, and global
.2×4√(3/2)E√(I Abar)/(sR²p).
Perry uses imperfectiona0=s/1000, η=a0 ro/rg²,
φ=[σc+(1+η)σEuler]/2, σP=φ-sqrt(φ²-σcσEuler).
The evaluator uses the algebraically equivalent rationalized root.
E410GPa, compression3900MPa, film1.5GPa remain inherited.
The380MPa strength case and node mass∝R·s sensitivity are separate.
The material is brittle; Perry's applicability and all joints remain open.

A131×401 coarse grid seeds local refinement of distinct peaks, checked against
801×1001. Payload is reoptimized with the same bounds. Bounds intentionally
are not silently expanded at largerR. Therefore this is a bounded continuation
of011b, not a proof of the best conceivable SiC frame.

The independent similarity diagnostic scales source011b s,ro,tw byR/10,
keeping film thickness fixed and separately reporting member and node count.
Its film score falls as1/R, all other modelled structural scores are constant.
If film also scaled in thickness, its mass would becomeR³ and this specific
film penalty would vanish. A different design would have to pay that mass.

## Provenance and validation

prepare_inputs.py verifies53 pins and extracts values without importing old
code. 021 revision1 is used; the superseded original has changed artifacts.
The actual019 filing ID uses lead-sci, despite the brief's lead-sciences spelling.

validate_and_plot.py imports neither numerical solver. It re-derives critical
pressures and carried-mass balances in45-digit Decimal arithmetic, reproduces
020 joining and021 points, and verifies source pins. frame.py separately
reproduces the011b SiC pressure scores. These are in-house arithmetic checks,
not an independent seat review, experiment or structural certification.

Reproduction sequence, working within this output directory:

    python3 prepare_inputs.py
    python3 compute.py
    python3 frame.py
    python3 catalogue.py
    python3 validate_and_plot.py
    python3 build_card.py

Set TMPDIR=unpublished-local-ref:1ffe4110219d37c0 and OPENBLAS_NUM_THREADS=1 for numerical runs.
The scripts write only their own directory; freeze filed outputs.
"""
(ROOT/"METHOD.md").write_text(format_prose(method))
run=json.loads((ROOT/"RUN.json").read_text())
now=datetime.now(ZoneInfo("America/Vancouver"))
run["completed_at"]=now.isoformat(timespec="seconds")
run["elapsed_wall_seconds"]=(now-datetime.fromisoformat(run["started_at"])).total_seconds()
run["scope"]="Full card, analysis, arithmetic checks and documentation; measured elapsed time, no task limit."
(ROOT/"RUN.json").write_text(json.dumps(run,indent=2)+"\n")
print("Built CARD.md, METHOD.md, NFI.json (17 rows), SCALE-ROWS.csv, RUN.json")
