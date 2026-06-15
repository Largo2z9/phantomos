#!/usr/bin/env python3
"""
render-beat.py · rend un BEAT de session (trouvé / analysé / encodé) en markdown sharp.

Le split D#520 · le CODE garantit la STRUCTURE (les 3 couches, les rejets, la
confiance-avec-raison, le pointeur /phantom ne peuvent pas s'effondrer en une
phrase météo). Le MODÈLE fournit le CONTENU (le payload, produit par le
sous-agent pendant que son contexte est frais · anti double-compression).

Entrée · un beat-payload JSON écrit par le producteur à
.phantom/beats/{slug}/{phase}.json  (état système, hors brands/ · ce n'est pas de
la donnée de marque mais un artefact de restitution, donc hors gate mutation).
Sortie · markdown sur stdout, que l'orchestrateur ÉMET tel quel (il ne re-narre
pas). Fail-open · toute erreur → stdout vide + exit 0, l'orchestrateur retombe
sur sa propre narration, jamais de crash du flux.

Usage ·
  python3 .skills/render-beat.py --brand onday --phase scan
  python3 .skills/render-beat.py --demo
"""

import sys
import json
import argparse
from pathlib import Path

PHASE_LABEL = {
    "scan": "Scan profond",
    "audiences": "Arbre d'audiences",
    "spectrum": "Carte du marché",
    "angles": "Angles",
    "close": "Atlas",
}

# Quelle vue /phantom chaque phase ouvre · le CODE décide (pas le modèle), pour ne
# JAMAIS teaser une vue pas encore construite. Au scan, le spectre n'existe pas
# (il vient au Step 2.5) · on pointe la décompo produit, qui ELLE est posée.
PHASE_VIEW = {
    "scan": "products",      # décompo produit · mécanismes → bénéfices → usages
    "audiences": "audiences",
    "spectrum": "spectre",   # carte marché · construite au Step 2.5
    "angles": "matrix",
    "close": "atlas",        # vue d'ensemble · synthèse des 7 entités
}

# Conscience de la TEMPORALITÉ · ce que la phase enchaîne dans le pipeline. En mode
# orchestré le beat montre la trajectoire (l'orchestrateur continue tout seul) · en
# standalone il la PROPOSE (le skill modulaire est arrivé seul, il appelle la suite ·
# c'est là que la proactivité se déclenche sans orchestrateur au-dessus).
PHASE_NEXT = {
    "scan":      "je dérive les audiences du mécanisme, pas du miroir des avis",
    "audiences": "je croise mécanisme et audiences en carte de marché (le spectre)",
    "spectrum":  "j'écris les angles d'attaque, un par territoire",
    "angles":    "je score la matrice et je sors les axes prioritaires",
    "close":     "",  # terminal · pas de suite dans la chaîne d'encodage
}

LEVEL_FR = {"forte": "forte", "moyenne": "moyenne", "faible": "faible",
            "high": "forte", "medium": "moyenne", "low": "faible"}


def _s(x):
    return "" if x is None else str(x).strip()


def _join(items, sep=", "):
    out = [_s(i) for i in (items or []) if _s(i)]
    return sep.join(out)


def _layer(label, body):
    body = _s(body)
    if not body:
        return ""
    return "**%s** · %s" % (label, body)


def _bullets(items):
    """Une string par bullet. Le modèle peut y mettre une amorce grasse
    (`**thèse.** justification`) · format report Shape of Key."""
    out = []
    for i in (items or []):
        t = _s(i)
        if t:
            out.append("- %s" % t)
    return out


def _section(title, body):
    """Un bloc · titre gras + ses bullets. Vide → omis."""
    if not body:
        return []
    return ["**%s**" % title] + body + [""]


def render(payload, brand, phase, mode="orchestrated"):
    phase = _s(payload.get("phase")) or phase or "scan"
    label = PHASE_LABEL.get(phase, "Passe")
    verdict = _s(payload.get("verdict"))
    read = _s(payload.get("read"))
    tease = _s(payload.get("tease"))
    view = PHASE_VIEW.get(phase, "atlas")  # le code décide la vue, pas le modèle

    lines = ["**%s**" % label, ""]

    # PROSE d'ouverture · le verdict tranché (gras) + une lecture courte. Le report
    # commence en prose, pas en bullets (format Shape of Key · prose PUIS bullets).
    prose = []
    if verdict:
        prose.append("**%s**" % verdict)
    if read:
        prose.append(read)
    if prose:
        lines.append(" ".join(prose))
        lines.append("")

    # LE RAISONNEMENT · ce qui fonde le verdict (déductions + faits + ce qui a été
    # écarté). Décision-ordonné, PAS process-ordonné · pas de labels Trouvé/Analysé,
    # chaque point porte sa propre amorce grasse et flue après l'ouverture.
    why = _bullets(payload.get("analyzed")) + _bullets(payload.get("found"))
    for r in (payload.get("rejected") or []):
        if isinstance(r, dict):
            what, w = _s(r.get("what")), _s(r.get("why"))
            if what:
                why.append("- **Écarté · %s**%s" % (what, (" · " + w) if w else ""))
        elif _s(r):
            why.append("- **Écarté** · %s" % _s(r))
    if why:
        lines += why + [""]

    # CE SUR QUOI JE RESTE PRUDENT · sources bloquées + confiance NON-forte, toujours
    # avec SA cause. L'expert ne caveat pas ce dont il est sûr (le verdict le porte),
    # il flague le reste · la confiance forte n'apparaît pas, elle vit dans le verdict.
    prudent = []
    for b in (payload.get("blocked") or []):
        if isinstance(b, dict):
            src, w = _s(b.get("source")), _s(b.get("reason"))
            if src:
                prudent.append("- **Bloqué · %s**%s" % (src, (" · " + w) if w else ""))
        elif _s(b):
            prudent.append("- **Bloqué** · %s" % _s(b))
    for c in (payload.get("confidence") or []):
        if isinstance(c, dict):
            lvl = LEVEL_FR.get(_s(c.get("level")).lower(), _s(c.get("level")))
            if lvl and lvl != "forte":
                claim, w = _s(c.get("claim")), _s(c.get("reason"))
                if claim:
                    prudent.append("- **%s · confiance %s**%s" % (claim, lvl, (" · " + w) if w else ""))
    lines += _section("Ce sur quoi je reste prudent", prudent)

    # LA BASE · une ligne sobre · la largeur du travail, sans la mettre en avant.
    basis = _s(payload.get("basis"))
    if basis:
        lines.append("Lu · %s" % basis)
        lines.append("")

    # CTA /phantom · teasé (le modèle dit la valeur DANS la vue) + actionnable (le
    # code garantit la commande paste-ready ET la bonne vue · jamais oublié, jamais
    # une vue pas encore construite). Le tease propose, la commande exécute.
    if tease:
        lines.append("→ **%s**" % tease)
    lines.append("Ouvre la vue · `/phantom %s %s`" % (brand, view))

    # TEMPORALITÉ · la conscience de l'étape dans la chaîne. Orchestré · trajectoire
    # (l'orchestrateur enchaîne, le beat signale juste le cap). Standalone · le skill
    # modulaire est arrivé seul, il PROPOSE la suite · la proactivité vient de là.
    nxt = PHASE_NEXT.get(phase, "")
    if nxt:
        lines.append("")
        if mode == "standalone":
            lines.append("Prochaine étape · %s. Je lance ?" % nxt)
        else:
            lines.append("_Et après · %s._" % nxt)

    return "\n".join(lines).strip() + "\n"


def _demo_payload():
    return {
        "phase": "scan",
        "verdict": "C'est un business d'abonnement, et ça change toute l'économie du jeu.",
        "read": "Tout converge vers l'abo à 74€/mois (kit offert, « 5000+ abonnés » en preuve), la vente one-shot à 89€ n'est qu'une porte d'entrée. Conséquence structurelle · tu te pilotes à la valeur vie de l'abonné, pas au ROAS du premier achat. Donc ton CAC acceptable est plus haut qu'un concurrent one-shot, tu peux surenchérir sur le froid, à une condition unique · que la rétention au mois 2 tienne. Et c'est précisément le chiffre que je ne vois pas.",
        "found": [
            "**Le positionnement ouvre une catégorie au lieu de se battre dans une.** AG1 possède la performance et le premium US ; Onday parle simplicité, chaleur, made-in-France. Le lane est libre parce qu'aucun acteur financé ne l'occupe, mais il plafonne ton AOV et ton moat devient l'affinité de marque, pas la supériorité produit.",
        ],
        "blocked": [
            {"source": "Trustpilot", "reason": "403, lu les forums sportifs à la place"},
        ],
        "analyzed": [
            "**Le move est category-defining, pas frontal** · attaquer AG1 sur la performance, c'est perdre de face. Défendable face à AG1, fragile face à un copieur français qui prendrait le même angle.",
        ],
        "rejected": [
            {"what": "l'angle performance", "why": "terrain d'AG1, frontal et perdu d'avance"},
        ],
        "encoded": [
            "**Spec produit** · 39 actifs, 11 usages dont 4 spéculatifs, positionnement FR chaleureux",
        ],
        "confidence": [
            {"claim": "le moteur éco abonnement", "level": "forte", "reason": "tout le site converge"},
            {"claim": "l'audience cœur", "level": "faible", "reason": "Trustpilot bloqué, pas parce que le signal est faible"},
        ],
        "basis": "fiche produit, mission, ingrédients, 39 actifs, 3 interviews fondateurs, forums sportifs",
        "tease": "La décompo produit est posée · 11 usages tirés du mécanisme, dont 4 que les avis seuls ne sortent pas.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", default="demo")
    ap.add_argument("--root", default=".")
    ap.add_argument("--phase", default="scan")
    ap.add_argument("--payload")
    ap.add_argument("--mode", default="orchestrated", choices=["orchestrated", "standalone"])
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    if args.demo:
        payload = _demo_payload()
        brand = "onday"
    else:
        if args.payload:
            ppath = Path(args.payload)
        else:
            ppath = Path(args.root) / ".phantom" / "beats" / args.brand / ("%s.json" % args.phase)
        try:
            payload = json.loads(ppath.read_text(encoding="utf-8"))
        except Exception:
            # Fail-open · pas de payload lisible → stdout vide, l'orchestrateur narre.
            return 0
        brand = args.brand

    try:
        sys.stdout.write(render(payload, brand, args.phase, args.mode))
    except Exception:
        return 0

    # Marqueur d'émission · le hook beat-emit ne re-pousse pas un beat déjà rendu.
    if not args.demo:
        try:
            phase = _s(payload.get("phase")) or args.phase or "scan"
            marker = Path(args.root) / ".phantom" / "beats" / brand / ("%s.emitted" % phase)
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text("emitted\n", encoding="utf-8")
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
