---
name: audit-meta-account
type: producer
version: "1.1.1"
isolation_scope: brand_only
layer: production
recommended_model: sonnet
reasoning_pattern: null
description: >
  v1.1.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution (entre Expert methodology et Step 0). Action LOURDE · narratif étendu 2 niveaux abstraction (macro état compte santé + micro score matrices par bloc audité phrasé en prose). Pose pair senior media buyer expert · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  Structured audit of a Meta Ads account setup. Two modes: API-driven (default when
  token available, factual data-backed audit) or declarative interview (fallback,
  operator answers questions or sends screenshots).
  FR: "audit meta", "vérifie mon setup meta", "check ma config meta", "audit setup meta".
  EN: "audit meta setup", "check my meta config", "meta ads audit".
permissions:
  reads: [brand]
  writes: [learning]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brands/{slug}/brand.json must exist
  postconditions: optional capture-learning for key findings with confidence ≥ 8
disambiguates_against:
  validate-resources: "route to validate-resources when operator says 'audit' or 'check' without a platform context · that's a workspace integrity check, not a Meta platform audit"
---

# Skill: audit-meta-account

Senior media buyer account health check. Two modes based on API access. Observational findings, not blame. Zero questionnaire format when API is available.

## Expert methodology

**Canonical expert persona**: senior media buyer / account strategist with 10+ years on Meta Ads.

**Framework**: 5-block diagnostic covering pixel reliability, account structure, campaign architecture, catalog health, rules and safety.

**Matrix** (applied to each block): *finding status (OK / Warning / Issue) × operational impact × recommended action*.

**Key variables**: CAPI event received last 7d, event_id dedup rate, domain verification status, 8-event priority order, campaign-to-adset ratio, catalog sync freshness, policy flags count.

**Codified reference**: if `resources/conventions/meta-ads.json` missing or incomplete, Gate doc blocks execution until it is filled (rate limits, OAuth scopes, endpoint patterns, pitfalls).

---

## Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ · 5-block diagnostic + API multi-endpoints + cross-reference benchmarks canon + score matrices output finding × impact × action). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement disclosure pré-engagement en amont et Output format synthèse 5 blocs en aval.

Pattern obligatoire · l'agent verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique le compte Meta et score chaque bloc diagnostic, en prose narrative sobre (zéro matrice ASCII en LIVE · le score matrices canon viennent en Output format post-audit).

**2 niveaux d'abstraction obligatoires** ·

1. **Macro état compte santé** · verbaliser la compréhension du périmètre compte Meta AVANT de rentrer dans le détail bloc par bloc.
   Exemple audit-meta-account · "On part d'un compte Meta Ads {nom · stade business inféré ARR signals · domaine industrie phrasé}, qui opère depuis {age compte estimé pixel events history}, qui gère probablement {volume budget mensuel × N campaigns actives estimé endpoints API}. Mon hypothèse de pattern santé compte · {majoritairement bien setup mais détail signal critical à confirmer · OU setup correct mais structure campaigns sous-optimale · OU plusieurs gaps techniques détectés}. Les zones critiques à creuser en priorité · {1-3 axes basés signaux endpoints initial scan · pixel reliability suspect / CAPI dedup incertain / catalog sync stale}. Mon hypothèse impact opérationnel macro · {tracking solide donc data optimization OK · OU data signal compromis donc reco priorité fix tracking d'abord}."

2. **Micro score matrices par bloc audité phrasé** · verbaliser chaque bloc diagnostic en prose narrative pendant l'audit.
   Exemple audit-meta-account · "Sur ce bloc {pixel reliability / account structure / campaign architecture / catalog health / rules + safety} · finding observé {phrasé sourced endpoint · CAPI events received last 7d · dedup rate · domain verification status · 8-event priority order · campaign-to-adset ratio · catalog sync freshness · policy flags count} → status {OK / Warning / Issue phrasé pourquoi · pas tag brut} → impact opérationnel {phrasé concrètement ce que ça génère sur perf account · attribution loss · cost inefficiency · scaling block} → action recommandée {phrasé canon · pas jargon · priorité explicit}."

**Calibration narrative** · prose sobre · registre pair senior media buyer expert · zéro jargon plumbing (jamais `meta-ads.json#endpoint_pattern`, `_field_types`, `confidence_chain[]`, endpoint URLs en LIVE) · zéro tableau ASCII en LIVE (score matrices canon = Output format post-audit). Adapter le tonal au registre opérateur détecté (grounded · standard · dense).

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger entre blocs audités si l'agent part dans une mauvaise direction d'inférence (mauvais finding projeté · mauvaise classification status · mauvais impact opérationnel estimé) AVANT que les downstream recos cascadent sur cette base, (b) pédagogie · il apprend la posture experte sur audit Meta Ads en regardant la manière de penser un finding × impact × action sur 5 blocs canon (pixel · structure · architecture · catalog · rules).

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

---

## Step 0 · Gate access check (MANDATORY, before anything else)

**CRITICAL:** **YOU MUST** check Meta API access BEFORE starting the audit. **NEVER** fall back to a questionnaire silently.

1. Read `brands/{slug}/credentials.env` and `credentials_shared.env` (workspace root). Look for `META_ACCESS_TOKEN` (or equivalent per convention).
2. Read `resources/conventions/meta-ads.json`. Check scopes, endpoint patterns, rate limits. If incomplete or missing → Gate doc first (read official Meta doc via WebFetch, fill the convention) before any API call.

**Branching** (use AskUserQuestion for option presentation when token absent):

- **Token present + convention complete** → announce API mode, proceed to Step 1A:
  > *"API access OK for {brand}. I pull the data directly from Meta. 2-3 min, back with the audit."*

- **Token absent** → present the choice:
  > *"To audit your Meta setup I need API access. Two options:*
  > *(a) Walk you through generating a Meta System User token. ~5 min, one-time, audit becomes factual and future audits are instant.*
  > *(b) Declarative mode: I ask questions, you answer or send screenshots. Slower, depends on your memory."*

(a) → run setup flow, then Step 1A. (b) → Step 1B.

**Si MCP/token absent** · AskUserQuestion 2 options ·
- (a) "Je te guide pour connecter Meta maintenant (2 min via connect-mcp-server)"
- (b) "Je bascule en mode declarative interview (tu me donnes les données à la voix, je structure)"
Default proactif proactif · (a) si l'opérateur a le temps, sinon fallback (b) sans blocker.

---

## Step 1A · API mode (default when token available)

Read `brands/{slug}/brand.json` for name, language, stage.

Pull from Meta Marketing API (respect rate limits in convention):

1. **Ad Accounts** · list, IDs, currency, owner
2. **Pixels + CAPI** · installed, CAPI events last 7 days, event_id dedup rate
3. **Domain verification** · verified domains at business level
4. **Standard events** · received last 28 days per pixel, volume per event
5. **Campaign structure** · campaigns by objective, ad sets, ads
6. **Catalog** · connected catalogs, product count, last sync, feed errors
7. **Attribution + iOS14 AEM** · 8-event priority, attribution window per campaign
8. **Account warnings** · policy flags, spending limits, identity confirmation

Deliver a factual audit: 5 blocks with **data-backed findings**. Each finding = status (OK / Warning / Issue) + what the data says + one-line operational impact. **NEVER** ask the operator questions the API already answered.

---

## Step 1B · Declarative mode (fallback only)

Announce the mode explicitly:
> *"Declarative mode. Structured questions on 5 areas. Answer what you know, skip what you don't, screenshots OK. The audit will be as reliable as your memory of the setup."*

Then proceed area by area, conversationally. **NEVER** a form, **NEVER** decorative ✓ bullets, **NEVER** dump all questions at once. One question per turn.

---

## Step 1 · Initialisation (applies to both modes)

Read `brands/{slug}/brand.json`. Extract:
- Brand name and positioning
- Language preference (FR/EN) · default FR
- Existing `platforms.meta` config (if any)
- Brand stage (new, piloting, scaling)

If brand.json is missing → gracefully stop and ask operator to create it first (`setup-brand`).

If `platforms.meta` exists, read current setup notes to avoid re-auditing known data.

---

## The 5 audit blocks

### Block 1 · Pixel and tracking

Verify:
- Meta pixel installed on all pages (Events Manager diagnostics)
- Conversions API (CAPI) active and receiving events server-side
- Standard events configured (ViewContent, AddToCart, InitiateCheckout, Purchase)
- Domain verified at Business Manager level
- Pixel + CAPI deduplication active (shared event_id)

### Block 2 · Account structure

Verify:
- Business Manager hygiene (users, assets, access levels)
- Ad account naming convention
- Custom audience creation and retention
- Lookalike sources (source quality signal)
- Catalog connected if ecommerce

### Block 3 · Campaign structure

Verify:
- Campaign count per objective (not too fragmented)
- Ad set per campaign (CBO vs ABO usage)
- Ads per ad set (too few → no learning phase exit, too many → budget fragmentation)
- Active vs paused ratio
- Campaign naming convention

### Block 4 · Catalog and dynamic ads

Verify (if catalog connected):
- Product count and last sync timestamp
- Feed errors or warnings
- Dynamic ads set up with audience signals
- Product sets and use cases

### Block 5 · Rules and safety

Verify:
- Account warnings or policy flags
- Spending limits configured
- Identity confirmation status
- Automated rules (budget, performance)

---

## Output format

Deliver findings per block. For each:

```
Block N · {name}

- {finding 1}: OK | Warning | Issue
  {what the data or answer says}
  Impact: {one-line operational consequence}
  Recommended action: {specific next step}

- {finding 2}: ...
```

Close with **priority action list** (top 5 by severity) and **archive** the audit at `brands/{slug}/audits/YYYY-MM-DD-audit-meta.md`.

## Optional post-audit

- If findings confidence ≥ 8 → trigger `capture-learning` automatically
- Critical findings (Issue severity) → append to `brands/{slug}/pending-validations.md`

---

## Cross-references

- `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ NIVEAU LIVE · doctrine canon racine 3 phases temporelles · AVANT exec disclosure pré-engagement · PENDANT exec NIVEAU LIVE thinking aloud expert action LOURDE 2 niveaux abstraction macro état compte santé + micro score matrices par bloc audité phrasé · APRÈS exec Output format synthèse 5 blocs (finding × impact × action) · HR-DVD-11 + AP-DVD-11 enforcement.
- `resources/conventions/meta-ads.json` · scopes, endpoint patterns, rate limits, pitfalls canon required Gate check.
- `.skills/skills/audit-google-pmax/SKILL.md` · sister auditor canon PMAX Google Ads (pattern audit similaire 7 dimensions canon · même posture senior expert).
- `.skills/skills/capture-learning/SKILL.md` · downstream auto-trigger si finding confidence ≥ 8.
