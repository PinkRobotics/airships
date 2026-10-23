#!/usr/bin/env python3
"""MAINLINE-013 source vetting: re-check every DOI named in cores.json against Crossref, independently of whoever
gathered it, and record the title, journal and year Crossref returns beside the title the record claims.

Run: python3 -I vet_sources.py   (needs network; writes source_check.json beside this file)
A DOI Crossref does not know, or whose title does not share the record's key words, is listed as a MISMATCH; the card
does not use a value whose only source fails this check.
"""
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def norm_words(s):
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if len(w) > 3}


def crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    req = urllib.request.Request(url, headers={"User-ref-8240dc08c477fab7cd29": "ref-6402fe46050c0dd7156c/1.0 (source check)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as fh:
            m = json.load(fh)["message"]
    except Exception as exc:  # unknown DOI or network: recorded, never guessed
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    issued = (m.get("issued") or {}).get("date-parts") or [[None]]
    return {"ok": True, "title": (m.get("title") or [""])[0], "journal": (m.get("container-title") or [""])[0],
            "year": issued[0][0], "authors": [a.get("family") for a in (m.get("author") or [])][:6]}


def main():
    table = json.load(open(os.path.join(HERE, "cores.json")))
    dois = {}
    for c in table["cores"]:
        doi = (c.get("source") or {}).get("doi")
        if doi:
            dois.setdefault(doi.strip(), []).append(c)
    for s in table.get("scaling", []):
        doi = (s.get("source") or {}).get("doi")
        if doi:
            dois.setdefault(doi.strip(), []).append(s)
    out = {"checked_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "dois": []}
    for doi, users in sorted(dois.items()):
        cr = crossref(doi)
        claimed = users[0].get("source", {}).get("citation", "")
        overlap = sorted(norm_words(cr.get("title")) & norm_words(claimed)) if cr.get("ok") else []
        verdict = "MATCH" if cr.get("ok") and len(overlap) >= 2 else "MISMATCH"
        out["dois"].append({"doi": doi, "crossref": cr, "claimed_citation": claimed, "shared_title_words": overlap,
                            "verdict": verdict, "used_by": [u.get("core_id") or u.get("applies_to") for u in users]})
        time.sleep(0.3)
    with open(os.path.join(HERE, "source_check.json"), "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    bad = [d for d in out["dois"] if d["verdict"] != "MATCH"]
    print(f"{len(out['dois'])} DOIs checked, {len(bad)} mismatched")
    for d in bad:
        print("MISMATCH", d["doi"], d["crossref"].get("title") or d["crossref"].get("error"), "|", d["claimed_citation"][:120])


if __name__ == "__main__":
    main()
