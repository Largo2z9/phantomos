---
name: map-mechanisms
type: producer
version: "1.2.0"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
mode: proposed
operator_facing: true
consumes:
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
  - path: brands/{slug}/audiences/*/pain_points/*.json
  - path: brands/{slug}/pain_points/*.json
description: >
  v1.2.0 (v2.64 ontologie sémantique pure lecture) · BREAKING refactor read pattern · lit pain_points depuis SUB-AUDIENCE (`brands/{slug}/audiences/*/pain_points/*.json`) pour mapping `mechanism.triggered_by` → pain au lieu de top-level v2.63 OR sub-field profile legacy. Cross-audience natif · un mechanism qui résout un pain owned par audience_A sert sémantiquement audience_A (pas de array affected_audiences[] requis · l'appartenance précède le tracking). Backward compat strict additif · read fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.1.0 (v2.63 ontologie pure lecture) · BREAKING refactor read pattern · lit pain_points depuis COLLECTION TOP-LEVEL séparée `brands/{slug}/pain_points/*.json` pour mapping `mechanism.triggered_by` → pain au lieu de sub-field `profile.pain_points[]` legacy. Profile schema v2.0 BREAKING · read fallback preserved pour brownfield v1.7.
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (pain-benefit-chain). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.0.0 (D#386 canon S55 atomique deep enrichment). Sub-skill cartographie atlas brand
  posé D#386. Reçoit en input le `spec.mechanisms[]` light pass produit par `snapshot-brand`
  (mechanism_id + name + description) et l'enrichit en deep pass avec 7 deep fields atomiques ·
  target, mode_of_action, time_window, duration, evidence_level, market_sophistication,
  triggered_by_specs[]. Canon-driven (cite EFSA / INSERM / clinical trials si disponible dans la
  matière scrapée OU dans les resources canon). Trigger opérateur distinct de `snapshot-brand`
  (l'opérateur peut creuser les mécanismes d'un produit déjà snapshotté sans relancer le full
  snapshot). Invocable ponctuellement par l'opérateur per décision D#386 (sub-skills `map-X`
  utilisables séparément).
  FR · "creuse les mécanismes de {product}", "approfondis mechanisms {product}", "map-mechanisms {product}", "deep dive mécanismes {product}"
  EN · "map mechanisms", "deep dive mechanisms", "enrich mechanisms {product}"
  FR: "creuse les mécanismes de {product}", "approfondis mechanisms {product}", "map-mechanisms {product}", "deep dive mécanismes {product}".
  EN: "map mechanisms", "deep dive mechanisms", "enrich mechanisms {product}".
permissions:
  reads: [brand, product]
  writes: [product]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists, product exists, spec.mechanisms[] light pass cartographié N ≥ 1 (via snapshot-brand)
  postconditions: deep fields enrichis et staged via mutation gate, finalize-mutation-batch event emitted
disambiguates_against:
  snapshot-brand: "snapshot-brand produces the light pass (mechanism_id + name + description) on the full product spec. map-mechanisms enriches the deep fields (target, mode_of_action, time_window, etc.) on mechanisms already cartographied. Route to snapshot-brand when the product spec doesn't exist yet."
  ingest-resource: "ingest-resource captures a founder PDF or clinical study to enrich the spec broadly. map-mechanisms only enriches the mechanisms[] array specifically with the 7 deep fields. Route to ingest-resource when the operator drops a single resource doc; route to map-mechanisms when the operator explicitly wants to deep dive the mechanisms."
  define-specs: "define-specs cartographs the spec from scratch (no URL, manual encoding). map-mechanisms presupposes spec.mechanisms[] light pass already exists. Route to define-specs when no scrape was possible."
prerequisites:
  - field: brands/{slug}/brand.json
    level: L1
    auto_pull: read_brand
    freshness_ttl_days: 365
  - field: brands/{slug}/products/{p_slug}/spec.json
    level: L1
    auto_pull: read_spec
    freshness_ttl_days: 90
  - field: spec.mechanisms[]
    level: L1
    threshold: 1
    block_if_missing: true
  - field: brands/{slug}/audiences/*/pain_points/*.json
    level: L2
    auto_pull: read_pain_points_sub_audience
    freshness_ttl_days: 90
    fallback: read_pain_points_top_level_then_profile_legacy
---

# Skill · map-mechanisms

> Atomique deep enrichment du `spec.mechanisms[]`. Light pass (snapshot) → deep pass (7 fields canon). Canon-driven · cite EFSA / INSERM / clinical refs si la matière l'autorise. Backward compat strict · les mechanisms light pass existing restent intacts, seuls les fields null sont enrichis.

---

## Tone

Posture d'investigation, pas de pitch. Le skill cartographie des mécanismes biologiques observés ou déduits, jamais inventés. Quand un mechanism manque de support clinical (anecdotal, mechanistic_only), le surface dans Section 3 (Inconnu) comme axe à investiguer, pas comme fait posé. Cite les références canon explicitement (numéro EFSA, étude INSERM, trial NCT) quand elles sont sourcées, jamais paraphrasé.

---

## Expert methodology

**Persona** · senior formulator R&D + senior medical writer. Sait lire un dossier clinique, distinguer in-vitro / animal model / clinical trial, mapper un ingrédient à un système biologique cible, calibrer le time_window observable selon evidence_level. Sépare ce qui est documenté de ce qui est revendiqué marketing.

**Framework** · les 7 deep fields canon de `spec.mechanisms[]` (schema v1.10+, D#386 canon S55) ·

| Deep field | Type | Rôle | Source canon attendue |
|---|---|---|---|
| `target` | string | système biologique ciblé | physiologie standard |
| `mode_of_action` | enum | type d'action canonique | classification pharmaco standard |
| `time_window` | enum | délai observable | clinical data ou enregistrement market |
| `duration` | string | persistance effet | clinical trial follow-up |
| `evidence_level` | enum | force de preuve | hiérarchie evidence-based med |
| `market_sophistication` | enum | maturité audience cible | analyste market |
| `triggered_by_specs[]` | array refs | spec ingredient/feature qui active | spec.composition / spec.ingredients |

---

## Step 0 · DRGFP prerequisite check (canon v2.38+)

Avant production, scanner les prerequisites canon DRGFP ·

1. **L1 silent** · `brands/{slug}/brand.json` + `brands/{slug}/products/{p_slug}/spec.json` doivent exister.
2. **L1 silent** · `spec.mechanisms[]` doit contenir au moins 1 entry (light pass cartographié par snapshot-brand).
3. **Block-if-missing** · si `spec.mechanisms[].length === 0` → refus poli + route opérateur ·

```
Pas de mechanism light pass cartographié sur {product_slug}. Move utile · snapshot-brand
sur l'URL produit (~3 min, extrait mechanism_id + name + description), puis je creuse
les deep fields ici.
```

Stop. Ne pas inventer des mechanisms pour satisfaire la requête.

4. **L2 gate** · si `spec.composition` est vide OR `spec.ingredients[]` est vide → flag inline en Section 3 (Inconnu) · les `triggered_by_specs[]` resteront partiels.
5. **L3 degraded** · si zéro canon clinical disponible (pas d'EFSA database, pas de trial cité dans `spec.proofs.scientific`) → tous les enrichments ship avec `evidence_level: anecdotal | mechanistic_only`, confidence 0.5-0.6.

---

## Step 1 · Read encoded data (v1.2.0 v2.64 ontologie sémantique pure · read pain_points sub-audience)

Load silently ·

- `brands/{slug}/brand.json` · sector, market.sophistication_stage, audience awareness baseline.
- `brands/{slug}/products/{p_slug}/spec.json` · 
  - `identity.product_category` (route les mechanisms canon attendus par catégorie · supplement → ingrédients actifs, skincare → mécanismes cutanés, etc.)
  - `specs.composition` ou `specs.ingredients` (matière brute pour `triggered_by_specs[]`)
  - `mechanisms[]` light pass (input principal)
  - `proofs.scientific` (refs clinical si dispo)
  - `proofs.authority` (mentions presse, certifications)
- **`brands/{slug}/audiences/*/pain_points/*.json` (v1.2.0 v2.64 sub-audience)** · scan tous les pain_points sub-audience cross-audiences pour mapping `mechanism.triggered_by` → pain (quels pains canon le mechanism résout-il ?). Path déclare audience parente (owned natif). Filter optional par product · pain_points avec `affected_products` contains `{p_slug}` OR vide (brand-wide). Un mechanism qui résout PNT-12 owned par audience_A sert sémantiquement audience_A (cross-ref direct via parent path, pas array affected_audiences[]).
- **Backward compat fallback v2.63** · si `brands/{slug}/audiences/*/pain_points/` vide OR absent, fallback lecture `brands/{slug}/pain_points/*.json` top-level v2.63 (avec affected_audiences[] array). Cross-audience natif top-level · un mechanism qui résout PNT-12 sert toutes les audiences listées dans PNT-12.affected_audiences[].
- **Backward compat fallback v1.7** · si top-level vide aussi, fallback lecture `brands/{slug}/audiences/*/profile.json#/pain_points[]` legacy v1.7 brownfield (scan tous les profile.json + aggrégat pain_points par audience).

Pour chaque mechanism light pass, noter ce qui est déjà observable depuis le scrape · name, description, optional `target` ou `mode_of_action` si snapshot l'a tagué partiellement.

Pour chaque pain_point lu (sub-audience OR fallback chain), garder mapping `pain_id` → `formulation` + `pain_category` + `audience_owner_slug` (depuis parent path) pour cross-ref Step 2 (mechanism.triggered_by → pain_id resolution).

---

## Step 2 · Deep enrichment per mechanism (CORE)

Pour chaque mechanism dans `spec.mechanisms[]` où au moins un deep field est null, enrichir les 7 fields canon ·

### 2.1 · `target` (système biologique ciblé)

Identifier le système physiologique précis sur lequel le mechanism opère. Exemples canon ·
- supplément ashwagandha · `target: "axe HPA + cortex surrénal"` (modulation cortisol)
- probiotique digestion · `target: "microbiote intestinal · genre Lactobacillus + Bifidobacterium"`
- sérum capillaire · `target: "follicule pileux · phase anagène"`
- adaptogène énergie · `target: "mitochondries · production ATP"`

Hard rule · jamais flouter (jamais `target: "le corps"` ou `target: "bien-être"`). Si la cible est ambiguë, flag en Section 3 (Inconnu) plutôt que poser une cible vague.

### 2.2 · `mode_of_action` (enum)

Mapper le mécanisme sur l'enum canon schema v1.10+ · `cofactor | antioxidant | adaptogen | probiotic | coenzyme | regulator | stimulant | inhibitor | structural | delivery | other`. Si `other`, ajouter `_notes` qui précise le mode réel (e.g. `_notes: "biomimétique · imite un facteur de croissance endogène"`).

### 2.3 · `time_window` (enum délai observable)

Enum canon · `immediate | 7d | 14d | 30d | 60d | 90d+`. Calibrer selon evidence_level ·
- `clinical_cited` ou `efsa_validated` → time_window précis sourcé étude.
- `anecdotal` ou `mechanistic_only` → time_window estimé prudemment, flag `_notes: "estimé · pas de data clinical pour ce dosage"`.
- Si zéro support → laisser null, flag en Section 3.

### 2.4 · `duration` (text persistance effet)

Délai observable libre format, granularité opérateur. Distinct de `time_window` (enum) · `duration` capture la persistance ("tant que prise continue", "effet rémanent 3 mois post-arrêt", "résultat immédiat puis fading 4-6h"). Source · clinical trial follow-up si dispo, OR formulation prudente sourcée mode_of_action.

### 2.5 · `evidence_level` (enum force de preuve)

Enum canon · `clinical_cited | efsa_validated | efsa_partial | anecdotal | mechanistic_only`. Hiérarchie ·
- `clinical_cited` · trial randomisé contrôlé publié, dose équivalente au produit, population comparable. Citer la ref (e.g. *"Lopresti et al. 2019, NCT03088787, n=60, 8 sem"*).
- `efsa_validated` · health claim EFSA validé pour cet ingrédient à ce dosage.
- `efsa_partial` · claim EFSA validé mais à dosage différent OU pour bénéfice connexe.
- `anecdotal` · pratique d'usage tradition, témoignages clients, pas de support clinical.
- `mechanistic_only` · mode d'action documenté in-vitro ou animal model, jamais validé en clinical human trial.

Confidence calibrée · `clinical_cited` → 0.85-0.9 · `efsa_validated` → 0.8 · `efsa_partial` → 0.7 · `anecdotal` → 0.5 · `mechanistic_only` → 0.55.

### 2.6 · `market_sophistication` (enum maturité audience)

Enum canon · `low | medium | high`. Calibration ·
- `low` · audience découvre le mécanisme pour la première fois · territoire éducatif disponible (huge opportunity pour produce-paid-angles).
- `medium` · le mécanisme est connu par segments éveillés, pas encore mainstream.
- `high` · mécanisme saturé (probiotiques digestion, magnésium sommeil), need différenciation par dosage / forme / preuve.

Source canon · `brand.json#market.sophistication_stage` cross-référencée avec sector heuristic.

### 2.7 · `triggered_by_specs[]` (array refs vers spec ingredients)

Identifier les ingrédients / features dans `spec.composition` ou `spec.ingredients` qui activent ce mechanism. Many-to-many · un mechanism peut être triggered par plusieurs specs (synergie), un spec peut trigger plusieurs mechanisms (e.g. KSM-66 → cortisol + énergie + sommeil).

Hard rule · ne jamais inventer un ingredient_id. Si `spec.composition` ne liste pas l'ingrédient, laisser le array vide ET flag Section 3 (Inconnu) · *"Le mechanism `cortisol modulation` doit être triggered par un ingrédient adaptogène, mais `spec.composition` est vide. Ingest le PDF founder ou la fiche produit complète pour mapper triggered_by_specs[]."*

---

## Step 3 · Stage chaque enrichment via mutation gate

Per deep field enrichi, stage proposal via `write-to-context.py` mode=proposed ·

```bash
python3 .skills/write-to-context.py \
  --path "products/{p_slug}/spec.json#/mechanisms/{mechanism_idx}/target" \
  --value "{target_value}" \
  --source agent \
  --confidence {0.5-0.9 selon evidence_level} \
  --mode proposed \
  --reason "map-mechanisms deep enrichment · {brief rationale + canon ref si dispo}"
```

Répéter pour les 7 fields per mechanism. Pour `triggered_by_specs[]` (array), value est JSON-encoded `'["ING-01", "ING-02"]'`.

**Confidence calibration table** ·

| Evidence level | Confidence base | Modulator |
|---|---|---|
| `clinical_cited` | 0.85 | +0.05 si ref directement citée dans spec.proofs.scientific |
| `efsa_validated` | 0.8 | +0.05 si claim revendiqué directement sur PDP |
| `efsa_partial` | 0.7 | -0.05 si dosage produit ≠ dosage EFSA |
| `anecdotal` | 0.5 | +0.05 si N témoignages cohérents dans VoC mining |
| `mechanistic_only` | 0.55 | -0.05 si seulement in-vitro, pas animal model |

---

## Step 4 · Synthesis 5 sections (investigation posture canon v2.54+)

### Section 1 · Observé (faits sourcés)

> *Observé · {N mechanisms} enrichis · {date}*

Lister les enrichments dont les sources sont directes (clinical trial cité, EFSA validation, ingredient mapping depuis spec.composition explicit) ·

- MEC-01 `{name}` · `target: {value}` · `mode_of_action: {enum}` · `evidence_level: clinical_cited` · réf · {citation directe}
- MEC-02 `{name}` · `target: {value}` · `mode_of_action: {enum}` · `evidence_level: efsa_validated` · ID · {EFSA registry id}

**Hard rules Section 1** · uniquement les enrichments avec evidence_level `clinical_cited` ou `efsa_validated` ET `triggered_by_specs[]` non vide. Le reste va en Section 2.

### Section 2 · Déduit (hypothèses avec confidence chain)

> *Déduit · {N hypothèses} à valider*

Hypothèses sur les mechanisms moins documentés ·

- MEC-03 `{name}` · `target: {value} (confidence moyenne)` · `mode_of_action: adaptogen (confidence forte, mapping standard)` · `evidence_level: mechanistic_only` · indicateur source · in-vitro studies cited in {ref}. Question opérateur · *"As-tu un dossier clinical pour MEC-03, ou tu acceptes le claim mechanistic_only ?"*

**Hard rules Section 2** · formulation comme questions, jamais conclusions posées. Chaque hypothèse porte confidence explicite (forte / moyenne / faible / TRÈS faible) + indicateur source.

### Section 3 · Inconnu (variables non observables)

> *Inconnu · {N variables} à creuser*

Variables qui ne peuvent pas être enrichies sans matière supplémentaire ·

- MEC-04 · `triggered_by_specs[]` vide · `spec.composition` ne liste pas l'ingrédient actif. Move · ingest PDF founder ou fiche technique fabricant.
- MEC-02 · `time_window` ambigü · pas de clinical follow-up à dosage produit. Move · clinical trial spécifique OU formulation prudente avec flag.
- MEC-05 · `evidence_level` non-déterminable · zéro trial cité, zéro EFSA, zéro VoC dense. Move · soit mining VoC pour anecdotal-grade, soit downgrade à `mechanistic_only` flagué.

### Section 4 · Leviers (drill-down options · opérateur arbitre)

> *Leviers · {N axes} d'investigation prioritaires*

- **Axe A · Documentation clinical** (lève Inconnu MEC-02, MEC-05) · `ingest-resource` sur dossier clinical fournisseur OR brief mining PubMed sur ingrédient principal. ~15 min.
- **Axe B · Compléter `spec.composition`** (lève Inconnu MEC-04) · `ingest-resource` sur fiche produit complète (back of pack, fiche technique founder) OR re-snapshot URL produit si page enrichie depuis. ~5 min.
- **Axe C · Audit `market_sophistication`** (calibre downstream `produce-paid-angles`) · `audit-meta-account` sur compte concurrent OR scan SimilarWeb top 5 catégorie. ~20 min.

### Section 5 · Close ouvert (UNE question macro)

> Sur ces {N mechanisms enrichis · {M en `forte`, K en `moyenne`, L en `faible`}}, deux moves possibles selon ta priorité ·
>
> A · Lever le bloc clinical (Axe A) · upgrade les mechanisms moyens/faibles en `clinical_cited` ou `efsa_validated`, downstream `produce-paid-angles` ranke plus haut sur evidence-driven hooks. Pertinent si claim regulatory matter (DACH, France, claims healthcare).
> B · Lever le bloc composition (Axe B) · mapper `triggered_by_specs[]` complet, unlock le mechanism-reveal copy (angle copy le plus fort sur supplements sophistiqués). Pertinent si l'angle marketing repose sur "what's inside".
> C · Garder l'état actuel et router vers `produce-paid-angles` · si claim_confidence agrégée acceptable pour test paid (~50-100€/angle budget calibré).
>
> Mon avis · {reco adaptive · si claim majoritairement `clinical_cited` → C valide direct · si majoritairement `anecdotal` ou `mechanistic_only` → A critique avant scale claims regulatory · si `triggered_by_specs[]` majoritairement vide → B critique avant copywriter brief}.

---

## Step 5 · Finalize

Mandatory avant output operator-facing ·

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Exit code 2 → blocking, revise. Exit code 0 → ship.

---

## Hard rules

- **Canon-driven.** Toujours citer la référence (EFSA registry id, NCT trial id, INSERM publication ref) quand elle existe. Jamais paraphrasé sans source.
- **Confidence calibré evidence_level.** Voir table Step 3. Anecdotal ≠ clinical_cited. Jamais ship `clinical_cited` sans la ref.
- **Jamais inventer time_window ou duration.** Si zéro support clinical ou EFSA → laisser null + flag Section 3.
- **Backward compat strict.** Les mechanisms light pass existing (mechanism_id, name, description) restent intacts. Seuls les fields null sont enrichis. Jamais overwrite un field operator-stated.
- **Triggered_by_specs jamais inventé.** Si `spec.composition` ne liste pas l'ingrédient, laisser array vide + flag Inconnu.
- **5 sections explicites, jamais fusionnées en prose continue.** Anti-pattern AP-6 doctrine.
- **Confidence chain visible Section 2.** Chaque hypothèse · forte / moyenne / faible / TRÈS faible + indicateur source.
- **Close ouvert UNE question.** Jamais affirmatif (*"On y va ?"*, *"Want anything else?"*). Toujours drill-down macro avec 2-3 options + reco adaptive.
- **`finalize-mutation-batch` mandatory.** Step 5 non-skippable.
- **DRGFP block-if-missing.** Si `spec.mechanisms[].length === 0` → refus poli + route vers `snapshot-brand`. Pas de fabrication mechanism pour satisfaire la requête.
- **Operator-facing rule.** JAMAIS exposer field paths (`spec.mechanisms[0].target`), JAMAIS exposer confidence numeric (0.7), JAMAIS exposer enum raw (`evidence_level:clinical_cited` → dire *"clinical sourcé, ref Lopresti 2019"*). Operateur voit `observé / déduit / inconnu`, jamais l'algèbre derrière.

---

## Cross-references

- `docs/system/investigation-posture.md` · 5 sections canon, confidence chain explicit, close drill-down macro.
- `docs/system/dependency-resolution-protocol.md` · DRGFP L1/L2/L3 prerequisite check.
- `docs/system/confidence-propagation.md` · algèbre cascade confidence, calibration evidence_level → confidence numeric.
- `docs/system/schema-encoding-doctrine.md` · mutation rule, `_field_types`, sourcing tags.
- `resources/schemas/spec.schema.json` v1.10+ · `mechanisms[]` 7 deep fields canon (D#386 schema cible).
- `.skills/skills/snapshot-brand/SKILL.md` · upstream producer du light pass mechanisms.
- `.skills/skills/produce-paid-angles/SKILL.md` · downstream consumer (mechanism-reveal angle).
- `.skills/skills/ingest-resource/SKILL.md` · source enrichment quand `spec.composition` ou clinical refs manquent.
- `.skills/skills/audit-meta-account/SKILL.md` · source `market_sophistication` calibration.
- `.skills/write-to-context.py` · canonical mutation channel.
- `.skills/finalize-mutation-batch.py` · mandatory Step 5 primitive.
- Decisions canon · D#386 (sub-skills `map-X` invocables séparément, S55 2026-05-04).

---

## Example output · supplement ashwagandha

Operator triggers · *"creuse les mécanismes de ashwa-plus"*

---

Sur les 3 mechanisms du spec ashwa-plus, deux sont sourcés clinical (cortisol + énergie), un est mechanistic_only (sommeil) et reste à valider. Les `triggered_by_specs[]` sont complets sur KSM-66, partiels sur les co-actifs.

**Observé · 2 mechanisms enrichis sourcés**

- MEC-01 `Modulation cortisol stress` · target · axe HPA + cortex surrénal · mode_of_action · adaptogen · evidence_level · clinical_cited (réf · Lopresti et al. 2019, NCT03088787, n=60, 8 sem, KSM-66 600mg/j) · time_window · 30d · duration · tant que prise continue, effet rémanent ~2 sem post-arrêt · triggered_by · KSM-66 (ING-01) · market_sophistication · medium.
- MEC-02 `Production énergie cellulaire` · target · mitochondries (production ATP) · mode_of_action · cofactor · evidence_level · efsa_validated (Vitamine B12 health claim · réduction fatigue) · time_window · 14d · duration · tant que prise continue · triggered_by · B12 (ING-04) + Magnésium (ING-05) · market_sophistication · high (claim saturé).

**Déduit · 1 hypothèse à valider**

- MEC-03 `Modulation sommeil` · target · axe HPA + neurotransmission GABA (confidence moyenne · documenté in-vitro et animal model, pas de clinical à ce dosage) · mode_of_action · adaptogen · evidence_level · mechanistic_only · time_window · 21-30d (estimé) · duration · estimé tant que prise continue · triggered_by · KSM-66 (ING-01) · market_sophistication · medium. Question · *"T'as un dossier clinical pour le claim sommeil ashwa, ou tu acceptes le mechanistic_only flag avec budget paid prudent ?"*

**Inconnu · 1 variable à creuser**

- MEC-03 · `evidence_level` non-upgradable sans clinical à dosage produit. Move · ingest PubMed ashwagandha + sleep meta-analysis OR ingest dossier fournisseur Ixoreal KSM-66 (s'ils ont fait un trial sommeil).

**Leviers · 2 axes d'investigation**

- **Axe A · Documentation clinical sommeil** (lève Inconnu MEC-03) · ingest meta-analysis ashwa + sleep (Cochrane Review 2021 si dispo). ~15 min.
- **Axe B · Audit claim regulatory France** (calibre downstream paid copy) · scan ANSES + DGCCRF guidance sur claims sommeil sans clinical à dosage. ~20 min.

**Close ouvert**

Sur ces 3 mechanisms (2 `forte` sourcés clinical/EFSA, 1 `moyenne` mechanistic_only), deux moves possibles ·

A · Lever le bloc clinical sommeil (Axe A) · si MEC-03 upgrade `clinical_cited`, le claim sommeil devient revendiquable directement sur PDP + ad copy. Pertinent si ton positioning principal est "supplément stress + sommeil" et tu veux scaler paid avec claims solides.

B · Garder l'état actuel et router `produce-paid-angles` · si t'as accepté que MEC-03 reste anecdotal/mechanistic_only avec budget paid calibré, le mechanism-reveal copy reste valide sur MEC-01 (cortisol clinical_cited) et MEC-02 (énergie EFSA), MEC-03 ship en angle secondaire avec flag `à valider`.

Mon avis · A si tu vises scale paid > 5k€/mois avec claims regulatory matter (France). B si tu testes le territoire à <2k€/mois avant de scaler.
