/* Level 1 — the catalog browser, and the shell page's number bindings.
 *
 * Two panes over one CATALOG: each pane holds a category and an index, arrows page
 * through, and the two panes exist so any two parts can be read side by side — a chord
 * pipe against the pencil tube it protects, a printed node against the sleeve that
 * retires it. All displayed numbers come from catalog.js (which reads the committed
 * model where the model knows); the HTML prose carries none of its own digits.
 */
import { CATALOG, CATS, byCat, SHIP, ARTICLE, BAND, GRID } from './catalog.js?v=75e59915';

const $ = (sel, root = document) => root.querySelector(sel);

/* ------------------------------------------------ number bindings ---------------------- */

const CTX = { ship: SHIP, article: ARTICLE, band: BAND, grid: GRID };

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

/* The seat & strap: a bearing pad presses the cell onto the chord; a light strap holds it. */
function drawSeat() {
  const cx = 180;
  return svgEl(`
    <path d="M 96 44 L 140 28 H 220 L 264 44" fill="none" stroke="${C.warm}" stroke-width="1.3"/>
    <text x="${cx}" y="18" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">cell underside — the UNLOADED film side</text>
    <rect x="${cx - 45}" y="44" width="90" height="18" rx="8"
          fill="${C.warm}" fill-opacity="0.12" stroke="${C.warm}" stroke-width="1.6"/>
    <text x="${cx + 56}" y="57" fill="${C.warm}" font-size="9.5" font-family="monospace">clamp sleeve</text>
    <rect x="${cx - 13}" y="64" width="26" height="18" rx="2"
          fill="${C.warm}" fill-opacity="0.35" stroke="${C.warm}" stroke-width="1.6"/>
    <text x="${cx + 22}" y="77" fill="${C.warm}" font-size="9.5" font-family="monospace">bearing seat</text>
    <line x1="60" y1="100" x2="300" y2="100" stroke="${C.cool}" stroke-width="2"/>
    <circle cx="${cx}" cy="100" r="12" fill="${C.cool}" fill-opacity="0.15" stroke="${C.cool}" stroke-width="1.8"/>
    <text x="64" y="118" fill="${C.cool}" font-size="10" font-family="monospace">outer chord</text>
    <line x1="90" y1="30" x2="90" y2="52" stroke="${C.warm}" stroke-width="1.5"/>
    <path d="M 86 46 L 90 56 L 94 46 Z" fill="${C.warm}"/>
    <text x="84" y="42" fill="${C.warm}" font-size="9.5" text-anchor="end" font-family="monospace">sky's push</text>
    <line x1="240" y1="44" x2="272" y2="94" stroke="${C.bone}" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="336" y="116" fill="${C.bone}" font-size="9.5" text-anchor="end" font-family="monospace">strap — light</text>
    <text x="${cx}" y="152" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">compression over millimetres — cannot buckle.</text>
    <text x="${cx}" y="167" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">the loaded film above faces nothing but sky.</text>`, '0 0 360 182');
}

const DRAW = { tube: drawTube, sleeve: drawSleeve, node: drawNode, lap: drawLap, film: drawFilm, seat: drawSeat };

/* True-relative-size strip: every tube on one scale — click a bore to select it. */
function tubeStrip(activeId) {
  const tubes = byCat('tubes');
  const maxOd = Math.max(...tubes.map(t => t.draw.odMm));
  const w = 340, pad = 26, innerW = w - 2 * pad;
  const gaps = 30 * (tubes.length - 1);
  const pxPerMm = Math.min(0.62, (innerW - gaps) / tubes.reduce((s, t) => s + t.draw.odMm, 0));
  const cy = 30 + maxOd * pxPerMm / 2;
  const yLab = cy + maxOd * pxPerMm / 2 + 16;
  let x = pad, out = '';
  for (const t of tubes) {
    const r = Math.max(2.4, t.draw.odMm * pxPerMm / 2);
    const on = t.id === activeId;
    x += r;
    out += `<g data-strip="${t.id}" style="cursor:pointer">
      <circle cx="${x}" cy="${cy.toFixed(1)}" r="${(r + 10).toFixed(1)}" fill="#000" fill-opacity="0" pointer-events="all"/>
      <circle cx="${x}" cy="${cy.toFixed(1)}" r="${r.toFixed(1)}" fill="${on ? C.warm : C.cool}" fill-opacity="${on ? 0.35 : 0.10}"
       stroke="${on ? C.warm : C.faint}" stroke-width="${on ? 1.8 : 1}"/>
      <text x="${x}" y="${yLab.toFixed(1)}" fill="${on ? C.warm : C.faint}" font-size="10" text-anchor="middle" font-family="monospace">${fmtMm(t.draw.odMm)}</text>
    </g>`;
    x += r + 30;
  }
  out += `<text x="${pad}" y="14" fill="${C.faint}" font-size="10" font-family="monospace">every tube, true relative bore — click to select</text>`;
  return svgEl(out, `0 0 ${w} ${(yLab + 10).toFixed(0)}`);
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
    mount.querySelectorAll('[data-strip]').forEach(g =>
      g.addEventListener('click', () => {
        const n = byCat(cat).findIndex(t => t.id === g.dataset.strip);
        if (n >= 0 && n !== idx) { idx = n; render(); }
      }));
  }
  render();
}

/* ------------------------------------------------ level figures ------------------------ */
/* Each level section gets a drawing of ITS idea. These are schematics of the design, not
 * renders — the explorer owns real geometry. Digits inside them come from catalog.js. */

/* Level 2 — one true Kelvin cell, wireframe, orthographic. Vertices are every
 * permutation of (0, ±1, ±2); edges join pairs at distance √2. */
function drawKelvinCell() {
  const V = [];
  for (const [a, b, c] of [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]) {
    for (const i of (a ? [1, -1] : [1]))
      for (const j of (b ? [1, -1] : [1]))
        for (const k of (c ? [1, -1] : [1])) V.push([a * i, b * j, c * k]);
  }
  const E = [];
  for (let i = 0; i < V.length; i++)
    for (let j = i + 1; j < V.length; j++) {
      const d = (V[i][0] - V[j][0]) ** 2 + (V[i][1] - V[j][1]) ** 2 + (V[i][2] - V[j][2]) ** 2;
      if (Math.abs(d - 2) < 1e-9) E.push([i, j]);
    }
  const az = -0.75, el = 0.5, S = 46, cx = 180, cy = 108;
  const ca = Math.cos(az), sa = Math.sin(az), ce = Math.cos(el), se = Math.sin(el);
  const P = V.map(([x, y, z]) => {
    const x1 = ca * x + sa * y, y1 = -sa * x + ca * y;
    return { sx: cx + S * x1, sy: cy - S * (z * ce - y1 * se), d: y1 * ce + z * se };
  });
  const ds = E.map(([i, j]) => (P[i].d + P[j].d) / 2);
  const dmin = Math.min(...ds), dmax = Math.max(...ds);
  let out = '';
  E.map((e, n) => ({ e, t: (ds[n] - dmin) / (dmax - dmin || 1) }))
    .sort((a, b) => a.t - b.t)
    .forEach(({ e: [i, j], t }) => {
      out += `<line x1="${P[i].sx.toFixed(1)}" y1="${P[i].sy.toFixed(1)}" x2="${P[j].sx.toFixed(1)}" y2="${P[j].sy.toFixed(1)}"
               stroke="${C.cool}" stroke-opacity="${(0.22 + 0.68 * t).toFixed(2)}" stroke-width="${(1 + 1.1 * t).toFixed(1)}"/>`;
    });
  out += `<text x="${cx}" y="212" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">the Kelvin cell · span ${(ARTICLE.spanM * 1000).toFixed(0)} mm</text>`;
  return svgEl(out, '0 0 360 224');
}

/* Level 2 — where the cell's mass lives, and the brutal float tick. */
function massBar() {
  const x0 = 30, w = 300, y = 46, h = 30, tot = ARTICLE.totalKg;
  const seg = [
    { v: ARTICLE.tubeKg, name: 'tube', col: C.cool, op: 0.35 },
    { v: ARTICLE.nodesKg, name: 'joints', col: C.warm, op: 0.35 },
    { v: ARTICLE.skinKg, name: 'film', col: C.bone, op: 0.5 },
  ];
  let x = x0, out = '';
  for (const s of seg) {
    const sw = w * s.v / tot;
    out += `<rect x="${x.toFixed(1)}" y="${y}" width="${sw.toFixed(1)}" height="${h}"
             fill="${s.col}" fill-opacity="${s.op}" stroke="${s.col}" stroke-width="1"/>`;
    const lab = s.v >= 0.1 ? `${s.v.toFixed(2)} kg` : `${(s.v * 1000).toFixed(0)} g`;
    const ly = s.name === 'film' ? y + h + 30 : y + h + 16;
    out += `<text x="${Math.min(x + sw / 2, 322).toFixed(1)}" y="${ly}" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">${s.name} ${lab}</text>`;
    x += sw;
  }
  const fx = x0 + w * (ARTICLE.displacedAirG / 1000) / tot;
  out += `<line x1="${fx.toFixed(1)}" y1="${y - 20}" x2="${fx.toFixed(1)}" y2="${y + h + 4}" stroke="${C.warm}" stroke-width="1.6"/>
          <text x="${(fx + 6).toFixed(1)}" y="${y - 8}" fill="${C.warm}" font-size="10" font-family="monospace">what its own air weighs: ${ARTICLE.displacedAirG.toFixed(0)} g</text>
          <text x="${x0}" y="20" fill="${C.faint}" font-size="11" font-family="monospace">one cell, ${tot.toFixed(2)} kg — the line is the float budget</text>`;
  return svgEl(out, '0 0 360 106');
}

/* Level 3 — a band cross-section: octagons sharing walls, atmosphere above, vacuum below. */
function drawBandSection() {
  const s = 33, R = s / (2 * Math.sin(Math.PI / 8)), flat = s * (1 + Math.SQRT2);
  const cy = 118, centres = [96, 96 + flat, 96 + 2 * flat];
  const pt = (cx, k) => {
    const a = (22.5 + 45 * k) * Math.PI / 180;
    return [cx + R * Math.cos(a), cy - R * Math.sin(a)];
  };
  let out = '';
  for (const cx of centres) {
    for (let k = 0; k < 8; k++) {
      const [x1, y1] = pt(cx, k), [x2, y2] = pt(cx, (k + 1) % 8);
      const top = (k === 1 || k === 2 || k === 3), bot = (k === 5 || k === 6 || k === 7);
      const st = top ? `stroke="${C.warm}" stroke-width="1.8"`
        : bot ? `stroke="${C.bone}" stroke-width="1.2" stroke-dasharray="4 3"`
              : `stroke="${C.cool}" stroke-width="1.4"`;
      out += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" ${st}/>`;
    }
  }
  for (const ax of [96, 96 + flat, 96 + 2 * flat])
    out += `<line x1="${ax}" y1="34" x2="${ax}" y2="52" stroke="${C.warm}" stroke-width="1.4"/>
            <path d="M ${ax - 4} 46 L ${ax} 54 L ${ax + 4} 46" fill="none" stroke="${C.warm}" stroke-width="1.4"/>`;
  const sx = 96 + flat / 2;
  out += `<text x="${96 + flat}" y="24" fill="${C.warm}" font-size="11" text-anchor="middle" font-family="monospace">outside — one atmosphere, loaded film</text>
          <line x1="${sx.toFixed(1)}" y1="${(cy - flat / 2).toFixed(1)}" x2="${sx.toFixed(1)}" y2="${(cy + flat / 2).toFixed(1)}" stroke="none"/>
          <text x="${96 + flat}" y="210" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">inside — vacuum · films unloaded, kept for breach</text>
          <text x="${(96 + flat / 2).toFixed(0)}" y="${cy + 4}" fill="${C.cool}" font-size="10" text-anchor="middle" font-family="monospace">shared</text>
          <text x="${(96 + flat / 2).toFixed(0)}" y="${cy + 16}" fill="${C.cool}" font-size="10" text-anchor="middle" font-family="monospace">wall</text>`;
  return svgEl(out, '0 0 360 224');
}

/* Level 4 — the deep sandwich wall, outside at the top. */
function drawWallSection() {
  const L = 44, Rr = 386;
  let out = `<line x1="${L}" y1="26" x2="${Rr}" y2="26" stroke="${C.bone}" stroke-width="1.2"/>
             <text x="${Rr + 4}" y="30" fill="${C.faint}" font-size="10" font-family="monospace"></text>`;
  const chord = (y) => {
    let s = '';
    for (let x = L + 20; x <= Rr - 20; x += 54)
      s += `<circle cx="${x}" cy="${y}" r="9" fill="${C.cool}" fill-opacity="0.15" stroke="${C.cool}" stroke-width="1.6"/>`;
    return s;
  };
  out += chord(56);
  for (let x = L + 20; x + 54 <= Rr - 12; x += 54)
    out += `<line x1="${x}" y1="64" x2="${x + 27}" y2="196" stroke="${C.cool}" stroke-opacity="0.5" stroke-width="1.2"/>
            <line x1="${x + 54}" y1="64" x2="${x + 27}" y2="196" stroke="${C.cool}" stroke-opacity="0.5" stroke-width="1.2"/>`;
  const s8 = 14, R8 = s8 / (2 * Math.sin(Math.PI / 8)), flat8 = s8 * (1 + Math.SQRT2);
  for (let cx = L + 47; cx <= Rr - 40; cx += flat8) {
    let d = '';
    for (let k = 0; k < 8; k++) {
      const a = (22.5 + 45 * k) * Math.PI / 180;
      d += `${k ? 'L' : 'M'} ${(cx + R8 * Math.cos(a)).toFixed(1)} ${(102 - R8 * Math.sin(a)).toFixed(1)} `;
    }
    out += `<path d="${d}Z" fill="${C.warm}" fill-opacity="0.08" stroke="${C.warm}" stroke-width="1.1"/>`;
  }
  out += chord(204);
  out += `<line x1="${L}" y1="232" x2="${Rr}" y2="232" stroke="${C.bone}" stroke-width="1" stroke-dasharray="5 4"/>`;
  out += `
    <text x="${L}" y="16" fill="${C.faint}" font-size="10" font-family="monospace">outside · weather jacket</text>
    <text x="${Rr}" y="46" fill="${C.cool}" font-size="10" text-anchor="end" font-family="monospace">outer chords — the ring hoops ARE the frames</text>
    <text x="${L}" y="126" fill="${C.warm}" font-size="10" font-family="monospace">the cell band — hangs just inside, kills the atmosphere</text>
    <text x="${Rr}" y="188" fill="${C.cool}" font-size="10" text-anchor="end" font-family="monospace">webs · shear</text>
    <text x="${L}" y="222" fill="${C.cool}" font-size="10" font-family="monospace">inner chords</text>
    <text x="${L}" y="248" fill="${C.faint}" font-size="10" font-family="monospace">void skin — a whisper of a wall</text>
    <text x="${(L + Rr) / 2}" y="272" fill="${C.warm}" font-size="11" text-anchor="middle" font-family="monospace">below: the void — pure vacuum, pure lift</text>
    <path d="M ${Rr + 10} 56 L ${Rr + 18} 56 L ${Rr + 18} 204 L ${Rr + 10} 204" fill="none" stroke="${C.faint}" stroke-width="1"/>
    <text x="${Rr + 24}" y="134" fill="${C.faint}" font-size="10" font-family="monospace" transform="rotate(90 ${Rr + 24} 134)">deep ≈ ${GRID.depthM} m</text>`;
  return svgEl(out, '0 0 440 284');
}

/* Level 4 — what holds a cell: bench (self-balanced), band (grid reacts), ring (hoop). */
function drawCellSupport() {
  const oct = (cx, cy, R, rot = 0, style = `fill="${C.cool}" fill-opacity="0.10" stroke="${C.cool}" stroke-width="1.3"`) => {
    let d = '';
    for (let k = 0; k < 8; k++) {
      const a = (22.5 + 45 * k + rot) * Math.PI / 180;
      d += `${k ? 'L' : 'M'} ${(cx + R * Math.cos(a)).toFixed(1)} ${(cy - R * Math.sin(a)).toFixed(1)} `;
    }
    return `<path d="${d}Z" ${style}/>`;
  };
  const arrowTo = (x1, y1, x2, y2, col) => {
    const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
    const bx = x2 - 5 * ux, by = y2 - 5 * uy;
    return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${bx.toFixed(1)}" y2="${by.toFixed(1)}" stroke="${col}" stroke-width="1.5"/>
      <path d="M ${x2.toFixed(1)} ${y2.toFixed(1)} L ${(x2 - 8 * ux - 3.5 * uy).toFixed(1)} ${(y2 - 8 * uy + 3.5 * ux).toFixed(1)} L ${(x2 - 8 * ux + 3.5 * uy).toFixed(1)} ${(y2 - 8 * uy - 3.5 * ux).toFixed(1)} Z" fill="${col}"/>`;
  };
  let out = '';

  /* panel 1 — the bench: sky on every side, net zero */
  const c1x = 110, c1y = 108, R1 = 44;
  out += oct(c1x, c1y, R1);
  for (let k = 0; k < 8; k++) {
    const a = (k * 45) * Math.PI / 180;
    out += arrowTo(c1x + Math.cos(a) * (R1 + 34), c1y - Math.sin(a) * (R1 + 34),
                   c1x + Math.cos(a) * (R1 + 8), c1y - Math.sin(a) * (R1 + 8), C.warm);
  }
  out += `<text x="${c1x}" y="208" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">bench: sky on every side</text>
          <text x="${c1x}" y="222" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">net zero — self-balanced</text>`;

  /* panel 2 — the band: one loaded face; it LEANS on the outer wall via bearing seats */
  const c2x = 330, c2y = 96, R2 = 42;
  out += oct(c2x, c2y, R2);
  for (const dx of [-24, 0, 24])
    out += arrowTo(c2x + dx, c2y - R2 - 40, c2x + dx, c2y - R2 - 10, C.warm);
  for (const sx of [-1, 1]) {
    const jx = c2x + sx * R2 * 0.72, jy = c2y + R2 * 0.72;
    out += `<rect x="${(jx - 6).toFixed(1)}" y="${jy.toFixed(1)}" width="12" height="16" rx="2"
             fill="${C.warm}" fill-opacity="0.30" stroke="${C.warm}" stroke-width="1.4"/>`;
    out += `<circle cx="${jx.toFixed(1)}" cy="${(jy + 26).toFixed(1)}" r="8" fill="${C.cool}" fill-opacity="0.15" stroke="${C.cool}" stroke-width="1.5"/>`;
  }
  out += `<text x="${c2x}" y="208" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">band: one face loaded — it leans</text>
          <text x="${c2x}" y="222" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">the sky presses it onto the skeleton</text>`;

  /* panel 3 — the ring: pushes become hoop squeeze (chords outside, band inside) */
  const ccx = 552, ccy = 610, Rr = 470;
  const arcP = (deg, r) => {
    const a = deg * Math.PI / 180;
    return [ccx + r * Math.cos(a), ccy + r * Math.sin(a)];
  };
  const [ax1, ay1] = arcP(-103, Rr), [ax2, ay2] = arcP(-77, Rr);
  out += `<path d="M ${ax1.toFixed(1)} ${ay1.toFixed(1)} A ${Rr} ${Rr} 0 0 1 ${ax2.toFixed(1)} ${ay2.toFixed(1)}"
           fill="none" stroke="${C.cool}" stroke-width="2.4"/>`;
  for (const deg of [-99.5, -93, -86.5, -80.5]) {
    const [px, py] = arcP(deg, Rr - 26);
    out += oct(px, py, 16, deg + 90, `fill="${C.warm}" fill-opacity="0.08" stroke="${C.warm}" stroke-width="1.1"`);
    const [fx, fy] = arcP(deg, Rr + 44), [tx2, ty2] = arcP(deg, Rr + 8);
    out += arrowTo(fx, fy, tx2, ty2, C.warm);
  }
  const tang = (deg, dir) => {
    const a = deg * Math.PI / 180;
    const [px, py] = arcP(deg, Rr);
    const tx = -Math.sin(a) * dir, ty = Math.cos(a) * dir;
    return arrowTo(px - 26 * tx, py - 26 * ty, px + 8 * tx, py + 8 * ty, C.cool);
  };
  out += tang(-101, 1) + tang(-79, -1);
  out += `<text x="552" y="208" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">ring: pushes become hoop squeeze</text>
          <text x="552" y="222" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">the arch holds itself</text>`;

  return svgEl(out, '0 0 660 234');
}

/* Level 4 — one bay zoomed: the sealed wall leans on the skeleton; webs live behind it. */
function drawWebDetail() {
  const faceY = 138, innerY = 284, n1 = 110, n2 = 330, mid = 220;
  let out = '';
  const s8 = 30, R8 = s8 / (2 * Math.sin(Math.PI / 8));
  const cellY = 78;
  const arrowTo2 = (x1, y1, x2, y2, col) => {
    const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
    return `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${(x2 - 5 * ux).toFixed(1)}" y2="${(y2 - 5 * uy).toFixed(1)}" stroke="${col}" stroke-width="1.5"/>
      <path d="M ${x2.toFixed(1)} ${y2.toFixed(1)} L ${(x2 - 8 * ux - 3.5 * uy).toFixed(1)} ${(y2 - 8 * uy + 3.5 * ux).toFixed(1)} L ${(x2 - 8 * ux + 3.5 * uy).toFixed(1)} ${(y2 - 8 * uy - 3.5 * ux).toFixed(1)} Z" fill="${col}"/>`;
  };
  for (const cx of [125, 220, 315]) {
    let d = '';
    for (let k = 0; k < 8; k++) {
      const a = (22.5 + 45 * k) * Math.PI / 180;
      d += `${k ? 'L' : 'M'} ${(cx + R8 * Math.cos(a)).toFixed(1)} ${(cellY - R8 * Math.sin(a)).toFixed(1)} `;
    }
    out += `<path d="${d}Z" fill="${C.warm}" fill-opacity="0.07" stroke="${C.warm}" stroke-width="1.2"/>`;
    out += arrowTo2(cx, cellY - R8 - 30, cx, cellY - R8 - 6, C.warm);
    for (const sx of [-1, 1]) {
      const jx = cx + sx * R8 * 0.72, jy = cellY + R8 * 0.72;
      out += `<rect x="${(jx - 5).toFixed(1)}" y="${jy.toFixed(1)}" width="10" height="${(faceY - 4 - jy).toFixed(1)}" rx="2"
               fill="${C.warm}" fill-opacity="0.28" stroke="${C.warm}" stroke-width="1.2"/>`;
    }
  }
  out += `<line x1="343" y1="64" x2="392" y2="132" stroke="${C.bone}" stroke-opacity="0.6" stroke-width="1" stroke-dasharray="3 3"/>
          <text x="436" y="98" fill="${C.bone}" font-size="9.5" text-anchor="end" font-family="monospace">strap — light</text>`;
  out += `<line x1="20" y1="${faceY}" x2="420" y2="${faceY}" stroke="${C.cool}" stroke-width="2"/>
          <line x1="20" y1="${innerY}" x2="420" y2="${innerY}" stroke="${C.cool}" stroke-width="1.4"/>`;
  for (const x of [n1, n2])
    out += `<circle cx="${x}" cy="${faceY}" r="11" fill="${C.cool}" fill-opacity="0.15" stroke="${C.cool}" stroke-width="1.8"/>`;
  out += `<circle cx="${mid}" cy="${innerY}" r="11" fill="${C.cool}" fill-opacity="0.15" stroke="${C.cool}" stroke-width="1.8"/>`;
  out += `<line x1="${n1}" y1="${faceY + 10}" x2="${mid}" y2="${innerY - 10}" stroke="${C.cool}" stroke-width="1.6"/>
          <line x1="${n2}" y1="${faceY + 10}" x2="${mid}" y2="${innerY - 10}" stroke="${C.cool}" stroke-width="1.6"/>
          <line x1="${n1}" y1="${faceY + 10}" x2="30" y2="${innerY - 14}" stroke="${C.cool}" stroke-opacity="0.35" stroke-width="1.4"/>
          <line x1="${n2}" y1="${faceY + 10}" x2="410" y2="${innerY - 14}" stroke="${C.cool}" stroke-opacity="0.35" stroke-width="1.4"/>`;
  out += arrowTo2(150, 178, 190, 252, C.bone) + arrowTo2(290, 178, 250, 252, C.bone);
  out += `
    <text x="24" y="16" fill="${C.faint}" font-size="10.5" font-family="monospace">one bay, zoomed — the sealed wall leans on the skeleton</text>
    <text x="24" y="31" fill="${C.warm}" font-size="10" font-family="monospace">seats: short bearings — the sky does the clamping</text>
    <text x="24" y="${faceY + 16}" fill="${C.cool}" font-size="10" font-family="monospace">outer wall · chords</text>
    <text x="60" y="222" fill="${C.bone}" font-size="10" font-family="monospace">webs walk the</text>
    <text x="60" y="235" fill="${C.bone}" font-size="10" font-family="monospace">load down</text>
    <text x="416" y="${innerY - 8}" fill="${C.cool}" font-size="10" text-anchor="end" font-family="monospace">inner wall</text>
    <text x="${mid}" y="${innerY + 24}" fill="${C.faint}" font-size="10.5" text-anchor="middle" font-family="monospace">nothing crosses the sealed wall — every strut lives in the lift</text>`;
  return svgEl(out, '0 0 440 316');
}

/* Level 4 — the ring in section: the sealed wall outermost, pressed onto two truss walls. */
function drawRingSection() {
  const cx = 195, cy = 235;
  let o = '';
  const ring = (r, style) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" ${style}/>`;
  const dots = (r, n, rad, col) => {
    let t = '';
    for (let k = 0; k < n; k++) {
      const a = (k / n) * 2 * Math.PI;
      t += `<circle cx="${(cx + r * Math.cos(a)).toFixed(1)}" cy="${(cy + r * Math.sin(a)).toFixed(1)}" r="${rad}"
             fill="${col}" fill-opacity="0.15" stroke="${col}" stroke-width="1.1"/>`;
    }
    return t;
  };
  o += `<circle cx="${cx}" cy="${cy}" r="80" fill="#0d0d10"/>`;
  for (let k = 0; k < 8; k++) {
    const a = k * Math.PI / 4 + Math.PI / 8;
    const x1 = cx + 192 * Math.cos(a), y1 = cy + 192 * Math.sin(a);
    const x2 = cx + 172 * Math.cos(a), y2 = cy + 172 * Math.sin(a);
    const ux = (x2 - x1) / 20, uy = (y2 - y1) / 20;
    o += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${(x2 - 4 * ux).toFixed(1)}" y2="${(y2 - 4 * uy).toFixed(1)}" stroke="${C.warm}" stroke-width="1.4"/>
          <path d="M ${x2.toFixed(1)} ${y2.toFixed(1)} L ${(x2 - 7 * ux - 3 * uy).toFixed(1)} ${(y2 - 7 * uy + 3 * ux).toFixed(1)} L ${(x2 - 7 * ux + 3 * uy).toFixed(1)} ${(y2 - 7 * uy - 3 * ux).toFixed(1)} Z" fill="${C.warm}"/>`;
  }
  o += ring(164, `stroke="${C.bone}" stroke-width="1"`);
  o += dots(153, 50, 5, C.warm);
  for (let k = 0; k < 50; k++) {
    const a = (k / 50) * 2 * Math.PI;
    o += `<line x1="${(cx + 147 * Math.cos(a)).toFixed(1)}" y1="${(cy + 147 * Math.sin(a)).toFixed(1)}"
                x2="${(cx + 141 * Math.cos(a)).toFixed(1)}" y2="${(cy + 141 * Math.sin(a)).toFixed(1)}"
                stroke="${C.warm}" stroke-width="1.3"/>`;
  }
  o += dots(135, 30, 4.5, C.cool);
  for (let k = 0; k < 30; k++) {
    const a1 = (k / 30) * 2 * Math.PI, a2 = a1 + Math.PI / 30, a3 = a1 + 2 * Math.PI / 30;
    o += `<line x1="${(cx + 129 * Math.cos(a1)).toFixed(1)}" y1="${(cy + 129 * Math.sin(a1)).toFixed(1)}"
                x2="${(cx + 99 * Math.cos(a2)).toFixed(1)}" y2="${(cy + 99 * Math.sin(a2)).toFixed(1)}"
                stroke="${C.cool}" stroke-opacity="0.45" stroke-width="1"/>
          <line x1="${(cx + 99 * Math.cos(a2)).toFixed(1)}" y1="${(cy + 99 * Math.sin(a2)).toFixed(1)}"
                x2="${(cx + 129 * Math.cos(a3)).toFixed(1)}" y2="${(cy + 129 * Math.sin(a3)).toFixed(1)}"
                stroke="${C.cool}" stroke-opacity="0.45" stroke-width="1"/>`;
  }
  o += dots(93, 30, 4.5, C.cool);
  o += ring(86, `stroke="${C.bone}" stroke-width="1" stroke-dasharray="5 4"`);
  o += `<text x="${cx}" y="${cy - 4}" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">the void</text>
        <text x="${cx}" y="${cy + 12}" fill="${C.faint}" font-size="10" text-anchor="middle" font-family="monospace">pure vacuum · pure lift</text>`;
  const lab = (r, ly, col, text) => {
    const a = Math.atan2(ly - cy, 372 - cx);
    const px = cx + r * Math.cos(a), py = cy + r * Math.sin(a);
    return `<line x1="${px.toFixed(1)}" y1="${py.toFixed(1)}" x2="374" y2="${ly}" stroke="${C.faint}" stroke-opacity="0.6" stroke-width="0.8"/>
            <text x="380" y="${ly + 3}" fill="${col}" font-size="9.5" font-family="monospace">${text}</text>`;
  };
  o += lab(164, 62, C.bone, 'weather jacket — hail armour');
  o += lab(153, 120, C.warm, 'THE SEALED WALL — evacuated cells,');
  o += lab(150, 138, C.warm, 'outermost, pressed on by the sky');
  o += lab(144, 186, C.warm, 'bearing seats');
  o += lab(135, 232, C.cool, 'outer wall · chords — the skeleton');
  o += lab(112, 278, C.cool, 'webs — all in vacuum');
  o += lab(93, 324, C.cool, 'inner wall · chords — the skeleton');
  o += lab(86, 370, C.bone, 'void skin — gossamer');
  o += `<text x="12" y="452" fill="${C.faint}" font-size="10" font-family="monospace">wall exaggerated ≈4× — at true scale the annulus is a tenth of the radius.</text>
        <text x="12" y="466" fill="${C.faint}" font-size="10" font-family="monospace">everything inboard of the sealed wall is vacuum: both truss walls live in the lift.</text>`;
  return svgEl(o, '0 0 580 476');
}

/* Level 5 — the closed hull under its atmosphere. */
function drawShipClosure() {
  const cy = 104, r = 52, xl = 118, xr = 302;
  const hull = (rr, dash) => `<path d="M ${xl} ${cy - rr} L ${xr} ${cy - rr} A ${rr} ${rr} 0 0 1 ${xr} ${cy + rr} L ${xl} ${cy + rr} A ${rr} ${rr} 0 0 1 ${xl} ${cy - rr} Z"
      fill="none" stroke="${dash ? C.warm : C.cool}" stroke-width="${dash ? 1.1 : 1.8}" ${dash ? 'stroke-dasharray="5 4"' : ''}/>`;
  let out = hull(r, false) + hull(r - 9, true);
  const arrows = [[210, 20, 0, 1], [210, 188, 0, -1], [40, cy, 1, 0], [380, cy, -1, 0],
                  [92, 34, 0.7, 0.7], [328, 34, -0.7, 0.7], [92, 174, 0.7, -0.7], [328, 174, -0.7, -0.7]];
  for (const [ax, ay, dx, dy] of arrows)
    out += `<line x1="${ax}" y1="${ay}" x2="${ax + 14 * dx}" y2="${ay + 14 * dy}" stroke="${C.warm}" stroke-width="1.5"/>
            <circle cx="${ax + 14 * dx}" cy="${ay + 14 * dy}" r="1.8" fill="${C.warm}"/>`;
  out += `
    <text x="210" y="${cy - 8}" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">void core — vacuum</text>
    <text x="210" y="${cy + 12}" fill="${C.warm}" font-size="10" text-anchor="middle" font-family="monospace">band + grid at the skin</text>
    <text x="210" y="216" fill="${C.faint}" font-size="11" text-anchor="middle" font-family="monospace">${SHIP.diaM} m × ${SHIP.lenM} m · the whole sky pressing in</text>`;
  return svgEl(out, '0 0 420 228');
}

/* Level 5 — the float ledger, both safety factors, always. */
function drawLedger() {
  const x0 = 130, k = 0.85, liftX = x0 + SHIP.liftT * k;
  const bar = (y, label, mass, col) => {
    const w = mass * k, over = Math.max(0, x0 + w - liftX);
    let s = `<text x="${x0 - 8}" y="${y + 14}" fill="${C.faint}" font-size="10" text-anchor="end" font-family="monospace">${label}</text>
             <rect x="${x0}" y="${y}" width="${Math.min(w, liftX - x0).toFixed(1)}" height="20" fill="${col}" fill-opacity="0.25" stroke="${col}" stroke-width="1.2"/>`;
    if (over > 0.5) s += `<rect x="${liftX}" y="${y}" width="${over.toFixed(1)}" height="20" fill="#d98b80" fill-opacity="0.45" stroke="#d98b80" stroke-width="1.2"/>`;
    const res = SHIP.liftT - mass;
    s += `<text x="${(x0 + w + 8).toFixed(1)}" y="${y + 14}" fill="${res >= 0 ? '#46d06e' : '#d98b80'}" font-size="11" font-family="monospace">${res >= 0 ? '+' : '−'}${Math.abs(res).toFixed(1)} t</text>`;
    return s;
  };
  let out = `<line x1="${liftX}" y1="16" x2="${liftX}" y2="120" stroke="#46d06e" stroke-width="1.4" stroke-dasharray="2 3"/>
             <text x="${liftX}" y="12" fill="#46d06e" font-size="10" text-anchor="middle" font-family="monospace">lift ${SHIP.liftT} t</text>`;
  out += bar(28, `structure @ SF 1.2`, SHIP.massT, C.cool);
  out += bar(76, `structure @ SF 1.5`, SHIP.massSF15T, C.cool);
  out += `<text x="210" y="140" fill="${C.faint}" font-size="9.5" text-anchor="middle" font-family="monospace">floats at the declared factor — the chord coupons decide SF 1.5</text>`;
  return svgEl(out, '0 0 420 150');
}

/* Level 6 — equipment callouts on the hull; the payload axis. */
function drawShipEquip() {
  const cy = 110, r = 44, xl = 128, xr = 292;
  let out = `<path d="M ${xl} ${cy - r} L ${xr} ${cy - r} A ${r} ${r} 0 0 1 ${xr} ${cy + r} L ${xl} ${cy + r} A ${r} ${r} 0 0 1 ${xl} ${cy - r} Z"
      fill="none" stroke="${C.bone}" stroke-width="1.6"/>`;
  const rotor = (x, y) => `<circle cx="${x}" cy="${y}" r="5" fill="${C.cool}" fill-opacity="0.3" stroke="${C.cool}" stroke-width="1.3"/>
      <line x1="${x - 13}" y1="${y}" x2="${x + 13}" y2="${y}" stroke="${C.cool}" stroke-width="1.1"/>`;
  out += rotor(160, cy - r - 12) + rotor(260, cy - r - 12) + rotor(160, cy + r + 12) + rotor(260, cy + r + 12);
  out += `<rect x="180" y="${cy + 14}" width="26" height="12" rx="4" fill="${C.cool}" fill-opacity="0.2" stroke="${C.cool}" stroke-width="1.1"/>
          <rect x="214" y="${cy + 14}" width="26" height="12" rx="4" fill="${C.cool}" fill-opacity="0.2" stroke="${C.cool}" stroke-width="1.1"/>`;
  out += `<line x1="210" y1="${cy + r}" x2="210" y2="${cy + r + 42}" stroke="${C.warm}" stroke-width="1.2"/>
          <circle cx="210" cy="${cy + r + 48}" r="6" fill="none" stroke="${C.warm}" stroke-width="1.3"/>`;
  out += `<circle cx="${xr + r - 6}" cy="${cy - 12}" r="2.5" fill="${C.warm}"/>`;
  const call = (x, y, tx, ty, label, anchor = 'start') =>
    `<line x1="${x}" y1="${y}" x2="${tx}" y2="${ty}" stroke="${C.faint}" stroke-width="0.8"/>
     <text x="${tx + (anchor === 'start' ? 4 : -4)}" y="${ty + 3}" fill="${C.faint}" font-size="10" text-anchor="${anchor}" font-family="monospace">${label}</text>`;
  out += call(160, cy - r - 12, 74, 34, 'rotor stations', 'end');
  out += call(193, cy + 20, 84, 196, 'water tanks', 'end');
  out += call(210, cy + r + 48, 300, 208, 'descent winch + bag');
  out += call(xr + r - 6, cy - 12, 352, 44, 'avionics');
  out += call(250, cy - r, 412, 24, 'the livery — paint at last', 'end');
  return svgEl(out, '0 0 420 224');
}

/* ------------------------------------------------ boot --------------------------------- */

bindNumbers();
const q = new URLSearchParams(location.search);
makePane($('#pane-a'), CATS.some(c => c.id === q.get('cat')) ? q.get('cat') : 'tubes', +(q.get('i') || 0) || 0);

const put = (sel, svg) => { const el = $(sel); if (el) el.innerHTML = svg; };
put('#fig-cell', drawKelvinCell());
put('#fig-cellmass', massBar());
put('#fig-band', drawBandSection());
put('#fig-wall', drawWallSection());
put('#fig-support', drawCellSupport());
put('#fig-webs', drawWebDetail());
put('#fig-ring', drawRingSection());
put('#fig-closure', drawShipClosure());
put('#fig-ledger', drawLedger());
put('#fig-equip', drawShipEquip());
