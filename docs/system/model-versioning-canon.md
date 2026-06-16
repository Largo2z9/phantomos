# Model Versioning Canon

> Doctrine canonique v2.44 ship · v2.46 pragma adapt. Tout skill qui appelle une API externe (image gen · LLM · etc.) déclare la version utilisée en frontmatter et la date de canon. Pas de runtime check obligatoire (drop v2.46 · trop strict, ralentit, peut planter). Audit manuel périodique tous les 3-6 mois. Sœur de skill-authoring-discipline et compositional-cartography.

## Le problème

PhantomOS skills hardcodent les endpoints API externes dans frontmatter `permissions.external_apis[]`. Exemple v2.43 · `compose-creative` et `craft-packshot` utilisaient `fal-ai/nano-banana-pro/edit` (Gemini 2.5 Flash Image · pre-novembre 2025). En novembre 2025, Google a release Gemini 3 Pro Image (fal endpoint `nano-banana-2/edit`) · meilleur · text fidelity supérieur · material preservation native. Skills PhantomOS continuaient à utiliser endpoint legacy · résultats sub-optimaux.

Cycle USAGE v2.44 stress test produit canon a livré 9 attempts échouées sur endpoint legacy (silhouette bouteille réinventée OR text gibberish) avant que swap vers `nano-banana-2/edit` résolve en 1 attempt avec prompt naturel français court. Apprentissage canon · le canon de novembre 2025 n'était plus le canon de mai 2026. Drift silencieux entre release modèle et adoption skill.

## Règle canon pragma v2.46

### Frontmatter annotation (OBLIGATOIRE)

Chaque skill qui call API externe DOIT declarer `permissions.external_apis[]` ·

```yaml
permissions:
  external_apis:
    - provider: "fal.ai"
      endpoint: "fal-ai/nano-banana-2/edit"
      model_family: "gemini_3_pro_image_novembre_2025"
      version_check_url: "https://fal.ai/models?keywords=banana"
      version_canon_date: "2025-11"
      replaced_legacy: "fal-ai/nano-banana-pro/edit (v2.43)"
      auto_upgrade: false
```

Champs ·
- `provider` · vendor de l'API (fal.ai, openai, anthropic, etc.)
- `endpoint` · path canonical actuel utilisé par skill
- `model_family` · famille modèle sous-jacent (gemini_3_pro_image, gpt_image, claude_opus_4, etc.)
- `version_check_url` · URL docs vendor pour check latest version (consulté en audit manuel, PAS runtime)
- `version_canon_date` · date release version utilisée (YYYY-MM) · sert de référence pour audit fraîcheur
- `replaced_legacy` · endpoint précédent superseded (audit trail)
- `auto_upgrade` · `false` toujours v2.46 pragma (drop auto-switch silent · trop risqué, peut casser une release stable)

### Pas de runtime check (drop v2.46)

**v2.44 doctrine initiale** · exigeait check `version_check_url` avant tout call API externe + flag operator si nouvelle version dispo. **Drop v2.46** · trop strict, ralentit chaque call (latence HTTP), peut planter (URL down, parser breakage, false positive). Hardcoder un endpoint stable testé n'est pas un anti-pattern · c'est ship-readiness pragmatique.

### Audit manuel périodique (NEW v2.46)

Tous les 3-6 mois, run audit manuel ·

1. Lister tous les `permissions.external_apis[]` cross-skills (grep frontmatter)
2. Pour chaque entry, ouvrir `version_check_url` et vérifier latest version vendor-side
3. Si `version_canon_date` < 6 mois et latest = canon date → skip
4. Si nouvelle version release vendor-side → ticket migration (cycle release dédié, pas hot-patch)
5. Documenter audit dans `docs/internal/audits/model-versioning-{YYYY-MM}.md`

### Matrice cross-skill · le SSOT durable (NEW)

Les endpoints externes vivent désormais en deux endroits cohérents · le frontmatter `permissions.external_apis[]` par skill (la déclaration locale) ET `resources/canon/model-provider-matrix.json` (le SSOT cross-skill pour l'audit). La matrice fait pareil pour les tiers Claude · elle mappe chaque alias logique (`opus` / `sonnet` / `haiku`) vers son modèle concret du jour, son provider, et sa chaîne de repli. Au swap d'un modèle, on édite UN fichier (la matrice), pas les 85 frontmatters.

Deux propriétés ·

- **Découplage durabilité.** La matrice sépare le substrat MODÈLE-INDÉPENDANT (les alias, les tiers, la discipline de repli) des valeurs MODÈLE-DÉPENDANTES (les ids concrets, les endpoints). Seules les valeurs bougent au swap.
- **Détecteur de régression.** Après tout swap de valeur, relancer `evals/` (le harness qualité). Si un score chute, c'est la couche prompting model-dépendante (exemplars, nudges de posture) qu'il faut re-tuner, pas le substrat. C'est ce qui rend un swap sûr au lieu de silencieux.

**Vérif au build, pas au runtime.** `build-manifest.py` valide que chaque `recommended_model` existe dans `allowed_aliases` de la matrice · `--strict` en fait une release gate (exit 1 sur tout alias inconnu). Étage cohérent avec l'audit manuel · zéro coût runtime, la décision v2.46 (pas de check runtime) reste intacte.

**Pas de `model_fallback` par skill.** Le repli vit dans la matrice (par tier), dérivé pas dupliqué · un skill nomme son tier, la matrice porte la chaîne. On évite la copie cross-skill qui drifte.

### Audit log runtime (OPTIONNEL)

Chaque skill output PEUT logger ·
- Endpoint utilisé exact (path complet vendor/model/operation)
- Version date (YYYY-MM release model · depuis frontmatter)
- Latency call
- Cost/call si vendor fournit metric

C'est utile pour debug + tracking cost, mais pas blocker.

### Naming convention versions

Endpoints fal.ai canon · noter version dans path ·
- `nano-banana` (v1.0 · Gemini 2.5 Flash Image)
- `nano-banana-pro` (v1.5 · Gemini 2.5 Pro Image)
- `nano-banana-2` (v2.0 · Gemini 3 Pro Image novembre 2025)
- Check latest via audit manuel `https://fal.ai/models` listing

Pattern equivalent autres vendors ·
- OpenAI · `gpt-image-1` (v1.0 mai 2025) · `gpt-image-2` (à venir 2026)
- Anthropic · `claude-opus-4-8` (canon · 1M context)

## Application historique

- v2.44 ship doctrine initiale (runtime check + frontmatter)
- v2.44 craft-packshot v1.1 swap nano-banana-pro → nano-banana-2 (stress test produit canon 1 attempt vs 9 échouées)
- v2.46 doctrine pragma adapt · drop runtime check, audit manuel périodique
- v2.46 migration consumers cohérence ·
  - `compose-creative` v1.1 → v1.2 swap nano-banana-2
  - `recompose-creative` v1.1 → v1.2 swap nano-banana-2
  - `decompose-ad` v1.2 → v1.3 (reference endpoint canon downstream + frontmatter declared)

## Cross-refs

- `resources/canon/model-provider-matrix.json` (SSOT cross-skill · alias logique vers modèle concret + chaîne de repli + endpoints externes)
- `evals/` (détecteur de régression au swap de modèle · le harness qualité)
- `docs/system/skill-authoring-doctrine.md` (frontmatter permissions canon)
- `docs/system/compositional-cartography.md` (production loop canon)
- `docs/system/visual-identity-doctrine.md` v2.43 (chantier 1 fidélité)
- Memory user `feedback_model_versioning_check.md` (apprentissage S55 cycle USAGE)

## Rationale pragma (NEW v2.46)

Operator feedback session 2026-05-12 · "hardcoder un endpoint c'est pas hyper fou". L'objectif est éviter le drift silencieux (v2.43 vs v2.44 fail produit canon), pas builder un système enforcement runtime. Frontmatter annotation + audit manuel 3-6 mois = même outcome sans complexité runtime. Trade-off ·

| Approche | Drift detection | Runtime cost | Risk |
|---|---|---|---|
| Pas d'annotation (avant v2.44) | Manuel ad-hoc | 0 | Drift silencieux mois après mois |
| Runtime check (v2.44 initiale) | Auto chaque call | Latence + parser + URL down | Bloque ship si URL down |
| Annotation + audit manuel (v2.46) | Cycle 3-6 mois | 0 | Drift window de 3-6 mois acceptable |

L'audit manuel ne supprime pas le risque de drift, juste le borne à un horizon connu et opérationnel.
