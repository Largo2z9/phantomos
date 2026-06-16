---
name: brief-day
type: navigator
version: "1.3.1"
recommended_model: haiku
layer: production
reasoning_pattern: null
description: >
  Session-start orientation briefing. Reads workspace state across all brands
  and returns a tight operator-facing summary: portfolio health, pending validations,
  flags, suggested next actions. Zero deliverable, pure orientation.
  FR: "brief", "daily brief", "où j'en suis", "quoi de neuf", "fais-moi le point".
  EN: "brief", "daily brief", "what's up", "where am I", "status".
permissions:
  reads: [brand, product, offer, profile, learning, strategy, visual_identity]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: at least one brand in brands/ (excluding `_`-prefixed)
  postconditions: none, read-only
---

# Skill: brief-day

**CRITICAL:** this is a Navigator, invoked directly by the operator for orientation. **NEVER** produce a deliverable. **NEVER** suggest deep work. **ALWAYS** stay in read-only summary mode.

## Tone

Chairman briefing a partner who just walked in. Zero jargon, zero file paths, zero JSON. Plain language, scannable in 30 seconds.

Posture adapted to context: if multi-brand operator (portfolio / agency) → portfolio-lead → principal. If solo brand → senior operator → founder. If early-stage → coach → builder.

---

## Step 1 · Scan workspace state (silent)

Read in parallel, no operator visibility:

- `brands/*/status.json` (exclude `_`-prefixed) for each brand: completeness level, last activity, flags
- `brands/*/pending-validations.md` for each brand: count unchecked items per section (context / access / enrichment / skill-candidates)
- `brands/*/todos.md` for each brand: `## In Progress` + `## P0/P1` top entries
- `brands/*/learnings.json` latest 3 entries (date, fact short)
- `brands/*/brand.json` for each brand: `identity.brand_name` (display label), `audiences_index` (count + labels mère/sous), `_validated_by_operator` gates set
- `brands/*/products/*/spec.json` for each brand: product count + display name + spec completeness flag
- `brands/*/products/*/visual_identity.json` (if present) for each brand × product: `assets_canonical.packshot_front._canonical` presence + `_validated_by_operator` gate
- `brands/*/visual_identity.json` brand-level (if present): `assets_canonical.logo_canonical` / `badge_canonical{}` / `mascotte_canonical` / `pattern_canonical{}` slots filled vs empty
- `brands/*/angles/` or `learnings.json` angle hypotheses: count tested vs validated terrain
- `brands/*/_snapshot.md` digest for fast read fallback if granular JSONs missing
- `operator/profile.json`: preferences.conversation_register, identity.profile, preferences.tracking
- `session-state.md` last 10 activity log lines if present

**Si MCP google-calendar absent** · degraded mode silencieux (no agenda block dans le brief) + 1 ligne mesurée proactif en bas du brief ·
"Calendrier non branché · `connecte mes outils` quand tu veux l'agenda dedans"
**Si MCP supabase absent** · même pattern · degraded mode + 1 ligne proactive.

## Step 2 · Classify what matters (silent)

Bucket detected signals:

- **Brand health**: 1 line per brand · name, completeness level, days since last activity, flag count
- **Needs your call**: items in pending-validations marked critical or blocking (gate access missing on skills operator asked for, inferred audience not yet validated before planned deliverable, etc.)
- **Flags across portfolio**: cross-brand patterns (e.g. 3 brands missing Meta credentials, 2 brands with learnings_stale flag)
- **Next action suggestions** (2-3 max, ranked by impact)

## Step 2bis · Compose État brand · info système (silent, then surface · v2.54 posture investigation allégée)

**Quand surface.** Si l'opérateur a une seule brand active OU est focalisé sur une brand (last activity < 7 jours, ou brand explicitement mentionnée). Sinon, prefer le format portfolio multi-brands de Step 3 standard et garde l'état brand pour drill explicite.

**Doctrinal contract v2.54.** brief-day est un cas particulier · c'est de l'**état descriptif** (cartographie de ce qui est rempli vs vide), pas de la synthèse stratégique. La doctrine investigation-posture s'applique en mode allégé · chaque item signale sa nature (observé directement vs déduit), la sous-section "À noter" devient "À explorer si pertinent" (drill-down options, pas injonction), et le close affirme un move défendu plutôt que de rendre une question macro (mécanique du close en Step 3).

**Posture observé / déduit par item** ·
- `observé directement` (data Supabase status.json, scan brand.json sourcé, audience_index Supabase, learnings.json structurés) → item présenté tel quel, pas de flag explicite (default · le système est sourced).
- `déduit` (inférence agent sur l'état · ex "audiences inférées non-validées", "brand a mascotte récurrente mais slot vide", "spec partielle nécessite enrichissement") → marquer explicitement `(déduit)` en suffixe sur le label item.

**Hiérarchie 3 niveaux** (ordre canonique, jamais inversé) ·

### Niveau 1 · Identité brand (setup-once)

Ce qui définit qui est la brand. Setup une fois, stable ensuite.

- **Setup** · "complet" (si `wedge_complete: true`) OR "partiel" (si `draft`/`partial`) OR "pas encore engagé" (si `empty`) · observé directement (status.json sourced)
- **Audiences** · "N mappées (1 mère, N-1 sous-audiences)" si `audiences_index` populé. Sinon "pas encore mappées · se construit avec setup-brand". Si certaines audiences sont `validation_status: hypothesis` → ajouter `(N audiences encore en hypothèse · déduit, pas validées terrain)`.

### Niveau 2 · Inventaire produits & assets (ajouts continus)

Ce dont la brand dispose pour produire des créa. Bouge avec chaque ajout.

- **Produits** · "N (Display Name A, Display Name B, +K)" si N≤3 nommer tous, sinon top 3 + "+K autres". Pour chaque produit hero (top 2-3) ·
  - "{Display Name} · spec complète · photo officielle prête" si `spec.json` `complete` AND `visual_identity.assets_canonical.packshot_front._canonical: true` (observé directement)
  - "{Display Name} · spec complète · pas encore de photo officielle" + hint passif "récupérable depuis ton site OU à drop" si spec OK mais packshot absent
  - "{Display Name} · spec partielle (déduit · enrichissement upstream nécessaire)" si spec incomplète
- **Assets brand** (brand-level, cross-products) ·
  - **Logo** · "OK" si `visual_identity.assets_canonical.logo_canonical.path` présent. Sinon "pas encore renseigné · récupérable depuis ton site"
  - **Badges** · "N renseignés ({slug_humain_A}, {slug_humain_B})" si `badge_canonical{}` non-vide. Sinon "pas encore renseignés"
  - **Mascotte** · "OK" si présente, "pas applicable" si brand n'a pas de mascotte selon identité (default), "pas encore renseignée (déduit · si brand a mascotte récurrente)" si brand a mascotte récurrente mais slot vide
  - **Patterns** · "N renseignés" si `pattern_canonical{}` non-vide. Sinon "pas encore renseignés"

### Niveau 3 · Atlas vivant (earned par usage)

Ce que la brand a appris en lançant des campagnes. Se construit avec le temps, pas avec setup.

- **Angles testés** · "N hypothèses · K validés terrain" si `angles/` populé OR `learnings.json` contient angle_hypothesis entries (observé · learnings.json sourced). Sinon "0 angles encodés · se construit au fil des campagnes".
- **Campagnes lancées** · "N résultats encodés" si `learnings.json` contient campaign_result entries (observé). Sinon "0 résultats encodés · se construit au fil des campagnes".

### Sous-section optionnelle · "À explorer si pertinent" (v2.54 remplace "À noter")

Max **2 items** courts, drill-down options pour gaps fort impact downstream. Posture · drill-down options à arbitrer par l'opérateur, jamais injonction. Drop entièrement si brand en très bon état OU si rien d'actionnable.

Format canonique v2.54 (drill-down option · "Pour creuser X, on peut faire Y") ·

- Produit avec spec complète mais pas de photo officielle → "Pour préparer tes prochaines pubs {Display Name} avec produit pixel-exact, on peut récupérer la photo depuis ton site ou tu drop manuellement."
- 0 résultats campagnes encodés ET angles testés > 0 → "Pour passer tes angles d'hypothèse à validés terrain, il faut encoder les résultats de campagnes déjà lancées (ou attendre les premiers tests)."
- Logo brand absent ET >1 produit avec photo officielle → "Pour brander tes pubs pixel-exact, on peut récupérer le logo depuis ton site."
- Audiences inférées jamais validées ET deliverable planifié → "Pour passer tes audiences d'hypothèse à validées avant de produire, on peut lancer une écoute clients réelle (~8-12 min)."

**Jamais** dépasser 2 items. **Jamais** nommer skill en surface (`craft-packshot`, `import-asset`, `setup-brand`, `mine-voc`, etc.). **Jamais** flag technique (`_canonical`, `_validated_by_operator`, `audiences_index`). **Jamais** injonction (`tu dois`, `il faut`, `complete ceci`). **Jamais** "À noter" en wording (v2.51 ←) · toujours "À explorer si pertinent" en wording v2.54.

## Step 3 · Deliver the brief

**ALWAYS** in executive format. 5-7 bullets max for portfolio summary. **NEVER** dump raw data. Si focus mono-brand ou single-brand workspace, surface l'État brand 3 niveaux composé en Step 2bis à la place du Portfolio health.

**Template portfolio multi-brands** (adapt, never paste literally):

> **Portfolio health**
> - Northsense: Level 2 complete, last session 2 days ago. 1 flag (learnings_stale)
> - {brand B}: Level 1, last session today, clean
> - {brand C}: Level 1 draft, 4 days idle, `access_missing Meta`
>
> **Needs your call (2)**
> - Northsense inferred audience (Maghrebi/ME women) never validated, will contaminate next brief
> - {brand C} Meta access still pending client-side, blocking the audit you queued
>
> **Pattern I noticed**
> - 2 of your 3 brands miss Meta credentials. Worth batching a client outreach?
>
> **Suggested next**
> - Validate Northsense audience (15 min, unlocks brief-créa)
> - Or skip to {brand B} if you prefer momentum

**Template focus mono-brand** (adapt, never paste literally · v2.54 posture investigation allégée) ·

> **État brand · Glowco**
>
> Identité
>   Setup · complet
>   Audiences · 3 mappées (1 mère, 2 sous-audiences) · (3 audiences encore en hypothèse · déduit, pas validées terrain)
>
> Inventaire
>   Produits · 3 (Cell Boost, Glow Boost, +1)
>     Cell Boost · spec complète · photo officielle prête
>     Glow Boost · spec complète · pas encore de photo officielle (récupérable depuis ton site OU à drop)
>   Assets brand
>     Logo · pas encore renseigné · récupérable depuis ton site
>     Badges · pas encore renseignés
>     Mascotte · pas applicable
>     Patterns · pas encore renseignés
>
> Atlas vivant
>   Angles testés · 5 hypothèses · 0 validés terrain
>   Campagnes lancées · 0 résultats encodés
>
> À explorer si pertinent
>   - Pour préparer tes prochaines pubs Glow Boost avec produit pixel-exact, on peut récupérer la photo depuis ton site ou tu drop manuellement.
>   - Pour passer tes audiences d'hypothèse à validées avant de produire des angles paid, on peut lancer une écoute clients réelle (~8-12 min).
>
> Le levier qui paie en premier · côté Glow Boost la preuve manque (photo officielle absente, audiences encore en hypothèse), et la lecture la plus probable c'est que la vente se perd sur le doute avant l'acquisition. Je récupère la photo officielle depuis ton site pour préparer les visuels, et je lance l'écoute clients en parallèle pour figer les audiences avant de produire. Tu veux pivoter sur une autre brand, dis-le.

**ALWAYS** clore par un verdict de move défendu, pas une question macro rendue. Le move n'est pas prescrit par une forme · il SORT du raisonnement sur le substrat encodé · fais tourner la chaîne diagnostique sur ce que la brand a encodé (position → négatif → audience-du-mécanisme → priorité-éco → verdict, `docs/doctrine/strategic-diagnostic-doctrine.md`) et le prochain levier qui paie tombe de là, défendu en une ligne, appuyé sur un déduit qui porte sa confidence, jamais sur un fait inventé. Posture du close (affirme / ouvre / gate, à ne pas re-coller ici) · `docs/system/investigation-posture.md` + master `docs/system/contextual-intelligence.md`.

**L'out honnête est un move, pas un aveu** · si la data ne porte pas encore de verdict, nomme l'UNIQUE inconnu qui bloque + le chemin exact pour le lever (cf out exemplar). Inventer un verdict pour paraître décisif est le seul échec.

**Avant de surfacer le close, relis-le** · tranche-t-il un move défendu, ou décrit-il l'état puis repasse une question (le bulletin météo) ? Si météo, réécris-le.

Le drill-down macro reste une **affordance de redirect**, pas le close par défaut · si l'opérateur veut arbitrer, `AskUserQuestion` (load via `ToolSearch(select:AskUserQuestion)`) avec options dérivées de l'état observé, jamais pre-templated.

Banque sharp vs mushy du close (à imiter / à fuir) · `resources/canon/exemplars/close.md`.

---

## Step 4 · What this skill NEVER does

- **NEVER** propose to run a Producer or Orchestrator skill without explicit operator request. Daily-brief orients, doesn't commit.
- **NEVER** expose file paths, field names, routing destinations, D# numbers.
- **NEVER** list all brands if portfolio > 5. Summarize: "{5 active, 2 need attention, see show-progress for full list}".
- **NEVER** give a brief longer than 10 bullets, regardless of workspace complexity. Pare down ruthlessly.
- **NEVER** surface pourcentage, "X/Y completed", "level N", capability menu ("tu peux faire X") dans l'État brand section. Posture descriptive info-system, pas push.
- **NEVER** nommer un skill (`craft-packshot`, `import-asset`, `setup-brand`, `mine-voc`, etc.) en surface dans l'État brand ou la sous-section À explorer si pertinent. Le système est invisible, l'opérateur ne lit que langage métier.
- **NEVER** flag technique en surface (`_canonical`, `_validated_by_operator`, `assets_canonical`, `audiences_index`, `wedge_complete`). L'opérateur lit "photo officielle prête" pas "packshot canonical validated".
- **NEVER** injonction dans l'État brand (`tu dois`, `il faut`, `complete ceci`, `manque ceci`). Soft offer indirecte uniquement · "récupérable depuis ton site" (= hint passif), "Pour creuser X, on peut faire Y" (= drill-down option v2.54).
- **NEVER** plus de 2 items dans la sous-section À explorer si pertinent. Si rien à signaler, drop entièrement la sous-section.
- **NEVER** wording "À noter" (v2.51 ←) · toujours "À explorer si pertinent" (v2.54+) en wording cohérent doctrine investigation-posture.
- **NEVER** close en bulletin météo · montrer l'état SANS le lire puis tendre une question passive (*"Other actions ?"*, *"Anything else ?"*, *"lequel veux-tu creuser ?"*) · BANNI. Montrer les faits et lister les inconnues est BON · le ratage c'est l'absence de lecture experte plus le hand-off passif. Le close affirme un move défendu (mécanique Step 3). Drill-down macro dispo en redirect si l'opérateur veut arbitrer, jamais comme close par défaut.
- **NEVER** présenter items déduits comme observés. Si "audiences inférées non-validées", suffixer `(déduit)` explicite. Anti-pattern AP-1 doctrine BANNI · affirmer une hypothèse comme un fait, même en cartographie d'état.

## Edge cases

- **Zero brands** → redirect: *"No brand configured yet. Run setup-brand or drop a URL."*
- **Single brand** → format État brand 3 niveaux (Step 2bis), pas de Portfolio health. Plus sous-section À explorer si pertinent max 2 items si pertinent. Drop section À explorer entièrement si brand en très bon état OU rien d'actionnable.
- **Brand fraîchement setup, 0 produits encore** → Identité OK, Inventaire `Produits · pas encore renseigné · se construit avec ajout produit`, Atlas vivant `0 angles encodés · se construit au fil des campagnes`. Pas de sous-section À explorer (rien d'actionnable encore).
- **Brand sans visual_identity.json** → tous slots assets brand `pas encore renseigné · récupérable depuis ton site` (logo, badges, patterns) ou `pas applicable` (mascotte default).
- **Operator just landed, no session-state.md** → treat as fresh start, mention "welcome back" once if > 3 days since last activity
- **Mode detected from operator/profile.json.preferences.conversation_register** → (1) grounded = more explanation of what each item means, (4) technical = pure bullet points zero fluff

---

## Cross-refs

- `docs/system/investigation-posture.md` (v2.54 doctrine canon) · cartographier avant affirmer · mode allégé pour brief-day · état descriptif observé / déduit · "À explorer si pertinent" remplace "À noter" · close = verdict de move défendu (affirme / ouvre / gate), drill-down macro en redirect opérateur.
- `docs/system/contextual-intelligence.md` · master doctrine, no orphan output, jargon zéro en surface.
- `docs/system/operator-vocabulary-translation.md` · canonical translations interne → operator-facing.
- `resources/schemas/visual_identity.schema.json` v1.2 · slots assets_canonical (logo, badges, mascotte, patterns).
