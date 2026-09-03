#!/usr/bin/env python3
"""Validate episode records and print a resumable continuity checkpoint."""
import pathlib
import sys

try:
    import yaml
except ImportError:
    print("ERROR: install PyYAML to validate YAML records", file=sys.stderr)
    raise SystemExit(2)

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
REQUIRED = ("series-bible.yaml", "continuity-ledger.yaml", "asset-index.yaml", "session-handoff.md")
STATUSES = {"proposed", "generated", "reviewed", "approved", "rejected", "superseded", "unresolved", "pending"}
errors = []

def load(name):
    path = ROOT / name
    if not path.exists():
        errors.append(f"MISSING {name}")
        return {}
    if path.suffix == ".md":
        return {"text": path.read_text()}
    try:
        value = yaml.safe_load(path.read_text())
        if not isinstance(value, dict):
            errors.append(f"INVALID {name}: top level must be a mapping")
            return {}
        return value
    except Exception as exc:
        errors.append(f"INVALID {name}: {exc}")
        return {}

series = load("series-bible.yaml")
ledger = load("continuity-ledger.yaml")
assets = load("asset-index.yaml")
handoff = load("session-handoff.md")
episode_data = []
for path in sorted(ROOT.glob("episode-*.yaml")):
    data = load(path.name)
    if "episode" not in data:
        errors.append(f"INVALID {path.name}: missing episode mapping")
    elif data["episode"].get("status") not in STATUSES:
        errors.append(f"INVALID {path.name}: unsupported episode status")
    episode_data.append(data)
if series and "series" not in series:
    errors.append("INVALID series-bible.yaml: missing series mapping")
if ledger and "episode_id" not in ledger:
    errors.append("INVALID continuity-ledger.yaml: missing episode_id")
for asset in assets.get("assets", []) if isinstance(assets.get("assets", []), list) else []:
    if not asset.get("id") or not asset.get("version"):
        errors.append("INVALID asset-index.yaml: every asset needs id and version")
    if asset.get("status") and asset["status"] not in STATUSES:
        errors.append(f"INVALID asset-index.yaml: unsupported status for {asset.get('id', '?')}")
for error in errors:
    print(error)
if errors:
    raise SystemExit(1)
print(f"SERIES: {series.get('series', {}).get('id', '?')}")
print(f"EPISODES: {', '.join(d.get('episode', {}).get('id', '?') for d in episode_data) or 'none'}")
print(f"LATEST APPROVED SHOT: {ledger.get('latest_approved_shot') or 'none recorded'}")
print(f"UNRESOLVED ITEMS: {len(ledger.get('unresolved', []))}")
print(f"HANDOFF PRESENT: {'yes' if handoff else 'no'}")
print("NEXT ACTION: confirm continuity checkpoint before generation")
