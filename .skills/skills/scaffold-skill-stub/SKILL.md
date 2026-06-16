---
name: scaffold-skill-stub
type: builder
version: "1.0.0"
recommended_model: sonnet
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Generates a SKILL.md stub in `.skills/skills/custom/{name}/`
  for a skill that populates or queries a newly scaffolded extension. Writes into the meta-OS
  namespace · hence the builder typology. Conditional step: only invoked if the operator's
  intent includes a custom skill. The stub body is skeletal; the operator fills in execution
  logic afterward or delegates to build-agent for deeper buildout.
  Invoked by scaffold-extension Phase 8.
  FR: "scaffold un skill stub" "génère le stub du skill" "crée le squelette du skill".
  EN: "scaffold skill stub" "generate skill stub" "create skill skeleton".
permissions:
  reads: [resource, brand]
  writes: [skill.custom]
  mode: direct
  subagent_safe: true
pipeline:
  preconditions: extension files scaffolded (Phase 7 complete), operator requested a populating skill
  postconditions: SKILL.md stub on disk at `.skills/skills/custom/{name}/SKILL.md`, ready for fill-in
---

# Skill: Scaffold Skill Stub

Generates the SKILL.md stub of a custom skill that will populate or query a new extension. Builder typology because it writes into `.skills/skills/`, the meta-OS namespace.

## Method

1. **Derive the skill name** from the intent (e.g. *"scrape competitor ads"* → `scrape-competitor-ads`). Enforce kebab-case.
2. **Select the type** based on what the skill will do:
   - Populate via external pipeline (scraper, API pull) → `producer`
   - Transform core data into the extension (derived) → `producer`
   - Read the extension and return output → `navigator` (if operator-facing) or `curator` (if called by another skill)
3. **Determine the model** · default `sonnet`. `haiku` for pure fetch/write skills with no generation. `opus` only with explicit justification.
4. **Declare permissions** · reads include `brand` and any required cross-entities. Writes include the new extension's path. Mode typically `direct` for scraped factual data, `proposed` for derived data needing review.
5. **Compose the stub** · frontmatter fully populated, Tone section with a one-line placeholder, and a body skeleton:
   - `## Invocation context`
   - `## Method` (numbered steps, placeholder prose for the operator to fill)
   - `## Output` (expected shape)
   - `## Hard rules` (at least the mutation gate and cross-ref discipline)
6. **Write the file** to `.skills/skills/custom/{skill_name}/SKILL.md` via `.skills/write-to-context.py`.
7. **Add a line to `brands/{slug}/todos.md → ## In Progress`**:

> *"[ ] Implement body of custom skill `{skill_name}` · stub created by scaffold-extension. Fill in Method steps. Test on one instance before scaling."*

## Output to orchestrator

```
{
  "skill_path": ".skills/skills/custom/{name}/SKILL.md",
  "skill_type": "producer | navigator | curator",
  "recommended_model": "sonnet | haiku | opus",
  "status": "ok | skipped | failed"
}
```

## Hard rules

- Builder typology: writes into `.skills/skills/custom/`. Never into core `.skills/skills/` (reserved for shipped skills).
- The stub is intentionally incomplete · the Method body has placeholders. The operator fills in or delegates to `build-agent`.
- Never auto-execute the generated skill in the same turn. Let the operator review and trigger when ready.
- Reject if a skill with the same name already exists at `.skills/skills/custom/{name}/`.
