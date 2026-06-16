#!/usr/bin/env python3
"""
discover-resources · FTS5 search over indexed resources.

Skills call this primitive at runtime to find knowledge relevant to their
current context. Returns ranked chunks by BM25 with boost for recency and
matching resource_type. No tagging is required on resource files · indexing
is purely content-driven (see .skills/memory-index.py).

The canonical execution flow for a skill is:
  1. Load brand entity schemas (mandatory source of truth)
  2. Derive keywords from brand context + current task
  3. Call discover-resources with those keywords
  4. Confront primary reasoning with retrieved chunks
  5. Compose output, pass through validate-output-coherence

Usage:
  python3 .skills/discover-resources.py --query "supplements claims compliance"
  python3 .skills/discover-resources.py --query "audit creative diversity" --limit 3
  python3 .skills/discover-resources.py --query "..." --source-types framework,guide
  python3 .skills/discover-resources.py --query "..." --format json
  python3 .skills/discover-resources.py --query "..." --boost-recency

Exit codes:
  0  any result count (zero included · check `hits` in output)
  1  arg / IO error, missing index
  2  FTS5 query syntax error
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

RESOURCE_SUBTYPES = {
    "framework", "frameworks",
    "guide", "guides",
    "catalogue", "catalogues",
    "sop", "sops",
    "convention", "conventions",
    "quality-spec", "quality-specs",
    "template", "templates",
    "routing",
}


def die(msg, code=1):
    print(f"[discover-resources] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def find_workspace_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / ".phantom" / "memory.db").is_file():
            return cur
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    die(f"no workspace or R&D root found (from {start})")


def fts_escape(q: str) -> str:
    """Wrap query tokens for FTS5 MATCH. Avoids operators getting interpreted
    as DSL (e.g., bare `AND`/`OR`). Splits on whitespace, quotes each token
    that contains special characters, joins with implicit AND."""
    tokens = q.strip().split()
    if not tokens:
        die("empty --query", 1)
    safe = []
    for t in tokens:
        # Strip FTS5 operator chars from leading/trailing
        t = t.strip("^*+()\"'`:")
        if not t:
            continue
        # Very short tokens usually noise; let FTS5 decide with stemming
        if len(t) < 2:
            continue
        if any(c in t for c in "-.,;!?[]{}/"):
            t = '"' + t.replace('"', '""') + '"'
        safe.append(t)
    if not safe:
        die("query contains no valid tokens after sanitization", 1)
    return " ".join(safe)


def main():
    ap = argparse.ArgumentParser(prog="discover-resources")
    ap.add_argument("--query", required=True,
                    help="Natural keywords or phrases. Auto-tokenized for FTS5.")
    ap.add_argument("--source-types", default=None,
                    help="Comma-separated: framework,guide,catalogue,sop,convention,quality-spec,template. "
                         "Default = all resource subtypes.")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--min-score", type=float, default=None,
                    help="Drop results below this BM25 score (lower=better). Default: no filter.")
    ap.add_argument("--boost-recency", action="store_true",
                    help="Apply small rank boost to resources modified in the last 30 days.")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    root = find_workspace_root(Path(args.cwd))
    db = root / ".phantom" / "memory.db"
    if not db.is_file():
        die(f"index not found at {db} · run '.skills/memory-index.py' first")

    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row

    where = ["memory_fts MATCH ?", "c.source_type = 'resource'"]
    params: list = [fts_escape(args.query)]

    subtype_filter = None
    if args.source_types:
        subtypes = {s.strip().lower() for s in args.source_types.split(",") if s.strip()}
        unknown = subtypes - RESOURCE_SUBTYPES
        if unknown:
            die(f"unknown source_types: {unknown}")
        # Normalize to plural folder names used in source_ref
        canonical = set()
        for s in subtypes:
            canonical.add(s if s.endswith("s") else s + "s")
            # Handle quality-spec → quality-specs
        canonical = {c.replace("qualityspec", "quality-specs")
                       .replace("quality-spec", "quality-specs") for c in canonical}
        subtype_filter = canonical

    order_expr = "bm25(memory_fts)"
    if args.boost_recency:
        cutoff = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        # Lower (more negative) = better in BM25. Subtract small bonus for recent.
        order_expr = f"bm25(memory_fts) - CASE WHEN c.date >= '{cutoff}' THEN 0.5 ELSE 0 END"

    sql = (
        "SELECT c.source_ref, c.title, c.date, c.file_path, "
        "       snippet(memory_fts, 1, '[', ']', '…', 20) AS snippet, "
        "       bm25(memory_fts) AS score "
        "FROM memory_fts "
        "JOIN memory_chunks c ON c.rowid = memory_fts.rowid "
        f"WHERE {' AND '.join(where)} "
        f"ORDER BY {order_expr} "
        "LIMIT ?"
    )
    params.append(args.limit * 3)  # over-fetch to allow subtype filtering after

    try:
        rows = con.execute(sql, params).fetchall()
    except sqlite3.OperationalError as e:
        die(f"FTS5 query error: {e}", 2)

    results = []
    for r in rows:
        if subtype_filter:
            # source_ref format: "resource:{rtype}:{stem}[:chunk_idx]"
            parts = r["source_ref"].split(":", 2)
            if len(parts) >= 2 and parts[1] not in subtype_filter:
                continue
        if args.min_score is not None and r["score"] > args.min_score:
            # BM25 conventions: lower is better; > min_score means worse than threshold
            continue
        # Extract resource_type from source_ref
        rtype = r["source_ref"].split(":", 2)[1] if ":" in r["source_ref"] else "unknown"
        results.append({
            "resource_type": rtype,
            "ref": r["source_ref"],
            "title": r["title"],
            "date": r["date"],
            "file": r["file_path"],
            "snippet": r["snippet"],
            "score": round(r["score"], 3),
        })
        if len(results) >= args.limit:
            break

    if args.format == "json":
        print(json.dumps({"query": args.query, "hits": len(results), "results": results},
                         ensure_ascii=False, indent=2))
        return

    print(f"query: {args.query!r}   hits: {len(results)}")
    if not results:
        print("  (no matching resources · try broader keywords or drop --source-types filter)")
        return
    for i, r in enumerate(results, 1):
        print(f"\n{i}. [{r['resource_type']}] {r['ref']}   score={r['score']}   {r['date'] or '·'}")
        if r["title"]:
            print(f"   {r['title'][:100]}")
        print(f"   {r['snippet'][:220]}")
        print(f"   → {r['file']}")


if __name__ == "__main__":
    main()
