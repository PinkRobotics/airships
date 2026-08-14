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
import { mountExplorer, LEVELS } from './explorer.js?v=60a254ea';

export function mountShipHero(canvas) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const api = mountExplorer({
    canvas,
    reducedMotion: reduced,
    lite: true,
    envRing: true,
    layers: { env: true },
    startLevel: LEVELS.findIndex((l) => l.id === 'vessel'),
    // Letterboxed banner framing: a touch above the beam and far enough out that
    // the ship, the raft below it and the whole shore ring share the frame.
    pose: { el: 0.24, d: 290 },
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
