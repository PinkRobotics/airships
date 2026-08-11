# Does the mission exist?

`docs/OPEN-QUESTIONS.md` #13: the whole concept is a shuttle between a fire and a lake, and no
figure anywhere in this project said what fraction of real fires have a lake worth shuttling
to. It bounds the market rather than the vehicle, and it had never been asked.

It has now. **Water is not the constraint. In twenty BC fire seasons there is not a single
fire of ten hectares or more without an adequate source in range of any class — and the median
one is under five kilometres from water.**

## Method

`pipeline/firehistory.py` pulls BC's historical fire perimeters — **3,286 fires of 10 ha or
more, 2006 through 2025, 10.93 million hectares burned** — and reduces each to the shoelace
centroid of its largest ring, keeping the simplified ring itself for the 615 fires of 1,000 ha
or more. `research/analysis/water-availability.js` joins that against the 13,646-body
Freshwater Atlas extract the monitor already uses, inside a real browser against the live
model, so every throughput figure is `planCycle`'s own.

Distance is to a body's **closest approach**, not its centroid: a 30 km lake with its tip
beside the fire is near water, and its centroid says otherwise.

## The answer

Nearest source that meets each class's own adequacy threshold:

| | threshold | qualifying bodies | median, by fire | p90 | median, by hectare burned | in range of the class |
|---|---|---|---|---|---|---|
| P-100 | 10 ha | 13,646 | **4.71 km** | 12.92 km | 5.38 km | **98.97%** of fires, 99.21% of hectares |
| P-1000 | 100 ha | 1,623 | 11.04 km | 32.19 km | 13.68 km | **100%** |
| P-10000 | 1,000 ha | 202 | 23.95 km | 68.30 km | 33.84 km | **100%** |

Every fire in the record has qualifying water within 300 km at every threshold tested, up to
5,000 ha — where only 56 bodies in the province qualify and the median distance is still
48.65 km. The binary question is settled. What remains is a distance distribution, and it is a
short one.

## The published throughput is conservative by nearly a factor of two

The reports work a 15 km one-way leg. The real median is 4.71 km, and the ledger is dominated
by transit:

| | at the 15 km worked example | at the real median | mean over all 3,286 fires | mean weighted by hectares burned |
|---|---|---|---|---|
| P-100 | 175.5 t/h | **332.3 t/h** | 322.0 t/h | 321.9 t/h |
| P-1000 | 1,696.7 t/h | 1,981.5 t/h | 1,996.2 t/h | 1,859.9 t/h |
| P-10000 | 13,183.4 t/h | 10,863.4 t/h | 11,134.8 t/h | 9,353.4 t/h |

The reference ship delivers **1.9× its published rate** against the real distribution of BC
fires. The P-10000 goes the other way — it needs 1,000 ha of water, the 202 bodies that
qualify are unevenly spread, and the big northern fires are far from them: weighted by
hectares burned its median leg is 33.84 km and it delivers 71% of the worked-example figure.

That inversion is worth stating plainly, because it is the reference-class argument arriving
from a direction nobody chose. The small ship is the one the geography suits.

## A large fire is not a point, and it does not change the answer

For the 615 fires of 1,000 ha or more, sampling twelve points around the perimeter and taking
the **worst-served** one:

| threshold | median worst edge | p90 worst edge |
|---|---|---|
| 10 ha | 7.51 km | 17.72 km |
| 100 ha | 15.61 km | 38.42 km |
| 1,000 ha | 36.90 km | 86.81 km |

The far edge of a median campaign fire is 7.5 km from P-100 water. Even the p90 is inside the
class's 25 km search radius.

## Two things this found in the model

**`findSource` does not return the nearest source.** It scores candidates as
`d / min(12, (area/minHa)^0.35)` — deliberately flying past a qualifying pond to reach a lake,
which is right operationally. But nobody has priced it: the model flies further than the
nearest adequate water on **45.4% / 43.0% / 31.5%** of fires, with a p90 detour of 9.25 /
24.16 / 29.07 km. The median detour is zero, so this is a tail behaviour, and on the tail it is
large enough to halve throughput. The size preference is an unjustified constant of the kind
`OPEN-QUESTIONS` #7 counts, and it now has a measured cost.

**The adequacy thresholds are far more conservative than the ship's own geometry.** A hull
holding station needs a disc it fits inside — 2.84 ha for a P-100, 60.27 ha for a P-10000.
The shipped thresholds are 3.5× and 16.6× that. Loosening the P-10000 to 500 ha would roughly
double its qualifying bodies and cut its median leg from 23.95 to 19.01 km.

Volume is a non-issue: a P-100 working flat out for twelve hours draws 2,106 t, which is
**2.1 cm** off a minimum-size body.

## What this analysis cannot answer, and it is the important one

**The Freshwater Atlas carries area. It does not carry depth.** The anchor bag has to submerge
to fill:

| | bag | diameter as a filled cylinder | water depth needed |
|---|---|---|---|
| P-100 | 125 t | 5.42 m | **8.1 m** |
| P-1000 | 1,250 t | 11.68 m | 17.5 m |
| P-10000 | 12,400 t | 25.09 m | **37.6 m** |

Nothing in this dataset says how many of those 13,646 bodies are 8 m deep where a ship would
hover, let alone 38 m. Small interior lakes are routinely shallower than that, and shallow is
exactly what a 10 ha lake tends to be. **This is now the binding uncertainty in the water
question, and it has moved from "is there a lake" to "is that lake deep enough".**

It is also answerable. BC holds bathymetry for a substantial subset of its lakes, and the
question is a join away for anyone with access to it.

## Honest limits

- **BC only.** The concept generalises; this dataset does not.
- **Fires below 10 ha are excluded.** BCWS records thousands of small starts a year that are
  out before anything flies. Including them would shorten every distance, because small fires
  are everywhere; excluding them keeps the analysis on fires that get an aviation response.
- **Straight-line distance.** No terrain, no airspace, no wind. The ship flies over ridges the
  distance ignores.
- **Surface area only.** Beyond depth: access, shoreline, ice, seasonal drawdown, fish habitat
  and any legal right to draft water are all absent from the Atlas and from this analysis. A
  lake that qualifies geometrically may be closed to a fleet for reasons that have nothing to
  do with hydrology.
- **Perimeters are the final footprint**, not where the fire was when it mattered. The
  distance a ship would actually fly on day two of a campaign is shorter than the figure here.
