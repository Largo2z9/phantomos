---
name: import-meta-results
type: capturer
version: "2.0.0"
recommended_model: haiku
isolation_scope: brand
layer: meta
description: >
  Brique 5 MINIMAL (réceptacle perf, D#482+) · pull Meta Insights par
  `lineage.ad_id` pour les creatives déployées (CRT-NN sous batch) · LAND le blob
  perf BRUT dans `creative.json#performance.raw` (+ performance.ad_id +
  performance.imported_at). Le job runtime = PULL + LAND, rien d'autre. La perf
  ATTERRIT + est JOIGNABLE (via genome_tags du dossier) + l'opérateur peut la VOIR.
  Le système n'APPREND PAS encore : l'analyse fine (gagnant/perdant, seuils de coupe,
  recalibrage régime explore/exploit, promotion canon, sémantique par plateforme,
  attribution) = CHANTIER DOCTRINE SÉPARÉ, DIFFÉRÉ → resources/sops/creative-production/perf-feedback-loop.md.
  Step 0 bridge proactif canon v2.77.
  FR: "import results Meta", "import perf ads", "land la perf", "import meta perf",
      "pull insights par ad_id", "récupère la perf des créas".
  EN: "import Meta results", "import ad perf", "land perf", "pull meta insights",
      "pull results by ad_id".
permissions:
  reads: ["brands/{slug}/creatives/*/*/creative.json"]
  writes: ["brands/{slug}/creatives/*/*/creative.json"]
  mode: silent
  subagent_safe: true
extension_hooks:
  consumable_by: ["creative_entity"]
disambiguates_against:
  - "analyze-perf · diagnostic deep-dive cross-platform multi-jour avec recos stratégiques
     vs import-meta-results · pull data brut + land dans performance.raw sans diagnostic ni analyse"
  - "learn-from-session · capture learnings session-end full conversation scan
     vs import-meta-results · pull Meta runtime continuous par ad_id ciblé, land brut"
  - "audit-creative-fatigue · curator scan fatigue creative-level avec reco
     vs import-meta-results · capturer pull data brut land dans le réceptacle perf"
  - "routine-perf · briefing perf quotidien navigator output operator-facing
     vs import-meta-results · capturer silent land perf brute dans creative.json sans output verbose"
pipeline:
  preconditions: |
    brands/{slug}/brand.json exists.
    brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json contient ≥1 créa avec
    lineage.ad_id non-null (= déployée Meta, clé de jointure renseignée).
    Credentials Meta présents (credentials_shared.env OR brands/{slug}/credentials.env).
  postconditions: |
    Pour chaque créa déployée : blob perf BRUT landé dans creative.json#performance.raw,
    + performance.ad_id (miroir lineage.ad_id) + performance.imported_at (date-time now).
    Aucune métrique re-modélisée (réceptacle ouvert additionalProperties).
    L'analyse fine (promotion canon, validations[], decay, recalibrage régime) reste DIFFÉRÉE
    (chantier perf-feedback-loop.md), gatée derrière une note 'TBD analyse fine'.
---

# Skill: import-meta-results

Capturer silent qui pull Meta Insights par `lineage.ad_id` pour les creatives déployées brand-side, puis LAND le blob perf BRUT dans `creative.json#performance.raw`. Brique 5 MINIMAL : on POSE le réceptacle, pas l'intelligence. La perf doit ATTERRIR + être JOIGNABLE (le signal « qu'est-ce qui a marché » se joint déjà aux `genome_tags` du dossier — on JOINT, on ne re-modélise pas). Layer meta, mode silent (pas de verbose output operator-facing).

**Le job runtime de ce skill en brique 5 = PULL + LAND.** Tout le reste (analyse fine, promotion canon, recalibrage régime, sémantique par plateforme, attribution) est un **CHANTIER DOCTRINE SÉPARÉ et DIFFÉRÉ** : `resources/sops/creative-production/perf-feedback-loop.md`. Ne PAS essayer de rendre ce skill intelligent maintenant.

## Expert methodology

**Canonical expert persona**: plombier du réceptacle perf · pull la donnée brute, la pose là où elle est joignable. Daemon silent, pas analyst, pas curator.

**Framework**: 2-step pipeline minimal (list créas déployées → pull Insights → land brut). Pas de cross-réf canon-tools, pas de classification outcome, pas de compute promotion. Ce sont des chantiers différés.

**Matrix** (applied per creative): *créa déployée × ad_id × blob perf brut landé dans performance.raw*.

**Codified reference**: `resources/schemas/creative.schema.json` (creative/1.4 · `lineage.ad_id` pattern-locké `plateforme_NNN` = clé de jointure, `performance` ouvert avec `performance.raw`), `resources/conventions/creative-storage.md` (forme batch `creatives/{batch}/{CRT-NN}/`), `resources/conventions/meta-ads.json` (Insights endpoints), `resources/sops/creative-production/perf-feedback-loop.md` (le marqueur du chantier différé : ce qui est posé vs ce qui reste à construire).

---

## Step 0 · Gate access + bridge proactif canon v2.77 (MANDATORY)

**CRITICAL:** verify connectivity AVANT pull Meta Insights. **NEVER** silently fail on missing token. **NEVER** écrire un blob perf sans data sourcée.

1. **Layer 1 MCP check.** Verify `facebook-graph` MCP connected via `claude mcp list`. Required pour Meta Insights pull par ad_id.
2. **Layer 2 credentials check.** Read `credentials_shared.env` (workspace) + `brands/{slug}/credentials.env` (brand). Required keys ·
   - `META_ACCESS_TOKEN` (token shared cross-brands)
   - `META_AD_ACCOUNT_ID` (brand-specific)
3. **Convention check.** Read `resources/conventions/meta-ads.json`. Si missing OR incomplete sur Insights endpoints, Gate doc canon avant call.

**Branching canon proactif v2.77** (AskUserQuestion via `ToolSearch(select:AskUserQuestion)`) ·

- **Tokens présents + MCP connecté** → silent proceed Step 1, mode capturer (pas annonce verbose) ·
  > *"Pull Meta results en cours · {N} créas déployées, ~30s. Je land la perf dans le dossier de chaque créa."*

- **Token absent / MCP absent** → AskUserQuestion 2 options ·
  - (a) "Je te guide pour connecter Meta maintenant (~2 min via connect-mcp-server). Future imports sont silent et continuous."
  - (b) "Skip pour cette fois · imports perf nécessitent Meta API. Reviens quand connecté."

  **Default proactif** · proposer (a) si l'opérateur a le temps, fallback (b) sans blocker (capturer skip propre, pas erreur).

---

## Step 1 · List creatives déployées (clé de jointure renseignée)

Scanner les créas sous la forme batch · `brands/{slug}/creatives/*/*/creative.json` (= `creatives/{batch}/{CRT-NN}/creative.json`, forme canon `resources/conventions/creative-storage.md`). **PAS** l'ancien dossier plat `brands/{slug}/creatives/produced/` (supprimé brique 3).

Pour chaque `creative.json` ·

1. Parse · extraire `creative_id`, `lineage.ad_id`.
2. **Filter (simple, brique 5 minimal)** · ne garder que les créas avec ·
   - `lineage.ad_id` non-null (= déployée Meta, clé de jointure renseignée, format pattern-locké `^(facebook|tiktok|snapchat|google)_[0-9]+$`).

   C'est le SEUL critère. **NE PAS** exiger `meta.deployed_at`, `meta.ad_id`, ni les champs canon-tools (`formula_used`, `framework_used`, `archetype_used`, `hook_used`, `objection_used`, `cta_used`) — ils n'existent PAS dans `creative.schema`. Le filtre rigide d'avant était le bug de la boucle morte (rien ne matchait jamais). Relâché : a un `lineage.ad_id` non-null = éligible.
3. Buffer · liste `[{creative_id, ad_id: lineage.ad_id, path: "creatives/{batch}/{CRT-NN}/creative.json"}]`.

Si zéro créa éligible (aucune n'a de `lineage.ad_id`) → close silent · log à `session-state.md` activity log entry `"import-meta-results run · 0 créa déployée (aucun lineage.ad_id renseigné)"`. Pas de output operator-facing verbose (mode silent canon).

---

## Step 2 · Pull Meta Insights par ad_id + LAND brut dans le réceptacle

Pour chaque créa buffered (max parallel 5, respect rate limit Meta canon meta-ads.json · 100k pts/h + 40 pts par ad active, sleep 0.5s entre calls) ·

Le `lineage.ad_id` est préfixé plateforme (`facebook_NNN`). Pour Meta, extraire la partie numérique `NNN` après le préfixe `facebook_` pour l'appel Graph.

Endpoint · `GET /{ad_id_numeric}/insights`

Params · `fields=spend,impressions,clicks,ctr,cpm,frequency,actions,cost_per_action_type,purchase_roas&date_preset=lifetime`

**LAND le brut, ne re-modélise PAS.** Le réceptacle `performance` est OUVERT (additionalProperties, blob `performance.raw`). On y dépose la perf telle que ramenée — impressions / spend / ctr / roas / cpa / hold-rate... selon la plateforme — SANS construire une ontologie de métriques. Quelle métrique = quel signal, normalisation cross-plateforme, seuils : tout ça est le chantier différé (perf-feedback-loop.md).

Construire le patch perf par créa ·

```json
{
  "ad_id": "{lineage.ad_id · ex facebook_120210000000123}",
  "imported_at": "{ISO date-time now}",
  "raw": {
    "...": "blob perf BRUT tel que ramené par l'API Insights (spend, impressions, ctr, cpm, frequency, actions[], cost_per_action_type, purchase_roas...). Non re-modélisé."
  }
}
```

**Write via `write_to_context`** (NEVER Edit/Write direct JSON) ·

- `field_path` · `creatives/{batch}/{CRT-NN}/creative.json#/performance`
  (écrire `performance.raw`, `performance.ad_id` = miroir de `lineage.ad_id`, `performance.imported_at`)
- `mode` · `direct` (capturer silent, pas de proposal flow)
- `source` · `agent` (auto-tagged capturer)

**Append-only sur l'historique** · si la créa a déjà une perf landée et qu'on veut garder la trace temporelle, pousser l'ancien blob dans `performance.snapshots[]` (append) avant d'écraser `performance.raw` avec le nouveau pull. Sinon écrire `performance.raw` directement. Jamais effacer un snapshot existant.

**NEVER** dump raw API output dans l'output operator-facing. Le brut va dans `performance.raw`, pas dans le chat.

---

## Step 3 · DIFFÉRÉ · l'analyse fine (CHANTIER perf-feedback-loop.md · TBD)

> **TBD analyse fine.** Cette section décrit l'intelligence qui RESTE à construire. Elle n'est PAS exécutée par ce skill en brique 5. Elle est GATÉE derrière ce marqueur et ne doit JAMAIS faire échouer le run sur des champs absents. Le job runtime ici = PULL + LAND (Steps 1-2). Référence chantier : `resources/sops/creative-production/perf-feedback-loop.md`.

Ce qui était précédemment câblé en dur dans ce skill (classification outcome success/neutral/failed/fatigued, cross-réf canon-tools, append `validations[]`, decay v2.37, threshold N≥3 brands auto-promote candidate, persist learnings.json) reposait sur des champs (`formula_used`, `framework_used`, `archetype_used`, `hook_used`, `objection_used`, `cta_used`, `meta.deployed_at`) qui **n'existent pas** dans `creative.schema`. C'était la cause de la boucle morte. **Désactivé**, repoussé au chantier doctrine.

La logique reste documentée ci-dessous comme cahier des charges du chantier — riche, préservé, mais **NON exécuté** (pas de write, pas de fail sur champs absents) tant que perf-feedback-loop.md n'est pas tranché.

Le chantier (par perf-feedback-loop.md, « RESTE à construire ») ·

1. **Sémantique par plateforme** — Meta / TikTok / Snapchat : métriques + seuils différents. Quelle métrique = quel signal (CTR, hold-rate, ROAS, CPA, thumb-stop, days_running). Normalisation cross-plateforme.
2. **Gagnant / perdant / « ça coupe »** — seuils de décision, par rapport à quelle baseline (marque, batch, benchmark). (Ancienne table outcome `purchase_roas >= target_stage` → success, etc. : à re-trancher ici, pas en dur dans le capturer.)
3. **Recalibrage régime explore/exploit** — comment la perf met à jour la jauge `perf_signal` (A3) → prochain régime + curseur sectoriel.
4. **Promotion canon (3e signal)** — quel principe abstrait se promeut vers la banque de concepts quand N créas convergentes gagnent. Le signal « qu'est-ce qui a marché » se JOINT aux `genome_tags` du dossier (mécanique / style / structure) déjà présents — on JOINT, on ne re-modélise pas. La règle exacte (ex N≥3, decay, validations[], cross-réf canon-tools) = ICI, pas dans le pull.
5. **Attribution** — multi-touch, fenêtre, multi-plateforme. Sujet en soi.
6. **Dashboard** — couche au-dessus, lit le même réceptacle (vue opérateur).

**Principe directeur (perf-feedback-loop.md)** · data-vs-logique : le réceptacle est GÉNÉRIQUE (la donnée, posée par ce skill), l'analyse est SPÉCIFIQUE (la logique, dans des skills/doctrines à écrire). Ne PAS figer l'ontologie des métriques dans le schéma ni dans ce capturer.

---

## Step 4 · Close silent

Une fois le land terminé, close terse (mode silent canon) ·

> *"Import done · {N} créas déployées, perf brute landée dans performance.raw. L'analyse (gagnant/perdant, promotion canon) reste un chantier séparé (perf-feedback-loop.md)."*

Log activity entry `session-state.md` · `"import-meta-results run · {N} créas, perf landée, analyse fine différée"`.

---

## Hard Rules

- **HR1** · Step 0 bridge proactif canon v2.77 MANDATORY · jamais skip access check. Default proactif (a) connect-mcp-server, fallback (b) skip propre (capturer silent, pas blocker).
- **HR2** · Brique 5 = POSER le réceptacle, PAS l'intelligence. Le job runtime = PULL + LAND. **NEVER** essayer de classer, scorer, promouvoir, recalibrer un régime ou cross-réf canon ici. Ces chantiers sont DIFFÉRÉS (perf-feedback-loop.md).
- **HR3** · Scan forme batch · lire `brands/{slug}/creatives/*/*/creative.json` (= `creatives/{batch}/{CRT-NN}/`). **NEVER** lire l'ancien dossier plat `creatives/produced/` (supprimé brique 3).
- **HR4** · Clé de jointure = `lineage.ad_id` (pattern-locké `^(facebook|tiktok|snapchat|google)_[0-9]+$`). **NEVER** lire `meta.ad_id` (inexistant). Filtre éligibilité = `lineage.ad_id` non-null, et RIEN d'autre.
- **HR5** · Filtre relâché (fix boucle morte) · **NEVER** exiger `meta.deployed_at` ni les canon-tools (`formula_used`/`framework_used`/`archetype_used`/`hook_used`/`objection_used`/`cta_used`) — ils n'existent pas dans `creative.schema`. **NEVER** faire échouer un run sur l'absence de ces champs.
- **HR6** · Land brut dans le réceptacle OUVERT · écrire le blob perf dans `creative.json#performance.raw` (+ `performance.ad_id` + `performance.imported_at`). **NEVER** re-modéliser les métriques, **NEVER** figer une ontologie de métriques (additionalProperties ouvert préservé).
- **HR7** · Append-only sur l'historique · push l'ancien `performance.raw` dans `performance.snapshots[]` avant écrasement si on veut la trace temporelle. **NEVER** effacer un snapshot existant.
- **HR8** · Write via `write_to_context` strict · **NEVER** Edit/Write direct sur `.json` files (mutation rule canon). Mode `direct` (capturer pas proposal flow), field_path `creatives/{batch}/{CRT-NN}/creative.json#/performance`.
- **HR9** · Mode silent canon · mode `silent` frontmatter. Output operator-facing minimal · 1 ligne announce Step 0 OK, 1 ligne close. **NEVER** verbose recap, **NEVER** 5 sections investigation-posture (curator/producer template, pas capturer).
- **HR10** · Zéro em-dash dans tout output (limited operator-facing). Substituer par virgule, parenthèses, point, deux-points ou middle dot (·). Canon `no_em_dash` strict.
- **HR11** · Brand isolation enforce · scope `brand_only`. Cross-brand read interdit par défaut. Le pull et le land restent dans `brands/{slug}/`.

---

## Anti-patterns

- **AP-1 · Rendre le skill intelligent maintenant** · agent classe outcome, calcule promotion canon, recalibre régime, cross-réf canon-tools en brique 5. Anti-pattern HR2 BANNI. Pattern canon · PULL + LAND seulement, analyse fine différée (perf-feedback-loop.md).
- **AP-2 · Lire l'ancien dossier plat** · agent scanne `creatives/produced/` (supprimé). Anti-pattern HR3 BANNI. Pattern canon · forme batch `creatives/*/*/creative.json`.
- **AP-3 · Lire meta.ad_id** · agent cherche la clé de jointure dans `meta.ad_id` (inexistant). Anti-pattern HR4 BANNI. Pattern canon · `lineage.ad_id` pattern-locké.
- **AP-4 · Filtre rigide boucle morte** · agent exige `meta.deployed_at` ou les canon-tools (`formula_used` etc.) absents du schéma → rien ne matche jamais → boucle morte. Anti-pattern HR5 BANNI. Pattern canon · filtre simple `lineage.ad_id` non-null.
- **AP-5 · Re-modéliser les métriques** · agent normalise/score/transforme la perf avant de l'écrire au lieu de lander le brut. Anti-pattern HR6 BANNI. Pattern canon · blob brut dans `performance.raw`, ontologie = chantier différé.
- **AP-6 · Écraser un snapshot** · agent overwrite `performance.snapshots[]` ou efface l'historique perf. Anti-pattern HR7 BANNI. Pattern canon · append-only sur snapshots.
- **AP-7 · Direct Edit/Write JSON** · agent edit `creative.json` via Edit/Write tools (bypass mutation gate). Anti-pattern HR8 BANNI. Pattern canon · `write_to_context` exclusive.
- **AP-8 · Verbose output operator-facing** · agent ship 5 sections investigation-posture pour un capturer silent. Anti-pattern HR9 BANNI. Pattern canon · 1 ligne announce + 1 ligne close, terse.
- **AP-9 · Fail silencieux sur token absent** · agent skip pull sans gate Step 0. Anti-pattern HR1 BANNI. Pattern canon · bridge proactif v2.77, jamais silent fail.
- **AP-10 · Promotion canon sans gate ni chantier** · agent écrit dans `resources/canon/` ou promeut un principe depuis ce skill. Anti-pattern HR2 BANNI. Pattern canon · promotion = chantier perf-feedback-loop.md, jamais ici.

---

## Cross-refs

- `resources/sops/creative-production/perf-feedback-loop.md` · **LE MARQUEUR DU CHANTIER DIFFÉRÉ** · ce qui est POSÉ (réceptacle, brique 5) vs ce qui RESTE à construire (analyse fine : sémantique par plateforme, gagnant/perdant, recalibrage régime, promotion canon, attribution, dashboard). Référence obligatoire avant toute tentative d'analyse.
- `resources/schemas/creative.schema.json` · creative/1.4 · `lineage.ad_id` (clé de jointure pattern-locké `plateforme_NNN`) + `performance` ouvert (`performance.raw`, `performance.ad_id`, `performance.imported_at`, `performance.snapshots[]`) = réceptacle générique SANS ontologie.
- `resources/conventions/creative-storage.md` · forme batch `brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json` (D#481) · allocation id par mkdir atomique · id de stockage (CRT-NN) séparé de la clé de join perf (ad_id externe).
- `resources/conventions/meta-ads.json` · Insights endpoints + rate limits + learned_rules.
- `docs/system/brand-isolation-doctrine.md` · scope `brand_only` enforced default.
- `analyze-perf` · sibling diagnostic deep-dive (vs capturer pull brut + land ici).
- `routine-perf` · sibling navigator briefing (vs capturer silent ici).
- `audit-creative-fatigue` · sibling curator scan fatigue (vs capturer land réceptacle ici).
- `learn-from-session` · sibling capturer session-end (vs continuous Meta runtime ici).
- `write_to_context` · canonical mutation gate (NEVER bypass).