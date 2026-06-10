# How to Build Skills. PhantomOS

**Status**. Permanent reference.
**Audience**. The `build-agent` skill, skill builders, advanced operators.
**Prerequisite**. Read `agent-design-guide.md` before this document.

---

## Taxonomy and Philosophy references

These two sections in `docs/system/architecture.md` are the non-negotiable contract for any new skill. Read them before writing any frontmatter.

- **`docs/system/patterns.md § Skill Taxonomy`**. Mandatory `type:` field in SKILL.md frontmatter. Exactly one of six typologies: `producer | curator | capturer | orchestrator | navigator | builder`. Each has a binary inclusion test and defaults for model, `subagent_safe`, write mode. `validate-resources` check 13b refuses any skill where `type:` is missing or invalid.
- **`docs/system/patterns.md § Skill Philosophy`**. Every skill embodies codified expert methodology. A complexity gate decides when the expert dissection is mandatory versus a light skill. Gate doc rule: if the required methodology is not codified in `resources/frameworks|catalogues|quality-specs|sops|conventions/`, **stop** generation and build the methodology artifact first.

---

## What a skill is

A skill is a markdown file (`SKILL.md`) that describes **step by step** what an agent must do. Not code. A protocol. The agent reads the SKILL.md and executes it.

A good SKILL.md is:
- **Human-readable.** An operator should understand what the skill does by reading it.
- **Agent-executable.** Steps are precise enough for an LLM to follow without ambiguity.
- **Maintainable.** If something changes (a JSON field, a business rule), one line of the SKILL.md changes.

---

## Anatomy of a SKILL.md

```
---
[frontmatter]           <- machine-readable metadata (includes type, model, subagent_safe)
---

# Skill: {Name}         <- title + short description (1 paragraph)

## Step 1. {Name}        <- numbered steps
## Step 2. {Name}
...

## Output Format         <- exact shape of the output

## Hard Rules            <- non-negotiable guardrails
```

Each section is mandatory. No section may be empty.

---

## The frontmatter

```yaml
---
name: my-skill
type: producer               # MANDATORY. One of producer | curator | capturer | orchestrator | navigator | builder. See docs/system/patterns.md § Skill Taxonomy.
version: "1.0.0"
recommended_model: sonnet    # Default per typology. Override with YAML comment justification if different.
description: >
  Short description of what the skill does.
  Triggers FR: "phrases that trigger this skill in French".
  Triggers EN: "phrases that trigger this skill in English".
permissions:
  reads: [brand, product]
  writes: [learning]
  mode: proposed             # proposed | direct | none | interactive | silent. See _TEMPLATE authoring notes.
  subagent_safe: true        # Default per typology (true for producer/curator/navigator, false for capturer/orchestrator/builder). Declare explicitly.
pipeline:
  preconditions: what must exist before this skill runs
  postconditions: what should run after
---
```

### Choose the right model

| Model | When to use |
|-------|-------------|
| `haiku` | Read-only, simple transformation, no complex reasoning. Fast and cheap. |
| `sonnet` | Analysis, classification, structured content generation, Context Engine writes. |
| `opus` | Multi-source reasoning, complex architecture, strategic decisions, problem decomposition. |

Rule. Start at `sonnet` when uncertain. Move to `opus` only if the skill fails on complex cases. `haiku` for purely mechanical tasks. The taxonomy default (see `docs/system/patterns.md § Skill Taxonomy`) is the first source of truth. Override only with a YAML comment justifying why.

### Declare subagent_safe explicitly

Always set `subagent_safe:` in the `permissions` block. The value drives whether the agent spawns the skill via the Task tool or runs inline.

- `true` for `producer`, `curator`, `navigator` by default.
- `false` for `capturer` (needs full session buffer), `orchestrator` (it IS the pilot), `builder` (needs operator dialogue).

### Write good triggers

Triggers are the phrases the operator says to launch the skill. They must be:
- **Natural.** How a human really says it.
- **Coverage-oriented.** Several formulations for the same intent.
- **Non-ambiguous.** No overlap with another skill's triggers.

```yaml
# Too generic. Matches too many things.
Triggers FR: "analyse", "regarde ça", "qu'est-ce qui se passe"

# Specific and natural.
Triggers FR: "analyse les perfs de {brand}", "routine perf", "point performance",
             "comment s'en sort {brand} cette semaine", "fais le point sur {brand}"
```

---

## The Steps

### Structure of a step

Each step must answer 3 questions:
1. **What to read.** Exact sources (files, APIs, outputs from other steps).
2. **What to decide.** The logic or analysis to perform.
3. **What to produce.** Output of this step (file, variable, input for the next step).

```markdown
## Step 2. Analyze metrics

Read `brands/{slug}/products/*/spec.json` to get targets (target ROAS, target CPA).

Compare against real metrics from Step 1:
- Real ROAS vs target ROAS. Compute gap in %.
- Real CPA vs target CPA. Compute gap in %.
- Identify under-performing adsets (ROAS < target - 20%).

Produce an `analysis` object with:
- `winning`. List of adsets above target.
- `underperforming`. List of adsets below target.
- `delta_roas`. Average delta in %.
```

### Rules for writing steps

**Be specific about file paths.**
```markdown
# Vague
Read the brand info.

# Precise
Read `brands/{slug}/brand.json`. Fields `name`, `purchase_driver`, `positioning.differentiator`.
```

**Always name produced variables.**
A step that produces something must name it explicitly so the next step can use it.

```markdown
# Implicit
Analyze the metrics and keep the results.

# Explicit
Produce a `perf_summary` object with fields: winning_adsets[], underperforming_adsets[], avg_roas_delta.
```

**Handle missing cases in the step, not in Hard Rules.**
If data may be absent, the step must say what to do.

```markdown
If `strategy.json` does not exist for this brand, skip this step and note "[strategy not defined]" in the output.
```

**One responsibility per step.**
If the step does two logically distinct things, it is two steps.

---

## Output Format

Mandatory section. Describes the exact structure of what the skill produces.

Two possible forms.

### Markdown (for reports readable by the operator)

```markdown
## Output Format

Markdown file saved to `brands/{slug}/reports/{date}-{type}.md`.

Structure:
# {Brand}. {Report type}. {Date}

## Synthesis
{2-3 lines summarizing the situation}

## Key metrics
| Metric | Real | Target | Gap |
|--------|------|--------|-----|
| ROAS | {val} | {val} | {val}% |

## Recommended actions
- [ ] {Action 1}. Priority: {high/medium/low}
- [ ] {Action 2}
```

### JSON (for outputs consumed by other agents)

```markdown
## Output Format

JSON object returned at the end of the skill:

{
  "brand_slug": "{slug}",
  "generated_at": "{ISO date}",
  "summary": "{string}",
  "proposals": [
    {
      "field_path": "strategy.focus_audiences[0]",
      "value": "{proposed value}",
      "confidence": 0.7,
      "rationale": "{why}"
    }
  ]
}
```

### Rule. Always a local file

Any skill output that produces a document is saved locally **first**. Referenced in `outputs-index.json`. External push optional afterward.

---

## Hard Rules

Hard Rules are the agent's guardrails. They cannot be overridden by context, operator instructions, or the skill's internal logic.

### Format

```markdown
## Hard Rules

- **Rule name**. Short description of the constraint.
- **Never [X]**. For absolute prohibitions.
- **Always [Y]**. For absolute obligations.
```

### What belongs in a Hard Rule

| Rule type | Example |
|-----------|---------|
| Write prohibitions | "Never modify `brand.json` directly. Always via `write_to_context()`." |
| Data protection | "Never read `credentials.env`." |
| Scope limits | "This skill analyzes one brand at a time. No cross-brand without orchestrator." |
| Behavior on missing data | "If target ROAS is missing from `spec.json`, flag and do not compute the gap." |
| Mandatory confirmation | "Always request confirmation before creating a Google Calendar event." |
| Anti-hallucination | "Never assume a missing value. Flag explicitly what is absent." |

### Standard Hard Rules for any skill calling external tools

These three rules are mandatory in any SKILL.md that performs API calls or tool calls in a loop. They prevent the most costly production failures.

```markdown
- **Max iterations**. Stop after {N} steps with no new signal or measurable progress. Flag to the operator.
- **Anti-repetition**. Never call the same tool with the same arguments twice in the same execution.
- **Centralized retry**. If a call fails, a single retry attempt with backoff. No cascading multi-level retries.
```

N depends on the skill. 3-5 steps for a simple skill, 10-15 for a deep analysis skill. The important thing is that it exists.

### What should NOT be a Hard Rule

Hard Rules are not steps in disguise. If it is a procedural instruction ("start by reading X"), it is a Step, not a Hard Rule.

```markdown
# Bad Hard Rule
- **Read brand.json first**. Before any analysis.

# Good Hard Rule
- **Never analyze without brand context**. If `brand.json` is absent, stop and flag.
```

---

## Common patterns

### Pattern 1. Collect -> Analyze -> Propose

Most frequent. Agent pulls data, analyzes, proposes enrichments to the Context Engine.

```
Step 1. Collect data (APIs, source files)
Step 2. Analyze and identify insights
Step 3. Formulate proposals (via write_to_context())
Step 4. Produce the synthesis report
```

Key hard rules. Mandatory proposal mode, no direct writes, flag missing data.

### Pattern 2. Read -> Generate -> Push

Agent reads context, generates a deliverable (report, brief, audit), pushes to external tool if configured.

```
Step 1. Read Context Engine (brand, strategy, active audiences)
Step 2. Read recent data (metrics, performance)
Step 3. Generate the deliverable (structured markdown)
Step 4. Save locally + reference in outputs-index.json
Step 5. Propose external push if integration configured
```

Key hard rules. Local first always, push requires confirmation on first time per session.

### Pattern 3. Audit -> Flag -> Todo

Agent scans workspace state, identifies anomalies, creates actionable tasks.

```
Step 1. Scan target files (status.json, todos.md, JSON entities)
Step 2. Identify anomalies (stale data, missing fields, inconsistencies)
Step 3. Prioritize flags (P0 blocking, P1 important, P2 improvement)
Step 4. Create todos in workspace or external tool per config
```

Key hard rules. Never create duplicates, system todos are distinct from operational todos.

### Pattern 4. Ingest -> Parse -> Enrich

Agent receives raw content (website, PDF, copy-paste), analyzes, proposes enrichments to existing entities.

```
Step 1. Receive the resource (URL, file, free text)
Step 2. Identify content type and target entity (brand, spec, profile, offers)
Step 3. Extract relevant info per the entity schema
Step 4. Compare with existing content. Propose only additions/corrections.
Step 5. Write proposals via write_to_context()
```

Key hard rules. Enrich, never overwrite, always indicate the source of each ingested piece of info.

---

## Versioning

A skill evolves. Versioning follows semver.

| Change | Version |
|--------|---------|
| New step, new feature, new output type | Minor. 1.0.0 -> 1.1.0 |
| Output format change (breaks compatibility with other skills) | Major. 1.1.0 -> 2.0.0 |
| Hard rule fix, step clarification | Patch. 1.0.0 -> 1.0.1 |

Always document major changes in the workspace `CHANGELOG.md`.

---

## Checklist before shipping a skill

Before considering a skill ready:

- [ ] Frontmatter complete. `name`, `type` (one of six typologies), `version`, `recommended_model`, `description` with FR+EN triggers, `permissions` (reads, writes, mode, **`subagent_safe` declared explicitly**), `pipeline` preconditions.
- [ ] `type:` passes the binary test from `docs/system/patterns.md § Skill Taxonomy`.
- [ ] If `recommended_model` or `subagent_safe` override the typology default, YAML comment present to justify.
- [ ] Expert methodology dissection done if the task is complex (Skill Philosophy complexity gate). If methodology is not yet codified in `resources/`, build it first before shipping the skill.
- [ ] Each step answers the 3 questions. What to read, what to decide, what to produce.
- [ ] File paths are explicit (no "read the brand files").
- [ ] Variables produced by a step are named and reused by later steps.
- [ ] Missing-data cases are covered in the steps.
- [ ] Output Format is defined with a structure example.
- [ ] Hard Rules cover. Context Engine writes, sensitive data, scope, anti-hallucination.
- [ ] Skill has been manually tested once on a real brand.
- [ ] Skill does not duplicate an existing skill (check `.skills/skills/`).

---

## Frequent mistakes of beginner builders

**"NEVER" is stronger than "ALWAYS".** Formulate Hard Rules as absolute prohibitions rather than obligations. The model retains negative constraints better. "Never write directly to brand.json" applies more reliably than "Always go through write_to_context()". Both say the same thing, but one is a brake, the other an intention.

**Put critical rules at the start AND the end.** Model attention follows a U-curve on a long prompt. Higher at start and end, lower in the middle. If a Hard Rule is non-negotiable, it must appear in both zones.

**Steps too short.** "Step 1. Read the data" without specifying which data, from which file, in which format. The agent improvises, unpredictable results.

**Hard Rules as a shopping list.** 15 hard rules of which 10 are procedural instructions. Real hard rules should fit in 5-7 lines max.

**No Output Format.** Skill produces "something useful" with no defined structure. Any consuming agent cannot rely on it.

**Triggers too broad.** "analyze" matches every analysis request in the workspace. The skill fires when it should not.

**Skill handling too many cases.** A skill with 8 conditional branches ("if A then X, else if B then Y, else if C...") is a sign it is several skills disguised as one.

**No preconditions.** Skill runs on an empty workspace and fails silently. Preconditions in the frontmatter prevent that.

**Missing `type:` field.** Will be refused by `validate-resources` check 13b. Not optional.

**Improvised domain reasoning inside the SKILL.md.** Never let the LLM reinvent the expert methodology on each run. The skill loads and applies a codified methodology from `resources/`. It does not re-derive it. See Skill Philosophy.
