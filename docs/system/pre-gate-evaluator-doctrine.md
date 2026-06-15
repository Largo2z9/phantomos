# Pre-Gate Evaluator · Operating Doctrine

> Canonique v2.90+. Annoncée à l'entrée CHANGELOG v2.88.0 (planifiée pour le sprint v2.88.1, jamais shippée jusqu'à v2.90.0) : cette version la grave. Doctrine canon du gate concepts (A6 du workflow créa-strat). Pose le POURQUOI et les invariants des 5 checks · le détail opérationnel (méthodes, verdicts, output contract) vit dans `.skills/skills/evaluate-concept/SKILL.md`. Doctrine sœur de `output-clarity-doctrine.md` (registre des rendus opérateur), `investigation-posture.md` (confidence et arbitrage), et du contrat de gate aval porté par `qc-creative`. Ferme le gap *"les concepts partent en production sur intuition, le premier verdict tombe après le spend"*.

---

## 1. Thèse fondatrice

> Une créa ratée ne coûte pas son temps de production. Elle coûte le budget paid qui l'a portée, le signal pollué qu'elle laisse dans l'ad account, et le cycle d'apprentissage gaspillé sur une hypothèse qui n'aurait jamais dû être testée. Le moment le moins cher pour tuer un mauvais concept est AVANT le premier pixel.

**Définition canon pre-gate evaluator** · verrou stratégique placé entre l'idéation (concepts candidats formulés) et la production (génération, compositing, brief humain). Il juge la solidité d'un concept sur 5 checks orthogonaux et rend un verdict tranché par concept (approuvé / rejeté / pari en arbitrage), avec pari surfacé quand le concept est un emprunt assumé. Un concept qui passe ce gate a une raison documentée d'exister : il est distinctif, sourcé, calibré en risque, produisible, cohérent.

L'asymétrie économique qui justifie le gate : évaluer un concept coûte des secondes de raisonnement · produire une créa coûte des minutes à des heures · tester une créa coûte des centaines d'euros de paid et une semaine de data · et une créa générique testée pollue le signal du compte au-delà de son propre budget (l'algorithme apprend sur du bruit). Chaque cran vers l'aval multiplie le coût de l'erreur. Le gate déplace la mortalité des concepts vers le cran le moins cher.

---

## 2. Le problème résolu

Sans pre-gate evaluator canon :

1. **Le premier verdict tombe après le spend.** Le seul gate existant en aval (`qc-creative`) juge le rendu, pas l'idée. Un concept générique parfaitement exécuté passe le QC visuel haut la main et meurt en campagne. Le système apprenait la mauvaise leçon : "l'exécution était bonne", alors que l'idée était morte d'avance.

2. **Génériques plausibles en série.** Le défaut structurel des concepts produits par LLM n'est pas la faute de goût, c'est l'interchangeabilité : des concepts propres, fluides, qui marcheraient mot pour mot chez le concurrent. Sans test de substitution systématique, ils passent, parce qu'ils ne choquent personne.

3. **Lignage décoratif.** Un concept halluciné avec un ANG-NN collé dessus a l'apparence de la traçabilité. Sans vérification du lignage jusqu'au pain encodé, l'atlas devient un alibi au lieu d'une source.

4. **Emprunts silencieux.** Les patterns cross-verticale sont la meilleure source de breakthroughs ET la première source de flops inexplicables. Sans mesure de distance et sans surfaçage du pari, impossible de distinguer au post-mortem un pattern qui ne transfère pas d'une exécution ratée.

5. **Spin infini.** Sans budget d'itérations, le cycle verdict → retouche → re-verdict tourne indéfiniment sur des variantes cosmétiques, en masquant le vrai problème (big_idea décrochée, curseur mal posé, atlas trop fin) derrière une activité d'évaluation.

---

## 3. Les 5 checks · référence canonique

Le détail opérationnel (méthode pas à pas, conditions de verdict, exemples) vit dans la skill. La doctrine grave le POURQUOI et l'invariant de chacun.

### Check 1 · Anti-générique (test de substitution)

**Pourquoi.** La distinctivité est la seule chose qu'une créa achète durablement : tout le reste se loue. Le test de substitution (remplacer la marque par son concurrent direct : l'ad se casse-t-elle ?) est le détecteur le plus fiable connu du moteur, prouvé en juge contextuel à 8,2/10 sur corpus cross-brand. Le second volet (l'audience finit-elle la phrase ?) vérifie que la distinctivité est ancrée côté lecteur, pas seulement côté marque.

**Invariant.** Ce check est non négociable et non overridable. Un concept qui échoue à la substitution ne passe jamais, quels que soient les quatre autres checks. La cohérence avec la big_idea encodée fait partie du check, dans les deux sens : un concept qui la contredit est arbitré (pas rejeté en silence), et un batch entier qui la contredit retourne le soupçon contre la big_idea elle-même.

### Check 2 · Ancrage atlas

**Pourquoi.** Un concept sans source dans la matière client réelle (verbatim, pain, desire encodés) est une fiction stratégique : il peut être brillant, il n'a aucune raison documentée de résonner. L'atlas existe précisément pour que la créa parte de ce que les clients disent, pas de ce que le modèle imagine qu'ils disent.

**Invariant.** Le lignage doit être traçable ET exploité (`angle_ref → pain_ref → matière encodée`). Le lignage décoratif vaut absence de lignage. Création ex-nihilo = rejet, non-overridable par override direct : aucun override ne fait passer un concept non ancré. MAIS ce verrou a une porte de sortie native : encoder la matière manquante dans l'atlas (le pain, le verbatim ou le desire que l'opérateur affirme) puis re-soumettre le concept. Le check se résout UNIQUEMENT en encodant puis re-soumettant, jamais par override.

### Check 3 · Distance consciente (curseur sectoriel, D#480)

**Pourquoi.** Interdire l'emprunt cross-verticale tuerait les breakthroughs · l'autoriser sans cadre produit des flops illisibles. La réponse canon n'est ni l'un ni l'autre : c'est l'emprunt CONSCIENT. La distance se mesure selon la fonction canon de `resources/sops/creative-production/cross-brand-curation.md` (0 même verticale, ou breadth `universal` + promote_status `promote-ready` · 1 verticale voisine · 2 au-delà), le rayon autorisé se décide en amont dans le frame (exploit 0 · balanced 1 · explore 2), et tout emprunt dans le rayon est approuvé MAIS surfacé comme pari nommé.

**Invariant.** Le risque est une décision d'opérateur, jamais une initiative silencieuse d'agent. Distance dans le rayon = pari surfacé obligatoire (pourquoi ça transfère, le risque). Distance hors rayon = rejet sauf override tracé. Le rayon se lit dans `frame.json#rayon_max` persisté (jamais re-dérivé) et l'enum de régime dans `frame.json#regime.mode`, jamais ne se suppose (`freedom_cursor` est un number 0-1, jamais l'enum).

### Check 4 · Faisabilité production

**Pourquoi.** Un concept approuvé improduisible est une dette : il encombre le pipeline et finit exécuté en dégradé, ce qui invalide le test. Mais la faisabilité est un problème de ROUTING, pas de censure : un concept excellent qui exige une capacité non câblée (rendu vidéo complet) mérite la Route B (brief humain) ou le différé, pas la poubelle.

**Invariant.** Ce check route d'abord, rejette en dernier recours. Il rejette uniquement quand aucune route n'existe. Il ne juge jamais la qualité de l'idée, seulement son chemin d'exécution.

### Check 5 · Cohérence charte

**Pourquoi.** Un concept qui se colle en force contre la charte (palette, ton, mood) importe son incohérence dans chaque déclinaison et brûle de la distinctivité de marque pour gagner une créa. L'adaptation est saine (la charte absorbe des flexions) · le conflit frontal ne l'est pas.

**Invariant.** Adapté passe, conflit direct rejette. L'évolution de la charte reste possible mais c'est une décision d'opérateur, tracée comme override : le gate ne décide jamais que la marque change.

---

## 4. Budget anti-spin · la frontière algo / business

Le cycle verdict → feedback → re-évaluation est plafonné à **3 itérations** par batch. Ce plafond n'est pas une limite de patience, c'est une frontière de diagnostic.

Jusqu'à 3 passages, l'hypothèse de travail est : les concepts sont perfectibles, le gate aide à les durcir. Au-delà de 3, l'hypothèse s'inverse : si les concepts butent encore, le problème n'est plus DANS les concepts, il est en amont. Trois racines typiques : la big_idea encodée est décrochée de la marque réelle · le curseur de liberté du frame est mal posé pour l'objectif du run · l'atlas est trop fin pour nourrir des concepts ancrés. Aucune de ces racines ne se répare en re-jugeant des concepts : ce sont des décisions business ou des chantiers de matière.

L'invariant : à la frontière, le gate ESCALADE au lieu de tourner. Il nomme le check dominant des rejets et la racine amont probable, et s'arrête. Continuer à itérer au-delà serait de l'activité qui masque un blocage, le pire des deux mondes : ni verdict utile, ni problème traité.

---

## 5. Trois gates orthogonaux · stratégie → concept → rendu

Le pre-gate evaluator est le deuxième verrou d'une chaîne de trois, chacun jugeant un objet différent :

| Gate | Position | Objet jugé | Question |
|---|---|---|---|
| frame-regime | amont | la STRATÉGIE du run | ce frame (audience, curseur, objectif) est-il le bon combat ? |
| pre-gate evaluator (`evaluate-concept`) | milieu | le CONCEPT candidat | cette idée mérite-t-elle production et budget ? |
| `qc-creative` | aval | le RENDU binaire | cet asset exécute-t-il fidèlement, sans défaut, prêt au spend ? |

Orthogonalité stricte : un vert à un étage n'implique JAMAIS le vert à l'étage suivant. Un frame impeccable produit des concepts génériques · un concept brillant se rend en binaire défectueux · et symétriquement, un QC visuel parfait ne rachète jamais un concept mort. Chaque gate juge son objet et seulement lui : le pre-gate ne regarde aucun pixel, le QC ne re-juge aucune stratégie. C'est cette séparation qui rend les post-mortems lisibles : quand une créa meurt en campagne, on sait quel étage a menti.

---

## 6. Hard Rules canon (HR-PGE-1 à HR-PGE-5)

### HR-PGE-1 · Aucun concept en production sans gate vert ou override tracé

Tout concept qui entre en production (génération, compositing, brief Route B) porte soit un verdict `approved` du gate, soit un override opérateur tracé avec raison. La production d'un concept non gaté = bug pipeline. L'override documente le check contourné, il ne le fait jamais disparaître.

### HR-PGE-2 · Deux verrous absolus : substitution et ancrage

Le système porte deux verrous non-overridables. Le Check 1 (substitution + complétion audience), check fondateur prouvé moteur (juge contextuel 8,2/10) : échec = rejet sec, rien d'autre à faire que rejeter, quels que soient les autres checks. Le Check 2 (ancrage atlas) : non-overridable lui aussi, mais résoluble UNIQUEMENT en encodant la matière manquante dans l'atlas puis en re-soumettant le concept, jamais par override. Les Checks 3 à 5 restent overridables tracés.

### HR-PGE-3 · Tout emprunt cross-verticale est surfacé, jamais silencieux

Distance > 0 = pari nommé devant l'opérateur (origine, raison de transfert, risque), même quand le curseur l'autorise largement. Un pari non surfacé rend le post-mortem illisible et transfère un risque business à l'agent. Violation = bug.

### HR-PGE-4 · Trois itérations max, puis escalade business

Le cycle d'évaluation s'arrête à 3 passages. Au-delà : escalade explicite nommant le check dominant et la racine amont probable. Jamais de quatrième évaluation, même demandée. Une variante cosmétique re-soumise compte comme itération.

### HR-PGE-5 · Le gate ne mute jamais le workspace

Le pre-gate evaluator retourne un verdict structuré au caller et s'arrête. Zéro écriture (pas de frame.json, pas de genome-package, pas de learnings). La persistance des verdicts appartient au caller : le flux appelant écrit le champ `evaluation` (approval_status, checks, iteration_count) dans chaque fichier concept `brands/{slug}/creatives/{batch}/concepts/CPT-NN.json` via `write_to_context`. Un gate qui écrit cesse d'être composable en subagent.

---

## 7. Anti-patterns canon (AP-PGE-1 à AP-PGE-3)

### AP-PGE-1 · Le gate complaisant (rubber stamp)

Le gate approuve tout le batch par défaut, réservant le rejet aux cas caricaturaux. Symptôme : taux d'approbation proche de 100% sur plusieurs runs, zéro SURFACE émis. Un gate qui ne tue rien ne protège rien : il ajoute de la latence sans déplacer la mortalité des concepts vers l'amont. Pattern correctif : HR-PGE-2 appliqué littéralement (la substitution rejette les génériques plausibles, qui sont la majorité silencieuse), et audit périodique du taux de rejet par check.

### AP-PGE-2 · Le REJECT vague

Verdict "pas assez fort", "à retravailler", "manque d'impact". Inactionnable : l'amont ne sait pas quoi changer, l'opérateur ne peut pas arbitrer, l'itération suivante est une loterie. Chaque rejet nomme le check, l'écart constaté et ce qui ferait repasser le concept. Pattern correctif : la `rejection_reason` est réutilisée telle quelle dans le rendu opérateur, donc écrite en langage métier actionnable dès le verdict.

### AP-PGE-3 · Le spin masqué

Re-soumettre des variantes cosmétiques du même concept rejeté (premise reformulée, même lignage, même pari) en consommant le budget d'itérations, ou contourner le plafond en relançant un "nouveau" batch identique. Le spin transforme un blocage business en activité d'évaluation : tout le monde travaille, rien n'avance. Pattern correctif : HR-PGE-4 (variante cosmétique = itération comptée et signalée) + escalade à la frontière qui nomme la racine amont au lieu de re-juger.

---

## 8. Cross-refs

- `.skills/skills/evaluate-concept/SKILL.md` · l'implémentation du gate : input contract, méthode des 5 checks, agrégation, output JSON + rendu opérateur
- `.skills/skills/qc-creative/SKILL.md` · gate aval (rendu binaire avant spend) · pattern read-only + verdict caller partagé
- frame-regime · gate amont (stratégie du run) · écrit le `frame.json` du batch · le Check 3 lit `frame.json#rayon_max` persisté (jamais re-dérivé) et `frame.json#regime.mode` (enum exploit / balanced / explore) · `regime.freedom_cursor` est un number 0-1, jamais l'enum
- `docs/system/investigation-posture.md` · confidence chain et arbitrage opérateur (les paris SURFACE suivent la même philosophie : hypothèse nommée, opérateur arbitre)
- `docs/system/output-clarity-doctrine.md` · registre du rendu opérateur du gate (dejargonisation, iconographie ✓ ✗ ⚠, action items)
- `CHANGELOG.md` · annonce initiale de cette doctrine à l'entrée v2.88.0 (planifiée pour le sprint v2.88.1, jamais shippée jusqu'à v2.90.0 · l'entrée [2.88.1] n'existe pas)
- D#472, D#473 (design du gate concepts), D#480 (curseur sectoriel distance/rayon), D#499 (arbitrage final) · décisions R&D sources

---

## Status

- **Canonique v2.90+.** Grave la doctrine annoncée à l'entrée CHANGELOG v2.88.0 (planifiée pour le sprint v2.88.1, jamais shippée jusqu'à v2.90.0). Première application : skill `evaluate-concept` v1.0.0 (gate A6 créa-strat).
- **Périmètre** · le POURQUOI et les invariants des 5 checks, le budget anti-spin, la frontière algo/business, l'orthogonalité des trois gates. Le COMMENT opérationnel vit dans la skill et évolue avec elle sans amender la doctrine, tant que les invariants tiennent.
- **Backward compat** · strict additif. N'amende ni `qc-creative` ni frame-regime : insère un étage entre eux.
- **Promotion criterion** · à reviewer après 3+ runs créa-strat complets gatés, 1 audit du taux de rejet par check (détection AP-PGE-1), et 1 post-mortem de campagne où la chaîne des trois gates a permis d'attribuer la cause (stratégie vs concept vs rendu) sans ambiguïté.

---

*Doctrine canonique skill-author-facing + agent-facing. Pose l'asymétrie économique qui justifie le gate concepts (tuer avant le pixel coûte des secondes, après le spend coûte des centaines d'euros et du signal), grave les invariants des 5 checks, plafonne l'itération à la frontière algo/business, et positionne le gate dans la chaîne orthogonale stratégie → concept → rendu.*
