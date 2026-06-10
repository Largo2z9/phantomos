# SOP · Curation cross-brand (corpus → bibliothèques partagées)

> Phase 2 du seeding. La phase 1 (décortiquer des ads en `competitive-intel/{batch}/{RCV-NN}/decomposition.json`) bâtit le **corpus brut**. La curation FAIT MONTER les patterns récurrents vers les **bibliothèques cross-brand shippées** (`resources/concepts/`, `resources/registries/hooks/`, `resources/registries/archetypes/`), sous forme d'objets `library-pattern.schema.json`.
>
> **État** · v1 MANUELLE (opérateur/analyste curate à la main depuis le corpus). Une skill `curate-pattern` automatisée = chantier futur. Ce doc = la doctrine que cette skill encodera.

## La règle de promotion (le garde-fou)

Un pattern passe **`watch` → `promote-ready`** seulement s'il est attesté par **≥ 2 SOURCES INDÉPENDANTES**.

**Une source = un système créatif indépendant, PAS une marque.** Découverte canon (D#485) : **hims et hers sont une seule factory créative genrée** (ads-miroir mot-pour-mot : RCV-143≈174≈194). Les compter comme 2 marques = **faux-positif de diversité** → sur-promotion garantie de patterns mono-source.

Donc on compte par **factory / système**, pas par logo :
- karacare = 1 source (FR · beauty-hair)
- naali = 1 source (FR · wellness-supplement)
- hims + hers = **1 source** (US · telehealth-rx)

`independent_source_count` du schéma encode ce compte factory-aware. `confirming_sources[].source` nomme la factory, pas la marque isolée.

## L'échelle de confiance

| Statut | Critère | Action |
|---|---|---|
| `watch` | 1 source indépendante | Garder, NE PAS promouvoir. Attendre une 2e source indépendante. |
| `promote-ready` | ≥ 2 sources indépendantes | Brique de bibliothèque utilisable par les skills côté A (génération de concept). |
| `deprecated` | invalidé (perf réelle ou contre-exemple) | Marquer, ne pas supprimer (append-only esprit). |

Un pattern vu chez karacare + naali + himshers = **3 sources** = solide. Un pattern US-only (hims+hers) = **1 source** = `watch`, même s'il est sur 20 ads.

## Le curseur sectoriel (4e invariant · `vertical_scope`)

Chaque pattern porte ses **verticales d'origine** + une **largeur** (`mono-vertical` / `cross-vertical` / `universal`). Ce n'est **jamais un filtre**, c'est une distance pour le régime explore/exploit de A (`freedom_cursor`) :
- **exploit** → rester dans la verticale de la marque opérée (emprunt proche, sûr).
- **explore** → oser reslotter un pattern d'une verticale lointaine (emprunt CONSCIENT, surfacé à l'opérateur).

Un pattern `universal` (vu cross-vertical ET cross-géo, ex le timeline-ladder) est le plus sûr à emprunter partout. Un pattern `mono-vertical` (ex le Rx-as-differentiator du telehealth) ne se reslotte qu'en mode explore assumé.

## Le pont vers le génome (`related_mechanic_ids`)

Chaque pattern liste les enums `decomposition.schema` (= `genome.schema`) qu'il instancie (`hook.mechanic_id`, `beat_type`, `proof_type`). C'est ce qui permet aux skills côté A de **générer** un génome qui porte le pattern, et de retrouver un pattern depuis un génome. Pattern ↔ mécanique = many-to-many.

## Le process (v1 manuelle)

1. **Clusterer** le corpus par mécanique (grep `hook.mechanic_id` / `beat_type` / `proof_type` cross-décompositions).
2. **Compter les sources indépendantes** (factory-aware) qui portent le cluster.
3. **Extraire** le squelette paramétrique commun + les slots + les réalisations concrètes (copy réelle) par source + les `RCV-NN` de traçabilité.
4. **Tagger** `vertical_scope` (origines + largeur) et `related_mechanic_ids`.
5. **Écrire** l'objet `library-pattern` dans son home (concept → `concepts/`, hook → `registries/hooks/`, archétype → `registries/archetypes/`), valider contre le schéma.
6. **Statuer** `promote_status` selon le garde-fou ≥2 sources.

## Home par type

| pattern_type | home |
|---|---|
| `concept-structural` | `resources/concepts/{slug}.json` |
| `hook-mechanic` | `resources/registries/hooks/{slug}.json` |
| `fiche-archetype` | `resources/registries/archetypes/{slug}.json` |
| `proof-pattern` | `resources/registries/proof/{slug}.json` |
| `offer-pattern` | `resources/registries/offers/{slug}.json` |

## À durcir plus tard (flaggé, pas construit · anti-over-eng)

- **Normalisation ingrédient** avant clustering (accents/casse/source · « Magnésium » vs « Magnesium », 30 variantes de « mélatonine végétale ») — sinon le clustering par ingrédient casse.
- **3e signal = perf réelle.** La curation actuelle promeut sur la RÉCURRENCE cross-source. Le signal le plus fort (la perf gagnante réelle) viendra de la feedback loop (`perf-feedback-loop.md`) quand des créas produites auront tourné. Un pattern `promote-ready` + confirmé gagnant en perf = canon.
- **Skill `curate-pattern`** automatisée (clustering + comptage factory-aware + draft de l'objet) = chantier futur.
