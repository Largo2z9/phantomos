---
name: evaluate-concept
type: curator
version: "1.0.0"
recommended_model: opus # jugement multi-checks adversarial · au-dessus du default curator
layer: meta
reasoning_pattern: null
operator_facing: false
invocable_by:
  - compose-creative
  - "*"
description: >
  Gate A6 du workflow créa-strat. Juge la SOLIDITÉ STRATÉGIQUE d'un ou plusieurs
  concepts candidats AVANT toute production (génération, compositing, brief humain).
  Applique les 5 checks canon du pre-gate-evaluator : anti-générique (test de
  substitution), ancrage atlas (lineage traçable, jamais halluciné), distance
  consciente (curseur sectoriel D#480), faisabilité production (routing capacités
  existantes), cohérence charte. Retourne un verdict structuré par concept
  (approved / rejected / surface_pending) + un rendu opérateur sobre. Ne mute
  JAMAIS le workspace : le verdict revient au caller (le FLUX orchestrant la
  chaîne, qui invoque ce gate après la production des concepts candidats par
  produce-paid-angles), et le flux persiste chaque verdict dans
  brands/{slug}/creatives/{batch}/concepts/CPT-NN.json champ evaluation.
  weave-hooks ne l'invoque pas, il exige des concepts déjà gatés. Budget
  anti-spin 3 itérations max, au-delà escalade business explicite.
  FR: "évalue les concepts", "ces concepts tiennent ?", "gate concepts", "valide les concepts avant prod".
  EN: "evaluate concepts", "concept gate", "are these concepts solid".
permissions:
  reads: [brand, product, profile, angle, creative]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: concepts candidats formulés (premise + angle_ref) dans brands/{slug}/creatives/{batch}/concepts/CPT-NN.json par le flux amont (produce-paid-angles en run cadré), frame.json du run présent avec regime.mode + rayon_max persistés, atlas brand encodé (angles + pain_points navigables).
  postconditions: verdict structuré retourné au caller pour chaque concept, paris cross-verticale relayés à l'opérateur par le caller, verdicts persistés PAR LE CALLER (le flux) dans brands/{slug}/creatives/{batch}/concepts/CPT-NN.json#evaluation (approval_status, checks, iteration_count) via write_to_context.
consumes:
  - path: docs/system/pre-gate-evaluator-doctrine.md
    min_version: 1.0.0
  - path: resources/schemas/angle.schema.json
    min_version: 1.3.0
  - path: resources/sops/creative-production/cross-brand-curation.md
    note: "fonction de distance d'emprunt unique (Check 3)"
produces_proposals_for:
  - brands/{slug}/creatives/{batch}/concepts/CPT-NN.json#evaluation (persisté par le caller, jamais par ce skill)
disambiguates_against:
  qc-creative: "qc-creative juge le RENDU visuel d'un binaire produit (vision read, fidélité produit, typo, compliance) · evaluate-concept juge la SOLIDITÉ STRATÉGIQUE d'un concept AVANT toute production. Concept écrit sans pixel → ici. Binaire rendu → qc-creative."
  score-matrix: "score-matrix priorise des territoires (ranking comparatif, scoring pondéré) · evaluate-concept rend un verdict binaire par concept candidat (passe ou ne passe pas, raison nommée). Prioriser → score-matrix. Gater → ici."
---

> Brique gate A6. Deuxième verrou de la chaîne créa-strat : `frame-regime` garde la STRATÉGIE en amont, ce skill garde le CONCEPT au milieu, `qc-creative` garde le RENDU en aval. Une créa générique coûte le budget paid qui la porte et pollue le signal du compte. Rien ne part en production sans gate vert ou pari assumé tracé. Doctrine fondatrice : `docs/system/pre-gate-evaluator-doctrine.md`.

## Tone

Structured machine output vers le caller : JSON, pas de prose. Le rendu opérateur est sobre, langage métier uniquement : un concept approuvé est nommé avec sa force, un rejeté avec sa raison actionnable, un pari avec son risque. Jamais de noms de checks internes, jamais de field paths, jamais de distance numérique brute côté opérateur. Iconographie limitée à ✓ ✗ ⚠ dans le rendu verdict.

---

# Skill: evaluate-concept (gate concepts avant production)

Le gate répond à une seule question par concept candidat : est-ce que ce concept mérite qu'on dépense de la production et du budget paid dessus ? Cinq checks, chacun avec un verdict propre (APPROVE / REJECT / SURFACE), agrégés en un statut par concept. Le check fondateur est le test de substitution (Check 1) : il est non négociable, prouvé par le moteur (juge contextuel 8,2/10 sur corpus cross-brand).

Ce skill ne produit rien, ne réécrit rien, ne sauve aucun concept en le reformulant. Il juge ce qu'on lui soumet et nomme pourquoi. La correction appartient au flux amont, la persistance au caller.

---

## Input contract

Le caller MUST fournir :

- `concepts[]` · les candidats à gater. Chaque concept porte : `concept_id`, la premise (1 à 3 phrases, l'idée centrale), `angle_ref` (lignage ANG-NN revendiqué), la verticale d'emprunt si le concept vient d'ailleurs, la liste des assets requis pour l'exécuter (image, compositing, vidéo, brief humain).
- `brand_slug` · la marque jugée (charge brand.json, visual_identity, atlas angles + pains).
- `audience_slug` · l'audience cible (charge profile.json, dont `psychology.big_idea`).
- `frame_path` · le frame.json du run créa-strat (charge `rayon_max` top-level persisté + `regime.mode` pour le Check 3 · `freedom_cursor` est un number 0-1, jamais un enum, et ne sert pas à re-dériver le rayon).
- `iteration_count` · 0 au premier passage, incrémenté par le caller à chaque re-soumission après feedback opérateur.

Si un concept arrive sans `angle_ref` ni premise exploitable, le gate le retourne `rejected` motif "concept non formé, rien à juger" sans brûler une itération sur les autres.

---

## Execution steps

### Step 1 · Charger le référentiel (ce contre quoi on juge)

Read :
- `brands/{slug}/brand.json` · positioning, tone_of_voice, verticale de la marque, concurrents directs nommés (le test de substitution a besoin d'un concurrent réel, pas d'un concurrent inventé).
- `brands/{slug}/products/{product_slug}/spec.json#visual_identity` · palette, mood, assets canoniques (Check 5 + Check 4).
- `brands/{slug}/audiences/{audience_slug}/profile.json` · `psychology.big_idea` (Check 1, cohérence), pains et desires encodés.
- `brands/{slug}/angles/{ANG-NN}.json` pour chaque `angle_ref` revendiqué · `lineage.pain_ref`, `lineage.pain_extract`, verbatim anchors (Check 2, traçabilité).
- `{frame_path}` · `rayon_max` top-level (persisté par frame-regime, JAMAIS re-dérivé localement) + `regime.mode` (enum exploit | balanced | explore) pour le Check 3.
- `brands/{slug}/creatives/{batch}/concepts/CPT-NN.json#evaluation` des concepts déjà gatés ce run · compteur d'itérations et verdicts antérieurs.

Lecture silencieuse, jamais narrée. Si une pièce manque (pas de big_idea encodée, pas de rayon_max), le check concerné dégrade explicitement : il rend son verdict avec `reason` qui nomme la donnée manquante, jamais un APPROVE silencieux par défaut.

### Step 2 · Check 1 · Anti-générique (test de substitution, LE check fondateur)

**Définition.** Un concept générique est un concept qui marcherait tel quel chez le concurrent direct. Il n'achète aucune position, il loue de l'attention au prix fort. C'est le défaut numéro un des concepts produits par LLM : plausibles, propres, interchangeables.

**Méthode.** Deux tests, les deux doivent passer :

1. *Substitution* · remplacer mentalement la marque par son concurrent direct le plus proche (lu dans brand.json, jamais inventé). L'ad se casse-t-elle ? Si le concept tient encore debout chez le concurrent sans rien changer, il est générique. Exemple canon : "I got my mornings back" porté par une grand-mère relationnelle casse chez Dr Scholl (marque clinique, le registre intime ne colle pas) → le concept PASSE. "Pain relief for feet" tient partout → générique, REJECT.
2. *Complétion audience* · l'audience finit-elle la phrase naturellement ? Un concept ancré déclenche la suite dans la tête du lecteur cible (le verbatim résonne, le contexte est le sien). Un concept générique se lit sans accroche.

**Cohérence big_idea.** Vérifier le concept contre `psychology.big_idea` de l'audience. Un concept qui CONTREDIT la big_idea encodée est flaggé SURFACE, jamais rejeté silencieusement ni approuvé en faisant comme si : *"ton concept contredit la big idea encodée · override ou rejet ?"*. L'intuition fondateur est injectée ET challengée dans les deux sens : si UN concept contredit la big_idea, c'est probablement le concept le problème · si TOUS les concepts du batch la contredisent, le signal remonte à l'opérateur : *"ta big idea est peut-être décrochée de la marque réelle, c'est elle qu'il faut re-regarder, pas les concepts"*.

**Verdict.** Substitution cassée + complétion naturelle → APPROVE. Concept interchangeable → REJECT, motif nommé (qu'est-ce qui le rend substituable : pas de marqueur de marque, pas de contexte audience, claim catégorie). Contradiction big_idea → SURFACE (arbitrage opérateur : override tracé ou rejet).

### Step 3 · Check 2 · Ancrage atlas (jamais halluciné)

**Définition.** Un concept doit sourcer d'un verbatim, d'un pain ou d'un desire RÉEL de l'atlas brand. Le lignage `angle_ref → lineage.pain_ref` doit être traçable jusqu'à la matière encodée. Un concept créé ex-nihilo, aussi séduisant soit-il, est de la fiction stratégique : il n'a aucune raison documentée de résonner.

**Méthode.** Suivre le lignage revendiqué : le `angle_ref` du concept existe-t-il dans `angles/` ? Son `lineage.pain_ref` (ou `pain_extract` legacy) pointe-t-il vers un pain encodé avec verbatims ? La premise du concept exploite-t-elle réellement ce pain, ou le lignage est-il décoratif (un ANG-NN collé sur un concept qui parle d'autre chose) ? Le lignage décoratif compte comme absence de lignage.

**Verdict.** Lignage traçable et exploité → APPROVE (le verdict porte `angle_ref` + `pain_source` pour que le caller persiste la chaîne). Création ex-nihilo introuvable dans l'atlas, ou lignage décoratif → REJECT, motif : *"concept sans source dans la matière client encodée"*. Pas de SURFACE sur ce check, et PAS d'override direct non plus (Hard Rule) : la porte de sortie native, c'est d'ENCODER la matière manquante dans l'atlas (le pain, le verbatim, le desire que l'opérateur affirme tenir) puis de RE-SOUMETTRE le concept. Le gate ne croit pas sur parole, il croit la matière encodée.

### Step 4 · Check 3 · Distance consciente (curseur sectoriel D#480)

**Définition.** Emprunter un pattern à une autre verticale est une arme (c'est souvent là que sont les breakthroughs), à condition que l'emprunt soit CONSCIENT : mesuré, autorisé par le rayon du run, et assumé comme pari devant l'opérateur. L'emprunt silencieux est interdit, pas l'emprunt.

**Méthode.** Distance d'emprunt UNIQUE, définie dans `resources/sops/creative-production/cross-brand-curation.md` :

```
distance(concept, marque) = 0  si verticale de la marque ∈ vertical_scope.origins du pattern
                               OU (vertical_scope.breadth == "universal"
                                   ET promote_status == "promote-ready")
                            1  si une origin est verticale VOISINE de la marque
                            2  sinon
```

Le `rayon_max` est lu dans le frame.json du run, champ TOP-LEVEL persisté par frame-regime (0 exploit · 1 balanced · 2 explore, l'enum vit dans `regime.mode`). Jamais re-dérivé localement, jamais supposé. Un pattern universal ET promote-ready compte distance 0 : la preuve a déjà été payée ailleurs.

**Verdict.**
- `distance == 0` → APPROVE, rien à surfacer.
- `0 < distance <= rayon` → APPROVE + SURFACE OBLIGATOIRE. La `surface_note` nomme le pari en langage métier : *"concept emprunté à la verticale X, pari assumé : voilà pourquoi ça devrait transférer ici, voilà le risque si ça ne transfère pas"*. Jamais d'emprunt silencieux, même autorisé.
- `distance > rayon` → REJECT sauf override opérateur tracé. Le motif nomme l'écart : le régime du run (regime.mode) est en exploit, ce concept demande explore. L'opérateur peut élargir le rayon (décision de frame, remonte au flux : re-cadrage, jamais re-dérivé ici) ou overrider ce concept précis (tracé dans le verdict).

### Step 5 · Check 4 · Faisabilité production (routing, pas rejet aveugle)

**Définition.** Un concept approuvé qui ne peut pas être produit est une dette. Le check vérifie que les assets requis se routent sur des capacités EXISTANTES du workspace : génération image, compositing layered avec asset canonique (packshot, logo collés, jamais re-générés sur fidélité critique), export brief humain (Route B).

**Méthode.** Pour chaque asset requis par le concept, mapper vers une capacité câblée. Trois sorties possibles par asset : produisible en interne, produisible via brief humain Route B, non câblé.

**Verdict.** Ce check REJECT rarement : il route. Un concept qui exige un rendu vidéo complet n'est pas rejeté aveuglément (le concept peut être excellent), il est marqué `route_implication: "Route B export ou différé"` : le bras vidéo n'est pas câblé, le concept part en brief humain ou attend. REJECT uniquement si AUCUNE route n'existe (ni production interne, ni Route B, ni différé ne couvrent le besoin), cas rare à motiver précisément.

### Step 6 · Check 5 · Cohérence charte (adapter, pas coller en force)

**Définition.** Le concept doit s'ADAPTER à la charte de la marque (`visual_identity` : palette, ton, mood), pas s'y coller en force. Un concept qui exige de casser la charte pour exister importera son incohérence dans chaque déclinaison.

**Méthode.** Confronter ce que le concept exige visuellement et tonalement à la `visual_identity` et au `tone_of_voice`. Trois cas : le concept vit naturellement dans la charte (adapté) · le concept demande une flexion que la charte absorbe (adapté, noter la flexion) · le concept exige un registre que la charte interdit frontalement (conflit direct).

**Verdict.** Adapté (y compris avec flexion absorbable) → APPROVE. Conflit direct → REJECT sauf override opérateur (il peut décider que la charte évolue, mais c'est SA décision, tracée, pas celle du gate).

### Step 7 · Agréger le verdict par concept

Règle d'agrégation, dans l'ordre :

1. Un REJECT non overridé sur n'importe quel check → `approval_status: rejected`, `rejection_reason` = la raison du check le plus en amont qui rejette (l'ordre des checks EST l'ordre de priorité : un concept générique n'a pas besoin qu'on évalue sa charte).
2. Zéro REJECT mais un SURFACE en attente d'arbitrage (pari cross-verticale, contradiction big_idea) → `approval_status: surface_pending`. Le concept n'est PAS approuvé tant que l'opérateur n'a pas arbitré.
3. Cinq checks APPROVE, zéro SURFACE pendant → `approval_status: approved`.

Un override opérateur tracé (raison fournie, posé dans le tour de feedback) convertit le REJECT ou le SURFACE concerné en APPROVE sur les Checks 3 à 5 UNIQUEMENT, et apparaît dans le verdict : l'override ne fait jamais disparaître le check, il le documente. Les Checks 1 et 2 ne s'overrident jamais : substitution échouée = rejet sec, ancrage manquant = encoder la matière dans l'atlas puis re-soumettre.

### Step 8 · Budget anti-spin (3 itérations, puis on arrête de tourner)

Le cycle verdict → feedback opérateur → re-évaluation est plafonné à 3 itérations par batch de concepts. Le `iteration_count` est fourni par le caller et retourné dans chaque verdict.

À `iteration_count == 3` avec encore des rejets : ce n'est plus un problème d'évaluation, c'est un blocage business. Le gate escalade explicitement au lieu de re-juger : *"trois passages, les concepts butent toujours sur {le check dominant}. Le problème n'est plus dans les concepts, il est en amont : {la big_idea, le curseur du frame, la matière atlas trop fine}. On arrête de tourner et on traite ça."* Aucune quatrième évaluation, même demandée poliment.

Variante cosmétique d'un concept déjà rejeté (même premise reformulée, même lignage, même pari) re-soumise telle quelle : compte comme itération, signalée comme cosmétique dans le verdict.

### Step 9 · Rendu opérateur (sobre, langage métier)

Après le JSON caller, produire le rendu opérateur. Trois blocs, uniquement ceux qui sont non vides :

- **Approuvés** · chaque concept avec sa force en une phrase (ce qui le rend défendable : l'ancrage, le marqueur de marque, le pattern prouvé). ✓
- **Rejetés** · chaque concept avec sa raison en langage métier, actionnable : *"interchangeable, marcherait mot pour mot chez {concurrent}"*, *"aucune source dans ce que tes clients disent réellement"*, *"demande un registre que ta charte interdit"*. ✗
- **Paris à arbitrer** · chaque SURFACE avec le pari nommé (d'où vient l'emprunt, pourquoi ça devrait transférer, le risque) et la question d'arbitrage. ⚠

Interdits dans ce rendu : noms de checks internes, field paths, valeurs `distance`/`rayon` numériques brutes (dire *"emprunté à une verticale voisine"*, pas *"distance 1, rayon 1"*), noms de skills, statuts JSON.

Le rendu se termine TOUJOURS par un next-step contextuel unique, fonction du verdict : s'il reste des paris pendants, c'est l'arbitrage (*"le pari {X} : tu l'assumes et les 3 partent en prod, ou on le coupe et on part à 2 ?"*) · si tout est approuvé, c'est le passage en production · si tout est rejeté à l'itération 3, c'est l'escalade amont nommée. Jamais "Done. Want anything else?".

Ce rendu est RETOURNÉ AU CALLER avec le JSON : c'est le caller (le flux orchestrant la chaîne) qui le relaie à l'opérateur et qui porte la question d'arbitrage. Ce skill ne dialogue jamais directement avec l'opérateur (cohérent avec operator_facing: false + subagent_safe: true).

---

## Output

Verdict structuré retourné au caller, un objet par concept :

```json
{
  "concept_id": "CPT-03",
  "checks": {
    "anti_generic": {
      "passed": true,
      "reason": "substitution cassée chez {concurrent} (registre relationnel vs clinique), complétion audience naturelle sur le verbatim morning"
    },
    "atlas_anchored": {
      "passed": true,
      "angle_ref": "ANG-04",
      "pain_source": "PNT-02"
    },
    "distance_conscious": {
      "passed": true,
      "distance": 1,
      "rayon": 1,
      "surface_note": "pattern emprunté verticale telehealth · transfère car même mécanique de honte sociale · risque : registre US à re-naturaliser FR"
    },
    "production_feasible": {
      "passed": true,
      "route_implication": "compositing layered avec packshot canonique, produisible interne"
    },
    "charter_coherent": {
      "passed": true,
      "reason": "mood intime compatible palette + ton encodés, flexion mineure sur la typo absorbée"
    }
  },
  "approval_status": "surface_pending",
  "rejection_reason": null,
  "iteration_count": 1
}
```

Conventions :
- `approval_status` ∈ `approved | rejected | surface_pending`.
- `rejection_reason` présent uniquement si `rejected` : une phrase, nommée, actionnable, en langage métier (elle est réutilisée telle quelle dans le rendu opérateur).
- `surface_note` rempli dès qu'un emprunt cross-verticale ou une contradiction big_idea existe, même sur concept approuvé après arbitrage (le pari reste documenté).
- Un override opérateur apparaît dans le `reason` du check concerné : `"REJECT converti par override opérateur · {raison fournie}"`.

**Le caller persiste, jamais ce skill.** Le caller est le FLUX (l'agent orchestrant la chaîne), qui invoque ce gate après la production des concepts candidats par `produce-paid-angles`. Il persiste le verdict de CHAQUE concept (approved, rejected ou surface_pending) dans `brands/{slug}/creatives/{batch}/concepts/CPT-NN.json#evaluation` (approval_status, checks, iteration_count, ...) via write_to_context. `weave-hooks` n'invoque PAS ce skill : il exige en précondition des concepts déjà gatés (au moins 1 CPT avec `evaluation.approval_status: approved`). Ce skill retourne le verdict et s'arrête là, pattern identique à `qc-creative`.

---

## Example · rendu opérateur (batch 4 concepts, itération 1)

Ce que l'opérateur voit après que le flux a soumis 4 concepts sur une marque foot-care :

---

Sur tes 4 concepts, 2 tiennent, 1 tombe, 1 est un pari à arbitrer.

✓ **Matins récupérés** · le plus solide du lot. Ancré sur ce que tes clientes disent vraiment (le verbatim "I got my mornings back" revient en boucle dans les avis), et il ne marcherait chez aucun concurrent : leur registre est clinique, le tien est relationnel. C'est un marqueur de marque, pas un claim de catégorie.

✓ **La chaussure du dimanche** · ancré sur la douleur des occasions ratées, vit naturellement dans ta charte. Moins puissant que le premier mais distinct, bon second de vague.

✗ **Soulagement immédiat** · rejeté : interchangeable. Colle le logo de Dr Scholl dessus, l'ad fonctionne pareil. Il ne dit rien que la catégorie entière ne dit déjà. Pour repasser, il faudrait l'ancrer sur un moment précis de tes clientes, pas sur la promesse générique.

⚠ **Le secret qu'on ne dit pas au podologue** · pari. Le pattern vient du telehealth US (la mécanique de honte sociale autour d'un sujet tabou), il devrait transférer parce que tes verbatims portent exactement cette gêne, le risque c'est le registre confession très US à re-naturaliser en français. Ton curseur de run l'autorise.

Le pari confession : tu l'assumes et les 3 partent en prod ensemble, ou on le coupe et on part à 2 sûrs ?

---

Notes sur ce rendu : aucune mention de check, de distance chiffrée, de statut JSON ou de skill. La raison du rejet contient le chemin de repassage. Le close est l'arbitrage pendant, pas un menu.

---

## Hard Rules

- **Never approuver un concept qui échoue au test de substitution.** C'est LE check fondateur, prouvé par le moteur (juge contextuel 8,2/10). Un concept interchangeable avec le concurrent direct ne passe jamais, quel que soit son score sur les quatre autres checks, quelle que soit l'envie de l'opérateur. Override impossible sur ce check précis.
- **Never approuver par override un concept qui échoue à l'ancrage atlas (Check 2).** Deux verrous absolus dans ce gate : la substitution (Check 1, rien d'autre à faire que rejeter) et l'ancrage (Check 2, résoluble UNIQUEMENT en encodant la matière manquante dans l'atlas puis en re-soumettant le concept, jamais par override direct). Les Checks 3 à 5 restent overridables, tracés.
- **Always surfacer un emprunt cross-verticale, jamais silencieux.** Toute distance > 0 produit une `surface_note` nommant le pari (pourquoi ça transfère, le risque), même quand le curseur l'autorise largement. Un pari non surfacé est un mensonge par omission au moment du post-mortem.
- **Never plus de 3 itérations.** Au-delà, escalade business explicite (Step 8). Le gate ne devient jamais une machine à tourner en rond, et ne re-juge pas une quatrième fois même sur demande.
- **Always retourner le verdict structuré au caller, jamais écrire soi-même dans le workspace.** Zéro mutation depuis ce skill : pas de write_to_context, pas d'Edit, rien. Le caller persiste les approuvés. Un gate qui écrit est un gate qu'on ne peut plus appeler en subagent sans risque.
- **Never traduire un REJECT en langage vague.** "Pas assez fort", "à retravailler", "manque de punch" sont interdits. La raison est nommée et actionnable : quel check, quel écart, quoi changer pour repasser.

---

## Cross-references

- `docs/system/pre-gate-evaluator-doctrine.md` · doctrine fondatrice : pourquoi un gate concepts avant production, les invariants des 5 checks, HR-PGE-1 à 5
- `.skills/skills/qc-creative/SKILL.md` · gate aval frère (juge le RENDU binaire, pattern read-only + verdict caller identique)
- `.skills/skills/produce-paid-angles/SKILL.md` · producteur amont des concepts candidats (`brands/{slug}/creatives/{batch}/concepts/CPT-NN.json`, run cadré) · le flux invoque ce gate juste après
- `.skills/skills/weave-hooks/SKILL.md` · consommateur aval (PAS un caller) : exige des concepts déjà gatés (`evaluation.approval_status: approved`) avant d'incarner
- `resources/sops/creative-production/cross-brand-curation.md` · fonction de distance d'emprunt unique (Check 3)
- `resources/schemas/angle.schema.json` v1.3 · lignage `lineage.pain_ref` / `pain_extract` que le Check 2 remonte
- `brands/{slug}/audiences/{audience_slug}/profile.json#psychology.big_idea` · référentiel du Check 1 (cohérence)
- frame.json du run créa-strat · `rayon_max` top-level persisté + `regime.mode` (Check 3)
- `brands/{slug}/creatives/{batch}/concepts/CPT-NN.json#evaluation` · réceptacle des verdicts, écrit par le caller (le flux), jamais par ce skill
- `.skills/write-to-context.py` · canal de mutation canonique utilisé par le CALLER pour persister (ce skill ne mute pas)
- D#472, D#473, D#480 (curseur sectoriel), D#499 · décisions R&D sources du design
