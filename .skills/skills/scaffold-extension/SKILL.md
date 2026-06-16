---
name: scaffold-extension
type: orchestrator
version: "1.3.0"
recommended_model: sonnet
patch_notes:
  v1.3.0: "v2.75.0 Phase 9 register-and-flag enrichie · NEW consumable_by field auto-detection · scaffold-extension v1.3.0+ register NEW entity avec liste enum orchestrateurs production consommables (creative-brief-composer · score-matrix · produce-paid-matrix · build-atlas-complete) selon entity_type + scope + data_shape · operator validation gate AskUserQuestion accept OR adjust manually. Cross-ref doctrine canon extension-discovery-doctrine.md v2.75.0 NEW. Backward compat strict additif · consumable_by champ optional · legacy v1.2.0 NEW entities sans consumable_by still registered mais pas auto-discovery (manual patch nécessaire si consumption later)."
layer: meta
reasoning_pattern: null
description: >
  Orchestrator for building a new extension in PhantomOS at one of three scopes (brand, operator, workspace).
  Custom entity, sidecar, or custom skill. The operator decides what mérite d'être encodé,
  peu importe le domaine (pro, perso, famille, hobby, créatif, technique, peu importe).
  Composes nine single-responsibility sub-skills for intent capture, scope detection, schema drafting,
  naming validation, cross-reference checking, canon validation, file scaffolding, and index registration.
  Respects the three governance rules of the extension layer: declared schema, registered-or-discovered,
  README documenting purpose.
  Triggers:
    FR: "crée une extension", "ajoute un custom entity", "scaffold extension", "nouveau type de données",
        "ajoute un sidecar", "track X cross sessions", "scaffold", "extension operator", "extension brand",
        "encoder X côté opérateur", "tracker X dans mon workspace"
    EN: "scaffold extension", "create custom entity", "new data type", "add sidecar",
        "scaffold a tracker for X", "build extension", "operator extension", "brand extension",
        "track X for myself", "encode X for me"
permissions:
  reads: [brand, operator, resource, index]
  writes: [brand.custom, brand.extensions, operator.extensions, operator.profile.extensions, resource.extensions, index, skill.custom, brand.todos, operator.todos]
  mode: direct
  subagent_safe: false
consumes:
  - path: docs/system/scope-extension-doctrine.md
pipeline:
  preconditions: workspace deployed, docs/system/extending.md present, validate-resources skill available
  postconditions: extension registered + validated + operator informed
---

# Skill: Scaffold Extension

Orchestrator for scaffolding a new extension in the workspace, at any of the three scopes (brand, operator, workspace). Covers custom entities, sidecar schemas, and the optional custom skill stub that populates the entity. Composed of nine single-responsibility sub-skills executed in strict sequence, with operator-visible checkpoints between phases.

The skill is **agnostic to the domain** of the extension. The operator decides what mérite d'être encodé : business spécifique à une marque, contacts globaux pro et perso, opportunités, prestataires (freelances, artisans, professionnels de santé), projets perso, domotique, suivi santé, lectures, hobbies, admin perso, n'importe quoi. Le système n'a aucune opinion sur la légitimité du domaine, il scaffolde la structure et l'agent compose dessus.

See `docs/system/extending.md § Three scopes` for the extension layer architecture and the scope routing rules. See `docs/system/patterns.md § Skill Taxonomy` for type definitions.

---

## Invocation context · two modes of entry

**Mode intent-first** · operator apporte une **intention** sans donnée en main. *"Je voudrais tracker mes concurrents Meta dans le temps."* Le skill crée la structure (schema + dossier + README + stub skill optionnel), vide. L'opérateur peuple plus tard.

**Mode data-first** · operator apporte une **donnée concrète** issue de son travail opérationnel (analyse, rapport, extraction structurée). *"Voici ma marge de contribution par channel sur Q1, range-la proprement."* Le skill parse la donnée, applique le gate 5-dimensions, et soit route vers l'existant (pas de scaffold), soit crée la structure ET peuple avec la donnée apportée en un seul flow.

Le gate `check-existing-coverage` en Phase 2 est le pivot. Dans les deux modes, la même logique :

- Si la donnée ou l'intention matche une entité core existante → route vers `.skills/write-to-context.py` sur cette entité, **aucun scaffold**.
- Si match sur sidecar ou custom entity existante → écrit dans l'existant, nouvelle instance ou enrichissement sidecar, **pas de nouveau scaffold**.
- Si match partiel avec un shared resource → scaffold une structure minimale qui cross-ref la ressource plutôt que dupliquer.
- Si genuinely new → scaffold complet. En mode data-first, le scaffold est suivi immédiatement du populate avec la donnée apportée.

**Invocation déclenchée par** :

- Opérateur dit *"scaffold", "crée une extension", "ajoute un sidecar", "range cette donnée", "intègre ce bloc dans mon contexte"*.
- `build-agent` Step 2b détecte un intent de type simple-extension et délègue.
- Main agent orchestration gate (voir `CLAUDE.md § Orchestration gate`) détecte qu'une requête opérateur nécessite soit un enrichissement structurel, soit l'intégration d'une variable opérationnelle.

---

## Pipeline

Execute the nine sub-skills in order. After each phase, surface a one-line status to the operator (unless the phase is silent by design). Halt at any phase if the operator refuses or if a validator returns a blocking error.

### Phase 1 · `analyze-extension-intent`

Capture the operator's intent. Classify three dimensions :

1. **Kind** : custom entity / sidecar / both / skill-only.
2. **Scope** : brand (lié à une mission précise) / operator (transversal à l'opérateur, pro et perso confondus) / workspace (partagé cross-brand). Detect via natural cues :
   - Brand-scope cues : *"sur Northsense"*, *"pour cette mission"*, *"dans cette marque"*, *"sur ce client"*, intent attaché à un brand_slug actif.
   - Operator-scope cues : *"pour moi"*, *"mes contacts"*, *"ma domotique"*, *"mon suivi santé"*, *"mes lectures"*, *"mes prestataires globalement"*, *"mes projets perso"*, intent transversal à l'opérateur sans rattachement à une marque.
   - Workspace-scope cues : *"partagé entre toutes mes marques"*, *"canon perso transversal"*, *"benchmark cross-client"*, intent partagé multi-brand.
   - Ambiguous → AskUserQuestion 2-3 options binaires.
3. **Attributes** : data shape (time-series / instance-per-item / aggregate), expected population mechanism (manual / scraper / derived), cross-references to other entities (core ou autres extensions, n'importe quel scope).

Three focused questions maximum across all three dimensions.

Output: structured intent object consumed by downstream phases. `scope` field locks the path routing for Phase 7 and the registration shape for Phase 9.

### Phase 2 · `check-existing-coverage`

Run the pre-build analysis gate. Walks dimensions in order, scope-aware :

- **All scopes** : core brand entities, shared resources, existing operator extensions, existing workspace extensions.
- **Brand scope additionally** : existing sidecars on the active brand, existing custom entities on the active brand, custom entities on sibling brands.
- **Operator scope additionally** : existing operator sidecars (`profile.extensions.json`).

Returns a verdict :

- `route-to-*` → scaffold halts. The main agent routes the operator to the existing structure. The new extension is not needed.
- `partial-reuse` → scaffold proceeds but Phase 3 schema draft uses the matched references as `cross_refs` or ID pointers rather than duplicating fields.
- `genuinely-new` → scaffold proceeds with full scope.

Cross-scope match awareness : if operator wants `vendors` in operator scope and `vendors` already exists at brand scope on a specific brand, the gate flags this as `partial-reuse` (operator scope is upstream, brand scope can reference operator scope by slug). Vice versa is also detected.

Surface the verdict to the operator with the matched target (if any). Operator can override (force scaffold if they have a reason to duplicate) but the default is respect the gate.

### Phase 2bis · `suggest-domain-canon` (conditional)

**Triggered when** the new extension targets a domain whose canonical methodology is **not yet encoded** in `resources/frameworks/` (e.g. operator asks for an extension on CRO, lifecycle email retention, B2B sales discovery, content SEO methodology · but no `cro-canon.md`, `retention-canon.md`, etc. exists).

**Why this phase exists.** The operator typically does not know the senior references of their own domain · they have a business need, not a bibliography. The agent's role is to identify the 2-3 most recognized canonical references for the domain, propose them as a default suggestion, and encode the canon itself. The operator must never be asked to name the canon · only to validate the agent's recommendation.

**Mechanism.**

1. Identify the domain underlying the operator's request (CRO, retention, sales discovery, etc.).
2. Pre-select the 2-3 canonical references most recognized in that domain (book + author + framework name + year if relevant). Restrict to *referenced senior practitioners with published work* · not generic blog posts. Cross-check via `mine-vom` patterns or hard-coded domain registry if available.
3. Surface to operator via **AskUserQuestion** with a default recommendation + 1 alternative + 1 escape hatch :
   - **Option A (default, agent recommendation)** : *"For [domain], the canonical references are [Author 1] + [Author 2] + [Author 3]. We encode all three as the foundation."*
   - **Option B (lighter scope)** : *"Just [Author 1] + [Author 2], skip the third."*
   - **Option C (operator override)** : *"I have my own framework I want encoded instead."* · operator names their preferred reference.
4. On validation, the agent fetches the publicly accessible material (book summaries, articles, talks, transcripts) via `WebFetch`, extracts the operable principles, structures them in `resources/frameworks/{domain}-canon.md` with traceable IDs (`AUTHOR-001` to `AUTHOR-N`).
5. Operator validates the encoded canon at the end (3-movement prose synthesis) · never asked to source it.

**Halt condition.** If the domain has no recognized canon (emerging field, niche too young), surface honestly : *"This domain doesn't have an established methodology yet. We'll capture your own observations as we go via `learnings.json` and matricize once a pattern emerges."* · fall back to capture-then-matricize, do not invent a canon.

**Output:** `resources/frameworks/{domain}-canon.md` populated and versioned. Operator-facing surface confirms : *"Canon encoded with [N principles from authors]. Skill scaffold continues."*

This phase is **mandatory** when canon is absent and the extension implies methodology-driven reasoning. It is **skipped** when (a) the canon already exists in `resources/frameworks/`, or (b) the extension is purely structural (data-shape only, no methodology underneath).

### Phase 3 · `propose-schema-draft`

Generate a canon-compliant JSON Schema draft for the custom entity (or sidecar). Follows `_version`, `_schema`, `_field_types` conventions. Uses patterns from `resources/schemas/` as structural reference. Integrates the cross-references and reused banks identified in Phase 2 · and the canon encoded in Phase 2bis if applicable (axes drawn from canonical references, not invented).

Operator sees the schema, approves or adjusts.

### Phase 3bis · `produce-decomposition-ecr` (NEW v1.2.0)

Consume the ECR decomposition object produced by `analyze-extension-intent v2.0.0` (Phase 1) plus the schema draft from Phase 3. Render an operator-facing ECR decomposition artifact ·

- Master equation instantiated for the subject `[SUJET] = X × Y × Z` (triptych pattern Strat/Compo/Exé · Funnel · Système · Performance · selon domaine)
- Cartographic matrix proposed (2D grid · axes × values)
- Atomes mesurables identified with associated metrics
- Templates suggérés depuis registry pattern existing (creative-mechanics-registry, angle-registry, proof-registry, frameworks)

Operator validates via AskUserQuestion · A) accept and continue Phase 4 · B) adjust 1-2 dimensions (re-prompt analyze-extension-intent) · C) halt.

**Conditional skip** · if `ecr_decomposition.eligibility.applicable = false` (test d'éligibilité 3 critères fail in Phase 1), this phase is skipped. Scaffold proceeds directly to Phase 4.

**Cross-ref** · `docs/system/operational-system-doctrine.md` (doctrine mère ECR canonisée v2.71).

### Phase 4 · `validate-naming`

Verify the proposed entity type name. Blocks collision with core entity names (see `validate-resources` check 17). Enforces kebab-case, MECE with existing extensions in `index.json`, no duplicate.

If collision detected, propose alternative names and re-prompt.

### Phase 5 · `check-cross-refs`

Walk every declared cross-reference in the schema. Verify target core entities exist in the current workspace. Flag references that cannot resolve. Prevents broken refs at creation rather than at runtime.

Halts if any cross-ref is unresolved; operator must fix or drop the ref.

### Phase 6 · `validate-schema-canon`

Validate the draft schema against canon requirements (reuses logic of `validate-resources` check 16 applied pre-write). Checks `_version`, `_schema`, `_field_types` enum, required fields, no override of core fields for sidecars.

Halts on any schema canon violation.

### Phase 7 · `scaffold-entity-files`

Write the physical files to disk via `.skills/write-to-context.py`. Path routing depends on scope :

**Brand scope :**
- `brands/{slug}/custom/{entity_type}/schema.json` (or `brands/{slug}/{entity}.extensions.json` for sidecar).
- `brands/{slug}/custom/{entity_type}/README.md` (canonical structure : purpose, cross-refs, field conventions).
- Empty or example instance file if requested.

**Operator scope :**
- `operator/extensions/{entity_type}/schema.json` (or `operator/profile.extensions.json` for sidecar on profile).
- `operator/extensions/{entity_type}/README.md`.
- Empty or example instance file if requested.

**Workspace scope :**
- `resources/extensions/{entity_type}/schema.json`.
- `resources/extensions/{entity_type}/README.md`.
- Empty or example instance file if requested.

For sidecars, only the `.extensions.json` file is written (no README, no folder, sidecars are discovered by convention).

### Phase 8 · `scaffold-skill-stub` (conditional)

If the intent includes a skill that populates the extension (common for scrapers, watchers, pipelines), generate a SKILL.md stub in `.skills/skills/custom/{skill_name}/`. The stub declares frontmatter (type, recommended_model, permissions referencing the new extension), a Tone section, and the pipeline skeleton. The operator fills in the execution logic afterward, or delegates to `build-agent` for the body.

Skipped if the operator does not need a populating skill (manual-only tracking, pure sidecar enrichment).

### Phase 9 · `register-and-flag` (enrichie v1.3.0)

Register NEW entity dans manifest workspace · `_extensions.json` (operator scope) OR `brands/{slug}/extensions.json` (brand scope) OR `_manifest.json#extensions` (workspace scope) selon Phase 1 scope.

**9.a · Register entity metadata** (existing v1.2.0)

For custom entities : add an entry to `index.json → extensions[]` via `.skills/write-to-context.py`, with `type`, `scope` (brand|operator|workspace), `schema` path (resolved per scope), `cross_refs`, `owner_skill`, `registered_at`, `entity_id`, `data_shape`, `file_path`. For sidecars : skip (sidecars are convention-discovered, not registered, see `docs/system/extending.md`).

**9.b · `consumable_by` auto-detection (NEW v1.3.0)**

Détermine quels orchestrateurs production peuvent consommer cette NEW entity via discovery hook.

Algorithm auto-detection ·

Q1 · `entity_type` matche quel orchestrateur production canon ?
- `creative_entity` (e.g. video-script · podcast-script · static-ad) → creative-brief-composer · score-matrix · build-atlas-complete
- `audience_entity` (e.g. niche-audience · proxy-audience) → all 4 orchestrateurs
- `angle_entity` (e.g. unique-angle · positioning-variant) → score-matrix · produce-paid-matrix · creative-brief-composer · build-atlas-complete
- `brief_entity` (e.g. brand-brief · creative-brief-variant) → creative-brief-composer · build-atlas-complete
- `territory_entity` (e.g. emerging-territory · niche-territory) → produce-paid-matrix · build-atlas-complete
- `product_entity` (e.g. NEW product type beyond canon spec) → build-atlas-complete
- `friction_entity` (e.g. NEW friction usage pattern) → build-atlas-complete
- `other` → empty consumable_by (operator validation gate manual flag if applicable)

Q2 · `scope` (brand/operator/workspace) limite-t-il quels orchestrateurs ?
- `brand_only` orchestrateurs (score-matrix · produce-paid-matrix · creative-brief-composer) compatible avec entity scope `brand` OU `workspace`
- `cross_brand` orchestrateurs (build-atlas-complete OK toutes scopes)
- `operator` scope entity · limited consume (rare cas spécifique)

Q3 · `data_shape` (instance-per-item / aggregate / time-series) compatible quel pattern orchestrateur ?
- `instance-per-item` · standard · OK all orchestrateurs
- `aggregate` · OK score-matrix · build-atlas-complete (consume aggregates)
- `time-series` · limited consumers · check case par case (default empty consumable_by)

**Output proposed** · liste enum `consumable_by` calculée auto via Q1+Q2+Q3.

**9.c · Operator validation gate (AskUserQuestion)**

Surface à l'opérateur ·

```
══════════════════════════════════════════════════════════════════════
NEW ENTITY · {entity_id} register · consumable_by proposed
══════════════════════════════════════════════════════════════════════

Le système propose que cette NEW entity puisse être consommée
automatiquement par ces orchestrateurs production ·

  ✓ creative-brief-composer (production briefs · variants visuels)
  ✓ score-matrix (scoring audience × angle)
  ✓ build-atlas-complete (pipeline atlas complet)

Tu veux ·
  A · Accepter proposed (3 orchestrateurs auto-consume next invocation)
  B · Ajuster manuellement (sélectionner sous-set OR ajouter autre)
  C · Skip · register sans consumable_by (NEW entity registered mais pas auto-discovery)
```

Operator choice via AskUserQuestion · Path A accept · Path B adjust subset · Path C skip empty.

**9.d · Persist consumable_by dans registry**

Final registry entry ·

```json
{
  "entity_id": "video-script-001",
  "entity_type": "creative_entity",
  "scope": "brand",
  "data_shape": "instance-per-item",
  "consumable_by": ["creative-brief-composer", "score-matrix", "build-atlas-complete"],
  "file_path": "brands/{slug}/custom/video-scripts/{id}.json",
  ...
}
```

Cross-ref doctrine canon · `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW.

**9.e · Flag adoption todos**

Add a flag entry to track adoption of the new extension (first data capture, first query) :

- **Brand scope** → `brands/{slug}/todos.md → ## In Progress`.
- **Operator scope** → `operator/todos.md → ## In Progress` (if absent, scaffold the section).
- **Workspace scope** → `todos.md` at workspace root, section dedicated to extension adoption.

Auto-triggered `validate-resources` runs post-write via the mutation rule in root CLAUDE.md, covering checks 15-18. Silent unless MAJOR or CRITICAL.

---

## Output to operator

After Phase 9 completes successfully, surface a concise recap in operator language. Adapt phrasing to scope :

**Brand scope :**
> *"Ton `{type}` est prêt sur `{brand_slug}`. Forme validée. {N} champs, {N} références vers ton contexte existant. {Un petit skill '{name}' a été ajouté, tu le rempliras avec `build-agent` ou à la main, je peux t'aider maintenant.} Tu peux commencer à l'utiliser en disant `{trigger phrase}`."*

**Operator scope :**
> *"Ton `{type}` est prêt côté opérateur, transversal à toutes tes missions. {N} champs, {N} références prêtes. Tu peux commencer à l'utiliser en disant `{trigger phrase}`."*

**Workspace scope :**
> *"Ton `{type}` est prêt en couche partagée, accessible à toutes tes marques. {N} champs, {N} références prêtes. Tu peux commencer à l'utiliser en disant `{trigger phrase}`."*

Never expose file paths, JSON structure, or internal field names. The operator owns the extension conceptually, not technically.

---

## Halt conditions

- Phase 4 blocking collision without operator-approved alternative
- Phase 5 broken cross-ref without operator-approved drop
- Phase 6 schema canon violation without operator-approved fix
- Operator refuses any intermediate checkpoint

On halt, write nothing. The workspace remains in its previous state. Resume is possible later by re-invoking with the same intent.

---

## Hard rules

- Mutation gate on every write. Never direct JSON edits.
- Schema canon compliance is non-negotiable (checks 16, 17 are CRITICAL severity).
- Operator language throughout. Internal vocabulary (field_path, schema, index.json) never leaks to the operator surface.
- One thread question per turn across all phases.
- Voice canon 100%. No triple-parallel, no coach-phrase, no decorative metaphor.

### HR-consumable-1 · consumable_by auto-detection + operator gate (NEW v1.3.0)

Toute NEW entity registered via scaffold-extension v1.3.0+ Phase 9 DOIT inclure 
`consumable_by` field avec liste enum orchestrateurs production proposés via 
auto-detection (Q1 entity_type + Q2 scope + Q3 data_shape) ET validé par 
operator gate AskUserQuestion (accept · adjust · skip). 

Backward compat · NEW entities scaffolded pré-v1.3.0 (v1.2.0 legacy) sans 
`consumable_by` field still registered fonctionnellement mais pas 
auto-discovery downstream · l'opérateur peut patcher manuellement registry 
entry pour ajouter consumable_by post-hoc.

Cross-ref · `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW.

---

## Related canon

- `docs/system/extending.md` · extension layer architecture, three governance rules.
- `docs/system/patterns.md § Skill Taxonomy` · type definitions.
- `docs/system/agent-contracts.md` · mutation gate rules.
- `brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing/` · canonical reference example.
- `.skills/skills/validate-resources/SKILL.md § Checks 15-18` · post-write integrity checks.
- `.skills/skills/build-agent/SKILL.md` · delegates here for simple extension intents.
- `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW (doctrine canon consumable_by + extension_hooks)
- 4 orchestrateurs production v2.75.0 downstream consumers (creative-brief-composer · score-matrix · produce-paid-matrix · build-atlas-complete)
