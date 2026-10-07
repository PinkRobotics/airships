# Evidence map

Every quantitative claim this project publishes, and what it actually rests on.

Written 2026-08-09 against the working tree at that date; PHYSICS and OPEN-QUESTIONS section numbers are theirs of that date. Every number in the right-hand
columns was either read out of the code or produced by running the model — `make test`
(194 passed, 2 known-failing), `AIRSHIPS.sim.selftest()` (19 checks, pass), and a series of
probe scripts driven through `tools/js_eval.py` against
`index.html?seed=7&data=snapshot`. Where this document disagrees with `docs/PHYSICS.md`, the
model was re-run and the model won; those disagreements are listed in §2.

`research/sources.json` did not exist when this was written, so cited sources are named in
prose. When the catalogue lands, the `rests on` column of the CITED rows should be replaced
with its ids and nothing else in this file should need to change.

## The five categories

**PHYSICS** — follows from a relation not in dispute, named in the row. Archimedes, the ISA
barometric relations, ideal actuator-disc momentum theory, hydraulic pump work, and pure
arithmetic identities on top of them. A PHYSICS row is not a claim that the figure is right;
it is a claim that *given its inputs*, the arithmetic is not where you should attack.

**CITED** — depends on a published source, named.

**ASSUMED** — somebody chose a number, said so, and said what it is for. The row gives what
constrains it and what would move it. This category was expected to be the largest, and it is
not: it is second, by a factor of two. That inversion is the main finding of this document and
§ Counts says why it matters.

**ARBITRARY** — a number with no stated justification anywhere in the repository. These are
defects. `min(6, RETURN_TRANSIT × 0.2)` is the known example; it is one of thirty-two rows.

**CIRCULAR** — a figure justified by another figure that was itself chosen to make the first
one come out. Four rows. One of them is the worst thing in the model.

Where a row carries two categories, the dominant one is given first.

---

## The map

### Atmosphere and the lift ledger

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| ISA constants | T₀ 288.15 K, p₀ 101 325 Pa, L 0.0065 K/m, g₀ 9.80665, R 287.0528 | `sim/atmosphere.js` `ISA` | **CITED** — ISO 2533:1975 / ICAO Doc 7488, named in the source | Solid. These are stipulated definitions, not measurements, so they are exact by construction. Cross-checked against the published table in `tests/cases/sim-atmosphere.cases.js`. The strongest evidence in the repository. |
| ρ_SL | 1.225 kg/m³ | `DEFAULTS.rhoSL` | **CITED** — p₀/(RT₀) under the same standard | Solid, and correctly used as the *anchor* of a column rather than as the density anything is weighed in. |
| ρ(h) | 0.956859 at 2 500 m; 1.111643 at 1 000 m | `airDensity()` | **PHYSICS** — hydrostatic balance through a linear temperature profile | Solid. Throws outside the layer rather than extrapolating, which is the right failure mode. |
| terrain reference `TERRAIN_MSL` | 1 000 m MSL | `sim/config.js` | **ASSUMED** — one figure for the whole interior plateau | Deliberately coarse and says so. Moving it moves every density in the model. A recovery onto a valley floor at 350 m is stated to be outside the design, which is the honest version. |
| working altitude `WORK_ALT_MSL` | 2 500 m MSL (1 500 m AGL) | `sim/config.js` | **ASSUMED**, constrained by a terrain envelope | The envelope claim — interior fuel belt from 300–500 m valley floors to ~2 100 m treeline, Big White ~2 320 m — is asserted in prose with no source. It is checkable and probably right, but it is uncited, and it is the justification for the single most expensive number in the model. |
| L = ρ(h)·V | — | `ledger()` | **PHYSICS** — Archimedes | Solid. The 2026-08-09 fix (altitude required, no default) is the right shape: a caller that has not decided where the ship is now gets an exception. |
| dry mass allowance | m_dry = m_payload | `ledger()`, `dryT: cls.payloadT` | **ASSUMED** — "the ledger's bet", stated as such | The single load-bearing assumption in the project. Nothing constrains it; it was chosen. Everything below inherits from it. See §1.1. |
| displacement | 2 200 m³ per tonne of payload → 220 000 / 2.2×10⁶ / 2.2×10⁷ m³ | `CLASSES[*].dispM3` | **ASSUMED** — solves float-up at 5% margin, then rounded up | 2 194.7 m³/t gives exactly 5.00%; 2 200 is the round number above it. Verified by sweep: 2 000 → −4.31%, 2 100 → +0.47%, 2 200 → +5.25%. |
| float-up margin | **+5.25%**, identical on all three classes | `figures.json` `floatUpMarginPct` | **CIRCULAR** | Presented as a result ("the margin is +5.25% on all three classes") when it is an input: a 5% requirement divided by a rounding. It is identical across classes only because m_dry = m_pay is identical across classes, so the "no class needed an exception" line is a restatement of the assumption, not a check on it. The arithmetic is right; the framing is not. |
| lift at working altitude | 210.5 / 2 105.1 / 21 050.9 t | `ledger(cls, 2500)` | **PHYSICS** on the two rows above | Solid arithmetic; entirely dependent on the assumed displacement. |
| surplus at the source (1 300 m) | 137.4 / 1 374.4 / 13 743.6 t | `ledLow.surplusT` | **PHYSICS** | Solid, and it is the number that makes the descent hard. Correctly evaluated where the manoeuvre happens, since 2026-08-09. |
| loaded break-even density | 0.90909 kg/m³ = ISA at 3 000 m | `docs/PHYSICS.md` §1 | **PHYSICS** — 2m_pay/V | Solid, and the cleanest single statement of the fix: it moved from 1 005 m (below the drop run) to 500 m above the ceiling. |
| hull dimensions | 190×47, 404×102, 876×219 m; fineness 4 | `CLASSES[*].lenM/diaM` | **PHYSICS** (spheroid volume) on an **ASSUMED** fineness ratio | Volume matches a prolate spheroid to better than 0.2%, which is checkable and checks out. Fineness 4 is a choice; it sets frontal area and therefore drag. |
| implied shell areal density | 4.43 / 9.58 / 20.59 kg/m² | `docs/PHYSICS.md` §2 | **PHYSICS** on the dry-mass bet | Solid arithmetic, and the project correctly refuses to call it a design. It is 47.5% of what the lift budget permits, identically for all three classes — again because m_dry = m_pay, not because anything was analysed. |
| monocoque vacuum-shell requirement | E/ρ_m² ≥ 5.0×10⁵ Pa·m⁶/kg²; best material short by ~6× | `docs/PHYSICS.md` §2 | **PHYSICS** (Zoelly elastic buckling of a complete sphere) + **CITED** material properties | The best-evidenced argument in the project, and it argues *against* the concept. The derivation is standard, the elimination of R and t is correct, and the materials table is checkable. No safety factor, no imperfection knockdown — which makes the 6× a floor, not an estimate. |
| Akhmeteli–Gavrilin shell analysis | cited as the structural escape route | `research/papers/akhmeteli-gavrilin-2021-vacuum-balloon.pdf`, concept page | **CITED** | The PDF is present. No note in `research/notes/` yet says what it establishes or where it fails to support the model, which is rule 4 of `research/README.md`. Until that note exists the citation is doing rhetorical work it has not earned. |

### The nitrogen tank and unpowered recovery

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| LN₂ to land a dead empty hull | 144.6 / 1 445.6 / 14 456.1 t | `ledger(cls, 1000).surplusT` | **PHYSICS** | Solid, and the choice to size at the *bottom* of the descent rather than the ceiling is correct and well argued. Ballast sized at the ceiling strands a P-100 at ~2 065 m for ever. |
| `ln2CapT` | 155 / 1 550 / 15 500 t | `CLASSES[*].ln2CapT` | **PHYSICS** (the row above) + **ARBITRARY** margin | The requirement is real and independently motivated. The 7.2% headroom over it is not derived, and the round-number-per-payload result (1.55 payloads exactly) suggests it was chosen for tidiness. `selftest.js` asserts `ln2CapT ≥ needT` — a tautology, since one was set from the other. It can only fail if someone edits one and not the other, which is a useful regression guard and not evidence. |
| LN₂ density | 808 kg/m³ → 192 / 1 921 / 19 207 m³ of tankage | `docs/OPEN-QUESTIONS.md` §0 | **CITED** — nitrogen at its boiling point, 1 atm (~806 kg/m³ in the standard tables) | Solid. The conclusion — tankage is 0.087% of hull volume and therefore free — follows. |
| `eLN2` | 0.45 kWh/kg | `DEFAULTS.eLN2` | **ASSUMED**, dial 0.30–0.80 | Labelled "demonstration assumption, not a plant spec". Industrial nitrogen liquefaction is in this band, but no source is given and none is in the repository. |
| energy to fill the tank | 65 / 651 / 6 505 MWh | `docs/OPEN-QUESTIONS.md` §0 | **PHYSICS** on the two rows above | Solid arithmetic. |
| unpowered recovery, solar only | **2.6 / 5.7 / 12.9 days** | `docs/OPEN-QUESTIONS.md` §0 | **PHYSICS** on an **ARBITRARY** solar figure | The arithmetic reproduces (6 505 MWh ÷ (24 − 3) MW = 310 h). It rests entirely on 200 W/m² applied twenty-four hours a day. The document says so — "a real recovery is several times longer again" — but publishes the optimistic number as the headline. See §1.5. |
| unpowered recovery, rated plant | 0.45 / 0.90 / 2.7 days | same | **PHYSICS** on **ARBITRARY** `cryoMW` | Arithmetic solid; `cryoMW` = 6/30/100 MW has no derivation anywhere. |
| `rtLN2` | 0.50 | `DEFAULTS.rtLN2` | **ASSUMED**, dial 0.35–0.60 | Only constraint is `selftest` requiring it < 1. Moves the P-10000's cycle by ±2.2% and the two smaller classes by nothing at all, because their recovery is discarded (see the energy section). |

### Descent, rotor authority and the anchor

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| `rotorMaxT` | 160 / 791 / 7 600 t | `plan.js`, inverted `diskMW` | **PHYSICS** (momentum theory) on **ASSUMED** inputs | The inversion is exact and round-trips in `tests/cases/sim-physics.cases.js`. Its inputs are `battMW`, `genMW`, `diskM2`, `propEta`, `rhoAir` — four assumptions and one arbitrary constant. |
| the aero-trim share | rotors carry 1/0.6 of their thrust budget | `rotorCapT = rotorMaxT / 0.6` | **ARBITRARY** | Nothing anywhere states why 60%. It is the difference between the descent closing and not closing, and it appears again in `state.js` as the upper end of a hand-drawn `share` schedule. |
| `diskM2` | 2 500 / 12 000 / 160 000 m² | `CLASSES[*].diskM2` | **CIRCULAR** | See §1 and the closing note. Chosen so a force balance closed at the ceiling; the balance now happens at the source, where it does not close (12 666 t of capacity against 13 723 t of hold). The comment asserting it still closes is live in `sim/config.js:230`. Sensitivity today: ±20% moves cycle energy by ∓0.4%. A number reverse-engineered from a result it no longer produces, controlling nothing. |
| `battMW` | 30 / 150 / 1 400 MW | `CLASSES[*].battMW` | **CIRCULAR** | Same origin, same problem, and measurably worse: ±20% moves *every* published figure by 0.0%. |
| hold at the source | 135.6 / 1 366.9 / 13 722.5 t | `ledLow.surplusT − ln2MakeT` | **PHYSICS** | Solid, and its discovery is the best piece of work in the repository: float-up and descent do not share a worst case, and the ceiling ledger was answering both. |
| `anchorBagT` | 125 / 1 250 / 12 400 t | `CLASSES[*].anchorBagT` | **CIRCULAR** (and the 90% is **ARBITRARY**) | The bag is 90.4 / 91.5 / 92.2% of the hold it is then shown to solve. Measured: the bag needed for `retainedT = 0` is 55 t on a P-1000 and **1 099 t** on a P-10000 — 8% of the surplus, not 90%. The other 82% is bought purely to shrink the letdown term. Nothing states a stopping rule, and the choice halves the headline energy. See §1.3. |
| the `min()` in `anchorT` | `min(anchorBagT, holdT)` | `plan.js` | **PHYSICS**, dead branch | The comment calls this "a physical ceiling, not a safety factor". True in principle; never reached in practice, because the bag is always the smaller of the two by construction. |
| `anchorM` | 350 / 600 / 850 m | `CLASSES[*].anchorM` | **ASSUMED**, loosely derived | Justified against `anchorFromAglM` (below) "with margin". The margin is not stated. Sets the winch time floor on `SOURCE_APPROACH`, which does not bind on any class. |
| `anchorFromAglM` | 300 / 500 / 750 m AGL | `plan.js`, 10 m scan | **PHYSICS** | Genuinely computed rather than guessed, and correctly fed back into the flight profile so the ship cannot descend into a band it needs the bag for while still at cruise. Good work. `sim/config.js` quotes 760 and 510 m against the computed 750 and 500 — a 10 m scan-granularity mismatch, cosmetic. |
| anchor pull | 1.2 / 12.3 / **121.6 MN** | `figures.json` | **PHYSICS** — mg | Solid. |
| the cable | 440 mm UHMWPE, 125 t | `sim/config.js`, README | **ASSUMED** | 440 mm at 850 m and ~970 kg/m³ does give 125 t, so the two numbers are consistent. 122 MN over that section is ~800 MPa, which is inside what UHMWPE rope achieves but implies a safety factor around 2 that is never stated. **The 125 t is explicitly not charged as dry mass anywhere** — the project says so, which is the right thing to do with a known omission. |
| `E.anchor` | 0.006 / 0.060 / **0.596 MWh** | `anchorT·g·15/0.85` | **ARBITRARY** | Both constants are unjustified. The 15 m is a fixed lift height applied to bags whose diameters are 6.2 m and 28.7 m — 2.4× the small bag's diameter and 0.52× the large one's — so it cannot be the "lift needed to break the surface" it is described as. The 0.85 winch efficiency has no source. The term is small (1.4% of the P-10000's cycle) but it is the number that makes the whole mechanism look free, quoted as "fifty-eight to one" against the rotor work it removes. |
| `retainedT` | 0 t on every class, mode, distance and wind | `plan.js` | **PHYSICS** — a consequence of the bag row | Honestly reported, and the removal-of-the-anchor test in `tests/cases/sim-plan.cases.js` exercises the live path. Without the anchor: 0 / 48.8 / 1 056.3 t. |
| Bambi bucket precedent | in service since 1983, commercial units near 10 t | README, `config.js`, `PHYSICS.md` | **CITED** in prose, no catalogue entry | The precedent is real and correctly used to say the *principle* is unchanged and the *engineering* is not. The scale ratio is stated three incompatible ways: "This is 1,200" (`config.js`), "the P-10000's is 2,400" (`PHYSICS.md` §11), "240 times the commercial scale" (`OPEN-QUESTIONS.md` §4). The correct figure is ~1 240×. |

**Current rope correction:** the table above is the dated earlier audit. This correction withdraws its earlier diameter and omission claims.

<!-- anchor-rope:basis:start -->
Illustration: the dry-mass budget sizes an assumed UHMWPE cable by minimum break strength, not by diameter. Design load including pickup is bag-water weight under the quasi-static pickup assumption; dynamic snatch, cable self-weight and bag/rigging dry weight are omitted. Required minimum break strength is that load times the safety factor. Assumption: credible safety factor 5; assumption: floor safety factor 3; assumption: demonstrated safety factor 7. Assumption: credible minimum-strength-per-linear-density coefficient 1.5 MN per kg/m; assumption: floor coefficient 2.0 MN per kg/m; assumption: demonstrated coefficient 1.4 MN per kg/m. Those columns do not qualify a rope product. The bottom-up dry-mass budget charges the installed cable, bag and winch. The flight model still assumes dry mass equals payload; it does not integrate that equipment bill. Terminations, wear, creep, cyclic pickup and the bag load path remain unqualified. See `research/analysis/mass-budget.py` and its generated records.
<!-- anchor-rope:basis:end -->

### Rotor and drag relations

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| P_ind = T^1.5/√(2ρA_d) | — | `diskMW()` | **PHYSICS** — ideal actuator-disc momentum theory | Correct as written and correctly labelled an ideal floor. §7 of `PHYSICS.md` states both places it is the wrong formula — hover form at 36 m/s cruise (overstates by 4.5–6.7×), and axial descent (understates by 21–31%) — with numbers. That is a model that knows where it is broken. |
| `propEta` | 0.70 | `DEFAULTS.propEta` | **ASSUMED** | Applied to drag *and* disc power, which are different machines. Largest single tunable effect on energy: −20% → +14.2% on the P-10000. |
| `Cd` | 0.05 on frontal area | `DEFAULTS.Cd` | **ASSUMED**, with a real cross-check | The best-defended assumption in the file: C_dv = 0.024, and a Reynolds/flat-plate estimate puts skin friction at 37% of the assumed total, which is a sane split for a fineness-4 hull. The document then says plainly that it is a *bare hull* figure charging nothing for 14 rotor installations, fins or the hose pod. |
| `rhoAir` | **1.10 kg/m³** for drag and every rotor calculation | `DEFAULTS.rhoAir` | **ARBITRARY** | Described as "a fixed working-band density". There is no such band: the hulls are sized at 0.9569 and fill at 1.0793. `config.js:24`, `PHYSICS.md` §11 and `OPEN-QUESTIONS.md` §1 all state it is "ISA at about 990 m"; it is ISA at **1 107 m** (`altitudeForDensity(1.10)` — run it). The stated consequences, drag overstated 15% and induced power understated 7%, are correct. Measured effect on the P-10000's cycle energy: ±20% → ±10.4%, eight times what `PHYSICS.md` §10 reports. |
| P_drag = ½ρC_dA_f v³/η | 1.06 / 9.16 / 69.68 MW | `dragMW()` | **PHYSICS** on the three rows above | Relation solid, inputs assumed. |
| `downMW` | 0.3 / 5.0 / 52.3 MW | `diskMW(resid·g·0.6)` | **PHYSICS** on **ARBITRARY** inputs (the 0.6, the bag fraction) | The exponent is the whole story and it is real: thrust^1.5 means the last 10% of the hold costs 3.2% of the full rotor power. That is a genuine and well-explained piece of physics. What the rotors are asked to hold is chosen, not derived. |
| disc loading, downwash | 406 N/m², 13.6 m/s induced | `PHYSICS.md` §7 | **PHYSICS** | Solid, and correctly flagged: nothing in the model accounts for a 14 m/s downwash over the fire. |

### Pumping

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| P_pump = ρ_w g Q h/η | 1.96 / 11.77 / 58.86 MW | `pumpMW()` | **PHYSICS** — hydraulic work | Solid, pinned by three tests and by `selftest`. Called "the least contentious number in the model" and that is right. |
| `pumpEta` | 0.75, all-in | `DEFAULTS.pumpEta` | **ASSUMED** | Lumps pump, motor, drive, hose friction and residual kinetic energy. `PHYSICS.md` §5 states the omission that matters: a 1.78 m bore at 15 m³/s, and a 250 m standing column of that bore weighing 625 t that the mass ledger never carries. |
| `hoseM` | 300 m on every class | `CLASSES[*].hoseM` | **ASSUMED** | Good design decision: hose length *is* the fill altitude *is* the pumping head, one number, so they cannot disagree. They previously did. |
| `fillM3s` | 0.5 / 3 / **15 m³/s** | `CLASSES[*].fillM3s` | **ARBITRARY** | No justification anywhere for any of the three. It sets `WATER_FILL` and, since the single-pass change, `WATER_RELEASE` as well — 22.2 of the P-10000's 45.5 cycle minutes, 49% of the cycle. See §1.4. |

### The cycle, phase by phase

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| cycle time | 34.2 / 35.4 / 45.5 min at 15 km | `planCycle().cycleMin` | **PHYSICS** (a sum) on assumed and arbitrary durations | The sum is asserted by test. Every term in it is chosen. |
| `SOURCE_APPROACH` | 2 / 3 / 5 min | `max(1.5·fixed, hoseDeployMin·0.5·hose)` | **ARBITRARY** | `hoseDeployMin` = 4/6/10 and the 0.5 and 1.5 are all unjustified. |
| `WATER_FILL` | 3.33 / 5.56 / 11.11 min | `deliveredT/fill/60` | **PHYSICS** on `fillM3s` | Identity; correctly uses delivered rather than payload. |
| transit legs | 11.76 / 9.63 / 8.14 min | `oneWayKm/gs·60·(1/0.85)` | **PHYSICS** on **ARBITRARY** 15% ramp | The trapezoid correction is right in principle — a leg is not a step — but 15% accelerating and 15% braking is chosen. It inflates every transit leg by 17.6%. |
| `cruiseKph` | 90 / 110 / 130 | `CLASSES[*]` | **ARBITRARY** | Nothing derives them. −20% costs the P-10000 8.2% of throughput and saves 17.8% of energy; +20% buys 6.3% of throughput for 26.5% more energy. |
| `WATER_RELEASE` | 3.33 / 5.56 / 11.11 min | `max(dropKm/(0.45·v)·60, delivered/fill/60)` | **PHYSICS** on `fillM3s`; the 0.45 is **ARBITRARY** and **currently inactive** | Verified: the drop-line term gives 1.78 / 3.03 / 5.13 min against fill-limited 3.33 / 5.56 / 11.11, so the metering rate binds on every class. `dropKm` therefore changes no published figure at all today — ±20% moves energy and throughput by 0.0%, against the ±2.1% / ±6.6% in `PHYSICS.md` §10. |
| `BUOYANCY_ESCAPE` | 2 min | `2 × mode.fixed` | **ARBITRARY** | A round number. |
| `passes` | 1 | literal in `plan.js` | **ASSUMED**, honestly | A literal, correctly described as one. The reasoning for going from three passes to one — an 876 m hull should not reverse over the fire it is dropping on, and the water lands on the same line either way — is sound. |
| `dropKm` | 1.2 / 2.5 / 5 km | `CLASSES[*]` | **ARBITRARY**, currently inert | Bounded above by `dropSeg()` shrinking the line to fit the fire, which is a real constraint; the values themselves are chosen. |
| `VZ_MAX`, `altTop`, the 0.30 climb factor | 6 m/s; `min(1500, 300 + 108·t_short)` | `config.js`, `state.js` | **ARBITRARY** | The *shape* is right — a ship does not climb to 1 500 m on a two-minute hop — and the fix it replaced (a P-1000 diving at 44 m/s) was real. The constants are picked. |
| wind treatment | Wind-triangle timing with track refusal | `sim/wind.js`, `planCycle()` and `power.js` | **PHYSICS** (straight-track wind triangle) on a supplied pressure-level vector | This row is maintained with the current model: crosswind cancellation reduces forward air progress, and a track with no positive ground speed at selected airspeed is refused. The power calculation uses the full air vector. No shear, turns, gusts or vertical air motion are represented. |
| `mode` multipliers | speed 1.15/1.0/0.8, hose, climb, cryoShare, fixed | `MODES` | **ARBITRARY** | Twelve unjustified numbers. A test in `sim-plan.cases.js` says outright that "the mode ordering has flipped five times and is not load-bearing", which is the honest way to carry them. |

### Throughput

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| tonnes per hour | **175 / 1 697 / 13 183 t/h** | `deliveredT·60/cycleMin` | **PHYSICS** — an identity | The identity is trivially correct and asserted by `selftest`. Everything contentious is in `cycleMin`. |
| drops per hour | 1.75 / 1.70 / 1.32 | `60/cycleMin` | **PHYSICS** — an identity | Solid. |
| delivered tonnes | full payload, all classes | `payloadT − retainedT` | **PHYSICS** — a consequence of the anchor bag | True as computed; true only because of a 90% choice with no stopping rule. |
| `bottleneck` | "transit distance" on all three at 15 km | `planCycle()` | computed, on **ARBITRARY** thresholds | The 0.25-payload retention threshold and the 0.92-of-bus `battLimited` threshold are unjustified. Two of the five bottleneck strings (`descent authority`, `descent ballast`) are unreachable on shipped numbers; `cryogenic production rate` fires in endurance mode on a flag that is true in all 135 grid cases and therefore carries no information. |
| fleet allocation rules | tiers at 1 000 / 10 000 ha; `minSourceHa` 10/100/1 000; `searchKm` 25/100/600 | `assign.js`, `CLASSES` | **ARBITRARY** | Six thresholds, no derivation. Monotonicity is tested; the values are not defended. |
| source score | `d / min(12, (area/minHa)^0.35)` | `water.js` | **ARBITRARY** | The exponent, the cap and the discount shape are all chosen. The *principle* — a fleet drawing full payloads from a pond beside a lake is the wrong picture — is sound. |

### The energy budget, line by line — P-10000, balanced, 15 km

Reconstructed from `plan.js` and verified to reproduce `eCycleMWh` exactly.

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| `E.WATER_FILL` | **6.149 MWh** (14.3%) | `max(0, P_pump·t_fill/60 − E_back)` | **PHYSICS** with an **ARBITRARY** clamp | The `max(0, …)` silently destroys energy on the two smaller classes: **0.303 MWh discarded on a P-100 whose entire cycle is 1.308 MWh, and 0.594 MWh on a P-1000**. On those classes the published pumping bill is *zero* — the least contentious number in the model does not appear in their headline energy at all. This is a defect and it is not on the list of six. |
| `E.OUTBOUND_TRANSIT` | 9.459 MWh (22.0%) | `P_drag · t_out/60` | **PHYSICS** | The only energy line charged at full drag. Solid. |
| `E.RETURN_TRANSIT` | **14.705 MWh** (34.2%) | `P_drag × 0.55 × t_ret/60 + E_cryo` | **ARBITRARY** (the 0.55) + **PHYSICS** (E_cryo) | Drag on a streamlined body does not depend on how much water is inside it. The comment "lighter ship, cheaper leg" is not a mechanism at this level of model. The 0.55 removes 4.26 MWh from the P-10000's cycle. |
| — of which E_cryo | 9.502 MWh | `ln2MakeT · eLN2` | **PHYSICS** on inert mass | 22% of the P-10000's published cycle energy is spent liquefying 21.1 t of nitrogen against an 11 051 t requirement. On the P-100 the same term is **54.4% of the whole cycle**. |
| `E.letdown` | **1.420 MWh** (3.3%) | `downMW · min(6, t_ret × 0.2)/60` | **ARBITRARY** — the project's own named defect | Correctly identified, correctly quantified, and now defused rather than fixed: it was 45% of the cycle before the bag. The cap is inactive below ~55 km one-way, so in practice the term is a bare 0.2 fraction. The `battLimited` interaction still runs backwards (a "longer, shallower letdown" *raises* the energy), and is now unreachable, which is worse than broken. |
| `E.anchor` | 0.596 MWh (1.4%) | `m_bag·g·15/0.85` | **ARBITRARY** | See the anchor row. |
| `E.other` | **10.689 MWh** (24.8%) | `P_hotel·t_cycle/60 + P_drag × 0.4 × (approach+escape+release)/60` | **ARBITRARY** ×2 | Hotel load is 2% of `genMW` — 2.276 MWh, 5.3% of the cycle, no derivation. The 0.4 drag multiplier removes a further 12.62 MWh. |
| **the two drag multipliers together** | 0.55 and 0.4 | `plan.js` | **ARBITRARY** | Charging drag at full rate on every phase gives **59.90 MWh instead of 43.02** (+39.2%), and **5.99 kWh/t instead of 4.30**. On the P-1000 it is +23.3%, on the P-100 +13.2%. Two unexplained numbers set 39% of the flagship energy claim. See §1.2. |
| `eCycleMWh` | **1.308 / 6.983 / 43.019 MWh** | sum of the above | **PHYSICS** — a sum, on the rows above | Reproduces exactly. The sum is arithmetic; four of its six terms are gated by unjustified constants. |
| `kwhPerTonne` | **13.08 / 6.98 / 4.30 kWh/t** | `eCycle·1000/deliveredT` | **PHYSICS** — an identity | The headline efficiency claim. The identity is trivial; the numerator is the problem. README nominates "the current 8–17 kWh/t" as the number to attack — that band is itself stale, the model now says 4.3–13.1. |
| integrated `stateAt` draw | 1.23× / 1.81× / **2.83×** the planned budget | `PHYSICS.md` §9, `app/loop.js` | **PHYSICS** — an independent integration of the same quantity, disagreeing | Both numbers ship. The suite carries this as a `knownFail` and reports it live. Honest, unresolved, and it means every energy figure above has a factor-of-three question mark that the project puts on the page. |

### Generation, the deficit and the fleet

| figure | value | where it comes from | rests on | strength |
|---|---|---|---|---|
| solar irradiance | **200 W/m², day and night** | hard-coded in `sim/state.js:351`, `selftest.js:108`, `app/cockpit/panels.js:107`, `3d/model/metadata.js:61`, `3d/physics/energy.js:73`, `3d/adapter/fable.js:201` | **ARBITRARY** | No derivation, no source, no dial, six copies, and — checked — **not in `sim/config.js`**, which the README's table calls the home of "every assumption, in one file". It is a peak-ish figure (≈20% efficiency at 1 000 W/m² insolation) applied continuously. `OPEN-QUESTIONS.md` §0 admits "a real recovery is several times longer again" and then publishes the optimistic figure anyway. |
| `solarM2` | 6 000 / 28 000 / 120 000 m² | `CLASSES[*]` | **ARBITRARY** | Computed against hull geometry: 85.5% / 86.5% / 79.6% of *planform* area. Near-total upper-surface coverage, chosen. |
| solar power | 1.20 / 5.60 / 24.00 MW | `solarM2 × 200/1e6` | **PHYSICS** on the two rows above | Arithmetic solid, inputs arbitrary. |
| per-cycle deficit | **0.62 / 3.68 / 24.81 MWh** | `figures.json` | **PHYSICS** on the budget above | The direction of this conclusion is robust and the project is right to publish it: solar covers 52% / 47% / 42% of spend at best. But it rests on a generation model that omits `genMW` entirely while the same file spends `genMW` on rotor thrust. |
| `genMW` | 8 / 40 / 150 MW | `CLASSES[*]` | **ARBITRARY**, and inconsistently applied | Defect 6, correctly identified as the most consequential item. Measured: removing `genMW` from `rotorMaxT` cuts rotor capacity by 14.6% / 14.6% / 6.6%. Crediting it as energy at full output gives 4.6 / 23.6 / **113.8 MWh** per cycle against spends of 1.31 / 6.98 / 43.02. The generators would cover every cycle on every class. |
| endurance | 18.3 / 19.2 / **61.1 h** at defaults | computed | **PHYSICS** on the deficit | `PHYSICS.md` §9 publishes 29.8 hours and 35.9 cycles for the P-10000 against a 55.67 MWh deficit. The model says 24.81 MWh, 80.6 cycles, 61.1 hours. The published figure is stale by a factor of two. |
| `battMWh` | 20 / 120 / 2 000 MWh | `CLASSES[*]` | **ARBITRARY** | `PHYSICS.md` §3 does the damaging arithmetic itself: at 250 Wh/kg the battery is 80% of the P-10000's entire dry allowance, and the 3D library's own mass split implies 1 430 Wh/kg. The two halves of the project do not agree and the document says so. |
| fleet composition | **16 hulls: 10 / 5 / 1** | `app/fleet.js` `FLEET` | **ARBITRARY** | No sizing argument of any kind. It is a stage set. |
| fleet delivery rate | **18 289 t/h** at seed 7 | sum over allocated missions | **PHYSICS** — a sum | Correctly computed, and correctly *not* published in the README. Note it is 22% below the naive 23 418 t/h you get from multiplying the 15 km class table by hull counts, because the legs the allocator actually produces are longer: Condor flies a 51.9 km leg for a fire 33.2 km from its lake. The 15 km worked example is a favourable case, not a typical one. |
| fires waiting | 34 uncovered at seed 7 | `S.uncovered` | computed on **CITED** live data (BC Wildfire Service) | Solid, and the decision to count and display the uncovered fires is the most honest single choice on the page. |
| fire, perimeter, hotspot, lake, wind and terrain data | — | `DATA-SOURCES.md` | **CITED** — BCWS, NRCan CWFIS, BC Freshwater Atlas (13 646 bodies), Open-Meteo, Mapzen/AWS, Natural Earth, Esri | Exemplary. Licences, exact queries, and per-file provenance sidecars. The Esri basemap is a known unresolved licensing problem and is documented as one. |

### Counts

89 rows. Fourteen carry two categories — a relation that is not in dispute, evaluated on an
input that is — so the two columns below differ: the first counts what each row *leads* with,
the second counts every category the row touches.

| category | leading | touching |
|---|---:|---:|
| PHYSICS | 42 | 43 |
| ARBITRARY | 23 | **32** |
| ASSUMED | 13 | 15 |
| CITED | 7 | 9 |
| CIRCULAR | 4 | 4 |

Two things to read off it.

**PHYSICS leads 42 of 89 rows and that is worth almost nothing on its own.** A PHYSICS row
says the arithmetic is not where to attack; it says nothing about the inputs. Trace any of
them down and it ends in an assumed or arbitrary number within two steps: `tph` is an
identity on `cycleMin`, which is a sum of six durations of which four are chosen; `liftT` is
Archimedes on a displacement set by a bet about structure mass. The honest summary is that
this model has very little arithmetic error and very little evidence.

**There are more than twice as many unjustified constants as stated assumptions.** That is the
finding. The project's whole pitch is that the assumptions live in one file where they can be
read in a sitting and argued with as a set — and they do, and 15 of them are there, dialled
and captioned. The other 32 are buried inside expressions in `plan.js` and `state.js`, never
surfaced, never dialled, never listed. Between them they set roughly 40% of the flagship
energy figure and about a fifth of the cycle time, which is more than everything on the
concept page's slider panel put together.

---

## 1. What is genuinely load-bearing

Ranked by how much of the published output each one controls. Figures are measured, at
defaults, balanced mode, 15 km, by mutating the live model through `setConfig()` and direct
`CLASSES` edits.

### 1.1 The structure allowance: m_dry = m_payload

**Controls: every dimension, every lift figure, the descent problem, the drag, and whether
the concept exists at all.**

This is the one to attack. It is not a sensitivity so much as a load-bearing wall. Required
displacement per tonne of payload is `(1 + k) × 1 000 × 1.05 / ρ_work` for a dry-mass ratio
k = m_dry/m_pay, which at k = 1 is 2 194.7 m³/t and is published as 2 200. Displacement then
sets length, diameter, wetted area, frontal area, drag, the buoyancy surplus, the size of the
descent problem, the size of the anchor bag, the size of the nitrogen tank, and the areal
density the shell would have to achieve.

Measured, re-sizing the P-10000 for other values of k — displacement by (1+k)/2, linear
dimensions by the cube root of that, everything else untouched:

| k = m_dry/m_pay | 0.8 | **1.0 (shipped)** | 1.2 | 1.5 |
|---|---:|---:|---:|---:|
| displacement, m³/t | 1 980 | **2 200** | 2 420 | 2 750 |
| diameter, m | 211.4 | **219.0** | 226.1 | 235.9 |
| cruise drag, MW | 65.0 | **69.7** | 74.3 | 80.9 |
| cycle energy, MWh | 39.98 (−7.1%) | **43.02** | 49.75 (+15.6%) | 63.56 (**+47.7%**) |
| implied shell σ, kg/m² | 17.7 | **20.6** | 23.2 | 26.6 |
| delivered t/h | 13 183 | **13 183** | 13 183 | 13 183 |

Read the energy and σ rows together, because they are the trade nobody has stated. A *more*
generous structure allowance makes the shell problem **easier** — 26.6 kg/m² instead of
20.6 — and costs 48% more energy per cycle. A tighter one makes the flying cheaper and the
hardest unsolved problem in the project harder. The model sits at k = 1 with no argument for
it either way, on the aggressive end of a trade it does not acknowledge exists. Throughput is
untouched throughout, which means this dial is invisible in every headline delivery figure and
decides the entire structural case.

The project already names this as the most likely place to be wrong, and §2 of `PHYSICS.md`
does a genuine job of arguing against itself. What is missing is any evidence *for* it. There
is no mass breakdown in `sim/`, and the only one that exists — `MASS_SHARE` in
`3d/model/metadata.js` — is a set of nine round fractions summing to 1.00 with no derivation,
which the physics document itself shows is inconsistent with any battery chemistry.

### 1.2 The two drag phase multipliers, 0.55 and 0.4

**Controls: 39% of the flagship "kWh per delivered tonne" figure.**

`E.RETURN_TRANSIT` charges drag at 0.55 and `E.other` charges it at 0.4 over the approach,
escape and drop run. Neither has any justification. Charge full drag on every phase the ship
is moving and the P-10000's cycle goes from **43.02 to 59.90 MWh** and its efficiency from
**4.30 to 5.99 kWh/t** — the P-1000 from 6.98 to 8.61, the P-100 from 13.08 to 14.80.

Two unexplained numbers therefore control more of the headline figure than the letdown
constant the project has flagged as a defect, by a factor of twelve. The letdown term is
1.42 MWh; these two remove 16.88 MWh. If only one line in `plan.js` gets fixed, it should not
be `E.letdown`.

There is a defensible physical argument available for a *reduced* return-leg charge — the
ship is trimmed differently and can fly a different profile — but it would have to be made,
and drag on a fixed geometry at a fixed speed does not fall because the tanks are empty.

### 1.3 The anchor bag at 90% of the hold

**Controls: a factor of 2.06 on published cycle energy.**

The bag was introduced to close a 1 056 t descent shortfall. Measured, the smallest bag that
delivers the whole payload is **1 099 t — 8% of the source surplus**. The shipped bag is
12 400 t, 90.2%. Everything between those two points is bought with an unjustified fraction:

| bag, as a fraction of the hold | none | 8% (the minimum that delivers) | 25% | 50% | 75% | **90% (shipped)** | 100% |
|---|---:|---:|---:|---:|---:|---:|---:|
| P-10000 cycle energy, MWh | 86.99 | 88.62 | 71.99 | 58.11 | 47.43 | **43.02** | 41.66 |
| delivered t/h | 12 157 | 13 183 | 13 183 | 13 183 | 13 183 | **13 183** | 13 183 |
| retained as ballast, t | 1 056 | 0 | 0 | 0 | 0 | **0** | 0 |

Throughput is flat from 8% upward. So the delivery claim needs one eleventh of the bag, and
the other 82% is a pure energy optimisation with no stopping rule — the docs justify it with
"rotor power goes as thrust^1.5", which explains *why more is better*, not *why to stop at
90%*. The stated reason for the remaining 10% ("the rotors keeping the last 10% for control
rather than for lift") is not a calculation.

(The first two columns are worth a second look: adding the *minimum* bag makes the cycle
slightly more expensive, not cheaper, because the water that was being retained also shortened
the fill and the drop run. The mechanism only starts paying once the bag is large enough to
take real load off the rotors — which is a good argument for a big bag and is not the argument
the documents make.)

The bag is also the second most sensitive class parameter in the model: −20% costs +12.5% on
the P-10000's cycle energy.

### 1.4 `fillM3s`

**Controls: 49% of the P-10000's cycle time, and therefore of every throughput figure.**

Since the drop became a single metered run, `fillM3s` sets both `WATER_FILL` and
`WATER_RELEASE`: 11.11 + 11.11 minutes of a 45.51-minute cycle. Measured, ±20% moves delivery
by −10.9% / +8.9% and is the only class parameter besides `cruiseKph` that moves throughput at
all. At −20% the P-10000's bottleneck flips to "water handling at the source".

There is no justification anywhere for 0.5, 3 or 15 m³/s. 15 m³/s is a 1.78 m bore at a
plausible in-hose velocity, 58.86 MW of pump shaft power, and — per `PHYSICS.md` §5 — a 625 t
standing water column that the mass ledger does not carry. Halve it and the P-10000's cycle
goes from 45.5 to **67.7 minutes**, delivery falls **32.8%** to 8 858 t/h, and the bottleneck
becomes "water handling at the source".

### 1.5 Solar at 200 W/m², continuous

**Controls: the deficit conclusion, the endurance figures, and the fail-safe recovery claim.**

Solar is the *only* generation term the model credits. It covers 52% / 47% / 42% of each
class's cycle spend, so the per-cycle deficit — the conclusion the project draws in public,
that the fleet needs an energy import chain — is a difference between two numbers of similar
size, one of which is an unsourced constant applied around the clock.

Two directions, and they matter differently:

- **The deficit conclusion is robust.** If 200 W/m² is optimistic, the deficit gets larger and
  the conclusion strengthens. Reading it as a 24-hour mean rather than a peak makes it worse
  by roughly a factor of four.
- **The unpowered-recovery claim is not.** 2.6 / 5.7 / 12.9 days scale inversely with solar,
  and the hotel load is subtracted first. For the P-10000, gross solar is 24 MW and hotel is
  3 MW — so if the true 24-hour mean is below **25 W/m²**, an unpowered P-10000 never recovers
  at all, because it cannot even run its own hotel load. That is a checkable failure boundary
  on a claim described as a safety property, and it is not stated anywhere.

**Honourable mentions**, not in the top five but close: `propEta` (−20% → +14.2% energy),
`cruiseKph` (+20% → +26.5% energy for +6.3% delivery), `rhoAir` (±20% → ±10.4% energy), and
the cryogenic term, which is **54.4% of the P-100's entire published cycle energy** while
every document in the repository describes the plant as doing nothing in the cycle.

---

## 2. What we claim more confidently than the evidence supports

### 2.1 Retained descent ballast, on the concept page

> "One refinement the monitor applies: when tanks and rotors together cannot cover a ship's
> post-drop buoyancy, the Mind retains part of the payload as descent ballast and only the
> rest counts as delivered — **on the largest class that retention is substantial, and
> cryogenic capacity becomes the visible constraint**." — `concept/index.html:957–960`

`retainedT` is 0 on every class, mode, distance and wind in the grid, and `selftest.js`
enforces that it is. Cryogenic capacity is the visible constraint nowhere. For this sentence
to be true the anchor would have to be removed, at which point the P-10000 retains 1 056 t and
the sentence becomes true — but then the published throughput is 12 157 t/h, not 13 183.

The README lists this defect for the *model*; the sentence survives on the page.

### 2.2 The dials that "materially move the answer"

> "Both are demonstration assumptions, not specifications for an airborne plant, and **both
> are dials above precisely because they materially move the answer**." — `concept/index.html:999`

Measured, `eLN2` ±20% moves cycle energy by **0.0% on every class** and throughput by nothing.
The reason is structural: `ln2MakeT` is cryo-rate-limited and therefore inversely proportional
to `eLN2`, so `E_cryo = m·e_LN2` is invariant. `rtLN2` moves the P-10000 by ±2.2% and the two
smaller classes by 0.0%, because their recovery is clamped away by `max(0, …)`.

For this claim to be true the plant would have to be tank-limited rather than rate-limited,
which it is in no combination on the 135-case grid.

The neighbouring sentence — "In endurance mode the cryogenic plant is usually the cycle's
bottleneck" (`concept/index.html:1000`) — is true as a *string*: `bottleneck` does return
"cryogenic production rate" in endurance mode. It is false as a *constraint*: `cryoLimited` is
true in all 135 cases, so the flag distinguishes nothing, and the plant changes no delivered
tonne anywhere.

### 2.3 "The force balance closes with nothing held back"

> "`diskM2` and `battMW` are **sized so the force balance closes with NOTHING held back**…
> The descent check is still made at the ceiling; see docs/OPEN-QUESTIONS.md #4 for why the
> bottom of the letdown is the harder case." — `sim/config.js:230`

The descent check is no longer made at the ceiling — that was fixed the same day — and at the
altitude it is now made, the balance does not close: `rotorMaxT/0.6` is 12 666 t against a
13 723 t hold. Remove the anchor and the P-10000 retains 1 056 t while running its rotors at
exactly 100% of bus.

`PHYSICS.md` §7 carries the same claim in weakened form ("still survives only under the hover
formula, but it is one class and one and a half percent away from surviving properly") and
computes its descent-power table against the *ceiling* surplus — 0.6 × 11 051 = 6 631 t. The
code works from 0.6 × 13 723 = 8 233 t, which under the same hover formula costs 1 748 MW
against a 1 550 MW bus. The margin is not 1.5%; there is no margin.

For the claim to be true, either the disc area and battery peak must be re-sized against the
source-altitude balance, or the sentence must be replaced with the truth, which is that the
descent closes because of a bag of lake water.

### 2.4 "Every assumption, in one file"

> "| Every assumption, in one file | `DEFAULTS`, `CLASSES`, `MODES` | `sim/config.js` |" — `README.md:59`

200 W/m² of solar irradiance is not in `sim/config.js`. It is hard-coded in six places across
`sim/`, `app/` and `3d/`. It is the sole generation term in the model and the basis of the
deficit conclusion and the fail-safe recovery figures.

The claim is nearly true and is worth making true. The boundary linter that enforces the
`sim/` purity rule — which genuinely works and has its own test suite — would be the natural
place to enforce it.

### 2.5 "Each with a test that fails on purpose"

> "The other five are awaiting implementation, **each with a test that fails on purpose**." — `README.md:103`

`make test` reports 2 known-failing tests. One is Defect 2. The other is an unrelated
`windUsed` flag bug. So of the five open defects, exactly one has a test that fails on
purpose. `OPEN-QUESTIONS.md` says three markers remain in one paragraph and records the third
coming off in another. The situation is defensible — the document explains why Defects 4, 5
and 6 *cannot* have failing tests — but the README sentence is not.

### 2.6 The stale figures

Published numbers that the model no longer produces. All re-run at defaults on 2026-08-09.

| where | published | model says | note |
|---|---|---|---|
| `PHYSICS.md` §5, `concept/index.html:608,968` | 250 m head, P-100 pump 1.635 MW | 300 m, **1.962 MW** | `PHYSICS.md`'s own notation table says 300 m. The page still says "pump pods on 250 m hoses". |
| `PHYSICS.md` §9 budget table | total 45.218 MWh | **43.019** | Two rows moved after the table was written. |
| `PHYSICS.md` §11 Defect 3 | letdown 34.20 MWh, **45.2%** of the cycle | **1.420 MWh, 3.3%** | §9 of the same document gives 1.420. The document contradicts itself by a factor of 24. |
| `PHYSICS.md` §9 | P-10000 endurance 29.8 h, 35.9 cycles, 55.67 MWh deficit | **61.1 h, 80.6 cycles, 24.81 MWh** | Stale by 2×. |
| `PHYSICS.md` §10 sensitivity | `rhoAir` ±20% → −1.3%/+2.7%; `dropKm` ±20% → ∓2.1% energy, ±6.6% t/h; `diskM2` −20% → +5.3%; `battMW` −20% → +6.3%; `rhoSL` −20% → −23.2% | **−10.3%/+10.4%; 0.0%/0.0%; +0.4%; 0.0%; −3.7%** | The whole table predates the single-pass drop and the anchor. `dropKm` and `battMW` now move nothing. |
| `README.md:75` | "The pass count is 3 for every one of the 135 combinations" | `passes` = **1** in all 151 golden entries | `passes` is now a literal. |
| `README.md:273` | "The current 8–17 kWh/t is the number to attack" | **4.30–13.08 kWh/t** | |
| `plan.js:159`, `config.js:158–159` | anchor costs "0.04 MWh against a 75 MWh cycle" | **0.596 MWh against 43.02** | The comment describes the 1 056 t bag, not the shipped 12 400 t one. |
| `config.js:176`, `PHYSICS.md` §11, `OPEN-QUESTIONS.md` §4 | Bambi scale "1,200" / "2,400" / "240 times" | **~1 240×** | Three documents, three numbers, one of them right. |
| `config.js:24`, `PHYSICS.md` §11, `OPEN-QUESTIONS.md` §1 | ρ_air 1.10 is "ISA at about 990 m" | **1 107 m** | ISA at 990 m is 1.1127. Run `altitudeForDensity(1.10)`. |
| `PHYSICS.md` §4, last paragraph | "Delivered per hour is 10% below the figure this page carried an hour earlier" | delivery is back to full | Describes the state between the descent fix and the anchor. |

`research/README.md` rule 1 exists precisely to stop this: "no report may contain a figure
that was typed by hand." The rule is applied to `research/reports/` and not to `docs/`, where
every one of the figures above is hand-typed. `docs/PHYSICS.md` is the document a hostile
reviewer will read first, and it currently contradicts itself within four sections.

### 2.7 Fail-safe float-up is conditional on two release mechanisms

> "A hull must be positively buoyant at `WORK_ALT_MSL` while fully loaded with water AND
> UNABLE TO DROP IT. A ship whose outlets jam must rise, not sink." — `sim/config.js:123`

The ledger that checks this excludes nitrogen ("LN2 ballast vents to atmosphere in seconds")
and excludes the anchor bag. A P-100 at 2 500 m with a full water load *and* a full nitrogen
tank masses 355 t against 210.5 t of lift. A P-10000 that cannot release its bag is holding
12 400 t against an 11 051 t surplus.

So the fail-safe property holds against one jammed mechanism (the water outlets) and fails
against either of the other two. That is a defensible design position — the vent and the bag
release are simpler devices than a payload dump — but it is a *conditional* safety claim
presented as an unconditional one, and the condition is not stated on the page.

---

## 3. What is missing

Numbers the project uses but never derives or cites.

1. **200 W/m² of solar irradiance.** The sole generation term. No source, no dial, six copies,
   and not in the assumptions file. A day-night average for the BC interior in fire season,
   at a stated panel efficiency, would take an afternoon and would move the recovery figures
   by a factor of several.

2. **`fillM3s` — 0.5, 3, 15 m³/s.** Sets half the cycle time. No pump is named, no bore is
   sized in `sim/`, no NPSH or hose-friction budget exists. The 1.78 m bore and 625 t standing
   column appear only as a caveat in `PHYSICS.md` §5.

3. **`cruiseKph` — 90, 110, 130.** No power-versus-speed optimum is computed, which is odd
   given that `dragMW` is right there and cubed.

4. **The 0.55 and 0.4 drag multipliers, the 0.6 aero-trim share, the 2% hotel load, the 15 m
   anchor lift, the 0.85 winch efficiency, the 15% transit ramp, the 0.45 drop-speed fraction,
   the 0.8 nitrogen target fraction, the simulator wind clamps recorded on 2026-08-09 (0.35–1.8×), the 0.92 bus threshold, the
   1.12 authority stretch, the 0.25 retention threshold.** Thirteen free constants in one file.
   Between them they set roughly 40% of the published energy and about a fifth of the cycle
   time.

5. **A mass budget.** The dry allowance is a single number equal to the payload. What is
   inside it is never enumerated in `sim/`. The only breakdown that exists is nine round
   fractions in `3d/model/metadata.js` which `PHYSICS.md` §3 shows to be inconsistent with any
   battery chemistry. Specifically uncharged: the anchor cable (125 t on a P-10000, stated),
   the standing water column in the hose (625 t, stated), the hose itself, the bag, the winch,
   the rotor installations, and the pump pod.

6. **Any suppression or comparison baseline.** README nominates kWh per delivered tonne as the
   number to attack "against real suppression logistics, not against nothing" — and the
   repository contains no figure for what a CL-415, a DC-10 tanker or a ground crew achieves
   per tonne delivered. Without one, 4.3 kWh/t is a number with nothing to be better or worse
   than. This is the single most valuable missing citation in the project.

7. **Cost, in any form.** Stated as out of scope in `PHYSICS.md` §12, which is legitimate. It
   is worth noting that it means the concept cannot currently be argued against on the axis
   most reviewers will reach for first.

8. **Rotor hardware.** 160 000 m² across 14 units is 120.6 m per disc at 9.7 kW/m², against
   about 0.4 kW/m² for an offshore wind turbine of the same diameter. `PHYSICS.md` §3 states
   this and states that the 3D library resolves the same area as 28 discs of 85 m. Nothing
   reconciles them, and no blade loading, tip Mach number or solidity is computed.

9. **`research/sources.json` itself.** As of this writing the catalogue does not exist, so no
   CITED row in the table above can be resolved to a licence, a DOI or a statement of what the
   project takes from the source. `research/papers/` held one PDF and `research/notes/` was
   empty when this was written, so rule 4 — a note written from the source, saying where it
   does *not* support what we would like it to — was unsatisfied for every citation in the
   project. That is the gap this folder exists to close, and it is the reason no row above
   could be marked CITED on the strength of a filename.

---

## The single worst circularity

**`diskM2` and `battMW` were reverse-engineered from a descent force balance the model no
longer performs, were not updated when the balance moved, and are still published as evidence
that the descent closes.**

The chain:

1. The hull is sized so it floats when full. That makes it violently buoyant when empty —
   13 723 t of surplus on a P-10000, at the lake.
2. Rotor disc area and battery peak power were then chosen so that `rotorMaxT/0.6` exceeded
   that surplus, "so the force balance closes with NOTHING held back". 160 000 m² and 1 400 MW
   are not engineering estimates; they are the values that made the inequality true.
3. On 2026-08-09 the balance correctly moved from the ceiling to the source, where the air is
   16% denser. The surplus grew by 24%. `diskM2` and `battMW` did not change.
4. The inequality is now false — 12 666 t of capacity against 13 723 t of hold — and the
   descent is closed instead by a bag of lake water whose size was itself chosen as 90% of
   that same hold.
5. `sim/config.js:230` still asserts the closure, and `PHYSICS.md` §7 still calls it "the
   model's central structural boast", computing its supporting table against the superseded
   ceiling ledger and reporting a 1.5% shortfall where the code's own numbers give 1 748 MW
   against a 1 550 MW bus.
6. Measured today, `diskM2` ±20% moves cycle energy by ∓0.4% and `battMW` ±20% moves every
   published figure by 0.0%.

So two of the most striking numbers on the class cards — 160 000 m² of rotor disc, 1 400 MW of
battery peak — exist to satisfy a constraint that no longer binds, and are cited as proof of a
property the model does not have. Nothing in the output would change if they were deleted.

That is worse than the letdown constant the project has flagged, and worse than the retention
copy on the concept page, because both of those are *dead* claims that a reader can check
against a zero. This one is a *live* claim, supported by a table, in the document the project
offers as its derivation.

---

## What holds up

Stated plainly, because a hostile-but-fair reviewer should know where not to spend effort.

- **The atmosphere module.** Sourced constants, cross-checked against the published table,
  throws rather than extrapolates, pure. It is the only part of the model with no free
  parameters of its own — its single input, ρ_SL, is the ISA value.
- **The vacuum-shell argument in `PHYSICS.md` §2.** A correct derivation that concludes the
  best material available is short by a factor of six, published in the project's own physics
  document. Very few concept papers argue against themselves this well.
- **The two-ledger insight.** Recognising that float-up and descent have different worst cases
  and are separated by 1 200 m of atmosphere is the best piece of modelling in the repository,
  and `anchorFromAglM` — computing the altitude at which the rotors lose the argument, and
  then constraining the flight profile to respect it — is exactly right.
- **The thrust^1.5 leverage.** The reason the bag is worth so much is real physics, correctly
  identified, correctly quantified.
- **The data provenance.** `DATA-SOURCES.md` is better than most published research.
- **The boundary linter, `selftest()` and the golden grid.** A guard with its own test suite,
  assertions that ship to the reader's browser, and a 135-case grid. The infrastructure for
  checking this project is genuinely present, which is why an audit like this one could be
  done in an afternoon.

The claim the project actually makes — that the arithmetic is checkable and the assumptions
are visible — survives. What this map adds is that the assumptions are not the only thing
driving the numbers: a comparable amount of the output is set by constants that were never
assumptions at all, because nobody ever decided them out loud.
