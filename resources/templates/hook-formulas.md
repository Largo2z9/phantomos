# Hook Formulas

> **TYPE:** Templates · structures output
> **CONSOMMÉ PAR:** hooks-generator (primary), script-writer, creative-strategist
> **SOURCE KB:** `02-angles-marketing.md` (Hook Testing), `phase-6-output.md` (Hooks Library), `03-copywriting-structures.md`
> **DÉPEND DE:** `registries/angle-registry.md` (pour les hook levers par angle)
> **FORMAT:** 1 fiche par catégorie de hook. Chaque fiche = formula (slots à remplir) + levier psy + quand utiliser + exemples.

---

## Principe

Un hook = les 3 premières secondes (vidéo) ou la première ligne (texte). 80% du job de conversion.

**3 composants d'un hook performant :**
1. **Pattern Interrupt** · casse le scroll / la lecture passive
2. **Open Loop** · ouvre une boucle mentale (curiosité non résolue)
3. **Identification** · le prospect se reconnaît ("c'est de moi qu'on parle")

**3 leviers psychologiques (testables séparément) :**
- **Fear** · perte, menace, conséquence négative
- **Desire** · gain, transformation, aspiration
- **Rational** · logique, preuve, curiosité intellectuelle

---

## Catégories de hook

### question · Question

**Mécanique :** Pose une question que le prospect se pose déjà (ou devrait se poser). Crée identification + open loop.

**Formula :**
```
"[Question que le prospect se pose] ?"
"Pourquoi [symptôme/problème observable] ?"
"Tu savais que [fait surprenant sous forme de question] ?"
```

**Lever dominant :** fear ou rational (selon la question)

**Awareness range :** problem_aware → solution_aware

**Quand utiliser :** Audience consciente du problème. La question doit nommer un symptôme dans le vocabulaire exact du prospect (`audience.voice.vocabulary_to_use`).

**Quand NE PAS utiliser :** Unaware (elle ne comprend pas la question). Most Aware (elle connaît déjà la réponse).

**Exemples :**
- "Pourquoi tes cheveux tombent plus depuis ton accouchement ?"
- "Tu savais que la biotine seule ne suffit pas contre la chute ?"
- "Combien de touffes sur ton oreiller ce matin ?"

---

### statement · Statement choquant

**Mécanique :** Affirmation contre-intuitive qui brise une croyance. Pattern interrupt maximal.

**Formula :**
```
"[Ce que tout le monde croit] [VERBE CHOC : aggrave / détruit / est un mensonge]"
"[Solution perçue comme bonne] est [la vraie cause du problème]"
"Arrête de [action courante] · ça [conséquence inattendue]"
```

**Lever dominant :** rational (curiosité) + fear (menace)

**Awareness range :** unaware → problem_aware → solution_aware

**Quand utiliser :** Marché sophistiqué (growth+). Insight prouvable. Audience sceptique des solutions classiques.

**Quand NE PAS utiliser :** Claim non prouvable. Audience Most Aware (clickbait). Produit sans vrai paradigm shift.

**Exemples :**
- "Les shampoings anti-chute AGGRAVENT ta chute de cheveux."
- "Ce n'est pas le stress qui te fait perdre tes cheveux."
- "Arrête les masques capillaires · ils ne traitent pas la cause."

---

### before-after · Before/After

**Mécanique :** Contraste temporel entre l'état de douleur (avant) et l'état transformé (après). Projection + social proof.

**Formula :**
```
"Il y a [durée] je [état de douleur]. Aujourd'hui [état transformé]."
"Avant [produit/solution] : [symptôme]. Après : [résultat]."
"[Durée] de différence. [Résultat visible]."
```

**Lever dominant :** desire (transformation)

**Awareness range :** problem_aware → solution_aware → product_aware

**Quand utiliser :** Produit avec résultat visible/mesurable (`market_context.demonstrability` = visible ou felt). Proofs before/after disponibles.

**Quand NE PAS utiliser :** Aucun résultat prouvable. Produit intangible sans transformation observable.

**Exemples :**
- "Il y a 3 mois je perdais des touffes. Aujourd'hui mes cheveux ont doublé de volume."
- "Janvier : je n'osais plus attacher mes cheveux. Avril : regarde ça."
- "3 mois de Glow Boost. Le miroir ne ment pas."

---

### statistic · Statistique

**Mécanique :** Chiffre précis (pas rond) qui surprend. Crédibilité + curiosité.

**Formula :**
```
"[Chiffre précis]% des [population cible] [fait surprenant]"
"[Chiffre] [unité] · c'est [comparaison qui donne l'échelle]"
"Sur [base], [chiffre] [résultat]"
```

**Lever dominant :** rational

**Awareness range :** problem_aware → solution_aware → product_aware

**Quand utiliser :** Stat réelle et sourcée (`product.proofs.performance.quantifiable_results`). Chiffre qui surprend ou qui met à l'échelle.

**Quand NE PAS utiliser :** Stat inventée ou arrondie ("plus de 90%"). Audience unaware (pas de contexte pour interpréter le chiffre).

**Exemples :**
- "78% des femmes post-partum perdent leurs cheveux · et le cachent."
- "92% de satisfaction. 10 000+ utilisatrices. 4.7/5."
- "Repousse visible pour 78% des utilisatrices à 3 mois."

---

### confession · Confession

**Mécanique :** Vulnérabilité authentique. Crée connexion émotionnelle + identification.

**Formula :**
```
"J'ai [émotion vulnérable] quand [moment de vie douloureux]."
"Je n'osais plus [action quotidienne] parce que [conséquence honteuse]."
"Personne ne sait que je [secret honteux lié au problème]."
```

**Lever dominant :** fear (honte, vulnérabilité) → desire (espoir)

**Awareness range :** problem_aware (primary), unaware (secondary · via empathie)

**Quand utiliser :** Produit qui touche à l'identité/confiance en soi. Audience avec forte charge émotionnelle (`audience.psychology.emotions` = honte, frustration, anxiété). Format UGC/témoignage.

**Quand NE PAS utiliser :** Produit utilitaire sans composante émotionnelle. Audience rationnelle pure. Risk de manipulation émotionnelle disproportionnée.

**Exemples :**
- "Je pleure sous la douche en voyant ce qui reste dans mes mains."
- "J'ai arrêté de me regarder dans le miroir le matin."
- "Mon mari m'a dit que c'était dans ma tête · mais je VOIS la différence."

---

### callout · Call-out

**Mécanique :** Interpelle directement la cible. Identification immédiate.

**Formula :**
```
"Si tu [situation spécifique de la cible], [impératif]."
"[Groupe identitaire] · [message direct]."
"Toi qui [comportement/symptôme], [promesse]."
```

**Lever dominant :** fear ou desire (selon la suite)

**Awareness range :** problem_aware → solution_aware

**Quand utiliser :** Audience bien définie avec des marqueurs identitaires forts. Le call-out filtre naturellement (seule la cible se reconnaît).

**Quand NE PAS utiliser :** Audience trop large (le call-out ne filtre rien). Unaware (ne se reconnaît pas encore).

**Exemples :**
- "Si tu perds tes cheveux depuis ton accouchement, écoute ça."
- "Femmes aux cheveux texturés · arrêtez de croire que c'est génétique."
- "Toi qui as tout essayé contre la chute · sauf ça."

---

### revelation · Révélation

**Mécanique :** Info cachée ou méconnue. Open loop maximal.

**Formula :**
```
"Ce que [autorité/source crédible] ne te dit pas sur [sujet]."
"Le secret derrière [résultat enviable]."
"Il y a une raison pour laquelle [phénomène observable] · et c'est pas celle que tu crois."
```

**Lever dominant :** rational (curiosité), fear (menace cachée)

**Awareness range :** unaware → problem_aware → solution_aware

**Quand utiliser :** Vrai insight à révéler (mechanism unique, cause racine méconnue). Marché sophistiqué où l'approche directe est saturée.

**Quand NE PAS utiliser :** Pas de vraie révélation (clickbait). Most Aware (ils savent déjà). Le "secret" est en fait banal.

**Exemples :**
- "Ce que ton dermato ne te dit pas sur la chute de cheveux post-partum."
- "La vraie raison pour laquelle tes cheveux ne repoussent pas."
- "Le secret des femmes qui ont retrouvé leur volume en 3 mois."

---

### analogie · Analogie

**Mécanique :** Fait externe surprenant (nature, science, culture pop) utilisé comme tremplin vers le produit. Pattern interrupt maximal via le décalage.

**Formula :**
```
"[Fait surprenant externe]. [Bridge vers le produit/prospect]."
"[Sujet externe] [capacité impressionnante]. [Prospect] [incapacité contrastée]."
```

**Lever dominant :** rational (curiosité) + desire (aspiration)

**Awareness range :** unaware → problem_aware → solution_aware

**Quand utiliser :** Marché saturé où les hooks directs sont épuisés. Audience sensible à l'humour ou au décalage. Le bridge analogie→produit est immédiat (pas besoin d'explication).

**Quand NE PAS utiliser :** Le bridge est forcé ou confus. Audience ultra-rationnelle (B2B technique). Le décalage fait perdre de la crédibilité.

**Exemples :**
- "This bear smells a seal through 3 feet of ice. You've lost your wallet 4 times this week."
- "Un saumon remonte 1000 km à contre-courant. Tu arrives pas à te lever sans 3 cafés."
- "Un bébé reconnaît sa mère à l'odeur en 48h. Tu reconnais pas ton propre shampooing."

---

### triptyque · Triptyque rhétorique

**Mécanique :** 3 affirmations en parallélisme syntaxique. Rythme + mémorabilité + escalade.

**Formula :**
```
"[Affirmation 1]. [Affirmation 2]. [Affirmation 3 (twist ou climax)]."
"[Verbe 1]. [Verbe 2]. [Verbe 3]."
```

**Lever dominant :** rational (structure) + desire (progression)

**Awareness range :** solution_aware → product_aware → most_aware

**Quand utiliser :** Annonces upgrade/launch. Brand statements. Copy qui doit sonner comme un slogan mémorable.

**Quand NE PAS utiliser :** Audience unaware (le triptyque assume de la familiarité). Sujet qui nécessite nuance (le triptyque est assertif).

**Exemples :**
- "Better Formula. Better Flavors. Same Price."
- "We Listened. We Upgraded. We Delivered."
- "One Heart. Two Cards. Zero Panic."

---

### storytelling · Storytelling / Mini-arc narratif

**Mécanique :** Micro-récit avec personnage + setup + twist. Ouvre une boucle narrative que le scroll ne peut pas fermer.

**Formula :**
```
"[Personnage] [setup (succès ou situation)]. [Twist inattendu (conséquence cachée)]."
"[État initial]. Then [événement qui change tout]."
```

**Lever dominant :** fear (twist) → desire (résolution)

**Awareness range :** problem_aware → solution_aware

**Quand utiliser :** Produit avec transformation démontrable. Pain point avec conséquence cachée (effets secondaires, coût caché). Audience qui bypass les hooks directs (sophistication élevée).

**Quand NE PAS utiliser :** Produit sans arc narratif naturel. Audience Most Aware (veut le deal, pas l'histoire).

**Exemples :**
- "She Lost 40 Pounds on Her GLP-1. Then Her Hairdresser Asked What Was Wrong."
- "Felt Slower Every Year. Then I Didn't."
- "Burnout Felt Endless. This Gave Me Relief."

---

### faux-dilemme · Faux dilemme / False trade-off

**Mécanique :** Pose un trade-off que le prospect accepte comme inévitable, puis le rejette. "Tu ne devrais pas choisir."

**Formula :**
```
"You shouldn't have to choose between [bénéfice A] or [conséquence B]."
"[Bénéfice A] SANS [sacrifice B]."
"Pourquoi choisir entre [X] et [Y] ?"
```

**Lever dominant :** desire (avoir les deux) + fear (le trade-off actuel)

**Awareness range :** problem_aware → solution_aware

**Quand utiliser :** Le prospect subit un trade-off réel (efficacité vs effets secondaires, résultat vs confort). Le produit élimine ce trade-off.

**Quand NE PAS utiliser :** Le trade-off n'existe pas réellement dans l'esprit du prospect. Le produit ne résout pas vraiment les deux côtés.

**Exemples :**
- "You Shouldn't Have to Choose Between Losing Weight or Losing Your Hair."
- "Performance sans les effets secondaires."
- "Résultats cliniques. Zéro compromis sur le goût."

---

### escalade-numerique · Escalade numérique

**Mécanique :** Accumulation de chiffres en séquence croissante ou impressionnante. Effet cascade.

**Formula :**
```
"[Chiffre 1 input]. [Chiffre 2 composants]. [Chiffre 3 résultat]."
"[Stat 1]%. [Stat 2]%. [Stat 3]%."
"[Chiffre extrême]% More [composant]."
```

**Lever dominant :** rational (data) + desire (résultat quantifié)

**Awareness range :** solution_aware → product_aware → most_aware

**Quand utiliser :** Produit avec données chiffrées multiples. Audience data-driven. Formulation upgrade (733% More B12).

**Quand NE PAS utiliser :** Chiffres inventés ou arrondis. Audience émotionnelle pure. Trop de chiffres = confusion.

**Exemples :**
- "2 Gummies. 11 Vitamines. 4 cm par mois."
- "90% moins cassant. 90% plus fort. 95% résultats visibles."
- "733% More B12. +50% MSM. +67% D3. +150% K2."

---

### expectation-subversion · Subversion d'attente

**Mécanique :** Commence par NIER le bénéfice attendu, puis AMPLIFIE avec un bénéfice supérieur. "PAS X... mais Y (mieux)."

**Formula :**
```
"Ceci ne va PAS [bénéfice attendu]... Mais [bénéfice supérieur]."
"Ce n'est pas [ce que vous pensez]. C'est [mieux]."
```

**Lever dominant :** rational (curiosité, pattern interrupt) → desire (amplification)

**Awareness range :** problem_aware → solution_aware

**Quand utiliser :** Le produit dépasse les attentes de la catégorie. Le prospect a des attentes calibrées sur la concurrence (basse barre).

**Quand NE PAS utiliser :** Le bénéfice supérieur n'est pas crédible. L'audience risque de décrocher à la négation.

**Exemples :**
- "Ceci ne va PAS transformer juste votre nuit... Mais vos vies."
- "Ce n'est pas un shampoing. C'est un traitement."
- "Don't expect better sleep. Expect a better life."

---

### direct-benefit · Bénéfice direct (ultra-bold)

**Mécanique :** Le bénéfice EST le hook. 2-5 mots, zéro device rhétorique, zéro euphémisme. Le prospect sait EXACTEMENT ce qu'il obtient.

**Formula :**
```
"[Bénéfice en 2-5 mots]."
"[Verbe impératif] [résultat]."
```

**Lever dominant :** desire (bénéfice brut)

**Awareness range :** solution_aware → product_aware → most_aware

**Quand utiliser :** Pain point universellement compris (pas besoin d'éduquer). Tabou (le nommer = acte de courage/destigmatisation). Urgence haute. Product-market fit évident.

**Quand NE PAS utiliser :** Pain point qui nécessite éducation (unaware). Produit dont le bénéfice est complexe ou indirect. Marché où la directness est mal perçue.

**Exemples :**
- "Get hard."
- "Stronger erections."
- "Regrow hair ASAP."
- "Better sex life."

---

### double-entendre · Double sens / Wordplay

**Mécanique :** Mot ou phrase avec 2 niveaux de lecture : sens littéral (bénéfice produit) + sens figuré (innuendo, humour, complicité). Le prospect "comprend" les 2.

**Formula :**
```
"[Mot/phrase à double sens] [contexte qui active les 2 lectures]."
```

**Lever dominant :** desire (complicité) + rational (mémorabilité)

**Awareness range :** solution_aware → product_aware → most_aware

**Quand utiliser :** Catégorie intime/tabou où le double sens est naturel (ED, sexualité, body). Audience qui apprécie l'humour implicite. Brand ton bold/provocateur.

**Quand NE PAS utiliser :** Audience sensible qui pourrait être offensée. Catégorie où l'humour détruit la crédibilité (cancer, urgence médicale). Le double sens est forcé.

**Exemples :**
- "Get hard results." (hard = érection + résultats)
- "Finish after she does." (finish = orgasme + complétion)
- "Rise to the occasion." (rise = érection + relever le défi)

---

## Combinaisons de catégories

Un hook peut combiner 2 catégories (ex: confession→revelation) si :
1. Le hook démarre par la mécanique de la catégorie primaire
2. La catégorie secondaire intervient en résolution (pas en introduction)
3. Les deux catégories ciblent le même awareness range (pas de conflit)
4. Le hook reste < 2 phrases (pas de mini-script)

**Notation :** `catégorie_primaire→catégorie_secondaire` (ex: `confession→revelation`)

---

## Levier psychologique : primaire et secondaire

Chaque hook a un **levier primaire** (dominant) et un **levier secondaire** optionnel.

- **Primaire :** le levier qui lance le hook (ex: fear ouvre la boucle)
- **Secondaire :** le levier qui résout ou complète (ex: desire referme avec espoir)
- **Notation :** `primaire→secondaire` (ex: `fear→desire`)
- **Combinaisons courantes :** fear→desire (douleur + espoir), rational→fear (curiosité + menace), fear→rational (menace + preuve)
- **Règle :** le levier primaire doit être compatible avec l'angle (cf. `angle-registry.md` → hook lever)

---

## Awareness Match · test explicite

Un hook **passe** le test Awareness Match si :
- L'awareness level ciblé est dans le `awareness range` documenté de la catégorie de hook
- L'angle utilisé n'est **pas** dans la colonne "avoid" de la matrice pour ce level

Un hook **échoue** le test si :
- L'awareness level ciblé est hors du range de la catégorie (ex: question pour unaware)
- L'angle est dans "avoid" pour ce level ET l'opérateur n'a pas overridé

---

## Règles de génération

- **Min 10 hooks par audience primaire.** Variance de test minimale.
- **Couverture 3 leviers :** au moins 3 fear + 3 desire + 3 rational par audience.
- **Vocabulaire prospect obligatoire.** Chaque hook utilise au moins 1 expression de `audience.voice.vocabulary_to_use` ou `audience.voice.key_expressions`.
- **Pas de hook générique.** Le hook doit être spécifique au produit × audience × awareness. Test : remplacer par un concurrent → si ça marche encore, c'est trop générique.
- **Test d'arrêt de scroll.** Lire à voix haute. Si pas "attends, c'est quoi ça ?" → rejeter.
- **Respecter l'awareness.** Un hook question pour unaware = inefficace. Un hook confession pour most_aware = hors sujet.

---

## Scoring hooks

→ Critères de qualité, tests de validation, et seuils définis dans **`quality-specs/hook-quality-spec.md`**.

---

## Extension

Pour ajouter une catégorie de hook :
1. Identifier la mécanique psychologique distincte (pas un doublon d'une catégorie existante)
2. Documenter : formula, lever, awareness range, quand/quand pas, 3+ exemples
3. Tester sur au moins 2 audiences différentes

---

## Spectre de persuasion textuelle

Le hook n'est pas binaire (présent/absent). C'est un spectre. De la persuasion la plus faible à la plus forte :

1. **Category label** ("NOS VESTES") → navigation pure, curseur 0-2
2. **Feature tag** ("Ultra doux") → information pure, curseur 2-3
3. **Catchphrase** ("Track smarter") → positionnement, curseur 3-5
4. **Hook mécanique** (question, stat, accusation) → persuasion moyenne, curseur 5-7
5. **Hook narratif** (storytelling, faux dilemme, expectation subversion) → persuasion forte, curseur 7-8
6. **Hook ultra-direct** (direct benefit, double entendre) → persuasion maximale, curseur 9-10

Le niveau de persuasion est corrélé au curseur texte/visual de la niche (cf. `creative-formula.md` §3).

---

*Dernière mise à jour : 2026-03-16 (Session 10 · V3, 15 hook patterns)*
