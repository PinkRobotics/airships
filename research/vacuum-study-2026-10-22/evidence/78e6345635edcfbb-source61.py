"""Read exactly named, pinned inputs; keep verified copies in this package."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = json.loads((ROOT / "SOURCE-INDEX.json").read_text())


def source(label, name, parse=True):
    artifact = INDEX[label]["artifacts"][name]
    destination = ROOT / "sources" / f"{label}--{name}"
    data = destination.read_bytes() if destination.exists() else Path(artifact["path"]).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != artifact["sha256"] or len(data) != artifact["bytes"]:
        raise ValueError(f"Pin mismatch: {label}/{name}")
    if not destination.exists():
        destination.write_bytes(data)
    return json.loads(data) if parse and name.endswith(".json") else data.decode()


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        label, name = arg.split("/", 1)
        print(f"\nPIN VERIFIED: {label}/{name}")
        value = source(label, name)
        print(json.dumps(value, indent=2) if not isinstance(value, str) else value)
