# Paid Angle Scoring Framework

> Codified scoring logic applied by `produce-paid-angles` to every cell of the cartesian product (audience × awareness × emotion × objection × placement) generated internally before ranking. Consumed, not improvised. The skill quotes this file as the binding reference for what each lens means, how lenses aggregate, what filters drop a cell entirely, and how to anchor the final hook in real customer voice. If a scoring decision cannot be backed by the rules below, the cell does not propagate to the operator-facing artifact.

This framework defines five lenses (verbatim density, emotional resonance, objection neutralization strength, placement viability, awareness-acquisition alignment), the aggregation formula that compresses them into a single internal rank, the cluster filter that prevents the operator from receiving three angles saying the same thing, the verbatim anchor selection rule that decides which customer phrase becomes the hook, the anti-patterns that corrupt the output, and the calibration policy for tuning weights as the skill matures. The downstream value of `produce-paid-angles` is bounded by the quality of this scoring. Under-quality here ships templated angles, fabricated verbatims, and the operator detects within one or two runs.

---

## 1. Scoring lenses

Five lenses apply to every cell. Four contribute weighted scores, one acts as a hard filter. Total weighted contribution sums to 100% across the four scoring lenses; the filter sits outside the sum and forces the cell to zero when it fails.

### Verbatim density (HIGH weight, 35%)

The single most important lens. A cell that maps to actual encoded verbatims scores high and earns the right to ship under customer voice. A cell inferred from structured tags alone · pain typology, objection type, emotion driver · scores low and either flags as "inferred, no customer voice support" in the internal trace or drops entirely if the cluster contains a verbatim-grounded sibling.

The signal sources are three. `audience.profile.json#voice.key_expressions[]` carries the verbatim phrases coded by `mine-voc` with `frequency`, `sample_size`, `platform`. `audience.profile.json#pain_points[].verbatim_quotes[]` carries the longer-form quotes attached to each pain. `audience.profile.json#objections[].formulation` carries the verbatim form of each objection when one was captured.

| Test | Score |
|---|---|
| Cell pain phrase exact match in `voice.key_expressions[]` | +3 |
| Cell pain phrase semantic match in `pain_points[].verbatim_quotes[]` | +2 |
| Cell objection exact match in `objections[].formulation` | +3 |
| Cell objection theme present but phrasing inferred | +1 |
| No verbatim support on either pain or objection axis | 0 (and flag) |

A cell scoring 0 on this lens is a candidate for drop. The cluster filter at § 3 makes the final call: if a sibling cell in the same cluster scores 4+ on verbatim density, the unanchored cell is dropped; if no sibling has anchor and the cell is the only carrier of a structurally important objection, it ships with the inferred flag.

### Emotional resonance (MEDIUM weight, 20%)

Does the cell's emotion match the audience's emotional dominant. A skincare audience whose JTBD emotional driver clusters around shame, hiding, post-mirror anxiety responds to angles that activate culpabilité, identitaire, soulagement · not to angles that activate fierté or accomplissement. A supplement audience whose emotional dominant is daily fatigue and frustration with stimulants responds to délivrance and épuisement; aspirational pride angles miss.

Sources: `audience.profile.json#psychology.jtbd.emotional_driver`, `audience.profile.json#pain_points[].emotion`, and the derived emotional dominant computed by clustering the top three pain emotions weighted by `pain_points[].frequency`. The cell's own emotion (assigned at cartesian generation from the activated `pain.emotion` dimension) is compared against that dominant; a tight semantic match scores 5, an adjacent emotion in the same family scores 3, an emotion from a different family scores 1, an emotion that contradicts the dominant scores 0.

### Objection neutralization strength (MEDIUM weight, 20%)

The cell pairs an objection with a proof type drawn from `product.spec.json#proofs.*` that actually answers it. Strength is the directness of that mapping, read against `resources/registries/proof-registry.md`. *"Trop cher pour 1-3 kg"* is a price-perception objection neutralized cleanly by `cost-calculator` (force forte) backed by `clinical-trial` (force maximale) · a single testimonial alone does not close it. *"J'ai déjà tout essayé"* is a scepticism objection neutralized by `clinical-trial` or `customer-review` carrying transformation narrative, not by `risk-reversal`. *"C'est juste du marketing"* is a trust objection neutralized by `press-quote` or `claim-science`, not by `social-proof-number`.

Sources: `audience.profile.json#objections[].refutation_anchor`, `product.spec.json#proofs.{social,authority,performance,scientific}`, `product.spec.json#benefits[].chain[]`. The lens scores 5 when the cell objection has a directly mapped proof type present in the spec at force ≥ forte, 3 when the mapping exists but at force moyenne, 1 when only a weak proof anchor exists, 0 when no proof in spec maps to the objection. A 0 here is a hard signal that the angle ships toothless · the cluster filter usually drops it in favor of an objection the brand can actually defuse.

### Placement viability (FILTER, not weight)

The cell hook works inside the placement format constraints. Hook over 8 words won't survive Reels first-frame attention test. Hook depending on text overlay won't work in TikTok organic where vernacular voiceover dominates. Hook with abstract emotional framing fails Stories where swipe-up curiosity needs a concrete loop. This is a hard filter, not a weighted contribution. Cell drops if hook breaks placement; cell passes neutral if hook fits.

Sources: hook length × placement format, format-specific constraints from `resources/conventions/{platform}.json` when available, falling back to the four-placement default rules · Reels: 3-second pattern interrupt, hook ≤ 8 words; Stories: swipe-up curiosity, hook ≤ 12 words; Feed UGC: identification-first, hook ≤ 15 words; TikTok: native vernacular, hook in customer language with no marketing register. Filter result is binary: `pass` or `fail`. A `fail` zeroes the cell regardless of its scores on the four weighted lenses.

### Awareness-acquisition alignment (CONTEXTUAL weight, 25%)

The cell's awareness stage matches the brand's strategic acquisition focus. A brand acquiring cold audiences along the problem-aware → solution-aware path needs counter-intuitive, transformation, emotional-identity angles; a brand retargeting most-aware purchasers needs urgency, scarcity, barrier-removal angles. Producing a scarcity angle for a problem-aware cold audience converts at zero. The lens cross-references `resources/routing/awareness-angle-matrix.md` and zeroes any cell whose angle sits in the "avoid" column for the dominant awareness.

Sources: `audience.profile.json#market_position.awareness_distribution`, `brand.json#strategy.acquisition_focus` if encoded, `strategy.json#current_focus` for the active priority. The lens scores 5 when the cell's awareness stage matches the brand's stated acquisition focus and the angle sits in the "primary" column of the awareness-angle matrix, 3 when it matches with the angle in "secondary", 1 when there's a partial match with no direct routing signal, 0 when the angle is in "avoid" for the dominant awareness. The 0 here cascades to a drop unless the operator forces an override at trigger time.

When `strategy.json#current_focus` is empty and no acquisition signal can be inferred, the lens drops out of the formula entirely and its 25% weight redistributes to verbatim density (which becomes 60%). Awareness without strategic anchor is guesswork; the framework refuses to weight guesswork.

---

## 2. Aggregation formula

Total internal score is a weighted sum, normalized 0-100, never exposed to the operator.

```
total = (verbatim × 0.35) + (emotion × 0.20) + (objection × 0.20) + (awareness × 0.25)
   if placement viability fails → cell dropped, score 0
   if strategy.current_focus empty → awareness lens drops, verbatim weight rises to 0.60
```

Each lens contributes a 0-5 raw score per § 1; the formula multiplies by weight and rescales to 0-100 for ranking comparability. A cell scoring above 70 is high-density; the skill may push the output cap from 5 to 7 angles when at least three top cells clear that threshold and the operator stated a wide-test objective. A cell scoring below 30 is rarely shipped and never as a top-three slot.

The score lives in `brands/{slug}/sources/produced-angles/{date}/scoring-trace.jsonl` for audit. The operator never sees the number. Saying *"angle 1 ranks first because it scores 87/100"* is plumbing leak; the synthesis paragraph at Step 8 of the skill expresses rank in plain prose · *"l'angle miroir sort en premier parce que tes verbatims Trustpilot le portent et que ton clinical trial neutralise frontalement le scepticisme"*.

---

## 3. Cluster filter

After scoring, before ranking, cluster similar cells and keep only the highest-scored representative per cluster. Two cells are similar when they share dominant pain (theme + emotion), dominant objection, and placement. A skincare cluster might collect three cells around the post-pregnancy mirror pain, the *"j'ai déjà tout essayé"* objection, and Reels · only the highest-scored survives, the rest drop. A supplement cluster might collect two cells around the chronic fatigue pain, the *"trop cher pour ce que c'est"* objection, and Stories · same rule.

The filter prevents the operator from receiving three angles that read as paraphrases of each other. The signal that the filter failed is unambiguous: the operator scans the table and says *"those are basically the same"*. That perception breaks trust and reads as template; the cluster filter exists to make it impossible.

When a cluster contains one verbatim-grounded cell and one inferred cell with marginally higher emotion or awareness scores, the verbatim-grounded cell wins. Verbatim grounding is the structural priority of the framework; tiebreakers go to it.

---

## 4. Verbatim anchor selection

For each ranked cell, the hook is anchored on a verbatim. Selection follows a strict order, no skipping.

1. Prefer exact verbatim match from `audience.profile.json#voice.key_expressions[]` with `sample_size ≥ 5`. The denominator matters · a verbatim cited by 5 of 30 reviews is a pattern; a verbatim cited by 5 of 5 is a coincidence. The schema enforces the denominator per `voc-coding.md`; the anchor selection enforces the threshold.
2. If no exact match clears the threshold, prefer a verbatim with high emotional weight from `pain_points[].verbatim_quotes[]`, where emotional weight derives from pairing the quote's coded emotion with the cell's target emotion.
3. If no verbatim is available on either path, fall back to a hook formula from `resources/templates/hook-formulas.md` matched to the cell's awareness range, and tag the internal trace with `(formulation type, no direct customer voice)` so the operator-facing artifact carries the *"à valider, pas de verbatim direct"* inline flag.
4. Never invent a quote and present it as customer voice. Never paraphrase a verbatim and present the paraphrase as the original. The fabrication of a single quote breaks operator trust irrecoverably and contaminates every downstream brief.

The rule is asymmetric on purpose. A real verbatim with weak emotional fit beats a perfect inferred phrasing every time, because the former is reproducible against the corpus and the latter is the agent's invention.

---

## 5. Anti-patterns

Six failure modes recur in scoring drafts. Each is caught by a binary test.

**Score exposed as a number.** The operator sees ranked angles, a synthesis paragraph, a five-column table. The operator never sees *"score 73/100"*, never sees the lens names, never sees the formula. The numbers stay in `scoring-trace.jsonl`. Test before shipping any operator-facing line: would an e-commerce manager ever say this sentence? If the sentence contains a digit referring to a lens score, rewrite.

**Cells generated past 4-5 active dimensions.** A cartesian of 5 × 5 × 4 × 4 = 400 cells dilutes signal across dimensions and produces a long ranked tail of marginal scores. The cap on active dimensions belongs at the activation step (Step 3 of the skill), not at scoring · the framework assumes the cap was respected. If scoring is running on a 200+ cell cartesian, the activation logic upstream is broken; the framework's quality contract does not survive that load.

**Verbatim anchor invented or paraphrased.** Banned. Either real verbatim from the corpus, or hook formula from the library with the explicit *"(formulation type)"* flag. The asymmetric preference for real-but-weak over invented-but-perfect is not a soft suggestion; it is the structural condition that lets the skill ship without fabricating customer voice.

**Cluster filter skipped.** Output contains three or four cells saying the same thing in marginally different language · operator perceives template, the skill loses credibility for the brand. The filter at § 3 is non-optional; if the agent cannot articulate why two cells with shared pain + objection + placement both shipped, one of them should not have.

**Awareness lens applied without strategy signal.** When `strategy.json#current_focus` is empty and no acquisition signal can be inferred from operator turns, the awareness lens drops and its weight cascades to verbatim density. Applying the lens against a guessed acquisition focus produces a ranking that looks rigorous but is actually noise. The framework prefers fewer lenses honestly applied to more lenses guessed.

**Bias toward most-aware angles.** Most-aware angles often pair best with the brand's existing proof stack · the brand has the cost-calculator, the risk-reversal, the urgency mechanic on hand, so cells targeting most-aware audiences score high on objection neutralization. Resist this bias when the brand's strategic acquisition focus is cold. Cold acquisition needs problem-aware and solution-aware angles even when the proof mapping is weaker; the awareness lens enforces this and the framework trusts it. A skill that ranks five most-aware angles for a brand acquiring cold has scored correctly and routed wrongly.

---

## 6. Output schema integration

The scores flow into two surfaces, strict separation per the snapshot/mine-voc precedent.

Layer A captures the audit substrate at `brands/{slug}/sources/produced-angles/{YYYY-MM-DD}/scoring-trace.jsonl`, one line per cell scored, full breakdown per lens, verbatim IDs referenced, rank position. Queryable post-hoc when the operator asks *"pourquoi cet angle ranke premier"* or when an audit needs to verify no verbatim was fabricated. The trace is never auto-loaded into context.

Layer B captures the operator-facing artifact at `brands/{slug}/produced/paid-angles/{YYYY-MM-DD}-{audience-slug}.md`, ranked top 3-5 (or up to 7 when high-density justifies), five-column table, synthesis paragraph above, citations footer linking back to Layer A. The artifact carries no scores, no dimension names, no lens vocabulary · pure operator-language. The full schema for both layers lives in `01-produce-paid-angles.md § 6`; this framework references it without restating.

---

## 7. Calibration over time

The skill ships at v1.0 with the weights specified in § 2: verbatim 0.35, emotion 0.20, objection 0.20, awareness 0.25. The weights are an opinionated default, not a measured optimum. After roughly five production runs across diverse brands (one DTC supplement, one skincare, one fashion, two adjacent verticals), the operator or maintainer can tune weights based on observed angle-test performance · which angles converted, which dropped, which the operator over-ruled at brief stage.

Calibration captures as entries in `learnings.json` with the field `framework: paid-angle-scoring, version: 1.0 → 1.1`, an explicit weight diff (*"verbatim 0.35 → 0.40, awareness 0.25 → 0.20"*), and the run IDs that justified the change. Framework versioning increments at this doc's header on every weight change. A v1.1 framework with logged justification beats a v1.0 framework that drifted in unlogged head-canon.

The lenses themselves · what they measure, what scores they produce · do not calibrate. Adding or removing a lens is a structural change that requires a new framework version and an explicit migration note in `learnings.json`. Lens removal in particular is high-cost: every Layer A trace produced before the change references the removed lens by name and becomes harder to audit retroactively.

---

## References

- `01-produce-paid-angles.md` · the consumer of this framework. Cites this file as binding for every scoring decision.
- `docs/system/contextual-intelligence.md` · master doctrine. The trust-the-model and no-plumbing-leak rules govern operator-facing output above.
- `docs/system/voice.md` · voice canon. Synthesis derived from ranked output follows it strictly.
- `resources/registries/angle-registry.md` · 14 angle types referenced by the awareness alignment lens.
- `resources/registries/proof-registry.md` · proof typology referenced by the objection neutralization lens.
- `resources/routing/awareness-angle-matrix.md` · awareness × angle routing referenced by the awareness alignment lens.
- `resources/quality-specs/hook-quality-spec.md` · hook validation applied after anchor selection.
- `resources/frameworks/voc-coding.md` · sister framework, defines the verbatim coding that feeds the verbatim density lens.

---

*v1.0 · initial framework. Weights opinionated default, recalibration after 5 production runs.*
