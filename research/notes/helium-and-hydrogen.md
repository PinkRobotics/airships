# Helium and hydrogen — the sources behind the gas ledger

The source record behind `research/analysis/helium.py` and `helium.md`, the round that finally
wrote down why this is not a helium project. Three USGS Mineral Commodity Summaries helium
chapters were downloaded, read against their own pages, and stored in `papers/` (public domain).
Everything else the comparison leans on is catalogued and not hosted — and some of it has not
been read at all, which this note labels rather than hides. Tags: **MEASURED** (read from a
primary source this round), **DATASHEET** (curated secondary, fetched), **OOM**
(order-of-magnitude, quoted secondhand, or remembered). Numbers computed for this note are
marked [calc].

The physics half of the ledger needs no external source: gas densities are ideal-gas arithmetic
on the US Standard Atmosphere at 2,500 m (`notes/noaa-1976-us-standard-atmosphere.md`), and the
structure rows come from `research/analysis/vacuum-cell.json`. What this note documents is the
market half, the historical half, and the places where the published comparison currently
outruns its sources.

## USGS Mineral Commodity Summaries, helium chapters — 2022, 2024, 2025 (MEASURED)

`papers/usgs-mcs-2022-helium.pdf`, `usgs-mcs-2024-helium.pdf`, `usgs-mcs-2025-helium.pdf`.

### What they establish

- **The repricing.** Estimated Grade-A base price $7.57/m³ ($210/Mcf) in 2021 (MCS 2022) →
  about $14/m³ ($390/Mcf) in 2023 (MCS 2024), holding through 2024 (MCS 2025). **+85% in two
  years**, and that is the *base* price: 2022 and 2024 say "with some producers posting
  surcharges to this price", 2025 says "with producers posting surcharges".
- **The federal buffer is gone.** The Federal Helium System — Cliffside Field reservoir,
  pipeline, and about 50 Mm³ of crude helium (Lot 1 ≈ 28, Lot 2 ≈ 22) — was sold in two lots on
  2024-01-25, both to one company, and transferred 2024-06-27. The CHEU purification unit was
  not part of the sale; its lease lapsed 2024-08-11 and no new agreement had been reached by
  the end of 2024, a court letting the new owner operate in the meantime (MCS 2025). The path
  there: management moved from BLM to GSA on 2022-12-03, a lawsuit to stop the sale was filed
  2023-09-07 and rejected 2023-11-02 (MCS 2024).
- **Geopolitics.** EU sanctions adopted 2024-06-25 banned imports of Russian helium effective
  2024-09-26. Russia produced 17 Mm³ in 2024 — third behind the US (81) and Qatar (64) — and
  holds the world's third resource at 6.8 Bm³. US import sources 2020–23: Qatar 40%, Canada
  36%, Algeria 10%, Russia 4% (MCS 2025).
- **Scale.** 2024 world production ≈ 180 Mm³; US apparent consumption 56 Mm³, of which
  **lifting gas is 18%** (16% of 59 Mm³ in 2023 — the share moves year to year).
- **Grades.** Grade-A is ≥ 99.997% helium; commercial "gaseous helium" is generally > 98%.
- **The substitution sentence**, in USGS's own words in both 2022 and 2025: hydrogen "can be
  substituted for helium in some lighter-than-air applications in which the flammable nature
  of hydrogen is not objectionable."

### What this project takes

Every market constant in `helium.py`: the two prices, US consumption, world production, the
lifting-gas share. The per-ship and fleet arithmetic is ours [calc], on the project's V =
220,000 m³ and A = 22,592 m²: one fill ≈ 171,844 std m³ ≈ $2.4M at the 2024 base price;
100 ships ≈ 17.2 Mm³ of inventory ≈ **31% of US apparent consumption and 10% of one year's
world production**. The conclusion the analysis draws — helium is cheap per ship and dangerous
per fleet — leans on these chapters and on nothing else that has been read.

### Where they do not support us

- **The "90-year federal buffer" in `helium.md` is not in any MCS chapter.** No chapter dates
  the program. The usual anchor is the Helium Act of 1925, which would make it closer to 99
  years — but that is memory (OOM), not a read source. As published, the age is unsourced.
- **The fleet comparison divides a stock by a flow.** 17.2 Mm³ is inventory held once, not an
  annual purchase; make-up, not the fill, is the recurring draw. The 31% figure is honest as a
  statement of what filling a fleet would take out of one year's supply, and should not be
  read as an annual burden.
- **The consumption denominator is itself an estimate.** MCS 2025's own footnote: USGS
  estimated 2024 apparent consumption because Census Bureau export data "were unusually high
  and may have contained misclassified items." 2024 production figures carry the 'e' flag too.
- **Nothing in the MCS predicts prices or market response.** "A 100-ship program is not a
  price-taker" is our inference from the size ratio, not a USGS statement.
- **The prices are US prices.** A BC-based fleet would buy into the Canadian supply picture —
  Canada was 36% of US imports and brought three new facilities online in 2024 — and the MCS
  says nothing about Canadian domestic pricing or availability.

## Hunt et al. 2019 — read as author manuscript; catalogued, not hosted

*Using the jet stream for sustainable airship and balloon transportation of cargo and
hydrogen*, Energy Conversion and Management: X 3, 100016, DOI 10.1016/j.ecmx.2019.100016.

**What it establishes.** A serious, peer-reviewed proposal for hydrogen-filled airships and
balloons riding the jet stream at 10–20 km to move cargo and hydrogen. On safety it is blunt:
around 90% of reported hydrogen-airship accidents involved fire, and the paper's mitigation is
operational — "if airship transportation, unloading and loading were to be performed
autonomously, airship ports located in isolated areas and they were not allowed to pass above
large cities at low altitudes, the risk of fatalities with hydrogen airships would reduce
considerably." That is the uncrewed-hydrogen competitor `helium.md` calls the open flank,
standing in the literature since 2019 (MEASURED, from the manuscript described below).

**Why it is not in `papers/`.** Crossref records the version of record as CC BY 4.0 and the
journal is gold open access — but the VoR PDF could not be fetched this round (ScienceDirect
refuses unauthenticated downloads; the round's earlier fetch saved a zero-byte file). The only
obtainable copy is the Manchester Metropolitan University repository's author deposit, whose
repository record is labelled CC BY 4.0 but whose own pages carry **no licence line** and whose
author list (five named) differs from the VoR's seven. Rule 3 wants the item's own licence
line; a hosted file we cannot match line-for-line to the DOI we cite fails that test. Catalogue
only until the VoR is in hand.

**Where it does not support us.** It is a cargo-transport study, not a firefighting one: the
mission is downwind transit at 10–20 km, not station-keeping at 2.5 km over a convective
column. Its safety argument works by *isolation* — autonomous ports, remote sites, no
overflight — precisely the levers a fire ship gives up by design. And it does not touch
certification. It establishes that uncrewed hydrogen is proposed in earnest; it does not
establish that it is viable at a wildfire, and neither side of that question has been costed
by this project.

## The historical gas-ship ledger — airships.net (DATASHEET, single-source)

The demonstrated dead-weight numbers in `helium.py` — *Hindenburg* 200,000 m³ and 118 t empty
(0.590 kg/m³ of volume, 49% useful on hydrogen), the same LZ-126 hull at 57% useful on
hydrogen for its delivery flight but 41% as USS *Los Angeles* on helium, the 90–95% inflation
practice, the water-recovery gear US helium ships carried to avoid venting — all come from one
curated secondary, Dan Grossman's airships.net. **The audit flags every one of these as
single-sourced**, and they are; before the useful-fraction comparison hardens, they should be
re-based to primary references (Burgess's *Airship Design*, the Navy's ZR-3 records). Not
redistributable; catalogued only.

The comparison uses an unbuilt level-2 M60J hierarchy formula, not a drawn hull.
At structural safety factor 1.5 against full sea-level pressure, its density margin is 0.6867 kg/m³ at sea level and 0.4186 kg/m³ at 2,500 m.
It assumes local-wall knockdown 0.30 and node mass 15%; material properties, joint mass, film convention and a drawn, tested structure remain unverified.
Comparing that formula with the historical 49%/41% useful fractions remains arithmetic on unequal evidence: 1930s duralumin and cotton against a target laminate.
The number a modern helium rigid would achieve, **0.3–0.45 kg/m³ in the draft, is an invented
OOM guess** (audit: invented); no modern transport-scale rigid exists to measure, and nothing
published by LTA Research yet fills the gap.

## The numbers the comparison still owes

Carried from the audit, each labelled where it is used:

- **FAA-P-8110-2's non-flammable lifting-gas requirement — cited from memory, still.** Two
  more fetch attempts this round failed. It is the only regulatory fact standing between the
  project's justification and the uncrewed-hydrogen competitor, and nobody on this project has
  read it. Not catalogued in `sources.json`, deliberately: we could not verify so much as its
  date this round, and cataloguing a document from memory is how citations get laundered.
- **The ~1 L/m²/day envelope permeability spec** (Liao & Pasternak 2009, Prog. Aerospace Sci.
  45:83–96 — paywalled, quoted secondhand, OOM until read). It drives the make-up estimate of
  3.7%/yr ≈ $90k/yr [calc]. Note which way it cuts: this figure powers the *concession* that
  helium is cheap per ship. If the true spec is worse, the helium case weakens, not ours.
- **Hydrogen at $1–7/kg** — standard grey-to-green range, OOM, not pinned to a current IEA or
  DOE document. Only the "20–150× cheaper than helium" contrast leans on it.
- **The LN₂ ballast plant at 12–120 t** — the project's self-declared worst-sourced mass
  number, repeated in this comparison because buoyancy control is the section the gas ships
  win; researched by nobody this round.
- **97% operating purity** costing 3% of net lift — the purity grades are USGS (MEASURED); the
  choice of 97% as the operating point is a project assumption [calc], loosely anchored to the
  90–95% inflation practice (airships.net, DATASHEET).
- Buoyancy-control context from the draft — Aeroscraft COSH compression (prototype-scale only,
  never at transport scale), Zeppelin NT's 1.10 kg/m³ dead weight, the *Hindenburg*'s
  designed-for-helium history — is Wikipedia-derived (DATASHEET) and was left out of
  `helium.md`'s generated claims; treat it as colour, not evidence, until sourced primary.

## Corrections this integration made to the draft

1. **"Break-even 0.067 kg/m³ is six times below the fourth hierarchy level" is wrong
   arithmetic.** 0.067 is 2.5× below level 4 (0.169 kg/m³) and 3.7× below level 3 (0.245); the
   6.4× multiple belongs to the level-2 *target* (0.428). The sentence appears in
   `research/README.md`, the `helium.py` docstring, and `helium.md`. The verdict — vacuum
   never wins on lift, at any level — is unchanged; the multiple should be fixed where it
   appears.
2. **Make-up: 3.7%/yr ≈ $90k/yr, not the draft's ~5%/yr ≈ $115k/yr.** The draft priced
   altitude-m³ as standard m³. `helium.py` computes the right number ($90k) but its own prose
   string still says "~$115k/yr" — a leftover from the draft that should be reconciled the
   next time the analysis is touched.
3. **Import-share attribution.** The Qatar-40/Canada-36 window (2020–23) is MCS 2025's; MCS
   2022's window (2017–20) reads Qatar 65%, Algeria 12%, Canada 11%, Portugal 7%. The draft's
   source table credited "import shares" to MCS 2022.
4. **The surcharge quote** is "with **some** producers posting surcharges" in MCS 2022 and
   2024; only MCS 2025 drops the "some".
5. **The "90-year" buffer age** is not in the USGS chapters (see above) and rides unsourced in
   `helium.md`.

## What this note holds up, and what it does not

The strong claims survive contact with the primary source: the +85% repricing, the loss of the
federal system to a single private buyer, the EU ban, lifting gas at 18% of US use, and the
USGS's own sentence conceding hydrogen substitution where flammability "is not objectionable"
— all MEASURED. The per-ship concession (fill and make-up are rounding errors) and the
fleet-scale warning (31% of a year's US consumption held as inventory) are our arithmetic on
those measured numbers. What is *not* yet supported: every historical dead-weight figure
(single secondary), the envelope-loss rate (secondhand OOM), the regulatory wall against
hydrogen (memory), and the modern-rigid strawman (invented). The comparison's conclusion does
not currently depend on any of the unsupported four — but the hydrogen flank does, and it
stays open until FAA-P-8110-2 is read and an uncrewed hydrogen fire ship is costed honestly.
