#!/usr/bin/env python3
"""
ensure-memory-fresh · rebuild .phantom/memory.db iff any indexed source is
newer than the DB (or the DB is missing). Idempotent and cheap: if nothing
changed, it prints `fresh` and returns immediately.

Called by the session-search skill before every query so the index is never
stale. Also safe to call from a Stop hook, a release script, or by hand.

Sources checked (mtime compared against .phantom/memory.db):
  session-log.md
  decisions.md
  .phantom/context-engine-events.jsonl
  brands/{slug}/learnings.json
  brands/{slug}/_snapshot.md
  brands/{slug}/session-state.md

Usage:
  python3 .skills/ensure-memory-fresh.py            # rebuild if stale
  python3 .skills/ensure-memory-fresh.py --check    # exit 0 if fresh, 1 if stale
  python3 .skills/ensure-memory-fresh.py --quiet    # silence `fresh`/`rebuilt` line
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def find_workspace_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / ".phantom" / "memory.db").is_file():
            return cur
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if (cur / "session-log.md").is_file() or (cur / "decisions.md").is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    print(f"[ensure-memory-fresh] ERROR: no workspace or R&D root found (from {start})",
          file=sys.stderr)
    sys.exit(1)


def sources_for(root: Path):
    yield root / "session-log.md"
    yield root / "decisions.md"
    yield root / ".phantom" / "context-engine-events.jsonl"
    brands_dir = root / "brands"
    if brands_dir.is_dir():
        for b in brands_dir.iterdir():
            if not b.is_dir() or b.name.startswith("_"):
                continue
            yield b / "learnings.json"
            yield b / "_snapshot.md"
            yield b / "session-state.md"


def is_stale(root: Path) -> bool:
    db = root / ".phantom" / "memory.db"
    if not db.is_file():
        return True
    db_mtime = db.stat().st_mtime
    for src in sources_for(root):
        if src.is_file() and src.stat().st_mtime > db_mtime:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(prog="ensure-memory-fresh")
    ap.add_argument("--check", action="store_true",
                    help="exit 0 if fresh, 1 if stale (no rebuild)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    root = find_workspace_root(Path(args.cwd))
    stale = is_stale(root)

    if args.check:
        if not args.quiet:
            print("stale" if stale else "fresh")
        sys.exit(1 if stale else 0)

    if not stale:
        if not args.quiet:
            print("[ensure-memory-fresh] fresh")
        return

    indexer = root / ".skills" / "memory-index.py"
    if not indexer.is_file():
        print(f"[ensure-memory-fresh] ERROR: indexer not found at {indexer}", file=sys.stderr)
        sys.exit(1)
    r = subprocess.run([sys.executable, str(indexer), "--cwd", str(root)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    if not args.quiet:
        print("[ensure-memory-fresh] rebuilt")


if __name__ == "__main__":
    main()
