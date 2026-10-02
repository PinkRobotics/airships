# Browser origin boundary

`make firstparty` runs the static loading-URL scanner, fixture unit tests and DevTools
network recording. It is also a prerequisite of `make check`.

The served file set comes from `dist.manifest`, including its `PARTIAL` exclusions.
Every served HTML page is opened with a fixture mirror, `?data=snapshot`, and an absent
mirror. The monitor must actually finish booting and name the expected tier. Fresh wind
must apply; stale and missing wind must clear it and state still air. Pages are scrolled
to trigger lazy images. Uncaught script errors and external request attempts fail.

`python3 tests/firstparty/check.py --evidence path/to/network.json` saves the request
events and a monitor screenshot beside them. The fixture server never reads a real mirror
and never fetches agency data. An external-image control must be detected; interception
blocks it before transmission. DNS is also confined to loopback in this test browser.
The control is separate from the page request counts. All requests, including redirects
and failed requests, are counted from `Network.requestWillBeSent` (WebSockets separately).

The static scanner covers `src`, `srcset`, stylesheet/preload/icon links, CSS `url()` and
`@import`, module imports, literal `fetch()` and resource URL assignments. Its explicit
non-loading allow-list is `a[href]`, `area[href]` and `link[rel=canonical][href]`.
It is a fast check for literal loads, not a JavaScript interpreter; the browser test covers
computed URLs along the exercised paths. It does not promise to exercise every possible
interaction or future worker script.

The recorded weather fixture has a provenance sidecar. Tests replace its dates only in
the fixture server; it is never presented as an actual current forecast.
