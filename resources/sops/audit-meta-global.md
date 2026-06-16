---
name: audit-meta-global
type: sop
category: audit
scope: single-brand
version: "1.0.0"
author: phantomos-template
last_reviewed: 2026-04-23
language: en-mixed-fr
description: >
  End-to-end audit methodology for a Meta Ads account on a single e-commerce brand.
  Covers tracking foundations, account hygiene, campaign structure, audiences, creative
  strategy, compliance, post-click integrity. Written to match what a senior paid
  media consultant would check on an engagement. Produces a prioritized findings
  report with severity-flagged gaps and concrete remediation steps.

invoked_by:
  - orchestrator: audit-meta-global
  - orchestrator: audit-global (inside portfolio-wide audit)
  - operator direct: "audit complet Meta sur {brand}"
  - operator direct: "meta audit"

requires:
  - Meta Ads account access (ads_read scope minimum, ads_management for deeper checks)
  - Pixel ID known
  - At least 30 days of spend history (for performance rollups)
  - brand.json#/platforms/meta/account_id populated
  - brand.json#/identity/language (for ad copy review)

precondition_checks:
  - mini_skill: check-meta-access-valid
  - mini_skill: check-pixel-id-present

used_in_scenarios:
  - "new client onboarding audit (week 1 discovery)"
  - "quarterly account review with client"
  - "pre-scaling diagnostic (before significant budget increase)"
  - "post-incident diagnostic (drop in ROAS, ban, anomaly)"
  - "agency switching audit (taking over from another agency)"

output_schema:
  format: markdown report
  sections:
    - executive_summary (3-5 bullets, severity-flagged)
    - findings_by_layer (structured per checkpoint)
    - prioritized_action_plan (P0/P1/P2/P3)
    - estimated_remediation_effort
    - checklist_pass_rate (X/Y per layer)

output_destination:
  - brands/{slug}/deliverables/audits/meta-global-{YYYY-MM-DD}.md
  - brands/{slug}/pending-validations.md (operator-actionable items appended)

estimated_runtime: 15-30 minutes (depends on account size + mini-skill availability)
estimated_tokens: ~40-80k (scales with ad count + data depth)

---

# SOP · Audit Meta Global (single brand)

> This is a methodology document. It defines WHAT to check, in WHICH ORDER, with WHICH SEVERITY, and WHICH mini-skill executes each check. It does NOT contain the execution logic · that lives in the mini-skills. An orchestrator reads this SOP, iterates the checkpoints, calls the mini-skills, and composes the output report.

## Framing posture

The operator reading this audit is either an agency manager presenting to a client, or a solo operator diagnosing their own account. Write the output as a paid-consultant deliverable: direct, numbered, severity-tagged, actionable. Never "it could be better" · always "gap identified, impact estimated, fix specified."

Severity levels:
- **P0 · blocking** · Money being actively wasted, attribution broken, or account at risk of ban. Fix before anything else.
- **P1 · material** · Meaningful performance delta on the table. Fix within 1-2 weeks.
- **P2 · hygiene** · Best practice drift. Fix at quarterly review cadence.
- **P3 · optimization** · Incremental gain opportunity. Fix when runway allows.

Each checkpoint produces one finding entry. Zero finding on a checkpoint = pass (not worth mentioning in output unless section-level summary).

---

## Layer 1 · Tracking foundations

> Goal: verify that what the account spends on can be measured. Without this, every subsequent layer's performance data is meaningless.

### 1.1 · Pixel deployment coverage (P0)
**Mini-skill**: `check-pixel-deployment`
**What**: Browse the brand's 5 key pages (homepage, collection, PDP, cart, thank-you) and verify the pixel fires on each via Meta Pixel Helper or equivalent.
**Pass**: Pixel fires on all 5 pages with matching pixel ID.
**Fail severity**: P0 if pixel absent on thank-you page (no purchase tracking). P1 if absent on collection or PDP (prospecting remarketing degraded).

### 1.2 · Conversion API (CAPI) deployment (P0)
**Mini-skill**: `check-capi-deployment`
**What**: Events Manager → Overview → check if CAPI is sending events alongside pixel. Verify event quality score is ≥ 6/10.
**Pass**: CAPI active on at least purchase, add_to_cart, initiate_checkout with quality score ≥ 6/10.
**Fail severity**: P0 if only pixel (iOS 14.5+ attribution loss estimated 20-40% of events). P1 if CAPI active but quality score < 6/10.

### 1.3 · Event deduplication (P0 conditional)
**Mini-skill**: `check-event-deduplication`
**What**: If both pixel AND CAPI are active, verify each event uses a consistent `event_id` on both channels so Meta deduplicates.
**Pass**: `event_id` present and matching across both channels for all events.
**Fail severity**: P0 · without deduplication, purchases are double-counted in dashboards (false ROAS inflation).

### 1.4 · Advanced Matching (P1)
**Mini-skill**: `check-advanced-matching`
**What**: Events Manager → Settings → Advanced Matching · verify email, phone, first name, last name, city, zip are being hashed and sent.
**Pass**: At least email + phone hashed and active.
**Fail severity**: P1 · missing advanced matching reduces match rate by 10-30% on audiences.

### 1.5 · iOS 14.5 event priority (P0 for ecom)
**Mini-skill**: `check-ios14-event-priority`
**What**: Domain verified in BM. 8 prioritized events configured in Events Manager → Aggregated Event Measurement. Purchase = priority 1.
**Pass**: Domain verified, 8 events configured, purchase = 1.
**Fail severity**: P0 if not configured at all (iOS traffic won't attribute). P1 if configured but priority order is suboptimal.

### 1.6 · Attribution window setting (P1)
**Mini-skill**: `check-attribution-window`
**What**: Ad account → Settings → attribution = 7-day click / 1-day view (or 7-click + 1-view for ecom post-iOS).
**Pass**: 7-day click attribution active.
**Fail severity**: P1 · different windows bias ROAS comparisons. P2 if older window in use but consistent.

### 1.7 · Pixel sharing across ad accounts (if multi-brand operator) (P2)
**Mini-skill**: `check-pixel-shared-across-accounts`
**What**: If operator manages multiple brands from one BM, verify each brand's pixel is properly scoped to the right ad account (no accidental cross-brand firing).
**Pass**: Each brand's pixel scoped to its own ad account only.
**Fail severity**: P2 (data hygiene) · P0 if actively cross-firing.

---

## Layer 2 · Account hygiene

> Goal: verify the account is structurally healthy, permissioned correctly, and audit-trailed. This is where incidents happen (loss of access, unauthorized spend, ban risk).

### 2.1 · BM permissions inventory (P1)
**Mini-skill**: `check-bm-permissions`
**What**: Business Manager → Users · list all people with admin, advertiser, analyst access. Flag unknowns or ex-team members still with access.
**Pass**: Every listed user identified, roles match actual function, no orphan admin.
**Fail severity**: P1 · unaudited admin access is a security liability.

### 2.2 · 2FA enforcement on BM (P0)
**Mini-skill**: `check-bm-2fa-enforcement`
**What**: BM → Security Center → 2FA required for all users.
**Pass**: 2FA mandatory.
**Fail severity**: P0 · one compromised account = account suspended or stolen.

### 2.3 · Spend limit configured (P2)
**Mini-skill**: `check-spend-limit`
**What**: Ad account → Billing → daily/monthly spend cap exists.
**Pass**: Cap set to 120-150% of expected monthly spend.
**Fail severity**: P2 · without cap, a runaway ad can burn the budget. P1 if shared payment method with multiple accounts.

### 2.4 · Payment method redundancy (P2)
**Mini-skill**: `check-payment-method-redundancy`
**What**: Ad account → Billing → at least 2 valid payment methods, primary + backup.
**Pass**: 2 valid methods.
**Fail severity**: P2 · single-method = account pause if card expires.

### 2.5 · Account restrictions history (P1)
**Mini-skill**: `check-account-restrictions-history`
**What**: Account Quality → review any flags, warnings, disabled ads in last 90 days. Count disapprovals + patterns.
**Pass**: Zero restrictions or < 3 ad-level disapprovals.
**Fail severity**: P1 if repeated warnings (ban risk). P0 if currently under review.

### 2.6 · BM domain verification status (P1)
**Mini-skill**: `check-domain-verification`
**What**: BM → Brand Safety → Domain · primary domain verified with DNS record or meta tag.
**Pass**: Verified.
**Fail severity**: P1 · unverified domain blocks iOS 14.5 event configuration and certain ad formats.

---

## Layer 3 · Campaign structure

> Goal: verify spend is deployed in a structure that allows learning, scaling, and attribution separation. Structure drives performance ceiling.

### 3.1 · Naming convention compliance (P2)
**Mini-skill**: `check-naming-convention`
**What**: Sample 10 recent campaigns/ad sets/ads. Verify naming matches brand's declared convention (e.g., `[Objective] [Audience] [Creative] [Date]`).
**Pass**: ≥ 80% of names match convention.
**Fail severity**: P2 · inconsistent naming → impossible to filter/compare/report cleanly.

### 3.2 · Test budget isolation (P1)
**Mini-skill**: `check-test-vs-scale-budget-separation`
**What**: Identify campaigns labeled or structured as "testing" vs "scaling". Verify they are separate ad accounts OR separate campaigns with distinct labels.
**Pass**: Clear separation, distinct campaigns.
**Fail severity**: P1 · testing in scaling campaigns contaminates learning phase + inflates CPA.

### 3.3 · Learning phase exit rate (P1)
**Mini-skill**: `check-learning-phase-exit-rate`
**What**: Count ad sets exited learning phase in last 30 days vs total active. Should be > 70%.
**Pass**: ≥ 70% of ad sets exited learning.
**Fail severity**: P1 · stuck-in-learning ad sets consume budget without optimization. Often caused by insufficient budget per ad set (< 50 weekly events = can't exit).

### 3.4 · CBO vs ABO coherence (P2)
**Mini-skill**: `check-cbo-abo-strategy-coherence`
**What**: Count campaigns using CBO (Campaign Budget Optimization) vs ABO (ad-set level). Check coherence with declared strategy.
**Pass**: Consistent with strategy, no random mix.
**Fail severity**: P2 · mixed without intent dilutes budget allocation logic.

### 3.5 · Spend distribution balance (P1)
**Mini-skill**: `check-spend-distribution`
**What**: Compute % of spend on: prospecting / retargeting / lookalike / retention. Target typical healthy ratio ~70/20/10 for most e-com (adjustable per strategy).
**Pass**: Matches brand's declared strategy ±10%.
**Fail severity**: P1 if retargeting > 30% and account scaling (over-reliance on warm audiences). P2 if misaligned with strategy.

### 3.6 · Campaign objective alignment (P1)
**Mini-skill**: `check-campaign-objectives`
**What**: For each active campaign, verify objective matches intent. Sales objective for prospecting ecom, not engagement/traffic. Catalog sales for DPA.
**Pass**: All campaigns use appropriate objective.
**Fail severity**: P1 · wrong objective = wrong bid optimization = wasted spend.

### 3.7 · Active ads per ad set (P2)
**Mini-skill**: `check-active-ads-per-ad-set`
**What**: Sample ad sets. Verify 3-6 active ads each (Meta best practice for creative rotation + fatigue prevention).
**Pass**: Most ad sets have 3-6 active ads.
**Fail severity**: P2 · > 8 ads = budget spread too thin. < 2 = no fatigue rotation.

---

## Layer 4 · Audiences

> Goal: verify audience construction is technically correct, strategically diverse, and leveraging account data.

### 4.1 · Custom audience foundation (P1)
**Mini-skill**: `check-custom-audiences-foundation`
**What**: Verify these custom audiences exist and are active:
- Website visitors 30d, 90d, 180d
- Product viewers 30d, 90d
- Add-to-cart 30d, 90d
- Initiate checkout 30d
- Purchasers 30d, 90d, 180d, 365d
- Video viewers 25%/50%/75%/95% 30d (if video content)
- IG/FB engagers 365d (if organic content)
**Pass**: Full set exists and populating.
**Fail severity**: P1 · missing foundation audiences = no retargeting universe.

### 4.2 · Lookalike audiences · source quality (P1)
**Mini-skill**: `check-lookalike-sources`
**What**: List active LLAs. Verify each is built from a high-value source: LTV top 25% customers, high-AOV purchasers, repeat customers, loyalty members. NOT "all purchasers" and NOT "all website visitors".
**Pass**: All active LLAs built from value-based sources.
**Fail severity**: P1 · LLA from "all purchasers" = mediocre-value prospect pool.

### 4.3 · Lookalike percentage tiers (P2)
**Mini-skill**: `check-lookalike-tiers`
**What**: Verify multiple tiers exist (1%, 3%, 5%, 10%) for scaling ladder.
**Pass**: At least 1%, 3%, 10% tiers present for scaling.
**Fail severity**: P2 · single-tier LLA limits scale headroom.

### 4.4 · Audience exclusions (P0)
**Mini-skill**: `check-audience-exclusions`
**Tier**: binary
**Inputs required**: `brands/{slug}/brand.json#/platforms/meta/ad_account_id`
**What**: Sample prospecting ad sets. Verify existing customers (purchasers 180d) are EXCLUDED.
**Pass**: Prospecting audiences have purchaser exclusions.
**Fail severity**: P0 · without exclusion, account is paying to advertise to existing customers = inflated ROAS falsely, wasted reach.

**Reasoning layer** :
Without exclusion, the account is paying to re-reach existing customers from prospecting campaigns. Three consequences : (1) ROAS is falsely inflated because conversions from existing customers get re-captured and credited to the prospecting campaign, (2) real waste is 15-30% of prospecting spend on average ecom brands, (3) real CAC is masked, so scaling strategy decisions are built on broken numbers.

Edge case : if the brand has a very short repurchase cycle (monthly consumable) AND a declared reactivation strategy, some "existing customers" audiences may be INCLUDED intentionally. In that case, flag as intentional in the audit notes, not a fail.

Common root causes when this fails : hasty account setup, agency migration without audit, client self-served without coaching on audience exclusions.

Remediation : 5-10 minutes. Open each prospecting ad set, exclude "Purchasers 180 days" (or the relevant timeframe matching product repurchase cycle).

### 4.5 · Retention window coherence (P2)
**Mini-skill**: `check-retention-window-coherence`
**What**: Custom audience retention windows should match product repurchase cycle. Supplements (monthly) → 30-day retarget. Durables → 180-365 day.
**Pass**: Windows match declared product cycle.
**Fail severity**: P2 · mismatched windows waste retargeting spend.

### 4.6 · CAPI audience builds (P2)
**Mini-skill**: `check-capi-audience-builds`
**What**: Verify at least one custom audience is built from CAPI-only event source (Shopify Order Paid via CAPI), showing audience builds use CAPI data not just pixel.
**Pass**: CAPI-sourced audience exists.
**Fail severity**: P2 · losing CAPI-only events reduces audience size.

---

## Layer 5 · Creative strategy

> Goal: verify creative inventory is diverse enough to test and scale, with fatigue managed.

### 5.1 · Format mix (P1)
**Mini-skill**: `check-creative-format-mix`
**What**: Count active ads by format: video / static image / carousel / collection / DPA. Target: at least 3 formats active, with video > 40% of spend (ecom 2026 norm).
**Pass**: ≥ 3 formats, video ≥ 40% of spend.
**Fail severity**: P1 · single-format accounts cap their reach and learning.

### 5.2 · Aspect ratio coverage (P2)
**Mini-skill**: `check-aspect-ratio-coverage`
**What**: Verify active ads cover: 9:16 (Reels/Stories), 1:1 (feed), 4:5 (feed). All three needed for cross-placement delivery.
**Pass**: All three ratios present in active ads.
**Fail severity**: P2 · missing ratio = wasted placements.

### 5.3 · Creative fatigue markers (P1)
**Mini-skill**: `check-creative-fatigue`
**What**: For each active ad with > 7 days in flight: compute frequency, CTR delta vs first 3 days, CPM trend. Flag ads with frequency > 3, CTR dropped > 20%, or CPM climbed > 30%.
**Pass**: < 20% of active ads flagged.
**Fail severity**: P1 · fatigued ads degrade ROAS progressively.

### 5.4 · Angle / awareness diversity (P1)
**Mini-skill**: `check-angle-awareness-diversity`
**Tier**: contextual
**Inputs required**:
- `brands/{slug}/brand.json#/positioning`
- `brands/{slug}/brand.json#/tone_of_voice`
- `brands/{slug}/brand.json#/meta/vertical`
- `brands/{slug}/products/{slug}/spec.json#/identity`
- `brands/{slug}/audiences/{slug}/profile.json`

**Resource discovery** :
```yaml
keywords_template: "angle diversity awareness stages {vertical} {product_category} creative ecommerce"
source_types: [framework, guide, routing]
limit: 5
```

**What**: Decompose active ads into angle × awareness-stage matrix (requires ad_decompositions library or manual inspection of top 10). Verify coverage of at least 3 angles × 2 awareness stages.
**Pass**: ≥ 3 angles × ≥ 2 stages covered.
**Fail severity**: P1 · mono-angle account = ceiling hit fast.

**Reasoning layer** :
Meta's algorithm optimizes within the ad set it's given. If the account ships only one angle (e.g., only "pain-based" headlines), the algorithm scales that angle until it saturates the highest-intent slice of the audience, then ROAS collapses. Diversity unlocks new audience pockets · each angle resonates with a different psychographic segment.

The awareness axis matters independently : a product-aware audience responds to competitive positioning, while an unaware audience needs problem framing first. Mono-awareness = missing 60-80% of potentially convertible prospects.

What "enough diversity" means depends on the vertical · for supplements, proof-heavy angles dominate (social, scientific, testimonial) because trust gates the purchase ; for fashion, identity and aspirational angles dominate because the product itself IS the identity signal. The SOP doesn't hardcode this per vertical · the runtime resource discovery retrieves vertical-specific angle libraries if present.

Common failure modes : accounts built around one winning creative that never got re-angled ; creative team bias toward one voice ; absent creative strategy framework.

Remediation : identify the dominant angle, sketch 2-3 alternative angles grounded in brand positioning + audience profile (not generic), test each at budget parity ; iterate every 4-6 weeks.

### 5.5 · Hook diversity (P2)
**Mini-skill**: `check-hook-diversity`
**What**: Sample first 3 seconds of active video ads. Classify hook type (pattern interrupt / question / social proof / claim / problem statement). Flag if < 3 types in rotation.
**Pass**: ≥ 3 hook types in rotation.
**Fail severity**: P2 · same-hook fatigue compounds.

### 5.6 · Landing page coherence (P1)
**Mini-skill**: `check-landing-page-coherence`
**What**: For sample of 10 top-spend ads: verify ad promise matches landing page headline and visual within 5 seconds of load.
**Pass**: ≥ 80% coherent.
**Fail severity**: P1 · incoherent = bounce, wasted click spend.

### 5.7 · Dynamic Creative Optimization (DCO) usage (P3)
**Mini-skill**: `check-dco-usage`
**What**: Count DCO campaigns vs manually composed. DCO should be used for broad-prospecting tests.
**Pass**: Some DCO presence if brand is testing.
**Fail severity**: P3 · DCO is optional but underused on most accounts.

---

## Layer 6 · Compliance & quality

> Goal: verify ad content is policy-safe and account is not at risk.

### 6.1 · Ad disapproval history (P1)
**Mini-skill**: `check-ad-disapproval-history`
**What**: Count disapproved ads last 90 days. Categorize reasons (restricted claim, misleading, etc.).
**Pass**: < 5 disapprovals, no repeat pattern.
**Fail severity**: P1 if pattern (repeated similar violations = account quality score drop). P0 if currently under restriction.

### 6.2 · Restricted claim detection (P1)
**Mini-skill**: `check-restricted-claims`
**Tier**: contextual
**Inputs required**:
- `brands/{slug}/brand.json#/meta/vertical`
- `brands/{slug}/brand.json#/meta/market`
- `brands/{slug}/products/{slug}/spec.json#/identity/category`

**Resource discovery** :
```yaml
keywords_template: "restricted claims compliance {vertical} {market} Meta policy regulation"
source_types: [framework, convention, quality-spec]
limit: 5
```

**What**: Scan active ad copy for: health/weight-loss claims without disclaimer (supplements, beauty), income claims, before/after imagery, unsubstantiated superlatives ("#1", "best").
**Pass**: No obvious violations.
**Fail severity**: P1 for supplements/beauty especially · claim violations escalate to account warnings.

**Reasoning layer** :
Claim regulation varies sharply by vertical and market. Supplements in the EU (EFSA-regulated) cannot claim to treat, prevent, or cure any disease · a header like "Combat hair loss" on a supplement ad is a policy violation AND a regulatory risk simultaneously. Supplements in the US have more latitude (DSHEA) but Meta's own policy is stricter than FTC on health claims.

Beauty claims around "anti-aging", "erase wrinkles", "permanent results" trigger similar escalation. Weight loss ads have a dedicated Meta review track and before/after imagery is almost always disapproved regardless of disclaimer.

Cumulative effect : accounts with repeated claim violations accumulate a "quality score" penalty that slows ad delivery, raises CPMs, and escalates to account-level restrictions. Three months of unaddressed violations = measurable impact on account health.

The `discover-resources` call on this checkpoint should retrieve the brand's specific regulatory context if documented (e.g., `resources/frameworks/fr-supplements-efsa-claims.md` or `resources/conventions/meta-health-claims-policy.md`). If retrieved, the check is informed by actual claim lists ; if absent, the check falls back to general patterns (disclaimer presence, absolute superlatives, before/after).

Remediation : add disclaimers where claims are retained ; rephrase claims toward educational framing ("supports healthy hair growth" vs "regrows hair") ; remove or flag before/after imagery ; provide substantiation links for superlatives.

### 6.3 · Special ad category declaration (P0 for regulated)
**Mini-skill**: `check-special-ad-category`
**What**: Brand is in housing / credit / employment / social issues → Special Ad Category declared? For supplements/health, check if restricted targeting applies.
**Pass**: Declaration matches vertical.
**Fail severity**: P0 · wrong declaration = account ban potential.

### 6.4 · Age/geo targeting policy (P2)
**Mini-skill**: `check-targeting-policy`
**What**: Verify age/gender targeting respects product (e.g., no 13-17 for supplements). Geographic targeting excludes embargoed regions.
**Pass**: Policy-compliant.
**Fail severity**: P2 standard, P1 for regulated products.

---

## Layer 7 · Post-click & attribution integrity

> Goal: verify what Meta reports aligns with ground truth (Shopify orders, GA4). Discrepancies here invalidate every previous layer's performance read.

### 7.1 · UTM parameter coverage (P1)
**Mini-skill**: `check-utm-coverage`
**What**: Sample 10 top-spend ads. Verify URL parameters: `utm_source=facebook`, `utm_medium=paid_social` (or ad), `utm_campaign={campaign_id}`, `utm_content={ad_id}`, and ideally `utm_term` if relevant.
**Pass**: ≥ 80% of ads carry full UTM.
**Fail severity**: P1 · missing UTM = blind attribution in Shopify, GA4, CRM.

### 7.2 · GA4 conversion ingestion (P1)
**Mini-skill**: `check-ga4-conversion-ingestion`
**What**: GA4 → Conversions → verify Meta paid traffic conversions are firing with revenue values attached.
**Pass**: GA4 shows Meta-attributed conversions with revenue.
**Fail severity**: P1 · without GA4 ingestion, no cross-channel attribution possible.

### 7.3 · Shopify attribution matching (P1)
**Mini-skill**: `check-shopify-attribution-matching`
**What**: Compare Shopify's "paid social" or "meta" attribution for a random 30-day window vs Meta's reported conversions. Delta < 25% = acceptable (platforms differ by attribution model).
**Pass**: Delta < 25%.
**Fail severity**: P1 if delta > 40% (one side materially wrong). P0 if Meta reports 2× what Shopify shows (pixel double-firing suspect).

### 7.4 · Landing page speed (P2)
**Mini-skill**: `check-landing-page-speed`
**What**: Core Web Vitals on landing pages: LCP < 2.5s, FID < 100ms, CLS < 0.1. Mobile-first.
**Pass**: All three within threshold.
**Fail severity**: P2 · slow LP = conversion rate penalty (5-10% per extra second).

### 7.5 · Thank-you page pixel fire completeness (P0)
**Mini-skill**: `check-thank-you-pixel-completeness`
**What**: Ensure the Purchase pixel fires with: `content_ids[]`, `value`, `currency`, `content_type=product`. Without these, catalog attribution breaks.
**Pass**: All fields present on purchase event.
**Fail severity**: P0 if missing value/currency (purchases without revenue attribution). P1 if missing content_ids (DPA broken).

---

## Scenario variants

Different contexts consume this SOP differently. The orchestrator should accept a `--scenario` parameter:

### `new-client-discovery` (full scope)
Run all 7 layers, all checkpoints. Produce full audit. Used in week-1 onboarding.

### `pre-scaling-diagnostic` (focus layers 1-5)
Skip layer 6-7 if spend history < 30 days. Focus on structure + creative health before scaling budget.

### `post-incident-diagnostic` (focus layers 1-2 + 6)
Triggered after ROAS drop, restriction, or ban alert. Deep dive tracking + account health + compliance. Skip structure/creative if incident is compliance-related.

### `quarterly-review` (full scope with trend)
Same as full but adds delta vs last quarter's audit (requires prior audit artifact).

### `agency-switching` (full scope + access audit)
Add to layer 2: inventory of access handoff items (ownership transfer, historical access logs, tracking account migration).

---

## Output report template

The orchestrator that implements this SOP produces output in this structure:

```markdown
# Meta Global Audit · {brand_slug} · {YYYY-MM-DD}

## Executive Summary
- {P0 count} blocking issues requiring immediate fix
- {P1 count} material issues on the table
- Checklist pass rate: {X}/{Y} ({%}%)
- Estimated remediation effort: {low/medium/high · X hours}
- Top 3 findings: {bulleted}

## Findings by layer

### Layer 1 · Tracking foundations ({pass_rate})
| ID | Check | Status | Severity | Finding | Fix |
|---|---|---|---|---|---|
| 1.1 | Pixel deployment | ✓ pass | · | · | · |
| 1.2 | CAPI deployment | ⚠ fail | P0 | No CAPI active | Configure via Shopify/GTM. ~4h. |
| ... |

(repeat for layers 2-7)

## Prioritized action plan
### P0 · blocking (do first, this week)
1. {finding}: {fix specification}
2. ...

### P1 · material (within 2 weeks)
...

### P2 · hygiene (quarterly)
...

### P3 · optimization (when runway)
...

## Annex
- Raw check outputs (JSON structured)
- Links to source of truth (Meta reports, Shopify, etc.)
- Suggested next audits
```

---

## Cross-references

- **Parent orchestrator**: `.skills/skills/audit-meta-global/SKILL.md` (to be created) · reads this SOP and executes
- **Mini-skills referenced**: 40+ (see each checkpoint). Many don't exist yet · orchestrator falls back to manual check + operator input where mini-skill missing.
- **Schema**: `resources/schemas/sop.schema.json` · this file follows the SOP meta-schema.
- **Related docs**: `docs/system/skill-architecture-redteam.md` (architectural context), `docs/system/skill-builder-cartography.md` (when to extend schema for new checkpoints).
- **Related SOPs (future)**: `sop-audit-shopify-global`, `sop-audit-tracking-global`, `sop-audit-portfolio-global` (orchestrator above single-brand).

---

## Maintenance

This SOP is reviewed:
- At each major Meta platform update (iOS event changes, attribution model shifts)
- Every 6 months minimum
- On operator feedback (a checkpoint missed something, a new pattern emerged)

Updates are versioned. Never delete a checkpoint · mark as `deprecated: true` with date, keep traceable.
