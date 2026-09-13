# Continuity record contract

This is the canonical ownership and validation contract for schema version 1.

| Record | Owns | Required identity | Approval authority |
|---|---|---|---|
| `series-bible.yaml` | Series identity, world rules, recurring assets, visual contract | `series.id`, title, integer version, status, timezone-aware `updated_at` | Series baseline only |
| `episode-XX.yaml` | Episode arc, scene plan, beginning/ending state | Unique `episode.id`, title, integer version, setup mode, status, timezone-aware `updated_at` | Episode plan |
| `continuity-ledger.yaml` | Shot state transitions and latest approved shot | Matching series and episode IDs, timestamp, unique shot states | Latest approved shot state |
| `asset-index.yaml` | Immutable reusable asset versions | Unique `(id, version)`, type, location, source, status, timestamp | Approved asset version |
| `video-take-*.yaml` | Generation and human review evidence | Resolvable episode, shot, source asset, prompt/model versions, output ID | Human review status |
| `session-handoff.md` | Resumption summary | Matching series/episode, setup mode, timestamp, current and next state | No independent canon authority |

Only approved ledger states and approved asset versions propagate as canon. A handoff summarizes those records; it cannot override them. When equal-authority records conflict, stop with `[CONFLICT—USER DECISION REQUIRED]`.

Run `python3 scripts/check_continuity_files.py PROJECT_DIR` before generation and after every record update. Blank starter templates intentionally fail validation until populated. Validation checks structure, meaningful required values, timestamps, duplicate identities, and cross-record references.

## Safe writes and concurrent sessions

Never overwrite a continuity record directly when another session may be active. Prepare the replacement separately, calculate the current target's SHA-256, then use:

```bash
python3 scripts/atomic_update.py continuity-ledger.yaml prepared-ledger.yaml --expect-sha256 CURRENT_SHA256
```

The helper acquires an exclusive per-record lock, rejects a stale digest, writes through a temporary file, atomically replaces the target, and keeps the prior record as `.bak`. A `LOCKED` or `STALE` result is a conflict, not permission to retry with a new digest without reviewing the intervening change.
