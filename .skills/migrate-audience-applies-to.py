#!/usr/bin/env python3
"""
migrate-audience-applies-to · one-shot migration v2.24.0.

Walks every brands/{slug}/audiences/{audience}/profile.json. If `meta.product_id`
is present (non-null) AND `meta.applies_to_products` is missing or empty:
  - Set `meta.applies_to_products` = [meta.product_id]
  - Keep `meta.product_id` for backward compat (does not delete)

Idempotent. Safe to re-run.

Usage:
    python3 .skills/migrate-audience-applies-to.py [--dry-run]

Reports per audience: migrated / already-migrated / brand-wide / skipped.
Exit 0 always.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(10):
        if (cur / ".skills").is_dir() and (cur / "brands").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def main():
    dry_run = "--dry-run" in sys.argv

    root = find_workspace_root(Path.cwd())
    if root is None:
        print("ERROR: workspace root not found", file=sys.stderr)
        sys.exit(1)

    brands_dir = root / "brands"
    if not brands_dir.is_dir():
        print("No brands/ directory.")
        sys.exit(0)

    counts = {"migrated": 0, "already": 0, "brand_wide": 0, "skipped": 0, "no_product_id": 0}

    for brand_dir in sorted(brands_dir.iterdir()):
        if not brand_dir.is_dir() or brand_dir.name.startswith("_"):
            continue
        audiences_dir = brand_dir / "audiences"
        if not audiences_dir.is_dir():
            continue

        for prof_path in audiences_dir.glob("*/profile.json"):
            if prof_path.parent.name.startswith("_"):
                continue
            try:
                with prof_path.open("r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, json.JSONDecodeError) as e:
                print(f"  SKIP {prof_path}: {e}")
                counts["skipped"] += 1
                continue

            meta = doc.setdefault("meta", {})
            existing = meta.get("applies_to_products")
            product_id = meta.get("product_id")

            if existing is not None and len(existing) > 0:
                counts["already"] += 1
                print(f"  ALREADY {brand_dir.name}/{prof_path.parent.name}: applies_to_products={existing}")
                continue

            if product_id is None or product_id == "":
                meta["applies_to_products"] = []
                counts["brand_wide"] += 1
                print(f"  BRAND-WIDE {brand_dir.name}/{prof_path.parent.name}: applies_to_products=[]")
            else:
                meta["applies_to_products"] = [product_id]
                counts["migrated"] += 1
                print(f"  MIGRATED {brand_dir.name}/{prof_path.parent.name}: product_id='{product_id}' -> applies_to_products=['{product_id}']")

            if not dry_run:
                with prof_path.open("w", encoding="utf-8") as f:
                    json.dump(doc, f, ensure_ascii=False, indent=2)
                    f.write("\n")

    print()
    print(f"Summary: migrated={counts['migrated']}, already={counts['already']}, brand_wide={counts['brand_wide']}, skipped={counts['skipped']}")
    if dry_run:
        print("(dry-run, no files written)")


if __name__ == "__main__":
    main()
