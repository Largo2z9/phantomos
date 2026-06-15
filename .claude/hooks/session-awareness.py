#!/usr/bin/env python3
"""
SessionStart hook · maintient operator/awareness.json MÉCANIQUEMENT (sprint base-saine).

LE PROBLÈME · le tour était non-idempotent · RIEN n'écrivait `sessions_count` ni
`tour_status` (grep .skills/ + .claude/hooks/ = vide). Donc un opérateur externe qui
faisait le tour sans créer de marque se re-tapait le sas verbatim à la session suivante
(brands/ vide + tour_status=not_started → la First-action re-lançait le tour). La
protection anti-replay vivait 100% dans la mémoire du modèle (prose · D#520).

CE HOOK · à chaque démarrage de session · (1) incrémente `sessions_count` · (2) si une
VRAIE marque existe (brands/{non-_}), marque `tour_status=completed` + `first_brand_validated`.
La First-action clé désormais sur ce signal ÉCRIT, pas sur la mémoire du modèle ·
sessions_count>=2 = opérateur déjà venu → accueil léger, pas le tour verbatim.

Garanties · fail-open absolu (exit 0 toujours), stdlib only, no-op si pas d'awareness.json.
C'est de la maintenance d'état système (comme budget-warn), pas une mutation d'agent ·
le hook tourne hors de la boucle d'outils, donc hors gate mutation.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def find_root(start: Path):
    cur = start.resolve()
    for _ in range(8):
        if (cur / "brands").is_dir() and (cur / "operator").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(env_root) if env_root else find_root(Path(data.get("cwd") or os.getcwd()))
    if root is None or not (root / "operator").is_dir() or not (root / "brands").is_dir():
        return

    aw_path = root / "operator" / "awareness.json"
    try:
        aw = json.loads(aw_path.read_text(encoding="utf-8"))
    except Exception:
        return  # pas d'awareness.json lisible · fail-open
    if not isinstance(aw, dict):
        return

    try:
        aw["sessions_count"] = int(aw.get("sessions_count") or 0) + 1
    except Exception:
        aw["sessions_count"] = 1

    # une vraie marque encodée = le tour est forcément derrière nous
    has_brand = any(
        p.is_dir() and not p.name.startswith("_")
        for p in (root / "brands").iterdir()
    )
    if has_brand:
        aw["tour_status"] = "completed"
        aw["first_brand_validated"] = True

    try:
        aw_path.write_text(json.dumps(aw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
