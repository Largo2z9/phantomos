# Proof Registry

> **TYPE:** Taxonomie · registre vivant
> **CONSOMMÉ PAR:** hooks-generator, script-writer, brief-generator, creative-strategist, pattern-extractor
> **SOURCE:** Retro-engineering 522 créas statiques (10 batches, 9 brands, 6 niches)
> **DÉPEND DE:** `templates/creative-formula.md` (§5.3)
> **FORMAT:** 1 fiche taggée par type de preuve. Hiérarchie force croissante. Champs parsables par agent.

---

## Principe

- **Multi-proof stacking.** Créas persuasives = 2-4 layers. Trust barrier haute → plus de layers.
- **Hiérarchie.** Risk reversal (faible) ≠ clinical trial (maximale). L'ordre reflète la force persuasive croissante.
- **Proof ≠ Angle.** La preuve supporte l'angle, ne le remplace pas.
- **Curseur-dependent.** Curseur 0-2 → logo brand seul. Curseur 8-10 → 3-4 layers.

---

## Format fiche

```
### [#] [ID] · [Nom]
- **Force:** faible | moyenne | forte | maximale
- **Définition:** [prose, 1-2 phrases]
- **Curseur min:** [number]
- **Objection levée:** [phrase courte · ce que ça prouve]
- **Angles:** [array]
- **Stack avec:** [array · proof types souvent empilés avec]
- **Awareness:** [array · awareness levels où pertinent]
- **Conditions:** [array · tags]
- **Anti-conditions:** [array · tags]
- **Piège:** [prose, 1 phrase]
- **Batches:** [array]
```

---

## Fiches (force croissante)

### 1. risk-reversal · Garantie / Remboursement

- **Force:** faible
- **Définition:** Le prospect ne prend aucun risque financier. La marque absorbe le risque (remboursement, essai gratuit, retour).
- **Curseur min:** 4
- **Objection levée:** "Tu ne risques rien à essayer."
- **Angles:** [security, price-value, barrier-removal]
- **Stack avec:** [social-proof-number, cost-calculator]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [premiere_conversion, prix_eleve, categorie_engagement_fort]
- **Anti-conditions:** [garantie_non_competitive, audience_deja_convaincue]
- **Piège:** Trop mise en avant, la garantie signale un doute sur le produit. Garder en layer secondaire.
- **Batches:** [B01, B05]

---

### 2. badge-tech · Badge Technologique

- **Force:** faible
- **Définition:** Certification, compatibilité, ou standard tech reconnu. Badge tiers crédible (Apple, USB-C, CE) comme shortcut de confiance.
- **Curseur min:** 3
- **Objection levée:** "Certifié/compatible par [standard reconnu]."
- **Angles:** [innovation, security, expertise]
- **Stack avec:** [social-proof-number, claim-science]
- **Awareness:** [solution_aware, product_aware]
- **Conditions:** [badge_reconnu_audience, compatibilite_critere_achat, badge_differencie]
- **Anti-conditions:** [badge_inconnu, standard_generique, badge_non_pertinent]
- **Piège:** 5 badges génériques < 1 badge significatif. L'accumulation dilue.
- **Batches:** [B01]

---

### 3. best-seller-badge · Badge Best-Seller

- **Force:** moyenne
- **Définition:** Indicateur de popularité : "best-seller", "#1 en [catégorie]". Bandwagon effect.
- **Curseur min:** 3
- **Objection levée:** "Tout le monde l'achète."
- **Angles:** [community, security, price-value]
- **Stack avec:** [customer-review, social-proof-number, press-logos]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [reellement_top_vente, audience_en_comparaison, simplifie_choix]
- **Anti-conditions:** [claim_inverifiable, auto_declare_sans_source, audience_contrarian]
- **Piège:** "Best-seller" sans qualificateur = claim vide. Ajouter "#1 sur [plateforme]" ou "[période]".
- **Batches:** [B02]

---

### 4. social-proof-number · Preuve Sociale Chiffrée

- **Force:** moyenne
- **Définition:** Nombre quantifiant l'adoption · clients, avis, communauté, produits vendus. Volume = proxy qualité.
- **Curseur min:** 4
- **Objection levée:** "N personnes ont déjà fait confiance."
- **Angles:** [community, security, transformation]
- **Stack avec:** [customer-review, risk-reversal]
- **Awareness:** [problem_aware, solution_aware, product_aware]
- **Conditions:** [nombre_impressionnant_categorie, social_proof_critere_decision]
- **Anti-conditions:** [nombre_petit, nombre_gonfle, audience_expert_merite]
- **Piège:** "1M clients" sur brand inconnue = suspect. Aligner le chiffre avec la notoriété perçue.
- **Batches:** [B01, B03, B04]

---

### 5. customer-review · Avis Client Authentique

- **Force:** moyenne-forte
- **Définition:** Verbatim client réel + étoiles et/ou source vérifiable (Trustpilot, Google). Voix client > voix marque.
- **Curseur min:** 5
- **Objection levée:** "Des vrais gens comme toi ont testé et validé."
- **Angles:** [transformation, security, community]
- **Stack avec:** [social-proof-number, press-logos, best-seller-badge]
- **Awareness:** [problem_aware, solution_aware, product_aware]
- **Conditions:** [avis_specifiques_pas_generiques, source_verifiable, avis_raconte_transformation]
- **Anti-conditions:** [avis_generiques, avis_fake, source_non_verifiable]
- **Piège:** Avis trop parfait = semble fake. Garder les imperfections de langage · c'est l'authenticité.
- **Batches:** [B01, B08]

---

### 6. press-logos · Logos Presse

- **Force:** forte
- **Définition:** Logos médias reconnus comme preuve de couverture. Transfert d'autorité du média vers le produit.
- **Curseur min:** 3
- **Objection levée:** "Des médias crédibles en ont parlé."
- **Angles:** [expertise, security, innovation]
- **Stack avec:** [customer-review, claim-science, best-seller-badge]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [couverture_presse_reelle, medias_reconnus_audience, branding_ou_conviction]
- **Anti-conditions:** [medias_inconnus_audience, publiredactionnel_non_disclosed, audience_sceptique_presse]
- **Piège:** Aligner logos avec audience cible. Forbes pour business, ELLE pour beauté. Logos hors cible diluent.
- **Batches:** [B01, B02, B09]

---

### 7. claim-science · Claim Scientifique Non Attribué

- **Force:** forte
- **Définition:** Affirmation scientifique sans attribution : "clinically proven", "testé dermatologiquement". Aura scientifique sans source.
- **Curseur min:** 5
- **Objection levée:** "C'est prouvé scientifiquement."
- **Angles:** [expertise, innovation, security]
- **Stack avec:** [social-proof-number, clinical-trial, press-logos]
- **Awareness:** [solution_aware, product_aware]
- **Conditions:** [base_scientifique_reelle, audience_non_sophistiquee, espace_limite]
- **Anti-conditions:** [zero_base_scientifique, audience_sophistiquee, risque_reglementaire, claim_exagere]
- **Piège:** Gap énorme entre "clinically proven" (non attribué) et "proven at [institut]" (attribué). Toujours upgrader si possible.
- **Batches:** [B03, B09]

---

### 8. cost-calculator · Démonstration Mathématique

- **Force:** forte
- **Définition:** Calcul explicite montrant économie/valeur · prix barré, coût/jour, comparaison annuelle. Le chiffre persuade.
- **Curseur min:** 7
- **Objection levée:** "Fais le calcul toi-même · objectivement un bon deal."
- **Angles:** [price-value, efficiency, parasitic-positioning]
- **Stack avec:** [risk-reversal, social-proof-number, parasitic-positioning]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [economie_reelle_significative, calcul_simple_verifiable, audience_rationnelle]
- **Anti-conditions:** [calcul_trompeur, positionnement_premium, economie_insignifiante]
- **Piège:** Le calcul doit résister à 5 secondes de réflexion critique. Si déconstruit mentalement → effet inversé.
- **Batches:** [B05]

---

### 9. celebrity-endorsement · Endorsement Célébrité

- **Force:** forte
- **Définition:** Personnalité connue recommande/utilise le produit. Capital confiance/admiration transféré au produit.
- **Curseur min:** 5
- **Objection levée:** "[Personne admirée] utilise ce produit."
- **Angles:** [expertise, community, emotional-identity]
- **Stack avec:** [press-logos, social-proof-number, clinical-trial]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [association_authentique, audience_admire, endorsement_reel]
- **Anti-conditions:** [association_artificielle, celebrite_controversee, audience_sceptique_endorsement, budget_insuffisant]
- **Piège:** Celebrity fatigue · 15 endorsements = 0 crédibilité. Exclusivité catégorielle renforce. Demi-vie courte.
- **Batches:** [B04, B05]

---

### 10. press-quote · Citation Presse Verbatim

- **Force:** très forte
- **Définition:** Citation complète d'un article, mot pour mot. Plus fort que logos seuls · le contenu éditorial spécifique crédibilise.
- **Curseur min:** 7
- **Objection levée:** "Un journaliste a écrit EXACTEMENT ça."
- **Angles:** [expertise, security, innovation]
- **Stack avec:** [press-logos, clinical-trial, best-seller-badge]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [citation_elogieuse_specifique, media_reconnu, citation_porte_seule]
- **Anti-conditions:** [citation_fade, citation_tronquee, media_non_reconnu]
- **Piège:** Citation cherry-picked hors contexte = bombe à retardement si le prospect vérifie l'article original.
- **Batches:** [B09]

---

### 11. parasitic-positioning · Positionnement Parasitaire

- **Force:** très forte
- **Définition:** Se positionner comme alternative/generic d'un category leader connu. Le référent fait le travail d'éducation.
- **Curseur min:** 7
- **Objection levée:** "Tu connais [leader]. Même chose, mieux/moins cher."
- **Angles:** [parasitic-positioning, price-value, efficiency]
- **Stack avec:** [cost-calculator, clinical-trial, risk-reversal]
- **Awareness:** [solution_aware, product_aware, most_aware]
- **Conditions:** [category_leader_universel, equivalent_demonstrable, audience_price_sensitive]
- **Anti-conditions:** [aucun_referent_connu, produit_fondamentalement_different, risque_legal, referent_mauvaise_reputation]
- **Piège:** Ancre le produit dans l'ombre du leader. Si le leader innove ou change de catégorie, le parasite perd son ancrage.
- **Batches:** [B09]

---

### 12. clinical-trial · Essai Clinique Attribué

- **Force:** maximale
- **Définition:** Essai clinique spécifique avec attribution · institut, méthodologie, statistique. Preuve scientifique la plus forte en créa.
- **Curseur min:** 7
- **Objection levée:** "[Institut crédible] a prouvé que ça marche, avec des chiffres."
- **Angles:** [expertise, security, innovation, efficiency]
- **Stack avec:** [press-logos, claim-science, social-proof-number]
- **Awareness:** [solution_aware, product_aware]
- **Conditions:** [essai_reel_methodologie_solide, resultat_significatif, audience_sophistiquee, trust_barrier_haute]
- **Anti-conditions:** [essai_biaise, statistique_trompeuse, audience_non_scientifique]
- **Piège:** "Cliniquement prouvé" ≠ essai attribué. L'attribution (institut + n= + stat) fait toute la différence.
- **Batches:** [B04]

---

### 13. sponsoring-disclosure · Disclosure Partenariat

- **Force:** maximale (paradoxale)
- **Définition:** Mention explicite contenu sponsorisé. Paradoxe : la transparence renforce la crédibilité au lieu de la détruire.
- **Curseur min:** 5
- **Objection levée:** "On est transparent · si on le montre, c'est qu'on est confiant."
- **Angles:** [security, community, expertise]
- **Stack avec:** [customer-review, social-proof-number]
- **Awareness:** [problem_aware, solution_aware, product_aware]
- **Conditions:** [ugc_sponsorise, obligation_legale_eu_fr, transparence_differenciateur]
- **Anti-conditions:** [contenu_non_sponsorise, disclosure_casse_flow]
- **Piège:** Trop grosse → "ils vendent". Trop petite → non-compliance. Intégrer naturellement (badge discret).
- **Batches:** [B08]

---

### 14. regulatory-disclaimer · Disclaimer Réglementaire

- **Force:** maximale (paradoxale)
- **Définition:** Mention légale obligatoire (FDA, "Rx required", "Results not typical"). La contrainte légale peut renforcer la perception de sérieux.
- **Curseur min:** 7
- **Objection levée:** "Régulé = assez sérieux pour avoir des règles."
- **Angles:** [security, expertise, barrier-removal]
- **Stack avec:** [clinical-trial, press-quote, customer-review]
- **Awareness:** [product_aware, most_aware]
- **Conditions:** [obligation_legale, disclaimer_signal_categorie]
- **Anti-conditions:** [aucune_obligation, disclaimer_volontaire_sans_contrepartie]
- **Piège:** Consomme 10-20% espace créa. Anticiper dans le layout. Ni cacher ni surdimensionner.
- **Batches:** [B09]

---

## Patterns de stacking

### Par trust barrier

| Trust barrier | Layers | Combo type |
|---|---|---|
| **low** | 1-2 | logo brand + best-seller |
| **medium** | 2-3 | social-proof-number + customer-review + press-logos |
| **high** | 3-4 | clinical-trial + press-logos + customer-review + risk-reversal |
| **regulated** | 3-4 + regulatory | clinical-trial + press-quote + social-proof + regulatory-disclaimer |

### Par awareness level

| Awareness | Proof prioritaires | Logique |
|---|---|---|
| **Unaware** | (minimal) | Pas encore conscient du problème. |
| **Problem Aware** | social-proof-number, customer-review | "D'autres comme toi ont résolu ce problème." |
| **Solution Aware** | clinical-trial, press-logos, claim-science | "Pourquoi cette solution est meilleure." |
| **Product Aware** | customer-review, risk-reversal, cost-calculator | "Achète en confiance." |
| **Most Aware** | risk-reversal, cost-calculator, best-seller | "Le deal. Zéro risque." |

---

## Extension

1. Fiche au format taggé ci-dessus
2. Placer dans la hiérarchie (comparer force persuasive)
3. Test chevauchement types existants
4. Valider ≥ 2 batches ou ≥ 5 créas
5. Ajouter dans `creative-formula.md` §5.3
6. Mettre à jour patterns de stacking si applicable

---

*Dernière mise à jour : 2026-03-17 (Session 11 · 14 fiches taggées, hiérarchisées)*
