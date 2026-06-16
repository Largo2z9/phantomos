# Creative Formula V3 · Formule de décomposition créative

> **TYPE:** Template · structure maître
> **CONSOMMÉ PAR:** tous les agents creative (hooks-generator, script-writer, brief-generator, creative-strategist, pattern-extractor)
> **SOURCE:** Retro-engineering de 522 créas statiques (10 batches, 9 brands, 6 niches)
> **DÉPEND DE:** `registries/angle-registry.md`, `templates/hook-formulas.md`, `registries/creative-mechanics-registry.md`, `registries/proof-registry.md`
> **FORMAT:** Architecture en couches + curseur modal. Ce doc est la SPEC · les registres détaillent chaque composant.

---

## 1. Le problème que V3 résout

La V2 `(mécanique · format · angle · pain_point · persona · ton) ^ stop_scroller(hook, visual)` a été stress-testée sur un échantillon de 522 créas statiques (10 batches, 9 brands, 6 niches). Trois classes de problème ont émergé :

- **Claim niches** (supplements, tech, telehealth) : la formule fonctionne mais il manque des dimensions (proof, offer, occasion, destination, produit, mix)
- **Visual niches** (fashion, lifestyle) : la formule collapse · hook, angle, pain point disparaissent quand le visual porte seul la persuasion
- **Assets catalogue** (DPA/DABA) : la formule est inapplicable · ce ne sont pas des créas au sens persuasif

V3 résout ces 3 problèmes via :
1. Un **curseur texte/visual** qui module les composants obligatoires
2. Une **architecture 3 couches** (Noyau / Contexte / Modifieurs) avec optionalité par couche
3. Un **classificateur de production** qui distingue Concept vs Template vs Asset

> **⚠️ Limite d'échantillon.** L'architecture V3 est solide (elle résout les 79 frictions identifiées). Mais les patterns par niche (curseur, mécaniques dominantes, ratios) sont des **hypothèses basées sur 522 créas / 9 brands**. Il faudrait significativement plus de data pour affirmer des lois par niche. Les observations spécifiques aux brands de l'échantillon sont isolées dans l'Annexe A.

> **Stress test S55 (mai 2026, 23 ads cross-typologies).** La V3 a été stress-testée sur 23 ads diverses (cosméto, telehealth, apparel, supplément, kids gear, B2B SaaS, info-product, DTC fashion). 10 patches affinants identifiés sans refonte structurelle. La V3 tient. Patches intégrés : modalité insight (formulé / implicite / absent), intent 4 valeurs (DR · Brand · Hybrid · B2B_lead_gen), seasonality_trigger metadata, craft_mode (product_only / with_overlay), longevity_signal (days_running > reach absolu comme proxy winner), cta modalité 4 valeurs (explicite · implicite_brand · absent_intentionnel · externalisé). Voir `decisions.md D#391` pour la trace empirique.

---

## 2. Classificateur de production (AVANT la formule)

Avant de décomposer une créa, déterminer son **mode de production**. Chaque mode active un sous-ensemble de la formule.

| Mode | Définition | Formule applicable |
|---|---|---|
| **CONCEPT** | Créa avec intention persuasive. Un humain a choisi un angle, un hook, un device. | Formule V3 complète |
| **TEMPLATE** | Créa issue d'un gabarit rigide. Le "concept" = le choix du template + la photo + la catégorie. | Formule réduite : template_type + visual + ton + [modifieurs] |
| **ASSET** | Photo produit sans intention persuasive. Sert le catalogue dynamique (DPA/DABA). | Hors formule. Classification par attributs visuels : modèle, contexte, styling, product_form |

**Test de classification :**
1. Y a-t-il un hook textuel (tension, promesse, question, stat) ? → OUI = CONCEPT, NON = continuer
2. Y a-t-il un template identifiable (layout fixe réutilisé N fois) ? → OUI = TEMPLATE, NON = continuer
3. Y a-t-il du texte au-delà du logo ? → OUI = TEMPLATE minimal, NON = ASSET

**Ratio concept/template/asset par brand** = indicateur stratégique. Hypothèse à valider sur plus de data : le ratio est corrélé à la brand equity (plus la marque est connue, plus les assets suffisent) et au funnel stage dominant.

---

## 3. Curseur Texte/Visual (0-10)

Le curseur détermine quels composants de la formule sont **obligatoires**, **optionnels**, ou **inapplicables** pour une créa donnée.

Le curseur est évalué **par créa** (pas par niche). Mais en pratique, les créas d'une même brand/niche gravitent autour d'une zone du spectre. Encodé brand-side dans `brand.json#creative_zone {min, max, dominant}` après N créas décomposées.

```
0 ─────── 2 ─────── 5 ─────── 7 ─────── 10
VISUAL                                    COPY
PUR                                       PUR

assets       templates    copy standard     copy max
catalogue    fashion      supplements       pain solver
DPA/DABA     retail       tech, skincare    pharma, tabou
```

### Impact sur les composants

| Composant | Curseur 0-2 (visual) | Curseur 3-5 (hybride) | Curseur 6-8 (copy) | Curseur 9-10 (copy max) |
|---|---|---|---|---|
| **hook** | N/A | Feature tag / Category label | Hook mécanique (question, stat, accusation) | Hook ultra-direct (benefit, double entendre) |
| **angle** | N/A | Saison/Occasion = angle primary | Angle stratégique (1 primary + 1 secondary) | Angle stratégique + angle proof intégré |
| **pain_point** | N/A | Besoin fonctionnel implicite | Pain point explicite | Pain point tabou, nommé sans filtre |
| **mécanique** | Packshot / Lifestyle | Template-based | Concept-based (diagnostic, versus, UGC...) | Concept-based (direct benefit, press quote...) |
| **stop_scroller** | Visual seul (corps, enfant, styling) | Visual dominant + badge/tag | Hook + visual co-dominants | Hook dominant, visual = support |
| **proof** | Logo brand = seul proof | Prix, badge attribut | 2-3 proof layers | 3-4 proof layers + regulatory |
| **ton** | Stable (seul composant universel) | Stable | Stable | Stable |

---

## 4. Architecture 3 couches

### Équation maître V3

```
CREATIVE = NOYAU(mécanique × format × stop_scroller(hook_layer, visual_layer) × ton)
        × CONTEXTE(angle[primary, secondary?] × pain_point × persona[type, buyer≠user?] × proof[layers])
        × MODIFIEURS(occasion · situation · offer · destination · produit · mix_pillar · campaign · regulatory · variant_of)
```

### COUCHE 1 · NOYAU (toujours présent, mais contenu variable selon curseur)

```
CREATIVE = mécanique × format × stop_scroller(hook_layer, visual_layer) × ton
```

| Composant | Définition | Obligatoire |
|---|---|---|
| **mécanique** | Comment la créa est construite. Le device structural. | TOUJOURS (mais le type change : concept / template / asset) |
| **format** | Statique, vidéo, carrousel, story, collection. | TOUJOURS |
| **stop_scroller** | Ce qui arrête le scroll. Binôme hook (texte) + visual. | TOUJOURS (mais le ratio hook/visual glisse avec le curseur) |
| **ton** | La voix. Comment on dit les choses. | TOUJOURS (seul composant stable 0→10) |

### COUCHE 2 · CONTEXTE STRATÉGIQUE (présent sur les CONCEPTS, partiel sur TEMPLATES, absent sur ASSETS)

```
× angle(primary, [secondary]) × pain_point × persona(type, [buyer≠user]) × proof(layers[])
```

| Composant | Définition | Obligatoire si CONCEPT | Obligatoire si TEMPLATE |
|---|---|---|---|
| **angle** | Perspective psychologique. POURQUOI cette créa devrait résonner. | OUI (primary + optional secondary) | PARTIEL (saison/occasion peut être l'angle) |
| **pain_point** | Le problème du prospect. | OUI (sauf promo/brand/launch = optionnel) | NON (besoin fonctionnel implicite) |
| **persona** | À qui on parle. Démographique ou condition-based. | OUI | OUI (mais souvent buyer ≠ user) |
| **proof** | Couches de crédibilité empilées. | OUI (min 1 layer) | PARTIEL (badge, prix) |

### COUCHE 3 · MODIFIEURS (optionnels, multiplicateurs contextuels)

```
× [occasion] × [offer] × [destination] × [produit] × [mix] × [campaign] × [regulatory] × [variant_of]
```

| Modifieur | Définition | Quand présent |
|---|---|---|
| **occasion** | Moment calendaire ou culturel (Valentine, New Year, Ramadan, Black Friday) | Campagnes saisonnières |
| **situation** | Trigger contextuel evergreen (travel, post-workout, morning routine) | Ciblage par usage |
| **offer** | Le deal (% off, free kit, bundle, prix club, prix primary) | Créas à objectif conversion |
| **destination** | Où la créa envoie (product page, quiz/diagnostic, collection, LP, article) | Toujours (mais invisible dans le visual) |
| **produit** | Quel produit/gamme ciblé (mono vs multi-produit) | Brands multi-produit |
| **mix / content_pillar** | Orientation : Produit / Pain Point / Brand / Promotion | Classification stratégique |
| **campaign** | Narrative partagée par N créas (launch campaign, seasonal push) | Quand N créas servent 1 message |
| **regulatory** | Contrainte légale (disclaimer FDA, prescription, paid testimonial, sponsoring disclosure) | Pharma, health claims, EU transparency |
| **variant_of** | Concept parent (même concept, 1-2 variables changées : photo, promo, hook swap) | Testing/déclinaison |
| **product_line_color** | Code couleur par gamme produit | Brands multi-produit avec système couleur |
| **brand_equity_level** | low (besoin hook/angle/proof) → high (logo suffit) | Détermine le curseur |

### §4.4 Patches v3.1 intégrés (issus stress test S55)

10 patches affinants absorbés dans le canon V3 sans refonte structurelle. Source empirique : 23 ads cross-typologies (S55, mai 2026). Encodés dans `creative.schema.json` (en cours) et `angle.schema.json` v1.2.

| Patch | Couche | Définition | Modalités |
|---|---|---|---|
| **intent** | Concept-level | Tag qui module la fractale Hook × Body × CTA. Mode persuasif global de la créa. | DR (direct response) · Brand · Hybrid · B2B_lead_gen |
| **insight (modalité)** | Concept (couche distincte) | Vérité non-dite verbalisée. À distinguer de pain_point (problème observable subi), tension (gap actuel/désiré) et jtbd (job hiré au produit). Quatre plans MECE (clarification doctrinaire issue audit nomenclature S55). | formulé · implicite · absent |
| **seasonality_trigger** | Concept (metadata temporelle) | Override d'occasion si déclencheur calendrier brand-spécifique (drop, anniversaire brand, fenêtre rituelle interne). | string · null |
| **craft_mode** | Execution (Craft.Verbal) | Mode catalog photo muet vs avec overlay textuel. Module les obligatoires Craft.Verbal. | product_only · with_overlay |
| **longevity_signal** | Performance (proxy winner) | Signal perf empirique. >30 jours = winner evergreen. Meilleur que reach absolu (qui corrèle avec budget plus que mérite intrinsèque). | days_running (int) + winner_proxy enum |
| **cta (modalité)** | Execution (couche CTA) | Reconnaissance que ~80% du paid social externalise le CTA. La modalité prime sur la formulation. | explicite (CTA verbal in-creative) · implicite_brand (brand recognition fait CTA) · absent_intentionnel (Brand-led statement) · externalisé (CTA délégué plateforme/funnel) |

**Doctrine MECE des couches concept** (clarification S55) :
- **pain_point** = problème observable subi par la cible
- **tension** = gap entre état actuel et état désiré
- **insight** = vérité non-dite verbalisée par la créa
- **jtbd** = job hiré au produit (progress)

Ces quatre plans sont distincts. Une créa peut activer 1 à 4 plans simultanément. Confondre insight et pain_point = erreur fréquente détectée S55.

---

## 5. Registres associés (détail dans fichiers dédiés)

### 5.1 Mécaniques créatives (registry SSOT)

→ `registries/creative-mechanics-registry.md` (25-29 mécaniques canon, registry = SSOT)

**Cross-ref schemas.** `angle.schema.json` v1.2 et `creative.schema.json` (en cours) pointent vers le registry par id (free string), pas enum hardcodé. Ne pas dupliquer la liste dans les schemas.

**Claim niches (curseur 5-10) :**

| ID | Mécanique | Batches source |
|---|---|---|
| versus | Comparaison produit/concurrent/workaround | B01, B05, B08 |
| diagnostic | Quiz/symptom check, CTA "faire le test" | B02, B05 |
| ugc | User Generated Content (5 sous-types) | B03, B05, B08 |
| celebrity | Endorsement par personnalité connue | B04, B05 |
| launch-narrative | Annonce upgrade/nouveau produit, souvent en série | B01, B02, B04, B05, B08 |
| offer-breakdown | Déballage structuré de l'offre (free kit, welcome kit) | B05, B08 |
| before-after | Contraste avant/après (visuel, émotionnel, 2 ou 3+ étapes) | B02, B03, B09 |
| testimonial-quote | Voix client + visual brand (hybride UGC/brand) | B05, B08 |
| cost-calculator | Démonstration mathématique de la valeur ($290→$89) | B05 |
| analogie | Élément externe surprenant bridgé vers le produit | B01 |
| trending-fake-natif | Simule contenu éditorial/natif (Notes, Safari, Story, Google, Trend) | B01, B02, B05, B06, B08 |
| direct-benefit | Le bénéfice EST le hook, zéro device ("Get hard") | B09 |
| press-quote | Citation presse verbatim = concept entier | B09 |
| format-menu | Présentation des options de format produit ("Treat. Pop. Drop.") | B09 |
| price-primary | Le prix EST toute la créa, zéro autre élément | B09 |
| diagnostic-service | Le produit = un test/screening, pas un traitement | B09 |
| founder-chat | Conversation simulée fondateur-client | B08 |
| recipe-instructions | Mode d'emploi/recette comme ad | B08 |
| bundle-duo | Regroupement de produits avec structure (jour/nuit, his/hers) | B01, B08 |
| curiosity_teaser | Hook accusateur + visuel-preuve + payoff externalisé via swipe | B-S55 |
| emotional_reframe | Ladder de futurs possibles (distinct meme_cultural et statement) | B-S55 |
| meme_cultural | Référence culturelle/meme bridgée vers le produit | B-S55 |
| educational_diagram | Diagramme/schéma pédagogique comme device principal | B-S55 |

**Visual niches (curseur 0-4) :**

| ID | Mécanique | Batches source |
|---|---|---|
| category-showcase | Template : photo + "NOS X" + badge + packshots | B06 |
| collection | Univers thématique (nom + palette + motifs) justifiant N produits | B06 |
| season-campaign | Photo extérieur + slogan saison + CTA | B06 |
| loyalty-campaign | Photo + nom campagne + prix club fidélité | B06 |
| guide-listicle | Titre + checklist + fake search bar | B06 |
| packshot-solo | 1 modèle, fond studio, produit porté, logo seul | B07 |
| packshot-contextuel | 1 modèle en contexte d'usage (gym, outdoor), logo seul | B07 |
| squad-group | 3-5 modèles ensemble, communauté visible | B07 |
| ugc-selfie | Selfie miroir, zéro texte, authenticité du format = message | B07 |

### 5.2 Hook patterns (15 identifiés)

→ Mise à jour de `templates/hook-formulas.md`

| ID | Pattern | Device | Batches |
|---|---|---|---|
| question | Question que le prospect se pose | Identification + open loop | B01, B02, B08 |
| statement | Affirmation contre-intuitive | Pattern interrupt | B02 |
| before-after | Contraste temporel état douleur/transformé | Projection | B02, B03, B09 |
| statistic | Chiffre précis qui surprend | Crédibilité + curiosité | B03 |
| confession | Vulnérabilité authentique | Connexion émotionnelle | B03 |
| callout | Interpelle directement la cible | Identification immédiate | B02 |
| revelation | Info cachée ou méconnue | Open loop maximal | B01, B02 |
| analogie | Fait externe surprenant bridgé au produit | Pattern interrupt + bridge | B01 |
| triptyque | 3 affirmations en parallélisme ("Better. Better. Same.") | Rythme + mémorabilité | B01, B04, B05 |
| storytelling | Mini-arc narratif (personnage + setup + twist) | Cliffhanger | B05 |
| faux-dilemme | "Tu ne devrais pas choisir entre X et Y" | Rejet du trade-off | B05 |
| escalade-numerique | Accumulation de chiffres croissants | Cascade persuasive | B03, B05 |
| expectation-subversion | "PAS X... mais Y (mieux)" | Nier puis amplifier | B08 |
| direct-benefit | Le bénéfice en 2-5 mots, zéro device | Ultra-directness | B09 |
| double-entendre | Wordplay à double sens (littéral + figuré) | Complicité + mémorabilité | B09 |

**Spectre de persuasion textuelle (du plus faible au plus fort) :**
1. Category label ("NOS VESTES") → navigation pure
2. Feature tag ("Ultra doux") → information pure
3. Catchphrase ("Track smarter") → positionnement
4. Hook mécanique (question, stat, accusation) → persuasion moyenne
5. Hook narratif (storytelling, faux dilemme, expectation subversion) → persuasion forte
6. Hook ultra-direct (direct benefit, double entendre) → persuasion maximale

### 5.3 Proof types (14 identifiés, hiérarchisés)

→ `registries/proof-registry.md` ✅ (14 fiches hiérarchisées · S11)

Du plus faible au plus fort :

| # | Type | Exemple | Batches |
|---|---|---|---|
| 1 | Risk reversal | "100 Days Free Return", "Satisfait ou remboursé" | B01, B05 |
| 2 | Badge tech | "Works with Apple Find My" | B01 |
| 3 | Best-seller badge | "Best-seller" | B02 |
| 4 | Social proof number | "60,000 femmes", "10,000+ reviews" | B01, B03, B04 |
| 5 | Customer review | ★★★★★ + verbatim Trustpilot | B01, B08 |
| 6 | Press logos | Forbes, ELLE, GRAZIA, COSMO, VOGUE | B01, B02, B09 |
| 7 | Claim science non attribué | "Validée par la science", "Clinically proven" | B03, B09 |
| 8 | Cost calculator | Math du deal ($290→$89) | B05 |
| 9 | Celebrity endorsement | Personnalité connue utilise/recommande le produit | B04, B05 |
| 10 | Press quote verbatim | Citation presse complète = concept créatif | B09 |
| 11 | Parasitic positioning | "Generic for [leader]", "X% cheaper than [référent]" | B09 |
| 12 | Clinical trial attribué | Institut + méthodologie + stat | B04 |
| 13 | Sponsoring disclosure | "Produits offerts, sans obligation" (paradoxe : renforce crédibilité) | B08 |
| 14 | Regulatory disclaimer | FDA, Prescription required, Paid testimonial | B09 |

**Pattern : multi-proof stacking.** Les créas les plus persuasives empilent 2-4 layers. Dans les niches à contrainte réglementaire, le regulatory s'ajoute en plus des layers persuasives.

### 5.4 Angles stratégiques (14 identifiés)

→ Mise à jour de `registries/angle-registry.md`

12 existants + 2 nouveaux :

| ID | Angle | Source |
|---|---|---|
| efficiency | Efficacité / Performance | KB + B01-B09 |
| simplicity | Simplicité / Accessibilité | KB + B01-B09 |
| price-value | Prix / Valeur | KB + B01-B09 |
| innovation | Innovation / Technologie | KB + B01-B05 |
| expertise | Expertise / Autorité | KB + B01-B09 |
| transformation | Transformation / Résultat | KB + B01-B09 |
| security | Sécurité / Confiance | KB + B01-B09 |
| community | Communauté / Appartenance | KB + B01-B07 |
| scarcity | Rareté / Exclusivité | KB + B01, B08 |
| urgency | Urgence / Opportunité | KB + B01, B05, B08 |
| counter-intuitive | Contre-Intuitif / Révélation | KB + B01, B02 |
| emotional-identity | Émotionnel / Identitaire | KB + B01, B08 |
| **barrier-removal** | **Levée de frein ("sans l'obstacle")** | **B09** |
| **parasitic-positioning** | **Positionnement adossé à un référent connu** | **B09** |

**Règles :**
- 1 angle primary + 1 secondary max par créa (70/30)
- 30% des créas ont 2+ angles (confirmé B01-B09)
- En fashion (curseur 0-4), l'angle peut être absent ou = saison/occasion

### 5.5 Sous-types UGC (hiérarchie d'authenticité perçue)

| # | Sous-type | Authenticité | Exemple |
|---|---|---|---|
| 1 | UGC Selfie/Mirror | ★★★★★ | Photo client brute, zéro texte |
| 2 | UGC Story Repost | ★★★★☆ | Screenshot story IG + commentaire informel |
| 3 | UGC Conversationnel Q&A | ★★★★☆ | Dialogue question follower → réponse détaillée |
| 4 | UGC Founder | ★★★☆☆ | Fondatrice en mode casual, ton personnel |
| 5 | Founder-Client Chat | ★★★☆☆ | Conversation simulée fondateur ↔ client(e) |
| 6 | Testimonial Quote + Brand Visual | ★★☆☆☆ | Voix client, image contrôlée brand |
| 7 | Avis client citation | ★★☆☆☆ | Verbatim encadré dans design brand |

### 5.6 Fake natif (sous-types)

| # | Sous-type | Format mimé |
|---|---|---|
| 1 | Format app | Notes iPhone, Safari browser bar |
| 2 | Format social | Story IG, Tweet, DM |
| 3 | Format trend/meme | Wishlist/Buylist, "POV:", "Nobody:" |
| 4 | Format editorial | Article presse, trending post |
| 5 | Format search | Barre recherche Google |
| 6 | Format whiteboard | Écriture manuscrite sur tableau |

---

## 6. Formule V3 · Notation complète

### Mode CONCEPT (curseur 5-10)

```
CREATIVE(concept) =
  NOYAU(mécanique, format, stop_scroller(hook[pattern, lever], visual[mechanic]), ton)
  × CONTEXTE(angle[primary, secondary?], pain_point?, persona[type, buyer≠user?], proof[layer1, layer2?, ...])
  × MODIFIEURS([occasion], [situation], [offer], [destination], [produit], [mix], [campaign], [regulatory], [variant_of])
```

### Mode TEMPLATE (curseur 2-4)

```
CREATIVE(template) =
  NOYAU(template_type, format, stop_scroller(visual[mechanic], [feature_tag | category_label]), ton)
  × CONTEXTE?(persona[buyer≠user?], [besoin_fonctionnel], [badge_attribut], [prix | prix_club])
  × MODIFIEURS([occasion], [saison], [collection], [produit], [variant_of])
```

### Mode ASSET (curseur 0-1)

```
ASSET =
  ATTRIBUTS(modèle[genre, morphologie, ethnicité], contexte[studio | gym | outdoor | lifestyle],
            produit[catégorie, couleur, fit], brand_signal[logo, colorway])
```

---

## 7. Patterns de production transversaux

### 7.1 Variant testing

1 concept → N variantes avec 1-2 variables changées :
- **Photo swap** : même hook, même layout, photo différente
- **Promo toggle** : même créa ± sticker promo
- **Hook swap** : même visual, hook différent
- **Background swap** : même hook + produit, fond différent
- **Split test persona** : même avatar, N hooks testant des angles différents

Le concept parent a un `concept_id`. Chaque variant porte `variant_of: concept_id` + le paramètre changé.

### 7.2 Campagne / Série narrative

N créas servent 1 message sous N angles. Patterns observés : launch campaign (N créas, N angles d'un même upgrade), seasonal push (N créas autour d'une occasion), multi-hook testing (même catégorie produit, test de hooks).

Attribut `campaign: {id, narrative, role_in_campaign}`.

### 7.3 Multi-proof stacking

Les créas les plus persuasives empilent les layers :
- 1 layer : baseline (logo, badge)
- 2 layers : standard (social proof + claim science)
- 3 layers : fort (press + testimonial + best-seller)
- 4 layers : maximum (ex : Trustpilot + science + novelty + accessibility)
- + regulatory : obligatoire quand la niche l'impose (pharma, health claims)

---

## 8. Dimensions spéciales

### 8.1 Persona · dual (buyer ≠ user)

Quand applicable (enfant, pet, cadeau, B2B) :
- **Buyer** : qui paye (parent, propriétaire, décideur)
- **User** : qui utilise (enfant, animal, utilisateur)
- La créa doit séduire le buyer. Le user apparaît dans le visual comme déclencheur émotionnel.

### 8.2 Persona · condition-based vs démographique

| Type | Quand | Exemple |
|---|---|---|
| Démographique | Tech, lifestyle | "homme 30-50, tech-savvy" |
| Condition-based | Santé, beauté | "peau rosacée", "chute de cheveux" |
| Psychographique | Premium, identitaire | "performance seeker", "aspirationnel fitness" |

### 8.3 Occasion vs Situation

| Type | Nature | Planifiable | Exemples |
|---|---|---|---|
| **Occasion** calendaire universelle | Temporel | OUI (calendrier marketing) | New Year, Valentine, Black Friday, summer |
| **Occasion** calendaire culturelle | Temporel + culturel | OUI (mais ciblage spécifique) | Ramadan, Diwali, Lunar New Year |
| **Occasion** personnelle | Temporel + individuel | NON (trigger data) | Anniversaire, naissance, mariage |
| **Situation** contextuelle | Evergreen | NON (audience targeting) | Travel, post-workout, morning routine, maternité |

### 8.4 Contraintes réglementaires

| Niveau | Contrainte | Impact créa | Niches |
|---|---|---|---|
| none | Aucune obligation | 100% espace libre | Fashion, tech, lifestyle |
| disclaimer | Mention légale obligatoire | 5-10% espace consommé | Supplements, claims "clinically proven" |
| sponsored | Disclosure partenariat | Badge + mention transparence | UGC sponsorisé (EU) |
| prescription | Rx required + FDA disclaimer | 15-20% espace consommé | Pharma, telehealth |
| paid_testimonial | "Results not typical" + "Paid testimonial" | Empilé sur BA/testimonial | Pharma BA, sponsored UGC |

---

## 9. Validation

La formule V3 a été testée sur les 10 batches de l'échantillon. Chaque batch a pu être entièrement décomposé via l'un des 3 modes (CONCEPT, TEMPLATE, ASSET). Aucune créa n'est restée "hors formule" sans explication.

Critère de validation : pour chaque créa de l'échantillon, la formule V3 peut (a) la classifier dans un mode, (b) la décomposer dans tous les composants applicables, (c) identifier ses registres.

Les résultats détaillés par batch sont dans `sandbox/batch-XX/retro-engineering-analysis.md`.

---

## 10 · Test atomique (atome irréductible)

Pour chaque créa décomposée, identifier l'atome irréductible : l'élément (mot, image, structure) sans lequel l'ad meurt. Test : "si je retire/change cet atome, mesure-t-on un delta de performance ?"

Exemples observés S55 :
- hers Rx Minoxidil Hair Gummy : le mot "Gummy" juxtaposé à "Rx Minoxidil". Si remplacé par "Tablet" l'angle s'effondre.
- BTB DAYS : "refuses des oui". Si remplacé par "n'as pas le budget" l'identitaire s'efface.
- Glowco GlowBoost : la cascade visuelle 3 flacons mirroring la timeline 3 mois.

L'atome irréductible n'est pas toujours verbal. Il peut être : un mot, une structure compositionnelle, un focal point visuel, un chiffre, une juxtaposition, un ordre. Encodé dans `creative.schema.json#atome_irréductible {element, delta_si_changé}`.

---

## 11. Extension

Pour enrichir la formule :
1. Identifier une friction (composant manquant, classement impossible, ambiguïté)
2. Vérifier sur ≥ 2 batches (pas un artefact d'une seule brand)
3. Classer : NOYAU (universel) / CONTEXTE (stratégique) / MODIFIEUR (optionnel)
4. Ajouter dans le registre approprié avec fiche complète
5. Vérifier que la formule V3 reste cohérente (pas de conflit avec composants existants)

---

## 12. Frictions résolues par V3 (79 total)

### Résolues par le classificateur de production (3 modes)
- F41 (formula collapse TAO), F42 (angle/PP absent fashion), F43 (template-based), F51 (DPA/DABA), F54 (brand comme seul signifiant), F56 (ratio assets/creatives)

### Résolues par le curseur texte/visual
- F45 (badge attribut comme substitut hook), F52 (stop scroller = corps), F15 (packshot/brand = formule vide)

### Résolues par l'ajout de composants manquants
- F1 (double angle → primary/secondary), F2 (pain point optionnel), F3 (occasion → modifieur), F6 (proof → couche contexte), F7 (offer → modifieur), F10 (mix/content pillar → modifieur), F11 (destination → modifieur), F17 (produit → modifieur), F69 (regulatory → modifieur), F71 (product line color → modifieur)

### Résolues par les registres enrichis
- F4 (analogie), F5 (trending/fake natif), F8 (hook analogie), F9 (ton journalistique), F12 (diagnostic/quiz), F13 (symptom close-up), F14 (hook templates), F16 (persona condition), F18 (multi-proof stacking), F19 (ton UGC founder), F20 (UGC testimonial), F21 (timeline), F22 (BA émotionnel), F23 (escalade numérique), F24 (claim science), F25 (celebrity endorsement), F26 (companion positioning), F27 (launch narrative), F28 (triptyque), F29 (clinical trial), F30 (visual aesthetic), F31 (offer breakdown), F32 (testimonial quote ≠ UGC), F33 (cost calculator), F34 (storytelling hook), F35 (situation ≠ occasion), F36 (variant testing), F37 (celebrity dans offre), F38 (faux dilemme), F39 (Notes app fake natif), F40 (stat shock), F44 (buyer ≠ user), F46 (collection), F47 (saison/météo), F48 (prix club), F49 (fake search bar), F50 (duplicates), F53 (UGC selfie), F55 (Ramadan cultural), F57 (UGC conversationnel), F58 (versus workaround), F59 (fake natif trend/meme), F60 (founder-client chat), F61 (expectation subversion), F62 (thumbnail vidéo), F63 (recette/instructions), F64 (identité/ton comme hook), F65 (disclosure sponsoring), F66 (multi-proof stacking extrême), F67 (direct benefit ultra-bold), F68 (double entendre), F70 (produit hero 3D), F72 (prix comme concept entier), F73 (BA 3 étapes), F74 (format menu), F75 (press quote = créa entière), F76 (diagnostic service), F77 (parasitic positioning), F78 (split test persona), F79 (barrier removal hook)

### Statut : 79/79 frictions adressées

---

---

## ANNEXE A · Observations échantillon (hypothèses, pas règles)

> **⚠️ Cette annexe documente des patterns observés sur un échantillon limité (522 créas, 9 brands, 6 niches). Ce sont des HYPOTHÈSES à valider avec plus de data · pas des lois par niche. Les noms de brands sont des références internes aux batches du sandbox, pas des vérités universelles sur ces brands.**

### A.1 Curseur observé par batch

| Batch | Niche | Mode observé | Curseur estimé |
|---|---|---|---|
| B01 | Tech tracker | CONCEPT | ~7 |
| B02 | Skincare naturel | CONCEPT | ~7 |
| B03 | Supplements beauté | CONCEPT | ~6 |
| B04-B05 | Nutrition premium | CONCEPT | ~8 |
| B06 | Mode enfant | TEMPLATE | ~2 |
| B07 | Fitness apparel | ASSET (~88%) | ~0 |
| B08 | Supplements bien-être | CONCEPT | ~7 |
| B09-B10 | Telehealth DTC | CONCEPT | ~9 |

### A.2 Hypothèses à valider (need more data)

- **H1 : les pain solvers (tabou, urgence haute) gravitent vers curseur 8-10.** Observé sur 1 brand telehealth (111 créas). Besoin de plus de brands pain solver pour confirmer.
- **H2 : la fashion retail gravite vers curseur 0-3.** Observé sur 2 brands (29 + 133 créas). Besoin de plus de brands fashion pour distinguer fast fashion vs premium vs luxury.
- **H3 : le ratio concept/asset est corrélé à la brand equity.** Observé qualitativement. Aucune mesure de brand equity dans l'échantillon.
- **H4 : chaque brand a 1-2 mécaniques "core" qui dominent >40% de son output.** Observé sur 9/9 brands. Pattern robuste mais besoin de confirmer sur des brands avec plus de volume créatif.
- **H5 : le multi-proof stacking atteint 4+ layers sur les niches à trust barrier haute.** Observé sur supplements + telehealth. Besoin de plus de niches à trust barrier pour confirmer.

### A.3 Ce qu'il faudrait pour passer de l'hypothèse à la règle

- **Volume :** ≥ 5 brands par niche, ≥ 100 créas par brand
- **Diversité :** couvrir luxury, food/bev, pet, digital products, SaaS
- **Données perf :** adosser le curseur/mécanique à des métriques (CTR, CPA, ROAS) pour distinguer ce qui EST fait de ce qui MARCHE
- **Temporalité :** observer l'évolution des patterns d'une brand sur 6-12 mois

→ Si BrandSearch.co sort un MCP, la formule V3 est le réceptacle. L'architecture est prête à parser à grande échelle.

---

*Dernière mise à jour : 2026-05-04 (S55 reconciliation · V3 + patches v3.1)*
*Source échantillon canon : 522 créas statiques, 10 batches, 9 brands, 6 niches (V3 maître)*
*Stress test : 23 ads cross-typologies (S55, mai 2026, 10 patches affinants intégrés)*
*Trace empirique S55 : `decisions.md D#391`*
