/* A test harness small enough to read in one sitting.
 *
 * The constraint that shapes it: this machine has no node, and CI has no browser. So the
 * assertions are written once as plain ES modules and executed by two runners
 * (tests/browser/index.html and tests/node/run.mjs). To make that possible the harness
 * COLLECTS test definitions at import time and runs them later, on demand, returning a
 * record rather than printing anything. Whoever calls it decides what output means.
 *
 * No dependencies, no globals, no timers, no async. A test is a synchronous function that
 * throws to fail.
 */

const suites = [];
let open = null;

/** Group tests. Nesting is allowed; names are joined with " › ". */
export function describe(name, body) {
  const parent = open;
  open = { name: parent ? `${parent.name} › ${name}` : name, tests: [] };
  suites.push(open);
  try { body(); } finally { open = parent; }
}

/** One test. `body` throws to fail. */
export function it(name, body) {
  if (!open) { describe("(ungrouped)", () => it(name, body)); return; }
  open.tests.push({ name, body, known: null });
}

/**
 * A test that is expected to FAIL because of a defect that is known and tracked.
 *
 * It still runs. Failing counts as "known"; PASSING counts as a hard failure, because a
 * defect that has quietly been fixed must not keep a permanent excuse in the suite. This
 * is how the three open physics defects are recorded here rather than in a comment.
 */
export function knownFail(name, reason, body) {
  if (!open) { describe("(ungrouped)", () => knownFail(name, reason, body)); return; }
  open.tests.push({ name, body, known: reason });
}

export function collect() { return suites; }
export function reset() { suites.length = 0; open = null; }

/* ---------- assertions ------------------------------------------------------------------- */

export class AssertionError extends Error {
  constructor(msg) { super(msg); this.name = "AssertionError"; }
}

function show(v) {
  if (typeof v === "number" || typeof v === "bigint") return String(v);
  if (typeof v === "string") return JSON.stringify(v);
  if (v === null || v === undefined || typeof v === "boolean") return String(v);
  try { return JSON.stringify(v); } catch { return String(v); }
}

function fail(msg) { throw new AssertionError(msg); }

export function ok(v, msg) {
  if (!v) fail(`${msg || "expected truthy"} — got ${show(v)}`);
}

export function eq(a, b, msg) {
  if (!Object.is(a, b)) fail(`${msg || "eq"}: ${show(a)} !== ${show(b)}`);
}

/** Absolute tolerance. State the tolerance you mean; there is no default. */
export function close(a, b, tol, msg) {
  if (typeof a !== "number" || !isFinite(a)) fail(`${msg || "close"}: ${show(a)} is not a finite number`);
  if (!(Math.abs(a - b) <= tol)) fail(`${msg || "close"}: ${a} !== ${b} within ${tol} (off by ${Math.abs(a - b)})`);
}

export function throws(body, msg) {
  let threw = false;
  try { body(); } catch { threw = true; }
  if (!threw) fail(`${msg || "throws"}: expected the call to throw, it returned`);
}

export function deepEq(a, b, msg) {
  const bad = firstDiff(a, b, "");
  if (bad) fail(`${msg || "deepEq"}: ${bad}`);
}

function firstDiff(a, b, path) {
  if (Object.is(a, b)) return null;
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b)) return `${path}: ${show(a)} vs ${show(b)}`;
    if (a.length !== b.length) return `${path}: length ${a.length} vs ${b.length}`;
    for (let i = 0; i < a.length; i++) { const d = firstDiff(a[i], b[i], `${path}[${i}]`); if (d) return d; }
    return null;
  }
  if (a && b && typeof a === "object" && typeof b === "object") {
    const ka = Object.keys(a).sort(), kb = Object.keys(b).sort();
    if (ka.join() !== kb.join()) return `${path}: keys ${show(ka)} vs ${show(kb)}`;
    for (const k of ka) { const d = firstDiff(a[k], b[k], `${path}.${k}`); if (d) return d; }
    return null;
  }
  return `${path || "value"}: ${show(a)} vs ${show(b)}`;
}

/* ---------- running -------------------------------------------------------------------- */

const clock = () => (typeof performance !== "undefined" ? performance.now() : Date.now());

/** Run one collected test. Never throws: the outcome is the return value. */
export function runTest(t) {
  const t0 = clock();
  let thrown = null;
  try { t.body(); } catch (e) { thrown = e; }
  const ms = clock() - t0;
  const msg = thrown ? String((thrown && thrown.message) || thrown) : "";
  if (t.known) {
    return thrown
      ? { name: t.name, status: "known", ms, known: t.known, error: msg }
      : { name: t.name, status: "fail", ms, known: t.known,
          error: `expected-failure test PASSED — the known defect (${t.known}) looks fixed; drop the knownFail marker and assert the corrected behaviour` };
  }
  return thrown
    ? { name: t.name, status: "fail", ms, error: msg, stack: thrown && thrown.stack }
    : { name: t.name, status: "pass", ms };
}

/** Run everything collected so far and return a record. Prints nothing. */
export function runAll() {
  const t0 = clock();
  const out = { suites: [], pass: 0, fail: 0, known: 0, total: 0, ms: 0 };
  for (const s of suites) {
    const rs = { name: s.name, tests: [] };
    for (const t of s.tests) {
      const r = runTest(t);
      rs.tests.push(r);
      out.total++;
      out[r.status === "pass" ? "pass" : r.status === "known" ? "known" : "fail"]++;
    }
    out.suites.push(rs);
  }
  out.ms = clock() - t0;
  return out;
}
