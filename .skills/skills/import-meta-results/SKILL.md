---
name: import-meta-results
type: capturer
version: "2.2.0"
recommended_model: sonnet
isolation_scope: brand
layer: meta
description: >
  v2.1.0 (v2.90.0 boucle minimale) · Step 3 TBD remplacé par l'exécution de la boucle
  CLASSER → TRACER → SIGNALER du SOP perf-feedback-loop.md (tranché, plus TBD) ·
  writes += learnings.json (kind test_result + observation) + creative.json#performance.signal ·
  rendu opérateur sobre (N classées · winners/losers · recos variantes · 1 next-step) ·
  Steps 0-2 pull+land inchangés, réceptacle performance.raw toujours brut ·
  recommended_model haiku → sonnet (la classification 3a-3c raisonne sur seuils + génome).
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
  reads: ["brands/{slug}/creatives/*/*/creative.json", "brands/{slug}/strategy.json",
          "brands/{slug}/learnings.json", "resources/concepts/", "resources/registries/hooks/"]
  writes: ["brands/{slug}/creatives/*/*/creative.json", "brands/{slug}/learnings.json"]
  mode: silent
  subagent_safe: true
extension_hooks:
  consumable_by: ["creative_entity"]
disambiguates_against:
  - "analyze-perf · diagnostic deep-dive cross-platform multi-jour avec recos stratégiques
     vs import-meta-results · pull data brut + land dans performance.raw sans diagnostic ni analyse"
  - "learn-from-session · capture learnings session-end full conversation scan
     vs import-meta-results · pull Meta runtime continuous par ad_id ciblé, land brut"
  - "audit-creative-fatigue · même classification (SOP perf-feedback-loop partagé), mais
     audit-creative-fatigue = scan dédié interactive avec output 5 sections
     vs import-meta-results · capturer silent, classification au fil de l'import, rendu 5 lignes max"
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
    Boucle minimale Step 3 exécutée (SOP perf-feedback-loop) : verdicts tranchés tracés dans
    learnings.json (kind test_result + observation), performance.signal écrit sur chaque créa
    classée. Le différé (attribution, cross-plateforme, promotion canon auto) reste différé.
---

# Skill: import-meta-results

Capturer silent qui pull Meta Insights par `lineage.ad_id` pour les creatives déployées brand-side, puis LAND le blob perf BRUT dans `creative.json#performance.raw`. Brique 5 MINIMAL : on POSE le réceptacle, pas l'intelligence. La perf doit ATTERRIR + être JOIGNABLE (le signal « qu'est-ce qui a marché » se joint déjà aux `genome_tags` du dossier — on JOINT, on ne re-modélise pas). Layer meta, mode silent (pas de verbose output operator-facing).

**Le job runtime de ce skill = PULL + LAND + boucle minimale (v2.1.0).** Le Step 3 exécute la boucle CLASSER → TRACER → SIGNALER du SOP `resources/sops/creative-production/perf-feedback-loop.md` (tranché v2.90.0). Tout le reste (attribution, sémantique cross-plateforme, promotion canon automatisée, dashboard) reste DIFFÉRÉ, liste explicite dans le SOP. Ne PAS déborder la boucle minimale.

## Expert methodology

**Canonical expert persona**: plombier du réceptacle perf · pull la donnée brute, la pose là où elle est joignable. Daemon silent, pas analyst, pas curator.

**Framework**: 3-step pipeline (list créas déployées → pull Insights → land brut → boucle minimale CLASSER/TRACER/SIGNALER selon le SOP). Pas de cross-réf canon-tools, pas de promotion canon : différés.

**Matrix** (applied per creative): *créa déployée × ad_id × blob perf brut landé dans performance.raw*.

**Codified reference**: `resources/schemas/creative.schema.json` (creative/1.4 · `lineage.ad_id` pattern-locké `plateforme_NNN` = clé de jointure, `performance` ouvert avec `performance.raw`), `resources/conventions/creative-storage.md` (forme batch `creatives/{batch}/{CRT-NN}/`), `resources/conventions/meta-ads.json` (Insights endpoints), `resources/sops/creative-production/perf-feedback-loop.md` (le SOP tranché v2.90.0 : seuils, verdicts, formule de jauge · et la liste de ce qui reste différé).

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

## Step 3 · Boucle minimale · CLASSER + TRACER + SIGNALER (SOP perf-feedback-loop tranché · v2.1.0)

> Exécuté APRÈS le land Step 2, pour chaque créa dont `performance.raw` vient d'atterrir. La logique canonique (seuils, verdicts, formats d'entrée, formule de jauge) vit dans `resources/sops/creative-production/perf-feedback-loop.md` · ce step l'EXÉCUTE, il ne la redéfinit pas. Sous-lecture du SOP obligatoire au premier run de session.

**3a · CLASSER.** Pour chaque créa avec perf fraîche · dériver les 4 signaux canon (CTR decay, CPM rise WoW, frequency saturation, ROAS decay · seuils EXACTS `audit-creative-fatigue` Step 3, jamais improvisés) + l'outcome fatigue (fresh/stable/warning/critical, table days_running + cross-signal logic) + le verdict winner/loser/inconclusive (target ROAS lu `strategy.json#annual_goals[]` kpi_metric ROAS actif · volume minimal spend ≥ 100€ ET days_running ≥ 7). Les slopes exigent du daily : si le blob Step 2 est lifetime agrégé, re-pull `date_preset=last_30d&time_increment=1` sur les créas éligibles (même endpoint, même rate limit), sinon verdict inconclusive · JAMAIS inventer un signal depuis un agrégat. Target ROAS absent → axe winner inconclusive + flag opérateur 1 ligne, une fois par run.

**3b · TRACER.** Pour chaque verdict TRANCHÉ (winner ou loser · inconclusive ne s'écrit pas) · append `learnings.json#entries[]` via `write_to_context` · `kind: test_result`, `fact` = le QUOI chiffré, `context` = le POURQUOI signaux (OBLIGATOIRE, entrée refusée sans), `cross_refs.creative_ids[]`, `test_result_data {roas, ctr, spend_eur, days_running, winner_proxy, fatigue_signal}`, `validation_status: tested`, `source: test_capture`. Append-only strict · re-classification = nouvelle entrée + `superseded_by` sur l'ancienne. Si winner ET `genome_tags` joignable à un pattern de bibliothèque (`resources/concepts/`, `registries/hooks/` via `related_mechanic_ids`) → entrée `kind: observation` en plus (pont curation · **JAMAIS write `resources/`**, promotion = humaine ≥ 2 sources, cf SOP).

**3c · SIGNALER.** Écrire `creatives/{batch}/{CRT-NN}/creative.json#/performance/signal` via `write_to_context` (mode direct) · `{outcome, verdict, classified_at, variant_axis_reco}` · mapping canon : CTR decay → `hook_swap` · CPM rise → `background_swap` · freq > 4.0 → `audience_swap` · compound → séquentiel hook puis background · winner sain → `null`. `performance.raw` et `snapshots[]` restent intouchés.

**3d · Recalibrage (rien à écrire).** La jauge `perf_signal` se calcule à la volée par ses consumers (formule canonique du SOP · none/early/established · consommée par frame-regime au gate A3). Si le run vient de la faire basculer (ex 3e verdict tranché avec convergence), le mentionner en 1 mot dans le rendu, en langage clair.

**3e · Signal de saturation du cœur (Spectre · D#506).** Conditions, toutes calculables à la volée (pas d'état persistant à détecter, canon « pas de fichier d'état ») · `perf_signal == established` (état COURANT, pas une détection de transition « vient de basculer ») ET `brand.json#/meta/stage ≠ launch` ET pas de `spectrum.json` frais (absent OU `refreshed_at` de plus de 90 jours, TTL canon) ET le signal `core_saturated` n'est PAS déjà dans le buffer pattern-detection pour cette marque (**dédupe** · sans ça il se re-poserait à chaque run une fois `established`). Si les 4 sont remplies, alors JUGEMENT de l'agent (sémantique, pas un champ pré-calculé · cf Master rule) · le mur dominant est-il le **MARCHÉ** ? (lire `strategic-diagnostic-doctrine` · un winner qui s'essouffle peut être un mur ANGLE et pas MARCHÉ · ne pas confondre cœur prouvé et marché ouvert). Si oui → poser `{type: core_saturated, brand, suggest: spectre}` dans le buffer, surfacé via le protocole Background (intégrer ou différer), JAMAIS silencieux. C'est le déclencheur n°3 du Spectre · le système propose la carte au bon moment. Si le mur est OFFRE ou ANGLE → ne PAS suggérer le Spectre (route le diagnostic, pas la carte).

**Rendu opérateur (sobre · remplace le close terse Step 4 quand Step 3 a tranché au moins 1 verdict)** ·

> *"Perf à jour sur 7 créas. 2 gagnantes (CRT-04, CRT-09 · au-dessus de ton objectif de rentabilité), 1 en fatigue critique (CRT-12 · l'accroche et le visuel s'usent, je recommande une variante d'accroche d'abord), 4 sans verdict (pas encore assez de volume). Assez de tests tranchés maintenant pour orienter le prochain batch sur ce qui gagne. Je prépare la variante d'accroche de CRT-12 pour validation ?"*

Cap 5 lignes. Chiffres seulement si l'opérateur drille. JAMAIS de field paths, de noms de skills, de jargon (`variant_axis`, `winner_proxy`) en surface · accroche, visuel, audience, objectif de rentabilité. UN next-step contextuel unique, jamais de menu.

**Reste différé (liste explicite, vit dans le SOP)** · sémantique normalisée cross-plateforme · attribution multi-touch · promotion canon automatisée · dashboard · decay automatique des validations. **NEVER** déborder la boucle minimale depuis ce skill.

---

## Step 4 · Close silent

Fallback quand Step 3 n'a RIEN tranché (0 créa classifiable · volume insuffisant partout) · close terse (mode silent canon) ·

> *"Import done · {N} créas déployées, perf brute landée. Aucun verdict tranchable encore (volume insuffisant), je re-classerai au prochain import."*

Sinon le rendu opérateur du Step 3 fait office de close.

Log activity entry `session-state.md` · `"import-meta-results run · {N} créas, perf landée, analyse fine différée"`.

---

## Hard Rules

- **HR1** · Step 0 bridge proactif canon v2.77 MANDATORY · jamais skip access check. Default proactif (a) connect-mcp-server, fallback (b) skip propre (capturer silent, pas blocker).
- **HR2** · Le job runtime = PULL + LAND + boucle minimale Step 3 (classer/tracer/signaler selon le SOP perf-feedback-loop, tranché v2.90.0). **NEVER** au-delà : pas de promotion canon, pas d'attribution, pas de normalisation cross-plateforme, pas de write `resources/`, pas de fichier d'état perf_signal (chantiers différés, liste explicite dans le SOP).
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

- **AP-1 · Déborder la boucle minimale** · agent promeut un pattern vers `resources/`, improvise un seuil hors SOP, écrit un fichier d'état perf_signal, normalise cross-plateforme ou tente une attribution. Anti-pattern HR2 BANNI. Pattern canon · PULL + LAND + boucle minimale Step 3 (seuils du SOP uniquement), le reste différé.
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

- `resources/sops/creative-production/perf-feedback-loop.md` · **LE SOP TRANCHÉ (v2.90.0)** · seuils, verdicts, formats d'entrée learnings, formule de jauge perf_signal = la logique canonique que le Step 3 exécute. Porte aussi la liste explicite de ce qui RESTE différé (sémantique cross-plateforme, attribution, promotion canon automatisée, dashboard). Sous-lecture obligatoire au premier run de session.
- `resources/schemas/creative.schema.json` · creative/1.4 · `lineage.ad_id` (clé de jointure pattern-locké `plateforme_NNN`) + `performance` ouvert (`performance.raw`, `performance.ad_id`, `performance.imported_at`, `performance.snapshots[]`) = réceptacle générique SANS ontologie.
- `resources/conventions/creative-storage.md` · forme batch `brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json` (D#481) · allocation id par mkdir atomique · id de stockage (CRT-NN) séparé de la clé de join perf (ad_id externe).
- `resources/conventions/meta-ads.json` · Insights endpoints + rate limits + learned_rules.
- `docs/system/brand-isolation-doctrine.md` · scope `brand_only` enforced default.
- `analyze-perf` · sibling diagnostic deep-dive (vs capturer pull brut + land ici).
- `routine-perf` · sibling navigator briefing (vs capturer silent ici).
- `audit-creative-fatigue` · sibling curator scan fatigue (vs capturer land réceptacle ici).
- `learn-from-session` · sibling capturer session-end (vs continuous Meta runtime ici).
- `write_to_context` · canonical mutation gate (NEVER bypass).