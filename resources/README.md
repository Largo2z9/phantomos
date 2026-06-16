# Shared Resources

Registries, matrices, specifications, formulas, and schemas shared across every brand in the workspace.

## Status · starter examples, not maintained content

**The seeded files under `registries/`, `quality-specs/`, `templates/`, `routing/`, and `guides/` are starter examples.** They demonstrate the format an operator can follow to structure their own resources. They are **not** canonical production content the template maintainer keeps polished. They ship in their original language (French in several cases) and are not translated on every template release.

Each operator is expected to **replace, augment, or delete** these starter files to fit their own domain, methodology, and vocabulary. `ingest-resource` is the primary way to bring in your own; `learn-from-session → promote-learning` is how patterns you validate get added over time.

The structural pieces · the folder layout, the JSON schemas under `resources/schemas/`, the conventions framework under `conventions/`, and `validate-resources` · are maintained and versioned. The example content is not.

## Folders at a glance

| Folder | Content | Populated at V1 |
|---|---|---|
| `catalogues/` | Taxonomies and ID-referenced entries (angles, formats, hooks) | no · seeded by `ingest-resource` |
| `conventions/` | Per-platform operational rules (Meta Ads, Shopify, GA4, Klaviyo…) | yes · filled at `setup-brand` when a platform is connected |
| `frameworks/` | Mental models (awareness levels, AIDA, psychology primitives) | no · seeded by `ingest-resource` |
| `guides/` | Contributor guides (*where-does-it-go* decision trees) | yes |
| `quality-specs/` | Output evaluation criteria (binary tests, thresholds) | yes · `hook-quality-spec` |
| `registries/` | Living taxonomies with stable identifiers (angles, mechanics, proof types) | yes · 3 registries |
| `routing/` | Decision tables mapping context to recommendation | yes · awareness × angle matrix |
| `schemas/` | JSON Schema definitions for every entity type | yes · brand, spec, offer, profile, strategy |
| `scripts/` | Validation and maintenance scripts | yes · `validate-all`, `pre-commit` |
| `sops/` | Step-by-step execution procedures | no · seeded by `ingest-resource` |
| `templates/` | Reusable formats (creative-formula, hook-formulas) | yes |

Folders marked *no* ship empty with a `.gitkeep`. They fill as the operator ingests resources via `ingest-resource` or as `learn-from-session` promotes patterns to the shared base.

## Seeded files · V1 content

### Registries

| File | Role | Consumed by |
|---|---|---|
| `registries/angle-registry.md` | 14 psychological angles (efficiency, simplicity, transformation, etc.) with awareness ranges and proof types | `hooks-generator`, `script-writer`, `brief-generator`, `creative-strategist` |
| `registries/creative-mechanics-registry.md` | 28 creative mechanics (versus, diagnostic, UGC, celebrity, before-after, etc.) with text-to-visual slider | `hooks-generator`, `script-writer`, `pattern-extractor` |
| `registries/proof-registry.md` | 14 proof types ranked from risk-reversal to clinical-trial, with stacking patterns | `script-writer`, `creative-strategist`, `brief-generator` |

### Routing

| File | Role | Consumed by |
|---|---|---|
| `routing/awareness-angle-matrix.md` | Primary router from audience awareness level to primary and secondary angles, tones, leads, formats | `hooks-generator`, `script-writer`, `brief-generator` |

### Quality specs

| File | Role | Consumed by |
|---|---|---|
| `quality-specs/hook-quality-spec.md` | Five binary criteria (pattern interrupt, identification, open loop, specificity, awareness match) with thresholds and integrity tests | `hooks-generator` Step 5, `script-writer` validation input |

### Templates

| File | Role | Consumed by |
|---|---|---|
| `templates/creative-formula.md` | Creative architecture V3 · core + strategic context + modifiers + text-to-visual slider (0-10) | every creative skill |
| `templates/hook-formulas.md` | 15 hook categories (question, statement, before-after, confession, etc.) with patterns and awareness ranges | `hooks-generator`, `script-writer`, `creative-strategist` |

### Schemas

Every Context DB entity has a schema in `schemas/` (`brand.schema.json`, `spec.schema.json`, `offer.schema.json`, `profile.schema.json`, `strategy.schema.json`). Never edited by skills · schemas are the contract, skills validate against it.

## Principles

**Append-only.** Registries grow (new entries) but past entries are never retroactively modified · historical decisions stay traceable.

**Source of truth.** These files are *the* reference for every skill. An output that falls outside the scope of these registries is flagged by `validate-resources`.

**MECE.** Categories do not overlap and collectively cover the full spectrum observed in retro-engineering (522 creatives, 10 batches, 9 brands).

**Craft-agnostic.** Content is business-agnostic. An angle like *transformation* works for beauty, supplements, or tech · the underlying psychology is universal.

## Common usage patterns

### Brand setup
1. Read `templates/creative-formula.md` § Classifier to pick the mode (CONCEPT / TEMPLATE / ASSET).
2. Read `routing/awareness-angle-matrix.md` to map audience awareness level to recommended angles.
3. Build the creative brief.

### Creative brief
Include audience, awareness level, psychology core desire, required angles (or leave open for the agent to pull from the matrix), format, text-to-visual slider estimate, and regulatory or compliance constraints. The agent will consult `awareness-angle-matrix.md`, `angle-registry.md`, `creative-mechanics-registry.md`, `proof-registry.md`, and `hook-formulas.md` as needed.

### Hook validation
Apply `quality-specs/hook-quality-spec.md` (five criteria). Minimum 4/5 passed = OK. Cross-reference angle × proof against the registries for compliance.

## Versioning

Each file carries a last-updated timestamp in its footer, format `YYYY-MM-DD (Session N)`. Major changes are tagged `[BREAKING]` (V1 → V2) or `[SUPERSEDED Sxx]` when an item is replaced by a later session's version.

## Extension and feedback

Three routes:
1. **Error or inconsistency.** File via the `/flag` skill → `feedback/` append-only → review in the next session.
2. **New entry.** Validate on at least two real cases → propose the structure tagged `_proposed` → review → merge.
3. **Modification of an existing entry.** Rare. Document why the current structure is insufficient (concrete case) → propose V2 → test on 5+ hooks or creatives without regression.

---

*Deployed 2026-04-13. Promoted from `/context-engine/shared-resources/` (R&D) to `/workspace-template/resources/` (shippable).*
