#!/usr/bin/env python3
"""Replace one continuity record atomically with stale-write protection."""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import shutil
import tempfile


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


parser = argparse.ArgumentParser()
parser.add_argument("target", type=pathlib.Path)
parser.add_argument("replacement", type=pathlib.Path)
parser.add_argument("--expect-sha256", required=True, help="Current target digest, or 'missing'")
args = parser.parse_args()
target = args.target.resolve()
replacement = args.replacement.resolve()
target.parent.mkdir(parents=True, exist_ok=True)
lock = target.with_name(f".{target.name}.lock")

try:
    lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
except FileExistsError:
    raise SystemExit(f"LOCKED: another update owns {lock}")

try:
    with os.fdopen(lock_fd, "w", encoding="utf-8") as handle:
        handle.write(f"pid={os.getpid()}\n")
    actual = digest(target)
    if actual != args.expect_sha256:
        raise SystemExit(f"STALE: expected {args.expect_sha256}, found {actual}")
    if not replacement.is_file():
        raise SystemExit(f"INVALID: replacement is not a file: {replacement}")
    if target.exists():
        shutil.copy2(target, target.with_suffix(target.suffix + ".bak"))
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", delete=False) as handle:
        temporary = pathlib.Path(handle.name)
        handle.write(replacement.read_bytes())
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)
    print(f"UPDATED {target} sha256={digest(target)}")
finally:
    lock.unlink(missing_ok=True)
