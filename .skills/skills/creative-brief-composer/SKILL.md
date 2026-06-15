---
name: creative-brief-composer
type: orchestrator
version: "1.4.0"
recommended_model: sonnet
subagent_safe: false
mode: proposed
operator_facing: true
isolation_scope: brand_only
layer: production
reasoning_pattern: null
extension_hooks:
  - creative_entity   # NEW creative types (e.g. video-script, podcast-script)
  - brief_entity      # NEW brief structures custom
  - audience_entity   # NEW audiences custom scaffolded
  - angle_entity      # NEW angle types
patch_notes:
  v1.3.0: "v2.75.0 NEW extension_hooks frontmatter declaration · permet manifest registry scan Step 0 DRGFP enrichi · NEW entities scaffolded via scaffold-extension v1.2.0+ avec consumable_by matching ce skill consommées automatiquement runtime. Backward compat strict additif · extension_hooks vide default · legacy v2.74.x comportement hard-coded canon entities preserved. Pattern canon doctrine extension-discovery-doctrine.md NEW v2.75.0."
  v1.2.0: "v2.64 ontologie sémantique pure pain_points + objections sub-audience · cohérence consume frontmatter · chain produce-copy-brief v1.6 + compose-creative v1.6 lisent désormais audiences/{audience_slug}/pain_points/*.json + audiences/{audience_slug}/objections/*.json sub-audience canonical. Frontmatter consumes: enrichi avec paths NEW sub-audience. Pas de modification logique propre orchestrator (Phase 1-5 pipeline inchangé), juste cohérence frontmatter + sub-skills versions bumped consistent. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved · sub-skills route transparent."
  v1.1.0: "v2.63 ontologie pure pain_points + objections collections top-level · cohérence consume frontmatter · chain produce-copy-brief v1.5 + compose-creative v1.5 lisent désormais pain_points/*.json + objections/*.json collections top-level (au lieu de profile.json sub-fields legacy). Frontmatter consumes: enrichi avec 2 paths NEW. Pas de modification logique propre orchestrator (Phase 1-5 pipeline inchangé), juste cohérence frontmatter + sub-skills versions bumped consistent. Backward compat lecture profile.pain_points[] + profile.objections[] legacy preserved · sub-skills route transparent selon disponibilité collections top-level vs profile sub-fields."
  v1.0.0: "v2.56 ship · résout gap orchestration Scenario 2 audit Phase 1. L'opérateur a sélectionné un angle prioritaire (via produce-paid-angles ou choix manuel) et veut matérialiser : brief structuré + 2-3 variants créa visuels Meta-ready. Chaîne produce-copy-brief → operator gate validate → compose-creative × N (parallèle ou séquentiel selon load). Orchestrateur pur, ne ré-implémente jamais la logique des sub-skills. Pattern Step 4-5 mirror onboard-brand (gate operator validate then push N variants). Cross-ref compositional-cartography.md §3 équation v3.1, investigation-posture.md output 5 sections."
description: >
  v1.2.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · orchestrator cohérence consume frontmatter · chain produce-copy-brief v1.6 + compose-creative v1.6 · les 2 sub-skills lisent désormais `audiences/{audience_slug}/pain_points/*.json` + `audiences/{audience_slug}/objections/*.json` sub-audience canonical. Pas de modification logique propre orchestrator · juste cohérence consume frontmatter + downstream sub-skills versions bumped. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.1.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · orchestrator cohérence consume frontmatter · chain produce-copy-brief v1.5 + compose-creative v1.5 · les 2 sub-skills lisent désormais `pain_points/*.json` + `objections/*.json` collections top-level (au lieu de profile.json sub-fields legacy). Pas de modification logique propre orchestrator · juste cohérence consume frontmatter + downstream sub-skills versions bumped. Backward compat lecture profile.pain_points[] + profile.objections[] legacy preserved (pre-v2.63 brands, route transparent).
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method, objections-mapping, pain-benefit-chain). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  Full-cycle creative materialization orchestrator. L'opérateur a sélectionné un angle prioritaire
  et veut générer brief structuré + 2-3 variants créa visuels Meta-ready en une seule passe.
  Chaîne : produce-copy-brief (brief artifact frontmatter brief.schema v1.0) → operator gate validate
  (brief markdown rendered, confirm ou ajuste) → compose-creative × N variants (visuels via
  nano-banana-2 + brief copy fiche v5). Synthèse finale 5 sections investigation-posture.
  Single operator intent, delegated pipeline across 2 producer skills.
  FR: "brief créa sur {angle_id}", "compose un brief créa", "génère brief + créa", "creative-brief-composer {angle_id}", "matérialise l'angle {angle_id}".
  EN: "creative brief composer", "compose brief and creative", "generate brief + variants", "materialize angle".
permissions:
  reads: [brand, product, profile, learning, strategy, angle, canon, visual_identity]
  writes: [brief, creative, learning]
  mode: proposed
  subagent_safe: false
consumes:
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
    note: identity + voice + tone register
  - path: brands/{slug}/audiences/{audience_slug}/profile.json
    min_version: 1.0.0
    note: audience source · 8 dimensions + Schwartz + persona
  - path: brands/{slug}/audiences/{audience_slug}/pain_points/*.json
    min_version: 1.0.0
    note: "v1.2.0 NEW v2.64 ontologie sémantique pure · pain_points canonical sub-audience (owned natif par parent path). Consumé downstream par produce-copy-brief v1.6 + compose-creative v1.6. Backward compat fallback top-level v2.63 + profile sub-fields v1.7."
  - path: brands/{slug}/audiences/{audience_slug}/objections/*.json
    min_version: 1.0.0
    note: "v1.2.0 NEW v2.64 ontologie sémantique pure · objections canonical sub-audience (owned natif par parent path). Consumé downstream par produce-copy-brief v1.6. Backward compat fallback top-level v2.63 + profile sub-fields v1.7."
  - path: brands/{slug}/pain_points/*.json
    min_version: 1.0.0
    note: "Legacy v2.63 backward compat read fallback · top-level collection."
  - path: brands/{slug}/objections/*.json
    min_version: 1.0.0
    note: "Legacy v2.63 backward compat read fallback · top-level collection."
  - path: brands/{slug}/angles/{angle_id}.json
    min_version: 1.2.0
    note: angle sélectionné · formula Obs+Tension+Reframe+Bridge + lineage canon (v1.3 pain_ref + objection_ref canonical v2.63 si produce-paid-angles v1.9+ a tourné)
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: visual_identity packshot canonisé (optional · fallback full_regen si absent)
  - path: brands/{slug}/products/{product_slug}/visual_identity.json
    min_version: 1.0.0
    note: fallback sibling path
  - path: resources/canon/copy/
    min_version: 1.0.0
    note: hooks + mécaniques + archétypes-voix + formules-titres
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
    note: mécaniques creative pour ranking variants
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/objections-mapping-doctrine.md
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
produces_proposals_for:
  - brands/{slug}/briefs/{BRF-NN}.md
  - brands/{slug}/creatives/{CRT-NN}.json
  - brands/{slug}/creatives/{CRT-NN}.jpg
pipeline:
  preconditions: |
    - brand_slug provided AND angle_id provided
    - angles/{angle_id}.json exists with lineage canon (formula + audience_slug + meta)
    - audiences/{audience_slug}/profile.json exists (angle's audience reference)
    - visual_identity packshot canonisé OPTIONAL (fallback full_regen mode si absent)
  postconditions: |
    - brief artifact persisté à brands/{slug}/briefs/{BRF-NN}.md (frontmatter brief.schema v1.0)
    - N variants créa persistés à brands/{slug}/creatives/{CRT-NN}.{json,jpg,md}
    - synthèse opérateur 5 sections investigation-posture + close ouvert
disambiguates_against:
  produce-copy-brief: "route to produce-copy-brief alone when operator wants ONLY a brief artifact, no visual creative downstream. creative-brief-composer chains brief → N visual variants in one pass."
  compose-creative: "route to compose-creative alone when operator already has a brief artifact and wants only visual variants. creative-brief-composer regenerates brief upstream of variants."
  produce-paid-angles: "route to produce-paid-angles when operator needs ANGLE IDEATION (matrice ranked). creative-brief-composer is downstream, angle is already selected."
  recompose-creative: "route to recompose-creative when adapting an existing creative variant. creative-brief-composer produces ex nihilo from angle."
---

# Skill: creative-brief-composer

**CRITICAL:** this is an **Orchestrator**. **YOU MUST NEVER** re-implement produce-copy-brief or compose-creative logic here. **YOU MUST** delegate to each existing skill in sequence via Task tool (`subagent_safe: true` on both sub-skills) or inline invocation. The orchestrator owns flow, gates, and synthesis. The sub-skills own production.

## Tone

Chairman orchestrating a 2-step pipeline with an operator gate in between. Narrate each handoff briefly to the operator (*"je pose le brief structuré sur l'angle... gate validation... je pars sur N variants en parallèle..."*). **NEVER** expose technical paths, field names, schema versions, or sub-skill names in operator-facing output. Keep the operator informed of progress without overloading.

## Engagement disclosure pré-runtime · canon v2.79.3

Avant de lancer la composition brief + variants, expose ce disclosure à l'opérateur (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.3) ·

```
Composition brief créa + N variants · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Pre-flight DRGFP (angle valide · audience résolue · visual_identity check)
  2. Load context (brand · audience · angle · canon refs)
  3. Génération brief structuré (produce-copy-brief sub-skill)
  4. Gate validation operator (binaire confirme ou ajuste)
  5. Composition N variants visuels parallèle (compose-creative × N)
  6. Synthèse 5 sections Investigation Posture + ranking + close

  ETA           ~12-20 min (selon N variants + visual_identity dispo)
  Implication   tu valides le brief avant push variants · N par défaut 3 (override possible)
  Livrable      1 brief structuré + N variants créa Meta-ready + ranking + reco test live

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite avant de lancer. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set ou si opérateur a flag `--no-disclosure` explicit. Sinon · disclosure obligatoire canon v2.79.3.

Cross-ref doctrine racine `docs/system/engagement-disclosure-doctrine.md` v2.79.3.

## Expert methodology

**Canonical expert persona** · senior creative director matérialisant un angle stratégique en deliverables Meta-ready en une seule sitting opérateur. Le brief sert le copywriter, les variants visuels servent l'A/B test live, l'orchestrateur garantit cohérence chain canon → brief → variants.

**Framework** · sequential pipeline avec gate operator entre brief et variants. Phase 1 produce brief, Phase 2 operator validate (binary gate, ajuste si demandé), Phase 3 compose N variants (parallèle si load permet, séquentiel sinon). Cross-ref `docs/system/compositional-cartography.md` §3 équation v3.1 NOYAU × CONTEXTE × MODIFIEURS · le brief encode NOYAU (angle + audience + canon), les variants composent CONTEXTE × MODIFIEURS (format · mécanique · craft).

**Matrix** ·

| Phase | Skill delegated | Subagent? | Gate before next phase |
|---|---|---|---|
| 0. Pre-flight DRGFP | inline | No | brand_slug + angle_id valides · angle.json + profile.json existent |
| 1. Load context | inline | No | angle + audience + brand + visual_identity loaded en mémoire orchestrateur |
| 2. Produce brief | `produce-copy-brief` | Yes (Task tool, sonnet) | brief artifact persisté `brands/{slug}/briefs/{BRF-NN}.md` frontmatter valide |
| 3. Operator gate validate | inline (AskUserQuestion) | No | operator confirme OR demande ajustements → loop Phase 2 |
| 4. Compose N variants | `compose-creative` × N | Yes (Task tool, opus, parallèle si N≤3) | N creatives persistés `brands/{slug}/creatives/{CRT-NN}.{json,jpg,md}` |
| 5. Synthesis 5 sections | inline | No | output operator-facing investigation-posture compliant |

**Variables tracked** ·
- `brand_slug` · brand workspace
- `angle_id` · ANG-NN sélectionné en input (mandatory)
- `audience_slug` · auto-derivé depuis angle.audience_slug
- `product_slug` · auto-derivé depuis angle.product_slug OR brand.primary_product
- `n_variants` · default 3, range 2-5 (operator override possible)
- `visual_identity_available` · bool · drives composite_mode (`layered` si canonical packshot dispo, `full_regen` sinon)

**Failure modes** ·
- angle_id introuvable ou lineage corrompu → abort Phase 1, surface gap à operator avec soft offer (regénérer angle via produce-paid-angles ou corriger ID)
- produce-copy-brief échoue mid-flow (thin voc, audience pauvre) → surface gap, propose mine-voc upstream, hold pipeline
- operator reject brief à Phase 3 → loop Phase 2 avec adjustments, max 2 retries avant escalate
- compose-creative échoue sur un variant (endpoint nano-banana-2 retry exhausted) → continue avec N-1 variants, log gap en synthesis Phase 5
- visual_identity absent ET operator pas autorisé fallback full_regen → hold, propose craft-packshot upstream

---

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

---

## Step 0 · Pre-flight (DRGFP)

Vérifier opérateur a fourni minimum context ·
- `brand_slug` explicite OR dérivable depuis brand active de session
- `angle_id` format `ANG-NN` (référence `brands/{slug}/angles/{angle_id}.json`)
- Optional · `n_variants` (default 3), `audience_slug` override, `channel` override

Si `angle_id` absent → AskUserQuestion *"Sur quel angle ? J'ai besoin d'un ANG-NN pour matérialiser. Veux-tu que je liste les angles encodés sur cette brand ?"*.

Si `angle_id` fourni mais fichier introuvable → soft offer *"Cet angle n'existe pas encore. Tu veux que je regénère une passe d'angles via produce-paid-angles, ou tu corriges l'ID ?"*.

Charger `angle.json` · valider `lineage` présent, `audience_slug` résolu, `product_slug` résolu OR fallback brand-wide.

Vérifier `visual_identity` (spec.json#visual_identity OR sibling visual_identity.json) · si absent, flag pour `composite_mode: full_regen` downstream Phase 4.

Annoncer le pipeline brièvement (chairman posture) ·

> *"OK, je matérialise l'angle {ANG-NN} sur {brand}. Pipeline · je pose le brief structuré sur l'audience encodée, tu valides, ensuite je pars sur {N} variants visuels en parallèle. ~5-8 min total selon le load. Let's go."*

---

## Step 1 · Load context (inline)

Lire en mémoire orchestrateur ·
- `brands/{slug}/brand.json` · identity + voice + tone register
- `brands/{slug}/audiences/{audience_slug}/profile.json` · 8 dimensions + Schwartz + persona + verbatims
- `brands/{slug}/angles/{angle_id}.json` · formula complète + lineage canon (hook + framework + archetype + leads)
- `brands/{slug}/products/{product_slug}/spec.json#visual_identity` (OR sibling fallback) · packshot canonisé + color_palette + distinctive_features
- `resources/canon/copy/` directory · hooks + mécaniques + archétypes-voix + formules-titres registries
- `resources/registries/creative-mechanics-registry.md` · pour ranking variants downstream

Si voc density faible (`voice.key_expressions[] < 5` OR cumulative `verbatim_quotes[] < 5`) sur l'audience référencée → flag à operator avant Phase 2 · *"L'audience sur cet angle est mince côté voix client (2 expressions captées). Le brief sortira moins ancré qu'il pourrait. Tu veux que je lance mine-voc d'abord, ou on continue avec ce qu'on a ?"*. Hold gate. Sinon, continue silently.

---

## Step 2 · Delegate to `produce-copy-brief` via Task tool

Spawn subagent ·
- `model: sonnet` (per produce-copy-brief frontmatter)
- `subagent_safe: true` verified
- Input · brand_slug, angle_id, audience_slug (résolu depuis angle), channel (default `meta_static_image`), product_slug optional
- Expected output · brief artifact persisté `brands/{slug}/briefs/{BRF-NN}.md` avec frontmatter brief.schema v1.0 valide (brief_id, angle_id, audience_slug, product_slug, creative_format, intent_mix, status, created)

**CRITICAL** · brief artifact lives in `brands/{slug}/briefs/{BRF-NN}.md` (canon path v2.42+). Si produce-copy-brief écrit ailleurs (legacy path `produced/copy-briefs/`), normaliser en post-Phase 2 avant Phase 3 gate.

**While brief generates**, l'agent reste en silence (operator a déjà la chairman announce de Step 0). Pas d'idle prose.

**When brief returns**, surface le rendu markdown brief à l'operator (full content), suivi du gate Phase 3.

---

## Step 3 · Operator gate validate (inline)

**CRITICAL** · binary gate, ne JAMAIS push aux variants sans confirmation operator.

Surface le brief markdown rendered (no JSON, no field paths). Suivi de ·

AskUserQuestion · *"Brief posé · BRF-NN sur angle {nom angle court}. On lance {N} variants visuels là-dessus, ou tu veux ajuster avant ?"*

Options ·
- **Confirme · go variants** → proceed Phase 4
- **Ajuste {section}** → loop Phase 2 avec adjustments (max 2 retries, sinon escalate)
- **Stop · je révise** → exit pipeline, brief reste persisté en `status: draft`

Si ajustement demandé sur dimension spécifique (audience pain anchor, intent_mix, CTA register, format) → repass produce-copy-brief avec override input + diff signal en patch_notes du nouveau brief.

---

## Step 4 · Delegate to `compose-creative` × N variants

**CRITICAL** · spawn N sub-agents en parallèle si `N ≤ 3` et load permet (Task tool max 5 parallel). Si `N > 3` OR endpoint nano-banana-2 saturated, séquentiel avec stagger.

Per variant ·
- `model: opus` (per compose-creative frontmatter)
- `subagent_safe: true` verified
- Input · brand_slug, angle_id, audience_slug, brief_id (BRF-NN référence), product_slug, variant_axis (default rotation · hook · mécanique · format), composite_mode (`layered` si visual_identity canonical packshot dispo, sinon `full_regen`)
- Expected output · creative artifact persisté `brands/{slug}/creatives/{CRT-NN}.json` + `.jpg` + `.md` (brief copy fiche v5 forward, compose-creative HR3 step 5)

**Diversité variants** · imposer rotation sur axes pour éviter clones ·
- Variant 1 · hook A × mécanique principale × format Meta 4:5
- Variant 2 · hook B × mécanique secondaire × format Meta 4:5
- Variant 3 · hook A × mécanique principale × format Meta 1:1 (alt ratio)

Operator override possible · *"genre 2 variants sur même hook, 1 sur hook alternatif"* → passer variant_axis explicite.

**While composing**, surface heartbeat ligne courte tous ~60s · *"variant 1 rendered... variant 2 en cours..."*. NE PAS dump intermediate output.

**When all N return**, normaliser paths absolus pour synthesis Phase 5. Si un variant a failed (endpoint exhaust) · log gap, continue avec N-1 variants, surface en synthesis.

**Compositional cartography link** · les variants composent CONTEXTE × MODIFIEURS de l'équation v3.1 sur le NOYAU encodé par le brief. Cf `docs/system/compositional-cartography.md` §3.

---

## Step 5 · Synthesis 5 sections (investigation-posture compliant)

**CRITICAL** · output opérateur-facing structuré 5 sections explicites per `docs/system/investigation-posture.md`. JAMAIS dump raw paths sans framing métier. JAMAIS clore sans question macro.

**Observé** · 2-3 lignes · brief {BRF-NN} généré sur angle {nom court angle}, N variants créa produits avec paths absolus opérateur-language ·
- Brief · `brands/{slug}/briefs/{BRF-NN}.md`
- Variants · `brands/{slug}/creatives/{CRT-NN}.{jpg,md}` × N

**Déduit** · hypothèses ranking variants confidence chain (forte / moyenne / faible) basé sur ·
- Ranking interne mécaniques (creative-mechanics-registry score per variant)
- Heuristiques · alignment hook × audience pain density · clarté CTA × intent_mix · packshot fidélité (layered vs full_regen)
- 1 reco · *"Variant {N} a la mécanique la plus dense sur cette audience (confidence moyenne). Probablement le premier à tester."*

**Inconnu** · variables non testables sans live ·
- CTR réel par variant
- Conversion downstream landing
- Audience response (saturation, fatigue, hook resonance)
- Cost per result vs benchmark Meta

**Leviers** · drill-down options · 
- Test live Meta Ads · setup A/B sur N variants, budget 50€/jour × 3 jours minimum signal
- `recompose-creative` · si un variant proche-mais-pas-tout-à-fait, l'adapter sans repartir de zéro
- `decompose-ad` · reverse-engineer concurrent benchmark sur même angle pour calibrer
- Itération brief · si signal live faible, ajuster brief upstream avant relancer variants

**Distribution fork (canon `docs/system/brief-distribution-doctrine.md` · v1.4.0)** · avant de rédiger le Close ouvert, résoudre silencieusement l'outil de centralisation de l'opérateur · cascade canon : `operator/connected-sources.json` + `brands/{slug}/connected-sources.json` (type `crm`/`custom`, capability `write`) → table Ecosystem du `CLAUDE.md` brand → clés `credentials.env` → MCP session réellement vérifiés. Intégrer le résultat au Close ouvert, 1 ligne max :

- **Outil détecté et connecté** → l'outil est nommé dans la question macro : *"on envoie en test live ces {N} variants, et j'en profite pour pousser le brief + les rendus dans ton Notion, base Créas ?"*. Push après confirmation explicite uniquement, jamais silencieux. `brands/{slug}/briefs/` + `creatives/` restent la source de vérité après push.
- **Rien détecté, question jamais posée pour cette brand** → UNE ligne proactive en fin de Close ouvert : *"au passage, tu centralises tes briefs et créas quelque part : Notion, ClickUp, autre ? je peux m'y brancher"*. Réponse positive → `connect-source`. Réponse négative → persist `brands/{slug}/config.json#preferences.brief_distribution: "workspace_only"`, jamais re-posée.
- **Route B reste ouverte post-pipeline** · le pipeline a déjà matérialisé la Route A (brief → variants gatés). Si un format sort du bras de génération (vidéo tant que le bras vidéo n'est pas câblé, prod partenaire), proposer l'export Route B : brief markdown + push outil + message d'accompagnement court.

**Close ouvert** · UNE question opérateur arbitre ·

> *"On envoie en test live ces {N} variants, ou on raffine d'abord variant {Z}, ou on génère {M} additional variants sur angle alternatif ?"*

**NEVER** clore sur affirmative sans question. **NEVER** menu hardcoded (a)/(b)/(c)/(d). Question rédigée selon contexte specific de la session. **NEVER** bloquer la synthesis 5 sections ni la livraison des artifacts sur la distribution. **NEVER** menu d'outils · la proposition de distribution vit dans le Close ouvert, fondue dans la question macro unique.

---

## Guardrails

- **NEVER** ré-implémenter produce-copy-brief OR compose-creative logic. Si bug sub-skill, fix là-bas, pas ici.
- **NEVER** skip Phase 3 gate. Push direct aux variants sans validation operator = violation contrat.
- **NEVER** dump raw sub-agent output verbatim. L'orchestrateur est la synthesis layer.
- **NEVER** expose `BRF-NN`/`CRT-NN`/`ANG-NN` en chairman announce ouverture. OK en synthesis Phase 5 (operator a vu les artifacts).
- **NEVER** parallel >5 variants (Task tool cap). Si operator demande >5, batch séquentiel.
- **ALWAYS** surface gap si voc density faible AVANT Phase 2 (anti-pattern · brief générique downstream).
- **ALWAYS** persister state pipeline en `brands/{slug}/session-state.md` après chaque phase (crash resumption).
- **ALWAYS** rebuild brand snapshot post-Phase 4 (`python3 .skills/build-brand-snapshot.py {slug}`) si writes sur core entities propagated.
- **ALWAYS** investigation-posture 5 sections en synthesis. Pas optionnel.
- **ALWAYS** close ouvert avec UNE question macro contextualisée. Pas de menu plat.

---

## Cross-refs

- **Master doctrine** · `docs/system/contextual-intelligence.md` (two-tier rule, no orphan output)
- **Investigation Posture** · `docs/system/investigation-posture.md` (5 sections output mandatory)
- **Compositional Cartography** · `docs/system/compositional-cartography.md` §3 équation v3.1 (NOYAU × CONTEXTE × MODIFIEURS)
- **Skill Routing Discipline** · root `CLAUDE.md` §Skill routing canon v2.55 (mapping output → skill)
- **DRGFP** · `docs/system/dependency-resolution-protocol.md` (Step 0 prerequisite check L1/L2/L3)
- **Sub-skills** · `produce-copy-brief` SKILL.md (Phase 2 producer) · `compose-creative` SKILL.md (Phase 4 producer)
- **Parent pattern** · `onboard-brand` SKILL.md (Step 4-5 gate validate then push pattern)
- **Confidence propagation** · `docs/system/confidence-propagation.md` (cascade confidence cross-skill orchestrator)
- **Brand isolation** · `docs/system/brand-isolation-doctrine.md` (`isolation_scope: brand_only` enforcement)
- `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW (extension_hooks + manifest registry scan canon)
- `scaffold-extension` v1.2.0+ Phase 9 register-and-flag (upstream registry NEW entities)
