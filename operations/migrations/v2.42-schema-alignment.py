#!/usr/bin/env python3
"""
v2.42-schema-alignment.py · Patch 1A migration · alignement schema vs data live.

Closes drift identified in audit 10 scopes v2.41:
  - brand.json v2.1 → v2.2 (creative_zone + brand_equity_level + strategic_context placeholders)
  - audiences/*/profile.json v1.2 → v1.4 (scope legacy mother/sub → broad/segment, entry_door inference)

Usage:
  python3 v2.42-schema-alignment.py <brand_path> --dry-run
  python3 v2.42-schema-alignment.py <brand_path> --apply

Idempotent · re-run safe (skips entries already at target version).
Backups horodatés YYYY-MM-DD pour chaque fichier muté.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ── Constants ──────────────────────────────────────────────────────────────────

BRAND_VERSION_FROM = "2.1"
BRAND_VERSION_TO = "2.2"

PROFILE_VERSION_FROM = ("1.2", "1.3")
PROFILE_VERSION_TO = "1.4"

# legacy scope → canon enum
SCOPE_MAPPING = {
    "mother": "broad",
    "sub": "segment",
    # canon already-valid passthroughs
    "broad": "broad",
    "segment": "segment",
    "micro": "micro",
}

# tag axis → entry_door enum
ENTRY_DOOR_INFERENCE = {
    "axis:pain-driven": "pain_driven",
    "axis:goal-driven": "goal_driven",
    "axis:identity-driven": "identity_driven",
}

ENTRY_DOOR_ENUM = ["pain_driven", "goal_driven", "identity_driven", None]


# ── Helpers ────────────────────────────────────────────────────────────────────

def backup_file(path: Path, dry_run: bool) -> Path:
    """Write timestamped backup next to the target file. Returns backup path."""
    stamp = datetime.now().strftime("%Y-%m-%d")
    backup_path = path.with_suffix(path.suffix + f".bak.{stamp}")
    if not dry_run:
        backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path


def write_json(path: Path, data: dict, dry_run: bool) -> None:
    """Write JSON with 2-space indent + trailing newline. Skips disk write in dry-run."""
    if dry_run:
        return
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def diff_lines(before: dict, after: dict, prefix: str = "") -> list[str]:
    """Surface top-level field diffs as readable lines."""
    out = []
    keys = set(before.keys()) | set(after.keys())
    for k in sorted(keys):
        b = before.get(k, "<absent>")
        a = after.get(k, "<absent>")
        if b != a:
            b_str = json.dumps(b, ensure_ascii=False) if not isinstance(b, str) else b
            a_str = json.dumps(a, ensure_ascii=False) if not isinstance(a, str) else a
            if len(str(b_str)) > 80:
                b_str = str(b_str)[:77] + "..."
            if len(str(a_str)) > 80:
                a_str = str(a_str)[:77] + "..."
            out.append(f"  {prefix}{k}: {b_str}  →  {a_str}")
    return out


# ── Brand patch ────────────────────────────────────────────────────────────────

def patch_brand(brand_json_path: Path, dry_run: bool) -> dict:
    """
    v2.1 → v2.2.
    Injects creative_zone, brand_equity_level, strategic_context placeholders if absent.
    Idempotent.
    """
    result: dict[str, Any] = {
        "path": str(brand_json_path),
        "skipped": False,
        "changes": [],
        "backup": None,
    }

    if not brand_json_path.exists():
        result["skipped"] = True
        result["reason"] = "brand.json not found"
        return result

    data = load_json(brand_json_path)
    before = copy.deepcopy(data)

    current_version = str(data.get("_version", ""))
    if current_version == BRAND_VERSION_TO:
        result["skipped"] = True
        result["reason"] = f"already v{BRAND_VERSION_TO}"
        return result

    # 1. creative_zone placeholder
    if "creative_zone" not in data:
        data["creative_zone"] = {
            "min": None,
            "max": None,
            "dominant": None,
            "_observed_on_n_creatives": 0,
        }
        result["changes"].append("creative_zone added (placeholder · {min, max, dominant, _observed_on_n_creatives})")

    # 2. brand_equity_level placeholder
    if "brand_equity_level" not in data:
        data["brand_equity_level"] = None
        result["changes"].append("brand_equity_level added (null · enum low/medium/high)")

    # 3. strategic_context placeholder
    if "strategic_context" not in data:
        data["strategic_context"] = {
            "stage": None,
            "momentum": None,
            "market": None,
            "atlas_state": None,
        }
        result["changes"].append("strategic_context added (placeholder · 4 axes modulateurs scoring)")

    # 4. bump _version + _changelog entry
    data["_version"] = BRAND_VERSION_TO
    changelog = data.get("_changelog", {})
    if BRAND_VERSION_TO not in changelog:
        changelog[BRAND_VERSION_TO] = (
            "v2.42-schema-alignment: creative_zone + brand_equity_level + strategic_context placeholders. "
            "4 axes modulateurs scoring brand-level. Backward compat: null = pas observé."
        )
        data["_changelog"] = changelog
        result["changes"].append(f"_version bumped {current_version} → {BRAND_VERSION_TO}")

    # 5. backup + write
    if result["changes"]:
        backup_path = backup_file(brand_json_path, dry_run)
        result["backup"] = str(backup_path)
        write_json(brand_json_path, data, dry_run)
        result["diff"] = diff_lines(before, data)

    return result


# ── Profile patch ──────────────────────────────────────────────────────────────

def infer_entry_door(tags: list[str]) -> tuple[str | None, bool]:
    """
    Returns (entry_door_value, inferred_flag).
    inferred_flag = True quand inférence depuis tag, False quand aucune correspondance (null).
    """
    for tag in tags:
        if tag in ENTRY_DOOR_INFERENCE:
            return ENTRY_DOOR_INFERENCE[tag], True
    return None, False


def patch_profile(profile_path: Path, dry_run: bool) -> dict:
    """
    v1.2/v1.3 → v1.4.
    - meta.scope: mother → broad, sub → segment (legacy mapping)
    - meta.entry_door: inferred from tags (axis:*) or null
    - bump _version
    Idempotent.
    """
    result: dict[str, Any] = {
        "path": str(profile_path),
        "audience_slug": profile_path.parent.name,
        "skipped": False,
        "changes": [],
        "backup": None,
    }

    if not profile_path.exists():
        result["skipped"] = True
        result["reason"] = "profile.json not found"
        return result

    data = load_json(profile_path)
    before = copy.deepcopy(data)

    current_version = str(data.get("_version", ""))
    if current_version == PROFILE_VERSION_TO:
        result["skipped"] = True
        result["reason"] = f"already v{PROFILE_VERSION_TO}"
        return result

    meta = data.get("meta", {})

    # 1. scope legacy → canon
    current_scope = meta.get("scope")
    if current_scope in SCOPE_MAPPING and current_scope in ("mother", "sub"):
        new_scope = SCOPE_MAPPING[current_scope]
        meta["scope"] = new_scope
        result["changes"].append(f"meta.scope: {current_scope} → {new_scope}")

    # 2. entry_door inference
    if "entry_door" not in meta or meta.get("entry_door") in ("", None):
        tags = meta.get("tags", [])
        inferred_value, was_inferred = infer_entry_door(tags)
        meta["entry_door"] = inferred_value
        meta["_inferred"] = was_inferred
        if was_inferred:
            result["changes"].append(
                f"meta.entry_door: null → {inferred_value} (inferred from tags) · _inferred: true"
            )
        else:
            result["changes"].append(
                "meta.entry_door: null (no axis:* tag found) · _inferred: false · operator gate post-migration"
            )

    # 3. bump _version + _changelog entry
    data["_version"] = PROFILE_VERSION_TO
    changelog = data.get("_changelog", {})
    if PROFILE_VERSION_TO not in changelog:
        changelog[PROFILE_VERSION_TO] = (
            "v2.42-schema-alignment: scope legacy (mother/sub) → canon (broad/segment), "
            "entry_door enum strict inféré depuis axis:* tags. _inferred flag visible si null."
        )
        data["_changelog"] = changelog
        result["changes"].append(f"_version bumped {current_version} → {PROFILE_VERSION_TO}")

    data["meta"] = meta

    # 4. backup + write
    if result["changes"]:
        backup_path = backup_file(profile_path, dry_run)
        result["backup"] = str(backup_path)
        write_json(profile_path, data, dry_run)
        result["diff"] = diff_lines(before.get("meta", {}), data.get("meta", {}), prefix="meta.")

    return result


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "brand_path",
        help="Absolute path to brand folder (e.g. /path/to/brands/kara/)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Aperçu sans mutation")
    group.add_argument("--apply", action="store_true", help="Apply patches")
    args = parser.parse_args()

    brand_root = Path(args.brand_path).resolve()
    if not brand_root.exists() or not brand_root.is_dir():
        sys.exit(f"brand_path introuvable ou pas un dossier · {brand_root}")

    mode_label = "DRY-RUN" if args.dry_run else "APPLY"

    print(f"\n{'=' * 70}")
    print(f"  v2.42-schema-alignment · {mode_label}")
    print(f"  brand: {brand_root}")
    print(f"{'=' * 70}\n")

    # 1. brand.json
    brand_json = brand_root / "brand.json"
    print(f"[1/2] brand.json · v{BRAND_VERSION_FROM} → v{BRAND_VERSION_TO}")
    print(f"      target: {brand_json}")
    brand_result = patch_brand(brand_json, args.dry_run)
    if brand_result.get("skipped"):
        print(f"      skipped · {brand_result.get('reason', 'no reason')}\n")
    else:
        for change in brand_result["changes"]:
            print(f"      · {change}")
        if brand_result.get("backup"):
            print(f"      backup: {brand_result['backup']}")
        for line in brand_result.get("diff", []):
            print(line)
        print()

    # 2. audiences/*/profile.json
    audiences_root = brand_root / "audiences"
    profile_paths = sorted(audiences_root.glob("*/profile.json")) if audiences_root.exists() else []

    # Exclude reserved folders (start with _)
    profile_paths = [p for p in profile_paths if not p.parent.name.startswith("_")]

    print(f"[2/2] audiences/*/profile.json · v{'/'.join(PROFILE_VERSION_FROM)} → v{PROFILE_VERSION_TO}")
    print(f"      target: {audiences_root} ({len(profile_paths)} profile files, excluding _*)\n")

    patched = 0
    skipped = 0
    inferred_count = 0
    null_count = 0
    for pp in profile_paths:
        r = patch_profile(pp, args.dry_run)
        print(f"      [{r['audience_slug']}]")
        if r.get("skipped"):
            print(f"        skipped · {r.get('reason', 'no reason')}")
            skipped += 1
        else:
            for change in r["changes"]:
                print(f"        · {change}")
            if r.get("backup"):
                print(f"        backup: {r['backup']}")
            # count inference outcomes
            data_after = load_json(pp) if not args.dry_run else None
            if data_after is None:
                # dry-run: re-infer for accounting
                src = load_json(pp)
                _, was_inferred = infer_entry_door(src.get("meta", {}).get("tags", []))
            else:
                was_inferred = data_after.get("meta", {}).get("_inferred", False)
            if was_inferred:
                inferred_count += 1
            else:
                null_count += 1
            patched += 1
        print()

    # Summary
    print(f"{'=' * 70}")
    print(f"  summary · mode={mode_label}")
    print(f"  brand.json: {'patched' if not brand_result.get('skipped') else 'skipped'}")
    print(f"  profiles: {patched} patched, {skipped} skipped (already target)")
    print(f"  entry_door inferred from tags: {inferred_count}")
    print(f"  entry_door null (operator gate): {null_count}")
    print(f"{'=' * 70}\n")

    if args.dry_run:
        print("  Dry-run only · no files written. Re-run with --apply to commit.\n")


if __name__ == "__main__":
    main()
