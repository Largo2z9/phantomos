# VoC Coding Framework

> Codified analytical lenses applied to every verbatim captured by `mine-voc`. Consumed, not improvised. The skill quotes this file as the binding reference for what each tag means and when it earns the label. If a verbatim cannot be coded against the rules below, it stays in Layer A as raw evidence and does not propagate into Layer B.

This framework defines four lenses (Jobs-To-Be-Done, Schwartz awareness levels, theme typology, pain category granularity), the order in which they apply, the anti-patterns that corrupt the corpus, and the exit points into the PhantomOS schema. The downstream value of mine-voc is bounded by the quality of this coding. Under-quality here corrupts every brief, hook, and copy decision that consumes the corpus afterwards.

---

## 1. Jobs-To-Be-Done

This section codes what the customer hired the brand to do for them, beyond the surface product description.

A JTBD code names the underlying job in the customer's frame, not the brand's frame. It splits along three dimensions, present together in most verbatims and tagged independently when the language supports the split. Functional is what the product mechanically delivers in the customer's life. Emotional is the internal state the purchase resolves. Social is the position relative to others the purchase secures. A skincare buyer saying *"je peux enfin me regarder dans le miroir le matin sans me cacher"* carries a thin functional signal (something visible improved), a strong emotional one (shame relief), and a latent social one (presentability). Each dimension is coded only if the verbatim names it; absence of mention is absence of evidence, not absence of the job.

The binary tests are tight. **Functional**: does the verbatim name a measurable change in physical state, time, output, or behavior? *"Je dors 7h au lieu de 4h"* yes; *"je me sens mieux"* no. **Emotional**: does it name a feeling state, anxiety, relief, fear, pride, or self-perception change? *"Je n'ai plus peur de regarder mes mails le matin"* yes; *"super produit"* no. **Social**: does it position the speaker against another (partner, peer, doctor, parent, colleague, stranger)? *"Mon mari ne me dit plus que je sens fort"* yes; *"je sens bon"* no.

Three good-bad pairs anchor the calibration.

**Skincare.** Good code on *"j'ai arrêté de mettre du fond de teint pour aller chercher mes enfants à l'école"* · functional (skin baseline visible enough to skip makeup), emotional (confidence to be seen bare), social (school-pickup peer context). Bad code on the same verbatim reduced to *"likes the product"* · collapses three dimensions into a sentiment polarity and loses every actionable signal.

**Supplement.** Good code on *"je peux enfin tenir mes réunions de l'après-midi sans café"* · functional (sustained energy without stimulant), emotional (relief from caffeine dependency anxiety), social absent (no peer reference). Bad code on *"gives me energy"* · generic, no JTBD layer, the verbatim is too thin and stays uncoded as JTBD signal (still useful for benefit theme).

**Fashion.** Good code on *"c'est la première marque où je trouve un 42 qui tombe comme du 38"* · functional (fit at size), emotional (size-shame relief), social (parity with smaller-size peers). Bad code on *"belle qualité"* · no JTBD content, codes as benefit-perceived only, JTBD field stays null.

The miscoding to watch is treating brand benefits as jobs. *"Formule clean"* is what the brand says it sells, not the job the customer hired it for. The job is downstream · *"je n'ai plus peur de mettre la crème pendant ma grossesse"*. Stay in customer voice; if the verbatim only restates a brand claim, JTBD is null.

---

## 2. Schwartz Awareness Levels

This section codes where the speaker stands on the awareness ladder, which determines what copy and creative angle will land for that audience segment.

The five stages map to vocabulary, specificity, and frame of reference. **Unaware** speakers do not name the problem the product solves; the verbatim references adjacent symptoms or none at all. **Problem-aware** speakers name the problem but not the category of solution. **Solution-aware** speakers name the solution category and have shopped it. **Product-aware** speakers compare named products in the category. **Most-aware** speakers know this brand specifically and are deciding on offer, format, or repeat-purchase. Stage assignment is a single value, not a range · pick the highest stage the verbatim demonstrates.

Binary tests, ordered most-aware down. **Most-aware**: names the brand or a specific SKU and discusses repurchase, format, or offer terms. **Product-aware**: names two or more competing branded products in the category. **Solution-aware**: names the solution category (*"sérum à la niacinamide"*, *"complément magnésium"*) without naming brands, and has tried at least one. **Problem-aware**: names the problem state (*"je ne dors pas"*, *"j'ai des taches"*) without a solution category. **Unaware**: complains of a downstream symptom without naming the problem the product solves (*"je suis crevée tout le temps"* read by a magnesium brand).

Three examples per stage anchor the coding.

**Unaware.** *"Je ne sais plus pourquoi je suis aussi fatiguée le matin"* (read by a sleep-supplement brand · fatigue is the symptom, the sleep problem is not yet framed). *"Mon visage tire mais je ne sais pas ce qu'il faut"* (skincare). *"Mes affaires ne me vont plus comme avant"* (fashion sizing brand).

**Problem-aware.** *"Je dors mal depuis trois mois et ça commence à peser"* (sleep). *"J'ai des taches pigmentaires post-grossesse"* (skincare). *"Je fais du 42 et rien ne tombe bien sur moi"* (fashion).

**Solution-aware.** *"J'ai testé la mélatonine, ça me rend groggy le matin"* (sleep). *"J'ai essayé deux sérums vitamine C, ça pique"* (skincare). *"Les marques de denim mid-size ne couvrent jamais ma morphologie"* (fashion).

**Product-aware.** *"Entre Nuit Calme et Chronodorm, je n'arrive pas à choisir"* (sleep). *"Caudalie Vinoperfect vs The Ordinary niacinamide, j'hésite"* (skincare). *"Sézane fait du 42 mais ça taille petit, Sessùn taille mieux mais coupe haute"* (fashion).

**Most-aware.** *"Je commande votre cure 3 mois mais je vois que vous faites une formule renforcée maintenant"* (sleep). *"Votre sérum tient bien mais je voudrais le format 50ml"* (skincare). *"Je reprends le même jean que l'an dernier mais j'ai vu que vous avez changé l'étiquette taille"* (fashion).

The stage matters because copy aimed at the wrong stage misses. A problem-aware buyer needs solution-category education; a most-aware buyer needs offer terms. Snapshot's inferred audience is usually one stage above where the actual customers sit; the corrective is one of the load-bearing findings of mine-voc.

---

## 3. Theme Typology

This section codes the type of statement carried by the verbatim, independent of valence.

A verbatim can carry zero, one, or many themes. Multi-theme is normal; *"le produit est top mais la livraison est catastrophique"* carries benefit (product) plus pain (operational). The typology is closed · no ad-hoc themes. If a verbatim does not match any of the seven below, it is corpus-only and does not become Layer B signal.

| Theme | What it looks like in verbatim | Tag rule | When to reject as noise |
|---|---|---|---|
| **Pain** | Names a problem the product is failing to solve, or a problem present before purchase | Tag with sub-axis (functional / emotional / social / financial) per § 4 | Vague displeasure (*"bof"*, *"pas top"*) without a named problem axis |
| **Benefit** | Names a positive outcome attributable to the product | Distinguish perceived (customer's frame) from claimed (echoes brand copy) | Generic praise (*"super produit"*) · codes as sentiment polarity only |
| **Objection** | Names a hesitation, doubt, refusal, or post-purchase regret | Tag sub-type: price / trust / fit / use case / regulatory | Pure complaint already coded as pain · objection is a *barrier to purchase or repurchase* |
| **Comparison** | Positions the product against another (named or implicit) | Tag axis: vs competitor / vs alternative format / vs nothing (status quo) | Comparison without an evaluation (*"j'ai aussi essayé X"* alone) · needs a verdict to count |
| **Surprise** | Outcome diverges from expectation, positive or negative | Tag valence (positive / negative) · surprise is structurally different from benefit because it reveals an unmet expectation about the brand promise | Mild satisfaction is benefit, not surprise; surprise needs an explicit *"je ne m'attendais pas"* signal |
| **Vocabulary** | A vernacular term, expression, or phrasing worth capturing for downstream copy | Tag the exact phrase, language, frequency, sample_size | Brand jargon repeated by the customer (*"actifs naturels"*) · that is brand voice echoed back, not vernacular |
| **Social proof signal** | Names review density, expert mention, peer recommendation, or third-party validation as the purchase trigger | Tag source type (peer / expert / press / influencer / review density) | Generic *"j'ai vu de bonnes critiques"* without a source type · too thin |

Two coding rules apply across themes. Preserve the verbatim text; the code lives next to the quote, not inside it. Recurrence is its own data point · a theme earns Layer B status when at least three distinct verbatims carry close variants of it; singletons stay in Layer A as evidence but do not become claims.

The hardest theme call is benefit-perceived versus benefit-claimed. *"Formule clean, j'adore"* is the brand's vocabulary echoed back · that is claimed-benefit signal, useful for measuring message penetration but not for discovering new angles. *"Je peux mettre la crème pendant ma grossesse sans stresser"* is perceived-benefit · that is the angle the brand under-exploits. Code both, distinguish them.

---

## 4. Pain Category Granularity

This section refines pain coding because price-too-high and feels-too-expensive-for-what-it-is are two different briefs.

Pains do not collapse into a single bucket. The granularity below distinguishes axes that drive different downstream actions · financial pain routes to offer engineering, emotional pain routes to copy framing, temporal pain routes to delivery and convenience design. A single pain verbatim can carry multiple categories; tag each that the verbatim explicitly names.

| Category | What it names | Customer-voice marker | Downstream routing |
|---|---|---|---|
| **Functional** | Product does not deliver the mechanical outcome | *"Ça ne marche pas"*, *"j'ai vu aucun changement après 3 mois"* | `spec.json#problems_solved[]` revisit; mechanism claim audit |
| **Emotional** | Internal state the product was supposed to resolve, persists or worsens | *"Je me sens encore plus moche"*, *"j'ai eu honte de l'avoir acheté"* | `profile.json#pain_points[].emotion`, copy framing |
| **Social** | Perceived position vs others around the use of the product | *"Mes amies se moquent quand je sors les flacons"*, *"mon médecin a tiqué"* | `profile.json#objections[]` (trust sub-type), creative direction |
| **Financial** | Absolute cost, budget impact, value-for-money in raw terms | *"40€ pour 30ml c'est trop cher pour mon budget"* | Offer engineering, bundle design, payment terms |
| **Temporal** | Time-to-result, timing of purchase, duration of use, moment-fit | *"3 mois avant de voir un effet, j'ai abandonné"*, *"acheté en hiver pour un produit d'été"* | Onboarding, expectation-setting copy, delivery window |
| **Relational** | Frictions with another person triggered by the purchase or use | *"Mon mari trouve ça inutile"*, *"ma dermato m'a déconseillé"* | Audience qualification, third-party trust signal design |

The financial-versus-emotional split is the most consequential miscode. *"C'est trop cher"* alone is financial · the absolute price is the barrier. *"Pour ce que c'est, c'est trop cher"* is value-perception, which sits between emotional pain (felt unfairness) and objection (price as barrier conditioned on perceived value). The two are not the same: financial pain is solved by lowering price or splitting payment; value-perception pain is solved by raising perceived value through proof, mechanism explanation, or repositioning. The brief that comes out of mine-voc has to know which one it is. When the verbatim is ambiguous, code both and let the synthesis flag the ambiguity rather than collapse it.

Relational pain is under-coded by default coders because it sits across categories and requires a third party to be named. It is also one of the highest-leverage findings · a *"mon médecin a tiqué"* pattern across three verbatims is a regulatory or trust signal that snapshot cannot see. Tag it whenever a third party shows up.

---

## 5. Coding Workflow

This section orders the four lenses to prevent re-work and contamination.

The order is deliberate. Theme typology runs first because it filters: a verbatim that codes as pure social-proof-signal does not need JTBD analysis, and a verbatim that codes as vocabulary-only feeds directly into `voice.key_expressions[]` without any further lens. JTBD runs second because it frames what the customer hired the product for, which is the structural backbone every other code hangs off. Awareness runs third because it depends on the vocabulary observed in steps one and two · a verbatim carrying named competitors is product-aware, full stop, and the lens applies near-mechanically once the theme and JTBD are locked. Pain category runs fourth and only conditionally, when theme = pain.

In sequence: (1) read the full verbatim once, no coding; (2) assign one or many themes from § 3; (3) if the verbatim names a job, code JTBD per § 1, splitting functional / emotional / social as the language supports; (4) assign Schwartz stage per § 2 using the highest-stage test that fires; (5) if any theme is pain, refine pain category per § 4; (6) capture vocabulary tags inline if vernacular phrasing is present; (7) attach provenance (platform, rating, verified_buyer) and write the entry to Layer A.

The skill batches verbatims through this workflow in groups of 30 to 80 per coding pass. Sample first when the corpus exceeds 200 · code 50 randomly sampled verbatims, check whether the coding distribution matches the brand's stated profile, and only run the full pass if the sample shows divergence. This is the validation-cascade-avoidance rule from `contextual-intelligence.md` applied to coding: do not run all four lenses on every verbatim before talking to the operator when a sample answers the synthesis question.

---

## 6. Anti-Patterns

This section names the failure modes that recur in first-pass coding and the binary test that catches each.

**Over-coding thin verbatims.** *"Super produit, je recommande"* is a sentiment polarity flag, not a four-lens artifact. JTBD is null, awareness is product-aware at most, theme is benefit-claimed, pain category is N/A. Forcing values into every field invents data. Test: if three of the four lenses return null or generic, leave them null.

**Inventing themes not in the verbatim.** A coder who infers *"the customer is probably price-sensitive"* from *"j'ai pris la cure 3 mois"* is fabricating. The verbatim says one thing · the customer bought a 3-month subscription · and price-sensitivity is not in it. Test: every code must point to a span of the verbatim that justifies it.

**Mixing coder voice with customer voice.** Paraphrasing *"je peux enfin me regarder dans le miroir"* as *"the customer expresses self-acceptance gains"* corrupts the corpus. The verbatim is the data; the code is the metadata. They never merge in Layer A. The synthesis paragraph in the operator-facing report can paraphrase, but the corpus stays raw.

**Aggregating away the singletons.** A theme earns Layer B status at three occurrences, but singletons are not noise · they are weak signal that stays in Layer A as audit material. A single verbatim mentioning a regulatory concern is not a finding, but it is corpus evidence available the day a second one appears. Test: never delete a verbatim from Layer A because it does not cluster.

**Forcing a Schwartz stage when vocabulary is thin.** A verbatim with no named problem and no named solution sits at unaware or stays uncoded for awareness. Promoting it to problem-aware because *"the brand sells a problem-aware solution"* is back-projection. Test: the verbatim's vocabulary alone determines the stage; if vocabulary is too thin, awareness is null.

**Treating brand voice echoed back as customer voice.** When a customer writes *"j'aime votre engagement clean beauty"*, that is the brand's positioning vocabulary returned, not vernacular. It measures message penetration, which is a useful signal in its own right, but it is not vocabulary worth capturing for downstream copy. Tag it as benefit-claimed, not as `voice.key_expressions[]`.

---

## 7. Output Schema Integration

This section names the exit points without duplicating the schema; full field definitions live in the entity schemas referenced.

The four lenses route into three Layer B targets. JTBD and pain coding feed `spec.json#problems_solved[].verbatim_quotes[]`, with `frequency` and `urgency` derived from corpus counts. Schwartz awareness tags onto `pain_points[].awareness_stage` and `benefits[].awareness_stage` in `profile.json`. Theme typology drives clustering across both entities and surfaces objections into `profile.json#objections[]` with their sub-type, severity, and lifecycle stage. Vocabulary tags flow into `profile.json#voice.key_expressions[]` with their `frequency`, `sample_size`, and `platform` triplet · without the denominator, frequency is meaningless and the schema enforces it.

Every Layer B field carrying VoC content must reference at least one Layer A `id` via `_source_meta.verbatim_ids`. That linkage is the audit chain · the operator clicks a synthesized claim, lands on the raw verbatim that justifies it. No claim without backing evidence; the doctrine carries through to the schema.

The skill writes everything in `mode=proposed` per the master mutation rule. Operator iteration in-session converges the proposed values; the in-session memory does the job, no enforcement layer needed downstream of the coding gate.

---

## References

- `mine-voc/SKILL.md` · the consumer of this framework. Cites this file as binding for every coding decision.
- `docs/system/contextual-intelligence.md` · master doctrine. The validation-cascade-avoidance and trust-the-model rules govern the workflow ordering above.
- `docs/system/voice.md` · voice canon. Operator-facing synthesis derived from coded corpus follows it strictly.
- `resources/schemas/spec.schema.json`, `resources/schemas/profile.schema.json` · exit points. Field definitions live there, never restated here.
