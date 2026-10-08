/* A dump of what the monitor actually SHOWS, for comparing a refactor against itself.
 *
 * The model has a golden file of its own; this covers the half a numeric dump cannot —
 * that the panels, tables, instruments and map still render the same thing. Text is
 * compared exactly; the map must remain visible, nonzero and drawn with varied pixels. */
(async () => {
  // The page publishes readiness after boot; route planning yields between missions.
  // Navigation time is not proof of completion on a loaded hosted runner.
  const deadline = performance.now() + 180000;
  while (!(window.AIRSHIPS ? (window.AIRSHIPS.app?.ready && window.AIRSHIPS.app.planning?.state === 'settled') : (typeof S !== 'undefined' && S.ready !== false && (!S.planning || S.planning.state === 'settled') && S.missions?.length && S.missions.every(m => m.idle || m.plan)))) {
    if (performance.now() >= deadline) throw new Error('golden: readiness deadline exceeded (180 s)');
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  const ov = document.getElementById('introOv'); if (ov) ov.click();

  /* PIN THE CLOCK before reading anything. The simulation advances in real time from the
     moment the page loads, so a dump taken "four seconds in" is really a dump of whatever
     the fleet happened to be doing after however long this particular load took. Freeze it
     at a fixed point in the cycle, let two frames render against that, and the comparison
     is of the interface rather than of the machine's mood. */
  /* PIN THE CLOCK FIRST, then settle, then pin again.
     
     Pinning only after the settle poll left a window — up to six seconds of it — in which the
     page was running at whatever speed it booted with, and the roster and the fire list are
     painted by a throttled 1.5 s tick. If that tick landed inside the window it recorded a
     running clock and did not necessarily repaint afterwards, so the dump captured a fleet
     several phases further round its cycle than the pinned time. It reproduced every run on
     this machine and not at all when the same page was driven by hand, which is the signature
     of a race rather than a change. Freeze it before anything is allowed to observe it. */
  {
    const A0 = window.AIRSHIPS ? window.AIRSHIPS.app : S;
    A0.paused = true;
    A0.simTime = 4200;
  }
  /* WAIT FOR THE LAYOUT TO SETTLE. The map canvas is sized by the grid, and the grid moves
     while the 3D panel mounts and the avatar claims its leftover space. Capturing "after
     four seconds" therefore records whichever moment the machine happened to reach — this
     dump differed by 22 pixels of map height between a laptop and a CI runner, which is a
     flaky gate, not a regression. Poll until the height stops changing. */
  {
    const el = document.getElementById('map');
    let last = -1, stable = 0;
    const layoutDeadline = performance.now() + 180000;
    while (stable < 3) {
      if (performance.now() >= layoutDeadline) throw new Error('golden UI layout did not settle within 180 s');
      await new Promise(r => setTimeout(r, 150));
      const h = el ? el.clientHeight : 0;
      stable = h > 0 && h === last ? stable + 1 : 0;
      last = h;
    }
  }

  const APPSTATE = window.AIRSHIPS ? window.AIRSHIPS.app : S;
  APPSTATE.paused = true;
  APPSTATE.simTime = 4200;
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  await new Promise(r => setTimeout(r, 1600));
  // The production slow-text tick deliberately skips paused simulations. Repaint
  // that text explicitly from the pinned state instead of retaining a boot-time
  // percentage. Load the same stamped module instance as the application.
  if (window.AIRSHIPS) {
    const main = document.querySelector('script[type="module"][src*="app/main.js"]');
    if (!main) throw new Error('golden UI application module is absent');
    const moduleURL = new URL('cockpit/panels.js', main.src);
    moduleURL.search = new URL(main.src).search;
    const panels = await import(moduleURL.href);
    panels.updateCockpitText();
    const mission = APPSTATE.sel?.m;
    if (mission && !mission.idle) {
      const Q = window.AIRSHIPS.sim;
      const expected = Q.narrate(mission, Q.stateAt(mission, APPSTATE.simTime));
      for (const [i, key] of ['last', 'now', 'next', 'plan'].entries()) {
        if (document.getElementById('opsN' + i)?.textContent !== expected[key])
          throw new Error('golden UI narration differs from the pinned state: ' + key);
      }
    }
  }
  const txt = (sel) => {
    const e = document.querySelector(sel);
    const value = e?.textContent.replace(/\s+/g, ' ').trim();
    if (!value) throw new Error(`golden UI selector is absent or empty: ${sel}`);
    return value;
  };
  return JSON.stringify({
    title: document.title,
    roster: txt('#roster'),
    fires: txt('#firesTop'),
    focus: txt('#cpShip'),
    forces: txt('#cpForces'),
    ops: txt('#cpOps'),
    status: txt('#modeNote'),
    /* There is no statistics element on the monitor. Model quantities are held by
       dump.js; keeping a null #stats key here would assert no rendered behaviour. */
    dialCount: document.querySelectorAll('.dialgrid svg, #phaseDial svg').length,
    bars: txt('#pwrBars'),
    /* Height is layout, not a model fact: browser modes can settle at different heights.
       Still require a visible, nonzero canvas with varied, opaque pixels. A 2D context
       alone says nothing about whether a map was drawn into it. Width remains pinned. */
    map: (() => {
      const c = document.getElementById('map');
      if (!c) return null;
      const rect = c.getBoundingClientRect();
      if (!c.width || !c.height || !rect.width || !rect.height) return 'collapsed';
      if (getComputedStyle(c).visibility === 'hidden') return 'hidden';
      const g = c.getContext('2d');
      if (!g) return 'no context';
      let pixels;
      try { pixels = g.getImageData(0, 0, c.width, c.height).data; }
      catch (_) { return 'unreadable'; }
      let first = null, varied = false;
      for (let i = 0; i < pixels.length; i += 4 * 97) {
        if (!pixels[i + 3]) continue;
        const color = (pixels[i] << 16) | (pixels[i + 1] << 8) | pixels[i + 2];
        if (first === null) first = color;
        else if (color !== first) { varied = true; break; }
      }
      return `${c.width}:${varied ? 'drawn' : 'blank'}`;
    })(),
    m3dMounted: !!document.querySelector('#m3dView canvas'),
    avatar: (() => { const c = document.getElementById('shipviz');
      return c ? `${c.width}x${c.height}:${c.getContext('2d') ? 'drawing' : '-'}` : null; })(),
    selected: APPSTATE.sel ? APPSTATE.sel.type : null,
    ships: APPSTATE.missions.filter(m => !m.idle).length,
    errors: window.__err || [],
  });
})()
