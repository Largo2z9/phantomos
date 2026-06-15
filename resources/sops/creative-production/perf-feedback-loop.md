---
name: perf-feedback-loop
type: sop
category: optimization
scope: single_brand
platforms: [meta, agnostic]
version: "1.0.0"
author: phantomos-template
last_reviewed: 2026-06-11
language: fr-mixed-en
description: >
  Boucle de feedback perf minimale sur les créas déployées d'une marque : CLASSER chaque créa
  (4 signaux fatigue canon + verdict winner-proxy) → TRACER en learnings append-only →
  SIGNALER sur la créa (performance.signal, jointure perf→génome) → RECALIBRER la jauge
  perf_signal à la volée. Ferme le pont produce→test→learn sans sur-ingénierie. Tout le reste
  (sémantique cross-plateforme, attribution, promotion canon auto, dashboard) reste différé
  et listé explicitement.
invoked_by:
  - source_type: orchestrator
    source: import-meta-results
    note: "Step 3 du capturer · exécute la boucle après chaque land de performance.raw"
  - source_type: orchestrator
    source: audit-creative-fatigue
    note: "le scan fatigue produit la même classification (CLASSER uniquement, layout legacy) · TRACER + SIGNALER réservés à import-meta-results tant qu'audit-creative-fatigue n'est pas migré au layout batch (dette explicite)"
  - source_type: orchestrator
    source: frame-regime
    note: "consumer de la formule perf_signal au gate A3 (Step 4 RECALIBRER · source de calcul unique)"
  - source_type: operator_direct
    source: "qu'est-ce qui a marché sur mes créas / lis la perf et apprends"
requires:
  - creative.json avec lineage.ad_id renseigné + performance.raw landé (import-meta-results Steps 1-2)
  - brands/{slug}/learnings.json existant (learnings.schema v1.1)
  - brands/{slug}/strategy.json avec un goal kpi_metric ROAS pour le verdict winner (sinon verdict inconclusive flaggé)
output_destination:
  - "brands/{slug}/learnings.json (entries append-only)"
  - "brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json#performance.signal"
---

# Perf feedback loop · la boucle minimale (CLASSER → TRACER → SIGNALER → RECALIBRER)

> Brique 5 a posé le RÉCEPTACLE (la plomberie). Ce doc, longtemps marqueur TBD, est désormais TRANCHÉ : il définit la boucle d'intelligence MINIMALE qui ferme le pont produce→test→learn. Pas l'analyse fine complète : la boucle qui suffit pour qu'une perf landée APPRENNE quelque chose au système, et rien de plus. Tout ce qui dépasse est différé et listé en bas, pas implicite.

## Thèse

La perf qui dort dans un blob brut n'apprend rien. `performance.raw` rend la donnée JOIGNABLE, il ne la rend pas EXPLOITÉE. Entre le réceptacle (générique, la donnée) et l'analyse fine complète (chantier lourd : attribution, normalisation cross-plateforme, promotion automatisée), il existe une boucle minimale à 4 temps qui produit déjà de l'apprentissage réel :

1. **CLASSER** · chaque créa avec perf fraîche reçoit un outcome (état fatigue) + un verdict (winner / loser / inconclusive). Seuils canon existants, zéro seuil inventé.
2. **TRACER** · chaque verdict tranché devient une entrée `learnings.json` append-only, le QUOI chiffré + le POURQUOI signaux.
3. **SIGNALER** · le verdict s'écrit sur la créa (`performance.signal`), ce qui rend le génome interrogeable par outcome : la jointure perf→génome devient une requête, pas une intention.
4. **RECALIBRER** · la jauge `perf_signal` (régime explore/exploit) se calcule à la volée depuis ce qui vient d'être tracé. Pas de fichier d'état.

Principe directeur inchangé (data-vs-logique) : le réceptacle reste GÉNÉRIQUE (la donnée, posée par `import-meta-results`), la logique vit ICI et dans les skills qui citent ce SOP. L'ontologie des métriques ne se fige ni dans le schéma ni dans le capturer.

## Posé en amont (brique 5 · inchangé, englobé)

- Clé de jointure : `creative.json#lineage.ad_id` (format `plateforme_NNN` : facebook_/tiktok_/snapchat_/google_).
- Réceptacle ouvert : `creative.json#performance` (additionalProperties · avale n'importe quelles métriques brutes dans `performance.raw`, historique dans `performance.snapshots[]`).
- Branchement : `import-meta-results` pull la perf par `ad_id` → land dans `performance.raw`. Le signal « qu'est-ce qui a marché » est joignable via les `genome_tags` du genome.json frère (mechanic_id, primary_style_id, support) : on JOINT, on ne re-modélise pas.
- Ce SOP ne touche JAMAIS `performance.raw`. La boucle écrit dans DEUX réceptacles distincts : `learnings.json` (la mémoire) et `performance.signal` (la jointure). Le brut reste brut.

## Vue d'ensemble · qui exécute quoi

| Temps | Exécutant | Lit | Écrit |
|---|---|---|---|
| CLASSER | `import-meta-results` Step 3 (à chaque import) · `audit-creative-fatigue` (à chaque scan · CLASSER uniquement, layout legacy) | `performance.raw` + Insights daily + `strategy.json` | rien (compute interne) |
| TRACER | `import-meta-results` Step 3 uniquement (réservé tant qu'audit-creative-fatigue n'est pas migré au layout batch · dette explicite) | classification + `genome_tags` | `learnings.json#entries[]` (append) |
| SIGNALER | `import-meta-results` Step 3 uniquement (même réserve, même dette) | classification | `creative.json#performance.signal` |
| RECALIBRER | tout skill côté A qui pose un régime (`frame-regime`) | `learnings.json` + `performance.signal` | rien (calcul à la volée) |

## Step 1 · CLASSER (outcome + verdict par créa)

Déclencheurs : chaque run `import-meta-results` (perf fraîche landée) et chaque run `audit-creative-fatigue` (scan fatigue dédié). Les deux produisent la MÊME classification, définie ici une seule fois.

### 1a · Les 4 signaux canon (seuils EXACTS de `audit-creative-fatigue` Step 3 · jamais improvisés)

| Signal | Compute | Seuils |
|---|---|---|
| **CTR decay** | CTR moyen J-1 à J-3 vs CTR moyen J-12 à J-14 · `(recent - baseline) / baseline × 100` | `< -25%` fatigue confirmed · `-10% à -25%` watch · `> -10%` OK |
| **CPM rise WoW** | CPM moyen J-1 à J-7 vs J-8 à J-14 · `(recent - previous) / previous × 100` | `> +30%` critical · `+15% à +30%` watch · `< +15%` OK |
| **Frequency saturation** | max frequency sur 7d window | `> 4.0` critical · `2.5 à 4.0` saturation · `1.8 à 2.5` normal · `≤ 1.8` optimal |
| **ROAS decay** | ROAS moyen J-1 à J-7 vs J-15 à J-21 · `(recent - baseline) / baseline × 100` | `< -30%` conversion fatigue · `-15% à -30%` watch · `> -15%` OK |

Les slopes exigent de la donnée DAILY. Si le blob landé est un agrégat lifetime sans `time_increment=1`, re-pull `last_30d&time_increment=1` sur les créas éligibles (même endpoint, même rate limit), ou déclarer les signaux slope non calculables pour ce run. JAMAIS inventer un signal depuis un agrégat.

### 1b · Outcome fatigue (table canon `audit-creative-fatigue` Step 4)

| Days running | Outcome |
|---|---|
| < 14 jours | **fresh** (learning phase, aucune action) |
| 14-21 jours | **stable** (OK si signaux verts, watch si 1+ jaune) |
| 21-30 jours | **warning** (si 2+ signaux rouges OR 1 critical) |
| > 30 jours | **critical** |

Cross-signal logic, inchangée : CTR decay confirmed + days ≥ 14 → warning minimum · CPM rise critical + days ≥ 14 → warning minimum · frequency > 4.0 → critical regardless days · 2+ signaux rouges simultanés → critical regardless days (compound).

### 1c · Verdict winner / loser / inconclusive

Le winner-proxy croise le ROAS observé au target encodé par l'opérateur :

- **Target ROAS** · lu dans `strategy.json#annual_goals[]`, l'entrée `status: active` avec `kpi_metric` ROAS → `target_value`. Si aucun goal ROAS encodé : l'axe winner est **inconclusive** pour toutes les créas + flag opérateur UNE fois par run (1 ligne, langage clair). JAMAIS inventer un target.
- **Volume minimal** · `spend_eur ≥ 100` ET `days_running ≥ 7`. Calibrage cohérent avec le budget test canon (~50-100€ par angle, 5-7 jours data minimum avant verdict, cf `produce-paid-angles` close). Sous ce volume, aucun verdict : le bruit statistique gagne.
- **winner** · volume minimal atteint ET ROAS (7 derniers jours, fallback lifetime si daily indisponible) ≥ target. `days_running > 30` encore au-dessus du target = winner renforcé (longevity_signal, meilleur proxy que le reach absolu).
- **loser** · volume minimal atteint ET ROAS < target ET (1+ signal fatigue confirmé OU `days_running ≥ 14`). La fenêtre 14j = fin de learning phase : une créa sous target avec signaux verts à 10 jours n'est PAS un loser, elle mûrit.
- **inconclusive** · tout le reste (volume insuffisant, target absent, signaux contradictoires, slopes non calculables).

Sortie du Step 1, par créa : `{outcome ∈ fresh|stable|warning|critical, verdict ∈ winner|loser|inconclusive, signaux[]}`. Compute interne, jamais surfacé brut à l'opérateur.

## Step 2 · TRACER (learnings.json · append-only)

Pour chaque créa à verdict TRANCHÉ (winner ou loser · les inconclusive ne s'écrivent pas, c'est du bruit qui noierait la jauge), append une entrée via `write_to_context` (`learnings.json#entries[]`, JAMAIS Edit direct) :

```json
{
  "id": "LRN-{next}",
  "kind": "test_result",
  "fact": "CRT-12 ({brand}) · loser à 23j : ROAS 1.4 vs target 2.5, CTR decay -33%, CPM +47% WoW, freq 3.2, spend 412€",
  "context": "OBLIGATOIRE · le POURQUOI avec les signaux : 'compound fatigue, hook usé (CTR decay confirmé) ET visual usé (CPM rise critical) · la mécanique testimonial-first n'a pas tenu au-delà de la learning phase sur cette audience'",
  "cross_refs": { "creative_ids": ["CRT-12"] },
  "test_result_data": {
    "roas": 1.4, "ctr": 0.014, "spend_eur": 412,
    "days_running": 23, "winner_proxy": false, "fatigue_signal": true
  },
  "validation_status": "tested",
  "source": "test_capture",
  "created_at": "{ISO now}"
}
```

- `fact` = le QUOI chiffré (1-3 phrases, chiffres ancrés). `context` porte le POURQUOI raisonné avec les signaux : une entrée sans reasoning est inutilisable par la curation et REFUSÉE par ce SOP.
- Append-only strict (learnings.schema v1.1) : un re-test de la même créa = NOUVELLE entrée, l'ancienne reçoit `superseded_by`. Jamais modifier, jamais supprimer.
- `cross_refs.creative_ids[]` obligatoire : c'est ce qui permet à la jauge (Step 4) et à la curation de re-joindre les `genome_tags` sans dupliquer les tags dans la learning.

## Step 3 · SIGNALER (performance.signal · la jointure perf→génome)

Écrire sur la créa, via `write_to_context` (`creatives/{batch}/{CRT-NN}/creative.json#/performance/signal`, mode direct, capturer) :

```json
{
  "outcome": "critical",
  "verdict": "loser",
  "classified_at": "{ISO now}",
  "variant_axis_reco": "sequential_hook_then_background"
}
```

Mapping `variant_axis_reco` canon (reprend `audit-creative-fatigue` HR9, une seule source) : CTR decay primary → `hook_swap` · CPM rise primary → `background_swap` · frequency > 4.0 → `audience_swap` (dépasse la capacité hook/background) · 2+ signaux compound → séquentiel (hook_swap puis background_swap, deux passes recompose). Winner sans signal fatigue → `null` (rien à swapper, on laisse tourner).

Pourquoi ce champ est load-bearing : les `genome_tags` du genome.json frère (mechanic_id, primary_style_id, support) deviennent INTERROGEABLES par outcome. « Quelles mécaniques gagnent chez cette marque » = scan `creatives/*/*/creative.json` where `performance.signal.verdict == winner` → join `genome.json#genome_tags`. C'est une requête, plus une re-modélisation. `performance.signal` est la SEULE zone interprétée du réceptacle (le bloc `performance` ouvert l'absorbe sans schema bump · figer le sous-schéma signal dans creative.schema = bump futur 1.5, flaggé pas bloquant) · `performance.raw` reste intouché.

## Step 3bis · OBSERVATION PATTERN (le pont vers la curation, sans la violer)

Si verdict **winner** ET le `genome_tags.mechanic_id` de la créa est joignable à un pattern de bibliothèque shippé (`resources/concepts/*.json`, `resources/registries/hooks/*.json`), la jointure se fait via l'espace d'ids déclaré par `related_mechanic_ids` (ids hook-level de l'enum 25 ET `mecanique_id` ad-level free-string du creative-mechanics-registry). `primary_style_id` se joint via le style-registry, PAS via `related_mechanic_ids`. Append alors une learning supplémentaire :

```json
{
  "kind": "observation",
  "fact": "Le pattern {pattern_slug} gagne aussi chez {brand} (CRT-09 winner, ROAS 3.1 vs target 2.5) · source perf réelle candidate pour la curation cross-brand (3e signal)",
  "cross_refs": { "creative_ids": ["CRT-09"] },
  "source": "test_capture"
}
```

Le garde-fou de `cross-brand-curation.md` reste ABSOLU : **JAMAIS modifier `resources/` depuis une marque.** La promotion `watch → promote-ready` est un acte de curation HUMAINE exigeant ≥ 2 sources indépendantes (factory-aware, pas par logo). Cette observation locale est exactement le « 3e signal = perf réelle » que la curation attendait : elle NOURRIT le curateur (qui lira les observations cross-brands au moment de statuer), elle ne le remplace pas. Une marque qui gagne = un point de donnée, pas une promotion.

## Step 4 · RECALIBRER (jauge perf_signal · calcul à la volée, pas de fichier d'état)

La jauge `perf_signal` (enum `none | early | established`, `genome-package.schema#gauges`, une des 3 jauges A3 qui produisent le `freedom_cursor` explore/exploit) ne vit dans AUCUN fichier d'état. Elle se calcule à la demande, par le skill qui en a besoin (`frame-regime`, tout skill côté A qui pose un régime de génération), depuis les deux réceptacles que la boucle vient de remplir.

**Formule canonique (UNE source de calcul · ce paragraphe · tout consumer le cite, jamais ne le duplique) :**

Soit T = les entrées `learnings.json` actives (kind=test_result, `superseded_by` null) de la marque.

- **none** · T = 0. Aucune perf tranchée : régime piloté par `atlas_richness` seule, explore prudent.
- **early** · T = 1 ou 2 · OU T ≥ 3 sans convergence joignable (aucun `mechanic_id` ni `primary_style_id`, rejoint via `cross_refs.creative_ids` → `performance.signal` + `genome_tags`, ne porte 2+ verdicts identiques). Du signal existe mais ne pointe pas encore une direction exploitable.
- **established** · T ≥ 3 ET au moins une convergence joignable (un même tag génome porte 2+ verdicts identiques, winners convergents ou losers convergents). Le régime peut basculer exploit sur les tags winners, et bannir les tags losers convergents du prochain batch.

Pourquoi à la volée : un fichier d'état serait un cache à invalider (3e source de vérité, drift garanti). T tient en un scan de `learnings.json` + un join sur N créas : le coût est négligeable, la cohérence est gratuite.

## DIFFÉRÉ explicitement (hors boucle minimale · ne pas construire en douce)

1. **Sémantique normalisée cross-plateforme** · TikTok hold-rate, Snapchat thumb-stop, équivalences de seuils. La boucle actuelle est calibrée Meta (seuls seuils canon existants). Étendre = nouvelle table de seuils par plateforme dans CE SOP, pas dans les capturers.
2. **Attribution multi-touch** · fenêtres, cross-platform, incrémentalité. Sujet en soi, aucune dépendance de la boucle minimale dessus.
3. **Promotion canon automatisée** (skill `curate-pattern`) · clustering + comptage factory-aware + draft d'objet library-pattern. La boucle fournit la matière (observations Step 3bis), la promotion reste humaine.
4. **Dashboard** · couche de lecture au-dessus des mêmes réceptacles. Rien à pré-construire.
5. **Decay automatique des validations** · vieillissement des test_results (un winner d'il y a 9 mois ne vaut plus preuve). Pour l'instant le `superseded_by` manuel suffit au volume réel.

## Hard rules

- **Never** improviser un seuil : les 4 signaux fatigue = seuils `audit-creative-fatigue` Step 3 (LA source des 4 seuils · pacing-doctrine = source amont des seuls axes frequency + CPM), le volume minimal et la fenêtre 14j = définis ici. Deux sources, zéro inline ailleurs.
- **Always** un reasoning (`context`) rempli sur chaque kind=test_result : le QUOI sans le POURQUOI n'apprend rien, entrée refusée sinon.
- **Never** écrire sous `resources/` depuis une marque : la promotion cross-brand reste un acte humain ≥ 2 sources indépendantes (cross-brand-curation.md).
- **Never** toucher `performance.raw` ni `performance.snapshots[]` : `performance.signal` est la seule zone interprétée du réceptacle.
- **Always** muter via `write_to_context` : learnings append-only (re-test = nouvelle entrée + superseded_by), signal en mode direct capturer.
- **Never** matérialiser `perf_signal` dans un fichier d'état : calcul à la volée, formule unique Step 4, citée jamais dupliquée.
- **Never** trancher un verdict sous le volume minimal (spend < 100€ OU days < 7) ni sans target ROAS encodé : inconclusive, et le dire.

## Cross-refs

- `.skills/skills/import-meta-results/SKILL.md` · l'exécutant principal de la boucle (dans son Step 3) · pull + land Steps 1-2 inchangés.
- `.skills/skills/audit-creative-fatigue/SKILL.md` · source canon des 4 signaux + outcome table + mapping variant_axis (HR2, HR9) · produit la même classification en mode scan dédié.
- `resources/schemas/learnings.schema.json` (v1.1) · format d'entrée (kind, fact, context, cross_refs.creative_ids[], test_result_data).
- `resources/schemas/creative.schema.json` (v1.4) · réceptacle `performance` ouvert + `lineage.ad_id` clé de jointure · sous-schéma `signal` à figer en 1.5 (flaggé, pas bloquant).
- `resources/schemas/genome-package.schema.json` · jauge `perf_signal` (none/early/established) + `freedom_cursor` · consumer de la formule Step 4.
- `resources/sops/creative-production/cross-brand-curation.md` · règle ≥ 2 sources indépendantes factory-aware · le « 3e signal = perf réelle » que Step 3bis alimente.
- `docs/system/pacing-doctrine.md` · source amont des seuls axes frequency + CPM (les 4 seuils opérationnels de la boucle vivent dans `audit-creative-fatigue` Step 3).
- `brands/{slug}/strategy.json#annual_goals[]` · target ROAS opérateur (kpi_metric ROAS, status active).
