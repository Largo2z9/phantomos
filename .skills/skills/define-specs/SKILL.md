---
name: define-specs
version: 1.3.1
type: orchestrator
recommended_model: sonnet
subagent_safe: true
layer: territoire
mode: proposed
operator_facing: true
patch_notes:
  v1.3.1: "v2.81.1 decomposition visibility NIVEAU LIVE · NEW section `Niveau LIVE · raisonnement thinking aloud pendant exécution` insérée AVANT Step 0bis prerequisite check (au début Hard Rules). Action LOURDE classification (orchestre snapshot + Q&A + ingest-resource + encoding spec.schema v1.10 + 3 niveaux Specs Visibility Matriciel post-exec). NIVEAU LIVE narratif étendu obligatoire pendant exécution · 2 niveaux abstraction obligatoires (macro contexte produit positionnement + micro spec → mécanisme → bénéfice 3 couches phrasé en prose narrative sobre). Pose pair senior expert thinking aloud · audit temps réel par l'opérateur entre specs encodées + pédagogie posture experte indissociables. Cross-ref `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid). Backward compat strict additif · cycle runtime préservé (Step 0bis + HR1-HR5 + Output Specs Visibility Matriciel preserved)."
  v1.3.0: "v2.78.2 decomposition-visibility-discipline · Output NEW section Specs Visibility Matriciel 3 niveaux obligatoire après encoding (specs objectifs · mécanismes · bénéfices 3 couches canon pain-benefit-chain). Méthode pédagogique verbale obligatoire. Cross-refs decomposition-visibility-discipline + pain-benefit-chain. Backward compat strict additif (existing Phases preserved)."
  v1.2.0: "v2.58 coverage extend · service_specs Q&A flow activé pour spec.identity.type service/clinical_service/hybrid (v1.11) · contraindications Q&A flow activé pour produits/services à contraintes usage. Closes 2 orphans audit v2.57. Backward compat strict additif."
description: >
  v1.3.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution (au début Hard Rules avant Step 0bis). Action LOURDE · narratif étendu 2 niveaux abstraction (macro contexte produit positionnement + micro spec → mécanisme → bénéfice 3 couches phrasé en prose). Pose pair senior expert · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  v1.3.0 (v2.78.2 decomposition-visibility-discipline) · Output NEW section Specs Visibility Matriciel 3 niveaux obligatoire après encoding (specs · mécanismes · bénéfices 3 couches canon pain-benefit-chain). Méthode pédagogique verbale obligatoire. v1.2.0 (v2.58 coverage extend) · service_specs Q&A flow activé pour spec.identity.type service/clinical_service/hybrid (v1.11) · contraindications Q&A flow activé pour produits/services à contraintes usage.
  FR: "définis les specs", "crée la fiche produit", "remplis le produit", "spec produit", "qu'est-ce que le produit", "cartographie le produit".
  EN: "define specs", "create product card", "populate product", "product spec", "what is the product", "map the product".
disambiguates_against:
  snapshot-brand: "snapshot-brand fait le scrape URL pur (auto). define-specs orchestre snapshot + Q&A operator + sources upload pour produits sans URL ou champs non-scrapés."
  cartograph: "cartograph est READ-ONLY (synthèse strategique). define-specs WRITE (peuple spec.json)."
  propose-schema-draft: "propose-schema-draft crée nouveau schema canon (R&D). define-specs peuple un spec.json existant pour une brand."
consumes:
  - resources/schemas/spec.schema.json
  - resources/schemas/spec.schema.json#visual_identity
  - brands/{slug}/brand.json
  - resources/canon/copy/*
  - skills.snapshot-brand
  - skills.ingest-resource
produces_validations_for: []
produces_proposals_for:
  - brands/{slug}/products/{product_slug}/spec.json
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/products/{slug}/spec.json via write_to_context]
  emits_events: [spec_proposal_created, spec_validated, spec_persisted]
pipeline:
  preconditions:
    - "brand.json existe"
    - "product slug défini ou disponible"
  postconditions:
    - "spec.json conforme spec.schema v1.10"
    - "operator validation gate passed"
prerequisites:
  - field: product.url
    level: L1
    auto_pull: shopify_products_api
    freshness_ttl_days: 7
  - field: operator.input_mode
    level: L2
    options:
      - url_provided
      - manual_qa
      - sources_upload
  - field: products/{slug}/sources/
    level: L1
    auto_pull: read_uploaded_files
    freshness_ttl_days: 30
  - field: products/{slug}/spec.json
    level: L1
    auto_pull: read_existing_spec_brownfield
    freshness_ttl_days: 90
---

## Description

`define-specs` est l'orchestrateur Phase 1 (Spec/Mécanisme/Bénéfice) qui peuple un `spec.json` produit en combinant trois sources de matière brute : auto-pull URL via `snapshot-brand`, ingestion de docs opérateur via `ingest-resource`, et Q&A guidé pour les gaps non-scrapés. La spec produit est le socle factuel qui alimente toute la chaîne downstream (audiences, angles, briefs copy). Skill hybride : aucun champ n'est écrit sans validation gate explicite de l'opérateur.

Posture : éducateur + collègue. Tu rassembles la matière, tu proposes l'assemblage, l'opérateur valide ou corrige. Jamais d'auto-write silencieux. Jamais d'hallucination de champ sans source.

## Hard Rules

### HR0 · Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ · orchestre snapshot + Q&A + ingest-resource + encoding spec.schema v1.10 + 3 niveaux Specs Visibility Matriciel post-exec). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement disclosure pré-engagement en amont et Output Specs Visibility Matriciel matricielle (NIVEAUX 1-3) en aval.

Pattern obligatoire · l'agent verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique le produit et encode chaque section spec.json, en prose narrative sobre (zéro matrice ASCII en LIVE · les matrices viennent en Output Specs Visibility Matriciel post-encoding).

**2 niveaux d'abstraction obligatoires** ·

1. **Macro contexte produit positionnement** · verbaliser la compréhension du périmètre produit AVANT de rentrer dans le détail spec.
   Exemple define-specs · "On part d'un produit {nom · catégorie · sous-catégorie} qui s'inscrit dans la brand {positioning macro · stade Schwartz inféré sophistication marché} comme {hero / secondaire / entry / new launch}. Le pattern catalogue indique {hero positionne sur axe X · ce produit drainage sub-axe Y · cohérent ou divergence détectée}. Le type produit · {DTC physical / service / clinical_service / hybrid · subscription / one-shot · refill / consommable} parce que {signaux scrape + Q&A operator + ingest sources}. Mon hypothèse de mécanisme dominant · {physiologique / technique / émotionnel / identitaire} parce que {pattern claims PDP + verbatims reviews tagged si disponibles + canon catégorie}."

2. **Micro spec → mécanisme → bénéfice 3 couches phrasé** · verbaliser la chaîne produit en prose narrative pendant l'encoding spec.json.
   Exemple define-specs · "Cette spec {composition / ingrédient / feature dominante phrasé sourced PDP ou Q&A} → mécanisme physiologique ou technique {comment ça agit · phrasé canon} → bénéfice fonctionnel {ce qui change extérieurement mesurable · résolution pain de surface} + bénéfice émotionnel {ce qui change subjectivement ressenti · résolution pain conséquence} + bénéfice identitaire {ce que l'audience projette socialement · résolution pain deep racine}. Cross-référence avec spec.contraindications si produit/service à contraintes usage · {phrasé canon pourquoi contraintes obligatoires v2.58}."

**Calibration narrative** · prose sobre · registre pair senior expert · zéro jargon plumbing (jamais `spec.json#identity.type`, `_field_types`, `confidence_chain[]`, schema field_path en LIVE) · zéro tableau ASCII en LIVE (matrices = Output Specs Visibility Matriciel post-encoding). Adapter le tonal au registre opérateur détecté (grounded · standard · dense).

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger entre specs encodées si l'agent part dans une mauvaise direction d'inférence (mauvais mécanisme physiologique projeté · mauvaise couche bénéfice dominante · mauvaise classification type produit/service) AVANT que les downstream consume cette base, (b) pédagogie · il apprend la posture experte sur cartographie produit en regardant la manière de penser une chaîne spec → mécanisme → bénéfice 3 couches canon pain-benefit-chain.

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant detection input mode (Step 1), scanner prerequisites :

1. Lookup `product.url` (operator-fournie ou pré-existante brand) → si présente + freshness 7d OK → L1 auto_pull Shopify silent
2. Lookup `products/{slug}/spec.json` brownfield existing → si présent + freshness 90d OK → read as seed silent
3. Lookup `products/{slug}/sources/` upload files → si présents + freshness 30d OK → ingest-resource silent
4. Si aucun des 3 résolus → L2 gate operator avec 3 options (url_provided / manual_qa / sources_upload)

Output state map des inputs disponibles + confidence_chain[] init.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

### HR1 · Detect input mode

Au démarrage, identifier le mode selon ce que l'opérateur fournit :

- **URL produit (Shopify, site brand) seule** → `mode: auto_pull`
- **Pas d'URL mais sources fournies (PDF brief, deck founder, CSV)** → `mode: source_ingest`
- **Ni URL ni sources** → `mode: q_and_a`
- **Combinaison de 2 ou 3 sources** → `mode: hybrid` (lance les 3 et merge)

Surface au démarrage en une phrase :
> "J'ai détecté [URL / sources / rien]. Je vais [auto-pull / ingest / Q&A guidé / les 3 en parallèle]. OK ?"

Confirmer le mode avant de lancer les sub-skills.

### HR2 · Auto-pull (mode auto_pull ou hybrid)

Si URL produit fournie :

1. Spawn `snapshot-brand` sub-skill via Task tool avec l'URL en input
2. Récupérer le draft `spec.json` populated retourné
3. Cache local dans `/tmp/define-specs/{brand}-{product}-snapshot.json`
4. Identifier les champs remplis vs vides depuis le snapshot output

Tagger la source des champs remplis comme `observed` (scrape literal).

### HR3 · Source ingest (mode source_ingest ou hybrid)

Si sources opérateur fournies (PDF, deck, CSV) :

1. Spawn `ingest-resource` sub-skill via Task tool avec les paths sources
2. Extraire les données structurables (specs, ingrédients, claims, dimensions, pricing)
3. Cache local dans `/tmp/define-specs/{brand}-{product}-sources.json`
4. Cross-référencer avec snapshot output si mode `hybrid`

Tagger la source des champs comme `structured` (inferred from documents).

### HR4 · Q&A guidé (mode q_and_a ou hybrid pour combler gaps)

Pour chaque section `spec.schema` majeure non-couverte par auto-pull/sources, poser 1 à 2 questions concises. Sections cibles :

- `identity` (catégorie, niche, type, positionnement, tagline)
- `specs` (matériaux, composition, dimensions, format)
- `mechanisms[]` (cible biologique/cognitive, mode action, fenêtre temporelle, niveau preuve)
- `benefits[]` (chaîne functional → emotional → identity)
- `problems_solved[]` (pain résolus + verbatims)
- `pricing` (prix, currency, modèle)
- `visual_identity` (packshots URLs, color_palette hex, label wordmark, distinctive_features)

Règle dure : **JAMAIS plus de 3 questions par tour**. Privilégier batch question (regrouper champs proches dans un seul prompt). Tagger les réponses comme `declared`.

### HR4.1 · Branche service_specs (v1.2.0 · spec.identity.type service / clinical_service / hybrid)

**Activation conditionnelle** · quand `spec.identity.type` ∈ {`service`, `clinical_service`, `hybrid`} (v1.11 enum extension), ajouter branche Q&A spécifique services pour populer `spec.specs.service_specs`.

Champs cibles ·

- `service_type` (select · consulting · coaching · clinical · workshop · subscription_membership)
- `duration_per_session` (text · "1h", "90 min", "demi-journée")
- `delivery_format` (select · in-person · remote · hybrid)
- `frequency` (select · ad-hoc · weekly · monthly · quarterly · once-off)
- `target_outcomes[]` (résultats clients attendus, array text)
- `prerequisites[]` (clients required state, array text)
- `tools_provided[]` (deliverables · slides · framework · 1-on-1 calls, array text)

Batch question typique (regrouper 3 max par tour cf. HR4) ·

> *Type de service · consulting / coaching / clinique / workshop / membership ?*
> *Format · présentiel / distanciel / hybride ?*
> *Durée par session · "1h", "90 min", "demi-journée" ?*

Puis tour suivant pour fréquence + outcomes/prerequisites/tools_provided regroupés.

Stage ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/products/{p_slug}/spec.json#/specs/service_specs" \
  --value '{"service_type":"consulting","duration_per_session":"90 min","delivery_format":"hybrid","frequency":"weekly","target_outcomes":["..."],"prerequisites":["..."],"tools_provided":["..."]}' \
  --source operator \
  --confidence 0.9 \
  --mode proposed \
  --reason "Service business_model Q&A flow"
```

Tagger les réponses comme `declared`.

### HR4.2 · Branche contraindications (v1.2.0 · produits/services à contraintes usage)

**Activation conditionnelle** · pour produits/services avec contraintes usage (cosmétique réactive · santé · service médical · `spec.identity.type` ∈ {`clinical_service`, certains produits cosmétiques/santé/nutrition signalés via `category` ou `niche`)), branche Q&A spécifique pour populer `spec.specs.contraindications`.

Champs cibles ·

- `medical_conditions[]` (conditions médicales contre-indiquées, array text)
- `age_restrictions` (text · "≥18 ans", "12-65 ans", "déconseillé < 6 ans")
- `pregnancy_warnings` (text · "déconseillé grossesse + allaitement", "ok 2e trimestre", "n/a")
- `drug_interactions[]` (interactions médicamenteuses, array text)
- `allergic_reactions[]` (allergènes/réactions documentées, array text)

Batch question typique (regrouper 3 max par tour cf. HR4) ·

> *Conditions médicales contre-indiquées (liste courte si applicable) ?*
> *Restrictions d'âge (mineurs, seniors) ?*
> *Grossesse / allaitement · ok, déconseillé, n/a ?*

Puis tour suivant pour drug_interactions + allergic_reactions si pertinents.

Stage chacun via write-to-context.py mode=proposed sur `spec.json#/specs/contraindications/{field}`. Tagger `declared`.

### HR5 · Assemble draft spec.json

Merge les outputs `auto_pull` + `source_ingest` + `q_and_a` en un draft unique conforme `spec.schema v1.10`.

Tagger chaque champ dans `_field_types` selon sa source :

- `observed` (auto-pull scrape literal)
- `declared` (operator Q&A)
- `structured` (inferred from multiple sources / docs)

Résolution conflit : si 2 sources donnent valeurs différentes pour un même champ, priorité `observed > declared > structured`. Flagger le conflit dans la section "GAPS DÉTECTÉS" du surface.

### HR6 · Surface draft à operator avec validation gate

Présenter le draft `spec.json` en format opérateur-facing (template ci-dessous). **Pas de JSON brut**. Vue lisible avec sections groupées.

Demander explicitement :
> "Voici la fiche produit assemblée. Tu valides en bloc, tu corriges un champ, ou tu poses une question ?"

- Si operator confirms en bloc → HR7
- Si operator corrige → boucle Q&A ciblée sur les champs corrigés, puis re-surface
- Si operator pose question → répondre, puis re-demander validation

### HR7 · Persist via mutation gate

Une fois validé, écrire via `write_to_context` sur `brands/{slug}/products/{product_slug}/spec.json`.

- `source = "operator_validated"`
- `confidence` dépend du `_field_types` de chaque champ
- `mode = "proposed"` (le mutation gate gère le commit)

Trigger `validate-resources` silencieusement post-write. Flagger seulement les MAJOR/CRITICAL à l'opérateur.

### HR8 · Output operator-facing

Vue lisible spec posée + next-step proposal contextuel :

- Si `snapshot-brand` n'a pas tourné dans la session et URL était disponible → propose-le pour enrichir
- Si `audiences/` vide → suggérer `map-audiences` (futur skill v2.33)
- Si produit a un Shopify URL mais `visual_identity` manque → suggérer packshot pull dédié

Format no-orphan-output : 1 reco forte + 1 ou 2 chemins backup si genuinely useful.

### HR8.5 · Output Specs Visibility Matriciel 3 niveaux (canon v2.78.2)

Après encoding specs produit (composition · mécanismes · bénéfices via HR5-HR7) et AVANT le next-step proposal (HR8), présenter OBLIGATOIREMENT la matrice 3 niveaux canon `decomposition-visibility-discipline` v2.78.2. Cette section rend visible à l'opérateur comment specs objectifs, mécanismes et bénéfices se mappent entre eux (graph atomique reverse engineering possible).

Backward compat strict · cette section vient s'ajouter APRÈS l'output spec posée existant (HR8 surface), pas en remplacement. L'opérateur voit d'abord la fiche assemblée (HR6 template), valide, puis reçoit la synthèse matricielle.

Bloc obligatoire à présenter (format opérateur-facing, pas JSON brut) ·

```
═══════════════════════════════════════════════════════════════
Specs Visibility · 3 niveaux canon (decomposition-visibility v2.78.2)
═══════════════════════════════════════════════════════════════

NIVEAU 1 · Specs objectifs (ce que le produit EST)
─────────────────────────────────────────────────
PRODUCT          {product_name} ({product_slug})
Catégorie        {category}
Type             {physical_product | digital_product | service | hybrid}

Atomes matériels observables ·
  Format / packaging       {format}
  Composition / materials  {composition}
  Posologie / usage        {usage}
  Cure / cycle             {cycle}
  Certifications           {certifications si applicable}

NIVEAU 2 · Mécanismes (ce qu'il FAIT)
─────────────────────────────────────
Atomes action sur corps / contexte ·

  [Mécanisme 1] · {mechanism.name}
    Target          {target} (corps system / context system)
    Mode of action  {mode_of_action}
    Time window     {time_window}
    Evidence level  {scientific | clinical_claim | empirical | anecdotal_strong | claim}
    Sources         {études / certifications / claims}

  [Mécanisme 2] · {mechanism.name}
    ...

Cross-réf vers map-mechanisms (canon-driven · EFSA/NCT/INSERM/etc.) si shipped et applicable.

NIVEAU 3 · Bénéfices 3 couches canon pain-benefit-chain
───────────────────────────────────────────────────────
Atomes ressentis · canon Halbert/Sugarman/StoryBrand ·

  FUNCTIONAL · {benefit.benefit} (bénéfice visible mesurable)
    emotional_signal   {signal}
    latency            {immediate | 7-14j | 2-12 semaines | etc.}
    evidence_verbatim  {verbatim sourcé}
    mechanism_ref      {Mécanisme N upstream}

  EMOTIONAL · {benefit.benefit} (bénéfice ressenti subjectif)
    emotional_signal   {signal}
    latency            {...}
    evidence_verbatim  {verbatim sourcé}
    mechanism_ref      {...}

  IDENTITY · {benefit.benefit} (qui je suis · identitaire)
    emotional_signal   {signal}
    latency            {...}
    evidence_verbatim  {verbatim sourcé}
    mechanism_ref      {...}
    ← layer le plus chargé sur audiences cible (si verbatim signal fort)
```

### Méthode pédagogique verbale obligatoire

Après le bloc matriciel, verbaliser TOUJOURS comment l'agent a décomposé les specs ·

> *"J'ai décomposé {product name} en 3 niveaux canon ·*
> *1. SPECS (objectif matériel) · {N} atomes*
> *2. MÉCANISMES (action) · {N} atomes ranked evidence_level*
> *3. BÉNÉFICES 3 couches (canon pain-benefit-chain) ·*
>    *Functional · {résumé}*
>    *Emotional  · {résumé}*
>    *Identity   · {résumé} ← layer le plus chargé sur ton segment cible*
>
> *Chaque bénéfice référence un mécanisme upstream (mechanism_ref canonical) · graph atomique reverse engineering possible · spec → mécanisme → bénéfice → pain addressed → audience served."*

Rappel posture · l'opérateur voit `observé / déduit / déclaré / incertain` (jamais `source / confidence / mode / field_path` raw cf HR9). La verbalisation utilise vocabulaire opérateur, pas vocabulaire interne.

### HR9 · Anti-patterns

- **JAMAIS** auto-write sans operator validation gate (HR6)
- **JAMAIS** poser plus de 3 questions par tour
- **JAMAIS** halluciner des specs sans source explicite (auto-pull, doc, ou operator stated)
- **JAMAIS** skip le mode hybrid si les 3 sources sont disponibles
- **JAMAIS** exposer JSON brut à l'opérateur dans le surface draft
- **JAMAIS** exposer `source`, `confidence` (numbers), ou `_field_types` raw. Traduire en `observé / déduit / déclaré / incertain` si la distinction aide
- **JAMAIS** utiliser em dash dans output
- **JAMAIS (v2.78.2)** encoding specs silent sans synthèse matricielle 3 niveaux (skip HR8.5)
- **JAMAIS (v2.78.2)** bénéfices 1 couche only (skip 2 autres layers canon pain-benefit-chain · functional + emotional + identity sont les 3 layers canoniques, jamais réduire à 1)
- **JAMAIS (v2.78.2)** `mechanism_ref` absent sur un bénéfice (bénéfice orphelin · pas de reverse engineering possible · chaîne spec → mécanisme → bénéfice cassée)
- **JAMAIS (v2.78.2)** skip méthode pédagogique verbale (opérateur ne sait pas comment specs décomposés · cf verbatim canon HR8.5)

## Operator output template (HR6 surface)

```
═══════════════════════════════════════════════════════════════
{brand_humain} · Fiche produit · {product_name}
═══════════════════════════════════════════════════════════════

Identité
  Catégorie         {category} (observé)
  Niche             {niche}
  Type              {type}
  Tagline           {tagline} (déclaré)
  Positionnement    {positioning}

Specs
  Matériaux         {materials}
  Composition       {composition}
  Format            {format}
  Volume / Quantité {volume}

Mécanismes (chaîne causale spec → bénéfice)
  · {mechanism_1.name} · cible {target} · fenêtre {time_window}
  · {mechanism_2.name} ...

Bénéfices (chaîne functional → emotional → identity)
  BNF-01 {benefit_name}
    functional   {chain.functional}
    emotional    {chain.emotional}
    identity     {chain.identity}
  ...

Problèmes résolus
  PRB-01 {problem} (verbatim sources : {n})
  ...

Pricing
  Prix          {price} {currency}
  Modèle        {pricing_model}

Identité visuelle
  Packshot      {packshot_url} (observé Shopify)
  Couleurs      container {hex} · label {hex} · content {hex}
  Label         {wordmark} · {sub_label}
  Distinctive   {features[]}

Gaps détectés
  · {champ_1} : pas couvert (proposer Q&A ?)
  · {champ_2} : conflit auto-pull vs operator (résoudre ?)

Validation requise · valider en bloc, corriger un champ, ou poser une question ?
```

## Cross-refs

- Schema target : `resources/schemas/spec.schema.json` (v1.10+ avec `visual_identity`)
- Sub-skill auto-pull : `.skills/skills/snapshot-brand/SKILL.md`
- Sub-skill ingest : `.skills/skills/ingest-resource/SKILL.md`
- Doctrine production : `docs/system/canonical-matrix-reasoning.md`
- Doctrine substrate : `docs/system/schema-encoding-doctrine.md`
- Doctrine authoring : `docs/system/skill-authoring-doctrine.md`
- Doctrine racine v2.78.2 + v2.81.1+ NIVEAU LIVE : `docs/system/decomposition-visibility-doctrine.md` (3 phases temporelles · AVANT exec NIVEAU 0 paramètres décomposés · PENDANT exec NIVEAU LIVE thinking aloud expert action LOURDE 2 niveaux abstraction macro produit + micro spec → mécanisme → bénéfice 3 couches phrasé · APRÈS exec NIVEAUX 1-3 Output Specs Visibility Matriciel · HR-DVD-11 + AP-DVD-11 enforcement)
- Doctrine 3 couches bénéfices : `docs/system/pain-benefit-chain.md` (functional · emotional · identity canon Halbert/Sugarman/StoryBrand)
- Doctrine investigation 5 sections : `docs/system/investigation-posture.md` (Observé / Déduit / Inconnu / Leviers / Close ouvert)
- Sister skills v2.78.2 + v2.81.1+ : `snapshot-brand` · `build-atlas-complete` · `profile-audience`
- Mutation gate : `write_to_context` (jamais Edit/Write direct sur `.json`)
- Validation post-write : `validate-resources`
