# Prior art — cellular and multi-cell vacuum lighter-than-air structures

*Topic note, 2026-08-10. Written from a research round with web access, then re-verified during
integration against what that round actually saved: Google Patents index fetches (JSON), a
Crossref result set, and the three primary PDFs already in `papers/`. Tags: **[read]** — the
document itself was read; **[biblio]** — bibliographic record verified (Crossref or the Google
Patents index), claims not read; **[secondary]** — known only through an encyclopedia or press
description; **[not re-verified]** — asserted by the research agent from a page that could not
be re-fetched during integration. Method limits are part of the finding and are stated in §5.*

## 1. Two corrections before anything else

**US 11,447,226 B1 is not Akhmeteli & Gavrilin, and it is not a vacuum patent.** The Google
Patents record [biblio] gives: "Lighter than air balloon systems and methods", first-named
inventor Rodger Farley, assignee World View Enterprises Inc., granted 2022-09-20 — a
zero-pressure gas lift balloon paired with a multi-chamber super-pressure air-ballast balloon.
Any project text attributing this number to Akhmeteli & Gavrilin, or citing it as vacuum-lift
prior art, is wrong on inventor, subject and kind code and must change. (The research round's
draft named four inventors; only Farley appears in the retained fetch, so only Farley is
asserted here.)

**What Akhmeteli & Gavrilin actually hold is two published applications, not a granted
patent.** The Google Patents index [biblio] returns exactly two items under Akhmeteli:
US 2006/0038062 A1 (published 2006-02-23) and US 2007/0001053 A1 (published 2007-01-04), both
"Layered shell vacuum balloons", both with no grant date. Their own 2021 paper [read — in
`papers/`] cites only application serial 11/517,915 (filed 2006-09-08), which is consistent.
Cite them as *applications*.

## 2. The historical line

Francesco Lana de Terzi's *Prodromo* (Brescia, 1670, ch. 6) proposed four evacuated copper
spheres lifting a boat — the first quantitative LTA proposal, and wrong for the reason that has
killed every successor: a wall thin enough to float buckles [read: analysed in Akhmeteli &
Gavrilin 2021 ref. 1 and Metlen 2013 §1.2]. Arthur De Bausset raised money in 1880s Chicago for
a "vacuum-tube" airship and had his application denied as wholly theoretical [secondary:
Wikipedia "Vacuum airship"]. Lavanda Armstrong patented a honeycomb-cellular wall with a
pressurised envelope around a vacuum core in 1921 — US 1,390,745, granted 1921-09-13 [biblio:
number and date verified from A&G 2021 ref. 8; claims not read]. Emmanuel Bliamptis added
inflatable strut rings in 1985 (US 4,534,525) and David Noel (1983) a geodesic double balloon
with pressurised air between skins [secondary: Wikipedia only — the Bliamptis number has not
been checked against any primary and is deliberately not catalogued]. The Journal of the
American Society for Naval Engineers was reviewing "The Vacuum Airship" in 1922
(doi:10.1111/j.1559-3584.1922.tb04969.x) [biblio: Crossref]. Nothing in the line was built and
flown, and the failure is always the same: the wall that must not buckle masses more than the
air it displaces, and every fix either leaves the exponent alone or pays for stability with gas
that costs lift.

## 3. The patent record

| Patent | Year | Architecture | Status / what we checked |
|---|---|---|---|
| US 1,390,745, L. M. Armstrong | 1921 | Vacuum core inside a pressurised envelope with honeycomb cellular wall — the first cellular wall in the record | Granted [biblio via A&G ref. 8]. Its cells hold *air*, not vacuum |
| US 4,534,525, E. Bliamptis | 1985 | Vacuum LTA with inflatable strut rings | [secondary: Wikipedia only — verify before the page cites it] |
| US 2006/0038062 A1 + US 2007/0001053 A1, Akhmeteli & Gavrilin | 2006–07 | Layered (sandwich) shell vacuum balloon — the escape their own impossibility proof demands | **Applications only** [biblio: Google Patents index]. The peer-reviewed version is the 2021 *Eng* paper we host |
| US 7,708,161 B2, S. A. Barton (FSU Research Foundation), "Light-Weight Vacuum Chamber and Applications Thereof" | 2010 | Array of internally *pressurised* thin-walled cells stabilising a central vacuum; walls in tension | Granted 2010-05-04 [biblio: A&G ref. 9]. The only prior cellular vacuum boundary — and its cells are pressurised, so the stabilising gas is paid for in both mass and lift |
| US 9,016,622 B1, I. Pasternak | 2015 | Constant-volume variable buoyancy by compressing the lifting gas (Aeroscraft COSH) | Granted 2015-04-28 [biblio: Google Patents index]. Not vacuum lift; kept because our air-ballast retraction touches it |
| US appl. 14/807,118, Rapport & Middleton | 2015 | "Lighter-Than-Air Fractal Tensegrity Structures" | [biblio: A&G ref. 12; not read]. The hierarchy instinct, unclosed |
| EP 3,480,106 A1, L. Turinetti | 2019 | Ellipsoid assembled from ≥32 hollow pentagon/hexagon elements held by external pressure, Roman-arch style | No longer active (Google Patents family state NOT_ACTIVE [biblio]; the round recorded it as withdrawn [not re-verified]). Elements share faces but the vacuum is one volume behind one valve — no cell-level sealing |
| CN 202966650 U / CN 102910279 A; CN 106347620 A; CN 113277058 A | 2013–21 | Assorted vacuum-airship utility models | [biblio: index only]. Existence proof of an active Chinese filing line; none read |
| US 11,447,226 B1, R. Farley (World View) | 2022 | Tandem gas balloon + multi-chamber super-pressure air ballast | Granted 2022-09-20 [biblio]. **The misattributed number — see §1. Not vacuum prior art** |
| US 11,679,856 B2, K. M. Hobson (Overallsky Inc.), "Airship with vacuum based lift methodology" | 2023 | Multiple rigid static vacuum chambers plus expandable "dynamic" vacuum chambers in a frame; trim chambers | Granted 2023-06-20 [biblio: index + claims snippet]. The only granted multi-chamber vacuum-lift airship patent found. The round's further detail (welded steel construction, 600-ft chambers) is [not re-verified]. Its chambers are independent tanks: every chamber wall carries the full atmosphere everywhere |
| US 2024/0017811 A1, I. Toli | 2024 | Vacuum airship, geodesic frame with unbonded or single-point-bonded skin | Filed 2022-07-16, published 2024-01-18 [biblio: index + claims snippet]. Application; unread. His peer-reviewed analysis is already catalogued (`toli-2026-kenemostat`) and also unread — see §6 |
| US 12,091,150 B2 (+ US 2023/0141407 A1), J. W. van Egmond | 2024 | "Low-density structured materials" — interconnected polyhedrons, tetrahedral arrangements, mechanical stability at low density | Granted 2024-09-17 [biblio: index + abstract snippet]. **Unread, and the single most important unread item in this note** — the title and abstract point at exactly a structured low-density material, and until someone reads the claims, no novelty language about "evacuated cellular material" may ship |

Patent-sweep coverage: the Google Patents search endpoint reported 36 results for "vacuum
airship" and 205 for "vacuum balloon" (retained fetches hold the first pages, which contain
every vacuum-LTA-relevant item the round identified); the page endpoint began returning 503
mid-session, so several rows above are index-record-only, as tagged.

## 4. The academic record

**The impossibility proof and the sandwich escape** — Akhmeteli & Gavrilin, *Eng* 2(4), 2021,
CC BY [read — in `papers/`]: a homogeneous single-layer evacuated sphere is impossible for any
solid at any radius (diamond buckles near 0.2 atm); their boron-carbide/honeycomb sandwich
closes at payload fraction 0.1, shell alone 1.16 kg per m³ enclosed. See the per-source note.

**The lattice step** — Jenett, Gregg & Cheung, AIAA 2019-0815 / NTRS 20190001133 [read — in
`papers/`]: a vacuum sphere whose wall is a cellular solid of hollow CFRP struts at fixed
R/t = 10; strength-limited conclusion; 0.508 kg/m³ shell with the skin counted at zero mass and
fibre (not laminate) properties. See the per-source note.

**The AFIT / Palazotto line** — the only sustained academic programme on vacuum LTA structures.
Metlen's 2013 thesis [read — in `papers/`] is its honest core: W/B 0.81 isogrid, 0.57 frame
alone, and **0.94 once a real membrane is costed** — the membrane term nearly doubles the
structure, which is the same term our correction 5 re-derived at 0.347 kg/m³. Around it,
verified bibliographically [biblio: Crossref during the round; DOIs not all re-fetchable at
integration]: Adorno-Rodriguez & Palazotto 2015 (J. Aircraft 52(3), 10.2514/1.C033284, icosahedron
under internal vacuum); Snyder & Palazotto 2018 and Graves et al. 2019 (already catalogued);
Schwemmer et al. 2018 (10.2514/1.J057043); Demasi et al. 2019 (starred polyhedra with internal
pockets — the programme's closest step toward subdividing the volume, and still not sealed
cells); Tran, Wan & Palazotto 2025 (descent dynamics — the programme is alive). Every AFIT
geometry is one polyhedral envelope: frame in compression, membrane carrying the full
atmosphere across every face. None subdivides the vacuum.

**Adorno & Palazotto 2020, "near-vacuum" gossamer envelopes (AIAA 2020-0479)** [biblio,
**unread**] — recorded here as an **open contradiction**. Our Δp scaling says shell-per-lift
strictly degrades as the vacuum softens, so full vacuum is optimal; the living AFIT programme
retreated to *near*-vacuum. Both cannot be right about the optimum unless their gossamer
coefficient gain beats the exponent loss. Until someone reads that paper, the page may not
claim "full vacuum is strictly optimal" as if uncontested.

**Barton's tension-stabilised line** — patent US 7,708,161 (§3) plus arXiv physics/0610222 and
J. Aircraft 2013 (10.2514/1.C031654; conference version 10.2514/6.2011-1717) [biblio: Crossref].
The round read the arXiv abstract only: an inflatable lobed vacuum chamber is stable when
internal pressure exceeds equilibrium by ≥ 4/3, *with experimental support* — which would make
it the only experimentally tested vacuum-buoyancy structure in the whole record. Both the 4/3
factor and the experimental claim are **single-sourced to an abstract** [not re-verified];
read the paper before either goes on the page.

**Mars branch** — Deshmukh & Arora 2023 (10.2514/6.2023-77208) and Dabas et al. 2025
(10.52202/083092-0074) [biblio: Crossref]. Relevant only as evidence the field's active edge
went to thinner atmospheres. It buys nothing on the governing number: ρ and P fall together, so
the E/ρ² criterion is unchanged, and a Mars feasibility result would not contradict the
terrestrial wall.

## 5. The novelty claim, stated as exactly what it is

What this project would like to say: *nobody has published a shared-wall multi-cell vacuum
interior — partitions at zero differential because vacuum sits on both sides, the atmosphere
carried only at the boundary, breach bounded by the smallest sealed enclosure.*

What this note can actually support is a **bounded negative**:

- **Searched:** Google Patents (JSON search API; page fetches until the endpoint went 503),
  Crossref, arXiv's API, Wikipedia, Hackaday, Marginalia, and the reference lists of the three
  read primaries (A&G 2021, Jenett 2019, Metlen 2013).
- **Blocked that day:** DuckDuckGo, Semantic Scholar (429), SSRN (403), Espacenet, Justia
  (Cloudflare), FreePatentsOnline, and Google Patents page fetches mid-session.
- **Found and read or verified:** every architecture in §§3–4. Each is one of (a) a single
  envelope with a clever wall (A&G sandwich, Jenett lattice wall, every AFIT polyhedron),
  (b) independent vacuum tanks that each pay the full boundary (Hobson 2023, Turinetti's
  single-volume elements), or (c) cells that hold *pressurised gas* to stabilise a vacuum
  (Armstrong 1921, Noel 1983, Barton, Bliamptis's inflated struts). The specific shared-wall
  evacuated-cell mechanism was found nowhere.
- **Located but NOT read:** van Egmond US 12,091,150 B2 — the closest title in the record to a
  vacuum-cell material and therefore the item most capable of falsifying the claim; Toli's
  application and his catalogued 2026 journal paper; Rapport & Middleton's fractal tensegrity
  application; Bliamptis's claims; the Chinese utility models; Demasi 2019's "pockets".

The audit flagged this claim as single-sourced — one sweep, with most search engines blocked —
and that label stands. The honest sentence for the page is "we could not find it in what we
could search on 2026-08-10, and US 12,091,150 remains unread", never "it does not exist".
Amateur record: equally bounded — one verified Hackaday writeup (2024-10-08, the Armstrong/Noel
architecture rediscovered, nothing built) [read], and Wikipedia names zero amateur attempts;
the folklore of imploding YouTube spheres could not be verified and is deliberately not cited.

## 6. Where the record does not support us

1. **No published design is within 2× of our level-2 number.** Best published shells: Jenett
   0.508 kg/m³ (skin uncosted, fibre properties), A&G 1.16, Metlen ≈ 1.15. Our level-1 figure
   (1.086) sits exactly in that company, which is reassuring. Our level-2 figure — **0.428
   kg/m³ — is beyond the entire literature and is supported by no published source** [audit:
   unsourced, load-bearing]. Its support is Lakes' hierarchy argument (Nature 361, 1993, a
   theory of material exponents, not of vacuum vessels with films, joints and knockdowns) plus
   this project's own model. The nearest *measured* multi-level datum is Zheng et al.,
   "Multi-scale metallic metamaterials", **Nature Materials 15 (2016)** — venue verified from
   the LLNL manuscript (LLNL-JRNL-677190) this round fetched; an earlier draft said *Science*,
   which is wrong — and it measures near-linear strength–density scaling, i.e. it supports the
   *mechanism* and says nothing about our *coefficient*. The page must call 0.428 a prediction
   of this project, not a result of the field.
2. **The living AFIT programme is walking the other way** (§4, Adorno & Palazotto 2020,
   unread). Open contradiction; cheap to resolve; until resolved it caps how hard the page may
   lean on full-vacuum optimality.
3. **Jenett's own conclusion opposes ours in regime**: he finds strength-limited, we find
   buckling-limited at our R/t ≈ 76. The reconciliation (his fixed R/t = 10 buys local-buckling
   immunity with mass and forfeits the proportion-optimising exponent) is already in the
   vacuum-cell analysis; keep it — an informed reviewer raises this within minutes.
4. **Unread wildcards that could contain contradicting numbers:** Toli 2026 (global buckling —
   already catalogued as the largest single gap in this collection); van Egmond US 12,091,150
   (prior claims on low-density structured materials); Schwemmer 2018 and Graves 2019 (W/B
   results that could beat Metlen's). None is licensed for `papers/`; all are
   catalogue-and-read items.

## 7. What the whole field lacked — and who came closest

| Mechanism (this project) | Closest prior | Gap |
|---|---|---|
| Shared-wall evacuated cells; interior partitions at zero differential | Jenett (cellular wall, one skin, no sealed cells); Hobson 2023 (many chambers, each paying a full boundary); Barton (cells, but pressurised) | Nobody combines them; the zero-differential-interior statement appears in no source found (bounded per §5) |
| Co-critical tube proportion (Euler = local wall buckling, R/t ≈ 76) | Jenett (hollow tubes, fixed R/t = 10) | Fixing the proportion forfeits the scaling law the result turns on |
| Level-2 hierarchy (tube-of-tubes) | A&G sandwich (= exactly level 1); Rapport & Middleton (unread); Lakes 1993 and Zheng 2016 (the theory and the measurement, no vessel) | No vacuum-LTA design in the record goes past level 1 |
| Seal at every scale (breach bounded by the smallest enclosure) | Hobson 2023 (one scale); Turinetti (elements, one shared vacuum behind one valve) | Nobody nests it |

Licence note per `research/README.md`: nothing new is copied into `papers/` from this round —
the three read primaries were already there, patents were fetched only as index records (cite
the number and USPTO/Espacenet, not a scraped page), and everything else found is AIAA, Wiley,
Elsevier, arXiv-default, CC BY-SA or vendor-hosted: catalogue only.
