#!/usr/bin/env python3
"""
session-search · query the narrative memory index.

Reads `{workspace}/.phantom/memory.db` (built by memory-index.py). Runs an
FTS5 MATCH over the title + content + source_ref of every indexed chunk.
Returns ranked results with source, date, brand slug, and a short snippet.

Usage:
  python3 .skills/session-search.py --query "{topic}"
  python3 .skills/session-search.py --query "mutation gate" --type decision
  python3 .skills/session-search.py --query "{topic}" --brand {slug}
  python3 .skills/session-search.py --query "security scan" --since 2026-04-20
  python3 .skills/session-search.py --query "{topic}" --format json --limit 5

Exit codes:
  0  any results returned (even 0 hits · intentional; grep for `hits: 0` in output)
  1  arg / IO error, or index missing
  2  FTS5 syntax error in --query
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

VALID_TYPES = {"session", "decision", "learning", "snapshot", "session_state", "event"}


def die(msg, code=1):
    print(f"[session-search] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


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
    die(f"no workspace or R&D root found (from {start})")


def fts_escape(q: str) -> str:
    """Quote the user query for FTS5 MATCH · protects against bare tokens that
    collide with FTS5 syntax (e.g. dots, dashes, colons in slugs)."""
    q = q.strip().replace('"', '""')
    if not q:
        die("empty --query", 1)
    return f'"{q}"'


def main():
    ap = argparse.ArgumentParser(prog="session-search")
    ap.add_argument("--query", required=True)
    ap.add_argument("--type", choices=sorted(VALID_TYPES), default=None)
    ap.add_argument("--brand", default=None)
    ap.add_argument("--since", default=None, help="ISO date YYYY-MM-DD, inclusive")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    root = find_workspace_root(Path(args.cwd))
    db = root / ".phantom" / "memory.db"
    if not db.exists():
        die(f"index not found at {db} · run '.skills/memory-index.py' first")

    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row

    where = ["memory_fts MATCH ?"]
    params: list = [fts_escape(args.query)]
    if args.type:
        where.append("c.source_type = ?")
        params.append(args.type)
    if args.brand:
        where.append("c.brand_slug = ?")
        params.append(args.brand)
    if args.since:
        where.append("(c.date IS NULL OR c.date >= ?)")
        params.append(args.since)
    params.append(args.limit)

    sql = (
        "SELECT c.source_type, c.source_ref, c.title, c.date, c.brand_slug, "
        "       c.file_path, snippet(memory_fts, 1, '[', ']', '…', 18) AS snippet, "
        "       bm25(memory_fts) AS score "
        "FROM memory_fts "
        "JOIN memory_chunks c ON c.rowid = memory_fts.rowid "
        f"WHERE {' AND '.join(where)} "
        "ORDER BY score LIMIT ?"
    )
    try:
        rows = con.execute(sql, params).fetchall()
    except sqlite3.OperationalError as e:
        die(f"FTS5 query error: {e}", 2)

    results = [
        {
            "type": r["source_type"],
            "ref": r["source_ref"],
            "title": r["title"],
            "date": r["date"],
            "brand": r["brand_slug"],
            "snippet": r["snippet"],
            "file": r["file_path"],
        }
        for r in rows
    ]

    if args.format == "json":
        print(json.dumps({"query": args.query, "hits": len(results), "results": results},
                         ensure_ascii=False, indent=2))
        return

    print(f"query: {args.query!r}   hits: {len(results)}")
    if not results:
        return
    for i, r in enumerate(results, 1):
        brand = f" [{r['brand']}]" if r["brand"] else ""
        date = r["date"] or "·"
        print(f"\n{i}. {r['type']:>6} {r['ref']}{brand}   {date}")
        if r["title"]:
            print(f"   {r['title'][:100]}")
        print(f"   {r['snippet'][:200]}")
        print(f"   → {r['file']}")


if __name__ == "__main__":
    main()
