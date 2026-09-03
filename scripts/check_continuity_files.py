#!/usr/bin/env python3
"""Report missing or malformed durable episode records."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
required = ["series-bible.yaml", "continuity-ledger.yaml", "asset-index.yaml", "session-handoff.md"]
missing = [name for name in required if not (root / name).exists()]
for name in missing:
    print(f"MISSING {name}")
for path in root.glob("episode-*.yaml"):
    try:
        text = path.read_text()
        if "episode:" not in text:
            print(f"INVALID {path}")
    except Exception as exc:
        print(f"INVALID {path}: {exc}")
if missing:
    raise SystemExit(1)
print("Continuity records present")
