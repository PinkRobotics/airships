# Does the mission exist?

`docs/OPEN-QUESTIONS.md` #13: the whole concept is a shuttle between a fire and a lake, and no
figure anywhere in this project said what fraction of real fires have a lake worth shuttling
to. It bounds the market rather than the vehicle, and it had never been asked.

The stored twenty-season record has geometrically qualifying water within 300 km of every
fire of ten hectares or more, at each tested threshold. The reference class's median leg is
under five kilometres. This does not establish usable depth, access or an accepted mission;
the accepted and stand-down counts are reported below.

## Method

`pipeline/firehistory.py` pulls BC's historical fire perimeters — **3,286 fires of 10 ha or
more, 2006 through 2025, 10.93 million hectares burned** — and reduces each to the shoelace
centroid of its largest ring, keeping the simplified ring itself for the 615 fires of 1,000 ha
or more. `research/analysis/water-availability.js` joins that against the 13,646-body
Freshwater Atlas extract the monitor already uses, inside a real browser against the live
model, so every rate comes from a plan its served selector accepts.

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

## Rates from accepted plans

<!-- logistics:rates:start -->
The flight model assumes a buoyant fleet for these logistics quotients; this does not establish that a drawn hull floats.

| Class | 15 km worked example t/h | Median leg t/h | Mean accepted fire legs t/h | Mean accepted legs, hectare-weighted t/h |
|---|---|---|---|---|
| P-100 | 111.7 | 229.7 | 225.8 | 244.7 |
| P-1000 | 505.0 | 580.4 | 531.1 | 495.9 |
| P-10000 | 6,657.8 | 5,178.4 | 5,489.3 | 4,473.7 |

15 km worked example:

| Class | Leg km | State / mode | Released t | Retained t | Supplied MWh/cycle |
|---|---|---|---|---|---|
| P-100 | 15.00 | ready / rapid | 65.000 | 35.000 | 5.201 |
| P-1000 | 15.00 | ready / endurance | 215.591 | 784.409 | 26.489 |
| P-10000 | 15.00 | ready / rapid | 2626.200 | 7373.800 | 200.116 |

Median leg:

| Class | Leg km | State / mode | Released t | Retained t | Supplied MWh/cycle |
|---|---|---|---|---|---|
| P-100 | 4.71 | ready / rapid | 50.000 | 50.000 | 2.021 |
| P-1000 | 11.04 | ready / endurance | 206.333 | 793.667 | 22.656 |
| P-10000 | 23.95 | ready / rapid | 2626.200 | 7373.800 | 237.750 |

| Class | Accepted fire legs | Not served | Stand-downs | Unavailable |
|---|---|---|---|---|
| P-100 | 3286 | 0 | 0 | 0 |
| P-1000 | 2897 | 389 | 389 | 0 |
| P-10000 | 3286 | 0 | 0 | 0 |

The selector is `selectServedPlan`, requested balanced, record energy basis, still air. It chooses among the served pages' bounded controls at each exact leg; this is not a global optimum. Stand-down or unavailable legs supply no rate and are excluded from both means. Geometric water access above is a separate count.
<!-- logistics:rates:end -->

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

**2026-10-02 correction:** the station-disc calculation now uses the capsule-era fleet lengths.
The [regeneration audit](../../docs/audit/26-10-02-analysis-regeneration.md) retains the former figures.

**The adequacy thresholds are far more conservative than the ship's own geometry.** A hull
holding station needs a disc it fits inside — 0.95 ha for a P-100, 20.59 ha for a P-10000.
The shipped thresholds are 10.5× and 48.6× that. Loosening the P-10000 to 500 ha would roughly
double its qualifying bodies and cut its median leg from 23.95 to 19.01 km.

<!-- logistics:drawdown:start -->
A P-100 repeating the accepted 15 km plan for twelve hours releases 1,340 t, a geometric drawdown of 1.3 cm on a minimum-size body. Continuous supply and lake access are assumed.
<!-- logistics:drawdown:end -->

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
