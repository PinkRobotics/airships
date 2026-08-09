/* The fleet roster and the top-fires list.
 */
import { CLASSES, PHASE_TINT, fmt, fmtMin, srcName, stateAt } from '../../sim/index.js';
import { timeSinceDrop } from '../cockpit/panels.js';
import { $, SHORT, esc } from '../dom.js';
import { needsShip } from '../feeds.js';
import { FLEET } from '../fleet.js';
import { select } from '../map/interact.js';
import { S } from '../store.js';

export function renderFires() {
  const el = $("firesTop");
  if (!el) return;
  const top = S.fires.filter(needsShip).slice().sort((a, b) => b.sizeHa - a.sizeHa).slice(0, 8);
  el.innerHTML = `<table class="fleettab"><tbody>` + top.map(f => {
    const m = f.mission;
    return `<tr class="r-ship" data-fid="${esc(f.id)}">` +
      `<td>${esc(f.name || f.geo || f.id)}</td>` +
      `<td style="text-align:right">${fmt(f.sizeHa)} ha</td>` +
      `<td class="dropt" style="text-align:right">…</td>` +
      `<td style="text-align:right">${m && !m.idle ? fmt(m.plan.tph) + " kL/h" : "waits"}</td></tr>`;
  }).join("") + "</tbody></table>";
  el.querySelectorAll("tr.r-ship").forEach(tr => tr.addEventListener("click", () => {
    const f = S.fires.find(x => x.id === tr.dataset.fid);
    if (!f) return;
    if (f.mission && !f.mission.idle) select({ type: "ship", m: f.mission });
    else select({ type: "fire", f, m: f.mission });
  }));
  updateFires();
}

export function updateFires() {
  const el = $("firesTop");
  if (!el) return;
  el.querySelectorAll("tr.r-ship").forEach(tr => {
    const f = S.fires.find(x => x.id === tr.dataset.fid);
    const cell = tr.querySelector(".dropt");
    if (!f || !cell) return;
    const m = f.mission;
    if (!m || m.idle) { cell.textContent = "—"; return; }
    const since = timeSinceDrop(m);
    cell.textContent = since === null ? "inbound" : "-" + fmtMin(since / 60);
  });
}

export function renderRoster() {
  const el = $("roster");
  if (!el) return;
  const body = FLEET.map(([clsId, count]) => {
    const ships = S.missions.map((m, i) => ({ m, i })).filter(x => x.m.cls && x.m.cls.id === clsId);
    const head = `<tr class="r-clsrow"><td colspan="3"><button class="r-cls" data-hl="${clsId}" ` +
      `aria-pressed="${S.hlClass === clsId}">${CLASSES[clsId].name} ×${count}</button></td></tr>`;
    const rows = ships.map(({ m, i }) =>
      `<tr class="r-ship${S.sel && S.sel.m === m ? " sel" : ""}" data-mi="${i}" title="${esc(m.why || "")}">` +
      `<td class="r-name">${esc(m.name || m.shipId || "?")}</td>` +
      `<td>${esc(m.fire.name || m.fire.geo || m.fire.id)}</td>` +
      `<td class="ph">…</td></tr>`).join("");
    return head + rows;
  }).join("");
  el.innerHTML = `<table class="fleettab"><tbody>${body}</tbody></table>`;
  el.querySelectorAll("tr.r-ship").forEach(tr => tr.addEventListener("click", () => {
    APP.selRow(+tr.dataset.mi);
  }));
  el.querySelectorAll(".r-cls").forEach(b => b.addEventListener("click", e => {
    e.stopPropagation();
    S.hlClass = S.hlClass === b.dataset.hl ? null : b.dataset.hl;
    el.querySelectorAll(".r-cls").forEach(x => x.setAttribute("aria-pressed", String(S.hlClass === x.dataset.hl)));
  }));
  updateRoster();
}

export function updateRoster() {
  const el = $("roster");
  if (!el) return;
  el.querySelectorAll("tr.r-ship").forEach(tr => {
    const m = S.missions[+tr.dataset.mi];
    if (!m || m.idle) return;
    const st = stateAt(m, S.simTime);
    const ph = tr.querySelector(".ph");
    const txt = st.stopped ? "no power" : SHORT[st.phase];
    if (ph && ph.textContent !== txt) ph.textContent = txt;
    tr.classList.toggle("sel", !!(S.sel && S.sel.m === m));
  });
}

/* ---------- fleet UI ------------------------------------------------------------------------ */

export function renderStats() {
  // The header stat line was retired; the elements survive on no page. Guard and skip.
  if (!$("fsFires")) return;
  const act = S.missions.filter(m => !m.idle);
  const n = { P100: 0, P1000: 0, P10000: 0 };
  let tph = 0;
  for (const m of act) { n[m.cls.id]++; tph += m.plan.tph; }
  $("fsFires").textContent = fmt(S.fires.length);
  $("fsNote").textContent = fmt(S.fires.filter(f => f.note).length) + " · " + fmt(S.fires.filter(f => f.status === "Out of Control").length);
  $("fsShips").textContent = `${n.P100}/10 · ${n.P1000}/5 · ${n.P10000}/1`;
  $("fsRate").textContent = fmt(Math.round(tph / 100) * 100) + (S.uncovered ? " · " + S.uncovered + " wait" : "");
}

export function renderTable() {
  if (!$("ftbody")) return;   // the flat mission table lives on no page now; roster covers it
  const rows = S.missions.map((m, i) => {
    const f = m.fire;
    return `<tr><td><button onclick="APP.selRow(${i})">${esc(f.id)}</button>${f.note ? " ★" : ""}</td>` +
      `<td>${esc(f.status)}</td><td class="num">${fmt(f.sizeHa)}</td>` +
      (m.idle ? `<td colspan="4">no suitable mapped source</td>` :
        `<td>${m.cls.name}</td><td>${esc(srcName(m))}</td><td class="num">${m.oneWayKm.toFixed(1)}</td>` +
        `<td class="num">${fmt(m.plan.cycleMin)}</td>`) +
      `<td class="num">${m.idle ? "—" : fmt(m.plan.tph)}</td>` +
      `<td class="phase">${m.idle ? "idle" : ""}</td></tr>`;
  });
  $("ftbody").innerHTML = rows.join("");
}
setInterval(() => {
  updateRoster();
  updateFires();
  const cells = document.querySelectorAll("#ftbody td.phase");
  if (!cells.length || document.hidden) return;
  S.missions.forEach((m, i) => {
    if (!m.idle && cells[i]) {
      const stt = stateAt(m, S.simTime);
      cells[i].innerHTML = `<span style="color:${PHASE_TINT[stt.phase]}">${stt.label}</span>`;
    }
  });
}, 2500);

/* ---------- assumptions + worked example ----------------------------------------------------- */
