# Creative Axis Canonicalization Doctrine · Operating Doctrine

> Canonique v2.88.0+. Doctrine canon qui codifie la hiérarchie créative stratégique (brand promise · big idea audience-scoped · axe créatif · créa instance) et le mapping du sous-workflow A Creative Strategy v3 vers l'équation compositionnelle v3.1 NOYAU × CONTEXTE × MODIFIEURS. Doctrine sœur de `creative-formula.md` v3.1 (équation maître substrate · CAC pose le niveau au-dessus stratégique audience-scoped), `creative-mechanics-registry.md` (29+ mécaniques canonisées · CAC référence par axe créatif), `output-clarity-doctrine.md` v2.79.2+ (visualisers matriciel ASCII enforcement), `pre-gate-evaluator-doctrine.md` NEW v2.88.1 (evaluator-optimizer A6 5 checks structurels). Ferme le gap *"comment passer d'une requête opérateur DTC à des assets publicitaires cohérents produits depuis l'atlas brand · qualité créative ne se joue pas dans la production IA mais dans la décomposition stratégique amont"* posé en R&D Creative Strategy session 25-27 mai 2026.

> **⚠ SUPERSEDED PARTIEL · v2.89.0 (2026-06-07).** Les références à `pre-gate-evaluator-doctrine.md` (évaluateur A6), à **HR-CAC-4**, et au `creative_axis.schema` sont **obsolètes** : ces briques n'ont jamais été construites, et la direction 2.89.0 (génome `genome.schema` + gate QC de sortie `qc-creative`) les a leapfroguées. RESTENT CANON : la hiérarchie créative (brand promise · big idea audience-scoped · axe créatif · instance) et le mapping vers l'équation v3.1. Ne pas implémenter le pre-gate-evaluator.

---

## 1. Thèse fondatrice

> Les marques DTC qui scalent à 500+ ads actifs (GLP-1 SOS, Hims, Naali) ne sont pas celles qui écrivent les meilleures phrases · ce sont celles qui décomposent leur matière en couches activables (audience × pain × angle × mécanique × voice × proof) et recomposent intelligemment via factory mode. La qualité créative est une décomposition fine en amont, pas une écriture finale.

**Définition canon creative axis canonicalization** · ensemble des pratiques opérationnelles qui codifient la hiérarchie créative stratégique (brand promise → big idea audience-scoped → axe créatif → créa instance) et garantissent que tout output créatif est ancré dans l'atlas brand encodé via decomposition compositionnelle traçable. La canonisation répond à 4 questions miroir ·

1. *"À quel niveau de la hiérarchie créative cet output vit-il ?"* (brand promise vs big idea vs axe créatif vs créa)
2. *"L'output est-il ancré dans l'atlas brand encodé ou hand-wavé ?"* (lineage canon obligatoire)
3. *"L'axe créatif mobilise-t-il l'atlas profond (dream_scenario_narrative · fears · jtbd · beliefs · key_expressions) ou reste-t-il au pain layer fonctionnel ?"* (psychographic depth gate)
4. *"L'incarnation support-spécifique respecte-t-elle la mécanique narrative et la typology_st de l'axe parent ?"* (cohérence cross-niveau)

**Différenciation canon vs creative output ad-hoc** ·

| Layer | Output ad-hoc | PhantomOS canon Creative Axis Canonicalization |
|---|---|---|
| Hiérarchie | 1 niveau plat (la "créa") | 4 niveaux explicites (brand promise · big idea · axe · créa) |
| Big idea | mélangée avec angle ou positioning | big idea audience-scoped persistée canon `profile.psychology.big_idea` v2.2 |
| Axe créatif | concept implicite réinventé chaque batch | entité persistée `creative_axis.json` lineage angles_ref + mechanique_id + character_archetype + typology_st |
| Atlas mobilisé | pain points + audience identity | 5 dimensions canon (dream_scenario_narrative · jtbd · beliefs · fears · key_expressions) gate evaluator A6 |
| Cohérence cross-support | espérée | enforced via typology_st et temporal_subtype creative-mechanics-registry |
| Traçabilité | absente | lineage canon angle_ref · big_idea_ref · mécanique_id surfacé proactivement |

Cette doctrine canonise la hiérarchie 4 niveaux + le mapping workflow A v3 ↔ équation v3.1 + les obligations de mobilisation atlas profond + les conventions de visualisation matriciel ASCII Output Clarity-compliant.

---

## 2. Le problème résolu

Sans Creative Axis Canonicalization canon ·

1. **Confusion hiérarchique cross-skills.** `compose-creative` produit des créas, `produce-paid-angles` produit des angles, `decompose-ad` reverse-engineer des ads existantes, mais aucun canon ne pose comment les 4 niveaux (brand promise · big idea · axe · créa) s'articulent et persistent. Drift session-to-session · output dispersé · réutilisation cross-batch impossible.

2. **Big idea audience-scoped non encodée.** Pre-v2.88.0, `profile.json` ne contient pas de champ `big_idea`. Conséquence · à chaque batch, la creative strategist redérive la big idea from scratch, perdant la cohérence cross-batch et la mémoire long-terme.

3. **Axe créatif réinventé chaque batch.** Pre-v2.88.0, pas de schema `creative_axis.json`. Conséquence · les axes créatifs vivent en mémoire conversationnelle ou dans des briefs markdown jetables, jamais persistés ni réutilisables cross-batch ni indexables par learnings.

4. **Mobilisation atlas profond aléatoire.** Pre-v2.88.0, `dream_scenario_narrative` v2.87.4 existe mais pas de gate evaluator-optimizer qui force sa mobilisation au moment de la conception des axes créatifs. Conséquence · axes restent au pain layer fonctionnel, perdent la racine psychographique Schwartz/Kern · copy générique potentiel.

5. **Typology spatial/temporel implicite.** Pre-v2.88.0, `creative-mechanics-registry.md` documente 29+ mécaniques sans typology canon spatial/temporel. Conséquence · décision cross-support viable vs support-natif faite intuitivement, dérive cross-batch, friction sur les axes qui ne se déclinent pas bien en cross-support.

6. **Pas de mapping explicit workflow A v3 ↔ equation v3.1.** Conséquence · session R&D Creative Strategy a réinventé 65% de vocabulaire existant (axe créatif vs CONTEXTE layer, direction narrative vs angle.formula, hook lock pattern vs stop_scroller, etc.). Risque récurrent si pas canonisé.

Creative Axis Canonicalization Doctrine = doctrine canon qui ferme ces 6 gaps via hiérarchie 4 niveaux + mapping equation + gate atlas profond + Hard Rules enforcement runtime cross-skills.

---

## 3. Hiérarchie canon · 4 niveaux

Hiérarchie créative canon v2.88.0+ stricte ·

```
1 · Brand promise (optionnelle · marque-globale)
    │
    └─→ N big ideas (1 par audience encodée)
         │
         └─→ M axes créatifs (par big idea · cross-support OU support-natif)
              │
              └─→ K créas instances (par axe · 1 hook variant par incarnation support)
```

| Niveau | Définition | Persistance canon | Cardinalité |
|---|---|---|---|
| **Brand promise** | Promesse centrale de la marque, marque-globale, audience-agnostique. Optionnelle · ne pas forcer si la marque ne l'a pas formalisée. | `brand.json#brand_promise` (optionnel · à canoniser si Largo le décide post-validation runtime) | 0-1 par marque |
| **Big idea audience-scoped** | Pitch stratégique 1-2 phrases qui condense la promesse activable pour une audience précise. Niveau au-dessus de l'angle (compositionnel) et au-dessous de la brand promise (marque-globale). | `audiences/{slug}/profile.json#psychology.big_idea` v2.2 NEW | 1 par audience encodée |
| **Axe créatif** | Niveau matriciel intermédiaire entre big idea et créa. Décline la big idea sur un angle particulier avec mécanique narrative + character archetype + typology_st locked. Produit par sous-workflow A étape A6 (creative strategist orchestrateur + evaluator-optimizer). | `brands/{slug}/axes/{creative_axis_id}.json` NEW v2.88.1 (cf `creative_axis.schema.json` shipped v2.88.1) | 3-5 par batch typique · réutilisable cross-batch |
| **Créa instance** | Ad finale individuelle · un fichier média prêt à pousser sur Meta/TikTok. Produit par sous-workflow B (production IA) ou usage externe (agency, équipe interne). | `brands/{slug}/produced/{CRT-NN}.{json,jpg,mp4}` existant + `creative.json` schema v1.2 | K par axe · variants_axis=hook_swap dominants |

**Règles canon hiérarchie** ·

- **Pas de saut de niveau.** Une créa instance doit avoir un `creative_axis_id` parent. Un axe créatif doit avoir un `big_idea_ref` parent. Une big idea vit dans une audience encodée. Pas d'output orphelin canon-conforme.
- **Cohérence descendante obligatoire.** Si la big idea audience-scoped active fears `[F1, F2]` et dream_scenario `D1`, l'axe créatif doit cohéremment activer un sous-ensemble de ces dimensions (pas toutes obligatoirement, mais aucune dimension non-encodée audience).
- **Réutilisabilité cross-batch.** L'axe créatif persisté permet de relancer un batch créa avec hooks variants différents sur le même axe validé · économise le raisonnement copywriting (effort dense, fréquence basse) au profit de l'instanciation hook (effort léger, fréquence haute).

---

## 4. Mapping workflow A v3 ↔ équation v3.1

Le sous-workflow A Creative Strategy v3 produit en 8 étapes (A1-A8) un brief strategy actionnable. Son vocabulaire externe (posé en session R&D 25-27 mai 2026) doit être réconcilié au canon equation v3.1 NOYAU × CONTEXTE × MODIFIEURS pour cohérence cross-skills.

### Mapping précis

```
Workflow A v3 Creative Strategy   ↔   Equation v3.1 PhantomOS canon
─────────────────────────────────────────────────────────────────────

Big idea audience-scoped              N'est PAS dans equation v3.1 · 
                                      vit au niveau au-dessus, meta-stratégique
                                      audience-scoped (canon profile.psychology.big_idea)

Axe créatif (composants)              CONTEXTE layer enrichi ·
                                      • angle.formula (= "direction narrative" externe
                                        absorbée dans angle.formula Obs+Tension+Reframe+Bridge)
                                      • pain_point (= "mécanisme à transmettre" externe)
                                      • persona + character_archetype (= "character archetype" externe)
                                      • proof (= "matière brand mobilisée" externe)
                                      
                                      + NEW canon v2.88.0 ·
                                      • typology_st (spatial/temporel)
                                      • temporal_subtype (si typology_st = temporel)
                                      • hook_pattern_default (référence hook-formulas.md)
                                      • narrative_direction (pitch 3-5 lignes cross-support)

Incarnation support-spécifique        NOYAU layer instancié ·
                                      • mécanique (= "mise en scène" externe)
                                      • format (= "support" externe)
                                      • stop_scroller (hook_layer + visual_layer)
                                      • ton
                                      + composants visual_identity produit instanciés
                                      + hook_pattern_override (si applicable) + reason obligatoire

Hook variant                          variant_of + variant_axis = hook_swap
                                      (creative.schema v1.2 existant)
                                      + obligation mobilisation verbatim OR key_expression
                                      (cf doctrine pre-gate-evaluator-doctrine HR-EVAL-5)

Modifieurs (occasion, offer,          MODIFIEURS layer (inchangé equation v3.1)
destination, etc.)
```

### Conséquence canon

Le workflow A v3 est **cohérent avec l'equation v3.1**, ce n'est PAS une réinvention fondamentale. Le vocabulaire externe ("axe créatif", "incarnation support-spécifique", "direction narrative", "hook lock pattern") est une réécriture partielle qu'il faut **harmoniser au canon** ·

- Côté code · adopter naming `creative_axis_id`, `incarnation_id` (sub-objet creative.json), pas `axis_id` (collision avec `origin_axis` angle.schema)
- Côté opérateur · garder "axe créatif" en surface (force pédagogique préservée), retirer "direction narrative" au profit de `angle.formula` + `creative_axis.narrative_direction`
- Côté schema · `creative_axis.schema.json` NEW v2.88.1 sérialise l'entité avec lineage canon (big_idea_ref + audience_slug + angles_ref[] + mecanique_id)

---

## 5. Vocabulaire canon harmonisé

Vocabulaire canon v2.88.0+ post-réconciliation R&D Creative Strategy ·

| Terme adopté canon | Terme externe abandonné | Path lookup |
|---|---|---|
| Brand promise | (identique) | `brand.json#brand_promise` (futur · à canoniser post-validation runtime) |
| Big idea audience-scoped | (identique) | `audiences/{slug}/profile.json#psychology.big_idea` v2.2 NEW |
| Axe créatif | (identique côté opérateur · code `creative_axis_id`) | `brands/{slug}/axes/{creative_axis_id}.json` NEW v2.88.1 |
| Créa instance | "concept créatif" (collision · abandonné) | `creative.json` v1.2 existant + CRT-NN |
| Mécanique narrative | "mise en scène" (équivalent) | `creative-mechanics-registry.md` (34 fiches canon) |
| Mécanisme produit | (distinct de mécanique) | `products/{slug}/spec.json#unique_mechanism` |
| Angle.formula (Obs+Tension+Reframe+Bridge) | "direction narrative" (au copy level) absorbé dans angle.formula | `angle.schema.json` v1.3 |
| Narrative direction (3-5 lignes pitch axe) | (NEW spécifique au niveau axe) | `creative_axis.narrative_direction` v2.88.1 |
| Hook pattern | "hook lock pattern" (terme externe) | `hook-formulas.md` 15 patterns + `creative_axis.hook_pattern_default` v2.88.1 |
| Hook variant | (identique · variant_axis=hook_swap) | `creative.json#variant_of + variant_axis` v1.2 existant |
| Typology_st | (NEW spatial/temporel) | `creative-mechanics-registry.md` mapping + `creative_axis.typology_st` v2.88.1 |
| Temporal_subtype | (NEW dialogique/démonstratif/narratif/pédagogique) | `creative-mechanics-registry.md` mapping + `creative_axis.temporal_subtype` v2.88.1 |
| Character archetype | (identique côté axe créatif) | `creative_axis.character_archetype` v2.88.1 (distinct de `profile.persona_archetype` côté audience) |
| Incarnation support-spécifique | (terme externe descriptif) | Sérialisé dans `creative.json` existant · pas de schema dédié |
| Evaluator-optimizer | (NEW pattern doctrine) | Cf `pre-gate-evaluator-doctrine.md` NEW v2.88.1 |
| Signal perf historique structuré | (NEW objet) | À canoniser ultérieurement v2.89+ (cf section 11 backlog) |

---

## 6. Spec étape A2 · consultation atlas brand canonique

Étape A2 du sous-workflow A Creative Strategy fait l'audit matière brand disponible avant le plan de cadrage A3. Pour respecter canon ontologie sémantique pure v2.63 + sub-audience v2.64, A2 doit consulter explicitement les paths canon ·

### Consultation obligatoire A2

**1. Identity card brand** ·
- `brands/{slug}/brand.json` · identity, positioning, tone_of_voice, financials, competitors

**2. Audiences encodées** ·
- `brands/{slug}/audiences/{audience_slug}/profile.json` · pour chaque audience visée par la requête opérateur
- Consultation profonde · `psychology.dream_scenario_narrative` (v2.87.4) · `psychology.big_idea` (NEW v2.88.0) · `psychology.fears` (NEW v2.88.0) · `psychology.jtbd` · `psychology.beliefs_limiting` + `psychology.beliefs_facilitating` · `voice.key_expressions[]`
- Lookup `psychology.confidence_chain` pour évaluer solidité épistémique (forte / moyenne / faible / TRÈS_faible)

**3. Pain points · cascade canon v2.63 / v2.64** ·
- **PRIMARY** v2.64 sub-audience · `brands/{slug}/audiences/{audience_slug}/pain_points/{PNT-NN}.json` (owned natif par parent path)
- **FALLBACK** v2.63 top-level · `brands/{slug}/pain_points/{PNT-NN}.json` filtered by `affected_audiences[]` contains `{audience_slug}`
- **FALLBACK ULTIME** v1.7 sub-field legacy · `profile.json#pain_points[]` (pre-v2.63 brands · backward compat lecture)

**4. Objections · cascade canon v2.63 / v2.64** ·
- **PRIMARY** v2.64 sub-audience · `brands/{slug}/audiences/{audience_slug}/objections/{OBJ-NN}.json`
- **FALLBACK** v2.63 top-level · `brands/{slug}/objections/{OBJ-NN}.json` filtered by `affected_audiences[]`
- **FALLBACK ULTIME** v1.7 sub-field legacy · `profile.json#objections[]`

**5. Products · spec + mechanism + visual identity** ·
- `brands/{slug}/products/{product_slug}/spec.json` · identity, specs, mechanism, benefits, problems_solved, proofs, pricing, visual_identity (S55 v2.31 extension)

**6. Offers** ·
- `brands/{slug}/products/{product_slug}/offers.json` · active offers, bundles, pricing, landing pages (cohérent CTA conceptuel axe créatif)

**7. Angles canon brand** ·
- `brands/{slug}/angles/{angle_id}.json` · catalogue d'angles encodés avec formula Obs+Tension+Reframe+Bridge + lineage canon

**8. Learnings · signal perf historique partial** ·
- `brands/{slug}/learnings.json` (append-only) · API workarounds, behaviors, compliance rules, test results · contient les apprentissages indexables par audience_id / angle_id / pain_id pour signal historique

**9. Strategy** ·
- `brands/{slug}/strategy.json` · annual goals, monthly targets, current focus, constraints (compliance verticale, plateforme, géo)

**10. Snapshot digest** ·
- `brands/{slug}/_snapshot.md` · digest 1-2KB cross-entités · lecture rapide pré-drill

### Pattern fallback canon

Cascade v2.64 → v2.63 → v1.7 strict pour pain_points et objections. Skill `compose-creative-batch` (NEW v2.88.2) doit implémenter cette cascade lookup en silent fallback, jamais bloquer si une couche est vide tant qu'une autre couche fournit la donnée.

### Output A2 attendu

État matière par dimension atlas · structuré pour consommation A3-A6 · inclut `confidence_chain` héritée par dimension (signal solidité épistémique) · flag explicite si dimensions critiques absentes (gate humain optionnel pré-A3 si verbatim_count < 5 sur l'audience visée).

---

## 7. Visualisers · Output Clarity Doctrine enforcement

Tous les visualisers du sous-workflow A Creative Strategy respectent strictement `output-clarity-doctrine.md` v2.79.2+ ·

**Posture canonique applicable** · matriciel ASCII (cockpit · synthesis · drill · scan-en-5-secondes), pas prose conversationnelle native (réservée onboarding `/tour`).

**Conformité enforcement** ·
- 5 symboles canon uniques · ✓ ◐ ○ ✗ ⚠ (HR-OCD-1)
- Zéro emoji couleur (🔥 🟢 🟡 🔴 🟠 🟣 ⚪️ ⚫ bannis)
- Headers H2 FR sobres 1-2 mots max (AXES CRÉATIFS · MATRICE · ATLAS MOBILISÉ · DÉCISIONS · LÉGENDE) (HR-OCD-3)
- Séparateurs ━━━ macro-sections · ─── sous-sections (HR-OCD-7)
- Cap output 60-80 lignes max user-visible (HR-OCD-7)
- Action items format stable max 3 (HR-OCD-5)
- Légende symboles au pied obligatoire (HR-OCD-8)
- One thing per line (HR-OCD-4)
- Drill footer minimaliste 3 lignes (HR-OCD-6)
- Zéro jargon Phantom-interne (HR-OCD-2 · mapping `operator-vocabulary-translation.md`)

**Visualiser canon · étape A3 plan de cadrage** · matrice plan avec audiences × pains × supports × régime × budget · symboles canon · validation 1-mot opérateur · drill footer.

**Visualiser canon · étape A6 axes créatifs validés** · dashboard axes en parallèle avec composants détaillés (typology · character · mécanique · direction narrative · atlas mobilisé · evaluator passé) · matrice volumes par axe × support · décisions à trancher au pied · cf section 10 cas anatomique Sereno fictif pour exemple structure.

**Visualiser canon · étape A8 brief strategy final** · header batch · sections par axe avec incarnations + hooks variants · matrice cross-références · enrichissements atlas proposés post-batch · flags compliance pour review production.

---

## 8. Hard Rules canon (HR-CAC-1 à HR-CAC-8)

### HR-CAC-1 · Hiérarchie 4 niveaux respectée · pas de saut

Output créatif canon-conforme respecte hiérarchie brand promise → big idea audience-scoped → axe créatif → créa instance. Pas de créa sans creative_axis_id parent. Pas d'axe sans big_idea_ref parent. Pas de big idea sans audience encodée. Violation = bug invalid output canon.

### HR-CAC-2 · Big idea audience-scoped persistée canon `profile.psychology.big_idea`

Big idea vit dans `profile.json#psychology.big_idea` v2.2, audience-scoped par essence. Jamais marque-globale (sauf brand promise, distincte). Jamais oubliée en mémoire conversationnelle. Validation pre-axis-creation · big_idea populated sur l'audience visée. Violation = bug invalid output canon.

### HR-CAC-3 · Axe créatif sérialisé canon `creative_axis.schema.json`

Axe créatif persisté brand-side avec lineage canon obligatoire · `big_idea_ref + audience_slug + angles_ref[] + mecanique_id + character_archetype + typology_st + hook_pattern_default + narrative_direction + volume_cible_par_support + evaluator_report`. Pas d'axe orphelin en mémoire conversationnelle. Violation = bug invalid output canon.

### HR-CAC-4 · Mobilisation atlas profond obligatoire en A6

Conception d'axe créatif gate evaluator-optimizer A6 check 1 · vérifie mobilisation des 5 dimensions canon · `dream_scenario_narrative` + `jtbd` + `beliefs_limiting∪facilitating` + `fears` + `key_expressions` (avec sample_size >= 5). Si une dimension absente sur l'audience visée, axe créatif refusé en gate ou flag avec degraded confidence (mode confidence_chain v2.87.4 hérité). Violation = bug invalid output canon.

### HR-CAC-5 · Typology_st locked au niveau axe · incarnations cohérentes

Axe créatif lock une `typology_st` (spatial OU temporel) + `temporal_subtype` si applicable. Les incarnations support-spécifiques en A7 doivent respecter cette typology (un axe temporel-dialogique ne s'incarne pas en static structurel). Le check 4 evaluator-optimizer enforce cohérence character × angle × perspective × typology. Violation = bug invalid output canon.

### HR-CAC-6 · Hook pattern default au niveau axe · override avec reason obligatoire

Axe créatif définit `hook_pattern_default` (référence `hook-formulas.md`). Incarnation peut override avec `hook_pattern_override` mais champ `hook_pattern_override_reason` obligatoire si populated · justification 1 ligne minimum auditable. Pas d'override silencieux. Violation = bug invalid output canon.

### HR-CAC-7 · Visualisers respect strict Output Clarity Doctrine v2.79.2+

Tous les visualisers du sous-workflow A Creative Strategy (A3 plan · A6 axes · A8 brief final) respectent strict 6 standards `output-clarity-doctrine.md` v2.79.2+ · 5 symboles canon · zéro emoji couleur · headers FR sobres · séparateurs ━━━ ─── · density modérée · cap 60-80 lignes · légende au pied. Posture matriciel ASCII, pas prose conversationnelle. Violation = bug invalid output canon.

### HR-CAC-8 · Lineage canon traçable cross-niveau

Toute créa produit (post-sous-workflow B) doit traçer le lineage complet · creative.json contient `creative_axis_id` parent · creative_axis.json contient `big_idea_ref` + `audience_slug` + `angles_ref[]` · `learnings.json` indexe par creative_axis_id pour feedback loop. Pas de créa orpheline. Violation = bug invalid output canon.

---

## 9. Anti-patterns canon (AP-CAC-1 à AP-CAC-6)

### AP-CAC-1 · Big idea générique cross-audience

Big idea formulée au niveau marque-globale (perte distinctivité audience-scoped) OR identique entre 2 audiences encodées (perte filter strategy). Pattern canon · 1 big idea par audience · activée par dream_scenario_narrative + fears + key_expressions spécifiques. Pattern correctif · HR-CAC-2 enforcement runtime.

### AP-CAC-2 · Axe créatif réinventé chaque batch

Axe créatif vit en mémoire conversationnelle d'une session, jamais persisté `creative_axis.schema.json`. Conséquence · pas de réutilisation cross-batch, pas d'indexation learnings, perte mémoire long-terme. Pattern canon · sérialisation obligatoire post-validation A6 humain. Pattern correctif · HR-CAC-3 enforcement runtime.

### AP-CAC-3 · Axe créatif au pain layer fonctionnel seulement

Axe conçu en activant uniquement `pain_points` + `audience.identity` (couches fonctionnelles), sans descente racine `dream_scenario_narrative` + `fears` + `jtbd` + `beliefs`. Conséquence · copy générique potentiel, perte distinction Schwartz/Kern. Pattern canon · 5 dimensions atlas profond obligatoires en check 1 evaluator-optimizer A6. Pattern correctif · HR-CAC-4 enforcement runtime.

### AP-CAC-4 · Incarnation incohérente avec typology_st de l'axe

Axe temporel-dialogique (founder-chat) s'incarne en static pur (composition fixe) · structurellement incompatible. Pattern canon · typology_st locked au niveau axe + check 4 evaluator-optimizer enforce cohérence. Pattern correctif · HR-CAC-5 enforcement runtime.

### AP-CAC-5 · Hook pattern override silencieux sans justification

Incarnation override `hook_pattern_default` de l'axe parent sans champ `hook_pattern_override_reason` populated. Conséquence · désalignement axe↔incarnation invisible · perte cohérence cross-incarnation. Pattern canon · reason obligatoire si override · auditable post-batch. Pattern correctif · HR-CAC-6 enforcement runtime.

### AP-CAC-6 · Visualiser sous-workflow A avec emoji couleur ou prose conversationnelle

Visualiser A6 axes créatifs ship 🔥 hot axis · 🟢 validé · 🟡 partiel (au lieu de symboles canon ✓ ◐ ○ ✗ ⚠) OR ship prose conversationnelle longue (réservée onboarding `/tour`). Pattern canon · matriciel ASCII strict Output Clarity Doctrine v2.79.2+. Pattern correctif · HR-CAC-7 enforcement runtime.

---

## 10. Cas anatomique Sereno fictif · illustration visualiser A6

À titre d'illustration pédagogique, voici un exemple de visualiser canon-compliant pour l'étape A6 axes créatifs validés, appliqué au cas Sereno fictif (supplément naturel anti-stress sommeil · audience cadres tech 30-40 · 3 audiences encodées · atlas simplifié).

> **Disclaimer canon** · Sereno fictif sert d'illustration anatomique uniquement. Le contenu Sereno est exemple inventé, la structure du visualiser est canonisable.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AXES CRÉATIFS · Sereno · 4 axes · 15 créas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Audience       cadres tech 30-40
Big idea       "Décrocher du travail sans culpabiliser de ralentir"

─────────────────────────────────────────────────────────────
AXE 1 · founder origin
─────────────────────────────────────────────────────────────

Typology              temporel · narratif · cross-support viable
Character             Léna 34-38 ex-cadre tech reconvertie · casual chic
Mécanique             ugc (creative-mechanics-registry)
Hook pattern default  confession

Direction narrative
  Léna raconte son moment de bascule personnel et son projet
  Sereno comme alternative aux somnifères, en activant la peur
  de devenir comme ses parents sacrifiés et le désir de
  protéger ses weekends.

Direction visuelle conceptuelle
  AI-photoreal ou photos castées lifestyle · intérieur
  appartement parisien · palette tons chauds neutres ·
  lumière naturelle douce

Mécanisme produit à transmettre
  cortisol bloqué + 3 adaptogènes sourcés cliniques ·
  distinction vs concurrents naturels génériques

Résolution à transmettre
  décrochage naturel à 4 semaines · retour weekends apaisés

CTA conceptuel
  "39€ première cure · 30 jours garantis"

Atlas mobilisé        ✓ dream_scenario_narrative ✓ jtbd
                      ✓ beliefs ✓ fears ✓ key_expressions
Positioning           ✓ activé · renforce ce qui distingue
Evaluator             ✓ passé après 1 raffinage

Déclinaisons          6 vidéos · 1 static transfert
Volume                7 créas

[AXES 2-4 omis pour concision · format identique]

─────────────────────────────────────────────────────────────
MATRICE VOLUMES PAR AXE × SUPPORT
─────────────────────────────────────────────────────────────

                       vidéo  static  total
Axe 1 founder origin       6      1      7
Axe 2 testimonial          0      3      3
Axe 3 mécanisme            3      0      3
Axe 4 démolition           2      0      2
─────────────────────────────────────────────────────────────
total                     11      4     15

─────────────────────────────────────────────────────────────
ENRICHISSEMENTS ATLAS PROPOSÉS POST-BATCH
─────────────────────────────────────────────────────────────

⚠ Big idea audience cadres tech à canoniser
⚠ Dream_outcome audience cadres tech non encodé
⚠ JTBD audience cadres tech non encodé
⚠ Fears audience cadres tech non encodées
⚠ Mechanism diagrams (axe 3) à produire et canoniser

─────────────────────────────────────────────────────────────
DÉCISIONS À TRANCHER
─────────────────────────────────────────────────────────────

1. Lock 4 axes ou révisions ?
   reco → lock all

2. Enrichissements atlas post-batch
   reco → planifier session enrichissement immédiate

─────────────────────────────────────────────────────────────
Légende    ✓ complet    ◐ partiel    ○ vide    ✗ absent    ⚠ critique
─────────────────────────────────────────────────────────────

Étape A6 → gate humain CRITIQUE
Reply "lock all" / "drill axe N" / "révise X"
```

**Note canon** · ce visualiser respecte les 6 standards `output-clarity-doctrine.md` v2.79.2+ · 5 symboles canon uniques · zéro emoji couleur · headers FR sobres · séparateurs ━━━ ─── · density modérée · cap < 80 lignes · légende au pied. Posture matriciel ASCII enforced.

---

## 11. Cross-refs

- `creative-formula.md` v3.1 · équation maître substrate NOYAU × CONTEXTE × MODIFIEURS · CAC pose niveau au-dessus stratégique audience-scoped
- `creative-mechanics-registry.md` · 34+ mécaniques canonisées + typology_st + temporal_subtype NEW v2.88.0 · ref obligatoire par axe créatif
- `hook-formulas.md` · 15 hook patterns instanciables · ref par `creative_axis.hook_pattern_default`
- `output-clarity-doctrine.md` v2.79.2+ · 6 standards visualisers matriciel ASCII · HR-CAC-7 enforcement
- `pre-gate-evaluator-doctrine.md` NEW v2.88.1 · pattern evaluator-optimizer 5 checks structurels · HR-CAC-4 + HR-CAC-5 enforcement
- `pain-benefit-chain-doctrine.md` · 4-layer chain pain → benefit · consommé par axe créatif via lineage angles_ref
- `angle-anatomy-doctrine.md` · formula Obs+Tension+Reframe+Bridge · ref par axe créatif via angles_ref[]
- `hooks-method-doctrine.md` · méthodologie hook · ref par hook_pattern_default
- `breakthrough-advertising-5-stages.md` · awareness stages Schwartz · ref par axe créatif via angle.lineage.awareness_stage
- `voice-doctrine.md` · registre tone canon · enforced via `brand.tone_of_voice` + `audience.voice.key_expressions[]`
- `investigation-posture.md` · 5 sections canon outputs stratégiques · enforced via evaluator-optimizer A6 rapport
- `confidence-propagation.md` · chain confidence cross-entités · enforced via `confidence_chain` hérité fears + dream_scenario_narrative
- `decomposition-visibility-doctrine.md` v2.79.1+ · 4 niveaux matriciels canon · enforced via posture matriciel ASCII visualisers
- `operator-vocabulary-translation.md` v2.79.2+ · mapping 134 entries · HR-CAC-7 enforcement runtime
- `compositional-cartography.md` · architecture 3 couches NOYAU × CONTEXTE × MODIFIEURS · mapping section 4
- `extending.md` + `scope-extension-doctrine.md` · doctrine "extend before create" · respect canon v2.88+ via patches ciblés vs refonte

---

## 12. Position dans système opérationnel 5 couches

Creative Axis Canonicalization Doctrine opère sur 4 des 5 couches du système opérationnel canon (`operational-system-doctrine.md`) ·

**Couche 1 · Principes.** Thèse fondatrice "qualité créative = décomposition fine, pas écriture finale" est principe canon section 1. Pattern miroir `extending.md` (extend before create) · `decomposition-visibility-doctrine.md` (4 niveaux matriciels canon) · `compositional-cartography.md` (architecture 3 couches).

**Couche 2 · Règles (heuristiques décision).** 8 Hard Rules canon strict (HR-CAC-1 à HR-CAC-8) sont heuristiques décision canon · *"si output créatif canon-conforme alors hiérarchie 4 niveaux respectée + lineage canon traçable + atlas profond mobilisé + typology cohérente cross-niveau"* enforcement runtime cross-skills v2.88+. Pattern miroir `output-clarity-doctrine.md` 8 Hard Rules · `decomposition-visibility-doctrine.md` 9 Hard Rules · `investigation-posture.md` 5 sections obligatoires.

**Couche 3 · Templates (raccourcis combinaisons gagnantes).** Hiérarchie 4 niveaux + mapping equation v3.1 + composants axe créatif canon + visualisers Output Clarity-compliant sont templates canon réutilisables cross-skills sous-workflow A. Pattern miroir `creative-formula.md` v3.1 templates · `hook-formulas.md` 15 templates hook · `resources/templates/*` canon templates.

**Couche 5 · Rituels (cadence opérationnelle).** Trigger systémique cross-skills sous-workflow A Creative Strategy (compose-creative-batch · compose-creative v1.9 incarnation_only · learn-from-session mode brief_strategy_intake) enforcement runtime canon. Rituel canon agent par batch créa · validation A3 plan humain · validation A6 axes humain · ship A8 brief strategy actionnable. Pattern miroir `decomposition-visibility-doctrine.md` enforcement runtime cross-slash commands · `engagement-disclosure-doctrine.md` disclosure pré-runtime cross-orchestrateurs.

**Couche 4 · Métriques additionnelle.** % axes créatifs persistés canon-conformes trackable via `learnings.json` append-only · feedback loop A8 → learnings enrichi v2.88.2 patch P9. Métrique convergente · CAC adoption rate cross-batches baseline post-v2.88.2 enforcement runtime · cible 95%+ canon-conforme à 3 mois post-ship.

---

## Status

- **Canonique v2.88.0+.** Codifie hiérarchie créative stratégique 4 niveaux + mapping workflow A v3 ↔ équation v3.1 + mobilisation atlas profond obligatoire + visualisers matriciel ASCII enforcement. Ferme gap systémique session R&D Creative Strategy 25-27 mai 2026 · workflow externe construit from scratch sans accès canon PhantomOS · 65% réinvention vocabulaire détectée · harmonisation canon décidée via 4 cycles débat orchestrateur.
- **Doctrines sœurs** · creative-formula.md v3.1 (équation maître · CAC pose niveau au-dessus) · creative-mechanics-registry.md v2.88.0 (29+ mécaniques + typology_st NEW) · hook-formulas.md v1.0+ (15 patterns) · output-clarity-doctrine.md v2.79.2+ (visualisers matriciel ASCII) · pre-gate-evaluator-doctrine.md NEW v2.88.1 (evaluator-optimizer 5 checks).
- **Backward compat** · strict additif · doctrine NEW n'override aucune existante. Skills pre-v2.88.0 (`compose-creative` v1.8 · `produce-paid-angles` v1.11 · `decompose-ad` v2.2 · `build-atlas-complete` v1.7.1) continuent fonctionner. Migration progressive v2.88+ enforce hiérarchie via `compose-creative-batch` NEW v2.88.2 orchestrator séquentiel.
- **First applications** · Sprint v2.88.0 · profile.schema.json v2.2 (big_idea + fears) · creative-mechanics-registry.md (typology_st + temporal_subtype + mapping initial 34 fiches). Sprint v2.88.1 · pre-gate-evaluator-doctrine.md + creative_axis.schema.json. Sprint v2.88.2 · compose-creative-batch + compose-creative v1.9 incarnation_only + learn-from-session brief_strategy_intake.
- **Test runtime cible** · Stepprs (pilote PhantomOS · atlas mature · permet test end-to-end). Pre-sprint enrichissement Stepprs atlas via `mine-voc` semi-auto sur corpus Trustpilot pour amorcer big_idea + fears. Pas d'encodage opérateur manuel.
- **Promotion criterion** · à reviewer après 5+ batches créa shipped canon-conformes via compose-creative-batch v2.88.2 + 1 audit cross-brand convergence vocabulaire + learnings.json append patterns CAC adoption rate stable 90%+ cross 3+ brands consécutifs.

---

*Doctrine canonique skill-author-facing + agent-facing. Canonise hiérarchie créative stratégique 4 niveaux (brand promise · big idea audience-scoped · axe créatif · créa instance) + mapping workflow A v3 Creative Strategy ↔ équation v3.1 NOYAU × CONTEXTE × MODIFIEURS + mobilisation atlas profond obligatoire 5 dimensions canon (dream_scenario_narrative · jtbd · beliefs · fears · key_expressions) + visualisers matriciel ASCII Output Clarity Doctrine v2.79.2+ enforced + 8 Hard Rules canon strict (HR-CAC-1 à HR-CAC-8) + 6 anti-patterns canonisés. Ferme gap structurel R&D Creative Strategy session externe orchestrée 25-27 mai 2026 via 4 cycles convergence canonisable. Pattern miroir creative-formula.md v3.1 (équation maître) + creative-mechanics-registry.md (mécaniques canon) + output-clarity-doctrine.md (visualisers) + pre-gate-evaluator-doctrine.md NEW v2.88.1 (evaluator-optimizer pattern).*
