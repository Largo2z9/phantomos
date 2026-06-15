# Doctrine du drill dynamique

> Le drill dynamique est un protocole qui recombine des éléments existants pour explorer un univers de proche en proche, sans carte définie à l'avance.

## Définition

Tu pars d'une thématique. L'agent rend une fiche courte qui se tient seule, puis il calcule sur le moment les deux à quatre concepts voisins les plus pertinents pour toi, et te laisse choisir où aller. Tu peux descendre dans un concept, ouvrir un voisin, déclencher une action, ou remonter. Il n'y a pas de cul-de-sac. C'est une exploration guidée où la carte se construit pendant le parcours, pas avant.

## Problème adressé

La plupart des explorations de connaissance reposent sur un sommaire figé : un arbre décidé à l'avance, où chaque branche mène toujours aux mêmes sous-branches, indépendamment de ce que tu cherches. Or ton intention change ce qui est pertinent. Si tu creuses un concept de production parce que tu veux comprendre comment générer en volume, les voisins utiles ne sont pas les mêmes que si tu le creuses pour comprendre comment garantir la cohérence. Un sommaire figé t'envoie au même endroit dans les deux cas.

Le drill dynamique inverse cette logique. Au lieu de parcourir un arbre pré-câblé, l'agent regarde où tu es et ce que tu cherches, puis fabrique les deux à quatre prochains pas les plus utiles pour ton intention. Le mécanisme croise trois sources au moment où tu choisis : ce que le concept courant touche directement, le réseau de renvois entre concepts déjà tracé dans l'univers, et le vocabulaire de référence qui indique quels termes sont proches de sens. La pertinence n'est pas stockée, elle est recalculée à chaque pas. C'est la différence entre une table des matières et une exploration qui suit ton intention.

## Le protocole, étape par étape

### Étape 0 : une fiche qui se tient seule

Depuis n'importe quelle thématique, l'agent rend d'abord une fiche au format de référence. Cinq blocs, dans cet ordre : une intro de deux à trois lignes qui pose le concept en langage clair, une section clé qui développe le coeur, un bloc "ce qui rend ça possible" qui montre le mécanisme structurel, un bloc "ce que ça change pour toi" qui traduit en levier opérationnel, et un bloc "pour aller plus loin" qui ouvre la suite. Environ trente lignes, pas plus.

Cette fiche est le livrable, pas un préambule à un menu. Tu dois pouvoir la lire, la comprendre, et repartir sans rien cliquer. La suite est offerte, jamais imposée. La raison : une exploration qui force un choix à chaque écran fatigue et transmet peu. Une exploration qui rend d'abord et propose ensuite te laisse apprendre à ton rythme.

### Étape 1 : le calcul des voisins

C'est ici que le drill dynamique se distingue d'un sommaire. Au lieu de proposer des voisins fixes attachés au concept, l'agent calcule deux à quatre concepts adjacents pertinents pour l'intention que tu viens d'exprimer.

Le calcul croise trois sources :
- Les adjacences directes du concept courant, c'est-à-dire ce qu'il touche par nature.
- Le réseau de renvois entre concepts déjà tracé dans l'univers, qui indique quels concepts citent celui-ci.
- Le vocabulaire de référence, qui indique quels termes sont proches de sens même sans lien explicite.

L'agent superpose les trois, garde ce qui est pertinent pour ton intention, et écarte le reste.

Un exemple. Tu creuses la composition : l'idée qu'un livrable se calcule en combinant des éléments stables et des éléments de contexte, plutôt qu'il ne s'invente. Si ton intention est "comprendre comment ça reste cohérent en volume", les voisins calculés penchent vers les éléments réutilisables et les règles qui cadrent. Si ton intention est "comprendre comment ça s'adapte à chaque cas", les voisins calculés penchent vers le contexte variable et le raisonnement qui s'ajuste. Même concept de départ, deux ouvertures différentes, parce que l'intention a changé le calcul.

Deux à quatre voisins, jamais plus. Au-delà, ce n'est plus un choix mais une liste à subir. Le nombre exact dépend de la richesse réelle du concept à cet endroit, pas d'un quota. Un concept simple ouvre deux pistes. Un carrefour dense en ouvre quatre.

### Étape 2 : ouvrir les dimensions quand le territoire est flou

Parfois tu ne sais pas encore ce que tu cherches. La thématique est large, l'intention n'est pas formée. Descendre tout de suite reviendrait à creuser au mauvais endroit.

Dans ce cas, l'agent n'enchaîne pas une fiche. Il ouvre d'abord les dimensions du territoire : il te pose des questions guidées et génère des axes sur le moment pour faire émerger ce que tu ne sais pas encore que tu dois considérer. Tu ne pars pas d'une page blanche, l'agent te montre les paramètres décidables. Une fois la zone éclairée, tu choisis où descendre, et le drill reprend en étape 0 sur le bon concept.

Ce passage par les dimensions utilise le même moteur d'ouverture que celui qui transforme une intention floue en carte de paramètres. On ne l'invoque pas systématiquement, seulement quand le flou bloque. La règle : si tu sais où tu vas, on descend ; si tu ne sais pas, on cartographie d'abord, puis on descend. Le drill ne fait jamais creuser à l'aveugle.

### Étape 3 : quatre choix vivants par fiche

Le bloc "pour aller plus loin" n'est pas une liste figée. Il est alimenté dynamiquement à chaque fiche, et il propose toujours quatre directions, jamais moins, pour qu'aucune fiche ne soit un cul-de-sac.

Les quatre directions :
- Descendre dans le concept courant, pour aller plus profond sur ce que tu lis.
- Ouvrir un adjacent calculé à l'étape 1, pour partir sur un voisin pertinent.
- Déclencher l'action ou la capacité associée au concept, quand le concept correspond à quelque chose que le système sait faire et pas seulement expliquer.
- Remonter, pour revenir au niveau au-dessus sans te perdre.

Le principe "jamais de cul-de-sac" répond à un problème simple : une exploration qui se termine sur une fiche sans sortie te laisse coincé, et tu dois reformuler toi-même pour repartir. En garantissant toujours une remontée et au moins un voisin, le drill reste navigable indéfiniment. Tu avances, tu recules, tu pivotes, sans jamais redémarrer.

### La discipline render-first

Une règle prime sur les autres et ne se négocie pas : la fiche en texte d'abord, le widget de choix seulement après, et seulement si une décision te bloque réellement.

Concrètement, l'agent rend la fiche complète, blocs et voisins compris, en texte, dans la conversation. Il ne remplace jamais ce rendu par une question interactive ou un menu cliquable. Tu navigues normalement en reformulant ou en nommant le concept suivant, sans aucun widget. Une question interactive n'apparaît qu'après le rendu complet, et uniquement si un arbitrage de ta part empêche réellement de continuer.

Le livrable du drill est la connaissance rendue, pas l'invite à choisir. Un système qui collecte ses informations puis substitue le contenu par un menu de navigation t'a fait perdre le contenu. La discipline render-first verrouille l'ordre : rendre, puis offrir, jamais offrir à la place de rendre. Cette règle est observée sur les cockpits du système et héritée telle quelle par le drill.

### Étape 4 : héritage de la posture d'investigation et mémoire de progression

Deux mécanismes ferment le protocole et le rendent honnête dans le temps.

Le premier est l'héritage de la posture d'investigation. Chaque concept ouvert distingue ce qui est observé de ce qui est déduit. Un voisin lu directement dans le réseau de renvois tracé est une chose. Un voisin inféré, c'est-à-dire calculé par proximité de sens sans lien explicite, en est une autre. Ce second cas est marqué confiance basse. Tu sais donc, à chaque pas, si l'agent t'emmène sur un voisin solide ou sur une piste qu'il a déduite. Une exploration qui présente l'inféré comme du certain te fait creuser des fausses pistes avec assurance. En marquant le niveau de confiance sur chaque adjacence proposée, le drill reste auditable. Tu décides en connaissance de cause d'aller sur le solide ou de tenter l'inféré.

Le second est la mémoire de progression multi-sessions. Le drill se souvient d'où tu as déjà creusé et de ce qui reste à ouvrir. D'une session à l'autre, tu ne réexplores pas ce qui est acquis, et l'agent peut te pointer les zones encore vierges. Une exploration sans mémoire te refait parcourir le même terrain à chaque fois. En gardant trace des concepts déjà ouverts contre ceux encore fermés, le drill accumule au lieu de se reperdre. Ta carte mentale de l'univers se construit sur la durée, elle ne se réinitialise pas.

Note de cadrage sur cette mémoire de progression. La trace par session est aujourd'hui partiellement outillée : le système sait dire ce qui a été touché récemment, mais il ne tient pas encore un journal complet "exploré contre à ouvrir" propre au parcours de drill. Ça s'encode : une trace dédiée au drill, qui marque chaque concept ouvert et son niveau de profondeur atteint, branchée sur la mémoire persistante déjà en place. C'est un cran d'outillage à poser, pas un manque de conception.

## Le calibrage : profondeur contre largeur

Le drill n'a pas une seule forme. Il s'adapte à ce que tu demandes.

Concept simple, intention claire : une fiche, deux adjacents. Tu lis, tu choisis, tu repars. Léger et rapide. C'est le mode par défaut quand tu sais ce que tu cherches et que le concept tient en un écran.

Intention multi-couches, sujet large ou question qui touche plusieurs niveaux : une cascade de fiches enchaînées. L'agent ouvre un concept, calcule ses voisins, t'en propose un, l'ouvre à son tour, et ainsi de suite, en gardant le fil de là où tu viens. La profondeur se construit pas à pas, jamais d'un bloc.

La richesse de l'ouverture suit la richesse de l'intention, pas un format imposé. Une intention simple sur-dimensionnée en cascade te noie. Une intention complexe écrasée en une seule fiche te frustre. Le drill lit le poids de ce que tu demandes et règle largeur et profondeur en conséquence : deux pistes pour un point précis, une cascade pour un territoire à couvrir.

## Ce que ça te permet, concrètement

Tu explores ton univers métier comme un terrain réel : tu pars d'un point, tu vois ce qui est autour de toi en fonction de là où tu veux aller, tu avances, et tu peux toujours revenir. Pas de plan à mémoriser, pas de syntaxe, pas de carte à connaître d'avance.

Une thématique floue devient une exploration guidée qui se forme au fil du parcours, calibrée sur ce que tu cherches. Une zone que tu pensais marginale peut se révéler centrale, quand le calcul des voisins montre qu'elle est un carrefour vers trois autres concepts que tu n'avais pas vus. Tu ne suis pas un sommaire imposé, tu construis ton chemin avec un agent qui calcule à chaque pas ce qui te sert le plus.

Parce que la posture d'investigation et la mémoire de progression sont câblées dans le protocole, tu sais toujours où tu marches sur du solide et où tu tentes une piste, et tu ne refais pas deux fois le même terrain. L'exploration s'accumule au lieu de se reperdre. C'est ce qui sépare une table des matières d'un système qui explore avec toi.

## Discipline pour l'agent : les règles dures

Pour que le protocole tienne, l'agent respecte ces points sans exception.

Rendre la fiche complète en texte avant tout. Ne jamais substituer le rendu par un menu ou une question interactive. La question interactive n'arrive qu'après le rendu, et seulement sur décision réellement bloquante.

Calculer les voisins à chaque pas, jamais les lire dans une liste figée. Croiser les trois sources : adjacences directes, réseau de renvois, vocabulaire de référence. Garder deux à quatre voisins, jamais plus, le nombre suivant la densité réelle du carrefour.

Marquer la confiance sur chaque adjacence : solide si lue dans un lien explicite, basse si inférée par proximité de sens. Ne jamais présenter un voisin inféré comme certain.

Garantir quatre sorties par fiche : descendre, ouvrir un adjacent, déclencher l'action associée, remonter. La remontée et au moins un adjacent figurent dans le bloc d'ouverture « pour aller plus loin » de CHAQUE fiche, pas seulement à la clôture finale du parcours. La fiche racine (la carte) offre en plus au moins une porte d'action concrète, pas uniquement des portes de drill. Jamais de fiche sans remontée. Jamais de cul-de-sac.

Ouvrir sur la charge, jamais sur du filler. Pas de « bienvenue dans la carte » ni d'accueil décoratif, pas de « retour toujours possible » en réassurance (la réversibilité se signale par l'affordance de navigation, pas par une phrase de réconfort). Pas de négation pédagogique (« tu n'explores pas un sommaire figé »), pas de chiffrage rhétorique (« testable en dix secondes »). Affirme en positif et varie l'attaque des blocs, ne verrouille pas un « tu... » obligatoire en tête de chaque fiche.

Ouvrir les dimensions par questions guidées seulement quand le territoire est flou. Si l'intention est claire, descendre directement. Ne jamais cartographier pour cartographier.

Calibrer largeur et profondeur sur le poids de l'intention. Deux pistes pour un point précis, cascade pour un territoire. Ne jamais imposer un format unique.

Tenir la mémoire de progression quand elle est disponible, et le dire clairement quand un pan n'est pas encore outillé : ce qui n'est pas encore câblé se nomme "pas encore outillé" et s'accompagne du comment ça s'encode. Jamais "impossible", jamais "hors sujet".

## Ce qui reste à outiller

Deux crans sont à poser pour que le protocole soit complet de bout en bout.

La trace de progression dédiée au drill. Aujourd'hui la mémoire récente existe mais ne distingue pas finement "exploré contre à ouvrir" sur un parcours d'exploration. Ça s'encode : une trace par parcours, qui marque chaque concept ouvert, le niveau de profondeur atteint, et la date, branchée sur la mémoire persistante déjà en place. Le rendu en bénéficie directement : l'agent peut alors pointer les zones vierges en début de session.

Le marquage systématique de la confiance d'adjacence. Le principe est posé, mais sa pose à chaque calcul de voisin reste à durcir pour qu'aucun voisin inféré ne passe sans son étiquette. Ça s'encode : un drapeau de confiance attaché à chaque adjacence proposée, dérivé de la source qui l'a fait remonter, rendu visible dans le bloc d'ouverture. Tant que ce n'est pas durci, l'agent applique la règle manuellement et la signale.

Aucun de ces deux points n'est un manque de conception. Le protocole tient comme doctrine. Ce sont deux crans d'outillage à poser pour qu'il s'exécute sans tenue à la main.
