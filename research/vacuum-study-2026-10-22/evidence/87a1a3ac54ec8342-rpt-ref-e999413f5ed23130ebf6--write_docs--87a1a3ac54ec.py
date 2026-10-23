#!/usr/bin/env python3
"""Render the morning card and the complete additive register, following 030c."""
import json
import re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from intake import B,load

def text(name,value):
    if name in ("CARD.md","METHOD.md"):
        links=[]
        def hold(m):
            links.append(m.group(0));return f"@@LINK{len(links)-1}@@"
        value=re.sub(r"\[[^\]]*\]\([^)]*\)|`[^`]*`",hold,value)
        value=re.sub(r"(?<=[a-z])(?=0\d{2})"," ",value)
        value=re.sub(r"\b(0\d{2}[bcd]?)(?=[a-zA-Z])",r"\1 ",value)
        value=re.sub(r"\b(0\d{2}) ([bcd])(?=[^a-zA-Z]|$)",r"\1\2",value)
        value=re.sub(r"([a-z]{2,})(?=\d)",r"\1 ",value)
        value=re.sub(r"('s)(?=\d)",r"\1 ",value)
        value=re.sub(r"([a-z]{2,})(?=(?:R\d|SF|G/|F1))",r"\1 ",value)
        value=re.sub(r"([a-z]{2,})(?=(?:[+−]?\.\d|[+−]\d))",r"\1 ",value)
        value=re.sub(r"(\d)(?=(?:kg|mm|g/m|km|cm³|°[FC]|kN|GPa|MPa|psi|lb|kn|t\b|m\b|days|years|panels|members|points|rows|findings))",r"\1 ",value)
        value=re.sub(r"(?<=\d)(?=(?:ISA|PDT|PBO|Be|SiC))"," ",value)
        value=re.sub(r"\bSF(?=\d)","SF ",value)
        value=re.sub(r"(?<![\w\d])\.(?=\d)","0.",value)
        value=re.sub(r"(?<=[a-z])(?=(?:100|200|433|430|750|961)\b)"," ",value)
        value=re.sub(r"(?<=[A-Za-z])(?=T[123]\b)"," ",value)
        value=re.sub(r"([,;])(?=\S)",r"\1 ",value)
        value=re.sub(r"(\.)(?=[A-Z][a-z])",r"\1 ",value)
        for i,link in enumerate(links):value=value.replace(f"@@LINK{i}@@",link)
    (B/name).write_text(value.rstrip()+"\n")
def esc(x):return str(x).replace("|","\\|").replace("\n"," ")
def table(headers,rows):
    return "\n".join(["| "+" | ".join(headers)+" |",
        "| "+" | ".join("---" for _ in headers)+" |"]+
        ["| "+" | ".join(esc(x) for x in row)+" |" for row in rows])
def pretty(x):return json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)
def label(p):
    if p is None:return "none"
    names=["G","Q","E/Fcy","film"]
    return "+".join(n for i,n in enumerate(names) if p["mask"]&(1<<i))+f" {p['usage']:.6f}"

R=load(B/"RESULTS.json");coverage=R["coverage"]
intake=load(B/"INTAKE.json")
reports={r["id"]:r for r in intake["reports"]}
aliases=R["source_aliases_030d"]
def link(alias):
    rid=aliases[alias]
    for name in ("CHECK.md","CARD.md"):
        if (B/"snapshots"/rid/name).exists():return f"snapshots/{rid}/{name}"
    return f"snapshots/{rid}/report.json"

account=load(B/"P2-048-ACCOUNT.json");primary=account["primary"]
endpoint=primary["cure_included_endpoint"];least=primary["least"]
life=load(B/"DAMAGE-AND-LIFE.json");reliability=load(B/"P3-RELIABILITY.json")
p3=load(B/"P3-052-ACCOUNT.json");p3least=p3["primary"]["least"]
p3table=table(["R, m","Weather","Ground endpoint, kg","Pressure-only onboard, kg","Dry-cavity onboard, kg"],
 [[r,w]+[f"{next(x for x in p3['rows'] if (x['R_m'],x['weather'],x['service'])==(r,w,s))['all_axes_endpoint']['payload_kg']:+.3f}"
           for s in ("ground","onboard_pressure","onboard_dry")]
  for r in (10,12,15,20,30) for w in ("ISA","optimistic","both")])
p3bill=table(["R10 ISA least P3 bill","kg"],
 [[k.replace("_"," "),f"{v:.6f}"] for k,v in p3least["bill_kg"].items()]+[
 ["Total charged",f"{sum(p3least['bill_kg'].values()):.6f}"],
 ["Reference lift",f"{p3least['lift_kg']:.6f}"],
 ["Signed payload",f"{p3least['payload_kg']:+.6f}"]])
weather50=load(B/"P2-WEATHER-050.json");w50=weather50["results"]
weathertable=table(["R, m","Family upper offset at100m, K","Family at500m, K","Fixed hull at100m, K","Fixed mass, kg"],
 [[r]+[f"{next(x for x in w50['design_family_boundaries'] if (x['R_m'],x['z_m'])==(r,z))['worst_P_RH_upper_offset_K']:+.1f}" for z in (100,500)]+[
  f"{min(min(x['RH0_upper_offset_K'],x['RH100_upper_offset_K']) for x in w50['fixed_boundary_slices'] if x['R_m']==r and x['z_m']==100):+.1f}",
  f"{next(x for x in w50['fixed_builds'] if x['R_m']==r)['mass_kg']:.0f}"]
  for r in (10,12,15,20,30)])
supply=load(B/"BERYLLIUM-SUPPLY.json")
pending=load(B/"PENDING.json")
pending_names=[p["item"] for p in pending if p["status"]=="PENDING"]
snapshot=datetime.fromisoformat(R["snapshot_at"]).astimezone(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
changes=load(B/"CHANGES.json")
change_lines="\n".join(f"- **{c['title']}:** {c['text']} [{c['alias']}]({link(c['alias'])})" for c in changes)

billtable=table(["R10 ISA multilayer bake bill, kg","Named endpoint","Least G+Q+film"],
 [[k.replace("_"," "),f"{endpoint['bill_kg'][k]:.6f}",f"{least['bill_kg'][k]:.6f}"]
  for k in endpoint["bill_kg"]]+[
 ["Total carried",f"{sum(endpoint['bill_kg'].values()):.6f}",f"{sum(least['bill_kg'].values()):.6f}"],
 ["Reference lift",f"{endpoint['lift_kg']:.6f}",f"{least['lift_kg']:.6f}"],
 ["Signed payload",f"{endpoint['signed_payload_kg']:+.6f}",f"{least['signed_payload_kg']:+.6f}"]])
radiusrows=[]
for r in (10,12,15):
    for w in ("ISA","optimistic","both"):
        a=next(x for x in account["rows"] if x["R_m"]==r and x["weather"]==w and not x["floor"])
        f=next(x for x in account["rows"] if x["R_m"]==r and x["weather"]==w and x["floor"])
        radiusrows.append([r,w,
            f"{a['cure_included_endpoint']['signed_payload_kg']:+.3f} / {f['cure_included_endpoint']['signed_payload_kg']:+.3f}",
            label(a["least"])+" / "+label(f["least"])])
radius_table=table(["R, m","Weather","Endpoint payload, actual / floor kg","Least set, actual / floor"],radiusrows)
lifetable=table(["Film point","Initial SF","Ten-year warehouse SF","Ten-year .5% loss target SF","Target plus hot/restraint SF"],
 [[x["point"],f"{x['initial']['sf0']:.6f}",
   f"{x['ten_year_laws']['light_blocked_warehouse_endpoint_exponential']['film_SF']:.6f}",
   f"{x['ten_year_laws']['dry_protection_acceptance_target']['film_SF']:.6f}",
   f"{x['ten_year_hot']['full_restraint_hot_SF']:.6f}"] for x in life["film_life_rows"]])
damage_table=table(["Source / lead","Mass cost or debit","Effect on least SF and scope"],[
 ["044 / P2","+36.661200 kg with 3.414034 kg old-plate credit; otherwise +40.075234 kg",
  "Old six-pad core SF .714286; combined R10 scarf sensitivity .9891. New048/R30 value uncomputed; candidate life remains unqualified."],
 ["044 / P3","Not calculated","No P3 life or SF result; no Be-pad/scarf transfer."],
 ["045 / P2","25 kg shield exceeds old 14.581 kg margin; operating vent admits 2645.660 kg",
  "Local damage growth is adverse despite unchanged transferred gamma. Old028b shield usage1.021. Transfer to048 and valve/protection cost remain open."],
 ["045 / P3, CHECK-045","100 kg protection costs about .039 of old intact SF; protective value unquantified",
  "Member-loss filmSF .838835. Improved1.5/2mm wall witnesses .805476/.483053; tear witness .975445 at848.604kg. No damaged041 qualification."],
 ["046 / P2","Not calculated","PBO ageing is not a Be-sandwich life result."],
 ["046 / P3","95.751 kg protection; hot-film+equipment closure deficits31.465–51.465 /39.916–59.916 kg",
  "041 warehouse filmSF .985018/.933256; hot target .995706/.944784. FilmSF1 repair does not fix019 localSF .978132 or whole-hull mass."]
])
reltable=table(["041 f5 reserve","Peak compression at own screen, GPa","Pf: member-scale / 1cm³-scale","Member scale for Pf10⁻⁶, GPa"],
 [[x["point"],f"{x['peak_compression_Pa']/1e9:.6f}",
   " / ".join(f"{next(p for p in reliability['probabilities'] if p['point']=='041-f5-'+x['point'] and p['calibration']==cal)['frame_Pf']:.9f}"
              for cal in ("whole_member","coupon_1cm3")),
   f"{x['required_member_scale_for_Pf1e6_Pa']/1e9:.5f}"] for x in reliability["requirements"]])
top=f"""# MAINLINE-030d — morning design register

**QUESTIONABLE / PROJECTION throughout. Qualified installed-hull SF, failure probability and life remain unknown. Snapshot {snapshot}.**

| Lead / comparison | Current result | What it depends on |
| --- | --- | --- |
| **P2, 048 light-finish R10 ISA** | **+118.695 kg** named endpoint with cure compression; least **G+Q+film .842794**, modeled SF1 | Unqualified finish/optics/bond; optimistic .1mm exterior water; full bill below |
| P2, coated R12 / R15 ISA | Least **G+Q .895850 / .733994**, retained floor | Cure-included account at R10–15; no both-weather float |
| P2, heavier retained water | **All 432 new 1mm cases fail to float** | Best all-four −998.333kg; exterior retention unmeasured |
| P2, 050 weather extension | **No R10–30 sampled size closes the declared10% hot profile** | Original048 account; fixed full-range builds have narrower windows than day-design families |
| **P3, 052 resized whole bill** | Ground-service full endpoints **R10 ISA +30.863 kg / R12 optimistic +46.259 kg**; R10 least **S+F+J .839340** | Requires unqualified **5.343 GPa effective ply strength** and **15.552h planned ground service** |
| P3, 052 service/weather limits | **No combined-weather or24h onboard-dry closure throughR30** | Chosen f5 family and pump/battery model; no universal architecture claim |
| P3, earlier fixed 041 /046 witnesses | Intact1.143285/1.083205; local1.033223/.978132; warehouse film.985018/.933256 | Still valid for those geometries;052 changes section, strength assumptions and account |

**R30 Be burden:** original040 endpoint **102.231t**, about **23.6%** of020's historical433t world mine output; finished-sheet capacity is unknown. **Damage tolerance is not demonstrated for either lead.**

**First three tests remain:** finished-sheet compression/specification; weighed curved sealed scarf, including042's full-blank extension; same-batch wrinkle coupons.

**Preserved:** 98 rows and961 findings. **Current:** {coverage['total_register_rows']} rows, {coverage['total_attributed_findings']} attributed findings; {coverage['new_canonical_reports']} new reports dispositioned. [Pending work](PENDING.json), [complete register](REGISTER.md), [corrections](LEDGER.md), [optimism](OPTIMISM-LEDGER.md), [ground-first](GROUND-FIRST.md).
"""
body=f"""
## Changes since 030c

{change_lines}

## P2: the complete 048 bill and its conditional floats

The latest account separates **optical finish, structural primer, exterior liquid and absorbed material water**. The multilayer finish is7.5752g/m² plus10%, or8.33272g/m² installed allowance, with transferred dry optics α=.09/ε=.80. Structural primer adds10g/m². Neither is a weighed, qualified Be finish. The alternative finishes and all drying routes remain in048's432 original configurations and the648-row CHECK-040 addendum. [048]({link('048')}), [048 addendum]({link('048fold')})

**Partial CHECK-048 is now filed; its full check remains PENDING.** It reproduces the compared mass bills, modes and payloads at all7149 stored points using the owner temperature tables, including the original+124.261910kg R10 endpoint at its supplied geometry. Its16679 raw differences are confined to initial-gas, counted-gas and desorption bookkeeping; proposed checker amendments remain unverified. Its independent thermal reconstruction differs in297/325comparisons, and independent least-set, E-axis bounds and auxiliary audits are unfinished. This is not a full independent verification of048 or its cure addendum. [Partial CHECK-048]({link('CHECK048partial')})

**Classical CCAg citation correction:** the source cited by048 gives **α=.08 and normal ε=.72 on Kapton**, whereas its modeled classical row uses.09/.65. The corrected source statistic and substrate must accompany that row. No automatic substitution or corrected-optics rerun is claimed. The selected multilayer recipe also lacks a matched installed-Be mass/optics specimen; the general qualification remains open.

The table uses cure compression in global/crimp demand. The named endpoint applies fullG/Q and .015lb/ft² film at each interface. The least-set point has **γ={least['properties']['gamma']:.9f}, Q={least['properties']['Q']:.9f}, film={least['properties']['film_kg_m2_interface']:.9f}kg/m² per interface** at usage{least['usage']:.9f}; its payload is a numerical zero. **The +118.695kg endpoint is not spare payload at the least-optimism point.** Each has a conditional modeled leastSF of1; neither has an installed-hull SF.

{billtable}

Joining is `max(actual joining,5% of faces+core)` in the retained-floor convention, with the separate structural primer outside that charge. Film, scarf, splice and seal are already inside joining. Daily sealed service is nested in100kg systems; extra30/50kg alternatives remain in048 if that allocation is committed elsewhere. The70kn pad is a resized mathematical load-path bill; cells are vented. All selected-point sources, full mode factors and dependencies are in [P2-048-ACCOUNT.json](P2-048-ACCOUNT.json).

The bake target removes90% of the **added material-water inventory**. At this R10 endpoint it changes1.369kg to.137kg. It does not reduce the125.664kg exterior-service charge. Dry gas retains the added inventory; onboard sorbent retains captured water and adds a bed/cartridge. Measured exterior retention before or after each route remains unknown.

**0.1mm is019's optimistic equivalent retained-film assumption;1mm is a separate conservative scenario.** Neither is a measured limit for these finishes. All432 new R10–15 cases at1mm are negative under both cure treatments; best all-four payload is−998.333kg and even the intentionally favorable interior-optimism bound is−998.280kg. CHECK-040's old 040 1 mm R30 example is−594.989kg. That old coating account does not establish the uncomputed new-finish R30 result. Wet optics and future rain/dew/frost remain open. [Water/bond sources](snapshots/{aliases['048fold']}/WATER-AND-BOND-SOURCES.md)

For multilayer finish, bake target, .1mm exterior water and cure compression included:

{radius_table}

The search objective is minimum axis count then common logarithmic usage. R12 andR15ISA therefore use two axes, whileR10 needs three. The original040R30 least-usage design remains a separate comparison, with a heavier finish and a different primer account. Newly filed050 extends the original048 finish account throughR30, but **no common cure-inclusive R10–30 search is claimed**. The generic “light coating makes P2 float” claim applies only to explicit scenario rows.

Including cure compression reduces the original048R10 bake endpoint+124.262kg to+118.695kg and removes all allowable floats in two marginal configurations: AgFEP05/R15/optimistic/floor/desiccant and AgFEP1/R15/optimistic/floor/dry-gas. CHECK-040's original R15 optimistic/actual all-four−1.821166kg row is reproduced separately. Edge/scarf coincidence removes four of thirteen original040 primary floats; it is **not** a quantified rerun of every048 coating row.

The detailed200°F source tests use **AF163-2K .060lb/ft², EC-3924B, metal-to-metal joints and50psi**. They do not qualify2U .015 Be/5056 honeycomb, tooling pressure or actual stress-free temperature. The040/037b fold is explicitly incorporated: all250°F as-designed rows fail their minimum-strength edge screen. The original+.120151kg scarf fix is a geometry-specific allowance, not a universal repair surcharge.

## 050 weather: a family of designs versus one fixed hull

050 reports2,027,245 weather points, all16 optimism subsets and retained minimum-cardinality ties overR10/12/15/20/30. It extends the **original048 account**, reproducingR10 ISA+124.262kg; it does not claim a rerun of the separately filed cure-included alternative. Its R20/R30 extension therefore does not extend the corrected+118.695kg account by implication. The following upper ISA offsets cover the entire RH0–100% / sea-pressure-anomaly±30hPa rectangle:

{weathertable}

The family can change geometry for each design day. Each fixed build instead retains the mass required for103.953kPa and its cold design point. The projected cold-interface boundary is aboutISA−10.5K at100m and−7.9K at500m. At500m onlyR30 retains a common fixed-hull window across the full pressure/humidity rectangle, about−7.9 to−6.8K. Extra cold-air buoyancy does not override a failed interface screen.

**No sampled size closes the declared MIL10% hot profile, even with all four optimistic endpoints.** AtR30 the all-four deficit is about2771kg. The1/5/10% hot, joint hot-humid and low-pressure markers all fail; absolute-humidity marginals give a different answer when assumed saturated than when paired with41°C air. The missing coincident weather is explicit. These markers are not annual flight probabilities or an impossibility proof at every radius.

Twelve-hour all-retained deposition is about.085–.090kg/m² in the clear reference, .0035–.0038 overcast, .236–.243 saturated-clear and.081–.084 cold frost. Latent heat makes the reference R10 case liquid rather than frost. With actual night density, dry-startR10 reference payload is **+117.381kg**, while saturated-clear is **−82.280kg**;R12 saturated-clear retains only about33kg. The dry-start deposit uses the reserved.1kg/m² allowance; a preexisting film is additional. The latter comparison is arithmetic, not a wet-start transient.

No drainage fraction is credited. R10 clear-night heating is about26.6kW/319kWh, or2952kg battery before installation; the chosen overcast case is162kg battery. A carried10–50g/m² cover adds12.6–62.8kg atR10 before supports/water. Projected low-emittance switching, ground power/support, morning waiting and ideal2.8/7.6h solar evaporation energy equivalents remain conditional mitigations, not free water removal or dry-out forecasts. The15 reported numerical checks address convergence and source-model reproduction; wet optics, actual retained water, installed controls and independent thermal validation remain open. [050]({link('050')}), [complete attributed weather result](P2-WEATHER-050.json)

## R30 supply and the Be-free branch

At the original040 R30ISA named endpoint, faces weigh **{supply['Be_faces_kg']/1000:.6f}t**: **{supply['share_2024']*100:.3f}%** of020's revised2024 world mine-output433t, or **{supply['share_2025']*100:.3f}%** of its2025 estimate430t. The least-usage point instead has{supply['least_usage_point_faces_kg']/1000:.6f}t faces. Keep the endpoint and least-set masses distinct.

These historical totals measure Be content, not available SR-200 sheet, current world output, fabrication yield or a purchase budget. Thin-gauge forming, post-form compression, double curvature, kilometre-scale seams, supply and controlled processing remain unqualified. [Exact supply comparison](BERYLLIUM-SUPPLY.json). The049 Be-free answer is PENDING unless a final report is listed in the filing snapshot.

## Damage and life: mass and SF effects for both leads

{damage_table}

The mass costs above are **scenario-specific**. The source geometry and annual spectrum must accompany every number; none is a validated fixed surcharge on the newer lead. Unpriced parts remain unknown, not zero. [DAMAGE-AND-LIFE.json](DAMAGE-AND-LIFE.json) retains both lead entries for044,045 and046.

**044/CHECK-044:** the original six-pad coreSF=.714285714 and plate-only damage-one index949.846393days are not survival predictions. The rigid ambient minimum-L thermal index3697.149914days and free-edge200°F minimum-W index18816.049843days use different load/mean-stress assumptions. The strict candidate's29.092835kg pads plus10.982399kg scarf change cost40.075234kg before any credit; the quoted36.661200kg requires removal of3.414034kg already aboard. Its .060lb/ft² titanium double-lap fatigue series is **AF163-2K**, not2U; the mass increment is unchanged. Qualified installed life remains null. [CHECK-044]({link('CHECK044')})

**045:** at028b's old geometry each face carries238.652kN/m. Critical lost-core diameters are54.779991mm clamped and27.127598mm simply supported. The modelled50.8mm hail produces an80.865mm crushed zone; growth occurs in two of three clamped readings and all three simply supported readings. Narrow-dent survival in a transferred global-gamma map does not prevent local crushed-core failure. Source “no damage-tolerant fix on budget” is adverse evidence for those old budgets; it is not a rerun of048's improved mass account.

The P3 hail probabilities .0113–.0528 per strike use transferred tube specimens and an unvalidated impact model. Removing one member in linear rigid-joint surrogates raises peak stress2.427–3.271× and merged-bay filmSF falls to.838835. This supports a damage-tolerance concern, not a solved nonlinear cascade probability on the resized041 frame. Source shelter/vent proposals require hardware, ground restraint, inspection and mission evidence; they are not qualified procedures. [045]({link('045')})

**CHECK-045 is complete with corrections.** It reproduces the major conditional danger screens while distinguishing71 differences in1358 comparisons and88 exact findings. Its55mm clamped growth threshold is **19.176311mm**, within the23.237218mm core. Pach's stored test-depth field is.0011m; the model's1.489–1.541mm peak depth does not agree with the1.1–1.2mm measured residual range. IEC prints35/55/65mm ball masses20.7/80.2/132.0g; their corrections do not change the50.8mm design case. The historical P3 Perry screen is **3.454499160**, not4.095817936, leaving nominalSF1.258252477 unchanged.

The check reproduces all56 selected frame comparisons and widens coverage to every f4/f5edge class: stress ratios **1.959485–3.270739**, maximum tension **0–1019.372MPa**. The four old removals are examples rather than every-member bounds. Stronger local-search witnesses give1.5/2.0/3.0mm-wallSF **.805476/.483053/.223304**, and the303.532MPa tear-screen witness reaches **.975445 at848.604kg film**; none reaches1. These replace unsupported best-point claims, not all historical source values. Exact independent50%-failure counts60.877292/12.784859 have unchanged integer ceilings61/13; repeated identical loading is not automatically an independent strength redraw.

Twenty-four half-kilogram leak-event times are corrected, including.464206s at a100mm hole and.000837478s for a torn bay. First ground contact forR10 occurs at10m centre height, not zero: the same reference torn bay reaches contact at23.099647–34.541863m/s. The trajectory uses a4889.444kg gross-neutral reference, not a demonstrated built inventory; admitted gas is not net heaviness. Sea-level air for the same vent differential is2912.791kg. Tap-test transfer and the0.2mm contour threshold do not establish Be detection. **No universal dynamic cascade, every-puncture opening or safe venting procedure is inferred.** All88 exact findings and31NFI records are preserved. [CHECK-045]({link('CHECK045')}), [exact findings](snapshots/{aliases['CHECK045']}/MISMATCHES.json)

**046/CHECK-046:** the films require nominal retained fractions .794753/.874673/.923186 for022d-5/041-5/041-019. Ten-year scenarios are:

{lifetable}

The .5% annual-loss case is an acceptance requirement, not an observed ageing law. Hot/full restraint consumes further margin; CHECK-046 gives a .457% annual loss ceiling for hot041-5, below that requirement. Warehouse source-reading uncertainty alone crossesSF1 at both041points. The019 local-shell sensitivity.978132 remains independently adverse even if the film is restored toSF1.

The041 OD4/white package is95.751kg. With30–50kg vacuum hardware and5kg adhesive placeholder it already exceeds the100kg allocation; .714/9.165kg hot-film additions increase the deficits to31.465–51.465/39.916–59.916kg. There is no spare payload credit. A268.099kg replaceable skin set and annual renewal do not establish a safe interval or reset frame/joint fatigue. SK99's static chemistry-only mass does not establish ten-year creep suitability. The coupon-water throughput label is corrected:458.672527kg/year becomes459.261468kg/year with declared-weather weighted leakage; it is removed at service, not accumulated airborne. [046]({link('046')}), [CHECK-046]({link('CHECK046')})

## P3: 052 whole bill, ground interval and changed assumptions

**052 is now filed.** It resizes the checked f5-019 family atR10/12/15/20/30 with constant gyration/radius and enforces the conservative peak local-shell screen. The first tested ground-service closures are **R10 ISA** and **R12 optimistic**. Their full endpoints are **+30.862710 / +46.258872kg**. The optimistic continuous crossing11.3584m is conditional on this family; no ISA radius below10m was searched. The alternate checked f5-5 family remains−21.563kg atR10 ISA. This is a new section/strength/account scenario, not a retrospective repair of041's original019 local factor. [052]({link('052')})

The axes are **S** assumed complete-member compression1→3.9GPa; **F** effective ply strength3.48→5.8GPa; **L** ten-year retention.861568874→.951110130; and **J** the max(actual,5%-of-tubes) allowance→actual sleeves. Least set means fewest axes, then common logarithmic usage. AtR10 ISA the least set is **S+F+J at.839340211**, with **5.343007948GPa effective ply strength** (92.12% of raw5.8GPa yarn), baseline retention.861568874 and45.874kg joint allowance. Its S-axis assumption is3.134038GPa, while its calculated peak compression requirement is1.055318GPa; these are distinct quantities. Keeping the inherited60% ply efficiency does not closeR10, althoughR12 ISA can close at3.48GPa.

At that resizedR10 root, globalSF1.083359, enforced peak-localSF1, ten-year filmSF1 and sized-jointSF1 are conditional component screens. Qualified installed SF and life remain unknown.

{p3bill}

The95.751kg OD4/white package already includes the034 barrier; it is charged once. The100kg systems line and **additional50kg service line are separate**. Explicit gas, exterior water, contamination and weather replace the old bulk reserve. The33.138kg mooring allowance is derived fromP2; theP3 hardpoint is not qualified. Damage-tolerance repair has no validated cost or design, so this intact closure does not close045/CHECK-045.

{p3table}

Pressure-only pumping cannot claim the dry-film life assumption. At theR10 least point, external water-vapour inflow is1.258056kg/day; the chosen32.5165Pa water-partial-pressure limit is reached in **17.279789h**, giving a planned **15.551810h** ground interval. The separate total-pressure limit is450.240558h. A colderh2 scenario shortens humidity time to11.474873h. These require assumed dry fill,90% material conditioning and transferred installed leakage; they are not a qualified operating schedule. Initial evacuation to10Pa in24h calls for roughly1575m³/h effective ground speed.

The24h dry-cavity packages use15–148 E2M28 units with75% nominal-speed and1000W/unit planning assumptions, plus batteries. TheR10 dry package is about4039kg and360.12kWh/day. Their failure to float is specific to the selected barrier/hardware/power assumptions. No combined-weather radius through30m closes; its negative cubic surplus also prevents simple enlargement of this chosen family from rescuing it. An additional.9kg/m² of exterior water alone costs1130.973kg atR10.

**Comparable allocation requires the cure correction too.** 052's source table subtracts50kg extra service from original048 endpoints, givingR10 ISA+82.640676kg. At the filed cure-included all-four point, the same allocation gives **+77.253kg**;R12 optimistic retained-floor gives **+28.576kg**. These are labelled fixed-point arithmetic, with no P2 reoptimization or new least-set claim. The+118.695kg P2 headline is its named G+Q+film endpoint under its original nested service convention. No confidence ranking follows from payload or axis count. [Full052 account and both comparison bases](P3-052-ACCOUNT.json)

At the new052 R10 root, hypothetical m10/3.9GPa compression calibration gives member-population Pf.000947798 versus1cm³-coupon Pf.824296. Neither is calibrated or a hull/lifetime probability. The earlier041/043 numbers below describe different fixed points. 052 reports1440 internal assertions and253 input pins; this register has not independently rerun its numerical search.

## P3 reliability and the proof correction

043's041supplement and CHECK-043 use the750-member f5 frames at their own screens. The m=10 and3.9GPa scales below are hypotheses, not measured distributions:

{reltable}

No measured finished-member compression Weibull modulus, characteristic scale, reference population or confidence bound supports either calibration. These are tube-fracture-only probabilities; joints, membrane, shared flaws, instability and lifetime damage remain outside them. The required scales are arithmetic targets, not new material allowables.

**Partial051 adds the operating-load distinction and a complete288-row target surface.** With the hypothetical whole-member3.9GPa/m10 distribution, q=1 gives Pf=.000643916/.000947308 for5%/019reserves; both meet10⁻³ inside that restricted hypothesis. At the higher own-screen loads they do not. The own-screen complete-member scales for Pf10⁻³ are4.278678/4.209090GPa; the1cm³ coupon targets are9.088382/8.907641GPa. Equal-member and common3m-reference distributions remain different conventions.

051 reviews14 construction families but leaves candidate masses, SFs, comparative rankings, resized041hail probabilities and dynamic cascade results unfinished/null after admission refusal. M55J/T700S composite compression averages890/1450MPa are not complete-tube scales or allowables. Its correction distinguishes045's f5stress factors2.427/2.480 from the larger3.27f4factor; no dynamic cascade was solved. The assignment stays PENDING. [Partial051]({link('051partial')}), [completed target surface](snapshots/{aliases['051partial']}/TARGET-SURFACE.csv), [partial-filing scope](PARTIAL-FILINGS.json)

**The030d brief's “proof testing would buckle the tubes” statement is corrected.** In CHECK-043's original selected-member example,1.25× target axial force gives1.259378651× peak stress and a member Euler ratio of **.375**. Exceeding a combined/local/global source screen does not establish individual Euler buckling. The separate f5 proof examples also exceed their respective screens; fixture, local/assembly stability, stress coverage, rejection population and proof damage remain unresolved.

**Rise8 is5446.290626kg charged total; the tubes alone are5039.557739kg.** The406.732887kg difference is the inherited joint/node/film/systems allowance. That label correction does not alter the headline probabilities; the frozen rise8 force solution remains independently unverified. [CHECK-043]({link('CHECK043')})

CHECK-041 corroborates the fixed f5 screen values and supplies an independent zero-start m24 nonlinear bracket [5.430900815498,5.430922833327]. It reports nine differing printed cells: three nonlinear midpoints and six film values. Its rigid/pinned film multipliers7.151119777/2.046193535 differ from7.155002497/2.047133403; direction-field reproduction remains open. The check discloses earlier owner postprocessor exposure and did not rerun optimization. Bare-pin mechanisms do not become a stable practical frame. [CHECK-041]({link('CHECK041')})

## Build, thermal evidence and first grounding work

CHECK-042 corrects **S-II's .254mm core-face matching gap**, which is not measured spherical error. Its simply supported critical disbond is27.127598mm; clamped54.779991mm. Two-skin seam length is5683.037088m at30:1 and5685.225425m at30.34:1; the latter coverage approximation needs at least1190panels per skin. Full-cohort tap a90/95 is41.8/29mm, not the selected-cohort43.3/28mm pair. None qualifies Be-specific inspection, the moulded shape, sheet supply, forming strain or seam process. The original028b unallocated mass is zero. [CHECK-042]({link('CHECK042')})

CHECK-040's primary arithmetic is conditional on the owner temperature table; the independently interpreted heat balance differs. The048addendum now states the existing natural/forced convection selection and conductance approximation explicitly. **That disclosure does not close independent or physical thermal reproduction**, combined mission weather or wet-finish optics. Original039stiffener,029gamma,037thermal,034service and all other030c findings remain in the preserved register.

The first three tests remainT1 compression/specification,T2 weighed curved sealed scarf with 042 F1 extension,T3 same-batch wrinkling. Finish/retention, loaded damaged panels/members, protected-film life and finished-member statistics/proof are added to the existing grounding routes. Costs are scenario estimates; this report authorizes no purchases or tests. [GROUND-FIRST.md](GROUND-FIRST.md)

## Filing scope

**PENDING:** {', '.join(pending_names)}. CHECK-048 and051 have partial filings; their completed portions are incorporated, and their unfinished portions remain pending. 050 and052 are now filed. The earlier050admission refusal is preserved as history; its completed card records authorized unchanged retries. Pending means no completed canonical report in the recorded scan, not an observation of a running seat.

The order-pinned COMMON.md changed during preparation. Its two added operational paragraphs require simjob for heavy runs and authorize unchanged-resource retries after admission refusal. They change no scientific input in this register. The original and both observed revisions, with exact differences, are recorded in [SOURCE-DRIFT.json](SOURCE-DRIFT.json). The pinned original remains intact.

All{coverage['new_canonical_reports']} new reports and{coverage['new_report_artifact_pins']} direct pins are indexed. Every prior row, finding, correction/optimism entry and ground-first route is retained. Current030d annotations govern over historical wording inside preserved sources. [METHOD.md](METHOD.md), [SOURCE-INDEX.json](SOURCE-INDEX.json), [VALIDATION.json](VALIDATION.json).

Stop and file one report. The robotics seat sends the next job.
"""
text("CARD.md",top+body)

reg=load(B/"REGISTER.json")
parts=["# MAINLINE-030d — complete attributed issue register",
       "QUESTIONABLE / PROJECTION. Current030d annotations govern; prior fields and findings remain verbatim history."]
for row in reg["rows"]:
    parts+=[f"## {row['rid']} — {row.get('topic_name','')}",
            row.get("current_030d",row.get("current_030c",{})).get("text",row.get("gap","")),
            "```json\n"+pretty(row)+"\n```"]
text("REGISTER.md","\n\n".join(parts))
for name,title in [("LEDGER","Corrections"),("OPTIMISM-LEDGER","Optimism ledger")]:
    d=load(B/(name+".json"))
    parts=[f"# MAINLINE-030d — {title}",
           "QUESTIONABLE / PROJECTION. All inherited entries are preserved;030d entries and annotations carry current corrections."]
    for i,row in enumerate(d["rows"]):
        heading=row.get("name") or row.get("correction") or row.get("id") or str(i+1)
        parts+=[f"## {i+1}. {heading}","```json\n"+pretty(row)+"\n```"]
    text(name+".md","\n\n".join(parts))
ground=load(B/"GROUND-FIRST.json")
text("GROUND-FIRST.md","# MAINLINE-030d — ground-first evidence\n\n"
     "QUESTIONABLE / PROJECTION. Preserve T1 compression/specification, T2 weighed curved sealed scarf including F1, T3 same-batch wrinkle as the first three. No procurement or test execution is authorized here.\n\n"
     "```json\n"+pretty(ground)+"\n```")
parts=["# MAINLINE-030d — new report dispositions",
       f"Snapshot {snapshot}. Earlier reports remain in [030c's report index](baseline030c/REPORTS.md)."]
for c in changes:
    r=reports[c["report"]]
    parts+=[f"## {c['report']}",f"[Filed evidence]({link(c['alias'])})",
            c["text"],"### Canonical report body",r["body"]]
text("REPORTS.md","\n\n".join(parts))
text("METHOD.md","""# MAINLINE-030d — preservation and synthesis method

QUESTIONABLE / PROJECTION. This register extends030c's source identity, snapshot, topic routing and ledger workflow. The full030c manifest, including its build code and nested030b history, is retained under `baseline030c`. No numerical source model is imported, copied into a solver, or executed by this register.

1. intake.py verifies the canonical030c report and every manifest entry, preserves bytes, and snapshots new canonical reports after04:03:32PDT excluding every report already indexed by030c. All direct artifact pins are verified. New numerical results come only from filed reports. An operational exception can be included without treating its numerical card as complete.
2. normalize.py preserves complete NFI records, including nested inherited documents. Identity is report, original file and JSON pointer. Every complete finding keeps its fields; auxiliary metadata and document-level qualifications remain inNEW-NFI-SOURCES.json. Attributed duplicates are not counted as independent physical gaps.
3. build_register.py preserves all98old rows and961findings, both ledgers and all grounding routes. New findings receive one primary topic through recorded rules and source-specific defaults. Current030d annotations coexist with the immutable history. Every newly ingested report must have an explicit semantic change disposition or the build stops.
4. Selected048 and all45 052 scenario points and bills are copied from filed data. Summation, mode minima, gamma/Q/film ratios, the same-allocation extra50kg service debit, historical433t/430t supply shares and conditional Weibull hazard inversion are the only new arithmetic. The052 source comparison used original048; its cure-included comparison is separate fixed-point arithmetic. No geometry optimization, finite-element solve, new source research, life qualification or damage-model rerun is claimed.
5. write_docs.py renders the morning summary, one line per change, full bill, damage/life matrix, corrected proof and manufacturing statements, complete attributed registers and ledgers. Historical false labels remain only as attributed source history; current annotations give corrected values.
6. validate_packet.py checks byte/field preservation, every source pointer and routing identity, ledger/grounding preservation, required corrections, selected arithmetic, source coverage, pending dispositions and rendered file links. These are register-integrity checks, not independent certifications of source models.

Reproduce: run normalize.py, build_register.py, write_docs.py, validate_packet.py in this directory with Python 3. Refresh intake.py only while deliberately incorporating additional filings; each new report requires explicit disposition. Final filing records one frozen source boundary. A final canonical scan checks for any unincorporated report immediately before submission.

Source snapshots may contain historical nonstandardInfinity/NaN in infeasible alternatives. Those original bytes remain unchanged. Current exported records are strict finite JSON; unavailable physical capacities remain null. All timings are measurements only. Writes stay in the own seat's.ship tree. No seat is restored, woken, inspected for live progress or contacted out of band.
""")
print("Rendered",coverage["total_register_rows"],"rows;",len(changes),"changes; card words",len((top+body).split()))
