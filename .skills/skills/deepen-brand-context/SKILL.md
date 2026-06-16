---
name: deepen-brand-context
type: orchestrator
version: "1.0.0"
recommended_model: sonnet
layer: territoire
reasoning_pattern: null
description: >
  Orchestrates deepening of brand context after snapshot. Chains mine-voc
  (Voice of Customer) → mine-vom (Voice of Market) → cross-deepening-signals
  (cross-skill synthesis). Market deep-dive (study-niche-marketdeepdive) is
  NOT in the default chain due to cost asymmetry · operator-pulled standalone
  only. Output: a final synthesis paragraph naming the load-bearing cross-
  signals between customer voice and market voice, plus the structured
  outputs from each delegated skill.
  FR: "deepen {brand}", "approfondis {brand}", "VoC + VoM ensemble", "audit complet contexte", "voix client et marché".
  EN: "deepen {brand}", "deep dive customer + market", "full deepening".
permissions:
  reads: [brand, product, profile, learning]
  writes: [brand, product, profile, learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: false
pipeline:
  preconditions: brand exists with snapshot complete (snapshot-brand has filled spec.json + offers.json + at least one profile.json). Operator has indicated trust in the snapshot.
  postconditions: |
    - mine-voc Layer A + B applied
    - mine-vom Layer A + B applied
    - cross-deepening-signals synthesis delivered to operator
    - status.json updated, snapshot rebuilt, finalize-mutation-batch event emitted
disambiguates_against:
  mine-voc: "route directly to mine-voc when operator wants ONLY customer voice (faster, lighter)"
  mine-vom: "route directly to mine-vom when operator wants ONLY market voice (faster, lighter)"
  study-niche-marketdeepdive: "route to standalone study-niche-marketdeepdive when operator wants strategic memo on the niche, not customer + market voice. NOT chained here due to 30-60 min runtime."
  onboard-brand: "route to onboard-brand for the full setup pipeline from scratch · deepen-brand-context assumes snapshot is done"
---

# deepen-brand-context

Chairman orchestrator. Chains the two voice-deepening specialists and a synthesis sub-skill, then delivers one strategic read. Narrate handoffs briefly. Never expose Task tool internals to the operator. Final synthesis follows snapshot Step 7 voice canon strictly.

## Expert methodology

Posture: senior agency lead delegating two specialists (consumer insights + market strategy) and reading their briefs side by side to produce one cross-signal synthesis.

Framework: sequential chain with cross-synthesis at the end. mine-voc and mine-vom run as subagents (both subagent_safe: true). cross-deepening-signals runs as final sub-skill, reads what both produced, names the cross-signals, returns the synthesis.

Hard line per onboard-brand precedent: this skill does not re-implement what the subskills already do. It delegates, listens, synthesizes via cross-deepening-signals, finalizes.

## Step 0 · Pre-flight

Verify brand state:

```bash
cat brands/{slug}/status.json
ls brands/{slug}/audiences/
cat brands/{slug}/spec.json | head -20
```

Gates:
- spec.json exists and non-empty
- offers.json exists with at least one offer
- audiences/ has at least one profile.json
- snapshot.md exists (snapshot-brand was run)

If any gate fails → stop, route operator to onboard-brand or setup-brand. Do not start the chain on a half-built brand.

Announce the pipeline:

> *"OK, deepening complet de {brand}. Je chain VoC (15 min) → VoM (25 min) → synthèse croisée (5 min). Total ~45 min. Je peux te briefer en cours, ou tu reviens à la fin et je te livre la synthèse intégrée. Tu choisis."*

Then ask via AskUserQuestion with four paths:
- "Je reste, briefe-moi en cours" · interactive mode, each subskill surfaces its own synthesis as it lands
- "Je reviens à la fin" · silent mode, only the final cross-synthesis is delivered
- "Lance VoC seulement (skip VoM)" · bypass orchestrator, route to mine-voc direct
- "Lance VoM seulement (skip VoC)" · bypass orchestrator, route to mine-vom direct

If operator picks a single skill → exit orchestrator, hand off to that skill standalone. The orchestrator only proceeds when operator has confirmed full chain (option 1 or 2).

## Step 1 · Delegate mine-voc

Spawn mine-voc as subagent via Task tool.

Inputs forwarded:
- brand slug
- run mode ("interactive" or "silent" per Step 0 choice)
- optional `--focus={objections|jobs|vocabulary|risks}` if operator passed it
- optional `--depth=deep` if operator passed it (recommend ticket · see Hard Rules)

Expected return:
- Layer A archive of verbatims (sources/voc/{run-date}/*.jsonl)
- Layer B mutations proposed against brand.json (audience candidates, voice.key_expressions enrichments, jobs-to-be-done, objections, risks)
- 5-paragraph synthesis (interactive mode only)

Operator-facing line during the run, no tool mechanics:

> *"Je dig les reviews et threads clients. Je reviens dans ~15 min."*

While mine-voc runs, orchestrator stays available to operator. Returns at natural break.

## Step 2 · Delegate mine-vom

Spawn mine-vom as subagent via Task tool.

Inputs forwarded:
- brand slug
- run mode (same as Step 1)
- optional `--vom-focus={white-space|sophistication|vernacular|positioning}` from operator
- competitors context (if competitors[] thin, mine-vom auto-triggers its competitor integrity pre-step)

Expected return:
- Layer A archive of market signals (sources/vom/{run-date}/*.jsonl)
- Layer B mutations proposed (sophistication_stage, market_vernacular, white-spaces, positioning, external_intelligence)
- 5-paragraph synthesis (interactive mode only)

Operator-facing line:

> *"Je passe au market · concurrents, vocabulaire, white-spaces. ~25 min."*

## Step 3 · Delegate cross-deepening-signals

Spawn cross-deepening-signals as sub-skill via Task tool. Sub-skill is subagent_safe: true and operator_facing: false · only this orchestrator invokes it.

Inputs:
- brand slug
- run timestamp range scoping which Layer B mutations to read (this run only, not historical)

Sub-skill reads:
- mine-voc Layer B mutations from this run (verbatim_quotes added, audience candidates proposed, voice.key_expressions enriched)
- mine-vom Layer B mutations from this run (sophistication_stage, market_vernacular, white-spaces, external_intelligence)

Sub-skill detects three cross-checks (defined in cross-deepening-signals SKILL.md): audience-market presence, vocabulary shift alignment, white-space × channel signals.

Returns: synthesis_text + structured check verdicts in JSON.

## Step 4 · Final synthesis (operator-facing, MANDATORY format)

Apply snapshot Step 7 voice canon strictly: prose-first, no bold-section anchors, no enumerated checks, no marketing language, no hype words. Three movements, 3-6 sentences each, 18 sentences max total. Operator reads in 90 seconds.

The orchestrator delivers cross-deepening-signals output as the final synthesis. In "briefe en cours" mode the operator already saw the individual VoC + VoM syntheses, so this final read is purely cross-signal · never a concatenation.

Three movements:
- **Movement 1** · the dominant cross-signal. Validation or contradiction between VoC and VoM. Example Respire: VoC reveals a "22-32 peau jeune réactive" candidate, VoM confirms the segment is actively discussed in clean-beauty Reddit and TikTok, verdict = validated audience, write to profile.json.
- **Movement 2** · the second-order insight. Often a timing or positioning question. Example: VoM detects market vocabulary shifted from "clean" to "actifs prouvés", VoC shows brand customers still talk "clean" · repositioning has timing risk on the existing base.
- **Movement 3** · the strategic priority for next 30 days based on cross-skill confluence. Example: VoM white-space on pregnancy/post-grossesse + VoC Reddit thread evidence of demand = priority lane, mine-vom flagged a top-3 strategic move.

Close with:

> *"Want to validate these cross-signals into the brand strategy, or keep digging on a specific axis?"*

If operator picks "validate" → route to setup-brand or update profile.json/brand.json with the cross-signal mutations marked status: validated.
If operator picks "keep digging" → ask which axis, route to mine-voc/mine-vom with --focus, or to study-niche-marketdeepdive if the question is strategic memo territory.

## Step 5 · Finalize

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

If the subskills already finalized individually (each emits its own coherence_check), this final pass validates orchestrator-level emission of `coherence_check` for the chain as a whole.

Update status.json:
- `last_deepening_run`: timestamp
- `voc_run_id`, `vom_run_id`, `cross_synthesis_run_id`
- snapshot rebuild triggered if profile.json mutations promoted

## --focus parameter (optional, forwarded)

```
deepen respire                          # default full chain
deepen respire --skip=vom               # VoC only via orchestrator (still cross-synthesis if other run exists)
deepen respire --skip=voc               # VoM only via orchestrator
deepen respire --voc-focus=objections   # forward focus to mine-voc
deepen respire --vom-focus=white-space  # forward focus to mine-vom
deepen respire --depth=deep             # forwarded to both, recommend ticket
```

When `--skip=vom` or `--skip=voc` is passed, orchestrator runs the remaining subskill, then runs cross-deepening-signals against the latest historical run of the skipped skill (if it exists) or downgrades synthesis to single-axis read with a warning.

## Hard Rules

- **Never re-implement subskill logic.** Orchestrator delegates. Per onboard-brand precedent · purity rule.
- **Never expose Task tool mechanics.** Say "I'm digging customer reviews" not "I spawned a subagent".
- **Always run cross-deepening-signals at end.** The value is in cross-skill synthesis, not in the individual outputs. Skipping it = wrapper, not orchestrator.
- **study-niche-marketdeepdive is NEVER in this chain.** Cost asymmetry (30-60 min, strategic memo scope). Standalone only · operator pulls it explicitly when they want a niche-level read, not customer+market voice.
- **Operator chooses brief mode at Step 0.** Never assume. The four-path AskUserQuestion is mandatory.
- **finalize-mutation-batch at end of full chain.** Even if subskills finalized individually.
- **No ticket required for default chain (~45 min).** Ticket recommended only if operator passes `--depth=deep` to either subskill.
- **One brand at a time.** No parallel deepening on multiple brands · confuses Layer B mutation scoping.
- **Snapshot must be complete.** Half-built brands route to setup-brand, not deepen.

## Cross-references

- `.skills/skills/mine-voc/SKILL.md` · delegated subagent
- `.skills/skills/mine-vom/SKILL.md` · delegated subagent
- `.skills/skills/cross-deepening-signals/SKILL.md` · final synthesis sub-skill
- `.skills/skills/study-niche-marketdeepdive/SKILL.md` · sibling, NOT chained
- `.skills/skills/onboard-brand/SKILL.md` · orchestrator pattern reference (purity rule)
- `.skills/skills/snapshot-brand/SKILL.md` · voice canon for Step 7 synthesis
- `docs/system/contextual-intelligence.md` · master doctrine
- `docs/system/voice.md` · voice canon
