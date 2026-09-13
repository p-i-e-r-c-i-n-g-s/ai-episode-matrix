#!/usr/bin/env python3
"""Validate episode records and print a resumable continuity checkpoint."""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: install PyYAML to validate YAML records", file=sys.stderr)
    raise SystemExit(2)

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SCHEMA_VERSION = 1
STATUSES = {"proposed", "generated", "reviewed", "approved", "rejected", "superseded", "unresolved", "pending"}
TAKE_STATUSES = {"pending", "approved", "rejected", "revise"}
HANDOFF_FIELDS = ("SETUP MODE", "UPDATED AT", "SERIES", "EPISODE", "SCRIPT VERSION", "LAST APPROVED SHOT", "CURRENT STORY STATE", "UNRESOLVED QUESTIONS", "NEXT RECOMMENDED SHOT")
errors: list[str] = []


def invalid(name: str, message: str) -> None:
    errors.append(f"INVALID {name}: {message}")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_text(record: dict[str, Any], field: str, name: str) -> None:
    if not nonempty(record.get(field)):
        invalid(name, f"{field} must be non-empty text")


def require_version(record: dict[str, Any], field: str, name: str) -> None:
    value = record.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        invalid(name, f"{field} must be a positive integer")


def require_timestamp(record: dict[str, Any], field: str, name: str) -> None:
    value = record.get(field)
    if not nonempty(value):
        invalid(name, f"{field} must be a non-empty ISO-8601 timestamp")
        return
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        invalid(name, f"{field} must be an ISO-8601 timestamp")
        return
    if parsed.tzinfo is None:
        invalid(name, f"{field} must include a timezone")


def load(name: str) -> dict[str, Any]:
    path = ROOT / name
    if not path.exists():
        errors.append(f"MISSING {name}")
        return {}
    if not path.is_file():
        invalid(name, "must be a regular file")
        return {}
    if path.suffix == ".md":
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            invalid(name, "file is empty")
            return {}
        return {"text": text}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        invalid(name, str(exc))
        return {}
    if not isinstance(value, dict):
        invalid(name, "top level must be a mapping")
        return {}
    return value


def require_schema(name: str, record: dict[str, Any]) -> None:
    if record and record.get("schema_version") != SCHEMA_VERSION:
        invalid(name, f"schema_version must be {SCHEMA_VERSION}")


def parse_handoff(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Z][A-Z /]+):\s*(.*)$", line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


series = load("series-bible.yaml")
ledger = load("continuity-ledger.yaml")
assets = load("asset-index.yaml")
handoff = load("session-handoff.md")
for filename, record in (("series-bible.yaml", series), ("continuity-ledger.yaml", ledger), ("asset-index.yaml", assets)):
    require_schema(filename, record)

series_record = series.get("series")
series_id = None
if not isinstance(series_record, dict):
    invalid("series-bible.yaml", "missing series mapping")
else:
    series_id = series_record.get("id")
    require_text(series_record, "id", "series-bible.yaml")
    require_text(series_record, "title", "series-bible.yaml")
    require_version(series_record, "version", "series-bible.yaml")
    require_timestamp(series_record, "updated_at", "series-bible.yaml")
    if series_record.get("status") not in STATUSES:
        invalid("series-bible.yaml", "unsupported series.status")

episode_paths = sorted(ROOT.glob("episode-*.yaml"))
if not episode_paths:
    errors.append("MISSING episode-*.yaml")
episode_data: list[dict[str, Any]] = []
episode_ids: set[str] = set()
for path in episode_paths:
    data = load(path.name)
    require_schema(path.name, data)
    episode = data.get("episode")
    if not isinstance(episode, dict):
        invalid(path.name, "missing episode mapping")
        continue
    require_text(episode, "id", path.name)
    require_text(episode, "title", path.name)
    require_version(episode, "version", path.name)
    require_timestamp(episode, "updated_at", path.name)
    if episode.get("setup_mode") not in {"quick", "full"}:
        invalid(path.name, "episode.setup_mode must be quick or full")
    if episode.get("status") not in STATUSES:
        invalid(path.name, "unsupported episode.status")
    episode_id = episode.get("id")
    if nonempty(episode_id):
        if episode_id in episode_ids:
            invalid(path.name, f"duplicate episode id {episode_id}")
        episode_ids.add(episode_id)
    if episode.get("status") == "approved":
        require_text(data, "beginning_state", path.name)
        require_text(data, "ending_state", path.name)
    episode_data.append(data)

ledger_episode_id = ledger.get("episode_id")
require_text(ledger, "series_id", "continuity-ledger.yaml")
require_text(ledger, "episode_id", "continuity-ledger.yaml")
require_timestamp(ledger, "updated_at", "continuity-ledger.yaml")
if series_id and ledger.get("series_id") != series_id:
    invalid("continuity-ledger.yaml", "series_id does not match series-bible.yaml")
if episode_ids and ledger_episode_id not in episode_ids:
    invalid("continuity-ledger.yaml", "episode_id does not resolve to an episode record")

states = ledger.get("states")
if not isinstance(states, list):
    invalid("continuity-ledger.yaml", "states must be a list")
    states = []
state_ids: set[str] = set()
approved_state_ids: set[str] = set()
for index, state in enumerate(states):
    if not isinstance(state, dict):
        invalid("continuity-ledger.yaml", f"states[{index}] must be a mapping")
        continue
    if not nonempty(state.get("shot_id")):
        invalid("continuity-ledger.yaml", f"states[{index}].shot_id is required")
        continue
    shot_id = state["shot_id"]
    if shot_id in state_ids:
        invalid("continuity-ledger.yaml", f"duplicate shot state {shot_id}")
    state_ids.add(shot_id)
    if state.get("status") not in STATUSES:
        invalid("continuity-ledger.yaml", f"unsupported status for {shot_id}")
    if state.get("status") == "approved":
        approved_state_ids.add(shot_id)
latest = ledger.get("latest_approved_shot")
if latest and latest not in approved_state_ids:
    invalid("continuity-ledger.yaml", "latest_approved_shot must resolve to an approved state")
if not isinstance(ledger.get("unresolved"), list):
    invalid("continuity-ledger.yaml", "unresolved must be a list")

asset_records = assets.get("assets")
if not isinstance(asset_records, list):
    invalid("asset-index.yaml", "assets must be a list")
    asset_records = []
asset_keys: set[tuple[str, int]] = set()
asset_ids: set[str] = set()
for index, asset in enumerate(asset_records):
    if not isinstance(asset, dict):
        invalid("asset-index.yaml", f"assets[{index}] must be a mapping")
        continue
    for field in ("id", "type", "path_or_url", "source"):
        require_text(asset, field, "asset-index.yaml")
    require_version(asset, "version", "asset-index.yaml")
    if asset.get("status") not in STATUSES:
        invalid("asset-index.yaml", f"unsupported status for {asset.get('id', '?')}")
    if nonempty(asset.get("id")) and isinstance(asset.get("version"), int):
        key = (asset["id"], asset["version"])
        if key in asset_keys:
            invalid("asset-index.yaml", f"duplicate asset version {asset['id']} v{asset['version']}")
        asset_keys.add(key)
        asset_ids.add(asset["id"])
require_timestamp(assets, "updated_at", "asset-index.yaml")

if handoff:
    values = parse_handoff(handoff.get("text", ""))
    for field in HANDOFF_FIELDS:
        if not nonempty(values.get(field)):
            invalid("session-handoff.md", f"{field} must have a value")
    if values.get("SETUP MODE") not in {"quick", "full"}:
        invalid("session-handoff.md", "SETUP MODE must be quick or full")
    if nonempty(values.get("UPDATED AT")):
        require_timestamp({"updated_at": values["UPDATED AT"]}, "updated_at", "session-handoff.md")
    if series_id and values.get("SERIES") != series_id:
        invalid("session-handoff.md", "SERIES does not match series-bible.yaml")
    if ledger_episode_id and values.get("EPISODE") != ledger_episode_id:
        invalid("session-handoff.md", "EPISODE does not match continuity-ledger.yaml")

for path in sorted(ROOT.glob("video-take-*.yaml")):
    take_record = load(path.name)
    require_schema(path.name, take_record)
    take = take_record.get("take")
    if not isinstance(take, dict):
        invalid(path.name, "missing take mapping")
        continue
    for field in ("id", "episode_id", "shot_id", "image_prompt_version", "source_image_id", "model_version", "video_prompt_version", "output_take_id"):
        require_text(take, field, path.name)
    require_timestamp(take, "created_at", path.name)
    if take.get("episode_id") not in episode_ids:
        invalid(path.name, "take.episode_id does not resolve to an episode record")
    if take.get("source_image_id") not in asset_ids:
        invalid(path.name, "take.source_image_id does not resolve to the asset index")
    if take.get("approval_status") not in TAKE_STATUSES:
        invalid(path.name, "unsupported approval_status")
    if not isinstance(take.get("generation_settings"), dict):
        invalid(path.name, "generation_settings must be a mapping")
    if not isinstance(take.get("observed_continuity_failures"), list):
        invalid(path.name, "observed_continuity_failures must be a list")
    if take.get("approval_status") in {"approved", "rejected", "revise"}:
        require_timestamp(take, "reviewed_at", path.name)
        require_text(take, "reviewed_by", path.name)
        require_text(take, "review_notes", path.name)

audio_plan = ROOT / "music-video-audio-plan.yaml"
if audio_plan.exists():
    record = load(audio_plan.name)
    require_schema(audio_plan.name, record)
    if not isinstance(record.get("audio"), dict):
        invalid(audio_plan.name, "audio must be a mapping")
    if not isinstance(record.get("edit_decision_list"), list):
        invalid(audio_plan.name, "edit_decision_list must be a list")
    if not isinstance(record.get("quality_gates"), dict):
        invalid(audio_plan.name, "quality_gates must be a mapping")

for error in errors:
    print(error)
if errors:
    raise SystemExit(1)
series_info = series.get("series") if isinstance(series.get("series"), dict) else {}
print(f"SERIES: {series_info.get('id')}")
print(f"EPISODES: {', '.join(sorted(episode_ids))}")
print(f"LATEST APPROVED SHOT: {latest or 'none recorded'}")
print(f"UNRESOLVED ITEMS: {len(ledger.get('unresolved', []))}")
print("HANDOFF PRESENT: yes")
print("NEXT ACTION: confirm continuity checkpoint before generation")
