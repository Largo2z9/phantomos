#!/usr/bin/env python3
"""validate-skill-reachability · garde-fou anti-décrochage doctrine <-> skill.

Attrape la classe de bug exposée par D#509 : un skill nommé dans la carte de
câblage d'une doctrine mais décroché du pipeline (silencieusement non invoqué),
plus les références fantômes (skill renommé / supprimé / typo / objet non-skill
pris pour un skill). Mécanique, sans jugement sémantique (cf Master rule du
workspace · mécanique = gate strict, sémantique = trust the model).

4 checks ·
  A. CRITICAL · toute référence chemin `.skills/skills/{name}/` pointe un skill réel.
  B. HIGH     · tout token en backtick à forme de skill (préfixe verbe) existe au manifest.
  C. HIGH     · tout skill nommé dans une doctrine-pipeline est atteignable (référencé)
                dans son ou ses orchestrateurs · sinon décrochage doctrine<->skill.
  D. WARN     · skill du manifest référencé nulle part hors de son propre SKILL.md (dormant).

Exit 1 si au moins un CRITICAL ou HIGH. WARN n'échoue pas (liste de revue).
Usage · python3 resources/scripts/validate-skill-reachability.py [--strict] [--json]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # workspace-template/
MANIFEST = ROOT / ".skills/_manifest.json"
SKILLS_DIR = ROOT / ".skills/skills"
DOCS = ROOT / "docs"
COMMANDS = ROOT / ".claude/commands"

# Doctrine-pipeline -> orchestrateurs qui doivent rendre ses skills atteignables.
# La doctrine NOMME le câblage, l'orchestrateur le LIVRE. Si un skill nommé par
# la doctrine n'apparait dans aucun orchestrateur, c'est le décrochage de D#509.
PIPELINE_MAP = [
    {
        "doctrine": DOCS / "system/onboarding-setup-flow.md",
        "orchestrators": [
            SKILLS_DIR / "build-atlas-complete/SKILL.md",
            SKILLS_DIR / "onboard-brand/SKILL.md",
        ],
        # Skills que la doctrine nomme explicitement comme NON chaînés par défaut
        # (subsumés ou standalone) · documentés tels quels dans la doctrine, pas un décrochage.
        "allow_unwired": {"mine-audience", "score-product-fit"},
    },
]

# Segments de chemin `.skills/skills/X/` qui ne sont PAS des skills · conventions
# de dossier (tiers Core/Community, dossier d'extensions) ou noms historiques cités
# par design dans les journaux et guides de conversion (cf D#494 audit-meta-global = un SOP).
NON_SKILL_PATHSEG = {
    "custom", "core", "community",
    "audit-meta-global", "daily-brief", "onboard-brand-full", "snapshot",
    # non-skills cités en contexte d'invocation · un type d'agent et une fonction système
    "explore-codebase", "recompute-derived-fields",
}

# Docs qui citent légitimement des noms de skills morts ou futurs (journaux, releases,
# roadmaps, guides de conversion) · hors canon runtime, exclus de la chasse aux phantoms.
def is_historical_doc(path):
    s = str(path)
    return (
        "/docs/internal/" in s
        or "/docs/vision/roadmap" in s
        or s.endswith("sop-skill-conversion.md")
    )

SKILL_SHAPE = re.compile(r"^[a-z][a-z0-9]+(?:-[a-z0-9]+)+$")
PATH_RE = re.compile(r"\.skills/skills/([a-z0-9][a-z0-9-]+)/")
# CHECK B · phantom en CONTEXTE D'INVOCATION uniquement (un skill qu'on prétend appeler
# mais qui n'existe pas) · bien plus fiable que « tout token à forme de skill en prose ».
INVOKE_RE = re.compile(
    r"(?:invoke|invoquer|invoque|d[ée]l[ée]gu[eé]r?\s+[àa]|delegate to|spawn|route to|route vers|cha[îi]ne[r]?|\bchain\b|skill)\s+`([a-z][a-z0-9-]+)`",
    re.IGNORECASE,
)
INVOKE_TASK_RE = re.compile(r"`([a-z][a-z0-9-]+)`\s*(?:\(Task|via Task)")


def load_skill_names():
    m = json.loads(MANIFEST.read_text())
    skills = m["skills"] if isinstance(m, dict) and "skills" in m else m
    items = skills.values() if isinstance(skills, dict) else skills
    return {s["name"] for s in items if isinstance(s, dict) and s.get("name")}


def word_present(name, text):
    return re.search(r"(?<![a-z0-9-])" + re.escape(name) + r"(?![a-z0-9-])", text) is not None


def main():
    strict = "--strict" in sys.argv
    as_json = "--json" in sys.argv
    skill_names = load_skill_names()
    md_files = list(DOCS.rglob("*.md")) + list(SKILLS_DIR.rglob("SKILL.md"))
    findings = []  # (severity, file, msg)

    def add(sev, f, msg):
        findings.append((sev, str(f).replace(str(ROOT) + "/", ""), msg))

    # CHECK A · phantom path references (.skills/skills/{name}/ -> skill réel)
    for md in md_files:
        if is_historical_doc(md):
            continue
        text = md.read_text(errors="ignore")
        for name in sorted(set(PATH_RE.findall(text))):
            if name in skill_names or name in NON_SKILL_PATHSEG:
                continue
            add("CRITICAL", md, f".skills/skills/{name}/ -> skill INEXISTANT (phantom / renommé / supprimé)")

    # CHECK B · phantom en contexte d'INVOCATION (on prétend appeler un skill absent du manifest)
    for md in md_files:
        if is_historical_doc(md):
            continue
        text = md.read_text(errors="ignore")
        invoked = set(INVOKE_RE.findall(text)) | set(INVOKE_TASK_RE.findall(text))
        for tok in sorted(invoked):
            if tok in skill_names or tok in NON_SKILL_PATHSEG or not SKILL_SHAPE.match(tok):
                continue
            add("WARN", md, f"`{tok}` présenté comme une invocation de skill mais ABSENT du manifest -> phantom, renommé (ex sync-creatives-to-notion -> sync-notion-atlas), futur non construit, ou doctrine prise pour un skill (revue · advisory tant que la dette pré-existante n'est pas nettoyée, puis promouvoir en HIGH)")

    # CHECK C · doctrine-pipeline reachability
    for entry in PIPELINE_MAP:
        doc = entry["doctrine"]
        if not doc.exists():
            continue
        doc_text = doc.read_text(errors="ignore")
        orch_text = "\n".join(
            p.read_text(errors="ignore") for p in entry["orchestrators"] if p.exists()
        )
        allow = entry.get("allow_unwired", set())
        named = {n for n in skill_names if word_present(n, doc_text)}
        for n in sorted(named):
            if n in allow:
                continue
            if not word_present(n, orch_text):
                add("HIGH", doc, f"`{n}` nommé dans la doctrine pipeline mais ABSENT des orchestrateurs -> décrochage doctrine<->skill (cf D#509)")

    # CHECK D · dormant skills (referenced nowhere but their own SKILL.md)
    corpus_files = (
        list(SKILLS_DIR.rglob("SKILL.md"))
        + list(DOCS.rglob("*.md"))
        + (list(COMMANDS.rglob("*.md")) if COMMANDS.exists() else [])
    )
    corpus = "\n".join(p.read_text(errors="ignore") for p in corpus_files)
    for n in sorted(skill_names):
        own = SKILLS_DIR / n / "SKILL.md"
        own_text = own.read_text(errors="ignore") if own.exists() else ""
        if (corpus.count(n) - own_text.count(n)) <= 0:
            add("WARN", "(manifest)", f"`{n}` référencé NULLE PART hors de son propre SKILL.md -> dormant candidate (revue · standalone légitime ou décroché ?)")

    # report
    order = {"CRITICAL": 0, "HIGH": 1, "WARN": 2}
    findings.sort(key=lambda x: (order.get(x[0], 9), x[1]))
    counts = {"CRITICAL": 0, "HIGH": 0, "WARN": 0}
    for sev, _, _ in findings:
        counts[sev] = counts.get(sev, 0) + 1

    if as_json:
        print(json.dumps({"counts": counts, "findings": [
            {"severity": s, "file": f, "message": m} for s, f, m in findings
        ]}, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("SKILL REACHABILITY · garde-fou anti-décrochage doctrine <-> skill")
        print("=" * 70)
        for sev, f, m in findings:
            tag = {"CRITICAL": "[CRIT]", "HIGH": "[HIGH]", "WARN": "[warn]"}.get(sev, sev)
            print(f"{tag} {f}\n       {m}")
        if not findings:
            print("[OK ] aucun décrochage, aucun fantôme, aucun dormant.")
        print("-" * 70)
        print(f"  CRITICAL {counts['CRITICAL']}   HIGH {counts['HIGH']}   WARN {counts['WARN']}")
        print("-" * 70)

    hard = counts["CRITICAL"] + counts["HIGH"]
    if hard > 0 or (strict and counts["WARN"] > 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
