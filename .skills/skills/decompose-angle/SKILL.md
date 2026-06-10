---
name: decompose-angle
type: producer
version: "1.2.0"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
mode: proposed
operator_facing: true
description: >
  v1.2.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · Triangulation cross-canon refactor · spec_activated (products/{p}/spec.json#mechanism_id) + pain_ref (audiences/{a}/pain_points/{PNT-NN}.json) + objection_ref (audiences/{a}/objections/{OBJ-NN}.json) tous canonical sub-audience. Step 4 bridge atoms · benefit_served référence audiences/{audience_slug}/pain_points/{PNT-NN}.json sub-audience. Step 2 tension atoms · reason_blocked référence audiences/{audience_slug}/objections/{OBJ-NN}.json sub-audience. Step 2 observation atom · phenomenon source canonical depuis sub-audience pain_points verbatim_quotes. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.1.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · Step 4 bridge atoms refactor · benefit_served peut désormais référencer `pain_points/{PNT-NN}.json` collection (PNT-NN ref si la formula bridge résout un pain canonical). Step 2 tension atoms · reason_blocked peut référencer `objections/{OBJ-NN}.json` collection (OBJ-NN si tension est une objection cartographiée). Triangulation cross-canon · spec_activated + pain_ref + objection_ref tous canonical. Backward compat lecture profile.pain_points[] + profile.objections[] legacy preserved (pre-v2.63 brands).
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.0.0 (angle.schema v1.2 design intent honored). Sub-skill atomique deep enrichment
  de `brands/{slug}/angles/{ANG-NN}.json` · light pass formula (Observation + Tension +
  Reframe + Bridge, one-line summary chacun) produit par `produce-paid-angles` → deep pass
  atoms (3+ atoms par component · phenomenon, source, sample_size, state_actual, state_desired,
  reason_blocked, perceptual_pivot, pivot_mechanism, spec_activated, benefit_served,
  promise_formulated). Distinct de `decompose-ad` (reverse-engineer competitor ad existante).
  Pattern atlas brand · l'opérateur peut creuser un angle stratégique pour drill un brief
  copywriter solide avant `produce-copy-brief`. Canon spec.json triangulation · `spec_activated`
  DOIT référencer `spec.mechanism_id` OR `spec.benefit_id` existant, jamais inventer.
  FR · "décompose l'angle {ANG-NN}", "approfondis cet angle", "deep dive angle {ANG-NN}", "décortique l'angle"
  EN · "decompose angle", "deep dive angle", "enrich angle formula"
  FR: "décompose l'angle {ANG-NN}", "approfondis cet angle", "deep dive angle {ANG-NN}", "décortique l'angle".
  EN: "decompose angle", "deep dive angle", "enrich angle formula".
consumes:
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
permissions:
  reads: [brand, product, profile]
  writes: [learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists, angle ANG-NN exists at brands/{slug}/angles/{ANG-NN}.json with formula light pass populated
  postconditions: formula deep atoms enriched, finalize-mutation-batch event emitted
disambiguates_against:
  decompose-ad: "decompose-ad reverse-engineers an existing COMPETITOR ad (extracts angle from observed creative). decompose-angle enriches an OWN angle already cartographied (deep dive own strategic angle). Route to decompose-ad when operator pastes a competitor ad URL/screenshot; route to decompose-angle when operator references an internal ANG-NN."
  produce-paid-angles: "produce-paid-angles generates the light pass (formula one-line summaries) on a ranked set of N angles for an audience. decompose-angle enriches ONE existing angle in depth. Route to produce-paid-angles when no angles exist yet; route to decompose-angle when operator wants to drill ONE angle."
  produce-copy-brief: "produce-copy-brief is the DOWNSTREAM step (one chosen angle → copywriter brief with hook variants + body + CTA). decompose-angle is the prerequisite enrichment if the formula is still light pass. Route to produce-copy-brief when formula atoms are already deep; route to decompose-angle first if atoms are null."
prerequisites:
  - field: brands/{slug}/brand.json
    level: L1
    auto_pull: read_brand
    freshness_ttl_days: 365
  - field: brands/{slug}/angles/{ANG-NN}.json
    level: L1
    auto_pull: read_angle
    block_if_missing: true
  - field: brands/{slug}/audiences/{audience_slug}/profile.json
    level: L1
    auto_pull: read_audience
    freshness_ttl_days: 60
  - field: brands/{slug}/products/{p_slug}/spec.json
    level: L1
    auto_pull: read_spec
    freshness_ttl_days: 90
---

# Skill · decompose-angle

> Atomique deep enrichment d'un angle existant. Light pass formula (4 components one-line) → deep pass atoms (3+ atoms par component, 11 atoms canon au total). Canon spec.json triangulation strict · `spec_activated` réfère un `spec.mechanism_id` OR `spec.benefit_id` existant, jamais inventé.

---

## Tone

Posture d'analyste stratégique, pas de copywriter. Le skill décompose un angle existant en ses atomes constitutifs pour rendre la composition traçable (downstream `produce-copy-brief` peut hériter la chaîne) et pour exposer les atomes flous (à creuser via mining VoC ou ingest founder). Jamais paraphrase narrative déguisée en analyse. Cite verbatim quand un atome est sourcé d'un verbatim VoC.

---

## Expert methodology

**Persona** · senior creative strategist + senior copy director. Sait lire une formula Obs+Tension+Reframe+Bridge et identifier où la matière brute manque (state_actual flou, perceptual_pivot pas calibré, spec_activated invented). Sépare l'observable (sourcé verbatim ou spec) du déduit (inférence à valider).

**Framework** · 11 deep atoms canon de `angle.schema.json` v1.2, formula object ·

| Component | Deep atoms | Source canon attendue |
|---|---|---|
| `formula.observation` | `phenomenon` + `source` + `sample_size` | verbatim VoC / stat clinical / benchmark category |
| `formula.tension` | `state_actual` + `state_desired` + `reason_blocked` | profile.json pain_points + JTBD |
| `formula.reframe` | `perceptual_pivot` + `pivot_mechanism` | analyste · 4 mechanism canon types |
| `formula.bridge` | `spec_activated` + `benefit_served` + `promise_formulated` | spec.json (mechanism_id OR benefit_id) |

**Canon spec triangulation rule** · `spec_activated` et `benefit_served` DOIVENT référencer une entrée existante dans `spec.json#mechanisms[]` (mechanism_id) OR `spec.json#benefits[]` (benefit_id). Jamais inventer une feature pour servir le bridge. Si zéro mechanism / benefit matche le reframe → flag Inconnu et propose `map-mechanisms` OR `ingest-resource`.

---

## Step 0 · DRGFP prerequisite check (canon v2.38+)

1. **L1 silent** · `brands/{slug}/brand.json` + `brands/{slug}/angles/{ANG-NN}.json` doivent exister.
2. **Block-if-missing** · si `angles/{ANG-NN}.json` n'existe pas → refus poli + route opérateur ·

```
Pas d'angle ANG-NN cartographié sur cette brand. Move utile · produce-paid-angles
sur l'audience source (~5 min, ranke 5-7 angles light pass formula), puis je décompose
l'angle de ton choix ici.
```

Stop. Ne pas inventer un angle pour satisfaire la requête.

3. **L1 silent** · `brands/{slug}/audiences/{audience_slug}/profile.json` doit exister (audience_slug lu depuis `angle.audience_slug`).
4. **L1 silent** · `brands/{slug}/products/{p_slug}/spec.json` doit exister (au moins un produit brand). Si multi-produit, lire tous les specs pour matcher spec_activated.
5. **L2 gate** · si `angle.formula` est totalement vide (zéro summary, zéro atom) → refus · l'angle n'a même pas son light pass · re-route vers `produce-paid-angles`.
6. **L3 degraded** · si `audience.profile.json#voice.key_expressions[]` < 5 OR `pain_points[].verbatim_quotes[]` < 5 → flag inline · les atoms `phenomenon`, `state_actual`, `state_desired` resteront partiels (formula-derived plutôt que verbatim-anchored). Propose `mine-voc` upstream.

---

## Step 1 · Read encoded data (v1.2.0 ontologie sémantique pure)

Load silently ·

- `brands/{slug}/angles/{ANG-NN}.json` · 
  - `name`, `audience_slug`, `origin_axis`, `awareness_movement`
  - `formula.observation.summary` (light pass starting point pour atoms)
  - `formula.tension.summary`, `formula.reframe.summary`, `formula.bridge.summary`
  - `lineage` (canon refs hook/framework/angle/archetype déjà tagués) + **v1.3 NEW** `lineage.pain_ref` + `lineage.objection_ref` (canonical refs PNT-NN + OBJ-NN si populés par produce-paid-angles v1.10+)
  - `insight` si déjà populé
  - `meta.validation_status`

**Sub-audience v2.64 (NEW · ontologie sémantique pure)** ·

- `brands/{slug}/audiences/{audience_slug}/pain_points/*.json` · PNT-NN canonical entities owned natif par parent path (formulation, verbatim_quotes, emotion, trigger, chain, severity). Source de vérité pour Step 4 bridge atom `benefit_served` ref PNT-NN si formula bridge résout un pain canonical. Source de vérité Step 2 observation atom `phenomenon` source canonical.
- `brands/{slug}/audiences/{audience_slug}/objections/*.json` · OBJ-NN canonical entities owned natif (formulation, type, response_counter, lifecycle_stage). Source de vérité Step 3 tension atom `reason_blocked` ref OBJ-NN si tension est une objection cartographiée.

**Backward compat lecture (v2.63 brands)** · si sub-audience pain_points/objections n'existent pas, fallback top-level `brands/{slug}/pain_points/*.json` + `brands/{slug}/objections/*.json` filtered by `affected_audiences[]` contains `{audience_slug}`.

**Backward compat lecture (pre-v2.63 brands)** · si top-level absent aussi, fallback `audiences/{audience_slug}/profile.json#pain_points[]` + `profile.json#objections[]` (legacy sub-fields v1.7). Skip ref canonical (text-only sourcing).

**Audience profile (toujours lu)** ·

- `brands/{slug}/audiences/{audience_slug}/profile.json` ·
  - `voice.key_expressions[]` (corpus pour phenomenon + state_actual)
  - `psychology.jtbd` (functional + emotional + social)
  - `market_position.awareness_dominant` (RENAME C1 profile/2.3, ex awareness_level)
  - **Backward compat** · `pain_points[]` + `objections[]` sub-fields legacy preserved en lecture, mais sub-audience collections prennent priorité si présentes.

- `brands/{slug}/products/{p_slug}/spec.json` ·
  - `mechanisms[]` (mechanism_id, name, target, mode_of_action · canon pour spec_activated)
  - `benefits[]` (benefit_id, benefit, chain · canon pour benefit_served)
  - `problems_solved[]` (verbatim_quotes · corpus pour observation.phenomenon)
- Canon copy refs déjà taguées dans `angle.lineage` (hook_canon_id, framework_canon_id, angle_canon_id, archetype_canon_id).

---

## Step 2 · Décomposer `formula.observation` en atoms

3 deep atoms canon · `phenomenon` + `source` + `sample_size`.

### 2.1 · `phenomenon` (fact observé)

Le fait observable que l'audience perçoit déjà OU pourrait voir si on le lui montre. Source priority ·
1. Verbatim direct dans `audience.profile.voice.key_expressions[]` · phenomenon = formulation literal du verbatim.
2. **v2.64 NEW sub-audience** `audiences/{audience_slug}/pain_points/{PNT-NN}.json#verbatim_quotes[]` canonical sub-audience · phenomenon = adaptation 2-4 mots du verbatim PNT-NN. Source canonical traçable. Backward compat fallback top-level `pain_points/{PNT-NN}.json#verbatim_quotes[]` v2.63 si sub-audience vide. Fallback v1.7 · `profile.pain_points[].verbatim_quotes[]` legacy sub-field.
3. Stat clinical depuis `spec.proofs.scientific` · phenomenon = la stat formulée plain language.
4. Benchmark category (mention dans `brand.json#market.external_intelligence`).
5. Inférence si zéro support → flag formula-derived, downgrade confidence atom.

### 2.2 · `source` (where this fact lives)

Free polysemic field (par design v1.2, distinct de top-level `origin_axis`). Examples ·
- `"Trustpilot {brand_slug}, 14 reviews citant {expression}"`
- `"Reddit r/skincare, 8 posts thread {topic}"`
- `"Audience profile.json voice.key_expressions VOC-trustpilot-7a2x sample_size 12"`
- `"Spec proofs.scientific Lopresti et al. 2019 NCT03088787"`
- `"Self-reported in audience.psychology.emotions[] dominant"`

### 2.3 · `sample_size` (integer si applicable)

Nombre de verbatims OR data points qui supportent le phenomenon. Null si non quantifiable (e.g. stat clinical ponctuelle, ou stat-benchmark category).

---

## Step 3 · Décomposer `formula.tension` en atoms

3 deep atoms canon · `state_actual` + `state_desired` + `reason_blocked`.

### 3.1 · `state_actual` (situation actuelle audience)

Ce que l'audience expérimente aujourd'hui. Source priority ·
1. `audience.psychology.emotions[]` dominant + **v2.64 NEW sub-audience** `audiences/{audience_slug}/pain_points/{PNT-NN}.json#formulation` (sub-audience canonical) principal · fallback v2.63 top-level `pain_points/{PNT-NN}.json#formulation` filtered audience · fallback v1.7 legacy `profile.pain_points[].formulation`.
2. `audience.jtbd.functional` négatif (ce que le job échoue à délivrer aujourd'hui).
3. Verbatim direct (priorité absolue si dispo).

### 3.2 · `state_desired` (situation visée)

Ce que l'audience aspire à atteindre. Source priority ·
1. `audience.jtbd.emotional` + `social` (aspiration identitaire + projection sociale).
2. `audience.psychology.identity_drivers[]` si encodé.
3. Inférence depuis pain inversé (si pain = "ballonnement permanent", desired = "ventre plat sans inconfort") · confidence moyenne.

### 3.3 · `reason_blocked` (friction qui bloque le passage)

La raison pour laquelle le gap state_actual → state_desired n'est pas franchi. 3 types canon ·
- **External obstacle** · contrainte matérielle (prix, temps, accessibilité). Source · `objections/*.json` (collection top-level v2.63) `type="cost"` ou `"access"` · fallback legacy `audience.objections[]`.
- **Internal belief** · croyance limitante. Source · `objections/*.json` `type="scepticism"` ou `"self-doubt"` · fallback legacy `audience.objections[]`.
- **Lack of awareness** · manque d'information sur la solution. Source · `audience.market_position.awareness_dominant` problem-aware ou solution-aware (pas product-aware).

**Canonical ref OBJ-NN (v1.1.0 NEW · v2.63 ontologie pure)** · si la friction match une objection canonique dans `objections/*.json`, stage atom enrichi avec `reason_blocked.objection_ref: "OBJ-NN"` canonical (en plus du `reason_blocked.type` enum). Persist via mutation gate path · `angles/{ANG-NN}.json#/formula/tension/reason_blocked_objection_ref`. Triangulation cross-canon · downstream `produce-copy-brief` peut drill direct l'objection canonique + son `response_counter` cristallisé. Backward compat (pre-v2.63) · skip canonical ref, type enum seul.

---

## Step 4 · Décomposer `formula.reframe` en atoms

2 deep atoms canon · `perceptual_pivot` + `pivot_mechanism`.

### 4.1 · `perceptual_pivot` (before/after de la perception)

Le shift de perception clé que l'angle propose. Formulation canon · *"L'audience voit aujourd'hui X. Après l'angle, l'audience voit X comme Y."*

Examples ·
- *"Les régimes échouent" → "Les régimes échouent parce que ton microbiote est dysbiotique" (shift: cause externe → cause interne)*
- *"Mon front se dégarnit" → "Mon front se dégarnit parce que le follicule manque de KGF" (shift: fatalité → biochimie réversible)*
- *"Le yoga c'est mou" → "Le yoga c'est la seule discipline qui synchronise nerveux + musculaire" (shift: faible intensité → leverage neurophysiologique)*

### 4.2 · `pivot_mechanism` (rhetorical mechanism canon)

4 mechanism types canon · `revelation | comparison | contrarian | inversion`. Définition ·

- **revelation** · révéler une cause cachée que l'audience ne connaissait pas. *"Les régimes échouent parce que le microbiote..."*. Force · transforme awareness problem-aware → solution-aware. Risque · over-claim si la révélation manque de support clinical.
- **comparison** · positionner contre une alternative dominante. *"Les régimes durent 3 mois, ce probiotique agit en 21j."*. Force · directe, lisible. Risque · ad-hoc si la comparaison n'est pas symétrique.
- **contrarian** · inverser la sagesse conventionnelle. *"Ne mange plus moins, mange plus tôt."*. Force · pattern interrupt fort. Risque · backfire si l'audience est déjà sceptique.
- **inversion** · retourner le problème en levier. *"Ton stress n'est pas une faiblesse, c'est ton signal d'adaptation."*. Force · identitaire. Risque · prétentieux si pas ancré.

Source canon · `resources/canon/copy/angles/{mechanism}.json` si lineage déjà tagué, sinon mapping analytique.

---

## Step 5 · Décomposer `formula.bridge` en atoms

3 deep atoms canon · `spec_activated` + `benefit_served` + `promise_formulated`. **Triangulation spec.json strict.**

### 5.1 · `spec_activated` (mechanism_id OR benefit_id)

Reference vers le spec qui matérialise le reframe. Triangulation canon ·
1. Lire `spec.json#mechanisms[]` · matcher le mechanism qui correspond au `pivot_mechanism` (e.g. reframe "ton microbiote dysbiotique" → spec_activated = MEC-{N} où `mechanism.target = "microbiote intestinal"`).
2. Si zéro mechanism match → lire `spec.json#benefits[]` · matcher le benefit qui sert le reframe.
3. Hard rule · `spec_activated` est UN identifier canonique (`MEC-NN` ou `BEN-NN`), pas une phrase libre. Si zéro match → laisser null + flag Section 3 Inconnu + propose `map-mechanisms` upstream pour enrichir spec.

### 5.2 · `benefit_served` (benefit_id + optional pain_ref canonical)

Reference vers le benefit que la promise délivre. Lire `spec.json#benefits[]` · matcher le benefit dont le `chain[]` (functional → emotional → identity) résonne avec le `state_desired` de la tension.

Hard rule · `benefit_served` est UN `benefit_id` (`BEN-NN`), pas une phrase libre.

**Canonical ref PNT-NN (v1.1.0 NEW · v2.63 ontologie pure)** · si la formula bridge résout un pain canonical (i.e. le `state_desired` matche l'inverse d'un PNT-NN dans `pain_points/*.json` filtered audience), stage atom enrichi avec `bridge.pain_ref: "PNT-NN"` canonical (cross-ref pain résolu par bridge). Persist via mutation gate path · `angles/{ANG-NN}.json#/formula/bridge/pain_ref`. Triangulation cross-canon complète · `spec_activated` (BEN-NN ou MEC-NN canonical spec) + `benefit_served` (BEN-NN canonical spec) + `pain_ref` (PNT-NN canonical pain) tous traçables. Downstream `produce-copy-brief` peut composer brief avec PNT-NN ID inline + drill verbatim_quotes directs. Backward compat (pre-v2.63) · skip canonical ref, benefit_served seul.

### 5.3 · `promise_formulated` (formulation textuelle de la promise)

La promise finale que l'audience walks away avec. Formulation plain language opérateur. Examples ·
- *"Retrouve un ventre plat en 21j sans changer ton alimentation"*
- *"Stoppe ton recul frontal en 90j avec le complexe KGF-Procapil"*
- *"Synchronise ton nerveux + musculaire en 8 sem, le yoga qui replace le sport"*

Hard rule · la promise doit être cohérente cross-component · `state_desired` (de Tension) + `pivot_mechanism` (de Reframe) + `benefit_served` (canon) → promise formulée tient les 3 fils sans contradiction.

---

## Step 6 · Stage chaque atom enrichi via mutation gate

Per atom enrichi, stage proposal ·

```bash
python3 .skills/write-to-context.py \
  --path "angles/{ANG-NN}.json#/formula/observation/phenomenon" \
  --value "{phenomenon_value}" \
  --source agent \
  --confidence {0.5-0.9 selon sourcing} \
  --mode proposed \
  --reason "decompose-angle deep enrichment · {brief rationale}"
```

Répéter pour les 11 atoms canon · phenomenon, source, sample_size, state_actual, state_desired, reason_blocked, perceptual_pivot, pivot_mechanism, spec_activated, benefit_served, promise_formulated.

**Canonical refs v1.1.0 (v2.63 ontologie pure)** · 2 paths additionnels SI canonical match détecté ·

```bash
# Tension.reason_blocked canonical objection ref
python3 .skills/write-to-context.py \
  --path "angles/{ANG-NN}.json#/formula/tension/reason_blocked_objection_ref" \
  --value "OBJ-{NN}" \
  --source agent \
  --confidence 0.9 \
  --mode proposed \
  --reason "decompose-angle canonical objection triangulation v2.63"

# Bridge.pain_ref canonical pain ref
python3 .skills/write-to-context.py \
  --path "angles/{ANG-NN}.json#/formula/bridge/pain_ref" \
  --value "PNT-{NN}" \
  --source agent \
  --confidence 0.9 \
  --mode proposed \
  --reason "decompose-angle canonical pain triangulation v2.63"
```

Skip silencieusement si zéro match canonical (pre-v2.63 brand OR formula-derived sur pain/objection hors collection).

**Confidence calibration** ·

| Sourcing | Confidence |
|---|---|
| Verbatim direct sourced (key_expression sample_size ≥ 5) | 0.85-0.9 |
| Verbatim semantic match (verbatim_quote pain_points) | 0.75-0.8 |
| Stat clinical citée dans spec.proofs.scientific | 0.85 |
| Spec ref direct (mechanism_id ou benefit_id existant) | 0.9 |
| Inference logique sourcée audience.psychology | 0.6-0.7 |
| Formula-derived (zéro verbatim direct, mapping canonique) | 0.5-0.55 |

---

## Step 7 · Synthesis 5 sections (investigation posture canon v2.54+)

### Section 1 · Observé (faits sourcés)

> *Observé · {N atoms} sourcés direct · ANG-NN {angle.name} · {date}*

Lister les atoms enrichis avec source directe (verbatim sample_size ≥ 5, spec ref canonique, clinical stat citée) ·

- **Observation** · phenomenon · `"{verbatim}"` · source · audience VoC `{ref VOC-id}`, sample_size {N}.
- **Tension** · state_actual · `"{verbatim adapté}"` (audience pain principal sourcé) · state_desired · `"{jtbd.emotional formulation}"` · reason_blocked · `{type}` sourcé `audience.objections[].formulation`.
- **Reframe** · pivot_mechanism · `{type canon}` (sourcé `angle.lineage.angle_canon_id`).
- **Bridge** · spec_activated · `{MEC-NN ou BEN-NN}` (canon spec.json) · benefit_served · `{BEN-NN}` (canon spec.json).

### Section 2 · Déduit (hypothèses avec confidence chain)

> *Déduit · {N atoms} en hypothèse à valider*

Atoms qui sont inférés à partir d'observable sans verbatim direct ·

- **Tension** · state_desired · formulation `{value}` (confidence moyenne · inférence depuis `audience.jtbd.emotional`, pas de verbatim direct attestant l'aspiration formulée). Question · *"Cette aspiration matche bien ton audience, ou tu veux qu'on capture des verbatims via `mine-voc` avant de fixer ?"*
- **Reframe** · perceptual_pivot · formulation `{value}` (confidence moyenne · construit analytique, pas testé en VoC). Question · *"On test ce pivot tel quel en paid (~50€/angle), ou tu veux qu'on l'ajuste après audit concurrent ?"*
- **Bridge** · promise_formulated · formulation `{value}` (confidence forte sur cohérence cross-component, moyenne sur résonance audience). Question · *"Cette promise tient les 3 fils (state_desired + pivot + benefit), reste à valider si l'audience la formule comme ça."*

### Section 3 · Inconnu (atoms qui restent flous)

> *Inconnu · {N variables} à creuser*

Atoms qui ne peuvent pas être enrichis sans matière supplémentaire ·

- **Bridge** · spec_activated · zéro mechanism match dans `spec.json#mechanisms[]` pour le reframe `{pivot}`. Move · `map-mechanisms` pour cartographier les mechanisms du produit en deep (target + mode_of_action), peut révéler un MEC-NN qui matche.
- **Observation** · sample_size null sur phenomenon `{phenomenon}` · audience profile.json voice trop fin (< 5 verbatims). Move · `mine-voc` sur audience cible (~15 min, capture verbatims denses).
- **Tension** · reason_blocked ambigu · entre "internal belief" et "lack of awareness", `audience.objections[]` ne distingue pas. Move · `ingest-resource` sur Trustpilot brand + concurrent direct (~5 min).

### Section 4 · Leviers (drill-down options · opérateur arbitre)

> *Leviers · {N axes} d'investigation prioritaires*

- **Axe A · Enrichir spec.mechanisms[]** (lève Inconnu Bridge.spec_activated) · `map-mechanisms` sur produit canonique, expose MEC-NN candidats pour le reframe. ~10 min.
- **Axe B · Densifier voice client** (lève Inconnu Observation.sample_size + Déduit Tension.state_desired) · `mine-voc` sur audience cible. ~15 min.
- **Axe C · Router downstream brief copywriter** (si atoms acceptables) · `produce-copy-brief ANG-NN` consume les atoms enrichis pour drill hook variants + body + CTA. ~5 min.

### Section 5 · Close ouvert (UNE question macro)

> Sur ANG-{NN} `{name}` ({N} atoms sourcés direct + {M} en hypothèse + {K} flous), deux moves possibles ·
>
> A · Lever les Inconnus d'abord (Axe A + Axe B) · upgrade les atoms flous à `forte` ou `moyenne` sourcé, puis route brief copywriter avec une formula entièrement traçable. Pertinent si l'angle vise scale paid > 5k€ ou positioning institutionnel.
> B · Router brief copywriter direct (Axe C) · accept les atoms `moyenne` agrégée, produce-copy-brief consume tel quel, test paid budget calibré (~50-100€/angle, 5-7j data). Pertinent si deadline serrée OR test exploratoire avant scale.
> C · {3e option si pertinente · ex "Décomposer un autre angle ANG-MM en parallèle pour comparer les deep formulas, choisir le meilleur pour brief copywriter"}
>
> Mon avis · {reco adaptive · si Bridge.spec_activated null → A critique (l'angle perd sa traçabilité produit) · si claim sourcing majoritairement `forte` → B valide direct · si majoritairement `moyenne` mais audience verbatim_density solide → B avec budget calibré}.

---

## Step 8 · Finalize

Mandatory avant output operator-facing ·

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Exit code 2 → blocking, revise. Exit code 0 → ship.

---

## Hard rules

- **Canon spec.json triangulation strict.** `spec_activated` et `benefit_served` DOIVENT référencer un `mechanism_id` OR `benefit_id` existant dans `spec.json`. JAMAIS inventer une feature pour servir le bridge. Si zéro match → null + flag Inconnu + propose `map-mechanisms` upstream.
- **Backward compat strict.** Le `formula.{component}.summary` light pass existing reste intact. Seuls les atoms (phenomenon, state_actual, etc.) sont enrichis. Jamais overwrite un atom operator-stated.
- **Verbatim jamais inventé.** Si zéro verbatim direct dans `audience.voice.key_expressions[]` ou `pain_points[].verbatim_quotes[]`, l'atom phenomenon ship en formula-derived avec confidence ≤ 0.55 + flag Section 2.
- **Cohérence cross-component obligatoire.** La promise_formulated doit tenir les 3 fils · state_desired (Tension) + pivot_mechanism (Reframe) + benefit_served (canon spec). Si incohérence détectée → flag Section 3 Inconnu + propose iteration sur l'atom incohérent.
- **5 sections explicites, jamais fusionnées en prose continue.** Anti-pattern AP-6 doctrine.
- **Confidence chain visible Section 2.** Chaque hypothèse · forte / moyenne / faible / TRÈS faible + indicateur source.
- **Close ouvert UNE question.** Jamais affirmatif (*"On y va ?"*, *"Brief copywriter ?"*). Toujours drill-down macro avec 2-3 options + reco adaptive.
- **`finalize-mutation-batch` mandatory.** Step 8 non-skippable.
- **DRGFP block-if-missing.** Si `angles/{ANG-NN}.json` n'existe pas OR formula totalement vide → refus poli + route vers `produce-paid-angles`. Pas de fabrication angle pour satisfaire la requête.
- **Operator-facing rule.** JAMAIS exposer field paths (`angles/ANG-03.json#/formula/observation/phenomenon`), JAMAIS exposer confidence numeric (0.65), JAMAIS exposer canon ref id raw (`hook_canon_id: H-curiosity-gap` → dire *"hook curiosity-gap (canon copy)"*). Operateur voit `observé / déduit / inconnu`, jamais l'algèbre derrière.
- **pivot_mechanism enum strict.** `revelation | comparison | contrarian | inversion`. Pas d'extension freestyle. Si le mechanism observé ne match aucun, route `correct-skill` (proposer extension enum, pas freestyle inline).
- **Confidence chain heritée surface.** L'angle porte déjà `lineage.derived_from_audience_confidence` + `derived_from_brand_confidence` + `claim_confidence` (v2.54 produce-paid-angles). decompose-angle ne dégrade pas cette chain ; il enrichit les atoms en respectant la borne supérieure de `claim_confidence`. Atom confidence > `claim_confidence` agrégée = downgrade à `claim_confidence` (algèbre conservative MIN).

---

## Cross-references

- `docs/system/investigation-posture.md` · 5 sections canon, confidence chain explicit, close drill-down macro.
- `docs/system/dependency-resolution-protocol.md` · DRGFP L1/L2/L3 prerequisite check.
- `docs/system/confidence-propagation.md` · algèbre cascade confidence cross-skill (audience → angle → brief), MIN conservative.
- `docs/system/schema-encoding-doctrine.md` · mutation rule, `_field_types`, sourcing tags, atom-level encoding.
- `docs/system/canonical-matrix-reasoning.md` · production 95% qualité, canon-driven.
- `resources/schemas/angle.schema.json` v1.2 · formula deep atoms structure (11 atoms canon).
- `resources/schemas/spec.schema.json` v1.10+ · mechanisms[] + benefits[] · canon refs pour spec_activated + benefit_served.
- `.skills/skills/produce-paid-angles/SKILL.md` · upstream producer du light pass formula.
- `.skills/skills/decompose-ad/SKILL.md` · sibling pour reverse-engineer competitor ad (distinct, voir disambiguates_against).
- `.skills/skills/produce-copy-brief/SKILL.md` · downstream consumer (one chosen angle → brief copywriter avec hook variants).
- `.skills/skills/mine-voc/SKILL.md` · upstream pour densifier voice client (atoms phenomenon + state_actual sourcés).
- `.skills/skills/map-mechanisms/SKILL.md` · sibling sub-skill atlas brand (enrichit spec.mechanisms[] pour unlock Bridge.spec_activated).
- `.skills/skills/ingest-resource/SKILL.md` · source enrichment quand audience profile.json est fin.
- `.skills/write-to-context.py` · canonical mutation channel.
- `.skills/finalize-mutation-batch.py` · mandatory Step 8 primitive.
- `resources/canon/copy/angles/*.json` · canon refs pour pivot_mechanism (revelation/comparison/contrarian/inversion).

---

## Example output · ANG-03 Ras-le-bol des régimes (okr probiotique minceur)

Operator triggers · *"décompose l'angle ANG-03"*

---

ANG-03 `Ras-le-bol des régimes` (audience femme-minceur-okr) · 8 atoms sourcés direct, 2 en hypothèse, 1 flou.

**Observé · 8 atoms sourcés direct**

- **Observation** · phenomenon · *"Frustration, échec, culpabilité, la boucle de tous les régimes"* · source · audience VoC `VOC-trustpilot-7a2x`, sample_size 14.
- **Tension** · state_actual · *"J'enchaîne les régimes depuis 10 ans, je reprends toujours plus"* (audience pain principal sourcé pain_points[0]) · state_desired · *"Stabiliser sans privation"* (sourcé jtbd.emotional). reason_blocked · `internal belief` ("je suis nulle en discipline") sourcé `audience.objections[].formulation` VOC-3.
- **Reframe** · pivot_mechanism · `revelation` (sourcé `angle.lineage.angle_canon_id: A-revelation-cause-cachee`, canon copy).
- **Bridge** · spec_activated · `MEC-02 · Régulation microbiote intestinal · genre Lactobacillus + Bifidobacterium` (canon spec.json) · benefit_served · `BEN-04 · Stabilisation pondérale sans restriction calorique` (canon spec.json).

**Déduit · 2 atoms en hypothèse à valider**

- **Reframe** · perceptual_pivot · formulation *"Les régimes échouent parce que ton microbiote est dysbiotique, pas parce que tu manques de discipline"* (confidence moyenne · cohérent cross-component, mais pas testé en VoC verbatim direct). Question · *"On test ce pivot tel quel en paid, ou audit ce que les concurrents okr disent du même territoire d'abord ?"*
- **Bridge** · promise_formulated · *"Stoppe la boucle des régimes en 21j sans privation, ton microbiote rééquilibré stabilise ton poids tout seul"* (confidence forte sur cohérence cross-component, moyenne sur résonance audience). Question · *"Cette promise tient les 3 fils (state_desired + pivot + benefit). Reste à valider qu'elle résonne ; on peut tester en paid budget calibré ou capturer 2-3 verbatims similaires d'abord."*

**Inconnu · 1 variable à creuser**

- **Observation** · sample_size sur phenomenon `"culpabilité"` flou · 14 verbatims sur "frustration/échec", seulement 4 sur "culpabilité" spécifiquement. Move · `mine-voc` zoom sur émotion culpabilité audience femme minceur (~10 min, capture verbatims denses sur cet axe émotionnel précis).

**Leviers · 2 axes d'investigation**

- **Axe A · Densifier voice client sur axe culpabilité** (lève Inconnu Observation.sample_size) · `mine-voc` zoom émotion. ~10 min. Unlock atoms phenomenon sourcing solide pour brief copywriter.
- **Axe B · Router downstream brief copywriter direct** (si atoms acceptables) · `produce-copy-brief ANG-03` consume les 11 atoms enrichis pour drill 3-5 hook variants + body + CTA family. ~5 min.

**Close ouvert**

Sur ANG-03 (8 atoms `forte` sourcés direct + 2 `moyenne` en hypothèse + 1 flou sur sample_size culpabilité), deux moves possibles ·

A · Lever l'Inconnu d'abord (Axe A) · upgrade Observation.phenomenon culpabilité de `moyenne` à `forte` via mine-voc zoom, puis route brief copywriter avec formula entièrement traçable. Pertinent si tu vises scale paid > 3k€/mois sur cet angle OU si culpabilité est ton angle principal de différenciation.

B · Router brief copywriter direct (Axe B) · accept les atoms `moyenne` agrégée (cohérence cross-component forte, manque uniquement sourcing direct sur culpabilité), produce-copy-brief consume tel quel, test paid budget calibré ~80€/angle, 5-7j data avant verdict. Pertinent si deadline lancement serrée OR test exploratoire avant scale.

Mon avis · B direct, l'angle est solide sur 8/11 atoms, les 2 hypothèses tiennent la cohérence, et la culpabilité reste secondaire au pivot principal "microbiote dysbiotique". Mine-voc zoom sera utile pour la vague 2 brief (variants ciblés culpabilité), pas critique pour l'ouverture.
