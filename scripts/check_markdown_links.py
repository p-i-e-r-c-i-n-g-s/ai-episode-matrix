#!/usr/bin/env python3
"""Fail closed when a Markdown link points at a missing local file."""
import pathlib
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
errors = []
pattern = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
for path in sorted(ROOT.rglob("*.md")):
    if any(part in {".git", "__pycache__"} for part in path.parts):
        continue
    for target in pattern.findall(path.read_text(errors="replace")):
        target = target.strip().split()[0].strip("<>")
        parsed = urlparse(target)
        if parsed.scheme or target.startswith("#"):
            continue
        local = (path.parent / unquote(parsed.path)).resolve()
        if not local.exists():
            errors.append(f"MISSING {path.relative_to(ROOT)} -> {target}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("Markdown links are valid")
