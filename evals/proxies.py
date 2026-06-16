#!/usr/bin/env python3
"""
proxies.py · Cheap, deterministic discriminators for the quality eval.

These are NOT the eval. They are the fast, stdlib-only floor under the LLM judge:
a handful of surface signals that separate a close that *tranche* (decides a move)
from a close that *describes* and hands the operator a menu of questions. The judge
(see judge.md) carries the semantic verdict, calibrated by operator ratings
(ratings.jsonl). The proxies catch the obvious failures for free and give the judge
a sanity anchor.

Design contract (matches evals/README.md):
  - hors-runtime: nothing here ever touches the write path. It reads golden artifacts
    off disk and scores text. It never imports the workspace, never mutates a brand.
  - stdlib only (json, re, pathlib, sys). Runs under python3.11.
  - a rubric declares which proxies apply to its artifact (typed registry). This file
    is the library of named checks; the rubric wires them.

Each check takes the artifact body (str) and returns a numeric signal (a count, a
density, or 0/1 for a boolean). The runner converts signal -> sharp/mushy contribution
using the rubric's {direction, weight, threshold}.
"""

import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Golden file parsing
# --------------------------------------------------------------------------- #

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_golden(path):
    """Parse a golden markdown file with a tiny YAML-ish frontmatter.

    Frontmatter keys (flat, string values): artifact, label, brand, note.
    Returns {"artifact","label","brand","note","body","path"}.
    No PyYAML dependency: we only read flat `key: value` lines.
    """
    text = Path(path).read_text(encoding="utf-8")
    meta = {"artifact": "", "label": "", "brand": "", "note": "", "path": str(path)}
    m = _FRONTMATTER_RE.match(text)
    body = text
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                k = k.strip()
                if k in meta:
                    meta[k] = v.strip().strip('"').strip("'")
        body = text[m.end():]
    meta["body"] = body.strip()
    return meta


# --------------------------------------------------------------------------- #
# Text helpers
# --------------------------------------------------------------------------- #

def _words(text):
    return re.findall(r"\b[\wàâäéèêëïîôöùûüç'-]+\b", text.lower())


def _lines(text):
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def _last_meaningful_line(text):
    ls = _lines(text)
    return ls[-1] if ls else ""


# --------------------------------------------------------------------------- #
# Lexicons (FR + EN). Surface markers only. The judge handles nuance.
# --------------------------------------------------------------------------- #

# Decision / move verbs: the close commits to a next move, defended.
# Kept tight: "en priorité" (a menu phrase) must NOT read as a verdict, so the bare
# "priorité" is excluded; only "la priorité" / "priorité 1" count.
_DECISION_MARKERS = [
    r"\bje partirais\b", r"\ble move\b", r"\bla priorité\b", r"\bpriorité\s*1\b",
    r"\bon attaque\b", r"\bje recommande\b", r"\bje pousse\b", r"\bcommence par\b",
    r"\bpremière action\b", r"\bà faire en premier\b", r"\ble premier move\b",
    r"\bmon verdict\b", r"\bje te propose d'attaquer\b", r"\bon part sur\b",
    r"\bje pars sur\b", r"\bl'angle gagnant\b", r"\ble pari\b", r"\bje trancherais\b",
    # EN
    r"\bi'd start\b", r"\bthe move\b", r"\bmy call\b", r"\bi recommend\b",
    r"\bfirst move\b", r"\bstart with\b", r"\bthe bet\b", r"\bi'd ship\b",
]

# Choice handed to the operator: the close outsources the DECISION ("which do you want?").
_OPERATOR_SOLICIT = [
    r"\btu veux\b", r"\bveux-tu\b", r"\blequel\b", r"\blaquelle\b", r"\bà toi de\b",
    r"\bqu'est-ce que tu\b", r"\btu préfères\b", r"\btu choisis\b", r"\btu pars sur\b",
    r"\bdis-moi\b", r"\btu en penses quoi\b", r"\bon creuse quoi\b", r"\btu valides\b",
    # EN
    r"\bdo you want\b", r"\bwhich one\b", r"\byour call\b", r"\bup to you\b",
    r"\bwhat do you\b", r"\bwhich would you\b",
]

# Info requested FROM the operator: solicitation markers plus possessives and
# interrogatives that ask the operator to supply data. Used to count homework
# questions (one gate is fine; two or more is setup-by-interrogation).
_OPERATOR_ASK = _OPERATOR_SOLICIT + [
    r"\bton\b", r"\bta\b", r"\btes\b", r"\bquel est\b", r"\bquelle est\b",
    r"\bcombien\b", r"\bas-tu\b", r"\bavez-vous\b", r"\byour\b", r"\bhow much\b",
]

# Hedge markers: soften a claim into mush.
_HEDGE_MARKERS = [
    r"\bpeut-être\b", r"\bil faudrait\b", r"\bon pourrait\b", r"\bça dépend\b",
    r"\bsans doute\b", r"\ba priori\b", r"\bje pense que\b", r"\bil semble\b",
    r"\bprobablement\b", r"\bplutôt\b", r"\béventuellement\b", r"\bpossiblement\b",
    # EN
    r"\bmaybe\b", r"\bperhaps\b", r"\bit depends\b", r"\bwe could\b", r"\bit seems\b",
    r"\bprobably\b", r"\bmight\b",
]

# Negative-coordinate markers for angles: what the angle stands AGAINST.
_NEGATIVE_MARKERS = [
    r"\bcontre\b", r"\bau lieu de\b", r"\bpas\s+(?:un|une|du|de la|le|la)\b",
    r"\bvs\b", r"\bversus\b", r"\bplutôt que\b", r"\bni\b.*\bni\b", r"\bsans\b",
    r"\binstead of\b", r"\bnot a\b", r"\brather than\b", r"\bunlike\b",
]

# Hollow wellness / landing-page filler: signals an artifact that decorates without
# deciding or standing for anything. The 'could be any brand' tell, made deterministic.
_GENERIC_MARKERS = [
    r"meilleure version de toi", r"te sentir bien", r"tu mérites", r"en douceur",
    r"au quotidien", r"bien dans ton corps", r"atteindre tes objectifs",
    r"reprends le contrôle", r"accompagne vers", r"naturel,?\s+sain", r"en confiance",
    r"bien-être", r"se sentir bien", r"version de toi-même",
    # EN
    r"best version of yourself", r"feel your best", r"you deserve",
    r"wellness journey", r"your best self",
]

# Menu-option lines: "A ·", "B ·", "1.", "2." used as a choose-your-axis menu.
_MENU_LINE_RE = re.compile(
    r"^\s*(?:[A-E]\s*[·\.\):]|[1-5]\s*[·\.\):])\s+\S", re.MULTILINE
)


def _count(patterns, text):
    low = text.lower()
    return sum(1 for p in patterns if re.search(p, low))


# --------------------------------------------------------------------------- #
# Named checks (the registry). Each returns a numeric signal.
# --------------------------------------------------------------------------- #

def has_decision_verb(body):
    """1 if the close commits to a move, else 0."""
    return 1 if _count(_DECISION_MARKERS, body) >= 1 else 0


def ends_with_operator_question(body):
    """1 if the last line is a question handed to the operator, else 0."""
    last = _last_meaningful_line(body)
    if "?" not in last:
        return 0
    return 1 if _count(_OPERATOR_SOLICIT, last) >= 1 else 0


def menu_of_axes(body):
    """Count of menu-option lines (A· / B· / 1. / 2. ...)."""
    return len(_MENU_LINE_RE.findall(body))


def question_to_operator_count(body):
    """Count of question lines that ask the operator to supply info or decide."""
    n = 0
    for ln in _lines(body):
        if "?" in ln and _count(_OPERATOR_ASK, ln) >= 1:
            n += 1
    return n


def question_count(body):
    """Raw count of question marks (open questions, any addressee)."""
    return body.count("?")


def hedge_density(body):
    """Hedge markers per 100 words."""
    w = _words(body)
    if not w:
        return 0.0
    hedges = sum(len(re.findall(p, body.lower())) for p in _HEDGE_MARKERS)
    return round(hedges * 100.0 / len(w), 2)


def has_negative_coordinate(body):
    """1 if an angle names what it stands against, else 0."""
    return 1 if _count(_NEGATIVE_MARKERS, body) >= 1 else 0


def generic_filler(body):
    """Count of hollow wellness/landing filler phrases (the 'any brand' tell)."""
    return _count(_GENERIC_MARKERS, body)


def has_confidence_chain(body):
    """1 if the text carries explicit confidence language, else 0."""
    markers = [r"\bconfidence\b", r"\bhypothèse\b", r"\bdéduit\b", r"\bobservé\b",
               r"\bà valider\b", r"\bforte\b", r"\bmoyenne\b", r"\bfaible\b",
               r"\bincertain\b", r"\bsourc"]
    return 1 if _count(markers, body) >= 2 else 0


CHECKS = {
    "has_decision_verb": has_decision_verb,
    "ends_with_operator_question": ends_with_operator_question,
    "menu_of_axes": menu_of_axes,
    "question_to_operator_count": question_to_operator_count,
    "question_count": question_count,
    "hedge_density": hedge_density,
    "has_negative_coordinate": has_negative_coordinate,
    "has_confidence_chain": has_confidence_chain,
    "generic_filler": generic_filler,
}


# --------------------------------------------------------------------------- #
# Rubric application
# --------------------------------------------------------------------------- #

def run_proxies(body, proxy_specs):
    """Apply a rubric's proxy list to a body.

    proxy_specs: list of {name, direction(sharp|mushy), weight, threshold?}.
    A check fires when its signal crosses the threshold (default >=1 for booleans
    and counts). A firing 'sharp' proxy adds +weight, a firing 'mushy' proxy
    subtracts weight. Returns {"score","verdict","signals":[...]}.
    """
    score = 0.0
    signals = []
    for spec in proxy_specs:
        name = spec["name"]
        fn = CHECKS.get(name)
        if fn is None:
            signals.append({"name": name, "error": "unknown check"})
            continue
        raw = fn(body)
        threshold = spec.get("threshold", 1)
        fired = raw >= threshold
        weight = float(spec.get("weight", 1))
        direction = spec.get("direction", "sharp")
        contribution = 0.0
        if fired:
            contribution = weight if direction == "sharp" else -weight
        score += contribution
        signals.append({
            "name": name, "raw": raw, "threshold": threshold,
            "fired": fired, "direction": direction, "contribution": contribution,
        })
    verdict = "sharp" if score > 0 else ("mushy" if score < 0 else "neutral")
    return {"score": round(score, 2), "verdict": verdict, "signals": signals}


if __name__ == "__main__":
    # Smoke: parse + dump signals for a golden file passed as arg.
    if len(sys.argv) < 2:
        print("usage: proxies.py <golden.md>", file=sys.stderr)
        sys.exit(2)
    g = parse_golden(sys.argv[1])
    print(f"artifact={g['artifact']} label={g['label']} brand={g['brand']}")
    for name, fn in CHECKS.items():
        print(f"  {name:32s} = {fn(g['body'])}")
