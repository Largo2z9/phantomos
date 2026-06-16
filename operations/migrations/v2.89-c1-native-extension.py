#!/usr/bin/env python3
"""
v2.89 C1 native extension migration (D#500) · idempotente, pattern v2.42-schema-alignment.py.

Migre les instances profile.json existantes vers profile/2.3 :
1. RENAME market_position.awareness_level -> awareness_dominant
   - si la valeur libre matche l'enum awareness-stage canon, on la garde
   - sinon -> null + note dans market_position._notes (jamais inventer)
2. market_position.sophistication_override string libre -> v1..v5 si matche, sinon null + note.

Aucune autre instance touchée (tout le reste du batch C1 est strict additif).
Usage : python3 operations/migrations/v2.89-c1-native-extension.py [--dry-run] [workspace_root]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

AWARENESS_ENUM = {"unaware", "problem_aware", "solution_aware", "product_aware", "most_aware"}
SOPHISTICATION_ENUM = {"v1", "v2", "v3", "v4", "v5"}

# tolérance de normalisation : variantes libres fréquentes -> canon
AWARENESS_ALIASES = {
    "problem-aware": "problem_aware",
    "solution-aware": "solution_aware",
    "product-aware": "product_aware",
    "most-aware": "most_aware",
    "mostaware": "most_aware",
}


def normalize_awareness(value):
    if not isinstance(value, str):
        return None
    v = value.strip().lower().replace(" ", "_")
    v = AWARENESS_ALIASES.get(v, v)
    return v if v in AWARENESS_ENUM else None


def normalize_sophistication(value):
    if not isinstance(value, str):
        return None
    v = value.strip().lower()
    return v if v in SOPHISTICATION_ENUM else None


def migrate_profile(path: Path, dry_run: bool) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # fichier illisible : signaler, ne pas toucher
        print(f"  SKIP (unreadable): {path} ({e})")
        return False

    mp = data.get("market_position")
    if not isinstance(mp, dict):
        return False

    changed = False
    notes = []

    # 1. rename awareness_level -> awareness_dominant (idempotent : absent si déjà migré)
    if "awareness_level" in mp:
        raw = mp.pop("awareness_level")
        canon = normalize_awareness(raw)
        # ne jamais écraser un awareness_dominant déjà posé (idempotence / re-run)
        if "awareness_dominant" not in mp or mp.get("awareness_dominant") in (None, ""):
            mp["awareness_dominant"] = canon
        if canon is None and raw not in (None, ""):
            notes.append(f"C1 migration: awareness_level='{raw}' hors enum awareness-stage -> null (jamais inventer)")
        changed = True

    # 2. sophistication_override : typer ou null
    so = mp.get("sophistication_override")
    if isinstance(so, str) and so.strip():
        canon = normalize_sophistication(so)
        if canon != so:
            mp["sophistication_override"] = canon
            if canon is None:
                notes.append(f"C1 migration: sophistication_override='{so}' hors enum v1-v5 -> null")
            changed = True

    if notes:
        existing = mp.get("_notes") or ""
        sep = " · " if existing else ""
        mp["_notes"] = f"{existing}{sep}{' · '.join(notes)}"

    if changed and not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    args = [a for a in sys.argv[1:]]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    root = Path(args[0]) if args else Path.cwd()

    profiles = sorted(root.glob("brands/*/audiences/**/profile.json"))
    if not profiles:
        print(f"no profile.json under {root}/brands/ · nothing to do")
        return

    migrated = 0
    for p in profiles:
        if migrate_profile(p, dry_run):
            migrated += 1
            print(f"  {'DRY ' if dry_run else ''}migrated: {p.relative_to(root)}")

    print(f"done · {migrated}/{len(profiles)} profile(s) migrated{' (dry-run)' if dry_run else ''}")


if __name__ == "__main__":
    main()
