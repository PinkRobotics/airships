---
name: Bug
about: Something is broken, blank, slow, or does not match what the page says it does
title: ''
labels: bug
---

<!--
For a number you believe is wrong, use the "Physics objection" template instead — it asks
for the things that make an arithmetic disagreement settleable. This one is for the page
misbehaving.
-->

## What happened

## What you expected instead

## The URL, including the determinism parameters

    https://…/index.html?seed=7&data=snapshot

Please reproduce it with both parameters set and paste the URL you actually used, seed
included. `?seed=N` pins every random choice the model makes and `?data=snapshot` pins the
input data to the copy in `data/`. Without them the fleet is doing something different for
every visitor and the report cannot be replayed.

**Does it still happen with `?data=snapshot`?**

- [ ] Yes — then it is in our code, and this is enough to start on
- [ ] No, only on live data — then it is a feed problem, or our handling of one; say roughly
      when you saw it, because the wildfire feeds change every few minutes and we may need
      to catch it in the same state

## Browser and platform

Name and full version, and the operating system. WebGL is involved in the map and the
cockpit view, so "Firefox on an old Intel Mac" is a genuinely different situation from
"Chrome on Windows".

## Console output

Open devtools and paste everything from the console, including warnings. A module that
failed to load leaves a 404 there and nothing at all on the page, which is otherwise
indistinguishable from a rendering bug.

## Screenshot

If it is visual, a screenshot saves several rounds of description.
