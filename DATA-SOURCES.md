# Data sources, licences and attribution

The wildfire data in this project is real and comes from public agencies. The fleet is
imagined. This file states, for every dataset the repository redistributes and every
service the server-side mirror calls: what it is, who publishes it, the exact licence, the
attribution sentence that licence requires, the URL it came from, how it was processed,
and which file holds it.

The code is Apache-2.0 (see `LICENSE`). The data is not: each dataset below keeps its own
terms. `NOTICE` carries the short form of everything here.

Two blanket statements, required by the Open Government Licences and true of all of it:

> **The Information used in this project was modified.** Coordinates were simplified and
> rounded, features were filtered, and elevation was rendered into a shaded image. Nothing
> in `data/` is a faithful copy of an official record. For anything that matters, go to the
> publisher.

> **No information provider endorses this project.** Its use of their data implies no
> official status of any kind. For real emergencies use the BC Wildfire Service, not this
> page.

## Contents

| # | Dataset | File | Licence |
|---|---------|------|---------|
| 1 | BC Wildfire Service active fires and perimeters | `data/snapshot.json`, `data/live/fires.json`, `data/live/perims.json` | OGL – British Columbia |
| 2 | NRCan CWFIS 24-hour satellite hotspots | `data/snapshot-heat.json`, `data/live/heat.json` | OGL – Canada |
| 3 | BC Freshwater Atlas lakes and reservoirs | `data/water-bc.json` | OGL – British Columbia |
| 4 | Terrain hillshade from AWS Terrain Tiles | `data/terrain-bc.jpg` | per-source; see below |
| 5 | Natural Earth roads and BC outline | `data/roads-bc.json`, `data/bc-outline.json` | public domain |
| 6 | Former Esri basemap | removed; first-party hillshade instead | see section 4 |
| 7 | Open-Meteo 850 hPa wind forecast | `data/live/wind.json` | CC BY 4.0 |
| 8 | BC historical fire perimeters, 2006-2025 | `data/fire-history-bc.json` (+ `.prov.json`) | Open Government Licence – British Columbia |

---

## 1. BC Wildfire Service active fires and fire perimeters

**What it is.** Every wildfire incident in British Columbia whose status is not `Out`: a
point per incident with fire number, status, cause, discovery size in hectares, ignition
date and geographic description; and, for fires large enough to have been mapped, a
polygon perimeter with a track date. This is the input the model plans against — the fires
the imagined fleet is sent to are these fires.

**Publisher.** Province of British Columbia, BC Wildfire Service (Ministry of Forests).

**Licence.** Open Government Licence – British Columbia, version 2.0.
<https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc>

**Required attribution**, verbatim as the licence specifies it where the provider gives no
statement of its own:

> Contains information licensed under the Open Government Licence – British Columbia.

**Where it came from.** The BCWS public ArcGIS FeatureServer, which is the same service
that backs the province's own public dashboard at
<https://wildfiresituation.nrs.gov.bc.ca/>. Catalogue records:

- BC Wildfire Fire Locations – Current: <https://catalogue.data.gov.bc.ca/dataset/bc-wildfire-fire-locations-current>
- BC Wildfire Fire Perimeters – Current: <https://catalogue.data.gov.bc.ca/dataset/bc-wildfire-fire-perimeters-current>

Exact endpoints, as issued by `pipeline/live.py`:

```
https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services
  /BCWS_ActiveFires_PublicView/FeatureServer/0/query
  ?where=FIRE_STATUS%20%3C%3E%20%27Out%27
  &outFields=FIRE_NUMBER,FIRE_STATUS,FIRE_CAUSE,INCIDENT_NAME,GEOGRAPHIC_DESCRIPTION,
             CURRENT_SIZE,IGNITION_DATE,FIRE_URL,FIRE_OF_NOTE_IND,RESPONSE_TYPE_DESC
  &returnGeometry=true&outSR=4326&f=geojson

https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services
  /BCWS_FirePerimeters_PublicView/FeatureServer/0/query
  ?where=FIRE_STATUS%20%3C%3E%20%27Out%27
  &outFields=FIRE_NUMBER,FIRE_STATUS,FIRE_SIZE_HECTARES,TRACK_DATE
  &returnGeometry=true&outSR=4326&maxAllowableOffset=0.002&f=geojson
```

**How it was processed.** For the live path: none. `pipeline/live.py` wraps the upstream
GeoJSON unchanged in `{fetchedAt, source, data}` and writes it to `data/live/`. Perimeter
geometry is generalised server-side by `maxAllowableOffset=0.002` (about 150 m at this
latitude) — a request parameter, not a local edit. For the committed snapshot: the same two
responses, taken at one instant, placed side by side under `fires` and `perimeters` keys
with a `retrievedAt` timestamp. `data/snapshot.json` holds 105 fires and 73 perimeters as
retrieved at 2026-08-08T18:42:38Z.

**Load discipline.** The browser never loads fire data from the BCWS service; an unavailable mirror uses
the dated snapshot.
`pipeline/live.py` runs on our server every ten minutes and refreshes the fire feeds only
when the mirror is older than eight minutes, so upstream sees roughly six requests an hour
regardless of how many people load the page. Traffic to this page must not become load on
emergency infrastructure. If you fork this, keep that property.

---

## 2. Natural Resources Canada — CWFIS 24-hour satellite hotspots

**What it is.** Thermal anomalies detected by satellite in the last 24 hours, each with a
brightness-derived `temp` value. On the page this is the heat layer: the diffuse glow under
the fire symbols. It is detection data, not a fire perimeter, and a hotspot is not a fire.

**Publisher.** Natural Resources Canada, Canadian Forest Service — Canadian Wildland Fire
Information System (CWFIS).

**Licence.** Open Government Licence – Canada, version 2.0.
<https://open.canada.ca/en/open-government-licence-canada>

**Required attribution**, verbatim as the licence specifies it:

> Contains information licensed under the Open Government Licence – Canada.

The same licence adds a non-endorsement condition, which is why the blanket statement at
the top of this file exists: nothing here may suggest official status or NRCan's
endorsement.

**Where it came from.** The CWFIS GeoServer WFS. Datamart: <https://cwfis.cfs.nrcan.gc.ca/datamart>

```
https://cwfis.cfs.nrcan.gc.ca/geoserver/public/wfs
  ?service=WFS&version=2.0.0&request=GetFeature
  &typeNames=public%3Ahotspots_last24hrs
  &outputFormat=application%2Fjson&srsName=EPSG:4326
  &CQL_FILTER=lat%20BETWEEN%2047.5%20AND%2060.6%20AND%20lon%20BETWEEN%20-140%20AND%20-113.3
  &sortBy=temp%20D&count=6000&propertyName=geometry,temp
```

**How it was processed.** Filtered server-side to the BC-and-margin bounding box shown in
the CQL above, sorted by descending temperature, capped at 6000 features, and reduced to
geometry plus `temp`. The live mirror stores that response verbatim. The committed snapshot
`data/snapshot-heat.json` keeps only the hottest 2000 of them, so that `?data=snapshot`
reproduces a fixed input; it records its own `retrievedAt` (2026-08-09T07:02:39Z) and
`source`. The live page uses the full feed. Refresh cadence in `pipeline/live.py` is 25
minutes, because the satellites pass a handful of times a day and anything faster is waste.

---

## 3. BC Freshwater Atlas — lakes and manmade waterbodies

**What it is.** Every mapped BC lake of 10 hectares or more, plus manmade reservoirs of the
same size, reduced to a centroid, a surface area, a name and (for the larger ones) a
simplified outline. This is the fleet's water supply: the model picks intakes from this
list, and the size-weighted choice rule is driven by the `AREA_HA` field.

**Publisher.** Province of British Columbia, GeoBC Branch — Freshwater Atlas.

**Licence.** Open Government Licence – British Columbia, version 2.0.
<https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc>

**Required attribution**, verbatim:

> Contains information licensed under the Open Government Licence – British Columbia.

**Where it came from.** The province's public WFS at `openmaps.gov.bc.ca`, two layers:

```
https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.FWA_LAKES_POLY/ows
  ?service=WFS&version=2.0.0&request=GetFeature
  &typeName=pub:WHSE_BASEMAPPING.FWA_LAKES_POLY
  &outputFormat=application/json&srsName=EPSG:4326&sortBy=AREA_HA
  &CQL_FILTER=AREA_HA>=10 AND FEATURE_CODE='GB15300000'

https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.FWA_MANMADE_WATERBODIES_POLY/ows
  ?service=WFS&version=2.0.0&request=GetFeature
  &typeName=pub:WHSE_BASEMAPPING.FWA_MANMADE_WATERBODIES_POLY
  &outputFormat=application/json&srsName=EPSG:4326&sortBy=AREA_HA
  &CQL_FILTER=AREA_HA>=10 AND FEATURE_CODE='GB24300000'
```

Catalogue records:

- Freshwater Atlas – Lakes: <https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-lakes>
- Freshwater Atlas – Manmade Waterbodies: <https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-manmade-waterbodies>

**How it was processed.** `pipeline/water.py`, paging the WFS 5000 features at a time. For
each waterbody it keeps the largest polygon's outer ring, computes a shoelace centroid,
and emits `[lon, lat, area_ha, kind, name, ring|null]` with `kind` 0 for lake and 1 for
reservoir. Coordinates are rounded to four decimal places, about 11 m. A simplified ring is
included only for bodies of 80 ha or more (Douglas–Peucker at 0.0025° below 2000 ha,
0.006° above); smaller bodies are drawn as area-scaled circles. The result is 13,617 lakes
and 29 reservoirs.

The file's own note says it and it is worth repeating: **surface area is a proxy only.** The
model treats a large lake as a usable intake. Depth, access, shoreline, ice, seasonal
drawdown and whether anyone is allowed to draft from it are all absent.

**Regenerate.** `python3 pipeline/water.py data/water-bc.json` (several minutes; ~14,000
features over many WFS pages).

---

## 4. Terrain hillshade — `data/terrain-bc.jpg`

**What it is.** A 2560 × 2304 JPEG: a dark-styled hillshade of BC and its surroundings,
used as the map backdrop. It is a rendering, not elevation data — you cannot read a height
out of it. Ocean is painted a flat colour, so no bathymetry is visible in the image even
though bathymetry was present in the tiles it was built from.

**Where it came from.** AWS Terrain Tiles (the Mapzen/Tilezen "terrarium" encoding),
`https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`, a public dataset
on the AWS Open Data registry: <https://registry.opendata.aws/terrain-tiles/>. `pipeline/terrain.py`
fetches zoom 7, tiles x 14–23 and y 36–44 inclusive — 90 tiles, 2560 × 2304 px, covering
longitude −140.625° to −112.5° and latitude 47.04° to 61.61°.

**What is actually in it.** Terrain Tiles composites different national and global
elevation datasets by zoom and location. At zoom 7 over this footprint, per the Tilezen
data-sources documentation, that is:

- **CDEM** (Canadian Digital Elevation Model, Natural Resources Canada) over Canada;
- **SRTM** (NASA/USGS) over the United States portion — Washington, Idaho, Montana, and
  northern Oregon;
- **GMTED2010** (USGS) north of 60°, i.e. the Yukon and NWT strip along the top edge;
- **ETOPO1** (NOAA) in the ocean — fetched, but painted over by the flat sea colour in the
  render, so it does not appear in the published image.

3DEP is *not* in this image: Terrain Tiles only sources it from zoom 10 upward.

**Licence and required attribution.** Per-source, not one licence. The attribution strings
below are the ones the Tilezen project specifies
(<https://github.com/tilezen/joerd/blob/master/docs/attribution.md>), reproduced for the
sources actually present here:

> Canada terrain data contains information licensed under the Open Government Licence –
> Canada;
> United States 3DEP (formerly NED) and global GMTED2010 and SRTM terrain data courtesy of
> the U.S. Geological Survey;
> Global ETOPO1 terrain data U.S. National Oceanic and Atmospheric Administration.

The USGS terms for GMTED2010 additionally ask that anyone who modifies the data describe
the modifications and not imply USGS approval. The modifications are: composited to a
mercator mosaic by Tilezen; then, by `pipeline/terrain.py`, a 315°/45° hillshade over
pixel-unit gradients divided by 60 (a vertical exaggeration chosen for looks), an
elevation tint clipped at 2600 m with a 0.7 gamma, a flat colour for every pixel at or
below 0 m, and JPEG compression at quality 84. USGS, NRCan and NOAA had no part in any of
that and approve none of it.

**Regenerate.** `python3 pipeline/terrain.py data/terrain-bc.jpg` (90 tile fetches; prints
the world bounds the page needs, which are hard-coded as `TERRAIN` in `app/map/basemap.js`).

---

## 5. Natural Earth — roads and the BC outline

The map uses `data/roads-bc.json` (306 polylines, 4,823 vertices) and
`data/bc-outline.json` (23 rings, 1,064 vertices) for orientation. The model does not
read these layers. They are public-domain Natural Earth data, credited as requested:

> Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.

**Reproducible source.** `pipeline/vectors.py` reads the tagged
[v5.1.2 archive](https://codeload.github.com/nvkelso/natural-earth-vector/tar.gz/refs/tags/v5.1.2),
and refuses any archive whose SHA-256 differs from
`62b2ecf311e54b76e433c680c4e47a29ecffc87b0cadd014716cbff7c6daa54b`.
It uses `geojson/ne_10m_roads.geojson` and the British Columbia feature of
`geojson/ne_50m_admin_1_states_provinces.geojson`. The archive is about 1.5 GB;
`--archive` reuses a local copy and still verifies its checksum.

Roads exclude ferries and are clipped to longitude −137.5°…−112°, latitude 47.3°…60.6°.
Douglas–Peucker tolerances are 0.003° for roads and 0.005° for the outline's outer rings;
holes and properties are discarded and coordinates rounded to three decimal places.
This is a cartographic outline, not a legal or survey boundary.

**Numbers changed on 2026-10-01.** The earlier files had 294 road polylines / 3,032
vertices and 23 outline rings / 804 vertices, with an inferred 5.x source and no generator.
The explicit clipping and simplification above produce 306 / 4,823 and 23 / 1,064.
The new geometry is not byte-identical; it preserves more road and coastline detail.
Both sidecars now record the exact archive, checksum, processing and retrieval time.
[Source terms](https://www.naturalearthdata.com/about/terms-of-use/).

---

## 6. Esri World Imagery — removed 2026-10-01

The tile loader and satellite toggle have been removed. No Esri images are loaded or
redistributed. The default backdrop is the first-party `data/terrain-bc.jpg` hillshade
in section 4, with outlined labels and fire markers, brighter water and stronger perimeters.
The former unkeyed tile access is no longer a dependency or a publication blocker.

---

## 7. Open-Meteo — mirrored 850 hPa wind forecast

**Source and credit.** Weather data by Open-Meteo.com. Data is licensed under
[CC BY 4.0](https://open-meteo.com/en/license); underlying forecasts come from national
meteorological services. This forecast is an input to simulated transit times, not an
aviation weather product.

`pipeline/live.py` makes at most one batch request per hour to
`https://api.open-meteo.com/v1/forecast`, using the hourly `wind_speed_850hPa` and
`wind_direction_850hPa` variables, `forecast_hours=1`, `wind_speed_unit=kmh` and `timezone=UTC`.
The fixed 5×5 grid has latitudes 47.5, 50.75, 54, 57.25, 60.5 and longitudes −140,
−133.25, −126.5, −119.75, −113. One request serves all visitors. Failed attempts also
consume that hour's request; a failed fetch preserves the previous successful timestamp.

The mirror writes `data/live/wind.json` with `fetchedAt`, the forecast hour, grid axes and
east/north velocity components in km/h. The browser reads that file from its own origin
and bilinearly interpolates the components at each mission midpoint, then converts them
back to speed and meteorological direction. Averaging components handles the 0°/360° seam.
No visitor coordinates or IP addresses are sent to the forecast provider by this page.

Missing, malformed or stale wind means still air, stated on the monitor. The fetch-age
limit is 90 minutes, and the forecast-hour limit is two hours. The page clears previously
applied wind on failure and at expiry. `?data=snapshot` always uses still air.

**API terms remain the operator's responsibility.** Moving requests to a mirror reduces
traffic and removes browser contact with the provider; it does not change Open-Meteo's
API-use terms or grant commercial-use permission. Configure an appropriately licensed
service before commercial operation. The server URL is contained in `pipeline/live.py`.

---

## 8. BC historical fire perimeters — twenty seasons

**What it is.** Every mapped BC fire perimeter of 10 hectares or more from 2006 onward:
3,286 polygons, 10,928,804 hectares. Fetched once by `pipeline/firehistory.py` from the
province's WFS and stored as `data/fire-history-bc.json`, with the full record in
`data/fire-history-bc.prov.json`.

**Where it came from.** `WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP` on
openmaps.gov.bc.ca, filtered `FIRE_YEAR>=2006 AND FIRE_SIZE_HECTARES>=10`, geometry requested
at `maxAllowableOffset` 0.001 degrees.

**Licence.** Open Government Licence – British Columbia 2.0, the same as the Freshwater Atlas
and the live fire feed. *Contains information licensed under the Open Government Licence –
British Columbia.* The Information was modified: filtered, simplified, reduced to centroids
and rounded to four decimal places. The Province does not endorse this project and nothing
here has official status.

**What it is used for.** `research/analysis/water-availability.js` and `delivery.py`, which
ask what fraction of real fires have an adequate water source in range and how a day's
delivery compares with a real fire's perimeter. It is not read by the page.

**Two things to be honest about.** The 10 ha floor excludes the thousands of small starts
BCWS records each year that are out before anything flies, so this is the population that
gets an aviation response and not the population of fires. And **perimeter lengths computed
from these rings are lower bounds** — Douglas-Peucker simplification shortens a convoluted
edge, and a fire's final mapped footprint is not the line anyone built.

---

## Per-file provenance sidecars

Every file in `data/` has a machine-readable `<name>.prov.json` beside it with the same
facts in structured form: `source`, `publisher`, `licence`, `licenceUrl`, `attribution`,
`retrievedAt`, `generator`, `notes`. Where a value is genuinely unknown it is `null` and
the reason is given in `notes`. Nothing in those files is guessed.
