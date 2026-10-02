/* Stamp a content-derived version onto every module URL.
 *
 *   node scripts/stamp-version.mjs            # stamp
 *   node scripts/stamp-version.mjs --check    # fail if the stamp is stale
 *   node scripts/stamp-version.mjs --strip    # remove the stamps
 *
 * WHY THIS EXISTS. The deployed site sits behind Cloudflare, which caches .js for four hours. A no-build
 * ES-module site cannot cache-bust from the entry point, because a relative specifier resolves
 * against the importing module's URL with the query string DROPPED — so `index.js?v=2` still
 * pulls a stale `model/build.js`. Requesting revalidation does not help either: Cloudflare answers
 * `cf-cache-status: HIT` to `Cache-Control: no-cache`.
 *
 * The result, observed rather than theorised: a deploy landed correctly on the origin and the
 * browser kept running the previous build for hours, across every browser, because the staleness
 * was at the edge and not in any client.
 *
 * So every relative specifier in the tree carries the SAME version query. Changing the version
 * changes every URL at once, and the whole graph misses the cache together. Uniformity is the
 * safety property: a partly-stamped tree would load some modules under two URLs and give you two
 * copies of module state (two `ASSUMPTIONS` objects, two style-injection guards), which is a far
 * nastier bug than a stale file. `--check` exists to keep that from drifting.
 *
 * The version is a hash of the module contents, so it changes exactly when the code does and a
 * rebuild with no changes re-stamps to the same value.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, relative, resolve, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const SITE = join(ROOT, '..');

const args = process.argv.slice(2);
const check = args.includes('--check');
const strip = args.includes('--strip');

/** Every .js in the module tree, plus the HTML entry points that import from it. */
function walkFiles(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === '.browser-scratch' || name === 'node_modules' || name === 'assets' || name === '.git') continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) walkFiles(p, out);
    else if (name.endsWith('.js') || name.endsWith('.mjs')) out.push(p);
  }
  return out;
}

const modules = walkFiles(ROOT).filter((p) => !p.includes(`${'scripts'}/`));
/**
 * HTML entry points are DISCOVERED, not listed.
 *
 * A hardcoded list is how tests/hud-demo.html shipped with an unstamped import: it fetched the
 * un-versioned module URL, was served a cached build from before the export it needed existed,
 * and the page died with "does not provide an export named AirshipHUD". Uniformity is the whole
 * safety property here, so the set of files it covers cannot be something a person must remember
 * to update.
 *
 * It was still half-listed, and the listed half was wrong: `walkHtml(ROOT)` plus a former
 * deployment path for the lab. Here the lab is at `model-lab/index.html`, so nothing was at
 * the listed path. The lab was never stamped, and `--check` exited 0 while it imported
 * `?v=41bc1f51` against a
 * tree that hashed to `f3cb948e`. Discovery is now by RESOLVING each specifier: every HTML page
 * in the repository whose imports land inside this tree is an entry point, wherever it moves.
 */
function walkHtml(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === '.browser-scratch' || name === 'node_modules' || name === 'assets' || name === '.git') continue;
    const q = join(dir, name);
    let st;
    try { st = statSync(q); } catch { continue; }
    if (st.isDirectory()) walkHtml(q, out);
    else if (name.endsWith('.html')) out.push(q);
  }
  return out;
}

/**
 * Add the query to relative specifiers only. Bare specifiers and absolute URLs are left alone —
 * there are none today, and silently rewriting one later would be worse than skipping it.
 *
 * Declared here rather than beside `stampSource` because entry-point discovery reads it too:
 * a page is an entry point exactly when one of these specifiers resolves into the tree.
 */
const SPEC = /(from\s*|import\s*\(\s*)(['"])(\.{1,2}\/[^'"?]+\.m?js)(?:\?[^'"]*)?(['"])/g;

/**
 * Does this relative specifier, resolved from `page`, land inside the module tree?
 *
 * Only those get stamped. A page may import this tree and someone else's modules in the same
 * block — `model-lab/` may import `sim/` — and rewriting the other owner's URLs would version
 * files they have deliberately left unversioned.
 */
function targetsTree(page, spec) {
  const target = resolve(dirname(page), spec);
  const rel = relative(ROOT, target);
  return rel === '' || (!rel.startsWith('..') && !isAbsolute(rel));
}
const importsTree = (page) => {
  const src = readFileSync(page, 'utf8');
  for (const m of src.matchAll(SPEC)) if (targetsTree(page, m[3])) return true;
  return false;
};
const htmlEntries = walkHtml(SITE).filter(importsTree);

/**
 * JS entry points OUTSIDE the tree that import into it — cell/explorer.js was the first.
 * Without this, a module in another owner's tree holds unversioned ../3d/ specifiers, and a
 * CDN serves it a stale graph for exactly as long as its cache pleases: the renderer fix of
 * 2026-08-11 would have been invisible behind Cloudflare. Discovery is by resolving
 * specifiers, same as the HTML entries and for the same reason.
 */
function walkJs(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === '.browser-scratch' || name === 'node_modules' || name === 'assets' || name === '.git') continue;
    const q = join(dir, name);
    let st;
    try { st = statSync(q); } catch { continue; }
    if (st.isDirectory()) walkJs(q, out);
    else if ((name.endsWith('.js') || name.endsWith('.mjs'))) out.push(q);
  }
  return out;
}
const insideTree = (p) => {
  const rel = relative(ROOT, p);
  return rel === '' || (!rel.startsWith('..') && !isAbsolute(rel));
};
const jsEntries = walkJs(SITE).filter((p) => !insideTree(p) && importsTree(p));

/* The version: a hash of the STRIPPED contents, so stamping is idempotent.
 *
 * The token pattern is deliberately PERMISSIVE. It used to require exactly eight hex characters,
 * which meant a hand-written label like `?v=0808fix3` could neither be stripped nor re-stamped:
 * the whole tree was pinned to a literal that no longer tracked content, `--check` reported it as
 * clean, and cache-busting was silently disabled for every future change. A checker that only
 * recognises its own output cannot tell you when someone else has edited the thing it guards. */
const STAMP = /(\.m?js)\?v=[A-Za-z0-9_.-]+(['"])/g;
const stripStamp = (s) => s.replace(STAMP, '$1$2');

const h = createHash('sha256');
for (const p of modules.slice().sort()) h.update(stripStamp(readFileSync(p, 'utf8')));
const VERSION = h.digest('hex').slice(0, 8);

/* One pass does both jobs: SPEC's third group excludes any existing query, so re-emitting the
 * match without one IS the strip. Only the tree's own URLs are touched — see targetsTree. */
function stampSource(page, src) {
  return src.replace(SPEC, (whole, kw, q1, spec, q2) =>
    (targetsTree(page, spec) ? `${kw}${q1}${spec}${strip ? '' : `?v=${VERSION}`}${q2}` : whole));
}

let changed = 0, stale = [];
for (const p of [...modules, ...htmlEntries, ...jsEntries]) {
  const src = readFileSync(p, 'utf8');
  const out = stampSource(p, src);
  if (out === src) continue;
  changed++;
  if (check) stale.push(relative(SITE, p));
  else writeFileSync(p, out);
}

/* Pages elsewhere on the site that import this tree are REPORTED, never edited — they belong to
 * a separate module tree. An unstamped import there is a stale-cache failure waiting to happen. */
{
  const foreign = [];
  const scan = (dir) => {
    for (const name of readdirSync(dir)) {
      if (name === '.browser-scratch' || name === 'node_modules' || name === 'assets' || name === '3d') continue;
      const q = join(dir, name);
      let st;
      try { st = statSync(q); } catch { continue; }
      if (st.isDirectory()) scan(q);
      else if (name.endsWith('.html') && !htmlEntries.includes(q)) {
        if (/3d\/index\.js(?!\?v=)/.test(readFileSync(q, 'utf8'))) {
          foreign.push(relative(SITE, q));
        }
      }
    }
  };
  try { scan(SITE); } catch { /* nothing to scan */ }
  if (foreign.length) {
    console.warn('stamp: NOTE — these pages import airship3d without a version query, so they ' +
      `can be served a stale module graph:\n  ${foreign.join('\n  ')}\n  Not edited (not this ` +
      `module's files). Add ?v=${VERSION} to their import, or ask their owner to.`);
  }
}

/* Publish the version so a host that imports this module DYNAMICALLY can pin it.
 *
 * A static import inside the tree gets stamped by this script. A dynamic `import("…/index.js")`
 * from someone else's page cannot be — it is their file — so that page rides the un-versioned URL
 * and gets whatever generation the CDN happens to hold. This file is how they pin it without
 * hand-editing a literal on every change:
 *
 *     const { version } = await (await fetch('/3d/version.json')).json();
 *     const mod = await import(`/3d/index.js?v=${version}`);
 */
if (!check && !strip) {
  writeFileSync(join(ROOT, 'version.json'),
    `${JSON.stringify({ version: VERSION, note: 'Pin dynamic imports to this. See scripts/stamp-version.mjs.' }, null, 2)}\n`);
}

if (check) {
  if (stale.length) {
    console.error(`stamp: ${stale.length} file(s) are not stamped at ${VERSION} ` +
      '(a foreign or hand-written version query counts as stale — it freezes cache-busting):');
    for (const f of stale.slice(0, 12)) console.error(`  ${f}`);
    console.error('\nRun `node scripts/stamp-version.mjs` and redeploy.');
    process.exit(1);
  }
  console.log(`stamp: all module URLs carry ?v=${VERSION}`);
} else {
  console.log(strip
    ? `stamp: removed version queries from ${changed} file(s)`
    : `stamp: ${changed} file(s) stamped at ?v=${VERSION}`);
}
