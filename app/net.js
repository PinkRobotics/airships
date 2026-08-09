/* Fetching, with a cache and a timeout. Knows about HTTP; knows nothing about fires.
 */
/* ============================================================================================
 * Application: data, map, interface. Everything below is presentation; the model is above.
 * ============================================================================================ */

export const FIRES_URL = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BCWS_ActiveFires_PublicView/FeatureServer/0/query" +
  "?where=" + encodeURIComponent("FIRE_STATUS <> 'Out'") +
  "&outFields=FIRE_NUMBER,FIRE_STATUS,FIRE_CAUSE,INCIDENT_NAME,GEOGRAPHIC_DESCRIPTION,CURRENT_SIZE,IGNITION_DATE,FIRE_URL,FIRE_OF_NOTE_IND,RESPONSE_TYPE_DESC" +
  "&returnGeometry=true&outSR=4326&f=geojson";

export const PERIMS_URL = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BCWS_FirePerimeters_PublicView/FeatureServer/0/query" +
  "?where=" + encodeURIComponent("FIRE_STATUS <> 'Out'") +
  "&outFields=FIRE_NUMBER,FIRE_STATUS,FIRE_SIZE_HECTARES,TRACK_DATE&returnGeometry=true&outSR=4326&maxAllowableOffset=0.002&f=geojson";

export async function fetchJSON(url, ms) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), ms || 15000);
  try {
    const r = await fetch(url, { signal: ctl.signal });
    if (!r.ok) throw new Error("HTTP " + r.status);
    return await r.json();
  } finally { clearTimeout(t); }
}

/* Courtesy cache. These are emergency-services feeds under real load; this page must not
   add to it meaningfully. Every remote source is cached in localStorage with a TTL matched
   to how often the source actually updates — reloads and extra tabs cost the origin nothing
   until the data could actually have changed. Ages stay honest: a cached fire feed shows
   its true fetch time, not the reload time. */
export async function cachedJSON(key, url, ttlMs, timeoutMs) {
  const K = "fleet:" + key;
  try {
    const raw = localStorage.getItem(K);
    if (raw) {
      const c = JSON.parse(raw);
      if (Date.now() - c.t < ttlMs) return { data: c.d, age: Date.now() - c.t };
    }
  } catch (e) { /* fall through to network */ }
  const d = await fetchJSON(url, timeoutMs);
  try { localStorage.setItem(K, JSON.stringify({ t: Date.now(), d })); } catch (e) { /* quota: fine */ }
  return { data: d, age: 0 };
}

/* The FIRST-PARTY mirror: tools/airships_live.py fetches the emergency feeds on a timer,
 * server-side, and publishes them under data/live/ as {fetchedAt, data}. Visitors read the
 * mirror, so page traffic never multiplies load on the BC Wildfire Service or CWFIS — one
 * fetch per interval total, not one per viewer. The direct feed remains only as a fallback
 * for when the mirror is missing or has gone stale (the refresh job died), so honesty about
 * data age survives either path. The ?ts bucket busts any intermediate HTTP cache politely
 * — one new URL per five minutes. */
export async function mirrorJSON(name, maxAgeMin, timeoutMs) {
  const j = await fetchJSON("data/live/" + name + ".json?ts=" + Math.floor(Date.now() / 300000),
    timeoutMs || 12000);
  const age = Date.now() - Date.parse(j.fetchedAt);
  if (!(age > -600000 && age < maxAgeMin * 60000)) throw new Error("mirror stale");
  return { data: j.data, age: Math.max(0, age) };
}
