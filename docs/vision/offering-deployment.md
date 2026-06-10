# Offering & Deployment

> Méthodologie commerciale et roadmap de packaging pour PhantomOS. Audience interne (maintainer, futurs collaborateurs) + partenaires commerciaux qui veulent comprendre comment le produit se vend et se déploie. Ce document n'est pas une offre commerciale finalisée : il documente le cadre dans lequel les offres se structurent et la manière dont chaque déploiement client est mené. Il s'enrichit au fur et à mesure que les premiers clients commerciaux signent et que les vertical packs matures.

---

## 1. Objet

Ce document existe pour deux raisons.

D'abord, séparer ce qui relève du **produit** (l'environnement, ses mécaniques, son extensibilité) de ce qui relève de **l'offre commerciale** (comment on package, on tarife, on déploie chez un opérateur). Le produit est documenté ailleurs : `vision.md`, `manifesto.md`, `prisms.md`, `fit.md`, `capabilities.md`. Cette doc traite l'autre versant : la mise en marché.

Ensuite, fournir un référentiel partagé pour quiconque vendrait, déploierait, ou évangéliserait PhantomOS sans avoir vécu chaque arbitrage de design. Un partenaire commercial ou un futur Forward Deployed Operator doit pouvoir lire ce document et comprendre : ce qui est inclus, ce qui ne l'est pas, ce qui se vend séparément, ce qui n'est pas encore packageable, et pourquoi.

Le scope est volontairement étroit : méthodologie commerciale + roadmap packaging. Pas de pricing arrêté avant le premier client signé. Pas de doctrine légale (transmissibility framework dépend du framework de provenance, déclenché plus tard). Pas de marketing de surface : c'est l'os de l'offre, pas la couche de communication.

---

## 2. Principe de l'offre

Quatre principes structurent toute offre PhantomOS, présents et futurs.

**Le produit est l'environnement.** Le workspace local, ses quatre couches (réceptacle, encodage métier, ressources partagées, capacités opérationnelles), ses mécaniques d'invariant (mutation gate, append-only, _field_types, mémoire de session, discipline de raisonnement interne). C'est ce qui se déploie chez tout opérateur, quel que soit son domaine.

**Le kit DTC est inclus par défaut.** Une trentaine de skills, le canon copywriting structuré, les registres et matrices transverses. Il sert deux fonctions simultanées : permettre à un opérateur DTC d'être productif dès J+1, et démontrer ce que devient l'environnement une fois rempli pour un domaine donné. Le kit n'est pas le produit : c'est la démonstration du produit. Cette distinction est critique commercialement : on ne vend pas une bibliothèque de skills DTC ; on vend l'environnement qui peut accueillir n'importe quelle bibliothèque de skills.

**Les vertical packs additionnels seront proposés à mesure qu'ils matures.** Consulting, media buying, coaching, créateurs codifiables, recherche appliquée. Chacun nécessite un canon métier encodé + un set de skills production scaffolded + au moins un pilote client validé. Pas de vertical pack speculatif : chaque pack se justifie par une demande mesurée et une instance de référence en production.

**Le consulting d'encodage est une offre humaine adjacente.** Quand un opérateur n'a pas le temps ou les compétences de poser son propre encodage, un déploiement assisté (maintainer ou un Forward Deployed Operator formé) accélère l'onboarding. C'est un service, pas un produit : facturé séparément, optionnel, avec un livrable défini (workspace opérationnel + méthode encodée + autonomie client à la sortie). Cette offre matérialise ce que Palantir formalise sous le terme *Forward Deployed Engineer*, transposé au scale SMB.

**Le licensing client-side reste en attente du framework de provenance.** Tant que la doctrine *Provenance & Trust* n'est pas écrite (déclenchée par 2e opérateur connecté, 1er knowledge pack vendu, ou 1er skill tiers), aucune offre formelle de licensing ne sort. Les patterns intermédiaires sont opérés par discipline contractuelle, pas par mécanique produit. Voir section 6.

---

## 3. Structure d'offre actuelle ()

L'offre commerciale en cours de construction au moment où ce document est écrit (S46, 2026-04) tient en une ligne :

**Workspace clean + kit DTC inclus, déployable chez un opérateur DTC mature, agency DTC, ou consultant growth.**

### Public cible actuel

- Solo opérateurs DTC à partir du mois 6 d'opération (assez d'historique pour que les décisions répètent).
- Agency owners DTC gérant 3 à 8 comptes clients (cognitive load + cross-brand pattern capture).
- Consultants growth senior dont la valeur dépend d'une méthodologie répétable (craft articulation + outcome-based pricing).
- Coaches et experts qui productisent une méthode codifiable (pas des créateurs volume).

Ces profils correspondent au best fit documenté dans `fit.md`. Out of scope : agencies enterprise 5-10 personnes (multi-tenant non couvert), founders pré-traction (encoder une thèse non validée densifie sur du faux signal), performance creators distribution-volume (PhantomOS ne couvre pas leur chaîne).

### Tarification actuelle

**À finaliser quand le premier client commercial signe.** Posture : pas de pricing arrêté ex ante. Trois principes guident la décision finale :

1. Pricing ancré sur la valeur opérée (output de l'environnement, pas heures du maintainer). Cohérent avec la posture *sell work, not software* (Tavel) et la nature compounding du workspace.
2. Distinguer **le produit** (l'environnement, abonnement ou licence) de **le service** (consulting d'encodage, ponctuel ou retainer). Mélanger les deux dans une seule facture brouille l'unit economics et empêche la scalabilité hors maintainer.
3. Tester deux ou trois modèles sur les premiers clients (one-time setup + abonnement vs retainer mensuel tout-inclus vs outcome-based) avant de figer une grille publique. Le premier modèle est un instrument d'apprentissage, pas une décision irréversible.

Le pricing initial indicatif (ordre de grandeur uniquement, à valider) : déploiement initial encadré + abonnement workspace + consulting d'enrichissement optionnel. Ne pas publier de grille sur le site avant le 3e client signé sur le même modèle.

---

## 4. Structure d'offre cible (future)

L'offre cible, à 12-18 mois, segmentée par vertical pack et par mode de consommation.

### Composition d'offre cible

**Workspace clean** (l'environnement, agnostique du domaine) + **choix d'un ou plusieurs vertical packs** :

- **DTC pack** (livré par défaut, devient un pack parmi d'autres ensuite).
- **Consulting-core pack** (engagement, stakeholder, SOW, milestone, deliverable + skills `generate-client-deliverable`, `pipeline-review`, `productize-method`).
- **Media-buyer-freelance pack** (retainer reporting, client dashboard, cross-account benchmark).
- **Coach-expert pack** (`methodology-map`, `cohort-curriculum`, `productize-framework`).
- **Compliance / vertical secondaire packs** (FR-compliance gambling, supplements EU, clinical claims, etc.) : composables en surcouche d'un pack primaire.

### Tarification cible

Probable segmentation :

- **Par vertical pack** (le pack DTC ne se tarife pas comme le pack consulting : densité de canon différente, valeur générée par session différente).
- **Par seat ou par session** (un solo opérateur ne paie pas comme une agency 5 personnes ; un consultant intermittent ne paie pas comme un opérateur quotidien).
- **Composition de packs envisageable** (DTC + FR-compliance ; consulting-core + media-buyer ; coach + content-SEO).

Prérequis avant publication grille future : 3+ clients signés par pack, données de consommation token + d'engagement réelles, pricing testé sur deux ou trois cohortes.

### Knowledge packs comme produit séparé (post-le framework de provenance)

Quand le framework *Provenance & Trust* est écrit (trigger : 2e opérateur connecté ou 1er knowledge pack vendu), les canons encodés deviennent des assets standalone vendables : pack copywriting DTC clean, pack media buying gambling FR, pack consulting discovery B2B. Voir section 8.

---

## 5. Méthodologie de déploiement client

Indépendamment du vertical pack, tout déploiement suit le même flow.

### Phase 1 · Onboarding (J0)

Tour guidé par l'agent (`tour.md`). Détection langue, niveau opérateur, profil métier. Présentation des concepts en termes opérateur, jamais en jargon doctrinal. Sortie : workspace initialisé, première brand prête à encoder, opérateur calibré sur les attentes.

Durée : 15-30 min.

### Phase 2 · Encodage initial guidé (J0-J1)

Skill `setup-brand` puis `snapshot-brand` (URL Shopify ou source équivalente) : pull la fondation produit + audience hypothèse + offers en 30-60 min via scrape + WebFetch + 4 questions clés à l'opérateur. Quand le domaine n'est pas DTC (consulting, coaching, etc.), `scaffold-extension` propose un canon de référence avec primitive `suggest-domain-canon` (auteur + framework reconnus, fetch automatique, validation opérateur sur synthèse jamais sources).

Sortie : Context DB opérationnelle, statut `wedge_complete`, productivité immédiate sur les premiers livrables.

Durée : 30-60 min selon densité de la fondation.

### Phase 3 · Productivité opérationnelle (J+1 à J+30)

L'opérateur produit du copy, des briefs, des landing pages, des analyses, des audits, selon son métier. À chaque correction qu'il apporte à un output de l'agent, `learn-from-session` capture la décision sous-jacente. Le workspace densifie. Les Decision Traces s'accumulent.

Sortie attendue : volume de livrables comparable à une production manuelle, qualité progressivement supérieure à mesure que les apprentissages se persistent.

### Phase 4 · Raffinement par l'opérateur (M+1 à M+6)

L'opérateur étend son workspace : nouvelles entités via `scaffold-extension`, nouveaux skills via `build-agent`, ressources métier ajoutées dans `resources/`, learnings promus en patterns. Le workspace devient *son* outil, pas un template générique.

Sortie attendue : qualité agency-grade sur les tâches encadrées par les capacités encodées, autonomie complète vis-à-vis du déployeur initial.

### Cycle de vie typique

| Étape | Durée | Effort opérateur | Output |
|-------|-------|------------------|--------|
| Onboarding | 15-30 min | Conversationnel | Workspace + tour |
| Encodage initial | 30-60 min | 4-6 questions | Context DB live |
| Productivité opérationnelle | J+1 à J+30 | Usage quotidien | Livrables + apprentissages cumulés |
| Raffinement | M+1 à M+6 | Discipline de capture | Workspace agency-grade |
| Régime stable | M+6+ | Maintenance + extension | Compounding asset |

---

## 6. Transmissibilité et continuité

Le workspace est transmissible par design. Cette propriété est à double tranchant : elle résout des problèmes business critiques et crée des tensions commerciales nouvelles. Trois patterns opérationnels existent pour la gérer (référence : `fit.md § Consultant tension upgraded S46`).

**Pattern 1 · Contractual licensing.** Le workspace reste propriété du consultant ; le client reçoit une licence d'usage bornée par la mission. Fin du retainer = fin de licence. Ne porte pas de couche de licensing applicative : c'est une discipline contractuelle, à inscrire dans le SOW.

**Pattern 2 · Workspace separation.** Un workspace encode la méthode propriétaire du consultant (le moat, qui reste avec lui). Un second workspace par client dérive du premier mais ne fusionne pas en arrière. Pas de skill qui automatise cette séparation : discipline opérateur jusqu'au prochain ship.

**Pattern 3 · Outcome-based pricing.** Quand le consultant facture le résultat plutôt que les heures, l'auto-replacement devient une feature plutôt qu'un bug. Le client garde le workspace, le consultant garde la mission d'évolution. Le plus solide des trois patterns tant que le framework de provenance n'est pas écrit.

**Continuité business.** La même propriété qui crée la tension consulting résout le problème miroir : que se passe-t-il quand le senior qui détient la méthode part, prend sa retraite, ou vend l'entreprise ? Réponse : le successeur ouvre le workspace et hérite de la méthode encodée sans semaines d'onboarding. Cette continuité est un argument commercial **vers les fondateurs d'entreprise** qui veulent dérisquer leur dépendance au capital humain individuel.

**Doc dédiée à drafter quand multi-tenant trigger.** `transmissibility-framework.md` : templates de clauses contractuelles, primitives techniques (workspace forking automatisé, license tracking), playbook commercial outcome-based. Pas écrit avant le 1er litige client ou le 2e consultant déployant chez un client tiers.

---

## 7. Roadmap des verticaux

Statut au S46 (2026-04) :

| Vertical | Statut | Prérequis manquants | ETA indicatif |
|----------|--------|---------------------|---------------|
| **DTC e-commerce** | Mature, livré | aucun | Disponible |
| **Consulting-core** | Identifié roadmap | Canon métier (frameworks consulting B2B), 5 skills production (`generate-client-deliverable`, `pipeline-review`, `productize-method` + 2), 1 client pilote | T+3-6 mois après 1er signal demande validé |
| **Media-buyer-freelance** | Identifié roadmap | Skills retainer reporting + client dashboard + cross-account benchmark, 1 client pilote | T+2-4 mois |
| **Coach-expert pack** | Identifié roadmap | Canon pédagogique (frameworks productisation knowledge), `methodology-map` + `cohort-curriculum` + `productize-framework`, 1 client pilote | T+3-5 mois |
| **Recherche appliquée** | Conceptuel | Encodage à designer, demande non mesurée | Non engagé |
| **Compliance vertical** | Conceptuel | Cadres légaux variables par juridiction, opérateur expert | Non engagé |

### Effort par vertical pack (estimation indicative)

Trois composantes :

1. **Canon métier à encoder** : auteurs + frameworks de référence, structurés en variables exploitables par l'agent. 2-4 semaines temps plein selon maturité du domaine. Primitive `suggest-domain-canon` accélère cette étape pour les domaines avec canon établi.
2. **Skills production à scaffolder** : typiquement 5 à 8 skills par vertical pack pour couvrir les tâches structurantes. 2-4 semaines.
3. **Premier client pilote** : déploiement réel, capture des frictions, itération. 4-8 semaines avant de pouvoir packager publiquement.

**Total ordre de grandeur : 2-4 mois par vertical pack mature**, sous condition d'un opérateur expert disponible pour valider le canon et un client pilote engagé.

---

## 8. Knowledge packs comme produit séparé (future+)

Trigger : framework le framework de provenance écrit (déclenché par 2e opérateur connecté, 1er knowledge pack vendu, 1er skill tiers).

**Hypothèse produit** : les canons encodés ont une valeur intrinsèque, indépendamment du workspace qui les héberge. Un *pack copywriting DTC clean* (le canon copywriting déjà livré, isolé et packageable), un *pack media buying gambling FR* (compliance + frameworks acquisition spécifique), un *pack consulting discovery B2B* (méthodologie de qualification + objections + proposal frameworks) peuvent se vendre comme assets standalone à des opérateurs qui possèdent déjà PhantomOS ou un environnement compatible.

### Conditions de déploiement marketplace

- **Le framework de provenance écrit** : provenance, attribution, license tracking, mécanisme de signalement de contamination.
- **Format d'asset stable** : schema d'un knowledge pack (structure dossier, manifest, dépendances skills, version, licence), versionnable et auditeable.
- **Trois packs internes éprouvés** avant ouverture tiers, pour valider que le format encaisse plusieurs domaines sans cas particulier.
- **Mécanisme de pricing** : fixed price, abonnement, pay-per-use ; à tester sur les premiers packs internes.

Ce mode rapproche le produit du modèle *vertical AI marketplace* émergent sans en adopter les contraintes : l'opérateur reste propriétaire de son environnement, les packs sont des extensions, pas des SaaS verticaux fermés.

---

## 9. Risques commerciaux identifiés

Trois risques structurants à expliciter pour ne pas les subir.

**Auto-replacement consultant.** Un consultant qui encode sa méthode dans le workspace d'un client lui transmet, après 6 mois d'usage, le moat et la justification budgétaire pour mettre fin au retainer. Mitigation : trois patterns décrits en section 6 (contractual licensing, workspace separation, outcome-based pricing). Aucun n'est enforcé par l'outil aujourd'hui ; c'est de la discipline opérateur. Risque stratégique principal pour la cible *agency owner* et *senior consultant*. À adresser frontalement dans la conversation commerciale, pas à cacher.

**Commodification du modèle IA sous-jacent.** Anthropic, OpenAI, Google convergent vers des modèles fungibles. Ce n'est **pas un risque pour PhantomOS** : la valeur n'est pas dans le modèle (qui sera commodifié), elle est dans la connaissance structurée et la méthodologie codifiée que l'opérateur accumule dans son workspace. À expliciter dans toute conversation de vente où l'objection *"et si Claude / GPT s'améliore tellement que je n'ai plus besoin de ton outil ?"* émerge. Argument inverse : plus le modèle s'améliore, plus la qualité de l'output dépend de la qualité du contexte, ce que PhantomOS structure.

**Dépendance Anthropic actuelle.** PhantomOS tourne sur Claude Code. Provider-agnosticisme est un objectif déclaré, mais non vérifié à grande échelle. Risque : changement de pricing Anthropic, changement de policy, ou éviction de Claude Code. Mitigation : architecture conçue pour découpler le runtime de l'agent du contenu encodé (le workspace est un dossier de fichiers, pas une base de données propriétaire). Validation empirique pending (cf. roadmap *empirical token benchmark*).

**Risque mineur mais probable : pas d'adoption.** Un projet qui reste l'outil personnel de son créateur, aussi raffiné soit-il, n'est pas un produit. Le test de validité empirique est mesuré en **utilisateurs externes actifs**, pas en sophistication de la thèse. Adresser commercialement signifie : prioriser le 1er, le 3e, et le 10e client commercial signés avant d'enrichir la doctrine au-delà du strict nécessaire.

---

## 10. Status

**Draft S46.** Document écrit après validation production live de la doctrine v2.11.0 (S45) et sacralisation de la pitch posture institutionnelle (D#367, S46). Le pricing initial n'est pas arrêté ; les vertical packs futurs ne sont pas signés ; le framework de provenance n'est pas écrit ; la doc `transmissibility-framework.md` n'est pas drafted.

Cette doc s'enrichit au fur et à mesure que :

- Le 1er client commercial signe (déclenche pricing final).
- Le 2e profil non-DTC adopte (déclenche pricing target segmenté par vertical).
- Le 1er vertical pack non-DTC matures (déclenche méthodologie pack-specific).
- Le multi-tenant ou le knowledge pack vendu trigger (déclenche le framework de provenance + transmissibility-framework.md).

Toute évolution se fait par patch additif : chaque section porte la version qui l'a verrouillée si elle évolue, et les versions précédentes deviennent SUPERSEDED non supprimées (cohérence avec la doctrine append-only de l'OS lui-même).

---

## Sources et inputs

- `vision.md` : postulat fondateur interne, full fat (D#307 Extractibility, D#362 architecture finale 5-doctrines).
- `manifesto.md` : thèse publique (first-party : chiffres du moteur uniquement, zéro stat de marché tierce depuis v2.89.1).
- `prisms.md` : huit angles produit pour calibrer les framings commerciaux.
- `roadmap.md` : vertical packs future iteration et future (consulting-core, media-buyer-freelance, coach-expert-pack, multi-operator).
- `fit.md` : best fit / conditional fit / misfit + cost honesty + consultant tension upgraded S46.
- `decisions.md` : D#307 (Extractibility), D#362 (architecture doctrinale), D#367 (pitch posture sacralisée + suggest-domain-canon).
- Memory cross-session : `feedback_phantomos_pitch_posture`.
