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
SCHEMA_VERSION = 1
REQUIRED = ("series-bible.yaml", "continuity-ledger.yaml", "asset-index.yaml", "session-handoff.md")
STATUSES = {"proposed", "generated", "reviewed", "approved", "rejected", "superseded", "unresolved", "pending"}
errors = []

def load(name):
    path = ROOT / name
    if not path.exists():
        errors.append(f"MISSING {name}")
        return {}
    if path.suffix == ".md":
        text = path.read_text()
        if not text.strip():
            errors.append(f"INVALID {name}: file is empty")
            return {}
        return {"text": text}
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
for name, record in (("series-bible.yaml", series), ("continuity-ledger.yaml", ledger), ("asset-index.yaml", assets)):
    if record and record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"INVALID {name}: schema_version must be {SCHEMA_VERSION}")
episode_data = []
for path in sorted(ROOT.glob("episode-*.yaml")):
    data = load(path.name)
    if data and data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"INVALID {path.name}: schema_version must be {SCHEMA_VERSION}")
    if not isinstance(data.get("episode"), dict):
        errors.append(f"INVALID {path.name}: missing episode mapping")
    elif data["episode"].get("status") not in STATUSES:
        errors.append(f"INVALID {path.name}: unsupported episode status")
    episode_data.append(data)
if series and not isinstance(series.get("series"), dict):
    errors.append("INVALID series-bible.yaml: missing series mapping")
elif series and not series["series"].get("id"):
    errors.append("INVALID series-bible.yaml: series.id is required")
if ledger and "episode_id" not in ledger:
    errors.append("INVALID continuity-ledger.yaml: missing episode_id")
if ledger and not isinstance(ledger.get("states"), list):
    errors.append("INVALID continuity-ledger.yaml: states must be a list")
asset_records = assets.get("assets", [])
if not isinstance(asset_records, list):
    errors.append("INVALID asset-index.yaml: assets must be a list")
    asset_records = []
for asset in asset_records:
    if not isinstance(asset, dict):
        errors.append("INVALID asset-index.yaml: every asset must be a mapping")
        continue
    if not asset.get("id") or not asset.get("version"):
        errors.append("INVALID asset-index.yaml: every asset needs id and version")
    if asset.get("status") and asset["status"] not in STATUSES:
        errors.append(f"INVALID asset-index.yaml: unsupported status for {asset.get('id', '?')}")
if ledger and not isinstance(ledger.get("unresolved"), list):
    errors.append("INVALID continuity-ledger.yaml: unresolved must be a list")
for path in sorted(ROOT.glob("video-take-*.yaml")):
    take_record = load(path.name)
    take = take_record.get("take")
    required_take_fields = ("id", "episode_id", "shot_id", "image_prompt_version", "source_image_id", "model_version", "video_prompt_version", "generation_settings", "output_take_id", "observed_continuity_failures", "approval_status", "reviewed_at", "reviewed_by", "review_notes")
    if not isinstance(take, dict):
        errors.append(f"INVALID {path.name}: missing take mapping")
        continue
    for field in required_take_fields:
        if field not in take:
            errors.append(f"INVALID {path.name}: missing take.{field}")
    if take.get("approval_status") not in {"pending", "approved", "rejected", "revise"}:
        errors.append(f"INVALID {path.name}: unsupported approval_status")
    if not isinstance(take.get("generation_settings"), dict):
        errors.append(f"INVALID {path.name}: generation_settings must be a mapping")
audio_plan = ROOT / "music-video-audio-plan.yaml"
if audio_plan.exists():
    record = load(audio_plan.name)
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"INVALID {audio_plan.name}: schema_version must be {SCHEMA_VERSION}")
    if not isinstance(record.get("audio"), dict):
        errors.append(f"INVALID {audio_plan.name}: audio must be a mapping")
    if not isinstance(record.get("edit_decision_list"), list):
        errors.append(f"INVALID {audio_plan.name}: edit_decision_list must be a list")
    if not isinstance(record.get("quality_gates"), dict):
        errors.append(f"INVALID {audio_plan.name}: quality_gates must be a mapping")
for error in errors:
    print(error)
if errors:
    raise SystemExit(1)
series_info = series.get("series") if isinstance(series.get("series"), dict) else {}
print(f"SERIES: {series_info.get('id', '?')}")
print(f"EPISODES: {', '.join(d.get('episode', {}).get('id', '?') for d in episode_data) or 'none'}")
print(f"LATEST APPROVED SHOT: {ledger.get('latest_approved_shot') or 'none recorded'}")
print(f"UNRESOLVED ITEMS: {len(ledger.get('unresolved', []))}")
print(f"HANDOFF PRESENT: {'yes' if handoff else 'no'}")
print("NEXT ACTION: confirm continuity checkpoint before generation")
