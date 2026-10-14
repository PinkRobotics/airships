# R3-I028 — machined aluminium socket bodies at the frozen drawn dimensions

Status: **conditional candidate, same-day return** — one material substitution on the
accepted R3-I019 (rev v3.1) / R3-I023 termination-and-load-path lineage, evaluated at
frozen integration base `e3a6f7b854ef0683fbcdacd6db330a7c3b94044b`
(tree `91c7eadb15f641e918fd94faf87c70599a418363`). Inputs pinned:
`R3-I019/termination.json` sha256 `0fb204a2362f17f342b1582fb2e41981f7207402b509db81ba3bbf5c38a2cc6a`,
`R3-I023/loadpath.json` sha256 `5094e61bcf60f98ff7e89d7d3798f633528b67a02cc1552857c2158f29c99b63`
(read as data; never imported, executed or regenerated).

## The one changed assumption

The two drawn socket-body sizes become **machined 6061-T6-class aluminium** bodies of
the **same drawn dimensions** — bore, OD, body length, grip and nose unchanged:

| property | Ti-6Al-4V (retained hardware) | aluminium body (this unit) |
|---|---|---|
| E | 114 GPa (datasheet) | **69 GPa** |
| density | 4,430 kg/m³ | **2,700 kg/m³** |
| working normal-stress limit | 880 MPa yield (datasheet) | **150 MPa chosen working limit** |

The aluminium record is **ASSUMED modelling input, not a sourced or certified
property**: 150 MPa is the chosen working limit with no hidden second material safety
factor; the fitting-demand factor and the pressure safety cases stay distinct; no
laminate or cord strength is borrowed. A named alloy alone does not qualify the body,
bond, thread or wet/creep service.

**Everything else is retained exactly:** titanium studs (M14×79 / M23×127), jam nuts,
anchor blocks and M10 attachment bolts (45/50 mm shanks); both UHMWPE-class cord
families (E = 70 GPa, 970 kg/m³, strength UNKNOWN); grip lengths 60/97 mm; potting;
plane/station counts; the full pressure structure. No station removal, shorter grip,
narrowed disturbance field or stiffness fit appears in this candidate.

## Mass: complete incremental bill (matching-lift basis)

Lift, payload, mission, gas inventory and pressure ratio are **unchanged**, so every
margin delta below comes solely from the reconciled mass. Bodies are priced by each
family's actual end count × geometric volume (π/4·(OD²−bore²)·body length); the
geometric volume reconciles with the frozen per-end body masses to ≤0.2 %.

| line | before (t) | after (t) | Δ (t) |
|---|---|---|---|
| socket bodies (metal only) | 12.866 | 7.842 | −5.024 |
| isolation/protection provision (0.025 kg/end, 42,470 ends) | — | 1.062 | +1.062 |
| machining/assembly stock (3 % of new body metal) | — | 0.235 | +0.235 |
| other socket metal (studs, nuts — unchanged) | 7.274 | 7.274 | 0 |
| **hardware increment** | | | **−3.728** |
| 5 % assembly share on the increment | | | −0.186 |
| **total increment** | | | **−3.914** |

The declared provision — an isolating bushing pair (epoxy-glass class) plus
primer/sealant film at every retained Ti-stud/Al-body interface, with its installation
stock — is priced so the necessary galvanic/contact barrier is **not at zero mass**;
its sufficiency is UNKNOWN. The 5 % share on the increment follows the record's own
assembly accounting (the x1.5 station-hardware precedent).

| whole-vehicle line | before | after |
|---|---|---|
| sockets line (hardware) | 20.14 t | 16.41 t |
| spokes line | 245.42 t | 241.51 t |
| whole known subtotal | 2,233.4 t | **2,229.5 t** |
| sea-level margin | +16.4 t | **+20.3 t** |
| 2,500 m margin | −476.1 t | **−472.2 t (FAIL persists)** |
| SF1.2 adverse case: after-mass / after-spokes / after-margin | 2,562.4 t / 243.98 t / −312.6 t | **2,558.5 t / 240.07 t / −308.7 t (FAIL persists)** |

The 2,233.4 t / +16.4 t / −476.1 t triple was already a **conditional known
subtotal**; it stays conditional. The inherited x1.5 station-hardware sensitivity
(+16.05 t increment, +0.3 t SL with its assembly share) does not scale socket bodies
and is carried unchanged; the new provision/machining lines are not part of that
frozen scenario.

## Compliance: the changed spring term, propagated

The stud/body series compliance (carried as cord length `L_ser` in the record's ONE
denominator law `L_free + 2·L_a`) is rebuilt replacing **only the body term** with the
new modulus — the frozen total minus the recomputed titanium body term keeps every
retained term exact (rebuild reconciliation ≤ 2×10⁻⁵ m, i.e. published 0.1-mm
rounding):

| family | L_ser (m) | chain denominator (m) | eta (mean cord) | first slack, declared model (mm) |
|---|---|---|---|---|
| d60 | 0.021040 → 0.025040 | 12.242397 → 12.250396 (+0.065 %) | 1.000257 → 1.000142 | 26.6213 → 26.6387 |
| d180/11 | 0.033220 → 0.039171 | 17.360698 → 17.372599 (+0.069 %) | 1.000381 → 1.000233 | 25.4921 → 25.5096 |

Pretension–extension: at the same installed prestrain the set tension falls
6.809 → 6.805 kN (d60) and 17.797 → 17.785 kN (d180/11); **holding the T0 set point
needs 16.0 / 23.8 µm of extra stud take-up** — stated as a demand only, with **no
restored stability licence, no free installation-after-evacuation, no extra travel and
no pressure-bearing tensile-cord path claimed** (the R3-I023 common-strain equilibrium
closure stays withdrawn; installation and global-equilibrium work stays UNKNOWN).
Plane preload totals are unchanged **on the set-point basis** (stud adjusted to T0).
The first-slack and class-bound tables of the frozen record propagate by the exact
denominator ratio (both bases tabulated in `socket_body.json`); the coupled eigen
margin (predecessor licensed value 1.000811) is **not recomputed** — a dependent
claim exposed as UNKNOWN under the changed spring, bounded analytically by the
< 0.07 % denominator move.

## Screens through the reduced body

- **Net body section (mouth/net annulus), fitting demand** — the frozen worst
  fitting-demand case T_fit = 1.3 × 2 × T0 traces through the unchanged net section:
  d60 17.7 kN / 3.70×10⁻⁴ m² = **47.8 MPa**, d180/11 46.27 kN / 9.67×10⁻⁴ m² =
  **47.9 MPa** — utilisation **0.319** against the ASSUMED 150 MPa limit:
  **conditional PASS** (conditional on the ASSUMED record, unqualified).
- **Bond interfaces** — demands are unchanged by this substitution (wall interface
  10.379 MPa, required grips 59.68/96.48 mm vs drawn 60/97 mm), but the 12 MPa design
  bond shear is **not valid for the machined aluminium substrate without
  qualification**: carried at utilisation 0.865 vs the ASSUMED value, capacity
  **UNKNOWN on the new substrate**.
- **Stud engagement and transfer surfaces** — dimensioned below; the frozen record
  does not pin the drawn thread-engagement length, so thread stripping has **no
  bounded justified screen: UNKNOWN** (as are fatigue, creep, and corrosion/contact
  behaviour beyond the declared provision mass; laminate bearing, block local
  bending, pull-through stay UNKNOWN from the record).

## Dimensioned detail (ASCII, both families; retained Ti parts marked Ti)

```
            cord axis ──────────────────────────────────────────►
        nose 8        grip 60 (d60) / 97 (d180-11)       nose 8
   ┌──────┬──────────────────────────────────────────────┬──────┐
   │ pot  │        potted cord + epoxy (unchanged)       │ pot  │
   └──────┴──────────────────────────────────────────────┴──────┘
   [Al body: OD 23.5 / 38.0 mm, bore 9.0 / 14.6 mm, length 76 / 113 mm]
        │                                              │
        │ bond film (assumed 12 MPa, Al substrate      │
        │ unqualified) — required grip 59.68/96.48 mm  │
        ▼                                              ▼
   ═════════════ Ti stud M14 / M23 (retained) ═════════════════
        ▲
        └── isolating bushing pair + sealant (0.025 kg/end, ASSUMED,
            galvanic/contact barrier priced, sufficiency UNKNOWN)
   anchor centre = grip back face (the record's ONE datum, unchanged);
   attachment: 3 × M10 Ti through-bolts, 45/50 mm shanks (retained)
```

## Verdict

A real density saving (−3.9 t whole-vehicle) with the compliance cost retained and
propagated; the net-section screen passes conditionally on the ASSUMED record; the
inherited **2,500 m and SF1.2 mass FAILs persist unchanged in kind**; the leading
uncertainties (bond/thread/fatigue/creep/corrosion on aluminium) are UNKNOWN, not
priced at zero. This is a **conditional candidate**, not a physical float claim.

**Weakest assumption:** the aluminium body record itself — whether the ASSUMED
6061-T6-class body and its bond/thread interfaces can carry the declared fitting
demand with acceptable compliance and durability; the bond value on the machined
substrate is the sharpest single unknown (capacity UNKNOWN; only demand is carried).

**Next change (ranked):** qualify the aluminium substrate bond and the stud-engagement
screen (thread stripping) — the two local UNKNOWNs this candidate turns on. If those
local screens hold, the independent R3-I023 equilibrium/installation construction
remains the next unresolved vehicle task, separate from this branch.

**Scoreboard (≤180 chars):** R3-I028 Al socket bodies @ fixed dims: known subtotal
2233.4→2229.5 t; SL +16.4→+20.3 t; 2500 m −476.1→−472.2 FAIL; SF1.2 −312.6→−308.7
FAIL; bond/thread on Al UNKNOWN.

## Reproduction

```
python3 research/design-iterations/R3-I028/socket_body.py
```

Standard library only; reads the frozen `baseline.json` (sha-pinned by
`sources.json`) and writes `socket_body.json`. Two bounded executions were used for
this unit (initial + one demonstrated margin-sign correction, both preserved in the
unit evidence); the design itself was frozen before the first run and never tuned.

## Expert-confirmation ledger (short)

1. Mass arithmetic is count × geometric volume at the two densities; reconciliation
   with frozen per-end masses ≤ 0.2 %.
2. The series-compliance replacement changes only the body term; retained terms are
   carried by the frozen residual, with an independent K-dimension rebuild agreeing
   to ≤ 2×10⁻⁵ m.
3. Every margin moves only by the reconciled −3.914 t increment (lift unchanged);
   no predecessor stiffness margin is silently retained where the spring term
   changed — the coupled eigen margin is exposed as not recomputed.
4. The net-section PASS is conditional on the ASSUMED 150 MPa record; nothing on
   this page qualifies the alloy, bond, thread, wet or creep service.
5. Inherited FAIL/UNKNOWN qualifications from R3-I019/R3-I023 remain visible and
   unclosed; this unit opens no review of their records and claims no float.
