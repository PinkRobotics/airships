/* Wiring the controls, reporting status, and starting the application.
 */
import * as SIM from '../sim/index.js';
import { CFG, DEFAULTS, PHASES, selftest, stateAt, resetConfig, setSeed } from '../sim/index.js';
import { M3D_SYS, M3D_SYS_CAM, m3d, m3dAz, m3dBreakSync, m3dCamMode, m3dFadeTo, m3dMode, m3dPhase, m3dVm, updSyncUI, setCamera, cameraMode } from './bridge/viz3d.js';
import { renderDrawer } from './cockpit/panels.js';
import { renderStats, renderTable } from './cockpit/tables.js';
import { $, esc } from './dom.js';
import { fetchHeat, fetchWind, loadLive } from './feeds.js';
import { rebuildMissions, replanAll } from './fleet.js';
import { frame } from './loop.js';
import { fitFires, fitFleet, focusMission, select } from './map/interact.js';
import { resize } from './map/projection.js';
import { fetchJSON } from './net.js';
import { S } from './store.js';
import { DIALS, renderWorked } from './worked.js';

export function wire() {
  $("btnPause").addEventListener("click", () => {
    S.paused = !S.paused;
    $("btnPause").textContent = S.paused ? "Resume" : "Pause";
    $("btnPause").setAttribute("aria-pressed", String(S.paused));
  });
  if (S.reduced) { $("btnPause").textContent = "Resume"; $("btnPause").setAttribute("aria-pressed", "true"); }
  document.querySelectorAll("[data-speed]").forEach(b => b.addEventListener("click", () => {
    S.speed = +b.dataset.speed;
    document.querySelectorAll("[data-speed]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
  }));
  document.querySelectorAll("[data-filter]").forEach(b => b.addEventListener("click", () => {
    S.filter = b.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
  }));
  document.querySelectorAll("[data-cls]").forEach(b => b.addEventListener("click", () => {
    S.exampleCls = b.dataset.cls;
    document.querySelectorAll("[data-cls]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    renderWorked();
  }));
  document.querySelectorAll("[data-mode]").forEach(b => b.addEventListener("click", () => {
    S.modeId = b.dataset.mode;
    document.querySelectorAll("[data-mode]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    replanAll();
  }));
  if ($("btnReset")) $("btnReset").addEventListener("click", () => {
    resetConfig();
    for (const dd of DIALS) { $("i_" + dd.k).value = CFG[dd.k]; $("o_" + dd.k).textContent = CFG[dd.k].toFixed(dd.d) + dd.unit; }
    replanAll();
  });
  ["Terrain", "Sat", "Hot", "Wind", "Places", "Perims", "Water", "Routes", "Labels"].forEach(nm => {
    $("tg" + nm).addEventListener("change", e => { S.layers[nm.toLowerCase()] = e.target.checked; });
  });
  $("btnFitFleet").addEventListener("click", fitFleet);
  $("btnFitFires").addEventListener("click", fitFires);
  // The split button flips the centre column between map-over-model and map-beside-model.
  // v2 key: vertical is THE default again for everyone; only a fresh explicit toggle
  // re-saves horizontal.
  S.split = localStorage.getItem("airshipsSplit2") === "h" ? "h" : "v";
  const applySplit = () => {
    $("cpMap").classList.toggle("split-h", S.split === "h");
    $("btnSplit").textContent = S.split === "h" ? "Split ◨" : "Split ⬒";
  };
  applySplit();
  $("btnSplit").addEventListener("click", () => {
    S.split = S.split === "h" ? "v" : "h";
    try { localStorage.setItem("airshipsSplit2", S.split); } catch (e) { /* private mode */ }
    applySplit();
  });
  $("btnLayers").addEventListener("click", () => {
    const lp = $("layersPanel");
    const open = lp.style.display !== "none";
    lp.style.display = open ? "none" : "flex";
    $("btnLayers").textContent = open ? "Layers ▾" : "Layers ▴";
  });
  $("btnFS").addEventListener("click", () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else $("monroot").requestFullscreen().catch(() => {});
  });
  document.addEventListener("fullscreenchange", () => {
    $("btnFS").textContent = document.fullscreenElement ? "Exit fullscreen" : "Fullscreen";
    resize();
  });
  document.querySelectorAll("[data-m3s]").forEach(b => b.addEventListener("click", () => {
    const k = b.dataset.m3s;
    setCamera({ panel: k });
    document.querySelectorAll("[data-m3s]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    $("m3dCustom").style.display = k === "custom" ? "flex" : "none";
    if (!m3d) return;
    if (k === "auto") setCamera({ phase: "", viewMode: "", mode: "sync", azimuth: null });
    else if (k === "shell") {
      m3dFadeTo(() => m3d.setProps({ viewMode: "exterior", systems: null }));
      setCamera({ viewMode: "exterior", mode: "sync", azimuth: null });
    } else if (k === "custom") applyM3DCustom();
    else if (k === "vacuum") {
      // The vacuum story gets its own view mode: a cutaway with the whole free interior
      // packed with pink cell-volume spheres, everything else ghosted.
      m3dFadeTo(() => m3d.setProps({ viewMode: "vacuum", systems: null }));
      setCamera({ viewMode: "vacuum" });
      setCamera({ mode: "presetHold" });
      m3d.goToPreset("side");
    }
    else if (M3D_SYS[k]) {
      m3dFadeTo(() => m3d.setProps({ viewMode: "systems", systems: M3D_SYS[k] }));
      setCamera({ viewMode: "systems" });
      setCamera({ mode: "presetHold" });              // hold this subject until resynced
      m3d.goToPreset(M3D_SYS_CAM[k] || "three-quarter");
    }
    updSyncUI();
  }));
  document.querySelectorAll("[data-m3c]").forEach(b => b.addEventListener("click", () => {
    if (b.dataset.m3c === "sync") setCamera({ mode: "sync", azimuth: null });
    else {
      setCamera({ mode: "preset" });
      if (m3d) m3d.goToPreset(b.dataset.m3c);
    }
    updSyncUI();
  }));
  $("m3dView").addEventListener("pointerdown", m3dBreakSync);
  // A wheel zoom is a softer break than a drag: the heading keeps following, the user's
  // distance is respected, and the sync light goes off until ⟳ Sync is pressed.
  $("m3dView").addEventListener("wheel", () => {
    if (cameraMode() === "sync") { setCamera({ mode: "syncManual" }); updSyncUI(); }
  }, { passive: true });
  // the custom panel: any base view, any mix of systems, a movable cut plane
  const CATS = ["structure", "vacuum", "water", "cryogenic", "power", "propulsion", "control", "sensors", "compute", "maintenance"];
  $("m3cCats").innerHTML = CATS.map(c =>
    `<label style="margin-right:8px;white-space:nowrap"><input type="checkbox" data-m3cat="${c}" checked style="accent-color:var(--warm)">${c}</label>`).join("");
  function applyM3DCustom() {
    if (!m3d) return;
    const on = [...document.querySelectorAll("[data-m3cat]")].filter(x => x.checked).map(x => x.dataset.m3cat);
    m3d.setProps({
      viewMode: $("m3cView").value,
      systems: on.length === CATS.length ? null : on,
      cutFrac: parseFloat($("m3cCut").value),
    });
    setCamera({ viewMode: $("m3cView").value });
  }
  $("m3cView").addEventListener("change", () => { if (panelMode() === "custom") applyM3DCustom(); });
  $("m3cCut").addEventListener("input", () => { if (panelMode() === "custom") applyM3DCustom(); });
  document.querySelectorAll("[data-m3cat]").forEach(x => x.addEventListener("change", () => { if (panelMode() === "custom") applyM3DCustom(); }));
}
window.APP = {
  selRow(i) { select({ type: "ship", m: S.missions[i] }); $("monroot").scrollIntoView({ behavior: "smooth", block: "start" }); },
  selShip() { if (S.sel && S.sel.m) select({ type: "ship", m: S.sel.m }); },
  step(dir) {
    if (!S.sel || !S.sel.m || S.sel.m.idle) return;
    const m = S.sel.m;
    const st = stateAt(m, S.simTime);
    const target = (st.idx + dir + PHASES.length) % PHASES.length;
    const startOfTarget = target ? m.phaseEnds[target - 1] : 0;
    const cur = ((S.simTime + m.offset * m.cycleSec) % m.cycleSec + m.cycleSec) % m.cycleSec;
    S.simTime += (startOfTarget - cur + 1) + (dir > 0 && target === 0 ? m.cycleSec : 0);
    renderDrawer();
  },
};

/* ---------- status line ------------------------------------------------------------------------ */

export function renderStatus() {
  const hl = $("hudLive");
  if (S.usingFallback) {
    hl.classList.add("warn");
    hl.innerHTML = `<b>DATA SNAPSHOT</b> · ${esc((S.snapshotDate || "").slice(0, 10))} · live feed unreachable`;
  } else {
    hl.classList.remove("warn");
    const t = S.fetchedAt.toLocaleTimeString("en-CA", { hour: "2-digit", minute: "2-digit" });
    hl.innerHTML = `<b>BC FIRE DATA</b> · ${S.fires.length} fires · fetched ${t}`;
  }
  const age = () => {
    const mins = Math.round((Date.now() - S.fetchedAt.getTime()) / 60000);
    $("dataline").textContent =
      (S.usingFallback
        ? `Showing the bundled data snapshot from ${(S.snapshotDate || "").replace("T", " ").slice(0, 16)} UTC — the live BC Wildfire Service feed could not be reached from your browser. `
        : `Live fire points and perimeters fetched ${mins} min ago from the BC Wildfire Service public feed (refreshed from operational systems roughly every 15 minutes; individual incidents can lag). `) +
      `This page refetches every 15 minutes, and every source is cached in your browser (5–30 min by source) so extra tabs and reloads add nothing to the emergency feeds' load. ` +
      (S.windOk ? `Winds: live 850 hPa (≈ the cruise band) per route from Open-Meteo, applied to transit times; altitude profiles remain nominal. `
                : `Winds: unavailable — still-air transit times; altitudes nominal. `) +
      `Simulation clock ${S.paused ? "paused" : "running at " + S.speed + "×"}${S.reduced ? " (reduced motion honoured: use the phase buttons in a ship's panel)" : ""}.`;
  };
  age();
  clearInterval(renderStatus._t); renderStatus._t = setInterval(age, 30000);
}

/* ---------- boot -------------------------------------------------------------------------------- */

/* Deterministic replay. `?seed=N` pins every choice the model makes, and `?data=snapshot`
 * (read in feeds.js) pins its inputs. The URL is parsed here, in the application, so that
 * nothing in sim/ needs to know a browser exists.
 *
 * Together they make a run reproducible: the same link shows another person exactly what
 * you were looking at, and the golden-output tests have something stable to compare. */
{
  const seed = new URLSearchParams(location.search).get('seed');
  if (seed) setSeed(seed);
}

export async function boot() {
  resize(); wire();
  try {
    const [outline, waterDoc, roads] = await Promise.all([
      fetchJSON("data/bc-outline.json", 20000),
      fetchJSON("data/water-bc.json", 30000),
      fetchJSON("data/roads-bc.json", 20000).catch(() => []),
    ]);
    S.outline = outline;
    S.roads = roads;
    // ringed lakes get true bounding boxes: a long lake must render (and cull) by its
    // real extent, not by a circle around a centroid that may be 60 km off-screen
    for (const w of waterDoc.water) {
      if (!w[5]) continue;
      let x0 = 999, x1 = -999, y0 = 999, y1 = -999;
      for (const q of w[5]) {
        if (q[0] < x0) x0 = q[0]; if (q[0] > x1) x1 = q[0];
        if (q[1] < y0) y0 = q[1]; if (q[1] > y1) y1 = q[1];
      }
      w.bb = [x0, y0, x1, y1];
      w.spanKm = Math.max((x1 - x0) * 111.32 * Math.cos(w[1] * Math.PI / 180), (y1 - y0) * 110.57) / 2;
    }
    S.water = waterDoc.water;
    S.waterMeta = waterDoc;
    const wd = $("waterDate"); if (wd && waterDoc.generated) wd.textContent = waterDoc.generated.slice(0, 10);
  } catch (e) {
    $("dataline").textContent = "Could not load the page's bundled map data (" + e.message + ").";
    return;
  }
  S.fires = await loadLive();
  rebuildMissions();
  for (const m of S.missions) if (!m.idle) S.water[m.waterIdx].used = true;
  renderStats(); renderTable(); renderWorked(); renderStatus();
  fitFires();
  // Open on the largest fire the fleet is actually working, so the cockpit starts occupied
  // rather than empty. A rule, not a named incident: every fire in the feed is out within
  // weeks, and a hardcoded fire number would leave the page opening on nothing.
  // Ties break on fire number so the same feed always selects the same ship.
  let pick = null;
  for (const m of S.missions) {
    if (m.idle) continue;
    if (!pick || m.fire.sizeHa > pick.fire.sizeHa ||
        (m.fire.sizeHa === pick.fire.sizeHa && m.fire.id < pick.fire.id)) pick = m;
  }
  if (pick) { S.sel = { type: "ship", m: pick }; S.follow = true; renderDrawer(); focusMission(pick); }
  fetchWind(); fetchHeat();
  S.ready = true;   // resize() may now repaint synchronously
  // First visit: one orientation screen, one tap to dismiss, remembered per browser.
  try {
    if (!localStorage.getItem("airshipsIntroSeen")) {
      const ov = $("introOv");
      ov.hidden = false;
      ov.addEventListener("click", () => {
        ov.hidden = true;
        try { localStorage.setItem("airshipsIntroSeen", "1"); } catch (e) { /* fine */ }
      }, { once: true });
    }
  } catch (e) { /* private mode: no overlay persistence, no overlay crash */ }
  requestAnimationFrame(frame);
  setInterval(async () => {
    if (document.hidden) return;
    try {
      S.fires = await loadLive();
      const selFire = S.sel ? (S.sel.f || S.sel.m.fire).id : null;
      const selType = S.sel ? S.sel.type : null;
      for (const w of S.water) w.used = false;
      rebuildMissions();
      for (const m of S.missions) if (!m.idle) S.water[m.waterIdx].used = true;
      if (selFire) {
        const ff = S.fires.find(x => x.id === selFire);
        if (!ff) S.sel = null;
        else if (selType === "fire") S.sel = { type: "fire", f: ff, m: ff.mission };
        else S.sel = ff.mission ? { type: selType, m: ff.mission } : null;
      }
      renderStats(); renderTable(); renderStatus(); renderDrawer();
      fetchWind(); fetchHeat();
    } catch (e) { /* keep the current picture; next tick retries */ }
  }, 900000);
  if (location.search.indexOf("selftest=1") >= 0) {
    try { const r = selftest(); console.log(r); document.title += " · " + r; }
    catch (e) { console.error(e.message); document.title += " · " + e.message; }
  }
}

document.addEventListener("visibilitychange", () => { S.lastFrame = null; });
/* The page is an ES module, so nothing it declares is global. These two are published
 * deliberately: `APP` because the markup binds to it, and `AIRSHIPS` so that anyone reading
 * the page can re-run the model in their own devtools console without cloning anything —
 * `AIRSHIPS.sim.selftest()` runs every assertion, and
 * `AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P100, AIRSHIPS.sim.MODES.balanced, 15)`
 * recomputes a published figure from scratch. Arithmetic nobody can re-run is just a claim.
 *
 * `APP` does only what the on-page controls do — select a ship, step its phase — and
 * `AIRSHIPS` is a read handle. Neither can edit the model's state or its assumptions: a
 * console visitor can inspect and recompute, not rewrite. */
window.AIRSHIPS = { sim: SIM, app: S, stateAt };

boot();
