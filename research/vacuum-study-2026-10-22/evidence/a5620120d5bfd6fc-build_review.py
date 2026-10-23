from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import csv,json,math

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
a=read("ARITHMETIC.json");fe=read("FE-SUMMARY.json");s=read("SUPPLEMENT.json")
physics=read("PHYSICAL-CHECKS.json");tol=read("TOLERANCE-ROOTS.json");owner=read("intake/OWNER-RESULTS.json")
findings=[]
def nfi(id,title,evidence,fix):
    findings.append(dict(id=f"C055-{id:02d}",title=title,status="open",blocking=False,
                         tag="QUESTIONABLE / PROJECTION",evidence=evidence,proposed_fix=fix))
nfi(1,"Rig gamma uses the Be denominator for the proposed aluminium article",
    "The article definition requires its own Kc*p_classical. Be p_H=169.207732590530 kPa; 5052-O p_H=174.466866567275 kPa. Sea-level/5m-water gamma is 0.575037552829/0.856083753548 for 5052-O, versus card 0.592910711208/0.882692312307. The latter reproduces on the Be reference.",
    "Label a Be-equivalent reference separately; report measured article gamma against its own section. Specify whether water head is measured above the pole.")
nfi(2,"Stand-in matches one elastic combination, not complete similarity",
    "3.103123575680 mm and yield-demand ratio 0.985992767035 reproduce for the QUESTIONABLE 89.6 MPa tensile proxy. Vc changes from 0.953213852654 to 0.858516900574, biaxial membrane stiffness increases 30.667536%, and the wrinkle margin multiplies by 4.003643932. At 9.318 mm the owner's own core-onset ratio is 1.041532306140, exceeding the text's 'within +2.6%'.",
    "State these changes and the separate 9.318-mm yield/onset ratios; measure the formed/cured 5052-O compression response before claiming a yield interaction match.")
nfi(3,"Published dimple limits are interpolations; direct roots are tighter",
    "Card elastic/outer-face/core-typical/core-minimum amplitudes are 5.823329047944/1.271068488423/2.377335243900/1.802745695209 mm. Independent direct coarse-mesh roots are 5.775402642639/1.221966307286/2.299766860540/1.763033119832 mm. All remain conditional elastic-model diagnostics.",
    "Label interpolation explicitly. Use direct solves with diagnostic and mesh conventions pinned; do not promote either set to a manufacturing allowable.")
nfi(4,"Stress diagnostics and cap-edge crossings are less reproducible than pressure maxima",
    "All 23 named pressure maxima reproduce within 0.001127%; stress-crossing differences reach 1.139% for inner-face yield and 2.551% for core crush. Refining the 5m Be cap from 256x(1f,4c,1f) to 512x(2f,6c,2f) moves inner yield 58.245971 to 52.674434 kPa and crush 59.318692 to 53.785270 kPa, while the pressure maximum stays stable.",
    "Pin stress sampling/rotation conventions; retain the edge as unresolved. Model a finite reinforced edge and check local convergence before using an edge allowable.")
nfi(5,"The R30-similar article cannot use the specified B tooling unchanged",
    "D requires a 6m cap; B specifies a 5.4m mould and a 5m tank. The 6m cap has 1.4505436 times the area and about 498 kg of matching aluminium faces, versus 331.852 kg for B. The owner's 15m full-R30 statement corresponds to a 5m R10 cap; its selected 6m similar cap corresponds to 18m.",
    "Size and price compatible mould, seal ring and tank, or change the article and recompute the boundary effect. Keep D's current price explicitly incomplete.")
nfi(6,"Cost arithmetic agrees for B; C is rounded and D has unallocated allowances",
    "B sums to USD 210000–685000 once, 70000–291000 per article and 420000–1558000 for three. C's literal 58.660260kg basis gives 936602.60–4583013.00, consistent with rounded 1–4.6M. Twice B's per-article lines gives D 140000–582000, not 150000–610000; the extra 10000/28000 is unallocated and cannot establish a tooling upgrade.",
    "Expose contingencies, fabrication yield, edge reinforcement, transport/tax and the larger D rig as separate PROJECTION lines; retain no-quote status.")
nfi(7,"DIC price evidence should use the actual primary award",
    "The cited 180–350k purchase indicator was an AI estimate from an aggregator. The related NIST award 1333ND26PNB30149, dated 2026-09-22, lists total value USD 530000. This is a different procurement scope from a rented or partner-supplied experiment.",
    "Replace the weak purchase-price reference with the primary award and scope distinction. Do not convert it directly into a revised rental or total test cost.")
nfi(8,"SR-200 ductility and available blank dimensions are misstated or incompletely transferred",
    "The owner's post_yield field says about 2–3% elongation. The cited SR-200 sheet datasheet specifies 10% minimum over a one-inch gauge. It allows 0.020–0.058-inch sheet only at reduced width/length; the 0.7946mm face falls in that range. The assumed 0.6096x1.8288m blank and 18-panels-per-face count are not established for it.",
    "Use the sheet-specific tensile requirement without treating it as formed/biaxial fracture data. Re-layout seams and price actual gauges/blanks. Carry CHECK038 and CHECK042 qualifications.")
nfi(9,"Statistics wording and sampling populations need correction",
    "The exact one-sided 90/95 noncentral-t factors reproduce, including k3=6.155281103326 and k10=2.354640131829. At n=3 and CV=10%, the formula gives a finite required mean 1.467373857912, not 'no mean'. It exceeds one only if gamma<=1 is imposed. One cap at each of three different dimple amplitudes is not three iid replicates of one amplitude population.",
    "State any gamma ceiling explicitly; separate model-discrimination tests from population tolerance bounds. The 10% model-agreement acceptance rule is a proposed rule, not a qualification standard established by the NASA precedent.")
nfi(10,"Specified metrology does not establish the smallest waviness target",
    "The proposed 0.1–0.3mm scan precision is 1.33–3.99 times the 0.0751mm end of the waviness requirement. No uncertainty budget, spatial sampling or frequency-band verification is supplied.",
    "Choose and validate metrology for the actual wavelength and tolerance; retain separate gross dimple and short-wave waviness requirements.")
nfi(11,"Core-law instability is reproduced; the reported 7–11kPa range is not the new pair of paths",
    "An independent acoustic-tensor calculation gives pure-simple-shear loss of ellipticity at 0.087740979 MPa (W) and 0.087868882 MPa (L) with E_in=0.01MPa. Interpolating the owner's new R10 paths at 0.088MPa gives 10.126661 and 16.750523kPa for 16.057/9.318mm dimples, not a 7–11kPa pair. The pure-shear threshold is not a full-state stability calculation.",
    "Correct the carried range and preserve the constitutive limitation. Replace the unsourced in-plane law or model cells; do not interpret coarse elastic maxima as physical capacities.")
nfi(12,"Core crush, compression and cure qualifications remain distinct",
    "Hexcel lists W shear 35/25psi typical/minimum and crush 35psi; these reproduce. Its bare and stabilized compression strengths differ from the crush plateau. ASTM C365 explicitly excludes core crush, referring to D7336. CHECK042 also already found that the cited 200F evidence does not qualify the specified adhesive variant and weight.",
    "Witness shear, flatwise compression and crush as separate quantities; specify D7336 where crush is intended. Qualify the actual face/core/bond/cure stack and retain the unresolved Be compression allowable.")
nfi(13,"Reis and R30 similarity conventions must be explicit",
    "The 356.777mm width uses legacy nu=0.33; with Be nu=0.0752 its Reis lambda is about 1.0278. R30 R/t_eq is 164.871, despite R/h=285.565, so the two thickness ratios cannot be interchanged in the thin-shell discussion. R30 FE also uses nu=0.0752 while its 040 source uses 0.0768. These are small arithmetic/convention changes inside a larger unproved sandwich transfer.",
    "Report both ratios and Poisson conventions. Preserve homogeneous neo-Hookean versus sandwich distinctions and compare R30 against its actual 97.172303kPa design load.")
nfi(14,"Cheapest/smallest and qualification claims exceed the tested model scope",
    "The finite-element comparisons omit seams, explicit cells, nonlinear materials, the proposed reinforcement, thermal residuals, water loading gradients and nonaxisymmetric modes. Generic handbook/CMH17 stand-in properties lack edition/page or laminate identification. Hardware listings establish size classes, not a qualified process, booking or quotation.",
    "Describe B as a proposed candidate among the examined options. Keep physical gamma, installed-hull SF and qualified tolerances null; define validated transfer and first-failure mode before applying the outcome bands.")
write("NFI.json",dict(schema=1,unit="vacuum-mainline055-check-1020",blocking=False,rows=findings))

mismatches=[]
def mismatch(row,field,claimed,checked,kind,nfi_id):
    mismatches.append(dict(row=row,field=field,owner=claimed,independent=checked,
                           kind=kind,nfi=f"C055-{nfi_id:02d}"))
mismatch("CARD B / rig reach","sea-level article gamma",.5929107112075593,.5750375528285177,"denominator correction",1)
mismatch("CARD B / rig reach","5m water article gamma",.8826923123071662,.8560837535484669,"denominator correction",1)
mismatch("CARD stand-in faithfulness / 9.318mm","core shear onset increase percent",2.6,
         (owner["stand_in_check"]["dimple 9.318 mm"]["core_shear_onset_ratio"]-1)*100,
         "text inconsistent with own results",2)
for ownkey,newkey in (
    ("elastic gamma_H 0.564164 (R10 need)","elastic_pressure_maximum_at_operating"),
    ("outer face below 345 MPa at operating","outer_face_345MPa"),
    ("core below CR III W typical shear (35 psi) at operating","core_W_typ_35psi"),
    ("core below CR III W minimum shear (25 psi) at operating","core_W_min_25psi")):
    mismatch("RESULTS dimple_tolerance",ownkey,owner["dimple_tolerance_from_fe_mm"][ownkey],
             tol[newkey]["amplitude_mm"],"direct root versus interpolation; conditional",3)
mismatch("N055-05 / 5m cap","inner-face yield kPa",57.61075405976462,
         s["refinement"][1]["refined_crossings"]["face_yield_inner"],"mesh-sensitive local diagnostic",4)
mismatch("N055-05 / 5m cap","core crush kPa",59.07565779899292,
         s["refinement"][1]["refined_crossings"]["core_crush_typ"],"mesh-sensitive local diagnostic",4)
mismatch("CARD D","fits B mould / tank","shared 5.4m mould and 5m tank",
         "6m cap requires larger tooling / tank","unpriced scope",5)
mismatch("RESULTS costs D","USD interval",[150000,610000],[140000,582000],
         "literal twice-B arithmetic; proposed allowance unallocated",6)
mismatch("RESULTS costs B basis","DIC purchase indicator USD",[180000,350000],530000,
         "primary award update, different rental scope",7)
mismatch("RESULTS stand_ins SR-200","elongation percent","about 2–3",10,
         "sheet source correction; one-inch gauge",8)
mismatch("CARD article count","n3 CV10 required mean","no mean will do",1.4673738579121771,
         "finite result; gamma<=1 condition absent",9)
mismatch("N055-04","0.088MPa crossing range kPa",[7,11],
         list(s["owner_path_tau088_crossing_kPa"].values()),"wrong inherited path range",11)
mismatch("CARD precursor core tests","crush standard","C365","D7336/D7336M-22",
         "standard scope correction; retain C365 for flatwise compression",12)
mismatch("RESULTS R30 FE","nu",.0752,.0768,"040 source convention; small effect",13)
write("MISMATCHES.json",mismatches)
with (ROOT/"MISMATCHES.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=list(mismatches[0]));w.writeheader();w.writerows(mismatches)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

caprows="\n".join(f"| {r['diameter_m']} | {r['material']} | {(r['limit_ratio']-1)*100:+.6f}% | {(r['core_shear_onset_ratio']-1)*100:+.6f}% |" for r in s["caps"])
card=f"""# CHECK MAINLINE-055

**Disposition: revise the rig denominator, several source/text claims and the cost scope. The conditional finite-element pressure results reproduce.** All fourteen NFI/fix rows are nonblocking. Everything remains QUESTIONABLE or PROJECTION; qualified gamma, manufacturing tolerances and installed-hull safety factor remain unknown.

**Independence and coverage.** I used my own scalar arithmetic and a newly written axisymmetric Q8 St. Venant–Kirchhoff solver. No foreign owner/predecessor executable was opened, copied, hashed or run. I previously authored 028b and CHECK035; that exposure is disclosed. Twenty independent models cover all 23 filed runs, with three exact-input duplicates checked as aliases. The 735 scalar comparisons reproduce under the owner's conventions. Another 207 endpoint/reference/stress comparisons and 3,985 path-field comparisons retain every numerical delta in the CSV files.

**The 5m cap.** At 16.057mm dimple amplitude, the Be sphere and cap have sampled pressure maxima of 79.405269 and 80.505744kPa: the cap is +1.385895% relative to the sphere. Refining meridional and through-thickness resolution and sampling the peak gives 79.407920 and 80.507711kPa, or +1.384989%. The matching aluminium cap is also close to its aluminium sphere. These are conditional axisymmetric equilibrium branches with uniform pressure and an ideal clamp.

| Diameter, m | Faces | Pressure maximum versus sphere | Typical core-shear onset versus sphere |
|---|---|---:|---:|
{caprows}

**The edge is unresolved.** At the original discretization I obtain inner-face yield at 58.245971kPa and the 35psi core-crush crossing at 59.318692kPa. The finer 5m cap gives 52.674434 and 53.785270kPa. Thus the broad “about 60kPa” warning survives, but its local stress thresholds are not mesh-converged. The proposed reinforcement is absent from both models. No reinforced-cap capacity has been demonstrated.

**The 5052-O match.** The independently derived face gauge is 3.103123575680mm, the core is 20.928718397320mm and the operating stress/yield ratio relative to Be is 0.985992767035. These reproduce 3.10mm and 0.99. The yield proxy is the supplier's 89.6MPa tensile value. Matching classical buckling stiffness while holding face separation changes Vc from 0.953213853 to 0.858516901; biaxial membrane stiffness rises 30.6675% and the wrinkle margin multiplies by 4.00364. The owner's 9.318mm core-onset ratio is +4.15323%, exceeding the prose's “within +2.6%”. Compression after forming/cure and the actual Be sheet response remain unmeasured.

**Rig correction.** Gamma is defined against the article's own Kc times classical pressure. That denominator is 169.207732591kPa for Be and 174.466866567kPa for 5052-O. With a 1kPa internal residual:

| Rig | Card's Be-reference gamma | Correct 5052-O article gamma |
|---|---:|---:|
| Sea-level evacuation | 0.592910711 | 0.575037553 |
| Plus 2m water | 0.708823352 | 0.687456033 |
| Plus 5m water | 0.882692312 | 0.856083754 |
| Plus 10m water | 1.172473913 | 1.137129954 |

The water figures assume head above the pole. Across the 5m cap the hydrostatic differential varies by 3.114020kPa. If “5m” is measured above the base, pole gamma is {s['rig_and_cost_scope']['gamma_5m_water_if_head_from_base']:.9f}. This loading gradient was not included in the uniform-pressure FE.

**Pre-test prediction.** The independently calculated Be sphere gammas are 0.469276837 at 16.057mm and 0.510830131 at 9.318mm, confirming the adverse prediction. All 23 named sampled maxima agree within 0.001127%. Typical W-shear crossings are 24.941256 and 37.821575kPa; they remain far below 95.460838kPa operating pressure. The worst original-mesh stress-crossing differences are 1.139% for inner-face yield and 2.551% for crush; those are preserved, not rounded away.

**Dimple limits.** Every published limit is exactly reproducible as linear interpolation of the owner's six sampled amplitudes. Direct independent solves give:

| Criterion | Card interpolation, mm | Direct solve, mm |
|---|---:|---:|
| Elastic maximum equals operating pressure | 5.823329048 | 5.775402643 |
| Outer face reaches 345MPa | 1.271068488 | 1.221966307 |
| Core reaches typical W shear, 35psi | 2.377335244 | 2.299766861 |
| Core reaches minimum W shear, 25psi | 1.802745695 | 1.763033120 |

These tighter numbers remain conditional model results. They are not allowable tolerances. The model's unsourced in-plane core law loses ellipticity under pure simple shear at 0.087741MPa in W, independently corroborating CHECK029. The new owner's paths cross 0.088MPa at 10.126661/16.750523kPa, not the carried 7–11kPa range. A full-state stability limit would require more than this pure-shear diagnostic.

**Scaling and R30.** R10 h=24.031841973mm, t_eq=41.624371297mm, R/h=416.114587 and R/t_eq=240.243869 reproduce. For R30, R/h=285.564976 but R/t_eq=164.871016; these ratios cannot be interchanged in the homogeneous-shell thin-limit argument. The 356.777mm width follows legacy nu=0.33; using Be nu=0.0752 in the same definition makes lambda about 1.0278. R30's FE uses 0.0752 while 040 uses 0.0768. Exact 040 ISA gamma range 0.373384057–0.418418964 and optimistic-weather range 0.459155504–0.529460764 support the rounded outcome bands. Those bands still require a validated article-to-hull transfer and identified first mode.

**Costs.** B's build-up is correct: USD 210000–685000 once, 70000–291000 per article, total 420000–1558000 for three. Its ideal aluminium face mass is 331.851974kg. C uses 58.660260kg Be; the literal assumed rates and add-ons give USD 936603–4583013, reasonably rounded to 1–4.6M. D's literal twice-B lines total 140000–582000, leaving 10000/28000 unexplained in its quoted 150000–610000 interval. More seriously, D's 6m article cannot use B's 5.4m mould and 5m tank unchanged; it has 45.05% more area and about {s['rig_and_cost_scope']['D_face_mass_kg']:.1f}kg of aluminium faces. A shared enlarged rig needs an explicit revised scope. All costs remain unquoted projections.

**Sources and test interpretation.** The cited [SR-200 sheet datasheet](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6) gives 10% minimum elongation over one inch, correcting the table's 2–3%. Its reduced-gauge stock restriction also leaves the assumed full-size blanks unestablished. The [related NIST DIC award](https://sam.gov/workspace/contract/opp/b3c6ad81649c467d86d2a44fbc4750a4/view) is USD 530000, replacing the weak 180–350k aggregator estimate as a purchase indicator; rental scope is separate. [ASTM C365](https://store.astm.org/c0365_c0365m-22.html) excludes crush testing and points to D7336. The proposed 0.1–0.3mm scan precision does not establish the 0.0751mm waviness target.

**Statistics.** Exact one-sided 90/95 normal factors and the 0.814988 mean at n=3/CV=5% reproduce. At CV=10%, n=3 requires finite mean 1.467374; “no mean” needs an explicit gamma<=1 restriction. Ten tests at CV=10% require 0.737917. Three different seeded amplitudes are three model-discrimination cases, not three iid replicates of one amplitude. NASA's eight-subscale/two-full-scale cylinder precedent does not establish the proposed three-article/10%-agreement qualification rule.

**Carry and completion.** CHECK035's S-II graph readings remain about 0.21–0.22 with roughly ±0.01 reading uncertainty; the broader 0.21–0.25 decision band is not a new measured range. CHECK038/042's blank-size, adhesive/cure, inspection and unmeasured-shape qualifications carry. Generic handbook stand-ins, custom geometry, material processing and all costs remain QUESTIONABLE/PROJECTION. This check is complete; the brief says stop and file. No supplier, laboratory or other seat was contacted, and no successor is selected.
"""
(ROOT/"CARD.md").write_text(card)
print(json.dumps({"nfis":len(findings),"headline_mismatches":len(mismatches),
                  "card_words":len(card.split()),"fe_comparisons":fe["scalar_comparisons"],
                  "path_comparisons":fe["path_comparisons"]}))
