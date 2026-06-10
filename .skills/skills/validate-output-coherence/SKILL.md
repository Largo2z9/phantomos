---
name: validate-output-coherence
type: curator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
operator_facing: false
invocable_by:
  - audit-meta-account
  - setup-brand
  - snapshot-brand
  - onboard-brand
  - ingest-resource
  - "*"
description: >
  Validates an agent output against the brand's facts, tone, and schemas BEFORE
  it reaches the operator. Sub-skill — not invoked by operator directly. Called
  by orchestrators and domain skills as a final gate. Returns a structured
  coherence report with warnings and blocking issues. Does NOT rewrite the
  output — only flags issues; caller decides whether to revise, ship, or block.
  FR: "valide la cohérence de l'output" "check coherence" "vérifie l'output contre la brand".
  EN: "validate output coherence" "check coherence" "verify output against brand".
permissions:
  reads: [brand, product, offer, profile, learnings, strategy]
  writes: []
  emits_events: [coherence_check]
  mode: none
  subagent_safe: true
---

> v2.32 reclassement : type shared vers curator. Skill read outputs, applies coherence rules, governance role (pas une primitive de mutation/validation réutilisable).

## Tone

Structured machine output. This skill returns JSON, not prose. Keep human-facing
commentary in `warnings[].message` fields — concise, actionable, no jargon.

---

# Skill: Validate Output Coherence

The final gate before any skill's output reaches the operator. Answers four
questions, each with a pass/warning/blocking status:

1. **Schema consistency** — does the output reference real fields in brand
   entity schemas, or does it fabricate paths (`brand.mythical_field`)?
2. **Fact consistency** — does the output contradict a stated brand fact
   (positioning, tone, products list, audiences, active offers)?
3. **Tone consistency** — does the output's voice match the declared
   `tone_of_voice.register` / `essence` / `signature`?
4. **No fabrication** — are numbers, claims, and quoted testimonials
   sourced (either from brand data, from a retrieved resource cited by path,
   or explicitly flagged as inferred)?

---

## Input contract

The caller MUST provide :

- `output_text` — the text or structured output about to be shown to the operator
- `brand_slug` — which brand's facts to validate against
- `entity_refs` — list of entities the output draws from (e.g., `["brand", "products/glow-boost", "audiences/core"]`). Loaded for comparison.
- `resource_refs` *(optional)* — list of resources cited in the output (paths from `discover-resources` results). Used for sourcing checks.
- `severity_threshold` *(optional, default `warning`)* — `warning` surfaces everything; `blocking` only flags severe issues that should halt shipment.

---

## Execution steps

### Step 1 — Load brand context

Read :

- `brands/{slug}/brand.json` — identity, positioning, tone_of_voice, products_index
- `brands/{slug}/products/{...}/spec.json` for each product in `entity_refs`
- `brands/{slug}/audiences/{...}/profile.json` for each audience in `entity_refs`
- `brands/{slug}/_snapshot.md` — for quick fact index

### Step 2 — Schema consistency check

Scan `output_text` for JSON-path patterns or field references (e.g. `brand.xyz`, `products.hair_boost.pricing`). For each:

- If the field exists in brand schemas → OK
- If the field does NOT exist → flag `schema_violation`, severity `blocking` (agent fabricated a path)
- If the field exists but in a different entity than cited → flag `schema_misattribution`, severity `warning`

### Step 3 — Fact consistency check

For each stated claim in `output_text`, attempt to match it against brand facts :

- **Product facts** — product names, prices, ingredient lists, formats. Contradiction = `fact_violation blocking`.
- **Positioning** — "premium / mass market / mid-tier" declarations. Contradiction with `brand.positioning` = `fact_violation blocking`.
- **Audience facts** — who buys, demographic ranges, pain points. Contradiction with `profile.json` = `fact_violation warning`.
- **Active offers** — promos, discounts, bundle compositions. If output describes an offer that doesn't exist in `offers.json` = `fact_violation blocking`.
- **Tone declarations** — brand voice, language register. Contradiction = `tone_violation warning`.

### Step 4 — Tone consistency check

Compare output's tonal characteristics against `brand.tone_of_voice` :

- Register match (formal / casual / premium / technical)
- Addressing match (tutoiement vs vouvoiement in French)
- Language match (FR content if brand content is FR)
- Anti-patterns flagged (em dash in runtime output, decorative emojis, agent-speak like "Certainly! I can help…")

Each mismatch = `tone_violation warning` with concrete quote + the brand's declared stance.

### Step 5 — Fabrication check

Scan for :

- Numbers (percentages, currencies, counts) — each must trace to brand data, a resource, or be explicitly labeled `inferred` / `estimated`.
- Quoted testimonials or client reviews — must match `brand.proofs.reviews[]` or `sources/` archive.
- Named competitors, partners, or creators — must exist in `brand.market.competitors[]` or be flagged as new.
- Claims using superlatives ("best", "#1", "most effective") without source = `fabrication warning`.

### Step 6 — Emit audit event (MANDATORY)

Before returning the report to the caller, **YOU MUST** emit a `coherence_check` event so the `turn-end-audit` hook sees the skill ran:

```bash
python3 .skills/emit-event.py \
  --kind coherence_check \
  --payload '{"brand_slug":"{slug}","ok":{true|false},"warnings":{N},"blocking":{N},"entity_refs":[...]}'
```

Skipping this step means the hook treats any entity-field claim in the caller's output as **unchecked** and surfaces a warning on turn end, even if validation passed. Emission is part of the contract, not optional observability.

---

## Output

Structured JSON to stdout :

```json
{
  "ok": false,
  "checks": {
    "schema": {"status": "pass|warning|blocking", "issues": [...]},
    "fact": {"status": "pass|warning|blocking", "issues": [...]},
    "tone": {"status": "pass|warning|blocking", "issues": [...]},
    "fabrication": {"status": "pass|warning|blocking", "issues": [...]}
  },
  "warnings": [
    {"kind": "tone_violation", "quote": "...", "brand_stance": "...", "fix_hint": "..."}
  ],
  "blocking_issues": [
    {"kind": "fact_violation", "claim": "...", "contradicts": "...", "source_path": "..."}
  ],
  "validated_at": "2026-04-23T...",
  "brand_slug": "...",
  "entity_refs_loaded": [...]
}
```

`ok: true` only if zero blocking_issues. Warnings may still exist — caller decides tolerance.

---

## Hard Rules

- **Never rewrite the output.** This skill is read-only validation. Calling skills decide whether to revise or ship as-is with caveats.
- **Never fabricate brand facts to validate against.** If a brand field is empty or missing, the check is `indeterminate` (neither pass nor fail), surfaced in the report.
- **Do not call LLM to "creatively interpret" whether a fact matches.** Literal comparison only, with a small tolerance for paraphrase. If unsure → flag as warning, let operator or caller decide.
- **Severity discipline** — `blocking` is reserved for actual contradictions with brand facts or fabricated schema paths. Style drift and light tone mismatches are `warning`.
- **Report only. Don't act.** No file writes, no mutations, no retries. The only exception is the mandatory `coherence_check` audit event (Step 6) which writes to `.phantom/context-engine-events.jsonl` via `.skills/emit-event.py`, not to brand JSON.
- **Event emission is non-optional.** Step 6 closes the loop with `turn-end-audit`. Skipping it = hook surfaces a false "unchecked entity claim" warning on the caller's turn even when validation passed.

---

## Cross-references

- `docs/system/skill-resource-discovery.md` — explains where this skill fits in the skill execution flow
- `.skills/discover-resources.py` — sibling primitive used by skills BEFORE calling this one
- `.skills/emit-event.py` — audit event channel, invoked in Step 6 to log the `coherence_check` event
- `.skills/write-to-context.py` — canonical mutation channel (this skill reads, never calls it)
- `.claude/hooks/turn-end-audit.py` — reads `.phantom/context-engine-events.jsonl` for recent `coherence_check` events; surfaces warning if entity claim appears without one
- `resources/sops/audit-meta-global.md` — example SOP whose orchestrator should invoke this skill on final output
