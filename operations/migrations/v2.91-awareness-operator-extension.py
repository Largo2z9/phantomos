#!/usr/bin/env python3
"""
Migration v2.91 · awareness.json schema v1.1 → v1.2

Adds NEW field canon v2.91.1 que tour.md écrit sur le chemin tool-first ·
- first_operator_extension_built (boolean · null default · NEW v2.91.1 Porte D scaffold:operator)

Le chemin tool-first (Porte D → scaffold-extension operator-scope) produit un premier
livrable non-marque (extension opérateur · contacts, prestataires, projets, admin...),
équivalent en dignité à l'atlas. Ce champ miroir de first_brand_validated permet au close
M3 et au replay M4 de reconnaître ce territoire substrat.

Idempotent · re-run safe · backup horodaté avant patch. Chaîne après v2.87.0 (v1.0 → v1.1).

Usage ·
    python3 operations/migrations/v2.91-awareness-operator-extension.py [workspace_path]

Default workspace_path = current dir.
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def migrate_awareness(workspace_path: Path) -> dict:
    awareness_path = workspace_path / "operator" / "awareness.json"

    if not awareness_path.exists():
        return {"status": "skip", "reason": "awareness.json absent · fresh workspace use template"}

    with awareness_path.open("r") as f:
        data = json.load(f)

    current_version = data.get("_version", "1.0")

    if current_version == "1.2":
        return {"status": "skip", "reason": "already v1.2 · idempotent"}

    if current_version != "1.1":
        return {
            "status": "error",
            "reason": f"expected v1.1 (run v2.87.0 migration first), got {current_version}",
        }

    backup_path = awareness_path.with_suffix(f".bak.{datetime.now().strftime('%Y-%m-%d')}")
    shutil.copy2(awareness_path, backup_path)

    data["_version"] = "1.2"

    data.setdefault("_field_types", {}).update({
        "first_operator_extension_built": "derived",
    })

    data.setdefault("first_operator_extension_built", None)

    ordered_keys = [
        "_version", "_schema", "_field_types",
        "tour_status", "tour_entry_door", "tour_last_run", "sessions_count",
        "concepts_introduced", "paths_explored", "paths_skipped",
        "first_deliverable_built", "first_deliverable_skill",
        "first_deliverable_validated_corrections",
        "first_operator_extension_built",
        "first_skill_offered", "first_skill_built", "first_brand_validated",
    ]
    ordered_data = {k: data[k] for k in ordered_keys if k in data}
    for k, v in data.items():
        if k not in ordered_data:
            ordered_data[k] = v

    with awareness_path.open("w") as f:
        json.dump(ordered_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return {
        "status": "migrated",
        "from_version": "1.1",
        "to_version": "1.2",
        "backup": str(backup_path.name),
        "fields_added": ["first_operator_extension_built"],
    }


if __name__ == "__main__":
    workspace = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    result = migrate_awareness(workspace)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] in ("migrated", "skip") else 1)
