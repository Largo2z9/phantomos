---
name: weight-dimensions
version: 1.1.1
type: producer
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: false
disambiguates_against:
  - profile-audience: "profile-audience structure les 8 dimensions raw. weight-dimensions PONDÈRE leur relevance par angle."
  - score-matrix: "score-matrix (futur v2.34) consomme weight-dimensions pour compute scoring final."
description: >
  v1.1.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (territoires-prioritisation). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  FR: "pondère les dimensions", "weight dimensions audience", "coefficient scoring".
  EN: "weight dimensions", "dimension relevance", "scoring coefficient".
consumes:
  - brands/{slug}/audiences/{audience}/profile.json (8 dimensions structurées)
  - brands/{slug}/angles/{angle}.json (formula + lineage)
  - resources/canon/copy/* (référentiel angle types)
  - path: docs/doctrine/territoires-prioritisation-doctrine.md
produces_validations_for: []
produces_proposals_for:
  - brands/{slug}/audiences/{audience}/dimension_weights.json (cache)
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/audiences/{slug}/dimension_weights.json via write_to_context]
  emits_events: [weights_computed]
pipeline:
  preconditions: ["profile.json existe avec 8 dimensions populated", "angles brand-side disponibles"]
  postconditions: ["dimension_weights.json présent", "sum weights = 1.0 ±0.01 par angle"]
prerequisites:
  - field: audiences/{slug}/profile.json#completeness
    threshold: 0.7
    level: L3
    fallback: origin_axis_biais_initiaux
    confidence_default: 0.5
  - field: angles/{angle_id}.json
    level: L1
    auto_pull: read_angle_target
    freshness_ttl_days: 30
---

# weight-dimensions

Producer skill machine-facing. Pour une audience donnée, calcule le poids relatif de chaque dimension (8 dimensions canon V3) pour chaque angle compatible. Sortie alimente le scoring matrice (Impact × Vitesse × Signal × modulateur dimension_relevance) consommé par `score-matrix` (v2.34+).

Non operator-facing par défaut. Exécuté en sous-skill par `score-matrix`. Si invoqué directement, surface vue compacte par audience.

## Hard Rules

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant calcul pondérations (Step 1), scanner prerequisites :

1. Lookup `angles/{angle_id}.json` → required, L1 read silent
2. Lookup `audiences/{slug}/profile.json#completeness` → si >= 0.7 → ponderation full canon V3 · si < 0.7 → L3 degraded · biais initiaux par origin_axis (audience-derived → Purchase/Problem/Benefit pèsent + · product-derived → Mechanism/Market pèsent + · etc.) · confidence 0.5 · flag _gaps

Output 8 weights sum 1.0 ±0.01 + dominant_top3 + confidence calculé.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

### HR1 · Load audience profile + angles list

Read `brands/{slug}/audiences/{audience}/profile.json` (8 dimensions populated obligatoire).
Read `brands/{slug}/angles/*.json` compatibles avec cette audience (filter via `awareness_movement.in ≤ profile.market_position.awareness_dominant` · RENAME C1 profile/2.3).

Si profile incomplet (une dimension manquante) ou aucun angle compatible : abort avec warning structuré, ne PAS écrire dimension_weights.json.

### HR2 · Pour chaque angle compatible, compute weights

Pour chaque combinaison (audience, angle) compatible :
- Pour chaque dimension parmi les 8 (`purchase_driver`, `problem_map`, `benefit_stack`, `mechanism`, `market_context`, `alternative_map`, `identity_signals`, `decision_process`) :
  - Évaluer relevance contextuelle (LLM-driven, pas hardcoded)
  - Sortir un poids 0.0-1.0
- Sum des 8 weights = 1.0 ±0.01

### HR3 · Heuristiques par origin_axis angle

Biais initiaux selon `origin_axis` de l'angle (PAS valeurs hardcoded, juste orientation contextuelle) :

- `audience-derived` → `purchase_driver` + `problem_map` + `benefit_stack` pèsent +
- `product-derived` → `mechanism` + `market_context` pèsent +
- `category-derived` → `alternative_map` + `market_context` pèsent +
- `brand-derived` → `identity_signals` pèsent +
- `temporal-cultural` → `identity_signals` + `decision_process` pèsent +

L'évaluation finale reste contextuelle (signal profile + signal angle prime sur le biais).

### HR4 · Identify dominant dimensions

Top 3 dimensions par angle (poids cumulatif > 0.6).
Skill flagge ces dimensions comme `dominant_top3` : leviers principaux pour cette combinaison audience × angle.

### HR5 · Persist via mutation gate

Write to `brands/{slug}/audiences/{audience}/dimension_weights.json` :

```json
{
  "audience_slug": "marathoniens-amateurs",
  "computed_at": "2026-05-04T10:00:00Z",
  "angles": {
    "ANG-01": {
      "dimensions": {
        "purchase_driver": 0.25,
        "problem_map": 0.30,
        "benefit_stack": 0.15,
        "mechanism": 0.10,
        "market_context": 0.05,
        "alternative_map": 0.05,
        "identity_signals": 0.05,
        "decision_process": 0.05
      },
      "dominant_top3": ["problem_map", "purchase_driver", "benefit_stack"],
      "sum_check": 1.0
    },
    "ANG-02": {}
  }
}
```

Toute écriture passe par `write_to_context` (mutation gate). Pas d'écriture directe FS.

### HR6 · Validate sum integrity

Pour chaque angle, vérifier `sum(dimensions) = 1.0 ±0.01`.
Si déséquilibre détecté :
- Tentative 1 : recompute avec contrainte normalisation explicite
- Tentative 2 : flag warning `sum_check_failed`, ne PAS persister cet angle

### HR7 · Output (machine-facing, pas operator-facing direct)

Skill non-operator-facing par défaut. Exécuté en sous-skill par `score-matrix` futur.

Si invoqué directement par opérateur, surface vue compacte par audience :

```
AUDIENCE {slug} · weights computed pour {N} angles
Top 3 dimensions par angle :
  ANG-01 : problem_map (30%) > purchase_driver (25%) > benefit_stack (15%)
  ANG-02 : mechanism (28%) > benefit_stack (22%) > market_context (18%)
```

Pas de prose analytique, pas de tableau verbeux. Vue dense.

### HR8 · Anti-patterns

- Ne JAMAIS hardcoder les weights (LLM contextuel obligatoire)
- Ne JAMAIS skip sum validation (1.0 ±0.01)
- Ne JAMAIS compute weights sans profile.json complet (8 dim populated)
- Ne JAMAIS écraser dimension_weights.json existant sans note timestamp dans `computed_at`
- Ne JAMAIS surface output operator-facing si invoqué en sous-skill (silent producer mode)

## Pipeline

### Preconditions

- `brands/{slug}/audiences/{audience}/profile.json` existe et 8 dimensions populated
- Au moins 1 angle compatible disponible dans `brands/{slug}/angles/`

### Postconditions

- `brands/{slug}/audiences/{audience}/dimension_weights.json` présent
- Sum weights = 1.0 ±0.01 par angle
- Event `weights_computed` émis

## Schema output

`brands/{slug}/audiences/{audience}/dimension_weights.json` :

| Field | Type | Description |
|---|---|---|
| `audience_slug` | string | slug audience source |
| `computed_at` | ISO-8601 | timestamp compute |
| `angles[ANG-XX].dimensions` | object | 8 dimensions → poids 0.0-1.0 |
| `angles[ANG-XX].dominant_top3` | array | 3 dim names cumul > 0.6 |
| `angles[ANG-XX].sum_check` | float | sum integrity (1.0 ±0.01) |
