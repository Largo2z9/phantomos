#!/usr/bin/env python3
"""Rebuild index.json from the resources/ filesystem (filesystem = source of truth).

Covers the 7 typed resource folders declared in index.schema.json. Registries,
canon/ and concepts/ are intentionally out of scope: they are not part of the
index enum (extending the enum is a schema decision, not an indexing one).

Usage (from workspace-template root):
  python3 resources/scripts/rebuild-index.py            # rebuild and write index.json
  python3 resources/scripts/rebuild-index.py --check    # dry-run, exit 1 if index drifts from filesystem

Run after seeding or removing template-side resources, and at every release
(pre-release gate companion). Operator-side, ingest-resource and
validate-resources maintain the same file incrementally.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
RESOURCES = ROOT / "resources"
INDEX = ROOT / "index.json"

FOLDER_TYPE = {
    "catalogues": "catalogue",
    "routing": "routing",
    "frameworks": "framework",
    "sops": "sop",
    "quality-specs": "quality-spec",
    "conventions": "convention",
    "templates": "template",
}

# Domain overrides by resource id. Default: general.
DOMAIN = {
    "awareness-angle-matrix": "creative",
    "hook-quality-spec": "creative",
    "paid-angle-scoring": "creative",
    "paid-angle-scoring-weights": "creative",
    "cross-brand-curation": "creative",
    "perf-feedback-loop": "creative",
    "creative-formula": "creative",
    "hook-formulas": "creative",
    "creative-storage": "ops",
    "audit-meta-global": "media",
    "google-ads": "media",
    "meta-ads": "media",
    "tiktok-ads": "media",
    "campaigns-active": "media",
    "klaviyo": "retention",
    "ga4": "ops",
    "shopify": "ops",
    "triplewhale": "ops",
}


def git_dates(path: Path):
    """(created, updated) from git history, fallback to today."""
    try:
        out = subprocess.run(
            ["git", "log", "--follow", "--format=%ad", "--date=short", "--", str(path)],
            capture_output=True, text=True, cwd=ROOT, check=True,
        ).stdout.split()
        if out:
            return out[-1], out[0]
    except Exception:
        pass
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return today, today


def title_of(path: Path):
    if path.suffix == ".md":
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    elif path.suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            meta = data.get("meta", {}) if isinstance(data, dict) else {}
            for key in ("name", "platform", "title"):
                if isinstance(meta.get(key), str):
                    return meta[key]
                if isinstance(data, dict) and isinstance(data.get(key), str):
                    return data[key]
        except Exception:
            pass
    return path.stem


def step_count_of(path: Path):
    if path.suffix != ".md":
        return None
    steps = re.findall(r"^#{2,3}\s+(?:Step|Étape|Etape)\s+\d+", path.read_text(encoding="utf-8"), re.M)
    return len(steps) or None


def build_entries():
    entries = []
    for folder, rtype in FOLDER_TYPE.items():
        base = RESOURCES / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if path.name.startswith(("_", ".")) or path.name in ("README.md", ".gitkeep"):
                continue
            rid = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
            created, updated = git_dates(path)
            tags = sorted(set(t for t in re.split(r"[^a-z0-9]+", path.stem.lower()) if len(t) > 2) | {folder.rstrip("s")})
            entry = {
                "id": rid,
                "type": rtype,
                "path": str(path.relative_to(ROOT)),
                "domain": DOMAIN.get(rid, "general"),
                "title": title_of(path),
                "created": created,
                "updated": updated,
                "tags": tags,
            }
            if rtype == "sop":
                entry["step_count"] = step_count_of(path)
            entries.append(entry)
    return entries


def main():
    check = "--check" in sys.argv
    entries = build_entries()
    by_type = {t: 0 for t in FOLDER_TYPE.values()}
    for e in entries:
        by_type[e["type"]] += 1
    current = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {}
    index = {
        "$schema": "index.schema.json",
        "version": current.get("version", "1.0.0"),
        "last_updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stats": {"total_resources": len(entries), "by_type": by_type},
        "resources": entries,
        "id_prefixes": current.get("id_prefixes", {}),
    }
    try:
        import jsonschema
        jsonschema.validate(index, json.loads((ROOT / "index.schema.json").read_text()))
        print("✓ schema validation pass")
    except ImportError:
        print("○ jsonschema absent, validation skipped")
    if check:
        stale = current.get("stats", {}).get("total_resources") != len(entries) or {
            e["path"] for e in current.get("resources", [])
        } != {e["path"] for e in entries}
        print(("✗ index drift detected" if stale else "✓ index in sync") + f" · filesystem={len(entries)} indexed={current.get('stats', {}).get('total_resources')}")
        sys.exit(1 if stale else 0)
    INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✓ index.json rebuilt · {len(entries)} resources · " + " ".join(f"{k}:{v}" for k, v in by_type.items() if v))


if __name__ == "__main__":
    main()
