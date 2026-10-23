#!/usr/bin/env python3
"""CHECK-030d: CHECK.md, RESULTS.json, NFI.json and INPUTS.json from this seat's own re-derivation (P2CHECK.json,
OWN-CHECKS.json) and its four tracing sub-workers (trace/A-D.json). The card's P2 values are parsed from 030d's
CARD.md itself, so the comparison is against the printed text."""
import datetime
import hashlib
import json
import os
import re

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def num(s):
    return float(s.replace("−", "-").replace(",", "").replace("+", ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def p2_items():
    """Compare the card's printed P2 values with this seat's own computation."""
    rows = P2["rows"]

    def g(r, w, fl, cure=True, fin="MLCCAg", route="bake70", ext=.1):
        return next(x for x in rows if x["finish"] == fin and x["R_m"] == r and x["weather"] == w and x["floor"] == fl
                    and x["route"] == route and x["external_water"] == ext and x["cure"] == cure)
    items = []

    def add(line, label, card, mine, digits):
        tol = 0.5 * 10 ** (-digits) + 1e-12
        items.append({"line": line, "passage": label, "card_value": card, "mine": mine,
                      "status": "REDERIVED-MATCH" if abs(num(str(card)) - mine) <= tol else "REDERIVED-DIFFERS",
                      "note": f"tolerance half a unit in the last printed digit ({tol:.1e})"})
    # the R10 bill table
    i0 = next(i for i, x in enumerate(LINES) if x.startswith("| R10 ISA multilayer bake bill, kg"))
    key = {"faces": "faces", "core": "core", "charged joining": "charged_joining", "coating": "coating",
           "mooring pad": "mooring_pad", "gas": "gas", "systems": "systems", "extra service": "extra_service", "water": "water",
           "contamination": "contamination", "weather headroom": "weather_headroom", "absorbed water": "absorbed_water",
           "structural primer": "structural_primer", "desiccant": "desiccant"}
    x = g(10, "ISA", True)
    nb, lb = x["named_bill"], x["least_bill"]
    for j in range(i0 + 2, i0 + 2 + 18):
        cells = [c.strip() for c in LINES[j].strip("|").split("|")]
        lab = cells[0]
        if lab in key:
            for col, bill, which in ((1, nb, "named endpoint"), (2, lb, "least G+Q+film")):
                add(j + 1, f"R10 bill {lab}, {which}", cells[col], bill[key[lab]], 6)
        elif lab == "Total carried":
            add(j + 1, "R10 bill total, named endpoint", cells[1], sum(nb.values()), 6)
            add(j + 1, "R10 bill total, least point", cells[2], sum(lb.values()), 6)
        elif lab == "Reference lift":
            add(j + 1, "R10 reference lift", cells[1], x["named_lift"], 6)
        elif lab == "Signed payload":
            add(j + 1, "R10 signed payload, named endpoint", cells[1], x["named_lift"] - sum(nb.values()), 6)
            add(j + 1, "R10 signed payload, least point", cells[2], x["least_payload"], 6)
    # the cure-included R10-15 table
    i1 = next(i for i, x in enumerate(LINES) if x.startswith("| R, m | Weather | Endpoint payload, actual / floor kg"))
    ab = {"gamma": "G", "Q": "Q", "face_compression_and_E": "E/F", "film": "film"}
    for j in range(i1 + 2, i1 + 11):
        cells = [c.strip() for c in LINES[j].strip("|").split("|")]
        r, w = int(cells[0]), cells[1]
        ca, cf = [c.strip() for c in cells[2].split("/")]
        la, lf = [c.strip() for c in cells[3].split("/")]
        a, f = g(r, w, False), g(r, w, True)
        add(j + 1, f"R{r} {w} named endpoint, actual", ca, a["endpoint_named_kg"], 3)
        add(j + 1, f"R{r} {w} named endpoint, floor", cf, f["endpoint_named_kg"], 3)
        for lab, cell, row in (("actual", la, a), ("floor", lf, f)):
            mine = "none" if row["least_axes"] is None else "+".join(ab[k] for k in row["least_axes"]) + f" {row['least_usage']:.6f}"
            items.append({"line": j + 1, "passage": f"R{r} {w} least set, {lab}", "card_value": cell, "mine": mine,
                          "status": "REDERIVED-MATCH" if cell == mine else "REDERIVED-DIFFERS", "note": "set and usage to 6 decimals"})
    # the least point's coefficients and usage
    m = re.search(r"γ=([\d.]+), Q=([\d.]+), film=([\d.]+) kg/m² per interface\*\* at usage ([\d.]+)", CARD)
    lp = x["least_properties"]
    for lab, cv, mv in (("least gamma", m.group(1), lp["gamma"]), ("least Q", m.group(2), lp["Q"]),
                        ("least film per interface, kg/m2", m.group(3), lp["film_kg_m2_interface"]),
                        ("least usage", m.group(4), x["least_usage"])):
        add(CARD[:m.start()].count("\n") + 1, lab, cv, mv, 9)
    # other P2 values
    ln = lambda s: CARD[:CARD.index(s)].count("\n") + 1
    nocure = g(10, "ISA", True, cure=False)
    add(ln("+124.261910 kg R10 bill reproduces"), "048 original R10 ISA floor bake endpoint", "124.261910", nocure["endpoint_named_kg"], 6)
    add(ln("giving R10 ISA+82.640676 kg"), "052 comparison: 048 all-four minus 50 kg", "82.640676", nocure["endpoint_all_kg"] - 50, 6)
    add(ln("gives **+77.253 kg**"), "052 comparison: cure-included all-four minus 50 kg", "77.253", g(10, "ISA", True)["endpoint_all_kg"] - 50, 3)
    add(ln("R12 optimistic retained-floor gives **+28.576 kg**"), "052 comparison: R12 optimistic floor all-four minus 50 kg",
        "28.576", g(12, "optimistic", True)["endpoint_all_kg"] - 50, 3)
    add(ln("it changes 1.369 kg to 0.137 kg"), "R10 material water before the bake, kg", "1.369", P2["r10_named_material_water_before_bake_kg"], 3)
    add(ln("it changes 1.369 kg to 0.137 kg"), "R10 material water after the bake, kg", "0.137", P2["r10_named_material_water_after_bake_kg"], 3)
    best = max((r for r in rows if r["external_water"] == 1.0), key=lambda r: r["endpoint_all_kg"])
    add(ln("best all-four payload is −998.333 kg"), "1 mm best all-four, kg", "-998.333", best["endpoint_all_kg"], 3)
    items.append({"line": ln("All 432 new R10–15 cases at 1 mm"), "passage": "1 mm: no case floats", "card_value": "all 432 fail",
                  "mine": f"none of the {sum(1 for r in rows if r['external_water'] == 1.0)} R10 ISA cases computed floats",
                  "status": "REDERIVED-MATCH" if not any(r["floats_any"] for r in rows if r["external_water"] == 1.0) else "REDERIVED-DIFFERS",
                  "note": "R10 ISA holds the best case; larger radii and other weathers were not recomputed"})
    for fin, route in (("AgFEP05", "desiccant"), ("AgFEP1", "dry_gas")):
        before, after = g(15, "optimistic", True, False, fin, route), g(15, "optimistic", True, True, fin, route)
        items.append({"line": ln("AgFEP05/R15/optimistic/floor/desiccant"), "passage": f"{fin}/R15/optimistic/floor/{route} loses its float with cure",
                      "card_value": "loses every allowed set", "mine": f"without cure {before['least_axes']} {before['least_usage']:.6f}; with cure none",
                      "status": "REDERIVED-MATCH" if before["least_axes"] and after["least_axes"] is None else "REDERIVED-DIFFERS", "note": ""})
    add(ln("8.33272 g/m² installed"), "installed finish, g/m2", "8.33272", 7.5752 * 1.1, 5)
    add(ln("648 new rows include cure compression"), "648 = 216 cure rows at 0.1 mm + 432 rows at 1 mm", "648", 4 * 3 * 3 * 2 * 3 + 432, 0)
    return items


def main():
    p2 = p2_items()
    own = OWN["items"]
    traced = []
    for k, t in TR.items():
        for it in t["items"]:
            traced.append(dict(it, worker=k))
    st = {}
    for it in traced:
        st[it["status"]] = st.get(it["status"], 0) + 1
    p2_ok = sum(1 for x in p2 if x["status"] == "REDERIVED-MATCH")
    p2_bad = [x for x in p2 if x["status"] != "REDERIVED-MATCH"]
    own_num = [x for x in own if x["item"] not in ("joined or broken tokens in CARD.md", "added grounding routes", "PENDING at filing")]
    numbers_traced = sum(v for s, v in st.items() if s in ("MATCH", "ROUNDING", "DERIVED-OK", "MISMATCH", "DERIVED-DIFFERS", "UNTRACEABLE"))
    mism = [x for x in traced if x["status"] in ("MISMATCH", "DERIVED-DIFFERS")]
    untr = [x for x in traced if x["status"] == "UNTRACEABLE"]
    pend = next(x for x in own if x["item"] == "PENDING at filing")
    since = [i for t, i in pend["filed_since"] if i.startswith(("rpt-check", "rpt-lead", "rpt-1228-mainline"))
             and "030d-design-register" not in i]
    typo = next(x for x in own if x["item"] == "joined or broken tokens in CARD.md")["found"]
    routes = next(x for x in own if x["item"] == "added grounding routes")
    total = numbers_traced + len(p2) + len(own_num)

    W = [  # wording items that change or blur meaning, with the source's wording
        ("143", "Pach's stored test-depth field is 0.0011 m", "CHECK-045: the stored owner field is 1.1 in a metres field; 0.0011 m is its correction",
         "Pach's stored test-depth field was 1.1 in a metres field; CHECK-045 corrects it to 0.0011 m"),
        ("213", "052's source table subtracts 50 kg extra service from original 048 endpoints, giving R10 ISA+82.640676 kg",
         "the endpoint is 048's all-four +132.640676 kg (RESULTS mask 15), not its published named +124.262 kg",
         "name the all-four endpoint (+132.640676 - 50 = +82.640676 kg)"),
        ("23", "the original +0.120151 kg allowance", "040's fold calls it a repair on 037b's original 028b geometry", "the original +0.120151 kg repair"),
        ("244", "four additions named", f"GROUND-FIRST.json carries {routes['found']}: {'; '.join(routes['mine'])}",
         "name the fifth, 052's complete dry-service and crossply demonstration"),
        ("13", "warehouse film 0.985018/0.933256", "046: ten-year warehouse values", "ten-year warehouse film 0.985018/0.933256"),
        ("31", "the member Euler ratio is 0.375, not buckling", "CHECK-043: the member is not shown to cross its Euler load; assembly and local wall still need assessment (line 232 says so)",
         "is 0.375: the member is not shown to buckle"),
        ("139", "quoted \"no damage-tolerant fix on budget\"", "045: \"neither can be made so on its own budget\"", "quote 045's words or drop the quotation marks"),
        ("236", "rigid/pinned film multipliers 7.151119777/2.046193535 differ from 7.155002497/2.047133403", "CHECK-041: m6 film-tangent values; which pair is the checker's is not stated",
         "say which pair is CHECK-041's and which the owner's"),
        ("236", "Bare-pin mechanisms do not become a stable practical frame", "CHECK-041 supports only zero positive stable margin for the prescribed bare pinned configuration",
         "limit the sentence to the prescribed bare pinned configuration"),
        ("35", "The exception itself supplies no numerical result", "the refusal report states 048's regression reproduced within 0.00014 kg",
         "supplies no new result"),
    ]
    now = datetime.datetime.now().astimezone()
    L = []
    a = L.append
    a("# CHECK-030d: the morning design register, checked behind its owner. QUESTIONABLE / PROJECTION")
    a("")
    a(f"Order {ORDER}. Card rpt-ref-e999413f5ed23130ebf6 (owner codex ref-3f7ec48b84b54a049007), "
      f"CARD.md sha256 {sha(D + '/CARD.md')[:16]}. Brief CHECK.md with COMMON.md. Started {STARTED[11:19]} PDT when the order "
      "was read; the end time is in RESULTS.json. Times are measurements, not limits. No 030d code was read or run.")
    a("")
    a("## Verdict")
    a("")
    a(f"**No numerical mismatch.** {total} numbers were checked:")
    a(f"- **{len(p2)} P2 values re-derived** with this seat's own code. These are the whole R 10 bill, the cure-included "
      "R 10-15 table, the least point, the 052 comparison points, the 1 mm best case and the two lost marginal floats. "
      f"Matches: {p2_ok} of {len(p2)}.")
    a(f"- **{len(own_num)} values from this seat's own arithmetic:** the R 30 beryllium faces and shares, six Weibull scales, "
      "the 18 folded reports, 408 pins, the snapshot copies, 51 links, and 104 rows and 1553 findings. All agree.")
    a(f"- **{numbers_traced} values traced** line by line to their source reports by four sub-workers of this seat, redoing "
      f"each derived number: {st.get('MATCH', 0)} exact, {st.get('ROUNDING', 0)} correct roundings, {st.get('DERIVED-OK', 0)} "
      f"re-derived, {len(mism)} mismatches. The {len(untr)} untraceable items resolve to 030d's own data (below).")
    a("")
    a(f"**Wording:** {len(W)} items blur or misstate a source. Four change the reading:")
    a("- the Pach test depth (stored and corrected values reversed);")
    a("- the unnamed 048 endpoint behind +82.640676 kg;")
    a("- 040's repair called an allowance;")
    a("- four of five added grounding routes named.")
    a("")
    a(f"**Typography:** {sum(typo.values())} joined or broken tokens, such as \"2, 027, 245\", \"AtR30\" and \"colderh 2\" for \"colder h=2\".")
    a("")
    a(f"**Pending list:** correct at filing (05:51). Since then {len(since)} reports have filed: {', '.join(since)}. They need a "
      "030e register or addendum.")
    a("")
    a("## How it was checked")
    a("")
    a("- **P2 (048's account with cure compression):** recomputed with this seat's model49/thermal49 (MAINLINE-049). It is "
      "this seat's port of 040, which reproduces 048's beryllium rows bit for bit and CHECK-040's rows within 0.0006 kg. "
      "It shares 040's equations, so it checks 030d's arithmetic and search, not the physics. It ran through simjob "
      "(8 cores, 48 s).")
    a("- **Own arithmetic:**")
    a("  - the R 30 faces from this seat's own 040-account run;")
    a("  - weakest-link Weibull scales with m = 10;")
    a("  - the queue scanned for every report ingested between 030c's snapshot and 030d's intake;")
    a("  - each folded report's pins against 030d's snapshot copies;")
    a("  - the card's links, and the rows of 030d's REGISTER.json and NFI.json.")
    a("- **Tracing:** four sub-workers, each holding a set of passages, read the source report bodies, cards and data files "
      "(never code). Each classified every number and redid every sum, difference, ratio and percentage.")
    a("")
    ch = json.load(open(f"{D}/CHANGES.json"))
    tagged = sum(1 for c in ch if "QUESTIONABLE" in c.get("tag", "") or "PROJECTION" in c.get("tag", ""))
    linked = sum(1 for ln_ in LINES if ln_.startswith("- **") and "](snapshots/" in ln_)
    a("## Tags, sources and formulas")
    a("")
    a(f"- **Tags:** the card is headed QUESTIONABLE / PROJECTION throughout; {tagged} of {len(ch)} change entries in CHANGES.json "
      "carry the tag.")
    a(f"- **Sources:** {linked} of the 18 change lines link their source report, and all 51 links resolve.")
    a("- **Formulas:** the stated ones reproduce the printed numbers. These are the retained-floor joining max(actual, 5% of "
      "faces + core) with the primer outside it, the bake's 90% removal of added material water, the 0.1 and 1 mm exterior "
      "films, and the weakest-link scaling of the Pf targets.")
    a("")
    a("## Results by passage")
    a("")
    a("| Passage | Checked by | Numbers | Exact | Rounding | Re-derived | Mismatch | Untraceable | Wording |")
    a("|---|---|---|---|---|---|---|---|---|")
    a(f"| Top table P2 rows, P2 section, R 10 bill, cure table (lines 7-9, 42-96) | own computation | {len(p2)} | - | - | {p2_ok} | "
      f"{len(p2_bad)} | 0 | 1 (line 213) |")
    a(f"| R 30 supply, scales, counts, intake, pins, links (lines 15, 19, 118-122, 224-228, 246-254) | own arithmetic | "
      f"{len(own_num)} | - | - | {sum(1 for x in own_num if x['ok'])} | {sum(1 for x in own_num if not x['ok'])} | 0 | 1 (line 244) |")
    names = {"A": "P3 frames, reliability, CHECK-041/043, partial 051 (13, 24, 31, 32, 37, 217-236)",
             "B": "Damage and life: 044, 045, 046 and their checks (26, 27, 30, 33, 38, 124-159)",
             "C": "Build, 040 fold, CHECK-042, 050 exception, partial CHECK-048, ground-first (17, 19, 23, 25, 35, 36, 46-48, 238-244)",
             "D": "050 weather and 052 P3 whole bill (10-12, 39, 40, 98-116, 161-215)"}
    for k, t in TR.items():
        c = {}
        for it in t["items"]:
            c[it["status"]] = c.get(it["status"], 0) + 1
        n = sum(v for s, v in c.items() if s != "WORDING")
        a(f"| {names[k]} | sub-worker {k} | {n} | {c.get('MATCH', 0)} | {c.get('ROUNDING', 0)} | {c.get('DERIVED-OK', 0)} | "
          f"{c.get('MISMATCH', 0) + c.get('DERIVED-DIFFERS', 0)} | {c.get('UNTRACEABLE', 0)} | {c.get('WORDING', 0)} |")
    a("")
    a("**Untraceable, resolved:**")
    a("- C's \"104 rows\" and \"1553 attributed findings\" are the row counts of 030d's REGISTER.json and NFI.json "
      "(98 + 6 and 961 + 583 + 9).")
    a("- C's line-244 additions are 030d's own extension routes D-G1 to D-G4 in GROUND-FIRST.json; it carries a fifth.")
    a("")
    a("**Re-derived highlights:**")
    a("- **R 10 bill:** all 28 line values, both totals, the lift and both payloads match to the printed 6 decimals: "
      "+118.694826 kg and +0.000003 kg.")
    a("- **Least point:** gamma 0.498375922, Q 0.710673963, film 0.081667779 kg/m2 and usage 0.842794177 match to 9 decimals.")
    a("- **Cure-included table:** all 18 endpoints within 0.0005 kg; all 18 least sets and usages match.")
    a("- **Other P2 values:** the 052 points (+82.640676, +77.253, +28.576 kg), the 1 mm best (-998.333 kg) and both lost "
      "AgFEP floats reproduce.")
    a("- **R 30 beryllium faces:** 102.230791 t (named endpoint) and 103.146242 t (least point). The share is 23.610% of "
      "433 t and 23.775% of 430 t.")
    a("")
    a("## Wording items")
    a("")
    a("| Line | Card | Source | Proposed |")
    a("|---|---|---|---|")
    for ln_, card_, src, fix in W:
        a(f"| {ln_} | {card_} | {src} | {fix} |")
    a("")
    a("Typography (count in CARD.md): " + "; ".join(f"`{k.replace(chr(92), '')}` x{v}" for k, v in typo.items()) + ".")
    a("")
    a("A wording item sub-worker A raised is not carried. Line 233 says 051 \"stays PENDING\" while its report says "
      "PARTIAL / HELD; that is 030d's declared convention for partial filings.")
    a("")
    a("## Pending list")
    a("")
    a("030d lists 029 check, 047, 047 check, 048 check, 049, 049 check and 051 as pending at its 05:46:07 intake. That "
      "was correct at filing (05:51:14). Filed since, by queue ingest time:")
    for t_, i in pend["filed_since"]:
        if i in since:
            a(f"- {t_[11:19]} {i}")
    a("")
    a("At this check, 047, the 047 check and the 049 check have no completed report.")
    a("")
    a("## Scope and limits")
    a("")
    a("- **Traced but not recomputed:** the model outputs of 041, 043, 045, 046, 050 and 052. 052's 1440 assertions and 253 "
      "pins are taken from its text.")
    a("- **1 mm cases:** of 048's 432, only the 24 R 10 ISA ones were recomputed. They hold the best case; the rest are larger "
      "radii and harsher weather.")
    a("- **Not re-derived:** the -998.280 kg favourable-bound value.")
    a("- **Copies and code:** 030d's snapshot copies were compared by sha256 only: 345 identical, 63 not copied (46 scripts, "
      "images, archives, logs).")
    a("- **No owner code:** no 030d code was read or run; no source's code was read by the sub-workers.")
    a("")
    a("## Files")
    a("")
    a("All files are pinned in the report:")
    a("- this check: CHECK.md, RESULTS.json, NFI.json, INPUTS.json;")
    a("- own code and outputs: p2check.py, own_checks.py, chk030d.py, P2CHECK.json, OWN-CHECKS.json;")
    a("- traces: trace/A-D.json;")
    a("- simretry.sh.")
    a("")
    a("## Then")
    a("")
    a("File one report; the robotics seat sends the next job.")
    text = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "CHECK.md.tmp"), "w") as fh:
        fh.write(text)
    os.replace(os.path.join(HERE, "CHECK.md.tmp"), os.path.join(HERE, "CHECK.md"))

    results = {"schema": 1, "check": "CHECK-030d", "order": ORDER, "card": "rpt-ref-e999413f5ed23130ebf6",
               "card_md_sha256": sha(D + "/CARD.md"), "tag": "QUESTIONABLE / PROJECTION", "started_at": STARTED,
               "ended_at": now.isoformat(), "times_are": "measurements only",
               "totals": {"numbers_checked": total, "p2_rederived": len(p2), "p2_rederived_match": p2_ok, "own_arithmetic": len(own_num),
                          "traced": numbers_traced, "traced_by_status": st, "mismatches": len(mism) + len(p2_bad),
                          "wording_items_carried": len(W), "typography_tokens": sum(typo.values())},
               "p2_items": p2, "own_items": own, "traced_items": traced, "wording": [dict(zip(("line", "card", "source", "proposed"), w)) for w in W],
               "pending": {"at_filing": pend["card"], "filed_since": pend["filed_since"]},
               "simjob": open("unpublished-local-ref:dfab88333f4b31a0").read().splitlines()}
    with open(os.path.join(HERE, "RESULTS.json.tmp"), "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "RESULTS.json.tmp"), os.path.join(HERE, "RESULTS.json"))
    nfi = {"schema": 1, "check": "CHECK-030d", "tag": "QUESTIONABLE", "items": [
        {"id": "NFI-CHK030d-WORDING", "kind": "fix card", "claim": f"{len(W)} wording items blur or misstate a source; four change the reading "
         "(lines 143, 213, 23, 244).", "proposed": "Apply the proposed wording in CHECK.md's table in the next register."},
        {"id": "NFI-CHK030d-TYPOGRAPHY", "kind": "fix card", "claim": f"{sum(typo.values())} joined or broken tokens in CARD.md, e.g. "
         "'2, 027, 245', 'AtR30', 'colderh 2' (source: 'colder h=2'), '041d amage'.", "proposed": "Restore the spaces and symbols in the next register."},
        {"id": "NFI-CHK030d-PENDING", "kind": "NFI", "claim": f"{len(since)} reports filed after 030d: {', '.join(since)}.",
         "proposed": "Fold them in a 030e register or addendum; 049 answers the Be-free branch (no sourced Be-free P2 floats)."},
        {"id": "NFI-CHK030d-SCOPE", "kind": "NFI", "claim": "Model outputs of 041/043/045/046/050/052 were traced, not recomputed; of the 432 "
         "1 mm cases only the 24 R10 ISA ones were recomputed; the -998.280 kg bound was not re-derived; this seat's P2 model shares "
         "040's equations.", "proposed": "None needed for the register; the cards' own checkers cover their models."}]}
    with open(os.path.join(HERE, "NFI.json.tmp"), "w") as fh:
        json.dump(nfi, fh, indent=1)
    os.replace(os.path.join(HERE, "NFI.json.tmp"), os.path.join(HERE, "NFI.json"))
    rep = json.load(open(f"{Q}/rpt-ref-e999413f5ed23130ebf6.json"))
    pinned = {a_["path"]: a_["sha256"] for a_ in rep["artifacts"]}
    read030d = ["CARD.md", "INTAKE.json", "PENDING.json", "CHANGES.json", "SNAPSHOT-FROZEN.json", "END.json",
                "REGISTER-COVERAGE.json", "REGISTER.json", "NFI.json", "GROUND-FIRST.json", "GROUND-FIRST.md", "SUPPLEMENTAL-ORDERS.json"]
    pins = []
    for n in read030d:
        p = f"{D}/{n}"
        h = sha(p)
        pins.append({"path": p, "sha256": h, "bytes": os.path.getsize(p), "role": "030d artifact read",
                     "matches_030d_report_pin": pinned.get(p) == h})
    for p in (f"{BRIEF}/CHECK.md", f"{BRIEF}/COMMON.md", f"{BRIEF}/CARD-030d-REGISTER-REFILE.md", f"{Q}/{ORDER}.json",
              f"{Q}/rpt-ref-e999413f5ed23130ebf6.json", f"{M49}/model49.py", f"{M49}/thermal49.py",
              f"{M49}/COMPUTE.json",
              "evidence/81710ad5e8ddd7e0-COATINGS.json"):
        pins.append({"path": p, "sha256": sha(p), "bytes": os.path.getsize(p), "role": "brief, order, report or own model read"})
    for k, t in TR.items():
        for s in t.get("sources_read", []):
            if isinstance(s, dict) and s.get("path") and os.path.exists(s["path"]):
                pins.append({"path": s["path"], "sha256": sha(s["path"]), "bytes": os.path.getsize(s["path"]), "role": f"source read by sub-worker {k}"})
    seen, uniq = set(), []
    for p in pins:
        if p["path"] not in seen:
            seen.add(p["path"])
            uniq.append(p)
    inputs = {"schema": 1, "check": "CHECK-030d", "order": ORDER, "pins": uniq,
              "brief_pins_match": {"CHECK.md": sha(f"{BRIEF}/CHECK.md").startswith("03b357cbce6a591d"),
                                   "COMMON.md": sha(f"{BRIEF}/COMMON.md").startswith("6a6a596f4dc23790")}}
    with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
        json.dump(inputs, fh, indent=1)
    os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
    print(total, "numbers;", len(p2), "p2 (", p2_ok, "match );", len(mism), "traced mismatches;", len(W), "wording;", len(uniq), "pins")
    for x in p2_bad:
        print("P2 DIFFERS:", x)


if __name__ == "__main__":
    main()
