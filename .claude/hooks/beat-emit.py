#!/usr/bin/env python3
"""
PostToolUse hook (matcher Task) · beat-emit · garantie de RESTITUTION (D#520).

LE PROBLÈME · le run onday a produit un raisonnement dense (sources lues, rejets
argumentés, confiance-avec-raison) puis l'a écrasé en une phrase météo. La cause ·
le ton SKILL ordonne « une phrase par handoff », et la prose se fait sauter au
runtime. Seul le mécanique tient.

CE HOOK · quand un sous-agent Task vient de finir (deep-scan, etc.), il vérifie si
le producteur a laissé un BEAT-PAYLOAD frais et NON ENCORE ÉMIS
(.phantom/beats/{slug}/{phase}.json sans sibling .emitted). Si oui, il pousse
l'orchestrateur à RENDRE le beat (les 3 couches trouvé/analysé/encodé + le pointeur
/phantom) au lieu de narrer une météo. Trigger mécanique (fin de Task, payload sur
disque), contenu sémantique (le modèle émet) · split Master rule respecté.

Le renderer (.skills/render-beat.py) écrit le marqueur .emitted · le hook ne
re-pousse jamais un beat déjà rendu. Forme canon · post-hoc, additionalContext,
jamais un blocage dur.

Garanties · fail-open absolu (exit 0 toujours), stdlib only, no-op silencieux si
aucun payload non-émis frais.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Un payload plus vieux que ça n'est plus « le scan qui vient de finir » · on ne
# harcèle pas sur un run abandonné il y a des heures.
FRESH_WINDOW_S = 1800  # 30 min


def find_workspace_root(start: Path):
    cur = start.resolve()
    for _ in range(12):
        if (cur / "brands").is_dir() and (cur / ".skills").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    if data.get("tool_name") != "Task":
        return

    root_str = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(root_str) if root_str else find_workspace_root(Path.cwd())
    if root is None:
        return

    beats_root = root / ".phantom" / "beats"
    if not beats_root.is_dir():
        return

    now = time.time()
    pending = []  # (slug, phase)
    for brand_path in beats_root.iterdir():
        if not brand_path.is_dir() or brand_path.name.startswith("_"):
            continue
        for payload in brand_path.glob("*.json"):
            phase = payload.stem
            if (brand_path / ("%s.emitted" % phase)).exists():
                continue  # déjà rendu
            try:
                if now - payload.stat().st_mtime > FRESH_WINDOW_S:
                    continue  # pas frais, on ne harcèle pas
            except Exception:
                continue
            pending.append((brand_path.name, phase))

    if not pending:
        return  # rien à émettre, no-op silencieux

    cmds = " · ".join(
        "`python3 .skills/render-beat.py --brand %s --phase %s`" % (s, p)
        for s, p in pending
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "BEAT DE RESTITUTION en attente (D#520) · le sous-agent a laissé un "
                "registre frais de son travail (trouvé / analysé / rejeté / encodé / "
                "confiance-avec-raison) qui n'a pas encore été montré à l'opérateur. "
                "Émets-le MAINTENANT en exécutant " + cmds + " et présente sa sortie "
                "telle quelle (les 3 couches + le pointeur /phantom). NE compresse PAS "
                "en une phrase météo · le travail doit être visible. C'est une garantie "
                "mécanique, pas une suggestion."
            ),
        }
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
