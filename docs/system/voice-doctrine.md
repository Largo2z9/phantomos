---
name: voice-doctrine
description: Doctrine canon · ton reference-grade artefacts internes PhantomOS · 3 registres + 5 principes wording + politique FR/EN + casse + conventions typographiques + famille paramétrage + 8 anti-patterns + notes transparence
type: doctrine
version: v2.84.1
status: shipped
---

# Voice Doctrine · ton canon artefacts internes

Pose le ton reference-grade applicable à tous les artefacts écrits internes du repo. Le CLAUDE.md runtime joue le rôle de filtre opérateur-facing (vulgarisation, register, langue) en aval. Les sources restent reference-grade.

## Scope

S'applique à · `docs/system/*.md`, `docs/internal/*.md`, `SKILL.md`, `canon.md`, `lexicon.md` interne, descriptions schemas, `project-journal.md` narrative, entrées `CHANGELOG.md`, `README.md`, `CONTRIBUTING.md`.

Ne s'applique pas à · `CLAUDE.md` runtime (opérateur-facing, filtre pédagogique), outputs runtime skills (adapté selon language/register détectés), slash-commands user-facing.

## Posture

Ton reference-grade. Précision dense plutôt que clarté étendue. Lecteur supposé compétent et patient. Cherche l'information, n'a pas besoin qu'on lui tienne la main. Comparables · documentation Stripe API, RFC IETF, docs PostgreSQL, docs Anthropic internes.

## Registres canon

Trois registres applicables aux outputs PhantomOS, à distinguer explicitement ·

| Registre | Cible | Voice-doctrine applicable | Exemples |
|----------|-------|---------------------------|----------|
| Reference-grade | artefacts internes (skill-authors, contributeurs) | strict | `docs/system/`, `docs/internal/`, `SKILL.md`, `canon.md`, `lexicon.md` interne |
| Semi-public | surface repo (découvreurs projet, contributeurs externes) | base + allègements bornés (cf section exception) | `README.md`, `WELCOME.md`, `CONTRIBUTING.md` |
| Runtime opérateur | exécution skill, dialogue agent | non · `CLAUDE.md` runtime filtre en aval | outputs skills, slash commands user-facing |

## Principes canon

### P1 · Précision dense

Le terme canonique l'emporte sur la périphrase. Définir une fois dans le glossaire canon, cross-référencer ensuite. Pas de redéfinition à chaque occurrence. Acronymes utilisés sans redéveloppement systématique après première occurrence.

### P2 · Verbes d'action et noms techniques assumés

Le verbe d'action porte l'opérabilité (encoder, paramétrer, cartographier, composer). Le nom technique porte la précision (substrat, atome, axe variable, mutation gate). Les deux coexistent selon le contexte. Pas de périphrase descriptive en remplacement d'un terme canon.

### P3 · Phrases denses, courtes, sans liaisons molles

Chaque phrase porte une information distincte. Pas de "par ailleurs", "en effet", "il convient de noter", "à titre d'exemple". Transitions implicites par juxtaposition ou cross-ref typé. Phrases d'enchaînement narratif réservées au `project-journal.md`.

### P4 · Le terme canon avant l'explication

Nommer la chose en premier, qualifier ensuite si nécessaire. Pas d'introduction par périphrase qui retarde le mot juste.

Anti · "Une approche consistant à reconstituer des outputs à partir d'éléments structurés, qu'on appelle la composition canonique."
Canon · "Composition canonique · assemblage d'atomes encodés en output. S'oppose à la génération libre."

### P5 · Le lecteur senior est assumé

Pas de baisse de niveau préventive. Si le lecteur ne comprend pas un terme, il consulte le glossaire canon. Cross-refs canoniques explicites (chemin fichier ou ancre). Pas de "pour les non-initiés" ni d'encart pédagogique en milieu de doctrine.

Note de transparence · P4 spécialise P1 sur l'ordre syntaxique d'ouverture de phrase. Conservé distinct pour visibilité opérationnelle (cible un défaut d'écriture fréquent).

## Politique linguistique FR/EN

Canon doctrinal rédigé en français. Les schemas, JSON field names, paths, slugs, universal tech terms (brand, workspace, skill, agent, API, token, MCP, RAG) restent en anglais.

Décisions canon doublons FR/EN ·

| Forme canon | Forme dépréciée | Justification |
|-------------|-----------------|---------------|
| opérateur | operator, operateur | FR canon, accent inclus, registre métier |
| décomposition | decomposition | FR canon |
| cartographie | cartography | FR canon, "cartography" toléré en nom de doctrine (Compositional Cartography) |
| territoire | territory | FR canon en prose, "Territory Discipline" toléré en nom doctrine |
| doctrine | discipline | "doctrine" canon pour corps de principes, "discipline" réservé aux fichiers historiques en attente de rename, nouveau fichier doctrinal = `*-doctrine.md` |

Les noms de doctrines existantes restent en l'état. 21 fichiers `*-discipline.md` identifiés à renommer `*-doctrine.md` · sprint v2.85.0 dédié (cross-refs sibling doctrines + `CLAUDE.md` root + manifest skills à propager).

Acronymes canon développés une fois dans `canonical-glossary.md` à venir. Usage en doctrine sans redéveloppement. Exemples · ECR, MECE, CMR, DRGFP, NIVEAU 0-4/LIVE, NOYAU × CONTEXTE × MODIFIEURS.

## Conventions de casse

### Majuscules réservées (canon)

Réservées aux constructions architecturales fondatrices. Plafond strict · 5-10 termes total dans le système. Liste canon actuelle ·

- NOYAU, CONTEXTE, MODIFIEURS (formule compositionnelle v3.1)
- NIVEAU 0, NIVEAU 1-4, NIVEAU LIVE (decomposition visibility)

Toute proposition d'extension validée contre le plafond et justifiée par appartenance à une construction architecturale racine.

### Minuscules par défaut

Tout le reste, y compris les concepts canon (substrat, atome, encodage, composition, doctrine, etc.). Les noms propres de doctrines en titres suivent les conventions de titre standard (Contextual Intelligence, Schema Encoding Discipline).

## Conventions typographiques

Séparateurs canon · usage cohérent cross-artefacts ·

| Séparateur | Usage canon | Anti-usage |
|------------|-------------|------------|
| `·` (middle dot) | prose et listes inline (énumération, attributs courts) | dans tableaux markdown |
| `\|` | tableaux markdown uniquement | en prose |
| `→` | flèche de conséquence, dépendance, transition | comme séparateur générique |
| `↔` | paires bidirectionnelles (ex · cartographier ↔ paramétrer) | flèche unidirectionnelle |
| em-dash `·` | **interdit canon** (cf memory `no_em_dash`) | tout contexte |

## Famille terminologique paramétrage (canon v2.84.0)

Adoption canon d'une famille terminologique pour nommer précisément l'acte de composition et ses dimensions.

| Terme canon | Nature | Définition courte | Remplace / déprécié |
|-------------|--------|-------------------|---------------------|
| axe variable | substantif | dimension du système qui peut varier dans la composition (audience, angle, mécanique, format, ton) | "dimension", "levier", "variable" seule, "input" générique |
| paramétrage | substantif d'action | acte d'injecter des valeurs dans les axes variables du substrat pour produire un output | "configuration", "mobilisation", "alimentation" |
| paramétrer | verbe | exécuter le paramétrage | "configurer", "mobiliser", "alimenter" |

Pair conceptuel canon · cartographier (lire/structurer) ↔ paramétrer (injecter/composer). Les deux verbes structurent les deux moments fondamentaux du cycle PhantomOS.

Exemple canon · "Le skill `produce-paid-angles` paramètre 5 axes variables en NIVEAU 0 (audience, angle source, mécanique, format, ton), validés par l'opérateur, puis exécute la composition."

## Anti-patterns

- **AP-VD-1 · Périphrase pédagogique avant terme canon.** Anti · "Une approche qui consiste à... que l'on appelle X". Canon · "X · définition courte. Distinct de Y, Z".
- **AP-VD-2 · Liaisons molles narratives.** Anti · "Par ailleurs, il convient de noter que...". Canon · juxtaposition directe ou cross-ref typé.
- **AP-VD-3 · Validation politesse / sycophant.** Aucune formule d'ouverture en matière ("Excellente question", "Bien sûr", "Avec plaisir") dans les artefacts internes. Distinct d'AP-VD-8 qui cible les pronoms conversationnels (tu/vous).
- **AP-VD-4 · Adjectifs vagues d'enrichissement.** Éviter "important", "intéressant", "puissant", "robuste", "avancé" non-spécifiés. Si important, nommer pourquoi (impact, risque, fréquence). Sinon couper.
- **AP-VD-5 · Inflation marqueurs de priorité.** Au-delà de `claude-md-discipline` (rename pending v2.85.0+, 3 CRITICAL/YOU MUST max par fichier), aucune autre forme d'emphase visuelle (gras, italique, majuscules) pour appuyer une règle. Le ton sec porte l'autorité.
- **AP-VD-6 · Diffusion du jargon doctrinal en surface opérateur.** Noms de doctrines (Contextual Intelligence, CMR, ECR, MECE, DRGFP) ne sortent jamais en surface opérateur. Cf `contract-daily.md` "Operator-facing rule absolue".
- **AP-VD-7 · Redéveloppement systématique des acronymes.** Après première occurrence dans un fichier, l'acronyme est utilisé seul. Pas de "(Contextual Intelligence, CI)" à chaque mention.
- **AP-VD-8 · Mélange registre runtime opérateur dans artefacts internes.** Pas de "tu", "vous", "votre brand". Registre tiers, factuel, descriptif. Le tu/vous est réservé au runtime.

Note de transparence · AP-VD-1, AP-VD-2, AP-VD-7 sont des applications négatives directes de P3, P4, P1 (redondance assumée). Conservés visibles pour fonction de checklist d'écriture en post-write.

## Conditions d'invocation

Invoquer pour · création artefact interne (doctrine, schema, etc.) · refactor artefact existant · audit cohérence terminologique cross-files · sprint propagation post-décision canon.

Ne pas invoquer pour · outputs runtime opérateur-facing (autre registre) · `WELCOME.md`, `README.md` (registre semi-public · cf section suivante).

## Exception README / WELCOME (registre semi-public)

Détaille les allègements du registre semi-public (cf section Registres canon). Allègements permis · phrases narratives pour introduire le projet · acronymes développés à chaque première occurrence (vs artefacts internes) · cross-refs vers ressources canon publiques mais pas vers doctrines internes.

Reste strictement applicable · vocabulaire canon (opérateur, substrat, paramétrer), pas de validation politesse / sycophant, pas d'adjectifs vagues d'enrichissement.

## Versioning et amendement

Semver strict · patch (clarification, exemple, AP complémentaire) · minor (nouveau principe, nouvelle décision canon FR/EN) · major (refonte structurelle, dépréciation). Pré-amendement obligatoire · test de suppression (cf `claude-md-discipline`) appliqué aux principes existants.

## Cross-refs

`claude-md-doctrine.md` v2.82.0 (cap, marqueurs, test de suppression · rename pending v2.85.0+) · `changelog-doctrine.md` v2.83.0 (Keep-a-Changelog · rename pending v2.85.0+) · `output-clarity-doctrine.md` v2.79.2 (rendu opérateur-facing, couche runtime aval · rename pending v2.85.0+) · `compositional-cartography.md` v3.1 (NOYAU × CONTEXTE × MODIFIEURS) · `decomposition-visibility-doctrine.md` v2.81.1+ (NIVEAUX 0/1-4/LIVE casse · rename pending v2.85.0+) · `contract-daily.md` (Operator-facing rule absolue · AP-VD-6).
