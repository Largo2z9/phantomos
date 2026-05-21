---
name: recompose-creative
version: 1.3.0
patch_notes_v2_87_4:
  - "1.3.0 (v2.87.4 canonical many-to-many enforcement mirror) · NEW HR-RC-CANON-1 mirror sibling compose-creative v1.8.0 · enforcement entry canonical `brands/{slug}/creatives/{CRT-NN}/` OBLIGATOIRE post-recomposition. Toute variante DOIT être NEW entry canonical (pas surcharge entry parent · variant_of ref dans lineage) · lineage populated avec `variant_of: CRT-{parent}` + tags variant typed (concept stable · creative new · variant true) + cross-refs many-to-many activés. Asset JPG sauvé dans `creatives/{CRT-NN}/produced/` (pas hors structure). Closes audit Fincut v2.87.3 finding · variantes générées sans entry canonical = perte traçabilité parent/enfant + tableau composition cassé. Backward compat strict additif. NOTE Notion bridge auto-wire DEFERRED v2.88.0+ (sync-creatives-to-notion pas shipped)."
type: producer
isolation_scope: brand_only
layer: production
recommended_model: opus
subagent_safe: true
mode: proposed
operator_facing: true
patch_notes:
  v1.2.1: "v2.51 operator-fiche-output canonique template applied · header + gate + footer refactor langage métier. HR1 menu variant_axis refactor · drop enum technique `(new_audience) / (new_platform : Meta → TikTok)` entre parenthèses, plain language seulement. Operator output template header refactor · `RECOMPOSE · CRT-N → CRT-X · variant_axis: hook_swap` → `═══ {BRAND_HUMAIN} · Variante de la pub n°{N_source} ═══` + sous-titre plain language. Body refactor selon canonique resources/templates/operator-fiche-output.md (drop `concept_id`, `variant_of`, `variant_axis` en surface · vit en backstage creative.json). Footer · 1 reco soft offer 1 ligne max."
  v1.2.0: "v2.46 endpoint migration nano-banana-pro/edit (Gemini 2.5 Flash Image legacy) → nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025). Cohérent compose-creative v1.2 + craft-packshot v1.1 upstream. Frontmatter permissions.external_apis[] déclare provider + endpoint + version_check_url + version_canon_date + replaced_legacy. HR4 prompt structure pipeline mirror nano-banana-2/edit · pattern adapt-from-source preservation-first préservé. Cross-ref doctrine model-versioning-canon v2.44."
description: >
  v1.2.2 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.0.0 (v2.34 ship production loop) : 3e skill P5 visual aux côtés de decompose-ad
  (reverse) et compose-creative (forward). Adapte une créa interne testée (ou
  hypothesis) en variante alignée sur UNE dimension changée : new_audience,
  new_platform, new_format, new_hook, new_visual_treatment. Output : nouveau
  CRT-X qui réutilise concept_id parent + flag variant_of source + variant_axis
  explicite. Préserve concept core (mécanique, ton, intent_mix) ; ne change
  qu'une dimension à la fois. Persist creative.schema v1.2 brand-side avec
  meta.validation_status = hypothesis (tag derived_from_test_results si la
  source a un score). Pipeline visuel mirror compose-creative (HR3) avec prompt
  adapté preservation-first. Output operator-facing : vue compacte side-by-side
  source vs variant + brief markdown explicit "WHAT CHANGED vs SOURCE".
  FR: "adapte cette créa", "version pour autre audience", "déclinaison",
  "variant créa", "variante TikTok", "version story", "décline cette créa".
  EN: "adapt this creative", "version for another audience", "variant",
  "tiktok version", "story version", "decline this creative".
triggers_fr:
  - "adapte cette créa"
  - "version pour autre audience"
  - "déclinaison"
  - "variant créa"
  - "variante TikTok"
  - "version story"
  - "décline cette créa"
triggers_en:
  - "adapt this creative"
  - "version for another audience"
  - "variant"
  - "tiktok version"
  - "story version"
  - "decline this creative"
disambiguates_against:
  compose-creative: "compose-creative crée ex nihilo depuis brand intelligence + angle. recompose-creative ADAPTE un creative existant (1 dimension change, concept core préservé)."
  decompose-ad: "decompose-ad analyse une ad EXTERNE (reverse-engineering benchmark concurrent). recompose-creative adapte une créa INTERNE (mode internal_production, source CRT-N déjà persisté)."
  produce-paid-angles: "produce-paid-angles produit un nouveau ANGLE (forward generation depuis brand intelligence). recompose-creative garde l'angle, change autre dimension (audience/platform/format/hook/visual)."
consumes:
  - path: brands/{slug}/produced/{CRT-N}.json
    min_version: 1.2.0
    note: creative source obligatoire ; concept_id réutilisé pour variant
  - path: brands/{slug}/audiences/{audience_slug}/profile.json
    min_version: 1.0.0
    note: requis si variant_axis = new_audience
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: packshots clean URL + distinctive features pour préserver fidélité produit en regen
  - path: resources/schemas/creative.schema.json
    min_version: 1.2.0
  - path: resources/canon/copy/formats-livrables/*.json
    min_version: 1.0.0
    note: requis si variant_axis = new_platform ou new_format (lookup contraintes ratio/durée/ton)
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
produces_proposals_for:
  - brands/{slug}/produced/{CRT-X}.json
  - brands/{slug}/produced/{CRT-X}.jpg
  - brands/{slug}/produced/{CRT-X}.md
prerequisites:
  - field: produced/{creative_id}.json
    level: L1
    auto_pull: read_creative_source
    freshness_ttl_days: 60
  - field: variant_axis
    level: L2
    options:
      - new_audience
      - new_platform
      - new_hook
      - new_visual_treatment
  - field: resources/canon/copy/formats-livrables
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
permissions:
  reads: [brand, product, profile, learning, creative, canon_copy, registries]
  writes: [creative]
  emits_events: [creative_recomposed, variant_generated]
  mode: proposed
  subagent_safe: true
  external_apis:
    - provider: "fal.ai"
      endpoint: "fal-ai/nano-banana-2/edit"
      model_family: "gemini_3_pro_image_novembre_2025"
      version_check_url: "https://fal.ai/models?keywords=banana"
      version_canon_date: "2025-11"
      replaced_legacy: "fal-ai/nano-banana-pro/edit (v1.0.x · Gemini 2.5 Flash Image)"
      auto_upgrade: false
pipeline:
  preconditions: |
    creative source CRT-N existe sous brands/{slug}/produced/.
    1 dimension change explicite (variant_axis ∈ [new_audience, new_platform, new_format, new_hook, new_visual_treatment]).
    Credentials FAL_API_KEY présent dans credentials_shared.env pour pipeline visuel.
    Si variant_axis = new_audience, audience cible profile.json existe.
    Si variant_axis = new_platform ou new_format, canon formats-livrables disponible pour cette plateforme/format.
  postconditions: |
    Nouvelle CRT-X persistée avec concept_id réutilisé, variant_of=CRT-N, variant_axis explicite.
    JPG local + brief markdown générés.
    meta.validation_status = {status: hypothesis, confidence: 0.5, source: derived_from_test_results}.
    tags.source = "internal_production".
    validate-resources triggered silencieusement.
---

# Skill: recompose-creative

> **Adapt an existing internal creative.** v1.0.0 · v2.34 ship production loop · creative.schema v1.2 · 3e skill P5 visual.

Adaptateur, not generator. Lit un creative interne déjà persisté (CRT-N), change UNE dimension explicitement déclarée par l'opérateur, persiste un instance creative.schema v1.2 brand-side avec variant_of + variant_axis tracking, rend une vue side-by-side source vs variant à l'opérateur en langage clair. Concept core (mécanique, ton, intent_mix) toujours préservé. Pour refonte 2+ dimensions ou nouveau concept, route vers compose-creative.

## Tone

Posture collègue senior media buying qui décline une créa testée. Pas inventeur. La fiche est dense mais lisible : ce qui reste vs ce qui change, justification courte de l'adaptation, comparaison side-by-side. Aucun JSON brut, aucun field_path interne. Si une dimension n'est pas explicitement déclarée, AskUserQuestion pour la fixer avant tout pipeline visuel.

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant adaptation (Step 1), scanner prerequisites :

1. L1 silent · `produced/{creative_id}.json` (required) · `resources/canon/copy/formats-livrables`
2. L2 gate · `variant_axis` non spécifié → AskUserQuestion 5 options (new_audience / new_platform / new_format / new_hook / new_visual_treatment)

Output state map + confidence_chain[] init avec variant_axis selected.

---

## Hard Rules

### HR1 · Identify variant axis explicit

Skill exige opérateur précise QUELLE dimension change. Surface au démarrage en langage clair, zéro enum technique entre parenthèses ·

```
Tu veux changer quoi sur cette créa ? Une seule chose à la fois ·
(a) l'audience cible
(b) la plateforme (par exemple Meta → TikTok)
(c) le format (image → carrousel, story → reel)
(d) le hook copy (variant A/B même visuel)
(e) le traitement visuel (variant scène, même hook)
```

Si l'opérateur reste ambigu ou tente de changer 2+ dimensions, AskUserQuestion mandatoire. Rappel · 2+ dimensions change = route compose-creative (nouveau concept), pas recompose-creative.

**Backstage mapping (NON surface operator)** · le choix opérateur (a)-(e) mappe sur `variant_axis` enum technique persisté dans creative.json (`new_audience`, `new_platform`, `new_format`, `hook_swap`, `visual_treatment_swap`). Cet enum reste backstage pour retrieval programmatique · operator ne le voit jamais.

### HR2 · Load creative source + identify what stays vs changes

Lire `brands/{slug}/produced/{CRT_source}.json` :
- Capturer `concept_id` source (sera réutilisé pour le variant, pas régénéré)
- Capturer tous les champs creative.schema v1.2 (mécanique, ton, intent_mix, format, stop_scroller, etc.)

Selon variant_axis, marquer rigoureusement ce qui reste vs ce qui change :

| variant_axis | Reste inchangé | Change |
|---|---|---|
| `new_audience` | mécanique, format, visuel, hook | `context.angle.audience_ref`, `context.persona` |
| `new_platform` | concept core, hook, mécanique | `format.type`, `format.ratio`, contraintes platform-specific |
| `new_format` | mécanique, hook, ton | `format.type` (image → carrousel, etc.) |
| `new_hook` | visual_layer, mécanique, intent_mix | `stop_scroller.hook_layer.verbal` |
| `new_visual_treatment` | hook_layer, mécanique, ton | `stop_scroller.visual_layer` |

Anti-pattern : retain 0 dimension du concept core = c'est compose-creative déguisé, refuser et re-router.

### HR3 · Apply contraintes platform/format spécifiques

Si variant_axis = `new_platform` ou `new_format`, lookup `resources/canon/copy/formats-livrables/{platform}.json` :

- **TikTok** : ratio 9:16, attention < 3 sec, native UGC plus fort, music context
- **Instagram Story** : ratio 9:16, swipe up CTA, sticker tap
- **Instagram Reel** : ratio 9:16, hook < 2 sec, trending audio, scroll-stop visuel
- **LinkedIn** : ratio 1.91:1 ou 1:1, ton professionnel, B2B context
- **YouTube Shorts** : ratio 9:16, hook < 5 sec, story arc compact
- **Meta Feed** : ratio 4:5 ou 1:1, hook scroll-stop visuel + verbal layered
- **Pinterest** : ratio 2:3 vertical, search-driven keywords visibles

Adapter les fields creative.schema concernés (`format.type`, `format.ratio`, `stop_scroller.dominance`, ton register). Si canon silencieux sur la plateforme demandée, surfacer à l'opérateur (*"pas de canon formats-livrables pour {platform}, je peux improviser sur les contraintes natives connues ou tu valides un override ?"*).

### HR4 · Génération visuelle adaptée (preservation-first)

Pipeline mirror compose-creative HR3 (FAL nano-banana-2/edit canon v2.46), prompt ajusté pour préserver le concept core :

- **Référence visuel original** : image_urls inclut `/tmp/compose-creative/{CRT_source}.jpg` (ou path persisté `brands/{slug}/produced/{CRT_source}.jpg`)
- **Référence packshot** : image_urls inclut `spec.visual_identity.packshots.primary_front` clean URL
- **Prompt structure** :
  ```
  Adapt this creative for {new_dimension_value}, preserving the core concept
  ({mecanique} + {hook}), changing only {what_changes_explicit}.
  
  CRITICAL preservation : {concept_id_signature} (mécanique, ton, intent_mix).
  CRITICAL change : {variant_axis_payload}.
  Product fidelity : {distinctive_features from spec.visual_identity}.
  ```
- **Retry** : max 2 si label produit régresse (audit S55 v2.34 sur endpoint legacy nano-banana-pro/edit · sans visual_identity le model régressait wordmark with brackets en variantes sans brackets ou caractères corrompus · pattern préservé avec nano-banana-2/edit mais marges plus généreuses sur text fidelity natif). Au 3e échec, surfacer à l'opérateur.

### HR5 · Generate variant brief markdown

Format opérateur-facing avec section explicite "WHAT CHANGED vs SOURCE" :

```markdown
# CRT-X · Variant of CRT-N

## Concept préservé
- concept_id : {cpt_id}
- mécanique : {mechanic}
- ton : {ton}
- intent_mix : {primary, secondary, weights}

## What stays
- [list per HR2 table]

## What changes
- {variant_axis} : {old_value} → {new_value}
- Justification : {why_this_change}

## Side-by-side
| Field | Source (CRT-N) | Variant (CRT-X) |
|---|---|---|
| audience | ... | ... |
| platform | ... | ... |
| format | ... | ... |
| ratio | ... | ... |

## Test recommendation
{a/b vs source · 2 autres axes à explorer si performant · score-matrix}
```

### HR6 · Persist variant creative.json

Conforme creative.schema v1.2. **NEVER** Edit/Write direct JSON, **ALWAYS** via `write_to_context` :

- `concept_id` = source.concept_id (réutilisé, pas régénéré)
- `creative_id` = nouveau CRT-X (incrément brand-scope)
- `variant_of` = source.creative_id (CRT-N)
- `variant_axis` ∈ enum [`photo_swap`, `promo_toggle`, `hook_swap`, `background_swap`, `persona_split`, `platform_swap`, `format_swap`, `visual_treatment_swap`, `audience_swap`]
- `meta.validation_status` = `{status: "hypothesis", confidence: 0.5, source: "derived_from_test_results"}` si la source CRT-N a un score testé, sinon `source: "derived_from_hypothesis"`
- `tags.source` = `"internal_production"`
- Tous les autres fields hérités de la source sauf ceux explicitement changés par variant_axis

Trigger `validate-resources` silencieusement post-write. Surface MAJOR/CRITICAL uniquement.

### HR7 · Output operator-facing

Vue compacte side-by-side source vs variant. Reco no-orphan-output finale :

- Suggest A/B test source vs variant si pas encore testé
- Suggest 2 autres axes de variation à explorer si concept performant en source
- Suggest `score-matrix` pour prioriser variants à tester si déjà 3+ variants existent

### HR8 · Anti-patterns

- **NEVER** recomposer sans variant_axis explicite (mode hypothesis trop large, pollue creative DB)
- **NEVER** changer 2+ dimensions simultanées (c'est un nouveau concept, route compose-creative)
- **NEVER** écraser le creative source (toujours nouveau CRT-X avec variant_of, source append-only)
- **NEVER** skip retain de concept core (sinon c'est compose-creative déguisé, refuser et re-router)
- **NEVER** exposer JSON brut, field_path, ou enum interne (`variant_axis` valeurs) à l'opérateur en surface output. Traduire en langage clair (*"on garde le hook, on change juste le format"*)
- **NEVER** Edit/Write direct sur `.json` brand-side (mutation rule, toujours `write_to_context`)
- **NEVER** régénérer `concept_id` (variant = même concept, dimension différente)

## Operator output template

Réf canonique · `resources/templates/operator-fiche-output.md`. Header plain language, body en vocabulaire métier, footer soft offer 1 ligne max. Bloc `concept_id` / `variant_of` / `variant_axis` persiste en backstage (creative.json) · operator ne le voit jamais.

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Variante de la pub n°{N_source}
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD} · {1 phrase plain language · ex "même concept, audience changée pour femmes 45-55 ménopause"}

───────────────────────────────────────────────────────────────
Ce qui reste
───────────────────────────────────────────────────────────────
Mécanique          {nom métier · ex "before-after-bridge"}
Ton                {plain · ex "direct response avec touche brand"}
Hook texte         "{verbatim hook · si retenu}"

───────────────────────────────────────────────────────────────
Ce qui change
───────────────────────────────────────────────────────────────
Dimension          {plain · ex "audience cible" ou "plateforme" ou "format" ou "hook texte" ou "traitement visuel"}
Avant              {plain · ex "femmes 30-45 post-grossesse"}
Après              {plain · ex "femmes 45-55 ménopause"}
Pourquoi           {1 phrase justif · ex "trigger émotionnel différent, registre copy à recalibrer"}

───────────────────────────────────────────────────────────────
Comparaison
───────────────────────────────────────────────────────────────
                   PUB n°{N_source}        VARIANTE n°{N_variant}
Cible              {old_audience}          {new_audience}
Plateforme         {old_platform}          {new_platform}
Format             {old_format}            {new_format}
{autres si changent}

Photo générée      ouvre dans Preview · open {path}

───────────────────────────────────────────────────────────────
{1 reco soft offer 1 ligne max · ex "Si tu veux, on peut tester A/B la source vs la variante."}
```

**Backstage (creative.json, NON rendu operator)** · `concept_id` (réutilisé source), `variant_of: {creative_id_source}`, `variant_axis` enum, `meta.validation_status`, `tags.source: internal_production`. Vivent dans le JSON pour retrieval programmatique · operator ne les voit jamais.

**Validation pre-ship fiche** ·
1. Header ne contient pas `RECOMPOSE`, `CRT-N → CRT-X`, `variant_axis:`, `concept_id`
2. Body ne contient pas `intent_mix: {...}`, `variant_of`, field paths JSON
3. Footer · 1 phrase soft offer max, jamais menu, jamais nommer skill `score-matrix` en surface

## Cross-refs

- `compose-creative` (forward generation ex nihilo, sibling P5 visual)
- `decompose-ad` (reverse-engineering ad externe, sibling P5 visual)
- `creative.schema.json` v1.2 (variant_of, variant_axis, meta.validation_status)
- `resources/canon/copy/formats-livrables/*.json` (contraintes platform/format)
- `docs/system/skill-authoring-doctrine.md` (frontmatter triad, type producer baseline)
- `docs/system/canonical-matrix-reasoning.md` (préservation concept core = matrix-driven)
- `validate-resources` (post-write silencieux)
