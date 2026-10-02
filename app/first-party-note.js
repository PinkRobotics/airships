/* Report what this browser requested, beside the repository's first-party claim. No network calls.
   The note claims only what it checks: the elements in the document, and the browser's Resource Timing
   log for this document. It cannot see a WebSocket, a connection that has not finished, or what a frame
   loads inside itself, so it never says "nothing else was contacted": it says what the log shows. */
const LOG_DEFAULT_SIZE = 250;   // Resource Timing keeps this many entries by default, then drops new ones
export function auditFirstPartyNote(note) {
  const hosts = new Set();
  const ownHost = location.hostname.toLowerCase();
  const label = location.host;
  let logState = "unavailable";   // "ok" | "full" | "unavailable"

  const add = raw => {
    if (!raw) return;
    try {
      const url = new URL(raw, document.baseURI);
      if (["http:", "https:", "ws:", "wss:"].includes(url.protocol) &&
          url.hostname.toLowerCase() !== ownHost) hosts.add(url.host);
    } catch (_) { /* A malformed attribute is not a browser request. */ }
  };
  const srcset = value => {
    // Each candidate starts after a comma. Data URLs are ignored by add().
    for (const candidate of value.split(/,\s*/)) add(candidate.trim().split(/\s+/)[0]);
  };
  const scanElements = () => {
    for (const el of document.querySelectorAll("[src], [srcset], [poster], object[data], link[href], image[href], use[href], a[ping], area[ping]")) {
      if (el.hasAttribute("src")) add(el.getAttribute("src"));
      if (el.hasAttribute("srcset")) srcset(el.getAttribute("srcset"));
      if (el.hasAttribute("poster")) add(el.getAttribute("poster"));
      if (el.localName === "object") add(el.getAttribute("data"));
      if (el.localName === "link" && /\b(?:stylesheet|icon|preload|modulepreload|prefetch|preconnect|dns-prefetch)\b/i.test(el.rel))
        add(el.getAttribute("href"));
      if (el.localName === "image" || el.localName === "use") add(el.getAttribute("href"));
      if (el.hasAttribute("ping")) for (const target of el.getAttribute("ping").split(/\s+/)) add(target);
    }
  };
  // Returns how many entries the browser's log holds, or null when it cannot be read.
  const scanLog = () => {
    try {
      if (typeof performance?.getEntriesByType !== "function") return null;
      const entries = performance.getEntriesByType("resource");
      for (const entry of entries) add(entry.name);
      return entries.length;
    } catch (_) { return null; }
  };
  const render = () => {
    try {
      scanElements();
      scanLog();
      const other = [...hosts].sort();
      const own = `This page's own code talks only to ${label}.`;
      const gap = logState === "full"
        ? "The browser's resource log for this page is full; other requests cannot be confirmed."
        : "Resource log unavailable; other requests cannot be confirmed.";
      // A host listed here was requested by something other than this page's code: the repository's
      // gate holds that code to its own site. Who added it (the network in front of the site, or the
      // browser itself) cannot be told from inside the page, so the note does not say.
      const message = other.length
        ? `${own} Also requested in this browser, not by that code: ${other.join(", ")}.` +
          (logState === "ok" ? "" : ` ${gap}`)
        : logState === "ok"
          ? `${own} The browser's resource log for this page shows no other host.`
          : `${own} ${gap}`;
      if (note.textContent !== message) note.textContent = message;
    } catch (_) {
      note.textContent = "This page's own code talks only to the site that served it. Resource check unavailable.";
    }
  };
  render();
  try {
    const observer = new MutationObserver(render);
    observer.observe(document.documentElement, { subtree: true, childList: true, attributes: true,
      attributeFilter: ["src", "srcset", "href", "rel", "poster", "data", "ping"] });
    if (typeof PerformanceObserver === "function" &&
        PerformanceObserver.supportedEntryTypes?.includes("resource")) {
      // A log that is already full has dropped entries nobody can recover: say so. From here on the
      // observer is handed every entry itself, whether or not the log has room to keep it.
      const held = scanLog();
      new PerformanceObserver(list => {
        for (const entry of list.getEntries()) add(entry.name);
        render();
      }).observe({ type: "resource", buffered: true });
      logState = held === null ? "unavailable" : held >= LOG_DEFAULT_SIZE ? "full" : "ok";
    }
    render();
    addEventListener("load", render);
  } catch (_) {
    note.textContent = `This page's own code talks only to ${label}. Resource check unavailable.`;
  }
}
