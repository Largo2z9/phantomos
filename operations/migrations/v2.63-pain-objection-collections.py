#!/usr/bin/env python3
"""
v2.63-pain-objection-collections.py · BREAKING migration · refactor ontologie pure.

Closes ontologie inconsistance pre-v2.63 (friction top-level depuis v2.56 mais
pain_points + objections sub-fields legacy v1.7 dans profile.schema). Parité
friction · 3 collections sub-tensions séparées (canon Notion stride-up strict).

Mutations:
  profile.schema v1.7 → v2.0 BREAKING · REMOVE pain_points[] + objections[]
  NEW pain_points.schema v1.0 (top-level collection brands/{slug}/pain_points/{PNT-NN}.json)
  NEW objections.schema v1.0 (top-level collection brands/{slug}/objections/{OBJ-NN}.json)
  friction.schema v1.1 → v1.2 (cross_refs canonical refs)
  angle.schema v1.2 → v1.3 (lineage.pain_ref + objection_ref optional)
  learnings.schema v1.0 → v1.1 (entries[].cross_refs.{pain_point_ids[], objection_ids[]})

Usage:
  python3 v2.63-pain-objection-collections.py <brand_path> --dry-run
  python3 v2.63-pain-objection-collections.py <brand_path> --apply

Idempotent · re-run safe (check existing pain_points/ + objections/ before write).
Backups horodatés YYYY-MM-DD pour chaque profile.json muté.
Log mutations dans .phantom/context-engine-events.jsonl si présent.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Constants ──────────────────────────────────────────────────────────────────

PROFILE_VERSION_FROM = ("1.4", "1.5", "1.6", "1.7")
PROFILE_VERSION_TO = "2.0"

PAIN_POINT_SCHEMA_VERSION = "pain_points/1.0"
OBJECTION_SCHEMA_VERSION = "objections/1.0"


# ── Helpers ────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def backup_file(path: Path, dry_run: bool) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d")
    backup_path = path.with_suffix(path.suffix + f".bak.{stamp}")
    if not dry_run:
        backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path


def write_json(path: Path, data: dict, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def log_event(events_log: Path, event: dict, dry_run: bool) -> None:
    """Append jsonl line to .phantom/context-engine-events.jsonl if present."""
    if dry_run:
        return
    events_log.parent.mkdir(parents=True, exist_ok=True)
    with events_log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


# ── ID allocator (incremental cross-brand) ─────────────────────────────────────

def next_id(prefix: str, existing_dir: Path) -> str:
    """
    Return next available PNT-NN or OBJ-NN id in directory.
    Scans existing {prefix}-NN.json files, returns next sequential id.
    """
    if not existing_dir.exists():
        return f"{prefix}-01"
    existing = []
    for p in existing_dir.glob(f"{prefix}-*.json"):
        stem = p.stem  # e.g. "PNT-12"
        try:
            n = int(stem.split("-")[1])
            existing.append(n)
        except (IndexError, ValueError):
            continue
    next_n = max(existing) + 1 if existing else 1
    return f"{prefix}-{next_n:02d}"


# ── Pain point extraction ──────────────────────────────────────────────────────

def extract_pain_to_collection(
    pain_entry: dict,
    pain_id: str,
    audience_slug: str,
    affected_products: list[str],
) -> dict:
    """Convert profile.pain_points[].item legacy v1.7 → pain_points.schema v1.0 file."""
    # legacy chain was array of {level, formulation} · convert to object surface/consequence/deep
    chain_legacy = pain_entry.get("chain", [])
    chain_obj: dict[str, str] = {}
    if isinstance(chain_legacy, list):
        for c in chain_legacy:
            lvl = c.get("level")
            if lvl in ("surface", "consequence", "deep"):
                chain_obj[lvl] = c.get("formulation", "")

    source_meta = pain_entry.get("_source_meta", {})
    origin = source_meta.get("origin", "")
    # map legacy origin to v2.63 _source enum
    source_map = {
        "voc": "mine_voc",
        "brand_declared": "operator",
        "inferred": "agent",
    }
    canon_source = source_map.get(origin, "operator")

    verbatim_quotes = []
    if source_meta.get("sample_size") is not None or source_meta.get("platform"):
        verbatim_quotes.append({
            "text": pain_entry.get("formulation", ""),
            "source": source_meta.get("platform", ""),
            "sample_size": source_meta.get("sample_size") or 0,
        })

    out = {
        "pain_id": pain_id,
        "formulation": pain_entry.get("formulation", ""),
        "affected_audiences": [audience_slug],
        "affected_products": list(affected_products),
        "meta": {
            "validation_status": "hypothesis",
            "_source": canon_source,
            "created": now_iso(),
            "created_by_skill": "v2.63-pain-objection-collections-migration",
        },
    }
    if pain_entry.get("pain_id"):
        out["pain_id"] = pain_entry["pain_id"]
    if pain_entry.get("pain_category"):
        out["pain_category"] = pain_entry["pain_category"]
    if chain_obj:
        out["chain"] = chain_obj
    if pain_entry.get("emotion"):
        out["emotion"] = pain_entry["emotion"]
    if pain_entry.get("trigger"):
        out["trigger"] = pain_entry["trigger"]
    if pain_entry.get("awareness_stage"):
        out["awareness_stage"] = pain_entry["awareness_stage"]
    if verbatim_quotes:
        out["verbatim_quotes"] = verbatim_quotes
    return out


def extract_objection_to_collection(
    obj_entry: dict,
    objection_id: str,
    audience_slug: str,
    affected_products: list[str],
) -> dict:
    """Convert profile.objections[].item legacy v1.7 → objections.schema v1.0 file."""
    # map legacy type enum (FR) → v2.63 canonical type enum (EN)
    type_map = {
        "prix": "price",
        "scepticisme": "scepticism",
        "temps": "fit",
        "confiance": "trust",
        "urgence": "urgency",
        "efficacité": "fit",
        "comparaison": "fit",
    }
    legacy_type = obj_entry.get("type") or ""
    canon_type = type_map.get(legacy_type, "fit")

    # map legacy severity enum (low/medium/high) directly · "blocking" v2.63 addition
    legacy_severity = obj_entry.get("severity") or ""
    canon_severity = legacy_severity if legacy_severity in ("low", "medium", "high") else None

    # legacy frequency was integer 1-10 · v2.63 enum low/medium/high · map by bucket
    legacy_freq = obj_entry.get("frequency")
    canon_freq = None
    if isinstance(legacy_freq, int):
        if legacy_freq <= 3:
            canon_freq = "low"
        elif legacy_freq <= 6:
            canon_freq = "medium"
        else:
            canon_freq = "high"

    out = {
        "objection_id": objection_id,
        "formulation": obj_entry.get("formulation", ""),
        "type": canon_type,
        "affected_audiences": [audience_slug],
        "affected_products": list(affected_products),
        "meta": {
            "validation_status": "hypothesis",
            "_source": "operator",
            "created": now_iso(),
            "created_by_skill": "v2.63-pain-objection-collections-migration",
        },
    }
    if obj_entry.get("objection_id"):
        out["objection_id"] = obj_entry["objection_id"]
    if obj_entry.get("lifecycle_stage"):
        out["lifecycle_stage"] = obj_entry["lifecycle_stage"]
    if canon_freq:
        out["frequency"] = canon_freq
    if canon_severity:
        out["severity"] = canon_severity
    if obj_entry.get("severity_score") is not None:
        out["severity_score"] = obj_entry["severity_score"]
    if obj_entry.get("response_counter"):
        out["response_counter"] = obj_entry["response_counter"]
    if obj_entry.get("derived_angle_refs"):
        out["derived_angle_refs"] = obj_entry["derived_angle_refs"]
    return out


# ── Profile patch ──────────────────────────────────────────────────────────────

def patch_profile(
    profile_path: Path,
    pain_dir: Path,
    obj_dir: Path,
    events_log: Path,
    dry_run: bool,
) -> dict:
    """
    Extract profile.pain_points[] → brands/{slug}/pain_points/{PNT-NN}.json files.
    Extract profile.objections[] → brands/{slug}/objections/{OBJ-NN}.json files.
    Remove arrays from profile, bump _schema_version to profile/2.0.
    Idempotent.
    """
    result: dict[str, Any] = {
        "path": str(profile_path),
        "audience_slug": profile_path.parent.name,
        "skipped": False,
        "changes": [],
        "pain_files_created": [],
        "objection_files_created": [],
        "backup": None,
    }

    if not profile_path.exists():
        result["skipped"] = True
        result["reason"] = "profile.json not found"
        return result

    data = load_json(profile_path)

    current_version = str(data.get("_schema_version", "") or data.get("_version", ""))
    if current_version in ("profile/2.0", PROFILE_VERSION_TO):
        result["skipped"] = True
        result["reason"] = f"already v{PROFILE_VERSION_TO}"
        return result

    audience_slug = profile_path.parent.name
    affected_products = data.get("meta", {}).get("applies_to_products", []) or []

    # 1. Extract pain_points
    pain_entries = data.get("pain_points", []) or []
    for entry in pain_entries:
        pain_id = entry.get("pain_id") or next_id("PNT", pain_dir)
        target_path = pain_dir / f"{pain_id}.json"
        if target_path.exists():
            # idempotent · skip if already extracted
            continue
        extracted = extract_pain_to_collection(entry, pain_id, audience_slug, affected_products)
        write_json(target_path, extracted, dry_run)
        result["pain_files_created"].append(str(target_path))
        log_event(events_log, {
            "ts": now_iso(),
            "action_type": "migration_extract",
            "migration": "v2.63-pain-objection-collections",
            "entity": "pain_points",
            "entity_id": pain_id,
            "source_path": str(profile_path),
            "target_path": str(target_path),
            "audience_slug": audience_slug,
        }, dry_run)

    # 2. Extract objections
    obj_entries = data.get("objections", []) or []
    for entry in obj_entries:
        obj_id = entry.get("objection_id") or next_id("OBJ", obj_dir)
        target_path = obj_dir / f"{obj_id}.json"
        if target_path.exists():
            continue
        extracted = extract_objection_to_collection(entry, obj_id, audience_slug, affected_products)
        write_json(target_path, extracted, dry_run)
        result["objection_files_created"].append(str(target_path))
        log_event(events_log, {
            "ts": now_iso(),
            "action_type": "migration_extract",
            "migration": "v2.63-pain-objection-collections",
            "entity": "objections",
            "entity_id": obj_id,
            "source_path": str(profile_path),
            "target_path": str(target_path),
            "audience_slug": audience_slug,
        }, dry_run)

    # 3. Remove pain_points + objections arrays + bump version
    if "pain_points" in data:
        del data["pain_points"]
        result["changes"].append("REMOVE profile.pain_points[] (extracted to pain_points/)")
    if "objections" in data:
        del data["objections"]
        result["changes"].append("REMOVE profile.objections[] (extracted to objections/)")

    data["_schema_version"] = f"profile/{PROFILE_VERSION_TO}"
    data["_version"] = PROFILE_VERSION_TO
    changelog = data.get("_changelog", {})
    if PROFILE_VERSION_TO not in changelog:
        changelog[PROFILE_VERSION_TO] = (
            "v2.63 BREAKING · refactor ontologie pure. REMOVE pain_points[] + objections[] "
            "(extracted to top-level collections brands/{slug}/pain_points/{PNT-NN}.json + "
            "brands/{slug}/objections/{OBJ-NN}.json). Parité friction · canon Notion stride-up strict."
        )
        data["_changelog"] = changelog
        result["changes"].append(f"_schema_version bumped {current_version} → profile/{PROFILE_VERSION_TO}")

    # 4. Backup + write
    if result["changes"] or result["pain_files_created"] or result["objection_files_created"]:
        backup_path = backup_file(profile_path, dry_run)
        result["backup"] = str(backup_path)
        write_json(profile_path, data, dry_run)
        log_event(events_log, {
            "ts": now_iso(),
            "action_type": "migration_profile",
            "migration": "v2.63-pain-objection-collections",
            "audience_slug": audience_slug,
            "source_path": str(profile_path),
            "schema_version_before": current_version,
            "schema_version_after": f"profile/{PROFILE_VERSION_TO}",
            "pain_extracted": len(result["pain_files_created"]),
            "objections_extracted": len(result["objection_files_created"]),
        }, dry_run)

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
    print(f"  v2.63-pain-objection-collections · {mode_label}")
    print(f"  brand: {brand_root}")
    print(f"{'=' * 70}\n")

    pain_dir = brand_root / "pain_points"
    obj_dir = brand_root / "objections"
    events_log = brand_root.parent.parent / ".phantom" / "context-engine-events.jsonl"

    print(f"  pain_points dir · {pain_dir}")
    print(f"  objections  dir · {obj_dir}")
    print(f"  events log      · {events_log}\n")

    audiences_root = brand_root / "audiences"
    profile_paths = sorted(audiences_root.glob("*/profile.json")) if audiences_root.exists() else []
    profile_paths = [p for p in profile_paths if not p.parent.name.startswith("_")]

    print(f"  audiences · {len(profile_paths)} profile files (excluding _*)\n")

    patched = 0
    skipped = 0
    total_pain = 0
    total_obj = 0
    for pp in profile_paths:
        r = patch_profile(pp, pain_dir, obj_dir, events_log, args.dry_run)
        print(f"  [{r['audience_slug']}]")
        if r.get("skipped"):
            print(f"    skipped · {r.get('reason', 'no reason')}")
            skipped += 1
        else:
            for change in r["changes"]:
                print(f"    · {change}")
            for pf in r["pain_files_created"]:
                print(f"    + pain  · {Path(pf).name}")
                total_pain += 1
            for of in r["objection_files_created"]:
                print(f"    + obj   · {Path(of).name}")
                total_obj += 1
            if r.get("backup"):
                print(f"    backup  · {r['backup']}")
            patched += 1
        print()

    print(f"{'=' * 70}")
    print(f"  summary · mode={mode_label}")
    print(f"  profiles patched · {patched}")
    print(f"  profiles skipped · {skipped} (already v2.0 or no entries)")
    print(f"  pain_points extracted · {total_pain}")
    print(f"  objections extracted  · {total_obj}")
    print(f"{'=' * 70}\n")

    if args.dry_run:
        print("  Dry-run only · no files written. Re-run with --apply to commit.\n")


if __name__ == "__main__":
    main()
