/* The parts catalog — level 1 of the build.
 *
 * One entry per part the ship is made of, grouped tubes / connectors / skins. Everything
 * the committed cell model already knows is READ from it (stockBuild, MATERIALS, the saw
 * table); nothing the model computes is retyped here. Ship-scale entries carry numbers
 * from the verified scoping analysis (~/data/airships-reviews/analysis/
 * 26-08-12-ship-scale-analysis-v2.md) and say so in their `prov` line — they swap to
 * ship.js imports when that module lands under the gates (see docs/HANDOFF.md, the
 * seven-levels section). Status vocabulary:
 *
 *   proven      measured on, or billed against, the built article A
 *   decided     an operator decision on record — geometry known, some numbers [TO VERIFY]
 *   scoping     ship-scale analysis line — real physics, pre-coupon, pre-catalogue
 *   superseded  carried the article but ruled out for flight; kept because it happened
 *
 * The design of record for joints (operator, 2026-08-12): titanium, CLAMPED — split
 * clamshell sleeves that close radially around placed members and bond over the full
 * lap. The connectors tab leads with that design; the printed polymer node sits last,
 * as history.
 */
import { MATERIALS, CUT_SCHEDULE_MEASURED, NODE_MASS_MEASURED_KG,
         stockBuild, barrierKgPerM2 } from './model.js?v=e4cd07ce';

const sb = stockBuild();

/* Linear masses from section geometry x the laminate density the model bills with. */
const linKgPerM = (odMm, wallMm, rho) => {
  const ro = odMm / 2000, ri = ro - wallMm / 1000;
  return Math.PI * (ro * ro - ri * ri) * rho;
};
const T700 = MATERIALS.T700_LAM;
const TI64 = MATERIALS.TI64;

/* Saw-table roll-ups, straight off the measured schedule. */
const sawnRows = CUT_SCHEDULE_MEASURED;
const fam = (name) => sawnRows.filter(r => r[0] === name);
const famM = (name) => fam(name).reduce((s, r) => s + r[1] * r[2] / 1000, 0);
const famCuts = (name) => fam(name).reduce((s, r) => s + r[2], 0);
const mainCuts = famCuts('octet') + famCuts('spoke') + famCuts('tie');
const mainM = famM('octet') + famM('spoke') + famM('tie');
const cutMin = Math.min(...sawnRows.map(r => r[1]));
const cutMax = Math.max(...sawnRows.map(r => r[1]));

/* The ship-0 summary the shell page quotes. SCOPING: analysis-v2 §7 plan-of-record row,
 * declared SF 1.2 with the SF 1.5 column beside it, as the house display rule requires.
 * These digits move only with that document until ship.js lands. */
export const SHIP = {
  name: 'ship 0',
  diaM: 52, lenM: 104, fineness: 2,
  volumeM3: 184055, hullM2: 16990,
  liftT: 225.5, massT: 221.7, residualT: 3.8, ratio: 1.017,
  massSF15T: 257.7, ratioSF15: 0.875, ratioSF15Sigma1450: 1.043,
  tempPctPerK: 0.34, windowK: 5,
  prov: 'ship-scale analysis v2 §7 — scoping, pending the gated ship.js port',
};

/* Band and grid scoping lines the level sections visualise. Same provenance rule. */
export const BAND = {
  arealKgM2Lo: 5.0, arealKgM2Hi: 10.7,     // by tube/joint basis (E' retuned … committed article)
  cells: 20000,                             // order-of: analysis v2 §7 seal-and-hold count (~2×10⁴)
  perCellPushT: 7.2,                        // ≈0.7 m² band footprint per cell × 1 atm, tonnes-force
  prov: 'ship-scale analysis v2 §3/§7 — one cell-span band absorbs the full atmosphere',
};
export const GRID = {
  depthM: 3, bayM: 2,
  hoopKPaM: 2634,                           // P·R at the ship-0 barrel radius (R = 26 m)
  bandCapKPaM: 67,                          // the band's own in-plane ceiling (upper bound)
  prov: 'ship-scale analysis v2 §3/§4 — the shell carries the global load; the band hangs on it',
};

/* The committed article, read live from the model so this page can never disagree
 * with the explorer next door. */
export const ARTICLE = {
  spanM: sb.spanM,
  totalKg: sb.totalKg,
  kgPerM3: sb.kgPerM3,
  sawnM: sb.sawnM,
  pipeCount: sb.pipeCount,
  printedNodes: sb.printedNodes,
  nodesKg: sb.nodesKg,
  skinKg: sb.skinKg,
  tubeKg: sb.totalKg - sb.nodesKg - sb.skinKg,
  displacedAirG: sb.displacedAirKg * 1000,
};

export const CATS = [
  { id: 'tubes', name: 'Tubes' },
  { id: 'connectors', name: 'Connectors' },
  { id: 'skins', name: 'Skins' },
];

export const CATALOG = [
  /* ------------------------------------------------ tubes ------------------------------ */
  {
    id: 'tube-main', cat: 'tubes',
    name: 'Main cell tube',
    status: 'proven',
    role: 'The octet frame, the spokes, and the ties of one cell — the member family that '
        + 'carries the crush of the sky on the smallest article.',
    story: 'Every one of these in the built article is on a measured saw table; the model '
        + 'bills the schedule, not an idealisation.',
    draw: { kind: 'tube', odMm: sb.odM * 1000, wallMm: (sb.odM - sb.idM) * 500, cutMm: cutMax },
    specs: [
      { k: 'Bore', v: `${(sb.odM * 1000).toFixed(0)} × ${(sb.idM * 1000).toFixed(0)}`, u: 'mm od × id' },
      { k: 'Construction', v: 'roll-wrapped T700 carbon', u: '' },
      { k: 'Linear mass', v: (linKgPerM(sb.odM * 1000, (sb.odM - sb.idM) * 500, T700.rho) * 1000).toFixed(1), u: 'g/m' },
      { k: 'Cuts in one cell', v: `${mainCuts}`, u: `pieces, ${cutMin.toFixed(0)}–${cutMax.toFixed(0)} mm` },
      { k: 'Sawn per cell', v: mainM.toFixed(1), u: 'm' },
    ],
    prov: 'cell/model.js stockBuild() + CUT_SCHEDULE_MEASURED (article A, as sawn)',
    flags: [],
  },
  {
    id: 'tube-rim', cat: 'tubes',
    name: 'Rim tube',
    status: 'proven',
    role: 'The cell’s outer edges, where the skin’s dihedral pull lands — a heavier '
        + 'bore than the interior because the film asks twice what a spoke does.',
    story: 'Two tube SKUs per cell, not one: the rim earned its own section the day the '
        + 'film loads were solved rather than smeared.',
    draw: { kind: 'tube', odMm: sb.rimOdM * 1000, wallMm: 1, cutMm: fam('rim')[0][1] },
    specs: [
      { k: 'Bore', v: `${(sb.rimOdM * 1000).toFixed(0)} × ${(sb.rimOdM * 1000 - 2).toFixed(0)}`, u: 'mm od × id' },
      { k: 'Construction', v: 'roll-wrapped T700 carbon', u: '' },
      { k: 'Linear mass', v: (linKgPerM(sb.rimOdM * 1000, 1, T700.rho) * 1000).toFixed(1), u: 'g/m' },
      { k: 'Cuts in one cell', v: `${famCuts('rim')}`, u: 'pieces' },
      { k: 'Sawn per cell', v: famM('rim').toFixed(1), u: 'm' },
    ],
    prov: 'cell/model.js stockBuild() + CUT_SCHEDULE_MEASURED (article A, as sawn)',
    flags: [],
  },
  {
    id: 'tube-web', cat: 'tubes',
    name: 'Grid web tube',
    status: 'scoping',
    role: 'The diagonals of the ship’s deep sandwich shell — they hold the two chord '
        + 'faces apart and carry the shear between them.',
    story: 'The longest single parts of the whole ship, and still shorter than a canoe.',
    draw: { kind: 'tube', odMm: 60, wallMm: 2, cutMm: 3600 },
    specs: [
      { k: 'Bore', v: '60 × 56', u: 'mm od × id (class)' },
      { k: 'Piece length', v: '≈3.6', u: 'm' },
      { k: 'Linear mass', v: (linKgPerM(60, 2, T700.rho)).toFixed(2), u: 'kg/m' },
      { k: 'Ship set', v: '≈4,000 pieces · ≈15 km', u: '' },
    ],
    prov: 'ship-scale analysis v2 §4 (webs 0.5 kg/m² scoping line)',
    flags: ['member-level design absent — scoping line only'],
  },
  {
    id: 'tube-chord', cat: 'tubes',
    name: 'Chord pipe',
    status: 'scoping',
    role: 'The ship’s ring hoops and longerons — the face members of the sandwich '
        + 'shell that carry the whole squeeze of the atmosphere as compression.',
    story: 'Fatter-not-thinner is the verified law: this section sits on the co-critical '
        + 'locus where Euler and wall buckling bind together.',
    draw: { kind: 'tube', odMm: 137, wallMm: 3.5, cutMm: 2000 },
    specs: [
      { k: 'Bore', v: '137 × 130', u: 'mm od × wall 3.5' },
      { k: 'Piece length', v: '≈2', u: 'm (one ring bay)' },
      { k: 'Linear mass', v: linKgPerM(137, 3.5, T700.rho).toFixed(2), u: 'kg/m' },
      { k: 'Governing stress', v: '742', u: 'MPa (co-critical, verified-class)' },
      { k: 'Coupon target', v: '1,050–1,450', u: 'MPa — decides the hull size' },
    ],
    prov: 'ship-scale analysis v2 §2/§4 — custom roll-wrap, beyond stock walls',
    flags: ['axial-compressive allowable [TO VERIFY] — the single biggest ship lever'],
  },
  {
    id: 'tube-chord-heavy', cat: 'tubes',
    name: 'Heavy chord pipe',
    status: 'scoping',
    role: 'The yield-cap end of the chord family: fewer, fatter members for the load '
        + 'concentrations — dome junctions, ring frames that double as bulkhead rims.',
    story: 'Nineteen centimetres of carbon pipe. The biggest single section anywhere in '
        + 'the design, and it still ships on a pallet.',
    draw: { kind: 'tube', odMm: 190, wallMm: 10, cutMm: 2000 },
    specs: [
      { k: 'Bore', v: '190 × 170', u: 'mm od × wall 10' },
      { k: 'Piece length', v: '≈2', u: 'm (one ring bay)' },
      { k: 'Linear mass', v: linKgPerM(190, 10, T700.rho).toFixed(2), u: 'kg/m' },
    ],
    prov: 'ship-scale analysis v2 §4 (chord class upper bound)',
    flags: ['sourcing [TO VERIFY] — custom-wrap territory'],
  },

  /* ---------------------------------------------- connectors --------------------------- */
  /* Design of record first; history last. */
  {
    id: 'conn-ti-sleeve', cat: 'connectors',
    name: 'Ti clamp sleeve',
    status: 'decided',
    role: 'The flight joint: a sintered titanium clamshell, split along its length, that '
        + 'clamps radially around tube and stub after placement and bonds over the full '
        + 'lap — the last member of a loop never has to slide where it cannot.',
    story: 'The main load path never crosses the seam — each half carries its half-'
        + 'circumference of glue. The seam only keeps the clamp closed: dovetail, pin, '
        + 'or a wrap of tow.',
    draw: { kind: 'sleeve', odMm: 12, wallMm: 1, lapMm: 10 },
    specs: [
      { k: 'Material', v: 'Ti-6Al-4V, sintered', u: `${TI64.rho} kg/m³` },
      { k: 'Wall', v: '1.0', u: 'mm' },
      { k: 'Closure', v: 'clamped', u: 'split clamshell, radial' },
      { k: 'Bonded lap', v: '8–11', u: 'mm per end' },
      { k: 'Set per cell', v: '0.42–0.60', u: 'kg' },
    ],
    prov: 'operator decision 08-12 · metal-joint report §5 (set-mass lower bounds)',
    flags: ['set mass [TO VERIFY] — central body + adhesive unpriced', 'seam capture detail undesigned'],
  },
  {
    id: 'conn-ti-gridnode', cat: 'connectors',
    name: 'Ti grid node',
    status: 'scoping',
    role: 'Where chord pipes meet: a cluster of the same clamped titanium sleeves, '
        + 'scaled to swallow meganewton loads at the ring-longeron-diagonal crossings.',
    story: 'Chunky enough that sintering stops being the process — at thousands of '
        + 'these, investment casting takes over and the printed part becomes the pattern.',
    draw: { kind: 'node', arms: 6, hubMm: 160 },
    specs: [
      { k: 'Material', v: 'Ti-6Al-4V, cast or sintered', u: '' },
      { k: 'Closure', v: 'clamped', u: 'split sleeves at every arm' },
      { k: 'Ship set', v: '≈7,000', u: 'nodes' },
      { k: 'Unit mass', v: '≈2.5', u: 'kg' },
      { k: 'Loads', v: '0.5–6', u: 'MN member class' },
    ],
    prov: 'ship-scale analysis v2 §6 (η_mass joint fraction) · production machinery note',
    flags: ['scoping — SHIP-3 order owns this'],
  },
  {
    id: 'conn-bond', cat: 'connectors',
    name: 'The bonded lap',
    status: 'decided',
    role: 'The glue line inside every clamp, promoted to a part: it carries the member '
        + 'load in shear and it is also the gas seal that lets a cell hold vacuum for months.',
    story: 'Cured under vacuum bagging — the atmosphere is the clamp while the clamp '
        + 'cures. In service every joint cavity reads on the cell’s own gauge, so a '
        + 'failing bond announces itself.',
    draw: { kind: 'lap', odMm: 10, lapMm: 10 },
    specs: [
      { k: 'Working shear', v: '20', u: 'MPa, aged allowable' },
      { k: 'Lap length', v: '8–11', u: 'mm' },
      { k: 'One lap carries', v: '≈6', u: 'kN on the main bore' },
      { k: 'Cure clamp', v: '1 atm', u: 'vacuum bag' },
    ],
    prov: 'metal-joint report (lap sizing) · joint-load report (mechanism)',
    flags: ['τ = 20 MPa unsourced — qualification campaign line'],
  },
  {
    id: 'conn-tie', cat: 'connectors',
    name: 'Seat & retention strap',
    status: 'decided',
    role: 'The interface, as ruled: the cell sits face-down on the outer wall, its push '
        + 'passing through a flush pad embedded in the face — compression over '
        + 'millimetres, which cannot buckle — while a light strap holds position '
        + 'whenever the sky lets go.',
    story: 'The rope survives the ruling as the strap: creep stops mattering when the '
        + 'load is occasional, so Dyneema is back on the table. And the loaded film '
        + 'above faces nothing but sky — every attachment lands on the unloaded side.',
    draw: { kind: 'seat' },
    specs: [
      { k: 'Bearing seat', v: 'embedded flush in the wall', u: 'the cell sits on its face' },
      { k: 'Film seal', v: 'boss = a taller land post', u: 'on the UNLOADED inner film' },
      { k: 'Strap', v: 'UHMWPE or Zylon braid', u: 'retention only — light' },
      { k: 'Per-seat load', v: 'tens of kN', u: 'set by seats-per-cell' },
      { k: 'Ship set', v: 'order 10⁵', u: 'seats' },
    ],
    prov: 'band-outside ruling 08-12 (operator) — supersedes the hang/tie variant',
    flags: ['seat pad + strap detail [TO VERIFY] — SHIP-2/3; seats-per-cell governs joint concentration'],
  },
  {
    id: 'conn-printed-node', cat: 'connectors',
    name: 'Printed polymer node',
    status: 'superseded',
    role: 'The many-arm printed hub that holds the built article together today — '
        + 'measured, weighed, and photographed from every side.',
    story: 'It carried the pump-down, and it is ruled out for flight: the polymer fails '
        + 'its own strength screen and drinks water into a months-hold vacuum. Titanium '
        + 'clamps replace it.',
    draw: { kind: 'node', arms: 7, hubMm: 46 },
    specs: [
      { k: 'Set per cell', v: `${sb.printedNodes}`, u: 'joints' },
      { k: 'Set mass', v: NODE_MASS_MEASURED_KG.toFixed(3), u: 'kg, measured' },
      { k: 'Share of tube mass', v: '≈30', u: '% — target is 15' },
      { k: 'Material', v: 'PAHT-CF, printed', u: '' },
    ],
    prov: 'cell/model.js NODE_MASS_MEASURED_KG (weighed set) · metal-joint report (the ruling)',
    flags: ['dead for flight — strength screen + hygroscopic reservoir'],
  },

  /* ------------------------------------------------ skins ------------------------------ */
  {
    id: 'skin-cell-film', cat: 'skins',
    name: 'Cell film',
    status: 'decided',
    role: 'The membrane that turns a frame into a vessel: Zylon-class high-modulus film, '
        + 'pre-formed into its solved dome shape so the sky loads it as a drum, not as a '
        + 'wrinkle.',
    story: 'The gore study measured flat cutting to death — even twelve gores per panel '
        + 'miss the elastic budget. The net keeps its proven outline and is formed.',
    draw: { kind: 'film', layers: [{ name: 'Zylon-class film', gsm: barrierKgPerM2(sb.spanM) * 1000 }] },
    specs: [
      { k: 'Per cell', v: (sb.skinKg * 1000).toFixed(0), u: 'g' },
      { k: 'Areal mass', v: (barrierKgPerM2(sb.spanM) * 1000).toFixed(1), u: 'g/m² (law, at article span)' },
      { k: 'Forming', v: '2 dies · 14 pressings', u: 'per cell class' },
    ],
    prov: 'cell/model.js barrierKgPerM2 + stockBuild().skinKg · gen_skin gore study',
    flags: ['formed-dome strain is a stated requirement, not a solved process'],
  },
  {
    id: 'skin-pvd', cat: 'skins',
    name: 'Barrier metallisation',
    status: 'decided',
    role: 'The nanometres of metal that make polymer film into a vacuum wall: '
        + 'permeation drops orders of magnitude for grams per square metre.',
    story: 'House doctrine from the seal arc: PVD plus impregnation is the barrier; '
        + 'tape is not a seal.',
    draw: { kind: 'film', layers: [{ name: 'PVD metal', gsm: 3 }, { name: 'carrier film', gsm: 12 }] },
    specs: [
      { k: 'Areal mass', v: '2–5', u: 'g/m²' },
      { k: 'Applied by', v: 'roll-to-roll PVD', u: 'bought as coated web' },
    ],
    prov: 'barrier doctrine (research/notes seal arc) · viz handoff register',
    flags: [],
  },
  {
    id: 'skin-void', cat: 'skins',
    name: 'Void terminal skin',
    status: 'scoping',
    role: 'The innermost surface of the ship: everything inboard of the band already '
        + 'sits near vacuum, so the core needs only a whisper of a wall.',
    story: 'Ten grams per square metre bounding a hundred and eighty thousand cubic '
        + 'metres of nothing — the cheapest wall in the whole machine.',
    draw: { kind: 'film', layers: [{ name: 'terminal skin', gsm: 10 }] },
    specs: [
      { k: 'Areal mass', v: '≈10', u: 'g/m²' },
      { k: 'Differential', v: '≤1', u: 'kPa' },
    ],
    prov: 'ship-scale analysis v2 §4 (band hangs, void skin line)',
    flags: ['scoping line'],
  },
  {
    id: 'skin-weather', cat: 'skins',
    name: 'Weather jacket',
    status: 'scoping',
    role: 'The outermost skin: sun, rain, hail, and the livery. Not a pressure part — '
        + 'the atmosphere is carried three layers further in.',
    story: 'Where the paint goes, eventually. Level six owns the look.',
    draw: { kind: 'film', layers: [{ name: 'jacket + finish', gsm: 50 }] },
    specs: [
      { k: 'Areal class', v: '≈50', u: 'g/m² (with skins/misc line)' },
    ],
    prov: 'ship-scale analysis v2 §7 (skins/weather 0.05 kg/m² scoping line)',
    flags: ['scoping line'],
  },
];

export const byCat = (catId) => CATALOG.filter(e => e.cat === catId);
