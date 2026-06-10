---
name: skill-name
type: producer   # MANDATORY: one of producer | curator | capturer | orchestrator | navigator | builder. See docs/system/patterns.md § Skill Taxonomy.
version: "1.0.0"
recommended_model: sonnet   # default per typology, override with YAML comment justification if different
description: >
  One-line description of what this skill does.
  Triggers: list the natural language phrases that activate this skill, in both FR and EN.
  FR: "trigger fr 1", "trigger fr 2".
  EN: "trigger en 1", "trigger en 2".
permissions:
  reads: [brand, product]
  writes: [learning]
  mode: proposed
  subagent_safe: true   # default per typology (true for producer/curator/navigator, false for capturer/orchestrator/builder)
pipeline:
  preconditions: what must be true before this skill runs (e.g. "brand must exist")
  postconditions: what should run after (e.g. "run validate-resources")
---

# Skill: {Skill Name}

One paragraph describing the skill's purpose, scope, and relationship to other skills.

---

## Step 1 — {First step name}

Describe what the agent does in this step. Be specific about:
- What to read
- What to decide
- What to produce

---

## Step 2 — {Second step name}

Continue with subsequent steps. Each step should be self-contained and actionable.

---

## Output Format

```
Describe the exact output format the skill produces.
Include field placeholders with {curly braces}.
```

---

## Hard Rules

- **Rule 1** — hard constraint the agent must never violate
- **Rule 2** — another hard constraint
- **Never [X]** — format as imperatives

---

## Authoring Notes (delete this section when creating a real skill)

### Frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, matches folder name |
| `version` | Yes | Semver string. Bump minor for additions, major for breaking changes |
| `recommended_model` | Yes | `haiku` (read-only, fast) / `sonnet` (write, classify) / `opus` (complex reasoning) |
| `description` | Yes | Must include trigger phrases in both FR and EN |
| `permissions.reads` | Yes | Array of entity types this skill reads: `brand`, `product`, `offer`, `profile`, `learning`, `strategy` |
| `permissions.writes` | Yes | Array of entity types this skill mutates: `brand`, `product`, `offer`, `profile`, `learning`, `strategy`, or `[]` if read-only |
| `permissions.mode` | Yes | `proposed` (for mutations that need review), `direct` (for human-facing skills that write authoritative data), `none` (for read-only skills), `interactive` (skill drives a guided operator dialogue and writes validated answers turn by turn), `silent` (background write, no operator gate or surface ; the caller surfaces the summary) |
| `pipeline.preconditions` | No | What must exist before this skill runs |
| `pipeline.postconditions` | No | What should run after this skill |

### Conventions

- Folder name = skill name in `lowercase-with-dashes`
- Place in `.skills/skills/{skill-name}/SKILL.md`
- Core skills (shipped with template) are in `.skills/skills/`
- Custom skills should go in `.skills/skills/` alongside core skills
- If two skills have overlapping triggers, make triggers more specific to avoid ambiguity
- Hard rules are the agent's guardrails — they override all other instructions in the skill
- Steps should be numbered and sequential
- Output format should be copyable/parseable by consuming agents
