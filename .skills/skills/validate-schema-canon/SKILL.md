---
name: validate-schema-canon
type: curator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Validates a draft schema against canon conventions
  before any file is written: `_version`, `_schema`, `_field_types` (with enum constraint),
  required core fields, no override of core fields for sidecars. Pre-write guard.
  Reuses the logic of validate-resources check 16 applied before scaffold.
  Invoked by scaffold-extension Phase 6.
  FR: "valide le schema canon" "check schema canon" "vérifie la conformité canon".
  EN: "validate schema canon" "check schema canon" "verify canon compliance".
permissions:
  reads: [resource, brand]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: draft schema from Phase 3 + reuse decisions from Phase 2
  postconditions: canon-compliant schema approved, or operator notified of violations
---

# Skill: Validate Schema Canon

Pre-write validator that refuses schemas not complying with canon conventions. Applies the logic of `validate-resources` check 16 before the extension is actually scaffolded.

## Method

1. **Top-level canon** · verify the draft contains:
   - `$schema` (JSON Schema draft-07)
   - `_version` field with `const` constraint
   - `_schema` field with `const` equal to the entity type name
   - `_field_types` object with enum on values (`observed | stated | derived | structured`)
   - `required` array containing at least `_version`, `_schema`, `meta`

2. **Sidecar-specific** · if the draft is a sidecar:
   - `_extends` field present at top-level, pointing to a valid core entity name
   - No properties redeclare fields already in the core schema (load core schema from `resources/schemas/` and diff)

3. **Structural hygiene** · check:
   - `additionalProperties: false` on nested object types where a bounded shape is expected
   - `pattern` constraints on slug-like fields (`^[a-z0-9-]+$`)
   - `format` constraints on date fields (`date-time`)

4. **Collect violations** · each violation has a severity: CRITICAL (blocks scaffold) or WARNING (flagged, operator can accept).

## Output to orchestrator

```
{
  "status": "pass | warning | fail",
  "violations": [
    {"severity": "CRITICAL | WARNING", "field": "...", "reason": "..."}
  ]
}
```

On FAIL, surface to operator with the specific violation and a suggested fix. Do not scaffold until the draft passes.

## Hard rules

- CRITICAL violations block the scaffold entirely. No override without manual operator intervention.
- Enum on `_field_types` values is mandatory · prevents silent drift to arbitrary type strings.
- Sidecar field-override check is non-negotiable · breaks append-only discipline otherwise.
