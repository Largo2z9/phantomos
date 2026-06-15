# Territory Doctrine · Operating Doctrine

> Canonique v2.67+. Codifie la distinction territoire vs production vs meta canon. Doctrine sœur de SED (Schema Encoding), CMR (Canonical Matrix Reasoning), SAD (Skill Authoring), SED-X (Scope Extension), CC (Compositional Cartography). Unifie trois vocabulaires historiques (Reference · Spatial encoding · Substrat) sous canon nommé unique.

---

## 1. Thesis

> Le PhantomOS workspace opère sur 2 layers temporellement orthogonaux. **Territoire** (substrat stable canonisé · specs + audiences + angles + frictions + roadmap + strategy + learnings · ce qui survit aux sessions). **Production** (livrable runtime on-demand · brief · creative · ad copy decomposition · audit · généré post-territoire). Plus 1 layer transverse · **Meta** (système gestion · validate · capture · scaffold · navigate · build).

Le territoire est CARTOGRAPHIÉ une fois bien posé (investissement Semaine 1 · ~20h opérateur), enrichi marginalement par la suite (1 audience/2 mois · 1 angle/2 semaines en croisière). La production est PRODUITE à la demande, cycle court (5-45 min par brief ou creative), post-territoire mature. La promesse PhantomOS codifie cette asymétrie · *encode métier UNE FOIS · produces N FOIS*.

Ce contrat est cassé si ·
1. Skill production écrit substrat territoire sans operator gate (corrompt cycle promotion canon Section 7)
2. Skill territoire produit livrable runtime opérateur-facing (anti-pattern conceptuel Section 12)
3. Orchestrator chain mixed territoire + production sans hiérarchie de layer dominant (cf build-atlas-complete v1.2.0 anomalie, corrigée v1.3.0)
4. Sync bridge externe push mixed layers dans canvas Notion canon (cf sync-notion-atlas v2.0.0 anomalie, corrigée v2.0.1)

Territory Doctrine codifie classification 67 skills par layer + cycle promotion production validée → territoire + enforcement runtime via frontmatter canon.

---

## 2. Le problème Territory Doctrine résout

Avant doctrine ·

1. **Confusion setup-territoire vs production-livrable.** Opérateur cargo-cult · skills mélangés dans orchestrators (build-atlas-complete v1.2.0 incluait Steps 8-9 production briefs+créas par erreur · corrigé v1.3.0 strip). Cause · pas de discipline layer canon sur skill authoring.

2. **Vocabularies canon scattered.** Trois noms canon historiques distincts pour le même concept · **Reference** (architecture.md §7 Data Nature table 2×4 · canon anglo) · **Spatial encoding** (schema-encoding-doctrine.md §3 · canon technique skill-author) · **Substrat** (session-log S54 + capture FR · canon FR). Aucun unification documentée.

3. **Cycle promotion implicite.** Production testée validée (winning angle ROAS >2.5 30j · winning hook · winning offer mechanic) devrait se cristalliser en territoire enrichi (roadmap.mix · profile.voice · spec.benefits). Mécanisme existait via `learn-from-session` Trigger N + `promote-learning` mais cycle pas doctrinalement nommé.

4. **Notion bridge ambiguity.** `sync-notion-atlas` v2.0.0 push default mixed territoire (10 collections atlas) + production (creatives Full funnel). Anomalie corrigée v2.0.1 (territoire-only default · creatives push deferred). Cause root · pas de doctrine séparation layers Notion-side.

5. **Polysémie macro/micro non disambiguée.** Terme "territoire" utilisé à 2 niveaux dans canon stride-up · macro (substrat brand entière) vs micro (intersection audience×angle output score-matrix). Renommage requis · "top-3 territoires" score-matrix devient "top-3 axes créatifs" pour libérer terme principal.

Territory Doctrine = doctrine canon qui ferme ces gaps.

---

## 3. Définition territoire (layer substrat)

**Le territoire est ce qui survit aux sessions.** Substrat canonisé encodant le métier d'une brand sur la durée.

**Entités canon brand-side** ·
- `brand.json` · identity, positioning, tone, financials, business_model
- `products/{slug}/spec.json` · specs, mécanismes, bénéfices, problèmes, pricing
- `products/{slug}/offers.json` · active offers, bundles, landing pages
- `audiences/{slug}/profile.json` · psychology, pain/benefit chains, objections
- `audiences/{slug}/pain_points/PNT-NN.json` · canonical pain points (v2.64 sub-folder sémantique pure)
- `audiences/{slug}/objections/OBJ-NN.json` · canonical objections
- `angles/ANG-NN.json` · paid angles canonical (formula Obs+Tension+Reframe+Bridge)
- `frictions/FRC-NN.json` · canonical frictions usage
- `roadmap.json` · mix paid + 30/60/90 priorities
- `strategy.json` · annual goals, monthly targets, current focus
- `learnings.json` · append-only learnings cross-session

**Storage path canonical** · `brands/{slug}/` (cf architecture.md §1 brand isolation).

**Volatilité empirique** · trimestrielle à mensuelle. Mature à Mois 4+ croisière (touch marginal).

**30 skills classifiés layer territoire (45% des 67 skills canon)** ·

setup-brand · snapshot-brand · mine-voc · mine-vom · profile-audience · cross-deepening-signals · deepen-brand-context · define-specs · map-mechanisms · map-specs · map-benefits · map-audiences · map-angles · mine-audience · produce-paid-angles · decompose-angle · score-matrix · weight-dimensions · score-product-fit · produce-strategy · study-niche-marketdeepdive · sync-notion-atlas · watch-competitors · cartograph · connect-source · import-asset · ingest-resource · onboard-brand · build-atlas-complete (post-refactor v1.3.0) · propose-schema-draft · produce-paid-matrix

Le territoire est cartographié une fois bien posé. Enrichi marginalement par la suite. Pas re-généré à chaque session.

---

## 4. Définition production (layer livrable runtime)

**La production est ce qui est produit à la demande.** Livrable runtime généré post-territoire, consommable directement par opérateur, cycle court.

**Entités canon brand-side** ·
- `briefs/{id}.md` · briefs créa markdown (composer / matrice canon)
- `creatives/{CRT-NN}.json` · creative builds JSON (compose / decompose / recompose)
- `creatives/{CRT-NN}/adaptations/` · ad copy adaptations par variant
- `audits/{slug}/perf-{date}.md` · audits Meta perf
- `briefs/copy-{id}.md` · briefs copy long-form

**Storage path canonical** · `brands/{slug}/briefs/` + `brands/{slug}/creatives/` + `brands/{slug}/audits/`.

**Volatilité empirique** · hebdomadaire à quotidienne. Cycle 5-45 min par item post-territoire mature.

**18 skills classifiés layer production (27% des 67 skills canon)** ·

produce-copy-brief · compose-creative · recompose-creative · decompose-ad · creative-brief-composer · craft-packshot · compose-overlay-text · audit-meta-account · analyze-copy · brief-day · red-team

La production est produite à la demande post-territoire. Cycle court. Se cristallise en territoire UNIQUEMENT via cycle promotion canon (Section 7), jamais via mutation directe substrat.

---

## 5. Définition meta (layer système)

**Le meta gère le système lui-même.** Ni territoire (substrat brand-side) ni production (livrable runtime opérateur). Système de gestion canonique.

**5 sous-types fonctionnels** ·
- **Validate** (integrity check) · validate-resources · validate-naming · validate-schema-canon · validate-output-coherence
- **Capture** (learnings system-side) · learn-from-session · capture-learning · promote-learning
- **Scaffold** (custom entities + skills) · scaffold-extension · scaffold-entity-files · scaffold-skill-stub
- **Navigate** (session continuity) · resume-session · session-search · export-session · query-context · brief-day (overlap production)
- **Build** (system extensibility) · create-skill · correct-skill · build-agent · check-cross-refs · check-existing-coverage · analyze-extension-intent · register-and-flag · update-workspace · migrate-workspace · encode-batch · connect-mcp-server

**19 skills classifiés layer meta (28% des 67 skills canon)** ·

validate-resources · validate-naming · validate-schema-canon · validate-output-coherence · learn-from-session · capture-learning · scaffold-extension · scaffold-entity-files · scaffold-skill-stub · build-agent · check-cross-refs · check-existing-coverage · analyze-extension-intent · register-and-flag · query-context · resume-session · session-search · export-session · update-workspace · migrate-workspace · promote-learning · correct-skill · create-skill · encode-batch · connect-mcp-server

Storage path canonical · `operator/` + `.skills/` + `resources/canon/` (transverse, pas brand-side).

---

## 6. Synonymes canon historiques

Trois vocabularies canon historiques distincts désignaient le même concept territoire. Territory Doctrine unifie sous canon v2.67+ sans casser backward compat (Section 13 amendment protocol).

| Canon historique | Source | Scope | Mapping v2.67+ |
|---|---|---|---|
| **Reference** (Reference vs Production) | `architecture.md §7 Data Nature` (table 2×4 existing) | Anglo skill-author | = **territoire** |
| **Spatial encoding** (Spatial vs Temporal) | `schema-encoding-doctrine.md §3` (pattern technique) | Technique skill-author | = **territoire** |
| **Substrat** | `session-log.md S54` (capture FR) | FR opérateur + skill-author | = **territoire** |
| **Production** (Reference vs Production) | `architecture.md §7` + `canonical-matrix-reasoning.md` | Stable cross-canon | = **production** (préservé) |
| **Temporal encoding** | `schema-encoding-doctrine.md §3` | Technique skill-author | englobe **production + meta** (split v2.67+) |

Sourcing verbatim `architecture.md §7 Data Nature` (à citer dans skill docstrings v2.67+) · *"Reference data (specs, audiences, angles, learnings) is canonical substrate. Production data (briefs, creatives, audits) is runtime output."*

Sourcing verbatim `schema-encoding-doctrine.md §3` · *"Spatial encoding captures persistent entities (the workspace shape). Temporal encoding captures events (the workspace history)."* Territory Doctrine raffine · Temporal split en Production (runtime livrable) + Meta (système).

Doctrine v2.67+ canon · **territoire / production / meta** trio. Synonymes historiques préservés via Section 6 (zero breaking change).

---

## 7. Cycle promotion · production validée → territoire enrichi

**Pattern canon doctrine.** Production runtime testée + validée se cristallise en territoire substrat. Mécanisme codifié.

**Validation status canon** (cf `_shared/validation-status.json`) · `hypothesis` → `validated` → `scaled`.

**Triggers cycle promotion** ·

| Trigger | Mécanisme | Skill canonical | Substrat enrichi |
|---|---|---|---|
| Winning angle testé 30j ROAS >2.5 | Capture pattern · cristallisation | `learn-from-session` Trigger N + `promote-learning` | `roadmap.mix` (angle promoted) + `learnings.json` append |
| Winning hook testé 50K imps CTR >1.8% | Capture verbatim hook | `promote-learning` | `audiences/{slug}/profile.voice.canonical_hooks[]` append |
| Winning offer mechanic testé multi-creative | Capture mechanic | `promote-learning` | `products/{slug}/spec.benefits[]` enriched |
| Winning copy hook validé cross-brand (N≥3 brands) | Promotion cross-brand canon | `promote-learning` + canon-tool v1.1 | `resources/canon/copy/` shared |

**Pattern référence** · `compositional-cartography.md` cycle produce → test → learn → promote codifie cette boucle au niveau créatif. Territory Doctrine généralise au niveau substrat workspace entier.

**Anti-pattern · mutation directe.** Skill production qui écrit substrat territoire sans cycle promotion = violation thesis Section 1. Bypass validation. Corrompt audit trail (mutation gate `proposed` mode skipping). Refusé canon.

Pattern canon · production reste production (livrable runtime · scope brand · cycle court) jusqu'à validation explicite + promotion gate operator. Alors et seulement alors substrat enrichi.

---

## 8. Pattern usage opérateur

Pattern empirique observé pilots (Stride-Up · we-bet · etc.) · investissement asymétrique territoire vs production.

**Semaine 1 · territoire setup intensif (~20h opérateur)** ·

```
Day 1 · onboard-brand → snapshot-brand (~3h)
Day 2-3 · mine-voc (5 audiences × 30 min mining) + mine-vom (~5h)
Day 4-5 · profile-audience × N audiences + map-audiences (~6h)
Day 6 · produce-paid-angles + score-matrix → top axes créatifs (~3h)
Day 7 · review · stage acceptations · validation_status promotions (~3h)
```

Sortie · territoire mature suffisant pour production. `wedge_complete: true` dans `status.json`.

**Semaines 2-24 · production cycle court (5-45 min par item)** ·

Le territoire ne bouge pas. Production rythme daily ·
- 1 brief / jour · `produce-copy-brief` ou `creative-brief-composer` (10-15 min)
- 2-3 creatives / semaine · `compose-creative` ou `recompose-creative` (15-30 min)
- 1-2 audit perf / semaine · `audit-meta-account` (20-30 min)
- 1 decompose-ad concurrent / semaine · `decompose-ad` (10-15 min)

**Mois 2-3 · enrichissements territoire rares** ·
- 1 audience / 2 mois (NEW audience post-mining via Pattern 3 SED-X)
- 1 angle / 2 semaines (NEW angle post-validation cycle promotion Section 7)
- 2 frictions / mois (NEW friction post-VoC mining)

**Mois 4+ croisière** ·
- Territoire mature · touch mensuel marginal
- Production rythme daily · 5-15 items / semaine

**Codification promesse PhantomOS** · *encode métier UNE FOIS · produces N FOIS*. Le pattern usage code cette asymétrie canon.

---

## 9. Skill layer enforcement

**Frontmatter NEW canon v2.67+** · chaque SKILL.md déclare `layer: territoire | production | meta`.

```yaml
---
name: produce-paid-angles
type: producer
layer: territoire
recommended_model: claude-sonnet-4-6
subagent_safe: true
---
```

**Enforcement runtime** ·
- `validate-resources` refuse SKILL.md missing ou invalid `layer` field (canon v2.67+ strict)
- Manifest expose `layer` field pour discoverability + routing canon
- Mutation gate respecte hiérarchie · skill `layer: production` peut pas écrire territoire substrat sans operator gate explicit (cf Anti-pattern Section 12.2)
- Manifest regen post-add via `build-manifest.py` (cf SED-X §4.1)

**Backward compat** · skills pré-v2.67 sans field `layer` flag à patcher (sprint dédié migration). Aucun break runtime · validate-resources warning level (pas refuse) jusqu'à v2.70.

**Mutation gate hiérarchie** ·
- `layer: territoire` skills peuvent muter `brands/{slug}/*.json` via mutation gate proposed mode
- `layer: production` skills peuvent écrire `brands/{slug}/briefs/` + `brands/{slug}/creatives/` + `brands/{slug}/audits/` directly (production output non-substrat)
- `layer: meta` skills peuvent muter `operator/` + `.skills/` + `resources/canon/`
- Cross-layer mutation = operator gate explicit (production → territoire via cycle promotion Section 7 uniquement)

---

## 10. Notion bridge implication

**11 collections canon stride-up bridge Notion** · mapping clarifié post-Territory Doctrine.

**10 collections layer territoire (push default)** ·
1. Produits (brand.json + spec.json)
2. Specs (spec.json composition)
3. Mécanismes (spec.mechanism)
4. Bénéfices (spec.benefits)
5. Personae (profile.json)
6. Pain Points (pain_points/PNT-NN.json)
7. Angles (angles/ANG-NN.json)
8. Objections (objections/OBJ-NN.json)
9. Frictions usage (frictions/FRC-NN.json)
10. Roadmap (roadmap.json)

**1 collection layer production** ·
11. Full funnel Meta (creatives + ad copy adaptations)

**Skill `sync-notion-atlas` v2.0.1+ default push = 10 collections territoire strict.** Creatives push deferred via NEW skill dédié `sync-creatives-to-notion` v2.68+ (cards/Kanban Notion pour briefs + créas par angle · production layer séparée).

**Pattern canon · 1 skill par layer Notion-side.** Cohérent avec Territory Doctrine thesis. Pattern reproductible cross-tools · bridge externe respecte séparation layers.

**Anomalie corrigée** · `sync-notion-atlas` v2.0.0 push mixed (10 territoire + 1 production) = violation layer separation. Patch v2.0.1 strip Step Full funnel Meta. NEW skill v2.68+ couvre production layer dédié.

---

## 11. Decision-aid Q1-Q4 pour skill authors

Avant d'ajouter NEW skill, applique ce decision-aid pour classifier layer canon ·

```
Q1 · Le skill écrit-il un JSON canon brand-side qui survit aux sessions ?
   (brand.json · spec.json · profile.json · angle.json · friction.json · roadmap.json · learnings.json · strategy.json)
   OUI → layer territoire
   NON → Q2

Q2 · Le skill produit-il un livrable runtime (markdown brief · JSON creative · audit doc) consommable directement par opérateur ?
   (briefs/{id}.md · creatives/{CRT-NN}.json · audits/{slug}/*.md)
   OUI → layer production
   NON → Q3

Q3 · Le skill gère-t-il le système (validate · capture · scaffold · navigate · build) ?
   (validate-resources · learn-from-session · scaffold-extension · resume-session · create-skill · etc.)
   OUI → layer meta
   NON → Q4

Q4 · Le skill orchestrateur chain plusieurs sub-skills layers différents ?
   OUI → layer dominant ·
     - Orchestrator chain N territoire + M production (production = downstream optionnel) → layer territoire
     - Orchestrator chain principalement production (territoire = read prerequisite only) → layer production
     - Orchestrator chain principalement meta → layer meta
   NON → flag à doctrine maintainers pour évaluation (cas non couvert · candidat sprint dédié)
```

**Tie-breaker overlap.** Si Q1-Q3 ambiguous (e.g. skill `brief-day` produit livrable runtime mais lecture-only sur substrat) → règle `output type` prime · output principal = livrable runtime = layer production. Cas brief-day classified production (cf Section 4).

---

## 12. Anti-patterns

### Anti-pattern 1 · Orchestrator mixed sans layer dominant

`build-atlas-complete v1.2.0` incluait Steps 8-9 production briefs+créas dans pipeline territoire setup. Violation séparation layers (territoire setup orchestrator doit produire territoire mature, pas production runtime). Patch v1.3.0 strip Steps 8-9. Production runtime générée via skills production dédiés post-territoire mature.

**Pattern canon** · orchestrator territoire chain skills territoire uniquement (cartographie). Orchestrator production chain skills production uniquement (composition livrable). Orchestrator meta chain skills meta uniquement (système).

### Anti-pattern 2 · Skill production écrit substrat directement

Skill `compose-creative` ou `produce-copy-brief` qui mute `audiences/{slug}/profile.json` directly sans cycle promotion canon (Section 7) = violation thesis Section 1. Corrompt audit trail. Bypass validation.

**Pattern canon** · production reste production jusqu'à validation explicite + promotion gate operator. Cristallisation territoire uniquement via `promote-learning` skill canonical.

### Anti-pattern 3 · Skill territoire produit livrable runtime

Skill `produce-paid-angles` (layer territoire) qui produirait un brief copy markdown opérateur-facing directement = violation conceptuelle. Le skill territoire enrichit substrat (angles/ANG-NN.json), il ne produit pas le livrable runtime consumable.

**Pattern canon** · territoire enrichit substrat (output JSON canonical brand-side). Production consume substrat + produit livrable runtime opérateur-facing. Boundary strict.

### Anti-pattern 4 · Doctrine name "Reference" anglo dans output opérateur-facing

Output opérateur-facing utilisant terme "Reference" (canon anglo historique architecture.md §7) au lieu de "territoire" (canon FR v2.67+) = violation accessibility CLAUDE.md root rule absolue (*"never expose doctrine names"*).

**Pattern canon** · operator-facing use "territoire" FR. Skill-author canon docs use "territoire" (canon principal v2.67+) avec mention synonymes historiques (Section 6) pour backward navigation.

### Anti-pattern 5 · Polysémie territoire macro vs micro non disambiguée

Terme "territoire" était utilisé à 2 niveaux dans canon stride-up · macro (substrat brand entière) vs micro (intersection audience×angle output score-matrix). Confusion mental model.

**Pattern canon v2.67+** · "territoire" reservé au sens macro (substrat brand). Output score-matrix renommé "top-3 axes créatifs" pour libérer terme principal. Lexicon canon `lexicon.md` capture cette distinction (cf cross-refs Section 13).

### Anti-pattern 6 · Mix layers dans canvas Notion push default

`sync-notion-atlas v2.0.0` push mixed (10 collections territoire + 1 collection production Full funnel Meta) = violation layer separation Notion-side. Patch v2.0.1 strip production. NEW skill `sync-creatives-to-notion` v2.68+ couvre production layer dédié.

**Pattern canon** · bridge externe respecte Territory Doctrine · 1 skill par layer push. Pattern reproductible cross-tools (Linear · ClickUp · Airtable · etc.).

---

## Position dans le système opérationnel 5 couches

Le territoire de marque (substrat stable canonisé) est l'objet structurel
de la couche 1 (modèle) du système opérationnel PhantomOS (cf
`operational-system-doctrine.md`). C'est le résultat tangible de
l'application de l'ECR à un brand.

La distinction territoire / production runtime est une conséquence directe
de l'équation maître multiplicative · le territoire = stable (modèle +
règles + templates) · la production = volatile (combine les 5 couches
en livrable à la demande).

---

## 13. Cross-references

- `architecture.md §7 Data Nature` · Reference vs Production · table 2×4 historique anglo (synonyme territoire/production canon v2.67+ Section 6)
- `schema-encoding-doctrine.md §3` · Spatial encoding vs Temporal encoding · pattern technique skill-author (synonyme territoire vs production+meta canon v2.67+)
- `compositional-cartography.md` · cycle produce → test → learn → promote · pattern référence cycle promotion Section 7 niveau créatif
- `canonical-matrix-reasoning.md` (CMR) · production skills 95% quality · doctrine sœur production layer canon
- `scope-extension-doctrine.md` (SED-X v2.65) · sister doctrine · pattern miroir 13 sections canon-style
- `investigation-posture.md` · 5 sections close synthesis · pattern enforcement skills production output
- `lexicon.md` · **Territoire** (sens macro v2.67+) + **Axe créatif** (intersection audience×angle · renommé score-matrix output v2.67+ pour disambiguation polysémie)
- `skill-authoring-doctrine.md` (SAD) · skill type taxonomy · frontmatter triad (+ NEW field `layer` canon v2.67+)
- `doctrine-governance.md` · amendment process append-only D# verrouillé · cross-refs traçables
- `contextual-intelligence.md` (CI) · master doctrine · agent reasons not form-fills
- `provenance-trust-discipline-scope.md` (PTD scope) · multi-operator canon-as-product

**Skill authors patches v2.67+** ·
- `build-atlas-complete v1.3.0` · Steps 8-9 stripped (territoire setup only · pas production)
- `sync-notion-atlas v2.0.1` · territoire-only default push (10 collections atlas strict)
- NEW frontmatter `layer` field 67 SKILL.md (territoire 30 · production 18 · meta 19)
- `score-matrix` output renaming · "top-3 territoires" → "top-3 axes créatifs" (lexicon canon)

**Future v2.68+** ·
- NEW skill `sync-creatives-to-notion` · production layer Notion · cards/Kanban briefs+créas par angle
- Pattern reproductible · 1 skill par layer bridge externe (cross-tools Linear/Airtable/etc.)

---

## Status

- **Canonique v2.67+.** Doctrine sœur SED · CMR · SAD · SED-X · CC · CI.
- **First applications** · classification 67 skills validée (territoire 30 · production 18 · meta 19). Build-atlas-complete v1.3.0 + sync-notion-atlas v2.0.1 + frontmatter layer canon v2.67+ ship sprint dédié.
- **Backward compat** · strict additif · doctrine NEW n'override aucune existing. Synonymes historiques (Reference · Spatial encoding · Substrat) préservés via Section 6 mapping.
- **Promotion criterion** · à reviewer après 3+ NEW skills shipped avec frontmatter `layer` canon (validate-resources warning → refuse v2.70).

---

*Doctrine canonique skill-author-facing. Codifie territoire vs production vs meta layers canon. Unifie 3 vocabularies historiques. Enforce frontmatter layer field v2.67+. Pattern miroir SED-X 13 sections.*
