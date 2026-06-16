---
name: check-cross-refs
type: curator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Walks declared cross-references in a proposed schema
  and verifies each target core entity (product, audience, offer, etc.) exists in the
  current workspace. Flags unresolved references before the extension is scaffolded.
  Invoked by scaffold-extension Phase 5.
  FR: "check les cross-refs" "vérifie les références" "résous les cross_refs".
  EN: "check cross-refs" "verify references" "resolve cross_refs".
permissions:
  reads: [brand]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: draft schema from Phase 3 with declared cross_refs
  postconditions: every cross_ref resolved, or operator notified of broken refs
---

# Skill: Check Cross-Refs

Verifies that every cross-reference declared in the draft schema points to a real core entity in the active brand's workspace.

## Method

Given the draft schema's `cross_refs` array (e.g. `"product_slug → brands/{slug}/products/{product_slug}/spec.json"`):

1. **Parse each cross_ref** · extract the source field, the target core entity type, and the target path pattern.
2. **Walk the brand workspace** · for each declared target, verify the referenced path pattern can resolve on at least one existing entity.
3. **Resolution outcomes** :
   - All refs resolve → return OK to orchestrator.
   - One ref resolves to zero entities (e.g. brand has no products yet but schema references `product_slug`) → return WARNING. Operator can proceed (the schema is future-proof) but no instance can be populated until the target exists.
   - One ref points to an invalid path pattern → return BLOCKING. Operator must fix the schema or drop the ref before Phase 6.
4. **Surface to operator** (only on WARNING or BLOCKING):

> *"Ton schema référence `{cross_ref}` mais je ne trouve aucun `{target_type}` existant dans la marque `{slug}`. Tu veux : (a) créer d'abord le core entity, (b) garder la ref même si elle pointe vers rien pour l'instant, (c) retirer la ref du schema ?"*

## Output

```
{
  "status": "ok | warning | blocking",
  "unresolved": [{"cross_ref": "...", "reason": "..."}],
  "resolved": [{"cross_ref": "...", "target_count": 3}]
}
```

## Hard rules

- Never modify the schema here. Only flag.
- Do not resolve `null` or optional refs as errors · schema may declare an optional ref.
- Runtime rot (target renamed later) is not detected here · that's a known V1 limit, runtime check is on the roadmap.
