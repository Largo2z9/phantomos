#!/usr/bin/env python3
"""
v2.42-canon-tool-v11.py · Patch 1A migration · canon-tool v1.0 → v1.1.

Closes drift identified in audit 10 scopes v2.41 · canon-tool.schema.json spec'd v1.1 (v2.37+)
but 58/58 fiches resources/canon/copy/**/*.json still _schema: "canon-tool/1.0".

Bulk-patch template canon copy fiches:
  - top-level _schema: "canon-tool/1.0" → "canon-tool/1.1"
  - for each entry in validations[] (probably empty everywhere) inject defaults:
      attribution_layer: "public-doctrine" (sentinel canon copy générique)
      decay_ttl_days: null (no decay sur canon partagée par défaut)
      _isolation_boundary: "shared" (cross-brand par design)
      brand_slug: unchanged (vide tolérée sur entries pré-validation)

Empty validations[] still gets bumped _schema. Idempotent · re-run safe.

Usage:
  python3 v2.42-canon-tool-v11.py <canon_copy_root> [--dry-run]
  Default · applies.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

# ── Constants ──────────────────────────────────────────────────────────────────

SCHEMA_FROM = "canon-tool/1.0"
SCHEMA_TO = "canon-tool/1.1"

VALIDATION_DEFAULTS = {
    "attribution_layer": "public-doctrine",
    "decay_ttl_days": None,
    "_isolation_boundary": "shared",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def backup_file(path: Path, dry_run: bool) -> Path:
    """Sibling .bak file per spec."""
    backup_path = path.with_suffix(path.suffix + ".bak")
    if not dry_run:
        backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def patch_validation_entry(entry: dict) -> tuple[dict, list[str]]:
    """Inject defaults if absent. Returns (patched_entry, list_of_changes)."""
    changes: list[str] = []
    patched = dict(entry)
    for k, v in VALIDATION_DEFAULTS.items():
        if k not in patched:
            patched[k] = v
            changes.append(f"validation entry · {k}: <absent> → {v!r}")
    # brand_slug · keep as-is, just confirm presence (NO mutation)
    if "brand_slug" not in patched:
        # spec says "brand_slug reste tel quel (vide ok pour entry sans validation brand)"
        # but it's a required field on v1.1 per schema. We leave it absent for empty-validations docs
        # since spec says "vide ok pour entry sans validation brand". Operator gate sur write.
        pass
    return patched, changes


def patch_canon_fiche(path: Path, dry_run: bool) -> dict:
    """
    v1.0 → v1.1 bulk patch.
    Idempotent · skips fiches already at v1.1.
    """
    result: dict[str, Any] = {
        "path": str(path),
        "name": path.stem,
        "layer": path.parent.name,
        "skipped": False,
        "changes": [],
        "backup": None,
    }

    data = load_json(path)
    before = copy.deepcopy(data)

    current_schema = data.get("_schema")
    if current_schema == SCHEMA_TO:
        result["skipped"] = True
        result["reason"] = f"already {SCHEMA_TO}"
        return result

    if current_schema != SCHEMA_FROM:
        result["skipped"] = True
        result["reason"] = f"unexpected _schema: {current_schema!r} (expected {SCHEMA_FROM!r})"
        return result

    # 1. bump _schema
    data["_schema"] = SCHEMA_TO
    result["changes"].append(f"_schema: {SCHEMA_FROM} → {SCHEMA_TO}")

    # 2. patch validations entries (probably empty)
    validations = data.get("validations", [])
    if validations:
        new_validations = []
        for i, entry in enumerate(validations):
            patched, entry_changes = patch_validation_entry(entry)
            new_validations.append(patched)
            for ec in entry_changes:
                result["changes"].append(f"validations[{i}] · {ec}")
        data["validations"] = new_validations
    # else: empty array · just _schema bump

    # 3. backup + write
    if result["changes"]:
        backup_path = backup_file(path, dry_run)
        result["backup"] = str(backup_path)
        write_json(path, data, dry_run)

    return result


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "canon_root",
        nargs="?",
        default="resources/canon/copy",
        help="Path to canon copy root (default: resources/canon/copy)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Aperçu sans mutation")
    args = parser.parse_args()

    canon_root = Path(args.canon_root).resolve()
    if not canon_root.exists() or not canon_root.is_dir():
        sys.exit(f"canon_root introuvable ou pas un dossier · {canon_root}")

    mode_label = "DRY-RUN" if args.dry_run else "APPLY"

    print(f"\n{'=' * 70}")
    print(f"  v2.42-canon-tool-v11 · {mode_label}")
    print(f"  root: {canon_root}")
    print(f"{'=' * 70}\n")

    # Discover all canon copy fiches
    fiche_paths = sorted(canon_root.glob("**/*.json"))
    # Exclude any .bak files explicitly
    fiche_paths = [p for p in fiche_paths if not p.name.endswith(".bak.json")]

    print(f"  Discovered {len(fiche_paths)} JSON fiches\n")

    patched_count = 0
    skipped_count = 0
    skipped_reasons: dict[str, int] = {}

    for fp in fiche_paths:
        r = patch_canon_fiche(fp, args.dry_run)
        if r.get("skipped"):
            reason = r.get("reason", "unknown")
            skipped_reasons[reason] = skipped_reasons.get(reason, 0) + 1
            skipped_count += 1
            # silent unless unexpected schema
            if "unexpected" in reason:
                print(f"  ⚠ {r['layer']}/{r['name']} · {reason}")
            continue

        patched_count += 1
        print(f"  · {r['layer']}/{r['name']}")
        for change in r["changes"]:
            print(f"      {change}")
        if r.get("backup"):
            print(f"      backup: {r['backup']}")

    # Summary
    print(f"\n{'=' * 70}")
    print(f"  summary · mode={mode_label}")
    print(f"  total fiches: {len(fiche_paths)}")
    print(f"  patched: {patched_count}")
    print(f"  skipped: {skipped_count}")
    for reason, n in skipped_reasons.items():
        print(f"    · {reason}: {n}")
    print(f"{'=' * 70}\n")

    if args.dry_run:
        print("  Dry-run only · no files written. Re-run without --dry-run to commit.\n")


if __name__ == "__main__":
    main()
