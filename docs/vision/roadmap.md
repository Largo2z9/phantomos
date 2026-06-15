# Roadmap

Planned evolutions, prioritized P2 (next) and P3 (later). Shipped history lives in [`../../CHANGELOG.md`](../../CHANGELOG.md).

---

## Recently shipped

> **Single source of truth for shipped state** : `_version.json` (template version, 2.90.0 at last release) + [`../../CHANGELOG.md`](../../CHANGELOG.md) for the full log. The S55 entries below are illustrative anchors only ; they are NOT the shipped log and must never be read as "what is or isn't built". This roadmap lists PLANNED evolutions ; when a planned item ships it moves to the CHANGELOG, it never lingers here marked "planned".

- **v2.26.0** · Atlas canon copy foundation. Typed registry of 11 layers × 58 fiches (frameworks, hooks, angles, niveaux-schwartz, archetypes-voix, formules-titres, objections, construction-offre, leads, formats-livrables, persuasion). Sources : Schwartz, Cialdini, Halbert, Sugarman, Hormozi, Carlton, Jung. Storage `resources/canon/copy/{layer}/{tool}.json`, schema `canon-tool/1.0`. D#382.
- **v2.27.0** · Skills consume + feed canon (living atlas). 4 skills refactored : `produce-paid-angles` (Step 0bis loads canon, Step 11 emits explicit lineage), `produce-copy-brief` (reads angle lineage, brief enriches instead of re-deciding), `mine-voc` (verbatims tagged with canon Schwartz / emotion / objection ids), `learn-from-session` (operator-gated canon promotion via `validations[]` append-only). D#383.
- **v2.28.0** · Schemas enriched for compositional cartography. `spec.schema.json#mechanisms[]` (mono to many, typed fields target / mode_of_action / time_window / evidence_level / market_sophistication / triggered_by_specs[]). `angle.schema.json` v1.0 created (formula recursive, origin enum 5 values, awareness_movement {in, out}, meta.validation_status cycle). Templates updated.
- **v2.28.1** · Angle schema v1.1 (10 patches v3.1 from S55 stress test on 23 ads cross-typology). Additive backward-compat fields : `intent` (DR / Brand / Hybrid / B2B_lead_gen), `mecanique` enum 16 values (adds `curiosity_teaser` + `emotional_reframe`), `insight` object (modalité formulé/implicite/absent + status), `seasonality_trigger`, `execution.craft_mode`, `execution.longevity_signal`, `execution.cta` (4-value modality), `_equation_ref` (canonical reference `creative_statique = concept × execution`). D#391.
- **v2.29.0 (shipped, see CHANGELOG)** · `creative.schema.json` materialization (concept vs instance vs variant entity, absorbing execution + classification + variant_of) + reconciliation v3 + v3.1 + nomenclature cleanup (audit S55 distinctions : pain_point ≠ tension ≠ insight ≠ JTBD, Mécanique creative ≠ Mechanism spec, atome_irreductible ≠ perceptual_pivot ≠ stop_scroller).

---

## P2. Next

### Sector-scoped conventions
Add `meta.sectors[]` to conventions. `query-context` filters by the active brand's sector.

### Skills namespace core/ vs custom/
Split `.skills/skills/core/` (shipped with the template) from `.skills/skills/custom/` (added by the operator). Custom may override core.
Impact. Unlocks extension by devs (Hugo use case).

### Batch operations
Bulk multi-brand ops. Credential rotation, template upgrade, seasonal updates.
Impact. Reduces maintenance at scale.

### Brand-slug in child entities
Add `meta.brand_slug` to `spec.json`, `profile.json`, `offers.json` for portability outside the filesystem.
Impact. Unlocks programmatic consumption and data pipelines.

### Audience model v2.0. 3D dimensions + activation scoring
Redesign `profile.schema.json`. Draft in `research/profile-v2.0-proposal/`. Decisions D#237 to D#242 (S30d).

Structural pivots:
- An audience = **named intersection** of 3 orthogonal dimensions. `use_context` times `pain_profile` times `identity` (not a node in a single hierarchy).
- Tree depth **unbounded**. `meta.parent_abstractions[]` array (multiple inheritance, not scalar `parent_slug`).
- **Three activation states** per node. `active` (profile complete, production live), `dormant` (documented, optionality bank, zero production), `contextual` (tag on parent, no own profile).
- **Mandatory focus scoring** (9 dimensions + composite). First-class steering variable, non-neutral, encodes the brand's strategic intent.
- **15% rule** as activation criterion. Measurable delta on 10 profile fields vs parent.
- `refresh_cadence` + `last_refreshed`. Anti-stale discipline for dormants.

Downstream dependencies:
- Audit agents (`mine-audience`, `score-product-fit`) as a distinct "analysis" agent category (D#237).
- `offers.target_audience_id` may point to any tree level (root for broad ads, leaf for segment-aware production).
- Production agents (copy, LP, ads, emails) read only `activation_state: active` nodes.

Impact. Unlocks real audience granularity (kills the "1 audience / 44 orphan offers" gap a la peaktrek), unlocks segment-aware downstream generation, redefines the Context Engine as "structured strategic intent" rather than objective market encyclopedia.

Promotion prerequisites. Red-team the draft + POC agent `mine-audience` on one brand + migrate existing `profile.json` files.

### Agent category split. context / analysis / production / optimization
Formalize the 4 agent categories (D#237). Today the template only carries context + production seed. Analysis and optimization are missing.

- **Context**. Onboarding, manual enrichment. Mutates the Context Engine.
- **Analysis**. `mine-audience`, `score-product-fit`, voice-of-market audit, competitive scan, gap analysis. Produces transient reports, does NOT mutate the Context Engine.
- **Production**. Copy, LP, ads, emails, SEO. Reads only `activation_state: active`. Deterministic.
- **Optimization**. Post-launch perf feedback. Proposes updates to the Context Engine, arbitrated by the operator.

Impact. Gives the operator a reason to come back to the tool beyond onboarding (iterative loop analysis -> decision -> re-production).

---

## P2+. Diagnostics (system observability channel)

**Context.** Past 10 external users, human debriefs do not scale. Need an automatic channel capturing **system dysfunctions** (not operator preferences. That is covered by `learn-from-session` -> `/operator/profile.json`).

**Critical distinction.**
- `/operator/profile.json` (shipped). Preferences, style, tools tested, personal anti-patterns.
- `brands/{slug}/learnings.json` (shipped). Domain learnings (API workarounds, compliance, test results).
- **`_system-issues/`** (to build later). Agent/skill/schema dysfunctions.

### 8 system issue types to log

| Type | Example | Detected by |
|------|---------|-------------|
| `schema_violation` | Cross-ref `pain_point_id: "PRB-03"` absent from spec | validate-resources |
| `skill_failure` | `setup-brand` crashes at Step 3, setup incomplete | skill-telemetry wrapper |
| `workflow_abandoned` | Brand created + audience missing after 24h | validate-resources |
| `agent_hallucination` | Agent proposes a field that does not exist in the schema | post-message check |
| `rule_violation` | Agent uses "assistant" (banned anti-pattern) | post-message check |
| `confidence_mismatch` | Snapshot confidence 40% validated without flag | snapshot-brand skill |
| `infrastructure_error` | `write_to_context` refused (blacklist field), file not written | write-to-context layer |
| `reference_broken` | Offer points to a non-existent `product_slug` | validate-resources |

### Architecture

```
_system-issues/
 issues.jsonl # append-only, 1 line = 1 anonymized dysfunction
 config.json # severity_threshold, opt-in sharing, retention days
 reports/ # markdown bundles exportable on demand
```

### 3 hooks to wire

1. **Extended `validate-resources`**. Append `_system-issues/issues.jsonl` on every broken cross-ref, schema violation, critical staleness (in addition to the current flag in `todos.md`).
2. **`skill-telemetry` wrapper** in the skill layer. Captures abnormal exits, exceptions, workflow violations.
3. **Light post-message check** in CLAUDE.md. Detects broken anti-patterns and ghost paths.

### Skill `export-system-issues`

Produces a markdown + jsonl bundle, **anonymized**, on operator demand. **Zero real business content**. Only mechanical signals.

Example entry:
```json
{
 "ts": "2026-04-18T14:32:00Z",
 "type": "schema_violation",
 "severity": "major",
 "context": "setup-brand step 3",
 "detected_by": "validate-resources check 11",
 "detail": "cross-ref pain_point not found in spec",
 "workflow_state": "brand_created+product_ingested+audience_ingested+validate_failed",
 "session_tour": 14
}
```

### 5 non-negotiable GDPR-friendly rules

1. **Explicit opt-in** at workspace setup (never default).
2. **Automatic sanitization** before export (regex scrub. Emails, domains, proper names, tokens).
3. **Transparency**. User can `cat _system-issues/issues.jsonl` and see exactly what is captured.
4. **Instant opt-out**. Command *"stop tracking"* -> immediate stop.
5. **User-initiated export**. No remote pull. The user pushes the file voluntarily.

### Bonus. Product quality dashboard

Once in place, PhantomOS reliability metrics:
- X% of setup-brand completing without `schema_violation`
- Y% of ingest with confidence > 0.8
- Top 5 skills that crash most often
- Top 3 anti-patterns violated most often

Product signal with no need to ask the user.

### Timing

- **Current alpha (N=2)**. Skip. Human debrief is enough.
- **Public release (10+ unknown users)**. Implement. ~2-3 days of code.
- **Consulting client**. Add skill `share-with-consultant` that pushes to a controlled endpoint.

### Dependencies

None. Independent. Can be built as soon as the alpha is conclusive.

**Total effort.** 2-3 days dev for the 3 hooks + export skill + opt-in doc.

---

## P3. Later

### Monitoring dashboard
HTML/Markdown dashboard generated by `validate --all`. Multi-brand health view.
Depends on. All-brands validation (shipped).

### Custom entities
`brands/{slug}/custom_entities/` folder for non-ecommerce verticals (SaaS, agency, creator). Free schema with imposed structure (meta, _field_types, _version).
Impact. Opens PhantomOS beyond DTC e-com.

### Web onboarding wizard
Local HTML/React form for onboarding without Claude Code. Generates the JSON files directly.
Impact. Unlocks non-technical users (Pierre use case).

### Empirical token benchmark
No public benchmark compares PhantomOS against Claude Projects, ChatGPT Teams, or classical vector-RAG on identical operator tasks today. Structural arguments in `docs/product/fit.md § Cost honesty` rest on measurable primitives (cache savings, re-brief avoided, indexed vs full-dump loading, output-per-token of parametric composition), but the end-to-end proof is missing.

**Plan.** Five operators on comparable profiles (three DTC solo, two senior consultant portfolio). Three months of standardized tasks repeated on PhantomOS and on alternative (Claude Projects or ChatGPT Teams with pasted brief). Instrument token consumption per task, per session, per month. Publish the curve with methodology and raw data.

**Success criteria.** Demonstrate per-task token efficiency past month 2 for anchored work, honest cost premium before that, curve crossover point quantified per profile.

**Dependencies.** Instrumentation wrapper for token accounting across sessions. Five operator volunteers with matched workload. Neutral third-party review of methodology before publication.

**Impact.** Moves the cost argument from structural to empirical. Removes the main commercial objection for operators evaluating adoption.

### Extension layer · `scaffold-extension` orchestrator · SHIPPED

The extension layer (`docs/system/extending.md` · custom entities, sidecar schemas, custom skills, external pipelines + three governance rules) is shipped. The `scaffold-extension` orchestrator (v1.3.0) collapses the manual scaffolding path into a guided operator flow, composing single-responsibility sub-skills (intent analysis, registry reuse suggestion, schema drafting, naming validation, cross-reference checking, canon validation, file scaffolding, skill stub, index registration). It is the live proof of the "no ceiling" thesis : the operator, or the agent on their behalf, grows the data model and the capabilities from inside the workspace.

**Status.** Shipped, built from observed patterns (the adoption gate it once waited on is cleared). Remaining work on this layer is hardening the at-scale guardrails (cross-workspace registry, custom-trigger namespacing, runtime integrity checks), documented in `extending.md § V1 known limits`.

**Impact.** Removes the friction that pushed operators to hack around the workspace. Preserves the governance rules (schema, index, README) that keep extensions interoperable with the core. The promotion path (extensions proving value across operators graduate to vertical packs or core) is live.

### Vertical packs for non-DTC profiles (future+, conditional on demand)

PhantomOS ships with the DTC paid acquisition kit. Vertical packs for other operator profiles are roadmap future+, conditioned on actual client demand from those segments (no anticipated build) :

- **`consulting-core`** · replaces DTC-specific entities with `engagement`, `stakeholder`, `sow`, `milestone`, `deliverable`. Adds skills for client deliverables, pipeline review, methodology productization.
- **`media-buyer-freelance`** · monthly retainer reporting, client dashboard export, cross-account benchmark library.
- **`coach-expert-pack`** · knowledge productization for coaches and experts.

Impact. Opens PhantomOS to operator profiles outside DTC paid once demand from those segments is validated. Not a priority.

### Multi-operator and client-facing layer (future)

PhantomOS runs single-operator per workspace today. This layer wires the multi-tenant architecture for agency operators running multiple DTC clients in parallel :

- **Role-based access** on the workspace (owner, collaborator, read-only).
- **Per-client read-only dashboard** for the agency to share encoded state with its client.
- **Workspace handoff layer** for retainer termination (export client substrate, transfer rules).
- **Simultaneous-session handling** on shared workspaces, conflict resolution on `session-state.md` and `awareness.json`.

Impact. Unlocks agencies with 3+ operators, shared client delivery, clean separation of agency vs client encoded data.

---

## Dependencies

```
MCP server -> independent
Cross-brand query -> MCP server (helps but non-blocking)
Learning promotion -> independent
Monitoring -> all-brands validate (shipped)
Custom entities -> core/custom namespace (helps but non-blocking)
Batch ops -> independent
Brand-slug -> independent (simple migration)
Audience model v2.0 -> independent (blocks audit agents + segment-aware production)
Agent category split -> depends on Audience model v2.0 for mine-audience + score-product-fit
```
