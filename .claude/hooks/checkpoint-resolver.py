#!/usr/bin/env python3
"""
checkpoint-resolver · UserPromptSubmit hook.

If the user's message resolves a staged workflow proposal (confirm/reject
pattern match on any brand's .workflow.json#/pending), promote or clear the
pending entry, append to history, set the checkpoint flag accordingly.

This is the ONLY path by which a workflow checkpoint becomes true. Agents
cannot self-mark, because checkpoint state is written from a UserPromptSubmit
hook whose input is the literal user text · not agent output.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

CONFIRM_PATTERNS = [
    r"\boui\b", r"\byes\b", r"\byep\b", r"\bok\b", r"\bgo\b", r"\bconfirm(e|é|ed)?\b",
    r"\bvalide(z|é|és|ée|ées)?\b", r"\bparfait\b", r"\bexact\b", r"\bcorrect\b", r"\byup\b",
    r"✓", r"👍", r"\bc'est bon\b", r"\bc bon\b",
    # Franglais Largo
    r"\bc good\b", r"\bnickel\b", r"\bdac\b", r"\bd'acc\b", r"\bcrème\b", r"\bclean\b",
    r"\btop\b", r"\bcool\b", r"\bniquel\b", r"\bok c bon\b",
    # NEW v2.87.4 · AskUserQuestion canon response patterns
    # Resolves friction audit Fincut v2.87.3 · opérateur sélectionne option AskUserQuestion (e.g. "Validé, encode comme ça")
    # puis devait retaper "go"/"ok" séparément · hook lit user text seulement · option label suffit désormais
    r"\bencode\b", r"\blance\b", r"\bjette[zs]?\b",
    r"\bça\s+(va|me\s+va|m'va|colle)\b", r"\bca\s+(va|me\s+va|m'va|colle)\b",
    r"\b(comme\s+ça|comme\s+ca|comme\s+ça\s+oui|comme\s+ca\s+oui)\b",
    r"\b(je\s+valide|j'valide)\b",
    r"\b(envoie|envoyez)\b",
    r"\b(roule|on\s+y\s+va|on\s+est\s+bon)\b",
]
REJECT_PATTERNS = [
    r"\bnon\b", r"\bno\b", r"\bnope\b", r"\bskip\b", r"\bpas\b.*\b(bon|ok|ça)\b",
    r"\breject(e|ed)?\b", r"\bfaux\b", r"\bincorrect\b", r"\bmauvais\b", r"\bpas du tout\b",
    r"\bnan\b", r"\bstop\b", r"\bannule\b", r"\bpas ça\b",
]
# Nuance connectors · indicate a partial accept with embedded corrections.
# When present, the response is a REFINE: agent must re-stage with corrections
# integrated, then re-ask for clean confirmation.
REFINE_PATTERNS = [
    r"\bmais\b", r"\bsauf\b", r"\bplutôt\b", r"\bplutot\b", r"\bpar contre\b",
    r"\bet dès\b", r"\bet des\b", r"\benlève\b", r"\benleve\b", r"\bajoute\b",
    r"\brajoute\b", r"\bmodifie\b", r"\bchange\b", r"\bsauf que\b", r"\bpresque\b",
    r"\bpresqu'\b", r"\bà part\b", r"\ba part\b", r"\bretire\b",
]


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def classify(text: str) -> str | None:
    lower = text.lower()
    has_confirm = any(re.search(p, lower) for p in CONFIRM_PATTERNS)
    has_reject = any(re.search(p, lower) for p in REJECT_PATTERNS)
    has_refine = any(re.search(p, lower) for p in REFINE_PATTERNS)

    # Overlap rule: refine trumps confirm (conservative · partial accept with
    # embedded corrections must be re-staged, not silently locked in).
    if has_refine and has_confirm:
        return "refine"
    if has_confirm:
        return "confirm"
    if has_reject:
        return "reject"
    if has_refine:
        # Refine without confirm = ambiguous corrective feedback, treat as refine
        return "refine"
    return None


def load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def save_json(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def resolve_brand(brand_dir: Path, prompt: str) -> str | None:
    wf_path = brand_dir / ".workflow.json"
    if not wf_path.exists():
        return None
    state = load_json(wf_path)
    pending = state.get("pending")
    if not pending:
        return None

    decision = classify(prompt)
    if decision is None:
        return None

    checkpoint = pending.get("checkpoint")
    product_slug = pending.get("product_slug")
    history_entry = {
        "resolved_at": datetime.utcnow().isoformat() + "Z",
        "checkpoint": checkpoint,
        "product_slug": product_slug,
        "summary": pending.get("summary"),
        "decision": decision,
        "operator_text": prompt.strip()[:500],
    }
    state.setdefault("history", []).append(history_entry)

    # Refine: keep pending, log decision, agent must re-stage with corrections
    # integrated and re-ask for clean confirmation. Checkpoint NOT promoted.
    if decision == "refine":
        save_json(wf_path, state)
        return f"{decision}:{checkpoint}" + (f":{product_slug}" if product_slug else "")

    state["pending"] = None

    if decision == "confirm":
        if checkpoint == "confirmed_products":
            lst = state["checkpoints"].setdefault("confirmed_products", [])
            if product_slug and product_slug not in lst:
                lst.append(product_slug)
        else:
            state["checkpoints"][checkpoint] = True

    save_json(wf_path, state)
    return f"{decision}:{checkpoint}" + (f":{product_slug}" if product_slug else "")


# --- Operator FUNCTION capture (le rooting du profil · D#52x) -----------------
# Le run live a prouvé que la fonction de l'opérateur ne root pas · il dit
# « je fais le paid » et profile.json reste null (la maladie D#520 à la couche
# opérateur). Ce hook voit le prompt littéral · c'est le BON étage pour inférer
# la fonction depuis le langage (session-awareness ne reçoit que cwd). Il écrit
# operator/profile.json#identity.function UNIQUEMENT si vide (jamais clobber), en
# inférence, et marque awareness.function_inferred=true (sémantique « proposé, à
# confirmer »). Fail-open absolu · une capture ratée ne casse jamais le prompt.

FUNCTION_FRAMES = [
    r"\bje fais (le |la |du |de la |de l'|que du |que de la |que de l'|surtout |principalement |essentiellement )",
    r"\bje (gère|gere|manage|pilote|drive) (le |la |les |leur |du |de la )",
    r"\bje m'occupe (du |de la |des |de l'|de )",
    r"\bje bosse (sur|en|dans) ",
    r"\bje leur (fais|gère|gere) (le |la |du |de la )",
    r"\bmon (job|poste|métier|metier|rôle|role|taf|boulot) (c'est|est|c)",
    r"\bje suis (le |la |un |une |en )?(media ?buyer|cro|copywriter|analyste|traffic manager|growth|dir(ecteur)? ?créa|data ?analyst)",
    r"\bc'est moi qui (fais|gère|gere|m'occupe)",
    r"\bje fais que ",
]
# Signaux par pôle, ordre canonique (les 9 pôles canon · vue flat, pas une hiérarchie).
POLE_SIGNALS = {
    "paid": [r"\bpaid\b", r"\bmédia ?buy", r"\bmedia ?buy", r"\bachat média", r"\bachat media",
             r"\bmeta ads?\b", r"\bfacebook ads?\b", r"\bgoogle ads?\b", r"\bacquisition payante",
             r"\bads manager", r"\bbudgets? (pub|média|media|paid)"],
    "creative": [r"\bstratégie créa", r"\bstrategie crea", r"\bcreative strateg", r"\bconcepts? (créa|publicitaires)",
                 r"\bveille créa", r"\btesting créa", r"\bpost-?mortems?\b", r"\bbriefs? créa"],
    "studio": [r"\bstudio\b", r"\bmontage\b", r"\bproduction (vidéo|video)", r"\bugc\b",
               r"\bdirection artistique", r"\bgraphis", r"\bmotion design", r"\bje fais (les|des) créas?\b"],
    "conversion": [r"\bcro\b", r"\bconversion\b", r"\blanding ?pages?\b", r"\bfiches? produit", r"\bpdp\b",
                   r"\bcheckout\b", r"\btaux de (conv|transfo)", r"\ba/?b ?test", r"\boptimisation? (des? )?pages?"],
    "retention": [r"\bemail(ing)?\b", r"\bcrm\b", r"\bnewsletter", r"\brétention\b", r"\bretention\b",
                  r"\bklaviyo", r"\bsms\b", r"\blifecycle", r"\bautomations?\b", r"\bflows?\b", r"\bfidélisation"],
    "intelligence": [r"\btracking\b", r"\banalytics?\b", r"\battribution\b", r"\breporting\b", r"\bga ?4\b",
                     r"\bcohort", r"\btableau de bord", r"\bdashboard", r"\bla mesure\b", r"\bla data\b"],
    "ops": [r"\bsupply\b", r"\blogistique", r"\bfulfillment", r"\ble stock\b", r"\ble catalogue\b",
            r"\bservice client", r"\bles opérations?\b", r"\bsav\b"],
    "finance": [r"\bfinance\b", r"\bmarges?\b", r"\bp&l\b", r"\brentabilité", r"\bunit economics",
                r"\bcashflow", r"\btrésorerie", r"\bforecast"],
    "growth": [r"\bgrowth\b", r"\bstratégie globale", r"\bgo-?to-?market", r"\bchannel mix", r"\bla roadmap\b",
               r"\barbitrages?\b", r"\bla strat\b", r"\bstratège"],
}


def detect_functions(prompt: str) -> list:
    lower = prompt.lower()
    if not any(re.search(f, lower) for f in FUNCTION_FRAMES):
        return []
    found = []
    for pole, sigs in POLE_SIGNALS.items():
        if any(re.search(s, lower) for s in sigs):
            found.append(pole)
    return found


def capture_operator_function(root: Path, prompt: str) -> list | None:
    prof_path = root / "operator" / "profile.json"
    if not prof_path.exists():
        return None
    prof = load_json(prof_path)
    if not isinstance(prof, dict):
        return None
    identity = prof.get("identity")
    if not isinstance(identity, dict):
        return None
    # Idempotent · jamais écraser une fonction déjà posée (stated ou déjà inférée).
    if identity.get("function"):
        return None
    poles = detect_functions(prompt)
    if not poles:
        return None
    identity["function"] = poles
    meta = prof.setdefault("_meta", {})
    if isinstance(meta, dict):
        meta["last_updated"] = datetime.utcnow().isoformat() + "Z"
        meta["last_enriched_by"] = "checkpoint-resolver(inference-function)"
    save_json(prof_path, prof)
    # Marqueur « proposé, à confirmer » · l'onboard/le runtime confirme d'un mot.
    aw_path = root / "operator" / "awareness.json"
    if aw_path.exists():
        aw = load_json(aw_path)
        if isinstance(aw, dict):
            aw["function_inferred"] = True
            aw["function_capture_lever"] = "inférée du langage opérateur · confirmer ou corriger d'un mot"
            save_json(aw_path, aw)
    return poles


def _function_l2_wanted(func: list, root: Path) -> bool:
    """True si AU MOINS une fonction consomme la production L2 (light/full). Lit la SSOT
    `function-pole-map.json`. Vide → True (FULL). Map illisible → True (fail-safe · ne
    conditionne pas à l'aveugle). Même logique que validate-all.load_operator_function_ctx."""
    if not func:
        return True
    try:
        poles = json.loads((root / "resources" / "canon" / "operator" / "function-pole-map.json").read_text(encoding="utf-8")).get("poles", {}) or {}
        return any((poles.get(p, {}).get("layers", {}) or {}).get("L2_production") in ("light", "full") for p in func)
    except Exception:
        return True


def sync_function_scope(root: Path) -> None:
    """Dérive `l2_wanted` depuis la fonction ÉCRITE et l'écrit MÉCANIQUEMENT dans
    `awareness.json#function_scope_l2` (on/off). L'orchestrateur (build-atlas Step 0ter) LIT
    ce champ écrit pour décider de skipper Phase 6/7 · il ne re-dérive PAS en prose (D#520 ·
    les garanties dans le code, pas dans la prose que le runtime improvise · revue adverse
    du chapitre fonction). Idempotent (n'écrit que si la valeur change), fail-open."""
    prof_path = root / "operator" / "profile.json"
    aw_path = root / "operator" / "awareness.json"
    if not prof_path.exists() or not aw_path.exists():
        return
    try:
        func = (load_json(prof_path).get("identity", {}) or {}).get("function") or []
        if not isinstance(func, list):
            func = []
    except Exception:
        func = []
    l2 = "on" if _function_l2_wanted(func, root) else "off"
    try:
        aw = load_json(aw_path)
        if isinstance(aw, dict) and aw.get("function_scope_l2") != l2:
            aw["function_scope_l2"] = l2
            save_json(aw_path, aw)
    except Exception:
        pass


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "")
    if not prompt or len(prompt) > 2000:
        sys.exit(0)

    cwd = Path(payload.get("cwd") or os.getcwd())
    root = find_workspace_root(cwd)
    if root is None:
        sys.exit(0)

    # Brick 2 · root la FONCTION de l'opérateur depuis le prompt (fail-open · une
    # capture ratée ne casse jamais le prompt ni la résolution de checkpoint).
    fn_captured = None
    try:
        fn_captured = capture_operator_function(root, prompt)
    except Exception:
        fn_captured = None
    # Dérive `function_scope_l2` de la fonction ÉCRITE et le persiste (D#520 · le routage
    # Phase 6/7 lit un champ écrit, pas une re-dérivation en prose). Tourne à chaque prompt
    # pour rester à jour même si la fonction a été posée en session antérieure. Fail-open.
    try:
        sync_function_scope(root)
    except Exception:
        pass

    brands_dir = root / "brands"
    if not brands_dir.is_dir():
        sys.exit(0)

    resolutions = []
    for brand_dir in brands_dir.iterdir():
        if not brand_dir.is_dir() or brand_dir.name.startswith("_"):
            continue
        r = resolve_brand(brand_dir, prompt)
        if r:
            resolutions.append(f"{brand_dir.name}:{r}")

    if resolutions or fn_captured:
        log = root / ".phantom"
        log.mkdir(exist_ok=True)
        entry = {"ts": datetime.utcnow().isoformat() + "Z"}
        if resolutions:
            entry["resolutions"] = resolutions
        if fn_captured:
            entry["function_captured"] = fn_captured
        with (log / "checkpoint-resolver.log").open("a") as f:
            f.write(json.dumps(entry) + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
