---
name: scaffold-entity-files
type: curator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Writes the physical files of a new custom entity
  (schema.json + README.md + optional example instance) or a sidecar file
  (`{entity}.extensions.json`) into the brand's workspace. All writes via mutation gate.
  Does not touch `.skills/` · the skill stub scaffold is handled by scaffold-skill-stub.
  Invoked by scaffold-extension Phase 7.
  FR: "scaffold les fichiers" "écris les fichiers de l'entité" "crée les fichiers extension".
  EN: "scaffold entity files" "write entity files" "create extension files".
permissions:
  reads: [brand]
  writes: [brand.custom, brand.extensions]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: draft schema passed Phases 4-6 validation
  postconditions: files on disk, schema canon-compliant, ready for registration
---

# Skill: Scaffold Entity Files

Writes the files of a new extension into the brand workspace. Split from `scaffold-skill-stub` to keep type clean: this skill touches only `brands/{slug}/custom/` and `brands/{slug}/{entity}.extensions.json`, never `.skills/`.

## Method

Depending on the extension class (custom entity or sidecar), execute one of the two paths.

### Path 1 · Custom entity

Write three files to `brands/{slug}/custom/{entity_type}/` via `.skills/write-to-context.py`:

1. **`schema.json`** · the validated draft from Phase 6. Pretty-printed, 2-space indent, final newline.
2. **`README.md`** · canonical template:
   - Title: entity type name
   - Purpose (one-paragraph, from Phase 1 intent)
   - Cross-references (from Phase 5, listing each declared ref with its resolution)
   - Writing convention (operator-facing guidance on how to mutate · see `docs/system/extending.md § Writing to custom entities`)
   - Index.json registration snippet (as reference)
3. **Instance file(s)** (conditional) · two cases:
   - **Mode intent-first** · no `provided_data` passed. Optionally write a single empty or example-template `{example_slug}.json` only if the operator requested a starter file. Otherwise skip.
   - **Mode data-first** · `provided_data` passed from Phase 1. **YOU MUST** populate one or more instance files from that data. Shape decides the count: `instance_per_item` → one file per item (slug derived from the item's key identifier), `time_series` → one file with the series appended, `aggregate` → one file holding the aggregate. Every populated field carries its `_field_types` mark (`observed` for data the operator brought, `derived` for anything computed). Halt if the data cannot be mapped to the validated schema and surface the mismatch to the orchestrator.

### Path 2 · Sidecar

Write a single file to `brands/{slug}/{entity}.extensions.json` via `.skills/write-to-context.py`:

1. **The sidecar file** · contains `_version`, `_schema`, `_extends: "{core_entity}"`, `_field_types`, and the operator-provided initial field values. In **mode data-first**, the initial values come from `provided_data`; in **mode intent-first**, the fields are empty or defaulted.

No README, no folder · sidecars are convention-discovered, not registered. Single file alongside the core entity.

## Output to orchestrator

```
{
  "class": "custom_entity | sidecar",
  "paths_written": ["..."],
  "status": "ok | partial | failed",
  "instance_count": 0 | 1 | N,
  "populated_from": "none | provided_data"
}
```

## Hard rules

- Mutation gate on every write. Never direct JSON/md edits.
- Never touch `.skills/` · that namespace is `scaffold-skill-stub`'s responsibility.
- If a file already exists at the target path, halt and surface to operator. Do not overwrite.
- After each write, the root CLAUDE.md mutation rule auto-triggers `validate-resources` on the brand. Do not re-trigger explicitly here.
