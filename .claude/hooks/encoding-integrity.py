#!/usr/bin/env python3
"""
PostToolUse hook (matcher Bash) — encoding-integrity gate (D#519).

THE CATEGORY SHIFT · les garanties d'encodage vivent dans le CODE, pas dans la
prose SKILL.md. Tout l'arc D#512-519 a montré que les checkpoints en prose se
font sauter au runtime (le modèle improvise, narre le raisonnement, et l'artefact
reste vide/template). Seul le mécanique tient. Ce hook est le premier mécanique ·
il mord EN VOL sur l'artefact dégénéré, juste après son écriture, et rend la main
au modèle pour qu'il ré-encode (additionalContext, jamais un blocage dur).

Déclencheur · une commande Bash qui invoque write-to-context.py avec
--path brands/{b}/audiences/{a}/profile.json (toute mutation brands/ passe par là).
Sur cette écriture précise, on RELIT l'artefact + le spec lié et on vérifie les
deux prédicats canon (miroir EXACT de resources/scripts/validate-all.py) ·
  a) audience_profile_template_clone  · le profil écrit = le gabarit dégénéré.
  b) use_cases_missing / no_speculative · le pont mécanisme→usage jamais persisté.

Forme canon-correcte (Master rule) · postcondition-sur-artefact-ÉCRIT, jamais
pré-validation du raisonnement. On inspecte l'empreinte disque, après coup.

Garanties dures ·
- Fail-open absolu · tout est wrappé, le hook ne crash JAMAIS le run (exit 0).
- Stdlib only (json/os/re/sys/pathlib), import-light, lecture <=2 fichiers par fire.
- No-op silencieux sur tout ce qui n'est pas une écriture de profil audience réel.
- Skeletons _TEMPLATE/_EXAMPLE/_example exclus DEUX fois (regex [^/_] + startswith).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

WRITE_CTX = re.compile(r"write-to-context\.py\b")
# --path value, optional quotes, '#pointer' fragment stripped
PATH_ARG = re.compile(r"""--path[=\s]+['"]?(brands/[A-Za-z0-9_/-]+\.json)(?:#[^'"\s]*)?['"]?""")
# audience profile under a REAL brand + REAL audience. [^/_] first-char skips
# _TEMPLATE / _EXAMPLE / _example in one shot (same intent as validate-all's
# startswith('_') skeleton guards). Belt; the predicates re-check (suspenders).
AUD = re.compile(r"^brands/([^/_][^/]*)/audiences/([^/_][^/]*)/profile\.json$")


def find_workspace_root(start: Path):
    """Walk up <=12 levels, stop when both brands/ and .skills/ exist."""
    cur = start.resolve()
    for _ in range(12):
        if (cur / "brands").is_dir() and (cur / ".skills").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def load_json(path: Path):
    """Return parsed JSON or None on any error (never raises)."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def check_clone(prof, brand_slug, audience_slug):
    """Mirror validate-all.py audience_profile_template_clone (L584-596)."""
    if brand_slug.startswith("_") or audience_slug.startswith("_"):
        return None
    meta_aud = prof.get("meta", {}) or {}
    jtbd_primary = str(((prof.get("psychology", {}) or {}).get("jtbd", {}) or {}).get("primary") or "")
    ident_desc = str((prof.get("identity", {}) or {}).get("description") or "")
    is_clone = meta_aud.get("slug") == "example-audience" or (
        not meta_aud.get("entry_door") and not jtbd_primary.strip() and not ident_desc.strip()
    )
    if is_clone:
        return ("audiences/%s/profile.json est le template degenere (slug=example-audience, "
                "ou entry_door+jtbd.primary+identity.description tous vides) · le raisonnement "
                "narre n'a jamais atteint l'artefact (split narrate-puis-ecris)" % audience_slug)
    return None


def check_use_cases(spec, brand_slug, prod_slug):
    """Mirror validate-all.py use_cases_missing (L502-509) + use_cases_no_speculative (L485-494)."""
    if prod_slug.startswith("_") or brand_slug.startswith("_"):
        return None
    mechanisms = spec.get("mechanisms") or []
    use_cases = spec.get("use_cases", []) or []
    if mechanisms and not use_cases:
        return ("spec a des mechanisms[] mais ZERO use_cases[] · le pont mecanisme->usage "
                "n'a jamais ete ecrit (carte vide) ; la cartographie d'audiences retombe sur "
                "le miroir des avis")
    if use_cases and not any((u or {}).get("status") == "speculative" for u in use_cases):
        return ("spec.use_cases[] present mais aucun status=speculative · la carte d'expansion "
                "n'a pas d'hypothese (D#502 Mc->U->A) ; ajouter un usage speculatif")
    return None


def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    if data.get("tool_name") != "Bash":
        return
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if not WRITE_CTX.search(cmd):
        return
    m = PATH_ARG.search(cmd)
    if not m:
        return
    rel = m.group(1)
    am = AUD.match(rel)
    if not am:
        return  # only fire on a real audience-profile write
    brand_slug, audience_slug = am.group(1), am.group(2)

    root_str = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(root_str) if root_str else find_workspace_root(Path.cwd())
    if root is None:
        return

    prof = load_json(root / rel)
    if prof is None:
        return  # half-written or unreadable, fail-open

    problems = []
    msg = check_clone(prof, brand_slug, audience_slug)
    if msg:
        problems.append(msg)

    # bound product spec(s): meta.applies_to_products[] (v2.24+) or deprecated meta.product_id
    meta = prof.get("meta", {}) or {}
    prod_slugs = meta.get("applies_to_products") or (
        [meta["product_id"]] if meta.get("product_id") else []
    )
    for ps in prod_slugs:
        if not isinstance(ps, str):
            continue
        spec = load_json(root / "brands" / brand_slug / "products" / ps / "spec.json")
        if spec is None:
            continue
        msg = check_use_cases(spec, brand_slug, ps)
        if msg:
            problems.append(msg)

    if not problems:
        return  # clean artifact, silent no-op

    joined = " · ".join(problems)
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "GATE D'ENCODAGE (D#519) · l'artefact que tu viens d'ecrire est degenere · "
                "le raisonnement narre dans le fil n'a pas atteint le fichier. Probleme(s) · "
                + joined
                + ". Re-encode immediatement via write_to_context les champs manquants (jtbd, "
                "entry_door, conscience pour l'audience · le pont use_cases pour le produit) "
                "AVANT de continuer · ne procede pas tant que l'artefact reste un clone du gabarit "
                "ou que la carte mecanisme->usage est vide. C'est une garantie mecanique, pas une "
                "suggestion."
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
