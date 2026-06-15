# Les quatre catégories d'agents

> Carte opérateur. Ce document décrit les quatre familles d'agents qui travaillent dans ton espace, et pourquoi elles sont séparées. La séparation n'est pas qu'une question d'organisation : c'est la pièce qui rend le système sûr. Tant que tu sais quelle famille a le droit d'écrire dans ta connaissance encodée et laquelle ne fait que la lire, tu gardes la main sur ce qui change et sur ce qui ne change pas.

---

## Principe

Un agent fait l'une de quatre choses avec ta connaissance encodée : il l'enrichit, il la lit pour raisonner, il la consomme pour produire, ou il propose de la corriger. Ces quatre gestes ne se mélangent pas dans un même agent. Ce cloisonnement évite que ton encodage dérive sans que tu le décides.

Le mécanisme derrière cette règle : ta valeur n'est pas le modèle, qui est devenu une marchandise disponible partout. Ta valeur est ce que tu as encodé une fois et que l'agent réutilise à chaque session. Si n'importe quel agent pouvait réécrire cet encodage à tout moment, ton avance bougerait sans que tu le décides. Le système réserve donc le droit d'écriture à un seul type d'agent, et oblige un second à passer par ton arbitrage. Les deux autres ne font que lire. Tu sais ainsi, par construction, d'où vient chaque changement.

---

## Contexte : les seuls agents qui écrivent dans le moteur

C'est la première famille, et la seule autorisée à écrire dans ta connaissance encodée. Quand tu fais ton onboarding, quand tu colles la page d'un produit, quand tu enrichis une audience ou que tu corriges un fait sur ta marque, c'est un agent de contexte qui travaille. Il range ce que tu lui donnes dans la structure du moteur : il transforme une matière brute en élément réutilisable, propre, relisable.

Le mécanisme : écrire dans le moteur veut dire modifier ce sur quoi toutes les sessions futures vont raisonner. C'est l'acte le plus lourd du système, donc le plus encadré. Un agent de contexte ne décide pas seul de ce qui est vrai. Il marque l'origine de chaque fait (observé sur une source, déclaré par toi, déduit) et son niveau de certitude. Un fait observé et un fait supposé n'entrent pas dans le moteur avec le même statut, et tu les retrouves distingués plus tard. Cela évite qu'un encodage se transforme en mélange où l'on ne sait plus ce qui est solide et ce qui est une hypothèse.

Pour toi, concrètement : tu n'as plus à réexpliquer ton activité. Tu encodes une fois, et l'avance que tu construis devient structurelle au lieu de se reperdre d'une conversation à l'autre. La contrepartie de ce pouvoir d'écriture, c'est qu'il est étroitement gardé. C'est voulu.

---

## Analyse : les agents qui lisent et raisonnent sans rien modifier

La deuxième famille lit ton encodage, le croise, en tire des verdicts, et n'écrit rien dedans. Un audit de la voix de ton marché, une cartographie d'audience, un repérage de l'écart entre tes offres et tes segments, un balayage concurrentiel : tout cela lit le moteur et produit un rapport, jamais une mutation.

Le mécanisme, qui est au cœur de la sûreté du système : un agent qui raisonne a besoin de fabriquer des hypothèses pour avancer. Il suppose, il extrapole, il teste des pistes. Si ce même agent pouvait écrire dans ton moteur, ses suppositions de travail s'y déposeraient et finiraient par ressembler à des faits établis. En lui retirant le droit d'écriture, on garantit que son raisonnement reste à l'extérieur de ta connaissance encodée. Il te rend ce qu'il a vu, ce qu'il a déduit, ce qu'il ignore encore, et les leviers pour lever ce qu'il ignore. Mais il ne décide pas à ta place que telle déduction devient un fait du moteur.

Pour toi : tu reçois une lecture honnête, séparée en ce qui est observé, ce qui est supposé, ce qui reste inconnu. Pas un document qui invente une certitude qu'il n'a pas, et pas un document qui se serait infiltré dans ta base sans que tu l'aies validé. Le rapport vit à côté du moteur, pas dedans.

> État actuel : à ce jour, cette famille n'est pas encore complètement outillée dans ton espace. Le moteur sait porter l'origine et l'incertitude de chaque fait, ce qui est la fondation dont l'analyse a besoin, mais les agents d'audit dédiés (cartographie d'audience fine, score d'adéquation offre-segment) ne sont pas encore tous câblés. Voilà comment cela s'encode quand ça arrive : ce sont des agents en lecture seule, branchés sur le même moteur, qui produisent un rapport daté et le déposent à côté de ta base, jamais dedans. La règle de séparation est déjà posée ; ce qui manque, ce sont les agents qui l'occupent.

---

## Production : les agents qui consomment l'actif validé sans remonter à la source

La troisième famille fabrique tes livrables : la copie, les pages, les déclinaisons publicitaires, les emails. Elle lit ton encodage pour le composer, et ne touche pas à la source. La distinction est précise : la production lit, elle ne réécrit pas le moteur.

Le mécanisme : un agent de production ne lit pas tout ton encodage, il lit seulement la part que tu as validée et activée. Ce qui est documenté mais pas encore prêt, ce qui est en réserve, ce qui est une piste dormante reste invisible pour lui. Il travaille à partir d'un vocabulaire fini d'éléments que tu as approuvés (angles, mécaniques, preuves, accroches, styles) et il les traverse en combinaisons pour produire en volume. C'est cette discipline qui te donne cent créations cohérentes sans chute de qualité au fil de la série : elles puisent toutes dans le même ensemble validé, donc elles ne dérivent pas.

Le séparer de la source te protège deux fois. D'abord, produire ne peut pas abîmer ton encodage par effet de bord, puisque la production n'a pas le droit d'écrire. Ensuite, comme elle ne consomme que l'actif validé, elle ne peut pas composer sur une hypothèse non confirmée ou un brouillon que tu n'as pas validé. La frontière entre ce que tu sais et ce que tu fabriques à partir de ce que tu sais reste nette.

Pour toi : tu produis en quantité sans repartir d'une page blanche, et sans craindre qu'une session de production vienne contaminer ta base. La source reste la source, intacte, pendant que la production tourne par-dessus.

---

## Optimisation : les agents qui proposent des corrections que tu arbitres

La quatrième famille ferme la boucle. Une fois que tes livrables sont dans le monde et que des résultats reviennent, ces agents lisent ce signal, le confrontent à ton encodage, et repèrent ce qui mériterait d'être mis à jour : une preuve qui tient mieux que prévu, un angle qui s'use, une audience plus réactive qu'estimé. Ils en tirent des propositions de mise à jour du moteur.

Le mécanisme, qui est la garantie centrale de cette famille : un agent d'optimisation propose, il n'applique pas. La correction qu'il formule attend ton arbitrage avant d'entrer dans la connaissance encodée. La raison est qu'une mise à jour pilotée par les résultats touche au cœur du moteur, comme un agent de contexte le ferait, mais sur la base d'un signal que toi seul peux qualifier. Un chiffre qui remonte peut être un vrai apprentissage ou un accident de mesure. Le système ne tranche pas cela à ta place. Il te présente la proposition, tu décides, et c'est ta décision qui modifie le moteur, pas l'observation brute.

Le mécanisme plus profond derrière cette famille : ce qui se répète vaut plus que ce qui n'est dit qu'une fois. Une correction qui revient session après session pèse davantage qu'un signal isolé, et le système densifie ta connaissance dans cette direction, toujours sous ta validation. Au fil du temps, chaque session a besoin de moins de corrections, parce que les apprentissages stables se sont déposés dans le moteur, un par un, chacun arbitré.

Pour toi : le creux de l'été, par exemple, cesse d'être une saison morte. Pendant que la production tourne au ralenti, les résultats accumulés deviennent matière à affiner ton encodage. Le temps calme devient un investissement, parce que la boucle d'optimisation transforme ce qui s'est passé en moteur plus dense pour la suite.

> État actuel : cette famille n'est pas encore outillée dans ton espace. Le geste existe ailleurs sous une forme manuelle (les apprentissages que tu actes en fin de session entrent déjà dans le moteur sous ton contrôle), mais les agents qui relisent automatiquement les résultats pour te proposer des mises à jour ne sont pas encore câblés. Voilà comment cela s'encode quand ça arrive : un agent qui lit le signal de performance, formule une proposition datée, te la soumet, et n'écrit dans le moteur que la version que tu as validée. Le principe d'arbitrage est déjà la règle ; ce qui manque, c'est l'agent qui alimente la proposition.

---

## Pourquoi cette séparation tient le système

Reprends la carte d'un seul regard. Une famille écrit dans ton moteur sous ton contrôle direct (contexte). Une famille ne fait que lire et raisonner, sans jamais écrire (analyse). Une famille consomme uniquement l'actif que tu as validé, sans remonter à la source (production). Une famille propose des corrections qui attendent ton feu vert (optimisation). Deux familles touchent ta connaissance encodée, deux n'y touchent pas, et celle qui voudrait la corriger doit passer par toi.

Le mécanisme d'ensemble : la sûreté d'un système qui raisonne et produit à ta place ne vient pas d'une promesse de bonne conduite, elle vient de qui a le droit d'écrire où. En cloisonnant le droit d'écriture, le système rend impossible toute une classe d'accidents : une hypothèse d'analyse qui se fige en fait, une session de production qui corrompt la base, un chiffre de performance qui réécrit ta stratégie sans que tu l'aies décidé. Chacun de ces accidents serait une dérive silencieuse de ton avance. La séparation des catégories les rend structurellement impossibles, pas seulement déconseillées.

Distinction utile, pour rester honnête sur ce que tu observes par rapport à ce qui se déduit : ce que tu observes aujourd'hui, c'est que le contexte et la production fonctionnent dans ton espace. Ce qui se déduit de l'architecture, c'est que l'analyse et l'optimisation s'y brancheront sans casser la règle, parce que la règle de séparation est déjà posée et que le moteur porte déjà l'origine et l'incertitude dont ces deux familles ont besoin. Elles n'ajoutent pas une exception au modèle ; elles occupent deux cases qui les attendent.

Au-dessus de ces quatre familles, un même réflexe les traverse sans en être une cinquième : aucun acte qui engage de l'argent ou qui est irréversible ne se déclenche sans une validation explicite de ta part. Ce n'est pas une catégorie d'agents, c'est une garde qui s'applique à toutes. On retrouve là le fil entier : ce qui rend le système sûr, c'est que tu restes l'arbitre de tout ce qui change et de tout ce qui coûte.
