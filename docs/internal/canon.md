# Canon interne PhantomOS

Glossaire technique reference-grade pour contributeurs et auteurs internes. Vocabulaire système, doctrines, disciplines, briques typées, méta-vocabulaire. Pour le vocabulaire opérateur user-facing, cf `lexicon.md`.

## Sens canon du mot "canon"

Le mot "canon" porte 7 sens distincts dans le corpus PhantomOS, hiérarchiquement imbriqués (polysémie documentée, pas fragmentée par renames). Désambiguïsation v2.84.3.

| Sens | Description | Marqueurs contextuels | Exemples |
|------|-------------|----------------------|----------|
| **S1** | Doctrine verrouillée · source de vérité | "doctrine canon", "principe canon", "règle canon" | Contextual Intelligence est canon. |
| **S2** | Archétype pédagogique pour tangibilité | "cas canonique", "vitrine canon", "exemple canon" | `_EXAMPLE/stepprs` est le cas canonique. |
| **S3** | Seuil qualité matrice production (CMR 95%) | "seuil canon", "qualité canon", "95% qualité" | CMR atteint le canon à 95% senior-quality. |
| **S4** | Formule compositionnelle typée | "formule canon", "compositional canon", "OTRB", "schema canon" | Angle = formule canon Observation × Tension × Reframe × Bridge. |
| **S5** | Référentiel partagé cross-système | "atlas canon", "frameworks canon", "library canon" | Atlas canon copy = 11 couches × 58 fiches. |
| **S6** | Copy ou archétype validé asset library | "canon validé", "validations canon" | Hooks canon = top-performers archivés. |
| **S7** | Terminologie normalisée FR canon | "FR canon", "naming canon", "terme canon" | `opérateur` est canon (vs `operator`). |

Hiérarchie · S1 → S3 → S4 → S5 → S6 · S7 transversal. Le contexte (marqueurs ante/post) tranche le sens à chaque occurrence.

## Système

- **PhantomOS** · operating system multi-agents pour le métier d'une marque · encode le savoir métier en substrat opérable, exécute les tâches, capitalise les apprentissages.
- **Context Engine** · moteur de données interne · entités JSON par marque, règles de qualité, pipelines de validation.
- **Template** · version vierge déployable de PhantomOS sous `workspace-template/` · source de vérité pour toute release.
- **Instance** · workspace déployé pour un opérateur · cloné depuis le Template, enrichi à l'usage.
- **Substrat** · savoir métier d'une marque encodé en objets typés persistants sous `brands/{slug}/` · lu par les agents pour raisonner.
- **Connected source** · plateforme externe connectée · typée par catégorie (paid_ads · analytics · ecommerce · email_sms · attribution · creative_intelligence).
- **Mémoire d'exécution** · capacité d'agir aligné hors session, à partir d'artefacts persistés et de règles régissant lecture/mutation.

## Objets phares métier

7 objets que l'opérateur encode pour une marque. Chacun a une définition stable, un mapping technique, un statut de matérialisation.

- **Produit** · spec d'un produit vendu (composition · mécanisme · claims · problème adressé · prix) · `products/{slug}/spec.json`.
- **ProductMap** · terrain typé des problématiques que le produit adresse · brand-specific · `products/{slug}/map.json`.
- **Position de marque** · antagoniste explicite · distinctive promise · point de vue catégorie · inclut Voice/Ton typé · `brand-position.json`.
- **Carte audiences** · audiences potentielles typées récursivement L1/L2/L3 · non sourçable = pas une audience · `audiences/{slug}/profile.json`.
- **Carte angles** · angles d'attaque possibles · formule canon Observation × Tension × Reframe × Bridge (OTRB) · origine typée par `origin_axis` (5 valeurs) · cycle `meta.validation_status` (hypothesis → tested → validated → scaled → fatigued) · `brands/{slug}/angles/{ANG-N}.json`. Cross-ref · `resources/templates/creative-formula.md`.
- **Creative** · 3 plans · **Concept** (objet intent persuasive · audience × insight × angle × mécanique · stable, transposable) · **Creative** (instance déployée d'un concept · 1 créa = 1 fichier) · **Variant** (du même `concept_id` avec 1-2 variables changées) · `creative.schema.json#concept_id`, `#variant_of`, `#variant_axis`.
- **Stratégie** · goals annuels · focus mensuel · priorités · `strategy.json`.
- **Apprentissages** · faits opérationnels append-only (workarounds · compliance · résultats tests) · `learnings.json` · inclut TestResult typé `{hypothesis, metric, sample, duration, result, status}`.

## Briques typées

Centralement typées, référencées par les schemas au lieu d'être redéclarées dans chaque objet. Règle dure · type uniquement ce qui circule entre objets.

- **Pain** · souffrance identifiée · profondeur typée par ChainNiveau (Pain · Symptom · Cause · Block) · circule dans Audience, Spec produit.
- **Bénéfice** · gain identifié · profondeur typée par ChainNiveau (Bénéfice · Outcome · Emotion · Identity) · circule dans Spec produit, Offer, Angle.
- **JTBD** · job que l'audience cherche à accomplir (Job To Be Done) · circule dans Audience, Strategy.
- **AwarenessStage** · niveau de conscience face au problème (Schwartz) · unaware · problem-aware · solution-aware · product-aware · most-aware · fluide, contextuel · circule dans Audience, Angle, Copy.
- **ChainNiveau** · chaîne de profondeur d'une brique · optionnelle par défaut, obligatoire en mode défensif.

## Atlas brand

Concept canonique upstream pour cartographie holistique data e-commerce d'une marque. Composé de 7 entités core (brand · spec · offers · profile · angle · learnings · strategy) + 2 dérivés (creatives produced · scoring matrix). Navigable via `/phantom` cockpit. Distinct d'Atlas canon copy (S5 cross-brand référentiel). Doctrine · `docs/system/atlas-brand.md`.

## Atlas canon copy

Référentiel typé partagé du copywriting · 11 couches × 58 fiches (frameworks · hooks · angles · niveaux-schwartz · archetypes-voix · formules-titres · objections · construction-offre · leads · formats-livrables · persuasion). Sources canoniques · Schwartz (Breakthrough Advertising) · Cialdini · Halbert · Sugarman · Hormozi · Carlton · Jung. Storage · `resources/canon/copy/{layer}/{tool}.json`. Schema · `canon-tool/1.0`. **Mécanisme atlas vivant** · 4 skills (`produce-paid-angles`, `produce-copy-brief`, `mine-voc`, `learn-from-session`) consomment et alimentent via `validations[]` append-only (operator-gated promotion). Doctrine · `docs/system/atlas-canon-copy.md`.

## Mechanisms (spec)

Brique typée du produit · many-to-many spec ↔ mécanisme ↔ bénéfice. Chaque mécanisme · `mechanism_id` (MEC-NN) · `name` · `target` (cible biologique/cognitive/comportementale) · `mode_of_action` (cofactor · antioxidant · adaptogen · etc) · `time_window` (immediate/7d/14d/30d/60d/90d+) · `evidence_level` (clinical_cited/efsa_validated/anecdotal/etc) · `market_sophistication` (low/medium/high) · `triggered_by_specs[]`. Schema · `spec.schema.json#mechanisms[]`. Distinct de Mécanique (creative · device narratif d'une créa · `creative-mechanics-registry.md`).

## Cellule

Unité de production d'un livrable. Croisement typé Audience × Angle × Canal × Mécanique. Objet runtime composé à la production, pas stocké. L'artefact résultant (LP · ad · email) est sourcé vers les briques utilisées.

## Sourçabilité · Provenance · Triangulation

- **Sourçabilité** · capacité d'une donnée à être tracée vers une source observable · règle dure · non sourçable = pas une donnée.
- **Provenance** · tag inline par champ · `_source_meta = {origin, confidence, evidence, validation_status}`.
- **Triangulation** · validation par croisement d'au moins 3 sources indépendantes · obligatoire pour tout champ load-bearing.

## Doctrines

Audience · contributeurs et auteurs internes. Acronymes développés ici, utilisés seuls ensuite.

- **Contextual Intelligence (CI)** · doctrine maître · l'agent raisonne sur l'univers business plutôt que de remplir des formulaires · `docs/system/contextual-intelligence.md`.
- **Schema Encoding Doctrine (SED)** · rigueur d'encodage du substrat · mutations gated · `_field_types` · sourcing · triangulation · append-only · `docs/system/schema-encoding-doctrine.md`.
- **Canonical Matrix Reasoning (CMR)** · mécanisme de production · schéma typé croisé avec matrice canon · sortie au seuil canon S3 95% qualité · `docs/system/canonical-matrix-reasoning.md`.
- **Skill Authoring Doctrine (SAD)** · création et évolution des skills consommant SED et CMR · `docs/system/skill-authoring-doctrine.md`.
- **Provenance & Trust Doctrine (PTD)** · authorship multi-opérateur · canon comme produit · skills marketplace · activée sur triggers · source R&D.
- **Doctrine Governance** · méta-process · promotion · amendement · rétraction · résolution de conflits entre doctrines · `docs/system/doctrine-governance.md`.

## Disciplines

- **Encodage compositionnel** · représenter tout objet métier comme équation de variables typées décomposables · "on ne décrit pas, on compose" · `research/encodage-compositionnel-2026-05-01.md`.
- **Compositionnel** · assemblage de variables par règles typées.
- **Modulaire** · substitution d'une variable sans casser le reste.
- **Typage récursif** · chaque variable est un type qui se compose · règle dure · type uniquement ce qui circule.
- **Two-tier rule** · principe architectural CI · couche mécanique strict enforcement (mutations · schemas · paths · ops destructives) · couche sémantique strict trust (audience · ton · claims · recommandations) · `CLAUDE.md`.
- **Génération neutre** · remplir le substrat sans filtre brand au stade découverte · anti biais de confirmation.
- **Apprentissage par lancement** · construire le substrat par opération réelle (ship rough · observe · refine), pas seulement en amont.
- **Séparation des voix** · distinguer ton agent (`voice.md`) du ton copy produit (DR · voix de marque · registre vente).

## Pipeline métier

Verbes ordonnés du cycle métier · **cartographier** (couvrir l'ensemble d'un champ) · **conceptualiser** (nommer précisément chaque variable) · **modéliser** (poser la structure typée · output schema) · **paramétrer** (injecter valeurs dans axes variables du substrat pour produire output) · **processiser** (transformer concept modélisé en étapes exécutables · output SOP/skill) · **systémiser** (intégrer process dans système global) · **anatomie** (décomposer objet en parties typées · outil transversal modélisation).

Pair conceptuel canon · cartographier (lire/structurer) ↔ paramétrer (injecter/composer).

## Patterns d'évolution

- **Cycle de validation** · lifecycle objet testable · hypothesis → tested → validated → scaled → fatigued · transition gated par test instancié.
- **Cycle de maturation** · lifecycle remplissage objet du substrat · rough → refined → mature · transition par enrichissement et triangulation.
- **Modes d'effort** · 3 niveaux d'investissement par opération · rapide · robuste · défensif.

## Extension layer

Toute addition construite par l'opérateur au-dessus du core workspace · custom entity · sidecar schema · custom skill · external pipeline. Suit 3 règles · schema déclaré · registered ou discovered · README documentant le purpose. Doctrine · `docs/system/extending.md`.

- **Custom entity** · nouveau type scopé par marque · `brands/{slug}/custom/{entity_type}/` · schema canon-compliant + instances + README · enregistrée dans `index.json → extensions[]`.
- **Sidecar schema** · extension append-only de champs sur entité core, sans modifier le schema core · `brands/{slug}/{entity}.extensions.json` · `_extends` déclaré · jamais override ni remove · mergé au runtime.
- **Core namespace vs custom namespace** · skills shippés sous `.skills/skills/{name}/` maintenus par releases · skills opérateur sous `.skills/skills/custom/{name}/` intacts aux upgrades.
- **Gate 5 dimensions** · séquence appliquée par `check-existing-encoding` avant scaffold · core entities · active-brand sidecars · active-brand custom entities · sibling-brand custom entities · shared resources. Match = route-to-existing. No match = genuinely-new.
- **Promotion threshold** · heuristique extension custom → vertical pack ou core · même pattern chez 3+ marques avec schemas convergents · décision finale manuelle.
- **Parametric composition** · génération par traversée de banques curées (angles · mécaniques · formats · preuves · hooks) plutôt que génération libre.

## Vocabulaire externe

Termes pour comm externe (tweet · LinkedIn · pitch · README). Cohérent avec "context engineering" mais plus spécifique.

- **Context Layering** · construire couche par couche l'environnement dans lequel l'agent raisonne.
- **Decision Trace** · raisonnement loggé derrière une correction, pas seulement la correction · champ `reasoning` ou `trace` dans `learnings.json`.
- **Skill Graph** · nœuds atomiques interconnectés · lecture par index · traversée sélective.
- **Feedback Loop** · agent propose, opérateur corrige, Decision Trace loggée, graphe enrichi, agent propose mieux · définit le compound effect.

## Propriétés émergentes

- **Spécificité par construction** · le copy produit est reconnaissable par le client cible · test · masque le nom de la marque, est-ce reconnaissable ? Émerge quand substrat rempli avec rigueur.
- **Réutilisation** · même brique typée sert dans N livrables · définie une fois, exploitée partout · justifie économiquement l'effort d'encodage initial.
- **Densification** · le substrat s'enrichit avec chaque opération · compound effect métier.

## Méta-vocabulaire

- **Doctrine** · principe raisonné qui oriente toutes les décisions d'un domaine (ex Contextual Intelligence). Canon FR.
- **Discipline** · pratique appliquée servant une doctrine (ex Encodage compositionnel sert l'intelligence contextuelle). Note · 21 fichiers `*-discipline.md` identifiés à renommer `*-doctrine.md` · sprint v2.85.0 dédié.
- **Règle dure** · invariant non-négociable, gardé par hook ou refus runtime.
- **Convention** · accord local stable, modifiable par décision.

## Cross-refs

`CLAUDE.md` (two-tier rule) · `lexicon.md` (vocabulaire opérateur user-facing) · `docs/system/contextual-intelligence.md` · `docs/system/schema-encoding-doctrine.md` (rename pending v2.85.0+) · `docs/system/canonical-matrix-reasoning.md` · `docs/system/atlas-brand.md` · `docs/system/atlas-canon-copy.md` · `docs/system/voice-doctrine.md` · `docs/system/extending.md` · `resources/templates/creative-formula.md` · `decisions.md` (D#129 · D#252 · D#237 · D#307-308 · D#326-332 · D#382-383 · D#391 · D#450-453) · `docs/README.md` (3 niveaux contexte L1/L2/L3).

---

*Dernière mise à jour · 2026-05-20.*
