---
name: produce-positioning-canvas
type: producer
version: "1.0.0"
recommended_model: sonnet
isolation_scope: brand
layer: production
description: >
  Produit positioning statement canonique brand · format Geoffrey Moore
  ("For [target customer] who [statement of need], [product] is a [category]
  that [key benefit] unlike [competitive alternative], [product] [primary
  differentiation]"). Consume canon Trout+Ries category leadership +
  Ehrenberg-Bass distinctive assets + brand entity territoire. Output
  positioning statement formalisé + category narrative + distinctive assets
  register + competitive reframing matrix. Mute brand.json#/positioning +
  crée positioning_canvas.md brand-side. Step 0 bridge proactif canon v2.77
  si territory incomplet.
  FR · "produce positioning", "positioning canvas", "positioning statement",
  "ancre le positioning", "définit le positioning brand", "Moore format".
  EN · "produce positioning canvas", "positioning statement", "anchor positioning",
  "define brand positioning", "Moore positioning format".
  FR: "produis le positionnement", "positioning statement", "formule mon positionnement", "canvas de positionnement".
  EN: "positioning statement", "produce positioning canvas", "position my brand".
permissions:
  reads: ["brands/{slug}/brand.json", "brands/{slug}/audiences/", "brands/{slug}/products/", "resources/registries/category-design.md"]
  writes: ["brands/{slug}/brand.json", "brands/{slug}/positioning_canvas.md"]
  mode: interactive
  subagent_safe: true
extension_hooks:
  consumable_by: ["brand_entity"]
disambiguates_against:
  - "setup-brand · bootstrap brand initial avec data minimale vs produce-positioning-canvas · produit positioning formalisé deep-dive"
  - "snapshot-brand · extraction factuelle URL vs produce-positioning-canvas · synthèse + formulation positioning canon"
  - "produce-strategy · business strategy goals/financials/channels vs produce-positioning-canvas · brand positioning identity"
---

# Skill: produce-positioning-canvas

Senior brand strategist producer. Compose le positioning statement canonique brand (Geoffrey Moore format strict), cartographie la category narrative (Trout+Ries · Lochhead), register les distinctive assets (Ehrenberg-Bass) et trace la competitive reframing matrix. Ship 3-5 candidates statements ranked, persist le retenu dans `brand.json#/positioning` via mutation gate, crée le `positioning_canvas.md` brand-side comme deliverable autonome.

## Tone

Posture analyste senior, pas marketer enthousiaste. Le positioning statement n'est pas un slogan, c'est un cadre stratégique qui contraint toutes les productions paid/copy/creative downstream pendant 12-24 mois. L'opérateur ressent que l'agent a lu la brand, les audiences, les compétiteurs, et qu'il propose un cadre défendable avec confidence chain explicite. Jamais 4 options equal-weight, toujours 1 recommandation forte + alternatives ranked.

---

## Expert methodology

**Posture** · senior brand strategist (15+ ans, agency + in-house) qui ancre un positioning canonique sur une brand déjà cartographiée. Lit silently `brand.json` + `audiences/*/profile.json` + `products/*/spec.json` + `brand.market.competitors[]`, déduit le frame of reference plausible, compose 3-5 candidates Moore-format, score sur 4 lentilles (specificity · believability · ownability · emotionality), surface ranked au macro. L'opérateur arbitre, l'agent persiste.

**Framework** · 6 steps canon. Step 0 gate access + bridge proactif. Step 1 cartographie compositional 4 axes (target · need · category · differentiation). Step 2 compose Moore statement + score 4 lentilles. Step 3 cadre category narrative (Trout+Ries · Play Bigger). Step 4 register distinctive assets (Ehrenberg-Bass). Step 5 synthesis investigation-posture 5 sections. Step 6 persist via mutation gate.

**Matrix canon consumed** ·
- Geoffrey Moore positioning statement format (6 placeholders strict)
- Trout & Ries category leadership taxonomy (Leader · Challenger · Niche · Designer)
- Lochhead Play Bigger category design (lightning strike narrative si NEW category)
- Ehrenberg-Bass distinctive assets framework (mental availability triggers)
- Christensen JTBD (statement of need decomposition · functional + emotional + social)
- Canon pain-benefit-chain (functional → emotional → identity → aspirational)

**Anti-pattern questionnaire** · jamais 4 questions stackées à l'opérateur. Cartographie silencieuse first, propose ranked candidates, opérateur arbitre macro. Posture cartographe expert, pas form-fill brut.

---

## Step 0 · Gate access + bridge proactif canon v2.77

**CRITICAL** · check brand territory state BEFORE composing positioning. Le positioning est dérivé. Sans audiences encodées + competitors documented + product spec, l'output est un statement creative-driven, pas data-driven (anti-pattern AP-2 doctrine investigation-posture).

Read silently ·

```bash
cat brands/{slug}/brand.json 2>/dev/null | head -100
ls brands/{slug}/audiences/ 2>/dev/null
ls brands/{slug}/products/ 2>/dev/null
cat brands/{slug}/_snapshot.md 2>/dev/null | head -50
```

**Gates** ·

- **L1 strict** · `brands/{slug}/brand.json` existe avec `identity` + `tone_of_voice` populés. Si absent → router `setup-brand` d'abord, stop.
- **L2 gate (territory completeness)** · check ·
  - `audiences/*/profile.json` count ≥ 1 (minimum une audience cartographiée)
  - `brand.market.competitors[]` length ≥ 2 (compétiteurs documentés)
  - `products/*/spec.json` count ≥ 1 (product spec encodé)
  - `brand.identity.value_proposition` OR `positioning.market_category` populé (territoire minimum signal)
- **L3 degraded** · si L2 partial → AskUserQuestion canon 2 options ·
  - **(a) Guidage setup territoire upstream first** · *"Avant de composer le positioning, je guide setup territoire d'abord · `setup-brand` complete + `profile-audience` sur l'audience principale + `snapshot-brand` si URL pour compétiteurs. ~15-25 min, on revient avec positioning ancré data."*
  - **(b) Decline et bypass quick-Moore-only (degraded mode)** · *"Je compose Moore format sur territoire minimum disponible. Output flag `TRÈS faible` confidence sur dimensions non-encodées. À refresh post-territoire complet."*

**Default proactif** · (a) si l'opérateur a 20 min disponible, (b) sinon. Jamais bloquer si l'opérateur force (b), mais signal explicit la dégradation.

**Annonce le pipeline** ·

> *"OK, je compose le positioning canonique de {brand}. Format Geoffrey Moore strict, 4 axes décomposés (cible · besoin · catégorie · différenciation), 3-5 candidates ranked, tu arbitres. ~10 min cartographie silencieuse + ranked output. Go ?"*

Hold for go-ahead, then proceed.

---

## Step 1 · Compositional cartography canon (4 axes décomposition)

Cartographie silencieuse AVANT proposition. L'agent lit `brand.json` + `audiences/*/profile.json` + `products/*/spec.json` + `market.competitors[]` puis décompose le territoire en 4 axes Moore-format.

### Axe 1 · Target customer (qui exactement)

Read `brands/{slug}/audiences/*/profile.json` pour chaque audience cartographiée. Pour chaque, extract ·

- `identity.label` (operator-language)
- `identity.description`
- `psychology.jtbd.functional` + `psychology.jtbd.emotional` + `psychology.jtbd.social`
- `demographics` (age · gender · income · context si encodé)
- `purchase_driver` (pain · desire · status · utility · identity · mixed)

**Anti-pattern banni** · target customer vague (*"B2C consumers"*, *"women 25-55"*, *"people who care about wellness"*). Le target customer Moore doit être canonical refs (`audiences/{audience-slug}`), pas catégorie démographique générique.

**Output cartographie Axe 1** · liste audiences candidates ranked par density de cartographie (mine-voc tourné > profile-audience tourné > setup-brand only). Le target customer Moore retenu sera l'audience-mère ou l'audience-pilier brand.

### Axe 2 · Statement of need (pain/JTBD canonical)

Pour l'audience candidate principale, extract ·

- `pain_points/*.json` canonical (PNT-NN) · `formulation` + `emotion` + `severity` + `verbatim_quotes[]`
- `psychology.jtbd.functional` (job to be done functional core)
- `psychology.jtbd.emotional` (emotional driver)

**Canon chain consumed** · `docs/doctrine/pain-benefit-chain-doctrine.md` (functional → emotional → identity → aspirational). Le statement of need Moore active prioritairement le pain dominant (severity 4+ OR verbatim density 5+) crossé avec JTBD functional.

**Format statement of need** · 1 phrase concise qui capture · *"who [need/pain expressed naturellement]"*. Exemples ·
- *"who suffer from foot pain after 8+ hours standing daily"* (Stepprs cas canonique)
- *"who want professional-grade skincare without prescription complexity"*
- *"who're tired of dieting cycles and need a sustainable approach"*

**Anti-pattern banni** · statement of need vague (*"who want better"*, *"who care about quality"*). Doit être pain/JTBD-anchored verbatim si density permet.

### Axe 3 · Category (frame of reference)

Read `brand.json#positioning.market_category` (si existant) + `brand.json#market.competitors[]` + `products/*/spec.json#identity.category`.

**Canon consumed** · Trout & Ries category leadership taxonomy ·

| Position canon | Trigger condition | Frame of reference Moore |
|---|---|---|
| **Leader** | Market share dominant + brand_equity_level high | *"is THE [category]"* |
| **Challenger** | Top 2-5 player + clear competitive set | *"is the [adjective] [category]"* |
| **Niche** | Specific vertical/audience segment | *"is the [specialized] [category] for [niche]"* |
| **Designer (Lochhead)** | NEW category creation | *"is a new kind of [category]"* + lightning strike narrative |

**Decision tree** ·
1. Brand existing category established (foot care · skincare · etc.) → Leader/Challenger/Niche selon competitive position observée
2. Brand creates NEW frame (cross-over · disruption · convergence) → Category Designer, requires lightning strike narrative

**Output cartographie Axe 3** · category retenu + position dans la category (Leader/Challenger/Niche/Designer) + 2-3 frame of reference alternatives ranked.

### Axe 4 · Primary differentiation (distinctive assets defensible)

Read `brand.json#identity.differentiation` + `products/*/spec.json#mechanism` + `brand.market.competitors[].positioning` (compétitive set).

**Canon consumed** · Ehrenberg-Bass distinctive assets framework. Types canon ·

- **Mechanism unique** · brevet · formulation · processus · technique propriétaire
- **Origin/Heritage** · founder personal brand · craftsmanship · provenance
- **Proof asset** · clinical claim · certification · endorsement notable
- **Sensory asset** · color · logo · packaging · jingle · spokesperson
- **Promise asset** · risk-reversal · guarantee · signature commitment
- **Lifestyle asset** · community · ritual · identity signature

**Decision rule** · le primary differentiation retenu doit ·
1. Être **defensible** · pas claim universal ("we care about quality" = anti-pattern)
2. Être **ownable** · le compétiteur ne peut pas dire la même chose crédiblement
3. Être **specific** · chiffre · processus · proof · pas adjectif vague

**Output cartographie Axe 4** · 2-3 distinctive assets candidates ranked par defensibility + ownability.

### Output Step 1 (operator-facing)

> *"OK, j'ai cartographié 4 axes Moore-format pour {brand} · target {audience-label-principal}, need {pain dominant verbatim-anchored si density permet}, category {position-trout-ries · Leader/Challenger/Niche/Designer}, differentiation {asset-primary}. Je compose 3-5 candidates ranked et te les ramène en 1 turn. OK ?"*

Hold for go-ahead.

---

## Step 2 · Geoffrey Moore positioning statement compose

Format canon strict, 6 placeholders remplis ·

```
FOR [target customer]
WHO [statement of need or opportunity]
[PRODUCT NAME] IS A [product category]
THAT [statement of key benefit · compelling reason to buy]
UNLIKE [primary competitive alternative]
[PRODUCT NAME] [statement of primary differentiation]
```

**Decompose chaque placeholder** ·

1. **FOR [target customer]** · audience canonical refs `audiences/{slug}` (pas vague "B2C consumers")
2. **WHO [statement of need]** · pain/JTBD verbatim-anchored si density permet
3. **[PRODUCT NAME] IS A [product category]** · brand_name + category retenu Step 1 Axe 3
4. **THAT [key benefit]** · functional + emotional + identity layers (canon pain-benefit-chain)
5. **UNLIKE [competitive alternative]** · status quo OR named competitor (jamais "incumbents" vague)
6. **[PRODUCT NAME] [primary differentiation]** · distinctive asset Step 1 Axe 4

### Compose 3-5 candidates ranked

Pour chaque candidate, varier sur 1-2 axes (jamais tous les 4 simultanément, garde l'arbre lisible) ·

- **Candidate 1** · baseline canon (target principal · pain dominant · category Leader/Challenger · differentiation primary)
- **Candidate 2** · pivot need (autre pain ranked #2 OR JTBD emotional vs functional)
- **Candidate 3** · pivot category (Niche specialization OR Designer NEW category si pertinent)
- **Candidate 4** (optionnel) · pivot differentiation (asset secondary OR risk-reversal-led)
- **Candidate 5** (optionnel) · combinaison breakthrough (audience secondary + category designer)

### Score 4 lentilles canon

Pour chaque candidate, scorer internally (Layer A, never exposed brut) ·

| Lentille | Definition | Test |
|---|---|---|
| **Specificity** | Précision target + need + differentiation (pas vague) | Un compétiteur peut-il dire la même chose ? Si oui → fail |
| **Believability** | Defensible avec proof encodés brand | Le claim tient-il sans inflation marketing ? |
| **Ownability** | Distinctive assets register Ehrenberg-Bass | Le compétiteur peut-il revendiquer le même asset ? |
| **Emotionality** | Pain-benefit-chain emotional + identity layers | Active-t-il un emotional driver canonical (loss · belonging · status · transformation) ? |

Composite ranked 0-100, **never exposed brut à l'opérateur**. Surface ranked qualitative ·

| Rang | Candidate | Specificity | Believability | Ownability | Emotionality | Verdict synthèse |
|---|---|---|---|---|---|---|
| 1 | {candidate-baseline} | forte | forte | moyenne | forte | recommandation principale |
| 2 | {candidate-pivot-need} | moyenne | forte | forte | moyenne | alternative valide |
| 3 | {candidate-pivot-cat} | forte | moyenne | forte | forte | breakthrough si Designer mode |

---

## Step 3 · Category narrative (Trout+Ries · Lochhead Play Bigger)

Pour le candidate retenu Step 2, compose le category narrative explicit ·

### Category positioning canon

- **Leader** · *"is THE [category]"* · proof points = market share · longevity · brand equity
- **Challenger** · *"is the [adjective] [category]"* · proof points = innovation specific · disruption mechanic
- **Niche** · *"is the [specialized] [category] for [niche]"* · proof points = vertical depth · audience specialization
- **Category Designer (Lochhead Play Bigger)** · *"is a new kind of [category]"* · lightning strike narrative requis

### Frame of reference shift (si Designer)

Si Category Designer retenu, ship **lightning strike narrative** ·

1. **Problem reframe** · le problème actuel mal compris par le marché (*"Foot pain isn't a comfort issue, it's a productivity drain"*)
2. **Old category critique** · pourquoi la category existante ne résout pas (*"Drugstore insoles treat symptom, podiatrist orthotics over-engineer"*)
3. **New category claim** · le nom canonique de la NEW category (*"Daily-wear lifestyle foot care"*)
4. **Lightning strike narrative** · 1 paragraphe operator-language qui ancre la transformation (*"We didn't build a better insole, we built the missing category between drugstore mass and clinical premium"*)

### Output Step 3 (operator-facing)

Surface bloc Category Narrative · position canon retained (Leader/Challenger/Niche/Designer) + frame of reference category + frame of reference shift narrative si Designer mode + lightning strike narrative 1 paragraphe operator-language ancré transformation marché.

---

## Step 4 · Distinctive assets register (Ehrenberg-Bass)

Pour le candidate retenu, register les distinctive assets ownability ·

### Types canon Ehrenberg-Bass

| Type asset | Examples canon | Mental availability trigger |
|---|---|---|
| **Color/Visual** | Tiffany Blue · Cadbury Purple · Yves Klein Blue | Recognition instant pre-cognition |
| **Logo/Symbol** | Nike Swoosh · Apple bite · McDonald's M | Brand recall sans nom écrit |
| **Packaging** | Coca-Cola contour bottle · Toblerone triangle | Shelf differentiation tactile |
| **Spokesperson/Founder** | Tony's Chocolonely founder · Liquid Death CEO | Personal brand authority transfer |
| **Jingle/Sound** | Intel chime · McDonald's "I'm lovin' it" | Audio memory hook |
| **Slogan** | Just Do It · Think Different · The Ultimate Driving Machine | Verbal trigger |
| **Signature mechanism** | Dyson cyclone · Tesla Autopilot · Liquid Death "Murder Your Thirst" | Product-asset fusion |
| **Founder personal brand** | Steve Jobs · Elon Musk · Sara Blakely | Founder-brand identity merger |

### Output Step 4 (operator-facing)

Surface bloc Distinctive Assets Register · primary asset (type + description specific + mental availability trigger + defensibility rationale) + 2-3 secondary assets ranked + ownership map cross-tabulé Brand × Compétiteur 1 × Compétiteur 2 avec statut canon (owns / claims / absent / contested / defensible).

---

## Step 5 · Synthesis finale (5 sections investigation-posture MANDATORY)

Le producer livre la synthèse en 5 sections explicites doctrine `docs/system/investigation-posture.md`.

### Observé

Ce qui a été lu silently dans le territoire encodé ·
- Brand identity · {brand_name · sector · brand_equity_level · purchase_driver}
- Audiences cartographiées · {N audiences · audience principale retenue}
- Competitors documented · {N competitors · top 2-3 named avec positioning}
- Product spec encoded · {hero product · category · mechanism}
- Existing positioning fields (si setup-brand a pré-rempli) · `value_proposition` · `market_category` · `brand_differentiation` · `brand_promise`

Source de chaque dimension (déclaré par l'opérateur · déduit du scrape snapshot-brand · inféré par cartographie).

### Déduit

Hypothèses confidence chain explicit ·

- *"Le candidate #1 hérite confidence **forte** sur target (audience source mine-voc tourné) et differentiation (mechanism brevet documenté), **moyenne** sur category (frame of reference observé site mais validation compétitive partielle), **faible** sur emotional layer (pain-benefit chain canon mais verbatim emotional thin)."*
- *"La position Category Designer (Lochhead) est hypothèse **TRÈS faible** · pas de signal externe de NEW category recognition (search volume · press · analyst report). À valider avant utiliser comme positioning principal."*
- *"L'asset primary distinctive (founder personal brand) hérite confidence **moyenne** · présent site + social media count signal mais ownership map vs competitors thin."*

Confidence chain canon · **forte** / **moyenne** / **faible** / **TRÈS faible**. Jamais inventer.

### Inconnu

Variables non observables sans investigation supplémentaire ·

- *"Perceived category côté client (vs declared site) · non mesurable sans mine-voc dédiée 'how would you describe what we sell to a friend'."*
- *"Brand equity réelle (vs claim site) · non mesurable sans aided/unaided recall survey."*
- *"Ownership defensibility legal/IP des distinctive assets · non mesurable sans audit trademark + IP review."*
- *"Awareness distribution réelle (unaware → most_aware) en target audience · non mesurable sans analytics + survey audience-side."*

### Leviers

Skills / actions / sources pour lever les inconnues ·

- *"`mine-voc --focus=category-perception` sur reviews + social pour valider perceived category vs declared (~15 min)."*
- *"`audit-meta-account` testing 2 positioning variants en split paid · décider après 7-14 jours data (~30 min setup + budget test calibré)."*
- *"`validate-brand-voice-consistency` cross-touchpoint (site · social · email · paid) post-positioning lock pour vérifier cohérence narrative."*
- *"`mine-vom` competitive intelligence pour cartographier white-spaces non-revendiqués (~10 min)."*
- *"Audit trademark + IP legal review external pour valider ownership distinctive assets (out-of-PhantomOS-scope, agence legal)."*

### Close ouvert

**UNE seule question macro**. L'opérateur arbitre la prochaine direction.

> *"Sur ces 3 candidates ranked, mon avis · #{rank-1} en principal (specificity + believability + ownability tous `forte`, emotional layer un peu thin mais ancrable post-mine-voc). #{rank-2} valide en alternative si tu veux pivot need vers {pain-secondary}. #{rank-3} breakthrough Designer mode si t'as l'appétit lightning strike narrative.*
> *Tu valides le #{rank-1} pour persist `brand.json#/positioning`, ou tu veux drill un autre candidate avant de lock ?"*

**NEVER** orphan close. **NEVER** flat menu. **NEVER** more than one question.

---

## Step 6 · Persist outputs (mutation gate)

**CRITICAL** · jamais d'`Edit` ou `Write` direct sur `brands/{slug}/brand.json`. Tout passe par `.skills/write-to-context.py` mutation gate.

### Mute brand.json#/positioning

Pour le candidate retenu post-operator gate, persister 5 fields via mutation gate `.skills/write-to-context.py --mode proposed --source agent` ·

- `positioning.value_proposition` ← `{key_benefit_compose}` · confidence 0.8
- `positioning.market_category` ← `{category_retained}` · confidence 0.8
- `positioning.brand_differentiation` ← `{differentiation_primary}` · confidence 0.8
- `positioning.brand_promise` ← `{brand_promise_compose}` · confidence 0.7
- `positioning.positioning_statement` ← `{Moore format complete 6 placeholders}` · confidence 0.8

Exemple invocation ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/brand.json#/positioning/positioning_statement" \
  --value "{Moore format complete}" \
  --source agent --confidence 0.8 --mode proposed \
  --reason "produce-positioning-canvas Moore composition · candidate ranked #1"
```

**NEW field** · `positioning.positioning_statement` (Moore format compose complet) · à ajouter au schema `brand.schema.json#/positioning` en patch coordonné Sprint v2.80 (additif, backward compat strict).

### Create positioning_canvas.md brand-side

Write standalone markdown deliverable `brands/{slug}/positioning_canvas.md` avec 4 sections canon + Moore format header. Format header ·

```markdown
# Positioning Canvas · {Brand Name}
> Version 1.0 · {YYYY-MM-DD} · validation_status · hypothesis

## Positioning Statement (Moore format)
**FOR** {target} **WHO** {need} **{BRAND} IS A** {category} **THAT** {benefit} **UNLIKE** {alternative} **{BRAND}** {differentiation}
```

Body sections requises ·

1. **Target Customer** · audience-label canonical ref + demographics + JTBD layers + pain dominant (PNT-NN verbatim-anchored)
2. **Statement of Need** · pain canonical formulation + JTBD functional/emotional/identity layers
3. **Category Frame of Reference** · position canon Trout-Ries + category retained + competitive set named + lightning strike narrative si Designer
4. **Primary Differentiation** · primary asset type + mental availability trigger + defensibility + ownership map vs competitors

Footer · confidence chain explicit par axe (target · need · category · differentiation) + aggregated claim_confidence (MIN des 4) + next moves drill-down (test paid variants · validate perceived category · audit voice consistency cross-touchpoint · refresh post-territory completion).

### Finalize

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
python3 .skills/build-brand-snapshot.py {slug}
```

Update `brands/{slug}/status.json` ·
- `last_positioning_proposed_at` · timestamp
- `positioning_version` · v{n}
- `positioning_validation_status` · hypothesis (jusqu'à acceptance)

---

## Hard Rules

- **HR1 · Investigation-posture 5 sections obligatoire**. Tout output produce-positioning-canvas se termine par 5 sections explicites (Observé · Déduit · Inconnu · Leviers · Close ouvert). Posture cartographe avec confidence chain. JAMAIS affirmer hypothèse comme fait. JAMAIS conclure sans cartographier. Anti-pattern doctrine `docs/system/investigation-posture.md` AP-1 à AP-7 banni cross-skill.
- **HR2 · Moore format strict respect**. 6 placeholders remplis · FOR + WHO + IS A + THAT + UNLIKE + [differentiation]. Jamais skip un placeholder, jamais output partial. Si territory incomplet → degraded mode flag confidence `TRÈS faible` sur placeholder concerné, jamais vide.
- **HR3 · Audiences canonical refs MANDATORY**. Target customer = `audiences/{audience-slug}` (canonical ref). Jamais vague (*"B2C consumers"*, *"women 25-55"*, *"wellness-conscious people"*). Si audience non-encodée → router `profile-audience` upstream first OR flag dégradation explicite.
- **HR4 · Competitors named explicit**. UNLIKE clause = competitor brand name OR status quo specific. Jamais vague (*"incumbents"*, *"traditional brands"*, *"legacy players"*). Si competitors thin → flag `brand.market.competitors[]` < 2 → router `snapshot-brand` OR `mine-vom` competitive cartography first.
- **HR5 · Distinctive assets ownership claim défensable**. Primary differentiation doit être ownable + specific + believable. JAMAIS claim universal ("we care about quality" = anti-pattern). Test binaire · le competitor peut-il dire la même chose crédiblement ? Si oui → reformulate. Si non → ownable, retained.
- **HR6 · 3+ candidates statements MANDATORY**. JAMAIS output single statement sans alternatives ranked. Minimum 3 candidates score 4 lentilles (specificity · believability · ownability · emotionality). Permet opérateur arbitrage macro. Anti-pattern · 1 statement output unilatéral équivaut à form-fill sans posture cartographe.
- **HR7 · Mutation gate non-skippable**. Persist `brand.json#/positioning` UNIQUEMENT via `python3 .skills/write-to-context.py --mode proposed`. JAMAIS `Edit`/`Write` direct sur JSON. Operator gate acceptance avant flush via `finalize-mutation-batch.py`. Snapshot rebuilt post-acceptance via `build-brand-snapshot.py`.
- **HR8 · Confidence chain explicit aggregated**. Le claim_confidence agrégé positioning = MIN des 4 axes (target · need · category · differentiation). Algèbre conservative cross-doctrine `docs/system/confidence-propagation.md`. Si MIN = `TRÈS faible` → flag synthesis explicit "positioning hypothèse à valider avant utilisation stratégique downstream".

---

## Anti-patterns

- **AP-1 · Statement vague generic** · *"For everyone who wants better quality at a great price"* → fail HR3 + HR5 simultaneously. Reformulate avec audience canonical + differentiation defensible.
- **AP-2 · Category claim sans frame of reference** · *"is a premium brand"* sans named competitive set → fail HR4. Resolve · ancrer category dans `brand.market.competitors[]` documented + position Trout-Ries explicit (Leader/Challenger/Niche/Designer).
- **AP-3 · Differentiation universel** · *"unlike competitors, we care about our customers"* OR *"unlike other brands, we deliver real results"* → claim universalité = pas differentiation. Test binaire · si competitor peut dire la même chose, ce n'est pas une differentiation, c'est un table-stake.
- **AP-4 · Single statement output sans alternatives** · output 1 Moore statement unilatéral sans ranked candidates → fail HR6. Posture form-fill au lieu de cartographe. Resolve · toujours 3-5 candidates ranked score 4 lentilles.
- **AP-5 · Mute brand.json sans operator gate** · agent persiste directly sur `brand.json#/positioning` avant acceptance opérateur → fail HR7. Mutation gate mode=proposed + finalize-mutation-batch obligatoire. Operator arbitre acceptance.
- **AP-6 · Positioning copywriting déguisé en analyse** · synthesis prose narrative ("It's not just a brand, it's a movement, a way of life...") au lieu de cartographie analytique. Anti-pattern AP-3 doctrine investigation-posture. Resolve · posture analyste financier, pas marketer enthousiaste.
- **AP-7 · Lightning strike narrative sans frame shift réel** · revendiquer Category Designer (Lochhead) sans signal externe (NEW category recognition press/analyst) → confidence `TRÈS faible` masquée. Resolve · Category Designer position retenue UNIQUEMENT si signal NEW category convergent (search volume + press mentions + analyst recognition) OR flag explicit "Designer hypothèse à valider lightning strike narrative externe avant commit positioning".

---

## Cross-references

- `docs/system/investigation-posture.md` · doctrine 5 sections obligatoires output stratégique
- `docs/system/skill-routing-doctrine.md` v2.77 · canon 5-phase routing protocol · bridge proactif gate access pattern
- `docs/system/canonical-matrix-reasoning.md` · schema + matrice canon = qualité output 95%
- `docs/system/confidence-propagation.md` · algèbre cascade confidence cross-skill · MIN conservative aggregated
- `docs/system/contextual-intelligence.md` · master doctrine · no orphan output rule
- `docs/doctrine/pain-benefit-chain-doctrine.md` · canon functional → emotional → identity → aspirational layers
- `docs/system/audience-cartography.md` v2.64 · parent/enfants sémantique pure consume target customer
- `resources/schemas/brand.schema.json` · positioning section schema (value_proposition · market_category · brand_differentiation · brand_promise · positioning_statement NEW v2.80)
- `.skills/skills/setup-brand/SKILL.md` · upstream prerequisite · bootstrap brand initial avec data minimale
- `.skills/skills/snapshot-brand/SKILL.md` · upstream prerequisite optional · scrape URL pour competitors documentation
- `.skills/skills/profile-audience/SKILL.md` · upstream prerequisite · audiences cartographiées canonical refs
- `.skills/skills/mine-voc/SKILL.md` · upstream optional · validation perception client (perceived category)
- `.skills/skills/mine-vom/SKILL.md` · upstream optional · cartographie competitive white-spaces
- `.skills/skills/define-brand-voice/SKILL.md` · sister Sprint v2.80 · brand voice canon downstream consume positioning
- `.skills/skills/validate-brand-voice-consistency/SKILL.md` · downstream consumer cross-touchpoint validation
- `.skills/skills/produce-strategy/SKILL.md` · sister · business strategy goals/financials/channels (distinct scope)
- `.skills/skills/produce-paid-angles/SKILL.md` · downstream consumer · angles paid héritent positioning + audiences
- `.skills/write-to-context.py` · canonical mutation channel
- `.skills/finalize-mutation-batch.py` · mandatory post-acceptance flush
- `.skills/build-brand-snapshot.py` · snapshot rebuild post-mutation

---
