/* The front page's spinning ship — the explorer's own vessel scene, booted with no
 * controls at all. One model everywhere: this imports the same mountExplorer the
 * public viewer runs, in lite mode, so the hull on the front page can never drift
 * from the hull in the viewer. What lite mode buys on a landing page:
 *
 *   - only The Ship level builds; the six joint-scale levels get empty shells,
 *   - the 6.5 MB of joint display meshes never load (they are a lazy module now),
 *   - no listeners attach: the page never captures a scroll, a drag or a key.
 *
 * The turntable is the viewer's own idle spin, which runs from the first frame
 * until an interaction — and here no interaction can ever come. The environment
 * boots already on, with the tree line and the watchers closing the full circle
 * (ctx.envRing), so the ship has company from every azimuth as it turns.
 * prefers-reduced-motion gets a still ship; a machine without WebGL2 keeps
 * whatever fallback the hosting section painted behind the canvas. */
import { mountExplorer, LEVELS } from './explorer.js?v=dd91118e';

export function mountShipHero(canvas) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const api = mountExplorer({
    canvas,
    reducedMotion: reduced,
    lite: true,
    envRing: true,
    transparentSky: true,      // the ship floats over the page; sky pixels are the page
    layers: { env: true },
    startLevel: LEVELS.findIndex((l) => l.id === 'vessel'),
    // Tight framing (operator, 08-14): the whole machine fills the frame — hull
    // top to the bucket at the water, raft and lines included — with minimal
    // margin. Target sits mid-stack (hull top +26 m, water -60 m); 32-degree
    // vertical fov at ~172 m covers the ~95 m stack. The shore ring reads at the
    // frame's edges as it turns, which is what the watchers are for.
    pose: { tg: [0, 0, -17], el: 0.05, d: 172 },
  });
  if (api) canvas.classList.add('live');
  // Spin only while the banner is actually on screen — a hero scrolled past should
  // not keep a phone's GPU warm. api.state is the mount's live state object.
  if (api && 'IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      for (const e of entries) api.state.turntable = e.isIntersecting && !reduced;
    }).observe(canvas);
  }
  return api;
}

// Self-boot when the hosting page marks a canvas for it; a page that wants manual
// control imports mountShipHero instead and leaves the attribute off.
const auto = document.querySelector('canvas[data-ship-hero]');
if (auto) mountShipHero(auto);
