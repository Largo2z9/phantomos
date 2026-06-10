# Mechanism Families Registry

> **TYPE:** Taxonomie · registre vivant (SSOT du vocabulaire `spec.json#mechanisms[].mode_of_action`)
> **CONSOMMÉ PAR:** define-specs, snapshot-brand, map-mechanisms, produce-paid-angles (le mécanisme nourrit l'angle), decompose-ad
> **SOURCE:** Enum historique spec.schema (pilotes ingestibles karacare/naali) + 1ère marque physique (Stepprs, vitrine `_EXAMPLE`)
> **STATUT:** v0.1 stub (v2.89.4) · ouvert par la décision de dé-hardcoder l'enum `mode_of_action` (biais ingestibles, violait l'esprit du test d'extractibilité D#307)

---

## Principe

- **Le schéma ne porte plus l'enum.** `mode_of_action` est une string libre côté `spec.schema` ; CE registre est la source de vérité du vocabulaire. Même pattern que `creative-mechanics-registry.md` pour la mécanique ad-level.
- **Consulter avant d'écrire.** Tout skill qui remplit `mode_of_action` pioche d'abord ici. Valeur absente du registre → l'utiliser quand même si elle est juste (string libre), ET la logger comme candidate (signal 1).
- **Promotion au 2e signal indépendant.** Une valeur candidate devient CANON quand 2 marques indépendantes (pas la même factory) l'utilisent. Jamais de famille inventée par anticipation.
- **`other` = poubelle surveillée.** Si `other` dépasse 30% des mécanismes d'une marque (≥3 mécanismes), c'est le signal qu'une famille manque ici, pas que le produit est inclassable. Check mécanique : `validate-all.py` (mechanism_other_saturation). Précédent : `proof_type other` 26% → 3,5% après durcissement taxonomie sur corpus réel.

---

## Familles CANON

### Ingestibles (héritées de l'enum historique · validées sur les pilotes wellness)

| Valeur | Définition courte |
|---|---|
| `cofactor` | Apporte un cofacteur d'une réaction physiologique |
| `antioxidant` | Neutralise le stress oxydatif |
| `adaptogen` | Module la réponse au stress |
| `probiotic` | Agit via le microbiote |
| `coenzyme` | Précurseur ou forme active d'une coenzyme |
| `regulator` | Régule un système (hormonal, glycémique...) |
| `stimulant` | Stimule un système (énergie, vigilance...) |
| `inhibitor` | Inhibe un processus (appétit, absorption...) |
| `delivery` | Le mécanisme EST le mode de délivrance (liposomal, retard...) |
| `structural` | Apporte un composant structurel (collagène, kératine...) |
| `other` | Aucune famille ne convient · surveillé (cf. Principe) |

### Physiques (candidates · 1 source : Stepprs `_EXAMPLE` · promotion au 2e signal)

| Valeur | Définition courte | Statut |
|---|---|---|
| `mechanical_stimulation` | Stimulation mécanique des tissus (massage, pression, texture) | CANDIDATE (1/2) |
| `biomechanical_redistribution` | Redistribue charges ou appuis (support de voûte, posture) | CANDIDATE (1/2) |
| `shock_absorption` | Absorbe ou amortit les impacts | CANDIDATE (1/2) |
| `friction_grip` | Agit par friction ou adhérence (antidérapant, maintien) | CANDIDATE (1/2) |

---

## Graduation

Quand une 2e marque indépendante utilise une candidate : passer son statut à CANON, déplacer la ligne dans la table CANON (section par vertical si besoin), noter la marque source. Quand un nouveau vertical arrive (cosmétique, textile, digital...), ses premières valeurs entrent ici en CANDIDATE, jamais directement dans un enum.

---

> **Pourquoi ce registre existe :** l'enum historique encodait silencieusement une hypothèse compléments alimentaires dans le core (cofactor, probiotic, efsa_*). Le test d'extractibilité (D#307) exige que le core survive au changement de produit. Le vocabulaire vit donc en données (enrichissable par corpus), le schéma reste agnostique. Décision v2.89.4.
