#!/usr/bin/env python3
"""
phantom-search · cross-brand keyword search across context entities.

Searches case-insensitively across:
  - brands/{slug}/brand.json (meta.name, identity, positioning, tone fields)
  - brands/{slug}/products/*/spec.json (meta.name, identity, description)
  - brands/{slug}/audiences/*/profile.json (meta.name, identity.description, voice.key_expressions[].text, pain_points[].formulation, benefits[].formulation, objections[].formulation)
  - brands/{slug}/angles/*.json or angles.json (name, audience_target, status)
  - brands/{slug}/learnings.json (entries[].fact, entries[].reasoning)
  - brands/{slug}/strategy.json (current_focus, goals)

Used by the /phantom search mode.

Usage:
    python3 .skills/phantom-search.py "keyword"

Output: JSON array on stdout, capped at 20 results, ordered by match strength:
    [{path, type, brand_slug, snippet, slug}]

Exit codes:
    0  success (empty array if no matches)
    1  workspace root not found OR no keyword
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


MAX_RESULTS = 20
SNIPPET_LEN = 120


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(10):
        if (cur / ".skills").is_dir() and (cur / "brands").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def safe_load(path: Path) -> dict | None:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def make_snippet(text: str, kw_re: re.Pattern, length: int = SNIPPET_LEN) -> str:
    if not text:
        return ""
    m = kw_re.search(text)
    if not m:
        return text[:length] + ("..." if len(text) > length else "")
    start = max(0, m.start() - length // 3)
    end = min(len(text), m.end() + length // 2)
    snippet = text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet.replace("\n", " ").strip()


def collect_text_fields(doc, prefix: str = "") -> list[tuple[str, str]]:
    """Walk a JSON doc, return [(path, text)] for every string leaf.
    Includes string elements inside arrays (e.g. meta.applies_to_products[]
    so /phantom search finds audiences by product slug).
    """
    out = []
    if isinstance(doc, dict):
        for k, v in doc.items():
            if k.startswith("_") or k.startswith("$"):
                continue
            out.extend(collect_text_fields(v, f"{prefix}/{k}" if prefix else k))
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            out.extend(collect_text_fields(v, f"{prefix}[{i}]"))
    elif isinstance(doc, str) and doc.strip():
        out.append((prefix, doc))
    return out


def search_file(path: Path, kw_re: re.Pattern, brand_slug: str, type_label: str, slug_hint: str | None = None) -> list[dict]:
    doc = safe_load(path)
    if doc is None:
        return []
    matches = []
    for field_path, text in collect_text_fields(doc):
        if kw_re.search(text):
            matches.append({
                "path": str(path),
                "type": type_label,
                "brand_slug": brand_slug,
                "slug": slug_hint or doc.get("meta", {}).get("slug") if isinstance(doc, dict) else slug_hint,
                "field": field_path,
                "snippet": make_snippet(text, kw_re),
            })
    return matches


def search_workspace(root: Path, keyword: str) -> list[dict]:
    kw_re = re.compile(re.escape(keyword), re.IGNORECASE)
    results = []
    brands_dir = root / "brands"
    if not brands_dir.is_dir():
        return results

    for brand_dir in sorted(brands_dir.iterdir()):
        if not brand_dir.is_dir() or brand_dir.name.startswith("_"):
            continue
        brand_slug = brand_dir.name

        brand_json = brand_dir / "brand.json"
        if brand_json.exists():
            results.extend(search_file(brand_json, kw_re, brand_slug, "brand", brand_slug))

        for spec in (brand_dir / "products").glob("*/spec.json") if (brand_dir / "products").is_dir() else []:
            results.extend(search_file(spec, kw_re, brand_slug, "product", spec.parent.name))

        for profile in (brand_dir / "audiences").glob("*/profile.json") if (brand_dir / "audiences").is_dir() else []:
            results.extend(search_file(profile, kw_re, brand_slug, "audience", profile.parent.name))

        learnings = brand_dir / "learnings.json"
        if learnings.exists():
            results.extend(search_file(learnings, kw_re, brand_slug, "learning"))

        strategy = brand_dir / "strategy.json"
        if strategy.exists():
            results.extend(search_file(strategy, kw_re, brand_slug, "strategy"))

        angles_dir = brand_dir / "angles"
        if angles_dir.is_dir():
            for angle_file in angles_dir.glob("*.json"):
                results.extend(search_file(angle_file, kw_re, brand_slug, "angle", angle_file.stem))

        if len(results) >= MAX_RESULTS * 3:
            break

    return results[:MAX_RESULTS]


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print(json.dumps({"error": "keyword required"}), file=sys.stderr)
        sys.exit(1)

    keyword = sys.argv[1].strip()
    root = find_workspace_root(Path.cwd())
    if root is None:
        print(json.dumps({"error": "workspace root not found"}), file=sys.stderr)
        sys.exit(1)

    results = search_workspace(root, keyword)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
