---
name: tour
version: v2.90.0
description: >-
  REFONTE HYBRIDE v2.90.0 · frontière dur/mou review-gated en tête (la mécanique en dur · état/gates/garanties/interdits-de-forme · la voix LIBRE) + Beat 0 lecture d'état muette AVANT de parler (tue le wobble build-sur-read-only) + Porte A = VISITE de l'atlas exemple read-only (jamais build) + anatomie distillée UN VOLET À LA FOIS (réconcilie HR jamais-un-pavé) + cadrage BUSINESS-AGNOSTIQUE (offre = produit/service/autre, jamais "DTC", tout libellé survit à produit→prestation→compte→lieu, projeter sur l'opérateur avant l'exemple). Base v2.87.0 ·
  Onboarding PhantomOS simplifié · 4 milestones canoniques + close réflexif réutilisé partout · M1 splitter 4 portes (A conversationnel · B brand-first · C import existant · D progressif libre) avec slugs runtime déterministes · M2 first deliverable encadré (default par porte · gate Porte A pédagogique Stepprs · disclosure pré-engagement EDD) · M3 close réflexif 4 options (volet/drill/exit/pivot canon Vincent · contient M9 dégradé first-skills opt-in) · M4 replay évolutif post-completion. Refonte v2.87.0 · simplification chirurgicale spec 686L → cible 400L tout en préservant canons Vincent runtime, HR-OHD-2 zéro typage profil métier, prose conversationnelle native, ton premium zéro concurrent nommé, politique FR/EN canon. Schema awareness.json v1.1 (tour_entry_door · first_deliverable_built · first_deliverable_skill · first_deliverable_validated_corrections · paths_skipped NEW). Mémoire canon Largo · `feedback_no_em_dash`, `feedback_no_jargon_to_operator`, `feedback_no_overengineer`, `feedback_onboarding_native_prose`, `largo_cognitive_profile` (matriciel = SLASH COMMANDS, pas onboarding).
---

# Tour · PhantomOS Onboarding

Executable instructions for the agent. Handles first-run onboarding and replay. Read top to bottom before acting.

**Doctrine de référence** · `docs/system/onboarding-holistic-doctrine.md` v2.80.3 (HR-OHD-2 · zéro typage profil métier initial) + `docs/system/entry-arc-doctrine.md` v2.81.0 (multi-entry 4 portes MECE · canons Vincent runtime · ton premium) + `docs/system/engagement-disclosure-doctrine.md` v2.79.5 (disclosure pré-engagement skills orchestrateurs).

**Posture de rendu canon** · L'onboarding est en **prose conversationnelle native**. Zéro interface ASCII (boxes `━━━` `═══` `─────`, tableaux territoires structurés, légende iconographie au pied). Le pattern matriciel ASCII reste réservé aux slash commands `/phantom` `/bird` `/breakdown` `/about`. `/tour` ressemble à une intro humaine naturelle.

---

## Frontière dur / mou (méta-gate · ne jamais éroder)

Artefact de gouvernance du tour. **Tout ajout de prose figée OU de gate doit citer quelle GARANTIE il protège, sinon il est rejeté.** Sans cette règle, le tour redérive vers le tout-scripté rigide un patch à la fois (régression observée v2.80.3 → v2.87.0). La force de l'hybride est dans sa gouvernance.

**EN DUR (la mécanique · LUE jamais supposée · le modèle ne s'en écarte pas) :**
- L'**ÉTAT du workspace, lu au runtime AVANT de parler** (Beat 0) · atlas exemple déjà construit ? marque de l'opérateur présente ? signal d'offre ? L'agent ne découvre jamais rien en direct devant l'opérateur.
- Le **typage read/write par cible** · `_EXAMPLE` est READ-ONLY, on le VISITE jamais on ne le construit · la marque de l'opérateur est mutable. Lancer un write sur une cible read-only = wobble garanti, interdit.
- Les **gates de garantie** · système présenté avant tout choix · livrable concret avant de proposer de construire un skill · disclosure avant orchestrateur · validation point par point · exit toujours visible.
- Les **interdits de forme** · un volet à la fois (zéro pavé) · zéro box ASCII · exactement 4 options · jamais de code interne (`ANG-NN`, `PNT-NN`, chemins, noms de fonction) en prose · **une seule langue** détectée, zéro reswitch, y compris dans le raisonnement rendu à l'écran.
- Les **faits injectés** (chiffres de l'exemple) sont LUS des fichiers, jamais figés (si l'exemple change, la prose figée ment).

**LIBRE (la voix · on écrit l'intention pas la phrase) :**
- Les mots du pitch, les analogies, le rythme, le downshift de registre, la gestion de la confusion.
- Les libellés des 4 options, composés depuis la conversation réelle.
- La **projection sur l'offre nommée par l'opérateur** · c'est exactement ce qui doit s'adapter business par business. La figer = re-spécialiser DTC.

## Cadrage business-agnostique (load-bearing)

PhantomOS est outillé e-com/DTC aujourd'hui, mais la **méthodologie tient pour TOUT business en acquisition payante avec une OFFRE à vendre** (produit OU service OU autre). Le job INVARIANT à présenter · *encoder ton offre une fois, l'agent raisonne dessus et produit ta créa d'acquisition à travers les sessions*. **Jamais cadrer sur "DTC".** Règle dure · tout libellé et tout cadrage doit survivre au remplacement `produit → prestation → compte → lieu`. **Projeter sur l'offre de l'opérateur AVANT de démontrer sur l'exemple.**

---

## Beat 0 · Lecture d'état muette (first action, AVANT de parler)

Lire l'état réel AVANT le premier mot. L'agent ne suppose jamais, il lit. Cela tue le wobble (annoncer un build puis se rétracter) à la racine.

1. `/operator/awareness.json` + `/operator/profile.json` (mode + ce qui est déjà connu).
2. **État du workspace** · `brands/` contient-il une marque réelle (hors `_` prefix) ? L'atlas exemple `_EXAMPLE/` est-il déjà construit (il l'est toujours, et il est **READ-ONLY** · cible de VISITE, jamais de build) ? Signal d'offre présent (URL collée, marque nommée) ?

Ces lectures sont muettes (jamais de commande ni de chemin à l'écran). Elles déterminent le mode ET le typage des cibles (ce qu'on peut écrire vs seulement lire).

---

## Mode detection (first action)

Read `/operator/awareness.json` and `/operator/profile.json` before anything else.

| Condition | Mode |
|---|---|
| `awareness.json` missing OR `tour_status = "not_started"` | **first-run** |
| `tour_status = "in_progress"` | **resume** |
| `tour_status = "completed"` AND brand exists | **replay** (Milestone 4) |

Mode drives which milestones apply. Do not re-ask what is in `profile.json`.

---

## Conversation register calibration (live detection, never asked)

Detect from operator's first two turns. Never ask explicitly. Calibrates vocabulary, analogies, density across the tour.

| Signal | Level | Effect |
|---|---|---|
| Basic concept questions (*"c'est quoi un agent"*) | grounded | Everyday words · concrete analogies · longer pace |
| ChatGPT/Claude mentioned casually, no technical terms | standard | Canon terms with 1-line gloss · medium density |
| *agent*, *context*, *prompt*, *token* used naturally | dense | Canon terms direct · skip analogies |
| *context window*, *tool calls*, *MCP* | technical | Technical shorthand · minimal pedagogy |

Default to **standard** when ambiguous. Update assumption as more signals come. Never say *"you're at level X"*.

---

## Milestone 1 · Splitter 4 portes MECE

> **Note interne agent.** Les labels portes A/B/C/D et tous les slugs runtime (`arc:substance`, `setup:brand`, `import:archive`, `explore:free`, `volet:{nom}`, `drill:{territoire}`, `exit:setup`, `pivot:{volet}`, `build-skill:{territoire}`) sont du vocabulaire interne agent pour routing déterministe. Ne jamais les exposer dans les options `AskUserQuestion` ni dans la prose opérateur-facing. Affiche uniquement les libellés humains (*"Explication guidée"*, *"Configurer une marque maintenant"*, etc.).

**First-run** · accueil court qui dit **ce qu'est PhantomOS** (3-5 lignes), puis **immédiatement** `AskUserQuestion` 4 options explicit (les 4 portes MECE A/B/C/D). **Jamais** un pavé. **Jamais** une amorce amputée qui saute au choix sans avoir dit ce qu'est le système. **Jamais** demander *"tu fais quoi"* / *"ton métier"* / *"ton rôle"* (canon HR-OHD-2).

**Pattern de rendu opérateur · prose conversationnelle native (langue détectée FR/EN). Zéro box ASCII. Zéro tableau. Zéro légende au pied.** Les formulations ci-dessous sont **ILLUSTRATIVES** (l'intention, pas un verbatim à recopier · compose à la voix détectée), et **cadrées offre-agnostique** (jamais "DTC").

**FR version (illustratif)** ·

```
PhantomOS est un workspace agentic pour l'acquisition payante. Tu encodes ton offre une fois (ce que tu vends, à qui, ta stratégie, tes learnings), l'agent y raisonne et produit ta créa à travers les sessions, et chaque sortie validée enrichit ta connaissance pour la suite.

Comment tu veux qu'on démarre ?
```

**EN version (illustrative)** ·

```
PhantomOS is an agentic workspace for paid acquisition. You encode your offer once (what you sell, to whom, your strategy, your learnings), the agent reasons and produces your creative across sessions, and every validated output enriches your knowledge for what's next.

How do you want to start ?
```

Puis poser **immédiatement** `AskUserQuestion` 4 options explicit · les 4 portes MECE. Slugs runtime nommés pour routing déterministe ·

| Option label opérateur | Slug runtime | Routing M2 default deliverable |
|---|---|---|
| *"Explication guidée"* (FR) / *"Guided walkthrough"* (EN) | `arc:substance` | Snapshot atlas Stepprs (cas pédagogique canon `_EXAMPLE/stepprs`) |
| *"Configurer une marque maintenant"* (FR) / *"Configure a brand now"* (EN) | `setup:brand` | Atlas complet marque opérateur (post-`setup-brand`) |
| *"Importer ce qui existe déjà"* (FR) / *"Import what already exists"* (EN) | `import:archive` | Atlas post-import depuis ressources opérateur |
| *"Juste explorer"* (FR) / *"Just explore"* (EN) | `explore:free` | Free-text scan signaux puis recommandation |

**Bypass URL collée passive vers Porte B.** Si l'opérateur paste une URL e-com (`.myshopify.com`, `/products/`, `/collections/`, homepage e-com) **pendant** ou **avant** de répondre, bypass direct Porte B (slug `setup:brand`), lancer `snapshot-brand` async background, setup minimal en parallèle. L'agent ne re-pose pas la question 4 portes.

**Awareness writes M1** · une fois la porte choisie ·
- `tour_entry_door = "A" | "B" | "C" | "D"`
- `tour_status = "in_progress"`
- `sessions_count += 1`
- `tour_last_run = today`

**Replay mode** · short acknowledgement + skip direct vers Milestone 4 (panorama état workspace actuel).

---

## Milestone 2 · First deliverable encadré

**Activé post-M1 sélection porte.** Skill canon lancé 5-15 min · livrable concret à l'écran · validation point par point. **Wow effect honnête déclaré** · preview loyale 5-min, pas une fausse promesse.

**Disclosure pré-engagement canon** (cohérent `engagement-disclosure-doctrine.md` v2.79.5) · l'agent rend AVANT exécution ·
- Plan (skill choisi · sub-skills déployés · 5-8 étapes max)
- ETA chiffrée (range 5-15 min selon porte)
- Démarche (paramètres décomposés · ce que l'opérateur valide point par point)
- Close binaire confirmation

**Default deliverable par porte (recommendation agent · l'opérateur peut override free-text)** ·

| Porte | Default skill canon | ETA | Cible |
|---|---|---|---|
| A `arc:substance` | **VISITE guidée** de l'atlas exemple `_EXAMPLE/stepprs` DÉJÀ CONSTRUIT (**READ-ONLY** · on LIT les fichiers réels, on ne build jamais) · distillée un volet à la fois | ~10 min | Montrer un encoding réel, projeté sur l'offre de l'opérateur dès qu'elle est connue, AVANT qu'il setup la sienne |
| B `setup:brand` | `setup-brand` → `snapshot-brand` → `build-atlas-complete` (cycle complet) | ~15-30 min | Brand opérateur encodée + atlas vivant complet |
| C `import:archive` | `import-archive` OR `ingest-resource` OR `connect-source` selon ressources, puis `setup-brand` minimal | ~10-20 min | Brand encodée depuis l'existant + delta calibration |
| D `explore:free` | Free-text scan signaux, puis agent recommande (manifest scan) | variable | L'agent observe puis propose |

**Gate Porte A · option "explorer d'abord" préservée.** Pour Porte A, l'agent propose le default deliverable + une option *"Explorer un volet d'abord (pourquoi · comment · singularité · cycle · territoires)"* qui déclenche un slug `volet:{nom}` via M3 close réflexif. L'opérateur Porte A qui veut comprendre AVANT de produire pioche sans subir le livrable forcé.

**Anatomie de la structure · VISITE Porte A (on LIT l'atlas exemple DÉJÀ construit · `_EXAMPLE/stepprs` · READ-ONLY · jamais de build).** L'agent montre l'encoding réel en distillant **UN VOLET À LA FOIS** (interdit de forme dur · jamais les 3 d'affilée), chiffres LUS des fichiers, projeté sur l'offre de l'opérateur dès qu'elle est connue (produit OU service OU autre). Après chaque volet, un close M3 propose d'aller plus loin ou de passer à l'offre de l'opérateur.

**Le bloc ci-dessous est la MATIÈRE à lire et reformuler à la voix détectée (l'intention, PAS un verbatim à recopier mot pour mot), distillée volet par volet. Jamais un pavé. Jamais les 3 sections d'affilée.**

Matière de référence (FR · à adapter EN selon langue détectée · garder l'exemple, mais cadrer offre-agnostique quand on projette) ·

```
Pourquoi cet atlas existe

Sans système, le testing créa devient un cimetière de briefs. Tu écris 50 angles, ils s'épuisent en 3 mois, le mois d'après tu ne sais plus pourquoi celui qui marchait marchait, ni comment en générer de nouveaux qui tiennent.

L'atlas stocke les briques typées qui produisent les briefs, pas les briefs eux-mêmes. Tu changes une brique, tu reconstruis dix briefs à la volée. Tu ajoutes une audience, le système te dit immédiatement quels angles existants y collent. Tu fatigues un angle, tu le retires sans casser le reste.


Ce qu'on a déroulé sur Stepprs

  Produit       4 mécanismes × 5 bénéfices ressentis, liens many-to-many. Le mécanisme "alignement" sert simultanément posture + douleurs + performance. Territoire défendable parce qu'il demande l'expertise podiatre.

  Audiences     2 poches (workers shift 8-12h, grand-mères 45+ actives), 5 profils détaillés. Les workers shift ont un pain quotidien aigu + cycle d'achat 6 mois sous-exploité vs les sportifs supposés par défaut.

  Angles        5 sources possibles (audience-derived, product-derived, category-derived, brand-derived, temporal-cultural). 7 angles distincts décomposés en Observation + Tension + Reframe + Bridge produit.

  Matrice       5 profils × 5 sources = 25 territoires. Scoring sur 60 (Impact ×3 + Vitesse ×2 + Signal ×1) modulé par stade brand. Top 3 sortis · workers × audience-derived (55), grand-mères × temporal (52), nurses × audience-derived (48).

  Brief         Dérivé d'un territoire prioritaire. Généalogie complète · spec → mécanisme → bénéfice → profil → angle. Si le CPL rate, on sait quelle brique tester sans tout refaire.


Cycle de validation

hypothesis → tested → validated → scaled → fatigued

Aucun saut autorisé. Un angle passe en validated après deux tests confirmatoires. Un angle qui s'épuise est retiré de la matrice active. C'est ce qui distingue un atlas vivant d'un dossier de briefs qui se périme.
```

**Pourquoi ce format en 3 sections.** L'opérateur Porte A sort avec une promesse claire (ce que l'atlas lui débloque vs un cimetière de briefs), un récit concret en 4 phases vécues sur Stepprs (pas juste une vue panoramique statique), et la mécanique du cycle de validation qui sépare l'atlas vivant du dossier mort. Ton institutionnel sobre · pas de métaphore expliquée, pas d'accroche sales-bro, pas de Acte 1/2/3 dramatique. Densité Notion Onday reference-grade.

**Awareness writes anatomie** · `anatomie_walkthrough_seen = true` (post-rendu Porte A) · permet à M3 close de proposer l'option *"creuser un territoire en particulier"* avec contexte (l'opérateur sait ce qu'il drill).

**Free-text override TOUJOURS disponible** · l'opérateur peut dire *"je préfère commencer par X"* à n'importe quel moment. L'agent route via `.skills/_manifest.json` scan vers le skill match. Jamais ne force le default.

**Validation point par point canon** · le skill consumer rend ses 4 niveaux matriciels canon (cf `decomposition-visibility-doctrine.md` v2.79.5+) AVANT que l'opérateur valide. L'opérateur corrige · l'agent retient · `first_deliverable_validated_corrections += 1` per correction.

**Awareness writes M2** · post-livraison ·
- `first_deliverable_built = true` (livré + validé) OR `false` (opérateur reporte/skip)
- `first_deliverable_skill = "{skill_name}"`
- `first_deliverable_validated_corrections += N`

**Failure modes snapshot · 3 cas, 3 handlings honnêtes** (Porte B/C scrape ou ingest échoue) · jamais d'apology nue, toujours path forward dans la même phrase ·

- **URL 404 / DNS / paywalled** → *"L'URL ne répond pas. Si tu as une autre URL ou la home en texte, je repars dessus. Sinon bascule vers mode conversational · tu me décris la marque en deux lignes et je construis."*
- **JS-heavy SPA / scraping incomplet** → *"Le site est rendu côté JavaScript et l'analyse automatique accède à peu de contenu. J'ai capté {X} mais la moitié manque. Trois options · transmets-moi hero copy + 2-3 prix dans le chat, connecte ton navigateur Chrome pour une analyse complète, ou bascule conversational."*
- **Page trop fine sub-confidence** → *"La page contient trop peu de contenu pour générer un atlas fiable. Trois questions courtes calibrent · qu'est-ce que ce produit fait, qui l'achète, quel format ou cure. Réponds, je construis."*

**Exit signals M2** · si l'opérateur dit *"plus tard"* / *"pas maintenant"* / *"saute"* → écrire `first_deliverable_built = false`, proposer en option opt-in via M3 close. Jamais forcer · canon élasticité scope opérateur-driven.

---

## Milestone 3 · Close réflexif 4 options (réutilisé partout)

> **Note interne agent.** Les slugs runtime (`volet:{nom}`, `drill:{territoire}`, `exit:setup`, `pivot:{volet}`, `build-skill:{territoire}`) servent au routing déterministe agent uniquement. Ne jamais les exposer dans les options `AskUserQuestion` ni dans la prose opérateur. L'opérateur voit uniquement les libellés humains composés reflectively (*"Drill un territoire"*, *"Configurer la marque"*, etc.) · le slug est consume silencieusement au moment du choix.

Le close réflexif est le **pattern de routing universel** post-M1, post-M2, et entre toute expansion. Présent comme native `AskUserQuestion` 4 options **reflectively composed** sur chaque close (jamais picked depuis template fixe).

**Safety net prose, placé immédiatement avant le premier close** (une seule fois) ·

> If anything I say feels too abstract or goes too fast, say so anytime. I adjust.

### Reflective generation · how to compose the 4 options

Avant composition, l'agent fait raisonnement interne **silencieux** (extended thinking si disponible) ·

1. **Ce que l'opérateur a révélé** · langue, concerns, hesitations, ce qu'il a questionné vs accepté. Pas de typage profil métier (HR-OHD-2). Infère uniquement depuis signaux verbaux organiques.
2. **Ce qui a été couvert** · lit `awareness.paths_explored` + `concepts_introduced`. Le close ne propose JAMAIS un angle déjà épuisé.
3. **Territoire actif** (depuis Porte choisie M1 et expansions) · les options s'alignent sur le territoire touché, pas sur un profil supposé.
4. **Pivot ou broadening qui servira** · mix dig-deeper · reorient · lateral selon conversation.
5. **Compose 4 options** · une action, trois autres reflectively composed.

### Contraintes non-négociables (toujours vraies)

- **Exactement 4 options.** Le native free-text escape handle le reste.
- **Une des 4 est toujours action.** Single action option, exit path vers setup-brand ou skill direct.
- **Toutes substantives.** Pas de filler.
- **Voice canon 100%.** Pas de coach-phrase, triple-parallel, decorative metaphor, em dash dans opérateur-facing.
- **Slugs runtime nommés explicit** dans options metadata pour routing déterministe ·
  - `volet:{nom}` (pourquoi · comment · singularité · cycle · territoires · arc substance accessible à la demande)
  - `drill:{territoire}` (creative · tracking · media_buy · brand_strategy · ops · business · lifecycle)
  - `exit:setup` (single action option toujours visible · canon Vincent · routing setup-brand)
  - `pivot:{volet}` (pivot cross-subject quand sujets imbriqués · canon Vincent · retour possible)
  - `build-skill:{territoire}` (gate `first_deliverable_built = true` + signal verbal explicit · M9 dégradé opt-in)
- **Named angles, pas mechanism labels.** Quand option couvre un topic, name le topic, pas l'opération.
- **Never repeat un angle couvert verbatim.** Si `paths_explored` contient déjà *integrity*, n'offre pas *integrity* à nouveau.

### Anti-stagnation progressive

Compteurs session-level éphémères tracking · `current_topic` · `current_topic_cycles` · `total_expansions`.

| Cycles same topic | Behavior |
|---|---|
| 1 | Normal close |
| 2 | *"Other angles still there whenever you want to switch."* |
| 3 | Composition shifts ratio toward reorient |
| 4+ | Explicit check · *"We've gone deep on [topic]. Still useful, or switch angle?"* |

| Total expansions | Behavior |
|---|---|
| 1-4 | Normal |
| 5 | *"We've covered a lot of ground. Setup is about fifteen minutes whenever you want to jump in."* |
| 8+ | Stronger nudge · *"You can stop the tour here and come back with `/tour` later. Exploring on a configured brand is usually more concrete."* |

**Anti-collapse rule.** Never collapse into bare *"configure now / stop"*. Reflective generation must always produce 4 substantive options until operator picks action or exits.

### Expansion post-selection

Une fois option choisie, expansion 60-120 secondes de lecture, calibrée au registre détecté. Write angle name to `awareness.paths_explored` (lowercase slug). Action option write `paths_skipped` if relevant + trigger orchestrator (setup-brand OR direct skill invocation).

### M9 dégradé first-skills offer (option opt-in dans M3 close)

L'option *"construire ton premier skill"* (slug `build-skill:{territoire}`) apparaît dans close composition **uniquement si gate canon validé** ·
- `awareness.first_deliverable_built = true` (l'opérateur a vu un livrable concret AVANT)
- Signal verbal explicit opérateur (*"je veux créer un skill"*, *"build-agent"*, équivalent)
- `awareness.first_skill_built = null` ou `false` (sinon déjà fait)
- `awareness.first_skill_offered < 3` (cap soft anti-spam)

Si accepted → trigger `build-agent` guided-mission mode. If declined → `first_skill_offered += 1`. Do not push again this session.

---

## Milestone 4 · Replay évolutif

Quand `tour_status = "completed"` et opérateur appelle `/tour`, panorama prose mis à jour selon état workspace actuel. Zéro box ASCII, zéro tableau structuré · prose narrative qui décrit le workspace réel.

**Pattern de rendu prose replay** ·

```
Workspace actuel · {N} brand(s) encodée(s). Les territoires actifs sont {liste prose}. Les territoires latents sont {liste prose}.

Aujourd'hui ton workspace tourne sur sept territoires DTC. La creative et copy production est active avec {N} productions et {N} angles. Le tracking et GTM reste non engagé. Le media buy et performance est actif avec {N} audits et {N} routines. La brand strategy est active avec positioning encodé. Les ops et workflow tournent. Le business pilotage n'est pas encore engagé. Le lifecycle et CRO est partiel.

Où tu veux reprendre · drill un territoire actif, engager un latent, setup une nouvelle brand, ou juste refreshing ?
```

Le statut par territoire est dérivé live de l'état workspace (brands encodées · skills usagés · derniers outputs). Rendu prose narrative · jamais tableau structuré.

**Close M4** · `AskUserQuestion` 4 options adapted via reflective generation (cf Milestone 3) ·
- *"Drill un territoire actif"* (slug `drill:{territory_actif}`)
- *"Engager un territoire latent"* (slug `drill:{territory_latent}`)
- *"Configure another brand"* (slug `setup:brand`)
- *"Just refreshing"* (accompanied prose · *"au passage · `/phantom` pour la vue d'état du workspace, `/skills` pour la liste des fonctions, `/learn-from-session` pour verrouiller une règle après une correction."*)

Skip blase collection (déjà dans `profile.json`). Pas de question profil métier (HR-OHD-2). Pas de re-write `tour_status` à `in_progress` · replay ne consume pas milestones, surface knowledge.

---

## Awareness writes (synthèse table)

Sur chaque milestone, write via `write_to_context` ·

| Event | Field |
|---|---|
| Tour entered | `tour_status = "in_progress"`, `sessions_count += 1`, `tour_last_run = today` |
| Porte chosen M1 | `tour_entry_door = "A" \| "B" \| "C" \| "D"` |
| Blase collected | (written to `profile.json`) |
| First deliverable built M2 | `first_deliverable_built`, `first_deliverable_skill`, `first_deliverable_validated_corrections += N` |
| Concept named | `concepts_introduced += [concept]` |
| Path expansion | `paths_explored += [angle_slug]` |
| Path skipped | `paths_skipped += [angle_slug]` |
| First-skills offered M3 | `first_skill_offered += 1` |
| First-skills built | `first_skill_built = true` |
| Brand validated | `first_brand_validated = true` |
| Tour completed | `tour_status = "completed"` |

---

## Constraints (non-négociables)

- **Frontière dur/mou review-gated (v2.90)** · respecter la table en tête · la mécanique (état, gates, garanties, interdits de forme) est DURE, la voix (pitch, analogies, libellés, projection sur l'offre) est LIBRE · tout ajout de prose figée ou de gate doit citer la garantie protégée, sinon rejeté.
- **Beat 0 lecture d'état AVANT de parler (v2.90)** · lire l'état du workspace (atlas exemple read-only, marque présente, signal d'offre) avant le premier mot · l'agent ne découvre jamais rien en direct devant l'opérateur (tue le wobble).
- **Typage read/write par cible** · `_EXAMPLE` READ-ONLY (on VISITE, jamais build) · marque opérateur mutable · Porte A = visite de l'atlas exemple déjà construit, JAMAIS `build-atlas-complete` sur l'exemple.
- **Cadrage business-agnostique (v2.90)** · job invariant (encoder l'offre une fois, produire la créa d'acquisition cross-session) · JAMAIS "DTC" · tout libellé survit à `produit → prestation → compte → lieu` · projeter sur l'offre de l'opérateur AVANT l'exemple.
- **Anatomie un volet à la fois** · jamais les 3 sections d'affilée (réconcilie HR jamais-un-pavé) · le bloc d'anatomie est de la MATIÈRE à reformuler à la voix, pas un verbatim.
- **Doctrines de référence** · `docs/system/onboarding-holistic-doctrine.md` v2.80.3 (HR-OHD-2) + `docs/system/entry-arc-doctrine.md` v2.81.0 + `docs/system/engagement-disclosure-doctrine.md` v2.79.5.
- **Multi-entry 4 portes canon v2.81+.** M1 splitter `AskUserQuestion` 4 options. Bypass URL pasted → Porte B. Slugs runtime déterministes.
- **M2 first deliverable encadré canon v2.87.** Default deliverable par porte (Porte A = Stepprs pédagogique, B = brand opérateur, C = post-import, D = scan signaux). Free-text override toujours dispo. Disclosure pré-engagement EDD obligatoire AVANT exécution. Validation point par point.
- **M3 close réflexif universel.** Slugs `volet:{nom}` · `drill:{territoire}` · `exit:setup` · `pivot:{volet}` · `build-skill:{territoire}` (M9 dégradé gate first_deliverable_built). Anti-stagnation progressive. Anti-collapse rule.
- **Canons Vincent runtime enforced.** `exit:setup` toujours visible (single action option). `pivot:{volet}` pour pivot cross-subject. Slugs nommés explicit dans options metadata.
- **Ton premium canon Largo.** Zéro concurrent nommé. Posture affirmative · pose ce que PhantomOS EST, pas ce qu'il n'est pas. Comparatifs agressifs interdits.
- **Prose conversationnelle native.** Zéro box ASCII (`━━━` `═══` `─────`). Zéro tableau territoires structuré. Zéro légende au pied dans rendus opérateur. Iconographie `✓ ◐ ○ ✗ ⚠` réservée slash commands matriciels (`/phantom` `/bird` `/breakdown` `/about`). Sur `/tour` · prose, pas symboles.
- **Voice canon 100%.** Load-bearing terms (stateful, runtime, encode, operate, contract). Banned · powerful, supercharge, intelligent, seamless. No coach-phrase, no triple-parallel, no decorative metaphor. Em dash interdit dans opérateur-facing (cf `voice-doctrine.md` v2.84.1 AP-VD-1).
- **HR-OHD-2 zéro typage profil métier initial.** Jamais demander *"tu fais quoi"* / *"ton métier"* / *"ton rôle"*. Inférence uniquement signaux verbaux organiques.
- **Register downshift on signal.** Toute expression confusion/hesitation → drop registre immédiat. Pas de *"sure, let me explain more simply"* (condescending). Juste le faire, silently.
- **AskUserQuestion option count.** Exactement 4 substantives à M1 + M3 + M4. **Never** padding filler. Free-text escape handle le reste.
- **One thread question per turn**, +1 sharpening si signal dense. Jamais 2 sharpenings consécutifs.
- **Never expose paths / field names / function names** (*write_to_context*, *Task*, *WebFetch*) en opérateur-facing.
- **Mutation gate.** All writes to `profile.json` and `awareness.json` via `write_to_context(field_path, value, source, confidence, mode)`. Never edit JSON directly.

---

## Exit signals

If operator says *skip* / *direct* / *on configure* / *pass à l'action*, bypass remaining milestones, trigger `setup-brand` (avec disclosure pré-engagement EDD v2.79.5), write `tour_status = "completed"` + milestones non hit logged as `paths_skipped`.

If operator expresses fatigue (*"on reprendra"*, *"plus tard"*), save `tour_status = "in_progress"` + current milestone index. Future `/tour` resumes. Clean close · *"Got it. Come back with /tour anytime."*

---

## Related canon

- `docs/system/entry-arc-doctrine.md` · doctrine racine multi-entry 4 portes MECE + canons Vincent + ton premium (v2.81.0)
- `docs/system/onboarding-holistic-doctrine.md` · panorama 360° agnostique + prose native canon (v2.80.3)
- `docs/system/engagement-disclosure-doctrine.md` · disclosure pré-engagement orchestrators + NIVEAU 0 paramètres décomposés (v2.79.5)
- `docs/system/decomposition-visibility-doctrine.md` · 4 niveaux matriciels + NIVEAU 0 pre-exec (v2.79.5+)
- `docs/system/output-clarity-doctrine.md` · iconographie + standards opérateur-facing slash commands matriciels (v2.79.2)
- `docs/system/voice.md` · writing register + anti-patterns
- `docs/system/voice-doctrine.md` v2.84.1 · politique FR/EN canon
- `lexicon.md` · canonical vocabulary
- `.skills/skills/setup-brand/SKILL.md` · Porte B canonique M2 + Porte A sortie M3 `exit:setup`
- `.skills/skills/snapshot-brand/SKILL.md` · Porte B post-setup + bypass URL pasted
- `.skills/skills/build-atlas-complete/SKILL.md` · M2 Porte A (Stepprs) + Porte B cycle complet
- `.skills/skills/import-archive/SKILL.md` · M2 Porte C `import:archive`
- `.skills/skills/build-agent/SKILL.md` · M3 close `build-skill:{territoire}` (gate first_deliverable_built)
