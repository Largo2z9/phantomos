---
name: register-and-flag
type: curator
version: "1.1.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Registers a newly scaffolded custom entity in
  the scope-routed registry `{scope}/_extensions.json` (NEW canon v2.75.0) and adds
  a tracking entry to `brands/{slug}/todos.md`.
  Sidecars are skipped (convention-discovered, not indexed). Final step of the orchestrator
  pipeline before operator-facing confirmation.
  Invoked by scaffold-extension Phase 9.
  FR: "register cette extension" "enregistre dans l'index" "flag pour adoption".
  EN: "register extension" "register in index" "flag for adoption".
permissions:
  reads: [index, brand, extensions_registry]
  writes: [extensions_registry, brand.todos]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: files scaffolded (Phase 7), optional skill stub created (Phase 8)
  postconditions: extension registered, adoption todo flagged, post-write validate-resources auto-triggered
---

# Skill: Register and Flag

Closes the scaffold pipeline by registering the new extension in the scope-routed registry and flagging it for adoption in the brand's todos.

## Pipeline · v1.1.0 (v2.75.0 NEW canon paths)

### Step 1 · Identify target registry by scope

Read Phase 1 scope from scaffold-extension upstream (brand/operator/workspace).

Selon scope ·
- **brand scope** · target = `brands/{slug}/_extensions.json`
- **operator scope** · target = `operator/_extensions.json`
- **workspace scope** · target = `resources/_extensions.json`

Si registry file n'existe pas (premier extension dans ce scope) · créer avec schema canon `extensions_registry/1.0` + array vide extensions[] · puis ajouter NEW entry.

### Step 2 · Build NEW entry

Construct registry entry from scaffold-extension Phase 9.b auto-detection output + Phase 9.c operator validation ·

```json
{
  "entity_id": "{computed}",
  "entity_type": "{from Phase 1 intent}",
  "scope": "{from Phase 1}",
  "data_shape": "{from Phase 1}",
  "consumable_by": ["{from Phase 9.c operator validated}"],
  "schema_path": "{from Phase 3 propose-schema-draft}",
  "instance_path_pattern": "{from Phase 7 scaffold-entity-files}",
  "owner_skill": "{from Phase 8 scaffold-skill-stub if applicable, null otherwise}",
  "cross_refs": "{from Phase 5 check-cross-refs}",
  "scaffolded_at": "{ISO 8601 timestamp now}",
  "scaffolded_by_skill_version": "scaffold-extension v1.3.0"
}
```

### Step 3 · Idempotent write

Append entry à `extensions[]` du registry file target. Skip duplicate si `entity_id` already present (idempotent).

### Step 4 · Backward compat read fallback

Pendant transition v2.75.0 → v2.76+ · si NEW canon `_extensions.json` absent ET legacy `index.json → extensions[]` existe · lire legacy en fallback. Pas écrire dans legacy (forward only). Migration manuelle backlog si opérateur veut migrer existing legacy entries.

### Step 5 · Surface to operator

Output canon ·
```
NEW entity registered · {entity_id}
  scope · {brand/operator/workspace}
  consumable_by · [{orchestrateurs auto-discovery enabled}]
  registry path · {scope}/_extensions.json
  
Next invocation des orchestrateurs production listés peut consommer
cette entity automatiquement via extension_hooks + Step 0 DRGFP scan.
```

### Step 6 · Adoption flag in todos

Add an entry to `brands/{slug}/todos.md → ## In Progress` ·

> *"[ ] Add your first entry to `{entity_type}` · created today. Capture at least one in the next 7 days to confirm the shape works. If blocked, revisit the setup."*

Two weeks later, if no instances exist, a future `validate-resources` run will flag the extension as `[UNUSED]` candidate for review.

### Step 7 · Post-write auto-validate

The root CLAUDE.md mutation rule automatically triggers `validate-resources` on the brand after any write to `custom/`, `.extensions.json`, or `_extensions.json`. This step does not re-trigger explicitly · just notes the expectation so the orchestrator can surface the result.

## Output to orchestrator

```
{
  "indexed": true | false,
  "registry_path": "{scope}/_extensions.json",
  "todo_added": true,
  "validate_result": "passed | flagged | critical",
  "flags": []
}
```

## Hard rules

- Mutation gate on all writes.
- Sidecars never indexed. If the orchestrator passes a sidecar here by mistake, skip indexing and return `indexed: false`.
- Never write to registry without matching schema file existing on disk (prevents ghost entries).
- Never create the todos.md entry if one with the exact same extension name already exists (idempotent).
- Forward writes uniquement vers NEW canon `_extensions.json` scope-routed · jamais réécrire legacy `index.json → extensions[]` (read fallback only).

## Related canon

- `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW (doctrine canon registry + consumable_by + auto-discovery)
- `resources/schemas/extensions-registry.schema.json` v1.0 NEW (schema canon registry file)
- `scaffold-extension` v1.3.0+ Phase 9 (upstream caller · NEW canon paths target)
- `docs/system/extending.md` (doctrine extension layer · NEW canon paths section post-v2.75.0)
