# Does the mission exist?

`docs/OPEN-QUESTIONS.md` #13: the whole concept is a shuttle between a fire and a lake, and no
figure anywhere in this project said what fraction of real fires have a lake worth shuttling
to. It bounds the market rather than the vehicle, and it had never been asked.

The stored twenty-season record measures mapped shore proximity. Drafting-station geometry
and invented exercise legs are reported separately. None establishes usable depth, access,
permission or a dispatch of a recorded fire; accepted-plan quotients and stand-down counts
at the stated proxy distances are reported below.

## Method

`pipeline/firehistory.py` pulls BC's historical fire perimeters — **3,286 fires of 10 ha or
more, 2006 through 2025, 10.93 million hectares burned** — and reduces each to the shoelace
centroid of its largest ring, keeping the simplified ring itself for the 615 fires of 1,000 ha
or more. `research/analysis/water-availability.js` joins that against the 13,646-body
Freshwater Atlas extract the monitor already uses, inside a real browser against the live
model. The rate tables are accepted-plan quotients at shore-proxy distances, not a dispatch
of any recorded fire or a demonstration of flight.

**Mapped shore proximity** means distance to the closest vertex of the simplified outline,
or the centroid where no outline exists. It is neither an exact shoreline distance nor a
flown leg. The separate station measure uses `sim/water.js`'s generated drafting points.
Selection keeps the size-weighted heuristic, using the nearest qualifying station on each
source; all stations offered to its mission fall within the class's search radius from the
incident point. The cycle planner chooses among those stations for the drop lines. Its mean
planned leg is published separately because a station-to-line route differs from a distance
to the incident point.

## Mapped shore proximity

Nearest mapped body meeting each class's area threshold, measured at its shore proxy:

| | threshold | qualifying bodies | median, by fire | p90 | median, by hectare burned | shore proxy within the class search radius |
|---|---|---|---|---|---|---|
| P-100 | 10 ha | 13,646 | **4.71 km** | 12.92 km | 5.38 km | **98.97%** of fires, 99.21% of hectares |
| P-1000 | 100 ha | 1,623 | 11.04 km | 32.19 km | 13.68 km | **100%** |
| P-10000 | 1,000 ha | 202 | 23.95 km | 68.30 km | 33.84 km | **100%** |

Every fire in the record has qualifying water within 300 km at every threshold tested, up to
5,000 ha — where only 56 bodies in the province qualify and the median distance is still
48.65 km. These are distances from recorded points to mapped water, not proof that a source
can supply an aircraft or that a mission exists.

## Rates from accepted plans

<!-- logistics:rates:start -->
The flight model assumes a buoyant fleet for these logistics quotients; this does not establish that a drawn hull floats.

| Class | 15 km worked example t/h | Median leg t/h | Mean accepted fire legs t/h | Mean accepted legs, hectare-weighted t/h |
|---|---|---|---|---|
| P-100 | 106.1 | 189.5 | 176.9 | 175.9 |
| P-1000 | 451.5 | 509.3 | 535.9 | 497.4 |
| P-10000 | 7,357.0 | 5,741.1 | 6,103.6 | 4,984.8 |

15 km worked example:

| Class | Leg km | State / mode | Released t | Retained t | Supplied MWh/cycle |
|---|---|---|---|---|---|
| P-100 | 15.00 | ready / balanced | 70.948 | 29.052 | 6.622 |
| P-1000 | 15.00 | ready / endurance | 191.775 | 808.225 | 24.472 |
| P-10000 | 15.00 | ready / rapid | 2945.496 | 7054.504 | 202.102 |

Median leg:

| Class | Leg km | State / mode | Released t | Retained t | Supplied MWh/cycle |
|---|---|---|---|---|---|
| P-100 | 4.71 | ready / rapid | 65.000 | 35.000 | 3.933 |
| P-1000 | 11.04 | ready / endurance | 179.806 | 820.194 | 20.646 |
| P-10000 | 23.95 | ready / rapid | 2945.496 | 7054.504 | 241.048 |

| Class | Accepted fire legs | Not served | Stand-downs | Unavailable |
|---|---|---|---|---|
| P-100 | 3009 | 277 | 277 | 0 |
| P-1000 | 3286 | 0 | 0 | 0 |
| P-10000 | 3286 | 0 | 0 | 0 |

The selector is `selectServedPlan`, requested balanced, record energy basis, still air. It chooses among the served pages' bounded controls at each exact leg; this is not a global optimum. Stand-down or unavailable legs supply no rate and are excluded from both means. Geometric water access above is a separate count.
<!-- logistics:rates:end -->

## Mapped shore proximity around the recorded perimeter

For the 615 fires of 1,000 ha or more, sampling twelve points around the perimeter and taking
the **worst-served** one:

| threshold | median worst edge | p90 worst edge |
|---|---|---|
| 10 ha | 7.51 km | 17.72 km |
| 100 ha | 15.61 km | 38.42 km |
| 1,000 ha | 36.90 km | 86.81 km |

At the reference area threshold the sampled perimeter's median worst shore-proxy distance
is 7.5 km. Its p90 shore proxy is within the class's 25 km radius; station coverage of those
perimeter samples is not measured here.

## Generated drafting stations and planned exercise legs

The size preference remains an explicitly unvalidated area heuristic. Keeping it avoids
changing the model's source-size preference while repairing its distance basis. It does not
establish sustainable repeated draw. The table compares the nearest generated station with
the size-weighted selection and checks that selection offers no station outside its radius.
The historical-point rows are geometry only. The flown-leg rows belong to the separately
labelled invented exercise: no fire shown there happened and no aircraft flew.

<!-- water-stations:start -->
| Class | Points with an in-radius station | No selected source | Nearest station median / p90, km | Selected station median / p90, km | Selections offering an out-of-radius station |
|---|---:|---:|---:|---:|---:|
| P-100 | 3251 | 35 | 4.98 / 13.14 | 7.07 / 19.17 | 0 |
| P-1000 | 3286 | 0 | 12.14 / 33.29 | 15.62 / 57.08 | 0 |
| P-10000 | 3286 | 0 | 25.90 / 70.05 | 28.10 / 93.98 | 0 |

| Class | Selection farther than nearest station, % | p90 station detour, km |
|---|---:|---:|
| P-100 | 47.31 | 9.50 |
| P-1000 | 45.01 | 25.97 |
| P-10000 | 32.65 | 30.37 |

Invented exercise geometry (empty when this study is run on another view):

| Hull | Invented incident | Class | Nearest station, km | Mean planned leg, km | Plan state |
|---|---|---|---:|---:|---|
| Condor | EX090 | P10000 | 61.21 | 47.39 | ready |
| Osprey | EX034 | P1000 | 19.19 | 15.64 | ready |
| Pelican | EX094 | P1000 | 15.20 | 14.30 | ready |
| Heron | EX044 | P1000 | 30.22 | 28.87 | ready |
| Albatross | EX057 | P1000 | 33.47 | 32.63 | ready |
| Skimmer | EX039 | P1000 | 28.45 | 27.25 | ready |
| Kingfisher | EX074 | P100 | 20.17 | 19.30 | ready |
| Tern | EX116 | P100 | 20.17 | 20.05 | ready |
| Merganser | EX049 | P100 | 6.10 | 5.73 | ready |
| Dipper | EX045 | P100 | 7.45 | 7.33 | ready |
| Grebe | EX097 | P100 | 14.41 | 13.98 | ready |
| Loon | EX058 | P100 | 10.11 | 9.78 | ready |
| Swift | EX013 | P100 | 5.53 | 5.54 | ready |
| Petrel | EX072 | P100 | 9.44 | 9.47 | ready |
| Kestrel | EX078 | P100 | 5.26 | 5.20 | ready |
| Auklet | EX075 | P100 | 4.94 | 4.94 | ready |
<!-- water-stations:end -->

## Source-area and depth limits

**2026-10-02 correction:** the station-disc calculation now uses the capsule-era fleet lengths.
The [regeneration audit](../../docs/audit/26-10-02-analysis-regeneration.md) retains the former figures.

**The adequacy thresholds are far more conservative than the ship's own geometry.** A hull
holding station needs a disc it fits inside — 0.95 ha for a P-100, 20.59 ha for a P-10000.
The shipped thresholds are 10.5× and 48.6× that. Loosening the P-10000 to 500 ha would roughly
double its qualifying bodies and cut its median mapped shore-proxy distance from 23.95 to 19.01 km.

<!-- logistics:drawdown:start -->
A P-100 repeating the accepted 15 km plan for twelve hours releases 1,274 t, a geometric drawdown of 1.3 cm on a minimum-size body. Continuous supply and lake access are assumed.
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
exactly what a 10 ha lake tends to be. Depth remains an unresolved requirement alongside
station geometry, access and permission.

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
- **Perimeters are the final footprint**, not an operational target or an incident-time
  dispatch request. This study measures distances and makes no counterfactual fire claim.
