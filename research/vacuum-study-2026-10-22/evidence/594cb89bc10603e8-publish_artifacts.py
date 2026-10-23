"""Render the independent check, with definite and conditional findings distinct."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json

ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT / "INPUTS.json").read_text())
R = json.loads((ROOT / "RESULTS.json").read_text())
V = json.loads((ROOT / "VALIDATION.json").read_text())
O = D["owner_results"]
now = datetime.now(ZoneInfo("America/Vancouver")).isoformat()

mass_rows = []
used = set()
for row in R["p3"]:
    if row["row"] in used:
        continue
    used.add(row["row"])
    old = next(x for x in O["p3"] if x["row"] == row["row"])
    mass_rows.append(f"| {row['row']} | {old['tube_mass_kg']:.6f} | {row['tube_mass_kg']:.6f} |")
mass_table = "\n".join(mass_rows)
pad_rows = []
for name in ["mooring_016_one_pad_SF1", "mooring_016_six_pads_SF1",
             "mooring_70kn_one_pad_SF1", "systems_100kg_six_pads", "reserve_411kg_one_pad"]:
    row = R["pads"][name]
    old, proposed = row["log_only_reproduction"], row["simply_supported_uniform_boss"]
    pad_rows.append(f"| {name} | {old['thickness_m']*1000:.3f} | {proposed['thickness_m']*1000:.3f} | "
                    f"{old['mass_total_kg']:.6f} | {proposed['mass_total_kg']:.6f} |")
pad_table = "\n".join(pad_rows)

card = f"""# MAINLINE-037 independent check

**The principal scalar arithmetic reproduces, but the filed card needs material, mass, source and model corrections.** All 541 numeric leaves of RESULTS.json have an explicit audit disposition. Ten tube-mass entries disagree with the upstream SiC/arc geometry; 84 thermal or projection entries cannot be independently recovered from the supplied inputs. Reproducing conditional arithmetic does not verify its temperatures or establish installed-hull safety.

Unit `vacuum-mainline037-check-1020`; order `ord-admiral-rr2-check037-codex-8497-1020`. Evidence and checking assumptions are in [INPUTS.json](INPUTS.json). The owner's six artifacts and six input references were hash-checked. `loads037.py` was hashed only: it was never inspected, imported or executed. All material transfers and engineering screens remain **QUESTIONABLE**; the countermodels and unqualified assembly assumptions are **PROJECTION**. Rendered {now}.

| Requested check | Independently calculated result | Disposition |
|---|---:|---|
| Be gradient coefficient | 1.771734429 MPa/K | Reproduces declared formula |
| Pressure face stress | 298.4358567 MPa | Reproduces geometry |
| Coated day-rise shear / typical W strength SF | 143.787762 kPa / 1.678282645 | Conditional on filed temperature |
| Coated day-night shear / SF | 263.037296 kPa / 0.917423153 | Conditional; below unity |
| Flight **increment-only** seven-screen minimum | 1.003303481 | Reproduces |
| 70-knot seven-screen minimum | 0.998441984 | Reproduces |
| Bare 0.0707 m² mooring patch SF | 0.353533014 | Load-only bearing screen reproduces |

The current E=290 GPa and full-endpoint E=293.6 GPa uses are distinct and intentional upstream. The 345 MPa input is a tensile-yield proxy for compression; 379.2 MPa is a historical lot result, not a thin formed-sheet allowable.

**P3 material and mass corrections.** All eight 022c rows use SiC tubes: the Euler/section/arc identity independently returns 410 GPa, and the mass identity returns 3100 kg/m³ in every row. Ti and CFRP label fittings. MAINLINE-037 instead implies tube densities of 4430 and 1600 kg/m³ for those rows and uses chord length for every tube mass while retaining arc-based upstream capacities.

| 022c cap row | Filed tube mass, kg | SiC/arc check, kg |
|---|---:|---:|
{mass_table}

The ten numeric mismatches include two repeated projection rows with alternative film CTEs. [AUDIT.csv](AUDIT.csv) identifies every exact result path, field, filed value, check value and basis. [CORRECTIONS.csv](CORRECTIONS.csv) separately records source corrections and conditional model changes.

Changing the frame CTE to SiC's 4.5e-6/K, holding the unreproduced temperature fields fixed, and adding steady flight pressure gives conditional minima of **0.739889 / 0.699994** for Ti-fitting/Kapton 5%/019 and **1.449566 / 1.376622** for CFRP-fitting/Zylon 5%/019. The latter geometries still fail the filed half-wave test. These are load sensitivities, not repaired thermal solutions. The prose also quotes Ti/Kapton uniform least as 0.74170; the actual uniform film minimum is **0.739113638**.

**Temperatures and solar pattern.** The 84 unresolved entries comprise 60 P3 temperatures, 10 P2 temperatures/swings, and 14 Legendre coefficients. Missing inputs include heat-transfer velocity, film/tube optical properties, complete sky/ground and cavity view factors, stress-free temperatures, angular temperature samples, and projection weights. A named correlation alone does not specify the heat problem.

From the *filed* n=2..6 coefficients, exact absolute residual maxima are **8.292853 K coated and 14.851720 K bare**, rather than 5.788444 and 17.145083 K. If the latter numbers describe an untruncated field, that field must be provided and the labels distinguished. Applying the stated constrained-bound formula to the filed reconstruction gives **29.38547 / 52.62661 MPa**, instead of 20.51117 / 60.75307 MPa. Analytic angular derivatives give bending screens **0.818470 / 0.771906 MPa**, only about 0.032% above the reported values; this small discretization difference is separate from the reconstruction discrepancy.

The scalar curvature expression and a membrane-free displacement trial do not establish complete thermoelastic equilibrium. A full solution needs both shell curvature components, constitutive relations and force/moment equilibrium. The audit therefore retains the pattern-stress claim as an NFI, rather than asserting a replacement installed stress.

An independently specified two-face model supplies a usable proposed thermal calculation in [THERMAL-COMPARISON.json](THERMAL-COMPARISON.json). It closes both local heat balances and whole-cavity radiation, uses equal sky/ground views, and varies a declared convection coefficient. At h=5 W/m²K its coated subsolar faces are **300.464904 / 300.064673 K**, and bare faces **345.666334 / 343.952862 K**. These alternatives show the effect of assumptions; they are not a recovery or validation of the filed 301.569/301.170 and 356.946/355.038 K.

![Declared thermal sensitivity](thermal-boundary-sensitivity.png)

**Wind source and combined load.** The FAA document's §3.6(b) includes the alternative lower bound 0.65 VH and defines design speeds as equivalent airspeeds. §3.9 includes gusts in any direction and both dynamic and steady loads. Its Appendix B explains that the earlier 78-knot mooring figure was reduced to 70; it is not an unresolved conflict with Table 4. See the [FAA primary document](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/airships/aceAirshipDesignCriteria.pdf), printed pp12, 15, 23, 121–122, with local page images and a pinned PDF.

At the owner's local-density/speed convention, the 290.633721 Pa gust value is only the increment. The selected 35-knot baseline contributes **189.213887 Pa**, giving **479.847608 Pa** total aligned stagnation pressure. Including both lowers the conditional P2 seven-screen minimum to **1.001324769**. EAS/TAS treatment still needs a consistent selected flight requirement. The original 70-knot arithmetic is sound; its capacity multiplier to reach unity is **1.001560447**, or approximately 0.156%. Mean potential-flow Cp=-0.5 does not prove a uniform-pressure buckling bound for a nonuniform loaded shell.

**Pad sizing.** The filed masses reproduce
`t² = 3F(1+nu) ln(a/b)/(2π Sy)`,
with inferred Sy=276 MPa, nu=0.33, density=2700 kg/m³, boss radius b=25 mm and a 1 mm thickness floor. Those inputs and the complete support/load model were not supplied. For an explicitly specified **uniform circular boss load and simply supported outer edge**, solving the plate boundary problem instead gives
`t² = 3F[(1+nu) ln(a/b) + 1 - (1-nu)b²/(4a²)]/(2π Sy)`.
This is a proposed model, not an assertion that it represents a pad continuously supported by honeycomb.

| Pad case | Filed t, mm | Proposed t, mm | Filed total kg | Proposed total kg |
|---|---:|---:|---:|---:|
{pad_table}

Under the recovered boss-radius assumption, the systems pad's filed 14.683 mm radius is smaller than the 25 mm boss; the alternative enforces containment. If the inherited p/2 core preload also acts under a compression pad, the original F/crush area gives **SF 0.834870**, not 1. The 48.259 kN one-pad example then needs **0.249289 m² and 12.6334 kg** in the proposed plate model. This is conditional on the actual load direction and reaction path. Face bending, bond peel, local shell failure, fittings and installation mass remain unclosed.

P3's 7/2/1 member counts reproduce scalar 5% load sharing; they do not supply attachment geometry or mass. The 411.299 kg reserve includes environmental lift losses and distributed water, not a single suspended payload. Its 4.033 kN pad is only a hypothetical concentrated-load case.

**Restoration and carry.** The 5863/1634 kg numbers are proportional sensitivities, not demonstrated re-sized, mass-closed structures. With corrected mass, CTE and total flight load, the same sensitivity becomes **5882.9 kg for Mylar-5 and 1153.3 kg for Ti-fitting/Kapton-5**. Changing tube wall requires recalculating section properties, local buckling, Perry, joints, film, sag and lift. A tube-wall change alone does not repair a film failure.

The coating does not guarantee shear SF above one: the filed cold-night assembly case is 0.9174. Hexcel's 35 psi W value is typical; its 25 psi minimum-average column would make that screen **0.655302**. The upstream 10 MPa scarf strength remains a projection. The owner's separate 0.980406 same-sign scarf/thermal interaction is also below unity and must not be hidden by the seven-screen minimum.

[NFI.json](NFI.json) assigns each open objection a proposed fix. The check uses 022c as the owner did; 022d subsequently filed and is the geometry to carry into a new calculation. The check is complete, with **{V['passed']}/{V['total']} numerical and integrity checks passing**, {V['source_pins_checked']} source pins, and explicit unresolved model inputs. No owner code or other seat was changed. One report closes this check; no successor is named.
"""
(ROOT / "CARD.md").write_text(card)

method = """# Independent calculation method

Only pinned JSON values, prose formulas and primary-source content are used. Owner executable bytes are hashed for integrity but are never decoded, imported or run. `prepare_inputs.py` captures the evidence; `check.py` recomputes all specified algebra and records coverage; `thermal_comparison.py` solves an explicitly separate thermal problem; `validate.py` checks pins, coverage, conservation, convergence and an independently posed plate boundary problem.

AUDIT contains one row for each numeric leaf in the owner's RESULTS.json and selected labels. MATCH means the arithmetic reproduces under its stated or explicitly recovered assumptions. It does not endorse physical validity. DECLARED_INPUT identifies assumed values. UNRESOLVED means necessary inputs are missing; no guessed value is presented as the answer. MISMATCH means a numeric disagreement with the inherited geometry/material calculation. RECONSTRUCTION_MISMATCH distinguishes a filed polynomial from a possibly different unprovided raw field. DISCRETIZATION_DIFFERENCE distinguishes analytic extrema from a small finite-grid difference. CORRECTIONS separates definite source/text fixes from conditional model differences.

Comparisons use relative tolerance 1e-8 and absolute tolerance 1e-9 in the field's SI units. This admits the upstream prose rounding without masking arc-length or density changes. Exact filed/check numbers and deltas remain in CSV and JSON.

**P2 algebra.** Let h=tf+tc and pressure face stress s=pR/(4tf). At the fixed 028b geometry, sigma0=E h/[R sqrt(1-nu²)], crimp=h²Gc/(2tf tc), Vc=sigma0/crimp and Kc=1-Vc/4 below Vc=2, otherwise 1/Vc. Full gamma=.2+.4 min(Vc,2). Global capacity is gamma Kc sigma0. Face capacity is 379.2 MPa; the separate tensile-proxy factor uses 345 MPa. Wrinkling is b*.82*sqrt(E Ec tf/tc), where b³+b=1. Dimpling is E(tf/cell)²/(1-nu²). Scarf equivalent face capacity is 10 MPa*901/30. Core crushing divides the typical crush value by p/2. These reproduce the upstream seven numerical screens, not unquantified assembly modes.

Full capacities use 293.6 GPa and nu=.0752; thermal stress and today's baseline use 290 GPa, as explicitly distinguished upstream. Thermal additions reduce the face, crimp, wrinkle and dimple factors in the owner's scalar scheme. Global and scarf use pressure-only stress; core crush uses pressure/2. This reproduces the table without silently assuming that thermal stresses have no possible effect on the real global or joint response.

Gradient coefficient is E alpha/[2(1-nu)]. Conduction-only core k=130*rho_core/2640 and U=k/tc. Shear lag uses lambda=sqrt(Gc/(E tf tc)) and tau=(alpha_Al-alpha_Be) DeltaT E tf lambda. Day rise uses outer subsolar temperature minus 284.9 K; swing uses the supplied day-night range. These are prescribed differential-strain screens. A real bonded cellular core needs effective in-plane stiffness/CTE, finite transfer length, boundary conditions and stress-free assembly temperature.

For the filed Legendre coefficients, construct Trest(mu)=sum(n=2..6) an Pn(mu), with mu=cos(phi). Find all real stationary roots inside [-1,1] and include both endpoints. The angular second derivative is (1-mu²)Trest''-mu Trest'. The declared curvature is -alpha/R times that derivative. Its absolute maximum is found by a second polynomial stationary-root search. The scalar face-bending screen is E(tf+tc)max|kappa|/[2(1-nu²)]. This is algebra on the specified reconstruction, not a solution of coupled shell equilibrium.

**Declared thermal alternative.** The day flux on the outer face is alpha*S*max(mu,0). Each point satisfies

    0 = solar - h(To-Ta) - epsilon_o sigma(To^4-Tenv^4) - U(To-Ti)
    0 = U(To-Ti) - epsilon_i (sigma Ti^4-B)
    B = area_mean(sigma Ti^4)

The last identity follows for a closed diffuse-gray spherical cavity with spatially constant inner emissivity; the cavity redistributes heat and has zero net source. Tenv^4=.5*Tsky^4+.5*Tground^4, Tground=Ta. Inner epsilon=.2. Night has no solar input, common To=Ti, and the same environment with Tsky=260 K. Day Tsky=275 K; Ta=284.9 K. Outer pairs are .2/.9 coated and .4/.05 bare. h is prescribed at .5,2,5,10 W/m²K, not claimed as a valid Whitaker prediction.

The nonlinear equations use an analytic Jacobian. Surface-area integration uses Gauss-Legendre quadrature in mu, split at the solar terminator; 64 and 128 total points converge to sub-nanokelvin differences for the reported endpoints. The split prevents the illumination kink from contaminating quadrature convergence. Pole values are separately solved using the converged cavity radiosity. Tests enforce local residuals, external energy conservation, zero net cavity radiation, and zero n>0 coefficients for a constant field. In-plane face conduction, thermal contact resistance and cell-to-cell/cross-cell radiation are omitted projections. Interior gas convection is absent. No temperature dependence or property validity at the hottest sensitivity points is claimed.

**P3 algebra.** For every upstream cap row, A=pi(ro²-ri²), I=pi(ro⁴-ri⁴)/4, ri=ro-tw, arc length l=2R asin(s/(2R)), member count=24piR²/(sqrt(3)s²), and N=pRs/(2sqrt(3)). All tubes have E=410 GPa and density=3100 kg/m³. Tube mass is count*rho*A*l; the owner's chord-based masses use s in place of l. Film mass is 4piR²*t*rho_film.

Axial stress=N/A. Euler stress=pi² E I/(A l²). Local stress=.6 E(tw/ro)gamma, gamma=1-.901[1-exp(-sqrt(ro/tw)/16)]. Perry uses eta=(l/1000)ro/(I/A), B=Fc+(1+eta)sigmaE and its numerically stable lower root 2Fc sigmaE/[B+sqrt(B²-4Fc sigmaE)]. The inherited Mylar branch uses Fc=380 MPa flexural proxy; the other rows use 3.9 GPa compression. Global pressure=.2*4sqrt(1.5) E sqrt(IA)/(sR²). Film stress=ps/(2t), with inherited film strengths. The declared half-wave expression uses pi sqrt(.75 R sqrt((ro²+ri²)/2)); that inner square root is a polar radius, not sqrt(I/A). Its source convention is retained for replication rather than silently changed.

Mechanical film strain is alpha_frame(Ttube-Ta)-alpha_film(Tfilm-Ta); delta_sigma=Efilm*strain/(1-nu_film); delta_N=delta_sigma*t*s/sqrt(3). Reproduction recovers the otherwise unstated film nu values .33/.38/.34/.30 for projection/Mylar/Kapton/Zylon. It is conditional on the supplied temperatures and the isotropic/stiff-frame assumption. The corrected comparison uses SiC CTE everywhere, holding temperatures fixed so it does not pretend to repair the heat model. Capacity factors divide by 1+q/p+delta_N/N, or 1+q/p+delta_sigma/sigma for film. These scalar load multipliers do not establish compatibility or full load redistribution.

**Wind.** Dynamic pressure is rho V²/2, drag=.47 q piR², and 016 mooring adds a factor 1.4. Reproduction uses the owner's rounded .514444 m/s per knot; exact 1852/3600 conversions are also retained. The gust increment at selected VB is rho VB U+rho U²/2. The selected steady-plus-gust case adds rho VB²/2. Averaging potential Cp=1-2.25sin²(theta) over sphere area gives -0.5; that average is not an eigenvalue comparison theorem. EAS/TAS selection, transient response, nonuniform pressure and hardpoint reactions remain separate.

**Pads.** The recovered log-only formula and its inferred inputs are identified in CARD. The proposed simply-supported alternative specifies a uniform patch of radius b and force F at the center of a plate of radius a. Inside the patch, w=q r^4/(64D)+c1 r²+c0; outside, w=F r² ln(r)/(8piD)+B r²+C ln(r)+d0. Continuity of displacement, slope and moments, the known shear resultant, w(a)=0 and Mr(a)=0 give

    Mcenter = F/(4pi) [(1+nu)ln(a/b)+1-(1-nu)b²/(4a²)]
    sigma_center = 6 Mcenter/t²

An independent numerical boundary-condition solve validates this expression at five radius ratios, including a=b. The latter reduces to the uniformly loaded simply-supported disk result. The alternative enforces a>=b and the same 1 mm thickness floor. A separate preload sensitivity sizes bearing area with crush-p/2 instead of crush. Neither solves a plate on an elastic foundation or a tensile/oblique mooring attachment.

The proportional mass correction is explicitly a sensitivity. It is not accepted as a re-sized solution: section properties, local buckling, Perry, global response, film, joint and reserve constraints must be re-evaluated after a geometry change. Existing fixed reserve is not converted to free payload or a single physical point load.
"""
(ROOT / "METHOD.md").write_text(method)

sources = """# Source and tag audit

**FAA.** [FAA-P-8110-2 with incorporated changes](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/airships/aceAirshipDesignCriteria.pdf) was downloaded and pinned as `sources/faa-airship.pdf`. It is scanned; the blank text extraction is not treated as evidence. PDF pages 24,27,35,139,140 were rendered and visually read, corresponding to printed pp12,15,23,121,122. The precise source corrections and selected-load arithmetic are in CARD/CORRECTIONS. In particular, the appendix resolves the historical mooring change. The source does not establish a vacuum-sphere buckling solution.

**Beryllium.** The pinned [Materion SR-200 sheet](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6) directly lists typical E=290 GPa, density=1.85 g/cm³ and thermal expansion=11.3 ppm/K over 25–100 C. It identifies 345 MPa as minimum tensile yield. Thus the thermal expansion need not be attributed solely to S-200-F as 037 does. It remains a typical value, not a matched formed-sheet coupon. [NASA CR-194164](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf), Tables 2–3, supports the historical orthotropic SR-200 constants and 379.2 MPa compression lot value. The isotropic nu=.0752 surrogate, full gamma/wrinkle assumptions and gauge/lot transfers remain conditional. Both source PDFs and upstream text extractions are pinned.

**Honeycomb.** [Hexcel CR III Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf), 5056 3/8-1.0, supports nominal 1 pcf density, typical compression modulus 15 ksi, typical crush 35 psi, W shear modulus 6.8 ksi and W shear strength 35 psi typical / 25 psi minimum average. These convert to 16.018463 kg/m³, 103.421359 MPa, 241.316505 kPa, 46.884350 MPa and 241.316505/172.368932 kPa. The data note a 0.625-inch test thickness. They do not provide a bonded-Be interfacial allowable or thermal-cycle qualification. The web tool read the official PDF; a direct local download returned HTTP 403, so no local PDF pin is claimed.

**Convection.** [Ansys's Whitaker implementation documentation](https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/dem_cfd_coupling/sec-fluidHeatTransfer.html) explicitly requires flow and viscosity inputs and lists a Reynolds-number range of 3.5–76000, with additional Prandtl/viscosity-ratio limits. For the filed 20 m diameter, 500 m density and viscosity, the upper Reynolds limit corresponds to only 0.05827 m/s. An unspecified sphere heat-transfer speed cannot be checked; ordinary flight speeds would be outside that documented range. The proposed thermal comparison uses prescribed h and does not claim to validate this correlation.

**Other material/assembly values.** SiC tube identity and capacity inputs come from the pinned 022c JSON and are independently checked by geometry/section identities; 034 independently states that the Ti/CFRP names denote fittings. The 022c film strengths are inherited screens. The additional film elastic moduli, CTEs and recovered Poisson ratios are not demonstrated laminate constitutive data. Zylon fiber properties do not by themselves define a sealed 0/90 film. Bare-Be optical values, coated optical durability, Al thermal conductivity/CTE transfer, the 10 MPa Be scarf value, stress-free assembly temperature and pad properties remain QUESTIONABLE or PROJECTION. The recovered 276 MPa pad yield and geometric parameters are numerical inferences, not source-verified specifications.

The 022c choice was valid at the owner's filing time; the later 022d geometry is recorded in the pinned previous check's P3-LATEST.md for carry. This audit does not silently substitute that different geometry into the filed 037 numbers.
"""
(ROOT / "SOURCE-AUDIT.md").write_text(sources)

issues = [
    ("HEAT-INPUTS", "QUESTIONABLE", "84 thermal/projection fields are not independently recoverable from supplied inputs.",
     "Publish velocities, all optical properties, sky/ground/cavity boundary conditions, grid, weights, converged day/night profiles and residuals; rerun both P2 and P3. The declared P2 comparison supplies a reproducible starting model."),
    ("PATTERN-DEFINITION", "QUESTIONABLE", "Filed residual maxima do not equal extrema of the filed n=2..6 polynomial.",
     "State whether maxima use raw or truncated temperatures; retain raw samples, area weights and projection coefficients; use analytic extrema and constant/linear-mode consistency checks."),
    ("SHELL-EQUILIBRIUM", "PROJECTION", "The scalar bending estimate and a membrane-free kinematic trial do not establish full spherical-shell equilibrium.",
     "Solve both curvature components, membrane/bending coupling and force/moment equilibrium with compatible thermal strains and core restraint; compare with the rough gradient screen."),
    ("P3-TUBE-IDENTITY", "QUESTIONABLE", "Ti/CFRP fittings were treated as tube materials in thermal CTE and mass while SiC capacities were retained.",
     "Use SiC properties for all tubes, keep fittings separate, and rerun temperatures plus compatibility. Corrected fixed-temperature sensitivities are already tabulated."),
    ("P3-ARC-MASS", "QUESTIONABLE", "Every filed tube mass uses chord length; inherited capacities use arcs.",
     "Charge each SiC tube's inherited arc length. Eight unique corrected masses and ten exact result mismatches are supplied."),
    ("STEADY-FLIGHT-LOAD", "PROJECTION", "The 290.634 Pa flight addition omits the selected VB baseline.",
     "For the same selected local-speed case add 189.214 Pa steady pressure; total 479.848 Pa gives conditional P2 least 1.001324769. Select EAS/TAS and dynamic-response treatment consistently."),
    ("WIND-PATCH", "PROJECTION", "Negative mean Cp is not proof that uniform excess bounds a nonuniform buckling mode.",
     "Compute the prestressed nonuniform pressure and hardpoint equilibrium, then compare instability/imperfection response; retain uniform excess as a screening assumption until shown."),
    ("PAD-SUPPORT", "PROJECTION", "The filed thickness reproduces only a logarithmic term; support and boss-loading conditions are unspecified.",
     "Select edge support versus elastic foundation and finite boss loading. The supplied simply-supported uniform-patch solution includes the nonlogarithmic term and has independent boundary-condition checks."),
    ("PAD-BOSS-FIT", "PROJECTION", "Under recovered 25 mm boss-radius assumptions the systems pad radius is only 14.683 mm.",
     "Define whether 25 mm is radius or diameter; enforce boss containment. The supplied 25 mm radius floor changes six-pad mass to 0.031809 kg before installation."),
    ("PAD-PRELOAD-LOADPATH", "PROJECTION", "Load-only F/crush sizing omits possible existing p/2 compression and does not address pull/oblique mooring transfer.",
     "Determine actual reaction direction and superpose compatible pressure loads; use available compression headroom when applicable, then check face bending, core shear, peel, local shell failure and hardware."),
    ("P3-HARDPOINTS", "PROJECTION", "7/2/1 member counts are scalar 5% sharing counts, without a vector load path or mass.",
     "Place attachment nodes and members, solve equilibrium and joint loads, size fittings/spreaders and weigh their mass into the same lift budget."),
    ("RESERVE-POINT-LOAD", "QUESTIONABLE", "The 411.299 kg reserve contains environmental lift losses and distributed masses, not one suspended payload.",
     "Use the actual payload and equipment layout; label the 4.033 kN example as hypothetical. Do not convert buoyancy penalties into concentrated hardware weight."),
    ("RESTORATION", "PROJECTION", "Multiplying a tube mass by reciprocal least SF is not a demonstrated structural restoration and cannot repair a separate film failure.",
     "Recompute changed sections, Euler/local/Perry/global modes, film, fittings, sag and lift. Use the supplied corrected proportional masses only as sensitivities."),
    ("SHEAR-ALLOWABLE", "QUESTIONABLE", "The 241.317 kPa W value is typical core shear, not a bonded-interface or cyclic allowable; the minimum-average column is 172.369 kPa.",
     "Choose the intended material statistic, stress-free bond temperature, finite transfer geometry and interface properties. The nominal thermal-change limits are 27.975 K typical and 19.982 K minimum-average in this screen."),
    ("CORE-CTE-LAG", "PROJECTION", "Prescribed Al-versus-Be strain in an equivalent shear-lag formula does not include effective cellular in-plane stiffness or finite boundary conditions.",
     "Model both adherends/core compatibility and effective thermal expansion, then compare with representative measured thermal-cycle shear and peel."),
    ("CONVECTION-OPTICS", "QUESTIONABLE", "No speed or validity check is provided for Whitaker; bare optics and coating durability are assumptions.",
     "Select climate and flight/ground thermal cases, validate the applicable convection regime, and retain measured or explicitly assumed surface optics and their temperature dependence."),
    ("FILM-CONSTITUTIVE", "PROJECTION", "Film nu is unstated, the frame is assumed rigid, and an isotropic law is applied even to the Zylon reinforcement case.",
     "Provide membrane/laminate stiffness and CTE tensors, prestress and slip/bond conditions; solve frame-film compatibility with both directions and barrier mass."),
    ("NONUNIFORM-BOW", "PROJECTION", "Saying uniform mismatch does not bow a member does not evaluate circumferential tube heating, asymmetric film traction or thermal imperfections.",
     "Calculate thermal curvature and load eccentricity for actual tube and attachment temperatures and add the resulting imperfection to the member stability calculation."),
    ("COMPLETE-MODE-ACCOUNT", "PROJECTION", "The seven-screen minimum omits unresolved assembly modes; the filed coated swing is 0.917 and a separate scalar scarf interaction is 0.980.",
     "Maintain a complete mode/load-case ledger, distinguish day-rise from night-reference assembly and map core thermal shear to scarf/bond stresses before combining them. Do not present seven-screen unity as installed-hull unity."),
    ("CURRENT-GEOMETRY", "QUESTIONABLE", "037 used 022c before 022d filed; several quoted high P3 factors are outside the half-wave band.",
     "Carry the now-filed 022d in-band geometry into the next thermal/load calculation, charging both film plies and fittings. Keep this audit tied to the original 022c record.")
]
nfi = {"unit": "vacuum-mainline037-check-1020", "status": "Check complete; no work blocked",
       "rows": [{"id": "NFI-CHECK037-" + key, "tag": tag, "status": "open",
                 "finding": finding, "proposed_fix": fix}
                for key, tag, finding, fix in issues],
       "resolved_source_findings": [
           "FAA 78-to-70-knot history is resolved by Appendix B, not a remaining document conflict.",
           "FAA VB lower bound includes the 0.65 VH alternative; design airspeeds are EAS.",
           "The SR-200 manufacturer's own sheet supports typical 11.3 ppm/K thermal expansion."
       ]}
(ROOT / "NFI.json").write_text(json.dumps(nfi, indent=2) + "\n")
print(json.dumps({"card_words": len(card.split()), "NFI_rows": len(issues),
                  "validation_passed": V["passed"], "rendered_at": now}))
