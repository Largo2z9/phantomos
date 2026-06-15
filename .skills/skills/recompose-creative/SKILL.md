---
name: recompose-creative
version: 1.4.0
patch_notes_brick4_step_c:
  - "1.4.0 (Brique 4 étape C · repath batch READ-source cross-batch + WRITE-variant batch-du-jour + split genome/creative/sidecar + mkdir-claim + variant_axis COLLAPSE) · La règle HR-RC-CANON-1 (déclarée en frontmatter v2.87.4 mais JAMAIS exécutée dans le body) est désormais MATÉRIALISÉE en section `## HR-RC-CANON-1` réelle et exécutable, miroir de compose-creative v1.9.0 (étape B). (1) REPATH LECTURE (consumes) · recompose lit le creative SOURCE sous la forme batch `brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json` (+ `genome.json` frère pour l'ADN), PAS `produced/{CRT-N}.json` flat-legacy. L'id source est GLOBAL au namespace CRT (batch-indépendant) → le lookup SCANNE TOUS les dossiers `{batch}/` pour localiser le `{CRT-NN}` source. consumes L53 + prerequisites L74 + auto-pull body + preconditions + HR2 alignés sur la même lecture. (2) REPATH ÉCRITURE · recompose PRODUIT une variante = un NOUVEAU `CRT-NN` dans le batch DU JOUR (la variante va dans le run courant par cohérence-de-run ; le CRT source est trouvé par scan cross-batch, la variante n'hérite PAS de son batch). mkdir-CLAIM STEP 0 atomique (résoudre {batch} du jour, scanner max CRT cross-batch, `mkdir` atomique du nouveau `{CRT-NN}/` + `produced/`, retry +1 sur EEXIST, refus-AVANT-claim). SPLIT persist · genome.json (ADN hérité/adapté de la source · genome/1.2) + creative.json (lignage · variant_of=CRT-source · variant_axis · creative/1.4) + produced/{slug}.json (sidecar manifest binaire · produced-asset/1.0) + brief.md. Le binaire .jpg écrit DIRECT sous produced/, le sidecar json passe par le gate. rebuild snapshot ajouté (était manquant). (3) variant_axis COLLAPSE (LE gros fix de recompose) · l'enum CANONIQUE = creative.schema `variant_axis` = `[photo_swap, promo_toggle, hook_swap, background_swap, persona_split, null]` (SINGLE string|null). SUPPRESSION des 4 vocabulaires divergents · la famille `new_*` (menu prereq L78 + HR1), le mapping mixte interne (L156), la liste persistée à 9 valeurs (HR6 L246 · retrait de platform_swap/format_swap/visual_treatment_swap/audience_swap qui ne sont PAS dans le schéma). Le menu opérateur garde des labels plain-language MAIS une TABLE menu→enum déterministe résout chaque choix vers EXACTEMENT une valeur canonique. variant_axis reste SINGLE (1 axe par recompose, son contrat). (4) variant_of = le CRT-NN source (pattern `^(CRT|RCV)-[0-9]{2,4}$` ; pour recompose c'est CRT). Vit dans creative.json#lineage (+ top-level miroir backward). recompose = 100% namespace CRT, jamais RCV. (5) _schema_version → creative/1.4 + genome/1.2. Cross-ref `resources/conventions/creative-storage.md` (D#481) + sibling compose-creative v1.9.0. Backward compat · forme cible imposée par le gate write-to-context.py (briques 1+3) · les anciennes écritures plates étaient déjà rejetées runtime, ce patch aligne le SOP sur le gate. NOTE Notion bridge auto-wire DEFERRED v2.88.0+ (sync-creatives-to-notion pas shipped)."
patch_notes_v2_87_4:
  - "1.3.0 (v2.87.4 canonical many-to-many enforcement mirror) · NEW HR-RC-CANON-1 mirror sibling compose-creative v1.8.0 · enforcement entry canonical `brands/{slug}/creatives/{CRT-NN}/` OBLIGATOIRE post-recomposition. Toute variante DOIT être NEW entry canonical (pas surcharge entry parent · variant_of ref dans lineage) · lineage populated avec `variant_of: CRT-{parent}` + tags variant typed (concept stable · creative new · variant true) + cross-refs many-to-many activés. Asset JPG sauvé dans `creatives/{CRT-NN}/produced/` (pas hors structure). Closes audit Fincut v2.87.3 finding · variantes générées sans entry canonical = perte traçabilité parent/enfant + tableau composition cassé. Backward compat strict additif. NOTE v2.87.4 cette règle restait phantom (déclarée ici, jamais exécutée body) · MATÉRIALISÉE en section `## HR-RC-CANON-1` exécutable par Brique 4 étape C (v1.4.0). NOTE Notion bridge auto-wire DEFERRED v2.88.0+ (sync-creatives-to-notion pas shipped)."
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
  v1.4.0 (Brique 4 étape C · repath batch + split genome/creative/sidecar + mkdir-claim + variant_axis collapse) · recompose lit le creative SOURCE sous la forme batch `creatives/{batch}/{CRT-NN}/creative.json` (+ genome.json frère pour l'ADN), id source GLOBAL au namespace CRT scanné cross-batch, et PRODUIT une variante = un NOUVEAU CRT-NN dans le batch DU JOUR (split genome.json + creative.json + produced/{slug}.json sidecar + brief.md, dossier réservé par mkdir-claim atomique STEP 0). variant_axis collapse sur l'enum canonique creative.schema (5+null, single). variant_of = le CRT-NN source (namespace CRT, jamais RCV). _schema_version creative/1.4 + genome/1.2. Backward compat · forme cible imposée par le gate.
  v1.2.2 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.0.0 (v2.34 ship production loop) : 3e skill P5 visual aux côtés de decompose-ad
  (reverse) et compose-creative (forward). Adapte une créa interne testée (ou
  hypothesis) en variante alignée sur UNE dimension changée : audience, plateforme,
  format, hook, traitement visuel. Output : nouveau CRT-NN qui réutilise concept_id
  parent + flag variant_of source + variant_axis canonique. Préserve concept core
  (mécanique, ton, intent_mix) ; ne change qu'une dimension à la fois. Persiste
  (Brique 4 étape C · split) sous brands/{slug}/creatives/{batch}/{CRT-NN}/ avec
  meta.validation_status = hypothesis (tag derived_from_test_results si la source a
  un score). Pipeline visuel mirror compose-creative (HR3) avec prompt adapté
  preservation-first. Output operator-facing : vue compacte side-by-side source vs
  variant + brief markdown explicit "WHAT CHANGED vs SOURCE".
  FR: "adapte cette créa", "version pour autre audience", "déclinaison",
  "variant créa", "variante TikTok", "version story", "décline cette créa".
  EN: "adapt this creative", "version for another audience", "variant",
  "tiktok version", "story version", "decline this creative".
disambiguates_against:
  compose-creative: "compose-creative crée ex nihilo depuis brand intelligence + angle. recompose-creative ADAPTE un creative existant (1 dimension change, concept core préservé)."
  decompose-ad: "decompose-ad analyse une ad EXTERNE (reverse-engineering benchmark concurrent). recompose-creative adapte une créa INTERNE (mode internal_production, source CRT-NN déjà persisté sous creatives/{batch}/{CRT-NN}/)."
  produce-paid-angles: "produce-paid-angles produit un nouveau ANGLE (forward generation depuis brand intelligence). recompose-creative garde l'angle, change autre dimension (audience/platform/format/hook/visual)."
  weave-hooks: "weave-hooks incarne des concepts NEUFS en scripts (amont) · recompose-creative décline une créa EXISTANTE en variantes (aval)"
consumes:
  - path: brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json
    min_version: 1.3.0
    note: "creative source obligatoire (couche lignage). L'id CRT-NN est GLOBAL au namespace CRT (batch-indépendant) → scanner TOUS les dossiers {batch}/ pour le localiser. concept_id réutilisé pour la variante."
  - path: brands/{slug}/creatives/{batch}/{CRT-NN}/genome.json
    min_version: 1.0.0
    note: "ADN frère du creative source (mécanique/format/support/hook/frames/genome_tags). Lu pour préserver le concept core en regen. {CRT-NN} localisé par le même scan cross-batch."
  - path: brands/{slug}/audiences/{audience_slug}/profile.json
    min_version: 1.0.0
    note: requis si l'axe variante = persona_split (recalibrage audience cible)
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: packshots clean URL + distinctive features pour préserver fidélité produit en regen
  - path: resources/schemas/creative.schema.json
    min_version: 1.3.0
    note: "couche lignage (Brique 4 étape C · creative/1.4 · variant_of CRT|RCV + lineage{} + variant_axis enum canonique SSOT)"
  - path: resources/schemas/genome.schema.json
    min_version: 1.0.0
    note: "NEW Brique 4 étape C · ADN par-créa (genome/1.2 · script_id GSC-NN, hook, frames, support, genome_tags) hérité/adapté de la source"
  - path: resources/schemas/produced-asset.schema.json
    min_version: 1.0.0
    note: "NEW Brique 4 étape C · sidecar manifest binaire (produced-asset/1.0 · 1 par .jpg produit, anti-orphelin)"
  - path: resources/conventions/creative-storage.md
    min_version: 1.0.0
    note: "forme batch creatives/{batch}/{CRT-NN}/ + allocation mkdir-claim (D#481)"
  - path: resources/canon/copy/formats-livrables/*.json
    min_version: 1.0.0
    note: requis si l'axe variante touche plateforme/format (lookup contraintes ratio/durée/ton, mappé sur background_swap pour l'axe canonique)
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
produces_proposals_for:
  - brands/{slug}/creatives/{batch}/{CRT-NN}/genome.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg
  - brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md
prerequisites:
  - field: creatives/{batch}/{CRT-NN}/creative.json
    level: L1
    auto_pull: read_creative_source
    freshness_ttl_days: 60
    note: "source localisée par scan cross-batch (id CRT-NN global). genome.json frère lu pour l'ADN."
  - field: variant_axis
    level: L2
    options:
      - photo_swap
      - promo_toggle
      - hook_swap
      - background_swap
      - persona_split
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
    creative source CRT-NN existe sous brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json (namespace CRT, batch dirs).
    L'id CRT-NN source est GLOBAL au namespace CRT → résolu par scan cross-batch de tous les dossiers {batch}/.
    genome.json frère disponible pour l'ADN à préserver.
    1 dimension change explicite (variant_axis ∈ enum canonique [photo_swap, promo_toggle, hook_swap, background_swap, persona_split]).
    Credentials FAL_API_KEY présent dans credentials_shared.env pour pipeline visuel.
    Si variant_axis = persona_split, audience cible profile.json existe.
    Si l'axe touche plateforme/format (résolu vers background_swap), canon formats-livrables disponible.
    {batch} du jour résolu (run date-stampé, ex 2026-06-07-NN) et `mkdir -p brands/{slug}/creatives/{batch}/` exécuté AVANT le mkdir-claim, sinon STEP 0 n'a pas de dossier-batch parent.
  postconditions: |
    Nouvelle CRT-NN (réservée par mkdir-claim atomique STEP 0) persistée dans le batch DU JOUR sous brands/{slug}/creatives/{batch}/{CRT-NN}/ via le split :
    genome.json (genome/1.2 · ADN hérité/adapté de la source) + creative.json (creative/1.4 · variant_of=CRT-source, variant_axis canonique, lineage{}) + sidecar produced/{slug}.json (produced-asset/1.0) + brief.md.
    JPG écrit DIRECT sous {CRT-NN}/produced/{slug}.jpg AVEC son sidecar le traçant (anti-orphelin). brief.md écrit DIRECT.
    concept_id réutilisé de la source (SSOT du groupage de variantes). variant namespace reste CRT (jamais RCV).
    meta.validation_status = {status: hypothesis, confidence: 0.5, confidence_source: derived_from_test_results} si la source a un score, sinon derived_from_hypothesis.
    tags.source = "internal_production".
    rebuild snapshot via build-brand-snapshot.py {slug} si un core file est touché. validate-resources triggered silencieusement.
---

# Skill: recompose-creative

> **Adapt an existing internal creative.** v1.4.0 · Brique 4 étape C · split genome/1.2 + creative/1.4 + produced-asset/1.0 · forme batch `creatives/{batch}/{CRT-NN}/` · variant_axis enum canonique · 3e skill P5 visual.

Adaptateur, not generator. Lit un creative interne déjà persisté sous la forme batch `creatives/{batch}/{CRT-NN}/` (id CRT-NN source GLOBAL au namespace CRT, localisé par scan cross-batch), change UNE dimension explicitement déclarée par l'opérateur, persiste (Brique 4 étape C · split) un NOUVEAU CRT-NN dans le batch DU JOUR · genome.json (ADN) + creative.json (lignage · variant_of + variant_axis canonique) + sidecar produced/{slug}.json + brief.md. Le dossier {CRT-NN}/ est réservé par mkdir-claim atomique AVANT tout write. Concept core (mécanique, ton, intent_mix) toujours préservé. Rend une vue side-by-side source vs variant à l'opérateur en langage clair. Pour refonte 2+ dimensions ou nouveau concept, route vers compose-creative.

## Tone

Posture collègue senior media buying qui décline une créa testée. Pas inventeur. La fiche est dense mais lisible : ce qui reste vs ce qui change, justification courte de l'adaptation, comparaison side-by-side. Aucun JSON brut, aucun field_path interne. Si une dimension n'est pas explicitement déclarée, AskUserQuestion pour la fixer avant tout pipeline visuel.

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant adaptation (Step 1), scanner prerequisites :

1. L1 silent · `creatives/{batch}/{CRT-NN}/creative.json` source (required · id CRT-NN résolu par scan cross-batch de tous les dossiers `{batch}/`) + `genome.json` frère (ADN) · `resources/canon/copy/formats-livrables`
2. L2 gate · `variant_axis` non spécifié → AskUserQuestion menu 5 options plain-language (HR1). Le choix opérateur résout déterministiquement vers UNE valeur de l'enum canonique creative.schema.

Output state map + confidence_chain[] init avec variant_axis selected.

---

## Hard Rules

### HR1 · Identify variant axis explicit (menu plain-language → enum canonique)

Skill exige opérateur précise QUELLE dimension change. Surface au démarrage en langage clair, zéro enum technique entre parenthèses ·

```
Tu veux changer quoi sur cette créa ? Une seule chose à la fois ·
(a) la photo / le packshot (même hook, même scène, autre visuel produit)
(b) la promo affichée (toggle promo on/off, autre offre commerciale)
(c) le hook copy (variant A/B même visuel)
(d) la scène / le décor (autre background, même produit, même hook · couvre aussi plateforme/format)
(e) le persona ciblé (autre audience, même concept)
```

Si l'opérateur reste ambigu ou tente de changer 2+ dimensions, AskUserQuestion mandatoire. Rappel · 2+ dimensions change = route compose-creative (nouveau concept), pas recompose-creative.

**Table menu → enum canonique (NON surface operator · déterministe, 1 choix = 1 valeur)** · le choix opérateur (a)-(e) résout vers EXACTEMENT une valeur de l'enum canonique `creative.schema.json#variant_axis` = `[photo_swap, promo_toggle, hook_swap, background_swap, persona_split, null]`. Cet enum reste backstage pour retrieval programmatique · operator ne le voit jamais.

| Choix opérateur (plain-language) | `variant_axis` canonique (persisté) |
|---|---|
| (a) la photo / le packshot | `photo_swap` |
| (b) la promo affichée | `promo_toggle` |
| (c) le hook copy | `hook_swap` |
| (d) la scène / le décor (inclut plateforme/format) | `background_swap` |
| (e) le persona ciblé (autre audience) | `persona_split` |

**Single axis (contrat recompose)** · `variant_axis` reste un SEUL string (ou null), jamais un array. recompose change EXACTEMENT 1 axe par invocation. C'est son contrat et la SSOT du schéma (`creative.schema.json#variant_axis` est single-enum). Pour multi-axes, c'est un nouveau concept → compose-creative.

> **NOTE plateforme/format (axe (d) → `background_swap`)** · un changement de plateforme (Meta → TikTok) ou de format (image → carrousel) modifie principalement la scène/le décor et les contraintes natives ; il se résout sur l'axe canonique `background_swap`. Les contraintes ratio/durée/ton restent lookées dans `resources/canon/copy/formats-livrables/` (HR3) et adaptées dans le genome (`support`, `aspect_ratio`, `format`), mais l'axe de lignage persisté est `background_swap` (l'enum schéma ne porte ni `platform_swap` ni `format_swap`).

### HR2 · Load creative source + identify what stays vs changes

Localiser le creative source par **scan cross-batch** (l'id CRT-NN est GLOBAL au namespace CRT, batch-indépendant) ·

```
ls -d brands/{slug}/creatives/*/{CRT_source} 2>/dev/null | head -1
```

Lire `brands/{slug}/creatives/{batch}/{CRT_source}/creative.json` ET son `genome.json` frère du même dossier :
- Depuis `creative.json` (lignage) · capturer `concept_id` source (sera réutilisé pour le variant, pas régénéré), `lineage{}` (refs), `intent_mix`, `execution`, `tags`, `meta.validation_status` + `meta.test_results[]` (pour décider le statut de la variante en HR6).
- Depuis `genome.json` (ADN) · capturer `support`, `hook` (mechanic_id + hook_text), `frames[]`, `genome_tags`, `lineage` ADN. C'est le concept core (mécanique, ton, intent_mix) à préserver.

Selon variant_axis (valeur canonique), marquer rigoureusement ce qui reste vs ce qui change :

| variant_axis (canonique) | Reste inchangé | Change |
|---|---|---|
| `photo_swap` | hook (genome), mécanique, format, scène, intent_mix | visuel produit / packshot (genome `frames[].visual_script`, produced/) |
| `promo_toggle` | concept core, hook, mécanique, scène | offre commerciale (`modifiers.offer`, overlay promo) |
| `hook_swap` | visual_script, mécanique, intent_mix | `hook.hook_text` (genome) · overlay verbal |
| `background_swap` | hook, mécanique, ton, produit (couvre plateforme/format) | scène/décor (genome `frames[].visual_script`) + contraintes natives (`support`, `aspect_ratio`) si plateforme/format change |
| `persona_split` | mécanique, format, visuel, hook | `lineage.audience_ref`, `context.persona`, registre copy recalibré |

Anti-pattern : retain 0 dimension du concept core = c'est compose-creative déguisé, refuser et re-router.

### HR3 · Apply contraintes platform/format spécifiques

Si l'axe variante touche la plateforme ou le format (choix opérateur (d), résolu vers `variant_axis: background_swap`), lookup `resources/canon/copy/formats-livrables/{platform}.json` :

- **TikTok** : ratio 9:16, attention < 3 sec, native UGC plus fort, music context
- **Instagram Story** : ratio 9:16, swipe up CTA, sticker tap
- **Instagram Reel** : ratio 9:16, hook < 2 sec, trending audio, scroll-stop visuel
- **LinkedIn** : ratio 1.91:1 ou 1:1, ton professionnel, B2B context
- **YouTube Shorts** : ratio 9:16, hook < 5 sec, story arc compact
- **Meta Feed** : ratio 4:5 ou 1:1, hook scroll-stop visuel + verbal layered
- **Pinterest** : ratio 2:3 vertical, search-driven keywords visibles

Adapter les fields concernés dans le genome (`support`, `aspect_ratio`, `frames[].visual_script`, ton register). Si canon silencieux sur la plateforme demandée, surfacer à l'opérateur (*"pas de canon formats-livrables pour {platform}, je peux improviser sur les contraintes natives connues ou tu valides un override ?"*). L'axe de lignage persisté reste `background_swap` (l'enum schéma ne porte pas de valeur platform/format dédiée).

### HR4 · Génération visuelle adaptée (preservation-first)

Pipeline mirror compose-creative HR3 (FAL nano-banana-2/edit canon v2.46), prompt ajusté pour préserver le concept core :

- **Référence visuel original** : image_urls inclut le binaire parent persisté `brands/{slug}/creatives/{batch}/{CRT_source}/produced/{slug}.jpg` (le `{CRT_source}` localisé par scan cross-batch HR2 ; `/tmp/compose-creative/` reste cache éphémère acceptable si présent).
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
- **Staging + persist** : download dans `/tmp/compose-creative/{brand}-{crt_id}.jpg` (staging éphémère), puis move final vers `brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg` (binaire écrit DIRECT · le dossier `{CRT-NN}/produced/` existe déjà, réservé par le mkdir-claim HR-RC-CANON-1 STEP 0) PUIS émettre le sidecar `produced/{slug}.json` (produced-asset/1.0 · `asset_role`, `file`, `tool: "fal"`, `endpoint`, `params`, `source_asset_ref: {kind: "parent_frame", path: <binaire parent>}`, `status: "generated"`, `created_at`, `genome_ref: <script_id GSC-NN>`) via `write_to_context` mode=proposed (anti BUG-ASSET-ORPHAN). Double régime · binaire .jpg direct, sidecar .json par le gate. Détail HR6 + HR-RC-CANON-1.

### HR5 · Generate variant brief markdown

Format opérateur-facing avec section explicite "WHAT CHANGED vs SOURCE". Écrit DIRECT (nom fixe `brief.md`) sous `brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md` (outil Write · `.md` exempt de `ALLOWED_PATH_PATTERNS` ET de mutation-guard, ne PAS router via `write_to_context`) ·

```markdown
# CRT-NN · Variant of CRT-source

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
| Field | Source (CRT-source) | Variant (CRT-NN) |
|---|---|---|
| audience | ... | ... |
| platform | ... | ... |
| format | ... | ... |
| ratio | ... | ... |

## Test recommendation
{a/b vs source · 2 autres axes à explorer si performant · score-matrix}
```

### HR6 · Persist split genome.json + creative.json + sidecar + brief.md (Brique 4 étape C)

> Le mkdir-claim atomique (réservation du `{CRT-NN}/` dans le batch DU JOUR) est exécuté en **STEP 0 de HR-RC-CANON-1** (section ci-dessous), AVANT cette persist. HR6 écrit dans le dossier déjà réservé.

L'unique `creative.json` historique se SPLIT en trois fichiers `.json` (+ le brief `.md`), chacun conforme à son schéma. La variante hérite/adapte l'ADN de la source. **NEVER** Edit/Write direct sur un `.json`, **ALWAYS** via `write_to_context` mode=proposed.

**genome.json** (ADN · conforme `genome.schema.json` `_schema_version: "genome/1.2"`, strictement nu) ·
- `script_id` : nouveau `GSC-NN` (Genome SCript · clé de join perf future · PAS CRT-NN · pattern `^GSC-[0-9]{2,4}$`).
- `support`, `route`, `hook`, `frames`, `genome_tags` (dont **`genome_tags.mecanique_id`** = le CONCEPT ad-level ET **`genome_tags.angle_id`** = l'ANGLE [unité stratégique de 1ère classe · porte objection+OTRB+payoff] + `audience_slug` · hérités TEL QUEL sauf si `variant_axis` les modifie · D#491/492) : hérités de la source PUIS la dimension changée par `variant_axis` est appliquée (ex `hook_swap` → nouveau `hook.hook_text` ; `background_swap` → nouveau `frames[].visual_script` + `support`/`aspect_ratio` adaptés).
- `lineage` (optionnel ADN abstrait) : `{concept_id (réutilisé source), angle_id (ANG-NN), persona_label}`.

**creative.json** (lignage · conforme `creative.schema.json` `_schema_version: "creative/1.4"`) ·
- `creative_id` : nouveau `CRT-NN` (réservé par mkdir-claim STEP 0 · pattern `^CRT-[0-9]{2,4}$`).
- `mode` : hérité source (`concept | template | asset`). `audience_slug` (nouveau si persona_split). `_equation_ref` const v3.1.
- `concept_id` = source.concept_id (réutilisé, PAS régénéré · SSOT du groupage de variantes).
- `variant_of` = source.creative_id (le `CRT-NN` source · pattern `^(CRT|RCV)-[0-9]{2,4}$` · pour recompose c'est TOUJOURS un CRT, jamais RCV). Vit dans `lineage.variant_of` (+ top-level `variant_of` miroir backward-compat).
- `variant_axis` ∈ enum canonique creative.schema `[photo_swap, promo_toggle, hook_swap, background_swap, persona_split, null]` (single string · valeur résolue par la table HR1).
- `lineage{}` : `{angle_ref (ANG-NN), audience_ref, product_ref, mechanism_ref, concept_ref (miroir descriptif de concept_id), variant_of (CRT-source), brief_ref (BRF-NN), ad_id}`.
- `intent_mix` hérité source. Champ legacy `intent` mirror backward-compat.
- `execution.overlay_density` + `execution.brand_mark_present` hérités source (sauf si changés par l'axe). Champ legacy `craft_mode` mirror dérivé.
- `meta.validation_status` = `{status: "hypothesis", confidence: 0.5, confidence_source: "derived_from_test_results"}` si la source CRT-NN a un score testé (`meta.test_results[]` non vide), sinon `confidence_source: "derived_from_hypothesis"`. `meta.created`. `meta.created_by_skill: "recompose-creative"`.
- `performance.longevity_signal` vide (variante pas encore en prod). `tags.source = "internal_production"`.
- Tous les autres fields hérités de la source sauf ceux explicitement changés par variant_axis.

**produced/{slug}.json** (sidecar manifest binaire · conforme `produced-asset.schema.json` `_schema_version: "produced-asset/1.0"`) · UN sidecar par binaire `.jpg` produit (anti-orphelin) ·
- `asset_role` (ex `"composite-final"`, `"variant-front"`), `file` (ex `"{slug}.jpg"`), `status: "generated"`, `created_at` requis.
- `tool: "fal"`, `endpoint: "fal-ai/nano-banana-2/edit"`, `params` (prompt/aspect_ratio/resolution), `source_asset_ref: {kind: "parent_frame", path: <binaire parent CRT-source>}`, `hash` optionnel, `qc` optionnel.
- `genome_ref` : `<script_id GSC-NN>` (relie le binaire à l'ADN sans le dupliquer). `created_by_skill: "recompose-creative"`.

**Mutation gate (séquence) :**

1. **Dossier déjà réservé** par le mkdir-claim atomique STEP 0 (HR-RC-CANON-1) · `creatives/{batch}/{CRT-NN}/` + `produced/` existent dans le batch DU JOUR. NE PAS s'appuyer sur le `mkdir(exist_ok=True)` du gate (non-atomique · 2 runs concurrents écraseraient le même `CRT-NN`).
2. Write `genome.json` + `creative.json` + sidecar `produced/{slug}.json` via `write_to_context(field_path, value, source, confidence, mode="proposed")` (les trois `.json`). **NEVER edit JSON directly via Edit/Write/NotebookEdit.**
3. Persist JPG : move `/tmp/compose-creative/{brand}-{crt_id}.jpg` → `brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg`. **Le binaire `.jpg`/`.mp4` est écrit DIRECT** (`write_to_context` ne gère que le `.json`), MAIS son sidecar `.json` (step 2) passe par le gate. Double régime non-négociable.
4. Write brief markdown : `brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md` (nom fixe `brief.md`, format HR5). **Écrit DIRECT via l'outil Write** (`.md` n'est NI dans `ALLOWED_PATH_PATTERNS` du gate write-to-context, NI dans mutation-guard qui ne garde que `.json`) · ne PAS router le `.md` via `write_to_context` (échouerait).
5. Rebuild snapshot via `python3 .skills/build-brand-snapshot.py {slug}` si un core file est touché (mutation rule · la variante est un nouvel artefact créa du brand).
6. Trigger `validate-resources` silencieusement post-write (valide genome + creative + sidecar contre `genome.schema.json` / `creative.schema.json` / `produced-asset.schema.json`, et la forme de path contre `ALLOWED_PATH_PATTERNS`). Flag MAJOR/CRITICAL à l'opérateur si remonte.
7. **Gate QC de sortie** · invoquer `qc-creative` (`creative_dir` = le `{CRT-NN}/` variante produit · Task tool · sonnet · subagent_safe) sur le binaire, écrire le verdict dans `produced/{slug}.json#qc` via `write_to_context`, et NE PAS présenter la variante comme spend-ready sans `decision: PASS`. Règle anti-défaut · logo/produit fidélité-critique = compositing `layered`, jamais re-généré. Voir `qc-creative/SKILL.md`.

---

## HR-RC-CANON-1 · Entry canonical batch + mkdir-claim (Brique 4 étape C · exécutable)

> Cette règle était déclarée en frontmatter (`patch_notes_v2_87_4`) mais JAMAIS exécutée. Elle est ici MATÉRIALISÉE en section réelle, miroir de compose-creative v1.9.0 (HR-CC-CANON-1). Toute variante recomposée DOIT créer son dossier canonique `brands/{slug}/creatives/{batch}/{CRT-NN}/` AVANT tout write, persister le split (genome + creative + sidecar + brief), et interdire tout asset orphelin hors structure. Cross-ref `resources/conventions/creative-storage.md` (D#481).

### Refus AVANT claim (ordre HR8)

Tous les refus HR8-style (variant_axis absent · 2+ dimensions · retain 0 concept core · `FAL_API_KEY` absent · source CRT-NN introuvable au scan cross-batch) s'exécutent **AVANT STEP 0c**. Un run refusé ne doit JAMAIS laisser un dossier `CRT-NN/` réservé vide. La claim atomique ne se prend qu'une fois la génération garantie possible.

### STEP 0 · mkdir-claim atomique (AVANT tout write_to_context)

Le mkdir-claim s'exécute en **STEP 0**, juste avant la génération visuelle persistée (HR4 produit le binaire en `/tmp` ; HR6 persiste dans le dossier réservé ici). **La variante va dans le batch DU JOUR (run courant), PAS dans le batch de la source** · le CRT source est trouvé par scan cross-batch (STEP 0b), mais le nouveau CRT-NN est écrit dans le `{batch}` du jour par cohérence-de-run.

**STEP 0a · résoudre {batch} du jour.** `{batch}` = run date-stampé du jour, lowercase + chiffres + tirets (regex gate `[a-z0-9-]+`). Default = `$(date +%Y-%m-%d)-NN` où NN = prochain run 2-digit du jour. Résoudre NN · lister `brands/{slug}/creatives/` pour les dossiers matchant `$(date +%Y-%m-%d)-*`, prendre le max suffixe, sinon `01`. Un run PEUT réutiliser le batch de session déjà ouvert. `mkdir -p brands/{slug}/creatives/{batch}/` (idempotent · le dossier-batch n'est PAS la claim).

**STEP 0b · candidat CRT-NN (scan max cross-batch).** Scanner TOUT l'arbre du namespace CRT pour le max existant, PAS juste le batch courant (les id sont globalement uniques dans le namespace CRT, batch-indépendants) · c'est le MÊME scan cross-batch qui sert à localiser la source en HR2 ·
```
ls -d brands/{slug}/creatives/*/CRT-* 2>/dev/null | grep -oE 'CRT-[0-9]{2,4}' | sort -t- -k2 -n | tail -1
```
→ N. Candidat = `CRT-(N+1)`, zero-paddé à ≥2 digits. CRT scanné SÉPARÉMENT de RCV (jamais fusionnés · RCV = namespace concurrent decompose-ad · recompose reste 100% CRT, jamais RCV).

**STEP 0c · claim atomique.** `mkdir brands/{slug}/creatives/{batch}/CRT-{N+1}/` SANS `-p` sur le segment final (le parent `{batch}/` existe déjà depuis 0a). `mkdir` sur un dossier existant échoue → **c'est le verrou** (la réservation). Sur succès · l'id est à toi, immédiatement `mkdir -p brands/{slug}/creatives/{batch}/CRT-{N+1}/produced/`. Sur EEXIST · `N = N+1`, retry (boucle bornée, ex 50 essais). C'est le SEUL mécanisme de réservation · pas de fichier-index, pas de lock-file, pas d'écrivain privilégié. Les trous d'id sont inoffensifs (unicité requise, pas absence-de-trou).

> **PIÈGE (vérifié source · write-to-context.py L453 `target.parent.mkdir(parents=True, exist_ok=True)`)** · ce mkdir du gate n'est PAS une claim atomique. Si un skill saute STEP 0c et compte sur le mkdir du gate, deux runs concurrents passent tous les deux et écrivent dans le MÊME `CRT-NN`, clobbering silencieux. Le `mkdir` atomique (sans `exist_ok`) DOIT être fait par le skill en STEP 0c.

**STEP 0d · write dans le dossier réservé.** MAINTENANT (HR6) · `write_to_context` les trois `.json` (`genome.json`, `creative.json`, sidecar `produced/{slug}.json`) en mode=proposed. Binaires (.jpg/.mp4) déplacés DIRECT sous `.../produced/` (write_to_context ne gère que le json). `brief.md` écrit DIRECT (outil Write · `.md` exempt de `ALLOWED_PATH_PATTERNS` ET de mutation-guard).

### Lignage 5-refs + variant_of obligatoire

`creative.json#lineage` doit être populé · `angle_ref` (ANG-NN) + `audience_ref` + `product_ref` + `mechanism_ref` + `concept_ref` (miroir descriptif de `concept_id`, SSOT groupage = `creative.concept_id` top-level) + `variant_of` (le `CRT-NN` source · namespace CRT, jamais RCV). Cross-refs many-to-many activés. JAMAIS surcharger le dossier `{CRT-source}/` parent · la variante est TOUJOURS un nouveau `{CRT-NN}/` réservé par mkdir-claim, source append-only.

### Interdit orphelin

JAMAIS sauver un asset JPG/PNG standalone hors structure (e.g. `visual-identity/creative_ANG-01_*.jpg` orphelin). TOUT binaire vit sous `creatives/{batch}/{CRT-NN}/produced/` AVEC son sidecar `produced/{slug}.json` (manifest gated). Pas de binaire sans sidecar (anti BUG-ASSET-ORPHAN). Pas d'entry variante sans genome.json + creative.json.

---

### HR7 · Output operator-facing

Vue compacte side-by-side source vs variant. Reco no-orphan-output finale :

- Suggest A/B test source vs variant si pas encore testé
- Suggest 2 autres axes de variation à explorer si concept performant en source
- Suggest `score-matrix` pour prioriser variants à tester si déjà 3+ variants existent

### HR8 · Anti-patterns

- **NEVER** recomposer sans variant_axis explicite (mode hypothesis trop large, pollue creative DB)
- **NEVER** changer 2+ dimensions simultanées (c'est un nouveau concept, route compose-creative)
- **NEVER** promouvoir `variant_axis` en array (casse le contrat single-axis de recompose ET le schéma single-enum). 1 axe = 1 string canonique.
- **NEVER** persister une valeur `variant_axis` hors enum canonique creative.schema `[photo_swap, promo_toggle, hook_swap, background_swap, persona_split, null]` (les anciennes `platform_swap`/`format_swap`/`visual_treatment_swap`/`audience_swap`/`new_*` sont SUPPRIMÉES · validate-resources rejette).
- **NEVER** écraser le creative source ni son dossier `{CRT-source}/` (toujours nouveau `{CRT-NN}/` réservé par mkdir-claim avec variant_of, source append-only)
- **NEVER** skip retain de concept core (sinon c'est compose-creative déguisé, refuser et re-router)
- **NEVER** mettre la variante dans le batch de la source (la variante va dans le batch DU JOUR · le CRT source est trouvé par scan cross-batch, jamais hérité de batch)
- **NEVER** `variant_of` en namespace RCV pour recompose (recompose = 100% CRT · RCV est réservé aux concurrents decompose-ad)
- **NEVER** confusion régime d'écriture sous `produced/` · INTERDIT écrire un `.json` (genome/creative/sidecar) en direct (toujours `write_to_context` mode=proposed) · ATTENDU écrire le binaire `.jpg`/`.mp4` DIRECT sous `produced/` (write_to_context ne gère que le json) MAIS chaque binaire DOIT avoir son sidecar `produced/{slug}.json` gated (anti BUG-ASSET-ORPHAN)
- **NEVER** exposer JSON brut, field_path, ou enum interne (`variant_axis` valeurs) à l'opérateur en surface output. Traduire en langage clair (*"on garde le hook, on change juste la scène"*)
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
Dimension          {plain · ex "audience cible" ou "scène / décor" ou "photo produit" ou "hook texte" ou "promo affichée"}
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

Photo générée      ouvre dans Preview · open {path} (= creatives/{batch}/{CRT-NN}/produced/{slug}.jpg)

───────────────────────────────────────────────────────────────
{1 reco soft offer 1 ligne max · ex "Si tu veux, on peut tester A/B la source vs la variante."}
```

**Backstage (creative.json, NON rendu operator)** · `concept_id` (réutilisé source), `variant_of: {creative_id_source}` (CRT-NN), `variant_axis` enum canonique, `meta.validation_status`, `tags.source: internal_production`. Vivent dans le JSON pour retrieval programmatique · operator ne les voit jamais.

**Validation pre-ship fiche** ·
1. Header ne contient pas `RECOMPOSE`, `CRT-N → CRT-X`, `variant_axis:`, `concept_id`
2. Body ne contient pas `intent_mix: {...}`, `variant_of`, field paths JSON
3. Footer · 1 phrase soft offer max, jamais menu, jamais nommer skill `score-matrix` en surface

## Cross-refs

- `compose-creative` v1.9.0 (forward generation ex nihilo, sibling P5 visual · même split genome/creative/sidecar + mkdir-claim + forme batch · Brique 4 étape B)
- `decompose-ad` (reverse-engineering ad externe, sibling P5 visual · namespace RCV concurrent)
- Schemas cibles (Brique 4 étape C · split) : `resources/schemas/creative.schema.json` v1.3 (lignage · variant_of CRT|RCV + lineage{} + variant_axis enum canonique SSOT 5+null), `resources/schemas/genome.schema.json` v1.0 (ADN par-créa · script_id GSC-NN, hook, frames, support, genome_tags), `resources/schemas/produced-asset.schema.json` v1.0 (sidecar manifest binaire · 1 par .jpg, anti-orphelin)
- Convention stockage : `resources/conventions/creative-storage.md` (D#481 · forme batch `creatives/{batch}/{CRT-NN}/` + allocation mkdir-claim atomique · CRT source trouvé cross-batch, variante écrite dans le batch du jour)
- `resources/canon/copy/formats-livrables/*.json` (contraintes platform/format · axe (d) → background_swap)
- `docs/system/skill-authoring-doctrine.md` (frontmatter triad, type producer baseline)
- `docs/system/canonical-matrix-reasoning.md` (préservation concept core = matrix-driven)
- `validate-resources` (post-write silencieux), `build-brand-snapshot.py` (rebuild snapshot post-mutation)
