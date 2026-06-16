#!/usr/bin/env python3
"""
phantom-recent · read the last N mutations from context-engine-events.jsonl.

Reads `.phantom/context-engine-events.jsonl` (canonical event log written by
write-to-context.py) and returns the last N events as a JSON array. Used by
the /phantom recent mode.

Usage:
    python3 .skills/phantom-recent.py [N]    # default N=10, max N=50

Output: JSON array on stdout, one entry per event:
    {ts, brand_slug, entity, action, source, confidence, mode, reason, path}

brand_slug and entity are derived from the event's `path` field
(e.g. "brands/karacare/audiences/chute-active/profile.json#/meta/name"
yields brand_slug="karacare", entity="audiences/chute-active").

Exit codes:
    0  success (always returns valid JSON, even empty)
    1  workspace root not found
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


MAX_N = 50
DEFAULT_N = 10


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(10):
        if (cur / ".skills").is_dir() and (cur / "brands").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def parse_path(path: str) -> tuple[str | None, str | None]:
    """Extract brand_slug and entity descriptor from event path."""
    rel = path.split("#", 1)[0]
    parts = rel.split("/")
    if len(parts) >= 2 and parts[0] == "brands":
        brand_slug = parts[1]
        if len(parts) >= 4 and parts[2] in {"products", "audiences", "angles"}:
            entity = f"{parts[2]}/{parts[3]}"
        elif len(parts) >= 3:
            entity = parts[2].replace(".json", "")
        else:
            entity = "(brand)"
        return brand_slug, entity
    if len(parts) >= 1 and parts[0] == "operator":
        return None, "operator"
    return None, rel


def tail_events(log_path: Path, n: int) -> list[dict]:
    if not log_path.exists():
        return []
    try:
        with log_path.open("rb") as f:
            f.seek(0, 2)
            size = f.tell()
            chunk = min(size, 65536 * max(1, n // 50 + 1))
            f.seek(max(0, size - chunk))
            tail = f.read().decode("utf-8", errors="replace")
    except OSError:
        return []
    lines = [ln for ln in tail.split("\n") if ln.strip()]
    events = []
    for ln in lines[-n:]:
        try:
            events.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return events


def main():
    n = DEFAULT_N
    if len(sys.argv) > 1:
        try:
            n = max(1, min(MAX_N, int(sys.argv[1])))
        except ValueError:
            pass

    root = find_workspace_root(Path.cwd())
    if root is None:
        print(json.dumps({"error": "workspace root not found"}), file=sys.stderr)
        sys.exit(1)

    log_path = root / ".phantom" / "context-engine-events.jsonl"
    events = tail_events(log_path, n)

    out = []
    for ev in events:
        brand_slug, entity = parse_path(ev.get("path", ""))
        out.append({
            "ts": ev.get("ts"),
            "brand_slug": brand_slug,
            "entity": entity,
            "action": ev.get("op"),
            "source": ev.get("source"),
            "confidence": ev.get("confidence"),
            "mode": ev.get("mode"),
            "reason": ev.get("reason"),
            "path": ev.get("path"),
        })

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
