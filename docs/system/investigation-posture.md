---
title: Investigation Posture · Cartographier avant affirmer
type: doctrine
patch_notes:
  - date: 2026-06-14
    change: "Ajout d'un crochet de capture optionnel en fin de synthèse (§ Crochet de capture). Les items Inconnu / Leviers à haute valeur et les hypothèses Déduit confidence faible / TRÈS faible s'écrivent en write léger vers brands/{slug}/pending-validations.md (§ Enrichment pour le contexte business à surfacer, § Context gate pour les champs inférés à valider), sans dépendre d'un passage ultérieur de learn-from-session. Additif strict : la structure 5 sections et la posture restent inchangées, le crochet est une affordance de persistance native en plus du close ouvert. Aligne sur le pattern d'écriture déjà porté par snapshot-brand / setup-brand. Doctrine de report des étapes différées · docs/system/onboarding-setup-flow.md."
---

# Investigation Posture · Cartographier avant affirmer

> Doctrine fondamentale v2.54+. Tout output stratégique d'un skill production / curator commence par cartographier le connu, déclare ses hypothèses avec confidence chain explicite, identifie les inconnus, et propose des leviers d'investigation à l'opérateur. JAMAIS affirmer comme un fait ce qui est une hypothèse. JAMAIS conclure sans avoir cartographié. L'opérateur arbitre au macro ce qu'on creuse.
>
> Sœur de `contextual-intelligence.md`. Cette doctrine encadre la posture cognitive · contextual-intelligence dit "trust the model" sur le semantic layer, investigation-posture dit "the model investigates before it affirms".

---

## Le problème · symptômes observables

Test live opérateur v2.53 sur cas réel (snapshot-brand sur URL Housswood, 6 min de scan) a révélé un défaut systémique de posture dans tous les outputs stratégiques.

**Symptômes** ·

- Scan URL en 6 minutes puis rapport stratégique complet (audiences, projections ROAS, leviers, plan de pitch) **comme s'il connaissait la marque depuis 6 mois**.
- Hypothèses dérivées de 3 indicateurs partiels lues comme faits (*"leur volume est plafonné par leur calendrier de drops influenceurs"*).
- Personas creative-driven (intuition LLM sur copy lu) présentés comme analyse data-driven (verbatims clients, mine-voc, analytics).
- Conversation fermée par synthèse complète · l'opérateur valide ou rejette en bloc, ne creuse pas, la porte reste fermée.
- Ton confiant produit du copywriting marketing déguisé en analyse business.

**Pourquoi c'est grave** · sur décisions à 5-50k€ de budget paid, affirmer hypothèses comme faits casse la confiance opérateur dès qu'une approximation est découverte · l'agent ferme l'espace de conversation que l'opérateur devrait ouvrir · scaling cross-clients produit des outputs interchangeables non-adaptés à chaque marque.

---

## Le principe canon

PhantomOS est un outil d'investigation, pas de production de slides. Sa valeur n'est pas de faire un meilleur deck que ChatGPT en 6 minutes. C'est de cartographier rigoureusement l'espace de connu et d'inconnu, et de driller avec l'opérateur jusqu'à la performance réelle, basée sur la data.

**Hiérarchie cognitive obligatoire** ·

| Niveau | Source | Confidence | Format en surface |
|---|---|---|---|
| **Observé** | Scrape URL, data Supabase, verbatims, capture opérateur explicite | Sourced | Faits avec source |
| **Déduit** | Inférence de l'agent à partir de l'observé + connaissance du secteur | Faible / moyenne / forte | Hypothèse présentée comme question |
| **Inconnu** | Variables non accessibles sans investigation supplémentaire | n/a | Liste explicite |
| **Leviers** | Skills / actions / sources pour lever les inconnues | n/a | Options drill-down macro |

**Principe absolu** · jamais mélanger les niveaux dans la même phrase sans signaler la nature de chaque élément. Une affirmation prose qui mélange observé + déduit + projection est un anti-pattern.

---

## Règle de structure · tout output stratégique

Tout skill qui produit une synthèse stratégique (snapshot-brand Movement 3-4, profile-audience, produce-paid-angles, brief-day, analyst-perf, audit-meta-account, etc.) DOIT structurer son output en 5 sections explicites.

### Section 1 · Observé (faits sourcés)

Format · table ou liste à puces. Chaque fait avec sa source.

Exemple cible (vs prose actuelle) ·

```
Observé · scan URL housswood.com (2026-05-13, 6 min)

- Produit hero · Lit cabane Héron, prix 369-375€ selon variante
- Fabrication · bois sapin massif non traité PEFC/FSC, Signes (Var)
- Catalogue · 1 produit principal + sur-mesure sur devis
- Preuve sociale revendiquée site · "665 familles", "avis 5 étoiles Google"
- Preuve sociale exposée fiche produit · aucun widget review embarqué (vérifié)
- Footer · 20+ créatrices influenceurs identifiables nominalement
- Trustpilot · accès bloqué côté scrape (résultat scan)
- Capture opérateur · Matteo dit "30 commandes/sem AOV 350 balles, 180k follow insta"

Pas observé directement (ne pas affirmer) · structure paid, audience démographique réelle, gross margin, base mail, plateforme email
```

Pas de prose narrative. Juste des faits avec leur ancrage source.

### Section 2 · Déduit (hypothèses avec confidence)

Chaque hypothèse présentée comme question à l'opérateur, avec confidence explicite et indicateurs sources.

Exemple cible (vs prose actuelle) ·

```
Déduit · 4 hypothèses à valider

H1 · Volume plafonné par calendrier influence (vs capacité atelier)
  Confidence · moyenne
  Indicateurs · scan zéro trace paid + déclaration "spikes" Matteo + 20+ collabs identifiées sur site
  À valider · Tu confirmes ? Y a-t-il déjà eu des tentatives paid abandonnées ? Atelier dispo pour absorber +30% volume ?

H2 · Frein conversion #1 · preuve sociale absente sur fiche produit
  Confidence · faible
  Indicateurs · panier moyen 370€ (achat considéré) + widget review absent vérifié + Trustpilot bloqué
  À valider · Y a-t-il un taux d'abandon panier mesuré ? Sur quelle page ? Heatmap dispo ?

H3 · Audience dominante = parent Montessori primo-acheteur
  Confidence · TRÈS faible (intuition LLM sur copy site, zéro data verbatim)
  Indicateurs · positionnement Montessori revendiqué, profil créatrices, vocabulaire site
  À valider · OBLIGATOIREMENT via mine-voc + données analytics avant de baser une stratégie paid dessus

H4 · ROAS break-even ≈ 3.3
  Confidence · projection conditionnelle (gross margin assumé 30%)
  Sensibilité · si gross margin 25% → break-even 4.0 / si 45% → break-even 2.2
  À valider · Quelle est la gross margin réelle ?
```

Confidence chain · `forte` (consensus 5+ indicateurs convergents externes/internes), `moyenne` (3-5 indicateurs convergents), `faible` (1-2 indicateurs partiels), `TRÈS faible` (intuition modèle sans support externe).

### Section 3 · Inconnu (variables non observables)

Liste explicite des variables qui décident de la stratégie mais qui ne peuvent pas être levées depuis le scan initial.

Exemple cible ·

```
Inconnu · 7 variables à creuser avant pitch

1. Audience démographique réelle (vs hypothèse Montessori) → mine-voc + analytics
2. Gross margin réelle → operator capture
3. Taux conversion + abandon panier par page → analytics
4. Plateforme email + segmentation existante → operator capture (Wix native ? Klaviyo ? Brevo ?)
5. Search volume FR "lit cabane Montessori" "lit bois bébé français" → KeywordTool / Google Keyword Planner
6. Compétitif paid · qui run sur Meta sur leur niche ? → Meta Ads Library
7. Stack analytics installé (GA4 ? Hotjar ?) → operator capture
```

Pas de "deviner" ces variables. Liste explicite.

### Section 4 · Leviers (drill-down options)

Pour chaque inconnue importante, quel skill / action permet de la lever. L'opérateur choisit où on dépense le temps d'investigation.

Exemple cible ·

```
Leviers · 4 axes d'investigation prioritaires

Axe A · Audience réelle (lève H3 + Inconnu 1)
  → mine-voc sur Trustpilot + forums maternité (8-12 min)
  → cross-référence avec analytics si dispo

Axe B · Structure économique (lève H4 + Inconnu 2)
  → 1 question opérateur (gross margin, AOV historique, distribution)
  → calibrage ROAS targets après

Axe C · Structure paid concurrentielle (lève Inconnu 6)
  → audit-meta-account si compte client dispo
  → Meta Ads Library scan compétiteurs sur niche

Axe D · Preuve sociale terrain (lève H2)
  → mine-voc reviews Google + influenceurs déjà collaborateurs (déclaration témoignages)
  → cross-référence taux conversion par page
```

### Section 5 · Close ouvert (question macro)

L'output se termine par UNE question macro sur la priorité de drill-down. Pas de "voici le plan complet", l'opérateur arbitre.

Exemple cible ·

```
On a 4 axes d'investigation. Pour ton pitch demain, lequel veux-tu creuser en priorité ?

A · Audience réelle (mine-voc · 8-12 min · le plus critique pour ton slide audiences)
B · Structure économique (1 question · 30 sec · calibre tes projections ROAS)
C · Structure paid compétitive (audit Meta Ads Library · 5-10 min · pour ton slide Meta)
D · Preuve sociale terrain (mine-voc reviews · 8-12 min · pour le slide friction)

Reco macro · A + B en premier (45 min total, pose la fondation), C/D si temps avant le call.
```

L'opérateur dit `A` ou `A+B` ou autre, l'agent enchaîne le drill-down sur l'axe choisi.

### Crochet de capture (optionnel · additif)

> Affordance de persistance native, en plus du close ouvert. Le close ouvert reste la fin canon visible de la synthèse (la question macro). Le crochet est muet côté opérateur · il grave en arrière-plan ce qui mérite d'être repris plus tard, pour que l'investigation ne dépende pas d'un passage ultérieur de `learn-from-session`.

Quand la synthèse pose des inconnues à haute valeur ou des hypothèses sur du sable, ces items s'écrivent en **write léger** vers `brands/{slug}/pending-validations.md` au fil de la synthèse, pas seulement en prose qui s'évapore à la fin du tour. C'est la même règle « inconnus, leviers et étapes différées sont des champs visibles, jamais des trous muets » que la doctrine de report des étapes différées (`docs/system/onboarding-setup-flow.md`, à laquelle on renvoie plutôt que de la rédupliquer).

**Ce qui se capture, et vers quelle surface** ·

| Item de la synthèse | Surface dans `pending-validations.md` | Pourquoi cette surface |
|---|---|---|
| Hypothèse `Déduit` confidence `faible` ou `TRÈS faible` qui sert d'appui à un livrable | `§ Context gate` | Champ inféré non validé humainement · soft friction si réutilisé tel quel |
| `Inconnu` à haute valeur (variable qui décide de la stratégie) | `§ Enrichment` | Contexte business non capté au scan · à surfacer avant de réinventer |
| `Levier` pré-amorçable rattaché à un Inconnu | `§ Enrichment` (avec le levier en clair sur la ligne) | L'item porte déjà le geste qui le lèverait |

**Forme de la ligne** · un `- [ ]` par item, formulé dans la langue de l'opérateur, tag de source en clair (`(inféré du site)`, `(déduit)`, `(à confirmer côté opérateur)`), jamais les mots-clés `source` / `confidence` / `mode`. Append-only, jamais d'écrasement. C'est exactement le pattern d'écriture que `snapshot-brand` et `setup-brand` portent déjà sur ces deux sections · cette doctrine ne fait que l'étendre à tout output stratégique qui passe par les 5 sections.

**Garde-fous du crochet** ·

- **Optionnel, jamais bloquant.** Pas de brand cible résolu (`_EXAMPLE`, contexte hors marque, question libre) → on saute le write en silence, la synthèse 5 sections reste intacte.
- **Sélectif, pas un dump.** On ne déverse pas les 5 sections dans le fichier · seuls les items à haute valeur ou à confiance faible y vont. Le reste vit dans la synthèse du tour.
- **Léger et muet.** L'écriture suit la règle « zéro plomberie visible » · on ne nomme ni le fichier ni les sections à l'écran. La seule trace opérateur-facing reste le close ouvert.
- **Indépendant de `learn-from-session`.** Le crochet grave au moment de la synthèse · il ne présuppose pas qu'un flush d'apprentissage de fin de session passera. Si `learn-from-session` passe ensuite, il enrichit, il ne remplace pas.
- **Mutation discipline.** Écriture via le canal d'écriture canon du fichier (append `[ ]` sous la bonne section), jamais d'édition manuelle qui casserait le format des autres sections.

---

## Anti-patterns explicites

### AP-1 · Affirmation d'hypothèse comme fait

Avant ·
> *"Leur volume est plafonné par leur calendrier de drops influenceurs, pas par leur capacité atelier ni leur marché."*

Après ·
> *Hypothèse · leur volume est probablement plafonné par leur calendrier d'influence plutôt que par leur capacité atelier (confidence moyenne · 3 indicateurs partiels). À valider auprès de Matteo · y a-t-il eu des tentatives paid abandonnées ? L'atelier peut-il absorber +30% volume ?*

### AP-2 · Personas inventés présentés comme analytiques

Avant ·
> *"Parent Montessori primo-acheteur. Cadre urbain ou périurbain, 28-38 ans, CSP+. A lu Maria Montessori avant la naissance..."*

Après ·
> *Hypothèse audience H1 · profil "parent Montessori primo-acheteur" (confidence TRÈS faible · intuition modèle sur copy site, zéro data verbatim client). Indicateurs site · vocabulaire Montessori, profil créatrices, ton. Validation OBLIGATOIRE avant utilisation stratégique · mine-voc sur reviews + verbatims influence + analytics audience si dispo.*

### AP-3 · Copywriting narratif déguisé en analyse

Avant ·
> *"C'est pas une marque de mobilier enfant. C'est une réponse artisanale à une contradiction que les parents Montessori vivent en silence : ils ont adopté une pédagogie de liberté de mouvement, mais le marché du mobilier bébé leur propose encore largement du MDF verni made-in-ailleurs."*

Après ·
> *Positionnement observé · "mobilier Montessori artisanal français" (revendiqué site, footer 20+ créatrices). Hypothèse driver d'achat · différenciation matériaux + valeurs vs MDF mainstream (confidence faible · intuition site, à valider verbatim).*

L'analyse rigoureuse ressemble à une note d'analyste financier, pas à un pitch de marque.

### AP-4 · Conclusion sans investigation

Avant ·
> *"Le ROAS break-even est 3.3"*

Après ·
> *Projection ROAS break-even = 3.3 conditionnelle à gross margin = 30%. Sensibilité · si 25% → 4.0, si 45% → 2.2. Variable à confirmer auprès opérateur AVANT de baser une décision budget dessus.*

### AP-5 · Close affirmatif qui ferme la conversation

Avant ·
> *"Je passe au tableau de projection chiffrée maintenant ?"*

Après ·
> *On a 4 axes d'investigation. Lequel veux-tu creuser pour ton pitch · audience réelle (mine-voc 10 min), structure économique (1 question), compétitif paid (audit 10 min), preuve sociale terrain (mine-voc 10 min) ?*

### AP-6 · Prose narrative continue sans structure

Avant · 3 pages de prose continue mélangeant observé + déduit + projection + reco.

Après · 5 sections explicites (Observé · Déduit · Inconnu · Leviers · Close ouvert). Chaque section a son rôle, l'opérateur navigue.

### AP-7 · Improvisation prose vs skill execution (NEW v2.55)

Avant ·
> Operator pose une question stratégique ("Quelles sont les audiences ?", "Quels angles paid ?"). L'agent répond en prose libre avec 3-4 audiences ou angles inventés depuis sa connaissance LLM, structurés en sections, avec verbatims, démographies, signaux paid. Convaincant mais zéro consume des matrices canon (hooks, angles, heuristiques-persuasion, mechanics-registry).

Après ·
> Operator pose même question. L'agent invoque le skill correspondant via Task tool · `profile-audience` pour audiences, `produce-paid-angles` pour angles. Le skill consume les matrices canon, applique l'équation compositionnelle, retourne un output structuré avec hypothèses confidence chain + références canon explicites. L'agent surface le résultat à l'opérateur en respectant la posture investigation (5 sections).

Test binaire · *"Est-ce que cet output aurait pu sortir directement d'un skill PhantomOS, ou j'invente la roue en prose ?"*. Skill existe → invoke. Pas de skill → flag gap, propose `create-skill`. Improvisation prose = bug v2.55+.

---

## Confidence chain · canon de formulation

| Niveau | Indicateurs requis | Formulation cible |
|---|---|---|
| **Forte** | 5+ convergents (interne + externe sector data) | "Quasi-certain · ..." OU "Pattern confirmé ·" |
| **Moyenne** | 3-5 convergents (majoritairement interne) | "Probable · ..." OU "Hypothèse soutenue par X indicateurs ·" |
| **Faible** | 1-2 partiels (intuition principalement) | "Hypothèse à valider · ..." |
| **TRÈS faible** | Intuition modèle sans support | "Intuition seulement · à valider OBLIGATOIREMENT avant utilisation stratégique" |

**Règle absolue** · une hypothèse `TRÈS faible` ne peut pas servir de fondation à une décision budget. L'opérateur doit savoir explicitement quand on est sur du sable.

---

## Drill-down macro · interaction opérateur

L'opérateur ne valide pas chaque détail. Il arbitre au **macro** ·

- Quel axe d'investigation prioriser ?
- Quelle hypothèse creuser en premier ?
- Quelle inconnue lever en priorité ?

L'agent fait le drill-down détaillé sur l'axe choisi, présente le nouveau output (en respectant les 5 sections), repropose au macro. Cycle itératif.

Anti-pattern · demander à l'opérateur de valider chaque audience candidate, chaque hypothèse, chaque chiffre individuellement. Macro-arbitrage uniquement.

---

## Application cross-skills

Skills concernés en priorité v2.54 ·

- **`snapshot-brand`** · refactor Movement 3 (synthesis 3-movements) en 5 sections obligatoires (le test live a sourcé le diagnostic)
- **`profile-audience`** · audiences = hypothèses TRÈS faible jusqu'à mine-voc, JAMAIS personas inventés présentés comme analytiques
- **`produce-paid-angles`** · angles dérivés des hypothèses doivent porter leur confidence chain
- **`brief-day`** · état brand = cartographie observé/déduit/inconnu, pas affirmation

Skills concernés v2.55+ (audit + propagation) ·

- `audit-meta-account` · l'audit produit déjà du data mais la synthèse doit suivre la posture
- `analyst-perf` · pareil
- `decompose-ad` · l'analyse d'une ad concurrente doit séparer ce qu'on voit vs ce qu'on déduit
- `produce-copy-brief` · le brief est déduit des hypothèses, doit porter leur confidence

---

## Position dans le système opérationnel 5 couches

Investigation posture (5 sections · Observé · Déduit · Inconnu · Leviers · Close ouvert) est règle canon couche 2 du système opérationnel (cf `operational-system-doctrine.md`). Elle s'applique à TOUT output stratégique (audience synthesis · paid angles · brief copy · audit perf · etc).

Sans cette règle · synthèses non-traçables freelancées. Avec elle · chaque assertion porte son étiquette d'origine et confidence chain.

---

## Cross-refs

- Master · `docs/system/contextual-intelligence.md` (cette doctrine en est une extension cognitive)
- Sister · `docs/system/canonical-matrix-reasoning.md` (production discipline · cette doctrine encadre la qualité analytique en amont)
- Sister · `docs/system/schema-encoding-doctrine.md` (substrate · les sections observé/déduit/inconnu/leviers s'encodent dans les schemas comme _field_types vs hypothesis_status)
- Workspace CLAUDE.md root · règle "Cartographier avant affirmer · confidence chain explicit · drill-down macro = opérateur"

---

## Rationale (S55 cycle USAGE)

L'opérateur Largo a testé snapshot-brand sur housswood.com en conditions réelles (préparation pitch client demain). L'output a produit · 3 audiences inventées présentées comme analytiques, projection ROAS posée comme un fait, copywriting narratif (*"C'est pas une marque de mobilier enfant..."*) en tête de rapport, close affirmatif (*"Je passe au tableau de projection chiffrée ?"*).

Feedback explicite opérateur ·

> *"Il est hyper affirmatif. Il sait tout alors qu'en vrai, il ne sait rien. Il n'a aucune donnée sur le shop, sur la structure. On n'a pas vraiment digué. Il doit être toujours en mode drill-down, break-down. Cartographier les variables, les différents leviers à disposition, pour aller chercher de l'information. En premier temps, c'est toujours la data. La data va t'apporter la performance. Il faut d'abord comprendre et analyser, toujours ne pas être hyper affirmatif. C'est ce qui fait que tu n'ouvres pas la porte à d'autres choses."*

Cette doctrine encode cette posture comme règle canon, applicable cross-skills.
