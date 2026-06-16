# VoM Mining · Analytical Framework

> Codified analytical lenses for coding market-level signal during `mine-vom` execution. Cited by `.skills/skills/mine-vom/SKILL.md`. Read before any market crawl that intends to write to `brand.json#market.*` or `audiences/*/profile.json#voice.market_vernacular[]`.

This framework defines four lenses the agent applies to broader-niche discourse: vernacular, sophistication stage, white space, and a selective read of Porter. The lenses are ordered. The output is synthesis the operator could not have reached alone, not a competitor benchmark. Per `docs/system/contextual-intelligence.md`, the test at every step is whether the lens serves the operator's next decision · not whether `market.*` ends the run with more filled fields.

## Section 1 · Vernacular extraction

Vernacular is the vocabulary the niche uses for itself when no marketer is listening. It is the highest-leverage output of the skill because the words cannot be invented and they directly raise creative quality on the brand's next ad, page, or email.

The detection grid is ruthless about source. Vernacular is what *customers and community members* type, not what brand marketers print on packaging. *Kibble* is vernacular in dog food; *dry food* is the marketer translation. *Stack* is vernacular in supplements; *supplement combo* is the listicle paraphrase. *Leave-in* is vernacular in haircare; *no-rinse conditioner* is the SEO title. *Slugging* is vernacular in skincare; *occlusive overnight treatment* is the brand reformulation. *Recomp* and *cut* are vernacular in fitness; *body recomposition phase* is the influencer voiceover.

A token earns vernacular status when it survives three binary tests at once.

First, **recurrence across at least three independent sources of different types** · one forum thread, one review surface, one influencer comment thread, for instance. Same word, three places, three contexts. A term repeated five times inside a single Reddit thread is one source, not five · the test is independence, not volume.

Second, **used without explanation**. Insiders do not gloss insider shorthand. If the most upvoted Reddit thread says *"slugged with Vaseline last night"* and nobody in the comments asks what slugged means, the term is in-niche canon. If the same thread reads *"slugging (which is when you put Vaseline on top of your routine)"*, the term is in transit and not yet canon · note it, do not promote it.

Third, **the translation test**. If a beginner reading the term cold would have to look it up, it is vernacular. If the term reads as plain English to a stranger, it is not vernacular · it is just a noun. *Hydration* fails the test ; *barrier-repair phase* passes.

| Niche | Vernacular | Marketer paraphrase to avoid |
|---|---|---|
| Skincare | slugging, INCI, dupes, purge, retin-uglies, barrier-repair | overnight occlusive, ingredient list, alternatives, breakout phase |
| Supplements | stack, intra, recomp, mini-cut, gainz, blood panel | supplement combo, intra-workout drink, body composition |
| Fitness | shred, AMRAP, deload, PR, hypertrophy block | cutting phase, max reps, recovery week, personal record |
| Pet (dog) | kibble, raw, BARF, freeze-dried, chonk | dry food, raw diet, overweight |
| Fashion | fit pic, drip, cop, OOTD, dad-fit, gorpcore | outfit photo, style, purchase, casual look |

Anti-patterns to police mid-extraction. The agent rejects any token that surfaces only on brand-controlled surfaces · the brand's own product copy, the brand's own homepage, paid ads, brand SEO titles. Those are circular evidence. The agent rejects any token a copywriter could have invented in five minutes. *Glow* is not vernacular. *Hydration* is not vernacular. *Wellness* is not vernacular. The token has to feel slightly off-brand if it were spoken on stage.

Vernacular is also coded with a frequency tag the operator does not see · *dominant* (recurs in 8+ sources), *common* (3-7 sources), *emerging* (3 sources, all from the last 60 days). The frequency tag drives downstream copy guidance: dominant tokens are safe defaults, emerging tokens are leading indicators worth testing, common tokens fill the middle. Operator-facing language stays plain · *"the niche uses 'slugging' constantly, this is now table stakes vocabulary"* rather than a frequency label.

Output route: `audiences/{slug}/profile.json#voice.market_vernacular[]` with a verbatim source citation per token. Per the operator-language rule, the operator sees the token and one example sentence, never the variable name or the source-confidence tag.

## Section 2 · Sophistication signal detection

Sophistication is read on the niche, not on the audience. Eugene Schwartz's five-stage ladder describes how a *category's* claim language hardens over time as competition and reader fatigue accumulate. The agent codes the niche's current stage from the messaging shape of its top players, the vocabulary of reviewers, the framing of listicles, and the angle expert journalists take.

Stage 1 is the rare niche where one player names the benefit directly and the claim is enough. Stage 2 is when competitors arrive and every claim doubles in volume · *fastest, strongest, most effective*. Stage 3 is when claim escalation stops working and players start naming the mechanism · *contains 2% retinaldehyde, the form your skin metabolizes faster*. Stage 4 is when mechanism is table stakes and players differentiate on a *better* mechanism · *encapsulated retinaldehyde with a micellar carrier, three times the bioavailability*. Stage 5 is when mechanism arms race exhausts and claims migrate to identity, belonging, values · the player wins because *they are the brand of women who already know which retinoid actually works*.

Detection moves bottom-up from market signal, never top-down from operator framing. Look at the top three players' hero copy. If hero copy names the benefit only, stage 1-2. If hero copy names a specific mechanism, stage 3. If hero copy names a *better* mechanism with a comparative claim, stage 4. If hero copy names a tribe or a stance and assumes mechanism is understood, stage 5. Cross-check with reviewer vocabulary · reviewers at stage 4 talk about ingredients, percentages, formulation choices ; reviewers at stage 5 talk about *what kind of person uses this brand*. Cross-check with editorial · Wirecutter at stage 4 compares specifications ; The Strategist at stage 5 profiles the user.

| Niche | Reading | Stage |
|---|---|---|
| Clean beauty FR 2026 | Top players (Caudalie, Typology) shifted hero from naturalité to actifs prouvés over 18 months ; reviewers debate *INCI courte* vs *actifs validés* ; "clean" used ironically in 30% of recent forum threads | 4 → 5 in transit |
| Mass-market protein powder US | Hero copy still claims *25g protein per scoop, fastest absorbing* ; reviews compare grams and price | 2-3 |
| Niche supplements (longevity stack) | Hero copy names rapamycin analog, NAD+ precursor mechanism, dosing protocol ; reviewers cite Examine.com studies | 4 |
| Streetwear (gorpcore) | Top players assume the wearer already knows what gorpcore is ; copy names neighborhoods, music, rituals | 5 |
| Mass dog kibble | Hero copy claims *complete and balanced, vet recommended* ; reviews compare price and bag size | 2 |

Progression over 12-24 months is observable. A niche moves up the ladder when the dominant player's claim shape changes and the rest follow within 6-12 months. The agent flags transit zones explicitly · *"the niche is at stage 4 on incumbent copy but reviewer language has crossed into stage 5"* is a load-bearing finding because it tells the operator where the puck is going. The clean-beauty FR transit between 2024 and 2026 is a worked example: in 2024, every player led with *naturalité* and *propre* (stage 4 mechanism-as-claim) ; by late 2025, the leaders had pivoted to *actifs prouvés / validé par derma* and reviewers had started using *clean* ironically · a stage 5 identity claim was forming around scientifically literate consumers, and the brands still leading on naturalité were now reading dated.

Three binary tests for stage placement before the agent commits. Does hero copy on the top three players name a benefit only, or a mechanism, or a better mechanism, or an identity ? Do reviewers in the top 20 most-upvoted threads of the last 90 days argue about specs, or about what kind of person uses the brand ? Does editorial coverage compare products on parallel grids (stage 3-4) or profile users (stage 5) ? Two of three signals at the same altitude grounds the call. Mixed signals across two adjacent stages mean transit ; flag it.

Most mature DTC niches sit at stage 4. Stage 5 is overclaimed by operators who confuse a vibey brand with a sophisticated one. Default skepticism: when in doubt between 4 and 5, write 4. Stage 5 requires that mechanism is so saturated and so understood across the niche that naming it again would bore the reader · a high bar most operators have not actually cleared.

Output route: `brand.json#market.market_overview.sophistication_stage` as a single integer with a short prose justification citing the three signals that grounded the call.

## Section 3 · White-space identification

A white space is a recurring need expressed in market verbatims that no current player addresses frontally as hero positioning. It is not a competitive gap. A competitive gap is *someone does this badly* · a wedge for a better operator. A white space is *no one names this at all* · the words exist in market discourse but have not yet been claimed by a brand on its homepage, in its hero copy, or as the spine of its category page.

The detection rule is three-part and conjunctive. The need must recur across three or more independent sources. The need must not map to any current top-player claim · the agent reads the top three to five competitors' positioning lines and confirms the need has no equivalent. And the need must be more than an unbranded category mention · *people talk about hydration* is not a white space, *people talk about hydration after retinol cycles and no clean brand owns it* is.

Examples that survive the filter. *Clean beauty for post-rétinol skin* · recurring in r/SkincareAddiction and r/SkincareAddictionFR over the last 12 months, no current French clean-beauty player has it as hero positioning, and the phrasing is specific enough to belong on a landing page. *Three-product minimalist routine* · recurring in 12+ Reddit threads as a stated preference, no incumbent owns the bundle as hero, the operator could ship it next quarter. *Transparent on the synthetic compromises* · recurring as ironic counter-discourse against clean-beauty marketing, no player has admitted it on-brand, and credibility upside is high. *Supplements for women in perimenopause who lift* · recurring in r/xxfitness, no top supplement brand positions there frontally.

Examples that fail. *People want clean beauty* · too generic, every clean-beauty brand already claims it. *People wish products were cheaper* · universal noise, not white space. *People hate fragrance* · partially addressed by fragrance-free lines from incumbents, not white. *People want results* · empty claim, table stakes everywhere. *People want sustainability* · table stakes since 2020, claimed by every player even when not delivered.

Three binary tests before promoting a candidate to white-space. Has the need been verbalized in the niche's own vernacular by at least three independent sources in the last 12 months ? Have the top three to five competitors been read on their hero positioning, category pages, and homepage tagline · and does none of them carry the claim ? Is the phrasing concrete enough that the operator could, in principle, ship a landing page next week with that claim as the H1 ? All three yes · promote. Any one no · hold as a flagged hypothesis, not a write.

The agent runs the white-space pass last among the three signal lenses, after vernacular and sophistication, because both feed it. Vernacular gives the language the white space must be expressed in (the operator will own it in the niche's words, not in marketer English). Sophistication tells the agent at what altitude the claim must sit · at stage 5, a white space is an identity claim ; at stage 3-4, a white space is a mechanism claim. A white space pitched at the wrong sophistication stage looks tone-deaf.

Output route: `brand.json#market.external_intelligence[]` as 3-5 entries per run, each tagged `white_space_gap: true`, each citing the verbatims that grounded the recurrence count. Cap is firm · more than five and the operator's attention disperses.

## Section 4 · Selective Porter

Porter's Five Forces is treated as a diagnostic menu, not a template. The agent picks the one or two forces that are *active* in the niche right now and matter for the operator's positioning. Applying all five is form-fill · it produces a dossier that reads thorough and decides nothing.

The forces, with the activation signal that should pull each into the analysis and the signal that should keep it out.

**Rivalry intensity** matters when the niche shows fragmentation with no dominant player above 20% mind-share, or when consolidation is visibly compressing margins (three players left, all running the same offer cadence). It does not matter when the niche has a clear leader nobody is chasing or when the operator's positioning is far enough off-axis that direct rivalry is hypothetical.

**Threat of new entrants** matters when the agent sees barrier-to-entry visibly low · Shopify-templated competitors appearing every quarter, ingredient sourcing trivial, no regulatory moat. It signals incoming saturation and a closing window. It does not matter when supply chain is gated (clinical-grade actives, exclusive distributor contracts) or when brand equity in the niche compounds heavily (heritage skincare).

**Buyer power** matters when the category has commoditized · buyers compare on price, switch costs are zero, and search intent is dominated by *cheapest X* queries. It does not matter when the niche carries a premium and buyers self-segment on identity rather than spec.

**Supplier power** matters when one ingredient or component is rare and a small number of suppliers gate the category · pharmaceutical-grade peptides, specific fabric mills, single-source botanicals with seasonal yield. The operator's COGS and lead times are exposed. It does not matter when inputs are fungible and any contract manufacturer can deliver.

**Substitute threat** matters when an adjacent category is visibly absorbing the use case · GLP-1 prescriptions partially replacing weight-management supplements, AI workout apps replacing 1:1 coaching, secondhand resale replacing fast fashion. The substitute does not need to be in the niche; it needs to be in the buyer's consideration set. It does not matter when the use case is bound to the category by physical or regulatory constraint.

| Niche | Active force | Why |
|---|---|---|
| Clean beauty FR | Rivalry + new entrants | 30+ Shopify clean brands launched 2024-2025, fragmentation acute, no moat |
| Longevity supplements | Supplier power | Rapamycin analogs, NAD precursors single-sourced and price-volatile |
| Weight management supplements | Substitute threat | GLP-1 prescriptions reframing the entire use case |
| Streetwear gorpcore | None active right now | Stage-5 identity niche, classic Porter forces structurally muted, skip the framework |
| Pet kibble (mass) | Buyer power | Commoditized, price-led, switch cost zero |

Three binary tests before invoking any force. Is there a market signal in the verbatim corpus that *names* this force's dynamic · buyers complaining about price commoditization for buyer power, reviewers naming ingredient scarcity for supplier power, listicles framing the category as crowded for rivalry, search queries spiking on adjacent solutions for substitutes ? Does naming the force change a positioning recommendation the operator is about to make ? Would a senior strategist looking at this niche over the operator's shoulder mention this force unprompted ? Two of three yes · invoke. One or zero · skip and move on.

Hard rule: the agent never runs the framework as a five-section template. It names the one or two active forces, justifies the call in two sentences each, and skips the rest in a single line · *"rivalry, new entrants, buyer power and substitute threat all read structurally muted in this niche right now ; not a useful frame here"*. If no force activates, the agent says so and drops Porter from the run entirely. Per `docs/system/contextual-intelligence.md § Anti-patterns / Form-fill agent`, applying all five for symmetry is the failure mode to police. The synthesis is stronger for one well-named force than for five paragraphs of rote analysis.

## Section 5 · Mining workflow

The four lenses are applied in order. The order is load-bearing because each lens conditions the next.

1. **Define the niche precisely.** Sector plus sub-vertical plus geography, pulled from `brand.json#identity` and `brand.json#meta`. *Skincare* is not a niche ; *clean beauty for women 30-50 in France* is. Without precision, every later lens dilutes.
2. **Vernacular first.** Build the niche vocabulary baseline before any other coding. Subsequent lenses will be expressed in the niche's words, not in marketer English. Skipping this step contaminates sophistication and white-space readings with off-niche language.
3. **Sophistication second.** Place the niche on the Schwartz ladder before looking for white space. The altitude of the white-space claim depends on the stage. A stage-3 white space is a mechanism nobody has named ; a stage-5 white space is an identity nobody has claimed.
4. **White space third.** Cross-reference recurring market needs against current top-player claim coverage, expressed in the vernacular surfaced in step 2 and pitched at the altitude surfaced in step 3.
5. **Porter last and selective.** Only when one or two forces are visibly active. The check is fast · name the force, ground it in two sentences of market signal, or skip Porter entirely for the run.

The agent does not run all four lenses for completeness. It runs the lenses that have signal and skips the ones that do not. A clean run that names vernacular, sophistication, and three white spaces, and explicitly drops Porter, is a complete run. A run that names all four lenses but where Porter reads as form-fill is an incomplete run dressed up as thorough · worse than the partial honest one.

Order also matters because of what the operator sees at synthesis close. The synthesis paragraph leads with the most load-bearing finding, not the most procedural one. In practice, that is usually the sophistication transit (if the niche is moving) or the white space (if the niche is stable but unclaimed) · rarely vernacular, almost never Porter. The lenses run in the codified order ; the synthesis paragraph reorders them by stake.

## Section 6 · Anti-patterns

Six failure modes recur in mine-vom output. Each is caught by a binary test before the synthesis paragraph ships.

**Porter as five-section template.** Form-fill, exactly the anti-pattern `contextual-intelligence.md` names. Test: did the agent run all five forces ? If yes, rewrite to one or two active forces and a one-line skip on the rest.

**Vernacular extracted from marketers.** Tokens pulled from competitor packaging, competitor SEO titles, or industry press releases. Circular, low-leverage, often wrong. Test: for each vernacular token, name the customer-side source (forum thread, review verbatim, influencer reply). If the source is brand-controlled, drop the token.

**Competitive gap dressed as white space.** *Brand X does this badly* is a wedge, not a white space. White space requires absence of the claim across all top players, not weakness of the claim by one. Test: can the operator name three competitors who address the need at all ? If yes, it is a competitive gap, not a white space.

**Over-staging sophistication.** Most mature DTC niches sit at stage 4. Stage 5 is rare and operator-framing-prone · operators want to believe they sell to a tribe. Test: name three signals of identity-over-mechanism in market discourse before writing stage 5. If two or fewer, write stage 4.

**One-source generalization.** A theme found in a single source is signal, not pattern. Every claim that lands in the synthesis must carry two or three independent confirmations. Test: for each load-bearing claim in the synthesis paragraph, name three sources of different types. If you cannot, downgrade the claim to a flagged hypothesis.

**Synthesis as competitor inventory.** The skill exists for the synthesis paragraph, not the per-competitor blurb list. Test: does the operator-facing close lead with a strategic diagnosis (sophistication shift, white-space angle, vocabulary turn) rather than a roll call ? If it leads with the roll call, rewrite.

**Filter-bubble queries.** If the agent only searches what the brand's own positioning already says, every result confirms the operator's existing framing and the run produces no insight. Per `contextual-intelligence.md § The agent always... Challenges the operator's framing when the data contradicts it`, the crawl includes contrarian queries · *"why {category} doesn't work"*, *"alternatives to {category}"*, *"{category} scam"* · to surface what the operator's framing misses. Test: does the corpus contain at least 10% verbatims that argue *against* the category itself ? If zero, the crawl was filter-bubbled.

**Stale recency.** A 2022 thread on a fast-moving niche (skincare actives, supplements) is misleading and may invert the sophistication call. Default filter is 540 days ; loosen for slow-moving categories (cookware, mass kibble, hardware tools) where claim shape moves over years not quarters. Test: what is the median publish date of the verbatims grounding each claim ? If older than 18 months on a fast niche, downgrade or refresh the source pull.

## Section 7 · Output schema integration

Codes generated by the four lenses flow into the brand context through the standard mutation gate. The agent never edits JSON directly ; every write goes through `write_to_context` in `mode=proposed` per the workspace mutation rule.

| Lens | Primary route | Companion routes |
|---|---|---|
| Vernacular | `audiences/{slug}/profile.json#voice.market_vernacular[]` | source verbatims in `brands/{slug}/sources/vom/{run_id}/` |
| Sophistication | `brand.json#market.market_overview.sophistication_stage` | `brand.json#market.awareness_distribution` for stage-derived shifts |
| White space | `brand.json#market.external_intelligence[]` (cap 5-7 per run) | flagged on competitor entries when relevant |
| Porter (selective) | `brand.json#market.external_intelligence[]` as 1-2 entries naming the active force | competitor positioning notes when rivalry is the active force |

Each proposed mutation carries a source block linking back to the run-id and the Layer A verbatim IDs that grounded it, so the operator can drill into any proposed write and see the evidence · per the audit-v2.7.4 provenance discipline. The framework's job is the coding ; the skill's job is the write-back. The operator never sees the framework variable names, only the synthesis paragraph and the staged proposals expressed in plain language.

Detail of the corpus archive layer, the proposed-mutation linkage to verbatims, and the operator-language presentation rules live in `mine-vom/SKILL.md` and the brief `audit-v2.7.4-prompting/deepening-skills-research/02-mine-vom.md`. This framework defines *how to code* market signal ; the skill defines *how to write it back* under the operator contract.
