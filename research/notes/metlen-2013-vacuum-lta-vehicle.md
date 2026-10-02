# Metlen (2013) — Design of a Lighter than Air Vehicle that Achieves Positive Buoyancy Using a Vacuum

AFIT-ENY-13-J-02, Air Force Institute of Technology MSc thesis, advisor A. N. Palazotto.
Approved for public release; distribution unlimited. Read the abstract, methodology and results
chapters in full.

## What it establishes

Metlen defines the figure of merit this whole literature turns on: **W/B**, the ratio of structure
weight to the weight of displaced air. W/B < 1 floats. He then optimises three real designs with a
non-linear programme in Matlab and reports what each costs.

- Thin-shelled sphere, isogrid of blade stiffeners, ultra-high-modulus carbon epoxy: **W/B = 0.81**.
- Same, with a beryllium skin: **W/B = 0.79**.
- Geodesic sphere of UHM carbon-epoxy pultruded rods, frame only, clamped cylindrical beam
  elements in FEA: **W/B = 0.57**.
- The same frame with a membrane that exists: Zylon-reinforced Mylar adds **0.37**, giving an
  overall **W/B = 0.94**.
- With a membrane as strong as graphene, the skin costs 0.001 and the total returns to 0.57.

He also investigated a twin counter-rotating-cylinder vacuum vehicle and found it infeasible.

For scale, he records that conventional airships reach W/B < 0.3, and the Zeppelin NT's skin plus
frame is about 0.18.

## Why it is in this collection

Because it is the most complete published accounting of the part everyone else leaves out. Jenett
et al. price the lattice and not the skin; Akhmeteli & Gavrilin price the sandwich and not the
joints or adhesive. Metlen prices a frame *and* a real membrane, and the membrane nearly doubles
the structure.

## Where it cuts against us

The fleet model assumes dry mass equals payload; it has not sized a fleet hull.
The [float ledger](../../docs/FLOAT-LEDGER.md) compares that allowance at sea level and 2,500 m.
Nothing floats today as drawn. Material and load tests, plus a complete structure and equipment bill, would have to establish closure.

Two further points make his number optimistic for us rather than pessimistic. Every design he
found workable is a sphere; the sphere is the best possible shape against external pressure and our
largest nominal hull is a 512 × 256 m capsule. And W/B counts structural mass
only — no rotors, no 2,000 MWh of batteries, no 15,500 t nitrogen tank, no pumps, no 850 m anchor
cable.

Where it does not settle the question: it is a 2013 masters thesis, not peer-reviewed, and the
graphene-skin case shows the author knew the membrane was the open problem. If a sealing skin
appears with a specific strength an order of magnitude beyond Zylon, his 0.57 returns and the
argument reopens. Nobody has built one.
