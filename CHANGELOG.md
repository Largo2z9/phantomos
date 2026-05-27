# Changelog

All notable changes to PhantomOS workspace-template canon.

Format · [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning · [SemVer](https://semver.org/spec/v2.0.0.html).
Détails étendus par release · `docs/internal/releases/manifest/{version}-manifest.json`.
Archive narrative Largo · `docs/internal/project-journal.md`.
Doctrine canon · `docs/system/changelog-doctrine.md` (v2.83.0+).

## [2.88.0] · 2026-05-28
### Added
- **Sprint MINOR v2.88.0 · Foundation Creative Strategy workflow** · 4 patches foundation suite session externe Creative Strategy v3 orchestrée 25-27 mai 2026 (4 cycles convergence orchestrateur PhantomOS ↔ session externe)
- **Patch profile.schema.json v2.1 → v2.2** · ajout `psychology.big_idea` (string audience-scoped · 1-2 phrases pitch stratégique consommé par sous-workflow A étape A3 plan de cadrage + A6 conception axes créatifs) + `psychology.fears` (array of objects typés · fear_text + source_verbatim_ref + intensity_score 1-5 + confidence_chain v2.87.4 héritée · racines psychographiques blocantes distinctes de emotions état observable et pain_points problèmes fonctionnels)
- **Patch creative-mechanics-registry.md** · ajout champs `typology_st` (spatial/temporel obligatoire) + `temporal_subtype` (dialogique/démonstratif/narratif/pédagogique optionnel si temporel) au format fiche · mapping initial 34 mécaniques canon avec table consolidée fin de document (22 mécaniques spatial pur · 9 mécaniques temporel pur · 3 mécaniques variable selon support · versus + celebrity + before-after)
- **NEW doctrine docs/system/creative-axis-canonicalization-doctrine.md** · codifie hiérarchie créative 4 niveaux (brand promise optionnelle marque-globale · big idea audience-scoped persistée canon profile.psychology.big_idea · axe créatif niveau matriciel intermédiaire · créa instance ad finale individuelle) + mapping workflow A v3 Creative Strategy ↔ équation v3.1 NOYAU × CONTEXTE × MODIFIEURS (axe créatif = CONTEXTE layer enrichi avec typology_st + character_archetype + hook_pattern_default + narrative_direction · incarnation = NOYAU layer instancié · hook variant = variant_axis hook_swap canon creative.schema v1.2) + vocabulaire canon harmonisé 15 termes mappés + spec étape A2 consultation atlas canonique cascade v2.64 sub-audience → v2.63 top-level → v1.7 sub-field legacy + visualisers matriciel ASCII Output Clarity Doctrine v2.79.2+ enforced + 8 Hard Rules canon (HR-CAC-1 à HR-CAC-8) + 6 anti-patterns canonisés (AP-CAC-1 à AP-CAC-6) + cas anatomique Sereno fictif illustration visualiser A6
### Notes
- **Foundation atlas + vocabulary harmonization shipped** · sprint v2.88.1 livrera schema creative_axis.json + doctrine pre-gate-evaluator-doctrine.md · sprint v2.88.2 livrera skill orchestrator compose-creative-batch + patch compose-creative v1.9 mode incarnation_only + patch learn-from-session mode brief_strategy_intake
- **Cohérence canon ENRICH > CREATE strict respecté** · zéro skill nouveau dans v2.88.0 · patches ciblés sur schemas + registries + 1 nouvelle doctrine · pas refonte from scratch
- **Backward compat strict additif** · fields psychology.big_idea + psychology.fears optional en read v2.0+ profile · obligatoire en write si workflow Creative Strategy v2.88+ invoqué · creative-mechanics-registry typology_st champs optional en lecture · mapping table consolidée sert SSOT lookup en attendant back-fill fiches individuelles cycle maintenance futur
- **Test runtime cible Stepprs** · pilote PhantomOS atlas mature · pre-sprint enrichissement Stepprs atlas via mine-voc semi-auto sur corpus Trustpilot pour amorcer big_idea + fears · pas d'encodage opérateur manuel (posture canon Largo confirmée)
- **Convergence canon via 4 cycles débat orchestrateur** · 65% vocabulaire externe réinventait du canon existant · harmonisation décidée via cycles structurés · 3 vraies nouveautés identifiées et canonisées (big_idea audience-scoped persisté · typology_st spatial/temporel + temporal_subtype · evaluator-optimizer pattern · ce dernier différé v2.88.1)
- **Hiérarchie créative canon 4 niveaux** · ferme gap "comment passer requête opérateur DTC à assets publicitaires cohérents produits depuis atlas brand · qualité créative ne se joue pas dans production IA mais dans decomposition stratégique amont"
- Tests non-régression PASS · schema JSON valid post-patch · creative-mechanics-registry markdown structure préservée · doctrine CAC créée respecte format canon doctrines
- D#474 captured · NEW memory canon `creative_axis_canonicalization_v2_88_0` (hiérarchie 4 niveaux + mapping equation v3.1 + 8 HR-CAC à poser post-merge)

## [2.87.7] · 2026-05-24
### Changed
- **SMART PROMPTING · output-clarity runtime enforcement cross 5 skills heavy via ENRICH > CREATE canon** · pattern hypothesis-driven · zéro patch sur SKILL.md bodies · zéro nouveau fichier doctrine · zéro overengineer · wall-time réel ~1.5h vs scope original 10-14h refonte SKILL.md (gain 8-12h)
- **Enrichi mapping `operator-vocabulary-translation.md`** · 107 → 134 entries · +27 NEW entries spécifiques aux 5 skills heavy modernes · codes canoniques bruts (PNT-NN → label métier · OBJ-NN · ANG-NN · OFR-NN · FRC-NN · CRT-NN · AUD-NN · LRN-NN) · fichiers JSON (brand.json · offers.json · roadmap.json · learnings.json · profile.json → métier) · champs schema modernes (chain_level · mechanism_ref · target_audience[] · intent_mix · overlay_density · confidence_chain · dream_scenario_narrative · target_recipient · context_setting · social_payoff) · doctrines names internal (formule canon OTRB · pattern parent/enfants sémantique pure · 8 dimensions canon · investigation-posture 5 sections) · Hard Rules codes (HR-CC-CANON-1 · HR-CP-SED-1 · HR9 · AP-NN → retirés du rendu opérateur) · L1/L2/L3 fallback (auto · à toi · partiel) · enums techniques (solution_aware → cherche déjà solution · primary_buyer → acheteur direct · cycle hypothesis→tested→validated→scaled→fatigued → exploratoire→testé→validé→scalé→essoufflé) · scripts Python visibles · skill names heavy verbalized
- **Ajouté `output-clarity-doctrine` + `operator-vocabulary-translation` au consumes block frontmatter des 5 skills heavy** · build-atlas-complete + decompose-ad + map-audiences + craft-packshot + compose-creative · 10 lignes ajoutées total cross 5 skills · zéro patch sur SKILL.md bodies · enforcement runtime smart prompting via consume pattern
### Notes
- **Diagnostic post-audit 5 sub-agents Haiku parallèle** · ~460 occurrences jargon cumulé cross 5 skills heavy détecté · canon `output-clarity-doctrine` + `operator-vocabulary-translation` EXISTAIENT DÉJÀ mais (1) mapping incomplet pour jargons modernes + (2) 5 skills heavy ne CONSUME PAS ces canon dans leur frontmatter (gap systémique)
- **Pattern ENRICH > CREATE strict respecté** · zéro nouveau fichier · le mapping canon existait déjà · le gap était dans entries manquantes + propagation runtime cross-skills via consume pattern
- **Hypothesis-driven fail-fast** · soft enforcement via consume + mapping enrichi · pas hardcode runtime · attente réduction leak ~460 → ~20-50 occurrences résiduelles, pas zéro · validation post-ship requise (Largo re-run /tour fresh post-update)
- **Branchement post-validation** · réduction significative (target <10% leak résiduel) → backlog v2.87.7.1 chirurgical sur résiduels seulement (~1h) · échec validation → fall-back plan original Lots 1-3 refonte SKILL.md (10-14h) JUSTIFIÉ défendable
- Tests non-régression PASS · build-manifest 81 skills + **119 jargon entries (+27 auto-detected du mapping enrichi)** · build-brand-snapshot _EXAMPLE 24 lines · em-dash 0 NEW content
- Backward compat strict additif (enrichissement mapping additive 107→134 · zéro suppression · consume frontmatter additive · jargon bank refresh auto)
- D#472 captured · NEW memory canon `v2_87_7_smart_prompting_pattern` à poser post-merge (pattern reproductible cross-skills heavy futurs)

## [2.87.6.2] · 2026-05-24
### Changed
- **`tour.md` section Anatomie de la structure · refactor format 3 sections registre Onday institutionnel sobre** · drop-in replacement section panoramique statique v2.87.6 (5 territoires listés bullet-style) → récit 3 sections vulgarisé sans infantiliser
- **Section 1 · Pourquoi cet atlas existe** · douleur opérateur cimetière de briefs (50 angles écrits épuisés 3 mois) + atlas stocke briques typées qui produisent les briefs pas les briefs eux-mêmes (changes une brique reconstruis dix · ajoutes audience système dit angles compatibles · fatigues angle retires sans casser le reste)
- **Section 2 · Ce qu'on a déroulé sur Stepprs** · 5 phases avec découvertes concrètes (Produit 4 mécanismes × 5 bénéfices + alignement pivot · Audiences 2 poches + 5 profils workers shift sous-exploités · Angles 5 sources + 7 angles formule OTRB · Matrice 5×5=25 territoires + scoring sur 60 + top 3 · Brief généalogie spec→mécanisme→bénéfice→profil→angle)
- **Section 3 · Cycle de validation** · `hypothesis → tested → validated → scaled → fatigued` aucun saut autorisé · 2 tests confirmatoires pour validated · fatigued retiré matrice active · sépare atlas vivant du dossier mort
### Notes
- Source pédagogique référence Notion Onday Mode d'emploi (cartographie raisonnée Onday) · adaptation registre PhantomOS reference-grade sans copier littéralement
- Ton institutionnel sobre · pas de métaphore expliquée · pas d'accroche sales-bro · pas de Acte 1/2/3 dramatique · densité Notion Onday
- Pattern itératif validation correction v1 → v2 · première itération trop ludique infantilisante (caps screaming + Acte 1/2/3 + métaphore Lego littérale) recadrée Largo · v2 institutionnel sobre validé
- Backward compat strict additif (drop-in section replacement · awareness write `anatomie_walkthrough_seen` préservé · structure M2 sub-section position inchangée · M3 close cross-ref préservé)
- D#473 captured · memory canon `voice_doctrine_canon` revalidé (registre reference-grade tenu pour surface pédagogique opérateur-facing)

## [2.87.6.1] · 2026-05-24
### Fixed
- **`/update` Step 1 detect versions · cascade canon réécrit · PRIMARY = main branch `_version.json`** · fix friction distribution v2.87.6 live · autre session Claude Code avait check via `gh api releases/latest` (gh CLI absent · 'command not found') puis fallback `git ls-remote --tags` qui ne retourne que les tags publiés · v2.87.6 squash merged dans main sans tag publié donc raté · faussement claim 'à jour, voire en avance sur le tag public' alors que v2.87.6 main shipped
- **Cascade canon v2.87.6.1+** · PRIMARY clone shallow main + cat `_version.json` (source canonique distribution toujours synced post-merge · les tags peuvent être absents post-squash-merge alors que main contient déjà la dernière version) · SECONDARY gh CLI tags (validation complémentaire si gh installed) · TERTIARY fallback legacy `git ls-remote --tags` (si PRIMARY ET SECONDARY échouent)
### Notes
- Pattern reproductible documenté inline bash bloc Step 1 · explication audit friction v2.87.6 distribution + pourquoi cascade refactor (tags = signal incomplet pour version canonique distribution post-squash-merge)
- Backward compat strict additif (cascade additive · tags secondary preserved · workspaces déjà à jour via tags continuent fonctionner · workspaces sur main sans tag détectés correctement maintenant)
- D#472 captured · memory canon `update_pipeline` enrichissable post-merge

## [2.87.6] · 2026-05-24
### Changed
- **SPRINT SUBSTRATE** · 5 patches structurels canon substrate orchestrés post-discussion Largo posture orchestrateur · refresh atlas Stepprs deep desire chain canon v2.87.4 + NEW section walkthrough Porte A many-to-many tour.md + Q5 axes découpage gate map-audiences + patch_notes_v2_87_6 cross 5 skills heavy
- **Patch A · `chronic-pain-45/profile.json` refresh deep desire chain** · ajout `psychology.dream_scenario_narrative` (narrative grand-parent transgénérationnel canon · petits-enfants au parc · 800m aller-retour · target_recipient petits-enfants + fils/fille validation parentale · context_setting dimanche après-midi famille élargie sortie spontanée · social_payoff grand-mère active présente transmission générationnelle préservée) + `psychology.confidence_chain` (sourcing_method derived_indirect · cas pédagogique canon ne nécessite pas activation paid producer)
- **Patch B · `workers-shifts/profile.json` refresh deep desire chain** · ajout `psychology.dream_scenario_narrative` (narrative conjoint Friday evening canon · vendredi 19h fin de shift sortie spontanée resto 15 min · target_recipient conjoint validation conjugale disponibilité énergie post-shift · context_setting transition travail → vie perso · social_payoff conjointe disponible présente couple préservé qualité weekend) + `$comment_dream_scenario_narrative` pédagogique + `psychology.confidence_chain` (cohérence schema canon v2.87.4)
- **Patch C · `tour.md` NEW section Anatomie de la structure** · M2 sub-section post-Gate Porte A · rendu opérateur prose conversationnelle native (5 territoires Stepprs encoded explicit en langue métier · pattern many-to-many illustré audience × angle × mécanique) · awareness write `anatomie_walkthrough_seen = true` post-rendu Porte A · permet M3 close option drill un territoire avec contexte
- **Patch D · 5 skills heavy `patch_notes_v2_87_6` entries chirurgicaux** · `trendtrack-enrich-brand` v1.1.0 · `decompose-ad` v2.2.0 · `map-audiences` v1.3.0 · `craft-packshot` v1.3.0 · `compose-creative` v1.8.0 · documentent enforcement runtime statut dette inchangé v2.87.4 + v2.87.5 maintien backlog v2.88.0+ implementation (pattern miroir scope chirurgical · pas refonte massive)
- **Patch E · `map-audiences` v1.3.0 NEW Q5 axes primaires de découpage MECE explicit** · 6 options canon `AskUserQuestion` (`use_case` · `démographie` · `canal` · `awareness_stage` · `sophistication` · `trigger_temporel`) · gate obligatoire si Q2 niveau granularité = 2 ou 3 sub-audiences scaffold détecté · pattern raisonnement agent proposer axe primaire maximise variance copy entre sub-audiences · test runtime cas concret obligatoire AVANT Step 2 scaffold (articuler 2 hooks copy distincts par axe candidat · comparer side-by-side · axe primaire = axe produit plus grande divergence copy) · persiste `meta.primary_splitting_axis` sur mère audience · anti-pattern banned scaffolder 2+ sub-poches sans Q5 explicit · enforcement runtime backlog v2.88.0+
### Notes
- **Enforcement runtime hardcoded Steps EDD + NIVEAU LIVE 5 skills heavy DEFERRED v2.88.0+** · statut dette inchangé v2.87.4 + v2.87.5 documentée · v2.87.6 maintien backlog v2.88.0+ implementation (pattern miroir v2.87.5 · pas refonte massive ce sprint cap qualité chirurgical scope)
- **Q5 axes découpage map-audiences enforcement runtime backlog v2.88.0+** · déclaratif patch_notes + runtime body documenté · pas hardcoded `AskUserQuestion` trigger automatique cycle map-audiences
- **Consume substrate `dream_scenario_narrative` dans compose-creative déclaratif patch_notes** · runtime implementation backlog v2.88.0+ (skill consume actuellement reste fonctionnel pain-relief flat · doctrine canon v2.87.4 spec'd mais consume runtime backlog)
- **Pattern méthodologique reproductible** · scope chirurgical patch_notes + NEW files canon vs refonte runtime massive · wall-time réel cumul ~3h (vs cap initial 7.5-9.5h)
- **Pattern orchestrateur posture validé Largo** · englober inputs Stepprs refresh + many-to-many walkthrough + Q5 axes découpage dans séquence orchestrée vs silo · permet substrate canon hardened post-distribution
- Tests non-régression à valider POST-EXEC · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · 0 em-dash NEW tour.md section + SKILL.md patch_notes_v2_87_6 entries
- Backward compat strict additif (NEW fields psychology déjà spec'd canon v2.87.4 schema · NEW tour.md section additive · patch_notes entries déclaratifs sans breaking runtime existing · Q5 NEW gate map-audiences additive)
- D#471 captured · NEW memory canon `v2_87_6_substrate_sprint` à poser post-merge

## [2.87.5] · 2026-05-22
### Changed
- **SPRINT EXPÉRIENCE OPÉRATEUR** · 5 patches structurels post-discussion ontologie + connectors organisationnels · pattern proactif phantom systémique (todos visibility + connectors propose + scheduling propose + entity add propose)
- **Patch A · `/phantom todo` brand-level dédié** · NEW `phantom-modes/todo-brand.md` · 4 blocs canon (Actions + Connectors + Schedules + Atlas completeness) · routing override `/phantom {brand} todo` ajouté dans `phantom.md` Mode detection
- **Patch B · `setup-brand` v2.1.1 → v2.2.0** · NEW Phase "Connectez vos outils" · matrice 7 catégories canon (Paid platforms · Analytics · Lifecycle · Attribution · Spy tools · CMS/production · Workspace tools via MCP claude natif) + branching choice 3 voies post-URL pasted via `AskUserQuestion` (A Approfondir maintenant · B Connecter outils d'abord · C Faire les deux séquence recommandée canon B-puis-A) + trade-off MCP claude natif (mono-auth solo) vs clé API per brand (multi-account agence)
- **Patch C · brand-todo proactif** · intégré `phantom-modes/todo-brand.md` 4 blocs canon · connectors checkup + schedules manquants + atlas gaps surfacés ensemble vs todo plat actions seules
- **Patch D · `phantom.md` v2.79.2 → v2.87.5** · NEW directive cockpit brand SCHEDULES section + storage canon `brands/{slug}/scheduled.json` + catalogue 7 skills schedulables (`mine-voc` weekly · `trendtrack-enrich-brand` weekly · `audit-creative-fatigue` monthly · `brief-day` daily · `watch-competitors` weekly · `analyze-perf` weekly · `trendtrack` shop profile monthly) + trigger mechanism `CronCreate` (predictable récurrent) OR `ScheduleWakeup` (dynamic /loop monitoring conditionnel)
- **Patch E · NEW `/add {entity}` slash command v1.0.0** · pre-flight proactif analytique · 8 étapes canon (Receive intent + Read atlas existing silent + Raisonner CC v3.1 + Cross-check overlap detection + Propose response + Trigger direct OR 1 question pivotale OR STOP signal) · triggers `/add audience` `/add angle` `/add pain` `/add objection` `/add product` `/add friction` OR détection auto type optimal selon intent verbal · pattern miroir senior media buyer brief équipe (*"voici ce que je vois, voici ce que je propose, OK ?"*)
### Notes
- **Patch F · enforcement runtime hardcoded Steps EDD + NIVEAU LIVE 5 skills heavy DEFERRED v2.88.0+** · déjà documenté dette `patch_notes_v2_87_4` cross trendtrack-enrich-brand + decompose-ad + map-audiences + craft-packshot + compose-creative · pas refonte massive ce sprint cap qualité chirurgical scope · enforcement runtime backlog v2.88.0+ implementation
- **Pattern méthodologique reproductible** · scope chirurgical patch_notes + NEW files canon vs refonte runtime massive · wall-time réel cumul ~2h (vs cap initial 5-7h)
- **Cross-ref memory canon** · `brand_connectors_onboarding_canon` (matrice 7 catégories connectors · branching choice 3 voies · proactive scheduling proposals · /add proactif analytique · 5 axes patches détaillés)
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · 0 em-dash NEW files (`/add.md` + `phantom-modes/todo-brand.md`)
- Backward compat strict additif (NEW files canon + patch_notes_v2_87_5 entries · cycle runtime skills heavy preserved · enforcement runtime hardcoded backlog v2.88.0+)
- D#470 captured · NEW memory canon `expérience_operateur_sprint_v287_5` à poser post-merge

## [2.87.4] · 2026-05-21
### Changed
- **SPRINT UNIFIÉ ÉTENDU post-audit Fincut session v2.87.3** · 5 agents Sonnet parallèle audit cross-axes (deep desire chain · fluidité jargon · adoption doctrines IP/DVD/EDD · honnêteté sourcing · atlas substrate matriciel) · 8 frictions HIGH + 8 MEDIUM identifiées · 3 patches structurels + 4 chirurgicaux
- **Patch A · schema audience deep desire chain** · `profile.schema` v2.0 → v2.1 · NEW `psychology.dream_scenario_narrative` (object · narrative 2 phrases + target_recipient relationnel + context_setting concret · 3 required) + `psychology.confidence_chain` (object · sourcing_method enum + confidence_level enum + 3 optional) · gate canon `profile-audience` v1.8.1 → v1.9.0 HR-DD-1 refuse audience pain layer fonctionnel sans descente racine Schwartz/Kern · Closes audit Fincut finding systémique audience encoding shallow
- **Patch B · propagation doctrines EDD + DVD NIVEAU LIVE cross 4 skills heavy** (dette documentée enforcement runtime backlog v2.87.5+) · `trendtrack-enrich-brand` v1.0.0 → v1.1.0 · `decompose-ad` v2.1.0 → v2.2.0 · `map-audiences` v1.2.0 → v1.3.0 · `craft-packshot` v1.2.0 → v1.3.0 · cross-refs `engagement-disclosure-doctrine` v2.79.5+ + `decomposition-visibility-doctrine` v2.81.1+
- **Patch C · compose-creative encoding canonical many-to-many enforcement** · `compose-creative` v1.7.0 → v1.8.0 + `recompose-creative` v1.2.2 → v1.3.0 + `compose-overlay-text` v1.0.1 → v1.1.0 · enforcement entry canonical `brands/{slug}/creatives/{CRT-NN}/` OBLIGATOIRE avec lineage (angle_ref + audience_ref + product_ref + mechanism_ref + concept_ref) + tags (concept + creative + variant + mécanique narrative) + cross-refs many-to-many activés · asset JPG dans `creatives/{CRT-NN}/produced/` + brief markdown dans `creatives/{CRT-NN}/brief.md` · Notion bridge auto-wire creatives DEFERRED v2.88.0+ pour skill `sync-creatives-to-notion` séparé (respect canon `territory-doctrine.md`)
- **Patch D · 4 chirurgicaux UX** ·
  - **D1** · `.claude/hooks/checkpoint-resolver.py` enrichi `CONFIRM_PATTERNS` avec patterns canon AskUserQuestion (encode · lance · ça va · comme ça · je valide · envoie · roule · on y va) · résout friction Phase 8 audit Fincut (opérateur sélectionne option AskUserQuestion puis devait retaper go/ok séparément) + regex validé(z|é|és|ée|ées) étendu accents
  - **D2** · jargon leak 3 occurrences · `produce-paid-angles` OTRB sigle → "4 temps Observation × Tension × Reframe × Bridge (acronyme interne · jamais exposé opérateur)" · `trendtrack-enrich-brand` LRN-NNNN IDs → "N patterns d'intelligence capturés" annotation explicit · `trendtrack-enrich-brand` AskUserQuestion auth path → plain language
  - **D3** · `mine-voc` v1.4.1 → v1.5.0 · NEW HR-VOC-403-1 Trustpilot 403 STOP signal canon · 4 obligations enforcement runtime (STOP signal proactif surface + LRN-type:workaround logged + `confidence_chain.blocked_sources` populated + pending-validations.md item mainteneur)
  - **D4** · `craft-packshot` v1.3.0 enrichi · NEW HR-CP-SED-1 packshots iterations versionnés → production layer `iterations/` subfolder · seul canonical validé en territory · 2 items backlog mainteneur v2.87.5+ (write-to-context.py ALLOWED_PATH_PATTERNS + runtime output_path)
### Notes
- **Audit Fincut session v2.87.3 référentiel** · 8 frictions HIGH résolues (Patch A deep desire + Patch B doctrines propagation déclarée + Patch C creatives canonical + Patches D1-D4 chirurgicaux) · 8 MEDIUM dette documentée (IP 5 sections cross 4 outputs · MECE overlaps · audience wardrobe-essentials non encodée · LRN cross-refs broken · drift clinique disclosure EDD · transition Stepprs → Fincut · CC v3.1 non adopté decompose-ad · confidence levels A1/A2 non verbalisés)
- **Backward compat strict additif** cross tous patches · lecture v2.0 préservée fields optional en read ancien · obligatoire en write profile-audience v1.9.0+ · cycle runtime skills heavy preserved (seul enforcement output change pour compose-creative/recompose-creative/compose-overlay-text)
- **Pattern systémique adoption doctrines** · build-atlas-complete reste skill canon référence propre EDD + NIVEAU 0 + IP complet (1/5 skills heavy validé runtime audit Fincut) · 4 autres skills heavy patch_notes_v2_87_4 documentent dette + cross-refs doctrines · enforcement runtime hardcoded Steps EDD + NIVEAU LIVE markers backlog v2.87.5+ implementation
- **Honnêteté discipline** · Notion bridge auto-wire creatives explicitement DEFERRED v2.88.0+ (skill `sync-creatives-to-notion` non shipped · `sync-notion-atlas` v2.0.1 territoire-only strict · creatives production layer skill séparé canon territory-doctrine). Pas inventer ce qui n'existe pas
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · backward compat strict additif · 0 régression runtime sur 3 repos sync
- Wall-time réel cumul ~3h sprint structurel (cap initial 6-8h respecté · scope chirurgical patch_notes vs refonte massive)
- D#468 captured · NEW memory canon `unified_sprint_v287_4`

## [2.87.3] · 2026-05-21
### Changed
- **PATCHES SURFACES PREMIER CONTACT PRÉ-PARTAGE** · 6 chantiers chirurgicaux résolvent 13/16 frictions HIGH audit qualité narration v2.87.2 (gate partage opérateurs externes)
- `WELCOME.md` 17L → 15L · chirurgie L9+L11+L13 · couper section Runtime definition (path interne `.claude/commands/tour.md`) · reformuler Awareness tracking en *Memory across sessions* plain language (zéro path `/operator/awareness.json`) · couper parenthèse gate plomberie L13 (`first deliverable built + operator explicitly asks`)
- `lexicon.md` 119L → 115L · supprime section Slug intégralement (concept interne agent · n'a pas place glossaire opérateur) · reformule Skill plain language (`L'agent reconnaît votre demande en langage naturel` · zéro mention `.skills/_manifest.json`)
- `.claude/commands/tour.md` 284L → 288L · failure modes M2 plain language (`Chrome MCP` → `ton navigateur Chrome` · `auto-snapshot ({score}%)` → `atlas fiable`) + 2 notes blockquote interne agent en tête M1 et M3 (labels portes A/B/C/D + slugs runtime `arc:substance`, `setup:brand`, `import:archive`, `explore:free`, `volet:{nom}`, `drill:{territoire}`, `exit:setup`, `pivot:{volet}`, `build-skill:{territoire}` sont vocabulaire interne agent · jamais exposer `AskUserQuestion` ni prose opérateur)
- `.skills/skills/mine-voc/SKILL.md` · sed em-dashes (62 occurrences → 0)
- `.skills/skills/produce-paid-angles/SKILL.md` · sed em-dashes (65 occurrences → 0) + renforce HR Banned jargon in operator surface (ajout explicit `voice.key_expressions[]` · `verbatim_quotes[]` · `pain_points[].verbatim_quotes[]` · `formula.tension.reason_blocked` + clause générale *no JSON field paths whatsoever in operator-facing surface*)
- `.skills/skills/audit-meta-account/SKILL.md` · sed em-dashes (20 occurrences → 0)
- Em-dashes cumul cross 3 skills · 147 → 0 (substitut middle dot `·` canon voice-doctrine v2.84.1)
### Notes
- **Audit qualité narration v2.87.2 référentiel** · 16 frictions HIGH identifiées (5 narration · 3 doctrines · 4 onboarding · 4 skills) · sprint LITE P0 chirurgical résout 13/16 (couches narration + onboarding + skills surface)
- **Sémantique runtime intacte** · cycles Step 0-12 produce-paid-angles + Steps 0-7 mine-voc + 5 blocs diagnostic audit-meta-account preserved · spec instructions agent inchangées · canons Vincent runtime slugs préservés (annotation interne ajoutée pour bloquer leak runtime futur)
- **3 frictions HIGH restantes** (P1 backlog v2.87.4 · ~2.5h) · doctrines docstrings massifs EDD + DVD + OCD auto-violation (chantier 7) · produce-paid-angles NIVEAU LIVE absent (chantier 8) · creative-brief-composer disclosure v2.79.3 → v2.79.5 + ANG-NN exposé + NIVEAU LIVE (chantier 9)
- **9 frictions P2 backlog v2.88.0+** · audit-meta-account disclosure pré-engagement add (chantier 10) · EDD↔DVD frontière format NIVEAU 0 cross-ref propriété explicit (chantier 11) · IP 5 sections adoption mine-voc + audit-meta-account + produce-paid-angles (chantier 12)
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · em-dash 0 cross 4 surfaces premier contact + 3 skills patchés · 0 path leak WELCOME + lexicon · 0 ## Slug section lexicon · 2 Note interne agent tour.md (M1 + M3)
- **Finding honnêteté discipline** · audit C6 (jargon JSON exposé opérateur produce-paid-angles) partiellement faux à la relecture · messages opérateur déjà plain language · paths apparaissent dans spec instruction agent qui entoure (contexte logique check) · patch C6 = renforcement HR730 prévient leak runtime futur par mimétisme agent
- **Séquence demain** · v2.87.0bis test runtime onboarding fresh post-v2.87.3 (~45min) · v2.86.1 validation runtime 5 scénarios skills compositionnels heavy (~1.5h) · v2.88.0 verbatim gate downstream (~1.5h) · distribution préparation
- D#467 captured · NEW memory canon `lite_p0_patches_v287` à poser

## [2.87.0] · 2026-05-20
### Changed
- **SIMPLIFICATION ONBOARDING + COHÉRENCE CROSS-SURFACES** · tour.md v2.81.0 → v2.87.0 · architecture 4 milestones canoniques + close réflexif réutilisé partout
- `.claude/commands/tour.md` · 686L → 284L (**-59%**) · M1 splitter 4 portes + M2 first deliverable encadré (remonté position 2 court-circuite tunnel) + M3 close réflexif universel (slugs `volet:{nom}` · `drill:{territoire}` · `exit:setup` · `pivot:{volet}` · `build-skill:{territoire}`) + M4 replay évolutif
- `operator/awareness.json` · schema v1.0 → v1.1 · 5 fields NEW (`tour_entry_door` · `paths_skipped` · `first_deliverable_built` · `first_deliverable_skill` · `first_deliverable_validated_corrections`) + 1 type fix (`first_skill_built` false → null)
- NEW `operations/migrations/v2.87.0-awareness-schema-fields.py` · migration idempotent · backup horodaté · re-run safe (pattern miroir v2.42/v2.63/v2.64)
- `WELCOME.md` 15L → 17L · phrase canon v4 EN en tête + flow réécrit pour matcher architecture v2.87
- `README.md` 67L → 69L · phrase canon v4 EN exacte en tête section description + restructure progression
- `lexicon.md` 103L → 119L · 4 entrées NEW prepend avant Brand (`Workspace agentic` · `Skill` · `Porte d'entrée` · `Slug`)
### Notes
- **3 décisions Phase 1 tranchées Largo orchestrateur** ·
  1. Architecture 4 milestones validée (avec 2 caveats préservation arc substance Porte A via slugs M3 close)
  2. Matrice défauts deliverable par porte M2 validée (A=Stepprs pédagogique · B=brand opérateur · C=post-import · D=scan signaux)
  3. Phrase canon v4 validée (micro-ajustement `l'agent y raisonne et exécute`)
- **Phrase canon v4 littéralement identique cross 3 surfaces premier contact** (README L3 EN · WELCOME L3 EN · tour.md M1 FR+EN · lexicon entrée Workspace agentic)
- **Préservations 8/8 confirmées** · canons Vincent runtime + détection live registre + bypass URL pasted + awareness writes structurés + failure modes 3 cas + HR-OHD-2 zéro typage profil métier + prose conversationnelle native + politique FR/EN voice-doctrine v2.84.1 + ton premium zéro concurrent nommé
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 4 surfaces · migration script idempotent confirmé (workspace clean + legacy v1.0 → v1.1)
- **Phase 5 test runtime ISOLÉE v2.87.0bis** · discipline honnêteté gate distribution non négociable fatigué · pattern miroir isolations précédentes (v2.85.1bis · v2.85.4 brand-isolation REPORT v2.85.5 · v2.85.3 effort 3)
- D#466 captured · D#467 réservé v2.87.0bis · NEW memory canon `onboarding_simplified_v287` (architecture 4 milestones + phrase canon v4 + matrice défauts par porte)
- Backlog · v2.87.0bis test runtime workspace fresh phantom-test-v287 · distribution preparation (GitHub Releases + liste opérateurs + message invitation)

## [2.86.0] · 2026-05-20
### Changed
- **AUDIT CROSS-FILES FINAL** post-clôture chantier propagation contenu v2.85.5
- **~56 patches résiduels Discipline → Doctrine cross-files** · `docs/system/README.md` catalogue listings (~25) + `claude-md-doctrine.md` propagation oubli (9) + `changelog-doctrine.md` propagation oubli (3) + `compositional-cartography.md` titre oubli lot 1 corrigé (5) + 6 doctrines body cross-refs descriptors + `voice.md` ligne 104 catalogue + `canon.md` interne descriptors + `provenance-trust-discipline-scope.md` titre + footer + `doctrine-governance.md` table header + exemples futures doctrines
### Notes
- **3 décisions tranchées v2.86.0** ·
  1. **synthesis** · Option A · CONSERVÉ EN unified (48 occurrences architectural concept CMR/CI primitif · 0 patch)
  2. **Notion/Airtable mention operational-system §1** · CONSERVÉE (tableau Différenciation structurelle comparative · registre GitHub/Vercel autorisé · refactor structurel hors scope)
  3. **26ème doctrine périphérique** · 3 doctrines non-propagées réellement identifiées (claude-md + changelog · notion-bridge déjà conforme) + 1 oubli lot 1 (compositional-cartography titre) · TOUTES traitées v2.86.0
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep Discipline résiduel 0 (sauf 2 voice-doctrine descriptifs convention historique + 1 em-dash documentation interdiction · tous légitimes)
- **État chantier propagation contenu post-v2.86.0** · 27/28 doctrines cohérentes · ~203 patches cumulés cross chantier complete · 18 sprints v2.84.0 → v2.86.0 · 0 régression runtime cumulée
- D#465 captured · memory canon `doctrine_propagation_complete` enrichi audit final
- Backlog · v2.86.1 validation runtime 5 scénarios (GATE distribution) · v2.86.2 test discovery externe · distribution préparation

## [2.85.5] · 2026-05-20
### Changed
- **CLÔTURE chantier propagation contenu voice-doctrine v2.84.1** · `brand-isolation-doctrine.md` propagée (68L · 1 patch principal titre `Brand isolation discipline` → `Brand Isolation Doctrine` cohérence post-rename + capitalisation canon)
- **25/26 doctrines propagées cumulé** lots 1+2+3+4+5 · 1 doctrine restante périphérique chantier (notion-bridge OR doctrine-governance · backlog v2.86.x si nécessaire)
### Notes
- Sprint court 20-30 min wall-time · application STRICT cohérente lots 1-4 (Phase 1 lecture intégrale + Phase 2 édition critique + self-conformance + Phase 3 gate hygiène + Phase 4 ship)
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 · grep Discipline résiduel 0
- **BILAN CHANTIER PROPAGATION CONTENU v2.84.1 → v2.85.5** ·
  - 17 sprints cumulés (1 doctrine NEW v2.84.0 + 3 propagations cross-files v2.84.1-v2.84.4 + 5 sprints rename v2.85.0.x + 5 sprints propagation contenu v2.85.1-v2.85.5)
  - 25/26 doctrines propagées
  - 147 patches cumulés cross 25 doctrines
  - 8094L total stable (2102+1457+2121+2346+68)
  - 0-1% compression structurelle cumulée (préservation stricte tenue 5 sprints)
  - 0 régression runtime cumulée
  - **Hypothèse VALIDÉE 5 lots consécutifs** · voice-doctrine propagée par ricochet plus largement qu'estimé · 3 vecteurs validés (doctrines créées sous discipline canon en amont + trilogie propagations v2.84.2-v2.84.4 + chantier rename v2.85.0.x)
- **Patterns systémiques identifiés** cross 5 lots ·
  - Discipline → Doctrine cohérence post-rename (115 patches cumulés)
  - Operational System cross-ref harmonisation systémique (cross 9-10 doctrines référençantes)
  - Generic discipline → doctrine systémique (meta-discipline · sub-discipline · etc.)
  - Cross-refs cassées avec dates obsolètes `-2026-04-26.md` corrigées
  - Anglicismes prose isolés patchés (skipée/négligée · explicit/explicite · capped/limitée · signaled/signalé · collapse/effondrent · operator/opérateur)
- **Garde-fous canons codifiés en memory canons** · cap 500L par doctrine (v2.85.1bis) · Phase 2.A lecture intégrale obligatoire (v2.85.1bis) · self-conformance Phase 2.C (v2.85.1bis) · scope strict voice-doctrine (Largo politique) · filter Haiku scoring main thread Sonnet (v2.85.3) · spot-check cross-refs entrantes producer central (v2.85.4)
- **Politique FR/EN consolidée canon** validée 5 lots · acronymes industrie EN + creative/operator/campaign FR + platform-specific EN + termes canon PhantomOS EN (canonical/load-bearing/Operator-facing)
- D#464 captured · NEW memory canon `doctrine_propagation_complete` (clôture officielle chantier) · memory canon `doctrine_propagation_progress` finalisé 25/26
- Backlog · v2.86.0 audit cross-files final + résolution synthesis (48 occurrences cumul) + Notion/Airtable mention operational-system §1 + 1 doctrine restante évaluation propagation

## [2.85.4] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 4/4** · 6 doctrines opérationnelles éditées critique main thread Sonnet · `operational-system-doctrine` · `attribution-multitouch-doctrine` · `skill-routing-doctrine` · `engagement-disclosure-doctrine` · `onboarding-holistic-doctrine` · `update-distribution-doctrine`
- 2346L → 2346L (0% compression structurelle · scope strict voice-doctrine respecté · 4 lots consécutifs validés)
- 40 patches cumulés · 5 titres Discipline → Doctrine + body occurrences (Skill Routing · Engagement Disclosure · Onboarding Holistic · Update Distribution · Attribution Multitouch + 1 dans operational-system pour Operational System Discipline auto-référence) + 5 cross-refs `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` harmonisées systémique + 1 frontmatter `update-distribution-discipline` → `-doctrine` + 4 cross-refs cassées corrigées dans operational-system (`audiences-cartography-doctrine.md` plural typo → `audience-cartography-doctrine.md` singular + `pain-benefit-chain-doctrine.md` inexistant → `pain-benefit-chain.md`)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 7 candidates inventoriées · filter main thread Sonnet · 0 doctrine effort 3 réel · cap 500L respecté (max 473L update-distribution · marge 27L)
- **Décision pré-flight** · brand-isolation-doctrine REPORTÉE v2.85.5 sprint court (68L · 1 patch principal · ~20-30 min) · cap strict 6 doctrines maintenu lot 4
- **Hypothèse VALIDÉE 4 lots consécutifs** · doctrines opérationnelles aussi conformes que doctrines racines (lot 1) + audience/creative (lot 2) + structurantes (lot 3). Pattern voice-doctrine propagation par ricochet confirmé sur cycle complet
- **Pattern systémique NEW lot 4** · `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` harmonisé cross 5 doctrines référencantes (skill-routing · engagement-disclosure · onboarding-holistic + déjà patché lots 1+2 sur OCD + pacing)
- **Pattern cross-ref cassées corrigées** · operational-system-doctrine référençait 2 fichiers inexistants/typos (`audiences-cartography-doctrine.md` plural + `pain-benefit-chain-doctrine.md` non-existing) · corrigés cohérence cross-rename systémique
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep Discipline résiduel 0
- **Spot-check operational-system cross-refs entrantes** · TOUS valides post-édition (CI ligne 146 · pacing 191/268/281/288 · OCD 375 → `operational-system-doctrine.md`) · cohérence cascade canonical préservée · scope strict respect règles canon 5 couches confirmé
- Monitor `synthesis` lot 4 · 2 occurrences (engagement-disclosure 2) · cumul lots 1+2+3+4 = 48 occurrences pour v2.86.0 audit cross-files résolution unifiée
- D#463 captured · memory canon `doctrine_propagation_progress` mis à jour (compteur 4/4 lots traités · 24/26 doctrines propagated · brand-isolation PENDING v2.85.5)
- Backlog · v2.85.5 sprint court brand-isolation (CLÔTURE 25/26 atteint) · v2.86.0 audit cross-files final + synthesis résolution + Notion/Airtable mention operational-system

## [2.85.3] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 3/4** · 6 doctrines authoring + schema éditées critique main thread Sonnet · `skill-authoring-doctrine` · `schema-encoding-doctrine` · `extension-discovery-doctrine` · `scope-extension-doctrine` · `territory-doctrine` · `entry-arc-doctrine`
- 2121L → 2121L (0% compression structurelle · scope strict voice-doctrine respecté · patches mécaniques substitution/cohérence uniquement)
- 55 patches cumulés · 5 titres `Discipline → Doctrine` (preserve acronymes SAD/SED/SED-X) + 28 occurrences body Discipline → Doctrine cohérence post-rename + 4 cross-refs obsolètes avec dates retirées (`canonical-matrix-reasoning-2026-04-26.md` → sans date) + 4 cross-refs `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` harmonisées + 5 patches generic `discipline → doctrine` (meta-discipline · sub-discipline · "an authoring discipline" · "single discipline that governs" · "another discipline") + 1 frontmatter `name: entry-arc-discipline → entry-arc-doctrine` + 1 cross-ref `onboarding-holistic-discipline → onboarding-holistic-doctrine` (4 occurrences replace_all)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 6 doctrines inventoriées · effort Haiku 2/2/2/2/3/3 · main thread filtre scoring · effort réel scope strict voice-doctrine = 2/6 (0 doctrine effort 3 réel · narratif structurel + termes canon "canonical"/"load-bearing" hors scope)
- Garde-fous PASSED · cap 500L respecté (max 458L entry-arc · marge 42L) · 0 isolation v2.85.3bis nécessaire
- **Hypothèse VALIDÉE 3 lots consécutifs** · doctrines structurantes (authoring + schema) aussi conformes que racines (lot 1) et audience + creative (lot 2). Voice-doctrine propagée par ricochet plus largement qu'estimé · violations majoritairement cosmétiques cohérence post-rename
- **Pattern systémique identifié** · 5 doctrines structurantes utilisaient `meta-discipline` / `an authoring discipline` / `parmi les disciplines` / `sub-discipline` génériques · patch cohérence canon `doctrine` systémique
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep `Discipline` résiduel post-Phase 3 fix 0 (1 occurrence extension-discovery ligne 29 manquée Phase 2 fixed Phase 3)
- Monitor `synthesis` lot 3 · 2 occurrences (skill-authoring 1 + territory 1) · cumul lots 1+2+3 = 46 occurrences pour v2.86.0 audit cross-files résolution unifiée
- D#462 captured · memory canon `doctrine_propagation_progress` mis à jour (compteur 18/26 cumul · 3 lots SHIPPED · lot 4 PENDING)
- Backlog · v2.85.4 lot 4/4 opérationnelles · v2.86.0 audit cross-files final + résolution synthesis

## [2.85.2] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 2/4** · 6 doctrines audience + creative éditées critique main thread Sonnet · `pain-benefit-chain` · `audience-cartography-doctrine` · `progressive-cartography-doctrine` · `creative-testing-doctrine` · `pacing-doctrine` · `visual-identity-doctrine`
- 1457L → 1457L (0% compression structurelle · scope strict voice-doctrine respecté · patches mécaniques substitution/cohérence uniquement)
- 30 patches cumulés · majoritairement `Discipline → Doctrine` cohérence post-rename v2.85.0.x (4 titres + 4 occurrences body) + franglais isolés (`skipée → négligée` · `explicit → explicite` · `capped → limitée` · `signaled → signalé` · `collapse → effondrent` · `operator → opérateur` prose FR) + 1 cross-ref `Operational System Discipline v2.71` → `système opérationnel (operational-system-doctrine.md)` (pacing-doctrine §8)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 6 doctrines inventoriées · effort 1 sur 2/6 + effort 2 sur 4/6 · garde-fous tous PASSÉS (cap 500L · max 379L · 0 isolation v2.85.2bis nécessaire)
- **Hypothèse pré-flight PARTIELLEMENT INFIRMÉE** · doctrines audience + creative v2.6x-v2.7x aussi conformes que doctrines récentes lot 1 (0.7-1.4 violations / 100L) · voice-doctrine propagée par ricochet plus largement qu'estimé (création sous discipline canon + trilogie v2.84.2-v2.84.4 + chantier rename v2.85.0.x)
- **Politique FR/EN consolidée** (validation Largo) · acronymes industrie EN préservés (CPM · CPA · ROAS · CTR · etc.) · termes traduits FR (creative→créative usage substantive · operator→opérateur prose FR) · technical platform-specific préservés EN (adset · copy · retargeting · landing page · buyer)
- Tests non-régression PASSÉS · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep `Discipline` résiduel titre interne 0
- D#461 captured · memory canon `doctrine_propagation_progress` mis à jour (compteur 12/26 cumul · lots 3-4 PENDING)
- Anglicisme `synthesis` (~10 occurrences lot 2 + 34 occurrences lot 1 déjà shipped) NON patché · cohérence cross-files prime sur patch unilatéral · question reportée v2.86.0 audit cross-files
- Backlog · v2.85.3 lot 3/4 authoring + schema · v2.85.4 lot 4/4 opérationnelles · v2.86.0 audit cross-files final + question synthesis

## [2.85.1] · 2026-05-20
### Changed
- **PROPAGATION VOICE-DOCTRINE LOT 1/4** · 6 doctrines racines + investigation éditées critique main thread Sonnet · `contextual-intelligence` · `investigation-posture` · `canonical-matrix-reasoning` · `compositional-cartography` · `decomposition-visibility-doctrine` · `output-clarity-doctrine`
- 2102L → 2083L (-1% · préservation stricte sémantique)
- 18 patches sprint initial cumulés · titres `Discipline → Doctrine` (cohérence post-rename v2.85.0.x) · Status DRAFT → SHIPPED canonical-matrix-reasoning · cross-ref `doctrine-governance-2026-04-26.md` corrigée · sections Position 5 couches compressées · bullets/sections narratives compressées
- **Fold v2.85.1bis** · audit honnêteté qualité post-sprint a révélé Phase 2.A lecture critique glissée sur 2/6 doctrines (DVD 668L + OCD 397L lues partiellement initialement) · sprint dédié v2.85.1bis lecture intégrale obligatoire DVD + OCD · 3 patches additionnels cohérence post-rename (DVD ligne 89 cross-ref Operational System Discipline → operational-system-doctrine.md · DVD ligne 295 skills decomposition-visibility-discipline → -doctrine · DVD ligne 527 narratif Decomposition Visibility Discipline → Doctrine)
### Notes
- Pré-flight Phase 1 · 1 sub-agent Haiku · 6 doctrines toutes en effort 1 (mineur) · ~15 violations totales · garde-fous tous PASSÉS
- **Apprentissage canon majeur** · doctrines racines + investigation déjà majoritairement conformes voice-doctrine (créées récemment v2.79.x-v2.82.x sous discipline canon · trilogie v2.84.2-v2.84.4 a aligné vocabulaire transverse · chantier rename v2.85.0.x touchait noms pas contenu) · compression réelle -1% vs briefing -30/-50% · préservation stricte sémantique > forced reduction
- **Apprentissage v2.85.1bis** · pré-flight conformité "majoritairement conforme" N'EST PAS un blanc-seing pour skip Phase 2.A lecture intégrale · NEW garde-fou canon lots 2-4 · cap 500L par doctrine dans un lot · doctrine candidate dépasse 500L → isoler en sprint dédié dès pré-flight (cohérent pattern LITE chantier rename + isolation decomposition-visibility v2.85.0.3a)
- Tests non-régression PASSÉS post v2.85.1bis · build-manifest 81 skills + 92 jargon · build-brand-snapshot _EXAMPLE 24 lines · grep em-dash 0 cross 6 doctrines · grep `*Discipline*` titre interne 0 cross 2 doctrines critiques (DVD + OCD)
- D#460 captured · memory canon `doctrine_propagation_progress` mis à jour (NEW garde-fou cap 500L lots 2-4 · 2/6 doctrines glissées v2.85.1 résolues v2.85.1bis)
- Backlog · v2.85.2 lot 2 audience + creative (doctrines plus anciennes v2.6x-v2.7x · compression réelle attendue plus proche briefing 10-20%)

## [2.85.0.3b] · 2026-05-20
### Changed
- **CLÔTURE CHANTIER RENAME · 21/21 doctrines renommées** · 2 dernières fichiers `*-discipline.md` → `*-doctrine.md` · `engagement-disclosure` · `schema-encoding` · alignment voice-doctrine v2.84.1 politique linguistique FR/EN canon COMPLET
- 147 cross-refs patches batch · 68 fichiers consumers patchés
### Notes
- Pré-flight ciblé Phase 1 · 1 sub-agent Haiku · garde-fous tous PASSÉS (174 cumulé < 250 · max 105 par doctrine < 150)
- Tests non-régression Phase 4 PASSÉS · build-manifest 81 skills · build-brand-snapshot _EXAMPLE 24 lines · grep résiduel 0 occurrence · spot-check 2 skills consumers (import-archive 4 refs · sync-notion-atlas 5 refs) ✓ · vérification 0 fichier `*-discipline.md` restant ✓
- **Bilan chantier rename 5 sprints v2.85.0 → v2.85.0.3b** · 21 doctrines renommées · 926 replacements cumulés (107 + 253 + 258 + 161 + 147) · 0 régression runtime
- D#459 captured · NEW memory canon `doctrine_rename_complete` (clôture officielle) · memory `v85_0_lite_lessons` mis à jour (calibration finale 5 lots)
- Pattern reproductible documenté pour sprints futurs refactor structurel cross-files (pré-flight + garde-fous + script Python batch + tests + spot-check + ship via PR)
- Prochain chantier · v2.85.1 propagation contenu voice-doctrine STRICT (qualitativement différent · pause cognitive obligatoire avant)

## [2.85.0.3a] · 2026-05-20
### Changed
- **Rename lot 4a/4** · isolation `decomposition-visibility-discipline.md` → `decomposition-visibility-doctrine.md` (doctrine la plus consommée du système · 12 skills consumer runtime) · **19/21 doctrines cumulées** renommées
- 161 cross-refs patches batch via script Python · 40 fichiers consumers patchés (12 skills + 5 doctrines sœurs + 4 slash commands + 5 manifests + 4 memory canons + R&D)
### Notes
- Pré-flight Phase 1 a révélé 2 garde-fous DÉPASSÉS sur lot 4 FULL · top doctrine 51.5% > cap 40% · replacements estimés 610 > cap 280 · décision Largo isolation v2.85.0.3a (decomposition-visibility seul) + v2.85.0.3b à venir (engagement-disclosure + schema-encoding)
- Tests non-régression INTENSIFS Phase 4 PASSÉS · build-manifest 81 skills · build-brand-snapshot _EXAMPLE 24 lines · spot-check 3 skills consumers (build-atlas-complete 13 refs · profile-audience 11 · mine-voc 8) tous OK
- 34 occurrences "decomposition-visibility-discipline" sans `.md` préservées en l'état (concept narrative · false positives intentionnels cohérents règle Phase 1.A initiale)
- Ratio observé lot 4a · 1.18:1 (190/161 · cohérent doctrine HIGH risk dense)
- Cumul 4 sprints rename · 19 doctrines · 779 replacements · 0 régressions
- D#458 captured · memory canon `v85_0_lite_lessons` mis à jour (lot 4a données)
- Backlog · v2.85.0.3b clôture chantier (engagement-disclosure + schema-encoding · 21/21 cumulé post-ship)

## [2.85.0.2] · 2026-05-20
### Changed
- **Rename lot 3/4** · 6 fichiers mid-stakes `*-discipline.md` → `*-doctrine.md` · `operational-system` · `onboarding-holistic` · `skill-routing` · `extension-discovery` · `progressive-cartography` · `update-distribution` · **18/21 doctrines cumulées** renommées
- 258 cross-refs patches batch · 85 fichiers consumers patchés
### Notes
- Pré-flight ciblé Phase 1 · 1 sub-agent Haiku · garde-fous PASSÉS (top doctrine 25.4% · replacements estimés 140)
- Tests non-régression Phase 3 PASSÉS · build-manifest 81 skills · build-brand-snapshot _EXAMPLE 24 lines · grep résiduel 0
- Ratio observé lot 3 · 1.05:1 (272/258 · plus dense qu'estimé 1.9:1 · pattern revisité pour lots futurs)
- Cumul 3 lots · 18 doctrines · 618 replacements · 0 régressions
- D#457 captured · memory canon `v85_0_lite_lessons` mis à jour
- Backlog · v2.85.0.3 lot 4/4 HIGH risk 3 doctrines (decomposition-visibility · engagement-disclosure · schema-encoding · validation runtime intensive obligatoire · lendemain matin frais)

## [2.85.0.1] · 2026-05-20
### Changed
- **Rename lot 2/4** · 6 fichiers mid-stakes `*-discipline.md` → `*-doctrine.md` dans `docs/system/` · `claude-md` · `skill-authoring` · `output-clarity` · `scope-extension` · `territory` · `entry-arc` · **12/21 doctrines cumulées** renommées
- 253 cross-refs patches batch via script Python · 75 fichiers consumers patchés (docs system + docs internal + manifests + skills + slash commands + CLAUDE.md root + memory canons + R&D)
### Notes
- Pré-flight ciblé Phase 1 · 1 sub-agent Haiku (~30s) · garde-fous tous PASSÉS (territory share 18% < cap 40% · replacements estimés 200 < cap 250 · false positives prose tolérables)
- Tests non-régression Phase 3 PASSÉS · build-manifest.py 81 skills + 92 jargon entries · build-brand-snapshot.py _EXAMPLE 24 lines · grep résiduel 0 occurrence (Round 1 suffisant)
- Calibration ratio cumulatif/replacements affinée · lot 1 = 2.4:1 (258/107) · lot 2 = 1.9:1 (477/253) · plus dense car mid-stakes runtime + sibling doctrines
- D#456 captured · memory canon `v85_0_lite_lessons` mis à jour
- Backlog · v2.85.0.2 lot 3/4 mid-stakes · v2.85.0.3 lot 4/4 HIGH risk (3 doctrines validation runtime intensive obligatoire · lendemain matin frais)

## [2.85.0] · 2026-05-20
### Changed
- **Rename lot 1/4** · 6 fichiers `*-discipline.md` → `*-doctrine.md` dans `docs/system/` · alignment naming convention voice-doctrine v2.84.1 politique linguistique FR/EN canon · `attribution-multitouch` · `brand-isolation` · `changelog` · `creative-testing` · `pacing` · `visual-identity`
- 107 cross-refs patches batch via script Python · 41 fichiers consumers patchés (docs system + docs internal + manifests + skills + slash commands + memory canons + R&D)
### Notes
- **Stratégie LITE** confirmée post-escalade garde-fous pré-flight Phase 1.A (3 sub-agents Haiku parallèle ont révélé 1066 cross-refs markdown + 170 non-markdown = ~1236 total · 6x estimation briefing 60-200) · scope réduit lot 1/4 (~258 refs cumulées) pour valider pattern · 15 doctrines restantes en lots dédiés v2.85.0.x sessions ultérieures
- Tests non-régression Phase 1.D PASSÉS · build-manifest.py 81 skills + 92 jargon entries · build-brand-snapshot.py _EXAMPLE 24 lines · grep résiduel 0 occurrence anciens noms
- 37 false positives "discipline" en prose préservés (concept doctrinal vivant · pas modifier)
- NEW `docs/internal/refactor/v2.85.0-rename-log.md` · journal sprint détaillé
- D#455 captured · 2 NEW memory canons (`doctrine_naming_canon` règle pérenne · `v85_0_lite_lessons` observations tactiques)
- Backlog v2.85.0.1-3 · 15 doctrines restantes en 3 lots successifs (lot 2 mid-stakes 6 · lot 3 mid-stakes 6 · lot 4 HIGH risk 3 doctrines avec validation runtime intensive)
- v2.85.1 propagation contenu reportée post-rename complet

## [2.84.4] · 2026-05-20
### Changed
- `README.md` · 4 patches mineurs application registre semi-public canon · acronymes DTC (ligne 3) et ROAS (ligne 9) développés à première occurrence · adjectif vague "Full honest audit" → "Detailed audit" (AP-VD-4) · cross-ref `docs/system/README.md` (doctrine interne leak) → `docs/system/extending.md` (cohérent allègement registre semi-public)
- `WELCOME.md` · audit conformity élevée pre-audit · ZÉRO patch structurel (15L très denses · em-dash zéro · acronymes universels · ton narratif allègement permis)
### Notes
- 3ème propagation downstream voice-doctrine v2.84.1 · trilogie de propagations doctrinales complétée (strict canon.md v2.84.3 + partiel lexicon.md v2.84.2 + semi-public README/WELCOME v2.84.4)
- Apprentissage cross-registres · voice-doctrine résiliente sur 3 registres canon distincts · doctrine guide application concrète selon registre cible · cadre canon validé via 3 propagations réelles
- D#454 captured

## [2.84.3] · 2026-05-20
### Changed
- `docs/internal/canon.md` refonte STRICT voice-doctrine v2.84.1 · 413L → 149L (-64%) · 2ème propagation downstream cadre canon · application reference-grade intégrale (P1-P5 + AP-VD-1à8 + FR/EN + casse + paramétrage + conventions typographiques)
### Added
- NEW section canon `Sens canon du mot 'canon'` · 7 sens MECE documentés (S1 doctrine verrouillée · S2 archétype pédagogique · S3 seuil CMR 95% · S4 formule OTRB · S5 référentiel partagé · S6 copy validée · S7 terminologie normalisée FR) avec marqueurs contextuels et exemples typiques · DÉSAMBIG-2 confirmé (polysémie documentée, pas rename)
- NEW `docs/internal/refactor/v2.84.3-preflight.md` · pré-flight consolidé 3 sub-agents Haiku parallèle (cartographie sens + cross-refs entrantes 32 + sortantes 39)
### Fixed
- Ref cassée · `docs/system/creative-formula.md` (path drift) → `resources/templates/creative-formula.md`
- Ref cassée · `GETTING_STARTED.md` (fichier absent) retirée et pointée vers `docs/README.md`
### Notes
- Audit ancres runtime · zéro skill runtime ne référence directement `docs/internal/canon.md` (5 skills + phantom slash-command pointent vers d'autres `*-canon.md` distincts) · seule ancre formelle préservée `§ Atlas brand` (référencée depuis `atlas-brand.md:78`)
- D#453 captured · NEW memory canon `canon_md_strict_canon`
- Backlog DÉSAMBIG-1.5 noté · rename ciblé S4 dominant ~1066 occurrences si polysémie insuffisante à l'usage (sprint dédié 8-12h post-distribution)

## [2.84.2] · 2026-05-20
### Changed
- `lexicon.md` user-facing refonte · 175L → 103L (-41%) · 1ère propagation downstream voice-doctrine v2.84.1 · application partielle scope (b) · FR/EN canon (opérateur, décomposition, etc) · AP-VD-4 adjectifs vagues retirés · AP-VD-6 zéro nom doctrine canon leaké · P1 précision dense · P3 phrases courtes · em-dash zéro · `vous`/`votre marque` registre opérateur préservés
### Removed
- DRGFP + Confidence propagation + Atlas 4 senses MECE + Lineage + Origin_axis + Schwartz entrées (jargon doctrinal surface opérateur ou specs internes R&D)
- Preamble CONTEXT/OBJECTIVE/TYPE/AUDIENCE/CANON INTERNE (overengineered) · footer narrative S53/S55 (versioning inline)
- Refs `docs/system/*-discipline.md` doctrines internes 6× (violations AP-VD-6)
### Notes
- 25 entrées core préservées (Brand, Produit, Offre, Audience, Persona, Pain point, Tension, Insight, JTBD, Angle, Axe créatif, Concept/Creative/Variant, Mécanique/Mechanism, Awareness, Atome irréductible, Landing page, Campagne, Test, Résultat, Apprentissage, Positioning, Territoire, Connected source)
- D#452 captured · cadre canon voice-doctrine v2.84.1 testé via propagation réelle

## [2.84.1] · 2026-05-19
### Changed
- `voice-doctrine.md` v2.84.0 → v2.84.1 · 5 patches post-audit Claude Web · NEW mini-section Registres canon (3 registres reference-grade · semi-public · runtime opérateur) · NEW section Conventions typographiques (séparateurs canon `·` `\|` `→` `↔` · em-dash interdit) · notes (rename pending v2.85.0+) cross-refs `*-discipline.md` · notes transparence P4 spécialise P1 + AP-VD-1/2/7 applications négatives · AP-VD-3 précision distinction AP-VD-8 · 150L pile sous cap claude-md-discipline 150
### Notes
- 21 fichiers `*-discipline.md` identifiés à renommer `*-doctrine.md` · sprint v2.85.0 dédié (cross-refs sibling + CLAUDE.md root + manifest skills)
- Rejet drift audit · frontmatter `***` était hallucination · file utilise déjà `---` YAML standard

## [2.84.0] · 2026-05-19
### Added
- NEW doctrine `voice-doctrine.md` · ton canon artefacts internes · 5 principes wording (P1-P5) · politique FR/EN canon (opérateur · décomposition · cartographie · territoire · doctrine vs discipline) · conventions casse (NOYAU/CONTEXTE/MODIFIEURS · NIVEAU 0/1-4/LIVE plafond 5-10) · famille paramétrage NEW (axe variable · paramétrage · paramétrer · pair canon cartographier ↔ paramétrer) · 8 anti-patterns (AP-VD-1 à AP-VD-8) · exception README/WELCOME semi-public
### Changed
- `docs/system/README.md` index · ajout `voice-doctrine` en Authoring infrastructure · `claude-md-discipline` + `changelog-discipline` listés (rattrapage) · count 24 → 27 doctrines
### Migration
- Aucune (cadre canon posé · pas de propagation lexicon/canon/doctrines existantes dans ce sprint · réécritures dédiées v2.84.x+)

## [2.83.0] · 2026-05-19
### Added
- NEW doctrine `changelog-doctrine.md` (cap 80L par release) · NEW `docs/internal/project-journal.md` (4270L préservés narrative archive)
### Changed
- `CHANGELOG.md` racine Keep-a-Changelog strict · `/version` + `/update` lisent CHANGELOG.md + manifests JSON
### Migration
- Ancien `CHANGELOG.md` 4270L → `docs/internal/project-journal.md`

## [2.82.1] · 2026-05-19
### Fixed
- Validation post-refactor v2.82.0 · zéro régression silencieuse · backward compat sémantique additive

## [2.82.0] · 2026-05-19
### Changed
- CLAUDE.md root refactor atomique 332L → 144L (-57%) · NEW doctrine `claude-md-doctrine.md` · NEW index `docs/system/README.md`

## [2.81.1] · 2026-05-19
### Added
- NIVEAU LIVE thinking aloud (DVD extension) · 7 skills consumers patched

## [2.81.0] · 2026-05-18
### Added
- NEW doctrine `entry-arc-doctrine.md` (4 portes MECE) · NEW skill `import-archive` · NEW M5b first deliverable

## [2.80.3] · 2026-05-18
### Changed
- /tour arc substance guidé (5 volets) · /about ton premium · HR-OHD-10 NEW

## [2.80.1] · 2026-05-18
### Changed
- /tour prose conversationnelle native (zero ASCII interface) · HR-OHD-9 NEW

## [2.80.0] · 2026-05-18
### Added
- NEW slash commands `/update` + `/version` · NEW doctrine `update-distribution-doctrine.md` · NEW migrations framework · GitHub Releases tags v2.65 → v2.79.5

## [2.79.5] · 2026-05-18
### Added
- NIVEAU 0 paramètres décomposés canon (DVD + EDD extensions) · 6 skills patched

## [2.79.4] · 2026-05-17
### Added
- NEW slash command `/about` · NEW doctrine `pain-benefit-chain.md` · /tour intro Vercel/GitHub-style

## [2.79.3] · 2026-05-17
### Added
- NEW doctrines `onboarding-holistic-doctrine.md` + `engagement-disclosure-doctrine.md` · /tour panorama 7 territoires · 6 orchestrators disclosure

## [2.79.2] · 2026-05-17
### Added
- NEW doctrine `output-clarity-doctrine.md` · /phantom + /bird + /breakdown refactor

## [2.79.1] · 2026-05-17
### Added
- NEW doctrine `decomposition-visibility-doctrine.md` (4 NIVEAUX matricial) · 4 skills patched

## [2.79.0] · 2026-05-17
### Added
- 3 NEW skills brand strategy (positioning-canvas · brand-voice · voice-consistency) · 6 Mark+Pearson archetypes

## [2.78.0] · 2026-05-17
### Added
- 5 NEW skills ops paid · 3 NEW doctrines (pacing · creative-testing · attribution-multitouch) · magic keyword cleanup 64 substitutions

## [2.77.0] · 2026-05-17
### Added
- NEW doctrine `skill-routing-doctrine.md` · NEW slash commands `/scope` + `/bird` · 697 em-dashes purgés

## [2.76.0] · 2026-05-16
### Changed
- /tour refactor pro-grade 10 patches (institutional voice + smart suggestions + dejargonisation)

## [2.75.1] · 2026-05-16
### Changed
- /tour Milestone 6 enriched (5 universal entry points + 3 canon principles)

## [2.75.0] · 2026-05-16
### Added
- NEW doctrine `extension-discovery-doctrine.md` · 4 orchestrators extension_hooks

## [2.74.1] · 2026-05-16
### Fixed
- Cleanup parasites (doublons Stepprs · refs canon paths · 255 em-dashes éliminés)

## [2.74.0] · 2026-05-16
### Added
- NEW slash command `/lexicon` (13 magic keywords canon) · decompose-ad FIT AVEC TA BRAND

## [2.73.0] · 2026-05-16
### Added
- NEW skill `adapt-from-competitor` · decompose-ad v2.0.0 grille ANATOMIE 3 niveaux

## [2.72.1] · 2026-05-16
### Fixed
- /tour Milestone 6 ligne 208 · 3 cohérence corrections

## [2.72.0] · 2026-05-16
### Added
- NEW skill `produce-decomposition-ecr` · ECR runtime methodology · anti-hallucination canon `_EXAMPLE/`

## [2.71.1] · 2026-05-16
### Added
- breakdown.md topics 11 intelligence + 12 apprentissage (transverse dimensions)

## [2.71.0] · 2026-05-16
### Added
- NEW doctrine mère `operational-system-doctrine.md` (ECR × Rules × Templates × Metrics × Rituals)

## [2.70.0] · 2026-05-16
### Added
- NEW slash command `/breakdown stepprs {topic}` (vitrine pédagogique · 7 topics)

## [2.69.1] · 2026-05-16
### Changed
- _EXAMPLE/stepprs UX live patch (3 layers · 9 frictions captured)

## [2.69.0] · 2026-05-16
### Added
- NEW skill `trendtrack-enrich-brand` (Market Intelligence Layer first runtime brick)

## [2.68.0] · 2026-05-15
### Added
- NEW doctrine `progressive-cartography-doctrine.md` (4 phases · hypothesis confidence 0.5 valid)

## [2.67.0] · 2026-05-15
### Added
- NEW doctrine `territory-doctrine.md` · layer field 67 skills

## [2.66.0] · 2026-05-15
### Breaking
- sync-notion-atlas v1.x → v2.0.0 dual-direction sync (Phase B push runtime exec-ready)

## [2.65.0] · 2026-05-15
### Added
- NEW doctrine `scope-extension-doctrine.md` (canon élasticité opérateur)

Release tags · `https://github.com/Largo2z9/phantomos/releases/tag/v{version}`.
