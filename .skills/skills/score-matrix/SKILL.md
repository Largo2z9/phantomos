---
name: score-matrix
version: 1.2.2
type: producer
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
extension_hooks:
  - audience_entity   # NEW audiences custom scaffolded
  - angle_entity      # NEW angle types
  - creative_entity   # NEW creative types (e.g. video-script)
disambiguates_against:
  - weight-dimensions: "weight-dimensions calcule pondérations dimensions audience → angle (input). score-matrix CONSOMME ces weights pour scoring final matrice."
  - produce-paid-angles: "produce-paid-angles produit des angles individuels. score-matrix priorise les COMBINAISONS audience × angle."
  - frame-regime: "frame-regime cadre un engagement de production (régime + format) AVANT génération · score-matrix priorise des territoires d'angles existants."
  - evaluate-concept: "evaluate-concept rend un verdict binaire par concept candidat · score-matrix score une matrice de territoires."
description: >
  v1.2.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution (au début Hard Rules avant Step 0 DRGFP). Action LOURDE · narratif étendu 2 niveaux abstraction (macro contexte priorisation portfolio brand + micro top-3 territoires phrasé pourquoi en prose). Pose pair senior strategic director · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  v1.2.0 (v2.75.0 NEW extension_hooks frontmatter declaration · permet manifest registry scan Step 0 DRGFP enrichi · NEW entities scaffolded via scaffold-extension v1.2.0+ avec consumable_by matching ce skill consommées automatiquement runtime. Backward compat strict additif · extension_hooks vide default · legacy v2.74.x comportement hard-coded canon entities preserved. Pattern canon doctrine extension-discovery-doctrine.md NEW v2.75.0.)
  v1.1.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (territoires-prioritisation). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  FR: "score la matrice", "priorise les territoires", "matrice scoring", "top territoires", "where to test next".
  EN: "score matrix", "prioritize territories", "matrix scoring", "top territories".
consumes:
  - brands/{slug}/audiences/*/profile.json (sub-clusters)
  - brands/{slug}/audiences/*/dimension_weights.json (weight-dimensions output)
  - brands/{slug}/angles/*.json (angles populated)
  - brands/{slug}/brand.json (modulateurs strategic_context · à ajouter v2.35 ou via brand_equity_level + creative_zone proxy)
  - resources/canon/copy/* (référentiels)
  - path: docs/doctrine/territoires-prioritisation-doctrine.md
produces_proposals_for:
  - brands/{slug}/scoring/matrix-{date}.json (matrice scorée + top territoires)
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/scoring/matrix-{date}.json via write_to_context]
  emits_events: [matrix_scored, territories_prioritized]
pipeline:
  preconditions: ["audiences populées avec dimension_weights", "angles compatibles disponibles", "brand modulateurs disponibles ou défauts"]
  postconditions: ["matrice scorée Sub-cluster × Source d'angle", "top 3-5 territoires identifiés", "trous identifiés pour exploration", "action recommandée du close persistée en ligne In Progress idempotente dans brands/{slug}/todos.md (format canonique, tichée auto quand le skill aval tourne)"]
prerequisites:
  - field: audiences/*/dimension_weights.json
    level: L1
    auto_pull: read_weight_outputs
    freshness_ttl_days: 30
  - field: brand.strategic_context
    level: L3
    fallback: proxy_brand_equity_level
    confidence_default: 0.6
  - field: audiences/*/profile.json
    level: L1
    auto_pull: read_audiences_profiles
    freshness_ttl_days: 60
  - field: angles/*.json
    level: L1
    auto_pull: read_brand_angles_existing
    freshness_ttl_days: 90
---

# score-matrix

Producer skill operator-facing. Clôt la Phase 3 doctrine cartographie. Consomme `weight-dimensions` outputs (v2.33) + audiences profile + angles + brand modulateurs. Produit la matrice scorée Sub-cluster × Source d'angle (formule canon Notion : Impact × 3 + Vitesse × 2 + Signal × 1, modulé 0.5 à 2). Termine sur top territoires + trous + action recommandée.

Cohérence cross-skill : sourcing weights précomputés via `weight-dimensions`, sources d'angle alignées canon V3 (`creative-formula.md`), compatibilité awareness verrouillée doctrine canonical-matrix-reasoning.

## Hard Rules

### HR0 · Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ · matrice Sub-cluster × Source d'angle · formule canon Impact × 3 + Vitesse × 2 + Signal × 1 modulé 0.5 à 2 · modulateurs brand × stage business × compatibility rules · top 3-5 territoires output). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement disclosure pré-engagement en amont et top territoires + matrice scoring en aval.

Pattern obligatoire · l'agent verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique le contexte priorisation et score chaque cellule audience × angle, en prose narrative sobre (zéro matrice ASCII en LIVE · la matrice scorée finale vient en output post-scoring).

**2 niveaux d'abstraction obligatoires** ·

1. **Macro contexte priorisation portfolio brand** · verbaliser la compréhension du périmètre priorisation AVANT de rentrer dans le détail scoring cellule par cellule.
   Exemple score-matrix · "On part d'une brand {nom · positionnement macro · stade business inféré} qui a {N audiences sub-clusters cartographiées × N angles produits compatibles} prêts à être scorés. Mon hypothèse de pattern priorisation · {majoritairement audiences product-fit large × angles convergents · OU portfolio fragmenté audiences niches × angles divergents · OU concentration sur 1-2 audiences-hero à exploiter en priorité}. Stage business filter détecté · {early/growth/scale phrasé pourquoi · signaux brand encoded}. Mon hypothèse de territoires gagnants candidats AVANT scoring · {2-3 axes intuitivement prometteurs basés densité signal × cohérence positioning macro}. Modulateurs canon mobilisés · {brand_equity_level · creative_zone · stage business · compatibility rules awareness × sophistication phrasé pourquoi chacun pèse}."

2. **Micro top-3 territoires phrasé pourquoi** · verbaliser les territoires émergents en prose narrative pendant le scoring.
   Exemple score-matrix · "Cette cellule {audience sub-cluster nom × source d'angle phrasé} score élevé parce que · Impact {pourquoi cet angle résout pain prioritaire de cette audience · phrasé sans chiffre brut} → Vitesse {pourquoi production rapide · proof points dispo OR vernacular calibré OR canon archetype matchant} → Signal {pourquoi traction probable · density verbatims supportants OR pattern catégorie + brand fit OR whitespace concurrentiel détecté}. Modulateur appliqué · {compatibility rule awareness × sophistication phrasé pourquoi modulateur 0.5 à 2}. Cohérence avec positioning brand · {phrasé pourquoi ce territoire renforce vs dilue le positionnement macro}. Asymétrie remarquable vs intuition AVANT scoring · {phrasé · si territoire score plus haut OR plus bas qu'attendu pourquoi}."

**Calibration narrative** · prose sobre · registre pair senior strategic director · zéro jargon plumbing (jamais `scoring/matrix-{date}.json#cell_id`, `_field_types`, formules brutes `Impact × 3 + Vitesse × 2 + Signal × 1` en LIVE) · zéro tableau ASCII en LIVE (matrice scorée canon = output post-scoring). Cohérent strict Compositional Cartography §7 (no raw numeric scoring exposed to operator). Adapter le tonal au registre opérateur détecté (grounded · standard · dense).

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger entre cellules scorées si l'agent part dans une mauvaise direction d'inférence (mauvais Impact projeté · mauvais modulateur appliqué · mauvaise compatibility rule détectée · territoire candidat hors positioning) AVANT que la matrice finale cristallise sur cette base, (b) pédagogie · il apprend la posture stratégique experte sur priorisation paid DTC en regardant la manière de penser un scoring canon Impact × Vitesse × Signal × Modulateurs cross-audience × cross-angle.

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

### Step 0 · DRGFP Manifest Registry Scan (NEW v2.75.0)

Pre-flight discovery NEW entities scaffolded via scaffold-extension v1.2.0+ · 
scan `_extensions.json` OR `_manifest.json#extensions` pour entities avec 
`consumable_by: [{skill_name}]` matching CE skill.

Pour chaque NEW entity registered matching extension_hooks frontmatter ·
- Match `entity_type` ∈ frontmatter `extension_hooks` enum
- Match `consumable_by` field registry contains `{skill_name}` 
- Include NEW entity dans inputs Phase 1 pipeline ci-dessous
- Output enrichi avec lineage extension consommée dans frame

Halt si NEW entity registered sans `consumable_by` field flagué (scaffold-extension v1.2.0 legacy) · 
silent skip · pas error · l'opérateur peut patcher manuellement le scaffold-extension Phase 9 register-and-flag pour ajouter `consumable_by`.

Cross-ref doctrine canon · `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW.

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant construction grille (Step 1), scanner prerequisites :

1. Lookup `audiences/*/dimension_weights.json` → si présents → consume silent · sinon flag _gaps suggestion run weight-dimensions chain
2. Lookup `audiences/*/profile.json` → required, L1 silent (au moins 1 audience nécessaire)
3. Lookup `angles/*.json` brand existing → silent · cellules sans angle = trous détectés (signal output)
4. Lookup `brand.strategic_context` → si présent → modulateurs full · si absent → L3 degraded · proxy `brand_equity_level` · confidence 0.6 · flag _gaps

Output state map + confidence_chain[] init.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

### HR1 · Construire la grille

Lignes = sub-clusters audience (depuis `profile.json` par audience_slug, champ `sub_clusters[]`).
Colonnes = 5 sources d'angle canon V3 : `audience_derived`, `product_derived`, `category_derived`, `brand_derived`, `temporal_cultural`.
Cellule = territoire potentiel (sub_cluster × source).

Cardinalité maîtrisée (canon canonical-matrix-reasoning) : sub_clusters ≤ 5 max par scoring run, sources fixes 5. Total 25 cellules max default.
Si plus de 5 sub_clusters disponibles : surface warning operator + propose batch (run sur top 5 par taille audience, signaler les autres pour run suivant). Ne PAS scorer 6+ silently.

### HR2 · Vérifier compatibilité par cellule

Règle dure canon (canonical-matrix-reasoning) : `awareness_movement.in (angle) ≤ awareness_dominant (sub_cluster)`.
Pour chaque cellule :
- Lister angles du fichier `brands/{slug}/angles/*.json` dont `source_type` matche la colonne ET `awareness_movement.in ≤` awareness du sub_cluster.
- Si 0 angle activable : `compatibility = vierge`, score = 0, skip scoring (mais marquer comme trou potentiel HR5).
- Si 1+ angles activables : `compatibility = fort` (3+) | `moyen` (1-2), passer à HR3.

Ne JAMAIS skip cette règle. Cellule incompatible = 0 hard.

### HR3 · Calculer score brut Impact × Vitesse × Signal

Pour chaque cellule compatible, le LLM raisonne contextuellement (jamais hardcoder) sur 3 axes 0-10 :

**Impact (0-10) · coefficient × 3**
- Volume audience : taille relative du sub_cluster vs autres sub_clusters de la marque.
- Fit produit : croiser top dimensions du `dimension_weights.json` de cette audience avec bénéfices produit (`spec.json#benefits`).
- Score = moyenne pondérée volume + fit, échelle 0-10.

**Vitesse (0-10) · coefficient × 2**
- Asset dispo : packshot existe (`brand.json#visual_identity`) ? canon copy lookup direct sur la source ?
- Effort production estimé : low → 8, med → 5, high → 2.
- Score = combinaison asset_ready + effort_inverted.

**Signal (0-10) · coefficient × 1**
- Preuves observées : angles brand-side similaires déjà validés (`learnings.json#validations`) ?
- Concurrents performant sur cellule similaire (`brand.json#competitors` croisé avec source_angle) ?
- Canon `validations[]` entries pour mécaniques pertinentes.

`score_brut = Impact × 3 + Vitesse × 2 + Signal × 1` (max 60).

### HR4 · Appliquer modulateurs brand (4 axes)

Lookup `brand.json#strategic_context` (v2.35+) ou défaut via proxy.

| Axe | Valeur | Coefficient |
|---|---|---|
| stade_brand | launch | × 1.2 (territoires d'éducation marché) |
| | growth | × 1.0 (default) |
| | scale | × 0.9 (territoires éprouvés) |
| | mature | × 0.8 (préserve plutôt que test) |
| moment_strategique | pmf | × 1.3 (territoires d'apprentissage) |
| | scaling | × 0.9 (winners only) |
| | defense | × 0.8 (cellules brand_derived) |
| | repositionnement | × 1.2 (reframes radicaux) |
| contexte_marche | nascent | × 1.2 (territoires éducatifs) |
| | mature | × 1.0 |
| | hyper_sature | × 0.8 (sauf reframe différenciant) |
| etat_atlas | vide | × 1.3 (fast-learning, scoring tolérant) |
| | partiel | × 1.0 |
| | consolide | × 0.9 (critères durcis) |

Si `strategic_context` absent : proxy via `brand_equity_level` (low → × 1.1, medium → × 1.0, high → × 0.95) appliqué uniformément sur axe stade_brand, autres axes = × 1.0 default.

`coefficient_cumule = stade × moment × marche × atlas`, capped `[0.5, 2.0]`.
`score_dynamique = score_brut × coefficient_cumule`.

Ne JAMAIS appliquer modulateurs hors bornes 0.5-2.

### HR5 · Identifier top territoires + trous + cellules vierges

- **Top territoires** : 3-5 cellules avec `score_dynamique` le plus haut, rank descendant.
- **Trous à combler** : cellules `compatibility = vierge` MAIS sub_cluster fort (top 3 par taille) ET source d'angle naturellement riche pour la marque (heuristique : audience_derived et product_derived prioritaires si trous). Signal pour run `produce-paid-angles`.
- **Cellules vierges acceptables** : compatibilité possible mais 0 angle dispo sur sub_cluster faible → noter sans flagger.

### HR6 · Persist matrix-{date}.json via write_to_context

Format canonique :

```json
{
  "computed_at": "ISO8601",
  "brand_slug": "...",
  "modulators_applied": {
    "stade_brand": "growth",
    "moment_strategique": "scaling",
    "contexte_marche": "mature",
    "etat_atlas": "partiel",
    "coefficient_cumule": 1.0
  },
  "matrix": {
    "sub_clusters": ["..."],
    "sources_angle": ["audience_derived", "product_derived", "category_derived", "brand_derived", "temporal_cultural"],
    "cells": [
      {
        "sub_cluster": "...",
        "source_angle": "...",
        "compatibility": "fort|moyen|vierge",
        "angles_activables": ["ANG-01", "ANG-03"],
        "impact": 7,
        "vitesse": 6,
        "signal": 4,
        "score_brut": 37,
        "score_dynamique": 44,
        "rank": 1
      }
    ]
  },
  "top_territoires": [...],
  "trous_a_combler": [...]
}
```

Path : `brands/{slug}/scoring/matrix-{YYYY-MM-DD}.json`. Mode `proposed`. Émettre events `matrix_scored` puis `territories_prioritized`.

### HR7 · Output operator-facing matrice ASCII

Ne JAMAIS exposer JSON brut. Toujours rendre vue compacte lisible :

```
═══════════════════════════════════════════════════════════════
{BRAND} · MATRICE SCORÉE · {date}
═══════════════════════════════════════════════════════════════
Modulateurs : stade {x} · moment {y} · marché {z} · atlas {w} · coeff cumulé {n}

┌────────────────────────────┬────────┬────────┬────────┬────────┬────────┐
│ Sub-cluster                │ aud-d  │ prod-d │ cat-d  │ brand-d│ temp-c │
├────────────────────────────┼────────┼────────┼────────┼────────┼────────┤
│ {sub_cluster_1}            │ 55 🔥  │ 42     │ 38     │ 0      │ 28     │
│ {sub_cluster_2}            │ 48     │ 52 🔥  │ 0      │ 35     │ 0      │
└────────────────────────────┴────────┴────────┴────────┴────────┴────────┘

TOP 3 TERRITOIRES
  1. {sub_cluster} × {source}  · score {n}  · {angles activables}
  2. ...

TROUS DÉTECTÉS (compatibles mais aucun angle)
  - {sub_cluster} × {source}  · run produce-paid-angles ?

→ Action recommandée : tester top 1 (run produce-copy-brief) · OU explorer top 2 trou
```

Marquer 🔥 sur top 1 par ligne. `0` sur cellules vierges. Aucun em-dash dans tout le rendu (substituer par `·`, virgule, deux-points).

### HR7bis · Persist l'action recommandée (v1.2.2, additif strict)

La ligne `→ Action recommandée` du rendu HR7 propose un prochain mouvement (tester le top 1 via produce-copy-brief · explorer un trou via produce-paid-angles). Elle vit dans la matrice rendue à l'écran. Mais une action qui ne vit que dans le chat meurt au prochain tour. Ce step lui donne une **trace persistante** · une ligne dans la todo de la brand, sans rien retirer de la matrice ASCII ni de la ligne action, qui restent tels quels.

Pattern déjà prouvé par `register-and-flag` Step 6 (write idempotent d'une ligne de tracking dans `brands/{slug}/todos.md`).

**Geste** · après le rendu HR7 (et le persist HR6 du matrix-{date}.json), écrire une ligne unique dans `brands/{slug}/todos.md → ## In Progress` au **format de ligne canonique** ·

```
- [ ] {Name} | P: {0-3} | E: {low|med|high} | T: {durée}
```

- `Name` · l'action recommandée verbalisée court depuis le top territoire ou le trou prioritaire (ex `produce-copy-brief sur le top territoire {sub_cluster} × {source}`, `produce-paid-angles sur le trou {sub_cluster} × {source}`). Operator-language + nom de skill aval recevable dans la ligne (réceptacle backstage).
- `P` · priorité dérivée du scoring · action sur le top 1 territoire (score_dynamique le plus haut) → `P: 1` · exploration d'un trou secondaire → `P: 2`.
- `E` · effort du skill aval (low pour un brief ciblé, med pour une matrice d'angles sur un trou).
- `T` · ETA verbalisé du skill aval (ex `15 min`, `quelques heures`), aligné `feedback_client_effort_scale` si client-facing.

**Un seul next-step persisté par run** · le prioritaire (le top 1 territoire, ou le trou le plus structurant si l'action recommandée pointe vers l'exploration). Les autres territoires et trous restent listés dans HR5/HR7, non dupliqués en todo (anti-bruit · la todo porte le mouvement, pas l'inventaire complet).

**Idempotence (dure, comme register-and-flag).** Avant d'écrire, scanner `## In Progress` · si une ligne porte déjà le même `Name` (même skill aval + même territoire/trou cible), ne pas dupliquer. Re-scoring de la même brand qui ressort le même top = zéro nouvelle ligne. Le write passe par le mutation gate (cohérent HR8 anti-pattern · jamais éditer le JSON ni le markdown directement) ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/todos.md#in-progress" --value "- [ ] {Name} | P: {n} | E: {level} | T: {eta}" --source agent --mode direct --reason "Persist action recommandée from score-matrix close (idempotent)"
```

Si `write-to-context.py` ne route pas le markdown todos, fallback `register-and-flag` (sous-skill curator) · même réceptacle, même idempotence. Ne JAMAIS hand-editer le markdown todos hors gate.

**Auto-tick aval.** La ligne est cochée `[x]` automatiquement quand le skill aval nommé tourne et produit son artifact · `produce-copy-brief` (Step 8bis) et `produce-paid-angles` (Step 12ter) lisent `## In Progress` à leur finalize, matchent une ligne dont le `Name` les désigne comme skill aval avec le même territoire/trou cible, et la basculent `[x]` (archivée selon la doctrine todos racine). Pas de tick manuel · le downstream ferme la boucle. Si aucune ligne ne matche, le downstream ne crée rien et continue (silencieux).

**Léger, jamais bloquant.** Échec du write (gate refuse, fichier absent) → flag interne silencieux, ne casse pas le ship de la matrice. La trace todo est un bonus de persistance, pas une précondition.

**Doctrine.** Report des étapes différées et matérialisation des next-steps comme tâches reprenables avec leur levier · `docs/system/onboarding-setup-flow.md` (sections « Exhaustivité offerte, jamais forcée, reportable » et « La persistance est native »). Référencée ici, pas redupliquée.

### HR8 · Anti-patterns

- Ne JAMAIS scorer sans `dimension_weights.json` précomputés. Si absent : abort + propose `weight-dimensions` d'abord.
- Ne JAMAIS skip awareness compatibility (HR2). Cellule incompatible = 0 hard, jamais scorée.
- Ne JAMAIS hardcoder Impact / Vitesse / Signal. LLM raisonne contextuellement à chaque run.
- Ne JAMAIS appliquer coefficient cumulé > 2.0 ou < 0.5. Cap obligatoire.
- Ne JAMAIS exposer JSON brut à l'opérateur. Toujours rendre vue ASCII HR7.
- Ne JAMAIS scorer 6+ sub_clusters silently. Warning + batch obligatoire (HR1).
- Ne JAMAIS éditer le JSON directement. Mutation gate `write_to_context` obligatoire.

## Cross-refs

- Doctrine canon Notion Stride-Up · formule scoring brut + modulateurs 4 axes
- `weight-dimensions` v1.0 · sibling producer, output `dimension_weights.json` consommé en HR3
- `creative-formula.md` V3 · 5 sources d'angle canoniques colonnes matrice
- `docs/system/canonical-matrix-reasoning.md` · cardinalité ≤ 5, awareness compatibility hard rule
- `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ NIVEAU LIVE · doctrine racine 3 phases temporelles · AVANT exec disclosure pré-engagement · PENDANT exec NIVEAU LIVE thinking aloud expert action LOURDE 2 niveaux abstraction macro contexte priorisation + micro top-3 territoires phrasé pourquoi · APRÈS exec top territoires + matrice scoring synthèse (no raw numeric scoring exposed canon Compositional Cartography §7) · HR-DVD-11 + AP-DVD-11 enforcement.
- `docs/system/skill-authoring-doctrine.md` · frontmatter triad + lifecycle
- `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW (extension_hooks + manifest registry scan canon)
- `scaffold-extension` v1.2.0+ Phase 9 register-and-flag (upstream registry NEW entities)
- `produce-paid-angles` · downstream sur trous détectés
- `produce-copy-brief` · downstream sur top territoire validé
