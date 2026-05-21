---
name: profile-audience
version: 1.9.0
patch_notes:
  - "1.9.0 (v2.87.4 deep desire chain gate canon) · NEW Hard Rule HR-DD-1 · gate obligatoire pre-validation audience · psychology.dream_scenario_narrative (object · narrative 2 phrases + target_recipient + context_setting + social_payoff) + psychology.confidence_chain (object · sourcing_method enum + verbatim_count + blocked_sources + confidence_level + caveat) DOIVENT être populated AVANT write profile.json validation_status='validated'. Refuse anti-pattern systémique audit Fincut v2.87.3 · audience encoding reste au pain layer fonctionnel sans descente racine Schwartz/Kern (e.g. 'valoriser corps' sans target_recipient='plaire partenaires/pairs/etc.'). Profile schema v2.0 → v2.1 (psychology.dream_scenario_narrative + psychology.confidence_chain NEW). Backward compat strict additif lecture v2.0 préservée. Cross-ref `docs/system/investigation-posture.md` v2.79.3+ (confidence chain canon) + `docs/system/territory-doctrine.md` (substrate stable psychographique). Anti-pattern · rendre profile.json sans dream_scenario_narrative.target_recipient explicite = refuse gate."
  - "1.8.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section `Niveau LIVE · raisonnement thinking aloud pendant exécution` insérée APRÈS HR0ter disclosure NIVEAU 0 v2.79.5 et AVANT Step 0bis prerequisite check. Action LOURDE classification (synthèse audience 8 dimensions canon V3 · cross-validation Schwartz double-stage · staging pain_points + objections sub-audience canonical · ~8 min selon densité mining). NIVEAU LIVE narratif étendu obligatoire pendant exécution · 2 niveaux abstraction obligatoires (macro contexte audience sub-cluster + micro pain-benefit-chain phrasé en prose narrative sobre). Pose pair senior expert thinking aloud · audit temps réel par l'opérateur entre dimensions encodées + pédagogie posture experte indissociables. Cross-ref `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid). Backward compat strict additif · cycle runtime préservé (HR0ter NIVEAU 0 + Step 0bis-0ter + 8 dimensions encoding + Audience Visibility Matriciel post-exec preserved)."
  - "1.8.0 (v2.79.5 decomposition visibility NIVEAU 0) · NEW section `Engagement disclosure pré-runtime v2.79.5+` AVANT Step 0bis prerequisite check · 6 paramètres décomposés contextualisés (Audience source · Dimensions cartographier · Sources data · Granularité output · Hypothèses figées · Biais à éviter · POURQUOI explicit chacun · raisonnement métier expert visible AVANT synthèse). Exemple concret canonisé in-line. ATTENDS confirmation explicite paramètres AVANT lancement profile synthesis. HR0ter canon ajouté. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` OR `--no-disclosure` explicit. Cross-ref `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ NIVEAU 0 + `docs/system/engagement-disclosure-doctrine.md` v2.79.5 Paramètres décomposés. Backward compat strict additif · cycle runtime préservé."
  - "1.7.0 (v2.78.2 decomposition visibility) · NEW Output section `Audience Visibility Matriciel` après encoding 8 dimensions canon V3 · matrice ASCII audience × pain × angle obligatoire si ≥2 pains owned sub-audience · stage business filter (early / growth / scale) si signal détectable · méthode pédagogique verbale explicit (8 dimensions résumées + many-to-many audience-pain-angle). HR10-HR14 + AP10-AP13 ajoutés. Backward compat strict additif · existing 8 dimensions + 5 sections IP preserved · operator output template v2.54 preserved (template legacy reste valide, NEW section l'enrichit). Cross-ref `docs/system/decomposition-visibility-doctrine.md` v2.78.2 (canon racine sister Sprint A)."
  - "1.2.0 · v2.39+ · Step 0ter framework awareness (4 questions cartography pédagogie inline)"
  - "1.3.0 · v2.54 investigation posture refactor surface · audiences présentées comme hypothèses avec confidence chain explicite (TRÈS faible par défaut sans mine-voc · faible 1-2 indicateurs site · moyenne mine-voc partiel · forte mine-voc + analytics convergents). Operator output template HR6 + HR8 restructurés · chaque audience porte hypothèse / confidence / indicateurs sources / validation requise / anti-pattern à respecter. Skill termine sur close drill-down macro · lancer mine-voc maintenant vs valider intuitivement et continuer. Préserve mécanismes 8 dimensions Schwartz double-stage problem_map. Refacto uniquement la posture surface · présentation comme hypothèse vs persona analytique. Cross-ref docs/system/investigation-posture.md."
  - "1.3.1 · v2.55 audit consume canon matrices · consumes: enrichi (archetypes-voix, heuristiques-persuasion, creative-formula.md) + HR0bis NEW Load canon matrices force lecture batch via phantom-canon.py + cross-product canon × audience obligatoire en HR3 Dimensions 1/6/7 (canon_ref cité Layer A trace + profile.json#lineage). Aligne déclaration consumes: avec ce que les Steps lisent réellement. Anti-pattern banni · halluciner archetype ou biais audience-side sans mapping canon. Master doctrine ré-activé · PhantomOS reasons over a business universe, canon dormant = output générique averaged-LLM."
  - "1.4.0 (v2.58 coverage extend) · role.type derivation depuis buyer_user_split · objections.severity_score synthesis · behavior.* sub-fields VoC-anchored. Closes 3 orphans audit v2.57."
  - "1.4.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (audiences-cartography, objections-mapping, pain-benefit-chain, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts."
  - "1.5.0 (v2.63 ontologie pure) · BREAKING refactor pain_points + objections passent en COLLECTIONS TOP-LEVEL séparées · stage `brands/{slug}/pain_points/{PNT-NN}.json#chain.surface/consequence/deep` + `brands/{slug}/objections/{OBJ-NN}.json#severity_score` au lieu de sub-fields profile.json legacy. Read pain + objection désormais depuis collections (scan `brands/{slug}/pain_points/*.json` + `brands/{slug}/objections/*.json` filtré par affected_audiences contains audience_slug). Profile schema v2.0 BREAKING · sub-fields legacy DEPRECATED write · read fallback preserved pour brownfield v1.7."
  - "1.6.0 (v2.64 ontologie sémantique pure) · pain_points + objections passent en SUB-AUDIENCE · stage `brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json#chain.surface/consequence/deep` + `brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json#severity_score` (owned natif par parent path). Read désormais depuis sub-audience direct (scan `brands/{slug}/audiences/{a_slug}/pain_points/*.json` + `brands/{slug}/audiences/{a_slug}/objections/*.json` sans filter affected_audiences nécessaire · l'audience parente est implicite). Backward compat strict additif · lecture fallback transparent top-level v2.63 `pain_points/*.json` + `objections/*.json` filtrés par affected_audiences si sub-audience vide OR absente. profile sub-fields legacy v1.7 read fallback aussi preserved."
type: orchestrator
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
description: |
  v1.8.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution (entre HR0ter NIVEAU 0 disclosure v2.79.5 et Step 0bis prerequisite check). Action LOURDE · narratif étendu 2 niveaux abstraction (macro contexte audience sub-cluster + micro pain-benefit-chain phrasé surface → consequence → deep + 3 couches bénéfice). Pose pair senior expert · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  v1.8.0 (v2.79.5 decomposition visibility NIVEAU 0) · NEW section "Engagement disclosure pré-runtime v2.79.5+" AVANT Step 0bis · 6 paramètres décomposés (Audience source · Dimensions cartographier · Sources data · Granularité output · Hypothèses figées · Biais à éviter · POURQUOI chaque) · raisonnement métier expert visible AVANT synthèse profile. ATTENDS confirmation paramètres AVANT lancement. HR0ter canon. Cross-ref `decomposition-visibility-doctrine.md` v2.79.5+ + `engagement-disclosure-doctrine.md` v2.79.5.
  v1.7.0 (v2.78.2 decomposition visibility) · NEW Output section `Audience Visibility Matriciel` après encoding 8 dimensions canon V3 · matrice ASCII audience × pain × angle si ≥2 pains owned · stage business filter (early/growth/scale) · méthode pédagogique verbale (8 dimensions résumées + many-to-many). Backward compat strict additif.
  v1.6.0 (v2.64 ontologie sémantique pure) · pain_points + objections passent en SUB-AUDIENCE · stage `brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json` + `brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json` (owned natif par parent path). Read désormais depuis sub-audience direct (pas de filter affected_audiences[] nécessaire · l'audience parente est implicite). Backward compat strict additif · lecture fallback top-level v2.63 collections + profile sub-fields legacy v1.7 preserved.
  v1.5.0 (v2.63 ontologie pure) · BREAKING refactor pain_points + objections passent en COLLECTIONS TOP-LEVEL séparées · stage `brands/{slug}/pain_points/{PNT-NN}.json` + `brands/{slug}/objections/{OBJ-NN}.json` au lieu de sub-fields profile.json legacy. Read désormais depuis collections (scan filtré par affected_audiences contains audience_slug). Profile schema v2.0 BREAKING · sub-fields legacy DEPRECATED write · read fallback preserved.
  v1.4.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (audiences-cartography, objections-mapping, pain-benefit-chain, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.4.0 (v2.58 coverage extend) · role.type derivation depuis buyer_user_split · objections.severity_score synthesis · behavior.* sub-fields VoC-anchored. Closes 3 orphans audit v2.57.
  Synthétise les outputs de mining (voc/vom/audience) en profil audience structuré 8 dimensions canon V3. Consume verbatims raw, produit profile.json conforme schema v1.3 avec validation gate operator. Ne mine pas, synthétise.
triggers_fr:
  - "profil audience"
  - "synthétise l'audience"
  - "8 dimensions audience"
  - "structure audience"
  - "cartographie sub-cluster"
triggers_en:
  - "profile audience"
  - "synthesize audience"
  - "8 dimensions"
  - "structure audience"
  - "map sub-cluster"
disambiguates_against:
  - mine-voc: "mine-voc capture verbatims clients (raw signals). profile-audience SYNTHÉTISE ces signals en profil 8-dim structuré."
  - mine-vom: "mine-vom capture vernaculaire marché. profile-audience consume les outputs des mining skills."
  - mine-audience: "mine-audience découvre des sub-clusters candidats. profile-audience structure un sub-cluster spécifique en 8 dimensions."
  - cartograph: "cartograph est READ-ONLY synthèse strategique. profile-audience WRITE (peuple profile.json)."
consumes:
  - brands/{slug}/audiences/_voc/* (mine-voc outputs)
  - brands/{slug}/audiences/_vom/* (mine-vom outputs)
  - brands/{slug}/audiences/{audience}/raw/* (mine-audience outputs)
  - resources/schemas/profile.schema.json (target)
  - resources/canon/copy/niveaux-schwartz/* (awareness stages reference · Schwartz double-stage Step Q3 + HR4)
  - resources/canon/copy/archetypes-voix/* (voix archetype matrice canon · cross-pollination identité audience HR3 Dimension 7)
  - resources/canon/copy/heuristiques-persuasion/* (biais cognitifs canon · informe purchase_driver HR3 Dimension 1 + objections psychology)
  - resources/canon/copy/creative-formula.md (8 dimensions canon V3 · contrat HR3)
  - path: docs/doctrine/audiences-cartography-doctrine.md
  - path: docs/doctrine/objections-mapping-doctrine.md
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/system/decomposition-visibility-doctrine.md
  - path: docs/system/pain-benefit-chain.md
  - path: docs/system/investigation-posture.md
  - path: docs/system/audience-cartography.md
produces_validations_for: []
produces_proposals_for:
  - brands/{slug}/audiences/{audience_slug}/profile.json
  - brands/{slug}/audiences/{audience_slug}/pain_points/{PNT-NN}.json
  - brands/{slug}/audiences/{audience_slug}/objections/{OBJ-NN}.json
  - brands/{slug}/pain_points/{PNT-NN}.json (legacy v2.63 backward compat read · DEPRECATED write)
  - brands/{slug}/objections/{OBJ-NN}.json (legacy v2.63 backward compat read · DEPRECATED write)
  - brands/{slug}/audiences/{audience_slug}/profile.json#/pain_points (legacy v1.7 backward compat read · DEPRECATED write)
  - brands/{slug}/audiences/{audience_slug}/profile.json#/objections (legacy v1.7 backward compat read · DEPRECATED write)
permissions:
  reads: [brands/, resources/]
  writes: [brands/{slug}/audiences/{slug}/profile.json via write_to_context]
  emits_events: [profile_proposal_created, profile_validated]
pipeline:
  preconditions:
    - "mine-voc OR mine-vom OR mine-audience a tourné"
    - "audience_slug défini"
  postconditions:
    - "profile.json conforme profile.schema v1.3"
    - "8 dimensions populated"
    - "operator validation gate passed"
prerequisites:
  - field: audiences/{slug}/profile.json
    level: L1
    auto_pull: brownfield_seed_read
    freshness_ttl_days: 90
  - field: audiences/{slug}/mining-outputs/
    level: L1
    auto_pull: read_mining_outputs
    freshness_ttl_days: 60
  - field: audiences/{slug}/verbatim_density
    threshold: 3
    level: L3
    fallback: infer_from_canon_archetype
    confidence_default: 0.5
  - field: resources/canon/copy/archetypes-voix
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
---

# profile-audience

Synthétise un sub-cluster d'audience en profil 8 dimensions canon V3. Consume les outputs de mining et produit `profile.json` conforme `profile.schema v1.3`. Operator-facing avec validation gate avant write.

## Hard Rules

### HR-DD-1 · Deep desire chain gate canon v2.87.4 (obligatoire pre-validation)

Avant tout write profile.json avec `meta.validation_status: "validated"`, l'agent DOIT avoir populé deux objets canon v2.87.4 dans psychology ·

**psychology.dream_scenario_narrative** · object 3 fields required ·
- `narrative` · 2 phrases concrètes scénarisant le moment dream outcome (setting + qui voit + réaction + payoff). Exemple Fincut gym-muscle-showcase canon · *"Lundi matin réunion bureau, je rentre dans la salle, 3 collègues remarquent que je me porte différemment cette semaine. Une nouvelle collègue me regarde 2 secondes de trop. Je n'ai rien eu à dire."* Anti-pattern refusé · *"Je me sens bien tout le temps"* (abstraction sans contexte ni récompense).
- `target_recipient` · pour qui le résultat est joué · cible relationnelle du payoff (partenaires sexuels/romantiques · pairs masculins · collègues professionnels · famille · soi-même au miroir · enfants observateurs · etc.). Champ qui force la sortie du fonctionnel pure vers le social/relationnel. **Sans target_recipient explicite, le gate refuse.**
- `context_setting` · contexte spatial+temporel concret (rencontre amoureuse · bureau lundi · vacances en couple · sport club · etc.). Anti-pattern · `every day` / `all contexts` / `au quotidien` refuse le gate (trop abstrait pour générer un angle paid scroll-stop).

**psychology.confidence_chain** · object 2 fields required ·
- `sourcing_method` enum · verbatim_direct | derived_indirect | inferred_no_source | mixed. Tracer honnêtement la provenance épistémique.
- `confidence_level` enum · forte | moyenne | faible | TRÈS_faible (canon investigation-posture v2.79.3+). Surfaçage obligatoire opérateur dans validation_status._note + audience drill rendu.

**Pourquoi ce gate (rationale canon)** · audit Fincut session v2.87.3 a confirmé pattern systémique · les 3 audiences encodées (gym-muscle-showcase · morpho-atypique-fit · extended-sizing-xl-4xl) sont restées au pain layer fonctionnel ("valoriser corps", "fit morphologique") SANS descendre au pourquoi racine (plaire aux femmes · dominance sociale subtile · réassurance anti-régression · permission soigner sans féminiser · récompense mérite physique). Impact opérationnel · angles paid générés downstream restent product-centric (même registre que paid actuel qui chute -37%) plutôt que persona-centric scroll-stop. Le gate force la descente AVANT validation pour empêcher cette dérive.

**Anti-patterns explicites refusés** ·
- Rendre profile.json sans `dream_scenario_narrative.target_recipient` explicite
- `target_recipient: "soi-même"` seul (acceptable seulement combiné avec autre cible relationnelle)
- `context_setting` abstrait ("every day", "au quotidien", "in life")
- `confidence_chain.sourcing_method: "verbatim_direct"` sans `verbatim_count` ≥ 5
- Skip gate avec `_skip_gate: true` (interdit canon)

**Cross-ref doctrines** · `investigation-posture.md` v2.79.3+ (confidence chain canon) · `territory-doctrine.md` (substrate stable psychographique) · `compositional-cartography.md` (NOYAU × CONTEXTE × MODIFIEURS · dream_scenario_narrative alimente le NOYAU narrative copy downstream).

### HR0ter · Engagement disclosure pré-runtime · canon v2.79.5+ (NIVEAU 0 paramètres décomposés)

Avant Step 0bis (prerequisite check) et Step 0ter (framework awareness), expose disclosure ENRICHI à l'opérateur (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.5 Paramètres décomposés + `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ NIVEAU 0 pré-exec). Le disclosure v2.79.5 expose NIVEAU 0 paramètres décomposés AVANT la synthèse · l'agent contextualise sur la brand + audience encoded · 6 paramètres opérationnels + raisonnement métier expert visible (POURQUOI chaque choix). L'opérateur valide ou ajuste les paramètres AVANT que l'agent consomme tokens synthesis.

#### Format canonique disclosure v2.79.5+ enrichi

```
Synthèse profil audience · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Paramètres posés · ce sur quoi je pars
  ─────────────────────────────────────────────────────────────────────
  Audience source       {segments atlas brand} · POURQUOI ce focus
  Dimensions cartograph. {pyramide Maslow · Schwartz · Cialdini}
                        POURQUOI ces dimensions
  Sources data          {brand encoded + first-party + verbatims}
                        POURQUOI cet ordre
  Granularité output    {parents/enfants · N audiences} · POURQUOI
  Hypothèses figées     {âge · canal · psychographie présumés}
  Biais à éviter        {over-segmentation · stéréotype démographique}

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Prerequisite check (brownfield seed · mining outputs · canon)
  2. Framework cartography 4 questions (Q1 porte d'entrée surface)
  3. Load canon matrices (Schwartz · archetypes · biais)
  4. Synthesize 8 dimensions canon V3
  5. Cross-validate Schwartz double-stage
  6. Stage pain_points + objections sub-audience canonical
  7. Surface draft profile en posture hypothèse (confidence chain)
  8. Audience Visibility Matriciel (matrice × pain × angle)
  9. Operator validation gate → write_to_context

  ETA           ~5-12 min (selon densité mining + brownfield seed)
  Implication   tu valides paramètres d'abord · puis tu valides synthèse
  Livrable      profile.json 8 dimensions + sub-audience pain_points/objections
                + matrice visibility + close drill-down macro

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

#### Pattern obligatoire NIVEAU 0

L'agent expose **6 paramètres décomposés contextualisés** sur la brand + audience cible (lecture `brand.json` + `audiences/*/profile.json` brownfield seed + mining outputs upstream). Pour chaque paramètre, **POURQUOI explicit** (raisonnement métier expert visible · pas implicite). L'opérateur voit le raisonnement avant la synthèse · il peut ajuster avant la consommation de tokens.

1. **Audience source** · segments atlas brand visés (depuis `brand.json#audiences` + `audiences/*/profile.json` encoded · scope sub-cluster cible). POURQUOI ce focus · positioning brand + densité signal mining disponible.
2. **Dimensions cartographier** · pyramide Maslow (besoins) · sophistication Schwartz (1-5) · awareness stage Cialdini / Schwartz 5 stades · 8 dimensions canon V3. POURQUOI ces dimensions · canon copywriting + audience-cartography doctrine + decomposition-visibility v2.78.2 matrice many-to-many.
3. **Sources data** · ordre · (1) brand encoded · (2) first-party (Klaviyo · Shopify · NPS · transcripts SAV) · (3) verbatims VoC / VoM mining si présents · (4) canon matrices (archetypes-voix · heuristiques-persuasion). POURQUOI cet ordre · brand-truth d'abord · first-party densité × biais minimal · third-party validation · canon pour cross-pollination identité.
4. **Granularité output** · parents / enfants · combien d'audiences distinctes · sub-clusters · enfants ENUM `[broad | segment | micro]`. POURQUOI cette granularité · signal volume_remaining + pitch_divergent + offer_divergent (framework cartography 4 questions Q2).
5. **Hypothèses figées** · ce que l'agent présume SANS valider (âge dominant inféré · canal d'acquisition supposé · psychographie projetée · trigger event supposé). L'opérateur sait ce qui n'est pas vérifié verbatim.
6. **Biais à éviter** · risk flags · over-segmentation (créer micro-audience sans volume remaining justifié) · stéréotype démographique ("femme 35 donc mobile") · projection persona-marketing analytique (anti-pattern AP-2 doctrine investigation-posture · personas inventés sans data verbatim).

#### Exemple concret canonisé · profile-audience sur Liv Happyfood audience-hero (femmes 30-45 minceur clean)

```
Synthèse profil audience · Liv Happyfood · audience-hero · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Paramètres posés · ce sur quoi je pars
  ─────────────────────────────────────────────────────────────────────
  Audience source       Femmes 30-45 actives urbaines (sub-cluster
                        audience-hero · 60% atlas brand encoded)
                        POURQUOI · positioning minceur clean brand.json
                        + signal mining mine-voc 47 verbatims encoded
                        upstream (densité OK pour synthèse moyenne)

  Dimensions cartograph. 8 dimensions canon V3 · Purchase Driver
                        Problem Map (3 niveaux surface/consequence/deep)
                        Benefit Stack (functional/emotional/identity)
                        Mechanism audience-side · Market Context Schwartz
                        Alternative Map · Identity Signals · Decision
                        POURQUOI · canon creative-formula V3 + pain-benefit
                        chain doctrine + audience-cartography 4 mouvements

  Sources data          1. brand.json + spec.json encoded (positioning
                           minceur clean · konjac mechanism · proof points)
                        2. Klaviyo Liv 5k NPS responses (first-party hero)
                        3. mine-voc output Trustpilot + forums (47 verbatims)
                        4. canon archetypes-voix (caregiver/sage map)
                           heuristiques-persuasion (loss-aversion · social
                           proof biais audience-side)
                        POURQUOI · brand-truth → first-party densité →
                        third-party validation → canon cross-pollination

  Granularité output    1 audience-hero broad-level · scope segment
                        (entre 100-500k actives FR) · pas micro-niche
                        POURQUOI · signal volume_remaining > 200k actives
                        FR + offer divergent (pas de sous-segment pricing
                        différencié encore encodé)

  Hypothèses figées     H1 · âge dominant 32-42 (inféré profil Klaviyo)
                        H2 · canal acquisition Instagram + Pinterest dominé
                             (inféré · pas verbatim)
                        H3 · psychographie auto-déclarée "active urbaine"
                             (matche site copy · pas mining verbatim)
                        H4 · trigger event "post-grossesse OU rentrée
                             post-vacances" (inféré seasonality)

  Biais à éviter        Over-segmentation · ne pas créer "femme 30-35"
                        et "femme 35-45" sub-audiences sans pitch_divergent
                        Stéréotype démographique · "femme donc Instagram"
                        statistique averaged-LLM → skip si pas verbatim
                        Projection persona-marketing · anti-pattern AP-2
                        doctrine investigation-posture (persona analytique
                        sans data verbatim · confidence TRÈS faible flag
                        obligatoire si zéro mining)

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Prerequisite check (Klaviyo + mine-voc + brownfield seed)
  2. Framework cartography Q1 porte d'entrée (pain/goal/identity)
  3. Load canon Schwartz + archetypes + heuristiques
  4. Synthesize 8 dimensions canon V3 (verbatim-anchored)
  5. Cross-validate Schwartz double-stage (product × emotional)
  6. Stage pain_points + objections sub-audience canonical v2.64
  7. Surface draft posture hypothèse + confidence chain explicit
  8. Audience Visibility Matriciel (audience × pains × angles)
  9. Operator validation gate → write_to_context profile.json

  ETA           ~8 min (mining + brownfield seed dispo · synthèse moyenne)
  Implication   tu valides paramètres d'abord · puis tu valides synthèse
  Livrable      profile.json 8 dim + sub-audience pain_points/objections
                + matrice visibility + close drill-down macro

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite paramètres AVANT lancement synthesis. L'opérateur peut · (a) valider tout · (b) ajuster un paramètre spécifique (e.g. "granularité micro pas segment", "ajoute Reddit dans sources", "biais saisonnalité à intégrer"), (c) abandonner / différer. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set OR si opérateur a flag `--no-disclosure` explicit. Sinon · disclosure obligatoire canon v2.79.5+.

Cross-ref doctrines · `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ (NIVEAU 0 pré-exec) + `docs/system/engagement-disclosure-doctrine.md` v2.79.5 (Paramètres décomposés section).

### HR0quater · Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ · synthèse 8 dimensions canon V3 · cross-validation Schwartz double-stage · staging pain_points + objections sub-audience canonical · ~8 min selon densité mining). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement HR0ter disclosure NIVEAU 0 en amont et Audience Visibility Matriciel matricielle (NIVEAUX 1-4) en aval.

Pattern obligatoire · l'agent verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique le sub-cluster audience et synthétise les 8 dimensions, en prose narrative sobre (zéro matrice ASCII en LIVE · les matrices viennent en Output Audience Visibility Matriciel post-encoding).

**2 niveaux d'abstraction obligatoires** ·

1. **Macro contexte audience sub-cluster** · verbaliser la compréhension du périmètre audience cible AVANT de rentrer dans le détail dimensions.
   Exemple profile-audience · "On part d'un sub-cluster {nom audience · cardinality broad / segment / micro} qui se situe dans l'atlas brand {positioning macro brand} comme audience {hero / secondaire / entry}. Densité mining disponible · {N verbatims encoded · sources actives · porte d'entrée Q1 framework cartography détectée pain_driven / goal_driven / identity_driven}. Stade Schwartz sophistication marché probable · {1-5 inféré canon × signaux brand}. Mon hypothèse archetype-voix candidate · {caregiver / sage / hero phrasé pourquoi · pas tag brut} parce que {pattern verbatims observés + canon archetypes-voix consulté}."

2. **Micro pain-benefit-chain phrasé** · verbaliser la chaîne pain × benefit pendant l'encoding 8 dimensions.
   Exemple profile-audience · "Cette audience entre par {Q1 porte} sur pain de surface {phrasé sourced verbatim} → conséquence vécue {phrasé canon pain-benefit-chain · ce que ça génère concrètement quotidien} → pain deep racine {phrasé · trigger identitaire profond derrière la surface} → bénéfice fonctionnel attendu {ce qui doit changer extérieurement mesurable} → bénéfice émotionnel attendu {ce qui doit changer subjectivement ressenti} → bénéfice identitaire attendu {ce que l'audience veut projeter socialement après résolution}. Cross-validation Schwartz double-stage · stage produit {1-5} mais stage émotionnel audience {1-5 souvent shift en aval} parce que {raisonnement canon}."

**Calibration narrative** · prose sobre · registre pair senior expert · zéro jargon plumbing (jamais `profile.json#purchase_driver`, `_field_types`, `confidence_chain[]`, `audience.lineage` en LIVE) · zéro tableau ASCII en LIVE (matrices = Output Audience Visibility Matriciel post-encoding). Adapter le tonal au registre opérateur détecté (grounded · standard · dense).

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger entre dimensions encodées si l'agent part dans une mauvaise direction d'inférence (mauvais pain deep projeté · mauvais archetype audience-side · cross-validation Schwartz incohérente) AVANT que les dimensions downstream cascadent sur cette base, (b) pédagogie · il apprend la posture stratégique experte sur cartographie audience en regardant la manière de penser une chaîne pain-benefit canon 3 couches × cross-validation Schwartz double-stage.

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

### Step 0bis · Prerequisite check (DRGFP v2.38)

Avant lecture mining outputs (Step 1), scanner prerequisites :

1. Lookup `audiences/{slug}/profile.json` brownfield existing → si présent + freshness 90d OK → seed corpus silent (HR2.5 v2.35 pattern)
2. Lookup mining outputs (mine-voc, mine-vom, mine-audience) → si présents → consume silent
3. Compter verbatim_density cumulé (existing seed + mining) → si < 3 → L3 degraded · fallback infer canon archetype · confidence 0.5 · flag _gaps
4. Lookup canon archetypes-voix → silent always (cross-brand canon read)

Output state map + confidence_chain[] init avec valeur dépendante de density actuelle.

Cross-ref doctrine : `docs/system/dependency-resolution-protocol.md`.

Note framework cartography · Step 0ter applique 4 questions framework (entry_door · scope · stade Schwartz · chevauchements). Cf `docs/doctrine/audience-cartography-framework.md`.

### Step 0ter · Framework awareness (v2.39+)

Application du framework cartography (4 questions canon · `docs/doctrine/audience-cartography-framework.md`).

Au début de la cartographie · poser Q1 explicit (porte d'entrée). Les 3 autres questions sont posées au fil du flow (Step 1 niveau · Step 4 stade · Step 7 chevauchements).

#### Q1 · Porte d'entrée

AskUserQuestion :

> Cette audience entre dans la catégorie {brand_category} par quelle porte ?
> 
> (a) Pain-driven · entre par un problème ressenti (ex chute, sec, gris)
> (b) Goal-driven · entre par une ambition (ex longueur pour mariage, summer hair)
> (c) Identity-driven · entre par qui elle est ou veut être (ex hijabi, sportive, mum)
> 
> 1 porte dominante. Si elle a 3 portes égales, c'est un mix mal séparé · à re-découper.

Persister dans meta.entry_door enum [pain_driven · goal_driven · identity_driven].

Si operator hésite ou répond "mix" → flag potential audience-redondante (Piège 2 framework) · suggestion · re-découper avant cartographier.

Operator-facing · jamais exposer "entry_door" brut. Dire "porte d'entrée" en surface.

#### Q2 · Niveau granularité (Step 1 mining)

Inférer scope automatiquement depuis :
- audience description scope (large/spécifique/hyper-niche)
- verbatim count + diversity (si forte diversité = broad ; concentrée = segment ; ultra-spécifique = micro)
- parent_slug détectable dans existing brand audiences

Si ambiguïté → AskUserQuestion :

> Niveau de granularité de cette audience ?
> 
> (a) Broad · audience mère, 500k+ actives, 1-3 par brand
> (b) Segment · poche définie, 100-500k actives, 5-15 par broad
> (c) Micro · hyper-niche, 20-100k actives, 0-3 par segment

Si micro → require justification 3/3 :
- volume_remaining_estimate (k actives)
- pitch_divergent (oui/non + en quoi)
- offer_divergent (oui/non + en quoi)

Si 0/3 ou 1/3 → refuse + suggestion "c'est une variation copy, pas une sous-audience".

Persister meta.scope + meta.parent_slug.

Operator-facing · dire "niveau" et "audience mère", jamais "scope" ni "parent_slug" brut.

#### Q3 · Stade Schwartz (Step 4 psychology block)

Au moment de remplir block psychology · inférer 2 axes Schwartz depuis verbatim + behaviour patterns :
- product-awareness (unaware → problem → solution → product → most-aware)
- emotional-maturity (niant · résigné · en recherche · combatif · acceptant)

Surface inference + AskUserQuestion validation :

> Stade Schwartz inféré pour cette audience :
> 
> Product-awareness : {inferred_stage_product}
> Emotional-maturity : {inferred_stage_emotional}
> 
> (a) Confirmer
> (b) Ajuster product-awareness
> (c) Ajuster emotional-maturity
> (d) Ajuster les deux

Persister psychology.awareness_stage_product + psychology.awareness_stage_emotional.

#### Q4 · Chevauchements (Step 7 write final)

Avant write_to_context final · scanner brand-side existing audiences pour chevauchements potentiels :
- Pain_points overlap (similarity threshold 0.6)
- Benefits overlap (similarity threshold 0.6)
- Identity narrative overlap (semantic similarity)

Surface les 1-3 audiences cousines détectées :

> J'ai détecté chevauchement potentiel avec :
> 
>   {audience_X} · pain similaire {pain_overlap} (~{score}% match)
>   {audience_Y} · benefit similaire {benefit_overlap} (~{score}% match)
> 
> (a) Confirmer ces chevauchements (write meta.overlap_with)
> (b) Ne pas signaler ces chevauchements
> (c) Ajouter d'autres chevauchements manuels

Persister meta.overlap_with[] array slugs.

Note pédagogique opérateur · les chevauchements ne disqualifient pas l'audience · ils révèlent les angles porteurs cousinés (cross-pollinisation copy). Operator-facing · dire "audiences cousines", jamais "overlap_with" brut.

### HR0bis · Load canon matrices (v2.55 routing systémique)

Avant HR1 (mining inputs), **force la lecture** des matrices canon copy déclarées en `consumes:`. Skill ne fonctionne pas en mode prose libre déduit de connaissance LLM · il consume canon. Si canon est dormant → output générique averaged-LLM, contourne le master doctrine `PhantomOS reasons over a business universe`.

Lecture batch via `python3 .skills/phantom-canon.py copy {layer}` pour chaque couche utilisée par ce skill ·

1. **`niveaux-schwartz`** · les 5 stages product_awareness + 5 stages emotional_maturity canoniques (Step Q3 + HR4 Schwartz double-stage). Cache en mémoire pour la durée du run.
2. **`archetypes-voix`** · 6+ archetypes canon (caregiver, sage, rebelle, amante, heros, homme-ordinaire). Cross-référencé en HR3 Dimension 7 (Identity Signals) pour mapper l'archetype audience-side à un archetype canon, pas inventer.
3. **`heuristiques-persuasion`** · biais cognitifs canon (loss-aversion, social-proof, scarcity, anchoring, reciprocity, authority, etc.). Cross-référencé en HR3 Dimension 1 (Purchase Driver) + Dimension 6 (Alternative Map · pourquoi insuffisant) pour informer le mapping psychology audience-side.
4. **`creative-formula.md` V3** · contrat 8 dimensions canon. Validé que les 8 dimensions HR3 mappent strictement aux 8 dimensions canon V3.

Pour chaque outil canon lu, garder en mémoire · `id, when_works[], when_avoid[], combines_with{}`. Ces contraintes filtrent quels archetypes/biais sont compatibles avec le contexte audience résolu en Step 0bis/0ter.

Cross-product canon × audience obligatoire en HR3 · chaque Dimension 1/6/7 cite explicitement le canon_ref utilisé (archetype_canon_id, biais_canon_id) dans Layer A trace + profile.json#lineage. Anti-pattern v2.55 banni · halluciner un archetype audience-side ("caregiver overprotecteur") sans le mapper au canon archetypes-voix.

### HR1 · Verify mining inputs available

Vérifier que `mine-voc` OR `mine-vom` OR `mine-audience` a tourné pour cette audience.
Si aucun mining n'a tourné, surface warning :

> Pas de signal mining disponible. Skill produira hypothesis-grade. Run mine-voc d'abord pour grade validated. Continuer ?

### HR2 · Load mining outputs (v1.6.0 v2.64 ontologie sémantique pure · read sub-audience direct)

Read `brands/{slug}/audiences/_voc/{audience}/*` + `_vom/*` + `raw/*`.
Aggrégate verbatims, key_expressions, benefits raw.

**Read pain_points + objections désormais depuis sub-audience direct (v2.64 ontologie sémantique pure)** ·

1. Scan `brands/{slug}/audiences/{audience_slug}/pain_points/*.json` → owned natif (pas de filter affected_audiences[] nécessaire · l'audience parente est implicite via path) → cache aggrégat pain_points scope audience courante
2. Scan `brands/{slug}/audiences/{audience_slug}/objections/*.json` → idem owned natif → cache aggrégat objections scope audience courante
3. Backward compat read fallback v2.63 · si `brands/{slug}/audiences/{audience_slug}/pain_points/` vide OR absent, fallback lecture `brands/{slug}/pain_points/*.json` top-level v2.63 filtré par `affected_audiences` contains `{audience_slug}` (brownfield migration partielle)
4. Backward compat read fallback v1.7 · si top-level v2.63 absent aussi, fallback lecture `profile.json#/pain_points[]` legacy v1.7 (brownfield original)
5. Idem objections · scan sub-audience d'abord, fallback top-level v2.63, fallback profile.json legacy v1.7

Cache localement dans `/tmp/profile-audience/{audience}-mining-corpus.json` (incl. pain_points + objections aggrégés sub-audience OR fallback chain).

Owned natif sub-audience · un pain_point dans `brands/{slug}/audiences/audience_A/pain_points/PNT-12.json` appartient SÉMANTIQUEMENT à audience_A. Si audience_B a un pain similaire, c'est une entité distincte `brands/{slug}/audiences/audience_B/pain_points/PNT-NN.json` (pas de dedup cross-audience · l'appartenance précède le tracking).

### HR2.5 · Read existing profile.json as seed corpus (brownfield · v1.6.0 v2.64 ontologie sémantique pure)

v1.0.1 (v2.35 alignment) : HR2.5 brownfield seed (read existing profile.json as seed corpus, preserve validated entries) + HR7.1 merge strategy explicite (no auto-overwrite).
v1.5.0 (v2.63 ontologie pure) : pain_points + objections désormais read top-level collections via HR2 · profile.json sub-fields legacy v1.7 read fallback only.
v1.6.0 (v2.64 ontologie sémantique pure) : pain_points + objections désormais read sub-audience direct via HR2 · top-level v2.63 et profile sub-fields v1.7 read fallback only.

Si `brands/{slug}/audiences/{audience_slug}/profile.json` existe et contient déjà des entries (verbatims inliné, voice.key_expressions, benefits chain, identity etc.) :

1. Read le profile.json existant comme seed (audience-bound fields uniquement post-v2.63 · voice, benefits, identity, psychology, behavior, decision_process, role, market_position, research_meta, meta, persona_archetype, buyer_user_split)
2. Extraire :
   - voice.key_expressions[] · verbatims pré-existants
   - benefits[] · chain functional/emotional/identity pré-existants
   - identity.* · démographie pré-existante
   - **pain_points[] + objections[] sub-fields LEGACY** · si présents en brownfield v1.7, read fallback (les sub-audience collections HR2 ont priorité si déjà encodées, puis top-level v2.63, puis profile sub-fields v1.7)
3. Merger avec mining corpus (HR2 · sub-audience direct + top-level fallback + profile sub-fields fallback) si dispo
4. Marquer chaque entry source : `existing_profile` (seed) vs `mine_voc/vom/audience` (fresh mining)
5. Préserver `validation_status` existant des entries déjà validées (status >= validated)

HR2.5 garantit le skill fonctionne en mode brownfield (audience pré-amorcée par opérateur ou skill antérieur) sans écraser ni perdre l'existant. v1.6.0 · les pain_points + objections legacy sub-fields v1.7 ET top-level v2.63 restent lisibles fallback, mais ne sont plus écrits · le write-side v2.64 stage vers sub-audience canonical (cf HR5 + HR7.5 P2).

### HR3 · Synthesize 8 dimensions

Pour chaque dimension, extraire/synthétiser depuis le corpus :

**Dimension 1 · Purchase Driver**
Identify dominant driver from verbatims : `pain | desire | status | utility | identity | mixed`.
Source verbatims supporting (sample_size).

**Dimension 2 · Problem Map**
Pain principal + frequency + intensity + context.
Décomposer en 3 niveaux : `surface` (ce qu'elle dit en premier) · `consequence` (impact quotidien) · `deep` (sens identitaire/existentiel).

**Dimension 3 · Benefit Stack**
Bénéfices cherchés rangés par ordre de priorité.
Chaîne `functional → emotional → identity`.

**Dimension 4 · Mechanism (audience-side)**
Comment la cible PENSE que la solution doit fonctionner.
Exemple : "elle pense que la repousse vient de la racine donc cherche traitement scalp" vs "elle pense que c'est génétique donc cherche transplant".

**Dimension 5 · Market Context**
Niveau Schwartz sophistication 1-5 (canon copy reference).
Awareness stage dominant : `unaware / problem_aware / solution_aware / product_aware / most_aware`.

**Dimension 6 · Alternative Map**
Autres solutions utilisées (concurrents, OTC, bricolage, abandons).
Pourquoi elles ne suffisent pas (verbatims).

**Dimension 7 · Identity Signals**
Marqueurs mode de vie observables (style, références culturelles, valeurs déclarées).

**Dimension 8 · Decision Process**
Path achat (recherche, comparaison, consultation, déclenchement).
Decision makers : `self / family / peers / influencer / professional`.
Trigger event qui déclenche l'achat.

### HR4 · Cross-validate Schwartz double-stage

Pour chaque sub-cluster, identifier :
- `product_stage` : niveau Schwartz produit-spécifique (ex `product_aware` sur une brand donnée)
- `emotional_stage` : niveau émotionnel orthogonal (ex `pain-active` vs `solution-seeking`)

Note : peut différer (cf D#384 multi-product binding · audit S55).

### HR5 · Identify pain_points 3 niveaux (v1.6.0 v2.64 ontologie sémantique pure · stage sub-audience)

Pour chaque pain principal, décomposer chaîne :
- `surface` : verbatim direct ("j'ai mal aux pieds en fin de service")
- `consequence` : impact quotidien ("je rentre épuisé, irritable")
- `deep` : sens identitaire ("j'envisage de changer de métier")

Tag verbatims sources pour chaque niveau.

**Stage v2.64 ontologie sémantique pure · sub-audience canonical** · au lieu de stage les chains 3 niveaux comme sub-field `audiences/{a_slug}/profile.json#/pain_points/{idx}/chain` legacy OR top-level `brands/{slug}/pain_points/{PNT-NN}.json` avec affected_audiences[], stage `brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json` entité complète owned natif (path déclare audience parente, pas de array affected_audiences[]).

Generation incrémentale PNT-NN · scan `brands/{slug}/audiences/*/pain_points/*.json` existing cross-audiences pour next id. Si pain point déjà encodé sub-audience courante (via mine-voc upstream OR profile-audience précédent), update entité existante (refine chain levels avec nouveau verbatim sourcing). Si pain similaire détecté dans une autre audience, stage NEW entité dans audience courante (pas de dedup cross-audience · owned natif par parent path).

Mutation gate stage entité complète (NEW pain point) ·

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/pain_points/{PNT-NN}.json" --value '{<full pain_point entity JSON avec chain[] 3 levels + _source_meta>}' --source agent --confidence 0.7 --mode proposed --reason "v2.64 ontologie sémantique pure · sub-audience canonical · 3-level chain synthesis from VoC"
```

Update chain levels existing (refine avec nouveau verbatim sourcing) ·

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/pain_points/{PNT-NN}.json#/chain" --value '[{"level":"surface","formulation":"..."},{"level":"consequence","formulation":"..."},{"level":"deep","formulation":"..."}]' --source agent --confidence 0.7 --mode proposed --reason "Chain refine from new VoC sourcing"
```

Backward compat strict · profile.json#/pain_points[] sub-fields legacy v1.7 + top-level v2.63 `pain_points/{PNT-NN}.json` NE SONT PLUS écrits par profile-audience v1.6.0+. Read fallback preserved (HR2 + HR2.5).

### HR6 · Surface draft profile à operator (posture investigation, v2.54+)

**Doctrinal contract.** Présenter en posture **hypothèse**, pas conclusion analytique. Chaque audience structurée porte sa confidence chain explicite per `docs/system/investigation-posture.md`. Anti-pattern AP-2 doctrine BANNI · personas inventés présentés comme analytiques sans data verbatim client. Quand le mining n'a pas tourné (ou tourné partiellement), l'output doit signaler explicitement que l'audience est sur du sable.

**Confidence chain explicit par audience** ·

| Niveau confidence | Indicateurs requis | Formulation cible operator |
|---|---|---|
| `forte` | Mine-voc + analytics audience convergents + verbatims 10+ par pain principal | "Pattern confirmé · {audience}" |
| `moyenne` | Mine-voc partiel (5-10 verbatims) + indicateurs site convergents | "Hypothèse soutenue · {N} indicateurs" |
| `faible` | 1-2 indicateurs site OR opérateur déclaré sans mining | "Hypothèse à valider · {indicateur}" |
| `TRÈS faible` | Intuition modèle sur copy / partenaires / vocabulaire site, zéro verbatim client | "Intuition seulement · à valider OBLIGATOIREMENT avant utilisation stratégique" |

Default sans mine-voc · confidence `TRÈS faible`. Le skill DOIT explicitement flagguer ces audiences comme non-utilisables comme fondation à une décision budget / brief créa / positioning.

**Structure operator output par audience** ·

Pour CHAQUE audience proposée, structure obligatoire (anti-pattern · persona analytique présenté sans confidence chain) ·

- **Hypothèse identifiée · {nom audience court}** (titre)
- **Confidence** · {forte / moyenne / faible / TRÈS faible}
- **Indicateurs sources** · {ce qui justifie l'hypothèse · copy site / influence partners profile / déclaration opérateur / verbatims si mining tourné}
- **Validation requise** · {ce qui doit être fait pour upgrader à `forte` · ex "mine-voc sur Trustpilot + analytics audience"}
- **Anti-pattern à respecter** · si confidence `TRÈS faible`, flag explicite "OBLIGATOIREMENT à valider via mining client réel avant utilisation stratégique (décision budget / brief créa / positioning)"

Demander macro arbitrage :

> Voici les audiences structurées en hypothèses. Confidence chain visible par audience. Pour passer ces audiences de hypothèse `TRÈS faible` ou `faible` à `validée` · veux-tu lancer une écoute clients réelle maintenant (~8-12 min de mining sur Trustpilot + forums niche pour récupérer les vrais verbatims) ou tu valides intuitivement et on continue, en sachant que ce qui sera produit downstream (angles, brief créa) portera cette confidence-là ?

L'opérateur arbitre · `lance écoute clients` → trigger mine-voc silencieusement OR `valide et continue` → préserver les audiences en hypothèse + propager confidence chain downstream.

### HR7 · Persist via mutation gate

Une fois validé, `write_to_context` sur `brands/{slug}/audiences/{audience_slug}/profile.json`.
Conformité `profile.schema v1.3` obligatoire.
Source : `derived` (skill orchestrator) + tag verbatims sources.

### HR7.1 · Merge strategy explicite

Avant write_to_context :

1. Re-load profile.json actuel (state of truth at write time)
2. Pour chaque entry du draft skill :
   - Si entry source `existing_profile` + `validation_status >= validated` → preserve (skill ne touche pas)
   - Si entry source `mine_*` + entry n'existe pas dans current profile → append
   - Si entry source `mine_*` + entry existe dans current profile → flag conflict, surface à operator
3. Operator gate explicite si conflits détectés

### HR7.5 · Coverage extends v2.58 (role.type · objections.severity_score · behavior sub-fields)

**Append-only additive coverage** (v1.4.0). Trois orphans audit v2.57 fermés par dérivations / synthèses **post-HR3, pre-HR7 persist**. Ces patches NE remplacent PAS les 8 dimensions canon, ils ENRICHISSENT le profile.json schema-conforme avec sub-fields opérationnels downstream (produce-paid-angles, produce-copy-brief, audit-meta-account).

**Backward compat strict** · si le buyer_user_split n'est pas encodé (v1.2 brownfield) ou si les verbatims ne mentionnent pas comportements achat → skip silencieusement le sub-field correspondant, ne pas bloquer le run. Confidence calibrée selon densité signal.

#### P1 · profile.role.{type, proxy_link_id} derivation

Depuis `buyer_user_split` déjà encodé (v1.3 NEW field), dériver `profile.role.type` enum [`end_user` · `buyer` · `influencer` · `gatekeeper`] selon les règles ·

- **buyer** · si `buyer_user_split.is_split = true` ET `buyer_user_split.buyer_role = acheteur` (B2C2C, achat pour un tiers · cadeau, parent pour enfant, etc.)
- **end_user** · si `buyer_user_split.is_split = false` OR `buyer_user_split.user_role = consommateur` (achat = consommation, même personne)
- **influencer** · cas spécifique détecté semantiquement (KOL audience-side, parent prescripteur sans achat direct, recommandation tiers)
- **gatekeeper** · cas pro détecté semantiquement (médecin prescripteur, coach, formateur, conseiller qui filtre la décision)

Si l'audience cible un rôle `buyer` ou `influencer` qui agit pour le compte d'un `end_user` distinct, peupler `proxy_link_id` avec le slug de l'audience end_user cousine (cross-ref `audiences/{end_user_slug}/profile.json`). Si pas d'audience cousine encodée, `proxy_link_id = null` + flag _gaps suggérant `mine-audience` pour cartographier le end_user.

Stage via mutation gate ·

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/profile.json#/role/type" --value "{enum}" --source agent --confidence 0.7 --mode proposed --reason "Derived from buyer_user_split"
```

Si `proxy_link_id` peuplé ·

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/profile.json#/role/proxy_link_id" --value "{end_user_slug}" --source agent --confidence 0.7 --mode proposed --reason "Cross-audience link buyer→end_user"
```

**Anti-pattern banni** · halluciner un `role.type = influencer` ou `gatekeeper` sans signal semantic explicite (mentions verbatim "je recommande", "je prescris", contexte pro). Default safe = `end_user` si ambiguïté.

#### P2 · objections.severity_score synthesis (v1.6.0 v2.64 ontologie sémantique pure · stage sub-audience)

Lors de l'output profile-audience (Step synthesis), pour chaque objection encodée en HR3 Dimension 1/6, computer `severity_score` 1-10 depuis la formule ·

```
severity_score = frequency_band × emotional_charge_multiplier

frequency_band:
  high (5+ mentions distinctes verbatim)   = 8-10
  medium (3-4 mentions)                    = 5-7
  low (1-2 mentions)                       = 2-4

emotional_charge_multiplier:
  default                                  = 1.0
  intensifier (verbatim contient "rage",
   "frustration profonde", "ras-le-bol",
   "j'en peux plus", "écœurée", caps,
   ponctuation exclamative répétée)        = 1.2 (cap à 10)
```

**Stage v2.64 ontologie sémantique pure · sub-audience canonical** · au lieu de stage `severity_score` comme sub-field `audiences/{a_slug}/profile.json#/objections/{idx}/severity_score` legacy OR top-level v2.63 `brands/{slug}/objections/{OBJ-NN}.json` avec affected_audiences[], stage `brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json` entité complète owned natif.

Generation incrémentale OBJ-NN · scan `brands/{slug}/audiences/*/objections/*.json` existing cross-audiences pour next id. Si objection déjà encodée sub-audience courante, update entité existante (refine severity_score si nouvelles données changent le calcul). Si objection similaire détectée dans une autre audience, stage NEW entité dans audience courante (pas de dedup cross-audience).

Mutation gate stage entité complète (NEW objection) ·

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/objections/{OBJ-NN}.json" --value '{<full objection entity JSON avec severity_score + type + formulation + frequency + lifecycle_stage>}' --source agent --confidence 0.7 --mode proposed --reason "v2.64 ontologie sémantique pure · sub-audience canonical · severity synthesis frequency × emotional charge"
```

Update severity_score existing (refine objection sub-audience) ·

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/objections/{OBJ-NN}.json#/severity_score" --value {N} --source agent --confidence 0.7 --mode proposed --reason "Severity refine from new frequency × emotional charge"
```

Le `severity_score` permet à `produce-paid-angles` (HR4 scoring framework, Objection neutralization lens 20%) de pondérer les objections par urgence réelle plutôt qu'égalité naïve. Top-3 objections par severity_score deviennent prioritaires pour la matrice paid.

**Anti-pattern banni** · scorer une objection 9/10 sans 5+ verbatims OR sans emotional intensifier explicite. Score 7+ requiert combinaison frequency_band high ET intensifier.

Backward compat strict · profile.json#/objections[] sub-fields legacy v1.7 + top-level v2.63 `objections/{OBJ-NN}.json` NE SONT PLUS écrits par profile-audience v1.6.0+. Read fallback preserved (HR2 + HR2.5).

#### P3 · profile.behavior.{purchase_frequency, conversion_timeline, dominant_device, cart_behavior, seasonal_spikes, channel_preferences}

Depuis les VoC verbatims mentionnant comportements achat (Step HR2 mining corpus + HR2.5 seed corpus), derive les sub-fields `behavior.*` quand le signal verbatim est présent ·

| Sub-field | Verbatim signaux | Confidence calibration |
|---|---|---|
| `purchase_frequency` | "j'achète tous les 3 mois", "1x par an", "je renouvelle chaque saison" | 0.7 si 3+ verbatims convergents · 0.5 si 1-2 |
| `conversion_timeline` | "j'hésite 2 semaines avant d'acheter", "achat impulsif", "je compare 1 mois" | 0.7 si 3+ convergents · 0.5 si 1-2 |
| `dominant_device` | "je commande sur mobile", "tablette", "ordi pour les gros achats" | 0.6 si signaux convergents · 0.5 si single mention |
| `cart_behavior` | "j'abandonne mon panier souvent", "je rajoute pour la livraison gratuite", "checkout direct" | 0.6 si 2+ mentions · 0.5 si single |
| `seasonal_spikes` | "je commande surtout en hiver", "rush BFCM", "pas avant l'été" | 0.7 si pattern saisonnier explicite · 0.5 si inférence légère |
| `channel_preferences` | "je viens d'Instagram", "TikTok m'a fait découvrir", "Google search produit", "bouche-à-oreille" | 0.7 si 3+ convergents · 0.5 si 1-2 |

Stage chaque sub-field présent (skip si verbatim density insuffisant) ·

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/profile.json#/behavior/{sub_field}" --value "{value}" --source agent --confidence {0.5-0.7} --mode proposed --reason "VoC-anchored behavior synthesis"
```

Les `behavior.*` enrichissent ·
- `produce-paid-angles` Step 2 (Resolve placement context) avec `dominant_device` + `channel_preferences` pour calibrer placements
- `audit-meta-account` avec `conversion_timeline` pour configurer attribution windows
- `produce-copy-brief` avec `seasonal_spikes` pour timing campagne
- `analyze-perf` avec `cart_behavior` pour diagnostic checkout funnel

**Anti-pattern banni** · inventer un `behavior.dominant_device = mobile` parce que "c'est l'audience femme 30-45 donc statistiquement mobile". Sub-field VoC-anchored uniquement · zéro verbatim → skip le sub-field, ne pas hallucinaer un default statistique.

**Surface operator** · ces sub-fields restent INTERNES (jamais exposés bruts en surface HR6/HR8). L'opérateur voit l'audience structurée en 8 dimensions + close drill-down macro. Les sub-fields servent les skills downstream qui les liront via le profile.json schema-conforme.

### HR8 · Output operator-facing (close drill-down macro, v2.54+)

Vue lisible profile · chaque audience portée comme hypothèse avec confidence chain explicite per HR6 refactor.

**Close obligatoire · UNE question macro drill-down** (anti-pattern AP-5 doctrine · close affirmatif qui ferme la conversation `Je passe au next step ?` → BANNI).

Format close canonique v2.54 ·

> Pour passer ces audiences de hypothèse `TRÈS faible` à validée terrain, ce qui débloque la suite (angles paid, brief créa) avec une fondation sourcée ·
>
> A · Lance l'écoute clients maintenant ({~8-12 min} sur Trustpilot + forums niche · récupère les vrais verbatims · upgrade confidence à `moyenne` ou `forte` selon densité corpus)
> B · Valide intuitivement et on continue · ce qui sera produit downstream (angles, brief créa) portera la confidence `TRÈS faible` héritée (à tester avec budget calibré, pas all-in)
> C · Tu m'injectes des données existantes que t'as déjà (reviews exportées, analytics audience, retours SAV) en 1-2 phrases denses, je les intègre et on re-évalue confidence
>
> Mon avis · {recommandation macro adaptive · si verbatim_density < 3 → A en premier critique pour fondation downstream · sinon B valide si confidence `moyenne` déjà sur l'audience}.

L'opérateur arbitre macro. Pas de menu décoratif, UNE question avec reco.

**Anti-patterns surface operator** ·
- JAMAIS exposer `confidence` comme un nombre (0.6, 0.4) en surface. Qualitatifs uniquement (`TRÈS faible / faible / moyenne / forte`).
- JAMAIS exposer field path interne (`meta.entry_door`, `psychology.awareness_stage_product`, `validation_status: hypothesis`) en surface. Reformuler en langage métier.
- JAMAIS nommer skill (`mine-voc`, `produce-paid-angles`) en surface · routing silencieux à l'agent après choix opérateur.
- JAMAIS afficher persona inventé comme analytique (anti-pattern AP-2 doctrine). Toujours flaggué hypothèse avec confidence chain.

### HR10 · NEW Output section `Audience Visibility Matriciel` obligatoire (v2.78.2 decomposition visibility)

Après encoding 8 dimensions canon V3 (HR3) + 5 sections IP (Observé · Déduit · Inconnu · Leviers · Close ouvert per `docs/system/investigation-posture.md`), présenter OBLIGATOIREMENT vue matricielle canon `decomposition-visibility-discipline` v2.78.2.

L'opérateur ne doit jamais voir l'encoding 8 dimensions sans la synthèse matricielle finale. Encoding silent sans visibilité = AP10 banni.

Section NEW à émettre AVANT le close investigation posture (avant la question macro drill-down HR8). Structure complète canon · cf section dédiée "Output · Audience Visibility Matriciel (canon v2.78.2)" infra.

### HR11 · Matrice audience × pain × angle obligatoire si ≥2 pains owned

Si l'audience encodée a sub-collection `audiences/{a_slug}/pain_points/PNT-NN.json` contenant ≥2 entités owned (post-HR5 stage), émettre matrice ASCII canon (audience header + pain_points listing + angles proposed vers `produce-paid-angles` downstream).

Si <2 pains owned · skip matrice ASCII · noter "matrice activée à partir de 2 pains owned, actuellement {N}" en surface (transparence opérateur).

Le many-to-many (audience ↔ N pains ↔ N angles) doit être explicit, JAMAIS implicite. Opérateur ne déduit pas la relation, l'agent la trace.

### HR12 · Stage business filter obligatoire si signal détectable

Si stage business inférable depuis brand context (signal observable · ARR mentionné, proof points encodés brand.json#financials, domain age via Wayback, traction signals stratégie), émettre table canon ·

```
STAGE business        [early | growth | scale]
Audience priorité     [primary | secondary | backup] selon stage
Angle dominant        [identity heavy | functional + identity | diversifié]
```

Si zéro signal détectable · skip table + noter "stage business non détectable depuis brand context actuel, table activée si signal ajouté brand.json#financials ou via snapshot-brand re-run".

L'inférence stage doit citer son signal source (anti-pattern · stage inventé sans signal observable).

### HR13 · Audience produit-fit vs ciblage créa distinction explicit

Dans le header matrice canon, distinguer deux statuts orthogonaux ·

- **Audience produit-fit** · toutes les audiences encoded retain by product (par définition encoded = produit-fit, sinon supprimée upstream)
- **Audience ciblage créa** · enum `primary | secondary | backup` selon positioning targeting strategy (encodée par produce-paid-matrix downstream)

Statut ciblage par défaut · "à déterminer downstream produce-paid-matrix" si jamais staged. Anti-pattern · confondre les deux statuts (produit-fit ≠ ciblage créa).

### HR14 · Méthode pédagogique verbale obligatoire

Verbaliser TOUJOURS comment l'agent a cartographié l'audience · résumé 1-ligne par dimension (8 lignes) + déclaration explicit du many-to-many (cette audience est [primary/secondary/backup] sur [N] pains, au stage [X] elle est prioritaire [oui/non], positioning targeting [produit-fit vs ciblage créa]).

Format ·

> J'ai cartographié [audience slug] en 8 dimensions canon V3 ·
> - Démographie · [résumé 1 ligne]
> - Psychographie · [résumé 1 ligne]
> - Triggers · [résumé 1 ligne]
> - Stage in journey · [résumé 1 ligne]
> - Sophistication · [niveau 1-5]
> - Buyer/User split · [résumé 1 ligne]
> - Language · [registre détecté]
> - Validation status · [hypothesis | confirmed | scaled]
>
> L'audience possède [N] pain_points sub-collection canonical PNT-NN.json · chacun owned, severity scoré, layer pain-benefit-chain explicit.
>
> Many-to-many · cette audience est [primary | secondary | backup] sur [N] pains identifiés · au stage business [détecté X], audience prioritaire [oui/non] · positioning targeting [audience produit-fit vs ciblage créa].

Pédagogie verbale = anti-jargon (jamais exposer field path interne · "8 dimensions" OK, "psychology.awareness_stage_product" jamais). Per HR8 operator-facing rules.

### HR15 · Anti-patterns

- Ne JAMAIS halluciner une dimension sans verbatims sources
- Ne JAMAIS poser une dimension à hypothesis sans tag `confidence < 0.5`
- Ne JAMAIS skip Schwartz double-stage check
- Ne JAMAIS auto-write sans operator validation gate
- Ne JAMAIS exposer JSON brut à l'opérateur
- **AP10 (v2.78.2)** · Ne JAMAIS encoding 8 dimensions silent sans synthèse matricielle finale `Audience Visibility Matriciel`. L'encoding seul = invisible decomposition.
- **AP11 (v2.78.2)** · Ne JAMAIS many-to-many implicite (opérateur déduit la relation audience-pain-angle). L'agent trace la matrice, pas l'opérateur.
- **AP12 (v2.78.2)** · Ne JAMAIS stage business absent du filtre si signal détectable. Skip légitime uniquement si zéro signal observable (transparence explicit obligatoire).
- **AP13 (v2.78.2)** · Ne JAMAIS méthode pédagogique skip. La verbalisation 8 dimensions + many-to-many est obligatoire, pas optionnelle.

## Output · Audience Visibility Matriciel (canon v2.78.2)

Après encoding 8 dimensions audience canon V3 (demographics · psychographics · triggers · stage_in_journey · sophistication · buyer_user_split · language · validation_status), présenter OBLIGATOIREMENT vue matricielle canon `decomposition-visibility-discipline` v2.78.2.

Cette section enrichit l'operator output template legacy (v2.54 investigation posture · 5 sections IP) sans le remplacer. Section ajoutée APRÈS les 8 dimensions encoded + 5 sections IP, AVANT le close drill-down macro HR8.

### Matrice audience × pain × angle (canon many-to-many)

Si audience encodée a sub-collection `pain_points/PNT-NN.json` owned (≥2 pains per HR11) · matrice ASCII obligatoire ·

```
AUDIENCE · [slug + nom mère]
Audience produit-fit · ✓ (toutes audiences encoded retain by product)
Audience ciblage créa · [✓ primary | ✓ secondary | · backup selon
                        positioning targeting strategy]

PAIN POINTS owned (sub-collection PNT-NN.json)
────────────────────────────────────────────
PNT-01 [label]    severity [1-10]   functional/emotional/identity
                  emotional_signal · [signal]
                  latency · [instant | 1-2 sessions | 2-3 semaines | etc.]

PNT-02 [label]    severity [1-10]   functional/emotional/identity
PNT-NN ...

ANGLES PROPOSED (vers produce-paid-angles downstream)
────────────────────────────────────────────────────
ANG-candidate-1   pain_addressed · PNT-01
                  formula · OTRB
                  niveau Schwartz · [unaware | problem | solution | product]
                  stage business match · [early | growth | scale]

ANG-candidate-2   ...
```

Si <2 pains owned · skip matrice + noter "matrice activée à partir de 2 pains owned, actuellement {N}" en surface (transparence opérateur, per HR11).

### Stage business filter (si détectable)

Si stage business inférable depuis brand context (ARR · proof points · domain age via Wayback · traction signals encodés brand.json#financials) · table canon obligatoire (per HR12) ·

```
STAGE business        [early | growth | scale]
Audience priorité     [primary | secondary | backup] selon stage
Angle dominant        [identity heavy | functional + identity | diversifié]
```

Si zéro signal détectable · skip table + noter transparence opérateur "stage business non détectable depuis brand context actuel, table activée si signal ajouté brand.json#financials ou via snapshot-brand re-run".

L'inférence stage doit citer son signal source en 1 ligne (e.g. "stage growth inféré · proof_points 50+ clients encoded brand.json + domain age 2y via Wayback").

### Méthode pédagogique verbale (per HR14)

Verbaliser TOUJOURS comment l'agent a cartographié l'audience ·

> J'ai cartographié [audience slug] en 8 dimensions canon V3 ·
> - Démographie · [résumé 1 ligne]
> - Psychographie · [résumé 1 ligne]
> - Triggers · [résumé 1 ligne]
> - Stage in journey · [résumé 1 ligne]
> - Sophistication · [niveau 1-5]
> - Buyer/User split · [résumé 1 ligne]
> - Language · [registre détecté]
> - Validation status · [hypothesis | confirmed | scaled]
>
> L'audience possède [N] pain_points sub-collection canonical PNT-NN.json · chacun owned, severity scoré, layer pain-benefit-chain explicit.
>
> Many-to-many · cette audience est [primary | secondary | backup] sur [N] pains identifiés · au stage business [détecté X], audience prioritaire [oui/non] · positioning targeting [audience produit-fit vs ciblage créa].

Pédagogie verbale = anti-jargon. Jamais exposer field path interne brut (e.g. "psychology.awareness_stage_product" jamais ; dire "stade Schwartz produit" en surface). Per HR8 operator-facing rules.

### Anti-patterns NEW section (canon v2.78.2)

- **AP10** · Encoding 8 dimensions silent sans synthèse matricielle finale → invisible decomposition, opérateur ne voit jamais le many-to-many.
- **AP11** · Many-to-many implicite (opérateur déduit la relation audience-pain-angle).
- **AP12** · Stage business absent du filtre si signal détectable.
- **AP13** · Méthode pédagogique verbale skip.

## Operator output template (v2.54 investigation posture)

Template canonique post-v2.54 · chaque audience portée comme hypothèse avec confidence chain explicite. Anti-pattern AP-2 doctrine BANNI · personas inventés présentés comme analytiques sans data verbatim.

```
{BRAND} · {AUDIENCE_SLUG} · HYPOTHÈSE STRUCTURÉE

Hypothèse identifiée · {nom audience court}
Confidence · {forte | moyenne | faible | TRÈS faible}
Indicateurs sources · {ce qui justifie · copy site / influence partners / déclaration opérateur / verbatims mine-voc si dispo}
Validation requise · {ce qui doit être fait pour upgrader · ex "mine-voc Trustpilot + analytics audience"}
{Si confidence TRÈS faible · ligne flag explicite "OBLIGATOIREMENT à valider avant utilisation stratégique (budget / brief créa / positioning)"}

─────────────────────────────────────────────

[1] Purchase driver (hypothèse)
  Dominant driver inféré  {driver}
  Indicateurs             {N} citations verbatim si dispo, OR signaux site si pas de mining
  À valider               {ce qui upgrade confidence sur ce driver}

[2] Problem map (hypothèse)
  Pain principal inféré  {pain}
  Fréquence              {frequency} ({confidence sur freq})
  Intensity              {intensity}
  Surface (1er niveau)   "{verbatim si dispo}" OR "à capturer via mining"
  Consequence (2e)       {consequence inférée}
  Deep (3e identitaire)  {deep_meaning inféré · confidence TRÈS faible si pas de mining}

[3] Benefit stack (hypothèse)
  Top bénéfices inférés
    1. {benefit_1} (functional → emotional → identity)
    2. ...
  Indicateurs              {sources mining si dispo}

[4] Mechanism · audience-side belief (hypothèse)
  La cible pense que la solution doit fonctionner via · {mechanism_belief}
  Confidence sur ce belief · {niveau}
  À valider                · {comment vérifier · ex "mine-voc reviews concurrence + forums"}

[5] Market context (déduit · confidence variable)
  Schwartz sophistication inféré  {1-5} ({confidence})
  Awareness stage dominant       {stage} ({confidence})
  Product awareness              {product/solution/problem/unaware}
  Emotional stage                {pain-active / solution-seeking / etc.}
  Indicateurs                    {sources mining OR signaux site}

[6] Alternative map (hypothèse)
  Solutions essayées avant inférées
    - {alt_1} · pourquoi insuffisant inféré · {reason}
    - {alt_2} · ...
  À valider · verbatims forums/reviews pour confirmer les vraies alternatives essayées

[7] Identity signals (hypothèse · confidence DEFAULT TRÈS faible sans data verbatim)
  Mode de vie inféré   {signals depuis copy + partners}
  Valeurs inférées     {values revendiquées site}
  Références inférées  {cultural_refs depuis ton + casting}
  À valider · mine-voc + scan vernaculaire forums niche

[8] Decision process (hypothèse)
  Path achat inféré    {path}
  Decision makers      {makers · confidence}
  Trigger event inféré {trigger}
  À valider · verbatims "comment as-tu connu" / "qu'est-ce qui t'a fait acheter"

─────────────────────────────────────────────

Close · UNE question macro drill-down

Pour upgrader cette audience de hypothèse {confidence actuelle} à validée terrain ·

A · Lance l'écoute clients (~8-12 min · mining Trustpilot + forums · récupère verbatims réels · upgrade à `moyenne` ou `forte`)
B · Valide intuitivement et continue · downstream porte confidence `{actuelle}` héritée
C · Injecte data existante (reviews exportées, analytics, retours SAV · 1-2 phrases denses)

Mon avis · {reco macro adaptive selon verbatim_density actuelle}.
```

**Hard rules template** ·
- Chaque dimension porte sa confidence par défaut quand pas de mining.
- Anti-pattern · présenter `[2] Problem map · Pain principal · "Je perds mes cheveux"` comme un fait alors que zéro verbatim n'a été récupéré. Toujours signaler "inféré" + indicateurs sources + à valider.
- Anti-pattern · close affirmatif (*"Tu valides en bloc ?"*) → BANNI. Toujours close drill-down macro avec UNE question A/B/C + reco.

## Cross-references

- `docs/system/decomposition-visibility-doctrine.md` (v2.78.2 + v2.79.5+ NIVEAU 0 + v2.81.1+ NIVEAU LIVE canon racine) · doctrine 3 phases temporelles · AVANT exec NIVEAU 0 paramètres décomposés (HR0ter) · PENDANT exec NIVEAU LIVE thinking aloud expert action LOURDE 2 niveaux abstraction macro contexte audience + micro pain-benefit-chain phrasé (HR0quater) · APRÈS exec NIVEAUX 1-4 Output Audience Visibility Matriciel · audience × pain × angle × stage business obligatoire après encoding 8 dimensions · many-to-many explicit, jamais implicite · HR-DVD-11 + AP-DVD-11 enforcement.
- `docs/system/investigation-posture.md` (v2.54 doctrine canon) · cartographier avant affirmer · confidence chain explicit · audiences comme hypothèses (TRÈS faible par défaut sans mine-voc) · close drill-down macro · opérateur arbitre.
- `docs/system/contextual-intelligence.md` · master doctrine, no orphan output, jargon zéro en surface.
- `docs/system/audience-cartography.md` · doctrinal contract cartography (mère / sous-audiences, 4 movements).
- `docs/system/pain-benefit-chain.md` · 3 couches functional · emotional · identity · chaînage canonique pain/benefit (layer explicit dans matrice).
- `docs/doctrine/audience-cartography-framework.md` · 4 questions framework canon Step 0ter.
- `docs/system/confidence-propagation.md` · algèbre cascade confidence cross-skill (audience → angle → brief créa).
- Sister skills v2.78.2 (canon decomposition visibility) · `snapshot-brand` · `build-atlas-complete` · `define-specs`.
- `resources/canon/copy/niveaux-schwartz/*` (sophistication 1-5, awareness stages).
- `resources/schemas/profile.schema.json` v1.3 (`persona_archetype`, `buyer_user_split`, `purchase_driver` derived).
- `resources/canon/copy/creative-formula.md` V3 (8 dimensions canon).
- D#384 multi-product binding (audit S55) sur Schwartz double-stage.
