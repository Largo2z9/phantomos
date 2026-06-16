#!/usr/bin/env python3
"""
memory-index · rebuild the SQLite FTS5 retrieval index over the narrative layer.

Scope · the NARRATIVE memory layer only. Indexes derived chunks from the
source files that already exist. Never writes back to any source. The index
lives at `{workspace}/.phantom/memory.db` and is fully re-buildable from the
source files at any time · if it gets corrupt, delete and rerun.

Sources indexed (when present):
  session-log.md        → one chunk per '## Session S##' section
  decisions.md          → one chunk per '| \\d+ |' table row
  brands/{slug}/learnings.json  → one chunk per entries[]
  brands/{slug}/_snapshot.md    → one chunk (the full snapshot)
  brands/{slug}/session-state.md → one chunk per Activity Log line
  .phantom/context-engine-events.jsonl → one chunk per event (write / refused)

Usage:
  python3 .skills/memory-index.py           # rebuild from scratch
  python3 .skills/memory-index.py --stats   # summary of indexed counts
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def find_workspace_root(start: Path) -> Path:
    """Walk up from `start` looking for a PhantomOS workspace OR an R&D project
    with narrative sources at its root. A workspace has brands/ + resources/.
    An R&D root has session-log.md or decisions.md."""
    cur = start.resolve()
    for _ in range(8):
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if (cur / "session-log.md").is_file() or (cur / "decisions.md").is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    print(f"[memory-index] ERROR: no workspace or R&D root found (from {start})", file=sys.stderr)
    sys.exit(1)


def stable_id(source_type: str, source_ref: str) -> str:
    return hashlib.sha256(f"{source_type}::{source_ref}".encode()).hexdigest()[:16]


def open_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.executescript("""
        DROP TABLE IF EXISTS memory_fts;
        DROP TABLE IF EXISTS memory_chunks;

        CREATE TABLE memory_chunks (
            id            TEXT PRIMARY KEY,
            source_type   TEXT NOT NULL,
            source_ref    TEXT NOT NULL,
            title         TEXT,
            content       TEXT NOT NULL,
            date          TEXT,
            brand_slug    TEXT,
            file_path     TEXT,
            indexed_at    TEXT NOT NULL
        );

        CREATE INDEX idx_memory_type ON memory_chunks(source_type);
        CREATE INDEX idx_memory_brand ON memory_chunks(brand_slug);
        CREATE INDEX idx_memory_date ON memory_chunks(date);

        CREATE VIRTUAL TABLE memory_fts USING fts5(
            title, content, source_ref,
            content='memory_chunks',
            content_rowid='rowid'
        );
    """)
    return con


def insert_chunk(con, source_type, source_ref, title, content, date=None,
                 brand_slug=None, file_path=None):
    if not content or not content.strip():
        return
    cid = stable_id(source_type, source_ref)
    con.execute(
        "INSERT OR REPLACE INTO memory_chunks "
        "(id, source_type, source_ref, title, content, date, brand_slug, file_path, indexed_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (cid, source_type, source_ref, title or "", content,
         date, brand_slug, file_path, datetime.utcnow().isoformat() + "Z"),
    )


def rebuild_fts(con):
    con.executescript("""
        INSERT INTO memory_fts (rowid, title, content, source_ref)
        SELECT rowid, title, content, source_ref FROM memory_chunks;
    """)


# -- Source parsers --------------------------------------------------------

SESSION_HEADER_RE = re.compile(r"^##\s+Session\s+(S?\d+[a-z0-9\-]*)\b(.*)$", re.MULTILINE)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def index_session_log(con, path: Path):
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    matches = list(SESSION_HEADER_RE.finditer(text))
    count = 0
    for i, m in enumerate(matches):
        ref = m.group(1)
        header = m.group(0).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        date_m = DATE_RE.search(header) or DATE_RE.search(body[:500])
        date = date_m.group(1) if date_m else None
        insert_chunk(con, "session", ref, header.lstrip("# ").strip(),
                     body, date=date, file_path=str(path))
        count += 1
    return count


DECISION_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*([\d\-]+)?\s*\|\s*(.+?)\s*\|$",
    re.MULTILINE,
)


def index_decisions(con, path: Path):
    """Parse markdown table rows. Tolerates bolded or plain titles."""
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    count = 0
    for m in DECISION_ROW_RE.finditer(text):
        num, title, date, body = m.group(1), m.group(2), m.group(3), m.group(4)
        # Strip leading/trailing **…** on the title if present.
        title_clean = title.strip()
        if title_clean.startswith("**") and title_clean.endswith("**"):
            title_clean = title_clean[2:-2].strip()
        # Skip header separator rows (all dashes/pipes).
        if not title_clean or set(title_clean) <= set("-· "):
            continue
        ref = f"D#{num}"
        content = f"{title_clean}\n\n{body.strip()}"
        insert_chunk(con, "decision", ref, title_clean, content,
                     date=(date or "").strip() or None, file_path=str(path))
        count += 1
    return count


def index_learnings(con, brand_slug: str, path: Path):
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0
    entries = data.get("entries")
    if not isinstance(entries, list):
        return 0
    count = 0
    for e in entries:
        if not isinstance(e, dict):
            continue
        ref = f"{brand_slug}:{e.get('id') or stable_id('learning', json.dumps(e, sort_keys=True))}"
        title = e.get("fact") or e.get("title") or ""
        parts = []
        for k in ("fact", "reasoning", "why", "context", "impact", "source", "mode"):
            v = e.get(k)
            if v:
                parts.append(f"{k}: {v}")
        content = "\n".join(parts)
        date = e.get("date") or e.get("logged_at") or e.get("created_at")
        insert_chunk(con, "learning", ref, title[:120], content,
                     date=date, brand_slug=brand_slug, file_path=str(path))
        count += 1
    return count


def index_snapshot(con, brand_slug: str, path: Path):
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    insert_chunk(con, "snapshot", f"{brand_slug}:snapshot",
                 f"Snapshot · {brand_slug}", text,
                 brand_slug=brand_slug, file_path=str(path))
    return 1


SESSION_STATE_ENTRY_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2})\]\s+(.+)$", re.MULTILINE)


def index_session_state(con, brand_slug: str, path: Path):
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    count = 0
    for i, m in enumerate(SESSION_STATE_ENTRY_RE.finditer(text)):
        date, body = m.group(1), m.group(2).strip()
        ref = f"{brand_slug}:state:{date}:{i}"
        insert_chunk(con, "session_state", ref, body[:120], body,
                     date=date, brand_slug=brand_slug, file_path=str(path))
        count += 1
    return count


def index_events(con, path: Path):
    if not path.exists():
        return 0
    count = 0
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            ref = f"event:{i}"
            ts = (e.get("ts") or "")[:10] or None
            op = e.get("op") or "?"
            ep = e.get("path") or ""
            title = f"{op} {ep}"
            content = json.dumps(e, ensure_ascii=False, indent=2)
            brand = None
            if ep.startswith("brands/"):
                brand = ep.split("/")[1]
            insert_chunk(con, "event", ref, title, content,
                         date=ts, brand_slug=brand, file_path=str(path))
            count += 1
    return count


# Resource indexing · covers resources/{type}/*.md and *.json.
# Frontmatter YAML optional, parsed if present for title/description hints.
# Chunks markdown by '## ' headings; files < 2KB or with no headings = 1 chunk.

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def _parse_frontmatter_min(text: str) -> tuple:
    """Return (metadata_dict, body_text). Minimal YAML-ish parser · only
    top-level `name: value` and `name: [items]` patterns. Avoids adding a
    yaml dependency to the workspace."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    block = m.group(1)
    body = text[m.end():]
    meta = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip("'\"")
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        meta[key] = val
    return meta, body


def _chunk_markdown(body: str, max_chunk_chars: int = 4000):
    """Split markdown body by '## ' headings. Small bodies return one chunk."""
    if len(body) < 2000:
        return [("", body.strip())]
    headings = list(HEADING_RE.finditer(body))
    if not headings:
        return [("", body.strip())]
    chunks = []
    # Content before first heading (intro) = one chunk if non-empty.
    intro = body[: headings[0].start()].strip()
    if intro:
        chunks.append(("intro", intro))
    for i, h in enumerate(headings):
        title = h.group(1).strip()
        start = h.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
        section = body[start:end].strip()
        if section:
            # Truncate very large sections to keep index manageable.
            if len(section) > max_chunk_chars:
                section = section[:max_chunk_chars] + "…"
            chunks.append((title, section))
    return chunks


RESOURCE_TYPES = ("frameworks", "guides", "catalogues", "sops",
                  "conventions", "quality-specs", "templates", "routing")


def index_resources(con, root: Path):
    """Walk resources/{type}/ and index each file's chunks. resource_type is
    derived from the parent folder name. No tagging or metadata required on
    the operator side · indexation is purely content-driven."""
    resources_dir = root / "resources"
    if not resources_dir.is_dir():
        return 0
    count = 0
    for rtype in RESOURCE_TYPES:
        type_dir = resources_dir / rtype
        if not type_dir.is_dir():
            continue
        for f in type_dir.rglob("*"):
            if not f.is_file():
                continue
            if f.name.startswith(("_", ".")) or f.name == "README.md":
                continue
            if f.suffix not in (".md", ".json"):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue

            # Parse frontmatter if markdown.
            meta, body = ({}, text) if f.suffix == ".json" else _parse_frontmatter_min(text)
            doc_title = (meta.get("name") if isinstance(meta.get("name"), str) else None) or f.stem
            doc_desc = meta.get("description") if isinstance(meta.get("description"), str) else ""

            rel = str(f.relative_to(root))
            date = datetime.utcfromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")

            # JSON → one chunk with full content; markdown → chunk by heading.
            if f.suffix == ".json":
                content = text if len(text) < 4000 else text[:4000] + "…"
                ref = f"resource:{rtype}:{f.stem}"
                chunk_content = (doc_desc + "\n\n" + content).strip() if doc_desc else content
                insert_chunk(con, "resource", ref, f"[{rtype}] {doc_title}",
                             chunk_content, date=date, file_path=rel)
                count += 1
                continue

            chunks = _chunk_markdown(body)
            for i, (section_title, section_body) in enumerate(chunks):
                ref = f"resource:{rtype}:{f.stem}:{i}"
                full_title = f"[{rtype}] {doc_title}"
                if section_title:
                    full_title += f" / {section_title}"
                # Prepend description to first chunk for better ranking signal.
                chunk_content = section_body
                if i == 0 and doc_desc:
                    chunk_content = f"{doc_desc}\n\n{section_body}"
                insert_chunk(con, "resource", ref, full_title,
                             chunk_content, date=date, file_path=rel)
                count += 1
    return count


# -- Driver ----------------------------------------------------------------


def build(root: Path) -> dict:
    db_path = root / ".phantom" / "memory.db"
    con = open_db(db_path)
    stats = {}
    with con:
        stats["session"] = index_session_log(con, root / "session-log.md")
        stats["decision"] = index_decisions(con, root / "decisions.md")
        stats["event"] = index_events(con, root / ".phantom" / "context-engine-events.jsonl")
        stats["learning"] = 0
        stats["snapshot"] = 0
        stats["session_state"] = 0
        brands_dir = root / "brands"
        if brands_dir.is_dir():
            for b in brands_dir.iterdir():
                if not b.is_dir() or b.name.startswith("_"):
                    continue
                stats["learning"] += index_learnings(con, b.name, b / "learnings.json")
                stats["snapshot"] += index_snapshot(con, b.name, b / "_snapshot.md")
                stats["session_state"] += index_session_state(con, b.name, b / "session-state.md")
        stats["resource"] = index_resources(con, root)
        rebuild_fts(con)
    con.close()
    return stats


def main():
    ap = argparse.ArgumentParser(prog="memory-index")
    ap.add_argument("--stats", action="store_true", help="print counts and exit")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    root = find_workspace_root(Path(args.cwd))
    stats = build(root)
    total = sum(stats.values())
    print(f"[memory-index] rebuilt {root / '.phantom' / 'memory.db'}")
    for k, v in stats.items():
        print(f"  {k:16s} {v:>6d}")
    print(f"  {'total':16s} {total:>6d}")


if __name__ == "__main__":
    main()
