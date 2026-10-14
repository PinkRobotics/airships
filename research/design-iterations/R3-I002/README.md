# R3-I002 — pressure relief, geometry and lifting-gas branch

> Not shown; 70.575 m He-assisted sphere +79.0 t assumed; confidence UNKNOWN; governing uncertainty: assembled lattice/boundary buckling.

Status: **internal, conditional design hypotheses**, 2026-10-14. No aircraft has
been built or flown. Positive arithmetic below is not a qualified floating
vehicle, a safety margin established by test, or clearance for a new public
scientific claim. All candidate budgets include assumed all-up allowances;
their actual sufficiency is UNKNOWN.

**Decision:** reject partial evacuation with residual air as the next rescue of
this lattice. At equal volume, 80% pressure reduction gives a worse balance than
99%, under every compared knockdown. Changing the capsule to a sphere saves
about one tonne. Enlarging the air-filled vacuum candidate to a 112 m sphere
leaves −100.303 t at the reference local-wall factor; its favourable +34.143 t
depends on simultaneous unverified stiffness, compression and joint assumptions.

The next ranked change was evaluated in the same paper iteration: replace the
retained air with helium at 80% ambient absolute pressure in the smaller sphere.
That branch has +79.011 t conditional margin even at local-wall factor 0.20,
including 24.565 t of helium and 20 t of equipment/payload allowances. This is
helium-assisted buoyancy, not evidence that pressure relief alone rescued vacuum
lift. The identical air-filled control is −74.192 t. A 1 mm minimum tube wall
at unchanged radii changes D to −2.786 t. Physical acceptance stays
UNKNOWN. A conventional, nearly ambient-pressure helium envelope is the next
comparison; a vacuum lattice must justify its extra mass against that control.

## Starting point and scope

Source revision: `afb2c2d1726b9d9a805f9781085c3dd6a52913e5`.
The [drawn-hull ledger](../../analysis/float-ledger.json) records a 52 m × 104 m
capsule at 403.1 t against 224.8 t sea-level lift, with structural factor 1.2,
its own skin sag and its own T700-based member layout. That is historical
context, not an all-up aircraft. The older 112 m bound has undrawn stiffness
credits and is not reused here.

This iteration instead prices the complete volume of a first-level, hollow-tube
octet lattice using the algebra in
[vacuum-cell.py](../../analysis/vacuum-cell.py), `arch_tube_strut`, and its
[limitations](../../analysis/vacuum-cell.md). There are no diametral/chordal-net
credits, unpriced shear skins or hierarchical tube walls. Therefore a difference
from the 403.1 t recorded hull cannot be attributed to geometry or pressure
alone. The controlled baseline and changes below use one architecture and one
set of atmosphere/material assumptions.

No native solver, CFD, FEA, historical simulation replay or physical attempt was
made. One paper design iteration was evaluated with one-process scalar
arithmetic. PASS of an arithmetic/check command is not scientific acceptance.
There were zero native-solver/physical attempts and zero control stops.

## Candidate construction and frozen assumptions

- **A, baseline:** unloaded capsule diameter 52 m, straight length 52 m, two
  hemispherical ends; overall length 104 m. Volume 184,055.442 m³; area
  16,989.733 m². First-level, volume-filling octet lattice, 2 m pinned struts.
- **B, geometry change:** sphere diameter 70.574858 m, same unloaded volume;
  area 15,647.678 m², 7.899% less. Both A and B are compared at both pressures.
- **C, scale change after pressure relief failed:** sphere diameter 112 m,
  same struts, material and allowances per unit volume/area; equipment remains
  an explicitly assumed fixed 20 t. This is a filled sphere, not the old
  112 m capsule or its 2,249.8 t lift row.
- **D, lifting-gas change:** B at 20% pressure reduction with helium, together
  with an otherwise identical air-filled control. It changes gas species
  explicitly; it is a separate branch after the air-only comparison.

All candidates use an open interior plenum. Hollow struts are vented to it, so
their walls do not separately sustain the hull pressure differential. There
are no pressure-rated interior partitions; one breach is not contained to a
cell. A film skin transmits the external differential to boundary members and
then to the bulk lattice. Spherical symmetry does not establish that the
boundary connections or complete assembly are stable.

| Input | Value and scope |
|---|---|
| Atmosphere | 101,325 Pa, 288.15 K, dry-air gas constant 287.05 J/(kg K); density 1.225012266 kg/m³ |
| Pressure fraction `q` | `1 − p_inside/p_outside`; fraction of pressure removed, not a fraction of hull volume |
| Air cases | `q=0.99`: 1,013.25 Pa inside, 100,311.75 Pa differential; `q=0.80`: 20,265 Pa inside, 81,060 Pa differential |
| Helium branch | `q=0.20`: 81,060 Pa inside, 20,265 Pa differential; gas at ambient temperature |
| Material | M60J-class epoxy composite; density 1,658 kg/m³ and UD modulus 354 GPa retained as mixture estimates |
| Effective stiffness | `354 GPa × 0.75^0.75 × 0.25^0.25 = 201.736 GPa`, the existing orthotropic surrogate, used consistently for both local and Euler sizing |
| Compression ceiling | 790 MPa favourable proxy, not an allowable for the cross-ply tube; 592.5 MPa sensitivity |
| Structural factor | 1.5 on pressure-derived member demand, including compression; independent film factor below |
| Local-wall factor `gamma` | 0.20 conservative sensitivity, 0.30 reference assumption, 0.65 favourable sensitivity; all unqualified for these tubes |
| Nodes/joints | 15% of member mass; 30% sensitivity; no separate joint-efficiency debit is also added |
| Film | Preformed inward domes over 2 m spans, cap rise/radius 0.25; assumed fibre strength 5.8 GPa, density 1,560 kg/m³, factor 4 and efficiency 0.5 |
| Added barrier/seams | 0.05 kg/m² of unloaded hull area, independent of the load-bearing film |
| Boundary transitions | 0.30 kg/m², for extra rim members, braces, clamps and film attachment beyond bulk struts/nodes; assumed mass, not stiffness credit |
| Additional all-up items | 20 t placeholder below, separate from hull, joints, film and gas |

The [Toray M60J sheet](https://www.toraycma.com/wp-content/uploads/M60J-Data-Sheet.pdf),
page 1, gives 790 MPa compression for a 60% fibre-volume composite; it also gives
360 GPa tensile modulus. We retain the model's 354 GPa estimate for a controlled
comparison. Its coupon properties do not qualify the proposed cross-ply tubes;
page 2 identifies the data as reference lot averages. Simultaneously obtaining
the stiffness surrogate and 790 MPa compression is particularly doubtful.

[NASA SP-8007 Rev. 2](https://ntrs.nasa.gov/citations/20205011530), printed page 25,
warns about long-cylinder buckling and shell/column interaction, and cautions
that the cited empirical correlation lacks verification above length/radius 5.
Our struts are far outside that range. `gamma=0.65` is a sensitivity, not a NASA
qualification. No whole-hull instability factor has been established.

## Calculation and accounting

All mass comparisons are in tonnes, using mass-equivalent buoyancy; multiply
both sides by gravity for force. `rho_air × V_loaded` is gross displaced-air
lift, counted once. Subtract residual gas once with the other component masses.
Do not also apply a separate `q` multiplier to gross lift in the budget table.

For strut solid fraction `phi`, radius/length `lambda`, and wall/radius `psi`:

```text
C = 6 sqrt(2) pi
kl = 0.605 gamma; a = 2 kl / pi²; c = 2 C a; k = kl / (3 sqrt(c))
phi_b = [SF q P / (k E_eff)]^(2/3)         # co-critical Euler/local-wall branch
phi_c = 3 SF q P / sigma_compression       # constituent compression floor
phi = max(phi_b, phi_c)
psi = sqrt(phi/c); lambda = sqrt(a psi)
r = 2 m × lambda; t = r psi
sigma_demand = 3 SF q P / phi
sigma_Euler = pi² E_eff lambda² / 2
sigma_local = kl E_eff psi
```

Here `r` is the tube mid-surface radius. The thin-wall expression uses
`A_tube = 2 pi r t`; the exact hollow-section Euler stress is larger than the
thin-wall value by `1 + psi²/4`. No end-fixity enhancement is credited. Continuous
lattice counts approximate a finite manufactured hull; boundary trimming,
joint stiffness and unequal member loads remain unresolved.

Loaded shape loses volume through ideal affine compression and film sag:

```text
epsilon = 3 q P / (phi E_eff)             # actual pressure, without sizing SF
V_loaded = V0 (1 − epsilon)^3 − 0.13 m × A0 (1 − epsilon)^2
M_members = rho_material phi V0
M_nodes = 0.15 M_members
M_gas = (1 − q) rho_air gas_ratio V_loaded
```

Using the full loaded volume for gas rather than subtracting composite solid
volume slightly overcharges gas. Film and boundary masses use the larger
unloaded area. These are small accounting conservatisms, not a bound on model
error. Joint compliance can reduce loaded volume further.

For the film, circular cap radius of curvature is 2.125 m; actual area/projected
area is 1.0625. The load-bearing film mass is
`1560 × q P × 2.125 / [2 × (5.8e9 / 4 × 0.5)] × 1.0625 × A0` kg.
The mean inward volume debit is assumed 0.13 m over the complete hull, slightly
above a circular 1 m radius, 0.25 m rise cap's 0.127604 m mean depth. A tiling
of those caps and its load-carrying attachment details have not been drawn;
the 0.30 kg/m² transition allowance must be replaced by a bill of materials.
Preforming is necessary: elastic stretching of a flat film is not credited.

The all-up placeholder is 2 t pumps/valves/pressure control, 3 t motors and
propulsors, 5 t energy/power equipment, 1 t avionics/cabling, 3 t equipment
hardpoints/suspension, 3 t ballast/landing/mooring provision and 3 t payload.
Every item is **assumed UNKNOWN**, not a purchased/weighed component or a lower
bound. Boundary film supports and bulk nodes are already charged elsewhere.
This is a static screening mission, not the site's P100 operating mission.
Emergency pressure controls, wind/flight loads, fatigue, leak compensation,
manufacturing minimum gauge and mission endurance are not qualified by it.

## Equal-volume air comparison

| Shape | q | Local-wall factor | Gross lift t | Total including gas/allowances t | Margin t |
|---|---:|---:|---:|---:|---:|
| capsule | 0.99 | 0.20 | 221.458 | 300.638 | -79.180 |
| capsule | 0.80 | 0.20 | 221.547 | 306.402 | -84.855 |
| sphere | 0.99 | 0.20 | 221.671 | 299.844 | -78.173 |
| sphere | 0.80 | 0.20 | 221.760 | 305.711 | -83.950 |
| capsule | 0.99 | 0.30 | 221.269 | 266.713 | -45.444 |
| capsule | 0.80 | 0.30 | 221.372 | 276.936 | -55.565 |
| sphere | 0.99 | 0.30 | 221.482 | 265.919 | -44.437 |
| sphere | 0.80 | 0.30 | 221.585 | 276.245 | -54.660 |
| capsule | 0.99 | 0.65 | 221.017 | 232.821 | -11.804 |
| capsule | 0.80 | 0.65 | 221.017 | 235.536 | -14.518 |
| sphere | 0.99 | 0.65 | 221.230 | 232.027 | -10.797 |
| sphere | 0.80 | 0.65 | 221.230 | 234.844 | -13.614 |

At `gamma=0.30`, sphere B improves baseline A by 1.007 t at `q=0.99`.
Changing B to `q=0.80` then loses 10.224 t: member and joint savings are smaller
than the extra residual-air mass. The same direction holds at 0.20 and 0.65.
This rejects the compared pressure-relief hypothesis under the frozen model.

There is a stronger limited result for the reference branch: full-pressure
member-plus-node density exceeds 1.225 kg/m³ even before skin and equipment.
The buckling contribution scales as `q^(2/3)`, which is at least `q` on
`0 < q <= 1`; air-only net gas displacement is proportional to `q`. Thus
partial evacuation cannot rescue that branch at any size within this model.
This is not an impossibility theorem for other materials or architectures.

## Same-iteration scale change and lifting-gas alternative

| C: 112 m sphere, q=0.99 | Sizing mode | Gross lift t | Total t | Margin t |
|---|---|---:|---:|---:|
| gamma=0.20 | buckling | 889.627 | 1124.762 | -235.136 |
| gamma=0.30 | buckling | 888.870 | 989.174 | -100.303 |
| gamma=0.65 | compression | 887.859 | 853.716 | +34.143 |

For C, an assumed factor 0.65 pushes sizing onto the 790 MPa compression floor.
Conditional break-even needs `gamma >= 0.42244` with the other defaults, or a
compression ceiling of at least 757.46 MPa when `gamma=0.65`. Those are separate
one-variable sensitivities, not jointly independent design requirements. At
the favourable inputs, diameter break-even is 85.490 m with fixed 20 t equipment.
At reference/conservative inputs, increasing size makes the shortfall worse.

D retains the smaller spherical geometry and changes the gas explicitly.
[NIST's helium molecular mass](https://webbook.nist.gov/cgi/cbook.cgi?Name=Helium)
is 4.002602 g/mol. The ideal-gas density ratio to this paper's air at equal
temperature/pressure is 0.13818655, using `R_universal=8.314462618 J/(mol K)`.
Helium inventory is charged as onboard mass; procurement, price and containment
performance remain UNKNOWN and no purchase is proposed by this calculation.

| D: 70.575 m helium-assisted sphere, q=0.20 | Gross lift t | Helium t | Total t | Margin t |
|---|---:|---:|---:|---:|
| gamma=0.20 | 222.211 | 24.565 | 143.199 | +79.011 |
| gamma=0.30 | 222.100 | 24.553 | 131.507 | +90.592 |
| gamma=0.65 | 221.842 | 24.524 | 113.143 | +108.699 |

At D's conservative factor 0.20, 2 m struts have mid-radius 37.307 mm, wall
0.529 mm and design stress 346.401 MPa. Length/radius is 53.609: the local factor
does not settle shell/column interaction. At B's reference factor and `q=0.99`,
the corresponding values are 52.108 mm, 0.962 mm and 675.789 MPa. The favourable
C strut is 60.800 mm radius and 0.705 mm wall at 790 MPa. None is a qualified
manufacturing drawing or allowable.

For D, the identical air-filled control gives −74.192 t: the +153.203 t change
is gas substitution, not a structural or geometrical miracle. Its material
volume/pressure budget is explicit, but buoyancy still depends on retaining
the light gas. At fixed temperature, pressure and geometry, about 51.6% air
mole fraction in the plenum consumes D's 79.011 t nominal margin. Pressure
regulation, leaks and a passive differential-pressure limit are necessary
design functions with unresolved hardware; the model does not size a runaway
pump/full-vacuum event as D's normal load.

## Component budgets and expert ledger

| Component, t | A q=.99 g=.30 | B q=.80 g=.30 | C g=.30 | C g=.20 | C g=.65 | D g=.20 |
|---|---:|---:|---:|---:|---:|---:|
| Lattice members | 203.839 | 176.844 | 814.687 | 932.583 | 696.906 | 80.337 |
| Nodes/joints | 30.576 | 26.527 | 122.203 | 139.887 | 104.536 | 12.050 |
| Load-bearing film | 4.140 | 3.081 | 9.602 | 9.602 | 9.602 | 0.770 |
| Barrier/seams | 0.849 | 0.782 | 1.970 | 1.970 | 1.970 | 0.782 |
| Boundary transitions | 5.097 | 4.694 | 11.822 | 11.822 | 11.822 | 4.694 |
| Equipment/payload allowances | 20.000 | 20.000 | 20.000 | 20.000 | 20.000 | 20.000 |
| Residual gas | 2.213 | 44.317 | 8.889 | 8.896 | 8.879 | 24.565 |
| All included mass | 266.713 | 276.245 | 989.174 | 1124.762 | 853.716 | 143.199 |
| Gross displaced-air lift | 221.269 | 221.585 | 888.870 | 889.627 | 887.859 | 222.211 |
| Net conditional margin | -45.444 | -54.660 | -100.303 | -235.136 | 34.143 | 79.011 |

No component is omitted silently: quantities above are either calculated from
the stated surrogate or explicitly assumed allowances. Whether the allowances
cover all hardware is UNKNOWN. Positive sums are conditional budgets, not
demonstrated all-up vehicles.

| Expert assumption to confirm | Why it matters and change if wrong |
|---|---|
| Tube/assembly stability and the local-wall factor | C moves from +34.143 t at 0.65 to −100.303 t at 0.30 and −235.136 t at 0.20. D retains +79.011 t at 0.20, but none of these scalars proves boundary or global stability. Resolve with a specified laminate, coupled member modes and a complete loaded assembly model, then applicable physical evidence. |
| Cross-ply compression and stiffness simultaneously available | Reducing C's compression ceiling by 25% gives −231.274 t; reducing its effective modulus by 20% gives −5.909 t. D at factor 0.20 is buckling-governed and unchanged by the 25% compression reduction. Resolve actual laminate/process allowables rather than importing a UD coupon ceiling. |
| Manufacturable wall gauge and joint tolerance | D assumes 0.529 mm walls. A 1 mm wall floor at its unchanged radii/grid raises member mass from 80.337 to 151.744 t and changes the margin to −2.786 t, including revised elastic contraction. The floor is a sensitivity, not a sourced manufacturing limit. Resolve layup, minimum gauge, damage and local reinforcement before crediting the thin tubes. |
| Joint fraction and equipment inventory | Doubling C's node fraction to 30% gives −70.393 t. Changing its equipment from 20 to 50 t leaves +4.143 t; 100 t gives −45.857 t. Applying both 30% nodes and 50 t equipment to D leaves +36.961 t, still conditional. Resolve a node/support bill and a named operating mission. |
| Boundary mass and load path | C at 1.0 kg/m² boundary mass leaves +6.557 t; break-even is 1.1664 kg/m². Added boundary mass alone does not demonstrate stiffness or transfer of film loads. Draw and size one repeating loaded boundary patch, its seam and its connection to the lattice. |
| Loaded volume, altitude and atmosphere | Another 1% loaded-volume loss leaves C +25.353 t when gas follows pressure control. At 2,500 m air density 0.9569 kg/m³, holding mass and shape fixed instead, C is −160.178 t. Sea-level arithmetic is not an altitude operating envelope. |
| Gas composition and containment for D | Replacing helium with air changes margin by −153.203 t; approximately 51.6% air mole fraction erases the nominal surplus. Resolve barrier permeation, leak rate, pressure protection and temperature schedule; no containment test exists. |

The dominant unresolved assumption for the current preferred paper branch D is
that the complete lattice and its boundary can carry the specified loads at
the priced mass. Its more generous scalar budget makes it the next candidate
to detail, not a vehicle that now floats confidently.

## Next design change and carry

Keep the 70.575 m sphere and the same payload allowance; compare D with a
near-ambient-pressure helium design, using an explicitly tension-loaded skin,
ballonet/pressure-control geometry, and a priced wind-load support/suspension
system. Carry a 1 mm tube-wall sensitivity wherever a lattice remains. Remove
the vacuum compression lattice only when those functions have
replacement mass and load paths. Do not extrapolate this lattice formula to
zero pressure and count a zero-mass structure as a design. The calculation here
has not established whether the hybrid is preferable to that conventional
control. That comparison is the next proposed assigned unit, with its own
bounded paper record; no new solve or physical work is started here.

Starting state: no qualified all-up aircraft. Learned: retaining air loses more
lift than the compared pressure relief saves; a spherical boundary alone is a
small saving; a high-performance vacuum sphere depends on an unqualified
material/knockdown combination; a helium-assisted branch has room in the scalar
budget. Deferred: global/combined-mode buckling, finite boundary assembly,
components, mission loads, manufacturing and gas/temperature control. Reason:
they need a drawn design and an appropriate execution/validation scope.

Documentation checks are `make readmecheck linkcheck buildercheck`, with the
Builder check after commit. These inspect documentation/history, not physics.
The one unit evidence record held with the candidate identifies the exact
base, tree, candidate and observed check exits. No signature or landing is
claimed here; the [programme claim gate](../../../docs/CLAIM-GATE.md) remains
applicable before any public result publication.

## Reproduce the bounded arithmetic

Run the following with Python 3, or save it to a local file and execute it.
It emits the comparison, scale and lifting-gas rows and one-variable
sensitivities. It uses no package, solver, service or input file. The 60-step
bisections find scalar budget zeroes only; they are not optimisations or
structural stability solves.

```python
"""Bounded paper arithmetic; no solver, repository mutation, or physical validation."""
import json
from math import pi, sqrt

P = 101325.0
RHO_AIR = P / (287.05 * 288.15)
E = 354e9 * 0.75**0.75 * 0.25**0.25
HELIUM_RATIO = (P * 0.004002602 / (8.314462618 * 288.15)) / RHO_AIR
RHO = 1658.0
SF = 1.5
C = 6 * sqrt(2) * pi
V_REF = pi * 26**2 * 52 + 4 * pi * 26**3 / 3
D_EQ = (6 * V_REF / pi)**(1 / 3)

def case(shape, diameter, q, gamma, sigma=790e6, modulus=E,
         nodes=0.15, edge=0.30, equipment=20000.0, gas_ratio=1.0,
         min_wall_m=0.0):
    assert 0 < q <= 1 and 0 < gamma <= 1
    if shape == "capsule":
        volume = 5 * pi * diameter**3 / 12
        area = 2 * pi * diameter**2
    else:
        assert shape == "sphere"
        volume = pi * diameter**3 / 6
        area = pi * diameter**2
    kl = 0.605 * gamma
    a = 2 * kl / pi**2
    c = 2 * C * a
    k = kl / (3 * sqrt(c))
    phi_b = (SF * q * P / (k * modulus))**(2 / 3)
    phi_c = 3 * SF * q * P / sigma
    phi = max(phi_b, phi_c)
    mode = "buckling" if phi_b > phi_c else "compression"
    psi = sqrt(phi / c)
    lam = sqrt(a * psi)
    radius = 2.0 * lam  # tube mid-surface radius, 2 m pinned strut
    wall = radius * psi
    if wall < min_wall_m:
        mode = "minimum gauge"
        wall = min_wall_m
        psi = wall / radius
        phi = 2 * C * radius * wall / 2.0**2
    strain = 3 * q * P / (phi * modulus)
    loaded = volume * (1 - strain)**3 - 0.13 * area * (1 - strain)**2
    members = RHO * phi * volume
    film_areal = 1560 * q * P * 2.125 / (2 * (5.8e9 / 4 * 0.5))
    masses = {
        "members": members,
        "nodes": nodes * members,
        "film": film_areal * 1.0625 * area,
        "barrier": 0.05 * area,
        "boundary": edge * area,
        "all_up_allowance": equipment,
        # Full loaded volume slightly overcharges gas: solids are not subtracted.
        "gas": (1 - q) * RHO_AIR * gas_ratio * loaded,
    }
    gross = RHO_AIR * loaded
    total = sum(masses.values())
    stress = 3 * SF * q * P / phi
    local = kl * modulus * psi
    euler = pi**2 * modulus / 2 * lam**2
    assert min(local, euler, sigma) >= stress * (1 - 1e-12)
    return {
        "shape": shape, "diameter_m": diameter, "q": q, "gamma": gamma,
        "gas_ratio": gas_ratio,
        "volume_m3": volume, "area_m2": area, "loaded_m3": loaded,
        "phi": phi, "phi_b": phi_b, "phi_c": phi_c,
        "radius_mm": radius * 1000, "wall_mm": wall * 1000,
        "l_over_r": 2 / radius, "r_over_t": 1 / psi,
        "strain": strain, "design_stress_mpa": stress / 1e6,
        "mode": mode,
        "mass_t": {name: kg / 1000 for name, kg in masses.items()},
        "gross_t": gross / 1000, "total_t": total / 1000,
        "margin_t": (gross - total) / 1000,
        "equipment_ceiling_t": (gross - total + equipment) / 1000,
    }

def bracket_zero(fn, lo, hi):
    assert fn(lo) < 0 < fn(hi)
    for _ in range(60):
        mid = (lo + hi) / 2
        if fn(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

if __name__ == "__main__":
    rows = [case(shape, d, q, gamma)
            for gamma in (0.20, 0.30, 0.65)
            for shape, d in (("capsule", 52), ("sphere", D_EQ))
            for q in (0.99, 0.80)]
    scale = [case("sphere", 112, 0.99, gamma) for gamma in (0.20, 0.30, 0.65)]
    hybrid = [case("sphere", D_EQ, .20, gamma, gas_ratio=HELIUM_RATIO)
              for gamma in (.20, .30, .65)]
    hybrid_air = case("sphere", D_EQ, .20, .20)
    base = scale[-1]
    sensitivity = {
        "nodes_30pct": case("sphere", 112, .99, .65, nodes=.30)["margin_t"],
        "sigma_minus25pct": case("sphere", 112, .99, .65, sigma=592.5e6)["margin_t"],
        "modulus_minus20pct": case("sphere", 112, .99, .65, modulus=.8*E)["margin_t"],
        "equipment_50t": case("sphere", 112, .99, .65, equipment=50000)["margin_t"],
        "equipment_100t": case("sphere", 112, .99, .65, equipment=100000)["margin_t"],
        "boundary_1kgm2": case("sphere", 112, .99, .65, edge=1.0)["margin_t"],
        "extra_1pct_loaded_volume_loss": base["margin_t"]-.99*base["gross_t"]*.01,
        "2500m_same_mass_shape": base["margin_t"]+(.9569-RHO_AIR)*base["loaded_m3"]/1000,
        "gamma_break_even": bracket_zero(lambda g: case("sphere",112,.99,g)["margin_t"],.30,.65),
        "sigma_break_even_mpa": bracket_zero(lambda s: case("sphere",112,.99,.65,sigma=s*1e6)["margin_t"],592.5,790),
        "diameter_break_even_m": bracket_zero(lambda d: case("sphere",d,.99,.65)["margin_t"],D_EQ,112),
        "boundary_break_even_kgm2": .30 + base["margin_t"]*1000/base["area_m2"],
        "hybrid_air_control_margin_t": hybrid_air["margin_t"],
        "hybrid_30pct_nodes_50t_equipment": case("sphere",D_EQ,.20,.20,nodes=.30,equipment=50000,gas_ratio=HELIUM_RATIO)["margin_t"],
        "hybrid_sigma_minus25pct": case("sphere",D_EQ,.20,.20,sigma=592.5e6,gas_ratio=HELIUM_RATIO)["margin_t"],
        "hybrid_minimum_wall_1mm": case("sphere",D_EQ,.20,.20,gas_ratio=HELIUM_RATIO,min_wall_m=.001)["margin_t"],
        "hybrid_air_mole_fraction_break_even": hybrid[0]["margin_t"]/(hybrid[0]["margin_t"]-hybrid_air["margin_t"]),
        "helium_ratio": HELIUM_RATIO,
    }
    print(json.dumps({"comparison":rows,"scale":scale,"hybrid":hybrid,"sensitivity":sensitivity},indent=2))
```
