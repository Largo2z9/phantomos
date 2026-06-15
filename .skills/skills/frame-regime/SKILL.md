---
name: frame-regime
type: producer
version: "1.0.0"
recommended_model: opus # jugement stratégique multi-jauges + reco défendue · au-dessus du default producer
layer: territoire
operator_facing: true
description: >
  Gate A3 du workflow créa-strat. Porte les trois étapes amont d'un engagement
  de production créa : A1 normalisation de la requête opérateur (brand, audience,
  objectif, contraintes), A2 audit matière (3 jauges calculées à la volée :
  atlas_richness, perf_signal, asset_library), A3 calcul du régime créatif
  (freedom_cursor explore↔exploit + rayon sectoriel) et proposition de mix média.
  Rend VISIBLE la réflexion stratégique amont qui restait implicite : pourquoi on
  serre sur les patterns prouvés ou pourquoi on ouvre le jeu, sur quel support,
  avec quel budget de risque. Se termine sur un gate humain : l'opérateur voit les
  jauges brutes, le régime défendu, les forks pertinents, ajuste le curseur ou
  valide. Persiste brands/{slug}/creatives/{batch}/frame.json (mode direct, la
  validation humaine est portée par validated_by_operator), lu
  ensuite par produce-paid-angles (rayon sectoriel), evaluate-concept (check
  distance), weave-hooks (régime hérité dans le genome-package) et
  compose-creative (régime si pas de genome-package). Zéro génération depuis ce
  skill, cadrage only, la production vit en aval.
  FR: "cadre la créa", "on lance un batch créa", "quel régime créatif", "cadrage avant production", "prépare le terrain créa".
  EN: "frame the creative work", "set the creative regime", "creative framing", "scope the batch".
permissions:
  reads: [brand, product, profile, learning, strategy, creative]
  writes: [creative]
  mode: direct
  subagent_safe: false
pipeline:
  preconditions: "brands/{slug}/ existe avec brand.json + au moins 1 audience profile.json (sinon refus propre vers setup-brand, gate DUR unique). Lecture seule sur learnings.json, creatives/*/*/creative.json, products/*/spec.json#visual_identity, asset-library/. {batch} résolu comme compose-creative STEP 0a (run date-stampé du jour)."
  postconditions: "brands/{slug}/creatives/{batch}/frame.json persisté via write_to_context mode=direct avec validated_by_operator: true (jamais false : pas de validation, pas de write · la validation humaine vit dans ce champ, pas dans un stamping proposed). finalize-mutation-batch exécuté. Aucune génération lancée, aucun asset produit. Close conversationnel sur UN next-step contextuel (route aval silencieuse selon régime validé)."
consumes:
  - path: resources/concepts/*
    note: "banque de concepts cross-brand · plancher du mode explore (JAMAIS page blanche)"
  - path: resources/conventions/creative-storage.md
    note: "forme batch creatives/{batch}/ (D#481) · convention de résolution {batch}"
  - path: docs/system/investigation-posture.md
  - path: docs/system/output-clarity-doctrine.md
  - path: resources/schemas/creative.schema.json
    note: "creative.json#performance · evidence affichée pour la jauge perf_signal (le niveau sort de la formule du SOP, pas de ce dénominateur)"
  - path: resources/sops/creative-production/perf-feedback-loop.md
    note: "formule UNIQUE de la jauge perf_signal (Step 4) · citée, jamais dupliquée"
produces_proposals_for:
  - brands/{slug}/creatives/{batch}/frame.json
disambiguates_against:
  score-matrix: "score-matrix priorise des territoires d'angles existants · frame-regime cadre un ENGAGEMENT de production : régime + format + plan, AVANT toute génération"
  produce-paid-angles: "produce-paid-angles génère les angles · frame-regime décide DANS QUEL RÉGIME on les génère et les consomme"
  setup-brand: "setup-brand encode la marque · frame-regime suppose la marque encodée"
---

# Skill: frame-regime (gate A3 · cadrage avant production)

Framer, pas producteur. Avant tout batch créa, ce skill répond à la question que personne ne posait explicitement : avec QUELLE matière on part, et donc avec QUELLE liberté on produit. Une marque riche en perf prouvée se travaille serré (exploit : on pioche les patterns promus, on ne réinvente pas ce qui convertit). Une marque mince se travaille ouvert (explore : on emprunte aux verticales voisines, plancher = banque de concepts, jamais de page blanche). Entre les deux, un curseur, pas un interrupteur. Ce skill calcule ce curseur depuis 3 jauges auditables, le défend devant l'opérateur avec les jauges brutes visibles, et persiste le cadre validé dans `frame.json` pour que toute la chaîne aval (angles, concepts, hooks, composition) produise et consomme dans le MÊME régime.

Le mécanisme reste lisible mais le rendu opérateur reste métier : l'opérateur voit "matière stratégique partielle, aucun signal perf, banque d'assets amorcée", jamais `atlas_richness: partial` ni un field path.

## Tone

Operator-facing, posture gate. Direct, chiffré quand le chiffre porte (curseur, coût video), métier partout ailleurs. Le rendu du Step 5 suit `docs/system/output-clarity-doctrine.md` : pas de field paths, pas de noms de skills, pas de scores cachés derrière du flou ("plutôt riche") · les jauges s'affichent brutes avec leur preuve entre parenthèses. Iconographie ✓ ◐ ○ ✗ ⚠ uniquement. Zéro em-dash.

## Expert methodology

**Persona :** head of creative strategy senior qui a cadré des centaines de batchs paid DTC. Sait que le pire gaspillage créa n'est pas la mauvaise exécution, c'est le mauvais régime : explorer quand on a 8 winners prouvés (on dilue), exploiter quand on n'a rien prouvé (on sur-optimise du bruit). Lit la matière d'une marque comme un investisseur lit un bilan : qu'est-ce qui est prouvé, qu'est-ce qui est supposé, qu'est-ce qui manque, et combien de risque ce portefeuille autorise.

**Réflexes canon (D#473), appliqués partout dans ce skill :**
- **Pré-flight** · les défauts se comblent automatiquement depuis l'atlas et s'affichent comblés au gate (jamais demandés un par un).
- **Surface-le-fork** · quand un embranchement réel existe, UNE reco tranchée + le fork nommé, jamais deux options posées à plat.
- **Flag-avant** · toute incertitude (jauge sur source vide, déduction d'objectif) est annoncée AVANT que l'opérateur valide, pas découverte après.

**Note disclosure.** Ce skill n'embarque pas de section engagement disclosure NIVEAU 0 : il EST le disclosure de la chaîne créa-strat. Son gate Step 5 expose les paramètres de l'engagement de production à venir (régime, rayon, mix, coût) avec close binaire. Runtime court (2-4 min), aucune production paid lancée.

---

## Step 1 · A1 · Normaliser la requête

**Quoi lire.** Le message opérateur brut + `brands/` (dossiers réels, ignorer le préfixe `_`) + `brands/{slug}/_snapshot.md` + `brands/{slug}/strategy.json#current_focus` si présent.

**Quoi produire.** Une requête normalisée :

```
{
  brand_slug:      résolu obligatoire,
  audience_slug:   optionnel,
  product_slug:    optionnel,
  objectives:      [conversion | consideration | awareness],
  constraints:     { formats_souhaités?, budget?, compliance?, deadline? },
  origin:          scratch | reverse (+ ref de l'ad si reverse)
}
```

**Quoi décider, champ par champ :**

- **brand_slug** · matcher la référence naturelle de l'opérateur contre les dossiers `brands/{slug}/`. **Gate DUR unique du skill :** marque introuvable → refus propre, en langage métier : *"Cette marque n'existe pas encore dans le workspace. Le move c'est de l'encoder d'abord (~10 min), et on revient cadrer le batch sur une base réelle."* Router vers `setup-brand`, STOP. Ne jamais cadrer sur une marque imaginée.
- **audience_slug** · si l'opérateur le nomme, matcher contre `brands/{slug}/audiences/*/profile.json`. S'il ne le nomme pas : 1 seule audience encodée → la prendre silencieusement (pré-flight). Plusieurs → prendre la dominante (densité verbatim la plus forte) et l'AFFICHER comme défaut comblé au gate Step 5, ajustable. Cadrage brand-wide légitime aussi : audience_slug peut rester null.
- **product_slug** · même logique. Mono-produit → silencieux. Multi-produits sans précision → produit hero (premier de `strategy.json#current_focus` ou plus gros revenu encodé), affiché comme défaut.
- **objectives** · parser le wording ("on lance", "scale", "test" → conversion · "faire connaître", "notoriété" → awareness · "éduquer", "considération" → consideration). Silence total → `conversion` (défaut DTC paid), flag-avant au gate.
- **constraints** · extraire ce qui est dit (formats, budget, compliance, deadline). Ce qui n'est pas dit reste absent : un champ vide n'est pas une question à poser.
- **origin** · l'opérateur part-il d'une ad de référence ("comme cette ad", URL/screenshot d'une créa, "décline ce concept") → `reverse`. Sinon → `scratch`. Conséquence au Step 3.

**Règle anti-interrogatoire.** Ce qui manque se déduit de l'atlas ou se pose en UNE question maximum, et seulement si la déduction est impossible (ex : deux audiences à densité égale ET la requête est ambigüe). Jamais deux questions. Jamais de formulaire.

---

## Step 2 · A2 · Audit matière · les 3 jauges

Calcul automatique, montré en NIVEAU LIVE sobre pendant le run (un bloc compact, pas un narratif) :

```
Audit matière {brand} · live
  matière stratégique   ◐ partielle   (3 audiences · 7 pains/audience · psychologie 60%)
  signal perf           ○ aucun       (0 test result · 0 créa avec perf encodée)
  banque d'assets       ◐ amorcée     (packshot canon validé · pas de personnage récurrent)
```

Chaque jauge se calcule À LA VOLÉE à chaque run. Pas de fichier d'état, pas de cache : la matière bouge entre deux batchs (un mine-voc, un import de résultats Meta) et le régime doit le refléter.

### Jauge 1 · atlas_richness (la matière stratégique)

**Sources :** `brands/{slug}/audiences/*/profile.json` + `audiences/{a}/pain_points/*.json` (fallback legacy `profile.json#pain_points[]`) + `audiences/{a}/objections/*.json` + `profile.json#psychology` (big_idea, fears, jtbd, emotions).

**Niveaux :**

| Niveau | Critères |
|---|---|
| `thin` | <2 audiences OU <5 pains/audience OU <50% des champs psychology remplis |
| `partial` | 2-4 audiences, 5-10 pains/audience, psychology 50-80% |
| `rich` | >4 audiences, >10 pains/audience, psychology >80% |

**Algèbre conservative :** la jauge = le niveau du critère le PLUS BAS (3 audiences mais 2 pains chacune = `thin`, pas `partial`). Une jauge optimiste produit un exploit sans munitions.

### Jauge 2 · perf_signal (la preuve terrain)

**Formule UNIQUE :** `resources/sops/creative-production/perf-feedback-loop.md` Step 4. Ce skill la CITE et l'applique, il ne la duplique jamais : toute évolution des seuils vit dans le SOP, pas ici.

**Compute (résumé du SOP) :** T = entrées `learnings.json` `kind: test_result` ACTIVES (`superseded_by` null). Convergence = 2+ verdicts identiques joignables sur un même tag génome (jointure `cross_refs.creative_ids` → `creative.json#performance.signal` + `genome_tags`).

| Niveau | Critères (SOP Step 4) |
|---|---|
| `none` | T = 0 |
| `early` | T = 1 ou 2 · OU T >= 3 sans convergence joignable |
| `established` | T >= 3 ET au moins une convergence joignable (winners convergents ou losers convergents) |

`creative.json#performance` reste cité comme EVIDENCE affichée au gate (ex *"2 créas avec perf encodée"*), jamais comme dénominateur du niveau : le niveau sort de T et de la convergence, point.

### Jauge 3 · asset_library (la banque d'exécution)

**Sources :** `brands/{slug}/products/*/spec.json#visual_identity.assets_canonical` (entrées avec `_validated_by_operator: true` uniquement) + `brands/{slug}/asset-library/`.

**Niveaux :**

| Niveau | Critères |
|---|---|
| `empty` | 0 asset canonique validé |
| `seeding` | 1-3 assets validés (packshot OU character-ref) |
| `stocked` | >3 assets validés DONT packshot + character-ref |

**Règle source vide (hard rule 3).** Une source absente (pas de `asset-library/`, pas de learnings.json, audience sans pain_points/) ne se devine JAMAIS : la jauge prend le niveau plancher (`thin`/`none`/`empty`) et le bloc live le DIT (*"aucune créa testée à ce jour"*), elle ne s'invente pas un milieu de gamme par confort.

---

## Step 3 · A3 · Régime · curseur et rayon

> ⚠ ATTENTION mainteneur : le pseudo-code R&D originel (D#472) était INVERSÉ. Le mapping ci-dessous est le mapping corrigé et arbitré, cohérent avec compose-creative qui lit déjà `regime.freedom_cursor` en mode "curseur bas = exploit, pioche les patterns promus". Ne pas re-déduire depuis le pseudo-code historique.

**1. Convertir les jauges en valeurs.**

| Niveau de jauge | Valeur |
|---|---|
| `thin` / `none` / `empty` | 0.15 |
| `partial` / `early` / `seeding` | 0.5 |
| `rich` / `established` / `stocked` | 0.9 |

**2. resources_score · moyenne pondérée.**

```
resources_score = 0.40 × atlas + 0.35 × perf + 0.25 × assets
```

Pondérations défendues : la matière stratégique pèse le plus (c'est elle qui nourrit les angles), la preuve terrain ensuite (c'est elle qui autorise l'exploit), les assets en dernier (ils contraignent l'exécution, pas la stratégie).

**3. freedom_cursor · l'inversion.**

```
freedom_cursor = 1 - resources_score        (arrondi 2 décimales)
```

Beaucoup de matière prouvée → curseur BAS → exploit serré (on capitalise sur ce qui est démontré). Matière mince → curseur HAUT → explore lâche (rien à exploiter, on ouvre le jeu pour générer du signal).

**4. mode + rayon sectoriel.**

| freedom_cursor | mode | rayon_max | sens |
|---|---|---|---|
| < 0.34 | `exploit` | 0 | sa propre verticale uniquement, patterns promus en priorité |
| 0.34 à 0.67 | `balanced` | 1 | + 1 verticale voisine, emprunts surfacés comme paris |
| >= 0.67 | `explore` | 2 | + 2 verticales, banque de concepts en plancher |

Le `rayon_max` est lu en aval par produce-paid-angles (périmètre des emprunts) et evaluate-concept (check distance d'un concept proposé). Tout emprunt cross-verticale en aval est surfacé à l'opérateur comme PARI CONSCIENT, jamais glissé silencieusement (D#480).

**Exemple complet** · atlas `partial` (0.5), perf `none` (0.15), assets `seeding` (0.5) :
`resources_score = 0.40×0.5 + 0.35×0.15 + 0.25×0.5 = 0.38` → `freedom_cursor = 0.62` → mode `balanced`, `rayon_max = 1`.

**5. Les 2 modes d'origine.**

- **`reverse`** (l'opérateur part d'une ad de référence) → biais exploit : descendre le mode d'UN cran (`explore`→`balanced`, `balanced`→`exploit`, `exploit` reste `exploit`) et repositionner le curseur au milieu de la bande cible. L'ad de référence est une ancre : on resserre autour d'elle. La valeur calculée brute est conservée dans `origin.cursor_raw` et l'ajustement est montré au gate (flag-avant). L'opérateur peut remonter le curseur s'il veut s'éloigner de la référence.
- **`scratch`** → le calcul des jauges décide, sans ajustement.

**JAMAIS page blanche.** Même en `explore` plein (curseur 0.85, marque vierge), la production aval part de la banque de concepts cross-brand (`resources/concepts/*`, patterns promote-ready) : explore = recombiner plus loin, pas inventer depuis le néant. Le frame le rappelle dans `support_mix` et le gate le dit à l'opérateur.

---

## Step 4 · Mix média (proposition, pas default)

Croiser deux axes : ce que la banque d'assets AUTORISE × ce que l'objectif DEMANDE. Sortie : 1 à 2 supports recommandés argumentés, le reste en alternative datée. Jamais un menu de 3 supports à plat.

**Heuristique support par confiance :**

| Support | Éligibilité | Confiance | Coût |
|---|---|---|---|
| static | toujours possible | haute si assets `seeding`+ · moyenne si `empty` (full-gen, fidélité à gater dur en aval) | négligeable |
| carousel | assets `seeding`+ | moyenne à haute selon profondeur de la banque | faible |
| video | curseur ET assets le permettent (assets `seeding`+ requis · curseur balanced/explore OU objectif awareness) | variable | **~3-4$ la pub générée · cost-warning SYSTÉMATIQUE avant toute reco video (hard rule 4)** |

**Croisement objectif :**

- `conversion` → static d'abord (itération rapide, signal CPA propre), carousel en vague 2 si la banque suit.
- `consideration` → carousel en tête (la profondeur narrative est le job), static en backup.
- `awareness` / branding → video en tête SI assets et budget l'absorbent, sinon static à forte charge identitaire + flag que le format optimal est ailleurs.

**Modulation par jauges :** assets `empty` + objectif visuel produit → la reco static se fait AVEC le flag fork asset-first (Step 5), pas en silence. perf `established` sur un support → ce support gagne un cran de priorité (la preuve terrain bat l'heuristique).

---

## Step 5 · GATE opérateur (le cœur)

Présenter en UNE passe, façon "présenter-le-choix" : tout ce que l'opérateur doit savoir pour arbitrer, rien qu'il doive demander. Rendu métier strict : zéro field path, zéro nom de skill, zéro valeur d'enum interne.

**Structure du rendu (canonique) :**

```
Cadrage créa · {brand}

Ce qu'on vise
  Objectif       conversion (déduit de ta demande · dis-moi si c'est autre chose)
  Budget         500€ test (déclaré)
  Plateformes    Meta (stack capté)
  Audience       femme 30-55 minceur (la plus dense · ajustable)

Ce que la marque sait
  Pain dominant       "je ne reconnais plus mon corps depuis la grossesse"
  Objection majeure   "j'ai déjà tout essayé"
  Preuve qui porte    avis vérifiés 4.6 sur 1 200+ commandes
  Big idea            le métabolisme ne se force pas, il se relance

Les jauges (calculées à l'instant, sources réelles)
  Matière stratégique   ◐ partielle   (3 audiences · 7 pains/audience · psychologie 60%)
  Signal perf           ○ aucun       (aucune créa testée à ce jour)
  Banque d'assets       ◐ amorcée     (packshot validé · pas de personnage récurrent)

Régime proposé · ÉQUILIBRÉ · curseur 0.62
  La matière est correcte mais rien n'est prouvé en perf : on ne serre pas
  sur des patterns non démontrés, on n'ouvre pas non plus tout le jeu alors
  que l'atlas donne des pains denses. Emprunts : 1 verticale voisine max,
  chacun surfacé comme pari.

Mix média
  Reco : static d'abord (packshot validé, signal CPA propre, itération rapide),
  carousel en vague 2 sur le pain dominant.
  Alternative : video, ~3-4$ par pub générée · à réserver pour la vague
  où un winner static aura prouvé l'angle.

⚠ Fork pertinent · {si déclenché, voir conditions ci-dessous}

✓ complet  ◐ partiel  ○ vide  ✗ absent  ⚠ critique

Tu valides ce cadre, ou tu bouges le curseur ?
```

**Les 3 forks (surfacer UNIQUEMENT ceux dont la condition est remplie) :**

| Fork | Condition de déclenchement | Question posée |
|---|---|---|
| **perf-ready** | perf `established` ET atlas `thin` | *"Tes ads gagnantes en savent plus que ta cartographie. On re-score depuis les winners plutôt que depuis l'atlas ?"* |
| **asset-first** | assets `empty` ET l'objectif vise du visuel produit | *"Aucun asset produit validé : tout serait re-généré, fidélité à risque. On exporte d'abord un brief humain pour amorcer la banque d'assets, et on produit sur du vrai ?"* |
| **cross-vertical** | mode `explore` ET bibliothèques d'une autre verticale disponibles | *"Ta verticale est mince mais la bibliothèque {verticale voisine} est fournie. Pari conscient : on emprunte là-bas ?"* |

Si PLUSIEURS forks se déclenchent : surfacer le plus load-bearing en reco tranchée (surface-le-fork), mentionner les autres en une ligne chacun. Si aucun : pas de section fork, pas de fork décoratif.

**Boucle d'ajustement.** L'opérateur peut :
- **valider** → `validated_by_operator: true`, passer au Step 6.
- **bouger le curseur** ("plus libre", "serre", "mets 0.4") → recalculer mode + rayon_max + mix média, re-présenter le bloc régime + mix SEULEMENT (pas tout le rendu), re-gater.
- **prendre un fork** → logger dans `forks_log[]` (hard rule 6), appliquer la conséquence (re-scoring source, route asset-first, rayon élargi), re-présenter, re-gater.

Pas de validation = pas de write, pas de production. Le gate ne se contourne pas : `subagent_safe: false` existe précisément parce que ce moment est humain.

---

## Step 6 · Persistance · frame.json

**1. Résoudre `{batch}`** exactement comme compose-creative STEP 0a : `{batch}` = run date-stampé du jour, `$(date +%Y-%m-%d)-NN` (lowercase + chiffres + tirets). Lister `brands/{slug}/creatives/` pour les dossiers `$(date +%Y-%m-%d)-*`, prendre le max suffixe, sinon `01`. Réutiliser le batch de session déjà ouvert si le cadrage prépare un batch en cours. `mkdir -p brands/{slug}/creatives/{batch}/` (idempotent).

**2. Écrire `brands/{slug}/creatives/{batch}/frame.json`** via write_to_context, jamais par Edit/Write :

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/creatives/{batch}/frame.json" \
  --value '{...frame complet...}' \
  --source agent --confidence 0.9 --mode direct \
  --reason "Cadrage batch validé au gate frame-regime"
```

`--source agent --confidence 0.9` : le calcul des jauges et du régime est de l'agent. `--mode direct` : la validation humaine est déjà portée par `validated_by_operator: true` (gate Step 5), un stamping proposed fichier-entier n'ajouterait rien.

**Shape canonique (frame/1.0) :**

```json
{
  "_schema_version": "frame/1.0",
  "request": {
    "brand_slug": "...", "audience_slug": "... | null", "product_slug": "... | null",
    "objectives": ["conversion"],
    "constraints": { "budget": "500€ test", "deadline": null, "compliance": null, "formats_souhaités": null }
  },
  "gauges": {
    "atlas_richness": "thin | partial | rich",
    "perf_signal": "none | early | established",
    "asset_library": "empty | seeding | stocked",
    "evidence": { "audiences": 3, "pains_per_audience_min": 7, "psychology_fill": 0.6, "test_results": 0, "creatives_with_perf": 0, "assets_validated": 1 },
    "computed_at": "ISO-8601"
  },
  "regime": { "mode": "exploit | balanced | explore", "freedom_cursor": 0.62 },
  "rayon_max": 1,
  "support_mix": {
    "recommended": [ { "support": "static", "why": "..." } ],
    "alternatives": [ { "support": "video", "cost_note": "~3-4$ la pub générée" } ]
  },
  "origin": { "kind": "scratch | reverse", "reference_ad": null, "cursor_raw": 0.62, "bias_applied": false },
  "forks_log": [ { "fork": "asset-first", "accepted": true, "at": "ISO-8601", "note": "route brief humain avant production visuelle" } ],
  "validated_by_operator": true,
  "created_at": "ISO-8601"
}
```

Les `gauges.evidence` rendent le calcul re-jouable et auditable : un mainteneur (ou un re-run) peut vérifier pourquoi le curseur valait 0.62 ce jour-là.

**3. Finaliser :** `python3 .skills/finalize-mutation-batch.py --brand-slug {slug}`. Exit code 2 = corriger avant de clore.

**4. Qui lit frame.json en aval (contrat de consommation) :**

| Consommateur | Ce qu'il lit | Ce qu'il en fait |
|---|---|---|
| `produce-paid-angles` | `rayon_max` + `regime.mode` | borne les emprunts sectoriels du scoring, surface les emprunts comme paris |
| `evaluate-concept` | `rayon_max` (persisté, jamais re-dérivé) + `regime.mode` | check distance : un concept hors rayon est rejeté ou re-soumis comme pari explicite · les verdicts sont persistés par le flux dans `concepts/CPT-NN.json#evaluation` |
| `weave-hooks` | `regime.mode` + `gauges` top-level (3 enums) + `origin.kind` + `origin.reference_ad` + `rayon_max` | hérite le régime dans le genome-package qu'il assemble (projection des 3 enums seulement) · n'incarne que les `concepts/CPT-NN.json` approuvés |
| `compose-creative` | `regime.freedom_cursor` | régime de composition si pas de genome-package (lit déjà ce champ : curseur bas = pioche les patterns promus) |

**5. Close conversationnel.** UN next-step contextuel, fonction du régime validé et de ce qui existe déjà. Exemples calibrés (jamais templates récités) : régime validé + atlas correct → *"Le cadre est posé. Le move qui suit, c'est sortir la matrice d'angles dans ce cadre : les emprunts resteront bornés à ta verticale +1 et chaque pari sera flagué. On y va ?"* · fork asset-first accepté → *"Cadre posé en attente d'assets. Le move c'est le brief humain packshot d'abord : dès qu'un asset canon est validé, le batch repart avec une banque réelle."*

---

## Hard Rules

- **Never lancer une génération depuis ce skill.** Cadrage only. Aucun appel fal.ai, aucun angle produit, aucun brief créa rédigé. La production vit en aval, dans le cadre que ce skill vient de poser.
- **Always montrer les 3 jauges brutes à l'opérateur.** Niveau + preuve entre parenthèses, au NIVEAU LIVE (Step 2) ET au gate (Step 5). La transparence du raisonnement est la raison d'être du skill : un régime imposé sans jauges visibles est un régime que l'opérateur ne peut pas contester.
- **Never inventer une jauge quand la source est vide.** learnings.json absent, asset-library/ inexistant, audience sans pains → la jauge tombe au plancher (`thin`/`none`/`empty`), assumé et DIT à l'opérateur. Une jauge moyenne par confort fausse le curseur et tout l'aval.
- **Always cost-warning avant de recommander la video.** ~3-4$ la pub générée, signalé systématiquement dans le mix média, même quand l'objectif awareness rend la video évidente. L'opérateur engage du budget en conscience ou pas du tout.
- **Never menu plat.** UNE reco de régime défendue (jauges à l'appui), curseur ajustable, forks surfacés seulement quand leur condition est remplie. Jamais "exploit, balanced ou explore, tu préfères lequel ?".
- **Always tracer un fork accepté dans `forks_log[]`.** Avec timestamp et note. Un pari conscient non tracé devient un choix silencieux au batch suivant : le log est ce qui permet à learn-from-session et au prochain cadrage de savoir quel pari a été pris et pourquoi.
- **Pas de write sans validation.** `validated_by_operator: false` n'existe pas dans un frame.json persisté : pas de validation au gate Step 5, pas de frame, pas de production aval.

---

## Cross-references

- `.skills/skills/compose-creative/SKILL.md` · consommateur aval principal : lit `regime.freedom_cursor` (curseur bas = exploit, pioche les patterns promus) · convention `{batch}` STEP 0a reprise telle quelle ici
- `.skills/skills/produce-paid-angles/SKILL.md` · consommateur aval : `rayon_max` borne les emprunts sectoriels du scoring
- `weave-hooks` + `evaluate-concept` (drafts v2.90, même vague que ce skill) · consommateurs aval : régime hérité dans le genome-package, check distance vs rayon
- `.skills/skills/score-matrix/SKILL.md` · voisin de désambiguïsation : priorise des territoires existants, ne cadre pas un engagement de production
- `.skills/skills/setup-brand/SKILL.md` · route de refus du gate DUR Step 1 (marque introuvable)
- `resources/concepts/*` · banque de concepts cross-brand, plancher du mode explore (JAMAIS page blanche)
- `resources/conventions/creative-storage.md` (D#481) · forme batch `creatives/{batch}/`, résolution `{batch}`
- `.skills/write-to-context.py` · canal de mutation unique pour frame.json (mode direct · la validation humaine vit dans validated_by_operator, pas dans un stamping proposed)
- `resources/sops/creative-production/perf-feedback-loop.md` Step 4 · formule UNIQUE de la jauge perf_signal, citée jamais dupliquée
- `.skills/finalize-mutation-batch.py` · primitive mécanique de clôture (Step 6.3)
- `docs/system/investigation-posture.md` · jauges = Observé/Déduit explicites, jamais d'hypothèse affirmée en fait
- `docs/system/output-clarity-doctrine.md` · rendu opérateur Step 5 : langage métier, iconographie canon, zéro jargon interne
- Décisions R&D fondatrices · D#472/473 (design A1-A3 + réflexes pré-flight/surface-le-fork/flag-avant), D#477 (jauges), D#480 (emprunts cross-verticale = paris conscients, rayon sectoriel)
