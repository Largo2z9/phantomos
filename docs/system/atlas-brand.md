# Atlas brand · doctrine cartographie holistique

> Concept canonique upstream PhantomOS · v2.36+. La cartographie holistique data d'une brand e-commerce. Distinct de atlas canon copy (référentiel cross-brand doctrine, sense 1).

## Définition

L'atlas brand est la **structure complète de la matière data d'une brand** dans PhantomOS · audiences + products + angles + creatives + scoring + verbatims + tests + learnings + strategy. C'est l'équivalent de la page "Données Atlas" dans Notion Stride-Up (Onday).

Pas un référentiel statique. Pas un fichier unique. C'est le **concept architectural** qui désigne l'ensemble structuré de la matière brand.

## Composants canoniques

L'atlas brand est composé de 7 entités core (mutation gate-protected) :

| Entité | Storage | Fonction |
|---|---|---|
| brand | `brand.json` | identité + positionnement + voix + creative_zone + brand_equity_level |
| spec | `products/{slug}/spec.json` (1 par produit) | matière produit · mechanisms[] · benefits[] · problems_solved[] · visual_identity |
| offers | `products/{slug}/offers.json` (1 par produit) | structures commerciales · bundles · pricing |
| profile | `audiences/{slug}/profile.json` (1 par audience) | 8 dimensions canon V3 + Schwartz double-stage + pain_points 3 niveaux |
| angle | `angles/{slug}/angle.json` (1 par angle) | axe d'attaque · formule Observation × Tension × Reframe × Bridge · lineage canon |
| learnings | `learnings.json` | append-only · règles métier capturées |
| strategy | `strategy.json` | objectifs annuels + targets mensuels + focus courant |

Plus 2 entités dérivées (post-skill outputs) :
- creatives produced · `produced/{CRT-N}.json` + JPG + brief markdown
- scoring matrix · `scoring/matrix-{date}.json`

## Atlas vivant DANS l'atlas brand

Le sense 2 (atlas vivant) est un **pattern de compound learning** qui s'applique DANS l'atlas brand. Chaque output skill (mining verbatims, angles produits, creatives testés) enrichit `validations[]` append-only sur les outils canon copy utilisés (sense 1). Au fil du temps, l'atlas canon générique devient validé empiriquement par brand.

Distinction critique :
- atlas brand (sense 4) = LA cartographie elle-même
- atlas vivant (sense 2) = mécanisme de feedback loop sur outils canon utilisés DANS la cartographie

## Navigation atlas brand · `/phantom`

L'atlas brand est navigable via `/phantom` (cockpit principal) :
- `/phantom {brand_slug}` (mode brand) · vue état global atlas (substrat L1/L3, mutations recent, next-suggested)
- `/phantom {brand_slug} audiences` · drill entité audiences
- `/phantom {brand_slug} audiences {audience_slug}` · drill item profil 8 dim
- `/phantom {brand_slug} products` · drill products
- `/phantom {brand_slug} angles` · drill angles
- `/phantom {brand_slug} creatives` · drill creatives produced (v2.36 si shippé)
- `/phantom {brand_slug} matrix` · drill scoring matrice (v2.36 si shippé)
- `/phantom {brand_slug} briefs` · drill briefs et tests (v2.36 si shippé)

## Distinction vs `_snapshot.md`

`_snapshot.md` (1-2KB plaintext digest auto-régénéré) = **résumé lisible** de l'atlas brand. Pas l'atlas lui-même. C'est l'artefact de communication rapide pour le cockpit. L'atlas brand est le concept architectural complet (les 7 entités + dérivées).

## Mécaniques d'enrichissement

L'atlas brand s'enrichit progressivement via skills :
- P0 onboarding : setup-brand, snapshot-brand, define-specs hybrid mode (initialise brand + spec)
- P2a audience : mine-voc, mine-vom, mine-audience, profile-audience (peuple audiences)
- P2b angle : produce-paid-angles, decompose-ad (peuple angles)
- P3 scoring : weight-dimensions, score-matrix (peuple scoring matrix)
- P4 brief : produce-copy-brief (peuple briefs)
- P5 visual : compose-creative, recompose-creative, decompose-ad (peuple creatives produced)
- ongoing : learn-from-session, validate-resources (maintenance + validation)

Chaque skill consomme ce qui existe déjà dans l'atlas et alimente ce qui manque. Pattern compound learning.

## Best practices

- Toujours penser atlas-first quand on parle de la matière data brand
- Distinguer atlas brand (sense 4) de atlas canon copy (sense 1) à l'oral et à l'écrit
- Référencer `_snapshot.md` quand on parle du digest, atlas brand quand on parle de la cartographie complète
- Utiliser `/phantom` comme entry point principal pour naviguer l'atlas brand
- Préserver le canon vivant (validations[]) à chaque output skill

## Cross-refs

- `lexicon.md § Atlas, 4 senses MECE` (definitions canonical)
- `docs/system/atlas-canon-copy.md` (sense 1 référentiel cross-brand)
- `docs/internal/canon.md § Atlas brand` (entry interne)
- `.claude/commands/phantom.md` (cockpit navigation)
- D#382-D#391 (decisions S55 atlas canon copy + skills consume + Phase B audit)
