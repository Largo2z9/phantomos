---
name: propose-schema-draft
type: producer
version: "1.0.0"
recommended_model: sonnet
layer: territoire
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Generates a canon-compliant JSON Schema draft
  for a new custom entity or sidecar, based on the captured intent and accepted reuse
  references. Follows `_version`, `_schema`, `_field_types` conventions. Uses patterns
  from `resources/schemas/` and `brands/_TEMPLATE/custom/_EXAMPLE/` as structural reference.
  Invoked by scaffold-extension Phase 3.
  FR: "propose un schema" "draft le schema" "génère le schema draft".
  EN: "propose schema" "draft schema" "generate schema draft".
permissions:
  reads: [resource, brand]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: intent + reuse references from Phases 1-2 available
  postconditions: draft JSON Schema proposed to operator for approval
---

# Skill: Propose Schema Draft

Composes a canon-compliant JSON Schema from the operator's intent.

## Method

1. **Load reference patterns** · read `resources/schemas/brand.schema.json` and `brands/_TEMPLATE/custom/_EXAMPLE/competitor_pricing/schema.json` as canonical examples.
2. **Compose frontmatter** · `$schema` (draft-07), `$id`, `_version: "1.0"`, `_schema` (equals the entity type name), `_field_types` (object with enum constraint on values: `observed | stated | derived | structured`).
3. **Compose required fields** · always include `_version`, `_schema`, `meta` (with `slug` and `created_at`). Add domain-specific required fields based on intent.
4. **Compose properties** · translate each attribute from the intent object into a property with appropriate type, enum, pattern, or `ref` to a registry if Phase 2 identified a reuse.
5. **Apply shape constraints** · time-series implies `observations: array` with `observed_at`. Instance-per-item implies a single object per file. Aggregate implies a single file with collection fields.
6. **Enforce `additionalProperties: false`** on nested objects where appropriate to prevent silent schema drift.

For sidecars: add `_extends: "{core_entity_name}"` at top-level. Do not redeclare fields already present in the core schema.

## Output to operator

Surface the draft in plain language (not raw JSON) before confirmation:

> *"Voici ce que je propose pour ton `{entity_type}`. Champs : {comma-separated list with short descriptions}. Références vers ton contexte existant : {list}. Forme : {historique sur le temps / une entrée par élément / un seul bloc résumé}. Tu valides, tu ajustes, ou tu veux qu'on creuse un champ ?"*

On operator approval, return the JSON Schema object to the orchestrator.

## Hard rules

- Never write to disk from this skill. Draft lives in memory until Phase 7.
- Follow canon conventions strictly · `validate-schema-canon` in Phase 6 will refuse non-compliant drafts.
- `_field_types` values must be one of `observed | stated | derived | structured`. Enum constraint required in the schema itself.
