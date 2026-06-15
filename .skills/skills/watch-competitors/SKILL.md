---
name: watch-competitors
type: producer
version: "1.2.0"
recommended_model: sonnet
layer: territoire
reasoning_pattern: null
consumes:
  - path: docs/doctrine/competitive-reading-doctrine.md
    min_version: 1.0.0
    note: "Doctrine d'interprétation des signaux · les 5 signaux ordonnés par fiabilité, la matrice nous × eux, la qualification des silences (opportunité / cimetière / désert), les 3 pièges (survivorship, copie d'angle, miroir). Les signaux Step 4 se LISENT avec cette doctrine, en contexte de LA marque, pas en checklist."
description: >
  Analyse les publicités Meta des concurrents d'une brand et produit un rapport
  de veille créative avec les angles, mechanics, et signaux d'opportunité observés.
  FR: "surveille mes concurrents Meta", "qu'est-ce que font mes concurrents sur Meta",
  "veille concurrentielle", "analyse les pubs des concurrents", "competitive Intel Meta".
  EN: "watch competitors on Meta", "competitor ads analysis", "Meta competitive intelligence".
permissions:
  reads: [brand, spectrum]
  writes: [brand, spectrum]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand.json existe avec market.competitors[] renseigné
  postconditions: validate-resources
  cadence: "weekly · chaque entrée external_intelligence porte run_id + observed_at (velocity_tier weekly) · un re-run dédoublonne par run_id et laisse la décroissance vieillir les signaux antérieurs, jamais un empilement · dégrade au lieu de stopper (un fetch raté laisse une trace horodatée, il ne disparaît pas)"
  independence: "Invocable SEUL par un cron pour rafraîchir la couverture marché du spectrum SANS rebuild l'atlas (l'indépendance des skills = le moteur de la carte vivante)."
---

## Tone

Rapport en langage business. L'opérateur lit des insights concurrentiels, pas des données brutes. Chiffres quand pertinents, conclusions actionables.

# Skill: Competitor Watcher

Analyse les publicités Meta des concurrents d'une brand.

À partir de `brand.json → market.competitors[]`, l'agent accède à la Meta Ads Library de chaque concurrent, extrait les créas actives, les catégorise selon l'angle-registry et creative-mechanics-registry du workspace, et produit un rapport de veille avec les signaux d'opportunité.

---

## Step 0 · Estamper le run_id (idempotence)

Générer `RUN_ID = wc-{YYYY-MM-DD}-{NNN}` (format canon, cf `mine-vom` `vom-2026-04-24-001`), même date que le nom de fichier du rapport. `NNN` = prochain index du jour, **zero-paddé sur 3 chiffres** (001 si premier run du jour, sinon dernier + 1 lu dans `brand.json#/market/external_intelligence[]` · 009 → 010, jamais `10` non-paddé · le schéma exige `[0-9]{3}`). Le `RUN_ID` est défini UNE fois ici · toute référence ultérieure (Step 5 en-tête, Step 6 payload + `--reason`, Output Format) le résout. C'est la clé de dedup de la cadence hebdo.

---

## Step 1 · Charger le contexte de la brand

Lire dans cet ordre :

1. **`brand.json`** → extraire :
   - `market.competitors[]` → liste des concurrents avec leur URL
   - `positioning.purchase_driver` → le driver de la brand (pain / desire / identity / etc.)
   - `positioning.brand_differentiation` → le positionnement actuel
   - `meta.vertical` + `meta.market`

2. **`shared-resources/registries/angle-registry.md`** → charger la taxonomie complète des angles. Ce sont les catégories d'analyse.

3. **`shared-resources/registries/creative-mechanics-registry.md`** → charger la taxonomie des mechanics. Ces deux fichiers sont la grille de lecture.

**Si `market.competitors[]` est vide ou absent (dégrade, ne stoppe pas) :**
→ Émettre quand même une trace de run : un rapport minimal (en-tête avec `RUN_ID` + méthode + `status: degraded` + raison "aucun concurrent renseigné") ET une entrée `external_intelligence` taguée `{run_id, observed_at, signal: "run dégradé · aucun concurrent renseigné", _source: "observed"}`. PUIS surfacer le next-step à l'opérateur : "Ajoute au moins un concurrent (nom + URL Meta Ads Library) dans `market.competitors[]` pour une vraie veille." Un fetch raté laisse une trace horodatée, il ne disparaît pas (sinon le cron hebdo ne sait jamais qu'il a tourné à vide).

---

## Step 2 · Collecter les publicités actives

Pour chaque concurrent dans `market.competitors[]` :

**Si MCP Meta Ads Library disponible :**
- Appeler l'outil MCP avec `advertiser_page_id` ou URL page Facebook du concurrent
- Paramètres : `active_status: ACTIVE`, `limit: 20`, `fields: [ad_creative_body, ad_creative_link_caption, ad_delivery_start_time, impressions]`
- Stocker les résultats dans une variable `$raw_ads_{competitor_slug}`

**Si MCP Meta Ads Library indisponible (fallback) :**
- Informer l'opérateur : "Je n'ai pas accès direct à Meta Ads Library. Pour chaque concurrent, ouvre `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={nom_concurrent}` et colle les textes des 5-10 pubs actives dans le chat."
- Attendre les inputs manuels
- Stocker dans `$raw_ads_{competitor_slug}`

**Si aucun résultat pour un concurrent :**
→ Logger "0 pubs actives trouvées pour {concurrent}" et continuer. Ne pas bloquer.

---

## Step 3 · Analyser chaque publicité

Pour chaque pub collectée, extraire :

| Champ | Comment l'identifier |
|-------|---------------------|
| `angle` | Comparer le message avec `angle-registry.md` → identifier l'angle dominant (1 angle par pub) |
| `mechanic` | Comparer la structure créative avec `creative-mechanics-registry.md` → identifier la mécanique (1-2 mechanics par pub) |
| `hook_type` | Question / Statement / Before-After / Statistic / Confession / Callout / Revelation |
| `awareness_level` | Unaware / Problem-aware / Solution-aware / Product-aware / Most-aware |
| `lever` | Fear / Desire / Rational |

Agréger par concurrent :
```
{concurrent_slug}:
  total_ads_analyzed: N
  angles_observed: [{angle: "transformation", count: 4}, ...]
  mechanics_observed: [{mechanic: "ugc", count: 6}, ...]
  dominant_angle: "transformation"  # le plus fréquent
  dominant_mechanic: "ugc"
  awareness_distribution: {problem_aware: 0.6, solution_aware: 0.3, ...}
```

---

## Step 4 · Identifier les signaux d'opportunité

**Doctrine d'interprétation obligatoire · `docs/doctrine/competitive-reading-doctrine.md`.** Les règles dures qui gouvernent ce step : (1) winners identifiés à la DURÉE de diffusion, pas au volume (budget ≠ mérite) · (2) chaque zone blanche QUALIFIÉE avant d'être présentée comme opportunité (opportunité / cimetière / désert · test VoC + claim + éco) · (3) le statu quo compte comme concurrent (l'alternative réelle du prospect, pas seulement les marques nommées) · (4) les signaux s'arbitrent contre le contexte de LA marque (stade, couverture VoC, cœur de cible), jamais déroulés en checklist · (5) la grammaire (mécaniques, hooks) se verse aux registres, les angles ne se copient pas (test de substitution).

Croiser les patterns concurrents avec la brand analysée :

**Angles over-indexés chez les concurrents** (> 60% des pubs sur un angle) :
→ Signal de saturation : éviter cet angle ou le contrarianer

**Angles absents chez les concurrents** :
→ Signal d'opportunité : whitespace potentiel

**Mechanics dominant la catégorie** :
→ Si même mechanic chez tous → hygiene. Si unique à un concurrent → propriété potentielle.

**Awareness gap** :
→ Si concurrents ciblent tous solution_aware → opportunité en problem_aware (top of funnel)

Format des signaux :
```
SIGNAL_1:
  type: "whitespace" | "saturation" | "mechanic_ownership" | "awareness_gap"
  observation: "[description factuelle]"
  implication: "[ce que ça signifie pour la brand]"
  suggested_action: "[angle ou mechanic à tester]"
  confidence: 0.7
```

---

## Step 5 · Produire le rapport

Générer `competitive-intel-{brand-slug}-{YYYY-MM-DD}.md` dans `brands/{brand}/strategy/` :

```markdown
# Competitive Intelligence · {brand.meta.name}
> Généré le : {date}
> Concurrents analysés : {liste}
> Pubs analysées : {total}
> Méthode : {MCP direct | input manuel}

---

## Vue par concurrent

### {concurrent_name}
- Angle dominant : {angle} ({count} pubs / {pct}%)
- Mechanics observées : {liste}
- Ton général : {lever} ({pct}%)
- Awareness ciblé : {distribution}
- Observations notables : [liste]

---

## Signaux d'opportunité

{liste des SIGNAL_X avec observation + implication + action suggérée}

---

## Recommandations pour la prochaine batch créative

1. **Angle à tester** : {angle whitespace identifié} · absent chez {N} concurrents sur {total}
2. **Mécanique à éviter** : {mechanic saturée} · utilisée par {N} concurrents
3. **Awareness à cibler** : {niveau sous-exploité} · {ratio concurrents qui l'utilisent}

---

## Sources

{liste des URLs Meta Ads Library consultées ou inputs manuels avec date}
```

---

## Step 6 · Proposer les insights au Context Engine

Pour les signaux à confidence ≥ 0.7, appeler `.skills/write-to-context.py` pour chaque insight :

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/brand.json#/market/external_intelligence/-" \
  --value '{"source":"Meta Ads Library","run_id":"{RUN_ID}","observed_at":"{YYYY-MM-DD}","signal":"{1-line observation}","tags":["competitor","creative-intel","{ANGLE_TAG}"]}' \
  --source inference \
  --confidence {0.7-0.9} \
  --mode proposed \
  --reason "watch-competitors run {RUN_ID}"
```

Un appel par signal. `--mode proposed` n'accepte que des dict values (stamps `_proposed/_source/_confidence` en place). Le `run_id` + `observed_at` vivent DANS le payload (pas seulement dans `--reason`) : `observed_at` est l'ancre de décroissance hebdo, `run_id` la clé de dedup d'un re-run.

Un appel par signal. Maximum 5 signaux par run.

---

## Step 7 · Pont vers la carte (`spectrum.coverage_market`)

**Le maillon qui ferme la matrice nous × eux (D#502/D#518).** Sans lui, un signal concurrentiel ne met à jour aucune cellule et reste une observation perdue (pitfall 5 de la doctrine). Conditionnel : ne tourne QUE si `brands/{slug}/spectrum.json` existe (sinon le terrain n'est pas encore cartographié, ce pont attend la phase 3).

Pour chaque signal de couverture concurrentielle (un concurrent diffuse / ne diffuse pas sur un usage × audience) :

1. **Résoudre la cellule cible.** Matcher le signal vers une `cells[]` du spectrum par `(audience_ref + awareness)` et l'`origin_axis` de l'angle observé. Le matching est un **jugement sémantique** (couche modèle, pas de gate dur · Master rule) : si le rapprochement est ambigu, demander UNE confirmation à l'opérateur, ne jamais forcer.
2. **Écrire `coverage_market`** sur la cellule : `covered` (le concurrent adresse pleinement) · `partial` · `blank` (personne n'adresse, observé). JAMAIS `unknown→autre` sans observation réelle.
3. **Pousser une `evidence_item`** sur la cellule : `{evidence_type:"behavioral", force:{strong si ad longue durée, weak si récente}, _source:"observed"|"inferred", ref:"{id/URL ad}", extracted_at:"{datetime}"}`. `inferred` est légitime et tagué, jamais maquillé en `observed` (D#503).
4. **Laisser `strategic_position` au champ dérivé** (ne pas l'écrire à la main) : il se calcule de `coverage_self × coverage_market` (battlefield / our-advantage / proxy-validated / whitespace) une fois `coverage_market != unknown`.

**Écriture spectrum** : read → merge par `cell_id` (préserver les cellules validated/scaled, ne jamais écraser une cellule prouvée) → write `--mode direct` (le writer refuse un fichier entier en `proposed`), même discipline que `map-angles` mode spectre.

Politique d'échec : une cellule dont la couverture marché n'a pas pu être observée garde `coverage_market: "unknown"` + un `lever` nommé (`watch-competitors`), jamais une valeur fabriquée.

---

## Output Format

- **Fichier markdown** : `brands/{brand}/strategy/competitive-intel-{brand-slug}-{YYYY-MM-DD}.md`
- **Proposals write-to-context** : `brands/{brand}/brand.json#/market/external_intelligence/-` (chaque entrée porte `run_id` + `observed_at`)
- **Pont carte** (si `spectrum.json` existe) : `brands/{brand}/spectrum.json#/cells[]` · `coverage_market` + `evidence_item` behavioral sur les cellules matchées (Step 7)
- **Log de run** : dernière ligne du rapport indique `RUN_ID`, `status` (ok / degraded), et nombre de proposals + cellules mises à jour

---

## Hard Rules

- **NEVER inventer des pubs.** Si une pub n'est pas collectée, elle n'existe pas. Pas d'hallucination sur les créas.
- **NEVER écrire directement dans brand.json.** Toujours ``.skills/write-to-context.py` (canonical channel · see capture-learning Step 4 for the exact Bash invocation)` en mode `proposed`.
- **ALWAYS indiquer la méthode de collecte** (MCP direct ou input manuel) dans le rapport.
- **ALWAYS utiliser l'angle-registry et le creative-mechanics-registry comme grille.** Ne pas inventer de nouvelles catégories dans le rapport.
- **Max 5 proposals** par run. Si plus de 5 signaux, prioriser par confidence décroissante.
- **Si 0 pub collectée** pour tous les concurrents → dégrader, pas stopper : émettre un rapport `status: degraded` + une entrée `external_intelligence` horodatée du run à vide, PUIS demander à l'opérateur de vérifier `market.competitors[]`. Le cron hebdo doit savoir que le run a tourné (sinon il croit n'avoir jamais tourné).
- **Pont spectrum honnête** · `coverage_market` ne passe jamais de `unknown` à une valeur sans `evidence_item` observée/inférée taguée · `strategic_position` reste dérivé, jamais écrit à la main · matching de cellule ambigu → UNE confirmation opérateur, jamais forcer (Master rule · le matching est sémantique).
