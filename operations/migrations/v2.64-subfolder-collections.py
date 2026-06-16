#!/usr/bin/env python3
"""
v2.64-subfolder-collections.py · BREAKING migration · ontologie sémantique pure.

Refactor v2.63 top-level collections → v2.64 sub-audience / sub-product location.
Sémantique pure · pain_point + objection = expression audience-specific (sub-audience).
friction = product-specific usage observation (sub-product). Canonical IDs PNT-NN /
OBJ-NN / FRC-NN preserved globaux (stable cross-folder).

Mutations:
  brands/{slug}/pain_points/{PNT-NN}.json
    → brands/{slug}/audiences/{primary_audience}/pain_points/{PNT-NN}.json
    (also_affects_audiences[] populated if N affected_audiences[] > 1)

  brands/{slug}/objections/{OBJ-NN}.json
    → brands/{slug}/audiences/{primary_audience}/objections/{OBJ-NN}.json
    (also_affects_audiences[] populated if N affected_audiences[] > 1)

  brands/{slug}/frictions/{FRC-NN}.json
    → brands/{slug}/products/{primary_product}/frictions/{FRC-NN}.json
    (affects_audiences[] preserved · cross-refs vers audiences impactées)

  pain_points.schema v1.0 → v1.1 (already bumped in resources/schemas/)
  objections.schema v1.0 → v1.1 (already bumped)
  friction.schema v1.2 → v1.3 (already bumped)

Usage:
  python3 v2.64-subfolder-collections.py <brand_path> --dry-run
  python3 v2.64-subfolder-collections.py <brand_path> --apply

Idempotent · re-run safe (check existing sub-folder target before write).
Backups horodatés zip des top-level dirs avant move.
Log mutations + warnings dans .phantom/context-engine-events.jsonl si présent.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Constants ──────────────────────────────────────────────────────────────────

PAIN_POINT_SCHEMA_VERSION = "pain_points/1.1"
OBJECTION_SCHEMA_VERSION = "objections/1.1"
FRICTION_SCHEMA_VERSION = "friction/1.3"


# ── Helpers ────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def log_event(events_log: Path, event: dict, dry_run: bool) -> None:
    """Append jsonl line to .phantom/context-engine-events.jsonl if log dir present."""
    if dry_run:
        return
    events_log.parent.mkdir(parents=True, exist_ok=True)
    with events_log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def backup_dir_as_zip(src_dir: Path, dry_run: bool) -> Path | None:
    """Zip top-level dir avant move. Horodatage YYYY-MM-DD-HHMMSS."""
    if not src_dir.exists() or not src_dir.is_dir():
        return None
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    backup_path = src_dir.parent / f"{src_dir.name}.bak.{stamp}.zip"
    if dry_run:
        return backup_path
    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in src_dir.rglob("*"):
            if f.is_file():
                zf.write(f, arcname=f.relative_to(src_dir.parent))
    return backup_path


# ── Pain point migration ───────────────────────────────────────────────────────

def migrate_pain_point(
    pain_path: Path,
    brand_root: Path,
    events_log: Path,
    dry_run: bool,
) -> dict:
    """
    Top-level pain_points/{PNT-NN}.json → audiences/{primary_audience}/pain_points/{PNT-NN}.json.
    Primary audience = 1ère de affected_audiences[]. Si N>1, populate also_affects_audiences[]
    avec [affected_audiences[1:]]. Si 0, skip with warning.
    """
    result: dict[str, Any] = {
        "path": str(pain_path),
        "entity_id": pain_path.stem,
        "skipped": False,
        "warning": None,
        "moved_to": None,
        "also_affects_added": [],
    }

    if not pain_path.exists():
        result["skipped"] = True
        result["warning"] = "file not found"
        return result

    data = load_json(pain_path)
    affected = data.get("affected_audiences", []) or []

    if not affected:
        result["skipped"] = True
        result["warning"] = f"zero affected_audiences[] · pain {pain_path.stem} stays top-level (edge case · operator review needed)"
        log_event(events_log, {
            "ts": now_iso(),
            "action_type": "migration_warning",
            "migration": "v2.64-subfolder-collections",
            "entity": "pain_points",
            "entity_id": pain_path.stem,
            "warning": "zero_affected_audiences",
            "source_path": str(pain_path),
        }, dry_run)
        return result

    primary_audience = affected[0]
    other_audiences = affected[1:] if len(affected) > 1 else []

    target_dir = brand_root / "audiences" / primary_audience / "pain_points"
    target_path = target_dir / pain_path.name

    # Idempotent · skip if already migrated
    if target_path.exists():
        result["skipped"] = True
        result["warning"] = f"already migrated to {target_path.relative_to(brand_root)}"
        return result

    # Populate also_affects_audiences[] if N > 1
    if other_audiences:
        existing_also = data.get("also_affects_audiences", []) or []
        merged = list(dict.fromkeys(existing_also + other_audiences))
        data["also_affects_audiences"] = merged
        result["also_affects_added"] = merged

    # Bump schema version
    data["_schema_version"] = PAIN_POINT_SCHEMA_VERSION

    # Write to target
    write_json(target_path, data, dry_run)
    result["moved_to"] = str(target_path)

    # Remove source after successful move
    if not dry_run and target_path.exists():
        pain_path.unlink()

    log_event(events_log, {
        "ts": now_iso(),
        "action_type": "migration_move",
        "migration": "v2.64-subfolder-collections",
        "entity": "pain_points",
        "entity_id": pain_path.stem,
        "source_path": str(pain_path),
        "target_path": str(target_path),
        "primary_audience": primary_audience,
        "also_affects_audiences": other_audiences,
    }, dry_run)

    return result


# ── Objection migration ────────────────────────────────────────────────────────

def migrate_objection(
    obj_path: Path,
    brand_root: Path,
    events_log: Path,
    dry_run: bool,
) -> dict:
    """
    Top-level objections/{OBJ-NN}.json → audiences/{primary_audience}/objections/{OBJ-NN}.json.
    Miroir migrate_pain_point logic.
    """
    result: dict[str, Any] = {
        "path": str(obj_path),
        "entity_id": obj_path.stem,
        "skipped": False,
        "warning": None,
        "moved_to": None,
        "also_affects_added": [],
    }

    if not obj_path.exists():
        result["skipped"] = True
        result["warning"] = "file not found"
        return result

    data = load_json(obj_path)
    affected = data.get("affected_audiences", []) or []

    if not affected:
        result["skipped"] = True
        result["warning"] = f"zero affected_audiences[] · objection {obj_path.stem} stays top-level (edge case · operator review needed)"
        log_event(events_log, {
            "ts": now_iso(),
            "action_type": "migration_warning",
            "migration": "v2.64-subfolder-collections",
            "entity": "objections",
            "entity_id": obj_path.stem,
            "warning": "zero_affected_audiences",
            "source_path": str(obj_path),
        }, dry_run)
        return result

    primary_audience = affected[0]
    other_audiences = affected[1:] if len(affected) > 1 else []

    target_dir = brand_root / "audiences" / primary_audience / "objections"
    target_path = target_dir / obj_path.name

    if target_path.exists():
        result["skipped"] = True
        result["warning"] = f"already migrated to {target_path.relative_to(brand_root)}"
        return result

    if other_audiences:
        existing_also = data.get("also_affects_audiences", []) or []
        merged = list(dict.fromkeys(existing_also + other_audiences))
        data["also_affects_audiences"] = merged
        result["also_affects_added"] = merged

    data["_schema_version"] = OBJECTION_SCHEMA_VERSION

    write_json(target_path, data, dry_run)
    result["moved_to"] = str(target_path)

    if not dry_run and target_path.exists():
        obj_path.unlink()

    log_event(events_log, {
        "ts": now_iso(),
        "action_type": "migration_move",
        "migration": "v2.64-subfolder-collections",
        "entity": "objections",
        "entity_id": obj_path.stem,
        "source_path": str(obj_path),
        "target_path": str(target_path),
        "primary_audience": primary_audience,
        "also_affects_audiences": other_audiences,
    }, dry_run)

    return result


# ── Friction migration ─────────────────────────────────────────────────────────

def migrate_friction(
    fric_path: Path,
    brand_root: Path,
    events_log: Path,
    dry_run: bool,
) -> dict:
    """
    Top-level frictions/{FRC-NN}.json → products/{primary_product}/frictions/{FRC-NN}.json.
    Si zéro affected_products[] · stay top-level mais log warning (friction sans product · cas edge).
    affects_audiences[] preserved tel quel (cross-refs canonical).
    """
    result: dict[str, Any] = {
        "path": str(fric_path),
        "entity_id": fric_path.stem,
        "skipped": False,
        "warning": None,
        "moved_to": None,
    }

    if not fric_path.exists():
        result["skipped"] = True
        result["warning"] = "file not found"
        return result

    data = load_json(fric_path)
    affected_products = data.get("affected_products", []) or []

    if not affected_products:
        result["skipped"] = True
        result["warning"] = f"zero affected_products[] · friction {fric_path.stem} stays top-level (edge case · operator review needed · brand-wide friction sans product attachment)"
        log_event(events_log, {
            "ts": now_iso(),
            "action_type": "migration_warning",
            "migration": "v2.64-subfolder-collections",
            "entity": "frictions",
            "entity_id": fric_path.stem,
            "warning": "zero_affected_products",
            "source_path": str(fric_path),
        }, dry_run)
        return result

    primary_product = affected_products[0]

    target_dir = brand_root / "products" / primary_product / "frictions"
    target_path = target_dir / fric_path.name

    if target_path.exists():
        result["skipped"] = True
        result["warning"] = f"already migrated to {target_path.relative_to(brand_root)}"
        return result

    # Bump schema version
    data["_schema_version"] = FRICTION_SCHEMA_VERSION

    write_json(target_path, data, dry_run)
    result["moved_to"] = str(target_path)

    if not dry_run and target_path.exists():
        fric_path.unlink()

    log_event(events_log, {
        "ts": now_iso(),
        "action_type": "migration_move",
        "migration": "v2.64-subfolder-collections",
        "entity": "frictions",
        "entity_id": fric_path.stem,
        "source_path": str(fric_path),
        "target_path": str(target_path),
        "primary_product": primary_product,
        "affects_audiences_preserved": data.get("affected_audiences", []) or [],
    }, dry_run)

    return result


# ── Cleanup top-level dirs post-migration ──────────────────────────────────────

def cleanup_top_level_dir(top_dir: Path, dry_run: bool) -> bool:
    """
    Remove top-level pain_points/ + objections/ + frictions/ après move success.
    Garde si fichiers restants (warnings cas edge zero affected_*).
    Returns True si dir removed, False si conservé.
    """
    if not top_dir.exists() or not top_dir.is_dir():
        return False

    remaining = list(top_dir.glob("*.json"))
    if remaining:
        # Garder le dir · cas edge avec warnings non-migrés
        return False

    if dry_run:
        return True

    # Remove empty dir
    shutil.rmtree(top_dir)
    return True


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
    print(f"  v2.64-subfolder-collections · {mode_label}")
    print(f"  brand: {brand_root}")
    print(f"{'=' * 70}\n")

    pain_dir = brand_root / "pain_points"
    obj_dir = brand_root / "objections"
    fric_dir = brand_root / "frictions"
    events_log = brand_root.parent.parent / ".phantom" / "context-engine-events.jsonl"

    print(f"  pain_points  dir · {pain_dir}")
    print(f"  objections   dir · {obj_dir}")
    print(f"  frictions    dir · {fric_dir}")
    print(f"  events log       · {events_log}\n")

    # Backups horodatés zip des top-level dirs avant move
    print(f"  [STEP 1/5] Backup top-level dirs as zip\n")
    for d in (pain_dir, obj_dir, fric_dir):
        if d.exists():
            backup = backup_dir_as_zip(d, args.dry_run)
            if backup:
                print(f"    backup · {backup}")
    print()

    # 1. Migrate pain_points/
    print(f"  [STEP 2/5] Migrate pain_points/ → audiences/{{primary}}/pain_points/\n")
    pain_files = sorted(pain_dir.glob("PNT-*.json")) if pain_dir.exists() else []
    print(f"    {len(pain_files)} pain files found\n")
    pain_moved = 0
    pain_skipped = 0
    pain_warnings = 0
    for pf in pain_files:
        r = migrate_pain_point(pf, brand_root, events_log, args.dry_run)
        if r["skipped"]:
            print(f"    [{r['entity_id']}] skipped · {r.get('warning', 'no reason')}")
            pain_skipped += 1
            if r.get("warning") and "stays top-level" in r["warning"]:
                pain_warnings += 1
        else:
            print(f"    [{r['entity_id']}] moved → audiences/{Path(r['moved_to']).parent.parent.name}/pain_points/")
            if r["also_affects_added"]:
                print(f"                    also_affects · {r['also_affects_added']}")
            pain_moved += 1
    print()

    # 2. Migrate objections/
    print(f"  [STEP 3/5] Migrate objections/ → audiences/{{primary}}/objections/\n")
    obj_files = sorted(obj_dir.glob("OBJ-*.json")) if obj_dir.exists() else []
    print(f"    {len(obj_files)} objection files found\n")
    obj_moved = 0
    obj_skipped = 0
    obj_warnings = 0
    for of in obj_files:
        r = migrate_objection(of, brand_root, events_log, args.dry_run)
        if r["skipped"]:
            print(f"    [{r['entity_id']}] skipped · {r.get('warning', 'no reason')}")
            obj_skipped += 1
            if r.get("warning") and "stays top-level" in r["warning"]:
                obj_warnings += 1
        else:
            print(f"    [{r['entity_id']}] moved → audiences/{Path(r['moved_to']).parent.parent.name}/objections/")
            if r["also_affects_added"]:
                print(f"                    also_affects · {r['also_affects_added']}")
            obj_moved += 1
    print()

    # 3. Migrate frictions/
    print(f"  [STEP 4/5] Migrate frictions/ → products/{{primary}}/frictions/\n")
    fric_files = sorted(fric_dir.glob("FRC-*.json")) if fric_dir.exists() else []
    print(f"    {len(fric_files)} friction files found\n")
    fric_moved = 0
    fric_skipped = 0
    fric_warnings = 0
    for ff in fric_files:
        r = migrate_friction(ff, brand_root, events_log, args.dry_run)
        if r["skipped"]:
            print(f"    [{r['entity_id']}] skipped · {r.get('warning', 'no reason')}")
            fric_skipped += 1
            if r.get("warning") and "stays top-level" in r["warning"]:
                fric_warnings += 1
        else:
            print(f"    [{r['entity_id']}] moved → products/{Path(r['moved_to']).parent.parent.name}/frictions/")
            fric_moved += 1
    print()

    # 4. Cleanup top-level dirs si vides
    print(f"  [STEP 5/5] Cleanup empty top-level dirs\n")
    for d, label in [(pain_dir, "pain_points"), (obj_dir, "objections"), (fric_dir, "frictions")]:
        removed = cleanup_top_level_dir(d, args.dry_run)
        if removed:
            print(f"    {label}/ removed (empty)")
            log_event(events_log, {
                "ts": now_iso(),
                "action_type": "migration_cleanup",
                "migration": "v2.64-subfolder-collections",
                "entity": label,
                "removed_dir": str(d),
            }, args.dry_run)
        elif d.exists():
            remaining = len(list(d.glob("*.json")))
            print(f"    {label}/ kept · {remaining} file(s) remaining (warnings · operator review)")
    print()

    # Summary
    print(f"{'=' * 70}")
    print(f"  summary · mode={mode_label}")
    print(f"  pain_points · {pain_moved} moved, {pain_skipped} skipped ({pain_warnings} warnings)")
    print(f"  objections  · {obj_moved} moved, {obj_skipped} skipped ({obj_warnings} warnings)")
    print(f"  frictions   · {fric_moved} moved, {fric_skipped} skipped ({fric_warnings} warnings)")
    print(f"{'=' * 70}\n")

    if args.dry_run:
        print("  Dry-run only · no files written. Re-run with --apply to commit.\n")


if __name__ == "__main__":
    main()
