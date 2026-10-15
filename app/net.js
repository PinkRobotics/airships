/* First-party JSON reads, bounded by a timeout. */
/* Every failure this can produce is tagged, because the caller has to tell them apart: a
 * file that timed out may be worth trying again later, one that answered with something
 * that is not JSON will answer the same way in five minutes, and the visitor is owed the
 * difference in words. An untagged rejection is a transport failure — DNS, offline, CORS,
 * connection reset — and carries the browser's own message.
 *
 *   e.timeout    we aborted it ourselves after `ms`
 *   e.http       the server answered with a non-2xx status (the number is on the tag)
 *   e.malformed  it answered, but the body did not parse as JSON
 *
 * Every URL this fetches is a static file this site serves itself. Nothing here talks to a
 * wildfire feed: the page asks no agency for anything, live or mirrored. */
export async function fetchJSON(url, ms) {
  const lim = ms || 15000;
  const ctl = new AbortController();
  let timedOut = false;
  const t = setTimeout(() => { timedOut = true; ctl.abort(); }, lim);
  try {
    const r = await fetch(url, { signal: ctl.signal });
    if (!r.ok) throw Object.assign(new Error("HTTP " + r.status), { http: r.status });
    try {
      return await r.json();
    } catch (e) {
      // An abort during the body read is a timeout, not a malformed body; only decide it
      // is malformed once we know we did not cut it off ourselves.
      if (timedOut) throw e;
      throw Object.assign(new Error("malformed body"), { malformed: true });
    }
  } catch (e) {
    if (timedOut) {
      throw Object.assign(new Error("timed out after " + Math.round(lim / 1000) + " s"),
        { timeout: true });
    }
    throw e;
  } finally { clearTimeout(t); }
}

/* localStorage, treated as the convenience it is.
 *
 * Both reading and writing it THROW rather than return null in ordinary browsers: a Safari
 * or Firefox private window, any browser set to block site storage, an origin whose quota is
 * full, and — in Chromium — merely touching the `localStorage` global with third-party
 * storage blocked. One unguarded getItem during boot is therefore a blank page for a visitor
 * whose only unusual act was opening a private window. Nothing on this page needs storage:
 * without it the visitor gets the whole monitor and simply is not remembered.
 *
 * These two functions are the only place the page touches it. A failed read means "nothing
 * stored", a failed write means "this will not be remembered", and neither is worth
 * interrupting anyone over. */
export function storeGet(key) {
  try { return localStorage.getItem(key); } catch (e) { return null; }
}

export function storeSet(key, value) {
  try { localStorage.setItem(key, value); return true; } catch (e) { return false; }
}
