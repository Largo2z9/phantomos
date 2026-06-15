# phantom-mode · spectrum-drill (`/phantom {brand} spectre`)

> Vue READ-ONLY de la carte du terrain produit × marché (le Spectre). Lit le singleton `brands/{slug}/spectrum.json`, ne l'écrit jamais. Produit par `map-angles` mode spectre (via le palier de `build-atlas-complete` ou un refresh à la demande). Canon C7 · D#502/D#506.

## Hard rule render-first

Rendre la carte EN TEXTE d'abord, intégralement. Le drill footer fait partie du rendu, en texte. AskUserQuestion admis UNIQUEMENT après le rendu complet et seulement si une décision est réellement ouverte. Jamais substituer le rendu par un widget de navigation.

## Précondition

`brands/{slug}/spectrum.json` existe. S'il est absent · une seule ligne · *"Pas encore de carte du spectre pour {brand}. Je peux la construire (mécanisme → usages → audiences → terrain), ça prend quelques minutes. On la lance ?"* → si oui, route `map-angles` mode spectre (qui exige `spec.use_cases[]` peuplé, donc `map-audiences` mode spectre d'abord si vide). Ne PAS fabriquer une carte vide.

## Lecture

Charger `spectrum.json`. **Mode de groupement NOMINAL en v1.0 · par `coverage_self`** (covered / partial / blank). En v1.0 la couverture concurrente (`coverage_market`) n'est pas encore alimentée (pont watch-competitors différé), donc `strategic_position` (battlefield / our-advantage / proxy-validated / whitespace) est **null partout** · ne pas le présenter comme l'axe principal tant qu'il l'est. Il deviendra le groupement quand la veille remplira `coverage_market` (v1.1). Marquer le cœur via `core_cell_ref` (top-level) avec ★. Pour les `coverage_self: blank`, surfacer `blank_qualification` (opportunity / cemetery / desert / unqualified) et le `lever`.

## Rendu (posture d'investigation, langage opérateur)

Table ASCII calquée sur matrix-drill · une ligne par cellule · colonnes : ce que ça sert (use_case label) · à qui (audience ou « grain usage » si null) · toi (coverage_self) · le marché (coverage_market, souvent inconnu tant que la veille n'a pas tourné) · lecture (strategic_position ou la qualification de la zone blanche). Le cœur de cible (★) en évidence.

Puis 4 sections courtes :
- **Observé** · les cellules couvertes et celles prouvées (evidence solide).
- **Déduit** · les cellules adjacentes / hypothèses, avec leur évidence typée (comportementale / voix client / VoM / structurelle).
- **Inconnu** · les zones blanches non qualifiées, leur `lever` nommé (jamais inventer si ça paie).
- **Leviers** · ce qui lèverait les inconnues (qualifier une zone blanche, scraper la concurrence pour remplir la couverture marché).
- **Close ouvert** · UNE question macro, l'opérateur arbitre où creuser.

**Fraîcheur honnête** · afficher `refreshed_at` et `stage_at_build`. Si la carte est ancienne (> 1 mois), le dire en une ligne et proposer un refresh.

**Frontière** · rappeler en une phrase si pertinent · cette carte montre l'étendue du jouable, elle ne décide pas le spend · la priorisation (top-3, budget) c'est `/phantom {brand} matrix` (score-matrix), un objet séparé (D#502).

## Action refresh (paste-ready, read-only ici)

Le drill ne mute pas. Le refresh est une action proposée · *"Rafraîchir la carte (re-croiser usages × audiences × sources, re-qualifier les zones blanches) ?"* → route `map-angles` mode spectre en scope partiel (brownfield-merge par `cell_id`, ne réécrit pas les cellules `validated`).

## AskUserQuestion (après rendu seulement, si décision ouverte)

Slots typiques · slot 1 « Qualifie les zones blanches » (route la vérification VoC + claim + éco) · « Rafraîchir la carte » · « Passe à la priorisation » (`/phantom {brand} matrix`) · « Rien, je regarde ».

## Anti-patterns

- Écrire dans `spectrum.json` depuis ce drill (read-only strict · le refresh route map-angles).
- Présenter la carte comme un plan de bataille (c'est l'étendue, pas la décision).
- Fabriquer des cellules ou une couverture marché non observée (`coverage_market: unknown` reste unknown tant que la veille n'a pas tourné).
- Exposer les noms de skills / champs JSON en surface opérateur.
