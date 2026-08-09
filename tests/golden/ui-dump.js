/* A dump of what the monitor actually SHOWS, for comparing a refactor against itself.
 *
 * The model has a golden file of its own; this covers the half a numeric dump cannot —
 * that the panels, tables, instruments and map still render the same thing. Text is
 * compared exactly; the canvases are compared by a cheap pixel digest, which is enough to
 * catch a layer that stopped drawing or moved. */
(async () => {
  const ov = document.getElementById('introOv'); if (ov) ov.click();
  await new Promise(r => setTimeout(r, 4000));

  /* PIN THE CLOCK before reading anything. The simulation advances in real time from the
     moment the page loads, so a dump taken "four seconds in" is really a dump of whatever
     the fleet happened to be doing after however long this particular load took. Freeze it
     at a fixed point in the cycle, let two frames render against that, and the comparison
     is of the interface rather than of the machine's mood. */
  const APPSTATE = window.AIRSHIPS ? window.AIRSHIPS.app : S;
  APPSTATE.paused = true;
  APPSTATE.simTime = 4200;
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  await new Promise(r => setTimeout(r, 1600));   // the 1.5 s slow-text tick
  const txt = (sel) => {
    const e = document.querySelector(sel);
    return e ? e.textContent.replace(/\s+/g, ' ').trim() : null;
  };
  const digest = (cv) => {
    if (!cv || !cv.width) return null;
    const g = cv.getContext('2d');
    if (!g) return 'webgl';
    let d;
    try {
      d = g.getImageData(0, 0, cv.width, cv.height).data;
    } catch (e) {
      // The basemap tiles come from a third-party host, which taints the canvas and makes
      // its pixels unreadable to us as well as to anyone else. Fall back to geometry.
      return `${cv.width}x${cv.height}:tainted`;
    }
    let h = 0, lit = 0;
    for (let i = 0; i < d.length; i += 4 * 97) {          // every 97th pixel: fast, stable
      h = (h * 31 + d[i] + d[i + 1] * 3 + d[i + 2] * 7) | 0;
      if (d[i + 3]) lit++;
    }
    return `${cv.width}x${cv.height}:${h}:${lit}`;
  };
  return JSON.stringify({
    title: document.title,
    roster: txt('#roster'),
    fires: txt('#firesTop'),
    focus: txt('#cpShip'),
    forces: txt('#cpForces'),
    ops: txt('#ops'),
    status: [...document.querySelectorAll('.statusbar p')]
      .map(e => e.textContent.replace(/\s+/g, ' ').trim()),
    stats: txt('#stats'),
    dialCount: document.querySelectorAll('.dialgrid svg, #phaseDial svg').length,
    bars: txt('#pwrBars'),
    map: digest(document.getElementById('map')),
    m3dMounted: !!document.querySelector('#m3dView canvas'),
    avatar: (() => { const c = document.getElementById('shipviz');
      return c ? `${c.width}x${c.height}:${c.getContext('2d') ? 'drawing' : '-'}` : null; })(),
    selected: APPSTATE.sel ? APPSTATE.sel.type : null,
    ships: APPSTATE.missions.filter(m => !m.idle).length,
    errors: window.__err || [],
  });
})()
