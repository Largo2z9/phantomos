---
name: cartograph
type: producer
version: "1.0.0"
recommended_model: sonnet
layer: territoire
reasoning_pattern: matrix-driven
matrix_mode: generating
consumes:
  - path: brands/{slug}/_snapshot.md
    min_version: 1.0.0
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
  - path: brands/{slug}/products/*/spec.json
    min_version: 1.0.0
  - path: brands/{slug}/products/*/offers.json
    min_version: 1.0.0
  - path: brands/{slug}/audiences/*/profile.json
    min_version: 1.0.0
  - path: brands/{slug}/strategy.json
    min_version: 1.0.0
  - path: brands/{slug}/learnings.json
    min_version: 1.0.0
  - path: brands/{slug}/status.json
    min_version: 1.0.0
description: >
  Knowledge cartography. Mode --learn pour cartographier un domaine
  (concepts core, leviers, débats, vocabulaire) ou une brand encodée
  (synthèse stratégique READ-ONLY cross-entités). Matérialise le verbe
  canonique métier (cartographier → conceptualiser → modéliser) en
  exécution exposée. Mode BUILD délégué à build-agent Step 2b silencieux.
  FR: "cartographier {sujet}", "carte stratégique {brand}", "explique-moi {domaine}", "comprends-moi {sujet}", "je connais mal {brand}", "synthèse {brand}".
  EN: "map {topic}", "strategic map {brand}", "explain {domain} to me", "I don't know {brand} well", "synthesize {brand}".
permissions:
  reads: [brand, product, profile, offer, learning, strategy]
  writes: []
  mode: none
  subagent_safe: true
disambiguates_against:
  snapshot-brand: snapshot-brand pour extraction factuelle scrape ; cartograph pour synthèse READ-ONLY de l'encodé.
  query-context: query-context pour lecture data brute ciblée ; cartograph pour raisonnement cross-entités synthétique.
  brief-day: brief-day pour todos jour + état brand ; cartograph pour synthèse stratégique macro.
  build-agent: build-agent fait carto BUILD silencieuse Step 2b interne ; cartograph fait LEARN exposé autonome.
  study-niche-marketdeepdive: study-niche pour deep-dive marché WRITE 30-60 min ; cartograph pour READ-ONLY synthèse rapide.
  deepen-brand-context: deepen-brand-context pour enrichir context via mine-voc + mine-vom (WRITE) ; cartograph pour synthèse READ-ONLY de l'existant.
pipeline:
  preconditions: |
    Mode --learn brand=<slug>: snapshot fait + status.json#wedge_complete = true.
    Mode --learn <domaine>: aucun pré-requis brand.
  postconditions: synthèse output operator-friendly avec 3 décisions actionnables. Aucune mutation. Aucun event.
---

# Cartograph · Knowledge Cartography

## Posture

Outil de raisonnement, pas d'extraction. Lit ce qui est encodé OU mappe un domaine pédagogiquement. Sortie = synthèse opérateur-friendly courte, pas dump structuré. Matérialise le verbe canonique du pipeline métier (cartographier → conceptualiser → modéliser → processiser → systémiser).

Outil pour comprendre avant d'agir. L'opérateur sort avec une carte mentale claire et 3 décisions à prendre, pas avec un mur de texte.

## Modes

| Mode | Trigger | Pré-requis | Output canonique |
|---|---|---|---|
| `cartograph --learn <domaine>` | "explique-moi X", "carte de Y", "comprends-moi Z" | Aucun | Carte pédagogique : définition, leviers, pièges, débats, vocabulaire, 3 décisions actionnables |
| `cartograph --learn brand=<slug>` | "carte stratégique brand X", "je connais mal cette brand" | brand discovery complete | Synthèse READ-ONLY : posé, gaps, attention, 3 décisions actionnables |
| `cartograph --learn brand=<slug> --incomplete` | "carte partielle brand X", "carte de ce qui est encodé" | Aucun (brand existe) | Synthèse partielle READ-ONLY : ce qui est encodé maintenant + warning explicite "discovery incomplet" + 3 décisions priorisant la complétion |

## Hard Rules

### HR1 · Pré-requis dur sur mode brand
**YOU MUST** vérifier `brands/{slug}/status.json#wedge_complete = true` avant exécution mode brand. Si false → refuse + propose `snapshot-brand {slug}` ou `setup-brand` selon état. **NEVER** produire une carte stratégique sur une brand non-encodée. Hallucination garantie sinon.

### HR2 · Sourçage strict tag par insight (mode brand)
Chaque ligne de carte porte un tag inline : `[observé · path]`, `[déclaré · path]`, `[déduit · path]`, `[gap · path vide]`, `[incertain]`. Pas de mélange. Tag observé/déclaré = lecture directe d'un champ. Tag déduit = inférence depuis ≥2 sources observées. Tag gap = absence encodée explicite. **NEVER** d'assertion sans tag dans une carte brand.

### HR3 · Zéro jargon plumbing exposé
**NEVER** exposer dans output les mots `convention`, `framework`, `SOP`, `quality-spec`, `catalogue`, `entity`, `field`, `schema`, `sidecar`, `extension`. Traduire en langage opérateur. Acronymes domaine (AOV, CAC, LTV, RFM) acceptés s'ils sont expliqués une fois en bas de section ou s'ils sont dans `operator/awareness.json#concepts_introduced`.

### HR4 · Zéro chiffre, take ou positionnement inventé
**NEVER** sortir un chiffre, AOV, ROAS, ratio, % sans tag observé pointant le path. **NEVER** inventer un positionnement, une niche, une phase d'acquisition, un AOV de référence. Si la donnée n'est pas encodée → tag `[gap]` explicite. Mode `--learn <domaine>` exempt de tags (pas de brand à sourcer), mais utiliser "règle terrain courante" plutôt que chiffre faux-précis.

### HR5 · Output = synthèse, pas dump
Sections courtes, phrases directes, pas de prose dense. Toujours terminer sur **3 décisions actionnables exactement** (jamais plus, jamais moins). Décisions = action sur substrate encodé (encoder X), choix opérateur (décider Y vs Z), ou geste sourcé du gap (mesurer Z). **NEVER** conseils business inventés.

### HR6 · Zéro mutation
`writes: []`. **NEVER** appeler `write_to_context`. Mode READ-ONLY strict. Si l'opérateur demande "applique cette reco" → refuse + redirect vers `capture-learning` (single fact) ou skill mutateur dédié.

### HR7 · Limite scope
Maximum 5-7 sections par carte. **NEVER** carte de 30 axes plats. Si sujet trop vaste → propose split en sous-cartos (`cartograph --learn audiences-segmentation` plutôt que `cartograph --learn marketing`).

## Protocole d'exécution

### Phase 1 · Détection mode + parse arguments
- Args contient `brand=<slug>` ou un slug de brand mentionné dans contexte → mode brand.
- Args contient un sujet/concept sans slug brand → mode domaine.
- Ambigu → 1 AskUserQuestion : 2 options (mode brand / mode domaine). Pas plus.

### Phase 2 · Pré-requis check (mode brand uniquement)
1. Lire `brands/{slug}/status.json`.
2. Vérifier `wedge_complete = true`. Si false :
   ```
   Snapshot pas fait sur {slug}. Lance `snapshot-brand {slug}` d'abord,
   puis je produirai la carte stratégique sourcée. Sans data, je ne devine
   pas, je hallucine.
   ```
   STOP. Ne pas exécuter Phase 3.
3. Lire `brands/{slug}/_snapshot.md` (digest 1-2KB) en premier.
4. Drill ciblé sur les fichiers JSON nécessaires selon focus de la carte (Phase 3 questions guidées).

### Phase 3 · Questions guidées (3 max via AskUserQuestion)

**Mode domaine** :
1. Niveau actuel sur le sujet : zéro / surface / partiel / avancé.
2. Objectif : apprendre / décider / construire / pitcher.
3. Profondeur : panorama / drill un angle / exhaustif (Recommended : panorama par défaut, no over-engineer).

**Mode brand** :
1. Focus de la carte : overview global / audiences / offre commerciale / stratégie + objectifs.
2. Niveau opérateur sur la brand : nouveau (premier contact) / déjà bossé (refresh).
3. (Conditionnelle) Question contextuelle libre selon brand state (ex: "le snapshot date de 30j, on rafraîchit avant ?").

**Si l'opérateur répond "skip" ou "panorama"** → exécuter avec defaults raisonnables. Pas insister.

### Phase 4 · Cartographie

**Mode domaine** : génération dynamique des sections selon réponses Phase 3. Default = template pédagogique (voir Output template).

**Mode brand** : pour chaque ligne, **OBLIGATOIRE** tag sourcing inline (HR2). Drill paths selon focus :
- Focus overview → brand.json + _snapshot.md + count entités peuplées
- Focus audiences → audiences/*/profile.json + brand.json#positioning
- Focus offre → spec.json + offers.json + brand.json#commercial
- Focus stratégie → strategy.json + learnings.json (filtrer cross-brand candidates)

### Phase 5 · Décisions actionnables (exactement 3)

**OBLIGATOIRE.** Chaque décision = action concrète + critère pour trancher si pertinent. Pas plus de 3, pas moins. Si moins de 3 vraies décisions émergent → reformuler ou élargir le focus.

## Output template

### Mode `--learn <domaine>`
```markdown
# {Sujet} · Carte pédagogique

## Définition
{1-2 phrases concrètes, pas de jargon}

## Comment ça marche
{Mécanisme en 2-3 lignes max}

## Les 3 leviers principaux
- **{Levier 1}**. {Explication + règle terrain courante si applicable}
- **{Levier 2}**. {Explication}
- **{Levier 3}**. {Explication}

## Là où ça se prend les pieds
- {Piège 1}
- {Piège 2}
- {Piège 3}

## Débats {année} (pas de consensus)
- **{Débat}** : {camp 1 vs camp 2, sans prendre parti}

## Mots utiles
- **{Terme}** : {traduction simple}

## 3 décisions actionnables
1. {Action concrète}
2. {Action concrète}
3. {Action concrète}
```

### Mode `--learn brand=<slug>`
```markdown
# {Brand} · Carte stratégique READ-ONLY

Synthèse READ-ONLY. Lecture du substrate encodé. Aucune mutation.

## Ce qui est posé
- {Insight}.
  [observé · path] OR [déclaré · path] OR [déduit · path1 + path2]

## Ce qui n'est pas posé (gaps)
- {Gap}.
  [gap · path vide]

## Ce qui mérite ton attention
- {Take sourcé du croisement de plusieurs gaps ou observés}.

## 3 décisions actionnables
1. {Action sur substrate ou choix opérateur}
2. {Action sur substrate ou choix opérateur}
3. {Action sur substrate ou choix opérateur}
```

## Failure mode

| Cause | Action |
|---|---|
| Mode brand + snapshot manquant | **Refuse** + propose `snapshot-brand {slug}`. **NEVER** produire output halluciné. |
| Mode brand + status.json incohérent | Surface conflit + propose `validate-resources {slug}`. |
| Mode domaine + sujet trop vaste (>7 axes naturels) | Propose split en sous-cartos. **NEVER** carte de 30 axes plats. |
| Opérateur demande mutation post-carte | **Refuse** + redirect vers `capture-learning` (single fact) ou skill mutateur dédié. Le skill est strict READ-ONLY. |
| Données encodées contradictoires entre 2 paths | Surface conflit explicite avec tag `[conflit · path1 vs path2]` + flag à l'opérateur, ne pas trancher. |

## Composition Contract

**Consumed by** :
- `build-agent` (optionnel) : LEARN domaine peut précéder Step 2b carto BUILD pour calibrer la dissection. Routing : opérateur chaîne `cartograph --learn X` puis `build-agent agent-X`.
- `brief-day` (extension future) : enrichissement briefing matin sur brand peu connue de l'opérateur (mode brand overview court).

**Consumes from** : aucun skill amont obligatoire. Skill terminal pour le verbe canonique métier `cartographier`. Lit canon brand encodé directement.

**Pattern d'orchestration** : conditional branch (mode domaine vs mode brand routé en Phase 1). Pas de fan-out, pas de pipe séquentiel.

## Surface contract

- Output operator-facing : sections courtes, FR par défaut, langage opérateur sans acronyme doctrine (CI / SED / CMR / SAD / PTD bannis), pas de path leak sauf legitimate reference dans tags sourcing.
- Pas de close orphan. Le bloc "3 décisions actionnables" sert de close contextuel.
- Émojis : interdits sauf ✓/⚠ pour state si nécessaire.
- Em-dashes : interdits (convention `·` → parenthèses, virgule, deux-points, middle dot `·`).

## Cross-référence

- `docs/system/skill-builder-cartography.md` : data cartography (variables → schemas → scaffold-extension). Cartograph est la couche knowledge complémentaire.
- `docs/system/skill-authoring-doctrine.md` : SAD doctrine, contrats skill et composition.
- `docs/system/canonical-matrix-reasoning.md` : CMR matrix-driven generating mode.
- `docs/system/patterns.md § Operator-facing cartography rule` : règle de translation expert → opérateur.
- D#323 : build-agent Step 2b carto BUILD silencieuse (complémentaire mode BUILD).
- D#380 : décision création cartograph + matérialisation verbe canonique pipeline métier.

---

*Skill évolue. Quand l'opérateur corrige une erreur de cartographie ou flag un take inventé, la correction est encodée comme Hard Rule numérotée ci-dessus via `correct-skill`. Règles cumulatives, permanentes.*
