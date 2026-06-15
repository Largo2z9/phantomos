# `_EXAMPLE` · Brand pédagogique Stepprs

> Brand pédagogique du cas canonique PhantomOS · **foot care insoles DTC** inspirée de stepprs.com. Vitrine canon PhantomOS v2.68 pour comprendre à quoi ressemble un territoire de marque bien posé. **NE PAS MODIFIER.** Ignored par `FIRST ACTION` canon (folder prefix `_`).

## Pourquoi cet exemple existe

PhantomOS encode le savoir métier d'une marque en substrat stable (territoire) qui survit aux sessions et alimente la production à la demande (briefs · creatives · ad copy). Cet `_EXAMPLE` te montre comment se traduit ce principe en JSON concrets · annotations canon-aware · cross-refs résolus.

Lis-le avant ta première brand · puis reviens-le consulter quand tu te demandes "à quoi ça doit ressembler quand c'est bien posé".

## Par où commencer · ordre de lecture suggéré

| # | Fichier | Ce que ça démontre |
|---|---|---|
| 1 | `brand.json` | Identity · positioning · purchase_driver · driver_blend · brand_equity_level · creative_zone · competitors · awareness_distribution. Le **squelette stable** de la marque. |
| 2 | `products/massage-insoles/spec.json` | Spec produit avec **4 arbres compositional cartography v3.1** · composition (3 couches) → 4 mécanismes typés → 5 benefits chained avec emotional_signal + latency + evidence_verbatim |
| 3 | `products/massage-insoles/offers.json` | Offer_groups[] · 1 standalone + 3 bundles volume tiered + 3 bundles thématiques + guarantees + shipping rules |
| 4 | `audiences/workers-shifts/profile.json` (mère) puis `nurses-12h/` `warehouse-10h/` `hospitality-retail/` (sous-poches) | Pattern **parent/enfants canon v2.64 sémantique pure**. Mère pose scope général · sous-poches héritent + spécificity_modifiers (trigger · context · vocab spécifiques). |
| 5 | `audiences/chronic-pain-45/profile.json` (mère) puis `plantar-fasciitis-diagnosed/` `heel-pain-general/` (sous-poches) | Démontre **awareness divergence dans le tree** · mère `solution_aware` · sous-poches `product_aware` vs `problem_aware` selon trigger. |
| 6 | `audiences/*/pain_points/PNT-*.json` + `objections/OBJ-*.json` | **Sub-collections canon v2.64** · pain shared = stocké mère · pain spécifique = stocké sous-poche. Chain `surface → consequence → deep` · severity discriminante + tier marker primary/secondary. Cross-refs `mechanisms_addressed[]` + `benefits_served[]`. |
| 7 | `products/massage-insoles/frictions/FRC-*.json` | **Friction sub-product canon v2.64** · friction usage produit · cross-refs `affected_audiences[]` + `affected_pain_points[]` + `mechanisms_workaround[]`. |
| 8 | `angles/ANG-*.json` | **Compositional cartography v3.1 · formula OTRB** · Observation + Tension + Reframe + Bridge · lineage (hook · framework · archetype) + compatibility + cross_refs canonical. 7 angles distribués sur 5 origin_axis (audience · product · category · brand · temporal-cultural). |
| 9 | `roadmap.json` | **4ème arbre canon** · phases timeline + mix axes weighted + production_status + relations cross-entités denormalized. |
| 10 | `status.json` | Niveau de complétion canon + flag `is_example: true`. |
| 11 | `todos.md` · `pending-validations.md` · `session-state.md` | **Couche OS du brand (NEW)** · à quoi ressemble la couche tâche, le buffer de validations / enrichissements ambiants et le log d'activité roulant une fois un brand posé. Vitrine du système todo + des surfaces lues par les navigators, absentes de l'exemple jusqu'ici. |

## Couche OS du brand · todo · validations · session (NEW)

La vitrine montre désormais la couche OS du brand, pas seulement le substrat Context DB. Trois fichiers pédagogiques minimaux ·

- `todos.md` · sections canon `In Progress · Backlog · Flags · Blocked · Archive` et format de ligne `- [ ] Name | P: 0-3 | E | T`. Format de référence · `resources/conventions/todos.json`. Sur ta marque, auto-maintenu par les skills écrivains, tu ne l'édites pas à la main.
- `pending-validations.md` · buffer append-only des micro-validations / enrichissements ambiants (`Context gate · Access gate · Enrichment · Skill candidates`). Ce sont les surfaces lues par les navigators et la cible du crochet de capture de la posture d'investigation (`docs/system/investigation-posture.md § Crochet de capture`).
- `session-state.md` · log d'activité roulant auto-maintenu au write, lu au démarrage de session pour récupérer le contexte.

Ces trois fichiers sont posés en register pédagogique Stepprs (`is_example: true`, validés par construction, zéro friction live) · ils enseignent le format, pas un travail en attente réel. Doctrine du report des étapes différées · `docs/system/onboarding-setup-flow.md`.

## Doctrines canon démontrées · mapping fichier → doc

| Fichier | Doctrine canon démontrée | Doc reference |
|---|---|---|
| Tous JSON | Substrat stable canonisé · territoire de marque | `docs/system/territory-doctrine.md` (v2.67) |
| `brand.json` `spec.json` | Compositional cartography v3.1 · 4 arbres + matrice + modulateurs | `docs/system/compositional-cartography.md` |
| `audiences/*/profile.json` parent/enfants | Sub-audience sémantique pure v2.64 | `docs/system/schema-encoding-doctrine.md` |
| `pain_points/PNT-*.json` chain surface→consequence→deep | Pain-benefit chain doctrine v2.60 | `docs/doctrine/pain-benefit-chain-doctrine.md` |
| `objections/OBJ-*.json` tier + severity discriminante | Objections mapping doctrine | `docs/doctrine/objections-mapping-doctrine.md` |
| `angles/ANG-*.json` formula OTRB | Angle anatomy doctrine + canonical-matrix-reasoning | `docs/doctrine/angle-anatomy-doctrine.md` + `docs/system/canonical-matrix-reasoning.md` |
| `audiences/*/` cartography parent/enfants 3 niveaux | Audiences cartography doctrine + map-audiences skill canon | `docs/doctrine/audiences-cartography-doctrine.md` |
| `_meta.is_example` + ignored canon | FIRST ACTION canon · folders prefix `_` ignored | `CLAUDE.md` root workspace-template |

## Ce que tu peux copier · ce que tu ne dois pas copier

**Copie le squelette** ·
- Structure des dossiers (`brands/{slug}/products/{p}/` · `audiences/{a}/pain_points/PNT-XX.json` · etc.)
- Pattern des `_field_types` riche per field (stated/observed/derived/structured)
- Annotations `$comment` quand un choix est non-trivial (positionning · pain category · etc.)
- Cross-refs canonical IDs (PNT-XX · OBJ-XX · FRC-XX · ANG-XX) entre les fichiers

**Ne copie pas** ·
- Mock data financials (revenue $1.2M/mois · LTV $65 · etc. inventés pédagogie)
- Verbatims clients (Mike Kowalski · Dean H · etc. captés du scrape Stepprs · pas applicable à ta marque)
- Audience labels (workers-shifts · chronic-pain-45 · etc. spécifiques Stepprs)

## Annotations canon-aware

Chaque fichier porte ·
- `$comment` racine explicite "EXEMPLE pédagogique · vitrine canon X"
- `_meta.is_example: true` (gate canon supplémentaire)
- `_meta.example_canon_showcased[]` · liste explicite des doctrines canon démontrées
- `_field_types` riche per field
- `validation_status: "validated"` (par construction pédagogique · pas via test ROAS réel)

Audiences mères canon v2.64 portent `_meta.cross_narrative_notes` quand pattern cross-audience targeting observed (cf `workers-shifts` + `chronic-pain-45` cross-narrative TrendTrack live 2026-05-16). NEW field additif backward compat · documente la distinction cartographie substrat vs ad targeting runtime sans casser pattern parent/enfants sémantique pure.

## Parcours pédagogique · `/breakdown stepprs`

Slash command vitrine qui démontre chaque doctrine PhantomOS via ce cas Stepprs concret. 13 chapitres structurés en 5 couches + 3 dimensions transverses (modèle · règles · templates · métriques · rituels · intelligence · apprentissage · extension). Lecture séquentielle ~30 min, drill direct sur un topic possible.

```
/breakdown stepprs                → index + parcours suggéré
/breakdown stepprs principe       → substrat vs production
/breakdown stepprs composition    → 4 couches chaînage
/breakdown stepprs vocabulaires   → registres canon fermés
/breakdown stepprs angles         → formula OTRB appliquée
/breakdown stepprs audiences      → hiérarchie vs targeting
/breakdown stepprs investigation  → 5 sections IP
/breakdown stepprs production     → brief copy en 5 min
```

Cible · opérateur marketeur, créa, stratège paid qui veut comprendre comment PhantomOS structure le savoir métier et produit des outputs reproductibles.

## Pour aller plus loin

- **Construire ta brand** · lance `/onboard-brand` (chain `setup-brand` → `snapshot-brand` → `validate-resources`) ou `/build-atlas-complete {brand_slug}` (chain progressive cartography v2.68 · gates light entre paliers Phase 1 Macro → Phase 2 Drilling → Phase 3 Audiences hiérarchique → Phase 4 Enrichissement)
- **Doctrine territoire substrat** · `docs/system/territory-doctrine.md`
- **Doctrine progressive-cartography** · `docs/system/progressive-cartography-doctrine.md`
- **Catalogue skills canon** · `.skills/README.md` + `.skills/_manifest.json`

## Canon vs réel · data TrendTrack live (2026-05-16)

Ce `_EXAMPLE` mélange canon pédagogique max-richesse (7 angles diversifiés · 2 audiences hiérarchiques · 4 arbres compositional cartography) ET data réelles sourced TrendTrack API live (skill `trendtrack-enrich-brand` v1.0.0 · ad sample 30 ads cross longest+newest+reach). Les deux ont leur valeur distincte.

**Canon vitrine** (audiences hiérarchiques · 7 angles distincts · 4 arbres compositional cartography) montre les POSSIBILITÉS structurelles que PhantomOS encode.

**Réel Stepprs paid** (capté via TrendTrack API live) montre le PATTERN OBSERVÉ d'un brand 2 ans mature ·
- 1 narrative hero (Michelle plantar fasciitis + 10h shifts work boots) répliqué cross-geo · pas 7 angles distincts
- Audiences workers + chronic COMBINÉES en single ad copy (pas séparées)
- Targeting 18+ broad · pain-based filtering via copy naturel (pas narrow 45+ demographic)
- Geo focus EU heavy (DE main) · pas US prioritaire malgré annonce
- CTA "Walk on Clouds Or It's FREE" capture 2 benefits en single phrase
- Landing variants /pages/review-3-x test funnels advertorial rotation
- Trustpilot 3.4/5 (pas 4.8 site claim) · réalité plus mitigée · justifie objections scepticism canon

### Cartographie audience ≠ ad targeting (distinction importante)

PhantomOS cartographie audiences = SUBSTRAT stable · qui souffre quoi · pain points + objections + JTBD par segment distinct. Canon v2.64 sémantique pure · parent/enfants hiérarchique.

Ad targeting runtime = PRODUCTION decision · qui voit l'ad. Peut COMBINER plusieurs audiences cartographiées en single ad copy si narrative crossover (e.g. Michelle testimonial · plantar fasciitis (chronic-pain-45) + 10h shifts work boots (workers-shifts) en single ad atteint les 2 segments simultanément via copy verbatim).

Les deux ne sont pas contradictoires ·
- Cartographie 7 audiences (mères + sous-poches) reste valide · documente le terrain
- Targeting paid Stepprs réel observé = 1 narrative hero répliqué cross-geo · combine workers+chronic via narrative shared (work boots + plantar fasciitis)
- Première production paid peut commencer simple (1 angle cross-audience comme Michelle hero) puis diversifier au fil des learnings

L'opérateur ne doit PAS forcer 1 ad par audience cartographiée · le canon permet flexibilité production runtime selon scaling strategy (single hero cross-audience VS diversified angles per audience).

**Implication pédagogique** · canon = ce que tu PEUX cartographier · réel = ce que les top performers FONT vraiment. Tes premières productions paid peuvent commencer simple (1 angle hero cross-audience) puis diversifier au fil des learnings · pas l'inverse.

Cross-refs canonical · `learnings.json` LRN-0002 + `angles/ANG-01.json` hero pattern + TrendTrack live capture 2026-05-16.

Plus skill `trendtrack-enrich-brand` v1.0.0 v2.69 · enrichis tout brand existing avec data live (chain lookup → shop profile → ads sample 3 queries → 8 patterns analysés). Pattern reproductible cross spy tools (Foreplay · Atria · Meta Ad Library · BigSpy · etc.) via NEW skills mirror.

8 patterns captured dans `learnings.json` post-enrichment Stepprs · ranked confidence · cross-refs canonical PNT/OBJ/ANG/mechanisms/benefits.
