---
name: cross-deepening-signals
type: orchestrator
version: "1.0.0"
recommended_model: sonnet
layer: territoire
reasoning_pattern: null
operator_facing: false
description: >
  Sub-skill invoked by deepen-brand-context. Reads mine-voc and mine-vom
  Layer B mutations from a single deepening run, detects three cross-checks
  (audience-market presence, vocabulary shift vs current vernacular, white-
  space vs channel signals), produces a 3-movement synthesis paragraph
  naming the load-bearing cross-signals. NOT invoked by operator directly.
  FR: "cross-deepening" "synthèse cross-signals" "croise les signaux de deepening".
  EN: "cross-deepening" "cross-signal synthesis" "cross deepening signals".
permissions:
  reads: [brand, product, profile, learning]
  writes: []
  emits_events: [coherence_check]
  mode: none
  subagent_safe: true
invocable_by:
  - deepen-brand-context
---

# cross-deepening-signals

> v2.32 reclassement : type shared vers orchestrator. Skill coordonne VoC x VoM signals (multi-input synthesis), pattern orchestrator natif. Pas un primitif réutilisable.

Structured machine output for the orchestrator caller. Operator surface = the synthesis paragraph only, delivered upstream via deepen-brand-context. This skill does not write to brand entity files. It reads, analyzes, returns.

## Expert methodology

Posture: senior strategy partner reading the consumer insights brief and the market study side by side, naming the one or two cross-signals that change the strategic read. Not an aggregator. A cross-signal detector.

Framework: three mandatory cross-checks. Each cross-check returns one of three verdicts. The verdicts inform a 3-movement synthesis. The synthesis follows snapshot Step 7 voice canon strictly · prose-first, no enumeration, no bold-section anchors.

## The three cross-checks (mandatory)

### Check 1 · VoC audience candidate × VoM market presence

Read mine-voc Layer B: did it propose a new audience candidate from verbatim signals? Example Respire: *"22-32 peau jeune réactive"* surfaced from Sephora reviews and Reddit threads.

Read mine-vom Layer B: is this sub-segment present in the niche?
- Forum mentions (Reddit, specialized communities)
- Competitor targeting signals (ads, landing pages, listicles)
- Press / influencer coverage of the segment

Verdict (one of):
- **Validated** · VoM confirms the segment exists and is discussed in the niche. Audience candidate moves to status `validated`, write to profile.json.
- **Brand-specific** · VoC reveals it but VoM shows the market doesn't talk about it. Potential moat. Tag as brand-bound, valoriser in positioning, do not assume scalable acquisition vocabulary.
- **Phantom** · VoC verbatims are weak (1-2 mentions, no pattern), VoM no signal. Drop the candidate, mark as noise in learning.

### Check 2 · VoM vocabulary shift × VoC current vernacular

Read mine-vom Layer B: did it detect a vocabulary shift in the market? Example: *"clean → actifs prouvés"* · the niche has moved from purity claims to efficacy claims.

Read mine-voc Layer B: what vocabulary does the brand's own customer base use? Read voice.key_expressions[] mutations and verbatim_quotes from this run.

Verdict (one of):
- **Brand customers ahead** · VoC shows they already use the new vocab. The operator's own communication is the lag. Update copy now, customers won't resist.
- **Brand customers behind** · VoC shows old vocab dominant. Repositioning has timing risk, may alienate the current base. Stage the shift over months, not weeks.
- **No gap** · vocab aligned. No urgency. Note in synthesis only if Movement 1 or 3 has no signal.

### Check 3 · VoM white-space × VoC channel signals

Read mine-vom Layer B: did it identify white-spaces? Recurring market need × no top-player coverage. Example Respire: pregnancy / post-grossesse skincare gap surfaced in mine-vom competitor scan.

Read mine-voc Layer B: do brand customers signal demand for any of those white-spaces in their verbatims? Reddit threads, review questions, support tickets.

Verdict (one of):
- **High-confidence opportunity** · white-space + customer demand signal. Priority strategic move. Example Respire: pregnancy gap + Reddit thread evidence = top-3 lane for next 30 days.
- **Market-only opportunity** · white-space exists, no current customer signal. Speculative bet, longer ROI horizon, not a 30-day priority.
- **Customer-only opportunity** · customer demand exists but the market is crowded. Not a white-space, just a feature gap. Tactical move, not strategic.

## Step 1 · Read the corpus

Load this run's outputs:

```bash
ls brands/{slug}/sources/voc/{run-date}/
ls brands/{slug}/sources/vom/{run-date}/
```

Read:
- `brands/{slug}/sources/voc/{run-date}/*.jsonl` · Layer A verbatims
- `brands/{slug}/sources/vom/{run-date}/*.jsonl` · Layer A market signals
- Latest mutations to `brand.json#market.*` from this run
- Latest mutations to `audiences/*/profile.json` from this run
- `brand.json#voice.key_expressions` (current state + this run's enrichments)

Scope strictly to this run. Historical Layer B mutations from previous deepening runs are out of scope · they're already in brand state.

## Step 2 · Apply the three cross-checks

Process each check in order. Document the verdict + the supporting evidence (1-2 sentences per check, internal log). If a check has no signal (e.g. mine-voc didn't propose any audience candidate this run), explicitly note "no signal" and skip the corresponding movement · do not invent.

Internal log format (not operator-facing):

```
Check 1 (audience_market_presence): validated | candidate="22-32 peau jeune réactive" | voc_evidence="3 Sephora reviews + 2 Reddit threads" | vom_evidence="active TikTok and r/SkincareAddiction segment"
Check 2 (vocabulary_shift_alignment): brand_behind | shift="clean → actifs prouvés" | voc_evidence="78% of recent reviews still use 'clean'"
Check 3 (whitespace_channel_confluence): high_confidence | whitespace="pregnancy/post-grossesse" | voc_evidence="Reddit thread r/BeautyAddictionFR, 4 verbatims requesting pregnancy-safe routine"
```

## Step 3 · Synthesis (3 movements, snapshot Step 7 canon)

Build the operator-facing synthesis. Strict prose-first, no bold-section anchors, no enumerated checks. The three cross-checks inform the three movements but never appear as headers.

- **Movement 1** = the dominant signal. Typically Check 1 (validated audience) or Check 3 (high-confidence white-space) when either is strong. If both are strong, Movement 1 = whichever has the deeper evidence base.
- **Movement 2** = the second-order insight. Typically Check 2 (vocabulary timing) or a contradiction surfaced between checks (e.g. VoC validates an audience that VoM shows the market doesn't address · moat opportunity).
- **Movement 3** = the strategic priority for next 30 days based on confluence. The "what to do Mvitatone morning" read.

Hard rule: 3-6 sentences per movement. Cap at 18 sentences total. Operator reads in 90 seconds. Concrete examples (real brand names, real verbatim fragments) preferred over abstract framing.

If a check returns "no signal", drop the corresponding movement or replace with whichever check has signal. Better one strong movement than three thin ones.

## Step 4 · Emit event

```bash
python3 .skills/emit-event.py \
  --kind coherence_check \
  --payload '{"brand_slug":"{slug}","ok":true,"warnings":N,"blocking":0,"source":"cross-deepening-signals","run_id":"{run_id}"}'
```

Warnings increment when a check returns "phantom" (Check 1), "brand_behind" with high copy lag (Check 2), or "customer_only" with crowded market (Check 3). Blocking stays at 0 · this is a synthesis layer, not a gate.

## Output to caller

Returns to deepen-brand-context:

```json
{
  "synthesis_text": "...",
  "checks": {
    "audience_market_presence": "validated|brand_specific|phantom|no_signal",
    "vocabulary_shift_alignment": "brand_ahead|brand_behind|no_gap|no_signal",
    "whitespace_channel_confluence": "high_confidence|market_only|customer_only|no_signal"
  },
  "evidence": {
    "audience_market_presence": "...",
    "vocabulary_shift_alignment": "...",
    "whitespace_channel_confluence": "..."
  },
  "run_id": "...",
  "emitted_at": "..."
}
```

The orchestrator surfaces synthesis_text to operator. The structured checks + evidence are logged for traceability and future learning extraction.

## Hard Rules

- **Read-only.** Never writes to brand entity files. Synthesis is operator-facing via orchestrator, not direct mutation. Promotion of cross-signals into brand state is the operator's call (post-synthesis "validate" path in deepen-brand-context Step 4).
- **NOT invoked by operator directly.** operator_facing: false enforced. Only deepen-brand-context invokes this skill.
- **Three cross-checks are MANDATORY.** Skipping a check = incomplete synthesis. If a check returns "no signal", document it as no_signal in the JSON return, do not silently skip.
- **No invention.** Cross-signals are based on what BOTH skills actually surfaced this run. If VoM has no white-space data, Movement 3 is dropped or replaced · never fabricated.
- **3-movement synthesis follows snapshot Step 7 canon strictly.** Prose-first, no bold-section anchors, no enumerated checks, no marketing language, 18 sentences max total.
- **Scope to this run only.** Historical Layer B mutations from prior deepening runs are out of scope.
- **Emit coherence_check event mandatory.** Even if all three checks return strong signals · the event marks the chain completion.
- **Concrete examples over abstract framing.** Use real brand names, real verbatim fragments, real white-space labels. Abstract synthesis = unreadable synthesis.

## Cross-references

- `.skills/skills/deepen-brand-context/SKILL.md` · caller orchestrator
- `.skills/skills/mine-voc/SKILL.md` · Layer B source (audience candidates, voice.key_expressions, verbatims)
- `.skills/skills/mine-vom/SKILL.md` · Layer B source (sophistication_stage, market_vernacular, white-spaces)
- `.skills/skills/snapshot-brand/SKILL.md` · voice canon for synthesis (Step 7 prose-first)
- `.skills/emit-event.py` · event emission primitive
- `.skills/finalize-mutation-batch.py` · orchestrator-level finalization (called upstream by deepen-brand-context, not here)
- `docs/system/contextual-intelligence.md` · master doctrine
- `docs/system/voice.md` · voice canon
