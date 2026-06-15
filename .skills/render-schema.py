#!/usr/bin/env python3
"""
render-schema · le renderer de schémas opérationnels de PhantomOS (D#521).

LA LEÇON DE L'ARC, APPLIQUÉE · le rendu est du CODE DÉTERMINISTE, pas le modèle
qui dessine du SVG à la main. Les schémas PhantomOS (2x2 de position, heatmap
use_case x audience, graphe de relations, sankey Mc->U->A) sont des layouts
CALCULABLES depuis le JSON. Le code émet le SVG, toujours identique, jamais
cassé. Le modèle décide QUAND appeler ce script et avec quelle data · le script
décide COMMENT rendre. Le design-system (charte read_me visualize reverse-
engineeré · couleur sémantique, ≤5 mots, sentence case, viewBox 680) est baké
dans les fonctions ci-dessous, pas re-suivi à chaque fois.

Sortie · un fichier .svg autonome (le CSS des classes est embarqué, contrairement
à claude.ai qui le fournit en ambiant), ouvrable partout (open -> navigateur).

Usage ·
  python3 .skills/render-schema.py --type 2x2 --brand {slug} [--open]
  python3 .skills/render-schema.py --type 2x2 --demo --open    # data synthétique

Stdlib only. Ne crash jamais le flux (fail-open). Auto-open avec fallback chemin.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Palette read_me · 9 rampes, stops clés (50 fill clair · 200 fill · 600 stroke · 800/900 texte).
# Couleur = SENS, pas séquence. Sémantique des quadrants de position posée explicitement.
RAMP = {
    "teal":  {"fill": "#E1F5EE", "mid": "#5DCAA5", "stroke": "#0F6E56", "text": "#085041", "deep": "#04342C"},
    "coral": {"fill": "#FAECE7", "mid": "#F0997B", "stroke": "#993C1D", "text": "#712B13", "deep": "#4A1B0C"},
    "amber": {"fill": "#FAEEDA", "mid": "#EF9F27", "stroke": "#854F0B", "text": "#633806", "deep": "#412402"},
    "gray":  {"fill": "#F1EFE8", "mid": "#D3D1C7", "stroke": "#888780", "text": "#2C2C2A", "deep": "#2C2C2A"},
    "blue":  {"fill": "#E6F1FB", "mid": "#85B7EB", "stroke": "#185FA5", "text": "#0C447C", "deep": "#042C53"},
    "purple":{"fill": "#EEEDFE", "mid": "#AFA9EC", "stroke": "#534AB7", "text": "#3C3489", "deep": "#26215C"},
}
MUTED = "#5F5E5A"
HINT = "#888780"


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def svg_doc(title, desc, height, body):
    """Enveloppe SVG · viewBox 680 load-bearing (ratio 1:1), role=img + a11y, CSS embarqué."""
    style = (
        ".th{font-weight:500;font-size:14px}.t{font-weight:400;font-size:14px}"
        ".ts{font-weight:400;font-size:12px}"
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="680" viewBox="0 0 680 %d" role="img" '
        "font-family=\"'Anthropic Sans', system-ui, -apple-system, sans-serif\">\n"
        "  <title>%s</title>\n  <desc>%s</desc>\n"
        "  <defs><style>%s</style></defs>\n%s\n</svg>\n"
    ) % (height, _esc(title), _esc(desc), style, body)


# ---------- Schéma · matrice 2x2 de position (nous x eux) ----------

# Les 4 quadrants canon (spectrum.strategic_position) -> rampe sémantique + position grille.
QUAD = {
    "our-advantage":   {"label": "Notre avantage",          "sub": "Creuser et défendre",    "ramp": "teal",  "col": 0, "row": 0},
    "battlefield":     {"label": "Champ de bataille",       "sub": "Différencier ou céder",  "ramp": "coral", "col": 1, "row": 0},
    "whitespace":      {"label": "Zone blanche",            "sub": "Qualifier avant de jouer", "ramp": "gray",  "col": 0, "row": 1, "dashed": True},
    "proxy-validated": {"label": "Validation par procuration", "sub": "Entrer mieux ou passer", "ramp": "amber", "col": 1, "row": 1},
}
DEMAND_R = {"strong": 42, "moderate": 32, "weak": 22, None: 26}


def _position_of(cell):
    """strategic_position explicite, sinon dérivé de coverage_self x coverage_market."""
    if cell.get("strategic_position") in QUAD:
        return cell["strategic_position"]
    self_on = cell.get("coverage_self") in ("covered", "partial")
    mkt_on = cell.get("coverage_market") in ("covered", "partial")
    if self_on and not mkt_on:
        return "our-advantage"
    if self_on and mkt_on:
        return "battlefield"
    if not self_on and mkt_on:
        return "proxy-validated"
    return "whitespace"  # ni l'un ni l'autre (ou unknown)


def _cell_radius(cell):
    forces = [e.get("force") for e in (cell.get("evidence") or []) if isinstance(e, dict)]
    if "strong" in forces:
        return DEMAND_R["strong"]
    if "moderate" in forces:
        return DEMAND_R["moderate"]
    if forces:
        return DEMAND_R["weak"]
    return DEMAND_R[None]


def render_2x2(cells, label_of=None):
    label_of = label_of or (lambda c: c.get("use_case_ref") or "")
    # géométrie des quadrants (reprend le proof validé · safe area, pas d'overlap)
    QW, QH = 248, 180
    X0, X1 = 140, 392
    Y0, Y1 = 78, 262
    cols_x = [X0, X1]
    rows_y = [Y0, Y1]
    parts = []
    # axes
    parts.append('<text class="ts" x="264" y="62" text-anchor="middle" fill="%s">eux absents</text>' % MUTED)
    parts.append('<text class="ts" x="516" y="62" text-anchor="middle" fill="%s">eux présents</text>' % MUTED)
    parts.append('<text class="ts" x="44" y="164" fill="%s">nous</text>' % MUTED)
    parts.append('<text class="ts" x="44" y="180" fill="%s">présents</text>' % MUTED)
    parts.append('<text class="ts" x="44" y="350" fill="%s">nous</text>' % MUTED)
    parts.append('<text class="ts" x="44" y="366" fill="%s">absents</text>' % MUTED)

    # bucketer les cellules par quadrant
    buckets = {k: [] for k in QUAD}
    for c in cells:
        buckets[_position_of(c)].append(c)

    for key, q in QUAD.items():
        r = RAMP[q["ramp"]]
        qx, qy = cols_x[q["col"]], rows_y[q["row"]]
        dash = ' stroke-dasharray="4 4"' if q.get("dashed") else ""
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s" stroke="%s" stroke-width="0.5"%s/>'
                     % (qx, qy, QW, QH, r["fill"], r["stroke"], dash))
        parts.append('<text class="th" x="%d" y="%d" fill="%s">%s</text>'
                     % (qx + 20, qy + 26, r["text"], _esc(q["label"])))
        if q.get("sub"):
            parts.append('<text class="ts" x="%d" y="%d" fill="%s">%s</text>'
                         % (qx + 20, qy + 44, r["stroke"], _esc(q["sub"])))
        # placer les bulles · jusqu'à 4 en mini-grille, +N au-delà
        items = buckets[key]
        shown = items[:4]
        # positions relatives dans le quadrant (centre-bas, sous le titre)
        spots = {
            1: [(0.5, 0.62)],
            2: [(0.32, 0.62), (0.68, 0.62)],
            3: [(0.30, 0.52), (0.70, 0.52), (0.50, 0.80)],
            4: [(0.30, 0.50), (0.70, 0.50), (0.30, 0.82), (0.70, 0.82)],
        }.get(len(shown), [(0.5, 0.62)])
        for cell, (fx, fy) in zip(shown, spots):
            cx = qx + int(QW * fx)
            cy = qy + int(QH * fy)
            rad = _clamp(_cell_radius(cell), 18, 40 if len(shown) > 1 else 44)
            if len(shown) >= 3:
                rad = _clamp(rad, 16, 24)
            parts.append('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="0.5"/>'
                         % (cx, cy, rad, r["mid"], r["stroke"]))
            lab = _esc(label_of(cell))[:18]
            parts.append('<text class="ts" x="%d" y="%d" text-anchor="middle" fill="%s">%s</text>'
                         % (cx, cy + 4, r["deep"], lab))
        if len(items) > 4:
            parts.append('<text class="ts" x="%d" y="%d" fill="%s">+%d autres</text>'
                         % (qx + 20, qy + QH - 14, MUTED, len(items) - 4))

    # légende · 3 dimensions orthogonales · jargon de DOMAINE sharp, zéro nom de champ/fichier
    parts.append('<text class="ts" x="140" y="478" fill="%s">Chaque bulle · un job du produit sur cette cellule</text>' % MUTED)
    parts.append('<text class="ts" x="140" y="494" fill="%s">Taille · force du signal (fort, modéré, faible)</text>' % MUTED)
    parts.append('<text class="ts" x="140" y="510" fill="%s">Pointillé · couverture concurrente pas encore observée</text>' % HINT)
    return svg_doc(
        "Carte de position · ce qu'on tient face à la concurrence",
        "Matrice 2 par 2 · notre couverture face à celle des concurrents · quatre quadrants: notre avantage, champ de bataille, validation par procuration, zone blanche.",
        524, "\n".join(parts))


# ---------- Schéma · graphe de relations (modèle d'entités) ----------

REL_NODES = [
    {"label": "Mécanisme",   "sub": "le comment",         "ramp": "gray"},
    {"label": "Cas d'usage", "sub": "le job servi",       "ramp": "purple"},
    {"label": "Audience",    "sub": "qui le vit",         "ramp": "blue"},
    {"label": "Angle",       "sub": "comment l'attaquer", "ramp": "coral"},
]
REL_CARD = ["1 : N", "N : M", "N : M"]


def render_relations(data=None, label_of=None):
    parts = []
    n = len(REL_NODES)
    w, h, yc = 120, 56, 108
    gap = (600 - n * w) // (n - 1)
    xs = [40 + i * (w + gap) for i in range(n)]
    for i in range(n - 1):
        x1, x2 = xs[i] + w, xs[i + 1]
        mid = (x1 + x2) // 2
        parts.append('<text class="ts" x="%d" y="%d" text-anchor="middle" fill="%s">%s</text>' % (mid, yc - 10, MUTED, REL_CARD[i]))
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="0.5" marker-end="url(#arrow)"/>' % (x1 + 2, yc, x2 - 4, yc, HINT))
    for nd, x in zip(REL_NODES, xs):
        r = RAMP[nd["ramp"]]
        parts.append('<rect x="%d" y="80" width="%d" height="%d" rx="8" fill="%s" stroke="%s" stroke-width="0.5"/>' % (x, w, h, r["fill"], r["stroke"]))
        parts.append('<text class="th" x="%d" y="102" text-anchor="middle" fill="%s">%s</text>' % (x + w // 2, r["text"], _esc(nd["label"])))
        parts.append('<text class="ts" x="%d" y="120" text-anchor="middle" fill="%s">%s</text>' % (x + w // 2, r["stroke"], _esc(nd["sub"])))
    ax, ux = xs[3] + w // 2, xs[1] + w // 2
    parts.append('<path d="M%d 136 C %d 196, %d 196, %d 138" fill="none" stroke="#993C1D" stroke-width="0.5" stroke-dasharray="4 3" marker-end="url(#arrow)"/>' % (ax, ax, ux, ux))
    parts.append('<text class="ts" x="%d" y="214" text-anchor="middle" fill="%s">N : 1 · la trace retour de l\'angle vers son usage</text>' % ((ax + ux) // 2, HINT))
    parts.append('<text class="ts" x="40" y="240" fill="%s">1:N un-à-plusieurs · N:M plusieurs-à-plusieurs (le coeur du modèle imbriqué)</text>' % MUTED)
    parts.append('<text class="ts" x="40" y="256" fill="%s">trait plein observé · pointillé déduit · une projection sans mécanisme porteur reste hachurée</text>' % HINT)
    return svg_doc("Comment le mécanisme ouvre les usages, les audiences et les angles",
                   "Graphe · le mécanisme génère les jobs, chaque job dérive ses audiences, chaque audience porte ses angles.",
                   272, "\n".join(parts))


# ---------- Schéma · heatmap use_case x audience ----------

HEAT = {
    "covered":    {"label": "Couvert",      "fill": "#5DCAA5", "stroke": "#0F6E56"},
    "adjacent":   {"label": "Adjacent",     "fill": "#FAC775", "stroke": "#854F0B"},
    "whitespace": {"label": "Zone blanche", "fill": "#F1EFE8", "stroke": "#888780", "dashed": True},
    "unobserved": {"label": "Non observé",  "fill": "none",    "stroke": "#B4B2A9", "hatch": True},
}


def render_heatmap(data, label_of=None):
    ucs, auds, cells = data["use_cases"], data["audiences"], data["cells"]
    n, m = len(ucs), len(auds)
    LM, RM = 150, 640
    cw = (RM - LM) // max(n, 1)
    ch, gy0 = 40, 92
    parts = []
    for j, uc in enumerate(ucs):
        parts.append('<text class="ts" x="%d" y="%d" text-anchor="middle" fill="%s">%s</text>' % (LM + j * cw + cw // 2, gy0 - 12, MUTED, _esc(uc)[:13]))
    for i, aud in enumerate(auds):
        ry = gy0 + i * ch
        parts.append('<text class="ts" x="40" y="%d" fill="%s">%s</text>' % (ry + ch // 2 + 4, MUTED, _esc(aud)[:16]))
        for j in range(n):
            cx = LM + j * cw
            s = HEAT.get(cells.get((i, j), "unobserved"))
            dash = ' stroke-dasharray="3 3"' if s.get("dashed") else ""
            fill = "none" if s["fill"] == "none" else s["fill"]
            parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" stroke="%s" stroke-width="0.5"%s/>' % (cx + 2, ry + 2, cw - 4, ch - 4, fill, s["stroke"], dash))
            if s.get("hatch"):
                parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="0.5" opacity="0.5"/>' % (cx + 6, ry + ch - 6, cx + cw - 8, ry + 6, "#B4B2A9"))
    ly = gy0 + m * ch + 26
    lx = 40
    for key in ("covered", "adjacent", "whitespace", "unobserved"):
        s = HEAT[key]
        sw = "#FFFFFF" if s["fill"] == "none" else s["fill"]
        parts.append('<rect x="%d" y="%d" width="14" height="14" rx="3" fill="%s" stroke="%s" stroke-width="0.5"/>' % (lx, ly, sw, s["stroke"]))
        parts.append('<text class="ts" x="%d" y="%d" fill="%s">%s</text>' % (lx + 20, ly + 11, MUTED, s["label"]))
        lx += 26 + len(s["label"]) * 7 + 22
    parts.append('<text class="ts" x="40" y="%d" fill="%s">Zone blanche · marché vu mais non servi · Non observé · pas encore exploré</text>' % (ly + 30, HINT))
    return svg_doc("Carte des jobs par audience · où on est couvert, où c'est libre",
                   "Grille · les cas d'usage en colonnes, les audiences en lignes · état de couverture par cellule.",
                   ly + 50, "\n".join(parts))


# ---------- Schéma · sankey Mc -> U -> A ----------

TIER = {
    "evident":     {"label": "Évident",    "color": "#1D9E75"},
    "adjacent":    {"label": "Adjacent",   "color": "#BA7517"},
    "speculative": {"label": "Spéculatif", "color": "#7F77DD", "dashed": True},
}


def render_sankey(data, label_of=None):
    mech = data["mechanism"]
    ucs = data["use_cases"]   # [{label, tier, strength}]
    auds = data["audiences"]  # [{label}]
    links = data["links"]     # [(uc_index, aud_index)]
    parts = []
    cx_m, cx_u, cx_a = 40, 290, 530
    w = 110
    # mechanism node (centré verticalement)
    uy = [92 + i * 56 for i in range(len(ucs))]
    ay = [92 + i * 56 for i in range(len(auds))]
    my = (uy[0] + uy[-1]) // 2
    rg = RAMP["gray"]
    # flux Mc -> U (couleur = tier, épaisseur = force)
    sw = {"strong": 6, "moderate": 4, "weak": 2}
    for i, uc in enumerate(ucs):
        t = TIER[uc.get("tier", "evident")]
        dash = ' stroke-dasharray="6 4"' if t.get("dashed") else ""
        wdt = sw.get(uc.get("strength", "moderate"), 4)
        parts.append('<path d="M%d %d C %d %d, %d %d, %d %d" fill="none" stroke="%s" stroke-width="%d" stroke-opacity="0.55"%s/>' % (cx_m + w, my, cx_m + w + 70, my, cx_u - 70, uy[i] + 16, cx_u, uy[i] + 16, t["color"], wdt, dash))
    # flux U -> A
    for (ui, ai) in links:
        t = TIER[ucs[ui].get("tier", "evident")]
        dash = ' stroke-dasharray="6 4"' if t.get("dashed") else ""
        parts.append('<path d="M%d %d C %d %d, %d %d, %d %d" fill="none" stroke="%s" stroke-width="3" stroke-opacity="0.45"%s/>' % (cx_u + w, uy[ui] + 16, cx_u + w + 60, uy[ui] + 16, cx_a - 60, ay[ai] + 16, cx_a, ay[ai] + 16, t["color"], dash))
    # mechanism node
    parts.append('<rect x="%d" y="%d" width="%d" height="40" rx="8" fill="%s" stroke="%s" stroke-width="0.5"/>' % (cx_m, my - 4, w, rg["fill"], rg["stroke"]))
    parts.append('<text class="th" x="%d" y="%d" text-anchor="middle" fill="%s">%s</text>' % (cx_m + w // 2, my + 20, rg["text"], _esc(mech)[:12]))
    # use_case nodes
    for i, uc in enumerate(ucs):
        t = TIER[uc.get("tier", "evident")]
        parts.append('<rect x="%d" y="%d" width="%d" height="32" rx="6" fill="%s" stroke="%s" stroke-width="0.5"/>' % (cx_u, uy[i], w, RAMP["purple"]["fill"], t["color"]))
        parts.append('<text class="ts" x="%d" y="%d" text-anchor="middle" fill="%s">%s</text>' % (cx_u + w // 2, uy[i] + 20, RAMP["purple"]["deep"], _esc(uc["label"])[:13]))
    # audience nodes
    for i, aud in enumerate(auds):
        parts.append('<rect x="%d" y="%d" width="%d" height="32" rx="6" fill="%s" stroke="%s" stroke-width="0.5"/>' % (cx_a, ay[i], w, RAMP["blue"]["fill"], RAMP["blue"]["stroke"]))
        parts.append('<text class="ts" x="%d" y="%d" text-anchor="middle" fill="%s">%s</text>' % (cx_a + w // 2, ay[i] + 20, RAMP["blue"]["deep"], _esc(aud["label"])[:13]))
    # bandeau colonnes
    for cxx, lab in ((cx_m, "Mécanisme"), (cx_u, "Cas d'usage"), (cx_a, "Audience")):
        parts.append('<text class="ts" x="%d" y="74" text-anchor="middle" fill="%s">%s</text>' % (cxx + w // 2, MUTED, lab))
    # légende tiers
    ly = max(uy[-1], ay[-1]) + 60
    lx = 40
    for key in ("evident", "adjacent", "speculative"):
        t = TIER[key]
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"%s/>' % (lx, ly + 6, lx + 22, ly + 6, t["color"], ' stroke-dasharray="6 4"' if t.get("dashed") else ""))
        parts.append('<text class="ts" x="%d" y="%d" fill="%s">%s</text>' % (lx + 28, ly + 10, MUTED, t["label"]))
        lx += 28 + len(t["label"]) * 7 + 26
    parts.append('<text class="ts" x="40" y="%d" fill="%s">Épaisseur du flux · solidité de la preuve · pointillé spéculatif, hypothèse non confirmée</text>' % (ly + 30, HINT))
    return svg_doc("Du mécanisme aux audiences · le flux d'expansion",
                   "Sankey · le mécanisme à gauche, les usages au centre, les audiences à droite · l'épaisseur suit la solidité de la preuve.",
                   ly + 50, "\n".join(parts))


# ---------- data ----------

def _demo_cells():
    return [
        {"use_case_ref": "beauté intérieur", "strategic_position": "our-advantage",
         "evidence": [{"force": "moderate"}]},
        {"use_case_ref": "énergie quotidienne", "strategic_position": "battlefield",
         "evidence": [{"force": "strong"}]},
        {"use_case_ref": "récup post-effort", "strategic_position": "proxy-validated",
         "evidence": [{"force": "moderate"}]},
        {"use_case_ref": "anti-carence vegan", "strategic_position": "whitespace",
         "evidence": [{"force": "weak"}]},
        {"use_case_ref": "immunité", "strategic_position": "battlefield",
         "evidence": [{"force": "weak"}]},
    ]


def _label_resolver(root, brand):
    """use_case_ref (UC-NN) -> label depuis spec.use_cases[], si dispo."""
    mapping = {}
    pdir = root / "brands" / brand / "products"
    if pdir.is_dir():
        for spec in pdir.glob("*/spec.json"):
            try:
                data = json.loads(spec.read_text(encoding="utf-8"))
            except Exception:
                continue
            for uc in data.get("use_cases", []) or []:
                if uc.get("use_case_id"):
                    mapping[uc["use_case_id"]] = uc.get("label") or uc["use_case_id"]
    return lambda c: mapping.get(c.get("use_case_ref"), c.get("use_case_ref") or "")


def _demo_sankey():
    return {
        "mechanism": "Compression ciblée",
        "use_cases": [
            {"label": "Énergie", "tier": "evident", "strength": "strong"},
            {"label": "Récup effort", "tier": "adjacent", "strength": "moderate"},
            {"label": "Beauté intérieur", "tier": "adjacent", "strength": "moderate"},
            {"label": "Anti-carence", "tier": "speculative", "strength": "weak"},
        ],
        "audiences": [
            {"label": "Actifs 25-40"}, {"label": "Sportifs"},
            {"label": "Beauté"}, {"label": "Vegan"},
        ],
        "links": [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1)],
    }


def _demo_data(typ):
    if typ == "2x2":
        return _demo_cells(), (lambda c: c.get("use_case_ref") or "")
    if typ == "heatmap":
        ucs = ["Énergie", "Récup", "Beauté", "Immunité", "Anti-carence"]
        auds = ["Actifs 25-40", "Sportifs", "Optimiseurs beauté", "Régimes vegan"]
        cells = {(0, 0): "covered", (0, 1): "adjacent", (0, 3): "adjacent",
                 (1, 0): "adjacent", (1, 1): "covered", (1, 3): "adjacent",
                 (2, 2): "covered", (2, 4): "whitespace",
                 (3, 0): "adjacent", (3, 4): "whitespace"}
        return {"use_cases": ucs, "audiences": auds, "cells": cells}, None
    if typ == "sankey":
        return _demo_sankey(), None
    return None, None  # relations · pas de data


RENDERERS = {"2x2": render_2x2, "heatmap": render_heatmap,
             "relations": render_relations, "sankey": render_sankey}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, choices=sorted(RENDERERS))
    ap.add_argument("--brand")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--open", action="store_true", dest="do_open")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    typ = args.type

    if args.demo:
        data, label_of = _demo_data(typ)
        out = Path(args.out) if args.out else Path("/tmp/phantom-%s-demo.svg" % typ)
    elif typ == "relations":
        # le graphe de relations = le modèle d'entités, ne dépend d'aucune marque
        data, label_of = None, None
        out = Path(args.out) if args.out else Path("/tmp/phantom-relations.svg")
    else:
        if not args.brand:
            print("ERROR: --brand requis (ou --demo)", file=sys.stderr)
            return 2
        try:
            spectrum = json.loads((root / "brands" / args.brand / "spectrum.json").read_text(encoding="utf-8"))
        except Exception:
            print("ERROR: pas de spectrum.json lisible pour %s" % args.brand, file=sys.stderr)
            return 1
        cells = spectrum.get("cells", []) or []
        if not cells:
            print("ERROR: spectrum.json sans cells", file=sys.stderr)
            return 1
        label_of = _label_resolver(root, args.brand)
        if typ == "2x2":
            data = cells
        else:
            print("ERROR: builder de données réelles pour '%s' pas encore câblé · utilise --demo" % typ, file=sys.stderr)
            return 1
        vdir = root / "brands" / args.brand / "visuals"
        vdir.mkdir(parents=True, exist_ok=True)
        out = Path(args.out) if args.out else vdir / ("%s.svg" % typ)

    svg = RENDERERS[typ](data, label_of)
    out.write_text(svg, encoding="utf-8")
    print("OK · %s écrit" % out)
    if args.do_open:
        try:
            subprocess.run(["open", str(out)], check=False)
            print("ouvert · %s" % out)
        except Exception:
            print("auto-open indispo · open %s" % out)
    else:
        print("pour l'afficher · open %s" % out)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("render-schema fail-open · %s" % e, file=sys.stderr)
        sys.exit(0)
