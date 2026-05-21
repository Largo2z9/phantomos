---
name: update
description: Mise à jour du workspace PhantomOS vers la dernière version canon. Preserve tes brands + operator state. Migrations automatiques pour BREAKING changes. Backup + rollback canon.
version: v2.83.0
---

# /update · mise à jour workspace canon

> **Note · spec interne vs rendu opérateur runtime**
>
> Ce fichier mélange spec agent technique et rendu opérateur. Les blocs bash, paths `docs/internal/*`, noms de doctrines (EDD · OCD · DVD), iconographie canon, et Hard Rules sont consommés par l'agent uniquement et ne doivent JAMAIS apparaître dans le rendu opérateur runtime.
>
> Le rendu opérateur runtime utilise · prose française naturelle · langage DTC métier · 0 path technique · 0 nom de doctrine · 0 préfixe symbolique non-explicité · 0 jargon dev (Keep-a-Changelog · rsync · etc.).

Slash command pointer vers le pipeline d'update PhantomOS. Synchronise les fichiers canon (skills · doctrines · commands · templates) depuis `Largo2z9/phantomos` vers ton workspace local, sans toucher à tes brands, ton operator state ou ta config.

## Sources de vérité migrations (canon v2.83.0+)

| Source | Rôle | Quand lire |
|---|---|---|
| `docs/internal/releases/manifest/{version}-manifest.json` | **source de vérité migrations structurées** · steps détaillés · type (additive/transform/deprecate/breaking) · impact data | TOUJOURS · Step 2 plan migration |
| `CHANGELOG.md` (Keep-a-Changelog) | résumé exécutif sections Added/Changed/Removed/Fixed/Migration/Breaking | cross-ref si opérateur veut résumé court |
| `docs/internal/project-journal.md` | narrative archive contexte historique étendu | rarement (opérateur curieux mentionné explicitement) |

**Règle canon · les manifests JSON sont la source structurée des migrations · le CHANGELOG est résumé humain pas spec exécutable.**

## Mode detection

| Argument | Routing |
|---|---|
| `/update` empty | check version locale vs latest · propose update si delta · disclosure pré-update NIVEAU 0 |
| `/update --check` | just check, no apply · affiche version locale + latest + delta + plan théorique |
| `/update --force` | re-apply current version (cas debug rare · workspace désynchronisé) |
| `/update --rollback {version}` | revert vers backup `_archive/migrations/pre-{version}-{date}/` |

## Workflow canon

### Step 1 · Detect versions

Lire version locale + fetch latest tag depuis remote canon.

```bash
LOCAL_VERSION=$(python3 -c "import json; print(json.load(open('_version.json'))['template_version'])")
LATEST_TAG=$(gh api repos/Largo2z9/phantomos/releases/latest --jq '.tag_name' 2>/dev/null || echo "")
```

Si `gh` indisponible · fallback `git ls-remote --tags https://github.com/Largo2z9/phantomos.git | tail -1`.

### Step 2 · Construire plan migration depuis manifests JSON

Si `latest > local` · lister tous les manifests intermédiaires depuis `docs/internal/releases/manifest/{version}-manifest.json`.

**Source de vérité = manifests JSON · PAS CHANGELOG (résumé exécutif sans spec exécutable).**

Pour chaque step intermédiaire · lire le manifest correspondant et capturer ·
- `type` · additive · transform · deprecate · breaking
- `steps` · liste actions structurées
- `impact_data` · zéro / minor / major
- `breaking_changes` · si présent · liste explicite

```bash
for version in $(ls docs/internal/releases/manifest/ | sort -V); do
  if [[ "$version" > "$LOCAL_VERSION" && "$version" <= "${LATEST_TAG#v}" ]]; then
    MANIFEST="docs/internal/releases/manifest/${version}-manifest.json"
    TYPE=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['type'])")
    STEPS=$(python3 -c "import json; print(len(json.load(open('$MANIFEST'))['steps']))")
    echo "  v${version} · ${TYPE} · ${STEPS} steps"
  fi
done
```

Affichage opérateur ·

```
Migrations à apply ·
v2.82.1 → v2.83.0 (additive · 3 steps · zéro impact data)
v2.82.0 → v2.82.1 (additive · 2 steps · zéro impact data)
```

### Step 3 · Disclosure pré-update canon (EDD v2.79.5 + NIVEAU 0)

Avant tout backup ou rsync · poser les paramètres décomposés depuis manifests JSON. Format canon ·

```
/update · mise à jour workspace
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Paramètres posés
  ────────────────────────────────────────────────────────────────
  Version locale       v2.82.1
  Version latest       v2.83.0
  Migrations           1 step (v2.82.1 → v2.83.0 · additive · 3 actions)
  Type changement      Additive · zéro impact data
  Brands préservées    1 (mykara-care)
  Operator state       préservé (awareness · session-state · todos)
  Backup destination   _archive/migrations/pre-v2.83.0-2026-05-19/

  Plan (steps manifest)
  ────────────────────────────────────────────────────────────────
  1. Backup brands/ + operator/ + .phantom/ vers _archive/migrations/
  2. Rsync canon workspace-template (exclude operator state)
  3. Apply migration scripts si BREAKING (additive ici · skip)
  4. Validate state post-update
  5. Confirm + cleanup temp

  ETA           ~30-60 secondes (additive · pas de transform)
  Implication   Tes brands + operator state préservés strict
  Livrable      Workspace v2.83.0 · brands intacts · backup dispo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour update ? ou tu rollback un autre jour ?
```

Attendre confirmation explicite avant de continuer (sauf `--force` qui short-circuite).

### Step 4 · Backup operator state

Rsync sélectif vers `_archive/migrations/pre-v{X.Y.Z}-{date}/` · ne backup QUE ce qui appartient à l'opérateur.

```bash
BACKUP_DIR="_archive/migrations/pre-${LATEST_TAG#v}-$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"
rsync -a \
  --include='brands/***' \
  --include='operator/***' \
  --include='.phantom/***' \
  --include='.workflow.json' \
  --include='credentials*.env' \
  --include='todos.md' \
  --exclude='*' \
  ./ "$BACKUP_DIR/"
```

Confirmer taille backup + chemin avant rsync canon.

### Step 5 · Apply update (rsync canon depuis remote)

Cloner remote canon en `/tmp` · checkout tag latest · rsync vers workspace en excluant strict tout l'operator state.

```bash
TMP_DIR="/tmp/phantomos-update-$$"
git clone https://github.com/Largo2z9/phantomos.git "$TMP_DIR"
cd "$TMP_DIR"
git checkout "$LATEST_TAG"
cd -
rsync -a --delete \
  --exclude='.git' \
  --exclude='.DS_Store' \
  --exclude='credentials_shared.env' \
  --exclude='credentials.env' \
  --exclude='brands/' \
  --exclude='operator/' \
  --exclude='.phantom/' \
  --exclude='.workflow.json' \
  --exclude='_archive/' \
  "$TMP_DIR/" ./
rm -rf "$TMP_DIR"
```

Les exclusions sont strictes · zéro fichier opérateur ne doit être écrasé. Si un fichier est ambigu (canon ET opérateur · ex `todos.md` racine) · privilégier la version opérateur.

### Step 6 · Apply migrations si BREAKING

Pour chaque step intermédiaire `> LOCAL_VERSION && <= LATEST_TAG` · lire `docs/internal/releases/manifest/{version}-manifest.json` champ `type`. Si `schema-bump` · `transform` · `breaking` · run le script de migration correspondant.

```bash
for MIGRATION in $(ls migrations/*.py 2>/dev/null | sort); do
  MIG_VERSION=$(basename "$MIGRATION" .py | cut -d- -f1)
  if [[ "$MIG_VERSION" > "$LOCAL_VERSION" && "$MIG_VERSION" <= "${LATEST_TAG#v}" ]]; then
    python3 "$MIGRATION" --apply
  fi
done
```

Sur additive · skip (rien à transformer). Sur schema-bump · déléguer à skill `migrate-workspace` pour chaque brand. Référence canon · champ `breaking_changes` du manifest JSON liste explicite des transformations attendues.

### Step 7 · Validate state post-update

Run `validate-resources` canon · vérifier intégrité brands + operator state + cohérence `_version.json`.

```bash
python3 .skills/skills/validate-resources/validate.py --all 2>&1 | tail -20
```

Si validation échoue · proposer rollback automatique vers backup créé Step 4.

### Step 8 · Confirm output canon

Format final ·

```
✓ Workspace mis à jour v2.82.1 → v2.83.0
✓ Brands préservées (1) · operator state préservé
✓ Backup disponible si besoin de rollback
✓ Rollback path · /update --rollback v2.82.1

Nouveautés v2.83.0 ·
- Ajout de la doctrine changelog (séparation propre par usage)
- Refonte du fichier changelog pour meilleure lisibilité
- Ajout d'une archive narrative du projet
```

Note pour l'agent · le rendu opérateur runtime traduit les préfixes Keep-a-Changelog (`+/~/-/✓/→/⚠`) en langage naturel (Ajout · Refonte · Suppression · Correction · Migration · Attention). Aucun préfixe symbolique ne doit apparaître dans le rendu opérateur. Aucun path technique (`docs/internal/*`) ne doit être cité. Aucune mention "Keep-a-Changelog" ou "sections Added/Changed". L'opérateur voit la prose, l'agent maintient les préfixes en interne (`CHANGELOG.md` canon).

## Mode --rollback

`/update --rollback {version}` revert canon ·

1. Detect backup dans `_archive/migrations/pre-{version}-*/`
2. Disclosure pré-rollback (paramètres · plan · implications)
3. Rsync inverse backup → workspace
4. Update `_version.json` vers version cible
5. Confirm + suggest validation

## Iconographie canon v2.79.2 (interne agent · jamais rendu opérateur)

| Icône | Sens |
|---|---|
| ✓ | done · validé · OK |
| ◐ | partiel · en cours · partial state |
| ○ | todo · pas encore fait |
| ✗ | failed · erreur · blocage |
| ⚠ | attention · warning · friction |

Iconographie réservée aux slash commands matriciels (`/phantom` · `/bird` · `/breakdown` · `/about`). `/update` n'est pas matriciel · l'agent peut utiliser `✓` ponctuellement quand un statut binaire est vraiment informatif (e.g. confirmation update réussie Step 8), JAMAIS de légende explicite au pied du rendu opérateur runtime.

## Préfixes Keep-a-Changelog canon

| Préfixe | Section CHANGELOG | Sens |
|---|---|---|
| `+` | Added | nouvelle feature · ajout canon |
| `~` | Changed | refactor · update existant |
| `-` | Removed | suppression · deprecate |
| `✓` | Fixed | bugfix · correction |
| `→` | Migration | migration auto v{X} → v{Y} |
| `⚠` | Breaking | breaking change · attention requise |

## Hard Rules runtime (interne agent · jamais citées en rendu opérateur)

> Note pour l'agent · ces règles sont des contraintes d'exécution internes. Ne jamais les citer ni leur format `HR ·` dans le rendu opérateur runtime. L'opérateur voit la conséquence (backup créé · état préservé · rollback proposé), pas la règle.

- HR · TOUJOURS backup avant apply (Step 4 non-négociable)
- HR · TOUJOURS preserve operator state (rsync exclude strict · `brands/` · `operator/` · `.phantom/` · `.workflow.json` · `credentials*.env`)
- HR · TOUJOURS valider post-update (Step 7 non-négociable)
- HR · TOUJOURS proposer rollback path dans output final
- HR · TOUJOURS disclosure pré-update NIVEAU 0 (cohérent EDD v2.79.5) avant tout rsync
- HR · TOUJOURS lire migrations détaillées depuis manifests JSON (source de vérité structurée) · PAS CHANGELOG (résumé exécutif humain)
- HR · TOUJOURS attendre confirmation explicite (sauf `--force` ou `--check`)
- HR · JAMAIS écraser un fichier opérateur ambigu sans demander
- HR · JAMAIS commit auto post-update · l'opérateur décide
- HR · JAMAIS exposer paths `docs/internal/*` ni `Keep-a-Changelog` ni noms de doctrines (EDD · OCD · DVD · etc.) dans le rendu opérateur runtime · paths techniques restent pour la spec agent uniquement

## Cross-refs canon

- `docs/system/update-distribution-doctrine.md` v2.80.0 · doctrine racine update pipeline
- `docs/system/engagement-disclosure-doctrine.md` v2.79.5 · disclosure pattern NIVEAU 0
- `docs/system/changelog-doctrine.md` v2.83.0 · doctrine split CHANGELOG / project-journal / manifests
- `.skills/skills/update-workspace/SKILL.md` · skill orchestrator sous-jacent
- `.skills/skills/migrate-workspace/SKILL.md` · skill schema migration brand-by-brand
- `/version` · pair canon · affiche état version sans muter
- `docs/internal/releases/manifest/{version}-manifest.json` · source de vérité migrations structurées
- `CHANGELOG.md` · résumé exécutif Keep-a-Changelog (cross-ref opérateur)
- `docs/internal/project-journal.md` · narrative archive contexte historique
