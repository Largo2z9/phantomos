---
name: trendtrack-enrich-brand
type: producer
version: "1.1.0"
patch_notes_v2_87_4:
  - "1.1.0 (v2.87.4 doctrines propagation canon · dette documentée) · Skill orchestrator heavy 3 steps (lookup + shop profile + 3 ads queries) ~5-8 min runtime DOIT exposer disclosure pré-engagement canon EDD v2.79.5+ (Plan + ETA + Démarche + Paramètres décomposés NIVEAU 0 + Confirmation binaire) AVANT exécution + thinking aloud NIVEAU LIVE DVD v2.81.1+ pendant Steps lookup et ads queries. Audit Fincut session v2.87.3 finding · lancé direct sans disclosure préalable · pattern systémique cross-skills heavy non-propagation doctrines. Cross-ref `docs/system/engagement-disclosure-doctrine.md` v2.79.5+ + `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11. Enforcement runtime hardcoded Steps EDD + NIVEAU LIVE markers · backlog v2.87.5+ implementation. Backward compat strict additif."
patch_notes_v2_87_6:
  - "1.1.0 (v2.87.6 SUBSTRATE sprint · enforcement runtime maintien dette) · Sprint substrate canon · refresh atlas Stepprs deep desire chain v2.87.4 (chronic-pain-45 grand-parent narrative canon · workers-shifts conjoint Friday evening narrative canon) + NEW section walkthrough Porte A many-to-many `tour.md` Anatomie de la structure (rendu post-build-atlas-complete Stepprs). Impact ce skill · consume atlas Stepprs refreshed si invoqué démo pédagogique (rare · skill cible brand opérateur real). Enforcement runtime hardcoded EDD Steps + NIVEAU LIVE markers · statut dette inchangé v2.87.4 documentée · v2.87.6 maintien backlog v2.88.0+ implementation (pattern miroir v2.87.5 · scope chirurgical patch_notes vs refonte massive runtime). Backward compat strict additif."
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
reasoning_pattern: null
patch_notes:
  v1.0.0: "v2.69 NEW skill canonical · TrendTrack API live enrichment brand existing · resolve via /v1/lookup → /v1/shops/{shopId} → /v1/ads?pageId={pageId} chain · stage proposals brand.json (year_founded · social_media · proofs.trustpilot · financials.monthly_visits · market.categories) + learnings.json (scaling patterns observed · ads winner verbatims sample · creative format split · geo distribution · spend concentration). Pattern reproductible cross spy tools sources futures (Foreplay · Atria · Meta Ad Library) via NEW skill mirror sync-{tool}-enrich-brand pattern. Cross-ref D#391 (TrendTrack token canon) + D#408 (R&D Market Intelligence Layer pattern reproductible)."
description: >
  TrendTrack API live enrichment skill · resolve brand existing via lookup + drill shop profile + sample top ads · stage proposals brand.json + learnings.json. Layer territoire · enrichit substrat stable brand depuis intelligence externe TrendTrack. Pattern reproductible cross spy tools sources (R&D Market Intelligence Layer D#408). Skill canonical Layer 2 (API direct via curl Bash OU MCP TrendTrack si configuré côté opérateur Layer 1).
  Pré-requis · credentials_shared.env TRENDTRACK_API_KEY OR MCP TrendTrack actif (verify via claude mcp list).
  FR: "enrichis cette brand depuis trendtrack", "trendtrack data sur {brand_slug}", "ajoute les data ads concurrent", "intelligence external brand".
  EN: "trendtrack enrich {brand_slug}", "fetch trendtrack data", "competitive intelligence enrich", "external market data brand".
permissions:
  reads: [brand]
  writes: [brand, learnings, custom]
  mode: proposed
  subagent_safe: true
consumes:
  - path: docs/system/territory-doctrine.md
  - path: docs/system/investigation-posture.md
  - path: docs/system/connectivity-layering.md
  - path: docs/system/scope-extension-doctrine.md
pipeline:
  preconditions: |
    brands/{slug}/brand.json non-empty (brand existing required · skill ENRICH pas CREATE)
    TRENDTRACK_API_KEY in credentials_shared.env OR MCP TrendTrack actif
    Quota remaining via /v1/usage check (min 50 credits requis safe budget)
  postconditions: |
    validate-resources triggered silently post staging mutations
    pending-validations.md enriched
    operator arbitrates accept/reject per proposal field
produces_proposals_for:
  - brands/{slug}/brand.json#/identity/year_founded
  - brands/{slug}/brand.json#/social_media/*
  - brands/{slug}/brand.json#/proofs/trustpilot
  - brands/{slug}/brand.json#/financials/monthly_visits
  - brands/{slug}/brand.json#/market/categories
  - brands/{slug}/learnings.json (multiple LRN-NNNN entries)
disambiguates_against:
  snapshot-brand: "snapshot-brand scrape PDP brand publique · trendtrack-enrich-brand fetch external intelligence TrendTrack (ads · trustpilot · socials · traffic) qui ne peuvent PAS être scraped depuis PDP brand. Complémentaire · snapshot-brand pour spec/offers/profile depuis URL · trendtrack-enrich-brand pour external intelligence."
  decompose-ad: "decompose-ad analyse 1 ad concurrente fournie par URL OR ad_id pour reverse-engineer formula. trendtrack-enrich-brand fetch sample ads brand pour PATTERN analysis (scaling strategy · creative format split · geo distribution) PAS deep-dive single ad."
  watch-competitors: "watch-competitors monitor changements competitors over time. trendtrack-enrich-brand snapshot one-shot enrichment moment T."
triggers_fr:
  - "enrichis cette brand depuis trendtrack"
  - "trendtrack data {brand_slug}"
  - "fetch trendtrack {brand_slug}"
  - "ajoute intelligence externe ads"
triggers_en:
  - "trendtrack enrich {brand_slug}"
  - "fetch trendtrack data"
  - "competitive intelligence enrich"
  - "external market data brand"
---

# Skill · TrendTrack Enrich Brand

Enrichit brand state existing avec intelligence externe TrendTrack (shop profile · ads winners · patterns scaling · geo distribution · spend concentration · creative format split). Skill territoire canon · stage proposals via mutation gate.

## Tone

Output operator-facing présenté comme intelligence enrichment · pas data dump. "J'ai trouvé X · Y · Z dans TrendTrack pour {brand_name} · voici ce qui m'apparaît significatif" pas "fetch /v1/shops/{shopId} retourne ...".

## Step 0 · DRGFP prerequisite check (L1 silent · L2 gate · L3 quota)

**L1 silent** · brand_slug fourni en argument ? `brands/{brand_slug}/brand.json` existe ET `identity.name` non-empty ?

Si NON · refuse cleanly · "Il me manque {ce_qui_manque} pour démarrer. Brand existante requise."

**L2 gate** · TRENDTRACK_API_KEY dans `credentials_shared.env` (workspace-level) ? OR MCP TrendTrack actif (`claude mcp list` shows trendtrack server) ?

Si NON · AskUserQuestion ·

```
L'enrichissement TrendTrack a besoin d'un accès API configuré.

(a) Tu as une clé API TrendTrack · colle-la, je la pose dans le workspace (gitignored, jamais commit)
(b) Tu préfères connecter le serveur officiel via OAuth (~30s)
(c) On laisse pour plus tard · je reprends quand l'accès est configuré
```

**L3 quota check** · `GET /v1/usage` · verify `data.credits.totalRemaining` >= 50 (safe budget pour chain lookup + shop + ads + sample). Si < 50 · flag explicit · "Quota TrendTrack faible (X credits remaining) · enrichment partiel possible · continuer ?".

```bash
curl -s -H "Authorization: Bearer $TRENDTRACK_API_KEY" \
  "https://api.trendtrack.io/v1/usage"
```

## Step 1 · Brand lookup resolution

Build search query depuis `brand.identity.name` OR `brand.identity.slug` (preferer name shorter form · pas domain complet · "stepprs" pas "stepprs.com" · lookup endpoint timeout sinon).

```bash
curl -s -H "Authorization: Bearer $TRENDTRACK_API_KEY" \
  "https://api.trendtrack.io/v1/lookup?q={brand_search_term}"
```

Parse response · array `data[]` avec match objects. Filter ·

- `matchType: "exact"` + `matchField: "name"` priority highest
- `score: 1` priority highest
- `signals.hasShop: true` requis (need shopId pour Step 2)
- `signals.activeAds > 100` priority (brand active paid · pas dormant)

Output · resolved shop_id + facebook_page_id + brand canonical name + signals overview.

Si multiple matches (ex stepprs principal + clone mystepprs.store) · surface tous + AskUserQuestion "Lequel correspond ?". Si match unique · continue silent.

Si zéro match · refuse cleanly · "TrendTrack ne trouve pas cette brand · vérifie l'orthographe OR brand absent de l'index TrendTrack."

## Step 2 · Shop profile fetch

```bash
curl -s -H "Authorization: Bearer $TRENDTRACK_API_KEY" \
  "https://api.trendtrack.io/v1/shops/{shop_id}"
```

Parse response · extract enrichment candidates ·

| Field source | Field target brand.json | Confidence |
|---|---|---|
| `data.createdAt` (ISO date) | `identity.year_founded` (extract year) | high (factual) |
| `data.profile.countryCode` + `data.profile.currency` + `data.profile.defaultLanguage` | `identity.target_geo[]` + `financials.currency` + `identity.language` | high |
| `data.trustpilot.{rating, reviewCount, url, brandName}` | `proofs.trustpilot` (NEW sub-object) | high (factual) |
| `data.socials.{facebook, instagram, tiktok, youtube}.{handle, followers, growth30d}` | `social_media.{platform}.{handle, followers, growth_30d}` | high |
| `data.catalog.{productsCount, mainCategory, categories[]}` | `market.categories[]` + `market.products_count` | high |
| `data.catalog.bestSellers[]` | confirme spec.json existing OR flags new products | medium (cross-check) |
| `data.traffic.{monthlyVisits, growth30d, history[], topCountries}` | `financials.monthly_visits` + `seasonality.traffic_history` + `market.top_countries[]` | high |

Stage proposals via `write-to-context.py --mode=proposed --source=import` avec meta tag `trendtrack` pour traçabilité (source enum canon · `{operator, agent, scrape, inference, import}` · `import` = data ingérée depuis source externe identifiée).

## Step 3 · Ads sample fetch (3 queries · pattern analysis)

3 calls API ads pour capture patterns ·

**Query 1 · Top by longest running** (winners durables) ·

```bash
curl -s -H "Authorization: Bearer $TRENDTRACK_API_KEY" \
  "https://api.trendtrack.io/v1/ads?pageId={facebook_page_id}&search={brand_name}&limit=10&sortBy=longestRunning&order=desc"
```

**Query 2 · Top by reach** (winners reach-driven) ·

```bash
curl -s -H "Authorization: Bearer $TRENDTRACK_API_KEY" \
  "https://api.trendtrack.io/v1/ads?pageId={facebook_page_id}&search={brand_name}&limit=10&sortBy=reach&order=desc"
```

**Query 3 · Newest** (active rotation) ·

```bash
curl -s -H "Authorization: Bearer $TRENDTRACK_API_KEY" \
  "https://api.trendtrack.io/v1/ads?pageId={facebook_page_id}&search={brand_name}&limit=10&sortBy=newest&order=desc"
```

Total · 3 queries · ~30 ads échantillonnés. Cost · ~6-10 credits cumulés.

## Step 4 · Patterns analysis

Process ~30 ads sampled · extract patterns ·

**Pattern 1 · Narrative diversity ratio**

- Count unique ad body hashes (premier 100 chars)
- Ratio `unique_narratives / total_ads` · low = single hero replicated · high = diversified angles
- Exemple Stepprs · ratio 1/10 newest (1 narrative répétée) + ratio cumulé probably 2-3/30 · scaling strategy "single hero replicated cross-geo"

**Pattern 2 · Geo distribution**

- Tally `audience.mainCountry` cross-ads
- Top 3 countries · indicates scaling priority markets

**Pattern 3 · Spend concentration**

- Sum `metrics.estimatedSpend` cross top 10 longest running
- Top 3 ads spend share · indicates concentration vs distribution

**Pattern 4 · Creative format split**

- Count `media.type` cross-ads (image vs video vs carousel)
- Indicates production split

**Pattern 5 · CTA patterns**

- Tally `content.callToAction` enum values
- Top CTA dominant + variants

**Pattern 6 · Landing pages diversity**

- Count unique `content.landingPageDomain` + paths
- Indicates funnel test variants

**Pattern 7 · Targeting demographic**

- Tally `audience.{gender, ageMin, ageMax}` distributions
- Indicates targeting strategy (broad demographic + pain-based filtering vs narrow demographic)

**Pattern 8 · Ad performance benchmarks** (si data dispo)

- Reach mean + max + median
- Days running mean + max + median
- Estimated spend total + per-ad average

## Step 5 · Stage proposals (mutation gate)

Per Pattern + brand field mapping · stage proposals avec `write-to-context.py --mode=proposed --source=import` ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/brand.json#/identity/year_founded" \
  --value '2024' \
  --source import \
  --confidence 0.95 \
  --mode proposed
```

Mutations stagées · `brand.json` (identity/financials/social_media/proofs/market) + `learnings.json` NEW entries capturant patterns observed (scaling strategy · top winners verbatims · CTA dominants · geo distribution · creative format split). En output opérateur · annonce "N patterns d'intelligence capturés" · jamais exposer IDs internes LRN-NNNN dans la prose rendu.

**Source canon** · `--source import` est la valeur enum existing (workspace v2.69 ne bump pas write-to-context.py VALID_SOURCES · path additif strict). Meta tag `trendtrack` dans `_meta.lineage` post-write pour traçabilité spécifique source externe. Anti-pattern · tagger `--source agent` (perd traçabilité origine data externe).

## Step 6 · Synthesis output 5 sections investigation-posture canon

**Observé** · `{brand_name}` trouvé TrendTrack · `shop_id={X}` · `monthly_visits={N}` · `active_ads={N}` · `trustpilot={X.X}/5 ({N} reviews)` · `FB {N}k IG {N}k followers` · `categories: [...]` · `top 3 winning narratives observed (verbatim 1-line each)`.

**Déduit** · scaling strategy (single hero replicated cross-geo VS diversified angles) avec confidence chain · narrative cross-audience (workers + chronic combined VS separated) · geo priority markets · spend concentration indicator · creative format dominant.

**Inconnu** · LTV exacte · organic content + email flows · CAC effectif paid · retention rates · seasonality validated (need mine-vom validation cross-source).

**Leviers** ·

- `decompose-ad` sur 1-2 top winning ads pour deep dive formula OTRB
- `profile-audience` enrich pour valider audiences inferred depuis verbatims testimonials
- `mine-voc` cross-source Trustpilot reviews 3.4/5 (real customer voice vs ad testimonials curated)
- `learn-from-session` capture patterns observed pour cross-brand learnings library
- `score-matrix` re-run avec data réelles updated

**Close ouvert** · UNE question macro · ex "Faut-il prioritiser decompose-ad sur Michelle hero ad winner OR creuser audience cross-narrative (workers+chronic combined) qui contraste avec ton canon 2-audiences-séparées ?"

## Hard rules

- **Mutation gate strict** · TOUT write via write-to-context.py mode=proposed. JAMAIS Edit/Write direct sur brand.json.
- **Quota awareness** · check /v1/usage avant chain queries · refuse silent si quota < 50 credits.
- **No invented data** · si TrendTrack absent value field (e.g. trustpilot null) · skip · ne pas combler heuristique.
- **isolation_scope brand_only** · skill enrichit UNE brand par invocation. Multi-brands · multi-invocations distinctes.
- **Source canonical "import"** · tag explicit dans `_field_types` post-enrichment + `_meta.lineage` tracking `source_origin: trendtrack`.
- **Operator-facing rule** · présenter intelligence enrichment business-language · pas API verbose · pas paths internes.
- **No em-dash** · canon style strict middle dot ·

## Cross-references

- `docs/system/territory-doctrine.md` · layer territoire canon
- `docs/system/investigation-posture.md` · 5 sections synthesis pattern
- `docs/system/connectivity-layering.md` · Layer 1 MCP vs Layer 2 API skill calls
- `docs/system/scope-extension-doctrine.md` · pattern NEW skill addition canon
- `.skills/skills/snapshot-brand/SKILL.md` · complementary skill (PDP scrape vs external intelligence)
- `.skills/skills/decompose-ad/SKILL.md` · downstream skill (deep dive 1 ad post-sample)
- `.skills/skills/profile-audience/SKILL.md` · downstream enrich (audiences inferred verbatims)
- `.skills/skills/mine-voc/SKILL.md` · cross-source validation Trustpilot vs ad testimonials
- `.skills/skills/learn-from-session/SKILL.md` · capture patterns for cross-brand library

## Status

Canonical v1.0.0 · ships v2.69. Future · pattern reproductible cross sources (Foreplay · Atria · Meta Ad Library · BigSpy) via NEW skills mirror `{source}-enrich-brand`.
