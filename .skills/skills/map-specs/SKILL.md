---
name: map-specs
type: producer
version: "1.0.0"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
reasoning_pattern: null
operator_facing: true
patch_notes:
  v1.0.0: "v2.58 NEW · D#386 canon S55 mappers atomiques. Sub-skill atomique deep enrichment spec.specs.* (composition, materials, variants, nutrition_facts, posology, contraindications, origin, production_method, preparation, external_databases, target_suitability, durability, perishability). Extraction depuis logique snapshot-brand spec section + ingestion ad-hoc (PDF founder, fiche technique). Distinct snapshot-brand qui couvre light pass identity/composition basique. map-specs deep-dive sub-fields canon-driven (INCI, Open Food Facts, EFSA refs)."
description: >
  v1.0.0 (v2.58 D#386 NEW) · Sub-skill atomique cartographie deep enrichment des sub-fields `spec.specs.*` d'un produit (composition structurée, nutrition_facts, posology, contraindications, origin, production_method, preparation, external_databases, target_suitability, durability, perishability). Distinct de snapshot-brand qui fait le light pass surface · map-specs drill-down sub-field par sub-field, canon-driven (INCI cosmétique, Open Food Facts food, EFSA supplements), invocable séparément par l'opérateur pour creuser/refresh la fiche technique sans relancer le full snapshot.
  FR · "map-specs {product}", "creuse les specs de {product}", "approfondis specs produit", "détaille la composition".
  EN · "map specs", "deep dive specs product", "detail composition".
  FR: "map-specs {product}", "creuse les specs de {product}", "approfondis specs produit", "détaille la composition", "drill spec produit", "fiche technique deep".
  EN: "map specs", "deep dive specs product", "detail composition", "drill product specs", "deep product card".
disambiguates_against:
  snapshot-brand: "snapshot-brand est le light pass scrape URL → spec.json (identity, composition top-level, pricing). map-specs deep-dive les sub-fields spec.specs.* après que le light pass existe."
  define-specs: "define-specs est l'orchestrateur Phase 1 qui combine snapshot + Q&A + sources upload pour assembler la spec from scratch. map-specs est atomique sur sub-fields spec.specs.* d'une spec déjà initialisée."
  ingest-resource: "ingest-resource extrait des données structurables depuis docs upload (PDF, deck, CSV) générique. map-specs consume les outputs ingest-resource pour drill spec.specs.* spécifiquement."
permissions:
  reads: [brand, product]
  writes: [product]
  mode: proposed
  subagent_safe: true
consumes:
  - brands/{slug}/products/{p_slug}/spec.json
  - brands/{slug}/products/{p_slug}/sources/
  - resources/schemas/spec.schema.json
  - canon refs réglementaires (INCI, Open Food Facts, EFSA, Nutri-Score)
produces_proposals_for:
  - brands/{slug}/products/{p_slug}/spec.json#/specs/composition
  - brands/{slug}/products/{p_slug}/spec.json#/specs/nutrition_facts
  - brands/{slug}/products/{p_slug}/spec.json#/specs/posology
  - brands/{slug}/products/{p_slug}/spec.json#/specs/contraindications
  - brands/{slug}/products/{p_slug}/spec.json#/specs/origin
  - brands/{slug}/products/{p_slug}/spec.json#/specs/production_method
  - brands/{slug}/products/{p_slug}/spec.json#/specs/preparation
  - brands/{slug}/products/{p_slug}/spec.json#/specs/external_databases
  - brands/{slug}/products/{p_slug}/spec.json#/specs/target_suitability
  - brands/{slug}/products/{p_slug}/spec.json#/specs/durability
  - brands/{slug}/products/{p_slug}/spec.json#/specs/perishability
pipeline:
  preconditions:
    - "brand.json existe (brand setup_complete)"
    - "products/{p_slug}/spec.json existe avec light pass déjà cartographié (snapshot-brand exécuté OU spec posée manuellement)"
  postconditions:
    - "spec.specs.* sub-fields enrichis avec _field_types tagging par sub-field"
    - "5-sections investigation-posture output operator-facing"
    - "gaps explicit listés (sub-fields non sourçables canon)"
---

## Tone

Posture analyste fiche technique. L'opérateur veut creuser un sub-field précis (composition, nutrition, posologie, etc.) ou rafraîchir une section périmée. Sortie structurée, sourcing canon explicit, gaps listés sans inventer.

---

# Skill · map-specs

Sub-skill atomique de la famille `map-X` (D#386 canon S55). Deep-enrich les sub-fields `spec.specs.*` d'un produit après que le light pass existe. Invocable en standalone par l'opérateur (`map-specs ma-gelule`) ou orchestré par snapshot-brand quand le full pipeline cartographique tourne.

## Step 0 · DRGFP (preconditions check)

Avant tout drill, scanner prerequisites ·

1. Lookup `brands/{slug}/brand.json` → si absent ou identity vide → bloquer · *"La marque n'est pas configurée. Run setup-brand d'abord."*
2. Lookup `brands/{slug}/products/{p_slug}/spec.json` → si absent → bloquer · *"La spec produit n'existe pas encore. Run snapshot-brand ou define-specs d'abord pour le light pass."*
3. Lookup `brands/{slug}/products/{p_slug}/sources/` → noter présence (PDF technique, fiche founder, datasheet) pour ingestion ad-hoc si dispo
4. Lookup `spec.identity.type` + `spec.identity.category` → calibre le canon ref par défaut · cosmétique → INCI · food/beverage → Open Food Facts + Ciqual · supplement → EFSA · apparel → durability + origin focus · service → skip composition/nutrition, focus service_specs (déjà couvert par define-specs HR4.1)

Output state map des sub-fields actuels (lesquels sont déjà remplis vs vides) + confidence_chain[] init. Surface 1 ligne contextuelle ·

> *Map-specs sur {product_name}. Light pass déjà posé · {N sub-fields remplis / 13}. Sources upload détectés · {oui · {N fichiers} | non}. Canon ref calibré · {INCI | Open Food Facts | EFSA | générique}.*

## Step 1 · Drill composition[]

Cible · `spec.specs.composition[]` structuré v1.8 (ingredient · pct · origin · inci · safety_class).

**Sources d'enrichissement** (priorité descendante) ·

1. Existing `spec.specs.composition[]` array (legacy strings ou objets partiels) · seed pour structurer
2. Sources upload `products/{p_slug}/sources/*.pdf` (datasheet, fiche technique founder) · ingest via `ingest-resource` sub-call si présent
3. External databases lookup · si `spec.specs.external_databases.open_food_facts_id` ou `inci_beauty_id` rempli → cross-ref API publique
4. Canon ref · INCI table cosmétique pour normaliser noms ingrédients

**Logique drill** ·

- Pour chaque ingredient string legacy → propose normalisation objet structuré ·
  - `ingredient` · nom commun (français langue opérateur) ou nom standardisé
  - `pct` · % composition si dispo (sinon `null`, JAMAIS inventé)
  - `origin` · pays/région ingrédient spécifique
  - `inci` · nom INCI normalisé pour cosmétique (canon ref Open INCI database)
  - `class` · `active | filler | preservative | fragrance | colorant | emulsifier | binder | other`
  - `organic_certified` · boolean si certification bio mentionnée

Stage chacun via mutation gate ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/products/{p_slug}/spec.json#/specs/composition" \
  --value '[{"ingredient":"...","pct":N,"class":"...","origin":"...","inci":"..."}]' \
  --source agent \
  --confidence 0.7 \
  --mode proposed \
  --reason "map-specs drill composition · {N ingrédients sourcés canon INCI + N inconnus pct/origin}"
```

**Hard rules composition** · JAMAIS inventer percentages (laisser `null` si non observable). JAMAIS halluciner ingredient supplémentaire absent du light pass. Tagger `_field_types.composition.{i}.pct` comme `observed` (datasheet) | `declared` (operator) | `structured` (inferred docs) | `unknown` (laissé null).

## Step 2 · Drill nutrition_facts

Cible · `spec.specs.nutrition_facts` (serving_size · calories · macros · micros · allergens · dietary_tags · nutri_score_grade · allergen_sources).

**Activation conditionnelle** · seulement si `spec.identity.category` ∈ {food, beverage, meal_replacement, supplement, ingestible} OU `spec.identity.product_category` ∈ {physical} avec niche food/nutrition.

**Sources d'enrichissement** ·

1. Existing nutrition section (souvent partielle)
2. Sources upload (étiquette nutrition photo, datasheet macros)
3. Open Food Facts API cross-ref si `spec.specs.external_databases.open_food_facts_id` rempli
4. Ciqual database FR pour micros vitamines/minéraux

**Logique drill** ·

- `serving_size` · "400 kcal pouch", "30g", "1 scoop (25g)"
- `calories` · number ≥ 0 par serving
- `macros` · protein_g, carbs_g (of_which_sugars_g), fat_g (of_which_saturated_g), fiber_g, salt_g
- `micros[]` · array vitamines/minéraux avec name + amount + unit (mg | µg | g | IU) + rda_pct
- `allergens[]` · EU14 enum strict (gluten, milk, soy, nuts, eggs, fish, shellfish, sesame, sulfites, celery, mustard, lupin, molluscs, peanuts, oats)
- `allergen_sources[]` · texte libre allergènes hors EU14 (lanolin, gelatin, latex)
- `dietary_tags[]` · enum vegan, vegetarian, gluten_free, lactose_free, keto, paleo, halal, kosher, organic, sugar_free, low_fodmap, caffeine_free, etc.
- `nutri_score_grade` · A-E (calcul mathématique depuis macros si possible · canon ref Santé Publique France formule)

Stage via mutation gate sur `spec.json#/specs/nutrition_facts`.

**Hard rules nutrition** · `allergens` strict EU14, JAMAIS valeur hors enum. `nutri_score_grade` calculé OU laissé `null`, JAMAIS inventé. Cross-ref Open Food Facts si ID dispo (high confidence) vs Q&A operator (medium confidence).

## Step 3 · Drill posology

Cible · `spec.specs.posology` (recommended_daily_servings · serving_unit · timing · duration_recommended · max_daily_dose · notes).

**Activation conditionnelle** · seulement si `spec.identity.category` ∈ {supplement, ingestible, cosmetic_active, skincare_routine} OU si product description mentionne dosage explicit.

**Sources d'enrichissement** ·

1. Existing posology (souvent vide)
2. Sources upload (notice produit, fiche posologie founder)
3. EFSA dosage recommendations pour vitamines/minéraux dosés
4. Q&A operator si gap

**Logique drill** ·

- `recommended_daily_servings` · number ≥ 0
- `serving_unit` · gelule | capsule | tablet | scoop | ml | g | sachet | application | wash | dose
- `timing` · text libre · "morning", "with meals", "before bed"
- `duration_recommended` · "3-month cure", "continuous", "until symptom relief"
- `max_daily_dose` · number safety upper limit
- `notes` · text libre

Stage via mutation gate sur `spec.json#/specs/posology`.

**Hard rules posology** · cross-ref EFSA pour upper limits supplements (high confidence). Q&A operator si gap (declared). JAMAIS inventer dosage non sourcé.

## Step 4 · Drill contraindications

Cible · `spec.specs.contraindications` (conditions · medications · age_min · age_max · pregnancy · breastfeeding · warnings).

**Activation conditionnelle** · obligatoire si `spec.identity.category` ∈ {supplement, drug, cosmetic_active, ingestible} · optionnel sinon (déjà couvert par define-specs HR4.2 si activé).

**Sources d'enrichissement** ·

1. Existing contraindications
2. Sources upload (notice médicale, fiche compliance founder)
3. EFSA contraindications database pour actifs nutritionnels
4. Q&A operator (declared)

**Logique drill** ·

- `conditions[]` · medical conditions disqualifying use · ex `['hypertension', 'thyroid_disorder', 'epilepsy']`
- `medications[]` · drug interactions · ex `['anticoagulants', 'SSRI', 'MAOI']`
- `age_min` / `age_max` · number
- `pregnancy` · enum `safe | avoid | consult_doctor | contraindicated`
- `breastfeeding` · enum idem
- `warnings[]` · text libre

Stage via mutation gate.

**Hard rules contraindications** · canon-driven EFSA pour suppléments dosés. JAMAIS halluciner contraindication non sourcée (risque légal compliance).

## Step 5 · Drill origin

Cible · `spec.specs.origin` (country · region · facility · local_supply_pct · made_in_claim · supply_chain_transparency).

**Sources d'enrichissement** ·

1. Existing origin section
2. Sources upload (certificat Origine France Garantie, traçabilité founder)
3. PDP scraping si claim "Made in {country}" sur fiche produit
4. Q&A operator

**Logique drill** ·

- `country` · ISO-3166 alpha-2 · "FR", "IT", "DE"
- `region` · texte libre · "Provence", "Tuscany"
- `facility` · nom usine ou ville
- `local_supply_pct` · % matières premières locales 0-100
- `made_in_claim` · texte certifié · "Fabriqué en France", "Origine France Garantie", "Made in Italy"
- `supply_chain_transparency` · enum `full | partial | opaque`

Stage via mutation gate.

**Hard rules origin** · `made_in_claim` doit être texte exact certifié (canon ref labels FR Origine France Garantie, Fabriqué en France 50%+). JAMAIS extrapoler `local_supply_pct` sans source.

## Step 6 · Drill production_method

Cible · `spec.specs.production_method` (type · batch_size · frequency · method_notes).

**Logique drill** ·

- `type` · enum `industrial | small_batch | artisanal | limited_batch | handmade | made_to_order`
- `batch_size` · units per batch si pertinent
- `frequency` · "weekly", "seasonal", "on demand"
- `method_notes` · texte libre process spécifique

Sources · sources upload (méthode founder, fiche fabrication) OU Q&A operator.

Stage via mutation gate.

## Step 7 · Drill external_databases

Cible · `spec.specs.external_databases` (open_food_facts_id · yuka_id · inci_beauty_id · ciqual_id · ean · gtin).

**Sources d'enrichissement** ·

1. Existing IDs si déjà dans spec
2. Lookup canon · si product `name` + `category` → recherche Open Food Facts API publique (food/beverage) ou INCI Beauty (cosmétique)
3. Sources upload (EAN/GTIN sur packaging photo OU fiche logistique)
4. Q&A operator si gap

**Logique drill** ·

- `open_food_facts_id` · ID Open Food Facts (food/beverage)
- `yuka_id` · ID Yuka (cross-ref food/cosmétique)
- `inci_beauty_id` · ID INCI Beauty (cosmétique)
- `ciqual_id` · ID Ciqual ANSES (food FR détaillé)
- `ean` · EAN-13 packaging
- `gtin` · GTIN-14 logistique

Stage via mutation gate.

**Hard rules external_databases** · cross-ref via API publique si possible (high confidence). Si lookup zero match → laisser `null`. JAMAIS inventer ID.

## Step 8 · Drill target_suitability

Cible · `spec.specs.target_suitability` (skin_types · hair_types · body_areas · use_cases · demographics).

**Logique drill** ·

- `skin_types[]` · enum `dry | oily | combination | sensitive | normal | mature | acne_prone | rosacea | eczema` (cosmétique)
- `hair_types[]` · enum `straight | wavy | curly | coily | fine | thick | dry | oily | damaged | colored | frizzy | thinning` (hair care)
- `body_areas[]` · texte libre · "face", "scalp", "hands", "full_body", "outdoor_trail", "urban"
- `use_cases[]` · texte libre · "trail_running", "daily_commute", "cold_weather", "travel"
- `demographics[]` · texte libre · "adults", "teens", "women_menopause", "men_40plus"

Sources · PDP scraping (claims `pour peaux sensibles`, `pour cheveux fins`), brand positioning, Q&A operator.

Stage via mutation gate.

**Hard rules target_suitability** · enum strict pour skin_types/hair_types (canon ref dermatologie). Texte libre OK pour body_areas/use_cases/demographics.

## Step 9 · Drill durability + perishability

Cible · `spec.specs.durability` (warranty_years · warranty_type · repairable · spare_parts_available · repair_program · lifespan_estimate · repairability_index) ET `spec.specs.perishability` (shelf_life_days · peak_freshness_days · storage_conditions · freshness_guarantee · period_after_opening_months · expiry_date_required).

**Durability** · pour goods durables (apparel, electronics, furniture, accessoires).
- `warranty_years` · number
- `warranty_type` · enum `limited | lifetime | conditional | commercial`
- `repairable` · boolean
- `spare_parts_available` · boolean
- `repair_program` · URL/nom programme brand
- `lifespan_estimate` · "10 years of regular use", "500 wash cycles"
- `repairability_index` · 0-10 (canon FR index réparabilité électronique 2021+)

**Perishability** · pour goods périssables (food, cosmétique, supplément).
- `shelf_life_days` · {min, max} number
- `peak_freshness_days` · {start, end} number
- `storage_conditions` · texte libre
- `freshness_guarantee` · texte libre
- `period_after_opening_months` · number (canon EU Cosmetics Regulation PAO, mandatory si shelf life > 30 mois)
- `expiry_date_required` · boolean (DLC/EXP mandatory)

Stage chacun via mutation gate.

**Hard rules durability/perishability** · cross-ref canon FR repairability_index pour électronique. PAO obligatoire cosmétique EU (compliance lock).

## Step 10 · Synthesis · 5 sections investigation-posture

**Doctrinal contract** · output structuré 5 sections per `docs/system/investigation-posture.md`. Cartographier avant affirmer · jamais affirmer une hypothèse comme un fait · jamais halluciner sub-field non sourcé · ouvrir le drill-down opérateur, ne pas le fermer.

### Section 1 · Observé (sub-fields enrichis sourcés)

> *Observé · drill spec.specs sur {product_name} ({date}, {durée})*
>
> *Sub-fields enrichis · {N sourced} / 13*
> *  composition · {N ingrédients normalisés INCI / N total} · sources · {datasheet | Open Food Facts | PDP}*
> *  nutrition_facts · {macros + N micros + N allergens EU14} · source · {Open Food Facts ID #{xxx} | étiquette photo upload}*
> *  posology · {dosage + timing + duration_recommended} · source · {notice produit upload | déclaré operator}*
> *  ... (un bullet par sub-field enrichi)*
>
> *Sub-fields inchangés (light pass déjà posé · pas de matière nouvelle) · {liste}*
>
> *Sub-fields non sourçables (pas de canon ref + pas de upload + pas de Q&A) · {liste}*

### Section 2 · Déduit (cohérence cross-sub-fields)

3-5 hypothèses derived from cross-checks · INCI matches composition raw, nutri_score matches macros calculation, posology matches EFSA upper limits, target_suitability matches niche+demographics.

> *Déduit · {N} cohérences à valider*
>
> *D1 · Cohérence composition/INCI · les {N} ingrédients matches INCI canon · confidence forte | aligné canon réglementaire*
>   À valider · {liste ingrédients non-matchés à clarifier opérateur}
>
> *D2 · Nutri-score calculé · {grade} cohérent avec macros · confidence forte*
>   À valider · si Nutri-Score officiel sur packaging matche le calcul
>
> *D3 · Posology vs EFSA · dosage recommandé en-dessous max safety EFSA · confidence moyenne (cross-ref partiel)*
>   À valider · si datasheet founder confirme exact upper limit

### Section 3 · Inconnu (sub-fields gap · canon refs non-trouvés)

> *Inconnu · {N} sub-fields non sourçables canon*
>
> *1. {sub-field critique} → {méthode pour lever · ex "ingest-resource sur PDF datasheet founder"}*
> *2. {sub-field 2} → {méthode · ex "ID Open Food Facts à scanner depuis packaging"}*
> *3. ... (typiquement 3-5 sub-fields gap sur drill complet)*

### Section 4 · Leviers (drill-down options · opérateur arbitre)

> *Leviers · {N} axes pour combler les gaps*
>
> *Axe A · Datasheet technique founder (lève {N sub-fields})*
> *  → action · "upload PDF datasheet founder dans products/{p_slug}/sources/, lance ingest-resource" (15 min)*
>
> *Axe B · Validation experte (lève {N sub-fields})*
> *  → action · "1 question opérateur sur composition % + dosage EFSA · 3 min"*
>
> *Axe C · Cross-ref base publique (lève {N sub-fields})*
> *  → action · "lookup Open Food Facts / INCI Beauty si IDs trouvables sur packaging" (5 min)*

### Section 5 · Close ouvert (UNE question macro)

> *Spec produit `{product_name}` enrichi sur {N sub-fields / 13}. {N gaps restants}. Sur quoi tu veux qu'on continue · datasheet founder (composition pct + safety), validation experte rapide, ou cross-ref Open Food Facts ?*

## Hard rules · canon-driven, zéro invention

- **HR1 · Canon-driven** · cite canon refs Open Food Facts, INCI Beauty, EFSA, Ciqual, Santé Publique France quand utilisés. Si pas de canon ref disponible → flag explicit `pas de canon ref` dans output Section 3.
- **HR2 · JAMAIS inventer percentages composition** · laisser `null` si non observable. Mention `(pct inconnu, à confirmer datasheet)` en surface.
- **HR3 · JAMAIS halluciner contraindications** · risque légal compliance. Sources obligatoires (EFSA, notice produit, operator declared).
- **HR4 · Enum strict respect** · allergens EU14, scent_family, skin_types, hair_types, warranty_type, mode_of_action, time_window. Valeur hors enum = stage refusé par mutation gate.
- **HR5 · _field_types per sub-field** · tag `observed | declared | structured | unknown` à chaque sub-field enrichi. Cross-ref doctrine `docs/system/field-types.md`.
- **HR6 · Backward compat strict** · sub-fields existing remplis (light pass snapshot-brand ou define-specs) NE sont PAS écrasés sauf si operator validate explicit. map-specs ajoute, ne réécrit pas silencieusement.
- **HR7 · Operator-facing rule** · JAMAIS exposer `_field_types`, `confidence` numerique, `mode=proposed`, paths internes. Traduire en `observé / déduit / déclaré / incertain` si distinction utile.
- **HR8 · Zéro em-dash** · `·`, `(.)`, `(,)`, `:` substituent partout.

## Anti-patterns à refuser

- AP-1 · Inventer pct composition pour combler `null` (HR2 violation)
- AP-2 · Halluciner contraindication non sourcée (HR3 violation, légal risk)
- AP-3 · Écraser silencieusement light pass existing (HR6 violation)
- AP-4 · Exposer `confidence: 0.7` ou `mode: proposed` en surface (HR7 violation)
- AP-5 · Drill exhaustif tous sub-fields sans calibration · si `spec.identity.category` = apparel, skip nutrition_facts/posology/contraindications. Activation conditionnelle obligatoire.
- AP-6 · Output prose narrative qui mélange Observé + Déduit + projection comme assertions confiantes (5-sections doctrine canon violation)

## Cross-refs

- Schema target · `resources/schemas/spec.schema.json` (v1.11 sub-fields specs.*)
- Doctrine investigation · `docs/system/investigation-posture.md`
- Doctrine production · `docs/system/canonical-matrix-reasoning.md`
- Doctrine substrate · `docs/system/schema-encoding-doctrine.md`
- Sub-skill ingest (composition PDF founder) · `.skills/skills/ingest-resource/SKILL.md`
- Mutation gate · `write_to_context` (JAMAIS Edit/Write direct sur `.json`)
- Validation post-write · `validate-resources` (silent, flag MAJOR/CRITICAL)
- Sibling map-skills · `map-benefits`, `map-mechanisms` (futur), `map-audiences` (futur), `map-angles` (futur)
- Orchestrateur · `snapshot-brand` (full pipeline brand cartographique appelle map-X en séquence)
- Sister · `define-specs` orchestrateur Phase 1 from-blank, map-specs atomique post-light-pass

## D#386 lineage

D#386 (2026-05-04, S55) · Architecture cartographie marketing · `snapshot-brand` orchestrateur + sub-skills `map-X` invocables séparément. Pattern Largo · *"snapshot lui donner la capacité d'appeler des sub-agents qui pourront être utilisés ponctuellement plus tard par l'utilisateur"*. map-specs = extraction de logique snapshot-brand spec section + drill deep des sub-fields que le light pass n'attaque pas. Distinct snapshot (light pass, identity + composition top-level) · map-specs deep-dive 13 sub-fields canon-driven.
