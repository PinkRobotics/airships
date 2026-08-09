# Security

## What this is

A static site. There are no accounts, no logins, no sessions, no cookies, no database, no
server-side code behind the pages, no secrets in the repository and no user input that reaches
anything but the reader's own browser. The pages are HTML importing ES modules directly; there is
no build step, no bundler and no package manager, so there is no dependency tree to compromise.
The only state the site keeps is in the reader's `localStorage`: a feed cache, a split-pane
preference and a flag saying the intro overlay has been dismissed.

That removes most of the usual attack surface. It does not remove all of it, and the parts that
remain are listed here so that a report has somewhere to aim.

## What is worth reporting

**The data pipeline.** `pipeline/live.py` is the one piece that runs on a server rather than in a
browser. It fetches the public wildfire feeds on a timer and writes `data/live/*.json`, which every
visitor then reads. Anything that lets an attacker influence what that script writes, or that turns
an upstream feed's content into code or markup on the page, matters. So do path handling,
unvalidated upstream responses, and any way the mirror could be made to serve something other than
mirrored data. `pipeline/water.py` and `pipeline/terrain.py` are run by hand and commit their output,
so a problem there is a supply-chain problem in the committed data rather than a live one.

**The mirror and the feed chain.** The page tries three tiers in order: our mirror at `data/live/`,
then the upstream feeds directly, then the dated snapshot committed to the repository. The upstream
origins the browser can be made to contact are `services6.arcgis.com` (BC Wildfire Service),
`cwfis.cfs.nrcan.gc.ca` (CWFIS hotspots), `api.open-meteo.com` (winds) and
`server.arcgisonline.com` (satellite tiles). A way to make the page contact something else, or to
make an untrusted response drive rendering, is in scope. So is anything that would cause the page to
hammer an emergency service's feed: the mirror exists specifically so that traffic to this site does
not multiply load on emergency infrastructure, and a defect that defeats that is a real defect even
though it harms someone else's servers rather than ours.

**Data that becomes markup.** Fire names, geographic descriptions and source names come from
third-party feeds and are rendered into the page. They are escaped through `esc()` in `app/dom.js`.
A path that reaches `innerHTML` without it is worth reporting even if the current upstream data
happens to be benign — the point is that we do not control that data.

**The dependency-free supply chain.** There is no npm, but there is still a chain: the committed
data files under `data/`, the raster and geometry assets under `3d/assets/`, the GitHub Actions
workflows, and whatever runs the deploy. Tampering that would survive review, or a workflow that can
be made to run attacker-controlled code, is in scope.

**Anything that misrepresents the wildfire data.** This is not a conventional security issue, but it
is the one we care most about. The fire data is real, live and about an emergency. A defect that
makes the page display stale data as current, attribute the wrong status to a fire, or otherwise
create a false impression of a real incident should be reported with the same urgency as a
vulnerability, and will be treated that way.

## What is not a finding

The simulated aircraft are imaginary and the model is known to be wrong in the ways the
[README](README.md) lists. A defect in the physics is a bug, not a vulnerability — send it as an
issue or a pull request, and see [CONTRIBUTING.md](CONTRIBUTING.md) for what makes one easy to act
on.

## Where to send it

**tyler@pinkai.ca.** Plain email is fine. Include what you did, what happened, and what you expected
instead; a proof of concept is welcome but not required to get a reply.

There is no bug bounty and nothing to claim. Expect an acknowledgement within a few days. If a
report is valid we will say what we are doing about it and when, and we will credit you by whatever
name you ask for unless you would rather not be named. Please give us a reasonable window to fix
something before publishing it — but this is a static site about imaginary aircraft, so we are not
going to argue about disclosure timelines.
