---
name: mine-audience
type: producer
version: "1.0.0"
agent_id: mine-audience@v1.0
recommended_model: sonnet
layer: territoire
reasoning_pattern: null
description: >
  Mine voice-of-market from Reddit, Trustpilot, and Meta Ads Library for a product+brand pair.
  Identify candidate audience segments and propose enrichments to profile.json (psychology, voice, pain_points, objections).
  Triggers FR: "mine les audiences pour {product}", "identifie les audiences {brand}", "voice of market {product}".
  Triggers EN: "mine audiences for {product}", "find audience segments {brand}", "voice of market {product}".
permissions:
  reads: [brand, product]
  writes: [profile]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: "brand.json and spec.json must exist for the product being analyzed"
  postconditions: "run score-product-fit to evaluate fit between discovered audiences and product"
disambiguates_against:
  mine-voc: "route to mine-voc when the goal is the existing customer voice on THIS brand (Trustpilot, Judge.me, brand reviews) · mine-audience is upstream, exploring who the audiences are at the product/segment level"
  mine-vom: "route to mine-vom when the goal is the broader market voice (competitors' customers, niche communities) · mine-audience focuses on segment discovery and audience proposals for a specific product"
---

## Tone

Présente les audiences découvertes en langage humain : qui sont ces gens, ce qu'ils disent, ce qui les bloque. Verbatims > jargon marketing.

# Skill: mine-audience

This agent scrapes voice-of-market sources (Reddit discussions, Trustpilot reviews, Meta Ads Library competitor analysis) for a product, identifies candidate audience segments, and proposes enrichments to profile.json fields. The agent works in proposal mode · all mutations are written as `_proposals` for human review.

---

## Step 1 · Collect inputs and validate

Read `brands/{brand}/brand.json` and `brands/{brand}/products/{product}/spec.json`. Extract:
- `brand.name` and positioning
- `spec.identity` (category, positioning, tagline)
- `spec.target_audience` if present (as current hypothesis)

If either file is missing or incomplete → signal which file/fields are absent and stop gracefully. Do NOT hallucinate product details.

---

## Step 2 · Scrape voice-of-market sources

Execute three parallel scrapes:

**Reddit mining:**
- Read `operations/reddit/mine_reddit.py` (or equivalent script in workspace)
- Query relevant subreddits based on `spec.identity.category` (e.g., r/nursing for healthcare products, r/fitness for sports)
- Harvest 50–100 verbatims discussing pain points, frustrations, needs, desires related to the product category
- Verbatims must include original text + post context (subreddit, timestamp if available)
- Source each verbatim: `{"type": "verbatim", "platform": "reddit", "ref": "r/{subreddit}/comments/{id}"}`

**Trustpilot reviews mining:**
- Read `operations/trustpilot/mine_reviews.py` (or equivalent)
- Fetch reviews for the product itself (if it exists on Trustpilot) AND competitor reviews (same category)
- Extract verbatims from review text: pain points mentioned, benefits praised, objections, trust anchors
- 30–50 verbatims minimum
- Source: `{"type": "verbatim", "platform": "trustpilot", "ref": "product_id/{id}/review/{review_id}"}`

**Meta Ads Library competitors:**
- Read competitor ads from Meta Ad Library for the same product category
- Look for: targeting hints, pain-point language, emotional triggers in ad copy
- Extract 20–30 ad copy snippets as verbatims
- Source: `{"type": "scrape", "platform": "meta_ads_library", "ref": "account/{account_id}/ad/{ad_id}"}`

Aggregate all verbatims into a single pool. Total expected: 100–180 verbatims.

---

## Step 3 · Cluster verbatims into audience intersections

Group verbatims by recurring themes across pain points, desires, and behaviors. Use clustering logic:

1. Identify core pain points (what frustrates this group?)
2. Identify core desires (what do they want?)
3. Identify decision behaviors (how do they buy? What do they trust?)
4. Tag with demographic hints if present (age, profession, lifestyle, income level)

Generate 3–6 candidate audience clusters. For each cluster:
- **cluster_name**: human-readable name (e.g., "busy-nurses", "bargain-conscious-parents")
- **verbatim_count**: how many verbatims support this cluster
- **confidence**: 0.6–0.85 based on verbatim agreement
- **hypothesis**: 2–3 sentences describing this audience segment
- **sources_used**: list of platforms that provided signals for this cluster

---

## Step 4 · Synthesize proposals for profile.json

For each candidate audience cluster, produce proposals targeting profile.json fields:

**For profile.psychology:**
- `core_desire`: synthesized from verbatim desires
- `values`: list of top 3 values inferred (e.g., "authenticity", "efficiency", "family")
- `beliefs_limiting`: common objections or misconceptions (e.g., "all supplements are dangerous")
- `goals`: what does this audience want to achieve?
- `emotions`: top emotions mentioned in verbatims (stress, confidence, frustration, relief)

**For profile.voice:**
- `vocabulary_to_use`: key words/phrases found in verbatims (not brand language · real user language)
- `vocabulary_to_avoid`: terms this audience rejects or finds off-putting
- `key_expressions`: direct quotes from verbatims (with `origin: "voc"`)
- `tone_register`: inferred from verbatim tone (e.g., "casual-authoritative", "humorous-practical")

**For profile.pain_points[] and profile.objections[]:**
- Extract top 3–5 pain points by frequency (with `priority: 1–3`)
- Extract top 3 objections with frequency + lifecycle stage (awareness/consideration/decision)
- Each pain point gets: `formulation`, `emotion`, `trigger`, `awareness_stage`
- Each objection gets: `type` (prix/scepticisme/confiance/efficacité), `frequency` (1–10), `severity` (low/medium/high)

**Confidence calibration:**
- High confidence (0.8–0.85): 5+ distinct verbatims supporting the claim, consistent across sources
- Medium confidence (0.65–0.79): 2–4 verbatims, mostly consistent
- Lower confidence (0.55–0.65): 1–2 verbatims, inferred from context
- Never propose below 0.5 confidence

Call ``.skills/write-to-context.py` (canonical channel · see capture-learning Step 4 for the exact Bash invocation)` for each proposal field with:
- `field_path`: e.g., `profile/busy-nurses/psychology/core_desire`
- `value`: synthesized text or list
- `source`: `{"type": "verbatim", "platforms": ["reddit", "trustpilot"], "verbatim_count": 12}`
- `confidence`: per above calibration
- `mode`: `"proposed"` (always)

---

## Output Format

Markdown report saved in `brands/{brand}/reports/{timestamp}-mine-audience-{product}.md`.

Structure:
```
# Audience Mining Report · {brand} / {product}
Generated: {ISO timestamp}
Verbatims collected: {N}

## Executive Summary
{2–3 sentences on what was found}

## Audience Clusters Discovered

### Cluster 1: {cluster_name}
- **Size signal:** {verbatim_count} verbatims across {platforms}
- **Confidence:** {0.55–0.85}
- **Core hypothesis:** {2–3 sentences}
- **Top pain points:** {list}
- **Top objections:** {list}
- **Voice markers:** {key expressions}

### Cluster 2: {cluster_name}
...

## Proposals Generated
- {N} new profiles created as proposals
- {M} enrichments to existing profiles
- Review at: phantom review {brand}

## Data Quality
- Total verbatims processed: {N}
- Verbatim agreement rate: {%}
- Missing data signals: {if any}
```

---

## Hard Rules

- **Jamais écrire directement dans profile.json.** Tous les enrichissements passent par ``.skills/write-to-context.py` (canonical channel · see capture-learning Step 4 for the exact Bash invocation)` en mode `proposed`.
- **Never hallucinate verbatims.** If a source is unavailable, signal it explicitly. Do NOT generate fake quotes.
- **Source every claim.** Each proposal must have a `source` dict with `type`, `platform`, and a reference URL or ID.
- **Confidence ≤ 0.9 for agents.** Agent confidence must never reach 1.0. That's reserved for humans.
- **Max iterations** · stop after processing 3 sources (Reddit, Trustpilot, Meta). If sources fail, report what was attempted and what succeeded.
- **Anti-repetition** · never scrape the same subreddit/keyword twice in a single run. If a retry is needed, use a different search term.
- **Graceful degradation** · if Trustpilot is down, proceed with Reddit + Meta Ads. Log what was skipped. NEVER fail silently.
- **No cross-brand scope** · this agent mines one product per invocation. To mine multiple products, call the agent once per product.

---

## Dependencies & Integration

- **Requires:** `operations/reddit/mine_reddit.py`, `operations/trustpilot/mine_reviews.py` (or equivalent scrapers)
- **Outputs:** proposals in event log, report in `brands/{brand}/reports/`
- **Next step:** run `score-product-fit` to evaluate fit between discovered audiences and the product spec
- **Version conflict:** if running `mine-audience@v0.x` and `v1.0` in parallel, they write different event_ids (safe, no collision)

---

## Changelog

- **1.0.0** (2026-04-13) · Initial spec. Collect → Analyze → Propose pattern. Proposal mode enforced.
