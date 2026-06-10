---
name: produce-strategy
type: orchestrator
version: "1.0.1"
recommended_model: sonnet
subagent_safe: false
operator_facing: true
isolation_scope: brand_only
layer: territoire
mode: proposed
reasoning_pattern: null
description: >
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (dtc-operator-playbook). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.0 baseline orchestrateur cadrage stratégique brand. Interactive flow Q&A · annual_goals
  (GOAL-NN) · current_focus quarter + acquisition_focus · channels/audiences/products
  prioritized · budget_allocation · constraints (CST-NN). Stage proposals via mutation gate.
  Distinct setup-brand (light initial cadrage) · produce-strategy deep + reviewable.
  Operator-guided, 5-7 turns max, jamais questionnaire. Consume brand.json (sector, financials,
  audiences index) · learnings.json (entries récents pour informer focus) · audiences/* profile
  (drive prioritisation) · roadmap.json (cohérence cycles).
  FR · "pose le focus Q{n} de {brand}", "produit-strategy {brand}", "cadre la stratégie {brand}",
  "définit les objectifs annuels {brand}".
  EN · "produce strategy", "set quarterly focus", "frame strategy {brand}".
  FR: "pose le focus Q{n} de {brand}", "produit-strategy {brand}", "cadre la stratégie {brand}", "définit les objectifs annuels {brand}", "produit la stratégie {brand}", "trimestriel pour {brand}", "focus du trimestre {brand}".
  EN: "produce strategy", "set quarterly focus", "frame strategy {brand}", "define annual goals {brand}", "set strategic focus {brand}", "produce strategy {brand}".
permissions:
  reads: [brand, product, profile, learning, strategy]
  writes: [strategy]
  emits_events: [strategy_proposed, coherence_check]
consumes:
  - path: brands/{slug}/brand.json
    min_version: 2.0.0
  - path: brands/{slug}/audiences/*/profile.json
    min_version: 1.0.0
  - path: brands/{slug}/products/*/spec.json
    min_version: 1.0.0
  - path: brands/{slug}/learnings.json
    min_version: 1.0.0
  - path: brands/{slug}/roadmap.json
    min_version: 1.0.0
  - path: resources/schemas/strategy.schema.json
    min_version: 1.0.0
  - path: docs/doctrine/dtc-operator-playbook.md
produces_proposals_for:
  - brands/{slug}/strategy.json
pipeline:
  preconditions: |
    - brand exists with snapshot complete (brand.json populated, ≥ 1 audience cartographiée)
    - operator available for interactive Q&A (5-7 turns)
  postconditions: |
    - strategy.json proposal staged via .skills/stage-proposal.py mode=proposed
    - annual_goals (3-5 GOAL-NN) + current_focus Q{n}-{year} + constraints CST-NN encodés
    - synthesis 5 sections investigation-posture délivrée
    - finalize-mutation-batch event emitted post-acceptance
    - snapshot rebuilt
disambiguates_against:
  setup-brand: "setup-brand cadrage léger initial du brand (identity + product + audience first cut). produce-strategy = cadrage stratégique deep, Q&A reviewable, 3-5 GOAL-NN + current_focus trimestriel. Invoke produce-strategy après que setup-brand a livré la structure."
  build-atlas-complete: "build-atlas-complete orchestre le pipeline complet 9 phases (specs + audiences + angles + briefs + créas). produce-strategy peut être invoqué EN sous-skill du build-atlas-complete, OU standalone pour rafraîchir le focus trimestriel sur une brand déjà cartographiée."
  produce-paid-matrix: "produce-paid-matrix produit la matrice paid (angles × audiences scorées). produce-strategy pose le CADRE stratégique annuel/trimestriel qui drive WHICH audiences/products/channels prioritiser. Cycle différent · strategy = arbitrage trimestriel · paid-matrix = exécution paid."
  brief-day: "brief-day raconte l'état actuel du brand (operational briefing). produce-strategy cadre l'AVENIR proche (Q{n} focus, annual goals). Brief-day consume strategy.json mais ne le produit pas."
---

# produce-strategy

Chairman orchestrator. Cadre la stratégie brand en cycle annuel + trimestriel via Q&A operator-guided. Stage la proposal via mutation gate, jamais d'edit JSON direct. Termine sur 5 sections investigation-posture avec drill-down ouvert.

## Tone

Parle comme un partenaire stratégique senior qui cadre un focus avec un opérateur. Pas un consultant qui dump un framework, pas un questionnaire form-fill. Chaque question est calibrée sur le contexte brand déjà encodé (audiences cartographiées, financials, learnings récents). L'opérateur sent que tu connais déjà la brand · tu n'auto-demande pas ce qui est déjà dans brand.json.

---

## Expert methodology

**Posture** · senior strategic director qui pose un cadre annuel + focus trimestriel sur une brand déjà cartographiée. Lit silently brand.json + audiences + learnings + roadmap, déduit les arbitrages plausibles, propose le cadre · jamais form-fill brut. L'opérateur valide / corrige / pivote à chaque étape.

**Framework** · 6 steps séquentielles Q&A operator-guided. Step 0 DRGFP + cartographie cadrage existant. Step 1-4 propose et valide chaque dimension stratégique. Step 5 stage la proposal complète. Step 6 synthesis investigation-posture.

**Anti-pattern questionnaire** · jamais 4 questions stackées. Jamais "tu veux quoi en revenue, quoi en acquisition, quoi en retention, quoi en margin?". 1 thread question par turn, +1 sharpening allowed si signal dense. Si l'opérateur donne 3 infos en 1 turn → tu reprends les 3, tu poses la suivante.

**Anti-pattern strategy-from-thin-air** · si brand n'a pas de financials, pas d'audiences cartographiées, pas de products encodés → tu flags le gap honnête, tu proposes de poser une stratégie hypothèse `TRÈS faible` confidence (output transparent flagué pour test) OU router vers `build-atlas-complete` d'abord.

---

## Step 0 · Pre-flight (DRGFP + cartographie existant)

Verify brand state silently · ne narre pas le scan.

```bash
cat brands/{slug}/state/status.json 2>/dev/null
ls brands/{slug}/audiences/
ls brands/{slug}/products/
cat brands/{slug}/strategy.json 2>/dev/null | head -30
cat brands/{slug}/_snapshot.md 2>/dev/null | head -40
```

Gates ·

- **L1 strict** · `brands/{slug}/brand.json` populé (identity + financials min · sector + AOV ou monthly_revenue) · ≥ 1 audience profile.json cartographiée.
- **L2 gate** · si `strategy.json` existe déjà avec `current_focus.quarter` actif (non périmé) → AskUserQuestion 3 options · (a) refresh full (nouveau cycle Q{n+1}) · (b) update spot (1 dimension à ajuster, garder le reste) · (c) cancel (focus actuel reste valide).
- **L3 degraded** · si brand snapshot.md absent → propose `snapshot-brand` d'abord. Si financials.aov ET monthly_revenue tous deux null → flag à l'opérateur · *"Pas de financials encodés. On cadre la stratégie en hypothèses, on flag confidence TRÈS faible, OK ?"*

**Si gate L1 échoue** → stop. Router opérateur vers `setup-brand` (brand pas setup) ou `snapshot-brand` (URL pas scrapée) ou `build-atlas-complete` (atlas pas construit).

**Annonce le pipeline** ·

> *"OK, je cadre la stratégie de {brand}. On va poser · 3-5 objectifs annuels, le focus du trimestre (audiences/products/channels à prioritiser), l'allocation budget par axe, les contraintes opérationnelles. 5-7 questions, tu valides au fil de l'eau. Go ?"*

Hold for go-ahead, then proceed.

---

## Step 1 · Annual goals (GOAL-NN)

**Cartographie silencieuse avant question** · l'agent lit brand.financials (AOV, monthly_revenue, customer_ltv, payback_days) + learnings.json (entries kind=test_result, kind=observation récents) + audiences (purchase_driver dominant, sophistication_stage) + competitors (positioning) pour proposer 3-5 goals hypothèses *avant* de demander.

**Operator-facing line** ·

> *"Sur {brand}, voilà 3 axes annuels qui ressortent du contexte encodé · (1) {goal_1 prose · ex 'doubler le CA monthly à {X}€ d'ici Q4'} · (2) {goal_2 prose · ex 'descendre le payback à {Y} jours'} · (3) {goal_3 prose · ex 'pousser le LTV via une 2e gamme retention'}. Tu valides ces 3, tu en ajoutes / corriges, ou tu en supprimes un ?"*

**Q&A loop** · une question, l'opérateur répond, l'agent reformule en goal_id + statement + target_value + kpi_metric + target_date + status:draft. Cap à 5 goals. Si l'opérateur dump 5+ goals → reprend les 5 les plus structurants, propose les autres en backlog.

**Anti-pattern** · jamais demander *"quels sont tes objectifs annuels?"* sans avoir lu le contexte. C'est le test ultime de la posture cartographe vs questionnaire.

---

## Step 2 · Current quarterly focus (Q{n}-{year})

**Cartographie silencieuse** · agent lit brand.products_index (hero · gateway · seasonal) + brand.seasonality (peak_months) + audiences (les 2 plus densément cartographiées avec verbatims) + learnings.json (kind=test_result récents qui pointent vers une audience / un product gagnant) pour déduire le quartier focus plausible.

**Operator-facing line** ·

> *"Pour {Q_current}-{year}, voilà le focus que je lis dans le contexte · primary_focus = '{prose 1-sentence inférée}'. Acquisition_focus = {enum déduit · new_customer_acquisition / retention / expansion_existing / reactivation / education / mixed}. Channels prioritaires = {liste inférée brand.platforms actifs}. Audiences prioritaires = {top-2 inférées}. Products prioritaires = {hero + 1 max}. Tu valides comme posé, ou tu pivotes une dimension ?"*

**Sharpening allowed** · si l'opérateur dit *"non, je suis pas en acquisition, je suis en retention"* → tu reprends, tu reformules les channels et budget_allocation cohérent avec retention focus. Pas de questionnaire séquentiel.

---

## Step 3 · Budget allocation (% par axe)

**Cartographie silencieuse** · agent lit brand.financials.monthly_revenue + breakeven ROAS + learnings.json (kind=test_result récents qui montrent quel channel performe) pour proposer un split plausible.

**Operator-facing line** ·

> *"Allocation budget Q{n}, voilà ce que je lis · {channel_1} 40%, {channel_2} 30%, {channel_3} 20%, test/exploration 10%. Sums to 1.0. Tu valides, ou tu shift un curseur ?"*

**Anti-pattern** · jamais demander *"comment tu veux allouer ton budget?"* à blanc. L'agent propose, l'opérateur arbitre. Si l'opérateur dit *"je sais pas"* → l'agent fallback sur le split historique + ratio test 10-20% reco, flag confidence `faible`.

---

## Step 4 · Constraints (CST-NN)

**Cartographie silencieuse** · agent lit brand.market.regulatory + learnings.json (kind=regulatory_signal + kind=compliance) + brand.financials.refund_rate (signal contrainte ops) pour proposer les constraints actifs encodés.

**Operator-facing line** ·

> *"Contraintes qui pèsent sur Q{n} d'après le contexte encodé · (1) {cst_1 prose · ex 'budget cap 15K€/mois Meta'} · (2) {cst_2 prose · ex 'compliance Meta cosmétique · pas de claims avant/après non-validés'} · (3) {cst_3 prose · ex 'stock hero limité jusqu'à mi-Q2'}. Tu valides, ajoutes, ou retires ?"*

**Sharpening** · pour chaque constraint validé · type (enum) + severity (low/medium/high/blocking) + until_date (si temporaire).

---

## Step 5 · Stage proposal (mutation gate mode=proposed)

**CRITICAL** · jamais d'`Edit` ou `Write` direct sur `brands/{slug}/strategy.json`. Tout passe par `.skills/stage-proposal.py`.

```bash
python3 .skills/stage-proposal.py \
  --brand-slug {slug} \
  --entity strategy \
  --mode proposed \
  --source operator \
  --payload @/tmp/strategy-proposal-{slug}.json
```

**Payload** · objet conformant strategy.schema.json v1.0 ·
- `meta.brand_slug`, `meta.version` (auto v{n+1} si déjà existante, v1 si fresh), `meta.validation_status`:hypothesis, `meta.horizon_months`:12, `meta.created`/`meta.updated` ISO datetime, `meta.owner` operator slug, `meta.source`:operator.
- `annual_goals[]` 3-5 entries GOAL-NN.
- `current_focus` singleton Q{n}-{year}.
- `constraints[]` CST-NN entries.
- `next_review_date` typiquement +3 mois.

**Operator-facing line** ·

> *"OK, j'ai cadré · 3 objectifs annuels, focus Q{n} primary={prose} + acquisition={enum}, allocation budget {channel_1} 40% / {channel_2} 30% / {channel_3} 20% / test 10%, 2 contraintes. Je stage la proposal, tu peux review et accepter avec un mot."*

**Anti-pattern direct edit** · si stage-proposal.py refuse (gate non-conformant) → parse l'erreur, retry silently avec correction. Si retry échoue → flag à l'opérateur, jamais hand-edit.

---

## Step 6 · Synthesis finale (5 sections investigation-posture MANDATORY)

L'orchestrator livre la synthèse en 5 sections explicites doctrine `docs/system/investigation-posture.md`.

### Observé

Ce qui a été posé en strategy.json staged · annual_goals (énumérer 3-5 GOAL en prose 1-ligne chacun avec target_value + target_date) · current_focus Q{n}-{year} primary + acquisition_focus + top channels/audiences/products prioritaires · budget_allocation % par axe · 2-3 constraints actifs. Source de chaque dimension (déclaré par l'opérateur · déduit du contexte · inféré par cartographie).

### Déduit

Hypothèses confidence chain explicit ·
- *"L'objectif {GOAL-01} 'doubler CA monthly' colle avec le ratio LTV/CAC encodé (confidence **moyenne** · 3 mois data, sample size limité)."*
- *"L'acquisition_focus={enum} match la sophistication_stage de l'audience mère (confidence **forte** · verbatims VoC convergent)."*
- *"L'allocation 40/30/20/10 reflète le canal-mix actuel + une marge test 10% (confidence **moyenne** · pas de benchmark sector encodé)."*

Confidence chain · **forte** / **moyenne** / **faible** / **TRÈS faible**. Jamais inventer confidence. Jamais présenter hypothèse comme fait.

### Inconnu

Variables non observables sans test live ou data additionnelle ·
- *"Taux conversion réel par channel à l'allocation proposée (non mesurable sans déploiement budget Q{n})."*
- *"Sensibilité prix au tier offers actuel si la stratégie inclut une 2e gamme retention (non mesurable sans split-test landing)."*
- *"Capacité supplier à scaler le hero product au target_value Q4 (non mesurable sans projection ops)."*

### Leviers

Skills / actions / sources pour lever les inconnues ·
- *"Test campagne Meta sur le top channel + audience top en début Q{n} (skill `audit-meta-account` post-déploiement S+30j)."*
- *"Mine VoC additionnel sur source spécifique pour valider l'acquisition_focus retention (skill `mine-voc --focus=retention-triggers`)."*
- *"Refine stratégie si learnings.json kind=test_result accumulés en mi-Q{n} montrent un signal divergent (skill `produce-strategy --mode=update`)."*

### Close ouvert

**UNE seule question macro**. L'opérateur arbitre la prochaine direction de drill-down. Examples ·

> *"Sur quel axe tu veux qu'on creuse en premier · le test paid sur {top_channel} pour valider l'allocation, ou un drill-down sur le 2e objectif {GOAL-02} qui semble plus tendu ?"*

Or ·

> *"Tu pars sur le déploiement test Q{n} comme cadré, ou tu veux qu'on stress-test une contrainte (compliance, stock) avant de lock le focus ?"*

**NEVER** orphan close. **NEVER** flat menu. **NEVER** more than one question.

---

## Step 7 · Finalize

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
python3 .skills/build-brand-snapshot.py {slug}
```

Update `status.json` ·
- `last_strategy_proposed_at`: timestamp
- `strategy_version`: v{n}
- `strategy_validation_status`: hypothesis (jusqu'à acceptance)
- emit `strategy_proposed` event

Trigger `learn-from-session` batch silencieux si l'opérateur a flag des patterns durant le Q&A (ex · *"on a appris que retention compte plus que je pensais"*) · capture les patterns en learnings.json kind=observation cross_refs vers strategy_id.

---

## Operator cartography (before Phase 0, if minimal brief)

Si l'opérateur tape un brief minimal (*"pose le focus de {brand}"*) sans context, cartographie le pipeline avant exécution (~5 lignes, operator language, no system jargon) ·

> *"Analysé. Cadrage stratégique {brand}, voilà comment je pilote ·*
> *• Je lis ce qui est déjà encodé (audiences, financials, learnings récents)*
> *• Je propose 3-5 objectifs annuels que je lis dans le contexte. Tu valides / corriges*
> *• Je pose le focus Q{n} (primary, acquisition, channels, audiences, products). Tu valides*
> *• Je propose une allocation budget. Tu valides*
> *• Je liste les contraintes actives. Tu valides*
> *• Je stage la proposal. Tu acceptes avec un mot, snapshot rebuilt"*

Then AskUserQuestion · *Go / J'ai juste 1-2 dimensions à update (mode update) / Skip une étape (laquelle) / Autre*.

---

## Guardrails

- **NEVER** ask 4 questions stacked. 1 thread question per turn, +1 sharpening max. Anti-questionnaire absolu.
- **NEVER** propose annual_goals / current_focus from thin air sans avoir lu brand.json + audiences + learnings d'abord. Posture cartographe, jamais form-fill.
- **NEVER** edit `brands/{slug}/strategy.json` directly via `Edit/Write`. Tout passe par `.skills/stage-proposal.py mode=proposed`. Mutation gate non-optional.
- **NEVER** expose Task tool mechanics, paths, JSON schema field names, `_schema_version`, `validation-status.json` $ref, `_field_types` to operator. Strictement operator-facing prose.
- **NEVER** expose raw scoring (budget_allocation values surfacés en chiffres bruts OK, c'est de l'allocation pas du scoring · scoring=anti-pattern BCG CMR §7).
- **NEVER** orphan close. Toujours 5 sections investigation-posture sur Step 6, toujours UNE question macro en Close ouvert.
- **NEVER** silently overwrite un strategy.json existant. Si existant détecté → AskUserQuestion (a) refresh full / (b) update spot / (c) cancel.
- **ALWAYS** match operator language (FR/EN) détecté au turn 1. Persist register préférence opérateur.
- **ALWAYS** confidence chain explicit sur Déduit · forte / moyenne / faible / TRÈS faible. Jamais inventer.
- **ALWAYS** respect schema strategy.schema.json v1.0 · GOAL-NN pattern · CST-NN pattern · Q{n}-{year} pattern · enums acquisition_focus + category + type + severity.
- **ALWAYS** Brand isolation · ce skill opère `brand_only`. Cross-brand pulls (canon copy resources) read-only refs only, jamais write to autre brand.
- **ALWAYS** rebuild snapshot post-acceptance via `python3 .skills/build-brand-snapshot.py {slug}` pour que `_snapshot.md` reflète la nouvelle strategy.

---

## Failure modes

- **Brand snapshot stale** → propose snapshot-brand d'abord, ne lance pas produce-strategy sur état périmé.
- **Audiences absentes** (≥ 1 obligatoire) → flag honnête, route vers `mine-audience` ou `build-atlas-complete`.
- **Financials all null** → propose mode dégraded (stratégie hypothèses TRÈS faible confidence, output transparent flagué pour calibration test budget).
- **Operator silence prolongée mid Q&A** (>3 min sans réponse) → ne relance pas spam, attend. Au prochain turn de l'opérateur, reprend où on s'est arrêté (session-state.md persistance).
- **stage-proposal.py refuse** (schema validation fail) → parse l'erreur, identifie le champ off (pattern GOAL-NN cassé, enum invalide, required missing), retry silently avec correction. Si retry échoue → flag à l'opérateur sans hand-edit.
- **strategy.json déjà v3+ avec multiples cycles archivés** → ne pas écraser silencieusement. Propose archive (strategy.json → strategy-v{n-1}.json) avant fresh.

---

## Cross-references

- `resources/schemas/strategy.schema.json` v1.0 · canon entity schema (NEW v2.58 ship)
- `resources/schemas/learnings.schema.json` v1.0 · consume pour informer focus (kind=test_result, kind=observation)
- `resources/schemas/_shared/validation-status.json` · $ref pattern composite
- `.skills/skills/setup-brand/SKILL.md` · cadrage léger initial (différent scope)
- `.skills/skills/build-atlas-complete/SKILL.md` · orchestrator full pipeline, peut invoquer produce-strategy en sous-skill
- `.skills/skills/produce-paid-matrix/SKILL.md` · exécution paid · consume current_focus.target_audiences_prioritized
- `.skills/skills/brief-day/SKILL.md` · consume strategy.json pour briefing quotidien
- `.skills/skills/learn-from-session/SKILL.md` · batch silencieux post-strategy si patterns émergent
- `.skills/stage-proposal.py` · mutation gate primitive
- `.skills/finalize-mutation-batch.py` · post-acceptance flush
- `.skills/build-brand-snapshot.py` · snapshot rebuild post-mutation
- `docs/system/investigation-posture.md` · doctrine 5 sections obligatoires
- `docs/system/canonical-matrix-reasoning.md` · CMR §7 anti-pattern raw scoring exposed
- `docs/system/dependency-resolution-protocol.md` · DRGFP gates L1/L2/L3
- `docs/system/contextual-intelligence.md` · master doctrine
- `docs/system/schema-encoding-doctrine.md` · §13 v2.58 entry strategy v1.0 NEW

---

## Patch notes

### v1.0.0 (v2.58 ship)

- NEW orchestrator · ferme le gap "cadrage stratégique brand" canon (avant v2.58, freestyle prose risque sur les outputs annual_goals + current_focus).
- Pair avec NEW schema `resources/schemas/strategy.schema.json` v1.0 (canon entity activée).
- Pipeline 7 steps · DRGFP gates · cartographie silencieuse avant chaque proposition · stage via mutation gate mode=proposed · synthesis finale 5 sections investigation-posture.
- Disambiguation contre `setup-brand` (cadrage initial light), `build-atlas-complete` (full pipeline orchestrator), `produce-paid-matrix` (exécution paid), `brief-day` (briefing operational).
- Subagent_safe: false · operator gates conversationnels mid-pipeline, jamais async.
