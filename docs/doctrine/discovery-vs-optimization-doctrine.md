# Découverte vs optimisation · le stade décide le jeu

> *« Au lancement, chaque euro dépensé achète de l'information. Au scale, chaque euro dépensé doit acheter des ventes. L'erreur n'est pas de jouer mal · c'est de jouer au mauvais jeu. »*

## L'enjeu

La même action peut être brillante ou suicidaire selon le moment où on la pose. Tester un quatrième angle sur une cinquième audience : signe de rigueur quand la marque cherche encore son premier couple gagnant, fuite caractérisée quand son cœur de cible saigne du CPA sans qu'on ait essoré ce qui marche déjà.

L'opérateur moyen confond les deux régimes parce qu'ils utilisent le même outil · le compte publicitaire · et produisent le même artefact · des créas. Il en déduit qu'il fait toujours la même chose. Faux. Au **lancement**, l'objectif latent n'est pas la vente, c'est la réduction d'incertitude · trouver le premier territoire (audience × job × source d'angle) qui convertit de façon répétable. Le spend est un instrument d'arpentage, on dessine la carte au crayon, on achète de l'information. Au **scale**, l'objectif redevient l'extraction de valeur · essorer le cœur jusqu'à la corde avant d'aller voir ailleurs, et n'attaquer un territoire adjacent que lorsque le cœur sature *vraiment*.

La faute classique tient en une phrase : cartographier des adjacents quand le vrai problème est l'angle. C'est le déguisement le plus séduisant de la procrastination stratégique · ça ressemble à de l'exploration ambitieuse, c'est en réalité un refus de creuser là où ça résiste.

## Les deux thèses

**Thèse A · « Explore d'abord, le marché est plus grand que ta première intuition. »** Eric Ries l'a martelé : au démarrage, ce que vous croyez savoir sur votre client est une hypothèse non testée, et la plupart des hypothèses fondatrices sont fausses sur au moins un axe. Dollar Shave Club ne vendait pas des rasoirs, il vendait une rébellion contre l'arnaque Gillette · ce cadrage n'était pas dans le brief initial, il a émergé du test. Brian Balfour ajoute que les boucles de croissance ne se devinent pas, elles se découvrent par itération. Sur-exploiter une cible avant d'avoir validé qu'elle est la bonne, c'est optimiser le chemin vers une falaise. À ce stade, l'exploration n'est pas un luxe, c'est la seule manière de générer le signal dont tout le reste dépendra.

**Thèse B · « Exploite jusqu'à la corde, la dispersion tue plus de marques que la sur-concentration. »** Le bandit manchot (explore/exploit) a une réponse mathématique : quand un bras paie de façon fiable, chaque tirage ailleurs a un coût d'opportunité réel. La plupart des marques DTC qui plafonnent n'ont pas un problème de portée, elles ont un problème de profondeur · elles n'ont jamais poussé leur angle gagnant à saturation réelle. Athletic Greens a vendu *un* produit, *un* bénéfice central, à *une* audience de biohackers/optimiseurs, pendant des années, en variant l'exécution et non le territoire. Élargir prématurément dilue le budget, brouille le positionnement, et fait croire à une saturation qui n'est qu'une sous-exploitation. La discipline n'est pas glamour, mais c'est elle qui compose les rendements.

Les deux ont raison · dans leur fenêtre. Le travail de la doctrine, c'est de nommer la fenêtre.

## Les principes canon

1. **Le stade pilote le régime, pas l'humeur.** `launch` → exploration dominante · `scale`/`mature` → exploitation d'abord. Le curseur n'est pas un goût, c'est une lecture d'état (cf T7, `brand.json#/meta/stage` LU par le Spectre pour régler explore/exploit).
2. **Au lancement, le spend achète de l'information.** Un test n'a pas pour but de vendre, il a pour but de tuer ou valider une hypothèse de territoire le plus vite possible. La métrique réelle est le taux d'apprentissage, pas le ROAS du jour.
3. **Au scale, on essore avant d'explorer.** On n'ouvre un adjacent que quand le cœur sature. Et la saturation se prouve · pas se ressent.
4. **La saturation réelle a une signature.** CPA qui plafonne *malgré des créas authentiquement fraîches* sur le territoire cœur. Si les créas se répètent, ce n'est pas le marché qui sature, c'est l'imagination.
5. **Le diagnostic décisif précède toute carte d'adjacents** : « mon mur est-il un problème d'OFFRE, d'ANGLE, ou de MARCHÉ ? » Cartographier les adjacents quand le problème est l'angle, c'est fuir le travail.
6. **L'exploration sert le cœur, ne le remplace pas.** Le cœur est le centre de gravité (cf T8, `core_cell_ref`). Toute cellule explorée doit, à terme, soit devenir un nouveau cœur prouvé, soit nourrir le cœur existant.
7. **Le capital de risque borne l'exploration.** Une marque sous-capitalisée explore moins large et plus vite · elle ne peut pas se payer le luxe de dix tirages perdants. L'ambition financière est une variable, pas une constante (le système la demande, ne la présume jamais).
8. **La richesse de l'atlas décale le curseur vers l'exploitation.** Plus la marque a déjà cartographié de VoC, de mécanismes, de profils validés, plus le réflexe par défaut devient « exploite l'existant » avant de payer un nouvel arpentage.

## La méthode · ce qui fait pencher

Avant de choisir entre creuser et cartographier, on passe le **diagnostic du mur** · trois questions exclusives, dans cet ordre, parce que chacune annule la suivante.

**1. Est-ce un problème d'OFFRE ?** Le couple prix/promesse/produit tient-il l'économie ? Si le breakeven CPA est structurellement sous le CPA plancher du canal, aucun angle ne sauvera la marque · le problème est en amont de la pub. *On ne cartographie pas des adjacents pour réparer une marge.* (Lecture : `spec.json#/pricing/breakeven_cpa` vs `brand.json#/financials/roas_breakeven`.)

**2. Est-ce un problème d'ANGLE ?** L'offre tient, mais le message ne déclenche pas. Symptôme : CTR faible, hook qui ne mord pas, reframe absent. *Ici, la réponse est de creuser le même territoire avec un angle neuf, pas d'ouvrir un territoire adjacent.* C'est le piège central · 80 % des « murs de scale » sont des murs d'angle déguisés en murs de marché. Glossier a passé des années à re-cadrer le même bénéfice (la beauté « vraie vie ») sur la même cible avant d'élargir.

**3. Est-ce un problème de MARCHÉ ?** L'offre tient, l'angle a été poussé à saturation prouvée (créas fraîches, CPA plafonné), et le cœur ne rend plus. *Seulement alors* la cartographie des adjacents est le bon mouvement · on passe en exploration ciblée d'un nouveau territoire.

Ce qui fait pencher, donc, c'est la conjonction de trois lectures : le **stade** (régime par défaut), la **signature de saturation** (le cœur rend-il encore ?), et le **diagnostic du mur** (offre/angle/marché). Tant que la saturation du cœur n'est pas prouvée, le défaut est l'exploitation · l'exploration doit *gagner* le droit de consommer du budget, elle ne l'a pas par principe.

Une nuance d'ambition : une marque qui vise une catégorie entière (le pari « devenir le Liquid Death de X ») assume plus d'exploration plus tôt, parce que sa thèse *est* l'expansion. Une marque qui vise un cœur rentable et durable exploite plus longtemps. Le système ne devine pas cette ambition · il la demande ou l'infère du `stage` + de l'equity, et la flague comme déduite tant qu'elle n'est pas déclarée.

## Les variables de décision (ce que le système lit)

| Variable | Ce qu'elle pèse | Où le système la lit dans l'état encodé de la marque |
|---|---|---|
| Stade de marque | Régime par défaut (explore vs exploit) · entrée maîtresse du curseur | `brand.json#/meta/stage` (`launch\|growth\|scale\|mature\|decline`) · trace au build : `spectrum.json#/stage_at_build` |
| Régime retenu | Le curseur effectif, une fois modulé | `spectrum.json#/regime` (`explore-dominant\|balanced\|exploit-dominant`) |
| Saturation du cœur | Autorise (ou non) l'ouverture d'adjacents · CPA qui plafonne malgré créas fraîches = vrai signal | `spectrum.json#/cells[]/saturation` (`fresh\|warming\|saturated`) sur la cellule cœur · `learnings`/perf en amont |
| Cellule cœur (centre de gravité) | Ce que l'exploration sert · null toléré en `launch` pur | `spectrum.json#/core_cell_ref` (SPC-NN) · `cells[]/is_core` |
| Économie d'arbitrage (diag OFFRE) | Tranche « problème d'offre » avant tout angle | `spec.json#/pricing/breakeven_cpa`, `/gross_margin` vs `brand.json#/financials` (`aov`, `roas_breakeven`, `payback_days`) |
| Intensité de la douleur (diag ANGLE) | Y a-t-il un angle non encore exploité sur le territoire ? | `spec.json#/problems_solved[]` (`urgency` 1-10, `frequency` 1-10) + `audiences/{slug}/pain_points/{PNT-NN}.json` |
| Sophistication du marché | Combien de re-cadrages possibles avant épuisement réel | `brand.json#/market/market_overview/sophistication` (`nascent\|growing\|mature\|hyper_saturated`) · par mécanisme : `spec.json#/mechanisms[]/market_sophistication` |
| Richesse de l'atlas | Décale le défaut vers l'exploitation de l'existant | dérivée du remplissage `profile.json`/`spec.json`/`spectrum.json` (frame-regime · pas de champ scalaire unique) |
| Statut de validation marque | Où en est la marque dans son cycle hypothèse→scaled | `brand.json#/meta/validation_status` · par cellule : `spectrum.json#/cells[]/status` (`hypothesis→tested→validated→scaled→fatigued`) |
| Capital / ambition de risque | Largeur et vitesse d'exploration tolérables | Non directement observable · le système le **demande** ou l'**infère** de `stage` + `brand_equity_level`, et le **flague comme déduit** jamais présumé |

Quand une variable n'est pas observable (le capital de risque, l'ambition de catégorie), le système ne tranche pas en silence · il pose la question ou marque l'inférence avec sa provenance (`_source: inferred`), conformément à la politique d'anti-fabrication transverse.

## Composition

Cette tension est le **régulateur de tempo** du graphe · elle ne produit pas de territoire, elle décide quand on a le droit d'en ouvrir un.

Elle est le jumeau opérationnel de **explore vs exploit** (T7) · même curseur, lu ici sous l'angle « quel jeu je joue », là sous l'angle « quel régime j'encode ». Les deux partagent `brand.json#/meta/stage` et `spectrum.json#/regime` · ne pas les dédoubler.

En amont, elle s'appuie sur **carte exhaustive vs spend sélectif** (T1) : la carte reste exhaustive *quel que soit* le régime · seule la priorité de dépense bascule. Explorer ne veut jamais dire mal cartographier.

En aval, elle commande **cœur de cible = centre de gravité** (T8) : l'exploitation, c'est servir le `core_cell_ref` · l'exploration, c'est candidater un nouveau cœur. Et elle s'articule au **scoring** (T6, propriétaire) · le diagnostic du mur reclasse les priorités, il ne réécrit pas la carte. Enfin elle hérite du garde-fou de **qualifier les silences** (T5) : un adjacent n'est une opportunité que qualifié · la procrastination par cartographie est précisément l'ouverture d'adjacents `unqualified`.

## Exemples

**Athletic Greens (AG1) · exploitation longue assumée.** Un produit, un bénéfice (la nutrition « tout-en-un » pour gens occupés/optimiseurs), une cible cœur tenue des années. AG n'a pas couru après des audiences adjacentes tant que le cœur rendait · ils ont varié l'exécution (formats créa, partenariats podcast) en gardant le territoire fixe. Lecture doctrine : `regime = exploit-dominant`, `core_cell_ref` stable, saturation gérée par fraîcheur créative et non par expansion. L'élargissement (sport, voyage) est venu *après* preuve de saturation, pas avant.

**Liquid Death · exploration au service d'une thèse de catégorie.** Ici l'ambition *est* l'expansion · vendre de l'eau comme une marque de metal/rébellion suppose d'arpenter large (festivals, straight edge, anti-plastique, gym) parce que la thèse est culturelle, pas produit. Lecture doctrine : `stage` jeune + ambition de catégorie déclarée → `regime = explore-dominant` légitime. Ce qui serait de la dispersion pour AG est de l'arpentage cohérent pour Liquid Death · même action, jeu différent, parce que l'ambition encodée diffère.

**Hims · le mur d'angle pris pour un mur de marché.** Au lancement, Hims aurait pu croire son plafond venait d'un marché trop étroit (perte de cheveux jeune). Le vrai déblocage fut un *re-cadrage* · normaliser, dédramatiser, esthétiser un sujet honteux · même produit, même cible, angle neuf. C'est le cas d'école du principe 5 : le mur était un mur d'ANGLE. Cartographier des adjacents (peau, sommeil, libido) *avant* d'avoir trouvé cet angle aurait dilué le signal · ces adjacents sont venus *après*, depuis une base cœur prouvée.

## Pitfalls classiques

- **Cartographier des adjacents pour fuir un angle qui résiste.** *Test :* ai-je poussé au moins 3 angles structurellement distincts sur le cœur avant d'ouvrir ailleurs ? Non → tu fuis.
- **Confondre créa répétée et marché saturé.** *Test :* mes 5 dernières créas cœur varient-elles l'angle, ou seulement l'habillage ? Habillage seul → ce n'est pas le marché qui sature.
- **Explorer large sans capital pour encaisser les tirages perdants.** *Test :* puis-je financer 8 à 10 tests morts sans menacer la trésorerie ? Non → resserre l'exploration.
- **Optimiser une cible jamais validée.** *Test :* mon cœur a-t-il un `validation_status` ≥ `validated`, ou est-ce encore une `hypothesis` que j'essore par confort ? Hypothèse → tu optimises une falaise.
- **Réparer une marge par un angle.** *Test :* le breakeven CPA est-il atteignable sur le canal ? Non → c'est l'offre, aucun message ne sauve.
- **Élargir parce que c'est excitant, pas parce que le cœur sature.** *Test :* la cellule cœur est-elle marquée `saturated` avec preuve, ou est-ce une envie ? Envie → reste.

## Checklist applicable

- [ ] J'ai lu le **stade** (`brand.json#/meta/stage`) et nommé le régime par défaut avant toute décision.
- [ ] J'ai passé le **diagnostic du mur** dans l'ordre OFFRE → ANGLE → MARCHÉ, et je sais lequel des trois bloque.
- [ ] Si je veux ouvrir un adjacent : le cœur est-il `saturated` *avec preuve* (CPA plafonné malgré créas authentiquement fraîches) ?
- [ ] J'ai épuisé au moins 3 angles distincts sur le territoire cœur avant de cartographier ailleurs.
- [ ] L'**ambition** (catégorie vs cœur rentable) est déclarée ou flaguée comme inférée · jamais présumée en silence.
- [ ] Le **capital de risque** autorise la largeur d'exploration envisagée.
- [ ] Toute cellule explorée sert le `core_cell_ref` · soit elle le nourrit, soit elle candidate à devenir un nouveau cœur prouvé.
- [ ] Les adjacents ouverts ne sont pas `unqualified` (cross-ref T5) · la demande existe en VoC, le claim est jouable, l'éco tient.

## Sources & lectures

- **Eric Ries**, *The Lean Startup* · validated learning, pivot vs persévérance, le spend comme achat d'information.
- **Brian Balfour** (Reforge) · *Growth Loops* et le fit à quatre niveaux (marché/produit/canal/modèle) · pourquoi les boucles se découvrent.
- **Rahul Vohra** (Superhuman) · le *PMF survey* (les 40 % « très déçus ») · diagnostic quantifié du cœur avant scale.
- **Sutton & Barto**, *Reinforcement Learning* · le dilemme explore/exploit, bandits, coût d'opportunité du tirage exploratoire.
- **Eugene Schwartz**, *Breakthrough Advertising* · les niveaux de sophistication marché · combien de re-cadrages restent avant épuisement réel d'un angle.
- **Clayton Christensen**, *Jobs To Be Done* · pour distinguer un problème d'offre d'un problème d'angle (le « job » sous-jacent).
