---
name: encode-batch
type: curator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
operator_facing: false
description: >
  Sub-skill invoked by producer skills (snapshot-brand, ingest-resource, mine-voc Layer B,
  mine-vom Layer B) to batch-encode N observations into N write-to-context calls without
  blocking the main thread. Producer extracts semantic signals, encode-batch maps them to
  field paths and stamps them. Mechanical mapping work, Haiku-grade. NOT invoked by
  operator directly.
  FR: "encode batch" "encode ces mutations" "écrit le batch en arrière-plan".
  EN: "encode batch" "encode mutations" "background encode".
permissions:
  reads: [brand, product, profile, learning, strategy, schema]
  writes: [brand, product, profile, learning, strategy]
  emits_events: [coherence_check]
  mode: direct
  subagent_safe: true
invocable_by:
  - snapshot-brand
  - ingest-resource
  - mine-voc
  - mine-vom
  - deepen-brand-context
disambiguates_against:
  finalize-mutation-batch: "finalize-mutation-batch is post-write structural check (Python primitive, no LLM). encode-batch is the write itself, Haiku-grade mapping observation → field_path → write_to_context call. Pipeline: producer extracts → encode-batch writes → finalize-mutation-batch verifies."
  write-to-context: "write-to-context is the single-mutation primitive. encode-batch wraps N write-to-context calls in one delegated execution so the main thread stays responsive."
---

> v2.32 reclassement : mode proposed vers direct. Utilitaire interne write loop, pas un proposal opérateur-facing. Mode direct = exécution immédiate sans operator gate.

## Tone

No operator-facing output. Sub-skill returns a structured JSON summary to the caller. The caller decides what (if anything) reaches the operator.

---

# Skill: encode-batch

Mechanical mapper. Receives N semantic observations, maps each to a `field_path` against the target schema, calls `write-to-context.py` per mutation, returns a structured summary. Haiku-grade because the cognitive work (extracting what counts as a pain, a benefit, a verbatim) was done upstream by the producer. This skill maps; it does not interpret.

**Why this exists.** Producer skills (snapshot-brand, ingest-resource) used to encode 15-50 mutations sequentially in the main thread. Visible lag for the operator. encode-batch absorbs that lag in a sub-agent, returns a one-line summary to the producer. Producer ships the operator-facing synthesis without waiting on field-by-field mapping.

---

## Input contract (from caller)

The caller MUST pass a single JSON payload via the Task tool prompt. Schema:

```json
{
  "brand_slug": "{slug}",
  "target_entities": [
    {"file_path": "brands/{slug}/products/{p}/spec.json", "schema": "resources/schemas/spec.schema.json"},
    {"file_path": "brands/{slug}/audiences/{a}/profile.json", "schema": "resources/schemas/profile.schema.json"}
  ],
  "observations": [
    {
      "semantic_kind": "product_name | product_category | pain_point | benefit | objection | key_expression | tone | value | belief | trigger_event | offer_price | offer_savings | objection_frequency | review_count | trust_badge | etc.",
      "raw_value": "<string | number | object>",
      "evidence": "<one-line trace: where did this come from, e.g. 'scrape: products/{handle}.js title field' or 'voc: 3 Sephora reviews + 2 Reddit threads'>",
      "source": "scrape | inference | operator | import",
      "confidence_signal": "literal | partial | inferred"
    }
  ],
  "default_mode": "proposed | direct"
}
```

Observation field semantics:
- **`semantic_kind`** is the producer's classification of the observation. encode-batch uses this to pick the right schema field.
- **`raw_value`** is the literal value to write. Already shaped (string trimmed, number parsed, object structured per the corresponding type schema if applicable).
- **`evidence`** is logged in events.jsonl for traceability. Never operator-facing.
- **`source`** maps directly to `write-to-context.py --source`.
- **`confidence_signal`** maps to a numeric `--confidence`: `literal=0.95`, `partial=0.7`, `inferred=0.5`. Adjust via the table below.

---

## Step 1 · Load target schemas

For each `target_entities[].schema`, read the file. Build an in-memory map:

```
schema_field_index := {
  "spec": {
    "identity.name": {type: "string", _field_type: "observed"},
    "identity.category": {type: "string", _field_type: "observed"},
    "pricing.price": {type: "number", _field_type: "observed"},
    ...
  },
  "profile": {
    "identity.label": {type: "string", _field_type: "stated"},
    "psychology.core_desire": {type: "string", _field_type: "stated"},
    "pain_points[]": {type: "array of pain", _field_type: "structured"},
    ...
  }
}
```

Read the `_field_types` block of the existing target file. Use it as the source of truth for field type when the schema and the file disagree (file wins, doctrine `docs/system/field-types.md`).

---

## Step 2 · Map semantic_kind → field_path

Apply the canonical mapping table. The table is the entire mechanical contract of this skill.

| `semantic_kind` | Target file | Default `field_path` | Notes |
|---|---|---|---|
| `product_name` | spec.json | `identity.name` | scalar |
| `product_category` | spec.json | `identity.category` | scalar |
| `product_format` | spec.json | `identity.format` | scalar |
| `product_description` | spec.json | `identity.description` | scalar, max 500 chars |
| `offer_price` | offers.json | `offer_groups[0].offers[].pricing.price` | append to offers[] |
| `offer_compare_price` | offers.json | `offer_groups[0].offers[].pricing.price_original` | scalar |
| `offer_currency` | offers.json | `offer_groups[0].shared.pricing.currency` | scalar |
| `pain_point` | profile.json | `pain_points[]` | append, full pain object expected in raw_value |
| `benefit` | profile.json | `benefits[]` | append, full benefit object |
| `objection` | profile.json | `objections[]` | append, full objection object |
| `key_expression` | profile.json | `voice.key_expressions[]` | append, full key_expression object |
| `tone_register` | profile.json | `voice.tone_register` | scalar |
| `core_desire` | profile.json | `psychology.core_desire` | scalar |
| `value` | profile.json | `psychology.values[]` | append scalar string |
| `belief_limiting` | profile.json | `psychology.beliefs_limiting[]` | append scalar string |
| `belief_facilitating` | profile.json | `psychology.beliefs_facilitating[]` | append scalar string |
| `emotion` | profile.json | `psychology.emotions[]` | append scalar string |
| `life_moment` | profile.json | `psychology.life_moments[]` | append scalar string |
| `trigger_event` | profile.json | `decision_process.awareness_trigger` | scalar |
| `awareness_stage` | profile.json | `market_position.awareness_dominant` | scalar enum |
| `audience_label` | profile.json | `meta.name` | scalar |
| `audience_gender` | profile.json | `identity.gender` | scalar |
| `audience_age_range` | profile.json | `identity.age_range` | object {min, max} |
| `tag` | profile.json | `meta.tags[]` | append scalar string with namespace |
| `trust_badge` | spec.json | `proofs.authority[]` | append |
| `review_count` | spec.json | `_snapshot.reviews_displayed` | scalar |
| `brand_positioning` | brand.json | `positioning.differentiation` | scalar |
| `brand_tone` | brand.json | `voice.tone` | scalar |
| `brand_value` | brand.json | `positioning.values[]` | append |

**If `semantic_kind` is not in the table** → log to summary as `unmapped`, do NOT invent a field_path, do NOT call write-to-context. Producer can either re-classify and re-call, or accept the loss.

**Override.** Caller may pass `field_path_override` per observation to bypass the table. Use it sparingly · overrides defeat the purpose of the mechanical mapping.

---

## Step 3 · Skip already-filled scalars

Before each scalar write (not array append), read the current value at `field_path`. If non-null and `default_mode == "proposed"` → skip the write, log `skipped_already_set` in summary. Producers that explicitly want to overwrite must pass `default_mode: "direct"` or per-observation `force: true`.

Array appends always proceed (idempotency is the producer's responsibility, not encode-batch's).

---

## Step 4 · Resolve confidence

Map `confidence_signal` to numeric:

| signal | confidence |
|---|---|
| `literal` | 0.95 |
| `partial` | 0.7 |
| `inferred` | 0.5 |

Caller may pass `confidence_override` per observation (numeric 0-1) to bypass.

---

## Step 5 · Emit one write-to-context call per observation

For each mapped observation:

```bash
python3 .skills/write-to-context.py \
  --path "{file_path}#{field_path}" \
  --value '{raw_value as JSON}' \
  --source "{source}" \
  --confidence {confidence} \
  --mode "{default_mode}" \
  --reason "{evidence}"
```

Capture exit code per call. Aggregate into the summary.

---

## Step 6 · Trigger snapshot rebuild + finalize-mutation-batch

After all writes, run once:

```bash
python3 .skills/build-brand-snapshot.py {slug}
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Capture finalize-mutation-batch exit code. If 2 (blocking) → flag in summary.

---

## Step 7 · Return summary to caller

Single JSON object back to caller. NO operator-facing prose.

```json
{
  "brand_slug": "{slug}",
  "mutations_attempted": 27,
  "mutations_succeeded": 25,
  "mutations_skipped_already_set": 1,
  "mutations_unmapped": 1,
  "mutations_failed": 0,
  "files_touched": ["products/hb-bottle/spec.json", "audiences/femmes-30-50/profile.json"],
  "unmapped_observations": [
    {"semantic_kind": "subscription_frequency", "evidence": "scrape: selling_plan.frequency"}
  ],
  "snapshot_rebuilt": true,
  "finalize_exit_code": 0,
  "finalize_warnings": 0,
  "events_logged": 27,
  "elapsed_ms": 4200
}
```

The caller (producer) reads the summary, decides whether to surface anything to the operator (typically only blocking issues), then proceeds to its own operator-facing synthesis.

---

## Hard Rules

- **Mechanical only.** No semantic interpretation. If `semantic_kind` doesn't map, return `unmapped`. Never invent a `field_path`.
- **NOT operator-facing.** `operator_facing: false` enforced. Output is structured JSON to the caller, never prose.
- **One write-to-context call per observation.** Never batch into a single multi-field write. The mutation gate audits one mutation at a time.
- **Skip already-set scalars by default.** Producers that need overwrite must opt in via `default_mode: direct` or per-observation `force: true`.
- **Read schemas + existing file before mapping.** Don't blindly trust the table · `_field_types` on the live file overrides schema hints.
- **Always rebuild snapshot + run finalize-mutation-batch at the end.** Single invocation each, not per-mutation.
- **Never expose `_field_path`, `_source`, `_confidence`, `mode` numbers up the chain.** The summary keeps those internal. The caller may reference counts ("27 mutations encoded") but never the internal stamping.
- **Subagent_safe: true.** Always launch via Task tool with `model: haiku` from the caller. Running encode-batch inline in main defeats its purpose.

---

## Cross-references

- `.skills/skills/snapshot-brand/SKILL.md` · caller, Step 3 + Step 6 delegate here
- `.skills/skills/ingest-resource/SKILL.md` · caller, mapping phase delegates here
- `.skills/write-to-context.py` · single-mutation primitive used internally
- `.skills/finalize-mutation-batch.py` · post-write structural check, run once at end
- `.skills/build-brand-snapshot.py` · snapshot rebuild, run once at end
- `docs/system/field-types.md` · `_field_types` doctrine
- `docs/system/contextual-intelligence.md` · master doctrine, "no semantic interpretation in mechanical layer"

---

## Performance target

Producer skill that previously encoded 25 mutations in 60-120s sequentially in main thread should now ship the synthesis in 5-15s (producer extracts), with the encode-batch sub-agent running in background. Operator perception: the synthesis arrives, the encoding is a footnote ("27 mutations encoded in background, all green"). If finalize-mutation-batch flags a blocking issue, producer surfaces it before close.
