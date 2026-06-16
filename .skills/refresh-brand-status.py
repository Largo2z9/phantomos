#!/usr/bin/env python3
"""
Mechanical status.json refresh for a given brand. No LLM.

Recomputes:
- last_activity: now (UTC)
- completeness.brand: "empty" | "draft" | "partial" | "complete"
- completeness.products: per-slug completeness from spec.json presence + required fields
- completeness.audiences: per-slug completeness from profile.json
- completeness.offers: per-product-slug completeness from offers.json (v2 offer_groups shape)
- wedge_complete: true when all 4 entity types have at least one "draft" or better

Usage:
  python3 .skills/refresh-brand-status.py {slug}

Exit 0 on success. Prints the updated status.json to stdout for inspection.
No-op if brands/{slug}/ does not exist (exits 0 silently · brand may have been
deleted).

Invoked by the .claude/hooks/post-write-flush.py PostToolUse hook after any
write-to-context.py invocation on a brand path. Replaces the "validate-resources
runs at the end of the onboarding" pattern that depended on the agent not
forgetting to call it.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(12):
        if (cur / "brands").is_dir() and (cur / ".skills").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def is_non_empty(v) -> bool:
    if v is None or v == "" or v == [] or v == {}:
        return False
    return True


def grade(filled: int, required: int) -> str:
    if filled == 0:
        return "empty"
    if filled >= required:
        return "complete"
    if filled >= max(1, required // 2):
        return "partial"
    return "draft"


def grade_brand(brand: dict | None) -> str:
    if not brand:
        return "empty"
    identity = brand.get("identity") or {}
    positioning = brand.get("positioning") or {}
    tone = brand.get("tone_of_voice") or {}
    filled = sum([
        is_non_empty(identity.get("name")),
        is_non_empty(identity.get("tagline")) or is_non_empty(identity.get("elevator_pitch")),
        is_non_empty(positioning.get("summary")) or is_non_empty(positioning.get("category")),
        is_non_empty(tone.get("register")) or is_non_empty(tone.get("essence")),
    ])
    return grade(filled, required=4)


def grade_product(spec: dict | None) -> str:
    if not spec:
        return "empty"
    identity = spec.get("identity") or {}
    pricing = spec.get("pricing") or {}
    filled = sum([
        is_non_empty(identity.get("name")),
        is_non_empty(identity.get("category")),
        is_non_empty(pricing.get("price")) or is_non_empty(pricing.get("price_retail")),
        is_non_empty(spec.get("benefits")) or is_non_empty(spec.get("problems")),
    ])
    return grade(filled, required=4)


def grade_audience(profile: dict | None) -> str:
    if not profile:
        return "empty"
    identity = profile.get("identity") or {}
    filled = sum([
        is_non_empty(identity.get("label")),
        is_non_empty(profile.get("psychology")) or is_non_empty(profile.get("top_pains")),
        is_non_empty(profile.get("objections")),
        is_non_empty(profile.get("benefits")) or is_non_empty(profile.get("pain_chain")),
    ])
    return grade(filled, required=4)


def grade_offers(offers: dict | None) -> str:
    if not offers:
        return "empty"
    groups = offers.get("offer_groups") or []
    if not groups:
        return "empty"
    total = 0
    active = 0
    for g in groups:
        for o in g.get("offers") or []:
            total += 1
            if o.get("active"):
                active += 1
    if total == 0:
        return "empty"
    if active >= 1 and total >= 1:
        return "complete" if total >= 2 else "partial"
    return "draft"


def compute_wedge_complete(comp: dict) -> bool:
    """True when all 4 entity types have at least one 'draft' or better."""
    levels = {"empty": 0, "draft": 1, "partial": 2, "complete": 3}

    def min_level(value) -> int:
        if isinstance(value, dict):
            if not value:
                return 0
            return min(levels.get(v, 0) for k, v in value.items() if not k.startswith("_"))
        return levels.get(value, 0)

    return all(
        min_level(comp[k]) >= 1
        for k in ("brand", "products", "audiences", "offers")
    )


def refresh(brand_dir: Path) -> dict | None:
    status_path = brand_dir / "status.json"
    status = load_json(status_path)
    if status is None:
        return None

    brand = load_json(brand_dir / "brand.json")

    products = {}
    offers = {}
    prod_dir = brand_dir / "products"
    if prod_dir.is_dir():
        for p in sorted(prod_dir.iterdir()):
            if not p.is_dir() or p.name.startswith("_"):
                continue
            spec = load_json(p / "spec.json")
            products[p.name] = grade_product(spec)
            ofr = load_json(p / "offers.json")
            offers[p.name] = grade_offers(ofr)

    audiences = {}
    aud_dir = brand_dir / "audiences"
    if aud_dir.is_dir():
        for a in sorted(aud_dir.iterdir()):
            if not a.is_dir() or a.name.startswith("_"):
                continue
            profile = load_json(a / "profile.json")
            audiences[a.name] = grade_audience(profile)

    status["last_activity"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    status["completeness"]["brand"] = grade_brand(brand)
    status["completeness"]["products"] = products
    status["completeness"]["audiences"] = audiences
    status["completeness"]["offers"] = offers
    status["wedge_complete"] = compute_wedge_complete(status["completeness"])

    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n")
    return status


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: refresh-brand-status.py {slug}", file=sys.stderr)
        sys.exit(2)
    slug = sys.argv[1]

    root = find_workspace_root(Path.cwd())
    if root is None:
        sys.exit(0)

    brand_dir = root / "brands" / slug
    if not brand_dir.is_dir() or slug.startswith("_"):
        sys.exit(0)

    status = refresh(brand_dir)
    if status is None:
        sys.exit(0)

    print(json.dumps({"slug": slug, "wedge_complete": status["wedge_complete"], "completeness": status["completeness"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
