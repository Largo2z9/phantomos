# PhantomOS · Architecture Reference

> Technical deep-dive. Not auto-loaded. Read on demand.
> For the main workspace reference, see CLAUDE.md.

---

## Positioning

**Product level** · PhantomOS ships as an agentic workspace for **DTC paid acquisition operators**. Default entities (brand / product / offer / audience / angle / learnings / strategy) are validated at scale on DTC e-commerce.

**Thesis level** · PhantomOS is designed as an **extensible substrate for encoding any operator domain** that an agent can operate on. DTC paid acquisition is the current incarnation. Other domains (legal, health, enterprise, brick-and-mortar) require custom encoding ; no shipped vertical pack today.

**Design discipline · extractibility test (binary).** For every core feature: *"if I rename 'brand' to 'matter' (legal) / 'creator' (personal brand) / 'account' (SaaS) / 'venue' (hospitality), does it still hold?"* Yes → core. No → isolate in a vertical pack. This rule makes the agnostic thesis falsifiable in continuous design, not aspirational marketing.

---

## Canonical vocabulary

PhantomOS implements a discipline named **Context Layering**, a more granular variant of context engineering (Lütke, Karpathy, June 2025). Four first-class concepts:

| Concept | What it is | Where it lives in PhantomOS |
|---------|------------|-----------------------------|
| **Context Layering** | The discipline of building, layer by layer, the environment in which the agent reasons. | Whole workspace : OS layer + KB layer + Context DB. |
| **Decision Trace** | The logged *reasoning* behind a correction, not the correction itself. Transforms learnings from "what" to "why". | `learnings.json` entries with `reasoning` / `trace` field. Captured by `capture-learning` / `learn-from-session`. |
| **Skill Graph** | Atomic interconnected nodes, entry via index, selective traversal, never monolithic ingestion. | `resources/catalogues/` + `routing/` + cross-refs by ID + `index.json`. |
| **Feedback Loop** | Agent proposes → operator corrects → Decision Trace logged → Skill Graph enriched → agent proposes better. | Defines the compound effect claimed in README. |

These four terms are the external canon (tweet, LinkedIn, pitch, README, consulting collateral). Use them.

---

## What PhantomOS is technically

### Pattern: Structured Context Store with Entity-Centric RAG

PhantomOS is a **structured context store with deterministic injection**. It's neither vector RAG nor GraphRAG. It's a third pattern.

**Classic vector RAG** · you index documents into embeddings, run a cosine similarity search, inject the closest chunks. Probabilistic, uncontrolled retrieval.

**GraphRAG (Microsoft, 2024)** · you automatically extract entities and relationships from text, build a graph, traverse it for multi-hop retrieval ("find concepts linked to X in 2 hops"). Discovery of hidden relationships, but approximate by nature.

**PhantomOS** · the operator explicitly defines the entities (brand, product, offer, audience, angle, learnings, strategy) and their relationships (cross-refs by ID). The agent loads only entities relevant to its intent via deterministic rules. Zero probability, zero ambiguity.

```
Vector RAG → cosine similarity → floating chunks
GraphRAG → graph traversal → relationship discovery
PhantomOS → intent matching → tagged entities
```

### Why this choice

The problem of vector RAG for an operator workspace: it doesn't know what it loads. A chunk of brand.json can be adjacent to a chunk of session-state.md, the LLM mixes them. No data contract.

The problem of GraphRAG for this use case: relationships between e-commerce entities are not discovered, they are defined. That a product targets an audience, that this audience has price-related objections, that these objections imply a specific angle, this is a strategic decision, not a relationship to discover in raw text.

PhantomOS assumes that **structure is known**. The 7 entities are fixed, their fields are tagged (`_field_types`), their relationships are explicit (via ID). In exchange : max precision, zero relationship hallucination, controlled context budget.

### Technical components

| Component | Role | RAG equivalent |
|---|---|---|
| `brands/{slug}/*.json` | Per-brand context store | Document store |
| `_field_types` | Data contract per field | Metadata schema |
| `learnings-index.json` | Lightweight index for lazy loading | Vector index (no embeddings) |
| `query-context` skill | Deterministic intent-based retrieval | Retrieval engine |
| `index.json` | Shared resource registry | Knowledge base index |
| `validate-resources` skill | Integrity + cross-entity consistency | Data quality layer |
| `ingest-resource` skill | Extraction + structuring from raw text | ETL pipeline |
| `learn-from-session` skill | Persistence of operational learnings | Feedback loop |

### What distinguishes it from classic RAG

1. **Deterministic retrieval**, the agent knows exactly what it loads. No random chunks.
2. **Strict data contract**. Each field has a type (`observed | stated | derived | structured`). The agent cannot confuse a fact with an inference.
3. **Lazy loading by index**, learnings.json can have 500 entries, the agent only loads 3 via learnings-index.json.
4. **Managed context budget**, ≤8k tokens for a brand session, planned.
5. **Incremental enrichment**, each session adds value without starting over.

### What it is not

- Not a knowledge graph (no formalized nodes/edges, no traversal)
- Not a vector store (no embeddings)
- Not a database (no SQL query, no transactions)
- Not an agent framework (no built-in multi-agent orchestration)
- **Not an action tool** · PhantomOS doesn't generate copy, launch campaigns, or run analysis. The skills plugged into it do.

### Core principle: standardized data receptacle

PhantomOS is a **receptacle**. Its only role is to maintain brand data in a structured, standardized, exploitable format for any agent.

**Standardized** · the 7 entities have a fixed versioned schema (`_version: "1.0"`), fields tagged by type (`_field_types`), and cross-refs by ID. A brand configured in PhantomOS has exactly the same structure as another, enabling comparison, aggregation, migration.

**Exploitable** · data is pure JSON. Any LLM, any tool, any pipeline can read it without a proprietary SDK dependency. A brand configured today in Claude Code can be consumed tomorrow by GPT-4, a Python pipeline, or a Looker dashboard. The data survives tool changes.

**Receptacle** · action skills (generate a hook, launch a Meta campaign, produce a creative brief) are not part of the receptacle. They plug in and consume the context it maintains. The receptacle has no opinion on what is done with the data, it just guarantees the data is there, structured, and up to date.

### Possible evolution to GraphRAG (V3+)

If data volume and discovery needs justify it, PhantomOS could evolve toward true GraphRAG by formalizing inter-entity relationships as typed edges:

```
brand → HAS_PRODUCT → spec
spec → TARGETS → profile
profile → HAS_OBJECTION → pain_point
pain_point → MATCHED_BY → angle (KB)
```

Which would enable multi-hop queries: "which audiences of my brands have an objection matching an angle I'm not yet using?" Today feasible manually via query-context, but not via automatic traversal.

---

## Field Type System (_field_types)

Every brand JSON file contains a `_field_types` map at top level. It tags each field by data nature:

| Type | Meaning | Example |
|------|---------|---------|
| `observed` | Observable fact, not computed | `proofs.rating`, `pricing.price` |
| `structured` | Framework-applied observation (still factual) | `benefits[].chain`, `market.market_overview.sophistication` |
| `derived` | Computed from other fields | `pricing.gross_margin`, `financials.roas_breakeven` |
| `stated` | Brand's own claims (accepted as-is) | `identity.tagline`, `positioning.value_proposition` |

Note: pre-v2.1 archives may still use the legacy labels `raw` (→ `observed`) and `declared` (→ `stated`). See CHANGELOG v2.1.0.

**Rules for agents:**
- Never write strategy/decisions into any field. Context DB = facts only.
- Derived fields should be computed, not manually filled.
- `_field_types` uses glob patterns (`identity.*`, `market.competitors[].name`).
- Validate skill checks _field_types consistency (check 11b).

**Canon + binary decision tests + examples** : `docs/system/field-types.md`.

## Cascade rules

Some canonical fields cascade across entity levels (brand → audience_tree → profile). The downstream level stores a `derived` resolved value, computed from the upstream cascade. Skills read the resolved field first, fallback to the upstream canon if null.

- **Pattern** : canon defined at brand level (default), optional override at audience_tree level (marketplaces with multi-sided populations), resolved at profile level as a `_field_types: derived` field.
- **Field concerned today** : `purchase_driver` (brand → audience_tree → profile). See `docs/system/schemas/brand.md § Cascade purchase_driver` for the canonical doctrine.
- **Future candidates** : `tone_register`, `target_geo`, `compliance_zone` and any field that varies by audience but defaults at brand level. Promote a field to cascade only when at least one tree-level or audience-level override exists in real workspaces (avoid premature cascade).
- **Skills doctrine** : read the resolved (derived) value first, fallback to brand canon if null. Never edit a derived cascade field manually. Mutation of any upstream level (`brand.{field}` or `brand.audience_trees[].{field}`) must trigger recompute on the downstream profiles via mutation gate (skill `recompute-derived-fields` or hook).
- **Cross-refs** : `docs/system/field-types.md` (sémantique derived), `docs/system/schemas/brand.md`, `docs/system/schemas/profile.md`.

## Data Nature: Reference vs Production

| | Reference | Production |
|---|---|---|
| What | Stable facts about the brand | Generated and tested by operators |
| Volatility | Quarterly | Weekly or continuous |
| Examples | brand.json, spec.json, profile.json | learnings.json entries, session-state.md, reporting |
| Test | Does this data exist BEFORE an operator acts? | Does it result from an action? |

Production data that proves its value **promotes** into reference (e.g. a consistently winning hook → captured in profile.json).

## Dependency Graph

```
Frameworks (mental models)
 ↓ engender
Catalogues (inventoried elements)
 ↓ referenced by
Routing (decision tables)
 ↓ consumed by
SOPs (execution workflows) ← Templates (output formats)
 ↓ validated by
Quality Specs (evaluation criteria)

Conventions (platform rules), transversal, consulted by SOPs
```

---

## Session Relay Protocol

At session start: read `session-state.md` (Activity Log, Open Threads, Active Decisions). If open threads exist, mention proactively. During session: skills auto-append Activity Log (max 30 entries, rolling). At session end: learn-from-session extracts learnings → entities, decisions → session-state.md, corrections → brand files. Update status.json. **Hard rule**: always read at start, never delete (archive only).

### Proposals pending

At session start, after loading session-state.md:
1. Scan the active brand's entities for `_proposals[]` with `status: "pending"`
2. Proposals that match the `auto_accept` criteria in config.json → auto-accept silently, log `action: "auto-accept"` in the event log
3. Remaining proposals (low confidence or untrusted source) → present to the operator in plain language:
 - "Since last time, I have [N] updates to propose."
 - Present each proposal as a readable diff: "I propose to change [field in plain language] from [old] to [new]. Reason: [source]."
 - The operator validates, refuses, or modifies inline in the conversation
4. Never the word "proposal". Never raw JSON. Always operator language.
5. If no proposals pending → mention nothing, go straight to normal flow.

---

## Context Budget

- Brand session: ≤8k tokens (CLAUDE.md + session-state + query results)
- Cross-brand query: ≤15k tokens
- Portfolio review: ≤20k tokens

If exceeded: compress session-state first, then trim reference sections, then cap query results to top 1.

---

## Rules (Full Reference)

- **Offer lifecycle**: "Deactivate offer X" → `active: false` + `active_until: today`. Never delete. "Reactivate" → `active: true`.
- **ENRICH > CREATE**: Query `index.json` before creating. >80% tag overlap = enrich existing.
- **One type per file**: Never mix resource types.
- **Reference by ID**: Catalogues use `{PREFIX}-{NN}`. All cross-refs use IDs.
- **Ramification**: Catalogues >12 entries → tag `[RAMIFY]`. SOPs >20 steps → split.
- **Context DB is facts only**: No strategy in brand entity files. Operational learnings → `learnings.json` (append-only, never delete, archive with `status: "archived"`).
- **Credentials are gitignored**: `credentials.env` and `credentials_shared.env`. Never commit.
- **OS files auto-maintained**: status.json, workspace-status.json, session-state.md · rebuilt by skills. Manual edits overwritten.
- **promote-backlog.json** · artefact OPTIONNEL, écrit par `validate-resources` Check 12b UNIQUEMENT si un `validate all` cross-brand détecte un candidat. Absent d'un workspace fresh. `promote-learning` gère son absence gracieusement (ne suppose jamais son existence).
- **Never load `sources/` in context**: Raw file archive. Access only on explicit request.
- **Never invent resource types**: 7 types are fixed. New type = structural decision + approval.
- **Never write to `_TEMPLATE/` or `_EXAMPLE/`**: Read-only references.
- **Field stability**: Renaming a stable field = major version bump + `[BREAKING]` tag.

### Where Does It Go?

```
Reusable by other brands? → resources/{type}/
Brand-specific data? → brands/{slug}/{entity}
Operational rule/finding? → brands/{slug}/learnings.json (use capture-learning)
Active campaigns? → resources/templates/campaigns-active.json
```
Full decision tree: `resources/guides/where-does-it-go.md`.

### Building Skills

Skills consuming PhantomOS context → read `cookbook.md` (same folder) first. Covers: load order, null field behavior, index-first for learnings.

### Roadmap

Planned evolutions in `roadmap.md` (same folder) P1-P3.

---

## Connectivity Pattern · Tool Registry

PhantomOS has no permanent auto-sync with external platforms (Meta Ads, Shopify, Klaviyo, GA4, Notion, ClickUp, calendar). But Claude Code **can natively call any API** when a skill needs it. Full pattern:

1. **On demand**, operator asks *"weekly Meta reporting"* → agent checks if it has the key → if not, asks, operator hands it once → no more back and forth.
2. **Persistence**, tokens/API keys in `credentials.env` (gitignored, brand-level) or `credentials_shared.env` (workspace-level). Once configured, it's set.
3. **Assisted setup**, the agent guides the connection (scopes, endpoint, permissions), not *"hand me the key and figure it out yourself"*.
4. **Doc gate mandatory before setup**, see `CLAUDE.md § Build → Execute gates (Gate 1: Access)`. The agent reads the official docs (WebFetch) and fills `resources/conventions/{platform}.json` BEFORE touching a token: rate limits, OAuth scopes, known pitfalls.
5. **Persisted conventions**, `resources/conventions/{platform}.json` filled over time. Reusable cross-brand, shareable via Git.
6. **One-time setup**, once per platform. Next time the agent uses it directly without re-asking.

**Reply script · when the operator asks "can you connect to my spaces?"** Never *"no live connectors in V1"* (product false-negative). Reply:

> *"No permanent auto-sync, but I connect natively on demand when a skill needs it. Example: you ask [adapted scenario] → I ask for your token once → you hand it → I file it locally → next time I'm operational direct. Same pattern for [2-3 relevant platforms]. Want to connect a platform now, or keep going without for now?"*

---

