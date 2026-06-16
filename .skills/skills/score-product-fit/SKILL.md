---
name: score-product-fit
type: producer
version: "1.0.0"
agent_id: score-product-fit@v1.0
recommended_model: haiku
layer: territoire
reasoning_pattern: null
description: >
  Evaluate product-audience fit by comparing spec.json against profile.json. Score 0-10, list strengths/gaps, identify language misalignment.
  Triggers FR: "evaluate le fit {product} × {audience}", "product-fit {brand}", "alignment {product} {audience}".
  Triggers EN: "evaluate fit {product} × {audience}", "product-fit analysis {brand}", "alignment analysis {product} {audience}".
permissions:
  reads: [product, profile]
  writes: [learning]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: "spec.json and profile.json must both exist and contain required fields"
  postconditions: "optional: promote top insights to learnings via promote-learning"
---

## Tone

Score + explication en langage courant. "Ce produit colle bien à cette audience parce que..." · pas un tableau de métriques abstraites.

# Skill: score-product-fit

This agent is an analysis engine (NOT a Context Engine mutator). It reads spec.json and profile.json, compares them systematically, and produces a fit report with:
- Fit score (0–10)
- Strengths (where product matches audience needs/language)
- Gaps (where audience needs aren't met, or language misaligns)
- Strategic priority recommendation (high/medium/low)
- Optional proposals to `profile.brand_alignment` and `profile.strategic_priority` fields

The agent does NOT mutate the Context Engine directly. Proposals are optional if strong signals warrant persistence; otherwise the report is transitional analysis only.

---

## Step 1 · Load and validate inputs

Read `brands/{brand}/products/{product}/spec.json` and `brands/{brand}/profiles/{audience}/profile.json`.

Validate required fields exist:
- **From spec.json:** `identity` (positioning, tagline, category), `benefits[]`, `key_features[]` if present
- **From profile.json:** `psychology` (core_desire, values, goals), `voice` (vocabulary_to_use), `pain_points[]`, `objections[]`

If critical fields are missing (e.g., no pain_points in profile), note it in the report as `[not defined]` and proceed with what's available.

---

## Step 2 · Analyze need satisfaction

Compare product benefits against audience pain points and desires:

**Mapping matrix:**
For each pain point in `profile.pain_points[]`:
- Does the product address it? (Yes / Partially / No)
- Which product benefit or feature maps to the pain relief?
- Is the benefit claim credible for this audience level? (e.g., "professional credentials" for nurses, "peer reviews" for bargain-conscious)

Produce a table:
| Pain Point | Product Addresses | Feature/Benefit | Credibility |
|---|---|---|---|
| {pain point} | Yes/Partial/No | {feature or "None"} | High/Medium/Low |

**Scoring rule:**
- **Full satisfaction:** 3 out of 3 top pain points fully addressed → +3 points
- **Partial satisfaction:** 2/3 addressed fully, 1/3 partially → +2 points
- **Weak satisfaction:** 1/3 fully, others partial/none → +1 point
- **No satisfaction:** 0/3 → +0 points

---

## Step 3 · Analyze language alignment

Compare product messaging against audience voice:

**Vocabulary alignment:**
- Extract top 3 words from `spec.identity` (positioning, tagline)
- Compare against `profile.voice.vocabulary_to_use` and `vocabulary_to_avoid`
- Match: how many spec words appear in audience vocabulary? (0–100%)
- Mismatch: how many spec words are in the "avoid" list? (0–10 is good, 10+ is red flag)

**Tone register match:**
- Infer spec tone from tagline + positioning (e.g., "premium-authoritative", "playful-casual")
- Compare to `profile.voice.tone_register`
- Match (yes/no/partial)

**Key expressions:**
- Do key brand expressions (tagline, claims) use language the audience recognizes and uses?
- Rate: High alignment / Partial / Misaligned

**Scoring rule:**
- **Strong language fit:** vocabulary match >70%, tone aligned, expressions resonate → +2.5 points
- **Medium fit:** vocabulary 50–70%, tone partially aligned → +1.5 points
- **Weak fit:** vocabulary <50%, tone misaligned → +0.5 points

---

## Step 4 · Analyze objection readiness

Compare product attributes against audience objections:

For each top 3 objections in `profile.objections[]`:
- **Objection type** (prix/scepticisme/confiance/efficacité)
- **Does product have a counter-argument?**
  - Price objection: does product offer value story, payment plan, guarantee?
  - Trust objection: does product have third-party validation, customer testimonials, credentials?
  - Efficacy objection: does product have proof points (studies, before/after, expert endorsement)?

**Scoring rule:**
- **All top objections addressed:** +2 points
- **2 out of 3 addressed:** +1 point
- **1 or fewer addressed:** +0 points

---

## Step 5 · Compute fit score and ranking

**Total fit score = need satisfaction + language alignment + objection readiness** (out of 10)

Example breakdown:
```
Need satisfaction:   3.0  (full satisfaction of top pain points)
Language alignment:  2.0  (strong vocabulary + tone match)
Objection readiness: 1.5  (2/3 objections addressed)
───────────────────────
TOTAL FIT SCORE:     6.5  (medium fit, actionable)
```

**Strategic priority ranking:**
- **Fit ≥ 8:** High priority (strong market fit, minimal risk)
- **Fit 6–7.9:** Medium priority (good fit, some language or objection gaps to address)
- **Fit 4–5.9:** Lower priority (fundamental fit exists but gaps are substantial)
- **Fit < 4:** Very low priority (misaligned or needs significant repositioning before scaling)

---

## Step 6 · Identify gaps and recommendations

List top 3 gaps (highest impact):

**Gap types:**
1. **Unaddressed pain point:** audience feels X, product doesn't solve X. Recommend: adjust messaging or feature roadmap.
2. **Language mismatch:** audience speaks Y, product copy uses Z. Recommend: rewrite messaging in audience vocabulary.
3. **Unresolved objection:** audience worried about [price/trust/efficacy], product doesn't counter it. Recommend: add trust anchor, testimonial, or price flexibility.

For each gap, rate impact: High (blocks scaling) / Medium (slows conversion) / Low (nice-to-have).

---

## Step 7 · Propose optional mutations

**IF fit score ≥ 7 AND language alignment is strong:**
- Propose to `profile.brand_alignment` → value: `{"product_fit_score": 7.5, "language_match": "strong", "last_reviewed": "2026-04-13"}`
- Confidence: 0.75–0.85 (based on data completeness)

**IF strategic priority is clearly Medium or High:**
- Propose to `profile.strategic_priority` → value: "high" or "medium"
- Confidence: 0.7–0.8

These proposals are OPTIONAL and only written if the signal is strong. If fit is uncertain (6–7 range), skip proposals · let the report stand on its own.

---

## Output Format

Markdown analysis report saved in `brands/{brand}/strategy/score-product-fit-{product}-{audience}-{date}.md`.

Structure:
```
# Product-Audience Fit Analysis
**Product:** {brand} / {product}
**Audience:** {audience_name}
**Generated:** {ISO timestamp}

## Fit Score: {X.X} / 10
- **Strategic Priority:** {High/Medium/Low}
- **Recommendation:** {one-line summary}

## Fit Breakdown

### Need Satisfaction: {score}/3
| Pain Point | Product Addresses | Feature | Credibility |
|---|---|---|---|
| {pp1} | Yes/Partial/No | {feature} | High/Medium/Low |
...

### Language Alignment: {score}/2.5
- **Vocabulary match:** {X}%
- **Tone register:** {match status}
- **Key expressions:** {resonance level}
- **Verdict:** {strong/partial/weak}

### Objection Readiness: {score}/2
| Objection | Product Counter-Argument | Coverage |
|---|---|---|
| {obj1} | {answer or "None"} | Yes/Partial/No |
...

## Top 3 Gaps

### Gap 1: {gap_type}
- **Impact:** {High/Medium/Low}
- **Description:** {what's missing}
- **Recommendation:** {how to address}

...

## Data Quality & Limitations
- Profile completeness: {%}
- Spec detail level: {sufficient/partial/minimal}
- Analysis confidence: {high/medium/low}
- Missing signals: {if any}

## Next Steps
- [ ] If fit ≥ 7: scale audience in media plan
- [ ] If fit 6–7: address top gaps before scaling
- [ ] If fit < 6: reconceptualize positioning or audience
```

---

## Hard Rules

- **Jamais écrire directement dans profile.json.** Les proposals passent par ``.skills/write-to-context.py` (canonical channel · see capture-learning Step 4 for the exact Bash invocation)` en mode `proposed`, ou ne sont pas écrites du tout (rapport seul).
- **Analysis before mutation.** Ce skill est un analyse engine. Les mutations Context Engine sont optionnelles et générées seulement si la confiance est forte (≥ 0.7).
- **No assumptions on missing data.** If `pain_points[]` is empty, note `[profile incomplete]` in the report. Never assume pain points.
- **Confidence ≤ 0.85 for scoring.** Even with strong signals, human review is mandatory for mutation decisions.
- **Single product × single audience per run.** This agent compares one product against one audience. To analyze multiple audiences, invoke once per audience.
- **Graceful degradation.** If profile lacks voice data, proceed with need satisfaction only (it's still valuable). Clearly note what was skipped.
- **No hallucinated objections.** Only score objections explicitly in `profile.objections[]`. Don't invent objections based on category assumptions.

---

## Dependencies & Integration

- **Requires:** spec.json and profile.json for the product-audience pair
- **Outputs:** markdown report in `brands/{brand}/strategy/`, optional proposals in event log
- **Consumed by:** humans doing strategic decisions; optionally feeds into promotion-learning workflow
- **Related:** if fit score suggests repositioning, hand off to copy-writer or product team (out of scope)

---

## Changelog

- **1.0.0** (2026-04-13) · Initial spec. Read → Analyze → Optional Propose pattern. Analysis first, mutation secondary.
