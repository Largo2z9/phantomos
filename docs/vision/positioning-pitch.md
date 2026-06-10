# PhantomOS, Positioning Pitch

> Pitch institutionnel officiel pour partenaires, prospects clients senior, agency owners et investisseurs. Posture validée S45, sacralisée comme référence durable. Extract-ready : tout extrait peut être copié-collé tel quel dans un deck, une note de fond, ou une conversation commerciale. Ton institutionnel sérieux et accessible, ni direct response punchy, ni marketing mou.

---

## Ce que c'est

PhantomOS est un environnement de travail local pour opérateurs paid DTC : la marque, les audiences, les angles et les apprentissages encodés dans des fichiers structurés et versionnés que l'opérateur possède, opérés par un agent IA. Le produit n'est pas une bibliothèque de contenu spécialisé. Le produit est **l'environnement lui-même** : les disciplines d'encodage des données, la mécanique de raisonnement de l'agent, l'extensibilité par l'utilisateur, et la persistance de la connaissance entre les sessions.

Le pattern est général, la preuve est locale : la même architecture peut encoder d'autres métiers, mais c'est sur le DTC paid que le système est livré, outillé et validé.

Le système est livré avec un kit de skills et de ressources métier prêtes à l'emploi, qui sert à la fois de démonstration de ce qui est possible et de point de départ utilisable. Ces skills et ressources livrés peuvent être utilisés tels quels, modifiés, remplacés, ou complétés par d'autres que l'opérateur ajoute lui-même au fil de l'usage.

## Le constat qui justifie son existence

Trois écarts récurrents apparaissent dès qu'on essaie d'industrialiser le travail intellectuel d'un métier de connaissance avec les outils IA disponibles.

**Le contexte ne s'accumule pas durablement.** Les outils IA grand public ont fait des progrès récents sur la mémoire (memory ChatGPT, Projects Claude, Custom GPTs), mais cette mémoire reste opaque, peu structurée, propriétaire au fournisseur, et non transposable d'un outil à l'autre. Le travail mental investi à brief le modèle ne se capitalise pas comme un actif que l'opérateur possède et structure lui-même.

**L'expertise méthodologique reste dans la tête des individus.** Quand ils partent ou quand on recrute, plusieurs semaines sont nécessaires pour transmettre ce contexte. La connaissance ne se capitalise pas comme un actif exploitable par l'agent.

**Les outils ne se parlent pas.** Notion pour la connaissance, Sheets pour la performance, le CRM, la plateforme média payant, plusieurs outils IA conversationnels en parallèle. L'opérateur fait l'intégration mentale et paie un coût de switching permanent. Aucune couche au-dessus ne maintient une vue cohérente du métier.

PhantomOS adresse ces trois écarts par une architecture ouverte et extensible, indépendante du domaine modélisé.

Le diagnostic est documenté : la plupart des systèmes d'IA générative en entreprise ne conservent rien, *"most GenAI systems do not retain feedback, adapt to context, or improve over time"* (MIT NANDA, 2025). Le problème n'est pas le modèle, il est architectural. Il se mesure aussi chez nous : sur le moteur créatif de PhantomOS, encoder les corrections en règles a fait passer la part d'outputs mal classifiés de 26% à 3,5%. La boucle qui manque aux projets qui échouent est exactement celle-là.

## Comment le système fonctionne

L'environnement repose sur quatre couches superposées, identiques quel que soit le métier encodé.

**Une couche réceptacle**, un workspace local sous forme de dossier de fichiers structurés. Cette couche est agnostique du métier. Elle définit où vivent les données, comment elles sont versionnées, comment elles sont mutées et auditées.

**Une couche d'encodage du métier**, où l'opérateur enregistre les données structurées de son activité : les entités centrales du domaine, leurs relations, les apprentissages cumulés, les décisions stratégiques verrouillées, la mémoire de session. Cette couche est extensible : actuellement optimisée pour les marques DTC paid acquisition, mais accueille tout autre domaine que l'opérateur souhaite modéliser via custom encoding.

**Une couche de ressources partagées**, où l'opérateur dépose les méthodologies, frameworks, registres, conventions et templates qu'il considère comme référence pour son domaine. Cette couche fonctionne comme une bibliothèque que l'agent consulte avant de produire un livrable. Elle est destinée à être enrichie par l'opérateur lui-même au fur et à mesure qu'il documente sa méthode.

**Une couche de capacités opérationnelles**, appelées skills, qui permettent à l'agent d'exécuter des tâches structurées en consommant les couches précédentes. L'opérateur peut utiliser les skills livrés par défaut, les modifier, les combiner en workflows, ou en créer entièrement nouveaux pour ses besoins propres.

L'utilisateur interagit avec le système en langage naturel. L'agent identifie l'intention, sélectionne la capacité pertinente, applique la méthodologie référencée, et produit un livrable défendable et traçable.

Tout le monde sait désormais que la qualité d'un agent dépend de ce qu'on met dans son contexte. Presque personne ne le fait avec discipline : un canon versionné, des corrections qui deviennent des règles, une trace à chaque mutation. PhantomOS est cette discipline, livrée en environnement de travail.

## Onboarding doctrine, posture light explicite

L'environnement est conçu pour qu'un opérateur soit productif dès la première session. La densification du contexte est progressive, jamais frontale.

**Profil opérateur d'abord, pas questionnaire initial.** Au démarrage, le système identifie qui est l'opérateur, comment il travaille, sur quels contextes il opère. Le workspace est immédiatement utilisable. Aucun formulaire d'admission n'est imposé avant de produire de la valeur.

**Premier jour, scrap rapide sur une nouvelle marque ou mission.** À partir d'une URL, le système produit en quelques minutes une fiche brève défendable sur le produit, le positionnement, et l'offre. L'objectif est de démontrer que les yeux de l'agent sont accurate sur le contexte avant tout autre engagement. Pas de gros rapport amont.

**Approfondissement à la demande.** Quand l'opérateur souhaite densifier, des agents spécialisés travaillent en parallèle sur les angles utiles, store, offres, audience, concurrence. Un chairman orchestrateur agrège les retours et flague les incohérences en mode interrogatif (*j'ai vu ceci, c'est intentionnel ?*), jamais comme une erreur de l'opérateur. La profondeur d'encodage reste un choix de l'opérateur, pas une obligation système.

Cette doctrine évite l'écueil classique des outils d'encodage qui imposent un onboarding lourd avant la première valeur, et se font abandonner avant même la fin du paramétrage.

## Ce qui est livré dans le kit par défaut

Pour rendre le système immédiatement utilisable et démontrer ce que peut produire un environnement bien rempli, PhantomOS est livré avec un kit initial constitué de :

- 82 skills versionnés couvrant les principales tâches d'un opérateur travaillant dans le marketing direct et l'e-commerce DTC : encodage initial d'une marque, extraction de la voix client, production de briefs publicitaires, audit de scripts existants, scoring d'offres, analyse de performance, génération de rapports clients,
- une bibliothèque de référence en copywriting et persuasion, regroupant les principes établis sur plusieurs décennies par les auteurs de référence du domaine, structurés sous forme de variables exploitables par l'agent,
- des registres et frameworks transverses qui permettent à l'agent de raisonner sur des combinaisons d'angles, d'audiences, de canaux et de leviers psychologiques.

**Le kit livré cible exclusivement le DTC paid acquisition.** Il permet à un opérateur DTC paid de démarrer immédiatement avec une production opérationnelle (angles, creatives, audiences, advertorials, audits setup). La plateforme reste extensible : un opérateur dans un autre métier peut créer son propre kit via custom encoding, mais ce n'est pas le scope commercial actuel.

## Ce que le système permet de faire

Les usages possibles dépendent du métier encodé et des skills disponibles. Sur le périmètre du kit livré, l'environnement couvre l'ensemble du cycle de vie d'une marque.

**En phase de recherche et de validation amont.** Identifier les segments d'audience prioritaires, miner les retours clients sur les sources publiques, cartographier les concurrents et les espaces blancs du marché, tester l'adéquation produit-marché sur des hypothèses early-stage.

**En phase de construction.** Produire des landing pages, des scripts vidéo, des séquences email, des accroches publicitaires, des briefs prêts à transmettre à un freelance ou à un membre d'équipe.

**En phase de scale.** Décliner un même message sur plusieurs canaux, générer des matrices d'angles ranked sur plusieurs audiences, capitaliser sur des patterns à travers plusieurs marques d'un même portfolio, automatiser le reporting client mensuel.

**En phase d'optimisation.** Auditer les setups techniques de media buying, analyser la performance avec contextualisation business, examiner des créas existantes contre la méthodologie de référence, scorer des offres concurrentes.

Au-delà de ces usages, l'opérateur peut construire des workflows propres à son process (par exemple un audit hebdomadaire client en quatre étapes) qu'il déclenche en une commande.

Le système est conçu pour que ces capacités s'étendent par ajout, jamais par remplacement. Un opérateur qui couvre un domaine non couvert par le kit initial développe ses propres skills, dépose ses propres ressources, et le système les intègre.

## Pour qui le système est conçu

PhantomOS est destiné aux opérateurs dont la valeur dépend d'une expertise méthodologique répétable, applicable à plusieurs contextes, marques ou clients.

Le premier angle de valeur, dominant pour la majorité des profils, est triple : **gain de temps mesurable** (zéro re-briefing, zéro switching cost entre outils), **interface unique centralisée** (un seul environnement remplace plusieurs onglets, plusieurs comptes, plusieurs bibliothèques disjointes), et **une avance pratique** (utiliser les disciplines d'encodage agentique sans devoir les construire soi-même).

Profils en fit direct :

- les fondateurs DTC passé le mois six avec ROAS stable, qui veulent productiser leur méthode d'acquisition payante (entre le mois trois et le mois six, post-premier-signal, le fit est conditionnel : structurer ce qui a un signal, pas des hypothèses),
- les growth leads en agence opérant entre 3 et 15 comptes DTC clients,
- les solo-opérateurs DTC paid qui passent l'essentiel de leur temps sur Meta, TikTok, Google Ads,
- les opérateurs portfolio gérant plusieurs marques DTC en propre ou en equity.

Profils hors périmètre : fondateurs pré-traction du jour zéro au mois trois (encoder des hypothèses non validées dégrade le système), info-products et services B2B (autre métier, autre stack), agences focalisées sur le social organic ou la distribution de volume créateur, agences enterprise multi-tenant (non couvert).

## Ce qui distingue le système

PhantomOS se positionne entre trois familles d'outils existants sans en être un.

**Vis-à-vis des outils IA conversationnels grand public** (ChatGPT, Claude, Gemini), il faut être lucide : ces outils ont récemment progressé sur la mémoire (memory features), les espaces dédiés (Projects, Custom GPTs), et l'interopérabilité (MCP, connecteurs natifs). PhantomOS n'oppose pas une mémoire à une absence de mémoire. Il oppose un encodage **structuré, métier-spécifique, possédé par l'opérateur** (entités, schemas, sourcing tags, registres méthodologiques) à une mémoire opaque et propriétaire au fournisseur. Quatre différenciants tiennent :

- la discipline d'écriture qui transforme chaque correction en règle persistante exploitable par l'agent à la session suivante,
- le compound effect comme propriété systémique : chaque livrable produit, chaque décision capturée, augmente la densité du système,
- l'interface unique centralisée qui remplace le switching cost entre une dizaine d'outils par un environnement cohérent,
- la propriété du format : le workspace est local, en fichiers lisibles, possédé par l'opérateur, transposable. Le runtime actuel est Claude Code ; le canon, lui, appartient à l'opérateur et part avec lui, quel que soit l'outil qui le lira demain.

**Vis-à-vis des bases de connaissance passives**, le système transforme la connaissance en ressource exécutable plutôt qu'en archive consultable. Les fichiers ne sont pas lus manuellement par un humain qui en extrait la valeur, mais composés en livrables par un agent. Encoder n'est pas logger : encoder structure la connaissance pour qu'un agent l'opère, logger l'archive pour qu'un humain la relise. La quasi-totalité des projets d'entreprise font du logging sophistiqué et l'appellent encoding. C'est le geste que Palantir vend aux Fortune 500 avec son Ontology, ramené ici à l'échelle d'un opérateur, dans un dossier de fichiers qu'il possède.

**Vis-à-vis des produits SaaS verticaux**, PhantomOS ne propose pas une interface fermée et figée mais un environnement ouvert, extensible par l'utilisateur, propriétaire de ses données, et applicable à plusieurs métiers au-delà du domaine d'illustration initial.

## Ce qui change structurellement pour l'utilisateur

L'effet de PhantomOS se manifeste sur trois axes.

L'utilisateur passe d'une production où chaque livrable est construit en réexpliquant le contexte, à une production où le contexte est déjà chargé et où l'agent s'appuie sur l'historique cumulé de la marque, du domaine ou du portefeuille.

L'expertise méthodologique cesse d'être une compétence individuelle non transmissible pour devenir une propriété du système. Le système est conçu pour que la qualité produite sur les tâches encadrées par les capacités encodées dépende de l'environnement, et plus seulement de l'individu qui l'opère, ce qui rend la scalabilité opérationnelle moins dépendante du recrutement. Cette propriété reste à démontrer en longitudinal chez des opérateurs externes ; c'est le test en cours.

À mesure que l'utilisation se prolonge (encodage progressif des marques, accumulation des apprentissages, développement de skills propres, raffinement de la méthodologie par l'opérateur), le workspace devient un actif défendable. La valeur n'est pas dans le modèle d'IA, qui restera commodifié, mais dans la connaissance structurée et la méthodologie codifiée que l'opérateur accumule dans son propre système.

Cette transformation rejoint la bascule documentée du marché vers la facturation du travail fini plutôt que du logiciel (*"sell work, not software"*, Sarah Tavel, Benchmark). La partie difficile n'est pas d'y croire, c'est d'échapper à l'écrasement des marges quand tout le monde y croit. C'est précisément ce que la propriété du canon protège : la méthode encodée reste un actif de l'opérateur, pas une feature du prestataire.

## Vision

PhantomOS livre actuellement un kit complet pour le DTC paid acquisition, là où la méthodologie de référence est mature, la demande pour l'industrialisation du travail intellectuel forte, et le terrain de validation immédiat. La plateforme reste extensible : un opérateur dans un autre métier peut créer son propre encodage custom, mais ce n'est pas le scope commercial actuel. Les vertical packs pour d'autres domaines (consulting, coaching, media buying autres canaux, etc.) restent en roadmap future+, conditionnés à une demande client réelle.

L'enjeu de fond est la transformation d'un talent humain rare en un système exploitable, composable et accumulable. Le niveau de qualité devient une propriété de l'environnement de travail, et non plus seulement de l'individu qui l'opère. C'est cette transformation que PhantomOS rend opérationnelle.

---

## Sources publiques citées

- MIT NANDA, *State of AI in Business 2025* (citée pour son diagnostic du learning gap, pas pour ses chiffres, méthodologiquement contestés).
- Sarah Tavel (Benchmark), *AI startups: sell work, not software* (2023).
- Palantir, *Ontology*, citée comme analogue d'échelle Fortune 500.
