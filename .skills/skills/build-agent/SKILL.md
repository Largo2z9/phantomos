---
name: build-agent
type: builder
version: "1.0.0"
recommended_model: opus
layer: meta
reasoning_pattern: null
description: >
  Custom agent architect. From a fuzzy operator intent, maps the available ecosystem
  (Context Engine, MCP, existing skills, workspace knowledge), designs the full
  architecture (1 or N agents), generates SKILL.md files directly executable in
  the workspace.
  FR: "construis-moi un agent", "je veux un agent qui", "build un outil qui",
  "j'ai besoin d'un agent pour", "construis-moi un système qui".
  EN: "build an agent", "I want an agent that", "build a tool that", "build a system that".
disambiguates_against:
  create-skill: "build-agent assemble un agent runtime (multi-skill + binding marque) depuis un intent flou. create-skill écrit un seul SKILL.md depuis un skill nommé. 'crée un skill' route create-skill; 'construis-moi un agent / un système qui' route build-agent."
  scaffold-extension: "scaffold-extension fait grandir le MODÈLE DE DONNÉES (entité custom, sidecar, schéma) pour un nouveau domaine à encoder. build-agent construit de nouvelles CAPACITÉS (skills/agents qui raisonnent ou produisent). Stocker/structurer une nouvelle donnée route scaffold-extension; un nouveau comportement route build-agent."
  connect-source: "connect-source branche un compte/API externe que l'opérateur utilise déjà (Meta, Shopify, un outil MCP). build-agent construit une capacité interne. 'branche mon compte X' route connect-source; 'construis un agent qui' route build-agent."
permissions:
  reads: [brand]
  writes: []
  mode: none
  subagent_safe: false
pipeline:
  preconditions: workspace deployed, .skills/agent-design-guide.md and .skills/how-to-build-skills.md present
  postconditions: run validate-resources to check workspace integrity
---

## Tone

The operator describes what they want in plain language. The agent translates into technical architecture silently. No technical jargon in the conversation, the output is a skill that works, not an architecture lecture.
---

# Skill: Build Agent

Agent architect for non-technical operators.

The operator has a business intent ("I want to monitor my competitors", "I want an automatic creative brief"). This skill turns that intent into functional agent(s). It maps what exists in the workspace, identifies the needed expertise, designs the architecture, asks the right questions, and generates SKILL.md files directly executable.

This skill is an **architect**, not a coder. It designs and orchestrates. Code generation is delegated.

## Invocation modes

Two entry modes, detected from context:

**Direct mode** (default). Operator has a clear intent (*"build an agent that monitors my competitors"*). Run the full flow below, one skill generated.

**Guided-mission mode** (triggered by `/tour` path (d) or by `first_skill_offered = false` surface in an opportune session). Operator has not yet built a skill. Instead of taking a raw intent, propose a concrete mission from a short catalog (e.g. publish a first Meta ad, set up a recurring reporting, monitor competitors). Decompose the mission into a **skill graph** — sequential skills with shared primitives (auth, API conventions, validation). Build each skill in order, explaining the decomposition logic as you go. Goal: the operator ends the session with real skills and a learned method, not just one skill. On completion, write `first_skill_built = true` to `/operator/awareness.json`.

The decomposition methodology for guided-mission mode is under active development. Until the method is formalized, the builder walks through each step explicitly with the operator and captures the decomposition pattern for later codification in `resources/sops/`.

## Delegation to `scaffold-extension`

When the dissection in Step 2b concludes that the intent maps to a **simple extension** — one custom entity plus an optional populating skill, or a sidecar enrichment — `build-agent` delegates to `scaffold-extension` rather than handling the scaffold itself.

**Detection rule** applied silently in Step 2b:

- Intent output is *"operator wants to track X over time"* or *"operator wants to store Y structurally"* or *"operator wants Z field enrichment on existing brand"* → **scaffold-extension scope**.
- Intent output is *"operator wants a multi-skill workflow with data flow between steps"* or *"operator wants a methodology agent with judgment loops"* → **build-agent scope** (handle internally).

When delegating, `build-agent` invokes `scaffold-extension` by surfacing the routing to the operator: *"Ton besoin rentre dans un pattern spécialisé · je passe la main au builder dédié, il va t'accompagner en neuf étapes. Je reviens après si on a des briques complémentaires à construire."* After `scaffold-extension` completes, `build-agent` either ends the session or continues with any remaining mission scope.

This delegation keeps each orchestrator narrow and composable. `scaffold-extension` owns the extension canonical path with its nine sub-skills; `build-agent` owns the generic architecture and delegates when the path is a known pattern.

---

## Step 1 — Load references and map the ecosystem

Before answering the operator, silently read in this order:

**Mandatory references (load first):**
- `.skills/agent-design-guide.md` — criteria to decide if an agent is justified, proven patterns, anti-patterns to avoid, contract with the Context Engine
- `.skills/how-to-build-skills.md` — method to write quality SKILL.md, common patterns, delivery checklist

**Available ecosystem:**

**Context Engine available:**
- `brands/*/brand.json` — which brands exist, which driver, which sector
- `brands/*/products/*/spec.json` — which products are encoded
- `brands/*/audiences/*/profile.json` — which audiences are active
- `brands/*/strategy/strategy.json` — if present
- `workspace-template/CLAUDE.md` — workspace rules and philosophy

**Existing skills:**
- List all files in `.skills/skills/*/SKILL.md`
- For each skill: read frontmatter (`name`, `description`) only, not full content
- Identify skills that could be reused or extended

**Available MCPs:**
- Read `.skills/mcp/README.md` to know which MCP capabilities are active
- Identify what the workspace can natively call (Meta Ads, Shopify, GA4, etc.)

**Existing knowledge:**
- Read `workspace-template/CLAUDE.md` → Philosophy section
- If `playbooks/` exists in the workspace → list the titles

This mapping is silent. Takes 30 seconds. Conditions everything that follows.

---

## Step 2 — Extract real business intent

Reply to the operator with **a single open question**:

> "Tell me what you want the agent to do, not technically, just what you want to be able to decide or produce with it."

Wait for the answer. Do not ask several questions at once.

Then, based on the answer, ask **one question at a time** to clarify:

| If the answer is fuzzy on... | Ask |
|-------------------------------|-------|
| Expected result | "What do you want to do with what the agent produces?" |
| Frequency | "Do you want it to run daily, on demand, or every session?" |
| Trigger | "Do you launch it manually, or should it run automatically?" |
| Scope | "On which brand(s) does it apply?" |
| Implicit expertise | Identify the domain (media buying, copy, analytics, CRO, etc.) and check if knowledge exists in the workspace |

Max 4 questions. Stop as soon as intent is clear. Never ask technical details, the operator doesn't know and shouldn't have to.

---

## Step 2b — Complexity gate + silent dissection + operator cartography

**CRITICAL:** before any deeper work, **YOU MUST** run this step. But tune the depth to the task's complexity — over-engineering a simple skill is as bad as under-engineering a complex one.

### Test 0 — Complexity gate (silent, mandatory first)

Binary test : *"Would a senior expert in this domain apply a named framework or matrix to do this, or is it pure mechanical execution?"*

- **Simple** (lookup, filter, rename, pure transformation, obvious output, no qualitative arbitrage, no domain thresholds) → skip full dissection. Go straight to Step 3b Tests A/B/C with minimal spec. **NEVER** codify expert methodology for a simple skill.
- **Complex** (output informs decisions, framework applied by a senior practitioner, variables/thresholds/context matter, domain literature exists) → full dissection below mandatory.

Examples :
- Simple → `list-brands-by-stage`, `show-progress`, `rename-audience-slug`
- Complex → `audit-klaviyo-deliverability`, `score-product-fit`, `generate-hook-brief`

### Silent dissection (complex tasks only)

**YOU MUST** fill a draft `.skills/skills/{name}/spec.md` silently covering the 10 dimensions below. **NEVER** expose raw dimensions to the operator.

1. **Real intent (expert relay)** — surface (what the operator said) vs deep (what business problem they actually solve). Push-back **YOU MUST** trigger if surface ≠ deep.
2. **Usage context** — frequency, who invokes (operator direct / another skill / scheduler), output destination (operator / external human / another skill)
3. **Data in / out** — entities read, fields consumed, destinations written, mode (proposed/direct/none)
4. **Infrastructure dependencies** — APIs, tools, auth, rate limits (exist in `resources/conventions/` ? YES/MISSING)
5. **Expert methodology to codify** ← *this is the core*
    - Canonical expert persona (who incarnates this at senior level in the real world)
    - Named framework they apply (AIDA, RFM, DMARC, JTBD, STPD, hook quality spec, etc.)
    - Key variables they compute (thresholds, metrics, signals)
    - Structuring matrix (2D or 3D grid that encodes decisions)
    - Formulas / heuristics if numeric
    - **Already codified in `resources/frameworks|catalogues|quality-specs|sops|conventions/` ? YES/MISSING** → if MISSING, Gate doc blocks generation until built
6. **Technical constraints** — model, subagent_safe, token budget, estimated latency
7. **Failure modes** — what breaks, what fallback, what graceful degradation
8. **Foreseeable evolution** — will it grow, split, become obsolete at 6 months ? V2 candidate patterns
9. **Overlap with existing skills** — recovery with what's already there, ENRICH vs CREATE decision
10. **Ecosystem impact** — touches template / brands / resources / operator profile

See `docs/system/patterns.md § Skill Philosophy` for the full doctrine.

Before generating SKILL.md, consult `docs/system/cookbook.md` for concrete build patterns (what to load, order, null-field behavior, pseudocode templates) that apply to skills consuming PhantomOS context.

### Operator cartography — visible synthesis (4-5 lines max)

Present the operator a **short cartography + one clear decision**. **YOU MUST** translate every technical term into operator-value language. **NEVER** expose PhantomOS internal vocabulary (`convention`, `framework`, `SOP`, `quality-spec`, `catalogue`, `entity`, `field`, `schema`) in this cartography — say what it *does for the operator*, not what it is internally.

**Template** (adapt to the detected conversation_register ; technical mode accepts denser tech shorthand) :

> *Analysé. Voilà ce que je lis :*
> *• **Ce que tu fais** : {deep intent reformulated in one sentence, operator language}*
> *• **La façon experte dont je vais raisonner** : {expert persona} applying {framework in plain terms}, grid / matrix {described in value terms}, key variables {translated}. {Already in your workspace | Needs to be codified first}.*
> *• **Insertion** : {new skill | enriches {existing skill in operator terms}}, lit {data in plain terms}, produit {output in plain terms}.*
> *• **Pour être au propre** : {nothing missing, go | X prereqs to build in operator terms, ~Yh}*

**Then AskUserQuestion** (load `ToolSearch(select:AskUserQuestion)` if not loaded) with 4 actionable options :

- *(a) Go, tu as bon → génère* (or *Construis les prérequis d'abord puis génère* if deps missing)
- *(b) Ajuste le scope (split / restreint / élargit)*
- *(c) Challenge la méthodo (tu veux une autre grille, un autre framework)*
- *(d) Autre, dis-moi*

**NEVER** ask more than one decision per turn. **NEVER** return to dimensions dissection in conversation — they stay in spec.md silently.

### Push-back obligation

If deep intent ≠ surface intent (ex: operator says *"automate my weekly reports"* but deep intent is *"stop doing low-value busywork, maybe kill the task altogether"*), **YOU MUST** push back before dissection : propose the challenge ("challenger le besoin plutôt qu'automatiser") as option in AskUserQuestion. See docs/system/patterns.md § Skill Philosophy.

### Persistence

After operator validates → persist `.skills/skills/{name}/spec.md` with the 10 dimensions filled. Skill.md generation proceeds at Step 4+. If operator picks *"skip dissection, just generate"* (complex task) → spec.md flagged *"dissection skipped by operator — revisit on first refactor"*.

---

## Step 3 — Identify needed expertise

From the clarified intent, identify:

1. **The business domain**: media buying / copywriting / analytics / CRO / product / other
2. **Existing knowledge**: does a playbook, skill, or brand context already cover this domain?

If existing knowledge is found, propose to the operator:

> "I found [playbook X / skill Y] in your workspace covering [domain]. Should the agent lean on this knowledge, or have its own independent logic?"

- **Lean on it** → the agent will read this file on every execution. If the playbook evolves, the agent evolves.
- **Independent logic** → expertise is embedded directly in the SKILL.md. More autonomous, less flexible.

Wait for the choice. Record the decision.

---

## Step 3b — Complexity heuristic (MANDATORY, 3 binary tests before Step 4)

**CRITICAL:** before designing architecture, **YOU MUST** run 3 binary tests silently. Their answers determine whether we generate 1 skill, split into an orchestrator + sub-skills, or stop to build prerequisite documentation first.

### Test A — Split into orchestrator?

> *"Can the need be decomposed into 2+ sub-tasks with logically independent Steps (different triggers, different outputs, usable separately)?"*

- **YES** → orchestrator + N sub-skills. Each sub-skill gets its own typology (via Test C below). The orchestrator chains them via Task tool when they are `subagent_safe: true`.
- **NO** → monolithic skill, continue to Test B.

Heuristic for "logically independent": if I could imagine the operator wanting only sub-task 2 without sub-tasks 1 and 3 on some other day, they are independent. If the sub-tasks only make sense executed together as a pipeline, they are internal Steps of one skill.

**Example (YES)**: *"build me an agent that audits my Klaviyo account"* → data pull + deliverability analysis + segmentation analysis + flows analysis → each usable separately on other days → **orchestrator + 4 sub-skills** (or 1 Producer with internal Steps if the 4 only make sense together as a single audit report).

**Example (NO)**: *"build me an agent that generates 3 creative brief angles from my brand"* → reads brand + applies creative framework + outputs 3 angles → one pipeline only, **1 Producer**.

### Test B — Prerequisite documentation needed?

> *"Does the skill consume an API, a framework, a platform convention, or a specialized methodology that has NO dedicated `resources/conventions/*.json`, `resources/frameworks/*.md`, or `resources/sops/*.md` file yet?"*

- **YES** → **STOP generation**. The skill would encode knowledge ad-hoc in its SKILL.md, violating `ENRICH > CREATE` and creating duplication. Instead:
  1. Identify the missing doc (convention for an API, framework for a methodology, SOP for a process).
  2. Run `ingest-resource` (via WebFetch on official docs if API, via operator briefing if framework) to build it.
  3. THEN come back to Step 3b and re-run the test.
- **NO** → continue to Test C.

**Example (YES)**: *"audit my Meta setup"* → consumes Meta Marketing API → check `resources/conventions/meta-ads.json` exists and is complete? If no → **STOP**, fill the convention first (rate limits, scopes, endpoints, pitfalls), then generate the skill.

**Example (NO)**: *"generate 3 creative brief angles"* → consumes brand context (already structured) + a creative framework that already exists in `resources/frameworks/` → **continue**.

### Test C — Assign typology (required output)

Apply the binary test of each typology (see `docs/system/patterns.md § Skill Taxonomy`) in this order, pick the FIRST match:

1. **Builder?** → writes into `.skills/` or modifies OS rules
2. **Orchestrator?** → calls 2+ named skills as sub-steps (from Test A = YES)
3. **Capturer?** → reads the current conversation to extract persistable knowledge
4. **Producer?** → output is a deliverable consumed directly by a human (operator, client, external)
5. **Curator?** → invoked in pipeline by other skills to maintain/query workspace state (backend)
6. **Navigator?** → invoked directly by the operator for orientation/understanding, no external deliverable (frontend)

**NEVER** assign 2 typologies. If the skill genuinely fits 2, the design is wrong, go back to Test A and split.

### Deliverable of Step 3b

**YOU MUST** present to the operator via `AskUserQuestion`:

> *"I've analyzed the need. Proposed architecture:*
> *- {1 skill | orchestrator + N sub-skills | stop, build doc first}*
> *- Typology: {type}*
> *- Prereq docs: {done | to build: list}*
> *Confirm or adjust?"*

Options: *Confirm / Adjust architecture / Change typology / Build prereq doc first*.

Wait for operator validation. Only then → Step 4 design.

---

## Step 4 — Design the architecture

Decide if the request needs **1 agent or several**.

**1 agent** if:
- Task is linear (read → analyze → produce)
- Output is single
- No strong specialization on distinct sub-tasks

**N agents** if:
- Multiple very different data sources
- Steps that require distinct expertise
- One step conditions the next with branching logic
- Intermediate output has value in itself

If N agents, design:
- **Agent A**: role, inputs, outputs
- **Agent B**: role, inputs, outputs
- **Orchestrator**: sequence logic, how A feeds B

Present to the operator:

```
Here's what I'll build:

Agent 1 — {name}: {role in one sentence}
  Reads: {sources}
  Produces: {output}

Agent 2 — {name}: {role in one sentence}
  Receives: {output from Agent 1}
  Produces: {final output}

Orchestrator — {name}: launches Agent 1 → passes the result to Agent 2.

Good, or want to adjust something?
```

If 1 agent, present the same way, simpler version. Wait for validation before generating.

---

## Step 4b — Determine skill typology (MANDATORY before Step 5)

**CRITICAL:** for each agent to generate, **YOU MUST** assign exactly one `type:` from the 6 typologies before generating the SKILL.md. Reference: `docs/system/patterns.md § Skill Taxonomy`.

Apply the binary test aloud, share the reasoning with the operator, then ask for confirmation:

> *"This skill takes input and produces a deliverable the operator will read directly → Producer. Default model: sonnet. Default subagent_safe: true. Confirm?"*

Use `AskUserQuestion` to propose the 6 options if the test is ambiguous.

**YOU MUST NEVER** generate a SKILL.md without a validated `type:`. If the operator's choice fails the binary test of the chosen typology, push back and re-test. If the skill genuinely fits 2 typologies → the design is wrong, split it into 2 skills.

---

## Step 5 — Generate SKILL.md files

For each agent validated at Step 4 and typed at Step 4b, generate `.skills/skills/{agent-name}/SKILL.md`.

Each generated file must:

**Frontmatter:**
- `name`: agent slug (`lowercase-with-dashes`)
- `type`: one of `producer | curator | capturer | orchestrator | navigator | builder` (validated at Step 4b)
- `version`: `"1.0.0"`
- `recommended_model`: default from typology (see Skill Taxonomy table). Override only with justification comment `# override: <reason>`.
- `description`: trigger phrases in FR and EN
- `pipeline.preconditions`: what must exist before
- `pipeline.postconditions`: what must run after (often `validate-resources`)

**Body:**
- Numbered, sequential, actionable steps
- Each step specifies: what to read, what to decide, what to produce
- Explicit output format (markdown, JSON, or both)
- Hard Rules: non-negotiable guardrails of the agent

**If the agent uses ``.skills/write-to-context.py` (canonical channel — see capture-learning Step 4 for the exact Bash invocation)`:**
- Explicitly state mutated fields, confidence value, mode (proposal by default)
- Never direct write to JSON, always via ``.skills/write-to-context.py` (canonical channel — see capture-learning Step 4 for the exact Bash invocation)`

**If the agent relies on existing knowledge (Step 3):**
- Add at Step 1: "Read [file] to load business context."
- Do not copy the knowledge into SKILL.md, reference the source file

**If orchestrator:**
- Generate a separate `.skills/skills/{orchestrator-name}/SKILL.md`
- It does nothing itself, it calls the agents in order and passes outputs

---

## Step 6 — Debrief the operator

Once files are generated, display:

```
{N} file(s) created:

→ .skills/skills/{agent-1}/SKILL.md
→ .skills/skills/{agent-2}/SKILL.md  (if applicable)
→ .skills/skills/{orchestrator}/SKILL.md  (if applicable)

To launch the assistant:
  "{main trigger phrase}"

What it will do:
  {2-line description max, plain language}

What it reads:
  {list of sources}

What it produces:
  {output described simply}

It's a v1.0. Run it once and tell me what's missing.
```

---

## Output Format

Files generated in `.skills/skills/{agent-name}/SKILL.md`. Content conforms to `_TEMPLATE/SKILL.md`.

Conversation ends with Step 6 debrief, no extra markdown, no exhaustive recap.

---

## Hard Rules

- **No technical jargon** with the operator. "SKILL.md file" can be said, but not "frontmatter", "MCP endpoint", "write contract", etc.
- **Never skip mapping** (Step 1). Even if the request seems simple, read first, reply after.
- **Max 4 questions** to clarify intent. Beyond that, the agent makes a reasoned choice and explains.
- **Always validate architecture** before generating (Step 4). Never generate without operator agreement.
- **``.skills/write-to-context.py` (canonical channel — see capture-learning Step 4 for the exact Bash invocation)` mandatory** for any agent that mutates the Context Engine. Never direct write.
- **Proposal mode by default** for any generated agent. Confidence = 1.0 reserved for `human:*` agents only.
- **Never create a skill that duplicates an existing skill.** If an existing skill covers 80%+ of the need, propose extending it rather than creating a new one.
- **The orchestrator does nothing itself.** It sequences only. Zero business logic in the orchestrator.
