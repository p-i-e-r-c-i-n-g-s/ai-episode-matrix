#!/usr/bin/env python3
"""Portable CI validation for the skill entrypoint."""
from __future__ import annotations

import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
skill = root / "SKILL.md"
errors: list[str] = []
if not skill.is_file():
    errors.append("MISSING SKILL.md")
else:
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append("INVALID SKILL.md: missing YAML frontmatter")
    else:
        frontmatter = match.group(1)
        if not re.search(r"^name:\s*ai-episode-matrix\s*$", frontmatter, re.MULTILINE):
            errors.append("INVALID SKILL.md: unexpected or missing name")
        if not re.search(r"^description:\s*\S.+$", frontmatter, re.MULTILINE):
            errors.append("INVALID SKILL.md: description is required")
    if any(token in text for token in ("TODO", "[TODO]", "{{placeholder}}")):
        errors.append("INVALID SKILL.md: unfinished scaffold marker")
metadata = root / "agents/openai.yaml"
if not metadata.is_file():
    errors.append("MISSING agents/openai.yaml")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("Skill package is valid")
