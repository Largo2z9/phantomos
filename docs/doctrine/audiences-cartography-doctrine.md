# Cartographier ses audiences · la méthode 3 niveaux et 4 questions

> *"Femmes 30-55 n'est pas une audience, c'est une démographie. La cartographier veut dire passer à 4 audiences mères × 12 sous-poches segmentées par stage de conscience et porte d'entrée."*

## L'enjeu

Le marketeux qui cible "femmes 30-55" en paid découvre vite la sanction. CTR plat, CPM cher, ROAS sous le break-even. Personne ne se reconnaît dans l'ad. La raison n'est pas le créatif ni le bidding. C'est l'audience elle-même, qui n'en est pas une.

Une démographie (âge, genre, géo, revenu) n'est qu'un filtre de targeting platform. Elle dit qui se trouve dans le bassin. Elle ne dit pas pourquoi cette personne va cliquer, ouvrir le portefeuille, recommander à une amie. La question qui suit (le pourquoi) appartient à un autre objet · l'audience opérable.

Une audience opérable se définit par trois variables imbriquées · une porte d'entrée (le scénario life-moment qui déclenche la recherche), un stage de conscience (Schwartz, position du prospect sur l'échelle awareness → most-aware), un sub-cluster psychographique (sophistication marché, sensibilité prix, identité projetée). Quand ces trois variables sont cartographiées, le copy se calibre, le visuel se cible, le funnel se séquence. Sans cartographie, le marketeux pulvérise du spend sur un brouillard démographique.

Cette doctrine propose une méthode de cartographie en 3 niveaux (broad → segment → micro) et 4 questions canon qui forcent le passage de la démographie à l'audience opérable. Sortie · une carte 3-5 mères × 8-15 sous-poches par marque, exploitable en paid, en copy, en CRM, en product.

**Ontologie pure v2.64 · pain_points + objections sont OWNED sub-folders audiences/{slug}/.** L'audience est l'entité root cartographiée par cette doctrine (porte d'entrée + stage + sub-cluster), et ses pain_points + objections vivent dans des sub-folders OWNED audience-specific · `brands/{brand}/audiences/{slug}/pain_points/PNT-NN.json` + `brands/{brand}/audiences/{slug}/objections/OBJ-NN.json`. Storage path · sémantique pure (expression subjective audience-specific). Le v2.63 status quo (collections top-level brand-wide séparées) deprecated · le canon Notion stride-up était un compromis opérationnel UI, pas sémantique pure. Sémantiquement, un pain ou une objection sont l'expression subjective d'une audience donnée · même formulation canonique peut diverger entre stress-pro et post-partum (severity, lifecycle, counter-pattern). Le storage OWNED sub-folder rend cette propriété explicite. Voir doctrines sœurs · `pain-benefit-chain-doctrine.md` (PNT-NN canon) et `objections-mapping-doctrine.md` (OBJ-NN canon).

## Les principes canon

**Principe 1 · Démographie n'égale pas audience.**

Une démographie (femmes 30-55, urbaines, revenu 50k+) est un filtre de targeting. Une audience opérable est un comportement contextualisé. Une femme de 38 ans qui vient d'avoir un bébé et une femme de 38 ans cadre dans une scale-up tech ne sont pas la même audience, même si elles cochent la même case démographique. Elles ont deux portes d'entrée distinctes, deux JTBD (Jobs to be Done · Clayton Christensen, Tony Ulwick), deux niveaux de sophistication.

**Principe 2 · Une audience égale une porte d'entrée.**

La porte d'entrée est le moment de bascule. Le scénario concret qui pousse le prospect à chercher une solution. "Je viens d'avoir un bébé et je dors plus" est une porte. "Femmes post-partum" n'est qu'une étiquette qui contient des portes différentes (1er enfant choc, 2ème enfant burnout, allaitement difficile, partenaire absent). La porte se source par verbatims clients réels (reviews 5-étoiles et 1-étoile, DMs Instagram, entretiens, search queries Google Trends), jamais par hypothèse interne.

**Principe 3 · Le stage de conscience définit l'approche copy.**

Eugene Schwartz dans Breakthrough Advertising (1966, canon absolu de la profession) identifie 5 stages · Unaware, Problem-Aware, Solution-Aware, Product-Aware, Most-Aware. Une audience à 80% Unaware ne se travaille pas comme une audience à 80% Product-Aware. Le copy d'entrée diffère, le hook diffère, la promesse diffère. Cartographier une mère sans stage = cartographie incomplète.

**Principe 4 · Le sub-cluster psychographique tranche la sophistication.**

À l'intérieur d'une mère, deux personnes au même stage Schwartz peuvent réagir différemment. Sophistication marché (Schwartz · 5 stages parallèles, du "j'ai jamais vu cette catégorie" au "j'ai tout essayé"). Sensibilité prix (price-driven vs value-driven vs prestige-driven). Identité projetée (founder, athlète, parent, créatif). Le sub-cluster désambigue la sous-poche.

**Principe 5 · Trois niveaux maximum.**

Mère (broad, 10-100k personnes accessibles selon niche). Sous-poche (segment, 1-10k). Micro (niche operable, 100-1k). Au-delà, fragmentation sans gain conversion. Un budget paid spliité sur 12 audiences ultra-niche fait tomber chaque audience sous le seuil de scale Meta (CBO ou ABO), aucune n'apprend, le compte stagne. Cap doctrinal · 3 niveaux, 3-5 mères, 2-4 sous-poches par mère.

**Principe 6 · Cartographier les chevauchements.**

Une mère peut overlap une autre. Une founder-mom est à la fois mère stress-pro et mère post-partum 1er-enfant. Ce chevauchement est documenté explicitement. Deux usages · exclusion paid (Meta Ads exclusion lists pour éviter double-exposure) ou opportunity (cross-sell, identity reinforcement, story-arc qui relie deux mères dans la même séquence email).

## La méthode · 4 questions canon

La cartographie de chaque mère se construit en répondant à 4 questions, dans l'ordre.

### Question 1 · Quelle est la porte d'entrée ?

La porte d'entrée est le SCÉNARIO life-moment qui pousse le prospect à chercher une solution. Pas un trait démographique. Une situation vivante, datée, contextualisée.

Trois critères qualifient une porte ·

- **Concrétude** · on peut visualiser la scène (la salle de bain, le matin, le miroir, la photo de mariage)
- **Déclencheur identifiable** · un événement précis (un anniversaire, un check-up médical, une remarque de partenaire, une photo)
- **Tension émotionnelle ressentie** · le prospect ressent une douleur, une frustration, une honte, une peur ou une envie suffisamment forte pour chercher activement

Exemples cross-niches ·

| Niche | Porte d'entrée canon | Déclencheur |
|---|---|---|
| Sleep supplements | "Je viens d'avoir un bébé et je dors plus" | Naissance enfant < 6 mois |
| Hair growth (Hims) | "J'ai vu ma photo de mariage et ma calvitie est devenue visible" | Photo formelle qui révèle |
| Skincare anti-aging | "J'ai 40 ans et je vois apparaître des tâches" | Anniversaire seuil + miroir matin |
| Greens (Athletic Greens) | "Je commence un nouveau job stressant" | Changement professionnel, énergie en chute |
| Fashion DTC (Allbirds) | "J'ai pris ou perdu 10kg, ma garde-robe me va plus" | Body transition post-grossesse, post-régime, post-stress |
| Mattress (Casper) | "Je déménage dans mon premier appart" | Premier mobilier adulte |
| Eyewear (Warby Parker) | "Mon ophtalmo m'a annoncé que je suis presbyte" | Diagnostic médical, première paire de lunettes |
| Fitness wearable (Whoop) | "Mon coach m'a dit que mon récup est insuffisante" | Plateau performance sportive |
| Insurance DTC (Lemonade) | "Je viens de signer mon premier bail" | Premier appart locataire, demande propriétaire |
| Payments B2B (Stripe) | "On lance un side project et il faut accepter des cartes" | First indie product launch |

Le sourcing de la porte · mining de verbatims clients réels. Reviews Amazon, Trustpilot, Google. DMs Instagram et TikTok. Entretiens téléphoniques (5-10 clients récents). Search queries (Google Trends, AnswerThePublic, Reddit). Forums niche (Reddit communities, Discord servers, Facebook groups). Negative reviews particulièrement riches (1 et 2 étoiles · le client dit pourquoi il a cherché et pourquoi le produit a déçu, double information).

### Question 2 · Quelle est la granularité ?

Doctrine 3 niveaux. Pour chaque mère identifiée, choisir le niveau de granularité utile au cas d'usage.

**Niveau Mère (broad)** · porte d'entrée + besoin générique. Taille 10-100k personnes accessibles par paid platform. Usage · campagnes prospecting top of funnel, brand-building, awareness. Copy générique de la mère, hooks plusieurs angles testés en parallèle.

**Niveau Sous-poche (segment)** · mère + sub-cluster psychographique. Taille 1-10k personnes. Usage · campagnes prospecting middle-funnel, retargeting catégoriel, séquences email post-opt-in segmentées. Copy calibré au sub-cluster.

**Niveau Micro (niche operable)** · sous-poche + variable behavioral spécifique (lookalike d'acheteurs récents, intent signal précis, custom audience source). Taille 100-1k. Usage · campagnes bottom-funnel, retargeting chaud, séquences acquisition haute conversion. Copy ultra-spécifique, témoignages ciblés.

**Cap 3 niveaux**. Au-delà, l'opérateur paid pulvérise son budget. Chaque audience tombe sous le seuil de learning Meta (50 conversions / 7 jours pour CBO). Aucune ne sort de phase learning, le compte stagne. Anti-pattern classique · "j'ai 27 audiences ultra-niche" = aucune ne scale.

Règle de décision granularité · si la mère a un volume suffisant (10k+) et que les sous-poches sont psychographiquement distinctes (les hooks ne sont pas interchangeables), descendre à sous-poche. Sinon, rester à mère et tester variations hook à l'intérieur.

### Question 3 · Quel stage de conscience ?

Application de la doctrine Schwartz 5 stages par audience. Pour chaque mère, estimer la distribution approximative ·

- **Unaware** · le prospect n'a pas conscience qu'il a un problème. Travailler en story-driven, education-first, soft-promise.
- **Problem-Aware** · conscience du problème, pas encore de la solution. Travailler en problem-agitation, empathy, then pivot solution.
- **Solution-Aware** · connaît qu'une solution existe, ne connaît pas les produits. Travailler en mechanism-of-action, why-now, differentiation.
- **Product-Aware** · connaît plusieurs produits, n'a pas encore choisi. Travailler en comparison, social proof, authority, offer stacking.
- **Most-Aware** · connaît, compare, est en train de décider. Travailler en urgency, scarcity, risk-reversal, last-mile objection handling.

Une audience n'est pas mono-stage. Une mère typique a une distribution. Exemple · sleep supplements mère stress-pro · 10% Unaware, 30% Problem-Aware, 40% Solution-Aware, 15% Product-Aware, 5% Most-Aware. La distribution dicte le mix de copy approaches à déployer.

Application au funnel ·

- TOFU (top of funnel) prospecting · Unaware + Problem-Aware (70%+ du spend)
- MOFU (middle) retargeting catégoriel · Solution-Aware (transition)
- BOFU (bottom) retargeting chaud · Product-Aware + Most-Aware

La cartographie stage permet de séquencer le funnel, pas seulement le copy d'un asset isolé.

### Question 4 · Quels chevauchements ?

Une mère peut overlap une autre. Documenter explicitement les overlaps majeurs (mediums et forts, low n'est pas exploitable).

Trois usages des chevauchements ·

**Exclusion paid** · si overlap fort entre mère A et mère B et qu'on les fait tourner en campagnes parallèles, exclure A en custom audience de B (et vice versa) pour éviter double-exposure (ROAS pollué, frequency inflation, ad fatigue accélérée).

**Sequencing CRM** · overlap permet de séquencer un email parcours qui touche deux mères en parallèle ("tu es founder ET 1er-enfant, voici une promesse qui te parle des deux à la fois").

**Identity reinforcement** · pivot copy basé sur l'identité partagée ("femme leader qui prend soin de soi" relie corporate-30-45 et founder-mom sans forcer un seul archétype).

Pas tous les chevauchements sont actionnables. Distinguer overlap démographique (low signal, deux mères qui partagent juste l'âge) d'overlap comportemental (high signal, deux mères qui partagent porte d'entrée et stage de conscience).

## La méthode · workflow concret

Workflow opérateur cartographie en 6 étapes ·

1. **Mining VoC (Voice of Customer)** · 100-300 verbatims minimum sourcés (reviews 5/4/2/1 étoiles, DMs, entretiens, forums). Coder par thème récurrent.
2. **Identification portes d'entrée** · sur les 100-300 verbatims, extraire 5-10 portes candidates. Regrouper les portes similaires.
3. **Validation portes** · chaque porte doit cocher concrétude + déclencheur + tension. Drop les portes trop vagues.
4. **Définition mères** · 3-5 mères par marque (rarement plus, rarement moins). Une mère = une porte dominante + un besoin.
5. **Décomposition sous-poches** · 2-4 sous-poches par mère. Variable de sub-cluster psychographique.
6. **Stage de conscience + chevauchements** · estimer distribution stages par mère, mapper chevauchements forts.

Output canon · un document 1 page par mère (porte d'entrée, taille estimée, 2-4 sous-poches, distribution stages, chevauchements). 3-5 documents pour une marque mature.

## Cartographie audience ≠ ad targeting (distinction canon)

La cartographie audience PhantomOS canon v2.64 segmente le SUBSTRAT (qui souffre quoi · pain points + objections + JTBD par segment distinct hiérarchique parent/enfants). C'est de l'encodage stable territoire.

L'ad targeting RUNTIME est une DÉCISION PRODUCTION distincte · qui voit l'ad. Une ad copy peut combiner plusieurs audiences cartographiées en single narrative quand crossover existe.

**Pattern observed (TrendTrack live 2026-05-16 · Stepprs foot care DTC)** ·

Brand cartographiée 2 audiences mères (workers-shifts + chronic-pain-45) avec 5 sous-poches. Strategy paid réelle observée · 1 narrative hero (Michelle testimonial · plantar fasciitis morning pain + 10h shifts work boots) répliqué 27 EU countries · single ad copy combine les 2 segments via crossover verbatim. Cross-narrative targeting cohérent avec cartographie · pas contradictoire.

**Canon décision** ·
- Cartographie audience N segments · valide pour substrat stable territory-discipline
- Ad targeting M ads runtime · M peut être < N · plusieurs audiences combinées single ad copy si narrative crossover
- Première production paid · commencer simple (1 angle hero cross-audience) puis diversifier au fil des learnings · pas l'inverse
- Annotation canon NEW · `_meta.cross_narrative_notes` sur audience mère quand cross-targeting pattern observé · documente l'opportunité sans forcer la séparation

Pattern reproductible cross brands · audiences cartographiées séparées + production runtime décide single ad cross-audience OR N ads séparées selon scaling strategy + learnings.

Cross-refs · `territory-doctrine.md` (encodage stable substrat), `progressive-cartography-doctrine.md` (cartographie hypothèse confidence 0.5 valide avant mining), `compositional-cartography.md` (NOYAU × CONTEXTE × MODIFIEURS · CONTEXTE audience-spécifique cohabite avec NOYAU mécanique cross-audience), ANG-01 hero angle pattern, LRN-0002 cross-narrative single-narrative observation.

## Cross-refs · sub-folders OWNED audience-specific + shared via cross-refs (v2.64)

L'audience cartographiée par cette doctrine est l'entité root, et ses sub-tensions (pain_points, objections) sont des sub-folders OWNED dans le dossier audience (audience-specific). Les frictions vivent en sub-folder OWNED des produits (product-specific). Storage paths sémantique pure ·

| Collection | Path canonical OWNED | ID format | Doctrine source |
|---|---|---|---|
| `audiences/` | `brands/{brand}/audiences/{slug}/profile.json` | slug | `audiences-cartography-doctrine.md` (ce fichier) |
| `pain_points/` (sub-audience) | `brands/{brand}/audiences/{slug}/pain_points/{PNT-NN}.json` | PNT-NN | `pain-benefit-chain-doctrine.md` |
| `objections/` (sub-audience) | `brands/{brand}/audiences/{slug}/objections/{OBJ-NN}.json` | OBJ-NN | `objections-mapping-doctrine.md` |
| `frictions/` (sub-product) | `brands/{brand}/products/{slug}/frictions/{FRC-NN}.json` | FRC-NN | (encodage runtime usage produit) |

Cross-refs canonical · les pain_points + objections shared entre plusieurs audiences sont stockés audience-specific dans le primary owner, avec `also_affects_audiences[]` array (slugs autres audiences impactées). Si PNT-01 "sommeil profond perturbé" affecte stress-pro + post-partum + senior-insomnie, encodé dans audience primary (typiquement stress-pro) avec `also_affects_audiences: [post-partum, senior-insomnie]`. Évite duplication, expose visibility cross-audience explicite. Drill audience-specific via `/phantom {brand} audiences {slug}` (entity-drill 360° expose profile + pain_points + objections inline + cross-refs inbound).

## Exemples concrets · cas pratiques cross-niches

### Cas pratique 1 · brand sleep supplements (référence Sentage, Olly Sleep)

Démographie de démarrage · "femmes 30-55, urban, stressed".

Output démographie · audience trop large pour paid. Hook "améliore ton sommeil" générique, CTR 0.4%, CPA hors business model.

Cartographie 3 niveaux ·

**Mère #1 · Stress-pro**
- Porte d'entrée · "Mon job me consume, je rumine la nuit, je dors 5h"
- Taille estimée · ~50k FR + EU active
- Stage dominant · Solution-Aware (60% · sait que les supplements existent)
- Sous-poches · founder-mom solo entrepreneurship, corporate-30-45 manager 50+ équipe, freelance-creative agence ou DA
- Chevauchement fort avec mère #2 (founder-mom × 1er-enfant)

**Mère #2 · Post-partum**
- Porte d'entrée · "J'ai un bébé < 2 ans et je dors plus, mon corps est encore en récup hormonale"
- Taille estimée · ~30k FR + EU active
- Stage dominant · Problem-Aware (50% · cherche solution mais ne connaît pas mécanisme)
- Sous-poches · 1er-enfant-choc (réveil brutal réalité parentale), 2ème-enfant-overwhelmed (gestion + ainé), partner-absent (mono-parentalité partielle ou totale)
- Chevauchement medium avec mère #4 (post-partum × athlete-recovery, mamans sportives qui veulent reprendre)

**Mère #3 · Pré-ménopause / périménopause**
- Porte d'entrée · "J'ai 45+, je commence à mal dormir, hot flashes la nuit, hormones qui bougent"
- Taille estimée · ~80k FR + EU active
- Stage dominant · Unaware → Problem-Aware transition (40% Unaware au début parcours, 40% Problem-Aware en cours)
- Sous-poches · perimenopause-early-symptoms (40-45 ans), hormonal-shifts-confirmed (45-50 ans diagnostic), postmenopause-insomnia (50+ ans chronique)
- Chevauchement low avec mère #1 (peu de stress-pro 45+ avec carrière encore en construction)

**Mère #4 · Athlete recovery**
- Porte d'entrée · "Je m'entraîne intensif et ma récup est cassée, je sens que je récupère plus comme avant"
- Taille estimée · ~15k FR + EU active (niche)
- Stage dominant · Product-Aware (70% · niche éduquée, connaît melatonin, magnesium, ashwagandha, compare brands)
- Sous-poches · runners marathon training, crossfitters compete level, weightlifters strength training
- Chevauchement medium avec mère #1 (founder-mom qui fait du sport intensif comme exutoire stress)

**Total cartographie** · 4 mères × ~3 sous-poches = ~12 audiences opérables. Chevauchements documentés. Distribution stages par mère.

Application paid · 4 campagnes prospecting (1 par mère), copy calibré porte + stage dominant. Sous-poches en variations hook à l'intérieur de chaque campagne. Exclusions cross-mères entre #1 et #2 (overlap fort founder-mom × 1er-enfant).

### Cas pratique 2 · brand fashion DTC (référence Allbirds, Patagonia-style)

Démographie de démarrage · "millennials, eco-conscious, $50k+ income, urban".

Cartographie ·

**Mère #1 · Urban-pro qui cherche shoes confort + style**
- Porte · "Je passe la journée à marcher entre métro, bureau, soir, et mes shoes me défoncent les pieds"
- Sous-poches · tech-worker remote, consultant déplacements, parent-pro urban commute

**Mère #2 · Outdoor-enthusiast pondéré**
- Porte · "Je fais du randonnée + city, je veux un shoe qui supporte les deux"
- Sous-poches · weekend-hiker, urban-explorer, light-traveler

**Mère #3 · Sustainability-conscious (eco-buyer)**
- Porte · "J'ai lu un article sur l'industrie textile et je veux acheter mieux"
- Sous-poches · climate-activist, conscious-consumer trendy, parent-modeling-values (parents qui veulent transmettre valeurs aux enfants)

Output · 3 mères × ~3 sous-poches = ~9 audiences. Distribution stages variée (eco-buyer souvent Solution-Aware via media exposure, urban-pro souvent Problem-Aware par pain pied direct).

### Cas pratique 3 · brand B2B SaaS (référence Linear, Notion)

Cartographie ICPs (Ideal Customer Profile). B2B diffère DTC sur deux dimensions · acheteur n'égale pas utilisateur (decision-maker vs end-user) et cycle vente longer.

**Mère #1 · Startup founder (Linear ICP canon)**
- Porte · "On vient de lever une seed, on doit shipper un produit, Asana est trop lourd"
- Stage dominant · Solution-Aware (80%)
- Sous-poches · technical-founder solo, founder + 2 devs, founder + non-tech co-founder
- Variable additionnelle · funding stage (pré-seed, seed, série A) influence willingness-to-pay

**Mère #2 · Enterprise PM**
- Porte · "Mon équipe utilise 5 tools, je veux consolider"
- Stage dominant · Product-Aware (60% · compare Asana, Monday, Jira)
- Sous-poches · PM tech 50-200 employees, PM scale-up 200-1000, PM enterprise 1000+

**Mère #3 · Agency creative**
- Porte · "Je gère 8 clients en parallèle et je perds le fil"
- Stage dominant · Problem-Aware (50%)
- Sous-poches · creative agency 5-20 people, design studio solo + 3, dev agency consulting

Output · 3 mères × ~3 sous-poches × variable verticale (size + maturity) = ~9-15 audiences opérables.

## Pitfalls classiques

**Pitfall 1 · Cibler une démographie au lieu d'une audience opérable.**

"Femmes 30-55" est un filtre, pas un cible. Le filtre est nécessaire (paid platforms l'imposent), mais insuffisant. Le copy doit s'adresser à une porte d'entrée précise, pas à une tranche d'âge. Conséquence ignorer · CTR sous 0.5%, CPM en hausse continue par ad fatigue générique, ROAS bloqué sous break-even.

**Fix** · pour chaque démographie, mapper 3-5 portes d'entrée distinctes, créer 3-5 angles copy distincts.

**Pitfall 2 · Mono-audience trap (1 audience pour 1 produit).**

Le founder du brand pense que son produit s'adresse à "tout le monde" ou "un seul type". La réalité · la plupart des produits ont 3-5 audiences opérables distinctes. Limiter à une seule mère = laisser 70%+ du marché potentiel sur la table.

**Fix** · forcer minimum 3 mères par cartographie initiale. Si la brand ne trouve que 1-2 mères, le produit a un problème de proposition de valeur (trop niche ou trop générique).

**Pitfall 3 · Fragmentation ultra-niche.**

Le marketeux qui découvre la cartographie peut tomber dans le piège inverse · 27 audiences ultra-niche de 200 personnes chacune. En paid, chaque audience tombe sous le seuil de learning Meta (50 conversions / 7 jours), aucune ne scale, le compte stagne.

**Fix** · cap 3 niveaux doctrinal. 3-5 mères, 2-4 sous-poches par mère. Niveau micro réservé aux campagnes BOFU retargeting chaud avec historique conversion.

**Pitfall 4 · Confusion démographie / stage de conscience.**

Le marketeux assume que "femmes 30-55" sont toutes Problem-Aware sur sleep. Faux · à l'intérieur de cette démographie, 20% sont Unaware (n'attribuent pas leur fatigue au sommeil), 40% Problem-Aware, 30% Solution-Aware, 10% Product-Aware.

**Fix** · cartographier la distribution stages par mère, pas par démographie. Calibrer copy mix sur la distribution.

**Pitfall 5 · Chevauchements ignorés.**

Mère A et Mère B ont 30% overlap, font tourner deux campagnes parallèles sans exclusion. Double exposure, frequency 2x trop élevée, ad fatigue accélérée, ROAS pollué (les conversions sont attribuées à la dernière campagne touchée, fausse les apprentissages).

**Fix** · documenter overlaps majeurs, exclure en custom audience paid OU séquencer en email CRM pour exploiter overlap.

**Pitfall 6 · Audiences inventées (projection brand).**

Le marketeux ou le founder invente l'audience à partir de son copy déjà écrit. Projection · "notre client idéal est X" sans aucun sourcing. Décalage copy / audience réelle invisible jusqu'au paid scaling fail.

**Fix** · sourcing obligatoire avant cartographie. Minimum 100-300 verbatims réels (reviews, DMs, entretiens). Aucune mère sans 10+ verbatims qui matchent.

**Pitfall 7 · Cartographie statique (faite une fois, jamais update).**

L'audience évolue. Le marché change. Les concurrents éduquent (Solution-Aware → Product-Aware migration). Une cartographie de 2024 ne tient pas en 2026.

**Fix** · re-cartographier 1x par an (refresh complet) ou à chaque shift majeur du marché (entrée nouveau gros concurrent, scandale niche, réglementation).

**Pitfall 8 · Le miroir des avis (biais du survivant).**

Le symétrique exact du Pitfall 6. Là où le Pitfall 6 invente une audience sans la sourcer, celui-ci s'enferme dans la donnée existante · cartographier les audiences depuis les seuls avis, clients actuels, verbatims collectés. Le piège est invisible parce qu'il a l'air rigoureux (« je source tout »). Mais les avis ne contiennent que les déjà-servis · qui a acheté, résolu l'objection prix, cru la promesse. L'audience que le mécanisme du produit pourrait atteindre mais que la marque n'adresse pas encore n'a jamais laissé d'avis · elle est structurellement absente de la donnée. Lire les audiences au miroir des avis reproduit donc le client qu'on a déjà et reste aveugle au marché non capté.

**Fix** · dériver d'abord les audiences candidates depuis le mécanisme et l'usage (quel job le produit peut servir, quel moment, qui vit ce moment), PUIS qualifier. Une audience dérivée-du-mécanisme sans verbatim n'est pas une audience inventée (Pitfall 6) · c'est une hypothèse à confiance faible avec son levier de validation (carte ouverte · `open-map-reasoning.md`). Le seuil de 10+ verbatims du Pitfall 6 reste la barre pour PROMOUVOIR une mère en cœur validé · il ne borne pas l'exploration. Les deux pitfalls se tiennent ensemble · ne pas inventer (sourcer), ne pas s'aveugler (dériver du mécanisme).

## Checklist applicable · cartographie d'une mère

Pour chaque mère identifiée, valider ·

- ☐ Porte d'entrée nommée (scénario life-moment concret, déclencheur identifiable, tension émotionnelle) ?
- ☐ 2-4 sous-poches identifiées (sub-cluster psychographique distinct) ?
- ☐ 3 niveaux respectés (mère → sous-poche → micro, pas au-delà) ?
- ☐ Stage de conscience dominant identifié (Schwartz 5 stages) ?
- ☐ Distribution stages estimée (% par stage, pas mono-stage) ?
- ☐ Sub-cluster distinguant (sophistication marché, sensibilité prix, identité projetée) ?
- ☐ Chevauchements avec autres mères mappés (forts et mediums, pas low) ?
- ☐ Sourcing client réel (minimum 10 verbatims par mère, reviews / DMs / entretiens / forums) ?
- ☐ Taille estimée (broad 10-100k, segment 1-10k, micro 100-1k) ?
- ☐ Mère exploitable en paid (volume suffisant pour atteindre seuil learning Meta 50 conv / 7j) ?
- ☐ Mère exploitable en copy (porte d'entrée traduisible en hook ad sans ambiguïté) ?
- ☐ Mère re-cartographiable (process de refresh annuel ou shift-driven prévu) ?

## Position dans le système opérationnel 5 couches

Audiences cartography est une instance canonique de la couche 1 (modèle ·
ECR pattern Funnel auto-similaire) du système opérationnel PhantomOS (cf
`operational-system-doctrine.md`). Le pattern parent/enfants hiérarchique
(audience mère → sous-poches) est fractal · le même schéma de raisonnement
se répète à toutes les échelles d'audience.

La distinction cartographie audience ≠ ad targeting paid (canon v2.69.1)
touche aussi la couche 2 (règles) · règle canon de décision production runtime.

## Sources et lectures

**Canon historique**

- Eugene Schwartz, *Breakthrough Advertising* (1966). Référence absolue · 5 stages of awareness, 5 stages of market sophistication. Le seul livre que la profession lit, relit, et applique pendant 60 ans sans le challenger.
- Claude Hopkins, *Scientific Advertising* (1923). Fondateur direct response · "ne vends pas à tout le monde, vends à quelqu'un de précis".
- Gary Halbert, *Boron Letters* (1986). Lettres à son fils sur le métier · l'importance du "starving crowd" (l'audience qui a faim, le porte d'entrée vivante).
- John Caples, *Tested Advertising Methods* (1932). Testing rigoureux des hooks par audience.

**Canon moderne**

- Russell Brunson, *DotCom Secrets* (2015) et *Expert Secrets* (2017). Framework audience targeting funnel-driven · Dream 100, Hook-Story-Offer.
- Donald Miller, *Building a StoryBrand* (2017). Audience comme protagoniste d'une histoire, brand comme guide.
- Alex Hormozi, *$100M Offers* (2021) et *$100M Leads* (2023). Avatar definition, Grand Slam Offer · l'audience qui paie premium.
- April Dunford, *Obviously Awesome* (2019). Positioning by audience · "qui est le best customer pour ce produit ?".

**JTBD (Jobs to be Done)**

- Tony Ulwick, *Jobs to be Done · Theory to Practice* (2016). Méthode outcome-driven innovation. La porte d'entrée = le job du client.
- Clayton Christensen, *Competing Against Luck* (2016). Application JTBD au product et marketing. "Le client n'achète pas un produit, il embauche un produit pour faire un job."

**Behavioral economics et psy**

- Robert Cialdini, *Influence · The Psychology of Persuasion* (1984). 6 principes persuasion appliqués à l'audience.
- Dan Ariely, *Predictably Irrational* (2008). Biais cognitifs qui distinguent les sub-clusters psychographiques.
- Tony Robbins, *Unlimited Power* (1986). Profilage psychologique, identités projetées.

**Operational refs**

- Hubspot, *Inbound Marketing* methodology. Persona development moderne.
- VoC (Voice of Customer) research method · *Forrester*, *Gartner* whitepapers sur mining techniques.
- Meta Business *Audience Insights* documentation officielle (techniques de cartographie native platform).

**Tactical · sources mining**

- Reddit search par niche-specific subreddits
- Amazon Reviews API · scraping légal pour mining VoC
- Trustpilot · reviews 1 et 2 étoiles particulièrement riches
- Reddit Reviews · authenticité high
- Google Trends · queries seasonality + porte d'entrée timing
- AnswerThePublic · question patterns par keyword

---

*Doctrine maintenue · cartographie audience canon, métier copywriter / creative strategist / brand strategist. Aucune doctrine n'est définitive · le marché évolue, le canon s'enrichit, l'opérateur teste et corrige.*
