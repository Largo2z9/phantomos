# Scrape = allocation sous contrainte

> Doctrine système (D#518). Sœur de `docs/system/open-map-reasoning.md` (raisonnement à carte ouverte), `docs/system/investigation-posture.md` (les 5 sections) et `docs/system/contextual-intelligence.md` (Master rule). Gouverne COMMENT le scan dépense son effort de fetch.

## La thèse

Le scan n'est pas un crawl qui couvre le site. C'est une **allocation d'effort sous contrainte** · maximiser la réduction d'incertitude sur la prochaine décision qui paie, pas la couverture des pages. Un artefact qui DIRIGE le fetch (un plan, une question) se remplit · un artefact qui le COURONNE (un rapport produit après coup) reste vide.

Valeur d'une lecture = réduction d'incertitude × poids de la décision qu'elle change. On fetch là où ce produit est haut, on s'arrête quand il tombe.

## Trois contraintes dures

### 1 · Pertinence · piloté par la question

- **L'enjeu AVANT la recon.** Avant de dimensionner le scan, on pose ce que ce scan doit trancher (où la marque veut aller, où ça coince · cf `docs/doctrine/strategic-diagnostic-doctrine.md`). « Pertinent » se mesure contre cet enjeu, jamais contre la couverture du site. Un scrape sans enjeu posé = du bruit bien formaté.
- **Les pré-amorces deviennent le PLAN de fetch, pas le rapport.** Les 2 à 4 inconnus à fort levier que la recon pré-remplit ne sont pas un appendice du rapport · chacun nomme le fetch ciblé qui le résoudrait. Le plan de scan profond EST la liste des pré-amorces converties en lectures.
- **Le Spectre DIRIGE le fetch, il ne le couronne pas.** La carte mécanisme→usage (`spec.use_cases[]` + `spectrum.json`) ne se construit pas à la fin pour décorer · elle pointe les zones blanches vers lesquelles le fetch marché/concurrentiel s'oriente. La cartographie ouvre les questions, le fetch les ferme.

### 2 · Temporalité · fraîcheur par velocity-tier

La fraîcheur est un curseur `exp(-Δt/demi-vie)`, jamais un booléen vrai/périmé. Chaque brique porte sa classe de volatilité (`velocity_tier`, cf `resources/schemas/_shared/extraction-provenance.json`) ·

| Tier | Quoi | Demi-vie |
|---|---|---|
| static | claim, mécanisme | ~270j |
| slow | VoC, profil | ~120j |
| drift | sophistication marché | ~60j |
| weekly | pubs concurrentes | ~14j |
| live | perf compte | ~2j |

La LONGÉVITÉ d'un signal nourrit sa force (une ad adverse à 8 mois = strong, récente = weak · ne pas confondre âge de la brique et durabilité du signal). Refresh = max(décroissance, déclencheur d'état), jamais calendaire-ou-jamais. C'est ce qui fait passer d'un instantané one-shot à une carte vivante · des skills indépendants (`watch-competitors` seul par un cron) rafraîchissent une couche sans rebuild l'atlas.

### 3 · Justesse · fiabilité par source, scrapé ≠ fait

`reliability_tier` plafonne la confiance d'ENTRÉE par nature de source (maillon-0 de la chaîne · le `min` existant fait le reste) ·

- revealed (back-end, comportement observé) ≤0.8
- behavioral-soft (volume de recherche, spend inféré) ≤0.5
- verbatim (VoC/VoM cité) ≤0.5
- structural (raisonnement mécanisme→job) = hypothèse, démarre non-prouvé
- declared (claim marque non vérifiable) ≤0.3

Un chiffre sans procédé de mesure (« 60k clients ») n'entre JAMAIS comme nombre nu · il porte son marqueur de fiabilité ou reste hypothèse. Là où on s'apprête à faire payer, **trianguler cross-nature** (≥2 natures dont une revealed/verbatim) · une cellule sur du structural seul reste une projection taguée.

## Les 4 conditions d'arrêt du fetch (rendement, pas couverture)

On arrête de fetcher dès qu'UNE est vraie ·

1. **Confiance-cible atteinte pour l'enjeu** · la décision qui paie est déjà tranchable, fetcher plus ne la change pas.
2. **Saturation des verbatims** · les nouvelles lectures répètent les mêmes signaux.
3. **Inconnu non-tranchable-par-scrape** · l'aiguille ne bougera pas avec plus de fetch · le TYPER avec son levier (zéro fetch de plus) et passer.
4. **Budget d'attention épuisé** · le plafond de la recon / du scan est atteint, le reste part en inconnu typé.

## Persistance · in situ, pas seulement au close

Chaque inconnu porteur + son levier s'écrit dans l'artefact **au moment où il surgit** (pas agrégé seulement au close). La carte garde son fond visible tout du long · les sections Inconnu/Leviers du close AGRÈGENT des cas déjà écrits, elles ne les inventent pas. Cf `docs/system/open-map-reasoning.md` Mécanisme 2 (inconnu typé + levier) et Mécanisme 5 (la carte s'accumule).

## Le verdict

De « crawl fixe one-shot qui couvre le site et fige une carte morte traitant tout scrapé comme un fait » à « boucle d'allocation pilotée par l'inconnu porteur, bornée par l'enjeu, qui horodate et note chaque brique par sa nature, et que des skills indépendants rafraîchissent couche par couche ». L'atlas cesse d'être un instantané, il devient une carte vivante et calibrée en confiance.
