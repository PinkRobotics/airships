from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,math,csv,hashlib
from check45 import ROOT,save,soft_depth,score,AREA,TF,TC,N,DF,CRUSH,growth

load=lambda name:json.loads((ROOT/name).read_text())
a=load("ARITHMETIC.json");c=load("inputs/owner/COMPUTE.json");l=load("LEAK-RESULTS.json")
aud=load("AUDIT-CHECKS.json");fc=load("FRAME-CHECKS.json")
frame_checks=[x for x in fc if "/radial_planar/" in x["path"]]
frame=load("FRAME-RESULTS.json")["radial_planar"];prose=load("PROSE-CROSS-CHECKS.json")
checks=load("ARITHMETIC-CHECKS.json")+load("LEAK-CHECKS.json")+frame_checks+aud
differences=[]
for item in checks:
    if item["pass_"]:continue
    path=item["path"]
    category="arithmetic_or_label"
    if "/p3/pricing/" in path or "/stop_25mm_slit/" in path:category="search_witness_difference"
    elif "/strikes_to_half_shi/" in path:category="rare_event_approximation"
    elif "/t_first_half_kg_s" in path:category="sampled_event_time"
    differences.append({**item,"category":category})
iec=[]
for i,mass in [(1,.0207),(3,.0802),(4,.1320)]:
    old=c["threats"]["hail_iec"][i];energy=.5*mass*old["v_m_s"]**2
    dent,b=soft_depth(old["D_m"]/2,energy=energy)
    row=dict(index=i,diameter_m=old["D_m"],owner_mass_kg=old["m_kg"],table_mass_kg=mass,
             owner_energy_J=old["E_J"],table_energy_J=energy,
             owner_depth_m=c["p2"]["threats"][i]["readings"]["all energy to the panel"]["depth_m"],
             corrected_depth_m=dent,corrected_growth=score(dent,b))
    iec.append(row)
    for field,value in [("m_kg",mass),("E_J",energy)]:
        differences.append(dict(path=f"COMPUTE/threats/hail_iec/{i}/{field}",owner=old[field],
          independent=value,difference=value-old[field],category="primary_source_input",
          note="IEC 61215-2:2016 Table 3 prints all six masses; original computation substituted constant-density masses."))
save("IEC-MASS-CORRECTIONS.json",iec)

prose_errors=[
 dict(path="CARD/P2 growth table/55 mm/clamped",owner="deeper than the core",
      independent="19.176311 mm, below the 23.237218 mm core depth",category="prose"),
 dict(path="NFI-045-DENT-MODEL/calibration",owner="model reads Pach within 1.1–1.2 mm and 30 mm",
      independent="model is 1.489009–1.541057 mm deep, 21.879845–27.046444 mm wide; test is 1.1–1.2 mm by about 30 mm",category="prose"),
 dict(path="CARD/P2 response/all impact dent width range",owner="lambda 0.077–0.258",
      independent="hail 0.077170–0.147242; tools 0.061648–0.077394; 8 lb bird reaches 0.314510; mooring 0.700718",category="prose"),
 dict(path="CARD/Detection/laser",owner="resolves 0.2 mm contours",
      independent="0.2 mm is a plotted contour interval and dent-diameter threshold, not a demonstrated detection resolution or PoD",category="source_scope"),
 dict(path="CARD/Threats/IEC masses",owner="table does not print the 35/55/65 mm masses",
      independent="Table 3 prints 20.7/80.2/132.0 g",category="source_scope"),
 dict(path="CARD/Puncture and leak/torn-bay heaviness",owner="about 5131 kg heavy",
      independent=f"5130.39–5130.88 kg is admitted gas; net downward buoyancy deficit at the model ground is {min(prose['bay_net_heaviness_at_zero_centre_height_kg']):.6f}–{max(prose['bay_net_heaviness_at_zero_centre_height_kg']):.6f} kg",category="quantity_definition"),
 dict(path="CARD/P3 hail table/25 mm/strikes to 50 percent, lower end",owner=484,
      independent=485,category="integer_probability_threshold",
      note="Exact independent-trial real count is about 484.102; round upward to reach at least 50%."),
]
differences.extend(prose_errors)
for row in load("TRUSS-RANK-CHECKS.json"):
    for state in ["intact","damaged"]:
        differences.append(dict(path=f"DET/frame/f{row['frequency']}/pinned_{'intact_cond' if state=='intact' else 'one_gone_cond'}",
            owner=row[f"owner_{state}_condition"],
            independent=row["intact_condition_after_orthogonal_rigid_mode_projection"] if state=="intact" else None,
            category="matrix_representation_unspecified",
            note=row["comparison_scope"]+(" Damaged condition is mathematically infinite." if state=="damaged" else "")))
save("NUMERICAL-CHECKS.json",checks)
save("MISMATCHES.json",differences)

nfis=[]
def nfi(suffix,title,claim,fix,kind="QUESTIONABLE",refs=None):
    nfis.append(dict(id="NFI-CHECK045-"+suffix,status="OPEN",blocking=False,tag=kind,title=title,
                     finding=claim,proposed_fix=fix,refs=refs or []))
nfi("PACH","Test units and calibration description",
    "The stored Pach test_depth_m is 1.1 instead of 0.0011. The claimed agreement with the measured 1.1–1.2 mm range is false: the model predicts 1.489–1.541 mm, and it is a peak-depth model compared with a residual dent.",
    "Correct the unit field; report the 24–40% depth overprediction relative to the stated test range and the peak/residual distinction.",
    refs=["MISMATCHES.json","sources/pach_full.pdf"])
nfi("IEC","Printed hail masses were replaced unnecessarily",
    "IEC Table 3 supplies all six masses. The substituted 35/55/65 mm masses and energies differ from the printed inputs.",
    "Use 20.7/80.2/132.0 g and 7.657344/46.083321/88.894740 J; carry the recomputed all-energy dents. The 50.8 mm design case is unchanged.",
    refs=["IEC-MASS-CORRECTIONS.json","sources/iec-table3.png"])
nfi("GROWTH-TABLE","55 mm growth entry",
    "The clamped 55 mm threshold is 19.176311 mm, not deeper than the 23.237218 mm core.",
    "Correct the table cell; keep its model and boundary qualifications.",refs=["PROSE-CROSS-CHECKS.json"])
nfi("PERRY","Perry factor does not follow the cited equation",
    "The filed 4.095817936 differs from 3.454499160 obtained from the stated L/1000 bow, direct magnified bending and an independent quadratic root. The pinned 022d table also gives 3.454499160.",
    "Replace the non-governing factor and add the direct-stress check. The overall nominal 1.258252477 is unchanged.",
    refs=["AUDIT-CHECKS.json","inputs/upstream/022d_tables_csv/TABLES.csv"])
nfi("STRIKES","Repeated-strike probability and approximation",
    "The stored count is ln(2)/Pf. For independent equal-risk trials the exact real-valued 50% count is ln(2)/[-ln(1-Pf)]. The design case changes 61.224523/13.134564 to 60.877292/12.784859. Repeated identical loading of the same Weibull specimen is not automatically an independent trial.",
    "Label the rare-event approximation and provide exact counts and integer ceilings: the 25 mm sectored-flexure lower bound is 485, not 484. Define strike location/damage history before treating counts as storm reliability.",
    "PROJECTION",["ARITHMETIC-DIFFERENCES.json"])
nfi("SEARCH","Additional feasible P3 witnesses",
    "The published priced witnesses reproduce, but a separate multistart search finds better points. Walls 1.5/2.0/3.0 mm yield SF 0.805476/0.483053/0.223304 versus 0.800189/0.469060/null. At 303.532 MPa film allowable, SF 0.975445 uses 848.604 kg film, versus 0.975205 and 880.534 kg.",
    "Retain filed points as local witnesses, add the independently verified alternatives and distinguish an unsuccessful search from an infeasibility proof. None of these wall/tear cases reaches SF 1.",
    "PROJECTION",["FILED-WITNESS-CHECKS.json","NEW-WITNESS-INVARIANTS.json"])
nfi("FEASIBILITY","Usage above one marked feasible",
    "Two patch-price rows and all four denser-core rows have feasible=true although their optimism usage exceeds one; 028b explicitly excludes that interpretation.",
    "Set design-feasible=false or rename the flag to geometry_solved, preserving the numeric usage.",refs=["MISMATCHES.json"])
nfi("LEAK-EVENT","First half-kilogram times are sampled too late",
    "Twenty-four stored event-time fields differ outside tolerance. A 100 mm hole reaches 0.5 kg at 0.464206 s, not 0.770164 s; the torn bay reaches it at 0.000837478 s, not 0.001535376 s.",
    "Root mass(t)-0.5 using dense output or an event function. Main touchdown and flow conclusions reproduce.",
    refs=["LEAK-DIFFERENCES.json"])
nfi("WIDTH-RANGE","Summary excludes small tools and the 8 lb bird",
    "The stated lambda range 0.077–0.258 omits the small-tool 0.061648 and 8 lb bird 0.314510. Both still lie below the adopted 0.630970 map cutoff.",
    "State threat-specific ranges and retain the distinction between crushed diameter and dent depth.",
    refs=["inputs/owner/COMPUTE.json"])
nfi("NDI","Contour interval is not detection performance",
    "The primary Prior thesis uses 0.2 mm contours as a dent-diameter measurement threshold. It does not establish 0.2 mm detection resolution or reliable identification of critical damage. Tap-test values are disbond PoD on aluminium.",
    "Report the measurement definition and retain unknown Be/SiC/PBO detection capability.",
    refs=["sources/prior_full.pdf","sources/tap_manual.pdf"])
nfi("FRAME","Four selected removals do not bound all damage cases",
    "All 56 reported frame comparisons reproduce with radial loads based on planar triangle areas. Across six f4 and nine f5 edge classes the stress ratio spans 1.959485–3.270739 and peak tension 0–1019.372 MPa. A static rigid-joint calculation does not prove a dynamic cascade after every possible member loss.",
    "Pin mesh, pressure quadrature, joint model and removed edges; distinguish selected cases from an envelope. Keep nonlinear and installed-joint verification open.",
    refs=["FRAME-RESULTS.json","FRAME-MESH-f4.json","FRAME-MESH-f5.json"])
nfi("FILM","Projected fracture screen stated as a certainty",
    "The slit lengths and 0.838835 merged-bay SF reproduce, but substitute-polymer toughness and assumed effective modulus do not demonstrate that every puncture opens an installed PBO bay.",
    "Use conditional fracture-screen language. Installed orthotropic film toughness, notch response, prestress and arrest features remain unknown.",
    "PROJECTION",["inputs/owner/NFI.json","ARITHMETIC-CHECKS.json"])
nfi("TRAJECTORY","Ground contact, inventory and heaviness conventions",
    "The trajectory assumes a neutral full sphere at 500 m with non-air mass 4889.444 kg, rather than proving the built 028b/022d inventory. Centre altitude zero is also ten metres below first contact for an R10 sphere. About 5131 kg is incoming gas, not the net buoyancy deficit.",
    "Specify carried inventory, sagged displacement and initial restraint; stop at centre height 10 m above terrain. For the same gross reference, torn-bay first-contact speeds remain 23.099647–34.541863 m/s and net heaviness about 4889 kg.",
    "PROJECTION",["GROUND-CONTACT-SENSITIVITY.json","PROSE-CROSS-CHECKS.json"])
nfi("VENT","Venting is a conditional load reduction, not a qualified operation",
    "The 0.458903732 pressure fraction and 2645.660029 kg use the 500 m full-volume state. At sea-level ISA the same absolute differential requires 2912.791114 kg on that convention. Venting an airborne neutral hull makes it descend; it needs a supported landing/handling sequence. Regulatory speeds are analogous test criteria, not established safe hull speeds.",
    "Retain the arithmetic and require explicit terrain, support, gas volume, atmosphere and valve control. Do not infer a 500 m AGL operating condition solely from a 500 m atmospheric design altitude.",
    "PROJECTION",["LEAK-RESULTS.json","PROSE-CROSS-CHECKS.json"])
nfi("RECONSTRUCTION","Unstated modeling choices and material transfers",
    "Exact reproduction needs SiC nu=0.16, core E/G scaled linearly with density in pricing, radial/planar nodal loading, a rounded 48.894 kg gas item, and an integral of the expanding hard-impact footprint. The artificial growth law, typical core crush and transferred shell/film properties remain unvalidated.",
    "Pin these input conventions and their PROJECTION tags. Keep primary measured properties distinct from transferred allowables and from predictions of installed damage tolerance.",
    "PROJECTION",["METHOD.md","inputs/owner/NFI.json"])
inherited=load("inputs/owner/NFI.json")["items"]
save("NFI.json",dict(status="OPEN",all_nonblocking=True,tag="QUESTIONABLE",
                     new=nfis,inherited=inherited,count_new=len(nfis),count_inherited=len(inherited),
                     count_total=len(nfis)+len(inherited)))

source_notes=[
 ("IEC ice masses","sources/iec_v25.pdf","Table 3, printed page 40; viewed page image","Primary IEC document hosted as a preview; all masses are printed. Three owner substitutions corrected."),
 ("Core properties","sources/cr3_crush.pdf","Printed pp.25–27","35 psi typical crush and ±20% preliminary-design scatter are supported; no installed crush allowable is established."),
 ("Pach test","sources/pach_full.pdf","Sections 2.4 and 3.2.6","1.57 J, 1.1–1.2 mm residual depth, approximately 30 mm width; source supports the test, not the claimed model agreement."),
 ("Clarke FE","sources/clarke_disp.pdf","Core density and material tables","2.37 mm least-dense-core peak displacement is a simulation, not a test. Model uses 503 MPa face yield and an assumed 80% absorbed energy."),
 ("Shi hail calibration","sources/shi_dent.pdf","Tables 3–4 and equation 11a","0.480 mm permanent dent and 6.55% mean work fraction are supported; combining them into a contact multiplier and transferring it to Be/honeycomb are projections."),
 ("SiC statistics","sources/tube_cring.pdf","Printed pp.5–7","299 MPa/m=4.6 and 192 MPa/m=5.5 are characteristic strengths; source explicitly distinguishes flaw orientation, area/volume and material vintage."),
 ("Film fracture inputs","sources/strato_full.pdf; sources/mylar_ewf.pdf; sources/kapton_elm25.pdf","Fracture tables and discussion","500 J/m² low StratoFilm value, PET EWF 40.2/63.7 kJ/m² and 0.07 N Kapton tear support source values. Their use as PBO toughness is unqualified."),
 ("Detection","sources/tap_manual.pdf; sources/prior_full.pdf","Tap Table 4; Prior contour discussion","41.8/29 mm logit a90/95 values are for disbonds; 0.2 mm is a topographic contour threshold."),
 ("Leaks","sources/nasa_choking.html; sources/nasa_orifice_Cd.pdf","NASA mass-flow derivation and seal example","Choked ideal-gas flow and an analogous square-edge Cd=0.60 are supported. Torn-hole Cd and in-service gas behavior remain assumptions."),
 ("Threats","sources/faa_bird_statistics.pdf; sources/nbs_v2.pdf","FAA height statistics; NBS Table 2","FAA PDF currently contains 1990–2025 data despite the 1990–2024 URL; 71% and 35%-per-1000-ft statements match. NBS 105 ft/s and 23.69 ft·lbf support the design hail."),
 ("Regulatory references","sources/cfr_25-571_2025.pdf; sources/cfr_25-631_2025.pdf; sources/cfr_25-473_2025.pdf; sources/cfr_31-27_2025.pdf; sources/cfr_101-13_2025.pdf; sources/cfr_101-19_2025.pdf; sources/tar473.pdf","2025 annual CFR edition; March 2000 TAR","Named masses, heights and test velocities verified in primary historical documents. The 2026 downloads and live eCFR HTTP client access failed; annual text is not a claim of a current approved regulatory route."),
]
save("EVIDENCE.json",dict(metadata_rows=388,selected_values=87,notes=[
 dict(topic=x[0],local=x[1],location=x[2],finding=x[3],tag="QUESTIONABLE") for x in source_notes],
 primary_downloads=load("SOURCE-DOCUMENT-CHECKS.json"),
 secondary_inputs_retained_only_as_assumptions=["ASTM debris values through a manufacturer summary","added-mass and sphere-drag entries cited through Wikipedia; independently treated as declared ideal-fluid/drag assumptions"],
 access_pages_quarantined=True))

counts=dict(total=len(checks),passed=sum(x["pass_"] for x in checks),different=sum(not x["pass_"] for x in checks),
            arithmetic=len(load("ARITHMETIC-CHECKS.json")),trajectory=len(load("LEAK-CHECKS.json")),
            selected_frame=len(frame_checks),audit=len(aud),explicit_findings=len(differences),
            input_pins=len(load("PIN-CHECKS.json")),source_files=len(load("SOURCE-DOCUMENT-CHECKS.json")))
results=dict(status="COMPLETE_WITH_CORRECTIONS",tag="QUESTIONABLE",certification=None,
             installed_damage_tolerance=None,checks=counts,
             main_conclusion="No demonstrated installed damage tolerance for either lead; main conditional danger screens reproduce.",
             p2_patch_critical_diameter_m=a["p2_constants"]["patch"],
             p2_design_hail_depths_m={k:v["depth_m"] for k,v in c["p2"]["threats"][6]["readings"].items()},
             p2_vent_fraction=c["p2"]["pricing"]["design_hail_needs"]["Shi-calibrated k rho v2"]["vent_fraction_dp"],
             p2_vent_air_kg=l["stationary_vent"]["target_mass_kg"],p2_vent_seconds=l["stationary_vent"]["time_s"],
             p3_nominal_SF=a["p3"]["lam"],p3_perry_SF=a["p3"]["modes"]["perry"],
             p3_sampled_frame_reproduced=True,p3_all_orbits_tension_range_MPa=[0.,max(x["tension_max_Pa"] for f in frame.values() for x in f["cases"])/1e6],
             hole_threshold_m=l["thresholds"],nfi_new=len(nfis),nfi_inherited=len(inherited),
             all_nfi_nonblocking=True,owner_code_read_or_run=False)
save("RESULTS.json",results)
save("RUN.json",dict(start=load("START.json"),computed_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat(),
  routines=["check45.py","frame45.py","truss45.py","leak45.py","audit45.py","plot45.py","assemble45.py"],
  input_source="only pinned non-code artifacts and primary documents",execution="own independent programs",
  tests="equation reconstruction, forward witness scoring, independent quadratic/section/mass checks, mesh symmetry classes, event roots and evidence pins",
  no_time_budget=True,no_external_seat_contact=True,no_successor_named=True))

method="""# CHECK-045 method

All installed-assembly conclusions remain QUESTIONABLE. Material transfers,
life-independent fracture probabilities and operating scenarios are PROJECTION.
This check neither changes the owner's files nor grants an allowable.

The owner report, checker order, requested briefs and fifteen additional
non-code upstream inputs were copied and SHA-256/byte checked. Nine named
owner/predecessor code artifacts were not opened, copied, hashed, imported or
executed. Their supplied metadata is retained in UNREAD-CODE.json. No other
seat was contacted. Acknowledgment and completion are ordinary queue filings.

All 36 frozen inputs still match their intake pins. The final original-file
recheck found one later COMMON amendment about retrying refused simulation
jobs; the other 35 originals remain identical. INPUT-DRIFT.json records the
amendment and its separate snapshot. It changes no scientific input, and no
unfinished simulation job remains. PIN-CHECKS.json preserves the earlier
72-of-72 check; VALIDATION.json records the final delivery check separately.

`check45.py` reconstructs the equations from the cards, 028b METHOD, 022d
METHOD and primary inputs. The owner JSON is an expected-value ledger, never
a source of executable functions. `frame45.py` builds a new mesh and beam
stiffness matrix; `leak45.py` integrates its own differential equations;
`audit45.py` checks input identity, source selection, the filed design
witnesses and independently expanded cross-form invariants.

P2 uses R=10 m, p=95460.837913905 Pa, lift=4889.442150187 kg, E=290 GPa,
rho_face=1850 kg/m³, nu=.0752 and the fixed 019 reserve 411.298944072 kg.
The 028b scarf shear screen gives sigma_face=10 MPa×901/30 and
tf=pR/(4 sigma_face). Core thickness solves the complete structural,
max(5% allowance, physical joining), 100 kg systems and reserve balance.
The nominal point is tf=.794624067 mm, tc=23.237217906 mm,
gamma=.564163567 and usage=.971977517. All modes and joining follow
the pinned 028b method. Denser-core pricing only reproduces with
Ec and Gc multiplied by density ratio k; crush uses k^(5/3). Those are
additional material projections, not product data.

For the patch, N=pR/4; D=Etf³/[12(1−nu²)]; q0=p−2N/R.
The clamped eigenvalue is the first positive root of J1, 3.831706;
the simply supported one solves xJ0(x)−(1−nu)J1(x)=0.
Critical diameter is 2x√(D/N). The owner's proposed growth depth is
(crush−q0)b²/[4(N−x²D/b²)] when the denominator is positive.
Below that eigenvalue threshold this *model* returns no growth.
This subtraction of a plate eigenvalue from a constant-force paraboloid
model is not a validated crush-foundation solution. Crushed width,
residual depth, peak penetration and face fracture are distinct quantities.

The 015b geometry transfer uses teq=√3(tc+tf), with the inherited nu=.33
for its width scale. Plateau is .964/(1+lambda)^1.23+.036.
Eq.3 inverse is −ln[(gamma−.45)/.51]/3.88 times teq; the Lee
inverse is [.25/(gamma−.068)−.28]teq. Narrow-width extrapolation and
sandwich transfer remain unvalidated. The separate Poisson conventions
are retained for reproduction and explicitly identified.

For a soft contact radius a, spread b=a+tf/2√(sigma_y/crush).
Plastic face work is π sigma_y tf d². Constant-footprint core work is
π crush b²d. Pressure balance gives d=max(0,(q a²−crush b²)/(2 sigma_y tf)).
For a hard hemisphere, contact radius expands as √(2rd−d²), capped at r;
core work is the integral of π crush b(d)² over penetration. This check
uses that integral analytically. Its differences from the filed hard-contact
quadrature are about one part per million. Eighty-percent absorption and
the doubled-depth band are declared assumptions. Core-through cases
do not establish a post-perforation shape or strain.

P3 geometry, coupled lambda-sized CFRP joints, annulus, sag loss, film mass,
six scalar modes and half-wave screen follow 022d METHOD. A new multistart
SLSQP search supplies alternative witnesses. The filed points are separately
forward-scored: their different objective values are search differences,
not automatically arithmetic errors. No global-optimality proof is claimed.
For Perry, e=L/1000 and eta=e ro A/I. If C and E denote the compression
and Euler load factors, the stable quadratic root is
2CE/[C+E(1+eta)+sqrt((C+E(1+eta))²−4CE)].
It matches the direct magnified-stress equation and the pinned 022d table.
The 15.586 MPa hypothetical tensile screen is also checked on every new witness.
At multipliers below one, lambda-sized joints are below operating demand.

The tube contact screen is an infinite isotropic plate on a Winkler foundation:
D=Et³/[12(1−nu²)], k=Et/ro², ell=(D/k)^(1/4), nu=.16, contact radius .012 m.
The centre stress multiplier is 3(1+nu)c²/t² times
integral J1(u)u²/[u⁴+(c/ell)⁴] du. Quadrature agrees with the independent
closed identity −Re[K1(z)/z], z=(c/ell)exp(iπ/4).
It gives 55.549976 Pa stress per Pa contact pressure.
Pf=1−exp[−(sigma/sigma0)^m]. Tube 299/192 MPa values are already
characteristic strengths; the 380 MPa bar mean is divided by Gamma(1+1/10).
No effective-size, dynamic-impact, installed-flaw or prestress qualification
is supplied. Exact repeated-trial counts require an independence assumption.

The beam reconstruction starts with an icosahedron, divides each face into
f² triangles and projects nodes to R=10. Euler–Bernoulli members use the
022d A/I, E=410 GPa, nu=.16 and J=2I. Radial loads with one third of each
*planar* triangle's area reproduce the owner. Spherical-area, equal-area
and face-normal alternatives are preserved as sensitivity calculations,
not errors in the selected model. Six free rigid-body modes are removed by
orthogonal Lagrange constraints. Every geometric edge class is removed:
six for f4 and nine for f5. Reported cases are paired by removed-force
class only after all independent classes have been solved. Meshes are pinned.
Truss compatibility rank confirms one additional mechanism after a member
is removed. A floating-point condition number near 1e17 is not a unique
physical property and cannot be reproduced without the exact constraint/scaling.

Atmosphere is T=288.15−.0065z, p=101325(T/288.15)^[g/(Rgas×.0065)],
Rgas=287.05287, g=9.80665. The baseline non-air mass is rho(500)V.
Mass flow uses the ideal-gas choked expression with gamma=1.4 and Cd=.6,
then the isentropic subsonic expression above pressure ratio .528281788.
Inside temperature follows outside temperature instantly. The sphere equation is
(M+m+.5rho V) zdotdot=(rho V−M−m)g−.5rho Cd_drag πR² zdot|zdot|.
The filed model omits incoming-air momentum; a separate sensitivity adds −mdot zdot.
The P2 pressure diagnostic uses 4π(R−tf−tc)³/3, although reference buoyancy
and descent use the full sphere. The tabular gas budget is rounded to 48.894 kg.
Those conventions are explicit reconstruction inputs.

DOP853 roots ground and m=.5 kg events. Main comparisons allow 0.1% plus
2e−5 in trajectory fields because very slow descent retains small oscillations.
Hole-diameter roots allow .02%. Stationary algebra normally uses relative
2e−7, hard-contact quadrature 5e−6, beam cases 3e−5 and new-search comparisons
2e−5. Every row records its own tolerance. Search differences and primary-input
corrections are separately classified. No tolerance turns a failed design into SF1.

The headline trajectory reproduces the owner's centre-height-zero convention.
GROUND-CONTACT-SENSITIVITY instead stops at z=R over level terrain. Incoming
gas is not net heaviness: the latter subtracts the local displaced mass.
The valve table follows a fixed-pressure hydrostatic gradient; a neutral
ISA descent uses the smaller density gradient, also tabulated.
Actual inventory, sagged volume, thermal fill, control and terrain need a
separate specified operating model.

All 388 library rows have source URLs and QUESTIONABLE tags; all 87 selected
value mappings match their underlying records. Primary documents were
retrieved independently. Five HTTP access pages are explicitly quarantined.
2025 annual CFR PDFs verify the cited historical clauses; failed current
retrievals do not establish current regulatory approval. EVIDENCE.json
records scope and corrections. Sixteen inherited NFIs and fifteen new
nonblocking rows remain open.
"""
(ROOT/"METHOD.md").write_text(method)

card=f"""# CHECK-045 — independent damage-tolerance audit

**Complete with corrections.** The main conditional danger screens reproduce.
Neither P2 nor P3 has demonstrated installed damage tolerance. The owner's
categorical statements about every puncture or member loss are stronger than
the unvalidated models support. All results remain QUESTIONABLE; transferred
properties and operating scenarios are PROJECTION. No installed allowable,
safe operating procedure, procurement or contact with another seat is claimed.

Order: `ord-admiral-rr2-check045-codex-d1c0-1020`.
Owner report: `rpt-ref-57c98dcce7960aca042a`.
Nine owner/predecessor programs remained unread and unexecuted.
The frozen report and its non-code inputs are under [inputs](inputs/).

The check contains {counts['total']} comparisons: {counts['arithmetic']} arithmetic/search,
{counts['trajectory']} trajectory, {counts['selected_frame']} selected frame and
{counts['audit']} independent witness/evidence/invariant checks.
{counts['passed']} pass their declared tolerances; {counts['different']} differ.
These include search improvements and approximation differences, not only errors.
[MISMATCHES.json](MISMATCHES.json) lists every differing field with both values,
then adds six primary-source mass/energy corrections, seven prose/integer
corrections and four condition-number fields whose matrix constraints were not
stated in the permitted non-code inputs. Those diagnostics are explicitly
distinguished from arithmetic errors.
The owner's priced geometry witnesses forward-score successfully; the 96
audit/invariant checks and all 56 selected frame comparisons pass.

![Independent critical checks](check45.png)

## P2: the important numbers reproduce

| Quantity | Independent value | Interpretation |
| --- | ---: | --- |
| Membrane force per face | 238.652095 kN/m | pR/4 |
| Face bending rigidity | 12.194523 N·m | nu=.0752 |
| Typical core crush used | 0.241 MPa | rounded; not an installed minimum |
| Clamped / simply supported patch cutoff | 54.779991 / 27.127598 mm | proposed growth model |
| 80 mm patch growth depth | 0.609913 / 0.366023 mm | clamped / simply supported |
| 50.8 mm hail crushed diameter | 80.865106 mm | **width, not depth** |
| Fluid / Shi / all-energy dent | 0.390712 / 1.675384 / 5.430417 mm | three conditional impact readings |
| Design-hail growth threshold | 0.611682 / 0.372950 mm | clamped / simply supported |
| Pressure fraction eliminating modeled growth | 0.458903732 | clamped, same fixed footprint |
| Air admitted at 500 m convention | 2645.660029 kg | full-volume, isothermal reference |
| Time through 200 mm stationary valve | 614.067073 s | includes short subsonic end interval |
| Available mass to usage=1 | 14.580616 kg | 11.602885 g/m² |

Thus the design hail exceeds the clamped threshold on the Shi and all-energy
readings; it exceeds the simply supported threshold on all three. The 0.914 m/s,
0.5 m contact expends more than the core-crush capacity. The analogous
lambda-1/Lee-depth contact speed is 0.494866 m/s.

The global-map threshold lambda=0.630970, widths and 16.057336/9.318286 mm
depth inversions also reproduce. They remain transferred dimple-map screens,
not a validated result for interacting impact damage in a sandwich.

The mass rejection is robust in the stated model. Bridging the 80.865 mm
patch requires a 1.030199 mm face; **faces alone weigh 4789.970 kg**, versus a
4169.660 kg structural upper bound even before the necessary core. Required
crush 0.577091/1.763546 MPa corresponds to density multipliers 1.688638/3.300820
under the assumed k^(5/3) law. The priced denser cores and shields reproduce.
Their `feasible=true` fields must not imply allowed optimism usage: six such
rows exceed one. [Detailed arithmetic](ARITHMETIC-CHECKS.json).

Corrections: the 55 mm clamped threshold is **19.176311 mm**, inside the
23.237218 mm core, contradicting its table cell. Pach's test-depth field must
be **0.0011 m**, not 1.1 m, and the modeled 1.489–1.541 mm is outside the stated
1.1–1.2 mm residual-test range. The primary thesis supports the measured range,
not the claimed calibration agreement. [Pach thesis](https://espace.rmc.ca/jspui/bitstream/11264/2883/1/AlekPach_Thesis_Submitted.pdf).

IEC's table prints the 35/55/65 mm ball masses: **20.7/80.2/132.0 g**.
Their corresponding energies are **7.657344/46.083321/88.894740 J**, rather
than 7.643405/46.071507/89.128614 J. The primary page was visually checked.
This does not alter the NBS 50.8 mm design case or the resulting growth
classifications. [Table image](sources/iec-table3.png),
[exact corrections](IEC-MASS-CORRECTIONS.json).

## P3: nominal point, contact and lost-member screens

The nominal 022d point reproduces: SF 1.258252477, spacing 3.170758569 m,
OD 275.082856 mm, wall 1.137364845 mm, force 873.771337 kN,
film 214.541558 kg and tubes 4183.590023 kg. Total-gauge film stress
1.382870316 GPa corresponds to **2.765740632 GPa in each directional ply**,
or 47.6852% of the assumed 5.8 GPa fibre strength.

The non-governing Perry value is wrong: **3.454499160**, not 4.095817936.
The direct magnified-bending equation, separate quadratic root and pinned
022d table agree. Correcting it leaves the nominal controlling factor unchanged.

The tube-contact transfer reproduces 55.549976 MPa per MPa pressure and
the design-hail conditional tube-hit probabilities **0.011321398–0.052772758**.
The 299/192 MPa characteristic strengths and 4.6/5.5 Weibull moduli are
supported; effective size, flaw population, impact dynamics and prestress
transfer are not qualified. [ORNL/INL primary report](https://lwrs.inl.gov/content/uploads/11/2024/03/M3LW-13IN0504053-Silicon_Carbide_Ceramic_Matrix_Composite_Failure_Mode_Analysis.pdf).

For independent repeated trials, exact real-valued 50%-failure counts are
**60.877292/12.784859**, versus the stored rare-event approximations
61.224523/13.134564. Integer ceilings remain 61/13. Identical repeated loading
of one specimen does not by itself justify independent strength redraws.
Neither per-tube-hit probability nor tube coverage supplies a storm frequency.

The four filed rigid-joint removals reproduce: stress ratios
**2.427468–3.270739**, moments up to 129.311660 kN·m and tension up to
947.133864 MPa. The independent model also checks all six f4 and nine f5 edge
classes. Their combined range is **1.959485–3.270739** in stress ratio and
**0–1019.372 MPa** in maximum tension. Consequently the four cases are
examples, not a bound on every lost member. A pin-jointed compatibility
calculation gains one non-rigid mechanism after a member is removed.
The static screen does not prove a dynamic cascade for every case.
[Mesh and all cases](FRAME-RESULTS.json), [condition/rank diagnostics](TRUSS-RANK-CHECKS.json).

The merged-bay geometric factor 1.5 and film SF **0.838834984** reproduce.
So do the projected slit half-lengths 0.006741–1.908531 mm.
These use substitute-polymer toughness and assumed moduli; an installed
PBO laminate's notch tolerance and arrest behavior remain unknown.

The owner's priced witnesses are numerically consistent, but the new search
finds stronger alternatives within the same scalar model:

| Case | Filed SF | New witness SF |
| --- | ---: | ---: |
| 1.0 GPa film allowable | 1.196893 | 1.200403 |
| 1.5 mm minimum tube wall | 0.800189 | 0.805476 |
| 2.0 mm minimum tube wall | 0.469060 | 0.483053 |
| 3.0 mm minimum tube wall | no point reported | 0.223304 |
| 303.532 MPa tear-screen allowable | 0.975205 | 0.975445 |

At the last point film mass is **848.604 kg**, versus 880.534 kg in the
filed local solution. None of the wall/tear fixes reaches SF1; these are
improved witnesses, not a proof of a global optimum or installed strength.
[Forward checks](FILED-WITNESS-CHECKS.json),
[independent mass/section/stress invariants](NEW-WITNESS-INVARIANTS.json).

## Leak and operating-model audit

All headline flow, pressure, touchdown and valve numbers reproduce under
the declared gross-mass, fixed-volume, isothermal assumptions:

| Quantity | Independent value |
| --- | ---: |
| 1 mm hole initial inflow | 0.107710854 g/s |
| Hole for 0.914 m/s touchdown | 63.100934–65.606770 mm |
| Hole for 4.2 m/s touchdown | 130.226408–146.972238 mm |
| 0.3 m hole touchdown speed | 8.551214–11.354483 m/s |
| Torn bay touchdown time | 23.468391–28.766999 s |
| Torn bay touchdown speed | 23.090363–34.587475 m/s |
| Valve for 0.914 / 2 / 7.5 m/s | 69.937748 / 103.455491 / 200.340697 mm |
| 1 Pa / 0.1 Pa one-hour equivalent leak | 0.363443 / 0.114931 mm |

The neutral full-sphere pressure ratio is **1.011407511**; the smaller P2
gas volume gives the approximately 1.0110 pressure result. This is a
temperature/volume convention, not increased differential pressure equal
to the entire outside pressure rise. The valve table uses the hydrostatic
pressure gradient; the neutral ISA density-gradient diameters are
62.933750/93.094819/180.277342 mm. Both require a specified control objective.

Twenty-four `t_first_half_kg_s` fields are late relative to rooted events:
for a 100 mm hole **0.464206 s**, not 0.770164 s; for a torn bay
**0.000837478 s**, not 0.001535376 s. These errors do not drive the published
touchdown values. [Exact event differences](LEAK-DIFFERENCES.json).

The trajectory's initial non-air mass is **4889.444 kg** for both hulls:
it is a full gross neutral reference, not the demonstrated carried inventory
of the built 028b/022d points. It also terminates with the sphere centre at
zero altitude. First contact over level terrain is at **10 m centre height**.
On that correction, the same reference torn bay reaches ground in
23.179081–28.334006 s at **23.099647–34.541863 m/s**.
The admitted 5130–5131 kg of gas is not net heaviness; the latter is about
**4889 kg** after subtracting local displacement. [Ground sensitivity](GROUND-CONTACT-SENSITIVITY.json).

The 46% venting result is a conditional reduction of the modeled load,
not a completed handling plan. At sea-level ISA the same absolute
differential needs **2912.791 kg** air on the full-volume convention.
An airborne neutral hull becomes heavy when vented; support, descent and
landing must be specified. A regulatory test velocity is not a demonstrated
safe speed for this shell. The atmosphere's 500 m reference is not by itself
an AGL operating altitude.

## Evidence and disposition

All 388 source-library rows have source URLs and QUESTIONABLE tags, and all
87 selected value mappings agree with their underlying records. Independent
retrieval yielded 41 substantive files; five eCFR access pages are quarantined.
The named CFR quantities were checked in the official 2025 annual edition;
this is historical source verification, not a claim of a current regulatory
route. [Evidence ledger](EVIDENCE.json).

All 36 frozen inputs remain intact. The final recheck found a later COMMON
amendment about simulation-job retry; 35 of 36 live originals still match.
No scientific input changed. [Recorded amendment](INPUT-DRIFT.json).

The tap-test 41.8/29 mm figures are disbond a90/95 values on aluminium.
The 0.2 mm laser statement is a contour interval and measurement threshold,
not established Be damage-detection performance. [Primary tap study](https://icaf.aero/icaf2023/proceedings/documents/55.pdf).

All **15 new and 16 inherited NFIs remain open and nonblocking**.
The proposed corrections are filed here for downstream adoption; the owner's
artifacts remain unchanged. No installed SF, damage-tolerance qualification
or universally safe puncture/dent limit is established.
[Method](METHOD.md), [full findings](MISMATCHES.json),
[NFI register](NFI.json), [machine results](RESULTS.json).

The brief names no successor. Stop and file; return to SLEEPING.
"""
(ROOT/"CARD.md").write_text(card)
print(json.dumps(dict(check_counts=counts,new_nfi=len(nfis),inherited_nfi=len(inherited),
                      card_words=len(card.split()),method_words=len(method.split())),indent=2))
