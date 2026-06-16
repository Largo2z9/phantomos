---
name: ingest-resource
type: curator
version: "1.1.0"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
reasoning_pattern: null
description: >
  Ingests raw content (notes, articles, transcripts, existing files, copy-paste),
  classifies into typed JSON resources OR brand context, writes to the correct folder,
  and updates the central index. Fully autonomous · no operator confirmation required.
  FR: "ingest" "ingère ça" "ajoute cette ressource" "range ça" "transforme en ressource" "mets ça dans la KB" "digère ce doc" "ajoute ces données".
  EN: "ingest" "add resource" "store this" "add to KB" "digest this" "add this data".
permissions:
  reads: [brand, product, profile]
  writes: [brand, product, profile, learning]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: none
  postconditions: run validate-resources to reconcile integrity
---

## Tone

Confirm in plain language what was structured. No paths, no JSON, no field names in the conversation. "I added your product info", not "I wrote to spec.json".

# Skill: Ingest Resource

Single entry point for ALL content entering the workspace.
No manual file creation. Every insertion is typed, validated, indexed.

**Responsibility**: ingest = optimistic write (fast, classifies and writes).
validate-resources = authoritative check (slow, reconciles everything).
Do not duplicate checks · ingest does not do cross-ref validation or status.json update. That's validate's job.

---

## Source Hierarchy for Product Snapshot (CRITICAL)

When snapshotting a Shopify store product, sources have different reliability levels. **Always prefer higher-ranked sources.**

### Tier 1 · Rendered page (Chrome / headless browser)
**= Source of truth.** It's what the customer sees.

Extracts: full composition, claims, real pricing (with bundle apps), offer stack, social proof (product rating, review count), scientific studies, comparison tables, safety warnings, labels (made in France, sugar-free, etc.), visuals.

**Why:** Shopify apps (Rebuy, Bold, ReCharge, Fly Bundles) rewrite prices, offers and content on the frontend. The rendered DOM = the only reality.

**How:** Claude in Chrome → `navigate` + `read_page` (depth 3, max_chars 50000). Enough to extract the whole page. `get_page_text` often too large (>50K chars).

### Tier 2 · Shopify API (`/products.json`)
**= Reliable index, unreliable content.**

Reliable: handles, names, variant count, SKUs, images, weights.
Unreliable: prices (bundle apps override on front), description (often truncated or empty), vendor (sometimes = tagline), product_type (often empty), tags (mix of operational + marketing).

**Usage:** Catalogue index (products_index in brand.json with enriched:false). Mapping handles → workspace slugs. Never as source for spec.json or offers.json.

### Tier 3 · Trustpilot / review platforms
**= Raw VoC, complementary.**

Brand-level rating + reviews. Not product-level (unless the platform segments by product). Feeds verbatim_quotes and key_expressions.

### Recommended snapshot-brand workflow

```
1. API /products.json → full catalogue → products_index (enriched:false for all)
2. Pick products to enrich (hero + 1-2 secondary)
3. Chrome read_page on each product page → spec.json + offers.json (enriched:true)
4. Trustpilot scrape → verbatim_quotes + brand.json proofs
5. Cross-ref check
```

**Price rule:** Always document both prices in specs.variants: `price_api` (Shopify JSON) and `price_front` / `price_front_original` (Chrome). If they differ, `price_front` is the source of truth, the API is just an index. Document the bundle app in meta._snapshot_source.

---

## Step 1 · Receive & Classify

Read the full content. First determine: **shared resource or brand context?**

### Brand Context Detection

Content is brand-level when:
- It describes a specific brand's identity, products, audiences, or market
- It contains client-specific data (account IDs, KPIs, reviews, campaign results)
- It's about a named product, audience segment, or competitor

**Brand context routing:**

| Content | Destination |
|---------|-------------|
| Brand identity, positioning, tone, proofs, financials, contacts | `brands/{slug}/brand.json` |
| Market data, competitors, awareness distribution, regulatory | `brands/{slug}/brand.json` → `market` section |
| Product specs, ingredients, mechanism, benefits, proofs | `brands/{slug}/products/{product}/spec.json` |
| Offers, pricing, bundles, promos | `brands/{slug}/products/{product}/offers.json` |
| Audience profile, psychographics, behavior, objections | `brands/{slug}/audiences/{poche}/profile.json` |
| Operational facts: API workarounds, account behaviors, test results, compliance rules | `brands/{slug}/learnings.json` (append to `entries[]`) |
| Annual goals, monthly KPIs, current focus, constraints, budget caps | `brands/{slug}/strategy.json` |

**Learnings entry structure (required fields):**
- `id`: "LRN-{NNN}" (auto-increment from existing entries)
- `fact`: string (the operational learning)
- `platform`: string (meta_ads, shopify, compliance, etc.)
- `date`: YYYY-MM-DD
- `source`: string (d'où vient l'info)
- `tags`: string[] (keywords for cross-ref)
- `status`: "active" (default for new entries)
- `superseded_by`: null (default)
- `genericity`: "brand-specific" | "sector" | "universal" (agent classifies)
- `promoted_to`: null (default, set by promote-learning)

→ Go to **Step 3B** (Write Brand Context).

### Shared Resource Classification

If NOT brand-specific, classify by type:

| Test | Type |
|------|------|
| Lists elements of a domain with properties per entry | `catalogue` |
| Says what to choose based on context (decision table) | `routing` |
| Conceptual model, principles, mental framework | `framework` |
| Sequential steps to execute a task | `sop` |
| Binary criteria to evaluate an output | `quality-spec` |
| Technical rules specific to a platform/tool | `convention` |
| Reusable structure/format for producing an output | `template` |

**Mixed content**: Split into separate files · one type per file.
**Tiebreak rule**: If ambiguous between two types (e.g. framework/sop), count the structural elements of each type (numbered steps → sop, levels/dimensions → framework). The type with the most structural elements wins. Log both candidate types in CHANGELOG.

**Decision**: Agent classifies autonomously. Log reasoning in CHANGELOG.md.

---

## Step 2 · Check Existing (ENRICH > CREATE)

Read `index.json`. For speed, filter via `stats.by_type` to only read resources of the same type.

For each classified content:

1. Filter resources by same `type` + same `domain`
2. Compare `tags` overlap:
   - **>80% tag overlap** → **ENRICH** (add entries, rows, steps to existing file)
   - **50-80% overlap** → **CREATE** as variant (new file, cross-ref existing)
   - **<50% overlap** → **CREATE** as new resource

For catalogues: check if same domain prefix exists in `id_prefixes`.

**Decision**: Agent decides enrich vs create. Logs in CHANGELOG.md.

---

## Step 3A · Write Shared Resource JSON

1. **Load schema**: `resources/schemas/{type}.schema.json`
2. **Build JSON** conforming to schema:
   - `meta.created` = today (new) or preserved (enrich)
   - `meta.updated` = today
   - For catalogues: generate IDs using prefix from `index.json.id_prefixes`
   - For SOPs: enforce `steps.length <= 20` (split into sub-SOPs if over · set `meta.parent_sop` on children, `meta.sub_sops[]` on parent)
   - For catalogues with `entries.length > 12`: add tag `[RAMIFY]` · validate will flag
3. **Write file** to `resources/{type}/{slug}.json`
4. **Cross-references**: Populate `refs` fields. Update referenced files too.

**Naming conventions**:
- Catalogues: `{domain-noun}.json` → `angles.json`
- Routing: `{dim1}-{dim2}.json` → `awareness-angle.json`
- Frameworks: `{slug}.json` → `awareness-levels.json`
- SOPs: `{verb}-{object}.json` → `piloter-cos.json`
- Quality specs: `{output-type}.json` → `hook.json`
- Conventions: `{platform}.json` → `meta-ads.json`
- Templates: `{output-type}.json` → `brief-crea.json`

---

## Step 3B · Write Brand Context

1. **Identify brand slug** from content or ask once if ambiguous
2. **Auto-create folders**: If the destination folder doesn't exist (product or audience not declared at setup), create it automatically:
   - Product: create `brands/{slug}/products/{product_slug}/`, copy `_TEMPLATE/products/_example/spec.json` and `offers.json`, update `meta.slug`
   - Audience: create `brands/{slug}/audiences/{audience_slug}/`, copy `_TEMPLATE/audiences/_example/profile.json`, update `meta.slug`
3. **Read existing file** at destination (if exists)
4. **Classify each field change**:
   - **New data** · field was null, new value available
   - **Update** · field had a value, the new one is different (mark ⚠)
   - **Identical** · same value → ignore, don't show in recap
5. **Always show a recap before writing**:
   ```
   Here's what I'll save for {brand}, {entity}:

   + New: description → "..."
   + New: pricing.price → 44€
   ~ Updated: benefits[0] → "formula B" (was "formula A")

   Good?
   ```
   Wait for "yes" / "ok" / "go". If the operator corrects a field → apply, reshow recap, reconfirm.
6. **Never write before explicit confirmation.**
7. **Respect _field_types**: Check the file's `_field_types` map. Never write strategy/decision data into context files. Derived fields should be computed, not manually filled. **If a written field doesn't exist in `_field_types`** → add it with the appropriate type (`raw` by default, unless clearly computed → `derived`). Never write an unmapped field without registering it.
8. **Sync products_index**: When writing to `products/{slug}/spec.json`, check `brand.json.products_index[]`. If the product slug is not listed, add it with `name` from spec.meta.name and `role: "secondary"` (operator can change later).
9. **Write via delegated encoding** (`encode-batch` sub-agent, Haiku) so the main thread stays responsive when the batch exceeds ~5 mutations. Producer (ingest-resource) extracts the semantic signals from the recap, packages them as observations, launches encode-batch via Task tool. Sub-agent maps each `semantic_kind` to a `field_path`, runs `write-to-context.py` per mutation, rebuilds the snapshot, runs `finalize-mutation-batch.py`. Returns a structured summary (mutations_count, files_touched, unmapped, finalize_exit_code).

For batches ≤ 5 mutations, calling `write-to-context.py` directly inline is acceptable (sub-agent overhead not worth it):

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/{entity-path}#{json-pointer}" \
  --value '{JSON-encoded value}' \
  --source {operator|scrape|inference|import} \
  --confidence {0.0-0.9 for agent, 1.0 for operator} \
  --mode {direct|proposed} \
  --reason "1-line rationale"
```

- `--mode proposed` ONLY for dict values (stamps `_proposed/_source/_confidence` in-place). Scalars and arrays use `--mode direct` (metadata preserved in event log).
- Writes to gated paths (`products/{slug}/spec.json`, `products/{slug}/offers.json`, `audiences/{slug}/profile.json`) require a resolved checkpoint · see `.skills/stage-proposal.py` and snapshot-brand Step 1/5 for the stage-then-ask pattern. If ingest-resource wants to write to a gated path without going through a preceding snapshot-brand run, stage a proposal first.
- Edit, Write, `python -c json.dump`, `echo >`, `sed -i`, `tee` are all blocked by mutation-guard. Surface the script's error to the operator if it blocks; never bypass.
- encode-batch full contract: `.skills/skills/encode-batch/SKILL.md`.

10. **Store raw source** in `brands/{slug}/sources/` if applicable

**Multi-entity split**: If the source content contains information about multiple entities (brand + product + audience mixed in a single brief), split into separate writes · one per entity target. Log the split in CHANGELOG.

Note: cross-ref validation (profile.pain_points[].ref → spec.problems_solved[]) and status.json completeness update are handled by validate-resources, not here.

### VoC (Voice of Customer) protocol

When ingested content is VoC (customer reviews, verbatims, reviews, SAV returns, surveys):

**Principle: raw → sources/, synthesis → entities.**

Raw VoC (review dump, CSV export, comment capture) is stored in `brands/{slug}/sources/`, never loaded into context, never injected directly into entities. What enters entities is only the **synthesis**:

| VoC data | Receptacle | Field | Type |
|---|---|---|---|
| Raw customer quotes (verbatim) | `spec.json` | `problems_solved[].verbatim_quotes` | `raw` |
| Recurring vocabulary (words, expressions) | `profile.json` | `voice.key_expressions` + `voice.vocabulary_to_use` | `raw` |
| Objections formulated by customers | `profile.json` | `objections[]` | `raw` (phrasing) + `structured` (type, frequency) |
| Pain points formulated by customers | `profile.json` | `pain_points[].formulation` | `raw` |
| Product issues (quality, shipping, support) | `learnings.json` | new entry with `type: "behavior"` | `raw` |
| Category signals (not brand-specific) | `brand.json` | `market.external_intelligence[]` | `raw` · **that's VoM, not VoC** |

**VoC / VoM separation rule:**
- VoC = what **this brand's** customers say. Feeds spec + profile + learnings.
- VoM = what the **market** says (competitor customers, category forums, trends). Feeds brand.market.external_intelligence.
- If a customer verbatim mentions a competitor → VoM.
- If a customer verbatim describes their experience with THIS product → VoC.

**Synthesis rule:**
- Never dump 500 raw quotes into `verbatim_quotes` or `key_expressions`. Max 10 representative quotes per field.
- Select quotes that illustrate a pattern (frequency), not outliers.
- Every pain_point, objection, or benefit added from VoC must have `_source_meta.origin: "voc"` to distinguish from brand copy (declared).
- `verbatim_quotes` are now object[]: each quote carries `{text, platform, rating, sentiment}`. Never insert a raw string.
- `key_expressions` carry `frequency` AND `sample_size`. Both required together. frequency alone = unusable.

**Merge policy (recurring mining):**

When re-mining the same source (e.g. Trustpilot at +6 months), the agent does NOT overwrite existing data. Procedure:

1. **Identify the cycle**: increment `_source_meta.date_captured` on new entries. Old date stays on old entries.
2. **Compare, don't replace**: read existing pain_points/objections/key_expressions BEFORE writing. If an existing pattern is confirmed by the new mining → update `sample_size` and `frequency` (values from new mining, not cumulative). If an existing pattern no longer appears → do not delete, add `_source_meta.status: "unconfirmed_latest"`.
3. **Quality rotation**: if the new mining finds a more representative verbatim/expression than an existing one (higher frequency, sharper phrasing), it REPLACES the weaker entry. The cap of 10 stays · it's a dynamic ranking, not FIFO.
4. **sample_size = always the latest pass**, never cumulative. Cumulative is computable via `sources/` if needed.
5. **Mining report**: each VoC pass produces a report in `sources/voc-{source}-{date}-report.md` documenting: number of reviews analyzed, patterns found, entries added/replaced/confirmed, co-occurrences detected, VoM signals redirected to external_intelligence.

**Operational flow:**
```
1. Operator pastes VoC (reviews, verbatims, CSV export)
2. Store raw in sources/ (file named: voc-{source}-{date}.{ext})
3. Read existing entities (profile.json, spec.json), know current state
4. Analyze: extract patterns (objections × frequency, pain points × phrasing, vocabulary)
5. Compare: match with existing, identify confirmed / new / disappeared
6. Synthesize: write patterns to profile.json + spec.json (merge policy above)
7. Produce mining report in sources/
8. Recap with source labels (✓ direct VoC / ⚠ inferred / ✗ missing)
```

---

## Step 4 · Update Index & Log

1. **Update `index.json`** (shared resources only):
   - Add/update entry in `resources[]` array
   - Update `stats.by_type` and `stats.total_resources`
   - Update `id_prefixes` if new catalogue
   - Set `last_updated` to now

2. **If writing to brand context**: Append activity log line to `session-state.md`:
   ```
   [{date} {time}] ingest: {1-line summary} → {files changed}
   ```
   Also update `status.json.last_activity` to ISO timestamp (now).

3. **Append to `CHANGELOG.md`**:
```
## {date} · Ingest

**Source**: {description of raw content}
**Action**: {CREATED | ENRICHED} {resource | brand context}
**Files**:
- [{type}] {path} · {short description}
**Decisions**: {classification reasoning, enrich vs create, tiebreak if applicable}
```

---

## Step 5 · Summary Output (MANDATORY)

After every ingest, display a structured summary to the user. This is the transparency layer · the user must see what was understood, what was inferred, and what's missing.

### Format · Brand Context

```
Ingest done. {N} entity(ies) updated.

What was enriched:
→ {entity} ({file_path}): {field1} ok, {field2} ok, {field3} +{N} new entries
→ {entity2}: no field enriched, the resource didn't carry info on this point

What's still missing:
→ {missing_field_1}, important for {concrete use}
→ {missing_field_2}, optional, enrich later

Next step: "{suggested ingest command for highest-impact missing field}"
```

Rule: zero JSON path in the operator diff. Name entities in natural language (e.g. "your customer profile", "the Glow Boost product sheet"). Paths stay in CHANGELOG only.

### Format · Shared Resource

```
Resource ingested. {action: CREATED | ENRICHED}

Type: {resource_type} | Domain: {domain}
File: {path}
Entries: {count} ({new_count} new, {enriched_count} enriched)
Tags: {tags}

{If ENRICHED}: Entries added to {existing_file} (was {old_count}, now {new_count})
{If CREATED}: New resource. Index updated.
```

### Inference labeling

When ingest makes an assumption (classifying content, inferring a field value, choosing between two possible entities), label it explicitly:

- `✓` = written from explicit user input (high confidence)
- `⚠ inféré` = deduced by agent, may be wrong (medium confidence)
- `✗ manquant` = required field not filled, needs user input

**Hard rule**: NEVER end an ingest silently. Always display the summary. The user must know what happened.

**Validate hint**: if this ingest modified ≥2 distinct entities (e.g. brand.json + spec.json + profile.json in the same run), add at the end of the summary:
```
You updated {N} entities. Run "validate" to check cross-consistency.
```
If only 1 entity modified → no validate mention (too light to justify).

### Completeness calculation

Count non-empty required fields / total required fields per entity. Round to nearest 5%.
- brand.json required: meta.name, identity.url, positioning.value_proposition, tone_of_voice.style
- spec.json required: meta.name, pricing.price, benefits (≥1), problems_solved (≥1)
- profile.json required: meta.name, demographics (≥1 field), psychology.pain_points (≥1)
- offers.json required: meta.product_slug, offers (≥1 entry with type + price)
- strategy.json required: annual_goals (≥1), current_focus
- learnings.json: count entries (not percentage-based)

---

## Call from learn-from-session

Input: qualified insight + suggested type + target
Entry point: Step 2 (already classified)
Common patterns:
- New catalogue entry → enrich existing catalogue
- New routing row → add to existing routing table
- Generic platform learning (applies to any brand) → `resources/conventions/{platform}.json`
- Brand-specific operational learning → `brands/{slug}/learnings.json` (append entry with fact, platform, date, source, tags)

---

## Hard Rules

- **Never create "Master" files** mixing types · always split
- **Never invent IDs** that exist · check `index.json.id_prefixes`
- **Never inline catalogue content** in routing or SOP · reference by ID
- **Minimum 3 entries** for a catalogue · below threshold, add entries with tag `[DRAFT]` and still write the file (no staging area)
- **Never modify schemas** · if content doesn't fit, type is wrong
- **Never ask the operator** for classification · decide and log
- **Always validate JSON** against schema before writing
- **Brand context is facts only** · no strategy, ops, or decisions in brand files
- **Never update status.json or run cross-ref checks** · that's validate-resources

---

## v1.8 Field Awareness (2026-04)

The `_TEMPLATE` is at v1.8. When ingesting a page/PDF/transcript that describes a product, if info exists on these dimensions, capture it in spec.json or offers.json:

**spec.json · v1.8 fields:**
- Structured composition (`specs.composition[]` with ingredient/pct/origin/inci)
- Posology (`specs.posology` · dosage, timing, duration)
- Contraindications (`specs.contraindications` · conditions, meds, pregnancy, breastfeeding)
- Origin (`specs.origin` · country, region, facility, local_supply_pct)
- Production method (`specs.production_method`)
- Preparation (`specs.preparation` · food)
- External DB IDs (`specs.external_databases` · OFF, Yuka, INCI Beauty, CIQUAL, EAN/GTIN)
- Target suitability (`specs.target_suitability` · skin_types, hair_types, body_areas)
- Durability (`specs.durability` · warranty, repairability · apparel/hardware)
- Nutri-Score (`nutrition_facts.nutri_score_grade` A-E)
- Allergen sources mapping
- Cosmetics PAO (`perishability.period_after_opening_months`)

**offers.json · v1.8 fields:**
- Duration type (calendar/usage_days/servings) + duration_servings
- Cure metadata (cure_name, is_premade, target_concern, phases)
- Duration tiers (incentives per engagement 1/3/6/12)
- Loyalty program (points, tiers, sign_up_bonus)
- Offer-level tags

**New dietary_tags:** caffeine_free, bio, raw, chicory_based, clean_beauty, cruelty_free.

**Rule:** Null > invention. If info is not in the source, leave null and flag `[v1.8_gap]` in ingest notes.
