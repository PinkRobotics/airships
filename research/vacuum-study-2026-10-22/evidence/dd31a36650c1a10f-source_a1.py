"""Copy only explicitly pinned evidence. Owner executable code is excluded."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / "sources" / name).read_text())


def take(entry, local_name):
    original = Path(entry.get("owned_copy", entry["path"]))
    if original.suffix in (".py", ".sh", ".ipynb", ".pyc"):
        raise ValueError("Owner code excluded: " + str(original))
    destination = ROOT / "sources" / local_name
    raw = destination.read_bytes() if destination.exists() else original.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == entry["sha256"], original
    assert len(raw) == entry["bytes"], original
    if not destination.exists():
        destination.write_bytes(raw)
    logpath = ROOT / "EVIDENCE-PINS.json"
    log = json.loads(logpath.read_text()) if logpath.exists() else {}
    log[local_name] = {"declared": entry, "read_from": str(original),
                       "local_path": str(destination), "sha256": entry["sha256"],
                       "bytes": entry["bytes"]}
    logpath.write_text(json.dumps(log, indent=2) + "\n")
    return destination


def primary(card, name):
    data = read(card + "--INPUTS.json")
    items = data["primary_source_pins"] if card == "062" else data["sources"]
    e = next(x for x in items if Path(x["path"]).name == name)
    return take(e, "primary--" + name)


def dependency(label, name):
    items = read("062--INPUTS.json")["brief_and_dependency_pins"]
    e = next(x for x in items if x.get("label") == label and Path(x["path"]).name == name)
    return take(e, label + "--" + name)


def runfile(case, name):
    items = read("056--ARTIFACT-MANIFEST.json")["files"]
    suffix = "/runs/" + case + "/" + name
    e = next(x for x in items if x["path"].endswith(suffix))
    return take(e, case + "--" + name)
