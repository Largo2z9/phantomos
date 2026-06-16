# Onboarding Holistic Doctrine · Operating Doctrine

> Canonique v2.80.3. Doctrine canon qui codifie la porte d'entrée opérateur PhantomOS. Patch v2.80.3 · `/tour` est l'explication conversationnelle de PhantomOS · accueil court qui dit ce qu'est le système, puis ARC SUBSTANCE guidé (pourquoi ça existe · comment ça raisonne · ce qui le distingue · le cycle · les 7 territoires) distillé un volet à la fois via `AskUserQuestion`, piloté par l'opérateur, expansions courtes. Double interdit canon · jamais un pavé (gap v2.80.2 *"là j'arrive sur un pavé"*) ET jamais une amorce amputée qui saute au choix de territoire sans présenter la vision/le fonctionnement/la doctrine (gap v2.80.3 recadrage Largo *"ça ne me va pas, tu ne présentes aucunement ce qu'est PhantomOS, vision, doctrine etc ?"*). `/about` reste le backup deep doc exhaustif, jamais un substitut de `/tour`. Pattern miroir AP-OHD-10. Onboarding agnostique (aucun typage métier à l'entrée) plus holistique (panorama 360° des territoires capability-mapped sur pied d'égalité visuelle) plus rendu EN PROSE CONVERSATIONNELLE NATIVE (pas d'interface ASCII boxes/tableaux/séparateurs structurés · réservée aux slash commands cockpit). Doctrine sœur de `scope-extension-doctrine.md` (canon élasticité scope opérateur-driven · racine philosophique), `output-clarity-doctrine.md` v2.79.2 (iconographie canon + headers FR sobres dans panorama), `engagement-disclosure-doctrine.md` v2.79.3 (disclosure gros skills · sister porte d'entrée), `pattern-detection-triggers.md` (smart suggest daemon apprentissage par usage), et `voice.md` (registre · ton accueil). Ferme le gap *"l'onboarding /tour survend creative/copywriting/brand-strategist alors que PhantomOS accueille n'importe quel métier DTC encodé · un opérateur tracking-GTM ne se reconnaît pas et ressent friction adoption"* flag systémique Sprint v2.79.3 post-audit Largo recadrage panorama 360° plus gap v2.80.1 *"/tour rendu en interface ASCII boxes/tableaux/séparateurs structurés · l'opérateur recadre · je ne veux pas d'interface, juste des messages natifs"* flag test live Largo Sprint v2.80.0.

---

## 1. Thèse fondatrice

> L'onboarding PhantomOS est agnostique (pas de typage opérateur à l'entrée) plus holistique (panorama 360° de toutes les capacités sur pied d'égalité) plus EN PROSE CONVERSATIONNELLE NATIVE (pas d'interface ASCII boxes/tableaux/séparateurs structurés · réservée aux slash commands cockpit). L'opérateur découvre l'étendue · se reconnaît dans le panorama · choisit où commencer · sans avoir à se déclarer profil métier · sans interface qui rompt le flow conversationnel.

**Définition canon onboarding holistique** · ensemble des pratiques opérationnelles qui forcent la porte d'entrée PhantomOS à accueillir tout opérateur DTC sans le filtrer ni le catégoriser à priori, en présentant l'étendue capability-mapped du système au scan rapide. Onboarding canon répond à 4 questions miroir ·

1. *"L'opérateur peut-il scanner l'étendue PhantomOS en 10-15 secondes ?"* (panorama 360° matriciel · 7 territoires capability-mapped)
2. *"Se reconnaît-il dans au moins un territoire sans devoir se déclarer ?"* (pied d'égalité visuelle · aucun territoire survendu)
3. *"Découvre-t-il des territoires adjacents qu'il opère sans encore le savoir ?"* (holistique cross-territoire · scope élastique)
4. *"Le système apprend-il son profil par observation plutôt que déclaration ?"* (apprentissage par usage · smart suggest existant)

**Différenciation canon vs onboarding typé classique** ·

| Layer | Onboarding typé classique (SaaS · agency-onboarding) | PhantomOS canon Onboarding Holistique |
|---|---|---|
| Entrée | question profil métier ("tu fais quoi · ton role") | aucune question profil · panorama direct |
| Surface adaptive | pré-configurée selon profil déclaré | identique cross-opérateur · pied d'égalité |
| Découverte territoires | filtrée selon profil ("tu es media-buyer · voici X") | exhaustive 7 territoires capability-mapped |
| Apprentissage profil | déclaration upfront stockée enum figé | observation usage progressive · jamais imposé |
| Re-entrée | figée post-setup initial | évolutive reflète état workspace actuel |
| Adoption opérateur hors-profil-survendu | friction (sentiment "pas pour moi") | reconnaissance directe (panorama égal) |

Onboarding typé signale au novice "le système attend de toi un profil canonique". Onboarding holistique PhantomOS signale "le système t'accueille tel quel et te révèle son étendue". C'est la différence entre un funnel filtre (passif) et un panorama découvrable (operable).

Cette doctrine canonise le pattern porte d'entrée opérateur. Toute surface onboarding user-facing respecte les 7 territoires capability-mapped panorama 360°.

---

## 2. Le problème résolu

Sans Onboarding Holistic Doctrine canon ·

1. **Survente territoires creative/copy/brand.** L'onboarding `/tour` historique présente proéminemment skills creative production · copywriting · brand strategy · audiences cartography. Opérateur tracking-GTM specialist (pixels Shopify · consent mode · server-side setup) ne se reconnaît pas · friction adoption · sentiment *"PhantomOS n'est pas pour moi"*. Adoption cassée hors-profil-survendu.

2. **Violation élasticité scope canon.** Memory canon Largo `phantomos_elastic_scope` codifie *"PhantomOS n'a pas de scope préalable · opérateur décide ce qui rentre · système accueille n'importe quel domaine"*. Détecter le profil métier en entrée et adapter pré-emptivement la surface = violation directe de cette élasticité. L'opérateur configure son workspace par USAGE PROGRESSIF, pas par déclaration upfront.

3. **Enum figé profile.json bloque scope extension.** Si `operator/profile.json#identity.profile` contient enum métier figé (`media_buyer | copywriter | brand_strategist`), tout opérateur hors-enum est en rupture canon. Tracking specialist · CRO consultant · lifecycle ops · business pilotage analyst · etc. = catégories absentes · l'opérateur n'a pas de slot pour exister. Pattern miroir anti-pattern AP-OHD-6.

4. **Découverte territoires latents impossible.** Sans panorama 360° exhaustif, l'opérateur ignore que PhantomOS accueille tracking-GTM, business pilotage, lifecycle, ops workflow. Skills shipped dorment · territoires latents pas annoncés · adoption fragmentée brand strategy-only.

5. **Adaptation surface pré-emptive = mauvais sample.** Si la surface s'adapte selon profil déclaré à T0, l'opérateur ne voit jamais l'étendue PhantomOS. Il opère sur slice partielle · ignore capacités cross-territoire · ne découvre pas de fenêtres d'extension scope opportunistes (cf SED-X v2.65).

6. **Re-entrée onboarding figée.** `/tour` post-setup initial figé sur déclaration T0 = perte d'opportunité découverte progressive. L'opérateur évolue · son workspace évolue · le panorama doit refléter l'état actuel pas l'état T0 figé.

7. **Onboarding rendu en interface ASCII boxes/tableaux/séparateurs structurés.** Cas test live Largo Sprint v2.80.0 · `/tour` rendu en panorama 360° formaté ASCII boxes (━━━ ─── tableaux structurés · légende iconographie ✓ ◐ ○ ✗ ⚠ au pied · grille visuelle) · pattern matriciel canon réservé aux slash commands cockpit (`/phantom` `/bird` `/breakdown` `/about` `/update` `/version`) appliqué par erreur à l'onboarding. Recadrage opérateur direct · *"je ne veux pas d'interface · uniquement pour les commandes slash Phantom · juste des messages natifs pendant tout l'onboarding"*. L'onboarding (`/tour` plus premiers messages opérateur) DOIT être prose conversationnelle native · pas d'interface · pas de structure ASCII · pas de tableau. Pattern miroir AP-OHD-9.

Onboarding Holistic Doctrine = doctrine canon qui ferme ces 7 gaps via panorama 360° de 7 territoires capability-mapped en PROSE CONVERSATIONNELLE NATIVE + zéro typage entrée + apprentissage par usage + re-entrée évolutive + 9 Hard Rules enforcement runtime.

---

## 3. Définition agnostique · zéro typage opérateur à l'entrée

Onboarding canon agnostique strict v2.79.3+ ·

**Aucune question profil métier au démarrage.** Pas de *"tu fais quoi"*, *"ton métier"*, *"ton role"*, *"ton profil"*, *"quel type d'opérateur tu es"*. L'opérateur n'est pas interrogé sur sa catégorie métier à T0.

**Aucune cartographie initiale typée.** Pas de questionnaire structuré qui aligne l'opérateur sur des archétypes (media-buyer · brand-strategist · copywriter · etc.). Pas de wizard "choisis ton template profil".

**Aucune adaptation pré-emptive de la surface.** Le panorama 360° est identique cross-opérateur à l'entrée. Skills shipped visibles tous · territoires capability-mapped tous · sur pied d'égalité visuelle.

**L'opérateur n'est pas filtré · catégorisé · scoré · enrichi.** Pas de métadonnées profil PhantomOS-attribuées au premier contact. Pas de tag *"profile_type: media_buyer"* en frontmatter operator/profile.json. Pas de score affinity territoire pré-calculé.

**Implication canon canon** · l'élasticité scope (memory canon `phantomos_elastic_scope`) est préservée dès le premier contact. Le système accueille avant de comprendre. La compréhension émerge par usage observation.

---

## 4. Définition holistique · panorama 360° sur pied d'égalité

Onboarding canon holistique strict v2.79.3+ ·

**Panorama 360° exhaustif.** TOUS les territoires métiers DTC capability-mapped sont représentés au lancement `/tour`. Pas de slice partielle · pas de top-N selectif · pas de "Featured territories". Exhaustivité canon obligatoire.

**Pied d'égalité visuelle.** Aucun territoire n'a de hiérarchie visuelle pré-emptive. Pas de creative > tracking · pas de media-buyer > copywriter · pas de brand-strategist > ops. Tous égaux dans l'angle de présentation graphique · ordre canon stable cross-opérateur.

**Capability-mapped pas profil-mapped.** Le panorama présente des capacités (CE QUE LE SYSTÈME FAIT) pas des profils opérateurs (QUI TU ES). L'opérateur scan les capacités et identifie où il opère.

**Reconnaissance opérateur autonome.** Le scan rapide (10-15 secondes) permet à l'opérateur de localiser son métier dans le panorama sans guidance. Il dit *"j'opère dans le territoire X"* OR *"je reconnais Y et Z dans mon flow quotidien"*. Auto-localisation canon.

**Découverte territoires adjacents.** Holistique implique aussi exposition aux territoires que l'opérateur N'opère PAS encore mais pourrait opérer. Tracking specialist découvre `Brand Strategy` adjacent · copywriter découvre `Business Pilotage` adjacent · etc. Fenêtre extension scope canon ouverte dès T0.

---

## 5. Territoires canon panorama 360° · 7 capability-mapped

Liste canon territoires v2.79.3+ stricte 7 capability-mapped sur pied d'égalité ·

```
┌─────────────────────────────────────────────────────────────────┐
│ PANORAMA 360° PHANTOMOS · 7 TERRITOIRES CAPABILITY-MAPPED      │
├─────────────────────────────────────────────────────────────────┤
│ 1. Creative & Copy Production                                   │
│    · angles paid · briefs copy · creatives composition          │
│    · sales letters · scripts VSL · email flows                  │
│ 2. Tracking & GTM                                               │
│    · pixels Meta/Google · server-side · consent mode            │
│    · audits coverage · attribution windows                      │
│ 3. Media Buy & Performance                                      │
│    · campagnes Meta · audits perf · score matrices              │
│    · brief-day · pacing budget · diagnostic CPA/ROAS            │
│ 4. Brand Strategy                                               │
│    · positioning canvas · voice 4D · archetypes                 │
│    · purpose · narrative · brand voice consistency              │
│ 5. Ops & Workflow                                               │
│    · todos · agendas · onboarding · setup                       │
│    · scripts opérations · scaffolding · validation              │
│ 6. Business Pilotage                                            │
│    · unit economics · WBR · cohort retention                    │
│    · roadmap · OKRs · projection                                │
│ 7. Lifecycle & CRO                                              │
│    · PDP optimization · landing pages · email flows             │
│    · upsell · LTV · checkout funnel                             │
└─────────────────────────────────────────────────────────────────┘
```

**Règles canon territoires** ·

- 7 territoires exacts · cap canon strict v2.79.3+ (issus audit Largo recadrage panorama)
- Capability-mapped (CE QUE LE SYSTÈME FAIT) pas profil-mapped (QUI TU ES)
- Ordre canon stable cross-opérateur · pas de reshuffling selon contexte session
- Chaque territoire annoncé avec · nom court (1-3 mots) plus 1 ligne descriptif plus 3-5 capacités citées plus statut canon (✓ shipped · ◐ partial · ○ ouvert)
- Pied d'égalité visuelle strict · même densité ligne · même grammaire annonce · aucun adjectif décoratif (PRIORITAIRES · CRITIQUES · ESSENTIELS) sur un territoire vs un autre

**Statut canon territoires v2.79.3+** ·

| # | Territoire | Statut canon | Skills shipped count |
|---|---|---|---|
| 1 | Creative & Copy Production | ✓ shipped | 12+ skills canon |
| 2 | Tracking & GTM | ○ ouvert | territoire annoncé · skills NEW backlog v2.80 |
| 3 | Media Buy & Performance | ✓ shipped | 8+ skills canon |
| 4 | Brand Strategy | ✓ shipped | 6+ skills canon |
| 5 | Ops & Workflow | ✓ shipped | 10+ skills canon |
| 6 | Business Pilotage | ◐ partial | skills partiel · territoire actif |
| 7 | Lifecycle & CRO | ◐ partial | skills partiel · territoire actif |

---

## 6. Pattern panorama canon · grammaire d'annonce stable

Pattern annonce canon v2.79.3+ panorama 360° cross-opérateur ·

**Grammaire annonce territoire** ·

```
N. {Nom court territoire} · {statut canon}
   {1 ligne descriptif court · 60 chars max}
   {3-5 capacités citées · séparateur middle dot ·}
```

**Exemple canon** ·

```
2. Tracking & GTM · ○ ouvert
   Setup pixels et attribution client-side et server-side
   pixels Meta/Google · server-side · consent mode · audits coverage
```

**Règles canon grammaire annonce** ·

- Grammaire identique cross-territoires · pied d'égalité visuelle strict
- Statut canon iconographie unique (✓ shipped · ◐ partial · ○ ouvert) miroir HR-OCD-1
- Descriptif 1 ligne · 60 chars cap · pas d'adjectif décoratif
- Capacités citées 3-5 max · séparateur middle dot `·` · langage opérateur-facing (cf operator-vocabulary-translation.md)
- Pas de skill names exposés (anti-pattern jargon leak) · capacités verbalisées en termes opérateur

**Canon v2.80.2 · panorama bref + entrée guidée tour à tour.** Sur `/tour` onboarding, le panorama est rendu **bref** · accueil court (2-3 phrases) + les 7 territoires en demi-lignes (une capacité-clé chacun · ≤6 lignes total · équité HR-OHD-1 préservée). Aucun paragraphe de pitch long, aucune section statut développée, aucun call-to-action en prose libre. Le panorama bref est immédiatement suivi d'une **question guidée** (`AskUserQuestion`, 4 options substantives composées · 2-3 territoires + 1 action setup, free-text natif pour le reste · jamais de menu figé, jamais d'option filler). Chaque tour suivant (drill territoire, choix capacité) enchaîne aussi sur une question guidée plutôt qu'une attente de texte libre nu. L'onboarding est conversationnel guidé tour à tour, pas un dump suivi d'une question ouverte. Le contenu exhaustif (architecture, philosophie, glossaire) vit dans `/about` opt-in, jamais déversé dans `/tour`. La grammaire d'annonce détaillée ci-dessus reste la référence pour les slash commands cockpit, pas pour l'entrée `/tour`.

**Header panorama canon** ·

```
PHANTOMOS · PANORAMA TERRITOIRES

7 territoires capability-mapped. Scan rapide pour localiser ton métier.
Reconnais où tu opères · drill par territoire ensuite.

[liste 7 territoires]

────────────────────────────────────────
Drill              /tour {territoire}
Démarrer           /tour start {territoire}
Aide               /tour ?

✓ shipped  ◐ partial  ○ ouvert
```

---

## 7. Apprentissage par usage · pas par déclaration

Apprentissage canon profil opérateur v2.79.3+ strict ·

**Le système apprend l'opérateur par ses ACTIONS, pas par sa DÉCLARATION.** Pattern canon · capture usage observation cross-session · smart suggest contextual existant (cf `pattern-detection-triggers.md` daemon + `learn-from-session` Trigger 8) capture pattern récurrent · propose progressivement extensions territoire-relevant.

**Mécanismes canon apprentissage usage** ·

| Mécanisme | Source | Latence |
|---|---|---|
| Pattern detection daemon | `pattern-detection-triggers.md` Trigger 8 | per-turn silent buffer |
| Learn-from-session capture | `learn-from-session` skill Trigger 8 | post-session batch |
| Skills invocation cross-session | `_field_types` audit trail per-skill | observation continue |
| Territoires touchés | brand state files mutations | snapshot par skill consume |

**Le profil métier émerge par observation · jamais imposé.** Si l'opérateur invoke 8 fois `mine-voc` plus 5 fois `produce-paid-angles` plus 2 fois `audit-meta-account` en 3 sessions, le système observe pattern *"creative + media buy"* sans avoir à demander. Smart suggest propose ensuite extensions territoire-relevant (e.g. *"tu opères beaucoup en creative paid · veux-tu setup tracking GTM pour boucler attribution ?"*).

**Anti-pattern strict** · questionnaire profil structuré T0 qui stocke enum métier figé dans frontmatter operator/profile.json. Apprentissage usage canon est progressive, observable, dérivable post-3+ sessions, jamais figé T0.

---

## 8. Skills latents annoncés transparent

Capacités canon en cours v2.79.3+ stricte transparence ·

**Skills NEW backlog annoncés explicit.** Capacités canon shipped count partiel ou nul (territoire ouvert · skills NEW backlog v2.80+) sont annoncées comme *"territoire ouvert · invocable freestyle prose ou backlog skill explicite"*. Pas de masquage · pas de présentation faux-shipped.

**Pattern annonce skill latent canon** ·

```
2. Tracking & GTM · ○ ouvert
   Setup pixels et attribution client-side et server-side
   Territoire ouvert · skills NEW backlog v2.80 · invocable freestyle
```

**Règles canon transparence** ·

- Si territoire ✓ shipped · annonce skills shipped count (e.g. *"12+ skills canon"*)
- Si territoire ◐ partial · annonce *"skills partiel · territoire actif"*
- Si territoire ○ ouvert · annonce *"territoire ouvert · skills NEW backlog v{version}"*
- JAMAIS présenter comme shipped un territoire avec 0 skills canon
- JAMAIS masquer un territoire ouvert pour faire bonne figure marketing

**Implication canon** · le panorama 360° ne ment pas. L'opérateur lit l'état réel du système · décide en connaissance · jamais leurré par faux-shipped.

---

## 9. Anti-typage opérateur · interdictions canon

Anti-typage canon strict v2.79.3+ ·

**JAMAIS de question profil métier** ·
- *"tu fais quoi"*
- *"ton métier"*
- *"ton role"*
- *"ton profil"*
- *"quel type d'opérateur tu es"*
- *"choisis ton archétype"*
- *"identifie ton profil dans cette liste"*

**JAMAIS d'enum métier figé** dans frontmatter operator/profile.json ·
- Pas de `identity.profile: media_buyer | copywriter | brand_strategist`
- Pas de `identity.archetype: creator | analyst | ops`
- Pas de `identity.specialty: tracking_gtm | lifecycle | etc.`

**JAMAIS d'adaptation surface pré-emptive** selon profil déclaré ·
- Pas de slice partielle skills selon profil
- Pas de masking territoires hors-profil
- Pas de "featured workflows" selon enum métier

**JAMAIS de filtre profil bloquant** accès skills hors-profil ·
- Tracking specialist peut invoke skills brand strategy
- Brand strategist peut invoke skills tracking GTM
- Aucune restriction enum-based · scope élastique strict

**Implication canon** · l'opérateur est libre cross-territoire dès T0. Pas de gating profil. Pas de pré-supposition. Pas de catégorisation imposée.

---

## 10. Rendu prose conversationnelle native · onboarding vs slash commands

Distinction canon v2.80.1+ rendu surface onboarding versus surface slash commands cockpit ·

**Distinction canon binaire** ·

| Surface | Format canon | Pattern |
|---|---|---|
| Slash commands cockpit (`/phantom` `/bird` `/breakdown` `/about` `/update` `/version`) | Format matriciel ASCII (boxes ━━━ ─── tableaux structurés · légende iconographie · panorama grille) | Canon UI cockpit · scan rapide structuré |
| Onboarding (`/tour` plus premiers messages opérateur) | Prose conversationnelle native (paragraphes naturels · retours ligne entre paragraphes) | Canon accueil flow conversationnel |

**Pattern prose conversationnelle native canon** ·

- Paragraphes naturels enchaînés · phrases complètes · pas de fragmentation bullet
- Retours ligne entre paragraphes pour respirer · pas de séparateurs visuels structurés
- ZÉRO box ASCII · ZÉRO tableau structuré · ZÉRO séparateur ═══ ━━━ ─── dans rendu opérateur
- Panorama 360° inclus dans prose narrative · pas tableau structuré · les 7 territoires verbalisés en flow conversationnel naturel
- Action close en phrase intégrée au flow conversationnel · pas bloc visuel structuré
- Statut canon territoires (shipped · partial · ouvert) verbalisé en prose · pas iconographie ✓ ◐ ○ avec légende au pied
- Aucune légende iconographique structurée en pied de message

**Exemple canon prose onboarding `/tour` v2.80.1+** ·

> Salut. Je suis l'agent PhantomOS · ton workspace pour opérer la croissance e-commerce. Je couvre 7 territoires métiers DTC à plat · creative et copywriting paid, tracking et GTM, media buy performance, brand strategy, ops et workflow, business pilotage, lifecycle et CRO. Tu peux scanner pour repérer où tu opères aujourd'hui.
>
> Côté shipped opérationnel, creative production a 12 skills canon, media buy 8 skills, brand strategy 6 skills, ops 10 skills. Business pilotage et lifecycle sont actifs partial. Tracking GTM ouvert · backlog skills NEW v2.80.
>
> Pour démarrer, dis-moi simplement sur quoi tu veux travailler. Brand à setup, audit perf à lancer, angle paid à creuser, peu importe le point d'entrée · le système accueille.

**Anti-pattern strict miroir AP-OHD-9** ·

Onboarding `/tour` rendu en interface ASCII boxes structurées (`┌─────┐ │     │ └─────┘` · tableaux Markdown · séparateurs ━━━ ─── ═══ · grille panorama avec colonnes alignées · légende iconographique ✓ ◐ ○ ✗ ⚠ structurée au pied). Pattern matriciel canon est ANTI-PATTERN sur onboarding · cassure flow conversationnel · violation recadrage opérateur direct *"je ne veux pas d'interface, juste des messages natifs"*.

**Implication canon** · l'onboarding accueille en conversation native · le cockpit slash commands structure en UI matricielle ASCII. Confondre les deux casse le flow porte d'entrée · provoque friction adoption · viole le recadrage opérateur Sprint v2.80.0.

---

## 11. Re-entrée onboarding · découverte continue

Re-entrée canon `/tour` v2.79.3+ évolutive ·

**Quand opérateur revient sur `/tour` post-setup initial**, le panorama 360° est mis à jour pour refléter l'état workspace actuel · pas figé T0.

**Mécanismes canon re-entrée évolutive** ·

| État workspace | Surface panorama re-entrée |
|---|---|
| Territoires actifs (skills invoked 3+ fois) | annoncés en premier · stat usage cited |
| Territoires latents (skills invoked 0 fois) | annoncés en deuxième · invitation drill |
| Brands encodées count | header panorama updated · stat actuelle |
| Skills usagés vs non touchés | territoire-level breakdown ◐ partial logique |
| NEW skills shipped post-T0 | flag *"NEW skill v{version}"* dans territoire |

**Découverte continue canon** · l'opérateur revient sur `/tour` après 5 sessions et voit (1) ses territoires actifs reconnus (2) territoires latents qu'il pourrait explorer (3) NEW skills shipped depuis sa dernière re-entrée. Pattern miroir releases notes adapté contexte opérateur personnel.

**Anti-pattern strict** · `/tour` re-entrée identique scope T0 · ignore état workspace actuel · perte d'opportunité découverte progressive. Pattern miroir AP-OHD-7.

---

## 12. Hard Rules canon (HR-OHD-1 à HR-OHD-10)

### HR-OHD-1 · Panorama 360° canon · 7 territoires capability-mapped pied d'égalité

`/tour` onboarding affiche canon strict 7 territoires capability-mapped sur pied d'égalité visuelle. Grammaire annonce identique cross-territoires (nom court · descriptif 1 ligne · capacités 3-5 · statut canon). Ordre canon stable. Pas de hiérarchie pré-emptive. Violation = bug invalid output onboarding canon.

### HR-OHD-2 · Zéro question profil métier au démarrage opérateur

`/tour` onboarding T0 strict ZÉRO question profil métier · *"tu fais quoi"* · *"ton role"* · *"ton profil"* · *"choisis archétype"* · etc. Aucune interrogation upfront sur catégorie métier opérateur. Violation = bug invalid output onboarding canon (force typage upfront violation phantomos_elastic_scope).

### HR-OHD-3 · Zéro adaptation surface pré-emptive selon profil déclaré

Surface panorama 360° identique cross-opérateur à T0. Aucune slice partielle · aucun masking territoires · aucun "featured workflows" selon enum métier. Pied d'égalité visuelle strict. Adaptation surface autorisée UNIQUEMENT post-observation usage (cf HR-OHD-6 apprentissage par usage). Violation = bug invalid output onboarding canon.

### HR-OHD-4 · Skills latents annoncés transparent

Territoires ◐ partial ou ○ ouvert annoncés explicit avec statut canon. JAMAIS présenter comme shipped un territoire 0 skills canon. JAMAIS masquer territoire ouvert pour faire bonne figure marketing. Transparence cap canon strict. Violation = bug invalid output onboarding canon (faux panorama leak).

### HR-OHD-5 · Iconographie canon v2.79.2 unique dans panorama state

Statut canon territoires utilise iconographie canon v2.79.2 strict (✓ shipped · ◐ partial · ○ ouvert · ✗ absent · ⚠ critique). Légende au pied du panorama miroir HR-OCD-8. Pas d'emoji couleur · pas d'émoticône décoratif. Violation = bug invalid output onboarding canon (rompt cohérence visuelle shipped product).

### HR-OHD-6 · Apprentissage opérateur par usage seulement

Profil opérateur émerge par observation usage cross-session (pattern-detection-triggers daemon + learn-from-session Trigger 8) jamais par déclaration upfront. Aucun enum métier figé en frontmatter operator/profile.json. Smart suggest contextual propose extensions territoire-relevant post-observation pattern récurrent (3+ sessions). Violation = bug invalid output onboarding canon.

### HR-OHD-7 · Re-entrée /tour reflète état workspace actuel · découverte continue

`/tour` re-entrée post-setup initial DOIT refléter état workspace actuel · territoires actifs (skills invoked 3+ fois) annoncés en premier · territoires latents annoncés en deuxième · NEW skills shipped flag *"NEW v{version}"*. Pas de panorama figé T0. Découverte continue canon. Violation = bug invalid output onboarding canon.

### HR-OHD-8 · Aucun enum métier figé en frontmatter operator/profile.json

Frontmatter `operator/profile.json#identity` DOIT NOT contenir enum métier figé (`profile` · `archetype` · `specialty` · `role` · etc.). Profil opérateur reste observable par usage cross-session, dérivable post-3+ sessions, jamais figé T0. Cross-ref `phantomos_elastic_scope` memory canon. Violation = bug invalid output onboarding canon (force typage upfront).

### HR-OHD-9 · Onboarding rendu prose conversationnelle native obligatoire

Onboarding (`/tour` plus premiers messages opérateur) DOIT être prose conversationnelle native. ZÉRO interface ASCII (boxes `┌─────┐ │     │ └─────┘` · séparateurs ━━━ ─── ═══ · tableaux structurés Markdown · légende iconographique structurée au pied · panorama 360° en grille avec colonnes alignées). Pattern matriciel ASCII réservé STRICT aux slash commands cockpit (`/phantom` `/bird` `/breakdown` `/about` `/update` `/version`). Onboarding rendu en flow conversationnel · paragraphes naturels · retours ligne entre paragraphes · statut canon territoires verbalisé en prose. Violation = bug invalid output onboarding canon (interface ASCII casse flow conversationnel · pattern miroir AP-OHD-9 · viole recadrage opérateur Sprint v2.80.0).

### HR-OHD-10 · Arc substance guidé tour à tour · ni pavé ni amorce amputée

`/tour` est l'explication conversationnelle de PhantomOS, pas un sélecteur de territoire. Milestone 1 DOIT ouvrir par un accueil court qui DIT ce qu'est PhantomOS (3-5 lignes · workspace stateful, encode une fois, raisonne/opère/apprend, différence avec un chat qui oublie), jamais réduit à une simple liste de territoires. Milestone 2 DOIT dérouler un ARC SUBSTANCE guidé · volets canon (pourquoi ça existe · comment ça raisonne · ce qui le distingue · le cycle · les 7 territoires) distillés UN À LA FOIS via `AskUserQuestion` (4 options substantives · volets non vus + toujours une option qui avance vers setup · free-text natif · jamais menu figé · jamais filler), expansions COURTES calibrées au registre, jamais d'attente texte-libre nu. Double interdit · (a) ZÉRO pavé, zéro déversement de toute la substance d'un bloc · (b) ZÉRO amorce amputée qui saute au choix de territoire sans avoir présenté vision/fonctionnement/différenciation. `/about` est le backup deep doc exhaustif, mentionné en une ligne, jamais substitut de `/tour`. **Exits toujours présentes (canon Vincent)** · chaque tour de l'arc porte (a) une porte de sortie rapide vers la configuration d'une marque (sortir du tunnel sans friction, single action option) ET (b) dès que les sujets s'imbriquent, un pivot cross-subject pour bifurquer latéralement et revenir. **Ton premium (canon Largo)** · on affirme ce que fait PhantomOS avec conviction, JAMAIS un comparatif agressif ni un concurrent nommé/dénigré (registre GitHub/Vercel, pas de tableau de scores contre des produits nommés · s'applique à `/tour` ET `/about`). Violation = bug invalid output onboarding canon (pattern miroir AP-OHD-10 · viole recadrages opérateur Sprint v2.80.2 *"un pavé"*, v2.80.3 *"tu ne présentes aucunement ce qu'est PhantomOS"* et *"le ton où on démontre Notion, Airtable, ce n'est pas premium"*).

---

## 13. Anti-patterns canon (AP-OHD-1 à AP-OHD-10)

### AP-OHD-1 · /tour demande "tu fais quoi" en porte d'entrée

`/tour` T0 ship question profil *"tu fais quoi · ton métier · ton role"* upfront avant panorama. Force typage opérateur · violation `phantomos_elastic_scope` memory canon · friction adoption hors-profil-survendu. Pattern canon · zéro question profil T0 · panorama direct. Pattern correctif · HR-OHD-2 enforcement runtime.

### AP-OHD-2 · Onboarding survend un territoire au détriment des autres

`/tour` ship panorama biaisé · creative/copy/brand-strategy proéminent · tracking GTM masqué ou last position · business pilotage absent. Pied d'égalité cassé · opérateur tracking specialist ne se reconnaît pas · friction adoption. Pattern canon · 7 territoires capability-mapped pied d'égalité visuelle strict. Pattern correctif · HR-OHD-1 enforcement runtime.

### AP-OHD-3 · Adaptation surface pré-emptive selon profil déclaré

`/tour` ship surface adaptive selon question profil T0 · slice partielle skills · masking territoires hors-profil · "featured workflows" enum-based. Surface différente cross-opérateur à T0 · découverte territoires adjacents bloquée · scope élastique violé. Pattern canon · surface identique T0 · adaptation post-usage seulement. Pattern correctif · HR-OHD-3 enforcement runtime.

### AP-OHD-4 · Skills latents présentés comme shipped

Panorama ship territoire 0 skills canon présenté ✓ shipped · faux marketing · l'opérateur invoke et bloque sur "skill not found". Trust cassé. Pattern canon · transparence statut canon strict (✓ shipped · ◐ partial · ○ ouvert). Pattern correctif · HR-OHD-4 enforcement runtime.

### AP-OHD-5 · Panorama hiérarchisé visuellement

Panorama ship territoires avec densité variable · creative section 8 lignes vs tracking section 1 ligne · adjectifs décoratifs *"creative PRIORITAIRE · tracking optionnel"*. Pied d'égalité visuelle cassé · signal hiérarchie implicite · biais adoption. Pattern canon · grammaire annonce identique cross-territoires. Pattern correctif · HR-OHD-1 enforcement runtime.

### AP-OHD-6 · Enum métier figé profile.json imposé

Frontmatter operator/profile.json ship enum métier figé · `identity.profile: media_buyer` · `identity.archetype: creator`. L'opérateur tracking specialist · CRO consultant · business pilotage analyst sans slot canonique · catégorisation imposée · scope rigide. Pattern canon · zéro enum métier figé · profil dérivable par usage. Pattern correctif · HR-OHD-8 enforcement runtime.

### AP-OHD-7 · Onboarding figé · pas de re-entrée /tour évolutive

`/tour` re-entrée post-setup initial identique scope T0 · ignore état workspace actuel · territoires actifs non reconnus · NEW skills shipped non flagués · découverte continue bloquée. Pattern canon · re-entrée évolutive reflète état workspace actuel. Pattern correctif · HR-OHD-7 enforcement runtime.

### AP-OHD-8 · Filtre profil bloquant accès skills hors profil déclaré

Surface ship restriction enum-based · brand strategist bloqué d'invoke skills tracking GTM · tracking specialist bloqué d'invoke skills brand strategy. Gating profil contraint · scope élastique violé · opérateur cross-territoire impossible. Pattern canon · zéro filtre profil bloquant · liberté cross-territoire stricte. Pattern correctif · HR-OHD-2 plus HR-OHD-8 enforcement runtime.

### AP-OHD-9 · Onboarding rendu avec interface ASCII boxes/tableaux/séparateurs structurés

`/tour` plus premiers messages onboarding rendus avec interface ASCII boxes (`┌─────┐ │     │ └─────┘` · panorama 360° en grille structurée avec colonnes alignées · tableaux Markdown structurés · séparateurs visuels ━━━ ─── ═══ · légende iconographie ✓ ◐ ○ ✗ ⚠ au pied du message · même pattern matriciel que slash commands cockpit `/phantom` `/bird` `/breakdown` `/about`). Confusion onboarding avec slash command UI · flow conversationnel cassé · friction adoption · violation recadrage opérateur direct *"je ne veux pas d'interface · uniquement pour les commandes slash · juste des messages natifs"* (cas test live Largo Sprint v2.80.0). Pattern canon · onboarding prose conversationnelle native strict · panorama 360° verbalisé en flow naturel · statut territoires en prose · zéro structure ASCII. Pattern correctif · HR-OHD-9 enforcement runtime.

### AP-OHD-10 · Pavé en entrée OU amorce amputée sans substance

Deux faces du même anti-pattern. **Face A · pavé** · `/tour` déverse toute la substance d'un bloc (pitch multi-paragraphes, vision + fonctionnement + différenciation + territoires développés) puis attend du texte libre ouvert. L'opérateur tombe sur un mur (recadrage Sprint v2.80.2 *"là j'arrive sur un pavé"*). **Face B · amorce amputée** · à l'inverse, `/tour` réduit l'entrée à 2 lignes + liste de territoires et saute direct à *"choisis ton territoire"* sans jamais dire ce qu'est PhantomOS, sa vision, comment il raisonne (recadrage Sprint v2.80.3 *"tu ne présentes aucunement ce qu'est PhantomOS, vision, doctrine etc ?"*). Les deux cassent l'onboarding · l'un noie, l'autre vide. Pattern canon · accueil court qui dit ce qu'est le système + arc substance distillé un volet à la fois via question guidée, expansions courtes, piloté par l'opérateur, `/about` en backup exhaustif. Pattern correctif · HR-OHD-10 enforcement runtime.

---

## 14. Cross-refs

- `output-clarity-doctrine.md` v2.79.2 · iconographie canon v2.79.2 unique (HR-OHD-5 dans panorama state ASCII slash commands · pas onboarding prose) plus headers FR sobres dans panorama · OHD applique OCD à la surface onboarding (prose native) et slash commands (ASCII canon)
- `tour.md` command · refondu v2.80.1 prose conversationnelle native canon · OHD est doctrine canon que `/tour` consomme
- `engagement-disclosure-doctrine.md` v2.79.3 · sister doctrine · disclosure gros skills · OHD plus EDD = paire porte d'entrée canon (entrée + invocation skills)
- `pattern-detection-triggers.md` · smart suggest daemon apprentissage par usage · HR-OHD-6 mécanisme
- `learn-from-session.md` Trigger 8 · capture usage opérateur post-session · HR-OHD-6 mécanisme
- `voice.md` · registre · ton accueil · OHD complète voice canon avec layer onboarding prose native
- `contextual-intelligence.md` · master doctrine · OHD est sub-doctrine opérationnelle scope onboarding
- `scope-extension-doctrine.md` v2.65 · canon élasticité scope opérateur-driven · racine philosophique · OHD opérationnalise SED-X pour cas concret onboarding porte d'entrée

---

## 15. Position dans le système opérationnel 5 couches

Onboarding Holistic Doctrine opère sur 3 couches simultanément du multiplicatif système opérationnel (`operational-system-doctrine.md`) · OHD est la PORTE D'ENTRÉE canon · couche racine accueil opérateur sans typage.

**Couche 2 · Règles (heuristiques décision).** 9 Hard Rules canon strict (HR-OHD-1 à HR-OHD-9) sont heuristiques décision canon · *"si onboarding /tour opérateur-facing alors panorama 360° agnostique 7 territoires obligatoires EN PROSE CONVERSATIONNELLE NATIVE"* enforcement runtime cross-surface onboarding. Distinction canon binaire onboarding (prose native) versus slash commands cockpit `/phantom` `/bird` `/breakdown` `/about` `/update` `/version` (format matriciel ASCII canon). Confondre les deux casse flow conversationnel porte d'entrée. Pattern miroir `output-clarity-doctrine.md` 8 Hard Rules · `decomposition-visibility-doctrine.md` 9 Hard Rules.

**Couche 3 · Templates (raccourcis combinaisons gagnantes).** Panorama 360° canon 7 territoires capability-mapped plus grammaire annonce stable (nom court · descriptif 1 ligne · capacités 3-5 · statut canon) sont templates canon réutilisables cross-`/tour` invocations · verbalisés en prose narrative pour onboarding et structurés ASCII pour slash commands cockpit. Pattern miroir `resources/templates/*` canon.

**Couche 5 · Rituels (cadence opérationnelle).** Trigger systémique porte d'entrée onboarding T0 plus re-entrée évolutive `/tour` post-setup initial enforcement runtime canon. Rituel canon agent par session opérateur first contact (prose native flow conversationnel) plus rituel canon agent par re-entrée découverte continue. Pattern miroir `brief-day` daily plus `routine-perf` weekly.

**Couche 4 · Métriques additionnelle.** % opérateurs reconnaissant leur territoire au scan rapide 10-15 secondes trackable via `learnings.json` append-only · adoption rate cross-territoire vs concentrated creative-only · plus zéro leak interface ASCII dans onboarding cross-sessions consécutives. Métrique convergente · OHD adoption rate cross-opérateur baseline v2.80.1 enforcement runtime.

**Position canon racine onboarding.** OHD est la couche racine accueil opérateur · prédicate à toute interaction post-T0. Sans OHD canon, adoption fragmentée brand-strategy-only · opérateurs hors-profil-survendu friction · scope élastique violé · interface ASCII casse flow conversationnel. Avec OHD canon, adoption distribuée cross-territoire · opérateurs reconnaissent leur métier dès T0 en prose native · scope élastique préservé.

---

## Status

- **Canonique v2.91.** Bump v2.80.1 → v2.91 · voir § 0 Évolution canon (agnostic-macro + kit DTC nommé · fan 4 verbes modèle mental d'entrée + 7 territoires granularité drill · HR-OHD-1 amendée · créa une lane · entrée tool-first operator-scope premier rang via `entry-arc-doctrine.md` v2.91). Additif · toutes les autres HR inchangées. Consumer · `/tour` v2.91.1.
- **Canonique v2.80.1.** Codifie pattern porte d'entrée opérateur PhantomOS agnostique plus holistique plus rendu PROSE CONVERSATIONNELLE NATIVE canon. Bump v2.79.3 → v2.80.1 post-cas test live Largo Sprint v2.80.0 (`/tour` rendu en interface ASCII boxes/tableaux/séparateurs structurés · recadrage opérateur direct *"je ne veux pas d'interface · uniquement pour les commandes slash Phantom · juste des messages natifs"*). Ferme gap structurel *"l'onboarding /tour survend creative/copywriting/brand-strategist · opérateurs hors-profil ne se reconnaissent pas · friction adoption"* (v2.79.3) plus gap *"/tour rendu en interface ASCII confondu avec slash command UI · viole flow conversationnel porte d'entrée"* (v2.80.1) via 7 territoires capability-mapped pied d'égalité en prose native plus 9 Hard Rules canon strict (HR-OHD-1 à HR-OHD-9) plus 9 anti-patterns (AP-OHD-1 à AP-OHD-9) enforcement runtime.
- **Doctrine sœur** · scope-extension-doctrine.md v2.65 (canon élasticité scope opérateur-driven · racine philosophique) · output-clarity-doctrine.md v2.79.2 (iconographie canon plus headers FR sobres dans slash commands ASCII · pas onboarding prose) · engagement-disclosure-doctrine.md v2.79.3 (disclosure gros skills · paire porte d'entrée) · pattern-detection-triggers.md (smart suggest daemon HR-OHD-6) · voice.md (registre · ton accueil prose native).
- **Backward compat** · strict additif · v2.80.1 n'override aucune règle existing. HR-OHD-9 plus AP-OHD-9 NEW enrichissent canon sans rétro-casser. `/tour` legacy pre-v2.80.1 conserve rendu ASCII jusqu'à patch · v2.80.1+ refonte prose conversationnelle native canon obligatoire.
- **First applications** · Sprint v2.80.1 patches `/tour` command refonte prose conversationnelle native (cas test live Largo Sprint v2.80.0 recadrage) plus distinction canon binaire onboarding prose native versus slash commands cockpit `/phantom` `/bird` `/breakdown` `/about` `/update` `/version` ASCII matriciel. Skills onboarding-adjacents v2.80.1+ migration progressive enforce prose native.
- **Promotion criterion** · à reviewer après 5+ opérateurs hors-profil-survendu reconnaissent leur territoire au scan 10-15 secondes en prose native plus 1 audit cross-opérateur adoption rate cross-territoire convergence plus learnings.json append patterns OHD adoption rate stable 80%+ plus zero typage upfront leak `/tour` consécutifs 3+ sessions plus zéro leak interface ASCII dans onboarding consécutif 5+ sessions.

---

*Doctrine canonique skill-author-facing plus agent-facing. Canonise porte d'entrée opérateur PhantomOS agnostique (zéro typage T0) plus holistique (panorama 360° 7 territoires capability-mapped pied d'égalité) plus rendu prose conversationnelle native (canon v2.80.1 post-recadrage Largo Sprint v2.80.0) plus 9 Hard Rules canon strict (HR-OHD-1 à HR-OHD-9) plus 9 anti-patterns canonisés (AP-OHD-1 à AP-OHD-9). Ferme gap structurel *"l'onboarding /tour survend creative/copywriting/brand-strategist · opérateurs hors-profil ne se reconnaissent pas"* (v2.79.3) plus gap *"/tour rendu en interface ASCII boxes/tableaux structurés · viole flow conversationnel"* (v2.80.1) via HR-OHD-1 à HR-OHD-9 enforcement runtime. Pattern miroir scope-extension-doctrine.md v2.65 (canon élasticité scope opérateur-driven · racine philosophique) plus output-clarity-doctrine.md v2.79.2 (iconographie canon plus headers FR sobres) plus engagement-disclosure-doctrine.md v2.79.3 (disclosure gros skills · paire porte d'entrée). OHD est la couche racine accueil opérateur · prédicate à toute interaction post-T0 · scope élastique préservé dès T0 · prose native canon strict.*
