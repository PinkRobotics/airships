# Akhmeteli & Gavrilin (2021) — Vacuum Balloon: A 350-Year-Old Dream

*Eng* 2021, 2(4), 480–491. CC BY 4.0. Read in full.

## What it establishes

Two things, and the second matters more than the first.

The negative result is exact. For a homogeneous single-layer evacuated sphere, floating requires
`h/R = ρa/3ρs` and surviving requires the classical buckling pressure to exceed one atmosphere;
combining them demands `E/ρs² ≳ 4.5 × 10⁵ kg⁻¹m⁵s⁻²`. Diamond, at 1.2 TPa and 3,500 kg/m³, reaches
about 1 × 10⁵. A perfect diamond sphere of ideal geometry buckles at roughly **0.2 atmospheres**.
No solid in existence can be a one-layer vacuum balloon, at any radius — the criterion is
scale-free.

The positive result is a three-layer sandwich: boron carbide face skins (460 GPa, 2,500 kg/m³,
3.2 GPa compressive) bonded to PLASCORE 5056 aluminium honeycomb (50 kg/m³). Optimising against
their own analytical buckling estimate and then against an ANSYS axisymmetric eigenvalue buckling
FEA gives face skins `4.23 × 10⁻⁵·R` and a core `3.52 × 10⁻³·R`, with a buckling safety factor
λ_min = 2.65. They check face-skin compressive stress (600 MPa against 3,200), shear crimping,
face wrinkling and intracell dimpling, the last of which sets a *minimum* radius of R > 2.11 m.
Worked example at R = 2.5 m: 106 µm skins, 8.8 mm core, shell 75.7 kg, payload 8.7 kg.

## What this project takes

The design is quoted at a **payload fraction q = 0.1**: at zero buoyancy, everything that is not
shell may weigh one tenth of the displaced air. That is the most rigorous published number for what
a vacuum hull costs, and it is the number our ledger has to beat.

## Where it does not support us

It does not support us anywhere. On their numbers the shell alone is 0.9 × 1.29 = **1.16 kg per m³**
of enclosed volume. The fleet model's entire dry-mass allowance, covering structure, rotors, batteries, cryogenic plant, pumps and tanks, is 0.455 kg/m³.
Their shell alone is 2.55 times that assumed allowance.

Worse, and this is our arithmetic rather than theirs: a shell massing 90% of sea-level air density
is neutrally buoyant *empty* at roughly 0.6–1.1 km in the ISA column, depending on whether you
size against their 1.29 kg/m³ or ISA's 1.225. Our hulls work at 2,500 m MSL. An Akhmeteli sphere
sized for our loads would not reach the altitude our fleet cruises at, let alone carry water there.

Their own caveats are worth carrying too. Imperfections are explicitly excluded from the FEA; they
argue by analogy from experiments on homogeneous shells that a knockdown factor above 0.4 is
achievable where 0.2 is the recommendation for sandwich domes, and note that ±1% thickness control
means ±0.1 mm on a 9 mm sandwich. Adhesive mass, joints between panels and leak management are all
named and none is costed. And nothing has been built: the paper's closing line asks how long the
first vacuum balloon will take.
