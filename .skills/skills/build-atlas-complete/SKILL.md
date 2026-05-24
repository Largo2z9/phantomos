---
name: build-atlas-complete
type: orchestrator
version: "1.7.1"
recommended_model: sonnet
reasoning_pattern: null
mode: proposed
operator_facing: true
subagent_safe: false
isolation_scope: brand_only
layer: territoire
extension_hooks:
  - audience_entity
  - angle_entity
  - creative_entity
  - brief_entity
  - territory_entity
  - product_entity
  - friction_entity
description: >
  v1.7.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution (entre disclosure pré-runtime NIVEAU 0 et chain Steps 1-10). Action LOURDE orchestrateur · narratif étendu 2 niveaux abstraction (macro brand entière + micro chaînes audiences/angles cross-encoded en prose) pendant handoffs sub-skills. Pose pair senior expert · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  v1.7.0 (v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés) · Section pré-runtime étendue · NIVEAU 0 ajouté en complément du disclosure plan/ETA/implication/livrable v2.79.3 existant · expose 6 paramètres décomposés au runtime (scope cartographier · profondeur cible · audiences à profiler · angles à générer · hypothèses figées · biais à éviter) avec POURQUOI chacun + close binaire OK ou ajuste · adapté au cycle 7 phases orchestrateur. Cross-ref doctrines decomposition-visibility-discipline + engagement-disclosure-discipline v2.79.5+. Backward compat strict additif (Phases 1-9 runtime preserved · seul l'amont disclosure enrichi).
  v1.6.0 (v2.78.2 decomposition visibility refactor) · NEW Phase Output Atlas Visibility Matriciel Multi-niveau obligatoire post-encoding entités (avant Step 9 Close) · 4 niveaux canon obligatoires (Décomposition produit cross-products · Many-to-many pain × audience matrix cross-atlas · Positionnement filtre par stage business · Méthode pédagogique verbale). Cross-ref doctrine `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2. Distinction explicit audience produit-fit (toutes encoded) vs audience ciblage créa (filter sub-set positioning targeting). Backward compat strict additif (Phases 1-7 + Step 8 stage + Step 9 close preserved · NEW phase output insérée entre Step 8 et Step 9). HR-NEW + AP-NEW ajoutés guardrails.
  v1.4.0 (v2.68 progressive cartography refactor) · chain orchestrator avec gates light entre paliers progressive (Phase 1+2 snapshot-brand · gate intermédiaire 1 · Phase 3 map-audiences hiérarchique parent/enfants · gate intermédiaire 2 · Phase 4 mine-voc + profile-audience enrichissement per audience). Mode `--fast-track` opérateur expert bypass gates auto-validate (opt-in flag OR config `auto_validate_after_n_brands` true). Validation operator entre chaque palier territoire (vs dump synthesis bloc canon précédent v1.3.0 où gates étaient Gate A audiences + Gate B angles seulement). Cross-ref doctrine `docs/system/progressive-cartography-doctrine.md` NEW v2.68. Backward compat strict additif sur chain skills (Steps preserved · gates additifs light · fast-track flag opt-in default off · gates A+B angles preserved après Phase 4).
  v1.3.0 (v2.67 territoire-pure refactor) · Steps 8-9 stripped (produce-copy-brief + compose-creative) · align doctrine `docs/system/territory-doctrine.md` shipped v2.67. Orchestrator scope = territoire substrat only · productions briefs+créas via `creative-brief-composer` post-atlas downstream (separate skill, separate invocation). Output explicite · complete strategic atlas substrate (specs + offers + audiences + angles + territoires scorés). BREAKING · operators v1.x qui invoquaient pour briefs+créas doivent invoquer `creative-brief-composer` post-`build-atlas-complete`. Migration documentée CHANGELOG v2.67.0. Backward compat strict additif sur Steps 1-7 unchanged (territoire chain preserved).
  v1.2.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience + frictions sub-product) · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans sub-parent locations · `audiences/{a_slug}/pain_points/` + `audiences/{a_slug}/objections/` + `products/{p_slug}/frictions/` (owned natif par parent path). Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.1.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans 3 collections séparées (`pain_points/` + `objections/` + `frictions/`) plus `profile.json` clean (identity + psychology + voice + behavior + decision_process restent · pain_points + objections sub-fields legacy supprimés post-v2.63 nouvelles brands). Backward compat preserved (pre-v2.63 brands route fallback profile sub-fields legacy).
  v1.0.2 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (dtc-operator-playbook, audiences-cartography, angle-anatomy, hooks-method, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  Full-cycle atlas substrate builder. Chains the territoire canon pipeline end-to-end on a
  blank or partially-built brand to produce the complete strategic atlas substrate
  (specs + offers + audiences + angles + territoires scorés) from a single operator intent.
  Single chairman orchestrating specialized skills with explicit gates between phases.
  Resolves the Scenario 4 orchestration gap surfaced in Phase 1 audit, so the agent never
  freestyles strategic prose to fill a multi-skill atlas request.
  FR: "génère l'atlas complet de {brand}", "build atlas {brand}", "lance le pipeline complet", "construis tout pour {brand}", "atlas complet from scratch".
  EN: "build complete atlas", "generate full atlas {brand}", "build everything for {brand}", "run full pipeline", "full atlas from scratch".
triggers_fr:
  - "génère l'atlas complet"
  - "build atlas {brand}"
  - "lance le pipeline complet"
  - "construis tout pour {brand}"
  - "atlas complet from scratch"
triggers_en:
  - "build complete atlas"
  - "generate full atlas"
  - "build everything"
  - "run full pipeline"
  - "full atlas from scratch"
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: [brand, product, offer, profile, learning, strategy]
  emits_events: [coherence_check, atlas_substrate_staged]
consumes:
  - brands/{slug}/brand.json
  - resources/schemas/spec.schema.json
  - resources/schemas/profile.schema.json
  - resources/schemas/angle.schema.json
  - resources/schemas/roadmap.schema.json
  - resources/catalogues/heuristiques-persuasion.json
  - resources/catalogues/niveaux-schwartz.json
  - resources/catalogues/formats-livrables.json
  - resources/catalogues/hooks.json
  - resources/catalogues/angles.json
  - path: docs/system/progressive-cartography-doctrine.md
  - path: docs/system/decomposition-visibility-doctrine.md
  - path: docs/system/territory-doctrine.md
  - path: docs/system/investigation-posture.md
  - path: docs/system/pain-benefit-chain.md
  - path: docs/doctrine/dtc-operator-playbook.md
  - path: docs/doctrine/audiences-cartography-doctrine.md
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/system/output-clarity-doctrine.md
  - path: docs/system/operator-vocabulary-translation.md
produces_proposals_for:
  - brands/{slug}/spec.json
  - brands/{slug}/products/*/offers.json
  - brands/{slug}/audiences/*/profile.json
  - brands/{slug}/audiences/*/pain_points/*.json
  - brands/{slug}/audiences/*/objections/*.json
  - brands/{slug}/products/*/frictions/*.json
  - brands/{slug}/pain_points/*.json (legacy v2.63 backward compat)
  - brands/{slug}/objections/*.json (legacy v2.63 backward compat)
  - brands/{slug}/frictions/*.json (legacy v2.63 backward compat)
  - brands/{slug}/angles/*.json
  - brands/{slug}/strategy.json
  - brands/{slug}/scoring/matrix-{date}.json
pipeline:
  preconditions: operator provides brand_slug AND (URL OR snapshot already completed). MCP tools available (facebook-graph optional, Notion optional).
  postconditions: |
    - brand structure fully populated across spec, offers, profile(s), angles
    - score-matrix territories ranked, top 3 axes créatifs selected
    - territories staged as proposals, ready for downstream production via creative-brief-composer (separate skill, separate invocation)
    - status.json updated, snapshot rebuilt, finalize-mutation-batch event emitted
    - learn-from-session flush proposed at end
disambiguates_against:
  onboard-brand: "route to onboard-brand when operator wants only the structural setup + snapshot + integrity check (no audiences/angles/briefs/créas). onboard-brand stops at the 'context loaded' gate."
  deepen-brand-context: "route to deepen-brand-context when operator wants only VoC + VoM mining on a snapshotted brand (no audiences/angles/briefs/créas downstream)."
  setup-brand: "route to setup-brand for initial identity/structure only."
  snapshot-brand: "route to snapshot-brand for URL scrape only on an existing brand."
  profile-audience: "route to profile-audience standalone when operator wants audiences only, not the full strategic atlas."
  score-matrix: "route to score-matrix standalone when atlas is already populated and operator wants only territory prioritization."
patch_notes:
  v1.7.1:
    - "v2.81.1 decomposition visibility NIVEAU LIVE thinking aloud · NEW section `Niveau LIVE · raisonnement thinking aloud pendant exécution` insérée APRÈS section disclosure pré-runtime NIVEAU 0 v2.79.5 et AVANT Expert methodology + chain Steps 1-10. Action LOURDE orchestrateur (30-90 min · 7 paliers · MCP optionnel) · NIVEAU LIVE narratif étendu obligatoire pendant exécution · pas seulement disclosure NIVEAU 0 en amont et Phase Output Atlas Visibility matricielle (NIVEAUX 1-4) en aval. Pattern canon · 2 niveaux abstraction obligatoires (macro brand entière + micro chaînes audiences/angles cross-encoded phrasé en prose narrative sobre). Pose pair senior expert thinking aloud · audit temps réel par l'opérateur entre handoffs sub-skills + pédagogie posture experte indissociables. Cross-ref `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid). Backward compat strict additif · cycle runtime préservé (Phases 1-9 + gates intermédiaires + Gate A + Gate B preserved · seul thinking aloud ajouté pendant chain skills exec)."
  v1.7.0:
    - "v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés · Section pré-runtime étendue (v2.79.3 plan/ETA/implication/livrable preserved · NIVEAU 0 6 paramètres décomposés ajouté en amont juste avant le plan) · expose au runtime · scope cartographier (brand entière vs scope partiel) · profondeur cible (substrate light hypothèse vs sourced 5+ verbatims) · audiences à profiler (N) · angles à générer (N par audience) · hypothèses figées (positioning canvas / voice 4D / whitespace) · biais à éviter (sur-engineering premier cycle / cartographier sans données / skip phases). Cross-ref doctrines decomposition-visibility-discipline + engagement-disclosure-discipline v2.79.5+. Backward compat strict additif (Phases 1-9 preserved · disclosure pré-runtime enrichi)."
  v1.6.0:
    - "v2.78.2 decomposition visibility refactor · NEW Phase Output Atlas Visibility Matriciel Multi-niveau insérée entre Step 8 (stage territories) et Step 9 (Close Investigation Posture)"
    - "4 niveaux canon obligatoires · NIVEAU 1 Décomposition produit cross-products (specs · mécanismes · bénéfices 3 couches functional/emotional/identity) · NIVEAU 2 Many-to-many pain × audience matrix cross-atlas (ASCII obligatoire) · NIVEAU 3 Positionnement filtre par stage business (early/growth/scale · audience produit-fit vs ciblage créa distinction) · NIVEAU 4 Méthode pédagogique verbale"
    - "Cross-ref doctrine canon racine `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2 shipped Agent A Sprint v2.78.2"
    - "Sister skills v2.78.2 cohérents · snapshot-brand · profile-audience · define-specs (chain entities encoded · Phase Atlas Visibility synthétise cross-atlas après tous returns)"
    - "Forward-compat sister skills v2.80 · produce-positioning-canvas (Moore format) · define-brand-voice (4D) si shipped · NIVEAU 3 Positioning Statement consume si entity present"
    - "HR-NEW · Phase output Atlas Visibility Matriciel obligatoire (post-encoding finale) · 4 niveaux matriciels canon obligatoires · Many-to-many matrix cross-products + cross-audiences obligatoire · Stage business filter obligatoire si signal détectable (ARR/proof points/domain age) · Audience produit-fit vs ciblage créa distinction explicit · Méthode pédagogique verbale obligatoire post-matrices"
    - "AP-NEW · Encodage atlas silent sans synthèse matricielle finale · Synthèse prose-only sans Phase Atlas Visibility · Many-to-many implicite cross-products (opérateur déduit) · Stage business absent du filtre positionnement · Méthode pédagogique skip (opérateur ne sait pas comment l'atlas a été construit)"
    - "Backward compat strict additif · Phases 1-7 chain skills preserved · Step 8 stage preserved · Step 9 close preserved (Investigation Posture 5 sections désormais consomme la synthèse matricielle Phase Atlas Visibility en amont · Observé section enrichie cross-niveaux)"
  v1.5.0:
    - "v2.75.0 NEW extension_hooks frontmatter declaration · permet manifest registry scan Step 0 DRGFP enrichi · NEW entities scaffolded via scaffold-extension v1.2.0+ avec consumable_by matching ce skill consommées automatiquement runtime. Backward compat strict additif · extension_hooks vide default · legacy v2.74.x comportement hard-coded canon entities preserved. Pattern canon doctrine extension-discovery-doctrine.md NEW v2.75.0."
  v1.4.0:
    - "v2.68 progressive cartography refactor · chain orchestrator avec gates light entre paliers progressive (Phase 1+2 snapshot · gate · Phase 3 map-audiences · gate · Phase 4 mine-voc + profile-audience). Mode --fast-track opérateur expert bypass gates auto-validate. Validation operator entre chaque palier territoire (vs dump synthesis bloc canon précédent v1.3.0). Cross-ref progressive-cartography-doctrine.md NEW v2.68. Backward compat strict additif sur chain skills (Steps preserved · gates additifs · mode flag opt-in)."
  v1.3.0:
    - "v2.67 territoire-pure refactor · Steps 8-9 stripped (produce-copy-brief + compose-creative) · align doctrine territory-doctrine.md. Orchestrator scope = territoire substrat only · productions briefs+créas via creative-brief-composer post-atlas downstream. BREAKING · operators v1.x qui invoquaient pour briefs+créas doivent invoquer creative-brief-composer post-build-atlas-complete. Migration documentée CHANGELOG v2.67.0. Backward compat strict additif sur Steps 1-7 unchanged (territoire chain preserved)."
  v1.0.0:
    - "Ship v2.56 · resolves Scenario 4 audit gap (Phase 1)"
    - "Chains 9 phases: setup → snapshot → deepen → profile → weight → angles → score → brief → créa"
    - "Explicit operator gates between Phases 4-5 and 6-7 (audience and angle validation)"
    - "Investigation Posture 5-section close (Observé / Déduit / Inconnu / Leviers / Close ouvert) mandatory"
    - "No raw numeric scoring exposed to operator (Compositional Cartography §7)"
  v1.0.1:
    - "v2.58 patch · canonical strategy.json path (was strategy/roadmap.json non-canon) · scoring matrix path aligned brands/{slug}/scoring/matrix-{date}.json (was strategy/score-matrix.json)"
    - "Closes dette technique runtime · strategy.schema v1.0 NEW shipped v2.58 canonical entity activée"
    - "produce-strategy v1.0.0 NEW orchestrator invokable en post-Phase 10 close si l'opérateur veut cadrer le focus Q{n} sur la brand atlas-complete · cycle stratégique distinct de la phase score-matrix"
  v1.0.2:
    - "v2.61 doctrine consume · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (dtc-operator-playbook, audiences-cartography, angle-anatomy, hooks-method, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts."
  v1.1.0:
    - "v2.63 ontologie pure pain_points + objections collections top-level · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans 3 collections séparées top-level (pain_points/ + objections/ + frictions/) plus profile.json clean (identity + psychology + voice + behavior + decision_process restent · sub-fields pain_points + objections legacy supprimés post-v2.63 nouvelles brands)"
    - "Downstream creative production phase · context.pain_point_ref canonical PNT-NN persisté dans creative.json downstream (cohérent v1.5)"
    - "Phase 6 produce-paid-angles consume v1.9 cohérent (lit pain_points/ + objections/ collections, persiste angle.lineage.pain_ref + objection_ref canonical)"
    - "Downstream copy brief phase consume v1.5 cohérent (sections Pain to activate + Objections to neutralize citent PNT-NN + OBJ-NN canonical IDs inline)"
    - "produces_proposals_for: enrichi avec pain_points/*.json + objections/*.json + frictions/*.json (NEW v2.63 top-level collections)"
    - "Backward compat strict · pre-v2.63 brands (legacy profile sub-fields) route fallback transparent, sub-skills route silently"
  v1.2.0:
    - "v2.64 ontologie sémantique pure pain_points + objections sub-audience + frictions sub-product · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans sub-parent locations (audiences/{a_slug}/pain_points/ + audiences/{a_slug}/objections/ + products/{p_slug}/frictions/), owned natif par parent path"
    - "Downstream creative phase v1.6 · context.pain_point_ref canonical PNT-NN persisté depuis sub-audience canonical"
    - "Phase 6 produce-paid-angles consume v1.10 cohérent (lit sub-audience pain_points/objections, persiste angle.lineage.pain_ref + objection_ref canonical sub-audience)"
    - "Downstream copy brief phase consume v1.6 cohérent (sections Pain to activate + Objections to neutralize citent PNT-NN + OBJ-NN sub-audience canonical IDs inline)"
    - "produces_proposals_for: enrichi avec audiences/*/pain_points/*.json + audiences/*/objections/*.json + products/*/frictions/*.json (NEW v2.64 sub-parent locations)"
    - "Backward compat strict additif · fallback transparent top-level v2.63 + profile sub-fields v1.7 preserved · sub-skills route silently selon disponibilité"
---

# Skill: build-atlas-complete

**CRITICAL:** this is an **Orchestrator**. **YOU MUST NEVER** re-implement setup-brand, snapshot-brand, map-audiences, mine-voc, profile-audience, weight-dimensions, produce-paid-angles, or score-matrix logic here. **YOU MUST** delegate to each existing skill in sequence via Task tool (when the subskill is `subagent_safe: true`) or inline invocation (when `subagent_safe: false`). Any deviation breaks the canon purity rule established by `onboard-brand`. **Scope v1.4.0 progressive cartography** · 4 paliers chain skills avec gates light entre paliers (`docs/system/progressive-cartography-doctrine.md` NEW v2.68) + Gate A audiences + Gate B angles preserved + mode `--fast-track` opérateur expert bypass gates intermédiaires (opt-in). **Scope v1.3.0 territoire-pure preserved** · productions briefs+créas post-atlas via `creative-brief-composer` (separate skill, separate invocation). Voir `docs/system/territory-doctrine.md`.

## Tone

Chairman orchestrating a territoire substrate pipeline that produces the complete strategic atlas substrate. Narrate each handoff in one operator-facing sentence ("structure prête… snapshot lancé… audiences cartographiées, deux gates devant nous… angles ranked…"). Operator never reads skill names, paths, field paths, scoring numbers, or Task tool mechanics. The pipeline is long (30-90 min depending on density), so heartbeat at each gate is non-negotiable.

---

## Engagement disclosure pré-runtime · canon v2.79.3 + NIVEAU 0 v2.79.5

Avant de lancer l'orchestration, expose ce disclosure à l'opérateur en DEUX phases successives (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.3 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5).

**Phase A · NIVEAU 0 paramètres décomposés (v2.79.5)** · expose les paramètres décomposés que l'orchestrateur va mobiliser. Build-atlas-complete est le skill orchestrateur le plus complexe du canon (7 paliers · 30-90 min · MCP optionnel · gates intermédiaires + Gate A + Gate B). Disclosure NIVEAU 0 obligatoire AVANT le plan/ETA pour que l'opérateur ajuste un paramètre racine (scope · profondeur · cardinalité audiences/angles) avant de brûler 30+ min.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Scope cartographier
     {brand entière (default · all 7 phases) OR scope partiel
     (audience X + angle Y) OR scope mère + sous-poches uniquement}
     POURQUOI · {ex "premier cycle atlas brand · scope complet"
     OR "atlas brand déjà cartographié 80% · refresh partiel
     2 audiences" OR "operator explicit demand subset"}

  2. Profondeur cible
     {substrate light (hypothèse confidence 0.5 valide · doctrine
     progressive-cartography v2.68) OR sourced (5+ verbatims par
     pain canonical · mine-voc enrichissement complet) OR mixte
     (mère sourced + sous-poches light)}
     POURQUOI ce niveau · {ex "premier cycle, hypothèse sourceable
     downstream · progressive cartography" OR "brand mature à
     scale · exige sourced complet pour producer paid"
     OR "MCP signals limités, hypothèse pragmatique"}

  3. Audiences à profiler
     {N audiences · default 3-5 mère + 2-4 sous-poches par mère ·
     cap Phase 6 top-3 par défaut}
     POURQUOI ce nombre · {ex "audience tree 4 mères posées Phase 3,
     enrichissement top-3 par density signal" OR "operator demand
     explicit N audiences" OR "MCP Reddit + Trustpilot mince ·
     scope reduit"}

  4. Angles à générer
     {N par audience · default top-5 angles ranked produce-paid-angles ·
     cap Phase 7 top-3 axes créatifs}
     POURQUOI cette variance · {ex "5 angles ranked par audience
     top-3 puis dédoublonnés cross-audience cluster-deduplication ·
     top-3 axes créatifs sélectionnés" OR "brand mature ·
     scope reduit top-3 angles top audience pour itération
     focus"}

  5. Hypothèses figées
     Positioning canvas en place · {OUI lu brand.json#positioning
     OR NON · canvas inféré spec.market_context + competitors
     ou propose-positioning-canvas suggéré post-atlas}
     Voice 4D définie · {OUI brand.json#tone_of_voice complet
     OR NON · voice inférée + flag inconnu Investigation Posture}
     Territoire whitespace identifié · {OUI lu brand.market.white_spaces
     OR NON · whitespace dérivé Phase 7 score-matrix · top axes
     créatifs = territoires whitespace par construction}

  6. Biais à éviter
     · Sur-engineering atlas premier cycle (encoder 8 audiences ×
       7 angles = 56 angles · canon = top-3 audience × top-5 angles
       puis cap top-3 axes · scope discipline territory-discipline
       v2.67)
     · Cartographier sans données (lancer Phase 6 angles avant
       Phase 4 mine-voc · canon HR4.5 verbatim density floor
       gate strict)
     · Skip phases (sauter Phase 3 map-audiences pour gagner
       temps · audiences inférées sans framework 4 questions =
       audience tree fragile · canon progressive-cartography v2.68
       refuse skip)

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je passe
  au plan + ETA ?
```

ATTENDS confirmation explicite Phase A avant d'enchaîner Phase B (plan + ETA + implication + livrable v2.79.3). Si opérateur ajuste un paramètre racine (ex "scope partiel 2 audiences" OR "profondeur sourced obligatoire"), recalibrer le plan + ETA en conséquence avant Phase B.

**Phase B · disclosure plan + ETA + implication + livrable (v2.79.3 preserved)** ·

```
Build atlas complet · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Structure brand + scan site (palier 1+2 · setup + snapshot)
  2. Cartographie audiences hiérarchique mère + sous-poches (palier 3)
  3. Enrichissement voix client par audience (palier 4 · mine-voc + profile)
  4. Pondérations dimensions audience × angle + angles paid ranked
  5. Scoring matrice brand-wide · top axes créatifs sélectionnés
  6. Synthèse Atlas Visibility Matriciel 4 niveaux canon
  7. Close Investigation Posture · handoff briefs+créas downstream

  ETA           ~30-90 min (selon densité audiences + signal disponible)
  Implication   tu valides aux gates intermédiaires + Gate A audiences + Gate B angles
  Livrable      atlas substrat complet (specs + offers + audiences enrichies + angles ranked + territoires scorés) prêt pour creative-brief-composer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite Phase B avant de lancer Step 0. Court-circuit (Phase A + Phase B) autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set ou si opérateur a flag `--no-disclosure` explicit OR si N usages successifs >= seuil expert (`auto_skip_after_n_calls` true). Sinon · disclosure 2 phases obligatoire canon v2.79.3 + v2.79.5.

Cross-ref doctrines racine `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5.

---

## Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ · orchestrateur 7 paliers · 30-90 min · gates intermédiaires + Gate A + Gate B). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement disclosure pré-engagement NIVEAU 0 en amont et Phase Output Atlas Visibility matricielle (NIVEAUX 1-4) en aval.

Pattern obligatoire · l'agent chairman verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique la brand entière et orchestre les handoffs sub-skills, en prose narrative sobre (zéro matrice ASCII en LIVE · les matrices viennent en Phase Output Atlas Visibility post-Step 8).

**2 niveaux d'abstraction obligatoires** ·

1. **Macro brand entière** · verbaliser la compréhension du périmètre stratégique global AVANT de rentrer dans le détail palier par palier.
   Exemple build-atlas-complete · "On part d'une brand qui s'adresse à {audience macro depuis brand.json existing ou snapshot}, qui opère sur {marché × stade Schwartz inféré sophistication}, qui propose {portfolio produits N hero + secondaires + entries détectés}. Le pattern catalogue cohérent · {hero positionne sur axe X · secondaires drainent vers Y · entries servent porte d'entrée Z}. Le business model est {DTC pure / subscription / hybrid} parce que {signaux scrape + offers encoded}. Mon hypothèse de territoires créatifs candidats à scorer · {3-5 axes potentiels visibles depuis specs × audiences mère}. Les angles vont probablement se cristalliser autour de {tension principale brand × pain audience-hero détecté reviews tagged Phase 2}."

2. **Micro chaînes audiences/angles cross-encoded phrasé** · verbaliser les chaînes parent/enfants + angle-fit pendant l'orchestration palier par palier.
   Exemple build-atlas-complete · "Cette audience-mère {nom · cardinality broad} se découpe en {N sous-poches détectées · entry doors distinctes · pain × consequence × deep chain phrasé} → pour chaque sous-poche · pain prioritaire {PNT-NN nom phrasé} → mécanisme reframe candidat {angle-formula Obs+Tension+Reframe+Bridge phrasé} → bénéfice 3 couches qui cible {functional · emotional · identity phrasé pourquoi cette couche dominante audience-side} → angle ranked top {score qualitatif phrasé · pas chiffre brut} → territoire créatif qui cristallise {axe macro phrasé · cohérent positioning brand}."

**Calibration narrative** · prose sobre · registre pair senior expert chairman · zéro jargon plumbing (jamais `score-matrix#axe_id`, `angle.lineage.pain_ref`, `_field_types`, Task tool mechanics en LIVE) · zéro tableau ASCII en LIVE (matrices = Phase Output Atlas Visibility post-Step 8 + Step 9 close). Adapter le tonal au registre opérateur détecté (grounded · standard · dense). Le narrating chairman entre paliers reste préservé (cf section Tone "structure prête… snapshot lancé… audiences cartographiées…") · le NIVEAU LIVE l'enrichit en thinking aloud expert substantif spécifique au cas brand, pas seulement transition de phase.

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger entre handoffs sub-skills si l'agent part dans une mauvaise direction d'inférence (mauvaise audience-hero priorisée · mauvais angle-fit détecté · mauvais territoire candidat émergent) AVANT que les paliers downstream consomment 30+ min, (b) pédagogie · il apprend la posture stratégique experte chairman en regardant la manière de penser un atlas paid DTC end-to-end (macro positioning → audiences cartography → angles cristallisés → territoires scorés cohérents).

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

---

## Expert methodology

**Canonical expert persona**: senior strategic director at a paid-acquisition agency, briefing a brand from blank URL to deployable territoire substrate in one sitting. Owns the chain, validates at each gate, lifts the operator's view to project altitude when uncertainty surfaces. Briefs+créas production handed off post-atlas to `creative-brief-composer`.

**Framework**: sequential territoire substrate chain en **4 paliers progressive cartography** (v1.4.0 v2.68 doctrine `docs/system/progressive-cartography-doctrine.md`) avec **gates light entre paliers** + Gate A audiences + Gate B angles preserved après Phase 4. Confidence chain propagated phase-by-phase per `docs/system/confidence-propagation.md`. Investigation Posture enforced on the final operator-facing synthesis per `docs/system/investigation-posture.md`. Scope discipline per `docs/system/territory-doctrine.md` (v2.67).

**Paliers progressive cartography v1.4.0** ·
- **Palier Phase 1+2** · snapshot-brand chain (structure + URL scan · ~10-15 min)
- **Gate intermédiaire 1** · territoire produit + offers + brand identity validation
- **Palier Phase 3** · map-audiences hiérarchique parent/enfants 3 niveaux mère + sous-poches (4 questions framework canon · ~15-20 min)
- **Gate intermédiaire 2** · arbre audiences validation (drop / ajoute / valide avant enrichissement)
- **Palier Phase 4** · mine-voc × N audiences + profile-audience × N (enrichissement per audience · pain_points + objections + JTBD canon V3 8 dimensions · ~30-45 min)
- Phase 5-9 preserved · weight-dimensions, produce-paid-angles (Gate B), score-matrix, stage territories, close

**Matrix**:

| Phase | Skill delegated | Subagent? | Gate before next phase |
|---|---|---|---|
| 0. Pre-flight (DRGFP) | inline | n/a | brand_slug present, URL or snapshot ready, MCP layer detected, `--fast-track` flag check |
| **Palier 1+2** | | | |
| 1. Structure + identity | `setup-brand` | No (conversational) | brand.json filled with name + language + sector |
| 2. URL snapshot | `snapshot-brand` (Task, includes Phase 1 macro + Phase 2 drilling gate) | Yes | spec.json + offers.json + profile.json draft at 60% |
| **GATE INTERMÉDIAIRE 1** (light · v1.4.0) | inline operator validate | n/a | Territoire produit + offers + brand identity posé · validation/correction binaire avant Phase 3 audiences |
| **Palier 3** | | | |
| 3. Map audiences (hiérarchique parent/enfants) | `map-audiences` (Task brand-wide) | Yes | N audiences mère + sous-poches proposed, 4 questions framework canon |
| **GATE INTERMÉDIAIRE 2** (light · v1.4.0) | inline operator validate | n/a | Arbre audiences validation · drop X / ajoute Y / valide avant Phase 4 enrichissement |
| **Palier 4** | | | |
| 4a. Mine VoC per audience | `mine-voc` (Task per audience validée) | Yes | pain_points + objections sub-audience populated, verbatim_quotes corpus |
| 4b. Profile audience per audience | `profile-audience` (Task per audience validée) | Yes | profile.json enriched JTBD canon V3 8 dimensions + psychology + voice + behavior + decision_process |
| **GATE A** (preserved v1.3.0) | inline operator validate | n/a | Operator accepts / corrects audiences enrichies |
| 5. Weight dimensions | `weight-dimensions` (Task brand-wide) | Yes | Audience-angle compatibility scores pre-computed (internal) |
| 6. Paid angles | `produce-paid-angles` (Task per top-3 audience) | Yes | Angles ranked per audience (formula Obs+Tension+Reframe+Bridge) |
| **GATE B** (preserved v1.3.0) | inline operator validate | n/a | Operator accepts / corrects ranked angles |
| 7. Score matrix | `score-matrix` (Task brand-wide) | Yes | Profil × Source d'angle matrix, top 3 axes créatifs selected |
| 8. Stage territories | inline (substrate review) | n/a | Territories staged as proposals, ready for downstream production |
| **8.5. Atlas Visibility Matriciel (NEW v1.6.0)** | inline (synthèse cross-atlas) | n/a | 4 niveaux canon · Décomposition produit · Many-to-many pain × audience · Stage business filter · Méthode pédagogique verbale |
| 9. Close | inline (Investigation Posture 5 sections) | No | Synthesis delivered, no orphan close, handoff to `creative-brief-composer` proposed |

**Mode `--fast-track`** · si flag `--fast-track` passed OR `operator/profile.json#preferences.auto_validate_after_n_brands` true détecté → skip Gate intermédiaire 1 + Gate intermédiaire 2 (auto-validate silent log). Gate A + Gate B preserved (structural decisions audiences finales + angles ranked). Default = gates light visible (premier-contact opérateur garde repère cognitif).

**Variables tracked**:
- `url_available` (bool) · drives whether Phase 2 runs or skips with confidence degradation
- `audience_count_validated` (int) · caps Phase 6 and Phase 7 cardinality (top-3 per default)
- `axe_creatif_count_selected` (int) · caps Phase 7 scoring output (top-3 axes créatifs per default)
- `confidence_floor` (float internal) · propagates worst-case across phases; never surfaced
- `mcp_layer` (set: facebook-graph, notion, none) · drives Phase 3 source breadth

**Failure modes**:
- Phase 1 (setup-brand) aborts mid-flow → persist `brands/{slug}/session-state.md`, allow resume via `resume-session`. Never restart from zero.
- Phase 2 (snapshot) fails (URL 404, JS-heavy, paywalled) → degrade gracefully: skip Phase 2, surface confidence drop to operator, continue downstream phases with declared-only data.
- Phase 3 (deepen) returns thin material (no Reddit, no Trustpilot reviews available) → flag as "Inconnu" in final synthesis, propose `mine-voc` ticket as Lever.
- Gate A or B operator rejects all proposals → pause pipeline, route to standalone `profile-audience` or `produce-paid-angles` for manual rework, do not silently kill chain.
- Phase 7 (score-matrix) finds zero viable axe créatif → surface honestly, propose alternative routes (expand audiences, re-mine VoC for missed angles).

---

### Step 0 · DRGFP Manifest Registry Scan (NEW v2.75.0)

Pre-flight discovery NEW entities scaffolded via scaffold-extension v1.2.0+ · 
scan `_extensions.json` OR `_manifest.json#extensions` pour entities avec 
`consumable_by: [{skill_name}]` matching CE skill.

Pour chaque NEW entity registered matching extension_hooks frontmatter ·
- Match `entity_type` ∈ frontmatter `extension_hooks` enum
- Match `consumable_by` field registry contains `{skill_name}` 
- Include NEW entity dans inputs Phase 1 pipeline ci-dessous
- Output enrichi avec lineage extension consommée dans atome_irreductible

Halt si NEW entity registered sans `consumable_by` field flagué (scaffold-extension v1.2.0 legacy) · 
silent skip · pas error · l'opérateur peut patcher manuellement le scaffold-extension Phase 9 register-and-flag pour ajouter `consumable_by`.

Cross-ref doctrine canon · `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW.

---

## Step 0 · Pre-flight (DRGFP)

Check operator provided minimum context. Apply Dependency Resolution & Gap-Filling Protocol L1 → L2:

- **brand_slug** required. If absent → ask via AskUserQuestion: *"Sur quelle marque je build l'atlas complet ?"*.
- **URL** or **existing snapshot**. If neither, mark `url_available = false` and warn confidence will degrade. If operator typed *"build atlas {brand}"* without URL on a blank workspace, ask once: *"Tu as une URL pour pré-remplir, ou je travaille en blind (purement déclaratif) ?"*.
- **MCP layer detection**: silent check `.mcp.json` for `facebook-graph` (Meta benchmarks) and `notion` (existing strategic memos). Populate `mcp_layer`. Surface only if operator asks.
- **Fast-track flag check (v1.4.0)** · check si flag `--fast-track` passed dans invocation OR `operator/profile.json#preferences.auto_validate_after_n_brands` true détecté. Si oui → mark `fast_track = true`, log silent ("opérateur expert détecté · gates intermédiaires bypass auto-validate · Gate A audiences + Gate B angles preserved"). Si non → mark `fast_track = false`, gates intermédiaires light visible default.

Announce the pipeline (chairman posture, no jargon, no skill names):

> *"OK, atlas complet de {brand}. Pipeline territoire substrat en 4 paliers progressive · Phase 1+2 structure + scan site, Phase 3 cartographie audiences (mère + sous-poches), Phase 4 enrichissement voix client per audience. Gates light entre paliers où tu valides au passage. Puis Phase 5-7 angles paid + scoring. Deux gates structurels (audiences enrichies puis angles ranked). 30 à 90 min selon la densité. Je pilote, tu valides aux gates. Une fois l'atlas posé, on enchaîne sur briefs+créas via `creative-brief-composer` sur l'axe créatif que tu choisis. Go ?"*

Si `fast_track = true` · ajouter une ligne *"Mode opérateur expert détecté · gates intermédiaires bypass auto-validate, on s'arrête seulement sur Gate A (audiences finales) + Gate B (angles ranked)."*

Hold for go-ahead, then proceed.

---

## Step 1 · Delegate `setup-brand` (inline, conversational)

**NEVER** spawn as subagent (`setup-brand.subagent_safe: false`). Invoke inline. Let it run its full conversational flow.

Pass context: operator-provided name/URL, detected profile (from `operator/profile.json`), language preference.

**Gate to Phase 2**: `brands/{slug}/brand.json` exists with `identity.name` and `identity.language` filled, OR operator explicitly deferred structure creation.

---

## Step 2 · Delegate `snapshot-brand` via Task tool

**If** `url_available = true` AND `snapshot-brand.subagent_safe: true`:

Spawn subagent via Task tool:
- `model: sonnet`
- Input: brand slug, URL
- Expected: `brands/{slug}/spec.json`, `brands/{slug}/products/{p}/offers.json`, `brands/{slug}/audiences/{a}/profile.json` drafts via stage-proposal pipeline

**CRITICAL · stage-before-ask is enforced through the subagent.** snapshot-brand SKILL.md mandates `.skills/stage-proposal.py` before any operator-facing proposal. This orchestrator inherits that rule by delegation. If the subagent ever skips staging and tries direct write, it hits the workflow gate. Do not retry a gated write; surface the gate message and wait for operator confirmation.

**Operator-facing line**:

> *"Je scanne le site pendant qu'on continue."*

Surface snapshot Step 7 synthesis paragraph when it returns (4-6 sentences, prose canon). Do not re-summarize.

**If `url_available = false`** → skip Phase 2, log `confidence_floor` drop, continue with declared-only context.

---

## GATE INTERMÉDIAIRE 1 · Phase 1+2 drilling validation (light · v1.4.0)

**Gate light** entre Palier Phase 1+2 (snapshot-brand) → Palier Phase 3 (map-audiences). Format canon doctrine `docs/system/progressive-cartography-doctrine.md` Section 8 Pattern gates light · 1-2 lignes synthesis + 1 binaire validation/correction. Pas Q&A verbeux.

**Si `fast_track = true`** · skip ce gate · auto-validate silent log ("Gate 1 bypass auto-validate · territoire produit + offers posé"). Continue direct Palier Phase 3.

**Si `fast_track = false`** (default) · surface synthesis 1-2 lignes + AskUserQuestion binaire ·

> *"Phase 1+2 drilling complete · territoire produit + offers + brand identity posé ({N produits · M offers · positioning détecté). Tu valides ou corriges avant qu'on attaque cartographie audiences ?"*

Options ·
- "Valide, on attaque cartographie audiences"
- "Corrige · {détail produit/offer/identity off}"

Si corrige → route correction inline (write_to_context mode proposed sur field concerné) puis re-surface gate. Si valide → proceed Palier Phase 3.

**NEVER** proceed Palier Phase 3 sans validation (gate light visible default) OR sans `fast_track = true` (opt-in auto-validate).

---

## Step 3 · Delegate `map-audiences` via Task tool (Palier Phase 3 hiérarchique)

**Refactor v1.4.0** · Phase 3 cartographie audiences hiérarchique parent/enfants 3 niveaux mère + sous-poches via `map-audiences` (4 questions framework canon doctrine `docs/system/progressive-cartography-doctrine.md` Section 5). Remplace ancien Step 3 deepen-brand-context (chain mine-voc + mine-vom upfront) qui a été déplacé vers Palier Phase 4 enrichissement per audience validée.

`map-audiences` is `subagent_safe: true`. Spawn single subagent brand-wide.

Pass context:
- brand slug
- territoire drilling Phase 2 (spec.json + offers.json + brand.json identity)
- mode: `hierarchique` (3 niveaux mère + sous-poches default)

For execution:
- `model: sonnet`
- Input: brand slug, snapshot Phase 2 output
- Expected: arbre audiences mère + sous-poches (hiérarchique parent/enfants 3 niveaux) avec 4 questions framework canon (qui? quoi? pourquoi? quand?) appliquées par audience

**Operator-facing line**:

> *"Je cartographie les audiences hiérarchique mère + sous-poches."*

When map-audiences returns, synthesize at orchestrator level into a single arbre audiences tableau (mère × sous-poches × confidence chain). **NEVER** dump raw subagent output verbatim per delegation pattern §synthesis layer.

---

## GATE INTERMÉDIAIRE 2 · Phase 3 audiences cartography validation (light · v1.4.0)

**Gate light** entre Palier Phase 3 (map-audiences hiérarchique) → Palier Phase 4 (enrichissement per audience). Format canon doctrine `docs/system/progressive-cartography-doctrine.md` Section 8 Pattern gates light.

**Si `fast_track = true`** · skip ce gate · auto-validate silent log ("Gate 2 bypass auto-validate · arbre audiences posé"). Continue direct Palier Phase 4.

**Si `fast_track = false`** (default) · surface synthesis 1-2 lignes + AskUserQuestion binaire ·

> *"Phase 3 cartographie audiences complete · {N} audiences mères + sous-poches posées. Tu valides l'arbre · drop X · ajoute Y · ou on attaque Phase 4 enrichissement ?"*

Options ·
- "Valide l'arbre, on attaque Phase 4 enrichissement"
- "Drop {audience X} · re-trim arbre"
- "Ajoute {audience Y} · enrichir arbre"

Si drop/ajoute → route correction inline (map-audiences refine targeted) puis re-surface gate. Si valide → proceed Palier Phase 4.

**NEVER** proceed Palier Phase 4 sans validation (gate light visible default) OR sans `fast_track = true`.

---

## Step 4 · Palier Phase 4 enrichissement per audience (mine-voc × N + profile-audience × N)

**Refactor v1.4.0** · Palier Phase 4 enrichissement per audience validée Gate Intermédiaire 2. Chain `mine-voc` × N audiences + `profile-audience` × N audiences (parallel cap 3 par delegation pattern). Remplace ancien Step 4 profile-audience standalone qui shootait à partir cross-signals upfront (vs audiences validées operator post Gate Intermédiaire 2 v1.4.0).

**Sub-step 4a · `mine-voc` per audience validée** ·

`mine-voc` is `subagent_safe: true`. Spawn one subagent per audience validée Gate Intermédiaire 2 (cap 3 parallel).

For each audience:
- `model: sonnet`
- Input: brand slug, audience id
- Expected: pain_points + objections sub-audience populated · `audiences/{a_slug}/pain_points/*.json` (PNT-NN entities) + `audiences/{a_slug}/objections/*.json` (OBJ-NN entities)

**v1.2.0 ontologie sémantique pure v2.64 · sub-parent locations.** Phase 4 mine-voc écrit dans sub-parent locations (owned natif par parent path) ·

- `brands/{slug}/audiences/{a_slug}/pain_points/*.json` (PNT-NN entities · formulation + verbatim_quotes + emotion + trigger + severity + chain + confidence_chain · audience owner implicite via parent path, pas de array affected_audiences[])
- `brands/{slug}/audiences/{a_slug}/objections/*.json` (OBJ-NN entities · formulation + type + frequency + severity + lifecycle_stage + response_counter + derived_angle_refs · audience owner implicite)
- `brands/{slug}/products/{p_slug}/frictions/*.json` (FRC-NN entities · formulation + type + signals · product owner implicite via parent path · NEW canonical layer for product-bound frictions sub-product)

**Backward compat strict additif** · fallback transparent top-level v2.63 (`pain_points/` + `objections/` + `frictions/` avec affected_audiences[]/affected_products[]) + profile sub-fields v1.7 preserved si brand brownfield.

**Sub-step 4b · `profile-audience` per audience validée** ·

`profile-audience` is `subagent_safe: true`. Spawn one subagent per audience validée (cap 3 parallel · run après mine-voc 4a complete pour enrichir profile avec verbatim_quotes corpus).

For each audience:
- `model: sonnet`
- Input: brand slug, audience id, mine-voc output (pain_points + objections sub-audience)
- Expected: full profile.json with JTBD canon V3 8 dimensions + identity + psychology + voice + behavior + decision_process · confidence chain explicit per axis · observed/déduit/déclaré sourcing tags

**Operator-facing line**:

> *"Je mine la voix client puis enrichis les profils audiences validées en parallèle. ~30-45 min en arrière-plan."*

When all 4a + 4b return, synthesize at orchestrator level into a single audience enrichi tableau (mère × sous-poches × pain_points + objections + JTBD × confidence chain). **NEVER** dump raw subagent output verbatim per delegation pattern §synthesis layer.

---

## GATE A · Operator validates audiences enrichies (preserved v1.3.0)

**MANDATORY GATE** before Phase 5. Surface the audience tableau, then AskUserQuestion:

- "Valide les audiences proposées, je continue sur les angles"
- "Corrige/affine d'abord, j'ouvre un drill sur {audience X}"
- "Stop, je veux relancer la voix client avant"
- "Autre"

If operator picks corrige → route to standalone `profile-audience` with focus, hold orchestrator state in `session-state.md`, resume on operator signal.

If operator picks stop → pause chain, route to `mine-voc` standalone.

**NEVER** proceed to Phase 5 without explicit validation. Audiences gate the entire downstream because Phase 5-9 fan out per audience.

---

## Step 5 · Delegate `weight-dimensions` via Task tool (brand-wide)

`weight-dimensions` is `subagent_safe: true`, `operator_facing: false`. Single subagent, brand-wide.

- `model: sonnet`
- Input: brand slug, validated audiences from Gate A
- Expected: internal audience × angle compatibility scores written to brand state (not exposed)

**Operator-facing line**:

> *"Je pré-compute les compatibilités angle × audience."* (one line, no detail)

**NEVER** surface raw numeric scores to operator. Compositional Cartography §7 enforcement.

---

## Step 6 · Delegate `produce-paid-angles` via Task tool (per top-3 audience)

`produce-paid-angles` is `subagent_safe: true`. Spawn one subagent per top-3 validated audience.

For each audience:
- `model: sonnet`
- Input: brand slug, audience id, weight-dimensions output
- Expected: angles ranked per audience using formula Obs + Tension + Reframe + Bridge, sourced from VoC verbatims where possible

**Operator-facing line**:

> *"Je génère les angles paid pour chaque audience top."*

When all return, synthesize into a per-audience angles tableau. Surface the top angle per audience with a 1-line rationale anchored on observed tension. **NEVER** expose internal scoring numbers.

---

## GATE B · Operator validates angles

**MANDATORY GATE** before Phase 7. Surface the angles tableau, then AskUserQuestion:

- "Valide les angles top, je continue sur les territoires + briefs + créas"
- "Corrige/affine, un angle est off sur {audience X}"
- "Stop, je veux re-mine VoC avant de produire les briefs"
- "Autre"

Same rejection logic as Gate A. **NEVER** proceed to Phase 7 without explicit validation. Angles gate briefs+créas because Phase 8-9 fan out per priority angle.

---

## Step 7 · Delegate `score-matrix` via Task tool (brand-wide)

`score-matrix` is `subagent_safe: true`, `operator_facing: true`. Single subagent, brand-wide.

- `model: sonnet`
- Input: brand slug, validated audiences (Gate A), validated angles (Gate B), weight-dimensions output
- Expected: Profil × Source d'angle matrix scored via canonical scoring, top-3 axes créatifs selected

**Operator-facing line**:

> *"Je build la matrice complète et je remonte les axes créatifs prioritaires."*

When subagent returns, surface only the **top-3 axes créatifs named in operator language** with prose rationale per axe (1-2 sentences anchored on audience tension + angle source). **NEVER** expose the full matrix grid with raw numbers. Compositional Cartography §7.

**Disambiguation lexicon v2.67** · "axe créatif" (micro · output score-matrix) vs "territoire" (macro · substrat atlas). Surface "axes créatifs" pour l'output ranking en Step 7. Le territoire macro = l'atlas substrate entier. Voir `docs/system/territory-doctrine.md`.

---

## Step 8 · Review & stage territories for downstream production

Territories prioritized (top-3 axes créatifs par score-matrix Step 7). Substrate complete. Atlas posé.

Next phase (outside this orchestrator) · materialize briefs + creatives via `creative-brief-composer` skill (separate invocation · operator chooses which axe créatif to materialize first).

**Operator-facing line**:

> *"Atlas substrat posé. 3 axes créatifs ranked. Prêt pour la phase production briefs+créas."*

---

## Phase Output Atlas · Visibility Matriciel Multi-niveau (canon v2.78.2)

**MANDATORY** post-encoding entités · présenter synthèse matricielle multi-niveau canon doctrine `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2 AVANT le Step 9 Close (Investigation Posture). Sans cette Phase, l'opérateur ne voit jamais la vue d'ensemble matricielle (product × pain × audience × positionnement × stage business) · output atlas reste prose-only · invalid.

Après encoding toutes entités atlas (brand · products · audiences · pains · objections · frictions · angles · offers · learnings · strategy), présenter OBLIGATOIREMENT synthèse matricielle multi-niveau canon decomposition-visibility-discipline v2.78.2.

### NIVEAU 1 · Décomposition produit cross-products

Pour chaque produit · table compacte décomposition specs · mécanismes · bénéfices 3 couches canon `docs/system/pain-benefit-chain.md` (functional · emotional · identity, layer chargé identifié explicit) ·

```
PRODUCT [name]
SPECS               MÉCANISMES                BÉNÉFICES 3 couches
[atome 1]           [atome action 1]          Functional · [bénéfice]
[atome 2]           [atome action 2]          Emotional  · [bénéfice]
                                              Identity   · [bénéfice]
                                                          ← layer chargé
```

Itérer pour les N produits encoded brand. Si produit unique · une table. Si multi-produits · N tables compactes empilées (séparateur visuel entre).

### NIVEAU 2 · Many-to-many · pain × audience matrix cross-atlas

Matrice ASCII OBLIGATOIRE cross-products + cross-audiences · skip = invalid output. Décompose explicitement quelle douleur frappe quelle audience avec intensité primary vs secondary ·

```
                       Audience-1    Audience-2    Audience-3   Audience-N
                       (slug)        (slug)        (slug)       (slug)
PNT-01 [pain label]      ✓✓ PRIMARY      ·            ✓           ·
PNT-02 [pain label]         ·         ✓✓ PRIMARY      ·           ✓
PNT-03 [pain label]         ✓             ✓        ✓✓ PRIMARY     ·
PNT-NN ...
─────────────────────────────────────────────────────────────────────
Espace blanc paid          ·         INCONTESTÉ      ·            ·
(compétitif intel)                   (5 concurrents
                                      sur axe unique)
```

Légende canon · `✓✓ PRIMARY` (douleur dominante audience) · `✓` (douleur secondaire affecte audience) · `·` (zéro affect). Row `Espace blanc paid` (optional · ship si signal compétitif détecté Phase 6 produce-paid-angles) · pour chaque audience, repère où concurrence est faible/inexistante sur l'angle → opportunité paid prioritaire.

### NIVEAU 3 · Positionnement filtre par stage business

Stage business détecté (signal ARR estimée · proof points · domain age · funding signals) OU opérateur-déclaré. Table canon ·

```
STAGE détecté            [early | growth | scale]
ARR estimée              [signal range]

AUDIENCE PRIORITAIRE     [audience slug + rationale 1 ligne]
ANGLES DOMINANTS         [3-5 angle ids ranked top]
POSITIONING STATEMENT    [Moore format si produce-positioning-canvas
                          shipped v2.80 · sinon stage hypothèse 1 ligne]

Distinction critique opérateur ·
Audience produit-fit     [toutes audiences encoded · ex audience-1 · audience-2 · audience-3]
Audience ciblage créa    [filter sub-set selon positioning targeting · ex audience-2 only stage early]
```

**HR · Stage business filter obligatoire si signal détectable.** ARR signal absent ET proof points absents ET domain age inconnu → flag `stage = inconnu` · ne pas inventer. Sinon · stage déclaré explicit.

**HR · Distinction explicit audience produit-fit vs ciblage créa.** Audience produit-fit = toutes audiences encoded Phase 4 (pertinentes pour le produit). Audience ciblage créa = sub-set filtré par positionnement stage-aware (ex · stage early → ciblage early adopters only, growth/scale audiences seront produit-fit mais pas ciblage créa runtime). Confusion = leak runtime · opérateur dépense paid sur audiences hors ciblage stage.

### NIVEAU 4 · Méthode pédagogique verbale

Verbaliser méthode décomposition canon · l'opérateur sait COMMENT l'atlas a été construit, pas seulement QUOI ·

> *"J'ai cartographié l'atlas {brand} en 4 niveaux canon ·*
> *1. Décomposition produit · specs/mécanismes/bénéfices 3 couches (functional · emotional · identity, layer chargé identifié)*
> *2. Many-to-many · {N} pains × {M} audiences (matrix primary/secondary affectations · espace blanc paid si signal compétitif)*
> *3. Stage business · {stage détecté} → audience prioritaire {slug} · {3-5 angles dominants}*
> *4. Positionnement filter · {produit-fit toutes audiences} vs {ciblage créa sub-set stage-aware}*
>
> *L'atlas est désormais opérable cross-skills downstream · `produce-paid-angles` · `creative-brief-composer` · `compose-creative`. Validation systémique opérée par confidence chain explicit cross-entity."*

**HR · Méthode pédagogique verbale obligatoire post-matrices.** Skip = opérateur ne sait pas comment l'atlas a été construit · runtime downstream skills consomment l'atlas en aveugle · debugging downstream impossible.

---

## Step 9 · Close (Investigation Posture, 5 sections MANDATORY)

**CRITICAL**: this is a strategic deliverable orchestrator, not a setup orchestrator. Investigation Posture is mandatory per `docs/system/investigation-posture.md`. Five sections explicit:

### Observé
What the pipeline produced, sourced. Audiences validated at Gate A, angles validated at Gate B, top-3 axes créatifs selected by score-matrix. Quantify (number of audiences, number of angles per audience, number of axes créatifs ranked). Never expose scoring numbers.

### Déduit
Hypotheses with explicit confidence chain. Examples per atlas type:
- "L'audience mère **{name}** ressort comme prioritaire (confidence **forte** · convergence VoC + VoM)."
- "L'angle **{name}** sur l'audience **{name}** porte le plus de tension observée (confidence **moyenne** · verbatims solides mais sample size limité)."
- "L'axe créatif **{name}** combine audience à haut volume + angle peu exploité par les concurrents (confidence **moyenne** · projection à valider en test)."

Confidence chain: **forte** / **moyenne** / **faible** / **TRÈS faible**. Never invent confidence. Never present hypothesis as fact.

### Inconnu
Variables non observables sans test live ou data additionnelle. Examples:
- "Volume réel de l'audience mère sur Meta (non mesurable sans audience-builder test)."
- "Performance comparative des angles sur le marché actif (non mesurable sans déploiement budget test)."
- "Sensibilité prix au-delà du tier offers.json actuel (non mesurable sans split-test landing)."

### Leviers
Skills / actions / sources pour lever les inconnues. Examples:
- "Test campagne Meta sur l'audience mère + 2 angles top (skill `audit-meta-account` post-déploiement)."
- "Mine VoC additionnel sur source spécifique (skill `mine-voc --focus={axis}`)."
- "Refine angles si Gate B a laissé des hypothèses floues (skill `produce-paid-angles --focus={audience}`)."

### Close ouvert
**UNE seule question macro**. L'opérateur arbitre la prochaine direction (production briefs+créas downstream ou enrichissement territoire substrat). Example canonical v1.3.0:

> *"Sur quel axe créatif tu veux qu'on matérialise d'abord briefs + créas via `creative-brief-composer` · T1 · T2 · T3 ? Ou tu veux d'abord enrichir le territoire (mine-voc supplémentaire · profile-audience drill · etc.) ?"*

**NEVER** orphan close. **NEVER** flat menu. **NEVER** more than one question.

---

## Step 10 · Finalize

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
python3 .skills/build-brand-snapshot.py {slug}
```

Update status.json:
- `last_atlas_build_run`: timestamp
- `atlas_substrate_complete`: true
- `audiences_count`, `angles_count`, `axes_creatifs_count`
- emit `atlas_substrate_staged` event

Trigger `learn-from-session` batch (posture adaptive, operational/ship register): briefer 5-7 bullets max sur ce qui a été produit (territoire substrat, pas briefs+créas), close binaire ("1 arbitrage à faire" = Close ouvert macro, ou "RAS, atlas posé, prêt pour `creative-brief-composer`").

---

## Operator cartography (before Phase 0, if complex brief)

If the operator typed a minimal brief ("build atlas {brand}") without context, briefly cartograph the pipeline before executing (~5 lines, operator language, no system jargon):

> *"Analysé. Atlas substrat complet en 4 paliers progressive cartography, voilà comment je vais piloter :*
> *• **Palier 1+2** · structure ta marque + scan le site. **Gate light** entre les paliers : tu valides territoire produit + offers*
> *• **Palier 3** · cartographie audiences hiérarchique mère + sous-poches. **Gate light** : tu valides l'arbre*
> *• **Palier 4** · mine voix client + enrichis les profils audiences validées. **Gate A** : tu valides audiences enrichies*
> *• Produits les angles paid ranked par audience. **Gate B** : tu valides les angles*
> *• Build la matrice complète et remonte les top-3 axes créatifs ranked*
> *• Clôture avec un drill-down · soit on enchaîne briefs+créas via `creative-brief-composer` sur l'axe que tu choisis, soit on enrichit le territoire d'abord"*

Si `fast_track = true` détecté · *"Mode opérateur expert · gates light intermédiaires bypass auto-validate, stop seulement Gate A + Gate B."*

Then AskUserQuestion: *Go / Skip URL scan / Active fast-track / Ajuste le pipeline (skip une phase) / Autre*.

---

## Guardrails

- **HR-NEW · Phase output Atlas Visibility Matriciel obligatoire (v1.6.0)** · post-encoding entités atlas (brand · products · audiences · pains · objections · frictions · angles · offers · learnings · strategy) · Phase Atlas Visibility 4 niveaux canon obligatoire AVANT Step 9 Close. Skip = invalid output (l'opérateur ne voit jamais la vue d'ensemble matricielle product × pain × audience × positionnement × stage business). Doctrine racine · `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2.
- **HR-NEW · 4 niveaux matriciels canon obligatoires (v1.6.0)** · NIVEAU 1 Décomposition produit cross-products · NIVEAU 2 Many-to-many pain × audience matrix cross-atlas · NIVEAU 3 Positionnement filtre par stage business · NIVEAU 4 Méthode pédagogique verbale. Skip 1 = invalid output.
- **HR-NEW · Many-to-many matrix cross-products + cross-audiences obligatoire (v1.6.0)** · ASCII matrix explicite avec `✓✓ PRIMARY` / `✓` / `·` symboles canon · skip = matrix implicite cross-products force opérateur à déduire affectations pain × audience.
- **HR-NEW · Stage business filter obligatoire si signal détectable (v1.6.0)** · ARR estimée + proof points + domain age + funding signals → stage déclaré explicit (early/growth/scale). Aucun signal détectable → flag `stage = inconnu` · NEVER inventer.
- **HR-NEW · Audience produit-fit vs ciblage créa distinction explicit (v1.6.0)** · audience produit-fit = toutes audiences encoded Phase 4 · audience ciblage créa = sub-set filtré par positionnement stage-aware. Confusion = leak runtime · opérateur dépense paid sur audiences hors ciblage stage. Skip = invalid output.
- **HR-NEW · Méthode pédagogique verbale obligatoire post-matrices (v1.6.0)** · verbaliser les 4 niveaux canon de cartographie atlas appliqués · skip = opérateur ne sait pas comment l'atlas a été construit · runtime downstream skills consomment en aveugle · debugging impossible.
- **AP-NEW · Encodage atlas silent sans synthèse matricielle finale (v1.6.0)** · NEVER ship atlas substrat sans Phase Atlas Visibility · `build-atlas-complete` v1.6.0+ MUST surface synthèse matricielle multi-niveau post-encoding entités.
- **AP-NEW · Synthèse prose-only sans Phase Atlas Visibility (v1.6.0)** · NEVER substitute Investigation Posture 5 sections Close (Step 9) en lieu de Phase Atlas Visibility matricielle (Step 8.5). Close consomme la synthèse matricielle en amont, ne la remplace pas.
- **AP-NEW · Many-to-many implicite cross-products (v1.6.0)** · NEVER force opérateur à déduire affectations pain × audience par inférence prose · ASCII matrix explicite obligatoire (NIVEAU 2 canon).
- **AP-NEW · Stage business absent du filtre positionnement (v1.6.0)** · NEVER skip stage filter si signal détectable · stage = inconnu acceptable seulement si zéro signal · NEVER inventer stage.
- **AP-NEW · Méthode pédagogique skip (v1.6.0)** · NEVER ship atlas matriciel sans verbaliser COMMENT l'atlas a été construit · l'opérateur perd la grammaire de raisonnement runtime.
- **HR · Gates entre Phases canon (v1.4.0)** · build-atlas-complete v1.4.0+ doit insérer **gate light entre Phase 2 (drilling) → Phase 3 (audiences hiérarchique) → Phase 4 (enrichissement)**. Anti-pattern · chain skills sans validation operator entre paliers progressive cartography (dump synthesis bloc canon précédent v1.3.0 où seuls Gate A + Gate B existaient). Doctrine `docs/system/progressive-cartography-doctrine.md` Section 8 Pattern gates light · format 1-2 lignes synthesis + 1 binaire validation/correction. Pas Q&A verbeux.
- **HR · Fast-track opt-in opérateur expert (v1.4.0)** · gates intermédiaires auto-validate **seulement si opérateur explicit** (flag `--fast-track` passed dans invocation) OR config opt-in (`operator/profile.json#preferences.auto_validate_after_n_brands` true détecté). Default = gates light visible. Premier-contact opérateur garde gates pour repère cognitif. Gate A + Gate B **toujours preserved** quel que soit le mode (structural decisions audiences finales + angles ranked, jamais bypass).
- **NEVER** run all phases sequentially blocking on one operator without heartbeat. Surface progress at each gate.
- **NEVER** skip Gate A or Gate B silently. Audiences gate angles, angles gate scoring. Skipping = fan-out on unvalidated hypotheses = wasted calls + low-quality atlas substrate.
- **NEVER** skip Gate Intermédiaire 1 or Gate Intermédiaire 2 sans `fast_track = true` opt-in explicit. Gates light visible default · premier-contact opérateur a besoin du repère cognitif entre paliers progressive.
- **NEVER** expose Task tool mechanics, subagent internals, or skill names to the operator ("I spawned profile-audience", "produce-paid-angles returned"). Say what it *does*: "je cartographie les audiences", "je génère les angles".
- **NEVER** re-implement subskill logic. If a subskill has a bug or gap, fix it there, not here. Pure orchestrator per `onboard-brand` precedent.
- **NEVER** expose raw scoring numbers, confidence floats, weight-dimensions matrix values, or internal field paths. Compositional Cartography §7 anti-pattern enforcement.
- **NEVER** freestyle prose for an output where a downstream skill exists. Skill routing canon v2.55 enforcement · invoke `produce-paid-angles`, never write angles in prose. The orchestrator delegates; it does not produce strategic content directly.
- **NEVER** produce briefs copy ou créas in this orchestrator (v1.3.0 territoire-pure scope). Briefs+créas materialization happens downstream via `creative-brief-composer` (separate skill, separate invocation). Voir `docs/system/territory-doctrine.md`.
- **NEVER** dump raw subagent output verbatim. The orchestrator main is the synthesis layer per delegation pattern.
- **ALWAYS** persist `brands/{slug}/session-state.md` rolling update after each phase (crash resumption).
- **ALWAYS** propagate confidence chain phase-by-phase per `docs/system/confidence-propagation.md`. Worst-case floor wins on the final synthesis.
- **ALWAYS** apply Investigation Posture 5 sections on Step 9 close. The audit gap that triggered v1.0.0 was exactly this missing structured close.
- **ALWAYS** respect parallel cap (3 subagents per phase) and depth cap (1 · `deepen-brand-context` already chains its own subagents, that is depth-2 already authorized by the architecture).
- **ALWAYS** Brand isolation: this orchestrator operates `brand_only` per `docs/system/brand-isolation-doctrine.md`. Cross-brand pulls (canon copy resources) are read-only references, never write to other brands.
- **One brand at a time.** No parallel atlas-build on multiple brands. Confuses Layer B mutation scoping.

---

## Cross-references

- `.skills/skills/onboard-brand/SKILL.md` · orchestrator pattern reference (purity rule, gate canon)
- `.skills/skills/setup-brand/SKILL.md` · Palier Phase 1 (Step 1)
- `.skills/skills/snapshot-brand/SKILL.md` · Palier Phase 1+2 (Step 2 · includes its own Phase 1 macro + Phase 2 drilling gate v1.4.0)
- `.skills/skills/map-audiences/SKILL.md` · Palier Phase 3 hiérarchique parent/enfants 3 niveaux mère + sous-poches (Step 3 v1.4.0 · 4 questions framework canon)
- `.skills/skills/mine-voc/SKILL.md` · Palier Phase 4 enrichissement per audience (Step 4a v1.4.0 · pain_points + objections sub-audience)
- `.skills/skills/profile-audience/SKILL.md` · Palier Phase 4 enrichissement per audience (Step 4b v1.4.0 · JTBD canon V3 8 dimensions)
- `.skills/skills/deepen-brand-context/SKILL.md` · legacy orchestrator (v1.3.0 Step 3 deepen chain · remplacé par map-audiences Step 3 + mine-voc/profile-audience Phase 4 v1.4.0)
- `.skills/skills/weight-dimensions/SKILL.md` · Phase 5
- `.skills/skills/produce-paid-angles/SKILL.md` · Phase 6
- `.skills/skills/score-matrix/SKILL.md` · Phase 7
- `.skills/skills/produce-strategy/SKILL.md` · invokable en post-Phase 9 close si l'opérateur veut cadrer le focus Q{n} sur la brand atlas-complete (strategy.schema v1.0 canon shipped v2.58)
- `.skills/skills/creative-brief-composer/SKILL.md` · downstream production briefs+créas post-atlas (separate invocation, operator chooses axe créatif)
- `docs/system/progressive-cartography-doctrine.md` · **NEW v2.68** · progressive cartography canon (Sections 3-7 phasing · Section 8 Pattern gates light) · doctrine source v1.4.0 refactor
- `docs/system/decomposition-visibility-doctrine.md` · **NEW v2.78.2 + v2.81.1+ NIVEAU LIVE** · doctrine canon racine 3 phases temporelles · AVANT exec NIVEAU 0 paramètres décomposés (v2.79.5) · PENDANT exec NIVEAU LIVE thinking aloud expert action LOURDE orchestrateur 2 niveaux abstraction macro + micro chaînes phrasé (v2.81.1+) · APRÈS exec NIVEAUX 1-4 matrices Atlas Visibility post-Step 8 (Décomposition produit cross-products · Many-to-many pain × audience cross-atlas · Stage business filter · Méthode pédagogique verbale · audience produit-fit vs ciblage créa distinction) · HR-DVD-11 + AP-DVD-11 enforcement
- `docs/system/pain-benefit-chain.md` · canon 3 couches bénéfices (functional · emotional · identity) · consume NIVEAU 1 Décomposition produit
- `.skills/skills/snapshot-brand/SKILL.md` v2.78.2 cohérent · sister skill encoding products + offers + brand identity (Phase 1+2 chain)
- `.skills/skills/profile-audience/SKILL.md` v2.78.2 cohérent · sister skill encoding audiences enrichies JTBD canon V3 8 dimensions (Phase 4b chain)
- `.skills/skills/define-specs/SKILL.md` v2.78.2 cohérent · sister skill décomposition produit specs/mécanismes/bénéfices (consume NIVEAU 1)
- `.skills/skills/produce-positioning-canvas/SKILL.md` (forward-compat v2.80 si shipped) · Moore positioning format pour NIVEAU 3 Positioning Statement
- `.skills/skills/define-brand-voice/SKILL.md` (forward-compat v2.80 si shipped) · 4D brand voice cohérence NIVEAU 3 positionnement
- `docs/system/territory-doctrine.md` · v2.67 · layer territoire scope canon (build-atlas-complete = substrat territoire only, productions briefs+créas downstream)
- `docs/system/investigation-posture.md` · 5-section close canon (Step 9 mandatory) · close ouvert Phase 4 vers production downstream via creative-brief-composer (out of scope build-atlas territoire-pure v1.3.0+)
- `docs/system/scope-extension-doctrine.md` · SED-X v2.65 · skill scope boundaries discipline
- `docs/system/canonical-matrix-reasoning.md` · CMR · production discipline (95% quality on intersectional outputs)
- `docs/system/compositional-cartography.md` · §7 anti-pattern (no raw numeric scoring to operator) · implémentation domaine créatif de CMR
- `docs/system/confidence-propagation.md` · confidence chain algebra
- `docs/system/brand-isolation-doctrine.md` · brand_only scope default
- `docs/system/skill-routing-doctrine.md` · v2.55 routing canon (orchestrator delegates, never freestyles strategic prose)
- `docs/system/delegation-pattern.md` · model routing + parallel caps
- `docs/system/contract-build.md` · Build mode rules + Orchestration gate
- `docs/system/voice.md` · operator-facing prose canon (3 movements, no bold-section anchors on synthesis paragraphs)
- `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW (extension_hooks + manifest registry scan canon)
- `scaffold-extension` v1.2.0+ Phase 9 register-and-flag (upstream registry NEW entities)

---

## Verdict v1.6.0

v1.6.0 ship orchestrator decomposition visibility refactor · NEW Phase Output Atlas Visibility Matriciel Multi-niveau insérée entre Step 8 stage territories et Step 9 Close Investigation Posture · 4 niveaux canon obligatoires (NIVEAU 1 Décomposition produit cross-products specs/mécanismes/bénéfices 3 couches functional/emotional/identity · NIVEAU 2 Many-to-many pain × audience matrix cross-atlas ASCII obligatoire avec espace blanc paid si signal · NIVEAU 3 Positionnement filtre par stage business early/growth/scale audience produit-fit vs ciblage créa distinction explicit · NIVEAU 4 Méthode pédagogique verbale). Doctrine racine `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2. Sister skills v2.78.2 cohérents (snapshot-brand · profile-audience · define-specs). Forward-compat sister skills v2.80 produce-positioning-canvas (Moore format NIVEAU 3) + define-brand-voice (4D). Backward compat strict additif · Phases 1-7 chain skills preserved · Step 8 stage preserved · Step 9 close preserved (Investigation Posture consomme synthèse matricielle Phase Atlas Visibility en amont · Observé section enrichie cross-niveaux).

## Verdict v1.4.0

v1.4.0 ship orchestrator progressive cartography refactor · chain skills avec gates light entre paliers progressive (Phase 1+2 snapshot-brand · gate intermédiaire 1 · Phase 3 map-audiences hiérarchique · gate intermédiaire 2 · Phase 4 mine-voc + profile-audience enrichissement per audience validée) · mode `--fast-track` opérateur expert bypass gates intermédiaires auto-validate (opt-in) · Gate A audiences + Gate B angles preserved structural · territoire substrat (specs + offers + profiles + pain_points + objections + angles + scoring + frictions + roadmap + strategy) end-to-end · productions briefs+créas via separate `creative-brief-composer` skill post-atlas downstream. Backward compat strict additif sur chain skills (Steps preserved · gates additifs light · fast-track flag opt-in default off).

## Verdict v1.3.0 (legacy)

v1.3.0 ship orchestrator territoire-pure · substrate atlas (specs + offers + profiles + angles + scoring + frictions + roadmap + strategy) end-to-end · productions briefs+créas via separate `creative-brief-composer` skill post-atlas downstream.
