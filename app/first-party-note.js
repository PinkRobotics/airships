/* Report browser-visible loads beside the repository's first-party claim. No network calls. */
export function auditFirstPartyNote(note) {
  const hosts = new Set();
  const ownHost = location.hostname.toLowerCase();
  const label = location.host;
  let resourceLogAvailable = false;
  let resourceObserverAvailable = false;

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
    for (const el of document.querySelectorAll("[src], [srcset], [poster], object[data], link[href], image[href], use[href]")) {
      if (el.hasAttribute("src")) add(el.getAttribute("src"));
      if (el.hasAttribute("srcset")) srcset(el.getAttribute("srcset"));
      if (el.hasAttribute("poster")) add(el.getAttribute("poster"));
      if (el.localName === "object") add(el.getAttribute("data"));
      if (el.localName === "link" && /\b(?:stylesheet|icon|preload|modulepreload|prefetch|preconnect|dns-prefetch)\b/i.test(el.rel))
        add(el.getAttribute("href"));
      if (el.localName === "image" || el.localName === "use") add(el.getAttribute("href"));
    }
  };
  const scanResources = () => {
    try {
      if (typeof performance?.getEntriesByType !== "function") return;
      for (const entry of performance.getEntriesByType("resource")) add(entry.name);
      resourceLogAvailable = true;
    } catch (_) { resourceLogAvailable = false; }
  };
  const render = () => {
    try {
      scanElements();
      scanResources();
      const other = [...hosts].sort();
      const message = other.length
        ? `This page's own code talks only to ${label}. Added by the network in front of it: ${other.join(", ")}.` +
          (resourceLogAvailable && resourceObserverAvailable ? "" : " Resource log unavailable; other requests cannot be confirmed.")
        : resourceLogAvailable && resourceObserverAvailable
          ? `This page talks only to ${label}.`
          : `This page's own code talks only to ${label}. Resource log unavailable; other requests cannot be confirmed.`;
      if (note.textContent !== message) note.textContent = message;
    } catch (_) {
      note.textContent = "This page's own code talks only to the site that served it. Resource check unavailable.";
    }
  };
  render();
  try {
    const observer = new MutationObserver(render);
    observer.observe(document.documentElement, { subtree: true, childList: true, attributes: true,
      attributeFilter: ["src", "srcset", "href", "rel", "poster", "data"] });
    if (typeof PerformanceObserver === "function" &&
        PerformanceObserver.supportedEntryTypes?.includes("resource")) {
      new PerformanceObserver(render).observe({ type: "resource", buffered: true });
      resourceObserverAvailable = true;
      render();
    } else {
      render();
    }
    addEventListener("load", render);
  } catch (_) {
    note.textContent = `This page's own code talks only to ${label}. Resource check unavailable.`;
  }
}
