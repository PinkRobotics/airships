/* Level 1 — the catalog browser, and the shell page's number bindings.
 *
 * Two panes over one CATALOG: each pane holds a category and an index, arrows page
 * through, and the two panes exist so any two parts can be read side by side — a chord
 * pipe against the pencil tube it protects, a printed node against the sleeve that
 * retires it. All displayed numbers come from catalog.js (which reads the committed
 * model where the model knows); the HTML prose carries none of its own digits.
 */
import { CATALOG, CATS, byCat, SHIP, ARTICLE } from './catalog.js?v=68fb2638';

const $ = (sel, root = document) => root.querySelector(sel);

/* ------------------------------------------------ number bindings ---------------------- */

const CTX = { ship: SHIP, article: ARTICLE };

function bindNumbers() {
  for (const el of document.querySelectorAll('[data-cat]')) {
    const path = el.dataset.cat.split('.');
    let v = CTX;
    for (const p of path) v = v?.[p];
    if (v === undefined || v === null) { el.textContent = '—'; el.classList.add('miss'); continue; }
    const f = el.dataset.f;
    el.textContent = typeof v === 'number'
      ? (f !== undefined ? v.toFixed(+f) : String(v)).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
      : String(v);
  }
}

/* ------------------------------------------------ svg helpers -------------------------- */

const NS = 'http://www.w3.org/2000/svg';
const svgEl = (inner, vb = '0 0 360 210') =>
  `<svg xmlns="${NS}" viewBox="${vb}" role="img">${inner}</svg>`;
const fmtMm = (mm) => mm >= 1000 ? `${(mm / 1000).toFixed(mm >= 10000 ? 0 : 1)} m` : `${mm.toFixed(mm < 20 ? 0 : 0)} mm`;

const C = { line: '#33333c', cool: '#7aa2c8', warm: '#ff4fa3', faint: '#74747f', bone: '#c9c3b6' };

/* Cross-section + side elevation, fitted per part; true wall proportion. */
function drawTube({ odMm, wallMm, cutMm }) {
  const R = 62;                                    // px radius of the section drawing
  const r = R * (1 - 2 * wallMm / odMm);
  const cx = 92, cy = 100;
  const barW = 168, barH = Math.max(10, Math.min(34, 34 * odMm / 200));
  const bx = 178, by = cy - barH / 2;
  return svgEl(`
    <circle cx="${cx}" cy="${cy}" r="${R}" fill="${C.cool}" fill-opacity="0.13" stroke="${C.cool}" stroke-width="2"/>
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="#0a0a0c" stroke="${C.cool}" stroke-width="1.4"/>
    <line x1="${cx - R}" y1="${cy + R + 16}" x2="${cx + R}" y2="${cy + R + 16}" stroke="${C.faint}" stroke-width="1"/>
    <text x="${cx}" y="${cy + R + 30}" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">⌀ ${fmtMm(odMm)} · wall ${wallMm.toFixed(1)} mm</text>
    <rect x="${bx}" y="${by}" width="${barW}" height="${barH}" rx="2"
          fill="${C.cool}" fill-opacity="0.13" stroke="${C.cool}" stroke-width="1.4"/>
    <line x1="${bx}" y1="${by + barH + 14}" x2="${bx + barW}" y2="${by + barH + 14}" stroke="${C.faint}" stroke-width="1"/>
    <line x1="${bx}" y1="${by + barH + 10}" x2="${bx}" y2="${by + barH + 18}" stroke="${C.faint}" stroke-width="1"/>
    <line x1="${bx + barW}" y1="${by + barH + 10}" x2="${bx + barW}" y2="${by + barH + 18}" stroke="${C.faint}" stroke-width="1"/>
    <text x="${bx + barW / 2}" y="${by + barH + 28}" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">cut ${fmtMm(cutMm)}</text>`);
}

/* The clamshell: tube passing through, two half-shells parted, seam flanges, lap bracket. */
function drawSleeve({ lapMm }) {
  const cy = 100, tubeH = 26, x0 = 40, x1 = 320;
  const shellX = 130, shellW = 110, part = 14;
  return svgEl(`
    <rect x="${x0}" y="${cy - tubeH / 2}" width="${x1 - x0}" height="${tubeH}" rx="3"
          fill="${C.cool}" fill-opacity="0.10" stroke="${C.cool}" stroke-width="1.4"/>
    <path d="M ${shellX} ${cy - tubeH / 2 - part} h ${shellW} a 8 8 0 0 0 8 -8 v -6 a 22 22 0 0 0 -22 -22 h -82 a 22 22 0 0 0 -22 22 v 6 a 8 8 0 0 0 8 8 z"
          fill="${C.warm}" fill-opacity="0.10" stroke="${C.warm}" stroke-width="1.6"/>
    <path d="M ${shellX} ${cy + tubeH / 2 + part} h ${shellW} a 8 8 0 0 1 8 8 v 6 a 22 22 0 0 1 -22 22 h -82 a 22 22 0 0 1 -22 -22 v -6 a 8 8 0 0 1 8 -8 z"
          fill="${C.warm}" fill-opacity="0.10" stroke="${C.warm}" stroke-width="1.6"/>
    <line x1="${shellX - 4}" y1="${cy - tubeH / 2 - part}" x2="${shellX + shellW + 4}" y2="${cy - tubeH / 2 - part}" stroke="${C.warm}" stroke-width="1" stroke-dasharray="3 3"/>
    <line x1="${shellX - 4}" y1="${cy + tubeH / 2 + part}" x2="${shellX + shellW + 4}" y2="${cy + tubeH / 2 + part}" stroke="${C.warm}" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="180" y="34" fill="${C.warm}" font-size="11" text-anchor="middle" font-family="monospace">two halves close radially</text>
    <line x1="${shellX}" y1="${cy + tubeH / 2 + 58}" x2="${shellX + shellW}" y2="${cy + tubeH / 2 + 58}" stroke="${C.faint}" stroke-width="1"/>
    <text x="${shellX + shellW / 2}" y="${cy + tubeH / 2 + 72}" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">bonded lap ≈ ${lapMm} mm/end</text>
    <text x="180" y="${cy + 4}" fill="${C.cool}" font-size="11" text-anchor="middle" font-family="monospace">tube stays put</text>`);
}

/* A hub with radiating arm stubs. */
function drawNode({ arms, hubMm }) {
  const cx = 180, cy = 105, hubR = Math.min(46, 16 + hubMm / 6);
  let out = `<circle cx="${cx}" cy="${cy}" r="${hubR}" fill="${C.warm}" fill-opacity="0.10" stroke="${C.warm}" stroke-width="1.8"/>`;
  for (let i = 0; i < arms; i++) {
    const a = (i / arms) * 2 * Math.PI - Math.PI / 2;
    const len = 52, w = Math.max(10, hubR * 0.42);
    const x = cx + Math.cos(a) * (hubR - 2), y = cy + Math.sin(a) * (hubR - 2);
    const deg = a * 180 / Math.PI;
    out += `<rect x="${x}" y="${-w / 2 + y}" width="${len}" height="${w}" rx="${w / 2}"
             transform="rotate(${deg} ${x} ${y})"
             fill="${C.cool}" fill-opacity="0.13" stroke="${C.cool}" stroke-width="1.4"/>`;
  }
  out += `<text x="${cx}" y="18" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">${arms} arms shown · sockets swallow the tube ends</text>`;
  return svgEl(out);
}

/* Two members overlapping; the glue band is the highlighted part. */
function drawLap({ lapMm }) {
  const cy = 100, h = 24;
  return svgEl(`
    <rect x="30" y="${cy - h / 2}" width="180" height="${h}" rx="3" fill="${C.cool}" fill-opacity="0.10" stroke="${C.cool}" stroke-width="1.4"/>
    <rect x="150" y="${cy - h / 2 - 14}" width="180" height="${h}" rx="3" fill="${C.cool}" fill-opacity="0.10" stroke="${C.cool}" stroke-width="1.4"/>
    <rect x="150" y="${cy - h / 2 - 7}" width="60" height="${h + 7}" fill="${C.warm}" fill-opacity="0.30" stroke="${C.warm}" stroke-width="1"/>
    <text x="180" y="${cy + 52}" fill="${C.warm}" font-size="11" text-anchor="middle" font-family="monospace">the lap: load path and gas seal, one part</text>
    <line x1="150" y1="${cy - h / 2 - 24}" x2="210" y2="${cy - h / 2 - 24}" stroke="${C.faint}" stroke-width="1"/>
    <text x="180" y="${cy - h / 2 - 32}" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">${lapMm} mm</text>`);
}

/* A layer stack, thickness bars scaled by areal mass. */
function drawFilm({ layers }) {
  const x = 70, w = 220; let y = 60, out = '';
  for (const L of layers) {
    const h = Math.max(10, Math.min(44, 8 + L.gsm * 0.55));
    out += `<rect x="${x}" y="${y}" width="${w}" height="${h}"
             fill="${C.cool}" fill-opacity="0.13" stroke="${C.cool}" stroke-width="1.4"/>
            <text x="${x + w + 10}" y="${y + h / 2 + 4}" fill="${C.faint}" font-size="11" font-family="monospace">${L.gsm.toFixed(0)} g/m²</text>
            <text x="${x - 10}" y="${y + h / 2 + 4}" fill="${C.bone}" font-size="11" text-anchor="end" font-family="monospace">${L.name}</text>`;
    y += h + 6;
  }
  out += `<path d="M ${x} ${y + 22} q ${w / 2} -26 ${w} 0" fill="none" stroke="${C.warm}" stroke-width="1.4" stroke-dasharray="4 3"/>
          <text x="${x + w / 2}" y="${y + 44}" fill="${C.warm}" font-size="11" text-anchor="middle" font-family="monospace">formed, not flat</text>`;
  return svgEl(out);
}

const DRAW = { tube: drawTube, sleeve: drawSleeve, node: drawNode, lap: drawLap, film: drawFilm };

/* True-relative-size strip: every tube in the catalog on one scale, active one lit. */
function tubeStrip(activeId) {
  const tubes = byCat('tubes');
  const maxOd = Math.max(...tubes.map(t => t.draw.odMm));
  const w = 340, pad = 26, innerW = w - 2 * pad;
  const gaps = 30 * (tubes.length - 1);
  const pxPerMm = Math.min(0.62, (innerW - gaps) / tubes.reduce((s, t) => s + t.draw.odMm, 0));
  let x = pad, out = '';
  for (const t of tubes) {
    const r = Math.max(2.4, t.draw.odMm * pxPerMm / 2);
    const on = t.id === activeId;
    x += r;
    out += `<circle cx="${x}" cy="46" r="${r}" fill="${on ? C.warm : C.cool}" fill-opacity="${on ? 0.35 : 0.10}"
             stroke="${on ? C.warm : C.faint}" stroke-width="${on ? 1.8 : 1}"/>`;
    if (on) out += `<text x="${x}" y="${46 + Math.max(r, 8) + 16}" fill="${C.warm}" font-size="10" text-anchor="middle" font-family="monospace">${fmtMm(t.draw.odMm)}</text>`;
    x += r + 30;
  }
  out += `<text x="${pad}" y="14" fill="${C.faint}" font-size="10" font-family="monospace">every tube, true relative bore</text>`;
  return svgEl(out, `0 0 ${w} ${Math.max(96, maxOd * pxPerMm + 66)}`);
}

/* ------------------------------------------------ the pane ----------------------------- */

const STATUS = {
  proven:     { label: 'proven on the article', cls: 'st-proven' },
  decided:    { label: 'decided',               cls: 'st-decided' },
  scoping:    { label: 'scoping',               cls: 'st-scoping' },
  superseded: { label: 'superseded',            cls: 'st-dead' },
};

function makePane(mount, catId, startIdx = 0) {
  let cat = catId, idx = startIdx;

  function render() {
    const items = byCat(cat);
    if (idx >= items.length) idx = 0;
    const it = items[idx];
    const st = STATUS[it.status];
    mount.innerHTML = `
      <div class="tabs" role="tablist">
        ${CATS.map(c => `<button role="tab" data-tab="${c.id}" aria-selected="${c.id === cat}"
           class="${c.id === cat ? 'on' : ''}">${c.name}</button>`).join('')}
      </div>
      <figure class="part-fig">${DRAW[it.draw.kind](it.draw)}</figure>
      <div class="part-head">
        <h3>${it.name}</h3>
        <span class="chip ${st.cls}">${st.label}</span>
      </div>
      <p class="part-role">${it.role}</p>
      <dl class="specs">
        ${it.specs.map(s => `<div><dt>${s.k}</dt><dd>${s.v} <span class="unit-sm">${s.u}</span></dd></div>`).join('')}
      </dl>
      <p class="part-story">${it.story}</p>
      ${it.flags.length ? `<ul class="flags">${it.flags.map(f => `<li>${f}</li>`).join('')}</ul>` : ''}
      <p class="prov">${it.prov}</p>
      ${cat === 'tubes' ? `<div class="strip">${tubeStrip(it.id)}</div>` : ''}
      <div class="pager">
        <button class="arrow" data-nav="-1" aria-label="previous part">‹</button>
        <span class="pos mono">${idx + 1} / ${items.length}</span>
        <button class="arrow" data-nav="1" aria-label="next part">›</button>
      </div>`;
    mount.querySelectorAll('[data-tab]').forEach(b =>
      b.addEventListener('click', () => { cat = b.dataset.tab; idx = 0; render(); }));
    mount.querySelectorAll('[data-nav]').forEach(b =>
      b.addEventListener('click', () => {
        const n = byCat(cat).length;
        idx = (idx + +b.dataset.nav + n) % n;
        render();
      }));
  }
  render();
}

/* ------------------------------------------------ boot --------------------------------- */

bindNumbers();
makePane($('#pane-a'), 'tubes');
makePane($('#pane-b'), 'connectors');
