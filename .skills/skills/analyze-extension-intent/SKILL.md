---
name: analyze-extension-intent
type: curator
version: "2.0.0"
recommended_model: sonnet
layer: meta
reasoning_pattern: null
description: >
  Sub-skill of scaffold-extension. Captures operator intent for a new extension and
  extracts structured attributes: entity class (custom entity / sidecar / skill-only),
  data shape (time-series / instance-per-item / aggregate), population mechanism
  (manual / scraper / derived), declared cross-references. Three focused questions max.
  Invoked by scaffold-extension Phase 1. Not intended for direct operator invocation.
  v2.0.0 layers in the ECR methodology (Équation Compositionnelle Récursive · 5
  étapes runtime + 4 patterns canon Strat/Compo/Exé · Funnel · Système · Performance
  + 5 pièges) on top of the structural capture, applied when the subject passes the
  3-criteria eligibility test (hiérarchie · auto-similarité · interdépendance
  multiplicative). Backward compatible · v1.0.0 mode preserved when eligibility fails.
  FR: "analyse l'intent extension" "capture l'intent" "extension intent" "décompose ECR".
  EN: "analyze extension intent" "capture extension intent" "extension intent" "ECR decomposition".
permissions:
  reads: [brand]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: operator has expressed intent to build an extension
  postconditions: structured intent object (optionally enriched with ECR decomposition tree) returned to orchestrator
---

# Skill: Analyze Extension Intent

Captures and structures the operator's intent for a new extension. v2.0.0 layers the
ECR methodology on top of the v1.0.0 structural capture when the subject is
compositionnel récursif.

## Method · structural capture (preserved v1.0.0)

Ask at most three focused questions, one per turn, calibrated to the conversation register:

1. **Nature of the data** · *"Ce que tu veux stocker, c'est plutôt une observation qui évolue dans le temps, des items distincts que tu ajoutes au fil, ou un enrichissement de ce que tu as déjà sur cette marque ?"*
2. **Source and cadence** · *"Tu le rempliras toi-même à la main, un skill va le remplir automatiquement (scraper, API pull), ou c'est calculé à partir d'autres données ?"*
3. **Cross-references** · *"Ça pointe vers quoi dans ton workspace ? Un produit précis ? Une audience ? Une offre ? Rien de précis ?"*

Skip questions that are already answered by the operator's opening message.

## Method · mode data-first (preserved v1.0.0)

Si l'opérateur fournit une donnée structurée (bloc JSON, tableau, liste de variables avec valeurs), inférer silencieusement :

- **Class** · si donnée = une liste d'observations sur même sujet avec évolution temporelle possible → time-series custom entity. Si donnée = plusieurs items distincts avec attributs parallèles → instance-per-item custom entity. Si donnée = champs qui enrichissent un concept brand existant → sidecar. Si donnée = un fait simple → route vers capture-learning (pas scaffold).
- **Shape** · inférée de la structure de la donnée.
- **Cross_refs** · scanner la donnée pour détecter les slugs/IDs qui pointent vers core entities (`product_slug`, `audience_slug`, `offer_id`).
- **Proposed_name** · inféré du contenu thématique ou demandé en 1 question si ambigu.

Poser maximum **une question** à l'opérateur, et uniquement sur ce qui reste ambigu après l'inférence (typiquement · population mechanism future · *"ça, ça va venir de toi manuellement, ou un skill va le pull automatiquement ?"*).

La donnée fournie est conservée dans le contexte pour Phase 7 (scaffold-entity-files) qui la populera directement en tant qu'instance(s) dans le fichier créé.

## Method · ECR decomposition (NEW v2.0.0)

Avant de retourner l'intent object, appliquer la méthodologie ECR en 5 étapes. Le but · ne pas se contenter d'un scaffold structurellement correct, mais guider la décomposition du sujet en équation compositionnelle récursive jusqu'aux atomes mesurables.

### Étape ECR-1 · Test d'éligibilité (3 critères)

Avant de décomposer, vérifier que le sujet est compositionnel récursif. Trois questions ·

1. Hiérarchie de niveaux ? (du macro au micro)
2. Auto-similarité (la même logique se répète à chaque niveau) ?
3. Interdépendance multiplicative (composition × pas addition) ?

Si 3/3 OUI → ECR applicable, continuer étapes 2-5.
Si moins → décomposition hiérarchique classique (organigramme), pas vraie ECR. Capture intent simple en mode v1.0.0 (Kind · Scope · Attributes seuls). Skip étapes 2-5.

Examples sujets qui passent · production créative, funnel acquisition, brand system, content strategy, customer journey, stratégie SEO.

Examples sujets qui ne passent pas · choix d'un nom de marque (ponctuel), négociation contrat (séquentiel), calcul budget (additif).

### Étape ECR-2 · Identifier l'atome de sortie

Quel est l'objet final mesurable du sujet ?

Examples ·
- Pour une créative · le pixel final
- Pour un funnel · la conversion finale
- Pour une marque · la perception mentale finale
- Pour un script vidéo · le mot/seconde qui déclenche l'action

C'est le point d'arrivée. Toute l'équation doit converger vers lui.

### Étape ECR-3 · Triptyque universel Pourquoi × Quoi × Comment

Il existe un pattern méta qui couvre 90% des sujets ECR ·

[Sujet] = Stratégie × Composition × Exécution

Pourquoi · stratégie, intention, contexte (niveau abstrait)
Quoi · composition, architecture, structure (niveau intermédiaire)
Comment · exécution, détails, atomes (niveau concret)

Pour le sujet, poser l'équation maître ·
[Sujet] = Pourquoi × Quoi × Comment
Adapter les noms au domaine spécifique.

4 patterns canon possibles selon domaine ·
- Strat/Compo/Exé (livrables créatifs · créatives · landing pages · emails · posts sociaux · campagnes pub)
- Funnel (parcours séquentiels emboîtés · TOFU × MOFU × BOFU · customer journey · email sequences)
- Système (composants × règles × interactions · brand system · design system · content strategy · SEO)
- Performance (input × processus × output mesurable · performance campagne · CRO · growth loops · LTV/CAC)

Identifier le pattern dominant pour le sujet · table de reconnaissance rapide ·

| Question opérateur | Pattern à utiliser |
|---|---|
| "Comment crée-t-on un [livrable] ?" | Strat/Compo/Exé |
| "Comment quelqu'un passe de A à Z ?" | Funnel |
| "Comment est structuré ce système ?" | Système |
| "Comment optimise-t-on ce résultat ?" | Performance |

### Étape ECR-4 · Décomposer chaque phase en 3-5 sous-variables MECE

Règle d'or · jamais moins de 3, jamais plus de 5 sous-variables par niveau.

Moins de 3 → sur-simplification, leviers ratés.
Plus de 5 → surcharge, inutilisable.

Pour chaque sous-variable proposée, appliquer test triple ·
1. Quels sont les leviers que je peux faire varier indépendamment ?
2. Quelles décisions distinctes je dois prendre à ce niveau ?
3. Si je retire cette variable, est-ce que je perds quelque chose d'essentiel ?

Si une variable ne passe pas les 3 tests → fusionner avec une autre ou supprimer.

Variables doivent être MECE · Mutually Exclusive (pas de chevauchement), Collectively Exhaustive (couverture complète).

### Étape ECR-5 · Décomposer récursivement jusqu'aux atomes mesurables

Pour chaque sous-variable, repose-toi la question · peut-elle se décomposer ?

Si oui → décompose-la avec 3-5 sous-sous-variables.
Si non → c'est un atome, arrête-toi.

Test d'atomicité · si tu peux modifier cet élément et observer un delta mesurable sur l'output final, c'est un atome. Sinon, c'est encore un agrégat à décomposer.

Cohérence descendante bidirectionnelle · chaque atome doit pouvoir remonter à un agrégat par une chaîne de "parce que" lisible.

## Output

Return a structured intent object to the orchestrator. v1.0.0 fields preserved · v2.0.0 adds `ecr_decomposition` block when test d'éligibilité passes (sinon block absent ou `applicable: false`).

```
{
  "class": "custom_entity | sidecar | skill_only | route-to-capture-learning",
  "shape": "time_series | instance_per_item | aggregate",
  "population": "manual | scraper | derived",
  "cross_refs": ["product_slug", "audience_slug", ...],
  "proposed_name": "{operator_provided_or_suggested}",
  "scope": "brand | workspace",
  "entry_mode": "intent_first | data_first",
  "provided_data": { /* populated only in data_first mode, passed to Phase 7 */ },
  "ecr_decomposition": {
    "eligibility": {
      "hierarchical": true,
      "auto_similar": true,
      "multiplicative": true,
      "applicable": true
    },
    "atom_output": "{description atome de sortie}",
    "triptych_pattern": "Strat/Compo/Exé | Funnel | Système | Performance",
    "master_equation": "[Sujet] = X × Y × Z",
    "decomposition_tree": {
      "X": {
        "sub_variables": ["a", "b", "c"],
        "mece_validated": true
      },
      "Y": { "sub_variables": [...], "mece_validated": true },
      "Z": { "sub_variables": [...], "mece_validated": true }
    },
    "atoms_identified": ["atom1", "atom2", ...]
  }
}
```

## Hard rules

- Three questions maximum across all turns of this phase.
- Never ask for field names here · schema drafting happens in Phase 3.
- Never ask for technical format (JSON, shape, etc.) · the skill infers from the conceptual answer.
- **HR-ECR-1** · Si test d'éligibilité fail (sujet pas fractal), capture intent simple sans ECR forcée (v1.0.0 mode · Kind · Scope · Attributes seuls, `ecr_decomposition.applicable: false`).
- **HR-ECR-2** · Pas plus de 5 sous-variables par niveau (sinon fusionner OU descendre d'un niveau).
- **HR-ECR-3** · Variables MECE strict (pas de chevauchement · test triple appliqué).
- **HR-ECR-4** · Cohérence descendante bidirectionnelle (chaque atome remonte par "parce que").
- **HR-ECR-5** · Ne JAMAIS forcer ECR sur sujet non-fractal (anti-pattern · décomposition artificielle).

## Cross-refs canon

- `docs/system/operational-system-doctrine.md` v2.71 · doctrine mère ECR canonisée (couche 1 du système opérationnel · 5 étapes + 4 patterns + 5 pièges).
- `docs/system/scope-extension-doctrine.md` SED-X · méthodologie ECR amont (scoping extension avant scaffold).
- `docs/system/compositional-cartography.md` · équation OUTPUT = NOYAU × CONTEXTE × MODIFIEURS (pattern Strat/Compo/Exé instancié au créatif).
