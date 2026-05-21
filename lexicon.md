# Lexicon opérateur

Vocabulaire métier user-facing pour opérateurs DTC paid. Termes classiques que vous utilisez déjà au quotidien.

## Workspace agentic

Le workspace PhantomOS lui-même · un dossier de fichiers (brands, resources, skills, docs) que l'agent lit et écrit à chaque session. Contraste avec un chatbot dont la mémoire vit dans le thread. Ici la mémoire vit sur disque · l'agent la consulte avant chaque réponse.

## Skill

Capacité exécutable de l'agent · cartographier une audience, produire un angle paid, auditer un compte Meta. L'agent reconnaît votre demande en langage naturel et mobilise la bonne capacité. Le catalogue est navigable via `/skills`.

## Porte d'entrée

Une des quatre options proposées au démarrage de `/tour` selon votre intention (explication guidée, configurer une marque maintenant, importer ce qui existe déjà, ou juste explorer). Chaque porte route vers un livrable par défaut adapté à l'intention choisie.

## Brand

Votre marque encodée dans PhantomOS. Identité, contacts, finances, concurrents. Stockée dans `brands/{slug}/brand.json`.

## Produit

Ce que la marque vend. Composition, mécanisme, claims, problème adressé, prix. Référence dans toutes les opérations paid.

## Offre

Comment un produit est présenté commercialement (prix, bundle, gifting, subscription, refill). Plusieurs offres possibles par produit.

## Audience

Cible identifiée pour la marque. Profil psychographique, pains, bénéfices, jobs to be done. Sourcée par observation (verbatims, reviews, threads) ou inférence.

## Persona

Alias surface opérateur de l'audience canon. Toléré en mode parlé, avec sous-rôles buyer/user quand split (B2B, cadeau, pet, kids).

## Pain point

Problème observable subi par l'audience. Visible dans les verbatims clients. Propriété de l'audience (owned natif sub-collection `audiences/{slug}/pain_points/PNT-NN.json` canon v2.64 ontologie sémantique pure) · pas dimension orthogonale de composition créative. Référencé par `angle.lineage.pain_ref`. Cf `compositional-cartography.md` v3.1 · le pain vit dans la couche CONTEXTE de la formule de composition créative (via angle).

## Tension

Gap entre état actuel et état désiré de l'audience.

## Insight

Vérité non-dite que la cible pense mais n'a jamais entendue formulée. Distinct de pain point (problème observable) et de tension (gap).

## JTBD

Job To Be Done. Job que la cible "embauche" le produit pour accomplir (framework Christensen).

## Angle

Axe d'attaque marketing. Composé via la formule Observation × Tension × Reframe × Bridge. Origine typée (audience · produit · catégorie · brand · culturel-temporel). Porte un lineage compositionnel · `audience_ref` + `pain_ref` (pain dominant sub-audience) + `mechanism_ref` (spec produit activée) + `awareness_movement` (entry → exit Schwartz). Cf `compositional-cartography.md` v3.1 · l'angle vit dans la couche CONTEXTE de la formule de composition créative.

## Axe créatif

Cellule au croisement audience × angle. Output de `score-matrix` (top-3 axes priorisés). Candidat à matérialiser en brief + creatives. Distinct du territoire (substrat macro).

## Concept, Creative, Variant

Concept = objet intent persuasive (audience × insight × angle × mécanique), stable. Creative = instance déployée d'un concept (un fichier). Variant = creative du même concept avec 1-2 variables changées.

## Mécanique (creative)

Device narratif d'une créa (testimonial, before-after, demo, comparison, statement, curiosity). Distinct de Mechanism (spec).

## Mechanism (spec)

Chaîne causale entre une spec produit et un bénéfice (ex. KSM-66 → réduction cortisol).

## Awareness stage

Niveau de conscience de l'audience (Eugene Schwartz) · unaware · problem-aware · solution-aware · product-aware · most-aware. Vit à deux endroits canon · `audience.psychology.market_position.awareness_level` (snapshot où l'audience est globalement) ET `angle.awareness_movement` (entry_stage → exit_stage · où l'angle prend l'audience et l'amène). Pas une dimension orthogonale de composition créative · corrélée à l'audience (cf `canonical-matrix-reasoning.md` activation sélective).

## Atome irréductible

Élément (mot, image, structure) sans lequel l'ad meurt. Test · si vous le retirez ou le changez, mesure-t-on un delta de performance ?

## Landing page

Page d'atterrissage du trafic paid. Variantes · advertorial (entrée par la voix audience, pivot produit à 50% scroll) · comparative (vs concurrents) · capture (lead magnet) · classique (PDP enrichie).

## Campagne

Structure paid sur une plateforme (Meta, TikTok, Google Ads). Contient ad sets (audiences) et ads (creatives). Track par budget, perf, objectif.

## Test

Hypothèse instanciée pour validation. Format · hypothèse, métrique, sample minimum, durée, règle de décision.

## Résultat

Sortie chiffrée d'un test. Métrique mesurée (CTR, CR, ROAS, CAC, LTV), valeur observée, baseline, delta. Statut · validé · invalidé · inconcluant · fatigué.

## Apprentissage

Fait opérationnel append-only retenu d'un test ou d'une opération. Réutilisable cross-marques pour densifier la stratégie.

## Positioning

Position de la marque sur le marché. Antagoniste explicite (contre quoi vous vous définissez), promesse distinctive, point de vue catégorie. Inclut voice et ton.

## Territoire

Substrat stable de la marque · ce qui survit aux sessions (specs produits, audiences, angles, frictions, roadmap, strategy, apprentissages cumulés). Posé une fois en setup (semaine 1), enrichi marginalement ensuite. Distinct de la production runtime (briefs, creatives qui changent chaque semaine).

## Connected source

Plateforme externe connectée à PhantomOS pour rapatrier data ou pousser des assets. Catégories · paid ads (Meta, TikTok, Google Ads) · analytics (GA4, Shopify) · e-commerce (Shopify, Stripe) · email/SMS (Klaviyo, Postscript) · attribution (TripleWhale, Northbeam) · creative intelligence (Atria, Foreplay).

---

*Dernière mise à jour · 2026-05-20.*
