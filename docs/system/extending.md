# Extending PhantomOS

How an operator adds custom entities, sidecar schemas, custom skills, and external pipeline integrations without breaking the coherence of the workspace. This document defines the extension layer, its primitives, and the rules that keep extensions interoperable with the core.

PhantomOS V1 ships with seven entities per brand (brand, product, offer, audience, angle, learnings, strategy) and a set of core skills. An operator who wants to encode competitor ad tracking, deeper financial cohorts, real-time scraped data, contacts network, commercial pipeline, freelances roster, home automation devices, personal admin trackers, or any other domain-specific concept must not hack around the workspace. The extension layer gives them a canonical way to add their own layer while keeping the core stable and the whole workspace legible.

## Three scopes

Extensions live at three scopes. The scope determines where the extension lives on disk, what it cross-references, and which skills consume it.

| Scope | Path root | What it encodes | Examples |
|---|---|---|---|
| **brand** | `brands/{slug}/custom/{type}/` | Anything specific to one mission. The extension is scoped to that brand's lifecycle. | competitor tracking, cohort financials for that product line, mission-specific creative tests, anything attached to the brand and its lifetime |
| **operator** | `operator/extensions/{type}/` | Anything transversal to the operator's life and activities, hors-mission. Lives at the operator layer, agnostic of any specific brand. The operator decides the breadth (work, personal, family, home, learning, health, hobby, admin, civic, anything they want their assistant to compose on). | contacts network across all registers (pro, perso, famille, mentor, voisinage, partenaires hobby), opportunities en cours quel que soit le registre, prestataires récurrents (freelances, artisans, professionnels de santé), side projects et hobbies, domotique et gestion domicile, suivi santé, suivi lecture / apprentissage, finances perso, admin perso, créatif |
| **workspace** | `resources/extensions/{type}/` | Anything shared cross-brand, transversal across every mission the operator runs. The extension is part of the operator's reusable canon. | méthodologies écrites par l'opérateur, registres de patterns observés cross-brand, benchmark tables, taxonomie de tags partagée, n'importe quoi qui s'applique à plusieurs marques |

A type can coexist at multiple scopes. Example `vendors` (prestataires que l'opérateur réutilise, peu importe le domaine, freelances pro autant qu'artisans ou professionnels de santé) :

- **operator scope** = tous les prestataires identifiés à un moment, tous registres confondus (pro et perso)
- **brand scope sur une mission donnée** = le sous-ensemble engagé sur cette mission spécifique, avec contexte mission

L'agent croise les scopes quand pertinent. Tu lui demandes *"qui dans mon réseau pourrait m'aider sur ce sujet"*, il regarde vendors operator-scope (qui je connais ?) et vendors brand-scope sur la mission active si applicable, propose l'intersection. Pareil pour un sujet perso : *"qui je connais qui s'y connaît en X"* fait la même mécanique sans aucun scope brand impliqué.

PhantomOS ne refuse pas ce que l'opérateur veut encoder. L'opérateur décide souverainement ce qui mérite d'être systématisé dans son assistant. Le critère c'est si l'opérateur veut que l'agent compose avec cette dimension, pas si le système juge la dimension légitime ou non. Domotique, suivi santé, hobbies, admin perso, gestion famille, n'importe quoi.

## The four extension primitives

### 1. Custom entities

A new data type, scoped to one of the three scopes (brand, operator, workspace), lives at the corresponding path root.

- **brand scope** : `brands/{slug}/custom/{entity_type}/`. Examples : `brands/northsense/custom/competitor_ads/`, `brands/{slug}/custom/financial_cohorts/`, `brands/{slug}/custom/{anything_specific_to_that_mission}/`.
- **operator scope** : `operator/extensions/{entity_type}/`. Examples : `operator/extensions/contacts/`, `operator/extensions/opportunities/`, `operator/extensions/vendors/`, `operator/extensions/projects/`, `operator/extensions/home/`, `operator/extensions/health/`, `operator/extensions/learning/`, `operator/extensions/admin/`, ou n'importe quoi d'autre que l'opérateur décide d'encoder.
- **workspace scope** : `resources/extensions/{entity_type}/`. Examples : `resources/extensions/personal_method_canon/`, `resources/extensions/cross_brand_benchmarks/`.

Each custom entity type ships with:
- One `schema.json` declaring the JSON Schema for instances of this type.
- Data files, one per instance (`{instance_slug}.json`) or one aggregate file, depending on the shape of the data.
- A short `README.md` explaining what this entity is, why it exists, and which core entities it cross-references.

The core does not need to know about custom entities. They are discovered via convention by `query-context`.

### 2. Sidecar schemas

Extends a core entity with additional fields without modifying the core schema. Example: `brands/{slug}/brand.extensions.json` adds financial fields that the operator needs but which do not belong in the universal `brand` entity. The agent reads the sidecar alongside the core file and treats both as a single logical entity at read time.

Sidecars are **append-only with respect to the core schema**. They add fields, never override or remove. The core `brand.json` stays stable, the operator builds on top. This applies to every core entity (brand-scope sidecars : `brand.extensions.json`, `{product_slug}/spec.extensions.json`, `{audience_slug}/profile.extensions.json`, and so on) and to the operator profile (operator-scope sidecar : `operator/profile.extensions.json` extends `operator/profile.json` with fields you want about yourself that do not belong in the universal profile schema).

**Sidecars are discovered by convention, not registered in `index.json`.** The agent walks each core entity file and checks for a matching `.extensions.json` sibling. If present, it reads both as a single merged view. This differs from custom entities, which require explicit `index.json` registration. The rule: custom entities are new types (registered), sidecars are extensions of existing types (convention).

**Worked example.** A DTC operator wants to track `contribution_margin_by_channel`, `supplier_lead_time_days`, and `price_elasticity_last_measured` per brand. None belong in the universal `brand.json`. The operator creates `brands/{slug}/brand.extensions.json`:

```json
{
 "_version": "1.0",
 "_schema": "brand.extensions",
 "_extends": "brand",
 "_field_types": {
 "contribution_margin_by_channel": "derived",
 "supplier_lead_time_days": "stated",
 "price_elasticity_last_measured": "derived"
 },
 "contribution_margin_by_channel": {
 "meta_ads": 0.42,
 "google_ads": 0.48,
 "email": 0.67,
 "organic": 0.71
 },
 "supplier_lead_time_days": 35,
 "price_elasticity_last_measured": {
 "value": -1.2,
 "observed_at": "2026-04-01"
 }
}
```

The agent now reads `brand.json` + `brand.extensions.json` as a single merged view. Skills that know about the extended fields use them; skills that do not continue to operate on the universal `brand.json` untouched.

### 3. Custom skills

Operator-built skills live in `.skills/skills/custom/{skill_name}/SKILL.md`. They follow the same frontmatter conventions as core skills (`type`, `recommended_model`, `subagent_safe`, `permissions`) and the same rules (mutation through `write_to_context`, voice canon, one question per turn). The only difference is namespace and the fact that they are not maintained by the core template.

Custom skills can read core and custom entities. They can also read sidecar schemas. They follow the same model routing rules as core skills.

### 4. External pipeline integrations

Scrapers, watchers, scheduled jobs, third-party API pulls, any code that brings external data into the workspace. Implemented as custom skills that execute the pipeline (via subprocess, MCP call, or inline code) and write the output into custom entities through the mutation gate. The pipeline is a skill like any other from the agent's perspective; what makes it a pipeline is that its output is a data capture, not a reasoning output.

## The three governance rules

For extensions to stay **interoperable, discoverable, and usable across time**, three rules are non-negotiable.

**Rule 1 · Declared schema.** Every custom entity and sidecar ships with a JSON Schema following the canon conventions of the core: `_version` field, `_schema` identifier, `_field_types` metadata, explicit required fields. `validate-resources` refuses extensions that do not comply. Without a schema, the extension is opaque to the agent and to other skills.

**Rule 2 · Registered or discovered.** Every **custom entity** adds an entry to `index.json → extensions[]`, the central registry. This makes it discoverable to the agent through `query-context` and visible when the operator asks *"what does this brand encode beyond the core?"*. **Sidecars** (`{entity}.extensions.json`) are discovered by convention, the agent walks core entity files and reads the sibling sidecar automatically if present. Unregistered custom entities are invisible to the agent, which defeats the point. Missing sidecars are silently ignored by design, which is the correct behavior.

**Rule 3 · README documenting purpose and cross-references.** Every extension carries a short README explaining what it is, why it was added, which core entities it references, and which skills consume it. This is editorial discipline, not ceremony. Without the README, the extension becomes technical debt for the operator's future self.

## How to add an extension · the canonical path

In V1 the operator performs the four steps manually. A complete copy-paste-ready example lives at `brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing/`, clone it as a starting point.

1. **Create the folder** `brands/{slug}/custom/{entity_type}/` with `schema.json`, data files, and `README.md`. Use `_EXAMPLE/competitor_pricing/schema.json` as a canon-compliant reference; adjust fields to your domain.
2. **Register in `index.json`**, add an entry under the `extensions` section (see format below).
3. **Validate via `validate-resources`**, ask the agent *"validate"* or *"check the workspace"* in natural language; the agent invokes the skill and reports any canon violation.
4. **If a skill is needed** to populate or query the extension, create it under `.skills/skills/custom/` following `.skills/how-to-build-skills.md`.

### Registering a custom entity in `index.json`

`index.json` is the central registry of the workspace. It has a top-level structure with `resources`, `stats`, `id_prefixes`, and `extensions`. The `extensions` array lists every custom entity type, with its scope, schema pointer, cross-references to core entities, and the skill that owns it (if any). Add an entry once per entity type, not per instance.

**Top-level `index.json` skeleton** (relevant sections only):

```json
{
 "_version": "1.0",
 "resources": [ /* shared resources, see architecture.md § Registry */ ],
 "stats": { /* auto-maintained by validate-resources */ },
 "id_prefixes": { /* auto-maintained */ },
 "extensions": [
 /* entries appended below */
 ]
}
```

**Extension entry format** (one per entity type) :

```json
{
 "extensions": [
 {
 "type": "competitor_pricing",
 "scope": "brand",
 "schema": "brands/{slug}/custom/competitor_pricing/schema.json",
 "cross_refs": [
 "product_slug → brands/{slug}/products/{product_slug}/spec.json"
 ],
 "owner_skill": "custom:scrape-competitor-pricing",
 "registered_at": "2026-04-19"
 },
 {
 "type": "contacts",
 "scope": "operator",
 "schema": "operator/extensions/contacts/schema.json",
 "cross_refs": [
 "brand_refs → brands/{slug}/",
 "activity_refs → operator/extensions/{type}/{slug}.json"
 ],
 "owner_skill": null,
 "registered_at": "2026-04-27"
 }
 ]
}
```

Fields :
- `type` : machine-readable name of the entity type. Must not collide with a core entity (`brand`, `product`, `offer`, `profile`, `learnings`, `strategy`).
- `scope` : `brand` (per-brand instances), `operator` (transversal to the operator, hors-mission), or `workspace` (cross-brand shared canon).
- `schema` : path to the JSON Schema file. Resolves under `brands/{slug}/custom/` for brand scope, under `operator/extensions/` for operator scope, under `resources/extensions/` for workspace scope.
- `cross_refs` : declare dependencies on other entities so `validate-resources` can detect broken refs on rename or delete. Operator-scope cross-refs can target brands, other operator extensions, or workspace resources.
- `owner_skill` : the skill that populates this entity. `null` if operator-maintained manually. Uses `custom:` prefix for custom skills, plain name for core skills.
- `registered_at` : date string.

### Writing to custom entities

All writes to custom entities go through the mutation gate, exactly like core entities. The field path convention varies by scope :

- **brand scope** : `custom.{entity_type}.{instance_slug}.{field_name}` (resolves to `brands/{active_slug}/custom/{entity_type}/{instance_slug}.json`)
- **operator scope** : `operator.{entity_type}.{instance_slug}.{field_name}` (resolves to `operator/extensions/{entity_type}/{instance_slug}.json`)
- **workspace scope** : `workspace.{entity_type}.{instance_slug}.{field_name}` (resolves to `resources/extensions/{entity_type}/{instance_slug}.json`)

Example invocation inside a custom skill (brand scope) :

```
write_to_context(
 field_path="custom.competitor_pricing.nike-airmax-97.observations[]",
 value={observed_at: "2026-04-19T10:00:00Z", price: 189.99, currency: "EUR"},
 source="scraper:nike.com",
 confidence=0.95,
 mode="direct"
)
```

Example invocation (operator scope) :

```
write_to_context(
 field_path="operator.contacts.marc-dubois.touch_history[]",
 value={observed_at: "2026-04-27T14:30:00Z", channel: "email", note: "discussion sur sa lecture en cours"},
 source="operator",
 confidence=0.95,
 mode="direct"
)
```

`mode="direct"` writes straight to the file (appropriate for scraped factual data). `mode="proposed"` requires operator review before landing (appropriate for derived or uncertain data). See `docs/system/agent-contracts.md` for full mutation rules.

**Writing to a sidecar** follows a parallel convention. Sidecars target a core entity explicitly via `_extends` and use the core entity name as the path root:

```
write_to_context(
 field_path="brand.extensions.contribution_margin_by_channel.meta_ads",
 value=0.42,
 source="derived:shopify_costs_meta_attribution",
 confidence=0.85,
 mode="direct"
)
```

The agent resolves `brand.extensions.*` to `brands/{active_slug}/brand.extensions.json`. Same pattern for `spec.extensions.*`, `profile.extensions.*`, `offers.extensions.*`, `strategy.extensions.*`, `learnings.extensions.*`.

### Running `validate-resources` on extensions

The operator triggers validation in natural language, *"validate"*, *"audit the workspace"*, *"check this brand"*. The agent invokes the `validate-resources` skill which walks:

- Core entity files against core schemas in `resources/schemas/`.
- Every custom entity under `brands/*/custom/*/` against its declared `schema.json`.
- Every sidecar file `{entity}.extensions.json` against its `_extends` target.
- The `index.json` extensions section for orphan entries or broken cross-refs.

Output: `0 critical / N major / M minor / K info`. Major or critical means the extension is not in valid state and should be fixed before the agent consumes it.

### `scaffold-extension` · orchestrator (shipped V1.5)

A single monolithic skill cannot handle everything an extension requires, business coherence across tags, naming discipline, cross-reference validation, schema canon enforcement, and data safety. Attempting it in one skill produces either a skill that misses edge cases or a skill too vague to validate.

`scaffold-extension` is an **orchestrator** composing nine single-responsibility sub-skills, each with a clear type and bounded permissions:

| Sub-skill | Responsibility | Type |
|---|---|---|
| `analyze-extension-intent` | Capture operator intent, extract attributes (data type, source, frequency, cross-references). Three focused questions maximum. | curator |
| `check-existing-coverage` | Walk five dimensions in order (core entities, active-brand sidecars, active-brand custom entities, sibling-brand custom entities, shared resources). Return a verdict: `route-to-*` (halt, write into existing), `partial-reuse` (scaffold with cross_refs), or `genuinely-new` (full scaffold). Blocks semantic duplication. | curator |
| `propose-schema-draft` | Compose a JSON Schema draft following canon conventions, pulling patterns from `resources/schemas/`. | producer |
| `validate-naming` | Verify naming, no collision with core entities, no duplicate with existing extensions, kebab-case, MECE with what exists. | curator |
| `check-cross-refs` | Identify the core entities the extension must reference. Validate that referenced IDs resolve. Prevents broken refs at creation. | curator |
| `validate-schema-canon` | Validate the draft against conventions (`_version`, `_schema`, `_field_types`). Reuses `validate-resources check 13b` logic. | curator |
| `scaffold-entity-files` | Write the extension's physical files (schema.json, README.md, optional example instance in brand workspace) or the sidecar file. Writes to `brands/{slug}/custom/` or `brands/{slug}/{entity}.extensions.json`. Never touches `.skills/`. | curator |
| `scaffold-skill-stub` | Conditional step: if the operator's intent includes a populating skill, generate a SKILL.md stub in `.skills/skills/custom/`. Builder typology because it writes into the meta-OS namespace. | builder |
| `register-and-flag` | Register the custom entity in `index.json → extensions[]` and add an adoption todo to the brand. Sidecars skip index registration (convention-discovered). | curator |

The orchestrator runs them in sequence with operator-visible checkpoints between each. At any checkpoint, the operator can refuse, adjust, or let it continue.

### How safety is enforced

Three protection layers against breaking existing data:

1. **Mutation gate**, every write passes through `write_to_context()`. No silent JSON edits.
2. **Sidecar-only extensions**, core schemas are never modified; extensions are additive through sidecars.
3. **Upstream validation**, `check-cross-refs` and `validate-schema-canon` run **before** `scaffold-entity-files` and `scaffold-skill-stub`. If a conflict or schema violation is detected, the orchestrator halts before writing anything. A malformed schema never lands.

### Two modes of invocation

`scaffold-extension` accepts both sides of the operator's reality:

- **Intent-first** · operator brings an intention, no data in hand. *"Je voudrais tracker mes concurrents Meta dans le temps."* The skill creates the structure (schema, folder, README, optional populating skill stub), empty. Operator populates later.
- **Data-first** · operator brings a concrete data block from their operational work (analysis, report, structured extraction). *"Voici ma marge de contribution par channel sur Q1, range-la proprement dans ma brand."* The skill parses the data, applies the five-dimension gate, then either routes to the existing encoding (no scaffold, write into existing) or scaffolds and populates with the provided data in a single flow.

The five-dimension gate (`check-existing-coverage`, Phase 2) is the pivot in both modes. Match against existing encoding wins over scaffolding new. Scaffold is the last resort, not the default.

### How to invoke

Three entry points, in increasing specificity:

- **Main agent orchestration gate** (first line) · every build intent, whether scaffold or skill, passes through the main agent's orchestration gate first (see root `CLAUDE.md § Orchestration gate`). The gate applies the five-dimension check via the `check-existing-coverage` logic. If an existing structure already covers the intent, the main agent routes there and no scaffold happens. Scaffold is the last resort, not the default.
- **Direct invocation** · operator explicitly says *"scaffold un tracker pour mes concurrents Meta"*, *"crée une extension pour mes cohortes financières"*, *"ajoute un sidecar à ma brand pour le supplier lead time"*. Even with explicit intent, `scaffold-extension` Phase 2 (`check-existing-coverage`) still runs as a safety gate. Operator can override if the gate finds a match but they have a reason to duplicate.
- **Via `build-agent` delegation** · when `build-agent` analyzes an intent in Step 2b and detects the request maps to a simple extension (custom entity + optional populating skill, or a sidecar), it delegates to `scaffold-extension`. `build-agent` keeps the general architecture role; `scaffold-extension` is the specialist for the extension canonical path. Both go through the five-dimension gate before any write.

### Live execution pattern

The orchestrator runs inline in the main session (subagent_safe: false). Each of the nine phases surfaces a checkpoint to the operator where relevant. Halt conditions at every phase: operator refusal, validator blocker, unresolved cross-reference. On halt, no files are written, the workspace remains in its previous state.

The canonical reference for what the output looks like is `brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing/`. Cloning that example manually is still supported for operators who prefer the manual path.

## Worked example · competitor ad tracking

An operator wants to track competitor Meta ads with screenshot, detected angle, first-seen date, and perceived effectiveness score.

**Step 1.** Create `brands/{slug}/custom/competitor_ads/` with:
- `schema.json` declaring fields (`ad_id`, `competitor_brand`, `screenshot_path`, `detected_angle`, `first_seen`, `effectiveness_score`, `notes`, standard `_version`/`_schema`/`_field_types`).
- `{ad_id}.json` files as instances drop in over time.
- `README.md` explaining the purpose and that `detected_angle` cross-references `resources/registries/angle-registry.md`.

**Step 2.** Register in `index.json` under a new type `competitor_ads`, with schema pointer.

**Step 3.** Create a custom skill `.skills/skills/custom/scrape-competitor-ads/SKILL.md` that pulls from Meta Ads Library, applies the angle classifier from `angle-registry.md`, and writes entries through `write_to_context()`.

**Step 4.** Add to brand `todos.md` a recurring note to review newly captured ads weekly.

The core `brand.json` is untouched. The `angle-registry.md` is referenced, not duplicated. The agent can now be asked *"show me this week's new competitor ads on Northsense"* and it resolves the query through `query-context` without the core needing to know what a competitor ad is.

## What the extension layer is not

**Not a fork.** Operators do not fork the core schemas to add fields. That breaks cross-brand compatibility. Use sidecars instead.

**Not a place for throw-away state.** Session state, temporary outputs, scratch work belong in `sources/` or `_tmp/`, not in custom entities. Custom entities are for structured, persistent, schema-validated data.

**Not a way around `write_to_context`.** All writes to custom entities follow the same mutation gate as core entities. No direct JSON editing. The mutation rule is universal.

## Promotion path · when an extension graduates to core

Some extensions prove valuable enough across multiple brands that they should no longer be custom. When an operator (or the wider ecosystem, once extensions are shared) ships the same custom entity type three or more times, it becomes a candidate for promotion to a vertical pack or to the core itself. The promotion process is not automated in V1, it goes through a manual review: the pattern is codified into `resources/schemas/` as a shipped schema, existing custom instances migrate, skills are updated to treat the former extension as first-class. This path mirrors the promotion from brand-level learnings to shared resources, but at the data-type level.

## V1 known limits · honest flags

The extension layer ships production-ready for V1 with the following known limitations. Each is documented, bounded, and on the roadmap.

**Runtime integrity checks are partial.** `validate-resources` enforces schema canon, naming, and index coherence at write time. It does **not** yet detect:
- Cross-ref rot when a core entity (product, audience) is renamed or deleted and custom entities still reference the old slug. Runtime check planned V1.x.
- Sidecar semantic divergence when a sidecar field contradicts a core field (e.g., `pricing_currency = "EUR"` in core, `financial_currency = "USD"` in sidecar). Currently flagged by operator review, not automated check.
- Schema version drift when the core template upgrades and existing custom extensions still point to an older `_version`. Migration framework planned V1.x.

**Concurrency is operator-responsibility.** Two parallel sessions writing to `index.json` or to the same custom entity can race. File locking via `write_to_context` is on the V1.x list · until then, avoid multi-session simultaneous edits on the same brand.

**Mutation gate is convention, not enforcement.** A custom skill that writes directly to JSON files bypasses `write_to_context` without detection. Hash-based audit tooling to flag bypasses is planned. Until then, rely on skill authoring discipline (see `.skills/how-to-build-skills.md`).

**No cross-workspace shared extension registry.** Extensions are local to each workspace. Two operators who independently build a `competitor_ads` extension with divergent schemas will fragment. V2 introduces a shared extension registry; until then, use the promotion path to `resources/` when a pattern stabilizes on three or more brands in one workspace.

**Scale threshold.** Query performance is acceptable through roughly five brands × three extensions per brand in one workspace. Beyond that, a dedicated index-inverted lookup is needed. Signals that the threshold is hit: `query-context` latency climbs or context budget saturates on cross-brand queries. Planned V1.x.

**Skill trigger collisions.** Past twenty-plus custom skills, the harness trigger-matching becomes non-deterministic when two skills declare overlapping trigger phrases. Namespacing (`custom:skill-name`) is planned. Until then, keep custom skill count bounded and triggers specific.

## Position post-v2.75.0 · NEW canon paths (SUPERSEDED legacy)

À partir de v2.75.0, le registry extensions canon n'écrit PLUS dans `index.json → extensions[]` (legacy convention v2.0+). NEW canon paths · `_extensions.json` scope-routed per scope ·

- **brand scope** · `brands/{slug}/_extensions.json`
- **operator scope** · `operator/_extensions.json`
- **workspace scope** · `resources/_extensions.json`

Schema canon · `resources/schemas/extensions-registry.schema.json` v1.0.

NEW field canon · `consumable_by` enum (orchestrateurs production v2.75.0 · build-atlas-complete · score-matrix · produce-paid-matrix · creative-brief-composer) qui permet auto-discovery via extension_hooks frontmatter + Step 0 DRGFP Manifest Registry Scan dans orchestrateurs production.

Doctrine canon NEW v2.75.0 · `docs/system/extension-discovery-doctrine.md`.

**Legacy `index.json → extensions[]`** · SUPERSEDED v2.75.0. Backward compat preserved en lecture pendant transition (register-and-flag v1.1.0 fallback read si NEW canon absent ET legacy present). Forward writes uniquement vers NEW canon paths. Migration manuelle legacy → NEW canon · backlog v2.76+ si opérateur a entries legacy persisting.

## Related canon

- `lexicon.md § Method · the encoding discipline`, definitions of extension, custom entity, sidecar schema, core vs custom namespace.
- `docs/system/architecture.md` · the core data model the extension layer builds on.
- `docs/system/patterns.md § Skill Taxonomy` · classification rules that apply equally to custom skills.
- `docs/system/voice.md` · writing conventions that custom skill authors follow.
- `.skills/how-to-build-skills.md` · authoring guide used for both core and custom skills.
- `docs/vision/roadmap.md` · `scaffold-extension` builder skill and external pipeline formalization are on the R&D list.
