/* The vacuum cell, as a live model.
 *
 * This is the same physics as research/analysis/vacuum-cell.py, in the browser so the page
 * can be dialled rather than read. The two are held together by tests/cases/cell-parity —
 * a second copy of a calculation is the failure this project keeps finding, so this one is
 * checked against the Python's own output rather than trusted.
 *
 * The argument, in one paragraph. A monolithic vacuum balloon fails by global shell
 * buckling, and that is an impossibility result no material escapes. Put the vacuum in many
 * small sealed cells and there is no global shell: an interior wall has vacuum on both sides
 * and carries no pressure differential at all, so the array is a solid body of cellular
 * material in hydrostatic compression. What governs then is the crushing strength of that
 * cellular solid at a relative density low enough to float — and at those densities the
 * struts are slender enough that BUCKLING governs, not yield. With solid struts nothing
 * floats. With hollow struts the exponent improves from phi^2 to phi^1.5, and aerospace
 * carbon floats with margin. The struts must be tubes.
 */

export const P_ATM = 101325;
export const C_PHI = 6 * Math.SQRT2 * Math.PI;   // octet truss: phi = C_PHI (r/l)^2
/* EXACT under hydrostatic load, and topology-independent: every strut in any
 * stretch-dominated truss takes the same affine strain, so solid stress is 3p/phi. */
export const ALIGN = 1 / 3;
export const K_LOCAL = 0.3;                       // local buckling of a thin tube wall
export const K_SHELL = 0.2;                       // imperfection knockdown, monolithic shell
/* Local buckling of an ORTHOTROPIC tube depends on sqrt(Ex*Etheta), not Ex — so the governing
 * modulus is Ex^(3/4)*Etheta^(1/4), and the best [0/90] split (3/4 axial) costs this factor. */
export const ORTHO_PENALTY = Math.pow(0.75, 0.75) * Math.pow(0.25, 0.25);   // 0.5699
export const CELL_AREA_COEFF = 3.0;               // internal area per m3, times cell size
export const NODE_MASS_FRAC = 0.15;               // nodes carry no load but weigh
/* The printed joints, WEIGHED rather than budgeted: tools/gen_nodes.py integrates every
 * node from its own signed distance field and writes the total to the geometry manifest.
 * The browser cannot read that file, so the number is carried here and the parity gate
 * holds it to the manifest the Python reads — if the joints are regenerated and this is
 * not updated, the build fails. NODE_MASS_FRAC survives only for the in-array kg/m3 rows,
 * where it is still an assertion. */
export const NODE_MASS_MEASURED_KG = 0.465;
/* The printed film pad on each hexagon hub. Local protection for the membrane, not a load
 * path — see filmEdgeLoads, which prices what a pad this size can actually collect. */
export const PAD_R_M = 0.035;
export const LATTICE_SF = 1.5;                    // every strut is critical at once

/* ISA troposphere density: rho = rho_SL * (T/T0)^(g/(L*R) - 1).
 * Writing the pressure form and the density form at once — reduced exponent AND dividing by
 * R*T — reads 6% high. It did, until the parity check disagreed with the live model. */
export function rhoAir(altM) {
  const t = 288.15 - 0.0065 * altM;
  return (101325 / (287.05 * 288.15)) * Math.pow(t / 288.15, 9.80665 / (287.05 * 0.0065) - 1);
}

/* Materials. sigma is the strength that governs a PRESSURE VESSEL, which is the weakest
 * direction — for a filament-printed part that is the interlayer (Z), not the in-plane (X-Y)
 * number a datasheet leads with. */
export const MATERIALS = {
  M60J_LAM: { name: 'M60J UD laminate, Vf 0.6', E: 354e9, sigma: 2.29e9, rho: 1658, orthotropic: true, printable: false },
  T700_LAM: { name: 'T700 UD laminate, Vf 0.6', E: 135e9, sigma: 2.50e9, rho: 1600, orthotropic: true, printable: false },
  CFF:      { name: 'Continuous carbon fibre, printed (Markforged-class)', E: 60e9, sigma: 800e6, rho: 1400, orthotropic: true, printable: true },
  PAHT_XY:  { name: 'Bambu PAHT-CF, in-plane (X-Y)', E: 3.86e9, sigma: 92e6, rho: 1060, orthotropic: true, printable: true },
  PAHT_Z:   { name: 'Bambu PAHT-CF, interlayer (Z)', E: 2.18e9, sigma: 47e6, rho: 1060, orthotropic: true, printable: true },
  TI64:     { name: 'Ti-6Al-4V, laser powder-bed sintered', E: 114e9, sigma: 1.10e9, rho: 4430, orthotropic: false, printable: true },
  AEROGEL:  { name: 'Silica aerogel, monolithic', E: 10e6, sigma: 0.5e6, rho: 120, orthotropic: false, printable: true },
};

export const eEff = m => m.E * (m.orthotropic ? ORTHO_PENALTY : 1);
/* NOT specific strength — every row is buckling-governed. This is the index. */
export const materialIndex = m => Math.pow(eEff(m), 2 / 3) / m.rho;

export function monolithic(m, p = P_ATM) {
  const nu = 0.3;
  const tOverR = Math.sqrt(p * Math.sqrt(3 * (1 - nu * nu)) / (2 * K_SHELL * m.E));
  return { architecture: 'monolithic shell', rho: 3 * m.rho * tOverR,
           governs: 'shell buckling', tOverR };
}

export function solidStrut(m, p = P_ATM) {
  const k = ALIGN * Math.PI * Math.PI / (4 * C_PHI), pd = p * LATTICE_SF;
  const phiB = Math.sqrt(pd / (k * m.E));
  const phiY = pd / (ALIGN * m.sigma);
  const phi = Math.max(phiB, phiY);
  return { architecture: 'solid-strut lattice', phi, rho: phi * m.rho,
           governs: phiB > phiY ? 'strut buckling' : 'material yield', phiB, phiY };
}

export function tubeStrut(m, p = P_ATM) {
  const a = 2 * K_LOCAL / (Math.PI * Math.PI);
  const c = 2 * C_PHI * a;
  const k = ALIGN * K_LOCAL / Math.sqrt(c);
  const pd = p * LATTICE_SF;
  const phiB = Math.pow(pd / (k * eEff(m)), 2 / 3);
  const phiY = pd / (ALIGN * m.sigma);
  const phi = Math.max(phiB, phiY);
  const psi = Math.sqrt(phi / c);          // tube wall / tube radius
  const lam = Math.sqrt(a * psi);          // tube radius / strut length
  return { architecture: 'tubular-strut lattice', phi, rho: phi * m.rho,
           governs: phiB > phiY ? 'strut buckling' : 'material yield',
           psi, lam, wallPerStrutLength: psi * lam, tubeROverT: 1 / psi, phiB, phiY };
}

export const ARCHS = { monolithic, solidStrut, tubeStrut };

/* The sealing film only has to SEAL — the lattice under it carries the load. It bulges into
 * one opening and holds the atmosphere as membrane tension, sigma = pR/2t. */
export function barrierKgPerM2(spanM, { sigmaF = 5.8e9, rhoF = 1560, sf = 4, eff = 0.5,
                                        bulge = 0.25 } = {}) {
  const a = spanM / 2, h = bulge * a;
  const rBulge = (a * a + h * h) / (2 * h);
  return rhoF * (P_ATM * rBulge / (2 * (sigmaF / sf * eff)));
}

/* Everything the page needs for one (material, architecture, altitude, strut length). */
export function evaluate(matKey, archKey, altM, strutLenM) {
  const m = MATERIALS[matKey];
  const wall = rhoAir(altM);
  const r = ARCHS[archKey](m);
  const out = {
    material: m, wall, rho: r.rho, phi: r.phi ?? null, governs: r.governs,
    floats: r.rho < wall,
    marginX: wall / r.rho,
    solidFractionPpm: r.phi ? r.phi * 1e6 : null,
  };
  if (archKey === 'tubeStrut') {
    out.tubeRadiusM = r.lam * strutLenM;
    out.tubeWallM = r.wallPerStrutLength * strutLenM;
    out.barrier = barrierKgPerM2(strutLenM);
    out.minStrutForWallM = (t) => t / r.wallPerStrutLength;
  }
  return out;
}

/* What one flooded cell costs its neighbours. In normal operation an interior wall carries
 * nothing; flood one cell and its shared walls have an atmosphere pushing into the vacuum next
 * door. It is a contingency and it is local, so bound it by a local load factor — and because
 * strength goes as phi^1.5, a factor L costs L^(2/3) in relative density. */
export function breach(matKey, altM) {
  const t = tubeStrut(MATERIALS[matKey]), wall = rhoAir(altM);
  return [[1, 'normal operation'], [1.5, 'spherical-cavity concentration (Lame)'],
          [2, 'a full atmosphere added locally'], [3, 'two adjacent cells lost']]
    .map(([L, note]) => {
      const rho = t.rho * Math.pow(L, 2 / 3);
      return { L, note, rho, marginX: wall / rho, floats: rho < wall };
    });
}

/* Would an aerogel core stabilise the tube wall? Face wrinkling on an elastic core is
 * 0.5*(Ef*Ec*Gc)^(1/3), and aerogel modulus falls as roughly the cube of density — so a core
 * stiff enough to matter is many times the mass of the wall, and one light enough to carry is
 * far too soft. There is no window. */
export function aerogelCore(matKey = 'M60J') {
  const mm = MATERIALS[matKey], t = tubeStrut(mm);
  const bare = 0.3 * mm.E * t.psi;
  return {
    bare,
    rows: [1, 3, 10, 30, 60, 120, 300].map(rc => {
      const Ec = 10e6 * Math.pow(rc / 120, 3), Gc = Ec / 2.6;
      const w = 0.5 * Math.cbrt(mm.E * Ec * Gc);
      return { rc, wrinkle: w, massRatio: rc / (2 * t.psi * mm.rho), beats: w > bare };
    }),
  };
}


/* THE TERM THE MODEL COMPUTED AND DID NOT COUNT, until a review caught it. Individually
 * sealed cells make the film the array's INTERNAL surface, ~3/l m2 per m3 — and its areal
 * mass grows with span exactly as fast as area-per-volume falls, so the product is the same
 * at every cell size. You cannot choose a cell size that makes it go away. */
export function barrierKgPerM3(spanM) {
  return barrierKgPerM2(spanM) * CELL_AREA_COEFF / spanM;
}

/* Lattice + nodes + interior film, which is what has to clear the wall. */
export function totalShell(m, cellSpanM, p = P_ATM, film = true) {
  const t = tubeStrut(m, p);
  const bar = film ? barrierKgPerM3(cellSpanM) : 0;
  return { lattice: t.rho, nodes: t.rho * NODE_MASS_FRAC, film: bar,
           total: t.rho * (1 + NODE_MASS_FRAC) + bar, detail: t };
}

/* ---- Everything below mirrors research/analysis/vacuum-cell.py, held identical by
 * tools/check_cell_parity.py. Same formulas, same constants, same order of operations. ---- */

/* The reference hull the film arithmetic uses: the right-sized P-100 from mass-budget. */
export const HULL_VOLUME_M3 = 220000;
export const HULL_ENVELOPE_M2 = 22592;

/* The outer envelope's film, priced for the job it actually has: holding a full atmosphere
 * (or datm of one, behind a graded band) over unsupported cell spans. An earlier version
 * charged an unsourced 17 g/m2 here — twelve times too light for the load. */
export function envelopeFilmKgPerM3(spanM = 2.0, datm = 1.0) {
  return barrierKgPerM2(spanM) * datm * HULL_ENVELOPE_M2 / HULL_VOLUME_M3;
}

/* Hierarchy: each level of structure-inside-structure improves the strength-density
 * EXPONENT — (n+2)/(n+1), tending to the linear scaling Jenett assumes. Lakes, Nature 361
 * (1993). It converges fast, level 2 is the one that matters — and the ladder ends where
 * the material's strength begins: the solid still carries 3p/phi, so phi can never fall
 * below the yield floor. Levels 3 and 4 hit it for every material here. */
export function ladder(m, levels = 5, film = null, nodes = NODE_MASS_FRAC) {
  const ee = eEff(m);
  const a = 2 * K_LOCAL / (Math.PI * Math.PI);
  const c = 2 * C_PHI * a;
  const k = ALIGN * K_LOCAL / Math.sqrt(c);
  const pd = P_ATM * LATTICE_SF;
  const x = pd / (k * ee);
  const phiYield = pd / (ALIGN * m.sigma);
  if (film === null) film = envelopeFilmKgPerM3();
  const names = ['solid rod', 'hollow tube', 'tube of tubes', 'third order', 'fourth order'];
  const out = [];
  for (let n = 0; n < levels; n++) {
    const alpha = (n + 2) / (n + 1);
    const phiB = Math.pow(x, 1 / alpha);
    const phi = Math.max(phiB, phiYield);
    const lat = phi * m.rho;
    out.push({ levels: n, exponent: alpha, phi, lattice: lat,
               total: lat * (1 + nodes) + film,
               yieldCapped: phiYield > phiB,
               solidStressOverStrength: 3 * pd / phi / m.sigma,
               name: names[n] || `order ${n}` });
  }
  return out;
}

/* How much of the array's wall area is interior — vacuum both sides, carrying nothing. */
export function sharedWall(cellSpanM) {
  const interior = CELL_AREA_COEFF / cellSpanM * HULL_VOLUME_M3;
  return { interiorM2: interior, envelopeM2: HULL_ENVELOPE_M2,
           interiorOverEnvelope: interior / HULL_ENVELOPE_M2,
           sharedFractionPct: 100 * interior / (interior + HULL_ENVELOPE_M2) };
}

/* Space-filling cell shapes: shared-wall area per m3, normalised by cell volume^(1/3).
 * The cube's 3.0 is what CELL_AREA_COEFF charges everywhere — conservative. The Kelvin cell
 * (truncated octahedron) is the interlocking near-sphere the design intends, 11.4% better. */
export function cellShapes() {
  const entry = (vol, area) => (area / 2) / vol * Math.pow(vol, 1 / 3);
  const kelvin = entry(8 * Math.SQRT2, 6 + 12 * Math.sqrt(3));
  const shapes = {
    cube: entry(1, 6),
    rhombicDodecahedron: entry(16 * Math.sqrt(3) / 9, 8 * Math.SQRT2),
    truncatedOctahedron: kelvin,
    weairePhelan: kelvin * (1 - 0.003),
  };
  const out = {};
  for (const [k, c] of Object.entries(shapes)) {
    out[k] = { coeff: c, filmSavingVsCubePct: 100 * (1 - c / 3) };
  }
  return out;
}

/* Nozzle -> extrusion width -> wall -> strut -> cell. The optimum tube wall is a FIXED
 * fraction of strut length, so the thinnest reliable wall sets the smallest cell at the
 * right proportions. 0.6 mm hardened x 2 perimeters is the design point: chopped carbon
 * abrades brass and bridges a 0.4 mm orifice. 251 mm struts fit a 256 mm bed. */
export function printerChain(m) {
  const t = tubeStrut(m);
  const wps = t.wallPerStrutLength;
  return [[0.4, 2], [0.6, 2], [0.6, 3], [1.0, 2]].map(([nozzleMm, perims]) => {
    const wallMm = nozzleMm * perims;
    const strut = wallMm / 1000 / wps;
    const cell = strut * Math.SQRT2;
    return { nozzleMm, perimeters: perims, wallMm,
             strutM: strut, cellM: cell,
             enclosedL: cell ** 3 * 1000,
             tubeRadiusMm: t.lam * strut * 1000,
             designPoint: nozzleMm === 0.6 && perims === 2 };
  });
}

/* The Kelvin demonstrator's lattice, counted exactly. Fill a Kelvin cell of span 2p with
 * the octet grid at pitch p: every lattice coordinate is a multiple of p/2, so in units of
 * p/2 the nodes are the integer triples with max|u| <= 2 and |ux|+|uy|+|uz| <= 3 (square
 * and hexagon planes), and the struts are the <110>-step pairs inside. Exact integers —
 * the Python mirrors this arithmetic and the parity gate holds the counts identical.
 * Boundary nodes (either bound met with equality) are where the skin is bonded. */
export function kelvinLatticeCounts(n = 1) {
  const lim = 2 * n;
  // FCC ONLY: coordinate sum even. The first version admitted every integer triple — two
  // interleaved octet lattices, twice the design density; the ratio test caught it.
  const inside = (u) => {
    const a = Math.abs(u[0]), b = Math.abs(u[1]), c = Math.abs(u[2]);
    return Math.max(a, b, c) <= lim && a + b + c <= 3 * n &&
      ((u[0] + u[1] + u[2]) % 2 + 2) % 2 === 0;
  };
  const onBoundary = (u) => {
    const a = Math.abs(u[0]), b = Math.abs(u[1]), c = Math.abs(u[2]);
    return Math.max(a, b, c) === lim || a + b + c === 3 * n;
  };
  const nodes = [];
  for (let x = -lim; x <= lim; x++) for (let y = -lim; y <= lim; y++) {
    for (let z = -lim; z <= lim; z++) {
      if (inside([x, y, z])) nodes.push([x, y, z]);
    }
  }
  const STEPS = [];
  for (const [a, b] of [[1, 1], [1, -1]]) {
    STEPS.push([a, b, 0], [a, 0, b], [0, a, b]);
  }
  let struts = 0;
  for (const u of nodes) {
    for (const s of STEPS) {
      const v = [u[0] + s[0], u[1] + s[1], u[2] + s[2]];
      if (inside(v)) struts++;               // each pair counted once: steps are one-sided
    }
  }
  const boundaryNodes = nodes.filter(onBoundary).length;
  // The rim frame: the octet has no nodes in the hexagon faces (their centres belong to
  // the dual lattice), so the skin is framed by printed members along the 36 edges — each
  // exactly n strut-lengths — joined at the 24 rim vertices, all INSET beneath the true
  // faces so the mating planes stay flat.
  //
  // VERTEX TIES — the load path the designer caught missing (2026-08-10): the 24 rim
  // vertices are permutations of (0, +-n, +-2n), coordinate sum ODD — dual sites. The rim
  // never touched the octet; they shared only the 6 square-centre nodes. Fix: 2 ties per
  // vertex to its nearest even-parity sites — <100> half-steps at n = 1, <110> full steps
  // at n >= 2. Equivalents are length-weighted at the same section.
  const tieStrutEquivalents = n === 1 ? 48 / Math.sqrt(2) : 48;
  // HEXAGON SUPPORT — the designer's second catch, same day: hexagon centres, at
  // permutations of (+-n,+-n,+-n), have coordinate sum 3n — real lattice sites at EVEN n,
  // dual sites at ODD n. At odd n each of the 8 faces gets a deliberate dual-site node
  // plus a tripod of three <100> half-step ties to its even neighbours; the tripod also
  // halves the skin's unsupported span and gives mating cells a shared bond point.
  // PARITY DECIDES WHETHER A BOUNDARY FRAME IS NEEDED AT ALL. A hexagon face lies in the
  // plane sum(s*u) = 3n: at ODD n that sum is odd, so the plane holds NO even-parity site
  // and the face is bare — the article must carry its own rim, hub, spokes and ties. At
  // EVEN n the plane is full of lattice sites and the film bonds straight to the octet,
  // so the whole boundary apparatus disappears. The floater wants an EVEN-n article.
  const odd = n % 2 === 1;
  const hexNodes = odd ? 8 : 0;
  const hexTieStruts = odd ? 24 : 0;
  const hexTieStrutEquivalents = odd ? hexTieStruts / Math.sqrt(2) : 0;
  // HEXAGON SPOKES — the designer's third catch: the squares were already braced in plane
  // (24 of the 48 vertex ties lie exactly in the square face planes) while the hexagons
  // had nothing. Six radial spokes per face, and they are the same cut as every primary:
  // the hexagon's circumradius IS the strut length.
  const hexSpokeStruts = odd ? 48 : 0;
  const hexSpokeStrutEquivalents = odd ? 48 * n : 0;
  return { struts, nodes: nodes.length, boundaryNodes,
           rimStrutEquivalents: odd ? 36 * n : 0, rimNodes: odd ? 24 : 0,
           tieStruts: odd ? 48 : 0, tieStrutEquivalents: odd ? tieStrutEquivalents : 0,
           hexNodes, hexTieStruts, hexTieStrutEquivalents,
           hexSpokeStruts, hexSpokeStrutEquivalents, boundaryFrameNeeded: odd };
}

/* A truncated octahedron's edge and areas, from its span across the square faces. THE EDGE
 * IS span/(2*sqrt2), NOT span/4 — two functions wrote span/4 and understated every film
 * area by exactly two. The tell is decisive: the wrong area is LESS than the equal-volume
 * sphere's, which no shape can be. Mirrored in the Python. */
export function kelvinFaces(span) {
  const a = span / (2 * Math.SQRT2);
  const areaM2 = (6 + 12 * Math.sqrt(3)) * a * a;
  return { edgeM: a, hexM2: 3 * Math.sqrt(3) / 2 * a * a, sqM2: a * a, areaM2,
           areaOverVolume: areaM2 / (span ** 3 / 2) };
}

/* Panel inradius as a fraction of the cell edge, per bracing scheme; barrier() wants twice
 * this, the same convention the unbraced hexagon always used. */
export const PANEL = {
  hexUnbraced: Math.sqrt(3) / 2,
  hexSpoked: 1 / (2 * Math.sqrt(3)),
  squareSpoked: 1 / (2 + Math.SQRT2),
};

/* Film mass for one article, priced PER FACE TYPE. The squares are smaller AND already
 * braced by the in-plane ties; only the hexagons were bare. */
export function filmKg(span, hexScheme = 'hexSpoked') {
  const f = kelvinFaces(span);
  return 8 * f.hexM2 * barrierKgPerM2(2 * PANEL[hexScheme] * f.edgeM)
       + 6 * f.sqM2 * barrierKgPerM2(2 * PANEL.squareSpoked * f.edgeM);
}

/* Membrane tension in one bulged panel and the sine of its tilt off the face plane. A
 * bulge of h = 0.25a is a spherical cap of radius (a^2+h^2)/2h, so T = pR/2 and the film
 * meets its boundary tilted by alpha with sin(alpha) = a/R — 0.4707, and independent of
 * panel size. filmEdgeLoads takes the out-of-plane part into bending, memberDemands takes
 * the in-plane part into axial; one function because two copies of the bulge geometry is
 * what the parity gate exists to catch. Mirrored in the Python. */
export function panelTension(irM, p = P_ATM) {
  const rB = (irM * irM + (0.25 * irM) ** 2) / (2 * 0.25 * irM);
  return [p * rB / 2, irM / rB];
}

/* Each panel's pressure resultant, split equally among the corners that carry it. A bulged
 * panel hands its frame exactly p*(flat area) along the inward face normal whatever the
 * bulge does; the in-plane parts are self-equilibrated and are memberDemands' other load
 * set. Spokes cut a hexagon into six triangles and in-plane ties cut a square into four, so
 * a corner takes a third of each triangle it belongs to: the hub is a corner of all six
 * (H/3) and each hexagon vertex of two (H/9); the square centre of all four (Q/3), each
 * square vertex of two (Q/6). */
export function faceShares(span, p = P_ATM) {
  const f = kelvinFaces(span);
  const h = p * f.hexM2, q = p * f.sqM2;
  return { hexFaceN: h, sqFaceN: q, hexToHubN: h / 3, hexToVertexN: h / 9,
           sqToCentreN: q / 3, sqToVertexN: q / 6 };
}

/* WHAT EACH FAMILY REACTS — every axial demand in the article, from its own load path.
 * One number used to be published as perStrutDemandN and handed to all 216 members, with a
 * comment reading "96 = 60 octet + 36 rim"; that sent crush to members that carry none and
 * left the 48 hexagon spokes with no derived demand at all.
 *
 * DO NOT "FIX" THE 96 TO 144. It is not a member count of this article, it is the octet
 * lattice's strut count per Kelvin-cell VOLUME and it is exact: FCC at half-pitch runs 3
 * struts per cubic half-pitch and the cell encloses 32 of them, 3*32 = 96. phi = 96*A*L/V
 * is what sigma = 3p/phi is evaluated on.
 *
 * Two load sets that do not mix. CRUSH is the array's hydrostatic field and only the octet
 * carries it — the rim vertices are dual-lattice sites, so no rim member is even an octet
 * strut, and at even n the whole boundary apparatus does not exist. THE FILM is the
 * standalone article's alone, and splits into a normal resultant (faceShares), which the
 * <100> props and the four struts at each square centre react exactly, and a
 * self-equilibrated in-plane pull q = T*cos(alpha) per edge, whose path is indeterminate
 * between the face's radial member and hoop in the rim — so both are sized for all of it.
 * Bending is filmEdgeLoads' business and governs the rim. Mirrored in the Python. */
export function memberDemands(span, sf = LATTICE_SF, p = P_ATM) {
  const f = kelvinFaces(span);
  const a = f.edgeM;                       // the cell edge IS the strut length
  const vol = span ** 3 / 2;
  const [tTri, sinA] = panelTension(PANEL.hexSpoked * a, p);
  const [tSq] = panelTension(PANEL.squareSpoked * a, p);
  const cosA = Math.sqrt(1 - sinA * sinA);
  const qHex = tTri * cosA, qSq = tSq * cosA;
  const crush = 3 * p * sf * vol / (96 * a);
  const pa2 = p * sf * a * a;
  const prop = pa2 / 2;                    // hub tripod AND rim-vertex inward tie
  const tieInPlaneNormal = pa2 / 3;        // the square's share at a rim vertex
  const octetEntry = pa2 / (6 * Math.SQRT2);
  // A vertex's radial tributary is its two half-edges resolved along the radius:
  // sqrt(3)/2*q*a in a hexagon, q*a/sqrt2 in a square. Hoop is the same load the other way
  // round the ring, where a 60 deg kink turns 2N*cos(60) = N loose in a hexagon.
  const spoke = sf * Math.sqrt(3) / 2 * qHex * a;
  const sqRadial = sf * qSq * a / Math.SQRT2;
  const hexHoop = spoke, sqHoop = sf * qSq * a / 2;
  // A rim edge belongs to two faces and both rings can want their hoop in it: 12 of the 36
  // edges are hexagon-hexagon, the other 24 square-hexagon.
  const rimHH = 2 * hexHoop, rimSH = hexHoop + sqHoop;
  const families = {
    octet: crush, rim: rimHH, spoke,
    tripodProp: prop, vertexTieInward: prop,
    vertexTieInPlane: tieInPlaneNormal + sqRadial,
  };
  const shares = faceShares(span, p);
  return {
    safetyFactor: sf, crushDivisor: 96, families,
    crushPerOctetStrutN: crush, octetStandaloneEntryN: octetEntry,
    rimSquareHexEdgeN: rimSH, hexRingHoopN: hexHoop, sqRingHoopN: sqHoop,
    inPlanePullHexNPerM: qHex, inPlanePullSqNPerM: qSq,
    governingShortMemberN: Math.max(families.tripodProp, families.vertexTieInward,
                                    families.vertexTieInPlane),
    externalFilmShareAtSF: Object.fromEntries(
      Object.entries(shares).map(([k, v]) => [k, v * sf])),
  };
}

/* THE CHECK THIS MODEL DID NOT HAVE: boundary members in BENDING under the film, which is
 * what actually governs this article. w = p * tributary width — equilibrium, no membrane
 * theory. Bending is why bracing pays: M ~ w*L^2 with both scaling as the panel, so the
 * moment falls as the CUBE of the bracing pitch. Mirrored in the Python. */
export function filmEdgeLoads(span, sf = LATTICE_SF) {
  const f = kelvinFaces(span);
  const a = f.edgeM;
  const sigmaU = MATERIALS.T700_LAM.sigma;
  const row = (member, w, length, propped = false, ro = 0.005, ri = 0.004) => {
    const Z = (Math.PI / 4 * (ro ** 4 - ri ** 4)) / ro;
    const s = propped ? length / 2 : length;
    const mPin = w * s * s / 8, mCl = w * s * s / 12;
    return { member, lineLoadNPerM: w, spanM: s,
             stressPinnedMPa: mPin / Z / 1e6, stressClampedMPa: mCl / Z / 1e6,
             marginPinnedAtSF: sigmaU / (mPin / Z * sf),
             marginClampedAtSF: sigmaU / (mCl / Z * sf),
             failsAtAtm: sigmaU / (mPin / Z) };
  };
  // Each panel's film pulls along its own tangent, tilted below the face by alpha, with
  // sin(alpha) = a_panel/R (0.4707 at the model's bulge, independent of panel size). For
  // two COPLANAR panels the in-plane parts cancel and 2*T*sin(alpha) is left; at a
  // DIHEDRAL edge they add along the bisector, and the rim load roughly doubles. Missing
  // that is what let the rim look survivable.
  const tension = (ir) => panelTension(ir, P_ATM);
  const dihedral = (t1, t2, sinA, theta) => {
    const cosA = Math.sqrt(1 - sinA * sinA), h = theta / 2;
    return (t1 + t2) * (Math.cos(h) * cosA + Math.sin(h) * sinA);
  };
  const thHH = Math.acos(-1 / 3);
  const [tBare, sa] = tension(PANEL.hexUnbraced * a);
  const [tTri] = tension(PANEL.hexSpoked * a);
  const [tSq] = tension(PANEL.squareSpoked * a);
  const wBare = dihedral(tBare, tBare, sa, thHH);
  const wRim = dihedral(tTri, tTri, sa, thHH);
  const wSpoke = 2 * tTri * sa;
  const wSqTie = 2 * tSq * sa;
  const hub = faceShares(span, P_ATM).hexToHubN;
  return {
    hexFaceLoadN: P_ATM * f.hexM2, squareFaceLoadN: P_ATM * f.sqM2,
    hexFaces: 8, squareFaces: 6,
    totalSurfaceLoadN: P_ATM * f.areaM2,
    totalSurfaceLoadTf: P_ATM * f.areaM2 / 9806.65,
    rows: [row('rim edge, hexagons UNBRACED (the design as it stood)', wBare, a),
           row('rim edge, hexagons spoked, 10x8', wRim, a),
           row('rim edge, hexagons spoked, 14x12', wRim, a, false, 0.007, 0.006),
           row('hexagon spoke, 10x8 (two coplanar panels)', wSpoke, a),
           row('hexagon spoke, midspan-propped', wSpoke, a, true),
           row('in-plane square tie (two coplanar panels)', wSqTie, a / Math.SQRT2)],
    bulgeVolumeLostPct: 100 * (8 * f.hexM2 * 0.25 * PANEL.hexSpoked * a / 2
      + 6 * f.sqM2 * 0.25 * PANEL.squareSpoked * a / 2) / (span ** 3 / 2),
    bulgeVolumeLostUnbracedPct: 100 * (8 * f.hexM2 * 0.25 * PANEL.hexUnbraced * a / 2
      + 6 * f.sqM2 * 0.25 * PANEL.squareSpoked * a / 2) / (span ** 3 / 2),
    hubShareN: hub,
    // Three <100> props at 54.74 deg to the face normal: the axial components sum to
    // 3*cos(54.74) = sqrt(3), so each carries F/sqrt(3) — not F/3.
    tripodPropN: hub / Math.sqrt(3),
    tripodPropNAtSF: hub / Math.sqrt(3) * sf,
  };
}

/* The printable proof-of-concept article — and it is NOT a cube. The design's cell is the
 * interlocking near-sphere, and the half-pitch meshing makes it buildable from the exact
 * same parts: a Kelvin cell of span 2x the printer-chain pitch, filled with the SAME
 * co-critical 251 mm struts, boundary nodes landing exactly in the faces, skin bonded on
 * them. A PAHT-CF lattice is still ~20x the wall at any size — relative density is
 * scale-free, so it does not float and is not supposed to. What it proves: print,
 * assemble, wrap, pump down, SEAL, hold for months, and carry a full atmosphere at the
 * co-critical proportions with at least the designed margin. */
export function demonstrator(m) {
  const t = tubeStrut(m);
  const chain = printerChain(m).find(r => r.designPoint);
  const p = chain.cellM;                      // the sub-cell pitch from the printer chain
  const spanM = 2 * p;                        // the Kelvin article, across its squares
  const vol = spanM ** 3 / 2;                 // BCC packs two Kelvin cells per span^3
  const counts = kelvinLatticeCounts();
  const rM = chain.tubeRadiusMm / 1000;
  const wallM = chain.wallMm / 1000;
  const strutKg = 2 * Math.PI * rM * wallM * chain.strutM * m.rho;   // thin-tube annulus
  const nStruts = counts.struts + counts.rimStrutEquivalents;
  const latKg = (nStruts + counts.tieStrutEquivalents + counts.hexTieStrutEquivalents
                 + counts.hexSpokeStrutEquivalents) * strutKg;
  const nodesKg = latKg * NODE_MASS_FRAC;
  // Kelvin surface area (6 + 12*sqrt(3)) s^2 at s = span/4; panels span up to the hexagon
  // across-flats (0.612 x span) between the rim frame and the interior grid.
  const areaM2 = kelvinFaces(spanM).areaM2;
  // Priced per face type at the panel each face actually has, on the true area.
  const film = filmKg(spanM);
  const displaced = 1.225 * vol;
  const totalKg = latKg + nodesKg + film;
  return { strutM: chain.strutM, cellM: p, spanM, enclosedL: vol * 1000,
           wallMm: chain.wallMm, tubeRadiusMm: chain.tubeRadiusMm,
           tubeROverT: t.tubeROverT,
           printedStruts: nStruts + counts.tieStruts + counts.hexTieStruts
                          + counts.hexSpokeStruts,
           printedNodes: counts.nodes + counts.rimNodes + counts.hexNodes,
           hexSpokeStruts: counts.hexSpokeStruts,
           octetStruts: counts.struts, rimStruts: counts.rimStrutEquivalents,
           tieStruts: counts.tieStruts, hexTieStruts: counts.hexTieStruts,
           hexNodes: counts.hexNodes,
           boundaryNodes: counts.boundaryNodes,
           inArrayShareKg: t.phi * m.rho * vol * (1 + NODE_MASS_FRAC) + film,
           latticeKg: latKg, nodesKg, filmKg: film,
           totalKg, displacedAirKg: displaced,
           massOverDisplaced: totalKg / displaced,
           crushMarginAtSeaLevelAtLeast: LATTICE_SF, floats: false };
}

/* The HYBRID article: purchased carbon pipe mains, printed everything else. The designer's
 * question that reframed the build (2026-08-10): "could this be assembled mainly from CF
 * stock and 3d printed connectors??" Yes — all 96 primary members are one SKU (identical
 * 251 mm cuts, rim included), the nodes are already printed sockets a pipe end seats into,
 * and pultruded tube IS the T700_LAM row. 96 purchased pipes, 48 printed vertex ties
 * (secondary — skin-edge loads, not primary crush), 43 printed node-sockets, film skin.
 * The 10 x 8 mm pipe holds its Euler margin even PINNED; socket fixity is bonus, and E5
 * crushes one strut+sockets to verify it. Mirrored in the Python. */
export function stockBuild() {
  const m = MATERIALS.T700_LAM;
  const chain = printerChain(MATERIALS.PAHT_Z).find(r => r.designPoint);
  const p = chain.cellM;
  const spanM = 2 * p;
  const vol = spanM ** 3 / 2;
  const L = chain.strutM;
  const counts = kelvinLatticeCounts();
  // ONE DEMAND PER FAMILY, each from the load path that puts it there. This was a single
  // 3*pd*vol/(96*L) handed to all 216 members; memberDemands says why 96 is right for the
  // octet and wrong for everyone else.
  const dem = memberDemands(spanM);
  const fDemand = dem.families.octet;
  const ro = 0.010 / 2, ri = 0.008 / 2;          // 10 x 8 roll-wrapped, catalogue dims
  const area = Math.PI * (ro ** 2 - ri ** 2);
  const inertia = Math.PI / 4 * (ro ** 4 - ri ** 4);
  const pcrPinned = Math.PI ** 2 * m.E * inertia / L ** 2;
  const pcrSocketed = pcrPinned / 0.65 ** 2;
  // TWO SKUs, TWO CUTS. The designer proposed a SMALLER pipe for the secondaries; carbon
  // yes, smaller no — sized against the film load they actually react, node by node, the
  // ties come out ABOVE the octet's own crush demand. They are the most loaded members in
  // the article, and the worst of them is the in-plane square tie, not the hexagon tripod.
  const kgPerM = area * m.rho;
  // TWO SKUs: the 36 cell edges carry the film's dihedral pull, twice what a spoke inside
  // a flat face sees, and need 14 x 12. Everything else stays on the 10 x 8.
  const rimKgPerM = Math.PI * ((0.014 / 2) ** 2 - (0.012 / 2) ** 2) * m.rho;
  const rimCuts = counts.rimStrutEquivalents;
  // 251 mm on the 10 x 8: the octet interior and the hexagon spokes. Written as
  // "96 - rimCuts + spokes" until 2026-08-11, reaching the right 108 by subtracting the rim
  // frame from a number that never contained it (see memberDemands on the 96).
  const longCuts = counts.struts + counts.hexSpokeStruts;
  const shortCuts = counts.tieStruts + counts.hexTieStruts;  // 177 mm
  const longKg = kgPerM * L * longCuts + rimKgPerM * L * rimCuts;
  const shortKg = kgPerM * (L / Math.SQRT2) * shortCuts;
  // Node mass is MEASURED by gen_nodes.py, not budgeted at 15% of strut mass; the page
  // reads the figure the Python read from the generator's manifest.
  const nodesKg = NODE_MASS_MEASURED_KG;
  const skinKg = filmKg(spanM);
  const totalKg = longKg + shortKg + nodesKg + skinKg;
  const displaced = 1.225 * vol;
  const loads = filmEdgeLoads(spanM);
  // ALL 72 SHORT MEMBERS ARE SIZED AT THE WORST OF THEM, which is no longer the hexagon
  // tripod prop: the 24 in-plane square ties carry the square's share of a rim vertex AND
  // that panel's in-plane radial pull, and the sum is above the prop's p*a^2/2.
  const tieDemand = dem.governingShortMemberN;
  const rimDemand = dem.families.rim, spokeDemand = dem.families.spoke;
  const pcrTie = Math.PI ** 2 * m.E * inertia / (L / Math.SQRT2) ** 2;
  const rimInertia = Math.PI / 4 * ((0.014 / 2) ** 4 - (0.012 / 2) ** 4);
  const pcrRim = Math.PI ** 2 * m.E * rimInertia / L ** 2;
  return { spanM, enclosedL: vol * 1000,
           odM: 2 * ro, idM: 2 * ri, rimOdM: 0.014,
           pipeCount: longCuts + rimCuts + shortCuts, longCuts, rimCuts, shortCuts,
           pipeCutM: L, shortCutM: L / Math.SQRT2,
           pipeTotalLengthM: (longCuts + rimCuts) * L + shortCuts * L / Math.SQRT2,
           pipeKg: longKg + shortKg,
           // perStrutDemandN is the OCTET's demand and nothing else's; every family has its
           // own number in demands, and reading this one for a rim or a spoke is the defect
           // that made the article's margins agree by accident.
           perStrutDemandN: fDemand,
           eulerMarginPinned: pcrPinned / fDemand,
           eulerMarginSocketed: pcrSocketed / fDemand,
           stressMargin: m.sigma * area / fDemand,
           rimDemandN: rimDemand, rimEulerMargin: pcrRim / rimDemand,
           spokeDemandN: spokeDemand, spokeEulerMargin: pcrPinned / spokeDemand,
           tieDemandN: tieDemand,
           tieEulerMargin: pcrTie / tieDemand,
           printedNodes: counts.nodes + counts.rimNodes + counts.hexNodes, nodesKg,
           skinKg, totalKg, displacedAirKg: displaced,
           // The article in the unit the wall is written in. Generated on both sides for the
           // same reason every other figure here is: the note quoted 16.06 kg/m3 by hand for a
           // fortnight after the joints moved from 0.444 to 0.465 kg, and nothing caught it.
           kgPerM3: totalKg / vol,
           governing: loads.rows[2],
           massOverDisplaced: totalKg / displaced, floats: false };
}

/* The pumped plenum: a soft, lossy, actively pumped partial vacuum across the whole ship,
 * so no interior cell operates against a full atmosphere. The ACTIVE member of the graded-
 * band family. Statics unchanged — the shell's mounts deliver the withheld atmosphere into
 * the array as structure load, so no lattice saving; what it buys is margin, permeation
 * life and breach softening, each scaling directly with the plenum pressure, plus graceful
 * pump-failure (a slow drift back to the 1 atm design case). Pump power needs a shell
 * leak-rate assumption that remains deliberately unchosen. */
export function pumpedPlenum() {
  return [1.0, 0.5, 0.25, 0.1].map(p => ({
    plenumAtm: p,
    cellOperatingMarginX: LATTICE_SF / p,
    permeationDriveX: p,
    breachFloodsToAtm: p,
  }));
}

/* Could a sealed article of this design weigh ZERO? Sized here, per rung of the material
 * ladder. The ladder's kg/m3 are IN-ARRAY densities; a standalone article pays a boundary
 * surcharge (its skin struts and rim are shared with nobody) that falls toward 1 as the
 * article grows, so each rung has a MINIMUM WEIGHTLESS SIZE at N half-span sub-cells per
 * side. Sea level (1.225 kg/m3) is the natural bench condition. Mirrored in the Python. */
/* The standalone article's film per cubic metre, and PARITY DECIDES THE SCALING. The old
 * term carried the span/4 area error AND divided by n a second time although what it
 * computed was already scale-free. Which is true depends on parity: at EVEN n the hexagon
 * faces are full of lattice sites, the film bonds to the octet at the lattice's own pitch,
 * the panel stays one cell wide however large the article grows, and the term falls as
 * 1/n. At ODD n the faces are bare, the panels grow with the article, and there is no
 * reward for building bigger. Mirrored in the Python. */
export function articleFilmKgPerM3(n, pitch = 0.3545) {
  const span = 2 * n * pitch;
  const f = kelvinFaces(span);
  if (n % 2 === 0) {
    const a1 = 2 * pitch / (2 * Math.SQRT2);
    return f.areaM2 * barrierKgPerM2(2 * PANEL.hexSpoked * a1) / (span ** 3 / 2);
  }
  return filmKg(span) / (span ** 3 / 2);
}

export function weightlessArticle(wall) {
  const NET_PER_N3 = 96;
  const rungs = [['PAHT_Z', 4, 'all-printed nylon'],
    ['CFF', 3, 'continuous fibre, printed'],
    ['T700_LAM', 2, 'T700, wound'],
    ['M60J_LAM', 2, 'M60J-class, wound']];
  return rungs.map(([key, level, label]) => {
    const lad = ladder(MATERIALS[key], 5, 0);
    const lat = lad[level].lattice * (1 + NODE_MASS_FRAC);
    let minNSeaLevel = null, minNAt2500m = null, densityAtN1 = null;
    for (let n = 1; n <= 12; n++) {
      const c = kelvinLatticeCounts(n);
      const ratio = (c.struts + c.rimStrutEquivalents + c.tieStrutEquivalents +
        c.hexTieStrutEquivalents + c.hexSpokeStrutEquivalents) / (NET_PER_N3 * n ** 3);
      const rho = lat * ratio + articleFilmKgPerM3(n);
      if (n === 1) densityAtN1 = rho;
      if (minNSeaLevel === null && rho < 1.225) minNSeaLevel = n;
      if (minNAt2500m === null && rho < wall) minNAt2500m = n;
    }
    return { key, label, level, densityAtN1, minNSeaLevel, minNAt2500m };
  });
}

/* Graded pressure, statics-correct THIRD model. Version one double-counted the load path;
 * version two claimed the gas columns carry the compression so the lattice sees only its
 * local step — refuted by a reviewer's force balance: gas transmits compression only up to
 * its own pressure, so the solid carries P_atm minus the local gas pressure and the load
 * ACCUMULATES inward. Zone j's lattice is sized for its cumulative j/N atm; the envelope
 * film is priced for the differential it actually sees. In bulk, grading surrenders over
 * half the net lift; as a thin outer band, the tenfold-lighter envelope film pays for the
 * band's gas — roughly free in mass, tenfold gentler on the outer surface. */
export function gradedPressure(m, wall) {
  const lad = ladder(m, 5, 0);
  const lat2 = lad[2].lattice;
  const filmAtm = barrierKgPerM3(2.0);
  const stackFactor = (n) => {
    let s = 0;
    for (let j = 1; j <= n; j++) s += Math.pow(j / n, 0.75);
    return s / n;
  };
  const bulk = [1, 2, 5, 10].map(n => {
    const gas = wall * (n - 1) / (2 * n);
    const struct = lat2 * stackFactor(n) * (1 + NODE_MASS_FRAC);
    const films = (n > 1 ? filmAtm / n : 0) + envelopeFilmKgPerM3(2.0, 1 / n);
    return { levels: n, structure: struct, gas, films,
             netLift: wall - struct - gas - films };
  });
  const f = 0.05, nb = 10;
  const gasCost = f * wall * (nb - 1) / (2 * nb);
  const structDelta = f * lat2 * (stackFactor(nb) - 1) * (1 + NODE_MASS_FRAC);
  const filmDelta = f * filmAtm / nb;
  const envelopeDelta = envelopeFilmKgPerM3(2.0, 1 / nb) - envelopeFilmKgPerM3(2.0, 1);
  const netCost = gasCost + structDelta + filmDelta + envelopeDelta;
  return {
    bulk,
    band: { bandVolumeFraction: f, levels: nb,
            outerSurfaceDifferentialAtm: 1 / nb,
            gasCost, structDelta, filmDelta, envelopeDelta, netCost,
            costPctOfNetLift: 100 * netCost / bulk[0].netLift },
  };
}
