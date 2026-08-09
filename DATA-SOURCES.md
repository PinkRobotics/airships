# Data sources, licences and attribution

The wildfire data in this project is real and comes from public agencies. The fleet is
imagined. This file states, for every dataset the repository redistributes and every
service the page calls at runtime: what it is, who publishes it, the exact licence, the
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
| 6 | Esri World Imagery basemap tiles | none — fetched by the visitor's browser | **unresolved; see below** |
| 7 | Open-Meteo 850 hPa wind forecast | none — fetched by the visitor's browser | CC BY 4.0 |

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

**Load discipline.** The page never sends a visitor to the BCWS service if it can avoid it.
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

**What it is.** Two thin vector layers drawn for orientation only: highway centrelines
(`data/roads-bc.json`, 294 polylines, 3032 vertices) and the British Columbia provincial
boundary including its islands (`data/bc-outline.json`, 23 rings, 804 vertices). Neither is
used by the model. They exist so that a reader can tell where they are looking.

**Publisher.** Natural Earth — Tom Patterson, Nathaniel Vaughn Kelso, and contributors.
<https://www.naturalearthdata.com/>

**Licence.** Public domain. The terms of use
(<https://www.naturalearthdata.com/about/terms-of-use/>) say:

> All versions of Natural Earth raster + vector map data found on this website are in the
> public domain. […] No permission is needed to use Natural Earth. Crediting the authors is
> unnecessary.

No attribution is required. Natural Earth requests the following credit if you wish to give
one, and this project gives it:

> Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.

**How the provenance was established.** These two files arrived in the repository with no
generator script and no recorded source, which was a publication risk: if they had been
OpenStreetMap-derived, ODbL share-alike would attach to the project. They are not. Every
vertex was matched against Natural Earth, and the match is exact:

- `data/roads-bc.json` — all 3032 vertices are present, to the full three decimal places
  they are stored at, in the `ne_10m_roads` layer of `nvkelso/natural-earth-vector` within
  this bounding box. 3032 of 3032.
- `data/bc-outline.json` — all 804 vertices are present in the `ne_50m_admin_1_states_provinces`
  feature named "British Columbia", and the file's 23 rings correspond one-to-one with that
  feature's 23 polygon parts. 804 of 804.

An identity match of that size is not coincidence. The comparison was made against
`natural-earth-vector` at version 5.2.0-pre; the exact release the files were originally
cut from is not recorded, and Natural Earth geometry does change between releases, so
treat the version as "5.x" rather than a specific number.

**How they were processed** (reconstructed from the match, since no script was committed):

- Roads: clipped to roughly longitude −137.5°…−112°, latitude 47.3°…60.6°; `featurecla`
  of `Ferry` dropped, so ferry routes are absent and only road classes remain (Major
  Highway, Secondary Highway, Beltway, Road); Douglas–Peucker simplification, which removes
  about half the in-box vertices; coordinates rounded to three decimal places (≈100 m);
  properties discarded entirely, leaving a bare array of `[[lon,lat],…]` polylines.
- Outline: the British Columbia feature's outer rings only, simplified and rounded the same
  way, holes discarded.

**Outstanding.** There is no `pipeline/` script that regenerates these two files, so the
processing above is inferred rather than replayed. That is a documentation gap, not a
licensing one. The recommendation is to add a `pipeline/vectors.py` that reproduces both
from a pinned Natural Earth release, and delete this paragraph when it exists.

---

## 6. Esri World Imagery basemap tiles — an unresolved licensing problem

**What the page does.** When the satellite layer is on, `app/map/basemap.js` builds tile
URLs of the form

```
https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
```

and sets them as `<img>` sources. The requests come from **the visitor's browser**, not
from our server. There is no API key, no token, no ArcGIS account and no signed agreement
behind them. Up to 600 tiles are held in a client-side cache. The imagery is then
brightness- and saturation-adjusted before being drawn.

**What that means for the visitor.** Every tile request sends the visitor's IP address,
user agent, `Referer` and — through the tile coordinates themselves — exactly where on the
map they are looking, to a third party the visitor has not been told about. No consent is
asked. This is a privacy fact about the page, independent of the licensing question.

**What that means legally.** Esri's World Imagery service composites commercial satellite
and aerial imagery (Maxar, Earthstar Geographics, and national and regional providers) that
Esri licenses in; it is not open data. Access is governed by the Esri Master Agreement and
the ArcGIS Online terms of use
(<https://www.esri.com/en-us/legal/terms/full-master-agreement>), which contemplate use
through a licensed ArcGIS account, generally require the "Powered by Esri" attribution and
the source list, and prohibit accessing the service other than through Esri's own APIs and
licensed channels. Unkeyed direct tile fetching from `server.arcgisonline.com` by an
arbitrary web page is very likely outside those terms. The endpoint answering with HTTP 200
is not permission. The page does not currently display Esri's required attribution beyond
the word "Esri" in a status line, which would be insufficient even if the access itself
were licensed.

**This has not been resolved, and it should be resolved before publication.** Three
options, in the order they are recommended:

1. **Replace the layer** with an openly-licensed source and attribute it properly. The
   candidate for this footprint is Sentinel-2 cloudless or ESA Sentinel-2 L2A imagery
   (CC BY / open), self-hosted or served from an operator with terms that permit it. This
   costs work and some visual quality, and it ends the problem.
2. **Key it.** Obtain an ArcGIS Location Platform account, use an API key, respect the
   basemap tile quota, and render Esri's full attribution string in the map frame. This
   keeps the imagery, introduces a credential and a bill, and still sends visitor IPs to
   Esri — so the privacy note above stays true and should be disclosed.
3. **Drop the satellite layer.** The terrain hillshade in section 4 is our own render of
   openly-licensed elevation, it is already the default backdrop, and the page reads
   perfectly well without imagery. This is the zero-risk option and the one to take if
   nobody wants to own the decision.

Doing nothing is not on the list.

---

## 7. Open-Meteo — 850 hPa wind forecast

**What it is.** Wind speed and direction at the 850 hPa pressure level, roughly the band
the imagined ships cruise in, sampled at the midpoint of each active mission's route and
applied to transit times. When the fetch fails, or when `?data=snapshot` is set, the model
runs in still air and the page says so.

**Publisher.** Open-Meteo (Patrick Zippenfenig). Underlying numerical weather prediction
comes from national meteorological services.

**Licence.** Data is provided under CC BY 4.0. <https://open-meteo.com/en/license>

**Required attribution.** CC BY 4.0 requires credit to the source:

> Weather data by Open-Meteo.com

**Where it came from.** Called live from the visitor's browser by `app/feeds.js`:

```
https://api.open-meteo.com/v1/forecast
  ?latitude=<lat,lat,…>&longitude=<lon,lon,…>
  &hourly=wind_speed_850hPa,wind_direction_850hPa
  &forecast_hours=1&wind_speed_unit=kmh&timezone=UTC
```

One request covers all active missions as a comma-separated batch, and responses are cached
in the page for 20 minutes.

**Two things to be honest about.** First, like the Esri tiles, this call is made by the
visitor's browser, so it sends the visitor's IP address and the approximate coordinates
they are looking at to a third party. Second, Open-Meteo's free tier is limited to
non-commercial use and to 10,000 calls per day, 5,000 per hour and 600 per minute; those
limits are consumed per visitor, not per server, so they scale with traffic. A page hosted
on a company domain is at least arguably commercial use. If this project attracts real
traffic, move the wind fetch behind the same server-side mirror that already fronts the
fire feeds (`pipeline/live.py`), which fixes the rate limit, the privacy leak and the
commercial-use question at once.

---

## Per-file provenance sidecars

Every file in `data/` has a machine-readable `<name>.prov.json` beside it with the same
facts in structured form: `source`, `publisher`, `licence`, `licenceUrl`, `attribution`,
`retrievedAt`, `generator`, `notes`. Where a value is genuinely unknown it is `null` and
the reason is given in `notes`. Nothing in those files is guessed.
