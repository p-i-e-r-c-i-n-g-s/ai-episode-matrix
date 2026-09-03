# Continuity file versioning and migrations

Continuity records use an integer `schema_version`. New starter files are version 1. A record is not safe to load when its version is missing, unsupported, or newer than the validator understands.

Migration policy:

1. Make migrations deterministic and additive where possible.
2. Never overwrite the source record in place; write a `.bak` or a new versioned copy first.
3. Preserve unknown fields and record `migrated_from`, `migrated_at`, and the tool version.
4. Validate the migrated output before it becomes the active checkpoint.
5. Only approved continuity state propagates after migration; proposed or unresolved changes remain flagged.

When schema 2 is introduced, provide a named migration such as `v1_to_v2`, a fixture for both versions, and a rollback note. Until that migration exists, the scanner must reject version 2 rather than silently guessing.
