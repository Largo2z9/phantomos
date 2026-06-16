---
name: update-workspace
type: orchestrator
version: "1.2.0"
recommended_model: sonnet
layer: meta
reasoning_pattern: null
description: >
  Applies one or more PhantomOS release updates to an installed workspace
  without losing operator data. Reads the installed version, finds all
  manifests between installed and latest, applies each change by type
  (doc, skill, schema, infra), delegates schema migrations to migrate-workspace.
  Preserves brands/, operator/, credentials.env, learnings.
  FR: "mets à jour phantomOS", "update workspace", "installe la nouvelle version", "applique les mises à jour".
  EN: "update workspace", "install latest version", "apply updates", "upgrade phantomos".
permissions:
  reads: [workspace, manifest]
  writes: [workspace_template_files, operator_installation]
  mode: direct
  subagent_safe: false
pipeline:
  preconditions: |
    - workspace currently installed (template files present)
    - /operator/installation.json present OR first-run detection
    - manifests available at docs/internal/releases/manifest/{version}-manifest.json
  postconditions: |
    - template files updated to target version
    - operator data untouched
    - /operator/installation.json reflects new version
    - validate-resources run on each brand, flags surfaced
disambiguates_against:
  migrate-workspace: "route to migrate-workspace when the operator only needs a schema migration within a version (no template file changes), not a full release update"
  setup-brand: "route to setup-brand when operator wants to add a new brand, not update the template"
---

# Skill: Update Workspace

Applies release updates to an installed PhantomOS workspace. Preserves operator data, syncs template files, runs migrations when schemas bump.

---

## Pipeline canon v2.80.0+

Skill consommé par la slash command `/update` (canon Sprint v2.80.0). Doctrine de référence · `docs/system/update-distribution-doctrine.md` v2.80.0 (Update Distribution Discipline).

**Position dans le pipeline canon ·**

- L'opérateur invoque `/update` (slash command opérateur-facing).
- `/update` route vers `update-workspace` (ce skill, orchestrator).
- `update-workspace` détecte les BREAKING changes dans la chaîne de manifests.
- Si BREAKING détecté → délègue à `migrate-workspace` (curator) qui consume les scripts du framework `migrations/` (canon v2.80.0 · scripts Python par BREAKING release).
- Backup pre-migration obligatoire dans `_archive/migrations/pre-v{version}-{date}/`.
- Rollback path canon disponible via `/update --rollback {version}`.

**Contrat opérateur-facing canon v2.80.0 ·**

- Disclosure pré-update obligatoire (cohérent `engagement-disclosure-doctrine.md` v2.79.5 · plan + ETA + démarche + close binaire confirmation).
- NIVEAU 0 paramètres décomposés exposés AVANT exécution (cohérent `decomposition-visibility-doctrine.md` v2.79.5+).
- Preserve operator state strict · brands/ + operator/ + credentials + session-state + learnings intacts.
- Migrations versionnées automatiques pour BREAKING changes (jamais silent).
- Backup pre-migration obligatoire (rollback path canon).

**Anti-patterns stricts ·** update silent sans disclosure · écrasement brands/operator/credentials · BREAKING appliqué sans migration script idempotent · absence backup pre-migration · absence rollback path.

---

## Tone

Chairman reporting an update installation. Plain language, no technical detail exposed unless operator asks. Summary first, steps silent unless something needs confirmation.

---

## Invocation

Operator says *"update"*, *"mets à jour"*, *"applique la nouvelle version"*, or the agent detects a version mismatch between `/operator/installation.json → template_version_installed` and `_version.json → template_version`. A `null` installed version is not a mismatch : it is a fresh install awaiting first-run initialization (see Step 1).

---

## Method

### Step 1 · Detect versions

Read:
- `_version.json → template_version` (the target/latest)
- `/operator/installation.json → template_version_installed` (what's installed)

If `/operator/installation.json` does not exist → check `brands/` for real brand folders (ignore `_` prefixed) BEFORE concluding. **No real brand** → first-run post-install : set `template_version_installed` to the template's current version, write `installation.json`, and exit (no update needed, this is a fresh install). **Real brands present** → this is an OLD INSTANCE without version tracking, NOT a fresh install : treating it as first-run would silently skip every data migration. STOP, surface to the operator, and determine the actually-installed version together (old `_version.json` if the template was not yet overwritten, `CHANGELOG.md` head, or operator memory). Write that version to `installation.json`, then proceed with the normal chain.

If `installation.json` exists but `template_version_installed` is `null` → same logic : no real brand → first-run case (the template ships it as `null`), set it to `_version.json → template_version`, set `first_install_at`, and exit. Real brands present → old-instance case above, never init-and-exit.

If versions match → *"Tu es déjà à jour en {version}. Rien à faire."* → exit.

If installed < target → continue.

### Step 2 · Build the update chain

List every manifest at `docs/internal/releases/manifest/{version}-manifest.json` where `from_version >= installed` and `to_version <= target`. Sort by `to_version` ascending. This is the chain of updates to apply in order.

If any manifest in the chain has `breaking: true` or `requires_confirmation: true` → present the list to the operator with summaries and explicit confirm via `AskUserQuestion`. Otherwise proceed silently.

### Step 3 · Apply each manifest in order

For each manifest in the chain, walk `changes[]` and apply per type:

**`doc-change` / `doc-added`** · overwrite/create the template file. Safe. No operator data touched.

**`infra-change` / `infra-added`** · overwrite/create the script. Run the `post_step` if declared (e.g. rebuild manifest, rebuild snapshots).

**`skill-added`** · copy the new SKILL.md folder into `.skills/skills/`. Regenerate `.skills/_manifest.json`.

**`skill-renamed`** · rename the folder, update the frontmatter `name:`, regenerate manifest. Keep old name as alias in the manifest's `aliases_to_keep` if provided.

**`skill-removed`** · flag to operator, propose alternative if declared. Move old folder to `.skills/skills/_archive/`. Update manifest.

**`schema-bump`** · DO NOT apply directly. Delegate to `migrate-workspace` via Task tool with the migration script path, from/to schema versions, and affected files glob. Collect migration report.

**`breaking`** · surface the full `notes` field to the operator, get explicit confirm, then apply as above.

### Step 4 · Post-update

For each applied manifest, append an entry to `/operator/installation.json → history[]`:

```json
{
  "from_version": "...",
  "to_version": "...",
  "applied_at": "...",
  "changes_count": N,
  "migrations_run": [],
  "flags": []
}
```

Update `template_version_installed` to the target.

Run the final manifest's `post_update_checklist` (typically: rebuild manifest, rebuild snapshots, run validate-resources).

### Step 5 · Surface to operator

Plain-language recap:

> *"Update {from} → {to} appliquée. {N} changements. {M} migrations. {Tes marques / ton contexte opérateur / tes learnings} intacts. {0 / K flags à regarder} post-update."*

If flags or migration warnings: surface as a short action list, not a report dump.

---

## Safety guarantees

- **Never touch**: `brands/{slug}/*` (except `_TEMPLATE/`), `operator/`, `credentials.env`, `credentials_shared.env`, `learnings.json` under a brand.
- **Always preserve**: user-authored extensions under `brands/{slug}/custom/`, custom skills under `.skills/skills/custom/`.
- **Verify before write**: read current file content, confirm it matches what the manifest expects, abort if divergence suggests local modifications.
- **Transactional per manifest**: if any change in a manifest fails, roll back the whole manifest (restore files from backup), log, surface to operator.

---

## Output

```
{
  "status": "ok | partial | failed",
  "from_version": "...",
  "to_version": "...",
  "manifests_applied": [...],
  "migrations_run": [...],
  "flags_raised": [...]
}
```

---

## Hard rules

- **NEVER** touch operator data. If uncertain whether a file is template or operator-owned, treat as operator-owned.
- **NEVER** skip schema-bump migrations. Data integrity > speed.
- **NEVER** apply a breaking manifest without explicit operator confirmation.
- **NEVER** update silent sans disclosure pré-engagement (canon v2.80.0).
- **NEVER** absence de backup pre-migration `_archive/migrations/pre-v{version}-{date}/` (canon v2.80.0).
- **NEVER** absence de rollback path (canon v2.80.0 · `/update --rollback {version}`).
- **ALWAYS** regenerate `.skills/_manifest.json` and `brands/{slug}/_snapshot.md` post-update.
- **ALWAYS** write to `/operator/installation.json → history[]` before marking update complete.
- **ALWAYS** expose NIVEAU 0 paramètres décomposés AVANT exécution (canon v2.80.0).

---

## Related

- `docs/system/update-distribution-doctrine.md` (v2.80.0) · doctrine canon pattern de mise à jour PhantomOS.
- `docs/system/updates.md` · doctrine for publishing clean updates.
- `docs/system/engagement-disclosure-doctrine.md` (v2.79.5) · disclosure pré-engagement.
- `docs/system/decomposition-visibility-doctrine.md` (v2.79.5+) · NIVEAU 0 paramètres décomposés.
- `docs/internal/releases/manifest/{version}-manifest.json` · per-release change manifest.
- `.skills/skills/migrate-workspace/SKILL.md` · delegated schema migration (consume `migrations/` framework v2.80.0).
- `migrations/` · framework canon v2.80.0 (scripts Python par BREAKING release).
- `_version.json` · target version registry.
- `.claude/commands/update.md` · slash command opérateur-facing canon v2.80.0.
