---
name: phantom
description: Cockpit PhantomOS. Sans arg, vue workspace (tous brands + état global). Avec un brand slug, vue détaillée du brand. Read-only.
version: v2.87.5
patch_notes_v2_87_5:
  - "v2.87.5 (P1 todo-brand + P4 schedules section) · NEW mode todo-brand `/phantom {brand} todo` brand-level proactif (cf `phantom-modes/todo-brand.md`) · 4 blocs canon · Actions + Connectors + Schedules + Atlas completeness. NEW directive cockpit brand `/phantom {brand}` · ajouter section SCHEDULES (à côté de ALERTES + ÉTAT + ACTIONS) listant schedules actifs `brands/{slug}/scheduled.json` + suggestions schedules manquants relevants (mine-voc weekly · trendtrack-enrich-brand weekly · audit-creative-fatigue monthly · brief-day daily · watch-competitors weekly · analyze-perf weekly · trendtrack shop profile monthly). Storage canon · `brands/{slug}/scheduled.json` brand-level avec skill + frequency + next_run_at + trigger_mechanism (CronCreate predictable récurrent OR ScheduleWakeup dynamic /loop monitoring conditionnel) + last_run_at + last_status + rationale. Canon `scheduled-routines.md` R&D level à promouvoir runtime workspace-template (backlog v2.88.0+). Cross-ref memory canon `brand_connectors_onboarding_canon` matrice 7 skills schedulables + 3 triggers proactivité (post-setup brand + cockpit /phantom + brand-todo entry). Enforcement runtime hardcoded backlog v2.88.0+ implementation. Backward compat strict additif (cycle cockpit preserved · seul NEW section schedules additive)."
---

# /phantom, cockpit

Vue synthétique du workspace PhantomOS. Lecture seule, aucune mutation. Read top to bottom before acting.

## Mode detection

Navigation pattern is **terminal-like**: `/phantom` lands at the workspace level (even with a single brand), `/phantom {slug}` drills into a brand, `/phantom {slug} {entity}` zooms further into a specific entity within a brand. The operator learns the system the way they learn `cd` and `ls`: top-down, never short-circuited.

Check the user's argument :

| Argument | Mode |
|---|---|
| empty (just `/phantom`), 0 brand encodé | **bootstrap** : message d'amorce vers `/tour` |
| empty, ≥1 brand encodé | **workspace** : always shows the workspace-level view, regardless of brand count. Operator drills explicitly via `/phantom {slug}`. |
| `workspace` or `all` | **workspace** : alias, same as empty when ≥1 brand exists |
| brand slug (e.g. `/phantom vitatone`) | **brand** : cockpit détaillé du brand |
| brand slug + entity (e.g. `/phantom vitatone audiences`) | **entity-drill** : zoom dense sur une entité spécifique du brand |
| brand slug + entity + item (e.g. `/phantom glowco audiences chute-active`) | **item** : preview d'un item unique (audience, angle, product) |
| `search {keyword}` (e.g. `/phantom search chute`) | **search** : grep cross-brand sur slugs, names, voc, learnings |
| `recent` ou `recent {N}` | **recent** : timeline des N dernières mutations (default 10) |
| `todo` | **todo** : vue agrégée des next-suggested cross-brand priorisés (workspace-level) |
| brand slug + `todo` (e.g. `/phantom vitatone todo`) | **todo-brand** : vue brand-level proactive (actions + connectors + schedules + atlas gaps · canon v2.87.5+ P1 · cf `phantom-modes/todo-brand.md`) |
| `?` ou `help` | **help** : cheatsheet auto-générée de tous les modes |
| `canon` | **canon-index** : liste des atlas du métier disponibles (workspace-level, transversal aux brands) |
| `canon {atlas}` | **canon-layers** : liste des couches d'un atlas (ex: `/phantom canon copy`) |
| `canon {atlas} {layer}` | **canon-tools** : liste des outils d'une couche (ex: `/phantom canon copy hooks`) |
| `canon {atlas} {layer} {tool}` | **canon-tool-card** : fiche détaillée d'un outil canon (ex: `/phantom canon copy hooks curiosity-gap`) |
| `{brand} briefs` | **briefs-drill** : DB Briefs créatifs (liste, statut, lien angle source) |
| `{brand} tests` | **tests-drill** : DB Tests live + résultats observés + verdict winner_proxy |
| `{brand} matrix` | **matrix-drill** : output `score-matrix` (matrice scorée + top territoires + trous) |
| `{brand} frictions` | **frictions-drill** : table frictions usage par severity + audiences affected (sub-product OWNED) |
| `{brand} roadmap` | **roadmap-drill** : phases chronologiques + current highlight + priorities |
| `{brand} funnel` | **funnel-drill** : couverture TOF/MOF/BOF + trous détectés |
| `{brand} services` | **services-drill** : services/packages business_model=service |
| `{brand} atlas` | **atlas-overview** : vue d'ensemble atlas brand (synthèse 6 entités + dérivés) |
| `doctrine` | **doctrine** : rend doctrine cartographie compositionnelle (méthode + équation V3.1) |
| `doctrine audiences` | **doctrine-audiences** : framework cartographie audiences (4 questions) |
| `{brand} audiences` | **audiences-tree** : arbre hiérarchie audiences + chevauchements |
| `{brand} products {p_slug} mechanisms` | **mechanisms-drill** : array `mechanisms[]` typé depuis `spec.json` |
| `{brand} products {p_slug} benefits` | **benefits-drill** : array `benefits[]` (chain functional/emotional/identity) |

---

## Mode bootstrap

```
PhantomOS · workspace vide
══════════════════════════════════════════════
Aucun brand encodé pour l'instant.

Pour démarrer le setup d'un premier brand · `/tour`
Pour parcourir les fonctions disponibles · `/skills`
```

Stop ici.

---

## Mode workspace

Vue globale du workspace, multi-brand + opérateur + capacités.

### Sources à lire (read-only)

1. `operator/profile.json` → identité opérateur, register, contexts.
2. `operator/awareness.json` → tour status, concepts introduits.
3. `brands/` → liste des dossiers brand (ignorer ceux préfixés `_`).
4. Pour chaque brand : `brands/{slug}/_snapshot.md` (digest) + `brands/{slug}/status.json` (level).
5. `.skills/_manifest.json` → count skills shipped vs custom.
6. `session-state.md` racine → last session timestamp.
7. `connected-sources.json` racine (si existe) → sources globales connectées (cross-brand).

### Format de rendu workspace

```
PhantomOS · workspace
══════════════════════════════════════════════
Opérateur       {operator_name_or_id}
Fonctions       {N} actives ({M} custom)
Dernière session                {time_ago}

Brands ({count})
{brand_lines}

Cross-brand
Tests actifs                    {total_active_tests}
Sources connectées globales     {global_sources_summary}

Actions prioritaires
{suggested_actions}

Suggestions automatiques
{daemon_patterns_or_silence}

Pour explorer un brand · `/phantom <brand_slug>`
Pour les fonctions disponibles · `/skills`
```

`daemon_patterns_or_silence` lit le buffer pattern-detection (cross-skills, recurring frictions, decision reversals, encoded fact drift). Si présents, lister 1-3 patterns détectés sous forme paste-ready. Sinon afficher *"aucune suggestion daemon active"*. Source : `docs/system/pattern-detection-triggers.md`.

### Brand lines (mode workspace)

Une ligne compacte par brand, ordonnée par activité récente :

```
{icon} {slug}              L{level}    {entity_summary}    last {time_ago}
```

Icônes (canon unifié v2.79.2) :
- `✓` : actif (last session < 7j) et niveau ≥ L2
- `◐` : actif mais sub-L2, ou L2+ mais inactif (7-30j)
- `○` : dormant (> 30j sans session)

`entity_summary` : count condensé "{products}P / {audiences}A / {angles}An / {tests}T". Skip si entité absente.

Exemples :
```
✓ vitatone              L2     1P / 5A / 8An / 3T    last 14h
◐ peaktrek            L1     1P / 2A / 0An         last 6d
○ northsense           L2     1P / 4A / 5An         last 47d
```

### Cross-brand metrics

- **Total tests actifs** : somme des `tests actifs` de chaque brand (entries learnings.json type=test-result, status absent ou inconclusive ou fatigued).
- **Connected sources globales** : si `connected-sources.json` racine existe (sources cross-brand comme un Meta Business Manager partagé), lister les plateformes avec last_sync agrégé. Sinon dire "(per-brand only)".

### Next suggested workspace-level

3 propositions max, ordonnées par priorité. **Each line MUST be a paste-ready command, not a conversational suggestion.** Format : *"  · `{exact natural-language command}` ({why, in one short clause})"*. The operator copies the back-tick content into the next prompt and the agent picks it up.

Sources :
- Brand dormant > 60j → *"  · `archive {slug}` ({slug} sans activité depuis {N} jours)"*
- Tests fatiguing dans plusieurs brands → *"  · `refresh angles fatigués sur {slug-le-plus-fatigué}` ({N} angles ROAS en chute)"*
- Operator profile incomplet → *"  · `densifie mon profil opérateur` (3 champs manquants : stack actuelle, register, contexte macro)"*
- Skill `audit-meta-account` jamais run sur un brand actif → *"  · `audit Meta sur {slug}` (token connecté, jamais audité)"*
- Niveau de contexte global moyen sub-L2 → *"  · `enrichis le contexte de {slug}` (L1, le brand le plus en retard)"*

Anti-pattern : *"  · Lancer un audit Meta dès que possible"* (passif, l'opérateur doit re-formuler). Always paste-ready, always specific.

---

## Mode brand

Vue détaillée d'un brand spécifique. **Page sobre structurée 4 sections (v2.79.2+) · ALERTES · ÉTAT · ACTIONS · Drill footer.** Adaptive selon `brand.json#identity.business_model` v2.4 NEW. Iconographie unifiée canon · `✓` complet · `◐` partiel · `○` vide · `✗` absent · `⚠` critique.

### Sources à lire (read-only, dans l'ordre)

1. `brands/{slug}/_snapshot.md` (digest 1-2KB pré-généré). Si absent, déclencher `python3 .skills/build-brand-snapshot.py {slug}` puis re-lire.
2. `brands/{slug}/status.json` → `wedge_complete`, `completeness_scores`, niveau de contexte L1/L2/L3.
3. `brands/{slug}/brand.json` → `meta.name`, `meta.sector`, `meta.updated`, `identity.business_model`, `identity.business_model_signals`.
4. `brands/{slug}/products/` → liste, count, last update par produit, validation_status, hero flag.
5. `brands/{slug}/audiences/` → liste, count, validation_status, verbatim_density, last_mining_at par audience.
6. `brands/{slug}/angles/` (si existe) → count par validation_status, lineage_signal, ROAS chute 14j.
7. `brands/{slug}/strategy.json` → `meta.updated`, `current_focus`.
8. `brands/{slug}/learnings.json` → count entries, count tests par status, tests actifs, promoted_count.
9. `brands/{slug}/connected-sources.json` (si existe) → liste plateformes connectées avec last_sync.
10. `brands/{slug}/session-state.md` (si existe) → last brand-scoped session.
11. `brands/{slug}/frictions/` (si existe) → count, severity_score max, N_bloquantes (≥7).
12. `brands/{slug}/roadmap.json` (si existe) → current_phase, priorities[].
13. `brands/{slug}/briefs/` (si existe) → count, status breakdown (draft/shipped/validated).
14. `brands/{slug}/matrix/latest.json` (si existe) → updated_at, top_territory.
15. `brands/{slug}/pending-validations.md` (si existe) → décisions en attente.
16. `.phantom/active-tasks.json` (si existe) → skills en cours runtime (mine-voc, score-matrix, sync-notion-atlas).
17. `.phantom/context-engine-events.jsonl` → mutations 24h.

### Format de rendu brand (4 sections obligatoires v2.79.2+)

```
{Brand_name}                                                  Cartographie {pct}%
{business_model_label} · {niche}                              {key_metric_brand}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ALERTES                                                          Sévérité
  ─────────────────────────────────────────────────────────────────────
  {alerte 1}                                                   critique
  {alerte 2}                                                   critique
  {alerte 3}                                                   majeur
  {alerte 4}                                                   majeur

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ÉTAT
  ─────────────────────────────────────────────────────────────────────
  Marque              ✓ encodée
  Produits ({N})      ◐ partiels       {commentaire condensé}
  Audiences ({N})     ◐ {x sur N} sourcée  {commentaire condensé}
  Angles paid ({N})   ○ vides
  Stratégie           ✗ pas de focus
  Roadmap             ✗ absente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ACTIONS
  ─────────────────────────────────────────────────────────────────────
  1. {Action verbalisée}                          {débloque X}
  2. {Action verbalisée}                          {débloque Y}
  3. {Action verbalisée}                          {débloque Z}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Drill                /phantom {slug} {audiences | products | strategy}
  Rechercher           /phantom search "<terme>"
  Aide                 /phantom ?

  ─────────────────────────────────────────────────────────────────────
  ✓ complet  ◐ partiel  ○ vide  ✗ absent  ⚠ critique
```

**Grammaire canon v2.79.2.** 4 sections strictes · ALERTES (sévérité criticité) · ÉTAT (santé encodage entités) · ACTIONS (top 3 numérotées) · Drill footer (3 lignes + légende iconographie). Density modérée · whitespace généreux · une chose par ligne · séparateurs ━━━ entre sections. Pas de tableaux nested 3 métriques empilées. Pas de skill names exposés (verbalisation action backstage).

### Section 1 · Header

Header sobre 2 lignes · brand name + cartographie pct (right-aligned) · business_model label + niche + key metric brand (right-aligned).

- **Cartographie pct** · lecture `status.json#completeness_scores` · convertir niveau L1/L2/L3 + completeness_scores composite en pct unique 0-100% (~33% par niveau atteint).
- **Modèle business** · lecture `brand.json#identity.business_model` v2.4 NEW · label opérateur-facing canonique ·
  - `DTC` → "DTC pure"
  - `service` → "service (B2B)"
  - `hybrid` → "hybrid ({primary} + {secondary})" · depuis `business_model_signals`
  - `subscription` → "subscription / SaaS"
  - `marketplace` → "marketplace"
  - Fallback (champ absent) → "modèle à cadrer"
- **Key metric brand** · ARR estimée OR niche + sous-secteur OR tests live count (selon ce qui est observable).

### Section 2 · ALERTES (santé brand actionnable)

Scan automatique de signaux. **Une seule liste, ordre sévérité descendante (critique → majeur → mineur).**

Sources scan ·
- Angles essoufflés (`status: fatigued` OR ROAS chute ≥30% sur 14j) · sévérité critique
- Frictions bloquantes (`severity_score ≥7`) · sévérité critique
- Décomposition produit incomplète (mécanismes/bénéfices vides) · sévérité majeure
- Sourcing audiences insuffisant (`verbatim_density < 5` OR `last_mining_at > 90j`) · sévérité majeure
- Stage business indéterminable (financiers absents) · sévérité majeure
- Briefs draft depuis >5j · sévérité mineure
- Décisions en attente (`pending-validations.md` non-empty) · sévérité variable selon contenu

Format ligne · `{alerte verbalisée}{whitespace}{sévérité}`. Max 6 alertes affichées. Si zéro alerte, afficher `✓ Brand serein` OU skip section entière (whitespace conservé).

**Tâches de fond actives** · scan `.phantom/active-tasks.json` ou équivalent · si présent, surface ligne unique en bas section ALERTES · `◐ {N} tâche(s) de fond en cours · {synthèse 1 ligne}`. Skip si zéro.

### Section 3 · ÉTAT (santé encodage entités)

**Rendering adaptatif par `business_model`. Cf section dédiée "Business model adaptation" plus bas pour la table complète.** Liste plate · une entité par ligne · icône canon unifiée + label + commentaire condensé. Pas de tableaux nested 3 métriques empilées.

#### Si `business_model: DTC` (default)

```
  Marque              ✓ encodée            {identity_summary 1 ligne}
  Produits ({N})      {✓◐○✗}              {commentaire condensé · ex "spec partielle"}
  Audiences ({N})     {✓◐○✗}              {commentaire · ex "1 sur 5 sourcée"}
  Angles paid ({N})   {✓◐○✗}              {commentaire · ex "vides"}
  Pubs Meta ({N})     {✓◐○✗}              TOF/MOF/BOF {N/M/K} · {live}/{fatigued}
  Briefs ({N})        {✓◐○✗}              {N_draft} draft · {N_shipped} shipped
  Stratégie           {✓◐○✗}              {focus 1 ligne OU "pas de focus"}
  Roadmap             {✓◐○✗}              {current_phase OU "absente"}
  Learnings           {✓◐○✗}              {recent_count} récents
```

Note ontologie pure v2.64 · pain_points + objections sont sub-folder dans audiences/{slug}/ (expression subjective audience-specific) · frictions sub-folder dans products/{slug}/ (usage produit-specific). Plus de top-level brand-wide sections séparées. Drill via `/phantom {brand} audiences {slug}` (audience-drill 360° expose pain + objections inline) et `/phantom {brand} products {slug}` (product-drill 360° expose frictions inline).

#### Si `business_model: hybrid`

```
  Marque              ✓ encodée            {identity} · {primary} + {secondary} ({weight})
  {Primary_layer}     {✓◐○✗}              {locations cartographiées count OR "à cartographier"}
  Produits ({N})      {✓◐○✗}              {idem DTC}
  Audiences ({N})     {✓◐○✗}              2 layers · {N_primary} {primary_layer} · {N_buyer} acheteurs
  Angles paid ({N})   {✓◐○✗}              {idem DTC}
  Pubs Meta ({N})     {✓◐○✗}              {idem DTC + campagnes locales}
  Stratégie           {✓◐○✗}              {idem DTC}
  Roadmap             {✓◐○✗}              {idem DTC}
```

#### Si `business_model: service`

```
  Marque              ✓ encodée            {identity} · service-only B2B
  Services ({N})      {✓◐○✗}              {pricing_tier} · {N_outcomes} outcomes
  ICPs B2B ({N})      {✓◐○✗}              sales-cycle · {N} ICPs cartographiés
  Angles lead-gen     {✓◐○✗}              case-study × {N} · contrarian × {N}
  Pipeline deals      {✓◐○✗}              {N_qualifiés} · MRR projeté {amount}
  Case studies        {✓◐○✗}              {N} publiés
  Stratégie           {✓◐○✗}              {focus 1 ligne}
  Roadmap             {✓◐○✗}              {current_phase}
```

#### Si `business_model: subscription` OR `marketplace`

Adapter le label "Produits" en "Plans / Tiers" (subscription) ou "Catalog / Sellers" (marketplace). Audiences = users/subscribers ou acheteurs/vendeurs (2 sides). Productions créatives = retention angles, churn-fighters (subscription) ou liquidité matching (marketplace).

#### Icônes status entités (canon unifié v2.79.2)

- `✓` : entité encodée, complète et fraîche (updated < 7j)
- `◐` : entité encodée mais partielle (gaps OR stale 7-14j OR completeness < 70%)
- `○` : entité absente / vide / pas encore encodée
- `✗` : entité absente ET bloquante pour le flow brand
- `⚠` : critique (stale > 90j OU tests en chute libre OU décision en attente bloquante)

Légende affichée en pied de chaque output `/phantom {brand}`. Ordre stratégie & ops · Stratégie → Roadmap → Learnings (frictions exposées via product-drill).

### Section 4 · ACTIONS (top 3 numérotées)

Max 3 actions verbalisées, ordonnées par priorité descendante. **Format canon strict** ·

```
  1. {Action verbalisée}                          {débloque X}
  2. {Action verbalisée}                          {débloque Y}
  3. {Action verbalisée}                          {débloque Z}
```

Hard rules ·
- Action verbalisée en langue naturelle opérateur · jamais skill name exposé (skill route backstage)
- Rationale 1 ligne max · format `débloque {entité OR état}` OR `règle {alerte critique}`
- Pas de backtick + texte naturel mixés (texte plain uniquement)
- Si zéro action prioritaire (brand mature serein), skip section et afficher *"Brand serein. Profite du calme."*

Sources d'extraction (action verbalisée) ·
- Tests fatiguing → "Refresh l'angle essoufflé sur {audience}" · débloque ROAS
- Audiences sans voix client → "Récupère la voix client manquante sur {N} audiences" · débloque sourcing
- Frictions bloquantes → "Traite la friction bloquante sur {audience}" · règle severity 9/10
- Briefs draft stale → "Relance le brief en draft depuis {N} jours"
- Stale > 14j sur entité critique → "Mets à jour {entité}" · dernière modif {N}j
- Niveau sub-L2 → "Densifie le contexte brand" · {N} champs manquants
- Décomposition produit vide → "Cartographie les mécanismes du produit hero" · débloque copy + paid
- Stage business indéterminable → "Cadre le stage business (ARR / proof points / domain age)"

Anti-pattern strict · skill names exposés ("Lancer mine-voc dès que possible", "Run produce-paid-angles") · backtick + commande paste-ready dans action. Le `/phantom` v2.79.2 verbalise · l'agent route le skill backstage si l'opérateur valide.

### Section 5 · Drill (footer minimaliste, max 3 lignes + légende)

Format strict 3 lignes navigation + légende iconographie au pied ·

```
  Drill                /phantom {slug} {audiences | products | strategy}
  Rechercher           /phantom search "<terme>"
  Aide                 /phantom ?

  ─────────────────────────────────────────────────────────────────────
  ✓ complet  ◐ partiel  ○ vide  ✗ absent  ⚠ critique
```

Substitutions selon business_model ·
- `service` · remplace `products` par `services`
- `subscription` · remplace `products` par `plans`
- `marketplace` · remplace `products` par `catalog`

Pas de listing exhaustif entités drillables, pas de "Bibliothèque métier", pas de "Historique changements". L'opérateur découvre les autres entités via `/phantom ?`.

---

## Scaling rules · produits dans ÉTAT

Règle universelle de rendering applied à la sous-section "Ligne produits" (ou équivalent business_model) de Matière brand.

| N produits | Rendering mode brand |
|---|---|
| 0 | Skip section · CTA "premier produit · `snapshot {brand} avec {url}`" |
| 1-3 | Full L2 nested (composition, mécanismes, bénéfices, offres, pubs liées) · 5 lignes par produit |
| 4-10 | Compact 1 ligne par produit · `├─ {slug} {hero_badge} · {validation_status} · {N_offres} · {N_audiences} · {N_angles} · {N_pubs}` |
| 11-30 | Top-5 par activité créa expanded + `└─ {N-5} autres SKUs · /phantom {brand} products` |
| 30+ | Top-5 par activité + groupes par `spec.identity.taxonomy` ou category si présent + obligation drill `/phantom {brand} products` pour list complète |

**Trigger "activité créa"** · score composite descending sur `(N_angles_live × 2) + N_pubs_winners + (N_tests_running × 0.5) + last_mutation_recency_weight`. Pas exposé à l'opérateur.

**Application services / plans / catalog** · même barème scaling. Substituer slug entity correspondante.

---

## Sub-line metrics canonisées

Règle universelle · sub-line surface ratios + top-1 nominal qualitatif, **JAMAIS volumes bruts seuls**. Si une ligne ne peut être enrichie (entité absente, count 0), basculer en empty state pédagogique (cf section *Empty states*).

| Entité | Sub-line v2 canonique |
|---|---|
| Produits (1) | `{count} · {validation_status majoritaire} · TOP-bénéfice: {benefit_name}` |
| Audiences (v2.64) | `{count} mères + {N} sous-poches · verbatims {sparse/medium/dense} · {N_pain} pain · {N_objections} objections (sub-folder OWNED)` |
| Angles | `{count} ({live}/{fatigued}/{validated}) · {lineage_objection_count} dérivés objections` |
| Frictions (v2.64 sub-product) | `{count} · severity max {max}/10 · {N} bloquantes (≥7) · sub-folder OWNED products/{slug}/frictions/` |
| Funnel Meta | `{creatives_count} live · TOF/MOF/BOF {a}/{b}/{c} · {winners} winners scalés` |
| Roadmap | `{current_phase} · {N} priorités · {due_date_top_priority}` |
| Strategy | `{focus_1_line} · target {kpi}: {value}/{period}` |
| Learnings | `{recent_count} récents · {promoted_count} promus canon` |
| Matrix | `{updated_time_ago} · top territoire {description}` |
| Briefs | `{N_draft} draft · {N_shipped} shipped · {N_validated} validés` |
| Tests | `{N_live} live · {N_winners} gagnants · {N_fatigued} essoufflés` |

**Densité qualitatif** · `sparse` (<5 verbatims), `medium` (5-30), `dense` (>30). Jamais exposer le number brut comme métrique principale.

**Top-1 nominal** · récupéré depuis `pain_points[0].label` ou `benefits[0].label` ranked par `priority_score` si présent, sinon premier de l'array. Pas de calcul ML, juste lecture de la sub-structure.

---

## Business model adaptation

Section dédiée explicitant comment le rendering brand mode adapte les entités présentées selon `brand.json#identity.business_model` v2.4 NEW. Le vocabulaire opérateur-facing change ; la grammaire 5 sections reste identique.

| business_model | Matière brand | Production créative | Stratégie & ops |
|---|---|---|---|
| `DTC` | brand · ligne produits · audiences | angles · pubs Meta · briefs | frictions · roadmap · strategy · learnings · matrix |
| `hybrid` | brand · {primary} (réseau cliniques OU showrooms OU agence locale) · ligne produits · audiences 2 layers | angles · pubs Meta · briefs · campagnes locales | idem DTC + opérations terrain |
| `service` | brand · services/packages · ICPs B2B | angles lead-gen · pipeline deals · case studies | frictions delivery · roadmap services · strategy · learnings · matrix |
| `subscription` | brand · plans/tiers · audiences (subscribers vs trial) | angles acquisition · churn-fighters · onboarding flows | frictions churn · roadmap features · strategy MRR · learnings · matrix |
| `marketplace` | brand · catalog/sellers · audiences (buyers vs sellers) | angles 2 sides · liquidité matching · trust signals | frictions liquidité · roadmap features · strategy GMV · learnings · matrix |

**Order de surface** ·
1. **Matière brand** d'abord (substrate, ce sur quoi tout repose)
2. **Production créative** ensuite (ce qui en sort)
3. **Stratégie & ops** en dernier (gouvernance, signaux, prioritisation)

**Cas hybrid** · le `primary` layer (typiquement réseau physique, cliniques, showrooms) surface AVANT la ligne produits parce qu'il représente le volume business dominant. Le `secondary` layer (e-com produit) reste accessible mais ne masque pas le primary.

---

## Mode entity-drill

`/phantom {brand_slug} {entity}` zooms on one entity within the brand. Dense, no top-level KPIs, no connected sources, no other entity rows. The operator chose the entity so the rendering goes deeper than brand mode allows in 60-70 lines.

**Supported entities v2.64** · `audiences`, `angles`, `products` (alias `produits`), `services`, `offers`, `strategy`, `learnings`, `frictions` (sub-product OWNED), `roadmap`, `briefs`, `tests`, `matrix`, `funnel`, `pipeline`. **REMOVED v2.64** · `pain-points` + `objections` (top-level brand-wide modes redondants · sub-folder OWNED expression subjective audience-specific · drill audience expose tout natif via entity-drill audience 360°).

### Pattern enrichi (universel)

Chaque entity-drill v2.57 rend ·
1. **Header breadcrumb** · `workspace > {brand} > {entity}`
2. **Synthèse compact** · sub-line metrics canon (cf section dédiée)
3. **Liste items** · top-N selon scaling rules · ordre par pertinence (ROAS / activity / severity selon entity)
4. **Cross-refs visibles** · e.g. audiences drill montre angles rattachés, frictions drill montre audiences affected
5. **Actions prioritaires** · 3-5 paste-ready dérivées du drill context
6. **Drill profondeur explicite** · drill item, drill sibling, retour brand

### Common header (all entity drills)

```
workspace > {brand} > {entity}
══════════════════════════════════════════════
{sub-line metrics canon}
```

Then entity-specific body, then **Actions prioritaires** + **Drill suivant** blocks.

### `audiences` · audiences-tree enrichi

Routing override · `/phantom {brand} audiences` invoke audiences-tree mode externe (cf section *Mode audiences-tree* + `.claude/commands/phantom-modes/audiences-tree.md`).

**v2.57 enrichissement** · audiences-tree rend l'arbre hiérarchie + chevauchements + sub-counts (pain points + objections + verbatim density qualitatif). Ajout des cross-refs · pour chaque audience, lister les angles_derived[] et frictions_affecting[] inline si présents.

**v2.64 ontologie pure** · pain_points + objections sont sub-folder OWNED dans `audiences/{slug}/pain_points/` + `audiences/{slug}/objections/` (expression subjective audience-specific). Le drill `/phantom {brand} audiences` (list-level) montre les sub-counts pain/objections inline · le drill `/phantom {brand} audiences {slug}` (entity-drill audience 360°, cf section dédiée plus bas) expose le détail complet inline.

Format ligne audience ·

```
{slug}    {scope}    {validation_label}    pain: {filled|vide}    voice: {filled|vide}    → {applies_to}    {N_angles} angles · {N_pain} pain · {N_objections} objections
   ├─ {sub_slug}    ...
```

`applies_to` formatting · cf rules existing audiences-tree (lit `meta.applies_to_products[]`, fallback `meta.product_id` legacy).

End with paste-ready · mine-voc sur missing pain, drill audience complète {slug} 360°, valider hypothesis blocks, merge low-signal sub-audiences.

### `audiences {slug}` · entity-drill audience 360° complète (v2.64)

`/phantom {brand} audiences {slug}` rend la fiche complète d'une audience. **Ontologie pure v2.64** · 9 schemas pertinents rendus 360° (profile OWNED + pain_points sub-folder OWNED + objections sub-folder OWNED + cross-refs inbound depuis 6 autres schemas).

Lecture · `brands/{brand}/audiences/{slug}/profile.json` + `brands/{brand}/audiences/{slug}/pain_points/*.json` + `brands/{brand}/audiences/{slug}/objections/*.json` + inverted index cross-refs.

Header breadcrumb ·

```
workspace > {brand} > audiences > {slug}
══════════════════════════════════════════════
{audience_name} · {scope} · {validation_label}
{verbatim_density} verbatims · {N_pain} pain points · {N_objections} objections
```

Rendering · 9 sections obligatoires.

**Section 1 · Profile (OWNED)**

```
Profile
   identity              {persona_archetype} · {role} · {buyer_user_split}
   psychology            decision_process · purchase_driver · market_position
   voice                 tone · key_expressions · lexical_signatures
   behavior              touchpoints · objection_frequency · purchase_cadence
   benefits              chain functional/emotional/identity
   meta                  research_meta · sourcing tags · last_mining_at
```

**Section 2 · Pain Points (sub-folder OWNED)**

Liste PNT-NN entries cette audience. Cap 10 (top severity desc). Format ligne ·

```
Pain Points ({N})
   PNT-01  {label}                    {category}   severity {X}/10
     chain                 functional → emotional → identity
     verbatim_quotes       "{verbatim 1}" · "{verbatim 2}" · ... ({count})
     triggered angles      {ANG-NN} · {ANG-NN}
   PNT-04  ...
```

**Section 3 · Objections (sub-folder OWNED)**

Liste OBJ-NN entries cette audience. Cap 10 (blocking ≥7 en premier, severity desc). Format ligne ·

```
Objections ({N})
   OBJ-01  {formulation}              {type}   severity-score {X}/10
     lifecycle             {stage-1} → {stage-2}
     response_counter      {pattern-1} · {pattern-2}
     verbatim_quotes       "{verbatim 1}" · "{verbatim 2}" · ... ({count})
     derived angles        {ANG-NN} ({short_reframe_note})
   OBJ-04  ...
```

**Section 4 · Cross-refs inbound (autres schemas pointent vers cette audience)**

Inverted index lookup depuis les 6 schemas suivants ·

```
Cross-refs inbound
   Angles dérivés          {ANG-NN} · {ANG-NN} · ... ({count} angles où angle.audience_slug = {slug})
   Briefs ciblant          {BRF-NN} · {BRF-NN} · ... ({count} briefs où brief.audience_slug = {slug})
   Créas ciblant           {CRT-NN} · {CRT-NN} · ... ({count} creatives où creative.audience_slug = {slug})
   Frictions impactant     {FRC-NN} (sub-product {product}) · ... ({count} frictions où friction.affects_audiences contient {slug})
   Test results            {TST-NN} · {TST-NN} · ... ({count} learnings où cross_refs.audience_slugs contient {slug})
   Roadmap priorisations   {phase-slug} · ... ({count} roadmap.relations.audience_slugs contient {slug})
```

Actions prioritaires ·
- `mine-voc sur {slug}` (audience hypothèse, <5 verbatims captés)
- `traite le pain bloquant {PNT-NN}` (top severity, audience-specific)
- `crée un angle reframe sur {OBJ-NN}` (objection bloquante sans angle dérivé)
- `valide l'audience {slug}` (hypothesis → tested transition)
- `merge low-signal sub-audiences sur {slug}` (si sous-poches < 5 verbatims)

Drill profondeur · `/phantom {brand} audiences {slug}/pain_points/{PNT-NN}` (fiche pain complète) · `/phantom {brand} audiences {slug}/objections/{OBJ-NN}` (fiche objection complète).

### `angles` · list + lineage signal

Per angle in `brands/{slug}/angles/` ·
- `angle_id`, `name`, `audience_target`, `status` (draft / live / fatigued / paused), `roas` if test_result exists, `lineage_objection` (depuis quelle objection dérive l'angle), `last_updated`.

**Tri** · live winners en premier, puis fatigués (à refresh), puis drafts, puis archivés.

End with paste-ready · refresh fatigued, validate draft, archive paused, créer angle depuis objection orpheline.

### `products` (alias `produits`) · liste compacte + scaling rules

Per product in `brands/{slug}/products/{slug}/spec.json` · sub-line canon ·

```
├─ {slug} {hero_badge} · {validation_status} · {N_offres} offres · {N_audiences} audiences · {N_angles} angles · {N_frictions} frictions · {N_pubs} pubs ({live}/{fatigued})
```

**Scaling rules respectées** (cf section dédiée). 1-3 produits = expanded ; 4-10 = compact 1 ligne ; 11+ = top-5 + drill obligatoire.

End with paste-ready · densify thinnest spec, snapshot a new product, audit produit hero, drill product complet {slug} 360°.

### `products {slug}` · entity-drill product 360° complet (v2.64)

`/phantom {brand} products {slug}` rend la fiche complète d'un produit. **Ontologie pure v2.64** · 10 schemas pertinents rendus 360° (spec OWNED + offers OWNED + funnel OWNED + visual_identity OWNED sidecar + frictions sub-folder OWNED + cross-refs inbound depuis 5 autres schemas).

Lecture · `brands/{brand}/products/{slug}/spec.json` + `offers.json` + `funnel.json` + `visual-identity/*.json` + `frictions/*.json` + inverted index cross-refs.

Header breadcrumb ·

```
workspace > {brand} > products > {slug}
══════════════════════════════════════════════
{product_name} · {hero_badge} · {validation_status}
{pricing_tier} · {N_offers} offers · {N_frictions} frictions · {N_angles} angles dérivés
```

Rendering · 10 sections obligatoires.

**Section 1 · Spec (OWNED)**

```
Spec
   identity              {product_name} · taxonomy · category
   composition           {N} ingredients · active_principle · {dosage}
   mécanismes ({N})      MEC-01 · MEC-02 · MEC-03 (top-3 names)
   bénéfices ({N})       chain functional/emotional/identity · BEN-01 · BEN-02 · ...
   market_context        sophistication market · competitive_landscape
   pricing               {tier} · MSRP · subscription_discount
   sustainability        certifications · supply_chain · packaging
   sensory_profile       taste · smell · texture
   problems_solved       {P-01 label} · {P-02 label}
   promise               headline benefit · proof points
   proofs                clinical_studies · testimonials · authority
   compliance            EFSA · FDA · regulatory tags
```

**Section 2 · Offers (OWNED)**

```
Offers ({N})
   offer_groups · {group_1}
     {OFF-01}   single             {price} · {savings} · active
     {OFF-02}   subscription       {price}/mo · {savings_pct}% · active
     {OFF-03}   bundle             {price} · {savings} · paused
   ...
```

**Section 3 · Funnel (OWNED)**

```
Funnel
   stages                awareness → consideration → decision → post-purchase
   economics             CAC {value} · LTV {value} · payback {N}d
   coverage              TOF/MOF/BOF {N}/{M}/{K}
   trous détectés        {gap_1} · {gap_2}
```

**Section 4 · Visual Identity (OWNED sidecar)**

```
Visual Identity
   packshots             {N} canonical · last_render {date}
   color_palette         {primary} · {secondary} · {accent}
   container             {shape} · {material} · {label_format}
   label                 typography · {key_visual_elements}
```

**Section 5 · Frictions usage (sub-folder OWNED)**

Liste FRC-NN entries ce produit. Cap 10 (top severity desc). Format ligne ·

```
Frictions usage ({N})       severity max {X}/10 · {N_bloquantes} bloquantes (≥7)
   FRC-01  emballage difficile à ouvrir       physical    severity 6/10
     customer_evidence     "{verbatim 1}" · "{verbatim 2}" · ... ({count})
     affects_audiences     stress-pro · post-partum (cross-refs)
     resolution_status     en cours · {action_taken}
   FRC-02  goût amer                          sensory     severity 5/10
     ...
```

**Section 6 · Cross-refs inbound (autres schemas pointent vers ce produit)**

Inverted index lookup depuis les 5 schemas suivants ·

```
Cross-refs inbound
   Angles dérivant         {ANG-NN} · {ANG-NN} · ... ({count} angles où angle.lineage.spec_activated reference {slug})
   Créas                   {CRT-NN} · {CRT-NN} · ... ({count} creatives où creative.product_slug = {slug})
   Briefs                  {BRF-NN} · {BRF-NN} · ... ({count} briefs où brief.product_slug = {slug})
   Roadmap                 {phase-slug} · ... ({count} roadmap.relations.product_slugs contient {slug})
   Learnings               {LRN-NN} · {LRN-NN} · ... ({count} learnings où cross_refs.product_slugs contient {slug})
```

Actions prioritaires ·
- `densify spec {slug}` (champs spec manquants si présents)
- `traite la friction bloquante {FRC-NN}` (top severity, sub-product)
- `map-mechanisms {brand}/{slug}` (enrichissement mécanismes 7 deep fields canon)
- `audit produit hero` (si hero_badge présent, densifier completeness)
- `craft-packshot {brand}/{slug}` (regénérer canonical packshot si stale)

### `services` (business_model: service)

Per service `brands/{slug}/services/{slug}/spec.json` (ou équivalent) ·

```
├─ {slug} · {validation_status} · {pricing_tier} · {N_outcomes} outcomes · {N_case_studies} case studies · {sales_cycle}j
```

End with paste-ready · case-study, brief méthodologie, scaling pricing.

### `offers` · table per product

Per offer file `brands/{slug}/products/{p}/offers.json`, render the `offer_groups[].offers[]` :
- `offer_id`, `name`, `type` (single / subscription / bundle / quantity_break / prepay), `price`, `savings_pct`, `active`.

End with paste-ready · connect Shopify if missing, mark inactive offers, etc.

### `strategy` · current focus + Q-target snapshot

Read `strategy.json`. Render :
- Annual goals (1-line each).
- Current quarter focus.
- Top 3 priorities.
- Last update timestamp.

End with paste-ready · update quarter focus, set new Q-target, rebalance focus.

### `learnings` · last 10 entries

Per entry in `learnings.json#entries[]` (newest first, capped at 10) :
- `id`, `kind` (test_result / workaround / compliance / observation / decision_trace), `fact` (truncated to 1 line), `promoted_to_canon` (yes/no), `created_at`.

End with paste-ready · capture-learning on a recent observation, promote a learning to brand-level rule, audit learnings sans promotion.

### `frictions` (NEW v2.57) · table frictions usage

Lecture · `brands/{slug}/frictions/*.json` (ou agrégat `frictions.json`).

Header breadcrumb ·

```
workspace > {brand} > frictions
══════════════════════════════════════════════
{N} frictions · severity max {X}/10 · {N_bloquantes} bloquantes (≥7) · {N_audiences_affected} audiences touchées
```

Rendering · table par category × severity.

```
Frictions critiques (severity ≥7)
  [FRC-08] · 9/10 · pricing-objection · audiences: chute-active, post-grossesse · {1-line fact}
  [FRC-05] · 8/10 · delivery-time · audiences: brand-wide · {1-line fact}

Frictions moyennes (severity 4-6)
  [FRC-04] · 6/10 · onboarding-friction · audiences: nouveaux-acheteurs · ...
  ...

Frictions mineures (severity 1-3)
  [FRC-02] · 2/10 · ...
```

Cap 10 plus saillantes (top severity desc). Cross-ref audiences via slug (drillable).

Actions prioritaires ·
- `traite la friction {FRC-NN}` (top severity bloquante)
- `cluster frictions par category` (si >15 frictions, suggérer regroupement)
- `capture-learning sur résolution {FRC-NN}` (si récemment traitée)

Drill item · `/phantom {brand} frictions {FRC-NN}`.

### `roadmap` (NEW v2.57) · phases sortées chronologique

Lecture · `brands/{slug}/roadmap.json` (ou `roadmap/phases.json`).

Header breadcrumb ·

```
workspace > {brand} > roadmap
══════════════════════════════════════════════
{current_phase_name} · {N} priorités · {due_date_top}
```

Rendering · phases chronologiques avec current highlighted.

```
Phase {N} · {phase_name} · {dates}                  ← EN COURS
  Priorité 1   {description}                        due {date} · {status}
  Priorité 2   {description}                        due {date} · {status}
  Priorité 3   ...
  → Angles refs · {ANG-XX, ANG-YY}
  → Audiences refs · {audience-slug-1, audience-slug-2}

Phase {N+1} · {phase_name} · {dates}                (à venir)
  ...

Phase {N-1} · {phase_name}                          (terminée)
  ✓ Priorité 1
  ✓ Priorité 2
```

Cap 3 phases (précédente + courante + suivante). Drill historique via `/phantom recent`.

Actions prioritaires ·
- `traite la priorité {P-NN}` (top current phase non-démarrée)
- `valide phase {N}` (si toutes priorités done)
- `réplane phase {N+1}` (si stale)

### `funnel` (NEW v2.57) · couverture TOF/MOF/BOF

Lecture · `brands/{slug}/funnel/coverage.json` (ou dérivé de Meta breakdown si connecté).

Header breadcrumb ·

```
workspace > {brand} > funnel
══════════════════════════════════════════════
TOF/MOF/BOF {N}/{M}/{K} · {winners} winners scalés · {fatigued} essoufflés
```

Rendering · table par stage × creative type.

```
TOF (top of funnel)             {N_total} pubs live
   ├─ Hook-driven               {n} ({live}/{fatigued}) · TOP ROAS: {value}
   ├─ Pain-driven               {n} ({live}/{fatigued})
   └─ Curiosity-driven          {n} ({live}/{fatigued})

MOF (middle of funnel)          {M_total} pubs live
   ├─ Mechanism explainer       {n} ({live}/{fatigued})
   ├─ Social proof              {n} ({live}/{fatigued})
   └─ Comparison                {n} ({live}/{fatigued})

BOF (bottom of funnel)          {K_total} pubs live
   ├─ Offer-driven              {n}
   ├─ Urgency / scarcity        {n}
   └─ Retargeting               {n}

Trous détectés
   · Aucun pain-driven sur audience {audience-slug}
   · MOF mechanism explainer absent depuis 30j
```

Actions prioritaires ·
- `comble le trou pain-driven sur {audience-slug}`
- `refresh MOF mechanism explainer`
- `scale top TOF winner {ad_id}`

### `briefs`, `tests`, `matrix` · délégués aux drills dédiés

`/phantom {brand} briefs` → mode briefs-drill (cf section dédiée).
`/phantom {brand} tests` → mode tests-drill (cf section dédiée).
`/phantom {brand} matrix` → mode matrix-drill (cf section dédiée).

Ces 3 drills sont harmonisés v2.57 sur le pattern enrichi (header breadcrumb + synthèse canon + items + cross-refs + actions + drill suivant).

### Hard rule for entity-drill

If `{entity}` is unsupported (not in the list above), surface · *"Entité '{x}' non reconnue. Disponibles · audiences, angles, products, services, offers, strategy, learnings, frictions, roadmap, briefs, tests, matrix, funnel. Pour drill pain_points/objections audience-specific · `/phantom {brand} audiences {slug}` (360°). Pour la vue brand complète · `/phantom {brand}`."*

### Filtrage par produit (entity-drill audiences)

Si l'opérateur tape `/phantom {brand} products {p_slug}` (item mode produit, voir plus bas), la fiche produit liste automatiquement les audiences dont `applies_to_products` contient `{p_slug}`. Pas de mode séparé `/phantom {brand} {product} audiences` (cap CLI à 3 niveaux). Le drill par produit se fait via item-mode produit.

---

## Mode item (niveau 3)

> **Split externe v2.36+** · full spec rendering → `.claude/commands/phantom-modes/item.md`. Lire ce fichier quand l'opérateur tape `/phantom {brand} {entity} {item}`. Si fichier absent, le créer avec la spec ci-dessous.

`/phantom {brand_slug} {entity} {item-slug}` zooms on ONE item inside an entity. Le rendering équivalent d'un *file preview* dans un Finder enrichi avec cross-refs résolus. Operator vient de drill quelque chose de spécifique · on déballe ce qu'on a, sans tout dump, mais avec **visibilité maximale sur les liens latéraux**.

### Pattern enrichi v2.57

1. **Header breadcrumb** · `workspace > {brand} > {entity} > {item}`
2. **Fiche item full** · tous fields canon du schema entity
3. **Cross-refs résolus** · liens lateraux dénormalisés inline ·
   - Audience drill → angles_derived[] + pubs_liées[] + frictions_affecting[] + objections enrichies avec angles_derived[]
   - Angle drill → audience_target + lineage_objection + tests_runs + briefs_sourced + ROAS history
   - Product drill → audiences applies_to + mechanisms[] + benefits[] chain + offers + pubs_liées
   - Friction drill → audiences_affected + severity + resolution_status + learnings_promoted
   - Brief drill → angle_source + audience_target + test_runs + winner_proxy
4. **Actions prioritaires** · 3-5 paste-ready dérivées du drill context item
5. **AskUserQuestion 4 slots** ·
   - Slot 1 · drill sibling (item voisin dans la même entity)
   - Slot 2 · action top-priority (paste-ready)
   - Slot 3 · drill cross-ref (e.g. depuis audience → angle dérivé)
   - Slot 4 · retour entity parent `/phantom {brand} {entity}` OU retour brand `/phantom {brand}`

### Entités drillables item v2.64

`audiences/{slug}` (360° expose profile + pain + objections + cross-refs natif), `audiences/{slug}/pain_points/{PNT-NN}` (sub-folder OWNED audience-specific), `audiences/{slug}/objections/{OBJ-NN}` (sub-folder OWNED audience-specific), `angles/{id}`, `products/{slug}` (360° expose spec + offers + funnel + frictions + cross-refs natif), `products/{slug}/frictions/{FRC-NN}` (sub-folder OWNED product-specific), `services/{slug}`, `briefs/{BRF-NN}`, `tests/{TST-NN}`, `roadmap/phases/{phase-slug}`. **REMOVED v2.64** · `pain-points/{PNT-NN}` + `objections/{OBJ-NN}` top-level (sub-folder OWNED audience-specific maintenant · accessible via audience-drill).

### Hard rule sur slug introuvable

Si `{item-slug}` n'existe pas dans `{entity}` du brand · *"Item '{slug}' introuvable dans {entity}. Items disponibles · {list_top_5}. Pour la liste complète · `/phantom {brand} {entity}`."* Pas d'AskUserQuestion.

---

## Mode search

`/phantom search {keyword}` cherche le mot-clé cross-brand sur tous les champs textuels indexables (slugs, names, descriptions, voc.key_expressions, pain_points, learnings.fact, strategy.goals).

Implémentation : invoquer `python3 .skills/phantom-search.py "{keyword}"` qui retourne un JSON array `[{path, type, brand_slug, slug, field, snippet}]`.

Header breadcrumb :

```
workspace > search "{keyword}"
══════════════════════════════════════════════
{N} matches · cross-brand
```

Rendering : un block par match (cap 20 affichés, mention si plus existent) :

```
{type} · {brand_slug}/{slug}
  {snippet avec keyword en gras ou highlight}
  Pour explorer · `/phantom {brand_slug} {entity} {slug}`
```

Group par `brand_slug`. Ordre par pertinence (matches sur `meta.name` en haut, matches sur descriptions/snippets en bas).

### AskUserQuestion (mode search)

| Slot | Rôle |
|---|---|
| 1 | Drill 1er match (paste-ready `/phantom {brand} {entity} {slug}`) |
| 2 | Drill 2e match |
| 3 | Drill 3e match |
| 4 | *"Retour workspace"* · relance `/phantom` |

Si 0 match : empty state pédagogique : *"Aucun résultat pour '{keyword}'. Essayer un autre terme avec `/phantom search`, ou consulter les actions en cours avec `/phantom todo`."* Pas d'AskUserQuestion dans ce cas.

---

## Mode recent

`/phantom recent` ou `/phantom recent {N}` (default N=10, max 50) liste les dernières mutations cross-brand en timeline lisible.

Implémentation : invoquer `python3 .skills/phantom-recent.py {N}` qui retourne un JSON array d'événements lus depuis `.phantom/context-engine-events.jsonl`.

Header breadcrumb :

```
workspace > recent
══════════════════════════════════════════════
Dernières {N} mutations · cross-brand
```

Rendering : un par ligne (compact) :

```
{time_ago}    {brand_slug}    {entity}    {action} {field_extrait}
                              → {reason si présent, sinon vide}
```

Exemple :
```
14h ago       glowco          audiences/chute-active     set meta.validation_status = "hypothesis"
                                                         → validated hierarchy
2d ago        vitatone        learnings                  append entry "test FB ad #3 ROAS 4.2"
6d ago        glowco          brand                      set positioning.tagline
```

### AskUserQuestion (mode recent)

| Slot | Rôle |
|---|---|
| 1 | Drill le brand le plus actif récent (paste-ready `/phantom {brand_slug}`) |
| 2 | Drill l'entity la plus modifiée (paste-ready `/phantom {brand_slug} {entity}`) |
| 3 | Drill un item du top match si pertinent |
| 4 | *"Retour workspace"* |

Si event log vide : *"Aucune mutation enregistrée pour l'instant. Revenir après la première session de mining ou de snapshot."*

---

## Mode todo

`/phantom todo` agrège les next-suggested top-priority de tous les brands actifs (skip dormants > 60j sauf `--all`). Vue cross-brand des actions à faire.

Header breadcrumb :

```
workspace > todo
══════════════════════════════════════════════
{N} actions actives · {M} brands
```

Rendering (top 5 max) :

```
{priority_icon} [{brand_slug}] {action description}
   · `{paste-ready commande}` ({why})
```

`priority_icon` (canon unifié v2.79.2) : `⚠` (critique : tests fatigués, brand stale > 30j sur entité critique), `◐` (à faire bientôt : audiences sans voix client, angles draft), `·` (peut attendre).

Exemple :
```
⚠ [vitatone] 2 angles ROAS en chute libre depuis 7j
   · `refresh les angles fatigués sur vitatone`

◐ [glowco] 7 audiences en hypothèse, aucune voix client encore
   · `lance la voix client sur glowco`

◐ [glowco] strategy.json sans focus Q2 posé
   · `pose le focus Q2 de glowco`

· [northsense] dormant depuis 47j, peut-être à archiver
   · `archive northsense`
```

### AskUserQuestion (mode todo)

| Slot | Rôle |
|---|---|
| 1 | Action ⚠ #1 (paste-ready) |
| 2 | Action ◐ #2 (paste-ready) |
| 3 | *"Drill {brand_slug}"* du brand qui concentre le plus d'actions |
| 4 | *"Retour workspace"* |

Si 0 todo (workspace serein) : *"Aucune action urgente en cours. Profiter du calme, ou démarrer un nouveau brand."*

---

## Mode help (?)

`/phantom ?` ou `/phantom help` rend une cheatsheet auto-générée. Court, dense.

Format :

```
PhantomOS · /phantom · vue d'ensemble des modes
══════════════════════════════════════════════
Navigation
  /phantom                            vue workspace (défaut)
  /phantom {brand}                    cockpit du brand
  /phantom {brand} {entity}           drill dense sur une entité
  /phantom {brand} {entity} {item}    preview d'un item

Utilitaires
  /phantom search "{keyword}"         recherche cross-brand
  /phantom recent [N]                 timeline des N dernières mutations (défaut 10)
  /phantom todo                       actions cross-brand priorisées
  /phantom ?                          cette vue

Référence métier (workspace-level)
  /phantom canon                      bibliothèque métier (copy, et autres à venir)
  /phantom canon copy                 11 couches de copywriting
  /phantom canon copy hooks           6 outils de hook
  /phantom canon copy hooks curiosity-gap   fiche détaillée

Entités drillables (v2.64)
  audiences, angles, products, services, offers, strategy, learnings, frictions (sub-product), roadmap, briefs, tests, matrix, funnel
  audience 360°    /phantom {brand} audiences {slug}   (profile + pain + objections + cross-refs)
  product 360°     /phantom {brand} products {slug}    (spec + offers + funnel + frictions + cross-refs)

Navigation rapide
  Chaque rendering termine par 4 boutons cliquables (drill, drill latéral, action, retour parent).
  Le slot 4 ramène toujours au niveau parent, aucun cul-de-sac.

Exemples concrets
  /phantom glowco audiences chute-active
  /phantom search "post-grossesse"
  /phantom recent 20
  /phantom canon copy frameworks pas

Routing fonctions
  Recherche par intention · consulter `.skills/INDEX.md` (fonctions par objectif)
  Recherche par état · rester dans /phantom
```

Pas d'AskUserQuestion en mode help. C'est une référence, pas un point d'action.

---

## Mode canon (atlas du métier, workspace-level)

> **Split externe v2.36** : full spec → `.claude/commands/phantom-modes/canon.md`. Lire ce fichier quand l'opérateur tape `/phantom canon[...]`. 4 sous-modes (`canon`, `canon {atlas}`, `canon {atlas} {layer}`, `canon {atlas} {layer} {tool}`), impl `python3 .skills/phantom-canon.py [atlas] [layer] [tool]`, AskUserQuestion 4 slots (drill voisin / drill couche / applique au brand / retour parent).

---

## Mode briefs-drill

`/phantom {brand} briefs` rend la DB Briefs créatifs (briefs produits via `produce-copy-brief`). Workspace tabular, parité Notion Stride-Up.

Lecture : `brands/{brand}/briefs/*.json` (ou agrégat `brands/{brand}/briefs.json`).

Header breadcrumb :

```
workspace > {brand} > briefs
══════════════════════════════════════════════
{N} briefs · {N_draft} draft · {N_shipped} shipped · {N_validated} validés

Briefs récents
  [BRF-03] · 2026-05-06 · ANG-01 · post-grossesse · draft
  [BRF-02] · 2026-05-04 · ANG-02 · stress hormonal · shipped
  [BRF-01] · 2026-04-28 · ANG-04 · croissance-projet · validé
  ...

Actions prioritaires
  · `produce-copy-brief sur {brand} ANG-XX` (générer brief sur angle non-couvert)
  · `audit briefs > 30j sans test` (briefs stale à promouvoir ou archiver)
```

Format ligne : `[brief_id] · {created_at} · {angle_id_source} · {audience_slug} · {status}`. Cap 10 plus récents. Cross-ref atlas via lien `angle_id_source` (drillable).

---

## Mode tests-drill

`/phantom {brand} tests` rend la DB Tests live + résultats observés + verdict `winner_proxy`.

Lecture : `brands/{brand}/learnings.json#entries[]` filtré sur `kind: test_result`.

Header breadcrumb :

```
workspace > {brand} > tests
══════════════════════════════════════════════
{N} tests · {N_live} live · {N_fatigued} fatigués · {N_winners} gagnants

Tests récents
  [TST-08] · live · BRF-03 · ANG-01 · ROAS 3.2 · spend 412€ · gagnant : en attente
  [TST-07] · fatigué · BRF-02 · ANG-02 · ROAS 1.4 (-38% 14j) · gagnant : non
  [TST-06] · gagnant · BRF-01 · ANG-04 · ROAS 4.7 · scalé · gagnant : oui
  ...

Actions prioritaires
  · `refresh les angles fatigués sur {brand}` ({N} tests en chute)
  · `promote winner TST-06 → angle scaled` (test confirmé, à intégrer au canon brand)
```

Format ligne : `[test_id] · {status} · {brief_id} · {angle_id} · ROAS {value} · {spend} · winner_proxy: {yes|no|pending}`. Cap 10 plus récents.

---

## Mode matrix-drill

`/phantom {brand} matrix` rend la priorisation des territoires (sous-groupes × source d'angle + top territoires + trous).

Lecture (backend, paths agent) : `brands/{brand}/matrix/latest.json` (output `weight-dimensions` + `score-matrix`).

Header breadcrumb :

```
workspace > {brand} > priorisation
══════════════════════════════════════════════
Facteurs d'ajustement : stade {growth} · marché {mature} · historique {partiel}
Coefficient cumulé : {1.1}

┌───────────────────────────┬──────┬──────┬──────┬──────┬──────┐
│ Sous-groupe audience      │ aud  │ prod │ cat  │ brand│ temp │
├───────────────────────────┼──────┼──────┼──────┼──────┼──────┤
│ chute-post-grossesse      │ 55 ★ │ 42   │ 38   │ 0    │ 28   │
│ croissance-projet         │ 48   │ 52 ★ │ 0    │ 35   │ 0    │
│ stress-hormonal           │ 32   │ 28   │ 41 ★ │ 0    │ 22   │
└───────────────────────────┴──────┴──────┴──────┴──────┴──────┘

Top 3 territoires
  1. chute-post-grossesse × angle audience       · 55  · ANG-01, ANG-03
  2. croissance-projet × angle produit           · 52  · ANG-04
  3. stress-hormonal × angle catégorie           · 41  · ANG-02

Trous détectés
  · angle brand sur chute-post-grossesse (0)
  · angle catégorie sur croissance-projet (0)
  · angle moment sur croissance-projet (0)

Actions prioritaires
  · `génère un brief copy sur le top-1` (chute-post-grossesse × angle audience, score 55)
  · `crée des angles publicitaires {brand} pour combler le trou angle brand sur chute-post-grossesse`
```

Icône `★` sur la cellule top par row. Légende colonnes (sources d'angle) : aud (depuis l'audience), prod (depuis le produit), cat (depuis la catégorie), brand (depuis la brand), temp (depuis un moment / saison).

---

## Mode atlas-overview

`/phantom {brand} atlas` rend la vue d'ensemble brand (synthèse 6 entités core + 3 dérivées + historique brand). Pédagogique pour onboarding nouveau opérateur.

Lecture (backend, paths agent) : `brands/{brand}/_snapshot.md` + `brand.json` + counts par entité.

Header breadcrumb :

```
workspace > {brand} > atlas
══════════════════════════════════════════════
Matière brand {brand_name} · vue d'ensemble

Matière brand (6)
  brand           ✓ identité posée · territoire créatif défini · niveau de notoriété {faible|moyen|fort}
  produits ({N}) {product_slug_1} · {product_slug_2}
  audiences ({N}) {audience_slug_1} · {audience_slug_2} · ... · {audience_slug_N}
  offres          {N} offres configurées
  apprentissages  {N} entrées · {N_canon} promues en référence
  stratégie       focus {month_year} : {strategy.current_focus}

Productions dérivées (3)
  angles produits          {N}
  visuels produits         {N}
  priorisation territoires · dernière exécution : {date}

Historique brand (ce qui a marché)
  Accroches validées        {N}
  Structures testées        {N}
  Styles validés            {N}
  Angles validés            {N}
  Formats validés           {N}

Actions prioritaires
  · `/phantom {brand} matrix` (priorisation des territoires)
  · `/phantom doctrine` (méthode du système)
```

Cross-ref backend (instructions agent) : `docs/system/atlas-brand.md`. Slug brand en majuscules dans header. Ne pas exposer ce path à l'opérateur.

### Mode atlas-overview · empty state (brand fresh)

Si `brands/{brand}/_snapshot.md` indique tout à 0 (pas d'audiences cartographiées, pas de produits, pas d'angles), le mode atlas bascule sur empty state distinct au lieu de la vue 0/0/0/0 décourageante.

Format empty state :

```
workspace > {brand}
══════════════════════════════════════════════
Démarrage de {brand_name}.

Par où commencer ?

  (a) Importer la matière existante (URL produit, brief PDF, deck founder)
  (b) Mining audience initial (clients ciblés, verbatims captés)
  (c) Cartographier l'offre (produits, mécanismes, bénéfices)
  (d) Adapter selon ton point de départ
```

Pas de "MATIÈRE ACTUELLE 0/0/0/0/0". Pas de "SIGNAL FORT" inventé. Posture propose action concrète.

**Trigger detection** : `audiences count = 0 AND products count = 0 AND angles count = 0` → empty state. Sinon vue normale (même si brand partial · audiences ok mais 0 angles reste vue normale degraded).

---

## Mode doctrine

`/phantom doctrine` rend la méthode du système (cartographie + composition). Equivalent Notion "Méthode & Doctrine". Vue pédago, workspace-level (transversal aux brands).

Lecture (backend, paths agent) : `docs/system/atlas-brand.md` + `resources/templates/creative-formula.md`.

Header breadcrumb :

```
workspace > doctrine
══════════════════════════════════════════════
Méthode du système · cartographier + composer

Vue d'ensemble · arbres de connaissance + priorisation + facteurs d'ajustement + boucle d'apprentissage

Parcours en 6 étapes
  Étape 1 démarrage          démarrer une nouvelle brand · cartographie initiale · poser les specs
  Étape 2 produit            mécanismes · bénéfices · problèmes résolus
  Étape 3a audience          récupérer les témoignages clients · cartographie audience (8 dimensions)
  Étape 3b angle             créer des angles publicitaires (Observation + Tension + Reframe + Bridge)
  Étape 4 priorisation       calculer les priorités d'audience · prioriser les territoires
  Étape 5 brief              générer un brief copy
  Étape 6 visuel             créer un visuel · adapter un visuel existant · décomposer une pub existante

Recette créative
  créa = NOYAU (mécanique × format × stop scroll × ton)
       × CONTEXTE (angle × douleur × persona × preuve)
       × MODIFICATEURS (occasion · offre · destination · etc.)

7 piliers du système
  Le système repose sur 7 piliers internes (encodage rigoureux, production qualité,
  création de skills, traçabilité, cartographie compositionnelle, gouvernance, intelligence contextuelle).
  L'opérateur en perçoit les effets, sans avoir à les nommer.

Boucle d'apprentissage (historique brand vivant)
  produire → tester → capturer ce qu'on a appris → tests passés cumulés sur la bibliothèque

Actions prioritaires
  · `/phantom canon` (bibliothèque métier · 11 chapitres copy)
  · `/phantom {brand} atlas` (vue brand-side de la méthode appliquée)
```

Détails complets (backend) : `resources/templates/creative-formula.md`. Source méthode (backend) : `docs/system/atlas-brand.md`.

---

## Mode doctrine audiences

> **Split externe** : full spec rendering du framework cartographie audiences (4 questions Q1-Q4 + pièges + Pareto) → `.claude/commands/phantom-modes/doctrine-audiences.md`. Lire ce fichier quand l'opérateur tape `/phantom doctrine audiences`.

Bref : framework pédagogique 4 questions (porte d'entrée, granularité, Schwartz, chevauchements). Operator-facing, workspace-level. Cross-ref · `docs/doctrine/audience-cartography-framework.md`.

---

## Mode audiences-tree

> **Split externe** : full spec rendering de l'arbre audiences brand-side (hiérarchie + chevauchements + gaps détectés + dégradation gracieuse) → `.claude/commands/phantom-modes/audiences-tree.md`. Lire ce fichier quand l'opérateur tape `/phantom {brand} audiences`.

Bref : iterate `brands/{brand}/audiences/*/profile.json`, extract `meta.scope` + `meta.parent_slug` + `meta.overlap_with`, render arbre indenté par porte d'entrée + ligne chevauchements + bloc gaps. Override le mode entity-drill générique pour l'entité `audiences`. Le drill per-audience reste mode item via `/phantom {brand} audiences {slug}`.

---

## Mode mechanisms-drill

`/phantom {brand} products {p_slug} mechanisms` rend l'array `mechanisms[]` typé depuis `spec.json`.

Lecture : `brands/{brand}/products/{p_slug}/spec.json#mechanisms[]`.

Header breadcrumb :

```
workspace > {brand} > products > {p_slug} > mechanisms
══════════════════════════════════════════════
{N} mécanismes typés

MEC-01 modulation cortisol stress
  cible           SN central, surrenales
  mode action     adaptogène
  fenêtre         21-30j
  preuve          clinique citée
  sophistication  faible
  triggered_by    KSM-66

MEC-02 ...

Actions prioritaires
  · `map-mechanisms {brand}/{p_slug}` (enrichissement profond des mécanismes)
  · `densifie spec {p_slug}` (champs manquants si présents)
```

Format par mécanisme : id + nom court, puis 6 champs (cible, mode action, fenêtre, preuve, sophistication, triggered_by). Si `mechanisms[]` vide : empty state *"Aucun mécanisme encodé. Lancer `map-mechanisms {brand}/{p_slug}` pour scaffold depuis la fiche produit."*

---

## Mode benefits-drill

`/phantom {brand} products {p_slug} benefits` rend l'array `benefits[]` (chain functional → emotional → identity).

Lecture : `brands/{brand}/products/{p_slug}/spec.json#benefits[]`.

Header breadcrumb :

```
workspace > {brand} > products > {p_slug} > benefits
══════════════════════════════════════════════
{N} bénéfices encodés (chain functional/emotional/identity)

BEN-01 cheveux denses visibles
  layer         functional
  trigger       MEC-01
  fenêtre       60-90j
  preuve        photo before/after
  audience_fit  chute-active, chute-post-grossesse

BEN-02 confiance retrouvée
  layer         emotional
  trigger       BEN-01
  ...

BEN-03 identité jeune mère épanouie
  layer         identity
  trigger       BEN-02
  ...

Actions prioritaires
  · `map-benefits {brand}/{p_slug}` (enrichissement profond de la chaîne)
  · `audit benefits sans audience_fit` (benefits orphelins)
```

Format par benefit : id + nom court, puis 5 champs (layer, trigger, fenêtre, preuve, audience_fit). Layer = `functional|emotional|identity`. Si `benefits[]` vide : empty state similaire à mechanisms.

---

## Empty states pédagogiques

Quand un rendering rencontre du vide, ne rends pas du vide · propose le next move concret. Toujours.

| Situation | Empty state output |
|---|---|
| Workspace mode, 0 brand | (déjà couvert par mode bootstrap) |
| Brand mode, 0 produit | *"Aucun produit encodé sur `{brand}`. Pour scaffold le hero produit · `snapshot {brand} avec {url}`."* |
| Brand mode, 0 audience | *"Aucune audience sur `{brand}`. Le snapshot propose une cartographie. Sinon · `lance mine-voc sur {brand}` pour partir du verbatim client."* |
| Entity-drill audiences, 0 audience | *"Aucune audience encodée. Passer par `/phantom {brand}` puis snapshot le hero pour scaffold les groupes principaux."* |
| Entity-drill angles, 0 angle | *"Aucun angle produit. Après récupération des témoignages · `crée des angles publicitaires {brand}` pour générer un set priorisé."* |
| Entity-drill learnings, 0 entry | *"Aucun learning capturé. Après une correction · `/learn-from-session` pour verrouiller la première règle."* |
| Entity-drill products, 0 produit | (idem brand mode 0 produit) |
| Entity-drill offers, 0 offer | *"Aucune offre. Le snapshot du hero produit scaffold les offres depuis l'API ou demande au pixel."* |
| Entity-drill strategy, 0 strategy | *"Stratégie non posée. Pour cadrer le focus · `pose le focus Q{n} sur {brand}`."* |
| Item mode, slug introuvable | (déjà couvert par hard rule item mode) |
| Search 0 match | (déjà couvert par mode search) |
| Recent log vide | (déjà couvert par mode recent) |
| Todo vide | (déjà couvert par mode todo) |

Hard rule : **toujours offrir un next move dans l'empty state**. Jamais juste *"rien à afficher"*.

---

## Status indicators enrichis

Étend la table d'icônes existante (mode brand, mode entity-drill, mode workspace) avec :

| Icône | Sens (canon unifié v2.79.2) |
|---|---|
| `✓` | encodé, complet, frais (< 7j) |
| `◐` | encodé partiel (gaps OR stale 7-14j OR completeness < 70%) OU tâche de fond en cours |
| `○` | absent / vide / pas encore encodé / non connecté (sources) |
| `✗` | absent ET bloquant pour le flow brand |
| `⚠` | critique (stale > 90j OU tests en chute libre OU décision bloquante) |
| `★` | top cellule par row (matrice priorisation uniquement) |

Application · utiliser `⚠` quand un test ROAS chute ≥30% sur 14j ou quand un brand a > 90j sans activité. `◐` quand `_mining_status: "running"` détecté ou une tâche de fond sub-agent en cours. Pas d'icône "créé < 24h" (signal dérivable depuis Section ALERTES si pertinent · pas iconographié).

**Hard rule iconographie v2.79.2.** Système unique strict · `✓ ◐ ○ ✗ ⚠ ★`. JAMAIS d'emoji couleur (cercles colorés, flammes, éclairs, sabliers, badges NEW). JAMAIS d'emoji décoratif. Légende affichée au pied de chaque output `/phantom {brand}`.

---

## Footer hint discoverability

À la fin de chaque rendering (workspace, brand, entity-drill, item, search, recent, todo), juste avant l'AskUserQuestion, insérer une ligne subtle :

```
─────
`/phantom ?` pour les modes disponibles · `/phantom search` pour rechercher
```

**Cap discoverability sans bruit.** Si l'opérateur a déjà tapé `/phantom ?` dans la session courante (track ephemeral), skip cette ligne. Sinon : présente, faible opacité visuelle.

---

## Post-render jargon filter (v2.42+)

**Scope** : tous les modes `/phantom` operator-facing (workspace, brand, entity-drill, item, search, recent, todo, atlas-overview, briefs-drill, tests-drill, matrix-drill, mechanisms-drill, benefits-drill, doctrine, doctrine-audiences, audiences-tree, canon-*). Coverage v2.42 phantom-modes only ; SKILL.md `output_format` : pass futur.

**Contrat avant émission** : (1) charger `.skills/_jargon_bank.json` (généré par `build-manifest.py` depuis `docs/system/operator-vocabulary-translation.md`, schema `jargon-bank/1.0`, 60+ entries). (2) Pour chaque entry `context: phantom-modes`, scanner le rendu, match case-insensitive longest-first sur les variants `internal[]`. (3) Substituer par `operator_fr` (default) ou `operator_en` (si `operator/profile.json#preferences.language` = en). (4) **Préserver** code fenced ```, inline `backticks`, markdown, JSON paths comme tech detail. (5) Token jargon résiduel hors backticks détecté → log warning + substitution forcée.

**Invocation** : `python3 .skills/apply-jargon-filter.py --locale fr` (stdin/stdout), ou import `from apply_jargon_filter import apply_jargon_filter`. Si infra non invoquée, agent applique la substitution mentalement post-render.

---

## Constraints (tous modes)

- **Read-only.** Aucun changement persistant. Si l'opérateur demande ensuite de fix quelque chose, propose le skill approprié, ne fais pas le changement toi-même.
- **One screen output.** Workspace mode · 30 lignes max. **Brand mode · 60-90 lignes max v2.79.2+ (page sobre structurée 4 sections obligatoires · ALERTES ≤ 12 lignes · ÉTAT ≤ 15 lignes · ACTIONS ≤ 8 lignes · Drill footer ≤ 6 lignes, cf section *Mode brand*).** **Entity-drill mode · 60-70 lignes max (drill enrichi cross-refs + actions, cf section *Pattern enrichi*).** Item mode · 40-60 lignes max selon entity.
- **Density modérée v2.79.2.** Séparateurs ━━━ entre sections (pas ────). Whitespace généreux. Une chose par ligne · jamais 3 métriques empilées. Iconographie unifiée `✓ ◐ ○ ✗ ⚠` · zéro emoji couleur. Pédagogie matricielle 4 niveaux (NIVEAU 1-4) déléguée à `/breakdown` + `/bird` + skills consumers · pas dans `/phantom` (scan rapide santé brand, pas reverse engineering pédagogique).
- **Pas de jargon doctrine.** Filtre `_jargon_bank.json` post-render v2.42+ (cf section *Post-render jargon filter*). Traduit en mots métier (validé / hypothèse / fatigué / fiche incomplète / voix client manquante / tâche de fond).
- **Honest staleness.** Si une entité n'a pas été touchée depuis 90j, dis-le. Si snapshot date > 1h, regenère silencieusement avant d'afficher.
- **Workspace est le default.** `/phantom` sans argument lande toujours au niveau workspace (sauf bootstrap si 0 brand). L'opérateur drille explicitement via `/phantom {slug}`. Pattern terminal-like, jamais court-circuiter la navigation.
- **Drill par étape, pas en bloc.** `/phantom {slug}` montre le brand. `/phantom {slug} {entity}` zoome sur une entité. Évite de tout dump en une fois ; économie de contexte ET de lisibilité.
- **Actions verbalisées.** Section ACTIONS (top 3 numérotées) en langue naturelle opérateur · jamais skill name exposé · pas de backtick + texte naturel mixés. Le skill route backstage si l'opérateur valide. Anti-pattern · *"`refresh-angles {brand}`"* ou *"Lancer mine-voc dès que possible"*.
- **Navigation cliquable systématique.** Chaque rendering `/phantom` (workspace, brand, entity-drill) se conclut PAR un AskUserQuestion natif qui propose la navigation suivante. Voir section *Navigation interactive* ci-dessous.

---

## Navigation interactive (AskUserQuestion)

Le terminal n'a pas de flèches haut/bas pour naviguer. AskUserQuestion compense : à chaque niveau, l'opérateur reçoit 4 options cliquables qui structurent la navigation comme dans un dossier imbriqué (drill plus profond, drill latéral, agir, remonter). Le rendering textuel reste · l'AskUserQuestion s'AJOUTE à la fin pour accélérer la navigation, jamais ne la remplace.

### Contrat universel des 4 options

Indépendamment du mode, le AskUserQuestion respecte la grammaire suivante :

| Slot | Rôle | Source de l'option |
|---|---|---|
| 1 | **Drill vertical** : aller plus profond dans la hiérarchie courante | mode-spécifique (voir tableaux ci-dessous) |
| 2 | **Drill vertical alternatif OU drill latéral** : autre branche au même niveau | mode-spécifique |
| 3 | **Action top-priority** : la 1re ligne de NEXT SUGGESTED (paste-ready, déclenche la commande au clic) | dérivée du même calcul que NEXT SUGGESTED |
| 4 | **Remonter d'un niveau OU exit** : navigation vers le parent | toujours présent, jamais omis |

**Hard rule.** Le slot 4 est toujours un retour vers le niveau parent (ou exit en workspace mode). L'opérateur sait qu'il peut toujours remonter en 1 click, même s'il s'est égaré.

### Workspace mode · slots concrets

| Slot | Question rendue (FR) |
|---|---|
| 1 | *"Explorer {brand_le_plus_actif}"* (brand avec last_session le plus récent) |
| 2 | *"Explorer {brand_en_alerte}"* (brand avec tests fatigués OU stale > 30j OU mining vide), ou si aucun : *"Explorer {2e brand le plus actif}"* |
| 3 | Actions prioritaires top-priority cross-brand (paste-ready commande) |
| 4 | *"Voir un autre brand / continuer"* (free-text fallback, possibilité de taper `/phantom {autre_slug}`) |

**Cas N=1 brand** : slots 1 + 3 + 4 only (3 options visibles). Slot 2 omis car redondant.

### Brand mode · slots concrets

| Slot | Question rendue (FR) |
|---|---|
| 1 | *"Explorer audiences"* (entity-drill audiences) |
| 2 | *"Explorer {entity_la_plus_chargée}"* · celle avec le plus d'instances ou l'état le plus actif (typiquement `angles` ou `learnings`) |
| 3 | Action prioritaire sur ce brand (paste-ready commande) |
| 4 | *"Retour workspace"* (déclenche `/phantom`) |

### Entity-drill mode · slots concrets

| Slot | Question rendue (FR) |
|---|---|
| 1 | Action prioritaire spécifique à l'entité (paste-ready commande) |
| 2 | Action 2e-priority sur la même entité (paste-ready commande) |
| 3 | *"Explorer {entity_voisine}"* (autre entity-drill du même brand, choisie par pertinence : depuis audiences → angles, depuis angles → audiences, depuis products → offers, depuis learnings → strategy) |
| 4 | *"Retour {brand_slug}"* (déclenche `/phantom {brand_slug}`) |

### Saturation pattern

Si la session courante a déjà déclenché 3 AskUserQuestion `/phantom` dans les 5 dernières minutes, le 4e rendu désactive le AskUserQuestion (rendering text-only). L'opérateur est en mode exploration profonde et le pattern interactif devient du bruit. Re-active après 5 min sans `/phantom` ou après un autre type de skill exécuté.

### Formulation de l'AskUserQuestion

Présenter les 4 slots dans cet ordre fixe (drill primaire, drill secondaire, action, retour). Phrasing court, jamais explicatif. Exemple sur brand mode glowco :

```
question : "Prochaine étape ?"
options :
- "Explorer audiences (7 audiences à valider)"
- "Explorer angles (5 hypothèses)"
- "Lancer mine-voc sur glowco"
- "Retour workspace"
```

L'opérateur clique. L'agent exécute :
- Slots 1, 2 → relance `/phantom {slug} {entity}` ou `/phantom`
- Slot 3 → exécute la commande paste-ready (snapshot, mine-voc, audit, etc.)
- Slot 4 → relance `/phantom` (workspace) ou `/phantom {slug}` (brand) selon le niveau parent.

### Anti-patterns

- **5 options ou plus.** Cap dur à 4. Si plus de candidats existent, dégrader vers free-text fallback (slot 4).
- **Slot 4 absent.** L'opérateur doit toujours pouvoir remonter en 1 click. Jamais de cul-de-sac.
- **Action non-paste-ready dans slot 3.** Le slot action déclenche une commande exécutable, pas un conseil. *"Pense à mine-voc"* est un anti-pattern.
- **AskUserQuestion sans rendering text.** Le rendering reste TOUJOURS, l'AskUserQuestion vient APRÈS. Le rendering porte l'information, l'AskUserQuestion accélère la navigation.
