/* A dump of what the monitor actually SHOWS, for comparing a refactor against itself.
 *
 * The model has a golden file of its own; this covers the half a numeric dump cannot —
 * that the panels, tables, instruments and map still render the same thing. Text is
 * compared exactly; the map must remain visible, nonzero and drawn with varied pixels. */
(async () => {
  const ov = document.getElementById('introOv'); if (ov) ov.click();
  await new Promise(r => setTimeout(r, 4000));

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
    for (let i = 0; i < 40 && stable < 3; i++) {
      await new Promise(r => setTimeout(r, 150));
      const h = el ? el.clientHeight : 0;
      stable = h === last ? stable + 1 : 0;
      last = h;
    }
  }

  const APPSTATE = window.AIRSHIPS ? window.AIRSHIPS.app : S;
  APPSTATE.paused = true;
  APPSTATE.simTime = 4200;
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  await new Promise(r => setTimeout(r, 1600));   // the 1.5 s slow-text tick
  const txt = (sel) => {
    const e = document.querySelector(sel);
    return e ? e.textContent.replace(/\s+/g, ' ').trim() : null;
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
