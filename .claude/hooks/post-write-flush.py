#!/usr/bin/env python3
"""
PostToolUse hook · flush brand status after any write-to-context call.

Wiring: matches `Bash` tool. If the executed command invokes
`.skills/write-to-context.py --path brands/{slug}/...`, extract {slug} and
synchronously run `.skills/refresh-brand-status.py {slug}` to recompute
completeness + wedge_complete + last_activity.

Replaces the SKILL.md instruction "trigger validate-resources silently after
save" which depended on the agent remembering. Now mechanical: every
successful write automatically flushes status.

Silent on success. Emits stderr only on hard error (so Largo sees it).
No-op on any Bash call that doesn't touch a brand.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

BRAND_PATH = re.compile(r"brands/([A-Za-z0-9_-]+)/", re.IGNORECASE)
WRITE_CTX = re.compile(r"write-to-context\.py\b")


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(12):
        if (cur / "brands").is_dir() and (cur / ".skills").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = (data.get("tool_input") or {}).get("command") or ""
    if not WRITE_CTX.search(cmd):
        sys.exit(0)

    match = BRAND_PATH.search(cmd)
    if not match:
        sys.exit(0)

    slug = match.group(1)
    if slug.startswith("_"):
        sys.exit(0)

    root_str = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(root_str) if root_str else find_workspace_root(Path.cwd())
    if root is None:
        sys.exit(0)

    refresh = root / ".skills" / "refresh-brand-status.py"
    if not refresh.is_file():
        sys.exit(0)

    try:
        subprocess.run(
            ["python3", str(refresh), slug],
            cwd=str(root),
            capture_output=True,
            timeout=5,
            check=False,
        )
    except Exception as e:
        print(f"[post-write-flush] refresh failed for {slug}: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
