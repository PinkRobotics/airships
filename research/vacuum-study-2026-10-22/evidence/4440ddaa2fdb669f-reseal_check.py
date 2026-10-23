"""XO check of A's actual clock-only re-seal (card 3e2b7eff, granted by ord-co27-sci-h1-stvk-clock-card-granted-1019).
Reads and hashes only; never imports or runs pack code; writes only under this folder.
Originals were snapshotted into orig/ at 02:58 PDT Oct 19, before A's unit started.
usage: python3 -I reseal_check.py <A's request .json in queue/submissions> [more submission .json ...]"""
import json, hashlib, datetime, os, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
O = HERE / "orig"
R = Path("unpublished-local-ref:c80d18a1e93a6262")
CLOCK, SEAL, OPS = str(R / "intake-clock.json"), str(R / "PACK-SEAL.json"), str(R / "offline-phase-start.json")
EXP = {"PACK-SEAL.json": ("70e66d6fe4e495d5a57a0dc1d6da171358462bcd06b6f72e39b9ad08fbc65bb1", 15327),
       "offline-phase-start.json": ("27e2b6bce996cc48158f9f9d3ab3a2b463e1e747633bec1e9b97f7af0ed7a24b", 281),
       "H1-STVK-CLOCK-ONLY-53-MEMBER-BASELINE-1019.json": ("0d0a9dbe", None)}
def sha(p):
    b = Path(p).read_bytes(); return hashlib.sha256(b).hexdigest(), len(b)
def iso(t): return datetime.datetime.fromtimestamp(t).astimezone().isoformat(timespec="seconds")
res = {"checks": [], "defects": [], "notes": []}
def check(name, ok, detail=""):
    res["checks"].append([name, bool(ok), str(detail)[:400]]); print(f"  [{'OK' if ok else 'DEFECT'}] {name}: {detail}")
    if not ok: res["defects"].append(f"{name}: {detail}")
mono_now, wall_now = time.monotonic(), time.time()
print("==", iso(wall_now), f"monotonic {mono_now:.3f}", "XO re-seal check")

print("\n[0] my snapshot of the originals")
o_seal = json.loads((O / "PACK-SEAL.json").read_text()); o_clock = json.loads((O / "intake-clock.json").read_text())
base = json.loads((O / "H1-STVK-CLOCK-ONLY-53-MEMBER-BASELINE-1019.json").read_text())
check("snapshot seal = 70e66d6f", sha(O / "PACK-SEAL.json") == EXP["PACK-SEAL.json"])
check("snapshot offline-phase-start = 27e2b6bc/281", sha(O / "offline-phase-start.json") == EXP["offline-phase-start.json"])
check("snapshot baseline = 0d0a9dbe", sha(O / "H1-STVK-CLOCK-ONLY-53-MEMBER-BASELINE-1019.json")[0].startswith("0d0a9dbe"))
o_st = {r["path"]: (r["sha256"], r["bytes"]) for r in o_seal["files"]}
bl = {r["path"]: (r["sha256"], r["bytes"]) for r in base["other_members_required_byte_identical"]}
check("baseline = original seal minus the clock", bl == {k: v for k, v in o_st.items() if k != CLOCK}, f"{len(bl)} members")

print("\n[1] the request(s) and their pins")
reqs = [json.loads(Path(p).read_text()) for p in sys.argv[1:]]
arts = []
for q in reqs:
    print(f"  {q.get('id')} from {q.get('from_seat') or q.get('from')} at {q.get('at')} ingested {q.get('ingested')} to {q.get('to')} cc {q.get('cc')}")
    for a in q.get("artifacts", []):
        arts.append(a)
        try: got = sha(a["path"])
        except OSError as e: got = (f"MISSING {e.__class__.__name__}", None)
        check(f"pin {Path(a['path']).name}", got[0] == a.get("sha256") and (a.get("bytes") is None or got[1] == a.get("bytes")),
              f"{a.get('sha256','')[:12]} {a.get('bytes')} -> {str(got[0])[:12]} {got[1]}")

print("\n[2] the new seal at the fixed root")
n_seal_sha = sha(SEAL); n_seal = json.loads(Path(SEAL).read_text())
check("new seal differs from 70e66d6f", n_seal_sha[0] != EXP["PACK-SEAL.json"][0], f"{n_seal_sha[0][:12]} {n_seal_sha[1]} B")
pinned = [a for a in arts if a["path"] == SEAL]
check("new seal is pinned by the request", bool(pinned) and pinned[-1]["sha256"] == n_seal_sha[0], pinned[-1]["sha256"][:12] if pinned else "not pinned")
n_st = {r["path"]: (r["sha256"], r["bytes"]) for r in n_seal["files"]}
check("same 54 paths as the original seal", set(n_st) == set(o_st), f"new {len(n_st)}, orig {len(o_st)}, +{sorted(set(n_st)-set(o_st))[:3]} -{sorted(set(o_st)-set(n_st))[:3]}")
check("entry keys unchanged", all(list(r) == list(o_seal["files"][0]) for r in n_seal["files"]))
same53 = {k: v for k, v in n_st.items() if k != CLOCK} == bl
diff53 = [k for k in bl if n_st.get(k) != bl[k]]
check("53 non-clock tuples = baseline 0d0a9dbe = original seal", same53, f"mismatches {len(diff53)} {diff53[:3]}")
check("clock tuple changed", n_st.get(CLOCK) != o_st[CLOCK], f"{o_st[CLOCK][0][:12]} -> {n_st.get(CLOCK, ('?',))[0][:12]}")
cur = [p for p, t in n_st.items() if sha(p) != t]
check("all 54 new-seal tuples re-hash against current bytes", not cur, f"mismatches {len(cur)} {cur[:3]}")
meta_o = {k: v for k, v in o_seal.items() if k != "files"}; meta_n = {k: v for k, v in n_seal.items() if k != "files"}
changed = {k: (meta_o.get(k), meta_n.get(k)) for k in set(meta_o) | set(meta_n) if meta_o.get(k) != meta_n.get(k)}
fixed = {"schema", "unit", "no_test_or_native_response_seen", "immutable_implementation", "derived_reference_policy"}
check("seal policy fields unchanged", not (set(changed) & fixed), f"changed fields: {sorted(changed)}")
for k, (a, b) in sorted(changed.items()): print(f"    {k}: {str(a)[:120]} -> {str(b)[:120]}")
res["seal_meta_changed"] = {k: [str(a)[:200], str(b)[:200]] for k, (a, b) in changed.items()}

print("\n[3] the new clock")
n_clock = json.loads(Path(CLOCK).read_text()); print("   ", json.dumps(n_clock)[:600])
origin = n_clock.get("captured_monotonic")
extra = sorted(set(n_clock) - set(o_clock)); missing = sorted(set(o_clock) - set(n_clock))
check("clock keeps every original key", not missing, f"missing {missing}")
if extra: res["notes"].append(f"new clock adds {extra}; run_pack.py:59-61 reads only captured_monotonic"); print(f"  [NOTE] new clock adds {extra}; run_pack.py lines 59-61 read only captured_monotonic")
check("new origin later than the old (2014112.830277349)", isinstance(origin, (int, float)) and origin > o_clock["captured_monotonic"], origin)
if isinstance(origin, (int, float)):
    el = mono_now - origin
    check("origin in the past and inside the 7165 s whole", 0 < el < 7165, f"elapsed now {el:.3f} s")
    o_off = datetime.datetime.fromisoformat(o_clock["captured_utc"]).timestamp() - o_clock["captured_monotonic"]
    try:
        n_off = datetime.datetime.fromisoformat(n_clock["captured_utc"]).timestamp() - origin
        check("wall/monotonic pairing agrees with the old clock's and with now", abs(n_off - o_off) < 0.5 and abs((wall_now - mono_now) - n_off) < 0.5,
              f"offsets old {o_off:.6f}, new {n_off:.6f}, now {wall_now - mono_now:.6f}")
        res["origin_wall"] = iso(datetime.datetime.fromisoformat(n_clock["captured_utc"]).timestamp())
    except Exception as e:
        check("captured_utc parses", False, repr(e))
    res["elapsed_at_check"] = round(el, 3); res["origin_monotonic"] = origin
    for q in reqs:
        try:
            qa = datetime.datetime.fromisoformat(q["at"]).timestamp() - n_off
            print(f"    request {q.get('id')} authored at origin+{qa - origin:.1f} s (stage 1 cap 690 s)")
            if q.get("ingested"):
                qi = datetime.datetime.fromisoformat(q["ingested"]).timestamp() - n_off
                print(f"    ingested at origin+{qi - origin:.1f} s; review stage cap ends by origin+{qa - origin + 900:.1f} s from authoring, latest origin+1590")
                res["stage1_end_s"] = round(qa - origin, 1); res["ingested_s"] = round(qi - origin, 1)
        except Exception as e:
            print("    request timing:", repr(e))

print("\n[4] the archive")
inv = None
for a in arts:
    try: j = json.loads(Path(a["path"]).read_text())
    except Exception: continue
    def find(o):
        if isinstance(o, list) and o and all(isinstance(x, dict) for x in o) and any(any("archiv" in k.lower() for k in x) for x in o): return o
        if isinstance(o, dict):
            for v in o.values():
                r = find(v)
                if r: return r
        return None
    f = find(j)
    if f: inv = (a["path"], f, j); break
check("an archive inventory is pinned", inv is not None, inv[0] if inv else "none found among the pinned JSON")
if inv:
    rows = inv[1]; print(f"    {len(rows)} rows; keys {sorted(rows[0])}")
    def get(r, *subs):
        for k, v in r.items():
            if all(s in k.lower() for s in subs): return v
    want = {CLOCK: o_st[CLOCK], SEAL: EXP["PACK-SEAL.json"], OPS: EXP["offline-phase-start.json"]}
    seen = {}
    for r in rows:
        op = get(r, "orig", "path") or get(r, "source") or get(r, "active") or get(r, "path")
        ap = get(r, "archiv", "path") or get(r, "archiv")
        seen[str(op)] = r
        print(f"    {Path(str(op)).name} -> {ap}")
        if ap and Path(str(ap)).exists():
            got = sha(ap); osha = get(r, "orig", "sha") or get(r, "sha")
            check(f"archived copy of {Path(str(op)).name} re-hashes to its original", got[0] in json.dumps(r) and (str(op) not in want or got == want[str(op)]),
                  f"{got[0][:12]} {got[1]} B; symlink {Path(str(ap)).is_symlink()}")
        else:
            check(f"archived copy of {Path(str(op)).name} exists", False, ap)
    for p, t in want.items():
        check(f"inventory names {Path(p).name} ({t[0][:8]}, {t[1]} B)", p in seen, "")
    parents = {str(Path(str(get(r, 'archiv', 'path') or get(r, 'archiv'))).parent) for r in rows}
    print(f"    archive parent(s): {sorted(parents)}")
    check("archive outside the active root's sealed paths", all(not any(par == str(Path(p).parent) for p in o_st) for par in parents), sorted(parents))

print("\n[5] the rest of the root")
check("offline-phase-start.json still the original (no phase begun)", sha(OPS) == EXP["offline-phase-start.json"], sha(OPS)[0][:12])
man = json.loads((O / "FINAL-EVIDENCE-MANIFEST.json").read_text())
mt = {r["path"]: (r["sha256"], r["bytes"]) for r in man["files"]}
moved = []
for p, t in mt.items():
    try: g = sha(p)
    except OSError: g = ("MISSING", None)
    if g != t: moved.append(Path(p).name)
check("old manifest members changed only where expected (clock, seal)", set(moved) <= {"intake-clock.json", "PACK-SEAL.json"}, f"changed: {sorted(moved)}")
top = sorted(os.listdir(R)); known = {Path(p).relative_to(R).parts[0] for p in mt} | {"FINAL-EVIDENCE-MANIFEST.json", "final-budget.json"}
new_top = [n for n in top if n not in known]
print(f"    root now {len(top)} top-level entries; not in the old manifest: {new_top}")
res["root_new_entries"] = new_top
rt = json.loads((R / "runtime-premises.json").read_text()); bad = [r["path"] for r in rt["files"] if sha(r["path"]) != (r["sha256"], r["bytes"])]
check("33 runtime pins re-hash", not bad and len(rt["files"]) == 33, f"{len(rt['files'])} files, mismatches {bad[:3]}")

res["verdict"] = "VERIFIED" if not res["defects"] else "DEFECTS"
res["new_seal"] = {"sha256": n_seal_sha[0], "bytes": n_seal_sha[1]}; res["new_clock"] = dict(zip(("sha256", "bytes"), sha(CLOCK)))
res["checked_at"] = iso(wall_now)
(HERE / "reseal-summary.json").write_text(json.dumps(res, indent=1) + "\n")
print(f"\n== {res['verdict']}: {sum(c[1] for c in res['checks'])}/{len(res['checks'])} checks OK; defects {len(res['defects'])}; took {time.monotonic() - mono_now:.1f} s")
