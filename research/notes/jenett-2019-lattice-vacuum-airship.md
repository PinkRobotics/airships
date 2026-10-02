# Jenett, Gregg & Cheung (2019) — Discrete Lattice Material Vacuum Airship

AIAA SciTech 2019-0815, also NTRS 20190001133. Read in full from the NTRS PDF.

## What it establishes

Earlier vacuum-balloon analyses concluded the problem was one of *stability*: a shell thin enough
to float buckles. This paper's contribution is to redo that analysis with a cellular solid in place
of a homogeneous material, and to show the constraint moves. For an architected lattice whose
modulus and strength both scale *linearly* with relative density (`A = B = 0.1`, `α = β = 1`), the
stiffness requirement collapses to a specific-modulus condition that carbon composites clear by an
order of magnitude, while the strength requirement does not move at all. Solid, thick-shell and
thin-shell designs all end at the same place: the lattice constituent needs a specific strength
above **1,220–1,236 kN·m/kg**. Toray M60JB (3.82 GPa, 1,930 kg/m³) gives 1,979 kN·m/kg, a margin
of 1.6. The conclusion is that a lattice vacuum airship is strength-limited, not stability-limited.

## What this project takes

The ledger's bet — `dryT = cls.payloadT` in `sim/physics.js` — is the claim that a hull enclosing
22 million m³ of vacuum can be built for 10,000 t. This is the paper that makes such a claim
arguable at all, and it is the only source in the collection that puts a *number* on the lift a
lattice sphere can produce. Table 2 gives net lift against radius: 3,005,114 kg at R = 100 m.

That table also convicts us. A sphere of R = 100 m displaces 5,131 t at 1.225 kg/m³, so the shell
is 2,126 t, or **0.508 kg per m³ of enclosed volume** — and because the design rules are ratios
(`R/t = 10`, lattice pitch `t/10`), the same fraction holds at every radius in the table. Our whole
dry allowance is 10,000 t in 22,000,000 m³, or **0.455 kg/m³**. Jenett's bare lattice shell is 1.12 times as heavy as everything the model has budgeted for structure, rotors, tanks, batteries, pumps and the
cryogenic plant combined.

## Where it does not support us

The paper prices the lattice and nothing else. Table 1 counts 125,600 skin panels and never gives
them a mass; the conclusion claims "large margins for skin mass penalties" without computing one,
and the sealing skin is the component Metlen (2013) found adds 0.37 to W/B on its own. There is no
joint mass, no valve, no vacuum plant.

The simulation is a planar quarter-section of beam elements in Oasys GSA, and the paper says full
3D work is "later work" — so the global buckling mode of a complete shell is not tested here.
Everything is a sphere at sea level; the model’s largest nominal hull is a 512 × 256 m capsule. The
sphere is the optimum shape for external pressure, so the drawn geometry is worse, and its assumed
buoyancy does not establish pressure capacity.

Altitude does not rescue us either. The governing requirement (equation 36) reduces to
`15 · P/ρ`, and `P/ρ` for air is `R·T` — a function of temperature alone. At 2,500 m ISA the
requirement falls from ≈1,241 to ≈1,171 kN·m/kg, under 6%. Thinner air lifts less in exactly the
proportion it presses less hard.

Finally, it is a conference paper carrying a literal `[cite]` placeholder in Section IV.C and
several undated references. It has not been through journal review.
