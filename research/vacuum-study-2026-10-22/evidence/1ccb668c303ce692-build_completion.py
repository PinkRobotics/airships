"""Render the completed 051 card without changing any earlier report artifact."""
from pathlib import Path
from datetime import datetime,timezone
import csv
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
OLD=ROOT.with_name("vacuum-mainline051-p3-frame-targets-1020")
TAG="QUESTIONABLE / PROJECTION"
def read(name):return json.loads((ROOT/name).read_text())
def dump(name,x):(ROOT/name).write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")
def fmt(x,n=3):return "unknown" if x is None else f"{x:,.{n}f}"
def gap(mat,reserve="5",policy="same_tube_mass",load="operating"):
    return next(x for x in GAPS if x["material"]==mat and x["reserve"]==reserve and x["section_policy"]==policy and x["load_case"]==load)
def target(g,m=10,pf=.001):
    return next((x for x in g["targets"] if x["m"]==m and x["Pf"]==pf),{})
def hail(mat,reserve="5",policy="same_tube_mass"):
    return next(x for x in HAIL["rows"] if x["material"]==mat and x["reserve"]==reserve and x["section_policy"]==policy and x["diameter_m"]==.0508)
def fenum(x):return "unknown" if x is None else f"{x:.5g}"

# Preserve imported inputs before writing derived evidence/catalog prose.
inputs=read("INPUTS.json")
for pin in inputs:
    local=Path(pin["local"])
    if local.name in ["MATERIAL-EVIDENCE.json","MATERIAL-EVIDENCE.csv","SOURCES.md"] or (
            local.exists() and hashlib.sha256(local.read_bytes()).hexdigest()!=pin["sha256"]):
        origin=Path(pin["path"])
        raw=origin.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==pin["sha256"]
        dst=ROOT/"intake/partial/imported"/local.name
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
        pin["local"]=str(dst);pin["role"]="unchanged imported source; modified root file is a derived artifact"
dump("INPUTS.json",inputs)

TARGETS=read("TARGETS.json")
GAPS=read("GAPS.json")["rows"]
HAIL=read("HAIL.json")
DAMAGE=read("DAMAGE.json")["rows"]
FE=read("FE-ALL.json")["rows"]
CHECKS=read("FE-CHECKS.json")
WIT=read("WITNESSES.json")["rows"]
MATS=read("MATERIAL-MODELS.json")
ids=[x["id"] for x in MATS]
parts=[]
def add(x):parts.append(x.strip()+"\n")
add("**MAINLINE-051 COMPLETE — P3 tube targets, candidate constructions, and damage**\n\n"+TAG)
add("""The requested calculations are complete. No candidate is established by the retrieved evidence to meet a measured whole-frame Pf of 1e-3. The obstacle is a missing complete-member compression distribution, in addition to unqualified structural and damage models. The conditional calculations below identify useful numerical targets without converting fibre tension, coupon averages, or flexural statistics into tube compression allowables.

At the 5% reserve, the same-mass Hexoloy-SA model comes closest among candidates with a sourced compression number: it already meets the **operating** q=1 target under the invented whole-member scale 3.9 GPa/m=10. At 041's higher original screened loads, that hypothesis needs roughly 10% more scale or 7% more m. These are different load cases. The high-modulus K13D2U wrapped laminate also passes the mechanical screen as a **ceiling**, but its compression strength and distribution are unknown. Neither is a qualified winner.""")
hex5=gap("Hexoloy-SA");hex19=gap("Hexoloy-SA","019")
k5=gap("K13D2U-50-20-20-10");k19=gap("K13D2U-50-20-20-10","019")
add(f"""For Hexoloy-SA, fresh same-mass mechanical SFs are **{hex5['conditional_mechanical_SF_or_ceiling']:.6f}/{hex19['conditional_mechanical_SF_or_ceiling']:.6f}** (5%/019 reserve). The required whole-member m10 scales at q=1 are **{target(hex5)['whole_member_scale_needed_Pa']/1e9:.6f}/{target(hex19)['whole_member_scale_needed_Pa']/1e9:.6f} GPa**. Its hypothetical m10 Pf is {hex5['hypothetical_Pf_m10_if_typical_is_member_scale']:.7g}/{hex19['hypothetical_Pf_m10_if_typical_is_member_scale']:.7g}. At 5%, the combined mechanical/reliability load multiplier is {hex5['joint_mechanical_and_hypothetical_reliability_q']:.6f}. At 019 reserve, the local wall screen is {100*(1/hex19['conditional_mechanical_SF_or_ceiling']-1):.3f}% short in load factor; raising compression strength alone cannot repair that buckling shortfall.

For K13D2U 50/20/20/10, the same-mass ceilings are **{k5['conditional_mechanical_SF_or_ceiling']:.6f}/{k19['conditional_mechanical_SF_or_ceiling']:.6f}**. Demonstrating whole-member compression scales of **{target(k5)['whole_member_scale_needed_Pa']/1e9:.6f}/{target(k19)['whole_member_scale_needed_Pa']/1e9:.6f} GPa at m10** would close the modeled reliability gap. There is no sourced compression denominator from which to claim an improvement multiplier. This is a test target, not evidence that a current K13D2U tube achieves it.""")
add("""**Target surface.** There are 750 members, with actual arc lengths 1.984730–2.623498 m (mean 2.399569 m, total 1799.676624 m). A “3 m member” is a reference size for strength transfer; the calculation does not lengthen the existing frame. 019 is the named fixed reserve case, not a 19% reserve.

For independent Weibull compression events, H=Σ wᵢ(σᵢ/σ₀)^m and Pf=1−exp(−H). Thus σ₀,required=[Σwᵢσᵢ^m/(−ln(1−Pf))]^(1/m). Every member is assigned its own beam peak, including L/1000 bow and Euler amplification. Equal complete-member fits use w=1; a common 3 m fit uses w=L/3; a 1 cm³ volume fit uses w=AL/10⁻⁶. These are alternative size conventions, not interchangeable strength data.

The table gives equal complete-member scales at the **original 041 own-screen loads**, in GPa. All integer m=5–40, both probability targets, both reserve cases, operating/own-screen loads, and all size conventions are in TARGET-SURFACE.csv.""")
lines=["| m | Pf 1e-3, 5% | Pf 1e-3, 019 | Pf 1e-6, 5% | Pf 1e-6, 019 |",
       "|---:|---:|---:|---:|---:|"]
for m in [5,8,10,15,20,30,40]:
    vals=[next(x["equal_complete_member_scale_GPa"] for x in TARGETS["rows"] if x["m"]==m and x["reserve"]==r and x["load"]=="own_screen" and x["frame_Pf_target"]==p) for p,r in [(.001,"5"),(.001,"019"),(1e-6,"5"),(1e-6,"019")]]
    lines.append("| "+str(m)+" | "+" | ".join(f"{v:.6f}" for v in vals)+" |")
add("\n".join(lines))
add("""At m10 the original own-screen target requires 4.278678/4.209090 GPa for Pf 1e-3: **1.09710×/1.07925×** the hypothetical whole-member 3.9 GPa scale. Alternatively m must rise from 10 to **10.74315/10.60365** (1.07432×/1.06037×), holding that scale fixed. Pf 1e-6 instead needs 8.537512/8.398658 GPa (2.18911×/2.15350×), or m=16.30240/16.08945.

At 5% reserve, a complete 3 m reference member has 2292.464 cm³ of material. Under the volume-flaw model, coupon-to-member retention is 0.21278, 0.46128, 0.67918 and 0.82412 at m=5,10,20,40. At m10 and the original screened loads, the required **1 cm³ coupon** scales are 9.088382/8.907641 GPa for Pf 1e-3, and 18.134612/17.773969 GPa for Pf 1e-6. Treating 3.9 GPa as that coupon scale gives Pf=0.99113/0.97905. At operating q=1, the original 041 whole-member hypothesis instead gives Pf=0.0006439/0.0009473; its coupon interpretation gives 0.7000/0.8187. The brief's near-unity coupon result is therefore a higher-load result, not a universal P3 probability.""")
add("""**Candidate masses and SFs.** The fixed envelope retains 041's f5 geometry, outside diameters, film, nodes, systems, reserves and joints. At the common tube-mass budgets (4263.218/4108.765 kg), the lift-budget total is 4889.442 kg in both reserve cases. This total includes reserve and the sag lift debit; it is not simply vehicle dry mass.

The table's first two columns give the **5% reserve fresh-FE q≥1 witness**, with unchanged OD and increased wall where necessary. “Frame” includes tubes, joints and nodes. The total also charges film, systems, reserve and sag. These are explicit witness sections, not minimum-mass designs. The last pair are SFs/ceilings at the **original tube-mass budgets**, not the heavier witness. A ceiling means compression or other failure modes remain unmeasured. Full sections, mode values, same-section alternatives and both reserve witnesses are in FRAME-COMPARE.json, WITNESSES.json and GAPS.csv.""")
lines=["| Tube construction | q≥1 witness frame kg, 5% | Witness lift-budget kg | Witness SF/ceiling | Same-budget SF/ceiling 5% / 019 |",
       "|---|---:|---:|---:|---:|"]
for mat in ids:
    w=next(x for x in WIT if x["material"]==mat and x["reserve"]=="5")
    a=gap(mat);b=gap(mat,"019")
    lines.append(f"| {mat} | {w['comparison_geometry']['frame_plus_joints_nodes_kg']:.1f} | {w['FE']['total_mass_including_reserve_sag_kg']:.1f} | {w['FE']['conditional_SF_or_ceiling']:.4f} | {a['conditional_mechanical_SF_or_ceiling']:.4f} / {b['conditional_mechanical_SF_or_ceiling']:.4f} |")
add("\n".join(lines))
add("""The reference row uses 041's E=410 GPa/rho=3100/nu=.14 assumptions. The Hexoloy sheet instead reports E=430 GPa; the CVD and UltraSiC rows use their separate manufacturer property sets. The updated local wall screen uses the orthotropic Donnell coefficient and peak axial-plus-bending demand. In the isotropic limit its classical coefficient is E/√[3(1−nu²)], rather than 041's rounded 0.6E, and it retains the same unvalidated knockdown γ. This explains why the reference's revised SF is lower than 041's 1.143/1.083. The old .6E/axial-demand values remain reproduced as regression checks; this is a sensitivity, not a validated replacement safety factor.

For composites, “UD” is axial fibre. 70/10/10/10 and 50/20/20/10 are 0/+45/−45/90 degree fractions in an ideal, finely interleaved, symmetric balanced wall. These wrapped virtual tubes are not measured pultruded products. Transverse/shear constants and densities use stated assumptions; D=Q̄t³/12, B=0. Fibre tensile strength is never used as compressive strength. All composite SFs omit at least transverse compression/interlaminar failure, even when a longitudinal compression screen exists.""")
add("""**Compression gaps at operating q=1, same tube-mass budget.** Whole-member m10 targets and ratios below use the fresh FE stress fields. A ratio below one means the assumed scale is sufficient for this model. A quoted average used as a whole-member Weibull scale is an explicit hypothetical assumption. “Unknown” supplies no empirical strength multiplier; the absolute target remains useful. No finite m can repair a proposed scale below a member's peak stress.""")
lines=["| Construction | Required whole scale GPa, 5% / 019 | × assumed compression scale, 5% | Required m, 5% |",
       "|---|---:|---:|---:|"]
for mat in ids:
    a=gap(mat);b=gap(mat,"019");ta=target(a);tb=target(b)
    scalea=ta.get("whole_member_scale_needed_Pa");scaleb=tb.get("whole_member_scale_needed_Pa")
    ratio=ta.get("whole_member_strength_factor_over_typical")
    if mat=="Al6061T6":ratio=None
    m=a.get("hypothetical_m_needed_for_Pf1e3")
    label="no finite m" if a.get("no_finite_m_at_assumed_scale") else fenum(m)
    lines.append(f"| {mat} | {fmt(None if scalea is None else scalea/1e9)} / {fmt(None if scaleb is None else scaleb/1e9)} | {fenum(ratio)} | {label} |")
add("\n".join(lines))
add("""The same calculation at each candidate's screened load and at its q≥1 witness is in GAPS.json, including m=5,8,10,11,15,20,30,40, Pf 1e-3/1e-6, coupon and 3 m references. Dividing a listed required m by the assumed 10 gives the m multiplier. This mathematical shape parameter improvement is not a measured processing trend.

For a monolithic 5% frame, the single missing reliability result is a complete-tube compression population meeting the target: at operating pressure the assumed Hexoloy scale already suffices, while preserving the original higher screen requires the roughly 10% scale improvement above. No one strength improvement closes all structural, reliability and hail gaps. For the fibre constructions, load sharing and matrix/interface failure prevent inference of a tube distribution from a filament or tow distribution.

The public M55J and T700S composite compression numbers are 890 and 1450 MPa, respectively, not tube allowables. M55J's current composite modulus is 338 GPa, not its fibre modulus 540 GPa. K13D2U's 935 GPa and 3.7 GPa are fibre modulus and tensile strength; no tube compression denominator was retrieved. [Toray M55J](https://www.toraycma.com/wp-content/uploads/M55J-Data-Sheet.pdf), [Toray T700S](https://www.toraycma.com/wp-content/uploads/T700S-Data-Sheet.pdf), [Mitsubishi DIALEAD](https://www.m-chemical.co.jp/carbon-fiber/pdf/dialead/composites.pdf).

The HNS research population illustrates the statistical distinction: filament m=8.42 and scale 3062 MPa versus 25 mm bundle m=9 and scale 1730 MPa; neither measures tube compression. Tyranno-SA/CVI m=10.2 describes flexure of 25×4×2 mm bars, not 3 m axial crushing. [HNS primary data](https://pmc.ncbi.nlm.nih.gov/articles/PMC7452681/), [Tyranno primary experiment](https://www.jstage.jst.go.jp/article/matertrans/44/9/44_9_1797/_pdf). SOURCES.md retains the source, test mode, size and missing properties for every construction.""")
add("""**Hail, conditional on a direct tube strike.** Use 50.8 mm ice at 32.004 m/s, a 12 mm contact radius, the inherited flow contact pressure 0.942725 MPa and the inherited Shi multiplier. 045's plate-on-membrane-foundation method is reproduced; an orthotropic plate with foundation k=Ehoop t/r² extends it to the virtual laminates. This approximation omits dynamic contact, axial preload, interface damage and residual strength.

The two probability columns below deliberately impose the **same hypothetical matching-contact distributions on every construction**: (scale=299 MPa,m=4.6) and (scale=192 MPa,m=5.5). They answer what 045's formula returns under those assumptions. They are **not measured break probabilities**, and are not a basis for ranking unlike materials. For the ceramic rows they are still uncalibrated transfers of C-ring/sectored flexural tests. For composites and ductile aluminium there is no basis to equate these events with member severance. Actual identified break-probability bounds remain [0,1].

The table uses the same-budget 5% sections; both reserves, all witness sections, seven hail sizes and pressure models are in HAIL.json. HAIL-DESIGN.csv is the compact design-strike table.""")
lines=["| Construction | Shi surface demand MPa | Hypothetical P, 299/m4.6 | Hypothetical P, 192/m5.5 |",
       "|---|---:|---:|---:|"]
for mat in ids:
    h=hail(mat)
    scenarios=[x for x in h["explicit_common_fit_scenarios"] if x["pressure_model"]=="Shi"]
    lines.append(f"| {mat} | {h['stress_Shi_Pa']/1e6:.2f} | {scenarios[1]['conditional_probability_if_contact_fit_applies']:.6g} | {scenarios[0]['conditional_probability_if_contact_fit_applies']:.6g} |")
add("\n".join(lines))
h5=hail("Hexoloy-SA");h19=hail("Hexoloy-SA","019")
add(f"""For the resized sintered-SiC frame, the two transferred Shi probabilities are {100*h5['explicit_common_fit_scenarios'][-1]['conditional_probability_if_contact_fit_applies']:.3f}–{100*h5['explicit_common_fit_scenarios'][-2]['conditional_probability_if_contact_fit_applies']:.3f}% (5%) and {100*h19['explicit_common_fit_scenarios'][-1]['conditional_probability_if_contact_fit_applies']:.3f}–{100*h19['explicit_common_fit_scenarios'][-2]['conditional_probability_if_contact_fit_applies']:.3f}% (019). Flow-pressure values are separately reported, not used as the ends of that interval. The source's old 55.549976 MPa/MPa coefficient is reproduced with its assumed nu=.16; the new 041 reference uses nu=.14.

A different, still uncalibrated choice—PremaTech's CVD flexure scale424 MPa/m11—gives {hail('CVD-PureSiC-HR')['sourced_population_surrogates'][-1]['uncalibrated_045_Pbreak_surrogate']:.6g} at the CVD same-budget section. The Tyranno flexural fit gives {hail('Tyranno-SA-CVI-scenario')['sourced_population_surrogates'][-1]['uncalibrated_045_Pbreak_surrogate']:.6g}. Those small numbers do not demonstrate superior tube survival: effective size, stress mode, grade, rate and failure event differ. Matching-contact targets are provided for m5/10/20/40 and conditional strike probabilities 1e-3/1e-6, so missing probability evidence becomes a numerical test target. CFRP first-ply stress screens and aluminium's hail-only yield margin are also reported separately from severance.""")
add("""**One member lost.** Each material/reserve pair was solved intact and with two independently selected member removals (median and maximum original compression). All beam pieces of the member and their unused internal nodes are removed; the adjacent triangular pressure bays become a quadrilateral. Pressure remains a balanced derivative of the closed fan volume, rather than loading unsupported deleted nodes. Joints retain their original, individually sized sleeves and bond overlaps.

Every one of the 72 same-budget deletion cases has a modeled secondary-failure trigger. The table reports the worst post-loss SF/ceiling and largest compression amplification among the two samples, at operating pressure. It is a static/tangent warning, not a computed dynamic cascade history. No statement that every possible lost edge produces the identical sequence is implied.""")
lines=["| Construction | Post-loss SF/ceiling, 5% / 019 | Max compression ratio, 5% / 019 |",
       "|---|---:|---:|"]
for mat in ids:
    val=[]
    for reserve in ["5","019"]:
        rows=[x for x in DAMAGE if x["material"]==mat and x["reserve"]==reserve]
        val.append((min(x["conditional_SF_or_ceiling"] for x in rows),
                    max((x["compression_amplification"] for x in rows if x["compression_amplification"] is not None),default=None)))
    lines.append(f"| {mat} | {val[0][0]:.4f} / {val[1][0]:.4f} | {fmt(val[0][1])} / {fmt(val[1][1])} |")
add("\n".join(lines))
reference=[x for x in DAMAGE if x["material"]=="041-reference" and x["reserve"]=="5"]
add(f"""In the 5% reference, peak compression rises to {min(x['q1_peak_compression_Pa'] for x in reference)/1e9:.3f}–{max(x['q1_peak_compression_Pa'] for x in reference)/1e9:.3f} GPa, about {min(x['compression_amplification'] for x in reference):.3f}–{max(x['compression_amplification'] for x in reference):.3f}× intact. This is not just axial force multiplication: bending and beam-column amplification dominate. The local wall screen falls below 0.45; the retained joint screen falls to about 0.49–0.51, and the merged-bay film screen to about 0.773. At 019 reserve the analogous film screen is about 0.733. The actual geometry gives a tension multiplier near 1.478, close to but distinct from 045's equilateral 1.5 assumption.

A better compression material alone does not resolve these joint and film failures. A damage-tolerant proposal needs a changed load path, joints and film-bay support with their masses charged. Existing perfect-joint/global-knockdown assumptions remain unvalidated; two static removals cannot identify a lifetime loss rate or a dynamic cascade probability.""")
add("""**Is a non-brittle tube better?** CFRP is not generally ductile; delamination, matrix cracking, microbuckling and compression-after-impact can govern. The present M55J and T700S reference constructions need higher mass than the buoyancy budget to reach the mechanical screen, and still lack member statistics. Ductile 6061-T6 needs much greater mass at this fixed OD and geometry. K13D2U with hoop and ±45 reinforcement is the promising conditional stiffness/mass construction, but no sourced compression population or impact-survival evidence supports calling it the better frame today. These comparisons are confined to the stated geometry and constitutive assumptions; they are not a global optimum or a proof that all composite designs fail. [NASA compression-after-impact research](https://ntrs.nasa.gov/api/citations/20160010546/downloads/20160010546.pdf).

017b's flat SiC trend concerns the cited stiffness/density history. It does not establish that strength scatter, processing defects, interfaces, proof testing or damage tolerance are frozen. Those are the relevant directions exposed here, alongside a load path that survives a missing member.""")
add(f"""**Evidence and completion.** {len(TARGETS['checks'])} target checks, six original scalar regressions, {len(HAIL['checks'])} hail/integral/angular checks and {len(CHECKS['checks'])} FE/mesh checks pass. The independent m6 calculation is checked against the prior m24 reference and against focused m12 intact/deleted-member cases. Every admitted job recorded its release; all runs retained one core and 1 GiB. Exit-75 refusals were retried under the resume order. One manual retry was inadvertently 29 seconds after the preceding refusal; the subsequent retry wrapper enforced at least 60 seconds. The initial comparison's fixed m=5000 root bracket was corrected to an analytic bracket. The hail anchor's nu mismatch was traced to the pinned source, not hidden by loosening its tolerance.

The earlier partial report and all its pinned files are preserved. Its unfinished computations are resolved by this package; physical qualification issues remain in NFI.json. INPUTS.json pins source copies; per-attempt START/END records pin executed code; CODE.tar.gz and MANIFEST-051-COMPLETE.json capture the completed package. Start/end times are measurements, with no task or phase cap. Stop and file; robotics owns any next job.""")
(ROOT/"CARD.md").write_text("\n".join(parts))

method=r"""**MAINLINE-051 calculation method — QUESTIONABLE / PROJECTION**

All pressures multiply p=95460.8379139 Pa. Sphere radius is 10 m; lift budget 4889.44215019 kg. Geometry is the exact f5 mesh (252 primary nodes, 750 curved members, 500 initial film faces) from the previously independent CHECK-041 implementation. References and source pins are in INPUTS.json. Every numerical program runs via tools/simjob.py with one CPU, 1 GiB, BLAS/OpenMP threads=1, no GPU and TMPDIR=unpublished-local-ref:1ffe4110219d37c0.

Reliability uses H=Σw(σ/σ0)^m and stable log-sum-exp. Target inversion and coupon/3 m weights are stated in CARD.md. Root finding for required m has analytic bracket m_hi=1.01[ln(n)−ln(Htarget)]/[−max ln(σ/σ0)]. When any σ≥σ0, no finite m can meet Pf=1e-3. Values are whole-member peak-stress surrogates; neither weakest-link independence nor volume scaling is established for compression or fibre composites. Full-member failure statistics may still be measured empirically for a composite, but cannot be deduced from its filament tensile m.

Material definitions are executable in material_models.py. Isotropic candidates use their separately cited E/rho/nu. Virtual laminate reduced stiffness is Q11=E1/(1−nu12²E2/E1), Q22=E2/(1−nu12²E2/E1), Q12=nu12E2/(1−nu12²E2/E1), Q66=G12. Engineering-strain transforms give Qbar=Σf TᵀQT. Axial modulus is 1/a11, hoop modulus 1/a22, a=Qbar⁻¹. B=0 and D=Qbar t³/12 are projections for a symmetric finely interleaved wall. Longitudinal compression, available transverse tensile stress and in-plane shear impose partial maximum-stress ply limits; transverse compression, interlaminar and processing failures remain omitted. Densities use declared fibre/matrix volume mixtures where no tube value exists.

For cylindrical local axial buckling, Klocal=min over z≥0 of sqrt[(Q11+2(Q12+2Q66)z²+Q22z⁴)/(a22+(2a12+a66)z²+a11z⁴)]/sqrt(3). The local stress limit is γ Klocal t/r, γ=.099+.901 exp[−sqrt(r/t)/16]. This continuum Donnell minimum ignores finite-wavelength discreteness and laminate manufacturing; the legacy isotropic knockdown is unvalidated here. Isotropic reduction is E/sqrt[3(1−nu²)]. The source formulation is [Nemeth and Mikulas, NASA/TP-2009-215778](https://ntrs.nasa.gov/citations/20090029956). Peak combined demand, rather than pure axial stress, is the chosen sensitivity screen.

For a circular tube A=π(ro²−ri²), I=π(ro⁴−ri⁴)/4. Euler e=π²Ex I/(L²N). At pressure multiplier q, compression demand is qa+qb/(1−q/e), a=N/A, b=(M+NL/1000)ro/I. The root against stress S is 2S/[d+sqrt(d²−4aS/e)], d=a+b+S/e. This combines linear FE moment with an assumed bow; it is not a nonlinear imperfection analysis. No finite q=1 stress is reported if a member Euler factor is ≤1. General deleted-member evaluation allows tension and uses absolute N for bow, with no destabilizing Euler term in a tension segment.

The original comparison uses fixed 041 N/M and EI-scaled global eigenvalues for three section policies: original section; equal tube mass; minimum wall meeting that limited deterministic screen at fixed OD. Its six scalar checks reproduce both reserves' mass, legacy local screen and original operating peak stress. EI scaling is explicitly approximate when GJ or EA/EI ratios change. The fresh FE calculations supersede that approximation for same-mass designs and for all q≥1 witnesses.

The beam solver independently assembles 3D Euler-Bernoulli axial, bending and torsional stiffness along subdivided great-circle arcs. For orthotropy, the old core's torsion-only algebraic parameter NU=Ex/(2Gxy)−1 makes GJ=2Gxy I; it is not a claimed isotropic Poisson ratio. Six rigid motions are projected without introducing a physical support. Pressure is −p∂V/∂u for a closed polygon-fan volume. The destabilizing operator is D=G_N−p∂²V/∂u². ARPACK solves Kφ=λDφ; the global screen is 0.2λ. Every solve records equilibrium, rigid-load-balance and eigen residuals. Fresh calculations use 6 pieces/member; focused 12-piece cases and the existing 24-piece reference assess discretization. Material nonlinearities, true geometric postbuckling and film tangent stiffness are not added.

Joints retain the original individual areas and overlaps, reconstructed from the pinned 041 forces and target. Sleeve capacity uses 1470 MPa with N/Aj+M ro,j/Ij. Bond capacity uses 28.9 MPa and sqrt[(N+2M/ro)²+(T/ro)²]/(2πro overlap). Material/environment appropriateness and joint stiffness remain assumptions. For mass, add rho A ΣL + original joint/film/node/system masses + fixed reserve and sag debit. The fresh q≥1 witnesses increase wall from the fixed-demand minimum using the observed shortfall, and stop at a passing projected screen; this is not an optimization. Every dimension and final SF is stored.

For damage, remove all subelements of either the original median- or maximum-compression member. Merge its two adjacent oriented triangular boundaries by canceling their common halfedges; remap surviving nodes. Grouping faces by boundary length preserves the same exact cubic volume differentiation. Static and tangent solves are repeated. Original sleeve and bond sizes remain. Film demand is multiplied by r_eff,quad/max(r_eff,triangle), where r_eff=2A/perimeter, following 045's equal rise/span assumption. This is a geometry sensitivity, not a solved membrane shape or tear analysis. Failed local-shell/compression member IDs are retained. Subsequent time integration, successive rupture and pressure loss are not simulated, so dynamic cascade probability remains null.

045's hail model is a uniform circular load on an infinite plate on a spring foundation k=Et/r², with D=Et³/[12(1−nu²)]. Set ell=(D/k)^1/4 and a=c/ell. At the patch centre M=(1+nu)p_contact c ell I(a)/2, I(a)=∫0∞ J1(au)u²/(u⁴+1)du. The independent closed form I(a)=−Im[e^(iπ/4) K1(ae^(iπ/4))] follows by differentiating the K0 transform and is checked against two-interval numerical integration. Surface stress=6M/t². Pinned run45.py uses nu=.16 (an unsourced assumption), whereas 041 uses .14. The source coefficient is reproduced with its own input; new rows use their declared inputs.

For a balanced orthotropic plate, retain the projected foundation k=Ehoop t/r². Dθ=D11 cos⁴θ+2(D12+2D66)cos²θ sin²θ+D22 sin⁴θ; ellθ=(Dθ/k)^1/4. Mx/p is the angular mean of c ellθ I(c/ellθ)(D11 cos²θ+D12 sin²θ)/Dθ; My follows by exchanging directional terms. Angular convergence uses 512/1024 points. Surface ply strains come from (t/2)D⁻¹M and lamina transforms. This is a declared extension of the approximate foundation model, not a validated shell impact model. Contact is unpreloaded, static and spatially averaged. A composite's first-ply stress screen is not complete-tube severance; aluminium uses a separate hail-only von Mises/yield margin.

Hail probabilities apply 1−exp[−(σ/scale)^m] only under explicit selected or hypothetical matching-contact distributions. C-ring, sectored flexure, CVD flexure and Tyranno bar populations differ in grade, mode and effective size; all transfers are marked uncalibrated. HNS tow and carbon/SiC fibre tensile strengths are not silently substituted for impact tube strength. Where a matching fit is absent, actual probability is null with identification bounds [0,1], while the same hypothetical contact-fit grid and required contact strength targets provide numerical sensitivity. No impact flux, lifetime accumulation or independence of successive strikes is assumed.
"""
(ROOT/"METHOD.md").write_text(method.strip()+"\n")

nfi_text=[
("complete-member-compression","Open physical qualification","No candidate has a retrieved 2–3 m complete-tube compression scale, m and effective size. Measure a relevant population, including joints/process/environment; do not substitute tensile or flexural fits."),
("strength-basis","Open physical qualification","Manufacturer typical compression averages are not Weibull scales, design allowables or specimen-size fits. All multipliers against them are explicitly hypothetical."),
("composite-constitutive","Open physical qualification","Virtual matrix/transverse/shear constants, density mixtures and homogenized B=0/D=Qbar t³/12 need construction-specific evidence; actual pultruded/wrapped geometry and fibre fractions may differ."),
("composite-failure","Open physical qualification","Transverse compression, interlaminar damage, microbuckling, defects, matrix shear and compression-after-impact remain incomplete. No CFRP tube is established to be non-brittle."),
("local-shell-screen","Open physical qualification","Peak-stress orthotropic Donnell screen with inherited gamma is unvalidated. The change from .6E axial demand materially reduces the baseline 019 margin."),
("global-and-joints","Open physical qualification","Rigid joints, global factor0.2, follower-pressure fan and lack of film tangent stiffness are projections; proof by nonlinear imperfection-sensitive structure tests/analysis is absent."),
("joint-and-film-loss","Open physical qualification","Every sampled loss triggers a second overload in the retained design. A changed load path, stronger joints and supported film bay must be designed with its mass charged."),
("dynamic-cascade","Open physical qualification","Two static edge removals per construction/reserve are not an exhaustive edge search, transient rupture chain or lifetime cascade probability."),
("hail-calibration","Open physical qualification","Pressure history/contact patch, preload, dynamic plate/shell response, effective flaw area and matching member-break fit are missing. Uncalibrated probabilities are not measured risks."),
("hail-composites","Open physical qualification","First-ply stress, leakage and complete-member severance are distinct events; tow load sharing cannot supply an impact Weibull population."),
("size-scaling","Open physical qualification","750 equal whole-member populations, 3 m reference weights and 1 cm³ volume weights are alternative hypotheses. Real compressive failure or composite load sharing may not follow weakest-link volume scaling."),
("source-conflicts","Open source qualification","Saint-Gobain sheet/web m/E/rho entries differ; Specialty Materials metric and imperial entries conflict; reported PremaTech flexural mean/scale are not internally exact. Preserve source populations instead of silently combining them."),
("CMC-temperature","Open physical qualification","GE's >1 GPa CMC compression concerns hot component averages; projected RT tube use and assumed E/G/rho are not justified by those data."),
("optimization-scope","Open design scope","Fixed OD, actual f5 member lengths, retained film/joints and declared layups bound this study. Passing witnesses are not global minima or commercially demonstrated tubes."),
("life-exposure","Open physical qualification","Hail flux, repeated impact, humidity/temperature, manufacturing scatter, stress corrosion and proof-test damage are unmodeled. No actual lifetime Pf is identified."),
("trend-scope","Open inference","The inherited flat stiffness/density trend does not constrain defect reduction, strength scatter, interfaces, proof testing or structural redundancy."),
]
dump("NFI.json",[dict(id="051-"+id,tag=TAG,status=status,issue=issue) for id,status,issue in nfi_text])

# Update the source catalog while preserving the originally imported version.
evidence=json.loads((OLD/"MATERIAL-EVIDENCE.json").read_text())
for e in evidence:
    for key in ["recomputed_frame_mass_kg","recomputed_P3_SF","strength_gap_multiplier","m_gap_multiplier"]:
        e.pop(key,None)
    e["computation_status"]="complete; numerical virtual-construction comparisons in GAPS/WITNESSES/HAIL/DAMAGE"
    e["numerical_results"]="GAPS.json; WITNESSES.json; HAIL.json; DAMAGE.json"
dump("MATERIAL-EVIDENCE.json",evidence)
with (ROOT/"MATERIAL-EVIDENCE.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in evidence for k in x)));w.writeheader();w.writerows(evidence)
sources=(OLD/"SOURCES.md").read_text().replace("No new P3 mass/capacity calculation was admitted.","Completed conditional P3 mass/capacity calculations are in WITNESSES.json and GAPS.json.")
sources=sources.replace("For the draft orthotropic calculation","For the projected orthotropic calculation").replace("unvalidated draft assumption","unvalidated constitutive assumption")
(ROOT/"SOURCES.md").write_text(sources)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]