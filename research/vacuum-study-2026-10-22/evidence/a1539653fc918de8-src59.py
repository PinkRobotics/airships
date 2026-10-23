#!/usr/bin/env python3
"""MAINLINE-059 sourced inputs: every value is drawn from the sourcing files by property id and text, and asserted."""
import json

SRC = "unpublished-local-ref:ff99c18d0b024e9e"
_FILES = {}
USED = {}


def rows(f):
    if f not in _FILES:
        _FILES[f] = json.load(open(f"{SRC}/{f}.json"))["rows"]
    return _FILES[f]


def val(key, f, pid, prop_text, value, prod_text="", tol=2e-3):
    """The sourced row with this property id whose property (and product) contain the texts; value asserted."""
    hits = [(i, r) for i, r in enumerate(rows(f)) if r["property_id"] == pid and prop_text in r["property"]
            and prod_text in str(r.get("product"))]
    if len(hits) > 1:
        hits = [(i, r) for i, r in hits if r["value"] is not None and abs(r["value"] - value) <= tol * max(1, abs(value))]
    assert len(hits) == 1, (f, pid, prop_text, prod_text, len(hits))
    i, r = hits[0]
    assert r["value"] is not None and abs(r["value"] - value) <= tol * max(1.0, abs(value)), (f, pid, r["value"], value)
    USED[key] = {"value": r["value"], "units": r["units"], "file": f"{f}.json", "index": i,
                 "printed": r["value_as_printed"], "source": r["source"].get("title"), "url": r["source"].get("url"),
                 "location": r["source"].get("location")}
    return r["value"]


def note(key, f, pid, prop_text, prod_text=""):
    """A sourced statement (words only): recorded and returned as its printed text."""
    hits = [(i, r) for i, r in enumerate(rows(f)) if r["property_id"] == pid and prop_text in r["property"]
            and prod_text in str(r.get("product"))]
    assert len(hits) >= 1, (f, pid, prop_text)
    i, r = hits[0]
    USED[key] = {"value": None, "file": f"{f}.json", "index": i, "printed": r["value_as_printed"],
                 "source": r["source"].get("title"), "url": r["source"].get("url"), "location": r["source"].get("location"),
                 "quote": r["source"].get("quote")}
    return r["value_as_printed"]
