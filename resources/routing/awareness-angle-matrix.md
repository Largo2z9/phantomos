# Awareness × Angle Matrix

> **TYPE:** Routing · logique de décision
> **CONSOMMÉ PAR:** hooks-generator, script-writer, brief-generator, creative-strategist
> **SOURCE KB:** `02-awareness-levels.md`, `02-angles-marketing.md`, `phase-5-combinatoire-creative.md`
> **DÉPEND DE:** `registries/angle-registry.md`
> **FORMAT:** Tables de routing par awareness level. L'agent lit l'awareness de l'audience, obtient les angles/lead types/tons prioritaires.

---

## Principe

Cette matrice est le **routeur principal** du système. Un agent de production reçoit une audience (avec son awareness_distribution) et doit décider quels angles, lead types et tons déployer.

**Règle fondamentale :** awareness level de l'audience = premier filtre. Tout le reste (angle, lead, ton, format) en découle.

---

## Table de routing principale

### Unaware

L'audience ne sait pas qu'elle a un problème.

| Dimension | Valeurs |
|---|---|
| **Angles primaires** | counter-intuitive, emotional-identity, transformation |
| **Angles secondaires** | community |
| **Angles à éviter** | efficiency, price-value, scarcity, urgency, barrier-removal, parasitic-positioning |
| **Lead types** | Story (primary), Prediction (secondary) |
| **Tons recommandés** | Emotional, Authentic |
| **Formats** | Shortform, Video UGC, Storytelling |
| **Mécaniques visuelles** | Storytelling, Problem Amplification, Behind the Scenes |
| **Approche** | Indirecte. Pas de mention produit dans le hook. Ouvrir la conscience du problème via narration, identité ou révélation. |

---

### Problem Aware

L'audience sait qu'elle a un problème mais ne connaît pas les solutions.

| Dimension | Valeurs |
|---|---|
| **Angles primaires** | transformation, counter-intuitive, emotional-identity |
| **Angles secondaires** | simplicity, community, innovation |
| **Angles à éviter** | scarcity, urgency, price-value, parasitic-positioning |
| **Lead types** | Problem-Solution (primary), Prediction (secondary) |
| **Tons recommandés** | Emotional, Expert |
| **Formats** | Video UGC, Shortform, Carousel |
| **Mécaniques visuelles** | Problem Amplification, Before/After, Storytelling |
| **Approche** | Agiter le problème, valider l'émotion, introduire l'espoir. Le hook nomme le problème dans le vocabulaire du prospect. |

---

### Solution Aware

L'audience sait que des solutions existent mais ne connaît pas la marque.

| Dimension | Valeurs |
|---|---|
| **Angles primaires** | efficiency, simplicity, innovation, community |
| **Angles secondaires** | transformation, expertise, counter-intuitive, parasitic-positioning |
| **Angles à éviter** | urgency (weak), scarcity (weak) |
| **Lead types** | Promise (primary), Problem-Solution (secondary), Secrets (secondary) |
| **Tons recommandés** | Expert, Casual |
| **Formats** | Video UGC, Carousel, Video VSL |
| **Mécaniques visuelles** | Side-by-Side, Result Showcase, Expert Talking Head |
| **Approche** | Différenciation. Pourquoi cette solution et pas une autre. Mechanism unique + preuves. |

---

### Product Aware

L'audience connaît le produit mais n'est pas convaincue.

| Dimension | Valeurs |
|---|---|
| **Angles primaires** | expertise, efficiency, security, price-value, barrier-removal |
| **Angles secondaires** | innovation, transformation, parasitic-positioning |
| **Angles à éviter** | emotional-identity (trop indirect), counter-intuitive (ils connaissent déjà) |
| **Lead types** | Promise autour du mechanism (primary), Offer (secondary) |
| **Tons recommandés** | Expert, Premium, Urgent |
| **Formats** | Video UGC, Carousel, Static |
| **Mécaniques visuelles** | POV/Unboxing, Expert Talking Head, Testimonial Montage, Result Showcase |
| **Approche** | Lever les dernières objections. Preuves spécifiques. Mécanisme expliqué. Risk reversal (garantie). |

---

### Most Aware

L'audience suit la marque, convaincue mais n'a pas agi.

| Dimension | Valeurs |
|---|---|
| **Angles primaires** | urgency, scarcity, price-value, barrier-removal |
| **Angles secondaires** | expertise, security, parasitic-positioning |
| **Angles à éviter** | counter-intuitive, emotional-identity, community (trop indirect) |
| **Lead types** | Offer/Invitation (primary), Promise courte (secondary) |
| **Tons recommandés** | Urgent, Premium |
| **Formats** | Static, Shortform, Carousel |
| **Mécaniques visuelles** | Result Showcase, Testimonial Montage |
| **Approche** | Ultra-direct. Offre, deadline, preuve finale. Pas de storytelling. Pas d'éducation. |

---

## Matrice croisée Audience Psychology × Awareness → Ton

Le ton dépend de la combinaison awareness + psychologie de l'audience.

| Core desire / Driver | Unaware | Problem Aware | Solution Aware | Product Aware | Most Aware |
|---|---|---|---|---|---|
| **Fear-driven** | Emotional | Emotional | Expert | Expert | Urgent |
| **Desire-driven** | Emotional | Casual | Casual | Premium | Premium |
| **Rational** | Expert | Expert | Expert | Expert | Urgent |
| **Belonging** | Authentic | Authentic | Casual | Casual | Authentic |

Source `audience.psychology.core_desire` + `audience.voice.tone_register` pour affiner.

---

## Matrice croisée Sophistication × Angle

Le niveau de sophistication du marché filtre les angles viables.

| Sophistication | Angles favorisés | Angles défavorisés | Logique |
|---|---|---|---|
| **nascent** | transformation, simplicity, efficiency | counter-intuitive, scarcity, parasitic-positioning | Marché vierge · angles directs, promesse claire. Pas besoin de paradigm shift ni de référent. |
| **growth** | transformation, innovation, community, expertise | price-value, urgency | Marché qui monte · différenciation par mechanism ou identité. |
| **mature** | counter-intuitive, expertise, security, community, parasitic-positioning | simplicity (trop basique), transformation (vu) | Marché saturé · paradigm shift, autorité, ou positionnement vs leader. |
| **saturated** | counter-intuitive, emotional-identity, scarcity, barrier-removal | efficiency, simplicity, price-value | Marché épuisé · angle radicalement différent ou levée du dernier frein. |

Source `product.market_context.sophistication`.

---

## Matrice croisée Trust Barrier × Proof Priority

| Trust barrier | Proof types prioritaires | Angle ajustement |
|---|---|---|
| **low** | social (volume suffit) | Angles desire-driven en priorité |
| **medium** | social + result | Angles standards |
| **high** | authority + transparency + trust (garantie) + result | Renforcer security, expertise. Chaque claim doit être prouvé. |

Source `product.market_context.trust_barrier`.

---

## Usage par un agent

```
1. Lire audience.market_position.awareness_distribution
2. Identifier le(s) awareness level(s) dominant(s) (> 25%)
3. Pour chaque awareness level :
   a. Consulter cette matrice → obtenir angles primaires
   b. Croiser avec sophistication → filtrer angles viables
   c. Croiser avec trust barrier → ajuster proof requirements
   d. Lire angle-registry.md pour chaque angle retenu → obtenir les hook levers, proof types, exemples
4. Si brief opérateur fixe un angle → vérifier compatibilité awareness (warning si avoid)
5. Si brief opérateur fixe un awareness → utiliser directement cette section
```

---

## Extension

Pour modifier la matrice :
1. Tester la modification sur au moins 3 combinaisons audience × produit réelles
2. Vérifier cohérence avec angle-registry.md (pas de contradiction sur les awareness ranges)
3. Documenter le raisonnement du changement

---

*Dernière mise à jour : 2026-03-16 (Session 11 · +barrier-removal, +parasitic-positioning dans routing)*
