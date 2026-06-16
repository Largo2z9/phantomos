# Hook Quality Spec

> **TYPE:** Quality Spec · critères d'évaluation pour hooks
> **CONSOMMÉ PAR:** hooks-generator (Step 5), script-writer (validation input), creative-strategist (audit)
> **DÉPEND DE:** `registries/angle-registry.md`, `routing/awareness-angle-matrix.md`, `templates/hook-formulas.md`
> **FORMAT:** Critères binaires (passe/échoue), scoring pondéré, seuils de passage.

---

## Critères de scoring

Chaque hook est évalué sur 5 critères binaires (0 ou 1).

| # | Critère | Poids | Test binaire | Méthode de vérification |
|---|---|---|---|---|
| 1 | **Pattern Interrupt** | 25% | Le hook casse le scroll / arrête la lecture passive ? | Lecture à voix haute. Si pas de "attends, c'est quoi ça ?" → échoue. |
| 2 | **Identification** | 25% | Le prospect se dit "c'est moi" / "c'est mon problème" ? | Le hook contient au moins 1 marqueur identitaire de l'audience (vocabulaire, situation, life moment). |
| 3 | **Open Loop** | 20% | Le lecteur veut la suite ? Curiosité non résolue ? | Le hook pose une question implicite ou explicite qui reste sans réponse. |
| 4 | **Spécificité** | 15% | Chiffres précis, vocabulaire prospect, pas de générique ? | Au moins 1 donnée spécifique de la DB (chiffre produit, expression audience, moment de vie). Pas de placeholder. |
| 5 | **Awareness Match** | 15% | Cohérent avec le niveau de conscience ciblé ? | L'awareness level ciblé est dans le range documenté de la catégorie de hook (cf. hook-formulas.md) ET l'angle n'est pas dans "avoid" (cf. awareness-matrix.md). |

---

## Seuil de passage

- **Minimum : 4/5 critères passés.** En dessous → retravailler ou rejeter.
- Un hook à 3/5 peut être retravaillé (1 itération max). À 2/5 ou moins → rejet définitif.

---

## Tests de validation complémentaires

### Test de substitution (anti-générique)

Remplacer le nom du produit par un concurrent direct. Si le hook fonctionne encore → trop générique → rejet.

**Tolérance :** un hook peut être "category-level" (fonctionne pour la catégorie produit) s'il est dans un batch qui contient au moins 60% de hooks "brand-level" (spécifiques à la marque). Pas l'inverse.

### Test vocabulaire prospect

Chaque hook DOIT contenir au moins 1 mot ou expression de :
- `audience.voice.vocabulary_to_use`
- `audience.voice.key_expressions`
- `audience.psychology.life_moments` (pour confession/before-after)

**Échec = rejet.** Pas de hook en langage marketing · en langage prospect.

### Test awareness compliance

Vérifications croisées avec les shared resources :

| Vérification | Source | Conséquence si échoue |
|---|---|---|
| L'angle est-il dans "avoid" pour cet awareness ? | `awareness-angle-matrix.md` | Rejet (sauf override opérateur explicite) |
| La catégorie de hook est-elle hors range awareness ? | `hook-formulas.md` → awareness range | Rejet |
| L'angle a-t-il ≥ 2 proof types disponibles dans la DB ? | `angle-registry.md` → proof types vs `product.proofs` | Warning (pas rejet · l'angle reste utilisable mais noter le manque dans la méta-analyse) |

### Test claims

Tout chiffre, stat, ou affirmation factuelle dans un hook doit être traçable à :
- `product.proofs.performance.quantifiable_results`
- `product.proofs.social.*`
- `product.proofs.authority.*`

**Chiffre non sourcé = rejet.** Pas de stats inventées, pas d'arrondis trompeurs.

---

## Couverture minimale (par audience)

| Dimension | Minimum | Logique |
|---|---|---|
| Hooks total | 10 (ou `quantity` du brief) | Variance de test minimale |
| Catégories de hook | 3 différentes | Diversité de mécanique |
| Leviers psychologiques | 2 différents (fear + desire OU desire + rational) | Diversité de registre émotionnel |
| Angles | 2 différents (sauf brief fixe 1 angle) | Diversité de perspective |

**En dessous des minimums → méta-analyse flag le gap + raison.**

---

## Méta-analyse obligatoire

Chaque hooks-library doit inclure une section méta-analyse avec :

- Hooks générés vs validés (count + ratio)
- Angles déployés (count par angle)
- Leviers (count par lever)
- Catégories couvertes (count par catégorie)
- Catégories sous-représentées (+ raison)
- Gaps identifiés (angles/catégories/audiences non couverts + raison)
- Hooks rejetés (count + raisons principales)
- Warnings (proof coverage insuffisante, awareness borderline, etc.)

---

## Extension

Pour modifier les critères de scoring :
1. Justifier pourquoi le critère actuel est insuffisant (cas concret)
2. Proposer le nouveau critère au format binaire (question oui/non vérifiable)
3. Valider sur au moins 10 hooks existants (pas de régression)
4. Mettre à jour le poids si nécessaire (total = 100%)

---

*Dernière mise à jour : 2026-03-16 (Session 9)*
