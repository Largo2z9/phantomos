# Schema Encoding Doctrine (SED) · Operating Doctrine

> **SED is the substrate sub-doctrine of `contextual-intelligence.md` (CI).** Without rigorous schema encoding, the matrix-driven reasoning of CMR has nothing to range over and the agent's intelligence has no stable ground.

---

## 1. Thesis

> **Encoding rigor is the precondition of every other discipline in PhantomOS.**

A workspace is a knowledge container. The agent reasons over what is encoded in it, entities, fields, sources, vocabulary, lifecycle. If the encoding is sloppy (free-text where enums should be, untracked sources, unversioned schemas, mutations that bypass the gate), every downstream skill inherits the noise. The matrix in CMR cannot select cells correctly when the schema is ambiguous. The recommendations in CI are unreliable when the substrate they rest on is unverifiable. The skills authored under SAD become brittle because the canon they consume drifts session-to-session.

SED names what it takes to keep the substrate clean: typed fields, externalized canon, append-only history, gated mutations, sourcing tags, triangulation, lifecycle hygiene. None of these are individually surprising, they exist scattered across `field-types.md`, `architecture.md`, `extending.md`, hooks, conventions, and the `_field_types` system. SED consolidates them into one named doctrine so that a skill author can ask, "am I encoding this correctly?" and have a single place to check.

---

## 2. The problem SED addresses

Without an encoding doctrine, three kinds of silent failure accumulate:

1. **Sloppy substrate poisons reasoning.** A field tagged `derived` but actually filled by an operator's stated value, an entity referenced by inconsistent slugs, a canon variable inlined in skill prose rather than externalized, each is a small drift. Cumulatively they make the agent's reasoning unreliable in ways that don't surface as bugs but as creeping inconsistency.
2. **Mutations bypass the gate.** A direct `Edit` on a brand JSON skips the audit trail, breaks the proposal/acceptance workflow, and corrupts the event log. The hooks (`mutation-guard.py`, `convention-guard.py`) catch the obvious cases ; without a doctrine that names and explains them, the rules feel arbitrary and accumulate exceptions.
3. **The temporal layer drifts independently of the spatial layer.** Entities (brand, product, audience, offers, learnings, strategy) describe what the brand *is*. But what the workspace has *learned*, *observed*, *captured over time*, events, learnings lifecycle, operator awareness, session traces, is a parallel encoding with its own discipline. Without naming this Memory & Observability sub-corpus inside SED, it falls between the cracks.

SED is the answer: a single doctrine that governs how the substrate gets and stays rigorous.

---

## 3. Two layers of encoding

SED encodes along two orthogonal axes:

**Spatial encoding** · the entities, fields, schemas, vocabularies, sourcing that describe the brand domain at any point in time. Six core entities (brand, product, offer, audience, learnings, strategy) plus extensions (custom entities, sidecars, registries). Versioned per-entity (`_version`), typed per-field (`_field_types`), enumerated where canon allows (closed vocabularies in JSON Schema enums).

**Temporal encoding** · what changes over time, what was observed, what was captured. Append-only logs (`decisions.md`, `learnings.json`, `session-log.md`, `events.jsonl`), operator memory (`/operator/profile.json`, `/operator/awareness.json`), narrative memory (`session-state.md`, snapshots), the three-layer memory system (entity / operator / narrative).

Both layers are SED territory. The spatial layer was historically the focus (the schemas, the field types) ; the temporal layer was scattered. SED consolidates both.

---

## 4. Minimum anatomy

A workspace satisfies SED if and only if it carries the following invariants:

| # | Invariant | Why it is load-bearing |
|---|---|---|
| 1 | **Six core entities + extensions, each with `_version` semver and `_field_types` tagging.** | Without versioning, schema evolution silently breaks consumers. Without `_field_types`, the agent cannot distinguish a fact from an inference, an observation from a declaration. |
| 2 | **Mutation gate non-optional.** Every write to brand/operator JSON goes through `write_to_context(field_path, value, source, confidence, mode)`. Direct `Edit/Write/NotebookEdit` on these files is refused by `mutation-guard.py`. | Bypassing the gate corrupts the proposal/acceptance workflow, skips the audit trail, and breaks the event log. Errors here are silent and persistent. |
| 3 | **Sourcing tags per field.** Every value carries `source` (observed / stated / structured / derived) and `confidence` (or qualitative tier). Auto-tagged from semantic signals at write time. | The operator and downstream skills need to distinguish what was scraped, declared, computed, or inferred. Without sourcing, every field looks equally authoritative. |
| 4 | **Closed vocabularies where canon exists**, enums in JSON Schema, lookup tables in registries, no free-text where a controlled vocabulary applies. | Free-text fields drift across brands and skills. *"rassurant"* in one workspace is *"reassuring"* in another is *"warm-authoritative"* in a third. The agent cannot compose across instances when vocab is open where it shouldn't be. |
| 5 | **Triangulation rule for load-bearing claims.** Any field that affects a downstream decision must be sourced from ≥3 independent inputs (verbatims, observations, operator confirmations) before being treated as canonical. Singletons are flagged as hypothesis. | Without triangulation, one outlier becomes a brand truth. CMR's verbatim-anchor rule depends on this, at the SED layer, sourcing must already be triangulation-aware. |
| 6 | **Append-only logs** for `decisions.md`, `learnings.json`, `session-log.md`, `events.jsonl`. Invalidation is `[SUPERSEDED Sxx]`, never deletion. | Editing history corrupts auditability. The cost of carrying superseded entries is one line of suffix ; the cost of losing the trail is unrecoverable. |
| 7 | **Snapshot / manifest regen post-mutation.** After any write to entity JSONs, regenerate `_snapshot.md` and any derived indexes (`_manifest.json`). Materialized-view pattern, not on-demand recompute. | Operators read the snapshot, not the full JSON tree. If snapshot is stale after a mutation, the operator and the agent operate on different views. |
| 8 | **Validation runtime**, `validate-resources`, `validate-naming`, `validate-all.py` run silently after writes, surface MAJOR/CRITICAL findings, ignore MINOR by default. | Invariants enforced at write-time prevent the workspace from drifting into invalid states. Surfaced selectively to avoid noise. |
| 9 | **Conventions plateforme** declared in `resources/conventions/{platform}.json`. Auto-loaded before any platform interaction. | Each external tool/API has its own conventions (Meta, Klaviyo, Shopify). Encoding them once in versioned conventions prevents skill-by-skill rediscovery. |
| 10 | **Extension layer governance**, custom entities under `brands/{slug}/custom/`, sidecars `{entity}.extensions.json`. Extensions follow same `_version` + `_field_types` rules as core. | Without governance, extensions drift faster than core. Extension layer is the most likely place to violate SED if discipline is not explicit. |

---

## 5. Sub-corpus · Memory & Observability

The temporal layer of SED has its own structure. Three memory layers, never mixed:

**Layer 1 · Entity memory** (`brands/{slug}/`). Spatial encoding. What the brand *is*. Mutated through the gate. Read by skills that produce, audit, recommend.

**Layer 2 · Operator memory** (`/operator/profile.json`, `/operator/awareness.json`). What we know about the *operator using the workspace*. Their identity, role, calibrated register, prior knowledge state, concepts already introduced. Persists across sessions.

**Layer 3 · Narrative memory** (`session-log.md`, `events.jsonl`, `session-state.md`, snapshots). What *happened*. The trail of sessions, mutations, decisions, learnings. Read by `session-search` for cross-session recall.

**Strict separation rule**: layers do not mix. An operator preference does not live in a brand JSON. A brand fact does not live in operator memory. A narrative event does not overwrite either. This separation is what makes the workspace forkable, the operator portable, and the audit trail intact.

**Lifecycle of `learnings.json`** · append-only, with `id / status / superseded_by / genericity / promoted_to`. Promotion path: brand-specific learning → cross-brand pattern → canon candidate. Staleness review at >180 days. `promote-backlog.json` (créé au premier candidat détecté, absent tant qu’aucun) tracks candidates.

**Events log** (`events.jsonl`) · schema includes `actor_id` (operator or agent), `action_type` (mutation / skill_invoked / hook_refused / checkpoint_resolved / etc.), `field_path`, `before`/`after`, timestamp. Read by `session-search`, audited by `turn-end-audit.py`.

**Awareness encoding** · `concepts_introduced[]` in `operator/awareness.json` tracks what has been explained to this operator. Calibrates the agent's register session-to-session. The agent never re-explains a concept the awareness file says is known.

---

## 6. Anti-patterns

| Name | Symptom | Fix |
|---|---|---|
| **Direct Edit on brand JSON** | An author bypassing `write_to_context` because "the gate doesn't cover my case". | Surface the gap to the maintainer. Extend the gate. NEVER hand-edit. |
| **Free-text where canon exists** | `tone: "rassurant et chaleureux mais pas trop direct"` instead of `tone: ["reassuring", "warm"]` from a controlled vocabulary. | Externalize the vocabulary in a registry, switch the field to enum. |
| **Untyped field** | A field carrying value but no `_field_types` tag. | Tag at write time. The agent cannot reason about provenance otherwise. |
| **Singleton-as-canon** | One verbatim, one operator declaration → brand truth. | Triangulation rule. Singletons flagged as hypothesis. |
| **Snapshot drift** | Operator asks "what's the brand status?", agent reads JSONs directly because snapshot is stale. | Hard rule: rebuild snapshot after every write to entity JSON. |
| **Memory cross-contamination** | An operator preference written into brand JSON ("operator prefers concise output", wrong layer). | Strict separation enforcement. The memory layer is determined by the *subject* of the fact, not the *trigger* of the write. |
| **Learnings overwrite** | A learning "corrected" by editing the original entry. | Append-only. New entry [SUPERSEDES Lxxx]. Old entry retains for audit. |
| **Schema drift** | Custom extension diverges from core schema patterns (no `_version`, no `_field_types`). | Extension layer governance, same rules as core. |
| **Convention drift** | Skill-author hardcodes a Meta API field name that conflicts with `resources/conventions/meta.json`. | Always read conventions before platform interaction. |
| **Validation noise** | Every MINOR finding surfaced to the operator → operator stops reading the audit. | Surface MAJOR/CRITICAL only. MINOR routes to a backlog. |

---

## 7. Decision-aid for skill creation

Skills authored under SAD must respect SED at the substrate level. Specifically:

**Before writing a new field or entity**, the skill author asks:
1. Is there an existing entity / sidecar / extension that already encodes this? (extend > create, see SAD)
2. What is the canonical type of this value (observed / stated / structured / derived)?
3. Is there a closed vocabulary that should constrain the field?
4. Will this field be load-bearing for downstream decisions? If yes → triangulation rule applies, version with `_version`, source-tag mandatory.
5. Is this spatial (entity) or temporal (event/learning/awareness)? Wrong layer = corruption.
6. Does this require an extension layer entry (custom entity / sidecar) or a core entity update? Core update requires schema bump + migration.

**Before writing a hook**, the skill author asks:
1. Is this enforcement *mechanical* (refuses an invalid state) or *semantic* (challenges model judgment)? Per CI, mechanical is enforceable, semantic is not.
2. Does this hook write to disk? If yes → must go through the mutation gate, must emit an event, must be auditable.

---

## 8. Operational requirements

**8.1 Schema versioning.** `_version` semver per entity / per canon file. Major bump requires migration script for consumers. Minor bump is backward-compatible enum extension. Patch is comment / clarification.

**8.2 Mutation gate enforcement.** `mutation-guard.py` blocks `Edit/Write/NotebookEdit` on `brands/**/*.json` and `operator/**/*.json`. Whitelist for explicit operator-tooling that goes through `write_to_context`. Refusals are logged.

**8.3 Sourcing tags auto-applied.** At write time, the source is inferred from the calling context (scrape literal → observed, operator declaration → stated, computation → derived, model inference → flagged inferred with confidence). The operator never sees `source` / `confidence` numbers · only `observé / déduit / déclaré / incertain` if relevant.

**8.4 Append-only enforcement.** `decisions.md` and `learnings.json` are append-only by hook. Edits to past entries are refused unless explicit `[SUPERSEDED]` annotation.

**8.5 Triangulation surfaced.** When a field is load-bearing but sourced from a single input, the agent flags it as hypothesis in operator-facing output ("à valider · basé sur 1 source").

**8.6 Snapshot regen automatic.** Post-write hook (`post-write-flush.py`) rebuilds `_snapshot.md` and any derived indexes within ~50ms of mutation.

**8.7 Validation runtime selective surfacing.** MAJOR/CRITICAL → flag operator. MINOR → backlog. CRITICAL → may halt operation.

**8.8 Extension governance.** Custom entities + sidecars validated by `validate-schema-canon` against same standards as core. New extension requires (a) schema declared, (b) `_version` set, (c) README explaining purpose, (d) registry entry.

**8.9 Convention precedence.** Platform conventions (`resources/conventions/`) take precedence over skill defaults. Conflict → conventions win.

**8.10 Memory layer separation.** Hooks refuse cross-layer writes (an operator preference attempted in a brand JSON is rejected with redirect). Three layers, never mixed.

---

## 9. Anti-cartography (what SED does NOT cover)

To prevent scope creep, SED explicitly does NOT cover:

- **The reasoning over the substrate** (CMR territory · production with intersectional matrices).
- **The creation of new skills consuming the substrate** (SAD territory · authoring discipline).
- **The trust / provenance / multi-tenant attribution of who wrote what** (PTD territory · full doctrine pending trigger conditions).
- **The agent's communication style** (CI Surface contract sub-corpus · voice, close, sharpening).
- **The vision / extractibility test** (Extractibility frame test).

When in doubt about whether a rule is SED or another doctrine, ask: *"is this about how data gets and stays well-encoded ?"* If yes, SED. If no, route elsewhere.

---

## 10. Open tensions

1. **`_field_types` enum extensibility.** The four canonical values (observed / stated / structured / derived) cover most cases, but boundary cases recur (a value computed from multiple observed inputs, derived ? structured ?). Working rule: derived = computed by deterministic function, structured = inferred by model. To be validated on three more brands.

2. **Triangulation rule cardinality.** "≥3 sources" works for verbatims (mine-voc easily produces dozens). It is harder for operator declarations (1 founder = 1 source, by definition). Working rule: operator declaration counts as 1 source ; needs corroboration from 2 other types (observed scrape + derived inference, for example) to become canonical. Singletons stay flagged as hypothesis.

3. **Layer separation and analytics.** Cross-layer queries (e.g. "for this brand, what concepts has this operator already mastered?") cross the entity / operator boundary. Read-only cross-layer is allowed by query primitives ; write-side is forbidden. To be codified explicitly.

4. **Memory layer for shared (cross-brand) learnings.** A pattern observed across 5 brands is canon-candidate, not brand-specific learning. Where does it live? Working rule: in `shared-resources/learnings-canon/` after promotion via `promote-learning`. Until promotion, lives in each brand's `learnings.json` flagged as cross-brand candidate.

5. **Extension layer maturity.** Custom entities are validated, but their *quality* (are they well-modeled?) is harder to enforce mechanically. SAD red-team checks help. Open question: should SED enforce extension review by ≥1 senior before promotion to runtime?

6. **PTD overlap.** When PTD ships full, it will introduce `_provenance` blocks and `actor_id` attribution that touch every entity write. SED today carries the substrate ; PTD will carry the trust layer atop. Boundary to be redrawn at PTD draft promotion.

---

## Position dans le système opérationnel 5 couches

SED opère sur 2 couches du système opérationnel (cf
`operational-system-doctrine.md`) · couche 1 (modèle · atomicité des
entités, cross-refs canonical, append-only learnings) · couche 4 (métriques ·
_field_types observed/stated/derived/structured assure traçabilité audit
trail, mutation gate proposed/accepted feedback loop).

SED est le squelette technique sur lequel toutes les autres couches s'appuient.

---

## 11. Cross-references

- **`contextual-intelligence.md`** · master doctrine ; SED is the substrate sub-doctrine that keeps CI's reasoning honest.
- **`canonical-matrix-reasoning.md`** · CMR depends on SED ontologically (no schema → no matrix). SED invariants 3 (sourcing) and 5 (triangulation) feed CMR invariants 4 (canon sourcing) and 9 (triangulation rule) directly.
- **`skill-authoring-doctrine.md`** · SAD governs how skills consume the SED substrate. SAD reads SED, not the inverse.
- **`provenance-trust-discipline-scope.md`** *(R&D zone, lives in `research/` until promotion triggers hit)* · PTD will extend SED with provenance/trust at the multi-tenant scale.
- **`field-types.md`** · canonical reference for the four `_field_types` values. Source of truth, SED chapter that points to it.
- **`extending.md`** · extension layer rules ; SED chapter that contextualizes them in the broader discipline.
- **`architecture.md`** · entity dependency graph, context budget, structural reference ; pre-existing input to SED.
- **Hooks** · `mutation-guard.py`, `convention-guard.py`, `post-write-flush.py`, `turn-end-audit.py`, operational enforcement of SED invariants.

---

## Amendment protocol

To amend this doctrine, follow the procedure documented in `docs/system/doctrine-governance.md` § Amendment : draft the change in a research note, register a new D# entry in `decisions.md` with explicit `[SUPERSEDES Dxxx]` annotation, patch the doctrine file with a changelog header, and surface a re-test list of consumer skills. Silent edits to a binding doctrine are refused by convention.

---

## 12. Status

- **Draft v0.1** · research zone, Build mode, .
- **Promotion criterion** · to be reviewed by the maintainer, then promoted to `workspace-template/docs/system/schema-encoding-doctrine.md` once cross-references with CMR / SAD / PTD scope are validated and the 11 sub-disciplines previously scattered are confirmed consolidated.
- **First applications** · patches to extension layer governance, sourcing-tag enforcement on legacy brand JSONs, triangulation-rule surface in `validate-resources` output.

---

## 13. Schema evolutions registry

Registre canonique des évolutions schemas par release. Toute mutation `resources/schemas/*.json` doit apparaître ici (bump version, NEW schema, patch additif, $ref refactor). Append-only.

### v2.64 (2026-05-14) · Sémantique pure · sub-audience / sub-product storage location

Driver · refactor ontologie pure post-v2.63. v2.63 avait fermé l'inconsistance friction-vs-pain/objection (3 top-level collections séparées), mais la sémantique top-level pour pain_point + objection était un compromis opérationnel (filter UI tableau facilité, miroir canon Notion stride-up workspace Onday top-level tables). Sémantique vraie · pain_point + objection = expression audience-specific (un pain est ressenti par une audience, une objection est portée par une audience). friction = product-specific usage observation (une friction se manifeste au contact d'un produit concret). v2.64 réconcilie · canonical IDs PNT-NN / OBJ-NN / FRC-NN preserved globaux (stable cross-folder), sémantique storage location alignée vérité (sub-audience pour pain + objection, sub-product pour friction).

| Schema | Action | Version | Diff |
|---|---|---|---|
| `pain_points.schema.json` | BREAKING storage path | v1.0 → v1.1 | Storage path · `brands/{slug}/audiences/{audience_slug}/pain_points/{PNT-NN}.json` (NEW v2.64 sub-audience location, au lieu de top-level v2.63). Sémantique pure · pain_point = expression audience-specific. NEW properties · `also_affects_audiences[]` array optional · cross-refs vers AUTRES audiences qui partagent ce pain canonical (canonical entry stocké chez primary owner audience = 1ère dans affected_audiences[], also_affects_audiences[] liste les audiences additionnelles partagent). Évite duplication fichier pour pain shared cross-audiences. Migration script `operations/migrations/v2.64-subfolder-collections.py` idempotent. |
| `objections.schema.json` | BREAKING storage path | v1.0 → v1.1 | Storage path · `brands/{slug}/audiences/{audience_slug}/objections/{OBJ-NN}.json` (NEW v2.64 sub-audience location). Sémantique pure · objection = expression audience-specific (barrage achat porté par une audience). NEW properties · `also_affects_audiences[]` array optional · mêmes sémantiques cross-refs que pain_points.also_affects_audiences[]. Migration via v2.64-subfolder-collections.py. |
| `friction.schema.json` | BREAKING storage path | v1.2 → v1.3 | Storage path · `brands/{slug}/products/{product_slug}/frictions/{FRC-NN}.json` (NEW v2.64 sub-product location, au lieu de top-level v2.56-v2.63). Sémantique pure · friction = product-specific usage observation. `affects_audiences[]` preserved (cross-refs canonical vers audiences impactées par la friction). Migration via v2.64-subfolder-collections.py · primary_product = 1ère dans affected_products[]. Cas edge · friction sans affected_products[] stay top-level avec warning log (operator review · brand-wide friction sans product attachment). |

**Décision design SED-side · (a) sémantique pure storage location** · pain + objection = expression audience-specific (un pain n'existe pas dans le vide · il est ressenti par une audience concrète · même formulation pain peut être ressentie différemment par 2 audiences différentes, ou seulement par une seule). objection = même logique (barrage achat porté par audience identifiée). friction = product-specific usage observation (une friction se manifeste au contact d'un produit ou d'une catégorie produit · pas brand-wide par défaut, sauf cas edge documentés). Sub-audience pour pain + objection, sub-product pour friction · ontologie alignée vérité métier.

**Décision design SED-side · (b) Largo's flag · canon Notion stride-up top-level était compromis opérationnel** · workspace Onday stride-up implémentait pain + objection + friction comme top-level tables Notion pour faciliter le filter UI tableau (drag-drop, sort, multi-select cross-audiences, view aggregate). Compromis opérationnel pour l'UI Notion (limitation native filters cross-DB), pas sémantique vraie. v2.63 avait dupliqué ce pattern dans PhantomOS storage (parité canon stride-up strict). v2.64 réconcilie · sémantique storage alignée vérité métier (sub-audience pour pain + objection, sub-product pour friction) + canonical IDs PNT-NN / OBJ-NN / FRC-NN preserved globaux (stable cross-folder, scan global possible pour aggregate queries via glob `brands/{slug}/audiences/*/pain_points/PNT-*.json`).

**Décision design SED-side · (c) also_affects_audiences[] cross-refs pour pain shared cross-audiences** · canonical entry stocké chez primary owner audience (1ère dans affected_audiences[]), also_affects_audiences[] = [affected_audiences[1:]] liste les audiences additionnelles qui partagent le pain. Évite duplication fichier (un pain ne doit pas exister en 2 ou 3 exemplaires identiques sous chaque audience qui le partage · single source of truth canonical chez primary). Join-style queries cross-audience possibles · scan toutes les audiences qui ont ce pain in affected_audiences[] (primary) ou also_affects_audiences[] (cross-refs).

**Décision design SED-side · (d) migration script idempotent v2.64-subfolder-collections.py · pattern reproductible** · miroir pattern `v2.63-pain-objection-collections.py` · idempotent par construction (check existing target sub-folder before write, skip si déjà migré), backup horodaté zip des top-level dirs avant move, log mutations + warnings dans `.phantom/context-engine-events.jsonl`, cleanup top-level dirs après move success (garde si fichiers restants pour cas edge zero affected_*). Pattern reproductible pour futurs refactor storage path (zip backup + idempotent target check + events log + cleanup conditionnel).

**Activation runtime** · `mine-voc` v2.64+ écrit directement dans `audiences/{slug}/pain_points/{PNT-NN}.json` + `audiences/{slug}/objections/{OBJ-NN}.json` via mutation gate (au lieu de top-level v2.63 path). `profile-audience` v2.64+ consume sub-audience scan canonical pour synthèse audience-level (glob `audiences/{audience_slug}/pain_points/*.json` au lieu de filter top-level by affected_audiences[]). `produce-paid-angles` v2.64+ consume sub-audience pain_points + objections comme atomes audience-scoped. `validate-resources` v2.64+ check storage path canonical match · MAJOR si pain_point top-level résiduel post-migration sans warning justifié.

**Backward compat read** · brands pre-v2.64 avec pain_points/ + objections/ + frictions/ top-level continuent à valider en read (legacy support). Migration explicite via script · pas de auto-migration silencieuse. Validation runtime MINOR · "pain_points top-level detected, propose migration v2.64 pour sémantique pure sub-audience".

**Cohérence cross-schema · cross-refs canonical-uniformes post-v2.64** · friction.cross_refs.pain_point_ids[] PNT-NN match `brands/{slug}/audiences/*/pain_points/PNT-*.json` (sub-audience). friction.cross_refs.objection_ids[] OBJ-NN match `brands/{slug}/audiences/*/objections/OBJ-*.json`. angle.lineage.pain_ref PNT-NN + objection_ref OBJ-NN match canonical sub-audience. learnings.entries[].cross_refs.{pain_point_ids[], objection_ids[]} match canonical sub-audience. Mismatch détecté par `validate-resources` surface comme MAJOR (référence canon brisée). friction.cross_refs.affects_audiences[] preserved cross-refs sub-audience audiences impactées par la friction.

### v2.63 (2026-05-14) · Refactor ontologie pure · pain_points + objections top-level collections

Driver · ontologie inconsistance identifiée post-v2.57 · `friction` est top-level collection depuis v2.56 (`brands/{slug}/frictions/{FRC-NN}.json` storage canon), mais `pain_points[]` et `objections[]` restaient sub-fields du `profile.schema` v1.7. Conséquence · `friction.cross_refs.{pain_point_ids[], objection_ids[]}` pointait vers du semi-vide (IDs PNT-NN/OBJ-NN générés v1.7 mais entités non-adressables canoniquement comme `friction/{FRC-NN}.json`). Refactor pure · 3 collections sub-tensions séparées (`friction` + `pain_points` + `objections`), parité canon Notion stride-up strict, ontologie cohérente, cross-refs canonical-uniformes.

| Schema | Action | Version | Diff |
|---|---|---|---|
| `pain_points.schema.json` | NEW | v1.0 | NEW top-level collection canonical. Storage `brands/{slug}/pain_points/{PNT-NN}.json`. Extracted from profile.pain_points[] legacy v1.7. PNT-NN id pattern cohérent FRC-NN/OBJ-NN/ANG-NN canon. Fields · pain_id + formulation + pain_category enum (6 valeurs alignées friction.category) + chain object (surface/consequence/deep) + emotion + trigger + awareness_stage ($ref _shared) + verbatim_quotes[] + affected_audiences[] cross-ref + affected_products[] cross-ref + derived_angle_refs[] back-ref + meta.{validation_status $ref, _source enum, created, updated, created_by_skill}. |
| `objections.schema.json` | NEW | v1.0 | NEW top-level collection canonical. Storage `brands/{slug}/objections/{OBJ-NN}.json`. Extracted from profile.objections[] legacy v1.7. OBJ-NN id pattern. Fields · objection_id + formulation + type enum 7 valeurs canon (price/scepticism/fit/urgency/trust/status/risk) + lifecycle_stage enum 4 canon + frequency enum (low/medium/high) + severity enum (low/medium/high/blocking) + severity_score 1-10 + response_counter + verbatim_quotes[] + affected_audiences[] + affected_products[] + derived_angle_refs[] + meta.{validation_status, _source, created, updated, created_by_skill}. |
| `profile.schema.json` | BREAKING | v1.7 → v2.0 | REMOVE pain_points[] array (extracted to pain_points top-level). REMOVE objections[] array (extracted to objections top-level). Keep · identity + psychology + voice + behavior + decision_process + market_position + research_meta + purchase_driver + persona_archetype + buyer_user_split + role + meta + benefits[] + _field_types. Migration script `operations/migrations/v2.63-pain-objection-collections.py` idempotent · scan profile.pain_points + profile.objections, génère PNT-NN + OBJ-NN ids (incrémental cross-audience), crée fichiers canonical avec affected_audiences=[audience_slug], remove arrays du profile, bump _schema_version. |
| `friction.schema.json` | patch additif | v1.1 → v1.2 | cross_refs.{pain_point_ids[], objection_ids[]} maintenant cross-refs canonical vers pain_points/{PNT-NN}.json + objections/{OBJ-NN}.json top-level collections (pattern `^PNT-[0-9]{2,3}$` + `^OBJ-[0-9]{2,3}$` enforced). Description ajustée explicite. Backward compat read · IDs PNT-NN/OBJ-NN existants (générés v1.7) valident. |
| `angle.schema.json` | patch additif | v1.2 → v1.3 | lineage.pain_ref (pattern `^PNT-[0-9]{2,3}$`) optional · canonical ref vers pain_points/{PNT-NN}.json quand lineage.pain_extract dérive d'un pain identifié. lineage.objection_ref (pattern `^OBJ-[0-9]{2,3}$`) optional · canonical ref vers objections/{OBJ-NN}.json quand formula.tension dérive d'une objection canonical. Legacy lineage.pain_extract text preserve. |
| `learnings.schema.json` | patch additif | v1.0 → v1.1 | entries[].cross_refs.pain_point_ids[] + objection_ids[] arrays ajoutés (cross-refs canonical vers pain_points/{PNT-NN} + objections/{OBJ-NN} top-level collections). Preserve angle_ids/audience_slugs/product_slugs/friction_ids/brief_ids/creative_ids existants. Patterns enforced (`^PNT-NN`, `^OBJ-NN`, `^FRC-NN`, `^ANG-NN`). |

**Décision design SED-side · pourquoi BREAKING justifié maintenant** · v2.57 avait posé PNT-NN/OBJ-NN id pattern dans profile sub-fields comme palier transitoire (canonical IDs sans casser ontologie). v2.63 termine le refactor · les IDs valident canonical seulement si l'entité est top-level adressable comme `friction`. Sub-field IDs sont canonical en nom uniquement, pas en storage. Inconsistance ontologique = drift latent (friction queries fonctionnent · `brands/{slug}/frictions/FRC-12.json`, pain queries impossible sans crawl profile JSONs). Refactor maintenant ferme le drift avant que des skills downstream (analyze-copy, produce-paid-angles, decompose-ad) ne construisent leur logique sur la double-ontologie. Migration script idempotent · re-run safe, backup horodaté, log mutations dans `.phantom/context-engine-events.jsonl`.

**Décision design SED-side · ontologie pure 3 collections sub-tensions parité canon Notion stride-up** · friction (moment usage observé) + pain_points (problème ressenti par audience) + objections (barrage achat). Chacun top-level adressable, chacun cross-ref vers les deux autres + audiences + products + angles. Composition libre · une friction peut surface plusieurs pain_points + amplifier plusieurs objections, un pain_point peut générer plusieurs objections, etc. Parité canon Notion stride-up workspace Onday · 3 collections séparées avec join-style queries cross-collection.

**Décision design SED-side · ID pattern PNT-NN / OBJ-NN cohérent FRC-NN canon** · 2-3 digits anticipation scale long-terme (audiences complexes peuvent générer 50+ pains, 30+ objections sur lifetime brand). Generation auto par migration script (incrémental cross-audience pour première pass, post-migration via `mine-voc` et `profile-audience` skills). Allocator scan existing `{prefix}-NN.json` dans collection dir pour next sequential id (jamais re-assignation).

**Décision design SED-side · migration idempotente · re-run safe** · script check existing `pain_points/{PNT-NN}.json` + `objections/{OBJ-NN}.json` avant write. Si fichier existe, skip extraction (idempotent par construction). Profile re-scan post-migration · si profile._schema_version == "profile/2.0", skip complet. Backup horodaté par profile muté (.bak.YYYY-MM-DD). Events log dans `.phantom/context-engine-events.jsonl` pour audit trail (one event par extraction + one event par profile patch).

**Mapping legacy → canonical · type enum** · profile.objections.type legacy enum FR (prix/scepticisme/temps/confiance/urgence/efficacité/comparaison) → objections.type v2.63 EN canon 7 valeurs (price/scepticism/fit/urgency/trust/status/risk). Mapping migration · prix→price, scepticisme→scepticism, temps→fit, confiance→trust, urgence→urgency, efficacité→fit, comparaison→fit. status + risk additions v2.63 non-mappées (générés post-migration par mine-voc enrichissement).

**Mapping legacy → canonical · frequency** · profile.objections.frequency legacy integer 1-10 → objections.frequency v2.63 enum (low/medium/high). Buckets · 1-3→low, 4-6→medium, 7-10→high. Preserve severity_score 1-10 integer (non-bucketé pour audit fin).

**Cohérence cross-schema · cross-refs canonical-uniformes post-v2.63** · friction.cross_refs.pain_point_ids[] PNT-NN match `brands/{slug}/pain_points/*.json`. friction.cross_refs.objection_ids[] OBJ-NN match `brands/{slug}/objections/*.json`. angle.lineage.pain_ref PNT-NN match canonical. angle.lineage.objection_ref OBJ-NN match canonical. learnings.entries[].cross_refs.{pain_point_ids[], objection_ids[]} match canonical. Mismatch détecté par `validate-resources` surface comme MAJOR (référence canon brisée).

**Backward compat read** · brands pre-v2.63 sans `pain_points/` ou `objections/` collections continuent à valider profile schema v1.7 en read (legacy support). Migration explicite via script · pas de auto-migration silencieuse. Validation runtime MINOR · "profile v1.7 detected, propose migration v2.63 pour cohérence ontologie 3 collections sub-tensions".

**Activation runtime** · `mine-voc` v2.x post-v2.63 écrit directement dans `pain_points/{PNT-NN}.json` + `objections/{OBJ-NN}.json` via mutation gate (au lieu de profile.pain_points[] + profile.objections[]). `profile-audience` v2.x consume cross-refs canonical pour synthèse audience-level. `produce-paid-angles` v2.x consume pain_points/* + objections/* comme atomes top-level (au lieu de drill profile sub-fields). `validate-resources` v2.x check cross-refs PNT-NN/OBJ-NN canonical match collections.

### v2.58 (2026-05-14) · Strategy + Learnings canon NEW · R&D zone shipped

Driver · audit dette technique runtime identifie 2 schemas en R&D zone (`05-projects/context-engine/schemas/strategy.schema.json`, `learnings.schema.json`) pré-existants depuis ~10 jours mais jamais promus workspace-template. `build-atlas-complete` runtime écrit `brands/{slug}/strategy/roadmap.json` + `brands/{slug}/strategy/score-matrix.json` sans canon schema (output orphan, non-validable par `validate-resources`). Promotion R&D → canon zone ferme la dette · activation runtime via NEW orchestrator `produce-strategy` + patch path canonical `build-atlas-complete`.

| Schema | Action | Version | Diff |
|---|---|---|---|
| `strategy.schema.json` | NEW | v1.0 | NEW canon entity. Singleton `brands/{slug}/strategy.json`. annual_goals[] (GOAL-NN id pattern + category enum revenue/growth/retention/expansion/operational/brand_equity/compliance + statement + target_value + kpi_metric + target_date + progress_pct + status enum draft/active/achieved/paused/abandoned). current_focus singleton Q{n}-{year} (primary_focus + acquisition_focus enum new_customer_acquisition/retention/expansion_existing/reactivation/education/mixed + channels_prioritized[] + target_audiences_prioritized[] + target_products_prioritized[] + budget_allocation %). constraints[] (CST-NN id pattern + type enum budget/regulatory/operational/team_capacity/supplier/seasonality/compliance/ethical + severity enum + until_date). meta.validation_status $ref _shared/validation-status. next_review_date. Cycle annuel + trimestriel reviewable. |
| `learnings.schema.json` | NEW | v1.0 | NEW canon entity. Singleton `brands/{slug}/learnings.json` append-only. entries[] (LRN-NNNN id pattern + kind enum test_result/workaround/compliance/observation/decision_trace/hypothesis_validated/pattern_promoted/regulatory_signal/competitor_move + fact + context + cross_refs canonical vers angle_ids/audience_slugs/product_slugs/friction_ids/brief_ids/creative_ids + test_result_data structure ROAS/CTR/spend/days_running/winner_proxy/fatigue_signal + validation_status $ref _shared/validation-status + superseded_by append-only invalidation + promoted_to_canon flag + source enum operator/agent/skill_output/test_capture). meta.append_only:true const, total_entries count, promoted_to_canon_count. |

**Décision design SED-side · pourquoi shipper maintenant après ~10 jours R&D lag** · `build-atlas-complete` v1.0.0 (shipped v2.56) écrit runtime `brands/{slug}/strategy/roadmap.json` + `brands/{slug}/strategy/score-matrix.json` sans canon schema. Outputs orphans non-validables, `validate-resources` ne les couvre pas, drift silencieux possible. Promotion R&D → canon zone + patch `build-atlas-complete` vers path canonical (`brands/{slug}/strategy.json` + `brands/{slug}/scoring/matrix-{date}.json` aligné avec `produce-paid-matrix.produces_proposals_for`) ferme la dette runtime. Backward compat strict · brands existantes sans `strategy.json` valident toujours (singleton optional, `validate-resources` trigger fresh proposal si missing).

**Décision design SED-side · `learnings.schema` baseline v1.0 ferme la fragmentation R&D** · R&D draft (`05-projects/context-engine/schemas/learnings.schema.json`) avait kind enum 5 valeurs · v2.58 canon étend à 9 valeurs (ajoute hypothesis_validated, pattern_promoted, regulatory_signal, competitor_move) pour couvrir les patterns détectés par `learn-from-session` Trigger 8 + `brief-day` smart-suggest daemon. cross_refs canonical vers entités v2.56+ (friction_ids · brief_ids · creative_ids) permet pattern detection cross-entity sans free-text drift. validation_status $ref composite avec append-only enforcement (superseded_by, jamais delete).

**Décision design SED-side · GOAL-NN / CST-NN / LRN-NNNN id patterns** · cohérence avec FRC-NN (friction v2.56) + ANG-NN (angle) + MEC-NN (mechanism) + PNT-NN/OBJ-NN (profile v2.57) + RDM-{slug} (roadmap v2.56). Numérotation 2-3 digits pour GOAL/CST (cycle stratégique ≤ 100 entries) · 3-5 digits pour LRN (log append-only croît) · anticipation scale long-terme.

**Activation runtime** · NEW skill `produce-strategy` v1.0.0 (orchestrator operator-guided 6 steps Q&A) consume `brand.json` + `audiences/*/profile.json` + `learnings.json` + `roadmap.json` et stage strategy.json via mutation gate mode=proposed. `build-atlas-complete` v1.0.1 patché canonical path · invokable produce-strategy en post-Phase 10 close si l'opérateur veut cadrer le focus Q{n} sur la brand atlas-complete. `learnings.schema` v1.0 consume side · `learn-from-session` Trigger 8 daemon append entries kind selon pattern détecté · `capture-learning` one-off operator-named · `brief-day` smart-suggest scan recent entries pour surface patterns.

**Cohérence cross-schema** · `strategy.current_focus.target_audiences_prioritized[]` doit matcher `brands/{slug}/audiences/{slug}/` existing folders. `target_products_prioritized[]` doit matcher `brands/{slug}/products/{slug}/`. `learnings.entries[].cross_refs.angle_ids[]` doit matcher `brands/{slug}/angles/*.json` ANG-NN ids. `learnings.entries[].cross_refs.friction_ids[]` doit matcher `brands/{slug}/frictions/*.json` FRC-NN ids (v2.56 NEW). Mismatch détecté par `validate-resources` surface comme MAJOR (référence canon brisée, pas erreur structurelle).

**Backward compat strict** · brands pre-v2.58 sans `strategy.json` ou `learnings.json` valident toujours en read. Validation runtime trigger fresh proposal si missing au lieu de fail. `validate-resources` MINOR · "strategy.json absent, propose `produce-strategy` pour cadrer Q{n} focus" · "learnings.json absent, propose `capture-learning` pour première entry". Surface opérateur uniquement si MAJOR (cross-refs cassées).

### v2.57 (2026-05-14) · Notion stride-up follow-up + hybrid business support

Driver · DataEng audit post-v2.56 identifie 4 gaps résiduels · (1) brand n'encode pas le business model (DTC vs service vs hybrid) qui drive le rendering /phantom contextuel ; (2) friction.cross_refs.{pain_point_ids[], objection_ids[]} pointe vers du vide car profile ne génère pas d'IDs stables ; (3) friction.category enum diverge de profile.pain_category (5 vs 6 valeurs, manque social_status) ; (4) spec.identity.type ne couvre pas service / hybrid / clinical_service. Patches additifs STRICTS, backward compat preserved (toutes nouvelles properties optional, enum extensions additives).

| Schema | Action | Version | Diff |
|---|---|---|---|
| `brand.schema.json` | patch additif | v2.3 → v2.4 | identity.business_model enum (DTC / service / hybrid / subscription / marketplace, default DTC) + identity.business_model_signals (physical_locations_detected / services_detected / products_detected / revenue_split_estimated / declared_by_operator). Drive rendering /phantom contextuel. Auto-detection heuristique snapshot-brand, override opérateur via setup-brand. |
| `profile.schema.json` | patch additif | v1.6 → v1.7 | pain_points.items.pain_id (pattern `^PNT-[0-9]{2,3}$`) + objections.items.objection_id (pattern `^OBJ-[0-9]{2,3}$`). Closes faille canonical IDs stables (friction.cross_refs peut désormais référencer canon). Optional, generated au mining post-v1.7. Profiles pre-v1.7 sans IDs valident toujours en read. |
| `friction.schema.json` | patch additif | v1.0 → v1.1 | category enum += social_status (align profile.pain_category v1.6 taxonomy 6 valeurs). Cohérence sémantique cross-schema. Existing friction valeurs valident toujours. |
| `spec.schema.json` | patch additif | v1.10 → v1.11 | identity.type enum += service / hybrid / clinical_service (aux existants functional / sensory / lifestyle). Cohérent brand.business_model v2.4 · service brand → product type service / clinical_service · hybrid brand → mix de types. Existing identity.type valeurs valident toujours. |

**Décision design SED-side** · business_model est encodé identity-level (pas meta-level) car c'est une propriété sémantique brand stable, pas un état de validation. business_model_signals capture les signaux scrape pour éviter re-detection silencieuse + permettre audit du raisonnement auto. declared_by_operator: true verrouille contre auto-override.

**Décision design SED-side · pain_id / objection_id pattern PNT-NN / OBJ-NN** · cohérence avec FRC-NN (friction) + ANG-NN (angle) + MEC-NN (mechanism) + RDM-{slug} (roadmap). Numérotation 2-3 digits (anticipation profils complexes >100 entrées). Generation auto par mining skills (mine-voc, profile-audience) au mining post-v1.7. Backfill manuel possible via write-to-context si profile pre-v1.7 est revisité.

**Décision design SED-side · enum extensions strictement additives** · friction.category + spec.identity.type étendus sans rename ni rephrasing des valeurs existantes. Anti-pattern breaking change (rename, suppression, restriction) refusé par convention. Cohérence semver patch.

**Cohérence cross-schema** · brand.business_model + spec.identity.type + brand.products_index.product_category forment une triple-cohérence rendering /phantom · brand business_model=service AND products_index entries product_category=service AND spec.identity.type=service (ou clinical_service). Mismatch détecté par validate-resources surface comme MAJOR (incohérence sémantique, pas erreur structurelle).

**Activation runtime** · setup-brand v2.x consume identity.business_model auto-detection · snapshot-brand v2.x scrape les signals · mine-voc v2.x + profile-audience v2.x génèrent pain_id / objection_id au mining post-v1.7 · friction-cartography skill (futur) référence pain_point_ids + objection_ids canon.

### v2.56 (2026-05-12) · Notion stride-up alignment

Driver · audit Phase 1 quantifie gap 70% coverage Notion 11 collections workspace `Onday`. PhantomOS implémente la doctrine `compositional-cartography.md` (4 arbres + matrice + modulateurs), Notion stride-up en est l'instance opérationnelle de référence. Bloc 1 comble 2 schemas manquants + 5 patches additifs, backward compat strict (toutes properties optional, validation existing instances OK).

| Schema | Action | Version | Diff |
|---|---|---|---|
| `friction.schema.json` | NEW | v1.0 | NEW entity. FRC-NN id pattern. Category enum (physical/emotional/friction_ux/logistical/cognitive). severity_score 1-10. customer_evidence[]. cross_refs vers objection_ids[] + pain_point_ids[]. Storage `brands/{slug}/frictions/{FRC-NN}.json`. Cross-ref doctrine compositional-cartography §"État atlas · couverture verbatims". |
| `roadmap.schema.json` | NEW | v1.0 | NEW entity. RDM-{brand_slug} id pattern. phases[] (phase_id, name, dates, status, priorities[]). mix[] (mix_id, weight 0-1, axis enum [audience, angle, product, funnel, creative]). production_status[]. relations cross-refs angles/audiences/products/creatives. Storage `brands/{slug}/roadmap.json` (brand-wide). |
| `spec.schema.json` | patch additif | v1.9 → v1.10 | benefits.items.properties · `emotional_signal` (string) + `latency_min`/`latency_max` (integer jours) + `evidence_verbatim[]`. mechanisms.items.properties · `duration` (string délai d'effet). meta · `validation_status` ($ref `_shared/validation-status.json`). |
| `profile.schema.json` | patch additif | v1.4 → v1.6 | pain_benefit_chain.items · `pain_category` enum (physical/emotional/friction_ux/logistical/cognitive/social_status, cohérent friction.schema). objections.items enrichi · `severity_score` 1-10 + `response_counter` (string) + `derived_angle_refs[]`. |
| `offer.schema.json` | patch additif | v2.1 → v2.2 | meta · `validation_status` ($ref `_shared/validation-status.json`). |
| `brand.schema.json` | patch additif | v2.2 → v2.3 | meta · `validation_status` ($ref `_shared/validation-status.json`). |

**Décision design SED-side** · NE PAS dupliquer `meta.source / meta.confidence` sur chaque schema. Le pattern `_field_types` per-field (observed/stated/derived/structured · cf section 5 + `field-types.md`) couvre déjà la sémantique source canon. Seul `meta.validation_status` est ajouté en composite uniforme (hypothesis/tested/validated/scaled/fatigued) via `$ref _shared/validation-status.json`, parce qu'il indique l'état de validation terrain (orthogonal à source canonique).

**Décision design SED-side · pas de objection.schema dédié** · 60% fragmenté volontaire. Doctrine compositional-cartography §4 confirme · objection n'est pas un arbre cartographique standalone, elle est consumée par profile (terrain audience) + angle (lever neutralization). Enrichissement profile.objections suffit. Anti-pattern cardinality dispersion évité.

**Activation runtime** · brief.schema v1.0 (shippé v2.42, orphan jusqu'à v2.56) activée via produce-copy-brief v1.4.0 Step 6bis. Storage canonical migré vers `brands/{slug}/briefs/{BRF-NN}.md`. Legacy path `produced/copy-briefs/` deprecated mais lecture backward compat.

**Bridge sync external (Layer 1 MCP)** · schemas v2.56 sont consommés par `sync-notion-atlas` skill v1.0.0 (pull-only MVP Phase A) pour synchronisation bidirectionnelle PhantomOS ↔ Notion workspace. Doctrine canonique de ce bridge · `docs/system/notion-bridge-doctrine.md`.

---

*Doctrine · consolidates 11 previously-scattered sub-disciplines (mutation rule, _field_types, _version semver, sourcing tags, triangulation, validation runtime, append-only conventions, snapshot/manifest regen, conventions plateforme, extension layer, memory & observability) into one named discipline. Sister to CMR, SAD, PTD scope under CI master.*
