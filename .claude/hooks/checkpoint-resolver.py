#!/usr/bin/env python3
"""
checkpoint-resolver — UserPromptSubmit hook.

If the user's message resolves a staged workflow proposal (confirm/reject
pattern match on any brand's .workflow.json#/pending), promote or clear the
pending entry, append to history, set the checkpoint flag accordingly.

This is the ONLY path by which a workflow checkpoint becomes true. Agents
cannot self-mark, because checkpoint state is written from a UserPromptSubmit
hook whose input is the literal user text — not agent output.
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
# Nuance connectors — indicate a partial accept with embedded corrections.
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

    # Overlap rule: refine trumps confirm (conservative — partial accept with
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

    if resolutions:
        log = root / ".phantom"
        log.mkdir(exist_ok=True)
        with (log / "checkpoint-resolver.log").open("a") as f:
            f.write(json.dumps({
                "ts": datetime.utcnow().isoformat() + "Z",
                "resolutions": resolutions,
            }) + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
