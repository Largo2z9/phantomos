# Field Types · Canon

> Canonical reference for `_field_types` values. Read this when unsure how to tag a field. Every brand JSON has a top-level `_field_types` map using glob patterns (`identity.*`, `market.competitors[].name`). Validation enforced by `validate-resources` check 11b and `validate-schema-canon`.

---

## The four values

| Type | Binary test | One-line definition |
|------|-------------|---------------------|
| `observed` | Could a stranger verify this by looking at the brand's site/data right now? | Observable fact, captured as-is, not computed. |
| `stated` | Did the brand (or operator on behalf of the brand) declare this about itself? | Brand's own claim, accepted at face value. |
| `structured` | Is this an observation that a framework/model classified into a canonical shape? | Framework-applied observation, factual raw material, canonical slot. |
| `derived` | Is this the output of a computation over other fields? | Computed from other fields. **Never filled manually.** |

**If two tests pass** → pick the most specific : `derived` > `structured` > `stated` > `observed`.

---

## Decisive examples

### observed

| Field | Why observed |
|-------|--------------|
| `pricing.price` = 29.90 | Read directly from the product page. |
| `proofs.rating` = 4.6 | Count from the site, no framework. |
| `products_index[]` | List of products scraped from the sitemap. |
| `market.competitors[].domain` | URL seen in search results. |

### stated

| Field | Why stated |
|-------|------------|
| `identity.tagline` = "Les meilleurs cheveux à Paris" | Brand's own claim on the hero. |
| `positioning.value_proposition` = "Clean beauty sans compromis" | What the brand says about itself. |
| `brand.origin_story` | Narrative authored by the brand. |
| `tone_of_voice.essence` = "rassurant, parent-centric" | Brand's declared voice, as validated by operator. |

### structured

| Field | Why structured |
|-------|----------------|
| `benefits[].chain` (feature → benefit → outcome → emotion) | Framework slot; the raw quote is observed, the decomposition is canonical. |
| `market.market_overview.sophistication` = "stage 3" | Eugene Schwartz framework applied to observation. |
| `audience.psychology.pain_chain` | Surface → root framework applied to stated pains. |
| `offers.mechanics[].type` = "bundle_discount" | Canonical enum applied to what's observed on the offer page. |

### derived

| Field | Why derived |
|-------|-------------|
| `pricing.gross_margin` | `(price - cogs) / price`. |
| `financials.roas_breakeven` | Function of margin + fixed costs. |
| `offers.effective_price_per_unit` | Price ÷ quantity in bundle. |
| `metrics.ltv_cac_ratio` | LTV ÷ CAC. |

---

## Hard rules

1. **Never fill `derived` manually.** If the computation formula is not encoded in a skill or primitive, the field stays empty. Manual guess = `fabrication` per `validate-output-coherence`.
2. **A field must be tagged exactly once.** If you catch yourself wanting `observed | stated` for the same path, stop : the underlying value is either a fact you saw (observed) or a claim the brand made (stated). Pick the origin of the value, not the feel.
3. **Glob patterns are allowed but precision wins.** `market.competitors[].name` > `market.*`. Use globs only when the entire sub-tree genuinely shares one nature.
4. **`structured` requires a framework reference.** If you tag a field `structured`, the framework name (market sophistication, benefit chain, pain ladder, etc.) must be retrievable from `resources/frameworks/` or the skill's `entity_refs`. No framework = downgrade to `observed` or `stated`.
5. **Unmapped field writes are refused.** When `write-to-context` receives a path that is not covered by any glob in `_field_types`, the write is gated. Add the entry to `_field_types` first (via the canonical mutation channel), then retry the data write.

---

## Orthogonalité `_field_types` vs `_extraction` vs confidence (C1)

Trois couches DISTINCTES, jamais fusionnées :

| Couche | Question à laquelle elle répond | Où elle vit |
|---|---|---|
| `_field_types` (épistémique) | **Comment on SAIT** (observé, déclaré, structuré, calculé) | root map de chaque entité |
| `_extraction` (mécanique) | **Comment c'est OBTENU** (api_json, json_ld, dom_parse, headless, absent) + quand + fraîcheur TTL | root map `$ref _shared/extraction-provenance.json` · porteurs : brand, spec, offer, profile, pain_points, objections, voc-verbatim |
| confidence (inférence) | **À quel point on CROIT l'inférence** | `validation-state.json` · `psychology.confidence_chain` |

Une donnée `observed` par `dom_parse` fragile ne pèse pas comme une `observed` par `api_json` : le moteur de raisonnement aval lit les deux étiquettes. `extraction_method: absent` = tenté et introuvable → exige `lever` (politique d'échec C1 : jamais inventer une brique).

**Hard rule additionnelle (C1)** : tout champ de `offer.economics_proxy` et `angle.test_readiness.eligibility.overall` = `derived` obligatoire dans `_field_types` (jamais rempli à la main).

---

## Legacy labels

Pre-v2.1 archives may still contain `raw` or `declared` :
- `raw` → `observed`
- `declared` → `stated`

Migration is automatic on the next write. See CHANGELOG v2.1.0.

---

## Cross-references

- `docs/system/architecture.md § Field Type System` · general entity architecture context
- `.skills/skills/validate-resources/SKILL.md` § 11b · consistency check enforced on every brand
- `.skills/skills/validate-schema-canon/SKILL.md` · enum constraint on schema drafts
- `.skills/skills/propose-schema-draft/SKILL.md` · applied when proposing new entity schemas
- `.skills/skills/scaffold-entity-files/SKILL.md` § Mode data-first · default tagging on instance creation
- `.skills/skills/ingest-resource/SKILL.md` § Respect _field_types · per-write enforcement
