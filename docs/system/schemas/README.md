# Schemas, documentation par entité

Chaque schema sous `resources/schemas/*.schema.json` a une doc dédiée ici qui explique le contexte, les best practices, les signaux pour Claude. Format unifié 7 sections (≤ 120 lignes par doc).

## Comment lire ces docs

1. Lis la `description` inline JSON du schema d'abord (autoritatif sur path + version + champs).
2. Si décision sémantique non triviale (champ load-bearing, conflit entre schemas, encodage flou), lis `docs/system/schemas/{name}.md` (≤ 2 min de lecture).
3. Si toujours flou après ces deux lectures, drill plus profond, `schema-encoding-doctrine.md` pour la mécanique d'encodage, `field-types.md` pour les tags `_field_types`, `audience-cartography.md` pour la doctrine audience.

## Index par entité

**Atlas (amont) :**

| Entité | Schema | Doc | Statut |
|---|---|---|---|
| brand | brand.schema.json | [brand.md](brand.md) | brand/2.4 (+ `brand_da` v2.89) |
| spec (produit) | spec.schema.json | [spec.md](spec.md) | v1.11 |
| profile (audience) | profile.schema.json | [profile.md](profile.md) | active |
| offer | offer.schema.json | [offer.md](offer.md) | v2.0 DRAFT |
| angle | angle.schema.json | [angle.md](angle.md) | angle/1.3 |
| sop | sop.schema.json | TODO P2 | docs à venir |
| canon-tool | canon-tool.schema.json | TODO P2 | docs à venir |
| connected-sources | connected-sources.schema.json | TODO P2 | docs à venir |

**Production (chaîne créa · Brique 4 + v2.89) :**

| Entité | Schema | Statut |
|---|---|---|
| creative (lignage) | creative.schema.json | creative/1.4 shippé |
| genome (ADN) | genome.schema.json | genome/1.2 |
| genome-package (contrat A→B) | genome-package.schema.json | genome-package/1.3 |
| decomposition (reverse) | decomposition.schema.json | decomposition/1.3 |
| produced-asset (sidecar binaire + qc) | produced-asset.schema.json | produced-asset/1.0 |
| library-pattern (patterns promus) | library-pattern.schema.json | library-pattern/1.0 (+ `visual-style`) |
| style-recipe (backing style_id) | style-recipe.schema.json | style-recipe/1.0 · NEW v2.89 · 22 fiches `registries/styles/` |

## Graphe de dépendances

```
brand
  ├── spec (produit)
  │   └── offer (offre par produit)
  ├── profile (audience)
  │   └── compatible avec → angle
  └── angle (couche stratégique)
      ├── lineage → resources/canon/copy/{layer}/{tool}.json
      └── compatible avec → creative
          └── creative (instance décomposée)
              ├── concept_id (groupage variantes)
              └── variant_of (filiation)
```

## Lecture des relations

- **brand** est la racine, tout enfant lit son contexte (creative_zone, brand_equity_level, purchase_driver, promotions brand-level).
- **spec** porte la matière brute factuelle d'un produit. **offer** habille cette matière en propositions commerciales (bundle, GWP, urgence).
- **profile** centralise la psychologie audience. **angle** la lit pour produire une stratégie d'attaque.
- **angle** post-v1.2 est strictement stratégique. Tout ce qui est instance déployée (format, CTA, mécanique, seasonality) vit dans **creative**.

## Posture canon

Ces docs sont du **contexte** qui aide la réflexion d'un agent qui découvre, pas des règles prescriptives. Si Claude voit un signal qui sort du cadre décrit, qu'il creuse plutôt que de force-fit. Posture éducateur + collègue, pas inspecteur. Référence : `docs/system/contextual-intelligence.md`.

## Champ couvert vs non-couvert

Cette zone documente les **5 schemas load-bearing** en P0, les 4 autres (sop, canon-tool, connected-sources, creative) sont en P2, à rédiger quand les skills consumers s'y appuient.
