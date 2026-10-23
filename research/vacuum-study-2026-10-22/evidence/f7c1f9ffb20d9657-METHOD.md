# MAINLINE-031 calculation method

ESTIMATE. QUESTIONABLE material/model transfers and PROJECTION atmosphere/fabrication. This is a uniform-pressure structural screen, not certification.

**Atmosphere and equilibrium.** R=10m, sphere volume 4188.790204786391m³, area 1256.6370614359173m², p₀=95460.83791390515Pa, T₀=284.9K, nominal gross displaced mass L₀=4889.442150186961kg. The reference is 500 geopotential metres. Geometric height is zRₑ/(Rₑ−z), Rₑ=6356660m; the difference is small here but actual terrain clearance needs geometric coordinates. The −6.5K/km lapse and altitude convention follow the standard-atmosphere definition, not a claim that hot days follow a measured standard profile. [NASA Appendix A](https://ntrs.nasa.gov/api/citations/20050207438/downloads/20050207438.pdf)

The moist-air density relation is ρ=(p−0.378e)/(R_d T). This is the ideal-mixture/virtual-temperature approximation used in the inherited climate ledger. [NWS virtual-temperature formula](https://www.weather.gov/media/epz/wxcalc/densityAltitude.pdf)

For each weather day, anchor p_d, T_d, e_d at 500m and impose constant e/p with height. Define k=1−0.378e_d/p_d, a=0.0065K/m, n=gk/(R_d a), R_d=287.053J/(kg K), g=9.80665m/s². Integration of hydrostatic balance gives:

```
T(z) = T_d − a(z−500)
p(z) = p_d [T(z)/T_d]^n
ρ(z) = k p(z)/(R_d T(z))
T_float = T_d [(M/V_eff)/ρ_d]^[1/(n−1)]
z_float = 500 + (T_d−T_float)/a
```

This integration is our calculation from hydrostatic balance; the profile choice is an explicit assumption. [NWS hydrostatic and hypsometric equations](https://www.weather.gov/source/zhu/ZHU_Training_Page/Miscellaneous/Heights_Thicknesses/thickness_temperature.htm)

Optimistic hot days use ΔT=10K, p_d/p₀=0.99 or 1.01, e_d=0 or 1000Pa. Conservative hot days use ΔT=25.1K, p_d/p₀=0.98 or 1.02, e_d=0 or 6000Pa. Also score ISA, heat-only and pressure-only days. These are 15 diagnostic days, with the hot-low-wet corner governing pressure and minimum height for the scored mass range. Cold +6000Pa states are excluded as supersaturated at the anchor. The two envelope sets retain the same optimistic nonclimate vehicle inventory.

Sensitivity profiles are (i) isothermal with constant e/p and (ii) the same lapse with constant e. In case (ii), p(z)=0.378e+(p_d−0.378e)[T(z)/T_d]^[g/(R_d a)]. None is established by the single-level 019 inputs. Supersaturated roots are flagged, not silently clipped.

**Definition of the least split.** C≥0 is absent climate mass relative to L_eff=L₀V_eff/V₀. M=L_eff−C. Positive C is not ballast and cannot be removed from a fixed hull by deleting a label. All calculated heights are passive free equilibria, with no tether or thrust.

For a specified centre-altitude floor z_min:

```
C_floor = max(0, L_eff − V_eff min_day ρ_day(z_min))
q_float(C) = max_day p_day(z_float(C))/p₀
q_required(C) = max(1, q_float(C))
nominal SF reserve = q_required − 1
```

The q≥1 constraint preserves the inherited p₀ structural requirement even when every free-float pressure is below p₀. Every inherited mode is a fixed pressure capacity divided by actual pressure; at fixed geometry, SF_i(z)=SF_i(p₀)p₀/p(z). A geometry is accepted only if all modes meet q_required at p₀ and all relevant float roots satisfy the specified floor. C_floor is an exact lower bound on mass headroom for this profile and displaced volume. Feasible reoptimised points attain it. With no altitude floor C=0 is the mathematical minimum; below-ground roots prevent interpreting it as an aircraft requirement.

The objective is lexicographic: minimum C for the stated floor; then fewest named additional optimisms; then smallest maximum logarithmic usage. Kg and SF are different quantities and have no unique combined minimum without an objective. A separate matched-property calculation reports the hardware mass needed at q_required minus that needed at p₀, reoptimising both geometries. It is an isolated mass-equivalent pressure cost, not an additional debit to the already closed mass budget and not a promise of payload at the same free-float altitude.

**P2 mass and capacities.** The 179.55812764546135kg nonclimate reserve is 125.66370614359174kg retained water, 5kg contamination and 48.89442150186961kg internal gas. Systems remain 100kg. Original optimistic climate is 213.036426543752kg temperature/pressure plus 18.704389882434043kg humidity.

With S the faces-plus-core mass, f the core mass fraction, ρ_f=1850kg/m³:

```
t_f = (1−f) S/(2 A ρ_f);  t_c = f S/(A ρ_c)
m_seam = (2A/w)[2b t_f ρ_f + 2b t_adh ρ_adh + t_c w_splice ρ_splice]
m_film = 2 A μ
m_joint = max(0.05 S, m_seam + m_film)
L₀ = C + 100 + 179.55812764546135 + S + m_joint
reserve = C + 179.55812764546135 + max(0,m_joint−0.05S)
```

Use 019 b=0.06m, t_adh=0.0002m, ρ_adh=1250kg/m³, w_splice=0.0015m, ρ_splice=1100kg/m³. Convert film lb/ft² using 0.45359237/0.09290304. The seam equation is linear in S at fixed f,w; the program solves both joint-floor branches algebraically. The unused system allowance remains reserved.

For h=t_c+t_f, ν=0.33:

```
σ₀ = E h/[R sqrt(1−ν²)]
σ_crimp = h² G_c/(2 t_f t_c)
V_c = σ₀/σ_crimp
K_c = 1−V_c/4 (V_c≤2), otherwise 1/V_c
σ_membrane = pR/(4t_f)
SF_global = γ K_c σ₀/σ_membrane
SF_face = σ_allow/σ_membrane
SF_crimp = σ_crimp/σ_membrane
SF_crush = 2 σ_core_crush/p
SF_wrinkle = b_x k_wr sqrt(E E_c t_f/t_c)/σ_membrane
SF_dimple = E/(1−ν²) [source link unavailable in this public projection]²/σ_membrane
b_x³+b_x=1
```

These preserve 021b's six equations and biaxial dimpling. ν and property transfers remain conditional. No additional joint-efficiency factor or joint strength mode is invented; those are open evidence needs.

The five named axes are γ: handbook 0.2 below V_c=2 and 1 at/above 2 → 0.2+0.4min(V_c,2); wrinkle 0.33→0.82; compression transfer 345→379.2MPa; panel seam-equivalent width 0.9144→4m; film 0.03→0.015lb/ft². For an allowed axis, x(u)=x_today(x_full/x_today)^u. E stays 290GPa in the least-set search, as in 021b; a full-grade E293.6GPa case is separate. Unneeded wrinkle/strength/gamma usage is reduced in the reported needed-values column without changing geometry. The constructed max-usage point and its complete SF vector remain in JSON.

All 47 eligible 021b honeycombs are searched. At a given subset and u, favourable panel/film bounds maximise available structural mass; all capacities are nondecreasing with that mass over the inherited branches. Search every subset through the first feasible cardinality; bisect u and optimise f, explicitly checking both sides of V_c=2. Lower-cardinality exclusions use a 32769-point/core verification; winning points use 131073 points/core plus local refinement.

021 rev1's original 5% margin is not a weather line. Fixed-hull rows show the unfilled margin, then add the same 019 nonclimate inventory. Its reconstructed optimisation retains only 5% joints and 100kg systems, uses 283→379.2MPa strength and the same gamma/wrinkle axes. This is an incomplete joint-budget comparator, not a replacement for 021b.

**P3.** Use the filed 022b equilateral, percent-joint 019 point, not the superseded 022 force model. Let n_v=8πR²/(√3s²)+2, n_e=3n_v−6, arc length ℓ=2R asin(s/(2R)), member force N=pRs/(2√3) (FIX-A). The 022b film sag reduces V_eff=V₀[1−s/(16R)] at every altitude. It is lost displacement, not carried mass. C scales with this volume for a fixed density/altitude requirement.

Tube material is the carried SiC E410GPa, density3100kg/m³, compression3900MPa. Projection film is 1.5GPa, 970kg/m³, minimum80µm. With each node20g and joints 5% of film+nodes+tubes, close M=L_eff−C=100+B+1.05(m_tube+m_node+m_film). Actual section area and inertia use exact annulus geometry.

```
SF_yield = σ_allow A_t/N
SF_Euler = π² E I/(ℓ² N)
γ_local = 1−0.901[1−exp(−sqrt(r_o/t_w)/16)]             (FIX-B)
SF_local = 0.6 E (t_w/r_o) γ_local A_t/N
SF_film = 2 σ_film t_film/(s p)
η = (ℓ/1000)r_o/(I/A_t)
σ_E = π² E(I/A_t)/ℓ²
φ = [σ_allow+(1+η)σ_E]/2
σ_Perry = φ−sqrt(φ²−σ_allow σ_E)
SF_Perry = σ_Perry A_t/N
SF_global = 0.2 × 4sqrt(1.5) E sqrt(I A_t)/(s R² p)
```

The local knockdown comes from straight isotropic cylinders; its curved-ceramic transfer remains QUESTIONABLE. [NASA SP-8007](https://ntrs.nasa.gov/api/citations/19690013955/downloads/19690013955.pdf)

Reoptimise s∈[0.4,8]m, r_o≤min(0.25m,s/3), film thickness ≥80µm; the resulting optima lie away from the upper spacing/radius bounds. Two independent differential-evolution seeds and a 3.11-million-point grid per scored case check the maxima. A separate Ti/Kapton sensitivity keeps 022b's SiC value and sizes Ti joint mass at the peak pressure: 2n_e C_end N_peak²/r_o, C_end=2.950e−14kg·m/N². Its film is 115.5MPa and 1420kg/m³, minimum25µm. Other 022b folded points are held-geometry comparisons only.

**Numerical scope.** Decimal scalar calculations independently reconstruct mass and pressure capacities from saved geometry. Direct integration of dp/dz checks analytic float roots. Every source artifact hash is checked. These checks validate arithmetic and search resolution, not the physical assumptions or a completed vehicle.
