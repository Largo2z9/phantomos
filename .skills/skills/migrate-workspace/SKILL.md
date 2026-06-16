---
name: migrate-workspace
type: curator
version: "1.1.0"
recommended_model: sonnet
layer: meta
reasoning_pattern: null
description: >
  Migrates an existing brand instance to match a newer template version.
  Compares instance structure against target template, generates a diff,
  proposes safe modifications (add fields, rename, deprecate). Never deletes data.
  FR: "migrate" "upgrade cette brand" "aligne avec le template" "check drift" "mets à jour la structure" "version mismatch".
  EN: "migrate" "upgrade brand" "align with template" "check drift" "template version mismatch" "sync to latest template".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: [brand, product, offer, profile, learning, strategy]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: brand must exist (setup-brand completed). Target template version known.
  postconditions: validate-resources should run after migration to verify integrity.
---

## Tone

Explique les changements en langage courant : ce qui sera ajouté, ce qui change, ce qui ne bouge pas. Confirmer avant d'appliquer. Jamais de diff technique brut.

# Skill: Migrate Instance

Safely brings an existing brand instance in line with a newer template version.
Handles field additions, renames, restructuring, and deprecations, without data loss.

---

## Pipeline canon v2.80.0+

Skill consommé par `update-workspace` (orchestrator) quand BREAKING détecté dans la chaîne de manifests. Doctrine de référence · `docs/system/update-distribution-doctrine.md` v2.80.0 (Update Distribution Discipline).

**Position dans le pipeline canon ·**

- L'opérateur invoque `/update` (slash command opérateur-facing canon v2.80.0).
- `/update` route vers `update-workspace` (orchestrator).
- `update-workspace` détecte BREAKING dans la chaîne de manifests.
- `update-workspace` délègue à `migrate-workspace` (ce skill, curator) via Task tool.
- `migrate-workspace` consume les scripts du framework `migrations/` (canon v2.80.0 · scripts Python par BREAKING release · 1 script par version BREAKING).

**Framework `migrations/` canon v2.80.0 ·**

Chaque script de migration Python suit le contrat canon · 4 méthodes obligatoires ·

- `check_required(instance_path) -> bool` · détermine si la migration s'applique à l'instance (idempotent · safe à appeler plusieurs fois).
- `run_transformation(instance_path) -> dict` · applique la transformation (additive · deprecate jamais supprime · backup pre-write).
- `validate_state(instance_path) -> dict` · valide l'état post-transformation (integrity check · flags surfacés).
- `rollback(instance_path, backup_path) -> bool` · restaure l'instance depuis le backup pre-migration (`_archive/migrations/pre-v{version}-{date}/`).

**Contrat opérateur-facing canon v2.80.0 ·**

- Idempotent · safe à ré-exécuter sans dommage (check_required gate).
- Backup pre-migration obligatoire `_archive/migrations/pre-v{version}-{date}/` (jamais migration sans backup).
- Rollback path canon · `rollback()` méthode disponible par script.
- Preserve operator state strict · jamais delete data (deprecate via `_deprecated_{name}`).
- Plan présenté à l'opérateur avant exécution (cohérent engagement-disclosure-discipline v2.79.5).

**Anti-patterns stricts ·** migration sans backup · delete data (vs deprecate) · script non-idempotent · absence rollback method · application silent sans plan opérateur.

---

## When to Use

- Template has been updated (new fields, renamed sections, structural changes)
- Operator says "migrate", "upgrade brand", "align with template"
- validate-resources flags `_version` mismatch between instance and template
- Operator deploys a brand from an older template and needs to catch up

---

## Step 1 · Detect Version Gap

1. Read `brands/{slug}/brand.json._version` (instance version)
2. Read `brands/_TEMPLATE/brand.json._version` (target version)
3. Compare. If same → report "already up to date", exit.
4. Repeat for all entity files: spec.json, offers.json, profile.json

Output: list of files with version gaps.

---

## Step 2 · Generate Structural Diff

For each file with a version gap:

1. Read the instance file
2. Read the corresponding _TEMPLATE file
3. Compare structure (keys at all nesting levels):
   - **Added fields**: present in template, absent in instance
   - **Removed fields**: present in instance, absent in template (potential deprecation)
   - **Renamed fields**: heuristic · same position + similar name (fuzzy match)
   - **Type changes**: field was string → now object, array → now nested, etc.
   - **_field_types changes**: new entries, removed entries, type reclassifications

4. Check CHANGELOG.md for `[BREAKING]` tags between instance version and target version

Output: structured diff per file.

---

## Step 3 · Propose Migration Plan

For each diff item, classify and propose action:

| Diff Type | Action | Risk |
|-----------|--------|------|
| Added field (non-required) | Add with empty/default value | None |
| Added field (required) | Add empty + flag in todos.md | Low |
| Renamed field | Copy value to new key, keep old as `_deprecated_{old_name}` | Low |
| Restructured (flat → nested) | Remap values to new structure | Medium |
| Removed field | Keep as `_deprecated_{name}`, do NOT delete | None |
| Type change | Transform value if safe, flag if ambiguous | Medium |
| _field_types update | Merge new entries, keep existing | None |

**Present plan to operator before executing.** Format:

```
## Migration Plan · {brand} → v{target}

### Safe (auto-apply)
- brand.json: Add `social_media.tiktok` (empty)
- brand.json: Add `seasonality.events[]` (empty array)
- spec.json: Update `_field_types` (3 new entries)

### Needs Review
- brand.json: `tone` → `tone_of_voice` (rename · will copy value)
- profile.json: `triggers[]` restructured to `decision_process.triggers[]` (remap)

### Breaking Changes
- [BREAKING] brand.json: `kpis` section removed in v2.0 · will move to `_deprecated_kpis`

Apply safe changes now? (y/n)
Apply reviewed changes after confirmation? (one by one)
```

---

## Step 4 · Execute Migration

After operator approval:

1. **Backup**: Copy current file to `brands/{slug}/sources/_pre-migration_{filename}_{date}.json`
2. **Apply safe changes**: Add empty fields, merge _field_types
3. **Apply reviewed changes**: One by one, with operator confirmation
4. **Bump `_version`** in migrated files to match target
5. **Log in CHANGELOG.md**: `[MIGRATION] {brand} migrated from v{old} to v{new} · {N} fields added, {N} renamed, {N} deprecated`
6. **Update status.json**: clear version-mismatch flags

---

## Step 5 · Post-Migration Validation

1. Run validate-resources on the migrated brand
2. Report any new flags introduced by migration
3. Flag any required fields that are now empty (added during migration but need data)

---

## Hard Rules

- **Never delete data.** Removed fields → `_deprecated_{name}`. Operator decides when to truly purge.
- **Never overwrite non-empty fields** unless the operator explicitly approves.
- **Always backup before migrating.** Pre-migration snapshot-brand in `sources/`.
- **One brand at a time.** No batch migration without explicit operator request.
- **Present plan before executing.** Never auto-apply "Needs Review" or "Breaking Changes".
- **CHANGELOG is mandatory.** Every migration logged with version, date, and field-level detail.
- **_TEMPLATE is read-only.** Migration reads _TEMPLATE for comparison, never writes to it.

---

## Batch Mode (optional, operator-triggered)

Operator says "migrate all brands" or "batch migration":

1. List all brands (same scan as validate --all)
2. Generate migration plan per brand
3. Present consolidated summary: "3 brands need migration, 2 safe-only, 1 has breaking changes"
4. Execute per-brand with individual confirmation for breaking changes
5. Update workspace-status.json after all migrations

---

## v1.7 → v1.8 Migration Path (2026-04)

**100% backward compatible.** No destructive migration required.

**v1.8 changes:**
- spec.json: +8 optional blocks (composition, posology, contraindications, origin, production_method, preparation, external_databases, target_suitability, durability)
- spec.json: +`nutrition_facts.allergen_sources`, +`nutri_score_grade`, +`perishability.period_after_opening_months`, +`perishability.expiry_date_required`
- spec.json: +6 dietary_tags, +"oats" in allergens
- offers.json: +`contents.duration_type`, +`duration_servings`, +`cure_metadata`, +`incentives.duration_tiers`, +`loyalty`, +`offer_groups[].offers[].tags` (v2 schema · legacy v1.x was `offers[].tags`)

**Migration steps:**
1. Read `_version` from `brands/_TEMPLATE` (living source) per entity, then align every instance file to the same value. The field is `_version` on every file (not `_template_version`, inherited drift). Current values: spec.json=1.8, offers.json=2.0, brand.json=2.2, profile.json=1.2.
2. Add `_field_types` and `_changelog` entries from `_TEMPLATE/products/_example/`.
3. Do NOT touch existing data. New blocks stay null until next snapshot.
4. Validation: rerun validate-resources, must pass without error.

**No re-snapshot needed.** v1.7 instances remain valid in v1.8. Enrichment is opt-in at next refresh.
