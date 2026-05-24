---
name: compose-creative
version: 1.8.0
patch_notes_v2_87_4:
  - "1.8.0 (v2.87.4 canonical many-to-many enforcement) · NEW HR-CC-CANON-1 · enforcement entry canonical `brands/{slug}/creatives/{CRT-NN}/` OBLIGATOIRE post-génération. Anti-pattern banned · sauver asset JPG/PNG standalone hors structure canonical (e.g. `visual-identity/creative_ANG-01_*.jpg` orphelin). Toute génération DOIT créer · (1) `creatives/{CRT-NN}/creative.json` conforme creative.schema v1.2+ avec lineage populated (angle_ref + audience_ref + product_ref + mechanism_ref + concept_ref) + tags populated (concept + creative + variant + mécanique narrative typed) + cross-refs many-to-many activés. (2) asset JPG sauvé dans `creatives/{CRT-NN}/produced/` (pas hors structure). (3) brief copy markdown S55 fiche v5 dans `creatives/{CRT-NN}/brief.md`. Closes audit Fincut session v2.87.3 finding · compose-creative générait visuel sans entry canonical · perte traçabilité + pas de tableau composition + pas de base de données imbriquée many-to-many. Backward compat strict additif · cycle runtime Step 0 → Step 4 preserved · seul l'output enforcement change. NOTE Notion bridge auto-wire creatives DEFERRED v2.88.0+ · skill `sync-creatives-to-notion` pas encore shipped (sync-notion-atlas v2.0.1 territoire-only canon respecté · creatives = production layer skill séparé). Backlog mainteneur."
patch_notes_v2_87_6:
  - "1.8.0 (v2.87.6 SUBSTRATE sprint · enforcement many-to-many + dream_scenario_narrative consume) · Sprint substrate canon · refresh atlas Stepprs deep desire chain v2.87.4 (chronic-pain-45 grand-parent narrative + workers-shifts conjoint Friday evening narrative) + NEW section walkthrough Porte A many-to-many `tour.md` Anatomie de la structure. Impact ce skill · compose-creative consume désormais `audiences/{slug}/profile.json#psychology.dream_scenario_narrative` (canon v2.87.4) pour brief copy S55 fiche v5 · le target_recipient relationnel (grand-parent transgénérationnel · conjoint post-shift) et le social_payoff doivent flow vers le visual concept + le hook copy. Pattern · si dream_scenario_narrative présent dans audience cible → encode visual cue relationnel (grand-mère + petits-enfants au parc · conjointe + mari sortie restaurant) plutôt que generic product shot. Closes gap v2.87.4 · canon deep desire chain existait dans schema mais consume runtime compose-creative restait fonctionnel pain-relief flat. Enforcement many-to-many entry canonical hardcoded préservé v2.87.4 · v2.87.6 ajoute consume substrate dream_scenario_narrative déclaratif · runtime implementation backlog v2.88.0+ (pattern miroir v2.87.5 · scope chirurgical patch_notes vs refonte massive runtime). Backward compat strict additif."
type: producer
isolation_scope: brand_only
layer: production
recommended_model: opus
subagent_safe: true
mode: proposed
operator_facing: true
reasoning_pattern: matrix-driven
matrix_mode: composing
patch_notes:
  v1.7.0: "v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés · Section pré-runtime ajoutée AVANT HR1 (detect input mode) · expose 6 paramètres décomposés au runtime (brief source · mécanique creative · variants visuels · hook variants · packshot/asset · hypothèses figées · biais à éviter) avec POURQUOI chacun + close binaire OK ou ajuste. Cross-ref doctrines `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ + `docs/system/engagement-disclosure-doctrine.md` v2.79.5+. Backward compat strict additif (HR1-HR7 runtime preserved · seul l'amont disclosure change)."
  v1.6.0: "v2.64 ontologie sémantique pure pain_points + objections sub-audience · HR2 CONTEXTE refactor · `context.pain_point` lookup canonical `audiences/{audience_slug}/pain_points/{PNT-NN}.json` (sub-audience NEW v2.64 · owned natif par parent path). HR5 persist · creative.json#context.pain_point_ref stage PNT-NN canonical (lookup chain sub-audience d'abord). Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved. Cohérent ontologie sémantique cross-skill (produce-paid-angles v1.10 + produce-copy-brief v1.6 + decompose-angle v1.2 idem refactor)."
  v1.5.0: "v2.63 ontologie pure pain_points + objections collections top-level · HR2 CONTEXTE refactor · `context.pain_point` lookup canonique `pain_points/{PNT-NN}.json` filtered by affected_audiences contains audience_slug (au lieu de profile.problem_map[idx] legacy sub-field). HR5 persist · creative.json#context.pain_point_ref stage PNT-NN canonical (au lieu de pain_extract text legacy seul). Backward compat lecture profile.pain_points[] preserved (pre-v2.63 brands · skip canonical ref, fallback pain text inline). Cohérent ontologie pure cross-skill (produce-paid-angles v1.9 + produce-copy-brief v1.5 + decompose-angle v1.1 idem refactor)."
  v1.4.2: "v2.51 operator-fiche-output canonique template applied · header + gate + footer refactor langage métier. Operator output template (HR6) refactor selon canonique resources/templates/operator-fiche-output.md · header `═══ {BRAND_HUMAIN} · Pub n°{N} ═══` + sous-titre plain language (drop `COMPOSE CREATIVE · CRT-N`). Section 1 / Section 2 / Section 3 réécrites plain language (drop `format: static_image | ratio: 4:5` JSON-style, drop `intent_mix` enum, drop `craft_mode density=0.6`, drop `concept_id: cpt_brand_audience_001`). Bloc `TAGS RETRIEVAL` retiré du template rendu operator (vit backstage dans creative.json pour retrieval programmatique). Footer · 1 reco soft offer 1 ligne max, pas menu. HR3.4 retry wording `compositing externe recommandé v2.35` clean → wording métier. HR-COMPOSITE soft offers wording cohérent canonique sans nommer skills."
  v1.4.1: "v2.50 UX patch · pull-not-push pattern systémique. HR-COMPOSITE decision rule (signal 2 canonical asset disponible) · soft offer au lieu de refuser quand asset manque · operator a 3 choix · (a) drop fichier local, (b) fetch from URL via bridge, (c) fallback full_regen. HR3b Step 3b.2 lookup canonical packshot · idem soft offer 3 options, jamais nommer skill craft-packshot ni layered en surface. HR3b Step 3b.5 multi-layer paste · build créa avec layers disponibles puis surface gap à operator en fin de pipeline avec soft offer 4 options (récupère site / drop fichier / skip cette pub / skip toujours). meta.composite_layers_missing[] log additif. Cohérent feedback operator session 2026-05-13 · jamais forcer user, pull naturel via downstream skill quand asset demandé manque, soft surface 1 ligne max."
  v1.4.0: "v2.48 multi-layer paste extension HR3b Step 3b.5 NEW · packshot + logo + badge en couches ordered pour ads complets branded pixel-exact. composite_layers[] input array · default ['packshot'] (Step 3b.3 standard single-layer) · extensions ['packshot', 'logo'] / ['packshot', 'badge:cert_plantes_naturelles'] / ['packshot', 'logo', 'badge:cert_plantes_naturelles']. Order = z-index render (premier paste = derrière, dernier = devant). Layer defaults · packshot scale 0.65 position center 0.62 shadow enabled · logo scale 0.12 position right 0.92 bottom-right shadow disabled · badge scale 0.10 position left 0.10 top-left shadow disabled. Operator override granular via dict {type, slug, variant, position, scale, shadow}. Multi_layer_composite() PIL function added · loop layers + resolve slot path depuis visual_identity.assets_canonical v1.2 nouveaux slots (logo_canonical + badge_canonical{}) + white-to-alpha threshold + paste ordered + soft shadow conditional. Workflow recommandé · craft-packshot upstream + import-asset logo+badge + compose-creative layered multi-layer. Bridge v2.48 visual_identity schema v1.2 nouveaux slots downstream consumer."
  v1.3.0: "v2.47 layered compositing mode · pattern studio photographer. Nouveau composite_mode input option · full_regen (default historique, nano-banana-2 régénère scène + produit) OR layered (NEW · scène générée séparément sans produit + packshot canon collé pixel-exact via PIL paste + soft drop shadow). HR-COMPOSITE section · decision rule quand layered (fidélité critique sub-label fin / badge plantes / claim · canonical packshot validé _canonical: true present · operator request explicit OR auto-trigger si retry exhausted HR3.4). HR3b pipeline 3 steps · scene-only gen + lookup canonical asset + PIL composite. Résout HR3.4 label_compositing_required flag historiquement orphan (compose-overlay-text v2.43 fait text overlay, pas packshot collage). Cohérent canonical assets pipeline · craft-packshot v1.1 upstream produit l'asset · compose-creative v1.3 layered le consomme downstream. Frontmatter inputs étendu · composite_mode enum."
  v1.2.0: "v2.46 endpoint migration nano-banana-pro/edit (Gemini 2.5 Flash Image legacy) → nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025). Cohérent craft-packshot v1.1 upstream (v2.44 stress test 1 attempt vs 9 échouées endpoint legacy sur silhouette + text fidelity). Frontmatter permissions.external_apis[] déclare provider + endpoint + version_check_url + version_canon_date + replaced_legacy. HR3 step 3 URL swap + meta.endpoint_used log audit trail. Cross-ref doctrine model-versioning-canon v2.44."
  v1.0.2: "v2.36 frictions runtime patch. HR3 step 3 explicit aspect_ratio param (4:5 default Meta feed). HR3.4 adaptive retry policy (max 3 retries scenes complexes vs 2 packshot only) + label_compositing_required flag forward to compose-overlay-text v2.37. HR3.5 post-gen aspect_ratio normalize via PIL crop centre si fal.ai output ratio differe target."
  v1.0.1: "v2.35 alignment. visual_identity path fallback (spec.json#visual_identity OR sibling visual_identity.json with _belongs_to pointer). HR1.4 + HR3.1 patched + consumes paths extended."
description: >
  v1.7.0 (v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés) · Section pré-runtime ajoutée AVANT HR1 detect input mode · expose 6 paramètres décomposés au runtime (brief source · mécanique creative · variants visuels · hook variants OTRB · packshot/asset · hypothèses figées · biais à éviter) avec POURQUOI chacun + close binaire OK ou ajuste. Cross-ref doctrines decomposition-visibility-discipline + engagement-disclosure-discipline v2.79.5+. Backward compat strict additif.
  v1.6.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · context.pain_point reference refactor · lookup `audiences/{audience_slug}/pain_points/{PNT-NN}.json` canonical sub-audience (owned natif par parent path). creative.json stage maintenant ref `context.pain_point_ref: "PNT-NN"` canonical depuis sub-audience. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.5.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · context.pain_point reference refactor · lookup `pain_points/{PNT-NN}.json` canonical (au lieu de profile.pain_points[idx] sub-field legacy). creative.json stage maintenant ref `context.pain_point_ref: "PNT-NN"` canonical. Backward compat lecture profile.pain_points[] legacy preserved (pre-v2.63 brands).
  v1.4.3 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method, pain-benefit-chain, breakthrough-advertising-5-stages). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.4.0 (v2.48) : multi-layer paste extension HR3b Step 3b.5 · composite_layers[] ordered packshot + logo + badge en couches pour ads complets branded pixel-exact.
  v1.3.0 (v2.47) : composite_mode input option · full_regen (default) OR layered (pattern studio photographer · packshot canon collé pixel-exact via PIL paste post-gen scene-only).
  v1.2.0 (v2.46) : endpoint nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025) cohérent craft-packshot v1.1.
  v1.0.1 (v2.35 alignment) : visual_identity path fallback (spec.json#visual_identity OR sibling visual_identity.json).
  v1.0.0 (v2.34 ship production loop). Pendant FORWARD de decompose-ad (qui est REVERSE).
  Génère une créa (visuel via fal.ai nano-banana-2/edit + brief copy markdown S55 fiche v5)
  depuis un brief structuré ancré dans canon × profil audience × angle × brand visual_identity.
  Assemblage compositionnel selon équation v3.1 (NOYAU x CONTEXTE x MODIFIEURS).
  Persiste creative.schema v1.2 + JPG local + brief markdown.
  Inputs supportés : (audience_slug, angle_id, product_slug optional), ou hypothèse from
  scratch ("produit angle pour {brand_slug} post-grossesse" sans angle_id, le skill propose 2-3
  angles depuis profile.json + canon copy).
triggers_fr:
  - "compose une créa"
  - "produis un visuel"
  - "génère une créa pour"
  - "creative pour cette audience"
  - "matérialise l'angle"
triggers_en:
  - "compose a creative"
  - "generate a visual"
  - "produce creative for"
  - "materialize the angle"
disambiguates_against:
  decompose-ad: "decompose-ad fait du REVERSE (analyse ad existante). compose-creative fait du FORWARD (génère depuis brief)."
  produce-paid-angles: "produce-paid-angles produit des ANGLES (stratégie textuelle). compose-creative produit la CRÉA finale (visuel + brief copy)."
  produce-copy-brief: "produce-copy-brief écrit un BRIEF copy. compose-creative orchestre brief + visuel ensemble."
  recompose-creative: "recompose-creative ADAPTE une créa existante (variant). compose-creative produit ex nihilo."
consumes:
  - path: brands/{slug}/angles/{angle_id}.json
    min_version: 1.2.0
    note: angle source (formula Obs+Tension+Reframe+Bridge + lineage canon)
  - path: brands/{slug}/audiences/{audience_slug}/profile.json
    min_version: 1.0.0
    note: 8 dimensions + Schwartz + persona
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
    note: brand_equity_level + creative_zone (curseur copy/visual)
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: "primary path. packshots clean + color_palette + distinctive_features (S55 v2.31 extension)"
  - path: brands/{slug}/products/{product_slug}/visual_identity.json
    min_version: 1.0.0
    note: "fallback path (sibling). Convention legacy or import-product-visuals output. Verifier _belongs_to pointer = product_slug."
  - path: resources/canon/copy/hooks/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/mecaniques/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/archetypes-voix/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/formules-titres/*.json
    min_version: 1.0.0
  - path: resources/templates/creative-formula.md
    min_version: 3.1.0
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
  - path: resources/schemas/creative.schema.json
    min_version: 1.2.0
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/system/output-clarity-doctrine.md
  - path: docs/system/operator-vocabulary-translation.md
produces_validations_for:
  - resources/canon/copy/hooks/*.json
  - resources/canon/copy/mecaniques/*.json
  - resources/canon/copy/archetypes-voix/*.json
produces_proposals_for:
  - brands/{slug}/produced/{CRT-N}.json
  - brands/{slug}/produced/{CRT-N}.jpg
  - brands/{slug}/produced/{CRT-N}.md
prerequisites:
  - field: angles/{angle_id}.json
    level: L1
    auto_pull: read_angle_target
    freshness_ttl_days: 30
  - field: products/{slug}/brief-{angle_id}.md
    level: L1
    auto_pull: read_brief_markdown
    freshness_ttl_days: 30
  - field: products/{slug}/visual_identity
    level: L1
    auto_pull: dual_path_inline_or_sibling
    freshness_ttl_days: 90
  - field: products/{slug}/visual_identity.assets_canonical.{slot}
    level: L2
    note: "v1.3 layered mode prerequisite · lookup canonical packshot path validated_by_operator + _canonical true · si absent, layered impossible et fallback full_regen"
    freshness_ttl_days: 90
  - field: brand.creative_zone
    level: L3
    fallback: proxy_brand_personality
    confidence_default: 0.6
  - field: resources/canon/copy/formats-livrables
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
permissions:
  reads: [brand, product, profile, angle, learning, strategy, canon_copy, registries]
  writes: [creative]
  emits_events: [creative_composed, visual_generated, brief_written, mecanique_proposal_flag]
  external_apis:
    - provider: "fal.ai"
      endpoint: "fal-ai/nano-banana-2/edit"
      model_family: "gemini_3_pro_image_novembre_2025"
      version_check_url: "https://fal.ai/models?keywords=banana"
      version_canon_date: "2025-11"
      replaced_legacy: "fal-ai/nano-banana-pro/edit (v1.0.x · Gemini 2.5 Flash Image)"
      auto_upgrade: false
pipeline:
  preconditions: "angle.json existe avec lineage canon. profile.json 8 dimensions populated. spec.json#visual_identity populated avec primary_front packshot. credentials FAL_API_KEY présent dans credentials_shared.env."
  postconditions: "creative.json conforme creative.schema v1.2 persisté. JPG local persisté dans produced/. brief markdown S55 fiche v5 forward rendu à l'opérateur. Validation silencieuse via validate-resources."
---

# Skill: compose-creative

> **Compose a creative forward.** v1.0.0 · S55 fiche v5 forward · creative.schema v1.2 · équation v3.1 · pendant FORWARD de decompose-ad.

Producer, not decomposer. Lit (angle × audience × brand × product visual_identity × canon copy), applique l'équation compositionnelle v3.1 en mode forward, génère un visuel via fal.ai nano-banana-2/edit (v2.46 canon, Gemini 3 Pro Image), écrit un brief copy markdown S55 fiche v5, persiste un creative.schema v1.2 brand-side. Le mécanisme reste invisible (pas de field paths, pas de scores numériques, pas de noms internes). L'opérateur voit une fiche quatre sections forward, un JPG local, et un bloc tags retrieval.

## Tone

Posture créateur senior + collègue stratège. Pas inspecteur, pas générateur aveugle. La fiche est dense mais lisible : phrases courtes, projection visuelle d'abord (Section 1), pourquoi ça raconte ça (Section 2), diagnostic prédictif honnête (Section 3), tags retrieval. Aucun jargon plumbing, aucun nom de field JSON, aucun acronyme doctrine en surface. Si un slot manque (visual_identity absent, profile incomplet), surface honnête et propose le skill prérequis à run d'abord.

## Expert methodology

**Persona.** Senior creative director qui a composé dix mille créas paid social cross-typologies. Lit un brief comme un copywriter senior lit un canon : isole le NOYAU (mécanique × format × stop_scroller × ton), branche le CONTEXTE (angle × pain_point × persona × proof), applique les MODIFIEURS (intent_mix × audience_segment × craft_mode × overlay_density × brand_mark_present × cta).

**Framework.** Équation compositionnelle v3.1 stress-tested S55. Source canon : `resources/templates/creative-formula.md`. SSOT mécaniques : `resources/registries/creative-mechanics-registry.md`. Free-string `mecanique_id` autorisé.

**Pattern partagé avec decompose-ad.** Mode forward (input = brief stratégique, output = creative). Mode reverse = decompose-ad (input = ad existante, output = fiche). Cohérence cross-skill obligatoire sur fiche v5 layout.

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant assemblage compositionnel (Step 1), scanner prerequisites :

1. L1 silent · `angles/{angle_id}.json` (required) · `products/{slug}/visual_identity` (dual path inline OR sibling, HR1.4 v2.35 formalisé) · `resources/canon/copy/formats-livrables`
2. L1 silent optionnel · `products/{slug}/brief-{angle_id}.md` (si présent, source de truth pour copy)
3. L3 degraded · si `brand.creative_zone` absent → fallback `brand_personality` · confidence 0.6 · flag _gaps

Output state map + confidence_chain[] init.

---

## Engagement disclosure pré-runtime · NIVEAU 0 paramètres décomposés (canon v2.79.5)

Avant HR1 (detect input mode + load pre-requisites), expose ce disclosure NIVEAU 0 à l'opérateur. Pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5. Le but · rendre les paramètres décomposés que ce skill va mobiliser visibles AVANT exécution. Coût compose-creative = appel fal.ai nano-banana-2/edit facturé (token + crédit image gen). Disclosure protège l'opérateur d'un run qui part sur mauvais asset / mauvaise mécanique.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Brief source
     {brief markdown atlas brand `products/{slug}/brief-{angle_id}.md`
     OR angle.json seul (mode hypothèse from scratch)}
     POURQUOI ce brief · {ex "brief copy déjà produit produce-copy-brief
     <24h, source de vérité pour copy"
     OR "pas de brief existant, je compose depuis angle + profile +
     canon copy"}

  2. Mécanique creative
     Sélection depuis `resources/registries/creative-mechanics-registry.md`
     {ex avant-après · démonstration · témoignage UGC · stat-choc ·
     question-callout · contrarian · before-after · split-screen · autre}
     POURQUOI cette mécanique · {ex "audience problem-aware →
     avant-après ancrage somatique" OR "objection 'just marketing'
     → démonstration mécanisme + proof scientifique" OR "stage
     conscience unaware → stat-choc pour briser pattern"}

  3. Variants visuels
     {N variants · default 1 single OR 2-3 si A/B test demandé}
     POURQUOI cette variance · {ex "single ship rapide pour test
     baseline" OR "3 variants croisent hook × mécanique × asset
     pour ladder A/B" OR "operator explicit demand N"}

  4. Hook variants
     OTRB · Observation × Tension × Reframe × Bridge
     {N hooks générés · default 3 hooks variants quality spec ≥4/5}
     POURQUOI ces variants · {ex "hook 1 verbatim exact, hook 2
     verbatim sémantique, hook 3 formula contre-intuitive"}. Structure
     canon angle-anatomy doctrine, pas freestyle.

  5. Packshot/asset
     Source · {visual_identity.assets_canonical.{slot}
     _validated_by_operator: true OR primary_front packshot OR
     fallback full_regen (no canonical asset)}
     POURQUOI cet asset · {ex "packshot canon validé pixel-exact
     mode layered" OR "pas de canonical, full_regen scène complète
     avec produit hallucination accepted" OR "layered + logo + badge
     multi-layer composite pour ad branded complet"}

  6. Hypothèses figées
     Format paid · {Meta vs organic (TikTok / Reels / Stories) ·
     default Meta si stack signals}
     Ratio aspect · {1:1 default Meta feed · 4:5 feed mobile
     optimized · 9:16 Stories/Reels · adapté placement}
     Placement · {feed / story / reel / carousel · inféré stack +
     brand focus + format demandé}

  7. Biais à éviter
     · Over-design (visuel surchargé qui dilue le hook · canon
       v2.51 craft_mode density modérée default)
     · Template visuel répétitif (cluster-deduplication contre
       formats identiques cross-runs)
     · Cliché créa DTC FR (registre "transformation 30 jours",
       "avant-après photoshop évident", "fond blanc isolé sans
       contexte" si audience demande scène-de-vie)

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?
```

ATTENDS confirmation explicite avant de lancer HR1. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set OR si l'opérateur a flag `--no-disclosure` explicit OR si N usages successifs >= seuil expert (`auto_skip_after_n_calls` true). Sinon · disclosure obligatoire canon v2.79.5.

Cross-ref doctrines racine `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5.

---

## HR1 · Detect input mode + load pre-requisites

L'opérateur peut fournir l'input sous trois formes. Detection auto :

| Input shape | Mode | Action |
|---|---|---|
| `(audience_slug, angle_id, product_slug)` explicite | forward_direct | Load tous les pre-requis, pipeline complet |
| `(audience_slug, angle_id)` sans product_slug | forward_direct | Lookup product principal de la marque, pipeline complet |
| `(audience_slug, product_slug)` sans angle_id | hypothesis_from_scratch | Skill propose 2-3 angles depuis profile.json + canon copy avant de composer |

**Composite mode (NEW v1.3) · option orthogonale aux inputs ci-dessus.**

Operator peut ajouter `composite_mode` au input · `full_regen` (default · pipeline HR3 standard) OR `layered` (pipeline HR3b · scène séparée + packshot canon collé PIL). Decision rule détaillée HR-COMPOSITE. Detection signaux ·
- Phrase explicite "studio photographer", "packshot canon", "fidélité critique", "preserve packshot", "mode layered", "composite mode" → `layered`
- Spec.identity.product_category ∈ {supplement, cosmetic, food, pharma} ET visual_identity.assets_canonical.{slot}._validated_by_operator: true → suggest `layered` avec AskUserQuestion gate
- Sinon · `full_regen` default

**Read pre-requisites obligatoires :**

1. `brands/{slug}/angles/{angle_id}.json` (formula + lineage canon).
2. `brands/{slug}/audiences/{audience_slug}/profile.json` (8 dimensions + Schwartz + persona).
3. `brands/{slug}/brand.json` (creative_zone + brand_equity_level + tone_of_voice).
4. `visual_identity` (packshots clean + color_palette + distinctive_features + label.wordmark_text). **Path lookup avec fallback :**
   1. Tenter `brands/{slug}/products/{product_slug}/spec.json#visual_identity` (path canonique inline).
   2. Si absent ou champ manquant, fallback `brands/{slug}/products/{product_slug}/visual_identity.json` (sibling). Verifier `_belongs_to` pointer = `product_slug` avant consume.
   3. Si toujours absent ou les 2 paths donnent des champs vides, surface gracefully + suggest `define-specs` (canon path) ou `import-product-visuals` (futur skill, sibling path).
   4. JAMAIS refuser bloquant si l'un des 2 paths donne quelque chose d'exploitable. Merge logique : sibling override inline si les 2 existent et divergent (sibling = source plus recente par convention import).
5. `resources/canon/copy/*` (hooks, mecaniques, archetypes-voix, formules-titres).
6. `resources/registries/creative-mechanics-registry.md` (SSOT mécaniques).

**Pre-requis manquants gate :**

- `visual_identity` absent ou `packshots.primary_front` null → surface warning, suggest `define-specs` à run d'abord. Refuse de composer (régression label garantie).
- `profile.json` incomplet (moins de 6 dimensions sur 8) → surface warning, suggest `profile-audience` à run d'abord. Continue si l'opérateur insiste mais flag confidence basse.
- `angle.json` absent et mode `hypothesis_from_scratch` → propose 2-3 angles candidats depuis profile.json problem_map + canon copy formules-titres, demande validation avant de composer.
- `FAL_API_KEY` absent → surface honnête, refuse de composer, suggest connect-source pour configurer la credential.

---

## HR2 · Apply équation v3.1 compositionnelle

Assembler creative.schema v1.2 selon NOYAU × CONTEXTE × MODIFIEURS.

**NOYAU (invariant créa) :**

- `mecanique` : choisir parmi `creative-mechanics-registry` SSOT en cohérence avec `angle.formula` + `profile.market_context`. Free-string `mecanique_id` autorisé. Si aucune mécanique ne fitte → `other` + flag `mecanique_proposal` (HR7).
- `format` : default `static_image` ratio 4:5 (Meta feed) sauf override opérateur (`carousel`, `video_short`, `reel`, `story`).
- `stop_scroller` :
  - `hook_layer` (verbal) pulled depuis `angle.formula.observation` summary, formulé en 1 phrase courte.
  - `visual_layer` (description scène) depuis `angle.formula.tension` + `audience.problem_map`, descriptif visuel objectif.
- `ton` : depuis `brand.tone_of_voice` + `audience.identity_signals`, croisé.

**CONTEXTE (couches stratégiques branchables) :**

- `angle_ref` : `angle_id` source (lineage canon préservé).
- `pain_point` (v1.6.0 ontologie sémantique pure) : lookup `audiences/{audience_slug}/pain_points/{PNT-NN}.json` canonical sub-audience (owned natif par parent path · NEW v2.64). Stage `context.pain_point_ref: "PNT-NN"` canonical dans creative.json downstream HR5. Si angle.lineage.pain_ref déjà populé (produce-paid-angles v1.10+), priorité absolue à ce ref canonique. Sinon, pick top pain entity par severity desc sur l'audience. Backward compat (v2.63 brands) · si sub-audience vide, fallback top-level `pain_points/{PNT-NN}.json` v2.63 filtered by `affected_audiences[]` contains `{audience_slug}`. Fallback v1.7 · si top-level vide aussi, fallback `profile.json#problem_map` ou `profile.json#pain_points[]` sub-field legacy · stage `context.pain_point_ref: null` + `context.pain_point_text: "{verbatim from legacy}"` inline.
- `persona` : depuis `profile` (type + buyer_user_split snapshot cache).
- `proof` : depuis `spec.problems_solved` + `audience.benefit_stack`.

**MODIFIEURS (override situationnels) :**

- `intent_mix` (multi-weighted) : depuis `brand.creative_zone` + `angle.intent` fallback. Si pure (`primary` 100%), skip `weights`. Si mélange (ex 60% DR + 40% Brand), encoder explicitement (`weights: {DR: 0.6, Brand: 0.4}`, somme à 1.0 ± 0.05).
- `audience_segment` : depuis `profile` (B2C default).
- `craft_mode + overlay_density + brand_mark_present` : depuis `brand.creative_zone` curseur.
  - `overlay_density` (0.0-1.0) : 0.0 photo produit pure, 0.1-0.3 minimal mark, 0.4-0.7 hook + claim layered, 0.8-1.0 verbal-dominated.
  - `brand_mark_present` (bool) : logo/wordmark visible, orthogonal à overlay_density.
  - `craft_mode` legacy mirror : `product_only` si density=0 et brand_mark_present=false ; `minimal_brand_mark` si density<0.3 et brand_mark_present=true ; `with_overlay` si density>=0.4.
- `cta` : modalité explicite depuis `angle.formula.bridge.promise` + `offer.json` si applicable.

---

## HR3 · Génération visuelle via fal.ai nano-banana-2/edit

Endpoint canon · `fal-ai/nano-banana-2/edit` (Gemini 3 Pro Image · canon novembre 2025 · supérieur vs `nano-banana-pro/edit` legacy Gemini 2.5 Flash Image qui régressait silhouette OR text fidelity). Cohérent craft-packshot v1.1 upstream qui valide ce pattern (S55 v2.44 stress test · 1 attempt vs 9 échouées endpoint legacy). Doctrine sœur · `docs/system/model-versioning-canon.md`.

Pipeline image gen :

1. Récupère packshot clean URL depuis `visual_identity.packshots.primary_front`. **Path lookup avec fallback :**
   1. Tenter `brands/{slug}/products/{product_slug}/spec.json#visual_identity.packshots.primary_front`.
   2. Si absent, fallback `brands/{slug}/products/{product_slug}/visual_identity.json#packshots.primary_front` (sibling, verifier `_belongs_to` pointer).
   3. Si les 2 paths absents ou null, refuse de composer (regression label garantie cf HR1.4).
2. Construis prompt structuré :
   - Référence DNA visuel angle (mécanique narrative + scène depuis HR2 NOYAU).
   - Hard constraints `visual_identity` (non-négo) :
     - Container : `{container.shape} {container.material} {container.cap_type}, {container.transparency}`.
     - Content : `{content.quantity_visible} {content.form} color {content.color_hex} {content.shape}`.
     - Label : `MUST read exactly '{label.wordmark_text}'. Sub-label: '{label.sub_label}'. Duration: '{label.duration_indicator}'.`.
     - Color palette : `container {color_palette.container_primary}, label background {color_palette.label_background}, label text {color_palette.label_text}.`.
     - Distinctive features : `MUST PRESERVE: {distinctive_features[0]}. {distinctive_features[1]}. ...`.
   - Atmosphère depuis `brand.creative_zone` + `audience.identity_signals`.
   - Format `4:5 vertical Meta feed` default.
3. POST `https://fal.run/fal-ai/nano-banana-2/edit` (endpoint canon v2.46, **PAS** `nano-banana-pro/edit` legacy v1.0.x ni `nano-banana/edit` v0 qui ignore aspect_ratio) avec payload :
   - `image_urls=[packshot_url]`
   - `prompt=<above>`
   - `aspect_ratio="4:5"` (default Meta feed, override possible via input opérateur). Enum supportée par endpoint : `auto, 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16`.
   - `output_format="jpeg"`, `resolution="1K"` (default Meta feed, override `2K` si haute fidélité requise).
   - Auth header `Authorization: Key ${FAL_API_KEY}`.
4. Download résultat dans `/tmp/compose-creative/{brand}-{crt_id}.jpg`.
5. Move final vers `brands/{brand}/produced/{CRT-N}.jpg`.

**Retry logic label preservation :**

- Si gen retourne visuel avec label régressé (wordmark différent du `label.wordmark_text`), retry max 2 fois avec prompt renforcé `"PRESERVE EXACTLY label artwork from reference image. Wordmark text MUST be '{label.wordmark_text}' character-for-character. NO variants, NO substitutions."`.
- Si toujours régressé après 3 iter total, flag warning à l'opérateur en langage métier (cf HR3.4 soft offer) + persiste avec note technique backstage `meta.label_compositing_required: true`.

**QC post-gen :**

- Valider chaque `distinctive_features[]` présent dans le render (lecture image + cross-check description).
- Valider color_palette dominantes match (hex tolérance ±15%).
- Échec sur 1+ feature → flag à l'opérateur + propose re-gen avec prompt renforcé.

---

## HR3.4 · Adaptive retry policy (v1.0.2)

Calibrer `max_retry` selon complexité scène détectée à partir du prompt assemblé en HR3 :

- **Scène simple** (packshot studio uniquement, pas de model, pas de scene context, pas de props multiples) → `max_retry = 2` (default historique).
- **Scène complexe** (model + props multiples OU scene context narratif OU 2+ couches sub-label/duration_indicator/distinctive_features à préserver) → `max_retry = 3`.

**Sub-label / duration_indicator regression handling :**

Après les retries autorisés, si le wordmark principal (`label.wordmark_text`) est préservé MAIS le sub-label (`label.sub_label`) ou duration indicator (`label.duration_indicator`) reste flou ou illisible :
1. NE PAS continuer à retry (gain marginal, brûle budget API).
2. **v1.3+ auto-trigger layered mode si canonical asset disponible** · check `visual_identity.assets_canonical.{slot}._validated_by_operator: true` · si oui, redéclencher pipeline en `composite_mode: layered` (HR3b) plutôt que persister régression. Solution canonique au problème historique.
3. Si pas de canonical asset · persister la créa avec wordmark préservé + set `meta.label_compositing_required: true` dans `creative.json`.
4. Note dans brief markdown S55 fiche v5 (Section 1, ligne Branding), langage métier · *"Petit texte sous le logo flou sur le packshot. Si on canonise une fois la photo produit officielle, ça sera net sur toutes les pubs suivantes."*
5. Flag explicite opérateur reco no-orphan, langage métier, soft offer · *"Logo principal préservé, mais le petit texte sous le logo est flou. Si tu veux, on peut canoniser le packshot une fois et le réutiliser sur toutes tes pubs (net garanti)."*

**Anti-pattern UX prose** · JAMAIS nommer `craft-packshot`, `compose-overlay-text`, `mode layered`, `HR3b`, `compositing` en surface operator. Soft offer + langage métier · "canoniser la photo produit", "réutiliser sur toutes tes pubs", "net garanti".

**Note v2.43+ scope shipped :** `compose-overlay-text` v2.43 fait le compositing PIL text overlay post-gen (sub-label, duration indicator, optional CTA badge). v2.47 ajoute layered mode HR3b in-skill · packshot collage pixel-exact upstream du text overlay (canonical asset + scène séparée). Deux outils complémentaires · layered = packshot, overlay-text = text crisp.

---

## HR3.5 · Post-gen aspect ratio normalize (v1.0.2)

Defensive primitive : même si HR3 step 3 passe `aspect_ratio` explicite, certains endpoints fal.ai (cas où l'opérateur override sur `nano-banana/edit` v0 sans suffixe, ou fallback API-side) peuvent retourner un ratio différent de la target.

**Procédure post-download :**

1. Lire dimensions image téléchargée (`/tmp/compose-creative/{brand}-{crt_id}.jpg`) via PIL.
2. Calculer ratio actuel `current_ratio = width / height`.
3. Calculer ratio target depuis param `aspect_ratio` envoyé en HR3 step 3 (ex `4:5` → `0.8`).
4. Si écart `|current_ratio - target_ratio| > 0.02` :
   - Crop centré via `PIL.Image.crop()` pour atteindre exactement le ratio target.
   - Préserver hauteur ou largeur selon laquelle dimension contraint (crop la plus large).
   - Sauvegarder over le fichier d'origine.
   - Note dans brief markdown S55 fiche v5 (Section 1, ligne Visuel généré) : *"auto-cropped {current_ratio} → {target_ratio} post-gen"*.
5. Si écart ≤ 0.02 → no-op, ratio déjà correct.

**Pas de retry fal.ai sur mismatch ratio.** Crop PIL est déterministe et instantané, retry fal.ai = gain marginal + coût API.

**Dépendance :** Python PIL (Pillow). Si absent dans l'env runtime, surface honnête à l'opérateur + persiste sans crop avec note `aspect_ratio_mismatch_unresolved` dans `meta`.

---

## HR-COMPOSITE · Mode selection full_regen vs layered (NEW v1.3)

Deux modes pour le pipeline visuel · `full_regen` (default historique HR3) régénère scène ET produit dans un seul call nano-banana-2. `layered` (NEW v1.3 · pattern studio photographer) sépare en 2 phases · scène générée sans produit + packshot canon collé pixel-exact via PIL paste.

**Decision rule.** Choisir `layered` si :

1. **Operator request explicite** · input contient `composite_mode: layered` OR phrase "studio photographer", "packshot canon", "fidélité critique", "preserve packshot".
2. **Canonical asset disponible** · `visual_identity.assets_canonical.{slot}._validated_by_operator: true` AND `_canonical: true` AND path file exists. Sans canonical asset → soft offer pull-not-push pattern (v2.50 NEW) · *"Pour faire ça en mode photo studio (packshot pixel-exact), j'aurais besoin d'une photo officielle du produit. Si tu en as une, drop-la. Si tu veux que je la prépare depuis ton site, dis-moi. Sinon je génère en mode classique (le produit peut bouger légèrement)."*. Operator décide · drop fichier OR fetch from URL OR fallback full_regen. Pas de "run craft-packshot d'abord" en surface (jargon skill name).
3. **Fidélité critique flag** · spec.identity.product_category ∈ {supplement, cosmetic, food, pharma} avec sub-label fin / badge plantes / claim certification / composition list visible. Ces produits = text fidelity blocker.
4. **Auto-trigger retry exhausted** · HR3.4 retry policy a flag `label_compositing_required: true` après 3 iter sur full_regen. Au lieu de surfacer opérateur "compositing externe recommandé" comme v1.2, v1.3 auto-trigger `layered` sur retry si canonical asset disponible (transparent fallback).

Choisir `full_regen` si :

1. Pas de canonical asset (craft-packshot pas encore run sur ce produit).
2. Scène narrative complexe avec produit en main de model OR en interaction physique (layered casse l'illusion · packshot collé ne tient pas dans une main convaincante).
3. Operator preference declared `composite_mode: full_regen`.

**Trade-off.** `layered` garantit packshot pixel-exact (substrat canonisé craft-packshot) MAIS scène autour générée sans produit peut sembler artificielle si la composition exigerait interaction (main qui tient, table contact réaliste, etc.). `full_regen` garantit cohérence visuelle scène-produit MAIS risque drift label (notre problème historique). Choisir selon priorité brand · text fidelity blocker → layered, narrative cohérence → full_regen.

**No false binary.** `layered` n'est pas "meilleur que" `full_regen` · c'est une alternative selon contexte produit. Pour packshot studio simple (90% des paid social Meta feed e-com), `layered` gagne. Pour lifestyle UGC narratif, `full_regen` gagne.

---

## HR3b · Pipeline layered compositing (NEW v1.3)

Activer si HR-COMPOSITE décide `composite_mode: layered`. Sinon skip et utiliser HR3 standard.

### Step 3b.1 · Génération scène-only via nano-banana-2

Prompt explicit "no product" pour générer background scène sans le produit ·

```
Empty professional photoshoot studio scene, soft lighting from the left,
{brand.atmosphere or audience.identity_signals depuis HR2 NOYAU},
clean composition with negative space center-bottom for product placement,
{angle.formula.tension surface en background context},
NO product, NO bottle, NO container, NO label, NO text overlay.
Format 4:5 vertical Meta feed.
```

Override aspect_ratio + resolution depuis input opérateur ou défauts HR3 step 3.

POST `https://fal.run/fal-ai/nano-banana-2/edit` MAIS sans `image_urls[]` (pure generation, pas edit) OR avec `image_urls=[]` ET prompt no-product explicite. Si endpoint refuse empty image_urls, fallback `nano-banana-2/text-to-image` (non-edit variant) si dispo, ELSE pass un mood reference scène vide pertinent.

Download résultat dans `/tmp/compose-creative/{brand}-{crt_id}-scene.jpg`.

### Step 3b.2 · Lookup canonical packshot path

1. Read `brands/{slug}/products/{product_slug}/visual_identity.json#assets_canonical.{slot}` (slot default `front`).
2. Verify `_validated_by_operator: true` AND `_canonical: true` AND `path` exists on filesystem.
3. Si absent ou flag false → **soft offer pull-not-push (v2.50)** au lieu de refuser. Langage métier, jamais nommer le skill ·

   > *"Pour faire la pub en photo studio (produit pixel-exact), il me faut une photo officielle du {product_name}. Trois options ·*
   > *(a) Tu as un fichier en local ? Drop-le.*
   > *(b) Je peux la récupérer depuis ton site et la préparer (1-2 min).*
   > *(c) Je génère en mode classique (le produit peut bouger légèrement vs photo officielle)."*

   Operator décide. Skill chain l'option choisie. Jamais bloquant.

   **Bridge code (v2.51 NEW · câblage explicite Task tool params)** ·

   Selon la réponse operator, l'agent invoke concrètement ·

   - **Option (a) drop fichier local** · operator drop path absolu d'un fichier image. Skill consume direct ·
     ```
     Lecture du fichier path operator + verify format (png/webp/jpg) + verify resolution (min 2048x2048 recommandé).
     Persist via Edit/Write dans visual_identity.json#assets_canonical.packshot_front avec _validated_by_operator: true uniquement APRÈS gate explicit operator validation Step 5 craft-packshot symétrique.
     Si quality assessment 8 critères < 6/8 pass · surface warning operator + propose re-upload.
     ```

   - **Option (b) récupère depuis ton site** · invoke `craft-packshot` skill via Task tool · params concrets ·
     ```
     Task tool invocation ·
     - description · "Génère packshot canonique {product_humain}"
     - subagent_type · "general-purpose" (le skill craft-packshot recommended_model: sonnet, subagent_safe: true)
     - prompt · "Run craft-packshot pour {brand_slug}/{product_slug}. Mode scrape_from_official_site. Brand URL · {brand.identity.website}. Aspect ratio · 1:1. Resolution · 2K. Output path canonique · brands/{brand_slug}/products/{product_slug}/assets/packshot-canonical-front-{date}-gen-v1.png. Skill flow standard 7 steps · scrape carousel → score → pick source → compose prompt → fal.ai nano-banana-2/edit → quality 8 critères → operator gate Step 5 → persist visual_identity.json. Return absolute path canonical asset post-validation."
     ```
     Wait completion. Re-read `visual_identity.json#assets_canonical.packshot_front` post-completion. Si `_validated_by_operator: true` AND path file exists · continue pipeline Step 3b.3 layered composite. Si operator a rejected dans craft-packshot Step 5 gate · fallback option (c).

   - **Option (c) génère en mode classique** · fallback `composite_mode: full_regen` · skip HR3b layered, route vers HR3 standard pipeline.

5. Path absolu canonical asset · `brands/{slug}/products/{product_slug}/{path}` (relative dans visual_identity.json).

### Step 3b.3 · PIL composite paste + soft drop shadow

```python
from PIL import Image, ImageFilter
import os

def layered_composite(
    scene_path,
    packshot_path,
    output_path,
    scale_factor=0.65,
    position=("center", 0.62),
    shadow_offset=(0, 20),
    shadow_blur=35,
    shadow_opacity=0.35
):
    """
    scene_path · jpg scene-only (Step 3b.1 output)
    packshot_path · png canonical packshot (Step 3b.2 lookup)
    scale_factor · packshot height / scene height (0.0-1.0, default 0.65)
    position · (horizontal, vertical_pct) · horizontal ∈ {center, left, right} ou int px, vertical_pct ∈ 0.0-1.0
    shadow_offset · (dx, dy) px shadow displacement
    shadow_blur · gaussian blur radius shadow
    shadow_opacity · 0.0-1.0 shadow alpha
    """
    scene = Image.open(scene_path).convert("RGBA")
    packshot = Image.open(packshot_path).convert("RGBA")

    # Threshold white background to alpha if packshot has white bg (canonical asset convention)
    if packshot.mode == "RGBA":
        data = packshot.getdata()
        new_data = []
        for px in data:
            r, g, b, a = px
            if r > 245 and g > 245 and b > 245:
                new_data.append((r, g, b, 0))
            else:
                new_data.append((r, g, b, a))
        packshot.putdata(new_data)

    # Resize packshot to target height
    target_height = int(scene.size[1] * scale_factor)
    aspect = packshot.size[0] / packshot.size[1]
    target_width = int(target_height * aspect)
    packshot_resized = packshot.resize((target_width, target_height), Image.LANCZOS)

    # Position
    horizontal, vertical_pct = position
    if horizontal == "center":
        x = (scene.size[0] - target_width) // 2
    elif horizontal == "left":
        x = int(scene.size[0] * 0.15)
    elif horizontal == "right":
        x = int(scene.size[0] * 0.85) - target_width
    else:
        x = int(horizontal)
    y = int(scene.size[1] * vertical_pct) - target_height // 2

    # Generate soft drop shadow
    shadow = Image.new("RGBA", scene.size, (0, 0, 0, 0))
    shadow_mask = packshot_resized.split()[3] if packshot_resized.mode == "RGBA" else None
    if shadow_mask:
        shadow_layer = Image.new("RGBA", packshot_resized.size, (0, 0, 0, int(255 * shadow_opacity)))
        shadow.paste(shadow_layer, (x + shadow_offset[0], y + shadow_offset[1]), shadow_mask)
        shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))

    # Composite · scene + shadow + packshot
    composite = Image.alpha_composite(scene, shadow)
    composite.paste(packshot_resized, (x, y), packshot_resized)

    # Convert RGBA → RGB for jpeg save
    composite_rgb = Image.new("RGB", composite.size, (255, 255, 255))
    composite_rgb.paste(composite, mask=composite.split()[3] if composite.mode == "RGBA" else None)
    composite_rgb.save(output_path, "JPEG", quality=92)

    return output_path
```

Defaults tuning ·
- `scale_factor: 0.65` · packshot occupe 65% hauteur scène, laisse air respiration top
- `position: ("center", 0.62)` · centré horizontalement, légèrement bas (règle des tiers)
- `shadow_offset: (0, 20)` · ombre légère décalée bas
- `shadow_blur: 35` · doux, pas hard edge
- `shadow_opacity: 0.35` · subtle, pas dramatique

Override possibles via operator input ou angle.formula.observation context (ex angle "produit en main" → layered probablement pas optimal, fallback HR3 full_regen).

### Step 3b.4 · Output composite

Save final composite dans `/tmp/compose-creative/{brand}-{crt_id}.jpg` (replace scene-only temp file). Path final downstream HR3 step 5 standard (move vers `brands/{brand}/produced/{CRT-N}.jpg`).

Note dans `meta` ·
- `composite_mode: "layered"`
- `composite_scene_endpoint: "fal-ai/nano-banana-2/edit"`
- `composite_canonical_asset_path: <relative path>`
- `composite_canonical_asset_validated_at: <date depuis visual_identity.json>`
- `composite_params: {scale_factor, position, shadow_offset, shadow_blur, shadow_opacity}`

**Avantage layered.** Text fidelity 100% (packshot canonisé craft-packshot · 8/8 quality check pass déjà validé opérateur). Pas de retry budget burned sur label preservation. Pipeline déterministe sur produit · stochastique uniquement sur scène.

**Limite layered.** Composition narrative limitée · packshot ne peut pas tenir convaincante dans main de model OU être en interaction physique réaliste avec props scène. Pour ces cas, fallback HR3 full_regen.

### Step 3b.5 · Multi-layer paste optional (NEW v1.4 · packshot + logo + badge)

Si `visual_identity.assets_canonical` contient aussi `logo_canonical._validated_by_operator: true` AND/OR `badge_canonical.{slug}._validated_by_operator: true`, layered mode supporte multi-layer paste pour ad complet branded pixel-exact.

**Input opérateur** · `composite_layers[]` array ordered, default `["packshot"]` (Step 3b.3 standard single-layer). Extensions ·
- `["packshot", "logo"]` · packshot center-bottom + logo bottom-right
- `["packshot", "badge:cert_plantes_naturelles"]` · packshot + badge top-left
- `["packshot", "logo", "badge:cert_plantes_naturelles"]` · les 3 ensembles
- Order = z-index render (premier paste = derrière, dernier = devant)

**Layer config defaults** ·

| Layer | Slot lookup | Default position | Default scale | Shadow |
|---|---|---|---|---|
| `packshot` | assets_canonical.packshot_front | (center, 0.62) | 0.65 (% scene height) | enabled (offset 0,20 · blur 35 · opacity 0.35) |
| `logo` | assets_canonical.logo_canonical | (right, 0.92) bottom-right | 0.12 | disabled (logos = no shadow typiquement) |
| `badge:{slug}` | assets_canonical.badge_canonical.{slug} | (left, 0.10) top-left | 0.10 | disabled |

Operator peut override chaque param via input dict ·
```
composite_layers: [
  {"type": "packshot", "scale": 0.7},
  {"type": "logo", "variant": "monochrome_white", "position": ["right", 0.95]},
  {"type": "badge", "slug": "cert_plantes_naturelles", "position": ["left", 0.08], "scale": 0.12}
]
```

**Extension PIL code** ·

```python
def multi_layer_composite(
    scene_path,
    layers_config,
    output_path,
    visual_identity_assets_canonical
):
    """
    scene_path · jpg scene-only output Step 3b.1
    layers_config · array ordered de {type, slug, variant, position, scale, shadow}
    visual_identity_assets_canonical · dict des assets canonical lus depuis visual_identity.json
    """
    scene = Image.open(scene_path).convert("RGBA")
    composite = scene.copy()

    for layer in layers_config:
        layer_type = layer["type"]

        # Resolve slot path
        if layer_type == "packshot":
            slot = visual_identity_assets_canonical.get("packshot_front", {})
            asset_path = slot.get("path")
        elif layer_type == "logo":
            slot = visual_identity_assets_canonical.get("logo_canonical", {})
            variant_name = layer.get("variant", "primary")
            asset_path = next(
                (v["path"] for v in slot.get("variants", []) if v["name"] == variant_name),
                slot.get("path")
            )
        elif layer_type == "badge":
            badges = visual_identity_assets_canonical.get("badge_canonical", {})
            slug = layer["slug"]
            slot = badges.get(slug, {})
            asset_path = slot.get("path")
        else:
            continue  # unknown layer type skipped

        if not asset_path:
            # Slot empty · soft offer pull-not-push pattern v2.50
            # Avant skip silencieux v1.4, maintenant v1.4.1+ surface gap à operator
            # avec offer fetch from URL OR drop OR skip
            missing_layers.append({
                "type": layer_type,
                "slug": layer.get("slug"),
                "variant": layer.get("variant"),
                "humain_label": _humain_label_from_layer(layer_type, layer)
            })
            continue  # skip ce layer pour l'instant, on surface après tous les layers

        # Load + apply white→alpha threshold (canonical asset convention)
        asset = Image.open(asset_path).convert("RGBA")
        if slot.get("background") == "white":
            data = asset.getdata()
            new_data = [(r, g, b, 0) if (r > 245 and g > 245 and b > 245) else (r, g, b, a) for r, g, b, a in data]
            asset.putdata(new_data)

        # Resolve params (operator override > defaults per layer type)
        defaults = {
            "packshot": {"scale": 0.65, "position": ["center", 0.62], "shadow": True},
            "logo": {"scale": 0.12, "position": ["right", 0.92], "shadow": False},
            "badge": {"scale": 0.10, "position": ["left", 0.10], "shadow": False}
        }
        cfg = {**defaults[layer_type], **layer}

        # Resize
        target_height = int(scene.size[1] * cfg["scale"])
        aspect = asset.size[0] / asset.size[1]
        target_width = int(target_height * aspect)
        asset_resized = asset.resize((target_width, target_height), Image.LANCZOS)

        # Position
        horizontal, vertical_pct = cfg["position"]
        if horizontal == "center":
            x = (scene.size[0] - target_width) // 2
        elif horizontal == "left":
            x = int(scene.size[0] * 0.05)
        elif horizontal == "right":
            x = int(scene.size[0] * 0.95) - target_width
        else:
            x = int(horizontal)
        y = int(scene.size[1] * vertical_pct) - target_height // 2

        # Shadow if enabled
        if cfg["shadow"]:
            shadow_layer = Image.new("RGBA", asset_resized.size, (0, 0, 0, int(255 * 0.35)))
            shadow_canvas = Image.new("RGBA", scene.size, (0, 0, 0, 0))
            shadow_canvas.paste(shadow_layer, (x, y + 20), asset_resized.split()[3])
            shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(35))
            composite = Image.alpha_composite(composite, shadow_canvas)

        # Paste layer
        composite.paste(asset_resized, (x, y), asset_resized)

    # Convert RGBA → RGB for jpeg save
    composite_rgb = Image.new("RGB", composite.size, (255, 255, 255))
    composite_rgb.paste(composite, mask=composite.split()[3] if composite.mode == "RGBA" else None)
    composite_rgb.save(output_path, "JPEG", quality=92)

    return output_path
```

**Missing layers handling (v2.50 NEW · soft offer pull-not-push)** ·

Si `multi_layer_composite()` rencontre un layer dont le slot canonique est vide (ex operator demande `composite_layers: ['packshot', 'logo', 'badge:cert_plantes_naturelles']` mais `logo_canonical` empty), v1.4.1+ pattern · build la créa avec les layers disponibles, puis surface gap à operator avec soft offer en fin de pipeline ·

> *"Pub générée avec ton packshot. J'ai pas trouvé ton logo brand ni le badge "cert plantes naturelles" en version officielle. Si tu veux, je peux les récupérer depuis ton site (1-2 min) pour les ajouter cette pub et toutes les suivantes."*

Operator décide ·
- (a) **Récupère depuis le site** · skill chain l'import des assets manquants puis re-compose
- (b) **Drop fichier(s) local** · skill consume immédiatement et re-compose
- (c) **Skip pour cette pub** · la créa actuelle est OK comme ça
- (d) **Skip pour toujours** · ces layers ne sont pas pertinents pour cette brand (flag opérateur preference, plus de relance)

Pas blocking. Pas refuser. Pas push. Soft offer 1 fois, operator passe à autre chose si pas pertinent. Jamais nommer les skills (import-asset / extract_from_url) en surface.

**Bridge code (v2.51 NEW · câblage explicite Task tool params)** ·

Selon réponse operator, l'agent invoke concrètement ·

- **Option (a) Récupère depuis le site** · pour chaque layer manquant dans `composite_layers_missing[]`, invoke `import-asset` skill via Task tool · params concrets ·
  ```
  Task tool invocation par layer manquant ·
  - description · "Récupère {label_humain_layer} depuis site brand"
  - subagent_type · "general-purpose" (import-asset recommended_model: sonnet, subagent_safe: true)
  - prompt · "Run import-asset Mode C extract_from_url pour {brand_slug}. Brand URL · {brand.identity.website}. Asset type · {layer.type} (logo OU badge selon layer demandé). Pour badge · slug {layer.slug} (ex cert_plantes_naturelles). Mode C workflow standard 4 sub-steps (C.1 scrape HTML, C.2 extract candidats heuristics par type, C.3 download + rasterize SVG fallback chain, C.4 operator gate validation). Return path canonical asset post-validation."
  ```
  Wait completion par layer. Re-read `visual_identity.json#assets_canonical.{slot}` post-completion. Si peuplé + validé · re-trigger `multi_layer_composite()` pour re-compose la pub avec les layers maintenant disponibles. Si operator rejected dans import-asset HR4 gate · skip ce layer pour cette pub (l'overlay sera incomplet pour cette créa, OK).

- **Option (b) Drop fichier(s) local** · pour chaque layer manquant, AskUserQuestion path absolu fichier. Pour chaque fichier dropé, invoke `import-asset` Mode A direct · ·
  ```
  Task tool ·
  - prompt · "Run import-asset Mode A operator_drop_local_path pour {brand_slug}. Asset type · {layer.type}. Slug si applicable · {layer.slug}. File path · {operator_drop_path}. Quality assessment 5 critères + operator gate HR4."
  ```
  Wait completion. Re-trigger multi_layer_composite() avec layers maintenant peuplés.

- **Option (c) Skip pour cette pub** · finalize la créa actuelle telle quelle (build sans layers manquants). Meta `composite_layers_missing[]` log pour audit. No re-compose.

- **Option (d) Skip pour toujours** · flag dans `brands/{slug}/brand.json#preferences.composite_layers_skip` array avec entries `{type, slug}`. Future invocations compose-creative layered ne re-proposent plus ces layers pour cette brand. Finalize créa actuelle. Cohérent operator decision · pas tous les brands ont logo/badge pertinents.

Pas de "run import-asset Mode C" en surface operator. Le bridge code ci-dessus est instruction agent-facing pour câblage runtime, jamais leak operator.

**Meta logged additif** ·
- `composite_layers: [...]` (array ordered des layers appliqués avec params résolus)
- `composite_layers_assets_paths: [...]` (paths absolus pour audit)
- `composite_layers_missing: [...]` (array layers demandés mais slot vide, surface à operator v2.50+)

**Workflow recommandé v2.48** ·
1. `craft-packshot` upstream → canonical packshot validé
2. `import-asset` pour logo + badge cert plantes
3. `compose-creative composite_mode: layered composite_layers: [packshot, logo, badge:cert_plantes_naturelles]` → ad complet pixel-exact branded

Avantage multi-layer · pubs avec branding complet (packshot + logo + badge cert) tous pixel-exact, réutilisation cross-pubs sans regen. Limite · si scene a composition complexe (model holding produit), packshot collé tient pas. Fallback `composite_mode: full_regen` pour ces cas (mais perd fidélité branding).

---

## HR4 · Génération brief markdown S55 fiche v5 forward

Format opérateur-facing structuré (équivalent decompose-ad output, mode forward).

**Section 1 · CE QUE LA CRÉA VA MONTRER** (projection visuelle objective)

| Champ | Contenu |
|---|---|
| Format | `static_image | carousel | video_short | reel | story` + ratio + langue |
| Hook visuel | Description scène depuis HR2 NOYAU stop_scroller.visual_layer |
| Hook texte | Verbatim généré, max 8 mots, formule depuis canon hooks |
| Body | Description body description (si présent) |
| CTA texte | Verbatim button label + texte autour |
| Branding | Logo position, packshot oui/non, couleur dominante (hex), font signal |
| Visuel généré | Path local `/tmp/compose-creative/{...}.jpg` → `produced/{CRT-N}.jpg` |

**Section 2 · CE QUE LA CRÉA RACONTE** (intention stratégique)

| Champ | Contenu |
|---|---|
| Cible | Phrase plain language depuis profile (persona type + buyer_user_split) |
| Niveau conscience | Schwartz double-stage (entrée + sortie visée) |
| Vérité non-dite | Insight depuis angle.formula.observation+tension, modalité formulee/implicite/absente |
| Angle d'attaque | Levier × positionnement-contre × promesse depuis angle.formula synthèse |
| Mécanique | Nom registry + 1 phrase explicative |
| Pivot du concept | Atome irréductible entre guillemets + 1 phrase justification |

**Section 3 · DIAGNOSTIC PRÉDICTIF**

- Cohérence chaîne : audience → insight → angle → mécanique → craft. Chaque transition `tient | tension | casse`. Verdict global + 1 phrase.
- Score arrêt-scroll prédit : 1-5, ancré sur observables Section 1 (densité visuelle, contraste feed, rupture pattern, charge cognitive, signature ton).
- Forces : 3-5 bullets observables (pas d'éloge vague, nommer le mécanisme).
- Risques : 3-5 bullets (légal, brand, audience, execution).

**Section TAGS RETRIEVAL** : tous les axes du schema, snake_case strict.

---

## HR5 · Persist creative.json + JPG + markdown

Conforme creative.schema v1.2 :

- `_schema_version: "creative/1.2"`.
- `_equation_ref` const v3.1.
- `intent_mix` (multi-weighted depuis HR2). Champ legacy `intent` mirror backward-compat.
- `execution.overlay_density` (0.0-1.0 numérique) + `execution.brand_mark_present` (bool). Champ legacy `craft_mode` mirror dérivé.
- `meta.validation_status` (object composite) : `{status: "hypothesis", confidence: 0.5, confidence_source: "default"}` (créa pas encore testée en prod).
- `meta.test_results[]` empty (sera populé après campagne live).
- `performance.longevity_signal` vide (pas encore en prod).
- `tags.source: "internal_production"`.
- `tags.concept_id` : nouveau `cpt_{brand_slug}_{angle_short}_{NNN}` ou `variant_of: {parent_concept_id}` si dérivé.

**Mutation gate :**

1. Generate `creative_id`. Pattern `CRT-NN`. Lookup max existing ID dans `brands/{slug}/produced/`, increment.
2. Write via `write_to_context(field_path, value, source, confidence, mode="proposed")`. **NEVER edit JSON directly via Edit/Write/NotebookEdit.**
3. Persist JPG : move `/tmp/compose-creative/{brand}-{crt_id}.jpg` → `brands/{brand}/produced/{CRT-N}.jpg`.
4. Write brief markdown : `brands/{brand}/produced/{CRT-N}.md` (format S55 fiche v5 forward).
5. Si `mecanique_id == "other"` → emit event `mecanique_proposal_flag` avec payload `{observed_mecanique_signature, ad_creative_id, registry_gap_description}`.
6. Trigger `validate-resources` silencieusement post-write. Flag MAJOR/CRITICAL à l'opérateur si remonte.

---

## HR6 · Output operator-facing

Render fiche markdown selon format S55 fiche v5 forward (template ci-dessous). Vocabulaire opérateur uniquement, pas plumbing. Pas `intent_mix: {primary: DR}`, dire `Type de campagne : direct response`. Pas `overlay_density: 0.6`, dire `Cadrage : hook + claim layered sur packshot`.

**No orphan output.** Terminer sur 1 reco douce (soft offer) ancrée sur ce qui vient d'être composé. Langage métier zéro jargon technique, jamais nommer de skill ni concept interne.

- Chaîne cohérente · *"Cette créa est cohérente. Si tu veux, on peut la tester sur Meta avec ton audience principale."*
- Hypothèse non-validée · *"Pas encore certain que cet angle va marcher. Si tu veux, on peut tester 2 angles en parallèle pour voir lequel performe."*
- Variantes possibles · *"Si tu veux, on peut décliner cette créa (autre hook, autre persona, autre plateforme) sans tout refaire."*
- Photo produit manque · *"Il manque une photo officielle du produit pour vraiment bien faire. Si tu en as une, drop-la, sinon on peut la générer."*

**Anti-pattern UX prose** · JAMAIS nommer `compose-creative`, `recompose-creative`, `define-specs`, `photo_swap`, `hook_swap`, `persona_split`, `Visual_identity` en surface operator. Soft offer langue métier · "tester", "décliner", "drop-la", "photo officielle".

Une reco forte, pas trois équivalentes.

---

## HR7 · Anti-patterns

1. **Compose sans visual_identity.** Régression label garantie sous 2 iter (audit S55 wordmark with brackets dégradé en variant sans brackets sur brand test workspace). Refuse de composer si `packshots.primary_front` absent dans les 2 paths (spec.json#visual_identity ET sibling visual_identity.json).
2. **Hardcoded mécanique.** Modifier le prompt mécanique hardcodé dans le skill au lieu de lookup canon registry SSOT. Drift inévitable cross-products.
3. **Skip angle.formula validation.** NOYAU sans angle = creative null. Refuse de composer si `angle.json` absent ou `formula` vide.
4. **Direct write produced/.** Mode `proposed` non-optionnel. Mutation gate via `write_to_context` obligatoire.
5. **Regen >3 iter pour label preservation.** Basculer en mode layered (HR-COMPOSITE) si canonical asset dispo, sinon flag opérateur en langage métier (HR3.4). Ne pas brûler API budget en boucle.
6. **JSON brut leak.** Surface `intent_mix: {primary: DR, weights: {DR: 0.6}}` à l'opérateur. Règle : traduction systématique en langage métier.
7. **Plumbing leak.** Surface `field_path`, `source`, `confidence`, `mode` à l'opérateur. Règle : opérateur voit `observé / déduit / déclaré / incertain`, jamais numbers.
8. **Doctrine name leak.** Surface `canonical-matrix-reasoning`, `Contextual Intelligence`, `Schema Encoding Discipline` à l'opérateur. Règle : opérateur sent les effets, pas les noms.
9. **Hypothesis from scratch sans validation.** Mode `hypothesis_from_scratch` propose 2-3 angles candidats AVANT de composer, jamais compose direct sur angle inventé.
10. **Phantom navigation leak.** Imiter `/phantom` avec "→ Tape : compose-next". Règle : 1 reco contextuelle en prose, pas de menu, pas de slash command surfacé.

---

## Operator output template

### Fiche canonique v2.51 forward template

Réf canonique · `resources/templates/operator-fiche-output.md`. Header plain language, body en vocabulaire métier, footer soft offer 1 ligne max. Bloc retrieval `concept_id`/`variant_of`/`intent_mix` persiste en backstage (creative.json) mais n'apparaît PAS dans le rendu operator.

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Pub n°{N}
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD} · {1 phrase plain language qui décrit la pub · ex "pub direct response Meta carrousel pour audience post-grossesse"}

───────────────────────────────────────────────────────────────
1 · CE QUE LA PUB MONTRE
───────────────────────────────────────────────────────────────
Format             {plain · ex "carrousel · 4:5 · français" ou "image statique · 1:1 · anglais"}
Accroche visuelle  {description scène en prose · 1-2 lignes}
Accroche texte     "{verbatim hook · max 8 mots}"
Corps              {description body · 1 ligne · ou — si pas de body}
Bouton             "{verbatim CTA}"
Branding           {plain · ex "Logo en bas à droite · photo officielle du produit centrée"}
Photo générée      ouvre dans Preview · open {path}

───────────────────────────────────────────────────────────────
2 · CE QUE LA PUB RACONTE
───────────────────────────────────────────────────────────────
Cible              {1 phrase plain · ex "femmes 35-45 post-grossesse, chute de cheveux + sentiment perte d'identité"}
Niveau conscience  {plain · ex "consciente du problème, pas encore du produit"}
Vérité non-dite    "{verbatim insight}" · {formulée | implicite | absente}
Angle              {1 phrase plain · ex "frustration des soins de surface"}
Type de campagne   {plain · "direct response" ou "branding" ou "direct response avec touche brand (priorité direct response)"}
Mécanique          {nom métier · ex "before-after-bridge"} · {1 phrase explicative}
Pivot du concept   "{atome irréductible}" · {1 phrase justif}

───────────────────────────────────────────────────────────────
3 · DIAGNOSTIC
───────────────────────────────────────────────────────────────
Cohérence          {plain · ex "tient · la mécanique reflète l'insight, l'angle est cohérent avec la cible"}
Score arrêt-scroll {★★★★☆ · 1-5 stars · 1 phrase courte}
Forces             · {observable concret · ex "rupture pattern Meta feed via cadrage carré sur visage"}
                   · {observable}
                   · {observable}
Risques            · {observable · ex "claim 'cliniquement testé' nécessite preuve attachée"}
                   · {observable}
                   · {observable}

───────────────────────────────────────────────────────────────
{1 reco soft offer 1 ligne max · ex "Si tu veux, on peut la tester en live sur Meta avec ton audience principale."}
```

**Backstage (creative.json, NON rendu operator)** · `concept_id`, `variant_of`, `variant_axis`, `intent_mix`, `execution.overlay_density`, `execution.brand_mark_present`, `tags.source`, `meta.validation_status`, etc. Vivent dans le JSON persisté pour retrieval programmatique et audit · operator ne les voit pas.

**Validation pre-ship fiche** ·
1. Header ne contient pas `COMPOSE CREATIVE`, `CRT-N`, `variant_axis`, `concept_id`
2. Body ne contient pas `intent_mix: {...}`, `overlay_density: 0.6`, `craft_mode`, field paths JSON
3. Footer · 1 phrase soft offer max, jamais menu (a)/(b)/(c), jamais "Tape commande X"
4. Vocabulaire cohérent avec `resources/templates/operator-fiche-output.md § Mappings vocabulaire`

---

## Edge cases

- **Hypothesis from scratch (pas d'angle_id).** Skill propose 2-3 angles candidats depuis `profile.problem_map` + `canon/copy/formules-titres`. Demande validation opérateur AVANT pipeline gen. Ne compose jamais sur angle inventé sans gate.
- **Multi-products brand.** Si `product_slug` absent et marque a 2+ produits, demande choix opérateur (1 question AskUserQuestion). Ne devine pas.
- **Visual_identity partiel.** `primary_front` présent mais `distinctive_features[]` vide → continue, flag confidence dégradée. `primary_front` absent → refuse.
- **fal.ai API down ou rate limit.** Surface honnête, propose retry ETA + langage métier soft offer. Ne tente pas mock.
- **Label régressé après 3 iter.** Persiste creative.json + JPG avec note `label_compositing_required: true` dans meta (backstage). Flag à l'opérateur en langage métier HR3.4 (soft offer · canoniser la photo produit pour text fidelity garantie).
- **Concept variant.** Si opérateur déclare "comme CRT-12 mais hook différent", set `variant_of: {parent_concept_id}` + `variant_axis: hook_swap`. Lineage préservé.

---

## Cross-refs

- Schema cible : `resources/schemas/creative.schema.json` v1.2 (D#391, audit Phase B v2.29.0 + v2.32 alignment).
- Équation : `resources/templates/creative-formula.md` v3.1 (stress-tested S55, 23 ads cross-typologies).
- SSOT mécaniques : `resources/registries/creative-mechanics-registry.md`.
- Schwartz stages : `resources/schemas/_shared/awareness-stage.json`.
- Visual identity schema : `resources/schemas/spec.schema.json#visual_identity` (v1.10+, S55 v2.31 extension).
- Audit visual fidelity : `decisions.md` D#392 (S55 audit régression label wordmark with brackets).
- Sibling skills : `decompose-ad` (REVERSE pattern, fiche v5 layout source), `produce-paid-angles` (forward angles textuels), `produce-copy-brief` (brief copy seul), `recompose-creative` (variant existant), `define-specs` (visual_identity prerequisite), `profile-audience` (profile prerequisite), `craft-packshot` v1.1+ (canonical asset upstream pour mode `layered` HR3b · v2.47), `compose-overlay-text` v2.43+ (text overlay PIL post-gen · complémentaire à layered packshot).
- Doctrines : `docs/system/canonical-matrix-reasoning.md` (production discipline), `docs/system/skill-authoring-doctrine.md` (frontmatter triad), `docs/system/contextual-intelligence.md` (operator-facing rule absolue), `docs/system/model-versioning-canon.md` v2.44+ (endpoint canon nano-banana-2/edit, frontmatter permissions.external_apis[] obligatoire), `docs/system/visual-identity-doctrine.md` v2.43+ (canonical assets + wordmark_pattern).
- Audit v2.46 endpoint migration : craft-packshot v1.1 upstream (S55 v2.44 stress test produit canon gen v10 · 1 attempt vs 9 échouées nano-banana-pro legacy) · pattern stress-testé puis propagé downstream consumers.
- Pattern v2.47 layered compositing · packshot canon (craft-packshot) + scène séparée nano-banana-2 + PIL composite paste · résout problème historique label regression sans burn budget API retry · text fidelity garantie 100% via substrat canonisé.
