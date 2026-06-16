---
name: validate-naming
type: curator
version: "1.0.0"
recommended_model: haiku
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Verifies the proposed extension name does not collide
  with core entity names (reserved), does not duplicate an existing extension, and
  respects kebab-case + MECE conventions.
  Invoked by scaffold-extension Phase 4.
  FR: "valide le nom" "check le naming" "vérifie le nom de l'extension".
  EN: "validate naming" "check name" "verify extension name".
permissions:
  reads: [brand, index]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: proposed entity name from Phase 1 or 3 available
  postconditions: name approved + clean, or alternatives proposed to operator
---

# Skill: Validate Nomenclature

Blocks naming collisions and enforces naming discipline for new extensions.

## Method

Given a proposed entity type name:

1. **Reserved names check** · case-insensitive match against core entity names: `brand`, `product`, `offer`, `profile`, `learnings`, `strategy`. Collision = CRITICAL, surface to operator with alternative suggestions.
2. **Duplicate check** · read `index.json → extensions[]` and `brands/*/custom/*/`. If same name exists elsewhere with different schema, flag MAJOR. If same name exists with convergent schema, suggest reuse of the existing extension instead of creating a new one.
3. **Kebab-case enforcement** · `^[a-z0-9-]+$`. Underscores, uppercase, spaces → reject with the kebab-case alternative proposed.
4. **MECE check** · scan existing extensions for semantic overlap (substring or lexical match on a curated list of stems: `ad`/`ads`, `competitor`/`concurrent`, `price`/`pricing`, `track`/`tracker`, etc.). If overlap detected, surface to the operator: *"Une extension similaire existe déjà sous le nom `{existing}`. Tu veux l'étendre ou tu en crées vraiment une nouvelle ?"*

## Output

- **OK** · return the validated name to the orchestrator.
- **Alternative** · propose 2-3 alternatives to the operator and wait for selection.
- **Block** · if reserved collision, the operator must choose a different name before Phase 5 can proceed.

## Hard rules

- Never silently rename. Always surface the issue and let the operator decide.
- Reserved names check is non-negotiable. No override.
- Case-insensitive matching on reserved names (`Brand`, `BRAND`, `brand` all blocked).
