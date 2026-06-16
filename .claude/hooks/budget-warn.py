#!/usr/bin/env python3
"""
SessionStart hook · context budget warning.

Runs `.skills/audit-context-budget.py --json` at every session start. If any
threshold is breached (root CLAUDE.md > 140 lines, always-loaded > 250, lazy
doc > 200, worst-case session > 600), appends a warning to
`.phantom/context-budget-warnings.log` and emits a single-line stderr warning
the agent (and maintainer) can surface if asked.

Rationale · operators accumulate brand context, learnings, decisions over
weeks. The cascade balloons silently; prefix cache degrades; latency and
costs rise. Operator has no visibility. This hook surfaces the drift early
without blocking the session (soft enforcement · a hard block would fail a
legitimate session mid-action).

Does nothing if the audit tool is missing (older workspaces).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def find_workspace_root(start: Path):
    cur = start.resolve()
    for _ in range(8):
        if (cur / "CLAUDE.md").is_file() and (cur / "brands").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        sys.exit(0)

    cwd = Path(payload.get("cwd") or os.getcwd())
    root = find_workspace_root(cwd)
    if root is None:
        sys.exit(0)

    audit = root / ".skills" / "audit-context-budget.py"
    if not audit.is_file():
        sys.exit(0)

    try:
        r = subprocess.run(
            [sys.executable, str(audit), "--json", "--cwd", str(root)],
            capture_output=True, text=True, timeout=10,
        )
    except Exception:
        sys.exit(0)
    if r.returncode != 0 or not r.stdout:
        sys.exit(0)

    try:
        report = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(0)

    findings = report.get("findings") or []
    if not findings:
        sys.exit(0)

    # Log for maintainer audit trail.
    log_dir = root / ".phantom"
    log_dir.mkdir(exist_ok=True)
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "findings": findings,
        "always_loaded_lines": (report.get("always_loaded") or {}).get("lines"),
        "worst_case_lines": (report.get("worst_case_session") or {}).get("lines"),
    }
    with (log_dir / "context-budget-warnings.log").open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Single-line stderr warning · visible in tool output, non-blocking.
    lines = (report.get("always_loaded") or {}).get("lines") or 0
    worst = (report.get("worst_case_session") or {}).get("lines") or 0
    print(
        f"[budget-warn] context cascade above threshold · always-loaded={lines} lines, "
        f"worst-case={worst}. Run `python3 .skills/audit-context-budget.py` for detail.",
        file=sys.stderr,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
