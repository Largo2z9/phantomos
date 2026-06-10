# Migrations Framework

Versioned migration scripts shipped per BREAKING release of the workspace template canon.

Each BREAKING change to the template (`MAJOR.MINOR.0` releases that transform operator workspace state) ships a Python migration script that brings an existing workspace from `v(N-1).x` to `vN.0.0` safely. Additive releases (NEW skills · NEW commands · NEW doctrines · zero data transformation) also ship a script for traceability and rollback, even if `run_transformation` is a no-op.

Cross-reference doctrine · `docs/system/update-distribution-doctrine.md` (v2.80.0+).

## Pattern

One Python script per BREAKING release. Lives at the root of `migrations/`. Discoverable by version sort.

## Two migration locations (do not confuse)

| Location | Scope | Discovered by |
|---|---|---|
| `migrations/` (this folder) | One script per release, brings the whole workspace from version N-1 to N. Always shipped, even no-op. | `/update` (version sort, sequential) |
| `operations/migrations/` | Schema-bump data migrations only (operator data transformed, e.g. `brand.json` v2.1 → v2.2). Naming `v{version}-{slug}.py`. | Release manifests (`migration_script` field), executed via `migrate-workspace` |

Both follow the same 4-method canonical structure below. A schema-bump release typically ships both: the release script here, and the data script in `operations/migrations/` referenced by the manifest.

## Naming Convention

```
{version}-{slug-description}.py
```

Examples ·
- `2.63.0-pain-points-toplevel.py`
- `2.71.0-brand-spec-restructure.py`
- `2.80.0-pipeline-update-canon.py`

Slug · lowercase, dashes, descriptive, max 5 words.

## Canonical Structure (4 Methods Required)

Every migration script MUST implement these 4 methods ·

| Method | Purpose | Returns |
|---|---|---|
| `check_required()` | Verify pre-conditions before applying (current version, expected files present, expected schema). | `(bool, str)` · ready flag + reason |
| `run_transformation(dry_run)` | Apply the migration. MUST be idempotent (safe to run 2x without breaking). | `None` |
| `validate_state()` | Verify state is canonical post-migration. | `(bool, str)` · valid flag + reason |
| `rollback()` | Revert this migration by restoring from automatic backup. | `bool` · success |

## Idempotence (CRITICAL)

Each method MUST be safe to run multiple times.

- `run_transformation` re-runs · detect already-transformed state · skip work, log skip reason.
- `check_required` re-runs · detect already-on-target-version · return `False` with reason `"already on vX.Y.Z"`.
- `validate_state` re-runs · pure read, no side effects.
- `rollback` re-runs · detect no-backup case · return `False` cleanly.

## Backup Pre-Migration (CANONICAL)

Before any `--apply`, the script creates an automatic backup at ·

```
_archive/migrations/pre-v{version}-{YYYY-MM-DD}/
```

Backup scope · only the files the migration will touch (NOT full workspace). Each migration script declares its own backup file list.

Example layout post-migration ·

```
_archive/migrations/
  pre-v2.63.0-2025-09-12/
    brands/example/spec.yaml
    brands/example/pain-points.yaml
  pre-v2.80.0-2026-05-18/
    _version.json
```

## Usage

```bash
# Check pre-conditions only (no transformation)
python3 migrations/2.80.0-pipeline-update-canon.py --check

# Preview transformation (no write)
python3 migrations/2.80.0-pipeline-update-canon.py --dry-run

# Apply migration (creates backup, transforms, validates)
python3 migrations/2.80.0-pipeline-update-canon.py --apply

# Rollback from automatic backup
python3 migrations/2.80.0-pipeline-update-canon.py --rollback
```

Exit codes · `0` success · `1` failure (pre-condition · validation · rollback miss).

## Migration Types

| Type | Definition | Example |
|---|---|---|
| `additive` | NEW canon shipped (skills · commands · doctrines). Zero transformation operator state. | v2.80.0 pipeline update |
| `transform` | Existing canon restructured. Operator data moved · renamed · reshaped. | v2.63.0 pain-points to top-level |
| `deprecate` | Canon removed or replaced. Cleanup phase post-migration window. | future v3.0.0 schema purge |

## Output Iconography

Migration scripts use canonical icons in `print()` outputs ·

| Icon | Meaning |
|---|---|
| `✓` | Success · validated |
| `◐` | In progress · partial |
| `○` | Pending · skipped |
| `✗` | Failure · blocked |
| `⚠` | Warning · degraded |
| `→` | Action taken (backup, transform step) |

## Template

Use `migrations/_template.py` as the starting point for any new migration script. The template ships all 4 methods stubbed with canonical structure, argparse CLI, backup logic, and validation pattern.

## Anti-Patterns

- **Skipping backup** · Never apply transformation without writing to `_archive/migrations/pre-v{version}-{date}/` first.
- **Non-idempotent transformation** · Always detect already-applied state · re-running must not corrupt.
- **Silent failure** · Always return non-zero exit code on validation failure. Never swallow exceptions.
- **Full workspace backup** · Backup only files the migration touches. Full backup is `/sync` responsibility, not migration responsibility.
- **Cross-version chains** · One script applies one version delta. To go from v2.5.0 to v2.8.0, run 3 scripts sequentially (`/update` orchestrates this).
- **Hardcoded paths** · Use `WORKSPACE_ROOT = Path.cwd()` · scripts run from workspace root, not from `migrations/` folder.

## Discovery by `/update`

The `/update` slash command (v2.80.0+) discovers applicable migrations by ·

1. Read current `_version.json` `template_version`.
2. List `migrations/*.py` scripts.
3. Filter scripts where `MIGRATION_VERSION > current_version AND MIGRATION_VERSION <= target_version`.
4. Sort ascending by semver.
5. Execute sequentially · halt on first failure.
