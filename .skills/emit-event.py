#!/usr/bin/env python3
"""
Thin primitive · append a structured event to the workspace audit trail.

Used by sub-skills (validate-output-coherence, validate-resources, ...) that
need to record they ran without going through the mutation pipeline (which is
reserved for entity JSON writes under brands/ or operator/).

Writes to `<workspace_root>/.phantom/context-engine-events.jsonl`, the same
channel used by write-to-context, convention-guard, mutation-guard. Hooks
(turn-end-audit) read this log to confirm sub-skill invocation.

Usage:
    python3 .skills/emit-event.py \\
        --kind coherence_check \\
        --payload '{"brand_slug":"acme","ok":true,"warnings":1,"blocking":0}'

Exit codes:
    0 · event appended
    1 · bad args or workspace root not found
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

VALID_KINDS = {
    "coherence_check",
    "resource_validation",
    "skill_invocation",
}


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(12):
        if (cur / "brands").is_dir() and (cur / ".skills").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def main() -> int:
    ap = argparse.ArgumentParser(prog="emit-event")
    ap.add_argument("--kind", required=True, choices=sorted(VALID_KINDS))
    ap.add_argument("--payload", required=True,
                    help="JSON-encoded dict (brand_slug, ok, counts, etc.)")
    ap.add_argument("--source", default="skill",
                    help="Who emitted (default: skill)")
    args = ap.parse_args()

    try:
        payload = json.loads(args.payload)
        if not isinstance(payload, dict):
            raise ValueError("payload must be a JSON object")
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"[emit-event] invalid --payload: {exc}", file=sys.stderr)
        return 1

    root_str = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(root_str) if root_str else find_workspace_root(Path.cwd())
    if root is None:
        print("[emit-event] workspace root not found", file=sys.stderr)
        return 1

    log_dir = root / ".phantom"
    log_dir.mkdir(exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "type": args.kind,
        "source": args.source,
        "payload": payload,
    }
    with (log_dir / "context-engine-events.jsonl").open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[emit-event] OK {args.kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
