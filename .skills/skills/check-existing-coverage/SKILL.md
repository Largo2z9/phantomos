---
name: check-existing-coverage
type: curator
version: "2.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Pre-build gate that checks whether the operator's intent
  can already be served by existing structures before scaffolding a new one. Scans five
  dimensions: core entities, existing sidecars on the active brand, custom entities on the
  active brand, custom entities on sibling brands in the portfolio, shared resources. If any
  dimension matches, routes to the existing structure instead of building new. Scaffold only
  proceeds when the intent is genuinely new.
  Replaces the narrower `suggest-reuse-registries`. Invoked by scaffold-extension Phase 2.
  FR: "check coverage" "vérifie si ça existe déjà" "y a déjà quelque chose pour ça" "check reuse".
  EN: "check coverage" "is there already something for this" "check existing coverage" "check reuse".
permissions:
  reads: [brand, resource, index]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: intent object from scaffold-extension Phase 1 available
  postconditions: verdict (route-to-existing | partial-reuse | genuinely-new) returned to orchestrator
---

# Skill: Check Existing Encoding

Pre-build analysis gate. Prevents the proliferation of redundant custom entities by verifying the operator's intent cannot be served by existing structures in the workspace. The gate walks five dimensions in order of specificity and returns the first matching outcome.

## Method

Given the intent object from scaffold-extension Phase 1 (class, shape, population, cross_refs, proposed_name, scope), run the five-dimension check in this order.

### Dimension 1 · Core entity coverage

Can the data fit into one of the six core entities (`brand`, `product spec`, `offers`, `profile`, `learnings`, `strategy`) without modification?

- Read the core schemas in `resources/schemas/`.
- Match the intent's conceptual target against core entity semantics.
- If match, **stop here**. Return `route-to-core`.

Example: operator says *"je veux tracker les apprentissages sur Meta pixel"*. This is already covered by `learnings.json` with `scope: "platform"`, `platform: "meta"`. Route to `capture-learning`, no extension needed.

### Dimension 2 · Existing sidecar on the active brand

Does a `{entity}.extensions.json` already exist on the active brand that covers the concept?

- Walk `brands/{slug}/*.extensions.json` and `brands/{slug}/{products|audiences}/*/*.extensions.json`.
- Match the intent's fields against existing sidecar fields.
- If match, **stop here**. Return `route-to-existing-sidecar` with the sidecar path.

Example: operator wants to add `supplier_lead_time_days` to brand, but `brand.extensions.json` already exists with this field. Route to `.skills/write-to-context.py` on the existing sidecar.

### Dimension 3 · Existing custom entity on the active brand

Does a `brands/{slug}/custom/{type}/` already exist that matches the intent's type or semantics?

- Walk `brands/{slug}/custom/*/` folders.
- Check schema files for semantic overlap on type name, fields, and shape.
- If exact or near-match, **stop here**. Return `route-to-existing-custom` with the path.

Example: operator wants to track competitor pricing, but `brands/{slug}/custom/competitor_pricing/` already exists. Propose adding new instances rather than creating a parallel entity.

### Dimension 4 · Custom entity on sibling brands (cross-portfolio)

Does a similar custom entity exist on **another brand** in this workspace?

- Read `index.json → extensions[]`.
- Filter entries with matching or convergent `type` name or cross_ref pattern.
- If found, **stop here** and surface two options to the operator:
  - *Reuse the existing pattern* · copy the schema from the sibling brand, adapt instances locally. Preserves cross-brand consistency.
  - *Promote the pattern to shared resource* · if it exists on 3+ brands with convergent schemas, it's a promotion candidate (see `docs/system/extending.md § Promotion threshold`).

Example: operator on `brand-B` wants to track competitor pricing. Already exists on `brand-A` with identical schema. Propose reuse.

### Dimension 5 · Shared resources coverage

Can the concept be represented using an existing shared resource (`resources/registries/`, `resources/routing/`, `resources/frameworks/`, `resources/templates/`)?

- Walk `resources/*/` and scan file contents for semantic match against the intent's fields.
- If the concept is fully a reference rather than new data (e.g. operator wants a *"tag of proven hook types"* → already exists as `resources/templates/hook-formulas.md`), surface to operator as reuse.
- If partial (e.g. operator wants to track which registry entry applies to each instance), suggest building a **thin extension** that cross-references the shared resource by ID rather than duplicating content.

Example: operator wants a library of creative angles. Already exists as `resources/registries/angle-registry.md`. Route to reuse; if operator wants per-brand tracking of which angles they've tested, propose a thin extension with ref fields pointing to angle-registry IDs.

## Output to scaffold-extension orchestrator

```
{
  "verdict": "route-to-core | route-to-existing-sidecar | route-to-existing-custom | reuse-cross-brand | route-to-shared-resource | partial-reuse | genuinely-new",
  "matched_dimension": 1 | 2 | 3 | 4 | 5 | null,
  "matched_target": "<path or resource id>" | null,
  "reuse_candidates": [<list of references if partial-reuse>],
  "operator_proposal": "<natural-language proposal to surface to operator>"
}
```

## Decision by orchestrator

- `route-to-*` → scaffold-extension halts. Main agent routes the operator to the existing structure via the appropriate skill (`.skills/write-to-context.py`, capture-learning, etc.).
- `partial-reuse` → scaffold-extension proceeds with Phase 3 schema draft, using the matched references as cross_refs instead of recreating fields.
- `genuinely-new` → scaffold-extension proceeds with full scaffold.

## Hard rules

- Always walk all five dimensions, even if an early match is found · multiple matches may exist, operator sees the full landscape.
- Never silently route. The operator sees the matched target and confirms or overrides.
- Cross-brand reuse proposals require explicit operator opt-in. Do not auto-copy schemas across brands.
- Shared resources match requires semantic overlap, not just lexical. A field named `angle` is not the same as `angle-registry` unless the intent is about tagging by angle type.
