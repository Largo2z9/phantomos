# Doctrine de portabilité

> Le no lock-in est une propriété de la façon dont ton contexte est encodé, pas un argument commercial. Ce document explique le mécanisme, pour que tu saches ce que tu possèdes et pourquoi.

---

## 1. Tu possèdes le dossier, pas un abonnement à une mémoire

La plupart des outils qui retiennent quelque chose de toi gardent cette mémoire chez eux, dans un format que tu ne peux ni lire ni emporter. Tu alimentes une boîte noire. Le jour où tu veux partir, ce que le système a appris de ton activité reste de l'autre côté du mur. Tu repars de zéro ailleurs.

Ici le rapport est inversé. Ce que le système sait de ton activité vit dans des fichiers, sur ton disque, dans un format ouvert et documenté. L'outil qui lit ces fichiers aujourd'hui est un lecteur parmi d'autres. Le format ne dépend d'aucun outil. C'est la distinction qui porte le reste : le moteur qui raisonne est interchangeable, ton contexte encodé ne l'est pas, et c'est toi qui le détiens.

Conséquence directe : tu peux ouvrir le dossier, le lire, le copier, le dupliquer pour un associé, le transférer vers un autre environnement, ou le vendre. Aucune de ces actions ne demande la permission de qui que ce soit, parce qu'aucune ne passe par un serveur tiers.

---

## 2. Capture sans friction, rangement par la machine

Le geste d'entrée est volontairement simple : tu colles du brut. Une page produit, un fil de commentaires, une note vocale retranscrite, un export de tableur, une phrase jetée en passant. Tu ne formates rien, tu ne tries rien. L'agent range.

Ce rangement n'est pas cosmétique. Chaque morceau de brut atterrit dans une case connue d'une structure connue : qui est la marque, quel produit, quelle audience, quel angle, quelle preuve. Le brut entre désordonné et ressort comme donnée placée. C'est le premier maillon de la portabilité : une note libre dans un coin de logiciel ne s'emporte pas proprement, une donnée rangée dans une structure stable, si.

---

## 3. Ce qui rend la donnée transportable : typée par origine, sourcée, historisée

Une donnée rangée mais muette ne vaut pas grand-chose. Ce qui la rend exploitable plus tard, et par n'importe qui, c'est ce qu'on sait d'elle en plus de sa valeur.

**Typée par origine.** Chaque valeur porte la trace de comment on la sait : observée (vue directement sur le site ou les données), déclarée (la marque l'affirme d'elle-même), structurée (une observation rangée dans une grille d'analyse connue), calculée (déduite d'autres valeurs par une formule). Tu ne vois jamais ces étiquettes en clair : le système te restitue du « observé », du « déduit », du « déclaré », de l'« incertain ». Le mécanisme dessous : sans cette distinction, un fait scrapé et une supposition pèsent pareil, et tout raisonnement bâti dessus hérite du flou.

**Sourcée.** Une affirmation qui pèse sur une décision n'est pas traitée comme acquise sur un seul signal. Tant qu'elle repose sur une source unique, elle reste marquée comme hypothèse à valider. Le mécanisme : un avis isolé ne devient pas une vérité de marque par accident.

**Historisée.** Rien ne s'efface. Une donnée corrigée n'écrase pas l'ancienne, elle la marque comme remplacée et garde la trace. Le mécanisme : l'historique est un actif, pas un encombrement. Le jour où tu veux comprendre pourquoi une décision a été prise il y a trois mois, la piste est intacte. Une mémoire qui se réécrit en silence perd sa valeur de preuve.

Ces trois propriétés voyagent avec la donnée parce qu'elles sont dans le fichier, pas dans la tête de l'outil.

---

## 4. Conséquence immédiate : lisible et exploitable à la demande

Comme tout est rangé, typé et sourcé, le dossier est lisible par un humain et exploitable par n'importe quelle machine. La donnée est du texte structuré ouvert, pas un format maison verrouillé. Aucun connecteur propriétaire requis pour la lire.

Ce que ça t'apporte concrètement : une marque encodée aujourd'hui peut être consommée demain par un autre modèle, un script que tu écris toi-même, ou un tableau de bord. Tu poses une question, le système va chercher exactement les éléments concernés, pas une approximation. Tu n'as pas à réexpliquer ton activité à chaque session : elle est déjà là, et elle s'accumule au lieu de se reperdre.

---

## 5. Le test de portabilité entre métiers : l'extractibilité

La portabilité ne s'arrête pas à « tu peux emporter tes données ». Elle inclut « la structure qui les range marche ailleurs que sur ton métier d'aujourd'hui ». C'est testable, et le test est binaire.

Pour chaque brique du système, on se demande : si je renomme « marque » en « compte » (pour un logiciel en abonnement), en « dossier » (pour du juridique), en « lieu » (pour de l'hôtellerie), est-ce que ça tient encore ? Si oui, la brique est universelle. Si non, elle appartient à un module spécialisé qu'on isole.

Le mécanisme : cette règle empêche le système de se souder à un seul métier sans qu'on s'en aperçoive. Ce qui passe le test est une fondation transférable. Aujourd'hui la fondation est calibrée sur l'acquisition e-commerce, c'est l'incarnation testée à grande échelle. Une structure qui survit au renommage « marque → compte » est une structure que tu peux porter vers un autre domaine sans la reconstruire.

---

## 6. Le dossier reste la référence face à n'importe quelle interface

Tu peux préférer travailler dans une interface en tableaux, vues, glisser-déposer, plutôt que dans le moteur lui-même. C'est permis. Le rapport reste asymétrique sur un point : le format de référence, c'est ton dossier. L'interface en est une vue.

Le mécanisme : si l'interface était la source, chaque opération devrait repasser par elle, avec sa latence, ses limites et son contrôle sur tes données. En gardant ton dossier comme référence, l'interface devient optionnelle. Tu la branches si elle te sert, tu l'ignores sinon, et dans les deux cas ton dossier reste lisible, versionnable, emportable.

---

## 7. Le dossier se fork, se transfère, se vend

Parce que ton activité est rangée par marque dans des dossiers étanches, l'unité que tu manipules est nette. Un dossier de marque ne fuit pas dans un autre : ce qui est appris sur l'une ne contamine pas l'autre sans une autorisation explicite de ta part. Le mécanisme protège ta confidentialité quand tu gères plusieurs clients, et il rend chaque dossier autonome.

Autonome veut dire détachable. Tu peux copier le dossier d'une marque pour le confier à un associé, en faire une variante de travail, le sortir de l'environnement, ou le céder. Rien dans l'encodage ne suppose qu'il doit rester là où il est né. À comparer à la mémoire d'un fournisseur où ton historique est inséparable de son service : le jour où tu pars, tu pars sans rien.

---

## 8. Migrable vers n'importe quel lecteur futur

Le moteur qui lit ton dossier aujourd'hui finira par changer. Un nouvel outil, un nouveau modèle, une nouvelle génération de logiciels arrivera. C'est attendu, pas redouté.

Le mécanisme : le format ne dépend d'aucun lecteur particulier. Il est documenté, ouvert, et conçu pour qu'un autre programme puisse l'ingérer. Le lecteur d'aujourd'hui est inclus dans ce raisonnement : lui aussi est remplaçable. Ton dossier lui survit. C'est l'inverse d'une donnée prisonnière du logiciel qui l'a créée, illisible dès qu'on coupe l'abonnement.

---

## 9. Ce qui n'est pas encore outillé, et comment ça s'encode

Deux chantiers de portabilité sont nommés mais pas encore câblés. État actuel, puis le chemin.

**Plusieurs opérateurs sur un même dossier.** Aujourd'hui le dossier suppose un seul pilote. Quand deux personnes écriront dans la même marque, il faudra tracer qui a écrit quoi et qui a le droit de modifier. Ce n'est pas encore outillé. Ça s'encode : chaque écriture porte déjà l'identité de son auteur dans le journal, il reste à poser au-dessus une couche qui dit qui possède et qui peut lire. La place est réservée pour ça.

**Le dossier comme produit vendable.** Vendre ou licencier un dossier encodé à un tiers demande de gérer les versions, l'attribution, la propriété. Ce n'est pas encore outillé. Ça s'encode : le format prévoit déjà l'emplacement d'un bloc qui dit d'où vient chaque élément, sous quelle licence, signé par qui. Le jour où tu vends, c'est ce bloc qui rend la cession propre.

---

## 10. Le zéro lock-in est structurel, pas un bonus

Reprends la chaîne. Tu colles du brut, l'agent le range. Le rangement produit de la donnée typée par origine, sourcée, historisée. Cette donnée est lisible par un humain et par n'importe quelle machine, dans un format ouvert qui ne dépend d'aucun lecteur. La structure qui la range survit au renommage d'un métier à l'autre. Le dossier reste la référence face à n'importe quelle interface. Il se fork, se transfère, se vend, et il migrera vers le prochain outil sans toi à la manœuvre.

À aucun maillon de cette chaîne tu n'as eu besoin de demander la permission d'un fournisseur. C'est la propriété structurelle : le no lock-in ne dépend pas d'une mise à jour ni d'une fin d'abonnement, parce qu'il n'est pas une faveur qu'on t'accorde. Il est dans la façon dont ton contexte est encodé. Tu possèdes le dossier.
